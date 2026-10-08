# Session DSH — relecture

- identifiant : `850eebf1-88b1-443e-b75e-6f89890b35ec`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-08 09:18:07
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : un moteur d'inférence écrit en Rust dans drave-core/, plus ~100 outils d'analyse en Python dans tools/, des rapports dans reports/, des sprints dans sprints/, et un fichier de reprise REPRISE.md).

MISSION : dresser l'inventaire FACTUEL et CHIFFRÉ de tout ce qui est mesuré dans ce dépôt sur la PARCIMONIE DES ACTIVATIONS et le MODE ÉVÉNEMENTIEL (exécution des projections en listes d'événements plutôt qu'en produit scalaire dense).

OÙ CHERCHER : drave-core/src/ (notamment model.rs et main.rs : options --flux, topk, seuil/thresh, act_levels, k-WTA, la fonction quant_scratch, l'encodage DRVF v1/v2/v3, les « listes d'événements »), tools/flux_codec.py, tools/granularite_flux.py, tools/trace_compacite.py, tools/approximabilite_bloc.py, reports/*.md, docs/*.md, sprints/*.md, REPRISE.md.

RENDS un rapport en français, structuré ainsi, et pour CHAQUE chiffre cite le fichier (avec le numéro de ligne quand c'est possible) :
1. LE MÉCANISME EXACT : comment un « événement » est défini (seuil ? top-k ? k-WTA ? quantification ?), quels réglages existent, leurs valeurs par défaut, et comment le moteur passe d'un tenseur dense à une liste d'événements.
2. LES TAUX D'ACTIVITÉ MESURÉS (% de canaux actifs, nombre d'événements par couche ou par jeton) par modèle et par couche : un tableau, avec la source de chaque ligne.
3. LES GAINS MESURÉS du mode événementiel contre le mode dense (temps, octets lus, mémoire), et à quelles conditions précises ils tiennent (modèle, taille, matériel).
4. LES TROUS : ce qui n'est PAS mesuré, ce qui est supposé, ce qui est déduit sans mesure.
5. LES HYPOTHÈSES RÉFUTÉES sur ce terrain, avec les chiffres qui les réfutent.

CONTRAINTES : ne modifie AUCUN fichier, ne lance aucune compilation. Sois factuel et sobre ; distingue explicitement « mesuré », « déduit » et « supposé ». Si une information est absente, écris-le plutôt que de l'inventer. Ton rapport final doit tenir en 150 lignes maximum, dense en chiffres.
Your parent agent id is "d31b3d9b-58e4-4d34-85fa-381b6f6a6a76". Before you finish, send your result to that agent with send_message({ agent_id: "d31b3d9b-58e4-4d34-85fa-381b6f6a6a76", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Cartographie du dépôt et repérage des sources sur la parcimonie/événementiel

Je commence par l'inventaire des fichiers et une recherche ciblée sur les mots-clés.

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet", "description": "List repository root"}`

  ```
total 308
drwxr-xr-x. 1 stephane stephane    612  7 oct 18:16 .
drwxr-xr-x. 1 stephane stephane   2374  3 oct 10:09 ..
drwxr-xr-x. 1 stephane stephane     40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane     56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane     96  1 oct 06:58 data
drwxr-xr-x. 1 stephane stephane   1130  5 oct 13:47 docs
drwxr-xr-x. 1 stephane stephane     82 28 sep 11:58 drave-core
drwxr-xr-x. 1 stephane stephane    164  8 oct 09:11 .git
-rw-r--r--. 1 stephane stephane    399 30 sep 10:01 .gitignore
drwxr-xr-x. 1 stephane stephane     34 27 sep 11:39 journal
drwxr-xr-x. 1 stephane stephane     88 25 sep 17:13 models
drwxr-xr-x. 1 stephane stephane    114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane   4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-------. 1 stephane stephane  36518  2 oct 10:21 README.md
drwxr-xr-x. 1 stephane stephane   4256  7 oct 18:22 reports
-rw-------. 1 stephane stephane 120322  5 oct 16:21 REPRISE.md
-rw-------. 1 stephane stephane   8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane  10507 30 sep 08:44 run_clusters.py
-rw-------. 1 stephane stephane  12507 30 sep 08:44 run_cpu.py
-rw-------. 1 stephan
… [708 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports 2>&1 | head -200", "description": "List key source directories"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src:
total 1408
drwxr-xr-x. 1 stephane stephane    214  5 oct 09:26 .
drwxr-xr-x. 1 stephane stephane     82 28 sep 11:58 ..
-rw-------. 1 stephane stephane  24376  1 oct 12:08 clusters.rs
-rw-r--r--. 1 stephane stephane  48545  3 oct 15:36 engine.rs
-rw-r--r--. 1 stephane stephane  24423  2 oct 17:26 engram.rs
-rw-r--r--. 1 stephane stephane  81296  2 oct 23:55 formats.rs
-rw-------. 1 stephane stephane 112072  3 oct 10:30 gguf.rs
-rw-r--r--. 1 stephane stephane  78414 30 sep 20:15 gpu.rs
-rw-------. 1 stephane stephane  94592  7 oct 19:41 kimi_k3.rs
-rw-------. 1 stephane stephane  75095  2 oct 23:55 list.rs
-rw-r--r--. 1 stephane stephane 310484  7 oct 20:37 main.rs
-rw-------. 1 stephane stephane  21464  1 oct 22:40 materiel.rs
-rw-r--r--. 1 stephane stephane 521949  5 oct 09:50 model.rs
-rw-------. 1 stephane stephane  26530  3 oct 10:41 tokenizer.rs

/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports:
total 1256
drwxr-xr-x. 1 stephane stephane   4256  7 oct 18:22 .
drwxr-xr-x. 1 stephane stephane    612  7 oct 18:16 ..
-rw-r--r--. 1 stephane stephane    386  1 oct 09:38 aiguille-30b.md
-rw-r--r--. 1 stephane step
… [13127 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des mécanismes événementiels dans le code Rust et Python

- **grep** `{"pattern": "quant_scratch", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src"}`

  ```
Found 13 matches

drave-core/src/model.rs
Line 4401:     fn quant_scratch(x: &[f32], levels: f32, thresh: f32, topk: usize, renorm: bool,
Line 4473:         let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
Line 4564:             Self::quant_scratch(x, levels, thresh, topk, renorm, scratch)
Line 4618:             let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
Line 4642:         let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
Line 5327:         // Quantification d'un lot : mêmes règles que `quant_scratch`.
Line 7029:                 if let Some((sv, sx)) = Self::quant_scratch(&hn, self.act_levels, self.act_thresh,
Line 7522:                 if let Some((sv, sx)) = Self::quant_scratch(&hn, self.act_levels, self.act_thresh,
Line 7812:             let (sv, sx) = match Self::quant_scratch(hi, self.act_levels, self.act_thresh,
Line 7939:         match Self::quant_scratch(x, 32767.0, self.act_thresh, self.act_topk,
Line 8062:         let (sv, sx) = match Self::quant_scratch(h, self.act_levels, self.act_thresh,
Line 8225:         let (sv, sx) = match Self::quant_scra
… [157 caractères tronqués]
  ```

- **grep** `{"pattern": "act_levels|act-levels|k_wta|k-wta|kWTA", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
Found 173 matches

tools/premiere_couche_semantique.py
Line 118:     Le moteur quantifie chaque enregistrement sur `act_levels = 127` niveaux :

drave-core/src/model.rs
Line 2399:     pub act_levels: f32,
Line 4339:             ctx, events: 0, paires: [0; 3], act_levels: 127.0, act_thresh: 0.0, act_topk: 0, act_renorm: false,
Line 5352:             quantifier(&hn, &mut xi, &mut sx, self.act_levels, self.act_thresh);
Line 5378:                                      &mut self.events, &mut self.paires[0], self.act_levels,
Line 5546:                 quantifier(&att, &mut ai[..t * n_in_wo], &mut sa, self.act_levels, self.act_thresh);
Line 5570:             quantifier(&hn, &mut xi, &mut sx, self.act_levels, self.act_thresh);
Line 5682:                         let ech = if mx > 0.0 { mx / self.act_levels } else { 1.0 };
Line 5725:                 quantifier(&gate, &mut gi, &mut sg, self.act_levels, self.act_thresh);
Line 7029:                 if let Some((sv, sx)) = Self::quant_scratch(&hn, self.act_levels, self.act_thresh,
Line 7087:                 Self::matvec(pool, &lay.wq, &hn, &mut q, events, &mut paires[0], self.act_levels, self.act_thresh, tk(0), self.act_renorm, &mut scratch, self
… [24106 caractères tronqués]
  ```

- **grep** `{"pattern": "DRVF", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
Found 250 of 478 matches

REPRISE.md
Line 34: > protocole v4, DRVF v2/v3, plafond R4, tableau de bord) : Qwen ctx 256 =
Line 877: | `DRAVE_TRACE_BLOCS=1` | trace DRVF **v3** : valeurs i8, échelle f16 par bloc de 32 | 45 079 930 o contre 66 370 408 en v2 (−32 %), rejeu 19,4029 contre 19,3885 (+0,074 %) |

sprints/26-la-porte-a-512-et-la-granularite-qui-route.md
Line 63: **65 536 octets** en f32), avec l'encodeur DRVF de référence :

sprints/22-la-composition-verifiee-et-les-deux-portes.md
Line 46:    lisait la version 1 du format DRVF (indice u32 + i16) ; le moteur écrit la 2

reports/recapitulatif.md
Line 29: On ne lit du professeur que **la couche qu'on veut émuler**, par des traces DRVF

reports/rapport-plateau-semantique.md
Line 19: `--trace-flux` et lue en DRVF.

tools/trace_gpu.py
Line 18: LE FORMAT EST CELUI DU MOTEUR — DRVF v2, via `flux_codec.encoder`. C'est
Line 23: LA QUANTIFICATION EN i16 EST CELLE DU MOTEUR AUSSI. DRVF v2 stocke des entiers
Line 100:         # « couche c » d'une trace DRVF est l'entrée NORMALÉE de l'attention du
Line 138:               f"et il faut passer en DRVF v3 (échelles) avant de s'en servir.")

sprints/12-la-rotation-des-couches-compressees.md
Li
… [41514 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du cœur Rust : quant_scratch, seuils, top-k et défauts

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "offset": 4330, "limit": 60}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "offset": 4390, "limit": 300}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
4330:         } else { None };
4331:         Model {
4332:             g, cfg, layers, out_norm, pool,
4333:             mla4, mla4_cache, mla4_comp_kv, mla4_comp_gate, mla4_cles_comp,
4334:             mla4_idx_kv, mla4_idx_gate, mla4_idx_cles, mla4_idx_scores,
4335:             hc, hc_tete, hc_retarde,
4336:             engram, engram_poids, historique: Vec::new(),
4337:             hc_porte_flux: None, hc_porte_imposee: None,
4338:             kv: caches_kv,
4339:             ctx, events: 0, paires: [0; 3], act_levels: 127.0, act_thresh: 0.0, act_topk: 0, act_renorm: false,
4340:             act_topk_proj: [0; 7], attn_topk: 0, attn_events: 0, qk_topk: 0,
4341:             moe_topk: 0,
4342:             profil_neurones: None,
4343:             profil_experts: None,
4344:             // Trace de routage des experts : c'est la matière première du
4345:             // découpage en clusters (quels experts sont allumés ENSEMBLE). Le
4346:             // fichier est créé (tronqué) au chargement, tamponné, et fermé avec
4347:             // le modèle — une exécution = une tr
… [2401 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
4390:     // ----------------------------------------------------------------------- //
4391: 
4392:     /// Quantifie un vecteur (une échelle pour tout le vecteur).
4393:     #[inline]
4394:     /// Parcimonie effective d'une projection : la valeur par projection prime,
4395:     /// sinon on retombe sur le réglage global.
4396:     #[inline]
4397:     pub fn topk_de(&self, proj: usize) -> usize {
4398:         if self.act_topk_proj[proj] > 0 { self.act_topk_proj[proj] } else { self.act_topk }
4399:     }
4400: 
4401:     fn quant_scratch(x: &[f32], levels: f32, thresh: f32, topk: usize, renorm: bool,
4402:                      scratch: &mut Vec<f32>) -> Option<(SparseVec, f32)> {
4403:         let mut mx = 0f32;
4404:         for &v in x { let a = v.abs(); if a > mx { mx = a; } }
4405:         if mx == 0.0 { return None; }
4406:         let s = mx / levels;
4407:         let inv = 1.0 / s;
4408:         // seuil absolu correspondant à la fraction demandée du maximum
4409:         let seuil = (thresh * levels) as i32;
4410:         let mut sv = SparseVec { idx: Vec::wit
… [16888 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des définitions de champs et des options CLI associées

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 130, "offset": 2380}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
2380:     pub kv: Vec<KvCache>,
2381:     pub ctx: usize,
2382:     pub events: u64,
2383:     /// **Paires** (poids × activation) effectivement multipliées, par
2384:     /// provenance : 0 = attention, 1 = experts routés, 2 = partagé (FFN dense,
2385:     /// expert partagé, tête).
2386:     ///
2387:     /// Pourquoi une seconde mesure à côté des `events` : les chemins qui
2388:     /// **déquantifient** (IQ, formats sans noyau) et le chemin MLA en f32 ne
2389:     /// construisent aucune liste, donc ne produisent aucun événement — le
2390:     /// rapport annonçait « 0 événement » pour des modèles qui calculaient des
2391:     /// milliards de produits. Une paire est ce qu'on **paie** : un chemin en
2392:     /// listes ne paie que ses poids non nuls, un chemin dense paie la matrice
2393:     /// entière, et l'écart entre les deux est exactement ce que le croisement
2394:     /// push/pull de 22 % arbitre (`reports/rapport-croisement-push-pull.md`).
2395:     pub paires: [u64; 3],
2396:     /// Nombre de niveaux de quantification des **activations** (127 pour int8,
2
… [7632 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -- '\"--act-thresh\"\\|\"--act-levels\"\\|\"--topk\"\\|\"--renorm\"\\|\"--flux\"\\|\"--act-topk\"\\|\"--seuil-push\"\\|\"--options-actives\"\\|\"--attn-topk\"\\|\"--qk-topk\"\\|\"--moe-topk\"\\|\"--abits\"' drave-core/src/mai … [63 caractères tronqués]`

  ```
701:            "--options-actives" => { o.options_actives = true; 1 }
731:            "--topk" => { o.topk = suivant(i).parse().unwrap(); 2 }
736:            "--abits" => { o.abits = suivant(i).parse().unwrap(); o.abits_impose = true; 2 }
742:            "--moe-topk" => { o.moe_topk = suivant(i).parse().unwrap(); 2 }
746:            "--attn-topk" => { o.attn_topk = suivant(i).parse().unwrap(); 2 }
747:            "--qk-topk" => { o.qk_topk = suivant(i).parse().unwrap(); 2 }
754:            "--act-thresh" => { o.act_thresh = suivant(i).parse().unwrap(); 2 }
755:            "--act-topk" => { o.act_topk = suivant(i).parse().unwrap(); 2 }
770:            "--flux" => { o.flux = true; 1 }
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 110, "offset": 690}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 140, "offset": 2470}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
690:             // 1,5 To. Ce n'est PAS une vérification (la référence ne tourne pas
691:             // sur un modèle incomplet) — juste : ça charge, ça calcule, ça sort
692:             // des valeurs finies et plausibles.
693:             "--k3-essai" => { o.k3_essai = true; 1 }
694:             "--banc-kv" => { o.banc_kv = suivant(i).parse().unwrap(); 2 }
695:             "--banc-topk" => { o.banc_topk = suivant(i).parse().unwrap(); 2 }
696:             "--banc-mla" => { o.banc_mla = Some(suivant(i).clone()); 2 }
697:             "--tensors" => { o.tensors = true; 1 }
698:             "--trace-flux" => { o.trace_flux = Some(suivant(i).clone()); 2 }
699:             "--flux-forcer" => { o.flux_forcer = Some(suivant(i).clone()); 2 }
700:             "--flux-serveur" => { o.flux_serveur = Some(suivant(i).clone()); 2 }
701:             "--options-actives" => { o.options_actives = true; 1 }
702:             "--options-strict" => { o.options_strict = true; 1 }
703:             "--tete-partielle" => { o.tete_partielle = true; 1 }
704:             "--ppl-reparti" => { o.ppl_
… [7151 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
2470: ///
2471: /// Les activations quantifiées circulent en `i16` (les noyaux d'experts prennent
2472: /// `&[i16]`) et les conversions saturent à ±32 767. Au-delà de 16 bits, les
2473: /// valeurs quantifiées dépassent cette borne : elles étaient SILENCIEUSEMENT
2474: /// ramenées à 32 767, ce qui revient à diviser l'activation par 2^(abits−16) —
2475: /// mesuré sur V4.1 : `--abits 16` donne 12 889 de perplexité, `--abits 24` en
2476: /// donne 127 496 (10× pire), sans un mot. On borne donc, et on le DIT.
2477: fn niveaux_activation(abits: u32) -> f32 {
2478:     let abits = abits.clamp(1, 16);
2479:     ((1u32 << (abits - 1)) - 1) as f32
2480: }
2481: 
2482: /// Applique `--abits` en le bornant, en ANNONÇANT la borne.
2483: fn poser_niveaux(mdl: &mut model::Model, abits: u32, source: &str) {
2484:     if abits > 16 {
2485:         eprintln!("[activation] --abits {abits} demandé ({source}) : borné à 16 (32 767 \
2486: niveaux), la borne du stockage i16 des activations quantifiées. Au-delà, les valeurs \
2487: étaient silencieusement saturées et le calcul faux d'un fact
… [6619 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"act_thresh\\|act_topk\\|act_renorm\\|seuil_push\\|act_levels\" drave-core/src/main.rs", "description": "Locate sparsity settings in main.rs"}`

  ```
450:             mdl.act_levels, mdl.act_thresh, mdl.act_topk, mdl.act_renorm);
452:             mdl.attn_topk, mdl.qk_topk, mdl.moe_topk, mdl.act_topk_proj);
464:             mdl.attn_window, mdl.swa_pattern, mdl.seuil_push, mdl.lot,
603:    act_thresh: f32, act_topk: usize, act_renorm: bool, topk_proj: [usize; 7],
754:            "--act-thresh" => { o.act_thresh = suivant(i).parse().unwrap(); 2 }
755:            "--act-topk" => { o.act_topk = suivant(i).parse().unwrap(); 2 }
781:            "--act-renorm" => { o.act_renorm = true; 1 }
861:        act_thresh, act_topk, act_renorm, topk_proj, moe_topk, patch: patch_file,
904:    mdl.act_thresh = act_thresh;
905:    mdl.act_topk = act_topk;
907:    mdl.act_renorm = act_renorm;
908:    mdl.act_topk_proj = topk_proj;
945:    if act_topk > 0 || act_thresh > 0.0 {
947:                 act_topk as f32 / 10.0,
948:                 if act_thresh > 0.0 { format!(", seuil {:.1} %", act_thresh * 100.0) } else { String::new() });
2489:    mdl.act_levels = niveaux_activation(abits);
2495:    mdl.act_thresh = opt.act_thresh;
2496:    mdl.act_topk = opt.act_topk;
2497:    mdl.act_renorm = opt.act_renorm;
2501:    mdl.act_topk_proj = opt.topk_proj
… [1013 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"SparseVec\" drave-core/src/list.rs | head -30; echo \"=== struct ===\"; grep -n -A 20 \"pub struct SparseVec\" drave-core/src/list.rs", "description": "Inspect SparseVec definition"}`

  ```
=== struct ===
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"struct SparseVec\" drave-core/src/ ; echo \"=== row_ev / accumulate_push ===\"; grep -rn \"row_ev\\|fn accumulate_push\" drave-core/src/*.rs | head -20", "description": "Find SparseVec and push matrix definitions"}`

  ```
drave-core/src/engine.rs:29:pub struct SparseVec {
=== row_ev / accumulate_push ===
drave-core/src/engine.rs:752:    pub fn accumulate_push(&mut self, m: &PushMat, sv: &SparseVec) -> Vec<i64> {
drave-core/src/list.rs:83:    pub fn row_events<F: FnMut(usize, i32)>(&self, r: usize, mut f: F) {
drave-core/src/list.rs:237:    pub fn row_events_count(&self, r: usize, acc: &mut usize) {
drave-core/src/list.rs:270:    pub row_ev: Vec<u32>,       // événements par source
drave-core/src/list.rs:285:        let mut row_ev = vec![0u32; n_in];
drave-core/src/list.rs:303:                row_ev[i] += 1;
drave-core/src/list.rs:314:        PushMat { n_in, n_out, row_start, row_ev, data, scale, n_events }
drave-core/src/list.rs:1574:    /// repose le compteur de flux : `row_ev[i]` doit valoir exactement le nombre
drave-core/src/list.rs:1591:        assert_eq!(m.row_ev.iter().map(|v| *v as usize).sum::<usize>(), m.n_events);
drave-core/src/list.rs:1592:        assert_eq!(m.row_ev, vec![2, 1, 2, 1], "événements par source");
drave-core/src/list.rs:1595:        assert_eq!(m.row_ev[1], 1);
drave-core/src/main.rs:342:        for &s in &sv.idx { fused.row_events_count(s as usize, &mut ev); }
drave-core/s
… [190 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 30, "offset": 440}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
440: /// (`--keep` en perplexité, `--ffn-gain` en inférence, les top-k dans les modes
441: /// flux, `--trace-flux` en inférence, `--threads` figé…), et chacun était
442: /// INVISIBLE : la sortie ne disait nulle part quelle valeur agissait. Ici, elle
443: /// le dit — et une valeur qu'on ne voit pas bouger est une valeur qui ne sert à
444: /// rien.
445: fn options_actives(mdl: &model::Model, mode: &str, ctx_impose: bool, dense: bool, keep: f32) {
446:     let oui = |b: bool| if b { "imposé" } else { "défaut" };
447:     println!("[options] mode {mode} · contexte {} ({}) · dense {} · keep {:.3}",
448:              mdl.ctx, oui(ctx_impose), dense, keep);
449:     println!("[options] activation : niveaux {:.0} · seuil {} · k-WTA {} · renorm {}",
450:              mdl.act_levels, mdl.act_thresh, mdl.act_topk, mdl.act_renorm);
451:     println!("[options] top-k : attn {} · q·k {} · MoE {} · par projection {:?}",
452:              mdl.attn_topk, mdl.qk_topk, mdl.moe_topk, mdl.act_topk_proj);
453:     println!("[options] couches {}..{} · flux brut {} · trace {} · rejeu {}",
45
… [1200 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/engine.rs", "limit": 40, "offset": 20}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 110, "offset": 860}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/engine.rs</path>
<type>file</type>
<content>
20: 
21: // --------------------------------------------------------------------------- //
22: // Vecteur creux d'activation (optimisation 3)
23: // --------------------------------------------------------------------------- //
24: 
25: /// Liste d'activations non nulles, construite en amont par la cascade.
26: /// Indices triés, valeurs contiguës : 8 octets par source active, aucune
27: /// indirection, aucun test de zéro dans la boucle chaude.
28: #[derive(Clone, Debug, Default)]
29: pub struct SparseVec {
30:     pub idx: Vec<u32>,
31:     pub val: Vec<i32>,
32: }
33: 
34: impl SparseVec {
35:     pub fn from_dense(x: &[i32]) -> Self {
36:         let mut idx = Vec::new();
37:         let mut val = Vec::new();
38:         for (i, &v) in x.iter().enumerate() {
39:             if v != 0 { idx.push(i as u32); val.push(v); }
40:         }
41:         SparseVec { idx, val }
42:     }
43:     #[allow(dead_code)] pub fn len(&self) -> usize { self.idx.len() }
44:     #[allow(dead_code)] pub fn is_empty(&self) -> bool { self.idx.is_empty() }
45: }
46: 
47: // ----------------
… [695 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
860:         keep, attn_window, swa_pattern, sans_fenetre, attn_sinks, attn_topk, qk_topk,
861:         act_thresh, act_topk, act_renorm, topk_proj, moe_topk, patch: patch_file,
862:         hebb_layer, hebb_q, hebb_out, hebb_diff, hebb_eta, hebb_clamp, sans_yarn, lot, ffn_gain,
863:         trace_flux, trace_couches, flux_forcer, ..
864:     } = opt;
865:     let path = &modele_chemin();
866:     // Défauts du mode INFÉRENCE : 512 jetons, la moitié des cœurs (l'attente
867:     // active de la barrière ne tolère pas la sursouscription), 8 bits. On prend
868:     // tous les cœurs physiques : mesuré, 10 threads rendent 14,3 Go/s contre
869:     // 22,5 à 20 — le `cpu / 2` laissait 36 % sur la table.
870:     let cpu = engine::coeurs_physiques();
871:     let ctx = if ctx_impose { ctx_opt } else { 512 };
872:     let n_threads = if threads_impose { threads_opt } else { cpu.max(1) };
873:     let abits = if abits_impose { abits_opt } else { 8 };
874:     let mut mdl = model::Model::load_partiel(path, ctx, n_threads, dense, keep, auto, q4, b6,
875:                           
… [5005 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"o\\.flux\\b\\|flux_liste\\|flux_blocs\\|seuil_push\\|dense:\" drave-core/src/main.rs | head -40; echo \"=== Options struct ===\"; sed -n '580,640p' drave-core/src/main.rs", "description": "Trace flux flags and Options defau … [5 caractères tronqués]`

  ```
445:fn options_actives(mdl: &model::Model, mode: &str, ctx_impose: bool, dense: bool, keep: f32) {
464:             mdl.attn_window, mdl.swa_pattern, mdl.seuil_push, mdl.lot,
591:    flux: bool, session: bool, chat: bool, flux_liste: bool, flux_blocs: bool,
593:    ctx: usize, threads: usize, abits: u32, dense: bool, auto: bool,
770:            "--flux" => { o.flux = true; 1 }
771:            "--flux-liste" => { o.flux_liste = true; 1 }
772:            "--flux-blocs" => { o.flux_blocs = true; 1 }
773:            "--session" => { o.session = true; o.flux = true; 1 }
3364:    let mode = if opt.flux_blocs { MODE_BLOCS }
3365:               else if opt.flux_liste { MODE_LISTE }
=== Options struct ===
    /// avec la référence numpy.
    banc_vision: Option<String>,
    /// `--tensors` : liste les tenseurs du fichier (nom, dimensions, type) et
    /// s'arrête. Sert à préparer un chemin qu'on ne sait pas encore lire — le
    /// projecteur de vision, par exemple.
    tensors: bool,
    // --- source des jetons
    ids: Vec<u32>, ids_file: Option<String>, texte_file: Option<String>,
    ppl_texte: bool, prompt: Option<String>, limit: usize, depuis: usize,
    // --- génération
    n: usi
… [2994 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"seuil_push\\|use_dense\\|mode push\\|mode pull\" drave-core/src/model.rs drave-core/src/engine.rs drave-core/src/list.rs | head -30", "description": "Find push/pull decision sites"}`

  ```
drave-core/src/model.rs:11://! produits scalaires sur les lignes Q8_0 d'origine. En mode push il faudrait un
drave-core/src/model.rs:1494:        // (`seuil_push = 0.22`, `reports/rapport-croisement-push-pull.md`).
drave-core/src/model.rs:2464:    pub seuil_push: f32,
drave-core/src/model.rs:4358:            seuil_push: 0.22,
drave-core/src/model.rs:4495:        let use_dense = match (&p.d, &p.m) {
drave-core/src/model.rs:4520:            if use_dense {
drave-core/src/model.rs:5374:                    // Pas de forme dense (mode push) : jeton par jeton.
drave-core/src/model.rs:5380:                                     self.act_renorm, &mut scratch, self.seuil_push);
drave-core/src/model.rs:7087:                Self::matvec(pool, &lay.wq, &hn, &mut q, events, &mut paires[0], self.act_levels, self.act_thresh, tk(0), self.act_renorm, &mut scratch, self.seuil_push);
drave-core/src/model.rs:7088:                Self::matvec(pool, &lay.wk, &hn, &mut k, events, &mut paires[0], self.act_levels, self.act_thresh, tk(1), self.act_renorm, &mut scratch, self.seuil_push);
drave-core/src/model.rs:7089:                Self::matvec(pool, &lay.wv, &hn, &mut v, events, &mut paires[0], self.act_levels
… [1113 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"\\.flux\\b\\|flux_serveur\\|est_flux\\|mode_flux\" drave-core/src/main.rs | head -40", "description": "Trace --flux usage in main.rs"}`

  ```
121:        (opt.flux_serveur.is_some(), "--flux-serveur"),
140:    if let Some(adresse) = opt.flux_serveur.clone() { run_serveur_flux(opt, &adresse); return; }
568:    flux_serveur: Option<String>,
700:            "--flux-serveur" => { o.flux_serveur = Some(suivant(i).clone()); 2 }
770:            "--flux" => { o.flux = true; 1 }
773:            "--session" => { o.session = true; o.flux = true; 1 }
2151:{} · {} jetons × {} canaux · {} banque(s)", relais.debut, relais.flux.len(),
2152:                                        relais.flux.first().map(|v| v.len()).unwrap_or(0),
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 60, "offset": 3340}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
3340: fn run_ppl_reparti(opt: Options, pair: &str) {
3341:     use std::time::Instant;
3342:     let chemin = modele_chemin();
3343:     let ctx = if opt.ctx_impose { opt.ctx } else { 256 };
3344:     let limite = opt.limit.max(1).min(ctx);
3345:     let couches_locales = if opt.couches_locales > 0 { opt.couches_locales } else { 12 };
3346:     // `--lot T` : préremplissage par LOTS sur le fil. La référence locale est
3347:     // alors calculée avec le MÊME découpage — sinon l'écart mesurerait la
3348:     // différence entre deux ordres de sommation, pas celle du découpage.
3349:     let lot = opt.lot.max(1);
3350:     let mut mdl = model::Model::load(&chemin,
3351:                                      ctx, fils(&opt), true, opt.keep, false, 0, 0);
3352:     appliquer_quantification(&mut mdl, &opt);
3353:     // Le `hc` du PILOTE : c'est SON modèle qui décide de la largeur du pré-mix
3354:     // qu'il envoie et de celle de celui qu'il reçoit (le pair valide le sien).
3355:     let hc_pilote = mdl.hc.as_ref().map(|v| v[0].0.hc).unwrap_or(1);
3356:     // `--tete-partiel
… [3023 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des rapports de mesure sur la parcimonie et le push/pull

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-granularite-flux.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-croisement-push-pull.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-granularite-flux.md</path>
<type>file</type>
<content>
1: # Granularité des listes et volume des flux entre unités — mesuré
2: 
3: > Fil repris le 03/10 (bloc 26) : « séparer les grappes et les couches en listes
4: > plus fines pour qu'elles puissent être sur des unités de traitement différentes,
5: > et surtout réduire le volume des flux d'activation potentiels entre unités.
6: > Plus de petits lots d'événements = plus de flexibilité pour l'optimisation en
7: > temps réel. »
8: >
9: > C'est l'axe 3 de `docs/vision.md` (« Distribuer, c'est router des listes »), dont
10: > les points ouverts étaient : la granularité, l'ordonnanceur de placement, et le
11: > flux de poids depuis le NVMe. Ce rapport mesure la granularité sur des
12: > **activations réelles** de V4-Flash (`DRAVE_DUMP_COUCHES`, 43 couches × 4
13: > positions ; tenseur `l_last` = le flux de coupure, 16 384 valeurs = 4 copies
14: > d'hyper-connexion × 4 096, soit **65 536 octets en f32**).
15: 
16: ## 1. Ce que le flux pèse selon sa représentation (une liste pour tout le flux)
17: 
18: | seuil θ (fraction du max) | événements | DRVF v2 (écart u8 + i16) 
… [4920 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-croisement-push-pull.md</path>
<type>file</type>
<content>
1: # Croisement push / pull — quand l'architecture événementielle est-elle justifiée ?
2: 
3: Deux façons d'exécuter le même modèle quantifié :
4: 
5: - **push** (notre architecture) : pour chaque source active, on *disperse* ses
6:   poids dans un accumulateur (`acc[dest] += x·w`). Le flux est indexé par
7:   source, un événement = écart + valeur, 2 octets.
8: - **pull** (le noyau dense ordinaire) : pour chaque sortie, on *lit* sa ligne de
9:   poids et on fait un produit scalaire. 1 octet par poids, aucune dispersion.
10: 
11: Elles donnent **exactement le même résultat** — vérifié : perplexité 19,2647 au
12: chiffre près sur 510 jetons, tokens identiques, en écrivant les deux chemins avec
13: le même ordre d'opérations (les sommes entières sont exactes des deux côtés).
14: 
15: > ⚠️ **Corrigé le 27/09** : le tableau de croisement de la section 1 mesurait
16: > « push » contre « dense » alors que le drapeau `--dense`, placé en dernier
17: > argument, n'était jamais lu (`while i + 1 < args.len()`), et le mode dense
18: > sommait des tranches périmées. Le
… [5667 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-parcimonie-imposee.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mode-listes.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-parcimonie-imposee.md</path>
<type>file</type>
<content>
1: # Parcimonie imposée à l'inférence — la frontière mesurée
2: 
3: *Peut-on donner à un modèle **préentraîné** le débit variable d'un réseau à
4: décharge, sans rien réentraîner ?* Campagne mesurée sur Qwen2.5-0.5B Q8_0, avec
5: deux jeux de 1 024 tokens : **A** pour le réglage, **B** (jamais vu) pour la
6: vérification.
7: 
8: Tout est déterministe : mêmes tokens, même perplexité, au chiffre près. Les
9: comptes d'événements et les perplexités sont donc exacts ; seule la mesure de
10: **temps** est bruitée (la machine tournait sous une charge de 8 à 14).
11: 
12: ---
13: 
14: ## 1. Pourquoi cette campagne
15: 
16: Le cahier des charges promet un débit **variable** selon ce qui s'active. Nous
17: avons mesuré le contraire sur un LLM dense : **0,00 % d'activations nulles**, donc
18: un débit constant, et l'argument « on ne paie que ce qui s'active » restait
19: théorique. Deux moyens d'imposer la parcimonie à l'inférence, tous deux inspirés
20: des neurones à décharge, aucun ne demandant d'entraînement :
21: 
22: - **seuil** : écarter les activations sous u
… [5755 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mode-listes.md</path>
<type>file</type>
<content>
1: # Drave — « mode listes » : exécuter sans GPU
2: 
3: Objectif : **pas** de compresser le modèle, mais l'exécuter avec des opérations
4: purement structurelles (compter, décaler, additionner) — donc **sans multiplieur,
5: sans cœur tensoriel, sans GPU**.
6: 
7: Mesures sur **qwen2 Q8_0** (494.0 M poids, densité 99.2 %).
8: 
9: ## Deux façons d'exprimer la valeur
10: 
11: | Mode | Principe | Décodeur |
12: |---|---|---|
13: | **unaire** | la valeur est la longueur de la suite de zéros (≤ 127) | un compteur |
14: | **décalage-addition** | valeur positionnelle, une addition par bit à 1 | un décalage + un compteur |
15: 
16: ## 1. Coût par poids
17: 
18: | Mode | additions/poids | bits de flux/poids |
19: |---|---|---|
20: | multiplieur (référence GPU) | 0.99 | 8,00 |
21: | **décalage-addition (popcount)** | **3.10** | 8,00 |
22: | **unaire (suites de zéros)** | **42.45** | **42.45** |
23: 
24: ➡️ L'unaire coûte **13.7× plus** d'opérations *et* de flux, pour le
25: même résultat exact.
26: 
27: ## 2. Projection sur 7 G poids
28: 
29: | Support | 8 bits positionnel |
… [1777 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des taux de densité mesurés par modèle et par couche

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-transport-liste.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-transport-liste.md</path>
<type>file</type>
<content>
1: # Phase 3.2 — transporter la LISTE au lieu du vecteur
2: 
3: **En une ligne** : le flux peut voyager en liste creuse — **897 octets au lieu de
4: 3 623** à seuil 5 %, et **1 568** avec des indices par écarts — mais jeter des
5: canaux coûte cher (**×1,8 de perplexité** à ce seuil), et la courbe est là pour
6: dire où.
7: 
8: ## Le protocole, mesuré
9: 
10: Deux modes dans le même en-tête (39 octets à l'époque de ces mesures, **79** depuis que les top-k voyagent) — magie, version, mode, plage,
11: position, dimension, échelle, **et les réglages d'activation** :
12: 
13: | mode | contenu | octets par flux (Qwen2.5-0.5B, 896 canaux) |
14: |---|---|---|
15: | 0 · dense f32 | `896 × f32` | **3 623** (39 + 3 584) |
16: | 1 · listes | `n × (indice u16 · valeur i16)` | 39 + 4 × actifs |
17: 
18: Le mode 1 est le format du disque, à l'octet près. La réponse est encodée comme
19: la demande : un pair qui parle en listes reçoit des listes.
20: 
21: ## La courbe (40 jetons, 12 couches de chaque côté)
22: 
23: | seuil | activité | octets/flux (aller) | octets/flux (reto
… [11908 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"densité\\|densite\\|actifs\\|actives\" reports/*.md docs/*.md 2>/dev/null | grep -i \"%\" | head -70", "description": "Grep density figures in reports and docs"}`

  ```
reports/rapport-8bits.md:7:- densité : **99.2 %**
reports/rapport-analyse-flux.md:14:Le croisement push/pull du projet est mesuré à **~10 % de densité**. Ce qui
reports/rapport-analyse-flux.md:30:Neurones actifs dans au moins 90 % des jetons, par couche : **0,89 % à 1,90 %**
reports/rapport-analyse-flux.md:56:Le croisement push/pull mesuré du projet est à ~10 % de densité. Avec les densités
reports/rapport-attention-creuse.md:39:matrice **creuse à ~12,5 %**. Et cette densité **décroît avec le contexte** :
reports/rapport-attention-creuse.md:110:| Poids creux, donc listables | ✅ 12,5 % de densité à 256, 0,8 % à 4 096 |
reports/rapport-coherence-docs-2.md:82:| 28 | `docs/format-flux.md:58-61`, `REPRISE.md:248,340-341`, `docs/roadmap.md:94` | v3 : **45 079 930 o** (−32,1 % vs v2), rejeu 19,4029 (+0,074 %), 21 630 645 actifs | valeurs cohérentes entre documents ; l'exécution courte confirme le sens (v3 plus petite, 166 206 actifs contre 171 554 sur la même trace de 4 jetons) | OK |
reports/rapport-coherence-docs.md:113:| 35 | `reports/rapport-transport-liste.md:25` | listes seuil 0,00 : **3 622** pour 100,0 % (896 actifs) | 39 + 4 × 896 = **3 623** ; l'octet manquant n'est pas expliqué
… [7602 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-analyse-flux.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-localite-activation.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-analyse-flux.md</path>
<type>file</type>
<content>
1: # Analyse du flux, couche par couche
2: 
3: Première analyse **pure** : aucune exécution du moteur, seulement une trace relue
4: (`tools/analyse_flux.py`). Ce qu'elle apporte, et pourquoi ces questions-là ont
5: été posées plutôt que d'autres.
6: 
7: Modèle : Qwen2.5-0.5B Q8_0, contexte 256, 256 jetons, 24 couches, 896 cachés,
8: trace enregistrée avec `--abits 8 --act-thresh 0.05` (réglage de COÛT, pas de
9: qualité : la perplexité de cette configuration est de 2 445 — ce qui suit décrit
10: la forme du flux, pas la qualité du modèle).
11: 
12: ## Densité : où le push paie, où le pull paie
13: 
14: Le croisement push/pull du projet est mesuré à **~10 % de densité**. Ce qui
15: manquait était la densité **par couche** — or elle varie du simple au triple :
16: 
17: | couche | densité | couche | densité |
18: |---|---|---|---|
19: | **9** | **20,1 %** | 6 | 40,5 % |
20: | 0 | 25,9 % | 5 | 45,6 % |
21: | 4 | 26,7 % | **1** | **56,3 %** |
22: | 3 | 28,8 % | 8 | 29,2 % |
23: 
24: Autrement dit : la décision « listes ou matrice dense » n'est pas une propriété du
25:
… [2379 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-localite-activation.md</path>
<type>file</type>
<content>
1: # Localité d'activation : ce que PowerInfer apporte, et ce qu'on en garde
2: 
3: > Étude demandée du dépôt [SJTU-IPADS/PowerInfer](https://github.com/SJTU-IPADS/PowerInfer)
4: > (miroir `Tiiny-AI/PowerInfer`), confrontée à nos propres mesures. Tout ce qui
5: > suit est mesuré sur cette machine ; les chiffres de PowerInfer viennent de leur
6: > README et de l'article SOSP 2024.
7: 
8: ## 1. Leur idée
9: 
10: La distribution des activations d'un LLM suit une **loi de puissance** : une
11: petite partie des neurones est active presque toujours (« chauds »), le reste
12: dépend de l'entrée (« froids »). PowerInfer en tire un moteur hybride CPU/GPU
13: **à la granularité du neurone** : les chauds résident sur le GPU, les froids sont
14: calculés sur le CPU, ce qui réduit à la fois la VRAM nécessaire et le trafic
15: PCIe. S'y ajoutent un **prédicteur** (un petit MLP qui devine l'ensemble actif
16: pour précharger) et des **opérateurs creux conscients des neurones**. Leur modèle
17: TurboSparse (≈ 90 % de creux) est *entraîné* ainsi, précisément parce
18: qu'
… [4077 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/flux_codec.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/note-cancellation-evenementielle.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/flux_codec.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Encodeur/décodeur de RÉFÉRENCE du flux d'activation (format DRVF v1 et v2).
3: 
4: Le format de trace et le contrat d'échange de la phase 3 sont le MÊME format :
5: une liste d'activation est ce qu'un nœud distant doit recevoir pour continuer le
6: calcul. Ce fichier est la deuxième implémentation de ce format — la première est
7: en Rust (`--trace-flux`) — et c'est ce qui permet de dire qu'il est sans
8: ambiguïté : deux implémentations indépendantes, un aller-retour identique.
9: 
10: Structure :
11:     en-tête   "DRVF" · u16 version · u32 n_layer · u32 hidden
12:     liste     u16 couche · u32 position · u32 n_actifs · f32 echelle
13:               puis n_actifs × ( u32 indice · i16 valeur )          [v1]
14:               puis n_actifs × ( u8 écart · i16 valeur )            [v2]
15:                    l'écart de 255 annonce l'indice ABSOLU sur u16
16:     fin       u16 0xFFFF
17: 
18: v2 : les indices sont écrits par ÉCARTS (la liste est triée). Mesuré sur une trace
19: réelle de 512 jetons : 132 396 736 octets en v1, **66 370 408** en v2
… [5708 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/note-cancellation-evenementielle.md</path>
<type>file</type>
<content>
1: # Note — la voie événementielle : prédire une couche pour ne transporter que l'imprévu
2: 
3: > Note de conception, 06/10. Elle part d'une objection de Stéphane : arrêter de
4: > retomber sur les solutions d'entraînement classiques, et traiter le problème
5: > par des **flux de données légers, en mode événements**, sans rétropropagation.
6: 
7: ## 1. Ce que le moteur a déjà, et qui n'est pas un détour
8: 
9: | primitive | ce qu'elle fait | où |
10: |---|---|---|
11: | `SignedDelta`, `BitmapSign`, `FusedSign`, `SparseK`, `PushMat` | transport par **listes d'événements**, y compris **signés** — un événement peut être négatif | `list.rs` |
12: | `quant_scratch` (k-WTA, seuil) | **inhibition latérale** : ne garder que les k plus grandes magnitudes | `model.rs` |
13: | `kda_pas`, `kda_porte`, `res_mix` | **récurrence** par tête et mélange résiduel — vérifiés contre llama.cpp sur 25 couches de K3 | `model.rs` |
14: | `Hebb` | adaptation **locale**, sans passe arrière | `model.rs` |
15: | `Engram` | table de mémoire adressable | `engram.rs` |
16: | `--trace-
… [15052 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des rapports de gains AER/optimisations et des entrées REPRISE.md

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cpu-aer.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cpu-aer.md</path>
<type>file</type>
<content>
1: # Drave — l'architecture « push » (AER) sur CPU
2: 
3: ## L'architecture
4: 
5: Au lieu de **tirer** les activations à des indices arbitraires (gather), on
6: **pousse** : chaque source active émet un événement, sa liste de destinations se
7: lit **séquentiellement**, et on disperse `acc[dest] += signe · x[src]`.
8: 
9: - la liste d'activation se construit **en cascade** (compaction des non-nuls) ;
10: - l'accès aléatoire se déplace de l'entrée (activation, large) vers la sortie
11:   (accumulateur, 4096 × 24 bits = **12 Kio**, tient dans les M20K) ;
12: - les poids se lisent en **flux séquentiel** : plus aucun gather.
13: 
14: ## Mesures sur ce bi-Xeon E5-2687W v3
15: 
16: - bande passante lecture séquentielle : **11.5 Go/s**
17: - dispersion (`np.bincount`) : **183999808.87 G événements/s**
18: - dispersion (`np.add.at`) : 364797216.41 G événements/s
19: 
20: ## Limites mesurées du CPU (bench/cpu_aer.c, 16 threads)
21: 
22: | Test | 1 th | 8 th | 16 th | 32 th |
23: |---|---|---|---|---|
24: | Lecture séquentielle | 4,1 Go/s | 23,4 | **28,7** | 28,2 |
25: | Dispe
… [2395 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"événement\\|evenement\\|densité\\|act-topk\\|act_thresh\\|push/pull\\|k-WTA\\|listes\" REPRISE.md | head -60", "description": "Grep REPRISE.md for sparsity entries"}`

  ```
18:projections soit en listes d'événements, soit en produit scalaire dense, gère les
220:> (`HebbDiff`, seuil d'événement, forme signée, décroissance), la **mesurer**, la
606:> (4) Granularité des listes : **elle route, elle ne compresse pas**
694:| Encodages | listes d'événements (push), dense int8 par ligne, dense 4 bits par bloc, **6 bits empaqueté par bloc** |
701:| **Flux mesuré** | le rapport de `--ppl` donne les **paires** (poids × activation) par provenance — **attention / experts / partagé** — et les scores : c'est ce qui dit *où* passe le flux, donc ce qu'on peut déporter, découper ou simplifier. Les **événements** ne comptent que le chemin en listes (poids non nuls) ; les paires comptent tout ce qui est payé, y compris les chemins **déquantifiés (IQ)** et **MLA f32** qui n'affichaient que des zéros (`reports/rapport-p0-flux.md`) |
731:1. **Mesurer avant de conclure.** Le croisement push/pull était annoncé à 10 %,
753:   « dont en listes » reste à 0,0 M — le modèle passe par le chemin dense de toute
919:dense, listes, blocs et **lot** ; `--flux-serveur` accepte `hôte:port`, et
927:| listes à échelle par bloc, seuil 0,01 | 1 608 | 2,7e-2 |
973:bloc de 32) est avec perte. L
… [820 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md", "limit": 60, "offset": 1}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md", "limit": 120, "offset": 690}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md</path>
<type>file</type>
<content>
1: # Reprise — état du projet et mode d'emploi pour une nouvelle session
2: 
3: > Rédigé à la fin d'une session longue. Tout ce qui suit est **mesuré**, pas
4: > déduit. Les valeurs de perplexité sont des **références de non-régression** :
5: > si une modification les change, c'est qu'elle a changé le calcul.
6: >
7: > **Nom** : le projet s'appelle **Drave** (binaire `drave`, paquet `drave-core`,
8: > variables `DRAVE_*`, histoire du renommage dans `docs/histoire.md`). Le dossier
9: > de travail, lui, s'appelle encore `Qtrinet` — les chemins ci-dessous sont ceux
10: > qui existent.
11: 
12: ---
13: 
14: ## 1. En une phrase
15: 
16: `drave-core` est un moteur d'inférence Rust (~13 758 lignes, `std` seul) qui
17: charge les GGUF **en place** (aucune copie, aucune requantification), exécute les
18: projections soit en listes d'événements, soit en produit scalaire dense, gère les
19: MoE, tient une conversation, et déporte au GPU ce qui y gagne. Il fait tourner du
20: 0,5 B au 120 B sur le CPU de cette machine.
21: 
22: ```bash
23: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave
… [2192 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md</path>
<type>file</type>
<content>
690: | Tête de sortie | `output.weight` si non lié (bug corrigé), sinon `token_embd` |
691: | Tokenizers | Qwen2 **et** o200k (gpt-4o), tous deux lus du GGUF, sélectionnés par `tokenizer.ggml.pre` |
692: | Échantillonnage | température, top-k 40, top-p, **pénalité de répétition** (`--rep-penalty`, fenêtre `--hist`) |
693: | Génération | **sortie en flux** (`--flux`), **session multi-tours** (`--session`), arrêt sur fin de tour |
694: | Encodages | listes d'événements (push), dense int8 par ligne, dense 4 bits par bloc, **6 bits empaqueté par bloc** |
695: | GPU | noyaux PTX + API pilote, tête et projections opt-in (`DRAVE_GPU=1`) |
696: | Outils | `--ppl`, `--plan` (placement), `--tokenize`, `--bits N` (simulation de précision) |
697: | Mesure | `--ppl-texte F` (identifiants du tokenizer du modèle), `--depuis N` (ne noter qu'à partir du jeton N, contexte ancré — les mêmes jetons deviennent comparables à 512, 1 024, 4 096… de contexte), `--ppl-profil` (perte par tranche de 256 positions), `--logits-bin F` (logits bruts), `--harmony*` (habillage harmony), `--swa-pattern N`, `--sans-fen
… [13476 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md", "limit": 100, "offset": 900}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md", "limit": 40, "offset": 1800}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md</path>
<type>file</type>
<content>
900: écart local/réparti **0,00e0** — 144,8289 des deux côtés à 40 jetons, et
901: **9,5146 des deux côtés à 1 024 jetons** (1 023 flux : le dernier jeton n'a rien
902: à prédire, il n'est plus envoyé), le banc
903: réparti prenant le temps du calcul local (19,7 contre 19,4 ms par jeton). Il a
904: fallu deux corrections dans `Model::forward`, et la première ne suffisait pas :
905: 
906: 1. la boucle partait de `0` au lieu de `couche_debut..couche_fin` : le pilote
907:    calculait les 24 couches, envoyait l'état FINAL, et le pair les recalculait
908:    toutes par-dessus (`forward_lot` et `forward_mla`, eux, respectaient la plage) ;
909: 2. la norme finale était appliquée DEUX fois (le nœud moteur normait parce que sa
910:    plage allait jusqu'à la dernière couche, puis le pilote normait). La règle est
911:    maintenant portée par un drapeau explicite, `flux_brut`.
912: 
913: **Le protocole de flux est en v5** (`docs/format-flux.md`) : en-tête de **79
914: octets** avec version, mode et le **contrat d'activation complet** (niveaux, seuil,
915: top-k, renorm, les sept top-k par pro
… [5331 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md</path>
<type>file</type>
<content>
1800: chacune avec une **porte** (commande + résultat attendu), un interdit et un budget.
1801: Trois faits vérifiés le 02/10 le structurent :
1802: 
1803: 1. **llama.cpp ne connaît pas `deepseek41`** (`unknown model architecture`) : il
1804:    n'existe aucune référence externe pour V4.1 ;
1805: 2. **llama.cpp exécute V4-Flash** (`deepseek4`, 1 325 tenseurs chargés,
1806:    NLL 11,737 sur un jeton froid) — c'est donc **V4-Flash le banc d'essai**, avec
1807:    les mêmes mécanismes (hyper-connexions, MLA, compresseur, indexeur, table) et
1808:    86,9 Go qui tiennent en RAM ;
1809: 3. **V4.1-Flash-Q2 n'a pas les tenseurs `output_hc_*`** alors qu'il déclare
1810:    `hc_mult = 4` : fichier incomplet ou converti à tort — question de provenance à
1811:    trancher avant d'écrire du code (phase P7).
1812: 
1813: **Le plan est écrit dans le vocabulaire de Drave, pas dans celui de llama.cpp** :
1814: V4.1 est fait de flux qui sont déjà des listes — les 6 experts sur 384
1815: (`--trace-experts`), la table `tid2eid` des 3 premières couches, la sélection de
1816: blocs du compresseur (`attn
… [924 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des défauts en mode perplexité et du sort de `--flux`

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"flux\" drave-core/src/main.rs | sed -n '1,80p'", "description": "List all flux mentions in main.rs"}`

  ```
121:        (opt.flux_serveur.is_some(), "--flux-serveur"),
140:    if let Some(adresse) = opt.flux_serveur.clone() { run_serveur_flux(opt, &adresse); return; }
424:/// fin d'une plage `--couches a:b`. Par défaut une plage partielle rend le flux
441:/// flux, `--trace-flux` en inférence, `--threads` figé…), et chacun était
453:    println!("[options] couches {}..{} · flux brut {} · trace {} · rejeu {}",
454:             mdl.couche_debut, mdl.couche_fin, mdl.flux_brut,
455:             mdl.trace.is_some(), mdl.flux_force.is_some());
548:    /// Trace du flux d'activation : fichier de sortie.
549:    trace_flux: Option<String>,
552:    flux_forcer: Option<String>,
568:    flux_serveur: Option<String>,
591:    flux: bool, session: bool, chat: bool, flux_liste: bool, flux_blocs: bool,
617:    /// sortie. Par défaut une plage partielle rend le flux résiduel brut (ce
698:            "--trace-flux" => { o.trace_flux = Some(suivant(i).clone()); 2 }
699:            "--flux-forcer" => { o.flux_forcer = Some(suivant(i).clone()); 2 }
700:            "--flux-serveur" => { o.flux_serveur = Some(suivant(i).clone()); 2 }
770:            "--flux" => { o.flux = true; 1 }
771:            "--flux-list
… [5118 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 60, "offset": 5150}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
5150:     if depuis > 0 {
5151:         println!("notation à partir du jeton {depuis} : les jetons précédents servent de contexte, \
5152:                   les mêmes jetons sont donc comparables à contexte 512, 1 024, 4 096…");
5153:     }
5154:     mdl.moe_topk = moe_topk;
5155:     poser_niveaux(&mut mdl, abits, "perplexité");
5156:     if let Some(f) = &patch_file {
5157:         let pt = model::Patch::load(f).expect("chargement du greffon");
5158:         let norme = |v: &[f32]| v.iter().map(|x| x * x).sum::<f32>().sqrt();
5159:         println!("greffon : couche {}, |u|={:.3} |v|={:.3} |d|={:.3}",
5160:                  pt.layer, norme(&pt.u), norme(&pt.v), norme(&pt.d));
5161:         mdl.patch = Some(pt);
5162:     }
5163:     if let Some((l, g)) = ffn_gain {
5164:         println!("gain FFN : couche {l} x {g}");
5165:         mdl.ffn_gain = Some((l, g));
5166:     }
5167:     mdl.act_thresh = act_thresh;
5168:     mdl.act_topk = act_topk;
5169:     mdl.act_renorm = act_renorm;
5170:     mdl.act_topk_proj = topk_proj;
5171:     mdl.attn_topk = attn_topk;
5172:    
… [2473 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"abits_impose\\|let abits\" drave-core/src/main.rs | head -20", "description": "Find abits defaults per mode"}`

  ```
597:    ctx_impose: bool, threads_impose: bool, abits_impose: bool,
736:            "--abits" => { o.abits = suivant(i).parse().unwrap(); o.abits_impose = true; 2 }
859:        ctx_impose, threads_impose, abits_impose, dense, auto, q4, b6,
873:    let abits = if abits_impose { abits_opt } else { 8 };
2478:    let abits = abits.clamp(1, 16);
2493:    let abits = if opt.abits_impose { opt.abits } else { 8 };
5076:        ctx_impose, threads_impose, abits_impose,
5091:    let abits = if abits_impose { abits_opt } else { 16 };
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 130, "offset": 2100}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
2100:     /// canaux, ~22 % plus petit, avec perte).
2101:     pub version: u16,
2102:     /// Nombre de canaux par bloc d'échelle en v3.
2103:     pub bloc: usize,
2104:     pub fichier: std::io::BufWriter<std::fs::File>,
2105:     /// Couches à tracer (toutes si vide).
2106:     pub couches: Vec<usize>,
2107:     pub octets: u64,
2108:     pub enregistrements: u64,
2109:     pub actifs: u64,
2110: }
2111: 
2112: impl TraceFlux {
2113:     pub fn nouveau(chemin: &str, couches: Vec<usize>, hidden: usize, n_layer: usize)
2114:         -> std::io::Result<Self> {
2115:         use std::io::Write;
2116:         let mut f = std::io::BufWriter::new(std::fs::File::create(chemin)?);
2117:         f.write_all(b"DRVF")?;
2118:         // Version 2 par défaut : indices par ÉCARTS, valeurs i16 — sans perte.
2119:         // Version 3 sur `DRAVE_TRACE_BLOCS=1` : en plus, valeurs i8 et une échelle
2120:         // f16 par bloc de 32 canaux (l'étude de compacité annonce −22 % de plus,
2121:         // au prix de la fidélité du rejeu).
2122:         let version: u16 = if std::env::var("
… [5731 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn quantifier\\|\\.ecrire(\\|trace.as_mut()\\|SEUIL_PROFIL\" drave-core/src/model.rs | head -30", "description": "Locate quantifier and trace write sites"}`

  ```
4685:    /// Seuil d'activation du profilage : une activation vaut `SEUIL_PROFIL` du
4691:    const SEUIL_PROFIL: f32 = 0.05;
4700:        let seuil = Self::SEUIL_PROFIL * mx;
4724:                              100.0 * Self::SEUIL_PROFIL, n_tok, largeur, n));
5426:                        kvc.ecrire(hh, pos, &ki[hh * hd..(hh + 1) * hd],
5793:            } else if let Some(tr) = trace.as_mut() {
5796:                tr.ecrire(base + l, j0 as usize, &actifs, e);
7034:                    self.trace.as_mut().unwrap().ecrire(l, j as usize, &actifs, sx);
7129:                        kvc.ecrire(hh, pos, &k[hh * hd..(hh + 1) * hd], &v[hh * hd..(hh + 1) * hd]);
7527:                    self.trace.as_mut().unwrap().ecrire(l + 1000, j as usize, &actifs, sx);
8472:            c.ecrire(1, 2, &k, &v);
8491:            c.ecrire(1, 2, &k2, &v);
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '4690,4760p' drave-core/src/model.rs", "description": "Read profiling threshold section"}`

  ```
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
        let larg
… [2812 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '7015,7045p' drave-core/src/model.rs; echo \"=== 7510-7535 ===\"; sed -n '7510,7535p' drave-core/src/model.rs; echo \"=== 5780-5800 ===\"; sed -n '5780,5800p' drave-core/src/model.rs", "description": "Read trace write contexts … [2 caractères tronqués]`

  ```
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
            //
… [3103 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/granularite_flux.py", "limit": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/granularite_flux.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """granularite_flux.py — le volume d'un flux de coupure selon sa GRANULARITÉ.
3: 
4: Un flux entre deux unités de traitement, c'est un ou plusieurs LISTES d'activation
5: (les événements). Ce script mesure, sur des activations RÉELLES vidées par le
6: moteur (`DRAVE_DUMP_COUCHES`), ce que coûte un flux selon :
7: 
8:   - la REPRÉSENTATION : dense f32, dense f16, liste DRVF v2 (écart u8 + valeur i16),
9:     liste « v3 » (échelle f16 par bloc de 32 + valeurs i8, estimée) ;
10:   - le SEUIL θ (fraction du max) qui décide quelles valeurs sont des événements ;
11:   - la GRANULARITÉ G : en combien de listes indépendantes on découpe le flux.
12: 
13: C'est la question de l'axe 3 (`docs/vision.md`) : « une liste est une unité de
14: travail autonome », donc plus de listes = plus de liberté de placement — mais
15: chaque liste paie son en-tête. Ce script donne le point où l'en-tête rattrape le
16: gain, et l'erreur qu'on accepte en échange.
17: 
18: Usage :
19:     granularite_flux.py <prefixe> --tensor l_last [--couches 0,20,42] [--positions 0,3]
… [2180 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Collecte des chiffres de compacité, d'échelle et de flux mesuré

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-compacite-trace.md", "limit": 80, "offset": 20}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-p0-flux.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-compacite-trace.md</path>
<type>file</type>
<content>
20: > Reste : l'emballage zstd en étape EXTERNE (−79 % au total, mesuré ici) — le
21: > moteur est en `std` seul, il n'embarque pas de compresseur, et c'est très bien
22: > ainsi : `zstd -19` sur le fichier fait le travail sans une ligne de code.
23: 
24: **En une ligne** : la trace DRVF v1 coûte **6,04 octets par neurone actif** quand
25: le transport en coûte ~2 ; les **indices u32 en sont les deux tiers**, et les
26: ramener à un octet par écarts divise la trace par deux **sans perdre un seul
27: indice** — le reste (valeurs i8, échelles f16, zstd) porte le total à **−79 %**.
28: 
29: Mesures faites avec `tools/trace_compacite.py`, qui lit les traces avec
30: `tools/flux_codec.py` (l'implémentation de référence validée contre le Rust) et
31: ne fait que compter des octets : aucune troisième lecture du format n'a été
32: écrite.
33: 
34: ---
35: 
36: ## 1. L'incohérence, chiffrée avant d'être corrigée
37: 
38: Le disque et le réseau encodent la même information — une liste creuse valuée —
39: mais plus de la même façon :
40: 
41: | | indices | valeurs | éche
… [3704 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-p0-flux.md</path>
<type>file</type>
<content>
1: # P0 — Le harnais de flux : compter ce qu'on paie, par provenance
2: 
3: **En une ligne** : les chemins **MLA** et **experts-IQ** annonçaient « 0
4: événement » alors qu'ils calculent des dizaines de milliards de produits par
5: jeton — le compteur manquait, pas le travail ; le moteur compte maintenant les
6: **paires** (poids × activation) par provenance (**attention / experts /
7: partagé**), et la première mesure dit une chose que la suite du plan doit
8: entendre : **sur ces deux chemins, le flux est dense** — 0 événement en listes,
9: la totalité des matrices est payée.
10: 
11: ## 1. Ce qui était muet, et pourquoi
12: 
13: `events_total()` ne comptait que le chemin **push** de `matvec` : `Σ row_ev[i]`
14: sur les sources actives, c'est-à-dire les poids **non nuls** réellement
15: multipliés. Trois chemins ne passaient jamais par là :
16: 
17: | chemin | ce qu'il fait | ce qu'il comptait |
18: |---|---|---|
19: | MLA (`attn_mla`) | projections de rang faible en **f32 plein** (`matvec_f32`) | rien — aucune liste n'est construite |
20: | experts **IQ** (`Source:
… [7212 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de la sémantique du compteur d'événements dans les scripts de campagne

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"événement\\|evenement\\|events\\|PPL\\|perplex\" run_sparsity.py | head -40", "description": "Inspect run_sparsity.py counters"}`

  ```
3:Drave — l'élagage permet-il une approche par événement ?
116:    L = ["# Drave — élagage et approche par événement\n",
123:         f"- événements réels (poids ∧ activation) : **{S.joint_density(d_nat, S.relu_density(np.maximum(Xte @ (q1*s1) + model.b1, 0)))*100:.1f} %**\n",
164:          "2. **L'encodage événementiel « bitmap + signe » domine le dense** : 1 + d bits/poids "
170:          "4. **Le vrai obstacle n'est pas le poids, c'est l'activation** : un événement "
173:          "d'événements réels). Récupérer l'activation à un index arbitraire impose une "
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"événements\" reports/rapport-optimisations.md reports/rapport-passage-a-l-echelle.md reports/rapport-attention-creuse.md reports/rapport-mur-memoire-4bits.md 2>/dev/null | head -30", "description": "Grep event counts in op … [20 caractères tronqués]`

  ```
reports/rapport-optimisations.md:1:# Moteur d'événements Rust — les 4 optimisations, et les 3 pièges
reports/rapport-optimisations.md:5:sorties, **4 303 745 événements** (ternaire issu des signes réels, densité 100 %).
reports/rapport-optimisations.md:21:Les écarts d'un octet (99,99 % des événements à forte densité) sont décodés **8 à
reports/rapport-passage-a-l-echelle.md:39:| listes d'événements (`PushMat`) | **1,98** | densité d'activation < 22 % |
reports/rapport-passage-a-l-echelle.md:117:d'événements, `DenseQ8` ou `DenseQ4`), et `Gguf::open` fait un `read_to_end` :
reports/rapport-passage-a-l-echelle.md:178:| l'accumulateur décide du débit en régime creux (mesuré : ×1,7 entre 4 et 32 threads sur des événements épars) | le **tuilage de la dimension de sortie** est le paramètre d'architecture, pas un détail |
reports/rapport-passage-a-l-echelle.md:179:| QSFP+ 4,8 Go/s, NVLink 25,78 Go/s, PCIe x8 6,5 Go/s | le flux d'événements adressé par destination est un protocole réseau naturel : c'est la thèse du CDC, et elle devient mesurable dès qu'un modèle dépasse un nœud |
reports/rapport-passage-a-l-echelle.md:196:| 7 | transport d'événements multi-nœuds | élevé | dépasser un nœud |

… [830 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-attention-creuse.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mur-memoire-4bits.md", "limit": 60}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-attention-creuse.md</path>
<type>file</type>
<content>
1: # Attention creuse — le trou se referme, et par le haut
2: 
3: Le point faible identifié dans nos bilans : l'attention n'est **pas exprimable en
4: listes d'événements**, parce que ses poids sortent d'un softmax calculé à
5: l'exécution, et son coût croît **linéairement avec le contexte** (2,0 ms à 64
6: tokens, 12,7 ms à 512, ~200 ms extrapolé à 8 192).
7: 
8: Une seule modification, à l'inférence, sans réentraînement : **ne garder que les
9: k plus grands scores par requête** avant le softmax. Les autres sont masqués
10: (`-∞`), le softmax renormalise sur les k retenus.
11: 
12: *Ce n'est pas une importation : c'est la même question que pour les activations —
13: imposer une parcimonie à un modèle préentraîné et mesurer ce qu'elle coûte. La
14: réponse, ici, est qu'elle **rapporte**.*
15: 
16: ---
17: 
18: ## 1. Résultat
19: 
20: Deux jeux de 1 024 tokens, réglage sur A, vérification sur B.
21: 
22: | k (clés gardées) | PPL (A) | PPL (B) | 2 040 tokens | ctx 512 |
23: |---|---|---|---|---|---|
24: | **dense** (référence) | 23,6125 | 26,2565 | 24,8995 | 1
… [7215 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mur-memoire-4bits.md</path>
<type>file</type>
<content>
1: # Le mur mémoire, et ce que les 4 bits achètent vraiment
2: 
3: > Suite de `rapport-croisement-push-pull.md`. Trois bugs de mesure corrigés, une
4: > mesure de bande passante, et un chemin 4 bits écrit puis mesuré.
5: 
6: ## 1. Trois bugs qui faussaient les conclusions
7: 
8: | bug | symptôme | cause |
9: |---|---|---|
10: | **drapeau final ignoré** | `--dense` « donnait exactement le même résultat que push » | `while i + 1 < args.len()` : un drapeau en **dernière** position n'était jamais lu |
11: | **tranches périmées en mode dense** | PPL **4 361 879** au lieu de 19,26 | chaque worker n'écrivait que sa tranche ; la somme des 16 vecteurs récupérait les restes du travail précédent |
12: | **parenthesage flottant** | pull et push divergeaient d'un token | `(dot×s)×sx` contre `acc×(sx×s)` — deux arrondis différents sur des sommes entières pourtant exactes |
13: 
14: Le troisième n'était pas un bug mais une occasion : en écrivant les deux chemins
15: avec **le même ordre d'opérations**, et parce que les sommes entières sont
16: exactes des deux côtés, on ob
… [2142 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,40p' tools/approximabilite_bloc.py; echo \"=== EOF usage ===\"; sed -n '1,30p' reports/rapport-optimisations.md; echo \"=== passage echelle 30-45 ===\"; sed -n '30,45p' reports/rapport-passage-a-l-echelle.md; echo \"=== vis … [178 caractères tronqués]`

  ```
#!/usr/bin/env python3
"""approximabilite_bloc.py — un bloc de couches est-il approximable par une
application BEAUCOUP plus simple ?

Question préalable à toute distillation (idée de Stéphane : distiller les couches
0-9 d'un grand modèle dans un modèle récurrent, en commençant par là parce que
l'entrée de la couche 0 est du TEXTE, donc échantillonnable sans rien simuler).

Ce que l'outil rend, pour un bloc `a..b` : la part de variance de la sortie du
bloc expliquée par une application LINÉAIRE de son entrée, ajustée sur les flux
réels (moindres carrés, forward-only).

  - R² élevé  → le bloc est presque linéaire ; un récurrent léger peut le porter ;
  - R² faible → le bloc fait autre chose, et il faudra de la non-linéarité.

La mesure se fait sur la représentation TRANSPORTÉE (DRVF v3), pas sur la
représentation exacte : c'est le bon périmètre ici, puisque c'est ce que Drave
transporte.

Usage : approximabilite_bloc.py <trace.drvf> --de 0 --a 10 [--base 0]
"""
import struct
import sys


def lire(chemin):
    def paires(f, n, version, bloc=32):
        ech = None
        if version == 3:
            nb, = struct.unpack("<I", f.read(4))
            ech = [struct.unpack("<e", f.read(
… [4787 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Derniers chiffres : mode 4 en lot et événements par jeton

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mode4-lot-listes.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mode4-lot-listes.md</path>
<type>file</type>
<content>
1: # Mode 4 — le lot en listes : ÷2,3 sur les octets, et ce qu'il coûte
2: 
3: **En une ligne** : un préremplissage de N états peut voyager en **listes creuses**
4: au lieu de f32 dense — 1,5 ko par jeton contre 3,5 — au prix d'une quantification
5: dont l'effet **dépend de la longueur du lot**, ce que ce rapport chiffre au lieu de
6: le cacher.
7: 
8: ## Ce que le mode ajoute
9: 
10: Le mode 3 (lot dense) envoie `t × dimension × f32` : simple, sans perte, et c'est
11: lui qui a rendu le préremplissage réparti fidèle (0,00e0). Le mode 4 envoie le même
12: lot **en listes** : chaque état est encodé comme le mode 2 (indices par écarts u8
13: avec échappement vers u16, valeurs i8, une échelle f32 par bloc de 32 canaux) et
14: **auto-délimité** par un préfixe de 12 octets — `a_j · n_blocs_j · longueur_j` —
15: dont les trois tailles se lisent avant toute allocation.
16: 
17: Le mode est **avec perte**, comme le mode 2. Le critère n'est donc pas l'égalité
18: mais la comparaison à ce que le mode 2 coûte déjà.
19: 
20: ## Mesuré
21: 
22: Corpus WikiText-2, 256 jeto
… [4991 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"événements/jeton\\|événements par jeton\\|ev/jeton\\|G év\\|M év\" reports/*.md docs/*.md REPRISE.md 2>/dev/null | head -30", "description": "Grep events per token figures"}`

  ```
reports/bilan-multi-materiel.md:46:| CPU (16 threads) | **5,3 G évts/s** mesuré | ~57 nJ |
reports/bilan-multi-materiel.md:47:| FPGA (1 carte, 51 voies) | 4,83 G évts/s *projeté* (limite DDR3) | **~8,3 nJ** |
reports/bilan-multi-materiel.md:48:| GPU (dispersion) | **18,1 G évts/s** mesuré | ~12,7 nJ |
reports/bilan-multi-materiel.md:54:| CPU | 1 thread 0,41 G → 8 : 2,75 → 16 : 4,45 → **32 : 5,3** G évts/s ; effondrement à 39+ |
reports/bilan-multi-materiel.md:56:| GPU | 18,1 G évts/s de dispersion, 380 Go/s de lecture |
reports/bilan-multi-materiel.md:93:| « Fusion divergente au rang 0 » et « 7,53 G évts/s » | **Fausses** — un état partagé à deux contrats de nettoyage ; valeurs réelles 3,66 / 4,99 G |
reports/bilan-multi-materiel.md:109:Une carte = 4,83 G évts/s = **un CPU 20 cœurs**, pour 41 % de la logique et 41 %
reports/rapport-attention-creuse.md:112:| Poids d'attention dans le flux d'événements | ✅ négligeable : 0,04 M paires/token contre 354 M événements |
reports/rapport-coherence-vision.md:55:| `programme-recherche.md` | **cohérent, 4 sites** | 4ᵉ propriété structurelle « **le flux se route** » ; 5,3 G événements/s sourcé |
reports/rapport-cpu-aer.md:17:- dispersion (`np.b
… [1894 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-inference.md", "limit": 70, "offset": 178}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-inference.md", "limit": 40, "offset": 255}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-inference.md</path>
<type>file</type>
<content>
178: **Démontré :**
179: 1. L'architecture « listes d'événements » **exécute un vrai LLM**, à qualité égale
180:    (perplexité à 0,4 %, 16 tokens identiques sur 16), en arithmétique entière.
181: 2. Elle tient dans **2 300 lignes de Rust sans aucune dépendance** — pas de BLAS, pas
182:    de framework, pas de GPU.
183: 3. Le débit est **entièrement déterminé par le nombre d'événements** : 3,9 G év/s,
184:    soit exactement la cadence mesurée du moteur au microbanc.
185: 4. Elle est **30 % plus rapide que numpy + OpenBLAS** sur le même modèle, sur le même
186:    CPU, avec 20 threads au lieu de 40.
187: 
188: **Non démontré :**
189: 1. **Le débit variable reste hors d'atteinte** : 352 M événements par token, tous les
190:    tokens, parce que les activations d'un LLM dense ne sont jamais nulles. Le mode
191:    événementiel ne paiera que sur des modèles à activations **creuses par
192:    construction** (seuil, top-k, ReLU, MoE, ou graphes).
193: 2. **Aucun avantage de cadence brute** : 3,9 G événements/s sur 20 cœurs ≈ 1 événement
194:    par cycle et par cœur. Un
… [2945 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-inference.md</path>
<type>file</type>
<content>
255: **quelle que soit la précision de la source**. Le 4 bits est élargi à 8 bits au
256: chargement. Et la vitesse suit le *nombre d'événements*, pas le nombre de bits :
257: −12 % d'événements, +14 % de débit. On échange 12 % de perplexité contre 11 % de
258: mémoire — un mauvais marché.
259: 
260: *(Même en empaquetant idéalement la valeur sur 4 bits, on serait à 1,5 octet par
261: événement contre 0,56 octet par poids en Q4 dense : le format liste reste 2,7× plus
262: gros, parce qu'à 99 % de densité chaque poids a besoin de son octet d'écart.)*
263: 
264: ### Le vrai résultat : le coût d'un événement n'est pas constant
265: 
266: En élaguant par magnitude (le levier qui, lui, réduit réellement le nombre
267: d'événements) :
268: 
269: | poids gardés | événements/token | tok/s | débit par événement |
270: |---|---|---|---|
271: | 100 % | 352,7 M | 10,33 | 3,56 G év/s |
272: | 50 % | 178,6 M | 12,17 | 2,28 G év/s |
273: | 25 % | 89,5 M | 15,64 | 1,43 G év/s |
274: | 10 % | 35,6 M | 21,40 | 0,88 G év/s |
275: 
276: **10× moins d'événements ne donnent que 2× de vit
… [1188 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '35,60p' reports/bilan-multi-materiel.md; echo \"=== spiking ===\"; sed -n '60,80p' docs/comparaison-spiking.md; echo \"=== x18 ===\"; grep -rn \"×18\\|18×\\|x18\" reports/*.md docs/*.md REPRISE.md 2>/dev/null | head -10", "de … [60 caractères tronqués]`

  ```
| numpy float32 + OpenBLAS (40 threads) | 132 | 7,6 | mesuré |
| CPU, moteur d'événements (push) | 64 | 15,6 | mesuré |
| **CPU, noyau dense int8 (pull)** | **27** | **36,4** | **mesuré — après correction du produit scalaire** |
| FPGA, 1 carte, 51 voies | ~73 | ~13,7 | *projeté* (PE et lecteur vérifiés et synthétisés) |
| GPU, mode listes (atomics) | ~19,5 | ~51 | *déduit* de la dispersion mesurée |
| **GPU, dense int8** | **~1,3** | **~770** | *déduit* de la bande passante mesurée |

### Le débit par événement, et son coût énergétique

| Ressource | Débit | Énergie par événement (TDP) |
|---|---|---|
| CPU (16 threads) | **5,3 G évts/s** mesuré | ~57 nJ |
| FPGA (1 carte, 51 voies) | 4,83 G évts/s *projeté* (limite DDR3) | **~8,3 nJ** |
| GPU (dispersion) | **18,1 G évts/s** mesuré | ~12,7 nJ |

### Montée en charge

| Ressource | Courbe mesurée |
|---|---|
| CPU | 1 thread 0,41 G → 8 : 2,75 → 16 : 4,45 → **32 : 5,3** G évts/s ; effondrement à 39+ |
| FPGA | 1 événement/cycle/voie, **0,86 mesuré** avec le lecteur ; optimum à 32 PE pour le banc seul (177 MHz) |
| GPU | 18,1 G évts/s de dispersion, 380 Go/s de lecture |

## 3. Ce que l'architecture événementielle apporte réellement
… [3382 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_flux.py", "limit": 75, "offset": 40}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/analyse_flux.py</path>
<type>file</type>
<content>
40:         else:
41:             e, = struct.unpack("<B", f.read(1))
42:             if e == 255:
43:                 i, = struct.unpack("<H", f.read(2))
44:             else:
45:                 i = prev + e
46:             prev = i
47:         if version == 3:
48:             v, = struct.unpack("<b", f.read(1))
49:             ech = echelles[i // bloc] if echelles else 1.0
50:             paires.append((i, v * ech))
51:         else:
52:             v, = struct.unpack("<h", f.read(2))
53:             paires.append((i, v))
54:     return paires
55: 
56: 
57: def lire(chemin):
58:     """Rend (n_layer, hidden, listes) — listes = (couche, pos, echelle, [(indice, valeur)]).
59: 
60:     Les valeurs sont ramenées à l'échelle du vecteur (`valeur · echelle`), comme
61:     le fait `TraceFlux::ecrire` côté moteur : la v3 porte en plus son échelle par
62:     bloc, appliquée ici.
63:     """
64:     with open(chemin, "rb") as f:
65:         assert f.read(4) == b"DRVF", "ce n'est pas une trace DRVF"
66:         version, = struct.unpack("<H", f.read(2))
67:         assert version 
… [2276 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification finale des citations avant rédaction

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '5,10p' reports/rapport-8bits.md; echo \"--- optim auto 113-120 ---\"; sed -n '113,120p' reports/rapport-optimisations-auto.md; echo \"--- eparsite 60-66 ---\"; sed -n '60,66p' reports/rapport-eparsite.md; echo \"--- inference … [189 caractères tronqués]`

  ```
## 1. Distribution des niveaux

- densité : **99.2 %**
- niveaux distincts : **256** (sur 256 possibles)
- `E[|v|]` : **42.79**
- `E[popcount(|v|)]` : **3.13**
--- optim auto 113-120 ---
un modèle plus gros que le cache) mais **ne compte pas comme un gain**.

**La tête à restriction garantie** : trois voies explorées, aucune ne tient. La
borne de Cauchy-Schwarz ne conclut jamais, et la sparsité de l'entrée détruit le
modèle (densité 5,1 % ⇒ perplexité ×107). Détail dans
[`rapport-tete-restreinte.md`](rapport-tete-restreinte.md).

## Ce qui est mesuré puis **gardé**, avec son avertissement
--- eparsite 60-66 ---

1. **Oui, un modèle ternaire est déjà creux** — ici 26.3 % de non-nuls, sans aucun élagage. C'est le point de départ, pas une contrainte ajoutée.
2. **L'encodage événementiel « bitmap + signe » domine le dense** : 1 + d bits/poids contre 2, soit jusqu'à 2× moins de trafic. Il ne coûte jamais plus cher.
3. **Le CSR, lui, est disqualifié** : rentable seulement sous 6 % (indice 32 b) ou 12 % (indice 16 b) de densité — un régime que les LLM n'atteignent pas sans s'effondrer.
4. **Le vrai obstacle n'est pas le poids, c'est l'activation** : un événement n'existe que si le poids *
… [2996 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction du rapport chiffré et envoi au parent

- **send_message** `{"agent_id": "d31b3d9b-58e4-4d34-85fa-381b6f6a6a76", "message": "RAPPORT — Parcimonie des activations et mode événementiel (Drave). Aucun fichier modifié, aucune compilation lancée. Légende : [M]=mesuré dans le dépôt, [D]=déduit/projeté par l'auteur, [S]=supposé/déclaré sans mesure. Toutes les mesur … [12629 caractères tronqués]`

  ```
message delivered to agent d31b3d9b-58e4-4d34-85fa-381b6f6a6a76
  ```

### 🤖 Assistant

⏵ Rapport livré au parent ; restitution du résultat

Inventaire factuel et chiffré — parcimonie des activations et mode événementiel (Drave). Aucun fichier modifié, aucune compilation lancée.
Légende : **[M]** mesuré dans le dépôt · **[D]** déduit/projeté par l'auteur du rapport source · **[S]** supposé. Toutes les mesures [M] sont sur 2×Xeon E5-2687W v3, 16 threads (`reports/rapport-cpu-aer.md:14`).

## 1. Le mécanisme exact
- Un **événement** = une activation quantifiée non nulle poussée vers ses destinations : `SparseVec { idx: Vec<u32>, val: Vec<i32> }` (`engine.rs:29-32`) ; en mode listes « une paire EST un événement » (`model.rs:4535-4540`, test `list.rs:1591`). Événement ≠ paire payée : les chemins denses (MLA f32, experts IQ déquantifiés, tête, 4 bits) paient la matrice entière sans liste (`rapport-p0-flux.md:29-34`).
- Construction : `quant_scratch(x, levels, thresh, topk, renorm, scratch)` (`model.rs:4401-4451`). Échelle `s = max|x|/levels` (4406), `q = round(v/s)` (4428/4446). Si `topk>0` → **k-WTA** : `k = round(topk/1000 × dimension)` borné `[1,dim]` (4419-4420) ; seuil = (len−k)-ième magnitude via `select_nth_unstable_by` (4425) ; garde si `|v| ≥ cut` **et** `q ≠ 0` (4426-4429). `topk` est un **pour-mille de la dimension**, pas un k absolu. Sinon seuil absolu : `q ≠ 0` et `|q| > thresh×levels` (4409, 4447). `renorm` remet la L1 des gardés à celle du vecteur complet (4431-4443).
- Défauts : `act_levels=127` (8 bits) en inférence/modes flux (`main.rs:873,2493` ; `model.rs:4339`), `32767` (16 bits) en perplexité (`main.rs:5091`) ; `act_thresh=0.0`, `act_topk=0`, `act_renorm=false`, `act_topk_proj=[0;7]`, `attn_topk=qk_topk=moe_topk=0` (`model.rs:4339-4341`) ; `seuil_push=0.22` (`model.rs:4358`).
- CLI : `--act-thresh`, `--act-topk`, `--topk-q/k/v/o/gate/up/down` (`main.rs:754-762`), `--act-renorm` (781), `--abits` (736 ; niveaux = `(1<<(abits−1))−1`, borné 16, `main.rs:2477-2490`), `--attn-topk/--qk-topk/--moe-topk` (742-747), `--profil-neurones` (791). **Aucune option `--act-levels`** : les niveaux ne se règlent que par `--abits`.
- `--flux` n'est **pas** le mode événementiel : c'est la sortie texte en flux (`main.rs:591,1156`). Le transport en listes = `--flux-liste`/`--flux-blocs` (771-772), protocole TCP v6, en-tête 79 o portant le contrat d'activation complet (`main.rs:2525,2558-2561`).
- Bascule dense→liste : `matvec` choisit push/pull selon `frac > seuil_push` (`model.rs:4492-4504`) ; `--auto` charge les deux et bascule par mesure, `--push`/`--dense` forcent (`main.rs:775-777`). Chemins q4 (4482-4491) et déquantification IQ (4613-4630) toujours denses.
- Format DRVF : en-tête 14 o (`model.rs:2117-2128`), puis u16 couche, u32 position, u32 n, f32 échelle (2210-2213). v1 = u32+i16 (6 o/actif) ; **v2 défaut** = écart u8 (255 → absolu u16) + i16 (3 o/actif) ; v3 (`DRAVE_TRACE_BLOCS=1`) = i8 + échelle f16/32 canaux (2 o/actif + 4+2·⌈n/32⌉) (2143-2183, 2215). Tracé = entrée quantifiée de l'attention (couche L, 7029-7035) et de la FFN (L+1000, 7522-7528).
- Le chemin par **lots** est dense → 0 événement (`note-cancellation-evenementielle.md:69-70` ; `model.rs:5349-5352`). Codec de référence : `tools/flux_codec.py:10-36,131` ; lecteurs `analyse_flux.py:57-81`, `granularite_flux.py:36-47`, `trace_compacite.py`, `approximabilite_bloc.py:16-18`.

## 2. Taux d'activité mesurés
| modèle / couche | mesure | source |
|---|---|---|
| Qwen2.5-0.5B Q8_0 (494 M poids, 24 c., hidden 896) | densité des poids **99,2 %** | `rapport-8bits.md:7` ; `rapport-mode-listes.md:7` [M] |
| idem, seuil nul | **0,00 %** d'activations nulles ; **352,7 M** événements/token | `rapport-parcimonie-imposee.md:17` ; `rapport-inference.md:271` [M] |
| idem, trace 512 jetons | 24 576 listes · **22 008 776 actifs** (≈99,9 %) | `docs/format-flux.md:64` ; `rapport-compacite-trace.md:59` [M] |
| idem, trace `--act-thresh 0.05`, 256 j. | 8 791 414 actifs → **39,9 %** | `rapport-compacite-trace.md:58` [M] |
| idem, **par couche** (seuil 0.05) | **20,1 % (c.9) à 56,3 % (c.1)** ; aussi 45,6/40,5/29,2/28,8/26,7/25,9 % | `rapport-analyse-flux.md:17-22` [M] |
| idem, `--profil-neurones` (5 % du max), 512 j. | **17,9 %** des neurones/jeton ; **0,08 %** tirés >90 % du temps ; 2,82 % >50 % ; 1/10/50 % les plus lourds = 12,3/33,1/74,2 % | `rapport-localite-activation.md:43-47` [M] |
| idem, persistance | **0,89 à 1,90 %** d'actifs dans ≥90 % des jetons | `rapport-analyse-flux.md:30` [M] |
| Qwen 0.5B, attention top-32 | **12,5 %** (ctx 256) ; 3,1 % (1 024) ; 0,78 % (4 096) ; poids d'attention 0,04 M paires/token contre **354 M** événements | `rapport-attention-creuse.md:43-46,112` [M] |
| V4-Flash `l_last` (16 384 val. = 4 hc × 4 096) | **12 071 / 9 448 / 5 829 / 3 193** événements à θ=0,01/0,02/0,05/0,10 | `rapport-granularite-flux.md:20-23` [M] |
| trace code 64 jetons | 34 335 939 o, 27 265 463 événements = **419 469/jeton** | `note-cancellation-evenementielle.md:63` [M] |
| GLM-5.3 (MLA + experts IQ) | **58,2 G paires/token — 0 en listes** | `rapport-p0-flux.md:60-64` [M] |
| gpt-oss / GLM MoE | **4 experts sur 128** par couche et jeton (3,1 %) ; 8/256 (3 %) | `rapport-localite-activation.md:59` ; `rapport-p0-flux.md:73-74` [M] |
| SpikeGPT (valeur externe) | **R̂ = 0,15** → ~6,7× moins d'événements | `rapport-croisement-push-pull.md:56` [D] |

## 3. Gains mesurés (et conditions)
- **Croisement push/pull**, `blk.0.ffn_gate.weight` (4 864×896, 4,36 M poids, 16 threads) : push/pull = 0,03/0,12/0,28/0,48/1,11/2,15/4,69 à 0/1/5/10/25/50/100 % → **croisement ~22 %**, pas 10 % (`rapport-croisement-push-pull.md:33-46` ; `rapport-mur-memoire-4bits.md:50-53`) [M]. Autres matrices : `attn_q` 24 %, `ffn_down` 33-45 % (bruyant, 45-48).
- **--auto**, modèle entier, 255 jetons : 11 % → 9,1→**7,1 s** (×1,28) ; 5 % → **6,2 s** (×1,47) (croisement:94-98) [M].
- Bascule pull sur modèle dense : **×2,27** (13,6 → 30,7 tok/s, 510 j.), PPL identique (croisement:107-108) [M] ; push 15,59 vs pull dense corrigé **36,43 tok/s**, même PPL 24,8995 (75-77).
- Octets : listes **1,98 o/événement** vs dense int8 1,00 vs 4 bits 0,53 (`rapport-passage-a-l-echelle.md:39-41`) [M]. En mémoire : 1,44 o/poids pour 494 M poids contre 1,06 en Q8_0 dense (**+36 %**) (`rapport-inference.md:195-197`) [M].
- Transport : 3 623 o → **1 568 o** (÷2,3) pour 2,74e-2 d'écart (`transport-liste.md:176-178`) ; blocs 0,01 = 2 268 o/2,7e-2 (`REPRISE.md:926-928`) ; mode 4 **1 500 o/jeton contre 3 663** en lot dense, écart 3,03e-2 (`mode4-lot-listes.md:25-31` ; `REPRISE.md:994`) [M].
- Trace disque : 132 396 736 → **66 370 408** (−49,87 %, rejeu identique 19,3885) → **45 079 930** (−32,1 %, +0,074 % PPL) (`format-flux.md:58-65` ; `REPRISE.md:967-970`) [M]. v1 = **6,04 o/actif** contre ~2 sur le câble ; zstd -19 = 1,27 o/actif (**−79 %**) (`compacite-trace.md:43-45,93`) [M].
- Parcimonie imposée (jeu B tenu à l'écart) : FFN 85 % = **−13,1 % d'événements pour +0,46 % de PPL** (`parcimonie-imposee.md:71`) [M] ; temps CPU −12,7 % (calme) à −3,0 % (load 8-14), fourchette 3-13 % (96-105).
- Noyau AER : **7,79 G év/s** à 16 threads avec décodage par écarts (`cpu-aer.md:24-26`) [M] ; en moteur 3,9 → **5,3 G év/s** après suppression de la liste des destinations (+35 %, PPL identique) (`inference.md:84,216-219`) [M].
- Lot sur lien 20 ms : **18×** (47,6→2,6 s) ; **7×** par jeton en local (`prefill-reparti.md:51-61`) [M].
- Matériel : CPU 5,3 G évts/s [M] ; GPU dispersion **18,1 G évts/s** [M] ; FPGA 4,83 G évts/s [D], ~8,3 nJ/événement [D] contre ~57 nJ CPU [M] (`bilan-multi-materiel.md:45-48`).

## 4. Les trous
- **Aucun volume d'activation par expert** n'est mesuré (vidage par expert inexistant) ; aucune latence par liste (`granularite-flux.md:94-100`).
- Chemins à **0 événement** : lots/préremplissage (`note-cancellation:69-70`), MLA f32 et experts IQ (`p0-flux.md:19-21,63-64`) ; compteur de paires de `forward_lot` limité à q/k/v (130-133).
- V4-Flash : `--dense` **inerte**, « dont en listes » = 0,0 M (`REPRISE.md:751-755`).
- Densité par couche : **un seul modèle** (Qwen2.5-0.5B), un seuil (0.05), 256 jetons (`analyse-flux.md:7-10`). Rien pour gpt-oss, V4-Flash, GLM.
- Les 17,9 % sont à seuil 5 %, réglage de **coût** : PPL 2 445 à ce seuil (`analyse-flux.md:8-10`) ; densité 5,1 % ⇒ PPL **×107** (`optimisations-auto.md:117`). Taux d'activité et qualité ne sont pas au même point de fonctionnement.
- Unité « événements/token » ambiguë : `parcimonie-imposee.md:28` annonce 352,8 M pour 512 jetons puis étiquette la colonne « /token » avec 343,8 M (32-37) ; `inference.md:271` écrit 352,7 M/token.
- Le croisement 22 % vient d'**une matrice** ; énergie et débit FPGA sont **projetés** (`bilan-multi-materiel.md:46-47`). Le « R̂ = 0,15 » est externe (SpikeGPT), non mesuré ici.
- Seuil de profilage 5 % (`model.rs:4691`) sans justification de qualité ; le critère « valeur quantifiée non nulle » est inutilisable (densité mesurée **51 104 %**, `localite:37`). Temps mesurés sous charge 8-14 pour partie (`parcimonie:96-97`).

## 5. Hypothèses réfutées
- **Le seuil absolu suffit** : −11,5 % d'événements → +5 % PPL ; −34,6 % → ×1,59 ; −58,9 % → **×117** (`parcimonie-imposee.md:32-37`). Le k-WTA est ~10× meilleur (49-52).
- **La renormalisation homéostatique compense** : elle dégrade (+0,2/+1,2/+3,6 % à 90/85/80 %) (84).
- **Parcimonie uniforme = parcimonie ciblée** : −14,9 %/+1,23 % contre **−13,1 %/+0,46 %** (67-71).
- **Croisement à 10 %** → **22 %** (`croisement:43-48` ; `mur-memoire:50-57`) ; `README.md:34` le dit encore à 10 % (`coherence-docs.md:128`).
- **« Le mode liste est 8 % plus rapide que le dense »** → faux : 15,59 vs **36,43 tok/s** après correction de l'accumulation i64 (66-77).
- **La granularité fine compresse** → non : à erreur égale G=1 = 43,3 % du dense contre **68,1 %** pour G=512 ; elle route (37-47,66-68).
- **Transmettre l'entrée normée** : 0,00e0 → **5,61e0** (`transport-liste:65-70`).
- **L'écart croît avec la longueur** → il décroît : 1,37e-1 (64 j.) → **1,32e-2** (1 024 j.) (147-152).
- **Préchargement statique des neurones chauds** → ensemble toujours chaud = **0,08 %** ; localité dynamique (`localite:49-54`).
- **L'attention creuse fait gagner du temps** → aucun gain : 11,5 ms dense, 11,5 ms à k=32, **11,6 ms à k=1** ; le coût est dans les scores (`attention-creuse:91-103`). Gains réels : qualité +0,5 à +1,2 % (109), poids creux (110).
- **Attention creuse + k-WTA FFN s'additionnent** → non : **+0,19 %** au lieu de −0,52 % (154-157).
- **Le creux gagne** : CSR rentable seulement <6 %/<12 % de densité (`eparsite:63`) ; le 4 bits ne paie pas : −12 % d'événements, +14 % de débit, **+12 % de PPL** (`inference:255-258`).
- **Un LLM dense a un débit variable** : 0,00 % de zéros, débit constant (`parcimonie:17` ; `inference:189-192`).
- Bug historique : k-WTA **inversé** gardait les k plus petites → 3,8 M événements au lieu de 349 M (`parcimonie:121-123`). Encodage unaire : 42,45 opérations/poids contre **3,10** (`mode-listes:21-22,40-41`).
- **Le compteur d'événements décrit le coût** : MLA + IQ affichent « 0 événement » pour **58,2 G paires payées** par jeton (`p0-flux:23-24,60-64`).

