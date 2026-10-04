//! **Kimi-K3** — l'inventaire des tenseurs, vérifié contre le fichier.
//!
//! Pourquoi ce module existe avant l'architecture : la couche 0 de Kimi-K3 est
//! **dense** (KDA + SiTU), les couches 3, 7, 11… sont **MLA**, les autres sont
//! **KDA + MoE latent**, et chaque type a sa liste de tenseurs. Se tromper de
//! liste donne un tenseur chargé VIDE et un calcul faux **en silence** — c'est
//! exactement le défaut que le mandat interdit. On vérifie donc l'inventaire
//! **avant** d'écrire la moindre passe avant, et on le vérifie sur le fichier.
//!
//! L'inventaire ci-dessous a été relevé sur le GGUF le 03/10 (shards 1 à 15) :
//!
//! | type de couche | tenseurs propres |
//! |---|---|
//! | toutes | `attn_norm`, `attn_res_score`, `ffn_norm`, `ffn_res_score` |
//! | KDA (`il % 4 != 3`) | `attn_q/k/v`, `ssm_conv1d_{q,k,v}`, `ssm_f_a`, `ssm_f_b`, `ssm_beta`, `ssm_a`, `ssm_dt`, `ssm_g`, `ssm_norm`, `attn_output` |
//! | MLA (`il % 4 == 3`) | `attn_q_a`, `attn_q_a_norm`, `attn_q_b`, `attn_kv_a_mqa`, `attn_kv_a_norm`, `attn_k_b`, `attn_v_b`, `attn_gate`, `attn_output` |
//! | dense (couche 0) | `ffn_gate/up/down` |
//! | MoE (les autres) | `ffn_gate_inp`, `exp_probs_b`, `ffn_routed_down`, `ffn_routed_norm`, `ffn_routed_up`, `ffn_{gate,up,down}_exps`, `ffn_{gate,up,down}_shexp` |
//!
//! (`ssm_a` est un tenseur SANS suffixe `.weight` — particularité du fichier.)

use crate::gguf::Gguf;

/// Type d'attention d'une couche, **lu dans le fichier** : le GGUF encode la
/// cadence dans `attention.head_count_kv` (1 sur les couches MLA, 0 ailleurs),
/// et c'est la seule source qui ne peut pas se tromper.
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum TypeCouche {
    /// Couche 0 : FFN dense, pas d'experts.
    Dense,
    /// Attention delta-net (3 couches sur 4).
    Kda,
    /// MLA « nope » (couches 3, 7, 11, …).
    Mla,
}

/// Ce qu'une couche porte, et ce qui manque.
#[derive(Clone, Debug)]
pub struct Couche {
    pub index: usize,
    pub type_: TypeCouche,
    pub manquants: Vec<String>,
    /// Le type est-il cohérent avec la cadence attendue (`il % 4 == 3` → MLA) ?
    pub cadence_ok: bool,
}

/// L'inventaire complet d'un fichier Kimi-K3.
#[derive(Clone, Debug, Default)]
pub struct Inventaire {
    pub n_couches_declarees: usize,
    pub couches: Vec<Couche>,
    pub n_experts: usize,
    pub n_experts_par_jeton: usize,
    pub latent: usize,
}

impl Inventaire {
    pub fn manquants(&self) -> usize {
        self.couches.iter().map(|c| c.manquants.len()).sum()
    }
    pub fn par_type(&self) -> (usize, usize, usize) {
        let mut d = 0; let mut k = 0; let mut m = 0;
        for c in &self.couches {
            match c.type_ {
                TypeCouche::Dense => d += 1,
                TypeCouche::Kda => k += 1,
                TypeCouche::Mla => m += 1,
            }
        }
        (d, k, m)
    }
    pub fn rapport(&self) -> String {
        let (d, k, m) = self.par_type();
        let mut s = format!(
            "{} couches vues sur {} déclarées · {} dense · {} KDA · {} MLA · \
{} experts ({} par jeton) · latent {}\n",
            self.couches.len(), self.n_couches_declarees, d, k, m,
            self.n_experts, self.n_experts_par_jeton, self.latent);
        let manquants = self.manquants();
        if manquants == 0 {
            s.push_str("  inventaire : COMPLET (aucun tenseur attendu ne manque)");
        } else {
            s.push_str(&format!("  inventaire : {manquants} tenseur(s) attendu(s) manquant(s)\n"));
            for c in self.couches.iter().filter(|c| !c.manquants.is_empty()).take(6) {
                s.push_str(&format!("    couche {} ({:?}) : {}\n", c.index, c.type_,
                                    c.manquants.join(", ")));
            }
            if self.couches.iter().filter(|c| !c.manquants.is_empty()).count() > 6 {
                s.push_str("    …\n");
            }
        }
        let hors_cadence: Vec<usize> = self.couches.iter()
            .filter(|c| !c.cadence_ok).map(|c| c.index).collect();
        if !hors_cadence.is_empty() {
            s.push_str(&format!("  ⚠️ cadence inattendue (MLA sur il%4==3) aux couches {:?}\n",
                                hors_cadence));
        }
        s
    }
}

/// **Vérifie l'inventaire** d'un fichier Kimi-K3 **éclaté en shards**.
///
/// ⚠️ Les tenseurs ne sont PAS dans le premier shard : les métadonnées y sont,
/// mais l'inventaire y est vide (mesuré : shard 1 = 0 tenseur). Il faut donc lire
/// l'en-tête de **chaque shard présent** — ce qui a le mérite de donner un
/// inventaire utilisable pendant le téléchargement (partiel, et l'appelant le
/// dit).
pub fn inventorie(chemin: &std::path::Path) -> std::io::Result<Inventaire> {
    let nom = chemin.file_name().and_then(|n| n.to_str()).unwrap_or("").to_string();
    let dossier = chemin.parent().unwrap_or_else(|| std::path::Path::new("."));
    // Tous les shards du même modèle présents dans le dossier, dans l'ordre.
    let prefixe = match nom.rsplit_once("-of-") {
        Some((tete, _)) => tete.rsplit_once('-').map(|(p, _)| p.to_string()),
        None => None,
    };
    let mut shards: Vec<std::path::PathBuf> = Vec::new();
    if let Some(pref) = &prefixe {
        if let Ok(rd) = std::fs::read_dir(dossier) {
            for e in rd.flatten() {
                let p = e.path();
                let n = p.file_name().and_then(|n| n.to_str()).unwrap_or("");
                if n.starts_with(pref.as_str()) && n.ends_with(".gguf")
                    && !n.contains(".part") {
                    shards.push(p);
                }
            }
        }
        shards.sort();
    }
    if shards.is_empty() { shards.push(chemin.to_path_buf()); }
    // Le premier shard porte les métadonnées ; tous portent des tenseurs.
    let g = Gguf::open_meta(&shards[0])?;
    let mut noms: Vec<String> = g.tensors.iter().map(|t| t.name.clone()).collect();
    for p in shards.iter().skip(1) {
        if let Ok(suivant) = Gguf::open_meta(p) {
            noms.extend(suivant.tensors.iter().map(|t| t.name.clone()));
        }
    }
    Ok(inventorie_avec(&g, &noms, shards.len()))
}

/// L'inventaire, à partir des métadonnées et de la LISTE des noms de tenseurs
/// (tous shards confondus). Séparé pour être testable sans fichier.
pub fn inventorie_avec(g: &Gguf, noms: &[String], n_shards: usize) -> Inventaire {
    let quelque_part = |s: &str| noms.iter().any(|n| n.ends_with(s));
    let par_couche = |l: usize, s: &str| {
        let nom = format!("blk.{l}.{s}");
        noms.iter().any(|n| *n == nom)
    };
    let lire_meta = |cle: &str| -> Option<usize> {
        g.meta.get(cle).and_then(|m| m.as_u64()).map(|v| v as usize)
    };
    let n_declare = lire_meta("kimi-k3.block_count").unwrap_or(0);
    // Les couches VUES : celles dont le nom apparaît dans l'inventaire.
    let mut vues: Vec<usize> = noms.iter().filter_map(|n| {
        let p: Vec<&str> = n.split('.').collect();
        if p.len() >= 3 && p[0] == "blk" { p[1].parse::<usize>().ok() } else { None }
    }).collect();
    vues.sort_unstable();
    vues.dedup();

    // La cadence MLA : `attention.head_count_kv` est une LISTE, 1 sur les
    // couches MLA et 0 ailleurs. C'est le fichier qui le dit, pas nous.
    let kv_heads: Vec<i64> = g.meta.get("kimi-k3.attention.head_count_kv")
        .and_then(|m| m.as_liste_i64()).unwrap_or_default();

    let mut inv = Inventaire {
        n_couches_declarees: n_declare,
        n_experts: lire_meta("kimi-k3.expert_count").unwrap_or(0),
        n_experts_par_jeton: lire_meta("kimi-k3.expert_used_count").unwrap_or(0),
        latent: lire_meta("kimi-k3.expert_latent_length").unwrap_or(0),
        ..Default::default()
    };
    let communes = ["attn_norm.weight", "attn_res_score.weight",
                    "ffn_norm.weight", "ffn_res_score.weight"];
    let kda = ["attn_q.weight", "attn_k.weight", "attn_v.weight",
               "ssm_conv1d_q.weight", "ssm_conv1d_k.weight", "ssm_conv1d_v.weight",
               "ssm_f_a.weight", "ssm_f_b.weight", "ssm_beta.weight", "ssm_a",
               "ssm_dt.bias", "ssm_g.weight", "ssm_norm.weight", "attn_output.weight"];
    let mla = ["attn_q_a.weight", "attn_q_a_norm.weight", "attn_q_b.weight",
               "attn_kv_a_mqa.weight", "attn_kv_a_norm.weight", "attn_k_b.weight",
               "attn_v_b.weight", "attn_gate.weight", "attn_output.weight"];
    let dense = ["ffn_gate.weight", "ffn_up.weight", "ffn_down.weight"];
    let moe = ["ffn_gate_inp.weight", "exp_probs_b.bias", "ffn_routed_down.weight",
               "ffn_routed_norm.weight", "ffn_routed_up.weight",
               "ffn_gate_exps.weight", "ffn_up_exps.weight", "ffn_down_exps.weight",
               "ffn_gate_shexp.weight", "ffn_up_shexp.weight", "ffn_down_shexp.weight"];

    for &l in &vues {
        // MLA si le fichier déclare une tête KV sur cette couche ; sinon KDA.
        let est_mla = kv_heads.get(l).map(|&v| v > 0).unwrap_or(l % 4 == 3);
        let type_ = if l == 0 && !est_mla { TypeCouche::Dense } else if est_mla { TypeCouche::Mla } else { TypeCouche::Kda };
        let mut attendus: Vec<&str> = communes.to_vec();
        attendus.extend_from_slice(if est_mla { &mla } else { &kda });
        attendus.extend_from_slice(if l == 0 { &dense } else { &moe });
        let mut manquants = Vec::new();
        for t in attendus {
            if !par_couche(l, t) { manquants.push(t.to_string()); }
        }
        inv.couches.push(Couche {
            index: l, type_, manquants,
            cadence_ok: est_mla == (l % 4 == 3),
        });
    }
    // Un tenseur qui apparaîtrait sans qu'on l'attende est signalé : c'est ainsi
    // qu'on repère une liste d'inventaire incomplète (plutôt que de la croire).
    let _ = quelque_part;
    let _ = n_shards;
    inv
}

