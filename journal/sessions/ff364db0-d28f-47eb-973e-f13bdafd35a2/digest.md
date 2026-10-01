# Session DSH — relecture

- identifiant : `ff364db0-d28f-47eb-973e-f13bdafd35a2`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-01 05:50:03
- agent : standard


## Tour 1

### 👤 Utilisateur

Relecture ADVERSARIALE de clôture, dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. Tu vérifies les artefacts de la nuit (30/09 19h49 → 01/10 07h39) qui n'ont PAS encore été audités par une relecture. Budget : 20 minutes. Ne modifie AUCUN fichier du dépôt.

Ce qui a déjà été audité (ne refais pas) : les rapports `rapport-gpu-topk-selection.md` (sprints 1-2), `rapport-logits-gpu-vs-cpu.md` (sprint 3), `rapport-aiguille-topk.md` sections sprints 3-4 (sprint 4) et 5-6 (sprints 5-6), les outils `tools/aiguille.py` et `tools/compare_logits.py`.

Ce qui reste à auditer :
1. `REPRISE.md`, la section « Sprint 7 (05h39 → 07h39) : clôture de la nuit — le livelock du contexte » et le tableau « Ce que la nuit a établi (sprints 2 à 6) » : chaque chiffre du tableau doit avoir sa source dans le dépôt (rapports, commits, logs /tmp). Vérifie en particulier : 8 lancements → 2 ; écart 7,2e-7 avec puits et 8,4e-7 sans ; attention plate 4,5–5,0 ms/jeton de 255 à 4 095 clés ; croisement ~300 clés ; ×7,8 à 4 095 clés ; 286,6 → 63,8 s (×4,5) ; 9,4335 / 9,4337 et 2,1e-5 ; |ΔNLL| 0,0000 sur un modèle dense et 0,038 nat + 497/511 sur un MoE ; 4,26 → 38,84 ms/jeton ; k = 1 024 suffit à 8 192 (12,5 %) ; dense 3/3, k = 256 1/3, k = 1 024 3/3 ; 8/9 en dense sur neuf fenêtres ; 18 tests.
2. `README.md`, section « Prochaines étapes » : les affirmations (chemin par lots ignore --attn-topk, 246 s par sonde au lieu de 75, 2 fenêtres sur 3 à k = 256) sont-elles sourcées et exactes ?
3. Le correctif du livelock (`drave-core/src/model.rs` : `KvCache::assurer` et `Model::generate`) : la correction est-elle complète ? Cherche d'autres chemins qui appellent `assurer` ou écrivent dans le cache au-delà de `ctx` (préremplissage par lots, `forward`, le mode réparti, `run_ppl` avec `--limit` > `--ctx`), et dis si l'un d'eux peut encore dépasser le contexte sans être tronqué ou refusé. Vérifie aussi que le nouveau test (`assurer_ne_boucle_pas_au_dela_du_contexte`, dans main.rs) teste bien ce qu'il prétend.
4. Les messages des cinq derniers commits : disent-ils la même chose que les fichiers ?

Méthode : pour chaque écart, (a) fichier/section, (b) ce qui est écrit, (c) ce que dit la source, (d) verdict, (e) correction minimale. Termine par (1) les écarts classés par gravité, (2) ce que tu as vérifié et trouvé conforme, (3) une phrase sur ce qui te paraît le plus fragile dans l'état laissé par la nuit.
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

⏵ Starting adversarial closure review of night artifacts

I'll start by orienting myself in the repo and reading the key files.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -8 && echo \"---DATE---\" && date && echo \"---STATUS---\" && git status --short | head -30", "description": "Show recent commits and repo status"}`

  ```
b3cba4c README et REPRISE : prochaines étapes et compteur de lignes après la nuit
c7fd7ea REPRISE : le livelock corrigé, et le bilan des six résultats de la nuit
32951e9 Le livelock du contexte est corrigé : troncature annoncée au lieu d'une boucle infinie
3209dc5 Sprint 6 : cérémonie (le taux par fenêtre, le livelock du contexte, planning du sprint 7)
45a0c44 Le « ralentissement » est un LIVELOCK : KvCache::assurer boucle sans fin si besoin > ctx (model.rs:1117)
361c186 Nuance : le facteur de ralentissement est un minorant (les deux exécutions à ctx 4608 n'ont jamais fini ; la même fenêtre rend en 85,1 s à ctx 5120)
e4b3ebc Le taux par fenêtre : 9 fenêtres contiguës, 8/9 en attention complète, et le mur du préremplissage
783f1f9 Sprint 6 : le taux de récupération (9 fenêtres × 3 chemins) et le point 16 384
---DATE---
jeu 01 oct 2026 05:50:05 EDT
---STATUS---
 M journal/README.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la && echo \"---TMP---\" && ls -la /tmp/ | head -40", "description": "List repo root and tmp files"}`

  ```
total 236
drwxr-xr-x. 1 stephane stephane   612 30 sep 17:59 .
drwxr-xr-x. 1 stephane stephane  2350 25 sep 11:55 ..
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane    52 25 sep 17:53 data
drwxr-xr-x. 1 stephane stephane   546 30 sep 17:40 docs
drwxr-xr-x. 1 stephane stephane    82 28 sep 11:58 drave-core
drwxr-xr-x. 1 stephane stephane   146  1 oct 05:50 .git
-rw-r--r--. 1 stephane stephane   399 30 sep 10:01 .gitignore
drwxr-xr-x. 1 stephane stephane    34 27 sep 11:39 journal
drwxr-xr-x. 1 stephane stephane    88 25 sep 17:13 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-------. 1 stephane stephane 29437  1 oct 05:49 README.md
drwxr-xr-x. 1 stephane stephane  2214 30 sep 22:47 reports
-rw-------. 1 stephane stephane 51453  1 oct 05:49 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane 10507 30 sep 08:44 run_clusters.py
-rw-------. 1 stephane stephane 12507 30 sep 08:44 run_cpu.py
-rw-------. 1 stephane stephane 11462 30
… [3500 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading REPRISE.md sprint 7 section and the summary table

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --format='%h %ad %s' --date=iso -8 && echo \"---FILES---\" && wc -l REPRISE.md README.md", "description": "Show commit dates and file sizes"}`

  ```
b3cba4c 2026-10-01 05:49:46 -0400 README et REPRISE : prochaines étapes et compteur de lignes après la nuit
c7fd7ea 2026-10-01 05:46:23 -0400 REPRISE : le livelock corrigé, et le bilan des six résultats de la nuit
32951e9 2026-10-01 05:46:06 -0400 Le livelock du contexte est corrigé : troncature annoncée au lieu d'une boucle infinie
3209dc5 2026-10-01 05:39:02 -0400 Sprint 6 : cérémonie (le taux par fenêtre, le livelock du contexte, planning du sprint 7)
45a0c44 2026-10-01 05:33:42 -0400 Le « ralentissement » est un LIVELOCK : KvCache::assurer boucle sans fin si besoin > ctx (model.rs:1117)
361c186 2026-10-01 05:25:20 -0400 Nuance : le facteur de ralentissement est un minorant (les deux exécutions à ctx 4608 n'ont jamais fini ; la même fenêtre rend en 85,1 s à ctx 5120)
e4b3ebc 2026-10-01 04:59:52 -0400 Le taux par fenêtre : 9 fenêtres contiguës, 8/9 en attention complète, et le mur du préremplissage
783f1f9 2026-10-01 03:38:47 -0400 Sprint 6 : le taux de récupération (9 fenêtres × 3 chemins) et le point 16 384
---FILES---
  685 REPRISE.md
  528 README.md
 1213 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Sprint 7\\|Ce que la nuit a établi\\|livelock\" REPRISE.md | head -40", "description": "Locate sprint 7 section in REPRISE.md"}`

  ```
509:### Sprint 7 (05h39 → 07h39) : clôture de la nuit — le livelock du contexte
523:### Ce que la nuit a établi (sprints 2 à 6)
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md", "offset": 440, "limit": 245}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md</path>
<type>file</type>
<content>
440:    bloquant : le garde de réallocation de la collecte était piloté par les
441:    dimensions au lieu des capacités, donc un échec d'allocation au milieu du `||`
442:    laissait un pointeur 0 pour l'appel suivant. Corrigés, avec en plus une fuite
443:    VRAM (`kv_assurer`), trois capacités périmées, quatre copies DtoD non
444:    vérifiées, une boucle infinie latente et un `rep` tronqué ;
445: 4. une SECONDE relecture adversariale, sur le branchement dans le moteur, a
446:    trouvé **un faux résultat silencieux dans un noyau plus ancien** :
447:    `attn_kv_recombine` lisait `sinks[warp]` (tête DANS le groupe KV) alors que la
448:    sortie est écrite par tête GLOBALE — sur gpt-oss, `DRAVE_GPU_KV=1` donnait donc
449:    à la tête `kvh×rep + w` le puits de la tête `w`, jusqu'à 4,65 logit d'écart
450:    (facteur 105 sur le drainage). **Mesuré avant/après** : perplexité gpt-oss ctx
451:    256 `DRAVE_GPU=1 DRAVE_GPU_KV=1` = **17,6531 AVANT** contre **15,1786 APRÈS**
452:    (référence CPU 15,1757 ; Qwen n'a pas de puits, donc la porte de 19,3885 ne
453:    pouvait pas le voir).
… [15910 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Gathering source reports and README section

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la reports/ | head -50 && echo \"---SPRINTS---\" && ls -la sprints/", "description": "List reports and sprints directories"}`

  ```
total 456
drwxr-xr-x. 1 stephane stephane  2214 30 sep 22:47 .
drwxr-xr-x. 1 stephane stephane   612 30 sep 17:59 ..
-rw-r--r--. 1 stephane stephane   371 29 sep 18:39 aiguille-30b.md
-rw-r--r--. 1 stephane stephane   355 29 sep 19:09 aiguille-gpt-oss.md
-rw-------. 1 stephane stephane  9179 30 sep 08:44 bilan-multi-materiel.md
-rw-r--r--. 1 stephane stephane  2465 30 sep 08:44 rapport-8bits.md
-rw-------. 1 stephane stephane  5208 29 sep 19:14 rapport-aiguille.md
-rw-------. 1 stephane stephane 17426  1 oct 05:46 rapport-aiguille-topk.md
-rw-r--r--. 1 stephane stephane  3250 30 sep 10:36 rapport-analyse-flux.md
-rw-------. 1 stephane stephane  7834 30 sep 08:44 rapport-attention-creuse.md
-rw-r--r--. 1 stephane stephane  2532 30 sep 15:30 rapport-attribution-kv.md
-rw-------. 1 stephane stephane  4652 30 sep 08:44 rapport-campagne-parcimonie.md
-rw-------. 1 stephane stephane  5617 30 sep 08:44 rapport-capteur-hebbien.md
-rw-------. 1 stephane stephane 29974 30 sep 15:17 rapport-coherence-docs-2.md
-rw-------. 1 stephane stephane 27057 30 sep 12:32 rapport-coherence-docs.md
-rw-------. 1 stephane stephane 15556 30 sep 13:08 rapport-compacite-trace.md
-rw-r--r--. 1 stephane stephan
… [3252 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Prochaines étapes\" README.md", "description": "Locate Prochaines étapes in README"}`

  ```
496:## Prochaines étapes
  ```

### 🤖 Assistant

