# Session DSH — relecture

- identifiant : `c25f97d1-9a4d-41da-b983-004f793afe43`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-09-30 11:47:11
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, paquet `drave-core`, binaire `drave`). Toute la documentation et les rapports sont en FRANÇAIS : écris en français.

CONTEXTE UTILE : ce dépôt a un mode d'échec récurrent, documenté par ses auteurs : un drapeau de ligne de commande ou une variable d'environnement est **analysé mais jamais appliqué** dans au moins un mode d'exécution. Cela s'est produit au moins six fois : `--pin`, `--moe-topk`, `--attn-window`, `--attn-sinks`, `--attn-topk`, `--qk-topk`, `--sans-yarn` (en inférence), et récemment `--abits`/`--act-thresh` dans les modes `--flux-serveur` et `--ppl-reparti`.

TA MISSION : produire l'audit SYSTÉMATIQUE de ce mode d'échec, avec des preuves, et écrire le rapport `reports/rapport-drapeaux-ignores.md`.

Méthode attendue :
1. Lis `drave-core/src/main.rs` : la structure `Options` (tous ses champs), la fonction d'analyse (`analyser`), et les modes d'entrée (inférence, `--ppl`, `--plan`, `--tokenize`, `--flux-serveur`, `--ppl-reparti`, les bancs `--banc-*`, `--tensors`).
2. Inventorie TOUS les drapeaux `--xxx` et TOUTES les variables d'environnement `DRAVE_*` (cherche `std::env::var`).
3. Pour chacun : dans quels modes est-il réellement APPLIQUÉ (pas seulement analysé ni imprimé) ? Donne le fichier et la ligne (`fichier:ligne`) de l'application réelle, et pour chaque mode où il est ignoré, donne la preuve (le chemin de code qui ne le lit pas).
4. Ne te contente pas des apparences : un drapeau peut être appliqué dans le mode « inférence » et oublié dans « --ppl », ou appliqué puis écrasé par une valeur par défaut plus loin. Cherche les écrasements.
5. Vérifie empiriquement 2 ou 3 cas suspects avec le binaire déjà compilé `./drave-core/target/release/drave` et le modèle `models/Qwen2.5-0.5B-Q8_0.gguf`, avec des exécutions TRÈS courtes (`--limit 4`). N'utilise PAS de drapeau `--ppl-reparti`/`--flux-serveur` (ils démarrent un serveur). INTERDIT : toute commande lourde, tout `cargo build`, toute modification d'un fichier autre que ton rapport.