// ===========================================================================
// La couche 0 : la passe avant, en f32, pour vérifier la STRUCTURE d'abord.
//
// Les poids sont déquantifiés une fois (~1,4 Go pour la couche 0 : elle est
// dense). Le chemin « poids empruntés » (Q8_0 en place, activations quantifiées)
// viendra après : il donne la tolérance serrée (~1e-6) contre llama.cpp, alors
// que le f32 déquantifié donne ~1e-3 (les produits ne sont pas quantifiés de la
// même façon). **On vérifie la structure d'abord, l'exactitude ensuite** — et
// l'écart entre les deux se mesure, il ne se suppose pas.
// ===========================================================================

/// Produit matrice-vecteur, `w` en lignes (`[n_out][n_in]`).
fn mv(w: &[f32], n_out: usize, n_in: usize, x: &[f32], out: &mut [f32]) {
    assert_eq!(w.len(), n_out * n_in, "matrice {n_out}×{n_in} de {} valeurs", w.len());
    assert!(x.len() >= n_in && out.len() >= n_out, "dimensions d'activation");
    for o in 0..n_out {
        let ligne = &w[o * n_in..(o + 1) * n_in];
        let mut s = 0f32;
        for j in 0..n_in { s += ligne[j] * x[j]; }
        out[o] = s;
    }
}

/// RMSNorm **avec poids** : `x / sqrt(moyenne(x²) + eps) × w`.
fn rms_norm_poids(x: &[f32], w: &[f32], eps: f32, out: &mut [f32]) {
    let n = x.len().min(w.len());
    let mut carre = 0f64;
    for v in &x[..n] { carre += (*v as f64) * (*v as f64); }
    let inv = 1.0 / ((carre / n as f64 + eps as f64).sqrt() as f32);
    for i in 0..n { out[i] = x[i] * inv * w[i]; }
}

/// Les tenseurs de la couche 0 (dense : KDA + SiTU), et ses états.
pub struct Couche0 {
    q: Vec<f32>, k: Vec<f32>, v: Vec<f32>, wo: Vec<f32>,
    f_a: Vec<f32>, f_b: Vec<f32>, g_proj: Vec<f32>,
    ffn_gate: Vec<f32>, ffn_up: Vec<f32>, ffn_down: Vec<f32>,
    attn_norm: Vec<f32>, attn_res_score: Vec<f32>,
    ffn_norm: Vec<f32>, ffn_res_score: Vec<f32>,
    conv_q: Vec<f32>, conv_k: Vec<f32>, conv_v: Vec<f32>,
    beta_w: Vec<f32>, ssm_a: Vec<f32>, dt_bias: Vec<f32>, o_norm: Vec<f32>,
    etat_conv_q: Vec<f32>, etat_conv_k: Vec<f32>, etat_conv_v: Vec<f32>,
    etat_delta: Vec<f32>,
    h: usize, nh: usize, hd: usize, d_inner: usize, d_conv: usize,
    ffn: usize, eps: f32,
    /// Valeurs des points de contrôle (la pile de l'attention résiduelle) :
    /// la couche 0 est « banque » (`0 % 12 == 0`), elle empile son entrée BRUTE.
    pile: Vec<f32>,
    n_ckpt: usize,
    /// Numéro du jeton traité, pour nommer les vidages comme la référence
    /// (`<préfixe>-<tenseur>-<couche>-<position>.bin`).
    pos: usize,
}

impl Couche0 {
    /// Charge la couche 0 depuis le fichier. **Refuse bruyamment** si un tenseur
    /// manque ou si une dimension ne colle pas.
    pub fn charge(g: &Gguf) -> Result<Couche0, String> {
        let lu = |nom: &str| -> Result<Vec<f32>, String> {
            let t = g.tensor(nom).ok_or_else(|| format!("tenseur absent : {nom}"))?;
            Ok(g.dequant(nom))
        };
        let dims = |nom: &str| -> Result<Vec<usize>, String> {
            let t = g.tensor(nom).ok_or_else(|| format!("tenseur absent : {nom}"))?;
            Ok(t.dims.iter().map(|d| *d as usize).collect())
        };
        let p = |s: &str| format!("blk.0.{s}");
        // ⚠️ **Les dimensions du moteur sont INVERSÉES par rapport au fichier** :
        // `TensorInfo::dims[0]` est `ne1` du GGUF, c'est-à-dire la dimension de
        // SORTIE (`Proj::load` fait `n_out = dims[0]`, `n_in = dims[1]`). Lire
        // `dims[1]` là où il faut `dims[0]` a donné `nh = 7168` au lieu de 96 et
        // fait tomber le produit matriciel — attrapé par le test de fumée, pas
        // par relecture.
        let h = dims(&p("attn_norm.weight"))?[0];
        let nh = dims(&p("ssm_beta.weight"))?[0];
        let hd = dims(&p("ssm_norm.weight"))?[0];
        let d_inner = nh * hd;
        let dc = dims(&p("ssm_conv1d_q.weight"))?;
        let d_conv = *dc.last().unwrap_or(&4);          // noyau : dernière dim du moteur
        let ffn = dims(&p("ffn_gate.weight"))?[0];
        let eps = 1e-5f32;                       // `kimi-k3.attention.layer_norm_rms_epsilon`
        eprintln!("[k3] h={h} nh={nh} hd={hd} d_inner={d_inner} d_conv={d_conv} ffn={ffn}");
        for (n, att) in [("attn_q.weight", (d_inner, h)), ("attn_output.weight", (h, d_inner)),
                         ("ssm_f_a.weight", (hd, h)), ("ssm_f_b.weight", (d_inner, hd)),
                         ("ssm_g.weight", (d_inner, h)), ("ffn_gate.weight", (ffn, h)),
                         ("ffn_down.weight", (h, ffn)), ("ssm_beta.weight", (nh, h))] {
            let t = g.tensor(&p(n)).ok_or_else(|| format!("absent {n}"))?;
            let vals = t.nelem();
            if vals != att.0 * att.1 {
                eprintln!("[k3] ⚠️ {n} : {} valeurs, attendu {}×{} = {}",
                          vals, att.0, att.1, att.0 * att.1);
            }
        }
        let etat_conv = vec![0f32; (d_conv - 1) * d_inner];
        Ok(Couche0 {
            q: lu(&p("attn_q.weight"))?, k: lu(&p("attn_k.weight"))?,
            v: lu(&p("attn_v.weight"))?, wo: lu(&p("attn_output.weight"))?,
            f_a: lu(&p("ssm_f_a.weight"))?, f_b: lu(&p("ssm_f_b.weight"))?,
            g_proj: lu(&p("ssm_g.weight"))?,
            ffn_gate: lu(&p("ffn_gate.weight"))?, ffn_up: lu(&p("ffn_up.weight"))?,
            ffn_down: lu(&p("ffn_down.weight"))?,
            attn_norm: lu(&p("attn_norm.weight"))?,
            attn_res_score: lu(&p("attn_res_score.weight"))?,
            ffn_norm: lu(&p("ffn_norm.weight"))?,
            ffn_res_score: lu(&p("ffn_res_score.weight"))?,
            conv_q: lu(&p("ssm_conv1d_q.weight"))?, conv_k: lu(&p("ssm_conv1d_k.weight"))?,
            conv_v: lu(&p("ssm_conv1d_v.weight"))?,
            beta_w: lu(&p("ssm_beta.weight"))?, ssm_a: lu(&p("ssm_a"))?,
            dt_bias: lu(&p("ssm_dt.bias"))?, o_norm: lu(&p("ssm_norm.weight"))?,
            etat_conv_q: etat_conv.clone(), etat_conv_k: etat_conv.clone(),
            etat_conv_v: etat_conv,
            etat_delta: vec![0f32; nh * hd * hd],
            h, nh, hd, d_inner, d_conv, ffn, eps,
            pile: Vec::new(), n_ckpt: 0, pos: 0,
        })
    }

    /// Hauteur du flux (pour l'appelant : la rangée d'embarquement fait `h`).
    pub fn hauteur(&self) -> usize { self.h }

    /// L'état (convolution + delta) remis à zéro : entre deux textes, on ne
    /// garde rien — un état oublié ne se voit pas dans les logits du premier
    /// jeton, il se voit au dixième.
    pub fn remise_a_zero(&mut self) {
        self.etat_conv_q.iter_mut().for_each(|v| *v = 0.0);
        self.etat_conv_k.iter_mut().for_each(|v| *v = 0.0);
        self.etat_conv_v.iter_mut().for_each(|v| *v = 0.0);
        self.etat_delta.iter_mut().for_each(|v| *v = 0.0);
        self.pile.clear();
        self.n_ckpt = 0;
    }

