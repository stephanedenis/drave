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


// ===========================================================================
// Contrôle des DIMENSIONS, tensor par tensor, avant d'écrire le calcul.
//
// C'est la classe de bug qui a déjà mordu : le moteur range `dims[0] = ne1` (la
// SORTIE) alors que le GGUF range `ne0` en premier. Une dimension lue du mauvais
// côté ne se voit ni à la compilation ni à la relecture — elle se voit au
// premier produit matriciel, ou jamais si les deux nombres sont proches.
// ===========================================================================

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
        // 4. les k experts, déquantifiés UN PAR UN
        let mut acc = vec![0f32; latent];
        for (i, &e) in choisis.iter().enumerate() {
            // trois tampons réutilisés d'un expert à l'autre : une allocation
            // par matrice, pas une par bloc.
            let mut g_e = vec![0f32; self.n_out_gate * self.n_in_gate];
            let mut u_e = vec![0f32; self.n_out_up * self.n_in_up];
            let mut d_e = vec![0f32; self.n_out_down * self.n_in_down];
            expert_mxfp4_dans(self.ptr_gate, self.n_out_gate, self.n_in_gate, e, &mut g_e);
            expert_mxfp4_dans(self.ptr_up, self.n_out_up, self.n_in_up, e, &mut u_e);
            expert_mxfp4_dans(self.ptr_down, self.n_out_down, self.n_in_down, e, &mut d_e);
            let mut ge = vec![0f32; self.n_out_gate];
            let mut ue = vec![0f32; self.n_out_up];
            mv(&g_e, self.n_out_gate, self.n_in_gate, &rin, &mut ge);
            mv(&u_e, self.n_out_up, self.n_in_up, &rin, &mut ue);
            for j in 0..ge.len() { ge[j] = crate::model::situ(ge[j], ue[j], self.situ_beta, self.situ_lin); }
            let mut de = vec![0f32; self.n_out_down];
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
        mv(&self.gate, d_inner, h, x_norme, &mut g2);
        for j in 0..d_inner { sortie[j] *= 1.0 / (1.0 + (-g2[j]).exp()); }
        // 6. projection de sortie
        let mut out = vec![0f32; h];
        mv(&self.wo, h, d_inner, &sortie, &mut out);
        Ok(out)
    }
}
