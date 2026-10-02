# Session DSH — relecture

- identifiant : `f2de810a-b765-444d-b3cc-d8fce1ba2105`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-02 15:03:29
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en Rust — dossier `drave-core/` — qui exécute les projections sous forme de listes d'activation creuses plutôt que de produits scalaires denses).

TÂCHE : dépouille EXHAUSTIVEMENT, avec l'outil read (lecture complète) :
1. les 9 fichiers de `sprints/` (01-premier-des-trois-noyaux-gpu-du-top-k-le.md, 02-fusionner-la-cha-ne-du-top-k-d-port-desc.md, 03-qualit-de-l-attention-creuse-long-contex.md, 04-le-k-de-l-attention-creuse-l-chec-au-mil.md, 05-refaire-la-grille-avec-de-vraies-fenetres.md, 06-le-taux-de-recuperation.md, 07-cloture-de-la-nuit.md, 08-un-modele-eclate-se-lit-comme-un-seul.md, 09-empreinte-memoire-ce-qui-reduit-vraiment.md) ;
2. l'en-tête (docstring/commentaires et messages d'aide argparse) des scripts de `tools/` : aiguille.py, analyse_empreinte.py, analyse_experts_statique.py, analyse_flux.py, clusters_moe.py, compare_etats.py, compare_logits.py, convertir_clusters.py, diff_flux.py, flux_codec.py, harmony_canonique.py, hc_synthetique.py, lire_meta_gguf.py, mesurer_lecture_experts.py, mla_synthetique.py, pair_factice.py, profil_flux.py, proxy_latence.py, session_report.py, telecharger_modeles.py, trace_compacite.py, verifier_formats.py, vision_mtmd.py, vision_ref.py, et les scripts shell portes.sh, portes_formats.sh, verifier_table_types.sh, inventaire_modeles_lourds.sh, extraire_tables_ggml.sh, preparer_colab.sh, colab_cote_local.sh, sprint.sh ;
3. les options de ligne de commande et les noms de champs exposés dans `drave-core/src/*.rs` (engine.rs, clusters.rs, formats.rs, gpu.rs, gguf.rs, list.rs, materiel.rs, model.rs, tokenizer.rs, main.rs) : cherche les `long("...")`, les `--drapeaux`, les constantes nommées, les enums.

LIVRABLE, structuré exactement ainsi :

## A. Termes, sigles et drapeaux
Une entrée par ligne :
- **TERME** — définition en une phrase ; où c'est utilisé (`chemin/fichier.ext:ligne`) ; nature (drapeau CLI, module Rust, outil Python, terme de protocole...).
Inclus tout le vocabulaire non-français-courant : noms de modes (mode 1/2/3/4), DRVF, DRVF v5, top-k, KV, MLA, MoE, GGUF, Q4_K, MXFP4, IQ2_XXS, AER, paire, grappe, shard, push, pull, porte, porte de correction, densité, engram, hyper-connexion, greffon, aiguille, spiking, Sinkhorn, Hadamard, RoPE, YaRN, RMSNorm, SiLU, SwiGLU, LoRA, MTP, spéculatif, NUMA, PCIe, DDR3, FPGA, DSP, ALM, M20K, AVX2, PTX, VRAM, RSS, TLB, mmap, zstd, perplexité, NLL, débit, bande passante, latence...

## B. Drapeaux CLI et variables d'environnement
Liste exhaustive : drapeau (ou variable `DRAVE_*`) — fichier:ligne — ce qu'il fait, d'après le code ou l'aide.

## C. Contradictions, chiffres périmés, affirmations douteuses
Ce qui est signalé comme périmé/obsolète/faux/corrigé, ou ce qui se contredit. Format : `fichier:ligne` — citation — problème.

## D. Fichiers du dépôt cités ou définis
Chemins cités dans ces fichiers, avec leur rôle.

Sois dense et exhaustif ; pas d'introduction ni de conclusion. Ne modifie AUCUN fichier.
Your parent agent id is "3d5618a0-4e3a-45bb-943d-a72c753fb7da". Before you finish, send your result to that agent with send_message({ agent_id: "3d5618a0-4e3a-45bb-943d-a72c753fb7da", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Inventaire des fichiers à dépouiller dans sprints/, tools/ et drave-core/src/

- **bash** `{"command": "ls -la sprints/ tools/ drave-core/src/ 2>&1 | head -100; echo \"---\"; wc -l sprints/*.md tools/*.py tools/*.sh drave-core/src/*.rs 2>&1", "description": "List files and line counts"}`

  ```
drave-core/src/:
total 1092
drwxr-xr-x. 1 stephane stephane    176  2 oct 11:07 .
drwxr-xr-x. 1 stephane stephane     82 28 sep 11:58 ..
-rw-------. 1 stephane stephane  24376  1 oct 12:08 clusters.rs
-rw-r--r--. 1 stephane stephane  47130  1 oct 21:09 engine.rs
-rw-r--r--. 1 stephane stephane  78620  2 oct 01:11 formats.rs
-rw-------. 1 stephane stephane 107023  2 oct 14:24 gguf.rs
-rw-r--r--. 1 stephane stephane  78414 30 sep 20:15 gpu.rs
-rw-------. 1 stephane stephane  73890  2 oct 10:44 list.rs
-rw-r--r--. 1 stephane stephane 258425  2 oct 12:17 main.rs
-rw-------. 1 stephane stephane  21464  1 oct 22:40 materiel.rs
-rw-r--r--. 1 stephane stephane 382980  2 oct 15:03 model.rs
-rw-------. 1 stephane stephane  20019 28 sep 14:34 tokenizer.rs

sprints/:
total 100
drwxr-xr-x. 1 stephane stephane   746  1 oct 17:43 .
drwxr-xr-x. 1 stephane stephane   612  2 oct 10:56 ..
-rw-r--r--. 1 stephane stephane 11248 30 sep 19:41 01-premier-des-trois-noyaux-gpu-du-top-k-le.md
-rw-r--r--. 1 stephane stephane  8829 30 sep 21:49 02-fusionner-la-cha-ne-du-top-k-d-port-desc.md
-rw-r--r--. 1 stephane stephane 10153 30 sep 23:44 03-qualit-de-l-attention-creuse-long-contex.md
-rw-r--r--. 1 stephane 
… [5500 caractères tronqués]
  ```

- **subagent** `{"description": "Extract Rust CLI flags part 1", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Rust « Drave », moteur d'inférence LLM). NE MODIFIE AUCUN FICHIER (lecture seule stricte).\n\nMISSION : extraire EXHAUSTIVEMENT, depuis ces 3 fichiers uniqu … [1932 caractères tronqués]`
- **subagent** `{"description": "Extract Rust flags part 2", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Rust « Drave », moteur d'inférence LLM). NE MODIFIE AUCUN FICHIER (lecture seule stricte).\n\nMISSION : extraire EXHAUSTIVEMENT, depuis ces 7 fichiers uniquemen … [1713 caractères tronqués]`
- **subagent** `{"description": "Extract Python tool headers", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. NE MODIFIE AUCUN FICHIER (lecture seule stricte).\n\nMISSION : dépouiller l'EN-TÊTE (docstring de module, commentaires d'en-tête, constantes de tête) ET LA DÉFINITIO … [1696 caractères tronqués]`
- **subagent** `{"description": "Extract shell script headers", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet. NE MODIFIE AUCUN FICHIER (lecture seule stricte).\n\nMISSION : dépouiller INTÉGRALEMENT (fichiers courts : 48-132 lignes, lis-les en entier) ces 8 scripts shell dan … [1193 caractères tronqués]`

  ```
started subagent 2c2a6595-b208-446e-bbd1-d0f49eca45e8
  ```


  ```
started subagent 18b8879c-f211-43b8-9908-cf65e509b21d
  ```


  ```
started subagent b13a6032-4f62-4e86-aa1f-03864a455c83
  ```


  ```
started subagent dcaa24d6-0017-4382-be21-8244c0fb9b7a
  ```

### 🤖 Assistant

⏵ Lecture intégrale des 9 fichiers de sprints/

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/01-premier-des-trois-noyaux-gpu-du-top-k-le.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/02-fusionner-la-cha-ne-du-top-k-d-port-desc.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/03-qualit-de-l-attention-creuse-long-contex.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/01-premier-des-trois-noyaux-gpu-du-top-k-le.md</path>
<type>file</type>
<content>
1: # Sprint 1 — Premier des trois noyaux GPU du top-k : les scores d'attention calculés en VRAM, vérifiés contre la référence CPU à 1e-6, avec leur banc
2: 
3: - **Début** : 17:41 · **Fin prévue** : 19:41 (boxing de 120 min)
4: - **Objectif** : Premier des trois noyaux GPU du top-k : les scores d'attention calculés en VRAM, vérifiés contre la référence CPU à 1e-6, avec leur banc
5: - **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.
6: 
7: 
8: ## Revue — ce qui est livré, mesuré
9: 
10: Durée : 120 min (boxing 120 min). Commits : 20.
11: 
12:   - `03243f7` Compteur de lignes Rust re-mesuré en fin de sprint : 13 480 (le chiffre avait bougé de 312 lignes pendant le sprint)
13:   - `22d3004` --options-actives dit si le top-k déporté s'applique, et pourquoi sinon
14:   - `e49f3bb` Rapport : l'étape 5 est faite, et la ligne de l'étape 4 dit la bonne variable (clés vues, pas contexte)
15:   - `c1fdfd4` Rapport et plan : 14 noyaux et 956 lignes (le noyau 3 est arrivé après le comptage), ordre réel de la collecte
16
… [10396 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/02-fusionner-la-cha-ne-du-top-k-d-port-desc.md</path>
<type>file</type>
<content>
1: # Sprint 2 — Fusionner la chaîne du top-k déporté : descente radix, collecte et somme dans UN noyau par ligne (8 lancements → 2, plus de tampon nh×n×4), et gagner dès ~1 000 clés
2: 
3: - **Début** : 19:49 · **Fin prévue** : 21:49 (boxing de 120 min)
4: - **Objectif** : Fusionner la chaîne du top-k déporté : descente radix, collecte et somme dans UN noyau par ligne (8 lancements → 2, plus de tampon nh×n×4), et gagner dès ~1 000 clés
5: - **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.
6: 
7: 
8: ## Revue — ce qui est livré, mesuré
9: 
10: Durée : 119 min (boxing 120 min). Commits : 6.
11: 
12:   - `a76d8c8` REPRISE : le doute sur les projections est à moitié levé (ctx 512 et 1024 identiques, ctx 256 évalue une autre chose)
13:   - `1dee0e6` REPRISE : sprint 2 (fusion du top-k, croisement à ~300 clés, le filet testé, le doute sur les projections)
14:   - `5bc4c0c` Grille propre, noyau fusionné dans le moteur, et gpt-oss (les puits en vrai)
15:   - `ed4ce47` Revue adverse du noyau fusionné : une course bl
… [8061 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/03-qualit-de-l-attention-creuse-long-contex.md</path>
<type>file</type>
<content>
1: # Sprint 3 — Qualité de l'attention creuse à long contexte : aiguille à 4k/8k/16k croisée avec --attn-topk 256, et instruction du doute sur le déport des projections
2: 
3: - **Début** : 21:49 · **Fin prévue** : 23:49 (boxing de 120 min)
4: - **Objectif** : Qualité de l'attention creuse à long contexte : aiguille à 4k/8k/16k croisée avec --attn-topk 256, et instruction du doute sur le déport des projections
5: - **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.
6: 
7: 
8: ## Revue — ce qui est livré, mesuré
9: 
10: Durée : 114 min (boxing 120 min). Commits : 5.
11: 
12:   - `470e3e9` Revue adverse du sprint 3 : deux écarts graves, dans les phrases qui commentent les chiffres
13:   - `d29e043` Correction : `--infer` n'ignore PAS `--lot` (mon grep ne suivait pas la chaîne d'appels)
14:   - `6ad2bc6` Aiguille × attention creuse : le milieu du contexte est perdu (et le doute sur les projections est instruit)
15:   - `6633338` « Accord du top-1 : 511/511 » était faux — 497/511, et l'outil ne le disait pas
16: 
… [9500 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/04-le-k-de-l-attention-creuse-l-chec-au-mil.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/05-refaire-la-grille-avec-de-vraies-fenetres.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/06-le-taux-de-recuperation.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/04-le-k-de-l-attention-creuse-l-chec-au-mil.md</path>
<type>file</type>
<content>
1: # Sprint 4 — Le k de l'attention creuse : l'échec au milieu est-il un réglage (k plus grand) ou un mécanisme manquant ? Grille en --lot 1 (tout le passage creux) et k = 256/512/1024
2: 
3: - **Début** : 23:44 · **Fin prévue** : 01:44 (boxing de 120 min)
4: - **Objectif** : Le k de l'attention creuse : l'échec au milieu est-il un réglage (k plus grand) ou un mécanisme manquant ? Grille en --lot 1 (tout le passage creux) et k = 256/512/1024
5: - **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.
6: 
7: 
8: ## Revue — ce qui est livré, mesuré
9: 
10: Durée : 113 min (boxing 120 min). Commits : 4.
11: 
12:   - `b14e4f2` Contrôle dense à 8 192 : l'information est retrouvée (1002 s, prompt de 7963 jetons) — la question du k vs contexte est mesurable là
13:   - `1425c79` Revue du sprint 4 : « trois fenêtres » étaient trois fois la même invite, et la portée du k était surestimée
14:   - `09adea5` Le k est un réglage : 0/3 au milieu à k=512, 3/3 à k=1024 (trois fenêtres par point)
15:   - `2ae761c` Préremplissage d
… [7130 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/05-refaire-la-grille-avec-de-vraies-fenetres.md</path>
<type>file</type>
<content>
1: # Sprint 5 — Refaire la grille avec de VRAIES fenêtres (outil corrigé) et mesurer si le k nécessaire croît avec le contexte (8192 : k=1024 et 2048)
2: 
3: - **Début** : 01:37 · **Fin prévue** : 03:37 (boxing de 120 min)
4: - **Objectif** : Refaire la grille avec de VRAIES fenêtres (outil corrigé) et mesurer si le k nécessaire croît avec le contexte (8192 : k=1024 et 2048)
5: - **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.
6: 
7: 
8: ## Revue — ce qui est livré, mesuré
9: 
10: Durée : 120 min (boxing 120 min). Commits : 4.
11: 
12:   - `a3691a5` Revue du sprint 5 : la section 8 192 manquait, et « au plus » dépassait la mesure d'un facteur 10
13:   - `0d50e75` À 8 192 clés, k=1024 (12,5 %) suffit : le k nécessaire croît plus lentement que le contexte (deux points)
14:   - `508d3d8` Grille refaite sur trois VRAIS textes : k=256 échoue 1 fois sur 3, pas 3 sur 3
15:   - `ee59519` Pourquoi --lot 1 diffère de --lot 256 : 7e-4 nat par position, top-1 identique partout — c'est une amplification chaotique, pas
… [6587 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/06-le-taux-de-recuperation.md</path>
<type>file</type>
<content>
1: # Sprint 6 — Le TAUX de récupération de l'attention creuse : neuf fenêtres à 4096 (dense, k=256, k=1024) et le troisième point de la courbe k(contexte) à 16384
2: 
3: - **Début** : 03:38 · **Fin prévue** : 05:38 (boxing de 120 min)
4: - **Objectif** : Le TAUX de récupération de l'attention creuse : neuf fenêtres à 4096 (dense, k=256, k=1024) et le troisième point de la courbe k(contexte) à 16384
5: - **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.
6: 
7: 
8: ## Revue — ce qui est livré, mesuré
9: 
10: Durée : 120 min (boxing 120 min). Commits : 4.
11: 
12:   - `45a0c44` Le « ralentissement » est un LIVELOCK : KvCache::assurer boucle sans fin si besoin > ctx (model.rs:1117)
13:   - `361c186` Nuance : le facteur de ralentissement est un minorant (les deux exécutions à ctx 4608 n'ont jamais fini ; la même fenêtre rend en 85,1 s à ctx 5120)
14:   - `e4b3ebc` Le taux par fenêtre : 9 fenêtres contiguës, 8/9 en attention complète, et le mur du préremplissage
15:   - `783f1f9` Sprint 6 : le taux de récupération (9 fenêtres × 3 
… [5363 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/07-cloture-de-la-nuit.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/08-un-modele-eclate-se-lit-comme-un-seul.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/07-cloture-de-la-nuit.md</path>
<type>file</type>
<content>
1: # Sprint 7 — Corriger le livelock du contexte (model.rs:1117) et consolider la nuit : handoff REPRISE/README, portes finales, revue de clôture
2: 
3: - **Début** : 05:39 · **Fin prévue** : 07:39 (boxing de 120 min)
4: - **Objectif** : Corriger le livelock du contexte (model.rs:1117) et consolider la nuit : handoff REPRISE/README, portes finales, revue de clôture
5: - **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.
6: 
7: 
8: ## Revue — ce qui est livré, mesuré
9: 
10: Durée : 121 min (boxing 120 min). Commits : 7.
11: 
12:   - `e7db33b` DeepSeek-V4-Flash téléchargé (86,9 Go, 3 shards) : architecture et tokenizer lus depuis le shard 1, 784 tenseurs depuis le shard 2 — il manque le lien entre les deux
13:   - `beacdf9` DeepSeek-V4.1-Flash : pas de poids ouverts — c'est DeepSeek-V4-Flash qui est téléchargé, et le plan d'adaptation est écrit
14:   - `17282a7` Le résultat de la nuit : à k=256 le taux est le MÊME que l'attention complète (8/9), et les échecs sont sur d'autres fenêtres
15:   - `1b9808e` Le correctif du livelock fin
… [9878 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/08-un-modele-eclate-se-lit-comme-un-seul.md</path>
<type>file</type>
<content>
1: # Sprint 08 — Un modèle éclaté se lit comme un seul : lecteur multi-fichiers, shards et clusters
2: 
3: - **Début** : 11:13 · **Fin** : 13:13 (boxing de 120 min) · **Close** : 11:50
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
19: `tbuf(&t)` — c'est ce qui a permis de changer la représentation sans dupl
… [18551 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/09-empreinte-memoire-ce-qui-reduit-vraiment.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/sprints/09-empreinte-memoire-ce-qui-reduit-vraiment.md</path>
<type>file</type>
<content>
1: # Sprint 09 — L'empreinte mémoire : ce qui réduit vraiment ce qu'il faut charger
2: 
3: - **Début** : 16:35 · **Fin prévue** : 18:35 (boxing de 120 min)
4: - **Objectif** : chiffrer ce qu'un MoE doit charger **avant d'opérer**, et écarter
5:   les pistes qui ne paient pas. Cible : DeepSeek-V4.1-Flash (365,7 Go) sur 125 Go.
6: - **Engagement de fin** : dépôt vert, mesures consignées, machine rendue.
7: 
8: ## Le résultat
9: 
10: L'empreinte de V4.1 tombe de **365,7 Go à 50–80 Go** — et pas en découpant les
11: experts. En décomposant les poids par famille :
12: 
13: | famille | Go | % | à charger |
14: |---|---|---|---|
15: | **engram** | **203,4** | **55,6 %** | **0,4 Go** |
16: | experts | 152,9 | 41,8 % | 21–71 Go |
17: | attention, embeddings, tête | 10,0 | 2,7 % | 10 Go |
18: 
19: `blk.N.engram_embd.weight` : **101,4 Go par couche**, `[384 006 168, 264]` en I8.
20: Ce n'est **pas un tenseur de poids mais une table de hachage de n-grammes**
21: (jusqu'à 4 tokens, 48 nombres premiers de hâchage). Une session de 10 000 jetons
22: n'en t
… [5509 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la && echo \"=== docs ===\" && ls -la docs/ 2>/dev/null && echo \"=== reports ===\" && ls -la reports/ 2>/dev/null | head -40", "description": "Read sprint 9 and list repo root/docs/reports"}`

  ```
total 268
drwxr-xr-x. 1 stephane stephane   612  2 oct 10:56 .
drwxr-xr-x. 1 stephane stephane  2350 25 sep 11:55 ..
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane    96  1 oct 06:58 data
drwxr-xr-x. 1 stephane stephane   636  2 oct 10:22 docs
drwxr-xr-x. 1 stephane stephane    82 28 sep 11:58 drave-core
drwxr-xr-x. 1 stephane stephane   164  2 oct 14:37 .git
-rw-r--r--. 1 stephane stephane   399 30 sep 10:01 .gitignore
drwxr-xr-x. 1 stephane stephane    34 27 sep 11:39 journal
drwxr-xr-x. 1 stephane stephane    88 25 sep 17:13 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-------. 1 stephane stephane 36518  2 oct 10:21 README.md
drwxr-xr-x. 1 stephane stephane  2920  2 oct 12:37 reports
-rw-------. 1 stephane stephane 81777  2 oct 12:37 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane 10507 30 sep 08:44 run_clusters.py
-rw-------. 1 stephane stephane 12507 30 sep 08:44 run_cpu.py
-rw-------. 1 stephane stephane 11462 30
… [5002 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction croisée des drapeaux CLI et variables DRAVE_* dans le dépôt

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== long(\\\"...\\\") occurrences ===\" && grep -rn --include=*.rs -o 'long(\"[^\"]*\")' drave-core/src/ | sort | uniq -c | sort -rn | head -50; echo; echo \"=== count long( ===\" && grep -rc 'long(\"' drave-core/src/*.rs", "d … [43 caractères tronqués]`

  ```
=== long("...") occurrences ===

=== count long( ===
drave-core/src/clusters.rs:0
drave-core/src/engine.rs:0
drave-core/src/formats.rs:0
drave-core/src/gguf.rs:0
drave-core/src/gpu.rs:0
drave-core/src/list.rs:0
drave-core/src/main.rs:0
drave-core/src/materiel.rs:0
drave-core/src/model.rs:0
drave-core/src/tokenizer.rs:0
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== DRAVE_ env vars repo-wide (counts) ===\" && grep -rhoE 'DRAVE_[A-Z0-9_]+' --include=* . 2>/dev/null | sort | uniq -c | sort -rn", "description": "Count all DRAVE_ env vars repo-wide"}`

  ```
=== DRAVE_ env vars repo-wide (counts) ===
    260 DRAVE_GPU
    175 DRAVE_GPU_KV
    106 DRAVE_KV_BITS
     94 DRAVE_GPU_TOPK
     71 DRAVE_CLUSTERS
     67 DRAVE_TRACE_BLOCS
     63 DRAVE_KV_K_F32
     59 DRAVE_KV_K_F16
     48 DRAVE_FLUX_VERIF
     45 DRAVE_KV_F16
     39 DRAVE_KV_V_F32
     31 DRAVE_YARN
     29 DRAVE_SANS_EMPRUNT
     29 DRAVE_GPU_TETE
     27 DRAVE_VISION_TEXTE
     24 DRAVE_TRACE_EXPERTS
     24 DRAVE_FLUX_POS
     22 DRAVE_HARMONY_TRACE
     22 DRAVE_DEBUG_FLUX
     21 DRAVE_YARN_NON
     21 DRAVE_Q8_BLOCS
     21 DRAVE_GPU_EXPERTS
     21 DRAVE_BANC_KV_GPU_SEUL
     20 DRAVE_BANC_KV_UNIT
     19 DRAVE_MMAP
     17 DRAVE_YARN_MSCALE
     16 DRAVE_BANC_KV_K0
     15 DRAVE_BANC_KV_V1
     15 DRAVE_BANC_KV_KUNIT
     14 DRAVE_BANC_KV_GRAD
     14 DRAVE_BANC_KV_DEBUG
     13 DRAVE_GPU_EXPERTS_GO
     12 DRAVE_DEBUG_MLA
     11 DRAVE_YARN_RAMPE
     11 DRAVE_DEBUG_ETAT
      9 DRAVE_BANC_SANS_PUITS
      8 DRAVE_BANC_KV_
      6 DRAVE_PRELIRE_TOUT
      5 DRAVE_LLAMA
      5 DRAVE_KV_
      5 DRAVE_DUMP_COUCHES
      4 DRAVE_PRELIRE
      4 DRAVE_MODELES
      4 DRAVE_KV
      4 DRAVE_ETAT_ENTREE
      3 DRAVE_MODELE
      2 DRAVE_VISIO
      2 DRAVE_FLUX_VER
  
… [92 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== literal --flags in .rs ===\" && grep -rhoE '\"--[a-z0-9][a-z0-9-]*\"' drave-core/src/*.rs | sort | uniq -c | sort -rn", "description": "List literal --flags in Rust sources"}`

  ```
=== literal --flags in .rs ===
      2 "--tokenize"
      2 "--threads"
      2 "--tensors"
      2 "--sonder-engram"
      2 "--ppl-reparti"
      2 "--ppl"
      2 "--plan"
      2 "--matrix"
      2 "--materiel"
      2 "--infer"
      2 "--gpu-banc"
      2 "--flux-serveur"
      2 "--config"
      2 "--banc-vision"
      2 "--banc-topk"
      2 "--banc-mla"
      2 "--banc-kv"
      1 "--trace-flux"
      1 "--trace-couches"
      1 "--top-p"
      1 "--topk-v"
      1 "--topk-up"
      1 "--topk-q"
      1 "--topk-o"
      1 "--topk-k"
      1 "--topk-gate"
      1 "--topk-down"
      1 "--topk"
      1 "--texte"
      1 "--tete-restreinte"
      1 "--tete-garantie"
      1 "--temp"
      1 "--swa-pattern"
      1 "--sortie"
      1 "--session"
      1 "--sans-yarn"
      1 "--sans-fenetre"
      1 "--rep-penalty"
      1 "--qk-topk"
      1 "--q4-tout"
      1 "--q4-ffn"
      1 "--q4-attn"
      1 "--q4"
      1 "--push"
      1 "--prompt"
      1 "--profil-neurones"
      1 "--ppl-texte"
      1 "--pin"
      1 "--patch"
      1 "--options-strict"
      1 "--options-actives"
      1 "--neurones-sortie"
      1 "--n"
      1 "--moe-topk"
      1 "--lot"
      1 "--logits-bi
… [775 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== --flags in tools ===\" && grep -rhoE '\\-\\-[a-z0-9][a-z0-9-]*' tools/*.py tools/*.sh | sort | uniq -c | sort -rn | head -80", "description": "List --flags in tools"}`

  ```
=== --flags in tools ===
      9 --top
      8 --lot
      7 --release
      7 --ctx
      7 --config
      7 --attn-topk
      6 --threads
      5 --repo
      5 --quiet
      5 --ppl
      5 --limit
      5 --couches
      4 --sortie
      4 --since
      4 --oneline
      4 --n
      4 --dense
      4 --clusters
      3 --tensors
      3 --jetons
      3 --gpu-topk
      3 --csv
      2 --zstd-v2
      2 --verifier
      2 --type
      2 --trace
      2 --tokenize
      2 --seulement
      2 --session
      2 --scale
      2 --sans-erreur
      2 --sans-compression
      2 --sans-analysis
      2 --modele
      2 --mode
      2 --manifeste
      2 --json
      2 --journal
      2 --j
      2 --i
      2 --graine
      2 --gpu
      2 --flux-serveur
      2 --fichier
      2 --etat
      2 --echantillon
      2 --dossier
      2 --bloc
      1 --version
      1 --trace-flux
      1 --timeout
      1 --temp
      1 --seuil
      1 --retry-delay
      1 --retry-all-errors
      1 --retry
      1 --prompt
      1 --poids
      1 --materiel
      1 --limite
      1 --lignes
      1 --infer
      1 --gpu-kv
      1 --gguf
      1 --format
      1 --flux-blocs
      1 --flux
      1 --
… [129 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== == \\\"--  in main.rs ===\" && grep -c 'starts_with(\"--\")\\|== \"--' drave-core/src/main.rs; echo \"=== sample of parser ===\" && grep -n 'starts_with(\"--\")\\|fn analyser_args\\|fn parse_args\\|fn args\\|USAGE\\|AIDE\\ … [108 caractères tronqués]`

  ```
=== == "--  in main.rs ===
1
=== sample of parser ===
720:                if a.starts_with("--") || (a.starts_with('-') && lettre) {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la src/ drave-core/ && echo \"=== grep args parse in src/ ===\" && grep -rn 'starts_with(\"--\")' src/ drave-core/ 2>/dev/null | head -20", "description": "Inspect top-level src and drave-core layout"}`

  ```
drave-core/:
total 16
drwxr-xr-x. 1 stephane stephane   82 28 sep 11:58 .
drwxr-xr-x. 1 stephane stephane  612  2 oct 10:56 ..
-rw-r--r--. 1 stephane stephane  154 30 sep 08:44 Cargo.lock
-rw-r--r--. 1 stephane stephane  375 30 sep 08:44 Cargo.toml
drwxr-xr-x. 1 stephane stephane   94 30 sep 20:15 gpu
-rw-r--r--. 1 stephane stephane 4351 30 sep 08:44 README.md
drwxr-xr-x. 1 stephane stephane  176  2 oct 11:07 src
drwxr-xr-x. 1 stephane stephane   70 25 sep 18:32 target

src/:
total 56
drwxr-xr-x. 1 stephane stephane  208 25 sep 17:41 .
drwxr-xr-x. 1 stephane stephane  612  2 oct 10:56 ..
-rw-------. 1 stephane stephane 3168 30 sep 08:44 bpe_np.py
-rw-------. 1 stephane stephane 5410 30 sep 08:44 encoding.py
-rw-------. 1 stephane stephane 6725 30 sep 08:44 gguf_min.py
drwxr-xr-x. 1 stephane stephane  394 25 sep 18:09 __pycache__
-rw-------. 1 stephane stephane 3223 30 sep 08:44 roofline.py
-rw-------. 1 stephane stephane 5370 30 sep 08:44 sparsity.py
-rw-------. 1 stephane stephane 6846 30 sep 08:44 ternary.py
-rw-------. 1 stephane stephane 4821 30 sep 08:44 tiny_model.py
-rw-------. 1 stephane stephane 6556 30 sep 08:44 transformer_np.py
=== grep args parse in src/ ===
drave-core
… [91 caractères tronqués]
  ```

### 👤 Utilisateur

Agent dcaa24d6-0017-4382-be21-8244c0fb9b7a sent a message:
RAPPORT — 8 scripts shell de /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ (lecture seule, aucun fichier modifié). Tous lus intégralement.

### tools/portes.sh (132 lignes)
- Rôle : l.2-6 « Les portes du dépôt, en une commande. » / « Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien : chaque porte est comparée à la valeur ATTENDUE, et le script sort en erreur si l'une diverge. Les valeurs sont celles publiées dans les rapports. » Usage l.8-9 : `tools/portes.sh` (toutes) ou `tools/portes.sh rapide` (« sans gpt-oss (le seul qui prenne ~20 min) »).
- Variables : l.11 `set -u` ; l.12 `cd "$(dirname "$0")/.."` ; l.13 `D=./drave-core/target/release/drave` ; l.14 `RAPIDE=${1:-}` ; l.15 `ECHEC=0` ; l.39 `sortie` ; l.40 `n` (tests passés) ; l.41 `ko` (échecs) ; l.51/58/64/75/89/108/119 `v`/`r`/`p` ; l.56 `A=/home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters-v2` ; l.65 `att=$(nproc); att=$((att / 2))` ; l.95 `M=/home/stephane/Data13TB/stephane/modeles/gguf` ; l.106 `O=/home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf`. AUCUNE variable d'environnement DRAVE_*/MODEL* n'est lue ; aucun `export`.
- Arguments : `$1` → `RAPIDE` (l.14), seule valeur testée : `rapide` (l.71 `if [ "$RAPIDE" = "rapide" ]`, l.105 `!= "rapide"`). Pas de getopts. Paramètres internes de fonctions : `$1/$2/$3` = nom/attendu/obtenu dans `compare()` (l.19-25), `$1/$2/$3` = nom/modèle/motif dans `route()` (l.87-94, appelé l.96-99).
- Commandes : `cargo test --release` lancé dans `drave-core` (l.39) ; `command -v gcc` (l.74) ; `bash tools/portes_formats.sh` sous `timeout 1800` (l.75) ; `nproc` (l.65) ; binaire `$D` avec : `--ppl /tmp/ids_qwen.txt --ctx 256 --abits 16 --threads 16 --limit 512 --dense` (l.51-52), `--ppl ... --ctx 64 --limit 8 --dense --threads 8 --lot 1` (l.58-59), `--materiel` (l.64), `--config` (l.89, l.108), `--tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_oss_512.txt` (l.116), `--ppl /tmp/ids_oss_512.txt --ctx 256 --dense --threads 16 --limit 512` (l.119-120) ; `timeout` 600/900/1800/2400 (l.51,58,75,119) ; pipes `grep -oE`/`head`/`cut` (l.31,40,41,46,64,89,108).
- Entrées-sorties : `models/Qwen2.5-0.5B-Q8_0.gguf` (l.51,64) ; `/tmp/ids_qwen.txt` (l.51,58) ; `$A` clusters Qwen3-30B (l.56,58) ; 4 GGUF sous `$M` (l.96-99) ; `$O` gpt-oss (l.106,108,116,119) ; `/tmp/wt2_txt.txt` (l.115) alimenté par `data/wikitext2_test.txt` (`head -c 20000`, l.115) ; `/tmp/ids_oss_512.txt` (l.114,116,118,119) ; `tools/portes_formats.sh` (l.74-75).
- Constantes/seuils : seuil tests `-ge 48` (l.42) ET `ko -eq 0` (l.42) ; `timeout 600` (l.51), `900` (l.58), `1800` (l.75), `2400` (l.119) ; `--ctx 256` (l.51,119), `--ctx 64` (l.58) ; `--abits 16` (l.52) ; `--threads 16` (l.52,120), `--threads 8` (l.59) ; `--limit 512` (l.52,120), `--limit 8` (l.58) ; `--lot 1` (l.59) ; attendus : Qwen2.5-0.5B ctx 256 = `19.3885` (l.53), Qwen3-30B clusters = `799.8557` (l.60, libellé « origine : 799,8557 »), gpt-oss-120b MXFP4 ctx 256 = `15.6017` (l.121) ; commentaire l.29-30 sur l'instrument faux qui donnait 17,431 (fenêtre 1) ; `head -5` des tests FAILED (l.46) ; threads attendus `>0` et `<= nproc/2` (l.65-66) ; motif de formats accepté `*"0 divergence(s), 0 absent(s)"*` (l.77) ; sous-chaînes de routage attendues : `sigmoïde` (l.96,97), `racine de softplus` (l.98), `softmax` (l.99) ; gpt-oss `*": oui"*` (l.110) ; `exit 2` si binaire absent (l.17) ; `exit $ECHEC` (l.132).
- Modèles codés en dur (route) : GLM-5.3-UD-IQ1_S-00001-of-00006 (l.96), Kimi-K2.7-Code-UD-IQ1_M-00001-of-00008 (l.97), DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003 (l.98), Qwen3-235B-A22B-Instruct-2507-Q2_K-00001-of-00002 (l.99).

### tools/portes_formats.sh (74 lignes)
- Rôle : l.2 « Portes des FORMATS : chaque déquantificateur comparé à libggml, bloc par bloc. » Usage l.4 `tools/portes_formats.sh [type ...]`. Justification l.6-13 : cinq premiers essais faux (IQ2_XXS, IQ1_M, Q2_K, Q5_K, Q6_K), « tous l'ont été par comparaison à la bibliothèque » ; « refuse de « passer » si le témoin a disparu du disque — un test qui saute est un test qui ne dit rien. » ; l.15 « La référence est liée à libggml (voir tools/ref_ggml_bloc.c). »
- Variables : l.16 `set -u` ; l.17 cd racine ; l.18 `RACINE=$PWD` ; l.19 `MODELES=${DRAVE_MODELES:-/home/stephane/Data13TB/stephane/modeles/gguf}` (ENV DRAVE_MODELES) ; l.20 `LLAMA=${DRAVE_LLAMA:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}` (ENV DRAVE_LLAMA) ; l.21 `REF=${REF_GGML_BLOC:-/tmp/ref_ggml_bloc}` (ENV REF_GGML_BLOC) ; l.22 `VERIF=tools/verifier_formats.py` ; l.23 `IFS=$'\n'` ; l.25 `ok=0; ko=0; abs=0` ; l.27 tableau `BATTERIE` ; l.53 `filtre="${*:-}"` ; l.55-58 `lib/fich/tens/typ` ; l.65-66 `sortie`/`sortie2`. Aucun export.
- Arguments : tous les positionnels → `filtre="${*:-}"` (l.53), comparés au libellé (` if [ -n "$filtre" ] && ! echo " $filtre " | grep -q " $lib "; then continue; fi`, l.59) ; noms de types = libellés de la 1re colonne (F32, F16, Q4_0, Q5_0, Q8_0, Q2_K, Q3_K, Q4_K, Q5_K, Q6_K, IQ2_XXS, IQ3_XXS, IQ1_S, IQ4_XS, IQ1_M, BF16, MXFP4). Pas de getopts/--options.
- Commandes : `gcc -O2 -I"$LLAMA/ggml/include" -I"$LLAMA/ggml/src" tools/ref_ggml_bloc.c -o "$REF" -L"$LLAMA/build/bin" -lggml -lggml-base -Wl,-rpath,"$LLAMA/build/bin"` (l.49-50, recompil si `[ ! -x "$REF" ] || [ tools/ref_ggml_bloc.c -nt "$REF" ]`, l.48 ; `|| exit 2` l.50) ; `python3 "$VERIF" "$fich" "$tens" 0` (l.65) et `python3 "$VERIF" "$fich" "$tens" 7` (l.66), sortie filtrée `tail -1` ; `cut -d'|' -f1..4 | xargs` (l.55-58) ; motif `"CONCORDE"` requis sur les deux blocs (l.67).
- Entrées-sorties : 17 modèles dans `$MODELES` + `$RACINE/models/Qwen2.5-0.5B-Q4_0.gguf` (l.28-44) ; tenseurs ciblés : blk.0.attn_norm.weight (l.28), token_embd.weight (l.29-33,35), output.weight (l.32), blk.0.attn_output.weight (l.34), blk.0.ffn_down.weight (l.36,37), blk.0.ffn_gate_exps.weight (l.38,42), blk.1.ffn_down_exps.weight (l.39), blk.3.ffn_gate_exps.weight (l.40), blk.11.ffn_down_exps.weight (l.41), blk.0.ffn_gate_inp.weight (l.43), blk.0.ffn_down_exps.weight (l.44) ; binaire témoin `$REF`=/tmp/ref_ggml_bloc (l.21,48,49) ; sortie ligne finale `formats : $ok concorde(s), $ko divergence(s), $abs absent(s)` (l.73) ; statut de sortie l.74 `[ $ko -eq 0 ] && [ $abs -eq 0 ]`.
- Constantes : tableau `libellé | fichier | tenseur | type ggml` (l.26-45) avec numéros de type ggml : F32=0 (l.28), F16=1 (l.29), Q4_0=2 (l.30), Q5_0=6 (l.31), Q8_0=8 (l.32), Q2_K=10 (l.33), Q3_K=11 (l.34), Q4_K=12 (l.35), Q5_K=13 (l.36), Q6_K=14 (l.37), IQ2_XXS=16 (l.38), IQ3_XXS=18 (l.39), IQ1_S=19 (l.40), IQ4_XS=23 (l.41), IQ1_M=29 (l.42), BF16=30 (l.43), MXFP4=39 (l.44) ; index de blocs testés 0 et 7 (l.65-66) ; fichier modèle cités : codestral-22b-v0.1-q4_k_m.gguf (l.28,35), bge-m3-FP16.gguf (l.29), qwen2.5-0.5b-instruct-q4_k_m.gguf (l.31,32,37), Qwen3-235B-A22B-Q2_K/...-00001-of-00002.gguf (l.33,34), Muse-Glimmer-30B-AD-Q4_K_M.gguf (l.36), DeepSeek-V4.1-Flash-Q2/DeepSeek-V4.1-Flash-Q2.gguf (l.38), Kimi-K2.7-Code-UD-IQ1_M-00002-of-00008.gguf (l.39), GLM-5.3-UD-IQ1_S-00002-of-00006.gguf (l.40), GLM-5.3-Flash-UD-IQ1_S-00002-of-00003.gguf (l.41), DeepSeek-V4-Flash-UD-IQ1_M-00002-of-00003.gguf (l.42,43), gpt-oss-120b-MXFP4.gguf (l.44).

### tools/verifier_table_types.sh (121 lignes)
- Rôle : l.2 « Confronte la table des tailles de types ggml du moteur à celle de `libggml`. » ; l.4-8 pourquoi (table relevée, type absent compté zéro : « un inventaire a annoncé 8,56 Go pour 86,9 Go de fichiers (les experts en `iq1_m`) ») ; usage l.13 `tools/verifier_table_types.sh [chemin de llama.cpp]` ; l.15 « Rend 0 si les tables concordent sur tous les types testés, 1 sinon. »
- Variables : l.17 `set -u` ; l.18 cd racine ; l.19 `RACINE=${1:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}` ; l.20 `SRC=drave-core/src/gguf.rs` ; l.25 `TMP=$(mktemp -d)` ; l.26 `trap 'rm -rf "$TMP"' EXIT` ; l.81 `manquants=0; divergents=0; verifies=0` ; l.104 `inconnus=""` ; boucles `t`, `bloc`, `taille`, `ligne` (l.82-96, 105-109) ; `$2`/`$3` l.90-91 proviennent de `set -- $ligne` (l.89), PAS de la ligne de commande. Aucune ENV, aucun export.
- Arguments : `$1` = chemin de llama.cpp (l.19, défaut /home/.../llama.cpp) ; pas d'options.
- Commandes : `gcc -I"$RACINE/ggml/include" -I"$RACINE/ggml/src" "$TMP/tailles.c" -o "$TMP/tailles" -L"$RACINE/build/bin" -lggml -lggml-base` avec `2>"$TMP/gcc.err"` (l.50-51) ; `sed 's/^/  /' "$TMP/gcc.err" | head -5` (l.52) ; `LD_LIBRARY_PATH="$RACINE/build/bin" "$TMP/tailles" | sort -n > "$TMP/ggml.txt"` (l.53) ; `python3 - "$SRC"` heredoc (l.56-73) : lit la source Rust, isole `pub fn octets_tensor_opt` (l.60-61), regex `(\d+)(?:u64)?\s*=>\s*\(\s*(\d+)(?:u64)?\s*,\s*([^)]+?)\s*\)` (l.62), substitue `TAILLE_Q4K as u64`→144 (l.65) et `TAILLE_Q6K as u64`→210 (l.66) ; `grep -E "^$t "` (l.83, l.106) ; `printf` (l.85,91).
- Entrées-sorties : entrée `$RACINE` (llama.cpp) et `drave-core/src/gguf.rs` (l.20) ; temporaires `$TMP/tailles.c` (l.29,50), `$TMP/tailles` (l.50,53), `$TMP/gcc.err` (l.51,52), `$TMP/ggml.txt` (l.53,83,109), `$TMP/rust.txt` (l.56,75,96,106) ; C embarqué l.29-49 (boucle `for (int t = 0; t <= 64; t++)` l.33, bornes l.44 `if (bs <= 0 || bs > 1024 || ts == 0 || ts > 1024) continue;`, printf l.45).
- Constantes : bornes de type 0..64 (l.33) et bloc/taille ≤1024 (l.44) ; 144 (TAILLE_Q4K, l.65), 210 (TAILLE_Q6K, l.66) ; résumé l.111 `types confondus : $verifies · divergents : $divergents · absents du moteur : $manquants` ; avertissement l.114-118 (trous d'énumération, valeurs non initialisées) ; `head -5` (l.52) ; `exit 2` (l.22,23,52,77), `exit 1` si `divergents -gt 0` (l.120), `exit 0` (l.121).

### tools/inventaire_modeles_lourds.sh (48 lignes)
- Rôle : l.2-3 « Inventorie les modèles lourds téléchargés et CONFRONTE les poids annoncés par les descripteurs GGUF aux tailles annoncées par HuggingFace. » ; l.5-7 « C'est la vérification croisée la plus large dont on dispose : si la table des types ggml était fausse d'un seul type, l'écart apparaîtrait sur des centaines de gigaoctets. Elle ne lit que les en-têtes (le plus gros fichier fait 366 Go). » ; usage l.9 `tools/inventaire_modeles_lourds.sh [dossier]`.
- Variables : l.11 `set -u` ; l.12 cd racine ; l.13 `D=${1:-/home/stephane/Data13TB/stephane/modeles/gguf}` ; l.14 `BIN=./drave-core/target/release/drave` ; l.21 `n` (nom) ; l.22 `f` (1er gguf) ; l.25 `ligne` ; l.27 `arch` ; l.28 `nf` ; l.29 `nt` ; l.30 `go` ; Python : `m`, `par`, `total`, `f`, `k`. Aucune ENV, aucun export.
- Arguments : `$1` = dossier des modèles (l.13, défaut /home/stephane/Data13TB/stephane/modeles/gguf) ; pas d'options.
- Commandes : `timeout 600 "$BIN" "$f" --tensors` (l.25, stderr jeté) filtré `grep -E "·.*tenseurs" | head -1` (l.25) ; `ls "$d"*.gguf | head -1` (l.22) ; `cut -d' ' -f1` (l.27) ; `grep -oE "[0-9]+ fichiers"` (l.28), `"[0-9]+ tenseurs"` (l.29), `"[0-9.]+ Go de poids"` (l.30) ; `python3 - <<'PY'` (l.36) lisant le JSON et agrégeant `f['octets'] / 1e9` (l.38-47) ; rappel `cargo build --release` dans le message d'erreur (l.16).
- Entrées-sorties : dossier `$D` et un `*.gguf` par sous-dossier (l.20-22) ; `tools/manifeste_modeles_lourds.json` (l.35, ouvert l.38) ; sortie tableau stdout (en-têtes l.18-19 `modèle/architecture/fich./tenseurs/poids lus`, lignes l.31 `%10s Go`) puis bloc HuggingFace (l.45-47, total l.47).
- Constantes : `timeout 600` (l.25) ; diviseur `1e9` (l.42) ; formats `%-28s %-12s %5s %8s %12s` (l.18) et `%8.1f Go` (l.45) ; `(illisible)` (l.26) ; `exit 2` si binaire absent (l.16). Modèles : parcours dynamique, aucune liste codée en dur.

### tools/extraire_tables_ggml.sh (55 lignes)
- Rôle : l.2-3 « Extrait les tables de ggml (grilles IQ) au format Rust, ou VÉRIFIE que celles embarquées dans drave-core/src/formats.rs sont bien celles de ggml. » ; usage l.5-6 : sans argument « imprime le code Rust des tables », `verifier` « compare avec formats.rs (code 1 si écart) » ; l.8-12 : tables de 4 à 16 Ko, « une grille fausse d'une seule entrée donne des poids faux sur un seul motif de bits, donc une perplexité un peu haute et rien d'autre. La seule garantie utile est de pouvoir REDIRE d'où vient chaque valeur, et de comparer automatiquement. »
- Variables : l.13 `set -eu` ; l.14 cd racine ; l.15 `LLAMA=${DRAVE_LLAMA:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}` (ENV DRAVE_LLAMA) ; l.16 `EXE=${TMPDIR:-/tmp}/extraire_tables_ggml` (ENV TMPDIR) ; Python : `table`, `genere`, `embarque`, `noms`, `echec`, `a`, `b`, `ecarts` (l.30-53). Aucun export.
- Arguments : `$1` ; mode dump si `"${1:-}" != "verifier"` (l.21-24, `exit 0` l.23) ; mode vérification sinon ; code de sortie = `sys.exit(echec)` (l.54).
- Commandes : `gcc -O2 -I"$LLAMA/ggml/include" -I"$LLAMA/ggml/src" tools/extraire_tables_ggml.c -o "$EXE" -L"$LLAMA/build/bin" -lggml -lggml-base -Wl,-rpath,"$LLAMA/build/bin"` (l.18-19) ; `"$EXE"` (l.22) ; `"$EXE" > "$EXE.rs"` (l.26) ; `python3 - "$EXE.rs" drave-core/src/formats.rs` heredoc (l.27-54) : regex `pub static {nom}\s*:[^=]*=\s*\[(.*?)\n\];` (l.32), extraction `-?\d+` (l.35).
- Entrées-sorties : source C `tools/extraire_tables_ggml.c` (l.18) ; includes/lib de `$LLAMA` (l.18-19) ; exécutable `$EXE` (l.16,22,26) ; sortie intermédiaire `$EXE.rs` (l.26,27) ; source embarquée `drave-core/src/formats.rs` (l.27,44) ; stdout : code Rust (l.22) ou rapport de comparaison (l.44,48,51-52).
- Constantes : `-O2`, `-Wl,-rpath` (l.18-19) ; liste des tables comparées (l.39) : `IQ2XXS_GRID`, `KSIGNS_IQ2XS`, `IQ1S_GRID`, `IQ3XXS_GRID`, `KVALS_IQ4NL` ; messages « MANQUANTE » (l.44, `echec=1`), « identique (N valeurs) » (l.48), « DIVERGE : N valeur(s) sur M — premier écart » (l.51-52).

### tools/preparer_colab.sh (54 lignes)
- Rôle : l.2-4 « Prépare la répétition Colab : le dépôt en UN fichier, l'empreinte du modèle, et les commandes des deux côtés. Rien n'est envoyé nulle part — c'est vous qui téléversez, et le script vous dit quoi vérifier. » ; usage l.6 `tools/preparer_colab.sh [modèle.gguf] [port]`.
- Variables : l.7 `set -u` ; l.8 cd racine ; l.9 `MODELE=${1:-models/Qwen2.5-0.5B-Q8_0.gguf}` ; l.10 `PORT=${2:-5599}` ; l.11 `BUNDLE=/tmp/drave.bundle` ; l.22 `TAILLE=$(stat -c%s "$MODELE")` ; l.23 `EMPREINTE=$(sha256sum "$MODELE" | cut -c1-24)`. Aucune ENV, aucun export.
- Arguments : `$1` = fichier .gguf (l.9, défaut `models/Qwen2.5-0.5B-Q8_0.gguf`) ; `$2` = port (l.10, défaut 5599) ; pas d'options.
- Commandes : `git bundle create "$BUNDLE" --all` (l.14, échec → `exit 1` l.14) ; `git bundle verify "$BUNDLE" | tail -1` (l.15) ; `stat -c%s` (l.16,22) ; `du -h | cut -f1` (l.16) ; `git log --oneline -1` (l.17) ; `sha256sum | cut -c1-24` (l.23) ; here-doc l.33-41 imprimant les commandes côté local : `cd $(pwd)/drave-core && cargo build --release` (l.34), `./target/release/drave ../$MODELE --flux-serveur 0.0.0.0:$PORT --ctx 256` (l.35) ; commentaires : `ngrok tcp $PORT` (l.37), `tailscale up` (l.38), `ssh -R $PORT:localhost:$PORT votre-vps` (l.39), `ss -ltn | grep $PORT` (l.40).
- Entrées-sorties : `$MODELE` (l.9,21,23,24,28,45) ; bundle `/tmp/drave.bundle` (l.11,14,15,16,45) ; notebook `colab/Drave-reparti.ipynb` (l.46) ; stdout sections 1-5 (l.13,20,32,44,48) + bloc ATTENDU l.49-54.
- Constantes : port défaut 5599 (l.10) ; diviseur 1048576 pour les Mo (l.24) ; empreinte tronquée à 24 caractères (l.23,25) ; `--ctx 256` (l.35) ; l.26 « → à coller dans la cellule 4 du notebook (constante ATTENDU) » ; attendus l.50-53 : `écart : 0.00e0 (mode dense : le transport f32 est sans perte)`, `transport : LOTS de 64 jetons · ~229 000 octets par lot · 4 lots pour 256 jetons`, `temps : ~1,6 s de calcul local par LOT de 64 (12 couches)`, `~8 jetons/s` à 60 ms d'aller-retour ; `exit 1` (l.14).

### tools/colab_cote_local.sh (69 lignes)
- Rôle : l.2-3 « Le côté LOCAL de la démonstration Colab : un nœud moteur qui écoute, et les trois façons de le rendre joignable depuis un runtime distant. » ; usage l.5 `tools/colab_cote_local.sh [modèle.gguf] [port]` ; l.7-9 « Le script ne configure PAS le tunnel à votre place (il demande un compte, ou une machine publique) : il vérifie ce qui peut l'être, il lance le nœud, et il affiche la commande exacte à coller dans le notebook. »
- Variables : l.10 `set -u` ; l.11 cd racine ; l.12 `MODELE=${1:-models/Qwen2.5-0.5B-Q8_0.gguf}` ; l.13 `PORT=${2:-5599}` ; l.14 `BIN=./drave-core/target/release/drave` ; l.31 `NOEUD=$!` ; l.32 `i`. Aucune ENV, aucun export.
- Arguments : `$1` = modèle gguf (l.12), `$2` = port (l.13) ; pas d'options.
- Commandes : `$BIN --version` (l.19) ; `stat -c%s` (l.20) ; `sha256sum | cut -c1-24` (l.22) ; `pgrep -x drave` (l.23) ; lancement en arrière-plan `$BIN "$MODELE" --flux-serveur "0.0.0.0:$PORT" --ctx 256 > /tmp/noeud_colab.log 2>&1 &` (l.30) ; attente `for i in $(seq 1 60); do ss -ltn 2>/dev/null | grep -q ":$PORT " && break; sleep 0.5; done` (l.32) ; contrôle `ss -ltn | grep -q ":$PORT "` (l.33) ; `kill $NOEUD` (l.34,66) ; `trap ... INT TERM` (l.66) ; boucle `while kill -0 $NOEUD; do sleep 2; done` (l.67) ; `tail -3 /tmp/noeud_colab.log` (l.69) ; commandes documentées dans le here-doc l.40-54 : `ngrok tcp $PORT` (l.42), `tailscale up && tailscale ip -4` (l.45), `ssh -R $PORT:localhost:$PORT votre-vps` (l.48) ; rappel `cd drave-core && cargo build --release` (l.17).
- Entrées-sorties : `$MODELE` (l.12,18,20,22,30) ; journal `/tmp/noeud_colab.log` (l.30,34,36,69) ; stdout sections 1-4 (l.16,28,39,57) + bloc ATTENDU l.58-62 + mention notebook cellules (l.21,43,46,49).
- Constantes : port défaut 5599 (l.13) ; diviseur 1048576 (l.20) ; empreinte 24 caractères (l.22) ; `--ctx 256` (l.30) ; écoute `0.0.0.0` (l.29,30) ; 60 essais × 0,5 s ≈ 30 s (l.32) ; `sleep 2` (l.67) ; `tail -3` (l.69) ; attendus l.59-61 : `écart : 0.00e0` (critère, mode dense), `transport : LOTS de 64 jetons · 229455 octets par lot · 4 lots`, `temps : ~1,6 s de calcul local par lot` ; débit « ridicule (< 1 Mbit/s) ; c'est la LATENCE qui décide » (l.52-53) ; `exit 1` (l.17,18,34).

### tools/sprint.sh (76 lignes)
- Rôle : l.2-3 « Boxing temps réel d'un sprint de 2 h : démarrage, état, clôture avec la trame de cérémonie (revue · rétrospective · planning). » ; usage l.5-8 : `start "<objectif du sprint>"`, `status`, `close`, `list` ; l.10-12 « Le sprint vit dans `sprints/` : un fichier par sprint, et `COURANT` qui dit lequel tourne. La durée est de 2 h (SCRUM_DUREE pour un autre boxing, en secondes : SCRUM_DUREE=3600 pour une heure). »
- Variables : l.13 `set -u` ; l.14 cd racine ; l.15 `DUREE=${SCRUM_DUREE:-7200}` (ENV SCRUM_DUREE) ; l.16 `COURANT=sprints/COURANT` ; fonction `restant()` : `local s=$1` (l.21) ; branche start : `objectif` (l.28), `num` (l.29-30), `debut`/`fin` (l.31), `slug` (l.32), `fic` (l.33) ; branches status/close : `num/debut/fin` via `read -r` (l.46,56), `m` (l.47,57), `fic` (l.57). Aucun export.
- Arguments : `$1` = sous-commande via `case "${1:-status}"` (l.26) avec `start` (l.27), `status` (l.44), `close` (l.54), `list` (l.72), `*` → usage + `exit 1` (l.75) ; `$2` = objectif obligatoire pour start : `objectif=${2:?"usage : sprint.sh start \"<objectif>\""}` (l.28) ; pas de getopts/--options.
- Commandes : `date +%s` (l.18) ; `date -d "@$1" +"%H:%M"` (l.19) ; `cut -d' ' -f1 "$COURANT"` (l.30) ; `tr '[:upper:]' '[:lower:]'` + `tr -cs 'a-z0-9' '-'` + `cut -c1-40` + `sed 's/-$//'` (l.32) ; `printf` (l.34,36-40,48,58,60-67) ; `head -3 "sprints/$(printf '%02d' "$num")-"*.md | tail -1` (l.49) ; `git log --oneline --since="@$debut" | wc -l` (l.51,62) ; `git log --oneline --since="@$debut" | sed 's/^/     /'` (l.52) ; `git log --format='- \`%h\` %s' --since="@$debut" | sed 's/^/  /'` (l.63) ; `ls sprints/$(printf '%02d' "$num")-*.md` (l.57) ; `rm -f "$COURANT"` (l.69) ; `head -1 "$f"` (l.73).
- Entrées-sorties : `sprints/COURANT` (l.16,30,34,45,46,55,56,69 ; contenu `"%s %s %s\n" num debut fin`, l.34) ; fichier de sprint `sprints/%02d-%s.md` (l.33,41 écrit par `>`, puis l.68 `>>` en clôture ; retrouvé l.49,57) ; `sprints/*.md` (l.73) ; stdout : messages l.42,48-52,58,70,73.
- Constantes : `SCRUM_DUREE` défaut **7200 s = 2 h** (l.15) ; 3600 dans `restant()` (l.23) ; slug tronqué à 40 caractères (l.32) ; format `%02d` (l.33,57) ; l.37-38 « boxing de %s min » (DUREE/60) ; l.40 « **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité. » ; trame de clôture l.60-67 : « ## Revue — ce qui est livré, mesuré », `Durée : %s min (boxing %s min). Commits : %s.`, « ## Rétrospective — garder / changer » avec `- **Garder**`, `- **Changer**`, `- **Doute**`, « ## Planning — le sprint suivant » avec tableau `| # | chantier | critère de succès |` ; `exit 0` (l.45,55), `exit 1` (l.75).

REMARQUES TRANSVERSALES : aucun des 8 scripts n'invoque `nvidia-smi`, `convert_hf_to_gguf.py`, `cargo run` ni `ssh` en exécution réelle (`ssh -R`/`ngrok`/`tailscale` ne figurent que dans des here-docs d'instructions : preparer_colab.sh l.37-40, colab_cote_local.sh l.42-48) ; `cargo` n'apparaît qu'en `cargo test --release` réel (portes.sh l.39) et en conseil `cargo build --release` (inventaire l.16, preparer_colab l.34, colab_cote_local l.17). Variables d'environnement effectivement lues : DRAVE_MODELES (portes_formats.sh:19), DRAVE_LLAMA (portes_formats.sh:20, extraire_tables_ggml.sh:15), REF_GGML_BLOC (portes_formats.sh:21), TMPDIR (extraire_tables_ggml.sh:16), SCRUM_DUREE (sprint.sh:15) ; LD_LIBRARY_PATH posé inline (verifier_table_types.sh:53) ; IFS modifié (portes_formats.sh:23) ; aucun `export` dans les 8 fichiers. Fichiers partagés entre scripts : tools/ref_ggml_bloc.c + /tmp/ref_ggml_bloc (portes.sh:74-75 ↔ portes_formats.sh:15,48-50), tools/verifier_formats.py (portes_formats.sh:22), tools/extraire_tables_ggml.c (extraire_tables_ggml.sh:18), drave-core/src/formats.rs (extraire_tables_ggml.sh:27), drave-core/src/gguf.rs (verifier_table_types.sh:20), tools/manifeste_modeles_lourds.json (inventaire_modeles_lourds.sh:35,38), /tmp/noeud_colab.log et port 5599 (preparer_colab.sh ↔ colab_cote_local.sh). Aucun fichier n'a été modifié (lecture seule stricte respectée).

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "offset": 640, "limit": 180}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
640:             "--logits-bin" => { o.logits_bin = Some(suivant(i).clone()); 2 }
641:             "--neurones-sortie" => { o.neurones_sortie = Some(suivant(i).clone()); 2 }
642:             "--harmony-contexte" => { o.harmony_contexte = Some(suivant(i).clone()); 2 }
643:             "--patch" => { o.patch = Some(suivant(i).clone()); 2 }
644:             "--n" => { o.n = suivant(i).parse().unwrap(); 2 }
645:             "--temp" => { o.temp = suivant(i).parse().unwrap(); 2 }
646:             "--top-p" => { o.top_p = suivant(i).parse().unwrap(); 2 }
647:             "--topk" => { o.topk = suivant(i).parse().unwrap(); 2 }
648:             "--rep-penalty" => { o.rep_pen = suivant(i).parse().unwrap(); 2 }
649:             "--hist" => { o.hist = suivant(i).parse().unwrap(); 2 }
650:             "--ctx" => { o.ctx = suivant(i).parse().unwrap(); o.ctx_impose = true; 2 }
651:             "--threads" => { o.threads = suivant(i).parse().unwrap(); o.threads_impose = true; 2 }
652:             "--abits" => { o.abits = suivant(i).parse().unwrap(); o.abits_impose = true; 2 }
653:      
… [10087 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'a\\.as_str()\\|match a\\b\\|=> {' drave-core/src/main.rs | sed -n '1,40p'; echo \"=== functions in main.rs ===\"; grep -n '^fn \\|^pub fn \\|^    fn ' drave-core/src/main.rs | head -60", "description": "Explore main.rs parse … [13 caractères tronqués]`

  ```
140:            "--matrix" if i + 1 < args.len() => { matrix = args[i + 1].clone(); i += 2; }
141:            "--threads" if i + 1 < args.len() => {
604:            "--infer" => { o.infer = true; 1 }
605:            "--ppl" => { o.ppl = true; o.ids_file = Some(suivant(i).clone()); 2 }
606:            "--ppl-texte" => { o.ppl = true; o.ppl_texte = true;
608:            "--plan" => { o.plan = true; 1 }
609:            "--tokenize" => { o.tokenize = true; 1 }
610:            "--gpu-banc" => { o.gpu_banc = true; 1 }
611:            "--banc-kv" => { o.banc_kv = suivant(i).parse().unwrap(); 2 }
612:            "--banc-topk" => { o.banc_topk = suivant(i).parse().unwrap(); 2 }
613:            "--banc-mla" => { o.banc_mla = Some(suivant(i).clone()); 2 }
614:            "--tensors" => { o.tensors = true; 1 }
615:            "--trace-flux" => { o.trace_flux = Some(suivant(i).clone()); 2 }
616:            "--flux-forcer" => { o.flux_forcer = Some(suivant(i).clone()); 2 }
617:            "--flux-serveur" => { o.flux_serveur = Some(suivant(i).clone()); 2 }
618:            "--options-actives" => { o.options_actives = true; 1 }
619:            "--options-strict" => { o.options_strict = true; 1 }
6
… [5170 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 70, "offset": 575}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
575:     texte: Option<String>, fichier: Option<String>, sortie: Option<String>,
576: }
577: 
578: /// Analyse la ligne de commande UNE fois. Les drapeaux à valeur consomment
579: /// l'argument suivant (`i += 2`) ; les drapeaux booléens non (`i += 1`).
580: fn analyser(args: &[String]) -> Options {
581:     let mut o = Options {
582:         n: 32, temp: 0.0, top_p: 1.0, hist: 64, hebb_q: 0.1,
583:         hebb_out: String::from("hebb.bin"), keep: 1.0, abits: 8,
584:         auto: true, limit: usize::MAX,
585:         matrix: String::from("blk.0.ffn_gate.weight"),
586:         ..Default::default()
587:     };
588:     let cpu = engine::coeurs_physiques();
589:     o.ctx = 512;
590:     o.threads = cpu.max(1);
591:     let suivant = |i: usize| -> &String {
592:         args.get(i + 1).unwrap_or_else(|| panic!("{} attend une valeur", args[i]))
593:     };
594:     let mut i = 2;
595:     while i < args.len() {
596:         // CHAQUE branche rend le nombre d'arguments consommés (1 pour un
597:         // drapeau booléen, 2 pour un drapeau à valeur). Un `i += 2` global
598: 
… [3436 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'usage\\|Usage\\|aide\\|Aide\\|help' drave-core/src/main.rs | head -40", "description": "Find usage/help text in main.rs"}`

  ```
3://! Usage :
51:        eprintln!("usage: drave <modele.gguf|dossier-de-clusters> [--matrix NOM] [--threads N]");
887:            for (role, texte) in [("system", "You are a helpful assistant."), ("user", p.as_str())] {
1175:/// de noyau aide, la mesure par jeton mélangeant tête, attention et
1742:    // celles de V4.1 par défaut : un plan générique n'aide personne.
4156:/// l'usage réel : le modèle *écrit* le texte).
4171:        v.extend(tk.encode("You are a helpful assistant."));
  ```

### 👤 Utilisateur

Background subagent dcaa24d6-0017-4382-be21-8244c0fb9b7a finished and will do no further work unless you send it more.
Its closing message:
⏵ Report sent to parent; delivering the same findings here.

### tools/portes.sh (132 lignes)
- **Rôle** : l.2-6 « Les portes du dépôt, en une commande. » / « Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien : chaque porte est comparée à la valeur ATTENDUE, et le script sort en erreur si l'une diverge. Les valeurs sont celles publiées dans les rapports. » Usage l.8-9 : `tools/portes.sh` (toutes) ou `tools/portes.sh rapide` (« sans gpt-oss (le seul qui prenne ~20 min) »).
- **Variables** : l.11 `set -u` ; l.12 `cd "$(dirname "$0")/.."` ; l.13 `D=./drave-core/target/release/drave` ; l.14 `RAPIDE=${1:-}` ; l.15 `ECHEC=0` ; l.39 `sortie` ; l.40 `n` ; l.41 `ko` ; l.51/58/64/75/89/108/119 `v`/`r`/`p` ; l.56 `A=/home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters-v2` ; l.65 `att=$(nproc); att=$((att / 2))` ; l.95 `M=/home/stephane/Data13TB/stephane/modeles/gguf` ; l.106 `O=.../gpt-oss-120b-MXFP4.gguf`. Aucune ENV DRAVE_*/MODEL* lue, aucun `export`.
- **Arguments** : `$1` → `RAPIDE` (l.14), seule valeur testée `rapide` (l.71, l.105). Pas de getopts. Paramètres internes : `$1/$2/$3` = nom/attendu/obtenu dans `compare()` (l.19-25) ; `$1/$2/$3` = nom/modèle/motif dans `route()` (l.87-94, appels l.96-99).
- **Commandes** : `cargo test --release` dans `drave-core` (l.39) ; `command -v gcc` (l.74) ; `bash tools/portes_formats.sh` sous `timeout 1800` (l.75) ; `nproc` (l.65) ; `$D` avec `--ppl /tmp/ids_qwen.txt --ctx 256 --abits 16 --threads 16 --limit 512 --dense` (l.51-52), `--ppl ... --ctx 64 --limit 8 --dense --threads 8 --lot 1` (l.58-59), `--materiel` (l.64), `--config` (l.89, l.108), `--tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_oss_512.txt` (l.116), `--ppl /tmp/ids_oss_512.txt --ctx 256 --dense --threads 16 --limit 512` (l.119-120) ; `timeout` 600/900/1800/2400 (l.51,58,75,119) ; pipes `grep -oE`/`head`/`cut` (l.31,40,41,46,64,89,108).
- **Entrées-sorties** : `models/Qwen2.5-0.5B-Q8_0.gguf` (l.51,64) ; `/tmp/ids_qwen.txt` (l.51,58) ; `$A` clusters Qwen3-30B (l.56,58) ; 4 GGUF sous `$M` (l.96-99) ; `$O` gpt-oss (l.106,108,116,119) ; `/tmp/wt2_txt.txt` (l.115) alimenté par `data/wikitext2_test.txt` (`head -c 20000`, l.115) ; `/tmp/ids_oss_512.txt` (l.114,116,118,119) ; `tools/portes_formats.sh` (l.74-75).
- **Constantes** : seuils tests `-ge 48` (l.42) et `ko -eq 0` (l.42) ; timeouts 600/900/1800/2400 (l.51,58,75,119) ; `--ctx 256` (l.51,119), `--ctx 64` (l.58) ; `--abits 16` (l.52) ; `--threads 16` (l.52,120), `8` (l.59) ; `--limit 512` (l.52,120), `8` (l.58) ; `--lot 1` (l.59) ; attendus `19.3885` (l.53), `799.8557` (l.60, « origine : 799,8557 »), `15.6017` (l.121) ; commentaire l.29-30 (17,431 = fenêtre 1, instrument faux) ; `head -5` (l.46) ; threads `>0` et `<= nproc/2` (l.65-66) ; motif formats `*"0 divergence(s), 0 absent(s)"*` (l.77) ; routages attendus `sigmoïde` (l.96,97), `racine de softplus` (l.98), `softmax` (l.99) ; gpt-oss `*": oui"*` (l.110) ; `exit 2` (l.17), `exit $ECHEC` (l.132). Modèles codés en dur : GLM-5.3-UD-IQ1_S-00001-of-00006 (l.96), Kimi-K2.7-Code-UD-IQ1_M-00001-of-00008 (l.97), DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003 (l.98), Qwen3-235B-A22B-Instruct-2507-Q2_K-00001-of-00002 (l.99).

### tools/portes_formats.sh (74 lignes)
- **Rôle** : l.2 « Portes des FORMATS : chaque déquantificateur comparé à libggml, bloc par bloc. » ; usage l.4 `tools/portes_formats.sh [type ...]` ; l.6-13 : cinq premiers essais faux (IQ2_XXS, IQ1_M, Q2_K, Q5_K, Q6_K), « refuse de « passer » si le témoin a disparu du disque — un test qui saute est un test qui ne dit rien. » ; l.15 « La référence est liée à libggml (voir tools/ref_ggml_bloc.c). »
- **Variables** : l.16 `set -u` ; l.17 cd racine ; l.18 `RACINE=$PWD` ; l.19 `MODELES=${DRAVE_MODELES:-/home/stephane/Data13TB/stephane/modeles/gguf}` (**DRAVE_MODELES**) ; l.20 `LLAMA=${DRAVE_LLAMA:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}` (**DRAVE_LLAMA**) ; l.21 `REF=${REF_GGML_BLOC:-/tmp/ref_ggml_bloc}` (**REF_GGML_BLOC**) ; l.22 `VERIF=tools/verifier_formats.py` ; l.23 `IFS=$'\n'` ; l.25 `ok=0; ko=0; abs=0` ; l.27 `BATTERIE` ; l.53 `filtre="${*:-}"` ; l.55-58 `lib/fich/tens/typ` ; l.65-66 `sortie`/`sortie2`. Aucun export.
- **Arguments** : tous les positionnels → `filtre="${*:-}"` (l.53), testé contre le libellé (l.59 `if [ -n "$filtre" ] && ! echo " $filtre " | grep -q " $lib "; then continue; fi`) ; valeurs = F32, F16, Q4_0, Q5_0, Q8_0, Q2_K, Q3_K, Q4_K, Q5_K, Q6_K, IQ2_XXS, IQ3_XXS, IQ1_S, IQ4_XS, IQ1_M, BF16, MXFP4. Pas de getopts/--options.
- **Commandes** : `gcc -O2 -I"$LLAMA/ggml/include" -I"$LLAMA/ggml/src" tools/ref_ggml_bloc.c -o "$REF" -L"$LLAMA/build/bin" -lggml -lggml-base -Wl,-rpath,"$LLAMA/build/bin"` (l.49-50, recompil si `-nt`, l.48 ; `|| exit 2` l.50) ; `python3 "$VERIF" "$fich" "$tens" 0` (l.65) et `... 7` (l.66), `tail -1` ; `cut -d'|' -f1..4 | xargs` (l.55-58) ; exigence `"CONCORDE"` sur les deux blocs (l.67).
- **Entrées-sorties** : 17 modèles sous `$MODELES` + `$RACINE/models/Qwen2.5-0.5B-Q4_0.gguf` (l.28-44) ; tenseurs : blk.0.attn_norm.weight (l.28), token_embd.weight (l.29-33,35), output.weight (l.32), blk.0.attn_output.weight (l.34), blk.0.ffn_down.weight (l.36,37), blk.0.ffn_gate_exps.weight (l.38,42), blk.1.ffn_down_exps.weight (l.39), blk.3.ffn_gate_exps.weight (l.40), blk.11.ffn_down_exps.weight (l.41), blk.0.ffn_gate_inp.weight (l.43), blk.0.ffn_down_exps.weight (l.44) ; témoin `$REF` (l.21,48,49) ; ligne finale l.73 `formats : $ok concorde(s), $ko divergence(s), $abs absent(s)` ; statut l.74 `[ $ko -eq 0 ] && [ $abs -eq 0 ]`.
- **Constantes** : type ggml par entrée : F32=0 (l.28), F16=1 (l.29), Q4_0=2 (l.30), Q5_0=6 (l.31), Q8_0=8 (l.32), Q2_K=10 (l.33), Q3_K=11 (l.34), Q4_K=12 (l.35), Q5_K=13 (l.36), Q6_K=14 (l.37), IQ2_XXS=16 (l.38), IQ3_XXS=18 (l.39), IQ1_S=19 (l.40), IQ4_XS=23 (l.41), IQ1_M=29 (l.42), BF16=30 (l.43), MXFP4=39 (l.44) ; blocs testés 0 et 7 (l.65-66) ; modèles : codestral-22b-v0.1-q4_k_m.gguf (l.28,35), bge-m3-FP16.gguf (l.29), qwen2.5-0.5b-instruct-q4_k_m.gguf (l.31,32,37), Qwen3-235B-A22B-Q2_K/...-00001-of-00002.gguf (l.33,34), Muse-Glimmer-30B-AD-Q4_K_M.gguf (l.36), DeepSeek-V4.1-Flash-Q2/DeepSeek-V4.1-Flash-Q2.gguf (l.38), Kimi-K2.7-Code-UD-IQ1_M-00002-of-00008.gguf (l.39), GLM-5.3-UD-IQ1_S-00002-of-00006.gguf (l.40), GLM-5.3-Flash-UD-IQ1_S-00002-of-00003.gguf (l.41), DeepSeek-V4-Flash-UD-IQ1_M-00002-of-00003.gguf (l.42,43), gpt-oss-120b-MXFP4.gguf (l.44).

### tools/verifier_table_types.sh (121 lignes)
- **Rôle** : l.2 « Confronte la table des tailles de types ggml du moteur à celle de `libggml`. » ; l.6-8 (« un inventaire a annoncé 8,56 Go pour 86,9 Go de fichiers (les experts en `iq1_m`) ») ; usage l.13 `tools/verifier_table_types.sh [chemin de llama.cpp]` ; l.15 « Rend 0 si les tables concordent sur tous les types testés, 1 sinon. »
- **Variables** : l.17 `set -u` ; l.18 cd racine ; l.19 `RACINE=${1:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}` ; l.20 `SRC=drave-core/src/gguf.rs` ; l.25 `TMP=$(mktemp -d)` ; l.26 `trap 'rm -rf "$TMP"' EXIT` ; l.81 `manquants=0; divergents=0; verifies=0` ; l.104 `inconnus=""` ; boucles `t`/`bloc`/`taille`/`ligne` (l.82-96, 105-109) ; `$2`/`$3` l.90-91 viennent de `set -- $ligne` (l.89), pas de la CLI. Aucune ENV, aucun export.
- **Arguments** : `$1` = chemin llama.cpp (l.19, défaut /home/.../llama.cpp) ; pas d'options.
- **Commandes** : `gcc -I"$RACINE/ggml/include" -I"$RACINE/ggml/src" "$TMP/tailles.c" -o "$TMP/tailles" -L"$RACINE/build/bin" -lggml -lggml-base` avec `2>"$TMP/gcc.err"` (l.50-51) ; `sed 's/^/  /' ... | head -5` (l.52) ; `LD_LIBRARY_PATH="$RACINE/build/bin" "$TMP/tailles" | sort -n > "$TMP/ggml.txt"` (l.53) ; `python3 - "$SRC"` heredoc (l.56-73) : isole `pub fn octets_tensor_opt` (l.60-61), regex `(\d+)(?:u64)?\s*=>\s*\(\s*(\d+)(?:u64)?\s*,\s*([^)]+?)\s*\)` (l.62), substitue `TAILLE_Q4K as u64`→144 (l.65), `TAILLE_Q6K as u64`→210 (l.66) ; `grep -E "^$t "` (l.83,106) ; printf l.85,91.
- **Entrées-sorties** : `$RACINE` + `drave-core/src/gguf.rs` (l.20) ; temporaires `$TMP/tailles.c` (l.29,50), `$TMP/tailles` (l.50,53), `$TMP/gcc.err` (l.51,52), `$TMP/ggml.txt` (l.53,83,109), `$TMP/rust.txt` (l.56,75,96,106) ; C embarqué l.29-49 (boucle `for (int t = 0; t <= 64; t++)` l.33 ; bornes l.44 `if (bs <= 0 || bs > 1024 || ts == 0 || ts > 1024) continue;` ; `printf("%d %lld %zu\n", t, (long long)bs, ts)` l.45).
- **Constantes** : 0..64 (l.33) ; ≤1024 (l.44) ; 144 (l.65), 210 (l.66) ; résumé l.111 `types confondus : $verifies · divergents : $divergents · absents du moteur : $manquants` ; avertissement l.114-118 (trous d'énumération, valeurs non initialisées) ; `head -5` (l.52) ; `exit 2` (l.22,23,52,77), `exit 1` si `divergents -gt 0` (l.120), `exit 0` (l.121).

### tools/inventaire_modeles_lourds.sh (48 lignes)
- **Rôle** : l.2-3 « Inventorie les modèles lourds téléchargés et CONFRONTE les poids annoncés par les descripteurs GGUF aux tailles annoncées par HuggingFace. » ; l.5-7 « si la table des types ggml était fausse d'un seul type, l'écart apparaîtrait sur des centaines de gigaoctets. Elle ne lit que les en-têtes (le plus gros fichier fait 366 Go). » ; usage l.9 `tools/inventaire_modeles_lourds.sh [dossier]`.
- **Variables** : l.11 `set -u` ; l.12 cd racine ; l.13 `D=${1:-/home/stephane/Data13TB/stephane/modeles/gguf}` ; l.14 `BIN=./drave-core/target/release/drave` ; l.21 `n` ; l.22 `f` ; l.25 `ligne` ; l.27 `arch` ; l.28 `nf` ; l.29 `nt` ; l.30 `go` ; Python : `m`, `par`, `total`, `f`, `k`. Aucune ENV, aucun export.
- **Arguments** : `$1` = dossier des modèles (l.13) ; pas d'options.
- **Commandes** : `timeout 600 "$BIN" "$f" --tensors` (l.25, stderr jeté) filtré `grep -E "·.*tenseurs" | head -1` (l.25) ; `ls "$d"*.gguf | head -1` (l.22) ; `cut -d' ' -f1` (l.27) ; `grep -oE "[0-9]+ fichiers"` (l.28), `"[0-9]+ tenseurs"` (l.29), `"[0-9.]+ Go de poids"` (l.30) ; `python3 - <<'PY'` (l.36) agrégeant `f['octets'] / 1e9` (l.38-47) ; message d'erreur `cargo build --release` (l.16).
- **Entrées-sorties** : `$D` + un `*.gguf` par sous-dossier (l.20-22) ; `tools/manifeste_modeles_lourds.json` (l.35, ouvert l.38) ; stdout : en-têtes l.18-19, lignes l.31 (`%10s Go`), bloc HuggingFace l.45-47.
- **Constantes** : `timeout 600` (l.25) ; `1e9` (l.42) ; formats `%-28s %-12s %5s %8s %12s` (l.18), `%8.1f Go` (l.45) ; `(illisible)` (l.26) ; `exit 2` (l.16).

### tools/extraire_tables_ggml.sh (55 lignes)
- **Rôle** : l.2-3 « Extrait les tables de ggml (grilles IQ) au format Rust, ou VÉRIFIE que celles embarquées dans drave-core/src/formats.rs sont bien celles de ggml. » ; usage l.5-6 (dump sans argument ; `verifier` « compare avec formats.rs (code 1 si écart) ») ; l.8-12 : tables de 4 à 16 Ko, « une grille fausse d'une seule entrée donne des poids faux sur un seul motif de bits, donc une perplexité un peu haute et rien d'autre. »
- **Variables** : l.13 `set -eu` ; l.14 cd racine ; l.15 `LLAMA=${DRAVE_LLAMA:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}` (**DRAVE_LLAMA**) ; l.16 `EXE=${TMPDIR:-/tmp}/extraire_tables_ggml` (**TMPDIR**) ; Python : `table`, `genere`, `embarque`, `noms`, `echec`, `a`, `b`, `ecarts`. Aucun export.
- **Arguments** : `$1` ; mode dump si `"${1:-}" != "verifier"` (l.21-24, `exit 0` l.23) ; sinon vérification ; code de sortie `sys.exit(echec)` (l.54).
- **Commandes** : `gcc -O2 -I"$LLAMA/ggml/include" -I"$LLAMA/ggml/src" tools/extraire_tables_ggml.c -o "$EXE" -L"$LLAMA/build/bin" -lggml -lggml-base -Wl,-rpath,"$LLAMA/build/bin"` (l.18-19) ; `"$EXE"` (l.22) ; `"$EXE" > "$EXE.rs"` (l.26) ; `python3 - "$EXE.rs" drave-core/src/formats.rs` heredoc (l.27-54), regex `pub static {nom}\s*:[^=]*=\s*\[(.*?)\n\];` (l.32), extraction `-?\d+` (l.35).
- **Entrées-sorties** : `tools/extraire_tables_ggml.c` (l.18) ; includes/lib de `$LLAMA` (l.18-19) ; exécutable `$EXE` (l.16,22,26) ; `$EXE.rs` (l.26,27) ; `drave-core/src/formats.rs` (l.27,44) ; stdout : code Rust (l.22) ou rapport (l.44,48,51-52).
- **Constantes** : `-O2`, `-Wl,-rpath` (l.18-19) ; tables comparées l.39 : `IQ2XXS_GRID`, `KSIGNS_IQ2XS`, `IQ1S_GRID`, `IQ3XXS_GRID`, `KVALS_IQ4NL` ; messages « MANQUANTE » (l.44), « identique (N valeurs) » (l.48), « DIVERGE : N valeur(s) sur M — premier écart » (l.51-52).

### tools/preparer_colab.sh (54 lignes)
- **Rôle** : l.2-4 « Prépare la répétition Colab : le dépôt en UN fichier, l'empreinte du modèle, et les commandes des deux côtés. Rien n'est envoyé nulle part — c'est vous qui téléversez, et le script vous dit quoi vérifier. » ; usage l.6 `tools/preparer_colab.sh [modèle.gguf] [port]`.
- **Variables** : l.7 `set -u` ; l.8 cd racine ; l.9 `MODELE=${1:-models/Qwen2.5-0.5B-Q8_0.gguf}` ; l.10 `PORT=${2:-5599}` ; l.11 `BUNDLE=/tmp/drave.bundle` ; l.22 `TAILLE=$(stat -c%s "$MODELE")` ; l.23 `EMPREINTE=$(sha256sum "$MODELE" | cut -c1-24)`. Aucune ENV, aucun export.
- **Arguments** : `$1` = .gguf (l.9) ; `$2` = port (l.10, défaut 5599) ; pas d'options.
- **Commandes** : `git bundle create "$BUNDLE" --all` (l.14, échec → `exit 1`) ; `git bundle verify "$BUNDLE" | tail -1` (l.15) ; `stat -c%s` (l.16,22) ; `du -h | cut -f1` (l.16) ; `git log --oneline -1` (l.17) ; `sha256sum | cut -c1-24` (l.23) ; here-doc l.33-41 : `cd $(pwd)/drave-core && cargo build --release` (l.34), `./target/release/drave ../$MODELE --flux-serveur 0.0.0.0:$PORT --ctx 256` (l.35) ; commentaires : `ngrok tcp $PORT` (l.37), `tailscale up` (l.38), `ssh -R $PORT:localhost:$PORT votre-vps` (l.39), `ss -ltn | grep $PORT` (l.40).
- **Entrées-sorties** : `$MODELE` (l.9,21,23,24,28,45) ; `/tmp/drave.bundle` (l.11,14,15,16,45) ; `colab/Drave-reparti.ipynb` (l.46) ; stdout sections 1-5 (l.13,20,32,44,48) + bloc ATTENDU l.49-54.
- **Constantes** : port 5599 (l.10) ; 1048576 (l.24) ; empreinte 24 car. (l.23,25) ; `--ctx 256` (l.35) ; l.26 « à coller dans la cellule 4 du notebook (constante ATTENDU) » ; attendus l.50-53 : `écart : 0.00e0 (mode dense : le transport f32 est sans perte)`, `LOTS de 64 jetons · ~229 000 octets par lot · 4 lots pour 256 jetons`, `~1,6 s de calcul local par LOT de 64 (12 couches)`, `~8 jetons/s` à 60 ms ; `exit 1` (l.14).

### tools/colab_cote_local.sh (69 lignes)
- **Rôle** : l.2-3 « Le côté LOCAL de la démonstration Colab : un nœud moteur qui écoute, et les trois façons de le rendre joignable depuis un runtime distant. » ; usage l.5 ; l.7-9 « Le script ne configure PAS le tunnel à votre place (il demande un compte, ou une machine publique) : il vérifie ce qui peut l'être, il lance le nœud, et il affiche la commande exacte à coller dans le notebook. »
- **Variables** : l.10 `set -u` ; l.11 cd racine ; l.12 `MODELE=${1:-models/Qwen2.5-0.5B-Q8_0.gguf}` ; l.13 `PORT=${2:-5599}` ; l.14 `BIN=./drave-core/target/release/drave` ; l.31 `NOEUD=$!` ; l.32 `i`. Aucune ENV, aucun export.
- **Arguments** : `$1` = modèle gguf (l.12) ; `$2` = port (l.13) ; pas d'options.
- **Commandes** : `$BIN --version` (l.19) ; `stat -c%s` (l.20) ; `sha256sum | cut -c1-24` (l.22) ; `pgrep -x drave` (l.23) ; `$BIN "$MODELE" --flux-serveur "0.0.0.0:$PORT" --ctx 256 > /tmp/noeud_colab.log 2>&1 &` (l.30) ; `for i in $(seq 1 60); do ss -ltn 2>/dev/null | grep -q ":$PORT " && break; sleep 0.5; done` (l.32) ; `ss -ltn | grep -q ":$PORT "` (l.33) ; `kill $NOEUD` (l.34,66) ; `trap ... INT TERM` (l.66) ; `while kill -0 $NOEUD; do sleep 2; done` (l.67) ; `tail -3 /tmp/noeud_colab.log` (l.69) ; here-doc l.40-54 : `ngrok tcp $PORT` (l.42), `tailscale up && tailscale ip -4` (l.45), `ssh -R $PORT:localhost:$PORT votre-vps` (l.48) ; conseil `cd drave-core && cargo build --release` (l.17).
- **Entrées-sorties** : `$MODELE` (l.12,18,20,22,30) ; `/tmp/noeud_colab.log` (l.30,34,36,69) ; stdout sections 1-4 (l.16,28,39,57) + bloc ATTENDU l.58-62 ; mentions notebook (l.21,43,46,49).
- **Constantes** : port 5599 (l.13) ; 1048576 (l.20) ; empreinte 24 car. (l.22) ; `--ctx 256` (l.30) ; `0.0.0.0` (l.29,30) ; 60×0,5 s ≈ 30 s (l.32) ; `sleep 2` (l.67) ; `tail -3` (l.69) ; attendus l.59-61 : `écart : 0.00e0`, `LOTS de 64 jetons · 229455 octets par lot · 4 lots`, `~1,6 s de calcul local par lot` ; « < 1 Mbit/s », « c'est la LATENCE qui décide » (l.52-53) ; `exit 1` (l.17,18,34).

### tools/sprint.sh (76 lignes)
- **Rôle** : l.2-3 « Boxing temps réel d'un sprint de 2 h : démarrage, état, clôture avec la trame de cérémonie (revue · rétrospective · planning). » ; usage l.5-8 (`start "<objectif du sprint>"`, `status`, `close`, `list`) ; l.10-12 « Le sprint vit dans `sprints/` : un fichier par sprint, et `COURANT` qui dit lequel tourne. La durée est de 2 h (SCRUM_DUREE pour un autre boxing, en secondes : SCRUM_DUREE=3600 pour une heure). »
- **Variables** : l.13 `set -u` ; l.14 cd racine ; l.15 `DUREE=${SCRUM_DUREE:-7200}` (**SCRUM_DUREE**) ; l.16 `COURANT=sprints/COURANT` ; `restant()` : `local s=$1` (l.21) ; start : `objectif` (l.28), `num` (l.29-30), `debut`/`fin` (l.31), `slug` (l.32), `fic` (l.33) ; status/close : `num/debut/fin` via `read -r` (l.46,56), `m` (l.47,57), `fic` (l.57). Aucun export.
- **Arguments** : `$1` = sous-commande via `case "${1:-status}"` (l.26) : `start` (l.27), `status` (l.44), `close` (l.54), `list` (l.72), `*` → usage + `exit 1` (l.75) ; `$2` = objectif obligatoire pour start (l.28 `objectif=${2:?"usage : sprint.sh start \"<objectif>\""}`) ; pas de getopts/--options.
- **Commandes** : `date +%s` (l.18) ; `date -d "@$1" +"%H:%M"` (l.19) ; `cut -d' ' -f1 "$COURANT"` (l.30) ; `tr`/`cut -c1-40`/`sed 's/-$//'` (l.32) ; `printf` (l.34,36-40,48,58,60-67) ; `head -3 "sprints/$(printf '%02d' "$num")-"*.md | tail -1` (l.49) ; `git log --oneline --since="@$debut" | wc -l` (l.51,62) ; `git log --oneline --since="@$debut" | sed 's/^/     /'` (l.52) ; `git log --format='- \`%h\` %s' --since="@$debut" | sed 's/^/  /'` (l.63) ; `ls sprints/$(printf '%02d' "$num")-*.md` (l.57) ; `rm -f "$COURANT"` (l.69) ; `head -1 "$f"` (l.73).
- **Entrées-sorties** : `sprints/COURANT` (l.16,30,34,45,46,55,56,69 ; contenu `"%s %s %s\n" num debut fin`, l.34) ; `sprints/%02d-%s.md` (l.33,41 `>`, l.68 `>>` ; relu l.49,57) ; `sprints/*.md` (l.73) ; stdout l.42,48-52,58,70,73.
- **Constantes** : `SCRUM_DUREE` défaut 7200 s = 2 h (l.15) ; 3600 (l.23) ; slug 40 car. (l.32) ; `%02d` (l.33,57) ; « boxing de %s min » (l.37-38) ; l.40 « **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité. » ; trame l.60-67 (« ## Revue — ce qui est livré, mesuré », `Durée : %s min (boxing %s min). Commits : %s.`, « ## Rétrospective — garder / changer » avec `- **Garder**`, `- **Changer**`, `- **Doute**`, « ## Planning — le sprint suivant », tableau `| # | chantier | critère de succès |`) ; `exit 0` (l.45,55), `exit 1` (l.75).

**Remarques transversales** : aucun des 8 scripts n'invoque `nvidia-smi`, `convert_hf_to_gguf.py`, `cargo run` ni `ssh` en exécution réelle (`ssh -R`/`ngrok`/`tailscale` ne figurent que dans des here-docs d'instructions : preparer_colab.sh l.37-40, colab_cote_local.sh l.42-48) ; `cargo` n'apparaît qu'en `cargo test --release` réel (portes.sh l.39) et en conseil `cargo build --release` (inventaire l.16, preparer_colab l.34, colab_cote_local l.17). ENV réellement lues : DRAVE_MODELES (portes_formats.sh:19), DRAVE_LLAMA (portes_formats.sh:20, extraire_tables_ggml.sh:15), REF_GGML_BLOC (portes_formats.sh:21), TMPDIR (extraire_tables_ggml.sh:16), SCRUM_DUREE (sprint.sh:15) ; LD_LIBRARY_PATH inline (verifier_table_types.sh:53) ; IFS modifié (portes_formats.sh:23) ; **aucun `export`** dans les 8 fichiers. Fichiers partagés : tools/ref_ggml_bloc.c et /tmp/ref_ggml_bloc (portes.sh:74-75 ↔ portes_formats.sh:15,48-50), tools/verifier_formats.py (portes_formats.sh:22), tools/extraire_tables_ggml.c (extraire_tables_ggml.sh:18), drave-core/src/formats.rs (extraire_tables_ggml.sh:27), drave-core/src/gguf.rs (verifier_table_types.sh:20), tools/manifeste_modeles_lourds.json (inventaire_modeles_lourds.sh:35,38), /tmp/noeud_colab.log + port 5599 (preparer_colab.sh ↔ colab_cote_local.sh). Aucun fichier modifié — lecture seule stricte respectée ; rapport transmis à l'agent parent `f2de810a-b765-444d-b3cc-d8fce1ba2105`.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 140, "offset": 1}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 120, "offset": 460}`

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
11: /// Variables d'environnement que le moteur lit, **sans** le préfixe `DRAVE_`.
12: ///
13: /// Sert à traduire un ancien nom `QT_*` resté dans un script, et à rien d'autre.
14: /// Le test `les_vars_lues_sont_completes` vérifie cette liste contre le source :
15: /// une variable lue mais absente d'ici rendrait le message muet, et une variable
16: /// listée mais jamais lue annoncerait une option qui n'existe pas.
17: const VARS_LUES: &[&str] = &[
18:     "BANC_KV_DEBUG", "BANC_KV_GPU_SEUL", "BANC_KV_GRAD", "BANC_KV_K0",
19:     "BANC_KV_KUNIT", "BANC_KV_UNIT", "BANC_KV_V1", "BANC_SANS_PUITS",
20:     "CLUSTERS", "DEBUG_ETAT", "DEBUG_FLUX
… [7322 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
460:         let cpu = engine::coeurs_physiques();
461:         cpu.max(1)
462:     }
463: }
464: 
465: /// **Toutes** les options de la ligne de commande, dans une seule structure.
466: ///
467: /// Les modes (inférence, perplexité, plan, tokenize) la remplissent par la MÊME
468: /// boucle : c'est la seule façon d'éviter qu'un drapeau fonctionne dans un mode
469: /// et pas dans l'autre. Le bug est arrivé quatre fois — `--pin`, `--moe-topk`,
470: /// `--attn-window` et `--attn-sinks` ont chacun été « analysés mais jamais
471: /// appliqués » dans un mode au moins, et un drapeau en dernière position était
472: /// ignoré à cause du pas de deux.
473: #[derive(Default)]
474: struct Options {
475:     // --- sélection du mode
476:     infer: bool, ppl: bool, plan: bool, tokenize: bool, gpu_banc: bool,
477:     /// Banc du KV déporté : nombre de clés à faire tenir en VRAM.
478:     banc_kv: usize,
479:     /// Banc des SCORES d'attention : nombre de clés à noter (noyau 1 du top-k).
480:     banc_topk: usize,
481:     /// Banc MLA : écrit les logits `(n_pos × vocab)` en f32 p
… [5856 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== env::var occurrences by file ===\" && grep -rn 'env::var\\|var_os\\|env!(\"' drave-core/src/*.rs | sed 's/^\\(.\\{160\\}\\).*/\\1/' ", "description": "List env::var call sites in Rust"}`

  ```
=== env::var occurrences by file ===
drave-core/src/clusters.rs:168:    match std::env::var("DRAVE_CLUSTERS") {
drave-core/src/gguf.rs:91:    matches!(std::env::var("DRAVE_PRELIRE_TOUT").as_deref(), Ok("1") | Ok("oui") | Ok("true"))
drave-core/src/gguf.rs:95:    match std::env::var("DRAVE_PRELIRE") {
drave-core/src/gguf.rs:156:    match std::env::var("DRAVE_MMAP") {
drave-core/src/gpu.rs:1540:        if std::env::var("DRAVE_GPU").is_err() { return None; }
drave-core/src/gpu.rs:1565:        if std::env::var("DRAVE_GPU").is_err() { return None; }
drave-core/src/main.rs:80:    let vieux_nom = std::env::vars().map(|(k, _)| k).find(|k| {
drave-core/src/main.rs:430:    if std::env::var("DRAVE_GPU_TOPK").map(|v| v != "0" && !v.is_empty()).unwrap_or(false) {
drave-core/src/main.rs:443:        } else if std::env::var("DRAVE_GPU").is_err() {
drave-core/src/main.rs:445:        } else if std::env::var("DRAVE_GPU_KV").is_err() {
drave-core/src/main.rs:1508:        let chemin = std::env::var("DRAVE_VISION_TEXTE").unwrap_or_default();
drave-core/src/main.rs:2555:                    if std::env::var("DRAVE_DEBUG_FLUX").is_ok() {
drave-core/src/main.rs:2872:    let bits = std::env::var("DRAVE_KV_BI
… [4018 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for v in DRAVE_FLUX_POS DRAVE_KV DRAVE_TRACE_HC DRAVE_BANC_KV_BITS DRAVE_MODELE DRAVE_MODELES DRAVE_LLAMA DRAVE_PRELIRE_TO DRAVE_VISIO DRAVE_FLUX_VER DRAVE_DEBUG; do echo \"=== $v ===\"; grep -rn \"$v\" --include='*.rs' --include='*. … [158 caractères tronqués]`

  ```
=== DRAVE_FLUX_POS ===
=== DRAVE_KV ===
./docs/histoire.md:57:| `QT_KV_BITS`, `QT_KV_F16` | `DRAVE_KV_BITS`, `DRAVE_KV_F16` |
./docs/roadmap.md:30:| 1.4 | **Écart int8 résiduel** (+3,0 % contre +0,8 % chez llama.cpp à 8 192) | ✅ | **attribué** : tout l'écart est dans les CLÉS (clés f32 + valeurs int8 = +0,023 % ; l'inverse = +3,01 %) ; **courbe du placement des bits faite** (`reports/rapport-placement-bits-kv.md`) — à taille égale, mettre les bits sur les clés change l'erreur d'un facteur 130 à 840. Suite FAITE : **clés f16 = +0,018 % pour 39 % de la taille f32** — le meilleur réglage mesuré (`DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1`) |
./docs/roadmap.md:158:drapeaux annoncés (`DRAVE_KV_V_F32`, `DRAVE_KV_K_F32`) ont été terminés, et
./docs/roadmap.md:173:Conséquence utilisable tout de suite : `DRAVE_KV_BITS=8 DRAVE_KV_K_F32=1` donne un
./docs/contexte-long.md:117:empaquetés en 4 bits — `DRAVE_KV_BITS=8` ou `4`, `[config] cache KV` dit ce qui est
./docs/contexte-long.md:194:facteur 840. **Le réglage recommandé est `DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1`** :
=== DRAVE_TRACE_HC ===
./docs/plan-deepseek41-complet.md:177:  jeton** ; on la trace comme telle (canal `DRAVE_TRACE_HC`), avec sa
=== DRAV
… [2575 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== mode in flux_codec.py ===\" && grep -n 'mode' tools/flux_codec.py | head -30; echo \"=== docstring flux_codec ===\"; head -40 tools/flux_codec.py; echo \"=== modes in docs/format-flux.md ===\"; grep -n 'mode [0-9]\\|mode=' … [84 caractères tronqués]`

  ```
=== mode in flux_codec.py ===
=== docstring flux_codec ===
#!/usr/bin/env python3
"""Encodeur/décodeur de RÉFÉRENCE du flux d'activation (format DRVF v1 et v2).

Le format de trace et le contrat d'échange de la phase 3 sont le MÊME format :
une liste d'activation est ce qu'un nœud distant doit recevoir pour continuer le
calcul. Ce fichier est la deuxième implémentation de ce format — la première est
en Rust (`--trace-flux`) — et c'est ce qui permet de dire qu'il est sans
ambiguïté : deux implémentations indépendantes, un aller-retour identique.

Structure :
    en-tête   "DRVF" · u16 version · u32 n_layer · u32 hidden
    liste     u16 couche · u32 position · u32 n_actifs · f32 echelle
              puis n_actifs × ( u32 indice · i16 valeur )          [v1]
              puis n_actifs × ( u8 écart · i16 valeur )            [v2]
                   l'écart de 255 annonce l'indice ABSOLU sur u16
    fin       u16 0xFFFF

v2 : les indices sont écrits par ÉCARTS (la liste est triée). Mesuré sur une trace
réelle de 512 jetons : 132 396 736 octets en v1, **66 370 408** en v2 (−49,87 %),
à contenu identique — le rejeu redonne la même perplexité au chiffre près.

Usage :
    flux_codec.py <t
… [1542 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '80,140p' docs/format-flux.md", "description": "Read flux format mode table"}`

  ```
qu'avec la même configuration de fenêtres. C'est dit ici parce que c'est le seul
cas où la clé n'est pas une simple fonction du jeton.
Avec la position, deux fenêtres réécrivaient les mêmes clés `(couche, position)`
et le rejeu rejouait la mauvaise : perplexité **356 694** au lieu de 17,43. Le
format sur le disque n'a pas changé ; c'est la sémantique du champ qui est
maintenant explicite — et c'est exactement le genre de précision qu'une
spécification doit porter.

## Transport (phase 3, TCP) — protocole v5

```
en-tête (79 octets, identique à l'aller et au retour)
          magie        u32          0x44525631 (« DRV1 »)
          version      u8           5   (refusée si différente, en le disant)
          mode         u8           0 = f32 dense · 1 = liste quantifiée
                                    2 = listes à échelle par bloc · 3 = LOT dense
                                    4 = LOT en listes (mode 2 répété par état)
          couche_debut u32
          couche_fin   u32
          position     u32
          n            u32          dimension (mode 0) ou actifs (mode 1)
          échelle      f32          mode 1 uniquement
          niveaux      f32          ┐
          s
… [2427 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 40, "offset": 2085}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
2085: /// d'un octet trop long (40 écrits pour 39 lus), invisible pendant des flux
2086: /// entiers parce qu'il ne décalait le corps que d'un octet.
2087: fn tete_flux(mode: u8, debut: u32, fin: u32, pos: u32, n: usize, echelle: f32,
2088:              mdl: Option<&model::Model>) -> Vec<u8> {
2089:     let act = mdl.map(Act::du_modele).unwrap_or(Act {
2090:         levels: 127.0, thresh: 0.0, topk: 0, renorm: false,
2091:         topk_proj: [0; 7], attn_topk: 0, qk_topk: 0, moe_topk: 0 });
2092:     let mut t = Vec::with_capacity(TAILLE_TETE);
2093:     t.extend_from_slice(&MAGIE_FLUX.to_le_bytes());
2094:     t.push(VERSION_FLUX);
2095:     t.push(mode);
2096:     t.extend_from_slice(&debut.to_le_bytes());
2097:     t.extend_from_slice(&fin.to_le_bytes());
2098:     t.extend_from_slice(&pos.to_le_bytes());
2099:     t.extend_from_slice(&(n as u32).to_le_bytes());
2100:     t.extend_from_slice(&echelle.to_le_bytes());
2101:     t.extend_from_slice(&act.levels.to_le_bytes());
2102:     t.extend_from_slice(&act.thresh.to_le_bytes());
2103:     t.extend_from_slice(&act.topk
… [1259 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== VERSION_FLUX/TAILLE_TETE/MAGIE ===\" && grep -n 'VERSION_FLUX\\|TAILLE_TETE\\|MAGIE_FLUX' drave-core/src/main.rs | head -12; echo; echo \"=== portes.sh 27-33 ===\" && sed -n '27,33p' tools/portes.sh", "description": "Check … [36 caractères tronqués]`

  ```
=== VERSION_FLUX/TAILLE_TETE/MAGIE ===
1893:const MAGIE_FLUX: u32 = 0x4452_5631;   // "DRV1"
1906:const VERSION_FLUX: u8 = 5;
1941:const TAILLE_TETE: usize = 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 1
2092:    let mut t = Vec::with_capacity(TAILLE_TETE);
2093:    t.extend_from_slice(&MAGIE_FLUX.to_le_bytes());
2094:    t.push(VERSION_FLUX);
2109:    assert_eq!(t.len(), TAILLE_TETE,
2110:               "en-tête de flux de {} octets pour {TAILLE_TETE}", t.len());
2213:    Ok((TAILLE_TETE + corps.len(), n))
2230:    Ok(TAILLE_TETE + corps.len())
2264:    Ok(TAILLE_TETE + corps.len())
2270:    let mut tete = [0u8; TAILLE_TETE];

=== portes.sh 27-33 ===

# Attention : le moteur affiche AUSSI une perplexité cumulée par fenêtre, avant
# le total. Prendre la première occurrence du motif donnait 17,431 (fenêtre 1) au
# lieu de 19,3885 (total) — un instrument faux qui accuse le code.
valeur() { grep -oE "=== perplexité [0-9]+\.[0-9]+" | grep -oE "[0-9]+\.[0-9]+" | head -1; }

echo "=== Portes ==="
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aiguille.py", "limit": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aiguille.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Aiguille dans la botte de foin — version 2, celle qui mesure vraiment.
3: 
4: La perplexité ne dit pas si un modèle RETROUVE une information. Ce script plante
5: un code à une profondeur donnée dans un contexte long, puis le redemande.
6: 
7: Ce qui a changé par rapport à la v1 (mesurée et arrêtée) :
8: 
9: 1. **le remplissage est du vrai texte VARIÉ** (`data/wikitext2_test.txt`), et non
10:    la même phrase recopiée jusqu'à la longueur voulue. Un remplissage répété ne
11:    teste rien : le modèle pouvait répondre en devinant la structure. Chaque sonde
12:    prend en plus une FENÊTRE DIFFÉRENTE du corpus, pour que les sondes ne
13:    partagent pas leur remplissage ;
14: 2. **la réponse est longue** (`--n 40` par défaut) : un code peut sortir au
15:    deuxième ou troisième jeton, et s'arrêter à 8 jetons faisait échouer des
16:    sondes que le modèle savait résoudre ;
17: 3. **le préremplissage par lots** (`--lot`) rend chaque sonde abordable : le
18:    moteur ne l'utilisait que pour la perplexité ;
19:    ⚠️ et depuis le sprint 4, le décal
… [2708 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aiguille.py", "offset": 80, "limit": 140}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aiguille.py</path>
<type>file</type>
<content>
80:         env["DRAVE_GPU"] = "1"
81:         env["DRAVE_GPU_KV"] = "1"
82:         env["DRAVE_GPU_TOPK"] = "1"
83:     cmd = [Q, modele, "--infer", "--chat", "--flux", "--prompt", invite,
84:            # Marge de 1024 et non 512 : certaines fenêtres de corpus tokenisent à
85:            # 4 750 jetons pour une cible de 4 096 (Mesuré), et un prompt PLUS LONG
86:            # que le contexte ne fait pas échouer le moteur — il le ralentit d'un
87:            # facteur 10 à 20 sans un mot (mesuré : 13 à 23 min au lieu de 75 s).
88:            "--n", str(args.n), "--ctx", str(ctx + 1024), "--threads", str(args.threads),
89:            "--temp", "0", "--lot", str(args.lot)]
90:     if args.attn_topk > 0:
91:         cmd += ["--attn-topk", str(args.attn_topk)]
92:     t0 = time.time()
93:     try:
94:         r = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout,
95:                            env=env)
96:     except subprocess.TimeoutExpired:
97:         return None, time.time() - t0, "délai dépassé"
98:     sortie = r.stdout + r.stderr
99:     # Le moteur 
… [7677 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/compare_logits.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/compare_logits.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """Compare deux fichiers de logits au format :
3:    int32 n_vocab, int32 n_pos, puis n_pos lignes de n_vocab f32 (petit-boutiste).
4: 
5: Usage : compare_logits.py <notre.bin> <reference.bin> [ids.txt]
6: 
7: Rend : par position, la perte (NLL) de chacun, l'écart de NLL, le rang du jeton
8: cible dans chacun, et l'accord du top-1. C'est ce qui localise une divergence :
9: une erreur d'embedding ou de norme se voit dès la position 0 ; une erreur de
10: position (RoPE) fait croître l'écart avec la position ; une erreur de MoE ou de
11: tête fait décrocher toutes les positions d'un coup.
12: """
13: import struct, sys, math
14: 
15: try:
16:     import numpy as np
17: except ImportError:
18:     np = None
19: 
20: 
21: def lire(chemin):
22:     with open(chemin, 'rb') as f:
23:         n_vocab, n_pos = struct.unpack('<ii', f.read(8))
24:         data = f.read(n_pos * n_vocab * 4)
25:     assert len(data) == n_pos * n_vocab * 4, f"{chemin} tronqué"
26:     if np is not None:
27:         a = np.frombuffer(data, dtype='<f4').reshape(n_pos, n_vocab
… [3944 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rhoE '[A-Za-z0-9_][A-Za-z0-9_./-]*\\.(md|rs|py|sh|c|json|tsv|gguf|bin|txt|ipynb)' sprints/*.md | sort -u | while read -r p; do if [ -e \"$p\" ]; then echo \"EXISTE   $p\"; else echo \"ABSENT   $p\"; fi; done", "description": "C … [42 caractères tronqués]`

  ```
ABSENT   00002-of-00003.gguf
ABSENT   aiguille.py
ABSENT   api-docs.deepseek.c
ABSENT   clusters.rs
ABSENT   commun.gguf
ABSENT   compare_logits.py
EXISTE   docs/contexte-long.md
EXISTE   docs/plan-deepseek-v4-flash.md
ABSENT   gpu.rs
ABSENT   huggingface.c
ABSENT   llama.c
ABSENT   mapping.tsv
ABSENT   model.rs
EXISTE   README.md
EXISTE   reports/rapport-aiguille-topk.md
EXISTE   reports/rapport-empreinte-memoire.md
EXISTE   reports/rapport-gpu-topk-selection.md
EXISTE   REPRISE.md
ABSENT   self.c
EXISTE   tools/analyse_empreinte.py
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 70, "offset": 137}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
137:     let mut i = 2;
138:     while i < args.len() {
139:         match args[i].as_str() {
140:             "--matrix" if i + 1 < args.len() => { matrix = args[i + 1].clone(); i += 2; }
141:             "--threads" if i + 1 < args.len() => {
142:                 n_threads = args[i + 1].parse().unwrap_or(n_threads); i += 2;
143:             }
144:             _ => i += 1,
145:         }
146:     }
147: 
148:     let t0 = Instant::now();
149:     let g = Gguf::open_auto(path).expect("ouverture du GGUF");
150:     println!("GGUF ouvert en {:?} — {} tenseurs", t0.elapsed(), g.tensors.len());
151:     let arch = g.meta.get("general.architecture").and_then(|m| m.as_str()).unwrap_or("?");
152:     let n_layer = g.cfg("block_count").and_then(|m| m.as_u64()).unwrap_or(0);
153:     let hidden = g.cfg("embedding_length").and_then(|m| m.as_u64()).unwrap_or(0);
154:     let inter = g.cfg("feed_forward_length").and_then(|m| m.as_u64()).unwrap_or(0);
155:     println!("architecture : {arch} · {n_layer} couches · hidden {hidden} · intermédiaire {inter}");
156:     println!("threads : 
… [2914 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== args parsing elsewhere ===\" && grep -rn 'env::args' drave-core/src/*.rs; echo \"=== plus gros flags: -keep etc ===\"; grep -rn '\"-[a-z]' drave-core/src/main.rs | head -20", "description": "Check other arg parsers"}`

  ```
=== args parsing elsewhere ===
drave-core/src/main.rs:49:    let args: Vec<String> = std::env::args().collect();
=== plus gros flags: -keep etc ===
  ```

### 👤 Utilisateur

Agent b13a6032-4f62-4e86-aa1f-03864a455c83 sent a message:
DÉPOUILLEMENT EN-TÊTE + CLI — 24 scripts de /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ (lecture seule stricte, aucun fichier modifié).

### tools/aiguille.py  (219 lignes)
- Rôle : « Aiguille dans la botte de foin — version 2, celle qui mesure vraiment. » La perplexité ne dit pas si un modèle RETROUVE une information : plante un code (« AZUR-7391 ») à une profondeur donnée dans un contexte long, puis le redemande. Remplissage = vrai texte varié (`data/wikitext2_test.txt`), fenêtre différente par sonde ; réponse longue ; préremplissage par lots ; contexte réellement atteint relu dans la sortie du moteur.
- Positional args : `modele` (l.127), `longueurs` CSV de contextes (l.128), `profondeurs` CSV de fractions 0..1 (l.129). Usage docstring l.27-28.
- Options CLI :
  · `--n` (int, 40, "jetons générés (réponse)") l.130
  · `--threads` (int, 16, sans help) l.131
  · `--lot` (int, 256, "lot de préremplissage") l.132
  · `--timeout` (int, 7200, sans help) l.133
  · `--gpu` (store_true, "DRAVE_GPU=1 (déport des projections)") l.134
  · `--gpu-kv` (store_true, "DRAVE_GPU=1 DRAVE_GPU_KV=1 (KV en VRAM)") l.135
  · `--attn-topk` (int, 0, "--attn-topk N (0 = attention complète)") l.140-141
  · `--gpu-topk` (store_true, "DRAVE_GPU=1 DRAVE_GPU_KV=1 DRAVE_GPU_TOPK=1") l.142-143
  · `--journal` (str, "", sans help) l.144
  Contraintes : `--gpu-topk` exige `--attn-topk N` sinon ap.error (l.149-150) ; `--attn-topk` doit être ≥0 (l.151-152). Pas de `choices` nulle part.
- Constantes de tête : `Q="./drave-core/target/release/drave"` l.41 ; `CORPUS="data/wikitext2_test.txt"` l.42 ; `CODE="AZUR-7391"` l.43 ; `AIGUILLE` l.44 ; `QUESTION` l.45-46. Env : DRAVE_GPU / DRAVE_GPU_KV / DRAVE_GPU_TOPK l.74-82.
- Formats : lit wikitext2 (normalisation @-@ @,@ @.@, l.53) ; lance le moteur avec `--infer --chat --flux --prompt --n --ctx --threads --temp 0 --lot [--attn-topk]` l.83-91 ; journal markdown `| contexte | profondeur | trouvé | secondes | détail |` l.205-215 ; retourne via sys.exit(main()) l.219.

### tools/analyse_empreinte.py  (208 lignes)
- Rôle : « Chiffrer l'empreinte mémoire d'un MoE depuis une trace de routage. » Rend : courbe succès/empreinte par couche, verdict sur l'allocation non uniforme, taille minimale utile d'un cache LRU, structure périodique (Jaccard par écart de couches), extrapolation à un modèle connu.
- Positional : `trace` (l.70). Usage docstring l.4-10.
- Options : `--limite` (int, None, "ne lire que les N premiers jetons") l.71-72 ; `--modele` (str, None, "nom d'un modèle connu pour l'extrapolation (deepseek4, deepseek41, qwen3moe)") l.73-75. `ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)` l.68-69.
- Constantes/vocabulaire : `connus = {"deepseek4": (43,256,6,5.51), "deepseek41": (40,384,6,9.95), "qwen3moe": (48,128,8,3.05)}` = (couches, experts, top-k, Mo/expert) l.188-192 ; seuils (0.50,0.70,0.80,0.90,0.95,0.99) l.95 ; caches testés (topk,16,32,64,128) l.120 ; sortie code 1 (sys.exit) si trace vide l.80, modèle inconnu l.194.
- Formats : lit trace texte « couche jeton expert1 expert2 … » (l.12, produite via DRAVE_TRACE_EXPERTS, l.5) ; stdout texte seulement.

### tools/analyse_experts_statique.py  (244 lignes)
- Rôle : « Analyse STATIQUE des experts d'un MoE : que portent les poids eux-mêmes. » Trois mesures : similarité intra-couche (experts jumeaux), profil de SOURCES (norme de colonne d'entrée), profil de DESTINATIONS (norme de ligne de sortie). « Ne lit que la tête des tenseurs ».
- Positional : `modele` (.gguf) l.175. Usage l.9.
- Options : `--couches` (str, "0,12,24,36,47", sans help) l.176 ; `--lignes` (int, 16, "lignes de sortie lues par expert (16 par défaut)") l.177-178 ; `--seuil` (float, 0.90, "similarité au-delà de laquelle deux experts sont jumeaux") l.179-180.
- Constantes/vocabulaire : classe `Lecteur` « Lecteur GGUF minimal : en-tête, descripteurs, et octets d'un tenseur » l.35-36 ; tenseurs cherchés `blk.{l}.ffn_gate_exps.weight`, `ffn_up_exps.weight`, `ffn_down_exps.weight` l.190-191 ; clés GGUF `general.architecture`, `{arch}.expert_count` l.184-185 ; types ggml gérés F32=0 et F16=1, sinon ValueError (l.167-169) ; tailles de bloc `{12:144, 14:210, 8:34, 0:4, 1:2}` l.200 ; seuil « 80 % » n80 l.230.
- Formats : lit un GGUF en-tête + tête de tenseurs ; stdout texte.

### tools/analyse_flux.py  (95 lignes)
- Rôle : « Analyse PURE d'une trace de flux : ce que la vision appelle “voir le modèle neurone par neurone”, mais chiffré par couche et sans exécuter le moteur. » Répond : quelle couche est creuse (~22 % de densité = décision push/pull), quels neurones sont PERSISTANTS, recouvrement des top-k entre couches.
- Positional : traces DRVF, jusqu'à 3 (`[:3]`) l.85. Usage l.16 : `analyse_flux.py <trace> [<trace2> ...] [--top 100]`.
- Options : `--top` (int, défaut 100, parsé à la main `sys.argv` l.83-84, pas d'argparse, pas de help).
- Constantes/vocabulaire : magie `b"DRVF"`, u16 version, u32 n_layer, u32 hidden, listes u16 couche / u32 pos / u32 n / f32 echelle, paires u32 indice + i16 valeur, sentinelle 0xFFFF (l.24-33) ; persistant si fréquence ≥ 0.9·jetons l.61 ; top1 %/top10 % l.64-65 ; couche ≥1000 affichée « FFN {couche-1000} » l.74.
- Formats : lit binaire DRVF ; stdout.

### tools/clusters_moe.py  (224 lignes)
- Rôle : « Découpage des MoE en clusters — à partir d'une trace de routage réelle. » Question de placement : quels experts s'allument ENSEMBLE ? Mesures : couverture, ventilation (fan-out pour 90 %), équilibre ; témoins aléatoire et fréquence seule.
- Positional : `trace` l.144. Usage l.23-24 : `clusters_moe.py /tmp/routage.txt [--clusters 8] [--json /tmp/clusters.json]`.
- Options : `--clusters` (int, 8, "nombre de groupes visés (nœuds ou GPU disponibles)") l.145-146 ; `--json` (str, "", sans help) l.147 ; `--graine` (int, 1234, sans help) l.148.
- Constantes/vocabulaire : `partition_equilibree(..., passes=6)` l.60 ; témoin fréquence = tranches de taille ceil(ne/K) (l.185-188) ; clés JSON : couches/clusters/n_jetons/n_experts (l.159-160), par couche `appris|hasard|frequence|affectation|membres` (l.190-191), mesures `couverture_moyenne`, `ventilation_moyenne`, `ventilation_max`, `taille_min`, `taille_max` (l.130-139).
- Formats : lit trace texte « couche jeton experts… » (`lire` l.32-42, docstring du moteur l.4-5) ; écrit JSON indent=1 si `--json` l.217-219.

### tools/compare_etats.py  (84 lignes)
- Rôle : « Compare les états intermédiaires de Drave à ceux de llama.cpp, tenseur par tenseur. » « La comparaison porte sur les vecteurs entiers, pas sur huit valeurs. »
- Positional : exactement 5 — `<préfixe_drave> <préfixe_ref> <nom> <couche> <positions>` (l.15-16, 46-48 ; `len(sys.argv)!=6` → SystemExit(__doc__)).
- Options : aucune (pas d'argparse).
- Constantes/vocabulaire : magie `REFD` l.34 ; dispositions `l_last` = [embd, hc, position], `hc_attn_pre` = [embd, position] l.51-56 ; verdicts ✅ si écart max ≤ 1e-4 × dynamique, « ~ » si corr > 0.999, sinon ❌ l.78.
- Formats : Drave = f32 bruts sans en-tête `<préfixe_drave>-<nom>-<couche>-<position>.bin` (écrits par DRAVE_DUMP_COUCHES) ; llama.cpp = `<préfixe_ref>-<nom>-<couche>.bin` en-tête `REFD`+ndim+ne[4] puis f32 ordre ggml (l.5-10, 30-42).

### tools/compare_logits.py  (109 lignes)
- Rôle : « Compare deux fichiers de logits » ; rend par position la NLL de chacun, l'écart de NLL, le rang du jeton cible et l'accord du top-1 (localise embedding/norme/RoPE/MoE).
- Positional : `<notre.bin> <reference.bin> [ids.txt]` (l.5, 44-47).
- Options : aucune.
- Constantes/vocabulaire : format = int32 n_vocab, int32 n_pos, puis n_pos × n_vocab f32 LE (l.2-3) ; flags numpy optionnel (fallback Python pur) l.15-18 ; échantillon imprimé si `i<24 or i%32==0` (l.71, 88) mais accord top-1 compté sur TOUTES les positions (l.73-76) ; codes retour 2 si ids absents/vides ou <2 ids (l.58-65).
- Formats : binaire logits ; ids en texte (espaces/virgules) l.47.

### tools/convertir_clusters.py  (525 lignes)
- Rôle : « Convertisseur GGUF → “modèle éclaté en clusters”, un fichier par cluster. » Chaque cluster = GGUF autonome, mmap seul ; il ne requantifie RIEN (octets copiés tels quels, blocs alignés sur l'axe experts). Champ `<arch>.expert_count` ajusté.
- Positional : `source` (.gguf) l.355, `dossier` l.356. Usage l.28-30.
- Options : `--clusters` (int, 8, sans help) l.357 ; `--trace` (str, "", "trace de routage (ordre des experts)") l.358 ; `--mode` (choices ["experts","couches"], défaut "experts", sans help) l.359 ; `--verifier` (store_true, "relit chaque fichier produit et compare les empreintes") l.360-361.
- Constantes/vocabulaire : `TYPES` ggml -> (nom, octets/bloc, éléments/bloc) l.42-48 : 0 F32(4,1), 1 F16(2,1), 2 Q4_0(18,32), 3 Q4_1(20,32), 6 Q5_0(22,32), 7 Q5_1(24,32), 8 Q8_0(34,32), 9 Q8_1(36,32), 10 Q2_K(84,256), 11 Q3_K(110,256), 12 Q4_K(144,256), 13 Q5_K(176,256), 14 Q6_K(210,256), 15 Q8_K(292,256), 39 MXFP4(17,32).
- Formats/sorties : `commun.gguf` l.417 ; `cluster-NN.gguf` l.449 et 464 ; `manifeste.json` (champs source, mode, clusters, n_experts, fichiers[fichier, role, octets, tenseurs | experts_locaux, experts_globaux_par_couche, couches], experts[ordre par couche]) l.391-393, 420-422, 455-459, 467-470 ; `mapping.tsv` avec `# drave-clusters-mapping v1` et colonnes couche/local/global/cluster l.341-348 ; trace lue en texte (couche jeton experts) l.297-305 ; mode experts si `"_exps." in nom` l.377, mode couches = groupes de couches l.396-412 ; vérif sha256 produit vs source l.481-519.

### tools/diff_flux.py  (91 lignes)
- Rôle : « Diff de deux traces de flux d'activation (format DRVF) » : où le flux diverge, à quelle couche, à quel jeton, de combien.
- Usage l.8 : `diff_flux.py <traceA> <traceB> [--top 8]`.
- Positional : traceA, traceB (sys.argv[1], [2]) l.37-38.
- Options : `--top` (int, défaut 8, parsé main l.39-41, pas de help).
- Constantes/vocabulaire : magie `b"DRVF"`, u16 version, u32 n_layer, u32 hidden, listes u16/u32/u32/f32, paires u32+i16, sentinelle 0xFFFF l.14-33 ; comparaison des valeurs DÉQUANTIFIÉES (v × échelle) l.54-61 ; dynamique = echelle·32767 l.70 ; couche ≥1000 → « FFN N » l.85 ; retour 1 si aucune liste commune, 0 si flux identiques l.46-48, 78-80.

### tools/flux_codec.py  (158 lignes)
- Rôle : « Encodeur/décodeur de RÉFÉRENCE du flux d'activation (format DRVF v1 et v2) » ; deuxième implémentation du contrat d'échange (l'autre en Rust `--trace-flux`).
- Positional : `trace` (sys.argv[1]) l.123. Usage l.22-25 : `flux_codec.py <trace>` / `<trace> --jetons N`.
- Options : `--jetons` (int, parsé main, l.146-147).
- Constantes/vocabulaire : `MAGIE=b"DRVF"` l.30 ; `VERSION=2` « ce que ce fichier ÉCRIT ; il LIT la 1, la 2 et la 3 » l.31 ; structs `ENTETE "<4sHII"`, `LISTE "<HIIf"`, `PAIRE_V1 "<Ih"`, `PAIRE_V2 "<Bh"`, `FIN "<H"` l.32-36.
- Format : en-tête DRVF + u16 version + u32 n_layer + u32 hidden ; liste u16 couche/u32 position/u32 n_actifs/f32 echelle ; v1 paires (u32 indice, i16 valeur) ; v2 écarts u8 + i16, écart 255 → indice absolu u16 ; v3 (lecture seule) u32 n_blocs + échelles f16 + paires (u8 écart, i8 valeur) indexées par bloc de 32 l.76-94 ; fin u16 0xFFFF. Mesure citée : v1 132 396 736 o → v2 66 370 408 o (−49,87 %) l.18-20.

### tools/harmony_canonique.py  (72 lignes)
- Rôle : « Construit un identifiant de perplexité au format harmony CANONIQUE » (le montage forcé est hors distribution : p=0,9999 pour le canal `analysis` contre 0,0001 pour `final`). Séquence : message système complet, tour user, canal analysis court, puis canal final portant le texte à noter.
- Positional : aucun. Flag : `--sans-analysis` (testé par `"--sans-analysis" in sys.argv` l.45) = même séquence SANS le message analysis (contrôle).
- Constantes : `Q="/home/stephane/.../Drave/drave-core/target/release/drave"` l.17 ; `M="/home/stephane/.../gpt-oss-120b-MXFP4.gguf"` l.18 ; `DEB, FIN, MSG, CANAL = 200006, 200007, 200008, 200005` l.20 ; message système verbatim l.49-53.
- Formats : lit `/tmp/wt2_prefixe.txt` et `/tmp/wt2_suite.txt` l.47-48 ; passe par le tokenizer du moteur (`--tokenize --fichier --sortie`) l.28-29 ; écrit `/tmp/harmony_canonique[_sans_analysis].ids` et `.dep` (indice du premier jeton de contenu) l.63-66.

### tools/hc_synthetique.py  (98 lignes)
- Rôle : « Référence numpy des hyper-connexions de DeepSeek-V4, et valeurs-témoins. » Formules recopiées des opérations ggml de `llama.cpp/src/models/deepseek4.cpp` (build_hc_pre, build_hc_sinkhorn, build_hc_post, build_hc_head), PAS du Rust ; sortie collée dans le test Rust `model::tests_hc::hyper_connexions_conforme_a_la_reference`.
- Usage : `python3 tools/hc_synthetique.py` (aucun argument) l.14.
- Constantes : `HC, H = 4, 3` l.18 ; `EPS = 1e-6` (« hyper_connection.epsilon (V4.1) ») l.19 ; `ITERS = 20` (« hyper_connection.sinkhorn_iterations (V4.1) ») l.20 ; graine np 20261002 l.63 ; `scale = [0.5, 1.5, 2.0]` l.67.
- Sortie : lignes Rust `const MELANGE/BASE/SCALE/X/Y/PRE/POST/COMB/ENTREE/SORTIE: [f32; N] = [...]` l.79-89, + invariants sommes par destination/source l.90-94.

### tools/lire_meta_gguf.py  (117 lignes)
- Rôle : « Lit les métadonnées d'un GGUF (en-tête seul) et imprime les clés demandées » (ex. `compress_ratios` : quelles couches sont compressées). Sans motif, imprime tout (valeurs >64 éléments tronquées).
- Positional : `fichier.gguf` + `[motif ...]` (sys.argv[2:]) l.71-74. Usage l.10-12.
- Options : aucune.
- Constantes : `TYPES` ggml {0:u8,1:i8,2:u16,3:i16,4:u32,5:i32,6:f32,7:bool,8:str,9:array,10:u64,11:i64,12:f64} l.17-18 ; `FIXES` structs LE l.19-21.
- Remarque : une fonction `lire_tenseur_f32(chemin, motif, index)` existe APRÈS le bloc `__main__` (l.77-117), non exposée en CLI ; utilise `general.alignment` (défaut 32) et n'accepte que le type F32.
- Format : GGUF (magie b"GGUF", version u32, n_tensors/n_kv u64).

### tools/mesurer_lecture_experts.py  (81 lignes)
- Rôle : « Lectures d'experts : série contre parallèle, sur un VRAI fichier froid. » Force le froid par `posix_fadvise(DONTNEED)` et compare deux passes appariées sur des blocs différents.
- Positional : `<shard.gguf>` l.36, `[nb_blocs]` défaut 240 l.37, `[nb_fils]` défaut 16 l.38.
- Options : aucune. Usage l.4.
- Constantes : `PAGE = 4096` l.24 ; `taille_bloc = 4 << 20` (4 Mo ≈ un expert) l.39 ; zones `debut = taille // 2`, `zone_b = debut + nb_blocs*taille_bloc` l.45-47.
- Format : ouvre le GGUF en mmap PROT_READ ; stdout Go/s série vs parallèle + rapport ×.

### tools/mla_synthetique.py  (250 lignes)
- Rôle : « Modèle MLA synthétique + référence numpy — le harnais du chantier 5. » Fabrique un modèle minuscule (poids aléatoires, formes MLA correctes), l'écrit en GGUF et calcule une référence numpy indépendante (cache KV latent : 1 tête de 128 + 32 valeurs par jeton).
- Options (aucun positional) : `--sortie` (str, "/tmp/mla_minuscule.gguf") l.226 ; `--dossier` (str, "/tmp/mla_ref") l.227 ; `--graine` (int, 1234) l.228 ; `--n` (int, 8, "jetons d'entrée") l.229. Usage l.15-16.
- Constantes : `H=64` hidden, `NL=2` couches, `NH=4` têtes requête, `NKV=1` (MLA = MQA), `QL=32` q_lora_rank, `KVL=48` kv_lora_rank, `QKR=16` qk_rope, `QKN=16` qk_nope, `VD=16` value_length, `FFN=128`, `VOCAB=64`, `EPS=1e-5`, `ROPE_BASE=10000.0` (l.28-40).
- Formats : écrit un GGUF version 3, tenseurs F32 (type 0), alignement 32 (l.176-206) ; noms de tenseurs `token_embd.weight`, `output_norm.weight`, `blk.N.attn_q_a`, `attn_q_a_norm`, `attn_q_b`, `attn_kv_a_mqa`, `attn_kv_a_norm`, `attn_kv_b`, `attn_output`, `ffn_*` (l.50-70) ; dans `--dossier` : `logits.npy`, `ids.npy`, `forme.json` (hidden, n_layer, n_head, q_lora, kv_lora, qk_rope, qk_nope, v_dim, ffn, vocab, graine) l.237-242.

### tools/pair_factice.py  (140 lignes)
- Rôle : « Pair factice du protocole de flux (v2) : il ÉCOUTE et DIT ce qu'il reçoit. » Rend visible ce que l'autre bout envoie (tailles, positions, modes, réglages) ; répond un flux de la dimension demandée.
- Positional : `<port>` défaut 45760 l.32, `[dimension]` défaut 896 l.33. Usage l.10.
- Options : aucune.
- Constantes/vocabulaire : `MAGIE = 0x44525631` l.14 ; `TETE = 79` (en-tête v4 : magie, version, mode, plage, position, n, échelle, niveaux, seuil, top-k, renorm, 7 top-k par projection, 3 top-k globaux) l.15-16 ; `MODES = {0:"dense f32", 1:"listes quantifiées", 2:"blocs (i8 + écarts)", 3:"lot dense (t états × dimension)", 4:"lot en listes (mode 2 par état)"}` l.17-18.
- Protocole : réponse struct `"<IBBIIIIfffIBIIIIIIIIII"` l.115-117 ; mode 3 = n états × dimension × 4 ; mode 4 = n états à liste vide, nb = (dimension+31)//32 blocs ; mode 2 = nb blocs + échelles f32 + longueur 0 ; mode dense = dimension × 4 (l.118-134) ; invariants mode 4 vérifiés (nb attendu, 2a ≤ lg ≤ 4a) l.80-86. Écoute 127.0.0.1.

### tools/profil_flux.py  (78 lignes)
- Rôle : « Profilage par neurone à partir d'une trace de flux (format DRVF) » — quels neurones s'allument, à quelle fréquence, avec quelle magnitude, par couche.
- Positional : `trace` (sys.argv[1]) l.37.
- Options RÉELLES : `--top` (int, défaut 6, parsé main l.39-40) ; `--csv` (chemin, l.42-43). ⚠️ DISCRÉPANCE : l'usage du docstring annonce `[--couche N]` (l.8) mais `--couche` n'est JAMAIS lu ni implémenté.
- Constantes/vocabulaire : format DRVF identique à analyse_flux (l.14-33) ; top10 % = len(forts)//10 l.61 ; couche ≥1000 → « FFN N » l.64.
- Formats : lit DRVF ; CSV en-tête `couche,neurone,magnitude,frequence` l.70.

### tools/proxy_latence.py  (54 lignes)
- Rôle : « Relais TCP qui ajoute une latence par message, pour mesurer ce qu'un lien distant coûte à un découpage de modèle » (le débit n'est jamais le problème — 0,25 Mbit/s — la latence si).
- Positional : `<port_écoute>` l.35, `<hôte_cible:port>` (rsplit ":",1) l.36, `[délai_ms]` converti en s, défaut 0.0, l.37. Usage l.10.
- Options : aucune.
- Constantes : recv 65536 l.18 ; bind 127.0.0.1, `listen(4)`, TCP_NODELAY sur les deux sockets l.40-48 ; threads daemon par direction l.49-50.

### tools/session_report.py  (341 lignes)
- Rôle : « Produit, pour chaque session DSH, un rapport qui reconstitue son essence et démontre le travail accompli, étape par étape. » Contenu : fiche, demandes, déroulé, travail, mesures, erreurs, commits (docstring l.10-19).
- Options (aucun positional) : `--repo` (str, défaut `Path(__file__).resolve().parent.parent`) l.293 ; `--session` (str, None) l.294 ; `--quiet` (store_true) l.295. Usage l.22.
- Constantes : `TRONC_SORTIE=700`, `TRONC_DEMANDE=700`, `TRONC_SYNTHESE=2500` l.38-40 ; `MOTIFS_MESURE` regex (tok/s | G év | MHz | ALMs | M20K | DSP | Go/s | Mo | Ko | % | ms, ou perplexité|surcoût|résidu|rang|R²|× suivi d'un nombre) l.45-49 ; `MOTIFS_ERREUR` regex (exit code [1-9], panicked at, ^Error, ^error[, ECHEC/ÉCHEC, DIVERGENT au rang, Error (n), fatal error) l.50-52.
- Formats : lit `$DSH_HOME/sessions/--<slug>--/session.jsonl*` (décompression `zstd -dc` si `.zstd`) l.55-61, 299-317 ; enregistrements JSONL par `type` : session, session/title, turn/start, user/message, assistant/message, tool/call, tool/result (l.112-169) ; écrit `journal/sessions/<id>/rapport.md` et `journal/README.md` (l.7-8, 306-336) ; sections : « ## Objectifs déclarés », « ## 1. Ce qui a été demandé », « ## 2. Déroulé, étape par étape », « ## 3. Travail accompli », « ## 4. Mesures et résultats marquants », « ## 5. Erreurs rencontrées », « ## 6. Commits » (l.211, 216, 222, 245, 263, 276, 283) ; retour 1 si aucune session (l.303-304).

### tools/telecharger_modeles.py  (197 lignes)
- Rôle : « Télécharge les modèles LOURDS, par tranches, avec reprise. » Le pont Xet de HF refuse un GET plein sur le fichier de 365,7 Go (HTTP 400) mais sert une requête `Range` (HTTP 206).
- Options (aucun positional, aucun `help=`) : `--manifeste` (str, "tools/manifeste_modeles_lourds.json") l.127 ; `--dest` (str, DEST_DEFAUT) l.128 ; `--seulement` (str, "") l.129 ; `--etat` (store_true) l.130 ; `--journal` (str, "/tmp/telechargement_lourds.log") l.131. Usage docstring l.12-15.
- Constantes : `RACINE="https://huggingface.co"` l.25 ; `CHUNK = 256 << 20` (256 Mo) l.26 ; `DEST_DEFAUT="/home/stephane/Data13TB/stephane/modeles/gguf"` l.27 ; `LIBRE_MINIMUM_GO = 300` l.28 ; `telecharger(..., fils=6, essais=6)` l.69, `_tranche(..., essais=6)` l.35 ; curl `-sSL -f --retry 3 --retry-delay 10 --retry-all-errors -r pos-haut` l.48-51.
- Formats : lit le manifeste JSON (entrées `nom`, `repo`, `chemin`, `octets`) l.134, 177-178 ; URL `{RACINE}/{repo}/resolve/main/{chemin}` l.178 ; fichier préalloué + sidecar `<dest>.etat.json` (position absolue par tranche) + temporaires `.part<cle>` (l.41-64, 155-165) ; `--etat` affiche l'avancement réel depuis le sidecar (getsize = 100 % dès le 1er octet sinon) l.147-174.

### tools/trace_compacite.py  (432 lignes)
- Rôle : « Chiffre ce que coûterait une trace DRVF v1 sous plusieurs encodages. » Disque = 6 o/neurone actif (u32 + i16), réseau ≈ 2 o/actif ; variantes comparées : `actuel`, `écarts+i16`, `écarts+blocs`, `blocs f16`, zstd/gzip. Lecture du format déléguée à tools/flux_codec.py.
- Positional : `trace` l.286. Usage l.29.
- Options : `--couches` (store_true, "ventilation par couche") l.287-288 ; `--sans-compression` (store_true, "saute le point de repère zstd/gzip") l.289-290 ; `--sans-erreur` (store_true, "saute le calcul de l'erreur de quantification i8") l.291-292 ; `--echantillon` (float, 16.0, metavar="Mio", "taille de l'échantillon compressé (défaut : 16 Mio)") l.293-294 ; `--zstd-v2` (store_true, "compresse aussi la variante écarts+blocs reconstruite") l.295-296.
- Constantes : `BLOC = 32` l.56 ; `ECHAPPEMENT = 255` l.57 ; `TAILLE_ENTETE_FICHIER = 14` l.58 ; `TAILLE_ENTETE_LISTE = 10` l.59 ; `TAILLE_QUEUE_BLOCS = 8` l.60 ; import `flux_codec` par sys.path l.53-54.
- Clés internes/vocabulaire : variantes "actuel","i16","blocs","f16" + "blocs_utiles","blocs_emis","echappements","n_err","err2" (l.351-380) ; retour 1 si trace introuvable, non DRVF ou sans activation l.299-313.

### tools/verifier_formats.py  (108 lignes)
- Rôle : « Compare notre déquantification d'un super-bloc à celle de libggml » — référence = `tools/ref_ggml_bloc.c`, côté Rust via `drave <modele> --bloc <tenseur>:<index>` (chemin row_f32). Sortie : écart max + verdict, retour 1 si divergence.
- Positional : `modele.gguf` l.58, `tenseur` l.58, `[index]` défaut 0 l.59-67. Option : `--type` (int, forcé, parsé main l.64-65). Usage l.4.
- Constantes : `RACINE` = racine du dépôt l.26 ; `DRAVE = RACINE/drave-core/target/release/drave` l.27 ; `REF = os.environ.get("REF_GGML_BLOC", "/tmp/ref_ggml_bloc")` l.28 ; `OCTETS_256` octets par super-bloc de 256 poids l.31-51 : 0 F32 1024, 1 F16 512, 2 Q4_0 144, 3 Q4_1 160, 6 Q5_0 176, 7 Q5_1 192, 8 Q8_0 272, 10 Q2_K 84, 11 Q3_K 110, 12 Q4_K 144, 13 Q5_K 176, 14 Q6_K 210, 16 IQ2_XXS 66, 18 IQ3_XXS 98, 19 IQ1_S 50, 23 IQ4_XS 136, 29 IQ1_M 56, 30 BF16 512, 39 MXFP4 136.
- Import : `from analyse_experts_statique import Lecteur` l.23-24 ; verdict CONCORDE si écart < 1e-6, codes retour 2 (usage/type non couvert/rien rendu), 1 (DIVERGE), 0 (l.96-104).

### tools/vision_mtmd.py  (159 lignes)
- Rôle : « Référence de vision : interroger libmtmd d'ollama, sans en-têtes. » Seule vérification qui tranche rotation 2-D, fenêtre locale et fusion 2×2 du ViT Qwen2.5-VL : compare la sortie complète de llama.cpp (via ollama) aux 3 584 valeurs du projecteur. Structure de params opaque 256 octets.
- Positional : `<modele.gguf>` défaut MODELE l.59, `<mmproj.gguf>` défaut MMPROJ l.60, `[sortie.bin]` optionnel l.150.
- Options : aucune. Usage l.15.
- Constantes : `OLLAMA = "/usr/lib/ollama"` l.22 ; `MODELE = .../Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf` l.23 ; `MMPROJ = .../mmproj-Qwen2.5-VL-7B-Instruct-f16.gguf` l.24 ; `TAILLE_PARAMS = 256` l.25 ; backends chargés explicitement `libggml-cpu-haswell/alderlake/sandybridge` l.44-45 ; image déterministe 336×336 (dégradé + carré central, comme le banc Rust) l.76-85 ; `projection_dim` = 3584 valeurs l.146 ; invite `"<|im_start|>user\n<marker>\ndecris cette image<|im_end|>\n<|im_start|>assistant\n"` l.117 ; type de morceau image = 1 l.138.
- Format écrit : `sortie.bin` = i32 longueur + N f32 (l.151-153).

### tools/vision_ref.py  (162 lignes)
- Rôle : « Référence numpy de l'embedding de patchs (première tranche du chemin image). » Le moteur écrit les sorties (`--banc-vision`) et les POIDS lus dans le GGUF ; ce script refait le CALCUL (même partage des rôles que MLA).
- Positional : `sortie.bin` (sys.argv[1]) l.28 ; poids = `sys.argv[2]` si fourni, sinon `sortie + ".poids"` l.29. ⚠️ l'usage annonce `[--poids <sortie.bin.poids>]` (l.9) mais aucune option n'est parsée : `--poids` serait pris comme chemin littéral.
- Options : aucune.
- Constantes : `erf` vectorisé Abramowitz-Stegun 7.1.26 (même approximation que le moteur) l.15-25 ; image du banc cote=28, carré central 10≤x<18 (l.38-44) ; GELU exact 0.5·h·(1+erf(h/√2)) l.75 ; eps LayerNorm 1e-6 l.109 ; rotation 2-D mRoPE : 4 blocs de hd/4, blocs 0/2 par la LIGNE, 1/3 par la COLONNE, base 10000, 16 têtes l.114-137 ; DÉSACCORD si écart relatif > 1e-5 l.156.
- Formats lus : `sortie.bin` = i32 n_patch, i32 cout puis n_patch×cout f32 ; `sortie.bin.poids` = i32 cout, cin, ky, kx puis f32 (reshape [cout,cin,ky,kx]) l.30-36 ; `sortie.bin.projecteur` = 4 i32 (n0,n1,n2,n3) + w0,b0,w2,b2 f32 l.65-72 ; `sortie.bin.bloc` = 3 i32 (npatch, e, nff) + poids f32 (ln1, ln2, wq/bq, wk/bk, wv/bv, wo/bo, wg/bg, wu/bu, wd/bd, x_eng) l.92-108.

SYNTHÈSE TRANSVERSALE (points saillants) :
1. Seuls 12 scripts utilisent argparse (aiguille, analyse_empreinte, analyse_experts_statique, clusters_moe, convertir_clusters, mla_synthetique, session_report, telecharger_modeles, trace_compacite) — en fait 9 avec argparse ; les autres parsent `sys.argv` à la main (analyse_flux, compare_etats, compare_logits, diff_flux, flux_codec, harmony_canonique, lire_meta_gguf, mesurer_lecture_experts, pair_factice, profil_flux, proxy_latence, verifier_formats, vision_mtmd, vision_ref).
2. Deux docstrings annoncent des options qui n'existent pas dans le code : `profil_flux.py --couche N` (l.8 vs main l.36-43) et `vision_ref.py --poids` (l.9 vs main l.29 — c'est un 2e positional).
3. Format DRVF réimplémenté 4 fois (analyse_flux, diff_flux, profil_flux, flux_codec) ; trace_compacite réutilise flux_codec par import.
4. Vocabulaire commun : couche ≥ 1000 = « FFN {couche-1000} » (analyse_flux l.74, diff_flux l.85, profil_flux l.64, trace_compacite l.422).
Aucune modification de fichier effectuée.

### 🤖 Assistant

⏵ Extraction des enums, constantes et structures exposées côté Rust

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && echo \"=== pub enum ===\" && grep -n 'pub enum' *.rs; echo; echo \"=== const UPPER ===\" && grep -nE '^\\s*(pub )?const [A-Z][A-Z0-9_]*' *.rs | head -80", "description": "List enums and consts in Rust"}`

  ```
=== pub enum ===
gguf.rs:134:pub enum Tampon {
gguf.rs:180:pub enum Meta {
list.rs:342:pub enum Source8 {
list.rs:619:pub enum Source {
model.rs:28:pub enum Gating {

=== const UPPER ===
engine.rs:51:const HIGH_BITS: u64 = 0x8080_8080_8080_8080;
engine.rs:496:                        const TUILE: usize = 16;
engine.rs:525:                            const TUILE4: usize = 8;
formats.rs:2766:const IQ1S_DELTA: f32 = 0.125;
gguf.rs:45:const PROT_READ: i32 = 1;
gguf.rs:46:const MAP_PRIVATE: i32 = 2;
gguf.rs:53:const MADV_WILLNEED: i32 = 3;
gguf.rs:258:pub const GGML_F32: u32 = 0;
gguf.rs:259:pub const GGML_F16: u32 = 1;
gguf.rs:260:pub const GGML_Q4_0: u32 = 2;
gguf.rs:261:pub const GGML_MXFP4: u32 = 39;
gguf.rs:262:pub const GGML_Q2_K: u32 = 10;
gguf.rs:263:pub const GGML_BF16: u32 = 30;
gguf.rs:264:pub const GGML_Q3_K: u32 = 11;
gguf.rs:265:pub const GGML_Q4_K: u32 = 12;
gguf.rs:271:pub const GGML_Q5_0: u32 = 6;
gguf.rs:272:pub const GGML_Q5_1: u32 = 7;
gguf.rs:273:pub const GGML_Q5_K: u32 = 13;
gguf.rs:274:pub const GGML_Q6_K: u32 = 14;
gguf.rs:278:pub const GGML_IQ2_XXS: u32 = 16;
gguf.rs:281:pub const GGML_IQ3_XXS: u32 = 18;
gguf.rs:283:pub const GGML_IQ1_S: u32 = 19;
gguf.rs:286:pu
… [2610 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== attn-topk lot ===\" && grep -rn 'IGNORÉ\\|ignore.*lot\\|mode lot' drave-core/src/model.rs | head -10; echo; echo \"=== KvCache::assurer ===\" && sed -n '1100,1140p' drave-core/src/model.rs", "description": "Check attn-topk … [37 caractères tronqués]`

  ```
=== attn-topk lot ===
2464:/// Un seul message pour `--attn-topk` ignoré en mode lot (voir `forward_lot`).
3969:            eprintln!("[attention] --attn-topk {} est IGNORÉ en mode lot (--lot {t}) : \

=== KvCache::assurer ===
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
            let mg = machi
… [1002 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'fn assurer\\|while cap < besoin\\|fn kv_assurer' drave-core/src/model.rs drave-core/src/gpu.rs | head; echo \"---\"; sed -n \"$(grep -n 'fn assurer' drave-core/src/model.rs | head -1 | cut -d: -f2- | cut -d: -f1),+22p\" drav … [86 caractères tronqués]`

  ```
drave-core/src/model.rs:2169:    pub fn assurer(&mut self, besoin: usize) {
drave-core/src/model.rs:2181:        while cap < besoin { cap = (cap * 2).min(self.ctx); }
drave-core/src/gpu.rs:440:    pub fn kv_assurer(&self, m: &mut KvGpu, besoin: usize) -> bool {
drave-core/src/gpu.rs:448:        while cap < besoin { cap = (cap * 2).min(m.ctx); }
---
  ```

### 👤 Utilisateur

Background subagent b13a6032-4f62-4e86-aa1f-03864a455c83 finished and will do no further work unless you send it more.
Its closing message:
### tools/aiguille.py  (219 lignes)
- Rôle : « Aiguille dans la botte de foin — version 2, celle qui mesure vraiment. » La perplexité ne dit pas si un modèle RETROUVE une information : plante un code (« AZUR-7391 ») à une profondeur donnée dans un contexte long, puis le redemande. Remplissage = vrai texte varié (`data/wikitext2_test.txt`), fenêtre différente par sonde ; réponse longue ; préremplissage par lots ; contexte réellement atteint relu dans la sortie du moteur.
- Positional args : `modele` (l.127), `longueurs` CSV de contextes (l.128), `profondeurs` CSV de fractions 0..1 (l.129). Usage docstring l.27-28.
- Options CLI : `--n` (int, 40, "jetons générés (réponse)") l.130 — `--threads` (int, 16, sans help) l.131 — `--lot` (int, 256, "lot de préremplissage") l.132 — `--timeout` (int, 7200, sans help) l.133 — `--gpu` (store_true, "DRAVE_GPU=1 (déport des projections)") l.134 — `--gpu-kv` (store_true, "DRAVE_GPU=1 DRAVE_GPU_KV=1 (KV en VRAM)") l.135 — `--attn-topk` (int, 0, "--attn-topk N (0 = attention complète)") l.140-141 — `--gpu-topk` (store_true, "DRAVE_GPU=1 DRAVE_GPU_KV=1 DRAVE_GPU_TOPK=1") l.142-143 — `--journal` (str, "", sans help) l.144. Contraintes : `--gpu-topk` exige `--attn-topk N` sinon ap.error (l.149-150) ; `--attn-topk` doit être ≥0 (l.151-152). Aucun `choices`/`nargs`.
- Constantes/vocabulaire de tête : `Q="./drave-core/target/release/drave"` l.41 ; `CORPUS="data/wikitext2_test.txt"` l.42 ; `CODE="AZUR-7391"` l.43 ; `AIGUILLE` l.44 ; `QUESTION` l.45-46 ; env DRAVE_GPU / DRAVE_GPU_KV / DRAVE_GPU_TOPK l.74-82.
- Formats lus/écrits : lit wikitext2 (normalisation `@-@ @,@ @.@`, l.53) ; lance le moteur `--infer --chat --flux --prompt --n --ctx --threads --temp 0 --lot [--attn-topk]` l.83-91 ; journal markdown `| contexte | profondeur | trouvé | secondes | détail |` l.205-215 ; `sys.exit(main())` l.219.

### tools/analyse_empreinte.py  (208 lignes)
- Rôle : « Chiffrer l'empreinte mémoire d'un MoE depuis une trace de routage. » Rend : courbe succès/empreinte par couche, verdict sur l'allocation non uniforme, taille minimale utile d'un cache LRU, structure périodique (Jaccard par écart de couches), extrapolation.
- Positional : `trace` (l.70). Usage l.4-10.
- Options CLI : `--limite` (int, None, "ne lire que les N premiers jetons") l.71-72 — `--modele` (str, None, "nom d'un modèle connu pour l'extrapolation (deepseek4, deepseek41, qwen3moe)") l.73-75. Parser : `description=__doc__`, `RawDescriptionHelpFormatter` l.68-69.
- Constantes/vocabulaire : `connus = {"deepseek4": (43,256,6,5.51), "deepseek41": (40,384,6,9.95), "qwen3moe": (48,128,8,3.05)}` = (couches, experts, top-k, Mo/expert) l.188-192 ; seuils (0.50…0.99) l.95 ; caches testés (topk,16,32,64,128) l.120 ; sortie code 1 si trace vide l.80, modèle inconnu l.194.
- Formats : lit la trace texte « couche jeton expert1 expert2 … » (l.12, produite via `DRAVE_TRACE_EXPERTS`, l.5) ; stdout texte.

### tools/analyse_experts_statique.py  (244 lignes)
- Rôle : « Analyse STATIQUE des experts d'un MoE : que portent les poids eux-mêmes. » Mesures : similarité intra-couche (experts jumeaux), profil de SOURCES (norme de colonne d'entrée), profil de DESTINATIONS (norme de ligne de sortie). « Ne lit que la tête des tenseurs ».
- Positional : `modele` (.gguf) l.175. Usage l.9.
- Options CLI : `--couches` (str, "0,12,24,36,47", sans help) l.176 — `--lignes` (int, 16, "lignes de sortie lues par expert (16 par défaut)") l.177-178 — `--seuil` (float, 0.90, "similarité au-delà de laquelle deux experts sont jumeaux") l.179-180.
- Constantes/vocabulaire : classe `Lecteur` « Lecteur GGUF minimal : en-tête, descripteurs, et octets d'un tenseur » l.35-36 ; tenseurs cherchés `blk.{l}.ffn_gate_exps.weight`, `ffn_up_exps.weight`, `ffn_down_exps.weight` l.190-191 ; clés GGUF `general.architecture`, `{arch}.expert_count` l.184-185 ; types ggml gérés F32=0 et F16=1, sinon ValueError l.167-169 ; `{12:144, 14:210, 8:34, 0:4, 1:2}` l.200 ; seuil « 80 % » n80 l.230.
- Formats : GGUF en-tête + tête de tenseurs ; stdout.

### tools/analyse_flux.py  (95 lignes)
- Rôle : « Analyse PURE d'une trace de flux : ce que la vision appelle “voir le modèle neurone par neurone”, mais chiffré par couche et sans exécuter le moteur. » Répond : quelle couche est creuse (croisement mesuré ~22 % de densité), quels neurones sont PERSISTANTS, recouvrement des top-k entre couches.
- Usage/positional : `analyse_flux.py <trace> [<trace2> ...] [--top 100]` l.16 ; traces limitées à 3 (`[:3]`) l.85.
- Options CLI : `--top` (int, défaut 100, parsé à la main `sys.argv` l.83-84, pas d'argparse, pas de help).
- Constantes/vocabulaire : magie `b"DRVF"`, u16 version, u32 n_layer, u32 hidden ; listes u16 couche / u32 pos / u32 n / f32 echelle ; paires u32 indice + i16 valeur ; sentinelle 0xFFFF (l.24-33) ; persistant si fréquence ≥ 0.9·jetons l.61 ; top1 %/top10 % l.64-65 ; couche ≥1000 → « FFN {couche-1000} » l.74.
- Formats : lit binaire DRVF ; stdout.

### tools/clusters_moe.py  (224 lignes)
- Rôle : « Découpage des MoE en clusters — à partir d'une trace de routage réelle. » Question de placement : quels experts s'allument ENSEMBLE ? Mesures couverture / ventilation (fan-out 90 %) / équilibre, avec témoins aléatoire et fréquence seule.
- Usage/positional : `clusters_moe.py /tmp/routage.txt [--clusters 8] [--json /tmp/clusters.json]` l.23-24 ; `trace` l.144.
- Options CLI : `--clusters` (int, 8, "nombre de groupes visés (nœuds ou GPU disponibles)") l.145-146 — `--json` (str, "", sans help) l.147 — `--graine` (int, 1234, sans help) l.148.
- Constantes/vocabulaire : `partition_equilibree(..., passes=6)` l.60 ; témoin fréquence en tranches ceil(ne/K) l.185-188 ; clés JSON `couches/clusters/n_jetons/n_experts` l.159-160 ; par couche `appris|hasard|frequence|affectation|membres` l.190-191 ; mesures `couverture_moyenne`, `ventilation_moyenne`, `ventilation_max`, `taille_min`, `taille_max` l.130-139.
- Formats : lit la trace texte « couche jeton experts… » (`lire` l.32-42) ; écrit JSON indent=1 si `--json` l.217-219.

### tools/compare_etats.py  (84 lignes)
- Rôle : « Compare les états intermédiaires de Drave à ceux de llama.cpp, tenseur par tenseur. » « La comparaison porte sur les vecteurs entiers, pas sur huit valeurs. »
- Usage/positional : `python3 tools/compare_etats.py <préfixe_drave> <préfixe_ref> <nom> <couche> <positions>` l.15-16 ; exactement 5 (`len(sys.argv)!=6` → SystemExit(__doc__)) l.46-48.
- Options CLI : aucune (pas d'argparse).
- Constantes/vocabulaire : magie `REFD` l.34 ; dispositions `l_last` = [embd, hc, position], `hc_attn_pre` = [embd, position] l.51-56 ; verdicts ✅ si écart max ≤ 1e-4 × dynamique, « ~ » si corr > 0.999, sinon ❌ l.78.
- Formats : Drave = f32 bruts sans en-tête `<préfixe_drave>-<nom>-<couche>-<position>.bin` (écrits par `DRAVE_DUMP_COUCHES`) ; llama.cpp = `<préfixe_ref>-<nom>-<couche>.bin`, en-tête `REFD`+ndim+ne[4] puis f32 ordre ggml (l.5-10, 30-42).

### tools/compare_logits.py  (109 lignes)
- Rôle : « Compare deux fichiers de logits » ; par position NLL de chacun, écart de NLL, rang du jeton cible, accord du top-1 (localise embedding/norme/RoPE/MoE/tête).
- Usage/positional : `compare_logits.py <notre.bin> <reference.bin> [ids.txt]` l.5, 44-47.
- Options CLI : aucune.
- Constantes/vocabulaire : format = int32 n_vocab, int32 n_pos, puis n_pos × n_vocab f32 LE l.2-3 ; numpy optionnel (fallback Python pur) l.15-18 ; échantillon affiché si `i<24 or i%32==0` (l.71, 88) mais accord top-1 compté sur toutes les positions (l.73-76) ; codes retour 2 si ids absents/vides ou <2 ids l.58-65.
- Formats : binaire logits ; ids texte (espaces/virgules) l.47.

### tools/convertir_clusters.py  (525 lignes)
- Rôle : « Convertisseur GGUF → “modèle éclaté en clusters”, un fichier par cluster. » Chaque cluster = GGUF autonome ouvrable seul en mmap. « il ne requantifie rien » : octets copiés tels quels (blocs alignés sur l'axe experts). `<arch>.expert_count` ajusté.
- Usage/positional : `convertir_clusters.py <source.gguf> <dossier> [--clusters 8] [--trace routage.txt] [--mode experts|couches] [--verifier]` l.28-30 ; `source` l.355, `dossier` l.356.
- Options CLI : `--clusters` (int, 8, sans help) l.357 — `--trace` (str, "", "trace de routage (ordre des experts)") l.358 — `--mode` (choices ["experts","couches"], défaut "experts", sans help) l.359 — `--verifier` (store_true, "relit chaque fichier produit et compare les empreintes") l.360-361.
- Constantes/vocabulaire : `TYPES` ggml -> (nom, octets/bloc, éléments/bloc) l.42-48 : 0 F32(4,1), 1 F16(2,1), 2 Q4_0(18,32), 3 Q4_1(20,32), 6 Q5_0(22,32), 7 Q5_1(24,32), 8 Q8_0(34,32), 9 Q8_1(36,32), 10 Q2_K(84,256), 11 Q3_K(110,256), 12 Q4_K(144,256), 13 Q5_K(176,256), 14 Q6_K(210,256), 15 Q8_K(292,256), 39 MXFP4(17,32).
- Formats lus/écrits : sorties `commun.gguf` l.417, `cluster-NN.gguf` l.449/464, `manifeste.json` (champs source, mode, clusters, n_experts, fichiers[fichier, role, octets, tenseurs | experts_locaux, experts_globaux_par_couche, couches], experts[ordre par couche]) l.391-393, 420-422, 455-459, 467-470, `mapping.tsv` avec `# drave-clusters-mapping v1` et colonnes couche/local/global/cluster l.341-348 ; trace lue en texte (couche jeton experts) l.297-305 ; mode experts si `"_exps." in nom` l.377, mode couches = groupes de couches l.396-412 ; vérif sha256 produit vs source l.481-519.

### tools/diff_flux.py  (91 lignes)
- Rôle : « Diff de deux traces de flux d'activation (format DRVF) » : où le flux diverge, à quelle couche, à quel jeton, de combien.
- Usage/positional : `diff_flux.py <traceA> <traceB> [--top 8]` l.8 ; traceA/traceB = sys.argv[1],[2] l.37-38.
- Options CLI : `--top` (int, défaut 8, parsé main l.39-41, pas de help).
- Constantes/vocabulaire : magie `b"DRVF"`, u16 version, u32 n_layer, u32 hidden, listes u16/u32/u32/f32, paires u32+i16, sentinelle 0xFFFF l.14-33 ; comparaison des valeurs DÉQUANTIFIÉES (v × échelle) l.54-61 ; dynamique = echelle·32767 l.70 ; couche ≥1000 → « FFN N » l.85 ; retour 1 si aucune liste commune, 0 si flux identiques l.46-48, 78-80.

### tools/flux_codec.py  (158 lignes)
- Rôle : « Encodeur/décodeur de RÉFÉRENCE du flux d'activation (format DRVF v1 et v2) » ; 2e implémentation du contrat d'échange de la phase 3 (la 1re est en Rust `--trace-flux`).
- Usage/positional : `flux_codec.py <trace>` / `<trace> --jetons N` l.22-25 ; `trace` = sys.argv[1] l.123.
- Options CLI : `--jetons` (int, parsé main, l.146-147).
- Constantes/vocabulaire : `MAGIE=b"DRVF"` l.30 ; `VERSION=2` « ce que ce fichier ÉCRIT ; il LIT la 1, la 2 et la 3 » l.31 ; structs `ENTETE "<4sHII"`, `LISTE "<HIIf"`, `PAIRE_V1 "<Ih"`, `PAIRE_V2 "<Bh"`, `FIN "<H"` l.32-36.
- Format : en-tête DRVF + u16 version + u32 n_layer + u32 hidden ; liste u16 couche/u32 position/u32 n_actifs/f32 echelle ; v1 paires (u32 indice, i16 valeur) ; v2 écarts u8 + i16, écart 255 → indice absolu u16 ; v3 (lecture seule) u32 n_blocs + échelles f16 + paires (u8 écart, i8 valeur) indexées par bloc de 32 l.76-94 ; fin u16 0xFFFF. Mesure citée : v1 132 396 736 o → v2 66 370 408 o (−49,87 %) l.18-20.

### tools/harmony_canonique.py  (72 lignes)
- Rôle : « Construit un identifiant de perplexité au format harmony CANONIQUE » (montage forcé hors distribution : p=0,9999 pour `analysis` contre 0,0001 pour `final`) : message système complet, tour user, canal analysis court, puis canal final portant le texte à noter.
- Usage/positional : aucun positional. Option : `--sans-analysis` (flag testé par `"--sans-analysis" in sys.argv` l.45) = même séquence SANS le message analysis (contrôle).
- Constantes : `Q="/home/stephane/.../Drave/drave-core/target/release/drave"` l.17 ; `M=".../gpt-oss-120b-MXFP4.gguf"` l.18 ; `DEB, FIN, MSG, CANAL = 200006, 200007, 200008, 200005` l.20 ; message système verbatim l.49-53.
- Formats : lit `/tmp/wt2_prefixe.txt` et `/tmp/wt2_suite.txt` l.47-48 ; tokenizer du moteur (`--tokenize --fichier --sortie`) l.28-29 ; écrit `/tmp/harmony_canonique[_sans_analysis].ids` et `.dep` (indice du premier jeton de contenu) l.63-66.

### tools/hc_synthetique.py  (98 lignes)
- Rôle : « Référence numpy des hyper-connexions de DeepSeek-V4, et valeurs-témoins. » Formules recopiées des opérations ggml de `llama.cpp/src/models/deepseek4.cpp` (build_hc_pre, build_hc_sinkhorn, build_hc_post, build_hc_head), PAS du Rust ; sortie collée dans le test Rust `model::tests_hc::hyper_connexions_conforme_a_la_reference`.
- Usage/positional : `python3 tools/hc_synthetique.py` (aucun argument) l.14.
- Options CLI : aucune.
- Constantes : `HC, H = 4, 3` l.18 ; `EPS = 1e-6` (« hyper_connection.epsilon (V4.1) ») l.19 ; `ITERS = 20` (« hyper_connection.sinkhorn_iterations (V4.1) ») l.20 ; graine np 20261002 l.63 ; `scale = [0.5, 1.5, 2.0]` l.67.
- Format de sortie : lignes Rust `const MELANGE/BASE/SCALE/X/Y/PRE/POST/COMB/ENTREE/SORTIE: [f32; N] = [...]` l.79-89 + invariants sommes par destination/source l.90-94.

### tools/lire_meta_gguf.py  (117 lignes)
- Rôle : « Lit les métadonnées d'un GGUF (en-tête seul) et imprime les clés demandées » (ex. `compress_ratios` : quelles couches compressées). Sans motif, imprime tout (listes >64 éléments tronquées l.66-67).
- Usage/positional : `python3 tools/lire_meta_gguf.py <fichier.gguf> [motif ...]` l.10-12 ; sys.argv[1] + sys.argv[2:] l.71-74.
- Options CLI : aucune.
- Constantes : `TYPES` ggml {0:u8,1:i8,2:u16,3:i16,4:u32,5:i32,6:f32,7:bool,8:str,9:array,10:u64,11:i64,12:f64} l.17-18 ; `FIXES` structs LE l.19-21.
- Remarque : `lire_tenseur_f32(chemin, motif, index)` existe APRÈS le bloc `__main__` (l.77-117), non exposée en CLI ; utilise `general.alignment` (défaut 32), F32 seulement.
- Format : GGUF (magie b"GGUF", version u32, n_tensors/n_kv u64).

### tools/mesurer_lecture_experts.py  (81 lignes)
- Rôle : « Lectures d'experts : série contre parallèle, sur un VRAI fichier froid. » Froid forcé par `posix_fadvise(DONTNEED)`, deux passes appariées sur des blocs différents.
- Usage/positional : `tools/mesurer_lecture_experts.py <shard.gguf> [nb_blocs] [nb_fils]` l.4 ; `chemin` l.36, nb_blocs défaut 240 l.37, nb_fils défaut 16 l.38.
- Options CLI : aucune.
- Constantes : `PAGE = 4096` l.24 ; `taille_bloc = 4 << 20` (4 Mo ≈ un expert) l.39 ; `debut = taille // 2`, `zone_b = debut + nb_blocs*taille_bloc` l.45-47.
- Format : mmap PROT_READ du GGUF ; stdout Go/s série vs parallèle + rapport ×.

### tools/mla_synthetique.py  (250 lignes)
- Rôle : « Modèle MLA synthétique + référence numpy — le harnais du chantier 5. » Modèle minuscule (poids aléatoires, formes MLA correctes) écrit en GGUF + référence numpy indépendante (cache KV latent : 1 tête de 128 + 32 valeurs par jeton).
- Usage/positional : `mla_synthetique.py --sortie /tmp/mla_minuscule.gguf --dossier /tmp/mla_ref` l.15-16 ; aucun positional.
- Options CLI : `--sortie` (str, "/tmp/mla_minuscule.gguf", sans help) l.226 — `--dossier` (str, "/tmp/mla_ref", sans help) l.227 — `--graine` (int, 1234, sans help) l.228 — `--n` (int, 8, "jetons d'entrée") l.229.
- Constantes : `H=64` hidden, `NL=2`, `NH=4`, `NKV=1` (MLA = MQA), `QL=32` q_lora_rank, `KVL=48` kv_lora_rank, `QKR=16` qk_rope, `QKN=16` qk_nope, `VD=16` value_length, `FFN=128`, `VOCAB=64`, `EPS=1e-5`, `ROPE_BASE=10000.0` l.28-40.
- Formats : GGUF version 3, tenseurs F32 (type 0), alignement 32 l.176-206 ; noms `token_embd.weight`, `output_norm.weight`, `blk.N.attn_q_a`, `attn_q_a_norm`, `attn_q_b`, `attn_kv_a_mqa`, `attn_kv_a_norm`, `attn_kv_b`, `attn_output`, `ffn_*` l.50-70 ; dossier : `logits.npy`, `ids.npy`, `forme.json` (hidden, n_layer, n_head, q_lora, kv_lora, qk_rope, qk_nope, v_dim, ffn, vocab, graine) l.237-242.

### tools/pair_factice.py  (140 lignes)
- Rôle : « Pair factice du protocole de flux (v2) : il ÉCOUTE et DIT ce qu'il reçoit. » Un pair qui parle le protocole sans calculer le modèle rend visible ce que l'autre bout envoie (tailles, positions, modes, réglages) ; répond un flux de la dimension demandée.
- Usage/positional : `python3 tools/pair_factice.py <port> [dimension]` l.10 ; port défaut 45760 l.32, dimension défaut 896 l.33.
- Options CLI : aucune.
- Constantes/vocabulaire : `MAGIE = 0x44525631` l.14 ; `TETE = 79` (en-tête v4 : magie, version, mode, plage, position, n, échelle, niveaux, seuil, top-k, renorm, 7 top-k par projection, 3 top-k globaux) l.15-16 ; `MODES = {0:"dense f32", 1:"listes quantifiées", 2:"blocs (i8 + écarts)", 3:"lot dense (t états × dimension)", 4:"lot en listes (mode 2 par état)"}` l.17-18.
- Protocole : réponse `struct.pack("<IBBIIIIfffIBIIIIIIIIII", ...)` l.115-117 ; mode 3 = n états × dimension × 4 ; mode 4 = n états à liste vide, nb = (dimension+31)//32 blocs ; mode 2 = nb blocs + échelles f32 + longueur 0 ; dense = dimension × 4 (l.118-134) ; invariants mode 4 vérifiés (`nb` attendu, `2a ≤ lg ≤ 4a`) l.80-86 ; écoute 127.0.0.1.

### tools/profil_flux.py  (78 lignes)
- Rôle : « Profilage par neurone à partir d'une trace de flux (format DRVF) » — quels neurones s'allument, à quelle fréquence, avec quelle magnitude, par couche.
- Usage/positional : `profil_flux.py <trace> [--couche N] [--top 6] [--csv sortie.csv]` l.8 ; `trace` = sys.argv[1] l.37.
- Options CLI RÉELLES : `--top` (int, défaut 6, parsé main l.39-40) — `--csv` (chemin, parsé main l.42-43). ⚠️ DISCRÉPANCE : `--couche N` est annoncé l.8 mais n'est jamais lu/implémenté.
- Constantes/vocabulaire : format DRVF identique à analyse_flux l.14-33 ; top10 % = len(forts)//10 l.61 ; couche ≥1000 → « FFN N » l.64.
- Formats : lit DRVF ; CSV en-tête `couche,neurone,magnitude,frequence` l.70.

### tools/proxy_latence.py  (54 lignes)
- Rôle : « Relais TCP qui ajoute une latence par message, pour mesurer ce qu'un lien distant coûte à un découpage de modèle » (le débit n'est jamais le problème — 0,25 Mbit/s — la latence si).
- Usage/positional : `python3 tools/proxy_latence.py <port_écoute> <hôte_cible:port> [délai_ms]` l.10 ; port l.35, `hôte:port` (rsplit ":",1) l.36, délai ms→s défaut 0.0 l.37.
- Options CLI : aucune.
- Constantes : recv 65536 l.18 ; bind 127.0.0.1, `listen(4)`, TCP_NODELAY sur les deux sockets l.40-48 ; un thread daemon par direction l.49-50.

### tools/session_report.py  (341 lignes)
- Rôle : « Produit, pour chaque session DSH, un rapport qui reconstitue son essence et démontre le travail accompli, étape par étape. » Contenu : fiche, demandes, déroulé, travail, mesures, erreurs, commits (l.10-19).
- Usage/positional : `python3 tools/session_report.py [--repo DIR] [--session ID] [--quiet]` l.22 ; aucun positional.
- Options CLI : `--repo` (str, défaut `Path(__file__).resolve().parent.parent`, sans help) l.293 — `--session` (str, None, sans help) l.294 — `--quiet` (store_true, sans help) l.295.
- Constantes : `TRONC_SORTIE=700`, `TRONC_DEMANDE=700`, `TRONC_SYNTHESE=2500` l.38-40 ; `MOTIFS_MESURE` regex (tok/s | G év | MHz | ALMs | M20K | DSP | Go/s | Mo | Ko | % | ms, ou perplexité|surcoût|résidu|rang|R²|× suivi d'un nombre) l.45-49 ; `MOTIFS_ERREUR` regex (exit code [1-9], panicked at, ^Error, ^error[, ECHEC/ÉCHEC, DIVERGENT au rang, Error (n), fatal error) l.50-52.
- Formats : lit `$DSH_HOME/sessions/--<slug>--/session.jsonl*` (zstd via `zstd -dc` si `.zstd`) l.55-61, 299-317 ; JSONL par `type` : session, session/title, turn/start, user/message, assistant/message, tool/call, tool/result l.112-169 ; écrit `journal/sessions/<id>/rapport.md` et `journal/README.md` l.7-8, 306-336 ; sections « ## Objectifs déclarés », « ## 1. Ce qui a été demandé », « ## 2. Déroulé, étape par étape », « ## 3. Travail accompli », « ## 4. Mesures et résultats marquants », « ## 5. Erreurs rencontrées », « ## 6. Commits » l.211, 216, 222, 245, 263, 276, 283 ; retour 1 si aucune session l.303-304.

### tools/telecharger_modeles.py  (197 lignes)
- Rôle : « Télécharge les modèles LOURDS, par tranches, avec reprise. » Le pont Xet de HF refuse un GET plein sur le fichier de 365,7 Go (HTTP 400) mais sert une requête `Range` (HTTP 206).
- Usage/positional : `--manifeste tools/manifeste_modeles_lourds.json` / `--seulement Kimi-K2.7-Code-UD-IQ1_M` / `--etat` l.12-15 ; aucun positional.
- Options CLI (aucun `help=`) : `--manifeste` (str, "tools/manifeste_modeles_lourds.json") l.127 — `--dest` (str, DEST_DEFAUT) l.128 — `--seulement` (str, "") l.129 — `--etat` (store_true) l.130 — `--journal` (str, "/tmp/telechargement_lourds.log") l.131.
- Constantes : `RACINE="https://huggingface.co"` l.25 ; `CHUNK = 256 << 20` l.26 ; `DEST_DEFAUT="/home/stephane/Data13TB/stephane/modeles/gguf"` l.27 ; `LIBRE_MINIMUM_GO = 300` l.28 ; `telecharger(..., fils=6, essais=6)` l.69, `_tranche(..., essais=6)` l.35 ; curl `-sSL -f --retry 3 --retry-delay 10 --retry-all-errors -r pos-haut` l.48-51.
- Formats : manifeste JSON (entrées `nom`, `repo`, `chemin`, `octets`) l.134, 177-178 ; URL `{RACINE}/{repo}/resolve/main/{chemin}` l.178 ; fichier préalloué + sidecar `<dest>.etat.json` (position absolue par tranche) + temporaires `.part<cle>` l.41-64, 155-165 ; `--etat` lit le sidecar (getsize = 100 % dès le 1er octet sinon) l.147-174.

### tools/trace_compacite.py  (432 lignes)
- Rôle : « Chiffre ce que coûterait une trace DRVF v1 sous plusieurs encodages. » Disque = 6 o/neurone actif (u32+i16), réseau ≈ 2 o/actif ; variantes `actuel`, `écarts+i16`, `écarts+blocs`, `blocs f16`, zstd/gzip. Lecture du format déléguée à `tools/flux_codec.py` (implémentation de référence).
- Usage/positional : `python3 tools/trace_compacite.py <trace.bin> [options]` l.29 ; `trace` l.286.
- Options CLI : `--couches` (store_true, "ventilation par couche") l.287-288 — `--sans-compression` (store_true, "saute le point de repère zstd/gzip") l.289-290 — `--sans-erreur` (store_true, "saute le calcul de l'erreur de quantification i8") l.291-292 — `--echantillon` (float, 16.0, metavar="Mio", "taille de l'échantillon compressé (défaut : 16 Mio)") l.293-294 — `--zstd-v2` (store_true, "compresse aussi la variante écarts+blocs reconstruite") l.295-296.
- Constantes : `BLOC = 32` l.56 ; `ECHAPPEMENT = 255` l.57 ; `TAILLE_ENTETE_FICHIER = 14` l.58 ; `TAILLE_ENTETE_LISTE = 10` l.59 ; `TAILLE_QUEUE_BLOCS = 8` l.60 ; import `flux_codec` via sys.path l.53-54.
- Formats/vocabulaire : variantes "actuel","i16","blocs","f16" + postes "blocs_utiles","blocs_emis","echappements","n_err","err2" l.351-380 ; retour 1 si trace introuvable, non DRVF ou sans activation l.299-313.

### tools/verifier_formats.py  (108 lignes)
- Rôle : « Compare notre déquantification d'un super-bloc à celle de libggml » — référence = `tools/ref_ggml_bloc.c`, côté Rust via `drave <modele> --bloc <tenseur>:<index>` (chemin row_f32). Sortie : écart max + verdict, retour 1 si divergence.
- Usage/positional : `tools/verifier_formats.py <modele.gguf> <tenseur> [index] [--type N]` l.4 ; modele l.58, tenseur l.58, index défaut 0 l.59-67.
- Options CLI : `--type` (int, forcé, parsé main l.64-65).
- Constantes : `RACINE` = racine du dépôt l.26 ; `DRAVE = RACINE/drave-core/target/release/drave` l.27 ; `REF = os.environ.get("REF_GGML_BLOC", "/tmp/ref_ggml_bloc")` l.28 ; `OCTETS_256` l.31-51 : 0 F32 1024, 1 F16 512, 2 Q4_0 144, 3 Q4_1 160, 6 Q5_0 176, 7 Q5_1 192, 8 Q8_0 272, 10 Q2_K 84, 11 Q3_K 110, 12 Q4_K 144, 13 Q5_K 176, 14 Q6_K 210, 16 IQ2_XXS 66, 18 IQ3_XXS 98, 19 IQ1_S 50, 23 IQ4_XS 136, 29 IQ1_M 56, 30 BF16 512, 39 MXFP4 136.
- Import : `from analyse_experts_statique import Lecteur` l.23-24 ; CONCORDE si écart < 1e-6 ; codes retour 2 (usage/type non couvert/rien rendu), 1 (DIVERGE), 0 l.96-104.

### tools/vision_mtmd.py  (159 lignes)
- Rôle : « Référence de vision : interroger libmtmd d'ollama, sans en-têtes. » Seule vérification qui tranche rotation 2-D, fenêtre locale et fusion 2×2 du ViT Qwen2.5-VL : compare la sortie complète de llama.cpp (via ollama) aux 3 584 valeurs du projecteur. Structure de params opaque et généreuse (256 o).
- Usage/positional : `vision_mtmd.py <modele.gguf> <mmproj.gguf> [sortie.bin]` l.15 ; modele défaut MODELE l.59, mmproj défaut MMPROJ l.60, sortie optionnelle l.150.
- Options CLI : aucune.
- Constantes : `OLLAMA = "/usr/lib/ollama"` l.22 ; `MODELE = .../Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf` l.23 ; `MMPROJ = .../mmproj-Qwen2.5-VL-7B-Instruct-f16.gguf` l.24 ; `TAILLE_PARAMS = 256` l.25 ; backends chargés explicitement `libggml-cpu-haswell/alderlake/sandybridge` l.44-45 ; image déterministe 336×336 (dégradé + carré central) l.76-85 ; 3584 valeurs attendues (projection_dim du mmproj) l.146 ; invite `"<|im_start|>user\n<marker>\ndecris cette image<|im_end|>\n<|im_start|>assistant\n"` l.117 ; type de morceau image = 1 l.138.
- Format écrit : `sortie.bin` = i32 longueur + N f32 l.151-153.

### tools/vision_ref.py  (162 lignes)
- Rôle : « Référence numpy de l'embedding de patchs (première tranche du chemin image). » Le moteur écrit les sorties (`--banc-vision`) et les POIDS lus dans le GGUF ; ce script refait le CALCUL (même partage des rôles que MLA).
- Usage/positional : `vision_ref.py <sortie.bin> [--poids <sortie.bin.poids>]` l.9 ; `sortie` = sys.argv[1] l.28 ; poids = sys.argv[2] si fourni, sinon `sortie + ".poids"` l.29.
- Options CLI : aucune. ⚠️ le `[--poids …]` du docstring n'est pas une option : c'est un 2e positional (passer littéralement `--poids` donnerait un chemin « --poids »).
- Constantes : `erf` vectorisé Abramowitz-Stegun 7.1.26 (même approximation que le moteur) l.15-25 ; image du banc cote=28, carré central 10≤x<18 l.38-44 ; GELU exact `0.5*h*(1+erf(h/√2))` l.75 ; eps LayerNorm 1e-6 l.109 ; rotation 2-D mRoPE : 4 blocs de hd/4, blocs 0/2 par la LIGNE, 1/3 par la COLONNE, base 10000, 16 têtes l.114-137 ; DÉSACCORD si écart relatif > 1e-5 l.156.
- Formats lus : `sortie.bin` = i32 n_patch, i32 cout puis n_patch×cout f32 l.30-33 ; `sortie.bin.poids` = i32 cout, cin, ky, kx puis f32 (reshape [cout,cin,ky,kx]) l.34-36 ; `sortie.bin.projecteur` = 4 i32 (n0,n1,n2,n3) + w0,b0,w2,b2 f32 l.65-72 ; `sortie.bin.bloc` = 3 i32 (npatch, e, nff) + poids f32 (ln1, ln2, wq/bq, wk/bk, wv/bv, wo/bo, wg/bg, wu/bu, wd/bd, x_eng) l.92-108.

POINTS TRANSVERSAUX
1. argparse : 9 scripts seulement (aiguille, analyse_empreinte, analyse_experts_statique, clusters_moe, convertir_clusters, mla_synthetique, session_report, telecharger_modeles, trace_compacite) ; les 15 autres parsent `sys.argv` à la main.
2. Docstrings qui annoncent des options inexistantes : `profil_flux.py --couche N` (l.8 vs main l.36-43) et `vision_ref.py --poids` (l.9 vs l.29, simple 2e positional).
3. Le format DRVF est réimplémenté 4 fois (analyse_flux, diff_flux, profil_flux, flux_codec) ; trace_compacite réutilise flux_codec par import.
4. Vocabulaire commun : couche ≥ 1000 = « FFN {couche-1000} » (analyse_flux l.74, diff_flux l.85, profil_flux l.64, trace_compacite l.422).

Aucun fichier modifié (lecture seule stricte). Résultat complet également transmis au parent (f2de810a-b765-444d-b3cc-d8fce1ba2105).

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 45, "offset": 2158}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
2158:                               k_f16, kp: Vec::new(),
2159:                               kf: Vec::new(), vf: Vec::new(),
2160:                               kq: Vec::new(), vq: Vec::new(), sk: Vec::new(), sv: Vec::new(),
2161:                               nb };
2162:         c.assurer(ctx.min(1024));
2163:         c
2164:     }
2165: 
2166:     /// Garantit `besoin` positions allouées (doublement, avec recopie : les
2167:     /// positions déjà écrites le restent). Chaque tête KV a son bloc contigu,
2168:     /// donc la recopie se fait tête par tête.
2169:     pub fn assurer(&mut self, besoin: usize) {
2170:         if besoin <= self.cap { return; }
2171:         // ⚠️ `besoin > ctx` faisait BOUCLER SANS FIN : `cap` plafonne à `ctx` et la
2172:         // condition reste vraie. Mesuré : une invite de 4 731 jetons avec
2173:         // `--ctx 4608` tournait à ~1 700 % de CPU pendant plus de 22 minutes sans
2174:         // jamais finir (livelock, pas ralentissement). Le même défaut avait été
2175:         // corrigé côté GPU au sprint 2 (`kv_assurer`) ; le chemin 
… [1505 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '436,470p' drave-core/src/gpu.rs; echo \"=== troncature generate ===\"; grep -n 'ABANDONNÉS\\|tronqu\\|ctx - n_new\\|contexte plein\\|génération arrêtée' drave-core/src/model.rs | head -20", "description": "Check livelock fixe … [3 caractères tronqués]`

  ```
}

    /// Garantit `besoin` positions allouées. Double la capacité (et COPIE ce qui
    /// était écrit : le cache est déjà rempli) jusqu'à couvrir la demande.
    pub fn kv_assurer(&self, m: &mut KvGpu, besoin: usize) -> bool {
        cu_ctx(self.ctx);
        if besoin <= m.capacite { return true; }
        // Sans ce garde, `cap` plafonne à `m.ctx` et la boucle de doublement ne
        // termine jamais : un appelant qui demande plus que le contexte déclaré
        // pendait le processus au lieu de recevoir `false`.
        if besoin > m.ctx { return false; }
        let mut cap = m.capacite.max(1);
        while cap < besoin { cap = (cap * 2).min(m.ctx); }
        let pas = match m.bits { 32 => m.hd * 4, 8 => m.hd, 4 => m.hd / 2, _ => return false };
        let donnees = m.n_kv * cap * pas;
        let echelles = if m.bits >= 32 { 0 } else { m.n_kv * cap * m.nb * 4 };
        let total = donnees * 2 + echelles * 2;
        if total > self.memoire_libre { return false; }
        unsafe {
            let (mut k, mut v, mut sk, mut sv) = (0u64, 0u64, 0u64, 0u64);
            if cuMemAlloc_v2(&mut k, donnees) != 0 { return false; }
            if cuMemAlloc_v2(&mut v, donnees) 
… [1298 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== nb de #[test] par fichier ===\" && grep -c '#\\[test\\]' drave-core/src/*.rs; echo \"TOTAL: $(grep -rh '#\\[test\\]' drave-core/src/*.rs | wc -l)\"; echo; echo \"=== model.rs:3905-3915 (cite par sprint 3) ===\"; sed -n '39 … [188 caractères tronqués]`

  ```
=== nb de #[test] par fichier ===
drave-core/src/clusters.rs:6
drave-core/src/engine.rs:2
drave-core/src/formats.rs:1
drave-core/src/gguf.rs:10
drave-core/src/gpu.rs:0
drave-core/src/list.rs:6
drave-core/src/main.rs:14
drave-core/src/materiel.rs:3
drave-core/src/model.rs:11
drave-core/src/tokenizer.rs:0
TOTAL: 53

=== model.rs:3905-3915 (cite par sprint 3) ===
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

=== model.rs:6398-6415 (troncature) ===
        // Invite plus longue que le contexte : on garde les DERNIERS jetons (le
        // début d'un long document est ce qu'on peut perdre avec le moins de
        // dégâts) et on le DIT. Sans ce garde, `KvCache::assurer` bouclait sans
        // fin — un hang, pas une erreur — et rien ne l'annon
… [770 caractères tronqués]
  ```

- **list_agents** `{}`

  ```
2c2a6595-b208-446e-bbd1-d0f49eca45e8 [running] — Extract Rust CLI flags part 1
18b8879c-f211-43b8-9908-cf65e509b21d [running] — Extract Rust flags part 2
b13a6032-4f62-4e86-aa1f-03864a455c83 [ready] — Extract Python tool headers
dcaa24d6-0017-4382-be21-8244c0fb9b7a [ready] — Extract shell script headers
  ```

### 👤 Utilisateur

Agent 2c2a6595-b208-446e-bbd1-d0f49eca45e8 sent a message:
RAPPORT CLI/CONFIG — drave-core/src/{main.rs,list.rs,engine.rs} (lecture seule, aucun fichier modifié)

FAIT MAJEUR : aucun clap/structopt. Toute la ligne de commande est analysée à la main dans `analyser()` (main.rs:580-742), en UNE passe. Chaque branche rend le nombre d'arguments consommés (1 booléen, 2 à valeur) — main.rs:596-603. `args[1]` est TOUJOURS le chemin du modèle (MODELE OnceLock, main.rs:88/390) ; l'analyse démarre à i=2 (main.rs:594). Aide = uniquement les eprintln de main.rs:51-64 (+ doc module main.rs:3-9) ; il n'existe AUCUN `--help`/`-h`/`--version` (grep négatif). Si args.len()<2 : usage puis exit(1) (main.rs:50-66). Aucun drapeau n'existe dans list.rs ni engine.rs (grep `--[a-z]` : 0 hit dans ces 2 fichiers).
93 drapeaux reconnus (93 branches + le `_` attrape-tout = 94 `=> {}`).
Mécanique : un drapeau à valeur placé en DERNIER argument panique « {flag} attend une valeur » (suivant(), main.rs:591-593) — SAUF --bloc/--tete-garantie/--tete-restreinte, gardés par `if i+1 < args.len()` (698-702) : en dernière position ils tombent dans la branche inconnue, sans panique. Drapeaux inconnus : retenus dans `inconnus` (714-724 ; détecte `--xxx` ET la faute `-xxx` où l'octet 2 est alphabétique), avertis en 728-732, puis `--options-strict` => exit(2) (733-737). Effets de bord immédiats : `--pin` -> engine::EPINGLER.store(true) (739) ; `--bits`>0 -> list::BITS_POIDS.store(bits) (740).
Défauts posés dans `analyser` (581-590) : n=32, temp=0.0, top_p=1.0, hist=64, hebb_q=0.1, hebb_out="hebb.bin", keep=1.0, abits=8, auto=true, limit=usize::MAX, matrix="blk.0.ffn_gate.weight", ctx=512, threads=coeurs_physiques().max(1) ; tout le reste = `Default` (0/false/None/Vec vide).
Défauts PAR MODE : inférence ctx 512/abits 8 (775-777) ; perplexité ctx 256/abits 16 (4303-4305) ; --flux-serveur ctx 4096 (2480) ; --ppl-reparti ctx 256 + couches_locales 12 (2606-2608) ; --banc-mla ctx 4096 figé (3449) ; --banc-kv DRAVE_KV_BITS défaut 32 (3492) ; --banc-topk DRAVE_KV_BITS défaut 8 (2872) ; --sonder-engram défaut 1000 (697).
Sous-commandes / modes = 16 sélecteurs, ordre de priorité d'exécution main.rs:91-121 : materiel > config > sonder-engram > bloc > banc-vision > flux-serveur > ppl-reparti > tensors > banc-mla > banc-kv > banc-topk > gpu-banc > plan > tokenize > ppl > infer ; sinon chemin HISTORIQUE sans mode = banc « mesure sur le vrai modèle » (3 sections, main.rs:122-380) qui RE-ANALYSE --matrix/--threads dans sa propre boucle (137-146). Si >1 mode demandé : avertissement `[modes]` (102-105). NB : `--bloc` est absent de ce tableau de diagnostic.
TEXTE D'AIDE EXACT (main.rs:51-64) :
  « usage: drave <modele.gguf|dossier-de-clusters> [--matrix NOM] [--threads N] »
  «        drave <modele> --infer (--ids 1,2,3 | --prompt TEXTE | --ids-file F) »
  «              [--n 32] [--temp 0] [--ctx 512] [--threads N] »
  «        drave <modele> --ppl FICHIER-IDS [--ctx N] [--limit N] [--dense] »
  «        drave <modele> --tensors      inventaire par les en-têtes seuls »
  «        drave <modele> --materiel     détection matérielle et plan de configuration, AVEC la raison de chaque choix — ne charge pas le modèle »
  «        drave <modele> --sonder-engram N   accès mmappé à une table d'engram »
  «        drave <modele> --tete-restreinte F  génération CONTRAINTE : la tête ne calcule que les tokens de F. Change la sortie — refusé en perplexité. »
  «        (un dossier contenant commun.gguf EST un modèle ; DRAVE_CLUSTERS=0,3 ne charge que certains clusters ; DRAVE_MMAP=0 lit au lieu de mapper) »
Doc module (main.rs:3-9) : « drave-core <modele.gguf> [--matrix blk.0.ffn_gate.weight] [--threads 8] ».

============ (a) DRAPEAUX GLOBAUX / TRANSVERSES ============
Format : `--nom` — main.rs:LIGNE — effet — portée — argument/défaut.
--options-actives — 618 — arme le tableau de bord final (options_actives, 393-452) imprimé APRÈS toutes les affectations ; booléen — inférence (855-857), perplexité (4409-4411), --flux-serveur (2483), --ppl-reparti (2615) ; ignoré ailleurs. Sortie : « [options] mode … contexte … dense … keep », niveaux/seuil/k-WTA/renorm, top-k (attn, q·k, MoE, par projection), couches début..fin, flux brut/trace/rejeu, fenêtre/motif/seuil push/lot/ffn_gain/hebb, cache KV, et le verdict « top-k déporté (DRAVE_GPU_TOPK) : ACTIF|inactif : … » (430-450).
--options-strict — 619 — un drapeau inconnu n'est plus un avertissement mais une ERREUR (exit code 2, message 734-736) ; booléen — global ; vérifié en fin d'analyse (733).
--threads N — 651 (+ copie legacy 141-143) — fixe les fils de calcul ; pose aussi `threads_impose=true` (650-651) ; usize — inférence 776, perplexité 4304, flux-serveur/ppl-reparti via `fils()` 457-463, banc-topk 2946, banc-kv 3551, gpu-banc 3661 ; défaut = engine::coeurs_physiques().max(1). ATTENTION : la docstring de `fils()` (454-456) dit « sinon la moitié des cœurs » et le commentaire 530-533 « la moitié des cœurs contre les trois quarts », mais le code rend `cpu.max(1)` = TOUS les cœurs physiques (460-462). Même écart en inférence (770-776).
--ctx N — 650 — longueur de contexte, pose `ctx_impose=true` ; usize — défaut 512 (589) ; par mode : 512 inférence, 256 perplexité, 4096 flux-serveur, 256 ppl-reparti, 4096 banc-mla (figé) ; en --plan il pilote le chiffrage KV au lieu du `context_length` du modèle (4058-4064).
--abits N — 652 — bits d'activation, pose `abits_impose=true` ; u32 — défaut 8 ; calcul `act_levels = (1<<(abits-1))-1` (803, 4368) ; défauts par mode 8 (inférence) / 16 (perplexité) / 8 dans les modes flux (appliquer_quantification, 1874).
--bits N — 653 — précision SIMULÉE des poids (bits conservés, 0 = tous les 8) stockée dans list::BITS_POIDS ; u32 ; défaut 0 ; lue par list.rs:456 (`dot_q8_source`). Le stockage est fait à la fin de `analyser` (740).
--limit N — 654 — plafond ; usize, défaut usize::MAX (584) — --ppl : nombre de jetons de CONTENU chargés (4314-4317, 4353-4354) ; --ppl-reparti : `limit.max(1).min(ctx)` (2607) ; --gpu-banc : « plafonne le nombre de lignes : c'est ce qui permet de distinguer un noyau qui boucle d'un transfert qui bloque » (3723-3725).
--depuis N — 655 — commence la NOTATION au jeton N (les précédents servent de contexte) ; usize, défaut 0 — --ppl seulement (4314-4316, 4363-4366, 4429-4432).
--keep F — 657 — fraction de poids conservés passée à Model::load_partiel ; f32, défaut 1.0 ; modes inférence (778), perplexité (4333), flux-serveur (2481), ppl-reparti (2613), banc-mla (3449) ; « `--keeep 0.05` (une faute de frappe) faisait tourner le modèle entier sans élagage et sans un mot » (496-497).
--dense — 688 — force le chemin dense ; booléen ; inférence (778), perplexité (4333), banc-mla (3449) ; défaut false.
--auto — 689 — remet `auto=true` (défaut) ; booléen ; mêmes modes.
--push — 690 — `o.auto=false; o.dense=false` — force le chemin « push » (dispersion PushMat) ; booléen ; mêmes modes.
--pin — 691 — épingle les workers aux processeurs (EPINGLER) ; booléen ; global, effet immédiat en fin d'analyse (739). Utilisé par engine::Pool::new (engine.rs:422-430, cibles_locales 332-360).
--sans-yarn — 693 — désactive la rotation YaRN (`mdl.cfg_yarn_off()`) ; booléen — inférence 845, perplexité 4386.
--matrix NOM — 639 (+ copie legacy 140) — nom du tenseur ciblé ; String, défaut "blk.0.ffn_gate.weight" (585) — chemin historique (195), --gpu-banc (choix du noyau MXFP4/Q6_K/Q4_K/Q8_0, 3665-3684).
--patch F — 643 — charge un greffon `model::Patch::load` et imprime couche/|u|/|v|/|d| ; Option<String> — inférence 924-930, perplexité 4369-4375.
--ffn-gain C:G — 676-679 — gain FFN « couche:gain » (split ':' en 2 champs) ; Option<(usize,f32)> — inférence 837-840 (« `--ffn-gain` était appliqué en perplexité et JAMAIS déstructuré ici », 835-836), perplexité 4376-4379.
--act-thresh F — 667 — seuil de parcimonie (fraction du max ; affiché « seuil {:.1} % » = ×100) ; f32, défaut 0.0 — inférence 805/846-849, perplexité 4380/4398-4401, modes flux via appliquer_quantification 1876 ; voyage dans l'en-tête de flux (1936-1938 : « 0,69 d'écart de perplexité avec un seuil 0,05 d'un côté et 0,00 de l'autre »).
--act-topk N — 668 — k-WTA ; usize, défaut 0 ; affiché « k-WTA garde {:.1} % » = N/10.0 pour cent (848), et « k-WTA k={act_topk} » en perplexité (4401) ; appliqué 806, 4381, 1877.
--act-renorm — 694 — renormalise les activations après sélection ; booléen ; 808, 4382, 1878 (et transporté dans l'en-tête, bit renorm 1973).
--topk-q/-k/-v/-o/-gate/-up/-down N — 669-675 — top-k PAR PROJECTION, index 0..6 de `topk_proj[7]` dans l'ordre q,k,v,o,gate,up,down ; usize, défaut [0;7] — inférence 809, perplexité 4383, flux 1882 ; « topk est une FRACTION de la dimension » (1951-1953) ; transportés sur le fil (1940, 2105).
--moe-topk N — 658 — top-k du routeur MoE ; usize, défaut 0 — inférence 804, perplexité 4367, flux 1885.
--attn-topk N — 662 — top-k d'attention ; usize, défaut 0 — inférence 843, perplexité 4384, flux 1883 ; --banc-topk : `k = if opt.attn_topk > 0 { opt.attn_topk } else { 256 }` (2965) ; condition d'activité du top-k GPU : k∈[1,1024] (433-438).
--qk-topk N — 663 — top-k des scores q·k ; usize, défaut 0 — 844, 4385, 1884.
--attn-window N — 659 — fenêtre d'attention ; usize, défaut 0 — précédence : `--sans-fenetre` d'abord (met 0) PUIS `--attn-window` s'il est >0 (810-811 ; identique en perplexité 4389-4390, « l'ordre était inversé entre les deux modes » 4387-4388).
--sans-fenetre — 692 — `mdl.attn_window = 0` ; booléen — 810, 4389.
--swa-pattern N — 660 — motif de couches à fenêtre glissante (`mdl.swa_pattern`) ; Option<usize>, défaut None — 812, 4391 ; affiché « motif {} » dans options_actives (414-415) et « motif {} (imposé par la ligne de commande) » (4392-4395) ; en --plan, gpt-oss => motif 2 (4075-4078).
--attn-sinks N — 661 — puits d'attention (attention sinks) ; usize, défaut 0, appliqué seulement si >0 — 813, 4397.
--ids 1,2,3 — 632-633 — liste d'identifiants séparés par des virgules ; Vec<u32> — inférence (source des jetons, 760/916), --ppl-reparti (2630-2636, tronqué à `limite`), --banc-mla (3454-3456, défaut 1..=8).
--trace-flux F — 615 — enregistre le flux d'activation dans F ; Option<String> — inférence 817-823 (« `--trace-flux` était ignoré en inférence : on le branche », 814-816), perplexité 4345-4351 ; --banc-mla l'IGNORE en le disant (3444-3447).
--flux-forcer F — 616 — rejoue une trace (les activations enregistrées remplacent celles calculées) ; Option<String> — inférence 824-834 (« Le REJEU aussi : `--flux-forcer` était ignoré en inférence, sans un mot »), perplexité 4335-4344 ; refusé/ignoré en --banc-mla (3444-3447).
--trace-couches N,N — 629-630 — liste de couches à tracer (vide = toutes, doc Options 513-514) ; Vec<usize> par split(',') + trim ; passé à model::TraceFlux::nouveau (818, 4346).
--logits-bin F — 640 — journal des logits (vocab i32, n_pos i32 réécrit à la fin, puis f32) ; Option<String> — perplexité seulement (4474-4486, 4570-4577).
--hebbian N — 664 — capteur hebbien sur la couche N ; Option<usize> — inférence 931-937 (couche, projection gate n_out×n_in, quantile), perplexité 4412-4417 (journalisation, `hb.log_on = true`).
--hebb-q F — 665 — quantile du capteur hebbien ; f32, défaut 0.1 — 934, 4413.
--hebb-out F — 666 — fichier de sortie du capteur ; String, défaut "hebb.bin" — inférence 1073-1080, perplexité 4617-4621 (écrit aussi "{hebb_out}.perte").
--profil-neurones — 703 — profilage des neurones « chauds » (idée PowerInfer) ; booléen — perplexité 4418-4422 (`mdl.activer_profil_neurones()`).
--neurones-sortie F — 641 — fichier du classement de neurones ; Option<String> — perplexité 4586-4593.
--harmony / --harmony-assistant / --harmony-user / --harmony-suite — 704-707 — choisissent le mode de fenêtrage harmony (gpt-oss) en posant `harmony = Some("alterne"|"assistant"|"user"|"suite")` ; booléens (1 arg) — perplexité 4427/4454-4468 ; modes documentés 4153-4156 : « `alterne` (user/assistant), `assistant` (tout en canal final), `user` (tout en rôle user), `suite` (une consigne courte en rôle user, puis le texte entier en canal assistant) ».
--harmony-contexte F — 642 — fichier de contexte pour le mode harmony ; Option<String> — perplexité 4459-4461 (« le contexte (si fourni) remplace la consigne générique », 4195-4202).
--q4 / --q4-ffn / --q4-attn / --q4-tout — 708-711 — masque `q4: u8` : `--q4` => `q4 |= 3` ; `--q4-ffn` => `q4 = (q4 & 4) | 1` ; `--q4-attn` => `q4 = (q4 & 4) | 2` ; `--q4-tout` => `q4 |= 7` (donc bit0=FFN, bit1=attention, bit2=posé par -tout et préservé par -ffn/-attn) ; booléens — inférence 763/778, perplexité 4291/4333 ; sémantique finale dans model::load_partiel (hors des 3 fichiers).
--bits-attn N / --bits-ffn N — 680-681 — N'est lu QUE si N==6 : `b6 |= 2` (attn) / `b6 |= 1` (ffn) ; toute autre valeur n'a AUCUN effet (pas d'avertissement) ; u32 — inférence 763/778, perplexité 4291/4333.
[légacy sans mode] --matrix/--threads — 140-143 — seuls drapeaux reconnus par la boucle du chemin historique (2 max).

============ (b) DRAPEAUX PAR SOUS-COMMANDE ============
--infer — 604 — sélectionne la génération autorégressive ; booléen (1 arg) ; run_infer 755-1101. Ses options propres :
  --prompt TEXTE — 635 — invite textuelle (gabarits Qwen `--chat` / harmony, 866-915) ; Option<String>.
  --ids-file F — 634 — identifiants depuis un fichier (séparateurs virgule/espace) ; Option<String> (916-923).
  --n N — 644 — jetons à générer ; usize, défaut 32 (582).
  --temp F — 645 — température ; f32, défaut 0.0.
  --top-p F — 646 — top-p ; f32, défaut 1.0.
  --topk N — 647 — mode DIAGNOSTIC pas-à-pas : imprime les N meilleurs logits à chaque position sans passer par `generate` (998-1028) ; usize, défaut 0.
  --rep-penalty F — 648 — pénalité de répétition ; f32, défaut 0.
  --hist N — 649 — taille d'historique pour la pénalité ; usize, défaut 64.
  --flux — 683 — sortie en flux (callback d'affichage au fil de l'eau) ; booléen (1044).
  --flux-liste — 684 / --flux-blocs — 685 — choix de l'encodage du flux (voir modes numérotés) ; booléens ; aussi lus par --ppl-reparti (2616-2618).
  --session — 686 — boucle interactive « vous> » (950-996, fin sur ligne vide ou /quit, max 50 tours) ; pose AUSSI `flux=true`.
  --chat — 687 — applique le gabarit de conversation ; booléen (858-899 : stop_id "<|im_end|>", gabarit Qwen2.5, ou HARMONY gpt-oss avec stop `<|return|>` + `<|end|>`).
  --tete-restreinte F — 701-702 — la tête de sortie ne calcule que les tokens de F (fichier d'ids, triés/dédoublonnés, 1138-1155) ; garde `if i+1 < args.len()` ; Option<String> — inférence 780-782 ; REFUSÉ en perplexité : « [tete] --tete-restreinte ignore en perplexite ({f}) : une perplexite calculee sur un vocabulaire restreint n'est comparable a rien. Utilisez --infer. » (4282-4285).
  --tete-garantie F — 699-700 — restriction de tête PROUVÉE exacte (Cauchy-Schwarz + paliers), `mdl.preparer_normes_tete()` (783-802) ; Option<String>.
--ppl FICHIER-IDS — 605 — perplexité ; pose `ppl=true` ET `ids_file=Some(valeur)` (2 args). Options lues par run_ppl (4277-4677) : --ctx/--threads/--abits, --limit, --depuis, --dense/--auto/--push/--q4/--bits-attn/--bits-ffn/--keep, --moe-topk, --act-*, --topk-*, --attn-*, --sans-fenetre/--swa-pattern/--sans-yarn, --patch, --ffn-gain, --logits-bin, --hebbian/--hebb-q/--hebb-out, --profil-neurones/--neurones-sortie, --trace-flux/--trace-couches/--flux-forcer, --harmony*, --lot, --options-actives. NON lus ici (destructuration `..`) : --tete-restreinte (ignoré, message 4282-4285), --tete-garantie, --n/--temp/--top-p/--topk/--rep-penalty/--hist, --prompt, --ids, --texte.
--ppl-texte F — 606-607 — perplexité sur TEXTE BRUT (tokenisé par le tokenizer du modèle, 4355-4362) ; pose `ppl=true`, `ppl_texte=true`, `texte_file=Some(F)` (2 args).
--plan — 608 — plan de placement (run_plan 3983-4138) ; booléen ; lit --ctx (4058-4064) ; n'utilise AUCUN réglage de quantification.
--tokenize — 609 — tokenisation (run_tokenize 3932-3975) ; booléen. Options : --texte TEXTE (636, défaut vide), --fichier F (637, encode un corpus entier et écrit `F.ids` ou --sortie), --sortie F (638, fichier de sortie ; défaut « {fichier}.ids »), et imprime un contrôle de réversibilité (3952-3965).
--tensors — 614 — inventaire (nom, dims, type) par les en-têtes seuls (run_tensors 1825-1866) ; booléen ; tout le reste est ignoré (main.rs:113).
--materiel — 695 — détection matérielle + plan de configuration SANS charger le modèle (run_materiel 1737-1823) ; booléen ; lit UNIQUEMENT --ctx (1740, affiché « Plan pour un contexte de {ctx} jetons ») ; si un modèle est donné en args[1], le plan s'appuie sur ses dimensions, sinon défaut « DeepSeek-V4.1 (défaut) » (1792). Termine par « Ces valeurs sont des DÉFAUTS : tout drapeau explicite les emporte. » (1822).
--config — 696 — ce que le moteur comprend d'un modèle sans le charger (run_config 1670-1735) ; booléen ; n'utilise AUCUN autre drapeau (main.rs:107).
--sonder-engram N — 697 — sonde mmap de la table d'engram (run_sonder_engram 1581-1654) ; usize lu avec `.parse().unwrap_or(1000)` => défaut 1000 ; 2 args ; préfixe `--sonder-engram` seul ou `=N` donne 1000 (le token de valeur est alors vu comme positionnel, ignoré).
--bloc TENSEUR:INDEX — 698 — déquantifie UN bloc (256 poids) et l'imprime (run_bloc 1536-1569) ; Option<String>, index défaut 0 si pas de ':' (1537-1540) ; garde `if i+1 < args.len()`.
--banc-vision F — 631 — banc vision : embedding de patchs écrit en binaire (+ `F.poids`, `F.bloc`) pour comparaison numpy (run_banc_vision 1195-1535) ; Option<String> ; utilise DRAVE_VISION_TEXTE (1508).
--flux-serveur ADRESSE — 617 — nœud MOTEUR (run_serveur_flux 2468-2588) ; Option<String> ; « `port` reste localhost ; `hôte:port` écoute sur l'interface nommée ("0.0.0.0:5599" pour un pair distant) » (2469-2475) ; ctx défaut 4096 (2480) ; fils via `fils()` ; réglages de quantification appliqués (2482) ; répond dans le mode reçu.
--ppl-reparti HÔTE:PORT — 620 — PILOTE réparti (run_ppl_reparti 2603-2857) ; Option<String> ; options : --ctx (défaut 256), --limit (≤ctx), --couches-locales N (621 ; défaut 12, 2608), --lot N (prép. par lots, 2612), --ids, --threads, --keep, --flux-liste/--flux-blocs (=> modes 1/2), et tous les --act-*/--topk-*/--moe-topk via appliquer_quantification (2614).
--couches-locales N — 621 — nombre de couches gardées en local par le pilote ; usize, défaut 12.
--couches A:B — 622-628 — exécution bornée des couches A..B ; Option<(usize,usize)> ; panique « --couches attend `a:b` (reçu « {v} ») » si pas de ':' ; passé à load_partiel (778-779, 4333-4334).
--gpu-banc — 610 — banc des noyaux GPU (run_gpu_banc 3658-3759) ; booléen ; aiguille selon --matrix vers banc_mxfp4 (3767), banc_q6k (3829), banc_q4k (3880), sinon tête Q8_0 ; lit --threads (3661) et --limit (3723-3725) ; tête par défaut "output.weight" sinon "token_embd.weight" (3677-3679).
--banc-kv N — 611 — banc du KV déporté, N clés (run_banc_kv 3479-3656) ; usize ; lit --threads (3551) et DRAVE_KV_BITS (3492, défaut 32) ; variables de cas dégénérés (voir section c).
--banc-topk N — 612 — banc des scores d'attention, N clés (run_banc_topk 2865-3434) ; usize ; lit --attn-topk (k, défaut 256 ; 2965), --threads (2946), DRAVE_KV_BITS (2872, défaut 8), DRAVE_BANC_SANS_PUITS (3151).
--banc-mla F — 613 — banc MLA : écrit (n_pos × vocab) logits f32 pour comparaison numpy (run_banc_mla 3438-3471) ; Option<String> ; ctx figé 4096 ; garde --ids (défaut 1..=8), --threads, --dense, --keep ; refuse/ignore trace et rejeu en le disant (3444-3447).
MODES NUMÉROTÉS (protocole de flux, main.rs:1907-1930) : mode 0 MODE_DENSE « Vecteur dense en f32 : 4 octets par canal, toute la dimension » ; mode 1 MODE_LISTE « LISTE creuse quantifiée : indice u16 + valeur i16, plus une échelle » (donné par --flux-liste) ; mode 2 MODE_BLOCS « LISTE à échelle par bloc de 32 canaux : indice u16, valeur i8, une échelle f32 par bloc » (donné par --flux-blocs) ; mode 3 MODE_LOT « n états de hidden canaux chacun, en f32 dense, dans UN SEUL flux » ; mode 4 MODE_LOT_LISTES « n états, chacun encodé comme le mode 2 …, enchaînés dans un seul flux » (--flux-blocs + lot). Sélection : 2616-2622 (`mode` puis `mode_lot = if mode==MODE_BLOCS {MODE_LOT_LISTES} else {MODE_LOT}`).

============ (c) VARIABLES D'ENVIRONNEMENT ============
Préfixe DRAVE_. main.rs:11-27 `const VARS_LUES: &[&str]` = les 39 noms SANS préfixe que le moteur lit ; main.rs:80-86 : tout QT_<suffixe> présent dans l'environnement et listé ici déclenche « [attention] {vieux} est l'ancien nom d'une variable d'environnement : il faut écrire DRAVE_{suffixe} (voir docs/histoire.md). Rien n'a été appliqué. » ; ne signale QUE la traduction exacte (les QT_* de Qt sont ignorés, test 5024-5031) ; test d'exhaustivité 4996-5019 (tout DRAVE_* cité dans src/*.rs doit être dans VARS_LUES et réciproquement).
Liste VARS_LUES (main.rs:18-26), avec le lieu de LECTURE vérifié par grep sur drave-core/src (les 3 fichiers cibles, puis hors de ces 3 fichiers — information de localisation, pas d'invention de rôle) :
--- lues DANS les 3 fichiers ---
DRAVE_GPU_TOPK — cité main.rs:428-430, 450 ; lu main.rs:430 (et model.rs:3123, 5512) — active le top-k déporté GPU ; motif d'inactivité affiché : k==0, k>1024, KV≠8/32 bits, fenêtre>0, lot>1, DRAVE_GPU absent, DRAVE_GPU_KV absent (433-449). Valeur testée `v != "0" && !v.is_empty()`.
DRAVE_GPU — cité main.rs:443-444 ; lu gpu.rs:1540, 1565 (commentaire gpu.rs:1530 « `DRAVE_GPU` active le déport ; sans lui, aucune » instance) — sans lui « rien ne va au GPU ».
DRAVE_GPU_KV — cité main.rs:445-446 ; lu model.rs:3088 (miroir VRAM du cache KV, model.rs:1907) — sans lui « pas de miroir VRAM à interroger ».
DRAVE_VISION_TEXTE — cité main.rs:1499, 1508 (mode --banc-vision) — « `<modele.gguf>` charge le modèle de texte et lui impose le PREMIER jeton d'image via `Model::emb_imposee` … contrôle de PLOMBERIE : le moteur ne panique pas, il rend des logits d'échelle normale » (1498-1503).
DRAVE_DEBUG_FLUX — lu main.rs:2555 (nœud --flux-serveur) — trace « [debug] lot reçu : n=… pos=… états=… plat=… corps=… ».
DRAVE_KV_BITS — lu main.rs:2872 (--banc-topk, défaut 8) et main.rs:3492 (--banc-kv, défaut 32) ; lu aussi model.rs:2940.
DRAVE_BANC_SANS_PUITS — cité main.rs:3150, 3236 ; lu main.rs:3151 — `=1` retire les puits d'attention : « Le moteur passe `None` pour les modèles SANS puits (Qwen, la plupart) : ce chemin n'était exercé par aucun banc ».
DRAVE_BANC_KV_K0 — lu main.rs:3509 — cas dégénéré « clés nulles (poids uniformes) ».
DRAVE_BANC_KV_V1 — lu main.rs:3510 — « valeurs constantes (la sortie vaut 1 quelle que soit la softmax) ».
DRAVE_BANC_KV_UNIT — lu main.rs:3514 et 3639 — « valeurs "une chaude" par position — la sortie devient alors le poids de chaque clé ».
DRAVE_BANC_KV_GRAD — lu main.rs:3519 — « cas "pente" … la softmax se concentre sur la DERNIÈRE clé ».
DRAVE_BANC_KV_KUNIT — lu main.rs:3522 — « clés "une chaude" : la clé k ne parle qu'à la composante k ».
DRAVE_BANC_KV_GPU_SEUL — cité main.rs:3548, 3590 ; lu main.rs:3550 — saute la référence CPU (« à 1 M de clés elle coûte 3 à 16 minutes »).
DRAVE_BANC_KV_DEBUG — lu main.rs:3646.
DRAVE_HARMONY_TRACE — lu main.rs:4222 et 4267 — affiche chaque fenêtre harmony construite (« [harmony] fenêtre N : X jetons, Y notés · |aperçu| »).
--- citées dans les 3 fichiers, lues HORS de ces 3 fichiers ---
DRAVE_CLUSTERS — usage main.rs:63 « DRAVE_CLUSTERS=0,3 ne charge que certains clusters » ; lu clusters.rs:168 (doc 166) ; erreurs clusters.rs:172, 245, 253, 272.
DRAVE_MMAP — usage main.rs:64 « DRAVE_MMAP=0 lit au lieu de mapper » ; lu gguf.rs:156 (doc 153 « force la lecture complète »).
DRAVE_PRELIRE — lu gguf.rs:95 (gguf.rs:67 « `DRAVE_PRELIRE=0` la désactive »).
DRAVE_PRELIRE_TOUT — lu gguf.rs:91 (doc 89 « demander le fichier entier au chargement », accepte 1/oui/true).
DRAVE_Q8_BLOCS — lu model.rs:960 (doc 954 « une échelle par bloc de 32 »).
DRAVE_SANS_EMPRUNT — lu model.rs:1021, 1028 (doc 1019 « force la reconstruction » ; l'emprunt exige keep>=1.0).
DRAVE_TRACE_BLOCS — lu model.rs:1507 (doc 1484, 1504 : version 3 de trace, valeurs i8 + échelle f16 par bloc de 32 ; model.rs:4469 « utilisez --lot 1, ou réenregistrez sans DRAVE_TRACE_BLOCS »).
DRAVE_TRACE_EXPERTS — lu model.rs:3204 (doc 1830 « Trace de routage : une ligne par … »).
DRAVE_ETAT_ENTREE — lu model.rs:3222 (doc 1950 « Fichier d'état d'ENTRÉE : le résidu du premier … »).
DRAVE_DUMP_COUCHES — lu model.rs:3223 (doc 1958 « Préfixe de vidage des états de couche »).
DRAVE_FLUX_VERIF — lu model.rs:5302.
DRAVE_DEBUG_ETAT — lu model.rs:5181 (doc 5177 « la norme de l'état résiduel à chaque … »).
DRAVE_DEBUG_MLA — lu model.rs:4512, 5182 (doc 4508 « les premières valeurs des projections MLA »).
DRAVE_GPU_EXPERTS — lu model.rs:3151 (doc 1997 « Cache VRAM des experts MoE »).
DRAVE_GPU_EXPERTS_GO — lu model.rs:3162 (taille en Go du cache d'experts).
DRAVE_GPU_TETE — lu model.rs:3066 (doc 3060 « Opt-in », 3062).
DRAVE_KV_F16 — lu model.rs:2157, 2277 (doc 2111 « arrondir clés et valeurs en f16 avant quantification »).
DRAVE_KV_K_F16 — lu model.rs:2155 (doc 2126 « les CLÉS sont stockées en f16, sans quantification »).
DRAVE_KV_K_F32 — lu model.rs:2154 (doc 2113 « garde les CLÉS en f32 (l'erreur qui passe par les scores disparaît) »).
DRAVE_KV_V_F32 — lu model.rs:2154 (doc 2114 « garde [les VALEURS en f32] »).
DRAVE_YARN — lu model.rs:2566, 2570 (doc 2529 « YaRN à toutes les positions, comme HF, llama.cpp »).
DRAVE_YARN_MSCALE — lu model.rs:2565 (doc 2563 « tranche explicitement »).
DRAVE_YARN_NON — lu model.rs:2571 (doc 2531 « jamais de YaRN (ce que fait `--sans-yarn`) »).
DRAVE_YARN_RAMPE — lu model.rs:3799 (doc 3798 « =0 force l'interpolation pure »).
Total VARS_LUES = 39 noms (4+4+6+3+5+6+5+5+1). AUCUNE mention de RAYON_NUM_THREADS, OMP_NUM_THREADS, MKL_NUM_THREADS, OPENBLAS_NUM_THREADS (grep négatif sur les 3 fichiers ET sur tout drave-core/src) : le parallélisme est piloté uniquement par --threads et engine::coeurs_physiques().

============ (d) ENUMS ============
main.rs:2016 `enum ChargeFlux` (privé) — Dense(Vec<f32>) ; Liste { idx: Vec<u16>, val: Vec<i16>, echelle: f32 } ; Blocs { idx: Vec<u16>, val: Vec<i8>, echelles: Vec<f32> } ; Lot(Vec<f32>) — charge utile d'un flux ; `en_dense(hidden)` déquantifie (2027-2048), `plat()` sert les lots.
list.rs:342 `pub enum Source8` (derive Clone, Copy, PartialEq, Eq) — Propre (« une échelle par ligne (historique) ») ; PropreBloc (« une échelle par bloc de 32, comme Q8_0 … l'hypothèse à tester ») ; Q8_0. Champ `DenseQ8.src` (list.rs:361).
list.rs:619 `pub enum Source` (derive Clone, Copy, PartialEq, Eq) — Propre, Q4_0, Mxfp4, Q4_K, Q6_K, Dequant(u32) (« Super-bloc de 256 poids sans noyau dédié : Q2_K, Q3_K, Q5_K, IQ1_S, IQ1_M, IQ2_XXS, IQ3_XXS, IQ4_XS » ; « Ces formats portent 30 % des poids de Kimi-K2.7, GLM-5.3 et DeepSeek-V4 »). Champ `DenseQ4.src` (list.rs:666).
Aucun autre `enum` dans les 3 fichiers (grep). Les « modes » 0-4 sont des constantes, pas un enum.

============ (e) CONSTANTES NOMMÉES ============
main.rs:17 `const VARS_LUES: &[&str]` — 39 suffixes de variables d'environnement lues (sans préfixe DRAVE_) ; sert au message QT_* et au test d'exhaustivité.
main.rs:390 `static MODELE: std::sync::OnceLock<String>` — chemin du modèle posé une fois par main (88) ; lu par `modele_chemin()` (391) — « les modes n'ont plus à fouiller `argv` ni à supposer que le modèle est en position 1 ».
main.rs:1893 `const MAGIE_FLUX: u32 = 0x4452_5631` — « "DRV1" », magie d'en-tête de flux.
main.rs:1906 `const VERSION_FLUX: u8 = 5` — version du protocole ; « Version 4 : le bloc de réglages transporte AUSSI les top-k … Version 3 : ajoute le mode LOT » ; test : `assert_eq!(VERSION_FLUX, 5, "le mode 4 impose la version 5")` (4694).
main.rs:1908 `const MODE_DENSE: u8 = 0` — « Vecteur dense en f32 : 4 octets par canal, toute la dimension ».
main.rs:1912 `const MODE_LISTE: u8 = 1` — « LISTE creuse quantifiée : indice u16 + valeur i16, plus une échelle ».
main.rs:1917 `const MODE_BLOCS: u8 = 2` — « LISTE à échelle par bloc de 32 canaux : indice u16, valeur i8, et une échelle f32 par bloc ».
main.rs:1923 `const MODE_LOT: u8 = 3` — « LOT : n états de hidden canaux chacun, en f32 dense, dans UN SEUL flux ».
main.rs:1930 `const MODE_LOT_LISTES: u8 = 4` — « LOT EN LISTES … Le lot dense coûte 3 589 octets par jeton ; celui-ci ≈ 1 530 (÷2,3) ».
main.rs:1941 `const TAILLE_TETE: usize = 79` — octets de l'en-tête de flux ; composition commentée 1939-1940 : magie · version · mode · plage · position · n · échelle · niveaux · seuil · top-k · renorm · attn_topk · qk_topk · moe_topk · topk_proj[7] ; vérifié par test 4690.
main.rs:2002 `const PLAFOND_FLUX: usize = 256 << 20` — plafond d'allocation pilotée par le réseau (256 Mo), « règle R4 de docs/plan-prefill-reparti.md » ; appliqué par verifier_taille (2005-2011).
list.rs:338 `pub static BITS_POIDS: std::sync::atomic::AtomicU32 = AtomicU32::new(0)` — « Précision simulée : nombre de bits conservés sur les poids d'une matrice int8 (0 = tous les huit) » ; écrit par --bits (main.rs:740), lu list.rs:456.
list.rs:539 `pub const BLOC_Q4: usize = 32` — « Taille des blocs d'échelle. 32 est le compromis standard (Q4_0) ».
list.rs:542 `pub const LUT_INT4: [i8; 16]` — « Grille int4 symétrique : le nibble n vaut n − 8 », valeurs -8..7.
list.rs:547 `pub const LUT_MXFP4: [i8; 16]` — « Table E2M1 du format MXFP4, magnitudes doublées » [0,1,2,3,4,6,8,12,0,-1,-2,-3,-4,-6,-8,-12].
engine.rs:265 `pub static EPINGLER: std::sync::atomic::AtomicBool = AtomicBool::new(false)` — « Épingle-t-on les workers ? Réglé une fois par le programme principal » ; posé par --pin (main.rs:739) ; consommé engine.rs:422-430.
engine.rs:51 `const HIGH_BITS: u64 = 0x8080_8080_8080_8080` (privé, masque SWAR du décodeur — pas un réglage).

============ (f) STRUCT(S) DE CONFIGURATION ============
`struct Options` — main.rs:473-576 — « Toutes les options de la ligne de commande, dans une seule structure » (doc 465-472 : « les modes … la remplissent par la MÊME boucle »). `#[derive(Default)]`. Champs (nom: type — rôle) :
infer: bool / ppl: bool / plan: bool / tokenize: bool / gpu_banc: bool — sélection du mode ; banc_kv: usize (« Banc du KV déporté : nombre de clés à faire tenir en VRAM ») ; banc_topk: usize (« Banc des SCORES d'attention : nombre de clés à noter (noyau 1 du top-k) ») ; banc_mla: Option<String> (« écrit les logits (n_pos × vocab) en f32 pour les comparer à la référence numpy ») ; trace_flux: Option<String> (« Trace du flux d'activation : fichier de sortie ») ; flux_forcer: Option<String> (« Relecture d'une trace … (rejeu) ») ; options_actives: bool (« imprime, APRÈS toutes les affectations, les réglages que le moteur utilise réellement ») ; inconnus: Vec<String> (« Drapeaux `--xxx` que l'analyse n'a PAS reconnus ») ; options_strict: bool (« un drapeau inconnu n'est plus un avertissement mais une ERREUR ») ; flux_serveur: Option<String> (« Adresse d'écoute du nœud moteur : `port`, ou `hôte:port` ») ; ppl_reparti: Option<String> (« pilote qui répartit le calcul sur un nœud distant (hôte:port) ») ; couches_locales: usize (« Nombre de couches gardées en local par le pilote ») ; couches: Option<(usize, usize)> (« Exécution bornée `a:b` ») ; trace_couches: Vec<usize> (« Couches à tracer (vide = toutes) ») ; banc_vision: Option<String> (« embedding de patchs, écrit en binaire ») ; tensors: bool (« liste les tenseurs du fichier (nom, dimensions, type) et s'arrête ») ; ids: Vec<u32> ; ids_file: Option<String> ; texte_file: Option<String> ; ppl_texte: bool ; prompt: Option<String> ; limit: usize ; depuis: usize ; n: usize ; temp: f32 ; top_p: f32 ; topk: usize ; rep_pen: f32 ; hist: usize ; flux: bool ; session: bool ; chat: bool ; flux_liste: bool ; flux_blocs: bool ; ctx: usize ; threads: usize ; abits: u32 ; dense: bool ; auto: bool ; ctx_impose: bool ; threads_impose: bool ; abits_impose: bool — « Vrai si `--ctx`, `--threads` ou `--abits` ont été donnés : leurs défauts diffèrent selon le mode (256 jetons et 16 bits en perplexité, 512 et 8 bits en inférence, la moitié des cœurs contre les trois quarts) » [commentaire d'origine — voir l'écart signalé en (a)] ; q4: u8 ; b6: u8 ; keep: f32 ; bits: u32 ; moe_topk: usize ; pin: bool ; attn_window: usize ; swa_pattern: Option<usize> ; sans_fenetre: bool ; attn_sinks: usize ; attn_topk: usize ; qk_topk: usize ; act_thresh: f32 ; act_topk: usize ; act_renorm: bool ; topk_proj: [usize; 7] ; logits_bin: Option<String> ; ppl_profil: bool ; config: bool ; profil_neurones: bool (« Profilage des neurones "chauds" (idée de PowerInfer) ») ; neurones_sortie: Option<String> ; materiel: bool ; sonder_engram: usize (« Sonde d'accès mmappé à la table d'engram … Démontre qu'une table de 101 Go s'adresse sans se charger ») ; bloc: Option<String> (« `TENSEUR:INDEX` : déquantifie UN bloc et l'imprime ») ; tete_restreinte: Option<String> (« Fichier d'identifiants de tokens … **Génération seulement** ») ; tete_garantie: Option<String> (« restriction de tête **prouvée exacte** (Cauchy-Schwarz + extension par paliers) ») ; lot: usize (« Taille du lot de préremplissage : 1 = jeton par jeton (défaut) ») ; harmony: Option<String> ; harmony_contexte: Option<String> ; sans_yarn: bool ; patch: Option<String> ; hebb_layer: Option<usize> ; hebb_q: f32 ; hebb_out: String ; ffn_gain: Option<(usize, f32)> ; matrix: String ; texte: Option<String> ; fichier: Option<String> ; sortie: Option<String>.
ANOMALIE VÉRIFIÉE : `ppl_profil` (main.rs:541) n'a AUCUNE branche dans `analyser` — aucun drapeau `--ppl-profil` n'existe (grep : seules occurrences 541, 4295, 4493). Il reste donc toujours `false` (Default) et tout `--ppl-profil` en ligne de commande est classé INCONNU (714-724) ; il ne pilote que `let profil = ppl_profil;` (4493) et l'impression du profil par profondeur (4578-4585).
`struct Act` — main.rs:1945-1958 — « Réglages d'activation d'un nœud : ils font partie du contrat d'échange » (transmis dans CHAQUE en-tête de flux, 79 octets) : levels: f32 ; thresh: f32 ; topk: u32 ; renorm: bool ; topk_proj: [u32; 7] (« top-k par projection (q, k, v, o, gate, up, down) : "topk est une FRACTION de la dimension" ») ; attn_topk: u32 ; qk_topk: u32 ; moe_topk: u32. Conversion depuis le modèle `Act::du_modele` (1961-1968), application `appliquer` (1969-1978). Défaut d'en-tête sans modèle (2089-2090) : levels 127.0, thresh 0.0, topk 0, renorm false, topk_proj [0;7], attn/qk/moe 0.
`struct Flux` — main.rs:1983-1995 — n (canaux/actifs/ÉTATS), debut, fin, pos, mode: u8, act: Act, charge: ChargeFlux, octets_corps: usize (comptabilité réelle du banc).
Champs de config du MODÈLE visibles dans ces 3 fichiers :
- via la construction `model::Cfg { … }` de run_config (main.rs:1722-1728) : n_layer, hidden, n_head, n_kv_head, head_dim, ffn, eps, rope_base, vocab, n_expert, n_expert_used, ffn_exp, ffn_act_oss, gating, expert_norm, expert_scale, hash_layers, n_rot, yarn (struct `Cfg` définie model.rs:416, hors des 3 fichiers).
- via `options_actives` (main.rs:405-424) : mdl.ctx, act_levels, act_thresh, act_topk, act_renorm, attn_topk, qk_topk, moe_topk, act_topk_proj, couche_debut, couche_fin, flux_brut, trace, flux_force, attn_window, swa_pattern, seuil_push, lot, ffn_gain, hebb, kv (bits, k_f32, k_f16, v_f32, f16_avant).
- métadonnées GGUF lues comme config par --tensors (main.rs:1849-1851) : block_count, embedding_length, feed_forward_length, attention.head_count, attention.head_count_kv, expert_count, expert_used_count, context_length, vocab_size ; et par --plan : context_length, attention.head_count_kv, attention.key_length, attention.sliding_window, rope.freq_base, rope.scaling.original_context_length, rope.scaling.factor (4063-4126).
Sortie de `--config` (main.rs:1673-1734), utile comme « aide config » : « modèle », « architecture », « couches », « experts », « routage (source) · renormalisation · échelle », « routage table : N/M premières couches par `ffn_gate_tid2eid` », « attn compress. : N couches · CSA (ratio 4) · HCA (ratio 128) · brutes aux couches […] », « hyper-conn. : copies · mélanges · Sinkhorn itérations · eps », « calculable : oui (passe avant implémentée) » ou « calculable : NON — il manque : … ».

FICHIERS : main.rs = 5033 lignes (toute la CLI), list.rs = 1572 lignes (0 drapeau, 0 env ; 1 static + 3 const + 2 enums), engine.rs = 1010 lignes (0 drapeau, 0 env ; 1 static + 1 const privé). Aucun fichier modifié.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== AVX2 ===\" && grep -rn 'AVX2\\|avx2' drave-core/src/*.rs | head -8; echo \"=== NUMA/PCIe/DDR/FPGA/DSP/ALM/M20K ===\"; grep -rn 'NUMA\\|PCIe\\|DDR3\\|FPGA\\|DSP\\|M20K\\|ALM' drave-core/src/*.rs docs/*.md tools/*.py 2>/dev/ … [63 caractères tronqués]`

  ```
=== AVX2 ===
drave-core/src/engine.rs:247:    /// mêmes activations en i16, pour le noyau AVX2 du mode 4
drave-core/src/gguf.rs:1603:            if std::is_x86_feature_detected!("avx2") {
drave-core/src/gguf.rs:1604:                return unsafe { self.q8_dot_avx2(v, row, qx) };
drave-core/src/gguf.rs:1627:    #[target_feature(enable = "avx2")]
drave-core/src/gguf.rs:1628:    unsafe fn q8_dot_avx2(&self, v: &Q8View, row: usize, qx: &[i16]) -> f32 {
drave-core/src/gguf.rs:2029:    /// même origine ne peut pas la voir (c'est arrivé : le chemin AVX2 et le
drave-core/src/list.rs:823:    #[target_feature(enable = "avx2")]
drave-core/src/list.rs:824:    unsafe fn dot16_q6_avx2(&self, o: usize, x: &[i16], sx32: &[i32]) -> f32 {
=== NUMA/PCIe/DDR/FPGA/DSP/ALM/M20K ===
drave-core/src/engine.rs:274:/// nœud NUMA 0. Un worker qui tourne sur l'autre socket paie chaque accès au
drave-core/src/engine.rs:332:/// Processeurs du premier nœud NUMA, cœurs physiques puis frères SMT.
drave-core/src/gpu.rs:7://! Principe de placement : **les poids restent sur le GPU**. Mesuré : PCIe x8
drave-core/src/gpu.rs:639:    /// pèse 14,7 Mo sur le bus PCIe, et 56 Mo à 1 M : la mesurer séparément est
drave-core/s
… [2257 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'ALM\\|M20K' docs/*.md tools/*.py reports/*.md 2>/dev/null | head -12", "description": "Locate ALM and M20K references"}`

  ```
docs/programme-recherche.md:58:| Carte FPGA | PE vérifié sur 309 020 événements réels, synthétisé (176 ALMs, 0 DSP), lecteur DDR3 vérifié de bout en bout |
tools/session_report.py:46:    r"\d+(?:[.,]\d+)?\s*(?:tok/s|G\s*év|G\s*evt|G\s*ev|MHz|ALMs|M20K|DSP\b|"
reports/bilan-multi-materiel.md:66:3. **Pas de multiplieur requis.** Le PE atteint 112,5 MHz avec 176 ALMs **et zéro
reports/bilan-multi-materiel.md:67:   DSP**, contre 115 ALMs et 1 DSP avec multiplieur — et **pas un hertz d'écart**.
reports/bilan-multi-materiel.md:95:| « 27 PE suffisent, 3 % de la logique » | **Corrigée** — en comptant le lecteur : 51 voies, 41 % de la logique et 41 % de la M20K |
reports/rapport-cpu-aer.md:11:  (accumulateur, 4096 × 24 bits = **12 Kio**, tient dans les M20K) ;
reports/rapport-encodage.md:77:   cette voie (croisement ou réplication de bancs M20K), pas le décodage.
reports/rapport-eparsite.md:64:4. **Le vrai obstacle n'est pas le poids, c'est l'activation** : un événement n'existe que si le poids *et* l'activation sont non nuls (ici 13.9 % d'événements réels). Récupérer l'activation à un index arbitraire impose une fenêtre de lecture et un multiplexeur par voie : ~21 LUT pour un 64:1, soit ≈ 
… [588 caractères tronqués]
  ```

### 👤 Utilisateur

Background subagent 2c2a6595-b208-446e-bbd1-d0f49eca45e8 finished and will do no further work unless you send it more.
Its closing message:
⏵ Rapport complet livré au parent

Le rapport complet a été envoyé au parent (`f2de810a-b765-444d-b3cc-d8fce1ba2105`). Le voici :

**FAIT MAJEUR** : aucun clap/structopt. Toute la ligne de commande est analysée à la main dans `analyser()` (main.rs:580-742), en UNE passe ; chaque branche rend le nombre d'arguments consommés (1 booléen, 2 à valeur). `args[1]` est TOUJOURS le chemin du modèle (`MODELE` OnceLock, main.rs:88/390) ; l'analyse démarre à i=2. Aide = uniquement les `eprintln` de main.rs:51-64 (+ doc module 3-9) ; **aucun** `--help`/`-h`/`--version`. 93 drapeaux reconnus. Un drapeau à valeur en dernière position **panique** (« {flag} attend une valeur », 591-593) sauf `--bloc`/`--tete-garantie`/`--tete-restreinte` (gardés par `i+1 < args.len()`, 698-702). Drapeaux inconnus retenus (714-724), avertis (728-732), `--options-strict` ⇒ exit(2) (733-737). Effets immédiats : `--pin`→EPINGLER (739) ; `--bits`→BITS_POIDS (740). Défauts : n=32, temp=0, top_p=1, hist=64, hebb_q=0.1, hebb_out="hebb.bin", keep=1.0, abits=8, auto=true, limit=usize::MAX, matrix="blk.0.ffn_gate.weight", ctx=512, threads=coeurs_physiques().max(1) (581-590). Défauts par mode : inférence 512/8 ; perplexité 256/16 ; flux-serveur 4096 ; ppl-reparti 256 + couches_locales 12 ; banc-mla 4096 ; banc-kv bits 32 ; banc-topk bits 8 ; sonder-engram 1000.

**Écart signalé** : `fils()` (454-463), le commentaire 770-776 et le doc d'`Options` (530-533) disent « la moitié des cœurs » / « trois quarts », mais le code rend `coeurs_physiques().max(1)` = **tous** les cœurs physiques.
**Anomalie vérifiée** : `ppl_profil` (main.rs:541) n'a **aucune** branche dans `analyser` ⇒ le drapeau `--ppl-profil` n'existe pas, le champ reste `false` et tout `--ppl-profil` est classé inconnu.

(a) Tous les drapeaux globaux avec ligne/effet/portée/défaut ; (b) tous les drapeaux par sous-commande (16 modes + modes numérotés 0=dense, 1=liste, 2=blocs, 3=lot, 4=lot-listes) ; (c) les 39 variables de `VARS_LUES` (main.rs:17-27) avec lieu de lecture réel (15 lues dans les 3 fichiers, 24 hors de ces 3 fichiers — localisation vérifiée par grep, rôles non inventés) ; aucune trace de RAYON_NUM_THREADS/OMP_NUM_THREADS/MKL/OPENBLAS ; (d) enums `ChargeFlux`, `Source8`, `Source` avec variantes ; (e) toutes les `const`/`static` (`VARS_LUES`, `MODELE`, `MAGIE_FLUX`, `VERSION_FLUX`, `MODE_DENSE/LISTE/BLOCS/LOT/LOT_LISTES`, `TAILLE_TETE`=79, `PLAFOND_FLUX`, `BITS_POIDS`, `BLOC_Q4`, `LUT_INT4`, `LUT_MXFP4`, `EPINGLER`) ; (f) `Options` champ par champ (type + rôle), `Act`, `Flux`, plus les champs de config modèle visibles via `run_config` (1722-1728) et `options_actives` (405-424).

Aucun fichier modifié (lecture seule stricte respectée).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for t in AER Hadamard RMSNorm SiLU SwiGLU LoRA MTP spéculatif TLB \"RSS\" PTX zstd; do echo \"=== $t ===\"; grep -rn \"$t\" drave-core/src/*.rs tools/*.py tools/*.sh docs/*.md sprints/*.md 2>/dev/null | head -4; done", "description": … [33 caractères tronqués]`

  ```
=== AER ===
docs/histoire.md:12:| **le virage événementiel** | l'idée qui a tout changé : ne plus multiplier des matrices, mais **pousser des listes d'activation** vers leurs destinations (AER, *Address Event Representation*). Le prototype C mesure **7,79 G événements/s**, le croisement push/pull est mesuré à **~22 % de densité** | `reports/rapport-cpu-aer.md`, `reports/rapport-croisement-push-pull.md`, `reports/rapport-encodage.md` |
docs/vision.md:34:  l'**AER** des architectures neuromorphiques (*Address Event Representation*),
docs/vision.md:225:  ce qui parle**. C'est la même idée que l'AER neuromorphique, et c'est ce qui
=== Hadamard ===
=== RMSNorm ===
drave-core/src/model.rs:886:    /// RMSNorm appliquée à chaque tête de Q et de K après projection
docs/comparaison-spiking.md:115:RMSNorm flottant hors du domaine événementiel ; si nous passons aux spikes, BN
docs/plan-deepseek41-complet.md:173:- État résiduel en 4 copies ; par couche `hc_pre` (RMSNorm → `hc_fn` → 24
docs/plan-mla-vision.md:31:| `blk.N.attn_q_a_norm.weight` | `[q_lora_rank]` | RMSNorm après la descente |
=== SiLU ===
drave-core/src/model.rs:431:    /// Activation du FFN. gpt-oss n'utilise **pas** SiLU : c'est

… [2284 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== lora ===\"; grep -rn 'lora' drave-core/src/*.rs tools/*.py 2>/dev/null | head -6; echo \"=== porte de correction ===\"; grep -rn 'porte de correction\\|portes de correction' --include='*.md' --include='*.sh' --include='*.r … [254 caractères tronqués]`

  ```
=== lora ===
drave-core/src/model.rs:1150:    pub q_a: Vec<f32>,      // [q_lora × h]
drave-core/src/model.rs:1151:    pub q_a_norm: Vec<f32>, // [q_lora]
drave-core/src/model.rs:1152:    pub q_b: Vec<f32>,      // [nh·head_dim × q_lora]
drave-core/src/model.rs:1155:    pub wo_a: Vec<f32>,     // [o_lora·n_groups × (nh/n_groups)·head_dim], par groupe
drave-core/src/model.rs:1156:    pub wo_b: Vec<f32>,     // [h × o_lora·n_groups]
drave-core/src/model.rs:1163:    pub o_lora: usize,
=== porte de correction ===
./reports/rapport-coherence-vision.md:20:| 1. cadrage | la vision retenue est celle de `docs/vision.md` **et** la précision du 02/10 : Drave ≠ llama.cpp ; listes d'activation (deux listes trinaires **ou** connexions pondérées) routées sur des **grappes de neurones** réparties entre composants et machines ; les flux sont aussi l'**instrument de débogage et d'analyse** qui adapte l'architecture à la tâche. llama.cpp n'est qu'une **porte de correction**. |
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:42:- **create** — Exécuter le plan docs/plan-deepseek41-complet.md phase par phase (P0→P9), en autonomie, en respectant pour chaque phase ses deux portes : port
… [2329 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs", "limit": 80, "offset": 253}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs</path>
<type>file</type>
<content>
253: 
254: impl TensorInfo {
255:     pub fn nelem(&self) -> usize { self.dims.iter().product::<u64>() as usize }
256: }
257: 
258: pub const GGML_F32: u32 = 0;
259: pub const GGML_F16: u32 = 1;
260: pub const GGML_Q4_0: u32 = 2;
261: pub const GGML_MXFP4: u32 = 39;
262: pub const GGML_Q2_K: u32 = 10;
263: pub const GGML_BF16: u32 = 30;
264: pub const GGML_Q3_K: u32 = 11;
265: pub const GGML_Q4_K: u32 = 12;
266: /// Bloc **Q5_0** (22 octets, 32 poids) et **Q5_1** (24 octets, 32 poids) :
267: /// échelle f16 (+ minimum f16 pour Q5_1), 4 octets de bits hauts, 16 octets de
268: /// quants 4 bits. Q5_0 est le type de `token_embd` et des `ffn_gate/up` de
269: /// Qwen2.5-0.5B en Q4_K_M — 62 % des poids de ce fichier : sans lui, le modèle
270: /// ne se charge pas du tout.
271: pub const GGML_Q5_0: u32 = 6;
272: pub const GGML_Q5_1: u32 = 7;
273: pub const GGML_Q5_K: u32 = 13;
274: pub const GGML_Q6_K: u32 = 14;
275: /// Types des experts de DeepSeek : IQ2_XXS (V4.1), IQ1_M (V4-Flash).
276: /// Sans ces constantes, `--bloc` les appelait « type 16 » et le lecteur les
277: /// re
… [2660 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== pub struct/enum (hors model.rs) ===\" && grep -n 'pub struct\\|pub enum\\|pub fn' drave-core/src/materiel.rs | head -30; echo; echo \"=== Gating ===\"; sed -n '24,44p' drave-core/src/model.rs; echo; echo \"=== pub static f … [133 caractères tronqués]`

  ```
=== pub struct/enum (hors model.rs) ===
24:pub struct Noeud {
31:pub struct Cpu {
45:pub struct Gpu {
56:pub struct Disque {
65:pub struct Materiel {
75:pub struct Plan {
212:pub fn ram_libre_go() -> f64 {
276:    pub fn detecter() -> Materiel {
288:    pub fn plan(&self, ctx: usize, taille_modele_go: f64, n_experts: usize,
381:    pub fn cout_par_jeton(&self, plan: &Plan, go_experts_par_jeton: f64,
408:    pub fn resume(&self) -> String {

=== Gating ===

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
    Sof
… [449 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs", "limit": 70, "offset": 128}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs</path>
<type>file</type>
<content>
128: }
129: 
130: /// Les octets d'un fichier, lus ou mappés.
131: ///
132: /// Le reste du lecteur ne fait pas la différence : les deux variantes se
133: /// déréférencent en `&[u8]`. Le choix se fait une fois, à l'ouverture.
134: pub enum Tampon {
135:     Lu(Vec<u8>),
136:     Mappe(Mappe),
137: }
138: 
139: impl Deref for Tampon {
140:     type Target = [u8];
141:     #[inline]
142:     fn deref(&self) -> &[u8] {
143:         match self { Tampon::Lu(v) => v, Tampon::Mappe(m) => m }
144:     }
145: }
146: 
147: impl Tampon {
148:     pub fn len(&self) -> usize { (**self).len() }
149:     pub fn is_empty(&self) -> bool { self.len() == 0 }
150: }
151: 
152: /// Faut-il mapper les fichiers ? Mappé par défaut : c'est moins de mémoire et
153: /// moins d'octets lus. `DRAVE_MMAP=0` force la lecture complète (utile pour
154: /// comparer, ou sur un système de fichiers qui refuse le mmap).
155: fn mmap_voulu() -> bool {
156:     match std::env::var("DRAVE_MMAP") {
157:         Ok(v) => !(v == "0" || v.eq_ignore_ascii_case("non") || v.eq_ignore_ascii_case("false")),
158:       
… [1696 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'engram_embd\\|384 006 168\\|384,006,168\\|101,4\\|101.4' reports/rapport-empreinte-memoire.md docs/*.md | head -20", "description": "Cross-check engram figures"}`

  ```
reports/rapport-empreinte-memoire.md:250:**`blk.N.engram_embd.weight`, à 101,4 Go par couche** (deux couches : 1 et 14),
reports/rapport-empreinte-memoire.md:251:en I8, de forme `[384 006 168, 264]`.
reports/rapport-empreinte-memoire.md:257:| entrées | 384 006 168 par couche |
docs/plan-deepseek41-complet.md:319:- Deux tables de 101,4 Go (couches 1 et 14) : hachage de n-grammes
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nm=json.load(open('tools/manifeste_modeles_lourds.json'))\nprint(type(m), list(m)[:10] if isinstance(m,dict) else len(m))\nprint(json.dumps(m, ensure_ascii=False)[:1500])\n\"", "description": "Read heavy mo … [14 caractères tronqués]`

  ```
<class 'list'> 24
[{"nom": "DeepSeek-V4-Flash-UD-IQ1_M", "repo": "unsloth/DeepSeek-V4-Flash-GGUF", "chemin": "UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00002-of-00003.gguf", "octets": 49971881124}, {"nom": "DeepSeek-V4-Flash-UD-IQ1_M", "repo": "unsloth/DeepSeek-V4-Flash-GGUF", "chemin": "UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf", "octets": 5256864}, {"nom": "DeepSeek-V4.1-Flash-Q2", "repo": "antirez/deepseek-v4.1-flash-gguf", "chemin": "DeepSeek-V4.1-Flash-Q2.gguf", "octets": 365713686528}, {"nom": "Kimi-K2.7-Code-UD-IQ1_M", "repo": "unsloth/Kimi-K2.7-Code-GGUF", "chemin": "UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00001-of-00008.gguf", "octets": 6913184}, {"nom": "Kimi-K2.7-Code-UD-IQ1_M", "repo": "unsloth/Kimi-K2.7-Code-GGUF", "chemin": "UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00002-of-00008.gguf", "octets": 49638722336}, {"nom": "Kimi-K2.7-Code-UD-IQ1_M", "repo": "unsloth/Kimi-K2.7-Code-GGUF", "chemin": "UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00003-of-00008.gguf", "octets": 48368994848}, {"nom": "Kimi-K2.7-Code-UD-IQ1_M", "repo": "unsloth/Kimi-K2.7-Code-GGUF", "chemin": "UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00004-of-00008.gguf", "octets": 48368994848}, {"nom": "Kimi-K2.7-Code-UD-IQ1_M", "repo": 
… [318 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for p in data/wikitext2_test.txt colab/Drave-reparti.ipynb tools/ref_ggml_bloc.c tools/extraire_tables_ggml.c tools/manifeste_modeles_lourds.json tools/ref_logits.cpp models/Qwen2.5-0.5B-Q8_0.gguf models/Qwen2.5-0.5B-Q4_0.gguf drave- … [579 caractères tronqués]`

  ```
OK   data/wikitext2_test.txt
OK   colab/Drave-reparti.ipynb
OK   tools/ref_ggml_bloc.c
OK   tools/extraire_tables_ggml.c
OK   tools/manifeste_modeles_lourds.json
OK   tools/ref_logits.cpp
OK   models/Qwen2.5-0.5B-Q8_0.gguf
OK   models/Qwen2.5-0.5B-Q4_0.gguf
OK   drave-core/gpu/drave_gpu.cu
OK   drave-core/gpu/drave_gpu.ptx
OK   drave-core/Cargo.toml
OK   docs/histoire.md
OK   docs/plan-deepseek-v4-flash.md
OK   docs/plan-deepseek41-complet.md
OK   docs/format-flux.md
OK   docs/contexte-long.md
OK   docs/comparaison-spiking.md
OK   reports/rapport-mode4-lot-listes.md
OK   reports/rapport-aiguille-topk.md
OK   reports/rapport-gpu-topk-selection.md
OK   reports/rapport-empreinte-memoire.md
OK   reports/rapport-lecteur-multifichiers.md
OK   REPRISE.md
OK   README.md

compiler.sh
cuda_stub.h
drave_gpu.cu
drave_gpu.ptx
  ```

- **list_agents** `{}`

  ```
2c2a6595-b208-446e-bbd1-d0f49eca45e8 [ready] — Extract Rust CLI flags part 1
18b8879c-f211-43b8-9908-cf65e509b21d [ready] — Extract Rust flags part 2
b13a6032-4f62-4e86-aa1f-03864a455c83 [ready] — Extract Python tool headers
dcaa24d6-0017-4382-be21-8244c0fb9b7a [ready] — Extract shell script headers
  ```

### 👤 Utilisateur

Agent 18b8879c-f211-43b8-9908-cf65e509b21d sent a message:
RAPPORT EXHAUSTIF — identifiants exposés dans 7 fichiers de drave-core/src (lecture seule, aucun fichier modifié)

Faits globaux vérifiés : `rg -ni '\benum\b'` sur les 7 fichiers ne rend QUE 3 enums : gguf.rs:134 Tampon, gguf.rs:180 Meta, model.rs:28 Gating. Il n'existe AUCUN enum de type de quantification dans ces 7 fichiers : les types ggml sont des constantes u32 `GGML_*` (gguf.rs:258-318) + un match de correspondance (gguf.rs:761-778 et 783-795). `Pool` (engine.rs:362), `Source`/`Source8`/`DenseQ8`/`DenseQ4`/`PushMat` (list.rs) sont HORS périmètre mais référencés par model.rs.

=====================================================================
FICHIER 1/7 : drave-core/src/clusters.rs (506 l.)
=====================================================================

--- ENUMS ---
(aucun)

--- CONSTANTES / STATIQUES ---
ACTIF — clusters.rs:125 — `static ACTIF: std::sync::OnceLock<Mapping>` — mapping du modèle courant, posé une fois à l'ouverture (jamais de drapeau global « nœud partiel », volontairement).

--- STRUCTS PUBLIQUES ET CHAMPS ---
Mapping — clusters.rs:26 (`#[derive(Clone)]`) — où trouver chaque expert global :
  n_couches : usize — 27 — nombre de couches du modèle.
  n_experts : usize — 28 — nombre d'experts globaux.
  n_clusters : usize — 29 — nombre de clusters annoncés par mapping.tsv.
  par_cluster : usize — 30 — experts par cluster (défaut n_experts/n_clusters, l.85).
  local : Vec<Vec<i32>> — 34 — PRIVÉ ; `local[couche][expert_global] = cluster*65536 + ligne`, ou -1 si absent.
Modele — clusters.rs:139 — un modèle prêt à tourner :
  gguf : Gguf — 140 — GGUF assemblé (commun + clusters préfixés).
  mapping : Mapping — 141 — mapping des experts.
  chemins : Vec<PathBuf> — 142 — fichiers ouverts (commun + cluster-*.gguf).

--- ENVIRONNEMENT ---
"DRAVE_CLUSTERS" — clusters.rs:168 — liste `0,3` de numéros de clusters ; trim + split(',') + parse::<usize> ; vide => None (tous). Erreur InvalidInput si non entier (l.170-172), NotFound si cluster demandé absent (l.252), InvalidInput si cluster hors bornes (l.244) ou liste vide (l.271).

--- LITTÉRAUX DE MODE/FORMAT ---
"n_couches" — clusters.rs:59 — clé d'en-tête TSV lue dans les lignes `#`.
"n_experts" — clusters.rs:60 — idem.
"clusters" — clusters.rs:61 — idem.
"experts_par_cluster" — clusters.rs:62 — idem (défaut = n_experts/n_clusters).
"·" — clusters.rs:54 — séparateur retiré avant découpage des commentaires.
"commun.gguf" — clusters.rs:187 — fichier obligatoire du dossier.
"cluster-" / ".gguf" — clusters.rs:200-201 — strip_prefix/strip_suffix pour extraire le NUMÉRO de cluster (jamais le rang).
"mapping.tsv" — clusters.rs:213 — table texte couche/local/global/cluster.
"cl{c}/" — clusters.rs:280 — préfixe des tenseurs d'experts (porte le NUMÉRO, pas le rang).
"#" — clusters.rs:49 — préfixe de commentaire du mapping.
"blk.0.ffn_gate_inp.weight", "token_embd.weight", "blk.0.ffn_gate_exps.weight", "cl0/…", "cl1/…", "cl2/…" — clusters.rs:363-455 — noms de tenseurs des tests.
Aucune comparaison `match` sur &str de mode/format hors clés ci-dessus.

--- FONCTIONS PUBLIQUES ---
Mapping::lire(chemin: &Path) -> io::Result<Mapping> — 39.
Mapping::ou(&self, l: usize, e: usize) -> Option<(usize,usize)> — 110 — (cluster, ligne locale).
Mapping::presents(&self, l: usize) -> usize — 117 — experts présents localement.
actif() -> Option<&'static Mapping> — 129.
ouvrir(dossier: &Path) -> io::Result<Modele> — 150.
ouvrir_sous_ensemble(dossier: &Path, clusters: Option<&[usize]>) -> io::Result<Modele> — 161.
gardes_du_milieu() -> io::Result<Option<Vec<usize>>> — 167.
ouvrir_meta(dossier: &Path) -> io::Result<Modele> — 180.

=====================================================================
FICHIER 2/7 : drave-core/src/formats.rs (2847 l.)
=====================================================================

--- ENUMS ---
(aucun)

--- CONSTANTES / STATIQUES (tables) ---
IQ2XXS_GRID — formats.rs:19-276 — `pub static IQ2XXS_GRID: [[u8; 8]; 256]` — grille IQ2_XXS : 256 codes de 8 niveaux (chaque code = u64 dont les octets sont les 8 niveaux) ; extraite de ggml-common.h. Fin de table l.276 (`];`).
KSIGNS_IQ2XS — formats.rs:278-288 — `pub static KSIGNS_IQ2XS: [u8; 128]` — paquets de signes 7 bits d'IQ2_XXS/IQ3_XXS (masque `kmask_iq2xs[j] = 1<<j`).
IQ1S_GRID — formats.rs:447-2496 — `pub static IQ1S_GRID: [[i8; 8]; 2048]` — grille IQ1_S : 2048 codes de 8 niveaux signés (-1/0/1) ; extraite de ggml-common.h. Fin l.2496 (`];`).
KVALS_IQ4NL — formats.rs:2499-2501 — `pub static KVALS_IQ4NL: [i8; 16]` = `-127,-104,-83,-65,-49,-35,-22,-10,1,13,25,38,53,69,89,113` — niveaux non linéaires d'IQ4_NL et IQ4_XS (le nibble est un INDEX dans cette table, pas une valeur).
IQ3XXS_GRID — formats.rs:2504-2761 — `pub static IQ3XXS_GRID: [[u8; 4]; 256]` — grille IQ3_XXS : 256 codes de 4 octets. Fin l.2761 (`];`).
IQ1S_DELTA — formats.rs:2766 — `const IQ1S_DELTA: f32 = 0.125` — décalage ± appliqué à chaque niveau de IQ1S_GRID (signe porté par un bit des mots qh).

--- TABLES DE CORRESPONDANCE type→taille (essentielles) ---
formats.rs ne contient PAS de match type→taille : chaque fonction de déquantification porte SA taille de bloc en dur dans son assert et ses index. Table complète :
  IQ4_XS  — 136 octets / 256 poids — dequant_iq4xs_dans, formats.rs:299 (assert l.300) ; structure : 2 o d (f16) + 2 o scales_h + 4 o scales_l + 128 o quants 4 bits ; 16 échelles de 6 bits (4 bits dans scales_l, 2 bits dans scales_h) ; sortie indexée `out[32*ib+j]`/`out[32*ib+j+16]` via KVALS_IQ4NL (l.312-313).
  IQ1_S   — 50 octets / 256 poids — dequant_iq1s_dans, formats.rs:334 (assert l.335) ; 2 o d (f16) + 32 o index de grille (l.337) + 16 u16 (l.340) portant 3 bits d'index, 3 bits d'échelle et 1 bit de signe du décalage ; `x = d·(2k+1)·(grille ± 0,125)` (l.341-347).
  IQ2_XXS — 66 octets / 256 poids — dequant_iq2xxs_dans, formats.rs:368 (assert l.369) ; 2 o d + 8 sous-blocs de 8 o (`aux = bloc[2+8*ib32 .. +8]`, l.377) ; `db = d·(0,5+scale)·0,25` (l.380) ; `x = db·grille·signe` (l.388).
  IQ3_XXS — 98 octets / 256 poids — dequant_iq3xxs_dans, formats.rs:414 (assert l.415) ; 2 o d + qs[2..98] dont ech = qs[64..96] (l.417-418) ; `db = d·(0,5+scale)·0,5` (l.423) ; pas de tableau d'échelles séparé.
  IQ1_M   — 56 octets / 256 poids — dequant_iq1m_dans, formats.rs:2775 (assert l.2776) ; ORDRE DES CHAMPS `qs[32]`, `qh[16]`, `scales[8]` (échelles EN DERNIER, l.2777-2785) ; échelle f16 répartie dans 4 mots de 16 bits (l.2787-2789) ; `x = d·(2e+1)·(grille ± 0,125)` (l.2794-2814).
Tailles « simples » correspondantes (dans gguf.rs, citées pour la table complète) : Q4_K=144, Q6_K=210, Q5_K=176, MXFP4=17/32, Q4_0=18/32, Q8_0=34/32, Q2_K=84/256, Q3_K=110/256.

--- LITTÉRAUX / COMMENTAIRES DE FORMAT ---
"bloc IQ4_XS trop court", "tampon de sortie trop court" — 300/305 ; "bloc IQ1_S trop court" — 335/338 ; "bloc IQ2_XXS trop court" — 369/371 ; "bloc IQ3_XXS trop court" — 415/419 ; "bloc IQ1_M trop court" — 2776/2792.
`ggml-common.h`, `tools/extraire_tables_ggml.sh`, `libggml` — 9-11 (provenance des tables).

--- FONCTIONS PUBLIQUES ---
dequant_iq4xs_dans(bloc: &[u8], out: &mut [f32]) — 299 ; dequant_iq4xs(bloc) -> Vec<f32> — 320 ; dequant_iq1s_dans — 334 ; dequant_iq1s — 355 ; dequant_iq2xxs_dans — 368 ; dequant_iq2xxs — 396 ; dequant_iq3xxs_dans — 414 ; dequant_iq3xxs — 440 ; dequant_iq1m_dans — 2775 ; dequant_iq1m — 2822.
Tests (2829-2847) : `iq2xxs_taille_et_plausibilite` vérifie `IQ2XXS_GRID.len()==256` (l.2844) et `KSIGNS_IQ2XS.len()==128` (l.2845).

=====================================================================
FICHIER 3/7 : drave-core/src/gpu.rs (1573 l.)
=====================================================================

--- ENUMS ---
(aucun)

--- CONSTANTES / STATIQUES ---
PTX — gpu.rs:40 — `const PTX: &str = include_str!("../gpu/drave_gpu.ptx")` — PTX compilé depuis gpu/drave_gpu.cu par clang, chargé par l'API pilote.
CHUNK — gpu.rs:819 — `const CHUNK: usize = 4096` — taille de tranche (nombre de clés) du radix select de la collecte top-k ; `ntr = n.div_ceil(CHUNK)` (l.826).
INSTANCE — gpu.rs:1532 — `static INSTANCE: OnceLock<Option<Gpu>>` — instance unique du processus ; activée seulement par `DRAVE_GPU`.
SECOND — gpu.rs:1536 — `static SECOND: OnceLock<Option<Gpu>>` — second périphérique (KV déporté moitié/moitié).
MACHINES — gpu.rs:1550 — `static MACHINES: OnceLock<Vec<&'static Gpu>>` — liste ordonnée des périphériques disponibles.

--- STRUCTS PUBLIQUES ET CHAMPS ---
MatriceGpu — gpu.rs:74 — matrice résidente GPU + tampons E/S :
  poids : u64 — 75 (privé) — pointeur device des poids.
  x_dev : u64 — 76 (privé) — tampon d'entrée (activations).
  out_dev : u64 — 77 (privé) — tampon de sortie.
  n_out : usize — 78 — lignes de sortie.
  nb : usize — 79 — nombre de blocs par ligne.
  octets_poids : usize — 80 — octets de poids copiés.
KvGpu — gpu.rs:86 — cache KV d'UNE couche en VRAM (disposition identique à KvCache) :
  k, v, sk, sv : u64 — 87-90 — pointeurs VRAM clés/valeurs et leurs échelles.
  n_kv : usize — 91 — têtes KV.
  ctx : usize — 93 — capacité LOGIQUE (positions adressables).
  capacite : usize — 99 — capacité ALLOUÉE, doublée à la demande (pagination par doublement).
  hd : usize — 100 — dimension de tête.
  nb : usize — 101 — blocs de 32 par tête.
  bits : u32 — 103 — 32 = f32, 8 = un octet/valeur, 4 = deux nibbles/octet.
  scores_dev : u64 / scores_cap : usize — 105-106 — tampon des scores (`attn_scores`).
  histo_dev : u64 / histo_cap : usize — 109-110 — histogrammes radix `[lignes][256]` u32 (14 têtes × 1 ko).
  prefixes_dev : u64 / prefixes_cap : usize — 112-113 — préfixes du radix select.
  topk : Option<TamponsTopk> — 115 — tampons de la collecte des k indices.
  octets : usize — 116 — total alloué.
  q_dev, part_dev, out_dev, sinks_dev : u64 — 121-124 — tampons de travail réutilisés.
  q_cap, part_cap, out_cap, sinks_cap : usize — 125-128 — leurs capacités.
TamponsTopk — gpu.rs:133 — tampons VRAM de la collecte top-k (noyaux 2b) :
  lignes : usize — 134 ; ntr : usize — 135 (tranches = div_ceil(CHUNK)) ; k : usize — 136 ; chunk : usize — 137.
  comptes : u64 / cap_comptes — 139-140 — `compte_sup[l][t]` puis `compte_eq[l][t]`.
  bases : u64 / cap_bases — 142-143 — `base_sup[l][t]` / `base_eq[l][t]`.
  meta : u64 / cap_meta — 145-146 — `prefixes[l]`, `debut_egaux[l]`, `besoin[l]`.
  sortie : u64 / cap_sortie — 148-149 — `sortie[l][k]` indices retenus.
Gpu — gpu.rs:152 — contexte CUDA + noyaux :
  ctx : *mut c_void — 153 (privé) ; module : *mut c_void — 154 (privé).
  f_tete, f_proj, f_tete_warp, f_proj_warp, f_mxfp4_warp, f_q4k_warp, f_q6k_warp : *mut c_void — 155-161 (privés) — fonctions noyaux Q8/MXFP4/Q4K/Q6K.
  f_attn_part, f_attn_recombine : *mut c_void — 162-163 (privés).
  f_attn_scores : *mut c_void — 165 (privé) — scores seuls (noyau 1 du top-k).
  f_attn_topk_histo : *mut c_void — 167 (privé) — histogramme du radix select (noyau 2a).
  f_attn_topk_compte, f_attn_topk_ecrit : *mut c_void — 169-170 (privés) — comptage par tranche + écriture ordonnée.
  f_attn_topk_somme : *mut c_void — 172 (privé) — softmax des k + somme pondérée des V (noyau 3).
  f_attn_topk_tout : *mut c_void — 175 (privé) — top-k complet d'une ligne en un lancement (noyau 4).
  nom : String — 176 — « GPU {ordinal} ».
  ordinal : c_int — 178 — numéro de périphérique.
  memoire_libre : usize — 179 — VRAM libre relevée par cuMemGetInfo_v2.

--- ENVIRONNEMENT ---
"DRAVE_GPU" — gpu.rs:1540 (`second()`) et gpu.rs:1565 (`instance()`) — `is_err()` => None : sans elle, aucune ressource vidéo n'est touchée (tout CPU). Dans second() : balayage `for ord in 0..4` en sautant le premier (l.1542-1545).

--- LITTÉRATÉRAUX DE MODE/FORMAT (noms de noyaux PTX, résolus par cuModuleGetFunction) ---
"cuda" — gpu.rs:16 — `#[link(name = "cuda")]`.
"tete_q8" — 231 ; "proj_q8" — 238 ; "tete_q8_warp" — 245 ; "proj_q8_warp" — 252 ; "proj_mxfp4_warp" — 259 ; "proj_q4k_warp" — 266 ; "proj_q6k_warp" — 273 ; "attn_kv_partiels" — 280 ; "attn_scores" — 287 ; "attn_topk_histo" — 294 ; "attn_topk_compte" — 301 ; "attn_topk_ecrit" — 308 ; "attn_topk_somme" — 315 ; "attn_topk_tout" — 322 ; "attn_kv_recombine" — 329.
"GPU {ordinal}" — 347.
Messages d'erreur indexés par nom de noyau : "lancement attn_scores" 625/713, "lancement attn_topk_histo" 796, "lancement attn_topk_compte" 896, "lancement attn_topk_ecrit" 947, "lancement attn_topk_somme" 1058, "lancement attn_topk_tout" 1160, "lancement attn_kv_partiels" 1241, "lancement attn_kv_recombine" 1280, "lancement proj_q6k_warp" 1332, "lancement proj_q4k_warp" 1368, "lancement proj_mxfp4_warp" 1404, "lancement proj" 1441, "lancement tete_q8_warp" 1483.

--- VALEURS DE FORMAT/SEUILS EN DUR (rôle) ---
34 — 362 — octets par bloc Q8_0 (échelle f16 + 32 niveaux), employé aussi pour la tête.
17 — 387/… — octets par bloc MXFP4 (bloc de 32 poids).
144 — 406 — octets par super-bloc Q4_K (256 poids).
256 — 415 — poids par super-bloc Q4_K pour dimensionner le tampon d'activation.
4096 — 222 — allocation témoin après création du contexte (sonde CUDA).
32/8/4 — 449 et 524 — `pas` par valeur selon `bits` : `32 => hd*4, 8 => hd, 4 => hd/2`.
ctx.min(2048) — 434 — première tranche allouée au KV GPU.
`cap = (cap*2).min(m.ctx)` — 448 — doublement de capacité.
`fils: c_uint = 256` et `blocs.min(65535)` — 1436-1438, 1477-1480, 1513-1516 — géométrie de lancement des noyaux.
`for ord in [1, 0]` — 188 — ouvrir_auto essaie le périphérique 1 puis 0 (celui qui pilote l'affichage peut refuser).
`cuMemAlloc_v2(&mut temoin, 4096)` — 222 — sonde.
`(n_in*4)` — partage mémoire dynamique des noyaux.

--- FONCTIONS PUBLIQUES (identifiants exposés) ---
Gpu::ouvrir_auto() -> Option<Gpu> — 187 ; Gpu::ouvrir(ordinal: c_int) -> Option<Gpu> — 195 ; charger_tete(blocs,n_out,_n_in,nb) -> Option<MatriceGpu> — 356 ; charger_proj — 379 ; charger_mxfp4 — 385 ; charger_q4k(144 o) — 404 ; kv_allouer(n_kv,ctx,hd,bits) — 424 ; kv_assurer — 440 ; kv_ecrire_tranche — 519 ; kv_ecrire — 548 ; attn_scores — 561 ; attn_scores_sans_relecture — 641 ; attn_topk_histo — 736 ; attn_topk_collecte — 815 ; attn_topk_somme — 968 ; attn_topk_tout — 1077 ; attn_kv — 1178 ; charger_q6k — 1288 ; proj_q6k — 1307 ; proj_q4k — 1343 ; proj_mxfp4 — 1379 ; proj — 1416 ; tete_warp — 1458 ; tete — 1494 ; second() -> Option<&'static Gpu> — 1538 ; machines() -> &'static [&'static Gpu] — 1554 ; instance() -> Option<&'static Gpu> — 1563.
unsafe impl Send/Sync pour Gpu (1570-1571) et MatriceGpu (1572-1573).

=====================================================================
FICHIER 4/7 : drave-core/src/gguf.rs (2246 l.)
=====================================================================

--- ENUMS ---
Tampon — gguf.rs:134 — octets d'un fichier, lus ou mappés :
  Tampon::Lu(Vec<u8>) — 135 — fichier lu entièrement en mémoire.
  Tampon::Mappe(Mappe) — 136 — fichier mmappé (déréférencement en &[u8] via Deref, l.139-145).
Meta — gguf.rs:180 — `#[derive(Debug, Clone)]` — valeur de métadonnée GGUF :
  Meta::U8(u8) / I8(i8) / U16(u16) / I16(i16) / U32(u32) / I32(i32) — 181.
  Meta::F32(f32) / Bool(bool) / Str(String) / Array(Vec<Meta>) / U64(u64) / I64(i64) / F64(f64) — 182.
  (Types de métadonnée GGUF correspondants lus dans Cur::value, l.381-399 : 0=U8, 1=I8, 2=U16, 3=I16, 4=U32, 5=I32, 6=F32, 7=Bool(1 octet), 8=Str, 9=Array, 10=U64, 11=I64, 12=F64 ; autre => panic "type de métadonnée inconnu".)

--- CONSTANTES / STATIQUES ---
PROT_READ — gguf.rs:45 — `const PROT_READ: i32 = 1` — protection mmap lecture seule.
MAP_PRIVATE — gguf.rs:46 — `const MAP_PRIVATE: i32 = 2` — mapping privé (copy-on-write).
MADV_WILLNEED — gguf.rs:53 — `const MADV_WILLNEED: i32 = 3` — conseil noyau « lance les lectures en avance ».
GGML_F32 — 258 — `u32 = 0` — type ggml F32 (1 valeur/bloc, 4 octets).
GGML_F16 — 259 — `u32 = 1` — F16 (1, 2 o).
GGML_Q4_0 — 260 — `u32 = 2` — Q4_0 (bloc 32, 18 o).
GGML_MXFP4 — 261 — `u32 = 39` — MXFP4 (bloc 32, 17 o).
GGML_Q2_K — 262 — `u32 = 10` — Q2_K (bloc 256, 84 o).
GGML_BF16 — 263 — `u32 = 30` — BF16 (1 valeur, 2 o).
GGML_Q3_K — 264 — `u32 = 11` — Q3_K (256, 110 o).
GGML_Q4_K — 265 — `u32 = 12` — Q4_K (256, 144 o).
GGML_Q5_0 — 271 — `u32 = 6` — Q5_0 (32, 22 o) ; type de `token_embd` et des `ffn_gate/up` de Qwen2.5-0.5B Q4_K_M (62 % des poids).
GGML_Q5_1 — 272 — `u32 = 7` — Q5_1 (32, 24 o, avec minimum f16).
GGML_Q5_K — 273 — `u32 = 13` — Q5_K (256, 176 o).
GGML_Q6_K — 274 — `u32 = 14` — Q6_K (256, 210 o).
GGML_IQ2_XXS — 278 — `u32 = 16` — IQ2_XXS (256, 66 o), experts de DeepSeek-V4.1.
GGML_IQ3_XXS — 281 — `u32 = 18` — IQ3_XXS (256, 98 o), 30 % des poids de Kimi/GLM-5.3/V4-Flash.
GGML_IQ1_S — 283 — `u32 = 19` — IQ1_S (256, 50 o), 42-45 % des poids de GLM.
GGML_IQ4_XS — 286 — `u32 = 23` — IQ4_XS (256, 136 o).
GGML_IQ1_M — 287 — `u32 = 29` — IQ1_M (256, 56 o), experts de V4-Flash.
TAILLE_Q4K — 295 — `pub const usize = 144` — octets par super-bloc Q4_K = 2+2+12+128 (256 poids).
TAILLE_Q6K — 296 — `pub const usize = 210` — octets par super-bloc Q6_K = 128+64+16+2.
TAILLE_Q5K — 299 — `pub const usize = 176` — octets par super-bloc Q5_K = 2+2+12+32+128.
GGML_Q4_1 — 314 — `u32 = 3` — Q4_1 (32, 20 o).
GGML_Q8_0 — 315 — `u32 = 8` — Q8_0 (32, 34 o).
GGML_I32 — 318 — `u32 = 26` — I32 (1 valeur, 4 o), table de routage `ffn_gate_tid2eid` de DeepSeek-V4.
SIGNALES — gguf.rs:747 — `static SIGNALES: Mutex<Vec<u32>>` (dans `octets_tensor`) — types inconnus déjà signalés une fois (inventaire sous-évalué plutôt que silencieux).
KV — gguf.rs:1068 — `const KV: [f32; 16] = [0.0,0.5,1.0,1.5,2.0,3.0,4.0,6.0, 0.0,-0.5,-1.0,-1.5,-2.0,-3.0,-4.0,-6.0]` (dans `dequant_mxfp4`) — niveaux E2M1 du MXFP4.
KMASK1 — gguf.rs:1205 — `const KMASK1: u32 = 0x0303_0303` (dequant Q2_K) — masque des 2 bits hauts d'échelle.
KMASK2 — gguf.rs:1206 — `const KMASK2: u32 = 0x0f0f_0f0f` — masque des 4 bits bas d'échelle.
KV — gguf.rs:1718 (test `dequant`) — `const KV: [f32; 16] = [0.0; 16]` — neutralisé (`let _ = KV;`).
Table de test l.2186-2188 : `[(GGML_F32, 4*1024), (GGML_Q8_0, 34*32), (GGML_Q4_K, 144*4), (GGML_Q6_K, 210*4), (GGML_MXFP4, 17*32), (29, 56*4), (30, 2*1024)]`.

--- TABLES DE CORRESPONDANCE type→taille (INTÉGRALES) ---
(1) `Gguf::octets_tensor_opt` — gguf.rs:759-779 — match `(bloc, octets)` puis `n / bloc * octets` :
  0 => (1u64, 4u64)   1 => (1, 2)       2 => (32, 18)      3 => (32, 20)          [l.762]
  6 => (32, 22)       7 => (32, 24)     8 => (32, 34)      9 => (32, 36)          [l.763]
  10 => (256, 84)     11 => (256, 110)  12 => (256, TAILLE_Q4K=144)              [l.764]
  13 => (256, 176)    14 => (256, TAILLE_Q6K=210)  15 => (256, 292)              [l.765]
  16 => (256, 66)     17 => (256, 74)   18 => (256, 98)    19 => (256, 50)        [l.766]
  20 => (32, 18)      21 => (256, 110)  22 => (256, 82)    23 => (256, 136)       [l.767]
  24 => (1, 1)        25 => (1, 2)      26 => (1, 4)       27 => (1, 8)  28 => (1, 8) [l.768]
  29 => (256, 56)     30 => (1, 2)      34 => (256, 54)    35 => (256, 66)        [l.769]
  39 => (32, 17)      40 => (64, 36)                                             [l.770]
  41 => (128, 18)     42 => (64, 18)    43 => (32, 26)     44 => (32, 28)         [l.774]
  45 => (32, 14)      46 => (32, 16)    47 => (32, 10)     48 => (32, 12)         [l.775]
  _ => return None                                                               [l.776]
  Types 41-48 « ajoutés à ggml après NVFP4 », noms lus dans ggml.h, tailles relevées par tools/verifier_table_types.sh.
(2) `Gguf::nom_type` — gguf.rs:783-798 — id → nom :
  0 "F32", 1 "F16", 2 "Q4_0", 3 "Q4_1", 6 "Q5_0", 7 "Q5_1", 8 "Q8_0", 9 "Q8_1", 10 "Q2_K", 11 "Q3_K", 12 "Q4_K", 13 "Q5_K", 14 "Q6_K", 15 "Q8_K", 16 "IQ2_XXS", 17 "IQ2_XS", 18 "IQ3_XXS", 19 "IQ1_S", 20 "IQ4_NL", 21 "IQ3_S", 22 "IQ2_S", 23 "IQ4_XS", 24 "I8", 25 "I16", 26 "I32", 27 "I64", 28 "F64", 29 "IQ1_M", 30 "BF16", 34 "TQ1_0", 35 "TQ2_0", 39 "MXFP4", 40 "NVFP4", 41 "Q1_0", 42 "Q2_0", 43 "Q6_0", 44 "Q6_1", 45 "Q3_0", 46 "Q3_1", 47 "Q2_0S", 48 "Q2_1" ; défaut `format!("type {ttype}")`.
(3) Délégation taille+fonction de déquantification, `row_f32` — gguf.rs:1349-1358 : Q2_K (84, Self::dequant_q2k), Q3_K (110, Self::dequant_q3k), Q5_K (TAILLE_Q5K, Self::dequant_q5k), IQ2_XXS (66, formats::dequant_iq2xxs), IQ3_XXS (98, formats::dequant_iq3xxs), IQ1_S (50, formats::dequant_iq1s), IQ4_XS (136, formats::dequant_iq4xs), _ (56, formats::dequant_iq1m).
(4) Même table dans `dequant` — gguf.rs:1774-1782 (identique).
(5) `Q8View`/`q8_view` bloc — gguf.rs:1447-1454 : Q8_0 => q4=false ; Q4_0 => q4=true ; Q4_K | Q6_K => q4=true ; autre => panic "q8_view : type {other} non géré" ; `bloc = if Q4_K|Q6_K {256} else {32}` (l.1454).
(6) Gardes de type par accesseur : q8_blocks exige GGML_Q8_0 (1473), q4k_blocks GGML_Q4_K (1481), q6k_blocks GGML_Q6_K (1488), mxfp4_blocks GGML_MXFP4 (1497), q4_blocks GGML_Q4_0 (1508).
(7) `raw_levels` — gguf.rs:1037-1059 : GGML_Q8_0 et GGML_Q4_0 gérés, `other => panic!("raw_levels : type {other} non géré")`.
(8) `dequant_q5_0 | dequant_q5_1` — 1409-1410 et 1705-1706 — choix par `t.ttype == GGML_Q5_0`.
(9) Déquantification de `dequant` par type — gguf.rs:1659-1787 : GGML_BF16 1660, GGML_F32 1666, GGML_F16 1671, GGML_Q8_0 1676, GGML_Q4_0 1684, GGML_Q4_1 1693, GGML_Q5_0|GGML_Q5_1 1705, GGML_MXFP4 1714, GGML_Q4_K 1721, GGML_Q6_K 1741, groupe IQ 1772-1782, `other => panic!("dequant : type {other} non géré")` 1787.

--- STRUCTS PUBLIQUES ET CHAMPS ---
Mappe — gguf.rs:30 — fichier mmappé : ptr : *mut u8 (31, privé), len : usize (32, privé) ; `unsafe impl Send/Sync` 37-38 ; Drop => munmap 124-128.
TensorInfo — gguf.rs:242 — `#[derive(Debug, Clone)]` :
  name : String — 243 ; dims : Vec<u64> — 244 (convention numpy, le plus lent d'abord ; ggml stocke à l'envers, inversé l.848) ; ttype : u32 — 245 (id ggml) ; offset : u64 — 246 (octets depuis le début des données du fichier) ; fichier : usize — 251 (index du fichier porteur, pour shards/clusters).
  méthode nelem() -> usize — 255.
Q8View — gguf.rs:321 — pointeur pré-résolu vers les lignes d'un tenseur quantifié (Q8_0 ou Q4_0) :
  fichier : usize — 323 ; base : usize — 324 ; n_cols : usize — 325 ; nb : usize — 326 ; q4 : bool — 327 ; ttype : u32 — 330 (type d'origine : la tête peut être Q8_0, Q4_0 ou Q4_K et se lit en place).
Gguf — gguf.rs:333 — lecteur :
  meta : HashMap<String, Meta> — 334 ; tensors : Vec<TensorInfo> — 335 ; bufs : Vec<Tampon> — 339 (privé, un par fichier) ; starts : Vec<usize> — 341 (privé, début des données de chaque fichier, aligné).
Cur<'a> — gguf.rs:344 — curseur de lecture binaire (privé) : b : &'a [u8], p : usize, deborde : bool.

--- ENVIRONNEMENT ---
"DRAVE_PRELIRE_TOUT" — gguf.rs:91 — `matches!(var.as_deref(), Ok("1") | Ok("oui") | Ok("true"))` — demander le fichier ENTIER au chargement (désactivé par défaut).
"DRAVE_PRELIRE" — gguf.rs:95 — active la prélecture madvise ; désactivée si `"0"` ou `eq_ignore_ascii_case("non")` ou `"false"` ; défaut = activée (`Err(_) => true`).
"DRAVE_MMAP" — gguf.rs:156 — mapper les fichiers ; désactivé si `"0"`/`"non"`/`"false"` ; défaut = mappé (`Err(_) => true`) ; en cas d'échec mmap => repli lecture complète (l.169).

--- LITTÉRAUX DE MODE/FORMAT ---
b"GGUF" — gguf.rs:827 — magie vérifiée sur les 4 premiers octets (`entete_de`) ; b"GGUF" aussi en test 480/482 (clusters.rs).
`version >= 2` — gguf.rs:830 — `assert!(version >= 2, "version GGUF {version} non gérée")`.
"general.architecture" — 496, 498, 501, 671, 673, 676, 885 (et tests 1819/1897/1948/2000/2085) — clé d'architecture ; `cfg()` compose `format!("{arch}.{key}")` (l.886).
"general.alignment" — 880 (et tests 1900/1951/2003) — alignement des données, défaut 32.
"config" — 947 — bloc `<arch>.config` (JSON recopié).
"attention.compress_ratios" / "compress_ratios" — 904 (couches_ratios) et 914 (couches_compressees) — ratios par couche, 0 = brute.
"hyper_connection.count" — 933 ; "hyper_connection.sinkhorn_iterations" — 934 (défaut 20) ; "hyper_connection.epsilon" — 936 (défaut 1e-6) — hyper-connexions V4.
"hc_mult" / "hc_sinkhorn_iters" / "hc_eps" — 933/934/938 — noms d'origine dans le JSON.
"expert_count" / "n_routed_experts" — 1838 (test `cfg_ou`).
"true" / "false" — 974-975 (analyseur JSON) et 990 (`json_bool` : `v == "true"`).
Codes de type de métadonnée 0..12 — 381-399 (match `vt`).
Suffixes de fichiers éclatés : `-00001-of-00003.gguf` (test 2218) ; `shard_de` 548 ; `chemins_du_modele` 566.

--- FONCTIONS PUBLIQUES (identifiants exposés) ---
prelire 65 ; prelire_tout 84 ; prelire_tout_voulu 90 ; bf16_to_f32 292 ; echelle_min_q4k 306 ; Mappe::ouvrir 103 (privé) ; Tampon::len/is_empty 148-149 ; Meta::as_liste_i64 190, as_liste_f32 201, as_u64 209, as_bool 218, as_f64 229, as_str 236 ; TensorInfo::nelem 255 ; Gguf::open 405, open_meta 428, open_multi 470, open_avec_prefixes 478, shard_de 548, chemins_du_modele 566, open_auto 605, open_meta_auto 619, open_multi_meta 634, open_meta_avec_prefixes 640, octets_tensor 741, octets_tensor_opt 759, nom_type 783, octets_poids 801, nb_fichiers 808, octets_charges 811, est_mappe 814, tranche_publique 860, cfg 884, cfg_ou 898, couches_ratios 903, couches_compressees 913, hc_params 928, json_brut 956, json_nombre 983, json_texte 987, json_bool 989, tensor 993, f32_to_f16 999, f16_to_f32 1011, raw_levels 1032, dequant_mxfp4 1066, echelle_e8m0 1089, dequant_q5_0 1100, dequant_q5_1 1107, dequant_q5k 1143, dequant_q5k_dans 1149, dequant_q3k 1190, dequant_q3k_dans 1196, dequant_q2k 1248, dequant_q2k_dans 1254, dequant_optionnel 1285, dequant_i32 1296, row_f32 1305, q8_view 1445, data_ptr 1460, type_de 1466, q8_blocks 1471, q4k_blocks 1479, q6k_blocks 1486, mxfp4_blocks 1495, q4_blocks 1506, q8_dot_at 1515, dequant 1654.

=====================================================================
FICHIER 5/7 : drave-core/src/materiel.rs (478 l.)
=====================================================================

--- ENUMS ---
(aucun)

--- CONSTANTES ---
VRAM — materiel.rs:383 — `const VRAM: f64 = 84.9` — débit VRAM mesuré (Go/s) pour le coût par jeton (noyau warp).
RAM — materiel.rs:384 — `const RAM: f64 = 22.5` — débit RAM mesuré 20 cœurs physiques.
NVME — materiel.rs:385 — `const NVME: f64 = 31.0` — débit NVMe mesuré à 16 lecteurs parallèles.
SUCCES — materiel.rs:388 — `const SUCCES: f64 = 0.80` — taux de succès du cache d'experts (25 % de l'empreinte sert 80 % des appels), appliqué au trafic.

--- STRUCTS PUBLIQUES ET CHAMPS (description matérielle + plan) ---
Noeud — materiel.rs:24 (`#[derive(Debug, Clone)]`) — nœud NUMA : id : usize (25), cpus : Vec<usize> (26), memoire_go : f64 (27).
Cpu — materiel.rs:31 : physiques : usize (32), logiques : usize (33), paires : Vec<Vec<usize>> (37, threads logiques par cœur physique), noeuds : Vec<Noeud> (38), l1_ko/l2_ko/l3_ko : usize (39-41).
Gpu — materiel.rs:45 : ordinal : i32 (46), nom : String (47), vram_libre_go : f64 (48), vram_totale_go : f64 (49), noeud : Option<usize> (50), liens_nvlink : usize (52, 25,8 Go/s soit 2× PCIe).
Disque — materiel.rs:56 : chemin : String (57), libre_go : f64 (58), noeud : Option<usize> (59), artefact : bool (62, disque des artefacts lu en flux).
Materiel — materiel.rs:65 : cpu : Cpu (66), gpus : Vec<Gpu> (67), ram_totale_go (68) / ram_libre_go (69) : f64, disques : Vec<Disque> (70).
Plan — materiel.rs:75 (`#[derive(Debug, Clone)]`) — plan GPU/CPU de configuration :
  threads : usize — 76 — cœurs physiques retenus.
  epinglage : Option<Vec<usize>> — 78 — placement explicite si < 8 cœurs et HT disponible.
  lecteurs : usize — 79 — lecteurs disque parallèles.
  cache_experts_go : f64 — 80 — VRAM allouée au cache d'experts.
  kv_bits : u32 — 81 — quantification du cache KV (8 ou 32).
  raisons : Vec<String> — 82 — justification de chaque choix (affichée par --materiel).

--- ENVIRONNEMENT ---
(aucun `env::var` dans ce fichier)

--- LITTÉRAUX / CHEMINS ET MODES ---
"/sys/devices/system/cpu" — 94 ; "cpu" (strip_prefix) — 98 ; "topology/physical_package_id" — 101 ; "topology/core_id" — 103.
"/sys/devices/system/node" — 120 ; "node" — 124 ; "cpulist" — 126 ; "meminfo" — 129.
"/sys/devices/system/cpu/cpu0/cache" — 140 ; "level" — 144 ; "type" — 145 ; "Instruction" (exclusion) — 147 ; "size" — 148 ; "L1d"/"L2"/"L3" — 156.
"nvidia-smi" — 179 et 193 ; "--query-gpu=index,name,memory.total,memory.free" — 180 ; "--format=csv,noheader,nounits" — 181 ; "nvlink","-s","-i" — 194 ; "GB/s" (comptage des liens) — 196 ; "/sys/bus/pci/devices/0000:{:02x}:00.0/numa_node" — 199.
"/proc/meminfo" — 213 et 223 ; "MemAvailable:" — 214/230 ; "MemTotal:" — 229.
"/home/stephane/FastNVMe" (artefact=true) — 244 ; "/home/stephane/Data13TB" (artefact=false) — 245 ; "df" + "-B","G","--output=avail" — 248 ; "findmnt","-no","SOURCE" — 255 ; "/dev/" — 260 ; "nvme" — 261 ; "mapper/" et "sd" — 263 ; "sda" — 266 ; "/sys/block/{bloc}/device/numa_node" — 268 ; 'G' trim — 251 ; 'K'/'M' trim — 149.

--- VALEURS/SEUILS DE MODE EN DUR (rôle) ---
`self.cpu.physiques < 8 && logiques > physiques` — 306 — déclenche l'épinglage hyperthread (+27 %).
`16.min(self.cpu.physiques.max(4))` — 322 — nombre de lecteurs disque.
`reserve = 2.0` — 329 — Go réservés au contexte CUDA/tampons/KV.
`commun_go = 8.0` — 330 — tête + attention + embeddings (V4.1).
`cache_experts_go = (vram - reserve - commun_go).max(0.0)` — 331.
`kv_par_jeton_f16 = 90_000.0` — 348 — octets par jeton en F16, 40 couches MLA.
`kv_bits = if kv_go > 0.35 * ram_libre_go { 8 } else { 32 }` — 350 — bascule int8 au-delà de 35 % de la RAM libre.
`n_experts as f64 * mo_par_expert / 1000.0` — 357 — empreinte experts en Go.
`101` : division `ko / 1e6` — conversions Ko→Go (133, 217, 229, 230).

--- FONCTIONS PUBLIQUES ---
ram_libre_go() -> f64 — 212 ; Materiel::detecter() -> Materiel — 276 ; Materiel::plan(&self, ctx, taille_modele_go, n_experts, mo_par_expert) -> Plan — 288 ; Materiel::cout_par_jeton(&self, plan, go_experts_par_jeton, go_tete, go_commun) -> String — 381 ; Materiel::resume(&self) -> String — 408.
(liste_cpus privée 160 ; detecter_cpu 91 ; detecter_gpus 178 ; detecter_ram 221 ; detecter_disques 242.)

=====================================================================
FICHIER 6/7 : drave-core/src/model.rs (7022 l.)
=====================================================================

--- ENUMS ---
Gating — model.rs:28 — `#[derive(Clone, Copy, PartialEq, Eq, Debug)]` — convention de routage des experts, 4 variantes :
  Gating::Softmax — 31 — softmax sur TOUS les logits, top-k, renormalisation (Qwen3-MoE, défaut llama.cpp).
  Gating::Sigmoid — 34 — sigmoïde par logit, top-k, renormalisation (Kimi-K2.7 `expert_gating_func=2`, GLM-5.3).
  Gating::SoftmaxPoids — 38 — top-k sur logits bruts (+ biais), puis softmax sur les k seuls, sans renormalisation (gpt-oss).
  Gating::SqrtSoftplus — 41 — `sqrt(softplus(x))` par logit, top-k, renormalisation (DeepSeek V4-Flash `expert_gating_func=4`, V4.1).
  Correspondance numéro→variante : `Gating::du_numero` — 46-53 — 1=Softmax, 2=Sigmoid, 3=SoftmaxPoids, 4=SqrtSoftplus, autre => None.
  `Gating::nom()` — 57-63 — "softmax", "sigmoïde", "top-k brut + softmax", "racine de softplus".
(Aucun enum de quantification dans model.rs ; `crate::list::Source` — hors périmètre — est l'enum de source de blocs utilisé par Vue4.)

--- CONSTANTES / STATIQUES (y compris dans fonctions et tests) ---
SEUIL_GPU — model.rs:1049 — `const SEUIL_GPU: usize = 8 << 20` (8 Mio) — taille minimale d'une projection Q8 pour valoir l'envoi GPU (~60 µs d'aller-retour).
TOPK_GPU_ECHEC — 2434 — `static TOPK_GPU_ECHEC: AtomicBool = false` — un seul message pour un échec de la chaîne top-k déportée (`DRAVE_GPU_TOPK`).
TETE_ACTIFS — 2439 — `pub static TETE_ACTIFS: AtomicU64 = 0` — densité de l'entrée de la tête (numérateur).
TETE_TOTAL — 2440 — `pub static TETE_TOTAL: AtomicU64 = 0` — total des entrées de tête examinées.
TETE_APPELS — 2441 — `pub static TETE_APPELS: AtomicU64 = 0` — nombre d'appels de tête mesurés.
LOT_TOPK_IGNORE — 2465 — `static LOT_TOPK_IGNORE: AtomicBool = false` — un seul message pour `--attn-topk` ignoré en mode lot.
SEUIL_PROFIL — 3514 — `const SEUIL_PROFIL: f32 = 0.05` — fraction du max pour qu'un neurone soit « chaud » (profilage) ; un seuil absolu à 16 bits laisserait passer 51 104 % de densité.
LIMITE — 3652 — `const LIMITE: f32 = 7.0` — écrêtage ±7 de l'activation gpt-oss.
ALPHA — 3653 — `const ALPHA: f32 = 1.702` — pente de la sigmoïde rapide de gpt-oss : `g·σ(1,702·g)·(u+1)`.
SEUIL_NOYAU4 — 5535 — `const SEUIL_NOYAU4: usize = 131_072` — nombre de clés sous lequel le noyau 4 fusionné (`attn_topk_tout`) bat la chaîne séparée (mesuré : 0,85 vs 0,89 ms à 131 k ; 1,58 vs 1,35 à 262 k).
TUILE_TETE — 5972 — `const TUILE_TETE: usize = 16` — jetons par tuile dans `logits_lot` (la ligne de poids reste chaude).
BLOC — 6132 — `const BLOC: usize = 32` — canaux par bloc d'échelle en trace v3 (`flux_en_liste_blocs` ; indice u16 => max 65 535 canaux).
S — 6559 — `static S: AtomicU64 = 0x9E3779B97F4A7C15` (dans `rand_u64`) — graine xorshift64 (constante de Weyl).
MELANGE — 6737 — `const MELANGE: [f32; 288]` (test hc_synthetique) — poids `hc_fn` synthétiques (hc=4, h=3) générés par tools/hc_synthetique.py.
BASE — 6775 — `const BASE: [f32; 24]` — biais `hc_base` synthétiques (2·hc + hc² = 24).
SCALE — 6780 — `const SCALE: [f32; 3]` = 0.5, 1.5, 2.0 — échelles pre/post/comb.
X — 6783 — `const X: [f32; 12]` — entrée synthétique (hc·h = 12).
Y — 6787 — `const Y: [f32; 3]` — sortie de sous-couche synthétique.
PRE — 6790 — `const PRE: [f32; 4]` — attendu après Sinkhorn (entrée).
POST — 6793 — `const POST: [f32; 4]` — attendu (sortie).
COMB — 6796 — `const COMB: [f32; 16]` — attendu (hc·hc = 16).
ENTREE — 6800 — `const ENTREE: [f32; 3]` — attendu du mélange d'entrée.
SORTIE — 6803 — `const SORTIE: [f32; 12]` — attendu des copies de sortie.

--- STRUCTS PUBLIQUES ET CHAMPS (config / description) ---
Routage — model.rs:242 — convention de routage lue du GGUF :
  n_expert : usize 243 ; n_expert_used : usize 244 ; ffn_exp : usize 245 ; gating : Gating 246 ; source : &'static str 248 (d'où vient le gating : "expert_gating_func", "JSON scoring_func", "défaut du moteur") ; norm : bool 249 ; echelle : f32 250 ; hash_layers : usize 251.
Cfg — model.rs:416 — configuration d'architecture :
  n_layer 417 ; hidden 418 ; n_head 419 ; n_kv_head 420 ; head_dim 421 ; ffn 422 ; eps : f32 423 ; rope_base : f32 424 ; vocab 425 ; n_expert 428 ; n_expert_used 429 ; ffn_exp 430 ; ffn_act_oss : bool 435 (activation gpt-oss, pas SiLU) ; gating : Gating 444 ; expert_norm : bool 449 ; expert_scale : f32 455 (1,5 V4 ; 2,5 GLM-5.3 ; 2,827 Kimi) ; hash_layers : usize 459 ; n_rot : usize 463 (rotary partiel) ; yarn : Option<(f32,f32,f32,f32,bool)> 466 — (facteur, beta_rapide, beta_lent, contexte d'origine, mscale).
Proj — model.rs:472 — projection, un des deux formats + biais :
  gpu : Option<crate::gpu::MatriceGpu> 474 ; m : Option<PushMat> 475 ; d : Option<DenseQ8> 476 ; q4 : Option<DenseQ4> 478 ; bias : Option<Vec<f32>> 479.
Vue4 — model.rs:691 — `#[derive(Clone, Copy)]` — vue sur tenseur quantifié découpable par expert :
  base : *const u8 692 ; n_out : usize 693 ; n_in : usize 694 ; nb : usize 695 ; src : crate::list::Source 696. `unsafe impl Sync` 818.
Moe — model.rs:821 — mélange d'experts :
  routeur : Vec<f32> 823 ; routeur_biais : Option<Vec<f32>> 826 ; biais_gate 829 / biais_up 830 / biais_down 831 : Option<Vec<f32>> ; n_ff : usize 832 ; gate/up/down : Vec<Vue4> 836-838 (une vue par fichier porteur) ; couche : usize 840 ; numeros : Vec<usize> 845 (numéro de cluster de chaque vue) ; n_expert_global : usize 847 ; local : Option<&'static clusters::Mapping> 849 ; shexp : Option<(Vue4,Vue4,Vue4)> 851 (expert partagé) ; tid2eid : Option<Vec<i32>> 856 (table de routage par jeton).
Layer — model.rs:879 : attn_norm 880 ; wq 881 ; wk 882 ; wv 883 ; wo 884 ; ffn_norm 885 ; q_norm 888 / k_norm 889 : Option<Vec<f32>> (RMSNorm par tête) ; sinks : Option<Vec<f32>> 894 (puits appris) ; wgate 895 ; wup 896 ; wdown 897 ; moe : Option<Moe> 900.
Stats — model.rs:903 : events : u64 904 ; prompt_s : f64 905 ; gen_s : f64 906 ; n_prompt : usize 907 ; n_gen : usize 908.
CacheExperts — model.rs:1072 — cache VRAM des experts MoE : cartes : HashMap<(usize,usize),(MatriceGpu,MatriceGpu,MatriceGpu,u64)> 1074 (privé) ; octets 1077 ; budget 1078 ; demandes 1079 ; manques 1080 ; evictions 1081 ; octets_envoyes 1082 ; ticks 1083 (privé).
Mla4 — model.rs:1149 — attention V4 (MLA compressée) : q_a 1150 ; q_a_norm 1151 ; q_b 1152 ; kv 1153 ; kv_norm 1154 ; wo_a 1155 ; wo_b 1156 ; sinks 1157 ; nh 1158 ; h 1159 ; head_dim 1160 ; rope 1161 ; n_groups 1162 ; o_lora 1163 ; rope_base 1164 ; eps 1165 ; ratio : usize 1169 (0 brute / 128 HCA / 4 CSA) ; rope_base_compresse : f32 1174 (160 000 V4-Flash) ; fenetre : usize 1177 ; indexer_top_k : usize 1183 (512 V4-Flash) ; a_indexeur : bool 1185 ; idx_q_b 1190 ; idx_proj 1191 ; idx_comp_kv 1192 ; idx_comp_gate 1193 ; idx_comp_ape 1194 ; idx_comp_norm 1195 ; idx_nh : usize 1197 ; idx_hd : usize 1199 (128) ; comp_kv 1203 ; comp_gate 1204 ; comp_ape 1205 ; comp_norm 1206.
EtatV4<'a> — model.rs:1214 — quatre tampons du chemin d'attention V4 : cles 1215 ; comp_kv 1216 ; comp_gate 1217 ; cles_comp 1218 ; idx_kv 1220 ; idx_gate 1221 ; idx_cles 1222 ; idx_scores 1224 (tous `&'a mut Vec<f32>`).
Hc — model.rs:1246 — hyper-connexions V4 : melange 1248 (`hc_fn`, [hc_mix × hc·h]) ; base 1250 (`[2·hc+hc²]`) ; scale 1252 (`[3]`) ; hc : usize 1253 ; h : usize 1254 ; iters : usize 1256 (Sinkhorn, 20 V4.1) ; eps : f32 1258 (1e-6).
HcSortie — model.rs:1263 : pre : Vec<f32> 1264 [hc] ; post : Vec<f32> 1265 [hc] ; comb : Vec<f32> 1266 [hc·hc].
Mla — model.rs:1407 — MLA latente : q_a 1408 ; q_a_norm 1409 ; q_b 1410 ; kv_a 1411 ; kv_a_norm 1412 ; kv_b 1416 (disposition combinée) ; k_b 1419 / v_b 1420 : Option<Vec<f32>> (disposition séparée Kimi/V3/V4) ; wo 1421 ; ffn_norm 1422 ; gate 1423 ; up 1424 ; down 1425 ; attn_norm 1426 ; q_lora/kv_lora/qkr/qkn 1427 ; vd/nh/ffn 1428 ; eps : f32 1433.
TraceFlux — model.rs:1482 — trace du flux d'activation : version : u16 1486 (2 = écarts+i16 sans perte ; 3 = `DRAVE_TRACE_BLOCS` i8 + échelle f16 par bloc de 32) ; bloc : usize 1488 ; fichier : BufWriter<File> 1489 ; couches : Vec<usize> 1491 ; octets : u64 1492 ; enregistrements : u64 1493 ; actifs : u64 1494.
FluxRelecteur — model.rs:1620 : listes : HashMap<(u16,u32),(f32,Vec<(u32,i16)>)> 1625 (v1/v2) ; listes_blocs : HashMap<(u16,u32),Vec<(u32,f32)>> 1630 (v3) ; servies : u64 1631 ; manquantes : u64 1632.
Model — model.rs:1755 — le modèle complet :
  g : Gguf 1756 ; cfg : Cfg 1757 ; layers : Vec<Layer> 1758 ; out_norm : Vec<f32> 1759 ; pool : Pool 1760 (type de engine.rs) ; kv : Vec<KvCache> 1765 ; ctx : usize 1766 ; events : u64 1767 ; paires : [u64;3] 1780 (0 attention, 1 experts routés, 2 partagé) ; act_levels : f32 1784 (127 int8 / 32767 int16) ; act_thresh : f32 1791 ; act_topk : usize 1792 ; act_renorm : bool 1796 ; act_topk_proj : [usize;7] 1799 (0 q,1 k,2 v,3 o,4 gate,5 up,6 down) ; attn_topk : usize 1804 ; attn_events : u64 1807 ; qk_topk : usize 1812 ; moe_topk : usize 1818 ; profil_neurones : Option<(Vec<u64>,Vec<f64>)> 1824 ; profil_experts : Option<Vec<u64>> 1828 ; profil_jetons : u64 1829 ; trace_experts : Option<BufWriter<File>> 1834 (`DRAVE_TRACE_EXPERTS=chemin`) ; attn_window : usize 1835 ; swa_pattern : usize 1842 ; attn_sinks : usize 1843 ; seuil_push : f32 1849 (croisement push/pull 22 %) ; stop_id : Option<u32> 1851 ; stop_id2 : Option<u32> 1854 ; prof : [f64;6] 1856 ; tete : String 1862 ("output.weight" sinon "token_embd.weight") ; sinks_vus : usize 1864 ; normes_tete : Option<Vec<f32>> 1873 ; ordre_normes : Option<Vec<u32>> 1874 ; tete_garantie : Option<Vec<u32>> 1876 ; tete_calculees : u64 1878 ; tete_appels_g : u64 1879 ; tete_gpu : Option<MatriceGpu> 1883 ; head4 : Option<DenseQ4> 1887 ; tete_restreinte : Option<Vec<u32>> 1901 ; tete_gpu_q6k : bool 1906 ; kv_gpu : Option<Vec<(usize, KvGpu)>> 1910 ; attn_gpu_part : Vec<f32> 1912 ; jeton_trace : u64 1917 ; trace : Option<TraceFlux> 1919 ; flux_force : Option<FluxRelecteur> 1923 ; emb_imposee : Option<Vec<f32>> 1928 ; emb_imposee_lot : Option<Vec<f32>> 1935 ; couche_debut/couche_fin : usize 1938-1939 ; flux_brut : bool 1947 ; mla : Option<Vec<Mla>> 1949 ; etat_entree : Option<String> 1957 (`DRAVE_ETAT_ENTREE`, format REFD) ; dump_couches : Option<String> 1962 (`DRAVE_DUMP_COUCHES`) ; mla4 : Option<Vec<Mla4>> 1965 ; mla4_cache : Vec<Vec<f32>> 1968 ; mla4_comp_kv 1971 / mla4_comp_gate 1972 / mla4_cles_comp 1976 : Vec<Vec<f32>> ; clamp_exp 1980 / clamp_shexp 1981 : Vec<f32> ; mla4_idx_kv 1983 / mla4_idx_gate 1984 / mla4_idx_cles 1985 / mla4_idx_scores 1988 : Vec<Vec<f32>> ; hc : Option<Vec<(Hc,Hc)>> 1991 ; hc_tete : Option<Hc> 1994 ; mla_cache : Vec<(Vec<f32>,Vec<f32>)> 1996 ; cache_experts : Option<CacheExperts> 1998 ; lot : usize 2002 ; patch : Option<Patch> 2004 ; ffn_gain : Option<(usize,f32)> 2007 ; hebb : Option<Hebb> 2011.
Patch — model.rs:2025 — greffon : layer : usize 2026 ; u : Vec<f32> 2027 ; v : Vec<f32> 2028 ; d : Vec<f32> 2029.
Hebb — model.rs:2053 — trace hebbienne : layer : usize 2054 ; quantile : f32 2055 ; n_out 2056 / n_in 2057 ; h : Vec<f32> 2058 ; n_fire : u64 2059 ; n_token : u64 2060 ; log : Vec<f32> 2063 ; log_on : bool 2064.
KvCache — model.rs:2106 — cache KV d'une couche :
  bits : u32 2107 (32 f32 défaut, 8 i8, 4 int4) ; n_kv : usize 2108 ; ctx : usize 2110 (longueur logique) ; f16_avant : bool 2112 (`DRAVE_KV_F16`) ; k_f32 : bool 2117 (`DRAVE_KV_K_F32`) ; v_f32 : bool 2118 (`DRAVE_KV_V_F32`) ; cap : usize 2122 (positions allouées, doublées) ; hd : usize 2123 ; kf 2124 / vf 2125 : Vec<f32> (privés) ; kp : Vec<u16> 2132 (privé, clés f16) ; k_f16 : bool 2133 (`DRAVE_KV_K_F16`) ; kq 2136 / vq 2137 : Vec<u8> (privés, quantifiés 8 bits, deux nibbles par octet en 4 bits) ; sk 2141 / sv 2142 : Vec<f32> (privés, échelles par bloc de 32 comme Q8_0) ; nb : usize 2143.

--- VARIABLES D'ENVIRONNEMENT (28 noms distincts sur les 7 fichiers ; tous les DRAVE_ de model.rs) ---
"DRAVE_Q8_BLOCS" — model.rs:960 — `is_ok()` => une échelle int8 par bloc de 32 (disposition Q8_0) au lieu d'une par ligne.
"DRAVE_SANS_EMPRUNT" — model.rs:1021 et 1028 — `is_err()` => emprunt autorisé si `keep >= 1.0` (sinon copie).
"DRAVE_TRACE_BLOCS" — model.rs:1507 — `is_ok()` => version 3 de la trace DRVF (i8 + échelle f16 par bloc de 32, ~22 % plus petit, avec perte).
"DRAVE_KV_K_F32" — 2153 — garde les CLÉS du cache KV en f32 (supprime l'erreur passant par les scores).
"DRAVE_KV_V_F32" — 2154 — garde les VALEURS en f32.
"DRAVE_KV_K_F16" — 2155 — clés stockées en f16 (2 octets/valeur, précision relative 2⁻¹¹) si `bits < 32`.
"DRAVE_KV_F16" — 2157 — arrondir clés ET valeurs en f16 avant quantification (`f16_avant`).
"DRAVE_YARN_MSCALE" — 2565 — `v != "0"` active le mscale YaRN ; sinon retombe sur `DRAVE_YARN`.
"DRAVE_YARN" — 2566 et 2570 — force YaRN partout (`toujours`).
"DRAVE_YARN_NON" — 2571 — désactive YaRN (`jamais`).
"DRAVE_KV_BITS" — 2940 — quantification du KV : parse u32 (8, 4, 32…).
"DRAVE_GPU_TETE" — 3066 — déporte la tête de sortie sur GPU.
"DRAVE_GPU_KV" — 3088 — miroir VRAM du cache KV.
"DRAVE_GPU_TOPK" — 3123 et 5512 — chaîne top-k déportée ; désactivée si `"0"` ou vide ; active aussi le noyau 4 si `SEUIL_NOYAU4` non dépassé (5535).
"DRAVE_GPU_EXPERTS" — 3151 — cache VRAM des experts MoE.
"DRAVE_GPU_EXPERTS_GO" — 3162 — budget en Go du cache d'experts (parse f64).
"DRAVE_TRACE_EXPERTS" — 3204 — chemin de la trace de routage (une ligne par (couche, jeton)).
"DRAVE_ETAT_ENTREE" — 3222 — fichier d'état d'entrée REFD (résidu du premier jeton lu du disque).
"DRAVE_DUMP_COUCHES" — 3223 — préfixe de vidage des états de couche (`<préfixe>-<couche>.bin`).
"DRAVE_YARN_RAMPE" — 3799 — `v == "0"` désactive la rampe YaRN.
"DRAVE_DEBUG_MLA" — 4512 et 5182 — traces de débogage MLA (`pos < 2` pour 4512).
"DRAVE_DEBUG_ETAT" — 5181 — traces de débogage d'état.
"DRAVE_FLUX_VERIF" — 5302 — vérification du flux.
(+ hors model.rs : "DRAVE_CLUSTERS" clusters.rs:168 ; "DRAVE_PRELIRE_TOUT" gguf.rs:91 ; "DRAVE_PRELIRE" gguf.rs:95 ; "DRAVE_MMAP" gguf.rs:156 ; "DRAVE_GPU" gpu.rs:1540/1565.)

--- LITTÉRAUX DE MODE/FORMAT COMPARÉS ---
"softmax" / "sigmoid" / "sqrtsoftplus" — model.rs:279-281 — `match v.as_str()` sur `scoring_func` du JSON => Gating.
"gpt-oss" — 288 (arch => défaut SoftmaxPoids), 2514 (`ffn_act_oss`), 3016 (motif SWA = 2 si fenêtre > 0).
"expert_gating_func" — 285 ; "JSON scoring_func" — 287 ; "défaut du moteur" — 289 — valeur du champ `Routage::source`.
"expert_count" / "n_routed_experts" — 264 ; "expert_used_count" / "num_experts_per_tok" — 268 ; "expert_feed_forward_length" / "moe_intermediate_size" — 272 ; "expert_gating_func" — 276 ; "expert_weights_norm" / "norm_topk_prob" — 296 ; "expert_weights_scale" / "routed_scaling_factor" — 300 ; "hash_layer_count" — 304 (routage du modèle).
"general.architecture" — 194, 257, 2484, 2513, 2518, 3012.
"attention.indexer.top_k" / "index_topk" / "indexer.top_k" — 111 ; "engram_embd.weight"/"engram.weight"/"engram.layer_ids"/"engram_layer_ids" — 123-124 ; "attn_output_a.weight"/"attn_kv.weight" — 132 ; "attn_derope" — 151 ; "attention.compress_ratios"/"compress_ratios" — 164 ; "attn_compressor_kv.weight" — 166 ; "attn_q_a.weight"/"attn_kv_a_mqa.weight" — 172 ; "hc_attn_fn.weight" — 99 ; "indexer." — 106.
Suffixes de tenseurs (préfixe `blk.{l}.`) — 508, 602-604, 621, 632-634, 652-658, 670-673, 720, 2877-2919 : "ffn_gate_exps.weight", "ffn_up_exps.weight", "ffn_down_exps.weight", "ffn_gate_inp.weight", "ffn_gate_shexp.weight", "exp_probs_b.bias", "ffn_gate_inp.bias", "ffn_gate_tid2eid.weight", "attn_norm.weight", "attn_q.weight", "attn_k.weight", "attn_v.weight", "attn_output.weight", "ffn_norm.weight", "post_attention_norm.weight", "attn_q_norm.weight", "attn_k_norm.weight", "attn_sinks.weight", "ffn_gate.weight", "ffn_up.weight", "ffn_down.weight".
"token_embd.weight" — 4008, 5060, 5156, 5212 ; "output_norm.weight" — 2928 ; "output.weight" / "token_embd.weight" — 3003 (choix de `Model::tete`).
MLA/V4 : "blk.0.attn_kv_a_mqa.weight" — 2642 ; "attn_q_a.weight" 2650/2677/2713/2758 ; "attn_q_b.weight" 2651/2760 ; "attn_kv_b.weight" 2664 ; "attn_k_b.weight" 2669 ; "attn_v_b.weight" 2670 ; "attn_q_a_norm.weight" 2678/2759 ; "attn_kv_a_norm.weight" 2681/2762 ; "attn_output.weight" 2683 ; "blk.0.attn_kv.weight" — 2704 ; "attn_output_a.weight"/"attn_output_b.weight" 2763-2764 ; "attn_kv.weight" 2761 ; "attn_sinks.weight" 2765 ; "attn_compressor_kv/gate/ape/norm.weight" 2741-2744 ; "indexer.proj.weight" 2749/2751 ; "indexer.attn_q_b.weight" 2750 ; "indexer_compressor_*.weight" 2752-2755 ; "blk.0.hc_attn_fn.weight" — 2822 ; "{nom}_fn/_base/_scale.weight" 2829-2831 ; "hc_attn"/"hc_ffn" 2834 ; "output_hc_fn/base/scale.weight" 2846-2850 ; "hc_head_fn/base/scale.weight" 2853-2857.
Clés de config lues : "rope.dimension_count" 2519/2652/2711 ; "rope.scaling.type" 2549 (`"yarn"` 2550) ; "rope.scaling.factor" 2551/3033 ; "rope.scaling.yarn_beta_fast" 2552 ; "rope.scaling.yarn_beta_slow" 2553 ; "rope.scaling.original_context_length" 2554/3032 ; "swiglu_clamp_exp" 2635 ; "swiglu_clamp_shexp" 2637 ; "attention.sliding_window" 2729/3007 ; "attention.sliding_window_pattern" 3013 ; "attention.compress_rope_freq_base"/"compress_rope_freq_base" 2725 ; "compress_rope_theta" 2727 ; "attention.key_length" 2506/2709 ; "attention.q_lora_rank" 2712 ; "attention.output_group_count" 2714 ; "attention.output_lora_rank" 2715 ; "attention.indexer.head_count" 2756 ; "attention.indexer.key_length" 2757 ; "attention.layer_norm_rms_epsilon" 2499 ; "block_count"/"num_hidden_layers" 2489 ; "embedding_length"/"hidden_size" 2491 ; "attention.head_count"/"num_attention_heads" 2493 ; "attention.head_count_kv"/"num_key_value_heads" 2495 ; "feed_forward_length"/"intermediate_size" 2497 ; "rope.freq_base"/"rope_theta" 2500/2720 ; "expert_count" 2508 ; "expert_used_count" 2509 ; "expert_feed_forward_length" 2510 ; JSON : "n_routed_experts" 266, "num_experts_per_tok" 270, "moe_intermediate_size" 274, "scoring_func" 278, "norm_topk_prob" 298, "routed_scaling_factor" 302, "rope_theta" 2722, "compress_rope_theta" 2727, "sliding_window" 2731.
Formats binaires : b"DRVF" (magie trace) — 1502 écriture, 1644 relecture ; versions acceptées 1, 2, 3 — 1649 ; b"QPAT" (magie patch) — 2037 (format documenté l.2024 : magie | version u32 | couche u32 | n u32 | n f32 u | n f32 v | n f32 d) ; b"REFD" (états llama.cpp) — 3841 ; en-tête DRVF = magie(4) + version(2) + n_layer(4) + hidden(4) = 14 octets — 1639/1642.
Vidages de couches (`vider_couche`) : "qr" 4691, "qr_norm" 4694, "q_norm" 4706, "kv_norm" 4730, "q_rope" 4731, "kv_rope" 4732, "comp_state_kv" 4747, "comp_state_gate" 4749, "comp_brut{bloc}" 4806, "comp_bloc{bloc}" 4818, "idx_scores" 4924, "attn_brut" 5008, "attn_derope" 5037, "attn_out" 5043, "hc_attn_pre" 5295, "l_last" 5890/5939.
Divers : "yarn " 2982 ; "activation-oss " 2983 ; "routage-table " 2986 ; "moe " 2987 ; "Q6_K"/"Q8_0" 3080 ; "aucun"/"par tête" 2777 ; "softmax"/"sigmoïde"/"top-k brut + softmax"/"racine de softplus" 59-62 ; "attentions compressées" 2616 ; "avx2"/"fma" 5255 (`is_x86_feature_detected!`) ; "projection dense requise" 4266/4271/4414 ; "projection sans format" 3379 ; "lot non vide" 6428 ; "largeur {} non multiple de 256" 720 ; "expert de type {} : activation de {} valeurs…" 725.
Chemins de test : "drave_noeud_partiel" 6627, "drave_mapping_etranger" 6693, "commun.gguf" 6636/6699, "cluster-00.gguf" 6705, "mapping.tsv" 6649/6708.

--- TABLES DE CORRESPONDANCE type→source/taille DANS model.rs ---
`source_de(t: u32) -> Option<crate::list::Source>` — model.rs:483-498 : GGML_Q4_K => Source::Q4_K (488) ; GGML_Q6_K => Source::Q6_K (489) ; GGML_MXFP4 => Source::Mxfp4 (490) ; GGML_Q4_0 => Source::Q4_0 (491) ; `_ if crate::list::sans_noyau(t) => Source::Dequant(t)` (495 — super-blocs de 256 sans noyau, déquantifiés puis f32) ; `_ => None` (496, avec message l.565-566 « format sans noyau ni déquantification »).
`Vue4::pas()` — model.rs:700-710 : Q4_K => TAILLE_Q4K (144), Q6_K => TAILLE_Q6K (210), Mxfp4 => 17, Q4_0 => 18, Propre => 0, Dequant(t) => list::octets_grille(t).
`bloc = if ttype == GGML_Q4_K || GGML_Q6_K { 256 } else { 32 }` — model.rs:570 et 598 (taille de super-bloc pour les vues d'experts).
Tailles+fonctions de déquantification (experts routés) — model.rs:1349-1358 (Q2_K 84, Q3_K 110, Q5_K TAILLE_Q5K, IQ2_XXS 66, IQ3_XXS 98, IQ1_S 50, IQ4_XS 136, IQ1_M 56) et identique en 1774-1782 (`dequant`).
`raw_levels`-like : model.rs:1008 et 1119-1121 (mxfp4_blocks) ; 3051 et 3177 (choix tête Q8_0 / MXFP4).
Activation gpt-oss : LIMITE 7.0 / ALPHA 1.702 — 3652-3653.
Tanh-approx / GELU : `sqrt_softplus` — 312-315 (seuil x > 20).

--- FONCTIONS PUBLIQUES (identifiants exposés) ---
manques_architecture 87 ; dim_gguf 226 ; reel_gguf 231 ; routage_du_gguf 256 ; sinkhorn 1281 ; f16_depuis_f32 1450 ; f32_depuis_f16 1463 ; Gating::du_numero 46 / nom 57 ; Moe::ou 864 ; Proj::vide 970 ; CacheExperts::nouveau 1087 / taux 1092 ; Hc::hc_mix 1313 / melanges 1316 / sortie 1331 / tete 1358 / melanger 1375 / retro 1387 ; TraceFlux::nouveau 1498 / ecrire 1524 / terminer 1609 ; FluxRelecteur::lire 1636 / appliquer 1732 ; Patch::load 2033 ; Hebb::new 2068 ; KvCache::new 2147 / assurer 2169 / octets 2241 / ecrire 2261 / vers_gpu_tranche 2337 / vers_gpu 2358 / miroir_gpu 2365 / cle 2377 / valeur 2409 ; Model::load 2474 / load_partiel 2480 / topk_de 3242 / cfg_yarn_off 3490 / activer_profil_neurones 3493 / rapport_neurones 3538 / ecrire_neurones 3626 / dot8 3680 / forward_lot 3943 / forward_mla 5054 / logits_f32 5151 / forward 5165 / logits_lot 5971 / flux_en_liste 6100 / flux_en_liste_blocs 6131 / norme_finale 6163 / logits 6171 / preparer_normes_tete 6274 / logits_garanti 6333 / generate 6392 / events_total 6489 / reset_events 6490.

=====================================================================
FICHIER 7/7 : drave-core/src/tokenizer.rs (507 l.)
=====================================================================

--- ENUMS ---
(aucun)

--- CONSTANTES ---
SEP — tokenizer.rs:28 — `const SEP: char = '\u{1}'` — séparateur interne des clés de fusion BPE (`a` + SEP + `b`) ; U+0001 ne peut jamais apparaître dans un symbole byte-level.

--- STRUCTS PUBLIQUES ET CHAMPS (description tokenizer) ---
Tokenizer — tokenizer.rs:30 — champs tous PRIVÉS (struct pub, pas de champ pub) :
  id_to_tok : Vec<String> — 32 — vocabulaire, l'indice est l'id du token.
  tok_to_id : HashMap<String, u32> — 34 — token brut GGUF → id (dernière occurrence gagnante).
  ranks : HashMap<String, u32> — 36 — (a,b) → rang de fusion, clé = `a` + SEP + `b`.
  byte_enc : [char; 256] — 38 — table byte-level GPT-2/Qwen (octet → caractère).
  byte_dec : HashMap<char, u8> — 40 — inverse, pour le décodage.
  token_type : Vec<i32> — 43 — types GGUF des tokens (1 = normal, 3 = contrôle, 4 = défini par l'utilisateur, 5 = inutilisé), utilisés par `special_id`.
  motif_gpt4o : bool — 46 — motif de pré-découpage o200k (`tokenizer.ggml.pre`) ; vrai pour « gpt-4o »/« o200k », sinon Qwen2.

--- ENVIRONNEMENT ---
(aucun)

--- LITTÉRAUX DE MODE/FORMAT COMPARÉS ---
"gpt-4o" — tokenizer.rs:77 — `pre.starts_with("gpt-4o")` => pré-tokenizer o200k.
"o200k" — tokenizer.rs:77 — `pre.starts_with("o200k")` => idem.
"qwen2" — mentionné en doc 6/44-45 comme motif par défaut (les autres motifs retombent sur qwen2) ; pas de comparaison runtime.
" " (espace) — 63 — coupure du merge au PREMIER espace ; `""` — 65 — second symbole vide si pas d'espace.
Types de tokens : 3 (contrôle) et 4 (défini par l'utilisateur) — 130-131, 144 (`t != 3 && t != 4`).
Motifs regex documentés (spécification, pas des littéraux comparés) : Qwen2 — 6-8 et 231 ; o200k — 278-280 ; contractions `'s|'t|'re|'ve|'m|'ll|'d` — 371-397 ; plages byte-level U+0021..U+007E, U+00A1..U+00AC, U+00AE..U+00FF — 182-199 ; `\r`, `\n`, `'/'` — 367.

--- FONCTIONS PUBLIQUES (identifiants exposés) ---
Tokenizer::new(tokens: Vec<String>, merges: Vec<String>, token_type: Vec<i32>, pre: &str) -> Self — 55 ; encode(&self, text: &str) -> Vec<u32> — 83 ; decode(&self, ids: &[u32]) -> String — 107 ; vocab_size(&self) -> usize — 124 ; special_id(&self, text: &str) -> Option<u32> — 141.
Privées : bpe 155 ; bytes_to_unicode 186 ; is_letter 216 ; is_number 221 ; is_space 226 ; next_piece 238 ; is_majuscule 262 ; is_minuscule 268 ; prefixe_possible 273 ; next_piece_gpt4o 285 ; avec_contraction 297 ; match_casse_decroissante 310 ; match_casse_croissante 332 ; match_nombre_trois 348 ; match_ponctuation_gpt4o 357 ; match_contraction 372 ; match_letters 405 ; match_number 427 ; match_punctuation 438 ; match_line_breaks 457 ; match_spaces_before_word 480 ; match_spaces 496.

=====================================================================
NOTES DE PORTÉE (à ne pas confondre avec des identifiants de ces 7 fichiers)
- Aucun enum de quantification (Q4_K, MXFP4, IQ2_XXS…) n'existe dans ces fichiers : ce sont les constantes `GGML_*` (gguf.rs:258-318) + les matchs gguf.rs:761-778 / 783-795 / 1349-1358 / 1447-1454.
- `crate::list::{Source, Source8, DenseQ8, DenseQ4, PushMat, sans_noyau, octets_grille, dequant_grille_dans}` (list.rs) et `crate::engine::Pool` (engine.rs) sont HORS des 7 fichiers mais référencés par model.rs (Vue4::src, Proj::m/d/q4, Model::pool).
- Aucun `env!`/`option_env!` dans les 7 fichiers ; uniquement `std::env::var`, 28 noms distincts, tous préfixés DRAVE_. Aucune variable CUDA_* lue par `env::var` (seule la lib « cuda » est liée, gpu.rs:16).
- Aucune modification de fichier effectuée (lecture seule).

### 👤 Utilisateur

Background subagent 18b8879c-f211-43b8-9908-cf65e509b21d finished and will do no further work unless you send it more.
Its closing message:
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

### 🤖 Assistant

⏵ Vérification des derniers termes (porte de correction, greffon, AER) avant rédaction

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'porte de correction' docs/*.md | head -5; echo \"=== greffon ===\"; grep -rn 'greffon' docs/*.md drave-core/src/*.rs REPRISE.md 2>/dev/null | head -6; echo \"=== E8M0/E2M1 ===\"; grep -rn 'E8M0\\|E2M1' drave-core/src/*.rs | … [69 caractères tronqués]`

  ```
docs/glossaire.md:176:« La conformité à llama.cpp est une porte de correction, pas le but : le but est de
docs/glossaire.md:180:**Porte Drave** — Épreuve propre au projet, opposée à la porte de correction :
docs/plan-deepseek41-complet.md:9:là-dessus : la conformité à llama.cpp devient une *porte de correction*, pas le but.
docs/plan-deepseek41-complet.md:136:- **porte de correction** — la comparaison à llama.cpp sur **V4-Flash**, étage par
=== greffon ===
docs/glossaire.md:475:cette porte : `a = SiLU(u·x) · (v·x)`, puis `a·d` (`reports/rapport-greffon.md:12-15`).
docs/glossaire.md:476:**Où** : MLP de Qwen2, tour ViT (`clip.use_silu`), greffon `--patch`.
docs/glossaire.md:682:**QPAT** — Format du « greffon » : un en-tête `QPAT | version | couche | n | u[n] |
docs/glossaire.md:684:`tools/make_patch.py`, `--patch` (`reports/rapport-greffon.md:19`).
docs/glossaire.md:803:(`reports/rapport-greffon.md:12-42`, `docs/programme-recherche.md:143-152`).
docs/glossaire.md:890:| `tools/make_patch.py` | fabrique un greffon `QPAT` pour `--patch` | `reports/rapport-greffon.md:70` |
=== E8M0/E2M1 ===
drave-core/src/gguf.rs:1065:    /// E8M0 puis 16 octets de nibbles E2M1, moitié basse puis moitié 
… [427 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l docs/glossaire.md && grep -n '^\\*\\*' docs/glossaire.md | head -100", "description": "List glossary entries"}`

  ```
924 docs/glossaire.md
13:**Ce que contient une entrée.** Chaque entrée suit le même patron :
20:**Conventions de lecture.**
33:**Ce que ce document n'est pas.** Ce n'est ni un tutoriel d'inférence, ni un
38:**Périmètre.** `docs/` (18 documents) et `reports/` (60 rapports) ; les 9 fichiers
49:**Si tu ne lis qu'un document, lis `docs/vision.md`** (279 lignes) : c'est la
94:**A/B (écart A/B)** — Comparaison de deux exécutions ne différant que par un
100:**Banc (bench)** — Dispositif de mesure isolé qui fait tourner une seule partie du
106:**Boxing** — Règle des sprints : 2 h chronométrées, on s'arrête quand la boîte est
110:**CDC** *(polysémie)* — Dans le corpus, **deux sens** :
119:**Créneau long** — Unité de travail de 3 h, entre le sprint (2 h) et la journée
122:**Definition of done (engagement de fin de sprint)** — Liste non négociable pour
127:**Drave** — Nom du projet depuis le 30/09/2026 : *stream of logs*, « le flux des
133:**Écart (0,00e0)** — Différence entre le résultat d'une exécution locale et celui
138:**Fait · mesuré · projeté · déduit** — Étiquettes de confiance du dépôt. *Mesuré* :
143:**Harnais (harness)** — Petit montage de test autonome, souvent en Python, qui
149:
… [7050 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '^\\*\\*' docs/glossaire.md | sed -n '100,200p'", "description": "List rest of glossary entries"}`

  ```
535:**Réf.** : Peng et al., *YaRN*, [arXiv:2309.00071](https://arxiv.org/abs/2309.00071).
541:**b/poids (bits par poids)** — Nombre moyen de bits nécessaires pour stocker un
548:**BitNet b1.58** — Famille de modèles **entraînés** en ternaire (−1, 0, +1), et non
552:**Réf.** : Ma et al., *The Era of 1-bit LLMs*, [arXiv:2402.17764](https://arxiv.org/abs/2402.17764).
554:**Bloc de quantification · échelle par bloc** — Les poids quantifiés sont rangés
560:**Réf.** : Frantar et al., *GPTQ*, [arXiv:2210.17323](https://arxiv.org/abs/2210.17323).
562:**Dequantification (déquantification)** — Recalcul de la valeur réelle d'un poids à
568:**E2M1 · E8M0** — Les deux composants du format MXFP4 : **E2M1** est la valeur sur
573:**Réf.** : *Microscaling Data Formats for Deep Learning*,
576:**Échappement · indices par écarts** — Une liste d'indices triés se comprime en
583:**Entropie · Huffman · inégalité de Kraft** — L'*entropie* d'une source est le
592:**GGUF (GPT-Generated Unified Format)** — Format de fichier des modèles : un
599:**ggml · type ggml · `ggml_blck_size` · `ggml_type_size`** — ggml est la
608:**I8 · I32** — Types entiers signés du GGUF, distincts des types quantifiés. V4.1
610:**a
… [4410 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 22 % ===\"; grep -rn '22 %\\|0,22\\|22%' tools/*.py drave-core/src/*.rs docs/glossaire.md | head -8; echo \"=== glossaire 9 sprints ===\"; sed -n '36,40p' docs/glossaire.md; echo \"=== harmony paths ===\"; sed -n '15,22p'  … [77 caractères tronqués]`

  ```
=== 22 % ===
tools/analyse_flux.py:8:  croisement mesuré est à ~22 % de densité) — mais elle se prend PAR COUCHE, pas
drave-core/src/model.rs:984:        // scalaire dense (pull). Le croisement mesuré est à 22 %
drave-core/src/model.rs:1485:    /// canaux, ~22 % plus petit, avec perte).
drave-core/src/model.rs:1505:        // f16 par bloc de 32 canaux (l'étude de compacité annonce −22 % de plus,
drave-core/src/model.rs:1779:    /// push/pull de 22 % arbitre (`reports/rapport-croisement-push-pull.md`).
drave-core/src/model.rs:1845:    /// deux architectures se croisent à **22 %** de densité
drave-core/src/model.rs:1847:    /// 0,22 après la mesure) ; on bascule un peu au-dessus pour absorber la
drave-core/src/model.rs:5531:                        // 0,13 contre 0,22 ms à 4 k clés, 0,85 contre 0,89 à 131 k —
=== glossaire 9 sprints ===
avec `fichier:ligne` et citation, sans être modifiés.

**Périmètre.** `docs/` (18 documents) et `reports/` (60 rapports) ; les 9 fichiers
de `sprints/` sont couverts pour leur vocabulaire propre (boxing, cérémonie,
porte). Le code est cité pour dire *où* un terme est utilisé (`drave-core/src/`,
=== harmony paths ===
import subprocess, sys, os

Q = "/ho
… [206 caractères tronqués]
  ```

- **bash** `{"command": "ls -d /home/stephane/Data13TB/stephane/GitHub/Drave 2>&1; ls /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf 2>&1 | head -2", "description": "Check hard-coded Drave path existence"}`

  ```
ls: cannot access '/home/stephane/Data13TB/stephane/GitHub/Drave': No such file or directory
/home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf
  ```

### 🤖 Assistant

⏵ Rédaction du livrable A–D et transmission au parent

- **send_message** `{"agent_id": "3d5618a0-4e3a-45bb-943d-a72c753fb7da", "message": "LIVRABLE — dépouillement exhaustif (9 sprints lus intégralement ; 24 outils Python + 8 scripts shell ; CLI/champs de drave-core/src/*.rs). Aucun fichier modifié.\n\n## A. Termes, sigles et drapeaux\n\n**Protocole de flux (DRVF)**\n- ** … [47624 caractères tronqués]`

  ```
message delivered to agent 3d5618a0-4e3a-45bb-943d-a72c753fb7da
  ```

### 🤖 Assistant

⏵ Livrable transmis au parent ; reproduction intégrale ci-dessous

## A. Termes, sigles et drapeaux

**Protocole de flux (DRVF)**
- **DRVF** — Format binaire de trace/échange d'activations : en-tête `"DRVF"` + u16 version + u32 n_layer + u32 hidden, listes (couche, position, n_actifs, échelle) et paires, sentinelle `0xFFFF` ; écrit par `model.rs:1502` (`b"DRVF"`), lu `model.rs:1644-1649`, spécifié `tools/flux_codec.py:16-31`, `tools/analyse_flux.py:24-33` ; terme de protocole/format.
- **DRVF v1 / v2 / v3** — Versions du fichier de trace : v1 paires `(u32 indice, i16 valeur)`, v2 écarts u8 + i16 (255 = indice absolu u16), v3 blocs i8 + échelle f16 par bloc de 32 (`DRAVE_TRACE_BLOCS`) ; `tools/flux_codec.py:28-36` (VERSION=2 écrit, lit 1/2/3), `model.rs:1507,1649` ; format.
- **DRVF v5** — Version du protocole de TRANSPORT TCP (≠ version du fichier) : en-tête de 79 octets, magie `0x44525631` (« DRV1 ») ; `main.rs:1893,1906,1941` (`MAGIE_FLUX`, `VERSION_FLUX=5`, `TAILLE_TETE`), `docs/format-flux.md:92-114` ; protocole.
- **mode 0 / MODE_DENSE** — Vecteur dense f32 (4 octets/canal) ; `main.rs:1908`, `tools/pair_factice.py:17` ; mode de protocole.
- **mode 1 / MODE_LISTE** — Liste creuse quantifiée : indice u16 + valeur i16 + une échelle (émis par `--flux-liste`) ; `main.rs:1912`, `tools/pair_factice.py:17` ; mode de protocole.
- **mode 2 / MODE_BLOCS** — Liste à échelle par bloc de 32 canaux : indice u16, valeur i8, échelle f32 par bloc (émis par `--flux-blocs`) ; `main.rs:1917`, `tools/pair_factice.py:18` ; mode de protocole.
- **mode 3 / MODE_LOT** — n états × hidden en f32 dense dans un seul flux (préremplissage réparti) ; `main.rs:1923`, `docs/format-flux.md:112` ; mode de protocole.
- **mode 4 / MODE_LOT_LISTES** — Lot d'états, chacun encodé comme le mode 2, auto-délimité ; `main.rs:1930` (« ≈1 530 octets/jeton, ÷2,3 »), `main.rs:2616-2622` ; mode de protocole.
- **TAILLE_TETE = 79** — Octets de l'en-tête de flux (règles d'activation comprises) ; `main.rs:1941`, `tools/pair_factice.py:15` ; constante.
- **PLAFOND_FLUX = 256 Mo** — Plafond d'allocation pilotée par le réseau (règle R4 de `docs/plan-prefill-reparti.md`) ; `main.rs:2002` ; constante.
- **Act** — Réglages d'activation voyageant dans chaque en-tête (levels, thresh, topk, renorm, topk_proj[7], attn/qk/moe top-k) ; `main.rs:1945-1978` ; structure de protocole.
- **pair / paire (indice, valeur)** — Unité de contenu d'une liste creuse, et « pair » = pair distant du protocole (`--ppl-reparti`) ; `tools/pair_factice.py:1-18`, `main.rs:2119` (`encoder_paires_blocs`) ; terme de protocole.
- **échappement (255)** — Écart de 255 annonçant un indice absolu sur u16 ; `main.rs:2114-2118`, `tools/trace_compacite.py:57` ; encodage.
- **shard** — Fragment d'un GGUF découpé (`…-00002-of-00003.gguf`) ; `gguf.rs:548` (`shard_de`), `gguf.rs:566` (`chemins_du_modele`), `gguf.rs:470` (`open_multi`) ; format/fichier.
- **commun.gguf / cluster-NN.gguf / mapping.tsv** — Trio du « modèle éclaté » : poids communs, un GGUF par cluster, table couche/ligne locale/expert global ; `clusters.rs:187,200,213`, `tools/convertir_clusters.py:341-348,417,449` ; format.

**Modèles, architectures, quantifications**
- **GGUF** — Format de fichier des modèles (magie `b"GGUF"`, version ≥ 2, alignement `general.alignment` défaut 32) ; `gguf.rs:827-830,880`, `docs/glossaire.md:592` ; format.
- **type ggml** — Identifiant u32 de format de tenseur (`GGML_Q4_K=12`, `GGML_MXFP4=39`…) + tables taille/nom ; `gguf.rs:258-318` (constantes), `gguf.rs:761-778` (37 types → (bloc, octets)), `gguf.rs:783-798` (42 noms) ; énumération par constantes (aucun enum Rust).
- **Q4_0 / Q4_1 / Q5_0 / Q5_1 / Q8_0 / Q8_1** — Types ggml « legacy » à blocs de 32 (18/20/22/24/34/36 octets) ; `gguf.rs:260,271,272,314,315`, `tools/convertir_clusters.py:42-48` ; quantification.
- **Q2_K / Q3_K / Q4_K / Q5_K / Q6_K / Q8_K (k-quants)** — Super-blocs de 256 poids (84/110/144/176/210/292 octets) ; `gguf.rs:262,264,265,273,274,295-299` (`TAILLE_Q4K=144`, `TAILLE_Q6K=210`, `TAILLE_Q5K=176`), `tools/verifier_formats.py:31-51` ; quantification.
- **Q4_K_M** — Variante « medium » de Q4_K, celle de `models/Qwen2.5-0.5B-Q4_K_M.gguf` ; `tools/aiguille.py:31` ; quantification.
- **MXFP4** — Virgule flottante 4 bits à échelle microscopique : bloc de 17 octets = exposant E8M0 + 16 octets de nibbles E2M1, bloc de 32 poids ; `gguf.rs:261,1065-1089`, `list.rs:547` (`LUT_MXFP4`), `docs/glossaire.md:635` ; quantification.
- **E2M1 / E8M0** — Composants de MXFP4 : valeur 4 bits (table `KV` à 16 niveaux) et échelle d'exposant ; `gguf.rs:1068,1079-1089` (`echelle_e8m0`), noyau `proj_mxfp4_warp` (`gpu.rs:259`) ; quantification.
- **IQ2_XXS / IQ1_M / IQ1_S / IQ2_S / IQ3_XXS / IQ4_NL / IQ4_XS** — Famille d'i-quants à grilles (256 poids ; 66/56/50/74/98/18/136 octets) ; `gguf.rs:278-287`, `formats.rs:19` (`IQ2XXS_GRID`), `formats.rs:447` (`IQ1S_GRID`), `formats.rs:2499` (`KVALS_IQ4NL`), `formats.rs:2504` (`IQ3XXS_GRID`) ; quantification.
- **TQ1_0 / TQ2_0 / NVFP4 / Q6_0 / Q1_0 …** — Types ggml 34,35,40,41-48 présents dans la table du moteur (tailles relevées par `tools/verifier_table_types.sh`) ; `gguf.rs:769,774-775`, `gguf.rs:783-798` ; quantification.
- **MoE** — Mélange d'experts : routeur top-k sur N experts ; `model.rs:821` (`Moe`), `docs/glossaire.md:380` ; architecture.
- **expert routé / expert partagé (shexp)** — Sous-réseaux choisis par le routeur / expert toujours actif ; `model.rs:851` (`shexp`), `model.rs:836-838` ; architecture.
- **grappe (cluster)** — Groupe d'experts (ou de neurones) traité comme unité de placement/disque ; `clusters.rs:26-34` (`Mapping`), `tools/clusters_moe.py:1`, `docs/glossaire.md:795` ; architecture/format.
- **nœud partiel** — Nœud qui ne charge que `commun.gguf` + certains clusters (`DRAVE_CLUSTERS`) ; `clusters.rs:161-172`, `sprints/08:151-155` ; mode d'exécution.
- **engram** — Table d'adresses creuse adressée par hachage de n-grammes (`blk.N.engram_embd.weight`, I8, `[384 006 168, 264]`) ; `model.rs:123`, `main.rs:697` (`--sonder-engram`), `sprints/09:19-22`, `docs/glossaire.md:275` ; terme d'architecture/fichier.
- **hyper-connexion (HC, hc_pre/hc_post/hc_head)** — L'état résiduel dupliqué en 4 copies avec mélanges appris normalisés par Sinkhorn ; `model.rs:1246-1266`, `tools/hc_synthetique.py:1-20`, `gguf.rs:933-938` ; architecture.
- **Sinkhorn** — Normalisation itérative lignes/colonnes (20 itérations, eps 1e-6 pour V4.1) ; `tools/hc_synthetique.py:19-20`, `gguf.rs:934,936`, `model.rs:1256-1258`, `docs/glossaire.md:481` ; algorithme.
- **MLA (Multi-head Latent Attention)** — Attention latente (q_lora/kv_lora, une tête KV latente) ; `model.rs:1407` (`Mla`), `tools/mla_synthetique.py:1`, `main.rs:613` (`--banc-mla`) ; architecture.
- **MQA / GQA** — Une seule tête KV (MLA = MQA) / requêtes groupées ; `tools/mla_synthetique.py:31` (`NKV=1`), `docs/glossaire.md:303,386` ; architecture.
- **CSA / HCA** — Régimes d'attention compressée de DeepSeek-V4 (ratio 4 « CSA », ratio 128 « HCA ») ; `model.rs:1169` (`ratio`), sortie `--config` `main.rs:1670-1734`, `docs/glossaire.md:261,310` ; architecture.
- **indexeur (lightning indexer)** — Petit réseau qui note des blocs de clés et n'en garde que `top_k` (512 sur V4-Flash) ; `model.rs:1183`, `model.rs:111` (`attention.indexer.top_k`), `docs/glossaire.md:322` ; architecture.
- **KV (cache clé-valeur)** — Mémoire des clés/valeurs déjà calculées ; `model.rs:2106` (`KvCache`), `gpu.rs:86` (`KvGpu`), `--ctx`/`DRAVE_KV_BITS` ; structure/terme.
- **puits d'attention (attention sinks)** — Clé virtuelle de valeur nulle, apprise, qui absorbe l'attention ; `model.rs:894` (`sinks`), `main.rs:661` (`--attn-sinks`), `sprints/02:51-59` ; architecture.
- **fenêtre glissante (SWA) / motif** — Attention limitée aux N dernières clés, motif par couche ; `main.rs:659-660` (`--attn-window`, `--swa-pattern`), `model.rs:1835-1842` ; architecture.
- **top-k** — Sélection des k plus grandes valeurs ; décliné en `--attn-topk`, `--qk-topk`, `--moe-topk`, `--topk-q/-k/-v/-o/-gate/-up/-down`, `--topk`, `--act-topk` ; `main.rs:647,658,662-663,668-675`, `docs/glossaire.md:514` ; drapeau/terme.
- **attention creuse** — Attention restreinte aux k meilleures clés par requête ; `sprints/03:56-68`, `model.rs` (top-k) ; concept.
- **k-WTA (k-Winners Take All)** — Parcimonie par sélection des k plus fortes activations ; `main.rs:668` (`--act-topk`), `docs/glossaire.md:339` ; concept.
- **perplexité (PPL)** — Exponentielle de la NLL moyenne par jeton ; mesure de référence de toutes les portes (`tools/portes.sh:53,60,121`), `main.rs:4277` (`run_ppl`) ; métrique.
- **NLL** — Log-vraisemblance négative par position ; `tools/compare_logits.py:34-40,93-99`, `main.rs:2595` (`nll_logits`) ; métrique.
- **RoPE** — Plongement positionnel rotatif (rotation par paires), y compris rotation inverse pour V4 ; `model.rs:3909-3912` (`rope_inverse`) ; architecture.
- **YaRN / mscale / rampe** — Extension de contexte par interpolation NTK avec facteur, betas et rampe ; `DRAVE_YARN`, `DRAVE_YARN_NON`, `DRAVE_YARN_MSCALE`, `DRAVE_YARN_RAMPE` (`model.rs:2565-2571,3799`), `main.rs:693` (`--sans-yarn`) ; architecture/drapeau.
- **RMSNorm** — Normalisation par la moyenne quadratique ; `model.rs:886-889` (par tête), `main.rs:2499` (`attention.layer_norm_rms_epsilon`) ; architecture.
- **SiLU / SwiGLU / GELU / sigmoïde rapide** — Non-linéarités du FFN : `x·σ(x)` ; `g·(u+1)·σ(1,702 g)` pour gpt-oss (clamp ±7) ; `model.rs:431-435`, `model.rs:3652-3653` (`LIMITE=7.0`, `ALPHA=1.702`), `model.rs:1977` (clamp SwiGLU V4) ; architecture.
- **routage / gating (Softmax, Sigmoid, SoftmaxPoids, SqrtSoftplus)** — Enum `Gating` à 4 conventions (Qwen3-MoE, Kimi/GLM, gpt-oss, DeepSeek V4) ; `model.rs:28-63`, sortie `--config` (`main.rs:96-99` : sigmoïde, racine de softplus, softmax) ; enum Rust.
- **tid2eid** — Table de routage par jeton `ffn_gate_tid2eid.weight` (I32, `GGML_I32=26`) ; `model.rs:856`, `gguf.rs:316-318` ; format.
- **LoRA (q_lora_rank / kv_lora_rank / o_lora)** — Projections de rang faible de la MLA (« descente » puis « montée ») ; `model.rs:1150-1163`, `tools/mla_synthetique.py:32-34` (`QL=32`, `KVL=48`), `docs/glossaire.md:359` ; architecture.
- **MTP (Multi-Token Prediction) et décodage spéculatif** — Prédiction de plusieurs jetons en avance (`dspark_*`, cibles 37-39) ; `docs/plan-deepseek41-complet.md:86`, `docs/glossaire.md:399` ; architecture (absent des 9 sprints).
- **« perdu au milieu » (lost in the middle)** — Échec de récupération d'une information située au milieu d'un long contexte ; `sprints/03:62-66`, `tools/aiguille.py` ; phénomène.
- **aiguille (needle)** — Sonde qui plante un code (« AZUR-7391 ») à une profondeur donnée et le redemande ; `tools/aiguille.py:1-46,57-122` ; outil/protocole de mesure.
- **greffon** — Neurone ajouté sans réentraînement, format `QPAT` ; `model.rs:2025-2037` (`Patch`), `main.rs:643` (`--patch`), `tools/make_patch.py`, `docs/glossaire.md:682,800` ; terme/fichier.

**Moteur, encodage, sparsité**
- **AER (Address Event Representation)** — Représentation par adresses d'événements : pousser des listes plutôt que multiplier des matrices ; `docs/histoire.md:12` (7,79 G événements/s), `docs/vision.md:34`, `docs/glossaire.md:736` ; concept fondateur.
- **événement** — Couple (écart d'indice, valeur) poussé vers une destination ; `docs/glossaire.md:773`, `engine.rs` ; unité de calcul.
- **liste d'activation / liste creuse / liste valuée** — Représentation creuse du vecteur d'activation ; `docs/glossaire.md:805`, `main.rs:2087-2118` ; structure.
- **push / pull / auto / `seuil_push`** — Exécution par dispersion d'événements / produit scalaire dense / choix automatique ; `main.rs:689-690` (`--auto`, `--push`), `model.rs:1845-1849` (`seuil_push`, croisement **22 %**), `tools/analyse_flux.py:8` ; stratégie.
- **SparseVec / PushMat / FusedSign / SignedDelta / BitmapSign / SparseK / DenseQ8 / DenseQ4** — Structures d'encodage creux/dense du moteur ; `list.rs:342,539-547,619`, `engine.rs:39-41` (imports de `main.rs`) ; structures Rust.
- **densité** — Proportion d'activations non nulles ; `tools/analyse_flux.py:8` (~22 % = croisement push/pull), `main.rs:44-46` (`fmt_bits`) ; mesure.
- **b/poids (bits par poids)** — Bits moyens par poids d'un encodage ; `main.rs:44-45` (`fmt_bits`), `docs/glossaire.md:541` ; métrique.
- **spiking / SNN / LIF** — Réseau à impulsions, neurone Leaky Integrate-and-Fire, comparaison avec l'événementiel ; `docs/comparaison-spiking.md:59-63,115`, `docs/glossaire.md:488` ; concept externe.
- **Hadamard** — Incohérence de Hadamard citée comme référence de QuIP# pour les i-quants ; `docs/glossaire.md:625` (seule occurrence du corpus) ; concept externe.
- **SWAR** — SIMD within a register (décodage d'octets en parallèle dans un u64) ; `main.rs:194`, `engine.rs:51` (`HIGH_BITS`), `docs/glossaire.md:847` ; technique.
- **AVX2** — Jeu d'instructions x86 utilisé par `q8_dot_avx2` et `dot16_q6_avx2` ; `gguf.rs:1603-1628`, `list.rs:823-824` ; matériel/code.
- **PTX** — Code noyau CUDA compilé depuis `gpu/drave_gpu.cu`, chargé par l'API pilote ; `gpu.rs:1-3,39-40`, `gpu.rs:231-329` (15 noms de noyaux) ; technique GPU.
- **VRAM** — Mémoire des cartes ; `gpu.rs:179` (`memoire_libre`), `materiel.rs:383` (`VRAM=84.9` Go/s) ; matériel.
- **NUMA** — Nœud mémoire/CPU ; `materiel.rs:24,118,198,238`, `engine.rs:274,332` (épinglage au premier nœud) ; matériel.
- **PCIe / NVLink** — Bus hôte↔GPU (6,5 Go/s) et lien direct (25,78 Go/s) ; `gpu.rs:7`, `materiel.rs:52,339`, `main.rs:4034,4105` ; matériel.
- **DDR3 / FPGA / DSP / ALM / M20K** — Ressources du prototype matériel : DDR3 9,66 Go/s, PE sans multiplieur (176 ALMs, 0 DSP), bancs M20K ; `docs/convertisseur.md:85-93`, `main.rs:378`, `reports/bilan-multi-materiel.md:66-67`, `reports/rapport-cpu-aer.md:11`, `tools/session_report.py:46` ; matériel.
- **mmap / MADV_WILLNEED** — Fichiers mappés en mémoire (défaut, `DRAVE_MMAP=0` force la lecture) et conseil de prélecture ; `gguf.rs:45-53,103-128,155-177`, `main.rs:64` ; technique/fichier.
- **RSS** — Mémoire résidente ; `sprints/08:146`, `main.rs:1649` (`VmRSS`/`VmSize` dans `--sonder-engram`) ; métrique.
- **TLB** — Cache de traduction d'adresses, invoqué pour le coût d'un accès aléatoire ; `main.rs:4040`, `docs/convertisseur.md:247` ; matériel.
- **zstd** — Compresseur sans perte (traces DSH `.zstd`, variante `--zstd-v2`) ; `tools/archive_sessions.py:40-42`, `tools/session_report.py:55-61`, `tools/trace_compacite.py:295-296` ; outil/format.
- **débit / bande passante / latence** — Débits mesurés (CPU 14–25 Go/s, PCIe 6,5, NVLink 25,78, VRAM ~750, RAM ~20, NVMe 5,5 aléatoire) et latence décisive en réparti ; `main.rs:3981,4034,4105`, `sprints/09:57-66`, `tools/proxy_latence.py:1-10` ; métrique.
- **porte / porte de correction / porte Drave** — Seuil chiffré de non-régression ; comparaison à une référence externe (llama.cpp) vs épreuve propre au projet ; `tools/portes.sh:2-9`, `tools/portes_formats.sh:2`, `docs/plan-deepseek41-complet.md:9,136`, `docs/glossaire.md:168-183` ; terme de méthode.
- **boxing** — Règle de sprint : 2 h chronométrées (`SCRUM_DUREE`) ; `tools/sprint.sh:1-15` ; terme de méthode.
- **verdict négatif / refus bruyant** — Piste fermée consignée, ou drapeau refusé au lieu d'être ignoré en silence ; `sprints/01:116-118`, `sprints/02:133`, `main.rs:618-619,714-737` ; principe.
- **drapeau inconnu / `--options-strict` / `--options-actives`** — Drapeaux non reconnus retenus puis affichés (ou fatals, exit 2) ; tableau de bord des options réellement appliquées ; `main.rs:494-501,618-619,714-741` ; drapeau.

## B. Drapeaux CLI et variables d'environnement

**B.1 — Binaire `drave`** (analyse manuelle unique `main.rs:580-742` ; aucun clap, aucun `--help`/`-h`/`--version` ; `argv[1]` = modèle ; aide = `main.rs:51-64`). 93 drapeaux reconnus.
- `--infer` — main.rs:604 — génération autorégressive (mode).
- `--ppl <fichier-ids>` — main.rs:605 — perplexité sur ids.
- `--ppl-texte <fichier>` — main.rs:606-607 — perplexité sur texte brut.
- `--plan` — main.rs:608 — plan de placement.
- `--tokenize` — main.rs:609 — tokenisation.
- `--gpu-banc` — main.rs:610 — banc des noyaux GPU.
- `--banc-kv N` — main.rs:611 — banc KV déporté (N clés).
- `--banc-topk N` — main.rs:612 — banc des scores d'attention (N clés).
- `--banc-mla <fichier>` — main.rs:613 — logits MLA pour comparaison numpy.
- `--tensors` — main.rs:614 — inventaire par en-têtes seuls.
- `--trace-flux <fichier>` — main.rs:615 — écrit une trace DRVF.
- `--flux-forcer <fichier>` — main.rs:616 — rejoue une trace.
- `--flux-serveur <port|hôte:port>` — main.rs:617 — nœud moteur qui écoute.
- `--options-actives` — main.rs:618 — imprime les réglages réellement appliqués.
- `--options-strict` — main.rs:619 — drapeau inconnu = erreur (exit 2).
- `--ppl-reparti <hôte:port>` — main.rs:620 — pilote réparti.
- `--couches-locales N` — main.rs:621 — couches gardées en local (défaut 12).
- `--couches A:B` — main.rs:622-628 — exécution bornée (panique si pas de `:`).
- `--trace-couches N,N` — main.rs:629-630 — couches tracées (vide = toutes).
- `--banc-vision <fichier>` — main.rs:631 — banc vision (patchs).
- `--ids 1,2,3` — main.rs:632-633 — ids séparés par virgules.
- `--ids-file <fichier>` — main.rs:634 — ids depuis un fichier.
- `--prompt <texte>` — main.rs:635 — invite.
- `--texte <texte>` — main.rs:636 — texte (tokenize).
- `--fichier <fichier>` — main.rs:637 — corpus (tokenize).
- `--sortie <fichier>` — main.rs:638 — sortie (défaut `{fichier}.ids`).
- `--matrix <nom>` — main.rs:639 (+ copie legacy 140) — tenseur ciblé (défaut `blk.0.ffn_gate.weight`).
- `--logits-bin <fichier>` — main.rs:640 — journal de logits (perplexité).
- `--neurones-sortie <fichier>` — main.rs:641 — classement des neurones chauds.
- `--harmony-contexte <fichier>` — main.rs:642 — contexte harmony.
- `--patch <fichier>` — main.rs:643 — greffon `QPAT` (garde `i+1<len`).
- `--n N` — main.rs:644 — jetons générés (défaut 32).
- `--temp F` — main.rs:645 — température (défaut 0).
- `--top-p F` — main.rs:646 — top-p (défaut 1).
- `--topk N` — main.rs:647 — diagnostic pas-à-pas des N meilleurs logits.
- `--rep-penalty F` — main.rs:648 — pénalité de répétition.
- `--hist N` — main.rs:649 — taille d'historique (défaut 64).
- `--ctx N` — main.rs:650 — contexte (défaut 512 ; 256 en perplexité).
- `--threads N` — main.rs:651 (+ copie legacy 141) — fils (défaut = tous les cœurs physiques).
- `--abits N` — main.rs:652 — bits d'activation (défaut 8 ; 16 en perplexité).
- `--bits N` — main.rs:653 — précision simulée des poids → `list::BITS_POIDS` (main.rs:740).
- `--limit N` — main.rs:654 — plafond (jetons en perplexité, lignes en `--gpu-banc`).
- `--depuis N` — main.rs:655 — début de notation.
- `--lot N` — main.rs:656 — taille du lot de préremplissage (1 = jeton par jeton).
- `--keep F` — main.rs:657 — fraction de poids conservés (défaut 1.0).
- `--moe-topk N` — main.rs:658 — top-k du routeur MoE.
- `--attn-window N` — main.rs:659 — fenêtre d'attention.
- `--swa-pattern N` — main.rs:660 — motif de fenêtres par couche.
- `--attn-sinks N` — main.rs:661 — nombre de puits.
- `--attn-topk N` — main.rs:662 — top-k d'attention.
- `--qk-topk N` — main.rs:663 — top-k des scores q·k.
- `--hebbian N` — main.rs:664 — capteur hebbien sur la couche N.
- `--hebb-q F` — main.rs:665 — quantile (défaut 0.1).
- `--hebb-out F` — main.rs:666 — sortie (défaut `hebb.bin`).
- `--act-thresh F` — main.rs:667 — seuil de parcimonie (fraction du max).
- `--act-topk N` — main.rs:668 — k-WTA.
- `--topk-q|--topk-k|--topk-v|--topk-o|--topk-gate|--topk-up|--topk-down N` — main.rs:669-675 — top-k par projection (fraction de la dimension).
- `--ffn-gain C:G` — main.rs:676-679 — gain FFN par couche.
- `--bits-attn N` / `--bits-ffn N` — main.rs:680-681 — 6 bits si N==6 seulement (sinon aucun effet ni avertissement).
- `--flux` — main.rs:683 — sortie en flux.
- `--flux-liste` — main.rs:684 — encodage mode 1.
- `--flux-blocs` — main.rs:685 — mode 2 (et 4 si lot).
- `--session` — main.rs:686 — boucle interactive (pose `flux=true`).
- `--chat` — main.rs:687 — gabarit de conversation (Qwen2.5/harmony).
- `--dense` — main.rs:688 — chemin dense.
- `--auto` — main.rs:689 — choix automatique (défaut).
- `--push` — main.rs:690 — force push (`auto=false`, `dense=false`).
- `--pin` — main.rs:691 — épingle les workers (effet immédiat, 739).
- `--sans-fenetre` — main.rs:692 — `attn_window=0`.
- `--sans-yarn` — main.rs:693 — désactive YaRN.
- `--act-renorm` — main.rs:694 — renormalise après sélection.
- `--materiel` — main.rs:695 — détection matérielle + plan (ne charge pas le modèle).
- `--config` — main.rs:696 — ce que le moteur comprend du modèle.
- `--sonder-engram N` — main.rs:697 — sonde mmap de l'engram (défaut 1000).
- `--bloc TENSEUR:INDEX` — main.rs:698 — déquantifie un bloc (garde `i+1<len`).
- `--tete-garantie F` — main.rs:699-700 — restriction de tête prouvée exacte.
- `--tete-restreinte F` — main.rs:701-702 — restriction (génération seule).
- `--profil-neurones` — main.rs:703 — profilage PowerInfer.
- `--harmony` / `--harmony-assistant` / `--harmony-user` / `--harmony-suite` — main.rs:704-707 — modes de fenêtrage harmony.
- `--q4` (`|=3`) / `--q4-ffn` (`|1`) / `--q4-attn` (`|2`) / `--q4-tout` (`|=7`) — main.rs:708-711 — masque q4.
- Défauts par mode : inférence 512/8 (775-777) ; perplexité 256/16 (4303-4305) ; flux-serveur 4096 (2480) ; ppl-reparti 256 + couches_locales 12 (2606-2608) ; banc-mla 4096 figé (3449) ; banc-kv bits 32 (3492) ; banc-topk bits 8 (2872).
- Priorité des modes (main.rs:91-121) : materiel > config > sonder-engram > bloc > banc-vision > flux-serveur > ppl-reparti > tensors > banc-mla > banc-kv > banc-topk > gpu-banc > plan > tokenize > ppl > infer ; plusieurs modes ⇒ avertissement `[modes]` (102-105, `--bloc` absent de la liste).
- Chemin historique sans mode : `--matrix`, `--threads` seulement (main.rs:137-146).

**B.2 — Outils Python**
- `aiguille.py <modele> <longueurs> <profondeurs>` — l.127-129 ; `--n` (40) l.130 ; `--threads` (16) l.131 ; `--lot` (256) l.132 ; `--timeout` (7200) l.133 ; `--gpu` l.134 ; `--gpu-kv` l.135 ; `--attn-topk` (0) l.140-141 ; `--gpu-topk` l.142-143 (exige `--attn-topk`, l.149-150) ; `--journal` l.144 ; pose `DRAVE_GPU`, `DRAVE_GPU_KV`, `DRAVE_GPU_TOPK` (l.74-82).
- `analyse_empreinte.py <trace>` — `--limite N` l.71-72 ; `--modele {deepseek4,deepseek41,qwen3moe}` l.73-75 ; connus (43,256,6,5.51)/(40,384,6,9.95)/(48,128,8,3.05) l.188-192.
- `analyse_experts_statique.py <modele.gguf>` — `--couches` ("0,12,24,36,47") l.176 ; `--lignes` (16) l.177-178 ; `--seuil` (0.90) l.179-180.
- `analyse_flux.py <trace> [<trace2>...]` — `--top` (100, parsé main) l.83-84 ; max 3 traces (l.85).
- `clusters_moe.py <trace>` — `--clusters` (8) l.145-146 ; `--json` l.147 ; `--graine` (1234) l.148.
- `compare_etats.py <préfixe_drave> <préfixe_ref> <nom> <couche> <positions>` — 5 positionals, aucune option (l.15-16,46-48).
- `compare_logits.py <notre.bin> <ref.bin> [ids.txt]` — aucune option ; code retour 2 si ids absents (l.58-65) ; accord top-1 global (l.73-76,95-97).
- `convertir_clusters.py <source.gguf> <dossier>` — `--clusters` (8) l.357 ; `--trace` l.358 ; `--mode {experts,couches}` l.359 ; `--verifier` l.360-361.
- `diff_flux.py <traceA> <traceB>` — `--top` (8, parsé main) l.39-41.
- `flux_codec.py <trace>` — `--jetons N` (parsé main) l.146-147.
- `harmony_canonique.py` — `--sans-analysis` (testé par `in sys.argv`) l.45.
- `hc_synthetique.py` — aucun argument (l.14).
- `lire_meta_gguf.py <fichier.gguf> [motif ...]` — aucune option (l.71-74).
- `mesurer_lecture_experts.py <shard.gguf> [nb_blocs=240] [nb_fils=16]` — aucune option (l.36-38).
- `mla_synthetique.py` — `--sortie` (/tmp/mla_minuscule.gguf) l.226 ; `--dossier` (/tmp/mla_ref) l.227 ; `--graine` (1234) l.228 ; `--n` (8) l.229.
- `pair_factice.py <port=45760> [dimension=896]` — aucune option (l.32-33) ; `MODES` 0-4 l.17-18 ; `TETE=79` l.15.
- `profil_flux.py <trace>` — `--top` (6) l.39-40 ; `--csv` l.42-43.
- `proxy_latence.py <port_écoute> <hôte:port> [délai_ms=0]` — aucune option (l.35-37).
- `session_report.py` — `--repo` (racine du dépôt) l.293 ; `--session` l.294 ; `--quiet` l.295.
- `telecharger_modeles.py` — `--manifeste` (tools/manifeste_modeles_lourds.json) l.127 ; `--dest` (…/modeles/gguf) l.128 ; `--seulement` l.129 ; `--etat` l.130 ; `--journal` (/tmp/telechargement_lourds.log) l.131.
- `trace_compacite.py <trace>` — `--couches` l.287-288 ; `--sans-compression` l.289-290 ; `--sans-erreur` l.291-292 ; `--echantillon` (16.0 Mio) l.293-294 ; `--zstd-v2` l.295-296.
- `verifier_formats.py <modele.gguf> <tenseur> [index=0]` — `--type N` (parsé main) l.64-65 ; env `REF_GGML_BLOC` l.28.
- `vision_mtmd.py [modele.gguf] [mmproj.gguf] [sortie.bin]` — aucune option (l.59-60,150).
- `vision_ref.py <sortie.bin> [poids]` — aucune option ; le docstring annonce `--poids` mais c'est un 2e positional (l.9 vs l.29).

**B.3 — Scripts shell**
- `portes.sh [rapide]` — `$1=rapide` l.14,71,105 ; `D=./drave-core/target/release/drave` l.13 ; `A=…/qwen3-30b-8clusters-v2` l.56 ; `M=…/modeles/gguf` l.95 ; `O=…/gpt-oss-120b-MXFP4.gguf` l.106 ; attendus 19.3885 l.53, 799.8557 l.60, 15.6017 l.121 ; seuil tests `-ge 48` et 0 échec l.42 ; timeouts 600/900/1800/2400 l.51,58,75,119 ; aucune variable d'env lue.
- `portes_formats.sh [type ...]` — `filtre="${*:-}"` l.53 ; `DRAVE_MODELES` l.19 ; `DRAVE_LLAMA` l.20 ; `REF_GGML_BLOC` l.21 ; 17 types testés l.26-45 ; blocs 0 et 7 l.65-66.
- `verifier_table_types.sh [chemin llama.cpp]` — `$1` défaut `…/GitHub/llama.cpp` l.19 ; `SRC=drave-core/src/gguf.rs` l.20 ; exit 1 si divergents l.120.
- `inventaire_modeles_lourds.sh [dossier]` — `$1` défaut `…/modeles/gguf` l.13 ; binaire l.14 ; lit `tools/manifeste_modeles_lourds.json` l.35,38 ; timeout 600 l.25.
- `extraire_tables_ggml.sh [verifier]` — `DRAVE_LLAMA` l.15 ; `TMPDIR` l.16 ; tables comparées l.39 (`IQ2XXS_GRID`, `KSIGNS_IQ2XS`, `IQ1S_GRID`, `IQ3XXS_GRID`, `KVALS_IQ4NL`).
- `preparer_colab.sh [modele.gguf] [port=5599]` — l.9-10 ; `/tmp/drave.bundle` l.11 ; empreinte sha256 tronquée 24 car. l.23 ; notebook `colab/Drave-reparti.ipynb` l.46.
- `colab_cote_local.sh [modele.gguf] [port=5599]` — l.12-13 ; `--flux-serveur 0.0.0.0:$PORT --ctx 256` l.30 ; `/tmp/noeud_colab.log` l.30 ; attente 60×0,5 s l.32.
- `sprint.sh <start|status|close|list> ["objectif"]` — l.26-28 ; `SCRUM_DUREE` (7200 s) l.15 ; `sprints/COURANT` l.16 ; trame de clôture l.60-67.

**B.4 — Variables `DRAVE_*`** (39 noms déclarés `main.rs:17-27`, liste vérifiée par test ; message si l'ancien nom `QT_*` est posé, `main.rs:80-86`)
- `DRAVE_GPU` — gpu.rs:1540,1565 — active le déport GPU (sans elle, rien ne va au GPU).
- `DRAVE_GPU_KV` — model.rs:3088 — miroir VRAM du cache KV.
- `DRAVE_GPU_TOPK` — main.rs:430,443-450 ; model.rs:3123,5512 — chaîne top-k déportée (`0`/vide = inactif) ; motifs d'inactivité affichés (k=0, k>1024, KV≠8/32, fenêtre>0, lot>1).
- `DRAVE_GPU_TETE` — model.rs:3066 — tête de sortie sur GPU.
- `DRAVE_GPU_EXPERTS` — model.rs:3151 — cache VRAM des experts MoE.
- `DRAVE_GPU_EXPERTS_GO` — model.rs:3162 — budget du cache (Go).
- `DRAVE_KV_BITS` — main.rs:2872 (défaut 8), main.rs:3492 (défaut 32), model.rs:2940 — quantification KV (32/8/4).
- `DRAVE_KV_F16` — model.rs:2157 — arrondi f16 avant quantification.
- `DRAVE_KV_K_F16` — model.rs:2155 — clés en f16.
- `DRAVE_KV_K_F32` / `DRAVE_KV_V_F32` — model.rs:2154 — clés/valeurs en f32.
- `DRAVE_Q8_BLOCS` — model.rs:960 — une échelle int8 par bloc de 32.
- `DRAVE_SANS_EMPRUNT` — model.rs:1021,1028 — force la reconstruction.
- `DRAVE_MMAP` — gguf.rs:156 — `0`/`non`/`false` ⇒ lecture complète (défaut mmap).
- `DRAVE_PRELIRE` — gguf.rs:95 — prélecture madvise (défaut activé).
- `DRAVE_PRELIRE_TOUT` — gguf.rs:91 — charger le fichier entier (1/oui/true).
- `DRAVE_CLUSTERS` — clusters.rs:168 — liste `0,3` de clusters à charger.
- `DRAVE_TRACE_BLOCS` — model.rs:1507 — trace v3 (i8 + échelle f16 par bloc).
- `DRAVE_TRACE_EXPERTS` — model.rs:3204 — trace de routage (couche jeton experts…).
- `DRAVE_ETAT_ENTREE` — model.rs:3222 — état d'entrée REFD.
- `DRAVE_DUMP_COUCHES` — model.rs:3223 — préfixe de vidage des couches.
- `DRAVE_FLUX_VERIF` — model.rs:5302 — vérification du flux rejoué.
- `DRAVE_DEBUG_FLUX` — main.rs:2555 — trace du nœud flux-serveur.
- `DRAVE_DEBUG_ETAT` — model.rs:5181 — norme de l'état résiduel.
- `DRAVE_DEBUG_MLA` — model.rs:4512,5182 — valeurs des projections MLA.
- `DRAVE_HARMONY_TRACE` — main.rs:4222,4267 — affiche chaque fenêtre harmony.
- `DRAVE_VISION_TEXTE` — main.rs:1508 — modèle de texte du banc vision.
- `DRAVE_YARN` / `DRAVE_YARN_NON` / `DRAVE_YARN_MSCALE` / `DRAVE_YARN_RAMPE` — model.rs:2565-2571,3799 — force/interdit YaRN, mscale, rampe.
- `DRAVE_BANC_SANS_PUITS` — main.rs:3151 — banc sans puits.
- `DRAVE_BANC_KV_K0` / `_V1` / `_UNIT` / `_GRAD` / `_KUNIT` / `_GPU_SEUL` / `_DEBUG` — main.rs:3509-3522,3550,3639,3646 — cas dégénérés du banc KV.
- Hors moteur : `DRAVE_MODELES` (portes_formats.sh:19), `DRAVE_LLAMA` (portes_formats.sh:20, extraire_tables_ggml.sh:15), `REF_GGML_BLOC` (portes_formats.sh:21, verifier_formats.py:28), `TMPDIR` (extraire_tables_ggml.sh:16), `SCRUM_DUREE` (sprint.sh:15), `LD_LIBRARY_PATH` (verifier_table_types.sh:53), `DSH_HOME` (session_report.py:55-61). Aucune variable `RAYON_*`, `OMP_*`, `MKL_*`, `OPENBLAS_*`, `CUDA_*` n'est lue.

## C. Contradictions, chiffres périmés, affirmations douteuses
- `sprints/01:12` — « 13 480 (le chiffre avait bougé de 312 lignes) » — le commit cité l.24 (`1f53667`) annonce 13 168 ; les deux chiffres cohabitent sans dire lequel est la mesure finale (sprint 7 dira 13 758, l.95).
- `sprints/01:31` — commit « exact à 1,03e-7, 40× plus rapide » — contredit par le tableau l.42 (« 1,6–2,3e-7 ») ; l'écart flatteur venait d'un banc qui réutilisait la même clé (l.56).
- `sprints/01:48` — « le croisement en clés est entre 255 et 2 047 » — formulation corrigée depuis « entre 8 192 et 16 384 clés » (l.89-93), qui confondait contexte et nombre de jetons.
- `sprints/01:116-118` — « `--attn-topk` est **ignoré par le mode lot** … **non corrigé** » — périmé : le moteur imprime désormais « IGNORÉ en mode lot » (`model.rs:3969`, message unique `LOT_TOPK_IGNORE` `model.rs:2465`).
- `sprints/02:47` — « 8 191 | 4 095 | 38,84 | (mesuré) | (calculé) » — cellules GPU/rapport étiquetées au lieu de chiffrées : ligne illisible et non vérifiable.
- `sprints/02:31` — « croisement à ~300 clés » — présenté comme mesure alors que le seuil mesuré du noyau fusionné est 131 072 clés (l.29) ; deux « croisements » distincts sous un seul mot.
- `sprints/03:51-53` — « ~175 ms par jeton de prompt (`--infer` préremplit jeton par jeton) » — **faux**, corrigé dans le même fichier l.79-85 (le préremplissage par lots est actif).
- `sprints/03:141-143` — introspection : « … parce que le préremplissage par lots n'est pas branché en inférence » — reprise de l'affirmation corrigée l.84 ; la cause invoquée est fausse.
- `sprints/03:29-30` vs `sprints/05:60` — « 511/511 » réapparaît comme accord top-1 (lot 1 vs 256) après la correction d'un « 511/511 » fautif en 497/511 (`sprints/03:40-47`) ; même graphie, mesures différentes.
- `sprints/04:14` — commit `09adea5` « 0/3 au milieu à k=512, 3/3 à k=1024 (trois fenêtres par point) » — contredit l.36-44 : les trois colonnes sont trois répétitions de la **même** invite (garde-fou d'offset).
- `sprints/04:39` — « l'offset avance de 200 000 » avec garde-fou à 400 000 — `sprints/05:79` décrit le même garde-fou comme « **20 000 fixes** » ; deux versions du même défaut, non réconciliées.
- `sprints/04:22-34` — tableau « 0/0/3 » présenté comme balayage en k — invalidé l.36-44 (répétitions déterministes) ; seuls la convergence avec le premier balayage et le seuil (12,5 %, 25 %] subsistent.
- `sprints/05:77-78` — « « 7e-4 nat par position AU PLUS » — contredit par le tableau deux lignes plus haut (max 0,0068) : c'est la MOYENNE. Corrigé. » — erreur reconnue dans le fichier.
- `sprints/06:32` — « k = 256 (GPU) | **NON** | (non mesuré) | … » — état périmé : `sprints/07:71` donne k=256 sur les 9 fenêtres (8/9).
- `sprints/06:53-54` — « Le « facteur 10 à 20 » est donc un minorant observé, pas une mesure » — puis l.58-62 : ce n'était pas un ralentissement mais un **LIVELOCK** (`while cap < besoin { cap = (cap*2).min(ctx) }`) ; la qualification initiale est fausse.
- `sprints/07:45-48` — « là où j'ai écrit « rendu la main en 312 s » … Mon script de vérification ne lisait ni le code de sortie ni le mot « panicked » : il a pris un core dump pour une réussite » — affirmation fausse reconnue (SIGABRT exit 134).
- `sprints/07:138-142` — « **DeepSeek-V4.1-Flash est un modèle d'API** … **aucun poids ouvert**, donc rien à télécharger » — contredit par le dépôt : `tools/manifeste_modeles_lourds.json:3` déclare `DeepSeek-V4.1-Flash-Q2` (repo `antirez/deepseek-v4.1-flash-gguf`, 365 713 686 528 octets), `tools/portes_formats.sh:38` teste `DeepSeek-V4.1-Flash-Q2.gguf`, `sprints/09:5,10` mesure ses 365,7 Go.
- `sprints/07:60` — « **18 tests** au lieu de 17 » vs `sprints/08:65` « **32 verts** (20 → 32) » vs `sprints/08:278` « **30 tests verts** (20 au début) » — trois décomptes pour le même sprint dans le même fichier ; `tools/portes.sh:42` exige ≥48 (53 `#[test]` dans les sources).
- `sprints/08:118-119` — « L'épreuve d'exécution : **ACQUISE**, 15,2789 des deux côtés » vs `sprints/08:257-260` « Le chemin par lots sur les MoE : **établir d'abord s'il est cassé** » — contradiction interne : la même page dit qu'il fonctionne (15,2736 en `--lot 64`, l.120-126).
- `sprints/08:132-133` — « `read_to_end` charge tout le fichier : DeepSeek-V4.1-Flash fait 366 Go, il **faudra** `mmap` » — périmé dans le même fichier : le mmap est livré l.145-149 et 283 ; `sprints/08:263` (Planning #3) le redemande.
- `sprints/08:218-221` — « 27,8 s de chargement, est-ce mieux ? Non, c'est **plus lent** que le fichier unique annoncé à 3,9 s » — deux périmètres différents (3,20 Go d'un cluster contre 18,55 Go complet) : comparaison écartée mais les deux chiffres restent côte à côte (l.62).
- `sprints/09:70` — « **Huit** pistes ont été testées, trois ont survécu » vs `sprints/09:100` « **Onze** pistes mesurées, trois retenues » — le tableau l.29-41 en compte onze : « huit » est un vestige.
- `sprints/09` — **deux** « ## Rétrospective » (l.68 et l.106) et **deux** « ## Planning » (l.84 et l.120) : deux versions fusionnées, la première précédant la section « Revue » (l.94).
- `sprints/09:5,10,19` — « Cible : **DeepSeek-V4.1-Flash** (365,7 Go) », « L'empreinte de V4.1 tombe… », engram `blk.N.engram_embd.weight` — le modèle effectivement téléchargé/converti ailleurs est **DeepSeek-V4-Flash** (`sprints/07:13,140-143`) ; V4.1 et V4-Flash sont employés l'un pour l'autre (voir `sprints/07:138`).
- `sprints/09:61-64` — « NVMe, aléatoire, blocs 4 Mo **5,5 Go/s** » > « NVMe, séquentiel **2,1 Go/s** » — l'aléatoire plus rapide que le séquentiel n'est explicable que par des tailles de bloc différentes, non données : affirmation douteuse en l'état.
- `sprints/09:74-76` et `sprints/09:111-115` — « trois fois un chiffre absurde a sauvé la conclusion (disque à 2 211 Go/s, allocation à 4,1 %, total à 4 231 Go) » / « `pread` sans contrôle a produit un chiffre faux d'un facteur 37 000 » — chiffres faux reconnus, conservés sans la valeur correcte correspondante.
- `tools/aiguille.py:84-88` — « un prompt PLUS LONG que le contexte **ne fait pas échouer le moteur — il le ralentit d'un facteur 10 à 20 sans un mot** (mesuré : 13 à 23 min au lieu de 75 s) » — **périmé** : `sprints/06:58-62` établit un livelock (jamais terminé) et `sprints/07:38-56` un correctif (troncature annoncée, exit 0) ; le commentaire de l'outil contredit l'état du moteur.
- `tools/aiguille.py:19-22` — « depuis le **sprint 4**, le décalage de fenêtre est RÉELLEMENT appliqué » — le correctif définitif du pas/garde-fou est daté du sprint 5 (`sprints/05:79-85`, `aiguille.py:167-199`) ; le sprint 4 n'avait produit qu'un garde-fou à 20 000 fixes.
- `tools/profil_flux.py:8` — l'usage annonce `[--couche N]` — option jamais lue ni implémentée (main l.36-43) : aide qui ment.
- `tools/vision_ref.py:9` — l'usage annonce `[--poids <sortie.bin.poids>]` — ce n'est pas une option mais un 2e positional (l.28-29) ; passer `--poids` donne un chemin littéral « --poids ».
- `tools/harmony_canonique.py:17` — `Q = ".../GitHub/Drave/drave-core/target/release/drave"` — chemin codé en dur vers un répertoire **inexistant** (`GitHub/Drave` ; le dépôt est `GitHub/Qtrinet`) : l'outil ne peut pas tourner tel quel.
- `drave-core/src/main.rs:454-456` — docstring de `fils()` : « sinon la moitié des cœurs » — le code (l.460-462) rend `coeurs_physiques().max(1)`, soit **tous** les cœurs physiques ; le commentaire d'`Options` (l.530-533) dit encore « la moitié des cœurs contre les trois quarts ».
- `drave-core/src/main.rs:541` — champ `ppl_profil: bool` sans aucune branche dans `analyser` (580-742) — `--ppl-profil` n'existe pas : tout usage est classé drapeau inconnu ; le champ reste toujours `false` (l.4295, 4493-4585 morts).
- `drave-core/src/main.rs:51-64` — l'aide n'énumère ni `--plan`, `--tokenize`, `--config`, `--flux-serveur`, `--ppl-reparti`, `--banc-*`, `--banc-vision`, `--bloc`, `--gpu-banc`, ni `--options-*` : 15 des 16 modes sont absents de l'usage.
- `sprints/03:81` et `sprints/06:60` / `sprints/07:29` — citations `model.rs:3911` et `model.rs:1117` — ces numéros ne résolvent plus dans le fichier actuel (7022 l.) : `3911` tombe dans `rope_inverse`, `1117` dans `CacheExperts` ; `KvCache::assurer` est à `model.rs:2169`, `kv_assurer` à `gpu.rs:440`.
- `tools/portes.sh:29-30` — « Prendre la première occurrence du motif donnait 17,431 (fenêtre 1) au lieu de 19,3885 (total) — un instrument faux qui accuse le code » — cohérent avec `sprints/01:49`, mais c'est la même classe d'erreur que `sprints/03:42-47` (sortie partielle lue comme globale), non mutualisée.
- `sprints/05:62` — « 7e-4 nat par position suffit à changer un jeton greedy après quelques dizaines de pas » — l'écart moyen mesuré est 0,0007 et le max 0,0068 (l.60) : la généralisation « suffit » n'est pas mesurée.

## D. Fichiers du dépôt cités ou définis
- `sprints/01-premier-des-trois-noyaux-gpu-du-top-k-le.md` … `09-empreinte-memoire-ce-qui-reduit-vraiment.md` — les 9 journaux de sprint dépouillés ; définis par `tools/sprint.sh:33,41,68`.
- `sprints/COURANT` — état `num debut fin` du sprint en cours ; `tools/sprint.sh:16,34`.
- `tools/aiguille.py` — sonde aiguille (récupération d'un code à une profondeur) ; cité `reports/rapport-aiguille-topk.md`.
- `tools/analyse_empreinte.py` — empreinte mémoire d'un MoE depuis une trace de routage ; cité `sprints/09:73,97`.
- `tools/analyse_experts_statique.py` — analyse statique des poids d'experts (jumeaux, sources, destinations) ; fournit `Lecteur` à `verifier_formats.py`.
- `tools/analyse_flux.py` — analyse pure d'une trace DRVF (densité, neurones persistants).
- `tools/archive_sessions.py` — archive des sessions DSH (JSONL/zstd).
- `tools/clusters_moe.py` — découpage des MoE en clusters depuis une trace de routage ; JSON consommé par `convertir_clusters.py --trace`.
- `tools/colab_cote_local.sh` — côté local de la démonstration Colab (nœud + tunnels).
- `tools/compare_etats.py` — comparaison tenseur par tenseur Drave/llama.cpp (format `REFD`, vidages `DRAVE_DUMP_COUCHES`).
- `tools/compare_logits.py` — comparaison de deux fichiers de logits (NLL, rang, accord top-1) ; cité `sprints/03:43`.
- `tools/convertir_clusters.py` — convertisseur GGUF → clusters (`commun.gguf`, `cluster-NN.gguf`, `manifeste.json`, `mapping.tsv`).
- `tools/diff_flux.py` — diff de deux traces DRVF.
- `tools/extraire_tables_ggml.c` / `.sh` — extraction/vérification des grilles IQ contre libggml ; compare à `drave-core/src/formats.rs`.
- `tools/flux_codec.py` — codec de référence DRVF v1/v2 (lit v3).
- `tools/harmony_canonique.py` — identifiant de perplexité au format harmony canonique (canaux `analysis`/`final`).
- `tools/hc_synthetique.py` — référence numpy des hyper-connexions V4 + témoins collés dans `model::tests_hc`.
- `tools/inventaire_modeles_lourds.sh` — inventaire des GGUF lourds confronté au manifeste HF.
- `tools/lire_meta_gguf.py` — lecture des métadonnées GGUF (en-tête seul).
- `tools/make_patch.py` — fabrication d'un greffon `QPAT` (`--patch`) ; cité `docs/glossaire.md:890`.
- `tools/manifeste_modeles_lourds.json` — manifeste des 24 fichiers lourds (nom, repo, chemin, octets) ; lu par `inventaire_modeles_lourds.sh:35` et `telecharger_modeles.py:127`.
- `tools/mesurer_lecture_experts.py` — lectures d'experts série/parallèle à froid (`posix_fadvise`).
- `tools/mla_synthetique.py` — modèle MLA synthétique + référence numpy (`logits.npy`, `ids.npy`, `forme.json`) ; consommé par `--banc-mla`.
- `tools/pair_factice.py` — pair factice du protocole de flux (écoute, dit ce qu'il reçoit) ; sert avec `--flux-serveur`/`--ppl-reparti`.
- `tools/portes.sh` — portes de non-régression du dépôt (Qwen, clusters, gpt-oss, matériel, formats).
- `tools/portes_formats.sh` — portes des décodeurs de formats contre libggml, bloc par bloc.
- `tools/preparer_colab.sh` — préparation de la répétition Colab (bundle git, empreinte, commandes).
- `tools/profil_flux.py` — profilage par neurone d'une trace DRVF (+ CSV).
- `tools/proxy_latence.py` — relais TCP ajoutant une latence par message.
- `tools/ref_ggml_bloc.c` / `tools/ref_logits.cpp` / `tools/ref_logits` — références C/C++ liées à libggml et llama.cpp ; cités `portes_formats.sh:15`, `verifier_formats.py:28`.
- `tools/session_report.py` — rapport par session DSH (`journal/sessions/<id>/rapport.md`, `journal/README.md`).
- `tools/sprint.sh` — boxing temps réel (`start`/`status`/`close`/`list`).
- `tools/telecharger_modeles.py` — téléchargement par tranches avec reprise (sidecar `.etat.json`, curl `-r`).
- `tools/trace_compacite.py` — chiffrage d'une trace DRVF sous plusieurs encodages (zstd compris).
- `tools/verifier_formats.py` — comparaison d'un super-bloc déquantifié à libggml (`--bloc`).
- `tools/verifier_table_types.sh` — confrontation de la table des types ggml du moteur à `libggml`.
- `tools/vision_mtmd.py` — référence de vision via libmtmd d'ollama.
- `tools/vision_ref.py` — référence numpy de l'embedding de patchs (mRoPE 2-D) ; consommé par `--banc-vision`.
- `drave-core/src/main.rs` (5033 l.) — CLI, modes, protocole de flux, bancs (top-k, KV, MLA, vision, GPU), serveur/pilote réparti, tokenize, plan, matériel.
- `drave-core/src/model.rs` (7022 l.) — modèle, MoE, MLA/Mla4, hyper-connexions, KV cache, traces/rejeu, `generate`/`forward`/`forward_lot`.
- `drave-core/src/gguf.rs` (2246 l.) — lecteur GGUF multi-fichiers/shardé, mmap, tables de types, déquantifications.
- `drave-core/src/formats.rs` (2847 l.) — grilles IQ (`IQ2XXS_GRID`, `KSIGNS_IQ2XS`, `IQ1S_GRID`, `IQ3XXS_GRID`, `KVALS_IQ4NL`) et déquantificateurs i-quants.
- `drave-core/src/gpu.rs` (1573 l.) — contexte CUDA par API pilote, PTX, 15 noyaux, KV VRAM, chaîne top-k.
- `drave-core/src/clusters.rs` (506 l.) — ouverture d'un modèle en clusters (`commun.gguf`, `cluster-NN.gguf`, `mapping.tsv`, `DRAVE_CLUSTERS`).
- `drave-core/src/materiel.rs` (478 l.) — détection CPU/NUMA/GPU/disques et plan (`--materiel`).
- `drave-core/src/list.rs` (1572 l.) — encodages creux/denses (`Source`, `Source8`, `PushMat`, `DenseQ8`, `DenseQ4`, `BLOC_Q4`, `LUT_INT4`, `LUT_MXFP4`, `BITS_POIDS`).
- `drave-core/src/engine.rs` (1010 l.) — pool de threads, épinglage NUMA (`EPINGLER`), matvec, SWAR.
- `drave-core/src/tokenizer.rs` (507 l.) — tokenizer BPE byte-level (motifs Qwen2/o200k).
- `drave-core/gpu/drave_gpu.cu` et `drave-core/gpu/drave_gpu.ptx` — source et PTX des noyaux (`gpu.rs:39-40`).
- `drave-core/Cargo.toml`, `drave-core/target/release/drave` — crate et binaire utilisés par tous les outils (`tools/aiguille.py:41`, `portes.sh:13`).
- `docs/contexte-long.md`, `docs/plan-deepseek-v4-flash.md`, `docs/plan-deepseek41-complet.md`, `docs/format-flux.md`, `docs/histoire.md`, `docs/comparaison-spiking.md`, `docs/convertisseur.md`, `docs/glossaire.md` — documents cités (contexte long, plan DeepSeek, spécification DRVF, traduction `QT_*`→`DRAVE_*`, comparatif spiking, placement PCIe/DDR3, glossaire) ; tous présents.
- `reports/rapport-gpu-topk-selection.md`, `rapport-aiguille-topk.md`, `rapport-empreinte-memoire.md`, `rapport-mode4-lot-listes.md`, `rapport-lecteur-multifichiers.md`, `rapport-logits-gpu-vs-cpu.md`, `rapport-drapeaux-ignores.md` — rapports cités par les sprints et les outils ; tous présents.
- `README.md`, `REPRISE.md` — handoff et compteur de lignes cités par `sprints/01:50`, `sprints/07:89-95` ; présents.
- `data/wikitext2_test.txt` — corpus de remplissage de l'aiguille et des portes (`aiguille.py:42`, `portes.sh:115`) ; présent.
- `colab/Drave-reparti.ipynb` — notebook de la démonstration répartie (`preparer_colab.sh:46`) ; présent.
- `models/Qwen2.5-0.5B-Q8_0.gguf`, `models/Qwen2.5-0.5B-Q4_0.gguf` — modèles des portes et des bancs (`portes.sh:51`, `portes_formats.sh:28`) ; présents.
- `/home/stephane/Data13TB/stephane/modeles/gguf/*.gguf` — modèles lourds (gpt-oss-120b-MXFP4, DeepSeek-V4-Flash-UD-IQ1_M 3 shards, DeepSeek-V4.1-Flash-Q2, Kimi-K2.7-Code, GLM-5.3, Qwen3-235B…) ; `portes.sh:95-99,106`, `manifeste_modeles_lourds.json`.
- `mapping.tsv`, `commun.gguf`, `cluster-NN.gguf`, `manifeste.json` — artefacts du format clusters (produits par `convertir_clusters.py`, lus par `clusters.rs`) ; absents du dépôt (données générées).
- `/home/stephane/GitHub/llama.cpp` — dépôt externe de référence (libggml/llama.cpp) ; `DRAVE_LLAMA` (`portes_formats.sh:20`, `extraire_tables_ggml.sh:15`, `verifier_table_types.sh:19`).
- `/tmp/ref_ggml_bloc`, `/tmp/drave.bundle`, `/tmp/noeud_colab.log`, `/tmp/ids_*.txt`, `/tmp/wt2_*.txt`, `/tmp/mla_*` — artefacts temporaires partagés entre outils (`portes.sh`, `preparer_colab.sh`, `colab_cote_local.sh`, `harmony_canonique.py`, `mla_synthetique.py`).
- `journal/sessions/<id>/rapport.md`, `journal/README.md` — sorties de `session_report.py` ; `journal/` présent.

Aucun fichier n'a été modifié. Livrable également transmis à l'agent parent `3d5618a0-4e3a-45bb-943d-a72c753fb7da`.