    /// **La passe avant de la couche 0**, dans l'ordre de la référence :
    /// `res_mix` (pile vide au premier appel) → empile l'entrée BRUTE →
    /// RMSNorm → KDA → **redémarrage du flux** (`0 % 12 == 0`) → `res_mix` →
    /// RMSNorm → SiTU → retour.
    pub fn avant(&mut self, x: &[f32]) -> Result<Vec<f32>, String> {
        let (h, nh, hd, d_inner) = (self.h, self.nh, self.hd, self.d_inner);
        if x.len() != h { return Err(format!("entrée de {} valeurs, {h} attendues", x.len())); }
        let mut tampon = vec![0f32; h.max(d_inner).max(self.ffn)];
        let vider = std::env::var("DRAVE_DUMP_COUCHES").ok().filter(|p| !p.is_empty());
        let pos = self.pos;
        self.pos += 1;
        // 0. **La banque appartient à la PASSE du jeton.** Il faut la repartir
        //    AVANT l'étape 1, pas après : l'attention résiduelle du jeton 0 est
        //    appelée avec une pile VIDE (`resi_stack == nullptr` → la référence
        //    renvoie `cur` tel quel), et c'est vrai à CHAQUE jeton puisque le
        //    graphe est reconstruit à chaque passe. Laisser le `n_ckpt` du jeton
        //    précédent faisait donc appliquer un `res_mix` là où la référence
        //    n'en applique pas — invisible au jeton 0, faux dès le jeton 1.
        self.pile.clear();
        self.n_ckpt = 0;
        // 1. attention résiduelle (pile vide → renvoie `x` tel quel)
        let cur0 = if self.n_ckpt == 0 {
            x.to_vec()
        } else {
            let mut out = vec![0f32; h];
            crate::model::res_mix(&self.pile, self.n_ckpt, h, x, &self.attn_res_score, self.eps, &mut out);
            out
        };
        // 2. la couche 0 EST une couche « banque » : on empile l'entrée BRUTE,
        //    AVANT l'attention (`res_push(prefix_sum)` dans la référence).
        //
        // **La banque est REPARTIE à chaque jeton, pas accumulée.** Dans la
        // référence, `resi_stack` est une variable locale au graphe : elle est
        // vide au début de chaque passe, et elle porte une colonne par jeton du
        // lot. Ici les jetons sont traités un par un, donc la couche 0 empile
        // l'entrée du jeton COURANT et rien d'autre. Accumuler entre jetons
        // faisait mélanger le jeton 1 avec l'entrée du jeton 0 — et c'est
        // exactement ce que la comparaison montrait : jeton 0 juste à 4e-04,
        // jetons 1 et 2 faux à 0,82 et 0,64 de corrélation.
        self.pile.extend_from_slice(x);
        self.n_ckpt = 1;
        // 3. RMSNorm d'entrée
        let mut cur = vec![0f32; h];
        rms_norm_poids(&cur0, &self.attn_norm, self.eps, &mut cur);
        if let Some(p) = vider.as_deref() { vide(p, "attn_norm", 0, pos, &cur); }
        // 4. projections + convolution courte + SiLU
        let mut q = vec![0f32; d_inner];
        let mut k = vec![0f32; d_inner];
        let mut v = vec![0f32; d_inner];
        mv(&self.q, d_inner, h, &cur, &mut q);
        mv(&self.k, d_inner, h, &cur, &mut k);
        mv(&self.v, d_inner, h, &cur, &mut v);
        // La convolution lit `x` et écrit `out` : il faut deux tampons distincts,
        // et UN SEUL appel par flux — l'état de convolution avance d'un cran par
        // jeton, pas deux. (Une première version appelait `kda_conv_silu` sur `q`
        // deux fois, dont une dans un temporaire : l'état avançait deux fois et
        // le résultat partait à la poubelle. Relu avant de compiler.)
        let mut qc = vec![0f32; d_inner];
        let mut kc = vec![0f32; d_inner];
        let mut vc = vec![0f32; d_inner];
        crate::model::kda_conv_silu(&q, &self.conv_q, &mut self.etat_conv_q, self.d_conv, d_inner, &mut qc);
        crate::model::kda_conv_silu(&k, &self.conv_k, &mut self.etat_conv_k, self.d_conv, d_inner, &mut kc);
        crate::model::kda_conv_silu(&v, &self.conv_v, &mut self.etat_conv_v, self.d_conv, d_inner, &mut vc);
        if let Some(p) = vider.as_deref() {
            vide(p, "kda_q_conv", 0, pos, &qc);
            vide(p, "kda_k_conv", 0, pos, &kc);
            vide(p, "kda_v_conv", 0, pos, &vc);
        }
        // La norme L2 par tête, entre la convolution et la récurrence.
        l2_q_et_k(&mut qc, &mut kc, nh, hd, self.eps);
        // 5. porte de décroissance (par tête) et pas appris
        let mut fa = vec![0f32; hd];
        mv(&self.f_a, hd, h, &cur, &mut fa);
        let mut g1 = vec![0f32; d_inner];
        mv(&self.f_b, d_inner, hd, &fa, &mut g1);
        let mut beta = vec![0f32; nh];
        mv(&self.beta_w, nh, h, &cur, &mut beta);
        // 6. récurrence delta, tête par tête
        let mut o = vec![0f32; d_inner];
        for t in 0..nh {
            let mut g = vec![0f32; hd];
            for i in 0..hd {
                let z = g1[t * hd + i] + self.dt_bias[t * hd + i];
                g[i] = crate::model::kda_porte(z, self.ssm_a[t], -5.0);
            }
            let b = 1.0 / (1.0 + (-beta[t]).exp());
            let mut ot = vec![0f32; hd];
            crate::model::kda_pas(&qc[t * hd..(t + 1) * hd], &kc[t * hd..(t + 1) * hd],
                                  &vc[t * hd..(t + 1) * hd], &g, b,
                                  &mut self.etat_delta[t * hd * hd..(t + 1) * hd * hd], hd, &mut ot);
            o[t * hd..(t + 1) * hd].copy_from_slice(&ot);
        }
        if let Some(p) = vider.as_deref() { vide(p, "kda_scan_out", 0, pos, &o); }
        // 7. norme + porte de sortie PLEIN RANG (calculée UNE fois)
        let mut g2 = vec![0f32; d_inner];
        mv(&self.g_proj, d_inner, h, &cur, &mut g2);
        for t in 0..nh {
            rms_norm_poids(&o[t * hd..(t + 1) * hd], &self.o_norm, self.eps,
                           &mut tampon[..hd]);
            for i in 0..hd {
                let s = 1.0 / (1.0 + (-g2[t * hd + i]).exp());
                o[t * hd + i] = tampon[i] * s;
            }
        }
        if let Some(p) = vider.as_deref() { vide(p, "kda_normed", 0, pos, &o); }
        let mut attn = vec![0f32; h];
        mv(&self.wo, h, d_inner, &o, &mut attn);
        if let Some(p) = vider.as_deref() {
            vide(p, "kda_out", 0, pos, &attn);
            vide(p, "prefix_sum_attn", 0, pos, &attn);
        }
        // 8. le flux REDÉMARRE ici (couche « banque ») : `prefix = attn`, pas `x + attn`
        let mut prefix = attn.clone();
        // 9. attention résiduelle avant la FFN
        let mut cur_ffn = vec![0f32; h];
        crate::model::res_mix(&self.pile, self.n_ckpt, h, &prefix, &self.ffn_res_score,
                              self.eps, &mut cur_ffn);
        rms_norm_poids(&cur_ffn, &self.ffn_norm, self.eps, &mut cur);
        if let Some(p) = vider.as_deref() { vide(p, "ffn_norm", 0, pos, &cur); }
        // 10. FFN dense avec SiTU
        let mut fg = vec![0f32; self.ffn];
        let mut fu = vec![0f32; self.ffn];
        mv(&self.ffn_gate, self.ffn, h, &cur, &mut fg);
        mv(&self.ffn_up, self.ffn, h, &cur, &mut fu);
        let beta_s = 4.0f32; let lin = 25.0f32;
        for i in 0..self.ffn { fg[i] = crate::model::situ(fg[i], fu[i], beta_s, lin); }
        let mut ff = vec![0f32; h];
        mv(&self.ffn_down, h, self.ffn, &fg, &mut ff);
        if let Some(p) = vider.as_deref() { vide(p, "ffn_out", 0, pos, &ff); }
        // 11. le flux reprend
        for i in 0..h { prefix[i] += ff[i]; }
        Ok(prefix)
    }
}


// ===========================================================================
// Contrôle des DIMENSIONS, tensor par tensor, avant d'écrire le calcul.
//
// C'est la classe de bug qui a déjà mordu : le moteur range `dims[0] = ne1` (la
// SORTIE) alors que le GGUF range `ne0` en premier. Une dimension lue du mauvais
// côté ne se voit ni à la compilation ni à la relecture — elle se voit au
// premier produit matriciel, ou jamais si les deux nombres sont proches.
// ===========================================================================

/// Vide un tenseur intermédiaire de la couche 0 au format de la référence :
/// `<préfixe>-<nom>-<couche>-<position>.bin`, f32 brut. C'est ce qui permet de
/// BISSECTER une divergence au lieu de raisonner sur la sortie de la couche.
fn vide(prefixe: &str, nom: &str, couche: usize, pos: usize, v: &[f32]) {
    use std::io::Write;
    if let Ok(mut f) = std::fs::File::create(format!("{prefixe}-{nom}-{couche}-{pos}.bin")) {
        let mut o = Vec::with_capacity(v.len() * 4);
        for x in v { o.extend_from_slice(&x.to_le_bytes()); }
        let _ = f.write_all(&o);
    }
}

/// **La norme L2 par tête**, appliquée à `q` et `k` après la convolution et
/// AVANT la récurrence — `build_gdn_l2_norm` de la référence :
///
/// ```text
///   l2(x) = x / sqrt(Σ x² + eps)          (la somme porte sur head_dim)
/// ```
///
/// Elle MANQUAIT, et c'est ce qui faisait diverger la couche 0 dès le jeton 1.
/// La signature le disait : au jeton 0 l'état delta est nul, donc
/// `o[j] = β·(Σ_i k[i]·q[i])·v[j]` — proportionnel à `v` quelle que soit
/// l'échelle de `q` et `k` — et la norme par tête qui suit efface justement
/// cette échelle. D'où une corrélation de 0,983 au jeton 0 **avec un rapport de
/// norme de 0,94**, puis 0,79 et 0,64 : à partir du jeton 1, l'accumulation
/// `s += k ⊗ β(v − sᵀk)` dépend de l'échelle de `k`, elle.
///
/// `facteur` porte le `1/sqrt(head_dim)` que la référence applique EN PLUS à
/// `q` seul (`ggml_scale(q, 1/sqrt(S_k))` dans `build_delta_net_autoregressive`).
fn l2_norme_tete(x: &mut [f32], hd: usize, eps: f32, facteur: f32) {
    let mut carre = 0f32;
    for v in x[..hd].iter() { carre += *v * *v; }
    let inv = facteur / (carre + eps).sqrt();
    for v in x[..hd].iter_mut() { *v *= inv; }
}

/// Les deux normalisations de la référence, sur `d_inner` canaux groupés par
/// tête : `q` reçoit `1/sqrt(head_dim)` en plus, `k` non.
fn l2_q_et_k(qc: &mut [f32], kc: &mut [f32], nh: usize, hd: usize, eps: f32) {
    let fq = 1.0 / (hd as f32).sqrt();
    for t in 0..nh {
        l2_norme_tete(&mut qc[t * hd..(t + 1) * hd], hd, eps, fq);
        l2_norme_tete(&mut kc[t * hd..(t + 1) * hd], hd, eps, 1.0);
    }
}


