# Session DSH — relecture

- identifiant : `18b8879c-f211-43b8-9908-cf65e509b21d`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-02 15:03:48
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Rust « Drave », moteur d'inférence LLM). NE MODIFIE AUCUN FICHIER (lecture seule stricte).

MISSION : extraire EXHAUSTIVEMENT, depuis ces 7 fichiers uniquement :
- drave-core/src/clusters.rs (506 l.)
- drave-core/src/formats.rs (2847 l.)
- drave-core/src/gpu.rs (1573 l.)
- drave-core/src/gguf.rs (2246 l.)
- drave-core/src/materiel.rs (478 l.)
- drave-core/src/model.rs (7022 l.)
- drave-core/src/tokenizer.rs (507 l.)

tout ce qui concerne les identifiants exposés :
1. Les ENUMS publics et TOUTES leurs variantes (avec fichier:ligne), et pour les enums de type de quantification (Q4_K, MXFP4, IQ2_XXS, etc.) la liste complète des variantes et leur taille de bloc si visible.
2. Les CONSTANTES nommées `const`/`static` en MAJUSCULES liées aux formats, blocs, tailles, seuils, modes (nom + valeur + rôle en une phrase).
3. Les champs de structs publiques de configuration/description (noms + type + rôle si lisible) : en particulier les structs de description de tenseur/bloc, de plan GPU, de description matérielle, de tokenizer.
4. Les variables d'environnement citées (DRAVE_*, CUDA_*, etc.) : `env::var("...")`.
5. Les chaînes de mode/format comparées (`match` sur des `&str`, littéraux `"q4_k"`, `"gguf"`, `"mxfp4"`...).

MÉTHODE : `grep -n` et `rg -n --no-heading` pour localiser, puis `read` offset/limit pour le contexte. Pour gguf.rs et formats.rs, les tables de correspondance type→taille sont essentielles : cite-les intégralement avec numéros de ligne.

