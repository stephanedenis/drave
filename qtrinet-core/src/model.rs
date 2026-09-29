//! Inférence Qwen2 en **mode listes d'événements** — std seul, sans GPU, sans
//! bibliothèque de tenseurs.
//!
//! Chaque matrice de poids est stockée en listes par source
//! (`PushMat` : écart de sortie en varint + valeur int8) et parcourue par le
//! moteur d'événements (`Pool`). Les activations sont quantifiées en int8 à la
//! volée, une échelle par vecteur : le produit est **entier**, l'échelle ne
//! revient qu'une fois par sortie.
//!
//! Seule exception : la tête de sortie (151 936 sorties) est calculée par
//! produits scalaires sur les lignes Q8_0 d'origine. En mode push il faudrait un
//! accumulateur de 151 936 × 8 octets **par worker** (36 Mo) et chaque sortie
//! serait écrite 896 fois : le déséquilibre est structurel, pas un compromis de
//! précision. Le reste du modèle — 99,7 % des poids — passe par les événements.

use crate::engine::{Pool, SparseVec};
use crate::gguf::Gguf;
use crate::list::{DenseQ4, DenseQ8, PushMat};
use std::time::Instant;

// --------------------------------------------------------------------------- //
// Configuration
// --------------------------------------------------------------------------- //

pub struct Cfg {
    pub n_layer: usize,
    pub hidden: usize,
    pub n_head: usize,
    pub n_kv_head: usize,
    pub head_dim: usize,
    pub ffn: usize,
    pub eps: f32,
    pub rope_base: f32,
    pub vocab: usize,
    /// MoE : nombre d'experts, combien sont allumés par jeton, et leur taille
    /// intermédiaire. `n_expert = 0` pour un modèle dense.
    pub n_expert: usize,
    pub n_expert_used: usize,
    pub ffn_exp: usize,
    /// Activation du FFN. gpt-oss n'utilise **pas** SiLU : c'est
    /// `g·σ(1,702·g)·(u+1)`, avec `g` et `u` écrêtés à ±7 — une sigmoïde
    /// rapide de type GELU, et un décalage de `up` de +1. Prendre SiLU par
    /// défaut donne une perplexité de 1 396 au lieu de la bonne.
    pub ffn_act_oss: bool,
    /// Convention de routage. Qwen3-MoE : softmax sur **tous** les experts,
    /// puis top-k, puis renormalisation. gpt-oss : top-k sur les logits
    /// **bruts**, puis softmax sur les seuls retenus — les deux donnent des
    /// poids très différents.
    pub routeur_topk_softmax: bool,
    /// Dimensions réellement tournées par tête. gpt-oss n'en tourne que la
    /// moitié (`partial_rotary_factor = 0,5`), là où Qwen et Llama tournent
    /// toute la tête.
    pub n_rot: usize,
    /// Étirement de contexte YaRN : `(facteur, beta_rapide, beta_lent,
    /// contexte d'origine)`. `None` pour un RoPE ordinaire.
    pub yarn: Option<(f32, f32, f32, f32, bool)>,
}

/// Une projection, dans l'un des deux formats, plus son biais éventuel.
/// `m` = listes d'événements (architecture du projet) ;
/// `d` = matrice dense int8 (référence de comparaison, sans événements).
pub struct Proj {
    /// Copie GPU des poids (sources Q8_0), si le déport est actif.
    pub gpu: Option<crate::gpu::MatriceGpu>,
    pub m: Option<PushMat>,
    pub d: Option<DenseQ8>,
    /// Variante 4 bits de la forme dense (0,5 octet/poids). Exclusif de `d`.
    pub q4: Option<DenseQ4>,
    pub bias: Option<Vec<f32>>,
}

/// Type ggml → origine des blocs pour `Vue4`.
fn source_de(t: u32) -> Option<crate::list::Source> {
    use crate::gguf::{GGML_MXFP4, GGML_Q4_0, GGML_Q4_K, GGML_Q6_K};
    use crate::list::Source;
    match t {
        GGML_Q4_K => Some(Source::Q4_K),
        GGML_Q6_K => Some(Source::Q6_K),
        GGML_MXFP4 => Some(Source::Mxfp4),
        GGML_Q4_0 => Some(Source::Q4_0),
        _ => None,
    }
}

/// Charge le mélange d'experts d'une couche, s'il existe.
///
/// Les trois tenseurs `ffn_*_exps` sont des tenseurs **3D** dont la première
/// dimension (la plus lente) est l'expert : chaque expert est donc un bloc
/// contigu, et le moteur n'a besoin que d'un pointeur et d'un pas.
fn charger_moe(g: &Gguf, l: usize, n_expert: usize) -> Option<Moe> {
    if n_expert == 0 { return None; }
    let p = |s: &str| format!("blk.{l}.{s}");
    let vue = |nom: &str| -> Option<Vue4> {
        let t = g.tensor(nom)?;
        if t.dims.len() < 3 || t.dims[0] as usize != n_expert { return None; }
        let src = source_de(t.ttype)?;
        let (n_out, n_in) = (t.dims[1] as usize, t.dims[2] as usize);
        let bloc = if t.ttype == crate::gguf::GGML_Q4_K || t.ttype == crate::gguf::GGML_Q6_K { 256 } else { 32 };
        if n_in % bloc != 0 { return None; }
        Some(Vue4 { base: g.data_ptr(nom)?, n_out, n_in, nb: n_in / bloc, src })
    };
    let gate = vue(&p("ffn_gate_exps.weight"))?;
    let up = vue(&p("ffn_up_exps.weight"))?;
    let down = vue(&p("ffn_down_exps.weight"))?;
    let routeur = g.dequant(&p("ffn_gate_inp.weight"));
    assert_eq!(routeur.len(), n_expert * gate.n_in, "routeur de taille inattendue");
    // Expert partagé (Qwen3-MoE d'origine, DeepSeek) : toujours actif.
    let shexp = match (vue(&p("ffn_gate_shexp.weight")), vue(&p("ffn_up_shexp.weight")),
                       vue(&p("ffn_down_shexp.weight"))) {
        (Some(a), Some(b), Some(c)) => Some((a, b, c)),
        _ => None,
    };
    let n_ff = gate.n_out;
    let biais = |nom: &str| -> Option<Vec<f32>> {
        let t = g.tensor(nom)?;
        // ne = (n_ff, n_expert) : l'expert est la dimension la plus lente.
        if t.dims.len() != 2 || t.dims[0] as usize != n_expert { return None; }
        Some(g.dequant(nom))
    };
    let routeur_biais = if g.tensor(&p("ffn_gate_inp.bias")).is_some() {
        Some(g.dequant(&p("ffn_gate_inp.bias")))
    } else { None };
    Some(Moe {
        routeur, routeur_biais,
        biais_gate: biais(&p("ffn_gate_exps.bias")),
        biais_up: biais(&p("ffn_up_exps.bias")),
        biais_down: biais(&p("ffn_down_exps.bias")),
        n_ff, gate, up, down, shexp,
    })
}

/// Vue sur un tenseur déjà quantifié, découpable **par expert**. Les experts
/// sont empilés dans un tenseur 3D et **contigus** : l'expert `e` commence à
/// `base + e × n_out × nb × pas`. Aucune copie, aucun découpage préalable.
#[derive(Clone, Copy)]
pub struct Vue4 {
    pub base: *const u8,
    pub n_out: usize,
    pub n_in: usize,
    pub nb: usize,
    pub src: crate::list::Source,
}

impl Vue4 {
    fn pas(&self) -> usize {
        use crate::list::Source::*;
        match self.src {
            Q4_K => crate::gguf::TAILLE_Q4K,
            Q6_K => crate::gguf::TAILLE_Q6K,
            Mxfp4 => 17,
            Q4_0 => 18,
            Propre => 0,
        }
    }

    /// Matrice 4 bits de l'expert `e`, **empruntée** au fichier.
    fn expert(&self, e: usize) -> crate::list::DenseQ4 {
        let base = unsafe { self.base.add(e * self.n_out * self.nb * self.pas()) };
        unsafe {
            match self.src {
                crate::list::Source::Q4_K =>
                    crate::list::DenseQ4::emprunter_q4k(base, self.n_out, self.n_in, self.nb),
                crate::list::Source::Q6_K =>
                    crate::list::DenseQ4::emprunter_q6k(base, self.n_out, self.n_in, self.nb),
                crate::list::Source::Mxfp4 =>
                    crate::list::DenseQ4::emprunter(base, self.n_out, self.n_in, self.nb, true),
                _ => crate::list::DenseQ4::emprunter(base, self.n_out, self.n_in, self.nb, false),
            }
        }
    }
}

unsafe impl Send for Vue4 {}
unsafe impl Sync for Vue4 {}

/// Mélange d'experts : un routeur (petit, en f32) et trois tenseurs empilés.
pub struct Moe {
    /// Routeur `[n_expert × n_embd]`, rangée par expert, en f32.
    pub routeur: Vec<f32>,
    /// Biais du routeur (gpt-oss en a un) : ajouté aux logits **avant** le
    /// softmax.
    pub routeur_biais: Option<Vec<f32>>,
    /// Biais par expert, `[n_expert × n_ff]` : chaque expert a les siens, pour
    /// ses trois projections. Absents chez Qwen3-MoE, présents chez gpt-oss.
    pub biais_gate: Option<Vec<f32>>,
    pub biais_up: Option<Vec<f32>>,
    pub biais_down: Option<Vec<f32>>,
    pub n_ff: usize,
    pub gate: Vue4,
    pub up: Vue4,
    pub down: Vue4,
    /// Expert partagé, toujours actif (certains modèles seulement).
    pub shexp: Option<(Vue4, Vue4, Vue4)>,
}

pub struct Layer {
    pub attn_norm: Vec<f32>,
    pub wq: Proj,
    pub wk: Proj,
    pub wv: Proj,
    pub wo: Proj,
    pub ffn_norm: Vec<f32>,
    /// RMSNorm appliquée à chaque tête de Q et de K après projection
    /// (Qwen3, Gemma 3…). Absente ailleurs.
    pub q_norm: Option<Vec<f32>>,
    pub k_norm: Option<Vec<f32>>,
    /// Puits d'attention **appris** : un logit par tête, ajouté aux scores
    /// comme une clé virtuelle dont la valeur est nulle. Elle ne contribue
    /// qu'au dénominateur du softmax — c'est le « drain » que les modèles
    /// récents (gpt-oss) apprennent au lieu de le bricoler.
    pub sinks: Option<Vec<f32>>,
    pub wgate: Proj,
    pub wup: Proj,
    pub wdown: Proj,
    /// Rempli pour les modèles à mélange d'experts ; `wgate/wup/wdown` sont
    /// alors vides.
    pub moe: Option<Moe>,
}

pub struct Stats {
    pub events: u64,
    pub prompt_s: f64,
    pub gen_s: f64,
    pub n_prompt: usize,
    pub n_gen: usize,
}

// --------------------------------------------------------------------------- //
// Chargement
// --------------------------------------------------------------------------- //

/// Élague chaque ligne de sortie en ne gardant que la fraction `keep` des poids
/// de plus grande magnitude. C'est le levier qui compte pour le moteur : son
/// coût est proportionnel au nombre de **non-zéros**, pas à la largeur des
/// valeurs. `keep = 1.0` ne touche à rien.
fn prune_rows(w: &mut [f32], n_out: usize, n_in: usize, keep: f32) {
    if keep >= 1.0 { return; }
    let k = ((n_in as f32 * keep) as usize).max(1);
    let mut abs = vec![0f32; n_in];
    for o in 0..n_out {
        let row = &mut w[o * n_in..(o + 1) * n_in];
        for (i, &v) in row.iter().enumerate() { abs[i] = v.abs(); }
        // seuil = k-ième plus grande magnitude (sélection en O(n))
        let (_, &mut seuil, _) = abs.select_nth_unstable_by(n_in - k, |a, b| a.partial_cmp(b).unwrap());
        for v in row.iter_mut() { if v.abs() < seuil { *v = 0.0; } }
    }
}

/// Élagage **structuré** : pour chaque source (entrée), on ne garde qu'une
/// fenêtre contiguë de destinations, centrée sur la plus forte. Les listes
/// d'événements deviennent des suites d'écarts de 1 — c'est la forme que
/// produiraient des grappes efférentes imposées à l'entraînement.
fn prune_structured(w: &mut [f32], n_out: usize, n_in: usize, keep: f32) {
    if keep >= 1.0 { return; }
    let win = ((n_out as f32 * keep) as usize).max(1);
    for i in 0..n_in {
        let mut best_o = 0usize;
        let mut best = 0f32;
        for o in 0..n_out {
            let a = w[o * n_in + i].abs();
            if a > best { best = a; best_o = o; }
        }
        let lo = best_o.saturating_sub(win / 2);
        let hi = (lo + win).min(n_out);
        for o in 0..n_out {
            if o < lo || o >= hi { w[o * n_in + i] = 0.0; }
        }
    }
}

/// Construit une matrice int8 : **une échelle par bloc de 32** (`QT_Q8_BLOCS=1`,
/// la disposition de Q8_0) ou une par ligne (défaut historique).
///
/// L'hypothèse testée : si le 6 bits bat notre int8, c'est peut-être grâce à ses
/// échelles par bloc de 32 et non grâce à ses deux bits supplémentaires.
fn construire_q8(w: &[f32], n_out: usize, n_in: usize) -> DenseQ8 {
    if std::env::var("QT_Q8_BLOCS").is_ok() && n_in % 32 == 0 {
        DenseQ8::build_blocs(w, n_out, n_in)
    } else {
        DenseQ8::build(w, n_out, n_in)
    }
}

impl Proj {
    /// Projection vide : les modèles à experts n'ont **pas** de tenseur FFN
    /// dense, et le moteur ne doit pas le chercher.
    pub fn vide() -> Self {
        Proj { gpu: None, m: None, d: None, q4: None, bias: None }
    }

    fn load(g: &Gguf, name: &str, bias: Option<&str>, dense: bool, auto: bool, keep: f32,
            q4: bool, bits6: bool) -> Self {
        let t = g.tensor(name).unwrap_or_else(|| panic!("tenseur {name} absent"));
        let n_out = t.dims[0] as usize;
        let n_in = t.dims[1] as usize;
        let mut w = g.dequant(name);
        if keep < 0.0 { prune_structured(&mut w, n_out, n_in, -keep); }
        else { prune_rows(&mut w, n_out, n_in, keep); }
        // `auto` charge les DEUX formes : le moteur choisit ensuite, par mesure
        // de la densité d'activation, entre dispersion (push) et produit
        // scalaire dense (pull). Le croisement mesuré est à 10 %.
        // Six bits empaquetés : même déquantification que les autres chemins,
        // mais la quantification vise la grille [-32, 31] au lieu de [-8, 7].
        if bits6 {
            let z = DenseQ4::build6(&w, n_out, n_in);
            let bias = bias.filter(|b| g.tensor(b).is_some()).map(|b| g.dequant(b));
            return Proj { gpu: None, m: None, d: None, q4: Some(z), bias };
        }
        let (m, d, q4v) = if q4 {
            // Source déjà en Q4_0 : on importe les blocs tels quels. Sinon on
            // quantifie depuis les f32 (une seule couche d'erreur, pas deux).
            // Import VERBATIM quand la source est déjà en 4 bits : MXFP4
            // (gpt-oss) puis Q4_0 (llama.cpp). Sinon, quantification depuis
            // les f32 — une seule couche d'erreur, jamais deux.
            // EMPRUNT, pas copie : on lit les blocs dans le fichier déjà
            // chargé. Recopier dans notre disposition doublerait la mémoire
            // (60 Go de fichier + 61 Go de copie pour gpt-oss-120b).
            if let Some((buf, nb)) = g.q6k_blocks(name) {
                (None, None, Some(unsafe { DenseQ4::emprunter_q6k(buf.as_ptr(), n_out, n_in, nb) }))
            } else if let Some((buf, nb)) = g.q4k_blocks(name) {
                // Q4_K : super-blocs de 256 poids lus en place. Aucune copie,
                // aucune requantification — la fidélité est par construction.
                (None, None, Some(unsafe { DenseQ4::emprunter_q4k(buf.as_ptr(), n_out, n_in, nb) }))
            } else if let Some((buf, nb)) = g.mxfp4_blocks(name) {
                (None, None, Some(unsafe { DenseQ4::emprunter(buf.as_ptr(), n_out, n_in, nb, true) }))
            } else if let Some((buf, nb)) = g.q4_blocks(name) {
                (None, None, Some(unsafe { DenseQ4::emprunter(buf.as_ptr(), n_out, n_in, nb, false) }))
            } else {
                (None, None, Some(DenseQ4::build(&w, n_out, n_in)))
            }
        } else if dense {
            // Source déjà en Q8_0 et aucun élagage : on EMPRUNTE les blocs au
            // lieu de les reconstruire depuis les f32 (copie == taille du
            // modèle, plus un transitoire f32 de quatre fois cette taille).
            // `QT_SANS_EMPRUNT=1` force la reconstruction : c'est ce qui permet
            // de comparer nos deux schémas d'échelle à la référence empruntée.
            let emprunt = keep >= 1.0 && std::env::var("QT_SANS_EMPRUNT").is_err();
            match (emprunt, g.q8_blocks(name)) {
                (true, Some((buf, nb))) =>
                    (None, Some(unsafe { DenseQ8::emprunter_q8(buf.as_ptr(), n_out, n_in, nb) }), None),
                _ => (None, Some(construire_q8(&w, n_out, n_in)), None),
            }
        } else if auto {
            let emprunt = keep >= 1.0 && std::env::var("QT_SANS_EMPRUNT").is_err();
            let dense8 = match (emprunt, g.q8_blocks(name)) {
                (true, Some((buf, nb))) =>
                    unsafe { DenseQ8::emprunter_q8(buf.as_ptr(), n_out, n_in, nb) },
                _ => construire_q8(&w, n_out, n_in),
            };
            (Some(PushMat::build(&w, n_out, n_in)), Some(dense8), None)
        } else {
            (Some(PushMat::build(&w, n_out, n_in)), None, None)
        };
        // Tous les modèles n'ont pas de biais QKV (Qwen3 n'en a pas) : son
        // absence est normale, pas une erreur.
        let bias = bias.filter(|b| g.tensor(b).is_some()).map(|b| g.dequant(b));
        // Déport GPU : les poids Q8_0 montent UNE fois ; ensuite chaque jeton
        // ne fait traverser que les activations.
        // Seuil fixé par la mesure, pas par le raisonnement :
        //   FFN du 0,5B, 4,6 Mo : CPU 123 µs, GPU 151 µs → le CPU gagne ;
        //   attention de gpt-oss, 12,5 Mo : CPU 216 µs, GPU 187 µs → le GPU gagne.
        // Le croisement est entre les deux. L'aller-retour coûte ~60 µs, presque
        // tout en latence de lancement et de synchronisation : c'est ce qu'il
        // faudra réduire (lancements groupés, flux) avant de descendre le seuil.
        const SEUIL_GPU: usize = 8 << 20;
        let gpu = match (&d, crate::gpu::instance()) {
            (Some(d8), Some(machine))
                if d8.src == crate::list::Source8::Q8_0 && keep >= 1.0
                   && n_out * d8.nb_ligne * 34 >= SEUIL_GPU => {
                let octets = n_out * d8.nb_ligne * 34;
                let blocs = unsafe { std::slice::from_raw_parts(d8.base, octets) };
                machine.charger_proj(blocs, n_out, d8.nb_ligne)
            }
            _ => None,
        };
        Proj { gpu, m, d, q4: q4v, bias }
    }
}