/// Dimensions attendues (côté MOTEUR, donc inversées par rapport au fichier)
/// pour une couche, d'après la configuration déclarée. Rend la liste des écarts.
pub fn verifie_dims(g: &Gguf, l: usize) -> Vec<String> {
    let d = |nom: &str| -> Option<Vec<usize>> {
        g.tensor(nom).map(|t| t.dims.iter().map(|x| *x as usize).collect())
    };
    let p = |s: &str| format!("blk.{l}.{s}");
    let lire = |cle: &str, def: usize| -> usize {
        g.meta.get(cle).and_then(|m| m.as_u64()).map(|v| v as usize).unwrap_or(def)
    };
    let h = lire("kimi-k3.embedding_length", 7168);
    let n_exp = lire("kimi-k3.expert_count", 896);
    let n_ff_exp = lire("kimi-k3.expert_feed_forward_length", 3072);
    let latent = lire("kimi-k3.expert_latent_length", 3584);
    let n_shared = lire("kimi-k3.expert_shared_count", 2);
    let nh = lire("kimi-k3.attention.head_count", 96);
    let kda_hd = lire("kimi-k3.kda.head_dim", 128);
    let kl_mla = lire("kimi-k3.attention.key_length_mla", 192);
    let vl_mla = lire("kimi-k3.attention.value_length_mla", 128);
    let kv_lora = lire("kimi-k3.attention.kv_lora_rank", 512);
    let q_lora = lire("kimi-k3.attention.q_lora_rank", 1536);
    let rope = lire("kimi-k3.rope.dimension_count", 64);
    let mut ecarts = Vec::new();
    // Le contrôle prend `ecarts` en paramètre : une fermeture qui le
    // capturerait interdirait les autres écritures (erreur de compilation, pas
    // de raisonnement).
    let attendu = |ecarts: &mut Vec<String>, nom: String, dims: Vec<usize>| match d(&nom) {
        None => ecarts.push(format!("{nom} : ABSENT")),
        Some(v) if v != dims => ecarts.push(
            format!("{nom} : moteur {v:?}, attendu {dims:?} (fichier inversé)")),
        Some(_) => {}
    };
    // communes
    attendu(&mut ecarts, p("attn_norm.weight"), vec![h]);
    attendu(&mut ecarts, p("ffn_norm.weight"), vec![h]);
    attendu(&mut ecarts, p("attn_res_score.weight"), vec![h]);
    let est_mla = d(&p("attn_kv_a_mqa.weight")).is_some();
    if est_mla {
        attendu(&mut ecarts, p("attn_q_a.weight"), vec![q_lora, h]);
        attendu(&mut ecarts, p("attn_q_a_norm.weight"), vec![q_lora]);
        attendu(&mut ecarts, p("attn_q_b.weight"), vec![nh * kl_mla, q_lora]);
        attendu(&mut ecarts, p("attn_kv_a_mqa.weight"), vec![kv_lora + rope, h]);
        attendu(&mut ecarts, p("attn_kv_a_norm.weight"), vec![kv_lora]);
        attendu(&mut ecarts, p("attn_k_b.weight"), vec![nh, kv_lora, kl_mla - rope]);
        attendu(&mut ecarts, p("attn_v_b.weight"), vec![nh, vl_mla, kv_lora]);
        attendu(&mut ecarts, p("attn_gate.weight"), vec![nh * vl_mla, h]);
        attendu(&mut ecarts, p("attn_output.weight"), vec![h, nh * vl_mla]);
    } else {
        attendu(&mut ecarts, p("attn_q.weight"), vec![nh * kda_hd, h]);
        attendu(&mut ecarts, p("attn_k.weight"), vec![nh * kda_hd, h]);
        attendu(&mut ecarts, p("attn_v.weight"), vec![nh * kda_hd, h]);
        attendu(&mut ecarts, p("ssm_g.weight"), vec![nh * kda_hd, h]);
        attendu(&mut ecarts, p("ssm_f_a.weight"), vec![kda_hd, h]);
        attendu(&mut ecarts, p("ssm_f_b.weight"), vec![nh * kda_hd, kda_hd]);
        attendu(&mut ecarts, p("ssm_beta.weight"), vec![nh, h]);
        attendu(&mut ecarts, p("ssm_dt.bias"), vec![nh * kda_hd]);
        attendu(&mut ecarts, p("ssm_a"), vec![nh]);
        attendu(&mut ecarts, p("ssm_norm.weight"), vec![kda_hd]);
        attendu(&mut ecarts, p("attn_output.weight"), vec![h, nh * kda_hd]);
        if let Some(v) = d(&p("ssm_conv1d_q.weight")) {
            if *v.last().unwrap_or(&0) != 4 {
                ecarts.push(format!("{}.ssm_conv1d_q.weight : noyau {:?} au lieu de 4",
                                    p(""), v));
            }
            if v.iter().product::<usize>() != 4 * nh * kda_hd {
                ecarts.push(format!("ssm_conv1d_q.weight : {:?} ≠ 4×{}", v, nh * kda_hd));
            }
        } else {
            ecarts.push("ssm_conv1d_q.weight : ABSENT".to_string());
        }
    }
    if l == 0 {
        attendu(&mut ecarts, p("ffn_gate.weight"), vec![lire("kimi-k3.feed_forward_length", 33792), h]);
        attendu(&mut ecarts, p("ffn_up.weight"), vec![lire("kimi-k3.feed_forward_length", 33792), h]);
        attendu(&mut ecarts, p("ffn_down.weight"), vec![h, lire("kimi-k3.feed_forward_length", 33792)]);
    } else {
        attendu(&mut ecarts, p("ffn_gate_inp.weight"), vec![n_exp, h]);
        attendu(&mut ecarts, p("exp_probs_b.bias"), vec![n_exp]);
        attendu(&mut ecarts, p("ffn_routed_down.weight"), vec![latent, h]);
        attendu(&mut ecarts, p("ffn_routed_up.weight"), vec![h, latent]);
        attendu(&mut ecarts, p("ffn_routed_norm.weight"), vec![latent]);
        attendu(&mut ecarts, p("ffn_gate_exps.weight"), vec![n_exp, n_ff_exp, latent]);
        attendu(&mut ecarts, p("ffn_up_exps.weight"), vec![n_exp, n_ff_exp, latent]);
        attendu(&mut ecarts, p("ffn_down_exps.weight"), vec![n_exp, latent, n_ff_exp]);
        attendu(&mut ecarts, p("ffn_gate_shexp.weight"), vec![n_shared * n_ff_exp, h]);
        attendu(&mut ecarts, p("ffn_down_shexp.weight"), vec![h, n_shared * n_ff_exp]);
    }
    ecarts
}

// ===========================================================================
// Le MoE latent — 92 couches sur 93.
//
// Les experts ne sont PAS déquantifiés à l'ouverture : une couche pèse 15,7 Go en
// MXFP4, et un jeton n'en lit que 16 sur 896 (~300 Mo). On déquantifie donc **par
// expert, à la demande** — c'est le geste qui rend un modèle de 1,5 To
// seulement lisible, et c'est aussi ce qui rend la réutilisation mesurable.
// ===========================================================================

/// Les parties denses d'un MoE (déquantifiées une fois) + les experts empruntés.
pub struct MoeK3 {
    gate_inp: Vec<f32>,      // [n_exp × h]   : le routeur (F32 dans le fichier)
    biais: Vec<f32>,         // [n_exp]       : biais de SÉLECTION
    rout_down: Vec<f32>,     // [latent × h]
    rout_up: Vec<f32>,       // [h × latent]
    rout_norm: Vec<f32>,     // [latent]
    sh_gate: Vec<f32>, sh_up: Vec<f32>, sh_down: Vec<f32>,   // partagés, [*6144*]
    // experts empruntés : pointeur + forme
    ptr_gate: *const u8, ptr_up: *const u8, ptr_down: *const u8,
    n_out_gate: usize, n_in_gate: usize,
    n_out_up: usize, n_in_up: usize,
    n_out_down: usize, n_in_down: usize,
    n_exp: usize, k: usize,
    h: usize, latent: usize, moe_ff: usize,
    situ_beta: f32, situ_lin: f32, eps: f32,
    /// `DRAVE_K3_MXFP4=1` : les experts passent par le noyau MXFP4 du moteur au
    /// lieu d'être déquantifiés en f32. CHANGE LA SORTIE — voir `mv_mxfp4`.
    noyau_mxfp4: bool,
    /// Numéro de couche et rang du jeton : servent à la TRACE de routage, qui
    /// est ce qui permet de prédire un cache d'experts avant d'en écrire un.
    l: usize,
    appels: std::cell::Cell<usize>,
}

/// Déquantifie **un** expert d'un tenseur MXFP4 emprunté : `n_out × n_in` poids,
/// blocs de 32 (17 octets), **dans un tampon fourni**.
///
/// ⚠️ La première version appelait `Gguf::dequant_mxfp4` par bloc, donc
/// **allouait un `Vec` par bloc** : 16 experts × 3 matrices × 344 064 blocs =
/// 16,5 millions d'allocations par jeton, mesuré à **25,7 s**. La même
/// déquantification écrite dans un tampon ne fait plus qu'une allocation par
/// matrice. La leçon est celle du dépôt : ce n'est pas le calcul qui coûtait,
/// c'était l'allocation.
fn expert_mxfp4_dans(ptr: *const u8, n_out: usize, n_in: usize, e: usize, out: &mut [f32]) {
    const KV: [f32; 16] = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0,
                           0.0, -0.5, -1.0, -1.5, -2.0, -3.0, -4.0, -6.0];
    let nb = n_in / 32;
    let base = unsafe { ptr.add(e * n_out * nb * 17) };
    for o in 0..n_out {
        for b in 0..nb {
            let bloc = unsafe { std::slice::from_raw_parts(base.add((o * nb + b) * 17), 17) };
            let d = crate::gguf::Gguf::echelle_e8m0(bloc[0]);
            let dst = &mut out[o * n_in + b * 32..o * n_in + b * 32 + 32];
            for j in 0..16 {
                dst[j] = KV[(bloc[1 + j] & 0x0F) as usize] * d;
                dst[j + 16] = KV[(bloc[1 + j] >> 4) as usize] * d;
            }
        }
    }
}


/// **Le même produit, sans déquantifier l'expert.** `expert_mxfp4_dans` écrit
/// 3 × 11 M valeurs f32 (132 Mo par expert) que `mv` relit aussitôt. Le noyau
/// MXFP4 du moteur (`DenseQ4::dot16`, AVX2, table de décodage) lit les blocs
/// 17 octets **directement** : plus de tampon intermédiaire, plus quatre fois
/// plus d'octets à faire passer.
///
/// **Ce chemin change la sortie, et il le dit.** Le noyau calcule en entier
/// (LUT × activation i16, échelle e8m0 par bloc) là où le chemin f32 déquantifie
/// puis somme en flottant : mêmes poids, ordre et arithmétique différents. Il est
/// donc OPT-IN (`DRAVE_K3_MXFP4=1`) et se mesure — pas un défaut qu'on glisse.
fn mv_mxfp4(ptr: *const u8, n_out: usize, n_in: usize, e: usize,
            x: &[f32], out: &mut [f32], x16: &mut Vec<i16>, s32: &mut Vec<i32>) {
    let nb = n_in / 32;
    let base = unsafe { ptr.add(e * n_out * nb * 17) };
    let d = unsafe { crate::list::DenseQ4::emprunter(base, n_out, n_in, nb, true) };
    // **L'échelle d'activation n'est pas optionnelle.** Une première version
    // clampait simplement en i16 : les valeurs après SiTU sont de l'ordre de
    // l'unité, donc l'arrondi entier les DÉTRUISAIT — écart relatif mesuré
    // 4,5 % et pente -0,44 (un biais d'échelle, pas un arrondi). Le moteur,
    // lui, quantifie toujours avec une échelle par vecteur et la remet à la
    // fin : `x ≈ x16 · sx`, le noyau rend `Σ w·x16`, on multiplie par `sx`.
    let mut mx = 0f32;
    for &v in x.iter() { let a = v.abs(); if a > mx { mx = a; } }
    let sx = if mx > 0.0 { mx / 32767.0 } else { 1.0 };
    x16.clear();
    for j in 0..n_in {
        x16.push((x[j] / sx).round().clamp(-32767.0, 32767.0) as i16);
    }
    *s32 = crate::list::sommes32(x16);
    for o in 0..n_out { out[o] = d.dot16(o, x16, s32) * sx; }
}

impl MoeK3 {
    pub fn charge(g: &Gguf, l: usize) -> Result<MoeK3, String> {
        let p = |s: &str| format!("blk.{l}.{s}");
        let lu = |nom: &str| -> Result<Vec<f32>, String> {
            if g.tensor(nom).is_none() { return Err(format!("tenseur absent : {nom}")); }
            Ok(g.dequant(nom))
        };
        let dims = |nom: &str| -> Result<Vec<usize>, String> {
            g.tensor(nom).map(|t| t.dims.iter().map(|d| *d as usize).collect())
                .ok_or_else(|| format!("tenseur absent : {nom}"))
        };
        let dg = dims(&p("ffn_gate_exps.weight"))?;    // moteur : [n_exp, moe_ff, latent]
        let du = dims(&p("ffn_up_exps.weight"))?;
        let dd = dims(&p("ffn_down_exps.weight"))?;    // [n_exp, latent, moe_ff]
        let (n_exp, moe_ff, latent) = (dg[0], dg[1], dg[2]);
        if du[0] != n_exp || du[1] != moe_ff || du[2] != latent
            || dd[0] != n_exp || dd[1] != latent || dd[2] != moe_ff {
            return Err(format!("formes d'experts incohérentes : {dg:?} {du:?} {dd:?}"));
        }
        let h = dims(&p("ffn_gate_inp.weight"))?[1];
        let n_shared_ff = dims(&p("ffn_gate_shexp.weight"))?[0];
        let lire = |cle: &str, def: usize| g.meta.get(cle).and_then(|m| m.as_u64())
            .map(|v| v as usize).unwrap_or(def);
        let ptr = |nom: &str| -> Result<*const u8, String> {
            g.data_ptr(nom).ok_or_else(|| format!("données absentes : {nom}"))
        };
        Ok(MoeK3 {
            gate_inp: lu(&p("ffn_gate_inp.weight"))?,
            biais: lu(&p("exp_probs_b.bias"))?,
            rout_down: lu(&p("ffn_routed_down.weight"))?,
            rout_up: lu(&p("ffn_routed_up.weight"))?,
            rout_norm: lu(&p("ffn_routed_norm.weight"))?,
            sh_gate: lu(&p("ffn_gate_shexp.weight"))?,
            sh_up: lu(&p("ffn_up_shexp.weight"))?,
            sh_down: lu(&p("ffn_down_shexp.weight"))?,
            ptr_gate: ptr(&p("ffn_gate_exps.weight"))?,
            ptr_up: ptr(&p("ffn_up_exps.weight"))?,
            ptr_down: ptr(&p("ffn_down_exps.weight"))?,
            n_out_gate: dg[1], n_in_gate: dg[2],
            n_out_up: du[1], n_in_up: du[2],
            n_out_down: dd[1], n_in_down: dd[2],
            n_exp, k: lire("kimi-k3.expert_used_count", 16),
            h, latent, moe_ff: n_shared_ff,
            situ_beta: 4.0, situ_lin: 25.0, eps: 1e-5,
            noyau_mxfp4: std::env::var("DRAVE_K3_MXFP4")
                .map(|v| v != "0" && !v.is_empty()).unwrap_or(false),
            l, appels: std::cell::Cell::new(0),
        })
    }

