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

/// Convention de routage des experts — quatre familles, et une seule
/// implémentation partagée par le jeton seul et le lot (voir [`router`]).
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Gating {
    /// `softmax` sur TOUS les logits, top-k, renormalisation. Qwen3-MoE, et le
    /// défaut de llama.cpp quand un modèle ne déclare rien.
    Softmax,
    /// `sigmoid` sur chaque logit, top-k sur ces scores, renormalisation.
    /// Kimi-K2.7 (`expert_gating_func = 2`), GLM-5.3 et GLM-5.3-Flash.
    Sigmoid,
    /// Top-k sur les logits **bruts** (plus le biais de sélection s'il existe),
    /// puis `softmax` sur les seuls k retenus — et **pas** de renormalisation
    /// ensuite, le softmax s'en charge. gpt-oss.
    SoftmaxPoids,
    /// `sqrt(softplus(x)) = sqrt(log(1+e^x))` sur chaque logit, top-k,
    /// renormalisation. DeepSeek V4-Flash (`expert_gating_func = 4`) et V4.1.
    SqrtSoftplus,
}

impl Gating {
    /// Numéro `expert_gating_func` du GGUF, tel que llama.cpp le définit.
    pub fn du_numero(n: u64) -> Option<Gating> {
        match n {
            1 => Some(Gating::Softmax),
            2 => Some(Gating::Sigmoid),
            3 => Some(Gating::SoftmaxPoids),
            4 => Some(Gating::SqrtSoftplus),
            _ => None,
        }
    }

    /// Nom lisible : ce que le moteur dit qu'il applique.
    pub fn nom(&self) -> &'static str {
        match self {
            Gating::Softmax => "softmax",
            Gating::Sigmoid => "sigmoïde",
            Gating::SoftmaxPoids => "top-k brut + softmax",
            Gating::SqrtSoftplus => "racine de softplus",
        }
    }
}

/// **Le moteur sait-il calculer ce modèle ?** — vérifié AVANT de construire
/// quoi que ce soit, avec la liste de ce qui manque.
///
/// Sans ce contrôle, un modèle d'architecture inconnue mourait sur un
/// « tenseur blk.3.attn_q.weight absent » qui accuse le FICHIER alors que c'est
/// le MOTEUR qui ne sait pas. Le coût n'est pas la panne, c'est la panne
/// trompeuse : on cherche le tenseur manquant dans un GGUF de 216 Go au lieu de
/// lire que l'attention MLA à rang faible n'est pas implémentée.
///
/// Trois des cinq plus gros modèles de cette machine sont dans ce cas —
/// Kimi-K2.7 (1 026 G poids), GLM-5.3 (754 G), DeepSeek-V4-Flash (284 G) et
/// V4.1 (755 G) : MLA à rang faible (`attn_q_a`/`attn_q_b`), hyper-connexions
/// (`hc_*`), attention par index (`indexer`), routage par table (`tid2eid`) et
/// engram. Aucun n'a jamais été exécuté par ce moteur ; leurs chiffres publiés
/// viennent d'analyses STATIQUES des tenseurs, pas d'une passe avant.
/// Ce que le moteur ne sait pas calculer de ce modèle, nommé.
///
/// **Une seule liste**, utilisée par le refus à l'ouverture ET par `--config`.
/// Deux copies de ce contrôle avaient déjà divergé : `--config` annonçait deux
/// manques quand la passe avant en refusait trois.
pub fn manques_architecture(g: &Gguf, cfg: &Cfg, ctx: usize, clusters: bool) -> Vec<&'static str> {
    // Le test porte sur TOUTES les couches, pas sur la couche 0 : GLM-5.3 a
    // trois couches denses puis des couches MLA, et regarder la première
    // laissait passer le modèle jusqu'au panic « attn_q absent » de la couche 3.
    let quelque_part = |suffixe: &str| g.tensors.iter().any(|t| t.name.ends_with(suffixe));
    let mut manques: Vec<&str> = Vec::new();
    if quelque_part("hc_attn_fn.weight") || quelque_part("hc_ffn_fn.weight") {
        manques.push("hyper-connexions (hc_attn_fn, hc_ffn_fn, hc_mult)");
    }
    // Attention par index (DSA) : l'indexeur choisit les clés gardées. Il ne
    // sert QUE si la séquence dépasse `index_topk` — en deçà, llama.cpp garde
    // toutes les clés et l'indexeur n'est pas appelé. On refuse donc seulement
    // les contextes où il changerait le résultat.
    if quelque_part("indexer.") {
        let topk = g.cfg("index_topk").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
        if topk == 0 || ctx > topk {
            manques.push("attention par index appris (indexer) au-delà de index_topk");
        }
    }
    // L'engram est une table mmappée que le moteur sait ADRESSER (`--sonder-engram`)
    // mais pas encore CALCULER. llama.cpp l'ignore aussi : ce n'est donc pas un
    // obstacle à une exécution comparable à la sienne, et le dire évite de
    // compter un manque qui n'en est pas un pour la validation croisée.
    if quelque_part("engram_embd.weight") || quelque_part("engram.weight")
        || g.cfg("engram.layer_ids").is_some() || g.json_brut("engram_layer_ids").is_some() {
        // informatif seulement : voir `--sonder-engram`
    }
    if quelque_part("attn_output_a.weight") {
        manques.push("projection de sortie à rang faible groupée (attn_output_a/attn_output_b, o_groups)");
    }
    // DeepSeek-V4 : l'attention n'est pas la MLA « simple » de GLM/Kimi.
    // `attn_derope` renvoie la sortie d'attention dans le repère non tourné et
    // surtout `compress_ratios` fait cohabiter TROIS attentions dans le même
    // modèle : compressée à candidats (CSA/LID), compressée simple (HCA) et
    // brute. Les implémenter à moitié donnerait des nombres faux sans rien
    // casser — c'est exactement ce que ce contrôle doit empêcher.
    //
    // Les puits par tête (`attn_sinks.weight`), eux, SONT implémentés : gpt-oss
    // en a et sa porte tourne (`--config` répond « calculable : oui » ; le
    // chargement, lui, affiche « puits appris sur 36/36 »). Les ranger dans le
    // même manque faisait répondre « calculable : NON » à un modèle que le
    // moteur calcule — un refus faux est un refus trompeur.
    //
    // Réserve connue : `attn_mla` ne consomme PAS `lay.sinks`. Aucun modèle du
    // parc ne combine le chemin MLA (`attn_kv_a_mqa`) et des puits ; le jour où
    // ça arrive, ce test devra refuser (ou `attn_mla` devra les appliquer).
    if quelque_part("attn_derope") {
        manques.push("attention V4 : dé-rotation de sortie");
    }
    if g.cfg("compress_ratios").is_some() || g.json_brut("compress_ratios").is_some() {
        manques.push("attentions compressées CSA/HCA (compress_ratios, candidate_*)");
    }
    if quelque_part("attn_q_a.weight") {
        // Informatif : la MLA à rang faible EST implémentée (`attn_mla`) et
        // validée à la position 0 contre llama.cpp (GLM-5.3) ; l'écart croît
        // ensuite. Le dire une fois, à l'ouverture, plutôt que de laisser
        // croire qu'un modèle qui tourne est un modèle juste.
        eprintln!("[mla] attention MLA à rang faible : cache LATENT (c_kv + k_rope), pas de \
fenêtre glissante ni de YaRN sur ce chemin. Validée contre llama.cpp sur GLM-5.3 à la \
POSITION 0 : corrélation des logits 0,999024, top-1 3/3 ; l'écart croît ensuite \
(+0,009 / +0,372 / +0,611 puis +4,070 nat à la position 3 — voir reports/rapport-mla-experts.md §7).");
    }
    manques
}

#[allow(clippy::too_many_arguments)]
fn refus_architecture(g: &Gguf, cfg: &Cfg, ctx: usize, clusters: bool, manques: Vec<&str>)
    -> Result<(), String> {
    if !manques.is_empty() {
        return Err(format!(
            "architecture « {} » non implémentée par ce moteur : {}.\n  \
Ce modèle n'a JAMAIS été exécuté ici : tout chiffre publié à son sujet vient \
d'une analyse statique des tenseurs (inventaire, empreinte, sonde mmap), pas \
d'une passe avant.\n  Tenseurs présents : {}{}{}",
            g.meta.get("general.architecture").and_then(|m| m.as_str()).unwrap_or("?"),
            manques.join(" · "),
            if g.tensors.iter().any(|t| t.name.ends_with("attn_q_a.weight")) { "attn_q_a " } else { "" },
            if g.tensors.iter().any(|t| t.name.ends_with("hc_attn_fn.weight")) { "hc_attn_fn " } else { "" },
            if g.tensors.iter().any(|t| t.name.ends_with("indexer.")) { "indexer " } else { "" }));
    }
    // Modèle à experts dont les tenseurs d'experts sont absents : ce n'est pas
    // une architecture inconnue, c'est un fichier incomplet — dit autrement.
    // Sauf en mode CLUSTERS : les experts y sont préfixés (`cl0/blk.0.…`), donc
    // « blk.0.ffn_gate_exps.weight absent » y est normal. Ce contrôle a refusé
    // le modèle en clusters de la porte publiée — un garde-fou qui casse une
    // porte verte est un garde-fou mal placé.
    if !clusters && cfg.n_expert > 0 && g.tensor("blk.0.ffn_gate_exps.weight").is_none()
        && g.tensor("blk.1.ffn_gate_exps.weight").is_none()
        && g.tensor("blk.0.ffn_gate.weight").is_none() {
        return Err(format!(
            "le modèle déclare {} experts mais aucun tenseur d'experts n'est lisible \
(blk.0.ffn_gate_exps.weight absent) — fichier tronqué, ou découpage en clusters \
incomplet", cfg.n_expert));
    }
    Ok(())
}

/// Dimension lue dans les clefs GGUF normalisées, puis dans les noms d'origine
/// de DeepSeek, puis dans le JSON `<arch>.config`.
///
/// Les trois existent dans la nature, et un modèle qui n'utilise QUE la
/// troisième était décrit avec des zéros : `--config` annonçait « couches : 0 »
/// pour DeepSeek-V4.1-Flash, dont tout le bloc `text_config` vit dans le JSON
/// (num_hidden_layers, hidden_size, num_attention_heads…). Un zéro silencieux
/// est pire qu'une absence : le plan matériel et les heuristiques s'appuient
/// dessus.
pub fn dim_gguf(g: &Gguf, cles: &[&str], cle_json: &str) -> Option<u64> {
    g.cfg_ou(cles).and_then(|m| m.as_u64())
        .or_else(|| g.json_nombre(cle_json).map(|v| v as u64))
}

pub fn reel_gguf(g: &Gguf, cles: &[&str], cle_json: &str) -> Option<f64> {
    g.cfg_ou(cles).and_then(|m| m.as_f64())
        .or_else(|| g.json_nombre(cle_json))
}

/// Décision de **routage** lue dans les métadonnées, avec sa provenance.
///
/// La provenance compte : « sigmoïde » peut venir d'une clef GGUF explicite, du
/// nom d'origine de DeepSeek, du JSON `<arch>.config`, ou d'un défaut choisi par
/// le moteur. Les quatre ne se valent pas — un défaut est une hypothèse, et le
/// mode `--config` la montre comme telle.
pub struct Routage {
    pub n_expert: usize,
    pub n_expert_used: usize,
    pub ffn_exp: usize,
    pub gating: Gating,
    /// D'où vient `gating` : `expert_gating_func`, le JSON, ou le défaut.
    pub source: &'static str,
    pub norm: bool,
    pub echelle: f32,
    pub hash_layers: usize,
}

/// Lit la convention de routage des experts — **une seule fois, à un seul
/// endroit** : le chargement du modèle et le mode `--config` appellent ceci.
pub fn routage_du_gguf(g: &Gguf) -> Routage {
    let arch = g.meta.get("general.architecture").and_then(|m| m.as_str())
                   .unwrap_or("").to_string();
    // Trois sources, dans cet ordre : la clef normalisée du GGUF, le nom
    // d'origine de DeepSeek, puis le JSON `<arch>.config` recopié par le
    // convertisseur. V4.1-Flash-Q2 n'a QUE la troisième : sans elle, il était
    // pris pour un modèle dense (`n_expert = 0`), donc exécuté sans un seul
    // expert.
    let n_expert = g.cfg_ou(&["expert_count", "n_routed_experts"])
                    .and_then(|m| m.as_u64())
                    .or_else(|| g.json_nombre("n_routed_experts").map(|v| v as u64))
                    .unwrap_or(0) as usize;
    let n_expert_used = g.cfg_ou(&["expert_used_count", "num_experts_per_tok"])
                    .and_then(|m| m.as_u64())
                    .or_else(|| g.json_nombre("num_experts_per_tok").map(|v| v as u64))
                    .unwrap_or(0) as usize;
    let ffn_exp = g.cfg_ou(&["expert_feed_forward_length", "moe_intermediate_size"])
                    .and_then(|m| m.as_u64())
                    .or_else(|| g.json_nombre("moe_intermediate_size").map(|v| v as u64))
                    .unwrap_or(0) as usize;
    let declare = g.cfg_ou(&["expert_gating_func"]).and_then(|m| m.as_u64())
                    .and_then(Gating::du_numero);
    let du_json = || g.json_texte("scoring_func").and_then(|v| match v.as_str() {
        "softmax" => Some(Gating::Softmax),
        "sigmoid" => Some(Gating::Sigmoid),
        "sqrtsoftplus" => Some(Gating::SqrtSoftplus),
        _ => None,
    });
    let (gating, source) = match declare {
        Some(x) => (x, "expert_gating_func"),
        None => match du_json() {
            Some(x) => (x, "JSON scoring_func"),
            None => (if arch == "gpt-oss" { Gating::SoftmaxPoids } else { Gating::Softmax },
                     "défaut du moteur"),
        },
    };
    // `expert_weights_norm` : vrai partout sauf gpt-oss, dont le softmax sur
    // les k somme déjà à 1. Le défaut « vrai » conserve les portes publiées
    // (Qwen2.5 dense, Qwen3-MoE, gpt-oss) ; les modèles qui déclarent
    // explicitement la clef sont lus, eux.
    let norm = g.cfg_ou(&["expert_weights_norm", "norm_topk_prob"])
                    .and_then(|m| m.as_bool())
                    .or_else(|| g.json_bool("norm_topk_prob"))
                    .unwrap_or(gating != Gating::SoftmaxPoids);
    let echelle = g.cfg_ou(&["expert_weights_scale", "routed_scaling_factor"])
                    .and_then(|m| m.as_f64())
                    .or_else(|| g.json_nombre("routed_scaling_factor"))
                    .unwrap_or(0.0) as f32;
    let hash_layers = g.cfg("hash_layer_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
    Routage { n_expert, n_expert_used, ffn_exp, gating, source, norm, echelle, hash_layers }
}

/// Calcule `sqrt(softplus(x))` comme llama.cpp : `softplus(x) = log(1+e^x)`,
/// avec `x` rendu tel quel au-delà de 20 (où `log(1+e^x)` vaut `x` à la
/// précision du f32 près). Sous −20, `e^x` s'annule : le résultat est 0.
#[inline]
fn sqrt_softplus(x: f32) -> f32 {
    let sp = if x > 20.0 { x } else { (1.0 + x.exp()).ln() };
    sp.sqrt()
}

/// **Sélection des experts d'une couche** — une seule implémentation, appelée
/// par le jeton seul ET par le lot.
///
/// Elle existe parce que les deux chemins avaient divergé : le biais du routeur
/// de gpt-oss était ajouté aux poids dans l'un et pas dans l'autre. Un modèle
/// dont la porte verte ne couvre qu'un des deux chemins ne dit rien de l'autre.
///
/// Quatre conventions coexistent (voir [`Gating`]), et les confondre ne casse
/// rien de visible : la perplexité monte de quelques pour cent, et les experts
/// choisis changent en silence.
///
/// `tid2eid` : les `hash_layer_count` premières couches de DeepSeek-V4 routent
/// par **table**, pas par score — l'expert est une fonction de l'identifiant du
/// jeton. Le biais de sélection ne s'y applique pas (llama.cpp passe
/// `exp_probs_b = nullptr`), mais les poids, la renormalisation et le facteur
/// d'échelle, oui.
///
/// Rend `(expert, poids)` dans l'ordre de sélection ; les poids somment à 1
/// (ou à `expert_scale`) et sont déjà multipliés par le facteur.
fn router(cfg: &Cfg, moe: &Moe, x: &[f32], tid: u32, k: usize) -> Vec<(usize, f32)> {
    let ne = moe.routeur.len() / x.len().max(1);
    let h = x.len();
    let mut logits = vec![0f32; ne];
    for e in 0..ne {
        let r = &moe.routeur[e * h..(e + 1) * h];
        logits[e] = r.iter().zip(x.iter()).map(|(a, b)| a * b).sum();
    }
    // Scores servant à la SÉLECTION, et scores servant aux POIDS : ils
    // diffèrent pour gpt-oss, dont le biais ne départage que la sélection.
    let biais = moe.routeur_biais.as_ref();
    let (mut probs, mut sel): (Vec<f32>, Vec<f32>) = match cfg.gating {
        Gating::Softmax => {
            let mx = logits.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
            let mut somme = 0f32;
            let mut p: Vec<f32> = logits.iter().map(|v| { let e = (v - mx).exp(); somme += e; e }).collect();
            if somme > 0.0 { for v in p.iter_mut() { *v /= somme; } }
            (p.clone(), p)
        }
        Gating::Sigmoid => {
            let p: Vec<f32> = logits.iter().map(|v| 1.0 / (1.0 + (-v).exp())).collect();
            let s = match biais { Some(b) => p.iter().zip(b).map(|(a, c)| a + c).collect(), None => p.clone() };
            (p, s)
        }
        Gating::SoftmaxPoids => {
            let s = match biais { Some(b) => logits.iter().zip(b).map(|(a, c)| a + c).collect(), None => logits.clone() };
            (logits.clone(), s)
        }
        Gating::SqrtSoftplus => {
            let p: Vec<f32> = logits.iter().map(|v| sqrt_softplus(*v)).collect();
            let s = match biais { Some(b) => p.iter().zip(b).map(|(a, c)| a + c).collect(), None => p.clone() };
            (p, s)
        }
    };
    let k = k.clamp(1, ne);
    let chosis: Vec<usize> = match moe.tid2eid.as_ref() {
        Some(t) => {
            let base = tid as usize * k;
            (0..k).map(|j| t[base + j].max(0) as usize).collect()
        }
        None => {
            let mut idx: Vec<u32> = (0..ne as u32).collect();
            if k < ne {
                idx.select_nth_unstable_by(k, |&a, &b| {
                    sel[b as usize].partial_cmp(&sel[a as usize]).unwrap()
                });
                idx.truncate(k);
            }
            idx.into_iter().map(|e| e as usize).collect()
        }
    };
    let mut poids: Vec<f32> = chosis.iter().map(|&e| probs[e]).collect();
    // gpt-oss : le softmax porte sur les k POIDS retenus, après sélection.
    // La renormalisation MULTIPLIE par l'inverse au lieu de diviser : c'est ce
    // que faisait le moteur avant que les deux chemins de routage soient
    // réunis, et `x * (1/s)` n'est pas `x / s` au dernier bit près. La
    // différence traverse 48 couches et déplace la porte publiée de 0,03 % —
    // mesuré, en comparant l'ancien et le nouveau binaire sur le même modèle.
    if cfg.gating == Gating::SoftmaxPoids {
        let mx = poids.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
        let mut somme = 0f32;
        for v in poids.iter_mut() { *v = (*v - mx).exp(); somme += *v; }
        if somme > 0.0 {
            let inv = 1.0 / somme;
            for v in poids.iter_mut() { *v *= inv; }
        }
    } else if cfg.expert_norm {
        let somme: f32 = poids.iter().sum();
        if somme > 0.0 {
            let inv = 1.0 / somme;
            for v in poids.iter_mut() { *v *= inv; }
        }
    }
    if cfg.expert_scale != 0.0 && cfg.expert_scale != 1.0 {
        for v in poids.iter_mut() { *v *= cfg.expert_scale; }
    }
    let _ = &mut probs;
    chosis.into_iter().zip(poids).collect()
}

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
    /// Convention de routage des experts (voir [`Gating`]).
    ///
    /// Elle était implicite et binaire — « softmax sur tous » ou « top-k sur les
    /// bruts » — ce qui est faux pour trois des cinq gros modèles MoE de cette
    /// machine : Kimi-K2.7 et GLM-5.3 routent par **sigmoïde**, V4-Flash et
    /// V4.1 par **racine de softplus**. Confondre les deux conventions ne casse
    /// rien de visible : la perplexité monte de quelques pour cent et les
    /// experts choisis changent en silence.
    pub gating: Gating,
    /// Renormaliser les poids des k experts retenus pour qu'ils somment à 1
    /// (`expert_weights_norm`, `norm_topk_prob`). Vrai chez Qwen3-MoE,
    /// DeepSeek, GLM et Kimi ; faux chez gpt-oss, où le softmax sur les k
    /// suffit déjà.
    pub expert_norm: bool,
    /// Facteur appliqué APRÈS la renormalisation (`expert_weights_scale`,
    /// `routed_scaling_factor`) : 1,5 pour V4-Flash et V4.1, 2,5 pour GLM-5.3,
    /// 2,827 pour Kimi-K2.7, 0 (aucun) ailleurs. Il était purement et simplement
    /// absent du moteur — un facteur d'échelle sur la sortie des experts change
    /// l'amplitude du flux résiduel, donc toute la suite du réseau.
    pub expert_scale: f32,
    /// Nombre de premières couches dont le routage est **donné** par la table
    /// `ffn_gate_tid2eid` (`hash_layer_count`) : 3 pour V4-Flash. Ces couches
    /// n'ont pas de top-k : l'expert est une fonction de l'identifiant du jeton.
    pub hash_layers: usize,
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
    use crate::gguf::{GGML_IQ1_M, GGML_IQ1_S, GGML_IQ2_XXS, GGML_IQ3_XXS,
                      GGML_MXFP4, GGML_Q4_0, GGML_Q4_K, GGML_Q6_K};
    use crate::list::Source;
    match t {
        GGML_Q4_K => Some(Source::Q4_K),
        GGML_Q6_K => Some(Source::Q6_K),
        GGML_MXFP4 => Some(Source::Mxfp4),
        GGML_Q4_0 => Some(Source::Q4_0),
        // Super-blocs de 256 poids SANS noyau dédié : déquantification puis
        // produit en f32. La liste est celle de `list::sans_noyau` — un test
        // vérifie que les deux ne peuvent pas diverger.
        _ if crate::list::sans_noyau(t) => Some(Source::Dequant(t)),
        _ => None,
    }
}

