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
use crate::engram::{Engram, PorteEngram, OCTETS_PAR_RANGEE, VALEURS_PAR_RANGEE};
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
    // Les **hyper-connexions** (DeepSeek-V4) ne sont plus un manque : elles sont
    // lues (`Hc`, `hc_params`) et consommées par la passe avant — l'entrée d'une
    // sous-couche est le mélange des `hc` copies, la sortie se route par `comb`
    // (Sinkhorn), et la tête les réduit en un état. Ce qui reste à faire sur ce
    // chemin est nommé ailleurs (sortie à rang faible groupée, attentions
    // compressées).
    if quelque_part("hc_attn_fn.weight") && g.hc_params().is_none() {
        manques.push("hyper-connexions : `hc_mult` absent des métadonnées");
    }
    // **Kimi-K3** — la cible de la classe « trop gros pour le local »
    // (`docs/plan-kimi-k3.md`, spécification dans `docs/architecture-kimi-k3.md`).
    // Le fichier se LIT déjà (métadonnées, 93 couches, Q8_0 dense + MXFP4 pour
    // les 896 experts), mais cinq mécanismes de la passe avant n'existent pas
    // encore. On les nomme TOUS : « architecture inconnue » ne dit pas quoi
    // écrire, et c'est exactement ce que la porte `--config` doit annoncer.
    if g.meta.get("general.architecture").and_then(|m| m.as_str()) == Some("kimi-k3") {
        manques.push("attention delta-net (KDA) : conv1d de 4, porte bornée (−5), récurrence par tête");
        manques.push("attention résiduelle : pile de points de contrôle tous les 12, softmax sur les scores");
        manques.push("MoE latent : projections down/up autour des experts (latent 3 584)");
        manques.push("activation SiTU (beta 4, linear_beta 25)");
        manques.push("redémarrage du flux résiduel aux couches « banque » (toutes les 12)");
    }
    // Attention par index (DSA) : l'indexeur choisit les clés gardées. Il ne
    // sert QUE si la séquence dépasse `index_topk` — en deçà, llama.cpp garde
    // toutes les clés et l'indexeur n'est pas appelé. On refuse donc seulement
    // les contextes où il changerait le résultat.
    if quelque_part("indexer.") {
        // La clé s'appelle `attention.indexer.top_k` dans les GGUF de V4
        // (`index_topk` dans le `config.json`). Lire le mauvais nom donnait
        // `topk = 0`, donc un refus — pas un silence, mais un refus dont le
        // motif était faux.
        let topk = g.cfg_ou(&["attention.indexer.top_k", "index_topk", "indexer.top_k"])
            .and_then(|m| m.as_u64())
            .or_else(|| g.json_nombre("index_topk").map(|v| v as u64))
            .unwrap_or(0) as usize;
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
    // La sortie à rang faible groupée (`attn_output_a`/`attn_output_b`,
    // `o_groups`) est implémentée : `attn_v4` la calcule par groupe de têtes,
    // comme `build_attention` de la référence. Elle ne compte donc plus comme un
    // manque — mais elle n'existe QUE sur le chemin V4, d'où le test sur le
    // chemin lui-même plutôt que sur la présence du tenseur.
    if quelque_part("attn_output_a.weight") && !quelque_part("attn_kv.weight") {
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
    // Les **attentions compressées** (CSA ratio 4, HCA ratio 128) et leur
    // **indexeur** sont implémentés : `attn_v4` construit les blocs (softmax
    // par canal, `ape`, norme, RoPE de bloc), le compresseur CSA chevauche, et
    // l'indexeur note les blocs puis garde les meilleurs. Validé contre
    // llama.cpp (`reports/rapport-v4-hca.md`). Ce n'est donc plus un manque.
    //
    // Rappel de ce que la lecture de cette clé a coûté : cherchée sous le nom
    // `compress_ratios` au lieu de `attention.compress_ratios`, elle faisait
    // dire « calculable » à V4-Flash sans que le moteur voie les 41 couches
    // compressées sur 44. Un faux « oui » est pire qu'un refus.
    if (g.cfg_ou(&["attention.compress_ratios", "compress_ratios"]).is_some()
        || g.json_brut("compress_ratios").is_some())
        && !quelque_part("attn_compressor_kv.weight") {
        manques.push("attentions compressées : `attn_compressor_kv` absent du fichier");
    }
    // **V4.1 : les ratios 1 et 2, et le cache compressé partagé.** Ce n'est plus
    // un manque, c'est implémenté : le compresseur (softmax PAR CANAL sur le
    // groupe, norme du latent, RoPE de bloc à la position du premier jeton, pas
    // d'`ape`) tourne sur les couches SOURCES, et les couches CONSOMMATRICES
    // lisent les tampons de leur source (`kv_source_layer_ids`, indexation par
    // `comp_source`) au lieu d'en calculer d'autres. Ce qui reste est nommé plus
    // bas (engram, indexeur de V4.1).
    // **Le mélange de tête manquant de V4.1** : ce n'est PAS un manque, c'est
    // une AUTRE chaîne. V4.1 n'a pas de `output_hc_*` parce qu'il n'a pas de
    // tête apprise : la référence replie le flux final avec la `pre` de la
    // dernière FFN (`hc_collapse_triton(hidden_states, pre_mix)`, commentaire
    // « v4.1 has no learned hc_head »), et les coefficients de chaque raccord
    // servent au raccord SUIVANT (`mhc_shifted_post_pre`). C'est implémenté
    // (`hc_retarde`), donc ce n'est plus un refus — mais ça reste ANNONCÉ.
    if quelque_part("hc_attn_fn.weight") && g.tensor("output_hc_fn.weight").is_none()
        && g.tensor("hc_head_fn.weight").is_none()
        && g.meta.get("general.architecture").and_then(|m| m.as_str()) != Some("deepseek41") {
        manques.push("réduction des copies avant la norme finale : `hc_*` sans \
`output_hc_*` sur une architecture qui n'est pas `deepseek41` — la chaîne retardée de V4.1 \
ne s'applique qu'à elle, et pour tout autre fichier le mode de réduction n'est pas écrit");
    }
    // **L'engram de V4.1 est BRANCHÉ** (02/10) : le hachage glissant, la lecture
    // des rangées de 264 octets, la projection `wkv` et l'injection sur les `hc`
    // copies sont dans la passe avant (`forward`, en tête de chaque couche
    // d'engram). Ce qui reste à vérifier n'est pas un manque de code : les
    // tenseurs d'injection doivent être là, sinon il n'y a rien à projeter.
    if let Some(couches) = g.cfg_ou(&["engram.layer_ids"]).and_then(|m| m.as_liste_i64()) {
        for l in couches {
            let p = |s: &str| format!("blk.{l}.{s}");
            if g.tensor(&p("engram_kv.weight")).is_none()
                || g.tensor(&p("engram_q_norm.weight")).is_none()
                || g.tensor(&p("engram_k_norm.weight")).is_none() {
                manques.push("engram : une couche déclarée n'a pas ses tenseurs \
d'injection (`engram_kv`, `engram_q_norm`, `engram_k_norm`) — sans eux, l'injection n'a \
rien à projeter");
                break;
            }
        }
    }
    // Ce message décrit le cache LATENT de la MLA « GLM/Kimi »
    // (`attn_kv_a_mqa`) : sur l'attention V4, qui a aussi un `attn_q_a` mais un
    // cache d'une seule tête déjà tournée, il serait faux.
    if quelque_part("attn_q_a.weight") && quelque_part("attn_kv_a_mqa.weight") {
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
Ce modèle n'est donc pas calculé. Les chiffres publiés à son sujet ne viennent pas \
d'une passe avant COMPLÈTE : analyse statique des tenseurs (inventaire, empreinte, \
sonde mmap), ou passe bornée `--couches a:b` — annoncée comme telle.\n  \
Tenseurs présents : {}{}{}",
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
    /// **Ce que le modèle DÉCLARE**, indépendamment de la décision du moteur :
    /// `(facteur, beta_rapide, beta_lent, contexte d'origine)`. La distinction
    /// compte : `yarn` porte le régime RETARDÉ (RoPE simple sous 4 × la longueur
    /// d'origine, mesuré sur gpt-oss), tandis qu'ici on garde la déclaration
    /// brute — dont les couches COMPRESSÉES de V4 ont besoin, parce que llama.cpp
    /// (`src/models/deepseek4.cpp:872-879`) ET vLLM
    /// (`models/deepseek_v41/common/rope.py:28-46`) appliquent YaRN à TOUTES les
    /// positions dès que `compress_ratio > 0`, et le RoPE simple seulement sur
    /// les couches brutes.
    pub yarn_declare: Option<(f32, f32, f32, f32)>,
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
    // **Deux biais de routeur dans le fichier de V4.1** (`exp_probs_b.bias` et
    // `exp_probs_b_vl.bias`, valeurs très différentes : ~9,8 contre ~21,2 sur la
    // couche 0) et le biais DOMINE la sélection (les scores `sqrt(softplus)` sont
    // de l'ordre de 0 à 5). Prendre le mauvais change donc les experts choisis —
    // et rien d'autre : la perplexité part en vrille sans qu'aucun tenseur ne
    // manque. Le texte seul doit prendre `exp_probs_b` ; `DRAVE_BIAIS_VL=1`
    // force l'autre, pour MESURER lequel des deux fait prédire le modèle.
    static BIAIS_VL: std::sync::OnceLock<bool> = std::sync::OnceLock::new();
    let biais_vl = *BIAIS_VL.get_or_init(|| {
        let actif = std::env::var("DRAVE_BIAIS_VL").map(|v| v != "0" && !v.is_empty())
                        .unwrap_or(false);
        if actif {
            eprintln!("[moe] DRAVE_BIAIS_VL est actif : le routeur sélectionne avec \
`exp_probs_b_vl.bias` au lieu de `exp_probs_b.bias` — ablation de diagnostic.");
        }
        actif
    });
    let nom_biais = if biais_vl && g.tensor(&p("exp_probs_b_vl.bias")).is_some() {
        "exp_probs_b_vl.bias"
    } else { "exp_probs_b.bias" };
    let routeur_biais = if g.tensor(&p(nom_biais)).is_some() {
        Some(g.dequant(&p(nom_biais)))
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

/// **Porte de décroissance du KDA** — variante **K3** (`kda_gate_lower_bound = −5`) :
///
/// ```text
/// g = borne · sigmoïde( exp(A_log) · (f_b(f_a(x)) + dt_bias) )
/// ```
///
/// Le fichier stocke **`-exp(A_log)`** dans `ssm_a` (repli fait à la conversion),
/// donc `exp(A_log) = -ssm_a` — c'est la note de la référence, et se tromper de
/// signe donne une porte **positive**, c'est-à-dire une croissance exponentielle
/// de l'état au lieu d'une décroissance : des scores plausibles et faux.
///
/// Avec `borne = −5`, la porte est **toujours dans (−5, 0)** donc `exp(g)` dans
/// (0, 1] : l'état ne peut que décroître. Kimi-Linear utilise l'autre variante
/// (`-exp(A_log)·softplus(…)`), sans borne : deux modèles, deux formules.
#[allow(dead_code)]
#[inline]
pub fn kda_porte(z: f32, ssm_a: f32, borne: f32) -> f32 {
    let exp_a_log = -ssm_a;                       // le fichier stocke -exp(A_log)
    borne * (1.0 / (1.0 + (-(exp_a_log * z)).exp()))
}

/// **Convolution courte causale du KDA** (noyau 4) par canal, suivie de **SiLU**.
///
/// `etat` porte les `d_conv − 1` entrées **précédentes** de chaque canal (la plus
/// ancienne d'abord) ; il est **mis à jour** par l'appel.
///
/// **Deux dispositions, et il ne faut pas les confondre** :
/// - l'ÉTAT est **canal-majeur** (les temps d'un même canal sont contigus),
///   `etat[k + (d_conv−1)·canal]` — c'est la disposition de la référence
///   (`ggml_view_3d(conv_state, d_conv-1, d_inner, …)`, `ne0` = temps) ; elle rend
///   aussi la fenêtre d'un canal contiguë en mémoire ;
/// - les POIDS sont `poids[k + d_conv·canal]`, parce que le tenseur GGUF a
///   `dims[0] = d_conv` (le noyau contigu).
///
/// La première version de ce code utilisait la même formule pour les deux : le
/// test l'a attrapée.
///
/// La référence fait `ggml_ssm_conv` puis `ggml_silu` : la fenêtre est
/// `[état (3), x (1)]` dans l'ordre chronologique, **sans retournement**.
#[allow(dead_code)]
pub fn kda_conv_silu(x: &[f32], poids: &[f32], etat: &mut [f32], d_conv: usize,
                     d_inner: usize, out: &mut [f32]) {
    debug_assert_eq!(etat.len(), (d_conv - 1) * d_inner);
    debug_assert!(x.len() >= d_inner && out.len() >= d_inner);
    debug_assert!(poids.len() >= d_conv * d_inner);
    for c in 0..d_inner {
        let mut acc = 0f32;
        for k in 0..d_conv - 1 {
            acc += poids[k + d_conv * c] * etat[k + (d_conv - 1) * c];
        }
        acc += poids[(d_conv - 1) + d_conv * c] * x[c];
        // SiLU : `x · sigmoïde(x)`
        out[c] = acc * (1.0 / (1.0 + (-acc).exp()));
    }
    // décalage de l'état : on jette la plus ancienne, on pousse la nouvelle
    for c in 0..d_inner {
        for k in 0..d_conv.saturating_sub(2) {
            etat[k + (d_conv - 1) * c] = etat[(k + 1) + (d_conv - 1) * c];
        }
    }
    if d_conv >= 2 {
        for c in 0..d_inner { etat[(d_conv - 2) + (d_conv - 1) * c] = x[c]; }
    }
}

/// **Règle delta à porte** — la récurrence du **KDA** de Kimi-K3, un jeton.
///
/// Transcription de `build_delta_net_autoregressive` (`llama.cpp-k3`,
/// `delta-net-base.cpp`) ; l'état `s` est **par tête**, `head_dim × head_dim` :
///
/// ```text
///   s ← s · exp(g)                       décroissance, PAR CANAL DE CLÉ
///   sk[j] = Σ_i s[i][j] · k[i]           (sᵀ k)
///   s[i][j] += k[i] · β · (v[j] − sk[j])  mise à jour delta (produit extérieur)
///   o[j] = Σ_i s[i][j] · q[i]            (sᵀ q)
/// ```
///
/// Conventions, et elles comptent : `i` indexe la dimension des **clés** (celle de
/// `k` et de `q`), `j` celle des **valeurs** ; `g` est la porte de décroissance
/// (un scalaire par canal de clé pour K3, d'où la diffusion le long de `j`) ;
/// `β` est le pas appris (`sigmoïde(W_beta·x)`), **par tête**.
///
/// La référence porte **trois** chemins de la même récurrence (chunked,
/// autorégressif, fusionné) : c'est celui-ci qui sert au décodage, et c'est le
/// seul qui se vérifie sans poids (l'état est petit). Le chemin par blocs —
/// nécessaire au préremplissage — viendra après, et devra donner **le même**
/// résultat : c'est en soi un point de vérification.
#[allow(dead_code)]
pub fn kda_pas(q: &[f32], k: &[f32], v: &[f32], g: &[f32], beta: f32,
               s: &mut [f32], hd: usize, out: &mut [f32]) {
    debug_assert_eq!(s.len(), hd * hd);
    debug_assert!(q.len() >= hd && k.len() >= hd && v.len() >= hd && out.len() >= hd);
    // 1. décroissance : `s[i][j] *= exp(g[i])` — la porte est par canal de CLÉ.
    for i in 0..hd {
        let d = g[i].exp();
        for j in 0..hd { s[i * hd + j] *= d; }
    }
    // 2. `sk[j] = Σ_i s[i][j]·k[i]`
    let mut sk = vec![0f32; hd];
    for i in 0..hd {
        let ki = k[i];
        if ki == 0.0 { continue; }
        for j in 0..hd { sk[j] += s[i * hd + j] * ki; }
    }
    // 3. mise à jour delta : produit extérieur `k ⊗ (β(v − sk))`
    for i in 0..hd {
        let ki = k[i];
        if ki == 0.0 { continue; }
        for j in 0..hd { s[i * hd + j] += ki * beta * (v[j] - sk[j]); }
    }
    // 4. sortie : `o[j] = Σ_i s[i][j]·q[i]`
    for j in 0..hd {
        let mut a = 0f32;
        for i in 0..hd { a += s[i * hd + j] * q[i]; }
        out[j] = a;
    }
}

/// **SiTU** — l'activation de Kimi-K3 (`kimi_k3_situ` de la référence) :
///
/// ```text
/// situ(g, u) = beta · tanh(g/beta) · sigmoïde(g)  ×  linear_beta · tanh(u/linear_beta)
/// ```
/// `linear_beta <= 0` **désactive** la transformation de la branche `up` (la
/// référence le dit : « linear_beta <= 0 disables the transform on the up
/// branch »). Elle remplace le SwiGLU : la porte est bornée par `beta` au lieu
/// d'être multipliée telle quelle, ce qui borne l'activation.
///
/// Écrite ici avant d'être branchée : c'est la seule pièce de K3 qui se vérifie
/// **sans poids** (une fonction, quelques points de contrôle), et la vérifier
/// d'abord est la règle du dépôt.
#[allow(dead_code)]
#[inline]
pub fn situ(g: f32, u: f32, beta: f32, linear_beta: f32) -> f32 {
    let a = beta * (g / beta).tanh() * (1.0 / (1.0 + (-g).exp()));
    let up = if linear_beta > 0.0 { linear_beta * (u / linear_beta).tanh() } else { u };
    a * up
}

/// **Attention résiduelle** de Kimi-K3 (`res_mix` de la référence) : à chaque
/// sous-couche, le flux est un MÉLANGE par softmax de la pile des points de
/// contrôle et du flux courant.
///
/// ```text
/// score(ckpt) = Σ_c rms_norm(ckpt)[c] · w[c]      ← les scores sont calculés
/// score(cur)  = Σ_c rms_norm(cur)[c]  · w[c]         sur les valeurs NORMÉES
/// p           = softmax([score(ckpt_1..k), score(cur)])
/// sortie      = Σ_i p_i · ckpt_i + p_cur · cur     ← la somme utilise les BRUTES
/// ```
///
/// `pile` est le tableau des points de contrôle (append-only, `n_ckpt × h`),
/// `courant` le flux courant (`h`), `w` le vecteur de score de la sous-couche.
/// `eps` est l'epsilon de la RMSNorm.
///
/// Deux détails décident de la fidélité, et les deux sont dans la référence :
/// **les scores voient les valeurs normalisées, la somme voit les brutes**, et
/// la pile ne se replie jamais (elle grandit, puis le flux **redémarre** aux
/// couches « banque »).
#[allow(dead_code)]
pub fn res_mix(pile: &[f32], n_ckpt: usize, h: usize, courant: &[f32], w: &[f32],
               eps: f32, out: &mut [f32]) {
    debug_assert_eq!(pile.len(), n_ckpt * h);
    debug_assert_eq!(courant.len(), h);
    debug_assert_eq!(w.len(), h);
    debug_assert_eq!(out.len(), h);
    let mut scores = vec![0f32; n_ckpt + 1];
    let mut norm = vec![0f32; h];
    for k in 0..n_ckpt {
        rms_norm_sans_poids(&pile[k * h..(k + 1) * h], eps, &mut norm);
        let mut s = 0f32;
        for c in 0..h { s += norm[c] * w[c]; }
        scores[k] = s;
    }
    rms_norm_sans_poids(&courant[..h], eps, &mut norm);
    let mut s = 0f32;
    for c in 0..h { s += norm[c] * w[c]; }
    scores[n_ckpt] = s;
    // softmax sur les points de contrôle ET le flux courant
    let mx = scores.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
    let mut somme = 0f32;
    for v in scores.iter_mut() { *v = (*v - mx).exp(); somme += *v; }
    let inv = if somme > 0.0 { 1.0 / somme } else { 0.0 };
    for v in scores.iter_mut() { *v *= inv; }
    // la somme, elle, porte sur les valeurs BRUTES
    out.fill(0.0);
    for k in 0..n_ckpt {
        let p = scores[k];
        for c in 0..h { out[c] += p * pile[k * h + c]; }
    }
    let pc = scores[n_ckpt];
    for c in 0..h { out[c] += pc * courant[c]; }
}

/// **`DRAVE_SIMD_DOT=1`** : le produit scalaire des super-blocs déquantifiés passe
/// en AVX2+FMA. Le drapeau **s'annonce** parce qu'il change une sortie : quatre
/// accumulateurs vectoriels, puis une somme horizontale — l'ordre des additions
/// n'est plus celui qui a produit les chiffres publiés, et le FMA n'arrondit
/// qu'une fois au lieu de deux. Le chemin par défaut reste le scalaire de gauche
/// à droite, bit à bit celui des références.
fn simd_dot() -> bool {
    static SIMD_DOT: std::sync::OnceLock<bool> = std::sync::OnceLock::new();
    *SIMD_DOT.get_or_init(|| {
        let demande = std::env::var("DRAVE_SIMD_DOT")
            .map(|v| v != "0" && !v.is_empty()).unwrap_or(false);
        #[cfg(target_arch = "x86_64")]
        let possible = std::is_x86_feature_detected!("avx2") && std::is_x86_feature_detected!("fma");
        #[cfg(not(target_arch = "x86_64"))]
        let possible = false;
        if demande && !possible {
            eprintln!("[simd] DRAVE_SIMD_DOT demandé mais AVX2+FMA indisponible sur ce \
processeur : chemin scalaire conservé (aucun changement de bits).");
        } else if demande {
            eprintln!("[simd] DRAVE_SIMD_DOT est actif : le produit scalaire des experts est \
vectorisé (AVX2+FMA, quatre accumulateurs). Les sommes ne sont plus dans l'ordre publié — \
les logits changent légèrement, et c'est mesurable avec tools/compare_logits.py.");
        }
        demande && possible
    })
}

/// Produit scalaire d'un super-bloc déquantifié par les activations du même bloc.
/// `simd = false` est le chemin historique : une accumulation, de gauche à droite.
#[inline]
fn dot_bloc_f32(valeurs: &[f32], x: &[f32], simd: bool) -> f32 {
    #[cfg(target_arch = "x86_64")]
    if simd {
        // Sûreté : `simd` n'est vrai que si AVX2 et FMA ont été détectés.
        return unsafe { dot_bloc_avx2(valeurs, x) };
    }
    let mut s = 0f32;
    for j in 0..valeurs.len() { s += valeurs[j] * x[j]; }
    s
}

/// Quatre accumulateurs vectoriels, puis somme horizontale. Le reste (bloc non
/// multiple de 32, ce qui n'arrive que sur le DERNIER super-bloc d'une ligne non
/// multiple de 256) est fini en scalaire.
#[cfg(target_arch = "x86_64")]
#[target_feature(enable = "avx2,fma")]
unsafe fn dot_bloc_avx2(valeurs: &[f32], x: &[f32]) -> f32 {
    use std::arch::x86_64::*;
    let n = valeurs.len().min(x.len());
    let (pv, px) = (valeurs.as_ptr(), x.as_ptr());
    let (mut a0, mut a1, mut a2, mut a3) = (_mm256_setzero_ps(), _mm256_setzero_ps(),
                                           _mm256_setzero_ps(), _mm256_setzero_ps());
    let mut j = 0usize;
    while j + 32 <= n {
        a0 = _mm256_fmadd_ps(_mm256_loadu_ps(pv.add(j)), _mm256_loadu_ps(px.add(j)), a0);
        a1 = _mm256_fmadd_ps(_mm256_loadu_ps(pv.add(j + 8)), _mm256_loadu_ps(px.add(j + 8)), a1);
        a2 = _mm256_fmadd_ps(_mm256_loadu_ps(pv.add(j + 16)), _mm256_loadu_ps(px.add(j + 16)), a2);
        a3 = _mm256_fmadd_ps(_mm256_loadu_ps(pv.add(j + 24)), _mm256_loadu_ps(px.add(j + 24)), a3);
        j += 32;
    }
    let s = _mm256_add_ps(_mm256_add_ps(a0, a1), _mm256_add_ps(a2, a3));
    let bas = _mm256_castps256_ps128(s);
    let haut = _mm256_extractf128_ps(s, 1);
    let q = _mm_add_ps(bas, haut);
    let q = _mm_add_ps(q, _mm_movehl_ps(q, q));
    let q = _mm_add_ss(q, _mm_shuffle_ps(q, q, 1));
    let mut total = _mm_cvtss_f32(q);
    while j < n { total += *pv.add(j) * *px.add(j); j += 1; }
    total
}

impl Vue4 {
    /// Octets d'UN expert, **tels que le chemin de lecture les parcourt**.
    ///
    /// `nb`/`pas()` ne suffisent pas : `nb` compte des blocs de 32 pour tous les
    /// formats sauf Q4_K/Q6_K, alors que `pas()` d'une grille (`Dequant`) est la
    /// taille d'un **super-bloc de 256**. Le produit `n_out × nb × pas()`
    /// surestimait donc l'expert d'un facteur 8 pour les formats quantifiés par
    /// grille (tous ceux de V4.1) : la PRÉLECTURE et `expert()` visaient huit
    /// experts plus loin, et le cache RAM copiait le mauvais. Relevé en écrivant
    /// le cache RAM (l'expert 0 était juste, les suivants étaient du bruit).
    fn octets_expert(&self) -> usize {
        use crate::list::Source::*;
        match self.src {
            Propre => 0,
            // Super-blocs de 256 poids : `DenseQ4` pour Q4_K/Q6_K, et
            // `matvec_dequant` (`nb = n_in / 256`) pour les grilles.
            Q4_K | Q6_K | Dequant(_) => self.n_out * (self.n_in / 256) * self.pas(),
            // Blocs de 32 poids (4,25 et 4,5 bits par poids).
            Mxfp4 | Q4_0 => self.n_out * (self.n_in / 32) * self.pas(),
        }
    }

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
    ///
    /// **Ce qui domine vraiment, mesuré** : le produit scalaire du super-bloc, pas
    /// la déquantification (vectoriser la déquantification d'IQ1_M n'a donné que
    /// ×1,07). Une seule accumulation de gauche à droite enchaîne 256 additions
    /// dépendantes : ~4 cycles de latence chacune, soit ~0,25 produit par cycle.
    /// `DRAVE_SIMD_DOT=1` prend le chemin AVX2+FMA (quatre accumulateurs, puis
    /// somme horizontale) — **et change donc les bits**, ce qui est dit à
    /// l'activation et mesuré (`tools/compare_logits.py`) : ce n'est pas le
    /// défaut, c'est une optimisation qui s'annonce.
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
        let simd = simd_dot();
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
                    // Le produit scalaire du super-bloc : c'est LUI le poste,
                    // pas la déquantification (mesuré : ×1,07 en vectorisant la
                    // déquantification d'IQ1_M). Voir `dot_bloc_f32`.
                    acc += dot_bloc_f32(&valeurs[..hi - lo], &x[lo..hi], simd);
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
        let octets = self.octets_expert();
        let p = unsafe { self.base.add(e * octets) };
        crate::gguf::prelire(p, octets);
    }

    /// Octets bruts de l'expert `e` (tels qu'ils sont dans le fichier) : c'est
    /// ce qu'il faut copier en VRAM pour que le noyau y travaille.
    fn blocs_expert(&self, e: usize) -> &[u8] {
        let octets = self.octets_expert();
        let p = unsafe { self.base.add(e * octets) };
        unsafe { std::slice::from_raw_parts(p, octets) }
    }

    /// Matrice 4 bits de l'expert `e`, **empruntée** au fichier.
    fn expert(&self, e: usize) -> crate::list::DenseQ4 {
        let base = unsafe { self.base.add(e * self.octets_expert()) };
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

/// `DRAVE_SANS_COMPRESSION=1` : le RATIO de toutes les couches est forcé à 0.
///
/// L'attention ne voit plus que sa fenêtre brute (128 jetons) et le chemin
/// compressé (compresseur, blocs, cache partagé des consommatrices) n'est plus
/// exercé. Ce n'est PLUS V4.1 : c'est l'ablation qui dit si le défaut du modèle
/// vient de là. La rotation (YaRN des couches compressées) reste celle du
/// fichier, pour ne changer QU'UNE chose.
static SANS_COMPRESSION_EXERCICE: std::sync::OnceLock<bool> = std::sync::OnceLock::new();

/// **Cache RAM des experts** (`DRAVE_EXPERTS_RAM` en Mo).
///
/// Les octets d'un expert sont lus une fois depuis le NVMe et gardés en
/// mémoire. Le noyau en garde déjà une partie en `buff/cache`, mais il les
/// évince au rythme des ~330 Go lus par passe ; ici la résidence est explicite
/// et bornée.
///
/// **Ce que ça ne fait pas** : aucun octet n'est modifié, aucun ordre de
/// sommation ne change — un expert lu en RAM rend exactement ce que le mmap
/// rendait. Vérifié : 2 544 vides identiques au bit près, perplexité inchangée.
///
/// **MESURÉ PLUS LENT, et c'est le résultat qui compte.** La trace de routage
/// rendait l'idée plausible (63 jetons de wiki réel : 15 360 lectures, 3 817
/// experts distincts, 50 % des lectures dans 394 experts, 31,9 % de réutilisation
/// entre jetons consécutifs) — mais le noyau fait DÉJÀ ce travail : `buff/cache`
/// garde ~95 Go de pages du fichier, donc la copie ajoute un second exemplaire et
/// du trafic mémoire sans retirer les lectures NVMe. Mesuré, passe ctx 32
/// (31 jetons) : **145,1 s sans cache, 151,2 s à 4 Go (+4 %), 175,5 s à 32 Go
/// (+21 %)** — plus le cache est grand, plus il coûte. Le drapeau reste, éteint
/// par défaut, pour re-mesurer là où le cache de pages est petit.
pub struct CacheExpertsRam {
    budget: usize,
    octets: usize,
    horloge: u64,
    table: std::collections::HashMap<(u8, usize, usize), (Box<[u8]>, u64)>,
}

impl CacheExpertsRam {
    pub fn nouveau(budget: usize) -> Self {
        CacheExpertsRam { budget, octets: 0, horloge: 0,
                          table: std::collections::HashMap::new() }
    }

    /// L'expert est-il en RAM ? Si oui, son adresse (stable : la `Box` ne bouge
    /// pas, même quand la table se réorganise) et il rajeunit.
    fn pointeur(&mut self, quoi: u8, l: usize, e: usize) -> Option<*const u8> {
        self.horloge += 1;
        let h = self.horloge;
        match self.table.get_mut(&(quoi, l, e)) {
            Some((octets, age)) => { *age = h; Some(octets.as_ptr()) }
            None => None,
        }
    }

    /// Copie l'expert en RAM s'il n'y est pas et si le budget le permet.
    fn garder(&mut self, quoi: u8, l: usize, e: usize, vue: &Vue4, loc: usize) {
        let taille = vue.octets_expert();
        if taille == 0 || taille > self.budget { return; }
        if self.table.contains_key(&(quoi, l, e)) { return; }
        while self.octets + taille > self.budget && !self.table.is_empty() {
            // Le plus ancien part. Balayage linéaire : la table fait quelques
            // milliers d'entrées et une éviction est rare (une par lecture
            // manquée au plus).
            let vieux = self.table.iter().min_by_key(|(_, (_, age))| *age)
                            .map(|(c, _)| *c).unwrap();
            if let Some((o, _)) = self.table.remove(&vieux) { self.octets -= o.len(); }
        }
        let src = unsafe { vue.base.add(loc * taille) };
        let copie = unsafe { std::slice::from_raw_parts(src, taille) }.to_vec().into_boxed_slice();
        self.octets += copie.len();
        self.horloge += 1;
        self.table.insert((quoi, l, e), (copie, self.horloge));
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

/// **L'attention de DeepSeek-V4** — un troisième chemin, qui n'est ni la MLA de
/// GLM/Kimi ni l'attention dense.
///
/// Ce qui la distingue, mesuré sur les tenseurs (`--tensors`, `--config`) et
/// relevé dans `llama.cpp/src/models/deepseek4.cpp` :
///
/// * la KV est **une seule tête latente** de `head_dim` (512 = 448 nope + 64
///   rope), normée **en entier** (`attn_kv_a_norm`) — pas de `k_b`/`v_b` ;
/// * la requête passe par `attn_q_a` → norme → `attn_q_b`, puis par une
///   **seconde norme RMS sans poids, par tête** (`ggml_rms_norm` seul) ;
/// * les **valeurs SONT les clés** (`build_attn_mha(q, k, k, …)`) : le même
///   vecteur sert de clé et de valeur ;
/// * la sortie subit une **dé-rotation** (`ggml_rope_ext_back`) avant d'être
///   projetée par groupes : `attn_output_a` par groupe de `nh/o_groups` têtes,
///   puis `attn_output_b` sur les groupes concaténés ;
/// * les puits appris (`attn_sinks`, un par tête) entrent dans le **softmax**.
pub struct Mla4 {
    pub q_a: Vec<f32>,      // [q_lora × h]
    pub q_a_norm: Vec<f32>, // [q_lora]
    pub q_b: Vec<f32>,      // [nh·head_dim × q_lora]
    pub kv: Vec<f32>,       // [head_dim × h]
    pub kv_norm: Vec<f32>,  // [head_dim]
    pub wo_a: Vec<f32>,     // [o_lora·n_groups × (nh/n_groups)·head_dim], par groupe
    pub wo_b: Vec<f32>,     // [h × o_lora·n_groups]
    pub sinks: Vec<f32>,    // [nh]
    pub nh: usize,
    pub h: usize,
    pub head_dim: usize,
    pub rope: usize,
    pub n_groups: usize,
    pub o_lora: usize,
    pub rope_base: f32,
    pub eps: f32,
    /// Ratio de compression de la couche (`attention.compress_ratios`) :
    /// **0** = couche brute (toute la chaîne est celle de P3), **128** = HCA
    /// (implémenté), **4** = CSA (avec indexeur — P5).
    pub ratio: usize,
    /// Base RoPE des couches compressées : `compress_rope_freq_base` (160 000
    /// pour V4-Flash) au lieu de `rope.freq_base` (10 000). Les deux chemins
    /// tournent à des bases différentes, et se tromper donne des scores
    /// plausibles **et faux** dès que la position dépasse 0.
    pub rope_base_compresse: f32,
    /// **YaRN des couches compressées** (`facteur, beta_rapide, beta_lent,
    /// contexte d'origine`) : la déclaration du modèle, appliquée à TOUTES les
    /// positions dès que `ratio > 0` — c'est ce que font llama.cpp
    /// (`deepseek4.cpp:872-879`) et vLLM (`rope.py:28-46`). `None` sur une couche
    /// brute (leur RoPE reste simple, YaRN y étant l'identité) ou quand le modèle
    /// ne déclare pas YaRN.
    pub yarn_compresse: Option<(f32, f32, f32, f32)>,
    /// Fenêtre brute des couches compressées (`attention.sliding_window`) : ce
    /// que l'attention garde en clair, le reste passant par les blocs.
    pub fenetre: usize,
    /// Nombre de blocs que l'**indexeur** garde (`attention.indexer.top_k`,
    /// 512 pour V4-Flash). L'indexeur n'est pas encore implémenté : tant que le
    /// nombre de blocs reste sous ce seuil, le top-k les garde TOUS et le
    /// résultat est exact — au-delà, il faudrait choisir, et Drave refuse
    /// plutôt que de calculer faux en silence.
    pub indexer_top_k: usize,
    /// La couche a-t-elle un indexeur (`indexer.proj` dans le fichier) ?
    pub a_indexeur: bool,
    /// **La couche POSSÈDE-t-elle son compresseur ?** V4 : oui, chaque couche
    /// compressée a ses tenseurs. V4.1 : seulement les couches SOURCES
    /// (`kv_source_layer_ids` = [2,8,14,20]) — les autres n'ont même pas
    /// `attn_compressor_kv` et lisent l'état publié par leur source.
    pub a_compresseur: bool,
    /// **Le filtre à DEUX NIVEAUX de V4.1** (`candidate_source_layer_id`,
    /// `candidate_topk_blocks`, `candidate_block_size`) : le nombre de positions
    /// compressées au-delà duquel il écarte des blocs AVANT l'indexeur, soit
    /// `candidate_topk_blocks × candidate_block_size` (2 048 × 8 = 16 384 pour ce
    /// fichier). En dessous, il ne mord pas : ignorer le filtre est alors exact.
    /// Au-delà, le moteur refuse au lieu de choisir sur un ensemble plus large que
    /// la référence. 0 = le fichier ne déclare pas de filtres.
    pub candidats_max: usize,
    /// La couche qui PUBLIE les blocs candidats (`candidate_source_layer_id`) :
    /// seuls les indexeurs AU-DESSUS masquent leurs scores, donc seuls ceux-là
    /// butent sur le filtre à deux niveaux.
    pub candidat_source: usize,
    /// **Y a-t-il une porte ?** Celle de la SOURCE : une couche consommatrice de
    /// V4.1 n'a pas de tenseur de porte, mais le pool qu'elle lit en a une (c'est
    /// le compresseur de sa source qui l'a remplie). Lire la présence sur la
    /// couche elle-même donnerait un pool SANS porte là où la référence en a une.
    pub a_porte: bool,
    /// **Largeur de l'état du compresseur** (`coff × head_dim`), celle de la
    /// SOURCE : une couche consommatrice n'a pas de tenseur d'où la lire.
    pub comp_largeur: usize,
    /// **De quelle couche viennent les blocs compressés ?** V4 : la couche
    /// elle-même (chaque couche compressée a son compresseur). **V4.1 : une
    /// couche SOURCE**, d'après `kv_source_layer_ids` — « Compressors and
    /// compressed-KV caches live only on `kv_source_layer_ids`; consumers reuse
    /// the most recently published source below them » (vLLM,
    /// `deepseek_v41/attention.py`). Les couches 3..7 lisent donc les clés
    /// publiées par la 2, 9..13 celles de la 8, et **21..39 celles de la 20**.
    /// Ne pas le savoir, c'est calculer un compresseur par couche et obtenir
    /// d'autres clés — un résultat faux qui ne casse rien.
    pub comp_source: usize,
    /// **Indexeur** (« lightning indexer ») : il note chaque bloc compressé et
    /// n'en garde que les `indexer_top_k` meilleurs. Ses propres tenseurs :
    /// compresseur de 256 valeurs par jeton (deux moitiés de 128, comme le CSA
    /// en a deux de 512), norme de 128, projection de requête et poids par tête.
    pub idx_q_b: Vec<f32>,
    pub idx_proj: Vec<f32>,
    pub idx_comp_kv: Vec<f32>,
    pub idx_comp_gate: Vec<f32>,
    pub idx_comp_ape: Vec<f32>,
    pub idx_comp_norm: Vec<f32>,
    /// Têtes de l'indexeur (`indexer.head_count`).
    pub idx_nh: usize,
    /// Dimension d'une tête d'indexeur (`indexer.key_length`, 128).
    pub idx_hd: usize,
    /// **Les clés de l'indexeur de V4.1** : `indexer.attn_k` [`idx_hd`, `head_dim`]
    /// et `indexer.k_norm` [`idx_hd`]. Elles ne projettent pas l'état de la couche
    /// mais le **latent du compresseur principal** (512 pour V4.1), et n'existent
    /// QUE sur les couches qui possèdent le cache de clés (`index_source_layer_ids`
    /// ∩ `kv_source_layer_ids` = [2, 8, 14, 20]). Les indexeurs de 24/28/32/36
    /// n'ont que `attn_q_b` et `proj` : ils lisent le cache de leur source de KV.
    pub idx_k: Vec<f32>,
    pub idx_k_norm: Vec<f32>,
    /// La couche POSSÈDE-t-elle ce cache (`indexer.attn_k` présent) ?
    pub a_idx_k: bool,
    /// Compresseur (`None` sur une couche brute) : `coff·head_dim × h` pour la
    /// valeur et la porte, `coff·head_dim × ratio` pour l'`ape`, `head_dim` pour
    /// la norme.
    pub comp_kv: Vec<f32>,
    pub comp_gate: Vec<f32>,
    pub comp_ape: Vec<f32>,
    pub comp_norm: Vec<f32>,
}

/// Les quatre tampons du chemin d'attention V4, regroupés : les clés brutes,
/// l'état du compresseur (valeur et porte de chaque jeton) et les **clés
/// compressées** (une par bloc complet). Les regrouper évite une signature à
/// quinze paramètres, et surtout oblige à les passer ENSEMBLE : un cache oublié
/// ne se voit pas, il donne des clés périmées.
pub struct EtatV4<'a> {
    pub cles: &'a mut Vec<f32>,
    pub comp_kv: &'a mut Vec<f32>,
    pub comp_gate: &'a mut Vec<f32>,
    pub cles_comp: &'a mut Vec<f32>,
    /// L'indexeur a son propre compresseur et ses propres blocs (128 valeurs).
    pub idx_kv: &'a mut Vec<f32>,
    pub idx_gate: &'a mut Vec<f32>,
    pub idx_cles: &'a mut Vec<f32>,
    /// Scores de l'indexeur par bloc, gardés pour la trace et l'analyse.
    pub idx_scores: &'a mut Vec<f32>,
}

/// **Hyper-connexions** (DeepSeek-V4 / V4.1) : au lieu d'additionner la sortie
/// d'une sous-couche au résidu, l'état résiduel est porté en **`hc` copies**
/// (4) qui se **mélangent** — c'est le « cas général en connexions pondérées »
/// de la vision, et `comb` en est la matrice : `hc × hc` connexions **par
/// jeton**, rendues doublement stochastiques par Sinkhorn.
///
/// Les formules sont celles de `src/models/deepseek4.cpp` de llama.cpp
/// (`build_hc_pre`, `build_hc_sinkhorn`, `build_hc_post`), recopiées ici pour
/// qu'un écart se voie ligne par ligne :
///
/// ```text
///   aplat      = rms_norm(x aplati sur hc × h)          (SANS poids appris)
///   mélanges   = hc_fn · aplat                          [2·hc + hc² = 24]
///   pre[ih]    = σ(mélanges[ih]·scale₀ + base[ih]) + eps          → entrée
///   post[ih]   = 2·σ(mélanges[hc+ih]·scale₁ + base[hc+ih])        → sortie
///   comb[d,s]  = Sinkhorn(mélanges[2hc + d + s·hc]·scale₂ + base[…])
///   entrée     = Σ_ih x[ih]·pre[ih]
///   sortie[d]  = y·post[d] + Σ_s résidu[s]·comb[d,s]
/// ```
pub struct Hc {
    /// `hc_fn` : `[hc_mix × hc·h]`, ligne par mélange — tel que rangé dans le GGUF.
    pub melange: Vec<f32>,
    /// `hc_base` : `[2·hc + hc²]` — les biais des trois groupes.
    pub base: Vec<f32>,
    /// `hc_scale` : `[3]` — une échelle pour `pre`, `post` et `comb`.
    pub scale: Vec<f32>,
    pub hc: usize,
    pub h: usize,
    /// `hyper_connection.sinkhorn_iterations` (20 pour V4.1).
    pub iters: usize,
    /// `hyper_connection.epsilon` (1e-6 pour V4.1).
    pub eps: f32,
}

/// Ce que `Hc::mélanges` rend pour une sous-couche : de quoi mélanger l'entrée,
/// remettre à l'échelle la sortie, et router les copies entre elles.
pub struct HcSortie {
    pub pre: Vec<f32>,   // [hc]
    pub post: Vec<f32>,  // [hc]
    pub comb: Vec<f32>,  // [hc·hc], `comb[d + s·hc]`
}

/// Normalisation RMS **sans poids** (celle de `ggml_rms_norm` seul, que les
/// hyper-connexions utilisent sur l'état aplati).
fn rms_norm_sans_poids(x: &[f32], eps: f32, out: &mut [f32]) {
    let mut s = 0f64;
    for &v in x { s += (v as f64) * (v as f64); }
    let inv = 1.0 / ((s / x.len().max(1) as f64) as f32 + eps).sqrt();
    for (o, &v) in out.iter_mut().zip(x.iter()) { *o = v * inv; }
}

/// **Sinkhorn** des connexions : softmax sur les destinations, puis
/// normalisations alternées lignes/colonnes avec `eps` — l'ordre exact du
/// modèle de référence (une passe « sources » d'abord, puis `iters − 1` paires).
pub fn sinkhorn(comb: &mut [f32], hc: usize, iters: usize, eps: f32) {
    // softmax sur `dst` (ne0 de ggml), pour chaque `src`
    for s in 0..hc {
        let mut mx = f32::NEG_INFINITY;
        for d in 0..hc { let v = comb[d + s * hc]; if v > mx { mx = v; } }
        let mut somme = 0f32;
        for d in 0..hc { let e = (comb[d + s * hc] - mx).exp(); comb[d + s * hc] = e; somme += e; }
        let inv = if somme > 0.0 { 1.0 / somme } else { 0.0 };
        for d in 0..hc { comb[d + s * hc] *= inv; }
    }
    for v in comb.iter_mut() { *v += eps; }
    // normalise sur les SOURCES, pour chaque destination (« norm_cols »)
    let norm_src = |c: &mut [f32]| {
        for d in 0..hc {
            let mut s = eps;
            for src in 0..hc { s += c[d + src * hc]; }
            for src in 0..hc { c[d + src * hc] /= s; }
        }
    };
    // normalise sur les DESTINATIONS, pour chaque source (« norm_rows »)
    let norm_dst = |c: &mut [f32]| {
        for src in 0..hc {
            let mut s = eps;
            for d in 0..hc { s += c[d + src * hc]; }
            for d in 0..hc { c[d + src * hc] /= s; }
        }
    };
    norm_src(comb);
    for _ in 1..iters { norm_dst(comb); norm_src(comb); }
}

impl Hc {
    pub fn hc_mix(&self) -> usize { 2 * self.hc + self.hc * self.hc }

    /// Les `24` mélanges d'un jeton : `hc_fn · rms_norm(x aplati)`.
    pub fn melanges(&self, x: &[f32]) -> Vec<f32> {
        let hc_dim = self.hc * self.h;
        let mut plat = vec![0f32; hc_dim];
        rms_norm_sans_poids(&x[..hc_dim.min(x.len())], 1e-20, &mut plat);
        let mut out = vec![0f32; self.hc_mix()];
        for (m, o) in out.iter_mut().enumerate() {
            let ligne = &self.melange[m * hc_dim..(m + 1) * hc_dim];
            let mut acc = 0f32;
            for i in 0..hc_dim { acc += ligne[i] * plat[i]; }
            *o = acc;
        }
        out
    }

    /// Les trois sorties d'un `hc_pre` : `pre`, `post`, `comb`.
    pub fn sortie(&self, x: &[f32]) -> HcSortie {
        let mel = self.melanges(x);
        let (hc, eps) = (self.hc, self.eps);
        let sig = |v: f32| 1.0 / (1.0 + (-v).exp());
        let mut pre = vec![0f32; hc];
        for i in 0..hc { pre[i] = sig(mel[i] * self.scale[0] + self.base[i]) + eps; }
        let mut post = vec![0f32; hc];
        for i in 0..hc {
            post[i] = 2.0 * sig(mel[hc + i] * self.scale[1] + self.base[hc + i]);
        }
        let mut comb = vec![0f32; hc * hc];
        for d in 0..hc {
            for s in 0..hc {
                let m = 2 * hc + d + s * hc;
                comb[d + s * hc] = mel[m] * self.scale[2] + self.base[m];
            }
        }
        sinkhorn(&mut comb, hc, self.iters, eps);
        HcSortie { pre, post, comb }
    }

    /// **Mélange de tête** (`build_hc_head`) : le `fn` de la tête n'a que `hc`
    /// lignes — une par copie — et non `2·hc + hc²` comme celui d'une
    /// sous-couche : elle ne produit ni `post` ni `comb`, seulement les poids
    /// qui réduisent les `hc` copies en UN état. Sa `scale` fait aussi 1 valeur,
    /// pas 3. Confondre les deux formes fait sortir de la tranche au 5ᵉ mélange
    /// (c'est le plantage qui l'a dit).
    pub fn tete(&self, x: &[f32]) -> Vec<f32> {
        let hc_dim = self.hc * self.h;
        let mut plat = vec![0f32; hc_dim];
        rms_norm_sans_poids(&x[..hc_dim.min(x.len())], 1e-20, &mut plat);
        let mut pre = vec![0f32; self.hc];
        for (i, p) in pre.iter_mut().enumerate() {
            let ligne = &self.melange[i * hc_dim..(i + 1) * hc_dim];
            let mut acc = 0f32;
            for j in 0..hc_dim { acc += ligne[j] * plat[j]; }
            *p = 1.0 / (1.0 + (-(acc * self.scale[0] + self.base[i])).exp()) + self.eps;
        }
        let mut out = vec![0f32; self.h];
        Hc::melanger(x, &pre, self.hc, self.h, &mut out);
        out
    }

    /// `hc_pre` : l'entrée de la sous-couche est le **mélange** des copies.
    pub fn melanger(x: &[f32], poids: &[f32], hc: usize, h: usize, out: &mut [f32]) {
        for o in out[..h].iter_mut() { *o = 0.0; }
        for ih in 0..hc {
            let p = poids[ih];
            if p == 0.0 { continue; }
            let copie = &x[ih * h..(ih + 1) * h];
            for e in 0..h { out[e] += copie[e] * p; }
        }
    }

    /// `hc_post` : les copies de sortie, à partir de la sortie de la
    /// sous-couche (`y`), du résidu gardé et des connexions `comb`.
    pub fn retro(y: &[f32], residu: &[f32], s: &HcSortie, hc: usize, h: usize,
                 out: &mut [f32]) {
        for d in 0..hc {
            let copie = &mut out[d * h..(d + 1) * h];
            let pd = s.post[d];
            for e in 0..h { copie[e] = y[e] * pd; }
            for src in 0..hc {
                let c = s.comb[d + src * hc];
                if c == 0.0 { continue; }
                let r = &residu[src * h..(src + 1) * h];
                for e in 0..h { copie[e] += r[e] * c; }
            }
        }
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

/// `matvec_f32` **en parallèle par LIGNES** : chaque ligne est sommée par un seul
/// fil, dans le même ordre que la version séquentielle.
///
/// C'est la seule forme d'accélération qui n'a pas à être annoncée comme un
/// changement de calcul : le résultat est **identique au bit près** (aucune
/// réassociation — un produit scalaire par ligne, séquentiel). Mesuré sur V4.1 :
/// le poste d'attention valait **7 283 ms par jeton** avec un seul fil alors que
/// la machine en a vingt ; les noyaux d'experts, eux, étaient déjà parallèles.
///
/// Le découpage est celui du noyau d'experts (`crate::list`) : tranches
/// contiguës, `o - o0` pour indexer la tranche du fil (indexer par le numéro de
/// ligne GLOBAL levait « len is 256 but the index is 256 » dès le deuxième fil).
/// Sous-postes d'`attn_v4`, en nanosecondes : (0) projets q/kv + rotations,
/// (1) compresseur + indexeur, (2) scores + softmax + somme pondérée, (3) sortie
/// groupée. Le profil publiait « somme pondérée + écriture KV » pour TOUT
/// `attn_v4` — une étiquette qui ne décrit que sa dernière partie et qui a fait
/// croire que l'attention de V4.1 ne coûtait rien alors qu'elle coûtait 12,4 s
/// par jeton (relevé au bloc 15).
pub static PROF_V4: [std::sync::atomic::AtomicU64; 5] =
    [const { std::sync::atomic::AtomicU64::new(0) };
     5];

fn matvec_f32_fils(w: &[f32], x: &[f32], n_in: usize, n_out: usize, y: &mut [f32],
                   n_fils: usize) {
    if n_fils <= 1 || n_out < 2 * n_fils || n_out * n_in < 1 << 16 {
        // Trop petit pour payer un `spawn` (mesuré : ~30 µs) : en dessous de
        // 65 536 produits, un fil coûte plus qu'il ne rapporte.
        return matvec_f32(w, x, n_in, n_out, y);
    }
    let par = n_out.div_ceil(n_fils);
    std::thread::scope(|sc| {
        let mut reste: &mut [f32] = &mut y[..n_out];
        let mut o0 = 0usize;
        let mut poignees = Vec::new();
        while o0 < n_out {
            let o1 = (o0 + par).min(n_out);
            let (tranche, reste2) = reste.split_at_mut(o1 - o0);
            reste = reste2;
            let w: &[f32] = w;
            let x: &[f32] = x;
            poignees.push(sc.spawn(move || {
                for (k, o) in (o0..o1).enumerate() {
                    let ligne = &w[o * n_in..(o + 1) * n_in];
                    let mut acc = 0f32;
                    for i in 0..n_in { acc += ligne[i] * x[i]; }
                    tranche[k] = acc;
                }
            }));
            o0 = o1;
        }
        for p in poignees { let _ = p.join(); }
    });
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
    /// **Sonde de plage** (`--tete-partielle`) : appliquer la tête de sortie à la
    /// fin d'une plage PARTIELLE. Par défaut une plage qui n'atteint pas la
    /// dernière couche rend le flux résiduel brut — c'est ce qu'un nœud de
    /// grappe doit expédier. Avec ce drapeau, elle rend les logits d'un modèle
    /// TRONQUÉ, ce qui est la seule façon de vérifier une réduction finale dont
    /// les couches suivantes ne tournent pas encore.
    pub tete_partielle: bool,
    /// Couches MLA, si le modèle en est un (`attn_kv_a_mqa` présent).
    pub mla: Option<Vec<Mla>>,
    /// Fichier d'état d'ENTRÉE (`DRAVE_ETAT_ENTREE`) : le résidu du premier
    /// jeton est lu du disque au lieu de venir de l'embarquement. C'est ce qui
    /// permet d'exécuter **une seule couche** et de la comparer à la référence
    /// quand la précédente n'est pas encore implémentée : on part de l'état que
    /// llama.cpp a produit (`l_last-<k-1>`), et on regarde ce que Drave en fait.
    /// Le fichier est au format `REF_DUMP` (`REFD`, dimensions, f32) ; la
    /// position demandée en est extraite.
    pub etat_entree: Option<String>,
    /// Préfixe de vidage des états de couche (`DRAVE_DUMP_COUCHES`) : après
    /// chaque couche, l'état résiduel est écrit en f32 brut dans
    /// `<préfixe>-<couche>.bin`. C'est le harnais de la porte de correction —
    /// `l_last-<il>` chez llama.cpp, les mêmes octets des deux côtés.
    pub dump_couches: Option<String>,
    /// **Attention V4** par couche (DeepSeek-V4 / V4.1), quand elle est
    /// reconnue (`attn_kv.weight`). Troisième chemin d'attention du moteur.
    pub mla4: Option<Vec<Mla4>>,
    /// Cache de l'attention V4 : une tête latente de `head_dim` par position,
    /// le vecteur déjà tourné (il sert de clé **et** de valeur).
    pub mla4_cache: Vec<Vec<f32>>,
    /// État du compresseur par couche : la valeur et la porte de chaque jeton,
    /// `ctx × coff·head_dim`. Elles servent à fabriquer une clé par bloc.
    pub mla4_comp_kv: Vec<Vec<f32>>,
    pub mla4_comp_gate: Vec<Vec<f32>>,
    /// Clés **compressées** : une par bloc complet (`ctx/ratio + 1`), déjà
    /// normées et tournées. Ce sont des clés d'activation au sens de la vision :
    /// un bloc est un résumé qu'on peut tracer, compter et transporter.
    pub mla4_cles_comp: Vec<Vec<f32>>,
    /// Bornes du **clamp SwiGLU** de DeepSeek-V4, par couche : `swiglu_clamp_exp`
    /// pour les experts, `swiglu_clamp_shexp` pour l'expert partagé (qui
    /// retombe sur la première quand elle est absente). Vide ailleurs.
    pub clamp_exp: Vec<f32>,
    pub clamp_shexp: Vec<f32>,
    /// État et blocs de l'**indexeur** (128 valeurs par bloc).
    pub mla4_idx_kv: Vec<Vec<f32>>,
    pub mla4_idx_gate: Vec<Vec<f32>>,
    pub mla4_idx_cles: Vec<Vec<f32>>,
    /// Scores de l'indexeur par bloc : la « liste de candidats » de la vision,
    /// gardée même quand le top-k les garde tous.
    pub mla4_idx_scores: Vec<Vec<f32>>,
    /// **Hyper-connexions** par couche : `(attention, FFN)`. Présentes sur
    /// DeepSeek-V4 / V4.1 (`hc_attn_fn`), absentes partout ailleurs.
    pub hc: Option<Vec<(Hc, Hc)>>,
    /// Mélange de **tête** : réduit les `hc` copies en un seul état avant la
    /// norme finale et les logits (`hc_head_fn/base/scale`).
    pub hc_tete: Option<Hc>,
    /// **mHC RETARDÉ** (DeepSeek-V4.1 seulement). V4 replie l'entrée d'un
    /// raccord avec les coefficients de CE raccord ; V4.1 les fait **servir au
    /// raccord suivant** — l'attention se replie avec la `pre` de la FFN
    /// précédente, la FFN avec la `pre` de l'attention courante, et la tête avec
    /// la `pre` de la DERNIÈRE FFN (V4.1 n'a pas de `output_hc_*`).
    ///
    /// Source : `vllm/models/deepseek_v41/nvidia/model.py` (`mhc_shifted_post_pre`
    /// + commentaire « the reference collapses each sublayer's input with the
    /// *previous* sublayer's pre-mix », `docs/reports/rapport-v41-mhc.md`).
    pub hc_retarde: bool,
    /// **Engram** (V4.1) : le hachage d'n-grammes et les tables de 101 Go. Les
    /// tables ne sont PAS chargées (elles s'adressent par rangée de 264 octets) ;
    /// ce champ porte le hachage, les premiers, le `token_map`.
    pub engram: Option<Engram>,
    /// Poids d'injection de chaque couche d'engram : `(indice de table, wkv,
    /// q_norm, k_norm)`. `wkv` fait `[(hc+1)·dim, (max_ngram−1)·n_heads·256]` :
    /// il transforme les 24 rangées lues (24 × 256 = 6 144) en `hc` clés plus
    /// **une valeur partagée** (5 × 5120 = 25 600).
    pub engram_poids: Vec<Option<(usize, Vec<f32>, Vec<f32>, Vec<f32>)>>,
    /// Les identifiants déjà vus de la séquence courante : le hachage glissant
    /// lit les `max_ngram − 1` jetons précédents. Rempli par `forward` (un jeton
    /// par appel), remis à zéro en tête de séquence.
    pub historique: Vec<u32>,
    /// **La `pre` portée par le dernier raccord FFN exécuté**, exposée pour le
    /// FLUX : la chaîne mHC retardée de V4.1 en a besoin d'un nœud à l'autre
    /// (`hc` valeurs f32 par jeton, 16 octets), et sans elle un nœud qui reprend
    /// au milieu du modèle replierait avec la copie 0 — faux, et muet. Remplie en
    /// fin de `forward` quand la plage s'arrête avant la dernière couche.
    pub hc_porte_flux: Option<Vec<f32>>,
    /// La `pre` REÇUE d'un autre nœud (protocole v6) : elle amorce la chaîne du
    /// premier raccord au lieu de la copie 0.
    pub hc_porte_imposee: Option<Vec<f32>>,
    /// Cache LATENT par couche : `c_kv` (kv_lora) et `k_rope` (qkr) par position.
    pub mla_cache: Vec<(Vec<f32>, Vec<f32>)>,
    /// Cache VRAM des experts MoE (`DRAVE_GPU_EXPERTS=1`).
    pub cache_experts: Option<CacheExperts>,
    /// Cache RAM des experts (`DRAVE_EXPERTS_RAM`), voir `CacheExpertsRam`.
    pub cache_ram: Option<CacheExpertsRam>,
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

/// L'indexeur de V4.1 (clés tirées du latent du compresseur principal) n'est pas
/// porté : le moteur le dit UNE fois, puis garde tous les blocs — ce qui est
/// exact tant que le nombre de blocs reste sous `indexer.top_k`.
static INDEXEUR_V41_DIT: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);

/// La « convention de sonde » d'une plage V4.1 se dit UNE fois : répétée à chaque
/// jeton, elle noyait 520 lignes de journal pour une seule information.
static PLAGE_V41_DITE: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);

impl Model {
    /// `couches` : exécution **bornée** `[a, b)` — le harnais qui permet
    /// d'exécuter et de COMPARER les couches qui n'ont pas besoin de ce qui
    /// manque encore (les couches 0 et 1 de V4-Flash n'ont pas d'attention
    /// compressée). Le reste du modèle reste déclaré non implémenté : on ne
    /// lève pas un manque, on constate qu'il ne s'applique pas à ce qu'on
    /// exécute — et on le dit.
    pub fn load(path: &str, ctx: usize, n_threads: usize, dense: bool, keep: f32,
                auto: bool, q4: u8, b6: u8) -> Model {
        Self::load_partiel(path, ctx, n_threads, dense, keep, auto, q4, b6, None)
    }

    #[allow(clippy::too_many_arguments)]
    pub fn load_partiel(path: &str, ctx: usize, n_threads: usize, dense: bool, keep: f32,
                        auto: bool, q4: u8, b6: u8, couches: Option<(usize, usize)>) -> Model {
        let t0 = Instant::now();
        let g = Gguf::open_auto(path).expect("ouverture du GGUF");
        let arch = g.meta.get("general.architecture").and_then(|m| m.as_str())
                       .unwrap_or("").to_string();
        let r = routage_du_gguf(&g);
        let (n_expert, n_expert_used, ffn_exp) = (r.n_expert, r.n_expert_used, r.ffn_exp);
        // Ce que le modèle déclare en YaRN : lu DANS le littéral (une seule fois),
        // ressorti ici pour les couches compressées.
        let mut declaration_yarn: Option<(f32, f32, f32, f32)> = None;
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
            // **L'epsilon des normes RMS** : les fichiers convertis depuis
            // HuggingFace le nomment `rms_norm_eps`, ceux de llama.cpp
            // `attention.layer_norm_rms_epsilon`. V4.1-Flash n'a QUE le
            // premier (1e-20) : retomber sur 1e-6 change chaque norme du modèle
            // d'environ 1e-6 en relatif — le niveau même où l'on prétend
            // comparer. (`Hc::melanges` a, lui, 1e-20 en dur.)
            eps: reel_gguf(&g, &["attention.layer_norm_rms_epsilon", "rms_norm_eps"],
                           "rms_norm_eps").unwrap_or(1e-6) as f32,
            rope_base: reel_gguf(&g, &["rope.freq_base", "rope_theta"], "rope_theta")
                           .unwrap_or(10000.0) as f32,
            // `attention.key_length` donne la dimension de tête réelle. Elle
            // n'est PAS toujours hidden/n_head : Qwen3-30B-A3B a 2048 cachés,
            // 32 têtes et 128 par tête, soit 4096 en sortie de Q — l'ancien
            // calcul (64) débordait le tampon de Q.
            head_dim: g.cfg("attention.key_length").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
            vocab: g.tensor("token_embd.weight").map(|t| t.dims[0] as usize).unwrap_or(0),
            // Les trois chiffres du routage viennent de `routage_du_gguf`, qui
            // lit AUSSI le JSON `<arch>.config` : les relire ici en GGUF-seul
            // donnait `n_expert = 0` sur V4.1-Flash (dont le convertisseur n'a
            // écrit que les noms HuggingFace), donc un modèle exécuté SANS un
            // seul expert — la lecture correcte était déjà là, juste jetée.
            n_expert,
            n_expert_used,
            ffn_exp,
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
            // Ce que le modèle DÉCLARE : rempli juste après le littéral, depuis
            // la lecture faite dans le bloc `yarn:` ci-dessous (une seule lecture
            // des métadonnées, deux usages).
            yarn_declare: None,
            yarn: {
                // **Trois sources, dans cet ordre** (le même schéma que le
                // routage) : la clef GGUF normalisée, puis le JSON `<arch>.config`
                // recopié par le convertisseur. V4.1-Flash n'a QUE la seconde —
                // `"rope_scaling":{"rope_type":"yarn","factor":16,…}` — et s'en
                // tenir au GGUF faisait dire « le modèle ne déclare pas YaRN »
                // alors qu'il le déclare, ailleurs. Une rotation fausse ne casse
                // rien : elle donne des scores plausibles dès la position 1.
                let type_declare = g.cfg("rope.scaling.type").and_then(|m| m.as_str())
                    .map(str::to_string)
                    .or_else(|| match g.json_texte("rope_type") {
                        Some(t) if t == "yarn" => Some({
                            println!("[rope] YaRN déclaré par le JSON `<arch>.config` \
(`rope_scaling`), pas par une clef GGUF — lu là, et ANNONCÉ");
                            t
                        }),
                        _ => None,
                    });
                // **`as_f64` ne lit QUE les flottants.** `original_context_length`
                // est un u32 dans le GGUF (`llama_model_loader` l'affiche « u32 ») :
                // le lire avec `as_f64` donnait `None`, donc le DÉFAUT 4096 au lieu
                // de 65 536 — et une rampe de correction deux fois trop large, qui
                // interpolait des paires que la référence n'interpole pas. Le
                // défaut était invisible : la rotation restait plausible, et c'est
                // la comparaison par tenseur qui l'a montré (rampe mesurée (8, 18)
                // au lieu de (15, 25)). Mesuré sur le fichier réel avant/après.
                let nombre = |cle_gguf: &str, cle_json: &str, def: f64| -> f64 {
                    g.cfg(cle_gguf)
                        .and_then(|m| m.as_f64().or_else(|| m.as_u64().map(|v| v as f64)))
                        .or_else(|| g.json_nombre(cle_json))
                        .unwrap_or(def)
                };
                let declare_yarn = match type_declare.as_deref() {
                    Some("yarn") => Some((
                        nombre("rope.scaling.factor", "factor", 1.0) as f32,
                        nombre("rope.scaling.yarn_beta_fast", "beta_fast", 32.0) as f32,
                        nombre("rope.scaling.yarn_beta_slow", "beta_slow", 1.0) as f32,
                        nombre("rope.scaling.original_context_length",
                               "original_max_position_embeddings", 4096.0) as f32,
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
                // La déclaration brute, sans la composante `mscale` (qui est une
                // décision, pas une déclaration).
                let declare_yarn = declare_yarn.map(|(f, bf, bl, o, _)| (f, bf, bl, o));
                declaration_yarn = declare_yarn;
                let declare = declare_yarn.map(|(f, bf, bl, o)| (
                    f, bf, bl, o,
                    std::env::var("DRAVE_YARN_MSCALE").map(|v| v != "0")
                        .unwrap_or_else(|_| std::env::var("DRAVE_YARN").is_ok()),
                ));
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
            c.yarn_declare = declaration_yarn;
            c
        };
        // AVANT toute construction : si le moteur ne sait pas calculer cette
        // architecture, le dire ici, avec la liste de ce qui manque. Sinon la
        // panne arrive trente lignes plus loin sous la forme « tenseur
        // blk.3.attn_q.weight absent » — qui accuse le fichier au lieu du moteur.
        let map = crate::clusters::actif();
        let mut manques = manques_architecture(&g, &cfg, ctx, map.is_some());
        // Exécution bornée : le manque « attentions compressées » ne s'applique
        // que s'il tombe DANS la plage demandée. On le retire en le disant —
        // jamais en silence, et jamais au-delà de la plage.
        if let (Some((a, b)), true) = (couches, !manques.is_empty()) {
            // Ce qui reste non implémenté dans la compression, c'est le chemin
            // **CSA** (ratio 4 : compresseur à chevauchement + indexeur, P5).
            // HCA (ratio 128) est fait ; une plage qui ne contient que du HCA
            // est donc exécutable, et le dire couche par couche vaut mieux
            // qu'un « compressé / pas compressé » binaire.
            let ratios = g.couches_ratios();
            let compressees: Vec<usize> = ratios.iter().enumerate()
                .filter(|(_, r)| **r != 0).map(|(i, _)| i).collect();
            let dedans: Vec<usize> = compressees.iter().copied()
                .filter(|l| *l >= a && *l < b).collect();
            if !dedans.is_empty() {
                let avant = manques.len();
                manques.retain(|m| !m.starts_with("attentions compressées"));
                if manques.len() != avant {
                    println!("[partiel] couches {a}..{b} : le compresseur (HCA ratio 128 et \
CSA ratio 4) est implémenté ; l'INDEXEUR (choix des blocs gardés) ne l'est pas — \
le résultat n'est exact que tant que le nombre de blocs compressés reste sous \
`indexer.top_k`, ce que le moteur vérifie et refuse au-delà. Le RESTE du modèle \
reste non implémenté.");
                }
            }
            // **Un manque qui ne tombe pas dans la plage ne s'applique pas.**
            // V4.1 : les couches 0 et 1 sont en ratio 0 et la couche 1 est la
            // seule engram du début du modèle — une plage 0..1 n'exécute NI
            // compresseur NI engram, donc les manques correspondants ne peuvent
            // pas la rendre fausse. On les retire en le DISANT : l'inverse
            // (garder le refus) interdisait la seule passe avant de V4.1 qui
            // soit fidèle, et l'inverse de l'inverse (retirer sans le dire)
            // ferait croire que tout V4.1 tourne.
            let dans = |l: usize| l >= a && l < b;
            // **L'indexeur de V4.1** (clés tirées du latent du compresseur
            // principal) n'est pas porté : dans une plage qui contient une couche
            // d'indexeur, il est CONTOURNÉ en gardant tous les blocs — exact sous
            // `indexer.top_k`, refusé au-delà, et annoncé une fois à l'exécution.
            // Le dire ici, pour que la plage ne passe pas pour complète.
            let idx_src: Vec<usize> = g.cfg_ou(&["index_source_layer_ids"])
                .and_then(|m| m.as_liste_i64()).unwrap_or_default()
                .into_iter().filter(|l| *l >= 0).map(|l| l as usize).collect();
            if idx_src.iter().any(|l| dans(*l))
                && g.tensor(&format!("blk.0.indexer_compressor_kv.weight")).is_none() {
                println!("[partiel] couches {a}..{b} : l'INDEXEUR de V4.1 (clés tirées du \
latent du compresseur principal, `indexer.attn_k` + `indexer.k_norm`) n'est pas porté — \
le moteur garde tous les blocs, ce qui est exact sous `indexer.top_k` et refusé au-delà.");
            }
        }
        if let Err(raison) = refus_architecture(&g, &cfg, ctx, map.is_some(), manques) {
            panic!("{raison}");
        }
        assert!(cfg.head_dim > 0, "dimension de tête indéterminée");
        assert!(cfg.head_dim * cfg.n_head >= cfg.hidden,
                "n_head × head_dim doit couvrir hidden");
        // Capturé avant que `cfg` ne soit déplacé dans la structure.
        let n_layer_total = cfg.n_layer;
        // Le clamp SwiGLU de V4, par couche — lu AVANT que `g` ne soit déplacé.
        //
        // **Deux façons de le déclarer, et n'en lire qu'une coûtait le modèle.**
        // V4 (V4-Flash) écrit une LISTE par couche (`swiglu_clamp_exp` /
        // `swiglu_clamp_shexp`) ; V4.1 écrit un SCALAIRE `swiglu_limit`. Sans la
        // seconde lecture, `clamp_exp` restait vide, `limite()` rendait 0 et
        // `activation()` prenait la branche SANS clamp : le SwiGLU n'était pas
        // borné, les experts rendaient d'autres valeurs que celles avec
        // lesquelles le modèle a été entraîné, et V4.1 prédisait au niveau du
        // hasard (top-1 0/31, perplexité 3 677 sur huit répétitions d'une phrase
        // là où un modèle qui fonctionne donne 1,8 — mesuré au bloc 20, localisé
        // au bloc 21). V4-Flash, qui déclare la liste, n'était pas touché.
        let scalaire = g.cfg_ou(&["swiglu_limit"]).and_then(|m| m.as_f64()).map(|v| v as f32);
        let liste_ou_scalaire = |cle: &str| -> Vec<f32> {
            match g.cfg_ou(&[cle]).and_then(|m| m.as_liste_f32()) {
                Some(v) if !v.is_empty() => v,
                _ => match scalaire {
                    Some(v) if v > 0.0 => {
                        eprintln!("[config] clamp SwiGLU : `{cle}` absent, `swiglu_limit` = {v} \
appliqué aux {} couches (V4.1 déclare un scalaire, V4 une liste)", cfg.n_layer);
                        vec![v; cfg.n_layer]
                    }
                    _ => Vec::new(),
                },
            }
        };
        let clamp_exp: Vec<f32> = liste_ou_scalaire("swiglu_clamp_exp");
        let clamp_shexp: Vec<f32> = liste_ou_scalaire("swiglu_clamp_shexp");
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
        // ---- Attention V4 (DeepSeek-V4 / V4.1) ----------------------------
        // Reconnue à `attn_kv.weight` : V4 n'a ni `attn_kv_a_mqa` (GLM/Kimi) ni
        // `k_b`/`v_b`. C'est un TROISIÈME chemin, et le confondre avec la MLA
        // existante donnerait des nombres faux de la bonne forme.
        let mla4 = if g.tensor("blk.0.attn_kv.weight").is_some() {
            let dim = |cles: &[&str], json: &str| -> Option<usize> {
                g.cfg_ou(cles).and_then(|m| m.as_u64()).map(|v| v as usize)
                    .or_else(|| g.json_nombre(json).map(|v| v as usize))
            };
            let hd = dim(&["attention.key_length"], "head_dim")
                .unwrap_or_else(|| panic!("attention V4 : `head_dim` introuvable"));
            let nr = dim(&["rope.dimension_count"], "qk_rope_head_dim").unwrap_or(64);

            let q_lora = dim(&["attention.q_lora_rank"], "q_lora_rank")
                .unwrap_or_else(|| g.dequant("blk.0.attn_q_a.weight").len() / cfg.hidden);
            let n_groups = dim(&["attention.output_group_count"], "o_groups").unwrap_or(1);
            let o_lora = dim(&["attention.output_lora_rank"], "o_lora_rank")
                .unwrap_or_else(|| {
                    let n = g.dequant("blk.0.attn_output_a.weight").len();
                    n / (cfg.n_head * hd / n_groups)
                });
            let base = g.cfg_ou(&["rope.freq_base", "rope_theta"])
                .and_then(|m| m.as_f64()).map(|v| v as f32)
                .or_else(|| g.json_nombre("rope_theta").map(|v| v as f32))
                .unwrap_or(10000.0);
            let ratios = g.couches_ratios();
            let base_comp = g.cfg_ou(&["attention.compress_rope_freq_base", "compress_rope_freq_base"])
                .and_then(|m| m.as_f64()).map(|v| v as f32)
                .or_else(|| g.json_nombre("compress_rope_theta").map(|v| v as f32))
                .unwrap_or(base);
            let fenetre = g.cfg_ou(&["attention.sliding_window", "sliding_window"])
                .and_then(|m| m.as_u64()).map(|v| v as usize)
                .or_else(|| g.json_nombre("sliding_window").map(|v| v as usize))
                .unwrap_or(0);
            // **Sources du cache compressé** (`kv_source_layer_ids`, V4.1).
            // V4 ne déclare pas la clé : chaque couche compressée est sa propre
            // source, ce qui est le comportement d'origine.
            let sources: Vec<usize> = g.cfg_ou(&["kv_source_layer_ids"])
                .and_then(|m| m.as_liste_i64())
                .unwrap_or_default()
                .into_iter().filter(|s| *s >= 0).map(|s| s as usize).collect();
            if !sources.is_empty() {
                let mut groupes: Vec<String> = Vec::new();
                for (i, &s) in sources.iter().enumerate() {
                    let fin = sources.get(i + 1).copied().unwrap_or(cfg.n_layer);
                    if s < cfg.n_layer {
                        groupes.push(format!("{s}..{} → {s}", fin.saturating_sub(1)));
                    }
                }
                println!("[config] cache compressé PARTAGÉ entre couches \
(`kv_source_layer_ids`) : {}. Les couches SOURCES projettent leur état ; les \
CONSOMMATRICES lisent les tampons de leur source au lieu d'en calculer d'autres — un \
compresseur par couche donnerait d'AUTRES clés, donc faux sans rien casser",
                         groupes.join(" · "));
            }
            let source_de = |l: usize| -> usize {
                sources.iter().copied().filter(|s| *s <= l).max().unwrap_or(l)
            };
            // **Les couches qui PORTENT un indexeur** (`index_source_layer_ids`,
            // V4.1 : [2,8,14,20,24,28,32,36]). La clé était déclarée par le
            // fichier et lue par personne : les quatre dernières n'ont pourtant
            // pas de compresseur propre, leur cache de clés d'indexeur est celui
            // de leur source de KV (20). Le dire ici, et VÉRIFIER la cohérence :
            // un indexeur hors de cette liste serait un fichier qui se contredit.
            let idx_sources: Vec<usize> = g.cfg_ou(&["index_source_layer_ids"])
                .and_then(|m| m.as_liste_i64())
                .unwrap_or_default()
                .into_iter().filter(|s| *s >= 0).map(|s| s as usize).collect();
            if !idx_sources.is_empty() {
                println!("[config] indexeurs : couches {:?} · les quatre premières \
possèdent le cache de clés, les autres lisent celui de leur source de KV — une couche \
qui porte `indexer.proj` sans être dans cette liste serait un fichier contradictoire",
                         idx_sources);
            }
            let mut v = Vec::with_capacity(cfg.n_layer);
            for l in 0..cfg.n_layer {
                let p = |s: &str| format!("blk.{l}.{s}");
                let ratio = ratios.get(l).copied().unwrap_or(0) as usize;
                // `DRAVE_SANS_COMPRESSION=1` (voir plus haut) : ratio forcé à 0.
                let sans_compression = *SANS_COMPRESSION_EXERCICE.get_or_init(|| {
                    let actif = std::env::var("DRAVE_SANS_COMPRESSION")
                        .map(|v| v != "0" && !v.is_empty()).unwrap_or(false);
                    if actif {
                        eprintln!("[attn] DRAVE_SANS_COMPRESSION est actif : toutes les couches \
sont traitées en ratio 0 (fenêtre brute seule) — ablation pour localiser un défaut, pas V4.1.");
                    }
                    actif
                });
                let ratio_exercice = if sans_compression { 0 } else { ratio };
                let src = if ratio != 0 { source_de(l) } else { l };
                // **Cohérence de la source.** Une couche consommatrice lit l'état
                // publié par sa source : si les deux ratios diffèrent, le nombre
                // de jetons par bloc diffère aussi et le cache lu n'est pas le
                // sien. Le fichier de V4.1 est cohérent (2..7 en ratio 2 autour de
                // la source 2, 21..39 en ratio 1 autour de la 20) ; on le VÉRIFIE
                // plutôt que de l'espérer.
                if ratio != 0 && src != l {
                    let r_src = ratios.get(src).copied().unwrap_or(0) as usize;
                    assert_eq!(r_src, ratio, "couche {l} (ratio {ratio}) : sa source de cache \
compressé est la couche {src} (ratio {r_src}) — les deux ratios doivent être égaux, sinon \
le cache lu n'est pas le sien");
                }
                // Présence de la porte et largeur de l'état : lues sur la SOURCE
                // quand la couche n'a pas ses propres tenseurs.
                let q_src = |s: &str| format!("blk.{src}.{s}");
                let a_porte = ratio > 1
                    && g.tensor(&q_src("attn_compressor_gate.weight")).is_some();
                let candidat_source = g.cfg_ou(&["candidate_source_layer_id"])
                    .and_then(|m| m.as_u64())
                    .or_else(|| g.json_nombre("candidate_source_layer_id").map(|v| v as u64))
                    .map(|v| v as usize).unwrap_or(usize::MAX);
                let candidats_max = {
                    let blocs = g.cfg_ou(&["candidate_topk_blocks"])
                        .and_then(|m| m.as_u64())
                        .or_else(|| g.json_nombre("candidate_topk_blocks").map(|v| v as u64))
                        .unwrap_or(0) as usize;
                    let taille = g.cfg_ou(&["candidate_block_size"])
                        .and_then(|m| m.as_u64())
                        .or_else(|| g.json_nombre("candidate_block_size").map(|v| v as u64))
                        .unwrap_or(1).max(1) as usize;
                    blocs * taille
                };
                let comp_largeur = if ratio != 0 {
                    let t = g.tensor(&q_src("attn_compressor_kv.weight"))
                        .unwrap_or_else(|| panic!("couche {l} : ratio {ratio} mais ni elle ni \
sa source {src} n'a d'`attn_compressor_kv` — le fichier ne dit pas d'où viennent ses clés"));
                    // **Le nombre de RANGÉES du tenseur**, c'est-à-dire
                    // `coff·head_dim` (`dims[0]` : le GGUF range (sortie, entrée) et
                    // le moteur lit ainsi). Ne PAS le diviser par `hidden` : pour un
                    // CSA de V4-Flash le tenseur fait `[1024, 4096]`, et
                    // `1024 / 4096` vaut **0** en arithmétique entière — le
                    // compresseur écrivait alors 512 valeurs au lieu de 1024, et la
                    // porte V4-Flash est tombée de 8430,2968 à 5026,4538 (mesuré,
                    // 02/10, attrapé par la porte et non par les sondes d'une couche,
                    // qui ne voient pas le bloc du DERNIER jeton évalué).
                    t.dims[0] as usize
                } else { 0 };
                // **Un fichier qui se contredit** : une couche qui a ses propres
                // tenseurs de compresseur ET une source déclarée. La référence dit
                // que le compresseur ne vit QUE sur les sources ; la laisser
                // projeter écrirait son état dans les tampons de sa source (le site
                // d'appel les alias) et corromprait les clés de tout le groupe.
                if ratio != 0 && src != l && g.tensor(&p("attn_compressor_kv.weight")).is_some() {
                    panic!("couche {l} : elle a ses propres tenseurs de compresseur ET une \
source de cache compressé déclarée (couche {src}) — le fichier se contredit ; le compresseur \
ne vit que sur les sources (`kv_source_layer_ids`)");
                }
                // Compresseur : `coff = 2` pour CSA (ratio 4), `1` pour HCA
                // (ratio 128). La largeur se lit dans le tenseur, pas dans une
                // constante recopiée : c'est elle qui décide.
                //
                // **Lu en OPTIONNEL, y compris l'`ape` et la porte** : V4.1 a
                // des ratios (1 et 2) où l'un ou l'autre n'existe pas — la
                // référence vLLM le dit (`has_gate = compress_ratio > 1`) et son
                // compresseur n'a pas d'`ape` du tout. Un `dequant` obligatoire
                // faisait paniquer le CHARGEMENT sur un modèle qu'une exécution
                // bornée (`--couches`) n'aurait jamais fait tourner : refuser au
                // chargement ce qu'on ne calcule pas est un refus mal placé.
                // **Lu en OPTIONNEL, y compris la valeur** : V4.1 n'a de
                // compresseur que sur ses couches SOURCES (`kv_source_layer_ids`
                // = [2,8,14,20]) — les couches 3..7 n'ont même pas
                // `attn_compressor_kv`, elles lisent les clés de la 2. Un
                // `dequant` obligatoire faisait paniquer le CHARGEMENT sur un
                // modèle qu'une exécution bornée (`--couches`) n'aurait jamais
                // fait tourner.
                let (comp_kv, comp_gate, comp_ape, comp_norm) = if ratio != 0 {
                    (g.dequant_optionnel(&p("attn_compressor_kv.weight")).unwrap_or_default(),
                     g.dequant_optionnel(&p("attn_compressor_gate.weight")).unwrap_or_default(),
                     g.dequant_optionnel(&p("attn_compressor_ape.weight")).unwrap_or_default(),
                     g.dequant_optionnel(&p("attn_compressor_norm.weight")).unwrap_or_default())
                } else { (Vec::new(), Vec::new(), Vec::new(), Vec::new()) };
                v.push(Mla4 {
                    indexer_top_k: dim(&["attention.indexer.top_k", "index_topk"], "index_topk")
                        .unwrap_or(512),
                    a_indexeur: {
                        let porte = g.tensor(&p("indexer.proj.weight")).is_some();
                        // Un indexeur hors de la liste déclarée : le fichier se
                        // contredit (`index_source_layer_ids`). On le dit, on ne
                        // le calcule pas — la liste est la source de la topologie.
                        if porte && !idx_sources.is_empty() && !idx_sources.contains(&l) {
                            panic!("couche {l} : elle porte un indexeur (`indexer.proj`) mais \
n'est pas dans `index_source_layer_ids` {idx_sources:?} — le fichier se contredit");
                        }
                        porte
                    },
                    a_compresseur: !comp_kv.is_empty(),
                    a_porte,
                    candidats_max,
                    candidat_source,
                    comp_largeur,
                    comp_source: if ratio != 0 { src } else { l },
                    idx_q_b: g.dequant_optionnel(&p("indexer.attn_q_b.weight")).unwrap_or_default(),
                    idx_proj: g.dequant_optionnel(&p("indexer.proj.weight")).unwrap_or_default(),
                    idx_comp_kv: g.dequant_optionnel(&p("indexer_compressor_kv.weight")).unwrap_or_default(),
                    idx_comp_gate: g.dequant_optionnel(&p("indexer_compressor_gate.weight")).unwrap_or_default(),
                    idx_comp_ape: g.dequant_optionnel(&p("indexer_compressor_ape.weight")).unwrap_or_default(),
                    idx_comp_norm: g.dequant_optionnel(&p("indexer_compressor_norm.weight")).unwrap_or_default(),
                    idx_nh: dim(&["attention.indexer.head_count"], "index_n_heads").unwrap_or(0),
                    idx_hd: dim(&["attention.indexer.key_length"], "index_head_dim").unwrap_or(0),
                    idx_k: g.dequant_optionnel(&p("indexer.attn_k.weight")).unwrap_or_default(),
                    idx_k_norm: g.dequant_optionnel(&p("indexer.k_norm.weight")).unwrap_or_default(),
                    a_idx_k: {
                        let possede = g.tensor(&p("indexer.attn_k.weight")).is_some();
                        // **Posséder le cache d'indexeur, c'est être une SOURCE de
                        // KV** (vLLM : « Index K cache: owned only by kv-source
                        // layers »). Un `attn_k` sur une consommatrice écrirait
                        // dans le tampon ALIASÉ de sa source et corromprait les
                        // clés de tout le groupe — refusé.
                        if possede && src != l {
                            panic!("couche {l} : elle porte `indexer.attn_k` (elle possède \
le cache de clés d'indexeur) mais sa source de cache compressé est la couche {src} — le \
fichier se contredit");
                        }
                        possede
                    },
                    q_a: g.dequant(&p("attn_q_a.weight")),
                    q_a_norm: g.dequant(&p("attn_q_a_norm.weight")),
                    q_b: g.dequant(&p("attn_q_b.weight")),
                    kv: g.dequant(&p("attn_kv.weight")),
                    kv_norm: g.dequant(&p("attn_kv_a_norm.weight")),
                    wo_a: g.dequant(&p("attn_output_a.weight")),
                    wo_b: g.dequant(&p("attn_output_b.weight")),
                    sinks: g.dequant_optionnel(&p("attn_sinks.weight")).unwrap_or_default(),
                    nh: cfg.n_head, h: cfg.hidden, head_dim: hd, rope: nr,
                    n_groups, o_lora, rope_base: base, eps: cfg.eps,
                    ratio: ratio_exercice, rope_base_compresse: base_comp, fenetre,
                    // `DRAVE_YARN_NON` (et `--sans-yarn`) veut dire « JAMAIS de YaRN » : il
                    // doit donc aussi couper celui des couches compressées, sinon le
                    // drapeau ne ferait plus ce qu'il annonce. C'est ce qui permet de
                    // MESURER les deux régimes contre llama.cpp.
                    yarn_compresse: if ratio != 0
                        && std::env::var("DRAVE_YARN_NON").is_err() { cfg.yarn_declare } else { None },
                    comp_kv, comp_gate, comp_ape, comp_norm,
                });
            }
            let m0 = &v[0];
            println!("[config] attention V4 : {} couches · 1 tête latente de {} ({} nope + {} rope) \
                      · {} têtes de requête · sortie groupée {}×{} · puits {}",
                     v.len(), m0.head_dim, m0.head_dim - m0.rope, m0.rope, m0.nh,
                     m0.n_groups, m0.o_lora,
                     if m0.sinks.is_empty() { "aucun" } else { "par tête" });
            Some(v)
        } else { None };
        let mla4_cache = match mla4.as_ref() {
            Some(v) => v.iter().map(|m| vec![0f32; ctx * m.head_dim]).collect(),
            None => Vec::new(),
        };
        let largeur_comp = |m: &Mla4| m.comp_kv.len() / m.h.max(1);
        let mla4_comp_kv = match mla4.as_ref() {
            Some(v) => v.iter().map(|m| vec![0f32; ctx * largeur_comp(m)]).collect(),
            None => Vec::new(),
        };
        let mla4_comp_gate = match mla4.as_ref() {
            Some(v) => v.iter().map(|m| vec![0f32; ctx * largeur_comp(m)]).collect(),
            None => Vec::new(),
        };
        let mla4_cles_comp = match mla4.as_ref() {
            Some(v) => v.iter().map(|m| vec![0f32; (ctx / m.ratio.max(1) + 2) * m.head_dim]).collect(),
            None => Vec::new(),
        };
        let largeur_idx = |m: &Mla4| m.idx_comp_kv.len() / m.h.max(1);
        let mla4_idx_kv = match mla4.as_ref() {
            Some(v) => v.iter().map(|m| vec![0f32; ctx * largeur_idx(m)]).collect(),
            None => Vec::new(),
        };
        let mla4_idx_gate = match mla4.as_ref() {
            Some(v) => v.iter().map(|m| vec![0f32; ctx * largeur_idx(m)]).collect(),
            None => Vec::new(),
        };
        let mla4_idx_cles = match mla4.as_ref() {
            Some(v) => v.iter().map(|m| vec![0f32; (ctx / m.ratio.max(1) + 2) * m.idx_hd]).collect(),
            None => Vec::new(),
        };
        let mla4_idx_scores = match mla4.as_ref() {
            Some(v) => v.iter().map(|m| vec![0f32; ctx / m.ratio.max(1) + 2]).collect(),
            None => Vec::new(),
        };

        // ---- Hyper-connexions (DeepSeek-V4 / V4.1) ------------------------
        // Deux sources pour les trois hyper-paramètres, et il faut les deux :
        // V4-Flash les déclare en clés GGUF normalisées
        // (`deepseek4.hyper_connection.*`), V4.1 seulement dans le `config.json`
        // recopié sous `deepseek41.config` (`hc_mult`, `hc_sinkhorn_iters`,
        // `hc_eps`). Lire une seule des deux donne `hc = 0` — donc un modèle
        // silencieusement traité comme s'il n'avait pas d'hyper-connexions.
        // **V4.1 = mHC RETARDÉ.** L'architecture se lit dans
        // `general.architecture` (« deepseek41 » contre « deepseek4 » pour
        // V4-Flash) : c'est elle qui décide QUELLE chaîne de repliement
        // s'applique, et se tromper donne des nombres plausibles et faux — le
        // même genre d'erreur que la base RoPE des couches compressées.
        let hc_retarde = g.meta.get("general.architecture")
            .and_then(|m| m.as_str()) == Some("deepseek41");
        let (hc, hc_tete) = if g.tensor("blk.0.hc_attn_fn.weight").is_some() {
            let (mult, iters, eps) = g.hc_params()
                .unwrap_or_else(|| panic!("hyper-connexions : `hc_mult` introuvable"));
            let mut v = Vec::with_capacity(cfg.n_layer);
            for l in 0..cfg.n_layer {
                let q = |s: &str| format!("blk.{l}.{s}");
                let mk = |nom: &str| Hc {
                    melange: g.dequant(&q(&format!("{nom}_fn.weight"))),
                    base: g.dequant(&q(&format!("{nom}_base.weight"))),
                    scale: g.dequant(&q(&format!("{nom}_scale.weight"))),
                    hc: mult, h: cfg.hidden, iters, eps,
                };
                v.push((mk("hc_attn"), mk("hc_ffn")));
            }
            // Mélange de TÊTE : une seule sortie (`hc` poids), donc son `fn`
            // est `[hc × hc·h]` et sa base `[hc]` — pas de `post` ni de `comb`.
            // Il est FACULTATIF : V4-Flash n'a pas de `hc_head_*` (le fichier
            // de V4.1 non plus, d'ailleurs), et l'exiger ferait paniquer un
            // modèle dont il ne manque qu'une réduction finale.
            // Le tenseur s'appelle **`output_hc_*`** dans le GGUF (la variable
            // de llama.cpp s'appelle `hc_head_*`, et chercher le nom de la
            // variable fait croire que la tête est absente — le moteur paniquait
            // alors à la norme finale, sur un état en `hc` copies normé par un
            // vecteur de `h`).
            let tete = if g.tensor("output_hc_fn.weight").is_some() {
                Some(Hc {
                    melange: g.dequant("output_hc_fn.weight"),
                    base: g.dequant("output_hc_base.weight"),
                    scale: g.dequant("output_hc_scale.weight"),
                    hc: mult, h: cfg.hidden, iters, eps,
                })
            } else if g.tensor("hc_head_fn.weight").is_some() {
                Some(Hc {
                    melange: g.dequant("hc_head_fn.weight"),
                    base: g.dequant("hc_head_base.weight"),
                    scale: g.dequant("hc_head_scale.weight"),
                    hc: mult, h: cfg.hidden, iters, eps,
                })
            } else { None };
            let mix = v[0].0.hc_mix();
            println!("[config] hyper-connexions : {} copies · {} mélanges par couche \
                      (pre {} + post {} + comb {}) · Sinkhorn {} itérations · eps {:e} · {} · \
chaîne {}",
                     mult, mix, mult, mult, mult * mult, iters, eps,
                     match &tete {
                         Some(t) => format!("mélange de tête {} poids", t.melange.len()),
                         None => "pas de mélange de tête (absent du fichier)".to_string(),
                     },
                     if hc_retarde {
                         "RETARDÉE (V4.1) : la `pre` d'un raccord sert au raccord SUIVANT, \
et la tête se replie avec la `pre` de la dernière FFN"
                     } else {
                         "directe (V4) : chaque raccord se replie avec ses propres coefficients"
                     });
            (Some(v), tete)
        } else { (None, None) };
        // **Engram (V4.1)** : les tables de 101 Go chacune ne se CHARGENT pas —
        // elles s'adressent par rangée de 264 octets (`lire_rangee`) ; on ne
        // charge que les projections d'injection (`wkv` [25600, 6144],
        // `q_norm`/`k_norm` [4, 5120]). Le hachage, les premiers et le
        // `token_map` viennent des métadonnées.
        let engram = Engram::depuis_gguf(&g);
        let engram_poids: Vec<Option<(usize, Vec<f32>, Vec<f32>, Vec<f32>)>> =
            (0..cfg.n_layer).map(|l| {
                let idx = engram.as_ref()?
                    .couches.iter().position(|c| *c == l)?;
                let p = |s: &str| format!("blk.{l}.{s}");
                Some((idx,
                      g.dequant(&p("engram_kv.weight")),
                      g.dequant(&p("engram_q_norm.weight")),
                      g.dequant(&p("engram_k_norm.weight"))))
            }).collect();
        if let Some(e) = engram.as_ref() {
            println!("[config] engram : tables sur les couches {:?} (rangées {:?}) · \
{} colonnes de hachage ({} reculs × {} têtes) · injection BRANCHÉE · {} octets lus par \
jeton et par table ({} rangées de 264)",
                     e.couches, e.rangees, e.n_hash_cols(), e.max_ngram - 1, e.n_heads,
                     e.n_hash_cols() * OCTETS_PAR_RANGEE, e.n_hash_cols());
        }
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
                wq: if mla.is_some() || mla4.is_some() { Proj::vide() } else {
                    Proj::load(&g, &p("attn_q.weight"), Some(&p("attn_q.bias")), dense || q4 != 0, auto, keep, q4 & 2 != 0, b6 & 2 != 0) },
                wk: if mla.is_some() || mla4.is_some() { Proj::vide() } else {
                    Proj::load(&g, &p("attn_k.weight"), Some(&p("attn_k.bias")), dense || q4 != 0, auto, keep, q4 & 2 != 0, b6 & 2 != 0) },
                wv: if mla.is_some() || mla4.is_some() { Proj::vide() } else {
                    Proj::load(&g, &p("attn_v.weight"), Some(&p("attn_v.bias")), dense || q4 != 0, auto, keep, q4 & 2 != 0, b6 & 2 != 0) },
                // gpt-oss porte un biais sur la projection de sortie
                // (`attention_bias = true` dans sa config : Q, K, V **et** O).
                // Le passer à `None` l'ignorait silencieusement — un décalage
                // constant ajouté à chaque couche, donc amplifié 36 fois.
                // L'attention V4 n'a pas d'`attn_output.weight` : sa sortie est
                // projetée par groupes DANS `attn_v4` (`attn_output_a` + `_b`).
                wo: if mla4.is_some() { Proj::vide() }
                    else { Proj::load(&g, &p("attn_output.weight"), Some(&p("attn_output.bias")), dense || q4 != 0, auto, keep, q4 & 2 != 0, b6 & 2 != 0) },
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
            // **Le modèle DÉCLARE YaRN, le moteur ne l'applique pas** (V4.1 :
            // `"rope_scaling":{"rope_type":"yarn","factor":16}` dans le JSON).
            // Le dire au lieu de « le modèle ne déclare pas YaRN » : la rotation
            // est fausse dès la position 1, et `DRAVE_YARN=1` l'applique à
            // toutes les positions, comme la référence.
            (None, _, _) if g.cfg("rope.scaling.type").and_then(|m| m.as_str()) == Some("yarn")
                || g.json_texte("rope_type").as_deref() == Some("yarn") =>
                println!("[config] rotation : RoPE simple sur les couches BRUTES (régime \
retardé : YaRN au-delà de quatre fois la longueur d'origine, seuil mesuré sur gpt-oss) — \
mais les couches COMPRESSÉES sont en YaRN ×{} à TOUTES les positions, comme llama.cpp \
(`deepseek4.cpp:872-879`) et vLLM (`rope.py:28-46`) ; `DRAVE_YARN=1`/`--sans-yarn` \
forcent l'un ou l'autre partout",
                         g.cfg("rope.scaling.factor").and_then(|m| m.as_f64())
                          .or_else(|| g.json_nombre("factor")).unwrap_or(1.0)),
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
            mla4, mla4_cache, mla4_comp_kv, mla4_comp_gate, mla4_cles_comp,
            mla4_idx_kv, mla4_idx_gate, mla4_idx_cles, mla4_idx_scores,
            hc, hc_tete, hc_retarde,
            engram, engram_poids, historique: Vec::new(),
            hc_porte_flux: None, hc_porte_imposee: None,
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
            clamp_exp, clamp_shexp,
            etat_entree: std::env::var("DRAVE_ETAT_ENTREE").ok(),
            dump_couches: std::env::var("DRAVE_DUMP_COUCHES").ok(),
            couche_debut: couches.map(|(a, _)| a).unwrap_or(0),
            couche_fin: couches.map(|(_, b)| b).unwrap_or(n_layer_total),
            flux_brut: false, tete_partielle: false,
            cache_experts,
            cache_ram: match std::env::var("DRAVE_EXPERTS_RAM").ok()
                            .and_then(|v| v.parse::<usize>().ok()) {
                Some(mo) if mo > 0 => {
                    println!("[experts] cache RAM des experts : {mo} Mo — ATTENTION, mesuré \
PLUS LENT que le cache de pages du noyau (ctx 32 : +4 % à 4 Go, +21 % à 32 Go ; voir \
`CacheExpertsRam`). Aucun octet du calcul ne change, mais le temps, si.");
                    Some(CacheExpertsRam::nouveau(mo << 20))
                }
                _ => None,
            },
            mla, mla_cache, jeton_trace: 0, trace: None, flux_force: None,
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
        Self::activation(gate, up, n_ff, act_oss, 0.0);
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
    /// Redirige une vue d'expert vers le cache RAM s'il la connaît, et l'y met
    /// sinon. Retourne la vue à employer et le `loc` qui va avec (0 quand la
    /// base pointe déjà sur l'expert).
    fn resident(cache: &mut Option<CacheExpertsRam>, quoi: u8, l: usize, e: usize,
                vue: &Vue4, loc: usize) -> (Vue4, usize) {
        let Some(c) = cache.as_mut() else { return (*vue, loc); };
        match c.pointeur(quoi, l, e) {
            Some(p) => (Vue4 { base: p, ..*vue }, 0),
            None => { c.garder(quoi, l, e, vue, loc); (*vue, loc) }
        }
    }

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
    pub fn cfg_yarn_off(&mut self) {
        // `--sans-yarn` veut dire JAMAIS de YaRN : il coupe le régime retardé des
        // couches brutes ET celui des couches compressées, sinon le drapeau ne
        // ferait pas ce qu'il annonce (relevé par la relecture adverse du 02/10 :
        // `yarn_compresse` était figé à la construction du modèle).
        self.cfg.yarn = None;
        self.cfg.yarn_declare = None;
        if let Some(v) = self.mla4.as_mut() {
            for m in v.iter_mut() { m.yarn_compresse = None; }
        }
    }

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
    /// `clamp_v4` : borne des activations d'expert de DeepSeek-V4 — `gate` est
    /// borné SUPÉRIEUREMENT (`min(g, limite)`), `up` des deux côtés, puis
    /// `silu(gate) * up`. C'est le `swiglu_clamp_exp` du modèle, par couche, et
    /// l'oublier ne se voit que sur les jetons où l'activation dépasse 10.
    fn activation(gate: &mut [f32], up: &[f32], n: usize, oss: bool, clamp_v4: f32) {
        if oss {
            const LIMITE: f32 = 7.0;
            const ALPHA: f32 = 1.702;
            for i in 0..n {
                let g = gate[i].min(LIMITE);
                let u = up[i].clamp(-LIMITE, LIMITE);
                gate[i] = (g / (1.0 + (-ALPHA * g).exp())) * (u + 1.0);
            }
        } else if clamp_v4 > 1e-6 {
            for i in 0..n {
                let g = gate[i].min(clamp_v4);
                let u = up[i].clamp(-clamp_v4, clamp_v4);
                gate[i] = (g / (1.0 + (-g).exp())) * u;
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

    /// Lit un état d'entrée : le fichier de llama.cpp (`REFD`, dimensions,
    /// f32 — la position `pos` est extraite) ou un fichier plat de f32 (celui
    /// que Drave écrit, une position par fichier).
    fn lire_etat(chemin: &str, pos: usize) -> Vec<f32> {
        let b = std::fs::read(chemin).unwrap_or_else(|e|
            panic!("état d'entrée {chemin} : {e}"));
        if b.len() >= 24 && &b[0..4] == b"REFD" {
            let ndim = i32::from_le_bytes(b[4..8].try_into().unwrap()).max(1) as usize;
            let mut ne = [1i32; 4];
            for i in 0..ndim.min(4) {
                ne[i] = i32::from_le_bytes(b[8 + 4 * i..12 + 4 * i].try_into().unwrap());
            }
            let (n0, n1, _n2) = (ne[0].max(1) as usize, ne[1].max(1) as usize, ne[2].max(1) as usize);
            let bloc = n0 * n1;
            let debut = 24 + pos * bloc * 4;
            assert!(debut + bloc * 4 <= b.len(),
                    "état d'entrée {chemin} : position {pos} hors du tenseur {:?}", ne);
            b[debut..debut + bloc * 4].chunks_exact(4)
                .map(|c| f32::from_le_bytes(c.try_into().unwrap())).collect()
        } else {
            b.chunks_exact(4).map(|c| f32::from_le_bytes(c.try_into().unwrap())).collect()
        }
    }

    /// Écrit l'état résiduel d'une couche (f32 brut, machine locale) si le
    /// vidage est demandé. Le format est volontairement le plus bête possible :
    /// c'est `llama.cpp` qui produit l'autre fichier, et le seul contrat est
    /// « mêmes nombres, même ordre » — `n_embd` puis `hc` copies.
    fn vider_couche(prefixe: Option<&str>, nom: &str, l: usize, pos: usize, x: &[f32]) {
        use std::io::Write;
        let Some(p) = prefixe else { return };
        // Le nom porte le tenseur, la couche ET la position : sans la position,
        // un fichier par couche ne garderait que le dernier jeton évalué — et
        // c'est justement au-delà de la position 0 que les écarts apparaissent.
        let chemin = format!("{p}-{nom}-{l}-{pos}.bin");
        match std::fs::File::create(&chemin) {
            Ok(mut f) => {
                let mut octets = Vec::with_capacity(x.len() * 4);
                for v in x { octets.extend_from_slice(&v.to_le_bytes()); }
                if let Err(e) = f.write_all(&octets) {
                    eprintln!("[dump] {chemin} : {e}");
                }
            }
            Err(e) => eprintln!("[dump] {chemin} : {e}"),
        }
    }

    /// **Les 24 poids d'un raccord à hyper-connexions** (4 `pre` + 4 `post` +
    /// 16 `comb`), écrits dans CET ordre — c'est le contrat que lit
    /// `tools/analyse_hc.py`. Ils étaient calculés puis jetés : la porte Drave de
    /// P1 demande qu'ils soient tracés par jeton, et que l'outil dise la
    /// **sparsité** des 16 connexions et leur **stabilité** d'un jeton à l'autre.
    ///
    /// `comb` sort du Sinkhorn : ses lignes et ses colonnes somment à 1 (à `eps`
    /// près), ce que l'outil vérifie — un raccord dont le `comb` n'est pas
    /// bistochastique signalerait que le Sinkhorn n'a pas convergé.
    fn vider_couche_poids_hc(prefixe: Option<&str>, nom: &str, l: usize, pos: usize,
                             s: &HcSortie) {
        if prefixe.is_none() { return; }
        let mut v = Vec::with_capacity(s.pre.len() + s.post.len() + s.comb.len());
        v.extend_from_slice(&s.pre);
        v.extend_from_slice(&s.post);
        v.extend_from_slice(&s.comb);
        Self::vider_couche(prefixe, nom, l, pos, &v);
    }

    /// **RoPE « NORM »** — l'autre convention d'appariement, celle des modèles
    /// Llama et **DeepSeek-V4** (`LLAMA_ROPE_TYPE_NORM` dans llama.cpp) :
    /// les paires sont `(2i, 2i+1)`. Celle de Drave (`rope`) apparie
    /// `(i, i + n_rot/2)`, ce que déclarent GLM et Kimi. Les deux donnent la
    /// même rotation à la position 0 (identité) et divergent ensuite : c'est
    /// exactement la signature qu'a montrée la comparaison à llama.cpp sur
    /// V4-Flash — position 0 juste à 1e-3, position 1 fausse à 30 %.
    fn rope_norm(v: &mut [f32], n_head: usize, head_dim: usize, pos: usize, base: f32,
                 n_rot: usize, inverse: bool) {
        let n_rot = if n_rot == 0 || n_rot > head_dim { head_dim } else { n_rot };
        let half = n_rot / 2;
        for h in 0..n_head {
            let t = &mut v[h * head_dim..(h + 1) * head_dim];
            for i in 0..half {
                // La fréquence suit le même barème dans les deux conventions :
                // seul l'appariement change (`ic = i0` contre `ic = i0/2`).
                let freq = 1.0 / base.powf(2.0 * i as f32 / n_rot as f32);
                let (s, c) = (pos as f32 * freq).sin_cos();
                let (s, c) = if inverse { (-s, c) } else { (s, c) };
                let a = t[2 * i];
                let b = t[2 * i + 1];
                t[2 * i] = a * c - b * s;
                t[2 * i + 1] = b * c + a * s;
            }
        }
    }

    /// **Le RoPE des couches COMPRESSÉES de V4 : convention NORM + YaRN.**
    ///
    /// Pourquoi il existe : llama.cpp (`src/models/deepseek4.cpp:872-879`) **et**
    /// vLLM (`models/deepseek_v41/common/rope.py:28-46`) appliquent YaRN à
    /// TOUTES les positions dès que `compress_ratio > 0`, et le RoPE simple
    /// seulement sur les couches brutes :
    ///
    /// ```c
    /// const bool use_compress_rope = hparams.dsv4_compress_ratios[il] != 0;
    /// const float freq_scale_l = use_compress_rope ? freq_scale : 1.0f;
    /// const float ext_factor_l = use_compress_rope ? ext_factor : 0.0f;
    /// ```
    ///
    /// Le moteur appliquait son régime *retardé* (RoPE simple sous 4 × la
    /// longueur d'origine) sur ces couches aussi, et **aucune vérification ne
    /// pouvait le voir** : YaRN n'interpole que les basses fréquences, dont les
    /// angles sont minuscules aux positions courtes (à la position 4, la paire la
    /// plus lente tourne de 4e-4 rad contre 2,5e-5 interpolée). Les comparaisons
    /// à 0,9999 contre llama.cpp (bloc tourné à la position 4, positions 8-9)
    /// étaient donc aveugles à ce choix ; à la position 1 024 l'écart d'angle
    /// passe à 0,1 rad contre 6,4e-3.
    ///
    /// `mscale` est **désactivé** : llama.cpp le calcule puis l'annule
    /// (`llama-context.cpp:492-494` : « when YARN is applied with yarn_ext_factor
    /// != 0.0f, we need to cancel this factor »), et vLLM le met à 0
    /// (`rope.py:44-45`) — les deux références concordent.
    #[allow(clippy::too_many_arguments)]
    fn rope_norm_yarn(v: &mut [f32], n_head: usize, head_dim: usize, pos: usize, base: f32,
                      facteur: f32, beta_rapide: f32, beta_lent: f32, ctx_origine: f32,
                      n_rot: usize, inverse: bool) {
        let n_rot = if n_rot == 0 || n_rot > head_dim { head_dim } else { n_rot };
        let half = n_rot / 2;
        let ln_base = base.ln();
        // Les dimensions de correction se comptent sur les dimensions TOURNÉES
        // (`rope_yarn_corr_dims(n_dims = rot_dim, …)`), pas sur la tête entière :
        // pour V4 elles font 64, pas 512.
        // **Bornées comme dans les DEUX références** : ggml écrit
        // `dims[0] = MAX(0, start)` et `dims[1] = MIN(n_dims - 1, end)`
        // (`ggml.c:4471-4480`), vLLM `max(low, 0)` / `min(high, dim - 1)`
        // (`rotary_embedding/common.py`, `yarn_find_correction_range`,
        // `truncate=True`). Sans ces bornes, une base petite et un contexte long
        // font sortir la rampe du barème : base 100, ctx 2e6 → (63, 89) au lieu de
        // (63, 63) — la rampe ne se terminerait jamais.
        let corr0 = (n_rot as f32 * (ctx_origine / (beta_rapide * 2.0 * std::f32::consts::PI)).ln()
                     / (2.0 * ln_base)).floor().max(0.0);
        let corr1 = (n_rot as f32 * (ctx_origine / (beta_lent * 2.0 * std::f32::consts::PI)).ln()
                     / (2.0 * ln_base)).ceil().min((n_rot - 1) as f32);
        for h in 0..n_head {
            let t = &mut v[h * head_dim..(h + 1) * head_dim];
            for i in 0..half {
                let freq = 1.0 / base.powf(2.0 * i as f32 / n_rot as f32);
                let theta_extrap = pos as f32 * freq;
                let theta_interp = theta_extrap / facteur;
                let rampe = if std::env::var("DRAVE_YARN_RAMPE").map_or(false, |v| v == "0") {
                    0.0
                } else {
                    let y = (i as f32 - corr0) / (corr1 - corr0).max(0.001);
                    1.0 - y.clamp(0.0, 1.0)
                };
                let theta = theta_interp * (1.0 - rampe) + theta_extrap * rampe;
                let (s, c) = theta.sin_cos();
                let (s, c) = if inverse { (-s, c) } else { (s, c) };
                let a = t[2 * i];
                let bb = t[2 * i + 1];
                t[2 * i] = a * c - bb * s;
                t[2 * i + 1] = bb * c + a * s;
            }
        }
    }

    /// **Rotation INVERSE** (dé-rotation), celle de `ggml_rope_ext_back` :
    /// mêmes appariements, angle opposé. Elle sert à l'attention de V4, qui
    /// tourne la partie rope de sa sortie AVANT la projection groupée.
    fn rope_inverse(v: &mut [f32], n_head: usize, head_dim: usize, pos: usize,
                    base: f32, n_rot: usize) {
        let n_rot = if n_rot == 0 || n_rot > head_dim { head_dim } else { n_rot };
        let half = n_rot / 2;
        for h in 0..n_head {
            let t = &mut v[h * head_dim..(h + 1) * head_dim];
            for i in 0..half {
                let freq = 1.0 / base.powf(2.0 * i as f32 / head_dim as f32);
                let (s, c) = (pos as f32 * freq).sin_cos();
                let a = t[i];
                let b = t[i + half];
                // rotation d'angle −θ : la matrice inverse de `rope`.
                t[i] = a * c + b * s;
                t[i + half] = b * c - a * s;
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
        // **Le chemin par lots ne porte PAS les hyper-connexions** : son corps
        // n'a aucune occurrence de `hc_*`, et l'état résiduel y est donc
        // additionné au lieu d'être remélangé. Un `--lot 8` sur V4-Flash ou V4.1
        // calculait donc un AUTRE modèle, sans un mot — le pire cas du dépôt.
        // On refuse, au lieu de rendre un chiffre faux qui a l'air d'un chiffre.
        // (Vérifié le 02/10 : `grep -c hc` dans le corps de `forward_lot` = 0.)
        if self.hc.is_some() && toks.len() > 1 {
            panic!("chemin par LOTS et hyper-connexions : ce chemin n'est pas porté (le \
résidu y est additionné au lieu d'être remélangé par `hc_post`) — utilisez `--lot 1`, ou \
implémentez-le. Le lot n'est pas neutre ici : il change le modèle");
        }
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
                        Self::activation(&mut col, &colu, nff, self.cfg.ffn_act_oss, 0.0);
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
                    Self::activation(&mut gg, &u0, self.cfg.ffn, self.cfg.ffn_act_oss, 0.0);
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
        // La tete partielle est une SONDE : elle ne rend pas le flux brut.
        if self.flux_brut || (self.couche_fin < self.cfg.n_layer && !self.tete_partielle) {
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

    /// **Attention V4** (`build_raw_attention` + sortie groupée) pour un jeton.
    ///
    /// `cache` porte une seule tête latente par position : `head_dim` valeurs,
    /// le vecteur **déjà tourné** (nope et rope concaténés), puisque c'est lui
    /// qui sert à la fois de clé et de valeur.
    ///
    /// `paires` compte ce que le chemin paie (aucune liste n'est construite
    /// ici) ; `sinks` sont les logits appris ajoutés au **dénominateur** du
    /// softmax, comme le fait `ggml_soft_max_add_sinks`.
    /// **Pool d'un groupe du compresseur** : `Σ_k valeur_k · softmax_k(porte_k)`,
    /// le softmax portant sur l'axe du **groupe** — donc **par canal**, ce que la
    /// référence écrit `tl.softmax(score, 0)` (`fused_save_compress_norm`). Un
    /// softmax par jeton (sur les canaux) donnerait des poids différents et des
    /// blocs faux, sans rien casser.
    ///
    /// `portes = None` : pas de porte (V4.1 en ratio 1) — le groupe fait un seul
    /// jeton et la valeur passe telle quelle. `base` est l'indice du premier jeton
    /// du groupe dans les tampons, `largeur` le pas entre deux jetons.
    fn pool_groupe(valeurs: &[f32], portes: Option<&[f32]>, largeur: usize, n: usize,
                   base: usize, c: usize) -> f32 {
        let Some(p) = portes else { return valeurs[base + c]; };
        let mut mx = f32::NEG_INFINITY;
        for k in 0..n { let v = p[base + k * largeur + c]; if v > mx { mx = v; } }
        let mut somme = 0f32;
        for k in 0..n { somme += (p[base + k * largeur + c] - mx).exp(); }
        let inv = if somme > 0.0 { 1.0 / somme } else { 0.0 };
        let mut acc = 0f32;
        for k in 0..n {
            acc += (p[base + k * largeur + c] - mx).exp() * inv * valeurs[base + k * largeur + c];
        }
        acc
    }

    #[allow(clippy::too_many_arguments)]
    fn attn_v4(m: &Mla4, etat: &mut EtatV4, x: &[f32], pos: usize, att: &mut [f32],
               paires: &mut u64, dump: Option<&str>, l: usize, n_fils: usize) {
        let (nh, hd, nr) = (m.nh, m.head_dim, m.rope);
        let nope = hd - nr;
        let h = m.h;
        let n = pos + 1;
        // Les couches compressées tournent à `compress_rope_freq_base`
        // (160 000) ; les couches brutes à `rope.freq_base` (10 000). Deux
        // régimes, deux bases — et le même `rope_norm` des deux côtés.
        let base_rope = if m.ratio != 0 { m.rope_base_compresse } else { m.rope_base };
        // **La rotation d'une couche compressée est YaRN, pas le RoPE simple.**
        // Une seule porte pour les six rotations de cette fonction (requête, clé,
        // clé de bloc, clé et requête d'indexeur, dé-rotation) : llama.cpp utilise
        // les MÊMES paramètres de rotation pour toutes (`freq_base_l`,
        // `freq_scale_l`, `ext_factor_l`, `n_ctx_orig_l` — `deepseek4.cpp:900`,
        // `:919`, `:1124`), et le moteur doit faire pareil, sinon deux rotations
        // d'une même couche divergeraient.
        if std::env::var("DRAVE_DEBUG_YARN").is_ok() {
            eprintln!("[yarn] couche {l} : ratio {} · yarn_compresse={:?} · base {base_rope}",
                      m.ratio, m.yarn_compresse);
        }
        let tourner = |v: &mut [f32], nh: usize, hd: usize, p: usize, nr: usize, inv: bool| {
            match m.yarn_compresse {
                Some((f, bf, bl, o)) => Self::rope_norm_yarn(v, nh, hd, p, base_rope, f, bf, bl, o, nr, inv),
                None => Self::rope_norm(v, nh, hd, p, base_rope, nr, inv),
            }
        };
        // L'indexeur choisit les blocs gardés ; il n'est pas implémenté. Tant
        // qu'il y a moins de blocs que son top-k, il les garde TOUS — le
        // résultat est alors exact, et on l'exécute. Au-delà, on refuse : un
        // chiffre faux qui a l'air juste coûte plus cher qu'un refus.
        // L'indexeur est implémenté : il n'y a plus à refuser au-delà de son
        // top-k, il CHOISIT les blocs. Le nombre gardé reste borné par lui.

        let t0 = Instant::now();
        // --- requête : descente, norme, remontée, norme PAR TÊTE sans poids
        let mut qr = vec![0f32; m.q_a.len() / h];
        matvec_f32_fils(&m.q_a, x, h, qr.len(), &mut qr, n_fils);
        Self::vider_couche(dump, "qr", l, pos, &qr);
        let mut qrn = vec![0f32; qr.len()];
        Self::rmsnorm(&qr, &m.q_a_norm, m.eps, &mut qrn);
        Self::vider_couche(dump, "qr_norm", l, pos, &qrn);
        let mut q = vec![0f32; nh * hd];
        matvec_f32_fils(&m.q_b, &qrn, qr.len(), nh * hd, &mut q, n_fils);
        // `ggml_rms_norm` SEUL, sur chaque tête : la seconde norme de la
        // référence, sans échelle apprise.
        {
            let mut t = vec![0f32; hd];
            for hh in 0..nh {
                rms_norm_sans_poids(&q[hh * hd..(hh + 1) * hd], m.eps, &mut t);
                q[hh * hd..(hh + 1) * hd].copy_from_slice(&t);
            }
        }
        Self::vider_couche(dump, "q_norm", l, pos, &q);
        // rotation de la partie rope de chaque tête
        {
            let mut qp = vec![0f32; nh * nr];
            for hh in 0..nh {
                qp[hh * nr..(hh + 1) * nr]
                    .copy_from_slice(&q[hh * hd + nope..(hh + 1) * hd]);
            }
            tourner(&mut qp, nh, nr, pos, nr, false);
            for hh in 0..nh {
                q[hh * hd + nope..(hh + 1) * hd].copy_from_slice(&qp[hh * nr..(hh + 1) * nr]);
            }
        }
        // --- clé/valeur : une seule tête latente, normée EN ENTIER
        let mut kv = vec![0f32; hd];
        matvec_f32_fils(&m.kv, x, h, hd, &mut kv, n_fils);
        let mut kvn = vec![0f32; hd];
        Self::rmsnorm(&kv, &m.kv_norm, m.eps, &mut kvn);
        {
            let mut kp = vec![0f32; nr];
            kp.copy_from_slice(&kvn[nope..]);
            tourner(&mut kp, 1, nr, pos, nr, false);
            kvn[nope..].copy_from_slice(&kp);
        }
        Self::vider_couche(dump, "kv_norm", l, pos, &kvn);
        Self::vider_couche(dump, "q_rope", l, pos, &q);
        Self::vider_couche(dump, "kv_rope", l, pos, &kvn);
        PROF_V4[0].fetch_add(t0.elapsed().as_nanos() as u64,
                             std::sync::atomic::Ordering::Relaxed);
        let t1 = Instant::now();
        // ---- compresseur : la valeur et la porte de CE jeton, puis un bloc
        // s'il est complet. Un bloc = un résumé de `ratio` jetons, obtenu par
        // un softmax **par canal** sur les portes (avec l'`ape` du rang dans le
        // bloc), suivi de la norme et d'une rotation à la position du PREMIER
        // jeton du bloc.
        // `DRAVE_SANS_BLOCS=1` : ablation des BLOCS COMPRESSÉS dans l'attention
        // (la fenêtre brute reste). Les couches 2 à 39 de V4.1 sont toutes
        // compressées : si les blocs — ou l'aliasing du cache partagé qui les
        // sert aux couches consommatrices — sont faux, ils empoisonnent le softmax
        // à CHAQUE position, ce qui ressemble exactement au symptôme observé
        // (top-1 0/31, perplexité au niveau du hasard dès la première tranche).
        static SANS_BLOCS: std::sync::OnceLock<bool> = std::sync::OnceLock::new();
        let sans_blocs = *SANS_BLOCS.get_or_init(|| {
            let actif = std::env::var("DRAVE_SANS_BLOCS")
                .map(|v| v != "0" && !v.is_empty()).unwrap_or(false);
            if actif {
                eprintln!("[attn] DRAVE_SANS_BLOCS est actif : l'attention NE VOIT PAS les \
blocs compressés (la fenêtre brute reste) — ablation pour localiser un défaut.");
            }
            actif
        });
        let n_vis = if sans_blocs || m.ratio == 0 { 0 } else { (pos + 1) / m.ratio };
        if m.ratio > 0 {
            // **Deux formes de compresseur, et deux ratios de plus.** V4 (ratios
            // 4 et 128) : la couche projette sa valeur ET sa porte, chacune en
            // `coff·hd` valeurs, plus un `ape` par rang dans le bloc. V4.1
            // (ratios 1 et 2, `vllm/models/deepseek_v41/compressor.py` +
            // `fused_save_compress_norm`) : une valeur de `hd` par jeton, une
            // porte seulement si `ratio > 1` (`has_gate = compress_ratio > 1`),
            // **aucun `ape`**, et le pool est un softmax **par canal** sur le
            // groupe (`tl.softmax(score, 0)`) — ratio 1 = aucun groupe.
            //
            // Une couche CONSOMMATRICE (V4.1, `kv_source_layer_ids`) n'a pas de
            // tenseurs de compresseur : elle lit l'état publié par sa source,
            // dont les tampons sont ceux de la source (le site d'appel les
            // alias). Elle ne réécrit donc pas les blocs.
            assert!(matches!(m.ratio, 1 | 2 | 4 | 128),
                    "compression de ratio {} : le moteur ne connaît que 1 et 2 (V4.1) \
et 4, 128 (V4)", m.ratio);
            // Une couche CONSOMMATRICE (V4.1) n'a pas de tenseurs : elle lit
            // l'état et les blocs publiés par sa SOURCE, dont les tampons sont
            // ceux qu'on lui a passés (le site d'appel les alias). Elle ne
            // projette donc rien et ne réécrit aucun bloc — le faire recalculerait
            // les mêmes nombres avec SES poids, qui n'existent pas.
            let coff_hd = if m.comp_largeur > 0 { m.comp_largeur } else { hd };
            if m.a_compresseur {
                matvec_f32_fils(&m.comp_kv, x, h, coff_hd, &mut etat.comp_kv[pos * coff_hd..(pos + 1) * coff_hd], n_fils);
                let sp = pos % m.ratio;
                if m.a_porte {
                    matvec_f32_fils(&m.comp_gate, x, h, coff_hd, &mut etat.comp_gate[pos * coff_hd..(pos + 1) * coff_hd], n_fils);
                    // L'`ape` est FACULTATIF : V4.1 n'en a aucun (son compresseur n'a
                    // que `kv`, `gate` et `norm`), V4 en a un par rang dans le bloc.
                    if !m.comp_ape.is_empty() {
                        for c in 0..coff_hd {
                            etat.comp_gate[pos * coff_hd + c] += m.comp_ape[sp * coff_hd + c];
                        }
                    }
                }
                Self::vider_couche(dump, "comp_state_kv", l, pos,
                                   &etat.comp_kv[pos * coff_hd..(pos + 1) * coff_hd]);
                Self::vider_couche(dump, "comp_state_gate", l, pos,
                                   &etat.comp_gate[pos * coff_hd..(pos + 1) * coff_hd]);
                *paires += (m.comp_kv.len() + m.comp_gate.len()) as u64;
            }
            if m.a_compresseur && (pos + 1) % m.ratio == 0 {
                let bloc = pos / m.ratio;
                let debut = pos + 1 - m.ratio;
                let (portes, valeurs, cles) = (&etat.comp_gate, &etat.comp_kv, &mut etat.cles_comp);
                // **CSA** (ratio 4) chevauche : la fenêtre d'un bloc est
                // `2 × ratio` jetons — la seconde moitié du bloc PRÉCÉDENT puis le
                // bloc courant. Et les deux moitiés du projecteur de 1024 valeurs
                // ont deux rôles : la première sert quand le jeton est « contexte
                // précédent », la seconde quand il est « bloc courant »
                // (`build_overlap_compressed_kv_from_state`).
                let chevauche = m.ratio == 4;
                let t0 = if chevauche { debut as isize - m.ratio as isize } else { debut as isize };
                let n_fenetre = (pos as isize - t0 + 1) as usize;
                // **Sans porte** (V4.1 en ratio 1) : le groupe fait UN jeton et le
                // softmax d'un singleton vaut 1 — la valeur passe telle quelle.
                // La référence le dit en une ligne : `if COMPRESS_RATIO == 1:
                // pooled = tl.load(raw + ...)`. La présence de la porte se lit sur
                // la SOURCE (`a_porte`) : une couche consommatrice n'a pas le
                // tenseur, mais l'état qu'elle lit a bien été projeté avec lui.
                let sans_porte = !m.a_porte;
                for c in 0..hd {
                    // **Cas SANS chevauchement** (V4.1 ratios 1 et 2, V4 HCA 128) :
                    // le groupe est une fenêtre contiguë qui commence à `t0 ≥ 0`,
                    // donc le pool est exactement `Σ_k valeur_k · softmax_k(porte_k)`
                    // — sorti en fonction pour être testable (l'orientation du
                    // softmax, par canal et non par jeton, ne se voit pas sur un
                    // état constant).
                    if !chevauche {
                        cles[bloc * hd + c] = Self::pool_groupe(
                            valeurs, if sans_porte { None } else { Some(portes) },
                            coff_hd, n_fenetre, t0 as usize * coff_hd, c);
                        continue;
                    }
                    if sans_porte {
                        let t = debut.max(0) as usize;
                        cles[bloc * hd + c] = valeurs[t * hd + c];
                        continue;
                    }
                    let mut mx = f32::NEG_INFINITY;
                    for k in 0..n_fenetre {
                        let t = t0 + k as isize;
                        // Un jeton d'avant le début du texte n'est pas un jeton
                        // du début : la référence ajoute une ligne dont la VALEUR
                        // est nulle mais dont la PORTE vaut **−infini**
                        // (`dsv4_append_zero_row(score_state, true)`), donc son
                        // poids de softmax est nul. Mettre 0 à la place laissait
                        // ce slot compter dans le dénominateur — 0,989 de
                        // corrélation au lieu de 1,000000, et seulement au
                        // PREMIER bloc (les suivants ont de vrais jetons avant).
                        let sc = if t < 0 { f32::NEG_INFINITY } else {
                            let (role, idx) = if chevauche && k < m.ratio { (0, c) } else if chevauche { (1, c) }
                                              else { (0, c) };
                            portes[t as usize * coff_hd + role * hd + idx]
                        };
                        if sc > mx { mx = sc; }
                    }
                    let mut somme = 0f32;
                    for k in 0..n_fenetre {
                        let t = t0 + k as isize;
                        let sc = if t < 0 { f32::NEG_INFINITY } else {
                            let (role, idx) = if chevauche && k < m.ratio { (0, c) } else if chevauche { (1, c) }
                                              else { (0, c) };
                            portes[t as usize * coff_hd + role * hd + idx]
                        };
                        somme += (sc - mx).exp();
                    }
                    let inv = if somme > 0.0 { 1.0 / somme } else { 0.0 };
                    let mut acc = 0f32;
                    for k in 0..n_fenetre {
                        let t = t0 + k as isize;
                        if t < 0 { continue; }
                        let (role, idx) = if chevauche && k < m.ratio { (0, c) } else if chevauche { (1, c) }
                                          else { (0, c) };
                        let w = (portes[t as usize * coff_hd + role * hd + idx] - mx).exp() * inv;
                        acc += w * valeurs[t as usize * coff_hd + role * hd + idx];
                    }
                    cles[bloc * hd + c] = acc;
                }
                Self::vider_couche(dump, &format!("comp_brut{bloc}"), l, pos,
                                   &cles[bloc * hd..(bloc + 1) * hd]);
                // norme RMS du bloc, puis rotation de sa partie rope
                let mut norm = vec![0f32; hd];
                Self::rmsnorm(&cles[bloc * hd..(bloc + 1) * hd], &m.comp_norm, m.eps, &mut norm);
                // **Les clés de l'indexeur de V4.1** se calculent ICI, sur le
                // latent du compresseur AVANT sa rotation (`k_norm(attn_k(latent))`,
                // `indexer_k_norm_rope_store`), et seulement sur les couches qui
                // possèdent le cache : les autres indexeurs lisent le même tampon.
                if m.a_idx_k && !m.idx_k.is_empty() {
                    let idh = m.idx_hd;
                    let mut k = vec![0f32; idh];
                    matvec_f32_fils(&m.idx_k, &norm, hd, idh, &mut k, n_fils);
                    let mut kn = vec![0f32; idh];
                    Self::rmsnorm(&k, &m.idx_k_norm, m.eps, &mut kn);
                    let idr = nr.min(idh);
                    let idn = idh - idr;
                    let mut kp = vec![0f32; idr];
                    kp.copy_from_slice(&kn[idn..]);
                    tourner(&mut kp, 1, idr, debut, idr, false);
                    kn[idn..].copy_from_slice(&kp);
                    etat.idx_cles[bloc * idh..(bloc + 1) * idh].copy_from_slice(&kn);
                    *paires += (m.idx_k.len() + idh) as u64;
                    Self::vider_couche(dump, &format!("idx_bloc{bloc}"), l, pos, &kn);
                }
                {
                    let mut kp = vec![0f32; nr];
                    kp.copy_from_slice(&norm[nope..]);
                    tourner(&mut kp, 1, nr, debut, nr, false);
                    norm[nope..].copy_from_slice(&kp);
                }
                cles[bloc * hd..(bloc + 1) * hd].copy_from_slice(&norm);
                Self::vider_couche(dump, &format!("comp_bloc{bloc}"), l, pos, &norm);
                *paires += (hd as u64) * (m.ratio as u64) * 2;
            }
        }
        PROF_V4[1].fetch_add(t1.elapsed().as_nanos() as u64,
                             std::sync::atomic::Ordering::Relaxed);
        let t2 = Instant::now();
        // ---- indexeur : il NOTE chaque bloc compressé et n'en garde que les
        // `indexer.top_k` meilleurs. Ses blocs sont plus étroits (128 valeurs)
        // mais suivent exactement la même règle de chevauchement que le CSA.
        let mut blocs_gardes: Option<Vec<u32>> = None;
        // **L'indexeur de V4.1 n'a pas de compresseur propre.** Ses clés viennent
        // du latent du compresseur PRINCIPAL (`indexer.attn_k` + `indexer.k_norm`,
        // construites dans le bloc ci-dessus) et les indexeurs qui n'possèdent pas
        // le cache (24, 28, 32, 36) lisent celui de leur source de KV — le site
        // d'appel alias `idx_cles` sur `comp_source` pour tout le monde. Il ne
        // reste donc ici que la REQUÊTE et les POIDS, qui sont propres à la couche.
        let indexeur_v41 = m.a_indexeur && m.idx_comp_kv.is_empty() && m.idx_comp_norm.is_empty();
        if indexeur_v41 && etat.idx_cles.is_empty() && n_vis > 0 {
            panic!("indexeur de V4.1 (couche {l}) : {n_vis} blocs compressés et AUCUNE clé \
d'indexeur — ni la couche ni sa source de KV n'a `indexer.attn_k`");
        }
        if m.a_indexeur {
            let idh = m.idx_hd;
            // **Le compresseur PROPRE de l'indexeur n'existe qu'en V4.** En V4.1 ses
            // clés sont construites avec celles du compresseur principal (plus
            // haut) : il n'y a ici ni projection d'état ni bloc à écrire.
            let iw = if indexeur_v41 { 0 } else { m.idx_comp_kv.len() / h.max(1) };
            if !indexeur_v41 {
                matvec_f32_fils(&m.idx_comp_kv, x, h, iw, &mut etat.idx_kv[pos * iw..(pos + 1) * iw], n_fils);
                matvec_f32_fils(&m.idx_comp_gate, x, h, iw, &mut etat.idx_gate[pos * iw..(pos + 1) * iw], n_fils);
                let sp = pos % m.ratio;
                for c in 0..iw {
                    etat.idx_gate[pos * iw + c] += m.idx_comp_ape[sp * iw + c];
                }
                *paires += (m.idx_comp_kv.len() + m.idx_comp_gate.len()) as u64;
            }
            if !indexeur_v41 && (pos + 1) % m.ratio == 0 {
                let bloc = pos / m.ratio;
                let debut = pos + 1 - m.ratio;
                let t0 = debut as isize - m.ratio as isize;    // chevauchement CSA
                let n_fen = (pos as isize - t0 + 1) as usize;
                let (portes, valeurs) = (&etat.idx_gate, &etat.idx_kv);
                let mut brut = vec![0f32; idh];
                for c in 0..idh {
                    let mut mx = f32::NEG_INFINITY;
                    for k in 0..n_fen {
                        let t = t0 + k as isize;
                        let role = if k < m.ratio { 0 } else { 1 };
                        let sc = if t < 0 { f32::NEG_INFINITY }
                                 else { portes[t as usize * iw + role * idh + c] };
                        if sc > mx { mx = sc; }
                    }
                    let mut somme = 0f32;
                    for k in 0..n_fen {
                        let t = t0 + k as isize;
                        let role = if k < m.ratio { 0 } else { 1 };
                        let sc = if t < 0 { f32::NEG_INFINITY }
                                 else { portes[t as usize * iw + role * idh + c] };
                        somme += (sc - mx).exp();
                    }
                    let inv = if somme > 0.0 { 1.0 / somme } else { 0.0 };
                    let mut acc = 0f32;
                    for k in 0..n_fen {
                        let t = t0 + k as isize;
                        if t < 0 { continue; }
                        let role = if k < m.ratio { 0 } else { 1 };
                        let w = (portes[t as usize * iw + role * idh + c] - mx).exp() * inv;
                        acc += w * valeurs[t as usize * iw + role * idh + c];
                    }
                    brut[c] = acc;
                }
                // norme, puis rotation de la partie rope (comme les blocs CSA)
                let mut norm = vec![0f32; idh];
                Self::rmsnorm(&brut, &m.idx_comp_norm, m.eps, &mut norm);
                let idr = nr.min(idh);
                let idn = idh - idr;
                {
                    let mut kp = vec![0f32; idr];
                    kp.copy_from_slice(&norm[idn..]);
                    tourner(&mut kp, 1, idr, debut, idr, false);
                    norm[idn..].copy_from_slice(&kp);
                }
                etat.idx_cles[bloc * idh..(bloc + 1) * idh].copy_from_slice(&norm);
            }
            // La requête de l'indexeur descend de `qr_norm` (la requête MLA
            // normalisée), pas de l'état : c'est la même « question » posée à
            // une autre résolution.
            if n_vis > 0 {
                let nq = m.idx_nh * idh;
                let mut q = vec![0f32; nq];
                matvec_f32_fils(&m.idx_q_b, &qrn, qr.len(), nq, &mut q, n_fils);
                let idr = nr.min(idh);
                let idn = idh - idr;
                {
                    let mut qp = vec![0f32; m.idx_nh * idr];
                    for hh in 0..m.idx_nh {
                        qp[hh * idr..(hh + 1) * idr]
                            .copy_from_slice(&q[hh * idh + idn..(hh + 1) * idh]);
                    }
                    tourner(&mut qp, m.idx_nh, idr, pos, idr, false);
                    for hh in 0..m.idx_nh {
                        q[hh * idh + idn..(hh + 1) * idh]
                            .copy_from_slice(&qp[hh * idr..(hh + 1) * idr]);
                    }
                }
                let poids = {
                    let mut p = vec![0f32; m.idx_nh];
                    matvec_f32_fils(&m.idx_proj, x, h, m.idx_nh, &mut p, n_fils);
                    let inv = 1.0 / (((idh * m.idx_nh) as f32).sqrt());
                    for v in p.iter_mut() { *v *= inv; }
                    p
                };
                *paires += (m.idx_q_b.len() + m.idx_proj.len()) as u64;
                let mut scores = vec![0f32; n_vis];
                for b in 0..n_vis {
                    let kb = &etat.idx_cles[b * idh..(b + 1) * idh];
                    let mut s = 0f32;
                    for hh in 0..m.idx_nh.min(m.nh) {
                        let mut d = 0f32;
                        for i in 0..idh { d += q[hh * idh + i] * kb[i]; }
                        s += poids[hh] * if d > 0.0 { d } else { 0.0 };   // relu
                    }
                    scores[b] = s;
                }
                Self::vider_couche(dump, "idx_scores", l, pos, &scores);
                for (b, s) in scores.iter().enumerate() { etat.idx_scores[b] = *s; }
                // top-k des blocs : au-delà de `indexer_top_k` il faut CHOISIR,
                // et c'est ce choix qui décide ce que l'attention voit.
                // **Le filtre à deux niveaux** n'est pas porté : au-delà de
                // `candidate_topk_blocks × candidate_block_size` positions
                // compressées, la référence écarte des blocs avant l'indexeur, et
                // choisir sur un ensemble plus large donnerait un autre choix. En
                // dessous, il ne mord pas — le moteur refuse donc au-delà.
                // Seuls les indexeurs APRÈS la source de candidats masquent leurs
                // scores (vLLM, `DeepseekV4Indexer` : les quatre premières ne
                // reçoivent même pas le tampon) — refuser pour toutes serait un
                // sur-refus, c'est-à-dire un refus faux.
                if m.candidats_max > 0 && l > m.candidat_source && n_vis > m.candidats_max {
                    panic!("indexeur de V4.1 (couche {l}) : {n_vis} blocs compressés > \
{} (le filtre à DEUX NIVEAUX de `candidate_*`), qui n'est pas porté — au-delà, choisir \
sur un ensemble plus large que la référence donnerait un autre choix", m.candidats_max);
                }
                let k = n_vis.min(m.indexer_top_k);
                let mut ordre: Vec<u32> = (0..n_vis as u32).collect();
                ordre.sort_by(|&a, &b| scores[b as usize]
                    .partial_cmp(&scores[a as usize]).unwrap_or(std::cmp::Ordering::Equal));
                ordre.truncate(k);
                ordre.sort_unstable();
                // Ce que l'indexeur a RETENU, sous forme de masque : c'est le
                // « flux qui décide de ce que l'attention voit », et sans ce vide
                // on ne peut vérifier que les scores, pas le CHOIX.
                if let Some(pr) = dump {
                    let mut masque = vec![0f32; n_vis];
                    for &b in &ordre { masque[b as usize] = 1.0; }
                    Self::vider_couche(Some(pr), "idx_gardes", l, pos, &masque);
                }
                blocs_gardes = Some(ordre);
            }
        }
        // Ce que l'attention voit en clair : la fenêtre des derniers jetons
        // (`attention.sliding_window`), le reste étant résumé en blocs.
        let debut_fenetre = if m.fenetre > 0 && n > m.fenetre { n - m.fenetre } else { 0 };
        *paires += (m.q_a.len() + m.q_b.len() + m.kv.len()) as u64;
        {
            let cache = &mut etat.cles;
            cache[pos * hd..(pos + 1) * hd].copy_from_slice(&kvn);
        }
        PROF_V4[2].fetch_add(t2.elapsed().as_nanos() as u64,
                             std::sync::atomic::Ordering::Relaxed);
        let t3 = Instant::now();
        // --- scores : `1/sqrt(head_dim)`, puits appris dans le dénominateur.
        //
        // Les clés sont de DEUX sortes, dans cet ordre : la fenêtre brute (les
        // derniers jetons en clair) puis les **blocs compressés** complets. Le
        // masque est celui de la référence : un jeton voit les jetons de sa
        // fenêtre et tous les blocs entièrement révolus — `n_visible =
        // (pos + 1) / ratio`, ce qui est exactement « un bloc n'est visible
        // qu'une fois complet » (`llama-kv-cache-dsv4.cpp`).
        let scale = 1.0 / (hd as f32).sqrt();
        let n_clair = n - debut_fenetre;
        // Les blocs que l'indexeur a gardés (tous, s'il n'y en a pas).
        let gardes: Vec<u32> = blocs_gardes.clone()
            .unwrap_or_else(|| (0..n_vis as u32).collect());
        let n_gardes = gardes.len();
        *paires += (nh as u64) * ((n_clair + n_gardes) as u64) * (hd as u64);
        let mut sortie = vec![0f32; nh * hd];
        let n_cles = n_clair + n_gardes + 1;
        let mut sc = vec![0f32; n_cles];
        let cles_comp = &etat.cles_comp;
        for hh in 0..nh {
            let qh = &q[hh * hd..(hh + 1) * hd];
            for t in debut_fenetre..n {
                let kt = &etat.cles[t * hd..(t + 1) * hd];
                let mut s = 0f32;
                for i in 0..hd { s += qh[i] * kt[i]; }
                sc[t - debut_fenetre] = s * scale;
            }
            for (j, &b) in gardes.iter().enumerate() {
                let kt = &cles_comp[b as usize * hd..(b as usize + 1) * hd];
                let mut s = 0f32;
                for i in 0..hd { s += qh[i] * kt[i]; }
                sc[n_clair + j] = s * scale;
            }
            // le puits : un logit appris, présent dans la somme du softmax mais
            // sans valeur associée — c'est ce qui « draine » l'attention.
            //
            // Il entre BRUT : la référence appelle `ggml_soft_max_ext(kq, mask,
            // kq_scale, …)` (l'échelle s'applique aux scores) PUIS
            // `ggml_soft_max_add_sinks(kq, sinks)` — le puits n'est pas mis à
            // l'échelle. Le multiplier par `1/sqrt(head_dim)` faisait diverger la
            // sortie dès la position 0 (où l'attention est triviale), ce qui a
            // mis la puce à l'oreille : un écart qui n'attend pas la longueur.
            let puits = m.sinks.get(hh).copied().unwrap_or(0.0);
            sc[n_clair + n_gardes] = puits;
            let mut mx = f32::NEG_INFINITY;
            for &v in sc.iter() { if v > mx { mx = v; } }
            let mut somme = 0f32;
            for v in sc.iter_mut() { let e = (*v - mx).exp(); *v = e; somme += e; }
            let inv = if somme > 0.0 { 1.0 / somme } else { 0.0 };
            let out = &mut sortie[hh * hd..(hh + 1) * hd];
            for t in debut_fenetre..n {
                let w = sc[t - debut_fenetre] * inv;
                if w == 0.0 { continue; }
                let kt = &etat.cles[t * hd..(t + 1) * hd];
                for i in 0..hd { out[i] += w * kt[i]; }
            }
            for (j, &b) in gardes.iter().enumerate() {
                let w = sc[n_clair + j] * inv;
                if w == 0.0 { continue; }
                let kt = &cles_comp[b as usize * hd..(b as usize + 1) * hd];
                for i in 0..hd { out[i] += w * kt[i]; }
            }
        }
        Self::vider_couche(dump, "attn_brut", l, pos, &sortie);
        PROF_V4[3].fetch_add(t3.elapsed().as_nanos() as u64,
                             std::sync::atomic::Ordering::Relaxed);
        let t4 = Instant::now();
        // --- dé-rotation de la partie rope, par tête
        {
            let mut op = vec![0f32; nh * nr];
            for hh in 0..nh {
                op[hh * nr..(hh + 1) * nr]
                    .copy_from_slice(&sortie[hh * hd + nope..(hh + 1) * hd]);
            }
            // `base_rope` et non `m.rope_base` : la dé-rotation doit être
            // l'inverse EXACTE de la rotation appliquée à `q` et `kv`, sinon on
            // « dé-tourne » d'un angle qui n'a jamais été appliqué. C'est le
            // bug qui a coûté le plus cher à voir : les 448 dimensions nope
            // étaient justes à 0,4 %, les 64 dimensions rope fausses de 10 %,
            // et la corrélation globale (0,996) restait « plausible ».
            tourner(&mut op, nh, nr, pos, nr, true);
            for hh in 0..nh {
                sortie[hh * hd + nope..(hh + 1) * hd]
                    .copy_from_slice(&op[hh * nr..(hh + 1) * nr]);
            }
        }
        // --- sortie GROUPÉE : `wo_a` par groupe de têtes, puis `wo_b`
        let hpg = nh / m.n_groups;                 // têtes par groupe
        let gdim = hpg * hd;                       // entrée d'un groupe
        let mut oa = vec![0f32; m.n_groups * m.o_lora];
        for g in 0..m.n_groups {
            let bloc = &m.wo_a[g * m.o_lora * gdim..(g + 1) * m.o_lora * gdim];
            let entree = &sortie[g * gdim..(g + 1) * gdim];
            matvec_f32_fils(bloc, entree, gdim, m.o_lora, &mut oa[g * m.o_lora..(g + 1) * m.o_lora], n_fils);
        }
        Self::vider_couche(dump, "attn_derope", l, pos, &sortie);
        *paires += (m.wo_a.len() + m.wo_b.len()) as u64;
        matvec_f32_fils(&m.wo_b, &oa, m.n_groups * m.o_lora, h, att, n_fils);
        // Seulement `h` valeurs : `att` est dimensionné `nh × head_dim` pour le
        // chemin dense, et vider le tampon entier noierait la sortie dans des
        // valeurs périmées (la comparaison a signalé « longueurs différentes »).
        Self::vider_couche(dump, "attn_out", l, pos, &att[..h]);
        PROF_V4[4].fetch_add(t4.elapsed().as_nanos() as u64,
                             std::sync::atomic::Ordering::Relaxed);
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
        // Les projections f32 de ce chemin étaient mono-fil : la parallélisation
        // par LIGNES ne change pas un bit (chaque ligne garde son ordre de sommation).
        let n_fils = self.pool.threads();
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
            matvec_f32_fils(&m.q_a, &hn, h, m.q_lora, &mut qa, n_fils);
            let mut qan = vec![0f32; m.q_lora];
            Self::rmsnorm(&qa, &m.q_a_norm, eps, &mut qan);
            let nq = nh * (qkn + qkr);
            let mut qb = vec![0f32; nq];
            matvec_f32_fils(&m.q_b, &qan, m.q_lora, nq, &mut qb, n_fils);
            // --- KV : descente MQA, norme sur la partie latente, remontée
            let mut kva = vec![0f32; kvl + qkr];
            matvec_f32_fils(&m.kv_a, &hn, h, kvl + qkr, &mut kva, n_fils);
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
                    matvec_f32_fils(&m.kv_b, &ckv[t * kvl..(t + 1) * kvl], kvl, nh * (qkn + vd), &mut kvt, n_fils);
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
                    matvec_f32_fils(&m.kv_b, &ckv[t * kvl..(t + 1) * kvl], kvl, nh * (qkn + vd), &mut kvt, n_fils);
                    let vt = &kvt[hh * (qkn + vd) + qkn..(hh + 1) * (qkn + vd)];
                    let w = sc[t] * inv;
                    for i in 0..vd { sortie[hh * vd + i] += w * vt[i]; }
                }
            }
            // --- projection de sortie et résidu
            let mut o = vec![0f32; h];
            matvec_f32_fils(&m.wo, &sortie, nh * vd, h, &mut o, n_fils);
            for i in 0..h { x[i] += o[i]; }
            // --- FFN (les poids du harnais sont en f32, donc lus ici)
            Self::rmsnorm(&x, &m.ffn_norm, eps, &mut hn);
            let mut g_t = vec![0f32; m.ffn];
            let mut u_t = vec![0f32; m.ffn];
            matvec_f32_fils(&m.gate, &hn, h, m.ffn, &mut g_t, n_fils);
            matvec_f32_fils(&m.up, &hn, h, m.ffn, &mut u_t, n_fils);
            let mut act = vec![0f32; m.ffn];
            Self::activation(&mut g_t, &u_t, m.ffn, false, 0.0);
            for i in 0..m.ffn { act[i] = g_t[i]; }
            let mut d = vec![0f32; h];
            matvec_f32_fils(&m.down, &act, m.ffn, h, &mut d, n_fils);
            for i in 0..h { x[i] += d[i]; }
        }
        if (self.couche_fin >= self.cfg.n_layer || self.tete_partielle) && !self.flux_brut {
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
        // Fils pour la déquantification des experts **sans noyau** (grilles Q2_K
        // & co, c'est-à-dire tous les experts de V4.1). Ils étaient BORNÉS à 8
        // sur une machine qui en a 20 : mesuré au bloc 17, ce chemin de
        // déquantification est **borné par le calcul** (deux passes identiques,
        // la seconde trouvant 12 Go d'experts dans le cache de pages, donnent le
        // même temps à 0,1 s près) — un fil en plus est donc un gain direct, et
        // le découpage par lignes le rend identique au bit près.
        let threads_iq = self.pool.threads().clamp(1, 32);
        // Diagnostic `DRAVE_DEBUG_ETAT=1` : la norme de l'état résiduel à chaque
        // couche. Un modèle qui prédit le MÊME jeton à toutes les positions a un
        // état qui ne dépend plus de l'entrée ; cette ligne dit à quelle couche
        // il cesse d'en dépendre (explosion, effondrement, ou rien du tout).
        let debug_etat = std::env::var("DRAVE_DEBUG_ETAT").is_ok();
        let debug_mla = std::env::var("DRAVE_DEBUG_MLA").is_ok();
        self.profil_jetons += 1;
        let Model { g, cfg, layers, out_norm, pool, kv, events, attn_events, kv_gpu,
                    attn_gpu_part, emb_imposee, paires, clamp_exp, clamp_shexp, .. } = self;
        // Borne du clamp SwiGLU de la couche : celle des experts, ou celle de
        // l'expert partagé (qui retombe sur la première si le modèle ne déclare
        // que `swiglu_clamp_exp` — c'est le cas de V4-Flash).
        let limite = |l: usize, partage: bool| -> f32 {
            let v = if partage { clamp_shexp.get(l).copied().unwrap_or(0.0) }
                    else { clamp_exp.get(l).copied().unwrap_or(0.0) };
            if v > 0.0 { v } else { clamp_exp.get(l).copied().unwrap_or(0.0) }
        };
        let h = cfg.hidden;
        let hd = cfg.head_dim;
        let nh = cfg.n_head;
        let nkv = cfg.n_kv_head;
        let rep = nh / nkv;
        let ctx = self.ctx;

        // Injection : un vecteur imposé (embedding d'image) remplace la ligne
        // `token_embd` pour cet appel, et seulement pour lui — c'est le seul
        // ajout d'architecture que la vision demande au moteur.
        let mut x = match self.etat_entree.as_ref() {
            // État d'entrée imposé : on démarre la boucle de couches avec le
            // résidu d'un AUTRE moteur, à la position demandée. Le fichier est
            // celui de llama.cpp (`REFD`) ; un fichier plat de f32 est accepté
            // aussi, parce que c'est ce que Drave écrit.
            Some(chemin) => Self::lire_etat(chemin, pos),
            None => match emb_imposee.take() {
                Some(v) => v,
                None => g.row_f32("token_embd.weight", tok as usize, h),
            },
        };
        // **Historique des jetons**, pour le hachage glissant de l'engram : le
        // préfixe de la séquence courante. Remis à zéro quand `pos` repart à 0
        // (chaque fenêtre de perplexité est une séquence neuve), puis complété.
        // Sans cela, le hachage d'un n-gramme lirait les jetons d'une AUTRE
        // fenêtre — des adresses plausibles et fausses.
        // Ce qui ARRIVE du flux, vidé tel quel : sans ce vide, un état reçu
        // « presque juste » est indiscernable d'un état reçu juste, et la couture
        // entre deux nœuds devient impossible à localiser (mesuré : la couche 20
        // d'un V4.1 découpé diffère de la passe complète, et il faut savoir si
        // c'est l'état reçu ou la `pre` reçue qui est en cause).
        Self::vider_couche(self.dump_couches.as_deref(), "etat_impose", 0, pos, &x);
        if pos == 0 { self.historique.clear(); }
        if self.historique.len() == pos { self.historique.push(tok); }
        else if self.historique.len() > pos { self.historique.truncate(pos); self.historique.push(tok); }
        debug_assert_eq!(self.historique.len(), pos + 1);
        // Hyper-connexions : l'état résiduel naît en `hc` copies IDENTIQUES de
        // l'embarquement (la référence fait `ggml_repeat_4d(inp, n_embd, hc)`),
        // et chaque sous-couche les remélangera.
        //
        // **Sans mélange de tête**, deux cas — et ils ne se confondent pas :
        //  · V4.1 (`hc_retarde`) : il n'y a PAS de tête apprise, la référence
        //    replie les copies avec la `pre` de la dernière FFN
        //    (`hc_collapse_triton(hidden, pre_mix)`), donc rien ne manque ;
        //  · tout autre modèle à `hc_*` sans `output_hc_*` : le fichier ne dit
        //    pas comment réduire les copies. Le dire vaut mieux qu'inventer une
        //    moyenne — c'est la question de provenance qui a ouvert P7.
        if let Some((ha, _)) = self.hc.as_ref().map(|v| &v[0]) {
            assert!(self.hc_tete.is_some() || self.hc_retarde,
                    "hyper-connexions sans `output_hc_fn` : le fichier ne dit pas \
comment réduire les {} copies en un état avant la norme finale (et son architecture \
n'est pas `deepseek41`, donc la chaîne retardée de V4.1 ne s'applique pas)",
                    ha.hc);
        }
        // **Chaîne retardée** : le repliement d'un raccord se fait avec les
        // coefficients PORTÉS depuis le raccord précédent — `None` au premier,
        // où la référence sélectionne la copie 0 (`residual[:, 0]`).
        // La chaîne retardée s'amorce sur la `pre` REÇUE si le flux en portait
        // une (protocole v6), sinon sur rien — c'est-à-dire la copie 0, la
        // convention du tout premier raccord du modèle.
        //
        // **Elle ne s'amorce sur la `pre` reçue que si CE nœud REPREND au
        // milieu du modèle** (`--couches a:b` avec a > 0, ou nœud moteur d'un
        // flux) : lui seul a besoin d'un chaînon précédent pour son premier
        // raccord, qui n'est pas celui du modèle. Un nœud qui commence à la
        // couche 0 voit un jeton NEUF entrer par l'embarquement : sa chaîne
        // repart de la copie 0, exactement comme la référence — et la `pre`
        // qu'il a reçue du pair appartient à la RÉDUCTION FINALE de ce jeton-là
        // (elle est lue par `norme_finale`, qui ne la consomme pas).
        //
        // La prendre ici la faisait consommer par le jeton SUIVANT : mesuré, le
        // pilote V4.1 de `--ppl-reparti` gardait la `pre` du pair au titre du
        // jeton 0, la réinjectait dans la chaîne du jeton 1, et rendait une
        // perplexité de 514 722,06 au lieu de 1 743 713,62 — la position 0
        // exacte au bit près, les suivantes fausses, sans un mot. Un défaut
        // muet de plus, et il ne pouvait apparaître que sur un modèle à chaîne
        // retardée (V4.1) : V4-Flash, dont la réduction finale est apprise,
        // ignore ce champ et restait exact.
        let reprend = self.couche_debut > 0;
        let recue = reprend && self.hc_porte_imposee.is_some();
        let mut hc_porte: Option<Vec<f32>> =
            if reprend { self.hc_porte_imposee.take() } else { None };
        // Un nœud qui REPREND à la couche k reçoit un flux brut : s'il ne porte
        // pas ces coefficients (protocole < v6), V4.1 replierait avec la copie 0
        // — faux, et muet. Depuis la v6 le flux les transporte (16 octets par
        // jeton), et le refus ne tombe plus que sur un flux qui ne les a pas.
        assert!(!(self.hc_retarde && self.flux_brut && self.couche_debut > 0 && !recue),
                "V4.1 découpé : la chaîne mHC retardée a besoin de la `pre` portée par \
le raccord précédent — un nœud qui reprend à la couche {} sans l'avoir reçue replierait \
avec la copie 0 (faux, et muet)", self.couche_debut);
        // SONDE LOCALE (`--couches a:b`, pas de flux) : la plage commence au
        // milieu du modèle, donc la `pre` du raccord précédent n'existe pas. On
        // replie le premier raccord avec la copie 0 — la convention de la
        // référence au PREMIER raccord du modèle — et on le DIT : ce n'est plus
        // la chaîne du modèle, c'est une convention de sonde.
        if self.hc_retarde && self.couche_debut > 0 && !self.flux_brut
            && !PLAGE_V41_DITE.swap(true, std::sync::atomic::Ordering::Relaxed) {
            eprintln!("[plage] V4.1 : la plage commence à la couche {} — la `pre` portée par \
le raccord précédent n'existe pas, le premier raccord se replie donc avec la COPIE 0 \
(convention de sonde, comme au tout premier raccord du modèle)", self.couche_debut);
        }
        // Un état reçu d'un autre nœud arrive DÉJÀ en `hc` copies : ne pas les
        // multiplier une seconde fois.
        if let Some((ha, _)) = self.hc.as_ref().map(|v| &v[0]) {
            if x.len() == h {
                let mut copies = Vec::with_capacity(ha.hc * h);
                for _ in 0..ha.hc { copies.extend_from_slice(&x); }
                x = copies;
            }
        }
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

        // `DRAVE_SANS_ENGRAM=1` : mesure de VIVACITÉ, lue une fois et ANNONCÉE.
        // Une injection branchée, vérifiée contre la référence numpy et non nulle
        // peut encore n'entrer dans aucun calcul sans que rien ne le dise ; le
        // seul moyen de l'établir est de couper et de regarder bouger. Le chiffre
        // obtenu n'est plus V4.1 (l'engram est 55 % du fichier), et le moteur le
        // dit au lieu de le laisser croire.
        // `DRAVE_V41_SANS_RETARD=1` : ablation de la règle RETARDÉE de V4.1 (les
        // coefficients d'un raccord servent au raccord SUIVANT). Diagnostic pur,
        // né du constat du bloc 20 — V4.1 ne prédit pas (top-1 0/31) alors que
        // V4-Flash, qui partage tout le reste du chemin, prédit (1,875 contre
        // 1,844 pour llama.cpp). Avec ce drapeau, V4.1 se replie comme V4 (chaque
        // raccord avec SES coefficients) : si la perplexité s'effondre vers 2,
        // c'est la règle du retard qui est fausse — pas le reste.
        static SANS_RETARD: std::sync::OnceLock<bool> = std::sync::OnceLock::new();
        let sans_retard = *SANS_RETARD.get_or_init(|| {
            let actif = std::env::var("DRAVE_V41_SANS_RETARD")
                .map(|v| v != "0" && !v.is_empty()).unwrap_or(false);
            if actif {
                eprintln!("[mhc] DRAVE_V41_SANS_RETARD est actif : la chaîne retardée est \
remplacée par la convention V4 (chaque raccord se replie avec SES coefficients). Ce n'est \
plus V4.1 — c'est une ablation pour localiser un défaut.");
            }
            actif
        });
        let retarde = self.hc_retarde && !sans_retard;
        // `DRAVE_V41_TETE_COPIE0=1` : la TÊTE de V4.1 (repliement final par la
        // `pre` de la dernière FFN) est remplacée par la copie 0 — l'alternative
        // la plus simple, et la seule autre convention que le fichier permet.
        // La tête est le seul endroit entre l'état et les logits : une erreur y
        // produit exactement ce qu'on observe (logits au niveau du hasard).
        static TETE_COPIE0: std::sync::OnceLock<bool> = std::sync::OnceLock::new();
        let tete_copie0 = *TETE_COPIE0.get_or_init(|| {
            let actif = std::env::var("DRAVE_V41_TETE_COPIE0")
                .map(|v| v != "0" && !v.is_empty()).unwrap_or(false);
            if actif {
                eprintln!("[mhc] DRAVE_V41_TETE_COPIE0 est actif : la réduction finale \
replie la COPIE 0 au lieu de la `pre` de la dernière FFN — ablation de diagnostic.");
            }
            actif
        });

        static SANS_ENGRAM: std::sync::OnceLock<bool> = std::sync::OnceLock::new();
        let sans_engram = *SANS_ENGRAM.get_or_init(|| {
            let actif = std::env::var("DRAVE_SANS_ENGRAM")
                .map(|v| v != "0" && !v.is_empty()).unwrap_or(false);
            if actif {
                eprintln!("[engram] DRAVE_SANS_ENGRAM est actif : l'injection de l'engram \
est COUPÉE — le moteur calcule un autre modèle que V4.1, pour mesurer ce que l'engram \
change (vivacité). Ce chiffre ne vaut pas comme référence.");
            }
            actif
        });

        // La plage PORTÉE par ce nœud (`couche_debut..couche_fin`), et non
        // `0..n_layer` : un nœud qui reçoit un flux reprend à SA première couche.
        // La boucle partait de zéro — le pilote calculait donc les 24 couches,
        // envoyait l'état final, et le pair les recalculait toutes par-dessus :
        // perplexité répartie 798,3 au lieu de 18,2. `forward_lot` et
        // `forward_mla` respectaient déjà la plage ; `forward` était l'exception.
        for l in self.couche_debut..self.couche_fin {
            let lay = &layers[l];
            // **Engram (V4.1)** : l'injection se fait AVANT les mélanges du
            // raccord d'entrée — la référence écrit `residual = self.engram(
            // previous_post, …)` PUIS `mhc_pre(residual, …)` — et sur le flux
            // ENTIER (`hc` copies), chaque copie ayant sa porte. Les 24 rangées
            // (24 × 264 octets) sont lues dans la table de 101 Go : c'est le
            // seul accès aléatoire du modèle, et il est mesuré.
            //
            // `DRAVE_SANS_ENGRAM=1` coupe l'injection. Ce n'est PAS un réglage
            // de production : c'est l'instrument qui manquait pour répondre à
            // « l'engram est-il vivant ? » — une injection branchée, vérifiée
            // contre la référence numpy et non nulle peut encore n'entrer dans
            // aucun calcul sans que rien ne le dise. Le moteur ANNONCE qu'il
            // calcule un autre modèle, une fois, et le résultat n'est plus V4.1.
            if !sans_engram {
            if let Some(Some((ti, wkv, qn, kn))) = self.engram_poids.get(l) {
                if let Some(eng) = self.engram.as_ref() {
                    let nhc = eng.n_hash_cols();
                    let dim = cfg.hidden;
                    let hcc = self.hc.as_ref().map(|v| v[0].0.hc).unwrap_or(1);
                    // Les adresses se calculent sur la FENÊTRE du hachage, pas sur
                    // tout le préfixe : un n-gramme de taille `max_ngram` ne regarde
                    // que `max_ngram − 1` jetons en arrière, donc il faut et il
                    // suffit des `max_ngram` derniers jetons (le courant compris) —
                    // c'est ce que découpe `lo = pos − (max_ngram − 1)`. Recalculer le préfixe entier coûtait
                    // O(position) par jeton et par couche — quadratique sur une
                    // séquence, pour un résultat identique (le vérificateur compare
                    // justement les deux : il recalcule, lui, sur tout le préfixe).
                    let lo = pos.saturating_sub(eng.max_ngram - 1);
                    let ids: Vec<u32> = self.historique[lo..=pos].to_vec();
                    let positions: Vec<usize> = (lo..=pos).collect();
                    // Texte seul : `dead_mask` est le masque des IMAGES
                    // (`image_sentinel_mask`), vide ici — et le masque d'injection
                    // est son complément, donc « garder partout ».
                    let morts = vec![false; ids.len()];
                    let adr = eng.adresses(&ids, &positions, &morts);
                    let base = ((ids.len() - 1) * eng.couches.len() + *ti) * nhc;
                    let mut rangee = vec![0f32; nhc * VALEURS_PAR_RANGEE];
                    let lue = eng.couches[*ti];
                    for col in 0..nhc {
                        let r = adr[base + col] as i64;
                        let vals = crate::engram::lire_rangee(g, lue, r)
                            .unwrap_or_else(|| panic!("engram couche {lue} : rangée {r} \
hors de la table ({} rangées)", eng.rangees[*ti]));
                        rangee[col * VALEURS_PAR_RANGEE..(col + 1) * VALEURS_PAR_RANGEE]
                            .copy_from_slice(&vals);
                    }
                    let kv_dim = (hcc + 1) * dim;
                    let mut kv = vec![0f32; kv_dim];
                    matvec_f32_fils(wkv, &rangee, nhc * VALEURS_PAR_RANGEE, kv_dim, &mut kv, pool.threads());
                    let porte = PorteEngram { hc: hcc, dim, eps: cfg.eps, clamp: 1e-6 };
                    let mut injecte = vec![0f32; hcc * dim];
                    porte.injecter(&x, &kv, qn, kn, None, &mut injecte);
                    x = injecte;
                    // Ce que l'injection coûte : les 24 rangées lues, la
                    // projection `wkv` (24×256 → 5×5120) et les deux normes.
                    paires[0] += (nhc * VALEURS_PAR_RANGEE * kv_dim
                                  + 2 * hcc * dim + hcc * dim) as u64;
                    Self::vider_couche(self.dump_couches.as_deref(), "engram_kv", l, pos, &kv);
                    Self::vider_couche(self.dump_couches.as_deref(), "engram_sortie",
                                       l, pos, &x);
                }
            }
            }
            // Fenêtre EFFECTIVE de cette couche : le motif déclaré (gpt-oss :
            // une couche sur deux en attention complète) prime sur le réglage
            // global. Lue en champs directs : `self` est déjà déstructuré.
            let fen = if self.attn_window == 0 { 0 }
                      else if self.swa_pattern <= 1 { self.attn_window }
                      else if l % self.swa_pattern < self.swa_pattern - 1 { self.attn_window }
                      else { 0 };
            // ---- hyper-connexions : l'entrée de l'attention n'est pas l'état,
            // c'est le MÉLANGE de ses `hc` copies (`pre`), et la sortie sera
            // re-router par `comb` au lieu d'être additionnée.
            let hc_l = self.hc.as_ref().map(|v| &v[l]);
            let mut hc_attn: Option<HcSortie> = None;
            let mut xin = vec![0f32; h];
            match hc_l {
                Some((ha, _)) => {
                    let s = ha.sortie(&x);
                    // **Les 24 poids de connexion du raccord** (4 `pre` + 4 `post`
                    // + 16 `comb`) : c'est le flux de P1 — ils étaient calculés
                    // puis JETÉS, donc muets. La porte Drave de P1 demande qu'ils
                    // soient écrits, relus et analysés (`tools/analyse_hc.py`).
                    Self::vider_couche_poids_hc(self.dump_couches.as_deref(), "hc_attn",
                                                l, pos, &s);
                    // **Quels coefficients replient l'entrée ?** V4 : ceux du
                    // raccord lui-même. V4.1 (mHC retardé) : ceux PORTÉS par le
                    // raccord précédent, et la copie 0 au tout premier — la
                    // référence fait `layer_input = residual[:, 0] if pre_mix is
                    // None else (pre_mix · residual).sum(1)`.
                    let poids: &[f32] = if retarde {
                        hc_porte.as_deref().unwrap_or(&[])
                    } else { &s.pre };
                    if poids.is_empty() { xin.copy_from_slice(&x[..h]); }
                    else { Hc::melanger(&x, poids, ha.hc, h, &mut xin); }
                    hc_attn = Some(s);
                }
                None => xin.copy_from_slice(&x),
            }
            Self::vider_couche(self.dump_couches.as_deref(), "hc_attn_pre", l, pos, &xin);
            let tm = Instant::now();
            Self::rmsnorm(&xin, &lay.attn_norm, cfg.eps, &mut hn);
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
            if let Some(m4) = self.mla4.as_ref().map(|v| &v[l]) {
                // Attention V4 : une tête latente, valeurs = clés, sortie
                // groupée. `att` fait `nh × head_dim` — la même taille que le
                // chemin dense quand `key_length` est déclaré.
                // `hn` et non `xin` : l'attention reçoit l'entrée MÉLANGÉE puis
                // NORMÉE (`hc_attn_pre` → `attn_norm`), comme les deux autres
                // chemins. Passer `xin` donnait une corrélation de 0,9986 —
                // « presque juste », le pire des écarts parce qu'il ne se voit
                // pas sur un coup d'œil.
                // **V4.1 : le cache compressé est PARTAGÉ.** Les compresseurs et
                // les caches de clés compressées ne vivent que sur les couches
                // SOURCES (`kv_source_layer_ids`) ; les suivantes « reuse the
                // most recently published source below them » (vLLM,
                // `deepseek_v41/attention.py`). On ne recopie donc pas l'état :
                // on indexe les tampons de la SOURCE, qui a déjà été calculée
                // pour ce jeton (sa couche est en dessous). Recopier donnerait un
                // cache par couche, donc d'AUTRES clés — faux, et muet.
                let src = m4.comp_source;
                let mut etat = EtatV4 {
                    cles: &mut self.mla4_cache[l],
                    comp_kv: &mut self.mla4_comp_kv[src],
                    comp_gate: &mut self.mla4_comp_gate[src],
                    cles_comp: &mut self.mla4_cles_comp[src],
                    idx_kv: &mut self.mla4_idx_kv[l],
                    idx_gate: &mut self.mla4_idx_gate[l],
                    // Les clés de l'indexeur sont, elles aussi, celles de la
                    // SOURCE (`owns_k` côté vLLM) : une couche qui note les blocs
                    // le fait avec SA requête, mais sur les mêmes clés.
                    idx_cles: &mut self.mla4_idx_cles[src],
                    idx_scores: &mut self.mla4_idx_scores[l],
                };
                Self::attn_v4(m4, &mut etat, &hn, pos, &mut att,
                              &mut paires[0], self.dump_couches.as_deref(), l,
                              pool.threads());
            } else if let Some(m) = self.mla.as_ref().map(|v| &v[l]) {
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
            // L'attention V4 a DÉJÀ projeté sa sortie (`attn_v4` applique
            // `attn_output_a` par groupe puis `attn_output_b`) : il n'y a pas de
            // `attn_output.weight` à charger, et refaire une projection ici
            // multiplierait la sortie par une matrice vide.
            if self.mla4.is_some() {
                o[..h].copy_from_slice(&att[..h]);
            } else {
                let n_att = match self.mla.as_ref().map(|v| &v[l]) {
                    Some(m) => m.nh * m.vd,
                    None => att.len(),
                };
                Self::matvec(pool, &lay.wo, &att[..n_att.min(att.len())], &mut o, events, &mut paires[0], self.act_levels, self.act_thresh, tk(3), self.act_renorm, &mut scratch, self.seuil_push);
            }
            // Hyper-connexions : `o` reste la SORTIE PURE de l'attention ; ce
            // sont les copies qui se rechargent (`comb`), et l'entrée de la FFN
            // est le mélange de ces copies — jamais `o`.
            let mut hc_x: Option<Vec<f32>> = None;
            let mut hc_ffn: Option<HcSortie> = None;
            match (hc_l, hc_attn.as_ref()) {
                (Some((_, hf)), Some(sa)) => {
                    let mut nx = vec![0f32; hf.hc * h];
                    Hc::retro(&o, &x, sa, hf.hc, h, &mut nx);
                    let sf = hf.sortie(&nx);
                    Self::vider_couche_poids_hc(self.dump_couches.as_deref(), "hc_ffn",
                                                l, pos, &sf);
                    let mut mel = vec![0f32; h];
                    // Le flux que voit le raccord FFN : c'est sur LUI que la
                    // référence calcule ses mélanges (`mixes = fn · rms_norm(x)`),
                    // et c'est ce que la vérification indépendante relit.
                    Self::vider_couche(self.dump_couches.as_deref(), "hc_ffn_in", l, pos, &nx);
                    // Idem pour la FFN : V4.1 la replie avec la `pre` de
                    // l'ATTENTION courante (« the FFN uses this layer's attention
                    // pre-mix »), et sa propre `pre` part au raccord suivant.
                    let poids: &[f32] = if retarde { &sa.pre } else { &sf.pre };
                    Hc::melanger(&nx, poids, hf.hc, h, &mut mel);
                    if self.hc_retarde {
                        // **Le maillon central de la chaîne retardée** : l'entrée de
                        // la FFN se replie avec la `pre` de l'ATTENTION. Aucune des
                        // trois égalités de `verifier_v41_mhc.py` ne le couvrait
                        // (elles lisent `l_last`, qui est en aval) : échanger
                        // `sa.pre` contre `sf.pre` ici passait inaperçu. Ces deux
                        // vides le rendent vérifiable — les coefficients employés
                        // ET le repliement qu'ils produisent.
                        Self::vider_couche(self.dump_couches.as_deref(), "hc_pre_attn",
                                           l, pos, &sa.pre);
                        Self::vider_couche(self.dump_couches.as_deref(), "hc_mel_ffn",
                                           l, pos, &mel);
                    }
                    Self::rmsnorm(&mel, &lay.ffn_norm, cfg.eps, &mut hn);
                    // L'entrée NORMÉE du MoE : sans elle, un vérificateur
                    // indépendant ne peut pas rejouer le routeur et les experts
                    // depuis les vides (`hc_mel_ffn` est AVANT la norme).
                    Self::vider_couche(self.dump_couches.as_deref(), "ffn_hn", l, pos, &hn);
                    if self.hc_retarde {
                        // Ce que la chaîne retarde : la `pre` de CE raccord FFN
                        // part au raccord suivant. La vider permet de vérifier la
                        // réduction finale contre la référence sans rejouer la
                        // couche (et c'est le seul endroit où elle existe).
                        Self::vider_couche(self.dump_couches.as_deref(), "hc_ffn_pre",
                                           l, pos, &sf.pre);
                        hc_porte = Some(sf.pre.clone());
                    }
                    hc_x = Some(nx);
                    hc_ffn = Some(sf);
                }
                _ => {
                    for i in 0..h { o[i] += x[i]; }
                    Self::rmsnorm(&o, &lay.ffn_norm, cfg.eps, &mut hn);
                }
            }
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
                    // Cache RAM : si l'expert y est, on lit SES octets (base
                    // redirigée, loc = 0) au lieu du mmap ; sinon on lit le
                    // mmap comme avant, puis on le recopie.
                    let (vg, loc_g) = Self::resident(&mut self.cache_ram, 0, l, e as usize,
                                                     &moe.gate[kexp], loc);
                    Self::matvec4_ou_iq(pool, &vg, loc_g, &hn, &mut gate, &mut paires[1],
                                        self.act_levels,
                                        self.act_thresh, tk(4), self.act_renorm, &mut scratch,
                                        moe.biais_gate.as_ref().map(|b| &b[e as usize * moe.n_ff..]),
                                        threads_iq);
                    let mu = moe.up[kexp].expert(loc);
                    let (vu, loc_u) = Self::resident(&mut self.cache_ram, 1, l, e as usize,
                                                     &moe.up[kexp], loc);
                    Self::matvec4_ou_iq(pool, &vu, loc_u, &hn, &mut up, &mut paires[1],
                                        self.act_levels,
                                        self.act_thresh, tk(5), self.act_renorm, &mut scratch,
                                        moe.biais_up.as_ref().map(|b| &b[e as usize * moe.n_ff..]),
                                        threads_iq);
                    Self::activation(&mut gate, &up, cfg.ffn_exp, cfg.ffn_act_oss,
                                     limite(l, false));
                    Self::compter_neurones(&mut self.profil_neurones, largeur_profil,
                                           l, &gate[..cfg.ffn_exp]);
                    let md = moe.down[kexp].expert(loc);
                    let (vd, loc_d) = Self::resident(&mut self.cache_ram, 2, l, e as usize,
                                                     &moe.down[kexp], loc);
                    Self::matvec4_ou_iq(pool, &vd, loc_d, &gate, &mut exp_out, &mut paires[1],
                                    self.act_levels, self.act_thresh, tk(6), self.act_renorm, &mut scratch,
                                    // Le biais de descente se découpe par la
                                    // largeur de SORTIE (h), pas par n_ff : les
                                    // deux coïncident sur gpt-oss (2 880) mais
                                    // pas sur Qwen3-MoE (768 contre 2 048).
                                    moe.biais_down.as_ref().map(|b| &b[e as usize * h..]),
                                    threads_iq);
                    for i in 0..h { down[i] += w_exp * exp_out[i]; }
                }
                // La somme des experts ROUTÉS, avant l'expert partagé : c'est le
                // seul vide qui manquait pour vérifier la composition du chemin
                // des experts (routeur ✓ vérifié, mais experts jamais comparés).
                Self::vider_couche(self.dump_couches.as_deref(), "moe_down", l, pos, &down);
                if let Some((sg, su, sd)) = moe.shexp.as_ref() {
                    Self::matvec4_ou_iq(pool, sg, 0, &hn, &mut gate, &mut paires[2], self.act_levels,
                                    self.act_thresh, tk(4), self.act_renorm, &mut scratch, None,
                                    threads_iq);
                    Self::matvec4_ou_iq(pool, su, 0, &hn, &mut up, &mut paires[2], self.act_levels,
                                    self.act_thresh, tk(5), self.act_renorm, &mut scratch, None,
                                    threads_iq);
                    Self::activation(&mut gate, &up, cfg.ffn_exp, cfg.ffn_act_oss,
                                     limite(l, true));
                    Self::matvec4_ou_iq(pool, sd, 0, &gate, &mut exp_out, &mut paires[2], self.act_levels,
                                    self.act_thresh, tk(6), self.act_renorm, &mut scratch, None,
                                    threads_iq);
                    for i in 0..h { down[i] += exp_out[i]; }
                }
                if let Some((gl, gg)) = self.ffn_gain {
                    if gl == l { for v in down.iter_mut() { *v *= gg; } }
                }
                match (hc_x.as_ref(), hc_ffn.as_ref(), hc_l) {
                    (Some(nx), Some(sf), Some((_, hf))) => {
                        let mut suite = vec![0f32; hf.hc * h];
                        Hc::retro(&down, nx, sf, hf.hc, h, &mut suite);
                        x = suite;
                    }
                    _ => for i in 0..h { x[i] = o[i] + down[i]; },
                }
                Self::vider_couche(self.dump_couches.as_deref(), "l_last", l, pos, &x);
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
            Self::activation(&mut gate, &up, cfg.ffn, cfg.ffn_act_oss, 0.0);
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
            match (hc_x.as_ref(), hc_ffn.as_ref(), hc_l) {
                (Some(nx), Some(sf), Some((_, hf))) => {
                    let mut suite = vec![0f32; hf.hc * h];
                    Hc::retro(&down, nx, sf, hf.hc, h, &mut suite);
                    x = suite;
                }
                _ => for i in 0..h { x[i] = o[i] + down[i]; },
            }
            Self::vider_couche(self.dump_couches.as_deref(), "l_last", l, pos, &x);
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
        // **Coupure de grappe** : on rend le flux résiduel BRUT, tel qu'il est —
        // et pour un modèle à hyper-connexions, cela veut dire les `hc` copies,
        // PAS leur réduction. Réduire ici puis ré-étendre à l'arrivée change le
        // modèle : mesuré, la perplexité répartie passait de 8 311 à 34 159
        // (écart 3,11) alors que le transport dense est exact. Le flux d'un
        // modèle à hyper-connexions coûte donc `hc` fois plus cher sur le fil.
        if self.flux_brut || (self.couche_fin < cfg.n_layer && !self.tete_partielle) {
            // **La `pre` portée part avec le flux** (protocole v6) : c'est ce qui
            // permet au nœud suivant d'amorcer sa chaîne retardée sur la bonne
            // valeur au lieu de la copie 0. 16 octets par jeton, sur les 65 615
            // que coûte déjà un état en `hc` copies — 0,02 %.
            if self.hc_retarde { self.hc_porte_flux = hc_porte.clone(); }
            return x;                       // nœud intermédiaire : flux brut
        }
        // Mélange de TÊTE : les `hc` copies redeviennent un seul état, qui voit
        // ensuite la norme finale puis les logits (`build_hc_head`).
        if let Some(ht) = self.hc_tete.as_ref() {
            x = ht.tete(&x);
        } else if self.hc_retarde {
            // **V4.1 n'a pas de tête apprise.** La référence replie le flux
            // final avec la `pre` de la DERNIÈRE FFN, celle qui a été calculée
            // sur le flux d'avant son `post` puis portée jusqu'ici :
            // `hc_collapse_triton(hidden_states, pre_mix)` puis `self.norm`.
            // La calculer ici n'est pas une convention du moteur : c'est la
            // seule chaîne que le fichier permet (pas de `output_hc_*`).
            match (hc_porte.as_deref(), tete_copie0) {
                (_, true) => {
                    let (hc, hh) = self.hc.as_ref()
                        .map(|v| (v[0].0.hc, v[0].0.h)).expect("`hc_retarde` sans hyper-connexions");
                    let mut replie = vec![0f32; h];
                    Hc::melanger(&x, &{
                        let mut p = vec![0f32; hc]; p[0] = 1.0; p
                    }, hc, hh, &mut replie);
                    x = replie;
                    let _ = hh;
                }
                (Some(pm), false) => {
                    let (hc, hh) = self.hc.as_ref()
                        .map(|v| (v[0].0.hc, v[0].0.h))
                        .expect("`hc_retarde` sans hyper-connexions chargées");
                    let mut replie = vec![0f32; h];
                    Hc::melanger(&x, pm, hc, hh, &mut replie);
                    x = replie;
                }
                (None, false) => panic!("V4.1 : flux final en `hc` copies sans `pre` portée — \
le dernier raccord FFN n'a pas été exécuté (plage de couches vide ?)"),
            }
        }
        Self::rmsnorm(&x, out_norm, cfg.eps, &mut hn);
        // L'état qui entre dans la tête de sortie : la dernière chose que la
        // chaîne retardée produit, donc ce qu'une vérification indépendante
        // recalcule à partir de `l_last` et de `hc_ffn_pre`.
        Self::vider_couche(self.dump_couches.as_deref(), "hidden_final", 0, pos, &hn);
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
    ///
    /// `&mut self` parce que la réduction CONSOMME la `pre` reçue du pair
    /// (V4.1) : elle appartient à ce flux-là et à lui seul. La laisser en place
    /// faisait reprendre la chaîne du jeton SUIVANT sur les coefficients du
    /// précédent — mesuré, `--ppl-reparti` rendait 514 722,06 au lieu de
    /// 1 743 713,62, la position 0 exacte au bit près et les suivantes fausses,
    /// sans un mot.
    /// `pos` ne sert QU'AUX VIDES : `hidden_final` (le vide de la passe
    /// complète) porte déjà cette quantité, et vider ici la même chose sous le
    /// nom `reduit` rend la réduction finale vérifiable TENSEUR PAR TENSEUR — ce
    /// qu'aucun vide ne permettait (relevé par la relecture adverse : la
    /// réduction n'était couverte que par l'égalité de perplexité).
    pub fn norme_finale(&mut self, x: &[f32], pos: usize) -> Vec<f32> {
        // **La `pre` reçue est prise ICI, avant toute branche** : une réduction
        // finale a lieu une fois par flux, et la `pre` appartient à ce flux-là.
        // La prendre dans la seule branche `hc_retarde` laissait le champ en
        // place pour les autres chemins (état de largeur `hidden`, modèle à
        // `hc_tete`) — et le `forward` suivant, s'il reprenait au milieu du
        // modèle, l'aurait consommée (relevé par la relecture adverse : les deux
        // branches étaient inatteignables aujourd'hui, mais « impossible par
        // construction » ne se démontre pas avec un `take()` conditionnel).
        let pre_recue = self.hc_porte_imposee.take();
        // Un état venu d'un autre nœud peut être en `hc` copies (modèle à
        // hyper-connexions) : c'est ICI que la réduction a lieu, une fois, sur
        // le nœud qui possède la tête — comme la norme finale.
        let reduit;
        let x = if x.len() > self.cfg.hidden {
            match self.hc_tete.as_ref() {
                Some(ht) => { reduit = ht.tete(x); &reduit[..] }
                // **V4.1 par le fil : impossible en l'état.** Sa réduction finale
                // n'est pas apprise, elle est la `pre` de la dernière FFN — un
                // vecteur de `hc` valeurs par jeton que le protocole DRVF ne
                // transporte PAS. Normer les `hc·h` valeurs telles quelles
                // reviendrait à normer la seule copie 0 : un état faux, sans un
                // mot. Refuser est la seule sortie honnête tant que le flux n'a
                // pas un champ pour cette `pre` (16 octets par jeton).
                // **La `pre` reçue du pair (protocole v6)** : la réduction finale
                // de V4.1 n'est pas apprise, c'est la `pre` du dernier raccord FFN
                // exécuté — celui du pair, qui la transporte. Un flux v5 ou un
                // émetteur qui ne l'envoie pas : refus, pas de repli muet.
                None if self.hc_retarde => match pre_recue {
                    Some(pm) => {
                        let (hc, h) = self.hc.as_ref()
                            .map(|v| (v[0].0.hc, v[0].0.h)).expect("`hc_retarde` sans HC");
                        let mut replie = vec![0f32; h];
                        Hc::melanger(x, &pm, hc, h, &mut replie);
                        reduit = replie;
                        &reduit[..]
                    }
                    None => panic!("V4.1 : un état en `hc` copies venu d'un autre nœud ne \
porte pas la `pre` de la dernière FFN (protocole < v6 ?), et sa réduction finale n'est \
pas apprise — le flux doit transporter ces {} valeurs par jeton",
                        self.hc.as_ref().map(|v| v[0].0.hc).unwrap_or(0)),
                },
                None => x,
            }
        } else { x };
        let mut hn = vec![0f32; self.cfg.hidden];
        Self::rmsnorm(x, &self.out_norm, self.cfg.eps, &mut hn);
        // Le même état que `hidden_final` sur un nœud qui a tout calculé : c'est
        // ce qui rend la RÉDUCTION FINALE comparable d'un côté à l'autre.
        Self::vider_couche(self.dump_couches.as_deref(), "reduit", 0, pos, &hn);
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
        for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { qx[i as usize] = v.clamp(-32767, 32767) as i16; }
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
        for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { qx[i as usize] = v.clamp(-32767, 32767) as i16; }
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
mod tests_hc {
    //! Les hyper-connexions de DeepSeek-V4, comparées à une **seconde**
    //! implémentation : `tools/hc_synthetique.py` recopie les opérations ggml de
    //! `llama.cpp/src/models/deepseek4.cpp` en numpy. Les mêmes formules écrites
    //! deux fois dans deux langages : un écart se voit.
    //!
    //! Les valeurs ci-dessous sont GÉNÉRÉES (`python3 tools/hc_synthetique.py`) ;
    //! ne pas les retoucher à la main. Dimensions minuscules (`hc = 4`, `h = 3`)
    //! et poids entiers pour que le test se relise sans calculatrice.
    use super::*;

    const MELANGE: [f32; 288] = [
        2.000000000e+00, -2.000000000e+00, -2.000000000e+00, -2.000000000e+00, -1.000000000e+00, -1.000000000e+00, -1.000000000e+00, 1.000000000e+00,
        -1.000000000e+00, 2.000000000e+00, -2.000000000e+00, 1.000000000e+00, 1.000000000e+00, 0.000000000e+00, 0.000000000e+00, 0.000000000e+00,
        2.000000000e+00, 2.000000000e+00, -2.000000000e+00, -1.000000000e+00, -2.000000000e+00, 0.000000000e+00, 2.000000000e+00, 1.000000000e+00,
        -2.000000000e+00, 2.000000000e+00, 2.000000000e+00, 1.000000000e+00, 2.000000000e+00, 0.000000000e+00, -1.000000000e+00, 1.000000000e+00,
        1.000000000e+00, 0.000000000e+00, 2.000000000e+00, -1.000000000e+00, 0.000000000e+00, -1.000000000e+00, 0.000000000e+00, 2.000000000e+00,
        -2.000000000e+00, -2.000000000e+00, 0.000000000e+00, 2.000000000e+00, 0.000000000e+00, -2.000000000e+00, -1.000000000e+00, -2.000000000e+00,
        -2.000000000e+00, 2.000000000e+00, -2.000000000e+00, 1.000000000e+00, -2.000000000e+00, -2.000000000e+00, -2.000000000e+00, 2.000000000e+00,
        -1.000000000e+00, 0.000000000e+00, 1.000000000e+00, 1.000000000e+00, 0.000000000e+00, 1.000000000e+00, -2.000000000e+00, -1.000000000e+00,
        0.000000000e+00, -2.000000000e+00, 1.000000000e+00, -1.000000000e+00, -2.000000000e+00, 1.000000000e+00, -1.000000000e+00, -2.000000000e+00,
        1.000000000e+00, 2.000000000e+00, 2.000000000e+00, -1.000000000e+00, -1.000000000e+00, -2.000000000e+00, 2.000000000e+00, 2.000000000e+00,
        -1.000000000e+00, 0.000000000e+00, 0.000000000e+00, -2.000000000e+00, -1.000000000e+00, 2.000000000e+00, 0.000000000e+00, 1.000000000e+00,
        2.000000000e+00, 0.000000000e+00, -2.000000000e+00, 1.000000000e+00, -2.000000000e+00, -1.000000000e+00, 1.000000000e+00, -1.000000000e+00,
        -2.000000000e+00, 0.000000000e+00, -2.000000000e+00, 0.000000000e+00, -1.000000000e+00, 2.000000000e+00, 0.000000000e+00, 1.000000000e+00,
        0.000000000e+00, 1.000000000e+00, -2.000000000e+00, -1.000000000e+00, 0.000000000e+00, 2.000000000e+00, -2.000000000e+00, 2.000000000e+00,
        2.000000000e+00, -2.000000000e+00, 1.000000000e+00, -2.000000000e+00, -1.000000000e+00, -2.000000000e+00, 0.000000000e+00, -1.000000000e+00,
        1.000000000e+00, 0.000000000e+00, 1.000000000e+00, 1.000000000e+00, 1.000000000e+00, -2.000000000e+00, 2.000000000e+00, 1.000000000e+00,
        -2.000000000e+00, 2.000000000e+00, 2.000000000e+00, 0.000000000e+00, -2.000000000e+00, -1.000000000e+00, 0.000000000e+00, 2.000000000e+00,
        0.000000000e+00, -1.000000000e+00, -1.000000000e+00, -1.000000000e+00, 2.000000000e+00, -2.000000000e+00, 0.000000000e+00, 0.000000000e+00,
        2.000000000e+00, -2.000000000e+00, -1.000000000e+00, -1.000000000e+00, 2.000000000e+00, 2.000000000e+00, 1.000000000e+00, -1.000000000e+00,
        -1.000000000e+00, -2.000000000e+00, -1.000000000e+00, -1.000000000e+00, -2.000000000e+00, -1.000000000e+00, -2.000000000e+00, 0.000000000e+00,
        2.000000000e+00, 1.000000000e+00, 2.000000000e+00, 0.000000000e+00, 2.000000000e+00, 1.000000000e+00, -2.000000000e+00, -2.000000000e+00,
        1.000000000e+00, 0.000000000e+00, 0.000000000e+00, -2.000000000e+00, -2.000000000e+00, 0.000000000e+00, -1.000000000e+00, 2.000000000e+00,
        1.000000000e+00, -1.000000000e+00, 2.000000000e+00, 1.000000000e+00, -2.000000000e+00, 0.000000000e+00, -2.000000000e+00, 2.000000000e+00,
        0.000000000e+00, 1.000000000e+00, 0.000000000e+00, 1.000000000e+00, 1.000000000e+00, 1.000000000e+00, 2.000000000e+00, -2.000000000e+00,
        -1.000000000e+00, 2.000000000e+00, -1.000000000e+00, 2.000000000e+00, 2.000000000e+00, -1.000000000e+00, 0.000000000e+00, 1.000000000e+00,
        0.000000000e+00, -1.000000000e+00, 2.000000000e+00, -1.000000000e+00, -1.000000000e+00, 2.000000000e+00, 2.000000000e+00, 1.000000000e+00,
        -2.000000000e+00, -1.000000000e+00, 0.000000000e+00, -2.000000000e+00, 0.000000000e+00, 2.000000000e+00, 2.000000000e+00, 2.000000000e+00,
        -1.000000000e+00, -1.000000000e+00, -1.000000000e+00, -1.000000000e+00, -2.000000000e+00, -1.000000000e+00, 1.000000000e+00, 1.000000000e+00,
        1.000000000e+00, -2.000000000e+00, 1.000000000e+00, -1.000000000e+00, 0.000000000e+00, 0.000000000e+00, 2.000000000e+00, 0.000000000e+00,
        0.000000000e+00, -1.000000000e+00, 0.000000000e+00, 0.000000000e+00, 1.000000000e+00, -1.000000000e+00, 2.000000000e+00, -2.000000000e+00,
        -2.000000000e+00, -2.000000000e+00, 2.000000000e+00, 0.000000000e+00, 0.000000000e+00, 0.000000000e+00, 1.000000000e+00, -1.000000000e+00,
        0.000000000e+00, 0.000000000e+00, 1.000000000e+00, 2.000000000e+00, 0.000000000e+00, -1.000000000e+00, -2.000000000e+00, -1.000000000e+00,
        0.000000000e+00, 2.000000000e+00, 1.000000000e+00, 1.000000000e+00, -2.000000000e+00, 0.000000000e+00, 2.000000000e+00, 0.000000000e+00,
        -1.000000000e+00, 2.000000000e+00, 1.000000000e+00, 0.000000000e+00, 1.000000000e+00, 2.000000000e+00, 2.000000000e+00, -1.000000000e+00,
        1.000000000e+00, 1.000000000e+00, 0.000000000e+00, 2.000000000e+00, -2.000000000e+00, 1.000000000e+00, -2.000000000e+00, -2.000000000e+00,
        1.000000000e+00, 0.000000000e+00, -2.000000000e+00, -1.000000000e+00, -2.000000000e+00, 0.000000000e+00, 0.000000000e+00, 1.000000000e+00,
    ];
    const BASE: [f32; 24] = [
        1.000000000e+00, 0.000000000e+00, 0.000000000e+00, 0.000000000e+00, -1.000000000e+00, 1.000000000e+00, -1.000000000e+00, -1.000000000e+00,
        -1.000000000e+00, 1.000000000e+00, -1.000000000e+00, 1.000000000e+00, 0.000000000e+00, -1.000000000e+00, 1.000000000e+00, 0.000000000e+00,
        -1.000000000e+00, 0.000000000e+00, 1.000000000e+00, 1.000000000e+00, -1.000000000e+00, 1.000000000e+00, 0.000000000e+00, 0.000000000e+00,
    ];
    const SCALE: [f32; 3] = [
        5.000000000e-01, 1.500000000e+00, 2.000000000e+00,
    ];
    const X: [f32; 12] = [
        -2.000000000e+00, 0.000000000e+00, -1.000000000e+00, 2.000000000e+00, -2.000000000e+00, -2.000000000e+00, 1.000000000e+00, 1.000000000e+00,
        -1.000000000e+00, 2.000000000e+00, 1.000000000e+00, 2.000000000e+00,
    ];
    const Y: [f32; 3] = [
        -1.000000000e+00, 2.000000000e+00, -1.000000000e+00,
    ];
    const PRE: [f32; 4] = [
        8.770634053e-01, 9.522664260e-02, 4.202786396e-01, 8.331579935e-01,
    ];
    const POST: [f32; 4] = [
        1.999999977e+00, 1.960112879e+00, 9.824524421e-01, 1.013996532e-01,
    ];
    const COMB: [f32; 16] = [
        1.337415487e-05, 2.076609642e-06, 9.989694829e-01, 2.014161513e-05, 1.287439464e-06, 9.038835995e-07, 9.279701907e-05, 9.990398264e-01,
        1.625873293e-06, 9.922175094e-01, 1.347101468e-06, 1.176386955e-06, 9.999827027e-01, 7.778517899e-03, 9.353739472e-04, 9.378564322e-04,
    ];
    const ENTREE: [f32; 3] = [
        5.229211011e-01, 1.062983348e+00, 1.785206568e-01,
    ];
    const SORTIE: [f32; 12] = [
        -5.711946950e-05, 4.999981709e+00, -5.214681907e-05, -9.523406790e-01, 4.920219977e+00, -2.936777237e+00, -2.978333719e+00, 1.965656011e+00,
        -1.979738118e+00, 1.898516606e+00, -1.794341314e+00, -2.097624911e+00,
    ];

    fn proche(a: &[f32], b: &[f32], tol: f32, quoi: &str) {
        assert_eq!(a.len(), b.len(), "{quoi} : longueurs {} contre {}", a.len(), b.len());
        for (i, (x, y)) in a.iter().zip(b.iter()).enumerate() {
            assert!((x - y).abs() <= tol,
                    "{quoi}[{i}] : {x:e} contre {y:e} (écart {:e})", (x - y).abs());
        }
    }

    /// `Sinkhorn` rend la matrice de connexions **doublement stochastique** :
    /// c'est ce qui autorise à lire `comb` comme un routage et non comme des
    /// poids arbitraires — et c'est la première chose à vérifier, avant même la
    /// comparaison à la référence.
    #[test]
    fn sinkhorn_rend_les_connexions_doubles() {
        let mut c = vec![0.7f32, -0.3, 1.2, 0.0, -1.1, 0.4, 0.2, 0.9,
                         0.05, -2.0, 0.3, 1.7, 0.6, 0.1, -0.8, 0.25];
        sinkhorn(&mut c, 4, 20, 1e-6);
        for d in 0..4 {
            let s: f32 = (0..4).map(|src| c[d + src * 4]).sum();
            assert!((s - 1.0).abs() < 1e-4, "somme des sources de la destination {d} = {s}");
        }
    }

    /// La sortie complète : `pre`, `post`, `comb`, l'entrée mélangée et les
    /// quatre copies de sortie, contre la référence numpy.
    #[test]
    fn hyper_connexions_conforme_a_la_reference() {
        let hc = Hc { melange: MELANGE.to_vec(), base: BASE.to_vec(),
                      scale: SCALE.to_vec(), hc: 4, h: 3, iters: 20, eps: 1e-6 };
        let s = hc.sortie(&X);
        proche(&s.pre, &PRE, 1e-6, "pre");
        proche(&s.post, &POST, 1e-6, "post");
        proche(&s.comb, &COMB, 1e-6, "comb");

        let mut entree = vec![0f32; 3];
        Hc::melanger(&X, &s.pre, 4, 3, &mut entree);
        proche(&entree, &ENTREE, 1e-6, "entrée mélangée");

        let mut sortie = vec![0f32; 12];
        Hc::retro(&Y, &X, &s, 4, 3, &mut sortie);
        proche(&sortie, &SORTIE, 1e-6, "copies de sortie");
    }

    /// **La rotation doit être réversible**, dans les deux conventions et pour
    /// toutes les bases : `rope_norm(forward)` puis `rope_norm(inverse)` doit
    /// redonner le vecteur d'origine. C'est l'invariant qui manquait le 02/10 :
    /// la dé-rotation d'une couche compressée utilisait la base des couches
    /// brutes, et 64 dimensions sur 512 étaient fausses de 10 % pendant que les
    /// 448 autres restaient justes à 0,4 % — une corrélation de 0,996, donc
    /// « plausible ». Un test de 6 lignes l'aurait dit.
    #[test]
    fn rotation_reversible_dans_les_deux_conventions() {
        for base in [10_000.0f32, 160_000.0] {
            for pos in [0usize, 1, 3, 37, 131] {
                let origine: Vec<f32> = (0..64).map(|i| ((i * 7 % 13) as f32) - 6.0).collect();
                let mut v = origine.clone();
                Model::rope_norm(&mut v, 2, 32, pos, base, 32, false);
                // À la position 0 la rotation est l'IDENTITÉ (angle nul) : c'est
                // précisément pour ça que le bug de base ne se voyait pas à la
                // position 0 et apparaissait à la position 1.
                assert_eq!(v != origine, pos > 0,
                           "rotation identité attendue à la position 0 (pos {pos}, base {base})");
                Model::rope_norm(&mut v, 2, 32, pos, base, 32, true);
                for (a, b) in v.iter().zip(origine.iter()) {
                    assert!((a - b).abs() < 1e-4,
                            "aller-retour rope_norm : {a} contre {b} (pos {pos}, base {base})");
                }
            }
        }
    }

    /// **`rope_norm_yarn` contre la transcription de ggml** (témoin calculé par
    /// `tools/rope_yarn_temoin.py`) : mêmes corr_dims, même rampe, même
    /// appariement NORM. Sans ce témoin, une erreur d'orientation de rampe ou de
    /// dimensions de correction ne se voit que sur un modèle de 284 Go.
    /// Diagnostic : imprime la sortie pour les paramètres RÉELS de V4-Flash
    /// (n_rot = 64, position 4), à comparer avec la même chose en Python.
    #[test]
    fn diagnostic_yarn_v4flash() {
        let mut v = [1.0f32; 64];
        for (i, x) in v.iter_mut().enumerate() { *x = (i as f32) * 0.1 - 3.0; }
        Model::rope_norm_yarn(&mut v, 1, 64, 4, 160_000.0, 16.0, 32.0, 1.0, 65536.0, 64, false);
        eprintln!("RUST {:?}", &v[..8]);
    }

    #[test]
    fn yarn_du_compresseur_conforme_a_ggml() {
        let mut v = [0.5f32, -1.25, 2.0, 0.75, -0.5, 1.5, -2.0, 0.25];
        Model::rope_norm_yarn(&mut v, 1, 8, 124, 160_000.0, 16.0, 32.0, 1.0, 65536.0, 8, false);
        let attendu = [-1.290996836e+00f32, -3.818732377e-01, 2.055401246e+00, 5.812277671e-01,
                       -8.059601869e-01, 1.360304443e+00, -2.001419332e+00, 2.383708423e-01];
        for (i, (a, b)) in v.iter().zip(attendu.iter()).enumerate() {
            assert!((a - b).abs() < 1e-6, "valeur {i} : {a:e} contre {b:e}");
        }
    }

    /// **Le softmax du compresseur est PAR CANAL, pas par jeton.** C'est la
    /// seule chose que la vérification sur le vrai modèle ne pouvait pas prouver
    /// (l'état injecté y était identique à toutes les positions, donc le pool
    /// était insensible aux poids). Témoin à la main, deux jetons DIFFÉRENTS :
    ///
    /// ```text
    /// largeur 2, groupe de 2 jetons
    /// valeurs = [ 1, 10 | 3, 4 ]      portes = [ 0, 0 | 0, ln 3 ]
    /// canal 0 : poids (0,5 ; 0,5)      → 0,5·1 + 0,5·3 = 2,0
    /// canal 1 : poids (1/4 ; 3/4)      → 0,25·10 + 0,75·4 = 5,5
    /// ```
    ///
    /// Un softmax par jeton (sur les canaux) puis une moyenne donnerait 4,625 :
    /// la valeur témoin l'exclut.
    #[test]
    fn pool_du_compresseur_est_par_canal() {
        let valeurs = [1.0f32, 10.0, 3.0, 4.0];
        let portes = [0.0f32, 0.0, 0.0, 3.0f32.ln()];
        let p0 = Model::pool_groupe(&valeurs, Some(&portes), 2, 2, 0, 0);
        let p1 = Model::pool_groupe(&valeurs, Some(&portes), 2, 2, 0, 1);
        assert!((p0 - 2.0).abs() < 1e-6, "canal 0 : {p0} au lieu de 2,0");
        assert!((p1 - 5.5).abs() < 1e-6, "canal 1 : {p1} au lieu de 5,5");
        // Sans porte (V4.1 en ratio 1) : la valeur passe telle quelle, et `base`
        // décale bien le jeton lu (le groupe d'un seul jeton est le jeton même).
        let p2 = Model::pool_groupe(&valeurs, None, 2, 1, 2, 1);
        assert_eq!(p2, 4.0, "sans porte, `base` doit désigner le jeton");
    }

    /// Le cas dégénéré doit redonner le résidu ordinaire : si `pre` vaut 1 sur
    /// la première copie et 0 ailleurs, `post` vaut 1 partout et `comb` est
    /// l'identité, alors `x ← x + y` — c'est le cas où les hyper-connexions ne
    /// font rien, et il doit être exactement ça.
    #[test]
    fn hyper_connexions_degenere_egale_le_residu() {
        let hc = 4usize; let h = 2usize;
        let x = vec![1.0f32, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0];
        let y = vec![0.5f32, -0.5];
        let mut s = HcSortie { pre: vec![1.0, 0.0, 0.0, 0.0], post: vec![1.0; 4],
                               comb: vec![0.0; 16] };
        for d in 0..hc { s.comb[d + d * hc] = 1.0; }   // identité
        let mut entree = vec![0f32; h];
        Hc::melanger(&x, &s.pre, hc, h, &mut entree);
        assert_eq!(entree, vec![1.0, 2.0]);
        let mut sortie = vec![0f32; hc * h];
        Hc::retro(&y, &x, &s, hc, h, &mut sortie);
        for d in 0..hc {
            assert_eq!(&sortie[d * h..(d + 1) * h], &[x[d * h] + y[0], x[d * h + 1] + y[1]]);
        }
    }
    // ---------------------------------------------------------------------
    // V4.1 : la chaîne mHC **RETARDÉE** (`tools/mhc_v41_synthetique.py`)
    // ---------------------------------------------------------------------
    // Recopiée de `vllm/model_executor/kernels/mhc/torch.py`
    // (`mhc_pre_delayed_torch`, « coefficients from the previous sublayer ») et
    // de `vllm/models/deepseek_v41/nvidia/model.py` : `mhc_shifted_post_pre`
    // (le post d'abord, puis la pre retardée) et la fin de modèle
    // `hc_collapse_triton(hidden_states, pre_mix)` — « v4.1 has no learned
    // hc_head ». Mêmes formules, deux langages, une seule source externe.
    //
    // Ce que le test FIXE : la `pre` d'un raccord sert au raccord SUIVANT, la
    // copie 0 au tout premier, et la tête se replie avec la `pre` de la
    // dernière FFN. Écrite à l'envers (la chaîne de V4), la même entrée donne
    // une tête qui diffère de 67 % — mesuré par le script.
    const MEL_A: [f32; 192] = [2.000000000e+00, -2.000000000e+00, -2.000000000e+00, -2.000000000e+00, -1.000000000e+00, -1.000000000e+00, -1.000000000e+00, 1.000000000e+00, -1.000000000e+00, 2.000000000e+00, -2.000000000e+00, 1.000000000e+00, 1.000000000e+00, 0.000000000e+00, 0.000000000e+00, 0.000000000e+00, 2.000000000e+00, 2.000000000e+00, -2.000000000e+00, -1.000000000e+00, -2.000000000e+00, 0.000000000e+00, 2.000000000e+00, 1.000000000e+00, -2.000000000e+00, 2.000000000e+00, 2.000000000e+00, 1.000000000e+00, 2.000000000e+00, 0.000000000e+00, -1.000000000e+00, 1.000000000e+00, 1.000000000e+00, 0.000000000e+00, 2.000000000e+00, -1.000000000e+00, 0.000000000e+00, -1.000000000e+00, 0.000000000e+00, 2.000000000e+00, -2.000000000e+00, -2.000000000e+00, 0.000000000e+00, 2.000000000e+00, 0.000000000e+00, -2.000000000e+00, -1.000000000e+00, -2.000000000e+00, -2.000000000e+00, 2.000000000e+00, -2.000000000e+00, 1.000000000e+00, -2.000000000e+00, -2.000000000e+00, -2.000000000e+00, 2.000000000e+00, -1.000000000e+00, 0.000000000e+00, 1.000000000e+00, 1.000000000e+00, 0.000000000e+00, 1.000000000e+00, -2.000000000e+00, -1.000000000e+00, 0.000000000e+00, -2.000000000e+00, 1.000000000e+00, -1.000000000e+00, -2.000000000e+00, 1.000000000e+00, -1.000000000e+00, -2.000000000e+00, 1.000000000e+00, 2.000000000e+00, 2.000000000e+00, -1.000000000e+00, -1.000000000e+00, -2.000000000e+00, 2.000000000e+00, 2.000000000e+00, -1.000000000e+00, 0.000000000e+00, 0.000000000e+00, -2.000000000e+00, -1.000000000e+00, 2.000000000e+00, 0.000000000e+00, 1.000000000e+00, 2.000000000e+00, 0.000000000e+00, -2.000000000e+00, 1.000000000e+00, -2.000000000e+00, -1.000000000e+00, 1.000000000e+00, -1.000000000e+00, -2.000000000e+00, 0.000000000e+00, -2.000000000e+00, 0.000000000e+00, -1.000000000e+00, 2.000000000e+00, 0.000000000e+00, 1.000000000e+00, 0.000000000e+00, 1.000000000e+00, -2.000000000e+00, -1.000000000e+00, 0.000000000e+00, 2.000000000e+00, -2.000000000e+00, 2.000000000e+00, 2.000000000e+00, -2.000000000e+00, 1.000000000e+00, -2.000000000e+00, -1.000000000e+00, -2.000000000e+00, 0.000000000e+00, -1.000000000e+00, 1.000000000e+00, 0.000000000e+00, 1.000000000e+00, 1.000000000e+00, 1.000000000e+00, -2.000000000e+00, 2.000000000e+00, 1.000000000e+00, -2.000000000e+00, 2.000000000e+00, 2.000000000e+00, 0.000000000e+00, -2.000000000e+00, -1.000000000e+00, 0.000000000e+00, 2.000000000e+00, 0.000000000e+00, -1.000000000e+00, -1.000000000e+00, -1.000000000e+00, 2.000000000e+00, -2.000000000e+00, 0.000000000e+00, 0.000000000e+00, 2.000000000e+00, -2.000000000e+00, -1.000000000e+00, -1.000000000e+00, 2.000000000e+00, 2.000000000e+00, 1.000000000e+00, -1.000000000e+00, -1.000000000e+00, -2.000000000e+00, -1.000000000e+00, -1.000000000e+00, -2.000000000e+00, -1.000000000e+00, -2.000000000e+00, 0.000000000e+00, 2.000000000e+00, 1.000000000e+00, 2.000000000e+00, 0.000000000e+00, 2.000000000e+00, 1.000000000e+00, -2.000000000e+00, -2.000000000e+00, 1.000000000e+00, 0.000000000e+00, 0.000000000e+00, -2.000000000e+00, -2.000000000e+00, 0.000000000e+00, -1.000000000e+00, 2.000000000e+00, 1.000000000e+00, -1.000000000e+00, 2.000000000e+00, 1.000000000e+00, -2.000000000e+00, 0.000000000e+00, -2.000000000e+00, 2.000000000e+00, 0.000000000e+00, 1.000000000e+00, 0.000000000e+00, 1.000000000e+00, 1.000000000e+00, 1.000000000e+00, 2.000000000e+00, -2.000000000e+00];
    const BASE_A: [f32; 24] = [-2.000000000e+00, 0.000000000e+00, -2.000000000e+00, 2.000000000e+00, 0.000000000e+00, -2.000000000e+00, 0.000000000e+00, 1.000000000e+00, 1.000000000e+00, 1.000000000e+00, 0.000000000e+00, 1.000000000e+00, -1.000000000e+00, 2.000000000e+00, -2.000000000e+00, 0.000000000e+00, 1.000000000e+00, -2.000000000e+00, -2.000000000e+00, -2.000000000e+00, -2.000000000e+00, 1.000000000e+00, 1.000000000e+00, 0.000000000e+00];
    const SCALE_A: [f32; 3] = [5.000000000e-01, 1.500000000e+00, 2.000000000e+00];
    const MEL_F: [f32; 192] = [-1.000000000e+00, 2.000000000e+00, -1.000000000e+00, 2.000000000e+00, 2.000000000e+00, -1.000000000e+00, 0.000000000e+00, 1.000000000e+00, 0.000000000e+00, -1.000000000e+00, 2.000000000e+00, -1.000000000e+00, -1.000000000e+00, 2.000000000e+00, 2.000000000e+00, 1.000000000e+00, -2.000000000e+00, -1.000000000e+00, 0.000000000e+00, -2.000000000e+00, 0.000000000e+00, 2.000000000e+00, 2.000000000e+00, 2.000000000e+00, -1.000000000e+00, -1.000000000e+00, -1.000000000e+00, -1.000000000e+00, -2.000000000e+00, -1.000000000e+00, 1.000000000e+00, 1.000000000e+00, 1.000000000e+00, -2.000000000e+00, 1.000000000e+00, -1.000000000e+00, 0.000000000e+00, 0.000000000e+00, 2.000000000e+00, 0.000000000e+00, 0.000000000e+00, -1.000000000e+00, 0.000000000e+00, 0.000000000e+00, 1.000000000e+00, -1.000000000e+00, 2.000000000e+00, -2.000000000e+00, -2.000000000e+00, -2.000000000e+00, 2.000000000e+00, 0.000000000e+00, 0.000000000e+00, 0.000000000e+00, 1.000000000e+00, -1.000000000e+00, 0.000000000e+00, 0.000000000e+00, 1.000000000e+00, 2.000000000e+00, 0.000000000e+00, -1.000000000e+00, -2.000000000e+00, -1.000000000e+00, 0.000000000e+00, 2.000000000e+00, 1.000000000e+00, 1.000000000e+00, -2.000000000e+00, 0.000000000e+00, 2.000000000e+00, 0.000000000e+00, -1.000000000e+00, 2.000000000e+00, 1.000000000e+00, 0.000000000e+00, 1.000000000e+00, 2.000000000e+00, 2.000000000e+00, -1.000000000e+00, 1.000000000e+00, 1.000000000e+00, 0.000000000e+00, 2.000000000e+00, -2.000000000e+00, 1.000000000e+00, -2.000000000e+00, -2.000000000e+00, 1.000000000e+00, 0.000000000e+00, -2.000000000e+00, -1.000000000e+00, -2.000000000e+00, 0.000000000e+00, 0.000000000e+00, 1.000000000e+00, 1.000000000e+00, 1.000000000e+00, 0.000000000e+00, 1.000000000e+00, -1.000000000e+00, 1.000000000e+00, -1.000000000e+00, -1.000000000e+00, -1.000000000e+00, 1.000000000e+00, -1.000000000e+00, 2.000000000e+00, -1.000000000e+00, -1.000000000e+00, 2.000000000e+00, 0.000000000e+00, -2.000000000e+00, -1.000000000e+00, 2.000000000e+00, 1.000000000e+00, -2.000000000e+00, 1.000000000e+00, 1.000000000e+00, 1.000000000e+00, -2.000000000e+00, 0.000000000e+00, -1.000000000e+00, 2.000000000e+00, -2.000000000e+00, -2.000000000e+00, 1.000000000e+00, 1.000000000e+00, -1.000000000e+00, 2.000000000e+00, 1.000000000e+00, 2.000000000e+00, -1.000000000e+00, 2.000000000e+00, -1.000000000e+00, -1.000000000e+00, -1.000000000e+00, 1.000000000e+00, -1.000000000e+00, -1.000000000e+00, 0.000000000e+00, 1.000000000e+00, 2.000000000e+00, -1.000000000e+00, -1.000000000e+00, -1.000000000e+00, -2.000000000e+00, -1.000000000e+00, 1.000000000e+00, -2.000000000e+00, 1.000000000e+00, 1.000000000e+00, 2.000000000e+00, 2.000000000e+00, 1.000000000e+00, 1.000000000e+00, 1.000000000e+00, -2.000000000e+00, 0.000000000e+00, 1.000000000e+00, 2.000000000e+00, 1.000000000e+00, -1.000000000e+00, 1.000000000e+00, -2.000000000e+00, -2.000000000e+00, -2.000000000e+00, 0.000000000e+00, 0.000000000e+00, -2.000000000e+00, 0.000000000e+00, 1.000000000e+00, 2.000000000e+00, -1.000000000e+00, 0.000000000e+00, 0.000000000e+00, -1.000000000e+00, 2.000000000e+00, 2.000000000e+00, 2.000000000e+00, -2.000000000e+00, 0.000000000e+00, 2.000000000e+00, -1.000000000e+00, 1.000000000e+00, 1.000000000e+00, 2.000000000e+00, 0.000000000e+00, 1.000000000e+00, 2.000000000e+00, 2.000000000e+00, -1.000000000e+00];
    const BASE_F: [f32; 24] = [-2.000000000e+00, -1.000000000e+00, -1.000000000e+00, 1.000000000e+00, 2.000000000e+00, -2.000000000e+00, 2.000000000e+00, 0.000000000e+00, 2.000000000e+00, 1.000000000e+00, -2.000000000e+00, -2.000000000e+00, 0.000000000e+00, 0.000000000e+00, -1.000000000e+00, -1.000000000e+00, 2.000000000e+00, 1.000000000e+00, 1.000000000e+00, 2.000000000e+00, -2.000000000e+00, 0.000000000e+00, 0.000000000e+00, 1.000000000e+00];
    const SCALE_F: [f32; 3] = [1.000000000e+00, 5.000000000e-01, 2.000000000e+00];
    const V0: [f32; 2] = [-2.000000000e+00, -2.000000000e+00];
    const W_A: [f32; 4] = [-2.000000000e+00, -1.000000000e+00, -1.000000000e+00, -2.000000000e+00];
    const W_F: [f32; 4] = [1.000000000e+00, 0.000000000e+00, 1.000000000e+00, -2.000000000e+00];
    const NORME_SORTIE: [f32; 2] = [1.000000000e+00, 2.000000000e+00];
    const PRE_A: [f32; 4] = [7.310595786e-01, 3.775416688e-01, 4.742687318e-02, 3.775416688e-01];
    const PRE_F: [f32; 4] = [7.718183382e-01, 9.919247579e-01, 9.813363965e-01, 8.958005126e-02];
    const ENTREE_A: [f32; 2] = [-2.000000000e+00, -2.000000000e+00];
    const ENTREE_F: [f32; 2] = [6.314459616e+00, 6.314459616e+00];
    const X2: [f32; 8] = [2.208429824e+01, -2.170500619e+00, -1.853952407e-01, -3.501728174e+00, 2.229741982e+01, -2.304406395e+00, 1.408702338e+01, 4.131784184e+00];
    const TETE: [f32; 2] = [1.392811111e+00, -4.902130496e-01];

    fn mat(w: &[f32], x: &[f32], n: usize) -> Vec<f32> {
        (0..n).map(|o| (0..n).map(|i| w[o * n + i] * x[i]).sum()).collect()
    }

    #[test]
    fn chaine_retardee_v41() {
        let (hc, h) = (4usize, 2usize);
        let attn = Hc { melange: MEL_A.to_vec(), base: BASE_A.to_vec(),
                         scale: SCALE_A.to_vec(), hc, h, iters: 20, eps: 1e-6 };
        let ffn = Hc { melange: MEL_F.to_vec(), base: BASE_F.to_vec(),
                        scale: SCALE_F.to_vec(), hc, h, iters: 20, eps: 1e-6 };
        // L'état naît en `hc` copies IDENTIQUES (l'embarquement diffusé).
        let x0: Vec<f32> = (0..hc).flat_map(|_| V0.iter().copied()).collect();
        let sa = attn.sortie(&x0);
        proche(&sa.pre, &PRE_A, 1e-6, "pre de l'attention");
        // 1er raccord : la référence replie avec `residual[:, 0]` — la copie 0,
        // PAS un mélange. La chaîne de V4 replierait avec `sa.pre`.
        let entree_a = x0[..h].to_vec();
        proche(&entree_a, &ENTREE_A, 1e-6, "entrée du 1er raccord (copie 0)");
        let mut x1 = vec![0f32; hc * h];
        Hc::retro(&mat(&W_A, &entree_a, h), &x0, &sa, hc, h, &mut x1);
        let sf = ffn.sortie(&x1);
        proche(&sf.pre, &PRE_F, 1e-6, "pre de la FFN (celle qui part à la tête)");
        // La FFN se replie avec la `pre` de l'ATTENTION, pas la sienne.
        let mut entree_f = vec![0f32; h];
        Hc::melanger(&x1, &sa.pre, hc, h, &mut entree_f);
        proche(&entree_f, &ENTREE_F, 1e-6, "entrée de la FFN (pre de l'attention)");
        let mut x2 = vec![0f32; hc * h];
        Hc::retro(&mat(&W_F, &entree_f, h), &x1, &sf, hc, h, &mut x2);
        proche(&x2, &X2, 1e-5, "flux après la FFN");
        // La tête : repliement par la `pre` de la dernière FFN, puis norme.
        let mut replie = vec![0f32; h];
        Hc::melanger(&x2, &sf.pre, hc, h, &mut replie);
        let mut norme = vec![0f32; h];
        rms_norm_sans_poids(&replie, 1e-20, &mut norme);
        for i in 0..h { norme[i] *= NORME_SORTIE[i]; }
        proche(&norme, &TETE, 1e-5, "tête (aucun poids appris)");
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
            hash_layers: hash, n_rot: 0, yarn: None, yarn_declare: None,
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

#[cfg(test)]
mod tests_kimi_k3 {
    //! Les deux mathématiques neuves de Kimi-K3, vérifiées **sans poids** :
    //! l'activation SiTU et l'attention résiduelle (`res_mix`).
    //!
    //! Les valeurs attendues sont recalculées à la main depuis la référence
    //! (`llama.cpp-k3/src/models/kimi-k3.cpp`), pas recopiées de notre code.
    use super::*;

    /// La même récurrence, écrite en NumPy — l'arbitre des tests KDA.
    fn kda_numpy(q: &[f64], k: &[f64], v: &[f64], g: &[f64], beta: f64,
                 s: &mut [f64], hd: usize) -> Vec<f64> {
        // s[i][j], i = clé, j = valeur — mêmes conventions que le Rust.
        for i in 0..hd {
            let d = g[i].exp();
            for j in 0..hd { s[i * hd + j] *= d; }
        }
        let mut sk = vec![0f64; hd];
        for i in 0..hd { for j in 0..hd { sk[j] += s[i * hd + j] * k[i]; } }
        for i in 0..hd { for j in 0..hd {
            s[i * hd + j] += k[i] * beta * (v[j] - sk[j]);
        } }
        (0..hd).map(|j| (0..hd).map(|i| s[i * hd + j] * q[i]).sum()).collect()
    }

    #[test]
    fn porte_kda_toujours_negative_et_bornée() {
        // Quelle que soit l'entrée, avec la borne −5 la porte est dans (−5, 0) :
        // `exp(g) ∈ (0, 1]`, donc l'état DÉCROÎT. Un signe inversé donnerait une
        // porte positive (croissance) — c'est le piège que la référence signale.
        for z in [-8.0f32, -1.0, 0.0, 1.0, 8.0] {
            let g = kda_porte(z, -1.0, -5.0);   // ssm_a = -exp(A_log) = -1
            assert!(g < 0.0 && g >= -5.0, "z={z} → g={g}");
        }
        // z = 0 → sigmoïde(0) = 0,5 → g = −2,5
        assert!((kda_porte(0.0, -1.0, -5.0) + 2.5).abs() < 1e-6);
        // exp(A_log) = 2 (ssm_a = −2) : g = −5·σ(0) = −2,5 aussi à z = 0
        assert!((kda_porte(0.0, -2.0, -5.0) + 2.5).abs() < 1e-6);
        // et une pente double pour z > 0
        let a = kda_porte(1.0, -1.0, -5.0);
        let b = kda_porte(1.0, -2.0, -5.0);
        assert!(b < a, "exp(A_log) plus grand décroît plus vite : {b} vs {a}");
    }

    #[test]
    fn conv_kda_glisse_la_fenetre_et_applique_silu() {
        let (d_conv, d_inner) = (4usize, 2usize);
        // noyau = 1 sur la DERNIÈRE position, 0 ailleurs → la sortie est la SiLU
        // de l'entrée courante, et l'état doit glisser.
        let mut poids = vec![0f32; d_conv * d_inner];
        for c in 0..d_inner { poids[(d_conv - 1) + d_conv * c] = 1.0; }
        // état CANAL-majeur : canal 0 = [0,1 ; 0,3 ; 0,5], canal 1 = [0,2 ; 0,4 ; 0,6]
        let mut etat = vec![0.1f32, 0.3, 0.5, 0.2, 0.4, 0.6];
        let x = [2.0f32, -2.0];
        let mut out = vec![0f32; d_inner];
        kda_conv_silu(&x, &poids, &mut etat, d_conv, d_inner, &mut out);
        let silu = |v: f32| v * (1.0 / (1.0 + (-v).exp()));
        assert!((out[0] - silu(2.0)).abs() < 1e-6);
        assert!((out[1] - silu(-2.0)).abs() < 1e-6);
        // l'état a glissé : canal 0 = [0,3 ; 0,5 ; 2,0], canal 1 = [0,4 ; 0,6 ; −2,0]
        assert!((etat[0] - 0.3).abs() < 1e-6 && (etat[1] - 0.5).abs() < 1e-6
                && (etat[2] - 2.0).abs() < 1e-6, "état canal 0 : {etat:?}");
        assert!((etat[3] - 0.4).abs() < 1e-6 && (etat[4] - 0.6).abs() < 1e-6
                && (etat[5] + 2.0).abs() < 1e-6, "état canal 1 : {etat:?}");
        // noyau = 1 sur la PREMIÈRE position → sortie = SiLU(plus ancien état)
        let mut poids2 = vec![0f32; d_conv * d_inner];
        for c in 0..d_inner { poids2[0 + d_conv * c] = 1.0; }
        // canal 0 = [0,5 ; 1,5 ; 2,5], canal 1 = [1,0 ; 2,0 ; 3,0]
        let mut etat2 = vec![0.5f32, 1.5, 2.5, 1.0, 2.0, 3.0];
        let mut out2 = vec![0f32; d_inner];
        kda_conv_silu(&x, &poids2, &mut etat2, d_conv, d_inner, &mut out2);
        assert!((out2[0] - silu(0.5)).abs() < 1e-6, "{}", out2[0]);
        assert!((out2[1] - silu(1.0)).abs() < 1e-6, "{}", out2[1]);
    }

    #[test]
    fn kda_une_etape_contre_numpy() {
        let hd = 4usize;
        let q = [0.5f32, -0.25, 1.0, 0.0];
        let k = [1.0f32, 0.5, -0.5, 0.25];
        let v = [0.1f32, 0.2, -0.3, 0.4];
        let g = [-0.1f32, -0.2, -0.3, -0.4];
        let beta = 0.7f32;
        let mut s = vec![0f32; hd * hd];
        for i in 0..hd * hd { s[i] = ((i as f32) * 0.13).sin() * 0.5; }
        let s0 = s.clone();
        let mut out = vec![0f32; hd];
        kda_pas(&q, &k, &v, &g, beta, &mut s, hd, &mut out);
        // référence en f64
        let (q8, k8, v8, g8) = (q.map(|x| x as f64), k.map(|x| x as f64),
                                v.map(|x| x as f64), g.map(|x| x as f64));
        let mut s8: Vec<f64> = s0.iter().map(|&x| x as f64).collect();
        let attendu = kda_numpy(&q8, &k8, &v8, &g8, beta as f64, &mut s8, hd);
        for j in 0..hd {
            let e = attendu[j] as f32;
            assert!((out[j] - e).abs() < 1e-5, "sortie {j} : {} vs {e}", out[j]);
        }
        for i in 0..hd * hd {
            assert!((s[i] - s8[i] as f32).abs() < 1e-5, "état {i} : {} vs {}", s[i], s8[i]);
        }
    }

    #[test]
    fn kda_etat_nul_rend_le_produit_exterieur() {
        // État nul : `sk = 0`, donc `s = k ⊗ (β v)` et `o = sᵀ q`.
        let hd = 2usize;
        let (q, k, v) = ([1.0f32, 1.0], [2.0f32, 3.0], [0.5f32, -0.5]);
        let g = [0.0f32, 0.0];
        let beta = 1.0f32;
        let mut s = vec![0f32; hd * hd];
        let mut out = vec![0f32; hd];
        kda_pas(&q, &k, &v, &g, beta, &mut s, hd, &mut out);
        // s = [[2·0,5, 2·(−0,5)], [3·0,5, 3·(−0,5)]] = [[1,−1],[1,5,−1,5]]
        assert!((s[0] - 1.0).abs() < 1e-6 && (s[1] + 1.0).abs() < 1e-6);
        assert!((s[2] - 1.5).abs() < 1e-6 && (s[3] + 1.5).abs() < 1e-6);
        // o = sᵀ q = [1+1,5, −1−1,5] = [2,5, −2,5]
        assert!((out[0] - 2.5).abs() < 1e-6 && (out[1] + 2.5).abs() < 1e-6);
    }

    #[test]
    fn kda_porte_negative_oublie_l_etat() {
        // Une porte très négative efface l'état : la sortie ne dépend plus que de
        // `k`, `v`, `q` du jeton courant (c'est le sens de la décroissance).
        let hd = 2usize;
        let (q, k, v, g) = ([1.0f32, 1.0], [1.0f32, 1.0], [1.0f32, 1.0], [-30.0f32, -30.0]);
        let mut s = vec![100.0f32; hd * hd];
        let mut out = vec![0.0f32; hd];
        kda_pas(&q, &k, &v, &g, 1.0, &mut s, hd, &mut out);
        // état ≈ k ⊗ v = [[1,1],[1,1]] ; o = [2,2]
        assert!((out[0] - 2.0).abs() < 1e-4, "{}", out[0]);
        assert!((out[1] - 2.0).abs() < 1e-4, "{}", out[1]);
    }

    #[test]
    fn situ_borne_la_porte() {
        let (beta, lin) = (4.0f32, 25.0f32);
        // g = 0 : tanh(0) = 0 → l'activation est nulle quelle que soit u.
        assert!((situ(0.0, 1.0, beta, lin)).abs() < 1e-7);
        // u = 0 : idem.
        assert!((situ(1.0, 0.0, beta, lin)).abs() < 1e-7);
        // Point de contrôle calculé à la main :
        //   tanh(2/4) = 0,46211716 · sigmoïde(2) = 0,88079708
        //   a = 4 × 0,46211716 × 0,88079708 = 1,62809172
        //   up = 25 × tanh(3/25) = 25 × 0,11942766 = 2,98569157
        let attendu = 4.0f32 * (2.0f32 / 4.0).tanh() * (1.0 / (1.0 + (-2.0f32).exp()))
            * (25.0f32 * (3.0f32 / 25.0).tanh());
        assert!((situ(2.0, 3.0, beta, lin) - attendu).abs() < 1e-6);
        assert!((attendu - 4.8612).abs() < 1e-3, "valeur de contrôle : {attendu}");
        // `linear_beta <= 0` DÉSACTIVE la transformation de la branche up.
        let sans = situ(2.0, 3.0, beta, 0.0);
        let a = 4.0f32 * (0.5f32).tanh() * (1.0 / (1.0 + (-2.0f32).exp()));
        assert!((sans - a * 3.0).abs() < 1e-6);
    }

    #[test]
    fn res_mix_melange_normes_et_bruts() {
        let h = 3usize;
        // Deux points de contrôle + le courant, tous distincts.
        let pile = vec![1.0f32, 0.0, 0.0,   0.0, 2.0, 0.0];
        let courant = vec![0.0f32, 0.0, 3.0];
        let w = vec![1.0f32, 1.0, 1.0];
        let mut out = vec![0.0f32; h];
        res_mix(&pile, 2, h, &courant, &w, 1e-6, &mut out);
        // Les trois scores sont ÉGAUX (chaque état a une seule composante non
        // nulle de même norme RMS) : le mélange est donc la MOYENNE des trois
        // états bruts, soit ([1,0,0] + [0,2,0] + [0,0,3]) / 3.
        let attendu = [1.0f32 / 3.0, 2.0 / 3.0, 1.0];
        for c in 0..h {
            assert!((out[c] - attendu[c]).abs() < 1e-5, "composante {c} : {} vs {}",
                    out[c], attendu[c]);
        }
        // Sans point de contrôle, la sortie EST le courant (poids 1).
        let mut out2 = vec![0.0f32; h];
        res_mix(&[], 0, h, &courant, &w, 1e-6, &mut out2);
        for c in 0..h { assert!((out2[c] - courant[c]).abs() < 1e-6); }
    }

    #[test]
    fn res_mix_score_sur_les_normes_pas_sur_les_bruts() {
        // Deux états colinéaires mais d'ÉCHELLE très différente : normalisés, ils
        // donnent le MÊME score (donc un mélange à égalité), alors que leurs
        // valeurs brutes diffèrent d'un facteur 100. Si le score portait sur les
        // bruts, le second écraserait le premier.
        let h = 2usize;
        let pile = vec![1.0f32, 1.0,   100.0, 100.0];
        let courant = vec![1.0f32, -1.0];
        let w = vec![1.0f32, 1.0];
        let mut out = vec![0.0f32; h];
        res_mix(&pile, 2, h, &courant, &w, 1e-12, &mut out);
        // Scores, calculés à la main : les deux points de contrôle se normalisent
        // en [1,1] (score 2 chacun, quelle que soit leur ÉCHELLE), le courant en
        // [1,-1] (score 0). Le softmax donne donc p = e²/(2e²+1) pour chaque
        // point et 1/(2e²+1) pour le courant — puis la somme porte sur les BRUTS.
        let e2 = (2.0f32).exp();
        let p = e2 / (2.0 * e2 + 1.0);
        let pc = 1.0 / (2.0 * e2 + 1.0);
        let attendu0 = p * 1.0 + p * 100.0 + pc * 1.0;
        let attendu1 = p * 1.0 + p * 100.0 + pc * (-1.0);
        assert!((out[0] - attendu0).abs() < 1e-3, "{} vs {}", out[0], attendu0);
        assert!((out[1] - attendu1).abs() < 1e-3, "{} vs {}", out[1], attendu1);
    }
}