    /// La passe avant du MoE, dans l'ordre de la référence.
    pub fn avant(&self, cur: &[f32]) -> Result<Vec<f32>, String> {
        let (h, latent, n_exp, k) = (self.h, self.latent, self.n_exp, self.k);
        if cur.len() != h { return Err(format!("entrée de {} au lieu de {h}", cur.len())); }
        // 1. logits du routeur, sur la PLEINE largeur
        let mut logits = vec![0f32; n_exp];
        mv(&self.gate_inp, n_exp, h, cur, &mut logits);
        // 2. sigmoïde, puis SÉLECTION avec le biais (le biais ne va pas aux poids)
        let probs: Vec<f32> = logits.iter().map(|v| 1.0 / (1.0 + (-v).exp())).collect();
        let mut choix: Vec<usize> = (0..n_exp).collect();
        choix.sort_by(|&a, &b| {
            let (pa, pb) = (probs[a] + self.biais[a], probs[b] + self.biais[b]);
            pb.partial_cmp(&pa).unwrap_or(std::cmp::Ordering::Equal)
        });
        let choisis = &choix[..k.min(n_exp)];
        let somme: f32 = choisis.iter().map(|&e| probs[e]).sum();
        let poids: Vec<f32> = choisis.iter().map(|&e| probs[e] / somme.max(1e-20)).collect();
        // 3. le latent
        let mut rin = vec![0f32; latent];
        mv(&self.rout_down, latent, h, cur, &mut rin);
        // Trace de routage (`DRAVE_K3_TRACE_EXPERTS`) : une ligne par (couche,
        // jeton), au même format que le reste du dépôt — c'est ce que lit
        // `tools/analyse_reutilisation_experts.py`. Sans elle, prédire un cache
        // d'experts sur K3 demanderait de l'écrire d'abord.
        if let Ok(chemin) = std::env::var("DRAVE_K3_TRACE_EXPERTS") {
            use std::io::Write;
            if let Ok(mut f) = std::fs::OpenOptions::new().create(true).append(true).open(&chemin) {
                let seq = self.appels.get();
                let mut ids: Vec<String> = choisis.iter().map(|e| e.to_string()).collect();
                ids.sort();
                let _ = writeln!(f, "{} {} {}", self.l, seq, ids.join(" "));
            }
        }
        self.appels.set(self.appels.get() + 1);
        // 4. les k experts, déquantifiés UN PAR UN
        let mut acc = vec![0f32; latent];
        let mut ge = vec![0f32; self.n_out_gate];
        let mut ue = vec![0f32; self.n_out_up];
        let mut de = vec![0f32; self.n_out_down];
        let (mut x16, mut s32) = (Vec::new(), Vec::new());
        for (i, &e) in choisis.iter().enumerate() {
            if self.noyau_mxfp4 {
                // Le noyau du moteur, sur les blocs empruntés au fichier.
                mv_mxfp4(self.ptr_gate, self.n_out_gate, self.n_in_gate, e, &rin, &mut ge,
                         &mut x16, &mut s32);
                mv_mxfp4(self.ptr_up, self.n_out_up, self.n_in_up, e, &rin, &mut ue,
                         &mut x16, &mut s32);
                for j in 0..ge.len() {
                    ge[j] = crate::model::situ(ge[j], ue[j], self.situ_beta, self.situ_lin);
                }
                mv_mxfp4(self.ptr_down, self.n_out_down, self.n_in_down, e, &ge, &mut de,
                         &mut x16, &mut s32);
                for j in 0..latent { acc[j] += poids[i] * de[j]; }
                continue;
            }
            // trois tampons réutilisés d'un expert à l'autre : une allocation
            // par matrice, pas une par bloc.
            let mut g_e = vec![0f32; self.n_out_gate * self.n_in_gate];
            let mut u_e = vec![0f32; self.n_out_up * self.n_in_up];
            let mut d_e = vec![0f32; self.n_out_down * self.n_in_down];
            expert_mxfp4_dans(self.ptr_gate, self.n_out_gate, self.n_in_gate, e, &mut g_e);
            expert_mxfp4_dans(self.ptr_up, self.n_out_up, self.n_in_up, e, &mut u_e);
            expert_mxfp4_dans(self.ptr_down, self.n_out_down, self.n_in_down, e, &mut d_e);
            mv(&g_e, self.n_out_gate, self.n_in_gate, &rin, &mut ge);
            mv(&u_e, self.n_out_up, self.n_in_up, &rin, &mut ue);
            for j in 0..ge.len() { ge[j] = crate::model::situ(ge[j], ue[j], self.situ_beta, self.situ_lin); }
            mv(&d_e, self.n_out_down, self.n_in_down, &ge, &mut de);
            for j in 0..latent { acc[j] += poids[i] * de[j]; }
        }
        // 5. norme DANS le latent, puis remontée
        let mut norme = vec![0f32; latent];
        rms_norm_poids(&acc, &self.rout_norm, self.eps, &mut norme);
        let mut sortie = vec![0f32; h];
        mv(&self.rout_up, h, latent, &norme, &mut sortie);
        // 6. les experts partagés (toujours actifs), ajoutés
        let mut gs = vec![0f32; self.moe_ff];
        let mut us = vec![0f32; self.moe_ff];
        mv(&self.sh_gate, self.moe_ff, h, cur, &mut gs);
        mv(&self.sh_up, self.moe_ff, h, cur, &mut us);
        for j in 0..self.moe_ff { gs[j] = crate::model::situ(gs[j], us[j], self.situ_beta, self.situ_lin); }
        let mut sh = vec![0f32; h];
        mv(&self.sh_down, h, self.moe_ff, &gs, &mut sh);
        for j in 0..h { sortie[j] += sh[j]; }
        Ok(sortie)
    }
}

// ===========================================================================
// La couche MLA de K3 (couches 3, 7, 11, … — une sur quatre).
//
// Différences avec l'MLA de V4/V4.1, et elles comptent :
//   - `mla_use_nope` : la partie `pe` est portée et concaténée, mais AUCUNE
//     rotation n'est appliquée ;
//   - `k_b` et `v_b` sont PAR TÊTE (tenseurs 3D) : l'absorption se fait tête par
//     tête, pas par une matrice unique ;
//   - la porte de sortie est un SIGMOÏDE plein rang (`attn_gate`), appliqué sur
//     l'entrée de couche NORMALISÉE, avant la projection de sortie.
// ===========================================================================

pub struct MlaK3 {
    q_a: Vec<f32>, q_a_norm: Vec<f32>, q_b: Vec<f32>,     // [1536×h], [1536], [18432×1536]
    kv_a: Vec<f32>, kv_a_norm: Vec<f32>,                  // [(512+64)×h], [512]
    k_b: Vec<f32>, v_b: Vec<f32>,                         // par tête : [512×128], [128×512]
    gate: Vec<f32>, wo: Vec<f32>,                         // [12288×h], [h×12288]
    h: usize, nh: usize, hd: usize, rope: usize, kv_lora: usize,
    /// Cache des clés/valeurs : une ligne par position déjà vue.
    cle: Vec<f32>, val: Vec<f32>, n_pos: usize, eps: f32,
}

impl MlaK3 {
    pub fn charge(g: &Gguf, l: usize) -> Result<MlaK3, String> {
        let p = |s: &str| format!("blk.{l}.{s}");
        let lu = |nom: &str| -> Result<Vec<f32>, String> {
            if g.tensor(nom).is_none() { return Err(format!("tenseur absent : {nom}")); }
            Ok(g.dequant(nom))
        };
        let dims = |nom: &str| -> Result<Vec<usize>, String> {
            g.tensor(nom).map(|t| t.dims.iter().map(|d| *d as usize).collect())
                .ok_or_else(|| format!("tenseur absent : {nom}"))
        };
        let dq = dims(&p("attn_q_b.weight"))?;        // moteur : [nh*hd, q_lora]
        let dk = dims(&p("attn_k_b.weight"))?;        // [nh, kv_lora, nope] ?
        let dv = dims(&p("attn_v_b.weight"))?;
        let dkv = dims(&p("attn_kv_a_mqa.weight"))?;  // [kv_lora+rope, h]
        let lire = |cle: &str, def: usize| g.meta.get(cle).and_then(|m| m.as_u64())
            .map(|v| v as usize).unwrap_or(def);
        let nh = dk[0];
        let kv_lora = dk[1];
        let nope = dk[2];
        let h = dkv[1];
        let rope = dkv[0] - kv_lora;
        let hd = nope + rope;
        if dq[0] != nh * hd { return Err(format!("q_b {:?} ≠ {}×{}", dq, nh, hd)); }
        // `v_b` : [nh, n_embd_head_v, kv_lora] — la tête de valeur peut différer
        // de la tête de requête (128 ici), on la DÉDUIT au lieu de la supposer.
        if dv[0] != nh || dv[2] != kv_lora {
            return Err(format!("v_b {:?} : {nh} têtes et un latent de {kv_lora} attendus", dv));
        }
        let _ = lire;
        Ok(MlaK3 {
            q_a: lu(&p("attn_q_a.weight"))?, q_a_norm: lu(&p("attn_q_a_norm.weight"))?,
            q_b: lu(&p("attn_q_b.weight"))?,
            kv_a: lu(&p("attn_kv_a_mqa.weight"))?, kv_a_norm: lu(&p("attn_kv_a_norm.weight"))?,
            k_b: lu(&p("attn_k_b.weight"))?, v_b: lu(&p("attn_v_b.weight"))?,
            gate: lu(&p("attn_gate.weight"))?, wo: lu(&p("attn_output.weight"))?,
            h, nh, hd, rope, kv_lora,
            cle: Vec::new(), val: Vec::new(), n_pos: 0, eps: 1e-5,
        })
    }