⏵ Reading README next-steps, sprint 7 note, and source reports

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md", "offset": 480, "limit": 50}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md</path>
<type>file</type>
<content>
480: reports/                rapports générés
481: ```
482: 
483: ## Lancer
484: 
485: ```bash
486: python3 run_quantify.py --epochs 400      # ~10 s, numpy seul
487: cd drave-core && cargo build --release  # moteur d'événements
488: ./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf --threads 16
489: ```
490: 
491: Aucune dépendance hors `numpy`. (`torch`/`gguf`/`transformers` seront nécessaires
492: plus tard, pour les modèles réels — pas pour le test de principe.)
493: 
494: ---
495: 
496: ## Prochaines étapes
497: 
498: La feuille de route complète est dans [`docs/roadmap.md`](docs/roadmap.md). Ce qui
499: est ouvert aujourd'hui, par ordre de valeur mesurée :
500: 
501: 1. **Le top-k déporté fonctionne — mais pas dans le préremplissage.** Les trois
502:    noyaux sont écrits, fusionnés en un seul (`attn_topk_tout` : descente radix,
503:    collecte et somme par ligne, 8 lancements → 2) et branchés dans le moteur
504:    (`DRAVE_GPU_TOPK=1`) : l'attention creuse déportée est **plate** (4,5–5,0
505:    ms/jeton de 255 à 4 095 clés) là où le CPU monte de 4,26 à 38,84, et le
506:
… [1844 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== SPRINT 07 ===\" && cat sprints/07-cloture-de-la-nuit.md && echo \"=== SPRINT 06 ===\" && cat sprints/06-le-taux-de-recuperation.md", "description": "Read sprint 6 and 7 notes"}`

  ```
=== SPRINT 07 ===
# Sprint 7 — Corriger le livelock du contexte (model.rs:1117) et consolider la nuit : handoff REPRISE/README, portes finales, revue de clôture

- **Début** : 05:39 · **Fin prévue** : 07:39 (boxing de 120 min)
- **Objectif** : Corriger le livelock du contexte (model.rs:1117) et consolider la nuit : handoff REPRISE/README, portes finales, revue de clôture
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.

=== SPRINT 06 ===
# Sprint 6 — Le TAUX de récupération de l'attention creuse : neuf fenêtres à 4096 (dense, k=256, k=1024) et le troisième point de la courbe k(contexte) à 16384

- **Début** : 03:38 · **Fin prévue** : 05:38 (boxing de 120 min)
- **Objectif** : Le TAUX de récupération de l'attention creuse : neuf fenêtres à 4096 (dense, k=256, k=1024) et le troisième point de la courbe k(contexte) à 16384
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.


## Revue — ce qui est livré, mesuré

Durée : 120 min (boxing 120 min). Commits : 4.

  - `45a0c44` Le « ralentissement » est un LIVELOCK : KvCache::assurer boucle sans fin si besoin > ctx (model.rs:1117)
  - `361c186` Nuance : le facteur de rale
… [5288 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Grepping table numbers against repo sources

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for n in \"7,2e-7\" \"8,4e-7\" \"7,8\" \"286,6\" \"63,8\" \"9,4335\" \"9,4337\" \"2,1e-5\" \"0,038\" \"497\" \"511\" \"4,26\" \"38,84\" \"12,5\" \"8/9\" \"4,5\" \"5,0\"; do echo \"=== $n ===\"; grep -rn -- \"$n\" --include=\"*.md\" . … [112 caractères tronqués]`

  ```
=== 7,2e-7 ===
=== 8,4e-7 ===
=== 7,8 ===
./reports/rapport-cpu-aer.md:51:   **cadence d'événements** (7,8 G/s), là où la carte est limitée par sa DDR3.
./reports/rapport-inference.md:251:| **Perplexité WikiText-2** | **24,90** | **27,83** | **+12 %** |
./reports/rapport-gpu-topk-selection.md:62:| 262 144 | 14/14 | 14/14 | 14/14 | **0** | 0,44 ms (224×) | 97,88 ms | 0,45 ms (896×) | 399,21 ms |
./reports/rapport-gpu-topk-selection.md:280:GPU en prend 36 %, à 4 095 clés il est **7,8× plus rapide** (4,97 contre
./reports/rapport-aiguille-topk.md:90:| **k = 256** (6,25 %) | NON (244,7 s) | NON (237,8 s) | NON (237,0 s) | **0/3** |
./reports/rapport-aiguille-topk.md:92:| **k = 512** (12,5 %) | NON (240,5 s) | NON (238,1 s) | NON (237,8 s) | **0/3** |
./run_cpu.py:250:         "   **cadence d'événements** (7,8 G/s), là où la carte est limitée par sa DDR3.",
./journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:12537:⏵ Q4 : perplexité **27,83 contre 24,90** pour le Q8 — 12 % de qualité perdue pour 11 % de mémoire gagnée. Je fige les mesures
=== 286,6 ===
./.git/logs/HEAD:289:9e22ed894d07c1a78c88d312a8fd4b39f7ea2793 2ae761cbdb8ed7cfba3ec36562aa1465301698e1 Stéphane <stephane@l
… [25129 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying top-k selection report numbers

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"e-7\\|e-06\\|lancements\\|avec puits\\|sans puits\\|sinks\\|puits\" reports/rapport-gpu-topk-selection.md | head -40", "description": "Search error magnitudes in topk report"}`

  ```
7:262 144 clés. Le **noyau 3** (softmax sur les k retenus + puits, puis Σ w·V) est
8:écrit et vérifié à **2,7–4,8e-7** — sous le critère de 1e-6 du plan.
81:Effet secondaire de la correction : l'écart du **noyau 1** n'est plus 1,03e-7 mais
82:**1,60 à 2,25e-7** selon la taille — c'est la même mesure faite sur des données non
117:  par tête (56 lancements au lieu de 4).
135:l'hôte. Les puits comptent dans le dénominateur, jamais au numérateur.
142:| 100 | 3 | 0,03 ms | 0,02 ms | **1,04e-7** |
143:| 4 096 | 256 | 0,07 ms | 0,64 ms | **4,79e-7** |
144:| 65 536 | 256 | 0,07 ms | 1,07 ms | **3,10e-7** |
145:| 262 144 | 256 | 0,07 ms | 0,98 ms | **2,70e-7** |
157:Première version : **le puits était ajouté par chaque fil** alors que chaque fil ne
160:fois corrigé (`tid == 0`), 4,79e-7. La relecture ne l'aurait pas vu : le code a
182:noyaux (1e-7 sur les scores) propagée par un top-k dont le **rang** bascule entre
204:mesuré à nombre de jetons égal) — à cause du coût fixe : 8 lancements et 17
210:la chaîne fait **six lancements et cinq recopies par couche et par jeton**, soit
211:~74 000 lancements pour ces 511 jetons, à comparer aux ~0,1 ms de calcul utile par
219:défaut dans un noyau **p
… [1412 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '250,300p' reports/rapport-gpu-topk-selection.md", "description": "Read topk report grid section"}`

  ```
| n clés | noyau 4 (2 lancements) | chaîne (9 lancements) | écart relatif du noyau 4 |
|---|---|---|---|
| 4 096 | **0,13 ms** | 0,22 ms | 7,19e-7 |
| 16 384 | **0,18 ms** | 0,43 ms | 9,15e-7 |
| 65 536 | **0,43 ms** | 0,57 ms | 5,68e-7 |
| 131 072 | **0,85 ms** | 0,89 ms | 6,36e-7 |
| 262 144 | 1,58 ms | **1,35 ms** | 7,01e-7 |

⚠️ **Le noyau fusionné perd au-delà de 131 072 clés** (1,58 contre 1,35 ms) : ses
14 blocs (un par ligne) saturent moins bien la VRAM que les 1 792 blocs de la
chaîne. Le seuil de bascule est donc **mesuré** (131 072) et câblé dans le modèle :
noyau 4 en dessous, chaîne au-dessus.

### La grille propre : une seule variable bouge

Le sprint précédent avait comparé des lignes qui différaient par DEUX variables
(le contexte alloué ET le nombre de jetons). Ici, contexte fixé (16 384), on fait
varier le NOMBRE DE JETONS — donc les clés réellement notées (`n = pos + 1`).
`--attn-topk 256`, 24 couches, Qwen2.5-0.5B Q8_0 :

| jetons | clés vues (moy.) | attention CPU | attention GPU | PPL CPU / GPU |
|---|---|---|---|---|
| 511 | 255 | **4,26** | 4,53 | 13,1358 / 13,1355 |
| 1 023 | 512 | 7,17 | **4,62** | 9,4167 / 9,4162 |
| 2 047 | 1 024 | 12,08 | **4,82** | — |
… [1350 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat sprints/02-fusionner-la-cha-ne-du-top-k-d-port-desc.md", "description": "Read sprint 2 note"}`

  ```
# Sprint 2 — Fusionner la chaîne du top-k déporté : descente radix, collecte et somme dans UN noyau par ligne (8 lancements → 2, plus de tampon nh×n×4), et gagner dès ~1 000 clés

- **Début** : 19:49 · **Fin prévue** : 21:49 (boxing de 120 min)
- **Objectif** : Fusionner la chaîne du top-k déporté : descente radix, collecte et somme dans UN noyau par ligne (8 lancements → 2, plus de tampon nh×n×4), et gagner dès ~1 000 clés
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.


## Revue — ce qui est livré, mesuré

Durée : 119 min (boxing 120 min). Commits : 6.

  - `a76d8c8` REPRISE : le doute sur les projections est à moitié levé (ctx 512 et 1024 identiques, ctx 256 évalue une autre chose)
  - `1dee0e6` REPRISE : sprint 2 (fusion du top-k, croisement à ~300 clés, le filet testé, le doute sur les projections)
  - `5bc4c0c` Grille propre, noyau fusionné dans le moteur, et gpt-oss (les puits en vrai)
  - `ed4ce47` Revue adverse du noyau fusionné : une course bloquante, et cinq autres points
  - `ea1d155` Le filet du noyau 4 doit agir AVANT la somme (test du filet, saboté exprès)
  - `8342f17` Noyau 4 : le top-k complet d'une ligne en UN lancement (8 la
… [7306 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"puits\\|8,38\\|8.38\\|7,19\\|7.19\" reports/rapport-gpu-topk-selection.md | sed -n '1,60p'", "description": "Search sinks and error values in report"}`

  ```
7:262 144 clés. Le **noyau 3** (softmax sur les k retenus + puits, puis Σ w·V) est
135:l'hôte. Les puits comptent dans le dénominateur, jamais au numérateur.
157:Première version : **le puits était ajouté par chaque fil** alors que chaque fil ne
222:KV, puits allant de −1,95 à +3,38), la tête `kvh×rep + w` recevait donc le puits de
236:Qwen2.5 n'a pas de puits : la porte de 19,3885 ne pouvait pas voir ce défaut, et
237:aucun banc ne le couvrait (les bancs KV n'ont pas de puits non plus). C'est la
253:| 4 096 | **0,13 ms** | 0,22 ms | 7,19e-7 |
286:## Les puits en vrai : gpt-oss (le seul modèle qui en a) sous `DRAVE_GPU_TOPK`
288:Qwen2.5 n'a pas de puits : le chemin des puits du noyau 4 n'était exercé que par le
289:banc, avec des puits fabriqués. gpt-oss-120b en a (64 valeurs, une par tête de
291:trouvé le mauvais indexage des puits dans `attn_kv_recombine`.
296:documenté, du calcul d'attention en VRAM. Les puits traversent donc le noyau 4 sans
342:| 3 | `attn_topk_somme` : softmax sur les k retenus + puits, puis Σ pondérée des V | ✅ 1,0–4,8e-7 · temps GPU constant (0,07 ms) |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"8,38\\|8.38e\\|7,19\" --include=\"*.md\" --include=\"*.log\" --include=\"*.txt\" . 2>/dev/null | grep -v journal/sessions | head -20; echo \"=== TMP LOGS ===\"; grep -l \"8.38e\\|8,38\\|7.19e\\|7,19\" /tmp/*.log /tmp/*.out … [81 caractères tronqués]`

  ```
./reports/rapport-gpu-topk-selection.md:253:| 4 096 | **0,13 ms** | 0,22 ms | 7,19e-7 |
./sprints/02-fusionner-la-cha-ne-du-top-k-d-port-desc.md:30:| 3 | banc : noyau 4 vérifié de n = 1 à 1 M, avec et sans puits | écart 7,19e-7 (avec puits) et **8,38e-7** (sans) · bornes n = 1, 100, 2 048, 4 097, 5 000 toutes vertes |
=== TMP LOGS ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '125,170p' reports/rapport-gpu-topk-selection.md", "description": "Read bench section of topk report"}`

  ```
pour la collecte et ≈900× pour le seuil (0,0004 ms au lieu de 0,45 ms, 0,0003 au
  lieu de 0,27 ms). Un affichage mal étiqueté est un affichage qui ment — et il a
  bien failli faire chercher un faux défaut dans le noyau.

## Noyau 3 : le softmax sur les k retenus, puis Σ w·V

`attn_topk_somme` : un bloc par ligne, les k scores rassemblés en mémoire partagée
(le max et le dénominateur se calculent donc une fois par ligne, pas une fois par
composante), un fil par composante pour la somme pondérée. Les indices sont lus
**en VRAM** — ceux que la collecte vient d'y écrire —, donc aucun aller-retour par
l'hôte. Les puits comptent dans le dénominateur, jamais au numérateur.

Référence CPU : mêmes indices (ceux du GPU), mêmes scores (ceux du GPU), valeurs
relues du cache hôte — le seul écart possible vient donc du noyau 3.

| N clés | k | GPU | CPU | écart relatif |
|---|---|---|---|---|
| 100 | 3 | 0,03 ms | 0,02 ms | **1,04e-7** |
| 4 096 | 256 | 0,07 ms | 0,64 ms | **4,79e-7** |
| 65 536 | 256 | 0,07 ms | 1,07 ms | **3,10e-7** |
| 262 144 | 256 | 0,07 ms | 0,98 ms | **2,70e-7** |

Le temps GPU est **constant** (0,07 ms de 4 k à 262 k clés) : le noyau ne lit que
les k scores retenus et 
… [1268 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /tmp/*topk* /tmp/*kv* 2>/dev/null | head -30; echo \"=== grep banc ===\"; grep -rln \"banc-topk\\|banc_topk\" /tmp/*.log /tmp/*.out /tmp/*.txt 2>/dev/null | head", "description": "Find topk bench logs in tmp"}`

  ```
-rw-r--r--. 1 stephane stephane  949 30 sep 16:58 /tmp/aiguille_kv2048.log
-rwxr-xr-x. 1 stephane stephane 1040 30 sep 16:15 /tmp/aiguille_kv2048.sh
-rw-r--r--. 1 stephane stephane  868 30 sep 16:07 /tmp/aiguille_kv.log
-rwxr-xr-x. 1 stephane stephane  874 30 sep 15:10 /tmp/aiguille_kv.sh
-rw-r--r--. 1 stephane stephane  910 30 sep 22:52 /tmp/aiguille_topk2.log
-rw-r--r--. 1 stephane stephane  125 30 sep 22:04 /tmp/aiguille_topk.log
-rwxr-xr-x. 1 stephane stephane  956 30 sep 21:51 /tmp/aiguille_topk.sh
-rw-r--r--. 1 stephane stephane 2067 29 sep 14:21 /tmp/banc_kv2.log
-rwxr-xr-x. 1 stephane stephane  679 29 sep 14:19 /tmp/banc_kv2.sh
-rw-r--r--. 1 stephane stephane 2864 30 sep 15:34 /tmp/banc_kv_cles.log
-rwxr-xr-x. 1 stephane stephane  959 30 sep 15:32 /tmp/banc_kv_clés.sh
-rw-r--r--. 1 stephane stephane 2055 29 sep 14:19 /tmp/banc_kv.log
-rw-r--r--. 1 stephane stephane 2864 30 sep 15:34 /tmp/banc_kv_runner.log
-rwxr-xr-x. 1 stephane stephane  718 29 sep 14:18 /tmp/banc_kv.sh
-rw-r--r--. 1 stephane stephane 1951 30 sep 18:30 /tmp/banc_topk_1M.log
-rw-r--r--. 1 stephane stephane 1260 30 sep 17:56 /tmp/banc_topk_262k_b.log
-rw-r--r--. 1 stephane stephane 1011 30 sep 17:52 /tmp/ban
… [954 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"puits\\|8\\.38\\|7\\.19\\|écart\\|ecart\" /tmp/banc_topk_final.log | head -40; echo \"=== 1M ===\"; tail -30 /tmp/banc_topk_1M.log", "description": "Inspect topk bench logs"}`

  ```
2:  écart max 1.192e-7 sur une dynamique de 7.449e-1 (relatif 1.60e-7)
7:    k-ième score identique au bit près : 14/14 lignes (écart entier max 0)
17:  écart max 1.788e-7 sur une dynamique de 8.385e-1 (relatif 2.13e-7)
22:    k-ième score identique au bit près : 14/14 lignes (écart entier max 0)
32:  écart max 1.788e-7 sur une dynamique de 7.951e-1 (relatif 2.25e-7)
37:    k-ième score identique au bit près : 14/14 lignes (écart entier max 0)
=== 1M ===
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
banc top-k : 1000000 clés · 2 têtes KV × 64 dim · 7 têtes de requête par tête KV · KV 8 bits
  CPU  20 fils :   951.78 ms
  GPU  scores  :    19.49 ms  (48.8× plus rapide)
  écart max 1.788e-7 sur une dynamique de 9.346e-1 (relatif 1.91e-7)
  → conforme au critère du plan (1e-6) : la sélection peut s'appuyer dessus
  top-k k = 256 :
    CPU  tri + comptage :   401.05 ms
    GPU  4 passes d'histogramme :     0.98 ms  (409.0× plus rapide)
    k-ième score identique au bit près : 14/14 lignes (écart entier max 0)
    comptes « strictement au-dessus » et « égaux » : 14/14 lign
… [1137 caractères tronqués]
  ```

- **bash** `{"command": "ls -la --time-style=+%m-%d_%H:%M /tmp/*.log /tmp/*.out /tmp/*.txt 2>/dev/null | awk '$6 >= \"09-30_19:00\" && $6 <= \"09-30_22:30\"' | head -40", "description": "List tmp logs from sprint 2 window"}`

  ```
-rw-r--r--. 1 stephane stephane     125 09-30_22:04 /tmp/aiguille_topk.log
-rw-r--r--. 1 stephane stephane    3896 09-30_22:04 /tmp/compare_logits_gptoss.txt
-rw-r--r--. 1 stephane stephane     217 09-30_20:00 /tmp/fusion_4095.log
-rw-r--r--. 1 stephane stephane     354 09-30_20:35 /tmp/grille_fusion.log
-rw-r--r--. 1 stephane stephane     258 09-30_21:58 /tmp/logits_run.log
-rw-r--r--. 1 stephane stephane     154 09-30_20:53 /tmp/oss_topk2.log
-rw-r--r--. 1 stephane stephane     659 09-30_20:42 /tmp/oss_topk.log
-rw-r--r--. 1 stephane stephane     198 09-30_19:15 /tmp/portes_binaire_final.log
-rw-r--r--. 1 stephane stephane     194 09-30_21:12 /tmp/portes_s2_final.log
-rw-r--r--. 1 stephane stephane     178 09-30_20:10 /tmp/portes_sprint2.log
-rw-r--r--. 1 stephane stephane     640 09-30_19:07 /tmp/topk_16k_final.log
-rw-r--r--. 1 stephane stephane     242 09-30_19:19 /tmp/topk_32k.log
  ```

