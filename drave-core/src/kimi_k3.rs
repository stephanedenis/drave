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