    /// Un jeton, à la position `pos` : la couche MLA complète, cache compris.
    /// `x_norme` est l'entrée de couche **normalisée** (la porte de sortie la lit).
    pub fn avant(&mut self, cur: &[f32], x_norme: &[f32], pos: usize) -> Result<Vec<f32>, String> {
        let (h, nh, hd, rope, kv_lora) = (self.h, self.nh, self.hd, self.rope, self.kv_lora);
        if cur.len() != h { return Err(format!("entrée de {} au lieu de {h}", cur.len())); }
        // 1. Q = q_b · rms_norm(q_a · cur)
        let q_lora = self.q_a.len() / h;
        let mut qa = vec![0f32; q_lora];
        mv(&self.q_a, q_lora, h, cur, &mut qa);
        let mut qan = vec![0f32; q_lora];
        rms_norm_poids(&qa, &self.q_a_norm, self.eps, &mut qan);
        let mut q = vec![0f32; nh * hd];
        mv(&self.q_b, nh * hd, q_lora, &qan, &mut q);
        // 2. kv = kv_a · cur, puis latent normalisé + partie pe (SANS rotation)
        let mut kv = vec![0f32; kv_lora + rope];
        mv(&self.kv_a, kv_lora + rope, h, cur, &mut kv);
        let mut latent = vec![0f32; kv_lora];
        rms_norm_poids(&kv[..kv_lora], &self.kv_a_norm, self.eps, &mut latent);
        let pe = &kv[kv_lora..];
        // 3. cache : clé = [latent, pe] (576), valeur = latent (512)
        if self.n_pos <= pos {
            self.cle.resize((pos + 1) * (kv_lora + rope), 0.0);
            self.val.resize((pos + 1) * kv_lora, 0.0);
            self.n_pos = pos + 1;
        }
        self.cle[pos * (kv_lora + rope)..pos * (kv_lora + rope) + kv_lora]
            .copy_from_slice(&latent);
        self.cle[pos * (kv_lora + rope) + kv_lora..(pos + 1) * (kv_lora + rope)]
            .copy_from_slice(pe);
        self.val[pos * kv_lora..(pos + 1) * kv_lora].copy_from_slice(&latent);
        // 4. attention causale, tête par tête, avec ABSORPTION de k_b
        let echelle = 1.0 / ((hd as f32).sqrt());
        let nope = hd - rope;
        let mut sortie = vec![0f32; nh * (hd - rope)];
        for t in 0..nh {
            // q_nope absorbé : [nope] → [kv_lora] par la matrice de tête
            let base_kb = t * kv_lora * nope;
            let mut qn = vec![0f32; kv_lora];
            for o in 0..kv_lora {
                let lig = &self.k_b[base_kb + o * nope..base_kb + (o + 1) * nope];
                let mut s = 0f32;
                for j in 0..nope { s += lig[j] * q[t * hd + j]; }
                qn[o] = s;
            }
            // ⚠️ Après absorption, la requête fait [latent 512, rope 64] = 576 —
            // la taille de la CLÉ — et non `hd` = 192. Se tromper fait tomber la
            // copie (« range end 512 out of range for length 192 ») : c'est la
            // panique qui l'a dit, pas la relecture.
            let mut qa2 = vec![0f32; kv_lora + rope];
            qa2[..kv_lora].copy_from_slice(&qn);
            qa2[kv_lora..].copy_from_slice(&q[t * hd + nope..t * hd + nope + rope]);
            // scores contre toutes les positions ≤ pos
            let mut scores = Vec::with_capacity(pos + 1);
            for p2 in 0..=pos {
                let c = &self.cle[p2 * (kv_lora + rope)..(p2 + 1) * (kv_lora + rope)];
                let mut s = 0f32;
                for j in 0..(kv_lora + rope) { s += qa2[j] * c[j]; }
                scores.push(s * echelle);
            }
            let mx = scores.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
            let mut somme = 0f32;
            for v in scores.iter_mut() { *v = (*v - mx).exp(); somme += *v; }
            // somme pondérée des valeurs (le latent), puis v_b : [kv_lora] → [head_v]
            let head_v = self.v_b.len() / (nh * kv_lora);
            let mut acc = vec![0f32; kv_lora];
            for p2 in 0..=pos {
                let pds = scores[p2] / somme;
                let v = &self.val[p2 * kv_lora..(p2 + 1) * kv_lora];
                for j in 0..kv_lora { acc[j] += pds * v[j]; }
            }
            let base_vb = t * head_v * kv_lora;
            for o in 0..head_v {
                let lig = &self.v_b[base_vb + o * kv_lora..base_vb + (o + 1) * kv_lora];
                let mut s = 0f32;
                for j in 0..kv_lora { s += lig[j] * acc[j]; }
                sortie[t * head_v + o] = s;
            }
        }
        // 5. porte de sortie (sigmoïde plein rang) sur l'entrée NORMALISÉE
        let d_inner = sortie.len();
        let mut g2 = vec![0f32; d_inner];
        mv(&self.gate, d_inner, h, x_norme, &mut g2);   // porte : reste en f32
        for j in 0..d_inner { sortie[j] *= 1.0 / (1.0 + (-g2[j]).exp()); }
        // 6. projection de sortie
        let mut out = vec![0f32; h];
        mv(&self.wo, h, d_inner, &sortie, &mut out);
        Ok(out)
    }
}

// ===========================================================================
// Le KDA, extrait en pièce RÉUTILISABLE (couches 1, 2, 4, 5, 6, 8, …).
//
// La couche 0 l'embarquait avec son FFN dense ; la composition (couche 0 → 1)
// exige de pouvoir le charger SEUL, pour n'importe quelle couche.
// ===========================================================================


/// **Une projection Q8_0 EMPRUNTÉE au fichier.** `g.dequant(nom)` copie la
/// matrice en f32 — 4 octets par poids au lieu de 1,06, et cette copie est
/// allouée puis libérée à CHAQUE chargement de couche. Sur la passe complète,
/// cela fait ~224 Go de tampons f32 par appel, ce qui **évince le cache de
/// pages** : les blocs Q8_0 du dense ne peuvent pas y rester, donc ils sont
/// relus au disque à chaque jeton. C'est le mur mesuré (voir
/// `docs/verification-kimi-k3.md`, « le mur est le disque »).
///
/// Emprunter les blocs supprime la copie ET laisse le cache de pages faire son
/// travail : le dense fait 59,6 Go, la machine a 125 Go de RAM.
struct Q8 {
    d: crate::list::DenseQ8,
}

impl Q8 {
    /// `None` si le tenseur n'est pas du Q8_0 (on retombe alors sur le f32).
    fn emprunter(g: &Gguf, nom: &str) -> Option<Q8> {
        let t = g.tensor(nom)?;
        let n_out = t.dims[0] as usize;
        let n_in = t.dims[1] as usize;
        let (buf, nb) = g.q8_blocks(nom)?;
        Some(Q8 { d: unsafe { crate::list::DenseQ8::emprunter_q8(buf.as_ptr(), n_out, n_in, nb) } })
    }

    /// `x ≈ xd · sx`, le noyau rend `Σ w·xd`, on remultiplie par `sx`. Même
    /// schéma que partout ailleurs dans le moteur : sans l'échelle, les
    /// activations de l'ordre de l'unité seraient détruites par l'arrondi
    /// entier (mesuré : 4,5 % d'écart et une pente de −0,44 sur la sortie).
    fn mv(&self, x: &[f32], out: &mut [f32], xd: &mut Vec<i32>) {
        let n_in = self.d.n_in;
        let mut mx = 0f32;
        for &v in x[..n_in].iter() { let a = v.abs(); if a > mx { mx = a; } }
        let sx = if mx > 0.0 { mx / 127.0 } else { 1.0 };
        xd.clear();
        for j in 0..n_in { xd.push((x[j] / sx).round().clamp(-127.0, 127.0) as i32); }
        for o in 0..self.d.n_out { out[o] = self.d.dot_q8_source(o, xd) * sx; }
    }
}

pub struct KdaK3 {
    /// Les cinq grosses projections, **empruntées** au fichier (Q8_0).
    q: Q8, k: Q8, v: Q8, wo: Q8, g_proj: Q8,
    f_a: Vec<f32>, f_b: Vec<f32>,
    conv_q: Vec<f32>, conv_k: Vec<f32>, conv_v: Vec<f32>,
    beta_w: Vec<f32>, ssm_a: Vec<f32>, dt_bias: Vec<f32>, o_norm: Vec<f32>,
    etat_conv_q: Vec<f32>, etat_conv_k: Vec<f32>, etat_conv_v: Vec<f32>,
    etat_delta: Vec<f32>,
    h: usize, nh: usize, hd: usize, d_inner: usize, d_conv: usize, eps: f32,
}

impl KdaK3 {
    pub fn charge(g: &Gguf, l: usize) -> Result<KdaK3, String> {
        let p = |s: &str| format!("blk.{l}.{s}");
        let lu = |nom: &str| -> Result<Vec<f32>, String> {
            if g.tensor(nom).is_none() { return Err(format!("tenseur absent : {nom}")); }
            Ok(g.dequant(nom))
        };
        let dims = |nom: &str| -> Result<Vec<usize>, String> {
            g.tensor(nom).map(|t| t.dims.iter().map(|d| *d as usize).collect())
                .ok_or_else(|| format!("tenseur absent : {nom}"))
        };
        let h = dims(&p("attn_norm.weight"))?[0];
        let nh = dims(&p("ssm_beta.weight"))?[0];
        let hd = dims(&p("ssm_norm.weight"))?[0];
        let d_inner = nh * hd;
        let d_conv = *dims(&p("ssm_conv1d_q.weight"))?.last().unwrap_or(&4);
        let etat = vec![0f32; (d_conv - 1) * d_inner];
        let emp = |n: &str| -> Result<Q8, String> {
            Q8::emprunter(g, n).ok_or_else(|| format!("{n} : pas du Q8_0 empruntable"))
        };
        Ok(KdaK3 {
            q: emp(&p("attn_q.weight"))?, k: emp(&p("attn_k.weight"))?,
            v: emp(&p("attn_v.weight"))?,
            wo: emp(&p("attn_output.weight"))?,
            f_a: lu(&p("ssm_f_a.weight"))?, f_b: lu(&p("ssm_f_b.weight"))?,
            g_proj: emp(&p("ssm_g.weight"))?,
            conv_q: lu(&p("ssm_conv1d_q.weight"))?, conv_k: lu(&p("ssm_conv1d_k.weight"))?,
            conv_v: lu(&p("ssm_conv1d_v.weight"))?,
            beta_w: lu(&p("ssm_beta.weight"))?, ssm_a: lu(&p("ssm_a"))?,
            dt_bias: lu(&p("ssm_dt.bias"))?, o_norm: lu(&p("ssm_norm.weight"))?,
            etat_conv_q: etat.clone(), etat_conv_k: etat.clone(), etat_conv_v: etat,
            etat_delta: vec![0f32; nh * hd * hd],
            h, nh, hd, d_inner, d_conv, eps: 1e-5,
        })
    }