- **bash** `{"command": "grep -l \"puits\\|sinks\" /tmp/*.log /tmp/*.out /tmp/*.txt 2>/dev/null | head -20; echo \"===\"; for f in /tmp/portes_s2_final.log /tmp/grille_fusion.log /tmp/fusion_4095.log /tmp/oss_topk.log /tmp/oss_topk2.log; do echo \"--- $f\"; cat \"$f\"; done", "description": "Search logs for sin … [13 caractères tronqués]`

  ```
/tmp/atk2_B_a_enorme.log
/tmp/atk2_C_nb_enorme.log
/tmp/atk2_D_lg_enorme.log
/tmp/atk_A_etat_vide.log
/tmp/atk_B_a_.log
/tmp/atk_C_nb_.log
/tmp/atk_D_lg_.log
/tmp/atk_E_nb_faux.log
/tmp/atk_enorme.log
/tmp/atk_F_tronque.log
/tmp/atk_G_mode_inconnu.log
/tmp/atk_H_liste_n0.log
/tmp/atk_I_a_hors_dimension.log
/tmp/atk_J_bruit_par_etat.log
/tmp/atk_K.log
/tmp/bad2_cli.log
/tmp/bad3_cli_mode2.log
/tmp/bad3_cli_t_faux.log
/tmp/bad4_cli.log
/tmp/bad_cli.log
===
--- /tmp/portes_s2_final.log
=== portes sprint 2 (binaire final) ===
Qwen Q8_0 ctx 256 : perplexité 19.3885 sur 510 tokens
gpt-oss MXFP4 ctx 256 : perplexité 15.1757 sur 510 tokens
cargo test : test result: ok. 17 passed
--- /tmp/grille_fusion.log
cpu      511 : attention 4.26 | 
gpu      511 : attention 4.53 | 
cpu     1023 : attention 7.17 | 
gpu     1023 : attention 4.62 | 
cpu     2047 : attention 12.08 | 
gpu     2047 : attention 4.82 | 
cpu     4095 : attention 19.77 | 
gpu     4095 : attention 4.86 | 
cpu     8191 : attention 38.84 | 
gpu     8191 : attention 4.97 | 
=== GRILLE FINIE ===
--- /tmp/fusion_4095.log
=== perplexité 12.2265 sur 4095 tokens (0 événements, 142.9 s) ===
    postes (ms/token) : projets-attn 2.49 | rop
… [937 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --all --oneline -S \"8,38e-7\" -- . | head; echo \"=== grep all ===\"; grep -rn \"8,38e\\|8\\.38e\" . --include=\"*\" 2>/dev/null | grep -v \"^./.git/\" | head -10; echo \"=== tmp broad ===\"; grep -rn \"sans puits\" /tmp --i … [76 caractères tronqués]`

  ```
b795f09 Sprint 2 : cérémonie (revue adverse autonome, introspection, planning du sprint 3)
=== grep all ===
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:37058:[DRAVE_BANC_SANS_PUITS=1]  noyau 4 (UN lancement) : 0.13 ms · écart max 1.043e-7 sur 1.245e-1 (relatif 8.38e-7)
./sprints/02-fusionner-la-cha-ne-du-top-k-d-port-desc.md:30:| 3 | banc : noyau 4 vérifié de n = 1 à 1 M, avec et sans puits | écart 7,19e-7 (avec puits) et **8,38e-7** (sans) · bornes n = 1, 100, 2 048, 4 097, 5 000 toutes vertes |
=== tmp broad ===
[timed out after 60000ms]
[killed by signal: SIGTERM]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '37040,37075p' journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md", "description": "Read raw bench output in journal"}`

  ```
- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\np='drave-core/src/model.rs'; s=open(p).read()\nvieux = \"\"\"                attn_idx.clear();\n                if k < n {\n                    attn_idx.extend(0..n as u32);\n                    attn_idx.select_nth_ … [4375 caractères tronqués]`

  ```
F3 : départage CPU déterministe
F7 : idx_ref retiré, chemin sans puits exerçable
build
    ensembles identiques au CPU : 14/14 lignes · différence symétrique 0 indices
    noyau 3 (softmax sur k + Σ w·V) : GPU 0.06 ms · CPU 0.73 ms · écart max 5.960e-8 sur 1.244e-1 (relatif 4.79e-7)
    noyau 4 (UN lancement) : 0.13 ms · écart max 1.268e-4 sur 1.244e-1 (relatif 1.02e-3)
    → AU-DESSUS du critère de 1e-6 : ne pas brancher le noyau 4
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\np='drave-core/src/main.rs'; s=open(p).read()\nvieux = \"\"\"                    let kvh = l / rep;\n                    let mut m = sinks[l];\n                    for &j in ord.iter() { m = m.max(ligne[j as usize]); … [1813 caractères tronqués]`

  ```
référence du banc alignée sur les puits du noyau
0
[]  n
… [1074 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Delegating the model.rs livelock audit while I verify numbers

- **subagent** `{"description": "Audit livelock fix in model.rs", "prompt": "You are doing an ADVERSARIAL code review in the Rust repository /home/stephane/Data13TB/stephane/GitHub/Qtrinet. DO NOT MODIFY ANY FILE. Read-only analysis. Report findings in French, concisely but precisely, with file:line references and  … [2633 caractères tronqués]`

  ```
started subagent 8288d350-b68e-4245-b903-5ef6d71910b4
  ```

### 🤖 Assistant

⏵ Checking the k=256 recovery counts in README vs REPRISE vs report

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '60,120p' reports/rapport-aiguille-topk.md", "description": "Read aiguille topk k-table"}`

  ```
milieu n'entre pas dans les 256 premières. L'attention complète, elle, la
   retrouve.
2. **Les deux implémentations se comportent pareil** (NON aux deux au milieu,
   oui aux deux au début) : le noyau fusionné et le chemin CPU ne divergent pas
   sur un comportement de qualité, pas seulement sur des chiffres.
3. **Le coût du pruning n'est donc pas uniforme** : il est nul là où l'information
   est au bord du contexte, et total au milieu. C'est une raison de plus pour
   l'**index** que le plan de la phase 1.1 rangeait « hors périmètre » : noter
   toutes les clés puis garder les k meilleures ne peut pas retrouver une
   information dont le score est moyen — il faut un mécanisme qui la *cherche*.

## Suite (sprint 4) : le k est un RÉGLAGE, pas une fatalité

⚠️ **Ce que cette grille est, et ce qu'elle n'est pas** — corrigé après la revue
adverse du sprint 4 (et re-corrigé au sprint 5, qui a refait la grille sur trois
textes) : les trois colonnes sont trois **répétitions de la MÊME invite**, pas trois
fenêtres de corpus. Le garde-fou d'`aiguille.py` comparait
l'offset à `len(corpus) - 400_000` alors que le corpus en fait **353 778** : la
remise à zéro se déclenchait donc toujours, et
… [2726 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"2/3\\|1/3\\|3/3\\|2 fois sur 3\\|1 fois sur 3\" reports/rapport-aiguille-topk.md README.md REPRISE.md sprints/*.md | head -40", "description": "Grep all k recovery fractions"}`

  ```
reports/rapport-aiguille-topk.md:89:| attention complète | oui (383,6 s) | oui (326,5 s) | oui (251,5 s) | **3/3** |
reports/rapport-aiguille-topk.md:91:| **k = 1 024** (25 %) | oui (239,6 s) | oui (253,2 s) | oui (244,1 s) | **3/3** |
reports/rapport-aiguille-topk.md:101:structurelle du top-k : **0 à k = 256 (6,25 %), 0 à k = 512 (12,5 %), 3/3 à
reports/rapport-aiguille-topk.md:102:k = 1 024 (25 %)**, référence complète à 3/3. Ce n'est pas « reproductible » au sens
reports/rapport-aiguille-topk.md:154:| attention complète | oui (266,2 s) | oui (280,2 s) | oui (251,1 s) | **3/3** |
reports/rapport-aiguille-topk.md:155:| **k = 256** (6,25 %) | NON (240,3 s) | **oui** (302,2 s) | **oui** (241,4 s) | **1/3** |
reports/rapport-aiguille-topk.md:156:| **k = 1 024** (25 %) | oui (238,9 s) | oui (275,6 s) | oui (265,7 s) | **3/3** |
reports/rapport-aiguille-topk.md:167:  dense 3/3, k = 256 **1/3**, k = 1 024 3/3.
reports/rapport-aiguille-topk.md:169:Trois fenêtres restent un petit échantillon (l'intervalle de confiance d'un 1/3 sur
reports/rapport-aiguille-topk.md:177:| 4 096 (trois fenêtres) | **3/3** | **3/3** (25 % du contexte) | — |
README.md:512:   l'information 2 fois sur 3 (trois fe
… [2029 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '125,185p' reports/rapport-aiguille-topk.md", "description": "Read sprint 5 grid section in report"}`

  ```
Les deux chemins ne donnent pas la même continuation à température 0 — c'est ce qui
rendait le contrôle « tout le passage creux » ininterprétable. Les logits, eux,
disent l'écart réel (Qwen2.5-0.5B Q8_0, ctx 2 048, 511 jetons, mêmes identifiants) :

| | perplexité | écart moyen \|ΔNLL\| | accord top-1 |
|---|---|---|---|
| `--lot 1` | 13,1368 (moteur) / 13,1367 (comparateur) | — | — |
| `--lot 256` | 13,1359 | **0,0007** (médiane 0,0003, p90 0,0017, max 0,0068) | **511/511** |

Le désaccord entre les deux chemins est donc de **7e-4 nat par position en moyenne**
(max 6,8e-3, p90 1,7e-3), et le jeton choisi est le même PARTOUT : ce n'est pas un chemin faux, c'est une
amplification chaotique — un écart de 1e-3 sur un logit suffit à changer un jeton
greedy après quelques dizaines de pas, et une réponse qui doit contenir un code de
8 caractères ne pardonne pas un jeton.

Conséquence pour la méthode : **toute comparaison de qualité doit se faire à lot
fixé**, et les verdicts binaires (trouvé / non trouvé) doivent être lus comme des
révélateurs d'un écart minuscule, pas comme une propriété stable du modèle.

### La grille refaite sur TROIS TEXTES (sprint 5)

L'outil corrigé produit enfin 
… [2212 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking 8/9 windows, prefill log, and logits report

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 8/9 in files ===\"; grep -rn \"8/9\\|9/9\" sprints/ reports/rapport-aiguille-topk.md README.md 2>/dev/null | head; echo \"=== s6 logs ===\"; ls -la --time-style=+%m-%d_%H:%M /tmp/s6*.log /tmp/aig_s6* 2>/dev/null; echo \"== … [106 caractères tronqués]`

  ```
=== 8/9 in files ===
sprints/06-le-taux-de-recuperation.md:14:  - `e4b3ebc` Le taux par fenêtre : 9 fenêtres contiguës, 8/9 en attention complète, et le mur du préremplissage
sprints/06-le-taux-de-recuperation.md:34:**Le contrôle dense est à 8/9, pas 9/9** : la fenêtre 3 (la plus longue, 4 731
=== s6 logs ===
-rwxr-xr-x. 1 stephane stephane 1266 10-01_04:41 /tmp/aig_s6b.sh
-rwxr-xr-x. 1 stephane stephane 1265 10-01_04:41 /tmp/aig_s6.sh
=== s6b ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== prefill_gpu.log ===\"; ls -la /tmp/prefill_gpu.log 2>/dev/null && cat /tmp/prefill_gpu.log; echo \"=== contexte-long 305-320 ===\"; sed -n '300,320p' docs/contexte-long.md", "description": "Verify prefill perplexity source … [2 caractères tronqués]`

  ```
=== prefill_gpu.log ===
-rw-r--r--. 1 stephane stephane 183 30 sep 23:46 /tmp/prefill_gpu.log
CPU      (lot 256, ctx 4096, 1023 jetons) : perplexité 9.4335 sur 1023 tokens
GPU KV   (lot 256, ctx 4096, 1023 jetons) : perplexité 9.4337 sur 1023 tokens
=== PREFILL GPU FINI ===
=== contexte-long 305-320 ===

Mesuré à la fin du sprint 3, avant le sprint 4 (Qwen2.5-0.5B Q8_0, prompt de
3 961 jetons, `--lot 256`, `--infer`) ; ⚠️ ces temps dépendent de la charge — une
re-mesure sous charge (deux autres tâches sur 40 cœurs) donne 372,0 s et 95,9 s,
soit ×3,9 au lieu de ×4,5 :

| chemin | prompt | postes (ms/jeton) |
|---|---|---|
| CPU | **286,6 s** (13,8 tok/s) | attention **52,6** · matvec+mlp 18,4 |
| `DRAVE_GPU=1 DRAVE_GPU_KV=1` | **63,8 s** (62,1 tok/s) | attention **2,2** · matvec+mlp 12,8 |

L'attention du préremplissage est **le** poste dominant sur CPU (73 % du temps :
le terme quadratique), et le miroir VRAM la divise par 24. La qualité ne bouge
pas : à ctx 4 096 et 1 023 jetons, perplexité **9,4335 (CPU)** contre **9,4337
(GPU KV)**, soit un écart **relatif** de 2,1e-5 (2e-4 sur les valeurs affichées) —
reproduit à l'identique par la revue adverse. En revanche, les jetons GÉNÉRÉS
… [271 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"4731\\|4 731\" /tmp --include=\"*.log\" --include=\"*.out\" --include=\"*.txt\" 2>/dev/null | head; echo \"=== aig_s6.sh ===\"; cat /tmp/aig_s6.sh; echo \"=== aig_s6b.sh ===\"; cat /tmp/aig_s6b.sh", "description": "Find sprint 6 raw logs"}`

  ```
/tmp/aiguille_s6b.log
/tmp/aiguille_s6.log
/tmp/rev_ids_100.txt
/tmp/ids_qwen_long.txt
/tmp/ids_qwen3.txt
/tmp/neurones_qwen.txt
/tmp/ids_refontee.txt
/tmp/ids_qwen_512.txt
/tmp/ids_qwen_v2.txt
/tmp/v_q.txt
=== aig_s6.sh ===
#!/bin/bash
# SPRINT 6 — le TAUX, pas le verdict.
#
# 1) Neuf fenêtres contiguës (l'outil avance d'un « besoin » de sonde à chaque
#    fois, donc non recouvrantes) à 4 096 clés, profondeur 0,5, trois chemins :
#    complète, k=256, k=1024. Avec `--gpu-kv` : une sonde tombe de ~250 s à 76 s,
#    ce qui rend les 27 sondes possibles dans un box. Toutes les configurations
#    partagent ce chemin, donc la comparaison reste interne et valable.
# 2) Le point 16 384 (deux fenêtres, trois chemins) pour un troisième point de la
#    courbe k(contexte).
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
M=models/Qwen2.5-0.5B-Q8_0.gguf
J=/tmp/aiguille_s6.log
: > "$J"
NEUF="0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5"
DEUX="0.5,0.5"
serie() {
  local nom=$1 ctx=$2 profs=$3; shift 3
  echo "########## $nom" >> "$J"
  timeout 7200 python3 tools/aiguille.py $M "$ctx" "$profs" --n 24 --lot 256 --gpu-kv "$@" 2>&1 \
    | grep --line-buffered -E "^ +[0-9]+ |fenêtres distinctes|
… [1546 caractères tronqués]
  ```

- **bash** `{"command": "echo \"=== s6b ===\"; cat /tmp/aiguille_s6b.log; echo; echo \"=== s6 (tail 40) ===\"; tail -40 /tmp/aiguille_s6.log", "description": "Read sprint 6 raw aiguille logs"}`

  ```
=== s6b ===
########## A - 4096 - complete - 9 fenetres
     4096        0.50     oui      76.1  prompt 4114 jetons
     4096        0.50     oui      73.6  prompt 3996 jetons
     4096        0.50     NON      85.1  prompt 4731 jetons
     4096        0.50     oui      82.6  prompt 4664 jetons
     4096        0.50     oui      74.2  prompt 4096 jetons
     4096        0.50     oui      73.6  prompt 4046 jetons
     4096        0.50     oui      74.4  prompt 4152 jetons
     4096        0.50     oui      72.7  prompt 4013 jetons
     4096        0.50     oui      74.3  prompt 4081 jetons
fenêtres distinctes utilisées : 9 sur 9 sondes
########## A - 4096 - k=256 GPU - 9 fenetres
     4096        0.50     NON     246.5  prompt 4114 jetons · [attention] --attn-topk 256 est IGNORÉ en mode lot (--lot 256) : l'attention par lots est DENSE. Utiliser --lo

=== s6 (tail 40) ===
########## A - 4096 - complete - 9 fenetres
     4096        0.50     oui      73.4  prompt 4114 jetons
     4096        0.50     oui      74.2  prompt 3996 jetons
     4096        0.50     NON      85.7  prompt 4731 jetons
     4096        0.50     oui      83.9  prompt 4664 jetons
     4096        0.50     oui    
… [700 caractères tronqués]
  ```

- **bash** `{"command": "echo \"=== FULL s6.log ===\"; cat /tmp/aiguille_s6.log; echo; echo \"=== line count ===\"; wc -l /tmp/aiguille_s6.log /tmp/aiguille_s6b.log", "description": "Read full s6 log"}`

  ```
=== FULL s6.log ===
########## A - 4096 - complete - 9 fenetres
     4096        0.50     oui      73.4  prompt 4114 jetons
     4096        0.50     oui      74.2  prompt 3996 jetons
     4096        0.50     NON      85.7  prompt 4731 jetons
     4096        0.50     oui      83.9  prompt 4664 jetons
     4096        0.50     oui      72.9  prompt 4096 jetons
     4096        0.50     oui      72.8  prompt 4046 jetons
     4096        0.50     oui      74.9  prompt 4152 jetons
     4096        0.50     oui      72.9  prompt 4013 jetons
     4096        0.50     oui      72.7  prompt 4081 jetons
fenêtres distinctes utilisées : 9 sur 9 sondes
########## A - 4096 - k=256 - 9 fenetres
     4096        0.50     NON     243.1  prompt 4114 jetons · [attention] --attn-topk 256 est IGNORÉ en mode lot (--lot 256) : l'attention par lots est DENSE. Utiliser --lo
     4096        0.50     oui     230.4  prompt 3996 jetons · [attention] --attn-topk 256 est IGNORÉ en mode lot (--lot 256) : l'attention par lots est DENSE. Utiliser --lo

=== line count ===
  14 /tmp/aiguille_s6.log
  13 /tmp/aiguille_s6b.log
  27 total
  ```

### 🤖 Assistant

⏵ Reading logits comparison report for dense/MoE claims

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-logits-gpu-vs-cpu.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-logits-gpu-vs-cpu.md</path>
<type>file</type>
<content>
1: # Rapport — pourquoi le déport des projections change (ou non) la perplexité
2: 
3: **En une ligne** : sur un modèle **dense**, le déport des projections donne des
4: logits **identiques** au CPU (écart moyen 0,0000, fichiers bit à bit égaux) ; sur un
5: **MoE**, il les décale de **0,038 nat** en moyenne — **497 jetons sur 511 gardent le
6: même top-1** (14 divergent), et cela suffit à déplacer la perplexité de 1,2 %. L'hypothèse la plus simple, fortement étayée par ce contraste, est que de
7: minuscules écarts numériques **changent le routage des experts** (top-8 sur 128).
8: 
9: ## Le doute, et d'où il vient
10: 
11: Au sprint 2, gpt-oss-120b MXFP4 à `--ctx 1024`, 511 jetons :
12: 
13: | chemin | perplexité | écart vs CPU |
14: |---|---|---|
15: | CPU | 18,5803 | — |
16: | GPU, miroir KV seul (`DRAVE_GPU_KV`) | 18,3074 | −1,47 % |
17: | GPU, projections seules (`DRAVE_GPU`) | 18,3538 | −1,22 % |
18: 
19: Ajouter le miroir KV aux projections ne pèse que **0,25 % de plus** : l'essentiel
20: (1,22 %) vient du déport des **projections** lui-même. Or les noy
… [4212 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying sprint 7 claims, six artifacts, and commit messages

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== grep chaine appels ===\"; grep -rn \"chaîne d'appels\\|chaine d'appels\\|ne suit pas la chaîne\" sprints/ reports/*.md | head -10; echo \"=== section annoncée ===\"; grep -rn \"section annoncée\\|annoncée dans un commit\"  … [87 caractères tronqués]`

  ```
=== grep chaine appels ===
sprints/03-qualit-de-l-attention-creuse-long-contex.md:13:  - `d29e043` Correction : `--infer` n'ignore PAS `--lot` (mon grep ne suivait pas la chaîne d'appels)
sprints/03-qualit-de-l-attention-creuse-long-contex.md:90:chaîne d'appels. La règle qui manquait : **vérifier dans le code APPELÉ, pas dans
sprints/05-refaire-la-grille-avec-de-vraies-fenetres.md:97:  chaîne d'appels, le décalage de fenêtre). Chaque fois, la vérification a coûté
sprints/06-le-taux-de-recuperation.md:81:  global, grep qui ne suit pas la chaîne d'appels, décalage de fenêtre remis à zéro,
reports/rapport-aiguille-topk.md:42:chaîne d'appels. La vérification se fait dans le code appelé, pas dans l'appelant.
=== section annoncée ===
sprints/06-le-taux-de-recuperation.md:82:  section annoncée dans un commit mais absente du rapport, et un moteur qui ralentit
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 312 s ===\"; grep -rn \"312\" sprints/07-cloture-de-la-nuit.md REPRISE.md 2>/dev/null; grep -rln \"312\" /tmp/*.log /tmp/*.out 2>/dev/null | head; echo \"=== 4788 ===\"; grep -rn \"4788\\|4 788\\|180 premiers\" --include=\ … [244 caractères tronqués]`

  ```
=== 312 s ===
REPRISE.md:520:premiers sont ABANDONNÉS »). Vérifié : la même invite rend la main en 312 s au lieu
/tmp/draft-8083.log
/tmp/full-chat.log
/tmp/go-8072.log
/tmp/llama-codestral-8000.log
/tmp/rsync-models.log
/tmp/s_cumul.log
/tmp/serveur_v1.log
/tmp/syn_dsp0.log
/tmp/syn_dsp1.log
/tmp/syn_eng.log
=== 4788 ===
./reports/rapport-aiguille-topk.md:262:« `[contexte] invite de 4788 jetons > ctx 4608 : les 180 premiers sont ABANDONNÉS
./REPRISE.md:519:**tronque l'invite en le disant** (« invite de 4788 jetons > ctx 4608 : les 180
=== model.rs line 1117 old ===
        c.assurer(ctx.min(1024));
        c
    }

    /// Garantit `besoin` positions allouées (doublement, avec recopie : les
    /// positions déjà écrites le restent). Chaque tête KV a son bloc contigu,
    /// donc la recopie se fait tête par tête.
    pub fn assurer(&mut self, besoin: usize) {
        if besoin <= self.cap { return; }
        let mut cap = self.cap.max(1);
        while cap < besoin { cap = (cap * 2).min(self.ctx); }
        let hd = self.hd;
        let nb = self.nb;
        let pas = self.pas();
        let (n_kv, bits) = (self.n_kv, self.bits);
        let f32_k = bits >= 32 || self.k_f32;
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '230,300p' reports/rapport-aiguille-topk.md", "description": "Read report sprint 7 section"}`

  ```
* **8 192 : mesuré depuis** (dense, k = 1 024, k = 2 048 — une fenêtre chacun,
  section précédente). **16 384 n'est pas mesuré** : le taux du 0.5B est de 58 à
  62 ms par jeton de prompt, soit ≈20 min par sonde à 16 384.
* plusieurs codes par sonde, **plusieurs fenêtres de corpus** : la mesure est
  binaire (trouvé / non trouvé), avec un seul code et — la correction ci-dessus le
  montre — **une seule fenêtre par (contexte, profondeur)**. Un « NON » peut être un
  échec de génération ; le détail (« oui » dense au même endroit) protège de cette
  lecture, mais la généralité inter-fenêtres n'est pas mesurée.
* **un seul modèle** (Qwen2.5-0.5B) : rien ne dit que le seuil k/contexte soit le
  même sur un modèle plus grand.
* le TAUX de récupération par fenêtre reste partiel : 9 fenêtres mesurées en
  attention complète (8 réussites), 1 seule en `k = 256` (échec) — la série
  complète demande le top-k dans le chemin par lots (246 s par sonde sans lui).

### Un piège du MOTEUR, trouvé parce qu'une sonde a duré 23 minutes

La fenêtre 3 tokenise à **4 731 jetons** là où la cible était 4 096, et l'outil
passait `--ctx 4608` : le prompt dépassait le contexte. Le moteur ne l'a pas refusé
— i
… [2404 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"4788\\|ABANDONNÉS\\|abandonnes\\|abandonnés\" /tmp/*.log /tmp/*.out /tmp/*.txt 2>/dev/null | head; echo \"=== recent tmp logs 05:00+ ===\"; ls -la --time-style=+%m-%d_%H:%M /tmp/*.log /tmp/*.out 2>/dev/null | awk '$6 >= \"10-01_05:00\"' | head -20", "description": "Find trun … [25 caractères tronqués]`

  ```
/tmp/integ2.out
/tmp/integ.out
/tmp/prep.out
/tmp/dis.txt
/tmp/ids_qwen3.txt
/tmp/ids_qwen_long.txt
/tmp/ids_qwen.txt
/tmp/ids_qwen_v2.txt
/tmp/ids_refontee.txt
/tmp/neurones_qwen.txt
=== recent tmp logs 05:00+ ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"312 s\\|312s\\|rend la main en 312\" journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md | tail -10; echo \"=== integ2/prep ===\"; for f in /tmp/integ2.out /tmp/integ.out /tmp/prep.out; do echo \"--- $f\"; ls -l … [137 caractères tronqués]`

  ```
=== integ2/prep ===
--- /tmp/integ2.out
-rw-r--r--. 1 stephane stephane 5376 09-21_16:46 /tmp/integ2.out
9:  référence : a57468cd0b66d1e478888dd351ba4f22cbd0b04bc074038ccf533f6285bfa889
10:  maintenant: a57468cd0b66d1e478888dd351ba4f22cbd0b04bc074038ccf533f6285bfa889
--- /tmp/integ.out
-rw-r--r--. 1 stephane stephane 4702 09-21_16:45 /tmp/integ.out
10:  maintenant: a57468cd0b66d1e478888dd351ba4f22cbd0b04bc074038ccf533f6285bfa889
--- /tmp/prep.out
-rw-r--r--. 1 stephane stephane 11673 09-21_16:25 /tmp/prep.out
42:     a57468cd0b66d1e478888dd351ba4f22cbd0b04bc074038ccf533f6285bfa889  -
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"contexte\\] invite\\|ABANDONN\" journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md | tail -10", "description": "Find truncation message in journal"}`

  ```
39900:3932 | ABANDONNÉS (troncature, pas de fenêtrage)", ids.len(), self.cfg.ctx, coupe);
39990:troncature : [contexte] invite de 4788 jetons > ctx 4608 : les 180 premiers sont ABANDONNÉS (troncature, pas de fenêtrage)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '39970,40010p' journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md", "description": "Read journal around truncation verification"}`

  ```
let ecoute = TcpListener::bind("127.0.0.1:0").unwrap();
        let adresse = ecoute.local_addr().unwrap();
        let serveur = std::thread::spawn(move || {
            let (mut sock, _) = ecoute.accept().unwrap();
            // en-tête v4 complet, mode lot, n = 100 millions d'états
            let mut tete: Vec<u8> = Vec::new();
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\np='drave-core/src/main.rs'; s=open(p).read()\nancre = \"\"\"    #[test]\n    fn un_nombre_de_blocs_dement_grand_est_refuse() {\"\"\"\nneuf = \"\"\"    /// Le livelock du contexte : `KvCache::assurer(besoin)` avec `b … [877 caractères tronqués]`

  ```
test ajouté

test result: ok. 18 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.11s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 400 python3 - <<'PY'\nimport subprocess, time, re\nfen = open('/tmp/fen_2.txt').read()   # fenêtre 3 : 4731 jetons\ninvite = fen + \"\\n\\nQuel est le code de verification de la reunion ? Reponds par le code seul, puis une ph … [787 caractères tronqués]`

  ```
durée 312.5 s · prompt 4788 jetons
troncature
… [1461 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"absente du rapport\\|annoncée\\|annoncé dans un commit\" journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md | tail -6; echo \"=== 16384 report ===\"; grep -n \"16 384\" reports/rapport-aiguille-topk.md | head  … [60 caractères tronqués]`

  ```
38680:   (d) FAUX. Les « 3/3 » et « 0/3 » sont trois répétitions de la MÊME invite (même texte, même position d'aiguille), pas trois textes. La justification annoncée (« avec une seule sonde, impossible de distinguer "l'attention creuse échoue" de "cette exécution a déraillé" ») n'est donc pas servie : les trois sondes ne peuvent rien dire de la généralité inter-fenêtres.
38725:- Premier balayage : k=512 NON (274,8 s), k=1024 oui (241,8 s) ⇒ la non-monotonie annoncée est bien dans /tmp/aiguille_k.log ; concordance avec les répétitions.
38750:- **(d)** **FAUX.** Les « 3/3 » et « 0/3 » sont trois répétitions de la **même invite**. La justification annoncée (« avec une seule sonde, impossible de distinguer *l'attention creuse échoue* de *cette exécution a déraillé* ») n'est pas servie : trois fois la même invite ne dit rien de la généralité inter-fenêtres.
38831:- Premier balayage : k=512 NON (274,8 s), k=1024 oui (241,8 s) → la non-monotonie annoncée est bien dans `/tmp/aiguille_k.log` ; les 3 nouvelles sondes **concordent** avec elle (k=512 : 4/4 NON ; k=1024 : 4/4 oui).
39247:**La cinquième artefact-trust error est donc l'écart 1** (une mesure annoncée dans un message de commit, ab
… [531 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for c in b3cba4c c7fd7ea 32951e9 3209dc5 45a0c44; do echo \"########## $c\"; git show --stat --format='%s%n%n%b' $c | head -40; done", "description": "Show last five commit messages and stats"}`

  ```
########## b3cba4c
README et REPRISE : prochaines étapes et compteur de lignes après la nuit

Les « prochaines étapes » disent maintenant ce que la nuit a établi : le top-k
déporté fonctionne (plate, croisement ~300 clés) mais PAS dans le préremplissage
(le chemin par lots ignore --attn-topk, 246 s par sonde au lieu de 75), et la
qualité de l'attention creuse se mesure en TAUX (k = 256 : 2 fenêtres sur 3), ce qui
demande ce même chantier pour être mesurée à moindre coût.

Compteur de lignes Rust : 13 758 (mesuré), dans README ×2 et REPRISE. Portes :
19,3885 · 15,1757 · **18 tests**.


 README.md                                          | 36 +++++++++++++---------
 REPRISE.md                                         |  2 +-
 journal/README.md                                  |  2 +-
 journal/sessions/MANIFEST.md                       |  2 +-
 .../bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md | 33 ++++++++++++++++++++
 .../rapport.md                                     | 17 +++++-----
 6 files changed, 66 insertions(+), 26 deletions(-)
########## c7fd7ea
REPRISE : le livelock corrigé, et le bilan des six résultats de la nuit



 REPRISE.md                                         | 26
… [3199 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --format='%s%n%n%b' 783f1f9 | head -30; echo \"=== ecart1 in journal ===\"; sed -n '39200,39250p' journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md", "description": "Check commit 783f1f9 and sixth artifa … [11 caractères tronqués]`

  ```
Sprint 6 : le taux de récupération (9 fenêtres × 3 chemins) et le point 16 384



 journal/README.md                                  |  2 +-
 journal/sessions/MANIFEST.md                       |  4 +-
 .../bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md | 48 ++++++++++++++++++++++
 .../rapport.md                                     | 15 +++----
 sprints/06-le-taux-de-recuperation.md              |  6 +++
 sprints/COURANT                                    |  1 +
 6 files changed, 66 insertions(+), 10 deletions(-)
=== ecart1 in journal ===

## Écart 3 — [MODÉRÉ, latent] `tools/aiguille.py` : le garde-fou d'offset est mal calibré à son tour

**(a)** `tools/aiguille.py` l.161-174 (boucle + garde), l.63-64 (garde interne de `sonde`), docstring l.12-13.

**(b)** La docstring promet « Chaque sonde prend … une FENÊTRE DIFFÉRENTE du corpus » ; le garde compare `offset + 20_000 > len(corpus)`, alors que le besoin réel est `besoin = int(ctx*4.2) + 400`.

**(c)** Calculs + exécution réelle de `main()` avec une sonde factice (sans lancer le moteur) :
- corpus réel **353 778**, 3 profondeurs → offsets **0 / 150 000 / 300 000**, fenêtres disjointes (0-17 603, 150 000-167 603, 300 000-317 603) : 
… [5364 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking sprint attribution of the GPU kv_assurer fix and line counter

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== sprint1 note ===\"; cat sprints/01-premier-des-trois-noyaux-gpu-du-top-k-le.md | head -60; echo \"=== kv_assurer ===\"; grep -rn \"kv_assurer\" sprints/*.md reports/*.md | head -20", "description": "Check sprint 1 note and … [24 caractères tronqués]`

  ```
=== sprint1 note ===
# Sprint 1 — Premier des trois noyaux GPU du top-k : les scores d'attention calculés en VRAM, vérifiés contre la référence CPU à 1e-6, avec leur banc

- **Début** : 17:41 · **Fin prévue** : 19:41 (boxing de 120 min)
- **Objectif** : Premier des trois noyaux GPU du top-k : les scores d'attention calculés en VRAM, vérifiés contre la référence CPU à 1e-6, avec leur banc
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.


## Revue — ce qui est livré, mesuré

Durée : 120 min (boxing 120 min). Commits : 20.

  - `03243f7` Compteur de lignes Rust re-mesuré en fin de sprint : 13 480 (le chiffre avait bougé de 312 lignes pendant le sprint)
  - `22d3004` --options-actives dit si le top-k déporté s'applique, et pourquoi sinon
  - `e49f3bb` Rapport : l'étape 5 est faite, et la ligne de l'étape 4 dit la bonne variable (clés vues, pas contexte)
  - `c1fdfd4` Rapport et plan : 14 noyaux et 956 lignes (le noyau 3 est arrivé après le comptage), ordre réel de la collecte
  - `dada69a` Journal : index des sessions régénéré
  - `b8d4fa5` Correction d'interprétation : les clés notées dépendent du nombre de JETONS, pas du contexte — le croisement e
… [5158 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"13 758\\|13758\" README.md REPRISE.md journal/README.md 2>/dev/null; echo \"=== dirty diff ===\"; git diff --stat; git diff journal/README.md | head -30", "description": "Check line counter and dirty working tree"}`

  ```
README.md:299:le moteur tenait en 386 lignes à ses débuts ; il en fait 13 758 aujourd'hui). Détail complet :
README.md:373:BLAS, sans aucune dépendance : **13 758 lignes de Rust, `std` seul** au 01/10 au matin (2 319 au premier prototype). Détail :
REPRISE.md:16:`drave-core` est un moteur d'inférence Rust (~13 758 lignes, `std` seul) qui
=== dirty diff ===
 journal/README.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
diff --git a/journal/README.md b/journal/README.md
index 1b13499..a9f3d34 100644
--- a/journal/README.md
+++ b/journal/README.md
@@ -22,7 +22,7 @@ de la session ; le `digest.md` voisin en donne le verbatim complet.
 | `7d0d2578` | Tu travailles dans le dépôt | 2026-09-30 11:47 | 0.1 h | 1 | 53 | 1 | 0 | [rapport](sessions/7d0d2578-0048-4998-8494-7d2daef56769/rapport.md) |
 | `8e04c99a` | Tu es VÉRIFICATEUR de documentation | 2026-09-30 18:07 | 0.2 h | 1 | 85 | 0 | 0 | [rapport](sessions/8e04c99a-8ba1-4675-9f80-fa3338449b17/rapport.md) |
 | `aa5f9fc5` | Tu es vérificateur de documentation | 2026-09-30 15:07 | 0.2 h | 1 | 100 | 1 | 0 | [rapport](sessions/aa5f9fc5-9450-4118-b65f-e8b99a28519d/rapport.md) |
-| `bbd6969f` | Continue avec REPRISE.md | 2026-09-28 14
… [761 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn kv_assurer\" -A 20 drave-core/src/gpu.rs | head -30; echo \"=== history of kv_assurer loop ===\"; git log --oneline -S \"kv_assurer\" -- drave-core/src/gpu.rs | head -10", "description": "Inspect kv_assurer and its histo … [4 caractères tronqués]`

  ```
440:    pub fn kv_assurer(&self, m: &mut KvGpu, besoin: usize) -> bool {
441-        cu_ctx(self.ctx);
442-        if besoin <= m.capacite { return true; }
443-        // Sans ce garde, `cap` plafonne à `m.ctx` et la boucle de doublement ne
444-        // termine jamais : un appelant qui demande plus que le contexte déclaré
445-        // pendait le processus au lieu de recevoir `false`.
446-        if besoin > m.ctx { return false; }
447-        let mut cap = m.capacite.max(1);
448-        while cap < besoin { cap = (cap * 2).min(m.ctx); }
449-        let pas = match m.bits { 32 => m.hd * 4, 8 => m.hd, 4 => m.hd / 2, _ => return false };
450-        let donnees = m.n_kv * cap * pas;
451-        let echelles = if m.bits >= 32 { 0 } else { m.n_kv * cap * m.nb * 4 };
452-        let total = donnees * 2 + echelles * 2;
453-        if total > self.memoire_libre { return false; }
454-        unsafe {
455-            let (mut k, mut v, mut sk, mut sv) = (0u64, 0u64, 0u64, 0u64);
456-            if cuMemAlloc_v2(&mut k, donnees) != 0 { return false; }
457-            if cuMemAlloc_v2(&mut v, donnees) != 0 { cuMemFree_v2(k); return false; }
458-            // Échec d'allocation des échelle
… [301 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --format='%h %ad %s' --date=format:'%m-%d %H:%M' -S \"besoin > m.ctx\" -- drave-core/src/gpu.rs | head; echo \"=== guard in old versions ===\"; git log --format='%h %ad %s' --date=format:'%m-%d %H:%M' --since=\"2026-09-30 00: … [88 caractères tronqués]`

  ```
47ce9b7 09-30 18:16 Relecture adversariale : 7 défauts corrigés, dont un bloquant sur les chemins d'échec
=== guard in old versions ===
ed4ce47 09-30 20:17 Revue adverse du noyau fusionné : une course bloquante, et cinq autres points
8342f17 09-30 20:03 Noyau 4 : le top-k complet d'une ligne en UN lancement (8 lancements → 2)
64c9d26 09-30 19:00 Top-k déporté : une synchro en trop, un budget de scores, un échec dit une seule fois
abcfab7 09-30 18:59 Relecture du branchement : un faux résultat silencieux dans attn_kv_recombine, et le top-k gagne à 16 k
d221ead 09-30 18:36 Étape 4 : le top-k déporté tourne dans le moteur (opt-in), et l'étape 5 est chiffrée
674a334 09-30 18:22 Noyau 3 : softmax sur les k retenus + Σ w·V, écart 1,0 à 4,8e-7
47ce9b7 09-30 18:16 Relecture adversariale : 7 défauts corrigés, dont un bloquant sur les chemins d'échec
fa6a4f3 09-30 18:12 Collecte top-k : réallouer quand k GRANDIT, et un banc qui le prouve
e950075 09-30 18:07 Noyaux 2b : collecte des k indices — même ensemble que le CPU, 896× le tri à 262 k clés
d00c01c 09-30 17:52 Noyau 2a du top-k GPU : histogramme d'octet, seuil exact sur 14/14 lignes
5e8bf48 09-30 17:46 Sprint 1 : noyau GPU de scores d'att
… [126 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying the Rust line counter and the GPU guard diff

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 47ce9b7 --stat | head -20; echo \"=== diff gpu guard ===\"; git show 47ce9b7 -- drave-core/src/gpu.rs | grep -n \"besoin > m.ctx\" -B 8 -A 4 | head -30", "description": "Inspect commit that added GPU guard"}`

  ```
commit 47ce9b7adb473edda8222e8094a22495da37e19b
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 18:16:49 2026 -0400

    Relecture adversariale : 7 défauts corrigés, dont un bloquant sur les chemins d'échec
    
    Un relecteur adversarial a relu les quatre noyaux et leur FFI. Presque tout a été
    trouvé en LISANT, pas en mesurant — et aucun des sept n'était visible au banc.
    
    1. BLOQUANT (gpu.rs, collecte) : le garde de réallocation était piloté par le
       triplet (lignes, tranches, k). Un `vram_assurer` qui échouait au milieu du
       `||` libérait son tampon et mettait sa capacité à zéro, mais les dimensions
       enregistrées restaient INCHANGÉES : l'appel suivant, plus petit, sautait la
       réallocation et passait un pointeur 0 au noyau (contexte CUDA empoisonné).
       Le garde est maintenant piloté par les CAPACITÉS : chaque échec est
       auto-réparateur.
    2. GRAVE : `kv_assurer` fuyait k et v (et sk) quand l'allocation des échelles
       échouait — ~1 Go de VRAM perdu, et une fuite de plus à chaque tentative.
    3. MODÉRÉ : `scores_cap` / `histo_cap` / `prefixes_cap` n'étaient remis à zéro
       qu'APRÈS une allocation réussie ; après un
… [807 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && find drave-core/src -name '*.rs' | xargs wc -l | tail -3; echo \"=== total all rs in repo ===\"; find . -name '*.rs' -not -path './target/*' | xargs wc -l 2>/dev/null | tail -1", "description": "Count Rust lines"}`

  ```
4111 drave-core/src/model.rs
  1573 drave-core/src/gpu.rs
 13758 total
=== total all rs in repo ===
 13758 total
  ```

### 🤖 Assistant

⏵ Independently checking the livelock fix and its callers

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 32951e9 -- drave-core/src/model.rs drave-core/src/main.rs", "description": "Show livelock fix diff"}`

  ```
commit 32951e958ce8e6c941a1b3b4266e4f358c937667
Author: Stéphane <stephane@localhost>
Date:   Thu Oct 1 05:46:06 2026 -0400

    Le livelock du contexte est corrigé : troncature annoncée au lieu d'une boucle infinie
    
    `KvCache::assurer` bouclait sans fin dès que `besoin > ctx` (`while cap < besoin {
    cap = (cap * 2).min(self.ctx) }` : `cap` plafonne et la condition reste vraie). Le
    même défaut avait été corrigé côté GPU au sprint 2 (`kv_assurer`) ; le chemin CPU
    était resté, et une invite de 4 788 jetons avec `--ctx 4608` tournait à ~1 700 % de
    CPU pendant plus de 22 minutes sans finir.
    
    Deux corrections :
    - `assurer` plafonne la capacité au contexte déclaré — la boucle termine toujours ;
    - `Model::generate` tronque l'invite en le DISANT : « [contexte] invite de 4788
      jetons > ctx 4608 : les 180 premiers sont ABANDONNÉS (troncature, pas de
      fenêtrage) ».
    
    Vérifié : la même invite rend la main en 312 s (coût normal du chemin CPU, sans
    --gpu-kv) au lieu de ne jamais finir. Test de non-régression ajouté — `assurer(1000)`
    sur un cache de 16 positions doit rendre la main : **18 tests** au lieu de 17, et
    c'est un test qu
… [3289 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"\\.assurer(\\|fn assurer\" drave-core/src/*.rs | head -20; echo \"=== KvCache::new signature ===\"; grep -n \"impl KvCache\" -A 26 drave-core/src/model.rs | head -40", "description": "Find assurer callers and KvCache::new" … [1 caractères tronqués]`

  ```
drave-core/src/main.rs:4374:    fn assurer_ne_boucle_pas_au_dela_du_contexte() {
drave-core/src/main.rs:4376:        c.assurer(1000);          // 1000 >> 16 : la boucle doit se terminer
drave-core/src/main.rs:4378:        c.assurer(8);
drave-core/src/model.rs:1110:        c.assurer(ctx.min(1024));
drave-core/src/model.rs:1117:    pub fn assurer(&mut self, besoin: usize) {
drave-core/src/model.rs:1210:        if pos + 1 > self.cap { self.assurer(pos + 1); }
=== KvCache::new signature ===
1094:impl KvCache {
1095-    pub fn new(bits: u32, n_kv: usize, ctx: usize, hd: usize) -> Self {
1096-        let bits = if bits >= 32 { 32 } else if bits > 4 { 8 } else { 4 };
1097-        if bits < 32 {
1098-            assert!(hd % 2 == 0, "4 bits empaquetés : dimension de tête paire requise");
1099-        }
1100-        let nb = hd.div_ceil(32).max(1);
1101-        let (k_f32, v_f32) = (std::env::var("DRAVE_KV_K_F32").is_ok(),
1102-                              std::env::var("DRAVE_KV_V_F32").is_ok());
1103-        let k_f16 = bits < 32 && std::env::var("DRAVE_KV_K_F16").is_ok();
1104-        let mut c = KvCache { bits, n_kv, ctx, cap: 0, hd,
1105-                              f16_avant: std::e
… [869 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1195,1240p' drave-core/src/model.rs", "description": "Read KV cache write path"}`

  ```
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
        if pos + 1 > self.cap { self.assurer(pos + 1); }
        let d = (kvh * self.cap + pos) * self.hd;
        if self.bits >= 32 {
            self.kf[d..d + self.hd].copy_from_slice(&k[..self.hd]);
            self.vf[d..d + self.hd].copy_from_slice(&v[..self.hd]);
            return;
        }
        let niv = if self.bits == 4 { 7.0 } else { 127.0 };
        // `DRAVE_KV_F16=1` : clés et valeurs arrondies en demi-précision avant
        // qua
… [1174 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"forward_lot\\|fn prefill\\|prefill_lot\\|lot > 1\" drave-core/src/model.rs | head -20", "description": "Locate batch prefill path"}`

  ```
922:    /// États imposés pour un LOT entier (`forward_lot`) : `t × hidden`, aplati.
1377:/// Un seul message pour `--attn-topk` ignoré en mode lot (voir `forward_lot`).
2349:    pub fn forward_lot(&mut self, toks: &[u32], pos0: usize) -> Vec<Vec<f32>> {
2861:    /// `forward_lot`, et non à chaque appel — `flux_lot` est appelé deux fois par
2892:                    // garde-fou devenait aveugle dès `--lot > 1`, et une trace
3083:        // perplexité répartie 798,3 au lieu de 18,2. `forward_lot` et
3938:        // Préremplissage par lots : `forward_lot` sur des tranches de `self.lot`
3939:        // jetons. `lot == 1` reprend exactement l'ancienne boucle (forward_lot
3948:                let hs = self.forward_lot(&ids[pos..pos + t], pos);
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3913,4010p' drave-core/src/model.rs", "description": "Read generate loop after fix"}`

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
        // Invite plus longue que le contexte : on garde les DERNIERS jetons (le
        // début d'un long document est ce qu'on peut perdre avec le moins de
        // dégâts) et on le DIT. Sans ce garde, `KvCache::assurer` bouclait sans
        // fin — un hang, pas une erreur — et rien ne l'annonçait.
        let ctx_modele = self.ctx;
        let ids = if ids.len() > ctx_modele {
            let coupe = ids.len() - ctx_modele;
            println!("[contexte] invite de {} jetons > ctx {} : les {} premiers sont \
ABANDONNÉS (troncature, pas de fenêtrage)", ids.len(), ctx_modele, coupe);
            &ids[c
… [3405 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/Game 2>/dev/null; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"pub fn forward\\b\\|fn forward(\" drave-core/src/model.rs | head; echo \"=== rotation ===\"; grep -n \"rotation\\|glissant\\|fenetre_glissante\\|self.ctx\" drave-core/sr … [79 caractères tronqués]`

  ```
3024:    pub fn forward(&mut self, tok: u32, pos: usize) -> Vec<f32> {
=== rotation ===
842:    /// Fenêtre d'attention glissante : ne noter que les `attn_window` dernières
1079:    /// que la feuille de route appelle, sans rotation ni échelle par tête.
1126:        let besoin = besoin.min(self.ctx);
1129:        while cap < besoin { cap = (cap * 2).min(self.ctx); }
1417:            // ------------------------------------------------ rotation (RoPE)
1568:        // Le modèle peut déclarer une fenêtre glissante (gpt-oss : 128) : lue
1588:            println!("[config] fenêtre glissante {fenetre} sur {n_fen}/{} couches (motif {swa_pattern}{})",
1592:        // Trace de rotation : le régime choisi ET la raison. Sans elle, un
1598:                println!("[config] rotation : YaRN ×{f}{} (contexte demandé {ctx} > {o} initial)",
1601:                println!("[config] rotation : RoPE simple (contexte {ctx} ≤ {o} initial ; \
1604:                println!("[config] rotation : RoPE simple (YaRN ×{f} refusé, contexte {ctx} > {o})"),
1605:            _ => println!("[config] rotation : RoPE simple (le modèle ne déclare pas YaRN)"),
2263:    /// rotation. La sortie est en plus multipliée par `
… [1112 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2905,2920p' drave-core/src/model.rs; echo \"=== forward head ===\"; sed -n '3018,3030p' drave-core/src/model.rs; echo \"=== forward_lot head ===\"; sed -n '2345,2360p' drave-core/src/model.rs", "description": "Read pos assert … [6 caractères tronqués]`

  ```
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
=== forward head ===
            out[o] = acc;
        }
        out
    }

    /// Un token, une position. Retourne l'état caché après la dernière norme.
    pub fn forward(&mut self, tok: u32, pos: usize) -> Vec<f32> {
        
… [1407 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2360,2400p' drave-core/src/model.rs | grep -n \"assert\\|ctx\" ; echo \"---\"; awk 'NR>=2349 && NR<=2420 && /assert/' drave-core/src/model.rs; echo \"=== all asserts pos ===\"; grep -n \"assert!(pos\" drave-core/src/model.rs" … [54 caractères tronqués]`

  ```
34:        let ctx = self.ctx;
40:                assert_eq!(v.len(), t * h,
---
                assert_eq!(v.len(), t * h,
=== all asserts pos ===
2914:        assert!(pos < self.ctx, "contexte dépassé");
3025:        assert!(pos < self.ctx, "contexte dépassé ({pos} ≥ {})", self.ctx);
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn run_ppl\\|fn ppl\\|--limit\" drave-core/src/main.rs | head -20", "description": "Locate run_ppl in main.rs"}`

  ```
571:            "--limit" => { o.limit = suivant(i).parse().unwrap(); 2 }
2110:fn run_ppl_reparti(opt: Options, pair: &str) {
3222:    // `--limit N` plafonne le nombre de lignes : c'est ce qui permet de
3776:fn run_ppl(opt: Options) {
3843:    // même découpage que celui qui a servi à l'entraîner. `--limit` compte les
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3776,3900p' drave-core/src/main.rs", "description": "Read run_ppl implementation"}`

  ```
fn run_ppl(opt: Options) {
    let montre_options = opt.options_actives;
    let Options {
        ids_file: idfile, texte_file, ppl_texte: _, limit, depuis,
        ctx: ctx_opt, threads: threads_opt, abits: abits_opt,
        ctx_impose, threads_impose, abits_impose,
        dense, auto, q4, b6, attn_window, swa_pattern,
        sans_fenetre, attn_sinks, attn_topk, qk_topk, act_thresh, act_topk, act_renorm,
        topk_proj, moe_topk, patch: patch_file, hebb_layer, hebb_q, hebb_out,
        ffn_gain, logits_bin, keep,
        ppl_profil, lot, profil_neurones, neurones_sortie, trace_flux, trace_couches, flux_forcer,
        harmony, harmony_contexte, sans_yarn, ..
    } = opt;
    let lot = lot.max(1);
    let path = &modele_chemin();
    // Défauts du mode PERPLEXITÉ : 256 jetons, trois quarts des cœurs, 16 bits
    // d'activation (la référence de non-régression en dépend).
    let cpu = std::thread::available_parallelism().map(|n| n.get()).unwrap_or(8);
    let ctx = if ctx_impose { ctx_opt } else { 256 };
    let n_threads = if threads_impose { threads_opt } else { (cpu * 3 / 4).max(1) };
    let abits = if abits_impose { abits_opt } else { 16 };
    let idfile = idfile.unwra
… [5203 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3900,3980p' drave-core/src/main.rs", "description": "Read ppl evaluation loop"}`

  ```
options_actives(&mdl, "perplexité", ctx_impose, dense, keep);
    }
    if let Some(l) = hebb_layer {
        let mut hb = model::Hebb::new(l, mdl.cfg.ffn, mdl.cfg.hidden, hebb_q);
        hb.log_on = true;
        mdl.hebb = Some(hb);
        println!("journalisation : couche {l}, entrée FFN ({} dim)", mdl.cfg.hidden);
    }
    if profil_neurones {
        mdl.activer_profil_neurones();
        println!("profilage des neurones actif : un neurone compte comme actif si sa valeur \
                  quantifiée n'est pas nulle (même critère que le chemin par événements)");
    }
    mdl.reset_events();
    // Fenêtres d'évaluation : soit des tranches brutes de `ctx` jetons (mode
    // historique, toutes notées), soit des tours harmony dont seuls les jetons
    // de contenu sont notés.
    let fenetres: Vec<(Vec<u32>, Vec<bool>)> = match &harmony {
        None => {
            // `--depuis N` : les fenêtres sont ancrées pour que le premier jeton
            // NOTÉ ait un contexte complet (on recule de ctx-1 jetons, qui ne
            // sont pas notés). Sans décalage, le protocole historique est
            // conservé au chiffre près (`chunks`).
            if depuis == 0 {
     
… [2833 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Testing the truncation path for a panic beyond ctx

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '\"--ids\"\\|\"--infer\"\\|\"--prompt\"\\|\"--n\"\\|\"--ctx\"' drave-core/src/main.rs | head -12; echo \"=== usage ===\"; ./drave-core/target/release/drave --help 2>&1 | head -30", "description": "Check CLI flags for inferenc … [3 caractères tronqués]`

  ```
57:        (opt.ppl, "--ppl"), (opt.infer, "--infer"),
528:            "--infer" => { o.infer = true; 1 }
549:            "--ids" => { o.ids = suivant(i).split(',')
552:            "--prompt" => { o.prompt = Some(suivant(i).clone()); 2 }
561:            "--n" => { o.n = suivant(i).parse().unwrap(); 2 }
567:            "--ctx" => { o.ctx = suivant(i).parse().unwrap(); o.ctx_impose = true; 2 }
=== usage ===
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.

thread 'main' (2720913) panicked at src/main.rs:98:30:
ouverture du GGUF: Os { code: 2, kind: NotFound, message: "No such file or directory" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport random\nrandom.seed(1)\nids=[random.randrange(0,150000) for _ in range(300)]\nopen('/tmp/rev_ids_300.txt','w').write(','.join(map(str,ids)))\nprint('ok')\" && timeout 300 ./drave-core/target/release/drave ./mode … [219 caractères tronqués]`

  ```
ok
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
[config] cache KV : 32 bits, 0.01 Go pour 256 jetons
[modele] 24 couches chargées en 821.708136ms — listes 0.00 Go , 8 threads
[config] 24 couches, hidden 896 · 
[config] puits appris sur 0/24 couches · n_rot 64 · ffn 4864 · experts 0
[config] rotation : RoPE simple (le modèle ne déclare pas YaRN)
Qwen2 · 24 couches · hidden 896 · 14 têtes / 2 KV · FFN 4864 · vocab 151936
[contexte] invite de 300 jetons > ctx 256 : les 44 premiers sont ABANDONNÉS (troncature, pas de fenêtrage)

thread 'main' (2721019) panicked at src/model.rs:3025:9:
contexte dépassé (256 ≥ 256)
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
timeout: the monitored command dumped core
[exit 134]
  ```

### 🤖 Assistant

⏵ Finding confirms a residual panic; now checking all cache-write callers

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"\\.forward(\\|\\.forward_lot(\\|\\.forward_mla(\\|\\.ecrire(\" drave-core/src/*.rs | grep -v \"^drave-core/src/model.rs:.*fn \\|assert\" | head -30", "description": "List forward and ecrire call sites"}`

  ```
drave-core/src/main.rs:886:        for (pos, &t) in ids.iter().enumerate() { last = mdl.forward(t, pos); }
drave-core/src/main.rs:897:            last = mdl.forward(next, ids.len() + step);
drave-core/src/main.rs:1344:            let hn = mdl.forward(0, 0);
drave-core/src/main.rs:2060:                    let hs = mdl.forward_lot(&vec![0u32; t], f.pos as usize);
drave-core/src/main.rs:2076:                let sortie = mdl.forward(0, f.pos as usize);
drave-core/src/main.rs:2153:            let hs = mdl.forward_lot(&ids[pos..pos + t], pos);
drave-core/src/main.rs:2164:            let last = mdl.forward(t, pos);
drave-core/src/main.rs:2198:            let hs = mdl.forward_lot(&ids[pos..pos + t], pos);
drave-core/src/main.rs:2276:        let etat = mdl.forward(t, pos);
drave-core/src/main.rs:2395:            cache.ecrire(kvh, pos, &kp, &vp);
drave-core/src/main.rs:2960:        let hn = mdl.forward_mla(t, pos);
drave-core/src/main.rs:3036:            cache.ecrire(kvh, pos, &k, &v);
drave-core/src/main.rs:3997:            let hs = mdl.forward_lot(&chunk[pos..pos + t], pos);
drave-core/src/model.rs:2380:            return vec![self.forward(toks.first().copied().unwrap_or(0), pos0)];
drave-
… [929 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"ctx\" drave-core/src/model.rs | sed -n '1,20p'; echo \"=== model ctx field ===\"; grep -n \"pub ctx\\|ctx: usize\" drave-core/src/model.rs | head", "description": "Check Model ctx field semantics"}`

  ```
458:/// PAS `(n_kv, ctx, head_dim)` mais **une seule tête latente** par couche —
803:    /// cache KV, par couche : `[n_kv_head × ctx × head_dim]`, en f32 ou quantifié
808:    pub ctx: usize,
1058:    pub ctx: usize,
1067:    /// Positions réellement allouées, doublées à la demande. Réserver `ctx`
1095:    pub fn new(bits: u32, n_kv: usize, ctx: usize, hd: usize) -> Self {
1104:        let mut c = KvCache { bits, n_kv, ctx, cap: 0, hd,
1110:        c.assurer(ctx.min(1024));
1119:        // ⚠️ `besoin > ctx` faisait BOUCLER SANS FIN : `cap` plafonne à `ctx` et la
1121:        // `--ctx 4608` tournait à ~1 700 % de CPU pendant plus de 22 minutes sans
1126:        let besoin = besoin.min(self.ctx);
1129:        while cap < besoin { cap = (cap * 2).min(self.ctx); }
1188:    /// réserve, pas ce que `ctx` laisse croire.
1381:    pub fn load(path: &str, ctx: usize, n_threads: usize, dense: bool, keep: f32,
1474:                    Some(y) if !jamais && ctx as f32 > y.3 * 4.0 => Some(y),
1537:            .map(|_| KvCache::new(kv_bits, cfg.n_kv_head, ctx, cfg.head_dim)).collect();
1539:            * KvCache::new(kv_bits, cfg.n_kv_head, ctx, cfg.head_dim).octets();
1540:        println!("[co
… [461 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '855,905p' drave-core/src/main.rs", "description": "Read inference loop in main.rs"}`

  ```
tronque
            } else { ids };
            print!("assistant> ");
            let _ = std::io::Write::flush(&mut std::io::stdout());
            let mut accumules: Vec<u32> = Vec::new();
            let mut deja = String::new();
            let mut affiche = |t: u32| {
                accumules.push(t);
                let texte = tks.decode(&accumules);
                if texte.len() > deja.len() {
                    print!("{}", &texte[deja.len()..]);
                    let _ = std::io::Write::flush(&mut std::io::stdout());
                    deja = texte;
                }
            };
            let (out, st) = mdl.generate(&ids, n_new, temp, top_p, rep_pen, hist,
                                         Some(&mut affiche));
            println!();
            eprintln!("  [{:.1} tok/s, {} jetons]", st.n_gen as f64 / st.gen_s.max(1e-9), st.n_gen);
            conversation.push_str(&tks.decode(&out));
            conversation.push('\n');
            n_tour += 1;
            if n_tour >= 50 { break; }
        }
        return;
    }

    let (out, st) = if topk > 0 {
        // pas-à-pas : utile pour confronter les logits à la référence numpy
        let t0 = Instant::
… [1087 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2140,2210p' drave-core/src/main.rs", "description": "Read distributed mode loops"}`

  ```
(le premier ne prédit rien) — reçu {}. Rien n'a été calculé.", ids.len());
        return;
    }
    println!("[flux] pilote : {couches_locales} couches en local, {} chez le pair, {} jetons",
             n_layer - couches_locales, ids.len());

    // 1. référence locale, tout le modèle (même découpage que le chemin réparti)
    let t0 = Instant::now();
    let mut nll_ref = 0f64;
    if lot > 1 {
        let mut pos = 0usize;
        while pos < ids.len() {
            let t = lot.min(ids.len() - pos);
            let hs = mdl.forward_lot(&ids[pos..pos + t], pos);
            let lgs = mdl.logits_lot(&hs);
            for i in 0..t {
                if pos + i + 1 < ids.len() {
                    nll_ref += nll_logits(&lgs[i], ids[pos + i + 1]);
                }
            }
            pos += t;
        }
    } else {
        for (pos, &t) in ids.iter().enumerate() {
            let last = mdl.forward(t, pos);
            if pos + 1 < ids.len() {
                nll_ref += nll_logits(&mdl.logits(&last), ids[pos + 1]);
            }
        }
    }
    let ppl_ref = (nll_ref / (ids.len() - 1) as f64).exp();
    println!("  référence locale  : perplexité {ppl_ref:.4}  ({:.1} s)"
… [1916 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '820,858p' drave-core/src/main.rs; echo \"=== reparti head ===\"; sed -n '2110,2145p' drave-core/src/main.rs; echo \"=== mla 3025-3040 ===\"; sed -n '3018,3040p' drave-core/src/main.rs", "description": "Read truncation in inte … [31 caractères tronqués]`

  ```
quantile {hebb_q} -> {hebb_out}");
    }
    if ids.is_empty() && !session {
        eprintln!("rien à générer : --ids ou --prompt requis");
        return;
    }

    mdl.reset_events();

    // ---------------------------------------------------------------- session
    // Boucle interactive : chaque tour est ajouté à la conversation et
    // retraité en entier. L'invite complète repasse donc par le modèle à chaque
    // tour (coût quadratique en nombre de tours), mais c'est exact, et le cache
    // KV n'a pas à être découpé par tour.
    if session {
        let tks = build_tokenizer(&mdl.g);
        let mut conversation = String::new();
        let mut n_tour = 0usize;
        loop {
            eprint!("vous> ");
            let _ = std::io::Write::flush(&mut std::io::stderr());
            let mut ligne = String::new();
            if std::io::stdin().read_line(&mut ligne).unwrap_or(0) == 0 { break; }
            let q = ligne.trim();
            if q.is_empty() { continue; }
            if q == "/quit" || q == "/q" { break; }
            conversation.push_str(&format!(
                "<|im_start|>user\n{q}<|im_end|>\n<|im_start|>assistant\n"));
            let ids = tks.
… [3785 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"truncate\\|\\.min(ctx)\\|ids.len() >\" drave-core/src/main.rs | head -20; echo \"=== forward_lot write ===\"; sed -n '2530,2550p' drave-core/src/model.rs; echo \"=== kvc.ecrire in forward ===\"; sed -n '3155,3175p' drave-co … [82 caractères tronqués]`

  ```
2114:    let limite = opt.limit.max(1).min(ctx);
2569:        ord.truncate(k);
2731:                    ord.truncate(k);
2911:                att.truncate(k2);
3850:        if ids.len() > voulu { ids.truncate(voulu); }
=== forward_lot write ===
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
         
… [1134 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2255,2290p' drave-core/src/main.rs; echo \"=== 2040-2085 ===\"; sed -n '2040,2085p' drave-core/src/main.rs", "description": "Read server-side pos handling"}`

  ```
hn.push(mdl.norme_finale(&etats[i * mdl.cfg.hidden..(i + 1) * mdl.cfg.hidden]));
            }
            let lgs = mdl.logits_lot(&hn);
            for i in 0..t {
                if pos + i + 1 < ids.len() {
                    nll += nll_logits(&lgs[i], ids[pos + i + 1]);
                }
            }
            pos += t;
        }
    } else {
    for (pos, &t) in ids.iter().enumerate() {
        let dernier = pos + 1 == ids.len();
        // Le DERNIER jeton n'a rien à prédire : lui demander un aller-retour
        // distant, c'est payer un calcul complet — des deux côtés — pour un état
        // que personne ne lit. On sort donc ici, AVANT le calcul local aussi.
        // La référence locale, elle, calcule encore ce dernier jeton pour rien
        // (1 sur N : négligeable, mais écrit ici pour que personne ne s'étonne
        // d'un écart de temps entre les deux chemins).
        if dernier { break; }
        let horloge = Instant::now();
        let etat = mdl.forward(t, pos);
        t_local += horloge.elapsed().as_secs_f64();
        let horloge = Instant::now();
        let (o, a) = envoyer_flux(&mut sock, couches_locales as u32, n_layer as u32,
                  
… [3277 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reproducing the residual panic in two configurations

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport random\nrandom.seed(2)\nids=[random.randrange(0,150000) for _ in range(256)]\nopen('/tmp/rev_ids_256.txt','w').write(','.join(map(str,ids)))\" && echo \"=== TEST ids == ctx ===\" && timeout 300 ./drave-core/targ … [232 caractères tronqués]`

  ```
=== TEST ids == ctx ===

thread 'main' (2721392) panicked at src/model.rs:3025:9:
contexte dépassé (256 ≥ 256)
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
timeout: the monitored command dumped core
[exit 134]
  ```

### 🤖 Assistant

⏵ Testing the distributed path with an over-long id list

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 ./drave-core/target/release/drave ./models/Qwen2.5-0.5B-Q8_0.gguf --ppl-reparti 127.0.0.1:9 --couches-locales 12 --ids \"$(cat /tmp/rev_ids_300.txt)\" --ctx 256 --lot 8 --dense --threads 8 2>&1 | tail -8; echo \"[exit ${P … [72 caractères tronqués]`

  ```
[config] rotation : RoPE simple (le modèle ne déclare pas YaRN)
[flux] quantification : 127 niveaux, seuil 0, top-k 0, renorm false
[flux] pilote : 12 couches en local, 12 chez le pair, 300 jetons

thread 'main' (2721582) panicked at src/model.rs:1213:20:
range end index 32832 out of range for slice of length 32768
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
timeout: the monitored command dumped core
[exit 134]
  ```

### 🤖 Assistant

⏵ Final source checks on the launch-count claim and subagent status

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '200,215p;240,252p' reports/rapport-gpu-topk-selection.md", "description": "Read launch-count context in report"}`

  ```
DEUX variables à la fois. Ce qui est établi : à ~255 clés le CPU gagne nettement
(4,21 contre 7,68 ms/jeton), à ~2 047 clés le déport gagne nettement (7,59 contre
19,58). **Le croisement en clés est donc entre 255 et 2 047 clés**, et il est plus
haut que celui de l'attention complète (~4 000 clés d'après `docs/contexte-long.md`,
mesuré à nombre de jetons égal) — à cause du coût fixe : 8 lancements et 17
transferts par couche et par jeton. Une grille propre demanderait de faire varier le
nombre de jetons à contexte fixé (17 434 jetons sont disponibles dans
`/tmp/ids_qwen_long.txt` ; une passe à 16 384 jetons coûte ~20 min par chemin). La
raison est la même que celle déjà payée sur le miroir KV (« les tampons alloués à
chaque appel : 24,5 ms/jeton au lieu de 2,9 », `docs/contexte-long.md` §4.ter) :
la chaîne fait **six lancements et cinq recopies par couche et par jeton**, soit
~74 000 lancements pour ces 511 jetons, à comparer aux ~0,1 ms de calcul utile par
couche. Ce n'est pas un noyau de plus qu'il faut, c'est **la fusion des quatre
passes** dans un seul noyau (descente radix sur le périphérique) et la
réutilisation des tampons hôtes.


## Noyau 4 : tout le top-k d'une ligne en U
… [628 caractères tronqués]
  ```

- **list_agents** `{}`

  ```
8288d350-b68e-4245-b903-5ef6d71910b4 [running] — Audit livelock fix in model.rs
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo -n \"tests in main.rs: \"; grep -c \"#\\[test\\]\" drave-core/src/main.rs; grep -rn \"#\\[test\\]\" drave-core/src/*.rs | wc -l; echo \"=== gates in README/REPRISE ===\"; grep -n \"19,3885\\|15,1757\\|18 tests\" README.md REPRIS … [71 caractères tronqués]`

  ```
tests in main.rs: 12
18
=== gates in README/REPRISE ===
README.md:363:| **gpt-oss-120b** (MoE, MXFP4) | MXFP4 | **15,1757** (ctx 256) | blocs lus | 60 Go |
REPRISE.md:35:> **19,3885** et gpt-oss ctx 256 = **15,1757**, `cargo test` **17/17**. La porte
REPRISE.md:62:| Qwen2.5-0.5B Q8_0 | `--dense --limit 512` | **19,3885** |
REPRISE.md:70:| gpt-oss-120b MXFP4 | `--dense --limit 512`, ids_oss | **15,1757** (510 jetons, deux fenêtres) |
REPRISE.md:182:| porte gpt-oss selon l'ouverture du pilote | sans `DRAVE_GPU` : **15,1757** · avec `DRAVE_GPU=1` : **15,1667** — l'écart vient du déport automatique des projections Q8_0 (> 8 Mo), pas d'une régression |
REPRISE.md:256:| `DRAVE_TRACE_BLOCS=1` | trace DRVF **v3** : valeurs i8, échelle f16 par bloc de 32 | 45 079 930 o contre 66 370 408 en v2 (−32 %), rejeu 19,4029 contre 19,3885 (+0,074 %) |
REPRISE.md:271:0,06 % (15,1757 → 15,1667 sur gpt-oss).
REPRISE.md:349:| rejeu `--flux-forcer` | 19,3885 | 19,3885 | 19,4029 (+0,074 %) |
REPRISE.md:354:« rejeu v3 = 19,3885 » lisait en fait la perplexité du calcul normal, la trace
REPRISE.md:452:   (référence CPU 15,1757 ; Qwen n'a pas de puits, donc la porte de 19,3885 ne
  ```

### 👤 Utilisateur

Agent 8288d350-b68e-4245-b903-5ef6d71910b4 sent a message:
REVUE ADVERSE — livelock `KvCache::assurer` (drave-core), lecture seule, aucune modif.

(a) VERDICT sur le correctif : la boucle est bien terminée, mais le correctif est INCOMPLET et le « vérifié : rend la main en 312 s » est FAUX (c'est un SIGABRT).
- `assurer` termine pour toute entrée : model.rs:1126 `let besoin = besoin.min(self.ctx);` puis model.rs:1129 `while cap < besoin { cap = (cap * 2).min(self.ctx); }`. `cap ≤ ctx` toujours (y compris ctx=0). OK.
- MAIS model.rs:1124-1125 affirme « l'appelant voit la troncature par le message ci-dessous » : FAUX. Le message n'existe que dans `generate`. `ecrire` (model.rs:1209-1213) ne teste QUE `pos + 1 > self.cap` puis indexe `let d = (kvh * self.cap + pos) * self.hd;` → au-delà de ctx, `assurer` ne grandit plus et l'écriture part dans le bloc de la tête KV SUIVANTE (corruption silencieuse) avant de paniquer sur la dernière tête. Le plafond transforme le livelock en OOB.
- Le vrai chemin nominal reste cassé : `generate` tronque à ctx SANS réserver `n_new` (model.rs:3930-3934 `&ids[coupe..]` → `ids.len() == ctx`), puis la décodage fait model.rs:3976-3977 `let pos = ids.len() + step; last = self.forward(next, pos);` et `forward` porte le seul garde : model.rs:3025 `assert!(pos < self.ctx, "contexte dépassé ({pos} ≥ {})", self.ctx);`. Donc dès le 1er jeton généré : panique (release = `panic = "abort"`, Cargo.toml), exit 134. Le mode session fait pourtant le bon calcul (main.rs:851-856 `ids.len() + n_new + 8 > ctx` → `garde = ctx - (n_new + 8)`), pas `generate`.
PREUVES (binaire release du dépôt, Qwen2.5-0.5B, ctx 8) :
1) `--ids 1..12 --n 2 --ctx 8 --lot 4` → exit 134, « [contexte] invite de 12 jetons > ctx 8 : les 4 premiers sont ABANDONNÉS » puis `panicked at src/model.rs:3025:9: contexte dépassé (8 ≥ 8)`.
2) invite 6 ≤ ctx 8, `--n 4` (la GÉNÉRATION dépasse) → même panique.
3) réplique exacte de la commande du digest (`--infer --chat --flux --prompt … --n 8 --ctx 8 --threads 16 --temp 0 --lot 4`) → exit 134, même panique.
4) La commande du « 312 s » (extraite verbatim de session.jsonl.zstd) est `--infer --chat --flux --prompt <4788 jetons> --n 8 --ctx 4608 --threads 16 --temp 0 --lot 256` : mêmes drapeaux → même abort après le préremplissage (312 s = le préremplissage). Le script de vérification ne lit jamais `r.returncode` ni « panicked » : il n'imprime que 3 lignes filtrées, donc l'abort est invisible. « code trouvé : False » s'explique par l'abort, pas par l'aiguille tronquée (elle était à mi-profondeur, donc conservée). Le commentaire du rapport (« rend maintenant la main en 312 s, coût normal du CPU ») et REPRISE.md sont donc non étayés.

(b) CHEMINS QUI DÉPASSENT ENCORE ctx SANS TRONCATURE NI REFUS :
- S1 CRITIQUE — décodage de `generate` : model.rs:3976-3977 (ci-dessus) + model.rs:3025. Tout prompt tronqué à ctx (le cas même du correctif) ou toute génération qui atteint ctx → SIGABRT. Prouvé (1,2,3).
- S2 ÉLEVÉ — `ecrire` sans contrôle de `pos < ctx` : model.rs:1210-1213. Prouvé par `--ppl-reparti`.
- S3 ÉLEVÉ — `--ppl-reparti --ids` : main.rs:2114 calcule `let limite = opt.limit.max(1).min(ctx);` mais main.rs:2133-2135 `let ids: Vec<u32> = if opt.ids.is_empty() { (1..=limite as u32).collect() } else { opt.ids.clone() };` ignore `limite`. Référence locale main.rs:2151-2161 (`forward_lot(&ids[pos..pos+t], pos)`) ou 2163-2168 (`forward(t, pos)`) → dépasse ctx AVANT même la connexion au pair. Prouvé : `--ppl-reparti 127.0.0.1:9 --ctx 8 --limit 4 --lot 4 --ids <40 jetons>` → exit 134, `panicked at src/model.rs:1213:20: range end index 1088 out of range for slice of length 1024`. Le refus propre main.rs:2053-2057 n'existe que côté SERVEUR.
- S4 MOYEN — mode `--topk` : main.rs:886 `for (pos, &t) in ids.iter().enumerate() { last = mdl.forward(t, pos); }` et main.rs:897 `last = mdl.forward(next, ids.len() + step);` : aucune troncature, aucun refus → panique si prompt > ctx ou prompt+n_new > ctx.
- S5 MOYEN (latent) — `forward_lot` n'a AUCUN garde de position : model.rs:2545 `kvc.ecrire(hh, pos, …)`, allocation model.rs:2442 `let mut sc2 = vec![0f32; nh * self.ctx];`, indexation model.rs:2599 `sc2[hh * ctx + tt] = …` et slice model.rs:2603 `&mut sc2[hh * ctx..hh * ctx + n]`. C'est ce que S3 déclenche. Les autres appelants sont bornés : serveur main.rs:2053 `if f.pos as usize + t > mdl.ctx { … }` (mais `break`, pas `continue`, alors que le message dit « le nœud continue » — défaut mineur), `run_ppl` (fenêtres ≤ ctx), `generate` (après troncature).
- S6 FAIBLE — `--banc-mla` main.rs:2960 → assert model.rs:2914 `assert!(pos < self.ctx, "contexte dépassé");`.
- S7 FAIBLE — harmony à petit ctx : main.rs:3706 `let budget = ctx.saturating_sub(consigne.len() + tete.len() + 1).max(16);`, main.rs:3735 `let piece = ((ctx.saturating_sub(systeme.len() + 16)) / 2).max(16);` et le garde main.rs:3748 `if cur.len() + e.len() + n + 1 > ctx && cur.len() > systeme.len()` : le `.max(16)` et le premier tour (cur == systeme) peuvent construire une fenêtre > ctx → `forward_lot` écrit au-delà du plafond. Non testé empiriquement (Qwen n'a pas `<|start|>` ; à ctx normal le garde tient).
- `run_ppl` avec `--limit` > `--ctx` : SÛR — main.rs:3924 `ids.chunks(ctx)` et main.rs:3933 `let fin = (base + ctx).min(ids.len());` bornent chaque fenêtre à ctx (plus de jetons = plus de fenêtres). RAS.
- Côté GPU, les gardes existent bien : gpu.rs:1185 `if n == 0 || n > m.ctx { return false; }`, gpu.rs:445-447 `if besoin > m.ctx { return false; }`, gpu.rs:519 `if kvh >= m.n_kv || t == 0 || pos0 + t > m.ctx { return false; }`. La revendication « le GPU était déjà corrigé » est exacte ; le CPU ne l'est qu'à moitié.

(c) VERDICT SUR LE TEST (main.rs:4370-4381) : il teste bien ce que son nom dit, mais faiblement.
```rust
    #[test]
    fn assurer_ne_boucle_pas_au_dela_du_contexte() {
        let mut c = model::KvCache::new(32, 2, 16, 8);   // ctx = 16 positions
        c.assurer(1000);          // 1000 >> 16 : la boucle doit se terminer
        assert!(c.cap <= 16, "capacité {} au-delà du contexte 16", c.cap);
        c.assurer(8);
        assert!(c.cap <= 16);
    }
```
- Oui : `assurer(1000)` avec besoin > ctx=16 ; si l'ancien corps revient (sans `besoin.min(ctx)`), la boucle ne termine pas → le test PEND (pas d'échec) et gèle tout `cargo test` (aucun timeout). Le mécanisme de non-régression existe donc.
- Mais : `KvCache::new` a déjà appelé `assurer(ctx.min(1024))` (model.rs:1110) → `cap == 16` ; le test sort à model.rs:1126-1127 sans jamais exécuter la boucle de doublement. Il ne teste que le plafond, pas la terminaison de la boucle (un cas `cap < besoin` avec `besoin > ctx` — p.ex. ctx 4096 puis `assurer(10_000)` — serait plus fort). Le second `assert` est vacuitaire (`assurer(8)` rend la main dès model.rs:1118).
- Il ne teste PAS la troncature de `generate`, contrairement à ce que le message de commit accole (« Deux corrections … un test de non-régression ») ; et donc rien dans la suite ne couvre S1-S3, ce qui explique que 18/18 passent alors que le scénario revendiqué abortit.

(d) COMPTAGE : 18 est exact, mais pas avec `grep -c` sur main.rs seul (12). Total crate = main.rs 12 + model.rs 1 + engine.rs 2 + list.rs 3 = 18. Avant 32951e9 : 17 (main.rs 11). `cd drave-core && cargo test --release` → « test result: ok. 18 passed; 0 failed; … finished in 0.12s », dont `tests_plafond::assurer_ne_boucle_pas_au_dela_du_contexte ... ok`.

(e) AUTRES DÉFAUTS / ÉCARTS DOC-CODE :
1. Le script de vérification du digest ne teste pas le code de sortie → le rapport et REPRISE.md affirment une réussite de bout en bout non mesurée ; l'explication « l'aiguille était peut-être dans les 180 jetons tronqués » est contredite par ses propres chiffres (aiguille à ~50 % de profondeur, donc conservée).
2. model.rs:1124-1125 : commentaire faux (« l'appelant voit la troncature ») ; `ecrire` ne peut rien voir.
3. main.rs:2057 : `break` (tue le nœud) au lieu de `continue`, contrairement aux deux autres refus et au message.
4. `vers_gpu_tranche` (model.rs:1284-1289) construit `from_raw_parts(self.kf[d..].as_ptr(), t * self.hd * 4)` : `self.kf[d..]` ne valide pas `d + t*hd ≤ len` → UB silencieuse si un appelant passait `t > 1` près de la fin ; aujourd'hui t=1 partout (miroir_gpu), donc latent.
5. Message de troncature sur stdout (`println!`) alors que les autres diagnostics sont sur stderr, et réimprimé à CHAQUE appel de `generate` (donc à chaque tour en mode session).
CONCLUSION : livelock réellement corrigé (terminaison garantie, cap ≤ ctx), mais le garde-fou est posé au mauvais endroit : `assurer` plafonne en silence et `ecrire`/`generate`/`--topk`/`--ppl-reparti --ids` transforment le dépassement en SIGABRT (ou en écriture dans la tête KV voisine). Le « vérifié 312 s » est un abort de préremplissage.

### 🤖 Assistant

⏵ Confirming abort mode and wrapping up findings

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"panic\\|profile\" drave-core/Cargo.toml | head; echo \"=== 312 command flags in report ===\"; grep -n \"312\\|4788\" reports/rapport-aiguille-topk.md", "description": "Check panic abort and report claims"}`

  ```
14:[profile.release]
18:panic = "abort"
=== 312 command flags in report ===
262:« `[contexte] invite de 4788 jetons > ctx 4608 : les 180 premiers sont ABANDONNÉS
264:sans finir rend maintenant la main en **312 s** (le coût normal du chemin CPU, sans
  ```

### 👤 Utilisateur

Background subagent 8288d350-b68e-4245-b903-5ef6d71910b4 finished and will do no further work unless you send it more.
Its closing message:
⏵ Rapport final : verdict, chemins non bornés, test, comptage

Rapport transmis à l'agent parent. Analyse strictement en lecture (aucun fichier du dépôt modifié ; seuls `target/`, `/tmp` et le binaire existant ont servi aux vérifications).

# (a) Verdict sur le correctif — INCOMPLET

**La boucle est bien terminée et `cap ≤ ctx` toujours** (y compris `ctx == 0`) :
- `drave-core/src/model.rs:1118` `if besoin <= self.cap { return; }`
- `drave-core/src/model.rs:1126` `let besoin = besoin.min(self.ctx);`
- `drave-core/src/model.rs:1129` `while cap < besoin { cap = (cap * 2).min(self.ctx); }`

**Mais l'invariant annoncé est faux et le scénario revendiqué ne fonctionne pas.**
1. `drave-core/src/model.rs:1124-1125` affirme « l'appelant voit la troncature par le message ci-dessous » : **faux**. Le message n'existe que dans `generate`. `ecrire` ne teste que `pos + 1 > self.cap` (`model.rs:1210`) puis indexe `let d = (kvh * self.cap + pos) * self.hd;` (`model.rs:1211`) : au-delà de `ctx`, `assurer` ne grandit plus, l'écriture part dans le **bloc de la tête KV suivante** (corruption silencieuse) puis panique sur la dernière tête. Le plafond convertit le livelock en OOB.
2. `generate` tronque à `ctx` **sans réserver `n_new`** (`model.rs:3930-3934` → `ids.len() == ctx`), puis la décodage fait `model.rs:3976-3977` `let pos = ids.len() + step; last = self.forward(next, pos);` — et le seul garde est `model.rs:3025` `assert!(pos < self.ctx, "contexte dépassé ({pos} ≥ {})", self.ctx);`. **Dès le 1er jeton généré : panique** (release `panic = "abort"` → SIGABRT, exit 134). Le mode session, lui, fait le bon calcul (`main.rs:851-856`, `ids.len() + n_new + 8 > ctx` → `garde = ctx - (n_new + 8)`), pas `generate`.

**Preuves (binaire release du dépôt, Qwen2.5‑0.5B)**
| essai | résultat |
|---|---|
| `--ids 1..12 --n 2 --ctx 8 --lot 4` | message de troncature puis `panicked at src/model.rs:3025:9: contexte dépassé (8 ≥ 8)`, exit **134** |
| invite 6 ≤ ctx 8, `--n 4` (la génération dépasse) | même panique, exit **134** |
| réplique exacte des drapeaux du digest (`--infer --chat --flux --prompt … --n 8 --ctx 8 --threads 16 --temp 0 --lot 4`) | message puis même panique, exit **134** |
| `--ppl-reparti … --ids <40> --ctx 8 --limit 4 --lot 4` | `panicked at src/model.rs:1213:20: range end index 1088 out of range for slice of length 1024`, exit **134** |

**Le « vérifié : rend la main en 312 s » est un abort.** La commande exacte, extraite de `journal/.../session.jsonl.zstd`, est `--infer --chat --flux --prompt <4788 jetons> --n 8 --ctx 4608 --threads 16 --temp 0 --lot 256` : mêmes drapeaux que ma réplique → abort après le préremplissage (312 s = le préremplissage). Le script de vérification ne lit **jamais** `r.returncode` ni `"panicked"` (il n'imprime que 3 lignes filtrées) : l'abort est invisible. « code trouvé : False » s'explique par l'abort, pas par l'aiguille tronquée (elle était à mi‑profondeur, donc **conservée**) — l'explication du rapport est contredite par ses propres chiffres. `REPRISE.md` et `reports/rapport-aiguille-topk.md` sont donc non étayés.

# (b) Chemins qui dépassent encore `ctx` sans troncature ni refus

| # | Sévérité | Chemin | Preuve / citation |
|---|---|---|---|
| S1 | **CRITIQUE** | décodage de `generate` | `model.rs:3976-3977` `let pos = ids.len() + step; last = self.forward(next, pos);` + `model.rs:3025` assert → SIGABRT (prouvé 3×) |
| S2 | **ÉLEVÉE** | `ecrire` sans contrôle `pos < ctx` | `model.rs:1210-1213` `if pos + 1 > self.cap { self.assurer(pos + 1); } let d = (kvh * self.cap + pos) * self.hd; … self.kf[d..d + self.hd]` |
| S3 | **ÉLEVÉE** | `--ppl-reparti --ids` : `limite` calculé puis ignoré | `main.rs:2114` `let limite = opt.limit.max(1).min(ctx);` vs `main.rs:2133-2135` `} else { opt.ids.clone() };` → boucle locale `main.rs:2151-2161` / `2163-2168` (prouvé) |
| S4 | MOYENNE | mode `--topk` | `main.rs:886` `for (pos, &t) in ids.iter().enumerate() { last = mdl.forward(t, pos); }` et `main.rs:897` `last = mdl.forward(next, ids.len() + step);` |
| S5 | MOYENNE (latent) | `forward_lot` sans garde de position | `model.rs:2545` `kvc.ecrire(hh, pos, …)`, `model.rs:2442` `let mut sc2 = vec![0f32; nh * self.ctx];`, `model.rs:2599` `sc2[hh * ctx + tt]`, `model.rs:2603` `&mut sc2[hh * ctx..hh * ctx + n]` |
| S6 | FAIBLE | `--banc-mla` | `main.rs:2960` → `model.rs:2914` `assert!(pos < self.ctx, "contexte dépassé");` |
| S7 | FAIBLE | harmony à petit `ctx` | `main.rs:3706` `… .max(16)`, `main.rs:3735` `… .max(16)`, garde `main.rs:3748` inopérant au 1er tour (`cur.len() > systeme.len()`) → fenêtre > ctx construite (non testé empiriquement : Qwen n'a pas `<|start|>`) |

**Ce qui est sûr** : `run_ppl` avec `--limit` > `--ctx` est **borné** — `main.rs:3924` `ids.chunks(ctx)` et `main.rs:3933` `let fin = (base + ctx).min(ids.len());` : plus de jetons = plus de fenêtres, jamais de fenêtre > ctx. Côté GPU les gardes existent bien : `gpu.rs:1185` `if n == 0 || n > m.ctx { return false; }`, `gpu.rs:445-447` `if besoin > m.ctx { return false; }`, `gpu.rs:519` `if kvh >= m.n_kv || t == 0 || pos0 + t > m.ctx { return false; }` → la revendication « le GPU était déjà corrigé » est exacte.
Défaut annexe : `main.rs:2053-2057` refuse le lot trop long mais avec `break` (tue le nœud) alors que le message dit « le nœud continue » et que les deux autres refus font `continue`.

# (c) Verdict sur le test `assurer_ne_boucle_pas_au_dela_du_contexte` (`main.rs:4370-4381`)

```rust
    #[test]
    fn assurer_ne_boucle_pas_au_dela_du_contexte() {
        let mut c = model::KvCache::new(32, 2, 16, 8);   // ctx = 16 positions
        c.assurer(1000);          // 1000 >> 16 : la boucle doit se terminer
        assert!(c.cap <= 16, "capacité {} au-delà du contexte 16", c.cap);
        c.assurer(8);
        assert!(c.cap <= 16);
    }
```
- **Il teste bien ce que son nom dit** : `assurer(1000)` avec `besoin > ctx` ; si l'ancien corps revient (sans `besoin.min(ctx)`), la boucle ne termine pas → le test **pend** et gèle tout `cargo test` (aucun timeout).
- **Mais faiblement** : `KvCache::new` a déjà appelé `assurer(ctx.min(1024))` (`model.rs:1110`) → `cap == 16` ; le test sort à `model.rs:1126-1127` **sans jamais exécuter la boucle de doublement**. Il ne vérifie que le plafond ; un cas `cap < besoin` avec `besoin > ctx` (p.ex. ctx 4096 puis `assurer(10_000)`) testerait la terminaison réelle. Le second `assert` est vacuitaire (`assurer(8)` rend la main dès `model.rs:1118`).
- **Il ne teste pas la troncature de `generate`**, contrairement à ce que le message de commit accole aux deux corrections — d'où 18/18 verts alors que le scénario revendiqué abortit.

# (d) Comptage des tests : 18 exact, mais pas via `grep -c` sur main.rs

`grep -c '#\[test\]' drave-core/src/main.rs` → **12**. Le total est **18** : main.rs 12 + model.rs 1 + engine.rs 2 + list.rs 3. Avant `32951e9` : 17 (main.rs 11). `cd drave-core && cargo test --release` → `test result: ok. 18 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.12s`, dont `tests_plafond::assurer_ne_boucle_pas_au_dela_du_contexte ... ok`.

# (e) Autres défauts

1. **Méthodologie** : la vérification du digest ne teste pas le code de sortie → une réussite de bout en bout est affirmée dans `REPRISE.md` et `reports/rapport-aiguille-topk.md` sans mesure ; l'explication « l'aiguille était peut-être dans les 180 tronqués » est fausse (aiguille à ~50 % de profondeur, conservée).
2. `model.rs:1124-1125` : commentaire faux (« l'appelant voit la troncature ») ; `ecrire` ne peut rien voir et panique.
3. `main.rs:2057` : `break` au lieu de `continue` (cf. supra).
4. `vers_gpu_tranche` (`model.rs:1284-1289`) : `from_raw_parts(self.kf[d..].as_ptr(), t * self.hd * 4)` — `self.kf[d..]` ne valide pas `d + t*hd ≤ len` → UB silencieuse si un appelant passait `t > 1` ; aujourd'hui `t = 1` partout, donc latent.
5. Message de troncature sur **stdout** (`println!`) alors que les autres diagnostics sont sur stderr, et réimprimé à chaque appel de `generate` (donc à chaque tour en mode session).

**Conclusion** : livelock réellement corrigé dans `assurer` (terminaison garantie, `cap ≤ ctx`), mais le garde-fou est posé au mauvais endroit — `assurer` plafonne en silence, et `ecrire` / la décodage de `generate` / `--topk` / `--ppl-reparti --ids` transforment le dépassement en SIGABRT (avec, avant l'abort, écriture dans la tête KV voisine). Le « vérifié : 312 s » est l'abort du préremplissage.

- **send_message** `{"agent_id": "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", "message": "REVUE ADVERSARIALE DE CLÔTURE (lecture seule, aucun fichier du dépôt modifié ; essais sur copies /tmp + binaire release existant). Budget tenu.\n\nMÉTHODE : chaque chiffre tracé vers rapport/commit/log /tmp/journal ; le livelock revu p … [9210 caractères tronqués]`

  ```
message delivered to agent bbd6969f-0f70-42b2-8951-64d1f2f36d2e
  ```

### 🤖 Assistant

⏵ Review complete, result sent to the parent agent

Relecture terminée (lecture seule ; aucun fichier du dépôt modifié — seuls `/tmp`, `target/` et le binaire release existant ont servi aux essais). Résultat transmis à l'agent parent.

---

# Relecture adversariale de clôture — artefacts non encore audités (30/09 19h49 → 01/10 07h39)

## 1. Écarts classés par gravité

### A — CRITIQUE : « Vérifié : la même invite rend la main en 312 s » est un SIGABRT
- **(a)** `REPRISE.md` §« Sprint 7 » (l.518‑521), `reports/rapport-aiguille-topk.md` (l.264‑266), message du commit `32951e9`.
- **(b)** « la capacité est plafonnée au contexte déclaré, et `Model::generate` tronque l'invite en le disant […] Vérifié : la même invite rend la main en 312 s au lieu de ne jamais finir. »
- **(c)** FAUX quant à l'issue. `generate` (model.rs:3930‑3934) tronque à **exactement** `ctx` sans réserver `n_new` ; la décodage fait `let pos = ids.len() + step; self.forward(next, pos)` (model.rs:3976‑3977) et `forward` assert `pos < self.ctx` (model.rs:3025). **Reproduit 3×** sur le binaire release du dépôt (Qwen2.5‑0.5B, ctx 256) : invite 300 > ctx → message de troncature puis `panicked at src/model.rs:3025: contexte dépassé (256 ≥ 256)`, **exit 134** (`panic = "abort"`). Idem avec invite == ctx. Le mode session, lui, réserve la place (main.rs:851‑856). Le script de vérification du journal ne lisait ni `returncode` ni « panicked » : l'abort est passé pour une réussite ; « code trouvé : False » vient de l'abort, pas de la troncature (l'aiguille était à mi‑profondeur, donc conservée).
- **(d)** Le correctif échange un livelock contre un core dump sur le chemin même qu'il prétend réparer.
- **(e)** Tronquer à `ctx - n_new` (comme la session) ou arrêter proprement la génération quand `pos ≥ ctx`, puis re‑vérifier en testant le code de sortie.

### B — ÉLEVÉ : le garde est au mauvais endroit, `ecrire` n'a aucun contrôle `pos < ctx`
- **(a)** `model.rs:1209‑1213`, commentaire faux `model.rs:1124‑1125`, `forward_lot` sans garde (`model.rs:2545`).
- **(c)** Au‑delà de `ctx`, `assurer` ne grandit plus : `d = (kvh*cap + pos)*hd` écrit dans le bloc de la **tête KV suivante** (corruption silencieuse) puis panique sur la dernière. Reproduit : `--ppl-reparti 127.0.0.1:9 --ids <300> --ctx 256 --lot 8` → `panicked at src/model.rs:1213: range end index 32832 out of range for slice of length 32768`, avant même la connexion au pair (cause : `limite` calculé puis ignoré quand `--ids` est fourni, main.rs:2114 vs 2133‑2135). Restent aussi `--infer --topk` (main.rs:886/897) et harmony à petit ctx (latent). **En revanche `run_ppl --limit > --ctx` est SÛR** (`ids.chunks(ctx)`, main.rs:3924/3933) et le serveur refuse les lots trop longs (main.rs:2053‑2057, mais avec `break` alors que le message dit « le nœud continue »). Côté GPU, les gardes existent bien (gpu.rs:445, 519, 1185).
- **(e)** Garde `pos + 1 ≤ ctx` dans `ecrire`, troncature de `--ids` dans `run_ppl_reparti`, `continue` au lieu de `break`.

### C — MOYEN : « corrigé au sprint 2 » était le sprint 1
`REPRISE.md` l.515‑516, rapport l.258, sprints/06 l.62, commit `32951e9`. Le garde `kv_assurer` a été ajouté par **47ce9b7, 30/09 18:16** = sprint 1 (17:41→19:41), pas sprint 2 (vérifié par `git log -S "besoin > m.ctx"`). REPRISE se contredit (sa description du sprint 1 dit déjà « une boucle infinie latente » corrigée).

### D — MINEUR : « 1/3 » vs « 2 fois sur 3 »
REPRISE l.532 vs README l.511‑513 décrivent la même mesure. La source (rapport l.154‑156, `/tmp/aiguille_s5.log`) donne NON, oui, oui = **2 réussites/3** ; « 1/3 » est le nombre d'échecs, écrit sous une colonne « trouvé ». Correction : « 2/3 (1 échec) ».

### E — MINEUR : commit `c7fd7ea` « six résultats » pour un tableau à 7 lignes.

### F — MINEUR : le test ne couvre que la moitié du correctif.
`KvCache::new` a déjà porté `cap` à 16 → `assurer(1000)` sort au premier garde sans exécuter la boucle de doublement ; rien ne couvre la troncature de `generate` (d'où 18/18 verts alors que le scénario revendiqué abortit). Il aurait bien pendu avant le correctif.

### G — MINEUR : le tableau omet le caveat de charge sur 286,6→63,8 s (×3,9 sous charge, porté par `docs/contexte-long.md`) ; « 23 min au lieu de 75 s » — le comparable mesuré est **85,1 s** à ctx 5120.

## 2. Vérifié et conforme
Tous les chiffres du tableau ont leur source : 8→2 (rapport), **7,2e‑7 / 8,4e‑7** (sortie brute du banc dans le journal, l.37058), 4,53→4,97 ms (`/tmp/grille_fusion.log`), croisement ~300 clés et ×7,8 (=38,84/4,97), 286,6→63,8 s et 9,4335/9,4337 + 2,1e‑5 relatif (`docs/contexte-long.md`, `/tmp/prefill_gpu.log`), 0,0000 dense et 0,0379≈0,038 + 497/511 MoE (rapport logits), k=1024 à 8 192 (12,5 %, un point), **8/9 dense** (`/tmp/aiguille_s6b.log`), **18 tests** (12+1+2+3, `cargo test` 18 passed), `model.rs:1117` exact avant correctif. README « Prochaines étapes » : chemin par lots ignorant `--attn-topk` avec avertissement, 246 s contre 75 (246,5 s mesuré vs 72,7‑85,7 s), 2 fenêtres sur 3 à k=256 — sourcés et exacts. Compteur 13 758 exact. Les six artefacts de la ligne 7 sont tous traçables. Quatre des cinq derniers messages de commit correspondent aux fichiers.

## 3. Le plus fragile
Le garde‑fou a été posé dans `assurer` (le symptôme) et non à l'invariant « `pos < ctx` » (`ecrire`) : la suite passe 18/18 et la nuit est clôturée sur « vérifié », alors que le scénario revendiqué — une invite plus longue que le contexte — se reproduit en SIGABRT sur le binaire committé ; le script de vérification ne lisait pas le code de sortie, troisième occurrence cette nuit d'un artefact qui affirme plus qu'il n'a mesuré.

