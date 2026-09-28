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
}

/// Une projection, dans l'un des deux formats, plus son biais éventuel.
/// `m` = listes d'événements (architecture du projet) ;
/// `d` = matrice dense int8 (référence de comparaison, sans événements).
pub struct Proj {
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
    Some(Moe { routeur, gate, up, down, shexp })
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

impl Proj {
    /// Projection vide : les modèles à experts n'ont **pas** de tenseur FFN
    /// dense, et le moteur ne doit pas le chercher.
    pub fn vide() -> Self {
        Proj { m: None, d: None, q4: None, bias: None }
    }

    fn load(g: &Gguf, name: &str, bias: Option<&str>, dense: bool, auto: bool, keep: f32,
            q4: bool) -> Self {
        let t = g.tensor(name).unwrap_or_else(|| panic!("tenseur {name} absent"));
        let n_out = t.dims[0] as usize;
        let n_in = t.dims[1] as usize;
        let mut w = g.dequant(name);
        if keep < 0.0 { prune_structured(&mut w, n_out, n_in, -keep); }
        else { prune_rows(&mut w, n_out, n_in, keep); }
        // `auto` charge les DEUX formes : le moteur choisit ensuite, par mesure
        // de la densité d'activation, entre dispersion (push) et produit
        // scalaire dense (pull). Le croisement mesuré est à 10 %.
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
            match (keep >= 1.0, g.q8_blocks(name)) {
                (true, Some((buf, nb))) =>
                    (None, Some(unsafe { DenseQ8::emprunter_q8(buf.as_ptr(), n_out, n_in, nb) }), None),
                _ => (None, Some(DenseQ8::build(&w, n_out, n_in)), None),
            }
        } else if auto {
            let dense8 = match (keep >= 1.0, g.q8_blocks(name)) {
                (true, Some((buf, nb))) =>
                    unsafe { DenseQ8::emprunter_q8(buf.as_ptr(), n_out, n_in, nb) },
                _ => DenseQ8::build(&w, n_out, n_in),
            };
            (Some(PushMat::build(&w, n_out, n_in)), Some(dense8), None)
        } else {
            (Some(PushMat::build(&w, n_out, n_in)), None, None)
        };
        // Tous les modèles n'ont pas de biais QKV (Qwen3 n'en a pas) : son
        // absence est normale, pas une erreur.
        let bias = bias.filter(|b| g.tensor(b).is_some()).map(|b| g.dequant(b));
        Proj { m, d, q4: q4v, bias }
    }
}

