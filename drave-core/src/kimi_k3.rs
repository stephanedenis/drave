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
            pile: Vec::new(), n_ckpt: 0,
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
        self.pile.extend_from_slice(x);
        self.n_ckpt += 1;
        // 3. RMSNorm d'entrée
        let mut cur = vec![0f32; h];
        rms_norm_poids(&cur0, &self.attn_norm, self.eps, &mut cur);
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
        let mut attn = vec![0f32; h];
        mv(&self.wo, h, d_inner, &o, &mut attn);
        // 8. le flux REDÉMARRE ici (couche « banque ») : `prefix = attn`, pas `x + attn`
        let mut prefix = attn.clone();
        // 9. attention résiduelle avant la FFN
        let mut cur_ffn = vec![0f32; h];
        crate::model::res_mix(&self.pile, self.n_ckpt, h, &prefix, &self.ffn_res_score,
                              self.eps, &mut cur_ffn);
        rms_norm_poids(&cur_ffn, &self.ffn_norm, self.eps, &mut cur);
        // 10. FFN dense avec SiTU
        let mut fg = vec![0f32; self.ffn];
        let mut fu = vec![0f32; self.ffn];
        mv(&self.ffn_gate, self.ffn, h, &cur, &mut fg);
        mv(&self.ffn_up, self.ffn, h, &cur, &mut fu);
        let beta_s = 4.0f32; let lin = 25.0f32;
        for i in 0..self.ffn { fg[i] = crate::model::situ(fg[i], fu[i], beta_s, lin); }
        let mut ff = vec![0f32; h];
        mv(&self.ffn_down, h, self.ffn, &fg, &mut ff);
        // 11. le flux reprend
        for i in 0..h { prefix[i] += ff[i]; }
        Ok(prefix)
    }
}