FORMAT DE SORTIE (texte brut, dense, pas d'introduction) : groupé par fichier, puis par catégorie (enums / constantes / structs / env / littéraux). Format par entrée : `NOM (ou "littéral")` — fichier:ligne — valeur/type — rôle en une phrase. Cite les numéros de ligne exacts. Sois exhaustif ; plusieurs centaines de lignes de sortie attendues, ne résume pas, n'invente rien.
Your parent agent id is "f2de810a-b765-444d-b3cc-d8fce1ba2105". Before you finish, send your result to that agent with send_message({ agent_id: "f2de810a-b765-444d-b3cc-d8fce1ba2105", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Cartographie des enums et constantes dans les 7 fichiers cibles

I'll start by locating the files and running broad greps to map the structure.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l drave-core/src/clusters.rs drave-core/src/formats.rs drave-core/src/gpu.rs drave-core/src/gguf.rs drave-core/src/materiel.rs drave-core/src/model.rs drave-core/src/tokenizer.rs", "description": "Count lines in the 7 target file … [3 caractères tronqués]`

  ```
506 drave-core/src/clusters.rs
  2847 drave-core/src/formats.rs
  1573 drave-core/src/gpu.rs
  2246 drave-core/src/gguf.rs
   478 drave-core/src/materiel.rs
  7022 drave-core/src/model.rs
   507 drave-core/src/tokenizer.rs
 15179 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading '^\\s*(pub\\s+)?enum\\s+' drave-core/src/clusters.rs drave-core/src/formats.rs drave-core/src/gpu.rs drave-core/src/gguf.rs drave-core/src/materiel.rs drave-core/src/model.rs drave-core/src/tokenizer.rs", "descript … [41 caractères tronqués]`

  ```
drave-core/src/gguf.rs:134:pub enum Tampon {
drave-core/src/gguf.rs:180:pub enum Meta {
drave-core/src/model.rs:28:pub enum Gating {
  ```

### 🤖 Assistant

⏵ Localisation des enums (y compris non-pub) et des impl blocks

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading '\\benum\\s+[A-Za-z_]' drave-core/src/clusters.rs drave-core/src/formats.rs drave-core/src/gpu.rs drave-core/src/gguf.rs drave-core/src/materiel.rs drave-core/src/model.rs drave-core/src/tokenizer.rs", "description … [42 caractères tronqués]`

  ```
drave-core/src/model.rs:28:pub enum Gating {
drave-core/src/gguf.rs:134:pub enum Tampon {
drave-core/src/gguf.rs:180:pub enum Meta {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading '^\\s*(pub\\s+)?(struct|trait|impl|type|union)\\s+' drave-core/src/clusters.rs drave-core/src/formats.rs drave-core/src/gpu.rs drave-core/src/gguf.rs drave-core/src/materiel.rs drave-core/src/model.rs drave-core/sr … [78 caractères tronqués]`

  ```
drave-core/src/tokenizer.rs:30:pub struct Tokenizer {
drave-core/src/tokenizer.rs:49:impl Tokenizer {
drave-core/src/materiel.rs:24:pub struct Noeud {
drave-core/src/materiel.rs:31:pub struct Cpu {
drave-core/src/materiel.rs:45:pub struct Gpu {
drave-core/src/materiel.rs:56:pub struct Disque {
drave-core/src/materiel.rs:65:pub struct Materiel {
drave-core/src/materiel.rs:75:pub struct Plan {
drave-core/src/materiel.rs:275:impl Materiel {
drave-core/src/gpu.rs:74:pub struct MatriceGpu {
drave-core/src/gpu.rs:86:pub struct KvGpu {
drave-core/src/gpu.rs:133:pub struct TamponsTopk {
drave-core/src/gpu.rs:152:pub struct Gpu {
drave-core/src/gpu.rs:182:impl Gpu {
drave-core/src/gguf.rs:16:type io_result<'a> = std::io::Result<&'a [u8]>;
drave-core/src/gguf.rs:30:pub struct Mappe {
drave-core/src/gguf.rs:101:impl Mappe {
drave-core/src/gguf.rs:115:impl Deref for Mappe {
drave-core/src/gguf.rs:116:    type Target = [u8];
drave-core/src/gguf.rs:124:impl Drop for Mappe {
drave-core/src/gguf.rs:139:impl Deref for Tampon {
drave-core/src/gguf.rs:140:    type Target = [u8];
drave-core/src/gguf.rs:147:impl Tampon {
drave-core/src/gguf.rs:185:impl Meta {
drave-core/src/gguf.rs:242:pub struct Tenso
… [1849 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Repérage global des constantes, statiques et variables d'environnement

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading '^\\s*(pub\\s+)?(const|static)\\s+[A-Z_0-9]+' drave-core/src/clusters.rs drave-core/src/formats.rs drave-core/src/gpu.rs drave-core/src/gguf.rs drave-core/src/materiel.rs drave-core/src/model.rs drave-core/src/toke … [74 caractères tronqués]`

  ```
drave-core/src/tokenizer.rs:28:const SEP: char = '\u{1}';
drave-core/src/materiel.rs:383:        const VRAM: f64 = 84.9;
drave-core/src/materiel.rs:384:        const RAM: f64 = 22.5;
drave-core/src/materiel.rs:385:        const NVME: f64 = 31.0;      // 16 lecteurs parallèles, mesuré
drave-core/src/materiel.rs:388:        const SUCCES: f64 = 0.80;
drave-core/src/gguf.rs:45:const PROT_READ: i32 = 1;
drave-core/src/gguf.rs:46:const MAP_PRIVATE: i32 = 2;
drave-core/src/gguf.rs:53:const MADV_WILLNEED: i32 = 3;
drave-core/src/gguf.rs:258:pub const GGML_F32: u32 = 0;
drave-core/src/gguf.rs:259:pub const GGML_F16: u32 = 1;
drave-core/src/gguf.rs:260:pub const GGML_Q4_0: u32 = 2;
drave-core/src/gguf.rs:261:pub const GGML_MXFP4: u32 = 39;
drave-core/src/gguf.rs:262:pub const GGML_Q2_K: u32 = 10;
drave-core/src/gguf.rs:263:pub const GGML_BF16: u32 = 30;
drave-core/src/gguf.rs:264:pub const GGML_Q3_K: u32 = 11;
drave-core/src/gguf.rs:265:pub const GGML_Q4_K: u32 = 12;
drave-core/src/gguf.rs:271:pub const GGML_Q5_0: u32 = 6;
drave-core/src/gguf.rs:272:pub const GGML_Q5_1: u32 = 7;
drave-core/src/gguf.rs:273:pub const GGML_Q5_K: u32 = 13;
drave-core/src/gguf.rs:274:pub const GGML_Q6_K: u32 = 14
… [3861 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading 'env::var|env!\\(|option_env!' drave-core/src/clusters.rs drave-core/src/formats.rs drave-core/src/gpu.rs drave-core/src/gguf.rs drave-core/src/materiel.rs drave-core/src/model.rs drave-core/src/tokenizer.rs", "des … [45 caractères tronqués]`

  ```
drave-core/src/gguf.rs:91:    matches!(std::env::var("DRAVE_PRELIRE_TOUT").as_deref(), Ok("1") | Ok("oui") | Ok("true"))
drave-core/src/gguf.rs:95:    match std::env::var("DRAVE_PRELIRE") {
drave-core/src/gguf.rs:156:    match std::env::var("DRAVE_MMAP") {
drave-core/src/gpu.rs:1540:        if std::env::var("DRAVE_GPU").is_err() { return None; }
drave-core/src/gpu.rs:1565:        if std::env::var("DRAVE_GPU").is_err() { return None; }
drave-core/src/clusters.rs:168:    match std::env::var("DRAVE_CLUSTERS") {
drave-core/src/model.rs:960:    if std::env::var("DRAVE_Q8_BLOCS").is_ok() && n_in % 32 == 0 {
drave-core/src/model.rs:1021:            let emprunt = keep >= 1.0 && std::env::var("DRAVE_SANS_EMPRUNT").is_err();
drave-core/src/model.rs:1028:            let emprunt = keep >= 1.0 && std::env::var("DRAVE_SANS_EMPRUNT").is_err();
drave-core/src/model.rs:1507:        let version: u16 = if std::env::var("DRAVE_TRACE_BLOCS").is_ok() { 3 } else { 2 };
drave-core/src/model.rs:2153:        let (k_f32, v_f32) = (std::env::var("DRAVE_KV_K_F32").is_ok(),
drave-core/src/model.rs:2154:                              std::env::var("DRAVE_KV_V_F32").is_ok());
drave-core/src/model.rs:2155:        l
… [2162 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Délégation des gros fichiers, lecture des petits en parallèle

- **subagent** `{"description": "Extract identifiers from formats.rs", "prompt": "Tu travailles dans le dépôt Rust /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM). LECTURE SEULE STRICTE : ne modifie aucun fichier.\n\nMISSION : extraire EXHAUSTIVEMENT d'UN SEUL fichier : dr … [2397 caractères tronqués]`
- **subagent** `{"description": "Extract identifiers from gguf.rs", "prompt": "Tu travailles dans le dépôt Rust /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM). LECTURE SEULE STRICTE : ne modifie aucun fichier.\n\nMISSION : extraire EXHAUSTIVEMENT d'UN SEUL fichier : drave … [2623 caractères tronqués]`
- **subagent** `{"description": "Extract identifiers from model.rs", "prompt": "Tu travailles dans le dépôt Rust /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM). LECTURE SEULE STRICTE : ne modifie aucun fichier.\n\nMISSION : extraire EXHAUSTIVEMENT d'UN SEUL fichier : drav … [3338 caractères tronqués]`

  ```
Error: subagent depth 4 exceeds maxDepth 3
  ```


  ```
Error: subagent depth 4 exceeds maxDepth 3
  ```


  ```
Error: subagent depth 4 exceeds maxDepth 3
  ```

### 🤖 Assistant

⏵ Délégation impossible (profondeur max) — extraction en direct

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/clusters.rs", "limit": 180}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/tokenizer.rs", "limit": 120}`

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
… [8316 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/tokenizer.rs</path>
<type>file</type>
<content>
1: //! Tokenizer BPE byte-level d'un modèle Qwen2.5, reconstruit depuis les
2: //! métadonnées GGUF (`tokenizer.ggml.tokens`, `.merges`, `.token_type`).
3: //!
4: //! Std seul : aucune dépendance. Chaîne de traitement, identique à celle de
5: //! Qwen2 / llama.cpp :
6: //!   1. découpage du texte par le pré-tokenizer, motif `qwen2` :
7: //!      `(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}`
8: //!      `| ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+`
9: //!      écrit à la main (l'ORDRE des alternatives et le lookahead `(?!\S)`
10: //!      font partie de la spécification) ;
11: //!   2. encodage byte-level de chaque morceau (table octet ↔ caractère de GPT-2) ;
12: //!   3. BPE : fusion répétée de la paire de rangs minimaux, puis conversion en ids.
13: //!
14: //! Les classes `\p{L}` et `\p{N}` sont approchées par `char::is_alphabetic()` et
15: //! `char::is_numeric()` : voir la nuance documentée sur `is_letter`.
16: //!
17: //! Vérification (hors dépôt, 737 cas : 300 lignes de wikitext2 avec et sans
18: //! retour à la ligne, cas pièges, plus 20
… [4859 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Poursuite de la lecture de clusters.rs et tokenizer.rs

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/clusters.rs", "offset": 181, "limit": 330}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/tokenizer.rs", "offset": 121, "limit": 390}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/clusters.rs</path>
<type>file</type>
<content>
181:     let gardes = gardes_du_milieu()?;
182:     ouvrir_interne(dossier, true, gardes.as_deref())
183: }
184: 
185: fn ouvrir_interne(dossier: &Path, meta_seule: bool, gardes: Option<&[usize]>)
186:     -> std::io::Result<Modele> {
187:     let commun = dossier.join("commun.gguf");
188:     if !commun.is_file() {
189:         return Err(std::io::Error::new(std::io::ErrorKind::NotFound,
190:             format!("{} : commun.gguf absent", dossier.display())));
191:     }
192:     // Le numéro de cluster est LU, jamais déduit du rang : un tri lexicographique
193:     // range « cluster-100 » avant « cluster-20 », et le préfixe `cl{c}/` porte ce
194:     // numéro. Confondre les deux ferait lire les experts d'un autre fichier —
195:     // mêmes formes, donc aucune erreur, juste un résultat faux.
196:     let mut clusters: Vec<(usize, PathBuf)> = Vec::new();
197:     for e in std::fs::read_dir(dossier)? {
198:         let p = e?.path();
199:         let n = p.file_name().and_then(|x| x.to_str()).unwrap_or("").to_string();
200:         let Some(num) = n.strip_prefix("cl
… [16147 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/tokenizer.rs</path>
<type>file</type>
<content>
121:     }
122: 
123:     #[allow(dead_code)] // fait partie de l'API demandée
124:     pub fn vocab_size(&self) -> usize {
125:         self.id_to_tok.len()
126:     }
127: 
128:     /// Id du token spécial à partir de sa chaîne (« <|im_end|> » -> 151645).
129:     ///
130:     /// Un token n'est « spécial » que si `token_type` le dit (3 = contrôle,
131:     /// 4 = défini par l'utilisateur). Si `token_type` ne couvre pas l'id
132:     /// (tableau vide ou tronqué), on renvoie l'id trouvé sans pouvoir trancher.
133:     /// Identifiant d'un jeton de contrôle, désigné par sa chaîne.
134:     ///
135:     /// Le type déclaré n'est pas décisif : le vocabulaire o200k range
136:     /// `<|start|>` et `<|message|>` parmi les jetons **ordinaires**. Exiger le
137:     /// type « contrôle » faisait donc échouer la détection du gabarit de
138:     /// gpt-oss et retomber sur une invite brute. On privilégie un jeton de
139:     /// contrôle, sinon on accepte n'importe quelle entrée portant exactement
140:     /// cette chaîne.
141:     pub fn special_id(&self, text: &str) -> 
… [15271 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de materiel.rs et repérage des littéraux

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/materiel.rs", "limit": 478}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/materiel.rs</path>
<type>file</type>
<content>
1: //! Détection du matériel et choix automatique de la configuration.
2: //!
3: //! Tout ce que ce module décide vient d'une **mesure**, pas d'une intuition.
4: //! Chaque heuristique porte le chiffre qui la justifie, et la commande
5: //! `--materiel` les affiche toutes avec leur raison — pour qu'un réglage
6: //! surprenant puisse être contesté.
7: //!
8: //! Les mesures de référence (session du 01/10, Xeon E5-2687W v3, 2 Quadro
9: //! RTX 5000, NVMe MAP1602) :
10: //!
11: //! | | |
12: //! |---|---|
13: //! | VRAM (noyau warp) | 84,9 Go/s |
14: //! | RAM, 20 cœurs physiques | 22,5 Go/s |
15: //! | RAM, 10 cœurs + leurs hyperthreads | 18,7 Go/s (+27 % sur 10 cœurs secs) |
16: //! | RAM, 20 cœurs + hyperthreads | 18,9 Go/s — **rien de plus** |
17: //! | NVMe, 1 lecteur | 5,4 Go/s |
18: //! | **NVMe, 16 lecteurs** | **31,1 Go/s** |
19: 
20: use std::path::Path;
21: use std::process::Command;
22: 
23: #[derive(Debug, Clone)]
24: pub struct Noeud {
25:     pub id: usize,
26:     pub cpus: Vec<usize>,
27:     pub memoire_go: f64,
28: }
29: 
30: #[derive(Debug, Clone)]
3
… [22523 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading '\"[a-zA-Z0-9_.:/<>|{}\\[\\] -]{2,}\"' drave-core/src/materiel.rs drave-core/src/clusters.rs drave-core/src/tokenizer.rs | head -120", "description": "Find string literals in small files"}`

  ```
drave-core/src/tokenizer.rs:77:        let motif_gpt4o = pre.starts_with("gpt-4o") || pre.starts_with("o200k");
drave-core/src/tokenizer.rs:175:            let merged = format!("{}{}", syms[i], syms[i + 1]);
drave-core/src/tokenizer.rs:202:        table[b as usize] = char::from_u32(c).expect("point de code valide");
drave-core/src/clusters.rs:59:                        "n_couches" => n_couches = v,
drave-core/src/clusters.rs:60:                        "n_experts" => n_experts = v,
drave-core/src/clusters.rs:61:                        "clusters" => n_clusters = v,
drave-core/src/clusters.rs:62:                        "experts_par_cluster" => par_cluster = v,
drave-core/src/clusters.rs:168:    match std::env::var("DRAVE_CLUSTERS") {
drave-core/src/clusters.rs:187:    let commun = dossier.join("commun.gguf");
drave-core/src/clusters.rs:190:            format!("{} : commun.gguf absent", dossier.display())));
drave-core/src/clusters.rs:200:        let Some(num) = n.strip_prefix("cluster-")
drave-core/src/clusters.rs:201:                          .and_then(|r| r.strip_suffix(".gguf")) else { continue };
drave-core/src/clusters.rs:213:    let mapping = Mapping::lire(&dossier.join("mapping
… [7151 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de gpu.rs (structs, constantes, littéraux)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs", "limit": 400}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs</path>
<type>file</type>
<content>
1: //! Chemin GPU : noyaux PTX chargés par l'API **pilote** de CUDA.
2: //!
3: //! Rien n'est lié à l'édition : le noyau est du PTX, compilé à la volée par le
4: //! pilote. Le programme ne dépend donc que de `libcuda.so`, présent avec
5: //! n'importe quel pilote NVIDIA — pas de boîte à outils CUDA à l'exécution.
6: //!
7: //! Principe de placement : **les poids restent sur le GPU**. Mesuré : PCIe x8
8: //! 6,5 Go/s contre 380 Go/s en lecture locale et 20 Go/s sur CPU. Déplacer les
9: //! poids à chaque jeton coûterait plus cher que de les lire sur CPU ; ne
10: //! traversent donc le bus que les activations (quelques kilo-octets) et le
11: //! résultat.
12: 
13: use std::ffi::c_void;
14: use std::os::raw::{c_char, c_int, c_uint};
15: 
16: #[link(name = "cuda")]
17: extern "C" {
18:     fn cuInit(flags: c_uint) -> c_int;
19:     fn cuDeviceGet(dev: *mut c_int, ordinal: c_int) -> c_int;
20:     fn cuDevicePrimaryCtxRetain(ctx: *mut *mut c_void, dev: c_int) -> c_int;
21:     fn cuCtxCreate_v2(ctx: *mut *mut c_void, flags: c_uint, dev: c_int) -> c_int;
22:     fn cuCtxSetCurr
… [19334 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading '\"[a-zA-Z0-9_.:/<>|{}\\[\\] -]{2,}\"' drave-core/src/gpu.rs | head -150", "description": "Find string literals in gpu.rs"}`

  ```
16:#[link(name = "cuda")]
40:const PTX: &str = include_str!("../gpu/drave_gpu.ptx");
198:            if rc != 0 { eprintln!("{}", erreur(rc, "cuInit")); return None; }
201:            if rc != 0 { eprintln!("{}", erreur(rc, "cuDeviceGet")); return None; }
208:                eprintln!("{}", erreur(rc, "cuCtxCreate"));
210:                if rc != 0 { eprintln!("{}", erreur(rc, "contexte")); return None; }
213:            if rc != 0 { eprintln!("{}", erreur(rc, "cuCtxSetCurrent")); return None; }
228:                eprintln!("{}", erreur(rc, "chargement du PTX"));
231:            let nom = std::ffi::CString::new("tete_q8").unwrap();
235:                eprintln!("{}", erreur(rc, "fonction tete_q8"));
238:            let nom_p = std::ffi::CString::new("proj_q8").unwrap();
242:                eprintln!("{}", erreur(rc, "fonction proj_q8"));
245:            let nom_tw = std::ffi::CString::new("tete_q8_warp").unwrap();
249:                eprintln!("{}", erreur(rc, "fonction tete_q8_warp"));
252:            let nom_pw = std::ffi::CString::new("proj_q8_warp").unwrap();
256:                eprintln!("{}", erreur(rc, "fonction proj_q8_warp"));
259:            let nom_mx = std::ffi::CStrin
… [4661 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la suite de gpu.rs et signatures publiques

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading '^\\s*(pub\\s+)?fn\\s+|^\\s*const\\s+|^\\s*static\\s+|^\\s*//\\s*---' drave-core/src/gpu.rs", "description": "List functions and consts in gpu.rs"}`

  ```
18:    fn cuInit(flags: c_uint) -> c_int;
19:    fn cuDeviceGet(dev: *mut c_int, ordinal: c_int) -> c_int;
20:    fn cuDevicePrimaryCtxRetain(ctx: *mut *mut c_void, dev: c_int) -> c_int;
21:    fn cuCtxCreate_v2(ctx: *mut *mut c_void, flags: c_uint, dev: c_int) -> c_int;
22:    fn cuCtxSetCurrent(ctx: *mut c_void) -> c_int;
23:    fn cuModuleLoadData(module: *mut *mut c_void, image: *const c_void) -> c_int;
24:    fn cuModuleGetFunction(f: *mut *mut c_void, module: *mut c_void, name: *const c_char) -> c_int;
25:    fn cuMemAlloc_v2(dptr: *mut u64, octets: usize) -> c_int;
26:    fn cuMemcpyHtoD_v2(dst: u64, src: *const c_void, octets: usize) -> c_int;
27:    fn cuMemcpyDtoH_v2(dst: *mut c_void, src: u64, octets: usize) -> c_int;
28:    fn cuMemcpyDtoD_v2(dst: u64, src: u64, octets: usize) -> c_int;
29:    fn cuLaunchKernel(f: *mut c_void, gx: c_uint, gy: c_uint, gz: c_uint,
33:    fn cuCtxSynchronize() -> c_int;
34:    fn cuMemFree_v2(dptr: u64) -> c_int;
35:    fn cuMemsetD32_v2(dst: u64, valeur: c_uint, n: usize) -> c_int;
36:    fn cuGetErrorName(code: c_int, nom: *mut *const c_char) -> c_int;
40:const PTX: &str = include_str!("../gpu/drave_gpu.ptx");
43:fn cu_ctx(ctx: *mut c_vo
… [2632 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs", "limit": 180, "offset": 1400}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs</path>
<type>file</type>
<content>
1400:             let partage = (n_in * 4) as c_uint;
1401:             let rc = cuLaunchKernel(self.f_mxfp4_warp, blocs.min(65535), 1, 1, fils, 1, 1,
1402:                                     partage, std::ptr::null_mut(),
1403:                                     params.as_mut_ptr(), std::ptr::null_mut());
1404:             if rc != 0 { eprintln!("{}", erreur(rc, "lancement proj_mxfp4_warp")); return None; }
1405:             if cuCtxSynchronize() != 0 { return None; }
1406:             let mut out = vec![0f32; m.n_out];
1407:             if cuMemcpyDtoH_v2(out.as_mut_ptr() as *mut c_void, m.out_dev, m.n_out * 4) != 0 {
1408:                 return None;
1409:             }
1410:             Some(out)
1411:         }
1412:     }
1413: 
1414:     /// Une passe de projection : le facteur d'échelle d'activation est appliqué
1415:     /// par le noyau, côté GPU.
1416:     pub fn proj(&self, m: &MatriceGpu, x: &[i32], sx: f32) -> Option<Vec<f32>> {
1417:         cu_ctx(self.ctx);
1418:         let n_in = m.nb * 32;
1419:         if x.len() < n_in { return None; }
1420:       
… [7969 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la section KV GPU (bits, capacités)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs", "limit": 165, "offset": 400}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs", "limit": 40, "offset": 810}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs</path>
<type>file</type>
<content>
400:         }
401:     }
402: 
403:     /// Réserve une matrice **Q4_K** (144 octets par super-bloc de 256 poids).
404:     pub fn charger_q4k(&self, blocs: &[u8], n_out: usize, nb: usize) -> Option<MatriceGpu> {
405:         cu_ctx(self.ctx);
406:         let octets_poids = n_out.checked_mul(nb)?.checked_mul(144)?;
407:         if blocs.len() < octets_poids { return None; }
408:         unsafe {
409:             let mut poids: u64 = 0;
410:             if cuMemAlloc_v2(&mut poids, octets_poids) != 0 { return None; }
411:             if cuMemcpyHtoD_v2(poids, blocs.as_ptr() as *const c_void, octets_poids) != 0 {
412:                 return None;
413:             }
414:             let mut x_dev: u64 = 0;
415:             cuMemAlloc_v2(&mut x_dev, nb * 256 * 4);
416:             let mut out_dev: u64 = 0;
417:             cuMemAlloc_v2(&mut out_dev, n_out * 4);
418:             Some(MatriceGpu { poids, x_dev, out_dev, n_out, nb, octets_poids })
419:         }
420:     }
421: 
422:     /// Réserve le cache KV d'une couche en VRAM. `None` si la VRAM manque :
423:     /// le m
… [8551 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs</path>
<type>file</type>
<content>
810:     /// contient, pour chaque ligne, les `k` indices **dans l'ordre du noyau** :
811:     /// d'abord ceux strictement au-dessus du seuil (indices croissants), puis les
812:     /// premiers égaux au seuil (indices croissants). Ce n'est PAS l'ordre
813:     /// croissant global, qui entrelace les deux groupes — mais c'est un ordre
814:     /// fixe et reproductible, et le même départage des ex æquo que le CPU.
815:     pub fn attn_topk_collecte(&self, m: &mut KvGpu, lignes: usize, n: usize, k: usize,
816:                               prefixes: &[u32], besoin: &[i32],
817:                               sortie: &mut [i32]) -> bool {
818:         cu_ctx(self.ctx);
819:         const CHUNK: usize = 4096;
820:         if lignes == 0 || n == 0 || k == 0 || k > n { return false; }
821:         if prefixes.len() < lignes || besoin.len() < lignes || sortie.len() < lignes * k {
822:             eprintln!("[topk] tampons hôtes trop courts pour la collecte");
823:             return false;
824:         }
825:         if m.scores_cap < lignes * n { return false; }
826:         le
… [1712 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Cartographie des tables type→taille dans gguf.rs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/Data13TB 2>/dev/null; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading 'GGML_|TAILLE_|match |=> ' drave-core/src/gguf.rs | sed -n '1,200p'", "description": "Locate GGML constants and match arms in gguf.rs"}`

  ```
95:    match std::env::var("DRAVE_PRELIRE") {
96:        Ok(v) => !(v == "0" || v.eq_ignore_ascii_case("non") || v.eq_ignore_ascii_case("false")),
97:        Err(_) => true,
143:        match self { Tampon::Lu(v) => v, Tampon::Mappe(m) => m }
156:    match std::env::var("DRAVE_MMAP") {
157:        Ok(v) => !(v == "0" || v.eq_ignore_ascii_case("non") || v.eq_ignore_ascii_case("false")),
158:        Err(_) => true,
167:        match Mappe::ouvrir(&f, len) {
168:            Ok(m) => return Ok(Tampon::Mappe(m)),
169:            Err(e) => eprintln!("[gguf] mmap refusé sur {} ({e}) : lecture complète",
191:        match self {
192:            Meta::Array(v) => v.iter().map(|m| m.as_u64().map(|x| x as i64)
193:                                           .or_else(|| match m { Meta::I64(x) => Some(*x), _ => None }))
195:            _ => None,
202:        match self {
203:            Meta::Array(v) => v.iter().map(|m| m.as_f64().map(|x| x as f32)
205:            _ => None,
210:        match self {
211:            Meta::U32(v) => Some(*v as u64),
212:            Meta::U64(v) => Some(*v),
213:            Meta::I32(v) => Some(*v as u64),
214:            Meta::I64(v) => Some(*v as u64),
215:     
… [9353 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture détaillée de l'en-tête de gguf.rs (enums, structs, constantes)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs", "limit": 345}`

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
11: use std::ops::Deref;
12: use std::path::Path;
13: 
14: /// Résultat empruntant à `self`. Écrit à la main parce qu'un tenseur peut vivre
15: /// dans n'importe lequel des fichiers de l'assemblage.
16: type io_result<'a> = std::io::Result<&'a [u8]>;
17: 
18: /// Fichier **mappé** en mémoire plutôt que lu.
19: ///
20: /// `read_to_end` fait deux choses coûteuses : il lit tout le fichier (18,55 Go
21: /// pour Qwen3-30B, 366 Go pour DeepSeek-V4.1-Flash) et il en garde une copie
22: /// dans le tas, en plus du cache de pages du noyau — soit deux fois la taille du
23: /// modèle en mémoire physique au premier accès.
24: ///
25: /// Le mmap ne lit rien : il rend une plage d'adre
… [13543 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction des tables de correspondance gguf.rs (lignes 740-880)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs", "limit": 160, "offset": 740}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs</path>
<type>file</type>
<content>
740:     /// tenseurs d'experts en `iq1_m` n'étaient pas dans la table.
741:     pub fn octets_tensor(t: &TensorInfo) -> u64 {
742:         if let Some(v) = Self::octets_tensor_opt(t) { return v; }
743:         // Un type hors table est compté zéro : le total serait faux, et c'est
744:         // ainsi qu'un inventaire a annoncé 8,56 Go pour 86,9 Go de fichiers
745:         // (les tenseurs d'experts en `iq1_m` n'étaient pas dans la table). On le
746:         // dit, une fois par type, plutôt que de rendre un chiffre trop petit.
747:         static SIGNALES: std::sync::Mutex<Vec<u32>> = std::sync::Mutex::new(Vec::new());
748:         if let Ok(mut v) = SIGNALES.lock() {
749:             if !v.contains(&t.ttype) {
750:                 v.push(t.ttype);
751:                 eprintln!("[gguf] type {} inconnu (tenseur « {} ») : sa taille compte pour \
752: zéro, l'inventaire sera sous-évalué", t.ttype, t.name);
753:             }
754:         }
755:         0
756:     }
757: 
758:     /// Taille d'un tenseur, ou `None` si son type n'est pas dans la table.
759:     pub fn octet
… [7606 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading '\"[a-z_]+\\.[a-z_.0-9]+\"' drave-core/src/gguf.rs | head -80", "description": "Find GGUF metadata key literals"}`

  ```
496:            if m.contains_key("general.architecture") {
498:                    None => arch_ref = m.get("general.architecture")
501:                        let ici = m.get("general.architecture").and_then(|v| v.as_str());
608:            if !p.join("commun.gguf").is_file() {
671:            if m.contains_key("general.architecture") {
673:                    None => arch_ref = m.get("general.architecture")
676:                        let ici = m.get("general.architecture").and_then(|v| v.as_str());
880:        let align = meta.get("general.alignment").and_then(|m| m.as_u64()).unwrap_or(32) as usize;
885:        let arch = self.meta.get("general.architecture")?.as_str()?;
904:        self.cfg_ou(&["attention.compress_ratios", "compress_ratios"])
914:        self.cfg_ou(&["attention.compress_ratios", "compress_ratios"])
933:        let mult = entier(&["hyper_connection.count"], "hc_mult")?;
934:        let iters = entier(&["hyper_connection.sinkhorn_iterations"], "hc_sinkhorn_iters")
936:        let eps = self.cfg_ou(&["hyper_connection.epsilon"]).and_then(|m| m.as_f64())
1819:        s(&mut b, "general.architecture");
1822:        s(&mut b, "essai.config");
1826:        let chem
… [1449 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Clés de configuration GGUF et début de formats.rs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading 'cfg_ou\\(|\\.cfg\\(\"|cfg\\(&|\"[a-z_0-9]+\\.[a-z_0-9.]+\"' drave-core/src/gguf.rs | sed -n '1,60p'; echo \"=== FONCTIONS GGUF ===\"; rg -n --no-heading '^\\s*pub fn |^\\s*fn ' drave-core/src/gguf.rs", "descriptio … [45 caractères tronqués]`

  ```
496:            if m.contains_key("general.architecture") {
498:                    None => arch_ref = m.get("general.architecture")
501:                        let ici = m.get("general.architecture").and_then(|v| v.as_str());
608:            if !p.join("commun.gguf").is_file() {
671:            if m.contains_key("general.architecture") {
673:                    None => arch_ref = m.get("general.architecture")
676:                        let ici = m.get("general.architecture").and_then(|v| v.as_str());
880:        let align = meta.get("general.alignment").and_then(|m| m.as_u64()).unwrap_or(32) as usize;
884:    pub fn cfg(&self, key: &str) -> Option<&Meta> {
885:        let arch = self.meta.get("general.architecture")?.as_str()?;
898:    pub fn cfg_ou(&self, cles: &[&str]) -> Option<&Meta> {
904:        self.cfg_ou(&["attention.compress_ratios", "compress_ratios"])
914:        self.cfg_ou(&["attention.compress_ratios", "compress_ratios"])
930:            self.cfg_ou(cles).and_then(|m| m.as_u64()).map(|v| v as usize)
933:        let mult = entier(&["hyper_connection.count"], "hc_mult")?;
934:        let iters = entier(&["hyper_connection.sinkhorn_iterations"], "hc_sinkhorn_iters")
9
… [8961 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Cartographie de formats.rs (tables, statiques, fonctions)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading '^\\s*(pub\\s+)?(fn|const|static|struct|enum|type|mod)\\s+|^\\s*//\\s*={3,}|^// ---' drave-core/src/formats.rs", "description": "List top-level items in formats.rs"}`

  ```
19:pub static IQ2XXS_GRID: [[u8; 8]; 256] = [
278:pub static KSIGNS_IQ2XS: [u8; 128] = [
299:pub fn dequant_iq4xs_dans(bloc: &[u8], out: &mut [f32]) {
320:pub fn dequant_iq4xs(bloc: &[u8]) -> Vec<f32> {
334:pub fn dequant_iq1s_dans(bloc: &[u8], out: &mut [f32]) {
355:pub fn dequant_iq1s(bloc: &[u8]) -> Vec<f32> {
368:pub fn dequant_iq2xxs_dans(bloc: &[u8], out: &mut [f32]) {
396:pub fn dequant_iq2xxs(bloc: &[u8]) -> Vec<f32> {
414:pub fn dequant_iq3xxs_dans(bloc: &[u8], out: &mut [f32]) {
440:pub fn dequant_iq3xxs(bloc: &[u8]) -> Vec<f32> {
447:pub static IQ1S_GRID: [[i8; 8]; 2048] = [
2499:pub static KVALS_IQ4NL: [i8; 16] = [
2504:pub static IQ3XXS_GRID: [[u8; 4]; 256] = [
2766:const IQ1S_DELTA: f32 = 0.125;
2775:pub fn dequant_iq1m_dans(bloc: &[u8], out: &mut [f32]) {
2822:pub fn dequant_iq1m(bloc: &[u8]) -> Vec<f32> {
2829:mod tests {
2833:    fn iq2xxs_taille_et_plausibilite() {
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs", "limit": 70, "offset": 899}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs</path>
<type>file</type>
<content>
899:         cles.iter().find_map(|c| self.cfg(c))
900:     }
901: 
902:     /// Les ratios de compression, **couche par couche** (0 = brute).
903:     pub fn couches_ratios(&self) -> Vec<i64> {
904:         self.cfg_ou(&["attention.compress_ratios", "compress_ratios"])
905:             .and_then(|m| m.as_liste_i64())
906:             .unwrap_or_default()
907:     }
908: 
909:     /// **Quelles couches ont une attention compressée** (`attention.compress_ratios`
910:     /// ≠ 0). C'est ce qui décide si une exécution BORNÉE est légitime : les
911:     /// couches 0 et 1 de V4-Flash n'en ont pas, donc on peut les exécuter —
912:     /// et les comparer à la référence — avant que la compression existe.
913:     pub fn couches_compressees(&self) -> Vec<usize> {
914:         self.cfg_ou(&["attention.compress_ratios", "compress_ratios"])
915:             .and_then(|m| m.as_liste_i64())
916:             .map(|v| v.iter().enumerate().filter(|(_, r)| **r != 0).map(|(i, _)| i).collect())
917:             .unwrap_or_default()
918:     }
919: 
920:     /// Les trois hyper-paramètres 
… [2754 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction des fonctions de déquantification dans formats.rs

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/formats.rs", "limit": 75, "offset": 1}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/formats.rs", "limit": 170, "offset": 296}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/formats.rs</path>
<type>file</type>
<content>
1: //! Déquantification des formats **non triviaux** : ceux qui reposent sur une
2: //! grille de codes plutôt que sur des échelles.
3: //!
4: //! Les formats « simples » (Q4_0, Q8_0, Q4_K, Q6_K, Q2_K, MXFP4) vivent dans
5: //! `gguf.rs`, à côté du lecteur. Ceux-ci ont besoin d'une table de constantes, et
6: //! la table doit être **extraite**, pas recopiée : une seule valeur fausse
7: //! ruinerait les 93 Go d'experts de DeepSeek-V4.1 en IQ2_XXS.
8: //!
9: //! Les tables viennent de `ggml-common.h` par un petit programme C qui les
10: //! imprime (`tools/extraire_tables_ggml.sh`). La vérification se fait contre
11: //! `libggml` elle-même : on déquantifie le même bloc des deux côtés et on
12: //! compare.
13: 
14: /// Grille d'IQ2_XXS : 256 codes de 8 niveaux. Chaque code est un u64 dont les
15: /// octets sont les huit niveaux.
16: // Tables extraites de ggml-common.h par programme, jamais recopiees a
17: // la main : une seule valeur fausse ruinerait 93 Go de poids.
18: 
19: pub static IQ2XXS_GRID: [[u8; 8]; 256] = [
20:     [8,8,8,8,8,8,8,8,],
21:     [43,8,8,8,8,8
… [1733 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/formats.rs</path>
<type>file</type>
<content>
296: /// **index** dans la table `kvalues_iq4nl` (−127 … 113), pas une valeur : c'est
297: /// une quantification non linéaire, et la lire comme un entier 4 bits donne des
298: /// poids faux d'un facteur qui dépend du niveau.
299: pub fn dequant_iq4xs_dans(bloc: &[u8], out: &mut [f32]) {
300:     assert!(bloc.len() >= 136, "bloc IQ4_XS trop court : {}", bloc.len());
301:     let d = crate::gguf::Gguf::f16_to_f32(u16::from_le_bytes([bloc[0], bloc[1]]));
302:     let scales_h = u16::from_le_bytes([bloc[2], bloc[3]]);
303:     let scales_l = &bloc[4..8];
304:     let qs = &bloc[8..136];
305:     assert!(out.len() >= 256, "tampon de sortie trop court : {}", out.len());
306:     for ib in 0..8usize {
307:         let ls = (((scales_l[ib / 2] >> (4 * (ib % 2))) & 0x0F) as i32
308:                   | ((((scales_h >> (2 * ib)) & 3) as i32) << 4)) - 32;
309:         let dl = d * ls as f32;
310:         for j in 0..16usize {
311:             let octet = qs[16 * ib + j];
312:             out[32 * ib + j] = dl * KVALS_IQ4NL[(octet & 0x0F) as usize] as f32;
313:             out[3
… [7301 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Fin de formats.rs : tables IQ4NL/IQ3XXS, IQ1S_DELTA, IQ1_M

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/formats.rs", "limit": 130, "offset": 2486}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/formats.rs", "limit": 90, "offset": 2758}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/formats.rs</path>
<type>file</type>
<content>
2486:     [1,0,0,0,1,1,1,1,],
2487:     [-1,-1,-1,1,1,1,1,1,],
2488:     [1,-1,-1,1,1,1,1,1,],
2489:     [-1,1,-1,1,1,1,1,1,],
2490:     [1,1,-1,1,1,1,1,1,],
2491:     [0,0,0,1,1,1,1,1,],
2492:     [-1,-1,1,1,1,1,1,1,],
2493:     [1,-1,1,1,1,1,1,1,],
2494:     [-1,1,1,1,1,1,1,1,],
2495:     [1,1,1,1,1,1,1,1,],
2496: ];
2497: 
2498: // Niveaux d'IQ4_NL et IQ4_XS : 16 valeurs signées (extraites de ggml-common.h).
2499: pub static KVALS_IQ4NL: [i8; 16] = [
2500:     -127,-104,-83,-65,-49,-35,-22,-10,1,13,25,38,53,69,89,113,
2501: ];
2502: 
2503: // Grille IQ3_XXS : 256 codes de 4 octets (extraits de ggml-common.h).
2504: pub static IQ3XXS_GRID: [[u8; 4]; 256] = [
2505:     [4,4,4,4,],
2506:     [20,4,4,4,],
2507:     [36,4,4,4,],
2508:     [12,12,4,4,],
2509:     [28,12,4,4,],
2510:     [62,12,4,4,],
2511:     [4,20,4,4,],
2512:     [20,20,4,4,],
2513:     [12,28,4,4,],
2514:     [20,36,4,4,],
2515:     [28,62,4,4,],
2516:     [44,62,4,4,],
2517:     [12,4,12,4,],
2518:     [28,4,12,4,],
2519:     [4,12,12,4,],
2520:     [20,12,12,4,],
2521:     [12,20,12,4,],
2522:     [
… [2402 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/formats.rs</path>
<type>file</type>
<content>
2758:     [20,4,44,62,],
2759:     [36,20,44,62,],
2760:     [4,28,52,62,],
2761: ];
2762: 
2763: 
2764: 
2765: /// `IQ1S_DELTA` de ggml : le décalage appliqué à chaque niveau de la grille.
2766: const IQ1S_DELTA: f32 = 0.125;
2767: 
2768: /// Déquantifie un bloc **IQ1_M** (56 octets, 256 poids).
2769: ///
2770: /// Structure : 8 octets d'échelles entrelacées, 32 octets d'index de grille (les
2771: /// 8 bits bas), 16 octets de bits hauts d'index **et** de bits de décalage.
2772: /// Trois bits d'échelle par sous-bloc de 16, un bit de signe du décalage.
2773: ///
2774: /// `x = d·(2·e+1)·(grille + ±0,125)`
2775: pub fn dequant_iq1m_dans(bloc: &[u8], out: &mut [f32]) {
2776:     assert!(bloc.len() >= 56, "bloc IQ1_M trop court : {}", bloc.len());
2777:     // L'ORDRE des champs est `qs[32]`, `qh[16]`, `scales[8]` — les échelles sont
2778:     // EN DERNIER. Les lire en premier donnait une échelle absurde et un écart de
2779:     // 2,4e5 : c'est la comparaison avec ggml qui l'a montré.
2780:     let sc: [u16; 4] = [
2781:         u16::from_le_bytes([bloc[48], bloc[49]])
… [3015 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Repérage des littéraux et tables de types dans model.rs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading '\"[a-zA-Z0-9_./<>|{}=\\[\\] -]{2,}\"' drave-core/src/model.rs | head -170", "description": "Find string literals in model.rs"}`

  ```
59:            Gating::Softmax => "softmax",
62:            Gating::SqrtSoftplus => "racine de softplus",
99:    if quelque_part("hc_attn_fn.weight") && g.hc_params().is_none() {
106:    if quelque_part("indexer.") {
111:        let topk = g.cfg_ou(&["attention.indexer.top_k", "index_topk", "indexer.top_k"])
113:            .or_else(|| g.json_nombre("index_topk").map(|v| v as u64))
123:    if quelque_part("engram_embd.weight") || quelque_part("engram.weight")
124:        || g.cfg("engram.layer_ids").is_some() || g.json_brut("engram_layer_ids").is_some() {
132:    if quelque_part("attn_output_a.weight") && !quelque_part("attn_kv.weight") {
151:    if quelque_part("attn_derope") {
164:    if (g.cfg_ou(&["attention.compress_ratios", "compress_ratios"]).is_some()
165:        || g.json_brut("compress_ratios").is_some())
166:        && !quelque_part("attn_compressor_kv.weight") {
172:    if quelque_part("attn_q_a.weight") && quelque_part("attn_kv_a_mqa.weight") {
194:            g.meta.get("general.architecture").and_then(|m| m.as_str()).unwrap_or("?"),
196:            if g.tensors.iter().any(|t| t.name.ends_with("attn_q_a.weight")) { "attn_q_a " } else { "" },
197:            if g.tenso
… [12348 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading 'ttype|q4_k|q6_k|mxfp4|ggml|GGML|type_de|\"iq|\"q[0-9]' drave-core/src/model.rs | head -80", "description": "Find quant type handling in model.rs"}`

  ```
482:/// Type ggml → origine des blocs pour `Vue4`.
484:    use crate::gguf::{GGML_IQ1_M, GGML_IQ1_S, GGML_IQ2_XXS, GGML_IQ3_XXS,
485:                      GGML_MXFP4, GGML_Q4_0, GGML_Q4_K, GGML_Q6_K};
488:        GGML_Q4_K => Some(Source::Q4_K),
489:        GGML_Q6_K => Some(Source::Q6_K),
490:        GGML_MXFP4 => Some(Source::Mxfp4),
491:        GGML_Q4_0 => Some(Source::Q4_0),
565:            let Some(src) = source_de(t.ttype) else {
566:                eprintln!("[moe] couche {l} : « {nom} » de type {} — format sans noyau ni déquantification", crate::gguf::Gguf::nom_type(t.ttype));
570:            let bloc = if t.ttype == crate::gguf::GGML_Q4_K || t.ttype == crate::gguf::GGML_Q6_K { 256 } else { 32 };
592:        let src = source_de(t.ttype)?;
598:        let bloc = if t.ttype == crate::gguf::GGML_Q4_K || t.ttype == crate::gguf::GGML_Q6_K { 256 } else { 32 };
1008:            } else if let Some((buf, nb)) = g.mxfp4_blocks(name) {
1119:            let mg = machine.charger_mxfp4(gate.blocs_expert(e), gate.n_out, gate.nb)?;
1120:            let mu = machine.charger_mxfp4(up.blocs_expert(e), up.n_out, up.nb)?;
1121:            let md = machine.charger_mxfp4(down.blocs_expert(e), do
… [1425 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des enums et structs de model.rs (lots 1-3)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 70, "offset": 20}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 90, "offset": 240}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 120, "offset": 410}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
20: 
21: // --------------------------------------------------------------------------- //
22: // Configuration
23: // --------------------------------------------------------------------------- //
24: 
25: /// Convention de routage des experts — quatre familles, et une seule
26: /// implémentation partagée par le jeton seul et le lot (voir [`router`]).
27: #[derive(Clone, Copy, PartialEq, Eq, Debug)]
28: pub enum Gating {
29:     /// `softmax` sur TOUS les logits, top-k, renormalisation. Qwen3-MoE, et le
30:     /// défaut de llama.cpp quand un modèle ne déclare rien.
31:     Softmax,
32:     /// `sigmoid` sur chaque logit, top-k sur ces scores, renormalisation.
33:     /// Kimi-K2.7 (`expert_gating_func = 2`), GLM-5.3 et GLM-5.3-Flash.
34:     Sigmoid,
35:     /// Top-k sur les logits **bruts** (plus le biais de sélection s'il existe),
36:     /// puis `softmax` sur les seuls k retenus — et **pas** de renormalisation
37:     /// ensuite, le softmax s'en charge. gpt-oss.
38:     SoftmaxPoids,
39:     /// `sqrt(softplus(x)) = sqrt(log(1+e^x))` sur chaque logit, top-k,
40
… [2577 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
240: /// le moteur. Les quatre ne se valent pas — un défaut est une hypothèse, et le
241: /// mode `--config` la montre comme telle.
242: pub struct Routage {
243:     pub n_expert: usize,
244:     pub n_expert_used: usize,
245:     pub ffn_exp: usize,
246:     pub gating: Gating,
247:     /// D'où vient `gating` : `expert_gating_func`, le JSON, ou le défaut.
248:     pub source: &'static str,
249:     pub norm: bool,
250:     pub echelle: f32,
251:     pub hash_layers: usize,
252: }
253: 
254: /// Lit la convention de routage des experts — **une seule fois, à un seul
255: /// endroit** : le chargement du modèle et le mode `--config` appellent ceci.
256: pub fn routage_du_gguf(g: &Gguf) -> Routage {
257:     let arch = g.meta.get("general.architecture").and_then(|m| m.as_str())
258:                    .unwrap_or("").to_string();
259:     // Trois sources, dans cet ordre : la clef normalisée du GGUF, le nom
260:     // d'origine de DeepSeek, puis le JSON `<arch>.config` recopié par le
261:     // convertisseur. V4.1-Flash-Q2 n'a QUE la troisième : sans elle, il était
262:
… [3983 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
410:         for v in poids.iter_mut() { *v *= cfg.expert_scale; }
411:     }
412:     let _ = &mut probs;
413:     chosis.into_iter().zip(poids).collect()
414: }
415: 
416: pub struct Cfg {
417:     pub n_layer: usize,
418:     pub hidden: usize,
419:     pub n_head: usize,
420:     pub n_kv_head: usize,
421:     pub head_dim: usize,
422:     pub ffn: usize,
423:     pub eps: f32,
424:     pub rope_base: f32,
425:     pub vocab: usize,
426:     /// MoE : nombre d'experts, combien sont allumés par jeton, et leur taille
427:     /// intermédiaire. `n_expert = 0` pour un modèle dense.
428:     pub n_expert: usize,
429:     pub n_expert_used: usize,
430:     pub ffn_exp: usize,
431:     /// Activation du FFN. gpt-oss n'utilise **pas** SiLU : c'est
432:     /// `g·σ(1,702·g)·(u+1)`, avec `g` et `u` écrêtés à ±7 — une sigmoïde
433:     /// rapide de type GELU, et un décalage de `up` de +1. Prendre SiLU par
434:     /// défaut donne une perplexité de 1 396 au lieu de la bonne.
435:     pub ffn_act_oss: bool,
436:     /// Convention de routage des experts (voir [`Gating`]).
437
… [5590 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des structs de model.rs (lots 4-6)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 60, "offset": 686}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 150, "offset": 818}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 30, "offset": 1070}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
686: 
687: /// Vue sur un tenseur déjà quantifié, découpable **par expert**. Les experts
688: /// sont empilés dans un tenseur 3D et **contigus** : l'expert `e` commence à
689: /// `base + e × n_out × nb × pas`. Aucune copie, aucun découpage préalable.
690: #[derive(Clone, Copy)]
691: pub struct Vue4 {
692:     pub base: *const u8,
693:     pub n_out: usize,
694:     pub n_in: usize,
695:     pub nb: usize,
696:     pub src: crate::list::Source,
697: }
698: 
699: impl Vue4 {
700:     fn pas(&self) -> usize {
701:         use crate::list::Source::*;
702:         match self.src {
703:             Q4_K => crate::gguf::TAILLE_Q4K,
704:             Q6_K => crate::gguf::TAILLE_Q6K,
705:             Mxfp4 => 17,
706:             Q4_0 => 18,
707:             Propre => 0,
708:             Dequant(t) => crate::list::octets_grille(t),
709:         }
710:     }
711: 
712:     /// Produit matrice-vecteur sur une source **sans noyau** : déquantifie
713:     /// chaque super-bloc de 256 poids et accumule en f32.
714:     ///
715:     /// Le travail est découpé par LIGNES de sortie entr
… [2163 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
818: unsafe impl Sync for Vue4 {}
819: 
820: /// Mélange d'experts : un routeur (petit, en f32) et trois tenseurs empilés.
821: pub struct Moe {
822:     /// Routeur `[n_expert × n_embd]`, rangée par expert, en f32.
823:     pub routeur: Vec<f32>,
824:     /// Biais du routeur (gpt-oss en a un) : ajouté aux logits **avant** le
825:     /// softmax.
826:     pub routeur_biais: Option<Vec<f32>>,
827:     /// Biais par expert, `[n_expert × n_ff]` : chaque expert a les siens, pour
828:     /// ses trois projections. Absents chez Qwen3-MoE, présents chez gpt-oss.
829:     pub biais_gate: Option<Vec<f32>>,
830:     pub biais_up: Option<Vec<f32>>,
831:     pub biais_down: Option<Vec<f32>>,
832:     pub n_ff: usize,
833:     /// Une vue par fichier porteur d'experts. Un GGUF ordinaire n'en a qu'une ;
834:     /// un modèle en clusters en a une par `cluster-XX.gguf`, chacune ne
835:     /// contenant que ses `experts_par_cluster` lignes.
836:     pub gate: Vec<Vue4>,
837:     pub up: Vec<Vue4>,
838:     pub down: Vec<Vue4>,
839:     /// Couche dont ce mélange fait partie (pour le
… [5986 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
1070: /// (`reports/rapport-localite-activation.md`) dit qu'un préchargement STATIQUE
1071: /// ne paie pas ; une résidence dynamique, si.
1072: pub struct CacheExperts {
1073:     /// Une entrée par (couche, expert) : ses trois matrices (gate, up, down).
1074:     cartes: std::collections::HashMap<(usize, usize), (crate::gpu::MatriceGpu,
1075:                                                        crate::gpu::MatriceGpu,
1076:                                                        crate::gpu::MatriceGpu, u64)>,
1077:     pub octets: usize,
1078:     pub budget: usize,
1079:     pub demandes: u64,
1080:     pub manques: u64,
1081:     pub evictions: u64,
1082:     pub octets_envoyes: u64,
1083:     ticks: u64,
1084: }
1085: 
1086: impl CacheExperts {
1087:     pub fn nouveau(budget: usize) -> Self {
1088:         CacheExperts { cartes: std::collections::HashMap::new(), octets: 0, budget,
1089:                        demandes: 0, manques: 0, evictions: 0, octets_envoyes: 0, ticks: 0 }
1090:     }
1091: 
1092:     pub fn taux(&self) -> f64 {
1093:         if self.demandes 
… [515 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des structs MLA/hyper-connexions de model.rs

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 175, "offset": 1145}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 110, "offset": 1400}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
1145: /// * la sortie subit une **dé-rotation** (`ggml_rope_ext_back`) avant d'être
1146: ///   projetée par groupes : `attn_output_a` par groupe de `nh/o_groups` têtes,
1147: ///   puis `attn_output_b` sur les groupes concaténés ;
1148: /// * les puits appris (`attn_sinks`, un par tête) entrent dans le **softmax**.
1149: pub struct Mla4 {
1150:     pub q_a: Vec<f32>,      // [q_lora × h]
1151:     pub q_a_norm: Vec<f32>, // [q_lora]
1152:     pub q_b: Vec<f32>,      // [nh·head_dim × q_lora]
1153:     pub kv: Vec<f32>,       // [head_dim × h]
1154:     pub kv_norm: Vec<f32>,  // [head_dim]
1155:     pub wo_a: Vec<f32>,     // [o_lora·n_groups × (nh/n_groups)·head_dim], par groupe
1156:     pub wo_b: Vec<f32>,     // [h × o_lora·n_groups]
1157:     pub sinks: Vec<f32>,    // [nh]
1158:     pub nh: usize,
1159:     pub h: usize,
1160:     pub head_dim: usize,
1161:     pub rope: usize,
1162:     pub n_groups: usize,
1163:     pub o_lora: usize,
1164:     pub rope_base: f32,
1165:     pub eps: f32,
1166:     /// Ratio de compression de la couche (`attention.compress_ratios
… [8015 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
1400:     }
1401: }
1402: 
1403: /// MLA (attention latente) : les poids d'une couche, lus en f32. Le cache n'est
1404: /// PAS `(n_kv, ctx, head_dim)` mais **une seule tête latente** par couche —
1405: /// `kv_lora` valeurs, plus les `qk_rope` composantes tournées. C'est tout
1406: /// l'intérêt de MLA : le cache ne dépend plus du nombre de têtes.
1407: pub struct Mla {
1408:     pub q_a: Vec<f32>,      // [h, q_lora]
1409:     pub q_a_norm: Vec<f32>, // [q_lora]
1410:     pub q_b: Vec<f32>,      // [q_lora, nh*(qkn+qkr)]
1411:     pub kv_a: Vec<f32>,     // [h, kv_lora+qkr]
1412:     pub kv_a_norm: Vec<f32>,// [kv_lora]
1413:     /// Disposition **combinée** : `[kv_lora, nh*(qkn+vd)]`, une matrice par
1414:     /// tête concaténée. Vide quand le modèle utilise la disposition séparée
1415:     /// (`attn_k_b` + `attn_v_b`), qui est celle de Kimi-K2.7 et DeepSeek-V3/V4.
1416:     pub kv_b: Vec<f32>,
1417:     /// Disposition **séparée** : `k_b` `[nh, kv_lora, qkn]` et `v_b`
1418:     /// `[nh, kv_lora, vd]` (convention numpy, le plus lent d'abord).
1419:     pub k_b: Opt
… [4613 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des structs Model, Patch, Hebb, KvCache

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 40, "offset": 1618}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 130, "offset": 1750}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 115, "offset": 2020}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
1618: /// recevoir pour continuer le calcul, on sait déjà l'écrire — ici, on apprend à
1619: /// le RELIRE et à repartir de là.
1620: pub struct FluxRelecteur {
1621:     /// (couche, position) -> (échelle, indices/valeurs)
1622:     /// (couche, jeton global) → (échelle, paires) pour les versions 1 et 2 : les
1623:     /// ENTIERS d'origine sont conservés, parce que le rejeu par LOTS les réinjecte
1624:     /// tels quels (chemin exact, sans déquantifier-requantifier).
1625:     pub listes: std::collections::HashMap<(u16, u32), (f32, Vec<(u32, i16)>)>,
1626:     /// Version 3 : les valeurs sont des f32 (i8 × échelle f16 de bloc), il n'y a
1627:     /// plus d'entiers d'origine. Le rejeu JETON PAR JETON les accepte ; le rejeu
1628:     /// par lots, non — et il le dira au lieu de compter des listes manquantes
1629:     /// sans explication.
1630:     pub listes_blocs: std::collections::HashMap<(u16, u32), Vec<(u32, f32)>>,
1631:     pub servies: u64,
1632:     pub manquantes: u64,
1633: }
1634: 
1635: impl FluxRelecteur {
1636:     pub fn lire(chemin: &str) -> std::io::R
… [1379 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
1750:             None => self.manquantes += 1,
1751:         }
1752:     }
1753: }
1754: 
1755: pub struct Model {
1756:     pub g: Gguf,
1757:     pub cfg: Cfg,
1758:     pub layers: Vec<Layer>,
1759:     pub out_norm: Vec<f32>,
1760:     pub pool: Pool,
1761:     /// cache KV, par couche : `[n_kv_head × ctx × head_dim]`, en f32 ou quantifié
1762:     /// Caches KV, un par couche (pub : le tableau de bord `--options-actives`
1763:     /// montre ce que le moteur utilise vraiment — et c'est là qu'on voit si
1764:     /// `DRAVE_KV_K_F32` ou `DRAVE_KV_K_F16` a réellement pris).
1765:     pub kv: Vec<KvCache>,
1766:     pub ctx: usize,
1767:     pub events: u64,
1768:     /// **Paires** (poids × activation) effectivement multipliées, par
1769:     /// provenance : 0 = attention, 1 = experts routés, 2 = partagé (FFN dense,
1770:     /// expert partagé, tête).
1771:     ///
1772:     /// Pourquoi une seconde mesure à côté des `events` : les chemins qui
1773:     /// **déquantifient** (IQ, formats sans noyau) et le chemin MLA en f32 ne
1774:     /// construisent aucune liste
… [7221 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
2020: /// réseau n'a jamais calculée — les 4 864 neurones d'origine n'apparient que
2021: /// `gate[i]` avec `up[i]`.
2022: ///
2023: /// Format binaire du fichier (little-endian) :
2024: ///   magie "QPAT" | version u32 | couche u32 | n u32 | n f32 (u) | n f32 (v) | n f32 (d)
2025: pub struct Patch {
2026:     pub layer: usize,
2027:     pub u: Vec<f32>,
2028:     pub v: Vec<f32>,
2029:     pub d: Vec<f32>,
2030: }
2031: 
2032: impl Patch {
2033:     pub fn load(path: &str) -> std::io::Result<Patch> {
2034:         use std::io::Read;
2035:         let mut buf = Vec::new();
2036:         std::fs::File::open(path)?.read_to_end(&mut buf)?;
2037:         if buf.len() < 16 || &buf[0..4] != b"QPAT" {
2038:             return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, "magie QPAT absente"));
2039:         }
2040:         let g = |o: usize| u32::from_le_bytes(buf[o..o+4].try_into().unwrap()) as usize;
2041:         let (layer, n) = (g(8), g(12));
2042:         let f = |base: usize| (0..n).map(|i| {
2043:             let o = base + 4*i;
2044:             f32::from_
… [4811 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Fin de Model/KvCache et valeurs des constantes clés

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 142, "offset": 1880}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
1880:     /// Chemin GPU : la tête et les projections y résident en permanence. Les
1881:     /// poids ne traversent le bus qu'une fois ; seules les activations font
1882:     /// l'aller-retour à chaque jeton.
1883:     pub tete_gpu: Option<crate::gpu::MatriceGpu>,
1884:     /// Tête de sortie en 4 bits (poids liés au plafond d'embedding). C'est la
1885:     /// plus grosse matrice du modèle — 151 936 × 896 — donc le poste où le
1886:     /// demi-octet par poids rapporte le plus.
1887:     pub head4: Option<DenseQ4>,
1888:     /// Tokens sur lesquels la tête de sortie est calculée. `None` = tout le
1889:     /// vocabulaire.
1890:     ///
1891:     /// Mesuré : le vocabulaire d'une langue tient en **13 %** des tokens (19 793
1892:     /// sur 151 936 pour 3 M de jetons français, et la couverture croît si
1893:     /// lentement qu'atteindre 50 % demanderait des milliards de jetons). La tête
1894:     /// pèse par ailleurs 36 % du trafic par jeton sur V4.1. Restreindre la boucle
1895:     /// aux lignes utiles divise donc ce poste par sept.
1896:     ///
1897:     /// 
… [8369 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for l in 1045 2430 2439 2463 3510 3648 5530 5968 6128 6555 6730 6770 6786 6790 6796 6800; do echo \"--- $l ---\"; sed -n \"${l},$((l+12))p\" drave-core/src/model.rs; done", "description": "Show context of model.rs constants"}`

  ```
--- 1045 ---
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
--- 2430 ---
}

/// Un seul message pour un échec de la chaîne top-k déportée, quel que soit le
/// nombre de couches et de jetons (voir la branche `DRAVE_GPU_TOPK`).
static TOPK_GPU_ECHEC: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);

/// Densité de l'entrée de la tête, mesurée sur tous les appels. Sert à décider
/// si un stockage par COL
… [11000 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification exhaustive : enums, env, littéraux restants

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== TOUS LES 'enum' (insensible casse) ===\"; rg -ni --no-heading '\\benum\\b' drave-core/src/clusters.rs drave-core/src/formats.rs drave-core/src/gpu.rs drave-core/src/gguf.rs drave-core/src/materiel.rs drave-core/src/model.r … [380 caractères tronqués]`

  ```
=== TOUS LES 'enum' (insensible casse) ===
drave-core/src/gguf.rs:134:pub enum Tampon {
drave-core/src/gguf.rs:180:pub enum Meta {
drave-core/src/model.rs:28:pub enum Gating {
=== ENV COMPLET (avec option_env) ===
2157:                              f16_avant: std::env::var("DRAVE_KV_F16").is_ok(), k_f32, v_f32,
2565:                        std::env::var("DRAVE_YARN_MSCALE").map(|v| v != "0")
2566:                            .unwrap_or_else(|_| std::env::var("DRAVE_YARN").is_ok()),
2570:                let toujours = std::env::var("DRAVE_YARN").is_ok();
2571:                let jamais = std::env::var("DRAVE_YARN_NON").is_ok();
2940:        let kv_bits: u32 = match std::env::var("DRAVE_KV_BITS").ok().and_then(|v| v.parse().ok()) {
3066:        let tete_gpu = if std::env::var("DRAVE_GPU_TETE").is_ok()
3088:        let kv_gpu = if std::env::var("DRAVE_GPU_KV").is_ok() {
3123:                    if std::env::var("DRAVE_GPU_TOPK").map(|v| v != "0" && !v.is_empty())
3151:        let cache_experts = if std::env::var("DRAVE_GPU_EXPERTS").is_ok()
3162:            let go: f64 = std::env::var("DRAVE_GPU_EXPERTS_GO").ok()
3204:            trace_experts: std::env::var("DRAVE_TRACE_EXPERTS").ok()
… [942 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading '\"[a-zA-Z0-9_./<>|{}=\\[\\] -]{2,}\"' drave-core/src/model.rs | sed -n '170,400p'", "description": "Remaining string literals in model.rs"}`

  ```
2829:                    melange: g.dequant(&q(&format!("{nom}_fn.weight"))),
2830:                    base: g.dequant(&q(&format!("{nom}_base.weight"))),
2831:                    scale: g.dequant(&q(&format!("{nom}_scale.weight"))),
2834:                v.push((mk("hc_attn"), mk("hc_ffn")));
2846:            let tete = if g.tensor("output_hc_fn.weight").is_some() {
2848:                    melange: g.dequant("output_hc_fn.weight"),
2849:                    base: g.dequant("output_hc_base.weight"),
2850:                    scale: g.dequant("output_hc_scale.weight"),
2853:            } else if g.tensor("hc_head_fn.weight").is_some() {
2855:                    melange: g.dequant("hc_head_fn.weight"),
2856:                    base: g.dequant("hc_head_base.weight"),
2857:                    scale: g.dequant("hc_head_scale.weight"),
2874:            let p = |s: &str| format!("blk.{l}.{s}");
2877:                attn_norm: g.dequant(&p("attn_norm.weight")),
2883:                    Proj::load(&g, &p("attn_q.weight"), Some(&p("attn_q.bias")), dense || q4 != 0, auto, keep, q4 & 2 != 0, b6 & 2 != 0) },
2885:                    Proj::load(&g, &p("attn_k.weight"), Some(&p("attn_k.bias")), den
… [8111 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dernières vérifications : env uniques, comparaisons de modes

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== ENV UNIQUES (7 fichiers) ===\"; rg -o --no-filename 'env::var\\(\"[A-Z_0-9]+\"\\)' drave-core/src/clusters.rs drave-core/src/formats.rs drave-core/src/gpu.rs drave-core/src/gguf.rs drave-core/src/materiel.rs drave-core/src … [351 caractères tronqués]`

  ```
=== ENV UNIQUES (7 fichiers) ===
env::var("DRAVE_CLUSTERS")
env::var("DRAVE_DEBUG_ETAT")
env::var("DRAVE_DEBUG_MLA")
env::var("DRAVE_DUMP_COUCHES")
env::var("DRAVE_ETAT_ENTREE")
env::var("DRAVE_FLUX_VERIF")
env::var("DRAVE_GPU")
env::var("DRAVE_GPU_EXPERTS")
env::var("DRAVE_GPU_EXPERTS_GO")
env::var("DRAVE_GPU_KV")
env::var("DRAVE_GPU_TETE")
env::var("DRAVE_GPU_TOPK")
env::var("DRAVE_KV_BITS")
env::var("DRAVE_KV_F16")
env::var("DRAVE_KV_K_F16")
env::var("DRAVE_KV_K_F32")
env::var("DRAVE_KV_V_F32")
env::var("DRAVE_MMAP")
env::var("DRAVE_PRELIRE")
env::var("DRAVE_PRELIRE_TOUT")
env::var("DRAVE_Q8_BLOCS")
env::var("DRAVE_SANS_EMPRUNT")
env::var("DRAVE_TRACE_BLOCS")
env::var("DRAVE_TRACE_EXPERTS")
env::var("DRAVE_YARN")
env::var("DRAVE_YARN_MSCALE")
env::var("DRAVE_YARN_NON")
env::var("DRAVE_YARN_RAMPE")
=== COMPARAISONS DE CHAINES ===
drave-core/src/clusters.rs:54:                let champs: Vec<&str> = c.split_whitespace().filter(|w| *w != "·").collect();
drave-core/src/tokenizer.rs:65:                None => (m.as_str(), ""),
drave-core/src/tokenizer.rs:77:        let motif_gpt4o = pre.starts_with("gpt-4o") || pre.starts_with("o200k");
drave-core/src/gguf.rs:96:        Ok(v) => !(v 
… [3537 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs", "limit": 30, "offset": 344}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs</path>
<type>file</type>
<content>
344: struct Cur<'a> { b: &'a [u8], p: usize, deborde: bool }
345: 
346: impl<'a> Cur<'a> {
347:     // Toutes les lectures sont bornées : un en-tête lu dans une tranche trop
348:     // courte doit être SIGNALÉ, pas provoquer une panique d'indexation. C'est
349:     // ce qui permet à `open_meta` de relire une tranche plus grande.
350:     fn reste(&self, n: usize) -> bool { self.p + n <= self.b.len() }
351:     fn u8(&mut self) -> u8 {
352:         if !self.reste(1) { self.deborde = true; return 0; }
353:         let v = self.b[self.p]; self.p += 1; v
354:     }
355:     fn u32(&mut self) -> u32 {
356:         if !self.reste(4) { self.deborde = true; return 0; }
357:         let v = u32::from_le_bytes(self.b[self.p..self.p+4].try_into().unwrap()); self.p += 4; v
358:     }
359:     fn u64(&mut self) -> u64 {
360:         if !self.reste(8) { self.deborde = true; return 0; }
361:         let v = u64::from_le_bytes(self.b[self.p..self.p+8].try_into().unwrap()); self.p += 8; v
362:     }
363:     fn i8(&mut self) -> i8 { self.u8() as i8 }
364:     fn u16(&mut self) -> u16 {

… [591 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inventaire final des fonctions publiques de model.rs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rg -n --no-heading '^\\s*pub fn |^\\s*pub static |^\\s*pub const ' drave-core/src/model.rs; echo \"=== KSIGNS fin ===\"; sed -n '288,300p' drave-core/src/formats.rs", "description": "List model.rs public functions and KSIGNS end"}`

  ```
46:    pub fn du_numero(n: u64) -> Option<Gating> {
57:    pub fn nom(&self) -> &'static str {
87:pub fn manques_architecture(g: &Gguf, cfg: &Cfg, ctx: usize, clusters: bool) -> Vec<&'static str> {
226:pub fn dim_gguf(g: &Gguf, cles: &[&str], cle_json: &str) -> Option<u64> {
231:pub fn reel_gguf(g: &Gguf, cles: &[&str], cle_json: &str) -> Option<f64> {
256:pub fn routage_du_gguf(g: &Gguf) -> Routage {
864:    pub fn ou(&self, e: usize) -> Option<(usize, usize)> {
970:    pub fn vide() -> Self {
1087:    pub fn nouveau(budget: usize) -> Self {
1092:    pub fn taux(&self) -> f64 {
1281:pub fn sinkhorn(comb: &mut [f32], hc: usize, iters: usize, eps: f32) {
1313:    pub fn hc_mix(&self) -> usize { 2 * self.hc + self.hc * self.hc }
1316:    pub fn melanges(&self, x: &[f32]) -> Vec<f32> {
1331:    pub fn sortie(&self, x: &[f32]) -> HcSortie {
1358:    pub fn tete(&self, x: &[f32]) -> Vec<f32> {
1375:    pub fn melanger(x: &[f32], poids: &[f32], hc: usize, h: usize, out: &mut [f32]) {
1387:    pub fn retro(y: &[f32], residu: &[f32], s: &HcSortie, hc: usize, h: usize,
1450:pub fn f16_depuis_f32(x: f32) -> u16 {
1463:pub fn f32_depuis_f16(h: u16) -> f32 {
1498:    pub fn nouveau(chemin: &st
… [3670 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Bornes exactes des tables et constantes de test

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '274,280p' drave-core/src/formats.rs; echo \"=== gguf 1064-1070 ===\"; sed -n '1064,1070p' drave-core/src/gguf.rs; echo \"=== gguf 1203-1208 ===\"; sed -n '1203,1208p' drave-core/src/gguf.rs; echo \"=== gguf 1718-1726 ===\"; s … [176 caractères tronqués]`

  ```
[8,8,25,25,8,43,43,43,],
    [8,25,8,8,25,43,43,43,],
];

pub static KSIGNS_IQ2XS: [u8; 128] = [
    0,129,130,3,132,5,6,135,136,9,10,139,12,141,142,15,
    144,17,18,147,20,149,150,23,24,153,154,27,156,29,30,159,
=== gguf 1064-1070 ===
    /// Déquantifie un bloc **MXFP4** (17 octets, 32 poids) : un octet d'exposant
    /// E8M0 puis 16 octets de nibbles E2M1, moitié basse puis moitié haute.
    pub fn dequant_mxfp4(bloc: &[u8]) -> Vec<f32> {
        assert!(bloc.len() >= 17, "bloc MXFP4 trop court : {}", bloc.len());
        const KV: [f32; 16] = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0,
                               0.0, -0.5, -1.0, -1.5, -2.0, -3.0, -4.0, -6.0];
        let d = Self::echelle_e8m0(bloc[0]);
=== gguf 1203-1208 ===
        // trois premiers mots porte une échelle de 4 bits, le troisième mot
        // porte les deux bits hauts des seize.
        const KMASK1: u32 = 0x0303_0303;
        const KMASK2: u32 = 0x0f0f_0f0f;
        let mut aux = [0u32; 4];
        for i in 0..3 {
=== gguf 1718-1726 ===
                    out.extend_from_slice(&Self::dequant_mxfp4(&buf[b * 17..]));
                }
            }
            GGML_Q4_K => {
                const KV: [f32
… [849 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dernier complément : fin de la struct KvCache

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 16, "offset": 2134}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
2134:     /// Quantifié : un octet par valeur en 8 bits, **deux nibbles par octet en
2135:     /// 4 bits** (même disposition que Q4_0/MXFP4 : nibble bas = indice pair).
2136:     kq: Vec<u8>,
2137:     vq: Vec<u8>,
2138:     /// Échelles **par bloc de 32**, comme Q8_0 — et non une par vecteur : c'est
2139:     /// ce qui explique l'écart mesuré avec llama.cpp (+5,2 % de perplexité
2140:     /// contre +0,8 % pour son cache q8_0).
2141:     sk: Vec<f32>,
2142:     sv: Vec<f32>,
2143:     nb: usize,
2144: }
2145: 
2146: impl KvCache {
2147:     pub fn new(bits: u32, n_kv: usize, ctx: usize, hd: usize) -> Self {
2148:         let bits = if bits >= 32 { 32 } else if bits > 4 { 8 } else { 4 };
2149:         if bits < 32 {

(Showing lines 2134-2149 of 7022. Use offset=2150 to continue.)
</content>
  ```

### 🤖 Assistant

⏵ Compilation du rapport exhaustif et envoi au parent

- **send_message** `{"agent_id": "f2de810a-b765-444d-b3cc-d8fce1ba2105", "message": "RAPPORT EXHAUSTIF — identifiants exposés dans 7 fichiers de drave-core/src (lecture seule, aucun fichier modifié)\n\nFaits globaux vérifiés : `rg -ni '\\benum\\b'` sur les 7 fichiers ne rend QUE 3 enums : gguf.rs:134 Tampon, gguf.rs:18 … [56434 caractères tronqués]`

  ```
message delivered to agent f2de810a-b765-444d-b3cc-d8fce1ba2105
  ```

### 🤖 Assistant

⏵ Rapport livré au parent ; récapitulatif final

Le rapport exhaustif a été extrait en lecture seule (aucun fichier modifié) et transmis au parent via `send_message`.

**Synthèse de ce qui a été trouvé :**

| Fichier | Enums | Const/static | Structs pub | Env | Tables clés |
|---|---|---|---|---|---|
| clusters.rs | 0 | 1 (`ACTIF`) | 2 (`Mapping`, `Modele`) | `DRAVE_CLUSTERS` | clés TSV `n_couches`, `n_experts`, `clusters`, `experts_par_cluster` |
| formats.rs | 0 | 6 (5 grilles + `IQ1S_DELTA`) | 0 | 0 | 5 fonctions de déquant avec taille de bloc en dur (136/50/66/98/56 o pour 256 poids) |
| gpu.rs | 0 | 2 const + 3 statics | 4 (`MatriceGpu`, `KvGpu`, `TamponsTopk`, `Gpu`) | `DRAVE_GPU` | noms de 15 noyaux PTX |
| gguf.rs | **2** (`Tampon`, `Meta` — 2 + 13 variantes) | 21 `GGML_*` + 3 `TAILLE_*` + 4 autres | 5 (`Mappe`, `TensorInfo`, `Q8View`, `Gguf`, `Cur`) | 3 | **table type→(bloc,octets) 37 entrées (l.761-778) + table type→nom 42 entrées (l.783-795)** |
| materiel.rs | 0 | 4 (`VRAM`, `RAM`, `NVME`, `SUCCES`) | 6 (`Noeud`, `Cpu`, `Gpu`, `Disque`, `Materiel`, `Plan`) | 0 | seuils du plan (reserve 2 Go, commun 8 Go, KV 90 000 o/jeton) |
| model.rs | **1** (`Gating`, 4 variantes) | ~25 const/static | **20** | **23 DRAVE_\*** | `source_de` (l.483-498), `Vue4::pas` (l.700-710), tables IQ (l.1349-1358) |
| tokenizer.rs | 0 | 1 (`SEP`) | 1 (`Tokenizer`, champs privés) | 0 | motifs `"gpt-4o"`/`"o200k"` (l.77) |

**Point important** : la mission présupposait des enums de quantification — il n'y en a **aucun** dans ces 7 fichiers. Les types de quantification sont des constantes `GGML_*` (u32) et des matchs numériques ; les tailles de bloc vivent dans la table gguf.rs:761-778 (37 types) et dans les asserts des fonctions de formats.rs. C'est signalé explicitement dans le rapport.