/// Charge le mélange d'experts d'une couche, s'il existe.
///
/// Les trois tenseurs `ffn_*_exps` sont des tenseurs **3D** dont la première
/// dimension (la plus lente) est l'expert : chaque expert est donc un bloc
/// contigu, et le moteur n'a besoin que d'un pointeur et d'un pas.
fn charger_moe(g: &Gguf, l: usize, n_expert: usize, map: Option<&'static crate::clusters::Mapping>)
    -> Option<Moe> {
    if n_expert == 0 { return None; }
    let p = |s: &str| format!("blk.{l}.{s}");
    // Un tenseur d'experts est soit en clair dans le fichier ouvert, soit dans
    // les fichiers de clusters sous le préfixe `cl{c}/`. Dans le second cas
    // chaque fichier ne porte QUE ses experts locaux : la dimension d'expert
    // du tenseur vaut `experts_par_cluster`, pas `n_expert`.
    let vues = |s: &str| -> Option<(Vec<usize>, Vec<Vue4>)> {
        let base = p(s);
        let (numeros, noms): (Vec<usize>, Vec<String>) = match map {
            // Un mapping actif prime sur le nom en clair : si les deux existent,
            // c'est le découpage qui dit où sont les experts, et lire le tenseur
            // entier indexerait ensuite une ligne locale dans un tenseur global.
            None if g.tensor(&base).is_some() => (vec![0], vec![base.clone()]),
            Some(m) => {
                // Les préfixes sont attribués par POSITION dans la liste des
                // fichiers ; un fichier qui ne porte pas ce tenseur décalerait
                // tous les suivants, en silence (mêmes formes). On exige donc la
                // série complète, dans l'ordre.
                // Un nœud partiel ne charge qu'une partie des clusters : les
                // absents sont NORMAUX. On garde ceux qui sont là, dans l'ordre
                // des numéros — c'est le préfixe qui porte le numéro, donc
                // `mapping.tsv` continue de désigner le bon fichier.
                let v: Vec<(usize, String)> = (0..m.n_clusters)
                    .map(|c| (c, format!("cl{c}/{base}")))
                    .filter(|(_, n)| g.tensor(n).is_some()).collect();
                if v.is_empty() {
                    eprintln!("[moe] couche {l} : aucun cluster chargé ne porte « {base} »");
                    return None;
                }
                (v.iter().map(|(c, _)| *c).collect(),
                 v.into_iter().map(|(_, n)| n).collect())
            }
            None => { eprintln!("[moe] couche {l} : « {base} » absent et aucun mapping"); return None; }
        };
        if noms.is_empty() {
            eprintln!("[moe] couche {l} : aucun fichier ne porte « {base} » (essayé le nom \
en clair et cl0..cl{})", map.map(|m| m.n_clusters.saturating_sub(1)).unwrap_or(0));
            return None;
        }
        let mut out = Vec::with_capacity(noms.len());
        for nom in &noms {
            let t = g.tensor(nom)?;
            if t.dims.len() < 3 { return None; }
            let ligne_experts = t.dims[0] as usize;
            // La dimension d'expert du tenseur doit être EXACTEMENT celle que
            // le mapping annonce : ni le nombre global (ce serait un tenseur non
            // découpé, dont les lignes locales n'ont pas le même sens), ni autre
            // chose. Une tolérance ici ferait lire le mauvais expert sans bruit.
            let attendu = match map { Some(m) => m.par_cluster, None => n_expert };
            if ligne_experts != attendu {
                match map {
                    Some(m) => eprintln!("[moe] couche {l} : « {nom} » a {ligne_experts} \
experts, le mapping en annonce {} par cluster", m.par_cluster),
                    None => eprintln!("[moe] couche {l} : « {nom} » a {ligne_experts} experts \
au lieu de {n_expert}, et aucun mapping n'est actif"),
                }
                return None;
            }
            let Some(src) = source_de(t.ttype) else {
                eprintln!("[moe] couche {l} : « {nom} » de type {} — format sans noyau ni déquantification", crate::gguf::Gguf::nom_type(t.ttype));
                return None;
            };
            let (n_out, n_in) = (t.dims[1] as usize, t.dims[2] as usize);
            let bloc = if t.ttype == crate::gguf::GGML_Q4_K || t.ttype == crate::gguf::GGML_Q6_K { 256 } else { 32 };
            if n_in % bloc != 0 {
                eprintln!("[moe] couche {l} : « {nom} » a {n_in} entrées, non multiple de {bloc}");
                return None;
            }
            let Some(ptr) = g.data_ptr(nom) else {
                eprintln!("[moe] couche {l} : données de « {nom} » introuvables");
                return None;
            };
            out.push(Vue4 { base: ptr, n_out, n_in, nb: n_in / bloc, src });
        }
        Some((numeros, out))
    };
    // Vue d'un tenseur 3D NON découpé (l'expert partagé, qui reste dans le
    // fichier commun) : aucune traduction d'index n'est nécessaire.
    // Vue d'un tenseur NON découpé : l'expert partagé, qui reste dans le
    // fichier commun. Il est en 2D (`[n_ff, hidden]`) — exiger 3 dimensions le
    // refusait en silence, et l'expert partagé des modèles DeepSeek/GLM/Kimi
    // n'était donc jamais calculé. Sa contribution n'est pas un détail : c'est
    // un FFN entier, toujours actif, ajouté à la sortie des experts routés.
    let vue_unique = |nom: &str| -> Option<Vue4> {
        let t = g.tensor(nom)?;
        let src = source_de(t.ttype)?;
        let (n_out, n_in) = match t.dims.len() {
            2 => (t.dims[0] as usize, t.dims[1] as usize),
            n if n >= 3 => (t.dims[1] as usize, t.dims[2] as usize),
            _ => return None,
        };
        let bloc = if t.ttype == crate::gguf::GGML_Q4_K || t.ttype == crate::gguf::GGML_Q6_K { 256 } else { 32 };
        if n_in % bloc != 0 { return None; }
        Some(Vue4 { base: g.data_ptr(nom)?, n_out, n_in, nb: n_in / bloc, src })
    };
    let (numeros, gate) = vues("ffn_gate_exps.weight")?;
    let (num_up, up) = vues("ffn_up_exps.weight")?;
    let (num_down, down) = vues("ffn_down_exps.weight")?;
    if num_up != numeros || num_down != numeros {
        panic!("couche {l} : les trois projections d'experts ne portent pas les mêmes \
clusters ({numeros:?}, {num_up:?}, {num_down:?})");
    }
    if map.is_some() {
        // L'EXHAUSTIVITÉ se vérifie à l'ouverture du dossier (numérotation
        // continue, ou chaque cluster demandé présent), pas ici : un contrôle
        // par couche devrait deviner si ce nœud est partiel, et le deviner par
        // un état global l'a rendu intestable (les tests s'exécutent en
        // parallèle, un `OnceLock` ne se pose qu'une fois). Ici, seule la
        // cohérence ENTRE les trois projections est du ressort de la couche.
        if gate.len() != up.len() || gate.len() != down.len() {
            panic!("couche {l} : {} fichiers de gate, {} de up, {} de down — répartition \
incohérente entre les trois projections d'experts", gate.len(), up.len(), down.len());
        }
    }
    let routeur = g.dequant(&p("ffn_gate_inp.weight"));
    assert_eq!(routeur.len(), n_expert * gate[0].n_in, "routeur de taille inattendue");
    // Le mapping et les métadonnées doivent décrire le MÊME modèle. Un mapping
    // étranger aux mêmes formes ferait sauter en silence les experts routés
    // au-delà de son propre compte.
    if let Some(m) = map {
        assert_eq!(m.n_experts, n_expert,
            "couche {l} : le mapping décrit {} experts, le modèle en déclare {n_expert} \
— mapping d'un autre modèle ?", m.n_experts);
    }
    // Expert partagé (Qwen3-MoE d'origine, DeepSeek) : toujours actif.
    let shexp = match (vue_unique(&p("ffn_gate_shexp.weight")),
                       vue_unique(&p("ffn_up_shexp.weight")),
                       vue_unique(&p("ffn_down_shexp.weight"))) {
        (Some(a), Some(b), Some(c)) => Some((a, b, c)),
        _ => None,
    };
    let n_ff = gate[0].n_out;
    let biais = |nom: &str| -> Option<Vec<f32>> {
        let t = g.tensor(nom)?;
        // ne = (n_ff, n_expert) : l'expert est la dimension la plus lente.
        if t.dims.len() != 2 || t.dims[0] as usize != n_expert { return None; }
        Some(g.dequant(nom))
    };
    // Biais de SÉLECTION, et il y en a deux sortes dans les GGUF :
    //   - `ffn_gate_inp.bias` (gpt-oss) : ajouté aux logits avant le top-k ;
    //   - `exp_probs_b.bias` (DeepSeek-V3/V4, GLM-5.3, Kimi) : le
    //     `e_score_correction_bias` du routage `noaux_tc`, ajouté aux scores
    //     pour la sélection SEULEMENT.
    // Les confondre ou en oublier un change les experts choisis — et rien
    // d'autre : la perplexité part en vrille sans qu'aucun tenseur ne manque.
    let routeur_biais = if g.tensor(&p("exp_probs_b.bias")).is_some() {
        Some(g.dequant(&p("exp_probs_b.bias")))
    } else if g.tensor(&p("ffn_gate_inp.bias")).is_some() {
        Some(g.dequant(&p("ffn_gate_inp.bias")))
    } else { None };
    let (bg, bu, bd) = (biais(&p("ffn_gate_exps.bias")), biais(&p("ffn_up_exps.bias")),
                        biais(&p("ffn_down_exps.bias")));
    // Un modèle en clusters peut avoir des biais par expert : ils sont alors
    // découpés eux aussi, et les indexer par l'expert GLOBAL lirait la mauvaise
    // ligne. Plutôt qu'un résultat faux et silencieux, on refuse.
    if map.is_some() && (bg.is_some() || bu.is_some() || bd.is_some()) {
        panic!("couche {l} : biais d'experts + clusters — le découpage des biais \
n'est pas implémenté, et les indexer par l'expert global serait faux");
    }
    // Routage par TABLE (couches `hash_layer_count` de DeepSeek-V4) : la
    // sélection des experts n'y dépend pas du routeur appris mais de
    // l'identifiant du jeton. Le tenseur est en I32, et l'ignorer ferait router
    // ces trois couches au hasard du score — sans erreur, sans message.
    let tid2eid = match g.tensor(&p("ffn_gate_tid2eid.weight")) {
        Some(t) => {
            let n_k = t.dims.get(1).copied().unwrap_or(0) as usize;
            let v = g.dequant_i32(&p("ffn_gate_tid2eid.weight"));
            eprintln!("[moe] couche {l} : routage par TABLE tid2eid, {n_k} experts par jeton ({} jetons de vocabulaire)", if n_k > 0 { v.len() / n_k } else { 0 });
            Some(v)
        }
        None => None,
    };
    Some(Moe {
        routeur, routeur_biais,
        biais_gate: bg, biais_up: bu, biais_down: bd,
        n_ff, gate, up, down, shexp, tid2eid,
        couche: l, numeros, n_expert_global: n_expert, local: map,
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
            Dequant(t) => crate::list::octets_grille(t),
        }
    }

    /// Produit matrice-vecteur sur une source **sans noyau** : déquantifie
    /// chaque super-bloc de 256 poids et accumule en f32.
    ///
    /// Le travail est découpé par LIGNES de sortie entre `n_fils` fils : les
    /// super-blocs d'une ligne sont indépendants, et la déquantification domine
    /// le coût (recherches dans les grilles), donc le parallélisme paie.
    fn matvec_dequant(&self, loc: usize, t: u32, x: &[f32], out: &mut [f32], n_fils: usize) {
        let taille = crate::list::octets_grille(t);
        assert!(self.n_in % 256 == 0, "largeur {} non multiple de 256", self.n_in);
        // Le noyau lit `x[j]` jusqu'à `n_in` : une activation plus COURTE
        // dépasserait en silence. Plus longue est normal — l'appelant passe son
        // tampon de travail entier (12 288 valeurs pour la descente d'un expert
        // de 2 048 entrées) et seules les `n_in` premières sont lues.
        assert!(x.len() >= self.n_in, "expert de type {} : activation de {} valeurs \
pour une projection de {} entrées × {} sorties", crate::gguf::Gguf::nom_type(t),
                x.len(), self.n_in, self.n_out);
        let x = &x[..self.n_in];
        let nb = self.n_in / 256;
        // Le pointeur vient d'un mmap qui vit plus longtemps que l'appel ; il
        // est transmis comme entier pour traverser `thread::scope` sans
        // `unsafe impl Send`.
        let base = unsafe { self.base.add(loc * self.n_out * nb * taille) } as usize;
        let n_out = self.n_out;
        let n_in = self.n_in;
        let travail = move |o0: usize, o1: usize, out: &mut [f32]| {
            // Un tampon par FIL, réutilisé pour tous les blocs : c'est ce qui
            // fait la différence entre 2,5 µs et 0,3 µs par super-bloc.
            let mut valeurs = vec![0f32; 256];
            for o in o0..o1 {
                let mut acc = 0f32;
                for b in 0..nb {
                    let p = unsafe { (base as *const u8).add((o * nb + b) * taille) };
                    let bloc = unsafe { std::slice::from_raw_parts(p, taille) };
                    crate::list::dequant_grille_dans(t, bloc, &mut valeurs);
                    let lo = b * 256;
                    let hi = (lo + 256).min(n_in);
                    let mut s = 0f32;
                    for j in lo..hi { s += valeurs[j - lo] * x[j]; }
                    acc += s;
                }
                // `out` est la TRANCHE de ce fil : l'indexer par le numéro de
                // ligne GLOBAL lève « len is 256 but the index is 256 » dès le
                // deuxième fil. Le premier fil (o0 = 0) passait, ce qui rendait
                // le bug dépendant du nombre de fils.
                out[o - o0] = acc;
            }
        };
        let n_fils = n_fils.clamp(1, n_out.max(1));
        if n_fils <= 1 {
            travail(0, n_out, out);
            return;
        }
        let par = n_out.div_ceil(n_fils);
        std::thread::scope(|sc| {
            let mut reste = out;
            let mut o0 = 0usize;
            let mut poignees = Vec::new();
            while o0 < n_out {
                let o1 = (o0 + par).min(n_out);
                let (tranche, reste2) = reste.split_at_mut(o1 - o0);
                reste = reste2;
                poignees.push(sc.spawn(move || travail(o0, o1, tranche)));
                o0 = o1;
            }
            for p in poignees { let _ = p.join(); }
        });
    }

    /// Demande au noyau de lancer la lecture de l'expert `e` **en avance**.
    ///
    /// Le routeur choisit ses `k` experts avant tout calcul : on connaît donc
    /// les plages à lire une couche entière à l'avance. Les demander d'un coup
    /// laisse le noyau paralléliser ses lectures de pages, au lieu de les subir
    /// une par une au fil du calcul.
    fn prelire_expert(&self, e: usize) {
        let octets = self.n_out * self.nb * self.pas();
        let p = unsafe { self.base.add(e * octets) };
        crate::gguf::prelire(p, octets);
    }

    /// Octets bruts de l'expert `e` (tels qu'ils sont dans le fichier) : c'est
    /// ce qu'il faut copier en VRAM pour que le noyau y travaille.
    fn blocs_expert(&self, e: usize) -> &[u8] {
        let octets = self.n_out * self.nb * self.pas();
        let p = unsafe { self.base.add(e * octets) };
        unsafe { std::slice::from_raw_parts(p, octets) }
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
    /// Une vue par fichier porteur d'experts. Un GGUF ordinaire n'en a qu'une ;
    /// un modèle en clusters en a une par `cluster-XX.gguf`, chacune ne
    /// contenant que ses `experts_par_cluster` lignes.
    pub gate: Vec<Vue4>,
    pub up: Vec<Vue4>,
    pub down: Vec<Vue4>,
    /// Couche dont ce mélange fait partie (pour le mapping).
    pub couche: usize,
    /// Numéro de cluster de chaque vue de `gate`/`up`/`down`. L'identifiant du
    /// mapping est un NUMÉRO ; sa place dans le `Vec` dépend de ce que ce nœud a
    /// chargé. Les confondre marchait tant que les huit clusters étaient là —
    /// et sortait du tableau dès qu'un nœud n'en portait qu'un.
    pub numeros: Vec<usize>,
    /// Nombre d'experts GLOBAUX : c'est lui qu'indexe le routeur, et lui seul.
    pub n_expert_global: usize,
    /// Mapping global → (fichier, ligne) quand le modèle est en clusters.
    pub local: Option<&'static crate::clusters::Mapping>,
    /// Expert partagé, toujours actif (certains modèles seulement).
    pub shexp: Option<(Vue4, Vue4, Vue4)>,
    /// Table `ffn_gate_tid2eid.weight` (`[vocabulaire × k]`, entiers 32 bits) :
    /// le routage des `hash_layer_count` premières couches de DeepSeek-V4 est une
    /// fonction de l'identifiant du jeton, pas d'un score. `None` partout
    /// ailleurs.
    pub tid2eid: Option<Vec<i32>>,
}

impl Moe {
    /// Où trouver l'expert GLOBAL `e` : `(vue, ligne locale)`. `None` signifie
    /// que cet expert n'est pas dans ce nœud — ce n'est pas une erreur, c'est
    /// le principe même du découpage.
    #[inline]
    pub fn ou(&self, e: usize) -> Option<(usize, usize)> {
        match self.local {
            None => if e < self.n_expert_global { Some((0, e)) } else { None },
            Some(m) => {
                let (cluster, ligne) = m.ou(self.couche, e)?;
                // Le cluster de l'expert n'est pas forcément chargé ici : c'est
                // exactement ce que veut dire « nœud partiel », et ce n'est pas
                // une erreur.
                let k = self.numeros.iter().position(|c| *c == cluster)?;
                Some((k, ligne))
            }
        }
    }
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

/// Construit une matrice int8 : **une échelle par bloc de 32** (`DRAVE_Q8_BLOCS=1`,
/// la disposition de Q8_0) ou une par ligne (défaut historique).
///
/// L'hypothèse testée : si le 6 bits bat notre int8, c'est peut-être grâce à ses
/// échelles par bloc de 32 et non grâce à ses deux bits supplémentaires.
fn construire_q8(w: &[f32], n_out: usize, n_in: usize) -> DenseQ8 {
    if std::env::var("DRAVE_Q8_BLOCS").is_ok() && n_in % 32 == 0 {
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
        // scalaire dense (pull). Le croisement mesuré est à 22 %
        // (`seuil_push = 0.22`, `reports/rapport-croisement-push-pull.md`).
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
            // `DRAVE_SANS_EMPRUNT=1` force la reconstruction : c'est ce qui permet
            // de comparer nos deux schémas d'échelle à la référence empruntée.
            let emprunt = keep >= 1.0 && std::env::var("DRAVE_SANS_EMPRUNT").is_err();
            match (emprunt, g.q8_blocks(name)) {
                (true, Some((buf, nb))) =>
                    (None, Some(unsafe { DenseQ8::emprunter_q8(buf.as_ptr(), n_out, n_in, nb) }), None),
                _ => (None, Some(construire_q8(&w, n_out, n_in)), None),
            }
        } else if auto {
            let emprunt = keep >= 1.0 && std::env::var("DRAVE_SANS_EMPRUNT").is_err();
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

/// Cache VRAM des experts MoE (MXFP4), à éviction LRU.
///
/// Pourquoi un cache et pas un simple déport : un expert pèse 4,4 Mo et
/// gpt-oss en a 4 608 (36 couches × 128) — 60 Go, la VRAM n'en tient pas le
/// quart. Mais un expert SÉLECTIONNÉ est réutilisé d'un jeton à l'autre : c'est
/// exactement ce qu'un cache attrape. La mesure d'activation
/// (`reports/rapport-localite-activation.md`) dit qu'un préchargement STATIQUE
/// ne paie pas ; une résidence dynamique, si.
pub struct CacheExperts {
    /// Une entrée par (couche, expert) : ses trois matrices (gate, up, down).
    cartes: std::collections::HashMap<(usize, usize), (crate::gpu::MatriceGpu,
                                                       crate::gpu::MatriceGpu,
                                                       crate::gpu::MatriceGpu, u64)>,
    pub octets: usize,
    pub budget: usize,
    pub demandes: u64,
    pub manques: u64,
    pub evictions: u64,
    pub octets_envoyes: u64,
    ticks: u64,
}

impl CacheExperts {
    pub fn nouveau(budget: usize) -> Self {
        CacheExperts { cartes: std::collections::HashMap::new(), octets: 0, budget,
                       demandes: 0, manques: 0, evictions: 0, octets_envoyes: 0, ticks: 0 }
    }

    pub fn taux(&self) -> f64 {
        if self.demandes == 0 { 0.0 } else { 100.0 * (1.0 - self.manques as f64 / self.demandes as f64) }
    }

    /// Les trois matrices de `(couche, expert)` en VRAM, envoyées si besoin.
    /// Évince les entrées les moins récemment utilisées tant que le budget est
    /// dépassé. `None` si même une entrée seule ne tient pas dans le budget.
    fn obtenir<'a>(&'a mut self, machine: &crate::gpu::Gpu, l: usize, e: usize,
                   gate: &Vue4, up: &Vue4, down: &Vue4)
        -> Option<(&'a crate::gpu::MatriceGpu, &'a crate::gpu::MatriceGpu,
                   &'a crate::gpu::MatriceGpu)> {
        self.ticks += 1;
        let t = self.ticks;
        let cle = (l, e);
        self.demandes += 1;
        if !self.cartes.contains_key(&cle) {
            self.manques += 1;
            let octets = 3 * gate.n_out * gate.nb * 17;
            while self.octets + octets > self.budget && !self.cartes.is_empty() {
                let victime = self.cartes.iter().min_by_key(|(_, v)| v.3).map(|(k, _)| *k)?;
                if let Some((g, u, d, _)) = self.cartes.remove(&victime) {
                    self.octets = self.octets
                        .saturating_sub(g.octets_poids + u.octets_poids + d.octets_poids);
                    self.evictions += 1;
                }
            }
            if self.octets + octets > self.budget { return None; }
            let mg = machine.charger_mxfp4(gate.blocs_expert(e), gate.n_out, gate.nb)?;
            let mu = machine.charger_mxfp4(up.blocs_expert(e), up.n_out, up.nb)?;
            let md = machine.charger_mxfp4(down.blocs_expert(e), down.n_out, down.nb)?;
            self.octets += mg.octets_poids + mu.octets_poids + md.octets_poids;
            self.octets_envoyes +=
                (mg.octets_poids + mu.octets_poids + md.octets_poids) as u64;
            self.cartes.insert(cle, (mg, mu, md, t));
        }
        let v = self.cartes.get_mut(&cle)?;
        v.3 = t;
        Some((&v.0, &v.1, &v.2))
    }
}

/// MLA (attention latente) : les poids d'une couche, lus en f32. Le cache n'est
/// PAS `(n_kv, ctx, head_dim)` mais **une seule tête latente** par couche —
/// `kv_lora` valeurs, plus les `qk_rope` composantes tournées. C'est tout
/// l'intérêt de MLA : le cache ne dépend plus du nombre de têtes.
pub struct Mla {
    pub q_a: Vec<f32>,      // [h, q_lora]
    pub q_a_norm: Vec<f32>, // [q_lora]
    pub q_b: Vec<f32>,      // [q_lora, nh*(qkn+qkr)]
    pub kv_a: Vec<f32>,     // [h, kv_lora+qkr]
    pub kv_a_norm: Vec<f32>,// [kv_lora]
    /// Disposition **combinée** : `[kv_lora, nh*(qkn+vd)]`, une matrice par
    /// tête concaténée. Vide quand le modèle utilise la disposition séparée
    /// (`attn_k_b` + `attn_v_b`), qui est celle de Kimi-K2.7 et DeepSeek-V3/V4.
    pub kv_b: Vec<f32>,
    /// Disposition **séparée** : `k_b` `[nh, kv_lora, qkn]` et `v_b`
    /// `[nh, kv_lora, vd]` (convention numpy, le plus lent d'abord).
    pub k_b: Option<Vec<f32>>,
    pub v_b: Option<Vec<f32>>,
    pub wo: Vec<f32>,       // [nh*vd, h]
    pub ffn_norm: Vec<f32>, // [h]
    pub gate: Vec<f32>,     // [h, ffn]
    pub up: Vec<f32>,       // [h, ffn]
    pub down: Vec<f32>,     // [ffn, h]
    pub attn_norm: Vec<f32>,// [h]
    pub q_lora: usize, pub kv_lora: usize, pub qkr: usize, pub qkn: usize,
    pub vd: usize, pub nh: usize, pub ffn: usize,
    /// Epsilon de normalisation du modèle : la MLA normalise `q_a` et `c_kv`
    /// AVANT de les remonter, et l'oublier donnerait des scores faux d'un
    /// facteur qui dépend de la norme de l'état — donc invisibles sur un jeton
    /// et fatals sur une séquence.
    pub eps: f32,
}

/// Produit matrice-vecteur en f32 : `y[o] = Σ_i w[o*n_in + i] * x[i]`.
/// Les poids MLA sont rangés ligne par ligne, comme les tenseurs GGUF F32.
fn matvec_f32(w: &[f32], x: &[f32], n_in: usize, n_out: usize, y: &mut [f32]) {
    for o in 0..n_out {
        let ligne = &w[o * n_in..(o + 1) * n_in];
        let mut acc = 0f32;
        for i in 0..n_in { acc += ligne[i] * x[i]; }
        y[o] = acc;
    }
}

/// f32 → f16 (IEEE 754 binary16), pour les échelles par bloc de la trace v3.
/// Arrondi au plus proche ; les dénormalisés deviennent 0 (des échelles nulles le
/// sont déjà). Aucune dépendance : le moteur est en `std` seul.
pub fn f16_depuis_f32(x: f32) -> u16 {
    let b = x.to_bits();
    let s = ((b >> 16) & 0x8000) as u16;
    let mut e = ((b >> 23) & 0xff) as i32 - 127 + 15;
    let mut m = b & 0x007f_ffff;
    if e <= 0 { return s; }
    if e >= 31 { return s | 0x7c00; }
    m += 0x1000;                                   // arrondi au bit 13
    if m & 0x0080_0000 != 0 { m = 0; e += 1; if e >= 31 { return s | 0x7c00; } }
    s | ((e as u16) << 10) | ((m >> 13) as u16)
}

/// f16 → f32, l'inverse exact de la fonction ci-dessus (dénormalisés compris).
pub fn f32_depuis_f16(h: u16) -> f32 {
    let s = ((h >> 15) & 1) as u32;
    let e = ((h >> 10) & 0x1f) as u32;
    let m = (h & 0x3ff) as u32;
    let bits = if e == 0 {
        if m == 0 { s << 31 } else {
            let (mut e2, mut m2) = (127 - 15 + 1i32, m);
            while m2 & 0x400 == 0 { m2 <<= 1; e2 -= 1; }
            (s << 31) | ((e2 as u32) << 23) | ((m2 & 0x3ff) << 13)
        }
    } else if e == 31 { (s << 31) | 0x7f80_0000 | (m << 13) }
    else { (s << 31) | ((e + 127 - 15) << 23) | (m << 13) };
    f32::from_bits(bits)
}

/// Trace du **flux d'activation** : par (couche, position), la liste des
/// neurones actifs — indice, valeur — avec son échelle. C'est le cœur de la
/// vision mis sur disque : on peut rejouer, comparer, et c'est aussi le format
/// qu'un nœud distant devrait recevoir pour continuer le calcul.
pub struct TraceFlux {
    /// Version écrite : 2 (indices par écarts, valeurs i16 — SANS PERTE) ou
    /// 3 (`DRAVE_TRACE_BLOCS=1` : valeurs i8 et une échelle f16 par bloc de 32
    /// canaux, ~22 % plus petit, avec perte).
    pub version: u16,
    /// Nombre de canaux par bloc d'échelle en v3.
    pub bloc: usize,
    pub fichier: std::io::BufWriter<std::fs::File>,
    /// Couches à tracer (toutes si vide).
    pub couches: Vec<usize>,
    pub octets: u64,
    pub enregistrements: u64,
    pub actifs: u64,
}

impl TraceFlux {
    pub fn nouveau(chemin: &str, couches: Vec<usize>, hidden: usize, n_layer: usize)
        -> std::io::Result<Self> {
        use std::io::Write;
        let mut f = std::io::BufWriter::new(std::fs::File::create(chemin)?);
        f.write_all(b"DRVF")?;
        // Version 2 par défaut : indices par ÉCARTS, valeurs i16 — sans perte.
        // Version 3 sur `DRAVE_TRACE_BLOCS=1` : en plus, valeurs i8 et une échelle
        // f16 par bloc de 32 canaux (l'étude de compacité annonce −22 % de plus,
        // au prix de la fidélité du rejeu).
        let version: u16 = if std::env::var("DRAVE_TRACE_BLOCS").is_ok() { 3 } else { 2 };
        f.write_all(&version.to_le_bytes())?;
        f.write_all(&(n_layer as u32).to_le_bytes())?;
        f.write_all(&(hidden as u32).to_le_bytes())?;
        // 14 octets d'en-tête, pas 16 : la comptabilité disait 16 depuis le
        // début et personne ne s'en apercevait (2 octets sur 132 Mo).
        Ok(TraceFlux { version, bloc: 32, fichier: f, couches, octets: 14,
                       enregistrements: 0, actifs: 0 })
    }

    /// Une liste : ce qui est réellement poussé dans la couche.
    ///
    /// Le corps est construit AVANT l'en-tête, parce que chaque version a son
    /// compte : `n` est le nombre d'entiers i16 (v1/v2) ou de valeurs i8 (v3), et
    /// la v3 ajoute ses échelles de bloc. Écrire l'en-tête d'abord obligeait à
    /// connaître les deux comptes — et la première version de ce code les
    /// écrivait tous les deux, décalant tout le fichier de huit octets.
    pub fn ecrire(&mut self, couche: usize, pos: usize, actifs: &[i32], echelle: f32) {
        use std::io::Write;
        if !self.couches.is_empty() && !self.couches.contains(&couche) { return; }

        let (n, ech_liste, corps): (u32, f32, Vec<u8>) = if self.version == 3 {
            // v3 : une échelle f16 par bloc de 32 canaux, valeurs i8. L'échelle
            // par bloc borne l'erreur RELATIVE (celle par vecteur borne l'absolue,
            // catastrophique sur les canaux faibles) et permet un octet par valeur.
            let n_blocs = actifs.len().div_ceil(self.bloc);
            let mut echelles = vec![0f32; n_blocs];
            let mut idx: Vec<u32> = Vec::new();
            let mut val: Vec<i8> = Vec::new();
            for b in 0..n_blocs {
                let lo = b * self.bloc;
                let hi = (lo + self.bloc).min(actifs.len());
                let mut mb = 0f32;
                for &q in &actifs[lo..hi] {
                    let a = (q as f32 * echelle).abs();
                    if a > mb { mb = a; }
                }
                if mb == 0.0 { continue; }
                let ech = mb / 127.0;
                echelles[b] = ech;
                for (k, &q) in actifs[lo..hi].iter().enumerate() {
                    if q == 0 { continue; }
                    let v = (q as f32 * echelle / ech).round().clamp(-127.0, 127.0);
                    if v != 0.0 { idx.push((lo + k) as u32); val.push(v as i8); }
                }
            }
            let mut c = Vec::with_capacity(4 + n_blocs * 2 + idx.len() * 3);
            c.extend_from_slice(&(n_blocs as u32).to_le_bytes());
            for e in &echelles { c.extend_from_slice(&f16_depuis_f32(*e).to_le_bytes()); }
            let mut prev = 0u32;
            for (i, v) in idx.iter().zip(val.iter()) {
                let ecart = *i - prev;
                if ecart < 255 {
                    c.push(ecart as u8);
                } else {
                    c.push(255);
                    c.extend_from_slice(&i.to_le_bytes()[..2]);
                }
                c.push(*v as u8);
                prev = *i;
            }
            (idx.len() as u32, 0f32, c)
        } else {
            // v1 et v2 : les entiers i16 du moteur, tels quels.
            let liste: Vec<(u32, i16)> = actifs.iter().enumerate()
                .filter(|(_, &v)| v != 0)
                .map(|(i, &v)| (i as u32, v.clamp(-32767, 32767) as i16))
                .collect();
            let mut c = Vec::with_capacity(6 * liste.len());
            let mut prev = 0u32;
            for (i, v) in &liste {
                if self.version == 1 {
                    c.extend_from_slice(&i.to_le_bytes());
                } else {
                    let ecart = *i - prev;
                    if ecart < 255 {
                        c.push(ecart as u8);
                    } else {
                        c.push(255);
                        c.extend_from_slice(&i.to_le_bytes()[..2]);
                    }
                    prev = *i;
                }
                c.extend_from_slice(&v.to_le_bytes());
            }
            (liste.len() as u32, echelle, c)
        };

        let _ = self.fichier.write_all(&(couche as u16).to_le_bytes());
        let _ = self.fichier.write_all(&(pos as u32).to_le_bytes());
        let _ = self.fichier.write_all(&n.to_le_bytes());
        let _ = self.fichier.write_all(&ech_liste.to_le_bytes());
        let _ = self.fichier.write_all(&corps);
        let octets_par_actif = if self.version == 3 { 2 } else if self.version == 1 { 6 } else { 3 };
        let octets_echelles = if self.version == 3 {
            4 + actifs.len().div_ceil(self.bloc) * 2
        } else { 0 };
        self.octets += 14 + octets_echelles as u64 + octets_par_actif as u64 * n as u64;
        self.enregistrements += 1;
        self.actifs += n as u64;
    }

    pub fn terminer(&mut self) {
        use std::io::Write;
        let _ = self.fichier.write_all(&0xFFFFu16.to_le_bytes());
        let _ = self.fichier.flush();
    }
}

/// Relit une trace de flux et rend, pour (couche, position), la liste
/// enregistrée. C'est le pendant du `TraceFlux` : ce qu'un nœud distant devrait
/// recevoir pour continuer le calcul, on sait déjà l'écrire — ici, on apprend à
/// le RELIRE et à repartir de là.
pub struct FluxRelecteur {
    /// (couche, position) -> (échelle, indices/valeurs)
    /// (couche, jeton global) → (échelle, paires) pour les versions 1 et 2 : les
    /// ENTIERS d'origine sont conservés, parce que le rejeu par LOTS les réinjecte
    /// tels quels (chemin exact, sans déquantifier-requantifier).
    pub listes: std::collections::HashMap<(u16, u32), (f32, Vec<(u32, i16)>)>,
    /// Version 3 : les valeurs sont des f32 (i8 × échelle f16 de bloc), il n'y a
    /// plus d'entiers d'origine. Le rejeu JETON PAR JETON les accepte ; le rejeu
    /// par lots, non — et il le dira au lieu de compter des listes manquantes
    /// sans explication.
    pub listes_blocs: std::collections::HashMap<(u16, u32), Vec<(u32, f32)>>,
    pub servies: u64,
    pub manquantes: u64,
}

impl FluxRelecteur {
    pub fn lire(chemin: &str) -> std::io::Result<Self> {
        use std::io::Read;
        let mut f = std::fs::File::open(chemin)?;
        // En-tête : magie (4) + version (2) + n_layer (4) + hidden (4) = 14 octets.
        // Lire 16 décalait tout de deux octets et faisait échouer la dernière
        // lecture — un « failed to fill whole buffer » qui ne dit pas pourquoi.
        let mut entete = [0u8; 14];
        f.read_exact(&mut entete)?;
        if &entete[0..4] != b"DRVF" {
            return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
                                           "ce n'est pas une trace DRVF"));
        }
        let version = u16::from_le_bytes([entete[4], entete[5]]);
        if version != 1 && version != 2 && version != 3 {
            return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
                format!("trace DRVF en version {version} : ce lecteur lit la 1, la 2 et la 3")));
        }
        let mut listes = std::collections::HashMap::new();
        let mut listes_blocs = std::collections::HashMap::new();
        loop {
            let mut tete = [0u8; 2];
            if f.read_exact(&mut tete).is_err() { break; }          // fin de fichier
            let couche = u16::from_le_bytes(tete);
            if couche == 0xFFFF { break; }
            let mut corps = [0u8; 12];
            f.read_exact(&mut corps)?;
            let pos = u32::from_le_bytes([corps[0], corps[1], corps[2], corps[3]]);
            let n = u32::from_le_bytes([corps[4], corps[5], corps[6], corps[7]]);
            let echelle = f32::from_le_bytes([corps[8], corps[9], corps[10], corps[11]]);
            let mut paires: Vec<(u32, i16)> = Vec::with_capacity(n as usize);
            if version == 3 {
                let mut paires3: Vec<(u32, f32)> = Vec::with_capacity(n as usize);
                // v3 : nombre de blocs u32 · échelles f16 · paires (écart u8, i8)
                let mut nb = [0u8; 4];
                f.read_exact(&mut nb)?;
                let n_blocs = u32::from_le_bytes(nb) as usize;
                let mut eb = vec![0u8; n_blocs * 2];
                f.read_exact(&mut eb)?;
                let echelles: Vec<f32> = (0..n_blocs).map(|k|
                    f32_depuis_f16(u16::from_le_bytes([eb[k*2], eb[k*2+1]]))).collect();
                let mut prev = 0u32;
                for _ in 0..n as usize {
                    let mut d = [0u8; 1];
                    f.read_exact(&mut d)?;
                    let i = if d[0] == 255 {
                        let mut a = [0u8; 2];
                        f.read_exact(&mut a)?;
                        u16::from_le_bytes(a) as u32
                    } else { prev + d[0] as u32 };
                    prev = i;
                    let mut b = [0u8; 1];
                    f.read_exact(&mut b)?;
                    let q = b[0] as i8 as f32;
                    let ech = echelles.get(i as usize / 32).copied().unwrap_or(0.0);
                    // La valeur rejouée est un f32 : le format v3 ne stocke plus
                    // d'entiers d'origine, il stocke des activations déquantifiées.
                    paires3.push((i, q * ech));
                }
                listes_blocs.insert((couche, pos), paires3);
                continue;
            }
            if version == 1 {
                let mut octets = vec![0u8; n as usize * 6];
                f.read_exact(&mut octets)?;
                for k in 0..n as usize {
                    let o = k * 6;
                    let i = u32::from_le_bytes([octets[o], octets[o+1], octets[o+2], octets[o+3]]);
                    let v = i16::from_le_bytes([octets[o+4], octets[o+5]]);
                    paires.push((i, v));
                }
            } else {
                // v2 : écart d'un octet (255 = les deux octets suivants portent
                // l'indice absolu), puis la valeur i16. Lu octet par octet : le
                // corps n'a pas de longueur fixe, donc pas de tampon à dimensionner.
                let mut prev = 0u32;
                for _ in 0..n as usize {
                    let mut d = [0u8; 1];
                    f.read_exact(&mut d)?;
                    let i = if d[0] == 255 {
                        let mut a = [0u8; 2];
                        f.read_exact(&mut a)?;
                        u16::from_le_bytes(a) as u32
                    } else { prev + d[0] as u32 };
                    prev = i;
                    let mut b = [0u8; 2];
                    f.read_exact(&mut b)?;
                    paires.push((i, i16::from_le_bytes(b)));
                }
            }
            listes.insert((couche, pos), (echelle, paires));
        }
        Ok(FluxRelecteur { listes, listes_blocs, servies: 0, manquantes: 0 })
    }

    /// Écrit dans `dst` l'activation DÉQUANTIFIÉE de la liste enregistrée.
    /// C'est exactement ce qu'un nœud recevant le flux ferait avant de continuer.
    pub fn appliquer(&mut self, couche: usize, pos: usize, dst: &mut [f32]) {
        let cle = (couche as u16, pos as u32);
        if let Some(paires) = self.listes_blocs.get(&cle) {
            for v in dst.iter_mut() { *v = 0.0; }
            for &(i, v) in paires {
                if (i as usize) < dst.len() { dst[i as usize] = v; }
            }
            self.servies += 1;
            return;
        }
        match self.listes.get(&cle) {
            Some((echelle, paires)) => {
                for v in dst.iter_mut() { *v = 0.0; }
                for &(i, q) in paires {
                    if (i as usize) < dst.len() { dst[i as usize] = q as f32 * *echelle; }
                }
                self.servies += 1;
            }
            None => self.manquantes += 1,
        }
    }
}