pub struct Model {
    pub g: Gguf,
    pub cfg: Cfg,
    pub layers: Vec<Layer>,
    pub out_norm: Vec<f32>,
    pub pool: Pool,
    /// cache KV, par couche : `[n_kv_head × ctx × head_dim]`, en f32 ou quantifié
    kv: Vec<KvCache>,
    pub ctx: usize,
    pub events: u64,
    /// Nombre de niveaux de quantification des **activations** (127 pour int8,
    /// 32767 pour int16). Les poids restent int8 : c'est la précision de
    /// l'activation qui décide de la fidélité au modèle flottant.
    pub act_levels: f32,
    /// Parcimonie **imposée** à l'inférence, sans aucun entraînement.
    /// `act_thresh` écarte les activations sous cette fraction du maximum du
    /// vecteur ; `act_topk` ne garde que les k plus grandes. Les deux imitent
    /// l'effet du seuil d'un neurone à décharge sur un modèle préentraîné
    /// ordinaire — c'est la seule façon d'obtenir un débit variable sans
    /// réentraîner quoi que ce soit.
    pub act_thresh: f32,
    pub act_topk: usize,
    /// Renormalisation homéostatique : après k-WTA, les activations conservées
    /// sont remises à l'échelle pour que leur norme L1 égale celle du vecteur
    /// complet. La coupure retire de l'énergie ; ceci la compense.
    pub act_renorm: bool,
    /// Parcimonie par projection : 0 = q, 1 = k, 2 = v, 3 = o, 4 = gate,
    /// 5 = up, 6 = down. La valeur 0 signifie « utiliser act_topk ».
    pub act_topk_proj: [usize; 7],
    /// Attention à k clés : ne garder que les k plus grands scores par requête.
    /// 0 = attention dense avec softmax (le modèle d'origine).
    /// Cela rend la matrice d'attention **creuse**, donc exprimable en liste
    /// d'événements — au prix d'une approximation, mesurable.
    pub attn_topk: usize,
    /// Événements d'attention : paires (requête, clé) retenues, cumulées.
    /// C'est la taille de la liste d'événements que l'attention creuse produirait.
    pub attn_events: u64,
    /// Parcimonie de Q et K, en millièmes de la dimension PAR TÊTE. Les scores
    /// d'attention se calculent sur toutes les clés ; leur coût est donc
    /// O(d) par clé. Creuser Q et K rend ce produit scalaire creux — c'est la
    /// seule façon d'attaquer le poste dominant. 0 = désactivé.
    pub qk_topk: usize,
    /// Fenêtre d'attention glissante : ne noter que les `attn_window` dernières
    /// clés, plus `attn_sinks` jetons puits au début de la séquence.
    /// 0 = attention complète. Si la qualité tient, le coût des scores cesse
    /// d'être O(N) — c'est le seul moyen d'attaquer le poste dominant.
    /// Nombre d'experts allumés par jeton (0 = valeur du modèle).
    pub moe_topk: usize,
    /// **Profilage des neurones « chauds »** (idée de PowerInfer) : pour chaque
    /// couche FFN, le nombre de fois où chaque neurone intermédiaire s'active.
    /// Un neurone est « actif » au sens du moteur : sa valeur quantifiée n'est
    /// pas nulle, c'est-à-dire `|a| > max|a| / (2 × niveaux)` — le même critère
    /// que le chemin par événements. `None` = profilage éteint.
    pub profil_neurones: Option<(Vec<u64>, Vec<f64>)>,   // (tirs, somme des |a|)
    /// L'analogue MoE des neurones chauds : combien de fois chaque expert est
    /// choisi, par couche. C'est LA question de placement qui compte pour
    /// gpt-oss (4 experts sur 128 par jeton).
    pub profil_experts: Option<Vec<u64>>,
    pub profil_jetons: u64,
    pub attn_window: usize,
    /// Période du motif fenêtre/plein : la couche `l` est fenêtrée si
    /// `l % motif < motif - 1`. gpt-oss déclare 128 de fenêtre sur **une couche
    /// sur deux** (`layer_types` alterne sliding_attention / full_attention,
    /// et llama.cpp pose `set_swa_pattern(2)`) : appliquer la fenêtre aux
    /// 36 couches supprimait toute information au-delà de 128 jetons dans la
    /// moitié du réseau. 0 ou 1 = toutes les couches fenêtrées.
    pub swa_pattern: usize,
    pub attn_sinks: usize,
    /// Seuil de bascule push/pull, en fraction de sources actives. Mesuré : les
    /// deux architectures se croisent à 10 % de densité ; on bascule un peu
    /// au-dessus pour absorber la marge d'erreur.
    pub seuil_push: f32,
    /// Token d'arrêt (EOS / <|im_end|>) : la génération s'interrompt dessus.
    pub stop_id: Option<u32>,
    /// Second jeton d'arrêt : gpt-oss termine par `<|return|>` **ou**
    /// `<|end|>` selon le canal.
    pub stop_id2: Option<u32>,
    /// Postes de temps cumulés, en secondes (diagnostic).
    pub prof: [f64; 6],
    /// Nom du tenseur de la tête de sortie : `output.weight` s'il existe,
    /// sinon `token_embd.weight` (poids liés). Les modèles non liés — le
    /// Qwen2.5-1.5B en fait partie — ont une matrice de sortie **différente**
    /// de la table d'embedding ; lire la mauvaise donne une perplexité de
    /// 50 000 au lieu de 11,4.
    pub tete: String,
    /// Nombre de couches dont les puits appris ont été trouvés (diagnostic).
    pub sinks_vus: usize,
    /// Chemin GPU : la tête et les projections y résident en permanence. Les
    /// poids ne traversent le bus qu'une fois ; seules les activations font
    /// l'aller-retour à chaque jeton.
    pub tete_gpu: Option<crate::gpu::MatriceGpu>,
    /// Tête de sortie en 4 bits (poids liés au plafond d'embedding). C'est la
    /// plus grosse matrice du modèle — 151 936 × 896 — donc le poste où le
    /// demi-octet par poids rapporte le plus.
    pub head4: Option<DenseQ4>,
    /// Greffon : un neurone supplémentaire, chargé sans réentraînement.
    pub patch: Option<Patch>,
    /// Gain appliqué à la sortie du FFN d'une couche : édition structurelle de
    /// granularité supérieure (elle porte sur les 4 864 neurones à la fois).
    pub ffn_gain: Option<(usize, f32)>,
    /// Capteur hebbien : accumule la trace de co-activation d'une projection
    /// pendant l'inférence, sur un cœur séparé en pratique. Il ne modifie
    /// jamais le calcul — c'est un espion, pas un acteur.
    pub hebb: Option<Hebb>,
}

/// Un neurone ajouté à une couche, sans réentraînement du reste du modèle.
///
/// Il suit la forme SwiGLU du réseau : `a = silu(u·x) · (v·x)`, contribution
/// `a · d` ajoutée au flux résiduel. Le point important : **le produit de deux
/// formes linéaires est quadratique**. Prendre `u` sur une ligne existante de
/// `gate` et `v` sur une AUTRE ligne de `up` fabrique une caractéristique que le
/// réseau n'a jamais calculée — les 4 864 neurones d'origine n'apparient que
/// `gate[i]` avec `up[i]`.
///
/// Format binaire du fichier (little-endian) :
///   magie "QPAT" | version u32 | couche u32 | n u32 | n f32 (u) | n f32 (v) | n f32 (d)
pub struct Patch {
    pub layer: usize,
    pub u: Vec<f32>,
    pub v: Vec<f32>,
    pub d: Vec<f32>,
}

impl Patch {
    pub fn load(path: &str) -> std::io::Result<Patch> {
        use std::io::Read;
        let mut buf = Vec::new();
        std::fs::File::open(path)?.read_to_end(&mut buf)?;
        if buf.len() < 16 || &buf[0..4] != b"QPAT" {
            return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, "magie QPAT absente"));
        }
        let g = |o: usize| u32::from_le_bytes(buf[o..o+4].try_into().unwrap()) as usize;
        let (layer, n) = (g(8), g(12));
        let f = |base: usize| (0..n).map(|i| {
            let o = base + 4*i;
            f32::from_le_bytes(buf[o..o+4].try_into().unwrap())
        }).collect::<Vec<f32>>();
        Ok(Patch { layer, u: f(16), v: f(16 + 4*n), d: f(16 + 8*n) })
    }
}

/// Trace hebbienne d'une projection : `H[o][i] += y[o] · x[i]` accumulée sur
/// les seules sorties qui « déchargent » (|y| au-dessus du quantile), ce qui est
/// le principe neuromorphique : seuls les neurones qui tirent apprennent.
pub struct Hebb {
    pub layer: usize,
    pub quantile: f32,
    pub n_out: usize,
    pub n_in: usize,
    pub h: Vec<f32>,
    pub n_fire: u64,
    pub n_token: u64,
    /// Journal : vecteur d'entrée de la couche à chaque token, pour l'analyse
    /// hors ligne. C'est la « journalisation en vue d'une version ultérieure ».
    pub log: Vec<f32>,
    pub log_on: bool,
}

impl Hebb {
    pub fn new(layer: usize, n_out: usize, n_in: usize, quantile: f32) -> Self {
        Hebb { layer, quantile, n_out, n_in, h: vec![0f32; n_out * n_in],
               n_fire: 0, n_token: 0, log: Vec::new(), log_on: false }
    }

    /// Accumule une paire (entrée, sortie). Seules les sorties dont |y| dépasse
    /// le quantile demandé contribuent : c'est ce qui rend le capteur bon marché.
    fn observe(&mut self, x: &[f32], y: &[f32], seuil: &mut Vec<f32>) {
        seuil.clear();
        seuil.extend_from_slice(y);
        // k sorties « déchargent » : celles dont |y| dépasse le k-ième plus grand
        let k = (self.quantile * y.len() as f32) as usize;
        let k = k.clamp(1, y.len() - 1);
        seuil.select_nth_unstable_by(k, |a, b| b.abs().partial_cmp(&a.abs()).unwrap());
        let theta = seuil[k].abs();
        for o in 0..self.n_out {
            if y[o].abs() < theta { continue; }
            let yo = y[o];
            let row = &mut self.h[o * self.n_in..(o + 1) * self.n_in];
            for i in 0..self.n_in { row[i] += yo * x[i]; }
            self.n_fire += 1;
        }
        self.n_token += 1;
    }
}

/// Cache KV d'une couche, en f32 ou quantifié.
///
/// Le mur du contexte long n'est pas la capacité du cache mais **son trafic de
/// relecture** : à chaque jeton, l'attention relit toutes les clés des couches
/// pleines. Mesuré sur gpt-oss à 1 M de contexte : 77 Go par jeton en f32 (3,9 s
/// depuis la RAM), 19 Go en int8, 9,7 Go en int4 (13 ms depuis les deux GPU).
///
/// La quantification est **par vecteur** (une échelle par tête et par position),
/// comme pour les activations : c'est le même compromis, et l'échelle coûte
/// 4 octets pour 64 valeurs (3 % en int8). Les clés et les valeurs sont
/// déquantifiées à la lecture, dans un tampon réutilisé — la structure de
/// l'attention ne change pas.
pub struct KvCache {
    pub bits: u32,          // 32 = f32 (défaut), 8 = i8
    pub n_kv: usize,
    pub ctx: usize,
    pub hd: usize,
    kf: Vec<f32>,
    vf: Vec<f32>,
    /// Quantifié : un octet par valeur en 8 bits, **deux nibbles par octet en
    /// 4 bits** (même disposition que Q4_0/MXFP4 : nibble bas = indice pair).
    kq: Vec<u8>,
    vq: Vec<u8>,
    sk: Vec<f32>,
    sv: Vec<f32>,
}

impl KvCache {
    pub fn new(bits: u32, n_kv: usize, ctx: usize, hd: usize) -> Self {
        let bits = if bits >= 32 { 32 } else if bits > 4 { 8 } else { 4 };
        let n = n_kv * ctx * hd;
        let nv = n_kv * ctx;
        if bits >= 32 {
            KvCache { bits, n_kv, ctx, hd, kf: vec![0.0; n], vf: vec![0.0; n],
                      kq: Vec::new(), vq: Vec::new(), sk: Vec::new(), sv: Vec::new() }
        } else {
            assert!(hd % 2 == 0, "4 bits empaquetés : dimension de tête paire requise");
            let nq = if bits == 8 { n } else { n / 2 };
            KvCache { bits, n_kv, ctx, hd, kf: Vec::new(), vf: Vec::new(),
                      kq: vec![0u8; nq], vq: vec![0u8; nq],
                      sk: vec![0.0; nv], sv: vec![0.0; nv] }
        }
    }

    /// Octets par vecteur (tête, position) dans le tableau quantifié.
    #[inline]
    fn pas(&self) -> usize { if self.bits == 8 { self.hd } else { self.hd / 2 } }

    /// Octets réellement occupés (diagnostic).
    pub fn octets(&self) -> u64 {
        (self.kf.len() + self.vf.len()) as u64 * 4
            + (self.kq.len() + self.vq.len()) as u64
            + (self.sk.len() + self.sv.len()) as u64 * 4
    }

    /// Écrit un vecteur de clé et un de valeur à la position `pos`.
    #[inline]
    pub fn ecrire(&mut self, kvh: usize, pos: usize, k: &[f32], v: &[f32]) {
        let d = (kvh * self.ctx + pos) * self.hd;
        if self.bits >= 32 {
            self.kf[d..d + self.hd].copy_from_slice(&k[..self.hd]);
            self.vf[d..d + self.hd].copy_from_slice(&v[..self.hd]);
            return;
        }
        let niv = if self.bits == 4 { 7.0 } else { 127.0 };
        let mut mk = 0f32;
        let mut mv = 0f32;
        for i in 0..self.hd { mk = mk.max(k[i].abs()); mv = mv.max(v[i].abs()); }
        let sk = if mk > 0.0 { mk / niv } else { 1.0 };
        let sv = if mv > 0.0 { mv / niv } else { 1.0 };
        let base = (kvh * self.ctx + pos) * self.pas();
        if self.bits == 8 {
            for i in 0..self.hd {
                self.kq[base + i] = (k[i] / sk).round().clamp(-niv, niv) as i8 as u8;
                self.vq[base + i] = (v[i] / sv).round().clamp(-niv, niv) as i8 as u8;
            }
        } else {
            // Nibble bas = indice pair, haut = impair, écrits ENSEMBLE : un `|=`
            // laisserait les nibbles de la fenêtre précédente, la même position
            // étant réécrite à chaque fenêtre.
            for j in 0..self.hd / 2 {
                let qk0 = (k[2 * j] / sk).round().clamp(-niv, niv) as i32 as u8 & 0x0F;
                let qk1 = (k[2 * j + 1] / sk).round().clamp(-niv, niv) as i32 as u8 & 0x0F;
                let qv0 = (v[2 * j] / sv).round().clamp(-niv, niv) as i32 as u8 & 0x0F;
                let qv1 = (v[2 * j + 1] / sv).round().clamp(-niv, niv) as i32 as u8 & 0x0F;
                self.kq[base + j] = qk0 | (qk1 << 4);
                self.vq[base + j] = qv0 | (qv1 << 4);
            }
        }
        let s = kvh * self.ctx + pos;
        self.sk[s] = sk;
        self.sv[s] = sv;
    }