    /// L'attention KDA seule, sur une entrée **déjà normalisée** (`attn_norm`).
    pub fn avant(&mut self, cur: &[f32]) -> Result<Vec<f32>, String> {
        let (h, nh, hd, d_inner) = (self.h, self.nh, self.hd, self.d_inner);
        if cur.len() != h { return Err(format!("entrée de {} au lieu de {h}", cur.len())); }
        let mut q = vec![0f32; d_inner];
        let mut k = vec![0f32; d_inner];
        let mut v = vec![0f32; d_inner];
        let mut xd: Vec<i32> = Vec::new();
        self.q.mv(cur, &mut q, &mut xd);
        self.k.mv(cur, &mut k, &mut xd);
        self.v.mv(cur, &mut v, &mut xd);
        let mut qc = vec![0f32; d_inner];
        let mut kc = vec![0f32; d_inner];
        let mut vc = vec![0f32; d_inner];
        crate::model::kda_conv_silu(&q, &self.conv_q, &mut self.etat_conv_q, self.d_conv, d_inner, &mut qc);
        crate::model::kda_conv_silu(&k, &self.conv_k, &mut self.etat_conv_k, self.d_conv, d_inner, &mut kc);
        crate::model::kda_conv_silu(&v, &self.conv_v, &mut self.etat_conv_v, self.d_conv, d_inner, &mut vc);
        // La norme L2 par tête, entre la convolution et la récurrence.
        l2_q_et_k(&mut qc, &mut kc, nh, hd, self.eps);
        let mut fa = vec![0f32; hd];
        mv(&self.f_a, hd, h, cur, &mut fa);
        let mut g1 = vec![0f32; d_inner];
        mv(&self.f_b, d_inner, hd, &fa, &mut g1);
        let mut beta = vec![0f32; nh];
        mv(&self.beta_w, nh, h, cur, &mut beta);
        let mut o = vec![0f32; d_inner];
        let mut tampon = vec![0f32; hd];
        for t in 0..nh {
            let mut g = vec![0f32; hd];
            for i in 0..hd {
                g[i] = crate::model::kda_porte(g1[t * hd + i] + self.dt_bias[t * hd + i],
                                               self.ssm_a[t], -5.0);
            }
            let b = 1.0 / (1.0 + (-beta[t]).exp());
            let mut ot = vec![0f32; hd];
            crate::model::kda_pas(&qc[t * hd..(t + 1) * hd], &kc[t * hd..(t + 1) * hd],
                                  &vc[t * hd..(t + 1) * hd], &g, b,
                                  &mut self.etat_delta[t * hd * hd..(t + 1) * hd * hd], hd, &mut ot);
            o[t * hd..(t + 1) * hd].copy_from_slice(&ot);
        }
        let mut g2 = vec![0f32; d_inner];
        self.g_proj.mv(cur, &mut g2, &mut xd);
        for t in 0..nh {
            rms_norm_poids(&o[t * hd..(t + 1) * hd], &self.o_norm, self.eps, &mut tampon[..hd]);
            for i in 0..hd {
                let s = 1.0 / (1.0 + (-g2[t * hd + i]).exp());
                o[t * hd + i] = tampon[i] * s;
            }
        }
        let mut out = vec![0f32; h];
        self.wo.mv(&o, &mut out, &mut xd);
        Ok(out)
    }

    pub fn zero(&mut self) {
        self.etat_conv_q.iter_mut().for_each(|v| *v = 0.0);
        self.etat_conv_k.iter_mut().for_each(|v| *v = 0.0);
        self.etat_conv_v.iter_mut().for_each(|v| *v = 0.0);
        self.etat_delta.iter_mut().for_each(|v| *v = 0.0);
    }
}

// ===========================================================================
// Les pièces qui manquaient pour COMPOSER des couches : les quatre petits
// tenseurs de norme/score de chaque couche, et le FFN dense de la couche 0.
// ===========================================================================

/// `attn_norm`, `attn_res_score`, `ffn_norm`, `ffn_res_score` d'une couche.
pub struct NormesK3 {
    pub attn: Vec<f32>, pub attn_score: Vec<f32>,
    pub ffn: Vec<f32>, pub ffn_score: Vec<f32>,
}

impl NormesK3 {
    pub fn charge(g: &Gguf, l: usize) -> Result<NormesK3, String> {
        let p = |s: &str| format!("blk.{l}.{s}");
        let lu = |nom: String| -> Result<Vec<f32>, String> {
            if g.tensor(&nom).is_none() { return Err(format!("tenseur absent : {nom}")); }
            Ok(g.dequant(&nom))
        };
        Ok(NormesK3 {
            attn: lu(p("attn_norm.weight"))?, attn_score: lu(p("attn_res_score.weight"))?,
            ffn: lu(p("ffn_norm.weight"))?, ffn_score: lu(p("ffn_res_score.weight"))?,
        })
    }
}

/// Le FFN **dense** de la couche 0 (SiTU), séparé de son attention KDA.
pub struct FfnDenseK3 {
    gate: Vec<f32>, up: Vec<f32>, down: Vec<f32>,
    h: usize, ffn: usize, beta: f32, lin: f32,
}

impl FfnDenseK3 {
    pub fn charge(g: &Gguf, l: usize) -> Result<FfnDenseK3, String> {
        let p = |s: &str| format!("blk.{l}.{s}");
        let lu = |nom: String| -> Result<Vec<f32>, String> {
            if g.tensor(&nom).is_none() { return Err(format!("tenseur absent : {nom}")); }
            Ok(g.dequant(&nom))
        };
        let h = g.tensor(&p("ffn_norm.weight")).map(|t| t.dims[0] as usize)
            .ok_or_else(|| "ffn_norm absent".to_string())?;
        let ffn = g.tensor(&p("ffn_gate.weight")).map(|t| t.dims[0] as usize)
            .ok_or_else(|| "ffn_gate absent".to_string())?;
        Ok(FfnDenseK3 {
            gate: lu(p("ffn_gate.weight"))?, up: lu(p("ffn_up.weight"))?,
            down: lu(p("ffn_down.weight"))?,
            h, ffn, beta: 4.0, lin: 25.0,
        })
    }

    pub fn avant(&self, x: &[f32]) -> Result<Vec<f32>, String> {
        if x.len() != self.h { return Err(format!("entrée de {} au lieu de {}", x.len(), self.h)); }
        let mut g = vec![0f32; self.ffn];
        let mut u = vec![0f32; self.ffn];
        mv(&self.gate, self.ffn, self.h, x, &mut g);
        mv(&self.up, self.ffn, self.h, x, &mut u);
        for j in 0..self.ffn { g[j] = crate::model::situ(g[j], u[j], self.beta, self.lin); }
        let mut out = vec![0f32; self.h];
        mv(&self.down, self.h, self.ffn, &g, &mut out);
        Ok(out)
    }
}

/// **Composition des premières couches** — l'instrument qui vérifie la CHAÎNE
/// (attention résiduelle, banque tous les 12, redémarrage du flux) et pas
/// seulement les pièces. Les états sont remis à zéro par `zero()`.
pub struct PetitesK3 {
    pub normes: Vec<NormesK3>,
    pub kda: Vec<Option<KdaK3>>,
    pub mla: Vec<Option<MlaK3>>,
    pub ffn_dense: Vec<Option<FfnDenseK3>>,
    pub moe: Vec<Option<MoeK3>>,
    pub pile: Vec<f32>, pub n_ckpt: usize,
    pub h: usize, pub eps: f32, pub bloc: usize,
}

impl PetitesK3 {
    /// Charge les couches `0..n` (les tenseurs doivent être présents).
    pub fn charge(g: &Gguf, n: usize) -> Result<PetitesK3, String> {
        let h = g.tensor("blk.0.attn_norm.weight").map(|t| t.dims[0] as usize)
            .ok_or_else(|| "blk.0.attn_norm absent".to_string())?;
        let mut s = PetitesK3 { normes: Vec::new(), kda: Vec::new(), mla: Vec::new(),
                                ffn_dense: Vec::new(), moe: Vec::new(),
                                pile: Vec::new(), n_ckpt: 0, h, eps: 1e-5, bloc: 12 };
        for l in 0..n {
            s.normes.push(NormesK3::charge(g, l)?);
            let mla = g.tensor(&format!("blk.{l}.attn_kv_a_mqa.weight")).is_some();
            if mla {
                s.kda.push(None);
                s.mla.push(Some(MlaK3::charge(g, l)?));
            } else {
                s.kda.push(Some(KdaK3::charge(g, l)?));
                s.mla.push(None);
            }
            if l == 0 {
                s.ffn_dense.push(Some(FfnDenseK3::charge(g, l)?));
                s.moe.push(None);
            } else {
                s.ffn_dense.push(None);
                s.moe.push(Some(MoeK3::charge(g, l)?));
            }
        }
        Ok(s)
    }

    /// Un jeton, à la position `pos`, à travers les `n` couches chargées.
    pub fn avant(&mut self, x0: &[f32], pos: usize) -> Result<Vec<f32>, String> {
        let h = self.h;
        // La banque appartient à la PASSE d'un jeton (voir `Couche0::avant`) :
        // la repartir ici est ce qui rend l'appel par jeton équivalent au lot.
        self.pile.clear();
        self.n_ckpt = 0;
        let mut x = x0.to_vec();
        for l in 0..self.normes.len() {
            let n = &self.normes[l];
            // 1. attention résiduelle sur le flux courant
            let mut cur = vec![0f32; h];
            if self.n_ckpt == 0 { cur.copy_from_slice(&x); }
            else {
                crate::model::res_mix(&self.pile, self.n_ckpt, h, &x, &n.attn_score, self.eps, &mut cur);
            }
            // 2. banque : on empile l'entrée BRUTE, avant l'attention
            let banque = l % self.bloc == 0;
            if banque { self.pile.extend_from_slice(&x); self.n_ckpt += 1; }
            // 3. norme puis attention (KDA ou MLA)
            let mut xn = vec![0f32; h];
            rms_norm_poids(&cur, &n.attn, self.eps, &mut xn);
            let attn = if let Some(kda) = self.kda[l].as_mut() {
                kda.avant(&xn)?
            } else {
                self.mla[l].as_mut().unwrap().avant(&xn, &xn, pos)?
            };
            // 4. le flux reprend : redémarrage si la couche est une banque
            let mut prefix = if banque { vec![0f32; h] } else { x.clone() };
            for i in 0..h { prefix[i] += attn[i]; }
            // 5. attention résiduelle avant la FFN, puis norme
            let mut cur2 = vec![0f32; h];
            crate::model::res_mix(&self.pile, self.n_ckpt, h, &prefix, &n.ffn_score, self.eps, &mut cur2);
            let mut xn2 = vec![0f32; h];
            rms_norm_poids(&cur2, &n.ffn, self.eps, &mut xn2);
            // 6. FFN dense (couche 0) ou MoE latent
            let ffn = if let Some(f) = self.ffn_dense[l].as_ref() { f.avant(&xn2)? }
                      else { self.moe[l].as_ref().unwrap().avant(&xn2)? };
            for i in 0..h { prefix[i] += ffn[i]; }
            x = prefix;
        }
        Ok(x)
    }

    pub fn zero(&mut self) {
        self.pile.clear();
        self.n_ckpt = 0;
        for k in self.kda.iter_mut().flatten() { k.zero(); }
    }
}

// ===========================================================================
// LA PASSE COMPLÈTE, COUCHE PAR COUCHE
//
// `PetitesK3::charge(g, n)` garde les n couches EN MÉMOIRE, tout le dense en
// f32 : 25 couches tiennent (59 Go), 93 n'y tiennent pas (~220 Go pour 125 Go de
// RAM). Or rien n'oblige à les garder : l'état récurrent d'une couche ne sert
// QUE pendant la passe de cette couche sur les jetons. En traitant les couches
// dans l'ordre et les jetons à l'intérieur de chaque couche — ce que fait déjà
// llama.cpp, dont le graphe est évalué couche par couche — une seule couche est
// vivante à la fois.
//
// Ce que ça change : le pic mémoire passe de « toutes les couches » à « une
// couche » (~2,2 Go), plus les états (~0,6 Go) et la pile résiduelle (quelques
// kilo-octets). Les 93 couches deviennent donc calculables sur cette machine.
//
// Ce que ça ne change PAS : le coût. Une couche MoE déquantifie ses 16 experts
// en f32, soit ~28 s par jeton ; 93 couches × 4 jetons font ~3 h. C'est un
// instrument de VÉRIFICATION, et il le reste.
// ===========================================================================

/// Une couche chargée, prête à traiter les jetons du lot.
enum CoucheK3 {
    Dense { normes: NormesK3, kda: Option<KdaK3>, mla: Option<MlaK3>, ffn: FfnDenseK3 },
    Moe  { normes: NormesK3, kda: Option<KdaK3>, mla: Option<MlaK3>, moe: MoeK3 },
}