pub struct Model {
    pub g: Gguf,
    pub cfg: Cfg,
    pub layers: Vec<Layer>,
    pub out_norm: Vec<f32>,
    pub pool: Pool,
    /// cache KV, par couche : `[n_kv_head × ctx × head_dim]`, en f32 ou quantifié
    /// Caches KV, un par couche (pub : le tableau de bord `--options-actives`
    /// montre ce que le moteur utilise vraiment — et c'est là qu'on voit si
    /// `DRAVE_KV_K_F32` ou `DRAVE_KV_K_F16` a réellement pris).
    pub kv: Vec<KvCache>,
    pub ctx: usize,
    pub events: u64,
    /// **Paires** (poids × activation) effectivement multipliées, par
    /// provenance : 0 = attention, 1 = experts routés, 2 = partagé (FFN dense,
    /// expert partagé, tête).
    ///
    /// Pourquoi une seconde mesure à côté des `events` : les chemins qui
    /// **déquantifient** (IQ, formats sans noyau) et le chemin MLA en f32 ne
    /// construisent aucune liste, donc ne produisent aucun événement — le
    /// rapport annonçait « 0 événement » pour des modèles qui calculaient des
    /// milliards de produits. Une paire est ce qu'on **paie** : un chemin en
    /// listes ne paie que ses poids non nuls, un chemin dense paie la matrice
    /// entière, et l'écart entre les deux est exactement ce que le croisement
    /// push/pull de 22 % arbitre (`reports/rapport-croisement-push-pull.md`).
    pub paires: [u64; 3],
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
    /// **Trace de routage** (`DRAVE_TRACE_EXPERTS=chemin`) : une ligne par
    /// (couche, jeton) avec les indices des experts retenus. C'est la matière
    /// première du découpage en clusters : les compteurs par expert disent
    /// lesquels sont chauds, la trace dit lesquels sont chauds ENSEMBLE.
    pub trace_experts: Option<std::io::BufWriter<std::fs::File>>,
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
    /// deux architectures se croisent à **22 %** de densité
    /// (`reports/rapport-croisement-push-pull.md` : le seuil est passé de 0,15 à
    /// 0,22 après la mesure) ; on bascule un peu au-dessus pour absorber la
    /// marge d'erreur.
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
    /// **Normes des lignes de la tête** `||w_i||`, calculées une fois, et
    /// l'ordre des lignes par norme DÉCROISSANTE. C'est ce qui rend une
    /// restriction de tête *garantie* : pour tout jeton `i`, `|w_i · h| ≤
    /// ||w_i|| · ||h||`, donc aucune ligne de norme plus petite que
    /// `meilleur_logit / ||h||` ne peut battre le meilleur logit déjà calculé.
    /// On étend la liste par paliers jusqu'à ce que la borne conclue — et
    /// lorsqu'elle ne conclut pas, on finit par tout calculer, ce qui est la
    /// réponse juste plutôt qu'une réponse rapide et fausse.
    pub normes_tete: Option<Vec<f32>>,
    pub ordre_normes: Option<Vec<u32>>,
    /// Liste de jetons candidats pour la tête garantie (`--tete-garantie`).
    pub tete_garantie: Option<Vec<u32>>,
    /// Compteurs de la tête garantie : lignes calculées et nombre de jetons.
    pub tete_calculees: u64,
    pub tete_appels_g: u64,
    /// Chemin GPU : la tête et les projections y résident en permanence. Les
    /// poids ne traversent le bus qu'une fois ; seules les activations font
    /// l'aller-retour à chaque jeton.
    pub tete_gpu: Option<crate::gpu::MatriceGpu>,
    /// Tête de sortie en 4 bits (poids liés au plafond d'embedding). C'est la
    /// plus grosse matrice du modèle — 151 936 × 896 — donc le poste où le
    /// demi-octet par poids rapporte le plus.
    pub head4: Option<DenseQ4>,
    /// Tokens sur lesquels la tête de sortie est calculée. `None` = tout le
    /// vocabulaire.
    ///
    /// Mesuré : le vocabulaire d'une langue tient en **13 %** des tokens (19 793
    /// sur 151 936 pour 3 M de jetons français, et la couverture croît si
    /// lentement qu'atteindre 50 % demanderait des milliards de jetons). La tête
    /// pèse par ailleurs 36 % du trafic par jeton sur V4.1. Restreindre la boucle
    /// aux lignes utiles divise donc ce poste par sept.
    ///
    /// **Ne s'applique pas à la perplexité** : le softmax normalise sur tout le
    /// vocabulaire, et retirer des termes en retire aussi de la masse au
    /// dénominateur — mesuré, la perplexité *baisse* artificiellement (24,31
    /// contre 25,37). Elle n'est alors plus comparable à rien.
    pub tete_restreinte: Option<Vec<u32>>,
    /// Vrai quand la tête déportée est en Q6_K (`proj_q6k_warp`) et non en
    /// Q8_0 (`tete_q8_warp`) : les deux noyaux ne rendent pas la même chose —
    /// celui de Q8_0 ne multiplie PAS par l'échelle d'activation, celui de Q6_K
    /// l'applique.
    pub tete_gpu_q6k: bool,
    /// Miroir VRAM du cache KV, une entrée par couche (`DRAVE_GPU_KV=1`).
    /// Un miroir VRAM par couche, avec l'index du périphérique qui le porte :
    /// deux cartes se partagent les couches (16 Go chacune).
    pub kv_gpu: Option<Vec<(usize, crate::gpu::KvGpu)>>,
    /// Tranches de clés du noyau d'attention, réutilisées d'un jeton à l'autre.
    pub attn_gpu_part: Vec<f32>,
    /// Compteur de jetons tracés : `position` dans la trace est ce compteur, et
    /// non la position DANS la fenêtre. Sans cela, une exécution à plusieurs
    /// fenêtres réécrivait les mêmes clés (couche, position) et le rejeu
    /// rejouait la mauvaise — mesuré : perplexité 356 694 au lieu de 17,43.
    pub jeton_trace: u64,
    /// Trace du flux d'activation (`--trace-flux`).
    pub trace: Option<TraceFlux>,
    /// Relecture d'une trace : les activations enregistrées REMPLACENT celles
    /// calculées (`--flux-forcer`). Si le rejeu redonne les mêmes logits, alors
    /// une liste suffit à continuer le calcul — c'est le contrat de la phase 3.
    pub flux_force: Option<FluxRelecteur>,
    /// Embedding imposé pour le prochain appel à `forward` : c'est le point
    /// d'injection des vecteurs d'image (ou de tout autre vecteur), le seul
    /// ajout d'architecture que la vision demande au moteur — `forward` partait
    /// toujours de `token_embd`.
    pub emb_imposee: Option<Vec<f32>>,
    /// États imposés pour un LOT entier (`forward_lot`) : `t × hidden`, aplati.
    ///
    /// C'est le pendant de `emb_imposee` pour le préremplissage réparti : un nœud
    /// qui reçoit N états d'un coup — au lieu des N identifiants de jetons —
    /// reprend le calcul à sa première couche sans repasser par les embeddings.
    /// Sans ce champ, le transport devait payer un aller-retour PAR JETON.
    pub emb_imposee_lot: Option<Vec<f32>>,
    /// Première et dernière couche PORTÉES par ce modèle (exclue). Un nœud
    /// distant ne charge que sa plage : c'est le découpage de la phase 3.
    pub couche_debut: usize,
    pub couche_fin: usize,
    /// Nœud **intermédiaire** du transport : sa plage peut aller jusqu'à la
    /// dernière couche, il n'en rend pas moins le flux résiduel BRUT.
    ///
    /// Sans ce drapeau, un nœud moteur qui porte les couches `N/2..N` normait le
    /// flux (`couche_fin >= n_layer`) et le pilote le normait une SECONDE fois :
    /// perplexité répartie **798,3** au lieu de **18,2**. La norme finale est
    /// appliquée par le nœud qui possède la tête de sortie — une seule fois.
    pub flux_brut: bool,
    /// Couches MLA, si le modèle en est un (`attn_kv_a_mqa` présent).
    pub mla: Option<Vec<Mla>>,
    /// Cache LATENT par couche : `c_kv` (kv_lora) et `k_rope` (qkr) par position.
    pub mla_cache: Vec<(Vec<f32>, Vec<f32>)>,
    /// Cache VRAM des experts MoE (`DRAVE_GPU_EXPERTS=1`).
    pub cache_experts: Option<CacheExperts>,
    /// Taille du lot de PRÉREMPLISSAGE en inférence (1 = jeton par jeton).
    /// Le préremplissage par lots n'était branché que sur la perplexité : une
    /// invite de 4 000 jetons se payait donc jeton par jeton en génération.
    pub lot: usize,
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
    /// Longueur LOGIQUE (positions adressables par le moteur).
    pub ctx: usize,
    /// `DRAVE_KV_F16=1` : arrondir clés et valeurs en f16 avant quantification.
    pub f16_avant: bool,
    /// Attribution de l'écart int8 : `DRAVE_KV_K_F32=1` garde les CLÉS en f32
    /// (l'erreur qui passe par les scores disparaît), `DRAVE_KV_V_F32=1` garde
    /// les VALEURS (celle de la somme pondérée). Le miroir GPU n'est pas
    /// utilisable dans ces variantes : il suppose une disposition homogène.
    pub k_f32: bool,
    pub v_f32: bool,
    /// Positions réellement allouées, doublées à la demande. Réserver `ctx`
    /// positions d'un coup coûtait 25,77 Go à contexte 1 M pour 512 jetons
    /// écrits (mesuré) ; c'est la même pagination que le miroir VRAM, côté hôte.
    pub cap: usize,
    pub hd: usize,
    kf: Vec<f32>,
    vf: Vec<f32>,
    /// `DRAVE_KV_K_F16=1` : les CLÉS sont stockées en f16, sans quantification
    /// par bloc. Deux octets par valeur — plus que l'int8 (1,125 avec son échelle)
    /// mais bien moins que le f32 (4) — et une précision RELATIVE de 2⁻¹¹ par
    /// valeur, là où l'int8 à échelle par bloc a une erreur ABSOLUE de bloc/254
    /// qui écrase les petits canaux. C'est le « meilleur quantificateur de clés »
    /// que la feuille de route appelle, sans rotation ni échelle par tête.
    kp: Vec<u16>,
    pub k_f16: bool,
    /// Quantifié : un octet par valeur en 8 bits, **deux nibbles par octet en
    /// 4 bits** (même disposition que Q4_0/MXFP4 : nibble bas = indice pair).
    kq: Vec<u8>,
    vq: Vec<u8>,
    /// Échelles **par bloc de 32**, comme Q8_0 — et non une par vecteur : c'est
    /// ce qui explique l'écart mesuré avec llama.cpp (+5,2 % de perplexité
    /// contre +0,8 % pour son cache q8_0).
    sk: Vec<f32>,
    sv: Vec<f32>,
    nb: usize,
}

impl KvCache {
    pub fn new(bits: u32, n_kv: usize, ctx: usize, hd: usize) -> Self {
        let bits = if bits >= 32 { 32 } else if bits > 4 { 8 } else { 4 };
        if bits < 32 {
            assert!(hd % 2 == 0, "4 bits empaquetés : dimension de tête paire requise");
        }
        let nb = hd.div_ceil(32).max(1);
        let (k_f32, v_f32) = (std::env::var("DRAVE_KV_K_F32").is_ok(),
                              std::env::var("DRAVE_KV_V_F32").is_ok());
        let k_f16 = bits < 32 && std::env::var("DRAVE_KV_K_F16").is_ok();
        let mut c = KvCache { bits, n_kv, ctx, cap: 0, hd,
                              f16_avant: std::env::var("DRAVE_KV_F16").is_ok(), k_f32, v_f32,
                              k_f16, kp: Vec::new(),
                              kf: Vec::new(), vf: Vec::new(),
                              kq: Vec::new(), vq: Vec::new(), sk: Vec::new(), sv: Vec::new(),
                              nb };
        c.assurer(ctx.min(1024));
        c
    }

    /// Garantit `besoin` positions allouées (doublement, avec recopie : les
    /// positions déjà écrites le restent). Chaque tête KV a son bloc contigu,
    /// donc la recopie se fait tête par tête.
    pub fn assurer(&mut self, besoin: usize) {
        if besoin <= self.cap { return; }
        // ⚠️ `besoin > ctx` faisait BOUCLER SANS FIN : `cap` plafonne à `ctx` et la
        // condition reste vraie. Mesuré : une invite de 4 731 jetons avec
        // `--ctx 4608` tournait à ~1 700 % de CPU pendant plus de 22 minutes sans
        // jamais finir (livelock, pas ralentissement). Le même défaut avait été
        // corrigé côté GPU au sprint 2 (`kv_assurer`) ; le chemin CPU était resté.
        // On plafonne au contexte déclaré : le cache ne grandit pas au-delà, et
        // l'appelant voit la troncature par le message ci-dessous.
        let besoin = besoin.min(self.ctx);
        if besoin <= self.cap { return; }
        let mut cap = self.cap.max(1);
        while cap < besoin { cap = (cap * 2).min(self.ctx); }
        let hd = self.hd;
        let nb = self.nb;
        let pas = self.pas();
        let (n_kv, bits) = (self.n_kv, self.bits);
        let f32_k = bits >= 32 || self.k_f32;
        let f32_v = bits >= 32 || self.v_f32;
        if self.k_f16 {
            let mut kp = vec![0u16; n_kv * cap * hd];
            for h in 0..n_kv {
                let (a, b) = (h * self.cap * hd, h * cap * hd);
                let n = self.cap * hd;
                if !self.kp.is_empty() { kp[b..b + n].copy_from_slice(&self.kp[a..a + n]); }
            }
            self.kp = kp;
        }
        if f32_k || f32_v {
            let mut kf = if f32_k { vec![0f32; n_kv * cap * hd] } else { Vec::new() };
            let mut vf = if f32_v { vec![0f32; n_kv * cap * hd] } else { Vec::new() };
            for h in 0..n_kv {
                let (a, b) = (h * self.cap * hd, h * cap * hd);
                let n = self.cap * hd;
                if f32_k && !self.kf.is_empty() {
                    kf[b..b + n].copy_from_slice(&self.kf[a..a + n]);
                }
                if f32_v && !self.vf.is_empty() {
                    vf[b..b + n].copy_from_slice(&self.vf[a..a + n]);
                }
            }
            if f32_k { self.kf = kf; }
            if f32_v { self.vf = vf; }
        }
        if bits < 32 {
            let mut kq = vec![0u8; n_kv * cap * pas];
            let mut vq = vec![0u8; n_kv * cap * pas];
            let mut sk = vec![0f32; n_kv * cap * nb];
            let mut sv = vec![0f32; n_kv * cap * nb];
            for h in 0..n_kv {
                let (a, b) = (h * self.cap * pas, h * cap * pas);
                let n = self.cap * pas;
                kq[b..b + n].copy_from_slice(&self.kq[a..a + n]);
                vq[b..b + n].copy_from_slice(&self.vq[a..a + n]);
                let (sa, sb) = (h * self.cap * nb, h * cap * nb);
                sk[sb..sb + self.cap * nb].copy_from_slice(&self.sk[sa..sa + self.cap * nb]);
                sv[sb..sb + self.cap * nb].copy_from_slice(&self.sv[sa..sa + self.cap * nb]);
            }
            self.kq = kq;
            self.vq = vq;
            self.sk = sk;
            self.sv = sv;
        }
        self.cap = cap;
    }

    /// Octets par vecteur (tête, position) dans le tableau quantifié.
    #[inline]
    fn pas(&self) -> usize { if self.bits == 8 { self.hd } else { self.hd / 2 } }

    /// Octets réellement ALLOUÉS (diagnostic) : c'est ce que le processus
    /// réserve, pas ce que `ctx` laisse croire.
    pub fn octets(&self) -> u64 {
        (self.kf.len() + self.vf.len()) as u64 * 4
            + (self.kq.len() + self.vq.len()) as u64
            + (self.sk.len() + self.sv.len()) as u64 * 4
    }

    /// Arrondi à la précision d'une demi-précision (10 bits de mantisse).
    /// Sert à tester l'hypothèse « llama.cpp calcule ses clés en f16 AVANT de
    /// les quantifier » : c'est peut-être là que se joue son +0,8 % de
    /// perplexité contre notre +3,0 % (à 8 192 jetons).
    #[inline]
    fn arrondi_f16(x: f32) -> f32 {
        let b = x.to_bits();
        if (b & 0x7F80_0000) >= 0x7F80_0000 { return x; }        // inf / NaN
        if (b & 0x7FFF_FFFF) < 0x3880_0000 { return 0.0 * x; }   // sous-normal f16
        f32::from_bits(b.wrapping_add(0x1000) & !0x1FFF)
    }

    /// Écrit un vecteur de clé et un de valeur à la position `pos`.
    #[inline]
    pub fn ecrire(&mut self, kvh: usize, pos: usize, k: &[f32], v: &[f32]) {
        // L'INVARIANT est ici, pas dans `assurer` : au-delà du contexte, `assurer`
        // ne grandit plus et `d = (kvh*cap + pos)*hd` écrivait dans le bloc de la
        // TÊTE KV SUIVANTE (corruption silencieuse) avant de paniquer sur la
        // dernière. Mesuré : `--ppl-reparti --ids 300 --ctx 256 --lot 8` →
        // « range end index 32832 out of range » avant même la connexion au pair.
        // L'appelant doit borner ses positions ; ici on refuse net.
        if pos >= self.ctx { return; }
        if pos + 1 > self.cap { self.assurer(pos + 1); }
        let d = (kvh * self.cap + pos) * self.hd;
        if self.bits >= 32 {
            self.kf[d..d + self.hd].copy_from_slice(&k[..self.hd]);
            self.vf[d..d + self.hd].copy_from_slice(&v[..self.hd]);
            return;
        }
        let niv = if self.bits == 4 { 7.0 } else { 127.0 };
        // `DRAVE_KV_F16=1` : clés et valeurs arrondies en demi-précision avant
        // quantification (ce que fait llama.cpp pour son cache q8_0). L'arrondi
        // s'applique DANS les boucles : allouer des tampons ici fuirait à chaque
        // écriture (une par couche et par jeton).
        let f16a = self.f16_avant;
        let arr = |x: f32| if f16a { Self::arrondi_f16(x) } else { x };
        let base = (kvh * self.cap + pos) * self.pas();
        let sb = (kvh * self.cap + pos) * self.nb;
        // Une échelle PAR BLOC DE 32, comme Q8_0 : un bloc peut porter une
        // valeur forte et des valeurs faibles, que l'échelle du vecteur entier
        // écrase. C'est la différence mesurée avec llama.cpp (+5,2 % de
        // perplexité contre +0,8 % pour son cache q8_0).
        for b in 0..self.nb {
            let lo = b * 32;
            let hi = (lo + 32).min(self.hd);
            let mut mk = 0f32;
            let mut mv = 0f32;
            for i in lo..hi { mk = mk.max(arr(k[i]).abs()); mv = mv.max(arr(v[i]).abs()); }
            let sk = if mk > 0.0 { mk / niv } else { 1.0 };
            let sv = if mv > 0.0 { mv / niv } else { 1.0 };
            self.sk[sb + b] = sk;
            self.sv[sb + b] = sv;
            if self.k_f32 {
                self.kf[d + lo..d + hi].copy_from_slice(&k[lo..hi]);
            }
            if self.k_f16 {
                // f16 direct, sans échelle : aucune division par un maximum de
                // bloc, donc aucune erreur absolue imposée aux petits canaux.
                for i in lo..hi { self.kp[d + i] = f16_depuis_f32(arr(k[i])); }
            }
            if self.v_f32 {
                self.vf[d + lo..d + hi].copy_from_slice(&v[lo..hi]);
            }
            if self.bits == 8 {
                for i in lo..hi {
                    if !self.k_f32 {
                        self.kq[base + i] = (arr(k[i]) / sk).round().clamp(-niv, niv) as i8 as u8;
                    }
                    if !self.v_f32 {
                        self.vq[base + i] = (arr(v[i]) / sv).round().clamp(-niv, niv) as i8 as u8;
                    }
                }
            } else {
                // Nibble bas = indice pair, haut = impair, écrits ENSEMBLE : un
                // `|=` laisserait les nibbles de la fenêtre précédente.
                for j in (lo..hi).step_by(2) {
                    let qk0 = (arr(k[j]) / sk).round().clamp(-niv, niv) as i32 as u8 & 0x0F;
                    let qk1 = (arr(k[j + 1]) / sk).round().clamp(-niv, niv) as i32 as u8 & 0x0F;
                    let qv0 = (arr(v[j]) / sv).round().clamp(-niv, niv) as i32 as u8 & 0x0F;
                    let qv1 = (arr(v[j + 1]) / sv).round().clamp(-niv, niv) as i32 as u8 & 0x0F;
                    self.kq[base + j / 2] = qk0 | (qk1 << 4);
                    self.vq[base + j / 2] = qv0 | (qv1 << 4);
                }
            }
        }
    }

