# Session DSH — relecture

- identifiant : `1966e052-ebc6-4f4b-b7f9-6d1c6cb4b445`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-08 09:18:41
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », drave-core/). LECTURE SEULE STRICTE : ne modifie aucun fichier, ne compile pas, ne lance aucun test ni binaire.

Objectif : inventorier les capacités d'EXPLOITATION DU GPU (et du tandem de GPU) du moteur.

À examiner :
- drave-core/src/gpu.rs : quelles fonctions, quels noyaux (kernels), quelles variables d'environnement (DRAVE_GPU, DRAVE_GPU_KV, DRAVE_GPU_TOPK, DRAVE_GPU_TETE, DRAVE_GPU_EXPERTS, DRAVE_GPU_EXPERTS_GO...), quel critère de dispatch automatique (taille du tenseur en Mo ? type de quantification ? seuil 8 Mo ?), combien de GPU reconnus (« second », « machines », choix par index ?), comment l'instance est initialisée, ce qui est REFUSÉ.
- drave-core/src/model.rs : où le dispatch GPU est appelé (lignes), quels chemins (projections Q8_0, KV, top-k attention, tête).
- docs/plan-gpu-topk.md, reports/rapport-gpu-scores.md, reports/rapport-gpu-tandem-nvlink.md, reports/rapport-gpu-topk-selection.md, reports/rapport-logits-gpu-vs-cpu.md, reports/rapport-cache-experts-vram.md, tools/trace_gpu.py, tools/gpu_*.py (s'il en existe), bench/ et la présence d'un dossier gpu/ ou gpu/compiler.sh.
- Ce qui teste le GPU dans une porte : grep « DRAVE_GPU » dans tools/portes.sh, tools/porte-flux.sh, tools/*.sh ; les tests Rust (#[cfg(test)] / mod tests) qui touchent gpu.rs.

Rends un condensé FACTUEL en français, maximum 45 lignes :
1) Tableau des capacités GPU : nom, ce qu'elle fait, variable qui l'active, fichier:ligne, chiffre mesuré s'il existe (gain de temps, écart de perplexité, écart numérique, Go/s, ms).
2) Critère exact du dispatch automatique des projections (copie la condition du code).
3) Combien de GPU simultanément utilisés et comment (premier/second, tandem, NVLink ?).
4) Ce qui est couvert par une porte automatisée vs mesuré à la main seulement vs non testé.
Distingue « mesuré », « déduit », « supposé ». Donne chemins et numéros de ligne.
Your parent agent id is "482522d1-31f1-43eb-ae9c-a681336404f7". Before you finish, send your result to that agent with send_message({ agent_id: "482522d1-31f1-43eb-ae9c-a681336404f7", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Inventaire lecture seule des capacités GPU de drave-core

Je commence par repérer les fichiers pertinents.

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"---\"; ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src 2>/dev/null; echo \"--- docs\"; ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs 2>/dev/null | head -50", "description": "List repo root … [21 caractères tronqués]`

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
… [3805 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l drave-core/src/gpu.rs drave-core/src/model.rs 2>/dev/null; echo \"--- tools\"; ls -la tools/ 2>/dev/null | head -60; echo \"--- reports gpu\"; ls -la reports/ 2>/dev/null | grep -i gpu; echo \"--- bench\"; ls -la bench/ 2>/dev/ … [134 caractères tronqués]`

  ```
1573 drave-core/src/gpu.rs
  9237 drave-core/src/model.rs
 10810 total
--- tools
total 1508
drwxr-xr-x. 1 stephane stephane   4850  7 oct 20:59 .
drwxr-xr-x. 1 stephane stephane    612  7 oct 18:16 ..
-rwx--x--x. 1 stephane stephane  11640  1 oct 04:21 aiguille.py
-rw-------. 1 stephane stephane   7797  6 oct 22:04 amplification.py
-rwx--x--x. 1 stephane stephane   8850  1 oct 17:40 analyse_empreinte.py
-rw-------. 1 stephane stephane   4614  2 oct 17:28 analyse_engram.py
-rwx--x--x. 1 stephane stephane  11086  1 oct 20:13 analyse_experts_statique.py
-rwxr-xr-x. 1 stephane stephane   5449  3 oct 04:19 analyse_flux.py
-rwx--x--x. 1 stephane stephane   6767  3 oct 09:42 analyse_hc.py
-rwx--x--x. 1 stephane stephane   6364  3 oct 08:11 analyse_octets_par_jeton.py
-rwx--x--x. 1 stephane stephane   6029  3 oct 11:51 analyse_reutilisation_experts.py
-rw-------. 1 stephane stephane   5049  3 oct 13:04 analyse_union_experts.py
-rw-------. 1 stephane stephane   4815  7 oct 10:32 ancre_professeur.py
-rwxr-xr-x. 1 stephane stephane   2995  5 oct 10:44 applique_pont.py
-rwxr-xr-x. 1 stephane stephane   6030  5 oct 08:43 approximabilite_bloc.py
-rwx--x--x. 1 stephane stephane   3776  3 oct 11:5
… [3747 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de gpu.rs et recherche des variables DRAVE_GPU

- **grep** `{"pattern": "DRAVE_GPU", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
Found 250 of 587 matches

REPRISE.md
Line 410: > changements) : gpt-oss avec `DRAVE_GPU=1` donne **15,1667**, la valeur attendue
Line 695: | GPU | noyaux PTX + API pilote, tête et projections opt-in (`DRAVE_GPU=1`) |
Line 782: | 7 | noyaux GPU | **fait, quatre formats** | warp par ligne : tête **Q8_0** (1,6 ms contre 7,3 CPU, écart 2e-7), **MXFP4** (0,1 ms, écart **0,00e0** — bit à bit), **Q4_K** (0,5 contre 1,2 ms, 4e-7), **Q6_K** (3,6 contre 8,3 ms sur la tête liée de 191 Mo, 3,3e-7 ; ×5 sur un tenseur de 11 Mo). **Tête Q6_K branchée** dans le moteur : `DRAVE_GPU=1 DRAVE_GPU_TETE=1` → 7,58 → **3,60 ms/jeton**, perplexité identique (13,6877). Reste le cache d'experts chauds en VRAM : la mesure d'activation (`rapport-localite-activation.md`) dit qu'un préchargement statique ne paie pas sur SiLU |
Line 783: | 8 | suite du plan 1 M | **fait pour E4/E5** | **E4 KV déporté en VRAM** : noyaux `attn_kv_*` (tuiles de 32 clés, softmax en ligne, recombinaison + puits), miroir du cache **paginé** (capacité doublée à la demande : 0,05 Go de VRAM à ctx 1 M après 512 jetons) et `DRAVE_GPU_KV=1` — à 1 M de clés l'attention passe de 968 ms à **13,2 ms** par couche (int4, ×73) et, dans le moteur à
… [39008 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs", "limit": 300}`

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
… [13701 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du reste de gpu.rs (noyaux, dispatch, tandem)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"pub fn \\|^fn \\|^    fn \\|^pub struct \\|^    pub fn \" drave-core/src/gpu.rs", "description": "List functions in gpu.rs"}`

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
43:fn cu_ctx(ctx: *mut c_void) {
62:fn erreur(code: c_int, ou: &str) -> String {
74:pu
… [2287 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"8 \\* 1024 \\* 1024\\|8_388_608\\|8 Mo\\|second\\|machines\\|deux GPU\\|Gpu2\\|ordinal\" drave-core/src/gpu.rs | head -60", "description": "Find dispatch threshold and multi-GPU refs"}`

  ```
19:    fn cuDeviceGet(dev: *mut c_int, ordinal: c_int) -> c_int;
178:    pub ordinal: c_int,
195:    pub fn ouvrir(ordinal: c_int) -> Option<Gpu> {
200:            let rc = cuDeviceGet(&mut dev, ordinal);
346:                       f_attn_part, f_attn_recombine, ordinal,
347:                       nom: format!("GPU {ordinal}"), memoire_libre: libre })
518:    /// faisait 24 000 micro-copies et y passait un quart de seconde.
1538:pub fn second() -> Option<&'static Gpu> {
1541:        let premier = instance().map(|g| g.ordinal).unwrap_or(0);
1552:/// Les périphériques disponibles, dans l'ordre — un seul si la seconde carte est
1554:pub fn machines() -> &'static [&'static Gpu] {
1558:        if let Some(b) = second() { v.push(b); }
  ```

### 🤖 Assistant

⏵ Recherche du critère de dispatch dans model.rs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"gpu::\\|charger_proj\\|charger_tete\\|proj(\\|tete_warp\\|tete(\\|second()\\|machines()\\|instance()\" drave-core/src/model.rs | head -80", "description": "Find GPU call sites in model.rs"}`

  ```
586:    pub gpu: Option<crate::gpu::MatriceGpu>,
1559:        let gpu = match (&d, crate::gpu::instance()) {
1565:                machine.charger_proj(blocs, n_out, d8.nb_ligne)
1583:    cartes: std::collections::HashMap<(usize, usize), (crate::gpu::MatriceGpu,
1584:                                                       crate::gpu::MatriceGpu,
1585:                                                       crate::gpu::MatriceGpu, u64)>,
1608:    fn obtenir<'a>(&'a mut self, machine: &crate::gpu::Gpu, l: usize, e: usize,
1610:        -> Option<(&'a crate::gpu::MatriceGpu, &'a crate::gpu::MatriceGpu,
1611:                   &'a crate::gpu::MatriceGpu)> {
1919:    pub fn tete(&self, x: &[f32]) -> Vec<f32> {
2498:    pub tete_gpu: Option<crate::gpu::MatriceGpu>,
2525:    pub kv_gpu: Option<Vec<(usize, crate::gpu::KvGpu)>>,
3150:    pub fn vers_gpu_tranche(&self, machine: &crate::gpu::Gpu, m: &mut crate::gpu::KvGpu,
3171:    pub fn vers_gpu(&self, machine: &crate::gpu::Gpu, m: &mut crate::gpu::KvGpu,
3178:    pub fn miroir_gpu(miroirs: Option<&mut [(usize, crate::gpu::KvGpu)]>, l: usize,
3181:        let machines = crate::gpu::machines();
4209:                          && crate::gpu::instan
… [1394 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs", "offset": 340, "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs</path>
<type>file</type>
<content>
340:             }
341:             cuMemGetInfo_v2(&mut libre, &mut total);
342:             Some(Gpu { ctx, module, f_tete, f_proj, f_tete_warp, f_proj_warp,
343:                        f_mxfp4_warp, f_q4k_warp, f_q6k_warp, f_attn_scores,
344:                        f_attn_topk_histo, f_attn_topk_compte, f_attn_topk_ecrit,
345:                        f_attn_topk_somme, f_attn_topk_tout,
346:                        f_attn_part, f_attn_recombine, ordinal,
347:                        nom: format!("GPU {ordinal}"), memoire_libre: libre })
348:         }
349:     }
350: 
351:     /// Réserve la place d'une matrice de tête et y **copie les poids une fois**.
352:     ///
353:     /// `blocs` est la tranche du fichier GGUF : les blocs Q8_0 y sont déjà dans
354:     /// la disposition attendue par le noyau (34 octets : échelle f16 + 32
355:     /// niveaux), donc la copie est un transfert brut, sans conversion.
356:     pub fn charger_tete(&self, blocs: &[u8], n_out: usize, _n_in: usize, nb: usize) -> Option<MatriceGpu> {
357:         // Le contexte courant est **par fil** : on l
… [5814 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des points de dispatch dans model.rs

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "offset": 1530, "limit": 110}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "offset": 4195, "limit": 130}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
1530:             let emprunt = keep >= 1.0 && std::env::var("DRAVE_SANS_EMPRUNT").is_err();
1531:             match (emprunt, g.q8_blocks(name)) {
1532:                 (true, Some((buf, nb))) =>
1533:                     (None, Some(unsafe { DenseQ8::emprunter_q8(buf.as_ptr(), n_out, n_in, nb) }), None),
1534:                 _ => (None, Some(construire_q8(&w, n_out, n_in)), None),
1535:             }
1536:         } else if auto {
1537:             let emprunt = keep >= 1.0 && std::env::var("DRAVE_SANS_EMPRUNT").is_err();
1538:             let dense8 = match (emprunt, g.q8_blocks(name)) {
1539:                 (true, Some((buf, nb))) =>
1540:                     unsafe { DenseQ8::emprunter_q8(buf.as_ptr(), n_out, n_in, nb) },
1541:                 _ => construire_q8(&w, n_out, n_in),
1542:             };
1543:             (Some(PushMat::build(&w, n_out, n_in)), Some(dense8), None)
1544:         } else {
1545:             (Some(PushMat::build(&w, n_out, n_in)), None, None)
1546:         };
1547:         // Tous les modèles n'ont pas de biais QKV (Qwen3 n'en a pas) : so
… [5187 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
4195:         // La tête N'EST PAS déportée en l'état : mesuré sur gpt-oss, elle passe
4196:         // de 23 à 159 ms. Le noyau lit une ligne par fil, donc des adresses
4197:         // distantes de 34 octets : chaque accès d'une même warp tombe dans une
4198:         // ligne de cache différente. Il faut une warp par ligne avec réduction
4199:         // — à écrire avant de réactiver.
4200:         // Le noyau « une warp par ligne » rend le déport de la tête enfin
4201:         // rentable : l'ancien lisait une ligne par fil (23 → 159 ms mesurés).
4202:         // Opt-in : `DRAVE_GPU_TETE=1`.
4203:         // Têtes liées de la famille Qwen en Q4_K_M : elles sont en **Q6_K**, pas
4204:         // en Q8_0 — sans cette reconnaissance, `DRAVE_GPU_TETE=1` ne faisait rien
4205:         // sur ces modèles (le noyau existait mais aucune tête ne lui était
4206:         // présentée).
4207:         let mut tete_gpu_q6k = false;
4208:         let tete_gpu = if std::env::var("DRAVE_GPU_TETE").is_ok()
4209:                           && crate::gpu::instance().is_some() {
4210:      
… [7601 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des sites d'appel forward (proj, KV, top-k, tête)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs", "offset": 1170, "limit": 60}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs", "offset": 1520, "limit": 54}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs</path>
<type>file</type>
<content>
1170:         if let Some(pos) = out.iter().position(|v| !v.is_finite()) {
1171:             eprintln!("[topk] noyau 4 : sortie non finie à l'indice {pos} — collecte incomplète, \
1172: repli CPU");
1173:             return false;
1174:         }
1175:         true
1176:     }
1177: 
1178:     pub fn attn_kv(&self, m: &mut KvGpu, q: &[f32], n: usize, scale: f32,
1179:                    sinks: Option<&[f32]>, nsplit: usize,
1180:                    part: &mut [f32], out: &mut [f32]) -> bool {
1181:         cu_ctx(self.ctx);
1182:         let rep = if m.n_kv == 0 { 0 } else { q.len() / (m.n_kv * m.hd) };
1183:         let hd = m.hd;
1184:         if rep == 0 || rep > 32 || hd % 32 != 0 || hd / 32 > 4 { return false; }
1185:         if n == 0 || n > m.ctx { return false; }
1186:         if out.len() < m.n_kv * rep * hd { return false; }
1187:         // un partiel par (tranche, tête KV, tête de requête)
1188:         if part.len() < nsplit * m.n_kv * rep * (hd + 2) { return false; }
1189:         let fils = (rep * 32) as c_uint;
1190:         let partage = ((rep * hd + 32 * 
… [2324 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs</path>
<type>file</type>
<content>
1520:             let rc = cuCtxSynchronize();
1521:             if rc != 0 { eprintln!("{}", erreur(rc, "synchronisation")); return None; }
1522:             let mut out = vec![0f32; m.n_out];
1523:             let rc = cuMemcpyDtoH_v2(out.as_mut_ptr() as *mut c_void, m.out_dev, m.n_out * 4);
1524:             if rc != 0 { eprintln!("{}", erreur(rc, "rapatriement")); return None; }
1525:             Some(out)
1526:         }
1527:     }
1528: }
1529: 
1530: /// Instance unique du processus. `DRAVE_GPU` active le déport ; sans lui, aucune
1531: /// ressource vidéo n'est touchée et le moteur reste strictement sur CPU.
1532: static INSTANCE: std::sync::OnceLock<Option<Gpu>> = std::sync::OnceLock::new();
1533: 
1534: /// Le SECOND périphérique, s'il y en a un (deux Quadro sur cette machine). Il
1535: /// sert au KV déporté : la moitié des couches d'un côté, la moitié de l'autre.
1536: static SECOND: std::sync::OnceLock<Option<Gpu>> = std::sync::OnceLock::new();
1537: 
1538: pub fn second() -> Option<&'static Gpu> {
1539:     SECOND.get_or_init(|| {
1540:         if std::env::
… [1280 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des branches forward : proj, KV, top-k, tête, experts

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 40, "offset": 4495}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 45, "offset": 5450}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
4495:         let use_dense = match (&p.d, &p.m) {
4496:             (Some(_), Some(_)) => frac > thresh_auto,
4497:             (Some(_), None) => true,
4498:             (None, Some(_)) => false,
4499:             // Le message porte les DEUX largeurs : c'est ce qui permet de
4500:             // reconnaître la projection fautive (une MLA a wq/wk/wv vides, un
4501:             // modèle à experts a la FFN dense vide) sans backtrace.
4502:             (None, None) => panic!("projection sans aucun format : {} entrées → {} sorties",
4503:                                    x.len(), out.len()),
4504:         };
4505:         if let (Some(machine), Some(mg)) = (crate::gpu::instance(), p.gpu.as_ref()) {
4506:             // Le noyau applique déjà l'échelle d'activation : rien à reprendre.
4507:             let mut xd = vec![0i32; x.len()];
4508:             for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { xd[i as usize] = v; }
4509:             if let Some(y) = machine.proj(mg, &xd, sx) {
4510:                 // Le biais fait partie de la projection : l'oublier donnait un
… [1229 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
5450:                 if groupe && self.kv_gpu.is_some() && nkv * rep == nh && n > 1 {
5451:                     let nsplit = (n / 256).clamp(1, 128);
5452:                     let besoin = nsplit * nkv * rep * (hd + 2);
5453:                     if self.attn_gpu_part.len() < besoin { self.attn_gpu_part.resize(besoin, 0.0); }
5454:                     let puits: Option<Vec<f32>> = lay.sinks.as_ref()
5455:                         .map(|s| (0..nh).map(|h| s[h]).collect());
5456:                     let part = &mut self.attn_gpu_part;
5457:                     // Copie des requêtes du jeton : `qi` emprunte `q` en
5458:                     // mutable pour la norme et la rotation, qui viennent d'être
5459:                     // faites — le noyau, lui, n'a besoin que de lire.
5460:                     let requetes = &qgpu[i * nq..(i + 1) * nq];
5461:                     let sortie = &mut att[i * nq..(i + 1) * nq];
5462:                     if let Some((idx, m)) = self.kv_gpu.as_mut().and_then(|v| v.get_mut(l)) {
5463:                         let machines = crate::gpu::machine
… [1975 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la branche top-k GPU et du cache d'experts

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 80, "offset": 7215}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 50, "offset": 7560}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
7215:                             }
7216:                         }
7217:                         *attn_events += ((h1 - h0) * n) as u64;
7218:                     }
7219:                 }
7220:                 // ---- top-k déporté (étape 4 du plan) -------------------------
7221:                 // Le miroir VRAM était interdit dès que `attn_topk > 0` : la
7222:                 // notation restait donc sur CPU, où elle coûte 968 ms par couche à
7223:                 // 1 M de clés. Les trois noyaux du plan (scores sans relecture,
7224:                 // seuil radix, collecte, somme) rendent maintenant le chemin
7225:                 // complet en VRAM — mesuré 3,90 ms pour 14 lignes × 1 M de clés,
7226:                 // contre 539,9 ms pour l'attention complète sur CPU.
7227:                 //
7228:                 // Opt-in par `DRAVE_GPU_TOPK=1` : le chemin CPU reste le défaut tant
7229:                 // que la porte de perplexité n'a pas montré l'égalité, et tout refus
7230:                 // d'un noyau retombe proprement sur le CPU (aucun résultat partiel
7
… [4707 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
7560:                 for &e in &idx {
7561:                     if let Some((k, loc)) = moe.ou(e) {
7562:                         moe.gate[k].prelire_expert(loc);
7563:                         moe.up[k].prelire_expert(loc);
7564:                         moe.down[k].prelire_expert(loc);
7565:                     }
7566:                 }
7567:                 for (&e, &poids_exp) in idx.iter().zip(poids.iter()) {
7568:                     let w_exp = poids_exp;
7569:                     // Traduction pour les modèles en clusters : l'expert global
7570:                     // `e` n'est pas forcément dans ce nœud.
7571:                     let Some((kexp, loc)) = moe.ou(e) else { continue; };
7572:                     // ---- experts MXFP4 sur le GPU ----
7573:                     // Le noyau MXFP4 est BIT À BIT identique au chemin CPU
7574:                     // (écart mesuré 0,00e0 sur un expert) : seule la vitesse
7575:                     // change, la perplexité ne peut pas bouger. Les poids
7576:                     // montent une fois et restent (cache LRU), sinon 
… [2571 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des tests, des outils et du dossier gpu/

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== cfg(test)/mod tests dans gpu.rs ===\"; grep -n \"cfg(test)\\|mod tests\\|#\\[test\\]\" drave-core/src/gpu.rs; echo \"=== tests touchant gpu dans les autres .rs ===\"; grep -rn \"cfg(test)\" drave-core/src/*.rs | head -20;  … [385 caractères tronqués]`

  ```
=== cfg(test)/mod tests dans gpu.rs ===
=== tests touchant gpu dans les autres .rs ===
drave-core/src/clusters.rs:299:#[cfg(test)]
drave-core/src/engine.rs:942:#[cfg(test)]
drave-core/src/engine.rs:989:#[cfg(test)]
drave-core/src/engram.rs:291:#[cfg(test)]
drave-core/src/formats.rs:2882:#[cfg(test)]
drave-core/src/gguf.rs:1890:#[cfg(test)]
drave-core/src/list.rs:1396:#[cfg(test)]
drave-core/src/list.rs:1425:#[cfg(test)]
drave-core/src/list.rs:1496:#[cfg(test)]
drave-core/src/list.rs:1536:#[cfg(test)]
drave-core/src/main.rs:5489:#[cfg(test)]
drave-core/src/main.rs:5510:#[cfg(test)]
drave-core/src/main.rs:5582:#[cfg(test)]
drave-core/src/main.rs:5845:#[cfg(test)]
drave-core/src/materiel.rs:438:#[cfg(test)]
drave-core/src/model.rs:8457:#[cfg(test)]
drave-core/src/model.rs:8509:#[cfg(test)]
drave-core/src/model.rs:8614:#[cfg(test)]
drave-core/src/model.rs:8914:#[cfg(test)]
drave-core/src/model.rs:9036:#[cfg(test)]
=== dossier gpu ===
total 352
drwxr-xr-x. 1 stephane stephane     94 30 sep 20:15 .
drwxr-xr-x. 1 stephane stephane     82 28 sep 11:58 ..
-rwxr-xr-x. 1 stephane stephane    861 30 sep 08:44 compiler.sh
-rw-r--r--. 1 stephane stephane   3299 30 sep 17:51 cuda_stub.h
-rw-r--r-
… [378 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 40, "offset": 7905}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
7905:                 }
7906:             });
7907:         }
7908:         (0..t).map(|i| (0..vocab).map(|o| out[o * t + i]).collect()).collect()
7909:     }
7910: 
7911:     /// Tête sur le GPU. `None` si aucune tête n'est déportée ou si le noyau
7912:     /// échoue : l'appelant retombe alors sur le CPU. Les deux noyaux ne
7913:     /// s'appellent pas de la même façon — `proj_q6k` applique l'échelle
7914:     /// d'activation, `tete_warp` la laisse à l'appelant.
7915:     fn logits_gpu(&self, xd: &[i32], sx: f32) -> Option<Vec<f32>> {
7916:         let machine = crate::gpu::instance()?;
7917:         let m = self.tete_gpu.as_ref()?;
7918:         if self.tete_gpu_q6k {
7919:             machine.proj_q6k(m, xd, sx)
7920:         } else {
7921:             machine.tete_warp(m, xd).map(|y| y.iter().map(|v| v * sx).collect())
7922:         }
7923:     }
7924: 
7925:     /// **Encode un flux pour le réseau** : la même quantification que la trace
7926:     /// (mêmes `act_levels`, `act_thresh`, `act_topk`, `act_renorm`), donc les
7927:     /// mêmes octets que sur le disqu
… [1474 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des rapports GPU et des portes

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== gpu dans les tests model.rs ===\"; for l in 8457 8509 8614 8914 9036; do echo \"--- autour de $l\"; sed -n \"${l},$((l+8))p\" drave-core/src/model.rs; done; echo \"=== grep -i gpu dans les modules de test ===\"; awk 'NR>=8 … [327 caractères tronqués]`

  ```
=== gpu dans les tests model.rs ===
--- autour de 8457
#[cfg(test)]
mod tests_kv {
    use super::KvCache;

    /// Aller-retour : ce qui est écrit doit se relire à l'erreur de
    /// quantification près, **aux deux précisions**, et une réécriture de la
    /// même position doit effacer l'ancienne valeur (le cache est réutilisé
    /// d'une fenêtre à l'autre).
    #[test]
--- autour de 8509
#[cfg(test)]
mod tests_noeud_partiel {
    use super::*;
    use crate::gguf::tests::{ecrire, gguf_synth, gguf_synth_q4_0};

    #[test]
    fn traduction_par_numero_de_cluster() {
        let d = std::env::temp_dir().join("drave_noeud_partiel");
        let _ = std::fs::remove_dir_all(&d);
--- autour de 8614
#[cfg(test)]
mod tests_hc {
    //! Les hyper-connexions de DeepSeek-V4, comparées à une **seconde**
    //! implémentation : `tools/hc_synthetique.py` recopie les opérations ggml de
    //! `llama.cpp/src/models/deepseek4.cpp` en numpy. Les mêmes formules écrites
    //! deux fois dans deux langages : un écart se voit.
    //!
    //! Les valeurs ci-dessous sont GÉNÉRÉES (`python3 tools/hc_synthetique.py`) ;
    //! ne pas les retoucher à la main. Dimensions minuscules (`hc = 4`, `h = 3
… [1081 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat reports/rapport-gpu-tandem-nvlink.md", "description": "Read tandem NVLink report"}`

  ```
# Le tandem GPU (2 × Quadro RTX 5000, NVLink) : ce qu'il fait, ce qu'il pourrait faire

> Question posée le 03/10 : « fais-tu bon usage du tandem de GPU en NVLink pour
> distribuer la charge principale ? »
>
> Réponse courte : **non — pour V4-Flash et V4.1, la charge principale (le MoE) est
> entièrement sur le CPU, et les deux GPU sont au repos.** Ce n'est pas un oubli :
> c'est la condition même du chemin GPU du moteur qui l'exclut. Ce rapport chiffre
> l'écart et ce qu'il faudrait pour le combler.

## 1. Le matériel, mesuré

```
GPU 0: Quadro RTX 5000 (16 Go)   GPU 1: Quadro RTX 5000 (16 Go)
topologie : GPU0 NV1 GPU1         (NVLink, 1 lien)
nvidia-smi nvlink -s : 25,781 Go/s par lien et par sens
NUMA : les deux GPU sur le node 0 (CPU 0-9,20-29)
PCIe : maximum Gen3 x16 (l'état courant oscille Gen1/Gen2 au repos — abaissement
       de veille classique, à revérifier sous charge)
```

Turing, 16 Go de VRAM chacun : **32 Go au total**, et 25,78 Go/s entre les deux
(soit ~4× le PCIe mesuré du dépôt).

## 2. Ce que le moteur fait des GPU aujourd'hui

Le principe est écrit dans `drave-core/src/gpu.rs` :

> « **les poids restent sur le GPU**. Mesuré : PCIe x8 6,5 Go/s contre 380 Go/s e
… [5384 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des rapports GPU chiffrés et de trace_gpu.py

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== portes.sh GPU ===\"; grep -in \"gpu\" tools/portes.sh tools/porte-flux.sh tools/portes_formats.sh 2>/dev/null | head; echo \"=== main.rs bancs GPU ===\"; grep -n \"gpu-banc\\|banc-topk\\|banc-kv\\|gpu_banc\\|banc_gpu\" dra … [150 caractères tronqués]`

  ```
=== portes.sh GPU ===
=== main.rs bancs GPU ===
124:        (opt.banc_kv > 0, "--banc-kv"), (opt.banc_topk > 0, "--banc-topk"),
125:        (opt.gpu_banc, "--gpu-banc"), (opt.materiel, "--materiel"), (opt.config, "--config"),
146:    if opt.gpu_banc { run_gpu_banc(opt); return; }
540:    infer: bool, ppl: bool, plan: bool, tokenize: bool, gpu_banc: bool, k3_essai: bool,
686:            "--gpu-banc" => { o.gpu_banc = true; 1 }
694:            "--banc-kv" => { o.banc_kv = suivant(i).parse().unwrap(); 2 }
695:            "--banc-topk" => { o.banc_topk = suivant(i).parse().unwrap(); 2 }
3642:/// Banc **des scores d'attention** (`--banc-topk N`) : le premier des trois noyaux
4441:fn run_gpu_banc(opt: Options) {
=== portes.sh entete ===
#!/bin/bash
# Les portes du dépôt, en une commande.
#
# Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien :
# chaque porte est comparée à la valeur ATTENDUE, et le script sort en erreur si
# l'une diverge. Les valeurs sont celles publiées dans les rapports.
#
#   tools/portes.sh            toutes les portes
#   tools/portes.sh rapide     sans gpt-oss (le seul qui prenne ~20 min)

set -u
cd "$(dirname "$0")/.."
D=./drave-core/target
… [1116 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat reports/rapport-gpu-scores.md; echo \"==========\"; cat reports/rapport-logits-gpu-vs-cpu.md", "description": "Read GPU scores and logits reports"}`

  ```
# Noyau GPU de scores d'attention — le premier des trois du top-k

**En une ligne** : les scores d'attention se calculent maintenant **en VRAM**, avec
un écart de **1,6 à 2,3e-7** sur la référence CPU et **40× plus vite** à 262 144 clés —
c'est la brique qui manquait pour que le mode creux (`--attn-topk`) cesse de
retomber sur le CPU au long contexte.

## Ce que le noyau fait

`attn_scores` (dans `drave-core/gpu/drave_gpu.cu`) reprend la tuile de clés du noyau
d'attention complet — chargement coopératif de 32 clés, déquantification int8/int4/
f32, produit scalaire par tête de requête — mais **écrit les scores** `rep × n` au
lieu de les consommer dans une softmax en ligne. Une grille de `n_kv × nsplit`
blocs : le découpage en tranches est celui du noyau complet, et c'est lui qui fait
la différence de débit.

`--banc-topk N` compare les deux chemins sur des clés et une requête
déterministes (même générateur que le banc KV), et chronomètre les deux.

## Mesuré

Qwen2.5-0.5B (2 têtes KV × 64, 7 têtes de requête par tête KV), KV int8, un
Quadro RTX 5000 :

| clés | CPU (20 fils) | GPU | accélération | écart relatif |
|---|---|---|---|---|
> ⚠️ **Correction du 30/09 (même journée)** : le
… [7854 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de trace_gpu.py, du cache d'experts et du plan top-k

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -60 tools/trace_gpu.py; echo \"=== grep env dans trace_gpu ===\"; grep -n \"DRAVE_\\|gpu\" tools/trace_gpu.py | head -30", "description": "Read trace_gpu.py"}`

  ```
#!/usr/bin/env python3
"""trace_gpu.py — tracer le professeur sur GPU, au MÊME format que le moteur.

POURQUOI. Le traçage est le coût fixe de tous nos cycles : 3,7 s par langue avec
le moteur, soit 26 minutes pour les 399 langues de l'article 1 — et le corpus
Wikipedia complet avait demandé des heures. Une passe avant de 50 jetons sur un
0,5 B est, sur un GPU, un problème de quelques centaines de microsecondes : c'est
la même opération, cent fois plus rapide.

CE QUI CHANGE, ET QU'IL FAUT MESURER. Le moteur trace avec ses POIDS QUANTIFIÉS
(Q8_0) et son noyau emprunté ; ici on trace avec les poids d'origine en
safetensors, en fp32. Ce ne sont PAS les mêmes nombres. Un corpus tracé sur GPU
n'est donc comparable à un corpus tracé par le moteur que si on le chiffre — même
discipline que la calibration dense/événementiel (`tools/calibre_modes.py`), et
`--calibrer` le fait : il trace les mêmes textes dans les deux et rend le cosinus
par couche.

LE FORMAT EST CELUI DU MOTEUR — DRVF v2, via `flux_codec.encoder`. C'est
délibéré : tous les outils d'analyse du dépôt (`premiere_couche_semantique.py`,
`profil_couches.py`, `invariance_unites.py`…) lisent ce format, et un corpus GPU
qui ne sera
… [2012 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^#\\|^|\" reports/rapport-cache-experts-vram.md | head -60; echo \"===== PLAN GPU TOPK =====\"; cat docs/plan-gpu-topk.md", "description": "Read experts cache report and topk plan"}`

  ```
1:# Rapport — un cache d'experts en VRAM pour Kimi-K3 : mesuré, et pourquoi c'est non
10:## 1. Le plafond, avant toute mesure
15:| poste | Go/jeton | part |
16:|---|---:|---:|
17:| **experts routés** (16 sur 896) | 25,83 | 29,3 % |
18:| experts partagés (2 par couche) | 12,40 | 14,1 % |
19:| **dense Q8_0** (attention, KDA, MLA, routage) | 48,56 | **55,1 %** |
20:| tête de sortie | 1,30 | 1,5 % |
21:| **total** | **88,09** | |
25:| taux de succès | gain |
26:|---|---:|
27:| 100 % (impossible) | **×1,41** |
28:| 70 % | ×1,26 |
29:| 47 % | ×1,16 |
30:| 25 % | ×1,08 |
32:## 2. Ce que la VRAM peut tenir
42:## 3. Le taux de succès, mesuré sur le routage RÉEL de K3
47:| | K3 (896 experts/couche, 16/jeton) | Qwen3-30B-A3B (128, 8/jeton) |
48:|---|---:|---:|
49:| réutilisation immédiate (t−1 → t) | **30,2 %** | 46,9 % |
50:| LRU 20 experts/couche | **28,7 %** | — |
51:| LRU 32 | 34,5 % | 86,8 % |
52:| LRU 128 | 49,8 % | — |
58:## 4. Le verdict
70:## 5. Ce qui rendrait le chiffre meilleur, et qu'il faut dire
81:## 6. Ce que Strata apporte quand même
===== PLAN GPU TOPK =====
# Plan — le top-k de l'attention dans le noyau GPU (phase 1.1)

**En une ligne** : l'attention creuse (`--attn-topk`) 
… [9457 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Consolidation : banc GPU CLI, sélection top-k, usage miroir KV

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== logits_gpu appels ===\"; grep -n \"logits_gpu\" drave-core/src/model.rs; echo \"=== miroir_gpu appels ===\"; grep -n \"miroir_gpu\\|vers_gpu\" drave-core/src/model.rs; echo \"=== run_gpu_banc ===\"; sed -n '4441,4500p' dra … [156 caractères tronqués]`

  ```
=== logits_gpu appels ===
7834:                match self.logits_gpu(&xd, sxs[i]) {
7915:    fn logits_gpu(&self, xd: &[i32], sx: f32) -> Option<Vec<f32>> {
8077:            if let Some(y) = self.logits_gpu(&xd, sx) { return y; }
=== miroir_gpu appels ===
3150:    pub fn vers_gpu_tranche(&self, machine: &crate::gpu::Gpu, m: &mut crate::gpu::KvGpu,
3171:    pub fn vers_gpu(&self, machine: &crate::gpu::Gpu, m: &mut crate::gpu::KvGpu,
3173:        self.vers_gpu_tranche(machine, m, kvh, pos, 1)
3178:    pub fn miroir_gpu(miroirs: Option<&mut [(usize, crate::gpu::KvGpu)]>, l: usize,
3184:            kvc.vers_gpu_tranche(machine, m, kvh, pos0, t);
5435:                KvCache::miroir_gpu(self.kv_gpu.as_deref_mut(), l, &self.kv[l], pos, 1);
7132:                KvCache::miroir_gpu(kv_gpu.as_deref_mut(), l, &kv[l], pos, 1);
=== run_gpu_banc ===
fn run_gpu_banc(opt: Options) {
    use std::time::Instant;
    let path = &modele_chemin();
    let threads = if opt.threads_impose { opt.threads } else {
        engine::coeurs_physiques().max(1)
    };
    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
    // Le banc porte sur la tête Q8_0, ou sur le tenseur nommé (`--matrix`) quand
 
… [2399 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '155,215p' reports/rapport-gpu-topk-selection.md; echo \"...\"; sed -n '280,360p' reports/rapport-gpu-topk-selection.md", "description": "Read topk selection report key sections"}`

  ```
### Le bug que le banc a attrapé en une ligne

Première version : **le puits était ajouté par chaque fil** alors que chaque fil ne
tient qu'une somme PARTIELLE — la réduction l'additionnait donc 256 fois. Mesuré :
dénominateur ×45,7 et sortie 55× trop petite à k = 1 ; écart relatif 2,05e-1. Une
fois corrigé (`tid == 0`), 4,79e-7. La relecture ne l'aurait pas vu : le code a
l'air juste, et c'est le banc — qui compare à une référence CPU écrite
indépendamment — qui a parlé.

## Étape 4 : le branchement dans le moteur

Le miroir VRAM était **interdit dès que `attn_topk > 0`**
(`groupe = fen == 0 && self.attn_topk == 0 && rep > 1`, `model.rs:3150`) : le mode
creux retombait donc sur le CPU. La condition est complétée par une branche
`DRAVE_GPU_TOPK=1` (opt-in) qui enchaîne les quatre noyaux sur le miroir et ne
publie son résultat que si **tous** rendent `true` — sinon le chemin CPU reprend,
sans résultat partiel.

Vérification A/B, même binaire, même modèle (Qwen2.5-0.5B Q8_0), `--ctx 2048
--limit 1024 --attn-topk 256 --dense` :

| chemin | perplexité | durée |
|---|---|---|
| CPU (`--attn-topk 256`) | 9,4167 | 41,59 s |
| **GPU** (`DRAVE_GPU=1 DRAVE_GPU_KV=1 DRAVE_GPU_TOPK=1`) | **9,4
… [7153 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification finale : portes, noyaux CUDA, refus, usages tandem

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== noyaux dans drave_gpu.cu ===\"; grep -n \"__global__\" drave-core/gpu/drave_gpu.cu | head -25; echo \"=== compiler.sh ===\"; cat drave-core/gpu/compiler.sh; echo \"=== portes.sh commandes ===\"; grep -n '\\$D ' tools/porte … [77 caractères tronqués]`

  ```
=== noyaux dans drave_gpu.cu ===
37:__global__ void tete_q8(const unsigned char* __restrict__ w,
64:__global__ void proj_q8(const unsigned char* __restrict__ w,
124:__global__ void tete_q8_warp(const unsigned char* __restrict__ w,
155:__global__ void proj_q8_warp(const unsigned char* __restrict__ w,
203:__global__ void proj_mxfp4_warp(const unsigned char* __restrict__ w,
255:__global__ void proj_q4k_warp(const unsigned char* __restrict__ w,
315:__global__ void proj_q6k_warp(const unsigned char* __restrict__ w,
415:__global__ void attn_kv_partiels(const void* __restrict__ kdata,
561:__global__ void attn_kv_recombine(const float* __restrict__ part,
624:extern "C" __global__ void attn_scores(const void* __restrict__ kdata,
734:extern "C" __global__ void attn_topk_histo(const float* __restrict__ sc,
781:extern "C" __global__ void attn_topk_compte(const float* __restrict__ sc,
814:extern "C" __global__ void attn_topk_ecrit(const float* __restrict__ sc,
897:extern "C" __global__ void attn_topk_somme(const float* __restrict__ sc,
987:extern "C" __global__ void attn_topk_tout(const float* __restrict__ sc,
=== compiler.sh ===
#!/bin/bash
# Compile les noyaux en PTX — la chaîne qui marche su
… [2247 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== condition groupe KV ===\"; grep -n \"let groupe\\|fait_en_gpu =\" drave-core/src/model.rs | head; echo \"=== mesure experts +6% ===\"; grep -rn \"6 %\\|+6\\|1,06\" reports/rapport-cache-experts-vram.md REPRISE.md docs/cont … [266 caractères tronqués]`

  ```
=== condition groupe KV ===
5447:                let groupe = fen == 0 && self.attn_topk == 0 && rep > 1;
5449:                let mut fait_en_gpu = false;
5468:                            fait_en_gpu = true;
7150:                let groupe = fen == 0 && self.attn_topk == 0 && rep > 1;
7154:                let mut fait_en_gpu = false;
7166:                            fait_en_gpu = true;
7267:                                fait_en_gpu = true;
7312:                            fait_en_gpu = true;
=== mesure experts +6% ===
REPRISE.md:808:| cache d'experts MXFP4 en VRAM (gpt-oss, 32 jetons) | 5,12 → **5,43 jetons/s (+6 %)**, 53,5 % de succès — verdict : ne pas activer par défaut |
REPRISE.md:1393:Décomposition des 365,7 Go de V4.1 : **engram 203,4 Go (55,6 %)** · experts
=== refus attn_scores_sans_relecture ===
4:        let rep = if m.n_kv == 0 || m.hd == 0 { 0 } else { q.len() / (m.n_kv * m.hd) };
6:        if rep == 0 || rep > 32 || hd % 32 != 0 { return false; }
7:        if q.len() % (m.n_kv * m.hd) != 0 { return false; }
8:        if n == 0 || n > m.capacite { return false; }
15:        if besoin * 4 > self.memoire_libre / 4 {
19:            return false;
22:            if m.sco
… [508 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dernières vérifications : mesures KV moteur et outils

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '270,320p' docs/contexte-long.md; echo \"=== outils GPU (nom) ===\"; ls tools/ | grep -i gpu; find . -name \"*gpu*\" -not -path \"./.git/*\" -not -path \"./drave-core/target/*\" -type f 2>/dev/null | head -20", "description":  … [44 caractères tronqués]`

  ```
indexées par vecteur (`vec * nb + i/32`) : écart de 7e7 en int8.

### Dans le moteur (`DRAVE_GPU=1 DRAVE_GPU_KV=1`)

Les DEUX variables sont nécessaires : c'est `DRAVE_GPU` qui ouvre le pilote (`gpu::instance`),
`DRAVE_GPU_KV` qui demande le miroir. Avec la seule seconde, il ne se passe rien — et
rien ne le dit, d'où la note.

Le cache est recopié en VRAM par **tranches contiguës** (une copie par couche et
par tête KV et par lot, pas une par vecteur), et l'attention par jeton emprunte
le noyau dès que la couche est en attention complète (ni fenêtre ni top-k). Le
chemin par lots garde le CPU.

| contexte | mode | perplexité | attention (ms/jeton) | durée du balayage |
|---|---|---|---|---|
| 512 | CPU | 13,1368 | 2,91 | 18,4 s |
| 512 | **KV déporté** | **13,1369** | 3,22 | 17,9 s |
| 4 096 | CPU | 12,2177 | **22,16** | 219,4 s |
| 4 096 | **KV déporté** | **12,2175** | **3,29** | **136,2 s** (−38 %) |

Le poste « attention » devient **plat** (3,3 ms/jeton quelle que soit la
longueur) là où le CPU croît linéairement : à 32 k il serait à ≈ 180 ms/jeton,
à 1 M à ≈ 5,7 s. Le point de croisement est vers **4 000 clés** (en dessous, les
lancements et les recopies coûtent plus que le calc
… [1861 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== banc-kv ===\"; grep -n \"run_banc_kv\\|fn banc_kv\" drave-core/src/main.rs | head; echo \"=== aiguille usage GPU ===\"; sed -n '70,90p' tools/aiguille.py; echo \"=== porte-flux.sh head ===\"; head -25 tools/porte-flux.sh", … [55 caractères tronqués]`

  ```
=== banc-kv ===
144:    if opt.banc_kv > 0 { run_banc_kv(opt); return; }
4262:fn run_banc_kv(opt: Options) {
=== aiguille usage GPU ===
    texte = remplissage[:coupe] + AIGUILLE + remplissage[coupe:]
    invite = texte + "\n\n" + QUESTION

    env = dict(os.environ)
    if args.gpu:
        env["DRAVE_GPU"] = "1"
    if args.gpu_kv:
        env["DRAVE_GPU"] = "1"
        env["DRAVE_GPU_KV"] = "1"
    if args.gpu_topk:
        env["DRAVE_GPU"] = "1"
        env["DRAVE_GPU_KV"] = "1"
        env["DRAVE_GPU_TOPK"] = "1"
    cmd = [Q, modele, "--infer", "--chat", "--flux", "--prompt", invite,
           # Marge de 1024 et non 512 : certaines fenêtres de corpus tokenisent à
           # 4 750 jetons pour une cible de 4 096 (Mesuré), et un prompt PLUS LONG
           # que le contexte ne fait pas échouer le moteur — il le ralentit d'un
           # facteur 10 à 20 sans un mot (mesuré : 13 à 23 min au lieu de 75 s).
           "--n", str(args.n), "--ctx", str(ctx + 1024), "--threads", str(args.threads),
           "--temp", "0", "--lot", str(args.lot)]
    if args.attn_topk > 0:
=== porte-flux.sh head ===
#!/bin/bash
# Porte du DÉCOUPAGE : deux nœuds, un petit modèle, cinq modes de flux.
… [1164 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dernière passe : NVLink dans le code, bancs dans les portes

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== peer/P2P dans gpu.rs ===\"; grep -n \"Peer\\|peer\\|P2P\\|cuMemcpyPeer\\|nvlink\\|NVLink\" drave-core/src/gpu.rs drave-core/gpu/drave_gpu.cu | head; echo \"=== banc dans portes.sh ===\"; grep -n \"banc\\|logits-bin\\|attn- … [280 caractères tronqués]`

  ```
=== peer/P2P dans gpu.rs ===
=== banc dans portes.sh ===
264:            --logits-bin /tmp/porte_our_qwen.bin >/dev/null 2>&1
=== gpu dans tout tools/*.sh ===
=== gpu dans main.rs (affichage options) ===
    }
    // Le top-k déporté est un mode, pas un détail : c'est ici qu'on voit s'il
    // s'applique VRAIMENT à cette configuration, et pourquoi sinon. La ligne
    // existe parce que huit drapeaux « analysés mais jamais appliqués » ont coûté
    // une session entière — et parce que `DRAVE_GPU_TOPK=1` posé sans
    // `DRAVE_GPU_KV` ne faisait rien en silence.
    if std::env::var("DRAVE_GPU_TOPK").map(|v| v != "0" && !v.is_empty()).unwrap_or(false) {
        let bits = mdl.kv.first().map(|k| k.bits).unwrap_or(32);
        let k = mdl.attn_topk;
        let motif = if k == 0 {
            "inactif : --attn-topk n'est pas donné"
        } else if k > 1024 {
            "inactif : k > 1024 (limite du noyau 3)"
        } else if bits != 8 && bits != 32 {
            "inactif : valeurs KV 4 bits (le noyau 3 n'en gère que 8 ou 32)"
        } else if mdl.attn_window > 0 {
            "inactif : la fenêtre garde le chemin CPU"
        } else if mdl.lot > 1 {
            "inactif en mo
… [438 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des valeurs de porte exactes

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"19,3\\|15,6\\|15,1\\|compare \\\"\" tools/portes.sh | head -20", "description": "Extract expected gate values"}`

  ```
30:# lieu de 19,3885 (total) — un instrument faux qui accuse le code.
53:compare "Qwen2.5-0.5B ctx 256" "19.3885" "$v"
60:    compare "Qwen3-30B en clusters (origine : 799,8557)" "799.8557" "$v"
143:        compare "V4-Flash 43 couches ctx 32" "8430.4966" "$p"
183:            compare "gpt-oss-120b MXFP4 ctx 256" "15.6017" "$p"
  ```

### 🤖 Assistant

⏵ Envoi du condensé au parent

- **send_message** `{"agent_id": "482522d1-31f1-43eb-ae9c-a681336404f7", "message": "INVENTAIRE GPU DRAVE (lecture seule, aucun fichier modifié ; M=mesuré, D=déduit du code, S=supposé)\n\n1) CAPACITÉS\n| capacité | effet | variable | fichier:ligne | chiffres |\n|---|---|---|---|---|\n| Pilote + 15 noyaux PTX | API pilo … [5539 caractères tronqués]`

  ```
message delivered to agent 482522d1-31f1-43eb-ae9c-a681336404f7
  ```

### 🤖 Assistant

⏵ Condensé GPU remis au parent, réponse finale

**Inventaire GPU DRAVE** (lecture seule ; M=mesuré, D=déduit du code, S=supposé)

**1) Capacités**

| capacité | effet | variable | fichier:ligne | chiffres |
|---|---|---|---|---|
| Pilote + 15 noyaux PTX | API pilote CUDA, PTX sm_75 chargé à la volée (clang, sans toolkit) | `DRAVE_GPU` (portail) | gpu.rs:1530-1568, 187-347 ; gpu/drave_gpu.cu:37-987 ; gpu/compiler.sh | M: 2× Quadro RTX 5000 16 Go ; NVLink 25,781 Go/s/sens ; PCIe cité 6,5 Go/s (gpu.rs:7) |
| Projections Q8_0 (auto) | poids ≥ 8 Mio copiés UNE fois en VRAM, noyau warp/ligne | `DRAVE_GPU` seul | model.rs:1550-1569 ; appel 4505-4518 | M: 0,5B FFN 4,6 Mo CPU 123 µs / GPU 151 µs ; gpt-oss attn 12,5 Mo 216/187 µs ; PPL gpt-oss 15,1757→15,1667 ; MoE ctx 1024 18,5803→18,3538 (−1,22 %) |
| Tête Q8_0/Q6_K | logits de sortie en VRAM | `DRAVE_GPU_TETE` | model.rs:4202-4227, 7911-7923 (appels 7834/8077) | M: Q8_0 1,6 ms / 88 Go/s, écart 1,99e-7 (CPU 7,3 ms) ; MXFP4 0,1 ms bit à bit ; Q4_K 0,5 vs 1,2 ms, 4e-7 ; Q6_K 3,6 vs 8,3 ms (tête 191 Mo), 3,3e-7 ; moteur 7,58→3,60 ms/jeton, PPL 13,6877 idem |
| Miroir KV | KV recopié en VRAM par tranches, attention complète déportée | `DRAVE_GPU_KV` | model.rs:4230-4282 (alloc), 3150-3190 (copie), 5447-5470 ; gpu.rs:1178 | M: ctx 4096 attn 22,16→3,29 ms/jeton (÷6,7), balayage 219,4→136,2 s (−38 %), PPL 12,2177→12,2175 ; préremplissage 3961 jetons 286,6→63,8 s (×4,5), attn 52,6→2,2 ms (contexte-long.md:305-310) ; 1 M clés int4 968→13,2 ms/couche (×73) |
| Top-k déporté | scores + radix select + collecte + softmax/Σw·V ; noyau 4 fusionné si n ≤ 131 072 | `DRAVE_GPU_TOPK` (+KV) | model.rs:7220-7312 (garde 7242-7246, seuil 7258) ; gpu.rs:561-1176 | M: banc 4 k clés 1,6e-7/31,6× ; 262 k 2,25e-7/40× ; ensemble = CPU 14/14 ; noyau 3 1,0-4,8e-7, 0,07 ms constant ; chaîne 1 M 3,90 vs 539,9 ms CPU (×138) ; moteur PPL 9,4162/9,4167 (2 k), 12,2265/12,2267 ; à 2 047 clés attn 19,58→7,59 (−61 %), balayage −24 % ; à 255 clés GPU perd (7,68 vs 4,21) |
| Cache experts MXFP4 | LRU (couche, expert) en VRAM | `DRAVE_GPU_EXPERTS` / `_GO` (déf. VRAM libre −2 Go) | model.rs:4291-4310, 1573-1639, 7578-7596 | M: gpt-oss 32 jetons 5,12→5,43 tok/s (+6 %), succès 53,5 %, « ne pas activer par défaut » ; 1 expert bit à bit ; K3 plafond ×1,41 (rapport-cache-experts-vram.md) |
| Bancs CLI | `--gpu-banc`, `--banc-topk`, `--banc-kv` | `DRAVE_GPU` | main.rs:4441, 3642, 4262 | M, hors porte |

**2) Critère exact du dispatch auto** (copie, model.rs:1558-1568)
```rust
const SEUIL_GPU: usize = 8 << 20;
let gpu = match (&d, crate::gpu::instance()) {
    (Some(d8), Some(machine))
        if d8.src == crate::list::Source8::Q8_0 && keep >= 1.0
           && n_out * d8.nb_ligne * 34 >= SEUIL_GPU => { ... machine.charger_proj(...) }
    _ => None,
};
```
→ Q8_0 seulement, poids empruntés au mmap (keep≥1, `DRAVE_SANS_EMPRUNT` absent), seuil 8 Mio = `n_out × nb_ligne × 34` octets ; sinon `None` → CPU. Seuil M : croisement entre FFN 4,6 Mo (CPU gagne) et attn 12,5 Mo (GPU gagne), aller-retour ~60 µs (commentaire 1552-1557). Refus : sans `DRAVE_GPU` rien ne part (gpu.rs:1540,1565) ; tête : Q6_K/Q8_0 seulement ; KV : refus si toutes les couches ne tiennent pas OU disposition mixte f32/f16 (model.rs:4245-4279), `kv_assurer` faux si besoin>ctx ou total>VRAM libre (gpu.rs:446-453) ; top-k : k≤1024, bits 8/32, rep≤32, hd%32=0, hd/32≤4, lot=1, fenêtre=0, nkv×rep=nh, `=0`/vide = inactif, tout refus → CPU sans résultat partiel (model.rs:7242-7312, main.rs:494-514) ; experts : MXFP4 + n_expert>0.

**3) GPU simultanés** : **2 au plus, uniquement pour le KV.** `instance()` = 1 carte — `ouvrir_auto` essaie les ordinals **[1,0]** (D : éviter la carte d'affichage) et crée un contexte plutôt que le primaire (gpu.rs:187-211) ; `second()` = un autre ordinal 0-3 (gpu.rs:1538-1548) ; `machines()` = [premier, second] (gpu.rs:1554-1561). Le miroir KV répartit les couches **en tournant** (`idx = l % machines.len()`, model.rs:4239) et le top-k suit la carte de sa couche (model.rs:7249). Projections, tête, experts : `instance()` seul, jamais « second ». NVLink : aucun appel peer/P2P/nvlink dans gpu.rs ni drave_gpu.cu → **D** : le code n'échange jamais entre cartes, NVLink n'est pas exploité explicitement ; **S** : CUDA l'emprunterait si un transfert inter-GPU existait (rapport-gpu-tandem-nvlink.md ; sur V4-Flash/V4.1 les deux GPU sont au repos).

**4) Couverture** — **portes automatisées : aucune ne touche le GPU.** `grep -i "gpu|DRAVE_GPU"` dans tools/*.sh = vide ; `tools/portes.sh` (:53 Qwen 19.3885, :183 gpt-oss 15.6017) et `tools/porte-flux.sh` ne posent aucune `DRAVE_GPU` — les valeurs de porte se mesurent **sans** GPU (REPRISE.md:890, plan-gpu-topk.md:101). gpu.rs (1573 l.) n'a aucun `#[cfg(test)]` ; les tests de model.rs (:8457 `tests_kv`, :8509, :8614, :8914, :9036) ne citent jamais gpu → **D** : zéro test Rust sur le GPU.
- **Mesuré à la main seulement** : tous les chiffres du §1 (bancs CLI, A/B PPL, `tools/compare_logits.py`) ; `tools/aiguille.py` arme `DRAVE_GPU/_KV/_TOPK` (l.74-82) = harnais, pas porte.
- **Non testé / absent** : `--gpu-banc/--banc-topk/--banc-kv` hors portes ; bench/ = seulement cpu_aer.c et cpu_merge.c ; pas de dossier gpu/ à la racine (seulement drave-core/gpu/) ; `tools/trace_gpu.py` = traceur PyTorch/transformers fp32 (safetensors), étranger à gpu.rs (**D** d'après son en-tête) ; chemins de refus (rep>32, hd%32≠0, KV mixte, seconde carte absente, budget experts) jamais exercés par une porte (**D**).
- **Écarts numériques** : noyaux exacts sur dense (logits bit à bit, Δ=0,0000) ; sur MoE le déport déplace la PPL de ~1,2-1,5 % (top-1 change sur 14/511) — cause **S** : bascule du routage top-8, hypothèse étayée non démontrée (rapport-logits-gpu-vs-cpu.md).

Le condensé a été transmis au parent (`send_message` → agent 482522d1…). Aucun fichier n'a été modifié, aucun binaire ni test lancé.

