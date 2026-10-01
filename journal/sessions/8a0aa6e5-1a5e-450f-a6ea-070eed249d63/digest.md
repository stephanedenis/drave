# Session DSH — relecture

- identifiant : `8a0aa6e5-1a5e-450f-a6ea-070eed249d63`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-01 11:15:40
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu es un relecteur adverse. Tu ne modifies AUCUN fichier : tu lis, tu vérifies, tu rapportes. Ton travail est de trouver ce qui est FAUX, pas de confirmer ce qui va bien.

Contexte : dépôt Rust à /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence GGUF « std seul », binaire `drave-core/target/release/drave`). Le commit le plus récent (3eb0af7) vient d'introduire un lecteur GGUF multi-fichiers et un format « clusters ». Le fichier de sprint `sprints/08-un-modele-eclate-se-lit-comme-un-seul.md` décrit ce qui a été fait et les mesures annoncées.

Fichiers à examiner en priorité :
- `drave-core/src/gguf.rs` (fonctions `open_multi`, `open_avec_prefixes`, `open_multi_meta`, `open_meta_avec_prefixes`, `tbuf`, `octets_tensor`, `shard_de`, `chemins_du_modele`, `open_auto`, `open_meta_auto`, `q8_dot_at`, `q8_dot_avx2`, `q8_view`, `data_ptr`)
- `drave-core/src/clusters.rs` (tout)
- `drave-core/src/model.rs` (fonction `charger_moe`, `impl Moe`, et les sites d'appel de `moe.ou(...)`)

Questions précises auxquelles répondre par OUI/NON avec la preuve (numéro de ligne + extrait) :

1. `tbuf` et les autres chemins (q8_dot_at, q8_dot_avx2, data_ptr, q8_blocks, q4k_blocks, q6k_blocks, mxfp4_blocks, q4_blocks, dequant, raw_levels, row_f32) utilisent-ils TOUS le bon décalage (début des données du bon fichier) ? Y a-t-il encore un chemin qui lit au début du fichier au lieu du début des données ?
2. Le calcul `octets_tensor` est-il juste pour tous les types listés ? Vérifie au moins Q4_K (144 o / 256 poids), Q6_K (210/256), Q8_0 (34/32), MXFP4 (17/32), IQ1_M (56/256), BF16 (2/1), F32 (4/1) contre la table de ggml. Un type est-il mal apparié à sa taille ou à sa taille de bloc ?
3. `chemins_du_modele` : que se passe-t-il si le dossier contient un fichier nommé par exemple `modele-00001-of-00002.gguf` ET `autre-00001-of-00002.gguf` ? Et si `total` vaut 1 ? Et si le chemin passé est un shard dont le préfixe contient lui-même « -of- » ?
4. `clusters::Mapping::lire` : y a-t-il un cas où un mapping INCOMPLET (tous les experts ne sont pas placés) est accepté silencieusement ? Le test `mapping_partiel_est_permis` dit qu'un mapping partiel est normal — est-ce cohérent avec l'usage qu'en fait `charger_moe` ?
5. `Moe::ou` : quand `local` est `None`, la borne est `e < self.n_expert_global`. `n_expert_global` vaut-il toujours la valeur attendue ? Vérifie le chemin où `charger_moe` est appelé.
6. Dans `clusters::ouvrir_interne`, l'ordre des fichiers est `commun.gguf` puis `cluster-*.gguf` TRIÉS par nom. Le tri lexicographique de `cluster-00.gguf` … `cluster-09.gguf` … `cluster-100.gguf` donne-t-il le bon ordre ? Quel est l'impact si ce n'est pas le cas ?
7. Y a-t-il un endroit où une erreur de lecture de fichier est ignorée (`let _ =`, `.ok()`, `unwrap_or`) alors qu'elle devrait être propagée ?
8. Le test `multi_fichiers_egale_mono_fichier` peut-il passer alors que le code est faux ? Décris un défaut qu'il ne détecterait pas.

Tu peux exécuter des commandes en LECTURE SEULE : `grep`, `sed -n`, `cargo test --release` (autorisé), et tu peux écrire UNIQUEMENT dans /tmp si tu veux fabriquer un fichier de test. Ne modifie aucun fichier du dépôt. Ne lance pas de commande qui compile le dépôt (pas de `cargo build`) — un `cargo test --release` est acceptable mais une seule fois.

Rends un rapport court et dense : pour chaque question, la réponse, la preuve (fichier:ligne), et — s'il y a un défaut — sa gravité (bloquant / gênant / cosmétique) et le correctif minimal proposé. Si tu ne trouves rien sur une question, dis-le explicitement plutôt que d'inventer. Ne félicite pas, ne résume pas le code.
Your parent agent id is "bbd6969f-0f70-42b2-8951-64d1f2f36d2e". Before you finish, send your result to that agent with send_message({ agent_id: "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

### 👤 Utilisateur

Current runtime context. This snapshot supersedes earlier runtime-context snapshots.

Current DSH file policy: danger-full-access. The DSH file sandbox does not restrict file modifications by available operations.

Approval prompts are disabled in this session: actions that require approval are rejected automatically — do not request sandbox escalation (do not set `sandbox_permissions`).

You are a delegated subagent: your permission scope was fixed when you were started and cannot be widened from inside this session — operations that require approval are rejected automatically. When the task needs access beyond that scope, do not retry the denied operation; state the limitation in your reply so the delegating agent can handle it.

### 👤 Utilisateur

<system-reminder>
A skill is a reusable set of task-specific instructions. The following skills are available in this session:

<available_skills>
- `microsoft-foundry`: Deploy, evaluate, fine-tune, and manage Foundry agents end-to-end with azd: hosted agent scaffold/run/deploy, prompt agent create, batch eval, continuous eval, prompt optimizer, Agent Optimizer scaffold, agent.yaml, dataset curation from traces, model fine-tuning (SFT/DPO/RFT). USE FOR: azd ai agent, azd provision/deploy, deploy agent, hosted agent, create agent, add tool to agent, invoke agent, evaluate agent, continuous eval, continuous monitoring, agent CI/CD, optimize prompt, improve prom...
</available_skills>

If the user names a skill, or the task clearly matches a skill's description, call the `skill` tool with the exact skill name before taking task actions. Load all applicable skills, then follow their full instructions. This catalog contains summaries only; do not infer or follow a skill's instructions until it has been loaded.
A user may also invoke a skill directly; its <skill_content> block then appears in this conversation. Follow it, and do not call the `skill` tool again for that skill.
</system-reminder>

### 🤖 Assistant

⏵ Lecture du code ciblé : gguf.rs, clusters.rs, model.rs

I'll start by reading the key files.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -5 && echo \"---\" && wc -l drave-core/src/gguf.rs drave-core/src/clusters.rs drave-core/src/model.rs sprints/08-un-modele-eclate-se-lit-comme-un-seul.md", "description": "Inspect repo state and file sizes"}`

  ```
3eb0af7 Un modèle éclaté se lit comme un seul : lecteur multi-fichiers, shards et clusters
7c1b9ff Convertisseur GGUF → modèle éclaté en clusters : un fichier par cluster, vérifié par empreintes
aea1b10 Politique de stockage : la bibliothèque brute sur le mécanique, le NVMe pour nos artefacts (mesures à l'appui)
e9cc44f Modèles lourds : file de 1,14 To en téléchargement, plan écrit, état honnête
b83d284 Découpage des MoE : la fréquence suffit, la co-activation n'ajoute rien (accord 1,000)
---
  1267 drave-core/src/gguf.rs
   260 drave-core/src/clusters.rs
  4248 drave-core/src/model.rs
   161 sprints/08-un-modele-eclate-se-lit-comme-un-seul.md
  5936 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls drave-core/src/", "description": "List source files"}`

  ```
clusters.rs
engine.rs
gguf.rs
gpu.rs
list.rs
main.rs
model.rs
tokenizer.rs
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs</path>
<type>file</type>
<content>
1: //! Lecteur GGUF minimal (std seul).
2: //!
3: #![allow(dead_code)] // lecteur générique : tous les formats ne servent pas au moteur
4: 
5: //! Ne lit que ce dont le moteur a besoin : métadonnées, descripteurs de tenseurs,
6: //! et les niveaux quantifiés (Q8_0 / Q4_0) ou les flottants (F32 / F16).
7: 
8: use std::collections::HashMap;
9: use std::fs::File;
10: use std::io::{Read, Seek, SeekFrom};
11: use std::path::Path;
12: 
13: #[derive(Debug, Clone)]
14: pub enum Meta {
15:     U8(u8), I8(i8), U16(u16), I16(i16), U32(u32), I32(i32),
16:     F32(f32), Bool(bool), Str(String), Array(Vec<Meta>), U64(u64), I64(i64), F64(f64),
17: }
18: 
19: impl Meta {
20:     pub fn as_u64(&self) -> Option<u64> {
21:         match self {
22:             Meta::U32(v) => Some(*v as u64),
23:             Meta::U64(v) => Some(*v),
24:             Meta::I32(v) => Some(*v as u64),
25:             Meta::I64(v) => Some(*v as u64),
26:             _ => None,
27:         }
28:     }
29:     pub fn as_f64(&self) -> Option<f64> {
30:         match self {
31:             Meta::F32(v) => Some(*v as
… [55257 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs", "offset": 1084}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs</path>
<type>file</type>
<content>
1084:             b.extend_from_slice(&(v.len() as u64).to_le_bytes());
1085:             b.extend_from_slice(v.as_bytes());
1086:         };
1087:         b.extend_from_slice(b"GGUF");
1088:         b.extend_from_slice(&3u32.to_le_bytes());
1089:         b.extend_from_slice(&(tensors.len() as u64).to_le_bytes());
1090:         b.extend_from_slice(&2u64.to_le_bytes());        // deux métadonnées
1091:         // Ordre GGUF : clef, type (u32), valeur.
1092:         s(&mut b, "general.architecture");
1093:         b.extend_from_slice(&8u32.to_le_bytes());        // GGUF_TYPE_STRING
1094:         s(&mut b, "essai");
1095:         s(&mut b, "general.alignment");
1096:         b.extend_from_slice(&4u32.to_le_bytes());        // GGUF_TYPE_UINT32
1097:         b.extend_from_slice(&32u32.to_le_bytes());
1098: 
1099:         // Les décalages sont relatifs au début du bloc de données de CE fichier.
1100:         let mut offsets = Vec::new();
1101:         let mut cur = 0u64;
1102:         for (_, dims) in tensors {
1103:             offsets.push(cur);
1104:             cur += dims.
… [9091 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de clusters.rs et des usages de moe.ou / q8_view

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/clusters.rs"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/clusters.rs</path>
<type>file</type>
<content>
1: //! Format **clusters** : un fichier commun, N fichiers d'experts, un mapping.
2: //!
3: //! Le problème que ce format résout : un MoE range ses 128 experts dans trois
4: //! tenseurs 3D par couche, et un nœud qui n'en sert que 16 en lit quand même
5: //! 128 — soit 8 fois trop. Découpé, le nœud ne lit que son huitième.
6: //!
7: //! Trois pièces, et rien d'autre :
8: //!
9: //! * `commun.gguf` — tout ce qui n'est pas un expert : embeddings, attention,
10: //!   normes, ET le routeur (`ffn_gate_inp`), qui doit rester global puisque
11: //!   c'est lui qui désigne l'expert ;
12: //! * `cluster-XX.gguf` — les seuls `ffn_{gate,up,down}_exps` d'un sous-ensemble
13: //!   d'experts, aux mêmes décalages internes que dans le fichier d'origine ;
14: //! * `mapping.tsv` — pour chaque couche, où est chaque expert global.
15: //!
16: //! Le mapping est un **texte**, délibérément : le moteur est en Rust sans
17: //! dépendance, et un format binaire maison demanderait un lecteur de plus à
18: //! éprouver. Trois colonnes se lisent à l'œil, ce qui n'est pas un luxe quand
19: //!
… [11250 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"q8_view\\|\\.base\\b\\|data_ptr\\|starts\\[\" --include=*.rs . | head -50", "description": "Find users of q8_view/base/data_ptr"}`

  ```
./drave-core/src/list.rs:451:            let p = unsafe { self.base.add((o * self.nb_ligne + b) * 34) };
./drave-core/src/list.rs:845:            let p = self.base.add((o * self.nb_ligne + sup) * crate::gguf::TAILLE_Q6K);
./drave-core/src/list.rs:910:            let p = self.base.add((o * self.nb_ligne + sup) * crate::gguf::TAILLE_Q4K);
./drave-core/src/list.rs:1020:            let p = unsafe { self.base.add((o * self.nb_ligne + sup) * t) };
./drave-core/src/list.rs:1052:            let p = unsafe { self.base.add((o * self.nb_ligne + sup) * t) };
./drave-core/src/list.rs:1109:            let p = unsafe { self.base.add((o * self.nb_ligne + b) * pas) };
./drave-core/src/list.rs:1141:            let p = self.base.add((o * self.nb_ligne + b) * pas);
./drave-core/src/model.rs:132:            out.push(Vue4 { base: g.data_ptr(nom)?, n_out, n_in, nb: n_in / bloc, src });
./drave-core/src/model.rs:145:        Some(Vue4 { base: g.data_ptr(nom)?, n_out, n_in, nb: n_in / bloc, src })
./drave-core/src/model.rs:218:        let p = unsafe { self.base.add(e * octets) };
./drave-core/src/model.rs:224:        let base = unsafe { self.base.add(e * self.n_out * self.nb * self.pas()) };
./drave-core/sr
… [1621 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection de model.rs : charger_moe, impl Moe, sites d'appel

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"charger_moe\\|struct Moe\\|impl Moe\\|n_expert_global\\|n_expert_local\\|moe\\.ou\\|\\.ou(\" drave-core/src/*.rs", "description": "Locate Moe struct and call sites"}`

  ```
drave-core/src/clusters.rs:180:    // dit à `charger_moe` où sont les experts.
drave-core/src/clusters.rs:222:        assert_eq!(m.ou(0, 3), Some((0, 0)));
drave-core/src/clusters.rs:223:        assert_eq!(m.ou(0, 1), Some((0, 1)));
drave-core/src/clusters.rs:224:        assert_eq!(m.ou(0, 0), Some((1, 0)));
drave-core/src/clusters.rs:225:        assert_eq!(m.ou(0, 2), Some((1, 1)));
drave-core/src/clusters.rs:226:        assert_eq!(m.ou(1, 3), Some((1, 1)));
drave-core/src/clusters.rs:228:        assert_eq!(m.ou(1, 9), None, "un expert hors bornes n'est pas une panique");
drave-core/src/clusters.rs:256:        assert_eq!(m.ou(0, 2), Some((1, 0)));
drave-core/src/clusters.rs:257:        assert_eq!(m.ou(0, 0), None);
drave-core/src/model.rs:97:fn charger_moe(g: &Gguf, l: usize, n_expert: usize) -> Option<Moe> {
drave-core/src/model.rs:186:        couche: l, n_expert_global: n_expert, local: map,
drave-core/src/model.rs:243:pub struct Moe {
drave-core/src/model.rs:264:    pub n_expert_global: usize,
drave-core/src/model.rs:271:impl Moe {
drave-core/src/model.rs:278:            None => if e < self.n_expert_global { Some((0, e)) } else { None },
drave-core/src/model.rs:279:            
… [328 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,260p' drave-core/src/model.rs", "description": "Read model.rs head"}`

  ```
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
    pub n_layer: usiz
… [10384 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '260,330p' drave-core/src/model.rs", "description": "Read Moe impl"}`

  ```
pub down: Vec<Vue4>,
    /// Couche dont ce mélange fait partie (pour le mapping).
    pub couche: usize,
    /// Nombre d'experts GLOBAUX : c'est lui qu'indexe le routeur, et lui seul.
    pub n_expert_global: usize,
    /// Mapping global → (fichier, ligne) quand le modèle est en clusters.
    pub local: Option<&'static crate::clusters::Mapping>,
    /// Expert partagé, toujours actif (certains modèles seulement).
    pub shexp: Option<(Vue4, Vue4, Vue4)>,
}

impl Moe {
    /// Où trouver l'expert GLOBAL `e` : `(vue, ligne locale)`. `None` signifie
    /// que cet expert n'est pas dans ce nœud — ce n'est pas une erreur, c'est
    /// le principe même du découpage.
    #[inline]
    pub fn ou(&self, e: usize) -> Option<(usize, usize)> {
        match self.local {
            None => if e < self.n_expert_global { Some((0, e)) } else { None },
            Some(m) => m.ou(self.couche, e),
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
    pub q_norm: Op
… [1481 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1580,1660p' drave-core/src/model.rs", "description": "Read charger_moe call site"}`

  ```
// Capturé avant que `cfg` ne soit déplacé dans la structure.
        let n_layer_total = cfg.n_layer;
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
                wo: Proj::load(&g, &p("attn_output.weight"), Some(&p("attn_output.bias")), dense || q4 != 0, au
… [4392 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2820,2900p' drave-core/src/model.rs", "description": "Read first moe.ou call site"}`

  ```
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
                    if trace_active {
                        use std::io::Write;
                        let mut ids: Vec<u32> = idx.clone();
                        
… [3333 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3630,3700p' drave-core/src/model.rs", "description": "Read second moe.ou call site"}`

  ```
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
      
… [3139 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2760,2822p' drave-core/src/model.rs", "description": "Read MoE routing prologue (batch path)"}`

  ```
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
                Self::rmsnorm(r, &lay.
… [2418 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3560,3632p' drave-core/src/model.rs", "description": "Read MoE routing prologue (single path)"}`

  ```
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
                if let Some(
… [3220 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche du convertisseur clusters et de la doc de format

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"commun.gguf\\|cluster-\" --include=* . 2>/dev/null | grep -v \"^./.git/\" | head -30", "description": "Find converter and docs referencing clusters"}`

  ```
(no output)
[timed out after 60000ms]
[killed by signal: SIGTERM]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls && ls tools 2>/dev/null; ls sprints", "description": "List repo root and sprints"}`

  ```
bench
colab
data
docs
drave-core
journal
models
__pycache__
Qtrinet-bootstrap.md
README.md
reports
REPRISE.md
run_8bit_perfection.py
run_clusters.py
run_cpu.py
run_encoding.py
run_harness.py
run_list_mode.py
run_precision.py
run_quantify.py
run_real_clusters.py
run_sparsity.py
run_value_encoding.py
sprints
src
tools
aiguille.py
analyse_flux.py
archive_sessions.py
clusters_moe.py
colab_cote_local.sh
compare_logits.py
convertir_clusters.py
diff_flux.py
flux_codec.py
harmony_canonique.py
make_patch.py
manifeste_modeles_lourds.json
mla_synthetique.py
pair_factice.py
preparer_colab.sh
profil_flux.py
proxy_latence.py
__pycache__
ref_logits
ref_logits.cpp
ref_logits.md
session_report.py
sprint.sh
telecharger_modeles.py
trace_compacite.py
vision_mtmd.py
vision_ref.py
01-premier-des-trois-noyaux-gpu-du-top-k-le.md
02-fusionner-la-cha-ne-du-top-k-d-port-desc.md
03-qualit-de-l-attention-creuse-long-contex.md
04-le-k-de-l-attention-creuse-l-chec-au-mil.md
05-refaire-la-grille-avec-de-vraies-fenetres.md
06-le-taux-de-recuperation.md
07-cloture-de-la-nuit.md
08-un-modele-eclate-se-lit-comme-un-seul.md
COURANT
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/08-un-modele-eclate-se-lit-comme-un-seul.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/08-un-modele-eclate-se-lit-comme-un-seul.md</path>
<type>file</type>
<content>
1: # Sprint 08 — Un modèle éclaté se lit comme un seul : lecteur multi-fichiers, shards et clusters
2: 
3: - **Début** : 11:13 · **Fin** : 13:13 (boxing de 120 min)
4: - **Objectif** : un modèle éclaté en plusieurs fichiers (shards d'un GGUF découpé,
5:   ou notre format en clusters) doit s'ouvrir avec **la même commande** qu'un
6:   modèle ordinaire, et rendre **le même résultat**.
7: - **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.
8: 
9: ## Ce qui a été fait
10: 
11: ### 1. Le lecteur ne connaissait qu'un fichier
12: 
13: `Gguf` portait `buf: Vec<u8>` et `data_start: usize` : un seul tampon, un seul
14: début de données. Un tenseur était donc `data_start + offset`, et rien ne
15: permettait de dire « ce tenseur vit dans l'autre fichier ».
16: 
17: Refonte : `bufs: Vec<Vec<u8>>` et `starts: Vec<usize>`, plus un champ `fichier`
18: sur chaque `TensorInfo`. Tous les accès aux poids passent par **un seul point**,
19: `tbuf(&t)` — c'est ce qui a permis de changer la représentation sans dupliquer
20: les quinze
… [7973 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"cluster-\\|n_clusters\\|cluster_index\\|{c:\\|:0\\|zfill\\|format(\" tools/convertir_clusters.py | head -60", "description": "Inspect converter naming"}`

  ```
20:    cluster-00.gguf …    par cluster : les tranches d'experts de TOUTES les couches
404:            chemin = os.path.join(args.dossier, f"cluster-{c:02d}.gguf")
411:                "fichier": os.path.basename(chemin), "role": f"cluster-{c:02d}",
415:            print(f"cluster-{c:02d}.gguf   : {len(nouveaux):4} tenseurs · "
419:        chemin = os.path.join(args.dossier, f"cluster-{c:02d}.gguf")
423:            "fichier": os.path.basename(chemin), "role": f"cluster-{c:02d}",
426:        print(f"cluster-{c:02d}.gguf   : {len(tlist):4} tenseurs · "
  ```

### 🤖 Assistant

⏵ Vérification des chemins d'ouverture, appels et erreurs avalées

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"open_auto\\|open_multi\\|open_avec_prefixes\\|chemins_du_modele\\|open_meta_auto\\|open_multi_meta\" --include=*.rs . ", "description": "Find callers of new constructors"}`

  ```
./drave-core/src/main.rs:99:    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
./drave-core/src/main.rs:1007:    let g = Gguf::open_meta_auto(path).ok()?;
./drave-core/src/main.rs:1041:    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
./drave-core/src/main.rs:1376:    // `open_meta_auto` : l'inventaire ne lit que les en-têtes. Avec `open`, un
./drave-core/src/main.rs:1380:    let g = Gguf::open_meta_auto(path).expect("ouverture de l'en-tête GGUF");
./drave-core/src/main.rs:2417:    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
./drave-core/src/main.rs:3032:    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
./drave-core/src/main.rs:3213:    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
./drave-core/src/main.rs:3488:    let g = Gguf::open_meta_auto(path).expect("ouverture du GGUF");
./drave-core/src/main.rs:3534:    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
./drave-core/src/model.rs:1476:        let g = Gguf::open_auto(path).expect("ouverture du GGUF");
./drave-core/src/clusters.rs:190:        Gguf::open_avec_prefixes(&chemins, &refs)?
./drave-core/src/gguf.rs:230:    pub fn open_multi<P: AsRef<Path>>(che
… [1866 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"let _ = \\|\\.ok()\\|unwrap_or(0)\\|unwrap_or_default()\" drave-core/src/clusters.rs drave-core/src/gguf.rs | head -40", "description": "Find swallowed errors in gguf/clusters"}`

  ```
drave-core/src/clusters.rs:56:                    let v = champs[i + 1].parse::<usize>().unwrap_or(0);
drave-core/src/clusters.rs:117:        self.local.get(l).map(|v| v.iter().filter(|x| **x >= 0).count()).unwrap_or(0)
drave-core/src/clusters.rs:181:    let _ = ACTIF.set(Mapping {
drave-core/src/clusters.rs:229:        let _ = std::fs::remove_file(&p);
drave-core/src/clusters.rs:243:        let _ = std::fs::remove_file(&p);
drave-core/src/clusters.rs:258:        let _ = std::fs::remove_file(&p);
drave-core/src/gguf.rs:305:        let total: usize = apres.parse().ok()?;
drave-core/src/gguf.rs:308:        let n: usize = num.parse().ok()?;
drave-core/src/gguf.rs:1018:                let _ = KV;
drave-core/src/gguf.rs:1191:        let _ = std::fs::remove_file(&p);
drave-core/src/gguf.rs:1244:        let _ = std::fs::remove_file(&p_tous);
drave-core/src/gguf.rs:1245:        let _ = std::fs::remove_file(&p_a);
drave-core/src/gguf.rs:1246:        let _ = std::fs::remove_file(&p_b);
drave-core/src/gguf.rs:1265:        for p in [&p_a, &p_b, &p_c] { let _ = std::fs::remove_file(p); }
  ```

### 🤖 Assistant

⏵ Vérification de la table ggml contre la source amont

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls docs/ && grep -rn \"IQ1_M\\|iq1_m\\|type_size\\|blck_size\" docs/*.md | head -40", "description": "Check docs for ggml type table"}`

  ```
colab-reparti.md
comparaison-spiking.md
contexte-long.md
convertisseur.md
format-clusters.md
format-flux.md
histoire.md
plan-deepseek-v4-flash.md
plan-gpu-topk.md
plan-mla-vision.md
plan-mode4-lot-listes.md
plan-modeles-lourds.md
plan-prefill-reparti.md
programme-recherche.md
roadmap.md
sprints.md
vision.md
docs/plan-deepseek-v4-flash.md:4:disque mécanique (`/home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/`,
docs/plan-deepseek-v4-flash.md:17:récupéré, en quantification **UD-IQ1_M** : la plus petite publiée, 86,9 Go en trois
docs/plan-deepseek-v4-flash.md:73:python3 tools/telecharger_modeles.py --seulement DeepSeek-V4-Flash-UD-IQ1_M
docs/plan-modeles-lourds.md:24:| **Kimi-K2.7-Code** | le meilleur agent de code ouvert | **303,9 Go** (UD-IQ1_M) | 262 k | en file |
  ```

- **bash** `{"command": "find / -name \"ggml-common.h\" -not -path \"*/proc/*\" 2>/dev/null | head -5; find / -name \"libggml*\" -not -path \"*/proc/*\" 2>/dev/null | head -5", "description": "Look for local ggml sources"}`

  ```
(no output)
[timed out after 60000ms]
[killed by signal: SIGTERM]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"type\\|octets\\|IQ1_M\\|iq1_m\\|144\\|210\\|56\\|17\" docs/format-clusters.md | head -60", "description": "Read format-clusters doc highlights"}`

  ```
6:18,56** et **625 ms au lieu de 3,9 s** sur Qwen3-30B-A3B.
37:1. **Aucune requantification.** Les octets des poids sont copiés tels quels. Les
39:   des multiples de 256), donc la tranche d'un expert est une **plage d'octets
40:   exacte** — le convertisseur le vérifie (`par_expert * ne == octets`) et
47:   compare le SHA-256 de **chaque** tenseur — pour les clusters, la concaténation
64:## Mesures (Qwen3-30B-A3B-Instruct Q4_K_M, 18,56 Go, 48 couches, 128 experts)
66:| fichier | en-tête (mmap) | lecture totale | octets |
70:| le modèle entier | 0,9 ms | **3 906,4 ms** | **18,56 Go** |
72:Un nœud qui sert le cluster 0 charge **3,20 Go au lieu de 18,56 (5,8× moins)** et
100:  mémoire (18,56 Go pour Qwen3-30B). Charger 3,20 Go est déjà 5,8× mieux, mais le
103:* **Le format binaire du manifeste** : JSON convient à quelques kilo-octets ; si le
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/convertir_clusters.py", "description": "Read converter header"}`

  ```
#!/usr/bin/env python3
"""Convertisseur GGUF → « modèle éclaté en clusters », un fichier par cluster.

**Pourquoi.** Notre mode d'opération ne lit que les experts qu'un jeton allume, et
les modèles MoE publient leurs experts dans UN tenseur par couche
(`blk.N.ffn_gate_exps.weight [n_experts, …]`). Un nœud qui n'héberge que 16 experts
sur 128 lit donc un fichier de 18 Go pour en utiliser un huitième. Ici, chaque
cluster devient un **fichier GGUF autonome** : on l'ouvre seul, en mmap, et on ne
lit que sa tranche.

**Ce que le convertisseur NE fait pas** : il ne requantifie rien. Les octets des
poids sont copiés tels quels (les blocs de quantification sont alignés sur l'axe
des experts, donc une tranche d'expert est une plage d'octets exacte). Aucune perte,
aucune conversion, aucun choix de format de rechange.

**Sortie** (dans un dossier) :

    commun.gguf          ce qui n'est pas un expert : embeddings, sortie, attention,
                         normes, routeur de chaque couche
    cluster-00.gguf …    par cluster : les tranches d'experts de TOUTES les couches
    manifeste.json       rôle de chaque fichier, tenseurs portés, tailles, ordre des
                         experts, co
… [1842 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && (curl -sL --max-time 25 https://raw.githubusercontent.com/ggml-org/llama.cpp/master/ggml/src/ggml-common.h -o ggml-common.h && echo OK && grep -n \"block_iq1_m\\b\" -A 8 ggml-common.h | head -40) 2>&1 | tail -20", "description": "Fetch ggml-common.h and inspect block_iq1_m"}`

  ```
OK
437:} block_iq1_m;
438:static_assert(sizeof(block_iq1_m) == QK_K/8 + QK_K/16 + QK_K/32, "wrong iq1_m block size/padding");
439-
440-// Used by IQ1_M quants
441-typedef union {
442-    ggml_half f16;
443-    uint16_t  u16;
444-} iq1m_scale_t;
445-
446-// Non-linear quants
  ```

- **bash** `{"command": "cd /tmp && grep -n \"static_assert(sizeof(block\" ggml-common.h | head -60", "description": "Extract all block size asserts"}`

  ```
185:static_assert(sizeof(block_q1_0) == sizeof(ggml_half) + QK1_0 / 8, "wrong q1_0 block size/padding");
192:static_assert(sizeof(block_q2_0) == sizeof(ggml_half) + QK2_0 / 4, "wrong q2_0 block size/padding");
199:static_assert(sizeof(block_q4_0) == sizeof(ggml_half) + QK4_0 / 2, "wrong q4_0 block size/padding");
212:static_assert(sizeof(block_q4_1) == 2 * sizeof(ggml_half) + QK4_1 / 2, "wrong q4_1 block size/padding");
219:static_assert(sizeof(block_mxfp4) == sizeof(uint8_t) + QK_MXFP4/2, "wrong mxfp4 block size/padding");
227:static_assert(sizeof(block_nvfp4) == sizeof(uint8_t)*(QK_NVFP4/QK_NVFP4_SUB) + QK_NVFP4/2, "wrong nvfp4 block size/padding");
235:static_assert(sizeof(block_q5_0) == sizeof(ggml_half) + sizeof(uint32_t) + QK5_0 / 2, "wrong q5_0 block size/padding");
249:static_assert(sizeof(block_q5_1) == 2 * sizeof(ggml_half) + sizeof(uint32_t) + QK5_1 / 2, "wrong q5_1 block size/padding");
256:static_assert(sizeof(block_q8_0) == sizeof(ggml_half) + QK8_0, "wrong q8_0 block size/padding");
269:static_assert(sizeof(block_q8_1) == 2*sizeof(ggml_half) + QK8_1, "wrong q8_1 block size/padding");
281:static_assert(sizeof(block_tq1_0) == sizeof(ggml_half) + QK_K / 64 + (QK_K - 4 *
… [1946 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && curl -sL --max-time 25 https://raw.githubusercontent.com/ggml-org/llama.cpp/master/ggml/src/ggml.c -o ggml.c && grep -n \"GGML_TYPE_.*blck_size\" ggml.c | head -30; echo ---; grep -n \"type_size *= *sizeof(block\" ggml.c | head -50", "description": "Fetch ggml.c type table"}`

  ```
---
680:        .type_size                = sizeof(block_q1_0),
688:        .type_size                = sizeof(block_q2_0),
696:        .type_size                = sizeof(block_q4_0),
704:        .type_size                = sizeof(block_q4_1),
724:        .type_size                = sizeof(block_q5_0),
732:        .type_size                = sizeof(block_q5_1),
740:        .type_size                = sizeof(block_q8_0),
748:        .type_size                = sizeof(block_q8_1),
755:        .type_size                = sizeof(block_mxfp4),
763:        .type_size                = sizeof(block_nvfp4),
771:        .type_size                = sizeof(block_q2_K),
779:        .type_size                = sizeof(block_q3_K),
787:        .type_size                = sizeof(block_q4_K),
795:        .type_size                = sizeof(block_q5_K),
803:        .type_size                = sizeof(block_q6_K),
811:        .type_size                = sizeof(block_iq2_xxs),
819:        .type_size                = sizeof(block_iq2_xs),
827:        .type_size                = sizeof(block_iq3_xxs),
835:        .type_size                = sizeof(block_iq3_s),
843:        .type_size                = sizeo
… [443 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle des usages de Q8View dans la tête de sortie

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3840,3870p' drave-core/src/model.rs && echo ===== && sed -n '4008,4030p' drave-core/src/model.rs", "description": "Read Q8View usage in head"}`

  ```
let s32: Vec<Vec<i32>> = (0..t)
                .map(|i| crate::list::sommes32(&qx[i * h..(i + 1) * h])).collect();
            let (qxr, s32r, sxsr) = (&qx, &s32, &sxs);
            std::thread::scope(|sc| {
                for (ci, part) in out.chunks_mut(chunk * t).enumerate() {
                    let base = ci * chunk;
                    sc.spawn(move || {
                        for i0 in (0..t).step_by(TUILE_TETE) {
                            let i1 = (i0 + TUILE_TETE).min(t);
                            for j in 0..(part.len() / t) {
                                let o = base + j;
                                for i in i0..i1 {
                                    part[j * t + i] = dref.dot16(o, &qxr[i * h..(i + 1) * h],
                                                                 &s32r[i]) * sxsr[i];
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
            std::t
… [1288 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '100,160p' drave-core/src/model.rs", "description": "Read Proj::load / data_ptr usage"}`

  ```
let map = clusters_actifs();
    // Un tenseur d'experts est soit en clair dans le fichier ouvert, soit dans
    // les fichiers de clusters sous le préfixe `cl{c}/`. Dans le second cas
    // chaque fichier ne porte QUE ses experts locaux : la dimension d'expert
    // du tenseur vaut `experts_par_cluster`, pas `n_expert`.
    let vues = |s: &str| -> Option<Vec<Vue4>> {
        let base = p(s);
        let noms: Vec<String> = match map {
            _ if g.tensor(&base).is_some() => vec![base],
            Some(m) => (0..m.n_clusters).map(|c| format!("cl{c}/{base}"))
                          .filter(|n| g.tensor(n).is_some()).collect(),
            None => return None,
        };
        if noms.is_empty() { return None; }
        let mut out = Vec::with_capacity(noms.len());
        for nom in &noms {
            let t = g.tensor(nom)?;
            if t.dims.len() < 3 { return None; }
            let ligne_experts = t.dims[0] as usize;
            if ligne_experts != n_expert {
                // Un fichier de cluster : sa dimension locale doit être celle
                // annoncée par le mapping, sinon les lignes seraient lues au
                // hasard.
                matc
… [2052 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"n_expert:\\|expert_count\\|n_expert_used\\|expert_used_count\\|ffn_exp\" drave-core/src/model.rs | head -30", "description": "Find cfg.n_expert derivation"}`

  ```
37:    pub n_expert: usize,
38:    pub n_expert_used: usize,
39:    pub ffn_exp: usize,
97:fn charger_moe(g: &Gguf, l: usize, n_expert: usize) -> Option<Moe> {
1491:            n_expert: g.cfg("expert_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
1492:            n_expert_used: g.cfg("expert_used_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
1493:            ffn_exp: g.cfg("expert_feed_forward_length").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
2116:        let largeur = self.cfg.ffn.max(self.cfg.ffn_exp);
2162:        let largeur = self.cfg.ffn.max(self.cfg.ffn_exp);
2223:            let par_jeton = self.cfg.n_expert_used.max(1) as f64;
2251:        let largeur = self.cfg.ffn.max(self.cfg.ffn_exp);
2802:                let k = if self.moe_topk > 0 { self.moe_topk } else { self.cfg.n_expert_used };
2859:                let nff = self.cfg.ffn_exp;
3155:        let largeur_profil = self.cfg.ffn.max(self.cfg.ffn_exp);
3179:        let mut gate = vec![0f32; cfg.ffn.max(cfg.ffn_exp)];
3183:        let mut up = vec![0f32; cfg.ffn.max(cfg.ffn_exp)];
3625:                let k = if self.moe_topk > 0 { self.moe_topk } else { cfg.n_expert_used };
3696:               
… [401 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '995,1015p' drave-core/src/main.rs", "description": "Read main.rs .ok()? context"}`

  ```
meta_ints(g, "tokenizer.ggml.token_type"),
        &pre,
    )
}

fn cfg_dims(m: &model::Model) -> usize { m.cfg.hidden }

/// Taille du vocabulaire, lue dans l'en-tête du GGUF sans charger le modèle.
fn mdl_cfg_vocab(path: &str) -> Option<usize> {
    // `open_meta` : le garde-fou n'a besoin que des dimensions du tenseur
    // d'embedding. Avec `open`, il lisait les 62 Go de gpt-oss AVANT que le
    // modèle ne soit chargé — deux lectures complètes du fichier par mesure.
    let g = Gguf::open_meta_auto(path).ok()?;
    g.tensor("token_embd.weight").map(|t| t.dims[0] as usize)
}

/// Tokenise un texte et imprime les identifiants — sert à vérifier le
/// pré-découpage contre une implémentation de référence.

/// Banc d'essai des noyaux GPU : la MÊME tête, trois chemins.
///
  ```

- **bash** `{"command": "cd /tmp && cat > t.rs <<'EOF'\nuse std::path::Path;\nfn main() {\n    let p = Path::new(\"modele-00001-of-00002.gguf\");\n    println!(\"parent = {:?}\", p.parent());\n    println!(\"read_dir = {:?}\", std::fs::read_dir(p.parent().unwrap_or(Path::new(\".\"))).err());\n}\nEOF\nrustc -O - … [86 caractères tronqués]`

  ```
parent = Some("")
read_dir = Some(Os { code: 2, kind: NotFound, message: "No such file or directory" })
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"expert_count\\|commun.gguf\\|manifeste\\|def ecrire\\|role\" tools/convertir_clusters.py | sed -n '1,60p'", "description": "Check converter expert_count and common file"}`

  ```
18:    commun.gguf          ce qui n'est pas un expert : embeddings, sortie, attention,
21:    manifeste.json       rôle de chaque fichier, tenseurs portés, tailles, ordre des
25:`<arch>.expert_count` y est ajusté au nombre d'experts du fichier, et le manifeste
150:def ecrire_gguf(chemin, kv_brut, tenseurs, source, debut_donnees, alignement,
346:    manifeste = {"source": os.path.abspath(args.source), "mode": args.mode,
370:    # ---- commun.gguf
372:        chemin = os.path.join(args.dossier, "commun.gguf")
375:        manifeste["fichiers"].append({"fichier": "commun.gguf", "role": "commun",
378:        print(f"commun.gguf      : {len(commun):4} tenseurs · {octets / 1e9:7.2f} Go")
385:        manifeste["experts"] = {str(l): ordres[l] for l in sorted(ordres)}
407:                kv_cluster = reecrire_kv(kv_brut, {f"{arch}.expert_count": len(ids)})
410:            manifeste["fichiers"].append({
411:                "fichier": os.path.basename(chemin), "role": f"cluster-{c:02d}",
422:        manifeste["fichiers"].append({
423:            "fichier": os.path.basename(chemin), "role": f"cluster-{c:02d}",
429:    with open(os.path.join(args.dossier, "manifeste.json"), "w", encoding="utf-8
… [340 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '330,430p' tools/convertir_clusters.py", "description": "Read converter split logic"}`

  ```
commun = []
    for t in tenseurs:
        if args.mode == "experts" and "_exps." in t["nom"]:
            couche = int(t["nom"].split(".")[1])
            experts[couche].append(t)
        else:
            commun.append(t)

    ne = 0
    if experts:
        premier = next(iter(experts.values()))[0]
        ne = premier["dims"][0]
        print(f"MoE : {len(experts)} couches × {ne} experts · "
              f"{sum(len(v) for v in experts.values())} tenseurs d'experts")

    os.makedirs(args.dossier, exist_ok=True)
    manifeste = {"source": os.path.abspath(args.source), "mode": args.mode,
                 "clusters": args.clusters, "n_experts": ne,
                 "fichiers": [], "experts": {}}

    # ---- mode « couches » : les blocs sont répartis par groupes de couches
    if args.mode == "couches":
        blocs = defaultdict(list)
        for t in commun:
            if t["nom"].startswith("blk."):
                blocs[int(t["nom"].split(".")[1])].append(t)
        if blocs:
            couches = sorted(blocs)
            par_cluster = (len(couches) + args.clusters - 1) // args.clusters
            noms_blocs = {t["nom"] for l in couches for t in blocs[l]}
            commu
… [3940 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des générateurs de mapping.tsv et du diff du commit

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"mapping.tsv\" --include=*.py --include=*.rs --include=*.md . | grep -v \"^./.git\" | head -20", "description": "Find mapping.tsv producers"}`

  ```
[stderr]
grep: ./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md: binary file matches
[timed out after 60000ms]
[killed by signal: SIGTERM]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat 3eb0af7 | head -30", "description": "Show commit stat"}`

  ```
commit 3eb0af715ff8f20c44694a7bf520b17056dcb63e
Author: Stéphane <stephane@localhost>
Date:   Thu Oct 1 11:14:59 2026 -0400

    Un modèle éclaté se lit comme un seul : lecteur multi-fichiers, shards et clusters
    
    Le lecteur GGUF ne connaissait qu'un fichier (un tampon, un début de données).
    Il porte maintenant un tampon et un début par fichier, et chaque tenseur sait
    lequel le porte. Tous les accès aux poids passent par un seul point (tbuf), ce
    qui a permis de changer la représentation sans toucher aux routines de calcul.
    
    - open_multi / open_avec_prefixes / open_multi_meta : métadonnées du premier
      fichier qui en porte, doublons divergents refusés, préfixes par fichier.
    - Détection des shards (-00002-of-00003) : un shard manquant est une erreur.
    - Un dossier contenant commun.gguf s'ouvre comme un modèle ordinaire.
    - clusters.rs : mapping.tsv (couche, ligne locale, expert global), refus des
      doublons ; Moe::ou(e) traduit l'expert global en (fichier, ligne locale) aux
      neuf points de lecture.
    - Table des tailles de types ggml relevée depuis libggml (iq1_m manquait :
      8,56 Go annoncés pour 86,9 Go de fichiers).
    
    
… [555 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"mapping.tsv\" tools/ drave-core/ docs/ sprints/ 2>/dev/null | head -20", "description": "Find mapping.tsv producers (scoped)"}`

  ```
drave-core/src/clusters.rs:14://! * `mapping.tsv` — pour chaque couche, où est chaque expert global.
drave-core/src/clusters.rs:37:    /// Lit `mapping.tsv`. Les lignes commençant par `#` sont des commentaires.
drave-core/src/clusters.rs:169:    let mapping = Mapping::lire(&dossier.join("mapping.tsv"))?;
drave-core/src/clusters.rs:172:            "{} fichiers de cluster pour {} annoncés dans mapping.tsv",
sprints/08-un-modele-eclate-se-lit-comme-un-seul.md:44:`clusters.rs` lit `mapping.tsv` (trois colonnes : couche, ligne locale, expert
sprints/08-un-modele-eclate-se-lit-comme-un-seul.md:114:- `mapping.tsv` n'est pas encore écrit par le convertisseur ; il a été produit
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat 3eb0af7 | tail -15 && git show 3eb0af7 -- drave-core/src/model.rs | head -60", "description": "Show commit files and model.rs diff"}`

  ```
tenseurs en 54 ms · Qwen3-30B-A3B en clusters 1587 tenseurs / 18,55 Go ·
    charge en 27,8 s · porte Qwen 19,3885 · 24 tests verts.

 REPRISE.md                                         |   21 +
 drave-core/src/clusters.rs                         |  260 +++
 drave-core/src/gguf.rs                             |  726 +++++-
 drave-core/src/main.rs                             |   62 +-
 drave-core/src/model.rs                            |  133 +-
 journal/README.md                                  |    2 +-
 journal/sessions/MANIFEST.md                       |    4 +-
 .../bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md | 2313 ++++++++++++++++++++
 .../rapport.md                                     |   97 +-
 .../08-un-modele-eclate-se-lit-comme-un-seul.md    |  161 ++
 sprints/COURANT                                    |    1 +
 11 files changed, 3634 insertions(+), 146 deletions(-)
commit 3eb0af715ff8f20c44694a7bf520b17056dcb63e
Author: Stéphane <stephane@localhost>
Date:   Thu Oct 1 11:14:59 2026 -0400

    Un modèle éclaté se lit comme un seul : lecteur multi-fichiers, shards et clusters
    
    Le lecteur GGUF ne connaissait qu'un fichier (un tampon, un début de données).
    Il 
… [2786 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lancement de cargo test --release en fond, lecture du diff main.rs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && ls target/release/drave 2>/dev/null; (cargo test --release 2>&1 | tail -60) ", "description": "Run cargo test --release once", "run_in_background": true, "timeoutMs": 900000}`

  ```
started background job bash-94
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 3eb0af7 -- drave-core/src/main.rs", "description": "Show main.rs diff of commit"}`

  ```
commit 3eb0af715ff8f20c44694a7bf520b17056dcb63e
Author: Stéphane <stephane@localhost>
Date:   Thu Oct 1 11:14:59 2026 -0400

    Un modèle éclaté se lit comme un seul : lecteur multi-fichiers, shards et clusters
    
    Le lecteur GGUF ne connaissait qu'un fichier (un tampon, un début de données).
    Il porte maintenant un tampon et un début par fichier, et chaque tenseur sait
    lequel le porte. Tous les accès aux poids passent par un seul point (tbuf), ce
    qui a permis de changer la représentation sans toucher aux routines de calcul.
    
    - open_multi / open_avec_prefixes / open_multi_meta : métadonnées du premier
      fichier qui en porte, doublons divergents refusés, préfixes par fichier.
    - Détection des shards (-00002-of-00003) : un shard manquant est une erreur.
    - Un dossier contenant commun.gguf s'ouvre comme un modèle ordinaire.
    - clusters.rs : mapping.tsv (couche, ligne locale, expert global), refus des
      doublons ; Moe::ou(e) traduit l'expert global en (fichier, ligne locale) aux
      neuf points de lecture.
    - Table des tailles de types ggml relevée depuis libggml (iq1_m manquait :
      8,56 Go annoncés pour 86,9 Go de fichiers).
    
    
… [7960 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/modeles/gguf/ 2>/dev/null | head -20; echo ---; ls /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/ 2>/dev/null | head", "description": "List model directories"}`

  ```
total 150826352
drwxr-xr-x. 1 stephane stephane        1206  1 oct 09:46 .
drwxr-xr-x. 1 stephane stephane          26  1 oct 08:59 ..
-rw-r--r--. 1 stephane stephane  1157671200 12 sep 19:02 bge-m3-FP16.gguf
-rw-r--r--. 1 stephane stephane 13341237600 13 aoû 07:27 codestral-22b-v0.1-q4_k_m.gguf
-rw-r--r--. 1 stephane stephane  8988109984 13 aoû 07:26 deepseek-r1-distill-qwen-14b-q4_k_m.gguf
-rw-r--r--. 1 stephane stephane  1117320800 24 sep 10:44 deepseek-r1-distill-qwen-1.5b-q4_k_m.gguf
drwxr-xr-x. 1 stephane stephane         118  1 oct 10:26 DeepSeek-V4.1-Flash-Q2
drwxr-xr-x. 1 stephane stephane         492  1 oct 10:48 DeepSeek-V4-Flash-UD-IQ1_M
-rw-r--r--. 1 stephane stephane   849103296 24 sep 13:15 eagle3-gpt-oss-120b-Q8_0.gguf
drwxr-xr-x. 1 stephane stephane           0  1 oct 09:05 GLM-5.3-Flash-UD-IQ1_S
drwxr-xr-x. 1 stephane stephane           0  1 oct 09:05 GLM-5.3-UD-IQ1_S
-rw-r--r--. 1 stephane stephane 63387346208 24 sep 13:14 gpt-oss-120b-MXFP4.gguf
drwxr-xr-x. 1 stephane stephane        1112  1 oct 11:23 Kimi-K2.7-Code-UD-IQ1_M
drwxr-xr-x. 1 stephane stephane           0  1 oct 09:05 MiniMax-H3
-rw-r--r--. 1 stephane stephane  1354162912 10 sep 14:31 mmproj-Qwen2.5
… [647 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la target 2>/dev/null; ls drave-core/target/release/drave 2>/dev/null; find . -name \"cluster-*.gguf\" -maxdepth 4 2>/dev/null | head; find . -name \"mapping.tsv\" -maxdepth 4 2>/dev/null | head", "description": "Check artifacts  … [18 caractères tronqués]`

  ```
drave-core/target/release/drave
  ```

### 👤 Utilisateur

background job bash-94 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && ls target/release/drave 2>/dev/null; (cargo test --release 2>&1 | tail -60) ) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-94"}`

  ```
target/release/drave
   --> src/gpu.rs:154:5
    |
152 | pub struct Gpu {
    |            --- fields in this struct
153 |     ctx: *mut c_void,
154 |     module: *mut c_void,
    |     ^^^^^^
...
158 |     f_proj_warp: *mut c_void,
    |     ^^^^^^^^^^^

warning: method `kv_ecrire` is never used
   --> src/gpu.rs:548:12
    |
182 | impl Gpu {
    | -------- method in this implementation
...
548 |     pub fn kv_ecrire(&self, m: &mut KvGpu, kvh: usize, pos: usize,
    |            ^^^^^^^^^

warning: the `ids:` in this pattern is redundant
   --> src/main.rs:672:9
    |
672 |         ids: mut ids, ids_file, prompt, n: n_new, temp, top_p, topk, rep_pen, hist,
    |         ^^^^^^^^^^^^ help: use shorthand field pattern: `mut ids`
    |
    = note: `#[warn(non_shorthand_field_patterns)]` on by default

warning: `drave-core` (bin "drave" test) generated 22 warnings (run `cargo fix --bin "drave" -p drave-core --tests` to apply 11 suggestions)
    Finished `release` profile [optimized] target(s) in 15.21s
     Running unittests src/main.rs (target/release/deps/drave-9a06049b91b56c63)

running 24 tests
test clusters::tests::mapping_lu_et_traduit ... ok
test clusters::tests::mapping_partie
… [1522 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la drave-core/target/release/drave && git log -1 --format=%cd && ls /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4.1-Flash-Q2/ | head && echo --- && ls /home/stephane/Data13TB/stephane/modeles/gguf/Kimi-K2.7-Code-UD-IQ … [69 caractères tronqués]`

  ```
-rwxr-xr-x. 2 stephane stephane 1885792  1 oct 11:20 drave-core/target/release/drave
Thu Oct 1 11:14:59 2026 -0400
DeepSeek-V4.1-Flash-Q2.gguf
DeepSeek-V4.1-Flash-Q2.gguf.part
---
Kimi-K2.7-Code-UD-IQ1_M-00001-of-00008.gguf
Kimi-K2.7-Code-UD-IQ1_M-00002-of-00008.gguf
Kimi-K2.7-Code-UD-IQ1_M-00003-of-00008.gguf
Kimi-K2.7-Code-UD-IQ1_M-00004-of-00008.gguf
Kimi-K2.7-Code-UD-IQ1_M-00005-of-00008.gguf
Kimi-K2.7-Code-UD-IQ1_M-00006-of-00008.gguf
Kimi-K2.7-Code-UD-IQ1_M-00006-of-00008.gguf.etat.json
Kimi-K2.7-Code-UD-IQ1_M-00006-of-00008.gguf.part0
Kimi-K2.7-Code-UD-IQ1_M-00006-of-00008.gguf.part1
Kimi-K2.7-Code-UD-IQ1_M-00006-of-00008.gguf.part2
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn modele_chemin\" -A 12 drave-core/src/main.rs && grep -n '\"--tensors\"\\|\"--modele\"' drave-core/src/main.rs | head", "description": "Check CLI for modele/tensors"}`

  ```
341:fn modele_chemin() -> String { MODELE.get().cloned().unwrap_or_default() }
342-
343-/// **Tableau de bord des réglages en vigueur** (`--options-actives`), lus sur le
344-/// MODÈLE après toutes les affectations.
345-///
346-/// Pourquoi il existe : le défaut le plus coûteux de ce dépôt n'est pas un calcul
347-/// faux, c'est un drapeau qui ne fait rien. Huit ont été corrigés en une session
348-/// (`--keep` en perplexité, `--ffn-gain` en inférence, les top-k dans les modes
349-/// flux, `--trace-flux` en inférence, `--threads` figé…), et chacun était
350-/// INVISIBLE : la sortie ne disait nulle part quelle valeur agissait. Ici, elle
351-/// le dit — et une valeur qu'on ne voit pas bouger est une valeur qui ne sert à
352-/// rien.
353-fn options_actives(mdl: &model::Model, mode: &str, ctx_impose: bool, dense: bool, keep: f32) {
54:        (opt.tensors, "--tensors"), (opt.banc_mla.is_some(), "--banc-mla"),
539:            "--tensors" => { o.tensors = true; 1 }
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"MODELE\" drave-core/src/main.rs | head", "description": "Check MODELE global syntax"}`

  ```
47:    let _ = MODELE.set(args[1].clone());
340:static MODELE: std::sync::OnceLock<String> = std::sync::OnceLock::new();
341:fn modele_chemin() -> String { MODELE.get().cloned().unwrap_or_default() }
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '35,60p' drave-core/src/main.rs", "description": "Check argv positional convention"}`

  ```
}
    // Une seule analyse, puis un aiguillage : `--plan`, `--tokenize`,
    // `--ppl`/`--ppl-texte` et `--infer` partagent désormais la même structure
    // d'options, donc les mêmes drapeaux.
    // Les variables d'environnement ont été renommées QT_* -> DRAVE_* : un
    // ancien nom encore présent dans un script ne ferait RIEN, en silence. On le
    // dit, plutôt que de laisser croire que l'option est active.
    if let Some((vieux, _)) = std::env::vars().find(|(k, _)| k.starts_with("QT_")) {
        eprintln!("[attention] {vieux} est l'ancien nom d'une variable d'environnement : \
elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.");
    }
    let opt = analyser(&args);
    let _ = MODELE.set(args[1].clone());
    // Plusieurs modes demandés : l'aiguillage en retient UN, dans un ordre
    // arbitraire, et le disait pas. On le dit.
    let modes: Vec<&str> = [
        (opt.banc_vision.is_some(), "--banc-vision"),
        (opt.flux_serveur.is_some(), "--flux-serveur"),
        (opt.ppl_reparti.is_some(), "--ppl-reparti"),
        (opt.tensors, "--tensors"), (opt.banc_mla.is_some(), "--banc-mla"),
        (opt.banc_kv > 0, "--banc-kv"), (opt.
… [266 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Tests empiriques : shards réels, nom ambigu, chemin sans dossier

- **bash** `{"command": "cd /tmp && printf 'GGUF' > x-00001-of-00002.gguf && printf 'GGUF' > x-00002-of-00002.gguf && printf 'GGUF' > essai-3-of-8.gguf && B=/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/target/release/drave && echo \"== bare filename (cwd=/tmp) ==\" && $B x-00001-of-00002.gguf --te … [259 caractères tronqués]`

  ```
== bare filename (cwd=/tmp) ==
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.

thread 'main' (2891932) panicked at src/main.rs:1380:40:
== ./ prefix ==
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.

thread 'main' (2891951) panicked at src/gguf.rs:526:9:
== nom ambigu essai-3-of-8.gguf ==
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.

thread 'main' (2891973) panicked at src/main.rs:1380:40:
  ```

- **bash** `{"command": "cd /tmp && timeout 300 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/target/release/drave /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf --tensors 2>&1 | head -12", "description": "Run inventory on rea … [38 caractères tronqués]`

  ```
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
deepseek4 · 3 fichiers · 1328 tenseurs · 86.90 Go de poids · en-têtes lus en 54.153788ms
  fichier 0 :     0 tenseurs · 0.00 Go
  fichier 1 :   784 tenseurs · 49.97 Go
  fichier 2 :   544 tenseurs · 36.92 Go
 · block_count 43 · embedding_length 4096 · attention.head_count 64 · attention.head_count_kv 1 · expert_count 256 · expert_used_count 6 · context_length 1048576
  Q4_K     output.weight                          [129280, 4096] · 529.5 M poids · fichier 1
  F32      output_hc_base.weight                  [4] · 0.0 M poids · fichier 1
  F32      output_hc_fn.weight                    [4, 16384] · 0.1 M poids · fichier 1
  F32      output_hc_scale.weight                 [1] · 0.0 M poids · fichier 1
  F32      output_norm.weight                     [4096] · 0.0 M poids · fichier 1
  Q4_K     token_embd.weight                      [129280, 4096] · 529.5 M poids · fichier 1
  ```

- **bash** `{"command": "cd /tmp && B=/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/target/release/drave && echo \"== bare ==\" && $B x-00001-of-00002.gguf --tensors 2>&1 | grep -A3 \"panicked\"; echo \"== ambigue ==\" && $B /tmp/essai-3-of-8.gguf --tensors 2>&1 | grep -A3 \"panicked\"; echo \"== . … [118 caractères tronqués]`

  ```
== bare ==
thread 'main' (2892031) panicked at src/main.rs:1380:40:
ouverture de l'en-tête GGUF: Os { code: 2, kind: NotFound, message: "No such file or directory" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
== ambigue ==
thread 'main' (2892040) panicked at src/main.rs:1380:40:
ouverture de l'en-tête GGUF: Custom { kind: NotFound, error: "modèle découpé incomplet dans /tmp : 8 shards annoncés, 1 présents" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
== ./ ==
thread 'main' (2892051) panicked at src/gguf.rs:526:9:
version GGUF 0 non gérée
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
  ```

### 🤖 Assistant

⏵ Preuve du panic « premier fichier sans métadonnées » et du tri des clusters

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport struct\ndef kv_str(k,v):\n    b=struct.pack(\"<Q\",len(k))+k.encode()\n    b+=struct.pack(\"<I\",8)+struct.pack(\"<Q\",len(v))+v.encode()\n    return b\n# A : GGUF sans aucune metadonnee\na=b\"GGUF\"+struct.pack(\"<I\",3)+struct.pack(\"<Q\",0)+struct … [516 caractères tronqués]`

  ```
24 69
thread 'main' (2892142) panicked at src/gguf.rs:435:59:
called `Option::unwrap()` on a `None` value
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
  ```

- **bash** `{"command": "python3 -c \"\nnoms=[f'cluster-{c:02d}.gguf' for c in range(128)]\ns=sorted(noms)\nimport re\nprint('positions 9..12 :',s[9:13])\nprint('index de cluster-100 :',s.index('cluster-100.gguf'))\nprint('index de cluster-10  :',s.index('cluster-10.gguf'))\nprint('index de cluster-99  :',s.ind … [169 caractères tronqués]`

  ```
positions 9..12 : ['cluster-09.gguf', 'cluster-10.gguf', 'cluster-100.gguf', 'cluster-101.gguf']
index de cluster-100 : 11
index de cluster-10  : 10
index de cluster-99  : 127
desaccord : 117 clusters sur 128
  ```

### 🤖 Assistant

⏵ Lecture du reste du diff model.rs (les 9 points de lecture)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 3eb0af7 -- drave-core/src/model.rs | sed -n '60,300p'", "description": "Read rest of model.rs diff"}`

  ```
+    // chaque fichier ne porte QUE ses experts locaux : la dimension d'expert
+    // du tenseur vaut `experts_par_cluster`, pas `n_expert`.
+    let vues = |s: &str| -> Option<Vec<Vue4>> {
+        let base = p(s);
+        let noms: Vec<String> = match map {
+            _ if g.tensor(&base).is_some() => vec![base],
+            Some(m) => (0..m.n_clusters).map(|c| format!("cl{c}/{base}"))
+                          .filter(|n| g.tensor(n).is_some()).collect(),
+            None => return None,
+        };
+        if noms.is_empty() { return None; }
+        let mut out = Vec::with_capacity(noms.len());
+        for nom in &noms {
+            let t = g.tensor(nom)?;
+            if t.dims.len() < 3 { return None; }
+            let ligne_experts = t.dims[0] as usize;
+            if ligne_experts != n_expert {
+                // Un fichier de cluster : sa dimension locale doit être celle
+                // annoncée par le mapping, sinon les lignes seraient lues au
+                // hasard.
+                match map {
+                    Some(m) if ligne_experts == m.par_cluster => {}
+                    _ => return None,
+                }
+            }
+            le
… [11474 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des tailles sur disque et recherche du dossier clusters

- **bash** `{"command": "ls -l /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/*.gguf | awk '{s+=$5; print $5, $9} END {printf \"TOTAL %.2f Go\\n\", s/1e9}'", "description": "Sum shard sizes on disk"}`

  ```
5256864 /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf
49971881124 /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00002-of-00003.gguf
36924175168 /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00003-of-00003.gguf
TOTAL 86.90 Go
  ```

- **bash** `{"command": "find /home/stephane/Data13TB/stephane/modeles -maxdepth 3 -name \"commun.gguf\" 2>/dev/null | head; find /home/stephane/Data13TB/stephane/modeles -maxdepth 3 -name \"mapping.tsv\" 2>/dev/null | head; find /home/stephane/Data13TB/stephane/modeles -maxdepth 3 -name \"cluster-*.gguf\" 2>/d … [72 caractères tronqués]`

  ```
(no output)
  ```

- **bash** `{"command": "cd /tmp && timeout 300 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/target/release/drave /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf --tensors 2>/dev/null | awk 'NF>=4 && $2 ~ /weight|bias/ {print  … [108 caractères tronqués]`

  ```
662 F32
    318 Q8_0
    126 Q5_K
     45 Q6_K
     44 IQ1_M
     43 BF16
     42 IQ2_XXS
     41 IQ3_XXS
      3 I32
      2 Q4_K
      2 MXFP4
  ```

### 🤖 Assistant

⏵ Vérification du chemin de repli quand charger_moe rend None

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn vide\" -A 8 drave-core/src/model.rs | head -20; echo ===; grep -n \"fn matvec\\b\" -A 25 drave-core/src/model.rs | head -40", "description": "Inspect Proj::vide and matvec fallback"}`

  ```
375:    pub fn vide() -> Self {
376-        Proj { gpu: None, m: None, d: None, q4: None, bias: None }
377-    }
378-
379-    fn load(g: &Gguf, name: &str, bias: Option<&str>, dense: bool, auto: bool, keep: f32,
380-            q4: bool, bits6: bool) -> Self {
381-        let t = g.tensor(name).unwrap_or_else(|| panic!("tenseur {name} absent"));
382-        let n_out = t.dims[0] as usize;
383-        let n_in = t.dims[1] as usize;
===
1987:    fn matvec(pool: &mut Pool, p: &Proj, x: &[f32], out: &mut [f32], events: &mut u64,
1988-              levels: f32, thresh: f32, topk: usize, renorm: bool, scratch: &mut Vec<f32>,
1989-              thresh_auto: f32) {
1990-        let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
1991-            for (o, v) in out.iter_mut().enumerate() {
1992-                *v = p.bias.as_ref().map_or(0.0, |b| b[o]);
1993-            }
1994-            return;
1995-        };
1996-        // ---- choix de direction par mesure : sous le seuil, disperser (push) ;
1997-        // au-dessus, le produit scalaire dense (pull) est plus rapide.
1998-        // Forme 4 bits : pas d'événements du tout, un seul chemin.
1999-    
… [739 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2008,2050p' drave-core/src/model.rs", "description": "Read matvec shape selection"}`

  ```
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
       
… [884 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Consolidation des numéros de ligne pour le rapport

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"filter(|n| g.tensor(n).is_some())\\|gate.len() != up.len()\\|let Some((k, loc))\\|let Some((kexp, loc))\\|n_expert_global\\|meta.as_ref().unwrap()\\|if tous.iter().any\\|champs\\[i + 1\\].parse\\|let _ = ACTIF.set\\|_ => re … [148 caractères tronqués]`

  ```
drave-core/src/gguf.rs:272:            let ds = Self::debut_donnees(meta.as_ref().unwrap(), fin);
drave-core/src/gguf.rs:435:            starts.push(Self::debut_donnees(meta.as_ref().unwrap(), fin));
drave-core/src/gguf.rs:437:                if tous.iter().any(|u| u.name == t.name) { continue; }
drave-core/src/gguf.rs:477:            _ => return 0,
drave-core/src/clusters.rs:56:                    let v = champs[i + 1].parse::<usize>().unwrap_or(0);
drave-core/src/clusters.rs:164:    clusters.sort();
drave-core/src/clusters.rs:181:    let _ = ACTIF.set(Mapping {
drave-core/src/model.rs:110:                          .filter(|n| g.tensor(n).is_some()).collect(),
drave-core/src/model.rs:150:    if map.is_some() && (gate.len() != up.len() || gate.len() != down.len()) {
drave-core/src/model.rs:186:        couche: l, n_expert_global: n_expert, local: map,
drave-core/src/model.rs:264:    pub n_expert_global: usize,
drave-core/src/model.rs:278:            None => if e < self.n_expert_global { Some((0, e)) } else { None },
drave-core/src/model.rs:2873:                    let Some((k, loc)) = moe.ou(e) else { continue; };
drave-core/src/model.rs:3681:                    let Some((kexp, loc)
… [42 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification que le dépôt n'a pas bougé sous mes pieds

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain && echo \"--- HEAD:\" && git log --oneline -1 && echo \"--- mtimes:\" && ls -l --time-style=full-iso drave-core/src/model.rs drave-core/src/gguf.rs drave-core/src/clusters.rs", "description": "Check working tre … [9 caractères tronqués]`

  ```
M drave-core/src/model.rs
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md
 M journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md
?? journal/sessions/8a0aa6e5-1a5e-450f-a6ea-070eed249d63/
--- HEAD:
3eb0af7 Un modèle éclaté se lit comme un seul : lecteur multi-fichiers, shards et clusters
--- mtimes:
-rw-------. 1 stephane stephane  11201 2026-10-01 11:06:43.672778350 -0400 drave-core/src/clusters.rs
-rw-------. 1 stephane stephane  60264 2026-10-01 11:06:43.671883029 -0400 drave-core/src/gguf.rs
-rw-r--r--. 1 stephane stephane 225650 2026-10-01 11:19:59.677204970 -0400 drave-core/src/model.rs
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat drave-core/src/model.rs && git diff drave-core/src/model.rs | head -80", "description": "Diff working tree model.rs vs commit"}`

  ```
drave-core/src/model.rs | 9 +++++++++
 1 file changed, 9 insertions(+)
diff --git a/drave-core/src/model.rs b/drave-core/src/model.rs
index 24a19fa..be57a3d 100644
--- a/drave-core/src/model.rs
+++ b/drave-core/src/model.rs
@@ -1640,6 +1640,12 @@ impl Model {
                   pool.threads());
         let n_layer = cfg.n_layer;
         let sinks_vus = layers.iter().filter(|l| l.sinks.is_some()).count();
+        // Combien de couches ont RÉELLEMENT un mélange d'experts chargé. La
+        // configuration dit que le modèle en a ; elle ne dit pas que le
+        // chargeur les a trouvés. Quand les deux diffèrent, le moteur tombe
+        // dans le chemin dense et panique cent lignes plus loin, sur un
+        // message (« projection dense requise ») qui ne dit pas pourquoi.
+        let moe_vus = layers.iter().filter(|l| l.moe.is_some()).count();
         // Trace de configuration : une ligne qui dit quelles particularités
         // d'architecture ont été reconnues. Sans elle, on débogue à l'aveugle
         // sur un modèle de 60 Go.
@@ -1651,6 +1657,9 @@ impl Model {
                  if cfg.n_expert > 0 { "moe " } else { "" },
                  if cfg.n_expert > 0 { "" } 
… [431 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dernière passe de vérification des lignes dans model.rs (arbre modifié)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '97,116p;146,156p;184,188p;271,282p' drave-core/src/model.rs", "description": "Re-read key model.rs lines"}`

  ```
fn charger_moe(g: &Gguf, l: usize, n_expert: usize) -> Option<Moe> {
    if n_expert == 0 { return None; }
    let p = |s: &str| format!("blk.{l}.{s}");
    let map = clusters_actifs();
    // Un tenseur d'experts est soit en clair dans le fichier ouvert, soit dans
    // les fichiers de clusters sous le préfixe `cl{c}/`. Dans le second cas
    // chaque fichier ne porte QUE ses experts locaux : la dimension d'expert
    // du tenseur vaut `experts_par_cluster`, pas `n_expert`.
    let vues = |s: &str| -> Option<Vec<Vue4>> {
        let base = p(s);
        let noms: Vec<String> = match map {
            _ if g.tensor(&base).is_some() => vec![base],
            Some(m) => (0..m.n_clusters).map(|c| format!("cl{c}/{base}"))
                          .filter(|n| g.tensor(n).is_some()).collect(),
            None => return None,
        };
        if noms.is_empty() { return None; }
        let mut out = Vec::with_capacity(noms.len());
        for nom in &noms {
            let t = g.tensor(nom)?;
    };
    let gate = vues(&p("ffn_gate_exps.weight"))?;
    let up = vues(&p("ffn_up_exps.weight"))?;
    let down = vues(&p("ffn_down_exps.weight"))?;
    if map.is_some() && (gate.len() !=
… [1046 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2868,2876p;3676,3686p' drave-core/src/model.rs && md5sum drave-core/src/model.rs drave-core/src/gguf.rs drave-core/src/clusters.rs", "description": "Re-read call sites and hash files"}`

  ```
let mut sxg: Vec<f32> = Vec::with_capacity(t);
                let mut yq = vec![0f32; t * nff];
                let mut col = vec![0f32; nff];
                let mut colu = vec![0f32; nff];
                let mut ga = vec![0i16; t * nff];
                let mut s32a: Vec<Vec<i32>> = Vec::with_capacity(t);
                let mut sxa: Vec<f32> = Vec::with_capacity(t);
                for e in 0..ne {
                    let g = groupes[e].len();
                    use std::io::Write;
                    let mut ids: Vec<u32> = idx.clone();
                    ids.sort_unstable();       // l'ordre de `select_nth` est arbitraire
                    let liste: Vec<String> = ids.iter().map(|e| e.to_string()).collect();
                    let _ = writeln!(f, "{} {} {}", l, pos, liste.join(" "));
                }
                for v in down.iter_mut() { *v = 0.0; }
                for &e in &idx {
                    let w_exp = sc_e[e as usize] * inv_k;
                    // Traduction pour les modèles en clusters : l'expert global
                    // `e` n'est pas forcément dans ce nœud.
d6b11c4314da87edaa3c5bdbfab3ac1a  drave-core/src/model.rs
10b97dcd60d8a37f0ec8ea8a07bb7
… [88 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification finale : enum ggml à jour et usage du diagnostic presents

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"\\.presents(\\|presents(\" drave-core/src/ | grep -v \"fn presents\"; echo \"--- ggml enum:\"; curl -sL --max-time 20 https://raw.githubusercontent.com/ggml-org/llama.cpp/master/ggml/include/ggml.h | grep -n \"GGML_TYPE_\" … [72 caractères tronqués]`

  ```
drave-core/src/clusters.rs:227:        assert_eq!(m.presents(0), 4);
drave-core/src/clusters.rs:255:        assert_eq!(m.presents(0), 1);
--- ggml enum:
43://       struct ggml_tensor * x = ggml_new_tensor_1d(ctx, GGML_TYPE_F32, 1);
47://       struct ggml_tensor * a  = ggml_new_tensor_1d(ctx, GGML_TYPE_F32, 1);
48://       struct ggml_tensor * b  = ggml_new_tensor_1d(ctx, GGML_TYPE_F32, 1);
137://       struct ggml_tensor * a = ggml_new_tensor_2d(ctx, GGML_TYPE_F32, nx, ny);
390:        GGML_TYPE_F32     = 0,
391:        GGML_TYPE_F16     = 1,
392:        GGML_TYPE_Q4_0    = 2,
393:        GGML_TYPE_Q4_1    = 3,
394:        // GGML_TYPE_Q4_2 = 4, support has been removed
395:        // GGML_TYPE_Q4_3 = 5, support has been removed
396:        GGML_TYPE_Q5_0    = 6,
397:        GGML_TYPE_Q5_1    = 7,
398:        GGML_TYPE_Q8_0    = 8,
399:        GGML_TYPE_Q8_1    = 9,
400:        GGML_TYPE_Q2_K    = 10,
401:        GGML_TYPE_Q3_K    = 11,
402:        GGML_TYPE_Q4_K    = 12,
403:        GGML_TYPE_Q5_K    = 13,
404:        GGML_TYPE_Q6_K    = 14,
405:        GGML_TYPE_Q8_K    = 15,
406:        GGML_TYPE_IQ2_XXS = 16,
407:        GGML_TYPE_IQ2_XS  = 17,
408:        GGML_TYPE_IQ3_XXS =
… [1119 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Deux dernières preuves empiriques sur shard_de

- **bash** `{"command": "cd /tmp && B=/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/target/release/drave && printf 'GGUF' > a-of-b-00001-of-00002.gguf && printf 'GGUF' > a-of-b-00002-of-00002.gguf && printf 'GGUF' > y-00001-of-00001.gguf && echo \"== prefixe contenant -of- ==\" && $B /tmp/a-of-b-00 … [224 caractères tronqués]`

  ```
== prefixe contenant -of- ==
thread 'main' (2892804) panicked at src/gguf.rs:526:9:
version GGUF 0 non gérée
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
== total=1 ==
thread 'main' (2892819) panicked at src/gguf.rs:526:9:
version GGUF 0 non gérée
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"let ne = self.cfg.n_expert\\|let ne = cfg.n_expert\\|n_expert: g.cfg(\\|moe.local.is_none()\\|let moe_vus\" drave-core/src/model.rs", "description": "Exact line numbers for Q5 evidence"}`

  ```
1491:            n_expert: g.cfg("expert_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
1648:        let moe_vus = layers.iter().filter(|l| l.moe.is_some()).count();
2227:            let ne = self.cfg.n_expert;
2807:                let ne = self.cfg.n_expert;
3630:                let ne = cfg.n_expert;
3695:                    if moe.gate[0].src == crate::list::Source::Mxfp4 && moe.local.is_none() {
  ```

### 🤖 Assistant

⏵ Rédaction du rapport adverse et envoi au parent

Review complete. Here is the report.

---

# Rapport adverse — commit 3eb0af7 (lecteur multi-fichiers + clusters)

**État vérifié** : `gguf.rs` md5 `10b97dcd…`, `clusters.rs` `35cbad5f…` (identiques au commit) ; `model.rs` `d6b11c43…` **modifié après le commit** (+9 lignes non commitées vers 1640, un diagnostic `mélanges d'experts chargés`). Les numéros de ligne `model.rs` ci-dessous sont ceux de l'arbre de travail actuel ; `gguf.rs`/`clusters.rs` sont ceux du commit.
**Vérifié empiriquement** : `cargo test --release` → **24 passed** ; inventaire DeepSeek → **3 fichiers · 1328 tenseurs · 86.90 Go · 54 ms**, répartition **0 / 784 / 544**, total disque **86.90 Go** — les mesures du sprint sont exactes.

## 1. Décalage des données — **OUI, tous les chemins sont corrects**
Aucun chemin ne lit plus au début du fichier : `tbuf` (`gguf.rs:560-567`), `octets_de` (`450-452`), `data_ptr` (`763-766`, passe par `tbuf`), `q8_dot_at` (`820` : `&self.bufs[v.fichier][self.starts[v.fichier]..]`), `q8_dot_avx2` (`934`, idem), `q8_blocks`/`q4k_blocks`/`q6k_blocks`/`mxfp4_blocks`/`q4_blocks` (`774-814`, tous `self.tbuf(t)`), `dequant` (`959`), `raw_levels` (`620`), `row_f32` (`653`).
Deux nuances, pas des défauts : `Q8View.base` est un offset **local au fichier** (`758`) — correct uniquement parce que les deux `q8_dot_*` tranchent `starts[...]` eux-mêmes ; tout nouveau lecteur de `Q8View` doit le refaire. Et `starts` des fichiers 2..N est calculé avec l'`alignment` du **premier fichier porteur de métadonnées** (`272`, `435`), pas du fichier concerné (`cosmétique` : tous les découpages réels partagent la même valeur).

## 2. `octets_tensor` — **OUI, juste pour tous les types listés**
Confronté à l'amont ggml (`ggml-common.h` `static_assert(sizeof(block…))` + table `type_size` de `ggml.c`) : Q4_K 144/256 ✓, Q6_K 210/256 ✓, Q8_0 34/32 ✓, MXFP4 17/32 ✓, **IQ1_M 56/256** ✓ (`sizeof(block_iq1_m) == QK_K/8+QK_K/16+QK_K/32`), BF16 2/1 ✓, F32 4/1 ✓, plus Q4_0/Q4_1/Q5_0/Q5_1/Q8_1/Q2_K/Q3_K/Q5_K/Q8_K/IQ2_XXS/IQ2_XS/IQ2_S/IQ3_XXS/IQ3_S/IQ1_S/IQ4_NL/IQ4_XS/TQ1_0/TQ2_0/NVFP4 (36/64) ✓. Aucun type mal apparié.
**Défaut (gênant)** : `_ => return 0,` (`gguf.rs:477`) — un type inconnu est compté **0 octet en silence**, exactement le mécanisme de l'incident iq1_m. Les types 41 (`Q1_0`) et 42 (`Q2_0`), ajoutés à ggml (`ggml.h:431-432`), tombent dedans. Correctif minimal : rendre `Option<u64>`/paniquer avec le numéro de type. À noter aussi : le commentaire `gguf.rs:461` renvoie à `docs/format-clusters.md`, qui **ne contient pas** la table.

## 3. `chemins_du_modele` — 2 défauts
- Deux modèles dans un dossier (`modele-…` + `autre-…`) : **OK**, le filtre `pref == prefixe && tot == total` (`330-331`) écarte l'autre ; `total == 1` : **OK** ; préfixe contenant `-of-` : **OK** (`rsplit_once` prend le dernier `-of-`) — vérifié en exécutant le binaire sur des fichiers factices dans /tmp.
- **Défaut A (gênant)** : chemin **sans dossier** (`cwd$ drave x-00001-of-00002.gguf`) → `path.parent()` vaut `Some("")` (`325`), `read_dir("")` échoue → panic `No such file or directory` alors que le fichier existe (reproduit ; avec `./x-…` ça passe). Correctif : `.filter(|d| !d.as_os_str().is_empty())` avant `unwrap_or(Path::new("."))`.
- **Défaut B (gênant)** : un **fichier unique** nommé `essai-3-of-8.gguf` est pris pour un shard → `open_auto` échoue en dur (`modèle découpé incomplet dans /tmp : 8 shards annoncés, 1 présents`, reproduit), alors que `shard_de` promet l'inverse (`298-301`). Correctif : exiger un numéro zero-paddé (largeur ≥ 5, comme llama.cpp) ou retomber sur l'ouverture mono-fichier si le fichier demandé existe.

## 4. Mapping incomplet — **OUI, accepté en silence ; incohérent avec `charger_moe`**
`local` est initialisé à `-1` (`clusters.rs:85`) et **jamais** contrôlé en complétude ; un `mapping.tsv` réduit à ses commentaires passe (tous les experts à -1), `Moe::ou` rend toujours `None`, les deux sites font `continue` (`model.rs:2873`, `3681`) : la couche MoE ne contribue plus rien, sans erreur ni message. Le test `mapping_partiel_est_permis` (`clusters.rs:249-259`) l'assume. Mais rien ne distingue « ce nœud ne porte pas cet expert » (voulu) d'« un mapping tronqué » ; le seul diagnostic, `presents()` (`clusters.rs:116`), n'est appelé que par des tests (`227`, `255`). Correctif minimal : à l'ouverture, imprimer `presents(l)/n_experts` par couche et refuser (ou exiger un drapeau `--nœud-partiel`) quand l'assemblage est complet.
**Défaut lié (gênant, bloquant si atteint)** : l'identifiant de cluster du TSV est utilisé comme **index direct** dans `Vec<Vue4>` (`model.rs:110`, `278`), mais le `Vec` est **compacté** par `.filter(|n| g.tensor(n).is_some())` (`110`) ; le contrôle `150` ne compare que gate/up/down entre eux, **jamais** à `m.n_clusters`. Un fichier de cluster sans le tenseur d'une couche décale silencieusement tous les index suivants (mêmes formes → aucune erreur) ; pire, si `ligne_experts == n_expert` (fichiers produits par `--mode couches`, qui gardent tous les experts), la branche `110` est acceptée et `loc` (< `par_cluster`) indexe le mauvais expert **sans bruit**. Correctifs : exiger `noms.len() == m.n_clusters`, et en mode clusters refuser `ligne_experts != par_cluster`.

## 5. `Moe::ou` et `n_expert_global` — **OUI, valeur attendue**
`n_expert_global = cfg.n_expert` (`model.rs:186`), lu depuis `expert_count` (`1491`) dans les métadonnées **du premier fichier qui en porte** (`gguf.rs:257-271`), qui est `commun.gguf` (`clusters.rs:175`) — le convertisseur y laisse le KV d'origine et ne réduit `expert_count` que dans les fichiers de cluster (`tools/convertir_clusters.py:372-374` vs `405-407`). Vérifié sur le vrai modèle : `expert_count 256`. La borne `e < n_expert_global` est donc **du code mort** : les deux sites itèrent `0..cfg.n_expert` (`2807`, `3630`), et avec `local == None` la `Vec` a exactement 1 élément (seule la branche `vec![base]` est atteignable), donc `(0, e)` est toujours valide. Aucun défaut ici. Nuance `cosmétique` : en clusters, le chemin GPU MXFP4 est désactivé en silence (`3695`, `&& moe.local.is_none()`) — le modèle tourne sur CPU sans le dire.

## 6. Tri des clusters — **NON, il est faux dès 100 clusters**
`clusters.sort()` (`clusters.rs:164`) est lexicographique : `cluster-100.gguf` arrive en position **11**, `cluster-10` en 10, `cluster-99` en 127 (mesuré : **117 des 128** positions diffèrent). Les préfixes sont attribués par **position** (`178` : `cl{c}/` avec `c` = rang) alors que `Mapping::ou` rend l'identifiant du TSV (`102`, `112`) → chaque expert est lu dans le mauvais fichier, **sans erreur** (formes identiques), et aucun test n'ouvre un dossier de clusters. Le nommage du convertisseur (`cluster-{c:02d}`) ne protège pas au-delà de 99 ; un nom non paddé casse dès 10. Gravité : **bloquant au-delà de 99 clusters**, latent sinon (défaut gênant aujourd'hui). Correctif minimal : trier par l'entier extrait de `cluster-<n>.gguf` et refuser si les numéros ne sont pas exactement `0..len-1`.

## 7. Erreurs avalées — oui, mais pas sur le chemin des poids
- `gguf.rs:437` : en mode en-tête seul, un doublon de nom est **silencieusement ignoré sans comparer dims/ttype**, alors que `open_avec_prefixes` refuse les divergents (`276-288`) → l'inventaire `--tensors` peut sous-compter sans le dire (`gênant`).
- `gguf.rs:477` (type inconnu → 0 octet) et `gguf.rs:452` (`.min(b.len())`, tranche tronquée silencieuse) — même famille (`gênant`).
- `gguf.rs:272` et `435` : `meta.as_ref().unwrap()` **panique** si le premier fichier ne porte pas `general.architecture`, ce qui rend l'erreur propre de `292`/`441` **inatteignable** et contredit le contrat documenté (« les métadonnées sont prises au premier fichier qui en porte », `219-222`). Reproduit : deux GGUF factices, le premier sans KV → `panicked at src/gguf.rs:435: unwrap() on None` (`gênant`).
- `clusters.rs:181` `let _ = ACTIF.set(...)` : un second modèle ouvert dans le même processus garde le premier mapping en silence (`cosmétique`, le processus ne sert qu'un modèle) ; `clusters.rs:56` `unwrap_or(0)` sur l'en-tête retombe en silence sur `n_experts/n_clusters` (`84`) (`cosmétique`) ; `gguf.rs:526` `assert!(version >= 2)` panique sur un fichier corrompu au lieu de rendre `Err` (`cosmétique`, préexistant).

## 8. `multi_fichiers_egale_mono_fichier` — **OUI, il peut passer sur du code faux**
Il ne fabrique que des tenseurs **F32** (`gguf.rs:1112`) et ne compare que via `dequant` : tout le chemin quantifié (`q8_dot_at`/`avx2`, `q4k/q6k/mxfp4/q8_blocks`, `raw_levels`, `Vue4`) lui échappe — c'est écrit noir sur blanc dans le sprint (`73-79`) pour le défaut qui a mis la perplexité à NaN. Autres angles morts : `open_avec_prefixes` (la route des clusters) n'est jamais appelé par un test ; `open_multi_meta` — le chemin où le défaut (b) a été trouvé — **n'a aucun test** ; `chemins_du_modele`/`open_auto` non plus ; `octets_poids()` compare la **même** fonction des deux côtés, donc une erreur de table s'annule ; et deux fichiers aux octets identiques (cas réel des petits tenseurs dupliqués dans les shards) rendraient une inversion d'origine invisible — le test l'évite exprès en donnant des valeurs distinctes par fichier.

## Mesures du sprint : vérifiées / non vérifiées
Vérifiés : 24 tests verts ; DeepSeek 3 shards, 1328 tenseurs, 86.90 Go annoncés = 86.90 Go sur disque, 54 ms, 0/784/544 ; l'histogramme des types du modèle réel (F32, Q8_0, Q5_K, Q6_K, IQ1_M, BF16, IQ2_XXS, IQ3_XXS, I32, Q4_K, MXFP4) ne contient **aucun type hors table**, ce qui recoupe Q2. Non vérifiables ici : les 27,8 s de chargement en clusters, la porte 19,3885, et l'inventaire Qwen3-30B en clusters — **aucun dossier de clusters n'existe plus sur disque** (`commun.gguf`/`mapping.tsv`/`cluster-*.gguf` introuvables sous `modeles/`).

**Ce que je n'ai pas trouvé** : aucune erreur de décalage restante (Q1), aucune entrée fausse dans la table ggml (Q2), aucun défaut sur `n_expert_global` (Q5).