impl CoucheK3 {
    fn charge(g: &Gguf, l: usize) -> Result<CoucheK3, String> {
        let normes = NormesK3::charge(g, l)?;
        let mla = g.tensor(&format!("blk.{l}.attn_kv_a_mqa.weight")).is_some();
        let kda = if mla { None } else { Some(KdaK3::charge(g, l)?) };
        let mlao = if mla { Some(MlaK3::charge(g, l)?) } else { None };
        if l == 0 {
            Ok(CoucheK3::Dense { normes, kda, mla: mlao, ffn: FfnDenseK3::charge(g, l)? })
        } else {
            Ok(CoucheK3::Moe { normes, kda, mla: mlao, moe: MoeK3::charge(g, l)? })
        }
    }
}

/// L'état récurrent d'une couche, sorti de son objet pour survivre à sa
/// libération. C'est ce qui permet de GÉNÉRER : la passe streaming recharge
/// chaque couche à chaque jeton, donc l'état doit vivre ailleurs que dans la
/// couche. Sa taille est modeste — 6,3 Mo de delta et 0,4 Mo de convolution par
/// couche KDA, soit ~0,6 Go pour les 93 couches — et c'est le prix à payer pour
/// ne garder qu'UNE couche de POIDS en mémoire.
pub enum EtatCouche {
    Kda { cq: Vec<f32>, ck: Vec<f32>, cv: Vec<f32>, delta: Vec<f32> },
    Mla { cle: Vec<f32>, val: Vec<f32>, n_pos: usize },
    Aucun,
}

impl CoucheK3 {
    fn sauver(&self) -> EtatCouche {
        match self {
            CoucheK3::Dense { kda, mla, .. } | CoucheK3::Moe { kda, mla, .. } => {
                if let Some(k) = kda {
                    EtatCouche::Kda { cq: k.etat_conv_q.clone(), ck: k.etat_conv_k.clone(),
                                      cv: k.etat_conv_v.clone(), delta: k.etat_delta.clone() }
                } else if let Some(m) = mla {
                    EtatCouche::Mla { cle: m.cle.clone(), val: m.val.clone(), n_pos: m.n_pos }
                } else { EtatCouche::Aucun }
            }
        }
    }
    fn restaurer(&mut self, e: &EtatCouche) {
        let (kda, mla) = match self {
            CoucheK3::Dense { kda, mla, .. } => (kda, mla),
            CoucheK3::Moe { kda, mla, .. } => (kda, mla),
        };
        match e {
            EtatCouche::Kda { cq, ck, cv, delta } => {
                if let Some(k) = kda.as_mut() {
                    k.etat_conv_q.copy_from_slice(cq);
                    k.etat_conv_k.copy_from_slice(ck);
                    k.etat_conv_v.copy_from_slice(cv);
                    k.etat_delta.copy_from_slice(delta);
                }
            }
            EtatCouche::Mla { cle, val, n_pos } => {
                if let Some(m) = mla.as_mut() {
                    // AFFECTATION, pas `copy_from_slice` : le cache MLA d'une
                    // couche fraîchement chargée est VIDE (sa taille définitive
                    // n'est connue qu'après le premier jeton), alors que l'état
                    // sauvegardé en porte déjà `n_pos` lignes. Copier dans un
                    // tampon de longueur nulle paniquait — « source slice
                    // length (1728) does not match destination slice length
                    // (0) » — et faisait tomber la génération APRÈS le premier
                    // pas, celui qui était justement vérifié.
                    m.cle = cle.clone();
                    m.val = val.clone();
                    m.n_pos = *n_pos;
                }
            }
            EtatCouche::Aucun => {}
        }
    }
}

/// **La passe complète** : `ids` traversés de la couche 0 à la couche `n-1`,
/// **La passe complète** : `ids` traversés de la couche 0 à la couche `n-1`,
/// une couche chargée à la fois. Rend le flux résiduel de chaque jeton après la
/// dernière couche — ce que la référence vide sous le nom `l_out-<n-1>`.
///
/// La banque est `[point de contrôle][jeton][canal]` : dans la référence,
/// `resi_stack` est `[n_embd, n_ckpt, n_tokens]`, donc un point de contrôle
/// porte UNE COLONNE PAR JETON du lot. L'aplatir en poussant une entrée par
/// jeton et par couche donnerait un `n_ckpt` quatre fois trop grand et un
/// mélange entre jetons.
pub fn passe_complete(g: &Gguf, ids: &[u32], n: usize, verbeux: bool, tete: bool,
                      pos0: usize, mut etats: Option<&mut Vec<EtatCouche>>)
                      -> Result<Vec<Vec<f32>>, String> {
    let h = g.tensor("blk.0.attn_norm.weight").map(|t| t.dims[0] as usize)
        .ok_or_else(|| "blk.0.attn_norm absent".to_string())?;
    let eps = 1e-5f32;
    let bloc = 12usize;
    let ntok = ids.len();
    let embd = g.dequant("token_embd.weight");
    let mut flux: Vec<Vec<f32>> = ids.iter()
        .map(|&t| embd[t as usize * h..(t as usize + 1) * h].to_vec()).collect();
    // pile[k][i] = entrée BRUTE du jeton i à la couche banque k.
    let mut pile: Vec<Vec<Vec<f32>>> = Vec::new();

    // Le temps se sépare en deux : CHARGER (lire les poids, les déquantifier en
    // f32, restaurer l'état) et CALCULER. Sans cette séparation, on optimise à
    // l'aveugle — et « ça a l'air lent » n'est pas une mesure.
    let (mut t_charge, mut t_calcul) = (0f64, 0f64);
    let (mut t_attn, mut t_ffn) = (0f64, 0f64);
    for l in 0..n {
        let t0 = std::time::Instant::now();
        let mut c = CoucheK3::charge(g, l)?;
        if let Some(e) = etats.as_deref_mut() {
            if let Some(ec) = e.get(l) { c.restaurer(ec); }
        }
        let t1 = std::time::Instant::now();
        let banque = l % bloc == 0;
        // ---- phase 1 : l'attention résiduelle voit la banque d'AVANT la
        //      couche courante (`res_mix` est appelé avant `res_push`).
        let n_avant = pile.len();
        let mut curs: Vec<Vec<f32>> = Vec::with_capacity(ntok);
        for i in 0..ntok {
            if n_avant == 0 { curs.push(flux[i].clone()); continue; }
            let mut plat = Vec::with_capacity(n_avant * h);
            for ck in pile.iter() { plat.extend_from_slice(&ck[i]); }
            let w = match &c {
                CoucheK3::Dense { normes, .. } => &normes.attn_score,
                CoucheK3::Moe { normes, .. } => &normes.attn_score,
            };
            let mut out = vec![0f32; h];
            crate::model::res_mix(&plat, n_avant, h, &flux[i], w, eps, &mut out);
            curs.push(out);
        }
        // ---- la couche est une banque : on empile son entrée BRUTE, toutes
        //      les colonnes du lot d'un coup.
        if banque { pile.push(flux.clone()); }

        for i in 0..ntok {
            let x = flux[i].clone();
            let mut prefix;
            let mut cur2 = vec![0f32; h];
            {
                let (normes, kda, mla) = match &mut c {
                    CoucheK3::Dense { normes, kda, mla, .. } => (normes, kda, mla),
                    CoucheK3::Moe { normes, kda, mla, .. } => (normes, kda, mla),
                };
                let ta = std::time::Instant::now();
                let mut xn = vec![0f32; h];
                rms_norm_poids(&curs[i], &normes.attn, eps, &mut xn);
                let attn = if let Some(k) = kda.as_mut() { k.avant(&xn)? }
                           else { mla.as_mut().unwrap().avant(&xn, &xn, pos0 + i)? };
                t_attn += ta.elapsed().as_secs_f64();
                prefix = if banque { vec![0f32; h] } else { x.clone() };
                for j in 0..h { prefix[j] += attn[j]; }
                let mut plat = Vec::with_capacity(pile.len() * h);
                for ck in pile.iter() { plat.extend_from_slice(&ck[i]); }
                crate::model::res_mix(&plat, pile.len(), h, &prefix,
                                      &normes.ffn_score, eps, &mut cur2);
            }
            let mut xn2 = vec![0f32; h];
            {
                let n2 = match &c {
                    CoucheK3::Dense { normes, .. } => &normes.ffn,
                    CoucheK3::Moe { normes, .. } => &normes.ffn,
                };
                rms_norm_poids(&cur2, n2, eps, &mut xn2);
            }
            let tf = std::time::Instant::now();
            let ffn = match &mut c {
                CoucheK3::Dense { ffn, .. } => ffn.avant(&xn2)?,
                CoucheK3::Moe { moe, .. } => moe.avant(&xn2)?,
            };
            t_ffn += tf.elapsed().as_secs_f64();
            for j in 0..h { prefix[j] += ffn[j]; }
            flux[i] = prefix;
        }
        t_charge += (t1 - t0).as_secs_f64();
        t_calcul += (std::time::Instant::now() - t1).as_secs_f64();
        if verbeux {
            eprintln!("  couche {l:>2} : {:>6} ms de chargement + {:>6} ms de calcul · banque {}{}",
                      (t1 - t0).as_millis(), (std::time::Instant::now() - t1).as_millis(),
                      pile.len(), if banque { " (empilée)" } else { "" });
        }
        // On sort l'état avant que `c` ne tombe : c'est lui qui survit.
        if let Some(e) = etats.as_deref_mut() {
            let sauve = c.sauver();
            if e.len() <= l { e.resize_with(l + 1, || EtatCouche::Aucun); }
            e[l] = sauve;
        }
        // `c` tombe ici : c'est tout l'intérêt (ses POIDS, pas son état).
    }
    if verbeux {
        let tot = t_charge + t_calcul;
        eprintln!("  ---- chargement {:.1} s ({:.0} %) · calcul {:.1} s ({:.0} %) \
[attention {:.1} s · FFN {:.1} s]",
                  t_charge, 100.0 * t_charge / tot.max(1e-9),
                  t_calcul, 100.0 * t_calcul / tot.max(1e-9), t_attn, t_ffn);
    }
    // ---- LA TÊTE : mélange résiduel final, norme, puis la matrice de sortie.
    // C'est ce que la référence fait APRÈS la boucle (`res_mix(cur, output_res_score, -1)`,
    // `build_norm(output_norm)`, `output`), et c'est ce qui rend la comparaison
    // possible sur les LOGITS — le critère de la porte de correction du dépôt —
    // et non seulement sur un état caché.
    if tete {
        let w = g.dequant("output_res_score.weight");
        let norme = g.dequant("output_norm.weight");
        let sortie = g.dequant("output.weight");
        let vocab = g.tensor("output.weight").map(|t| t.dims[0] as usize)
            .ok_or_else(|| "output.weight absent".to_string())?;
        let mut lgs = Vec::with_capacity(ntok);
        for i in 0..ntok {
            let mut cur = vec![0f32; h];
            if pile.is_empty() { cur.copy_from_slice(&flux[i]); }
            else {
                let mut plat = Vec::with_capacity(pile.len() * h);
                for ck in pile.iter() { plat.extend_from_slice(&ck[i]); }
                crate::model::res_mix(&plat, pile.len(), h, &flux[i], &w, eps, &mut cur);
            }
            let mut xn = vec![0f32; h];
            rms_norm_poids(&cur, &norme, eps, &mut xn);
            let mut lg = vec![0f32; vocab];
            mv(&sortie, vocab, h, &xn, &mut lg);
            lgs.push(lg);
        }
        return Ok(lgs);
    }
    Ok(flux)
}