    /// Copie les octets de `t` positions consécutives d'une tête KV vers le
    /// miroir VRAM. Aucune conversion : le noyau lit la même disposition que le
    /// CPU, échelles par bloc comprises.
    pub fn vers_gpu_tranche(&self, machine: &crate::gpu::Gpu, m: &mut crate::gpu::KvGpu,
                            kvh: usize, pos0: usize, t: usize) -> bool {
        let pas = self.pas();
        let d = (kvh * self.cap + pos0) * self.hd;
        let base = (kvh * self.cap + pos0) * pas;
        let sb = (kvh * self.cap + pos0) * self.nb;
        if self.bits >= 32 {
            let ko = unsafe { std::slice::from_raw_parts(
                self.kf[d..].as_ptr() as *const u8, t * self.hd * 4) };
            let vo = unsafe { std::slice::from_raw_parts(
                self.vf[d..].as_ptr() as *const u8, t * self.hd * 4) };
            machine.kv_ecrire_tranche(m, kvh, pos0, t, ko, vo, &[], &[])
        } else {
            machine.kv_ecrire_tranche(m, kvh, pos0, t, &self.kq[base..base + t * pas],
                                      &self.vq[base..base + t * pas],
                                      &self.sk[sb..sb + t * self.nb],
                                      &self.sv[sb..sb + t * self.nb])
        }
    }

    /// Un seul vecteur.
    pub fn vers_gpu(&self, machine: &crate::gpu::Gpu, m: &mut crate::gpu::KvGpu,
                    kvh: usize, pos: usize) -> bool {
        self.vers_gpu_tranche(machine, m, kvh, pos, 1)
    }

    /// Recopie vers la VRAM les `t` positions nouvellement écrites de la couche
    /// `l`. Silencieux quand aucun miroir n'est installé.
    pub fn miroir_gpu(miroirs: Option<&mut [(usize, crate::gpu::KvGpu)]>, l: usize,
                      kvc: &KvCache, pos0: usize, t: usize) {
        let Some((idx, m)) = miroirs.and_then(|v| v.get_mut(l)) else { return };
        let machines = crate::gpu::machines();
        let Some(machine) = machines.get(*idx) else { return };
        for kvh in 0..kvc.n_kv {
            kvc.vers_gpu_tranche(machine, m, kvh, pos0, t);
        }
    }

    /// Déquantifie la clé `(kvh, t)` dans `dst`.
    #[inline]
    pub fn cle(&self, kvh: usize, t: usize, dst: &mut [f32]) {
        let d = (kvh * self.cap + t) * self.hd;
        if self.bits >= 32 { dst[..self.hd].copy_from_slice(&self.kf[d..d + self.hd]); return; }
        if self.k_f32 {
            let d = (kvh * self.cap + t) * self.hd;
            dst[..self.hd].copy_from_slice(&self.kf[d..d + self.hd]);
            return;
        }
        if self.k_f16 {
            let d = (kvh * self.cap + t) * self.hd;
            for i in 0..self.hd { dst[i] = f32_depuis_f16(self.kp[d + i]); }
            return;
        }
        let base = (kvh * self.cap + t) * self.pas();
        let sb = (kvh * self.cap + t) * self.nb;
        if self.bits == 8 {
            for i in 0..self.hd {
                dst[i] = self.kq[base + i] as i8 as f32 * self.sk[sb + i / 32];
            }
        } else {
            for i in 0..self.hd {
                let o = self.kq[base + i / 2];
                // Extension de signe du nibble : 0..7 tel quel, 8..15 -> -8..-1.
                let q = if i % 2 == 0 { (o & 0x0F) as i32 } else { (o >> 4) as i32 };
                let q = if q >= 8 { q - 16 } else { q };
                dst[i] = q as f32 * self.sk[sb + i / 32];
            }
        }
    }

    /// Déquantifie la valeur `(kvh, t)` dans `dst`.
    #[inline]
    pub fn valeur(&self, kvh: usize, t: usize, dst: &mut [f32]) {
        let d = (kvh * self.cap + t) * self.hd;
        if self.bits >= 32 || self.v_f32 {
            dst[..self.hd].copy_from_slice(&self.vf[d..d + self.hd]);
            return;
        }
        let base = (kvh * self.cap + t) * self.pas();
        let sb = (kvh * self.cap + t) * self.nb;
        if self.bits == 8 {
            for i in 0..self.hd {
                dst[i] = self.vq[base + i] as i8 as f32 * self.sv[sb + i / 32];
            }
        } else {
            for i in 0..self.hd {
                let o = self.vq[base + i / 2];
                let q = if i % 2 == 0 { (o & 0x0F) as i32 } else { (o >> 4) as i32 };
                let q = if q >= 8 { q - 16 } else { q };
                dst[i] = q as f32 * self.sv[sb + i / 32];
            }
        }
    }
}

/// Un seul message pour un échec de la chaîne top-k déportée, quel que soit le
/// nombre de couches et de jetons (voir la branche `DRAVE_GPU_TOPK`).
static TOPK_GPU_ECHEC: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);

/// Densité de l'entrée de la tête, mesurée sur tous les appels. Sert à décider
/// si un stockage par COLONNES vaudrait le coup : ce serait la seule façon
/// **exacte** de ne pas lire toute la matrice.
pub static TETE_ACTIFS: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);
pub static TETE_TOTAL: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);
pub static TETE_APPELS: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);

// NOTE — la tête à restriction *garantie* a été essayée et RETIRÉE.
//
// L'idée : `logit_o = W_o · h ≤ ‖W_o‖ · ‖h‖` (Cauchy-Schwarz). Si le maximum
// trouvé sur une liste dépasse cette borne pour tout le reste, l'argmax global
// est dans la liste — une preuve, pas une heuristique. Implémentée, elle rendait
// bien la sortie identique à une tête complète.
//
// Mais elle ne conclut **jamais** : la borne vaut `logit / cos(W_o, h)`, soit 5
// à 20 fois le logit réel en haute dimension. La boucle descendait donc tout le
// vocabulaire **ligne par ligne**, bien plus lentement que la passe parallèle
// complète. Mesuré : le calcul ne terminait pas là où la tête entière prend
// 6,9 ms.
//
// La voie exacte par sparsité a été mesurée aussi, et elle échoue pour une autre
// raison : l'entrée de la tête n'est creuse qu'au prix d'un seuil qui détruit le
// modèle (densité 5,1 % ⇒ perplexité ×107 ; 30,3 % ⇒ +48 % ; 61,5 % ⇒ +15 %).
//
// Conclusion consignée dans `reports/rapport-tete-restreinte.md` : on ne peut pas
// garantir l'argmax en lisant moins que tout. Reste `--tete-restreinte`, qui est
// une **génération contrainte** assumée — elle change la sortie, et le dit.

/// Un seul message pour `--attn-topk` ignoré en mode lot (voir `forward_lot`).
static LOT_TOPK_IGNORE: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);