    /// Déquantifie la clé `(kvh, t)` dans `dst`.
    #[inline]
    pub fn cle(&self, kvh: usize, t: usize, dst: &mut [f32]) {
        let d = (kvh * self.ctx + t) * self.hd;
        if self.bits >= 32 { dst[..self.hd].copy_from_slice(&self.kf[d..d + self.hd]); return; }
        let s = self.sk[kvh * self.ctx + t];
        let base = (kvh * self.ctx + t) * self.pas();
        if self.bits == 8 {
            for i in 0..self.hd { dst[i] = self.kq[base + i] as i8 as f32 * s; }
        } else {
            for i in 0..self.hd {
                let o = self.kq[base + i / 2];
                // Extension de signe du nibble : 0..7 tel quel, 8..15 -> -8..-1.
                let q = if i % 2 == 0 { (o & 0x0F) as i32 } else { (o >> 4) as i32 };
                let q = if q >= 8 { q - 16 } else { q };
                dst[i] = q as f32 * s;
            }
        }
    }

    /// Déquantifie la valeur `(kvh, t)` dans `dst`.
    #[inline]
    pub fn valeur(&self, kvh: usize, t: usize, dst: &mut [f32]) {
        let d = (kvh * self.ctx + t) * self.hd;
        if self.bits >= 32 { dst[..self.hd].copy_from_slice(&self.vf[d..d + self.hd]); return; }
        let s = self.sv[kvh * self.ctx + t];
        let base = (kvh * self.ctx + t) * self.pas();
        if self.bits == 8 {
            for i in 0..self.hd { dst[i] = self.vq[base + i] as i8 as f32 * s; }
        } else {
            for i in 0..self.hd {
                let o = self.vq[base + i / 2];
                let q = if i % 2 == 0 { (o & 0x0F) as i32 } else { (o >> 4) as i32 };
                let q = if q >= 8 { q - 16 } else { q };
                dst[i] = q as f32 * s;
            }
        }
    }
}