LIVRABLE : `reports/rapport-drapeaux-ignores.md`, en français, concis et factuel, avec :
- un tableau : drapeau/variable · modes où il est appliqué (`fichier:ligne`) · modes où il est ignoré (preuve) · gravité (silencieux ? change les chiffres ?) ;
- une section « ce qui est correct » (pour ne pas donner l'impression que tout est cassé) ;
- une section « recommandation » : comment empêcher la récidive (une idée simple et applicable, par exemple un tableau de bord `--options-actives` qui imprime les réglages réellement appliqués).
Termine ta réponse par un résumé de 10 lignes maximum : le nombre de drapeaux audités, le nombre ignorés dans au moins un mode, et les 3 plus graves.
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

⏵ Démarrage de l'audit des drapeaux ignorés dans drave-core

Je commence par explorer le dépôt et lire `main.rs`.

- **bash** `{"command": "ls -la && echo \"---\" && ls drave-core/src/ && echo \"---\" && wc -l drave-core/src/*.rs", "description": "Lister le dépôt et les sources"}`

  ```
total 208
drwxr-xr-x. 1 stephane stephane   588 30 sep 08:44 .
drwxr-xr-x. 1 stephane stephane  2350 25 sep 11:55 ..
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    52 25 sep 17:53 data
drwxr-xr-x. 1 stephane stephane   348 30 sep 11:08 docs
drwxr-xr-x. 1 stephane stephane    82 28 sep 11:58 drave-core
drwxr-xr-x. 1 stephane stephane   146 30 sep 11:46 .git
-rw-r--r--. 1 stephane stephane   399 30 sep 10:01 .gitignore
drwxr-xr-x. 1 stephane stephane    34 27 sep 11:39 journal
drwxr-xr-x. 1 stephane stephane    88 25 sep 17:13 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-------. 1 stephane stephane 26646 30 sep 08:44 README.md
drwxr-xr-x. 1 stephane stephane  1580 30 sep 11:03 reports
-rw-------. 1 stephane stephane 28339 30 sep 11:39 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane 10507 30 sep 08:44 run_clusters.py
-rw-------. 1 stephane stephane 12507 30 sep 08:44 run_cpu.py
-rw-------. 1 stephane stephane 11462 30 sep 08:44 run_encoding.py
-rw-------. 1 stephane stephan
… [863 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/ 2>/dev/null | head -50; echo \"---\"; ls -la models/ 2>/dev/null; echo \"---\"; ls -la drave-core/target/release/drave 2>/dev/null", "description": "Vérifier rapports, modèle et binaire"}`

  ```
total 260
drwxr-xr-x. 1 stephane stephane  1580 30 sep 11:03 .
drwxr-xr-x. 1 stephane stephane   588 30 sep 08:44 ..
-rw-r--r--. 1 stephane stephane   371 29 sep 18:39 aiguille-30b.md
-rw-r--r--. 1 stephane stephane   355 29 sep 19:09 aiguille-gpt-oss.md
-rw-------. 1 stephane stephane  9179 30 sep 08:44 bilan-multi-materiel.md
-rw-r--r--. 1 stephane stephane  2465 30 sep 08:44 rapport-8bits.md
-rw-------. 1 stephane stephane  5208 29 sep 19:14 rapport-aiguille.md
-rw-r--r--. 1 stephane stephane  3250 30 sep 10:36 rapport-analyse-flux.md
-rw-------. 1 stephane stephane  7834 30 sep 08:44 rapport-attention-creuse.md
-rw-r--r--. 1 stephane stephane  2469 30 sep 11:03 rapport-attribution-kv.md
-rw-------. 1 stephane stephane  4652 30 sep 08:44 rapport-campagne-parcimonie.md
-rw-------. 1 stephane stephane  5617 30 sep 08:44 rapport-capteur-hebbien.md
-rw-r--r--. 1 stephane stephane  3269 30 sep 08:44 rapport-cpu-aer.md
-rw-------. 1 stephane stephane  6381 30 sep 08:44 rapport-croisement-push-pull.md
-rw-r--r--. 1 stephane stephane  5116 30 sep 08:44 rapport-encodage.md
-rw-r--r--. 1 stephane stephane  4411 30 sep 08:44 rapport-eparsite.md
-rw-------. 1 stephane stephane 12636 30 sep 
… [1851 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de `main.rs` : structure `Options` et fonction `analyser`

- **bash** `{"command": "grep -n \"struct Options\" -A 200 drave-core/src/main.rs | head -250", "description": "Extraire la structure Options"}`

  ```
329:struct Options {
330-    // --- sélection du mode
331-    infer: bool, ppl: bool, plan: bool, tokenize: bool, gpu_banc: bool,
332-    /// Banc du KV déporté : nombre de clés à faire tenir en VRAM.
333-    banc_kv: usize,
334-    /// Banc MLA : écrit les logits `(n_pos × vocab)` en f32 pour les comparer à
335-    /// la référence numpy du modèle synthétique.
336-    banc_mla: Option<String>,
337-    /// Trace du flux d'activation : fichier de sortie.
338-    trace_flux: Option<String>,
339-    /// Relecture d'une trace : les activations enregistrées remplacent celles
340-    /// calculées (rejeu).
341-    flux_forcer: Option<String>,
342-    /// Phase 3 : nœud MOTEUR qui écoute et applique sa plage de couches.
343-    /// Adresse d'écoute du nœud moteur : `port`, ou `hôte:port` pour écouter
344-    /// au-delà de localhost (un pair distant, un tunnel, une autre machine).
345-    flux_serveur: Option<String>,
346-    /// Phase 3 : pilote qui répartit le calcul sur un nœud distant (hôte:port).
347-    ppl_reparti: Option<String>,
348-    /// Nombre de couches gardées en local par le pilote.
349-    couches_locales: usize,
350-    /// Couches à tracer (vide = toutes).
351-    trace
… [11308 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"fn analyser\\|fn main\\|--\" drave-core/src/main.rs | grep -n \"fn analyser\\|fn main\" ; echo \"===\"; grep -n \"fn \" drave-core/src/main.rs", "description": "Lister les fonctions de main.rs"}`

  ```
2:27:fn main() {
32:396:fn analyser(args: &[String]) -> Options {
===
23:fn fmt_bits(b: u64, n: usize) -> String {
27:fn main() {
318:fn modele_chemin() -> String { MODELE.get().cloned().unwrap_or_default() }
396:fn analyser(args: &[String]) -> Options {
523:fn stats_experts(mdl: &model::Model) {
532:fn run_infer(opt: Options) {
793:fn all_ids_of(v: &[u32]) -> Vec<u32> { v.to_vec() }
795:fn meta_strings(g: &Gguf, key: &str) -> Vec<String> {
802:fn meta_ints(g: &Gguf, key: &str) -> Vec<i32> {
809:fn build_tokenizer(g: &Gguf) -> tokenizer::Tokenizer {
819:fn cfg_dims(m: &model::Model) -> usize { m.cfg.hidden }
822:fn mdl_cfg_vocab(path: &str) -> Option<usize> {
841:fn erf(x: f32) -> f32 {
857:fn run_banc_vision(sortie: &str) {
1193:fn run_tensors() {
1214:fn appliquer_quantification(mdl: &mut model::Model, opt: &Options) {
1263:    fn du_modele(m: &model::Model) -> Self {
1267:    fn appliquer(&self, m: &mut model::Model) {
1301:    fn en_dense(&self, hidden: usize) -> Vec<f32> {
1320:    fn actifs(&self) -> usize {
1330:fn envoyer_flux(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos: u32,
1400:fn recevoir_flux(s: &mut std::net::TcpStream) -> std::io::Result<Flux> {
1491:fn ru
… [1009 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "offset": 1, "limit": 330}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1: //! drave-core — moteur d'exécution par listes d'événements.
2: //!
3: //! Usage :
4: //!   drave-core <modele.gguf> [--matrix blk.0.ffn_gate.weight] [--threads 8]
5: //!
6: //! Mesure sur le VRAI modèle :
7: //!   1. taille exacte de chaque encodage de liste (bits/poids),
8: //!   2. débit du moteur d'événements selon la densité des activations,
9: //!   3. exécution sans multiplieur (décalages + additions) vs multiplication.
10: 
11: mod engine;
12: mod gguf;
13: mod list;
14: mod model;
15: mod gpu;
16: mod tokenizer;
17: 
18: use engine::{matvec_dense, matvec_shift_add, Pool, SparseVec};
19: use gguf::Gguf;
20: use list::{dense_bits, BitmapSign, DenseQ4, DenseQ8, FusedSign, PushMat, SignedDelta, SparseK};
21: use std::time::Instant;
22: 
23: fn fmt_bits(b: u64, n: usize) -> String {
24:     format!("{:8.3} b/poids  ({:7.2} Mo)", b as f64 / n as f64, b as f64 / 8.0 / 1e6)
25: }
26: 
27: fn main() {
28:     let args: Vec<String> = std::env::args().collect();
29:     if args.len() < 2 {
30:         eprintln!("usage: drave-core <modele.gguf> [--matrix NOM] [--threads N
… [17491 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"env::var\\|DRAVE_\" drave-core/src/*.rs", "description": "Chercher toutes les variables d'environnement"}`

  ```
drave-core/src/gpu.rs:778:/// Instance unique du processus. `DRAVE_GPU` active le déport ; sans lui, aucune
drave-core/src/gpu.rs:788:        if std::env::var("DRAVE_GPU").is_err() { return None; }
drave-core/src/gpu.rs:813:        if std::env::var("DRAVE_GPU").is_err() { return None; }
drave-core/src/main.rs:38:    // Les variables d'environnement ont été renommées QT_* -> DRAVE_* : un
drave-core/src/main.rs:41:    if let Some((vieux, _)) = std::env::vars().find(|(k, _)| k.starts_with("QT_")) {
drave-core/src/main.rs:43:elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.");
drave-core/src/main.rs:1161:    // `DRAVE_VISION_TEXTE=<modele.gguf>` charge le modèle de texte et lui impose le
drave-core/src/main.rs:1170:        let chemin = std::env::var("DRAVE_VISION_TEXTE").unwrap_or_default();
drave-core/src/main.rs:1711:    let bits = std::env::var("DRAVE_KV_BITS").ok().and_then(|v| v.parse().ok()).unwrap_or(32u32);
drave-core/src/main.rs:1728:    let k_nul = std::env::var("DRAVE_BANC_KV_K0").is_ok();
drave-core/src/main.rs:1729:    let v_un = std::env::var("DRAVE_BANC_KV_V1").is_ok();
drave-core/src/main.rs:1733:    let v_unitaire = std::env::var("DRA
… [4241 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des modes d'exécution : inférence, ppl, réparti

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "offset": 532, "limit": 270}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "offset": 1193, "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
532: fn run_infer(opt: Options) {
533:     // Une seule analyse de la ligne de commande (voir `analyser`) : chaque mode
534:     // ne fait plus que déstructurer ce dont il a besoin.
535:     let Options {
536:         ids: mut ids, ids_file, prompt, n: n_new, temp, top_p, topk, rep_pen, hist,
537:         flux, session, chat, ctx: ctx_opt, threads: threads_opt, abits: abits_opt,
538:         ctx_impose, threads_impose, abits_impose, dense, auto, q4, b6,
539:         keep, attn_window, swa_pattern, sans_fenetre, attn_sinks, attn_topk, qk_topk,
540:         act_thresh, act_topk, act_renorm, topk_proj, moe_topk, patch: patch_file,
541:         hebb_layer, hebb_q, hebb_out, sans_yarn, lot, ..
542:     } = opt;
543:     let path = &modele_chemin();
544:     // Défauts du mode INFÉRENCE : 512 jetons, la moitié des cœurs (l'attente
545:     // active de la barrière ne tolère pas la sursouscription), 8 bits.
546:     let cpu = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
547:     let ctx = if ctx_impose { ctx_opt } else { 512 };
548:     let n_threads = if
… [12991 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1193: fn run_tensors() {
1194:     let path = &modele_chemin();
1195:     let g = Gguf::open(path).expect("ouverture du GGUF");
1196:     let nom_type = |t: u32| match t {
1197:         0 => "F32", 1 => "F16", 2 => "Q4_0", 3 => "Q4_1", 6 => "Q5_0", 7 => "Q5_1",
1198:         8 => "Q8_0", 9 => "Q8_1", 10 => "Q2_K", 11 => "Q3_K", 12 => "Q4_K", 13 => "Q5_K",
1199:         14 => "Q6_K", 30 => "BF16", 39 => "MXFP4", _ => "?",
1200:     };
1201:     println!("{} tenseurs dans {}", g.tensors.len(), path);
1202:     for t in &g.tensors {
1203:         let poids: u64 = t.dims.iter().product();
1204:         println!("  {:5} {:38} {:?} · {:.1} M poids", nom_type(t.ttype), t.name, t.dims,
1205:                  poids as f64 / 1e6);
1206:     }
1207: }
1208: 
1209: /// Applique les réglages de quantification de la ligne de commande à un modèle
1210: /// des chemins FLUX. Ils étaient ignorés dans `--flux-serveur` et
1211: /// `--ppl-reparti` : un `--act-thresh 0,05` n'y changeait rien, et le mode
1212: /// « listes » transportait donc une liste PLEINE au lieu d'une liste creuse —
1213
… [4821 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 210, "offset": 1491}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 120, "offset": 2151}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1491: fn run_serveur_flux(opt: Options, adresse: &str) {
1492:     // `port` reste localhost ; `hôte:port` écoute sur l'interface nommée
1493:     // (« 0.0.0.0:5599 » pour un pair distant). Le pair distant est le cas de la
1494:     // phase 3.4 : un nœud Colab, ou une autre machine du réseau.
1495:     let (hote, port) = match adresse.rsplit_once(':') {
1496:         Some((h, p)) => (h.to_string(), p.parse().expect("port invalide")),
1497:         None => ("127.0.0.1".to_string(), adresse.parse().expect("port invalide")),
1498:     };
1499:     let chemin = modele_chemin();
1500:     // Le contexte du nœud moteur suit `--ctx` : figé à 4096, il faisait payer au
1501:     // pair des tampons d'attention seize fois plus grands que le banc (mesuré :
1502:     // 4,8 s contre 1,7 s pour le même calcul, à contexte 256).
1503:     let ctx = if opt.ctx_impose { opt.ctx } else { 4096 };
1504:     let mut mdl = model::Model::load(&chemin, ctx, 16, true, 1.0, false, 0, 0);
1505:     appliquer_quantification(&mut mdl, &opt);
1506:     let hidden = mdl.cfg.hidden;
1507:     let ecou
… [11137 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
2151: fn run_tokenize(opt: Options) {
2152:     let path = &modele_chemin();
2153:     let texte = opt.texte.clone().unwrap_or_default();
2154:     let fichier = opt.fichier.clone().unwrap_or_default();
2155:     let sortie = opt.sortie.clone().unwrap_or_default();
2156:     // En-tête seul : le décodage du vocabulaire n'a pas besoin des poids, et
2157:     // `open` lisait le fichier entier (62 Go pour gpt-oss) à chaque appel.
2158:     let g = Gguf::open_meta(path).expect("ouverture du GGUF");
2159:     let tk = build_tokenizer(&g);
2160:     if !fichier.is_empty() {
2161:         // Encoder un corpus ENTIER avec le tokenizer du modèle : chaque modèle
2162:         // a le sien, et nourrir un modèle avec les identifiants d'un autre
2163:         // donne une perplexité qui ne mesure que l'absurdité de l'entrée.
2164:         let texte = std::fs::read_to_string(&fichier).expect("fichier illisible");
2165:         let ids = tk.encode(&texte);
2166:         let cible = if sortie.is_empty() { format!("{fichier}.ids") } else { sortie };
2167:         let corps: Vec<String> =
… [6060 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de `run_ppl` et des bancs restants

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 340, "offset": 2494}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 110, "offset": 2270}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
2494: fn run_ppl(opt: Options) {
2495:     let Options {
2496:         ids_file: idfile, texte_file, ppl_texte: _, limit, depuis,
2497:         ctx: ctx_opt, threads: threads_opt, abits: abits_opt,
2498:         ctx_impose, threads_impose, abits_impose,
2499:         dense, auto, q4, b6, attn_window, swa_pattern,
2500:         sans_fenetre, attn_sinks, attn_topk, qk_topk, act_thresh, act_topk, act_renorm,
2501:         topk_proj, moe_topk, patch: patch_file, hebb_layer, ffn_gain, logits_bin,
2502:         ppl_profil, lot, profil_neurones, neurones_sortie, trace_flux, trace_couches, flux_forcer,
2503:         harmony, harmony_contexte, sans_yarn, ..
2504:     } = opt;
2505:     let lot = lot.max(1);
2506:     let path = &modele_chemin();
2507:     // Défauts du mode PERPLEXITÉ : 256 jetons, trois quarts des cœurs, 16 bits
2508:     // d'activation (la référence de non-régression en dépend).
2509:     let cpu = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
2510:     let ctx = if ctx_impose { ctx_opt } else { 256 };
2511:     let n_threads = if threads_
… [18215 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
2270: 
2271:     // ------------------------------------------------------- contexte long
2272:     // Le mur du contexte n'est pas le même que celui des poids : le KV croît
2273:     // LINÉAIREMENT avec la longueur et se relit EN ENTIER à chaque jeton. À
2274:     // 1 M, c'est ce trafic qui décide de tout — d'où ce chiffrage, séparé en
2275:     // f32 / int8 / int4 et tenant compte des couches à fenêtre glissante, qui
2276:     // n'ont jamais besoin de plus de `fenetre` entrées.
2277:     let ctx_demande = if opt.ctx > 0 {
2278:         opt.ctx
2279:     } else {
2280:         g.cfg("context_length").and_then(|m| m.as_u64()).unwrap_or(4096) as usize
2281:     };
2282:     let n_kv = g.cfg("attention.head_count_kv").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
2283:     let head_dim = {
2284:         let d = g.cfg("attention.key_length").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
2285:         if d > 0 { d } else {
2286:             let h = g.cfg("embedding_length").and_then(|m| m.as_u64()).unwrap_or(1) as usize;
2287:             let nh = g.cfg("attention.hea
… [5986 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 180, "offset": 1701}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 120, "offset": 1877}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1701:     let path = &modele_chemin();
1702:     let g = Gguf::open(path).expect("ouverture du GGUF");
1703:     let n_kv = g.cfg("attention.head_count_kv").and_then(|m| m.as_u64()).unwrap_or(1) as usize;
1704:     let n_head = g.cfg("attention.head_count").and_then(|m| m.as_u64()).unwrap_or(1) as usize;
1705:     let hidden = g.cfg("embedding_length").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
1706:     let hd = match g.cfg("attention.key_length").and_then(|m| m.as_u64()) {
1707:         Some(v) if v > 0 => v as usize,
1708:         _ => hidden / n_head.max(1),
1709:     };
1710:     let n_layer = g.cfg("block_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
1711:     let bits = std::env::var("DRAVE_KV_BITS").ok().and_then(|v| v.parse().ok()).unwrap_or(32u32);
1712:     let n = opt.banc_kv;
1713:     let rep = (n_head / n_kv.max(1)).max(1);
1714:     let scale = 1.0 / (hd as f32).sqrt();
1715:     println!("banc KV : {n} clés · {n_layer} couches · {n_kv} têtes KV × {hd} dim, {rep} têtes de requête par tête KV · KV {} bits",
1716:              if bits >= 32 { 
… [9051 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1877: fn run_gpu_banc(opt: Options) {
1878:     use std::time::Instant;
1879:     let path = &modele_chemin();
1880:     let threads = if opt.threads_impose { opt.threads } else {
1881:         (std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8) * 3 / 4).max(1)
1882:     };
1883:     let g = Gguf::open(path).expect("ouverture du GGUF");
1884:     // Le banc porte sur la tête Q8_0, ou sur le tenseur nommé (`--matrix`) quand
1885:     // c'est une matrice d'experts MXFP4 — c'est le poste dominant de gpt-oss.
1886:     let mx = g.mxfp4_blocks(&opt.matrix).is_some();
1887:     let nom_q6k = opt.matrix.clone();
1888:     if !mx && g.q6k_blocks(&nom_q6k).is_some() {
1889:         return banc_q6k(opt, &g, &nom_q6k, threads);
1890:     }
1891:     let nom_q4k = opt.matrix.clone();
1892:     if !mx && nom_q4k != "output.weight" && nom_q4k != "token_embd.weight"
1893:         && g.q4k_blocks(&nom_q4k).is_some() {
1894:         return banc_q4k(opt, &g, &nom_q4k, threads);
1895:     }
1896:     let nom = if mx { opt.matrix.clone() } else if g.tensor("output.weight").i
… [5552 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 80, "offset": 855}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 60, "offset": 1140}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
855: /// suit l'est aussi, et le comparer seul évite d'attribuer au modèle une erreur
856: /// de découpage.
857: fn run_banc_vision(sortie: &str) {
858:     use std::io::Write;
859:     let path = &modele_chemin();
860:     let g = Gguf::open(path).expect("ouverture du GGUF");
861:     let Some(t) = g.tensor("v.patch_embd.weight") else {
862:         println!("pas de v.patch_embd.weight dans ce fichier");
863:         return;
864:     };
865:     // dims du moteur : (sortie, entrée, ky, kx)
866:     let (cout, cin, ky, kx) = (t.dims[0] as usize, t.dims[1] as usize,
867:                                t.dims[2] as usize, t.dims[3] as usize);
868:     let mut proj: Option<(Vec<f32>, Vec<f32>)> = None;
869:     println!("v.patch_embd.weight : sortie {cout} · entrée {cin} · noyau {ky}×{kx}");
870:     let w = g.dequant("v.patch_embd.weight");
871:     let mut tour: Option<Vec<f32>> = None;
872:     assert_eq!(w.len(), cout * cin * ky * kx, "poids de patch inattendus");
873:     // Image 28 × 28 déterministe : dégradé + carré central, pour que la
874:     // référence numpy p
… [3134 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1140:                 for i in 0..n3 { acc += w2[o * n3 + i] * h[i]; }
1141:                 y[g * n2 + o] = acc;
1142:             }
1143:         }
1144:         {
1145:             let mut f2 = std::io::BufWriter::new(
1146:                 std::fs::File::create(format!("{sortie}.projecteur")).expect("création"));
1147:             for v in [(n0 as i32), (n1 as i32), (n2 as i32), (n3 as i32)] {
1148:                 f2.write_all(&v.to_le_bytes()).unwrap();
1149:             }
1150:             for v in w0.iter().chain(b0.iter()).chain(w2.iter()).chain(b2.iter()) {
1151:                 f2.write_all(&v.to_le_bytes()).unwrap();
1152:             }
1153:         }
1154:         println!("projecteur : {n_groupe} groupes × {n2} valeurs, |sortie| = {:.4}, 4 premières {:?}",
1155:                  y.iter().map(|v| v * v).sum::<f32>().sqrt(),
1156:                  &y[..4].iter().map(|v| (v * 1e4).round() / 1e4).collect::<Vec<_>>());
1157:         proj = Some((Vec::new(), y));
1158:     }
1159: 
1160:     // ---- Injection : le moteur consomme-t-il un embedding d'image ?
1161:
… [2511 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inventaire systématique des champs d'`Options` et de leurs usages

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"opt\\.[a-z_0-9]*\" drave-core/src/main.rs | sed 's/^\\([0-9]*\\):.*opt\\.\\([a-z_0-9]*\\).*/\\1 opt.\\2/' | sort -k2 | uniq", "description": "Lister tous les accès opt.champ"}`

  ```
1215 opt.abits
1219 opt.act_renorm
1217 opt.act_thresh
1218 opt.act_topk
1712 opt.banc_kv
52 opt.banc_kv
51 opt.banc_mla
47 opt.banc_vision
1562 opt.couches_locales
1503 opt.ctx
1560 opt.ctx
2277 opt.ctx
2278 opt.ctx
1668 opt.dense
2154 opt.fichier
1565 opt.flux_blocs
1566 opt.flux_liste
48 opt.flux_serveur
53 opt.gpu_banc
1571 opt.ids
1573 opt.ids
1673 opt.ids
1675 opt.ids
57 opt.infer
1561 opt.limit
1944 opt.limit
1886 opt.matrix
1887 opt.matrix
1891 opt.matrix
1896 opt.matrix
54 opt.plan
56 opt.ppl
49 opt.ppl_reparti
2155 opt.sortie
50 opt.tensors
2153 opt.texte
1770 opt.threads
1880 opt.threads
55 opt.tokenize
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"mdl\\.[a-z_0-9]* *=\" drave-core/src/main.rs", "description": "Lister les affectations mdl.champ"}`

  ```
551:    mdl.act_levels = ((1u32 << (abits - 1)) - 1) as f32;
552:    mdl.moe_topk = moe_topk;
553:    mdl.act_thresh = act_thresh;
554:    mdl.act_topk = act_topk;
555:    mdl.lot = lot.max(1);
556:    mdl.act_renorm = act_renorm;
557:    mdl.act_topk_proj = topk_proj;
558:    if sans_fenetre { mdl.attn_window = 0; }
559:    if attn_window > 0 { mdl.attn_window = attn_window; }
560:    if let Some(p) = swa_pattern { mdl.swa_pattern = p; }
561:    if attn_sinks > 0 { mdl.attn_sinks = attn_sinks; }
564:    mdl.attn_topk = attn_topk;
565:    mdl.qk_topk = qk_topk;
573:        mdl.stop_id = build_tokenizer(&mdl.g).special_id("<|im_end|>");
610:            mdl.stop_id = tk.special_id("<|return|>");
611:            mdl.stop_id2 = Some(fin);
643:        mdl.patch = Some(pt);
648:        mdl.hebb = Some(model::Hebb::new(l, n_out, n_in, hebb_q));
1173:            mdl.emb_imposee = Some(y[..n_emb].to_vec());
1216:    mdl.act_levels = ((1u32 << (abits - 1)) - 1) as f32;
1217:    mdl.act_thresh = opt.act_thresh;
1218:    mdl.act_topk = opt.act_topk;
1219:    mdl.act_renorm = opt.act_renorm;
1526:                mdl.couche_debut = f.debut as usize;
1527:                mdl.couche_fin = f.fin as
… [1084 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des éventuels écrasements dans `model.rs` et `engine.rs`

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"act_levels\\|act_thresh\\|act_topk\\|act_topk_proj\\|attn_window\\|swa_pattern\\|attn_sinks\\|attn_topk\\|qk_topk\\|moe_topk\\|sans_yarn\\|cfg_yarn_off\\|\\.lot\\b\\|keep\\b\" drave-core/src/model.rs | head -80", "descripti … [51 caractères tronqués]`

  ```
240:/// Élague chaque ligne de sortie en ne gardant que la fraction `keep` des poids
243:/// valeurs. `keep = 1.0` ne touche à rien.
244:fn prune_rows(w: &mut [f32], n_out: usize, n_in: usize, keep: f32) {
245:    if keep >= 1.0 { return; }
246:    let k = ((n_in as f32 * keep) as usize).max(1);
261:fn prune_structured(w: &mut [f32], n_out: usize, n_in: usize, keep: f32) {
262:    if keep >= 1.0 { return; }
263:    let win = ((n_out as f32 * keep) as usize).max(1);
299:    fn load(g: &Gguf, name: &str, bias: Option<&str>, dense: bool, auto: bool, keep: f32,
305:        if keep < 0.0 { prune_structured(&mut w, n_out, n_in, -keep); }
306:        else { prune_rows(&mut w, n_out, n_in, keep); }
345:            let emprunt = keep >= 1.0 && std::env::var("DRAVE_SANS_EMPRUNT").is_err();
352:            let emprunt = keep >= 1.0 && std::env::var("DRAVE_SANS_EMPRUNT").is_err();
376:                if d8.src == crate::list::Source8::Q8_0 && keep >= 1.0
620:    pub act_levels: f32,
622:    /// `act_thresh` écarte les activations sous cette fraction du maximum du
623:    /// vecteur ; `act_topk` ne garde que les k plus grandes. Les deux imitent
627:    pub act_thresh: f32,
628:    pub act_topk
… [5099 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"BITS_POIDS\\|EPINGLER\" drave-core/src/*.rs", "description": "Vérifier les statiques globales bits et pin"}`

  ```
drave-core/src/engine.rs:265:pub static EPINGLER: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);
drave-core/src/engine.rs:388:        let epingle = EPINGLER.load(Ordering::Relaxed);
drave-core/src/list.rs:338:pub static BITS_POIDS: std::sync::atomic::AtomicU32 = std::sync::atomic::AtomicU32::new(0);
drave-core/src/list.rs:456:            let bits = BITS_POIDS.load(std::sync::atomic::Ordering::Relaxed);
drave-core/src/main.rs:516:    if o.pin { engine::EPINGLER.store(true, std::sync::atomic::Ordering::Relaxed); }
drave-core/src/main.rs:517:    if o.bits > 0 { list::BITS_POIDS.store(o.bits, std::sync::atomic::Ordering::Relaxed); }
  ```

### 🤖 Assistant

⏵ Recherche de la documentation et de l'historique des drapeaux ignorés

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls docs/ && echo \"=== README grep ===\" && grep -n \"ignor\\|jamais appliqué\\|analysé\" README.md docs/*.md REPRISE.md 2>/dev/null | head -40", "description": "Chercher les mentions d'options ignorées"}`

  ```
colab-reparti.md
comparaison-spiking.md
contexte-long.md
convertisseur.md
format-flux.md
histoire.md
plan-mla-vision.md
programme-recherche.md
roadmap.md
vision.md
=== README grep ===
docs/convertisseur.md:102:  Un plan de placement qui ignore les nœuds NUMA laisse 20 % sur la table, et
docs/programme-recherche.md:105:Trois résultats de ce projet ferment des portes. Les ignorer serait la faute
docs/roadmap.md:55:| 3.1 | **Contrat d'échange v1** : tranche de liste = en-tête (couche, source, échelle, bits) + paires (destination, valeur) | ✅ | format écrit, relu, rejoué sans perte (phase 0.3/0.3bis) ; **transport TCP en place et FIDÈLE** (`--flux-serveur`, `--ppl-reparti`) — écart local/réparti **0,00e0** sur 40 et 199 flux, après correction de deux défauts (plage de couches ignorée par `forward`, norme finale appliquée deux fois) |
docs/roadmap.md:222:1. **`forward` ignorait la plage de couches.** La boucle partait de `0` au lieu de
docs/roadmap.md:227:   d'échec « analysé mais jamais appliqué » du dépôt produit.
REPRISE.md:65:> mesurés avec deux bugs depuis corrigés : le biais `attn_output` ignoré et la
REPRISE.md:118:| Les boucles d'analyse CLI sont **triplées** | un drapeau en **d
… [326 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline | head -30", "description": "Historique git récent"}`

  ```
2184fc5 Banc réparti : plus de flux pour le dernier jeton
1cf4714 REPRISE et journal : la formule de latence et la validation à 1 024 jetons
e80ceb1 Phase 3.3 : le coût du découpage en fonction de la latence, mesuré
af18f29 Transport en listes à 1 024 jetons : ÷2,3 pour 1,3 % d'écart
86ddf12 Le CODE de l'encodage par écarts, oublié dans le commit précédent
3ae3f45 Découpage fidèle à 1 024 jetons : 0,00e0 sur 1 024 flux
f4bce59 tools/pair_factice.py : les trois modes, et plusieurs clients
9fe0c80 Feuille de route : les cinq mesures de la session au journal
cb37c83 Transport : indices par écarts — 3 623 → 1 568 octets par flux, à quantification identique
976cb81 Transport : l'écart DÉCROÎT avec la longueur (la courbe le dit, pas moi)
4396f25 REPRISE : le calcul réparti tient debout (§6bis) et les commandes pour le rejouer
fb8183a L'entrée normée sur le fil : hypothèse RÉFUTÉE par la mesure
2c7271b Transport : les chiffres du VRAI texte, plus sobres que ceux des identifiants synthétiques
27f46c1 Répétition Colab : nœud moteur écoutable au-delà de localhost + recette
5ea06f9 Phase 3 : échelles par bloc, TCP_NODELAY, et l'écart KV attribué aux clés
7b88131 Phase 3.2 : le flux voyage en 
… [1074 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '140,165p' REPRISE.md && echo \"=== histoire.md ===\" && grep -n \"pin\\|moe-topk\\|attn-window\\|attn-sinks\\|attn-topk\\|qk-topk\\|sans-yarn\\|abits\" docs/histoire.md | head -40", "description": "Lire REPRISE.md et histoire … [5 caractères tronqués]`

  ```
## 6. Les huit chantiers : où ils en sont

| # | chantier | état | mesure |
|---|---|---|---|
| 1 | protocole de perplexité longue | **fait** | `--depuis N` note les mêmes jetons à contexte variable ; `--depuis 256 --ctx 256` redonne exactement la fenêtre 2 historique (21,565) |
| 2 | seuil de rotation YaRN | **fait, seuil à 4 × la longueur déclarée** | comparaison appariée (mêmes 512 jetons) : contexte 128→1536, RoPE simple 39,52/49,79/49,93/298,56 contre interpolation 42,13/82,02/82,15/578,86 → le simple gagne partout. **Au-delà du seuil** (5 120 jetons, corpus de 17 k maintenant disponible) : simple **9,6986** contre interpolation seule **1 269,1777** → le seuil de 4 096 était **trop bas** ; le moteur ne bascule plus qu'à 1,25 × la longueur déclarée. Au-delà (16 k, 131 k) : non mesuré, une passe à 16 k coûte une heure |
| 3 | KV int8 puis int4 | **fait, jusqu'à 8 192** | **échelles par bloc de 32** : int8 +**1,5 %** à 512 (était +7,1 %), **+3,0 % à 8 192** (llama.cpp +0,8 %) ; int4 **+364 % à 8 192** contre +494 % pour llama.cpp — meilleur que la référence, et 1 M tient en int4 (9,7 Go). Prix caché : la passe coûte 864 s (f32) / 1 144 (int8) / 1 461 (int4), la déquantification p
… [3461 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"DRAVE_\" README.md docs/*.md REPRISE.md 2>/dev/null | head -40", "description": "Chercher la doc des variables DRAVE_"}`

  ```
README.md:12:Le nom du crate et du binaire (`drave-core`, variables `DRAVE_*`) changera dans un
docs/contexte-long.md:89:  défaut dans le mode retardé ; `DRAVE_YARN=1` la rétablit pour reproduire les
docs/contexte-long.md:104:| E4 | **KV déporté sur les 2 GPU** (pagination, préchargement) | **fait** : noyau `attn_kv_*` (tuiles de 32 clés en mémoire partagée, une passe par (tête KV, tranche), recombinaison + puits), miroir VRAM du cache (`DRAVE_GPU_KV=1`) — mesuré **×12 à ×73** sur l'attention selon le format, PPL identique ; voir §4.ter | décodage à 1 M borné par la VRAM et non par la RAM | moyen |
docs/contexte-long.md:117:empaquetés en 4 bits — `DRAVE_KV_BITS=8` ou `4`, `[config] cache KV` dit ce qui est
docs/contexte-long.md:236:### Dans le moteur (`DRAVE_GPU=1 DRAVE_GPU_KV=1`)
docs/contexte-long.md:238:Les DEUX variables sont nécessaires : c'est `DRAVE_GPU` qui ouvre le pilote (`gpu::instance`),
docs/contexte-long.md:239:`DRAVE_GPU_KV` qui demande le miroir. Avec la seule seconde, il ne se passe rien — et
docs/contexte-long.md:299:Le cache LRU d'experts a été écrit et mesuré (`DRAVE_GPU_EXPERTS=1`, budget 12 Go,
docs/contexte-long.md:339:(`DRAVE_KV_F16=1`, arrondi à 10 bits de 
… [4850 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/audit.sh <<'EOF'\n#!/bin/bash\nF=drave-core/src/main.rs\n# bornes des fonctions (début -> fin)\ndeclare -A RANGES=(\n [main]=\"27 307\" [analyser]=\"396 519\" [run_infer]=\"532 786\"\n [run_banc_vision]=\"857 1189\" [run_t … [1583 caractères tronqués]`

  ```
infer            | analyser,main,
ppl              | analyser,main,run_ppl,run_ppl_reparti,
plan             | analyser,main,run_plan,
tokenize         | analyser,main,
gpu_banc         | analyser,main,
banc_kv          | analyser,main,run_banc_kv,
banc_mla         | analyser,main,
trace_flux       | analyser,run_ppl,
flux_forcer      | analyser,run_ppl,
flux_serveur     | analyser,main,
ppl_reparti      | analyser,main,
couches_locales  | analyser,run_ppl_reparti,
trace_couches    | analyser,run_ppl,
banc_vision      | analyser,main,
tensors          | analyser,main,run_banc_vision,run_plan,run_tensors,
ids              | analyser,fenetres_harmony,main,run_banc_mla,run_infer,run_ppl,run_ppl_reparti,run_tokenize,
ids_file         | analyser,run_infer,run_ppl,
texte_file       | analyser,run_ppl,
ppl_texte        | analyser,run_ppl,
prompt           | analyser,main,run_infer,
limit            | analyser,run_gpu_banc,run_ppl,run_ppl_reparti,
depuis           | analyser,run_infer,run_ppl,
n                | analyser,fenetres_harmony,main,run_banc_kv,run_banc_vision,run_gpu_banc,run_infer,run_plan,run_ppl,run_ppl_reparti,run_serveur_flux,run_tokenize,
temp             | analyser,main,r
… [2925 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inventaire complet des variables `DRAVE_*` et de leur site d'application

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rno \"DRAVE_[A-Z0-9_]*\" drave-core/src/*.rs | sort -t: -k3 | awk -F: '{print $3\" \"$1\":\"$2}' | sort -u", "description": "Extraire toutes les variables DRAVE_ citées"}`

  ```
DRAVE_BANC_KV_DEBUG drave-core/src/main.rs:1865
DRAVE_BANC_KV_GPU_SEUL drave-core/src/main.rs:1767
DRAVE_BANC_KV_GPU_SEUL drave-core/src/main.rs:1769
DRAVE_BANC_KV_GPU_SEUL drave-core/src/main.rs:1809
DRAVE_BANC_KV_GRAD drave-core/src/main.rs:1738
DRAVE_BANC_KV_K0 drave-core/src/main.rs:1728
DRAVE_BANC_KV_KUNIT drave-core/src/main.rs:1741
DRAVE_BANC_KV_UNIT drave-core/src/main.rs:1733
DRAVE_BANC_KV_UNIT drave-core/src/main.rs:1858
DRAVE_BANC_KV_V1 drave-core/src/main.rs:1729
DRAVE_ drave-core/src/main.rs:38
DRAVE_ drave-core/src/main.rs:43
DRAVE_FLUX_VERIF drave-core/src/model.rs:2807
DRAVE_GPU drave-core/src/gpu.rs:778
DRAVE_GPU drave-core/src/gpu.rs:788
DRAVE_GPU drave-core/src/gpu.rs:813
DRAVE_GPU_EXPERTS drave-core/src/model.rs:1505
DRAVE_GPU_EXPERTS drave-core/src/model.rs:752
DRAVE_GPU_EXPERTS_GO drave-core/src/model.rs:1508
DRAVE_GPU_KV drave-core/src/model.rs:1413
DRAVE_GPU_KV drave-core/src/model.rs:707
DRAVE_GPU_TETE drave-core/src/model.rs:1385
DRAVE_GPU_TETE drave-core/src/model.rs:1387
DRAVE_GPU_TETE drave-core/src/model.rs:1391
DRAVE_HARMONY_TRACE drave-core/src/main.rs:2439
DRAVE_HARMONY_TRACE drave-core/src/main.rs:2484
DRAVE_KV_BITS drave-core/src/main.rs:1711
DRAV
… [1088 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"\\blot\\b\" drave-core/src/main.rs | sed -n '1,20p'; echo \"=== model.rs lot ===\"; grep -n \"self\\.lot\\|lot:\" drave-core/src/model.rs | head -20", "description": "Vérifier l'usage de --lot et mdl.lot"}`

  ```
382:    /// Taille du lot de préremplissage : 1 = jeton par jeton (défaut).
383:    lot: usize,
462:            "--lot" => { o.lot = suivant(i).parse().unwrap(); 2 }
541:        hebb_layer, hebb_q, hebb_out, sans_yarn, lot, ..
555:    mdl.lot = lot.max(1);
2334:    println!("  préremplissage SÉQUENTIEL estimé : {:.1} h (le moteur ne fait pas de lot ; \
2502:        ppl_profil, lot, profil_neurones, neurones_sortie, trace_flux, trace_couches, flux_forcer,
2505:    let lot = lot.max(1);
2696:        // Préremplissage par lots : `lot` jetons d'un coup. `lot == 1` emprunte
2700:            let t = lot.min(chunk.len() - pos);
2710:                // Tête au fil du jeton (lot 1) : chronométrée à part, sinon son
=== model.rs lot ===
735:    pub emb_imposee_lot: Option<Vec<f32>>,
757:    pub lot: usize,
1553:            emb_imposee: None, emb_imposee_lot: None, lot: 1,
3502:        // Préremplissage par lots : `forward_lot` sur des tranches de `self.lot`
3505:        let lot = self.lot.max(1);
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3490,3520p' drave-core/src/model.rs && echo \"=== 2790-2820 (FLUX_VERIF) ===\" && sed -n '2785,2820p' drave-core/src/model.rs", "description": "Vérifier generate/lot et DRAVE_FLUX_VERIF"}`

  ```
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
                last = hs.into_iter().next_back().expect("lot non v
… [2462 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '440,470p' drave-core/src/list.rs && echo \"=== DenseQ8::build callers ===\" && grep -rn \"DenseQ8::build\\|DenseQ8::emprunter\\|dense8\\|q8_blocks\" drave-core/src/model.rs | head -20", "description": "Vérifier BITS_POIDS et  … [9 caractères tronqués]`

  ```
pub unsafe fn emprunter_q8(base: *const u8, n_out: usize, n_in: usize,
                               nb_ligne: usize) -> Self {
        DenseQ8 { n_in, n_out, q: Vec::new(), scale: Vec::new(), scb: Vec::new(),
                  src: Source8::Q8_0, base, nb_ligne }
    }

    /// Produit scalaire sur une matrice Q8_0 **empruntée** : l'échelle du bloc
    /// est appliquée à la somme entière du bloc, comme dans le fichier.
    pub fn dot_q8_source(&self, o: usize, x: &[i32]) -> f32 {
        let mut acc = 0f32;
        for b in 0..self.nb_ligne {
            let p = unsafe { self.base.add((o * self.nb_ligne + b) * 34) };
            let octets = unsafe { std::slice::from_raw_parts(p, 34) };
            let d = crate::gguf::Gguf::f16_to_f32(u16::from_le_bytes([octets[0], octets[1]]));
            let xb = &x[b * BLOC_Q4..b * BLOC_Q4 + BLOC_Q4];
            let mut s = 0i32;
            let bits = BITS_POIDS.load(std::sync::atomic::Ordering::Relaxed);
            if bits >= 8 || bits == 0 {
                for j in 0..BLOC_Q4 { s += (octets[2 + j] as i8 as i32) * xb[j]; }
            } else {
                // Arrondi au niveau le plus proche de la grille réduite, puis
              
… [979 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"flux_force\\|self\\.trace\\b\" drave-core/src/model.rs | head -30", "description": "Vérifier trace et rejeu dans forward/forward_lot"}`

  ```
723:    pub flux_force: Option<FluxRelecteur>,
1552:            cache_experts, mla, mla_cache, jeton_trace: 0, trace: None, flux_force: None,
2200:            Self::flux_lot(&mut self.trace, &mut self.flux_force, &mut self.jeton_trace,
2410:            Self::flux_lot(&mut self.trace, &mut self.flux_force, &mut self.jeton_trace,
2803:            if self.flux_force.is_some() {
2810:                let r = self.flux_force.as_mut().unwrap();
2822:            } else if self.trace.is_some() {
2829:                    self.trace.as_mut().unwrap().ecrire(l, j as usize, &actifs, sx);
3063:            if let Some(r) = self.flux_force.as_mut() {
3066:            } else if self.trace.is_some() {
3073:                    self.trace.as_mut().unwrap().ecrire(l + 1000, j as usize, &actifs, sx);
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -- \"--keep\\|--ffn-gain\\|--hebb-q\\|--hebb-out\\|--topk-q\\|--lot\\|--depuis\\|--trace-flux\\|--profil-neurones\\|--bits\\b\\|--q4\\|--auto\\b\\|--push\\b\" README.md docs/*.md REPRISE.md 2>/dev/null | head -40", "descripti … [52 caractères tronqués]`

  ```
README.md:377:| **push** (`--push`) | densité < 22 % — réseau creux, k-WTA, ReLU | 13,6 tok/s à 100 %, 20,6 à 5 % |
README.md:378:| **4 bits** (`--q4`, `--q4-tout`) | modèle 4 bits existant (Q4_0) ou débit prioritaire | **41,6 – 44 tok/s** |
docs/contexte-long.md:105:| E5 | **Attention creuse** | à faire — `--attn-topk` et `--attn-window` existent et se mesurent au protocole `--depuis` | casse le O(N) du décodage | moyen |
docs/contexte-long.md:286:Qwen2.5-0.5B, contexte 4 096, 4 095 jetons notés, `--lot 512` :
docs/contexte-long.md:360:> de 6 à 542 de perplexité selon la tranche. Le protocole `--depuis N` corrige
docs/contexte-long.md:405:contexte 5 120, protocole apparié `--depuis` :
docs/contexte-long.md:492:   `--depuis` (mêmes jetons, contexte long) donnent le prix en perplexité de
docs/contexte-long.md:494:3. **Débit du préremplissage** : `--lot N` sur un modèle dense et sur gpt-oss,
docs/format-flux.md:5:1. la **trace** d'exécution (`--trace-flux`) : ce qui s'est passé, couche par
docs/format-flux.md:94:| deux implémentations indépendantes lisent le même fichier | Rust (`--trace-flux`) et Python (`tools/flux_codec.py`) : aller-retour **identique** sur 132 396 736 octets |
do
… [1171 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la data/ bench/ 2>/dev/null | head -30 && echo \"=== petits fichiers texte ===\" && ls -la docs/*.md | head", "description": "Chercher un corpus de test existant"}`

  ```
bench/:
total 16
drwxr-xr-x. 1 stephane stephane   40 25 sep 15:38 .
drwxr-xr-x. 1 stephane stephane  588 30 sep 08:44 ..
-rw-r--r--. 1 stephane stephane 4193 25 sep 15:34 cpu_aer.c
-rw-r--r--. 1 stephane stephane 4522 25 sep 15:38 cpu_merge.c

data/:
total 384
drwxr-xr-x. 1 stephane stephane     52 25 sep 17:53 .
drwxr-xr-x. 1 stephane stephane    588 30 sep 08:44 ..
-rw-r--r--. 1 stephane stephane 359041 25 sep 18:02 wikitext2_test.txt
-rw-r--r--. 1 stephane stephane  30005 25 sep 17:53 wt2.json
=== petits fichiers texte ===
-rw-r--r--. 1 stephane stephane  5485 30 sep 11:39 docs/colab-reparti.md
-rw-------. 1 stephane stephane  8505 30 sep 08:44 docs/comparaison-spiking.md
-rw-------. 1 stephane stephane 28812 30 sep 08:44 docs/contexte-long.md
-rw-------. 1 stephane stephane 16030 28 sep 11:57 docs/convertisseur.md
-rw-r--r--. 1 stephane stephane  4786 30 sep 10:49 docs/format-flux.md
-rw-------. 1 stephane stephane  4359 30 sep 08:45 docs/histoire.md
-rw-------. 1 stephane stephane 38716 30 sep 08:44 docs/plan-mla-vision.md
-rw-------. 1 stephane stephane 11951 27 sep 16:09 docs/programme-recherche.md
-rw-------. 1 stephane stephane 20063 30 sep 11:39 docs/roadmap.md
-rw------
… [56 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --plan 2>&1 | head -12", "description": "Test T3 : --plan sans --ctx"}`

  ```
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
plan de placement — qwen2, 24 couches

  couche     attention           ffn       experts          cumul  placement
      0        2.0 Mo       13.9 Mo        0.0 Mo        0.02 Go  CPU
      1        2.0 Mo       13.9 Mo        0.0 Mo        0.03 Go  CPU
      2        2.0 Mo       13.9 Mo        0.0 Mo        0.05 Go  CPU
      3        2.0 Mo       13.9 Mo        0.0 Mo        0.06 Go  CPU
      4        2.0 Mo       13.9 Mo        0.0 Mo        0.08 Go  CPU
      5        2.0 Mo       13.9 Mo        0.0 Mo        0.10 Go  CPU
      6        2.0 Mo       13.9 Mo        0.0 Mo        0.11 Go  CPU
      7        2.0 Mo       13.9 Mo        0.0 Mo        0.13 Go  CPU
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --plan 2>/dev/null | grep -A3 \"contexte\"", "description": "Extraire la ligne contexte du plan"}`

  ```
=== contexte : 512 jetons ===
  KV par jeton et par couche : 2 têtes KV × 64 dim × 2 (K et V)
  KV f32  :    0.01 Go en attention complète partout ·    0.01 Go avec la fenêtre
  KV int8 :    0.00 Go en attention complète partout ·    0.00 Go avec la fenêtre
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --tensors 2>/dev/null | grep -i \"context\\|rope\" | head -5; echo \"--- gguf cfg values ---\"; strings -n 6 models/Qwen2.5-0.5B-Q8_0.gguf 2>/dev/null | grep -m2 \"conte … [71 caractères tronqués]`

  ```
--- gguf cfg values ---
qwen2.context_length
  ```

### 🤖 Assistant

⏵ Vérification empirique : `--keep` en `--ppl`, `--ffn-gain` en inférence

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"### --plan --ctx 0 (branche else) ###\" && ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --plan --ctx 0 2>/dev/null | grep \"contexte :\"", "description": "Vérifier la branche else de --plan"}`

  ```
### --plan --ctx 0 (branche else) ###
=== contexte : 32768 jetons ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"### T1a baseline ppl ###\" && timeout 300 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-texte data/wikitext2_test.txt --limit 4 --ctx 64 --threads 4 2>/dev/null | grep -E \"poids gardés|perplexité [0-9] … [83 caractères tronqués]`

  ```
### T1a baseline ppl ###
=== perplexité 1929.3230 sur 3 tokens (0 événements, 0.3 s) ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"### T1b ppl + --keep 0.05 ###\" && timeout 300 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-texte data/wikitext2_test.txt --limit 4 --ctx 64 --threads 4 --keep 0.05 2>/dev/null | grep -E \"poids gardés … [104 caractères tronqués]`

  ```
### T1b ppl + --keep 0.05 ###
=== perplexité 1929.3230 sur 3 tokens (0 événements, 0.3 s) ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"### T1c infer baseline ###\" && timeout 300 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --infer --ids 1,2,3,4,5 --n 4 --ctx 64 --threads 4 2>/dev/null | grep -E \"poids gardés|tokens générés\"", "descriptio … [56 caractères tronqués]`

  ```
### T1c infer baseline ###
tokens générés : [6, 25010, 10, 4999]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"### T1d infer + --keep 0.05 ###\" && timeout 300 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --infer --ids 1,2,3,4,5 --n 4 --ctx 64 --threads 4 --keep 0.05 2>/dev/null | grep -E \"poids gardés|tokens généré … [77 caractères tronqués]`

  ```
### T1d infer + --keep 0.05 ###
tokens générés : [53116, 84925, 36109, 36752]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"### T2a ppl + --ffn-gain 0:4 ###\" && timeout 300 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-texte data/wikitext2_test.txt --limit 4 --ctx 64 --threads 4 --ffn-gain 0:4 2>/dev/null | grep -E \"gain F … [103 caractères tronqués]`

  ```
### T2a ppl + --ffn-gain 0:4 ###
gain FFN : couche 0 x 4
=== perplexité 4949.4977 sur 3 tokens (0 événements, 0.3 s) ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"### T2b infer + --ffn-gain 0:4 ###\" && timeout 300 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --infer --ids 1,2,3,4,5 --n 4 --ctx 64 --threads 4 --ffn-gain 0:4 2>/dev/null | grep -E \"gain FFN|tokens géné … [93 caractères tronqués]`

  ```
### T2b infer + --ffn-gain 0:4 ###
tokens générés : [6, 25010, 10, 4999]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1290,1310p' drave-core/src/model.rs", "description": "Vérifier le message poids gardés"}`

  ```
}
            layers.push(lay);
        }
        let out_norm = g.dequant("output_norm.weight");
        // Précision du cache KV : 32 (f32, défaut), 8 ou 4. Le trafic de
        // relecture est LE mur du contexte long ; la trace le dit au chargement.
        let kv_bits: u32 = std::env::var("DRAVE_KV_BITS").ok()
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

… [76 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du contrat de flux (champs transmis) et des env var

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1355,1400p' drave-core/src/main.rs", "description": "Lire envoyer_flux et l'en-tête Act"}`

  ```
let (n, echelle, corps): (usize, f32, Vec<u8>) = if mode == MODE_BLOCS {
        let (idx, val, echelles) = mdl.expect("modèle requis pour quantifier un flux")
                                      .flux_en_liste_blocs(actifs);
        // Indices par ÉCARTS : la liste est triée (les blocs sont parcourus dans
        // l'ordre), donc l'écart au neurone précédent tient sur un octet dans
        // l'immense majorité des cas — 255 est l'échappement vers l'indice absolu.
        // Deux octets par neurone actif au lieu de trois, à quantification
        // IDENTIQUE : c'est du rangement, pas de la perte.
        let mut c = Vec::with_capacity(4 + echelles.len() * 4 + idx.len() * 2);
        c.extend_from_slice(&(echelles.len() as u32).to_le_bytes());
        for e in &echelles { c.extend_from_slice(&e.to_le_bytes()); }
        let mut paires: Vec<u8> = Vec::with_capacity(idx.len() * 2);
        let mut prev = 0u32;
        for (&i, &v) in idx.iter().zip(val.iter()) {
            let ecart = i as u32 - prev;
            if ecart < 255 {
                paires.push(ecart as u8);
            } else {
                paires.push(255);
                paires.extend_from_slice(&i.to_le_byte
… [1110 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"attn_sinks\\|sinks\" drave-core/src/model.rs | sed -n '1,25p'", "description": "Vérifier l'usage réel de attn_sinks"}`

  ```
219:    pub sinks: Option<Vec<f32>>,
650:    /// clés, plus `attn_sinks` jetons puits au début de la séquence.
674:    pub attn_sinks: usize,
693:    pub sinks_vus: usize,
1277:                sinks: if g.tensor(&p("attn_sinks.weight")).is_some() {
1278:                    Some(g.dequant(&p("attn_sinks.weight"))) } else { None },
1312:        let sinks_vus = layers.iter().filter(|l| l.sinks.is_some()).count();
1324:        println!("[config] puits appris sur {sinks_vus}/{n_layer} couches · n_rot {} · ffn {} · experts {}{}",
1546:            attn_sinks: if fenetre > 0 { 0 } else { 4 },
1550:            tete_gpu, tete_gpu_q6k, head4, sinks_vus, kv_gpu, attn_gpu_part: Vec::new(),
2299:                    let puits: Option<Vec<f32>> = lay.sinks.as_ref()
2332:                            let puits = lay.sinks.as_ref().map(|s| s[hh]);
2361:                    let puits = lay.sinks.as_ref().map(|s| s[hh]);
2905:                let puits: Option<Vec<f32>> = lay.sinks.as_ref()
2938:                        let puits = lay.sinks.as_ref().map(|s| s[hh]);
2978:                let ns = if lo > 0 { self.attn_sinks.min(lo) } else { 0 };
2996:                    let ns = if lo > 0 { self.attn_sinks.
… [161 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1400,1425p' drave-core/src/main.rs && echo \"=== 2960-3010 model.rs ===\" && sed -n '2960,3010p' drave-core/src/model.rs", "description": "Lire l'en-tête du flux et le chemin attn_sinks"}`

  ```
tete.extend_from_slice(&MAGIE_FLUX.to_le_bytes());
    tete.push(VERSION_FLUX);
    tete.push(mode);
    tete.extend_from_slice(&debut.to_le_bytes());
    tete.extend_from_slice(&fin.to_le_bytes());
    tete.extend_from_slice(&pos.to_le_bytes());
    tete.extend_from_slice(&(n as u32).to_le_bytes());
    tete.extend_from_slice(&echelle.to_le_bytes());
    tete.extend_from_slice(&act.levels.to_le_bytes());
    tete.extend_from_slice(&act.thresh.to_le_bytes());
    tete.extend_from_slice(&act.topk.to_le_bytes());
    tete.push(act.renorm as u8);
    s.write_all(&tete)?;
    s.write_all(&corps)?;
    s.flush()?;
    Ok((TAILLE_TETE + corps.len(), n))
}

/// Envoie un LOT d'états (`t × hidden`, aplati) dans un seul flux.
///
/// Le lot voyage en f32 dense : c'est le mode de la phase 3.4 (préremplissage
/// réparti), où la latence domine tout — le quantifier est la suite, et il faudra
/// alors une liste PAR ÉTAT, ce que ce cadriciel ne sait pas encore décrire.
fn envoyer_lot(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos0: u32,
               etats: &[f32], t: usize, mdl: &model::Model) -> std::io::Result<usize> {
    use std::io::Write;
=== 2960-3010 model.rs ===
             
… [3069 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"env\" drave-core/src/gpu.rs && echo \"=== appels gpu::instance ===\" && grep -rn \"gpu::instance()\\|machine\\b\" drave-core/src/model.rs | head -20 && echo \"=== 1378-1420 ===\" && sed -n '1378,1420p' drave-core/src/model. … [56 caractères tronqués]`

  ```
748:            if rc != 0 { eprintln!("{}", erreur(rc, "envoi des activations")); return None; }
788:        if std::env::var("DRAVE_GPU").is_err() { return None; }
813:        if std::env::var("DRAVE_GPU").is_err() { return None; }
=== appels gpu::instance ===
374:        let gpu = match (&d, crate::gpu::instance()) {
375:            (Some(d8), Some(machine))
380:                machine.charger_proj(blocs, n_out, d8.nb_ligne)
423:    fn obtenir<'a>(&'a mut self, machine: &crate::gpu::Gpu, l: usize, e: usize,
443:            let mg = machine.charger_mxfp4(gate.blocs_expert(e), gate.n_out, gate.nb)?;
444:            let mu = machine.charger_mxfp4(up.blocs_expert(e), up.n_out, up.nb)?;
445:            let md = machine.charger_mxfp4(down.blocs_expert(e), down.n_out, down.nb)?;
1052:    pub fn vers_gpu_tranche(&self, machine: &crate::gpu::Gpu, m: &mut crate::gpu::KvGpu,
1063:            machine.kv_ecrire_tranche(m, kvh, pos0, t, ko, vo, &[], &[])
1065:            machine.kv_ecrire_tranche(m, kvh, pos0, t, &self.kq[base..base + t * pas],
1073:    pub fn vers_gpu(&self, machine: &crate::gpu::Gpu, m: &mut crate::gpu::KvGpu,
1075:        self.vers_gpu_tranche(machine, m, kvh, pos, 1)
1084
… [3166 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1175,1240p' drave-core/src/model.rs", "description": "Lire la logique YaRN"}`

  ```
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
            // Pourquoi une décision par SÉQUENCE et non par
… [3094 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification critique : `--sans-yarn` est-il appliqué avant le calcul des tables RoPE ?

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"yarn\" drave-core/src/model.rs | head -40", "description": "Tracer cfg.yarn dans model.rs"}`

  ```
56:    pub yarn: Option<(f32, f32, f32, f32, bool)>,
1184:            //   `DRAVE_YARN_NON=1`  jamais de YaRN (ce que fait `--sans-yarn`) ;
1201:            yarn: {
1203:                    Some("yarn") => Some((
1205:                        g.cfg("rope.scaling.yarn_beta_fast").and_then(|m| m.as_f64()).unwrap_or(32.0) as f32,
1206:                        g.cfg("rope.scaling.yarn_beta_slow").and_then(|m| m.as_f64()).unwrap_or(1.0) as f32,
1318:                 if cfg.yarn.is_some() { "yarn " } else { "" },
1327:                 cfg.yarn.map(|y| format!(" · yarn ×{}", y.0)).unwrap_or_default());
1357:        match (cfg.yarn, g.cfg("rope.scaling.original_context_length").and_then(|m| m.as_u64()),
1750:    pub fn cfg_yarn_off(&mut self) { self.cfg.yarn = None; }
2005:    /// RoPE avec étirement **YaRN** (`rope.scaling.type = yarn`).
2014:    fn rope_yarn(v: &mut [f32], n_head: usize, head_dim: usize, pos: usize, base: f32,
2257:                match self.cfg.yarn {
2259:                        Self::rope_yarn(qi, nh, hd, pos, self.cfg.rope_base, f, bf, bl, orig, ms, self.cfg.n_rot);
2260:                        Self::rope_yarn(ki, nkv, hd, pos, self.cfg.rope_base, f, bf, bl, orig, ms, 
… [271 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1350,1378p' drave-core/src/model.rs && echo \"=== 2245-2270 ===\" && sed -n '2245,2270p' drave-core/src/model.rs", "description": "Vérifier l'usage de cfg.yarn au chargement et en forward"}`

  ```
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
            _
… [2155 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Preuve du bug de boucle dans le mode par défaut (sans mode)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"### --dense --threads 4 (mode par defaut) ###\" && timeout 6 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --dense --threads 4 2>&1 | head -3; echo \"### --threads 4 seul ###\"; timeout 6 ./drave-core/target/ … [149 caractères tronqués]`

  ```
### --dense --threads 4 (mode par defaut) ###
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
GGUF ouvert en 222.300567ms — 290 tenseurs
architecture : qwen2 · 24 couches · hidden 896 · intermédiaire 4864
### --threads 4 seul ###
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
GGUF ouvert en 191.749149ms — 290 tenseurs
architecture : qwen2 · 24 couches · hidden 896 · intermédiaire 4864
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"### --dense --threads 4 ###\" && timeout 10 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --dense --threads 4 2>&1 | grep \"^threads :\"; echo \"### --threads 4 seul ###\"; timeout 10 ./drave-core/target/rele … [337 caractères tronqués]`

  ```
### --dense --threads 4 ###
threads : 30
### --threads 4 seul ###
threads : 4
### --dense --limit 4 --threads 4 ###
threads : 30
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '419,512p' drave-core/src/main.rs | grep -o '\"--[a-z0-9-]*\"' | tr -d '\"' | sort -u | nl | tail -60 && echo \"TOTAL:\" && sed -n '419,512p' drave-core/src/main.rs | grep -o '\"--[a-z0-9-]*\"' | sort -u | wc -l", "description … [43 caractères tronqués]`

  ```
25	--flux-liste
    26	--flux-serveur
    27	--gpu-banc
    28	--harmony
    29	--harmony-assistant
    30	--harmony-contexte
    31	--harmony-suite
    32	--harmony-user
    33	--hebbian
    34	--hebb-out
    35	--hebb-q
    36	--hist
    37	--ids
    38	--ids-file
    39	--infer
    40	--keep
    41	--limit
    42	--logits-bin
    43	--lot
    44	--matrix
    45	--moe-topk
    46	--n
    47	--neurones-sortie
    48	--patch
    49	--pin
    50	--plan
    51	--ppl
    52	--ppl-profil
    53	--ppl-reparti
    54	--ppl-texte
    55	--profil-neurones
    56	--prompt
    57	--push
    58	--q4
    59	--q4-attn
    60	--q4-ffn
    61	--q4-tout
    62	--qk-topk
    63	--rep-penalty
    64	--sans-fenetre
    65	--sans-yarn
    66	--session
    67	--sortie
    68	--swa-pattern
    69	--temp
    70	--tensors
    71	--texte
    72	--threads
    73	--tokenize
    74	--topk
    75	--topk-down
    76	--topk-gate
    77	--topk-k
    78	--topk-o
    79	--topk-q
    80	--topk-up
    81	--topk-v
    82	--top-p
    83	--trace-couches
    84	--trace-flux
TOTAL:
84
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '375,400p' drave-core/src/engine.rs && echo \"=== forward_lot verif ? ===\" && grep -c \"DRAVE_FLUX_VERIF\" drave-core/src/model.rs && sed -n '3050,3075p' drave-core/src/model.rs", "description": "Vérifier EPINGLER et l'absenc … [24 caractères tronqués]`

  ```
xs32: AtomicPtr::new(std::ptr::null_mut()),
            sx: AtomicUsize::new(0),
            outs: AtomicPtr::new(std::ptr::null_mut()),
            mode: AtomicUsize::new(1),
            sv_idx: AtomicPtr::new(std::ptr::null_mut()),
            sv_val: AtomicPtr::new(std::ptr::null_mut()),
            n_active: AtomicUsize::new(0),
            accs: AtomicPtr::new(std::ptr::null_mut()),
            accs64: AtomicPtr::new(std::ptr::null_mut()),
            spans: AtomicPtr::new(std::ptr::null_mut()),
            dirty: AtomicPtr::new(std::ptr::null_mut()),
        });
        let mut handles = Vec::with_capacity(n);
        let epingle = EPINGLER.load(Ordering::Relaxed);
        let cibles = if epingle { cibles_locales(n) } else { Vec::new() };
        for id in 0..n {
            let sh = Arc::clone(&shared);
            let cpu = if epingle && !cibles.is_empty() {
                Some(cibles[id % cibles.len()])
            } else { None };
            handles.push(std::thread::spawn(move || {
                if let Some(c) = cpu { epingler(c); }
                let mut last = 0usize;
                loop {
                    // Attente active d'une nouvelle génération. La barriè
… [1593 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1526,1556p' drave-core/src/model.rs && echo \"=== verif lignes clés ===\" && sed -n '65,73p' drave-core/src/main.rs && echo \"--- 1503-1505 ---\" && sed -n '1503,1505p' drave-core/src/main.rs && echo \"--- 1562-1564 ---\" &&  … [123 caractères tronqués]`

  ```
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
            tete_gpu, tete_gpu_q6k, head4, sinks_vus, kv_gpu, attn_gpu_part: Vec::new(),
            couche_debut: 0, couche_fin: n_layer_total, flux_brut: false,
            ca
… [837 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Anomalie : les numéros de ligne semblent avoir bougé, je vérifie l'état du fichier

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && stat -c '%y %s %n' drave-core/src/main.rs && wc -l drave-core/src/main.rs && git status --porcelain | head -20 && echo \"=== grep ===\" && grep -n \"let ctx = if opt.ctx_impose\\|Model::load(&chemin, ctx, 16\" drave-core/src/main.rs" … [53 caractères tronqués]`

  ```
2026-09-30 11:53:17.194748588 -0400 150084 drave-core/src/main.rs
2976 drave-core/src/main.rs
 M drave-core/src/main.rs
 M drave-core/src/model.rs
 M journal/README.md
?? docs/plan-prefill-reparti.md
?? tools/trace_compacite.py
=== grep ===
1563:    let ctx = if opt.ctx_impose { opt.ctx } else { 4096 };
1564:    let mut mdl = model::Model::load(&chemin, ctx, 16, true, 1.0, false, 0, 0);
1648:    let ctx = if opt.ctx_impose { opt.ctx } else { 256 };
1655:    let mut mdl = model::Model::load(&chemin, ctx, 16, true, 1.0, false, 0, 0);
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 5 && stat -c '%y %s' drave-core/src/main.rs && sha256sum drave-core/src/main.rs drave-core/src/model.rs drave-core/target/release/drave && git diff --stat", "description": "Vérifier la stabilité du fichier et son empreinte"}`

  ```
2026-09-30 11:53:17.194748588 -0400 150084
8f352ee72d40f48f8630ce8cc343c2e62cf5a050167cf231c708e79b267fa820  drave-core/src/main.rs
1d7eacc506db6cab71007d96aa4cbc647c46d37691e9c876cf2ac152a84039cc  drave-core/src/model.rs
7d46614a8be3a07058887eb9f6cedaca10b37b9527d98eb0a58932eacd57b063  drave-core/target/release/drave
 drave-core/src/main.rs  | 190 ++++++++++++++++++++++++++++++++++++++++++------
 drave-core/src/model.rs |  35 +++++++--
 journal/README.md       |   2 +-
 3 files changed, 198 insertions(+), 29 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date && echo \"=== nouveaux drapeaux vs HEAD ===\" && git diff drave-core/src/main.rs | grep \"^+\" | grep -o '\"--[a-z0-9-]*\"' | sort -u", "description": "Dater et repérer les nouveaux drapeaux du diff"}`

  ```
mer 30 sep 2026 11:53:45 EDT
=== nouveaux drapeaux vs HEAD ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '\"--[a-z0-9-]*\"' drave-core/src/main.rs | sed -n '1,10p' && echo \"--- total drapeaux actuel ---\" && sed -n '/fn analyser/,/^}/p' drave-core/src/main.rs | grep -o '\"--[a-z0-9-]*\"' | sort -u | wc -l", "description": "Reco … [45 caractères tronqués]`

  ```
68:            "--matrix" => matrix = args[i + 1].clone(),
69:            "--threads" => n_threads = args[i + 1].parse().unwrap(),
420:            "--infer" => { o.infer = true; 1 }
421:            "--ppl" => { o.ppl = true; o.ids_file = Some(suivant(i).clone()); 2 }
422:            "--ppl-texte" => { o.ppl = true; o.ppl_texte = true;
424:            "--plan" => { o.plan = true; 1 }
425:            "--tokenize" => { o.tokenize = true; 1 }
426:            "--gpu-banc" => { o.gpu_banc = true; 1 }
427:            "--banc-kv" => { o.banc_kv = suivant(i).parse().unwrap(); 2 }
428:            "--banc-mla" => { o.banc_mla = Some(suivant(i).clone()); 2 }
--- total drapeaux actuel ---
84
  ```

### 🤖 Assistant

⏵ Le fichier a été modifié pendant l'audit : je reprends la cartographie sur la version actuelle

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^fn \\|^/// \\|^const \\|^static \" drave-core/src/main.rs | grep \"^[0-9]*:fn \" ", "description": "Nouvelle carte des fonctions"}`

  ```
23:fn fmt_bits(b: u64, n: usize) -> String {
27:fn main() {
318:fn modele_chemin() -> String { MODELE.get().cloned().unwrap_or_default() }
396:fn analyser(args: &[String]) -> Options {
523:fn stats_experts(mdl: &model::Model) {
532:fn run_infer(opt: Options) {
793:fn all_ids_of(v: &[u32]) -> Vec<u32> { v.to_vec() }
795:fn meta_strings(g: &Gguf, key: &str) -> Vec<String> {
802:fn meta_ints(g: &Gguf, key: &str) -> Vec<i32> {
809:fn build_tokenizer(g: &Gguf) -> tokenizer::Tokenizer {
819:fn cfg_dims(m: &model::Model) -> usize { m.cfg.hidden }
822:fn mdl_cfg_vocab(path: &str) -> Option<usize> {
841:fn erf(x: f32) -> f32 {
857:fn run_banc_vision(sortie: &str) {
1193:fn run_tensors() {
1214:fn appliquer_quantification(mdl: &mut model::Model, opt: &Options) {
1349:fn envoyer_flux(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos: u32,
1423:fn envoyer_lot(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos0: u32,
1450:fn recevoir_flux(s: &mut std::net::TcpStream, hidden: usize) -> std::io::Result<Flux> {
1551:fn run_serveur_flux(opt: Options, adresse: &str) {
1637:fn nll_logits(lg: &[f32], cible: u32) -> f64 {
1645:fn run_ppl_reparti(opt: Options, pair: &str) {
1809:fn run_banc_mla
… [506 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff drave-core/src/main.rs | grep -n \"^@@\\|^+fn \\|^-fn \" | head -40", "description": "Voir les zones modifiées du diff"}`

  ```
5:@@ -1240,6 +1240,12 @@ const MODE_LISTE: u8 = 1;
18:@@ -1275,6 +1281,8 @@ impl Act {
27:@@ -1293,6 +1301,8 @@ enum ChargeFlux {
36:@@ -1301,6 +1311,10 @@ impl ChargeFlux {
47:@@ -1321,8 +1335,13 @@ impl ChargeFlux {
61:@@ -1396,8 +1415,39 @@ fn envoyer_flux(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos: u32,
70:+fn envoyer_lot(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos0: u32,
97:-fn recevoir_flux(s: &mut std::net::TcpStream) -> std::io::Result<Flux> {
98:+fn recevoir_flux(s: &mut std::net::TcpStream, hidden: usize) -> std::io::Result<Flux> {
102:@@ -1424,6 +1474,16 @@ fn recevoir_flux(s: &mut std::net::TcpStream) -> std::io::Result<Flux> {
119:@@ -1460,7 +1520,7 @@ fn recevoir_flux(s: &mut std::net::TcpStream) -> std::io::Result<Flux> {
128:@@ -1482,7 +1542,7 @@ fn recevoir_flux(s: &mut std::net::TcpStream) -> std::io::Result<Flux> {
137:@@ -1517,7 +1577,7 @@ fn run_serveur_flux(opt: Options, adresse: &str) {
146:@@ -1529,6 +1589,24 @@ fn run_serveur_flux(opt: Options, adresse: &str) {
171:@@ -1554,12 +1632,26 @@ fn run_serveur_flux(opt: Options, adresse: &str) {
177:+fn nll_logits(lg: &[f32], cible: u32) -> f64 {
198:@@ -1574,19 +1666,28 @@ fn run_ppl_repart
… [325 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 150, "offset": 1209}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1209: /// Applique les réglages de quantification de la ligne de commande à un modèle
1210: /// des chemins FLUX. Ils étaient ignorés dans `--flux-serveur` et
1211: /// `--ppl-reparti` : un `--act-thresh 0,05` n'y changeait rien, et le mode
1212: /// « listes » transportait donc une liste PLEINE au lieu d'une liste creuse —
1213: /// le défaut « le drapeau est analysé mais jamais appliqué », déjà vu cinq fois.
1214: fn appliquer_quantification(mdl: &mut model::Model, opt: &Options) {
1215:     let abits = if opt.abits_impose { opt.abits } else { 8 };
1216:     mdl.act_levels = ((1u32 << (abits - 1)) - 1) as f32;
1217:     mdl.act_thresh = opt.act_thresh;
1218:     mdl.act_topk = opt.act_topk;
1219:     mdl.act_renorm = opt.act_renorm;
1220: }
1221: 
1222: /// ---- Phase 3 : le flux passe d'un nœud à l'autre ----------------------------
1223: ///
1224: /// Cadriciel : `u32` magie, `u32` plage (debut, fin), `u32` position, `u32`
1225: /// dimension, puis les activations en f32. C'est le même contenu que le format
1226: /// de trace, réduit à ce qu'un nœud a besoin de recevo
… [6611 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Re-vérification de tous les ancrages sur la révision actuelle (main.rs 8f352ee, model.rs 1d7eacc)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"o.ctx = 512\\|o.threads = (cpu\\|if o.pin\\|if o.bits\\|o.ctx_impose = true\" drave-core/src/main.rs && echo \"=== dispatch ===\" && sed -n '45,58p' drave-core/src/main.rs", "description": "Vérifier analyser et le dispatch" … [1 caractères tronqués]`

  ```
405:    o.ctx = 512;
406:    o.threads = (cpu * 3 / 4).max(1);
456:            "--ctx" => { o.ctx = suivant(i).parse().unwrap(); o.ctx_impose = true; 2 }
516:    if o.pin { engine::EPINGLER.store(true, std::sync::atomic::Ordering::Relaxed); }
517:    if o.bits > 0 { list::BITS_POIDS.store(o.bits, std::sync::atomic::Ordering::Relaxed); }
=== dispatch ===
    let opt = analyser(&args);
    let _ = MODELE.set(args[1].clone());
    if let Some(f) = opt.banc_vision.clone() { run_banc_vision(&f); return; }
    if let Some(adresse) = opt.flux_serveur.clone() { run_serveur_flux(opt, &adresse); return; }
    if let Some(pair) = opt.ppl_reparti.clone() { run_ppl_reparti(opt, &pair); return; }
    if opt.tensors { run_tensors(); return; }
    if let Some(f) = opt.banc_mla.clone() { run_banc_mla(opt, &f); return; }
    if opt.banc_kv > 0 { run_banc_kv(opt); return; }
    if opt.gpu_banc { run_gpu_banc(opt); return; }
    if opt.plan { run_plan(opt); return; }
    if opt.tokenize { run_tokenize(opt); return; }
    if opt.ppl { run_ppl(opt); return; }
    if opt.infer { run_infer(opt); return; }
    let path = &args[1];
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Model::load(\\|appliquer_quantification(&mut mdl\" drave-core/src/main.rs", "description": "Vérifier tous les appels Model::load"}`

  ```
550:    let mut mdl = model::Model::load(path, ctx, n_threads, dense, keep, auto, q4, b6);
1172:            let mut mdl = model::Model::load(&chemin, 512, 16, true, 1.0, false, 0, 0);
1564:    let mut mdl = model::Model::load(&chemin, ctx, 16, true, 1.0, false, 0, 0);
1565:    appliquer_quantification(&mut mdl, &opt);
1655:    let mut mdl = model::Model::load(&chemin, ctx, 16, true, 1.0, false, 0, 0);
1656:    appliquer_quantification(&mut mdl, &opt);
1812:    let mut mdl = model::Model::load(path, 4096, 16, opt.dense, 1.0, false, 0, 0);
2684:    let mut mdl = model::Model::load(path, ctx, n_threads, dense, 1.0, auto, q4, b6);
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"### run_infer (532-786) ###\" && awk 'NR>=532 && NR<=786 && (/mdl\\.(act|moe|lot|attn|qk|patch|hebb|cfg_yarn)/ || /Hebb::new/ || /hebb_out/ || /let ctx = if/ || /let n_threads = if/ || /let abits = if/)' drave-core/src/main.rs … [475 caractères tronqués]`

  ```
### run_infer (532-786) ###
547:    let ctx = if ctx_impose { ctx_opt } else { 512 };
548:    let n_threads = if threads_impose { threads_opt } else { (cpu / 2).max(1) };
549:    let abits = if abits_impose { abits_opt } else { 8 };
551:    mdl.act_levels = ((1u32 << (abits - 1)) - 1) as f32;
552:    mdl.moe_topk = moe_topk;
553:    mdl.act_thresh = act_thresh;
554:    mdl.act_topk = act_topk;
555:    mdl.lot = lot.max(1);
556:    mdl.act_renorm = act_renorm;
557:    mdl.act_topk_proj = topk_proj;
558:    if sans_fenetre { mdl.attn_window = 0; }
559:    if attn_window > 0 { mdl.attn_window = attn_window; }
560:    if let Some(p) = swa_pattern { mdl.swa_pattern = p; }
561:    if attn_sinks > 0 { mdl.attn_sinks = attn_sinks; }
564:    mdl.attn_topk = attn_topk;
565:    mdl.qk_topk = qk_topk;
566:    if sans_yarn { mdl.cfg_yarn_off(); }
643:        mdl.patch = Some(pt);
648:        mdl.hebb = Some(model::Hebb::new(l, n_out, n_in, hebb_q));
772:        let mut f = std::fs::File::create(&hebb_out).expect("création du fichier hebbien");
1216:    mdl.act_levels = ((1u32 << (abits - 1)) - 1) as f32;
1217:    mdl.act_thresh = opt.act_thresh;
1218:    mdl.act_topk = opt.act_topk;
1219:    md
… [1227 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"TraceFlux::nouveau\\|FluxRelecteur::lire\\|mdl.trace = Some\\|mdl.flux_force = Some\\|ppl_profil\\|journal = match\\|activer_profil_neurones\\|rapport_neurones\\|ecrire_neurones\\|neurones_sortie\\|act_log.bin\\|loss_log.bi … [266 caractères tronqués]`

  ```
2640:        ids_file: idfile, texte_file, ppl_texte: _, limit, depuis,
2646:        ppl_profil, lot, profil_neurones, neurones_sortie, trace_flux, trace_couches, flux_forcer,
2647:        harmony, harmony_contexte, sans_yarn, ..
2649:    let lot = lot.max(1);
2667:            .take(limit.saturating_add(depuis))
2686:        match model::FluxRelecteur::lire(chemin) {
2689:                mdl.flux_force = Some(r);
2695:        match model::TraceFlux::nouveau(chemin, trace_couches.clone(), mdl.cfg.hidden,
2697:            Ok(t) => { println!("[trace] flux enregistré dans {chemin}"); mdl.trace = Some(t); }
2704:    if let Some(f) = &texte_file {
2756:    if profil_neurones {
2757:        mdl.activer_profil_neurones();
2797:            let texte_contexte: Option<String> = harmony_contexte.as_ref()
2799:            let f = fenetres_harmony(&tk, &ids, ctx, mode, texte_contexte.as_deref());
2803:                     if harmony_contexte.is_some() { ", avec contexte" } else { "" },
2814:    let mut journal = match &logits_bin {
2831:    let profil = ppl_profil;
2844:            let t = lot.min(chunk.len() - pos);
2919:    if let Some(rapport) = mdl.rapport_neurones() {
2921:        if let S
… [387 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"ctx_demande\\|let threads = if opt.threads_impose\\|opt.limit\\|opt.matrix\\|opt.texte\\|opt.fichier\\|opt.sortie\\|opt.couches_locales\\|opt.flux_liste\\|opt.flux_blocs\\|opt.ids\" drave-core/src/main.rs", "description": " … [32 caractères tronqués]`

  ```
1649:    let limite = opt.limit.max(1).min(ctx);
1650:    let couches_locales = if opt.couches_locales > 0 { opt.couches_locales } else { 12 };
1657:    let mode = if opt.flux_blocs { MODE_BLOCS }
1658:               else if opt.flux_liste { MODE_LISTE }
1663:    let ids: Vec<u32> = if opt.ids.is_empty() {
1665:    } else { opt.ids.clone() };
1817:    let ids: Vec<u32> = if opt.ids.is_empty() {
1819:    } else { opt.ids.clone() };
1914:    let threads = if opt.threads_impose { opt.threads } else {
2024:    let threads = if opt.threads_impose { opt.threads } else {
2030:    let mx = g.mxfp4_blocks(&opt.matrix).is_some();
2031:    let nom_q6k = opt.matrix.clone();
2035:    let nom_q4k = opt.matrix.clone();
2040:    let nom = if mx { opt.matrix.clone() } else if g.tensor("output.weight").is_some() {
2088:    let n_out = if opt.limit < n_out { opt.limit } else { n_out };
2297:    let texte = opt.texte.clone().unwrap_or_default();
2298:    let fichier = opt.fichier.clone().unwrap_or_default();
2299:    let sortie = opt.sortie.clone().unwrap_or_default();
2421:    let ctx_demande = if opt.ctx > 0 {
2441:    println!("\n=== contexte : {} jetons ===", ctx_demande);
2450:        let complet
… [735 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 115, "offset": 1551}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1551: fn run_serveur_flux(opt: Options, adresse: &str) {
1552:     // `port` reste localhost ; `hôte:port` écoute sur l'interface nommée
1553:     // (« 0.0.0.0:5599 » pour un pair distant). Le pair distant est le cas de la
1554:     // phase 3.4 : un nœud Colab, ou une autre machine du réseau.
1555:     let (hote, port) = match adresse.rsplit_once(':') {
1556:         Some((h, p)) => (h.to_string(), p.parse().expect("port invalide")),
1557:         None => ("127.0.0.1".to_string(), adresse.parse().expect("port invalide")),
1558:     };
1559:     let chemin = modele_chemin();
1560:     // Le contexte du nœud moteur suit `--ctx` : figé à 4096, il faisait payer au
1561:     // pair des tampons d'attention seize fois plus grands que le banc (mesuré :
1562:     // 4,8 s contre 1,7 s pour le même calcul, à contexte 256).
1563:     let ctx = if opt.ctx_impose { opt.ctx } else { 4096 };
1564:     let mut mdl = model::Model::load(&chemin, ctx, 16, true, 1.0, false, 0, 0);
1565:     appliquer_quantification(&mut mdl, &opt);
1566:     let hidden = mdl.cfg.hidden;
1567:     let ecou
… [5790 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"DRAVE_\\|cfg_yarn_off\\|let ns = if lo > 0\\|attn_sinks: if fenetre\" drave-core/src/model.rs", "description": "Re-vérifier les ancrages model.rs"}`

  ```
279:/// Construit une matrice int8 : **une échelle par bloc de 32** (`DRAVE_Q8_BLOCS=1`,
285:    if std::env::var("DRAVE_Q8_BLOCS").is_ok() && n_in % 32 == 0 {
343:            // `DRAVE_SANS_EMPRUNT=1` force la reconstruction : c'est ce qui permet
345:            let emprunt = keep >= 1.0 && std::env::var("DRAVE_SANS_EMPRUNT").is_err();
352:            let emprunt = keep >= 1.0 && std::env::var("DRAVE_SANS_EMPRUNT").is_err();
707:    /// Miroir VRAM du cache KV, une entrée par couche (`DRAVE_GPU_KV=1`).
752:    /// Cache VRAM des experts MoE (`DRAVE_GPU_EXPERTS=1`).
866:    /// `DRAVE_KV_F16=1` : arrondir clés et valeurs en f16 avant quantification.
868:    /// Attribution de l'écart int8 : `DRAVE_KV_K_F32=1` garde les CLÉS en f32
869:    /// (l'erreur qui passe par les scores disparaît), `DRAVE_KV_V_F32=1` garde
900:        let (k_f32, v_f32) = (std::env::var("DRAVE_KV_K_F32").is_ok(),
901:                              std::env::var("DRAVE_KV_V_F32").is_ok());
903:                              f16_avant: std::env::var("DRAVE_KV_F16").is_ok(), k_f32, v_f32,
997:        // `DRAVE_KV_F16=1` : clés et valeurs arrondies en demi-précision avant
1182:            //   `DRAVE_YARN=1`      
… [1666 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rno \"DRAVE_[A-Z0-9_]*\" drave-core/src/*.rs | awk -F: '{print $3\" \"$1:\"$2}' | sort -u | awk '{print $1}' | sort -u && echo \"--- total ---\" && grep -rno \"DRAVE_[A-Z0-9_]*\" drave-core/src/*.rs | awk -F: '{print $3}' | sor … [75 caractères tronqués]`

  ```
--- total ---
27
[stderr]
awk: cmd. line:1: {print $3" "$1:"$2}
awk: cmd. line:1:               ^ syntax error
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk 'NR>=1645 && NR<=1808 && /lot/ {print NR\": \"$0}' drave-core/src/main.rs", "description": "Vérifier l'usage de --lot en ppl-reparti"}`

  ```
1671:     // `--lot T` : préremplissage par LOTS sur le fil. La référence locale est
1674:     let lot = opt.lot.max(1);
1686:     println!("[flux] pilote : {couches_locales} couches en local, {} chez le pair, {} jetons",
1692:     if lot > 1 {
1695:             let t = lot.min(ids.len() - pos);
1696:             let hs = mdl.forward_lot(&ids[pos..pos + t], pos);
1697:             let lgs = mdl.logits_lot(&hs);
1728:     if lot > 1 {
1729:         // PRÉREMPLISSAGE RÉPARTI : un lot par aller-retour au lieu d'un flux par
1731:         // coûter la latence d'UN message par lot, pas par jeton.
1734:             let t = lot.min(ids.len() - pos);
1736:             let hs = mdl.forward_lot(&ids[pos..pos + t], pos);
1740:             let o = envoyer_lot(&mut sock, couches_locales as u32, n_layer as u32,
1741:                                 pos as u32, &plat, t, &mdl).expect("envoi du lot");
1745:             let rep = recevoir_flux(&mut sock, mdl.cfg.hidden).expect("réception du lot");
1750:                        "lot reçu de {} valeurs pour {t} jetons de {} canaux",
1753:             // lots : le lot reçu ne redescend pas jeton par jeton.
1758:             let lgs = mdl.logits_lot(&hn)
… [285 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rno \"DRAVE_[A-Z0-9_]*\" drave-core/src/*.rs | sed 's/:[0-9]*:/ /' | awk '{print $2\" \"$1}' | sort -u", "description": "Lister proprement les variables DRAVE_"}`

  ```
DRAVE_BANC_KV_DEBUG drave-core/src/main.rs
DRAVE_BANC_KV_GPU_SEUL drave-core/src/main.rs
DRAVE_BANC_KV_GRAD drave-core/src/main.rs
DRAVE_BANC_KV_K0 drave-core/src/main.rs
DRAVE_BANC_KV_KUNIT drave-core/src/main.rs
DRAVE_BANC_KV_UNIT drave-core/src/main.rs
DRAVE_BANC_KV_V1 drave-core/src/main.rs
DRAVE_DEBUG_FLUX drave-core/src/main.rs
DRAVE_ drave-core/src/main.rs
DRAVE_FLUX_VERIF drave-core/src/model.rs
DRAVE_GPU drave-core/src/gpu.rs
DRAVE_GPU_EXPERTS drave-core/src/model.rs
DRAVE_GPU_EXPERTS_GO drave-core/src/model.rs
DRAVE_GPU_KV drave-core/src/model.rs
DRAVE_GPU_TETE drave-core/src/model.rs
DRAVE_HARMONY_TRACE drave-core/src/main.rs
DRAVE_KV_BITS drave-core/src/main.rs
DRAVE_KV_BITS drave-core/src/model.rs
DRAVE_KV_F16 drave-core/src/model.rs
DRAVE_KV_K_F32 drave-core/src/model.rs
DRAVE_KV_V_F32 drave-core/src/model.rs
DRAVE_Q8_BLOCS drave-core/src/model.rs
DRAVE_SANS_EMPRUNT drave-core/src/model.rs
DRAVE_VISION_TEXTE drave-core/src/main.rs
DRAVE_YARN drave-core/src/model.rs
DRAVE_YARN_MSCALE drave-core/src/model.rs
DRAVE_YARN_NON drave-core/src/model.rs
DRAVE_YARN_RAMPE drave-core/src/model.rs
  ```

### 🤖 Assistant

⏵ Remise à jour de la cartographie champ→fonction sur la révision courante

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && F=drave-core/src/main.rs; for c in keep ffn_gain hebb_q hebb_out topk_proj moe_topk attn_window swa_pattern sans_fenetre attn_sinks attn_topk qk_topk sans_yarn q4 b6 dense auto threads ctx lot limit trace_flux trace_couches flux_forc … [881 caractères tronqués]`

  ```
keep             | analyser run_infer 
ffn_gain         | analyser run_ppl 
hebb_q           | analyser run_infer 
hebb_out         | analyser run_infer 
topk_proj        | analyser run_infer run_ppl 
moe_topk         | analyser run_infer run_ppl 
attn_window      | analyser run_infer run_ppl 
swa_pattern      | analyser run_infer run_ppl 
sans_fenetre     | analyser run_infer run_ppl 
attn_sinks       | analyser run_infer run_ppl 
attn_topk        | analyser run_infer run_ppl 
qk_topk          | analyser run_infer run_ppl 
sans_yarn        | analyser run_infer run_ppl 
q4               | analyser run_infer run_ppl 
b6               | analyser run_infer run_ppl 
dense            | analyser banc_mla envoyer_flux main run_infer run_ppl 
auto             | analyser run_infer run_ppl 
threads          | analyser banc_kv gpu_banc main run_infer run_ppl 
ctx              | analyser harmony_fn main plan ppl_reparti run_infer run_ppl serveur_flux 
lot              | analyser envoyer_flux plan ppl_reparti recevoir_flux run_infer run_ppl serveur_flux 
limit            | analyser gpu_banc ppl_reparti run_ppl 
trace_flux       | analyser run_ppl 
trace_couches    | analyser run_ppl 
flux_force
… [549 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff drave-core/src/model.rs | grep \"^@@\" && echo \"=== 2421-2426 ===\" && sed -n '2421,2426p' drave-core/src/main.rs", "description": "Vérifier les hunks model.rs et la ligne ctx du plan"}`

  ```
@@ -726,6 +726,13 @@ pub struct Model {
@@ -1543,7 +1550,7 @@ impl Model {
@@ -2091,8 +2098,16 @@ impl Model {
@@ -2105,9 +2120,19 @@ impl Model {
=== 2421-2426 ===
        println!("  à {:>9.1} Go/s ({nom}) : {:>7.2} tok/s", debit, debit / (actifs / 1e9));
    }
    if n_expert > 0 {
        // Mesuré sur le 30B-A3B : les tranches d'experts sont lues à 8 Go/s,
        // pas 20 — dix-huit mille tranches de 900 Ko dispersées sur 18 Go
        // coûtent en TLB et en localité ce que la lecture séquentielle ne paie
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date && stat -c '%y %s' drave-core/src/main.rs && sha256sum drave-core/src/main.rs && wc -l drave-core/src/main.rs && grep -n \"let ctx_demande\" drave-core/src/main.rs && grep -n \"=== contexte :\" drave-core/src/main.rs", "descript … [47 caractères tronqués]`

  ```
mer 30 sep 2026 11:54:49 EDT
2026-09-30 11:54:25.370717707 -0400 151659
1726f9ac3665c3ce02bc0b963d26bc9e2910f153ee1aaf45c9ddeed79bb7e1f0  drave-core/src/main.rs
2999 drave-core/src/main.rs
2444:    let ctx_demande = if opt.ctx > 0 {
2464:    println!("\n=== contexte : {} jetons ===", ctx_demande);
  ```

### 🤖 Assistant

⏵ Le fichier est encore en cours d'édition : j'attends la stabilisation avant de figer les références

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 9); do m=$(stat -c '%Y %s' drave-core/src/main.rs); echo \"$(date +%H:%M:%S) $m\"; sleep 10; done", "description": "Surveiller la stabilité du fichier pendant 90 s", "timeoutMs": 150000}`

  ```
11:54:55 1790783665 151659
11:55:05 1790783665 151659
11:55:15 1790783665 151659
11:55:25 1790783665 151659
11:55:35 1790783665 151659
11:55:45 1790783665 151659
11:55:55 1790783665 151659
11:56:05 1790783665 151659
11:56:15 1790783665 151659
  ```

### 🤖 Assistant

⏵ Révision stable : capture finale de tous les ancrages avant rédaction

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum drave-core/src/main.rs drave-core/src/model.rs drave-core/src/list.rs drave-core/src/engine.rs drave-core/src/gpu.rs && wc -l drave-core/src/*.rs && echo \"=== ANCRES main.rs ===\" && grep -n \"let mut i = 2;\\|i += 2;\\|if … [1124 caractères tronqués]`

  ```
1726f9ac3665c3ce02bc0b963d26bc9e2910f153ee1aaf45c9ddeed79bb7e1f0  drave-core/src/main.rs
1d7eacc506db6cab71007d96aa4cbc647c46d37691e9c876cf2ac152a84039cc  drave-core/src/model.rs
6960c3f77e87477f486ae9924b3efc478c56ebe2323d74d834f657adefe6354b  drave-core/src/list.rs
d3f40b1b43453ba8f318f72757c019be3ff75d991d15d0258afe81e69128ac0c  drave-core/src/engine.rs
4aa5abcc835f2754b563dafff1fd2599916ad82b02f00d9a1dfbbb5dd211f71a  drave-core/src/gpu.rs
   976 drave-core/src/engine.rs
   721 drave-core/src/gguf.rs
   821 drave-core/src/gpu.rs
  1440 drave-core/src/list.rs
  2999 drave-core/src/main.rs
  3675 drave-core/src/model.rs
   507 drave-core/src/tokenizer.rs
 11139 total
=== ANCRES main.rs ===
65:    let mut i = 2;
72:        i += 2;
405:    o.ctx = 512;
410:    let mut i = 2;
516:    if o.pin { engine::EPINGLER.store(true, std::sync::atomic::Ordering::Relaxed); }
517:    if o.bits > 0 { list::BITS_POIDS.store(o.bits, std::sync::atomic::Ordering::Relaxed); }
550:    let mut mdl = model::Model::load(path, ctx, n_threads, dense, keep, auto, q4, b6);
551:    mdl.act_levels = ((1u32 << (abits - 1)) - 1) as f32;
552:    mdl.moe_topk = moe_topk;
553:    mdl.act_thresh = act_thresh;
554:    
… [3909 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== model.rs ===\" && grep -n \"DRAVE_\\|act_levels: 127.0\\|attn_sinks: if fenetre\\|pub fn cfg_yarn_off\\|let ns = if lo > 0\\|lot: 1,\\|pub fn load(path\" drave-core/src/model.rs && echo \"=== list.rs ===\" && grep -n \"BIT … [251 caractères tronqués]`

  ```
=== model.rs ===
279:/// Construit une matrice int8 : **une échelle par bloc de 32** (`DRAVE_Q8_BLOCS=1`,
285:    if std::env::var("DRAVE_Q8_BLOCS").is_ok() && n_in % 32 == 0 {
343:            // `DRAVE_SANS_EMPRUNT=1` force la reconstruction : c'est ce qui permet
345:            let emprunt = keep >= 1.0 && std::env::var("DRAVE_SANS_EMPRUNT").is_err();
352:            let emprunt = keep >= 1.0 && std::env::var("DRAVE_SANS_EMPRUNT").is_err();
707:    /// Miroir VRAM du cache KV, une entrée par couche (`DRAVE_GPU_KV=1`).
752:    /// Cache VRAM des experts MoE (`DRAVE_GPU_EXPERTS=1`).
788:    pub fn load(path: &str) -> std::io::Result<Patch> {
866:    /// `DRAVE_KV_F16=1` : arrondir clés et valeurs en f16 avant quantification.
868:    /// Attribution de l'écart int8 : `DRAVE_KV_K_F32=1` garde les CLÉS en f32
869:    /// (l'erreur qui passe par les scores disparaît), `DRAVE_KV_V_F32=1` garde
900:        let (k_f32, v_f32) = (std::env::var("DRAVE_KV_K_F32").is_ok(),
901:                              std::env::var("DRAVE_KV_V_F32").is_ok());
903:                              f16_avant: std::env::var("DRAVE_KV_F16").is_ok(), k_f32, v_f32,
997:        // `DRAVE_KV_F16=1` : clés et valeurs
… [2607 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"QT_\\|let ctx = if ctx_impose\\|let n_threads = if threads_impose\\|let abits = if abits_impose\\|let mut journal = \\|DRAVE_HARMONY_TRACE\\|DRAVE_DEBUG_FLUX\\|DRAVE_BANC_KV_BITS\\|DRAVE_KV_BITS\\|DRAVE_BANC_KV_GPU_SEUL\\|D … [224 caractères tronqués]`

  ```
38:    // Les variables d'environnement ont été renommées QT_* -> DRAVE_* : un
41:    if let Some((vieux, _)) = std::env::vars().find(|(k, _)| k.starts_with("QT_")) {
547:    let ctx = if ctx_impose { ctx_opt } else { 512 };
548:    let n_threads = if threads_impose { threads_opt } else { (cpu / 2).max(1) };
549:    let abits = if abits_impose { abits_opt } else { 8 };
568:        println!("parcimonie imposée : k-WTA garde {:.1} %{}",
712:    let (out, st) = if topk > 0 {
1620:                    if std::env::var("DRAVE_DEBUG_FLUX").is_ok() {
1878:    let bits = std::env::var("DRAVE_KV_BITS").ok().and_then(|v| v.parse().ok()).unwrap_or(32u32);
1895:    let k_nul = std::env::var("DRAVE_BANC_KV_K0").is_ok();
1934:    //    `DRAVE_BANC_KV_GPU_SEUL=1` la saute : à 1 M de clés elle coûte 3 à 16
1936:    let gpu_seul = std::env::var("DRAVE_BANC_KV_GPU_SEUL").is_ok();
1976:        println!("  CPU non mesuré (DRAVE_BANC_KV_GPU_SEUL) · {:.2} Go de KV, une couche", octets as f64 / 1e9);
2032:    if std::env::var("DRAVE_BANC_KV_DEBUG").is_ok() {
2606:        if std::env::var("DRAVE_HARMONY_TRACE").is_ok() {
2651:    if std::env::var("DRAVE_HARMONY_TRACE").is_ok() {
2677:    let ctx = if ctx_i
… [404 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '41,45p' drave-core/src/main.rs && echo \"--- FS debug ---\" && sed -n '1600,1612p' drave-core/src/main.rs && echo \"--- harmony trace ---\" && grep -n \"DRAVE_HARMONY_TRACE\" drave-core/src/main.rs", "description": "Vérifier  … [36 caractères tronqués]`

  ```
if let Some((vieux, _)) = std::env::vars().find(|(k, _)| k.starts_with("QT_")) {
        eprintln!("[attention] {vieux} est l'ancien nom d'une variable d'environnement : \
elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.");
    }
    let opt = analyser(&args);
--- FS debug ---
                // finale appartient au nœud qui a la tête de sortie, et à lui
                // seul. C'est ce qui manquait — 798,3 au lieu de 18,2.
                mdl.flux_brut = true;
                if f.mode == MODE_LOT {
                    // Préremplissage réparti : N états d'un coup. Le nœud n'a pas
                    // les identifiants de jetons — il n'en a pas besoin, les
                    // états entrent directement dans SA première couche.
                    let t = f.n;
                    // Refus EXPLICITE plutôt qu'une boucle sans fin : au-delà de
                    // son contexte, `KvCache::assurer` ne peut pas agrandir et
                    // tournerait indéfiniment (relevé dans `docs/plan-prefill-reparti.md`).
                    if f.pos as usize + t > mdl.ctx {
                        println!("[flux] lot refusé : {t} états à partir de la p
… [156 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date && stat -c '%y %s' drave-core/src/main.rs && sha256sum drave-core/src/main.rs && wc -l drave-core/src/main.rs && git diff drave-core/src/main.rs | grep \"^@@\" | tail -8", "description": "Re-vérifier l'état du fichier"}`

  ```
mer 30 sep 2026 11:56:58 EDT
2026-09-30 11:54:25.370717707 -0400 151659
1726f9ac3665c3ce02bc0b963d26bc9e2910f153ee1aaf45c9ddeed79bb7e1f0  drave-core/src/main.rs
2999 drave-core/src/main.rs
@@ -1517,7 +1588,7 @@ fn run_serveur_flux(opt: Options, adresse: &str) {
@@ -1529,6 +1600,33 @@ fn run_serveur_flux(opt: Options, adresse: &str) {
@@ -1554,12 +1652,26 @@ fn run_serveur_flux(opt: Options, adresse: &str) {
@@ -1574,19 +1686,28 @@ fn run_ppl_reparti(opt: Options, pair: &str) {
@@ -1604,6 +1725,45 @@ fn run_ppl_reparti(opt: Options, pair: &str) {
@@ -1623,22 +1783,17 @@ fn run_ppl_reparti(opt: Options, pair: &str) {
@@ -1646,6 +1801,17 @@ fn run_ppl_reparti(opt: Options, pair: &str) {
@@ -1658,6 +1824,7 @@ fn run_ppl_reparti(opt: Options, pair: &str) {
  ```

### 🤖 Assistant

⏵ Rédaction du rapport d'audit

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"DRAVE_VISION_TEXTE\\|run_banc_vision(&f)\\|run_banc_vision(sortie\\|recevoir_flux(&mut sock\\|fn recevoir_flux\\|fn envoyer_flux\\|let act = mdl.map(Act::du_modele)\" drave-core/src/main.rs && echo \"--- nb drapeaux ---\" & … [210 caractères tronqués]`

  ```
47:    if let Some(f) = opt.banc_vision.clone() { run_banc_vision(&f); return; }
857:fn run_banc_vision(sortie: &str) {
1161:    // `DRAVE_VISION_TEXTE=<modele.gguf>` charge le modèle de texte et lui impose le
1170:        let chemin = std::env::var("DRAVE_VISION_TEXTE").unwrap_or_default();
1353:fn envoyer_flux(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos: u32,
1356:    let act = mdl.map(Act::du_modele).unwrap_or(Act { levels: 127.0, thresh: 0.0,
1461:fn recevoir_flux(s: &mut std::net::TcpStream, hidden: usize) -> std::io::Result<Flux> {
1591:        match recevoir_flux(&mut sock, hidden) {
1745:            let rep = recevoir_flux(&mut sock, mdl.cfg.hidden).expect("réception du lot");
1786:        let rep = recevoir_flux(&mut sock, mdl.cfg.hidden).expect("réception du flux");
--- nb drapeaux ---
84
    tete.push(act.renorm as u8);
    assert_eq!(tete.len(), TAILLE_TETE,
               "en-tête de flux de {} octets pour {TAILLE_TETE}", tete.len());
    s.write_all(&tete)?;
    s.write_all(&corps)?;
    s.flush()?;
    Ok((TAILLE_TETE + corps.len(), n))
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"act.levels.to_le_bytes\\|act.thresh.to_le_bytes\\|act.topk.to_le_bytes\\|act.renorm as u8\" drave-core/src/main.rs && sed -n '1265,1271p' drave-core/src/main.rs", "description": "Lignes exactes de l'en-tête Act"}`

  ```
1412:    tete.extend_from_slice(&act.levels.to_le_bytes());
1413:    tete.extend_from_slice(&act.thresh.to_le_bytes());
1414:    tete.extend_from_slice(&act.topk.to_le_bytes());
1415:    tete.push(act.renorm as u8);
1442:    tete.extend_from_slice(&act.levels.to_le_bytes());
1443:    tete.extend_from_slice(&act.thresh.to_le_bytes());
1444:    tete.extend_from_slice(&act.topk.to_le_bytes());
1445:    tete.push(act.renorm as u8);
struct Act {
    levels: f32,
    thresh: f32,
    topk: u32,
    renorm: bool,
}
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md", "content": "# Drapeaux et variables « analysés mais jamais appliqués » — audit systématique\n\n**Révision auditée** : `drave-core/src/main.rs` sha256 `1726f9ac3665c3ce…` (2 999 lignes),\n`drave-core/ … [18467 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Vérification des dernières références citées dans le rapport

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"--- model.rs ---\" && grep -n \"let lot = self.lot.max(1)\\|if self.moe_topk > 0\\|Self::flux_lot(&mut self.trace\" drave-core/src/model.rs && echo \"--- main.rs ---\" && grep -n \"let mut conversation\\|mdl.generate(&ids, n_n … [341 caractères tronqués]`

  ```
--- model.rs ---
2200:            Self::flux_lot(&mut self.trace, &mut self.flux_force, &mut self.jeton_trace,
2410:            Self::flux_lot(&mut self.trace, &mut self.flux_force, &mut self.jeton_trace,
2417:                let k = if self.moe_topk > 0 { self.moe_topk } else { self.cfg.n_expert_used };
3083:                let k = if self.moe_topk > 0 { self.moe_topk } else { cfg.n_expert_used };
3505:        let lot = self.lot.max(1);
--- main.rs ---
412:        // CHAQUE branche rend le nombre d'arguments consommés (1 pour un
490:            "--flux-liste" => { o.flux_liste = true; 1 }
491:            "--flux-blocs" => { o.flux_blocs = true; 1 }
666:        let mut conversation = String::new();
700:            let (out, st) = mdl.generate(&ids, n_new, temp, top_p, rep_pen, hist,
712:    let (out, st) = if topk > 0 {
749:        mdl.generate(&ids, n_new, temp, top_p, rep_pen, hist, cb)
1669:    let limite = opt.limit.max(1).min(ctx);
--- depuis ---
2663:        ids_file: idfile, texte_file, ppl_texte: _, limit, depuis,
2688:            // `--depuis N` : on charge N jetons de plus que la limite, pour que
2690:            .take(limit.saturating_add(depuis))
2711:                pr
… [565 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"opt.matrix\" drave-core/src/main.rs && echo \"--- flux_force lot ---\" && grep -n \"flux_force.as_mut()\" drave-core/src/model.rs && echo \"--- PR mode ---\" && sed -n '1677,1682p' drave-core/src/main.rs && echo \"--- I des … [120 caractères tronqués]`

  ```
2053:    let mx = g.mxfp4_blocks(&opt.matrix).is_some();
2054:    let nom_q6k = opt.matrix.clone();
2058:    let nom_q4k = opt.matrix.clone();
2063:    let nom = if mx { opt.matrix.clone() } else if g.tensor("output.weight").is_some() {
--- flux_force lot ---
2810:                let r = self.flux_force.as_mut().unwrap();
3063:            if let Some(r) = self.flux_force.as_mut() {
--- PR mode ---
    let mode = if opt.flux_blocs { MODE_BLOCS }
               else if opt.flux_liste { MODE_LISTE }
               else { MODE_DENSE };
    println!("[flux] quantification : {} niveaux, seuil {}, top-k {}, renorm {}",
             mdl.act_levels, mdl.act_thresh, mdl.act_topk, mdl.act_renorm);
    let n_layer = mdl.cfg.n_layer;
--- I destructure ---
    let Options {
        ids: mut ids, ids_file, prompt, n: n_new, temp, top_p, topk, rep_pen, hist,
        flux, session, chat, ctx: ctx_opt, threads: threads_opt, abits: abits_opt,
        ctx_impose, threads_impose, abits_impose, dense, auto, q4, b6,
        keep, attn_window, swa_pattern, sans_fenetre, attn_sinks, attn_topk, qk_topk,
        act_thresh, act_topk, act_renorm, topk_proj, moe_topk, patch: patch_file,
        hebb_layer, heb
… [79 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md", "old_string": "| `--dense` | I (550) · P (2707) · BM (1835) | FS/PR : sans effet car `dense=true` y est déjà forcé — pas de perte, mais le drapeau n'est pas lu ; BV/BK : ignoré | 🟡 |", "new_string":  … [224 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md", "old_string": "| `--lot` | I (555→`generate`, model.rs:3517) · P (2867) · **PR (1674, nouveau)** |", "new_string": "| `--lot` | I (555→`generate`, model.rs:3505) · P (2867) · **PR (1674, nouveau)** | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md", "new_string": "| `--moe-topk` | I (552) · P (2739) | FS/PR : jamais lu. Inerte sur modèle dense (model.rs:2417 et 3083 : lu seulement si `n_expert > 0`) | 🔴 (MoE) |", "old_string": "| `--moe-topk` |  … [126 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md", "new_string": "| `DRAVE_FLUX_VERIF` | Une **seule** occurrence : `forward` jeton par jeton (model.rs:2807) | **Muet dès que `--lot > 1`** : le chemin par lots applique bien le rejeu (`flux_lot`, mode … [304 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md", "new_string": "| `--depuis` | P (2690, 2731, fenêtrage 2794-2806) | Ailleurs : *sans objet* | — |", "old_string": "| `--depuis` | P (2690 et fenêtrage 2805-2830) | Ailleurs : *sans objet* | — |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md", "new_string": "| `--matrix` | D (68) · GB (2053-2063) | Ailleurs : *sans objet* (hérité du banc d'origine) | — |\n| `--couches-locales` `--flux-liste` `--flux-blocs` | PR seulement (1670, 1677-1679)  … [260 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md", "new_string": "- **46 drapeaux (55 %) sont ignorés dans au moins un mode où ils devraient s'appliquer**,\n  dont 20 classés 🔴 (silencieux, et ils changent les chiffres dès que le réglage a un effet\n … [470 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md", "limit": 60}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md</path>
<type>file</type>
<content>
1: # Drapeaux et variables « analysés mais jamais appliqués » — audit systématique
2: 
3: **Révision auditée** : `drave-core/src/main.rs` sha256 `1726f9ac3665c3ce…` (2 999 lignes),
4: `drave-core/src/model.rs` sha256 `1d7eacc506db6cab…` (3 675 lignes), 30/09 11:54.
5: Le dépôt était en cours d'édition pendant l'audit (zone flux / préremplissage réparti) :
6: les numéros de ligne cités sont ceux de cette révision, et **les chemins audités† sont hors
7: des hunks modifiés** (`git diff` ne touche que la zone ≥ l. 1 240). † mode par défaut,
8: `--infer`, `--ppl`, `--plan`, boucle d'analyse.
9: 
10: **Périmètre** : 84 drapeaux `--xxx` extraits de `analyser()` (main.rs:396-519) et 26 variables
11: `DRAVE_*` (27 chaînes, dont le préfixe cité dans un message). Pour chacun : recherche du **site
12: d'application réelle** (`mdl.champ = …`, argument de `Model::load(…)`, `std::env::var`),
13: puis de tous les modes qui ne le lisent pas.
14: 
15: **Convention de lecture.** I = `--infer` · P = `--ppl`/`--ppl-texte` · PL = `--plan` ·
16: T = `--tokenize` · FS = `--flux-serv
… [4976 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum drave-core/src/main.rs && stat -c '%y' drave-core/src/main.rs && wc -l reports/rapport-drapeaux-ignores.md && grep -c \"^|\" reports/rapport-drapeaux-ignores.md", "description": "Vérifier la stabilité de la source et le rap … [6 caractères tronqués]`

  ```
1726f9ac3665c3ce02bc0b963d26bc9e2910f153ee1aaf45c9ddeed79bb7e1f0  drave-core/src/main.rs
2026-09-30 11:54:25.370717707 -0400
234 reports/rapport-drapeaux-ignores.md
62
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"§[0-9]\" reports/rapport-drapeaux-ignores.md", "description": "Repérer les renvois de section"}`

  ```
46:| `--keep` | I seulement : `Model::load(…, keep, …)` (550) | **P : `Model::load(…, 1.0, …)` en dur (2707)** · FS (1575) · PR (1675) · BM (1835) · BV (1172). Vérifié empiriquement (§4.2) | 🔴 |
50:| `--threads` | I (548) · P (2678) · BK (1937) · GB (2047) | **FS (1575), PR (1675), BM (1835), BV (1172) : `16` en dur** · **D : avalé par la boucle `i += 2`** (main.rs:65-73, §4.4) | 🟠 |
51:| `--ctx` | I (547) · P (2677) · FS (1574) · PR (1668) · PL (2444) | **BM (1835 : `4096` en dur)** · **BV (1172 : `512` en dur)** · et en **PL le défaut 512 masque le contexte déclaré** (§4.3) | 🟠 |
83:| `--ffn-gain` | P : 2750 | **I : jamais déstructuré** (bloc 535-542) ni appliqué. Vérifié empiriquement (§5.2) | 🔴 |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -i 's/Vérifié empiriquement (§4\\.2)/Vérifié empiriquement (§7.1)/; s/main\\.rs:65-73, §4\\.4/main.rs:65-73, §7.4/; s/le contexte déclaré\\*\\* (§4\\.3)/le contexte déclaré** (§7.3)/; s/Vérifié empiriquement (§5\\.2)/Vérifié empi … [164 caractères tronqués]`

  ```
46:| `--keep` | I seulement : `Model::load(…, keep, …)` (550) | **P : `Model::load(…, 1.0, …)` en dur (2707)** · FS (1575) · PR (1675) · BM (1835) · BV (1172). Vérifié empiriquement (§7.1) | 🔴 |
50:| `--threads` | I (548) · P (2678) · BK (1937) · GB (2047) | **FS (1575), PR (1675), BM (1835), BV (1172) : `16` en dur** · **D : avalé par la boucle `i += 2`** (main.rs:65-73, §7.4) | 🟠 |
51:| `--ctx` | I (547) · P (2677) · FS (1574) · PR (1668) · PL (2444) | **BM (1835 : `4096` en dur)** · **BV (1172 : `512` en dur)** · et en **PL le défaut 512 masque le contexte déclaré** (§7.3) | 🟠 |
83:| `--ffn-gain` | P : 2750 | **I : jamais déstructuré** (bloc 535-542) ni appliqué. Vérifié empiriquement (§7.2) | 🔴 |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md", "offset": 60, "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md</path>
<type>file</type>
<content>
60: |---|---|---|---|
61: | `--topk-q` `--topk-k` `--topk-v` `--topk-o` `--topk-gate` `--topk-up` `--topk-down` | I (557) · P (2755) | **FS et PR** : `appliquer_quantification` (1214-1220) ne pose que niveaux/seuil/top-k/renorm ; **et l'en-tête de flux ne transporte que ces quatre champs** (`Act` 1265-1270, écriture 1412-1415 et 1442-1445, `TAILLE_TETE` 1261). Les deux nœuds divergent donc **en silence** — exactement ce que le commentaire 1250-1256 dit vouloir empêcher | 🔴🔴 |
62: | `--moe-topk` | I (552) · P (2739) | FS/PR : jamais lu. Inerte sur modèle dense (model.rs:2417 et 3083 : lu seulement si `n_expert > 0`) | 🔴 (MoE) |
63: | `--attn-topk` `--qk-topk` | I (564-565) · P (2756-2757) | FS/PR : ni appliqués ni transportés (mêmes preuves que ci-dessus) | 🔴 |
64: | `--attn-window` | I (559) · P (2759) | FS/PR/BM/BV/BK/GB/PL/D : jamais lu. `--attn-window 0` est de plus ignoré (condition `> 0`) : pour l'annuler il faut `--sans-fenetre` | 🔴 |
65: | `--sans-fenetre` | I (558) · P (2760) | Idem. **Précédence inversée entre I et P** : en I `--attn-window` l'emport
… [9002 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"    pub fn forward\\b\\|    pub fn forward(\\|pub fn forward_lot\\|pub fn forward_mla\\|fn rope_yarn\\|rotation : YaRN\\|\\[config\\] rotation\" drave-core/src/model.rs && echo \"--- contexte 3055-3070 ---\" && sed -n '3055 … [373 caractères tronqués]`

  ```
1360:                println!("[config] rotation : YaRN ×{f}{} (contexte demandé {ctx} > {o} initial)",
1363:                println!("[config] rotation : RoPE simple (contexte {ctx} ≤ {o} initial ; \
1366:                println!("[config] rotation : RoPE simple (YaRN ×{f} refusé, contexte {ctx} > {o})"),
1367:            _ => println!("[config] rotation : RoPE simple (le modèle ne déclare pas YaRN)"),
2014:    fn rope_yarn(v: &mut [f32], n_head: usize, head_dim: usize, pos: usize, base: f32,
2098:    pub fn forward_lot(&mut self, toks: &[u32], pos0: usize) -> Vec<Vec<f32>> {
2620:    pub fn forward_mla(&mut self, tok: u32, pos: usize) -> Vec<f32> {
2731:    pub fn forward(&mut self, tok: u32, pos: usize) -> Vec<f32> {
--- contexte 3055-3070 ---
                    for (o, x) in out.iter_mut().zip(vd.iter()) { *o += w * x; }
                }
            }
            self.prof[2] += ta.elapsed().as_secs_f64();
            let tf = Instant::now();
            Self::matvec(pool, &lay.wo, &att, &mut o, events, self.act_levels, self.act_thresh, tk(3), self.act_renorm, &mut scratch, self.seuil_push);
--- quelle fonction contient 3063 ? ---
derniere fonction avant 3063 -> 2731:     pub
… [58 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md", "new_string": "| `DRAVE_FLUX_VERIF` | Une **seule** occurrence : `forward` jeton par jeton (model.rs:2807) | **Muet dès que `--lot > 1`** : le chemin par lots applique bien le rejeu (`flux_lot`, mode … [316 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md", "new_string": "| `--sans-yarn` | I (566) · P (2758) → `cfg_yarn_off` (model.rs:1750) | FS/PR/BM/BV/BK/GB/PL/T/D : jamais appelé. **De plus la trace `[config] rotation` (model.rs:1360-1367) est imprim … [492 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md", "offset": 180}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-drapeaux-ignores.md</path>
<type>file</type>
<content>
180: *Note : toutes les exécutions affichent au passage l'avertissement `QT_IM_SWITCHER … rien n'a
181: été appliqué`, faux positif de `main.rs:41-44`.*
182: 
183: ---
184: 
185: ## 8. Recommandation : un tableau de bord `--options-actives`, et trois garde-fous
186: 
187: **L'idée simple** : un drapeau `--options-actives` (et `--options-strict`) qui imprime, au
188: début de chaque mode, **les réglages réellement en vigueur**, lus sur le modèle *après* toutes
189: les affectations (`mdl.act_levels`, `mdl.act_thresh`, `mdl.attn_window`, `mdl.keep`…), et qui
190: signale explicitement chaque drapeau présent dans `argv` mais absent de cette liste :
191: 
192: ```
193: [options] --keep 0.05      : IGNORÉ dans ce mode (--ppl charge toujours le modèle entier)
194: [options] --threads 4      : inactif (le mode utilise 16 fils en dur)
195: [options] act_levels=65535  act_thresh=0.05  attn_window=0  moe_topk=0  lot=1  topk_proj=[0;7]
196: ```
197: 
198: Mise en œuvre minimale : une fonction `enregistrer(nom, valeur)` appelée **à chaque site
199: d'application** (`mdl.
… [2777 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle final du rapport et de la stabilité de la révision

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"--- lignes de tableau avec un nombre de colonnes != 4 ---\" && awk -F'|' '/^\\|/ && NF!=6 {print NR\": NF=\"NF}' reports/rapport-drapeaux-ignores.md && echo \"(rien ci-dessus = tables bien formées)\" && echo \"--- révision sou … [161 caractères tronqués]`

  ```
--- lignes de tableau avec un nombre de colonnes != 4 ---
(rien ci-dessus = tables bien formées)
--- révision source ---
1726f9ac3665c3ce02bc0b963d26bc9e2910f153ee1aaf45c9ddeed79bb7e1f0  drave-core/src/main.rs
2026-09-30 11:54:25.370717707 -0400
mer 30 sep 2026 11:59:07 EDT
  ```

### 🤖 Assistant

⏵ Envoi du résultat à l'agent parent

- **send_message** `{"agent_id": "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", "message": "Audit « drapeaux analysés mais jamais appliqués » TERMINÉ. Livrable : reports/rapport-drapeaux-ignores.md (234 lignes, français, tableaux + preuves + recommandation).\n\nRévision auditée : main.rs sha256 1726f9ac… (2999 l., mtime 11:54 … [3438 caractères tronqués]`

  ```
message delivered to agent bbd6969f-0f70-42b2-8951-64d1f2f36d2e
  ```

### 🤖 Assistant

⏵ Audit terminé, rapport écrit et transmis au parent

Rapport écrit : `reports/rapport-drapeaux-ignores.md` (234 lignes, français, tableaux + preuves de code + 4 vérifications empiriques + recommandation).

**Résumé (10 lignes)**
1. **110 options auditées** : 84 drapeaux `--xxx` (extraits d'`analyser`, main.rs:396-519) + 26 variables `DRAVE_*`.
2. **46 drapeaux (55 %) sont ignorés dans au moins un mode où ils devraient s'appliquer**, dont 20 classés critiques ; 5 de plus le sont sur le sous-chemin `--topk` de l'inférence ; 1 variable (`DRAVE_FLUX_VERIF`) est muette dès `--lot > 1`.
3. **N°1** — `--topk-q/-k/-v/-o/-gate/-up/-down` (+ `--attn-topk`, `--qk-topk`, `--moe-topk`) ne sont ni appliqués ni transportés en `--flux-serveur`/`--ppl-reparti` : **deux nœuds divergent en silence** (main.rs:1214-1220 ; en-tête `Act` 1265-1270, 1412-1415) — le correctif `--abits`/`--act-thresh` est donc incomplet.
4. **N°2** — `--keep` ignoré en `--ppl` (`Model::load(…, 1.0, …)` en dur, main.rs:2707) : PPL 1929.3230 **identique** avec et sans `--keep 0.05`, alors qu'en `--infer` les jetons changent.
5. **N°3** — `--ffn-gain` ignoré en `--infer` (prouvé : jetons `[6, 25010, 10, 4999]` avec et sans) alors qu'il fait passer la PPL de 1929,3 à 4949,5 en `--ppl`.
6. Autres : mode par défaut qui a gardé la boucle `i += 2` (`--dense --threads 4` → 30 fils, prouvé) · `--banc-vision` ne reçoit aucune `Options` · `--threads`=16 en dur en FS/PR/BM/BV · `--hebb-q`/`--hebb-out` en dur en `--ppl` · `--sans-yarn` ignoré en FS/PR et trace `[config] rotation` mensongère · `--plan` annonce 512 au lieu des 32768 déclarés · précédence `--sans-fenetre`/`--attn-window` inversée entre `--infer` et `--ppl`.
7. Ce qui est correct : `--abits/--act-thresh/--act-topk/--act-renorm` partout, `--pin` et `--bits` globaux (516-517), les réglages d'activation voyagent dans le flux, `--ppl-texte`/`--depuis`/`--trace-flux`+`--lot`/`--patch`/`--q4`.
8. Recommandation : `--options-actives` (imprime les réglages réellement en vigueur lus sur `mdl` après toutes les affectations, signale tout drapeau d'`argv` absent) + `--options-strict`, suppression des `..` dans les déstructurations, transport de tous les champs d'activation avec `VERSION_FLUX` incrémenté, test de non-régression sur la liste des 84 drapeaux.
9. Réserve : `main.rs` a été **modifié pendant l'audit** (zone flux, +167 lignes, `--lot` maintenant appliqué en `--ppl-reparti`) ; les numéros cités valent pour la révision `1726f9ac…` (2999 l., 11:54:25) et les chemins testés sont hors des hunks modifiés ; le binaire testé date de 11:41.
10. Aucune compilation, aucune modification hors le rapport, aucune commande lourde ni mode serveur.