impl Model {
    pub fn load(path: &str, ctx: usize, n_threads: usize, dense: bool, keep: f32,
                auto: bool, q4: u8, b6: u8) -> Model {
        let t0 = Instant::now();
        let g = Gguf::open_auto(path).expect("ouverture du GGUF");
        let arch = g.meta.get("general.architecture").and_then(|m| m.as_str())
                       .unwrap_or("").to_string();
        let r = routage_du_gguf(&g);
        let (n_expert, n_expert_used, ffn_exp) = (r.n_expert, r.n_expert_used, r.ffn_exp);
        let cfg = Cfg {
            n_layer: dim_gguf(&g, &["block_count", "num_hidden_layers"], "num_hidden_layers")
                         .unwrap_or(0) as usize,
            hidden: dim_gguf(&g, &["embedding_length", "hidden_size"], "hidden_size")
                        .unwrap_or(0) as usize,
            n_head: dim_gguf(&g, &["attention.head_count", "num_attention_heads"],
                             "num_attention_heads").unwrap_or(0) as usize,
            n_kv_head: dim_gguf(&g, &["attention.head_count_kv", "num_key_value_heads"],
                                "num_key_value_heads").unwrap_or(0) as usize,
            ffn: dim_gguf(&g, &["feed_forward_length", "intermediate_size"],
                          "intermediate_size").unwrap_or(0) as usize,
            eps: g.cfg("attention.layer_norm_rms_epsilon").and_then(|m| m.as_f64()).unwrap_or(1e-6) as f32,
            rope_base: reel_gguf(&g, &["rope.freq_base", "rope_theta"], "rope_theta")
                           .unwrap_or(10000.0) as f32,
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
            gating: r.gating, expert_norm: r.norm, expert_scale: r.echelle,
            hash_layers: r.hash_layers,
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
            //   `DRAVE_YARN=1`      YaRN à toutes les positions, comme HF, llama.cpp
            //                    et l'implémentation officielle d'OpenAI ;
            //   `DRAVE_YARN_NON=1`  jamais de YaRN (ce que fait `--sans-yarn`) ;
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
                        // 192,63 à 2 048. Le mode FORCÉ (`DRAVE_YARN=1`) garde donc
                        // le comportement des implémentations de référence, et
                        // le mode retardé — celui du moteur — s'en passe.
                        // `DRAVE_YARN_MSCALE=0/1` tranche explicitement dans les
                        // deux cas.
                        std::env::var("DRAVE_YARN_MSCALE").map(|v| v != "0")
                            .unwrap_or_else(|_| std::env::var("DRAVE_YARN").is_ok()),
                    )),
                    _ => None,
                };
                let toujours = std::env::var("DRAVE_YARN").is_ok();
                let jamais = std::env::var("DRAVE_YARN_NON").is_ok();
                // Seuil de bascule : mesuré au protocole apparié (`--depuis`,
                // mêmes 512 jetons notés) à 5 120 jetons — RoPE simple **9,6986**
                // contre **1 269,1777** en interpolation seule — puis à 16 384 :
                // **35,18** contre **1 133,02**. L'interpolation n'a JAMAIS gagné
                // sur l'étendue mesurée (128 → 16 384), et l'écart se creuse avec
                // la longueur. Le seuil passe donc à 4 × la longueur déclarée
                // (16 384 pour gpt-oss, la plus grande longueur mesurée) : elle ne
                // s'active plus là où on sait qu'elle nuit. Au-delà, extrapolation
                // non mesurée — le corpus disponible s'arrête à 17 k jetons.
                match declare {
                    Some(y) if toujours => Some(y),
                    Some(y) if !jamais && ctx as f32 > y.3 * 4.0 => Some(y),
                    _ => None,
                }
            },
        };

        let cfg = {
            let mut c = cfg;
            if c.head_dim == 0 { c.head_dim = c.hidden / c.n_head.max(1); }
            c
        };
        // AVANT toute construction : si le moteur ne sait pas calculer cette
        // architecture, le dire ici, avec la liste de ce qui manque. Sinon la
        // panne arrive trente lignes plus loin sous la forme « tenseur
        // blk.3.attn_q.weight absent » — qui accuse le fichier au lieu du moteur.
        let map = crate::clusters::actif();
        let manques = manques_architecture(&g, &cfg, ctx, map.is_some());
        if let Err(raison) = refus_architecture(&g, &cfg, ctx, map.is_some(), manques) {
            panic!("{raison}");
        }
        assert!(cfg.head_dim > 0, "dimension de tête indéterminée");
        assert!(cfg.head_dim * cfg.n_head >= cfg.hidden,
                "n_head × head_dim doit couvrir hidden");
        // Capturé avant que `cfg` ne soit déplacé dans la structure.
        let n_layer_total = cfg.n_layer;
        // Le mapping est lu UNE fois et passé aux couches : un état global lu
        // par couche rendait ce chemin intestable (les tests s'exécutent en
        // parallèle, un `OnceLock` ne se pose qu'une fois).
        let mla = if g.tensor("blk.0.attn_kv_a_mqa.weight").is_some() {
            let mut v = Vec::with_capacity(cfg.n_layer);
            for l in 0..cfg.n_layer {
                let p = |s: &str| format!("blk.{l}.{s}");
                let opt = |n: &str| g.dequant_optionnel(&p(n));
                let t = |n: &str| g.tensor(&p(n)).unwrap_or_else(|| panic!("tenseur MLA {n} absent"));
                // Le fichier déclare (entrée, sortie) ; le moteur renverse à la
                // lecture, donc `dims[0]` est ici la SORTIE (= le rang).
                let q_lora = t("attn_q_a.weight").dims[0] as usize;
                let q_b = g.dequant(&p("attn_q_b.weight"));
                let qkr = g.cfg("rope.dimension_count").and_then(|m| m.as_u64())
                    .unwrap_or(0) as usize;
                let cle = t("attn_kv_a_mqa.weight").dims[0] as usize;
                let kv_lora = cle - qkr;
                let nh = cfg.n_head;
                let total = q_b.len() / q_lora;              // nh*(qkn+qkr)
                let qkn = total / nh - qkr;
                // Deux dispositions, lues à la présence des tenseurs : un
                // `attn_kv_b` combiné (V3 ancien, harnais synthétique), ou
                // `attn_k_b` + `attn_v_b` séparés (Kimi-K2.7, V4). Deviner
                // d'après le nom de l'architecture marcherait jusqu'au premier
                // modèle qui mélange les deux.
                let (kv_b, k_b, v_b, vd) = if g.tensor(&p("attn_kv_b.weight")).is_some() {
                    let kv_b = g.dequant(&p("attn_kv_b.weight"));
                    let per = kv_b.len() / kv_lora;          // nh*(qkn+vd)
                    (kv_b, None, None, per / nh - qkn)
                } else {
                    let k_b = g.dequant(&p("attn_k_b.weight"));
                    let v_b = g.dequant(&p("attn_v_b.weight"));
                    // `attn_v_b` est `[nh, v, kv_lora]` : la dimension rapide
                    // est l'ENTRÉE (voir `attn_mla`).
                    let vd = v_b.len() / (nh * kv_lora);
                    (Vec::new(), Some(k_b), Some(v_b), vd)
                };
                v.push(Mla {
                    q_a: g.dequant(&p("attn_q_a.weight")),
                    q_a_norm: g.dequant(&p("attn_q_a_norm.weight")),
                    q_b,
                    kv_a: g.dequant(&p("attn_kv_a_mqa.weight")),
                    kv_a_norm: g.dequant(&p("attn_kv_a_norm.weight")),
                    kv_b, k_b, v_b,
                    wo: g.dequant(&p("attn_output.weight")),
                    ffn_norm: opt("ffn_norm.weight").unwrap_or_default(),
                    gate: opt("ffn_gate.weight").unwrap_or_default(),
                    up: opt("ffn_up.weight").unwrap_or_default(),
                    down: opt("ffn_down.weight").unwrap_or_default(),
                    attn_norm: g.dequant(&p("attn_norm.weight")),
                    q_lora, kv_lora, qkr, qkn, vd, nh, ffn: cfg.ffn,
                    eps: cfg.eps,
                });
            }
            let m0 = &v[0];
            println!("[config] MLA : {} couches · q_lora {} · kv_lora {} · qk_nope {} + qk_rope {} · v {} · \
                      cache latente {} valeurs par jeton (au lieu de {})",
                     v.len(), m0.q_lora, m0.kv_lora, m0.qkn, m0.qkr, m0.vd,
                     m0.kv_lora + m0.qkr, cfg.n_kv_head * (m0.qkn + m0.vd));
            Some(v)
        } else { None };
        let mut layers = Vec::with_capacity(cfg.n_layer);
        let mut bytes = 0u64;
        for l in 0..cfg.n_layer {
            let p = |s: &str| format!("blk.{l}.{s}");
            let moe = charger_moe(&g, l, cfg.n_expert, map);
            let lay = Layer {
                attn_norm: g.dequant(&p("attn_norm.weight")),
                // Couche MLA : Q, K et V n'existent pas en dense — ils sont
                // calculés par `attn_mla` depuis les projections de rang faible.
                // Charger `attn_q.weight` ici, c'est chercher un tenseur que le
                // modèle n'a pas, et refuser 216 Go pour un nom.
                wq: if mla.is_some() { Proj::vide() } else {
                    Proj::load(&g, &p("attn_q.weight"), Some(&p("attn_q.bias")), dense || q4 != 0, auto, keep, q4 & 2 != 0, b6 & 2 != 0) },
                wk: if mla.is_some() { Proj::vide() } else {
                    Proj::load(&g, &p("attn_k.weight"), Some(&p("attn_k.bias")), dense || q4 != 0, auto, keep, q4 & 2 != 0, b6 & 2 != 0) },
                wv: if mla.is_some() { Proj::vide() } else {
                    Proj::load(&g, &p("attn_v.weight"), Some(&p("attn_v.bias")), dense || q4 != 0, auto, keep, q4 & 2 != 0, b6 & 2 != 0) },
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
                // La FFN dense se charge COUCHE PAR COUCHE : « le modèle a des
                // experts » ne veut pas dire « toutes ses couches en ont ».
                // GLM-5.3 a 3 couches denses puis 76 à experts, Kimi 1 puis 60.
                // Le test global les vidait toutes, et le modèle mourait sur
                // « projection sans aucun format » à la première couche dense.
                wgate: if moe.is_some() { Proj::vide() } else {
                    Proj::load(&g, &p("ffn_gate.weight"), None, dense || q4 != 0, auto, keep, q4 & 1 != 0, b6 & 1 != 0) },
                wup: if moe.is_some() { Proj::vide() } else {
                    Proj::load(&g, &p("ffn_up.weight"), None, dense || q4 != 0, auto, keep, q4 & 1 != 0, b6 & 1 != 0) },
                wdown: if moe.is_some() { Proj::vide() } else {
                    Proj::load(&g, &p("ffn_down.weight"), None, dense || q4 != 0, auto, keep, q4 & 1 != 0, b6 & 1 != 0) },
                moe,
            };
            for pj in [&lay.wq, &lay.wk, &lay.wv, &lay.wo, &lay.wgate, &lay.wup, &lay.wdown] {
                if let Some(m) = &pj.m { bytes += m.data.len() as u64; }
                if let Some(d) = &pj.d { bytes += d.q.len() as u64 + d.scale.len() as u64 * 4; }
            }
            layers.push(lay);
        }
        let out_norm = g.dequant("output_norm.weight");
        // Précision du cache KV : 32 (f32), 8 ou 4.
        //
        // Le défaut est maintenant **choisi** au lieu d'être figé. Le mur du
        // contexte long n'est pas le calcul mais la place : mesuré sur V4.1, le
        // KV de MLA pèse 90 Ko par jeton en F16, soit 96,6 Go à 1 M de jetons —
        // plus que les 71 Go d'experts. En int8, 48,3 Go.
        //
        // La règle : on garde le f32 tant qu'il tient dans un tiers de la RAM
        // libre ; au-delà, on passe en int8. Un tiers et pas la moitié, parce
        // que les experts et le commun doivent aussi tenir. `DRAVE_KV_BITS`
        // reste prioritaire — c'est un défaut, pas une décision.
        let kv_bits: u32 = match std::env::var("DRAVE_KV_BITS").ok().and_then(|v| v.parse().ok()) {
            Some(v) => v,
            None => {
                let octets_f16 = cfg.n_layer as u64 * 2
                    * (cfg.n_kv_head.max(1) * cfg.head_dim) as u64 * 4 * ctx as u64;
                let libre = crate::materiel::ram_libre_go() * 1e9;
                if libre > 0.0 && octets_f16 as f64 > libre / 3.0 {
                    println!("[config] cache KV en int8 : {:.1} Go en f32 pour {ctx} jetons, \
soit plus du tiers de la RAM libre ({:.0} Go) — DRAVE_KV_BITS pour forcer",
                             octets_f16 as f64 / 1e9, libre / 1e9);
                    8
                } else { 32 }
            }
        };
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
        // Combien de couches ont RÉELLEMENT un mélange d'experts chargé. La
        // configuration dit que le modèle en a ; elle ne dit pas que le
        // chargeur les a trouvés. Quand les deux diffèrent, le moteur tombe
        // dans le chemin dense et panique cent lignes plus loin, sur un
        // message (« projection dense requise ») qui ne dit pas pourquoi.
        let moe_vus = layers.iter().filter(|l| l.moe.is_some()).count();
        // Trace de configuration : une ligne qui dit quelles particularités
        // d'architecture ont été reconnues. Sans elle, on débogue à l'aveugle
        // sur un modèle de 60 Go.
        let ligne_echelle = if cfg.n_expert > 0 && cfg.expert_scale != 0.0 && cfg.expert_scale != 1.0 {
            format!("échelle {:.2} ", cfg.expert_scale) } else { String::new() };
        println!("[config] {} couches, hidden {} · {}{}{}{}{}{}{}{}",
                 cfg.n_layer, cfg.hidden,
                 if cfg.yarn.is_some() { "yarn " } else { "" },
                 if cfg.ffn_act_oss { "activation-oss " } else { "" },
                 if cfg.n_expert > 0 { cfg.gating.nom() } else { "" },
                 ligne_echelle,
                 if cfg.hash_layers > 0 { "routage-table " } else { "" },
                 if cfg.n_expert > 0 { "moe " } else { "" },
                 if cfg.n_expert > 0 { "" } else { "" },
                 if cfg.head_dim > 0 { "" } else { "" });
        if cfg.n_expert > 0 {
            println!("[config] mélanges d'experts chargés : {moe_vus}/{n_layer} couches · \
mapping {}",
                     match map {
                         None => "absent (experts en clair dans le fichier)".to_string(),
                         Some(m) => format!("actif : {} clusters × {} experts",
                                            m.n_clusters, m.par_cluster),
                     });
        }
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
        // Opt-in : `DRAVE_GPU_TETE=1`.
        // Têtes liées de la famille Qwen en Q4_K_M : elles sont en **Q6_K**, pas
        // en Q8_0 — sans cette reconnaissance, `DRAVE_GPU_TETE=1` ne faisait rien
        // sur ces modèles (le noyau existait mais aucune tête ne lui était
        // présentée).
        let mut tete_gpu_q6k = false;
        let tete_gpu = if std::env::var("DRAVE_GPU_TETE").is_ok()
                          && crate::gpu::instance().is_some() {
            let machine = crate::gpu::instance();
            let charge = if let (Some(machine), Some((blocs, nb))) =
                (machine, g.q6k_blocks(&tete)) {
                tete_gpu_q6k = true;
                machine.charger_q6k(blocs, cfg.vocab, nb)
            } else if let (Some(machine), Some((blocs, nb))) =
                (machine, g.q8_blocks(&tete)) {
                machine.charger_tete(blocs, cfg.vocab, cfg.hidden, nb)
            } else { None };
            if let (Some(machine), Some(m)) = (machine, charge.as_ref()) {
                println!("[gpu] {} · tête {} × {} ({}) sur le GPU : {:.0} Mo résidents, \
                          {:.0} Mo libres", machine.nom, cfg.vocab, cfg.hidden,
                         if tete_gpu_q6k { "Q6_K" } else { "Q8_0" },
                         m.octets_poids as f64 / 1e6,
                         machine.memoire_libre as f64 / 1e6);
            }
            charge
        } else { None };
        // Miroir VRAM du cache KV (étape E4) : opt-in, et seulement si TOUTES
        // les couches tiennent — sinon on le dit et on garde le CPU.
        let kv_gpu = if std::env::var("DRAVE_GPU_KV").is_ok() {
            let machines = crate::gpu::machines();
            if machines.is_empty() { None } else {
                // Les couches sont réparties EN TOURNANT sur les périphériques :
                // à deux cartes, chacune porte la moitié du cache — c'est ce qui
                // fait tenir un contexte très long sans rien évincer.
                let mut v: Vec<(usize, crate::gpu::KvGpu)> = Vec::with_capacity(caches_kv.len());
                let mut complet = true;
                for (l, c) in caches_kv.iter().enumerate() {
                    let idx = l % machines.len();
                    match machines[idx].kv_allouer(c.n_kv, c.ctx, c.hd, c.bits) {
                        Some(m) => v.push((idx, m)),
                        None => { complet = false; break; }
                    }
                }
                let mixte = caches_kv.iter().any(|c| c.k_f32 || c.v_f32 || c.k_f16);
                if mixte {
                    println!("[gpu] KV déporté désactivé : les variantes d'attribution \
(clés ou valeurs en f32) supposent une disposition homogène");
                }
                if complet && !mixte {
                    let total: usize = v.iter().map(|(_, m)| m.octets).sum();
                    for (i, machine) in machines.iter().enumerate() {
                        let part: usize = v.iter().filter(|(k, _)| *k == i)
                            .map(|(_, m)| m.octets).sum();
                        println!("[gpu] KV déporté : {} couches sur {}, {:.2} Go ici ({:.2} Go libres)",
                                 v.iter().filter(|(k, _)| *k == i).count(), machine.nom,
                                 part as f64 / 1e9, machine.memoire_libre as f64 / 1e9);
                    }
                    println!("[gpu] KV déporté : {:.2} Go au total pour {} couches", 
                             total as f64 / 1e9, v.len());
                    // Le drapeau du top-k ne dit rien par lui-même : sans cette
                    // ligne, `DRAVE_GPU_TOPK=1` posé sans `DRAVE_GPU_KV` (ou avec
                    // un `--attn-topk` hors limites) laissait croire qu'on
                    // mesurait le GPU alors que tout restait au CPU.
                    if std::env::var("DRAVE_GPU_TOPK").map(|v| v != "0" && !v.is_empty())
                        .unwrap_or(false) {
                        let bits = caches_kv.first().map(|c| c.bits).unwrap_or(32);
                        if !(bits == 8 || bits == 32) {
                            println!("[gpu] top-k déporté REFUSÉ : valeurs KV {bits} bits (le noyau 3 n'en gère que 8 ou 32)");
                        } else {
                            println!("[gpu] top-k déporté demandé (DRAVE_GPU_TOPK) : actif si --attn-topk vaut 1 à 1024, sans fenêtre, et si nkv × rep = nh");
                        }
                    }
                    Some(v)
                } else {
                    println!("[gpu] KV déporté impossible sur {} périphérique(s) : contexte {} \
                              trop long pour la VRAM — cache KV gardé en RAM",
                             machines.len(), caches_kv.first().map(|c| c.ctx).unwrap_or(0));
                    None
                }
            }
        } else { None };
        // ---- MLA : reconnu à ses tenseurs, sans aucune clé de configuration
        // (les rangs se lisent dans les FORMES, ce qui évite d'ajouter cinq
        // champs à `Cfg` et de les tenir à jour).
        let mla_cache = match mla.as_ref() {
            Some(v) => v.iter().map(|m| (vec![0f32; ctx * m.kv_lora], vec![0f32; ctx * m.qkr])).collect(),
            None => Vec::new(),
        };

        // Cache VRAM des experts : opt-in, et seulement sur un modèle à experts
        // au format MXFP4 (les autres formats ont leurs propres noyaux).
        let cache_experts = if std::env::var("DRAVE_GPU_EXPERTS").is_ok()
                               && crate::gpu::instance().is_some()
                               && cfg.n_expert > 0 {
            // Budget par défaut : ce que la VRAM peut donner sans étrangler le
            // reste. Mesuré : la VRAM lit à 84,9 Go/s contre 22,5 pour la RAM,
            // et un cache de 25 % de l'empreinte sert 80 % des appels.
            let defaut = {
                let m = crate::materiel::Materiel::detecter();
                let libre: f64 = m.gpus.iter().map(|g| g.vram_libre_go).sum();
                (libre - 2.0).max(1.0)      // 2 Go de réserve pour le contexte CUDA
            };
            let go: f64 = std::env::var("DRAVE_GPU_EXPERTS_GO").ok()
                .and_then(|v| v.parse().ok()).unwrap_or(defaut);
            let budget = (go * 1e9) as usize;
            println!("[gpu] cache d'experts : budget {:.1} Go de VRAM (LRU), éviction par (couche, expert)",
                     go);
            Some(CacheExperts::nouveau(budget))
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
            ctx, events: 0, paires: [0; 3], act_levels: 127.0, act_thresh: 0.0, act_topk: 0, act_renorm: false,
            act_topk_proj: [0; 7], attn_topk: 0, attn_events: 0, qk_topk: 0,
            moe_topk: 0,
            profil_neurones: None,
            profil_experts: None,
            // Trace de routage des experts : c'est la matière première du
            // découpage en clusters (quels experts sont allumés ENSEMBLE). Le
            // fichier est créé (tronqué) au chargement, tamponné, et fermé avec
            // le modèle — une exécution = une trace.
            trace_experts: std::env::var("DRAVE_TRACE_EXPERTS").ok().and_then(|c| {
                std::fs::File::create(&c).ok().map(|f| {
                    println!("[moe] trace de routage des experts → {c}");
                    std::io::BufWriter::new(f)
                })
            }),
            profil_jetons: 0,
            attn_window: fenetre,
            swa_pattern,
            attn_sinks: if fenetre > 0 { 0 } else { 4 },
            seuil_push: 0.22,
            stop_id: None, stop_id2: None, prof: [0.0; 6],
            tete,
            tete_gpu, tete_gpu_q6k, head4, tete_restreinte: None,
            normes_tete: None, ordre_normes: None, tete_garantie: None,
            tete_calculees: 0, tete_appels_g: 0,
            sinks_vus, kv_gpu, attn_gpu_part: Vec::new(),
            couche_debut: 0, couche_fin: n_layer_total, flux_brut: false,
            cache_experts, mla, mla_cache, jeton_trace: 0, trace: None, flux_force: None,
            emb_imposee: None, emb_imposee_lot: None, lot: 1,
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
              paires: &mut u64,
              levels: f32, thresh: f32, topk: usize, renorm: bool, scratch: &mut Vec<f32>,
              thresh_auto: f32) {
        // On ne quantifie QUE la tranche utile de l'activation. Les appelants
        // passent volontiers un tampon de travail plus large que l'entrée de la
        // projection (12 288 valeurs pour une descente d'expert qui en lit
        // 2 048, 36 864 pour une sortie d'attention MLA qui en produit 16 384) :
        // quantifier le reste fait dépendre l'ÉCHELLE d'activation de valeurs
        // périmées laissées par la position ou la couche précédente. Mesuré :
        // l'écart à llama.cpp sur GLM-5.3 passait de 0,33 à 1,69 de NLL entre la
        // position 0 et la position 6 — une erreur qui grandit avec la position,
        // donc dans le cache ou dans la quantification, pas dans les poids.
        let n_in = p.q4.as_ref().map(|q| q.n_in)
            .or_else(|| p.d.as_ref().map(|d| d.n_in))
            .or_else(|| p.m.as_ref().map(|m| m.n_in))
            .unwrap_or(x.len());
        let x = &x[..n_in.min(x.len())];
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
            *paires += (q.n_in as u64) * (q.n_out as u64);
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
            // Le message porte les DEUX largeurs : c'est ce qui permet de
            // reconnaître la projection fautive (une MLA a wq/wk/wv vides, un
            // modèle à experts a la FFN dense vide) sans backtrace.
            (None, None) => panic!("projection sans aucun format : {} entrées → {} sorties",
                                   x.len(), out.len()),
        };
        if let (Some(machine), Some(mg)) = (crate::gpu::instance(), p.gpu.as_ref()) {
            // Le noyau applique déjà l'échelle d'activation : rien à reprendre.
            let mut xd = vec![0i32; x.len()];
            for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { xd[i as usize] = v; }
            if let Some(y) = machine.proj(mg, &xd, sx) {
                // Le biais fait partie de la projection : l'oublier donnait une
                // perplexité de 27 millions sur un modèle à biais QKV.
                *paires += (x.len() as u64) * (mg.n_out as u64);
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
            *paires += (d.n_in as u64) * (d.n_out as u64);
            for o in 0..d.n_out {
                out[o] = y[o] + p.bias.as_ref().map_or(0.0, |b| b[o]);
            }
            return;
            }
        }
        {
            let m = p.m.as_ref().expect("projection sans format");
            // En listes, une paire EST un événement : on ne paie que les poids
            // non nuls. Les deux compteurs doivent donc avancer ensemble ici —
            // c'est ce qui rend l'écart avec un chemin dense lisible.
            let avant = *events;
            for &i in &sv.idx { *events += m.row_ev[i as usize] as u64; }
            *paires += *events - avant;
            let acc = pool.accumulate_push(m, &sv);
            for o in 0..m.n_out {
                let mut y = acc[o] as f32 * (sx * m.scale[o]);
                if let Some(b) = &p.bias { y += b[o]; }
                out[o] = y;
            }
        }
    }

    /// Produit matrice-vecteur sur une matrice 4 bits empruntée (experts).
    /// Les trois projections d'un expert MXFP4 sur le GPU, avec la MÊME
    /// quantification des activations que `matvec_q4` (mêmes entiers, même
    /// échelle) : la sortie doit être identique au chiffre près.
    #[allow(clippy::too_many_arguments)]
    fn expert_mxfp4_gpu(machine: &crate::gpu::Gpu,
                        mg: &crate::gpu::MatriceGpu, mu: &crate::gpu::MatriceGpu,
                        md: &crate::gpu::MatriceGpu,
                        hn: &[f32], gate: &mut [f32], up: &mut [f32], exp_out: &mut [f32],
                        down: &mut [f32], w_exp: f32, moe: &Moe, e: usize,
                        n_ff: usize, h: usize, levels: f32, thresh: f32,
                        tk4: usize, tk5: usize, tk6: usize, renorm: bool,
                        act_oss: bool, scratch: &mut Vec<f32>) -> bool {
        let quant = |x: &[f32], topk: usize, scratch: &mut Vec<f32>| {
            Self::quant_scratch(x, levels, thresh, topk, renorm, scratch)
        };
        let Some((sv, sx)) = quant(hn, tk4, scratch) else { return false };
        let mut xd = vec![0i32; hn.len()];
        for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { xd[i as usize] = v; }
        let Some(yg) = machine.proj_mxfp4(mg, &xd, sx) else { return false };
        let bg = moe.biais_gate.as_ref().map(|b| &b[e * n_ff..]);
        for o in 0..n_ff { gate[o] = yg[o] + bg.map_or(0.0, |b| b[o]); }
        // `up` se quantifie à partir de la MÊME activation : une seule
        // quantification suffit pour gate et up, comme sur le CPU.
        let Some(yu) = machine.proj_mxfp4(mu, &xd, sx) else { return false };
        let bu = moe.biais_up.as_ref().map(|b| &b[e * n_ff..]);
        for o in 0..n_ff { up[o] = yu[o] + bu.map_or(0.0, |b| b[o]); }
        Self::activation(gate, up, n_ff, act_oss);
        // La descente part de l'activation (non linéaire) : nouvelle
        // quantification, exactement comme `matvec_q4` sur la porte activée.
        let Some((sv2, sx2)) = quant(&gate[..n_ff], tk6, scratch) else { return false };
        let mut gd = vec![0i32; n_ff];
        for (&i, &v) in sv2.idx.iter().zip(sv2.val.iter()) { gd[i as usize] = v; }
        let Some(yd) = machine.proj_mxfp4(md, &gd, sx2) else { return false };
        let bd = moe.biais_down.as_ref().map(|b| &b[e * h..]);
        for i in 0..h { exp_out[i] = yd[i] + bd.map_or(0.0, |b| b[i]); }
        for i in 0..h { down[i] += w_exp * exp_out[i]; }
        true
    }

    /// Produit scalaire d'un expert, **quel que soit son format** : noyau 4 bits
    /// emprunté quand il existe, déquantification sinon.
    ///
    /// Les formats IQ (IQ1_S, IQ1_M, IQ2_XXS, IQ3_XXS) portent 30 % des poids de
    /// Kimi-K2.7, GLM-5.3 et DeepSeek-V4. Ils n'ont pas de noyau ici, et les
    /// refuser rendait ces modèles inchargeables — « mélanges d'experts
    /// chargés : 0/79 » était la seule trace, sans dire pourquoi.
    fn matvec4_ou_iq(pool: &mut Pool, vue: &Vue4, loc: usize, x: &[f32], out: &mut [f32],
                     paires: &mut u64,
                     levels: f32, thresh: f32, topk: usize, renorm: bool,
                     scratch: &mut Vec<f32>, biais: Option<&[f32]>, n_fils: usize) {
        if let crate::list::Source::Dequant(t) = vue.src {
            // Quantification de l'activation par le MÊME chemin que les autres
            // formats (niveaux, seuil, top-k), puis produit en f32 sur le
            // super-bloc déquantifié : la seule différence est que les poids
            // sont reconstruits au lieu d'être lus quantifiés.
            let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
                for v in out[..vue.n_out].iter_mut() { *v = 0.0; }
                return;
            };
            let mut xd = vec![0f32; x.len()];
            for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { xd[i as usize] = v as f32 * sx; }
            // Déquantification puis produit f32 : la matrice ENTIÈRE est payée,
            // quel que soit le nombre d'activations. C'est le chemin le plus
            // cher du moteur, et il ne produisait aucun compteur.
            *paires += (vue.n_in as u64) * (vue.n_out as u64);
            vue.matvec_dequant(loc, t, &xd, &mut out[..vue.n_out], n_fils);
            if let Some(b) = biais { for o in 0..vue.n_out { out[o] += b[o]; } }
            return;
        }
        let d = vue.expert(loc);
        Self::matvec_q4(pool, &d, &x[..vue.n_in.min(x.len())], out, paires, levels, thresh, topk,
                        renorm, scratch, biais);
    }

    fn matvec_q4(pool: &mut Pool, m: &crate::list::DenseQ4, x: &[f32], out: &mut [f32],
                 paires: &mut u64,
                 levels: f32, thresh: f32, topk: usize, renorm: bool,
                 scratch: &mut Vec<f32>, biais: Option<&[f32]>) {
        let x = &x[..m.n_in.min(x.len())];
        let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
            for v in out[..m.n_out].iter_mut() { *v = 0.0; }
            return;
        };
        let mut xd = vec![0i32; x.len()];
        for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { xd[i as usize] = v; }
        let y = pool.matvec_dense_q4(m, &xd, sx);
        *paires += (m.n_in as u64) * (m.n_out as u64);
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
        for l in self.couche_debut..self.couche_fin {
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
                for l in self.couche_debut..self.couche_fin {
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
    pub fn dot8(a: &[f32], b: &[f32]) -> f32 {
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
                // DRAVE_YARN_RAMPE=0 force l'interpolation pure.
                let rampe = if std::env::var("DRAVE_YARN_RAMPE").map_or(false, |v| v == "0") {
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
        // Modèle MLA : le chemin par lots ne connaît que Q/K/V denses. On
        // repasse par le jeton seul, qui porte la MLA et le cache latent. Le
        // préremplissage par lots perd son intérêt sur ces modèles — c'est dit
        // ici plutôt que découvert par un panic « projection sans format ».
        if self.mla.is_some() {
            return toks.iter().enumerate()
                .map(|(i, &t)| self.forward(t, pos0 + i)).collect();
        }
        let t = toks.len();
        // Lot IMPOSÉ (préremplissage réparti) : les états arrivent de l'autre
        // nœud, on ne repasse pas par `token_embd`. Lu avant tout le reste — y
        // compris avant le retour anticipé sur `t == 0`, sinon une trame vide
        // laissait l'état imposé en place pour le lot suivant (D7 de la
        // relecture) — et consommé une seule fois, comme `emb_imposee` pour un
        // jeton seul.
        let impose = self.emb_imposee_lot.take();
        if t == 0 { return Vec::new(); }
        // `--attn-topk` n'est PAS implémenté dans le chemin par lots : le lot
        // calcule une attention DENSE (la sélection à k clés n'y a jamais été
        // écrite). Jusqu'ici le drapeau était simplement ignoré — le pire cas du
        // dépôt, une valeur qui ne fait rien et ne le dit pas : `--lot 8
        // --attn-topk 256` et `--lot 1 --attn-topk 256` ne donnaient pas le même
        // résultat. Relevé par la relecture du branchement ; on le dit une fois,
        // et on le dit FORT, en attendant de l'implémenter ou de le refuser.
        if self.attn_topk > 0 && t > 1 && !LOT_TOPK_IGNORE.swap(true, std::sync::atomic::Ordering::Relaxed) {
            eprintln!("[attention] --attn-topk {} est IGNORÉ en mode lot (--lot {t}) : \
l'attention par lots est DENSE. Utiliser --lot 1 pour l'attention creuse.", self.attn_topk);
        }
        if t == 1 {
            if let Some(v) = impose { self.emb_imposee = Some(v); }
            // Le jeton n'est PAS lu quand un état est imposé : `forward` prend
            // `emb_imposee` et n'appelle jamais `token_embd`. `toks` peut donc
            // être vide côté nœud distant, qui ne connaît que des états.
            //
            // Le raccourci sort AVANT l'avance du compteur : `forward` avance le
            // sien. Le faire avancer ici aussi doublait la clé à chaque jeton
            // (2, 4, 6…) — et une trace écrite en `--lot 1` n'était alors
            // relisible par AUCUN autre mode.
            return vec![self.forward(toks.first().copied().unwrap_or(0), pos0)];
        }
        // Clé de trace du lot : compteur global, 1-based, avancé une fois pour
        // tout le lot. Le chemin jeton par jeton écrit la même famille de clés.
        let j0 = self.jeton_trace + 1;
        self.jeton_trace += t as u64;
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
        match impose {
            Some(v) => {
                assert_eq!(v.len(), t * h,
                           "lot imposé de {} valeurs pour {t} jetons de {h} canaux",
                           v.len());
                x.copy_from_slice(&v);
            }
            None => {
                for (i, &tok) in toks.iter().enumerate() {
                    let r = self.g.row_f32("token_embd.weight", tok as usize, h);
                    x[i * h..(i + 1) * h].copy_from_slice(&r);
                }
            }
        }
        let mut hn = vec![0f32; t * h];
        let mut xi = vec![0i32; t * h];
        let mut sx = vec![0f32; t];
        let mut q = vec![0f32; t * nh * hd];
        let mut k = vec![0f32; t * nkv * hd];
        let mut v = vec![0f32; t * nkv * hd];
        let mut att = vec![0f32; t * nh * hd];
        // Copie des requêtes APRÈS rotation, pour le noyau GPU : `q` est
        // emprunté en mutable par la norme et la rotation, et le noyau n'a
        // besoin que de lire.
        let mut qgpu = vec![0f32; t * nh * hd];
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
        // Scores groupés : `nh × ctx`, comme dans le chemin jeton par jeton.
        let mut sc2 = vec![0f32; nh * self.ctx];
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
        for l in self.couche_debut..self.couche_fin {
            let lay = &self.layers[l];
            // 1. norme d'entrée du lot
            for i in 0..t {
                let r = &x[i * h..(i + 1) * h];
                Self::rmsnorm(r, &lay.attn_norm, self.cfg.eps, &mut hn[i * h..(i + 1) * h]);
            }
            quantifier(&hn, &mut xi, &mut sx, self.act_levels, self.act_thresh);
            Self::flux_lot(&mut self.trace, &mut self.flux_force, j0,
                           0, l, t, &mut xi, &mut sx, h);
            let t_proj = Instant::now();
            // 2. q, k, v : un produit matrice-matrice chacun. Trois tampons
            //    DISTINCTS (un `y` partagé avec un pas par projection mélangeait
            //    les sorties : mesuré, une perplexité de 1,6 million).
            let nq = nh * hd;
            let nk = nkv * hd;
            for (pj, dst, taille) in [(&lay.wq, &mut qa, nq),
                                      (&lay.wk, &mut ka, nk),
                                      (&lay.wv, &mut va, nk)] {
                if let Some(d8) = pj.d.as_ref() {
                    self.paires[0] += (d8.n_in as u64) * (d8.n_out as u64) * t as u64;
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
                                     &mut self.events, &mut self.paires[0], self.act_levels,
                                     self.act_thresh, 0,
                                     self.act_renorm, &mut scratch, self.seuil_push);
                        dst[i * taille..(i + 1) * taille].copy_from_slice(&out);
                    }
                }
            }
            q.copy_from_slice(&qa);
            k.copy_from_slice(&ka);
            v.copy_from_slice(&va);
            self.prof[0] += t_proj.elapsed().as_secs_f64();
            let t_att = Instant::now();
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
                qgpu[i * nq..(i + 1) * nq].copy_from_slice(qi);
                {
                    let kvc = &mut self.kv[l];
                    for hh in 0..nkv {
                        kvc.ecrire(hh, pos, &ki[hh * hd..(hh + 1) * hd],
                                          &vi[hh * hd..(hh + 1) * hd]);
                    }
                }
                // Miroir VRAM, une position à la fois : l'attention du jeton `i`
                // a besoin des clés de TOUT le lot déjà écrit, donc la copie doit
                // suivre l'écriture. Quelques centaines d'octets par couche et par
                // jeton — le contraire (copier le lot à la fin) donnerait au noyau
                // un cache amputé de son propre lot.
                KvCache::miroir_gpu(self.kv_gpu.as_deref_mut(), l, &self.kv[l], pos, 1);
                let fen = if self.attn_window == 0 { 0 }
                          else if self.swa_pattern <= 1 { self.attn_window }
                          else if l % self.swa_pattern < self.swa_pattern - 1 { self.attn_window }
                          else { 0 };
                let kvc = &self.kv[l];
                let n = pos + 1;
                let lo = if fen > 0 && n > fen { n - fen } else { 0 };
                // Chemin GROUPÉ dès que possible : `rep` têtes de requête
                // partagent une tête KV, donc la clé (et la valeur) ne doivent
                // être déquantifiées qu'UNE fois par groupe. Le chemin par tête
                // les relisait `rep` fois — mesuré ×2,2 sur ce poste.
                let groupe = fen == 0 && self.attn_topk == 0 && rep > 1;
                // ---- KV déporté : la même attention, calculée en VRAM (E4) ----
                let mut fait_en_gpu = false;
                if groupe && self.kv_gpu.is_some() && nkv * rep == nh && n > 1 {
                    let nsplit = (n / 256).clamp(1, 128);
                    let besoin = nsplit * nkv * rep * (hd + 2);
                    if self.attn_gpu_part.len() < besoin { self.attn_gpu_part.resize(besoin, 0.0); }
                    let puits: Option<Vec<f32>> = lay.sinks.as_ref()
                        .map(|s| (0..nh).map(|h| s[h]).collect());
                    let part = &mut self.attn_gpu_part;
                    // Copie des requêtes du jeton : `qi` emprunte `q` en
                    // mutable pour la norme et la rotation, qui viennent d'être
                    // faites — le noyau, lui, n'a besoin que de lire.
                    let requetes = &qgpu[i * nq..(i + 1) * nq];
                    let sortie = &mut att[i * nq..(i + 1) * nq];
                    if let Some((idx, m)) = self.kv_gpu.as_mut().and_then(|v| v.get_mut(l)) {
                        let machines = crate::gpu::machines();
                        let machine = machines[*idx];
                        if machine.attn_kv(m, requetes, n, scale,
                                           puits.as_deref(), nsplit, part, sortie) {
                            self.attn_events += (nh * n) as u64;
                            fait_en_gpu = true;
                        }
                    }
                }
                if groupe && !fait_en_gpu {
                    for kvh in 0..nkv {
                        let h0 = kvh * rep;
                        let h1 = (h0 + rep).min(nh);
                        for tt in 0..n {
                            kvc.cle(kvh, tt, &mut kd);
                            for hh in h0..h1 {
                                let qh = &qi[hh * hd..(hh + 1) * hd];
                                sc2[hh * ctx + tt] = Self::dot8(qh, &kd) * scale;
                            }
                        }
                        for hh in h0..h1 {
                            let row = &mut sc2[hh * ctx..hh * ctx + n];
                            let mut mx = f32::NEG_INFINITY;
                            for &val in row.iter() { if val > mx { mx = val; } }
                            let puits = lay.sinks.as_ref().map(|s| s[hh]);
                            if let Some(s) = puits { if s > mx { mx = s; } }
                            let mut somme = 0f32;
                            for val in row.iter_mut() { let e = (*val - mx).exp(); *val = e; somme += e; }
                            if let Some(s) = puits { somme += (s - mx).exp(); }
                            let inv = 1.0 / somme;
                            for val in row.iter_mut() { *val *= inv; }
                        }
                        for hh in h0..h1 {
                            let out = &mut att[i * nq + hh * hd..i * nq + (hh + 1) * hd];
                            for val in out.iter_mut() { *val = 0.0; }
                        }
                        for tt in 0..n {
                            kvc.valeur(kvh, tt, &mut vd);
                            for hh in h0..h1 {
                                let w = sc2[hh * ctx + tt];
                                let out = &mut att[i * nq + hh * hd..i * nq + (hh + 1) * hd];
                                for (oo, xx) in out.iter_mut().zip(vd.iter()) { *oo += w * xx; }
                            }
                        }
                    }
                } else if !fait_en_gpu {
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
                }
                self.attn_events += (nh * (n - lo)) as u64;
            }
            self.prof[2] += t_att.elapsed().as_secs_f64();
            let t_ffn = Instant::now();
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
            Self::flux_lot(&mut self.trace, &mut self.flux_force, j0,
                           1000, l, t, &mut xi, &mut sx, h);
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
                let trace_active = self.trace_experts.is_some();
                for i in 0..t {
                    // Le MÊME routeur que le chemin jeton seul (voir `router`) :
                    // deux copies avaient divergé sur le biais de gpt-oss.
                    let choix = router(&self.cfg, moe, &hn[i * h..(i + 1) * h], toks[i], k);
                    if trace_active {
                        use std::io::Write;
                        let mut ids: Vec<usize> = choix.iter().map(|(e, _)| *e).collect();
                        ids.sort_unstable();
                        let liste: Vec<String> = ids.iter().map(|e| e.to_string()).collect();
                        let f = self.trace_experts.as_mut().unwrap();
                        let jeton = self.jeton_trace.saturating_sub(t as u64) + i as u64;
                        let _ = writeln!(f, "{} {} {}", l, jeton, liste.join(" "));
                    }
                    for (e, poids) in choix { groupes[e].push((i, poids)); }
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
                    // L'expert global `e` peut ne pas être dans ce nœud.
                    let Some((k, loc)) = moe.ou(e) else { continue; };
                    for (j, &(i, _)) in groupes[e].iter().enumerate() {
                        xg[j * h..(j + 1) * h].copy_from_slice(&x16[i * h..(i + 1) * h]);
                    }
                    s32g.clear();
                    sxg.clear();
                    for &(i, _) in groupes[e].iter() { s32g.push(s32[i].clone()); sxg.push(sx[i]); }
                    let mg = moe.gate[k].expert(loc);
                    self.pool.gemm_dense_q4(&mg, &xg[..g * h], g, &s32g, &sxg,
                                            &mut yq[..mg.n_out * g]);
                    for j in 0..g {
                        for oo in 0..nff {
                            gate[oo * g + j] = yq[oo * g + j]
                                + moe.biais_gate.as_ref().map_or(0.0, |b| b[e * nff + oo]);
                        }
                    }
                    let mu = moe.up[k].expert(loc);
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
                    let md = moe.down[k].expert(loc);
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
            self.prof[3] += t_ffn.elapsed().as_secs_f64();
        }
        if self.flux_brut || self.couche_fin < self.cfg.n_layer {
            // Nœud intermédiaire : on rend le flux résiduel brut, sans norme.
            return (0..t).map(|i| x[i * h..(i + 1) * h].to_vec()).collect();
        }
        for i in 0..t {
            let r = x[i * h..(i + 1) * h].to_vec();
            Self::rmsnorm(&r, &self.out_norm, self.cfg.eps, &mut hn[i * h..(i + 1) * h]);
        }
        (0..t).map(|i| hn[i * h..(i + 1) * h].to_vec()).collect()
    }

    /// Trace OU impose le flux d'un LOT : `xi` porte les entiers quantifiés du
    /// lot (t × h) et `sx` une échelle par jeton. Sur ce chemin, le rejeu est
    /// EXACT — on remplace les entiers et l'échelle, sans repasser par une
    /// déquantification suivie d'une requantification.
    #[allow(clippy::too_many_arguments)]
    /// `j0` est la clé du PREMIER jeton du lot (compteur global, 1-based comme
    /// sur le chemin jeton par jeton) : elle est calculée UNE fois par lot par
    /// `forward_lot`, et non à chaque appel — `flux_lot` est appelé deux fois par
    /// couche (famille attention, base 0, et famille FFN, base 1000) et les deux
    /// doivent écrire les MÊMES clés. Avant, le compteur avançait de `t` à chaque
    /// appel : une trace écrite avec `--lot N` n'était rejouable qu'avec le même N
    /// (relecture adversariale, D3).
    fn flux_lot(trace: &mut Option<TraceFlux>, force: &mut Option<FluxRelecteur>,
                j0: u64, base: usize, l: usize, t: usize,
                xi: &mut [i32], sx: &mut [f32], h: usize) {
        if trace.is_none() && force.is_none() { return; }
        let mut j0 = j0;                 // clé du jeton i du lot : j0 + i
        for i in 0..t {
            if let Some(r) = force.as_mut() {
                if let Some((ech, paires)) = r.listes.get(&((base + l) as u16, j0 as u32)).cloned() {
                    for v in xi[i * h..(i + 1) * h].iter_mut() { *v = 0; }
                    for (idx, q) in paires {
                        if (idx as usize) < h { xi[i * h + idx as usize] = q as i32; }
                    }
                    sx[i] = ech;
                    r.servies += 1;
                } else if r.listes_blocs.contains_key(&((base + l) as u16, j0 as u32)) {
                    // Une trace v3 n'a plus d'entiers d'origine : le rejeu par
                    // lots, qui les réinjecte, ne peut pas s'en servir. On le dit
                    // UNE fois, plutôt que de compter des manquantes muettes.
                    if r.servies == 0 && r.manquantes == 0 {
                        eprintln!("[flux] trace v3 (valeurs i8) : le rejeu par LOTS ne \
s'applique pas — utilisez --lot 1, ou réenregistrez sans DRAVE_TRACE_BLOCS");
                    }
                    r.manquantes += 1;
                } else {
                    // D2 de la relecture adversariale : sans ce `else`, une clé
                    // absente des DEUX cartes n'était comptée nulle part — le
                    // garde-fou devenait aveugle dès `--lot > 1`, et une trace
                    // entièrement étrangère s'affichait « 0 manquante ».
                    r.manquantes += 1;
                }
            } else if let Some(tr) = trace.as_mut() {
                let actifs: Vec<i32> = xi[i * h..(i + 1) * h].to_vec();
                let e = sx[i];
                tr.ecrire(base + l, j0 as usize, &actifs, e);
            }
            j0 += 1;
        }
    }

    /// **Attention MLA** pour un jeton : quatre projections de rang faible et
    /// un cache LATENT.
    ///
    /// `Q = W_q_b · norm(W_q_a · h)` ; `c_kv = norm(W_kv_a · h)` et
    /// `k_rope = RoPE(W_kv_a · h)` ; puis, à la lecture, `k_nope` et `v` sont
    /// **reconstruits** depuis `c_kv` par `W_k_b` et `W_v_b`. Le cache ne
    /// stocke donc que `c_kv` (512 valeurs) et `k_rope` (64) par position, au
    /// lieu de `n_head × (qk_nope + v)` — 8 192 pour Kimi. C'est tout l'intérêt
    /// de MLA, et c'est aussi ce qui rend le cache indépendant du nombre de
    /// têtes.
    ///
    /// Deux dispositions existent, et elles ne se devinent pas :
    ///   - **séparée** (Kimi-K2.7, DeepSeek-V3) : `attn_k_b` `[nh, kv_lora,
    ///     qk_nope]` et `attn_v_b` `[nh, kv_lora, v]` ;
    ///   - **combinée** (harnais `tools/mla_synthetique.py`) : un seul
    ///     `attn_kv_b` `[kv_lora, nh*(qk_nope+v)]`.
    /// Laquelle s'applique se lit à la présence des tenseurs, jamais au nom de
    /// l'architecture.
    fn attn_mla(m: &Mla, cache: &mut (Vec<f32>, Vec<f32>), hn: &[f32], pos: usize,
                rope_base: f32, att: &mut [f32], paires: &mut u64, scores: &mut u64) {
        // `DRAVE_DEBUG_MLA=1` : les premières valeurs des projections MLA, à
        // comparer à `llama-debug --tensor-filter Kcur-0` sur les mêmes jetons.
        // Une divergence de corrélation sur les LOGITS ne dit pas où elle
        // commence ; ces quatre lignes le disent.
        let dbg = std::env::var("DRAVE_DEBUG_MLA").is_ok() && pos < 2;
        let (nh, qkn, qkr, vd, kvl) = (m.nh, m.qkn, m.qkr, m.vd, m.kv_lora);
        let eps = m.eps;
        let h = hn.len();
        // **Flux de ce chemin** : les projections de rang faible sont des
        // matrices f32 PLEINES (aucune liste n'est construite ici), donc elles
        // ne produisent pas d'événements — on compte les paires payées. C'est
        // la mesure qui manquait : un modèle MLA annonçait « 0 événement ».
        *paires += (m.q_a.len() + m.q_b.len() + m.kv_a.len()) as u64;
        // --- requête : descente, norme, remontée, découpage nope / rope
        let mut qa = vec![0f32; m.q_lora];
        matvec_f32(&m.q_a, hn, h, m.q_lora, &mut qa);
        let mut qan = vec![0f32; m.q_lora];
        Self::rmsnorm(&qa, &m.q_a_norm, eps, &mut qan);
        let nq = nh * (qkn + qkr);
        let mut qb = vec![0f32; nq];
        matvec_f32(&m.q_b, &qan, m.q_lora, nq, &mut qb);
        // --- KV : descente, norme sur la partie latente, rotation de l'autre
        let mut kva = vec![0f32; kvl + qkr];
        matvec_f32(&m.kv_a, hn, h, kvl + qkr, &mut kva);
        let mut c_n = vec![0f32; kvl];
        Self::rmsnorm(&kva[..kvl], &m.kv_a_norm, eps, &mut c_n);
        let mut k_rope = kva[kvl..].to_vec();
        Self::rope(&mut k_rope, 1, qkr, pos, rope_base, qkr);
        let mut q_rope = vec![0f32; nh * qkr];
        for hh in 0..nh {
            q_rope[hh * qkr..(hh + 1) * qkr]
                .copy_from_slice(&qb[hh * (qkn + qkr) + qkn..(hh + 1) * (qkn + qkr)]);
        }
        Self::rope(&mut q_rope, nh, qkr, pos, rope_base, qkr);
        if dbg {
            eprintln!("[mla] pos {pos} q_a[..4] {:.5e} {:.5e} {:.5e} {:.5e}", qa[0], qa[1], qa[2], qa[3]);
            eprintln!("[mla] pos {pos} q_a_norm[..4] {:.5e} {:.5e} {:.5e} {:.5e}", qan[0], qan[1], qan[2], qan[3]);
            eprintln!("[mla] pos {pos} q_b[..4] {:.5e} {:.5e} {:.5e} {:.5e}", qb[0], qb[1], qb[2], qb[3]);
            eprintln!("[mla] pos {pos} c_kv[..4] {:.5e} {:.5e} {:.5e} {:.5e}", c_n[0], c_n[1], c_n[2], c_n[3]);
            eprintln!("[mla] pos {pos} k_rope[..4] {:.5e} {:.5e} {:.5e} {:.5e}", k_rope[0], k_rope[1], k_rope[2], k_rope[3]);
            eprintln!("[mla] pos {pos} q_rope[..4] {:.5e} {:.5e} {:.5e} {:.5e}", q_rope[0], q_rope[1], q_rope[2], q_rope[3]);
        }
        // --- écriture du cache latent
        {
            let (ckv, krop) = cache;
            ckv[pos * kvl..(pos + 1) * kvl].copy_from_slice(&c_n);
            krop[pos * qkr..(pos + 1) * qkr].copy_from_slice(&k_rope);
        }
        let (ckv, krop) = (&cache.0, &cache.1);
        let n = pos + 1;
        // Par (tête, position), le chemin paie : la remontée `k_b` (kvl × qkn),
        // la remontée `v_b` (vd × kvl), le score (qkn + qkr), et l'accumulation
        // (vd). La disposition combinée (`kv_b`) paie le produit entier
        // kvl × nh × (qkn + vd) dans les DEUX boucles, d'où le facteur 2.
        //
        // La remontée `v_b` n'est comptée qu'UNE fois : la boucle de scores la
        // calculait aussi, dans une variable jamais relue (`vv`), et ce calcul
        // mort a été supprimé le 02/10 — il payait un tiers du travail de la
        // boucle de scores pour un résultat jeté.
        //
        // Les scores vont dans le MÊME compteur que l'attention dense
        // (`attn_events`) : sans ça, un modèle MLA affichait « 0 paire
        // (requête, clé) » alors qu'il en calcule autant qu'un autre — et la
        // comparaison entre les deux familles aurait été fausse.
        let sep = m.k_b.is_some() && m.v_b.is_some();
        let remontees: u64 = if sep {
            (kvl * qkn + vd * kvl + vd) as u64        // k_b (scores) + v_b (sortie) + accumulation
        } else {
            (2 * kvl * nh * (qkn + vd) + vd) as u64   // `kv_b` est payé dans les DEUX boucles
        };
        *paires += nh as u64 * n as u64 * remontees;
        *scores += nh as u64 * n as u64 * (qkn + qkr) as u64;
        let scale = 1.0 / ((qkn + qkr) as f32).sqrt();
        let mut sc = vec![0f32; n];
        let mut kn = vec![0f32; qkn];
        for hh in 0..nh {
            let q_nope = &qb[hh * (qkn + qkr)..hh * (qkn + qkr) + qkn];
            let qr = &q_rope[hh * qkr..(hh + 1) * qkr];
            for t in 0..n {
                let c = &ckv[t * kvl..(t + 1) * kvl];
                match (&m.k_b, &m.v_b) {
                    // Disposition séparée : `k_b[hh]` est `[kvl, qkn]`, donc
                    // `k_nope[o] = Σ_c k_b[hh][c][o] · c_kv[c]` — l'index de
                    // sortie est le PLUS LENT. L'écrire dans l'autre sens donne
                    // des scores plausibles et faux.
                    (Some(kb), Some(_)) => {
                        // ATTENTION à l'asymétrie des deux remontées, qui ne se
                        // devine pas : llama.cpp déclare
                        //   wk_b = {qk_nope, kv_lora, nh}  → la dimension RAPIDE
                        //                                    est la SORTIE ;
                        //   wv_b = {kv_lora, v,      nh}  → la dimension RAPIDE
                        //                                    est l'ENTRÉE.
                        // Les écrire toutes deux « sortie rapide » donne des
                        // valeurs fausses de la bonne forme — mesuré : `kqv_out`
                        // de la couche 0 valait 5e-4 au lieu de 1,5e-3 chez
                        // llama.cpp, et la corrélation des logits tombait à
                        // −0,04. `k_b` se réduit donc sur la dimension LENTE,
                        // `v_b` sur la dimension RAPIDE.
                        let bk = &kb[hh * kvl * qkn..(hh + 1) * kvl * qkn];
                        for o in 0..qkn {
                            let mut s = 0f32;
                            for (c_, &cc) in c.iter().enumerate() { s += bk[c_ * qkn + o] * cc; }
                            kn[o] = s;
                        }
                        // La remontée `v_b` n'est PAS faite ici : elle l'était,
                        // pour un résultat que personne ne relisait (`vv`). Elle
                        // se fait dans la boucle de sortie, une fois.
                    }
                    // Disposition combinée : un seul tenseur par tête.
                    _ => {
                        let mut kvt = vec![0f32; nh * (qkn + vd)];
                        matvec_f32(&m.kv_b, c, kvl, nh * (qkn + vd), &mut kvt);
                        kn.copy_from_slice(&kvt[hh * (qkn + vd)..hh * (qkn + vd) + qkn]);
                    }
                }
                let mut s = 0f32;
                for i in 0..qkn { s += q_nope[i] * kn[i]; }
                for i in 0..qkr { s += qr[i] * krop[t * qkr + i]; }
                sc[t] = s * scale;
            }
            // softmax sur la fenêtre
            let mx = sc.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
            let mut somme = 0f32;
            for v in sc.iter_mut() { *v = (*v - mx).exp(); somme += *v; }
            let inv = if somme > 0.0 { 1.0 / somme } else { 0.0 };
            for v in sc.iter_mut() { *v *= inv; }
            // somme pondérée : les valeurs sont reconstruites par `v_b` à la
            // lecture, donc le cache reste latent.
            let out = &mut att[hh * vd..(hh + 1) * vd];
            for v in out.iter_mut() { *v = 0.0; }
            for t in 0..n {
                let w = sc[t];
                if w == 0.0 { continue; }
                let c = &ckv[t * kvl..(t + 1) * kvl];
                match (&m.k_b, &m.v_b) {
                    (Some(_), Some(vb)) => {
                        let bv = &vb[hh * vd * kvl..(hh + 1) * vd * kvl];
                        for o in 0..vd {
                            let mut s = 0f32;
                            for (c_, &cc) in c.iter().enumerate() { s += bv[o * kvl + c_] * cc; }
                            out[o] += w * s;
                        }
                    }
                    _ => {
                        let mut kvt = vec![0f32; nh * (qkn + vd)];
                        matvec_f32(&m.kv_b, c, kvl, nh * (qkn + vd), &mut kvt);
                        for o in 0..vd { out[o] += w * kvt[hh * (qkn + vd) + qkn + o]; }
                    }
                }
            }
        }
    }

    /// Passe avant d'un modèle **MLA**, un jeton à la fois, avec le cache
    /// LATENT : `c_kv` (la seule tête latente) et `k_rope` (les composantes
    /// tournées) sont écrites une fois par position, et `k_nope`/`v` sont
    /// reconstruits à la lecture par `W_kv_b` — c'est le contrat de MLA.
    ///
    /// Chemin séparé de `forward` à dessein : le modèle jouet du harnais
    /// (`tools/mla_synthetique.py`) n'a ni tenseurs Q8_0 ni fenêtre glissante, et
    /// mélanger les deux chemins rendrait la validation illisible.
    pub fn forward_mla(&mut self, tok: u32, pos: usize) -> Vec<f32> {
        assert!(pos < self.ctx, "contexte dépassé");
        let h = self.cfg.hidden;
        let eps = self.cfg.eps;
        let scale = 1.0 / ((self.mla.as_ref().unwrap()[0].qkn
                            + self.mla.as_ref().unwrap()[0].qkr) as f32).sqrt();
        let mut x = self.g.row_f32("token_embd.weight", tok as usize, h);
        let mut hn = vec![0f32; h];
        for l in self.couche_debut..self.couche_fin {
            let m = &self.mla.as_ref().unwrap()[l];
            let (nh, qkn, qkr, vd, kvl) = (m.nh, m.qkn, m.qkr, m.vd, m.kv_lora);
            // --- norme d'entrée
            Self::rmsnorm(&x, &m.attn_norm, eps, &mut hn);
            // --- requête : descente, norme, remontée, découpage nope / rope
            let mut qa = vec![0f32; m.q_lora];
            matvec_f32(&m.q_a, &hn, h, m.q_lora, &mut qa);
            let mut qan = vec![0f32; m.q_lora];
            Self::rmsnorm(&qa, &m.q_a_norm, eps, &mut qan);
            let nq = nh * (qkn + qkr);
            let mut qb = vec![0f32; nq];
            matvec_f32(&m.q_b, &qan, m.q_lora, nq, &mut qb);
            // --- KV : descente MQA, norme sur la partie latente, remontée
            let mut kva = vec![0f32; kvl + qkr];
            matvec_f32(&m.kv_a, &hn, h, kvl + qkr, &mut kva);
            let mut c_n = vec![0f32; kvl];
            Self::rmsnorm(&kva[..kvl], &m.kv_a_norm, eps, &mut c_n);
            let mut k_rope = kva[kvl..].to_vec();
            Self::rope(&mut k_rope, 1, qkr, pos, self.cfg.rope_base, qkr);
            // --- rotation des seules composantes « rope » de Q
            let mut q_rope = vec![0f32; nh * qkr];
            for hh in 0..nh {
                q_rope[hh * qkr..(hh + 1) * qkr]
                    .copy_from_slice(&qb[hh * (qkn + qkr) + qkn..(hh + 1) * (qkn + qkr)]);
            }
            Self::rope(&mut q_rope, nh, qkr, pos, self.cfg.rope_base, qkr);
            // --- écriture du cache LATENT
            {
                let (ckv, krop) = &mut self.mla_cache[l];
                ckv[pos * kvl..(pos + 1) * kvl].copy_from_slice(&c_n);
                krop[pos * qkr..(pos + 1) * qkr].copy_from_slice(&k_rope);
            }
            // --- attention : k_nope et v reconstruits à la lecture
            let n = pos + 1;
            let (ckv, krop) = &self.mla_cache[l];
            let mut sortie = vec![0f32; nh * vd];
            let mut kvt = vec![0f32; nh * (qkn + vd)];
            let mut sc = vec![0f32; n];
            for hh in 0..nh {
                let q_nope = &qb[hh * (qkn + qkr)..hh * (qkn + qkr) + qkn];
                let qr = &q_rope[hh * qkr..(hh + 1) * qkr];
                for t in 0..n {
                    matvec_f32(&m.kv_b, &ckv[t * kvl..(t + 1) * kvl], kvl, nh * (qkn + vd), &mut kvt);
                    let kt = &kvt[hh * (qkn + vd)..hh * (qkn + vd) + qkn];
                    let mut s = 0f32;
                    for i in 0..qkn { s += q_nope[i] * kt[i]; }
                    for i in 0..qkr { s += qr[i] * krop[t * qkr + i]; }
                    sc[t] = s * scale;
                }
                let mut mx = f32::NEG_INFINITY;
                for &v in sc.iter() { if v > mx { mx = v; } }
                let mut somme = 0f32;
                for v in sc.iter_mut() { let e = (*v - mx).exp(); *v = e; somme += e; }
                let inv = 1.0 / somme;
                for t in 0..n {
                    matvec_f32(&m.kv_b, &ckv[t * kvl..(t + 1) * kvl], kvl, nh * (qkn + vd), &mut kvt);
                    let vt = &kvt[hh * (qkn + vd) + qkn..(hh + 1) * (qkn + vd)];
                    let w = sc[t] * inv;
                    for i in 0..vd { sortie[hh * vd + i] += w * vt[i]; }
                }
            }
            // --- projection de sortie et résidu
            let mut o = vec![0f32; h];
            matvec_f32(&m.wo, &sortie, nh * vd, h, &mut o);
            for i in 0..h { x[i] += o[i]; }
            // --- FFN (les poids du harnais sont en f32, donc lus ici)
            Self::rmsnorm(&x, &m.ffn_norm, eps, &mut hn);
            let mut g_t = vec![0f32; m.ffn];
            let mut u_t = vec![0f32; m.ffn];
            matvec_f32(&m.gate, &hn, h, m.ffn, &mut g_t);
            matvec_f32(&m.up, &hn, h, m.ffn, &mut u_t);
            let mut act = vec![0f32; m.ffn];
            Self::activation(&mut g_t, &u_t, m.ffn, false);
            for i in 0..m.ffn { act[i] = g_t[i]; }
            let mut d = vec![0f32; h];
            matvec_f32(&m.down, &act, m.ffn, h, &mut d);
            for i in 0..h { x[i] += d[i]; }
        }
        if self.couche_fin >= self.cfg.n_layer && !self.flux_brut {
            Self::rmsnorm(&x, &self.out_norm, eps, &mut hn);
            hn
        } else {
            x
        }
    }

    /// Logits d'un état caché avec une tête **liée en f32** (le harnais MLA n'a
    /// pas de blocs Q8_0 : `logits` ne s'applique pas).
    pub fn logits_f32(&self, hn: &[f32]) -> Vec<f32> {
        let h = self.cfg.hidden;
        let v = self.cfg.vocab;
        let mut out = vec![0f32; v];
        for o in 0..v {
            let ligne = self.g.row_f32("token_embd.weight", o, h);
            let mut acc = 0f32;
            for i in 0..h { acc += ligne[i] * hn[i]; }
            out[o] = acc;
        }
        out
    }

    /// Un token, une position. Retourne l'état caché après la dernière norme.
    pub fn forward(&mut self, tok: u32, pos: usize) -> Vec<f32> {
        assert!(pos < self.ctx, "contexte dépassé ({pos} ≥ {})", self.ctx);
        self.jeton_trace += 1;
        // lus AVANT l'emprunt destructuré : la parcimonie par projection
        let tkp = self.act_topk_proj;
        let tkg = self.act_topk;
        let tk = |p: usize| if tkp[p] > 0 { tkp[p] } else { tkg };
        // Lus AVANT l'emprunt destructuré (comme la parcimonie par projection).
        let largeur_profil = self.cfg.ffn.max(self.cfg.ffn_exp);
        // Fils à donner à la déquantification des experts IQ. Lus avant
        // l'emprunt destructuré, comme le reste.
        let threads_iq = self.pool.threads().clamp(1, 8);
        // Diagnostic `DRAVE_DEBUG_ETAT=1` : la norme de l'état résiduel à chaque
        // couche. Un modèle qui prédit le MÊME jeton à toutes les positions a un
        // état qui ne dépend plus de l'entrée ; cette ligne dit à quelle couche
        // il cesse d'en dépendre (explosion, effondrement, ou rien du tout).
        let debug_etat = std::env::var("DRAVE_DEBUG_ETAT").is_ok();
        let debug_mla = std::env::var("DRAVE_DEBUG_MLA").is_ok();
        self.profil_jetons += 1;
        let Model { g, cfg, layers, out_norm, pool, kv, events, attn_events, kv_gpu,
                    attn_gpu_part, emb_imposee, paires, .. } = self;
        let h = cfg.hidden;
        let hd = cfg.head_dim;
        let nh = cfg.n_head;
        let nkv = cfg.n_kv_head;
        let rep = nh / nkv;
        let ctx = self.ctx;

        // Injection : un vecteur imposé (embedding d'image) remplace la ligne
        // `token_embd` pour cet appel, et seulement pour lui — c'est le seul
        // ajout d'architecture que la vision demande au moteur.
        let mut x = match emb_imposee.take() {
            Some(v) => v,
            None => g.row_f32("token_embd.weight", tok as usize, h),
        };
        let mut hn = vec![0f32; h];
        if debug_etat {
            let n2: f32 = x.iter().map(|v| v * v).sum();
            eprintln!("[etat] jeton {tok} pos {pos} : |emb| {:.4e} · début {:.4e} {:.4e} {:.4e}",
                      n2.sqrt(), x[0], x[1], x[2]);
        }
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

        // La plage PORTÉE par ce nœud (`couche_debut..couche_fin`), et non
        // `0..n_layer` : un nœud qui reçoit un flux reprend à SA première couche.
        // La boucle partait de zéro — le pilote calculait donc les 24 couches,
        // envoyait l'état final, et le pair les recalculait toutes par-dessus :
        // perplexité répartie 798,3 au lieu de 18,2. `forward_lot` et
        // `forward_mla` respectaient déjà la plage ; `forward` était l'exception.
        for l in self.couche_debut..self.couche_fin {
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
            if self.flux_force.is_some() {
                // Diagnostic : comparer ce que la trace impose à ce que le
                // calcul vient de produire. Un écart minuscule = la liste est
                // fidèle ; un écart énorme = le codage de la liste est faux.
                let verif = std::env::var("DRAVE_FLUX_VERIF").is_ok();
                let avant = if verif { hn.clone() } else { Vec::new() };
                let j = self.jeton_trace;
                let r = self.flux_force.as_mut().unwrap();
                r.appliquer(l, j as usize, &mut hn);
                if verif && r.servies < 4 {
                    let mut mx = 0f32;
                    let mut dyn_ = 0f32;
                    for (a, b) in avant.iter().zip(hn.iter()) {
                        mx = mx.max((a - b).abs());
                        dyn_ = dyn_.max(a.abs());
                    }
                    println!("[verif] couche {l} pos {pos} : écart max {mx:.3e} sur une \
dynamique de {dyn_:.3e} (relatif {:.2e})", mx / dyn_.max(1e-9));
                }
            } else if self.trace.is_some() {
                let mut tmp = Vec::with_capacity(h);
                if let Some((sv, sx)) = Self::quant_scratch(&hn, self.act_levels, self.act_thresh,
                                                            tk(0), self.act_renorm, &mut tmp) {
                    let mut actifs = vec![0i32; h];
                    for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { actifs[i as usize] = v; }
                    let j = self.jeton_trace;
                    self.trace.as_mut().unwrap().ecrire(l, j as usize, &actifs, sx);
                }
            }
            // ---- attention MLA ------------------------------------------
            // Deux architectures d'attention dans la même passe avant :
            // Q/K/V denses (Qwen, gpt-oss, Llama) ou projections de rang
            // faible avec cache LATENT (DeepSeek-V3/V4, Kimi, GLM). Le reste
            // de la couche — résidu, FFN dense ou mélange d'experts, tête —
            // est partagé, et c'est ce qui compte : dupliquer la couche pour
            // deux attentions aurait donné deux MoE qui divergent.
            let ta = Instant::now();
            if let Some(m) = self.mla.as_ref().map(|v| &v[l]) {
                Self::attn_mla(m, &mut self.mla_cache[l], &hn, pos, cfg.rope_base, &mut att,
                               &mut paires[0], attn_events);
                if debug_mla && l == 0 {
                    eprintln!("[mla] couche 0 pos {pos} att[..8] {:.5e} {:.5e} {:.5e} {:.5e} {:.5e} {:.5e} {:.5e} {:.5e}",
                              att[0], att[1], att[2], att[3], att[4], att[5], att[6], att[7]);
                }
            } else {
                Self::matvec(pool, &lay.wq, &hn, &mut q, events, &mut paires[0], self.act_levels, self.act_thresh, tk(0), self.act_renorm, &mut scratch, self.seuil_push);
                Self::matvec(pool, &lay.wk, &hn, &mut k, events, &mut paires[0], self.act_levels, self.act_thresh, tk(1), self.act_renorm, &mut scratch, self.seuil_push);
                Self::matvec(pool, &lay.wv, &hn, &mut v, events, &mut paires[0], self.act_levels, self.act_thresh, tk(2), self.act_renorm, &mut scratch, self.seuil_push);
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
                // écriture du cache KV à la position courante
                {
                    let kvc = &mut kv[l];
                    for hh in 0..nkv {
                        kvc.ecrire(hh, pos, &k[hh * hd..(hh + 1) * hd], &v[hh * hd..(hh + 1) * hd]);
                    }
                }
                KvCache::miroir_gpu(kv_gpu.as_deref_mut(), l, &kv[l], pos, 1);
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
                // ---- KV déporté (étape E4) : la MÊME attention, calculée en VRAM.
                // Le noyau a besoin d'un nombre entier de têtes de requête par tête
                // KV ; la fenêtre et le top-k gardent le chemin CPU.
                let mut fait_en_gpu = false;
                if groupe && kv_gpu.is_some() && nkv * rep == nh && n > 1 {
                    let nsplit = (n / 256).clamp(1, 128);
                    let besoin = nsplit * nkv * rep * (hd + 2);
                    if attn_gpu_part.len() < besoin { attn_gpu_part.resize(besoin, 0.0); }
                    let puits: Option<Vec<f32>> = lay.sinks.as_ref()
                        .map(|s| (0..nh).map(|h| s[h]).collect());
                    if let Some((idx, m)) = kv_gpu.as_mut().and_then(|v| v.get_mut(l)) {
                        let machine = crate::gpu::machines()[*idx];
                        if machine.attn_kv(m, &q[..nh * hd], n, scale, puits.as_deref(),
                                           nsplit, attn_gpu_part, &mut att[..]) {
                            *attn_events += (nh * n) as u64;
                            fait_en_gpu = true;
                        }
                    }
                }
                if groupe && !fait_en_gpu {
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
                        *attn_events += ((h1 - h0) * n) as u64;
                    }
                }
                // ---- top-k déporté (étape 4 du plan) -------------------------
                // Le miroir VRAM était interdit dès que `attn_topk > 0` : la
                // notation restait donc sur CPU, où elle coûte 968 ms par couche à
                // 1 M de clés. Les trois noyaux du plan (scores sans relecture,
                // seuil radix, collecte, somme) rendent maintenant le chemin
                // complet en VRAM — mesuré 3,90 ms pour 14 lignes × 1 M de clés,
                // contre 539,9 ms pour l'attention complète sur CPU.
                //
                // Opt-in par `DRAVE_GPU_TOPK=1` : le chemin CPU reste le défaut tant
                // que la porte de perplexité n'a pas montré l'égalité, et tout refus
                // d'un noyau retombe proprement sur le CPU (aucun résultat partiel
                // n'est publié).
                // `=0` veut dire NON : la convention `is_ok()` du dépôt fait qu'une
                // variable mise à 0 par un script active le chemin — un piège de
                // mesure pour un A/B qui ne bascule que par la variable.
                let topk_gpu_demande = std::env::var("DRAVE_GPU_TOPK")
                    .map(|v| v != "0" && !v.is_empty()).unwrap_or(false);
                // Les limites du noyau 3 sont testées ICI, pas après sept
                // lancements : `--attn-topk 2048` ou `DRAVE_KV_BITS=4` refaisaient
                // toute la chaîne GPU par couche et par jeton avant de rendre la
                // main au CPU — plus lent que le CPU seul, et une ligne d'erreur par
                // couche et par jeton.
                let topk_gpu_possible = self.attn_topk > 0 && self.attn_topk.min(n) <= 1024
                    && (kvc.bits == 8 || kvc.bits == 32);
                if topk_gpu_possible && fen == 0 && kv_gpu.is_some()
                    && nkv * rep == nh && n > 1 && topk_gpu_demande
                {
                    let k = self.attn_topk.min(n);
                    if let Some((idx, m)) = kv_gpu.as_mut().and_then(|v| v.get_mut(l)) {
                        let machine = crate::gpu::machines()[*idx];
                        let puits: Option<Vec<f32>> = lay.sinks.as_ref()
                            .map(|s| (0..nh).map(|h| s[h]).collect());
                        // Noyau fusionné (descente + collecte + somme en UN lancement)
                        // tant qu'il est mesuré plus rapide que la chaîne séparée :
                        // 0,13 contre 0,22 ms à 4 k clés, 0,85 contre 0,89 à 131 k —
                        // au-delà (262 k : 1,58 contre 1,35) la chaîne reprend, car
                        // ses 1 792 blocs saturent mieux la VRAM que les 14 blocs du
                        // noyau fusionné. Le seuil est MESURÉ, pas choisi.
                        const SEUIL_NOYAU4: usize = 131_072;
                        if n <= SEUIL_NOYAU4 {
                            let mut ok = machine.attn_scores_sans_relecture(m, &q[..nh * hd], n, scale);
                            if ok {
                                ok = machine.attn_topk_tout(m, nh, n, k, hd, rep, puits.as_deref(),
                                                            &mut att[..nh * hd]);
                            }
                            if ok {
                                *attn_events += (nh * k) as u64;
                                fait_en_gpu = true;
                            } else if !TOPK_GPU_ECHEC.swap(true, std::sync::atomic::Ordering::Relaxed) {
                                eprintln!("[topk] noyau fusionné en échec : repli CPU (message unique)");
                            }
                        } else {
                        let mut pref = vec![0u32; nh];
                        let mut dessus = vec![0usize; nh];
                        let mut hist = vec![0u32; nh * 256];
                        let mut ok = machine.attn_scores_sans_relecture(m, &q[..nh * hd], n, scale);
                        let mut dec = 24i32;
                        while ok && dec >= 0 {
                            ok = machine.attn_topk_histo(m, nh, n, dec, &pref, &mut hist);
                            for hh in 0..nh {
                                let h = &hist[hh * 256..(hh + 1) * 256];
                                let mut cum = dessus[hh];
                                let mut b = 256usize;
                                while b > 0 && cum < k { b -= 1; cum += h[b] as usize; }
                                dessus[hh] = cum - h[b] as usize;
                                pref[hh] = (pref[hh] << 8) | b as u32;
                            }
                            dec -= 8;
                        }
                        let besoin: Vec<i32> = (0..nh).map(|hh| (k - dessus[hh]) as i32).collect();
                        let mut sel = vec![-1i32; nh * k];
                        if ok {
                            ok = machine.attn_topk_collecte(m, nh, n, k, &pref, &besoin, &mut sel);
                        }
                        // Une case non écrite laisserait le noyau 3 lire un indice
                        // PÉRIMÉ du jeton précédent (le tampon VRAM n'est pas remis à
                        // zéro) : sortie plausible et fausse, publiée sans un mot. Le
                        // contrôle est gratuit — `sel` vient d'être recopié.
                        if ok && sel.iter().any(|&v| v < 0) {
                            eprintln!("[topk] collecte incomplète (case non écrite) : repli CPU");
                            ok = false;
                        }
                        if ok {
                            ok = machine.attn_topk_somme(m, nh, n, k, hd, rep, puits.as_deref(),
                                                         &mut att[..nh * hd]);
                        }
                        if ok {
                            // Même unité que le chemin CPU (`iter.len()` = k paires
                            // retenues par tête) : compter `nh * n` ici faisait
                            // varier la ligne « paires (requête, clé) par token »
                            // d'un facteur n/k selon le drapeau, à calcul identique.
                            *attn_events += (nh * k) as u64;
                            fait_en_gpu = true;
                        } else if !TOPK_GPU_ECHEC.swap(true, std::sync::atomic::Ordering::Relaxed) {
                            // Un échec par couche et par jeton ferait des milliers de
                            // lignes : on le dit UNE fois, et le repli CPU est
                            // silencieux ensuite (les raisons, elles, sont imprimées
                            // par le noyau fautif).
                            eprintln!("[topk] chaîne déportée en échec : repli CPU (message unique)");
                        }
                        }
                    }
                }
                for hh in 0..(if groupe || fait_en_gpu { 0 } else { nh }) {
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
                        *attn_events += iter.len() as u64;
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
                        // ⚠️ `select_nth_unstable_by` n'est PAS stable : lequel des
                        // ex æquo tombe avant le rang k dépend de la partition. Le
                        // noyau GPU, lui, garde les PREMIERS égaux par ordre d'indice
                        // — deux chemins qui prétendaient au même départage et ne
                        // l'avaient pas (relevé par une relecture adversariale). On
                        // garde la sélection pour trouver la VALEUR du k-ième (elle
                        // est juste même si l'élément choisi ne l'est pas), puis on
                        // reconstruit l'ensemble en ordre d'indice : au-dessus du
                        // seuil d'abord, puis les premiers égaux — exactement la
                        // convention du noyau.
                        attn_idx.extend(0..n as u32);
                        attn_idx.select_nth_unstable_by(k, |&a, &b| {
                            sc[b as usize].partial_cmp(&sc[a as usize]).unwrap()
                        });
                        let seuil = sc[attn_idx[k] as usize];
                        attn_idx.clear();
                        let mut sup = 0usize;
                        for t in 0..n {
                            if sc[t] > seuil { attn_idx.push(t as u32); sup += 1; }
                        }
                        let besoin = k - sup;
                        let mut pris = 0usize;
                        for t in 0..n {
                            if sc[t] == seuil && pris < besoin {
                                attn_idx.push(t as u32);
                                pris += 1;
                            }
                        }
                    }
                    // en mode dense, seules les n premières clés existent : itérer
                    // sur tout le contexte lirait des scores au-delà de pos.
                    let iter: &[u32] = if k < n { &attn_idx } else { &attn_all[..n] };
                    *attn_events += iter.len() as u64;
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
            }
            // Chronométré APRÈS la branche : les deux chemins d'attention
            // doivent apparaître dans le même poste, sinon la comparaison des
            // profils entre un modèle MLA et un modèle dense serait fausse.
            self.prof[2] += ta.elapsed().as_secs_f64();
            let tf = Instant::now();
            // `att` est dimensionné en `nh × head_dim`, mais un chemin MLA n'en
            // remplit que `nh × vd` : passer le tampon entier quantifiait des
            // valeurs périmées (voir `matvec`).
            let n_att = match self.mla.as_ref().map(|v| &v[l]) {
                Some(m) => m.nh * m.vd,
                None => att.len(),
            };
            Self::matvec(pool, &lay.wo, &att[..n_att.min(att.len())], &mut o, events, &mut paires[0], self.act_levels, self.act_thresh, tk(3), self.act_renorm, &mut scratch, self.seuil_push);
            for i in 0..h { o[i] += x[i]; }
            Self::rmsnorm(&o, &lay.ffn_norm, cfg.eps, &mut hn);
            if let Some(r) = self.flux_force.as_mut() {
                let j = self.jeton_trace;
                r.appliquer(l + 1000, j as usize, &mut hn);
            } else if self.trace.is_some() {
                let mut tmp = Vec::with_capacity(h);
                if let Some((sv, sx)) = Self::quant_scratch(&hn, self.act_levels, self.act_thresh,
                                                            tk(3), self.act_renorm, &mut tmp) {
                    let mut actifs = vec![0i32; h];
                    for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { actifs[i as usize] = v; }
                    let j = self.jeton_trace;
                    self.trace.as_mut().unwrap().ecrire(l + 1000, j as usize, &actifs, sx);
                }
            }
            // ------------------------------------------------------ MoE
            // Un routeur linéaire choisit `k` experts parmi `n` ; seuls leurs
            // poids sont lus. C'est la parcimonie **structurelle** — 8 experts
            // sur 128, soit 6 % du FFN — et c'est le régime où l'architecture
            // événementielle cesse d'être un coût.
            if let Some(moe) = lay.moe.as_ref() {
                let ne = cfg.n_expert;
                let k = if self.moe_topk > 0 { self.moe_topk } else { cfg.n_expert_used };
                let k = k.clamp(1, ne);
                // Une seule implémentation du routage, partagée avec le lot.
                let choix = router(cfg, moe, &hn, tok, k);
                let idx: Vec<usize> = choix.iter().map(|(e, _)| *e).collect();
                let poids: Vec<f32> = choix.iter().map(|(_, p)| *p).collect();
                if self.profil_experts.is_some() {
                    let base = l * ne;
                    let p = self.profil_experts.as_mut().unwrap();
                    for &e in &idx { p[base + e as usize] += 1; }
                }
                if let Some(f) = self.trace_experts.as_mut() {
                    use std::io::Write;
                    let mut ids: Vec<usize> = idx.clone();
                    ids.sort_unstable();       // l'ordre de `select_nth` est arbitraire
                    let liste: Vec<String> = ids.iter().map(|e| e.to_string()).collect();
                    let _ = writeln!(f, "{} {} {}", l, pos, liste.join(" "));
                }
                for v in down.iter_mut() { *v = 0.0; }
                // Prélecture : on connaît les experts du jeton AVANT de les
                // calculer. Les demander tous d'un coup laisse le noyau lancer
                // ses lectures de pages en parallèle — mesuré, le NVMe passe de
                // 5,4 à 31 Go/s quand les lectures se recouvrent.
                for &e in &idx {
                    if let Some((k, loc)) = moe.ou(e) {
                        moe.gate[k].prelire_expert(loc);
                        moe.up[k].prelire_expert(loc);
                        moe.down[k].prelire_expert(loc);
                    }
                }
                for (&e, &poids_exp) in idx.iter().zip(poids.iter()) {
                    let w_exp = poids_exp;
                    // Traduction pour les modèles en clusters : l'expert global
                    // `e` n'est pas forcément dans ce nœud.
                    let Some((kexp, loc)) = moe.ou(e) else { continue; };
                    // ---- experts MXFP4 sur le GPU ----
                    // Le noyau MXFP4 est BIT À BIT identique au chemin CPU
                    // (écart mesuré 0,00e0 sur un expert) : seule la vitesse
                    // change, la perplexité ne peut pas bouger. Les poids
                    // montent une fois et restent (cache LRU), sinon on
                    // repasserait 4,4 Mo sur le bus à chaque jeton.
                    let mut fait = false;
                    if moe.gate[0].src == crate::list::Source::Mxfp4 && moe.local.is_none() {
                        if let (Some(machine), Some(cache)) =
                                (crate::gpu::instance(), self.cache_experts.as_mut()) {
                            if let Some((mg, mu, md)) = cache.obtenir(machine, l, e as usize,
                                                                      &moe.gate[0], &moe.up[0], &moe.down[0]) {
                                fait = Self::expert_mxfp4_gpu(
                                    machine, mg, mu, md, &hn, &mut gate, &mut up, &mut exp_out,
                                    &mut down, w_exp, moe, e as usize, cfg.ffn_exp, h,
                                    self.act_levels, self.act_thresh, tk(4), tk(5), tk(6),
                                    self.act_renorm, cfg.ffn_act_oss, &mut scratch);
                            }
                        }
                    }
                    if fait {
                        Self::compter_neurones(&mut self.profil_neurones, largeur_profil,
                                               l, &gate[..cfg.ffn_exp]);
                        continue;
                    }
                    let mg = moe.gate[kexp].expert(loc);
                    Self::matvec4_ou_iq(pool, &moe.gate[kexp], loc, &hn, &mut gate, &mut paires[1],
                                        self.act_levels,
                                        self.act_thresh, tk(4), self.act_renorm, &mut scratch,
                                        moe.biais_gate.as_ref().map(|b| &b[e as usize * moe.n_ff..]),
                                        threads_iq);
                    let mu = moe.up[kexp].expert(loc);
                    Self::matvec4_ou_iq(pool, &moe.up[kexp], loc, &hn, &mut up, &mut paires[1],
                                        self.act_levels,
                                        self.act_thresh, tk(5), self.act_renorm, &mut scratch,
                                        moe.biais_up.as_ref().map(|b| &b[e as usize * moe.n_ff..]),
                                        threads_iq);
                    Self::activation(&mut gate, &up, cfg.ffn_exp, cfg.ffn_act_oss);
                    Self::compter_neurones(&mut self.profil_neurones, largeur_profil,
                                           l, &gate[..cfg.ffn_exp]);
                    let md = moe.down[kexp].expert(loc);
                    Self::matvec4_ou_iq(pool, &moe.down[kexp], loc, &gate, &mut exp_out, &mut paires[1],
                                    self.act_levels, self.act_thresh, tk(6), self.act_renorm, &mut scratch,
                                    // Le biais de descente se découpe par la
                                    // largeur de SORTIE (h), pas par n_ff : les
                                    // deux coïncident sur gpt-oss (2 880) mais
                                    // pas sur Qwen3-MoE (768 contre 2 048).
                                    moe.biais_down.as_ref().map(|b| &b[e as usize * h..]),
                                    threads_iq);
                    for i in 0..h { down[i] += w_exp * exp_out[i]; }
                }
                if let Some((sg, su, sd)) = moe.shexp.as_ref() {
                    Self::matvec4_ou_iq(pool, sg, 0, &hn, &mut gate, &mut paires[2], self.act_levels,
                                    self.act_thresh, tk(4), self.act_renorm, &mut scratch, None,
                                    threads_iq);
                    Self::matvec4_ou_iq(pool, su, 0, &hn, &mut up, &mut paires[2], self.act_levels,
                                    self.act_thresh, tk(5), self.act_renorm, &mut scratch, None,
                                    threads_iq);
                    Self::activation(&mut gate, &up, cfg.ffn_exp, cfg.ffn_act_oss);
                    Self::matvec4_ou_iq(pool, sd, 0, &gate, &mut exp_out, &mut paires[2], self.act_levels,
                                    self.act_thresh, tk(6), self.act_renorm, &mut scratch, None,
                                    threads_iq);
                    for i in 0..h { down[i] += exp_out[i]; }
                }
                if let Some((gl, gg)) = self.ffn_gain {
                    if gl == l { for v in down.iter_mut() { *v *= gg; } }
                }
                for i in 0..h { x[i] = o[i] + down[i]; }
                if debug_etat {
                    let n2: f32 = x.iter().map(|v| v * v).sum();
                    let na: f32 = att.iter().map(|v| v * v).sum();
                    let nd: f32 = down.iter().map(|v| v * v).sum();
                    eprintln!("[etat] couche {l:3} pos {pos} : |x| {:.4e} · |att| {:.4e} · \
|ffn| {:.4e}", n2.sqrt(), na.sqrt(), nd.sqrt());
                }
                self.prof[3] += tf.elapsed().as_secs_f64();
                continue;
            }
            Self::matvec(pool, &lay.wgate, &hn, &mut gate, events, &mut paires[2], self.act_levels, self.act_thresh, tk(4), self.act_renorm, &mut scratch, self.seuil_push);
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
            Self::matvec(pool, &lay.wup, &hn, &mut up, events, &mut paires[2], self.act_levels, self.act_thresh, tk(5), self.act_renorm, &mut scratch, self.seuil_push);
            Self::activation(&mut gate, &up, cfg.ffn, cfg.ffn_act_oss);
            Self::compter_neurones(&mut self.profil_neurones, largeur_profil,
                                   l, &gate[..cfg.ffn]);
            Self::matvec(pool, &lay.wdown, &gate, &mut down, events, &mut paires[2], self.act_levels, self.act_thresh, tk(6), self.act_renorm, &mut scratch, self.seuil_push);
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
            if debug_mla && l == 0 {
                eprintln!("[mla] couche 0 pos {pos} x[..8] {:.5e} {:.5e} {:.5e} {:.5e} \
{:.5e} {:.5e} {:.5e} {:.5e}", x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]);
            }
            if debug_etat {
                let n2: f32 = x.iter().map(|v| v * v).sum();
                let na: f32 = att.iter().map(|v| v * v).sum();
                let nd: f32 = down.iter().map(|v| v * v).sum();
                eprintln!("[etat] couche {l:3} pos {pos} : |x| {:.4e} · |att| {:.4e} · \
|ffn| {:.4e} (dense)", n2.sqrt(), na.sqrt(), nd.sqrt());
            }
            self.prof[3] += tf.elapsed().as_secs_f64();
        }
        if self.flux_brut || self.couche_fin < cfg.n_layer {
            return x;                       // nœud intermédiaire : flux brut
        }
        Self::rmsnorm(&x, out_norm, cfg.eps, &mut hn);
        hn
    }

    /// **Tête de sortie par lots** : la même matrice pour `t` états cachés.
    ///
    /// La tête est la plus grosse matrice du modèle (151 936 × 896 pour Qwen
    /// 0.5B, 145 Mo lus par jeton) et elle restait calculée jeton par jeton dans
    /// le chemin par lots : c'était 25 % du temps. Ici la ligne de poids reste au
    /// chaud pendant qu'elle sert `TUILE_TETE` jetons.
    pub fn logits_lot(&mut self, hs: &[Vec<f32>]) -> Vec<Vec<f32>> {
        const TUILE_TETE: usize = 16;
        let t = hs.len();
        if t == 0 { return Vec::new(); }
        if t == 1 { return vec![self.logits(&hs[0])]; }
        let h = self.cfg.hidden;
        // 1. quantification de chaque état caché (mêmes règles que `logits`)
        let mut qx: Vec<i16> = vec![0i16; t * h];
        let mut sxs = vec![0f32; t];
        let mut scratch: Vec<f32> = Vec::with_capacity(h);
        for (i, hi) in hs.iter().enumerate() {
            let (sv, sx) = match Self::quant_scratch(hi, self.act_levels, self.act_thresh,
                                                     self.act_topk, self.act_renorm, &mut scratch) {
                Some(v) => v,
                None => (SparseVec { idx: Vec::new(), val: Vec::new() }, 1.0),
            };
            sxs[i] = sx;
            for (&j, &val) in sv.idx.iter().zip(sv.val.iter()) {
                qx[i * h + j as usize] = val.clamp(-32767, 32767) as i16;
            }
        }
        // Tête déportée : un appel par jeton (le noyau avale une ligne de
        // vocabulaire entière, il n'a pas besoin du lot pour être efficace).
        // Sans ce chemin, une mesure de perplexité — qui passe toujours par des
        // lots — n'aurait jamais touché le GPU.
        if self.tete_gpu.is_some() {
            let mut xd = vec![0i32; h];
            let mut tous: Vec<Vec<f32>> = Vec::with_capacity(t);
            let mut complet = true;
            for i in 0..t {
                for (a, &b) in xd.iter_mut().zip(qx[i * h..(i + 1) * h].iter()) {
                    *a = b as i32;
                }
                match self.logits_gpu(&xd, sxs[i]) {
                    Some(y) => tous.push(y),
                    None => { complet = false; break; }
                }
            }
            if complet { return tous; }
        }
        let vocab = self.cfg.vocab;
        let nt = self.pool.threads().max(1);
        // Liste restreinte : on ne calcule QUE ces lignes. Les autres restent à
        // zéro, ce qui suffit à la génération (elles ne seront jamais choisies)
        // et serait faux pour une perplexité — d'où le refus explicite ailleurs.
        let lignes: Vec<u32> = match &self.tete_restreinte {
            Some(l) => l.clone(),
            None => (0..vocab as u32).collect(),
        };
        // Répartition sur les THREADS par sous-listes disjointes, et non par
        // tranches de `out` : avec une liste restreinte, les lignes à écrire ne
        // sont plus contiguës, donc `chunks_mut` écrirait aux mauvaises places.
        // L'écriture passe par un pointeur brut ; la sûreté tient à ce que les
        // sous-listes sont disjointes par construction, donc les indices
        // `o * t + i` aussi.
        let tranche = lignes.len().div_ceil(nt.max(1)).max(1);
        let sous_listes: Vec<&[u32]> = lignes.chunks(tranche).collect();
        let mut out = vec![0f32; vocab * t];
        if let Some(d) = self.head4.take() {
            let dref = &d;
            let s32: Vec<Vec<i32>> = (0..t)
                .map(|i| crate::list::sommes32(&qx[i * h..(i + 1) * h])).collect();
            let (qxr, s32r, sxsr) = (&qx, &s32, &sxs);
            let base_out = out.as_mut_ptr() as usize;
            std::thread::scope(|sc| {
                for sous in &sous_listes {
                    let base_out = base_out;
                    sc.spawn(move || {
                        for i0 in (0..t).step_by(TUILE_TETE) {
                            let i1 = (i0 + TUILE_TETE).min(t);
                            for &o in sous.iter() {
                                let o = o as usize;
                                for i in i0..i1 {
                                    let v = dref.dot16(o, &qxr[i * h..(i + 1) * h],
                                                      &s32r[i]) * sxsr[i];
                                    unsafe { *(base_out as *mut f32).add(o * t + i) = v; }
                                }
                            }
                        }
                    });
                }
            });
            self.head4 = Some(d);
        } else {
            let view = self.g.q8_view(&self.tete);
            let g = &self.g;
            let view = &view;
            let (qxr, sxsr) = (&qx, &sxs);
            let base_out = out.as_mut_ptr() as usize;
            std::thread::scope(|sc| {
                for sous in &sous_listes {
                    let base_out = base_out;
                    sc.spawn(move || {
                        for i0 in (0..t).step_by(TUILE_TETE) {
                            let i1 = (i0 + TUILE_TETE).min(t);
                            for &o in sous.iter() {
                                let o = o as usize;
                                for i in i0..i1 {
                                    let v = g.q8_dot_at(view, o, &qxr[i * h..(i + 1) * h]) * sxsr[i];
                                    unsafe { *(base_out as *mut f32).add(o * t + i) = v; }
                                }
                            }
                        }
                    });
                }
            });
        }
        (0..t).map(|i| (0..vocab).map(|o| out[o * t + i]).collect()).collect()
    }

    /// Tête sur le GPU. `None` si aucune tête n'est déportée ou si le noyau
    /// échoue : l'appelant retombe alors sur le CPU. Les deux noyaux ne
    /// s'appellent pas de la même façon — `proj_q6k` applique l'échelle
    /// d'activation, `tete_warp` la laisse à l'appelant.
    fn logits_gpu(&self, xd: &[i32], sx: f32) -> Option<Vec<f32>> {
        let machine = crate::gpu::instance()?;
        let m = self.tete_gpu.as_ref()?;
        if self.tete_gpu_q6k {
            machine.proj_q6k(m, xd, sx)
        } else {
            machine.tete_warp(m, xd).map(|y| y.iter().map(|v| v * sx).collect())
        }
    }

    /// **Encode un flux pour le réseau** : la même quantification que la trace
    /// (mêmes `act_levels`, `act_thresh`, `act_topk`, `act_renorm`), donc les
    /// mêmes octets que sur le disque — indice `u16`, valeur `i16`, une échelle
    /// par liste. Transporter la LISTE au lieu du vecteur dense est le sujet de
    /// la phase 3 : « des listes, pas des matrices » vaut aussi sur le câble.
    pub fn flux_en_liste(&self, x: &[f32]) -> (Vec<u16>, Vec<i16>, f32) {
        assert!(x.len() <= u16::MAX as usize,
                "flux de {} canaux : l'indice u16 ne suffit pas", x.len());
        let mut scratch = Vec::with_capacity(x.len());
        // Le champ de valeur du fil fait 16 bits : on quantifie donc sur 32 767
        // niveaux, PAS sur `act_levels`. C'est gratuit — deux octets par valeur
        // dans les deux cas — et mesuré : à 127 niveaux, l'écart de perplexité du
        // découpage passait de quelques pour mille à ×2. Le seuil, lui, reste
        // celui du modèle : c'est lui qui décide de la sparsité, donc de la taille.
        match Self::quant_scratch(x, 32767.0, self.act_thresh, self.act_topk,
                                  self.act_renorm, &mut scratch) {
            Some((sv, sx)) => (sv.idx.iter().map(|&i| i as u16).collect(),
                               sv.val.iter().map(|&v| v.clamp(i16::MIN as i32,
                                                              i16::MAX as i32) as i16).collect(),
                               sx),
            None => (Vec::new(), Vec::new(), 0.0),
        }
    }

    /// **Liste à échelle par bloc de 32 canaux** : trois octets par neurone actif
    /// (indice u16, valeur i8) plus une échelle f32 par bloc.
    ///
    /// Pourquoi ce mode existe : le résidu brut a une dynamique large, donc une
    /// échelle UNIQUE par vecteur donne une erreur *absolue* constante — énorme
    /// en relatif sur les petits canaux (2,6 % de perplexité à 16 bits pleins,
    /// mesuré). Une échelle par bloc borne l'erreur relative à l'intérieur du
    /// bloc, ce qui permet de descendre la valeur à UN octet : moins d'octets
    /// par neurone actif ET une précision localement meilleure.
    ///
    /// Le seuil, lui, reste GLOBAL (fraction du maximum du vecteur) : c'est lui
    /// qui décide de la sparsité, donc de la taille sur le fil.
    pub fn flux_en_liste_blocs(&self, x: &[f32]) -> (Vec<u16>, Vec<i8>, Vec<f32>) {
        const BLOC: usize = 32;
        // La même garde que `flux_en_liste` : au-delà de 65 535 canaux, l'indice
        // u16 tronque EN SILENCE (les modes 2 et 4 en dépendent).
        assert!(x.len() <= u16::MAX as usize,
                "flux de {} canaux : l'indice u16 ne suffit pas", x.len());
        let n_blocs = x.len().div_ceil(BLOC);
        let mut echelles = vec![0f32; n_blocs];
        let mut mx = 0f32;
        for &v in x { let a = v.abs(); if a > mx { mx = a; } }
        let seuil = self.act_thresh * mx;
        let mut idx: Vec<u16> = Vec::new();
        let mut val: Vec<i8> = Vec::new();
        for b in 0..n_blocs {
            let lo = b * BLOC;
            let hi = (lo + BLOC).min(x.len());
            let mut mb = 0f32;
            for &v in &x[lo..hi] { let a = v.abs(); if a > mb { mb = a; } }
            if mb == 0.0 { continue; }
            let ech = mb / 127.0;
            echelles[b] = ech;
            for (k, &v) in x[lo..hi].iter().enumerate() {
                if v.abs() <= seuil { continue; }
                let q = (v / ech).round().clamp(-127.0, 127.0);
                if q != 0.0 { idx.push((lo + k) as u16); val.push(q as i8); }
            }
        }
        (idx, val, echelles)
    }

    /// Norme finale, pour un état venu d'un AUTRE nœud : le nœud distant rend le
    /// flux résiduel brut, c'est le dernier qui norme.
    pub fn norme_finale(&self, x: &[f32]) -> Vec<f32> {
        let mut hn = vec![0f32; self.cfg.hidden];
        Self::rmsnorm(x, &self.out_norm, self.cfg.eps, &mut hn);
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
        // La tête est la plus grosse matrice du modèle et elle est TOUJOURS
        // dense : la compter dans « partagé » est ce qui explique qu'un petit
        // modèle ait un flux partagé énorme (Qwen 0.5B : 136 M paires pour la
        // seule tête, contre 313 M pour ses 24 FFN).
        self.paires[2] += (h.len() as u64) * (self.cfg.vocab as u64);
        // Chemin GPU : les poids de la tête sont déjà en mémoire vidéo ; seules
        // les activations montent et les logits descendent.
        if self.tete_gpu.is_some() {
            let mut xd = vec![0i32; h.len()];
            for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { xd[i as usize] = v; }
            if let Some(y) = self.logits_gpu(&xd, sx) { return y; }
        }
        // Tête 4 bits : chemin DIRECT par tranches de vocabulaire, comme la tête
        // int8 — et non par le pool. Le pool coûtait 4 ms de plus par jeton pour
        // 72 Mo lus au lieu de 136 : ses seize tampons de sortie (9,7 Mo) sont
        // écrits, remis à zéro puis réduits, soit plus de trafic que les poids
        // économisés.
        // Densité de l'entrée de la tête : `sv.idx` porte les coordonnées
        // vivantes après quantification. Si elle est faible, un stockage par
        // COLONNES permettrait de ne lire que ces colonnes — exactement, sans
        // borne ni approximation. On la mesure avant de s'engager.
        TETE_ACTIFS.fetch_add(sv.idx.len() as u64, std::sync::atomic::Ordering::Relaxed);
        TETE_TOTAL.fetch_add(h.len() as u64, std::sync::atomic::Ordering::Relaxed);
        TETE_APPELS.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
        if self.head4.is_some() {
            let xi: Vec<i16> = sv.idx.iter().zip(sv.val.iter())
                .fold(vec![0i16; h.len()], |mut a, (&i, &v)| {
                    a[i as usize] = v.clamp(-32767, 32767) as i16; a
                });
            let d = self.head4.take().unwrap();
            let dref = &d;
            let vocab = d.n_out;


            // Liste restreinte : ne calculer que ces lignes. `chunks_mut` ne
            // convient plus, les lignes n'étant pas contiguës — on passe par un
            // pointeur brut, sûr parce que les sous-listes sont disjointes.
            let lignes: Vec<u32> = match &self.tete_restreinte {
                Some(l) => l.clone(),
                None => (0..vocab as u32).collect(),
            };
            let nt = self.pool.threads().max(1);
            let tranche = lignes.len().div_ceil(nt).max(1);
            let mut out = vec![0f32; vocab];
            let xi = &xi;
            let sx32 = &crate::list::sommes32(xi);
            let base_out = out.as_mut_ptr() as usize;
            std::thread::scope(|sc| {
                for sous in lignes.chunks(tranche) {
                    let base_out = base_out;
                    sc.spawn(move || {
                        for &o in sous.iter() {
                            let v = dref.dot16(o as usize, xi, sx32) * sx;
                            unsafe { *(base_out as *mut f32).add(o as usize) = v; }
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
        let lignes: Vec<u32> = match &self.tete_restreinte {
            Some(l) => l.clone(),
            None => (0..vocab as u32).collect(),
        };
        let tranche = lignes.len().div_ceil(nt).max(1);
        let mut out = vec![0f32; vocab];
        let g = &self.g;
        let view = &view;
        let base_out = out.as_mut_ptr() as usize;
        std::thread::scope(|s| {
            for sous in lignes.chunks(tranche) {
                let qx = &qx;
                let base_out = base_out;
                s.spawn(move || {
                    for &o in sous.iter() {
                        let v = g.q8_dot_at(view, o as usize, qx) * sx;
                        unsafe { *(base_out as *mut f32).add(o as usize) = v; }
                    }
                });
            }
        });
        out
    }

    /// Calcule `||w_i||` pour toutes les lignes de la tête, et l'ordre des
    /// lignes par norme décroissante. Coût : UNE passe sur la matrice de tête
    /// (3,4 ms pour 151 936 × 896 en Q8_0), payée une fois.
    pub fn preparer_normes_tete(&mut self) {
        if self.normes_tete.is_some() { return; }
        let vocab = self.cfg.vocab;
        let view = self.g.q8_view(&self.tete);
        let (buf, nb) = match self.g.q8_blocks(&self.tete) {
            Some(v) => v,
            None => {
                eprintln!("[tete-garantie] la tête « {} » n'est pas Q8_0 : les normes de \
lignes ne sont pas calculées, la restriction garantie est indisponible", self.tete);
                return;
            }
        };
        let mut normes = vec![0f32; vocab];
        let nt = self.pool.threads().max(1);
        let tranche = vocab.div_ceil(nt).max(1);
        let base = buf.as_ptr() as usize;
        let nb = nb;
        let out_ptr = normes.as_mut_ptr() as usize;
        std::thread::scope(|s| {
            for (t, _) in (0..vocab).collect::<Vec<_>>().chunks(tranche).enumerate() {
                let (lo, hi) = (t * tranche, ((t + 1) * tranche).min(vocab));
                s.spawn(move || {
                    for o in lo..hi {
                        let mut acc = 0f32;
                        for b in 0..nb {
                            let p = unsafe { (base as *const u8).add((o * nb + b) * 34) };
                            let d = crate::gguf::Gguf::f16_to_f32(u16::from_le_bytes(
                                [unsafe { *p }, unsafe { *p.add(1) }]));
                            let mut s2 = 0f32;
                            for j in 0..32 {
                                let q = unsafe { *p.add(2 + j) } as i8 as f32;
                                s2 += q * q;
                            }
                            acc += d * d * s2;
                        }
                        unsafe { *(out_ptr as *mut f32).add(o) = acc.sqrt(); }
                    }
                });
            }
        });
        let _ = view;
        let mut ordre: Vec<u32> = (0..vocab as u32).collect();
        ordre.sort_unstable_by(|&a, &b| normes[b as usize].partial_cmp(&normes[a as usize]).unwrap());
        println!("[tete-garantie] normes de {} lignes : max {:.4e} · médiane {:.4e} · min {:.4e}",
                 vocab, normes[ordre[0] as usize],
                 normes[ordre[vocab / 2] as usize],
                 normes[*ordre.last().unwrap() as usize]);
        self.normes_tete = Some(normes);
        self.ordre_normes = Some(ordre);
    }

    /// **Tête garantie** : les logits calculés suffisent à prouver l'argmax.
    ///
    /// On part de la liste de candidats, on borne toutes les autres lignes par
    /// `||w_i|| · ||h||`, et on étend par paliers tant qu'une ligne non calculée
    /// peut battre le meilleur logit connu. Rend `(logits, lignes calculées,
    /// borne du meilleur logit NON calculé)` ; quand la borne est sous le
    /// meilleur logit, l'argmax est exact — et quand la liste atteint le
    /// vocabulaire entier, il l'est aussi, par construction.
    pub fn logits_garanti(&mut self, h: &[f32]) -> (Vec<f32>, usize, f32) {
        let vocab = self.cfg.vocab;
        let mut scratch = Vec::with_capacity(h.len());
        let (sv, sx) = match Self::quant_scratch(h, self.act_levels, self.act_thresh,
                                                self.act_topk, self.act_renorm, &mut scratch) {
            Some(v) => v,
            None => return (vec![0f32; vocab], 0, 0.0),
        };
        let mut qx = vec![0i16; h.len()];
        for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { qx[i as usize] = v as i16; }
        // ||h|| dans la MÊME unité que les poids : `logits = Σ d·q·x·sx`, donc la
        // borne porte sur `||w|| · ||x·sx||`.
        let norme_h = (qx.iter().map(|&v| (v as f32) * (v as f32)).sum::<f32>()).sqrt() * sx;
        let normes = self.normes_tete.clone().expect("preparer_normes_tete d'abord");
        let ordre = self.ordre_normes.clone().unwrap();
        let view = self.g.q8_view(&self.tete);
        let mut out = vec![0f32; vocab];
        let mut calcules = vec![false; vocab];
        let mut n_calc = 0usize;
        let mut fait = |o: u32, out: &mut Vec<f32>, calcules: &mut Vec<bool>, n: &mut usize| {
            if !calcules[o as usize] {
                out[o as usize] = self.g.q8_dot_at(&view, o as usize, &qx) * sx;
                calcules[o as usize] = true;
                *n += 1;
            }
        };
        // Passe 1 : la liste de candidats.
        let liste = self.tete_garantie.clone().unwrap_or_default();
        for &o in &liste { fait(o, &mut out, &mut calcules, &mut n_calc); }
        // Paliers : on ajoute les lignes de plus grande norme tant qu'elles
        // peuvent battre le meilleur logit connu.
        let mut palier = 1024usize;
        loop {
            let meilleur = out.iter().enumerate().filter(|(i, _)| calcules[*i])
                               .map(|(_, &v)| v).fold(f32::NEG_INFINITY, f32::max);
            // Borne du meilleur logit non calculé : les lignes étant triées par
            // norme décroissante, c'est la première non calculée.
            let mut borne = f32::NEG_INFINITY;
            for &o in ordre.iter() {
                if !calcules[o as usize] {
                    borne = normes[o as usize] * norme_h;
                    break;
                }
            }
            if borne <= meilleur || n_calc >= vocab {
                return (out, n_calc, borne);
            }
            let avant = n_calc;
            for &o in ordre.iter().take(palier) { fait(o, &mut out, &mut calcules, &mut n_calc); }
            if n_calc == avant { palier *= 2; }
            if palier > vocab { palier = vocab; }
            if n_calc >= vocab { return (out, n_calc, f32::NEG_INFINITY); }
        }
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
        // Invite plus longue que le contexte : on garde les DERNIERS jetons (le
        // début d'un long document est ce qu'on peut perdre avec le moins de
        // dégâts) et on le DIT. Sans ce garde, `KvCache::assurer` bouclait sans
        // fin — un hang, pas une erreur — et rien ne l'annonçait.
        let ctx_modele = self.ctx;
        // On réserve la place de la GÉNÉRATION : tronquer à `ctx` exactement
        // laissait la boucle de décodage appeler `forward(pos = ctx)`, dont
        // l'assertion tombait — un SIGABRT (exit 134) là où le correctif
        // prétendait rendre la main. Marge de 8 comme le mode session.
        let place = ctx_modele.saturating_sub(n_new + 8).max(1);
        let ids = if ids.len() > place {
            let coupe = ids.len() - place;
            println!("[contexte] invite de {} jetons > {} (ctx {} − {} de génération) : les {} \
premiers sont ABANDONNÉS (troncature, pas de fenêtrage)",
                     ids.len(), place, ctx_modele, n_new, coupe);
            &ids[coupe..]
        } else {
            ids
        };
        // Préremplissage par lots : `forward_lot` sur des tranches de `self.lot`
        // jetons. `lot == 1` reprend exactement l'ancienne boucle (forward_lot
        // délègue à `forward` pour un jeton), donc rien ne change par défaut.
        let lot = self.lot.max(1);
        let mut pos = 0usize;
        while pos < ids.len() {
            let t = lot.min(ids.len() - pos);
            if t == 1 {
                last = self.forward(ids[pos], pos);
            } else {
                let hs = self.forward_lot(&ids[pos..pos + t], pos);
                last = hs.into_iter().next_back().expect("lot non vide");
            }
            pos += t;
        }
        let prompt_s = t0.elapsed().as_secs_f64();
        let prompt_events = self.events - events0;
        let mut out = Vec::with_capacity(n_new);
        let t1 = Instant::now();
        for step in 0..n_new {
            // Tête GARANTIE : on ne calcule que les lignes qui peuvent encore
            // gagner, et on étend par paliers tant que la borne de
            // Cauchy-Schwarz ne conclut pas. Quand elle conclut, l'argmax est
            // celui du calcul complet — la sortie est identique, pas approchée.
            let mut logits = if self.tete_garantie.is_some() {
                let (lg, n_calc, borne) = self.logits_garanti(&last);
                self.tete_calculees += n_calc as u64;
                self.tete_appels_g += 1;
                if self.tete_appels_g <= 3 {
                    eprintln!("[tete-garantie] {} lignes calculées sur {} (meilleur hors liste \
borné à {:.4e})", n_calc, self.cfg.vocab, borne);
                }
                lg
            } else { self.logits(&last) };
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
            // Contexte plein : on s'arrête au lieu de dépasser. Sans cette borne,
            // l'assertion de `forward` faisait tomber le processus (mesuré).
            if pos + 1 >= ctx_modele {
                println!("[contexte] contexte plein ({ctx_modele}) : génération arrêtée à \
{} jetons", out.len());
                break;
            }
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

/// Le nœud partiel : charger UN cluster et vérifier que la traduction des
/// experts se fait par NUMÉRO de cluster, pas par rang dans la liste chargée.
///
/// Ce test existe parce que la revue adverse a montré que le correctif n'en
/// avait aucun : remplacer `self.numeros.iter().position(...)` par
/// `Some((cluster, ligne))` laissait les trente tests verts. Sur un nœud complet
/// les deux coïncident — il faut donc un nœud partiel dont le cluster chargé
/// n'est PAS le rang 0.
#[cfg(test)]
mod tests_noeud_partiel {
    use super::*;
    use crate::gguf::tests::{ecrire, gguf_synth, gguf_synth_q4_0};

    #[test]
    fn traduction_par_numero_de_cluster() {
        let d = std::env::temp_dir().join("drave_noeud_partiel");
        let _ = std::fs::remove_dir_all(&d);
        std::fs::create_dir_all(&d).unwrap();
        // Quatre experts globaux, deux clusters de deux. n_in = 32 (un bloc),
        // n_ff = 32 : les formes minimales acceptées par `charger_moe`.
        let (n_in, n_ff, par_cluster, n_clusters) = (32u64, 32u64, 2u64, 2usize);
        // Le commun : le routeur, en F32, dimensionné sur les experts GLOBAUX.
        let routeur: Vec<(&str, Vec<u64>)> =
            vec![("blk.0.ffn_gate_inp.weight", vec![4, n_in])];
        std::fs::write(d.join("commun.gguf"), gguf_synth(&routeur, 0, 1.0)).unwrap();
        // Chaque cluster : ses experts LOCAUX, en Q4_0 (le type que `source_de`
        // accepte, donc le seul qui permette de construire un `Moe`).
        for c in 0..n_clusters {
            let t: Vec<(&str, Vec<u64>)> = vec![
                ("blk.0.ffn_gate_exps.weight", vec![par_cluster, n_ff, n_in]),
                ("blk.0.ffn_up_exps.weight",   vec![par_cluster, n_ff, n_in]),
                ("blk.0.ffn_down_exps.weight", vec![par_cluster, n_ff, n_in]),
            ];
            std::fs::write(d.join(format!("cluster-{c:02}.gguf")),
                           gguf_synth_q4_0(&t, 1.0)).unwrap();
        }
        // Experts globaux 0,1 → cluster 0 ; 2,3 → cluster 1.
        std::fs::write(d.join("mapping.tsv"), "\
# n_couches 1 · n_experts 4 · clusters 2 · experts_par_cluster 2
0\t0\t0\t0
0\t1\t1\t0
0\t0\t2\t1
0\t1\t3\t1
").unwrap();

        // On ne charge QUE le cluster 1 : les vues n'en contiennent qu'une, et
        // le mapping continue de dire « cluster 1 ».
        let m = crate::clusters::ouvrir_sous_ensemble(&d, Some(&[1]))
            .expect("le nœud partiel doit s'ouvrir");
        assert_eq!(m.gguf.nb_fichiers(), 2, "commun + le seul cluster demandé");
        let map: &'static crate::clusters::Mapping =
            Box::leak(Box::new(m.mapping.clone()));
        let moe = charger_moe(&m.gguf, 0, 4, Some(map)).expect("le MoE doit se charger");
        assert_eq!(moe.numeros, vec![1], "la vue porte le NUMÉRO 1, pas le rang 0");
        // Expert 3 : dans le cluster 1 → présent, en tête des vues chargées.
        assert_eq!(moe.ou(3), Some((0, 1)), "expert 3 = cluster 1, ligne locale 1");
        assert_eq!(moe.ou(2), Some((0, 0)), "expert 2 = cluster 1, ligne locale 0");
        // Experts 0 et 1 : dans le cluster 0, que ce nœud ne porte pas.
        assert_eq!(moe.ou(0), None, "un expert absent du nœud n'est pas une erreur");
        assert_eq!(moe.ou(1), None);
        // Hors bornes : le routeur n'en parlera jamais, mais la réponse doit
        // rester `None` et non une panique.
        assert_eq!(moe.ou(99), None);

        // Avec les DEUX clusters, la traduction doit rester juste et couvrir
        // tout le monde — c'est le cas où le défaut d'origine était invisible.
        let tous = crate::clusters::ouvrir_sous_ensemble(&d, None).unwrap();
        let map2: &'static crate::clusters::Mapping =
            Box::leak(Box::new(tous.mapping.clone()));
        let moe2 = charger_moe(&tous.gguf, 0, 4, Some(map2)).unwrap();
        assert_eq!(moe2.numeros, vec![0, 1]);
        assert_eq!(moe2.ou(0), Some((0, 0)));
        assert_eq!(moe2.ou(3), Some((1, 1)));

        let _ = std::fs::remove_dir_all(&d);
    }

    /// `eguille` du garde-fou : un mapping d'un autre modèle (mêmes formes,
    /// compte d'experts différent) doit être refusé, pas suivi en silence.
    #[test]
    fn mapping_dun_autre_modele_est_refuse() {
        let d = std::env::temp_dir().join("drave_mapping_etranger");
        let _ = std::fs::remove_dir_all(&d);
        std::fs::create_dir_all(&d).unwrap();
        let (n_in, n_ff) = (32u64, 32u64);
        let routeur: Vec<(&str, Vec<u64>)> =
            vec![("blk.0.ffn_gate_inp.weight", vec![4, n_in])];
        std::fs::write(d.join("commun.gguf"), gguf_synth(&routeur, 0, 1.0)).unwrap();
        let t: Vec<(&str, Vec<u64>)> = vec![
            ("blk.0.ffn_gate_exps.weight", vec![2, n_ff, n_in]),
            ("blk.0.ffn_up_exps.weight",   vec![2, n_ff, n_in]),
            ("blk.0.ffn_down_exps.weight", vec![2, n_ff, n_in]),
        ];
        std::fs::write(d.join("cluster-00.gguf"), gguf_synth_q4_0(&t, 1.0)).unwrap();
        // Le mapping annonce 6 experts, le modèle en a 4 : c'est un mapping
        // étranger, et le suivre ferait sauter des experts sans un mot.
        std::fs::write(d.join("mapping.tsv"), "\
# n_couches 1 · n_experts 6 · clusters 1 · experts_par_cluster 2
0\t0\t0\t0
0\t1\t1\t0
").unwrap();
        let m = crate::clusters::ouvrir_sous_ensemble(&d, None).unwrap();
        let map: &'static crate::clusters::Mapping =
            Box::leak(Box::new(m.mapping.clone()));
        let e = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
            charger_moe(&m.gguf, 0, 4, Some(map))
        }));
        assert!(e.is_err(), "un mapping de 6 experts pour un modèle qui en a 4 doit être \
refusé, pas suivi en silence");
        let _ = std::fs::remove_dir_all(&d);
    }
}

#[cfg(test)]
mod tests_router {
    use super::*;

    fn moe_synthetique(routeur: Vec<f32>, biais: Option<Vec<f32>>, tid: Option<Vec<i32>>) -> Moe {
        Moe {
            routeur,
            routeur_biais: biais,
            biais_gate: None, biais_up: None, biais_down: None,
            n_ff: 1,
            gate: Vec::new(), up: Vec::new(), down: Vec::new(),
            couche: 0, numeros: Vec::new(), n_expert_global: 0, local: None,
            shexp: None, tid2eid: tid,
        }
    }

    fn cfg_synthetique(gating: Gating, norm: bool, echelle: f32, hash: usize) -> Cfg {
        Cfg {
            n_layer: 1, hidden: 1, n_head: 1, n_kv_head: 1, head_dim: 1, ffn: 1,
            eps: 1e-6, rope_base: 10000.0, vocab: 1,
            n_expert: 4, n_expert_used: 2, ffn_exp: 1,
            ffn_act_oss: false, gating, expert_norm: norm, expert_scale: echelle,
            hash_layers: hash, n_rot: 0, yarn: None,
        }
    }

    /// Les quatre conventions sur le MÊME vecteur de logits, valeurs calculées à
    /// la main. Ce test est la définition exécutable du routage : chaque ligne
    /// correspond à une ligne de `llama-graph.cpp` (`build_moe_ffn`).
    #[test]
    fn quatre_conventions_sur_les_memes_logits() {
        // 4 experts, h = 1 : le logit vaut directement le poids du routeur.
        let logits = vec![0.0f32, 1.0, 2.0, -1.0];
        let x = vec![1.0f32];

        // 1. softmax sur tous, top-2, renormalisation.
        let m = moe_synthetique(logits.clone(), None, None);
        let r = router(&cfg_synthetique(Gating::Softmax, true, 0.0, 0), &m, &x, 0, 2);
        assert_eq!(r.iter().map(|(e, _)| *e).collect::<Vec<_>>(), vec![2, 1]);
        let (e2, e1) = ((2.0f32).exp(), (1.0f32).exp());
        let (s2, s1) = (e2 / (e2 + e1), e1 / (e2 + e1));
        assert!((r[0].1 - s2 / (s1 + s2)).abs() < 1e-6);

        // 2. sigmoïde, top-2, renormalisation.
        let r = router(&cfg_synthetique(Gating::Sigmoid, true, 0.0, 0), &m, &x, 0, 2);
        assert_eq!(r.iter().map(|(e, _)| *e).collect::<Vec<_>>(), vec![2, 1]);
        let sig = |v: f32| 1.0 / (1.0 + (-v).exp());
        let (a, b) = (sig(2.0), sig(1.0));
        assert!((r[0].1 - a / (a + b)).abs() < 1e-6, "poids sigmoïde : {:?}", r);

        // 3. top-k sur les logits BRUTS, softmax sur les k, aucune
        //    renormalisation ensuite (le softmax somme déjà à 1).
        let r = router(&cfg_synthetique(Gating::SoftmaxPoids, false, 0.0, 0), &m, &x, 0, 2);
        assert_eq!(r.iter().map(|(e, _)| *e).collect::<Vec<_>>(), vec![2, 1]);
        let (p2, p1) = ((2.0f32).exp(), (1.0f32).exp());
        assert!((r[0].1 - p2 / (p1 + p2)).abs() < 1e-6);

        // 4. racine de softplus, top-2, renormalisation.
        let r = router(&cfg_synthetique(Gating::SqrtSoftplus, true, 0.0, 0), &m, &x, 0, 2);
        assert_eq!(r.iter().map(|(e, _)| *e).collect::<Vec<_>>(), vec![2, 1]);
        let sp = |v: f32| (1.0 + v.exp()).ln().sqrt();
        let (a, b) = (sp(2.0), sp(1.0));
        assert!((r[0].1 - a / (a + b)).abs() < 1e-6, "poids softplus : {:?}", r);
    }

    /// Le biais de gpt-oss ne départage QUE la sélection : il n'entre pas dans
    /// les poids. C'est la différence qui a fait passer la porte gpt-oss de
    /// 15,1757 à 15,6017 — l'ancien code le laissait dans le softmax.
    #[test]
    fn biais_de_selection_hors_des_poids() {
        // Sans biais, l'expert 3 (logit −1) n'est jamais retenu ; avec un biais
        // de +10 sur lui, il passe premier — mais son poids reste celui du
        // logit BRUT, donc minuscule.
        let logits = vec![0.0f32, 1.0, 2.0, -1.0];
        let m = moe_synthetique(logits.clone(), None, None);
        let sans = router(&cfg_synthetique(Gating::SoftmaxPoids, false, 0.0, 0), &m, &vec![1.0], 0, 2);
        assert_eq!(sans.iter().map(|(e, _)| *e).collect::<Vec<_>>(), vec![2, 1]);

        let biais = vec![0.0f32, 0.0, 0.0, 10.0];
        let m = moe_synthetique(logits.clone(), Some(biais), None);
        let avec = router(&cfg_synthetique(Gating::SoftmaxPoids, false, 0.0, 0), &m, &vec![1.0], 0, 2);
        assert_eq!(avec.iter().map(|(e, _)| *e).collect::<Vec<_>>(), vec![3, 2],
                   "le biais doit changer la SÉLECTION");
        let (p3, p2) = ((-1.0f32).exp(), (2.0f32).exp());
        assert!((avec[0].1 - p3 / (p2 + p3)).abs() < 1e-6,
                "le poids doit venir du logit BRUT (−1), pas du logit biaisé (+9) : {:?}", avec);
    }

    /// Le facteur d'échelle s'applique APRÈS la renormalisation, et il manquait
    /// complètement : GLM-5.3 déclare 2,5, Kimi 2,827, V4 1,5.
    #[test]
    fn facteur_dechelle_apres_renormalisation() {
        let logits = vec![0.0f32, 1.0, 2.0, -1.0];
        let m = moe_synthetique(logits, None, None);
        let sans = router(&cfg_synthetique(Gating::Sigmoid, true, 0.0, 0), &m, &vec![1.0], 0, 2);
        let avec = router(&cfg_synthetique(Gating::Sigmoid, true, 2.5, 0), &m, &vec![1.0], 0, 2);
        for (a, b) in sans.iter().zip(avec.iter()) {
            assert_eq!(a.0, b.0);
            assert!((b.1 - a.1 * 2.5).abs() < 1e-6, "{:?} contre {:?}", a, b);
        }
    }

    /// Le routage par TABLE : les experts viennent de l'identifiant du jeton, et
    /// le score ne sert plus qu'aux poids.
    #[test]
    fn routage_par_table_des_jetons() {
        let logits = vec![0.0f32, 1.0, 2.0, -1.0];
        // Table : jeton 0 → experts 0 et 3 ; jeton 1 → experts 3 et 1.
        let table = vec![0i32, 3, 3, 1];
        let m = moe_synthetique(logits.clone(), None, Some(table));
        let r = router(&cfg_synthetique(Gating::SqrtSoftplus, true, 0.0, 2), &m, &vec![1.0], 0, 2);
        assert_eq!(r.iter().map(|(e, _)| *e).collect::<Vec<_>>(), vec![0, 3]);
        let r = router(&cfg_synthetique(Gating::SqrtSoftplus, true, 0.0, 2), &m, &vec![1.0], 1, 2);
        assert_eq!(r.iter().map(|(e, _)| *e).collect::<Vec<_>>(), vec![3, 1]);
        // Sans table, le top-k donnerait les experts 2 et 1 : la table CHANGE la
        // sélection, elle ne la confirme pas.
        let m2 = moe_synthetique(logits, None, None);
        let sans = router(&cfg_synthetique(Gating::SqrtSoftplus, true, 0.0, 0), &m2, &vec![1.0], 0, 2);
        assert_eq!(sans.iter().map(|(e, _)| *e).collect::<Vec<_>>(), vec![2, 1]);
    }
}