impl Model {
    pub fn load(path: &str, ctx: usize, n_threads: usize, dense: bool, keep: f32,
                auto: bool, q4: u8, b6: u8) -> Model {
        let t0 = Instant::now();
        let g = Gguf::open(path).expect("ouverture du GGUF");
        let cfg = Cfg {
            n_layer: g.cfg("block_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
            hidden: g.cfg("embedding_length").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
            n_head: g.cfg("attention.head_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
            n_kv_head: g.cfg("attention.head_count_kv").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
            ffn: g.cfg("feed_forward_length").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
            eps: g.cfg("attention.layer_norm_rms_epsilon").and_then(|m| m.as_f64()).unwrap_or(1e-6) as f32,
            rope_base: g.cfg("rope.freq_base").and_then(|m| m.as_f64()).unwrap_or(10000.0) as f32,
            // `attention.key_length` donne la dimension de tête réelle. Elle
            // n'est PAS toujours hidden/n_head : Qwen3-30B-A3B a 2048 cachés,
            // 32 têtes et 128 par tête, soit 4096 en sortie de Q — l'ancien
            // calcul (64) débordait le tampon de Q.
            head_dim: g.cfg("attention.key_length").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
            vocab: g.tensor("token_embd.weight").map(|t| t.dims[0] as usize).unwrap_or(0),
            n_expert: g.cfg("expert_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
            n_expert_used: g.cfg("expert_used_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
            ffn_exp: g.cfg("expert_feed_forward_length").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
            // L'architecture « gpt-oss » implique sa propre activation ; elle
            // n'est pas déclarée dans les métadonnées.
            ffn_act_oss: g.meta.get("general.architecture").and_then(|m| m.as_str())
                             == Some("gpt-oss"),
            routeur_topk_softmax: g.meta.get("general.architecture").and_then(|m| m.as_str())
                                      == Some("gpt-oss"),
            n_rot: {
                let arch = g.meta.get("general.architecture").and_then(|m| m.as_str());
                let declare = g.cfg("rope.dimension_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
                if declare > 0 { declare }
                // Une hypothèse « moitié de tête » pour gpt-oss a été TESTÉE et
                // REFUTÉE : 185 -> 1 095 de perplexité. La tête est tournée en
                // entier ; seul `rope.dimension_count` déclaré fait foi.
                else { 0 }
            },
            // ------------------------------------------------ rotation (RoPE)
            // Trois régimes, choisis **par mesure** :
            //
            //   `QT_YARN=1`      YaRN à toutes les positions, comme HF, llama.cpp
            //                    et l'implémentation officielle d'OpenAI ;
            //   `QT_YARN_NON=1`  jamais de YaRN (ce que fait `--sans-yarn`) ;
            //   défaut           **YaRN à retardement** : RoPE simple tant que le
            //                    contexte demandé tient dans la longueur initiale
            //                    du modèle (4 096 pour gpt-oss), YaRN au-delà.
            //
            // Mesuré sur gpt-oss à contexte 512 : YaRN ×32 coûte un facteur 9
            // (174,34 contre 18,58). Mais l'étirement est indispensable pour
            // dépasser les 4 096 positions vues à l'entraînement initial : le
            // retardement garde les deux propriétés.
            //
            // Pourquoi une décision par SÉQUENCE et non par position : la
            // structure de position relative survit tant que toutes les clés
            // partagent le même jeu de fréquences (le produit q·k ne dépend
            // alors que de la différence des positions). Changer de jeu de
            // fréquences en cours de séquence détruit cette propriété pour
            // toutes les paires qui traversent la frontière — c'est un choix de
            // conception, pas une simplification.
            yarn: {
                let declare = match g.cfg("rope.scaling.type").and_then(|m| m.as_str()) {
                    Some("yarn") => Some((
                        g.cfg("rope.scaling.factor").and_then(|m| m.as_f64()).unwrap_or(1.0) as f32,
                        g.cfg("rope.scaling.yarn_beta_fast").and_then(|m| m.as_f64()).unwrap_or(32.0) as f32,
                        g.cfg("rope.scaling.yarn_beta_slow").and_then(|m| m.as_f64()).unwrap_or(1.0) as f32,
                        g.cfg("rope.scaling.original_context_length")
                            .and_then(|m| m.as_u64()).unwrap_or(4096) as f32,
                        // La mise à l'échelle de température (`mscale`) est la
                        // moitié NUISIBLE de YaRN : mesuré sur gpt-oss, la
                        // retirer fait passer la perplexité de 174,34 à 19,65 à
                        // 512 jetons, de 417,65 à 71,35 à 1 024, de 722,56 à
                        // 192,63 à 2 048. Le mode FORCÉ (`QT_YARN=1`) garde donc
                        // le comportement des implémentations de référence, et
                        // le mode retardé — celui du moteur — s'en passe.
                        // `QT_YARN_MSCALE=0/1` tranche explicitement dans les
                        // deux cas.
                        std::env::var("QT_YARN_MSCALE").map(|v| v != "0")
                            .unwrap_or_else(|_| std::env::var("QT_YARN").is_ok()),
                    )),
                    _ => None,
                };
                let toujours = std::env::var("QT_YARN").is_ok();
                let jamais = std::env::var("QT_YARN_NON").is_ok();
                match declare {
                    Some(y) if toujours => Some(y),
                    Some(y) if !jamais && ctx as f32 > y.3 => Some(y),
                    _ => None,
                }
            },
        };

        let cfg = {
            let mut c = cfg;
            if c.head_dim == 0 { c.head_dim = c.hidden / c.n_head.max(1); }
            c
        };
        assert!(cfg.head_dim > 0, "dimension de tête indéterminée");
        assert!(cfg.head_dim * cfg.n_head >= cfg.hidden,
                "n_head × head_dim doit couvrir hidden");
        let mut layers = Vec::with_capacity(cfg.n_layer);
        let mut bytes = 0u64;
        for l in 0..cfg.n_layer {
            let p = |s: &str| format!("blk.{l}.{s}");
            let lay = Layer {
                attn_norm: g.dequant(&p("attn_norm.weight")),
                wq: Proj::load(&g, &p("attn_q.weight"), Some(&p("attn_q.bias")), dense || q4 != 0, auto, keep, q4 & 2 != 0, b6 & 2 != 0),
                wk: Proj::load(&g, &p("attn_k.weight"), Some(&p("attn_k.bias")), dense || q4 != 0, auto, keep, q4 & 2 != 0, b6 & 2 != 0),
                wv: Proj::load(&g, &p("attn_v.weight"), Some(&p("attn_v.bias")), dense || q4 != 0, auto, keep, q4 & 2 != 0, b6 & 2 != 0),
                // gpt-oss porte un biais sur la projection de sortie
                // (`attention_bias = true` dans sa config : Q, K, V **et** O).
                // Le passer à `None` l'ignorait silencieusement — un décalage
                // constant ajouté à chaque couche, donc amplifié 36 fois.
                wo: Proj::load(&g, &p("attn_output.weight"), Some(&p("attn_output.bias")), dense || q4 != 0, auto, keep, q4 & 2 != 0, b6 & 2 != 0),
                // gpt-oss nomme `post_attention_norm` la normale d'entrée du
                // FFN ; c'est le même tenseur sous un autre nom.
                ffn_norm: if g.tensor(&p("ffn_norm.weight")).is_some() {
                    g.dequant(&p("ffn_norm.weight"))
                } else {
                    g.dequant(&p("post_attention_norm.weight"))
                },
                q_norm: if g.tensor(&p("attn_q_norm.weight")).is_some() {
                    Some(g.dequant(&p("attn_q_norm.weight"))) } else { None },
                k_norm: if g.tensor(&p("attn_k_norm.weight")).is_some() {
                    Some(g.dequant(&p("attn_k_norm.weight"))) } else { None },
                sinks: if g.tensor(&p("attn_sinks.weight")).is_some() {
                    Some(g.dequant(&p("attn_sinks.weight"))) } else { None },
                wgate: if cfg.n_expert > 0 { Proj::vide() } else {
                    Proj::load(&g, &p("ffn_gate.weight"), None, dense || q4 != 0, auto, keep, q4 & 1 != 0, b6 & 1 != 0) },
                wup: if cfg.n_expert > 0 { Proj::vide() } else {
                    Proj::load(&g, &p("ffn_up.weight"), None, dense || q4 != 0, auto, keep, q4 & 1 != 0, b6 & 1 != 0) },
                wdown: if cfg.n_expert > 0 { Proj::vide() } else {
                    Proj::load(&g, &p("ffn_down.weight"), None, dense || q4 != 0, auto, keep, q4 & 1 != 0, b6 & 1 != 0) },
                moe: charger_moe(&g, l, cfg.n_expert),
            };
            for pj in [&lay.wq, &lay.wk, &lay.wv, &lay.wo, &lay.wgate, &lay.wup, &lay.wdown] {
                if let Some(m) = &pj.m { bytes += m.data.len() as u64; }
                if let Some(d) = &pj.d { bytes += d.q.len() as u64 + d.scale.len() as u64 * 4; }
            }
            layers.push(lay);
        }
        let out_norm = g.dequant("output_norm.weight");
        // Précision du cache KV : 32 (f32, défaut), 8 ou 4. Le trafic de
        // relecture est LE mur du contexte long ; la trace le dit au chargement.
        let kv_bits: u32 = std::env::var("QT_KV_BITS").ok()
            .and_then(|v| v.parse().ok()).unwrap_or(32);
        let caches_kv: Vec<KvCache> = (0..cfg.n_layer)
            .map(|_| KvCache::new(kv_bits, cfg.n_kv_head, ctx, cfg.head_dim)).collect();
        let kv_octets = cfg.n_layer as u64
            * KvCache::new(kv_bits, cfg.n_kv_head, ctx, cfg.head_dim).octets();
        println!("[config] cache KV : {} bits, {:.2} Go pour {ctx} jetons",
                 if kv_bits >= 32 { 32 } else { kv_bits }, kv_octets as f64 / 1e9);
        let pool = Pool::new(n_threads, cfg.hidden);
        eprintln!("[modele] {} couches chargées en {:?} — listes {:.2} Go{} , {} threads",
                  cfg.n_layer, t0.elapsed(), bytes as f64 / 1e9,
                  if keep < 0.0 { format!(" (poids gardés : {:.0} % structuré)", -keep * 100.0) }
                  else if keep < 1.0 { format!(" (poids gardés : {:.0} %)", keep * 100.0) }
                  else { String::new() },
                  pool.threads());
        let n_layer = cfg.n_layer;
        let sinks_vus = layers.iter().filter(|l| l.sinks.is_some()).count();
        // Trace de configuration : une ligne qui dit quelles particularités
        // d'architecture ont été reconnues. Sans elle, on débogue à l'aveugle
        // sur un modèle de 60 Go.
        println!("[config] {} couches, hidden {} · {}{}{}{}{}{}",
                 cfg.n_layer, cfg.hidden,
                 if cfg.yarn.is_some() { "yarn " } else { "" },
                 if cfg.ffn_act_oss { "activation-oss " } else { "" },
                 if cfg.routeur_topk_softmax { "routeur-topk " } else { "" },
                 if cfg.n_expert > 0 { "moe " } else { "" },
                 if cfg.n_expert > 0 { "" } else { "" },
                 if cfg.head_dim > 0 { "" } else { "" });
        println!("[config] puits appris sur {sinks_vus}/{n_layer} couches · n_rot {} · ffn {} · experts {}{}",
                 if cfg.n_rot == 0 { cfg.head_dim } else { cfg.n_rot },
                 cfg.ffn, cfg.n_expert,
                 cfg.yarn.map(|y| format!(" · yarn ×{}", y.0)).unwrap_or_default());
        let tete = if g.tensor("output.weight").is_some() { "output.weight" } else { "token_embd.weight" };
        let tete = tete.to_string();
        // Le modèle peut déclarer une fenêtre glissante (gpt-oss : 128) : lue
        // AVANT que `g` ne soit déplacé dans la structure.
        let fenetre = g.cfg("attention.sliding_window").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
        // Motif fenêtre/plein : gpt-oss alterne une couche sur deux (18 des 36
        // couches sont « full attention »), et llama.cpp le pose par défaut
        // (`set_swa_pattern(2)`) faute de clé dans le GGUF. Les appliquer
        // toutes revenait à amputer la moitié du réseau au-delà de 128 jetons.
        let arch = g.meta.get("general.architecture").and_then(|m| m.as_str()).unwrap_or("");
        let motif_declare = g.cfg("attention.sliding_window_pattern")
            .and_then(|m| m.as_u64()).unwrap_or(0) as usize;
        let swa_pattern = if motif_declare > 0 { motif_declare }
                          else if fenetre > 0 && arch == "gpt-oss" { 2 }
                          else { 0 };
        // Trace : sans elle, impossible de savoir si la fenêtre est active
        // partout ou une couche sur deux. C'est exactement ce qui a coûté une
        // mesure fausse sur gpt-oss (perplexité croissante avec la fenêtre).
        if fenetre > 0 {
            let n_fen = if swa_pattern <= 1 { cfg.n_layer } else {
                (0..cfg.n_layer).filter(|&l| l % swa_pattern < swa_pattern - 1).count()
            };
            println!("[config] fenêtre glissante {fenetre} sur {n_fen}/{} couches (motif {swa_pattern}{})",
                     cfg.n_layer,
                     if swa_pattern <= 1 { ", toutes" } else { " alterné" });
        }
        // Trace de rotation : le régime choisi ET la raison. Sans elle, un
        // chiffre de perplexité ne dit pas s'il vient du RoPE simple ou de YaRN
        // — et c'est exactement la confusion qui a coûté une session.
        match (cfg.yarn, g.cfg("rope.scaling.original_context_length").and_then(|m| m.as_u64()),
               g.cfg("rope.scaling.factor").and_then(|m| m.as_f64())) {
            (Some((f, _, _, o, ms)), _, _) =>
                println!("[config] rotation : YaRN ×{f}{} (contexte demandé {ctx} > {o} initial)",
                         if ms { "" } else { " sans mscale" }),
            (None, Some(o), Some(f)) if o as usize >= ctx =>
                println!("[config] rotation : RoPE simple (contexte {ctx} ≤ {o} initial ; \
                          YaRN ×{f} prendrait le relais au-delà)"),
            (None, Some(o), Some(f)) =>
                println!("[config] rotation : RoPE simple (YaRN ×{f} refusé, contexte {ctx} > {o})"),
            _ => println!("[config] rotation : RoPE simple (le modèle ne déclare pas YaRN)"),
        }
        // Tête en 4 bits : la plus grosse matrice du modèle, donc le plus gros
        // gain possible sur un noyau déjà au mur de la bande passante.
        // La tête emprunte dès que la source est déjà quantifiée sur 4 ou
        // 6 bits : c'est exact (aucune requantification) et six fois plus
        // rapide que le chemin scalaire Q6_K, qui coûtait 42 % du temps par
        // jeton sur un 7B.
        let tete_quantifiee = g.q6k_blocks(&tete).is_some() || g.q4k_blocks(&tete).is_some()
            || g.mxfp4_blocks(&tete).is_some() || g.q4_blocks(&tete).is_some();
        // --- chemin GPU : la tête Q8_0 est copiée UNE fois dans la mémoire vidéo
        // La tête N'EST PAS déportée en l'état : mesuré sur gpt-oss, elle passe
        // de 23 à 159 ms. Le noyau lit une ligne par fil, donc des adresses
        // distantes de 34 octets : chaque accès d'une même warp tombe dans une
        // ligne de cache différente. Il faut une warp par ligne avec réduction
        // — à écrire avant de réactiver.
        // Le noyau « une warp par ligne » rend le déport de la tête enfin
        // rentable : l'ancien lisait une ligne par fil (23 → 159 ms mesurés).
        // Opt-in : `QT_GPU_TETE=1`.
        let tete_gpu = if std::env::var("QT_GPU_TETE").is_ok()
                          && crate::gpu::instance().is_some() {
            match (crate::gpu::instance(), g.q8_blocks(&tete)) {
                (Some(machine), Some((blocs, nb))) => {
                    let m = machine.charger_tete(blocs, cfg.vocab, cfg.hidden, nb);
                    if let Some(m) = m.as_ref() {
                        println!("[gpu] {} · tête {} × {} sur le GPU : {:.0} Mo résidents, \
                                  {:.0} Mo libres", machine.nom, cfg.vocab, cfg.hidden,
                                 m.octets_poids as f64 / 1e6,
                                 machine.memoire_libre as f64 / 1e6);
                    }
                    m
                }
                _ => None,
            }
        } else { None };
        let head4 = if q4 & 4 != 0 || tete_quantifiee {
            let t0 = Instant::now();
            let v = cfg.vocab;
            let h = cfg.hidden;
            let d = if let Some((buf, nb)) = g.q6k_blocks(&tete) {
                unsafe { DenseQ4::emprunter_q6k(buf.as_ptr(), v, h, nb) }
            } else if let Some((buf, nb)) = g.q4k_blocks(&tete) {
                unsafe { DenseQ4::emprunter_q4k(buf.as_ptr(), v, h, nb) }
            } else if let Some((buf, nb)) = g.mxfp4_blocks(&tete) {
                unsafe { DenseQ4::emprunter(buf.as_ptr(), v, h, nb, true) }
            } else if let Some((buf, nb)) = g.q4_blocks(&tete) {
                unsafe { DenseQ4::emprunter(buf.as_ptr(), v, h, nb, false) }
            } else {
                DenseQ4::build(&g.dequant(&tete), v, h)
            };
            println!("[tête 4 bits] {} × {} → {:.2} b/poids, {:.0} Mo, {:.1} s",
                     v, h, d.bits_per_weight(),
                     (d.q.len() + d.sc.len()) as f64 / 1e6, t0.elapsed().as_secs_f64());
            Some(d)
        } else { None };
        Model {
            g, cfg, layers, out_norm, pool,
            kv: caches_kv,
            ctx, events: 0, act_levels: 127.0, act_thresh: 0.0, act_topk: 0, act_renorm: false,
            act_topk_proj: [0; 7], attn_topk: 0, attn_events: 0, qk_topk: 0,
            moe_topk: 0,
            profil_neurones: None,
            profil_experts: None,
            profil_jetons: 0,
            attn_window: fenetre,
            swa_pattern,
            attn_sinks: if fenetre > 0 { 0 } else { 4 },
            seuil_push: 0.22,
            stop_id: None, stop_id2: None, prof: [0.0; 6],
            tete,
            tete_gpu, head4, sinks_vus,
            patch: None, ffn_gain: None, hebb: None,
        }
    }

    // ----------------------------------------------------------------------- //
    // Briques de calcul
    // ----------------------------------------------------------------------- //

    /// Quantifie un vecteur (une échelle pour tout le vecteur).
    #[inline]
    /// Parcimonie effective d'une projection : la valeur par projection prime,
    /// sinon on retombe sur le réglage global.
    #[inline]
    pub fn topk_de(&self, proj: usize) -> usize {
        if self.act_topk_proj[proj] > 0 { self.act_topk_proj[proj] } else { self.act_topk }
    }

    fn quant_scratch(x: &[f32], levels: f32, thresh: f32, topk: usize, renorm: bool,
                     scratch: &mut Vec<f32>) -> Option<(SparseVec, f32)> {
        let mut mx = 0f32;
        for &v in x { let a = v.abs(); if a > mx { mx = a; } }
        if mx == 0.0 { return None; }
        let s = mx / levels;
        let inv = 1.0 / s;
        // seuil absolu correspondant à la fraction demandée du maximum
        let seuil = (thresh * levels) as i32;
        let mut sv = SparseVec { idx: Vec::with_capacity(x.len()), val: Vec::with_capacity(x.len()) };
        if topk > 0 {
            // k-WTA : ne garder que les k plus grandes magnitudes (inhibition
            // latérale). `topk` est une FRACTION de la dimension : sans cela la
            // même valeur de k ne veut pas dire la même chose pour un vecteur de
            // 896 et un de 4 864.
            scratch.clear();
            scratch.extend(x.iter().map(|v| v.abs()));
            let mag = &mut *scratch;
            let k = (((topk as f32) / 1000.0) * x.len() as f32).round() as usize;
            let k = k.clamp(1, x.len());
            // l'élément d'indice (n - k) est le k-ième PLUS GRAND : c'est le
            // seuil du k-WTA. Prendre l'indice (k - 1) revenait à garder les k
            // plus PETITES — bug attrapé parce que le compte d'événements était
            // absurde (3,8 M au lieu de 349 M).
            let (_, &mut cut, _) = mag.select_nth_unstable_by(x.len() - k, |a, b| a.partial_cmp(b).unwrap());
            for (i, &v) in x.iter().enumerate() {
                if v.abs() < cut { continue; }
                let q = (v * inv).round();
                if q != 0.0 { sv.idx.push(i as u32); sv.val.push(q as i32); }
            }
            if renorm && !sv.val.is_empty() {
                let l1_tot: f64 = x.iter().map(|v| v.abs() as f64).sum();
                let l1_kept: f64 = sv.val.iter().map(|q| q.abs() as f64).sum::<f64>() * s as f64;
                if l1_kept > 0.0 {
                    let f = (l1_tot / l1_kept) as f32;
                    let lim = levels - 1.0;
                    for q in sv.val.iter_mut() {
                        let v = (*q as f32 * f).round().clamp(-lim, lim);
                        *q = v as i32;
                    }
                    sv.idx.retain(|_| true);
                }
            }
        } else {
            for (i, &v) in x.iter().enumerate() {
                let q = (v * inv).round();
                if q != 0.0 && (q as i32).abs() > seuil { sv.idx.push(i as u32); sv.val.push(q as i32); }
            }
        }
        Some((sv, s))
    }

    /// Produit matrice-vecteur **par événements** : les activations actives
    /// poussent leur contribution dans les sorties de leur liste.
    fn matvec(pool: &mut Pool, p: &Proj, x: &[f32], out: &mut [f32], events: &mut u64,
              levels: f32, thresh: f32, topk: usize, renorm: bool, scratch: &mut Vec<f32>,
              thresh_auto: f32) {
        let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
            for (o, v) in out.iter_mut().enumerate() {
                *v = p.bias.as_ref().map_or(0.0, |b| b[o]);
            }
            return;
        };
        // ---- choix de direction par mesure : sous le seuil, disperser (push) ;
        // au-dessus, le produit scalaire dense (pull) est plus rapide.
        // Forme 4 bits : pas d'événements du tout, un seul chemin.
        if let Some(q) = &p.q4 {
            let mut xd = vec![0i32; x.len()];
            for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { xd[i as usize] = v; }
            let y = pool.matvec_dense_q4(q, &xd, sx);
            for o in 0..q.n_out {
                out[o] = y[o] + p.bias.as_ref().map_or(0.0, |b| b[o]);
            }
            return;
        }
        let frac = sv.idx.len() as f32 / x.len().max(1) as f32;
        // le seuil ne tranche que si LES DEUX formes sont chargées ; sinon la
        // seule forme disponible impose le chemin (sinon : panique).
        let use_dense = match (&p.d, &p.m) {
            (Some(_), Some(_)) => frac > thresh_auto,
            (Some(_), None) => true,
            (None, Some(_)) => false,
            (None, None) => panic!("projection sans aucun format"),
        };
        if let (Some(machine), Some(mg)) = (crate::gpu::instance(), p.gpu.as_ref()) {
            // Le noyau applique déjà l'échelle d'activation : rien à reprendre.
            let mut xd = vec![0i32; x.len()];
            for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { xd[i as usize] = v; }
            if let Some(y) = machine.proj(mg, &xd, sx) {
                // Le biais fait partie de la projection : l'oublier donnait une
                // perplexité de 27 millions sur un modèle à biais QKV.
                for o in 0..mg.n_out.min(out.len()) {
                    out[o] = y[o] + p.bias.as_ref().map_or(0.0, |b| b[o]);
                }
                return;
            }
        }
        if let Some(d) = &p.d {
            if use_dense {
            // référence dense : pas d'événement, chaque sortie est un produit
            // scalaire complet sur la ligne de poids
            let mut xd = vec![0i32; x.len()];
            for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { xd[i as usize] = v; }
            let y = pool.matvec_dense_i8(d, &xd, sx);
            for o in 0..d.n_out {
                out[o] = y[o] + p.bias.as_ref().map_or(0.0, |b| b[o]);
            }
            return;
            }
        }
        {
            let m = p.m.as_ref().expect("projection sans format");
            for &i in &sv.idx { *events += m.row_ev[i as usize] as u64; }
            let acc = pool.accumulate_push(m, &sv);
            for o in 0..m.n_out {
                let mut y = acc[o] as f32 * (sx * m.scale[o]);
                if let Some(b) = &p.bias { y += b[o]; }
                out[o] = y;
            }
        }
    }

    /// Produit matrice-vecteur sur une matrice 4 bits empruntée (experts).
    fn matvec_q4(pool: &mut Pool, m: &crate::list::DenseQ4, x: &[f32], out: &mut [f32],
                 levels: f32, thresh: f32, topk: usize, renorm: bool,
                 scratch: &mut Vec<f32>, biais: Option<&[f32]>) {
        let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
            for v in out[..m.n_out].iter_mut() { *v = 0.0; }
            return;
        };
        let mut xd = vec![0i32; x.len()];
        for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { xd[i as usize] = v; }
        let y = pool.matvec_dense_q4(m, &xd, sx);
        match biais {
            Some(b) => for o in 0..m.n_out { out[o] = y[o] + b[o]; },
            None => out[..m.n_out].copy_from_slice(&y[..m.n_out]),
        }
    }

    /// Désactive l'étirement YaRN (pour éprouver l'hypothèse).
    pub fn cfg_yarn_off(&mut self) { self.cfg.yarn = None; }

    /// Active le profilage des neurones et alloue les compteurs.
    pub fn activer_profil_neurones(&mut self) {
        let largeur = self.cfg.ffn.max(self.cfg.ffn_exp);
        self.profil_neurones = Some((vec![0u64; self.cfg.n_layer * largeur],
                                     vec![0f64; self.cfg.n_layer * largeur]));
        if self.cfg.n_expert > 0 {
            self.profil_experts = Some(vec![0u64; self.cfg.n_layer * self.cfg.n_expert]);
        }
        self.profil_jetons = 0;
    }

    /// Compte les neurones actifs d'une couche FFN pour le jeton courant.
    ///
    /// Le critère est celui du moteur : une activation est « morte » si elle
    /// s'arrondit à zéro dans la quantification par vecteur. C'est donc
    /// exactement l'ensemble que le chemin par événements ignore.
    /// Seuil d'activation du profilage : une activation vaut `SEUIL_PROFIL` du
    /// maximum du vecteur. Le critère « valeur quantifiée non nulle » ne
    /// convient PAS : à 16 bits d'activation il laisse passer presque tout
    /// (mesuré : densité de 51 104 %, tous les neurones « chauds »). PowerInfer
    /// travaille sur des modèles ReLU, où zéro est exact ; pour du SiLU il faut
    /// un seuil relatif, et c'est celui-là.
    const SEUIL_PROFIL: f32 = 0.05;

    #[inline]
    fn compter_neurones(profil: &mut Option<(Vec<u64>, Vec<f64>)>, largeur: usize,
                        couche: usize, a: &[f32]) {
        let Some((tirs, poids)) = profil.as_mut() else { return };
        let mut mx = 0f32;
        for &v in a { let x = v.abs(); if x > mx { mx = x; } }
        if mx == 0.0 { return; }
        let seuil = Self::SEUIL_PROFIL * mx;
        let base = couche * largeur;
        for (i, &v) in a.iter().enumerate() {
            let x = v.abs();
            poids[base + i] += x as f64;
            if x > seuil { tirs[base + i] += 1; }
        }
    }

    /// Rapport de profilage : la loi de puissance des activations, mesurée.
    ///
    /// C'est la question que pose PowerInfer : quelle part des neurones est
    /// « chaude » (active presque toujours) et quelle part des activations
    /// concentrent-ils ? Si la réponse est « peu de neurones, beaucoup
    /// d'activations », le placement à la granularité du neurone a un sens.
    pub fn rapport_neurones(&self) -> Option<String> {
        let (tirs, poids) = self.profil_neurones.as_ref()?;
        let largeur = self.cfg.ffn.max(self.cfg.ffn_exp);
        let n_tok = self.profil_jetons.max(1);
        let mut out = String::new();
        let n = tirs.len();
        let tot_tirs: u64 = tirs.iter().sum();
        let tot_poids: f64 = poids.iter().sum();
        out.push_str(&format!("profil de neurones (seuil {:.0} % du max) : {} jetons,                               {} neurones par couche, {} neurones au total\n",
                              100.0 * Self::SEUIL_PROFIL, n_tok, largeur, n));
        out.push_str(&format!("  densité moyenne : {:.1} % des neurones tirés par jeton                               ({:.0} par couche)\n",
                              100.0 * tot_tirs as f64 / (n as f64 * n_tok as f64),
                              tot_tirs as f64 / n_tok as f64 / self.cfg.n_layer as f64));
        // Localité : quelle part du travail total portent les k % de neurones
        // les plus « lourds » (somme des |a|) et les plus « assidus » (tirs) ?
        let mut idx_poids: Vec<usize> = (0..n).collect();
        idx_poids.sort_by(|&a, &b| poids[b].partial_cmp(&poids[a]).unwrap());
        let mut cumul = 0f64;
        let mut parts = Vec::new();
        for part in [0.01f64, 0.05, 0.10, 0.20, 0.50] {
            let k = ((n as f64 * part) as usize).max(1);
            let deja: f64 = idx_poids[..k.min(n)].iter().map(|&i| poids[i]).sum();
            cumul = deja;
            parts.push((part, 100.0 * cumul / tot_poids.max(1e-12)));
        }
        for (part, pct) in &parts {
            out.push_str(&format!("  les {:>4.0} % de neurones les plus LOURDS portent {:>5.1} %                                   de la magnitude d'activation\n", part * 100.0, pct));
        }
        for (seuil, nom) in [(0.9f32, "> 90 %"), (0.5, "> 50 %"), (0.1, "> 10 %")] {
            let chauds = tirs.iter().filter(|&&c| c as f32 / n_tok as f32 > seuil).count();
            out.push_str(&format!("  neurones tirés {nom} du temps : {:>5.2} %\n",
                                  100.0 * chauds as f64 / n as f64));
        }
        // Dispersion entre couches : une localité qui ne tient que sur quelques
        // couches ne se place pas de la même façon.
        let mut par_couche: Vec<(f64, f64)> = Vec::new();
        for l in 0..self.cfg.n_layer {
            let t = &tirs[l * largeur..(l + 1) * largeur];
            let p = &poids[l * largeur..(l + 1) * largeur];
            let mut ip: Vec<usize> = (0..largeur).collect();
            ip.sort_by(|&a, &b| p[b].partial_cmp(&p[a]).unwrap());
            let k = (largeur / 10).max(1);
            let part: f64 = ip[..k].iter().map(|&i| p[i]).sum::<f64>()
                            / p.iter().sum::<f64>().max(1e-12);
            par_couche.push((t.iter().sum::<u64>() as f64 / n_tok as f64, 100.0 * part));
        }
        let f = |i: usize| par_couche[i].0;
        let g = |i: usize| par_couche[i].1;
        let (a1, b1) = par_couche.iter().enumerate()
            .fold((0usize, 0usize), |(mi, ma), (i, v)| {
                if v.0 < par_couche[mi].0 { (i, ma) } else if v.0 > par_couche[ma].0 { (mi, i) } else { (mi, ma) }
            });
        let _ = (f, g);
        out.push_str(&format!("  selon la couche : tirs de {:.0} à {:.0} par jeton ;                               part des 10 % les plus lourds de {:.1} à {:.1} %\n",
                              par_couche.iter().map(|v| v.0).fold(f64::MAX, f64::min),
                              par_couche.iter().map(|v| v.0).fold(0.0, f64::max),
                              par_couche.iter().map(|v| v.1).fold(f64::MAX, f64::min),
                              par_couche.iter().map(|v| v.1).fold(0.0, f64::max)));
        let _ = (a1, b1);
        // ---- section MoE : les experts « chauds »
        if let Some(exp) = self.profil_experts.as_ref() {
            let ne = self.cfg.n_expert;
            let n_tok = self.profil_jetons.max(1) as f64;
            let par_jeton = self.cfg.n_expert_used.max(1) as f64;
            out.push_str(&format!("\n  MoE : {ne} experts par couche, {par_jeton} par jeton\n"));
            // Couverture par les k experts les plus utilisés, moyennée par couche.
            for part in [0.05f64, 0.10, 0.25, 0.50] {
                let k = ((ne as f64 * part) as usize).max(1);
                let mut couverts = 0f64;
                for l in 0..self.cfg.n_layer {
                    let mut t: Vec<u64> = exp[l * ne..(l + 1) * ne].to_vec();
                    t.sort_unstable_by(|a, b| b.cmp(a));
                    let tot: u64 = t.iter().sum();
                    if tot == 0 { continue; }
                    couverts += t.iter().take(k).sum::<u64>() as f64 / tot as f64;
                }
                out.push_str(&format!("    les {:>4.0} % d'experts les plus utilisés couvrent {:>5.1} %                                       des choix\n", part * 100.0, 100.0 * couverts / self.cfg.n_layer as f64));
            }
            let jamais: usize = exp.iter().filter(|&&c| c == 0).count();
            out.push_str(&format!("    experts jamais choisis : {jamais}/{} ({:.0} %) ;                                   taux moyen {:.3} par jeton\n",
                                  exp.len(), 100.0 * jamais as f64 / exp.len() as f64,
                                  exp.iter().sum::<u64>() as f64 / exp.len() as f64 / n_tok));
        }
        Some(out)
    }

    /// Écrit le classement des neurones (couche, indice, taux) pour un
    /// placement ultérieur : les plus chauds d'abord.
    pub fn ecrire_neurones(&self, chemin: &str) -> std::io::Result<usize> {
        use std::io::Write;
        let Some((tirs, poids)) = self.profil_neurones.as_ref() else { return Ok(0) };
        let largeur = self.cfg.ffn.max(self.cfg.ffn_exp);
        let n_tok = self.profil_jetons.max(1) as f32;
        let mut lignes: Vec<(usize, usize, f32)> = (0..tirs.len())
            .map(|i| (i / largeur, i % largeur, poids[i] as f32 / n_tok)).collect();
        lignes.sort_by(|a, b| b.2.partial_cmp(&a.2).unwrap());
        let mut f = std::io::BufWriter::new(std::fs::File::create(chemin)?);
        writeln!(f, "# couche neurone taux")?;
        for (l, i, t) in &lignes { writeln!(f, "{l} {i} {t:.6}")?; }
        Ok(lignes.len())
    }

    /// Activation du FFN, appliquée en place dans `gate`.
    ///
    /// - SiLU (défaut) : `g·σ(g)`, multiplié par `u` ;
    /// - gpt-oss : `g` et `u` écrêtés à ±7, `a = g·σ(1,702·g)`, résultat
    ///   `a·(u+1)`.
    #[inline]
    fn activation(gate: &mut [f32], up: &[f32], n: usize, oss: bool) {
        if oss {
            const LIMITE: f32 = 7.0;
            const ALPHA: f32 = 1.702;
            for i in 0..n {
                let g = gate[i].min(LIMITE);
                let u = up[i].clamp(-LIMITE, LIMITE);
                gate[i] = (g / (1.0 + (-ALPHA * g).exp())) * (u + 1.0);
            }
        } else {
            for i in 0..n { gate[i] = (gate[i] / (1.0 + (-gate[i]).exp())) * up[i]; }
        }
    }

    /// Produit scalaire f32 à huit accumulateurs indépendants.
    ///
    /// Un `iter().zip().map().sum()` est une **chaîne** d'additions : chaque
    /// élément attend le précédent (4 cycles de latence sur Haswell), et LLVM ne
    /// peut pas réassocier un flottant. Mesuré : 2,10 ms par jeton pour les
    /// seuls scores d'attention à contexte 256, soit ~1,2 cycle par élément.
    /// Huit chaînes indépendantes laissent le processeur remplir ses ports.
    /// Le résultat n'est plus la somme « dans l'ordre » — quelques ulp d'écart,
    /// à comparer au facteur gagné.
    #[inline]
    fn dot8(a: &[f32], b: &[f32]) -> f32 {
        let n = a.len().min(b.len());
        let mut acc = [0f32; 8];
        let mut i = 0usize;
        while i + 8 <= n {
            for k in 0..8 { acc[k] += a[i + k] * b[i + k]; }
            i += 8;
        }
        let mut s = ((acc[0] + acc[1]) + (acc[2] + acc[3]))
                  + ((acc[4] + acc[5]) + (acc[6] + acc[7]));
        while i < n { s += a[i] * b[i]; i += 1; }
        s
    }

    /// Même produit scalaire en AVX2 + FMA : 8 flottants par instruction.
    /// Le chemin scalaire tient 3,3 opérations par cycle, c'est-à-dire la
    /// largeur d'émission du processeur — il n'y a plus rien à gagner sans
    /// SIMD. Quatre accumulateurs vectoriels couvrent 32 éléments par tour.
    #[cfg(target_arch = "x86_64")]
    #[target_feature(enable = "avx2,fma")]
    unsafe fn dot8_avx(a: &[f32], b: &[f32]) -> f32 {
        use std::arch::x86_64::*;
        let n = a.len().min(b.len());
        let mut v0 = _mm256_setzero_ps();
        let mut v1 = _mm256_setzero_ps();
        let mut v2 = _mm256_setzero_ps();
        let mut v3 = _mm256_setzero_ps();
        let (pa, pb) = (a.as_ptr(), b.as_ptr());
        let mut i = 0usize;
        while i + 32 <= n {
            v0 = _mm256_fmadd_ps(_mm256_loadu_ps(pa.add(i)), _mm256_loadu_ps(pb.add(i)), v0);
            v1 = _mm256_fmadd_ps(_mm256_loadu_ps(pa.add(i + 8)), _mm256_loadu_ps(pb.add(i + 8)), v1);
            v2 = _mm256_fmadd_ps(_mm256_loadu_ps(pa.add(i + 16)), _mm256_loadu_ps(pb.add(i + 16)), v2);
            v3 = _mm256_fmadd_ps(_mm256_loadu_ps(pa.add(i + 24)), _mm256_loadu_ps(pb.add(i + 24)), v3);
            i += 32;
        }
        let mut v = _mm256_add_ps(_mm256_add_ps(v0, v1), _mm256_add_ps(v2, v3));
        while i + 8 <= n {
            v = _mm256_fmadd_ps(_mm256_loadu_ps(pa.add(i)), _mm256_loadu_ps(pb.add(i)), v);
            i += 8;
        }
        let mut t = [0f32; 8];
        _mm256_storeu_ps(t.as_mut_ptr(), v);
        let mut s = (t[0] + t[1]) + (t[2] + t[3]) + ((t[4] + t[5]) + (t[6] + t[7]));
        while i < n { s += *pa.add(i) * *pb.add(i); i += 1; }
        s
    }

    fn rmsnorm(x: &[f32], w: &[f32], eps: f32, out: &mut [f32]) {
        let mut ss = 0f32;
        for &v in x { ss += v * v; }
        let inv = 1.0 / (ss / x.len() as f32 + eps).sqrt();
        for i in 0..x.len() { out[i] = x[i] * inv * w[i]; }
    }

    /// k-WTA par tête : ne garder que la fraction demandée des composantes les
    /// plus grandes de chaque tête. Appliqué à Q et K, il rend le produit
    /// scalaire des scores creux.
    fn creuse_tetes(v: &mut [f32], n_head: usize, head_dim: usize, milliemes: usize) {
        let k = ((milliemes as f32 / 1000.0) * head_dim as f32).round() as usize;
        let k = k.clamp(1, head_dim);
        if k >= head_dim { return; }
        let mut tmp = [0f32; 256];
        for h in 0..n_head {
            let t = &mut v[h * head_dim..(h + 1) * head_dim];
            let n = head_dim.min(256);
            tmp[..n].copy_from_slice(&t[..n]);
            let (_, &mut cut, _) = tmp[..n].select_nth_unstable_by(n - k, |a, b| {
                a.abs().partial_cmp(&b.abs()).unwrap()
            });
            let cut = cut.abs();
            for x in t.iter_mut() { if x.abs() < cut { *x = 0.0; } }
        }
    }

    /// RoPE avec étirement **YaRN** (`rope.scaling.type = yarn`).
    ///
    /// YaRN n'interpole pas toutes les fréquences : les basses dimensions
    /// (longueurs d'onde courtes) sont laissées telles quelles, les hautes sont
    /// divisées par le facteur, et une rampe relie les deux. Sans cette rampe,
    /// un modèle entraîné à 4 096 de contexte ne peut pas travailler à 128 000 —
    /// et même à contexte court, diviser *toutes* les fréquences fausse la
    /// rotation. La sortie est en plus multipliée par `mscale = 1 + 0,1·ln(f)`,
    /// qui compense la perte d'amplitude de l'attention dilatée.
    fn rope_yarn(v: &mut [f32], n_head: usize, head_dim: usize, pos: usize, base: f32,
                 facteur: f32, beta_rapide: f32, beta_lent: f32, ctx_origine: f32,
                 mscale_actif: bool, n_rot: usize) {
        let n_rot = if n_rot == 0 || n_rot > head_dim { head_dim } else { n_rot };
        let half = n_rot / 2;
        let ln_base = base.ln();
        let corr0 = (head_dim as f32 * (ctx_origine / (beta_rapide * 2.0 * std::f32::consts::PI)).ln()
                     / (2.0 * ln_base)).floor();
        let corr1 = (head_dim as f32 * (ctx_origine / (beta_lent * 2.0 * std::f32::consts::PI)).ln()
                     / (2.0 * ln_base)).ceil();
        // La mise à l'échelle de température compense l'entropie du softmax
        // quand le nombre de clés grandit ; à contexte court, elle rend
        // l'attention trop tranchée. Séparable de l'interpolation.
        let mscale = if mscale_actif { 1.0 + 0.1 * facteur.ln() } else { 1.0 };
        for h in 0..n_head {
            let t = &mut v[h * head_dim..(h + 1) * head_dim];
            for i in 0..half {
                let freq = 1.0 / base.powf(2.0 * i as f32 / n_rot as f32);
                let theta_extrap = pos as f32 * freq;
                let theta_interp = theta_extrap / facteur;
                // RÉSULTATS NÉGATIFS, mesurés sur gpt-oss (63 jetons) :
                //   RoPE simple, sans YaRN ........ 39,8   <- le meilleur
                //   YaRN avec rampe (ext_factor 1)  184,9
                //   YaRN interpolation pure ........ 1 171
                // Aucune variante ne bat le RoPE simple aux contextes testés
                // (<= 512). L'hypothèse la plus probable est que l'étirement ne
                // doit s'appliquer QU'AU-DELÀ du contexte d'origine (4 096) :
                // en deçà, le modèle n'a jamais vu de fréquences étirées.
                // À implémenter ainsi, puis à remesurer.
                //
                // Variante d'extrapolation : la rampe mélange extrapolation
                // (basses dimensions) et interpolation (hautes). Selon les
                // implémentations, le facteur d'extrapolation vaut 1 (rampe
                // active) ou 0 (interpolation PURE) — les deux se rencontrent.
                // QT_YARN_RAMPE=0 force l'interpolation pure.
                let rampe = if std::env::var("QT_YARN_RAMPE").map_or(false, |v| v == "0") {
                    0.0
                } else {
                    let y = (i as f32 - corr0) / (corr1 - corr0).max(0.001);
                    1.0 - y.clamp(0.0, 1.0)
                };
                let theta = theta_interp * (1.0 - rampe) + theta_extrap * rampe;
                let (s, c) = theta.sin_cos();
                let (s, c) = (s * mscale, c * mscale);
                let a = t[i];
                let b = t[i + half];
                t[i] = a * c - b * s;
                t[i + half] = b * c + a * s;
            }
        }
    }

    /// RoPE « neox » (Qwen2) : rotation des deux moitiés de chaque tête.
    fn rope(v: &mut [f32], n_head: usize, head_dim: usize, pos: usize, base: f32, n_rot: usize) {
        // `n_rot` = dimensions tournées ; les autres restent intactes. La
        // rotation « neox » apparie `i` et `i + n_rot/2`.
        let n_rot = if n_rot == 0 || n_rot > head_dim { head_dim } else { n_rot };
        let half = n_rot / 2;
        for h in 0..n_head {
            let t = &mut v[h * head_dim..(h + 1) * head_dim];
            for i in 0..half {
                let freq = 1.0 / base.powf(2.0 * i as f32 / head_dim as f32);
                let (s, c) = (pos as f32 * freq).sin_cos();
                let a = t[i];
                let b = t[i + half];
                t[i] = a * c - b * s;
                t[i + half] = b * c + a * s;
            }
        }
    }

    /// **Préremplissage par lots** : `t` jetons d'un coup, aux positions
    /// `pos0..pos0+t`.
    ///
    /// Toute la différence avec `forward` est dans les projections : elles
    /// passent d'un produit matrice-vecteur par jeton à un produit
    /// matrice-matrice pour le lot, donc chaque ligne de poids n'est lue qu'une
    /// fois au lieu de `t` fois (mesuré au noyau : ×2,4 à 16 jetons sur une
    /// matrice 4864 × 896).
    ///
    /// L'attention reste par jeton (elle est causale : le jeton i doit voir le
    /// cache écrit par les jetons < i), mais elle réutilise les Q, K, V calculés
    /// en lot. Les modèles à experts retombent sur le chemin jeton par jeton :
    /// leur regroupement par expert est l'étape suivante.
    pub fn forward_lot(&mut self, toks: &[u32], pos0: usize) -> Vec<Vec<f32>> {
        let t = toks.len();
        if t == 0 { return Vec::new(); }
        if t == 1 {
            return vec![self.forward(toks[0], pos0)];
        }
        // Les modèles à experts suivent le même chemin par lots, avec en plus le
        // regroupement des jetons par expert (voir la section MoE plus bas).
        let h = self.cfg.hidden;
        let hd = self.cfg.head_dim;
        let nh = self.cfg.n_head;
        let nkv = self.cfg.n_kv_head;
        let rep = nh / nkv;
        let ctx = self.ctx;
        // --- activations du lot, en i32 quantifié (une seule quantification de
        //     l'entrée normative sert à q, k, v ET au FFN)
        let mut x = vec![0f32; t * h];
        for (i, &tok) in toks.iter().enumerate() {
            let r = self.g.row_f32("token_embd.weight", tok as usize, h);
            x[i * h..(i + 1) * h].copy_from_slice(&r);
        }
        let mut hn = vec![0f32; t * h];
        let mut xi = vec![0i32; t * h];
        let mut sx = vec![0f32; t];
        let mut q = vec![0f32; t * nh * hd];
        let mut k = vec![0f32; t * nkv * hd];
        let mut v = vec![0f32; t * nkv * hd];
        let mut att = vec![0f32; t * nh * hd];
        let mut o = vec![0f32; t * h];
        let mut scratch: Vec<f32> = Vec::with_capacity(h);
        let mut gate = vec![0f32; t * self.cfg.ffn];
        let mut up = vec![0f32; t * self.cfg.ffn];
        let mut down = vec![0f32; t * h];
        let mut tmp = vec![0f32; hd];
        // Tampons du lot, alloués UNE fois : les recréer à chaque couche et à
        // chaque lot annulait le gain du produit matrice-matrice.
        let nq_max = nh * hd;
        let nk_max = nkv * hd;
        let mut qa = vec![0f32; t * nq_max];
        let mut ka = vec![0f32; t * nk_max];
        let mut va = vec![0f32; t * nk_max];
        let mut yl = vec![0f32; t * nq_max.max(nk_max).max(self.cfg.ffn).max(h)];
        let mut ai = vec![0i32; t * h.max(nq_max)];   // h et n_têtes × dim_tête
        let mut sa = vec![0f32; t];
        let mut gi = vec![0i32; t * self.cfg.ffn];
        let mut sg = vec![0f32; t];
        let mut sc = vec![0f32; pos0 + t];
        let mut kd = vec![0f32; hd];
        let mut vd = vec![0f32; hd];
        let attn_all: Vec<u32> = (0..ctx as u32).collect();
        let mut attn_idx: Vec<u32> = Vec::with_capacity(ctx);
        let scale = 1.0 / (hd as f32).sqrt();
        // Quantification d'un lot : mêmes règles que `quant_scratch`.
        let quantifier = |src: &[f32], dst: &mut [i32], ech: &mut [f32],
                          niveaux: f32, seuil: f32| {
            let n = src.len() / t;
            for i in 0..t {
                let ligne = &src[i * n..(i + 1) * n];
                let mut mx = 0f32;
                for &val in ligne { let a = val.abs(); if a > mx { mx = a; } }
                let s = if mx > 0.0 { mx / niveaux } else { 1.0 };
                ech[i] = s;
                let inv = 1.0 / s;
                let se = (seuil * niveaux) as i32;
                for (j, &val) in ligne.iter().enumerate() {
                    let r = (val * inv).round() as i32;
                    dst[i * n + j] = if r.abs() > se { r } else { 0 };
                }
            }
        };
        for l in 0..self.cfg.n_layer {
            let lay = &self.layers[l];
            // 1. norme d'entrée du lot
            for i in 0..t {
                let r = &x[i * h..(i + 1) * h];
                Self::rmsnorm(r, &lay.attn_norm, self.cfg.eps, &mut hn[i * h..(i + 1) * h]);
            }
            quantifier(&hn, &mut xi, &mut sx, self.act_levels, self.act_thresh);
            // 2. q, k, v : un produit matrice-matrice chacun. Trois tampons
            //    DISTINCTS (un `y` partagé avec un pas par projection mélangeait
            //    les sorties : mesuré, une perplexité de 1,6 million).
            let nq = nh * hd;
            let nk = nkv * hd;
            for (pj, dst, taille) in [(&lay.wq, &mut qa, nq),
                                      (&lay.wk, &mut ka, nk),
                                      (&lay.wv, &mut va, nk)] {
                if let Some(d8) = pj.d.as_ref() {
                    self.pool.gemm_dense_i8(d8, &xi, t, &sx, &mut yl[..d8.n_out * t]);
                    for i in 0..t {
                        for oo in 0..taille {
                            dst[i * taille + oo] = yl[oo * t + i]
                                + pj.bias.as_ref().map_or(0.0, |b| b[oo]);
                        }
                    }
                } else {
                    // Pas de forme dense (mode push) : jeton par jeton.
                    for i in 0..t {
                        let mut out = vec![0f32; taille];
                        Self::matvec(&mut self.pool, pj, &hn[i * h..(i + 1) * h], &mut out,
                                     &mut self.events, self.act_levels, self.act_thresh, 0,
                                     self.act_renorm, &mut scratch, self.seuil_push);
                        dst[i * taille..(i + 1) * taille].copy_from_slice(&out);
                    }
                }
            }
            q.copy_from_slice(&qa);
            k.copy_from_slice(&ka);
            v.copy_from_slice(&va);
            // 3. normes de tête, rotation, écriture du cache, attention
            for i in 0..t {
                let pos = pos0 + i;
                let qi = &mut q[i * nq..(i + 1) * nq];
                let ki = &mut k[i * nkv * hd..(i + 1) * nkv * hd];
                let vi = &v[i * nkv * hd..(i + 1) * nkv * hd];
                if lay.q_norm.is_some() || lay.k_norm.is_some() {
                    if let Some(w) = lay.q_norm.as_ref() {
                        for hh in 0..nh {
                            let tt = &mut qi[hh * hd..(hh + 1) * hd];
                            Self::rmsnorm(tt, w, self.cfg.eps, &mut tmp);
                            tt.copy_from_slice(&tmp);
                        }
                    }
                    if let Some(w) = lay.k_norm.as_ref() {
                        for hh in 0..nkv {
                            let tt = &mut ki[hh * hd..(hh + 1) * hd];
                            Self::rmsnorm(tt, w, self.cfg.eps, &mut tmp);
                            tt.copy_from_slice(&tmp);
                        }
                    }
                }
                match self.cfg.yarn {
                    Some((f, bf, bl, orig, ms)) => {
                        Self::rope_yarn(qi, nh, hd, pos, self.cfg.rope_base, f, bf, bl, orig, ms, self.cfg.n_rot);
                        Self::rope_yarn(ki, nkv, hd, pos, self.cfg.rope_base, f, bf, bl, orig, ms, self.cfg.n_rot);
                    }
                    None => {
                        Self::rope(qi, nh, hd, pos, self.cfg.rope_base, self.cfg.n_rot);
                        Self::rope(ki, nkv, hd, pos, self.cfg.rope_base, self.cfg.n_rot);
                    }
                }
                {
                    let kvc = &mut self.kv[l];
                    for hh in 0..nkv {
                        kvc.ecrire(hh, pos, &ki[hh * hd..(hh + 1) * hd],
                                          &vi[hh * hd..(hh + 1) * hd]);
                    }
                }
                let fen = if self.attn_window == 0 { 0 }
                          else if self.swa_pattern <= 1 { self.attn_window }
                          else if l % self.swa_pattern < self.swa_pattern - 1 { self.attn_window }
                          else { 0 };
                let kvc = &self.kv[l];
                let n = pos + 1;
                let lo = if fen > 0 && n > fen { n - fen } else { 0 };
                for hh in 0..nh {
                    let kvh = hh / rep;
                    let qh = &qi[hh * hd..(hh + 1) * hd];
                    for tt in lo..n {
                        kvc.cle(kvh, tt, &mut kd);
                        sc[tt] = Self::dot8(&qh, &kd) * scale;
                    }
                    let puits = lay.sinks.as_ref().map(|s| s[hh]);
                    let mut mx = f32::NEG_INFINITY;
                    for tt in lo..n { if sc[tt] > mx { mx = sc[tt]; } }
                    if let Some(s) = puits { if s > mx { mx = s; } }
                    let mut somme = 0f32;
                    for tt in lo..n { let e = (sc[tt] - mx).exp(); sc[tt] = e; somme += e; }
                    if let Some(s) = puits { somme += (s - mx).exp(); }
                    let inv = 1.0 / somme;
                    let out = &mut att[i * nq + hh * hd..i * nq + (hh + 1) * hd];
                    for val in out.iter_mut() { *val = 0.0; }
                    for tt in lo..n {
                        let w = sc[tt] * inv;
                        kvc.valeur(kvh, tt, &mut vd);
                        for (oo, xx) in out.iter_mut().zip(vd.iter()) { *oo += w * xx; }
                    }
                }
                self.attn_events += (nh * (n - lo)) as u64;
            }
            // 4. projection de sortie du lot, résidu, norme du FFN
            {
                // `att` fait t × (n_têtes × dim_tête), qui n'est PAS t × h :
                // sur gpt-oss c'est 4 096 contre 2 880. Le tampon d'activation
                // doit suivre la dimension d'ENTRÉE de la projection.
                let n_in_wo = {
                    let d8 = self.layers[l].wo.d.as_ref().expect("projection dense requise");
                    d8.n_in
                };
                quantifier(&att, &mut ai[..t * n_in_wo], &mut sa, self.act_levels, self.act_thresh);
                let n_out = {
                    let d8 = self.layers[l].wo.d.as_ref().expect("projection dense requise");
                    self.pool.gemm_dense_i8(d8, &ai[..t * n_in_wo], t, &sa, &mut yl[..d8.n_out * t]);
                    d8.n_out
                };
                let bias = self.layers[l].wo.bias.clone();
                for i in 0..t {
                    for oo in 0..n_out {
                        o[i * h + oo] = yl[oo * t + i]
                            + bias.as_ref().map_or(0.0, |b| b[oo]) + x[i * h + oo];
                    }
                }
            }
            for i in 0..t {
                let r = &o[i * h..(i + 1) * h];
                Self::rmsnorm(r, &lay.ffn_norm, self.cfg.eps, &mut hn[i * h..(i + 1) * h]);
            }
            quantifier(&hn, &mut xi, &mut sx, self.act_levels, self.act_thresh);
            if let Some(moe) = lay.moe.as_ref() {
                // ---- MoE PAR LOTS : les jetons qui ont choisi le même expert
                // sont traités ensemble, donc la matrice de l'expert est lue une
                // fois pour le groupe au lieu d'une fois par jeton.
                let ne = self.cfg.n_expert;
                let k = if self.moe_topk > 0 { self.moe_topk } else { self.cfg.n_expert_used };
                let k = k.clamp(1, ne);
                let mut x16: Vec<i16> = vec![0i16; t * h];
                for (j, &v) in xi.iter().enumerate() { x16[j] = v.clamp(-32767, 32767) as i16; }
                let s32: Vec<Vec<i32>> = (0..t)
                    .map(|i| crate::list::sommes32(&x16[i * h..(i + 1) * h])).collect();
                let mut groupes: Vec<Vec<(usize, f32)>> = vec![Vec::new(); ne];
                for i in 0..t {
                    let hni = &hn[i * h..(i + 1) * h];
                    let mut sc_e: Vec<f32> = (0..ne).map(|e| {
                        let r = &moe.routeur[e * h..(e + 1) * h];
                        let sc: f32 = r.iter().zip(hni.iter()).map(|(a, b)| a * b).sum();
                        sc + moe.routeur_biais.as_ref().map_or(0.0, |b| b[e])
                    }).collect();
                    let mut idx: Vec<u32> = (0..ne as u32).collect();
                    let mut inv_k = 1.0f32;
                    if self.cfg.routeur_topk_softmax {
                        if k < ne {
                            idx.select_nth_unstable_by(k, |&a, &b| {
                                sc_e[b as usize].partial_cmp(&sc_e[a as usize]).unwrap()
                            });
                            idx.truncate(k);
                        }
                        let mx = idx.iter().map(|&e| sc_e[e as usize])
                                   .fold(f32::NEG_INFINITY, f32::max);
                        let mut somme = 0f32;
                        for &e in &idx {
                            let v = (sc_e[e as usize] - mx).exp(); sc_e[e as usize] = v; somme += v;
                        }
                        if somme > 0.0 { inv_k = 1.0 / somme; }
                    } else {
                        let mx = sc_e.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
                        let mut somme = 0f32;
                        for v in sc_e.iter_mut() { *v = (*v - mx).exp(); somme += *v; }
                        if somme > 0.0 { for v in sc_e.iter_mut() { *v /= somme; } }
                        if k < ne {
                            idx.select_nth_unstable_by(k, |&a, &b| {
                                sc_e[b as usize].partial_cmp(&sc_e[a as usize]).unwrap()
                            });
                            idx.truncate(k);
                        }
                        let somme_k: f32 = idx.iter().map(|&e| sc_e[e as usize]).sum();
                        inv_k = if somme_k > 0.0 { 1.0 / somme_k } else { 0.0 };
                    }
                    for &e in &idx { groupes[e as usize].push((i, sc_e[e as usize] * inv_k)); }
                }
                for i in 0..t { down[i * h..(i + 1) * h].iter_mut().for_each(|v| *v = 0.0); }
                let nff = self.cfg.ffn_exp;
                let mut xg = vec![0i16; t * h];
                let mut s32g: Vec<Vec<i32>> = Vec::with_capacity(t);
                let mut sxg: Vec<f32> = Vec::with_capacity(t);
                let mut yq = vec![0f32; t * nff];
                let mut col = vec![0f32; nff];
                let mut colu = vec![0f32; nff];
                let mut ga = vec![0i16; t * nff];
                let mut s32a: Vec<Vec<i32>> = Vec::with_capacity(t);
                let mut sxa: Vec<f32> = Vec::with_capacity(t);
                for e in 0..ne {
                    let g = groupes[e].len();
                    if g == 0 { continue; }
                    for (j, &(i, _)) in groupes[e].iter().enumerate() {
                        xg[j * h..(j + 1) * h].copy_from_slice(&x16[i * h..(i + 1) * h]);
                    }
                    s32g.clear();
                    sxg.clear();
                    for &(i, _) in groupes[e].iter() { s32g.push(s32[i].clone()); sxg.push(sx[i]); }
                    let mg = moe.gate.expert(e);
                    self.pool.gemm_dense_q4(&mg, &xg[..g * h], g, &s32g, &sxg,
                                            &mut yq[..mg.n_out * g]);
                    for j in 0..g {
                        for oo in 0..nff {
                            gate[oo * g + j] = yq[oo * g + j]
                                + moe.biais_gate.as_ref().map_or(0.0, |b| b[e * nff + oo]);
                        }
                    }
                    let mu = moe.up.expert(e);
                    self.pool.gemm_dense_q4(&mu, &xg[..g * h], g, &s32g, &sxg,
                                            &mut yq[..mu.n_out * g]);
                    for j in 0..g {
                        for oo in 0..nff {
                            up[oo * g + j] = yq[oo * g + j]
                                + moe.biais_up.as_ref().map_or(0.0, |b| b[e * nff + oo]);
                        }
                    }
                    // Activation jeton par jeton (elle n'est pas linéaire), puis
                    // descente en lot : la matrice de descente est relue pour tout
                    // le groupe.
                    s32a.clear();
                    sxa.clear();
                    for j in 0..g {
                        for oo in 0..nff {
                            col[oo] = gate[oo * g + j];
                            colu[oo] = up[oo * g + j];
                        }
                        Self::activation(&mut col, &colu, nff, self.cfg.ffn_act_oss);
                        let mut mx = 0f32;
                        for &v in col.iter() { mx = mx.max(v.abs()); }
                        let ech = if mx > 0.0 { mx / self.act_levels } else { 1.0 };
                        for oo in 0..nff {
                            ga[j * nff + oo] = ((col[oo] / ech).round())
                                .clamp(-32767.0, 32767.0) as i16;
                        }
                        s32a.push(crate::list::sommes32(&ga[j * nff..(j + 1) * nff]));
                        sxa.push(ech);
                    }
                    let md = moe.down.expert(e);
                    let mut yd = vec![0f32; md.n_out * g];
                    self.pool.gemm_dense_q4(&md, &ga[..g * nff], g, &s32a, &sxa, &mut yd);
                    for (j, &(i, w)) in groupes[e].iter().enumerate() {
                        for oo in 0..h {
                            // Le biais de descente est indexé par la LARGEUR DE
                            // SORTIE (h), pas par la largeur d'expert.
                            let b = moe.biais_down.as_ref().map_or(0.0, |b| b[e * h + oo]);
                            down[i * h + oo] += w * (yd[oo * g + j] + b);
                        }
                    }
                }
                for i in 0..t {
                    for oo in 0..h { x[i * h + oo] = o[i * h + oo] + down[i * h + oo]; }
                }
            } else {
                // ---- FFN DENSE PAR LOTS
                for (pj, dst, taille) in [(&lay.wgate, &mut gate, self.cfg.ffn),
                                          (&lay.wup, &mut up, self.cfg.ffn)] {
                    if let Some(d8) = pj.d.as_ref() {
                        self.pool.gemm_dense_i8(d8, &xi, t, &sx, &mut yl[..d8.n_out * t]);
                        for i in 0..t {
                            for oo in 0..taille { dst[i * taille + oo] = yl[oo * t + i]; }
                        }
                    }
                }
                for i in 0..t {
                    let g0 = gate[i * self.cfg.ffn..(i + 1) * self.cfg.ffn].to_vec();
                    let u0 = up[i * self.cfg.ffn..(i + 1) * self.cfg.ffn].to_vec();
                    let mut gg = g0;
                    Self::activation(&mut gg, &u0, self.cfg.ffn, self.cfg.ffn_act_oss);
                    gate[i * self.cfg.ffn..(i + 1) * self.cfg.ffn].copy_from_slice(&gg);
                }
                quantifier(&gate, &mut gi, &mut sg, self.act_levels, self.act_thresh);
                {
                    let d8 = self.layers[l].wdown.d.as_ref().expect("projection dense requise");
                    self.pool.gemm_dense_i8(d8, &gi, t, &sg, &mut yl[..d8.n_out * t]);
                }
                for i in 0..t {
                    for oo in 0..h {
                        down[i * h + oo] = yl[oo * t + i];
                        x[i * h + oo] = o[i * h + oo] + down[i * h + oo];
                    }
                }
            }
        }
        for i in 0..t {
            let r = x[i * h..(i + 1) * h].to_vec();
            Self::rmsnorm(&r, &self.out_norm, self.cfg.eps, &mut hn[i * h..(i + 1) * h]);
        }
        (0..t).map(|i| hn[i * h..(i + 1) * h].to_vec()).collect()
    }

    /// Un token, une position. Retourne l'état caché après la dernière norme.
    pub fn forward(&mut self, tok: u32, pos: usize) -> Vec<f32> {
        assert!(pos < self.ctx, "contexte dépassé ({pos} ≥ {})", self.ctx);
        // lus AVANT l'emprunt destructuré : la parcimonie par projection
        let tkp = self.act_topk_proj;
        let tkg = self.act_topk;
        let tk = |p: usize| if tkp[p] > 0 { tkp[p] } else { tkg };
        // Lus AVANT l'emprunt destructuré (comme la parcimonie par projection).
        let largeur_profil = self.cfg.ffn.max(self.cfg.ffn_exp);
        self.profil_jetons += 1;
        let Model { g, cfg, layers, out_norm, pool, kv, events, .. } = self;
        let h = cfg.hidden;
        let hd = cfg.head_dim;
        let nh = cfg.n_head;
        let nkv = cfg.n_kv_head;
        let rep = nh / nkv;
        let ctx = self.ctx;

        let mut x = g.row_f32("token_embd.weight", tok as usize, h);
        let mut hn = vec![0f32; h];
        let mut q = vec![0f32; nh * hd];
        let mut k = vec![0f32; nkv * hd];
        let mut v = vec![0f32; nkv * hd];
        let mut att = vec![0f32; nh * hd];
        let mut o = vec![0f32; h];
        let mut gate = vec![0f32; cfg.ffn.max(cfg.ffn_exp)];
        // tampon partagé : sélection k-WTA pendant les produits matriciels, puis
        // quantiles du capteur hebbien — les deux usages ne se recouvrent pas.
        let mut scratch: Vec<f32> = Vec::with_capacity(cfg.ffn);
        let mut up = vec![0f32; cfg.ffn.max(cfg.ffn_exp)];
        let mut exp_out = vec![0f32; h];
        let mut down = vec![0f32; h];
        let mut sc = vec![0f32; pos + 1];
        // scores par TÊTE pour le chemin groupé (cf. plus bas) : les têtes
        // d'un même groupe KV partagent les mêmes clés et valeurs.
        let mut sc2 = vec![0f32; nh * ctx];
        #[cfg(target_arch = "x86_64")]
        let simd = std::is_x86_feature_detected!("avx2") && std::is_x86_feature_detected!("fma");
        #[cfg(not(target_arch = "x86_64"))]
        let simd = false;
        let point = |a: &[f32], b: &[f32]| -> f32 {
            #[cfg(target_arch = "x86_64")]
            if simd { return unsafe { Self::dot8_avx(a, b) }; }
            Self::dot8(a, b)
        };
        let mut attn_idx: Vec<u32> = Vec::with_capacity(ctx);
        let attn_all: Vec<u32> = (0..ctx as u32).collect();

        for l in 0..cfg.n_layer {
            let lay = &layers[l];
            // Fenêtre EFFECTIVE de cette couche : le motif déclaré (gpt-oss :
            // une couche sur deux en attention complète) prime sur le réglage
            // global. Lue en champs directs : `self` est déjà déstructuré.
            let fen = if self.attn_window == 0 { 0 }
                      else if self.swa_pattern <= 1 { self.attn_window }
                      else if l % self.swa_pattern < self.swa_pattern - 1 { self.attn_window }
                      else { 0 };
            let tm = Instant::now();
            Self::rmsnorm(&x, &lay.attn_norm, cfg.eps, &mut hn);
            Self::matvec(pool, &lay.wq, &hn, &mut q, events, self.act_levels, self.act_thresh, tk(0), self.act_renorm, &mut scratch, self.seuil_push);
            Self::matvec(pool, &lay.wk, &hn, &mut k, events, self.act_levels, self.act_thresh, tk(1), self.act_renorm, &mut scratch, self.seuil_push);
            Self::matvec(pool, &lay.wv, &hn, &mut v, events, self.act_levels, self.act_thresh, tk(2), self.act_renorm, &mut scratch, self.seuil_push);
            self.prof[0] += tm.elapsed().as_secs_f64();
            // Qwen3 normalise chaque tête de Q et K avant la rotation.
            if lay.q_norm.is_some() || lay.k_norm.is_some() {
                let mut tmp = vec![0f32; hd];
                if let Some(w) = lay.q_norm.as_ref() {
                    for hh in 0..nh {
                        let t = &mut q[hh * hd..(hh + 1) * hd];
                        Self::rmsnorm(t, w, cfg.eps, &mut tmp);
                        t.copy_from_slice(&tmp);
                    }
                }
                if let Some(w) = lay.k_norm.as_ref() {
                    for hh in 0..nkv {
                        let t = &mut k[hh * hd..(hh + 1) * hd];
                        Self::rmsnorm(t, w, cfg.eps, &mut tmp);
                        t.copy_from_slice(&tmp);
                    }
                }
            }
            let tr = Instant::now();
            match cfg.yarn {
                Some((f, bf, bl, orig, ms)) => {
                    Self::rope_yarn(&mut q, nh, hd, pos, cfg.rope_base, f, bf, bl, orig, ms, cfg.n_rot);
                    Self::rope_yarn(&mut k, nkv, hd, pos, cfg.rope_base, f, bf, bl, orig, ms, cfg.n_rot);
                }
                None => {
                    Self::rope(&mut q, nh, hd, pos, cfg.rope_base, cfg.n_rot);
                    Self::rope(&mut k, nkv, hd, pos, cfg.rope_base, cfg.n_rot);
                }
            }
            if self.qk_topk > 0 {
                Self::creuse_tetes(&mut q, nh, hd, self.qk_topk);
                Self::creuse_tetes(&mut k, nkv, hd, self.qk_topk);
            }
            self.prof[1] += tr.elapsed().as_secs_f64();
            let ta = Instant::now();
            // écriture du cache KV à la position courante
            {
                let kvc = &mut kv[l];
                for hh in 0..nkv {
                    kvc.ecrire(hh, pos, &k[hh * hd..(hh + 1) * hd], &v[hh * hd..(hh + 1) * hd]);
                }
            }
            // attention groupée
            let scale = 1.0 / (hd as f32).sqrt();
            let kvc = &kv[l];
            // Tampons de déquantification : en f32 ils ne servent pas, en 8 bits
            // la clé (ou la valeur) y est reconstruite une fois par groupe.
            let mut kd = vec![0f32; hd];
            let mut vd = vec![0f32; hd];
            let n = pos + 1;
            // ---- chemin GROUPÉ par tête KV (attention complète sans top-k) ----
            // Mesuré : « attention » croît exactement linéairement avec le
            // contexte (0,88 / 1,91 / 3,20 ms à 64 / 128 / 256) — c'est la
            // relecture du cache KV, pas le calcul. Or `rep` têtes de requête
            // partagent une même tête KV : la boucle par tête relisait donc les
            // mêmes clés `rep` fois (7 ici). En parcourant les clés une fois par
            // groupe et en tenant `nh` scores, on divise ce trafic par `rep`.
            // L'arithmétique par tête est inchangée et dans le même ordre : les
            // sorties restent bit à bit identiques.
            let groupe = fen == 0 && self.attn_topk == 0 && rep > 1;
            if groupe {
                let t_scores = Instant::now();
                for kvh in 0..nkv {
                    let h0 = kvh * rep;
                    let h1 = (h0 + rep).min(nh);
                    for t in 0..n {
                        kvc.cle(kvh, t, &mut kd);
                        for hh in h0..h1 {
                            let qh = &q[hh * hd..(hh + 1) * hd];
                            sc2[hh * ctx + t] = point(qh, &kd) * scale;
                        }
                    }
                }
                self.prof[4] += t_scores.elapsed().as_secs_f64();
                let t_soft = Instant::now();
                for kvh in 0..nkv {
                    let h0 = kvh * rep;
                    let h1 = (h0 + rep).min(nh);
                    for hh in h0..h1 {
                        let row = &mut sc2[hh * ctx..hh * ctx + n];
                        let mut mx = f32::NEG_INFINITY;
                        for &v in row.iter() { if v > mx { mx = v; } }
                        let puits = lay.sinks.as_ref().map(|s| s[hh]);
                        if let Some(s) = puits { if s > mx { mx = s; } }
                        let mut sum = 0f32;
                        for v in row.iter_mut() { let e = (*v - mx).exp(); *v = e; sum += e; }
                        if let Some(s) = puits { sum += (s - mx).exp(); }
                        let inv = 1.0 / sum;
                        for v in row.iter_mut() { *v *= inv; }
                    }
                }
                self.prof[5] += t_soft.elapsed().as_secs_f64();
                for kvh in 0..nkv {
                    let h0 = kvh * rep;
                    let h1 = (h0 + rep).min(nh);
                    for hh in h0..h1 {
                        let out = &mut att[hh * hd..(hh + 1) * hd];
                        for v in out.iter_mut() { *v = 0.0; }
                    }
                    for t in 0..n {
                        kvc.valeur(kvh, t, &mut vd);
                        for hh in h0..h1 {
                            let w = sc2[hh * ctx + t];
                            let out = &mut att[hh * hd..(hh + 1) * hd];
                            for (o, x) in out.iter_mut().zip(vd.iter()) { *o += w * x; }
                        }
                    }
                    self.attn_events += ((h1 - h0) * n) as u64;
                }
            }
            for hh in 0..(if groupe { 0 } else { nh }) {
                let kvh = hh / rep;
                let qh = &q[hh * hd..(hh + 1) * hd];
                // produit scalaire écrit en itérateurs : la forme indexée
                // (`for d in 0..hd { s += qh[d]*kt[d] }`) ne se vectorise pas —
                // mesuré à 1,9 GFLOP/s sur un cœur, soit 0,6 opération par cycle.
                // fenêtre glissante : seules les clés de la fenêtre sont notées,
                // plus quelques puits au début (leur attention sert de drain).
                let nw = pos + 1;
                let lo = if fen > 0 && nw > fen {
                    nw - fen
                } else { 0 };
                let ns = if lo > 0 { self.attn_sinks.min(lo) } else { 0 };
                // les puits sont NOTÉS comme les autres : leur donner un score
                // arbitraire (0) fausse la distribution au lieu de la drainer.
                for t in (0..ns).chain(lo..nw) {
                    kvc.cle(kvh, t, &mut kd);
                    sc[t] = point(qh, &kd) * scale;
                }
                for t in ns..lo { sc[t] = f32::NEG_INFINITY; }
                // Attention à k clés. Le CALCUL DES SCORES reste sur toutes les
                // clés — il faut les noter pour savoir lesquelles garder. En
                // revanche le softmax ET la somme pondérée n'itèrent plus que sur
                // les k retenues : c'est là qu'est le O(N·k). Masquer sans
                // réécrire les boucles ne gagnait rien (mesuré : 12,4 → 12,5 ms).
                let n = pos + 1;
                let k = if self.attn_topk > 0 { self.attn_topk.min(n) } else { n };
                if fen > 0 {
                    // pas de top-k : on note exactement les clés de la fenêtre
                    attn_idx.clear();
                    let ns = if lo > 0 { self.attn_sinks.min(lo) } else { 0 };
                    attn_idx.extend((0..ns as u32).chain(lo as u32..n as u32));
                    let iter: &[u32] = &attn_idx;
                    self.attn_events += iter.len() as u64;
                    let mut mx = f32::NEG_INFINITY;
                    for &t in iter { let v = sc[t as usize]; if v > mx { mx = v; } }
                    // Le puits appris compte dans le dénominateur même quand la
                    // fenêtre est active — c'est même son rôle : drainer
                    // l'attention que la fenêtre ne peut pas absorber.
                    let puits = lay.sinks.as_ref().map(|s| s[hh]);
                    if let Some(s) = puits { if s > mx { mx = s; } }
                    let mut sum = 0f32;
                    for &t in iter { let e = (sc[t as usize] - mx).exp(); sc[t as usize] = e; sum += e; }
                    if let Some(s) = puits { sum += (s - mx).exp(); }
                    let inv = 1.0 / sum;
                    for &t in iter { sc[t as usize] *= inv; }
                    let out = &mut att[hh * hd..(hh + 1) * hd];
                    for v in out.iter_mut() { *v = 0.0; }
                    for &t in iter {
                        let w = sc[t as usize];
                        kvc.valeur(kvh, t as usize, &mut vd);
                        for (o, x) in out.iter_mut().zip(vd.iter()) { *o += w * x; }
                    }
                    continue;
                }
                attn_idx.clear();
                if k < n {
                    attn_idx.extend(0..n as u32);
                    attn_idx.select_nth_unstable_by(k, |&a, &b| {
                        sc[b as usize].partial_cmp(&sc[a as usize]).unwrap()
                    });
                    attn_idx.truncate(k);
                }
                // en mode dense, seules les n premières clés existent : itérer
                // sur tout le contexte lirait des scores au-delà de pos.
                let iter: &[u32] = if k < n { &attn_idx } else { &attn_all[..n] };
                self.attn_events += iter.len() as u64;
                // softmax stable sur les seules clés retenues. Le puits appris
                // compte dans le dénominateur MÊME en attention complète : c'est
                // un logit de plus (HF concatène la colonne du puits avant le
                // softmax, puis la retire du numérateur). L'oublier ici ne
                // touchait que les couches non fenêtrées — sur gpt-oss, la
                // moitié du réseau, et précisément celles qui voient loin.
                let puits = lay.sinks.as_ref().map(|s| s[hh]);
                let mut mx = f32::NEG_INFINITY;
                for &t in iter { let v = sc[t as usize]; if v > mx { mx = v; } }
                if let Some(s) = puits { if s > mx { mx = s; } }
                let mut sum = 0f32;
                for &t in iter { let e = (sc[t as usize] - mx).exp(); sc[t as usize] = e; sum += e; }
                if let Some(s) = puits { sum += (s - mx).exp(); }
                let inv = 1.0 / sum;
                for &t in iter { sc[t as usize] *= inv; }
                // somme pondérée : on accumule par clé dans le vecteur de sortie,
                // ce qui lit vc séquentiellement au lieu de le parcourir à stride.
                let out = &mut att[hh * hd..(hh + 1) * hd];
                for v in out.iter_mut() { *v = 0.0; }
                for &t in iter {
                    let w = sc[t as usize];
                    kvc.valeur(kvh, t as usize, &mut vd);
                    for (o, x) in out.iter_mut().zip(vd.iter()) { *o += w * x; }
                }
            }
            self.prof[2] += ta.elapsed().as_secs_f64();
            let tf = Instant::now();
            Self::matvec(pool, &lay.wo, &att, &mut o, events, self.act_levels, self.act_thresh, tk(3), self.act_renorm, &mut scratch, self.seuil_push);
            for i in 0..h { o[i] += x[i]; }
            Self::rmsnorm(&o, &lay.ffn_norm, cfg.eps, &mut hn);
            // ------------------------------------------------------ MoE
            // Un routeur linéaire choisit `k` experts parmi `n` ; seuls leurs
            // poids sont lus. C'est la parcimonie **structurelle** — 8 experts
            // sur 128, soit 6 % du FFN — et c'est le régime où l'architecture
            // événementielle cesse d'être un coût.
            if let Some(moe) = lay.moe.as_ref() {
                let ne = cfg.n_expert;
                let k = if self.moe_topk > 0 { self.moe_topk } else { cfg.n_expert_used };
                let k = k.clamp(1, ne);
                let mut sc_e: Vec<f32> = (0..ne).map(|e| {
                    let r = &moe.routeur[e * h..(e + 1) * h];
                    let s: f32 = r.iter().zip(hn.iter()).map(|(a, b)| a * b).sum();
                    s + moe.routeur_biais.as_ref().map_or(0.0, |b| b[e])
                }).collect();
                let mut idx: Vec<u32> = (0..ne as u32).collect();
                let mut inv_k = 1.0f32;
                if cfg.routeur_topk_softmax {
                    // gpt-oss : le top-k se décide sur les logits BRUTS, et le
                    // softmax ne porte que sur les retenus.
                    if k < ne {
                        idx.select_nth_unstable_by(k, |&a, &b| {
                            sc_e[b as usize].partial_cmp(&sc_e[a as usize]).unwrap()
                        });
                        idx.truncate(k);
                    }
                    let mx = idx.iter().map(|&e| sc_e[e as usize])
                               .fold(f32::NEG_INFINITY, f32::max);
                    let mut somme = 0f32;
                    for &e in &idx { let v = (sc_e[e as usize] - mx).exp(); sc_e[e as usize] = v; somme += v; }
                    if somme > 0.0 { inv_k = 1.0 / somme; }
                } else {
                    // Qwen3-MoE : softmax sur tous, puis sélection, puis
                    // renormalisation sur les retenus.
                    let mx = sc_e.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
                    let mut somme = 0f32;
                    for v in sc_e.iter_mut() { *v = (*v - mx).exp(); somme += *v; }
                    if somme > 0.0 { for v in sc_e.iter_mut() { *v /= somme; } }
                    if k < ne {
                        idx.select_nth_unstable_by(k, |&a, &b| {
                            sc_e[b as usize].partial_cmp(&sc_e[a as usize]).unwrap()
                        });
                        idx.truncate(k);
                    }
                    let somme_k: f32 = idx.iter().map(|&e| sc_e[e as usize]).sum();
                    inv_k = if somme_k > 0.0 { 1.0 / somme_k } else { 0.0 };
                }
                if self.profil_experts.is_some() {
                    let base = l * ne;
                    let p = self.profil_experts.as_mut().unwrap();
                    for &e in &idx { p[base + e as usize] += 1; }
                }
                for v in down.iter_mut() { *v = 0.0; }
                for &e in &idx {
                    let w_exp = sc_e[e as usize] * inv_k;
                    let mg = moe.gate.expert(e as usize);
                    Self::matvec_q4(pool, &mg, &hn, &mut gate, self.act_levels,
                                    self.act_thresh, tk(4), self.act_renorm, &mut scratch,
                                    moe.biais_gate.as_ref().map(|b| &b[e as usize * moe.n_ff..]));
                    let mu = moe.up.expert(e as usize);
                    Self::matvec_q4(pool, &mu, &hn, &mut up, self.act_levels,
                                    self.act_thresh, tk(5), self.act_renorm, &mut scratch,
                                    moe.biais_up.as_ref().map(|b| &b[e as usize * moe.n_ff..]));
                    Self::activation(&mut gate, &up, cfg.ffn_exp, cfg.ffn_act_oss);
                    Self::compter_neurones(&mut self.profil_neurones, largeur_profil,
                                           l, &gate[..cfg.ffn_exp]);
                    let md = moe.down.expert(e as usize);
                    Self::matvec_q4(pool, &md, &gate, &mut exp_out, self.act_levels,
                                    self.act_thresh, tk(6), self.act_renorm, &mut scratch,
                                    // Le biais de descente se découpe par la
                                    // largeur de SORTIE (h), pas par n_ff : les
                                    // deux coïncident sur gpt-oss (2 880) mais
                                    // pas sur Qwen3-MoE (768 contre 2 048).
                                    moe.biais_down.as_ref().map(|b| &b[e as usize * h..]));
                    for i in 0..h { down[i] += w_exp * exp_out[i]; }
                }
                if let Some((sg, su, sd)) = moe.shexp.as_ref() {
                    let mg = sg.expert(0);
                    Self::matvec_q4(pool, &mg, &hn, &mut gate, self.act_levels,
                                    self.act_thresh, tk(4), self.act_renorm, &mut scratch, None);
                    let mu = su.expert(0);
                    Self::matvec_q4(pool, &mu, &hn, &mut up, self.act_levels,
                                    self.act_thresh, tk(5), self.act_renorm, &mut scratch, None);
                    Self::activation(&mut gate, &up, cfg.ffn_exp, cfg.ffn_act_oss);
                    let md = sd.expert(0);
                    Self::matvec_q4(pool, &md, &gate, &mut exp_out, self.act_levels,
                                    self.act_thresh, tk(6), self.act_renorm, &mut scratch, None);
                    for i in 0..h { down[i] += exp_out[i]; }
                }
                if let Some((gl, gg)) = self.ffn_gain {
                    if gl == l { for v in down.iter_mut() { *v *= gg; } }
                }
                for i in 0..h { x[i] = o[i] + down[i]; }
                self.prof[3] += tf.elapsed().as_secs_f64();
                continue;
            }
            Self::matvec(pool, &lay.wgate, &hn, &mut gate, events, self.act_levels, self.act_thresh, tk(4), self.act_renorm, &mut scratch, self.seuil_push);
            // --- capteur hebbien : espionne la co-activation (entrée, sortie)
            // de la projection gate. Aucun effet sur le calcul.
            if let Some(hb) = self.hebb.as_mut() {
                if hb.layer == l {
                    if hb.log_on { hb.log.extend_from_slice(&hn); }
                    let (hn2, gate2) = (&hn, &gate);
                    let mut seuil = std::mem::take(&mut scratch);
                    hb.observe(hn2, gate2, &mut seuil);
                    scratch = seuil;
                }
            }
            Self::matvec(pool, &lay.wup, &hn, &mut up, events, self.act_levels, self.act_thresh, tk(5), self.act_renorm, &mut scratch, self.seuil_push);
            Self::activation(&mut gate, &up, cfg.ffn, cfg.ffn_act_oss);
            Self::compter_neurones(&mut self.profil_neurones, largeur_profil,
                                   l, &gate[..cfg.ffn]);
            Self::matvec(pool, &lay.wdown, &gate, &mut down, events, self.act_levels, self.act_thresh, tk(6), self.act_renorm, &mut scratch, self.seuil_push);
            // --- greffon : neurone supplémentaire, sans réentraînement
            if let Some(pt) = self.patch.as_ref() {
                if pt.layer == l {
                    let mut g = 0f32;
                    let mut uu = 0f32;
                    for i in 0..h { g += pt.u[i] * hn[i]; uu += pt.v[i] * hn[i]; }
                    let a = (g / (1.0 + (-g).exp())) * uu;
                    for i in 0..h { down[i] += pt.d[i] * a; }
                }
            }
            if let Some((gl, g)) = self.ffn_gain {
                if gl == l { for v in down.iter_mut() { *v *= g; } }
            }
            for i in 0..h { x[i] = o[i] + down[i]; }
            self.prof[3] += tf.elapsed().as_secs_f64();
        }
        Self::rmsnorm(&x, out_norm, cfg.eps, &mut hn);
        hn
    }

    /// Tête de sortie : produits scalaires entiers sur les lignes Q8_0 du
    /// plafond d'embedding (poids liés). Parallélisé par tranches de vocabulaire.
    pub fn logits(&mut self, h: &[f32]) -> Vec<f32> {
        let mut scratch = Vec::with_capacity(h.len());
        let (sv, sx) = match Self::quant_scratch(h, self.act_levels, self.act_thresh,
                                                self.act_topk, self.act_renorm, &mut scratch) {
            Some(v) => v,
            None => return vec![0f32; self.cfg.vocab],
        };
        // Chemin GPU : les poids de la tête sont déjà en mémoire vidéo ; seules
        // les activations montent et les logits descendent.
        if let (Some(machine), Some(m)) = (crate::gpu::instance(), self.tete_gpu.as_ref()) {
            let mut xd = vec![0i32; h.len()];
            for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { xd[i as usize] = v; }
            if let Some(y) = machine.tete_warp(m, &xd) {
                return y.iter().map(|v| v * sx).collect();
            }
        }
        // Tête 4 bits : chemin DIRECT par tranches de vocabulaire, comme la tête
        // int8 — et non par le pool. Le pool coûtait 4 ms de plus par jeton pour
        // 72 Mo lus au lieu de 136 : ses seize tampons de sortie (9,7 Mo) sont
        // écrits, remis à zéro puis réduits, soit plus de trafic que les poids
        // économisés.
        if self.head4.is_some() {
            let xi: Vec<i16> = sv.idx.iter().zip(sv.val.iter())
                .fold(vec![0i16; h.len()], |mut a, (&i, &v)| {
                    a[i as usize] = v.clamp(-32767, 32767) as i16; a
                });
            let d = self.head4.take().unwrap();
            let dref = &d;
            let vocab = d.n_out;
            let nt = self.pool.threads().max(1);
            let chunk = vocab.div_ceil(nt);
            let mut out = vec![0f32; vocab];
            let xi = &xi;
            let sx32 = &crate::list::sommes32(xi);
            std::thread::scope(|sc| {
                for (ci, part) in out.chunks_mut(chunk).enumerate() {
                    sc.spawn(move || {
                        let base = ci * chunk;
                        for (j, o) in part.iter_mut().enumerate() {
                            *o = dref.dot16(base + j, xi, sx32) * sx;
                        }
                    });
                }
            });
            self.head4 = Some(d);
            return out;
        }
        // int16 : la troncature en i8 ruinerait une activation quantifiée sur
        // 32767 niveaux (le corps du modèle, lui, n'est pas concerné : il
        // transporte des i32 dans le vecteur creux).
        let mut qx = vec![0i16; h.len()];
        for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { qx[i as usize] = v as i16; }
        let vocab = self.cfg.vocab;
        let view = self.g.q8_view(&self.tete);
        let nt = self.pool.threads().max(1);
        let chunk = (vocab + nt - 1) / nt;
        let mut out = vec![0f32; vocab];
        let g = &self.g;
        let view = &view;
        std::thread::scope(|s| {
            for (ci, part) in out.chunks_mut(chunk).enumerate() {
                let qx = &qx;
                s.spawn(move || {
                    let base = ci * chunk;
                    for (j, o) in part.iter_mut().enumerate() {
                        *o = g.q8_dot_at(view, base + j, qx) * sx;
                    }
                });
            }
        });
        out
    }

    /// Génère `n_new` tokens après `ids`. `temp` ≤ 0 ⇒ glouton (déterministe).
    /// Génère `n_new` jetons. `flux` reçoit chaque jeton **dès qu'il est
    /// produit**, ce qui permet de l'afficher sans attendre la fin.
    #[allow(clippy::too_many_arguments)]
    pub fn generate(&mut self, ids: &[u32], n_new: usize, temp: f32, top_p: f32,
                    rep_pen: f32, hist: usize, mut flux: Option<&mut dyn FnMut(u32)>)
                    -> (Vec<u32>, Stats) {
        let t0 = Instant::now();
        let mut last = Vec::new();
        let mut events0 = self.events;
        for (pos, &t) in ids.iter().enumerate() {
            last = self.forward(t, pos);
        }
        let prompt_s = t0.elapsed().as_secs_f64();
        let prompt_events = self.events - events0;
        let mut out = Vec::with_capacity(n_new);
        let t1 = Instant::now();
        for step in 0..n_new {
            let mut logits = self.logits(&last);
            // Historique pour la pénalité : les derniers jetons vus, invite
            // comprise. Sans elle, une génération longue finit en boucle —
            // c'est le mode d'échec le plus visible en usage réel.
            let n_hist = if hist == 0 { ids.len() + out.len() } else { hist };
            let debut = ids.len() + out.len() - n_hist.min(ids.len() + out.len());
            let recents: Vec<u32> = ids[debut.min(ids.len())..].iter().copied()
                .chain(out.iter().copied()).collect();
            let next = if temp <= 0.0 && rep_pen <= 1.0 {
                let mut best = 0usize;
                for (i, &v) in logits.iter().enumerate() { if v > logits[best] { best = i; } }
                best as u32
            } else {
                sample_avance(&mut logits, temp.max(1e-4), top_p, &recents, rep_pen)
            };
            out.push(next);
            if let Some(f) = flux.as_mut() { f(next); }
            if Some(next) == self.stop_id || Some(next) == self.stop_id2 { break; }
            let pos = ids.len() + step;
            last = self.forward(next, pos);
        }
        let gen_s = t1.elapsed().as_secs_f64();
        events0 = self.events - events0 - prompt_events;
        let _ = events0;
        let st = Stats {
            events: self.events,
            prompt_s, gen_s,
            n_prompt: ids.len(), n_gen: out.len(),
        };
        (out, st)
    }

    pub fn events_total(&self) -> u64 { self.events }
    pub fn reset_events(&mut self) { self.events = 0; }
}

/// Échantillonnage température + top-k (k = 40), avec un générateur xorshift
/// déterministe : pas de dépendance, pas d'entropie système.
/// Échantillonnage complet : pénalité de répétition, top-k, top-p (noyau).
///
/// La pénalité suit la formule usuelle : un logit positif est divisé, un logit
/// négatif multiplié — donc dans les deux cas on s'éloigne du jeton déjà vu.
fn sample_avance(logits: &mut [f32], temp: f32, top_p: f32, recents: &[u32],
                 rep_pen: f32) -> u32 {
    if rep_pen > 1.0 {
        for &t in recents {
            let v = logits[t as usize];
            logits[t as usize] = if v > 0.0 { v / rep_pen } else { v * rep_pen };
        }
    }
    let mut idx: Vec<u32> = (0..logits.len() as u32).collect();
    idx.sort_unstable_by(|&a, &b| logits[b as usize].partial_cmp(&logits[a as usize]).unwrap());
    let mx = logits[idx[0] as usize];
    let k = 40.min(idx.len());
    let mut w = Vec::with_capacity(k);
    let mut sum = 0f32;
    for &i in &idx[..k] {
        let e = ((logits[i as usize] - mx) / temp).exp();
        w.push(e);
        sum += e;
    }
    // top-p : plus petit ensemble dont la masse dépasse p.
    if top_p < 1.0 && sum > 0.0 {
        let mut cum = 0f32;
        let mut garde = w.len();
        for (j, &e) in w.iter().enumerate() {
            cum += e / sum;
            if cum >= top_p { garde = j + 1; break; }
        }
        w.truncate(garde);
        sum = w.iter().sum();
    }
    let mut r = (rand_u64() as f64 / u64::MAX as f64) as f32 * sum;
    for (j, &e) in w.iter().enumerate() {
        r -= e;
        if r <= 0.0 { return idx[j]; }
    }
    idx[w.len().saturating_sub(1)]
}

fn sample(logits: &[f32], temp: f32) -> u32 {
    let mut idx: Vec<u32> = (0..logits.len() as u32).collect();
    idx.sort_unstable_by(|&a, &b| logits[b as usize].partial_cmp(&logits[a as usize]).unwrap());
    let k = 40.min(idx.len());
    let mx = logits[idx[0] as usize];
    let mut w = Vec::with_capacity(k);
    let mut sum = 0f32;
    for &i in &idx[..k] {
        let e = ((logits[i as usize] - mx) / temp).exp();
        w.push(e);
        sum += e;
    }
    let mut r = (rand_u64() as f64 / u64::MAX as f64) as f32 * sum;
    for (j, &e) in w.iter().enumerate() {
        r -= e;
        if r <= 0.0 { return idx[j]; }
    }
    idx[k - 1]
}

fn rand_u64() -> u64 {
    use std::sync::atomic::{AtomicU64, Ordering};
    static S: AtomicU64 = AtomicU64::new(0x9E3779B97F4A7C15);
    let mut x = S.load(Ordering::Relaxed);
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    S.store(x, Ordering::Relaxed);
    x
}

#[cfg(test)]
mod tests_kv {
    use super::KvCache;

    /// Aller-retour : ce qui est écrit doit se relire à l'erreur de
    /// quantification près, **aux deux précisions**, et une réécriture de la
    /// même position doit effacer l'ancienne valeur (le cache est réutilisé
    /// d'une fenêtre à l'autre).
    #[test]
    fn aller_retour_kv() {
        for bits in [32u32, 8, 4] {
            let (nkv, ctx, hd) = (2usize, 4usize, 8usize);
            let mut c = KvCache::new(bits, nkv, ctx, hd);
            let k: Vec<f32> = (0..hd).map(|i| (i as f32 - 3.5) * 0.7).collect();
            let v: Vec<f32> = (0..hd).map(|i| 1.5 - i as f32 * 0.2).collect();
            c.ecrire(1, 2, &k, &v);
            let mut tk = vec![0f32; hd];
            let mut tv = vec![0f32; hd];
            c.cle(1, 2, &mut tk);
            c.valeur(1, 2, &mut tv);
            // L'erreur permise est d'une DEMI-marche d'arrondi, en absolu :
            // l'échelle est celle du vecteur (max/niveaux), pas celle de chaque
            // composante. Exiger une erreur relative d'un niveau rejetait des
            // arrondis parfaitement corrects.
            let niv = if bits == 4 { 7.0f32 } else if bits == 8 { 127.0 } else { 1e9 };
            let (mk, mv) = (k.iter().fold(0f32, |a, x| a.max(x.abs())),
                            v.iter().fold(0f32, |a, x| a.max(x.abs())));
            let (dk, dv) = (0.5 * mk / niv + 1e-6, 0.5 * mv / niv + 1e-6);
            for i in 0..hd {
                assert!((k[i] - tk[i]).abs() <= dk, "clé {i} bits {bits} : {} contre {}", tk[i], k[i]);
                assert!((v[i] - tv[i]).abs() <= dv, "valeur {i} bits {bits} : {} contre {}", tv[i], v[i]);
            }
            // Réécriture : les nibbles de l'ancienne valeur ne doivent pas rester.
            let k2: Vec<f32> = k.iter().map(|x| -x).collect();
            c.ecrire(1, 2, &k2, &v);
            c.cle(1, 2, &mut tk);
            for i in 0..hd {
                assert!((k2[i] - tk[i]).abs() <= dk,
                        "réécriture {i} bits {bits} : {} contre {}", tk[i], k2[i]);
            }
        }
    }
}