pub struct Model {
    pub g: Gguf,
    pub cfg: Cfg,
    pub layers: Vec<Layer>,
    pub out_norm: Vec<f32>,
    pub pool: Pool,
    /// cache KV, par couche : `[n_kv_head × ctx × head_dim]`
    kv_k: Vec<Vec<f32>>,
    kv_v: Vec<Vec<f32>>,
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
    pub attn_window: usize,
    pub attn_sinks: usize,
    /// Seuil de bascule push/pull, en fraction de sources actives. Mesuré : les
    /// deux architectures se croisent à 10 % de densité ; on bascule un peu
    /// au-dessus pour absorber la marge d'erreur.
    pub seuil_push: f32,
    /// Token d'arrêt (EOS / <|im_end|>) : la génération s'interrompt dessus.
    pub stop_id: Option<u32>,
    /// Postes de temps cumulés, en secondes (diagnostic).
    pub prof: [f64; 6],
    /// Nom du tenseur de la tête de sortie : `output.weight` s'il existe,
    /// sinon `token_embd.weight` (poids liés). Les modèles non liés — le
    /// Qwen2.5-1.5B en fait partie — ont une matrice de sortie **différente**
    /// de la table d'embedding ; lire la mauvaise donne une perplexité de
    /// 50 000 au lieu de 11,4.
    pub tete: String,
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

impl Model {
    pub fn load(path: &str, ctx: usize, n_threads: usize, dense: bool, keep: f32,
                auto: bool, q4: u8) -> Model {
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
                wq: Proj::load(&g, &p("attn_q.weight"), Some(&p("attn_q.bias")), dense || q4 != 0, auto, keep, q4 & 2 != 0),
                wk: Proj::load(&g, &p("attn_k.weight"), Some(&p("attn_k.bias")), dense || q4 != 0, auto, keep, q4 & 2 != 0),
                wv: Proj::load(&g, &p("attn_v.weight"), Some(&p("attn_v.bias")), dense || q4 != 0, auto, keep, q4 & 2 != 0),
                wo: Proj::load(&g, &p("attn_output.weight"), None, dense || q4 != 0, auto, keep, q4 & 2 != 0),
                ffn_norm: g.dequant(&p("ffn_norm.weight")),
                q_norm: if g.tensor(&p("attn_q_norm.weight")).is_some() {
                    Some(g.dequant(&p("attn_q_norm.weight"))) } else { None },
                k_norm: if g.tensor(&p("attn_k_norm.weight")).is_some() {
                    Some(g.dequant(&p("attn_k_norm.weight"))) } else { None },
                wgate: if cfg.n_expert > 0 { Proj::vide() } else {
                    Proj::load(&g, &p("ffn_gate.weight"), None, dense || q4 != 0, auto, keep, q4 & 1 != 0) },
                wup: if cfg.n_expert > 0 { Proj::vide() } else {
                    Proj::load(&g, &p("ffn_up.weight"), None, dense || q4 != 0, auto, keep, q4 & 1 != 0) },
                wdown: if cfg.n_expert > 0 { Proj::vide() } else {
                    Proj::load(&g, &p("ffn_down.weight"), None, dense || q4 != 0, auto, keep, q4 & 1 != 0) },
                moe: charger_moe(&g, l, cfg.n_expert),
            };
            for pj in [&lay.wq, &lay.wk, &lay.wv, &lay.wo, &lay.wgate, &lay.wup, &lay.wdown] {
                if let Some(m) = &pj.m { bytes += m.data.len() as u64; }
                if let Some(d) = &pj.d { bytes += d.q.len() as u64 + d.scale.len() as u64 * 4; }
            }
            layers.push(lay);
        }
        let out_norm = g.dequant("output_norm.weight");
        let kv = vec![0f32; cfg.n_kv_head * ctx * cfg.head_dim];
        let pool = Pool::new(n_threads, cfg.hidden);
        eprintln!("[modele] {} couches chargées en {:?} — listes {:.2} Go{} , {} threads",
                  cfg.n_layer, t0.elapsed(), bytes as f64 / 1e9,
                  if keep < 0.0 { format!(" (poids gardés : {:.0} % structuré)", -keep * 100.0) }
                  else if keep < 1.0 { format!(" (poids gardés : {:.0} %)", keep * 100.0) }
                  else { String::new() },
                  pool.threads());
        let n_layer = cfg.n_layer;
        let tete = if g.tensor("output.weight").is_some() { "output.weight" } else { "token_embd.weight" };
        let tete = tete.to_string();
        // Tête en 4 bits : la plus grosse matrice du modèle, donc le plus gros
        // gain possible sur un noyau déjà au mur de la bande passante.
        // La tête emprunte dès que la source est déjà quantifiée sur 4 ou
        // 6 bits : c'est exact (aucune requantification) et six fois plus
        // rapide que le chemin scalaire Q6_K, qui coûtait 42 % du temps par
        // jeton sur un 7B.
        let tete_quantifiee = g.q6k_blocks(&tete).is_some() || g.q4k_blocks(&tete).is_some()
            || g.mxfp4_blocks(&tete).is_some() || g.q4_blocks(&tete).is_some();
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
            kv_k: vec![kv.clone(); n_layer], kv_v: vec![kv; n_layer],
            ctx, events: 0, act_levels: 127.0, act_thresh: 0.0, act_topk: 0, act_renorm: false,
            act_topk_proj: [0; 7], attn_topk: 0, attn_events: 0, qk_topk: 0,
            moe_topk: 0, attn_window: 0, attn_sinks: 4, seuil_push: 0.22,
            stop_id: None, prof: [0.0; 6],
            tete,
            head4,
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
                 scratch: &mut Vec<f32>) {
        let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
            for v in out[..m.n_out].iter_mut() { *v = 0.0; }
            return;
        };
        let mut xd = vec![0i32; x.len()];
        for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { xd[i as usize] = v; }
        let y = pool.matvec_dense_q4(m, &xd, sx);
        out[..m.n_out].copy_from_slice(&y[..m.n_out]);
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

    /// RoPE « neox » (Qwen2) : rotation des deux moitiés de chaque tête.
    fn rope(v: &mut [f32], n_head: usize, head_dim: usize, pos: usize, base: f32) {
        let half = head_dim / 2;
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

    /// Un token, une position. Retourne l'état caché après la dernière norme.
    pub fn forward(&mut self, tok: u32, pos: usize) -> Vec<f32> {
        assert!(pos < self.ctx, "contexte dépassé ({pos} ≥ {})", self.ctx);
        // lus AVANT l'emprunt destructuré : la parcimonie par projection
        let tkp = self.act_topk_proj;
        let tkg = self.act_topk;
        let tk = |p: usize| if tkp[p] > 0 { tkp[p] } else { tkg };
        let Model { g, cfg, layers, out_norm, pool, kv_k, kv_v, events, .. } = self;
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
            Self::rope(&mut q, nh, hd, pos, cfg.rope_base);
            Self::rope(&mut k, nkv, hd, pos, cfg.rope_base);
            if self.qk_topk > 0 {
                Self::creuse_tetes(&mut q, nh, hd, self.qk_topk);
                Self::creuse_tetes(&mut k, nkv, hd, self.qk_topk);
            }
            self.prof[1] += tr.elapsed().as_secs_f64();
            let ta = Instant::now();
            // écriture du cache KV à la position courante
            {
                let kc = &mut kv_k[l];
                let vc = &mut kv_v[l];
                for hh in 0..nkv {
                    let dst = (hh * ctx + pos) * hd;
                    kc[dst..dst + hd].copy_from_slice(&k[hh * hd..(hh + 1) * hd]);
                    vc[dst..dst + hd].copy_from_slice(&v[hh * hd..(hh + 1) * hd]);
                }
            }
            // attention groupée
            let scale = 1.0 / (hd as f32).sqrt();
            let kc = &kv_k[l];
            let vc = &kv_v[l];
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
            let groupe = self.attn_window == 0 && self.attn_topk == 0 && rep > 1;
            if groupe {
                let t_scores = Instant::now();
                for kvh in 0..nkv {
                    let h0 = kvh * rep;
                    let h1 = (h0 + rep).min(nh);
                    for t in 0..n {
                        let kt = &kc[(kvh * ctx + t) * hd..(kvh * ctx + t) * hd + hd];
                        for hh in h0..h1 {
                            let qh = &q[hh * hd..(hh + 1) * hd];
                            sc2[hh * ctx + t] = point(qh, kt) * scale;
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
                        let mut sum = 0f32;
                        for v in row.iter_mut() { let e = (*v - mx).exp(); *v = e; sum += e; }
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
                        let vt = &vc[(kvh * ctx + t) * hd..(kvh * ctx + t) * hd + hd];
                        for hh in h0..h1 {
                            let w = sc2[hh * ctx + t];
                            let out = &mut att[hh * hd..(hh + 1) * hd];
                            for (o, x) in out.iter_mut().zip(vt.iter()) { *o += w * x; }
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
                let lo = if self.attn_window > 0 && nw > self.attn_window {
                    nw - self.attn_window
                } else { 0 };
                let ns = if lo > 0 { self.attn_sinks.min(lo) } else { 0 };
                // les puits sont NOTÉS comme les autres : leur donner un score
                // arbitraire (0) fausse la distribution au lieu de la drainer.
                for t in (0..ns).chain(lo..nw) {
                    let kt = &kc[(kvh * ctx + t) * hd..(kvh * ctx + t) * hd + hd];
                    sc[t] = point(qh, kt) * scale;
                }
                for t in ns..lo { sc[t] = f32::NEG_INFINITY; }
                // Attention à k clés. Le CALCUL DES SCORES reste sur toutes les
                // clés — il faut les noter pour savoir lesquelles garder. En
                // revanche le softmax ET la somme pondérée n'itèrent plus que sur
                // les k retenues : c'est là qu'est le O(N·k). Masquer sans
                // réécrire les boucles ne gagnait rien (mesuré : 12,4 → 12,5 ms).
                let n = pos + 1;
                let k = if self.attn_topk > 0 { self.attn_topk.min(n) } else { n };
                if self.attn_window > 0 {
                    // pas de top-k : on note exactement les clés de la fenêtre
                    attn_idx.clear();
                    let ns = if lo > 0 { self.attn_sinks.min(lo) } else { 0 };
                    attn_idx.extend((0..ns as u32).chain(lo as u32..n as u32));
                    let iter: &[u32] = &attn_idx;
                    self.attn_events += iter.len() as u64;
                    let mut mx = f32::NEG_INFINITY;
                    for &t in iter { let v = sc[t as usize]; if v > mx { mx = v; } }
                    let mut sum = 0f32;
                    for &t in iter { let e = (sc[t as usize] - mx).exp(); sc[t as usize] = e; sum += e; }
                    let inv = 1.0 / sum;
                    for &t in iter { sc[t as usize] *= inv; }
                    let out = &mut att[hh * hd..(hh + 1) * hd];
                    for v in out.iter_mut() { *v = 0.0; }
                    for &t in iter {
                        let w = sc[t as usize];
                        let vt = &vc[(kvh * ctx + t as usize) * hd..(kvh * ctx + t as usize) * hd + hd];
                        for (o, x) in out.iter_mut().zip(vt.iter()) { *o += w * x; }
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
                // softmax stable sur les seules clés retenues
                let mut mx = f32::NEG_INFINITY;
                for &t in iter { let v = sc[t as usize]; if v > mx { mx = v; } }
                let mut sum = 0f32;
                for &t in iter { let e = (sc[t as usize] - mx).exp(); sc[t as usize] = e; sum += e; }
                let inv = 1.0 / sum;
                for &t in iter { sc[t as usize] *= inv; }
                // somme pondérée : on accumule par clé dans le vecteur de sortie,
                // ce qui lit vc séquentiellement au lieu de le parcourir à stride.
                let out = &mut att[hh * hd..(hh + 1) * hd];
                for v in out.iter_mut() { *v = 0.0; }
                for &t in iter {
                    let w = sc[t as usize];
                    let vt = &vc[(kvh * ctx + t as usize) * hd..(kvh * ctx + t as usize) * hd + hd];
                    for (o, x) in out.iter_mut().zip(vt.iter()) { *o += w * x; }
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
                    r.iter().zip(hn.iter()).map(|(a, b)| a * b).sum()
                }).collect();
                let mx = sc_e.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
                let mut somme = 0f32;
                for v in sc_e.iter_mut() { *v = (*v - mx).exp(); somme += *v; }
                if somme > 0.0 { for v in sc_e.iter_mut() { *v /= somme; } }
                let mut idx: Vec<u32> = (0..ne as u32).collect();
                if k < ne {
                    idx.select_nth_unstable_by(k, |&a, &b| {
                        sc_e[b as usize].partial_cmp(&sc_e[a as usize]).unwrap()
                    });
                    idx.truncate(k);
                }
                let somme_k: f32 = idx.iter().map(|&e| sc_e[e as usize]).sum();
                let inv_k = if somme_k > 0.0 { 1.0 / somme_k } else { 0.0 };
                for v in down.iter_mut() { *v = 0.0; }
                for &e in &idx {
                    let w_exp = sc_e[e as usize] * inv_k;
                    let mg = moe.gate.expert(e as usize);
                    Self::matvec_q4(pool, &mg, &hn, &mut gate, self.act_levels,
                                    self.act_thresh, tk(4), self.act_renorm, &mut scratch);
                    let mu = moe.up.expert(e as usize);
                    Self::matvec_q4(pool, &mu, &hn, &mut up, self.act_levels,
                                    self.act_thresh, tk(5), self.act_renorm, &mut scratch);
                    for i in 0..cfg.ffn_exp {
                        gate[i] = (gate[i] / (1.0 + (-gate[i]).exp())) * up[i];
                    }
                    let md = moe.down.expert(e as usize);
                    Self::matvec_q4(pool, &md, &gate, &mut exp_out, self.act_levels,
                                    self.act_thresh, tk(6), self.act_renorm, &mut scratch);
                    for i in 0..h { down[i] += w_exp * exp_out[i]; }
                }
                if let Some((sg, su, sd)) = moe.shexp.as_ref() {
                    let mg = sg.expert(0);
                    Self::matvec_q4(pool, &mg, &hn, &mut gate, self.act_levels,
                                    self.act_thresh, tk(4), self.act_renorm, &mut scratch);
                    let mu = su.expert(0);
                    Self::matvec_q4(pool, &mu, &hn, &mut up, self.act_levels,
                                    self.act_thresh, tk(5), self.act_renorm, &mut scratch);
                    for i in 0..cfg.ffn_exp {
                        gate[i] = (gate[i] / (1.0 + (-gate[i]).exp())) * up[i];
                    }
                    let md = sd.expert(0);
                    Self::matvec_q4(pool, &md, &gate, &mut exp_out, self.act_levels,
                                    self.act_thresh, tk(6), self.act_renorm, &mut scratch);
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
            for i in 0..cfg.ffn { gate[i] = (gate[i] / (1.0 + (-gate[i]).exp())) * up[i]; }
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
    pub fn generate(&mut self, ids: &[u32], n_new: usize, temp: f32) -> (Vec<u32>, Stats) {
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
            let logits = self.logits(&last);
            let next = if temp <= 0.0 {
                let mut best = 0usize;
                for (i, &v) in logits.iter().enumerate() { if v > logits[best] { best = i; } }
                best as u32
            } else {
                sample(&logits, temp)
            };
            out.push(next);
            if Some(next) == self.stop_id { break; }
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
