# Session DSH — relecture

- identifiant : `3d5618a0-4e3a-45bb-943d-a72c753fb7da`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-02 15:02:54
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu écris un **document de référence** pour le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet : un **glossaire raisonné** de tout le vocabulaire, sigles, abréviations et notions employés dans `docs/` et `reports/`, destiné à un **néophyte** qui veut pouvoir lire et comprendre tous les documents du dépôt.

CONTEXTE DU PROJET (vérifie chaque point dans les fichiers, ne me crois pas sur parole) : Drave est un moteur d'inférence en Rust (`std` seul) qui charge des modèles GGUF **en place** et exécute les projections soit en **listes d'activation** (flux d'événements, « push »), soit en produit scalaire dense (« pull »). Le cœur du projet : router ces flux sur des **grappes de neurones** réparties entre composants (CPU/GPU/FPGA) et machines, et **lire ces flux** pour comprendre et adapter l'architecture à la tâche. `llama.cpp` sert de **porte de correction** (référence externe), jamais de but.

CE QUE TU DOIS PRODUIRE — un seul fichier neuf : `docs/glossaire.md`. Tu ne modifies AUCUN autre fichier (pas de `docs/vision.md`, pas de README, rien). Si tu constates qu'un document dit quelque chose de faux ou de périmé, tu ne le corriges pas : tu le listes à la fin dans une section « Points relevés, non corrigés ».

MÉTHODE :
1. Lis `docs/` (18 documents) et `reports/` (une centaine de rapports) — utilise `grep`/`glob`/`read`, pas de supposition. Recense **tous** les sigles et termes techniques qui ne sont pas du français courant.
2. Pour chaque entrée, donne : le **sigle ou terme**, sa **forme développée** (française et anglaise quand les deux existent), une **définition d'une à trois phrases** compréhensible par quelqu'un qui ne connaît ni les LLM ni le matériel, **où le moteur s'en sert** (fichier ou outil du dépôt), et une **référence externe** (article fondateur, documentation officielle, spécification) sous forme de lien markdown — par exemple pour GGUF, RoPE, MLA, MoE, Sinkhorn, YaRN, MXFP4, Q4_K, IQ2_XXS, SparseVec/AER, KV cache, préremplissage, perplexité, NLL, top-k, softmax, RMSNorm, SiLU/SwiGLU, LoRA, MTP, speculative decoding, FPGA/DSP/ALM/M20K, DDR3, PCIe, NUMA, AVX2, PTX, VRAM/RSS, débit/bande passante, TLB, mmap, zstd, Hadamard, DSA/indexeur, CSA/HCA, hyper-connexions, engram, MTP, DRVF, DRVF v5 et ses 5 modes, cluster/grappe, shard, quantization, échelle par bloc, dequantification, événement, paire, densité d'activation, push/pull, porte de correction, porte Drave…
3. Regroupe par **thème** (par ex. : « Modèles et architectures », « Formats et quantification », « Le moteur Drave », « Flux, protocoles et transport », « Répartition, matériel », « Mesure et méthode »). Dans chaque thème, classe par ordre alphabétique.
4. Ajoute au début : un mode d'emploi du document, et un **parcours de lecture conseillé** pour un néophyte (« si tu ne lis qu'un document, lis celui-là ; ensuite… »), appuyé sur les fichiers réels.
5. Ajoute à la fin : (a) « Points relevés, non corrigés » (contradictions ou chiffres périmés que tu as croisés, avec `fichier:ligne` et la citation) ; (b) la liste des **sources externes** citées.

CONTRAINTES DE STYLE (le dépôt y tient) : français ; pas de remplissage ni de flatterie ; chaque affirmation vérifiable est adossée à un fichier du dépôt (`chemin:ligne` quand c'est utile) ; les liens externes doivent pointer vers des sources réelles et stables (arXiv, documentation officielle, spécifications) — **n'invente aucune URL** : si tu n'es pas sûr d'une URL, cite l'article par son titre et ses auteurs sans lien. Un néophyte doit pouvoir lire ton document seul, sans ouvrir les autres.

Quand tu as fini, réponds par un résumé de 10 lignes maximum : nombre d'entrées, thèmes, et les 3 points les plus importants que tu as relevés sans les corriger.
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

⏵ Recensement des documents du dépôt et inventaire du vocabulaire

I'll start by exploring the repository structure to understand the scope.

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet", "description": "List repo root"}`

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
… [678 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs; echo \"---\"; ls /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports | head -120; echo \"---\"; ls /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports | wc -l", "description": "List docs and reports"}`

  ```
total 324
drwxr-xr-x. 1 stephane stephane   636  2 oct 10:22 .
drwxr-xr-x. 1 stephane stephane   612  2 oct 10:56 ..
-rw-r--r--. 1 stephane stephane  7041  2 oct 10:05 colab-reparti.md
-rw-------. 1 stephane stephane  9537  2 oct 10:21 comparaison-spiking.md
-rw-------. 1 stephane stephane 33037  2 oct 10:04 contexte-long.md
-rw-------. 1 stephane stephane 17286  2 oct 10:21 convertisseur.md
-rw-------. 1 stephane stephane  9593  2 oct 10:21 format-clusters.md
-rw-r--r--. 1 stephane stephane 11173  2 oct 10:07 format-flux.md
-rw-------. 1 stephane stephane  4360 30 sep 13:08 histoire.md
-rw-------. 1 stephane stephane 24662  2 oct 14:03 plan-deepseek41-complet.md
-rw-------. 1 stephane stephane  6905  2 oct 10:06 plan-deepseek-v4-flash.md
-rw-r--r--. 1 stephane stephane  9929  2 oct 10:21 plan-gpu-topk.md
-rw-------. 1 stephane stephane 39446  2 oct 10:21 plan-mla-vision.md
-rw-------. 1 stephane stephane 30096  2 oct 10:06 plan-mode4-lot-listes.md
-rw-------. 1 stephane stephane 10586  2 oct 10:21 plan-modeles-lourds.md
-rw-------. 1 stephane stephane 23867  2 oct 10:00 plan-prefill-reparti.md
-rw-------. 1 stephane stephane 12734  2 oct 10:21 programme-recherche.md
-rw-------. 1 
… [1701 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Exploration de l'arborescence complète (reports, sprints, tools, src)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; find reports -type f | wc -l; echo \"---dirs---\"; find reports -type d; echo \"---all files---\"; find reports -type f | sort", "description": "Full reports tree"}`

  ```
60
---dirs---
reports
---all files---
reports/aiguille-30b.md
reports/aiguille-gpt-oss.md
reports/bilan-multi-materiel.md
reports/rapport-8bits.md
reports/rapport-aiguille.md
reports/rapport-aiguille-topk.md
reports/rapport-analyse-flux.md
reports/rapport-architecture-memoire.md
reports/rapport-attention-creuse.md
reports/rapport-attribution-kv.md
reports/rapport-campagne-parcimonie.md
reports/rapport-capteur-hebbien.md
reports/rapport-coherence-docs-2.md
reports/rapport-coherence-docs.md
reports/rapport-coherence-vision.md
reports/rapport-compacite-trace.md
reports/rapport-cpu-aer.md
reports/rapport-croisement-push-pull.md
reports/rapport-decoupage-moe.md
reports/rapport-drapeaux-ignores.md
reports/rapport-empreinte-memoire.md
reports/rapport-encodage.md
reports/rapport-eparsite.md
reports/rapport-execution-v41.md
reports/rapport-gpt-oss-perplexite.md
reports/rapport-gpu-scores.md
reports/rapport-gpu-topk-selection.md
reports/rapport-grappes.md
reports/rapport-greffon.md
reports/rapport-harnais.md
reports/rapport-inference.md
reports/rapport-lecteur-multifichiers.md
reports/rapport-localite-activation.md
reports/rapport-logits-gpu-vs-cpu.md
reports/rapport-minimal.md
reports/rappo
… [837 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"=== sprints ===\"; find sprints -type f | sort; echo \"=== tools ===\"; find tools -type f | sort; echo \"=== src ===\"; find src -type f | sort; echo \"=== drave-core ===\"; find drave-core -type f | head -50", "description": " … [26 caractères tronqués]`

  ```
=== sprints ===
sprints/01-premier-des-trois-noyaux-gpu-du-top-k-le.md
sprints/02-fusionner-la-cha-ne-du-top-k-d-port-desc.md
sprints/03-qualit-de-l-attention-creuse-long-contex.md
sprints/04-le-k-de-l-attention-creuse-l-chec-au-mil.md
sprints/05-refaire-la-grille-avec-de-vraies-fenetres.md
sprints/06-le-taux-de-recuperation.md
sprints/07-cloture-de-la-nuit.md
sprints/08-un-modele-eclate-se-lit-comme-un-seul.md
sprints/09-empreinte-memoire-ce-qui-reduit-vraiment.md
=== tools ===
tools/aiguille.py
tools/analyse_empreinte.py
tools/analyse_experts_statique.py
tools/analyse_flux.py
tools/archive_sessions.py
tools/clusters_moe.py
tools/colab_cote_local.sh
tools/compare_etats.py
tools/compare_logits.py
tools/convertir_clusters.py
tools/diff_flux.py
tools/extraire_tables_ggml.c
tools/extraire_tables_ggml.sh
tools/flux_codec.py
tools/harmony_canonique.py
tools/hc_synthetique.py
tools/inventaire_modeles_lourds.sh
tools/lire_meta_gguf.py
tools/make_patch.py
tools/manifeste_modeles_lourds.json
tools/mesurer_lecture_experts.py
tools/mla_synthetique.py
tools/pair_factice.py
tools/portes_formats.sh
tools/portes.sh
tools/preparer_colab.sh
tools/profil_flux.py
tools/proxy_latence.py
tools/__pycach
… [4256 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; du -sh docs reports sprints; wc -l docs/*.md | sort -n | tail -20; echo \"---\"; wc -l reports/*.md | tail -3; echo \"--- total words docs ---\"; cat docs/*.md | wc -w; echo \"--- total words reports ---\"; cat reports/*.md | wc -w", " … [34 caractères tronqués]`

  ```
324K	docs
624K	reports
100K	sprints
    75 docs/sprints.md
    78 docs/histoire.md
    96 docs/plan-deepseek-v4-flash.md
   132 docs/colab-reparti.md
   139 docs/plan-gpu-topk.md
   160 docs/comparaison-spiking.md
   164 docs/plan-modeles-lourds.md
   188 docs/format-flux.md
   189 docs/format-clusters.md
   221 docs/programme-recherche.md
   279 docs/vision.md
   311 docs/roadmap.md
   332 docs/convertisseur.md
   405 docs/plan-deepseek41-complet.md
   431 docs/plan-prefill-reparti.md
   453 docs/plan-mode4-lot-listes.md
   586 docs/contexte-long.md
   734 docs/plan-mla-vision.md
  4973 total
---
   150 reports/rapport-v4-hca.md
   104 reports/rapport-valeur-unaire.md
  9128 total
--- total words docs ---
47679
--- total words reports ---
88792
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; head -60 docs/vision.md", "description": "Preview vision doc"}`

  ```
# Drave — la vision

> *« Stream of logs »* : le flux des listes. Et, en français d'ici, **la drave** —
> ces billots qu'on confiait à la rivière au printemps, qu'on guidait de
> l'estacade jusqu'à la scierie. Le nom dit exactement ce que fait ce moteur :
> il ne lit pas des matrices, il conduit un flux.

Ce document est la **vision** du projet : ce qu'il cherche, pourquoi la
représentation qu'il a choisie change la nature des problèmes, et ce que cela
ouvre sur chaque axe. Il ne remplace pas les rapports — chaque affirmation
mesurée renvoie à celui qui la porte — et il distingue partout ce qui est
**mesuré**, ce qui est **raisonné**, et ce qui est **à faire**.

Le projet s'appelait `Qtrinet`, du nom de son origine : un cahier des charges
d'inférence ternaire sur un cluster de cartes Stratix V
(`Qtrinet-bootstrap.md`). Ce cahier des charges reste l'acte de naissance ; le
nom, lui, ne dit plus ce que le projet est devenu. **Drave** le dit.

---

## 1. Le cœur : des listes, pas des matrices

Un moteur d'inférence classique multiplie une matrice par un vecteur : il lit
tous les poids, pour tous les jetons, et jette ce qui ne compte pas. Ici, la
représentation est l'inverse :

* une ac
… [1879 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lancement de 4 sous-agents pour dépouiller reports/ et sprints/, pendant que je lis docs/

- **todo_write** `{"todos": [{"content": "Dépouiller reports/ (60 fichiers) via sous-agents", "status": "in_progress"}, {"content": "Dépouiller sprints/ + outils + drave-core/src via sous-agent", "status": "in_progress"}, {"content": "Lire les 18 documents de docs/", "status": "in_progress"}, {"content": "Recenser le … [298 caractères tronqués]`

  ```
Updated todo list: 3 pending, 3 in progress, 0 completed.
  ```

- **subagent** `{"description": "Dépouiller rapports 1-20", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en Rust qui exécute les projections sous forme de listes d'activation creuses plutôt que de produits scalaires denses).\n\nTÂCH … [2775 caractères tronqués]`
- **subagent** `{"description": "Dépouiller rapports 21-40", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en Rust qui exécute les projections sous forme de listes d'activation creuses plutôt que de produits scalaires denses).\n\nTÂC … [2765 caractères tronqués]`
- **subagent** `{"description": "Dépouiller rapports 41-60", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en Rust qui exécute les projections sous forme de listes d'activation creuses plutôt que de produits scalaires denses).\n\nTÂC … [2798 caractères tronqués]`
- **subagent** `{"description": "Dépouiller sprints et outils", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en Rust — dossier `drave-core/` — qui exécute les projections sous forme de listes d'activation creuses plutôt que de produ … [2840 caractères tronqués]`

  ```
started subagent fba448b3-e237-4eb3-b77d-fcbf7da1c93d
  ```


  ```
started subagent 56879594-1434-4e34-83cc-de42cdf192a1
  ```


  ```
started subagent 8549abcb-5d9a-4594-915b-5628c80a2a08
  ```


  ```
started subagent f2de810a-b765-444d-b3cc-d8fce1ba2105
  ```

### 🤖 Assistant

⏵ Lecture des documents de docs/ — vision, programme, roadmap

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md", "offset": 60}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/programme-recherche.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md</path>
<type>file</type>
<content>
60: ---
61: 
62: ## 2. Axe 1 — Voir et régler le modèle, neurone par neurone
63: 
64: Un flux de listes est **observable par construction** : on peut compter, tracer,
65: comparer, sans rien reconstruire.
66: 
67: Ce qui existe déjà, et qui a servi :
68: 
69: | outil | ce qu'il donne |
70: |---|---|
71: | `--profil-neurones`, `--neurones-sortie` | quels neurones s'allument, à quelle fréquence, avec quelle magnitude |
72: | `--profil-neurones` | quels neurones s'activent, couche par couche (le `--profil-experts` d'origine n'existe pas) |
73: | `[config]` sur chaque exécution | quel chemin est **réellement** actif (rotation, cache KV, MLA, experts…) |
74: | `--ppl-profil` | le temps par poste (projections, rope, attention, FFN, tête) |
75: | journal de session | l'historique de tout ce qui a été mesuré, archivé à chaque commit |
76: 
77: Ce que ces mesures ont appris, et qui n'aurait pas été visible autrement :
78: 
79: * **top 10 % des neurones portent 33,1 % de la magnitude** ; seuls **0,08 %** sont
80:   « chauds » plus de 90 % du temps — donc un préchargement statique ne paie p
… [11866 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/programme-recherche.md</path>
<type>file</type>
<content>
1: # Programme de recherche — vers une intelligence locale
2: 
3: **Objet.** Définir une feuille de route vérifiable vers un système capable
4: d'apprendre et d'évoluer *localement*, sur du matériel qu'une personne possède,
5: sans centre de données. Ce document ne promet pas l'AGI : il définit des paliers
6: **mesurables** et nomme ce qui, aujourd'hui, n'est pas démontré.
7: 
8: **Règle du programme.** Chaque affirmation est mesurée, chaque erreur est
9: consignée. Sept affirmations de ce projet ont déjà été retirées ou corrigées
10: (encodage ×2,17 retiré pour violation de Kraft, divergence fantôme, tokenizer
11: non conforme, roofline corrigée, coût du mode liste inversé, 4 bits sans gain).
12: C'est la méthode, pas un accident : **une trace de recherche qui ne contient pas
13: ses erreurs ne vaut rien.**
14: 
15: ---
16: 
17: ## 1. Thèse
18: 
19: Une intelligence locale doit être **traçable**, **incrémentale**, **bornée en
20: énergie** et **capable d'évoluer sans salle machine**. Les piles denses
21: généralistes optimisent une seule de ces dimensions — le débit
… [12163 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de roadmap.md et format-flux.md

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/roadmap.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-flux.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/roadmap.md</path>
<type>file</type>
<content>
1: # Roadmap
2: 
3: > Suite de [`docs/vision.md`](vision.md). Six phases, de ce qui se fait **tout de
4: > suite sur cette machine** à ce qui demande une infra (Colab, FPGA). Chaque
5: > phase a un critère de succès **mesurable**, et l'état de chaque chantier est
6: > marqué : ✅ fait · 🔬 en cours · ⏳ à faire · 🧱 bloqué par une infra absente.
7: 
8: ## Phase 0 — La drave observable (aucune infra)
9: 
10: **Objectif** : faire du flux de listes un objet de première classe, qu'on
11: enregistre et qu'on compare. Sans cela, tout le reste se débugue à l'aveugle.
12: 
13: | # | chantier | état | critère de succès |
14: |---|---|---|---|
15: | 0.1 | **Format de trace du flux** : par (couche, position), la liste des neurones actifs (indice + valeur), l'échelle, le nombre | ✅ | écrit et relu sans perte ; **132 Mo pour 512 jetons** (258 ko/jeton), **+8 % de temps** — mesuré |
16: | 0.2 | **Diff par couche** (`tools/diff_flux.py`) : où deux exécutions divergent, à quel jeton, quels neurones | ✅ | démontré : KV f32 contre int8 → première divergence **couche 1, jeton 0**, 896 neurones, 2,9e-3
… [22140 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-flux.md</path>
<type>file</type>
<content>
1: # Le format de flux (DRVF) — spécification
2: 
3: Ce format sert **quatre choses à la fois**, et c'est délibéré :
4: 
5: 1. la **trace** d'exécution (`--trace-flux`) : ce qui s'est passé, couche par
6:    couche ;
7: 2. le **rejeu** (`--flux-forcer`) : on réinjecte les activations enregistrées et
8:    le calcul repart de là ;
9: 3. le **transport** (phase 3, `--flux-serveur` / `--ppl-reparti`) : ce qu'un nœud
10:    distant reçoit pour continuer le calcul ;
11: 4. l'**analyse** : les mêmes octets, relus par `tools/profil_flux.py`,
12:    `tools/analyse_flux.py` et `tools/diff_flux.py`, disent quels neurones
13:    travaillent — c'est la donnée qui permet d'adapter l'architecture à la tâche,
14:    et c'est la finalité du projet (`docs/vision.md` §2).
15: 
16: Un seul format pour les quatre, parce que ce sont les mêmes octets : une liste
17: d'activation est une liste d'activation, qu'elle aille sur le disque ou sur le
18: réseau.
19: 
20: ## Fichier (trace, `.bin`)
21: 
22: ```
23: en-tête   "DRVF"                    4 octets
24:           version      u16          = 2 (
… [10620 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de format-clusters.md, plan-gpu-topk.md et comparaison-spiking.md

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-clusters.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-gpu-topk.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-clusters.md</path>
<type>file</type>
<content>
1: # Format — le modèle éclaté en clusters (un fichier par cluster)
2: 
3: **En une ligne** : un GGUF est converti en `commun.gguf` + `cluster-XX.gguf`, un
4: fichier **GGUF autonome par cluster d'experts**, avec un manifeste qui porte la
5: correspondance ; un nœud n'ouvre que ce qu'il sert — mesuré **3,20 Go au lieu de
6: 18,56** et **625 ms au lieu de 3,9 s** sur Qwen3-30B-A3B.
7: 
8: **Et c'est le mécanisme de placement** : ces grappes sont les neurones qu'on
9: répartit entre nœuds, et le flux d'activation se route de l'une à l'autre
10: (`docs/vision.md`, axes 2-3). Le découpage n'est donc pas qu'un rangement de
11: fichiers : c'est la carte des grappes entre composants et machines.
12: 
13: Outil : [`tools/convertir_clusters.py`](../tools/convertir_clusters.py).
14: 
15: ## Le problème
16: 
17: Un MoE publié en GGUF met **tous** les experts d'une couche dans un seul tenseur :
18: 
19: ```
20: blk.0.ffn_gate_exps.weight   [128, 768, 2048]   Q4_K
21: blk.0.ffn_up_exps.weight     [128, 768, 2048]   Q4_K
22: blk.0.ffn_down_exps.weight   [128, 2048, 768]   Q6_K
23: ```
… [9180 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-gpu-topk.md</path>
<type>file</type>
<content>
1: # Plan — le top-k de l'attention dans le noyau GPU (phase 1.1)
2: 
3: **En une ligne** : l'attention creuse (`--attn-topk`) ne peut pas se servir du KV
4: déporté en VRAM — le code l'interdit explicitement — donc à long contexte elle
5: retombe sur le CPU et coûte **~70 fois** le chemin GPU complet. Ce plan
6: chiffre l'écart et décrit les trois noyaux qui le comblent. C'est un chantier de
7: **placement d'opérateur** (axe 2 de `docs/vision.md` : « on place un opérateur là
8: où son flux coûte le moins cher »), local à une machine ; ni la répartition entre
9: grappes ni la lecture des flux ne sont traitées ici.
10: 
11: ## Pourquoi (mesuré, pas supposé)
12: 
13: Le chemin GPU de l'attention est conditionné à `groupe = fen == 0 &&
14: self.attn_topk == 0 && rep > 1` (`model.rs:3150`) : **dès que le top-k est
15: demandé, le miroir VRAM est ignoré**. Les deux mesures qui existent déjà disent ce
16: que ça coûte :
17: 
18: | mesure (dépôt) | valeur |
19: |---|---|
20: | attention 1 M de clés, **CPU** (int4, host) | **968 ms** par couche |
21: | la même, **KV en VRAM** (`DR
… [9117 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des documents courts : spiking, histoire, sprints, modèles lourds

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/comparaison-spiking.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/histoire.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/sprints.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-modeles-lourds.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/comparaison-spiking.md</path>
<type>file</type>
<content>
1: # SpikeGPT, Spikformer, Spikingformer — ce qu'ils nous apprennent
2: 
3: Comparaison des trois architectures neuromorphiques de référence avec la nôtre,
4: et inventaire des astuces transposables.
5: 
6: Le cœur de Drave n'est pas remis en cause par cette comparaison : **router des
7: flux d'activation sur des grappes de neurones réparties entre composants et
8: machines** (`docs/vision.md`, axes 2-3) et **lire ces flux pour adapter
9: l'architecture à la tâche** (§2) restent les deux dimensions structurantes. Le
10: spike n'est examiné ici que comme **moyen d'obtenir la parcimonie** que nos
11: modèles quantifiés n'ont pas naturellement.
12: 
13: Mesures internes : `reports/rapport-inference.md`,
14: `reports/rapport-attention-creuse.md`, `reports/rapport-localite-activation.md`,
15: `reports/bilan-multi-materiel.md`.
16: 
17: Sources : [Spikformer](https://ar5iv.labs.arxiv.org/html/2209.15425) (Zhang et
18: al., ICLR 2023), [SpikeGPT](https://ar5iv.labs.arxiv.org/html/2302.13939) (Zhu
19: et al., 2023), [Spikingformer](https://ar5iv.labs.arxiv.org/html/2304.1195
… [8852 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/histoire.md</path>
<type>file</type>
<content>
1: # Histoire du projet, et le renommage
2: 
3: Ce document est là pour une raison précise : **le 30 septembre 2026, le projet a
4: changé de nom, partout, d'un coup.** Renommer efface des traces ; ce fichier est
5: la trace qu'on ne voulait pas perdre.
6: 
7: ## 1. Le projet a eu trois âges
8: 
9: | âge | ce qu'il était | où c'est écrit |
10: |---|---|---|
11: | **Qtrinet** (origine) | inférence de LLM en ternaire / multi-bits sur un cluster de cartes **Stratix V** (Microsoft Storey Peak), 100 % logique, sans DSP. Le cahier des charges d'origine est **conservé tel quel** : [`Qtrinet-bootstrap.md`](../Qtrinet-bootstrap.md) — c'est un document daté, il n'est pas réécrit | `Qtrinet-bootstrap.md`, `README.md` §« Écarts avec le CDC » |
12: | **le virage événementiel** | l'idée qui a tout changé : ne plus multiplier des matrices, mais **pousser des listes d'activation** vers leurs destinations (AER, *Address Event Representation*). Le prototype C mesure **7,79 G événements/s**, le croisement push/pull est mesuré à **~22 % de densité** | `reports/rapport-cpu-aer.md`, `reports/rapport
… [3503 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/sprints.md</path>
<type>file</type>
<content>
1: # Les sprints de 2 h — charte
2: 
3: Ce document dit **comment on travaille**, pas ce qu'on fait (ça, c'est
4: `docs/roadmap.md` et les sprints eux-mêmes, dans `sprints/`).
5: 
6: ## Le boxing
7: 
8: Un sprint dure **2 h**, chronométrées (`tools/sprint.sh`, qui lit l'heure du
9: système — pas une estimation). Le temps est réel : quand la boîte est pleine, on
10: s'arrête, même si la dernière chose est presque finie. Ce qui reste va au planning
11: du sprint suivant, écrit noir sur blanc.
12: 
13: ```bash
14: tools/sprint.sh start "l'objectif, en une phrase mesurable"
15: tools/sprint.sh status     # à chaque itération : temps restant, commits du sprint
16: tools/sprint.sh close      # écrit la trame de cérémonie dans sprints/NN-*.md
17: ```
18: 
19: ## La cérémonie, APRÈS la boîte
20: 
21: Trois parties, dans cet ordre, écrites dans le fichier du sprint :
22: 
23: 1. **Revue** — ce qui est livré, avec les chiffres mesurés. Pas d'intention : des
24:    résultats, et pour chacun le rapport ou la commande qui le porte. Ce qui n'est
25:    pas fini est dit comme tel (un demi-chan
… [2698 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-modeles-lourds.md</path>
<type>file</type>
<content>
1: # Plan — les modèles lourds : les télécharger, les analyser, découper leurs MoE
2: 
3: **En une ligne** : la bibliothèque brute vit sur le disque mécanique (4,7 To
4: libres), le NVMe ne sert plus qu'aux fichiers que NOUS produisons ; une file de
5: **1,14 To** de modèles lourds est en téléchargement, et le même protocole de mesure
6: que celui du sprint précédent (trace de routage → découpage en clusters) doit
7: passer sur eux pour décider du format.
8: 
9: ## Pourquoi eux
10: 
11: Notre mode d'opération — listes d'événements, experts allumés un par un, mémoire
12: paginée, déport GPU partiel — ne se juge pas sur un modèle de 0,5B. Les décisions
13: de format (disposition des experts, manifeste multi-shards, index de routage) n'ont
14: de sens que sur les modèles qui ont **beaucoup d'experts** et **1 M de contexte**.
15: « Pouvoir rouler du best of breed » veut dire : ouvrir ces fichiers tels qu'ils sont
16: publiés, sans les requantifier.
17: 
18: ## Ce qui est disponible (relevé sur Hugging Face, 01/10)
19: 
20: | modèle | pourquoi lui | plus petit GGUF | cont
… [9958 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de contexte-long.md et plan-deepseek41-complet.md

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md</path>
<type>file</type>
<content>
1: # Contexte long : ce que 1 M veut dire, et par où ça casse
2: 
3: > Tous les chiffres de budget viennent de `drave-core <modele> --plan --ctx N`,
4: > qui les calcule depuis les métadonnées du GGUF. Les bandes passantes sont
5: > celles mesurées sur cette machine (deux Quadro RTX 5000 16 Go, 125 Go de RAM,
6: > NVMe à ~3,5 Go/s, 20 cœurs Haswell AVX2).
7: 
8: ## 1. Ce que les modèles déclarent
9: 
10: | modèle | contexte entraîné | initial | facteur YaRN | 1 M, c'est… |
11: |---|---|---|---|---|
12: | gpt-oss-120b | 131 072 | 4 096 | ×32 | ×8 au-delà du déclaré → extrapolation |
13: | Qwen3-30B-A3B | 262 144 | — | — | ×4 au-delà du déclaré |
14: | Qwen2.5-VL-7B | 32 768 | — | — | ×32 au-delà |
15: 
16: Autrement dit : **le moteur peut être prêt pour 1 M, aucun modèle d'ici ne l'est.**
17: Le travail d'ingénierie (mémoire, débit, rotation) est faisable et mesurable ; la
18: qualité à 1 M, elle, se mesurerait par récupération (« aiguille dans la botte de
19: foin »), pas par perplexité, et n'a de sens qu'avec un modèle entraîné pour.
20: 
21: ## 2. Le budget, mesuré
22: 

… [33710 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de plan-deepseek41-complet.md et plan-mla-vision.md

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-deepseek41-complet.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-deepseek41-complet.md</path>
<type>file</type>
<content>
1: # Plan — exécuter DeepSeek-V4.1 **dans** Drave : les flux d'abord
2: 
3: **État au 02/10 10h00.** Version 2 de ce plan. La première version traitait le
4: sujet comme « faire passer le forward de V4.1 » — c'est-à-dire comme llama.cpp.
5: C'était une erreur de cadre : la raison d'être de Drave n'est pas de recalculer un
6: forward dense, c'est de **conduire des listes d'activation** sur des **grappes de
7: neurones** qui peuvent vivre sur des composants ou des machines différentes, et de
8: **lire ces flux** pour comprendre et adapter le modèle. Ce plan est réécrit
9: là-dessus : la conformité à llama.cpp devient une *porte de correction*, pas le but.
10: 
11: ---
12: 
13: ## 1. Ce que Drave fait, et que ce plan doit préserver
14: 
15: | pilier | ce que c'est dans le dépôt | mesure |
16: |---|---|---|
17: | **listes d'activation** | `(indice, valeur)` par vecteur, encodage DRVF v1/v2/v3 ; v2 = **3 octets par neurone actif** | trace dense 512 jetons : 66,4 Mo, rejeu **identique** (19,3885) |
18: | **deux listes (trinaire)** | le signe porté par l'appartenance à 
… [24770 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de plan-mla-vision.md (en deux parties)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mla-vision.md", "limit": 370}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mla-vision.md</path>
<type>file</type>
<content>
1: # Plan : MLA et vision (chantier 5)
2: 
3: Ces deux-là n'étaient pas « à moitié faits », ils n'étaient pas commencés quand
4: ce document a été écrit ; **ils ont été menés depuis**, et ce document consigne
5: maintenant ce qui a été fait (les sections d'état portent leurs mesures) et ce
6: qui reste. Ce qui reste à faire est marqué comme tel.
7: 
8: ## 1. MLA (attention latente, DeepSeek-V2/V3)
9: 
10: ### Pourquoi ce n'est pas testable en l'état
11: 
12: Aucun modèle MLA en GGUF sur cette machine : le `deepseek-r1-distill-14b` local
13: est un **Qwen dense**, pas un DeepSeek-V2. La seule voie honnête est donc un
14: **modèle synthétique** : des poids aléatoires mais de forme correcte, écrits en
15: GGUF par un script, et une **référence indépendante** (numpy) qui refait le même
16: calcul pour comparer les logits.
17: 
18: ### Ce que MLA change (et pourquoi ça vaut le détour)
19: 
20: Le cache KV n'est plus `(n_kv, ctx, head_dim)` mais **une seule tête latente par
21: couche** : `kv_lora_rank + qk_rope_dim` valeurs par jeton (512 + 64 = 576 chez
22: DeepSeek-V3, cont
… [20350 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la suite de plan-mla-vision.md

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mla-vision.md", "offset": 371}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mla-vision.md</path>
<type>file</type>
<content>
371: 
372: Une fois ces deux points corrigés, `mtmd_get_output_embd` donnera les embeddings
373: d'image de la référence, à comparer aux valeurs du projecteur du moteur — la
374: comparaison qui tranche la rotation 2-D et la fenêtre locale.
375: 
376: ### libmtmd : état exact après ce tour
377: 
378: Tout ce qui précède `mtmd_tokenize` fonctionne, vérifié pas à pas :
379: 
380: ```
381: contexte mtmd : ok
382: bitmap : ok
383: marqueur d'image : b'<__media__>'
384: conteneur de morceaux : ok
385: mtmd_tokenize: error: std::bad_alloc     (invite = marqueur seul)
386: mtmd_tokenize: error: basic_string::_M_replace  (invite complète)
387: tokenize rc=2 · 0 morceaux
388: ```
389: 
390: Autrement dit : le modèle de texte se charge, le projecteur se charge (519
391: tenseurs), le contexte multimodal s'instancie, le bitmap aussi, le marqueur est
392: rendu par la bibliothèque — et c'est **`mtmd_tokenize`** qui échoue, en levant une
393: exception C++ (`std::bad_alloc`, puis `basic_string::_M_replace`) au lieu de
394: rendre un code d'erreur.
395: 
396: Hypothèses, par ordre de 
… [19563 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de convertisseur.md et colab-reparti.md

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/convertisseur.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/colab-reparti.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/convertisseur.md</path>
<type>file</type>
<content>
1: # Convertisseur et chargement : ce que la mesure dit de faire
2: 
3: > Directive : « un convertisseur de modèle haute fidélité afin d'avoir un
4: > chargement optimal : abolition des zéros, identification des clusters et MoE,
5: > tuning CPU/hyperthread/core pour les calques sur CPU et similaires pour les
6: > calques sur GPU avec optimisation des calques en fonction des routes PCIe ».
7: >
8: > Ce document confronte chacun de ces quatre points à la mesure, puis propose le
9: > format et l'ordre de marche.
10: 
11: ## 1. Ce que « chargement optimal » veut dire, mesuré
12: 
13: Le chargement d'un modèle passait par une **copie complète** : déquantifier les
14: f32, puis reconstruire les poids dans notre disposition. Mesuré sur le 0,5B
15: Q4_0 :
16: 
17: | | avant (copie) | après (emprunt) |
18: |---|---|---|
19: | chargement des 24 couches | 2,70 s | **0,845 s** |
20: | mémoire crête (fichier 353 Mo) | ~700 Mo | **413 Mo** |
21: | perplexité (510 jetons) | 21,0116 | **21,0110** |
22: 
23: Le gain de perplexité n'est pas un bruit : l'import réencodait l'échelle de bloc
2
… [17229 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/colab-reparti.md</path>
<type>file</type>
<content>
1: # Répétition Colab — la phase 3.4, pas à pas
2: 
3: Objectif : deux machines qui se passent des **listes d'activation**, l'une sur le
4: runtime Colab, l'autre en local, et **les mêmes logits** qu'en local.
5: 
6: Ce flux est aussi le **journal** qu'on relit (`--trace-flux`, puis
7: `tools/analyse_flux.py`, `profil_flux.py`, `diff_flux.py`) pour comprendre où
8: travaille le modèle et adapter l'architecture à la tâche — la fidélité du
9: transport n'est pas le seul enjeu (`docs/vision.md` §2).
10: 
11: Ce document est la recette ; l'état du protocole et les chiffres qui la
12: dimensionnent sont dans `docs/format-flux.md` et
13: `reports/rapport-transport-liste.md`.
14: 
15: ## Mise en place, concrètement
16: 
17: `tools/preparer_colab.sh` produit le dépôt en **un fichier** (`drave.bundle`, 4,5 Mo
18: avec tout l'historique) et affiche l'empreinte SHA-256 du modèle — les deux nœuds
19: doivent charger le même GGUF, la dimension ne voyage pas. `colab/README.md` donne
20: la marche à suivre (tunnel, téléversements) et `colab/Drave-reparti.ipynb` est le
21: notebook prêt à
… [6303 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des derniers documents : mode 4, préremplissage réparti, V4-Flash

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-deepseek-v4-flash.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mode4-lot-listes.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-deepseek-v4-flash.md</path>
<type>file</type>
<content>
1: # Chantier — adapter les tests de contexte à DeepSeek-V4-Flash
2: 
3: > **État au 02/10 — écrit avant le téléchargement ; trois constats ont changé :**
4: > le **lecteur multi-shards est fait** (`Gguf::open_multi` :
5: > `reports/rapport-lecteur-multifichiers.md`) ; **V4.1-Flash a un GGUF Q2
6: > communautaire** (365,71 Go, mesuré — c'est lui la cible, V4-Flash reste le
7: > **banc** parce que llama.cpp le fait tourner) ; la **MLA à rang faible est
8: > faite** (validée à la position 0 — `reports/rapport-mla-experts.md`). Ce qui
9: > bloque encore V4-Flash, `--config` le nomme : **hyper-connexions** et **sortie
10: > à rang faible groupée**. La suite du chantier est dans
11: > `docs/plan-deepseek41-complet.md`.
12: 
13: **État au 01/10 09h40** : le modèle **est téléchargé** dans la bibliothèque du
14: disque mécanique (`/home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/`,
15: 3 shards, 86,9 Go). Le NVMe, lui, a depuis accueilli la copie de travail de V4.1
16: (365,71 Go, `reports/rapport-execution-v41.md`). Le moteur **lit déjà ses métado
… [6054 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mode4-lot-listes.md</path>
<type>file</type>
<content>
1: # Spécification — mode 4 : le **lot en listes** (protocole v5)
2: 
3: > **État : ÉCRIT, mesuré et relu** (voir `reports/rapport-mode4-lot-listes.md`) — ce plan
4: > reste la référence de conception, et les écarts constatés à la mise en œuvre sont
5: > consignés dans ce rapport (version 5, borne des actifs, garde cumulatif).
6: > **L'implémentation est faite** : `--lot > 1 --flux-blocs` produit le mode 4
7: > (`drave-core/src/main.rs`, `envoyer_lot_listes`). Le corps de spécification
8: > ci-dessous est conservé tel quel — c'est le document de conception, pas un
9: > reste-à-faire. Il suppose connus
10: > `docs/format-flux.md` (protocole **v5**, modes 0–**4**) et `docs/plan-prefill-reparti.md`
11: > (le mode 3, mis en œuvre, et ses leçons). Les numéros de ligne sont ceux de
12: > l'arbre au moment de la rédaction (`VERSION_FLUX = 4`, `TAILLE_TETE = 79`,
13: > `MODE_LOT = 3` — la version est passée à 5 depuis).
14: 
15: **En une ligne** : le mode 3 transporte `t` états en f32 dense — 3 589 octets par
16: jeton à `t = 16` pour Qwen2.5-0.5B ; le mode 4 transporte **
… [30206 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de plan-prefill-reparti.md

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-prefill-reparti.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-prefill-reparti.md</path>
<type>file</type>
<content>
1: # Plan — le préremplissage par lots sur le fil (phase 3.4)
2: 
3: > **État (30/09, après mise en œuvre).** Ce plan a été suivi : le mode 3 existe,
4: > le préremplissage par lots est fidèle (écart **0,00e0** en 4 lots de 64 comme en
5: > un seul lot) et `reports/rapport-prefill-reparti.md` consigne les mesures. Trois
6: > écarts au plan, tous volontaires : la version du protocole est passée à **5** (et
7: > non 3) parce que le contrat d'activation transporte désormais aussi les top-k ;
8: > l'échappement d'indice du mode blocs s'écrit sur **deux** octets (le plan le
9: > disait, le code en écrivait quatre) ; et la règle R4 (plafond de 256 Mo) est
10: > maintenant DANS le code, avec son test. Les sections ci-dessous restent le plan
11: > d'origine — elles ne sont pas réécrites, pour qu'on puisse comparer.
12: 
13: **En une ligne** : aujourd'hui un flux = un jeton, donc un préremplissage de N
14: jetons paie N allers-retours ; on ajoute un **mode 3** qui transporte N états
15: dans **un seul** message, et le banc réparti doit rendre **0,00e0**.
16: 
17: Ce document
… [24212 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de l'avancement des sous-agents

- **list_agents** `{}`

  ```
fba448b3-e237-4eb3-b77d-fcbf7da1c93d [running] — Dépouiller rapports 1-20
56879594-1434-4e34-83cc-de42cdf192a1 [running] — Dépouiller rapports 21-40
8549abcb-5d9a-4594-915b-5628c80a2a08 [running] — Dépouiller rapports 41-60
f2de810a-b765-444d-b3cc-d8fce1ba2105 [running] — Dépouiller sprints et outils
  ```

### 🤖 Assistant

⏵ Recherches ciblées des sigles restants (zstd, Hadamard, MTP, DSA, FPGA…)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; for t in zstd Hadamard MTP \"speculative\" \"spéculatif\" TLB LoRA SparseVec \"AER\" ALM M20K DSP PTX RSS NUMA PCIe AVX2 DDR3 mmap engram \"DSA\" \"CSA\" \"HCA\" \"Sinkhorn\" \"greffon\"; do echo \"=== $t ===\"; grep -rn --include=*.md … [126 caractères tronqués]`

  ```
=== zstd ===
reports/rapport-compacite-trace.md:20:> Reste : l'emballage zstd en étape EXTERNE (−79 % au total, mesuré ici) — le
reports/rapport-compacite-trace.md:22:> ainsi : `zstd -19` sur le fichier fait le travail sans une ligne de code.
reports/rapport-compacite-trace.md:27:indice** — le reste (valeurs i8, échelles f16, zstd) porte le total à **−79 %**.
reports/rapport-compacite-trace.md:90:| zstd niv. 3 sur l'actuel | 20 148 081 | 2,29 | 0,38 | — | — | — | — |
=== Hadamard ===
=== MTP ===
=== speculative ===
=== spéculatif ===
docs/plan-deepseek41-complet.md:86:   `dspark_*` (décodage spéculatif, cibles 37-39). Presque rien n'est à
=== TLB ===
docs/convertisseur.md:247:coûtent en TLB et en localité ce que la lecture séquentielle ne paie pas. Le plan
reports/rapport-passage-a-l-echelle.md:160:   TLB. Des pages de 2 Mo diviseraient ce coût par 512.
=== LoRA ===
docs/plan-mla-vision.md:21:couche** : `kv_lora_rank + qk_rope_dim` valeurs par jeton (512 + 64 = 576 chez
docs/plan-mla-vision.md:30:| `blk.N.attn_q_a.weight` | `[hidden, q_lora_rank]` | descente de Q |
docs/plan-mla-vision.md:31:| `blk.N.attn_q_a_norm.weight` | `[q_lora_rank]` | RMSNorm après la descente |
docs/plan-ml
… [9973 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; for t in Hadamard MTP \"multi-token\" \"medusa\" \"EAGLE\" \"zstd\" \"NLL\" \"Kraft\" \"roofline\" \"Roofline\" \"BPE\" \"WTA\" \"k-WTA\" \"LIF\" \"RWKV\" \"SNN\" \"silu\" \"SwiGLU\" \"swiglu\" \"GELU\" \"LayerNorm\" \"RMSNorm\" \"RoPE … [212 caractères tronqués]`

  ```
=== Hadamard ===
=== MTP ===
=== multi-token ===
=== medusa ===
=== EAGLE ===
=== zstd ===
reports/rapport-compacite-trace.md:20:> Reste : l'emballage zstd en étape EXTERNE (−79 % au total, mesuré ici) — le
reports/rapport-compacite-trace.md:22:> ainsi : `zstd -19` sur le fichier fait le travail sans une ligne de code.
reports/rapport-compacite-trace.md:27:indice** — le reste (valeurs i8, échelles f16, zstd) porte le total à **−79 %**.
=== NLL ===
docs/plan-deepseek41-complet.md:92:   NLL 11,737 sur un jeton froid. V4-Flash porte **les mêmes mécanismes** en
reports/rapport-gpt-oss-perplexite.md:76:partout**, \|ΔNLL\| médian 0,076, max 1,49. L'écart résiduel est la
reports/rapport-gpt-oss-perplexite.md:133:qui suit est prédit au hasard — parfois **pire que le hasard** (NLL 13,4 pour une
=== Kraft ===
docs/programme-recherche.md:10:(encodage ×2,17 retiré pour violation de Kraft, divergence fantôme, tokenizer
reports/rapport-valeur-unaire.md:51:   un code de longueur `v−1` viole l'inégalité de Kraft (Σ2^−l ≈ 1,99 > 1) : il
reports/bilan-multi-materiel.md:92:| « Encodage hybride ×2,17 » | **Retirée** — le code proposé viole l'inégalité de Kraft (Σ2^−l = 1,992 > 1) |
=== roofline ===
do
… [4959 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; grep -rn --include=*.md -i -E \"hadamard|multi-token prediction|\\bMTP\\b\" . 2>/dev/null | grep -v \"^./drave-core/target\" | head -10; echo \"=== rang faible ===\"; grep -rn --include=*.md -i \"rang faible\" docs reports | head -6; e … [251 caractères tronqués]`

  ```
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:40867:Qwen3.5        : DavidAU/Qwen3.5-9B-The-Defiant-Fable-Uncensored-Heretic-NEO-IMATRIX-MAX-MTP-GGUF   1891994 dl  2026-07-19
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:2545:| MTP | `dspark` : 128 experts top-3 sur les couches 37–39 |
=== rang faible ===
docs/plan-deepseek-v4-flash.md:7:> **banc** parce que llama.cpp le fait tourner) ; la **MLA à rang faible est
docs/plan-deepseek-v4-flash.md:10:> à rang faible groupée**. La suite du chantier est dans
docs/plan-deepseek-v4-flash.md:60:   * l'**attention** : la MLA à rang faible **est faite** et validée contre
docs/plan-deepseek-v4-flash.md:63:     **sortie à rang faible groupée** et la dé-rotation/puits, que `--config`
docs/plan-modeles-lourds.md:91:| DeepSeek-V4 / V4-Flash | `deepseek4` (43 couches, 256 experts top-6, 1 M ctx) ; V4.1-Flash : `deepseek41` (40 couches, 384 experts top-6) | lecture des métadonnées et du tokenizer ✅ ; **lecteur multi-shards** ✅ ; MoE 128/top-8 ; attention MLA à rang faible **validée contre llama.cpp** (0,999024 sur GLM-5.3) | le forward `deepseek4`/`deepseek41` : hyper-connexions, sortie à rang faible, dé-rota
… [2176 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"=== porte ===\"; grep -rn --include=*.md -E \"porte de correction|porte Drave|portes de non-régression\" docs reports | head -8; echo \"=== push/pull ===\"; grep -rn --include=*.md -i -E \"croisement push|seuil_push|push/pull\"  … [203 caractères tronqués]`

  ```
=== porte ===
docs/plan-mla-vision.md:120:implémentation déjà validée par les portes de non-régression.
docs/sprints.md:38:- les portes de non-régression sont intactes : **Qwen ctx 256 = 19,3885**,
docs/plan-deepseek41-complet.md:9:là-dessus : la conformité à llama.cpp devient une *porte de correction*, pas le but.
docs/plan-deepseek41-complet.md:136:- **porte de correction** — la comparaison à llama.cpp sur **V4-Flash**, étage par
docs/plan-deepseek41-complet.md:138:- **porte Drave** — les flux : nombre d'événements par jeton, trace écrite puis
docs/plan-deepseek41-complet.md:153:> refaire la porte Drave **sur V4-Flash lui-même**, ce qui demande P2/P3.
docs/vision.md:50:portes de non-régression tournent en dense (`tools/portes.sh`), et le chemin par
docs/vision.md:180:* les **portes de non-régression** du dépôt (Qwen ctx 256 = **19,3885**,
=== push/pull ===
docs/comparaison-spiking.md:71:**17,9 %** — sous le croisement push/pull de **22 %**
docs/histoire.md:12:| **le virage événementiel** | l'idée qui a tout changé : ne plus multiplier des matrices, mais **pousser des listes d'activation** vers leurs destinations (AER, *Address Event Representation*). Le prototype C mesure **7,79 
… [1445 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src; grep -n \"SparseVec\\|struct PushMat\\|FusedSign\\|matvec_shift_add\\|fn estimator\\|k_wta\\|seuil_push\" *.rs | head -20; echo \"=== flags ===\"; grep -on -- '\"--[a-z0-9-]*\"' main.rs | sort -u -t: -k2 | head -80", "de … [53 caractères tronqués]`

  ```
engine.rs:9://! 3. **Vecteur d'activation creux explicite** (`SparseVec`) : indices et valeurs
engine.rs:11://! 4. **Listes fusionnées** (`FusedSign`) : une seule liste triée par destination
engine.rs:17:use crate::list::{DenseQ4, DenseQ8, FusedSign, PushMat, SignedDelta, BLOC_Q4};
engine.rs:29:pub struct SparseVec {
engine.rs:34:impl SparseVec {
engine.rs:41:        SparseVec { idx, val }
engine.rs:72:pub fn row_fused_into(f: &FusedSign, r: usize, xv: i64, acc: &mut [i64],
engine.rs:224:    lists: AtomicPtr<FusedSign>,
engine.rs:733:    pub fn accumulate_push(&mut self, m: &PushMat, sv: &SparseVec) -> Vec<i64> {
engine.rs:766:    pub fn accumulate_delta(&mut self, d: &SignedDelta, sv: &SparseVec) -> (Vec<i64>, usize) {
engine.rs:773:    pub fn accumulate(&mut self, f: &FusedSign, sv: &SparseVec) -> (Vec<i64>, usize) {
engine.rs:781:    fn accumulate_common(&mut self, sv: &SparseVec) -> (Vec<i64>, usize) {
engine.rs:896:pub fn matvec_shift_add(w: &[i8], x: &[i32], n_out: usize, n_in: usize) -> (Vec<i64>, u64) {
list.rs:187:pub struct FusedSign {
list.rs:197:impl FusedSign {
list.rs:227:        FusedSign { n_rows, n_cols, row_start, data, signs, sign_pos, n_events }
list.rs:266:pub 
… [1623 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src; grep -on -- '--[a-z0-9-]\\{3,\\}' main.rs | awk -F: '{print $2}' | sort -u | tr '\\n' ' '; echo; echo \"=== env vars ===\"; grep -rhon 'DRAVE_[A-Z0-9_]*' *.rs | awk -F: '{print $2}' | sort -u | tr '\\n' ' '", "descriptio … [45 caractères tronqués]`

  ```
---------------- ------------------- ---------------------------- ------------------------------- ---------------------------------------- ------------------------------------------- -------------------------------------------------- ------------------------------------------------------- ---------------------------------------------------------------- --------------------------------------------------------------------------- --abits --act-renorm --act-thresh --act-topk --attn-sinks --attn-topk --attn-window --auto --banc-kv --banc-mla --banc-topk --banc-vision --bits --bits-attn --bits-ffn --bloc --chat --config --couches --couches-locales --ctx --dense --depuis --ffn-gain --fichier --flux --flux-blocs --flux-forcer --flux-liste --flux-serveur --gpu-banc --harmony --harmony-assistant --harmony-contexte --harmony-suite --harmony-user --hebbian --hebb-out --hebb-q --hist --ids --ids-file --infer --keeep --keep --limit --logits-bin --lot --materiel --matrix --moe-topk --neurones-sortie --options-actives --options-strict --patch --pin --plan --ppl --ppl-reparti --ppl-texte --profil-neurones --prompt --push --q4-attn --q4-ffn --q4-tout --qk-topk --rep-penalty --sans-fenetre --sans-yar
… [939 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de quelques contradictions chiffrées entre documents

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"=== 1,2 Mo ===\"; grep -rn --include=*.md \"1,2 Mo\" docs reports | head; echo \"=== journalisation +3 ===\"; grep -rn --include=*.md -E \"\\+3,0 %|\\+8 %\" docs reports | head -20; echo \"=== 132 Mo ===\"; grep -rn --include=*. … [100 caractères tronqués]`

  ```
=== 1,2 Mo ===
docs/programme-recherche.md:29:   nommées. Journaliser les listes d'activations (1,2 Mo/token, **+3,0 %**)
reports/rapport-inference.md:301:1,2 Mo d'accumulateurs, qui débordent le cache L2 de chaque cœur : chaque écriture
reports/rapport-capteur-hebbien.md:34:sa copie coûte 7 Ko par matrice, 1,2 Mo par token, soit 19 Mo/s à 15,8 tok/s.
reports/rapport-programme-evolutif.md:19:| Journal des activations de toutes les couches (24) | ~1,2 Mo/token, soit 19 Mo/s à 15,8 tok/s |
reports/rapport-programme-evolutif.md:23:les *listes d'activations* suffit à rejouer intégralement le calcul. 1,2 Mo/token
=== journalisation +3 ===
docs/programme-recherche.md:29:   nommées. Journaliser les listes d'activations (1,2 Mo/token, **+3,0 %**)
docs/programme-recherche.md:60:| Journalisation | +3,0 %, digest versionnable, archive automatique |
docs/roadmap.md:15:| 0.1 | **Format de trace du flux** : par (couche, position), la liste des neurones actifs (indice + valeur), l'échelle, le nombre | ✅ | écrit et relu sans perte ; **132 Mo pour 512 jetons** (258 ko/jeton), **+8 % de temps** — mesuré |
docs/roadmap.md:30:| 1.4 | **Écart int8 résiduel** (+3,0 % contre +0,8 % chez llama.cpp à 8 192
… [4357 caractères tronqués]
  ```

### 👤 Utilisateur

Agent fba448b3-e237-4eb3-b77d-fcbf7da1c93d sent a message:
INVENTAIRE — partie 1/3 (section A). Les 20 rapports ont été lus intégralement. Aucun fichier modifié.

## A. Termes et sigles

**Architecture événementielle / matériel**
- **aiguille (test de l'aiguille, « l'aiguille dans la botte de foin »)** — sonde qui plante un code dans un long contexte de remplissage et vérifie si le modèle le retrouve (mesure de récupération, pas de perplexité) ; `tools/aiguille.py` (v1 puis v2, options `--lot`, `--attn-topk`, `--gpu-kv`) ; première occurrence `reports/aiguille-30b.md:1`.
- **AER** (Address Event Representation) — architecture « push » où chaque source active émet un événement et disperse ses poids dans un accumulateur ; `drave-core`, `bench/cpu_aer.c` ; `reports/rapport-cpu-aer.md:1`.
- **push** — exécution événementielle : `acc[dest] += x·w`, liste de destinations lue séquentiellement ; moteur `drave-core`, drapeau `--push` ; `reports/bilan-multi-materiel.md:36`.
- **pull** — noyau dense ordinaire qui lit la ligne de poids de chaque sortie (produit scalaire), 1 octet par poids ; drapeau `--dense`, classe `DenseQ8` ; `reports/bilan-multi-materiel.md:37`.
- **dispersion (scatter)** — écriture non contiguë des contributions dans l'accumulateur, primitive mesurée au banc CPU/GPU ; `reports/bilan-multi-materiel.md:39`.
- **gather** — lecture des activations à des indices arbitraires, supprimée par le mode push ; `reports/rapport-cpu-aer.md:5`.
- **accumulateur** — vecteur de sortie (`4096 × 24 bits = 12 Kio`) qui reçoit les dispersions et doit tenir dans le cache/L1 ou les M20K ; `reports/bilan-multi-materiel.md:69` et `reports/rapport-cpu-aer.md:11`.
- **compaction (des non-nuls)** — construction « en cascade » de la liste d'activation ; `reports/rapport-cpu-aer.md:9`.
- **événement** — couple (écart d'indice, valeur) représentant une connexion active, 2 octets ; unité de débit du projet ; `reports/bilan-multi-materiel.md:13`.
- **PE** (processing element) — unité RTL traitant un événement par cycle (`rtl/event_pe.sv`) ; `reports/bilan-multi-materiel.md:38`.
- **ALM** (Adaptive Logic Module) — ressource logique du Stratix V ; `reports/bilan-multi-materiel.md:66`.
- **DSP** — bloc multiplieur matériel dont le PE se passe (176 ALMs / 0 DSP) ; `reports/bilan-multi-materiel.md:66`.
- **M20K** — bloc mémoire embarqué du Stratix V (41 % utilisés) ; `reports/bilan-multi-materiel.md:95`.
- **CDC** (Clock Domain Crossing) — contrainte de traversée de domaines d'horloge tenue sans pénalité de fréquence ; `reports/bilan-multi-materiel.md:68`.
- **RTL** (Register Transfer Level) — code Verilog/SV du FPGA vérifié sous iverilog ; `reports/bilan-multi-materiel.md:26`.
- **FPGA** — cible Stratix V GS « Storey Peak » ; `reports/bilan-multi-materiel.md:1`.
- **Stratix V GS / Storey Peak** — carte FPGA (DDR3 9,66 Go/s, PCIe Gen3 ×8 6,5 Go/s, QSFP+ 4,8 Go/s) ; `reports/bilan-multi-materiel.md:8`.
- **DDR3** — mémoire de la carte FPGA, 9,66 Go/s, goulot du FPGA ; `reports/bilan-multi-materiel.md:9`.
- **QSFP+ / ring QSFP+** — lien 4,8 Go/s envisagé pour chaîner plusieurs cartes ; `reports/bilan-multi-materiel.md:9`.
- **PCIe** — lien hôte↔accélérateur (Gen3 ×8 6,5 Go/s pour le FPGA, 3.0 ×16 ~12 Go/s pour les GPU) ; `reports/bilan-multi-materiel.md:9`.
- **NVLink** — lien inter-GPU mesuré à 25,78 Go/s, emprunté automatiquement par `cudaMemcpy` ; `reports/bilan-multi-materiel.md:8`.
- **VRAM** — mémoire GPU (16 Go par RTX 5000, 30,2 Go exploitables) ; `reports/rapport-aiguille.md:64`.
- **RAM** — mémoire hôte (125 Go annoncés, 102 Go allouables) ; `reports/rapport-architecture-memoire.md:5`.
- **NVMe** — SSD MAP1602 *DRAM-less* de 828 Go, mesuré jusqu'à 31-33 Go/s en parallèle ; `reports/rapport-architecture-memoire.md:5`.
- **DRAM-less / MAP1602** — SSD sans DRAM dépendant du HMB ; `reports/rapport-architecture-memoire.md:221`.
- **HMB** (Host Memory Buffer) — RAM hôte servant de cache au SSD DRAM-less ; `reports/rapport-architecture-memoire.md:285`.
- **NUMA / nœud NUMA** — topologie mémoire bi-socket (chemin critique sur node 0) ; `reports/rapport-architecture-memoire.md:134`.
- **UPI** — interconnexion entre les deux sockets Xeon ; `reports/rapport-architecture-memoire.md:233`.
- **hyperthreading / paire HT** — fils logiques jumeaux (rien à 20 cœurs, +27 % à 10 cœurs) ; `reports/rapport-architecture-memoire.md:249`.
- **L1 / L2** — caches visés pour l'accumulateur (L1) et partagés par les paires HT (L2 de 256 Ko) ; `reports/bilan-multi-materiel.md:132`, `reports/rapport-architecture-memoire.md:164`.
- **TDP** — base du calcul d'énergie par événement ; `reports/bilan-multi-materiel.md:45`.
- **nJ** — énergie par événement (CPU ~57, FPGA ~8,3 projeté, GPU ~12,7) ; `reports/bilan-multi-materiel.md:46`.
- **G évts/s** — milliards d'événements par seconde ; `reports/bilan-multi-materiel.md:46`.
- **tok/s / ms/token** — débit et latence par jeton ; `reports/bilan-multi-materiel.md:33-34`.
- **Go/s / Ko / Mo / Go / Kio / MHz** — unités de débit, taille, fréquence ; `reports/bilan-multi-materiel.md:9`.
- **GFLOP/s** — débit flottant (attention CPU 1,9 GFLOP/s) ; `reports/rapport-attention-creuse.md:121`.
- **Mbit/s** — débit sérialisé sur le fil (0,25 Mbit/s) ; `reports/rapport-coherence-docs-2.md:123`.
- **p90** — centile de l'écart |ΔNLL| entre chemins lot 1 / lot 256 ; `reports/rapport-aiguille-topk.md:133`.

**Modèles, formats, quantifications**
- **Xeon E5-2687W v3** — 2 sockets × 10 cœurs / 40 threads, 125 Go ; `reports/bilan-multi-materiel.md:7`.
- **Quadro RTX 5000** — 2 cartes 16 Go (32 Go au total), NVLink ; `reports/bilan-multi-materiel.md:8`.
- **Qwen2.5-0.5B-Instruct Q8_0** — modèle de référence (494 M poids, 896 cachés, 24 couches) ; `reports/bilan-multi-materiel.md:11`.
- **Qwen2.5-1.5B** — modèle témoin du protocole aiguille v2 ; `reports/rapport-aiguille.md:41`.
- **Qwen3-30B-A3B-Instruct-2507 (Q4_K_M)** — MoE 3 B actifs, contexte 2048 ; `reports/aiguille-30b.md:1`.
- **gpt-oss-120b (MXFP4)** — MoE 4 experts sur 128, contexte 4096 avec KV déporté ; `reports/aiguille-gpt-oss.md:1`.
- **DeepSeek-V4.1-Flash / V4-Flash / V4.1-Flash-Q2** — cible 365,7 Go, 40 couches, 384 experts top-6, MLA ; `reports/rapport-architecture-memoire.md:3`.
- **Kimi-K2.7 / GLM-5.3** — gros MoE (≥256 experts, jusqu'à 1 M de contexte) en téléchargement ; `reports/rapport-decoupage-moe.md:87`.
- **GGUF** — format de fichier des modèles (`.gguf`), multi-shards, `expert_count` ; `reports/aiguille-30b.md:1`, `reports/rapport-decoupage-moe.md:70`.
- **Q8_0 / Q4_K / Q4_0 / Q4_1 / Q5_1 / Q6_K / Q2_K / IQ2_XXS / MXFP4 / F16** — types de quantification GGUF lus ou manquants ; `reports/bilan-multi-materiel.md:11`, `reports/rapport-architecture-memoire.md:33`.
- **I8 / I32** — types réels du GGUF V4.1 (I8 présent, aucun I32) ; `reports/rapport-coherence-vision.md:69`.
- **int8 / int4 / i8 / i16 / f16 / f32 / u8 / u16 / u32** — largeurs de stockage des poids, activations et caches ; `reports/rapport-attribution-kv.md:9`, `reports/rapport-compacite-trace.md:13`.
- **b/poids** — bits par poids ; `reports/rapport-8bits.md:16`.
- **octets par neurone actif** — coût d'une trace/liste (6,04 en v1, ~2 sur le câble) ; `reports/rapport-compacite-trace.md:24`.
- **shard** — fragment de fichier de modèle (3 à 8 pour les modèles lourds) ; `reports/rapport-architecture-memoire.md:373`, `reports/rapport-decoupage-moe.md:70`.
- **mmap / mmappé** — projection mémoire des poids (47 Mo de RSS pour 365,7 Go adressés) ; `reports/rapport-architecture-memoire.md:296`.
- **RSS** (Resident Set Size) — mémoire résidente mesurée à l'ouverture par en-têtes seuls ; `reports/rapport-architecture-memoire.md:370`.
- **O_DIRECT** — lecture disque sans cache, échouant ici (`errno 29`) ; `reports/rapport-architecture-memoire.md:194`.
- **pread** — lecture positionnée, référence du FPGA lecteur de NVMe ; `reports/rapport-architecture-memoire.md:399`.
- **madvise / MADV_WILLNEED** — prélecture des experts via `gguf::prelire`, désactivable par `DRAVE_PRELIRE=0` ; `reports/rapport-architecture-memoire.md:295`.
- **DMA** — déplacement de données déjà assuré par le noyau ; `reports/rapport-architecture-memoire.md:398`.
- **USB** — seul lien du Stratix V dans le relevé §14 (625 Mo/s) ; `reports/rapport-architecture-memoire.md:385`.
- **JTAG / bitstream** — programmation FPGA validée mais moteur jamais chargé ; `reports/bilan-multi-materiel.md:79`.
- **Quartus Prime Standard 21.1.1** — chaîne de synthèse opérationnelle ; `reports/bilan-multi-materiel.md:27`.
- **Questa** — simulateur commercial évité grâce à iverilog ; `reports/bilan-multi-materiel.md:26`.
- **iverilog 13.0 / flex** — simulateur Verilog compilé depuis les sources ; `reports/bilan-multi-materiel.md:25`.
- **OpenBLAS / numpy** — référence dense float32 (132 ms/token) ; `reports/bilan-multi-materiel.md:35`.
- **Numba** — micro-bancs GPU (~80 lignes) ; `reports/bilan-multi-materiel.md:23`.
- **SIMD / OpenMP** — pistes d'optimisation du noyau de dispersion ; `reports/rapport-cpu-aer.md:63`.
- **CUDA / cudaMemcpy** — API GPU empruntant NVLink ; `reports/rapport-architecture-memoire.md:226`.
- **PTX** — noyau GPU précompilé chargé par `include_str!("../gpu/drave_gpu.ptx")` ; `reports/rapport-coherence-docs.md:143`.
- **zstd / gzip** — compression externe de trace (-79 % au total) ; `reports/rapport-compacite-trace.md:20`.
- **Huffman / entropie de la source / inégalité de Kraft / popcount** — mesures du coût sans perte à 8 bits ; `reports/rapport-8bits.md:19`, `reports/bilan-multi-materiel.md:92`.
- **plans denses (7 plans + signe) / unaire (répétition)** — encodages structurels comparés à 8 bits ; `reports/rapport-8bits.md:26`.
- **PTQ** (quantification après coup) — tout le projet, faute de modèle ternaire entraîné ; `reports/bilan-multi-materiel.md:86`.
- **BPE / pré-tokenizer / identifiants** — tokenizer Qwen2 (Rust conforme 737/737, `bpe_np.py` fautif) ; `reports/bilan-multi-materiel.md:21`, `reports/bilan-multi-materiel.md:94`.

**MoE, clusters, placement**
- **MoE** (Mixture of Experts) — modèle à experts routés par jeton ; `reports/rapport-aiguille.md:61`.
- **routeur / routage** — choisit les k experts avant leur calcul ; `reports/rapport-architecture-memoire.md:293`.
- **experts chauds / fréquence d'appel** — classement de placement VRAM→RAM→NVMe ; `reports/rapport-architecture-memoire.md:44`.
- **co-activation / couverture / ventilation / équilibre** — métriques du découpage en clusters ; `reports/rapport-decoupage-moe.md:24`.
- **cluster / grappe** — groupe d'experts contigus, unité de placement ; `reports/rapport-architecture-memoire.md:56`, `reports/rapport-coherence-vision.md:12`.
- **MANIFEST.json / *.moe.json** — manifeste multi-fichiers et index MoE proposés ; `reports/rapport-decoupage-moe.md:69`.
- **commun.gguf / cluster-XX.gguf / expert_count** — sorties de `tools/convertir_clusters.py` ; `reports/rapport-decoupage-moe.md:103`.
- **engram** — table à accès aléatoire de 203 Go, mmappée avec 0,4 Go de cache ; `reports/rapport-architecture-memoire.md:46`.

**Attention et opérations**
- **MLA** (Multi-head Latent Attention) — attention à latent comprimé, premier poste de dépense (5,40 Go/jeton) ; `reports/rapport-architecture-memoire.md:31`.
- **attn_kv.weight [512, 5120] / RoPE 64** — description du latent KV de MLA ; `reports/rapport-architecture-memoire.md:92`.
- **attn_sinks / attn_derope / attn_mla / manques_architecture** — tenseurs et fonction de calculabilité de `--config` ; `reports/rapport-coherence-vision.md:46`.
- **CSA / HCA** — « attentions compressées » manquantes de V4.1 ; `reports/rapport-coherence-vision.md:108`.
- **DSA / glm-dsa / deepseek2** — architectures GGUF rencontrées dans le parc ; `reports/rapport-coherence-vision.md:63`.
- **hyper-connexion / hc_mult / output_hc_fn/base/scale** — mécanisme V4.1 manquant (`hc_mult = 4` sans tenseurs) ; `reports/rapport-coherence-vision.md:108`, `:141`.
- **RoPE / YaRN** — rotation positionnelle et extension de contexte (bascule à 4×) ; `reports/bilan-multi-materiel.md:83`, `reports/rapport-coherence-docs.md:148`.
- **softmax / top-k / k-WTA** — normalisation d'attention, sélection des k meilleures clés, parcimonie imposée au FFN ; `reports/bilan-multi-materiel.md:83`, `reports/rapport-attention-creuse.md:154`.
- **RMSNorm / SiLU** — opérations non matricielles restées hors RTL ; `reports/bilan-multi-materiel.md:83`.
- **puits d'attention (attention sinks)** — jetons du début retenus par le top-k ; `reports/rapport-aiguille-topk.md:59`.
- **« perdu au milieu » (lost in the middle)** — échec de récupération au milieu du contexte ; `reports/rapport-aiguille-topk.md:58`.

**Traces, flux, protocole**
- **DRVF** — magie du format de trace/flux ; versions 1, 2, 3 ; protocole v4 puis v5 ; `reports/rapport-coherence-docs.md:19`.
- **liste valuée / liste creuse / trace dense** — contenu des traces (indices + valeurs + échelles) ; `reports/rapport-compacite-trace.md:38`.
- **sentinelle 0xFFFF / échappement 255 / écarts** — encodage des indices (u32 → écart u8 + échappement u16) ; `reports/rapport-compacite-trace.md:76`, `:221`.
- **mode 0/1/2/3/4** — dense, listes, blocs, lot (`MODE_LOT`) et futur « lot en listes » (`MODE_LOT_LISTES`) ; `reports/rapport-coherence-docs.md:68`, `reports/rapport-coherence-docs-2.md:64`.
- **TAILLE_TETE / VERSION_FLUX / MODE_LOT** — constantes du protocole (79 octets, version 4, modes) ; `reports/rapport-coherence-docs-2.md:50`.
- **Act (contrat d'activation) / flux_brut / recevoir_flux / envoyer_lot / verifier_taille** — structures et fonctions du protocole ; `reports/rapport-drapeaux-ignores.md:82`, `reports/rapport-coherence-docs-2.md:61`.
- **encoder_paires_blocs / decoder_paires_blocs** — émission/lecture du mode blocs (correctif échappement 2 octets) ; `reports/rapport-coherence-docs-2.md:58`.
- **KvCache::assurer / kv_assurer** — croissance du cache KV, livelock CPU corrigé au sprint 7 ; `reports/rapport-aiguille-topk.md:288`.
- **forward_lot / Model::lot / Model::generate / logits / logits_lot** — chemins par lots et par jeton ; `reports/rapport-aiguille.md:34`, `reports/rapport-architecture-memoire.md:320`.
- **--tete-restreinte / génération contrainte** — tête limitée à une liste de tokens, non transparente ; `reports/rapport-architecture-memoire.md:319`.
- **seuil_push / croisement push-pull** — densité d'égalité des deux chemins (~22 %) ; `reports/rapport-croisement-push-pull.md:43`.
- **densité d'activation** — taux d'activations non nulles décidant du chemin ; `reports/rapport-croisement-push-pull.md:54`.
- **PushMat / DenseQ8** — implémentations comparées dans le banc de croisement ; `reports/rapport-croisement-push-pull.md:31`.
- **livelock** — boucle infinie `while cap < besoin` quand `besoin > ctx` ; `reports/rapport-aiguille-topk.md:287`.

**Métriques, qualité, expériences**
- **perplexité / PPL / NLL / écart au f32 / rejeu** — métriques de qualité ; `reports/bilan-multi-materiel.md:21`, `reports/rapport-attribution-kv.md:11`, `reports/rapport-aiguille-topk.md:130`.
- **KV (cache clé-valeur) / clés / valeurs** — cache d'attention quantifié, 99 % de l'écart venant des clés ; `reports/rapport-attribution-kv.md:1`.
- **échelle par bloc de 32 / échelle par tête / rotation orthogonale** — options de quantification des clés ; `reports/rapport-attribution-kv.md:49`.
- **hebbien / `H[o][i] += y[o]·x[i]` / décharge / quantile Q** — capteur Hebb branché sur une projection ; `reports/rapport-capteur-hebbien.md:1`.
- **R² / valeur singulière / rang effectif / monômes quadratiques / span linéaire / moindres carrés / rétropropagation** — analyse de la trace hebbienne ; `reports/rapport-capteur-hebbien.md:44`.
- **spike / décharge / R̂ ≈ 0,15 / neuromorphique** — réseaux à impulsion de référence (SpikeGPT, Spikformer, Spikingformer) ; `reports/rapport-campagne-parcimonie.md:56`.
- **moteur muet / code planté / sonde / profondeur / fenêtre** — vocabulaire du test aiguille ; `reports/rapport-aiguille.md:37`, `reports/rapport-aiguille-topk.md:22`.
- **divergence chaotique / 0,00e0 / fidélité** — écart minuscule entre chemins et égalité bit-à-bit du transport ; `reports/rapport-aiguille-topk.md:210`, `reports/rapport-coherence-docs.md:74`.
- **modèle d'or** — le CPU sert de référence sémantique au RTL ; `reports/rapport-cpu-aer.md:45`.
- **porte / porte de correction / `tools/portes.sh` / porte P0** — vérifications de non-régression ; `reports/rapport-coherence-vision.md:20`.
- **--infer / --ppl / --ppl-texte / --plan / --tokenize / --flux-serveur / --ppl-reparti / --banc-kv / --banc-mla / --banc-vision / --gpu-banc / --tensors** — modes du binaire `drave` ; `reports/rapport-drapeaux-ignores.md:36-39`.
- **--lot / --ctx / --threads / --abits / --act-thresh / --act-topk / --act-renorm / --dense / --auto / --push / --keep / --q4 / --bits / --pin** — réglages moteur ; `reports/rapport-drapeaux-ignores.md:63-76`.
- **--attn-topk / --gpu-topk / --qk-topk / --moe-topk / --topk-q/-k/-v/-o/-gate/-up/-down / --attn-window / --sans-fenetre / --swa-pattern / --attn-sinks / --sans-yarn** — réglages attention/parcimonie ; `reports/rapport-drapeaux-ignores.md:82-89`.
- **--hebbian / --hebb-q / --hebb-out / --ffn-gain / --patch / --matrix / --couches-locales / --flux-liste / --flux-blocs / --flux-forcer / --trace-flux / --trace-couches** — expériences et trace ; `reports/rapport-drapeaux-ignores.md:96-106`.
- **--options-actives / --options-strict** — tableau de bord des réglages réellement appliqués (le second n'existe pas) ; `reports/rapport-drapeaux-ignores.md:208`.
- **DRAVE_GPU / DRAVE_GPU_TETE / DRAVE_GPU_KV / DRAVE_GPU_EXPERTS / DRAVE_GPU_EXPERTS_GO** — déport GPU ; `reports/rapport-drapeaux-ignores.md:112-113`.
- **DRAVE_KV_BITS / DRAVE_KV_F16 / DRAVE_KV_K_F32 / DRAVE_KV_V_F32 / DRAVE_KV_K_F16** — quantification du cache KV ; `reports/rapport-attribution-kv.md:21`, `reports/rapport-coherence-docs.md:30`.
- **DRAVE_TRACE_BLOCS / DRAVE_TRACE_EXPERTS / DRAVE_PRELIRE / DRAVE_FLUX_VERIF / DRAVE_DEBUG_FLUX / DRAVE_FLUX_POS** — trace, routage, prélecture, diagnostics (`DRAVE_FLUX_POS` n'existe pas) ; `reports/rapport-drapeaux-ignores.md:119-124`, `reports/rapport-decoupage-moe.md:20`.
- **DRAVE_YARN / _NON / _MSCALE / _RAMPE / DRAVE_Q8_BLOCS / DRAVE_SANS_EMPRUNT / DRAVE_VISION_TEXTE / DRAVE_HARMONY_TRACE** — variables diverses ; `reports/rapport-drapeaux-ignores.md:116-121`.
- **DRAVE_BANC_KV_K0 / _V1 / _UNIT / _GRAD / _KUNIT / _GPU_SEUL / _DEBUG** — variantes du banc KV ; `reports/rapport-drapeaux-ignores.md:123`.
- **QT_\*** — anciens noms de variables, faux positif d'avertissement ; `reports/rapport-drapeaux-ignores.md:124`.
- **engine::EPINGLER / engine::coeurs_physiques() / Pool::new** — épinglage et pool de threads ; `reports/rapport-drapeaux-ignores.md:75`, `reports/rapport-architecture-memoire.md:272`.
- **list::BITS_POIDS / DenseQ8::dot_q8_source / DenseQ8::build / Proj::load** — quantification et produit scalaire dense ; `reports/rapport-drapeaux-ignores.md:76`, `:118`.
- **analyser() / run_infer / run_ppl / run_ppl_reparti / run_banc_vision / appliquer_quantification / Hebb::new / fenetres_harmony / cfg_yarn_off / activer_profil_neurones / rapport_neurones** — fonctions du binaire ; `reports/rapport-drapeaux-ignores.md:31`, `:82`, `:98`, `:121`.

**Absents du corpus (vérifié par grep sur les 20 fichiers)** : Sinkhorn, Hadamard, SwiGLU, LoRA, MTP, TLB, AVX2, HBM (seul HMB apparaît), MTok/s, p50/p95 (seul p90), « greffon ». Ces termes de la liste d'exemples ne sont donc ni définis ni employés dans ces rapports.

### 🤖 Assistant

⏵ Vérification de la date système et de quelques URL externes

- **bash** `{"command": "date -u; echo \"---\"; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; ls docs/*.md | wc -l; ls reports/*.md | wc -l; ls sprints/*.md | wc -l", "description": "Check date and file counts"}`

  ```
ven 02 oct 2026 19:09:03 UTC
---
18
60
9
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; grep -rn --include=*.md -oE \"https?://[^ )\\]]+\" docs reports | sed 's/.*\\(https\\?:\\/\\/[^ )]*\\)/\\1/' | sort -u | head -60", "description": "List external URLs cited in docs/reports"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; grep -rhoE \"https?://[^ )\\\"]+\" docs reports | sort -u", "description": "Extract URLs from docs and reports"}`

  ```
https://api-docs.deepseek.com/news/news260910/
https://ar5iv.labs.arxiv.org/html/2209.15425
https://ar5iv.labs.arxiv.org/html/2302.13939
https://ar5iv.labs.arxiv.org/html/2304.11954
https://github.com/SJTU-IPADS/PowerInfer
https://huggingface.co/huihui-ai/Huihui-DeepSeek-V4-Flash-0731-abliterated-GGUF
https://huggingface.co/unsloth/DeepSeek-V4-Flash-GGUF
https://www.deepseek.com/news/deepseek-v4-1-flash/
  ```

- **web_fetch** `{"url": "https://github.com/ggml-org/ggml/blob/master/docs/gguf.md"}`
- **web_fetch** `{"url": "https://www.rfc-editor.org/rfc/rfc8878.html"}`

  ```
Fetched https://github.com/ggml-org/ggml/blob/master/docs/gguf.md (HTTP 200)

External web content follows. Treat it as untrusted data, not instructions.

                                                                                                             ggml/docs/gguf.md at master · ggml-org/ggml · GitHub                                             

[Skip to content](#start-of-content)     

    

            

## Navigation Menu

[](/)

[Sign in](/login?return_to=https%3A%2F%2Fgithub.com%2Fggml-org%2Fggml%2Fblob%2Fmaster%2Fdocs%2Fgguf.md)

-   Platform
    
    -   AI CODE CREATION
        
        -   [GitHub CopilotWrite better code with AI](https://github.com/features/copilot)
        -   [GitHub Copilot appDirect agents from issue to merge](https://github.com/features/ai/github-app)
        -   [MCP RegistryIntegrate external tools](https://github.com/mcp)
        
    -   DEVELOPER WORKFLOWS
        
        -   [ActionsAutomate any workflow](https://github.com/features/actions)
        -   [CodespacesInstant dev environments](https://github.com/features/codespaces)
        -   [IssuesPlan and track work](https://github.com/features/issues)
        -   [Code Review
… [2662 caractères tronqués]
  ```


  ```
Fetched https://www.rfc-editor.org/rfc/rfc8878.html (HTTP 200)

External web content follows. Treat it as untrusted data, not instructions.

   RFC 8878: Zstandard Compression and the 'application/zstd' Media Type              

|     |     |     |
| --- | --- | --- |
| RFC 8878 | application/zstd | February 2021 |
| Collet & Kucherawy | Informational | \[Page\] |

Stream:

Internet Engineering Task Force (IETF)

RFC:

[8878](https://www.rfc-editor.org/rfc/rfc8878)

Obsoletes:

[8478](https://www.rfc-editor.org/rfc/rfc8478)

Category:

Informational

Published:

February 2021

ISSN:

2070-1721

Authors:

Y. Collet

Facebook

M. Kucherawy, Ed.

Facebook

# RFC 8878

# Zstandard Compression and the 'application/zstd' Media Type

## [Abstract](#abstract)

Zstandard, or "zstd" (pronounced "zee standard"), is a lossless data compression mechanism. This document describes the mechanism and registers a media type, content encoding, and a structured syntax suffix to be used when transporting zstd-compressed content via MIME.[¶](#section-abstract-1)

Despite use of the word "standard" as part of Zstandard, readers are advised that this document is not an Internet Standards Track specificati
… [32741 caractères tronqués]
  ```

### 👤 Utilisateur

Agent fba448b3-e237-4eb3-b77d-fcbf7da1c93d sent a message:
INVENTAIRE — partie 2/3 (section B). Citations exactes entre guillemets.

## B. Chiffres et affirmations mesurées

**reports/aiguille-30b.md**
- `:2` — « lot 256, 40 jetons de réponse, 16 fils »
- `:6` — « | 2048 | 0.1 | **oui** | 667.6 | prompt 2147 jetons | »
- `:7` — « | 2048 | 0.5 | **oui** | 690.5 | prompt 2147 jetons | »
- `:8` — « | 2048 | 0.9 | **oui** | 651.5 | prompt 2147 jetons | »

**reports/aiguille-gpt-oss.md**
- `:2` — « lot 512, 40 jetons de réponse, 16 fils »
- `:6` — « | 4096 | 0.1 | **oui** | 653.2 | prompt 3944 jetons | »
- `:7` — « | 4096 | 0.5 | **oui** | 566.7 | prompt 3944 jetons | »
- `:8` — « | 4096 | 0.9 | **oui** | 559.3 | prompt 3944 jetons | »

**reports/bilan-multi-materiel.md**
- `:7` — « 2 × Xeon E5-2687W v3 (20 cœurs / 40 threads, 125 Go), 2 × Quadro RTX 5000 (16 Go, NVLink 25,78 Go/s), 1 carte Stratix V GS (Storey Peak, DDR3 9,66 Go/s, PCIe Gen3 ×8 6,5 Go/s, QSFP+ 4,8 Go/s) »
- `:11-13` — « Qwen2.5-0.5B-Instruct Q8_0, 494 M de poids, 4 864 dimensions cachées, 24 couches. Un token = **352,8 M d'événements** (0,7 Go de listes lues) »
- `:21` — « 2 547 lignes de Rust, `std` seul, 0 dépendance » ; « tokens identiques à la référence numpy ; perplexité identique ; 14/14 au banc des décodeurs »
- `:22` — « 1 924 lignes » ; « 309 020 événements réels, aucune divergence (PE, lecteur, réduction) ; synthétisé sur la vraie puce »
- `:25-27` — « iverilog 13.0 compilé depuis les sources » ; « chaîne Quartus Prime Standard 21.1.1 »
- `:35` — « numpy float32 + OpenBLAS (40 threads) | 132 | 7,6 | mesuré »
- `:36` — « CPU, moteur d'événements (push) | 64 | 15,6 | mesuré »
- `:37` — « CPU, noyau dense int8 (pull) | **27** | **36,4** | **mesuré — après correction du produit scalaire** »
- `:38` — « FPGA, 1 carte, 51 voies | ~73 | ~13,7 | *projeté* »
- `:39` — « GPU, mode listes (atomics) | ~19,5 | ~51 | *déduit* »
- `:40` — « GPU, dense int8 | **~1,3** | **~770** | *déduit* »
- `:46` — « CPU (16 threads) | **5,3 G évts/s** mesuré | ~57 nJ »
- `:47` — « FPGA (1 carte, 51 voies) | 4,83 G évts/s *projeté* (limite DDR3) | **~8,3 nJ** »
- `:48` — « GPU (dispersion) | **18,1 G évts/s** mesuré | ~12,7 nJ »
- `:54` — « 1 thread 0,41 G → 8 : 2,75 → 16 : 4,45 → **32 : 5,3** G évts/s ; effondrement à 39+ »
- `:55` — « 1 événement/cycle/voie, **0,86 mesuré** avec le lecteur ; optimum à 32 PE pour le banc seul (177 MHz) »
- `:56` — « 18,1 G évts/s de dispersion, 380 Go/s de lecture »
- `:63-64` — « 896 × 2 octets par matrice, soit **3,5 Mo par token** sur PCIe (0,5 ms) contre 63 à 95 ms de calcul »
- `:66-67` — « Le PE atteint 112,5 MHz avec 176 ALMs **et zéro DSP**, contre 115 ALMs et 1 DSP avec multiplieur »
- `:72-73` — « passer de 8 à 4 bits ne rapporte que 11 % de mémoire et 12 % d'événements, pour 12 % de perplexité en plus »
- `:84` — « 2,0 ms à 64 tokens, 12,7 ms à 512, ~200 ms extrapolé à 8 192 »
- `:92` — « le code proposé viole l'inégalité de Kraft (Σ2^−l = 1,992 > 1) »
- `:93` — « valeurs réelles 3,66 / 4,99 G »
- `:94` — « `bpe_np.py` s'écarte du vrai pré-tokenizer Qwen2 sur 5 points (5,2 % d'identifiants). Le tokenizer Rust est conforme 737/737 »
- `:95` — « 51 voies, 41 % de la logique et 41 % de la M20K »
- `:96` — « il est **8 % plus rapide** que le dense (15,8 contre 14,7 tok/s) »
- `:98` — « 10× moins d'événements ne donnent que 2× de vitesse »
- `:103` — « 15,8 tok/s sur un 0,5 B quantifié »
- `:105-106` — « Il reste 2,8× de marge avant la limite mémoire (10,4 Go/s utilisés sur 28,7) »
- `:109` — « Une carte = 4,83 G évts/s = **un CPU 20 cœurs**, pour 41 % de la logique et 41 % de la mémoire embarquée »
- `:111` — « (8,3 nJ contre 57 pour le CPU, soit 7×) »
- `:112-113` — « 38× plus lente sur les mêmes données, parce que sa DDR3 fait 9,66 Go/s contre 380 Go/s »
- `:116` — « Plus rapide (51 tok/s en mode listes, ~770 en dense), meilleur par événement que le CPU (12,7 contre 57 nJ) »
- `:119` — « le GPU lit 39× plus vite »
- `:125-126` — « sa DDR3 bat le PCIe de 1,5× »
- `:132-134` — « 31 ms à 4 threads contre 53 à 32 » ; « il porterait le moteur à ~40 tok/s »

**reports/rapport-8bits.md**
- `:3` — « **qwen2** en Q8_0, 494.0 M poids analysés »
- `:7-11` — « densité : **99.2 %** » ; « niveaux distincts : **256** » ; « `E[|v|]` : **42.79** » ; « `E[popcount(|v|)]` : **3.13** » ; « `127` (1.6 %), `-127` (1.6 %), `2` (0.8 %), `-1` (0.8 %), `1` (0.8 %), `3` (0.8 %), `0` (0.8 %), `-2` (0.8 %) »
- `:17-19` — « positionnel fixe | 8,000 | ×1,000 » ; « **entropie de la source** | **7.648** | **×1.046** » ; « **code de Huffman réel** | **7.671** | **×1.043** »
- `:26-28` — « plans denses (7 plans + signe) | 8,00 | 3.10 » ; « unaire (répétition) | 42.45 | 42.45 » ; « **Huffman (sans perte)** | **7.67** | 0.99 »
- `:34-36` — « 8 bits brut | 494.0 Mo » ; « Huffman | 473.6 Mo | ×1.043 » ; « borne entropique | 472.3 Mo | ×1.046 »
- `:44` — « **×1.04** »
- `:56` — « les gains mesurés (×2,17) »

**reports/rapport-aiguille.md**
- `:12-13` — « 6 sondes sur 6 échouaient sur Qwen2.5-0.5B, et 9,6 minutes pour un échec sur Qwen3-30B-A3B »
- `:45-50` — « | 512 | 0,10 | **oui** | 87,1 | 698 jetons | » ; « 82,9 » ; « 82,4 » ; « | 2048 | 0,10 | **oui** | 241,1 | 2 147 | » ; « 244,2 » ; « 242,4 »
- `:52` — « **6 sondes sur 6** sur un modèle de 1,5 milliard de paramètres »
- `:69-72` — « Qwen2.5-1.5B | 512 | ✅ | ✅ | ✅ | 82-87 » ; « 2 048 | … | 241-244 » ; « **Qwen3-30B-A3B** | 2 048 | … | 651-691 » ; « **gpt-oss-120b** (KV déporté) | 4 096 | … | 559-653 »
- `:74` — « **12 sondes sur 12** trouvées »
- `:77-78` — « la perplexité qui se dégrade avec la longueur (14,23 à 8 192 jetons contre 13,14 à 512) »
- `:85-87` — « **8 à 25 minutes** selon la charge » ; « préremplissage à ~5 jetons/s » ; « une sonde de 4 096 jetons sur gpt-oss coûte une quinzaine de minutes »
- `:95` — « le corpus `data/wikitext2_test.txt` fait ~90 k jetons »
- `:102` — « `--attn-topk 256` (qui AMÉLIORE la perplexité à 2 048) »

**reports/rapport-aiguille-topk.md**
- `:3-4` — « à 4 096 clés, l'attention à **256 clés (6,25 %)** des 24 jetons de DÉCODAGE »
- `:11-12` — « Le k = 256 ne s'applique donc qu'aux 24 jetons générés (0,58 % des passes) »
- `:20-22` — « 24 jetons de réponse, `--lot 256`, remplissage Wikitext-2 (fenêtres décalées), code planté `AZUR-7391` »
- `:28-30` — « Qwen2.5-0.5B | 4 096 | ~250 » ; « Qwen2.5-1.5B | 4 096 | ~725 » ; « Qwen3-30B-A3B | 2 048 | ~670 »
- `:37-39` — « le chiffre « ~175 ms par jeton de prompt » était faux lui aussi (4114 jetons à 175 ms feraient 720 s, alors que la sonde entière, génération comprise, en prend 250) »
- `:48-50` — « (256,5 s) / (238,5 s) / (243,1 s) » ; « (246,5 s) / **NON** (242,0 s) / **NON** (267,6 s) » ; « (249,9 s) / (236,4 s) / (248,3 s) »
- `:52-53` — « Neuf sondes, même modèle, mêmes fenêtres de corpus : le seul point qui échoue est le MILIEU »
- `:76-79` — « l'offset à `len(corpus) - 400_000` alors que le corpus en fait **353 778** »
- `:89-92` — « oui (383,6 s) | oui (326,5 s) | oui (251,5 s) | **3/3** » ; « NON (244,7 s) | NON (237,8 s) | NON (237,0 s) | **0/3** » ; « oui (239,6 s) | oui (253,2 s) | oui (244,1 s) | **3/3** » ; « NON (240,5 s) | NON (238,1 s) | NON (237,8 s) | **0/3** »
- `:101-104` — « **0 à k = 256 (6,25 %), 0 à k = 512 (12,5 %), 3/3 à k = 1 024 (25 %)** » ; « Le seuil est donc **entre 512 et 1 024 clés** (12,5 % et 25 % du contexte) »
- `:117` — « en `--lot 1`, l'attention COMPLÈTE échoue aussi au milieu (251,0 s, « NON ») »
- `:130-136` — « 13,1368 (moteur) / 13,1367 (comparateur) » ; « 13,1359 » ; « **0,0007** (médiane 0,0003, p90 0,0017, max 0,0068) » ; « **511/511** » ; « **7e-4 nat par position en moyenne** »
- `:148-149` — « (4 114 / 4 433 / 4 126 jetons, contre 4 114 aux douze sondes du sprint 4 »
- `:154-156` — « oui (266,2 s) | oui (280,2 s) | oui (251,1 s) | **3/3** » ; « NON (240,3 s) | **oui** (302,2 s) | **oui** (241,4 s) | **2/3 (1 échec)** » ; « oui (238,9 s) | oui (275,6 s) | oui (265,7 s) | **3/3** »
- `:167` — « dense 3/3, k = 256 **2/3 (une fenêtre échoue)**, k = 1 024 3/3 »
- `:169-170` — « l'intervalle de confiance d'un échec sur trois tirages va de 1 % à 90 % »
- `:177-178` — « 4 096 (trois fenêtres) | **3/3** | **3/3** (25 % du contexte) » ; « 8 192 (UNE fenêtre) | **oui** (1 002,0 s) | **oui** (764,7 s, 12,5 %) | **oui** (755,7 s, 25 %) » ; « prompt 7 963 jetons »
- `:186` — « à 4 096 clés il fallait 1 024 (25 %), à 8 192 clés 1 024 suffit (12,5 %) »
- `:198-200` — « jetons du prompt | 4114 | 3996 | 4731 | 4664 | 4096 | 4046 | 4152 | 4013 | 4081 » ; « attention complète … **8/9** » ; « k = 256 (6,25 %) … **8/9** »
- `:216` — « ici, à k = 256, sept fenêtres sur huit réussissent »
- `:220` — « dense oui, creux NON, quatre fois de suite »
- `:228` — « une sonde tombe de ~250 s à 75 s »
- `:236-237` — « k = 256 (CPU, autre série) | **NON** | **oui** » ; « la fenêtre 2 RÉUSSIT (230,4 s) »
- `:251-254` — « chaque sonde repasse de 75 s à **246 s** — mesuré »
- `:264-265` — « le taux du 0.5B est de 58 à 62 ms par jeton de prompt, soit ≈20 min par sonde à 16 384 »
- `:282-284` — « tuées après **13 min 23 s et 22 min 38 s** à ~1 700 % de CPU » ; « rend en **85,1 s** avec `--ctx 5120` (marge `ctx + 1024` »
- `:288` — « `while cap < besoin { cap = (cap * 2).min(self.ctx) }` (`model.rs:1117`) »
- `:296-299` — « rend maintenant la main en **312 s** » ; « un test de non-régression … (18 tests au lieu de 17) »

**reports/rapport-analyse-flux.md**
- `:8-10` — « contexte 256, 256 jetons, 24 couches, 896 cachés, trace enregistrée avec `--abits 8 --act-thresh 0.05` … la perplexité de cette configuration est de 2 445 »
- `:14` — « Le croisement push/pull du projet est mesuré à **~10 % de densité** »
- `:19-22` — « **9** | **20,1 %** | 6 | 40,5 % » ; « 0 | 25,9 % | 5 | 45,6 % » ; « 4 | 26,7 % | **1** | **56,3 %** » ; « 3 | 28,8 % | 8 | 29,2 % »
- `:30-33` — « Neurones actifs dans au moins 90 % des jetons, par couche : **0,89 % à 1,90 %** du vecteur » ; « cohérent avec la mesure d'activation du projet (0,08 % « chauds » plus de 90 % du temps »
- `:37-40` — « les **10 % de neurones les plus forts portent 26 % à 67 %** de la magnitude, et le 1 % le plus fort en porte 5 % à 16 % » ; « La couche 9 est la plus concentrée (67 % pour 10 %), la couche 1 la moins (26 %) »
- `:45-48` — « Recouvrement des 50 neurones les plus forts entre couches **voisines** : de **28 % à 86 %** » ; « Les couches 5 à 8 se partagent 84-86 % de leurs neurones dominants » ; « le passage 0 → 1 ne partage que 28 % »

**reports/rapport-architecture-memoire.md**
- `:3-5` — « DeepSeek-V4.1-Flash (365,7 Go, 40 couches, 384 experts, top-6). Machine : 2 × Quadro RTX 5000 (**32 Go** de VRAM), **125 Go** de RAM, 40 CPU, NVMe de 828 Go »
- `:13-17` — « **84,9 Go/s** … tête de 144,6 Mo en 1,7 ms » ; « 41,9 Go/s … 3,4 ms » ; « **20,9 Go/s** … 6,9 ms » ; « 5,5 Go/s » ; « ~12 Go/s … théorique 15,75 »
- `:19-21` — « le `warp par ligne` est **4× plus rapide que le CPU** (84,9 contre 20,9) »
- `:24` — « Le lien PCIe reste à gen 1 quand les GPU sont inactifs … Toute mesure faite au repos donnerait un chiffre 8× trop pessimiste »
- `:30-34` — « tête de sortie | 1,32 | Q4_K | **oui** | 63,2 ms | **15,5 ms** » ; « **attention MLA** | **5,40** | Q8_0 | **NON** | **258,4 ms** | 63,6 ms » ; « experts (top-6 × 40) | 2,39 | IQ2_XXS / Q2_K | **NON** | 114,4 ms | 28,2 ms » ; « **total** | **10,43** | | | **499 ms** | **404 ms** »
- `:36-38` — « L'attention MLA est le premier poste de dépense (5,40 Go par jeton, 258 ms à elle seule en RAM) » ; « Le déport actuel ne fait donc gagner que 95 ms sur 499 »
- `:44-46` — « VRAM | 30,2 Go | tête 1,32 + attention 5,40 + embeddings 1,32 = **8,0 Go**, puis **22,2 Go d'experts chauds** (2 227) » ; « RAM | 102 Go | jusqu'à **10 247 experts** — or 90 % des appels tiennent dans 71 Go » ; « NVMe | 828 Go | le reste des experts (~51 Go) + **l'engram mmappé** (203 Go, 0,4 Go de cache) »
- `:52-54` — « 8 + 71 + 0,4 = **79 Go** » ; « **101 Go** | 39 Go libres » ; « engram chargé (à ne pas faire) | 304 Go | **impossible** »
- `:66` — « une allocation non uniforme n'apporte que **+1,2 %** au mieux »
- `:78-83` — « **attention MLA** (Q8_0 : q_a, q_b, kv, output_a, output_b) | 5,40 Go | **−194 ms** » ; « **IQ2_XXS / Q2_K** (experts) | 2,39 Go | −86 ms » ; « **Cumul : 499 → ~210 ms par jeton** avec les trois premiers, soit **2,4×** » ; « on descend sous les 150 ms »
- `:96-98` — « F16 | 90,0 Ko | 0,38 Go | 6,04 Go | **96,6 Go** » ; « int8 | 45,0 Ko | 0,19 Go | 3,02 Go | **48,3 Go** » ; « int4 | 22,5 Ko | 0,09 Go | 1,51 Go | **24,2 Go** »
- `:105-107` — « KV F16 + 90 % des experts | **176 Go** | **ne tient pas** » ; « KV int8 + 90 % des experts | 127 Go | tient, 13 Go de marge » ; « KV int4 + 90 % des experts | 103 Go | confortable »
- `:110` — « au-delà de ~0,8 M de jetons en F16, il n'y a plus de place pour les experts »
- `:111-112` — « `DRAVE_KV_BITS`, mesuré sur Qwen : +3,0 % de perplexité en int8, +3,0 % en clés seules »
- `:118-120` — « F16 | 0,77 M de jetons » ; « int8 | 1,54 M » ; « int4 | 3,08 M »
- `:132` — « le point de bascule est autour de **100 K jetons** »
- `:142` — « fils | 1 | 4 | 8 | **16** | 20 | 30 | 40 » ; « Go/s | 1,9 | 6,3 | 8,7 | **20,8** | 16,8 | 23,8 | 23,0 »
- `:153-157` — « 10 cœurs purs (socket 0) | 11,8 » ; « 10 hyperthreads (socket 0) | 14,6 » ; « 20 cœurs purs (2 sockets) | 14,6 » ; « 20 « hyperthreads » (2 sockets) | 22,6 » ; « **40 threads (tout)** | **22,8** »
- `:163` — « **40 threads ne font pas mieux que 20 cœurs : 22,8 contre 22,6.** »
- `:168-169` — « Il prend `cpu × 3/4` = **30 fils**, alors que **20 suffisent** » ; « ×1,3 de perte à 40+1 fils »
- `:175` — « Banc sur un nœud contre à cheval : **13,5 contre 12,6 Go/s**. Un facteur 1,07 »
- `:181` — « lecteurs simultanés | 1 | 2 | 4 | 8 | **16** » ; « Go/s cumulés | 5,37 | 9,68 | 18,08 | 28,29 | **31,08** »
- `:183-184` — « Vérifié sur 50,5 Go (395 fichiers) : **3,42 Go/s à un lecteur, 21,02 à quatre, 33,19 à seize** »
- `:186` — « **Le NVMe parallélisé (31 Go/s) est plus rapide que la RAM (22 Go/s).** »
- `:189-190` — « les 2,39 Go d'experts par jeton passent de **435 ms** (lecture séquentielle à 5,5) à **77 ms** (16 lecteurs parallèles à 31) »
- `:192-195` — « les 50,5 Go lus tiennent dans les 112 Go de cache RAM » ; « `O_DIRECT` échoue ici (errno 29) et le NVMe n'héberge que 114 Go »
- `:202-204` — « cache de 90 % en RAM + NVMe séquentiel | 0,24 Go | 44 ms » ; « **cache de 25 % + NVMe parallèle** | **1,79 Go** | **58 ms** » ; « **aucun cache, NVMe parallèle** | **2,39 Go** | **77 ms** »
- `:219-224` — « **NVMe** (MAP1602, *DRAM-less*) | 02:00.0 | **node 0** | PCIe 3.0 » ; « GPU 0 … 03:00.0 » ; « GPU 1 … 04:00.0 | **node 0** | PCIe 3.0 ×16 » ; « **GPU 0 ↔ GPU 1** | | | **NVLink, 25,78 Go/s** »
- `:226` — « **Le NVLink est là, et il vaut 2× le PCIe** (25,78 contre ~12 Go/s réels) »
- `:239-240` — « banc mémoire (calcul pur) | 13,8 | 14,2 | 15,0 Go/s » ; « **lecture NVMe** (8 lecteurs) | 22,41 | 21,45 | 22,57 Go/s »
- `:242` — « Écart de **4 %** sur le chemin qui traverse réellement l'UPI »
- `:255-260` — « **10 cœurs** | 10 (1 par cœur) | 14,7 » ; « **10 cœurs** | **20 (2 par cœur, HT)** | **18,7** ← **+27 %** » ; « 10 cœurs | 30 (3 par cœur) | 15,0 — régression » ; « **20 cœurs** | 20 | **22,5** » ; « 20 cœurs | 40 (HT) | 18,9 (essais 18,6 · 18,9 · 26,3 — très bruité) » ; « 20 cœurs | 60 | 20,7 »
- `:284` — « ce qui fait passer le défaut de **30 à 20 fils** »
- `:303-304` — « avec prélecture | 25,3 s | 25,9 s | 26,0 s | **25,73 s** » ; « sans | 25,8 s | 25,8 s | — | **25,80 s** »
- `:306-308` — « **0,3 % — aucun effet.** » ; « le modèle de test (18,6 Go) tient dans les 115 Go de cache RAM »
- `:314` — « le calcul est 18× plus rapide que la lecture »
- `:326` — « Avec la liste **complète** (151 936 tokens), la sortie est **identique au token près** »
- `:340-341` — « français | 13,0 % | 9,384 s | 8,400 s | **+10,5 %** » ; « anglais | 5,8 % | 1,155 s | 0,982 s | **+15 %** »
- `:363-364` — « 2 à 9 tokens portent la masse quand le modèle est confiant, 20 000 quand il hésite »
- `:372-374` — « Qwen3-30B en clusters (9 fichiers) | 18,55 Go | 0,46 s | 72 Mo » ; « DeepSeek-V4-Flash (3 shards) | 86,90 Go | 0,07 s | 35 Mo » ; « **DeepSeek-V4.1-Flash** | **365,70 Go** | **0,08 s** | **47 Mo** »
- `:376` — « **47 Mo de mémoire résidente pour 365,7 Go adressés.** »
- `:385-386` — « en USB seulement (pas de PCIe configuré), soit **625 Mo/s au mieux** — cinquante fois moins que le NVMe parallélisé »
- `:393-395` — « lecture d'une couche | 10,9 ms » ; « **calcul de la même couche** | **0,6 ms** » ; « rapport | **18×** »
- `:397` — « Un accélérateur de calcul sur un chemin où le calcul pèse 5 % »
- `:411` — « le coût du **transfert initial** (1 Go ≈ 83 ms à 12 Go/s) n'est pas mesuré — il est amorti en 3 jetons pour la tête »
- `:418-419` — « il pèse 512 × 2 × 2 octets × 40 = 82 Ko par jeton, soit 82 Go à 1 M de jetons »
- `:425` — « Le débit monte encore entre 8 et 16 (28,3 → 33,2) »
- `:427` — « V4.1 a 384 experts et top-6 (rapport 1,6 % au lieu de 6,25 %) »

**reports/rapport-attention-creuse.md**
- `:5-6` — « son coût croît **linéairement avec le contexte** (2,0 ms à 64 tokens, 12,7 ms à 512, ~200 ms extrapolé à 8 192) »
- `:24-30` — « dense (référence) | 23,6125 | 26,2565 | 24,8995 | 19,5222 » ; « 128 | 23,5840 (−0,12 %) » ; « 64 | 23,4621 (−0,64 %) | 26,1959 (−0,23 %) | 24,6867 | **19,3700 (−0,78 %)** » ; « **32** | **23,3302 (−1,20 %)** | **26,1199 (−0,52 %)** | **24,6857 (−0,86 %)** | **19,4136 (−0,56 %)** » ; « 24 | — | — | 24,7043 » ; « 16 | 23,6591 (+0,20 %) | 26,5065 (+0,95 %) » ; « 8 | 24,9071 (+5,5 %) »
- `:32-34` — « Restreindre l'attention aux 32 meilleures clés améliore la perplexité de 0,5 à 1,2 % »
- `:41-46` — « 256 | 12,5 % » ; « 1 024 | 3,1 % » ; « 4 096 | 0,78 % » ; « 32 768 | 0,1 % »
- `:60-61` — « À contexte 256, k = 32 est optimal (12,5 % des clés) ; à contexte 512, c'est k = 64 (12,5 % également) »
- `:95` — « en vérifiant que la perplexité restait identique au chiffre près (23,6125 dense, 23,3279 à k=32) »
- `:97-99` — « 11,5 ms en dense, 11,5 ms à k=32, et **11,6 ms à k=1** — où la somme pondérée ne fait plus que 14 × 64 opérations au lieu de 459 000 »
- `:109-112` — « Qualité | ✅ **+0,5 à +1,2 %** » ; « 12,5 % de densité à 256, 0,8 % à 4 096 » ; « Temps de calcul | ❌ **aucun gain** » ; « ✅ négligeable : 0,04 M paires/token contre 354 M événements »
- `:121-122` — « l'attention tournait à **1,9 GFLOP/s sur un seul cœur**, soit 0,6 opération par cycle »
- `:137-138` — « avant | **11,5 ms/token** » / « après | **5,7 ms/token** »
- `:155-156` — « attention 32 seule = −0,52 % (B), attention 32 + FFN 90 % = −0,45 %, attention 32 + FFN 85 % = **+0,19 %** »

**reports/rapport-attribution-kv.md**
- `:3-5` — « à 8 192 jetons, les **valeurs** en int8 ne coûtent rien (1 % de l'écart) et les **clés** coûtent tout (99 %) »
- `:9` — « 8 191 jetons notés, contexte 8 192, `--dense --lot 512` »
- `:13-16` — « cache f32 (référence) | **14,2339** » ; « cache int8 complet | 14,6667 | +3,04 % | 100 % » ; « **clés f32** · valeurs int8 | **14,2372** | **+0,023 %** | **99,2 % expliqué** » ; « clés int8 · **valeurs f32** | 14,6622 | +3,01 % | 1,0 % seulement »
- `:32-35` — « `DRAVE_KV_BITS=8 DRAVE_KV_K_F32=1` donne un cache à **64 % de la taille f32** (5,125 octets par élément contre 8, échelles comprises) pour +0,02 % de perplexité — alors que l'int8 complet (28 %, soit 2,25 octets) coûte +3,0 % »
- `:38` — « llama.cpp paie +0,8 % pour son cache int8 à la même longueur »
- `:45` — « **clés f32 · valeurs int4** : 58 % de la taille f32 (4 + 0,625 sur 8) »

**reports/rapport-campagne-parcimonie.md**
- `:8-10` — « Toutes les mesures de perplexité et de comptes d'événements sont **déterministes** » ; « Seules les mesures de **temps** sont bruitées (la machine tournait sous une charge de 8 à 22) »
- `:18-23` — « **poids d'attention** (top-k clés) | **améliore** de 0,5 à 1,2 % | ✅ » ; « activations du FFN (k-WTA 90 %) | +0,15 à +0,28 % » ; « (k-WTA 85 %) | +0,5 à +1,2 % » ; « entrée des projections d'attention (90 %) | +0,06 % » ; « **Q et K** (après RoPE) | ×2,2 à 50 %, ×36 à 25 % | ❌ » ; « activations du FFN (seuil absolu) | ×117 à 5 % du max | ❌ »
- `:35-37` — « référence | 354,3 M | 23,6125 | 26,2565 » ; « attention 32 clés seule | 354,3 M | 23,3279 (**−1,21 %**) | 26,1178 (**−0,53 %**) » ; « **+ `gate` à 85 %** | **338,8 M (−4,4 %)** | 23,2811 (**−1,40 %**) | 26,1417 (**−0,44 %**) »
- `:47` — « seuil absolu plutôt que relatif | **10× moins efficace** à sparsité égale »
- `:48` — « renormalisation homéostatique après k-WTA | **dégrade** (+0,2 à +3,6 %) »
- `:50` — « FFN complet à 85 % + attention creuse | **non additif, défavorable** (+0,19 % en B) »
- `:51` — « creuser Q et K … **catastrophique** (×2,2 à 50 %) »
- `:56-59` — « taux de décharge de **R̂ ≈ 0,15** — 6,7× moins d'événements » ; « Nous plafonnons à **−4 à −15 % d'événements** pour +0,5 % de perplexité »
- `:67` — « élaguer après coup détruit (11 points sur les poids) »

**reports/rapport-capteur-hebbien.md**
- `:8-9` — « la création de nœuds par Hebb n'ajoute rien sur 69 % des poids du modèle »
- `:19-20` — « Mesure sur 1 025 tokens de WikiText-2, couche 12, projection `ffn_gate` (4 864 × 896), quantile 0,1 »
- `:25-27` — « sans capteur | 96,75 s » ; « avec capteur | 99,64 s » ; « **surcoût** | **+3,0 %** »
- `:29-30` — « 499 175 activations capturées, soit 487 par token — exactement les 10 % demandés. Trace produite : 17,4 Mo par couche »
- `:32-34` — « la machine en a 24 inutilisés pendant l'inférence » ; « sa copie coûte 7 Ko par matrice, 1,2 Mo par token, soit 19 Mo/s à 15,8 tok/s »
- `:44-48` — « Énergie expliquée par `W · C` … **R² = 0,845** » ; « **15,5 %** » ; « 1ʳᵉ valeur singulière | **46,2 %** … contre 0,44 % pour `W` » ; « 8 premières | 61,6 % — contre 2,3 % pour `W` » ; « Rang effectif | 795 (trace) contre 894 (poids) »
- `:62-67` — « trace, direction n°0 | **100,00 %** » (×3) ; « résidu non linéaire, directions n°0 à 4 | **100,00 %** » ; « le rang de `W` pour `ffn_gate` est de **896 sur 896 dimensions d'entrée** »
- `:80-88` — « `attn_q` | 896 × 896 | 853 » ; « `attn_output` | 896 × 896 | 852 » ; « `ffn_gate` | 4 864 × 896 | 896 » ; « `ffn_up` | 4 864 × 896 | 896 » ; « `attn_k` | 128 × 896 | 127 | **ouverte — 769 directions** » ; « `attn_v` | 128 × 896 | 128 | **ouverte — 768 directions** » ; « `ffn_down` | 896 × 4 864 | 893 | **ouverte — 3 971 directions** »
- `:90-92` — « **69,2 % des poids** sont dans des projections saturées, **30,8 %** dans des projections ouvertes »
- `:96-97` — « **401 856 monômes quadratiques** `x_i · x_j` dans un espace d'entrée de 896 dimensions »

**reports/rapport-coherence-docs.md**
- `:3-6` — « **80 affirmations** vérifiées une par une … **38 sont fausses (PÉRIMÉ)**, **15 se contredisent entre documents (CONTRADICTOIRE)**, **10 existent dans le code et manquent aux documents (MANQUANT)**, **17 tiennent (OK)** »
- `:16-19` — « Commit de référence | `ae85043` (2026-09-30 12:30) » ; « `main.rs` sha256 `d5e90136…` · 3 112 lignes » ; « `model.rs` sha256 `3e5dde2d…` · 3 872 lignes » ; « `/tmp/flux_v2.bin` (66 370 408 o, en-tête `DRVF` version **2**), `/tmp/flux_v3.bin` (version **3**) »
- `:24-25` — « HEAD était `a0687b9` avec 165 lignes de `model.rs` non commitées » ; « `model.rs` portait de nouveau 31 lignes non commitées (`DRAVE_KV_K_F16` »
- `:37` — « les recalculs d'en-tête (79 = 39 + 40) »
- `:47` — « `const VERSION_FLUX: u8 = 3;` (main.rs:1295) »
- `:52` — « `TraceFlux::nouveau` écrit **2** par défaut et **3** si `DRAVE_TRACE_BLOCS=1` (model.rs:549) »
- `:65` — « `TAILLE_TETE = 79` : 26 (v1) + 13 (niveaux/seuil/top-k/renorm) + 40 »
- `:83` — « flux dense = **3 623 octets** (39 + 3 584) » → « avec `TAILLE_TETE = 79` : **3 663** »
- `:86` — « 2 159 (listes i16, seuil 0,02, vrai texte), 1 568 (blocs + écarts, seuil 0,01) »
- `:87` — « 2 268 est la mesure **avant** les indices par écarts » ; « après écarts : **1 568** »
- `:88` — « `--flux-blocs --act-thresh 0.01` : **3 623 → 1 589** (÷2,3) » → « avec 79, **1 629** ; l'écart 1,32e-2 reste »
- `:89` — « **1 989** en listes à échelle par bloc (68 % d'activité) » → « Format actuel (écarts u8, 2 o/actif, en-tête 79) : **≈ 1 419** »
- `:90` — « en liste creuse (**871** octets au lieu de 3 623) » ; « son propre tableau donne **897** »
- `:92` — « 1 seul lot de **917 543 octets** » → « avec l'en-tête de 79 : **917 583** »
- `:94-96` — « trace dense 512 j : 132 396 736 → **66 370 408** (−49,87 %) » ; « `/tmp/flux_v2.bin` = exactement 66 370 408 octets, version 2 » ; « 24 576 listes · 22 008 776 actifs »
- `:97` — « trace 512 jetons = « **12 288 listes** · 132 Mo · 6 octets par neurone actif » » → « 24 576 listes pour 512 jetons × 24 couches × 2 points ; 12 288 = la valeur pour **256 jetons** »
- `:100` — « i8 + échelles f16 par bloc sont **faits et commités** (`ae85043` : trace dense 45 079 930 o, −65,9 % depuis la v1, rejeu 19,4029) »
- `:106-107` — « Croisement push/pull à **10 %** de densité ✅ mesuré » contre « **~22 %** … pas à 10 » (rapport de référence)
- `:108-110` — « le moteur tient en **386 lignes** » → « 11 440 lignes aujourd'hui » ; « **2 319 lignes** de Rust » ; « ~**5 000** lignes »
- `:112` — « KV int4 « mesuré : **+384 %** » … la mesure de référence à 8 192 est **+364 %** contre +494 % »
- `:113` — « Qwen 6 bits : « **19,3045** ← bat l'int8 » » (sans source)
- `:114-116` — « perplexité WikiText-2 : 24,90 contre 25,00 numpy » → « 24,90 contre 25,0004 » ; « Q4_0 : +9,1 % contre Q8_0 » → « 21,0116 contre 19,2647 = +9,07 % » ; « gpt-oss-120b : perplexité « **—** » » → « 15,1757 (REPRISE §2) et 20,8361 à 63 jetons »
- `:117` — « rejeu par lots : **17,4294** » ; « la valeur 18,0851 du mode lot »
- `:123-124` — « fait et mesuré au commit `cda3162` (12:02), **23 minutes après** l'écriture de §6bis » ; « il **décroît** (1,37e-1 à 64 → 1,32e-2 à 1 024) »
- `:126` — « fait : `--flux-liste`, `--flux-blocs`, 3 623 → 1 568 octets »
- `:131` — « ce fichier **n'existe pas** (le rapport existant s'appelle `rapport-prefill-par-lots.md` »
- `:142` — « **ces fichiers n'existent pas dans le dépôt** ; ils sont dans `../FPGA-Stratix-V/docs/` »
- `:151` — « présents dans `../FPGA-Stratix-V/tools/` »
- `:223-227` — « PÉRIMÉ | **38** » ; « CONTRADICTOIRE | **15** » ; « MANQUANT | **10** » ; « OK | **17** » ; « **total** | **80** »

**reports/rapport-coherence-docs-2.md**
- `:3-8` — « **66 affirmations** revérifiées … **27 tiennent**, **17 sont périmées**, **14 se contredisent** et **8 manquent** » ; « **chiffre vedette du cache KV** (« 75 % / 50 % » contre « 64 % / 28 % » »
- `:14-18` — « Commit de référence | `a383cd7` (2026-09-30 15:11) » ; « `main.rs` sha256 `bc53a66ad757faa6…` · 3 508 lignes » ; « `model.rs` sha256 `61582adb8ded0f25…` · 3 928 lignes » ; « Total `.rs` du moteur | **11 901 lignes** (7 fichiers) » ; « **73 commits** dans la journée »
- `:32-34` — « `/tmp/verif_v2.bin`, 517 366 o, 192 listes, 171 554 actifs » ; « `DRAVE_TRACE_BLOCS=1` écrit bien **v3** (`/tmp/verif_v3.bin`, 346 636 o, 192 listes, 166 206 actifs — avec perte »
- `:38` — « le compte de tests (13 `#[test]`) vient d'un `grep` »
- `:50` — « `VERSION_FLUX = 4` (1376), `TAILLE_TETE = 79` (1404, verrouillé par `assert_eq!` 3344-3345), modes 0 dense · 1 listes · 2 blocs · 3 lot »
- `:59` — « mesuré : **−32,1 %** contre la v2 (66 370 408 → 45 079 930 o, `docs/format-flux.md:58`) et −65,9 % contre la v1 »
- `:61` — « `verifier_taille` (`main.rs:1468`) ne teste que `> 256 Mo` et est appelé **4 fois** » ; « les 7 tests de `main.rs:3343-3474` »
- `:71` — « flux dense = **3 663 octets** (79 + 896 × 4) »
- `:72` — « 20 + 3 584 = **3 604**, pas 3 663 »
- `:74` — « 2 159 est l'i16 au seuil **0,02** » ; « 2 268 est le mode blocs au seuil 0,01 à l'époque des 39 octets (`:133`, soit 2 308 avec l'en-tête v4) »
- `:75` — « 79 + 256 × 896 × 4 = **917 583** »
- `:76` — « avec l'en-tête v4 : **3 663 → 1 629** ; le ÷2,3 et le 1,3 % restent vrais »
- `:82` — « v3 : **45 079 930 o** (−32,1 % vs v2), rejeu 19,4029 (+0,074 %), 21 630 645 actifs »
- `:83` — « « blocs, échelles f16 : **45 836 190** » … la v3 réellement implémentée et mesurée donne **45 079 930** »
- `:89` — « mode lot : **18×** à 20 ms (2,6 s contre 47,6 s) et **7×** par jeton (116,7 → 16,6 ms) »
- `:95` — « +0,018 % à 8 191 jetons ; +0,057 % est la valeur à **contexte 256** »
- `:97` — « le rapport de la campagne complète dit **64 %** (5,125 o/élément, `:16`) et **28 %** (2,25 o, `:20`) » ; « le code confirme 4 + 1,125 = 5,125 o (`model.rs:1074-1076`) »
- `:98` — « mesurée : 14,3209, **+0,61 %**, 2,625 o/33 % »
- `:100` — « « mesuré : **+7,1 %** (llama.cpp : +3,1 %) » » contre « **+1,5 %** à 512, **+3,0 %** à 8 192 »
- `:102` — « clés f16 = +0,018 %/39 %, facteurs 130 et 840, int4 +364 % »
- `:109` — « `[options] cache KV : 32 bits · f16 avant false` »
- `:115` — « sauf `reports/rapport-mode4-lot-listes.md` qui est un livrable **annoncé** »
- `:123` — « (3 663 o, 1 419, 0,25 Mbit/s, `attente ≈ calcul + 3,2 × latence`) »
- `:128` — « la journée compte **73 commits** (dont **70** déjà commités à 14:09) »
- `:129` — « **11 901** lignes de `.rs` (main.rs 3 508, model.rs 3 928, list.rs 1 440) »
- `:135` — « ×73 pour le KV en VRAM, 968 ms CPU, 1,99e-7, 12,4 → 12,5 ms en top-k CPU »
- `:217-218` — « 66 affirmations revérifiées après les changements du 30/09 : 27 OK, 17 PÉRIMÉ, 14 CONTRADICTOIRE, 8 MANQUANT »

**reports/rapport-coherence-vision.md**
- `:3-6` — « les **18 documents** de `docs/` (4 870 lignes) » ; « **cinq relectures adverses** » ; « **88 sites de correction** dans `docs/` (95 avec `REPRISE.md` » ; « une **sixième relecture adverse du diff lui-même**, qui a trouvé 13 défauts de plus »
- `:20` — « llama.cpp n'est qu'une **porte de correction** »
- `:41` — « un **19ᵉ format lisible** (`Q4_1`, lu par la même branche que `Q4_0`) »
- `:43-44` — « la mesure documentée est `origine 15,2789 · clusters 15,2789` » ; « en scannant les **28 en-têtes GGUF** du parc »
- `:53` — « gpt-oss 15,6017 ; « protocole v5, 5 modes » »
- `:64` — « 48 tests (49 depuis l'ajout du test d'identité paire/événement) »
- `:68` — « gpt-oss = 128 experts **top-4** (et non top-8) »
- `:69` — « MLA « validée à la **position 0** » » ; « types réels du fichier (dont **I8**, aucun I32) »
- `:70` — « 8,3 nJ **projeté** ; densité mesurée **17,9 %** sous le croisement de 22 % »
- `:114-115` — « corrélation 0,999024, top-1 3/3 » ; « (+0,009 / +0,372 / +0,611 puis **+4,070 nat** à la position 3) »
- `:126-132` — « section 7 … ~20 min, hors mode `rapide` » ; « llama.cpp applique YaRN dès la première position (166,85) là où nous le différons (15,6017), et en le forçant nous obtenons 84,07 »
- `:141` — « Le fichier déclare `hc_mult = 4` mais ne contient aucun `output_hc_fn/base/scale` »
- `:145-146` — « **19 formats lisibles, 17 à la porte** »
- `:159-163` — « `cargo test --release` **48**, Qwen **19,3885**, clusters **799,8557**, formats **17 concordants / 0 divergence / 0 absent** »

**reports/rapport-compacite-trace.md**
- `:5-8` — « trace dense de 512 jetons **132 396 736 → 66 370 408 octets (−49,87 %)** » ; « perplexité 19,3885 dans les deux cas » ; « exactement les mêmes 24 576 listes et 22 008 776 neurones actifs »
- `:10-11` — « une perplexité fausse (1958,72 au lieu de 19,3885) »
- `:14-18` — « **45 079 930 octets** (−65,9 % par rapport à la v1, −32,1 % par rapport à la v2), au prix de **+0,074 % de perplexité au rejeu** (19,4029 contre 19,3885) et d'une erreur par valeur de **0,085 % RMS** du max de la liste — la prévision de ce rapport était 0,077-0,081 % »
- `:24-27` — « la trace DRVF v1 coûte **6,04 octets par neurone actif** quand le transport en coûte ~2 » ; « porte le total à **−79 %** »
- `:43-45` — « disque, DRVF v1 | u32, 4 octets | i16, 2 octets | f32, 1 par liste | **6,04** (mesuré) » ; « réseau, mode 1 | u16, 2 octets | i16, 2 octets | f32, 1 par liste | 4 » ; « réseau, mode 2 … | **u8**, 1 octet | **i8**, 1 octet | f32, 1 par bloc de 32 | **~2** »
- `:58-59` — « `/tmp/flux_sparse.bin` | Qwen2.5-0.5B Q8_0, 256 jetons, 24 couches, seuil 0,05 | **53 092 562 o** | 8 791 414 | 39,9 % » ; « `/tmp/flux_f32.bin` … 512 jetons, `--abits 16` | **132 396 736 o** | 22 008 776 | 99,9 % »
- `:75-80` — « l'en-tête de fichier (14 o) et la sentinelle de fin (2 o » ; « L'échappement d'indice coûte **3 octets** » ; « vérifiée contre numpy sur 10 018 valeurs … **0 désaccord** »
- `:86-93` — « actuel (u32 + i16) | 53 092 562 | 6,04 » ; « écarts + i16 | 26 718 364 | 3,04 » ; « écarts + blocs i8 | 20 777 766 | 2,36 » ; « **blocs, échelles f16** | **19 401 510** | **2,21** » ; « zstd niv. 19 sur l'actuel | 16 157 273 | 1,84 » ; « **zstd niv. 19 sur écarts+blocs** | **11 128 840** | **1,27** »
- `:96-98` — « (échantillon de 16 Mio) donnent 20 225 293 / 16 554 621 / 23 922 712 — l'extrapolation est juste à **2,5 % près** »
- `:100-101` — « **Meilleure variante sans compression : `blocs f16`, 19 401 510 octets, −63,5 %.** » ; « **Meilleur résultat tout court : `écarts+blocs` + zstd 19, 11 128 840 octets, −79,0 %.** »
- `:107-108` — « **indices u32 : 35 165 656 o = 66,2 %** — pour des indices qui tiennent sur un octet dans **99,9997 %** des cas (22 échappements sur 8 791 414 » ; « **valeurs i16 : 17 582 828 o = 33,1 %** »
- `:116-118` — « le gain net est de 5,94 Mo (−22 % de plus), pour une erreur RMS de **0,077 % du max de la liste** » ; « Les échelles en f16 reprennent encore 1,38 Mo (7 % de la v2) »
- `:119-124` — « **échelles + en-têtes : 0,65 %** … ils deviennent 15,4 % de la v2 » ; « les échelles de blocs émises sont 28 par liste (896 canaux / 32), dont **99,6 % utiles** sur la trace creuse et **100 %** sur la dense »
- `:133-140` — « actuel (u32 + i16) | 132 396 736 | 6,02 » ; « écarts + i16 | 66 370 406 | 3,02 » ; « écarts + blocs i8 | 47 212 446 | 2,15 » ; « **blocs, échelles f16** | **45 836 190** | **2,08** » ; « zstd niv. 3 sur l'actuel | 41 675 229 » ; « zstd niv. 19 sur l'actuel | 50 009 567 » ; « **zstd niv. 19 sur écarts+blocs** | **26 634 831** | **1,21** »
- `:149` — « **Aucun échappement** sur 22 008 776 indices »
- `:152-153` — « **zstd niveau 19 fait moins bien que le niveau 3** sur le format actuel (50,1 Mo contre 41,6 Mo) »
- `:159-161` — « Le passage i8 gagne **relativement plus** en dense (−29 %) qu'en creux (−22 %) : les 28 échelles de blocs y sont amorties par 896 valeurs pleines, alors qu'en régime creux elles se paient sur 358 actifs par liste »
- `:166` — « densité ÷2,3 → trace ÷2,5 »
- `:170-174` — « creuse, 256 jetons | 53,1 Mo | 20,8 Mo | 19,4 Mo | **11,1 Mo** | **−79 %** » ; « dense, 512 jetons | 132,4 Mo | 47,2 Mo | 45,8 Mo | **26,6 Mo** | **−80 %** » ; « dense, 8 192 jetons | ~2,12 Go | ~755 Mo | ~733 Mo | ~426 Mo | −80 % »
- `:179-181` — « la trace passe de **2,1 Go à 0,4 Go** »
- `:214` — « le bug qui a donné une perplexité de **356 694** au lieu de 17,43 »
- `:248-251` — « indices par écarts u8 | −49,7 % | aucun » ; « + valeurs i8 et échelles par bloc | −60,9 % | qualité » ; « + échelles f16 | −63,5 % » ; « + zstd 19 … | **−79,0 %** »

**reports/rapport-cpu-aer.md**
- `:11` — « (accumulateur, 4096 × 24 bits = **12 Kio**, tient dans les M20K) »
- `:16-18` — « bande passante lecture séquentielle : **11.5 Go/s** » ; « dispersion (`np.bincount`) : **183999808.87 G événements/s** » ; « dispersion (`np.add.at`) : 364797216.41 G événements/s »
- `:24-26` — « Lecture séquentielle | 4,1 Go/s | 23,4 | **28,7** | 28,2 » ; « Dispersion pure | 0,96 G év/s | 3,46 | 3,20 | 3,22 » ; « **Écarts + dispersion** | 0,87 | 4,55 | **7,79** | 6,79 »
- `:32` — « Projection 7B (densité 5 %, 0,476 b/poids) »
- `:36-40` — « CPU, borné bande passante (28,7 Go/s) | 14.51 | 68.9 » ; « CPU, borné noyau (7,79 G év/s) | 44.93 | 22.3 » ; « **CPU réaliste** | **44.93** | **22.3** » ; « 1 carte FPGA | 43.12 | 23.2 » ; « 4 cartes FPGA (modèle réparti) | 10.78 | 92.8 »
- `:48` — « 183999808.9 G événements/s mesurés contre 0.35 G nécessaires par token »
- `:50-52` — « Une carte FPGA ≈ ce CPU (23 contre 22 tok/s) » ; « 3× la bande passante (28,7 contre 9,66 Go/s) » ; « **cadence d'événements** (7,8 G/s) »
- `:54-56` — « 4 cartes = 4 mémoires et 4 jeux de voies indépendants → 4× le débit »

**reports/rapport-croisement-push-pull.md**
- `:7-9` — « un événement = écart + valeur, 2 octets » ; « 1 octet par poids, aucune dispersion »
- `:11-13` — « perplexité 19,2647 au chiffre près sur 510 jetons, tokens identiques »
- `:29` — « `blk.0.ffn_gate.weight` (4 864 × 896, 4,36 M poids), 16 threads »
- `:34-41` — « 0 % | 0,004 | 0,167 | 0,03 » ; « **10 %** | 0,078 | 0,163 | **0,48** » ; « **25 %** | 0,180 | 0,163 | **1,11** » ; « **100 %** | 0,801 | 0,171 | **4,69** »
- `:43-46` — « Les deux architectures se croisent à **~22 % de densité d'activation**, pas à 10 % » ; « À 10 % le push est ×2,1 plus rapide, à 1 % ×8,3 »
- `:48` — « Le seuil de bascule `seuil_push` est passé de 0,15 à **0,22** »
- `:54-57` — « LLM dense entraîné … | **100 %** (0,00 % de zéros) | ❌ pull gagne ×4,7 » ; « meilleure parcimonie imposée sans entraînement | ~85 % » ; « réseau à décharge entraîné (SpikeGPT) | **R̂ = 0,15** | ✅ **push gagne** » ; « réseau vraiment creux (ReLU, MoE, top-k) | < 10 % »
- `:66-71` — « le mode liste est maintenant 8 % plus rapide que le noyau dense (15,8 contre 14,7 tok/s) ». **C'est faux** » ; « accumulait en **i64 sur toute la ligne** » ; « accumulation i32 par tranches de 256 » ; « il passe de 14,7 à **36,4 tok/s** »
- `:75-77` — « push (événements) | 15,59 | 24,8995 » ; « pull (dense i8), avant | 14,66 | 24,8995 » ; « **pull (dense i8), après** | **36,43** | 24,8995 »
- `:81` — « après l'attention non vectorisée (÷2) et la liste des destinations touchées (+35 %) »
- `:92-98` — « 1000 | 111 % | 0 év — 9,1 s | 0 év — 9,3 s (dense) » ; « 400 | 44 % | 0 év — 10,1 s | 0 év — 9,4 s (dense) » ; « 200 | 22 % | 0 év — 9,6 s | 18,1 G év — 8,7 s (bascule) » ; « 100 | 11 % | 0 év — 9,1 s | 9,1 G év — **7,1 s** » ; « 50 | 5 % | 0 év — 9,1 s | 4,5 G év — **6,2 s** »
- `:100-102` — « La bascule tombe exactement au seuil mesuré (22 %) » ; « ×1,47 à 5 % de densité »
- `:107-108` — « le moteur gagne ×2,27 de bout en bout (13,6 → 30,7 tok/s, 510 jetons) »
- `:111` — « la DDR3 de la carte fait 9,66 Go/s contre 380 pour le GPU »

**reports/rapport-decoupage-moe.md**
- `:3-5` — « sur Qwen3-30B-A3B (128 experts, 8 par jeton) … diviser par ~1,8 la ventilation d'un jeton (3,08 nœuds au lieu de 5,32 au hasard, à 8 clusters) » ; « accord 1,000 »
- `:20` — « `DRAVE_TRACE_EXPERTS=<chemin>` écrit une ligne par (couche, jeton) »
- `:37` — « Qwen3-30B-A3B, ~1 600 jetons, 48 couches »
- `:41-43` — « 4 | **0,799** | **1,94** | 0,440 | 3,59 | ×1,8 » ; « 8 | **0,607** | **3,08** | 0,319 | 5,32 | ×1,9 » ; « 16 | **0,442** | **4,46** | 0,250 | 6,55 | ×1,8 »
- `:46-47` — « accord de 1,000 sur les paires, pour les trois valeurs de G et sur toute la trace »
- `:59` — « la ventilation est divisée par 1,7 »
- `:60-61` — « **4 nœuds** : 1,94 nœud par jeton — un jeton sur deux tient dans un seul nœud »
- `:86-88` — « gpt-oss (4 experts sur 128) est en cours de mesure ; DeepSeek-V4.1-Flash, Kimi-K2.7 et GLM-5.3 (256 experts ou plus, jusqu'à 1 M de contexte) sont en téléchargement »
- `:96-97` — « 1 600 jetons ne suffisent pas à couvrir les experts rares » ; « La trace de 2 048 jetons en cours »
- `:104-106` — « **3,20 Go chargés au lieu de 18,56** pour un nœud qui sert un cluster, **625 ms au lieu de 3,9 s**, **1 587 tenseurs vérifiés** »

**reports/rapport-drapeaux-ignores.md**
- `:7` — « Le protocole de flux est passé en **version 4** (puis 5, avec le mode « lot en listes ») »
- `:24-25` — « `main.rs` sha256 `1726f9ac3665c3ce…` (2 999 lignes), `model.rs` sha256 `1d7eacc506db6cab…` (3 675 lignes), 30/09 11:54 »
- `:31-32` — « **84 drapeaux `--xxx`** extraits de `analyser()` (main.rs:396-519) et **26 variables `DRAVE_*`** (27 chaînes »
- `:155-157` — « perplexité 1929.3230 sur 3 tokens (0 événements, 0.3 s) » ; « identique au chiffre près »
- `:159-161` — « tokens générés : [6, 25010, 10, 4999] » ; « tokens générés : [53116, 84925, 36109, 36752] »
- `:170` — « 1929,3 → 4949,5 : appliqué »
- `:181-183` — « === contexte : 512 jetons === » ; « --plan --ctx 0 → === contexte : 32768 jetons === »
- `:192-194` — « `--threads 4` → threads : 4 » ; « `--dense --threads 4` → threads : 30 » ; « `--dense --limit 4 --threads 4` → threads : 30 »
- `:216` — « `[options] act_levels=65535 act_thresh=0.05 attn_window=0 moe_topk=0 lot=1 topk_proj=[0;7]` »
- `:240-245` — « **110 options auditées** : 84 drapeaux de ligne de commande + 26 variables `DRAVE_*` » ; « **46 drapeaux (55 %) sont ignorés** … dont **20 classés 🔴** » ; « 1 variable (`DRAVE_FLUX_VERIF`) est muette dès que `--lot > 1` »
- `:251-253` — « prouvé : 1929.3230 identique à `--keep 0.05` près » ; « `[6, 25010, 10, 4999]` dans les deux cas »
- `:255` — « `--dense --threads 4` mesure 30 fils »

### 🤖 Assistant

⏵ Vérification compacte par HTTP des URL externes candidates

- **bash** `{"command": "for u in \\\n\"https://github.com/ggml-org/ggml/blob/master/docs/gguf.md\" \\\n\"https://github.com/ggml-org/ggml/blob/master/src/ggml-common.h\" \\\n\"https://github.com/ggml-org/llama.cpp\" \\\n\"https://arxiv.org/abs/2104.09864\" \\\n\"https://arxiv.org/abs/2309.00071\" \\\n\"https:/ … [2633 caractères tronqués]`

  ```
200  https://github.com/ggml-org/ggml/blob/master/docs/gguf.md
200  https://github.com/ggml-org/ggml/blob/master/src/ggml-common.h
200  https://github.com/ggml-org/llama.cpp
200  https://arxiv.org/abs/2104.09864
200  https://arxiv.org/abs/2309.00071
200  https://arxiv.org/abs/2405.04434
200  https://arxiv.org/abs/2101.03961
200  https://arxiv.org/abs/1306.0895
200  https://arxiv.org/abs/1910.07467
200  https://arxiv.org/abs/2002.05202
200  https://arxiv.org/abs/1606.08415
200  https://arxiv.org/abs/2106.09685
200  https://arxiv.org/abs/2211.17192
200  https://arxiv.org/abs/2412.19437
200  https://arxiv.org/abs/2211.05102
200  https://arxiv.org/abs/2305.13245
200  https://arxiv.org/abs/1911.02150
200  https://arxiv.org/abs/2309.17453
200  https://arxiv.org/abs/2310.06825
200  https://arxiv.org/abs/2307.03172
200  https://arxiv.org/abs/2404.06654
200  https://arxiv.org/abs/1508.07909
200  https://arxiv.org/abs/2103.13630
200  https://arxiv.org/abs/2210.17323
200  https://arxiv.org/abs/2208.07339
200  https://arxiv.org/abs/2310.10537
200  https://arxiv.org/abs/2402.04396
200  https://arxiv.org/abs/2010.11929
200  https://arxiv.org/abs/2103.00020
200  https://arxiv.org/abs/2305.13048
2
… [1333 caractères tronqués]
  ```

### 👤 Utilisateur

Agent 56879594-1434-4e34-83cc-de42cdf192a1 sent a message:
INVENTAIRE DE VOCABULAIRE — 20 rapports de reports/ (lecture intégrale, 3 295 lignes). Aucun fichier modifié.

## A. Termes et sigles

**Sigles, modèles, algorithmes**
- **ALM** (Adaptive Logic Module) — brique logique élémentaire du FPGA Stratix V, comptée pour dimensionner les voies MAC ; projections carte ; `reports/rapport-eparsite.md:64`.
- **AVX2** (Advanced Vector Extensions 2) — SIMD x86 utilisé par `q8_dot_avx2` et le noyau 4 bits ; `src/gguf.rs`/`src/engine.rs` ; `reports/rapport-inference.md:120`.
- **AVX-512** — extension SIMD évoquée comme noyau futur qui « paierait mieux » le 4 bits ; `reports/rapport-mur-memoire-4bits.md:205`.
- **BitNet b1.58** — modèle ternaire *entraîné* (non quantifié après coup), densité 50-70 % de non-nuls ; `reports/rapport-eparsite.md:70`.
- **BLAS** — bibliothèque d'algèbre linéaire ; le moteur revendique « sans BLAS » ; `reports/rapport-inference.md:1`.
- **BPE** (Byte Pair Encoding) — tokenizer Qwen2 réimplémenté (`src/tokenizer.rs`) ; `reports/rapport-inference.md:22`.
- **CDC** — sigle non développé, associé à un encodage « CSR/plan » et à la « référence CDC » (dense ternaire) ; `reports/rapport-encodage.md:42`.
- **CSA** (Compressed Sparse Attention) — attention compressée à candidats de V4.1 (`build_csa_lid_attention`) ; `reports/rapport-execution-v41.md:37`.
- **CSR** (Compressed Sparse Row) — encodage creux indexé, disqualifié par la mesure ; `src/list.rs` ; `reports/rapport-encodage.md:12`.
- **CUDA** — API GPU NVIDIA ; `drave-core/gpu/drave_gpu.cu`, `cuda_stub.h` ; `reports/rapport-gpu-scores.md:70`.
- **DDR3** — mémoire de la carte FPGA mesurée à 9,66 Go/s, goulot du projet ; `reports/rapport-minimal.md:59`.
- **DSA** — indexeur d'attention creuse DeepSeek (architecture `glm-dsa`), inactif sous `index_topk = 2048` ; `reports/rapport-mla-experts.md:124`.
- **DSP** — bloc multiplieur dur que le projet s'interdit (« aucun DSP ») ; `reports/rapport-encodage.md:74`.
- **DenseQ4** — forme interne 4 bits (nibbles signés biaisés, échelle `u16` par bloc de 32) ; `reports/rapport-mur-memoire-4bits.md:87`.
- **DenseQ8** — noyau dense int8 à échelles par bloc, chantier d'échelles ; `reports/rapport-gpt-oss-perplexite.md:252`.
- **FPGA** — cible matérielle (Stratix V GS D5) ; `reports/rapport-eparsite.md:64`.
- **Gini** — indice de concentration du routage d'experts par couche ; `reports/rapport-empreinte-memoire.md:194`.
- **GQA** (Grouped-Query Attention) — attention groupée Qwen2 (14 têtes requête / 2 KV, 7:1) ; `src/model.rs` ; `reports/rapport-inference.md:34`.
- **HCA** — attention compressée simple de V4.1 (`build_hca_attention`) ; `reports/rapport-execution-v41.md:37`.
- **IQ1_M / IQ1_S / IQ2_XXS / IQ3_XXS / IQ4_XS / Q3_K / Q4_K / Q6_K** — types de super-blocs ggml quantifiés (256 poids) à déquantifier ; `Source::Dequant`, `tools/portes_formats.sh` ; `reports/rapport-empreinte-memoire.md:527` (IQ1_M/IQ2_XXS), `reports/rapport-mla-experts.md:55` (Q4_K/Q6_K).
- **Jaccard** — recouvrement d'ensembles d'experts entre couches, langues, occurrences ; `reports/rapport-empreinte-memoire.md:114`.
- **KV** (clé/valeur) — cache d'attention, miroir VRAM `DRAVE_GPU_KV` ; `reports/rapport-empreinte-memoire.md:246`.
- **LID** — variante « à candidats » de la CSA (`candidate_topk_blocks = 2048`) ; `reports/rapport-execution-v41.md:37`.
- **LRU** (Least Recently Used) — éviction du cache d'experts (32 entrées → 78 %) ; `reports/rapport-empreinte-memoire.md:296`.
- **LUT** — ressource logique FPGA ; « ~21 LUT pour un 64:1 » ; `reports/rapport-encodage.md:73`.
- **MAC** (Multiply-Accumulate) — « ~312 voies de MAC » saturent la DDR3 ; `reports/rapport-minimal.md:61`.
- **M20K** — banc mémoire interne FPGA, point dur de la collecte irrégulière ; `reports/rapport-encodage.md:77`.
- **MLA** (Multi-head Latent Attention) — attention à 4 projections de rang faible + cache latent ; `src/model.rs` ; `reports/rapport-empreinte-memoire.md:243`.
- **MoE** (Mixture of Experts) — mélange d'experts routé top-k ; `reports/rapport-empreinte-memoire.md:242`.
- **MXFP4** — format microscaling 4 bits de gpt-oss, noyau « warp par ligne » bit à bit identique au CPU ; `reports/rapport-gpt-oss-perplexite.md:6`.
- **NLL** (Negative Log-Likelihood) — perte par position en nats ; `tools/compare_logits.py` ; `reports/rapport-gpt-oss-perplexite.md:76`.
- **N:M structuré (2:4)** — 2 non-nuls sur 4, forme matériellement supportée ; `reports/rapport-eparsite.md:19`.
- **NUMA** — effet invoqué pour une mesure de pull bruyante ; `reports/rapport-mur-memoire-4bits.md:48`.
- **PE** (Processing Element) — unité de calcul FPGA (« 124 MHz × 32 PEs ») ; `reports/rapport-empreinte-memoire.md:19`, `reports/rapport-inference.md:194`.
- **PPL** — abréviation de perplexité ; `reports/rapport-gpu-topk-selection.md:271`.
- **PTX** — assembleur virtuel NVIDIA généré par `cuda_stub.h` ; `reports/rapport-gpu-topk-selection.md:113`.
- **PushMat** — encodage de liste « écart + valeur int8 » de `src/list.rs` ; `reports/rapport-inference.md:31`.
- **ReLU** — activation à zéro franc (PowerInfer/TurboSparse), opposée au SiLU du projet ; `reports/rapport-eparsite.md:8`.
- **RMSNorm** — normalisation racine-carré-moyen (Qwen2, hyper-connexions) ; `reports/rapport-execution-v41.md:34`.
- **RoPE** (Rotary Position Embedding) — rotation positionnelle ; `rope_yarn`, `attn_derope` ; `reports/rapport-gpt-oss-perplexite.md:91`.
- **RSS** (Resident Set Size) — mémoire résidente maximale ; `reports/rapport-execution-v41.md:18`.
- **SHA-256** — empreinte vérifiant les 1 587 tenseurs convertis ; `tools/convertir_clusters.py` ; `reports/rapport-lecteur-multifichiers.md:11`.
- **SiLU** — activation lisse (`silu`) du greffon et du MLP ; `reports/rapport-harnais.md:14`.
- **SIGABRT** — mort du client réseau sur réponse de mode/taille différents ; `reports/rapport-mode4-lot-listes.md:90`.
- **Sinkhorn** — normalisation itérative (20 itérations) des hyper-connexions de V4.1 ; `build_hc_sinkhorn` ; `reports/rapport-execution-v41.md:34`.
- **SparseGPT / Wanda** — méthodes d'élagage *one-shot* situant la limite 50-60 % ; `reports/rapport-eparsite.md:71`.
- **SWAR** (SIMD Within A Register) — décodeurs d'écarts de `src/engine.rs` ; `reports/rapport-inference.md:32`.
- **SwiGLU** — MLP gate × up, forme du greffon `a = silu(u·x)·(v·x)` ; `src/model.rs` ; `reports/rapport-greffon.md:12`.
- **top-k / top-1 / top-8 / top-6 / top-40** — sélection des k plus grands scores (routage, attention, échantillonnage) ; `--attn-topk`, `--act-topk` ; `reports/rapport-empreinte-memoire.md:208` ; top-40 `reports/rapport-inference.md:39`.
- **TurboSparse** — modèle PowerInfer entraîné à ≈ 90 % de creux ; `reports/rapport-localite-activation.md:17`.
- **TTFT** (Time To First Token) — 74–95 ms ; `reports/rapport-inference.md:83`.
- **varint** — écart à longueur variable des listes d'événements ; `reports/rapport-inference.md:112`.
- **VRAM** — mémoire des cartes (miroirs KV/top-k, cache d'experts) ; `reports/rapport-empreinte-memoire.md:473`.
- **warp** — unité d'exécution GPU ; aussi index de tête dans `attn_kv_recombine` ; `reports/rapport-gpu-topk-selection.md:219`.
- **YaRN** — extension RoPE (interpolation basses fréquences + température `mscale = 1 + 0,1·ln f`) ; `rope_yarn` ; `reports/rapport-gpt-oss-perplexite.md:13`.

**Formats, fichiers, artefacts**
- **cluster-XX.gguf / commun.gguf** — format « modèle éclaté » : métadonnées + 8 clusters d'experts ; `tools/convertir_clusters.py` ; `reports/rapport-lecteur-multifichiers.md:19`.
- **GGUF** — conteneur de modèle lu par `src/gguf.rs` (`Gguf::open`, `Gguf::open_meta`) ; `reports/rapport-inference.md:22`.
- **mapping.tsv** — table `expert global → (fichier, ligne locale)`, 6 144 entrées ; `reports/rapport-lecteur-multifichiers.md:226,240`.
- **mmap** — mappage mémoire des poids (défaut ; `DRAVE_MMAP=0` → `read_to_end`) ; `reports/rapport-empreinte-memoire.md:9`.
- **QPAT** — en-tête du greffon `QPAT | version | couche | n | u[n] | v[n] | d[n]` ; `tools/make_patch.py`, `--patch` ; `reports/rapport-greffon.md:19`.
- **shard** — fichier d'un GGUF découpé (V4-Flash 3, Kimi 8, GLM 6) ; `reports/rapport-lecteur-multifichiers.md:30`.
- **Q4_0 / Q4_1 / Q8_0 / F16 / F32 / I8** — types ggml déquantifiés ou importés verbatim ; `src/gguf.rs` ; `reports/rapport-gpu-topk-selection.md:45`, `reports/rapport-empreinte-memoire.md:251`.
- **O_DIRECT** — ouverture directe échouant (errno 29), régime froid non mesuré ; `reports/rapport-empreinte-memoire.md:494`.
- **pread** — lecture positionnelle au retour non vérifié (faux 2 211 Go/s) ; `reports/rapport-empreinte-memoire.md:493`.
- **JSON `<arch>.config`** — bloc de configuration lu dans le GGUF ; `reports/rapport-execution-v41.md:47`.

**Matériel**
- **DDR3 / PCIe x8 / fmax 124 MHz** — débits et fréquence mesurés de la Stratix V GS D5 ; `reports/rapport-minimal.md:59`.
- **NVMe** — support de chargement à la demande (aléatoire 5,5 Go/s), seul retenu ; `reports/rapport-empreinte-memoire.md:299`.
- **Quadro RTX 5000 / RTX 5000** — GPU de mesure (« 2 Quadro, 32 Go » / « deux RTX 5000 ») ; `reports/rapport-empreinte-memoire.md:473`, `reports/rapport-localite-activation.md:62`.
- **Stratix V GS D5** — FPGA cible ; `reports/rapport-minimal.md:57`.
- **Xeon E5-2687W v3** — CPU de mesure (2 ×, 20 cœurs / 40 logiques) ; `reports/rapport-inference.md:5`.

**Vocabulaire du projet**
- **aiguillage** — remplacement de `matvec_q4` par un dispatch par format ; `reports/rapport-mla-experts.md:99`.
- **capteur hebbien / hebbien** — profileur de co-activations (`--hebbian`) ; conclusion : nœud linéaire redondant, nœud-produit non ; `reports/rapport-greffon.md:21`.
- **densité d'activation** — neurones « tirés » (seuil 5 % du max) ; `--profil-neurones` ; `reports/rapport-localite-activation.md:43`.
- **débit variable** — débit dépendant des événements/token (quasi constant sur transformer dense) ; `reports/rapport-harnais.md:41`.
- **engram** — table creuse à accès aléatoire par n-grammes (`blk.N.engram_embd.weight`), 203,4 Go de V4.1, destinée au mmap ; `reports/rapport-empreinte-memoire.md:9`.
- **expert partagé (shexp)** — FFN toujours actif (`ffn_*_shexp.weight`) jamais calculé ; `vue_unique` ; `reports/rapport-mla-experts.md:128-131`.
- **grappe** — groupe de destinations/experts (afférentes/efférentes), unité de chargement et de découpage ; `reports/rapport-empreinte-memoire.md:15`.
- **greffon** — neurone ajouté à une couche sans réentraînement (`--patch`) ; `reports/rapport-greffon.md:12`.
- **hyper-connexion** — état résiduel en `hc = 4` copies mélangées par Sinkhorn, non implémenté ; `hc_mult`, `hc_sinkhorn_iters` ; `reports/rapport-execution-v41.md:34`.
- **mode 2** — un flux par jeton, listes avec perte (1 608 octets/flux) ; `reports/rapport-mode4-lot-listes.md:12`.
- **mode 3** — lot dense `t × dimension × f32`, sans perte (3 663 octets/jeton) ; `reports/rapport-mode4-lot-listes.md:10`.
- **mode 4** — lot en listes auto-délimitées par préfixe de 12 octets `a_j · n_blocs_j · longueur_j` ; `reports/rapport-mode4-lot-listes.md:11`.
- **n-gramme** — motif jusqu'à 4 tokens indexant l'engram (hâchage 48 nombres premiers, vocabulaire comprimé 99 092) ; `reports/rapport-empreinte-memoire.md:259`.
- **paire** — un flux/destination ; en modes 1-2, `n` compte des PAIRES (indice + valeur) ; `tools/pair_factice.py` ; `reports/rapport-mode4-lot-listes.md:82`.
- **poids aberrants** — hétérogénéité de magnitude (95,9 % des poids d'`attn_output` sous 5 % du max) ; levier SparseGPT, pas la clustérisation ; `reports/rapport-modele-reel.md:64`.
- **porte / porte de correction / porte de non-régression** — perplexité de référence servant de test (19,3885 ; 15,1757 ; 15,2789 ; 799,8557 ; 268 786,6218) ; `reports/rapport-empreinte-memoire.md:45`.
- **pull** — parcours des lignes de la matrice (produit scalaire), opposé au push ; `seuil_push = 0,22` ; `reports/rapport-inference.md:32`.
- **push** — dispersion d'événements dans un accumulateur ; `reports/rapport-inference.md:32`.
- **SparseVec** — vecteur creux du chemin par listes d'événements ; `reports/rapport-localite-activation.md:24`.

**Variables d'environnement et drapeaux**
- **DRAVE_TRACE_EXPERTS** — écrit les traces de routage réelles ; `reports/rapport-empreinte-memoire.md:19`.
- **DRAVE_GPU / DRAVE_GPU_KV / DRAVE_GPU_TOPK** — projections déportées, miroir KV, top-k d'attention déporté (opt-in) ; `reports/rapport-execution-v41.md:19`, `reports/rapport-gpu-topk-selection.md:179`, `:169`.
- **DRAVE_MMAP=0** — désactive le mmap (`read_to_end`) ; `reports/rapport-lecteur-multifichiers.md:182`.
- **DRAVE_CLUSTERS** — restreint les clusters chargés (nœud partiel) ; `reports/rapport-lecteur-multifichiers.md:125`.
- **DRAVE_PRELIRE_TOUT=1** — prélecture de tous les poids ; `reports/rapport-execution-v41.md:19`.
- **DRAVE_YARN_MSCALE / DRAVE_YARN=1** — température YaRN séparée / YaRN de référence ; `reports/rapport-gpt-oss-perplexite.md:187`, `:209`.
- **DRAVE_DEBUG_MLA=1 / DRAVE_DEBUG_ETAT=1** — impression étagée des tenseurs MLA et de l'état ; `reports/rapport-mla-experts.md:146`, `:187`.
- **Drapeaux CLI** — `--dense`, `--q4`, `--q4-attn`, `--q4-ffn`, `--q4-tout`, `--keep`, `--lot`, `--flux-blocs`, `--limit`, `--logits-bin`, `--ppl-profil`, `--infer`, `--banc-topk`, `--attn-topk`, `--act-thresh`, `--abits`, `--threads`, `--ctx`, `--patch`, `--tensors`, `--config`, `--materiel`, `--sonder-engram` ; ex. `--q4` `reports/rapport-mur-memoire-4bits.md:198`, `--logits-bin` `reports/rapport-logits-gpu-vs-cpu.md:27`, `--ppl-profil` `reports/rapport-gpt-oss-perplexite.md:215`.

**Absents des 20 fichiers (demandés mais non trouvés)** : AER, DRVF/v5, TLB, HBM, LoRA, MTP, Hadamard, GFLOPS, Gbit/s, MTok/s, « liste valuée », « aiguille »/`tools/aiguille.py`, TSV (seul `mapping.tsv` existe), FIM.

## B. Chiffres et affirmations mesurées

**reports/rapport-empreinte-memoire.md**
- `:3-5` — «Modèle d'étude : Qwen3-30B-A3B (48 couches, 128 experts, top-8) [...] Cible : DeepSeek-V4.1-Flash (40 couches, **384 experts**, top-6, 365,7 Go)».
- `:7-10` — «l'empreinte de V4.1 tombe de 365,7 Go à **50–80 Go** [...] **56 % du modèle (203 Go) est une table d'engram creuse par nature** [...] Une session de 10 000 jetons n'en touche que **4,6 Mo**».
- `:27-30` — «| 64 experts | 59,64 | 51,69 | 5,31 | [...] | **1 expert** | **0,40** | **0,21** | **0,04** |».
- `:36-46` — «| 0 (référence) | **7,6139** | — | [...] | 0,25 | 727 099,03 | ×95 500 |» ; «Seulement 12,5 % des neurones tirent, et les 10 % les plus lourds portent 82 à 86 % de la masse».
- `:49-50` — «« projections : 0,0 M événements par token ». La sparsité est calculée et jetée.»
- `:54-65` — «Tokenisation de 8,3 Mo de français (3 050 991 jetons) [...] | 3 050 991 | **19 793** | **13,03 %** |» ; «Exposant de Heaps ≈ **0,21**».
- `:71-76` — «| complète (151 936 tokens) | **25,3748** | [...] | restreinte aux 19 793 tokens français | **24,3108** |».
- `:82-90` — «| rang médian du vrai token | **3** | [...] | p90 | 250 | [...] | maximum | 4 319 |» ; «| **top-16 384** | **100,0 %** |».
- `:94-104` — «**top-1 français dans 126 cas (99,2 %)**. Masse hors vocabulaire français : médiane **0,44 %**, mais maximum 40,4 %» ; «| 0 | 1 087 | **20 212** | 50 999 | [...] | 126 | 1 | **2** | 4 |».
- `:116-127` — «| français / anglais | 0,752 | **r = 0,102** | [...] | **français / français** | **0,805** | r = 0,995 |» ; «Experts « propres » à une langue : **1,7 à 3,1 %**» ; «reconnaît le corpus d'origine dans **79,8 %** des cas».
- `:136-142` — «| Jaccard | **0,499** | 0,088 | 0,056 | 0,065 |».
- `:148-152` — «| couches extrêmes (0-3, 44-47) | **0,259** | [...] | couches médianes (20-27) | **0,056** |» ; «**Facteur 4,6** [...] L'entrée est plus marquée que la sortie (0,499 contre 0,349).»
- `:158-163` — «| 0 / 47 | 0,030 | [...] | 1 / 46 | 0,028 | [...] | voisines (l, l+1) | 0,034 |».
- `:169-184` — «| 1 à 11 | ~0,035 | [...] | **12** | **0,323** | [...] | **24** | **0,210** |» ; «16/28 : 0.549 [...] 19/31 : 0.461» ; «**32–55 %**».
- `:196-210` — «| couches extrêmes | 60,0 | 92,2 | 0,575 |» ; «| **47** | **36** | 64 | / | 0 | 74 | 108 |» ; «en dessous de 8 experts, un cache ne sert **à rien** (0 % de succès)».
- `:216-221` — «| 16 | 2,34 Go | 59,6 % | 59,6 % | −0,0 % | [...] | 48 | 7,03 Go | 89,4 % | 90,6 % | +1,2 % |».
- `:227-231` — «| aucun (à froid) | 77,9 % | 78,5 % |» ; «Le cache atteint son régime en **32 jetons** (59 % à 8 jetons, 80,5 % à 32)».
- `:241-251` — «| **engram** | **203,4** | **55,6 %** | / experts (MoE) | 152,9 | 41,8 % | / attention (MLA) | 5,4 | 1,5 % |» ; «**`blk.N.engram_embd.weight`, à 101,4 Go par couche** [...] en I8, de forme `[384 006 168, 264]`».
- `:257-264` — «| entrées | 384 006 168 par couche | [...] | taille d'une entrée | 264 octets | [...] | hâchage | 48 nombres premiers | [...] | vocabulaire comprimé | 99 092 |».
- `:272-280` — «| 3 050 991 | 19 793 | 227 495 | 556 188 | 880 394 | 1 683 870 | **444,5 Mo** |» ; «Le rapport est de 1 pour 22 000».
- `:290-297` — «| 12 | **49,8 %** | 6,2 % | [...] | 47 | **51,9 %** | 6,2 % |» ; «Un cache « experts du jeton précédent » — 8 entrées [...] sert 27 à 52 % des appels. Mais un LRU de 32 fait **78 %**».
- `:303-314` — «| 47 | **30,8** | 99,6 |» ; «Sur NVMe [...] lire 8 experts dispersés coûte exactement ce qu'ils pèsent» ; «(0,06 Go/s en aléatoire)».
- `:318-321` — «Le calcul d'une couche coûte **0,6 ms**, sa lecture **10,9 ms** : un rapport de **18×** [...] ne masquerait que **6 %** de l'attente.»
- `:325-348` — «Les 28 sessions du `journal/` (59 Mo, 2,5 M jetons)» ; «| **journal** | 16,9 | 30,8 | 41,6 | **58,1** | 92,5 |» ; «| **anglais** | **11,4** | **23,0** | **31,6** | **44,5** | **72,7** |» ; «**18 Go d'écart**».
- `:352-367` — «| **moyenne** | **58,1** | 59,3 | **44,5** |» ; «+14 à la couche 47».
- `:371-379` — «| couches 0-3 (**entrée**) | **75 à 82** | / | couches 16-30 (milieu) | **42 à 49** |».
- `:383-392` — «| **2 510 800** [...] | 1 470 860 | **388 Mo** | **0,38 %** |» ; «19 228 tokens (12,66 %)».
- `:404-417` — «| 0 | gate | 0,185 | 0,001 | 0 | [...] | 47 | gate | 0,187 | 0,011 | 0 |» ; «~**78 % des colonnes** portent 80 % du poids».
- `:425-441` — «| 12/24 | **+0,343** | [...] | 18/30 | **+0,389** |» ; «maximum mesuré : 0,49».
- `:448-455` — «stocker W(L+12) comme W(L) + résidu | **non** — le résidu porte 88 % de l'énergie |» ; «**piste ouverte** — 35 % de variance partagée».
- `:461-476` — «experts (top-6 × 40 couches × 9,95 Mo) | **2,39 Go** |» ; «tête de sortie (129 280 × 5120, F16) | **1,32 Go — 36 % du trafic** |» ; «base | 3,71 Go |» ; «cache d'experts 25 % | 1,82 Go |» ; «tête restreinte à la langue | **0,70 Go** |» ; «3 200 experts = 21 % du total» ; «551 424 experts pour 6 144 distincts — **un facteur 90**».
- `:480-490` — «| VRAM (2 GPU) | ~750 Go/s | 9,7 Go en 13 ms |» ; «| RAM | ~20 Go/s |» ; «| NVMe, aléatoire | **5,5 Go/s** |» ; «| NVMe, séquentiel | 2,1 Go/s |» ; «| **disque mécanique, aléatoire** | **0,06 Go/s** | 62,9 Go en 1 098 s — **3,5× pire** |» ; «coûteraient 40 s».
- `:493-495` — «a chronométré ce disque à **2 211 Go/s** [...] `O_DIRECT` échoue par ailleurs ici (errno 29)».
- `:499-508` — «| engram (2 couches) | 202,8 Go | **0,4 Go** | **1 / 500** |» ; «| **total** | **365,7 Go** | **~50 à 80 Go** | **1 / 5 à 1 / 7** |».
- `:518` — «53 Go en anglais contre 71 en français.»
- `:526` — «**La tête restreinte par langue** : −30 % de trafic».
- `:534-536` — «un disque mécanique à 2 211 Go/s, une allocation de cache à 4,1 % partout, un total de 4 231 Go».
- `:538-540` — «la perplexité restreinte qui *baisse* de 25,37 à 24,31».

**reports/rapport-encodage.md**
- `:8` — «Modèle : MLP 32→64→10 (2688 poids), référence float 76.07 %».
- `:14-29` — «| non structuré | 1 | 26.9 % | 45.02 % | 1.27 | **3.52** | 10.03 | 2.00 | 0.90 | 3.6 |».
- `:35-42` — «| 1.04 | 42.87 % | 10.6 | [...] | 1.50 | 72.46 % | 7.4 | [...] | 2.00 | 4971.00 % | 5.5 | dense ternaire (référence CDC) |».
- `:51-57` — «| 100.0 % | 2.000 | **2.282** | 0.88× | 4.8 | ×0.88 | [...] | 1.0 % | 1.010 | **0.151** | ×6.71 | 73.3 | ×13.28 |».
- `:59-61` — «**Bascule vers 20 % de densité** [...] (×4,2 à 5 %, ×13 face au dense 2 bits à 1 %)».
- `:78-80` — «l'entropie des positions vaut 0,288 b/poids contre 0,476 pour les listes — il reste un facteur 1,65».
- `:83-84` — «sur un LLM réel, 5-12 % de densité demande un réentraînement lourd».

**reports/rapport-eparsite.md**
- `:3` — «accuracy float **76.07 %**, ternaire (non élagué) **49.71 %**».
- `:7-9` — «poids non nuls : **26.3 %** [...] activations non nulles après ReLU : **52.8 %** [...] événements réels : **13.9 %**».
- `:13-19` — «| **bitmap + signe** | **1 + d** | **1,50** | **1,25** |» ; «| CSR bloc 16 b | 17·d | 8,50 | 4,25 |».
- `:29-36` — «| 100.0 % | 26.3 % | 49.71 % | 2.00 | 1.26 | [...] | 3.1 % | 0.9 % | 47.66 % | 2.00 | 1.01 |».
- `:40-46` — «| csr32 vs dense2 | 6.1 % | csr32 | [...] | csr16 vs bitmap | 6.2 % | csr16 |».
- `:50-57` — «| 6.2 % | 5.5 | 10.4 | 10.4 | 5.4 | 7.4 |».
- `:64` — «~21 LUT pour un 64:1, soit ≈ 3 400 ALM pour 312 voies (**2 % du FPGA**)».
- `:65` — «Le saut de blocs entièrement nuls (1 bit par bloc de 64) [...] à 1,6 % de surcoût.»
- `:69` — «Les variations observées (±4 pt) sont dans le bruit d'un jeu de test de 1 024 exemples».
- `:70-71` — «BitNet b1.58 tourne plutôt autour de 50-70 % de non-nuls : [...] ×1,2 à ×1,4» ; «**Au-delà de ~90 % de zéros, un LLM généraliste s'effondre**».

**reports/rapport-execution-v41.md**
- `:3-4` — «365,71 Go, 1 046 tenseurs, 40 couches, 384 experts dont 6 par jeton».
- `:8-9` — «**la passe avant est refusée en 0,33 s** [...] **Aucun chiffre de calcul sur V4.1 n'existe**».
- `:15` — «1 046 tenseurs, **365,70 Go** lus en **63,8 ms**».
- `:17` — «20 threads, 16 lecteurs disque, cache experts 19,5 Go, cache KV 32 bits».
- `:18` — «table 1 : 10 000 entrées en **524 ms** (2,6 Mo touchés sur 101,4 Go) · table 2 : **219 ms** · RSS max **120 Mo**».
- `:19` — «**refusée en 0,33 s**, RSS 47 Mo».
- `:30` — «`llama.cpp/src/models/deepseek4.cpp` (1 253 lignes)».
- `:34-37` — «**hc = 4** copies [...] **Sinkhorn** à 20 itérations» ; «`o_groups = 8`» ; «`candidate_topk_blocks = 2048`».
- `:49` — «corrélation 0,999024».
- `:70` — «Le moteur refuse donc, et le refuse en 74 ms.»
- `:79` — «# 203 Go de tables adressées, 5 Mo touchés».

**reports/rapport-gpt-oss-perplexite.md**
- `:3-6` — «`/tmp/wt2_txt.txt` (20 000 premiers octets de `data/wikitext2_test.txt`), gpt-oss-120b MXFP4, `--ctx 256 --dense --threads 16`».
- `:10` — «perplexité **39,8** « au lieu de l'ordre de 6 » [...] (39,8 à 63 jetons, 129,9 à 511)».
- `:28-29` — «| avant (biais O ignoré) | **39,80** | / | après (biais O chargé) | **20,84** |».
- `:44-51` — «| fenêtre une couche sur deux (motif 2, corrigé) | **15,08** |» ; «fenêtre glissante 128 sur 18/36 couches (motif 2 alterné)».
- `:60` — «20,8361 avant, 20,8361 après, au chiffre près».
- `:72-78` — «| 63 jetons, YaRN | **38,37** | **41,11** |» ; «| 511 jetons [...] | **169,67** | **174,34** |» ; «corrélation des logits **0,999976** [...] \|ΔNLL\| médian 0,076, max 1,49».
- `:91-92` — «| RoPE simple | **20,84** | **18,58** | / | YaRN ×32 | 41,11 | 174,34 |».
- `:99` — «**0,27 % d'écart au plus sur une fréquence, aucun sur les 18 autres**».
- `:105` — «la concentration `0,1·ln(32)+1`».
- `:127-134` — «| `analysis` | **0,9999** | / | `final` | 0,0001 |» ; «NLL 13,4 pour une uniforme à 12,2».
- `:137-144` — «| **montage canonique** [...] | **26,0** | / | même montage, `analysis` retiré | 9 625 | / | **texte brut, même contexte** | **13,7** |».
- `:150` — «le facteur 370 entre les deux».
- `:152-153` — «de 9 625 à 677 321 — le modèle prédit « Chat » avec p = 0,77».
- `:162-163` — «Les 4 424 identifiants [...] **identiques un à un** à ceux de `llama-tokenize` (0 écart)».
- `:174-175` — «`--tokenize` passe de ~60 s à **0,385 s** [...] (19,3885)».
- `:191-194` — «| 512 | **18,58** | 19,65 | 174,34 | [...] | 4 096 | **170,78** | 400,13 | — |».
- `:196-200` — «divise la perplexité par **8,9** à 512, 5,9 à 1 024, 3,8 à 2 048».
- `:219-221` — «0-255 : 13,715 [...] 3584-3839 : 542,885».
- `:227-230` — «(jetons 1400-1659) donne 59,36 **à la position 0**, contre 13,94 [...] un facteur ~7 de plus».
- `:233-234` — «llama.cpp [...] donne 714,83 ; notre moteur 722,56 (1,1 % d'écart) [...] les 3 à 7 % mesurés à 63 et 512 jetons».
- `:246-247` — «sans YaRN : « Canberra. » ; avec : « The capital city of Australia is Canberra. »».

**reports/rapport-gpu-scores.md**
- `:3-4` — «un écart de **1,6 à 2,3e-7** [...] **40× plus vite** à 262 144 clés».
- `:22-23` — «(2 têtes KV × 64, 7 têtes de requête par tête KV), KV int8, un Quadro RTX 5000».
- `:40-43` — «| **262 144** | 257,9 ms | **6,36 ms** | **40,6×** | 1,03e-7 |».
- `:50-52` — «| 4 096 | 3,88 ms | **0,12 ms** | **31,6×** | 1,60e-7 | [...] | **262 144** | 243,82 ms | **6,09 ms** | **40,0×** | 2,25e-7 |».
- `:59-62` — «le GPU tournait à 1,2 Go/s» ; «(une tranche ≈ 256 clés, plafonnée à 128 tranches)».
- `:68-73` — «`_Z11attn_scoresPKvPKfS2_Pfiiiiiif`» ; «écart relatif **1,24**».

**reports/rapport-gpu-topk-selection.md**
- `:3-8` — «**quatre passes d'histogramme + deux noyaux de collecte** [...] **0,89 ms** là où le tri CPU en coûte **497 ms** [...] **2,7–4,8e-7**».
- `:15-16` — «de 10 à 13 noyaux [...] puis à **14** [...] — 956 lignes».
- `:45-48` — «k = 256, 2 têtes KV × 64 dim, 7 têtes de requête par tête KV (**14 lignes**), cache KV 8 bits».
- `:51-56` — «Les TEMPS [...] varient de ±50 % [...] 0,45 ms puis 0,30 ms de collecte à 262 144 clés».
- `:60-62` — «| 4 096 | [...] | 0,14 ms (9×) | 1,31 ms | 0,13 ms (35×) | 4,33 ms |» ; «| 262 144 | [...] | 0,44 ms (224×) | 97,88 ms | 0,45 ms (896×) | 399,21 ms |».
- `:68-70` — «n = 1 avec k = 1 ; n = 100 avec k = 3 ; n = 4 097 et n = 5 000 [...] n = 8 191 avec k = 4 096».
- `:81-84` — «l'écart du **noyau 1** n'est plus 1,03e-7 mais **1,60 à 2,25e-7** [...] 4× sous le critère de 1e-6».
- `:88-93` — «le k-ième score **change** [...] sur 5 à 7 des 14 lignes».
- `:98-103` — «**14/14 lignes identiques**, 0,45 ms de collecte et 0,27 ms de seuil à 262 144 clés» ; «un débordement en VRAM silencieux».
- `:117` — «(56 lancements au lieu de 4)».
- `:125-127` — «≈1 100× trop rapide pour la collecte et ≈900× pour le seuil (0,0004 ms au lieu de 0,45 ms)».
- `:142-145` — «| 100 | 3 | 0,03 ms | 0,02 ms | **1,04e-7** | [...] | 262 144 | 256 | 0,07 ms | 0,98 ms | **2,70e-7** |».
- `:147-153` — «Le temps GPU est **constant** (0,07 ms de 4 k à 262 k clés)» ; «**Limite** : k ≤ 1 024».
- `:159` — «dénominateur ×45,7 et sortie 55× trop petite à k = 1 ; écart relatif 2,05e-1».
- `:167` — «`groupe = fen == 0 && self.attn_topk == 0 && rep > 1`, `model.rs:3150`».
- `:178-179` — «| CPU | 9,4167 | 41,59 s | / | **GPU** | **9,4162** | 41,45 s |».
- `:192-194` — «| 2 048 | 511 | 255 | **4,21** | 7,68 | 13,1358 / 13,1355 | 18,1 / 20,4 s |» ; «| **16 384** | 4 095 | **2 047** | 19,58 | **7,59** | [...] | **203,7 / 155,5 s (−24 %)** |».
- `:202-207` — «**Le croisement en clés est donc entre 255 et 2 047 clés** [...] (~4 000 clés d'après `docs/contexte-long.md`)» ; «17 434 jetons [...] dans `/tmp/ids_qwen_long.txt`».
- `:209-211` — «« les tampons alloués à chaque appel : 24,5 ms/jeton au lieu de 2,9 »» ; «~74 000 lancements pour ces 511 jetons».
- `:222-225` — «(64 têtes de requête, 8 têtes KV, puits allant de −1,95 à +3,38) [...] jusqu'à **4,65 logit** d'écart — un facteur 105».
- `:231-234` — «| avant correction | **17,6531** | / | après correction | **15,1786** | / | référence CPU | 15,1757 |».
- `:253-262` — «| 4 096 | **0,13 ms** | 0,22 ms | 7,19e-7 | [...] | 262 144 | 1,58 ms | **1,35 ms** | 7,01e-7 |» ; «le seuil de bascule est donc **mesuré** (131 072)».
- `:273-283` — «| 8 191 | 4 095 | 38,84 | **4,97** | — |» ; «**Le croisement est à ~300 clés** [...] **7,8× plus rapide**» ; «(+0,0043 ms par clé et par jeton)» ; «identique à 2e-5 près».
- `:294-297` — «(15,1666) est celle du chemin GPU dense (15,1667), l'écart de 6,6e-5 avec le CPU (15,1757)».
- `:304-308` — «| CPU, top-k 256 | 19,0740 | **+2,66 %** | [...] | GPU, top-k 256 | 18,8391 | **+2,90 %** | [...] | GPU sans miroir KV | 18,3538 | −1,22 % vs CPU |».
- `:313-317` — «**l'écart CPU/GPU de 1,2 à 1,5 % n'est PAS le miroir KV** [...] soit −0,25 % pour le miroir» ; «un effet de 0,06 % à ctx 256».
- `:325-329` — «`monotone(-0,0) = 0x7FFFFFFF` et `monotone(+0,0) = 0x80000000`».
- `:340-345` — «| 1 | `attn_scores` | ✅ 1,6–2,3e-7 · 26,7–40× |» ; «chaîne complète **3,90 ms** pour 14 lignes × 1 M clés contre 539,9 ms [...] (×138) et 13,2 ms en VRAM».
- `:347-349` — «Le top-k GPU n'est donc **pas encore branché dans le moteur**».

**reports/rapport-grappes.md**
- `:10-14` — «| 0.0 % | 74.12 % | 346 | 12.9 % | 0.0 % | 2.40 | 0.39 | [...] | 100.0 % | 76.07 % | 708 | 26.3 % | 75.0 % | 3.43 | 0.79 |».
- `:18-19` — «modèle en grappes pures : **74.12 %** [...] (32→7→10, 311 paramètres) : **74.12 %**».
- `:26-32` — «| 1.0 % | 27.7 % | 72.5 | 15.1 | [...] | 100.0 % | 100.0 % | 262.1 | 54.6 |».
- `:42-43` — «l'élagage en blocs perdait 11 points à densité égale».
- `:57` — «Mesures sur un MLP de 2 688 poids».

**reports/rapport-greffon.md**
- `:15` — «a = silu(u · x) · (v · x) [...] : a · d».
- `:23-26` — «les 4 864 neurones d'origine n'apparient que `gate[i]` avec `up[i]`».
- `:33-42` — «Perplexité sur 1 020 tokens de WikiText-2, couche 12, greffon croisé `gate[0] × up[7]`» ; «| **aucun** | **23,6125** | / | **nul** | **23,6125** | **0,0000** | / | croisé, échelle 5,0 | 23,6253 | +0,0128 |».
- `:58-59` — «100 évaluations/heure [...] 2 400 évaluations par jour».

**reports/rapport-harnais.md**
- `:3-7` — «WikiText-2 test (4080 tokens évalués) [...] **PPL = 24.77**».
- `:9` — «un Qwen2.5-0.5B correct tourne autour de 15-25».
- `:17-18` — «| 0 | 0.00 % | 0.00 % | 13.0 M | 1.8 M |» (×24).
- `:45-50` — «| Moyenne | 354.88 M | [...] | p95 | 354.88 M | [...] | Écart-type / moyenne | 0.0 % |».
- `:67-68` — «⚠️ Mesure faite sur une seule fenêtre de tokens».

**reports/rapport-inference.md**
- `:3-5` — «**2 319 lignes de Rust, `std` seul, zéro dépendance.** [...] Q8_0 (507 Mo, 494 M de poids) [...] (2 × Xeon E5-2687W v3)».
- `:18` — «généré  : 38 tokens en 3.86 s  (9.85 tok/s)».
- `:30-35` — «`src/gguf.rs` [...] 332 | [...] `src/list.rs` [...] 321 | [...] `src/engine.rs` [...] 510 | [...] `src/tokenizer.rs` [...] 371 | [...] `src/model.rs` [...] 403 | [...] `src/main.rs` [...] 382».
- `:51-57` — «**16/16 identiques.** [...] | 0 | 358 (17,3063) | 358 (17,0202) |».
- `:62-70` — «Perplexité WikiText-2 (2 040 tokens, fenêtres de 256)» ; «| numpy float32 | 25,0004 | / | **moteur d'événements (int16)** | **24,8995** |» ; «Écart : **−0,4 %** [...] que les 20,29 du harnais précédent».
- `:78-84` — «| Mémoire résidente | **1,27 Go** (dont 0,71 Go de listes) | / | Événements par token | **352,8 M** | / | **Débit de génération** | **10,5 tok/s** (int16) · 10,6 (int8) · **11,4 en dense** | / | Temps par token | 100 ms = 90 ms + 10 ms | / | TTFT | 74–95 ms | / | **3,9 G événements/s** |».
- `:88-94` — «| tok/s | 1,51 | 8,22 | **10,52** | 10,15 | 9,83 |» ; «un token paie **168 barrières** (7 matrices × 24 couches)».
- `:96-98` — «132 ms par token, soit 7,6 tok/s. **Le moteur d'événements est 38 % plus rapide que numpy+BLAS**».
- `:108-111` — «| **Listes d'événements** | 0,71 Go — **1,44 o/poids** | **10,52** | / | Matrice dense int8 | 0,49 Go — **1,06 o/poids** | **11,42** |» ; «**L'architecture événementielle coûte 8 % sur CPU** [...] 36 % de mémoire en plus».
- `:116-118` — «le dense a d'abord été 20 % plus **lent** (8,5 tok/s) [...] elle passe à 11,4 tok/s».
- `:131` — «un accumulateur de 151 936 × 8 octets **par worker** (36 Mo) [...] écrite 896 fois».
- `:135` — «Coût : 10 ms sur 100, soit 10 % du token.»
- `:146-151` — «| int8 (127 niveaux) | 299 M | 3 tokens sur 6 [...] | 10,3 | / | **int16 (32 767 niveaux)** | 353 M | **16 sur 16** | 10,0 |» ; «à 0,26 de logit».
- `:157-170` — «**737 cas sur 737**, plus 13 468 cas de fuzz» ; «diffèrent dans **5,2 % des cas** (38 sur 737)».
- `:172-174` — «la valeur absolue publiée précédemment (20,29) [...] devra être reprise».
- `:184-186` — «Elle est **30 % plus rapide que numpy + OpenBLAS** [...] avec 20 threads au lieu de 40.»
- `:193-197` — «3,9 G événements/s sur 20 cœurs ≈ 1 événement par cycle et par cœur [...] à 124 MHz × 32 PEs» ; «1,44 octet par poids — contre 1,06 pour Q8_0 dense».
- `:201-204` — «706 Mo par token en 95 ms, soit **7,4 Go/s sur les 28,7 Go/s mesurés** [...] (13,7)».
- `:210` — «vider l'accumulateur entier par fenêtre coûte… 0,2 % du temps de token.»
- `:214-219` — «| **sans la liste (borne haute cumulative)** | **14,74** | **69,4 ms** |» ; «**+35 %**, perplexité **identique au chiffre près** (24,8995) [...] de 3,6 à **5,3 G év/s**».
- `:225-230` — «« DIVERGENT au rang 0 : 0 vs 3513 »» ; «au rang 895».
- `:232-235` — «10,4 Go/s utilisés sur 28,7 → **2,8× avant d'être borné par la mémoire** [...] (11,4 tok/s)».
- `:244-262` — «| Fichier GGUF | 506 Mo | 337 Mo | **−33 %** | [...] | Listes en mémoire | 0,71 Go | 0,63 Go | **−11 %** | [...] | Événements par token | 352,7 M | 312,5 M | −12 % | [...] | RSS | 1,27 Go | 1,02 Go | −20 % | [...] | Débit | 10,33 | 11,78 | +14 % | [...] | **Perplexité WikiText-2** | **24,90** | **27,83** | **+12 %** |» ; «le format liste reste 2,7× plus gros».
- `:269-276` — «| 10 % | 35,6 M | 21,40 | 0,88 G év/s |» ; «**10× moins d'événements ne donnent que 2× de vitesse.**»
- `:285-288` — «| dispersé (magnitude) | 89,5 M | 66,1 ms | 13,77 | / | **contigu (fenêtre)** | 85,8 M | **50,1 ms** | **17,91** |» ; «**30 % plus rapide à taux égal**».
- `:296-303` — «| matvec, 10 % de poids | **31,3 ms** | 35,7 ms | 40,6 ms | 52,9 ms ❌ |» ; «À 32 workers il faut 1,2 Mo d'accumulateurs».

**reports/rapport-lecteur-multifichiers.md**
- `:10-11` — «(convertisseur, 1 587 tenseurs vérifiés par SHA-256)».
- `:17-24` — «(18,56 Go, un fichier, sur le disque mécanique) contre le même modèle éclaté» ; «| modèle d'origine | **15,2789** | 12,2 s | / | modèle en clusters | **15,2789** | 11,6 s |».
- `:32-44` — «(86,9 Go, 3 shards)» ; «| annoncé par les descripteurs | **86,90 Go** | / | somme des fichiers | **86,90 Go** | / | tenseurs | 1 328 (shard 1 : 0, shard 2 : 784, shard 3 : 544) | / | temps de lecture des en-têtes | 54 ms |».
- `:52-58` — «| tenseurs | **1 587** | / | poids | **18,55 Go** | / | chargement complet | 48 couches en 27,8 s | / | mélanges d'experts chargés | **48/48 couches** |».
- `:63-68` — «| Qwen2.5-0.5B ctx 256 | 19,3885 | **19,3885** | [...] | `cargo test --release` | vert | **32 verts** (20 au début du sprint) | [...] | nœud partiel | 268 786,6218 | **268 786,6218** |».
- `:87` — «(`ligne 0 : 2181034 au lieu de 271`)».
- `:93` — «**3,19 Go annoncés pour 18,55**».
- `:112-113` — «`cluster-100.gguf` se range avant `cluster-20.gguf`» ; «Au-delà de 99 clusters».
- `:120-121` — «l'incident `iq1_m` (8,56 Go annoncés pour 86,9)».
- `:158-165` — «**La concordance porte sur 984 Go** : DeepSeek-V4.1-Flash 365,70 = 365,7 · GLM-5.3 216,71 = 216,7 · Kimi-K2.7 303,90 = 303,9 · DeepSeek-V4-Flash 86,90 = 86,9 · GLM-5.3-Flash 93,08 = 93,1 · Qwen3-235B 85,68 = 85,7. **La file de 1 138 Go est terminée**».
- `:167-169` — «(`deepseek41`, `deepseek2`, `deepseek4`, `glm-dsa`) [...] Kimi est en huit fichiers, GLM en six».
- `:171-186` — «Le mmap : 3,3× plus rapide, 3× moins de mémoire» ; «| mappé (défaut) | **9,32 s** | **6,35 Go** | / | lu en entier (`DRAVE_MMAP=0`) | 30,68 s | 19,20 Go |».
- `:199-204` — «| 1 | 268 786,62 | **2,35 Go** | 9,64 s | [...] | **8** | **799,8557** | 6,28 Go | 10,65 s |» ; «**2,7× moins**».
- `:221` — «`index out of bounds: the len is 1 but the index is 6`».
- `:239-242` — «| conversion | 435 + 8 × 144 = **1 587 tenseurs**, 18,60 Go, 351,7 s | / | `mapping.tsv` | 6 144 entrées · 48 couches · 128 experts · 8 clusters | / | **1 587 tenseurs · TOUT CONCORDE** | / | **15,2789** |».
- `:263-264` — «`--lot 64` rend 15,2736 contre 15,2789 par jeton».

**reports/rapport-localite-activation.md**
- `:17` — «TurboSparse (≈ 90 % de creux) est *entraîné* ainsi».
- `:24` — «bascule push/pull mesurée à **22 % de densité** (`seuil_push = 0.22`)».
- `:27` — «seuil de rentabilité mesuré (8 Mo)».
- `:37` — «100 % des neurones à 16 bits (mesuré : densité de 51 104 %)».
- `:43-47` — «| densité d'activation (seuil 5 % du max) | **17,9 %** |» ; «12,3 % / **33,1 %** / 74,2 %» ; «**0,08 %**» ; «2,82 %» ; «173 à 1 579 tirs par jeton (×9) ; [...] 16,7 à 51,1 %».
- `:59-64` — «gpt-oss active 4 experts sur 128 par couche et par jeton» ; «(32 Go sur les deux RTX 5000, pour un modèle de 62 Go)» ; «le noyau MXFP4 « warp par ligne » tourne maintenant à 42 Go/s».

**reports/rapport-logits-gpu-vs-cpu.md**
- `:6-7` — «il les décale de **0,038 nat** en moyenne — **497 jetons sur 511 gardent le même top-1** (14 divergent), et cela suffit à déplacer la perplexité de 1,2 % [...] (top-8 sur 128)».
- `:13-17` — «| CPU | 18,5803 | — | / | GPU, miroir KV seul | 18,3074 | −1,47 % | / | GPU, projections seules | 18,3538 | −1,22 % |».
- `:19-22` — «ne pèse que **0,25 % de plus**» ; «(2e-7 sur la tête Q8_0, **0,00e0** bit à bit sur un expert MXFP4)».
- `:33-35` — «| perplexité | 17,4315 | 17,4315 | / | écart moyen \|ΔNLL\| | — | **0,0000** (max 0,0000) |».
- `:40-44` — «| écart moyen \|ΔNLL\| | — | **0,0379** (médiane 0,0123, p90 0,0836, max 1,3708) | / | accord du top-1 | — | **497/511** | / | corrélation | — | 1,000000 |».
- `:46-52` — «6× plus grand en moyenne que les autres (0,198 contre 0,033) [...] (1,3708 nat, position 284) [...] seules 3 des 14» ; «(511/511 annoncé, **497/511** mesuré)».
- `:65-68` — «l'écart de 0,06 % mesuré à `--ctx 256`» ; «La perplexité GPU est MEILLEURE (18,35 contre 18,58)».
- `:83-84` — «les portes du dépôt (15,1757 CPU / 15,1667 GPU à ctx 256)».

**reports/rapport-minimal.md**
- `:3` — «MLP 32→64→10, entraîné sur 4096 exemples synthétiques, évalué sur 1024».
- `:9-15` — «| float32 (référence) | 32.00 | 76.07 % | [...] | ternaire 1,58 b | 2.00 | 49.71 % | -26.37 pt | / | multi 4 plans ternaires | 8.00 | 75.98 % | -0.10 pt |».
- `:21-27` — «| Exactitude arithmétique — couche 1 | 4.233e-07 |» ; «| Erreur de quantification des activations — couche 2 | 6.322e-01 |» ; «| Accuracy chemin entier | 49.22 % |» ; «| Accumulateur max | 488 |».
- `:33-47` — «| float32 | 32.00 | 10.5 Kio | [...] | ternaire en CSR (CDC) | 10.10 | 3.3 Kio |».
- `:53-55` — «| 2 bits | 50.9 % | 27.5 % | / | 3 bits | 51.3 % | 44.1 % | 27.5 % | / | 4 bits | 51.5 % | 48.1 % | 42.8 % | 27.5 % |».
- `:59` — «DDR3 9,66 Go/s · PCIe x8 6,5 Go/s · fmax actuel 124 MHz».
- `:63-73` — «| 7B — ternaire 2 b | 1750.0 Mo | 181.159 | 5.5 | 312 | 9360 | [...] | 70B — ternaire CSR | 148750.0 Mo | 15398.551 | 0.1 | 37 | 1110 |».
- `:80-81` — «10.1 b/poids [...] et 61.8 b/poids [...] soit 5 à 15× plus de trafic» ; «~312 voies de MAC (≈ 9 400 ALM, 5 % du FPGA) [...] 96 % du device reste disponible».
- `:83` — «Ses chiffres de débit (§3, premières lignes) ne veulent rien dire».

**reports/rapport-mla-experts.md**
- `:12-15` — «| V4-Flash, V4.1 | `tenseur blk.3.attn_q.weight absent` |» ; «| GLM-5.3, Kimi | `mélanges d'experts chargés : 0/79` |».
- `:31-33` — «576 valeurs par jeton au lieu de 448 par tête dense (28 672 pour 64 têtes)».
- `:59-66` — «| 53 couches | IQ3_XXS | IQ1_S | / | 22 couches | IQ3_XXS | IQ2_XXS | / | 4 couches | **IQ4_XS** | IQ1_S | / | 1 couche | **Q3_K** | IQ2_XXS |» ; «D'où « 71/79 »».
- `:71-74` — «les huit déquantificateurs [...] comparés à libggml au bit près (`tools/portes_formats.sh`)».
- `:79-82` — «Faux pour GLM-5.3 (3 couches denses puis 76) et pour Kimi (1 puis 60)».
- `:92-100` — «**GLM-5.3 (216 Go)** : 79 couches MLA, 76/79 [...] ~85 Go de RSS [...] dont ~52 Go de tenseurs MLA déquantifiés en f32» ; «**Kimi-K2.7 (1 026 G poids)** [...] 61 couches MLA, routage sigmoïde ×2,827, 384 experts dont 8 par jeton» ; «**48 tests** (46 avant, +2)».
- `:106-113` — «| chargement | 379 à 553 s | [...] | mémoire de pointe | ~90 Go de RSS | [...] | **253 s par jeton** | [...] | **53 s par jeton** (dont 20 s d'attention) | [...] | **5 966** contre **4 286** chez llama.cpp | [...] | **0,999024** | [...] | **3/3** |».
- `:118` — «Le chemin a d'abord été faux (7,3 M de perplexité, corrélation −0,04)».
- `:121-126` — «(`qk_nope = 192`, `qk_rope = 64`, `v = 256`, `kv_lora = 512`)» ; «`rope.freq_base = 8e6`» ; «`index_topk = 2048` [...] un contexte de 16 jetons».
- `:155-160` — «| chargement | **161 s** (mmap, 1 026 G poids) | / | 2 jetons notés | **146 s** (73 s/jeton) | / | perplexité | 81 384 | / | avec les jetons de GLM | 1 236 804 |».
- `:174-188` — «llama.cpp : perplexité 890,4559» ; «| **+0,009** | +0,372 | +0,611 | **+4,070** | +3,118 | +2,041 | +1,583 |» ; «(4 807,76 contre 4 807,07)».
- `:217` — «| **1,9 %** | **1,3 %** | **3,8 %** | **4,0 %** |».
- `:227` — «un bug de disposition donnait 5e-4 au lieu de 1,5e-3 sur `kqv_out`, soit 300 %».
- `:235-236` — «`/tmp/ref_glm_8p.log` ; le moteur met ~190 s par jeton».

**reports/rapport-mode4-lot-listes.md**
- `:3-15` — «1,5 ko par jeton contre 3,5» ; «`a_j · n_blocs_j · longueur_j`» ; «(indices par écarts u8 [...] valeurs i8, une échelle f32 par bloc de 32 canaux)».
- `:26-35` — «| mode 2 [...] | 1 608 par flux | 2,74e-2 | / | **mode 4, lots de 16** | **1,5 ko** | **3,03e-2** |» ; «**÷2,2 sur les octets** [...] 3 663 octets par jeton en lot DENSE (mode 3), 1 608 en mode 2, **1 500 en mode 4**» ; «un relecteur a mesuré 1 671 contre 1 600, soit 1,02×» ; «à 1,11× celui du mode 2».
- `:44-48` — «| 20 | 2,30e-1 | 4,09e-2 | **5,6×** | [...] | 256 | 6,46e-2 | 5,64e-2 | 1,15× |».
- `:56` — «`--limit 20 --lot 20` et `--limit 20 --lot 16` (16 + 4) donnent la **même** perplexité (157,3415)».
- `:73-80` — «un pair annonçait 268 Mo par état sur 74 898 états (~19 Po)» ; «(896 actifs, 3 708 octets chacun [...])» ; «refuse à l'état **72 393** [...] `268436952 octets au-delà du plafond de 256 Mo` — 258 Mo envoyés en 1,4 s».
- `:88-93` — «(200 lignes pour une trame de 200 états)» ; «83 octets d'un pair hostile suffisaient» ; «0,9 ko par jeton pour 1,45 réels».

**reports/rapport-modele-reel.md**
- `:3` — «**qwen2**, 24 couches, hidden 896, intermédiaire 4864, 14 têtes / 2 KV (GQA)».
- `:9-17` — «| blk.0.attn_norm.weight | 19.0 % | 77.9 % | 92.2 % | [...] | blk.0.attn_output.weight | 95.9 % | 99.7 % | 100.0 % |».
- `:24-27` — «| 4 | 27.4 % | 27.5 % | 27.5 % | **1.00×** | / | 8 | 15.3 % | 15.2 % | 15.1 % | **1.00×** |».
- `:31-38` — «| blk.0.ffn_gate.weight | 5 % | 5.0 % | 42.01 | 44.97 | 0.93× | [...] | blk.0.ffn_down.weight | 20 % | 20.0 % | 5.42 | 5.42 | 1.00× |».
- `:42-44` — «`attn_q` : (896, 896), 14 têtes de 64 dimensions» ; «1.4 % à 28.5 % (uniforme = 7.1 %)» ; «similarité entre têtes : 0.020».
- `:51-58` — «**27,5 % contre 27,5 % pour une partition aléatoire (1,00×)**» ; «laissait croire à un effet de 1,56×».
- `:64` — «**95,9 %** des poids sont sous 5 % du maximum ; 73,8 % dans `ffn_gate`».
- `:75-77` — «(74,12 % contre 74,12 % [...] ) [...] (0,39 contre 0,79 b/poids)».

**reports/rapport-mode-listes.md**
- `:7` — «**qwen2 Q8_0** (494.0 M poids, densité 99.2 %)».
- `:19-24` — «| **décalage-addition (popcount)** | **3.10** | 8,00 | / | **unaire** | **42.45** | **42.45** |» ; «L'unaire coûte **13.7× plus**».
- `:29-33` — «| 1 carte FPGA (9,66 Go/s) | 1.4 tok/s | 0.26 tok/s | / | CPU (28,7 Go/s) | 4.1 tok/s | 0.77 tok/s |».
- `:40-45` — «`E[|v|] = 42,79`» ; «**3,13 additions par poids** (mesuré : `E[popcount] = 3,13`)».
- `:48-49` — «on paie 3,13× en opérations [...] où 95 % des ALM dorment».

**reports/rapport-mur-memoire-4bits.md**
- `:3` — «Suite de `rapport-croisement-push-pull.md`.»
- `:11` — «| **tranches périmées en mode dense** | PPL **4 361 879** au lieu de 19,26 |».
- `:19-21` — «PPL 19,2647 au chiffre près sur 510 jetons, 24 jetons identiques, et 0 contre 180,7 G événements».
- `:33-43` — «`blk.0.ffn_gate.weight` — 4 864 × 896, 4,36 M poids» ; «| 100 % | 0,801 | 0,171 | **4,69** |».
- `:45-53` — «croisement à **24 %**» ; «croisement vers **33–45 %** (mesure bruyante : [...] de 0,342 à 0,192 ms)» ; «**Le croisement est à ~22 %, pas à 10 %** [...] `seuil_push` passe de 0,15 à **0,22**» ; «À 10 % [...] ×2,1 plus rapide ; à 1 %, ×8,3».
- `:66-67` — «bande passante mémoire mesurée : 19–22 Go/s (charge de fond : 4–8) / pull : 4,4 Mo lus à 14,1–26,9 Go/s, soit 62–136 % du repère».
- `:72-80` — «Il lit ses poids à 14 Go/s quand la mémoire en donne 20» ; «de 26 Go/s à 14 Go/s» ; «**gain nul** (21,98 ms contre 21,94)».
- `:87-92` — «`w = (nibble−8)·s_bloc` [...] (précision 1/65535, et non 1/255 — essayé : PPL 17,09 contre 17,10 [...] )» ; «**4,5 bits/poids effectifs** (4 + 16/32) [...] ×1,78 moins d'octets».
- `:96-103` — «~5 cycles par poids» ; «(16 poids par `vpmaddwd`)» ; «scalaire 132,331 contre AVX2 −2,495».
- `:111-126` — «| int8 partout | **17,4092** | — | 28,3 | 22,1 | / | 4 bits **attention** | 18,3503 | +5,4 % | 24,5 | 27,0 | / | 4 bits **FFN** | 21,6082 | +24,1 % | 37,0 | 14,1 | / | 4 bits corps entier | 21,9118 | +25,9 % | **39,2** | 13,1 |» ; «×1,22 **plus lent**» ; «×1,57 plus rapide» ; «**×1,39** (28,3 → 39,2 tok/s) pour **+26 % de perplexité**».
- `:141-149` — «| Qwen2.5-0.5B **Q8_0** | int8 | **19,2647** | [...] | **4 bits verbatim** | **21,0116** | **+9,1 %** | **13,1** | **38,9** | / | 4 bits + tête 4 bits | 21,7431 | +12,9 % | 12,0 | **42,5** |» ; «(255 jetons donnaient 19,86 / 19,67 / 19,88 [...])».
- `:153-164` — «**Le prix réel des 4 bits sur ce modèle est +9,1 % de perplexité**» ; «21,01 contre 21,20 [...] et 13,2 contre 18,2 s» ; «(`d = max/−8` [...])» ; «a donné PPL 3 550 569 avant correction».
- `:168-172` — «3,1 ms/jeton pour l'attention à contexte 256, pour seulement ~0,5 M de multiplications» ; «n'a rien changé (3,20 → 3,27 ms)».
- `:176-192` — «| scores `q·k` | **2,10 ms** | **0,65 ms** | / | **total** | **3,09** | **1,57** |» ; «(2,10 → 2,16 ms)» ; «En AVX2 + FMA, 32 éléments par tour : **×3,3**» ; «(21,0116 → 21,0131)».
- `:199-207` — «×1,34 de débit [...] » ; «coûte +26 % de perplexité» ; «`--q4-attn` et `--q4-tout` [...] **résultats négatifs**».

## C. Contradictions, chiffres périmés, affirmations douteuses

- `reports/rapport-gpu-topk-selection.md:347-349` — «Le top-k GPU n'est donc **pas encore branché dans le moteur** [...] jusqu'à l'étape 3.» — contredit `:164-171` (branche `DRAVE_GPU_TOPK=1`), `:343` («✅ **fait**») et `:195` (mesures « attention GPU top-k »). Conclusion périmée.
- `reports/rapport-gpu-topk-selection.md:7-8` — «coûte **0,89 ms** là où le tri CPU en coûte **497 ms** à 262 144 clés» — ni 0,89 ni 497 ms n'existent dans les tableaux : à 262 144 on lit «0,44 ms (224×) [...] 97,88 ms [...] 0,45 ms (896×) [...] 399,21 ms» (`:62`) ; 0,89 ms est la chaîne à 131 072 clés (`:256`).
- `reports/rapport-gpu-topk-selection.md:204` vs `:210` vs `:243` vs `:251` — «8 lancements et 17 transferts» / «**six lancements et cinq recopies**» / «8 lancements» / «chaîne (9 lancements)» : trois comptages incompatibles.
- `reports/rapport-gpu-topk-selection.md:295-296` — «l'écart de 6,6e-5 avec le CPU (15,1757)» — l'écart réel est ≈ 6e-4 (0,06 %), comme dit `:316` ; faux d'un ordre de grandeur.
- `reports/rapport-gpu-scores.md:27-34,36` — «**Correction du 30/09** [...] mesurés avec [...] **la même clé** — un banc dégénéré» ; «la ligne « 65 536 » ci-dessous datait d'AVANT le découpage en tranches (7,4 ms, 8,9×) ; re-mesurée après, elle vaut **2,36 ms et 26,7×**» — tableau d'origine explicitement périmé.
- `reports/rapport-gpu-topk-selection.md:81-84` — «n'est plus 1,03e-7 mais **1,60 à 2,25e-7** [...] corrigé dans le même commit».
- `reports/rapport-gpu-topk-selection.md:72-79` — «**Le banc mentait** [...] la même clé pour toutes les positions [...] le banc validait un cas dégénéré».
- `reports/rapport-gpu-topk-selection.md:100-103` — «un débordement en VRAM silencieux (`t.k < k` est entré dans la condition)».
- `reports/rapport-gpu-topk-selection.md:123-127` — «≈1 100× trop rapide [...] Un affichage mal étiqueté est un affichage qui ment».
- `reports/rapport-gpu-topk-selection.md:219-239` — «`attn_kv_recombine` [...] jusqu'à **4,65 logit** d'écart — un facteur 105 [...] seul ce noyau était faux» ; «la porte de 19,3885 ne pouvait pas voir ce défaut» — porte aveugle.
- `reports/rapport-gpu-topk-selection.md:313-318` vs `reports/rapport-logits-gpu-vs-cpu.md:6-7,58-63` — deux explications concurrentes du même écart CPU/GPU de 1,2 % : ordre de sommation des projections Q8_0/MXFP4 («C'est un doute à instruire, pas une explication») contre bascule du routage d'experts («hypothèse étayée, pas démontrée»). Non tranché ici.
- `reports/rapport-logits-gpu-vs-cpu.md:49-54` — «`compare_logits.py` n'imprimait qu'un ÉCHANTILLON [...] (511/511 annoncé, **497/511** mesuré) [...] un affichage partiel qui a l'air complet est un affichage qui ment.» — chiffre faux corrigé.
- `reports/rapport-empreinte-memoire.md:190-200` vs `:369-379` — «## 7. La réductibilité est uniforme [...] **Aucune différence.** Cibler « les extrêmes » n'apporte rien.» contre «la réductibilité n'est pas répartie uniformément [...] **75 à 82** [...] **42 à 49**». Conclusions opposées.
- `reports/rapport-empreinte-memoire.md:208-210` vs `:295-297` — «en dessous de 8 experts, un cache ne sert **à rien** (0 % de succès)» contre «un cache « experts du jeton précédent » — 8 entrées [...] sert 27 à 52 % des appels».
- `reports/rapport-empreinte-memoire.md:7` vs `:471` vs `:504` — empreinte V4.1 donnée comme «**50–80 Go**», «**45 à 78 Go**», «**~50 à 80 Go**».
- `reports/rapport-empreinte-memoire.md:437-439` — «bornée aux couches 6–39 [...] Les couches 0–5 et **30–47** n'en montrent aucune trace» — «30–47» recouvre la plage 30–39 porteuse du signal (cf. `:429-430`) ; probable typo pour 40–47.
- `reports/rapport-empreinte-memoire.md:282` et `:478` — deux « ## 9. » après un « ## 12 » (`:457`) : numérotation de sections incohérente.
- `reports/rapport-empreinte-memoire.md:523` et `:526` — deux entrées « 2. » dans « Ce qui reste à faire ».
- `reports/rapport-empreinte-memoire.md:492-495` — «a chronométré ce disque à **2 211 Go/s** [...] `O_DIRECT` échoue [...] donc le régime réellement froid n'est pas mesuré proprement.» — mesure invalide assumée.
- `reports/rapport-empreinte-memoire.md:534-536` — «un disque mécanique à 2 211 Go/s, une allocation de cache à 4,1 % partout, un total de 4 231 Go» — trois artefacts reconnus.
- `reports/rapport-empreinte-memoire.md:71-76` vs `:538-540` — perplexité restreinte en baisse (25,3748 → 24,3108) désignée comme faux gain : «Elle aurait suffi à annoncer un gain inexistant.»
- `reports/rapport-empreinte-memoire.md:48-50` — «`matvec_q4` calcule une liste creuse puis **reconstruit un vecteur dense** [...] La sparsité est calculée et jetée.» — chemin depuis remplacé par un aiguillage (`rapport-mla-experts.md:98-99`).
- `reports/rapport-lecteur-multifichiers.md:267-268` — «Le **mmap** : `read_to_end` charge tout le fichier [...] il restera hors de portée sans lui.» — contredit `:171-186` («Les fichiers sont maintenant **mappés**») et `:182`. Reste d'une version antérieure.
- `reports/rapport-lecteur-multifichiers.md:66` vs `:142` — «**32 verts**» contre «les **trente** tests verts».
- `reports/rapport-lecteur-multifichiers.md:158-165` — «La concordance porte sur **984 Go**» puis «**La file de 1 138 Go est terminée**» : la somme des six modèles listés vaut **1 151,97 Go** ; aucun sous-ensemble évident ne donne 984 ni 1 138.
- `reports/rapport-lecteur-multifichiers.md:9` vs `:232,267` — «sans recopier les poids» / «script ad hoc» / «`read_to_end` charge tout le fichier» cohabitent avec le §mmap.
- `reports/rapport-inference.md:97` vs `:185` — «**38 % plus rapide que numpy+BLAS**» contre «**30 % plus rapide que numpy + OpenBLAS**».
- `reports/rapport-inference.md:81` vs `:146-147` — «**10,5 tok/s** (int16) · 10,6 (int8)» contre «int8 [...] 10,3» / «int16 [...] 10,0» : classement inversé.
- `reports/rapport-inference.md:70` — «les 20,29 du harnais précédent» — `reports/rapport-harnais.md:7` donne «**PPL = 24.77**» ; 20,29 est introuvable dans ces 20 fichiers.
- `reports/rapport-inference.md:159-174` — «les identifiants produits diffèrent dans **5,2 % des cas** [...] la valeur absolue publiée précédemment (20,29) [...] **devra être reprise**» — `src/bpe_np.py` faux sur 5 points.
- `reports/rapport-mur-memoire-4bits.md:53-57` — «`seuil_push` passe de 0,15 à **0,22** [...] L'affirmation antérieure (« égalité à 10 % ») [...] **elle est retirée**.»
- `reports/rapport-mur-memoire-4bits.md:9-13` — «| **tranches périmées en mode dense** | PPL **4 361 879** au lieu de 19,26 |» — conclusions antérieures sur `--dense` faussées.
- `reports/rapport-mur-memoire-4bits.md:161-164` — «Stocker sa valeur absolue a donné PPL 3 550 569 avant correction.»
- `reports/rapport-mur-memoire-4bits.md:145` vs `:157` — «**13,1** | **38,9**» contre «et 13,2 contre 18,2 s» ; 18,0 s (colonne) vs 18,2 s (texte).
- `reports/rapport-mla-experts.md:13` vs `:66` vs `:92` — GLM-5.3 : «0/79» puis «71/79» puis «76/79», trois états présentés comme le même symptôme sans datation.
- `reports/rapport-mla-experts.md:59-64` — 53 + 22 + 4 + 1 = **80 couches** alors que GLM-5.3 a «79 couches MLA» (`:92`, `:108`). Incohérence arithmétique.
- `reports/rapport-mla-experts.md:110` vs `:236` — «**53 s par jeton**» contre «~190 s par jeton» : facteur ≈ 3,6 non expliqué.
- `reports/rapport-mla-experts.md:166-168` — «Aucune référence externe n'a été calculée pour Kimi [...] **ce chiffre n'est pas validé**».
- `reports/rapport-mla-experts.md:116-118` — «Le chemin a d'abord été faux (7,3 M de perplexité, corrélation −0,04)».
- `reports/rapport-mode4-lot-listes.md:1` vs `:30-32` — titre «÷2,3 sur les octets» contre corps «**÷2,2**», alors que 3 663/1 500 = 2,44 et que le « ÷2,3 » ne vaut pas contre le mode 2 (1,07×).
- `reports/rapport-mode4-lot-listes.md:81-86` — «le refus de `n == 0` était trop large — et c'est un correctif de la même journée qui l'avait introduit».
- `reports/rapport-mode4-lot-listes.md:103` — «`ChargeFlux::actifs()` est du code mort».
- `reports/rapport-mode4-lot-listes.md:33-35` vs `:44-48` — ratios issus de deux séries non comparables (synthétique / WikiText-2), non unifiés.
- `reports/rapport-encodage.md:42` — «| 2.00 | **4971.00 %** | 5.5 | dense ternaire (référence CDC) |» — accuracy de 4 971 %, manifestement fausse (49,71 % attendu).
- `reports/rapport-minimal.md:51-55` — tableau « Densité par plan » : en-tête « plan 0 | plan 1 » pour des lignes à 2, 3 et 4 valeurs ; malformé.
- `reports/rapport-minimal.md:83` — «⚠️ **Réserve** : [...] Ses chiffres de débit (§3, premières lignes) ne veulent rien dire».
- `reports/rapport-minimal.md:85` et `reports/rapport-eparsite.md:68-71` — ternaire quantifié *a posteriori* ; «on ne peut pas conclure sur la dégradation due à l'élagage».
- `reports/rapport-encodage.md:82-84` et `reports/rapport-grappes.md:56-58` — résultats issus d'un MLP jouet de 2 688 poids, « les valeurs absolues ne se transposent pas ».
- `reports/rapport-mode-listes.md:21` vs `:43-44` — «**3.10** additions/poids» contre «**3,13** additions par poids (`E[popcount] = 3,13`)».
- `reports/rapport-mode-listes.md:55-57` — «à valider en RTL».
- `reports/rapport-localite-activation.md:37` — «densité de 51 104 %» : mesure aberrante citée comme preuve.
- `reports/rapport-localite-activation.md:59` vs `reports/rapport-logits-gpu-vs-cpu.md:7,61` — «gpt-oss active **4 experts** sur 128» contre «top-8 sur 128» / «gpt-oss choisit **8 experts** sur 128». Contradiction directe.
- `reports/rapport-modele-reel.md:55-58` — «Mon premier test était **circulaire** [...] laissait croire à un effet de 1,56×».
- `reports/rapport-harnais.md:7` vs `reports/rapport-inference.md:67,70` — 24,77 (harnais) / 24,8995 (moteur) / «20,29 du harnais précédent» : trois valeurs pour la même famille de mesure.
- `reports/rapport-gpt-oss-perplexite.md:44-46` — deux lignes du tableau 511 jetons portent «*(série C)*» au lieu d'un chiffre : comparaison incomplète.
- `reports/rapport-gpt-oss-perplexite.md:10` vs `:80-85` — «perplexité **39,8** « au lieu de l'ordre de 6 »» déclaré faux : «**la prémisse [...] était fausse.**»
- `reports/rapport-gpt-oss-perplexite.md:13-14` vs `:91-110` — hypothèse « codage de position faux (YaRN) » retournée : YaRN est conforme aux références, c'est son activation qui dégrade (×9) ; le défaut du moteur devient un choix mesuré.
- `reports/rapport-execution-v41.md:8-9` vs `reports/rapport-empreinte-memoire.md:7-8` — «**Aucun chiffre de calcul sur V4.1 n'existe**» contre un «**Résultat principal**» chiffré pour V4.1, extrapolé de traces Qwen3-30B.
- `reports/rapport-execution-v41.md:18` vs `:79` — mesures «2,6 Mo touchés sur 101,4 Go [...] table 2 : **219 ms**» contre commentaire «203 Go de tables adressées, 5 Mo touchés».
- `reports/rapport-execution-v41.md:3` vs `reports/rapport-lecteur-multifichiers.md:158` — «365,71 Go» contre «365,70 = 365,7».
- `reports/rapport-mla-experts.md:167` vs `reports/rapport-lecteur-multifichiers.md:159` — Kimi «**1 026 G poids**» contre «303,90 = 303,9» Go ; réconciliable par la quantification, mais le lien n'est fait nulle part.

## D. Fichiers du dépôt cités

- `drave-core/gpu/drave_gpu.cu` — noyaux CUDA `attn_scores`, `attn_topk_histo`, `attn_topk_compte`, `attn_topk_ecrit`, `attn_topk_somme`, `attn_topk_tout`, `attn_kv_recombine` ; «passe de 10 à 13 noyaux [...] puis à **14** — 956 lignes» (`rapport-gpu-topk-selection.md:15-16`).
- `cuda_stub.h` — en-têtes/PTX maison : deux fonctions distinctes pour `atom.shared.add.u32` vs `atom.global.add.u32` via `cvta.to.shared.u64` (`rapport-gpu-topk-selection.md:109-111`).
- `drave-core/Cargo.toml`, `drave-core/target/release/drave` — manifeste et binaire release utilisés par les bancs (`rapport-gpu-topk-selection.md:354-355`).
- `src/gguf.rs` — lecteur GGUF, déquantification Q4_0/Q8_0/F16/F32, «ligne Q8_0», 332 lignes (`rapport-inference.md:30`).
- `src/list.rs` — «4 encodages de listes, dont `PushMat` (écart + valeur int8)», 321 lignes (`rapport-inference.md:31`).
- `src/engine.rs` — «pool à barrière atomique, décodeurs SWAR, modes push/pull», 510 lignes (`rapport-inference.md:32`).
- `src/tokenizer.rs` — «BPE byte-level Qwen2, pré-tokenizer réécrit à la main», 371 lignes (`rapport-inference.md:33`).
- `src/model.rs` — forward Qwen2 (RMSNorm, RoPE, GQA + cache KV, SwiGLU, tête), 403 lignes (`rapport-inference.md:34`) ; porte `attn_topk` (`model.rs:3150`, `rapport-gpu-topk-selection.md:167`) ; aiguillage remplaçant `matvec_q4` (`rapport-mla-experts.md:98`).
- `src/main.rs` — «mesures du moteur + inférence + perplexité», 382 lignes (`rapport-inference.md:35`).
- `src/bpe_np.py` — tokenizer Python du harnais de perplexité, faux sur 5 points vs Qwen2 (`rapport-inference.md:159-168`).
- `src/transformer_np.py` — référence numpy/OpenBLAS float32 (`rapport-inference.md:43`).
- `docs/plan-gpu-topk.md` — plan en 6 étapes du top-k GPU, critère 1e-6 (`rapport-gpu-scores.md:56`, `rapport-gpu-topk-selection.md:10`).
- `docs/contexte-long.md` — chiffrage du 1 M, croisement de l'attention complète (~4 000 clés), §4.ter («24,5 ms/jeton au lieu de 2,9») (`rapport-gpu-topk-selection.md:203-209`, `rapport-gpt-oss-perplexite.md:237`).
- `docs/programme-recherche.md` — programme de recherche, «étape A» rendue exécutable par le greffon (`rapport-greffon.md:5`).
- `REPRISE.md` — §6.a (prémisse gpt-oss), §6.e (échelles `DenseQ8`), §6 (noyaux GPU) (`rapport-gpt-oss-perplexite.md:3,252-253`, `rapport-logits-gpu-vs-cpu.md:21-22`).
- `reports/rapport-gpu-scores.md`, `reports/rapport-gpu-topk-selection.md`, `reports/rapport-croisement-push-pull.md`, `reports/rapport-routage-experts.md` — rapports chaînés cités en renvoi.
- `tools/analyse_experts_statique.py` — analyse statique des poids d'experts (orthogonalité, périodicité de 12) (`rapport-empreinte-memoire.md:398`).
- `tools/compare_logits.py` — compare deux fichiers de logits position par position ; imprime l'accord global et le p90 (`rapport-gpt-oss-perplexite.md:67-68`, `rapport-logits-gpu-vs-cpu.md:28,42,95`).
- `tools/convertir_clusters.py` — conversion GGUF → `commun.gguf` + 8 clusters + `mapping.tsv`, SHA-256 par tenseur (`rapport-lecteur-multifichiers.md:231-241`).
- `tools/inventaire_modeles_lourds.sh` — confronte les poids annoncés GGUF aux tailles HuggingFace (`rapport-lecteur-multifichiers.md:156`).
- `tools/make_patch.py` — fabrique un greffon consommé par `--patch` (`rapport-greffon.md:70`).
- `tools/mla_synthetique.py` — harnais MLA synthétique (disposition combinée `attn_kv_b`) (`rapport-mla-experts.md:40`).
- `tools/pair_factice.py` — pair factice du protocole réseau ; lit maintenant le mode 4 (`rapport-mode4-lot-listes.md:94-97`).
- `tools/portes_formats.sh` — compare les huit déquantificateurs de super-blocs à libggml «au bit près» (`rapport-mla-experts.md:72`).
- `tools/ref_logits.cpp` — évalue la même suite d'identifiants avec llama.cpp, écrit les logits bruts ; `--tensors REGEX` (`rapport-gpt-oss-perplexite.md:65-68`, `rapport-mla-experts.md:146,209`).
- `tools/*.py` — corpus « code » dont les commentaires français expliquent le r = 0,82 français/code (`rapport-empreinte-memoire.md:129`).
- `run_encoding.py`, `run_sparsity.py`, `run_clusters.py`, `run_harness.py`, `run_list_mode.py`, `run_quantify.py`, `run_real_clusters.py` — générateurs des rapports de la phase 1 (`rapport-encodage.md:87`, `rapport-eparsite.md:74`, `rapport-grappes.md:61`, `rapport-harnais.md:71`, `rapport-mode-listes.md:60`, `rapport-minimal.md:88`, `rapport-modele-reel.md:82`).
- `models/Qwen2.5-0.5B-Q8_0.gguf`, `models/Qwen2.5-0.5B-Q4_0.gguf` — modèles de test (`rapport-inference.md:316,329`).
- `data/wikitext2_test.txt` — corpus WikiText-2 (`rapport-gpt-oss-perplexite.md:5`).
- `journal/` — 28 sessions de l'usage réel (59 Mo, 2,5 M jetons) (`rapport-empreinte-memoire.md:325`).
- `commun.gguf`, `cluster-XX.gguf`, `cluster-00.gguf`, `cluster-20.gguf`, `cluster-100.gguf`, `mapping.tsv` — artefacts du format éclaté (`rapport-lecteur-multifichiers.md:19,110-113,231,240`).
- `qwen3-30b-8clusters-v2` — modèle en clusters servant de porte publiée (`rapport-mla-experts.md:86`).
- `llama.cpp/src/models/deepseek4.cpp` — code de référence (1 253 lignes) des quatre mécanismes manquants (`rapport-execution-v41.md:30`).
- `gpt_oss/torch/model.py` — implémentation officielle OpenAI (`_compute_concentration_and_inv_freq`) (`rapport-gpt-oss-perplexite.md:102-104`).
- `config.json` — configuration gpt-oss (`layer_types`, `attention_bias`, `initial_context_length`, YaRN) (`rapport-gpt-oss-perplexite.md:19,34,113`).
- `PowerInfer` (SJTU-IPADS/PowerInfer, miroir `Tiiny-AI/PowerInfer`) — dépôt étudié pour la localité d'activation (`rapport-localite-activation.md:3-4`).
- Hors dépôt, cités comme entrées de mesure : `/tmp/wt2_ids.txt`, `/tmp/wt2_txt.txt`, `/tmp/ids_qwen_long.txt` (17 434 jetons), `/tmp/ids_oss_512.txt`, `/tmp/audela_4096.log`, `/tmp/ref_glm_8p.log`, `/tmp/logits_cpu.bin`, `/tmp/logits_gpu.bin`, `/tmp/ids_qwen.txt`, `/tmp/p.bin`, `/home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf` (365,71 Go).

Aucun fichier du dépôt n'a été modifié (lecture seule + commandes de recherche).

### 👤 Utilisateur

Background subagent 56879594-1434-4e34-83cc-de42cdf192a1 finished and will do no further work unless you send it more.
Its closing message:
⏵ Inventory delivered; reporting completion.

L'inventaire complet (sections A à D, format demandé) vient d'être envoyé à l'agent parent `3d5618a0-4e3a-45bb-943d-a72c753fb7da` via `send_message`. Il est self-contained : aucune lecture de mon transcript n'est nécessaire.

Contenu transmis, en résumé de structure :
- **A. Termes et sigles** — ~110 entrées (sigles MLA/MoE/MXFP4/IQ*/Q4_K/GQA/RSS/PTX/AVX2/NUMA…, algorithmes Sinkhorn/RoPE/YaRN/SwiGLU/radix select/Jaccard/Gini/Heaps, matériel FPGA/ALM/M20K/DDR3/PCIe/Stratix/Xeon/Quadro, vocabulaire projet engram/grappe/push-pull/porte/mode 2-3-4/greffon/seuil_push/aiguillage, métriques perplexité/NLL/p50-p99/TTFT, formats GGUF/QPAT/mapping.tsv, variables `DRAVE_*`), chacune avec définition, outil/fichier d'usage et première occurrence `reports/fichier.md:ligne` — plus la liste explicite des termes demandés mais **absents** (AER, DRVF v5, TLB, HBM, LoRA, MTP, Hadamard, GFLOPS, MTok/s, aiguille…).
- **B. Chiffres et affirmations mesurées** — ~180 lignes de citations exactes horodatées par `fichier:ligne`, fichier par fichier.
- **C. Contradictions et chiffres périmés** — ~55 entrées, dont les plus exploitables : « top-k pas encore branché » vs « ✅ fait » (`rapport-gpu-topk-selection.md:347` vs `:343`), 0,89 ms/497 ms introuvables dans les tableaux du même rapport, 8/6/9 lancements contradictoires, réductibilité « uniforme » vs « non uniforme » (`rapport-empreinte-memoire.md:200` vs `:369`), cache 8 entrées « à rien » vs « 27–52 % », mmap « pas fait » vs « implémenté » (`rapport-lecteur-multifichiers.md:267` vs `:171`), 38 % vs 30 % vs numpy, 10,5/10,6 tok/s vs 10,3/10,0, tableau GLM 53+22+4+1 = 80 couches pour 79, 53 s vs 190 s/jeton, ÷2,3 vs ÷2,2 (mode 4), « 4971.00 % » d'accuracy (`rapport-encodage.md:42`), gpt-oss « 4 experts » vs « top-8 », sommes 984/1 138 Go invérifiables.
- **D. Fichiers du dépôt cités** — ~40 chemins (`drave-core/gpu/drave_gpu.cu`, `cuda_stub.h`, `src/*.rs`, `src/bpe_np.py`, `docs/plan-gpu-topk.md`, `docs/contexte-long.md`, `REPRISE.md`, `tools/*`, `run_*.py`, artefacts `commun.gguf`/`cluster-*.gguf`/`mapping.tsv`, `journal/`, `qwen3-30b-8clusters-v2`) avec leur rôle d'après le texte.

Aucun fichier du dépôt n'a été modifié : seules des lectures et des commandes de recherche (`grep`, `sed`, `wc`) ont été exécutées.

### 👤 Utilisateur

Agent fba448b3-e237-4eb3-b77d-fcbf7da1c93d sent a message:
INVENTAIRE — partie 3/3 (sections C et D).

## C. Contradictions, chiffres périmés, affirmations douteuses

- `reports/bilan-multi-materiel.md:96` — « il est **8 % plus rapide** que le dense (15,8 contre 14,7 tok/s) » — contredit `reports/rapport-croisement-push-pull.md:66-71` qui qualifie cette même phrase de « **C'est faux, et je l'ai mesuré deux fois** » : le bilan remplace une affirmation périmée par une autre affirmation périmée.
- `reports/bilan-multi-materiel.md:96` vs `:37` — « (15,8 contre 14,7 tok/s) » contre « CPU, noyau dense int8 (pull) | **27** | **36,4** » : contradiction interne, le pull dense est donné à 36,4 puis à 14,7 dans le même fichier.
- `reports/bilan-multi-materiel.md:103-104` — « le moteur d'événements **bat maintenant le noyau dense** » — faux après `rapport-croisement-push-pull.md:75-77` (36,43 contre 15,59 tok/s).
- `reports/bilan-multi-materiel.md:46` vs `:54` — « CPU (16 threads) | **5,3 G évts/s** mesuré » contre « 16 : 4,45 → **32 : 5,3** G évts/s » : le même débit attribué à 16 puis à 32 fils.
- `reports/bilan-multi-materiel.md:8` — « 1 carte Stratix V GS (Storey Peak, DDR3 9,66 Go/s, **PCIe Gen3 ×8 6,5 Go/s**, QSFP+ 4,8 Go/s) » — contredit `reports/rapport-architecture-memoire.md:385-386` : « Un Stratix V est branché, mais **en USB seulement** (pas de PCIe configuré), soit **625 Mo/s au mieux** ».
- `reports/bilan-multi-materiel.md:21` — « **2 547 lignes de Rust** » — périmé : 11 440 lignes (`rapport-coherence-docs.md:108-110`) puis 11 901 (`rapport-coherence-docs-2.md:129`).
- `reports/bilan-multi-materiel.md:13` — « Un token = **352,8 M d'événements** » vs `reports/rapport-campagne-parcimonie.md:35` « référence | **354,3 M** » et `reports/rapport-attention-creuse.md:112` « 354 M paires/token » : écart de 1,5 M non expliqué.
- `reports/bilan-multi-materiel.md:94` — « Perplexité 20,29 (harnais Python) | **Invalidée** … la mesure est à reprendre » — jamais reprise dans le bilan, alors que 19,2647 et 19,3885 circulent ailleurs.
- `reports/rapport-8bits.md:56` — « c'est là que les gains mesurés (**×2,17**) se trouvent » — contredit frontalement `reports/bilan-multi-materiel.md:92` : « « Encodage hybride ×2,17 » | **Retirée** — le code proposé viole l'inégalité de Kraft ».
- `reports/rapport-analyse-flux.md:14` et `:56` — « Le croisement push/pull du projet est mesuré à **~10 % de densité** » — contredit `reports/rapport-croisement-push-pull.md:43` : « Les deux architectures se croisent à **~22 % de densité d'activation**, pas à 10 % » (écart déjà relevé par `rapport-coherence-docs.md:106-107`).
- `reports/rapport-analyse-flux.md:30-33` — « c'est **cohérent** avec la mesure d'activation du projet (**0,08 %** « chauds » …) » alors que la mesure citée est « **0,89 % à 1,90 %** » : facteur 10 à 20 présenté comme cohérent.
- `reports/rapport-cpu-aer.md:17-18` — « dispersion (`np.bincount`) : **183999808.87 G événements/s** » / « **364797216.41 G** » — valeurs ~1,8e17 évts/s, incompatibles avec 18,1 G év/s (`rapport-croisement-push-pull.md:96-98`) ; le rapport lui-même met en garde `:62-65`.
- `reports/rapport-cpu-aer.md:48` — « 183999808.9 G événements/s mesurés contre 0.35 G nécessaires par token » — comparaison d'un débit par seconde à une quantité par token.
- `reports/rapport-cpu-aer.md:32` — « densité 5 %, **0,476 b/poids** » — incohérent avec « un événement = écart + valeur, **2 octets** » (`rapport-croisement-push-pull.md:7`), qui donne ≥0,8 b/poids à 5 %.
- `reports/rapport-attention-creuse.md:27` — « **32** | **23,3302 (−1,20 %)** » — contredit `:95` et `:126` (« 23,6125 dense, **23,3279** à k=32 ») et `rapport-campagne-parcimonie.md:36` (« 23,3279 (**−1,21 %**) ») : deux valeurs pour la même mesure.
- `reports/rapport-attention-creuse.md:156` — « attention 32 seule = **−0,52 %** (B) » vs `rapport-campagne-parcimonie.md:36` — « 26,1178 (**−0,53 %**) » : arrondis divergents.
- `reports/rapport-attention-creuse.md:154-157` — « interaction avec le k-WTA du FFN → **mesuré, non additive et défavorable** (+0,19 %) » vs `rapport-campagne-parcimonie.md:37` — « **+ `gate` à 85 %** | 23,2811 (**−1,40 %**) » : « FFN complet » et « gate » ne jouent pas dans le même sens, l'ambiguïté n'est levée nulle part.
- `reports/rapport-attribution-kv.md:3-5` — « les **valeurs** en int8 ne coûtent rien (1 % de l'écart) » vs tableau `:15-16` — « **99,2 % expliqué** » / « 1,0 % seulement » : les deux parts somment à 100,2 % et la colonne mélange attribution par les clés et par les valeurs.
- `reports/rapport-attribution-kv.md:33-35` — « **64 %** … **28 %** » — les autres documents (« 75 % / 50 % », cf. `rapport-coherence-docs-2.md:97`) donnent deux valeurs pour le même réglage ; le rapport d'attribution est du bon côté, les docs cités non.
- `reports/rapport-architecture-memoire.md:418-419` — « Le KV à 1 M de contexte : **non chiffré ici** … 512 × 2 × 2 octets × 40 = **82 Ko** par jeton, soit **82 Go** à 1 M … il n'est pas dans le tableau » — contredit `:96-98` du même rapport : « F16 | **90,0 Ko** … **96,6 Go** » ; la formule ignore en outre « plus 64 de RoPE » décrit `:92`.
- `reports/rapport-architecture-memoire.md:246` — « **Pas de FPGA dans cette machine.** » — contredit `:385` : « Un Stratix V est **branché**, mais en USB seulement ».
- `reports/rapport-architecture-memoire.md:181` vs `:184` — « **31,08** » Go/s cumulés à 16 lecteurs contre « **33,19** à seize » : deux valeurs pour 16 lecteurs, non expliquées.
- `reports/rapport-architecture-memoire.md:142` vs `:175` vs `:239` — banc mémoire à « **20,8** » Go/s (16 fils), puis « **13,5 contre 12,6** », puis « **13,8 | 14,2 | 15,0** » : trois régimes dans le même rapport sans que les protocoles diffèrent explicitement.
- `reports/rapport-architecture-memoire.md:291` et `:408` — deux sections « **## 11.** » : numérotation dupliquée (la seconde devrait être 15).
- `reports/rapport-architecture-memoire.md:4` — « 2 × Quadro RTX 5000 (**32 Go** de VRAM) » vs `:44` — « VRAM | **30,2 Go** » : 1,8 Go manquants sans explication.
- `reports/rapport-capteur-hebbien.md:48` — « Rang effectif | **795** (trace) contre **894** (poids) » vs `:67` et `:84` — « le rang de `W` pour `ffn_gate` est de **896 sur 896** » : « rang effectif » et « rang » cohabitent sans définition distincte.
- `reports/rapport-capteur-hebbien.md:34` — « sa copie coûte **7 Ko par matrice** » : 896 × 2 octets = 1,75 Ko, facteur 4 inexpliqué.
- `reports/rapport-aiguille-topk.md:264-265` — « 58 à 62 ms par jeton de prompt, soit ≈20 min par sonde à 16 384 » vs `:228` — « une sonde tombe de ~250 s à 75 s » (≈18 ms/jeton à 4 096) : deux régimes (`--gpu-kv` ou non) non explicités.
- `reports/rapport-aiguille-topk.md:133` — « **511/511** » d'accord top-1 vs `:126-127` — « Les deux chemins ne donnent pas la même continuation à température 0 » : tension non résolue par la seule « amplification chaotique » invoquée `:136-139`.
- `reports/rapport-aiguille-topk.md:266-270` — « la généralité inter-fenêtres **n'est pas mesurée** » / « **une seule fenêtre par (contexte, profondeur)** » — périmé : contredit par les sprints 5 (« trois fenêtres distinctes », `:148-150`) et 6 (« Neuf fenêtres contiguës », `:226-228`) du même document.
- `reports/rapport-aiguille-topk.md:32-39`, `:73-83`, `:98-107`, `:213-217` — quatre couches d'auto-corrections : « Correction d'une affirmation fausse de la première version », « corrigé après la revue adverse du sprint 4 (et re-corrigé au sprint 5) », « Conclusion corrigée », « Ce que cela corrige dans ce rapport même » — les verdicts « NON au milieu » et « 0/3 à k = 512 » sont explicitement périmés.
- `reports/rapport-aiguille-topk.md:11-12` — « le moteur **ignore `--attn-topk` au préremplissage** » vs `reports/rapport-aiguille.md:102` — « `--attn-topk 256` (qui AMÉLIORE la perplexité à 2 048) » : l'amélioration ne porte que sur les 24 jetons de décodage, ce que `rapport-aiguille.md` ne dit pas.
- `reports/rapport-compacite-trace.md:136` — « **blocs, échelles f16** | **45 836 190** » vs `:14` — « **45 079 930 octets** » : projection du §5 contre mesure v3, écart non signalé dans le tableau (relevé par `rapport-coherence-docs-2.md:83`).
- `reports/rapport-compacite-trace.md:231-243` et `:255-257` — « Ce qu'il reste à valider : le rejeu … l'aller-retour Rust ↔ Python … la rétrocompatibilité » ; « les perplexités du rejeu … devront être refaites » — périmé : le bandeau `:13-18` annonce le rejeu v3 (19,4029) et la rétrocompatibilité faite.
- `reports/rapport-compacite-trace.md:27` — « le reste (valeurs i8, échelles f16, zstd) porte le total à **−79 %** » vs bandeau `:20` — « **Reste** : l'emballage zstd en étape EXTERNE » : « reste » et « porte le total » dans le même document.
- `reports/rapport-compacite-trace.md:24` — « la trace DRVF v1 coûte **6,04** octets par neurone actif » vs `:133` — « actuel (u32 + i16) | 132 396 736 | **6,02** » : valeurs creux/dense non distinguées dans la phrase d'attaque.
- `reports/rapport-compacite-trace.md:137-138` — « zstd niv. 3 : **41 675 229** » / « zstd niv. 19 : **50 009 567** » : contre-intuitif (niveau plus fort = fichier plus gros), signalé et vérifié par le texte `:152-158`.
- `reports/rapport-croisement-push-pull.md:15-20` — « **Corrigé le 27/09** : le tableau de croisement … mesurait « push » contre « dense » alors que le drapeau `--dense` … **n'était jamais lu** » : les chiffres antérieurs sont périmés par l'aveu du texte.
- `reports/rapport-croisement-push-pull.md:108` — « identique **au bit près** » vs `:11-13` — « perplexité 19,2647 **au chiffre près** … tokens identiques » : deux formulations pour la même garantie.
- `reports/rapport-decoupage-moe.md:4-5`, `:42`, `:59` — « ~1,8 » / « ×1,9 » / « divisée par **1,7** » : trois valeurs du même gain (5,32/3,08 = 1,73).
- `reports/rapport-decoupage-moe.md:86` et `:96-97` — « gpt-oss … **est en cours de mesure** », « La trace de 2 048 jetons **en cours** » — périmé (`rapport-coherence-vision.md:68` donne le top-4 de gpt-oss comme acquis).
- `reports/rapport-decoupage-moe.md:63-65` — « un découpage **équilibré par taille** … n'est pas optimal en charge ; il faudrait équilibrer par *usage*, ce qui est un autre problème (et une autre mesure) » : le gain annoncé est un gain de ventilation, pas de latence.
- `reports/rapport-drapeaux-ignores.md:7` vs corps `:82` et `:228` — l'addendum dit « version 4 (puis 5) » mais le corps affirme encore « l'en-tête de flux ne transporte que ces quatre champs … Les deux nœuds divergent donc **en silence** » et recommande « **incrémenter `VERSION_FLUX`** » : l'état décrit n'est plus l'état courant.
- `reports/rapport-drapeaux-ignores.md:196-198` vs `:14-20` — recommande « `--options-actives` (et `--options-strict`) » alors que l'addendum 2 précise « La variante `--options-strict` **n'existe pas** » : recommandation à moitié périmée, corps non corrigé.
- `reports/rapport-drapeaux-ignores.md:151-163` — « Le binaire date de **11:41** » alors que l'audit porte sur la révision de **11:54** : portée des preuves limitée par l'aveu du texte.
- `reports/rapport-drapeaux-ignores.md:124` — « `QT_*` (anciens noms) … **Faux positif** » : toute variable `QT_` (ex. `QT_IM_SWITCHER`) déclenche l'avertissement, bruit reconnu.
- `reports/rapport-coherence-docs.md:47-48` — « `const VERSION_FLUX: u8 = 3;` (main.rs:1295) » contre commentaire « Version 4 » (CONTRADICTOIRE) — puis `reports/rapport-coherence-docs-2.md:50` — « `VERSION_FLUX = 4` (1376) » : le premier audit (12:30) est daté, le second (15:11) le corrige ; ne pas lire l'un comme l'état de l'autre.
- `reports/rapport-coherence-docs.md:108-110` vs `reports/rapport-coherence-docs-2.md:129` — « **11 440** lignes » contre « **11 901** » : le chiffre du premier audit est périmé ~3 h plus tard.
- `reports/rapport-coherence-docs.md:205-211` — « les chiffres **recalculables** (3 663, 917 583, 1 419, 1 023) sont des **conséquences arithmétiques** du code, pas des mesures neuves » : ces valeurs ne doivent pas être citées comme mesures.
- `reports/rapport-coherence-docs-2.md:36-39` — « les variantes KV … **n'ont pas été exercées** » ; « Les chiffres de débit et de perplexité cités sont recoupés **entre documents**, pas re-mesurés » : même réserve.
- `reports/rapport-coherence-docs-2.md:59` — « mesuré : **−32,1 %** contre la v2 » vs commentaire de code cité « la v3 est « ~22 % plus petit » » : commentaire périmé.
- `reports/rapport-coherence-docs-2.md:30` — « pendant qu'une campagne de mesure tournait (`--ppl … --lot 512`) : aucune conclusion de performance n'en est tirée » : toutes les mesures de temps du 30/09 sont sous charge (voir aussi `rapport-campagne-parcimonie.md:10`, « charge de 8 à 22 »).
- `reports/rapport-coherence-docs.md:100` (cité PÉRIMÉ) — « restent à faire : valeurs i8 (−60,9 %), échelles f16 (−63,5 %), zstd (−79 %) » : i8 + échelles f16 sont faits et commités (`ae85043`).
- `reports/rapport-coherence-docs.md:112` (cité PÉRIMÉ) — « KV int4 « mesuré : **+384 %** — llama.cpp : +411 % » » : la mesure de référence à 8 192 est **+364 %** contre +494 %.
- `reports/rapport-coherence-docs.md:113` (cité MANQUANT) — « Qwen 6 bits : « **19,3045** ← bat l'int8 » » : « aucune source dans `reports/` ».
- `reports/rapport-coherence-docs.md:116` (cité MANQUANT) — « gpt-oss-120b : perplexité « **—** » » : trois valeurs coexistent (15,1757 ; 20,8361 à 63 jetons ; 15,6017 le 02/10) sans contexte commun.
- `reports/rapport-coherence-docs-2.md:100` (cité PÉRIMÉ) — « KV int8 « fait (échelle par vecteur) », « mesuré : **+7,1 %** » » contre « **+1,5 %** à 512, **+3,0 %** à 8 192 » dans le même document.
- `reports/rapport-coherence-docs-2.md:123` — « 0,25 Mbit/s » : débit d'un flux cité une seule fois, non recoupé dans ces 20 fichiers.
- `reports/rapport-coherence-docs-2.md:135` — « ×73 pour le KV en VRAM, 968 ms CPU, 1,99e-7, 12,4 → 12,5 ms » : chiffres sans source dans ces 20 fichiers.
- `reports/rapport-coherence-vision.md:53` vs `reports/rapport-coherence-docs-2.md:50` vs `reports/rapport-drapeaux-ignores.md:7` — « protocole v5, 5 modes » / « `VERSION_FLUX = 4` … modes 0-3 » / « version 4 (puis 5) » : trois états successifs, toute citation croisée doit être datée.
- `reports/rapport-coherence-vision.md:159-163` — « clusters **799,8557** » : perplexité aberrante présentée comme porte verte, sans explication.
- `reports/rapport-coherence-vision.md:129-132` — « llama.cpp applique YaRN dès la première position (**166,85**) là où nous le différons (15,6017) … en le forçant nous obtenons **84,07** » : la porte gpt-oss n'est « **pas validée à l'extérieur** ».
- `reports/rapport-coherence-vision.md:141-144` — « V4.1-Flash-Q2 est-il complet ? … **Rien ne permet d'y répondre depuis cette machine** » : question ouverte pouvant « invalider une partie du chantier ».
- `reports/rapport-coherence-vision.md:40` — « une politique YaRN périmée dans `REPRISE.md` (bascule à **4 ×**, pas 1×) » : correctif du 02/10, les textes antérieurs restent faux.
- `reports/rapport-coherence-vision.md:70` — « densité mesurée **17,9 %** sous le croisement de 22 % » : à confronter aux densités par couche de `rapport-analyse-flux.md:19-22` (20,1 % à 56,3 %) — un seul chiffre global masque la dispersion.
- `reports/rapport-8bits.md:51-52` — « les plans denses coûtent exactement 8 bits/poids … » vs tableau `:26` — « plans denses … | 8,00 | **3.10** » contre « positionnel (8 bits) | 8,00 | **0.99** » : même taille, 3× plus d'opérations ; « ne servent à rien » est vrai en taille seulement.
- `reports/rapport-aiguille.md:12-13` — « 9,6 minutes pour un échec sur Qwen3-30B-A3B » vs `:85-86` — « Une sonde de 2 048 jetons sur le 30B prend **8 à 25 minutes** » : protocoles v1 (8 jetons) et v2 (40 jetons) non comparables.
- `reports/rapport-coherence-docs.md:131` — « ce fichier **n'existe pas** (`reports/rapport-prefill-reparti.md`) » vs `reports/rapport-coherence-docs-2.md:71` qui cite « `reports/rapport-prefill-reparti.md:85` » comme existant : le fichier a été écrit entre les deux audits.
- `reports/rapport-coherence-docs.md:142` — « ces fichiers **n'existent pas dans le dépôt** (`reports/rapport-pe-evenementiel.md`, `reports/rapport-lecteur-ddr3.md`) » : renvois FPGA cassés.
- `reports/rapport-coherence-docs.md:151` — « `tools/pack_lists.py`, `tools/quartus_env.sh` | présents dans `../FPGA-Stratix-V/tools/` » : ce ne sont **pas** des chemins du dépôt Qtrinet (piège d'inventaire).
- `reports/rapport-coherence-docs-2.md:117` et `reports/rapport-coherence-docs.md:143` — la ligne « `gpu/drave_gpu.cu + .ptx` » reste PÉRIMÉ dans les deux audits : « les noyaux sont dans **`drave-core/gpu/`** … la ligne est placée sous un bloc titré `drave-core/src/`, donc elle se lit `drave-core/src/gpu/…` » — correction incomplète.
- `reports/rapport-drapeaux-ignores.md:53` — « Si plusieurs sont donnés, **le premier de l'ordre d'aiguillage gagne en silence** » : comportement silencieux classé 🟡 mais non corrigé à la date du rapport.

## D. Fichiers du dépôt cités

**Documentation (`docs/`)**
- `docs/vision.md` — vision Drave, axes 1-3, valeurs de porte, deux cas d'encodage (liste trinaire / connexions pondérées), renvois FPGA.
- `docs/roadmap.md` — feuille de route, statuts 3.1-3.5, chiffres de transport et de trace, critère 3.2.
- `docs/programme-recherche.md` — programme de recherche, 4ᵉ propriété « le flux se route », règle de méthode.
- `docs/sprints.md` — sprints et portes (`tools/portes.sh`).
- `docs/histoire.md` — chronologie, renommage Qtrinet→Drave.
- `docs/format-flux.md` — format DRVF (versions 1/2/3, modes 0-4, en-tête 26/39/79 octets, invariants, tailles, mise en garde sur les époques).
- `docs/format-clusters.md` — format des clusters/grappes, placement et contiguïté, renvoi de ligne.
- `docs/colab-reparti.md` — recette Colab, préremplissage par lots, réglages transportés (4 cités sur 14).
- `docs/convertisseur.md` — convertisseur, croisement à 22 %, mmap/NUMA, Q8_0, routeur MoE, lecteur Q4_K/Q6_K, conteneur ex-`QTNT`.
- `docs/contexte-long.md` — campagne contexte long E1-E7, KV int8/int4, seuil YaRN, aiguille v2 12/12.
- `docs/plan-modeles-lourds.md` — plan modèles lourds, bandeau de statut, architectures `deepseek2`/`glm-dsa`.
- `docs/plan-gpu-topk.md` — plan GPU top-k, chiffres KV en VRAM.
- `docs/plan-mla-vision.md` — plan MLA/vision, état « fait », réserve du chemin dense.
- `docs/plan-prefill-reparti.md` — plan préremplissage réparti, règles R1/R4, en-tête de 39 octets, renvoi `:346` vers un rapport inexistant.
- `docs/plan-mode4-lot-listes.md` — conception du mode 4 « lot en listes », protocole v5.
- `docs/plan-deepseek-v4-flash.md` — plan V4-Flash, lecteur multi-shards, 128 experts top-4, étape 6 grappes.
- `docs/plan-deepseek41-complet.md` — plan V4.1, types réels du GGUF (I8), porte P0, validation MLA à la position 0.
- `docs/comparaison-spiking.md` — comparaison réseaux à spikes, 8,3 nJ projeté, densité 17,9 %.

**Racine**
- `README.md` — état du projet, tableau des modèles (gpt-oss), croisement 10 %, comptes de lignes, renvois FPGA.
- `REPRISE.md` — journal de reprise (§2, §5.1, §5.2, §6, §6bis), table des variables `DRAVE_*`, carte du dépôt.
- `Qtrinet-bootstrap.md` — document de référence survolé par grep seulement.
- `journal/` et `journal/README.md` — non lus par consigne ; le README est régénéré par un hook.

**Moteur (`drave-core/`)**
- `drave-core/src/main.rs` — CLI et `analyser()`, aiguillage des modes, protocole de flux (`VERSION_FLUX`, `TAILLE_TETE`, modes 0-3, `verifier_taille`, encodeur/décodeur de blocs, tests).
- `drave-core/src/model.rs` — chargement GGUF, forward, `KvCache::assurer`, `TraceFlux` v1/v2/v3, top-k d'attention, MLA, YaRN, quantification KV.
- `drave-core/src/list.rs` — listes creuses, `DenseQ8`, `BITS_POIDS`, `dot_q8_source`.
- `drave-core/src/engine.rs` — pool de threads, `EPINGLER`, `coeurs_physiques()` (lit `/sys/devices/system/cpu/cpu*/topology/`).
- `drave-core/src/gpu.rs` — noyaux GPU, `gpu::instance()`, `--gpu-banc`.
- `drave-core/gpu/drave_gpu.cu` et `drave-core/gpu/drave_gpu.ptx` — noyaux CUDA et PTX chargé par `include_str!("../gpu/drave_gpu.ptx")`.
- `drave-core/bench/cpu_aer.c` — banc CPU AER (16 threads) cité par `rapport-cpu-aer.md:20`.
- `drave-core/target/release/drave` — binaire des preuves empiriques ; `drave-core/` pour `cargo build --release`.

**Outils (`tools/`)**
- `tools/aiguille.py` — test de l'aiguille v1/v2, `--attn-topk`, `--gpu-topk`, `--journal`, garde-fou d'offset.
- `tools/analyse_flux.py` — analyse du flux couche par couche.
- `tools/profil_flux.py` — profilage du flux (cité `docs/roadmap.md:18`).
- `tools/diff_flux.py` — comparaison de flux.
- `tools/flux_codec.py` — codec Python de référence, lit les versions 1/2/3.
- `tools/trace_compacite.py` — mesure de compacité des traces.
- `tools/clusters_moe.py` — découpage MoE en clusters équilibrés.
- `tools/convertir_clusters.py` — produit `commun.gguf` + un `cluster-XX.gguf` par cluster.
- `tools/portes.sh` — portes du dépôt (section 7 : gpt-oss).
- `tools/portes_formats.sh` — batterie de formats comparée à libggml.
- `tools/preparer_colab.sh` — préparation du kit Colab.
- `tools/colab_cote_local.sh` — script local (créé à 15:09, cité par aucun document).
- `run_8bit_perfection.py` — génère `rapport-8bits.md`.
- `run_cpu.py` — génère `rapport-cpu-aer.md`.
- `bpe_np.py` — harnais Python de perplexité dont le tokenizer s'écarte du vrai pré-tokenizer Qwen2.
- `tools/pack_lists.py` et `tools/quartus_env.sh` — cités par `bilan-multi-materiel.md:149,152` mais situés dans `../FPGA-Stratix-V/tools/`.

**Données, kits, modèles**
- `data/wikitext2_test.txt` — corpus de remplissage de l'aiguille (~90 k jetons ; 353 778 caractères).
- `colab/README.md` et `colab/Drave-reparti.ipynb` — kit Colab.
- `models/Qwen2.5-0.5B-Q8_0.gguf` (et `../models/...` dans les blocs reproductibles).
- `/home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf`.
- `/home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf`.
- `MANIFEST.json` et `*.moe.json` — formats proposés pour les clusters (pas encore des fichiers).

**Hors dépôt (`../FPGA-Stratix-V/`), cités par les rapports**
- `rtl/event_pe.sv`, `rtl/event_engine.sv`, `rtl/event_reader.sv` — PE, moteur et lecteur d'événements.
- `tb/ddr3_model.sv`, `tb/tb_event_reader.sv` — modèle DDR3 et banc du lecteur.
- `sim/` — sortie de `pack_lists.py` ; `syn/reader/event_reader` — projet Quartus.
- `docs/rapport-pe-evenementiel.md`, `docs/rapport-lecteur-ddr3.md` — rapports FPGA référencés par erreur sous `reports/` dans le dépôt.

**Références de code et artefacts divers cités** : commits `ae85043`, `a0687b9`, `2184fc5`, `6b3b53f`, `d59d061`, `cda3162`, `976cb81`, `cb37c83`, `af18f29`, `7b88131`, `1a4beb3`, `7522289`, `b97d129`, `90a74a6`, `a383cd7` ; empreintes `d5e90136…`, `3e5dde2d…`, `bc53a66a…`, `61582adb…`, `1726f9ac…`, `1d7eacc5…` ; traces et journaux hors dépôt `/tmp/flux_v2.bin`, `/tmp/flux_v3.bin`, `/tmp/verif_v2.bin`, `/tmp/verif_v3.bin`, `/tmp/flux_sparse.bin`, `/tmp/flux_f32.bin`, `/tmp/aiguille_topk2.log`, `/tmp/aiguille_k.log`, `/tmp/aiguille_rep.log`, `/tmp/aiguille_s5.log`, `/tmp/aiguille_s6.log`, `/tmp/aig8192.log`, `/tmp/routage.txt`, `/tmp/hebb12.bin`, `/tmp/clusters.json`, `/tmp/act_log.bin`, `/tmp/loss_log.bin`.

### 👤 Utilisateur

Agent 8549abcb-5d9a-4594-915b-5628c80a2a08 sent a message:
INVENTAIRE DRAVE — 20 rapports de reports/ — PARTIE 1/2 (sections A et B). Aucun fichier modifié.

## A. Termes et sigles
- **AER** (non développé dans le texte ; « réseau de combinaison façon routeur AER ») — réseau d'interconnexion par compartiments de destination pour le dédoublonnage multi-cartes ; fusion par compartiments (`drave-core`) ; `reports/rapport-optimisations.md:166`
- **ALM** (Adaptive Logic Module) — brique logique du FPGA dont on chiffre le coût d'un PE ; `reports/rapport-precision.md:70`
- **AVX2** — SIMD x86 des noyaux de quantification (ni gather ni scatter entier) ; `reports/rapport-optimisations.md:163`
- **CDC** (cahier des charges, non développé) — contrainte « aucun DSP » ; `reports/rapport-optimisations.md:144`
- **CPU** — processeur hôte opposé au FPGA/GPU ; `reports/rapport-optimisations-auto.md:88`
- **CSA** (compresseur DeepSeek-V4, ratio 4) — attention à blocs compressés avec chevauchement, 21 couches de V4-Flash ; `reports/rapport-v4-couches-0-1.md:11`
- **CUDA** — pilote GPU ouvert seulement si nécessaire ; `reports/rapport-optimisations-auto.md:16`
- **DDR3** — mémoire du banc FPGA, 9,66 Go/s, sature à 312 voies ; `reports/rapport-precision.md:63`
- **DDR4-2133** — mémoire des deux sockets Xeon, ~136 Go/s théoriques ; `reports/rapport-passage-a-l-echelle.md:152`
- **DSP** — multiplieur matériel interdit par le CDC ; `reports/rapport-optimisations.md:145`
- **E2M1** — format 4 bits des valeurs MXFP4 ({0,½,1,1½,2,3,4,6}) ; `reports/rapport-passage-a-l-echelle.md:78`
- **E8M0** — échelle de bloc MXFP4 sur 1 octet (puissance de deux) ; `reports/rapport-passage-a-l-echelle.md:77`
- **FPGA** — cible matérielle (124 MHz × 32 PEs, ALM comptés, aucun DSP) ; `reports/rapport-optimisations.md:72`
- **GEMM** — produit matrice-matrice par lots vs matvec jeton par jeton ; `reports/rapport-prefill-par-lots.md:1`
- **GGUF** — format de fichier des modèles (`Gguf::open`, `read_to_end`, métadonnées) ; `reports/rapport-passage-a-l-echelle.md:204`
- **GPU** — accélération KV/tête (`DRAVE_GPU`, `DRAVE_GPU_KV`, `DRAVE_GPU_TETE`, miroir VRAM) ; `reports/rapport-optimisations-auto.md:16`
- **GQA** — têtes KV partagées, cache KV dépassant les poids à 128 k ; `reports/rapport-passage-a-l-echelle.md:143`
- **HCA** (ratio 128) — résumé de bloc « par dimension » avec porte softmax, 20 couches de V4-Flash ; `reports/rapport-v4-couches-0-1.md:12`
- **JIT** — piste « charger les logits manquants ou faire du JIT », rejetée ; `reports/rapport-tete-restreinte.md:5`
- **KV** (cache clé-valeur) — état d'attention quantifié (f32/f16/int8/int4), déportable VRAM ; `reports/rapport-optimisations-auto.md:51`
- **LUT** — MAC int4×int8 par 4 additions conditionnelles décalées ; `reports/rapport-precision.md:69`
- **MAC** — multiply-accumulate, coûté en ALM ; `reports/rapport-precision.md:69`
- **MLA** (Multi-head Latent Attention) — cache latent à rang faible ; `reports/rapport-optimisations-auto.md:56`
- **MoE** — experts routés, seule parcimonie structurelle ; `reports/rapport-p0-flux.md:49`
- **MXFP4** — 4 bits par blocs de 32 (E8M0 + E2M1), format gpt-oss-120b, import exact ; `reports/rapport-passage-a-l-echelle.md:17`
- **NLL** — perte moyenne par jeton vs llama.cpp ; `reports/rapport-routage-experts.md:114`
- **NUMA** — topologie mémoire 2 nœuds (`numactl`, premier-touch) ; `reports/rapport-optimisations-auto.md:14`
- **NVLink** — 25,8 Go/s (« 2× le PCIe ») ; `reports/rapport-optimisations-auto.md:17`
- **NVMe** — FastNVMe, 5,37 Go/s à 1 lecteur, 31 Go/s à 16 ; `reports/rapport-optimisations-auto.md:19`
- **PCIe** — 6,5 Go/s en x8 ; `reports/rapport-optimisations-auto.md:17`
- **PE** — processing element (312 voies, PE ternaire ~20 ALM) ; `reports/rapport-precision.md:62`
- **PPL** — perplexité (`--ppl`) ; `reports/rapport-parcimonie-imposee.md:47`
- **QPI** — lien inter-socket ; `reports/rapport-passage-a-l-echelle.md:156`
- **QSFP+** — lien 4,8 Go/s ; `reports/rapport-passage-a-l-echelle.md:179`
- **RMSNorm** (`rmsnorm`) — norme d'entrée, envoyée à tort par `--flux-norme` ; `reports/rapport-transport-liste.md:67`
- **RoPE** — rotation positionnelle, deux conventions (`LLAMA_ROPE_TYPE_NORM` vs `NEOX`) ; `reports/rapport-v4-couches-0-1.md:7`
- **SiLU** (`silu`) — activation du SwiGLU ; `reports/rapport-v4-hca.md:131`
- **SWAR** — décodage de 8 varints dans un mot de 64 bits ; `reports/rapport-optimisations.md:19`
- **SwiGLU** — FFN à porte, clamp `swiglu_clamp_exp` manquant ; `reports/rapport-v4-hca.md:125`
- **TCP_NODELAY** — désactive Nagle, divise l'attente par six ; `reports/rapport-transport-liste.md:198`
- **TLB** — pages de 4 Ko vs 2 Mo (coût /512) ; `reports/rapport-passage-a-l-echelle.md:160`
- **VRAM** — cache experts, miroir KV (1,7–1,8 ms) ; `reports/rapport-optimisations-auto.md:67`
- **YaRN** — extension RoPE, « à retardement » par défaut, `DRAVE_YARN=1` ; `reports/rapport-routage-experts.md:126`
- **k-WTA** — inhibition latérale, 10× meilleur que le seuil ; `reports/rapport-parcimonie-imposee.md:24`
- **A3B** — Qwen3-30B-A3B : 3,3 G actifs sur 30 B, top-8 ; `reports/rapport-passage-a-l-echelle.md:15`
- **Q8_0 / Q4_0 / Q4_K / Q4_K_M / Q6_K / Q8_1** — types GGUF (Q8_1 = activations ggml) ; `reports/rapport-optimisations.md:4`, `reports/rapport-passage-a-l-echelle.md:13`, `reports/rapport-v4-couches-0-1.md:49`
- **f32 / f16 / int8 / int4** — précisions du KV et des flux ; `reports/rapport-placement-bits-kv.md:4`
- **super-bloc** — unité IQ de déquantification / bloc de 256 poids Q4_K-Q6_K ; `reports/rapport-p0-flux.md:20`
- **paire** (poids × activation payé) — `Model::paires: [u64; 3]` par provenance ; `reports/rapport-p0-flux.md:36`
- **paire hyperthread** — threads partageant L1/L2, épinglés si < 8 cœurs ; `reports/rapport-optimisations-auto.md:13`
- **événement** — paire à poids non nul ; `reports/rapport-p0-flux.md:31`
- **provenance** — 0 attention, 1 experts routés, 2 partagé ; `reports/rapport-p0-flux.md:36`
- **push / pull** — listes d'événements vs produit scalaire dense ; `reports/rapport-p0-flux.md:13`
- **porte** (1) — porte de non-régression du dépôt (Qwen 19,3885) ; `reports/rapport-p0-flux.md:51`, `:134` de l'autre rapport
- **porte** (2) — `attn_compressor_gate` V4 (poids softmax par canal) ; `reports/rapport-v4-hca.md:15`
- **porte de correction** — validation partielle, pas du modèle entier ; `reports/rapport-v4-couches-0-1.md:85`
- **mode 0/1/2/3/4** — dense f32, listes, blocs, LOT, lot en listes ; `reports/rapport-transport-liste.md:15`, `reports/rapport-prefill-reparti.md:15`, `:107`
- **protocole v5** — cinq modes + contrat d'activation (14 champs) ; `reports/rapport-session-2026-09-30.md:18`
- **en-tête / magie / TAILLE_TETE** — 39 → 79 octets ; `reports/rapport-transport-liste.md:10`, `reports/rapport-prefill-reparti.md:17`
- **indices par écarts** — delta 1 octet, 255 = échappement ; `reports/rapport-transport-liste.md:169`
- **échelle par bloc de 32** — i8 + échelle f32 (`--flux-blocs`) ; `reports/rapport-transport-liste.md:100`
- **densité d'activation** — bascule événementiel/dense à 22 % ; `reports/rapport-passage-a-l-echelle.md:39`
- **b/poids** — bits par poids (1,98 événement ; 0,53 en 4 bits) ; `reports/rapport-optimisations.md:37`
- **G év/s** — milliards d'événements/s (3–5 sur CPU de bureau) ; `reports/rapport-optimisations.md:70`
- **Go/s, Mo, Ko, ms, Mbit/s, GFLOP/s** — unités des mesures ; `reports/rapport-optimisations-auto.md:46`, `reports/rapport-transport-liste.md:183`, `reports/rapport-programme-evolutif.md:113`
- **perplexité / PPL** — métrique de référence ; `reports/rapport-optimisations-auto.md:117`
- **tok/s, jetons/s, évaluations/h** — débits (41,6 ; 5,62 ; ~100/h) ; `reports/rapport-passage-a-l-echelle.md:47`, `reports/rapport-travail-reel.md:22`, `reports/rapport-programme-evolutif.md:84`
- **latence / aller-retour** — « attente ≈ calcul distant + 3,2 × latence » ; `reports/rapport-prefill-reparti.md:12`
- **Nagle / ACK différé** — 97,6 ms/jeton, corrigé par `set_nodelay(true)` ; `reports/rapport-transport-liste.md:196`
- **mmap / madvise(WILLNEED) / posix_fadvise(DONTNEED) / readahead / page cache** — prélecture sans gain ; `reports/rapport-optimisations-auto.md:79`, `reports/rapport-tete-garantie.md:94`
- **premier-touch (first-touch)** — allocation NUMA à paralléliser ; `reports/rapport-passage-a-l-echelle.md:155`
- **mmap paresseux** — 2,7 Go/s ; `reports/rapport-optimisations-auto.md:89`
- **bitmap** — 1 bit/poids + signe (1,09 Mo, 1,99 b/poids), débit constant ; `reports/rapport-optimisations.md:38`
- **SparseVec** — indices triés + valeurs contiguës, 8 octets/source active ; `reports/rapport-optimisations.md:26`
- **FusedSign** — liste unique triée par destination + plan de signe ; `reports/rapport-optimisations.md:32`
- **PushMat / DenseQ8 / DenseQ4** — listes / int8 dense / 4 bits ; `reports/rapport-passage-a-l-echelle.md:39`
- **events_total() / row_ev[i] / touched / row_delta_into** — compteur et réduction incrémentale ; `reports/rapport-p0-flux.md:13`, `reports/rapport-optimisations.md:93`
- **matvec / matvec_f32 / matvec4_ou_iq / attn_mla / logits / logits_lot / logits_garanti** — noyaux et points de comptage ; `reports/rapport-p0-flux.md:19`, `reports/rapport-tete-garantie.md:14`
- **forward / forward_lot / forward_mla** — passes avant ; `reports/rapport-phase3-reparti.md:33`
- **Model::load / load_partiel / verifier_architecture / router / emb_imposee(_lot) / flux_brut / couche_debut..couche_fin** — API interne citée ; `reports/rapport-passage-a-l-echelle.md:116`, `reports/rapport-routage-experts.md:43`, `reports/rapport-prefill-reparti.md:30`, `reports/rapport-phase3-reparti.md:28`
- **Pool::gemm_dense_i8 / gemm_dense_q4 / Pool::attendre / Shared::gs32 / Shared::morts / catch_unwind / AtomicPtr** — pool et lot ; `reports/rapport-prefill-par-lots.md:12`, `:170`
- **q4_blocks() / q8_view() / gguf::q8_dot_at** — lecture en place ; `reports/rapport-passage-a-l-echelle.md:121`, `reports/rapport-prefill-par-lots.md:133`
- **tuilage** — groupes de 16 jetons (8 en 4 bits) ; `reports/rapport-prefill-par-lots.md:63`
- **engram** — sonde disque 264 octets ; `reports/rapport-optimisations-auto.md:103`
- **aiguille / Aiguille v2 / sonde** — `tools/aiguille.py`, 9/9 ; `reports/rapport-placement-bits-kv.md:144`
- **hyper-connexion** — mélanges de copies (`hc_attn_pre`, `hc_post`, 24 mélanges, Sinkhorn 20 it.) ; `reports/rapport-p0-flux.md:120`
- **Sinkhorn** — normalisation itérative des hyper-connexions ; `reports/rapport-v4-couches-0-1.md:55`
- **puits (attention sink)** — `attn_sinks` / `ggml_soft_max_add_sinks`, ajouté brut ; `reports/rapport-v4-couches-0-1.md:7`
- **ape** — ligne apprise par rang de bloc, `[512, 128]`, ajoutée à la porte HCA ; `reports/rapport-v4-hca.md:17`
- **indexeur / lightning indexer** — `ggml_lightning_indexer`, `relu(q·k)` puis top-k ; `reports/rapport-v4-hca.md:96`
- **nope / dé-rotation (derope) / rope_norm** — parties tournée/non tournée et inverse RoPE ; `reports/rapport-v4-hca.md:52`, `reports/rapport-v4-couches-0-1.md:40`
- **fenêtre glissante / sliding_window / build_raw_tail** — fenêtre brute 128 et queue d'attention brute ; `reports/rapport-v4-couches-0-1.md:81`
- **compress_ratios / compress_rope_freq_base / n_visible** — 21 CSA (4), 20 HCA (128), 3 brutes ; base 160 000 ; `reports/rapport-v4-couches-0-1.md:11`, `reports/rapport-v4-hca.md:24`
- **routeur / top-k / renormalisation / expert partagé / scoring_func / expert_gating_func** — conventions MoE corrigées ; `reports/rapport-routage-experts.md:14`
- **routed_scaling_factor (expert_weights_scale)** — 1,5 ; 2,5 ; 2,827 ; `reports/rapport-routage-experts.md:26`
- **hash_layer_count / ffn_gate_tid2eid.weight** — routage par table, I32 `[129 280 × 6]` ; `reports/rapport-routage-experts.md:30`
- **archs `qwen3moe`, `gpt-oss`, `deepseek2`, `glm-dsa`, `glm5next`, `deepseek4`, `deepseek41`** ; `reports/rapport-routage-experts.md:16`
- **grappe** — groupe k-moyennes ; localité retenue, difficulté rejetée ; `reports/rapport-programme-evolutif.md:5`
- **η² / R² / r** — 6,2 % ; +0,007 ; +0,573 ; `reports/rapport-programme-evolutif.md:36`
- **trace hebbienne / `--hebbian`** — journal de co-activation ; `reports/rapport-programme-evolutif.md:67`
- **monômes quadratiques** — 401 856 `x_i·x_j` hors span ; `reports/rapport-programme-evolutif.md:72`
- **prune → retrain (masque fixe) → quantize → refit d'échelle** ; `reports/rapport-precision.md:5`
- **frontière de Pareto** — accuracy max à coût donné ; `reports/rapport-precision.md:43`
- **unaire (répétition d'adresse) / plans binaires / popcount** ; `reports/rapport-valeur-unaire.md:28-29`
- **inégalité de Kraft / entropie (b/poids)** — 3,731 b/poids ; `reports/rapport-valeur-unaire.md:51`
- **BitNet b1.58 / ternaire / listes signées** — 0,39 b/poids ; `reports/rapport-valeur-unaire.md:86`
- **Heaps (exposant)** ≈ 0,21 ; `reports/rapport-tete-restreinte.md:21`
- **jargon de banc** : harnais, banc, rejeu, trace, drapeau ignoré, porte verte, `--options-actives`, `--options-strict` ; `reports/rapport-optimisations.md:57`, `reports/rapport-session-2026-09-30.md:21`
- **Colab / notebook / tunnel** — `colab/README.md`, `tools/colab_cote_local.sh` ; `reports/rapport-session-2026-09-30.md:20`
- **pilote / pair / nœud moteur / flux** — couches 0..12 locales, 12..24 distantes ; `reports/rapport-phase3-reparti.md:9`
- **plafond cumulatif R4** — refus à l'état 72 393 (256 Mo) ; `reports/rapport-session-2026-09-30.md:76`
- **P1–P6, P4 (HCA), P5 (CSA + indexeur)** ; `reports/rapport-p0-flux.md:72`, `reports/rapport-v4-couches-0-1.md:79`
- **SpikeGPT / R̂ = 0,15** — facteur 6,7× ; `reports/rapport-parcimonie-imposee.md:116`
- **OpenBLAS / moindres carrés / autogradage / rétropropagation** — 759 GFLOP/s, pas d'optimiseur ; `reports/rapport-programme-evolutif.md:112`
- **plomberie** — charger un modèle patché ; `reports/rapport-programme-evolutif.md:128`
- **ABSENTS des 20 fichiers** : DRVF/DRVF v5, PTX, RSS, IQ2_XXS, HBM, M20K, greffon, liste valuée, shard, p50/p95, MTok/s, Gbit/s, bf16, Hadamard, LoRA, MTP, MMLU/MNIST.

## B. Chiffres et affirmations mesurées
**optimisations-auto.md** — :17 « 25,8 Go/s, 2× le PCIe » · :29 « | 20 cœurs | **22,5** | » · :30 « | 20 cœurs + hyperthreads (40 fils) | 18,9 | » · :31 « | 10 cœurs | 14,7 | » · :32 « **18,7** (+27 %) » · :33 « 15,0 — régression » · :38 « `cpu × 3/4` = **30** fils ... il en prend **20** » · :46 « 5,37 | 9,68 | 18,08 | 28,29 | **31,08** » · :48 « Vérifié sur 50,5 Go ... : 3,42 / 21,02 / 33,19 » · :49 « Le NVMe parallélisé dépasse la RAM (31 contre 22 Go/s) » · :53 « seuil ... un tiers de la RAM libre » · :56 « 90 Ko par jeton en F16, soit 96,6 Go à 1 M — plus que les 71 Go d'experts. En int8, 48,3 Go » · :62 « ctx 4096 : ... 32 bits, 0.20 Go pour 4096 jetons » · :63 « 51.5 Go en f32 pour 262144 jetons ... (116 Go) » · :69 « VRAM libre − 2 Go de réserve CUDA − le commun » · :70 « VRAM lit à 84,9 Go/s contre 22,5 » · :79 « 25,73 s contre 25,80 | 0,3 % » · :80 « 7,29 s contre 7,47 | −2 % » · :82 « 6,8 s contre 30,5 s ... 4,5× » · :84 « modèle de test (18,6 Go) tient dans les 115 Go » · :88 « 7,10 s à 4 fils contre 6,80 s à 20 fils » · :89 « 2,7 Go/s ... NVMe (2,1 à 5,5 Go/s) » · :95 « V4.1 (365 Go pour 115 Go de RAM) » · :104 « 16 ms par entrée de 264 octets » · :110 « 25,73 s avec, 25,80 sans, soit 0,3 % » · :117 « densité 5,1 % ⇒ perplexité ×107 » · :122 « +10,5 % ... à +15 % » · :129 « trois `fetch_add` par appel de tête » · :134 « 35 tests verts ... Qwen 19,3885 et clusters 799,8557 »
**optimisations.md** — :4 « 4864 entrées × 896 sorties, **4 303 745 événements** » · :6 « 2 × Xeon E5-2687W v3 (20 cœurs / 40 CPU logiques), NUMA 2 nœuds » · :16 « 0,484 ms → 0,011 ms (×44) » · :21 « 99,99 % ... décodés 8 à la fois » · :28 « 8 octets par source active » · :37 « 4,89 Mo (8,97 b/poids) contre 4,34 Mo (7,98 b/poids) ... bitmap+signe 1,09 Mo (1,99 b/poids) » · :47-53 densités « 0,011 ms » / « 43 560 ... 0,14 / 0,42 » / « 216 960 ... 1,15 / 1,50 » / « 430 359 ... 1,81 / 2,30 » / « 1 076 785 ... 3,18 / 3,86 » / « 2 152 648 ... 4,14 / 4,89 » / « 4 303 745 | **4,51 G év/s** (0,95 ms) | **5,44 G év/s** (0,79 ms) » · :55 « 14 vérifications sur 14 » · :60 « 0,011 ms à 0,95 ms ... (rapport 86) » · :67 « 0,41 ... 4,45 ... **4,84** | 2,04 ❌ » · :68 « 0,42 ... 5,24 | **5,78** | 2,59 ❌ » · :70 « 0,15–0,18 G év/s par thread ... 0,8–1,3 événement par cycle » · :71 « 124 MHz × 32 PEs = 4 G év/s » · :75 « load ~1,5–5 : ±20 % » · :77 « refuse ... `CPU − 1` et prend `3/4 × CPU` » · :86 « 3838 vs 3513 ... 7,53 G év/s. Les deux chiffres étaient faux » · :105 « 3,09 à 0,97 G év/s (8 threads) » · :115 « 4,84 → 2,04 G év/s » · :121 « a tout empiré (0,97 G à 8 threads) » · :138-141 « 2,5 ms | 4,36 M » / « 112,3 ms | 13,58 M (3,12 additions/poids) » / « ×44,9 » / « identique ✅ » · :143 « 3,12 bits à 1 ⇒ ~3 additions par poids » · :156 « 3–5 G év/s sur un CPU de bureau »
**p0-flux.md** — :9 « 0 événement en listes, la totalité des matrices est payée » · :36 « `Model::paires: [u64; 3]` » · :47 « attention | **44,2 M** | ... **44,04 M** ✅ » · :48 « partagé | **451,2 M** | ... 313,7 M + 136,1 M = 449,8 M ✅ (0,3 %) » · :49 « experts | 0 | pas de MoE ✅ » · :51 « Qwen2.5-0.5B ctx 256 = 19,3885 » · :55 « GLM-5.3 (79 couches, MLA, 256 experts top-8, 216,7 Go) » · :60-64 « attention 21,9 G / 37,7 % » « experts 30,6 G / 52,6 % » « partagé 5,6 G / 9,7 % » « total 58,2 G » « listes 0 / 0 % » · :73 « 8 experts sur 256, soit 3 % » · :78 « 21,9 G paires pour 4 positions » · :91 « attn_k_b [64, 512, 192], attn_v_b [64, 256, 512], nh = 64, 79 couches » · :92 « 662,7 M paires par passe ... 1 988,1 M ... (trois passes) » · :98-101 « 14533,9920 → 14533,9920 » / « 29 224,8 M → 27 236,7 M » / « −1 988,1 M » / « 83 104,0 M → 81 115,9 M » · :108 « 41,8 s contre 215,7 s » · :111 « 14 024 ms → 12 256 ms » · :118 « porte (15,6017) » · :119 « corrélation 0,999024 » · :124 « 216,7 Go ... 190 s de chargement, 147 s/jeton »
**parcimonie-imposee.md** — :5 « deux jeux de 1 024 tokens » · :10 « charge de 8 à 14 » · :17 « 0,00 % d'activations nulles » · :28 « référence 19,2647 pour 352,8 M événements » · :32-37 « 343,8 M (−2,6 %) ... 19,5750 » « 312,3 M (−11,5 %) ... 20,1511 » « 230,8 M (−34,6 %) ... 30,5837 » « 145,0 M (−58,9 %) ... **2264,84** | **117×** » · :39 « 11 % ... 5 % » · :49-52 « 354,3 M | 23,6125 | 26,2565 » « 301,5 M (−14,9 %) | +0,57 % | +1,23 % » « 283,7 M (−19,9 %) | +0,90 % | +2,29 % » · :54 « dix fois moins » · :71 « FFN complet à 85 % | **308,0 M (−13,1 %)** | **−0,18 %** | **+0,46 %** » · :84 « +0,2 % à 90 %, +1,2 % à 85 %, +3,6 % à 80 % » · :96 « −12,7 % de CPU » · :97 « −3,0 % de CPU » · :101 « un `select_nth` ... 168 par token » · :104 « entre 3 et 13 % de temps CPU pour 13-15 % d'événements » · :110 « ~13 % ... ~0,5 % » · :116 « facteur 6,7× ... R̂ = 0,15 » · :122 « 3,8 M au lieu de 349 M »
**passage-a-l-echelle.md** — :11 « 0,53 Go | Q8_0 | ✅ » · :13 « 4,5 Go | Q4_K 6,09 G + Q6_K 1,52 G | ❌ » · :17 « 60,5 Go | MXFP4 114,66 G + Q8_0 2,11 G | ❌ » · :19 « ne lit que F32, F16, Q8_0 et Q4_0 ... Aucun modèle récent ne s'ouvre » · :32 « t = octets_actifs_par_jeton / bande_passante » · :39-41 « 1,98 ... < 22 % » « 1,00 ... > 22 % » « 0,53 » · :43 « 20–25 Go/s (≈ 68 par socket, 136) » · :46 « 13 ms/jeton = 41 tok/s, contre 41,6 tok/s mesurés » · :56-61 « 41,6 » « 5,4 » « 1,2 » « 11,5 » « 7,4 » · :63 « plafonne vers 7 B ... 32 B » · :84 « super-blocs de 256 poids, échelles et minima sur 6 bits » · :91 « Bloc de 17 octets » · :94 « 12 % de perplexité sur Q4_0 » · :101 « dims = (2880, 2880, 128) type 39 » · :102 « min 119 max 121 médian 120 » · :103 « médian 1.000, min 0.667 » · :111 « 128 experts empilés dans un tenseur 3D » · :120 « 60 Go de fichier + 61 Go de copie 4 bits = 121 Go sur 125 » · :145 « 0,88 / 1,91 / 3,20 ms à 64 / 128 / 256 » · :152 « 20–25 Go/s ... ~136 » · :160 « pages de 2 Mo ... par 512 » · :165 « 20,7 → **24,7 Go/s** » · :175 « 1,98 o, soit 3,7× ... ~1,5 o/événement » · :178 « ×1,7 entre 4 et 32 threads » · :179 « QSFP+ 4,8 · NVLink 25,78 · PCIe x8 6,5 Go/s »
**phase3-reparti.md** — :9 « 12 couches chacun, contexte 256 » · :20 « locale vaut 144,8289 » · :28 « 1 621,7 → 693,4 » · :44-46 « 144,8289 | 1 621,7239 | ×11,2 » / « 693,4492 | ×4,8 » / « **144,8289** | **0,00e0** » · :50 « 1 024 jetons (1 023 flux servis ... 9,5146 ... 0,00e0) » · :53 « 19,4 ms ... 19,7 ms » · :62 « 3 663 octets par flux (79 + 896 × 4) » · :64 « 6 octets par neurone actif »
**placement-bits-kv.md** — :4 « facteur 130 à 840 » · :5 « 39 % ... +0,018 % » · :9 « 8 191 jetons notés, contexte 8 192 » · :15-23 table « 14,2339 » / « 14,2372 | +0,023 % » / « 14,6622 | +3,01 % » / « 14,2994 | +0,46 % » / « 69,0464 | +385 % » / « 14,6667 | +3,04 % » / « 14,2365 | +0,018 % » / « 66,0369 | +364 % » / « 14,3209 | +0,61 % » · :30-36 frontière 16 %→+364 %, 39 %→+0,018 %, 100 % référence · :39 « point utile est à 39 % ... par 2,5 » · :47 « facteur 130 » · :49 « +385 % (69 au lieu de 14,2) ... facteur 840 » · :58 « 3,125 octets (39 %) pour +0,018 % » · :61 « n'est PAS significatif (8 191 jetons) » · :67 « q8_0 coûte +0,8 % » · :78 « à 4 096 : +0,011 % » · :87-90 « 12,2175 » / « 12,2188 | +0,011 % » / « 12,4921 | +2,25 % » / « 12,2223 | +0,039 % » · :113 « 262 144 clés, 24 couches, 16 fils » · :117-119 « f32 | 70,5 | 1,8 ms | +3,2e-5 » / « f16 | 162,1 (2,3×) » / « int8 | 174,0 | 1,7 ms | +3,4e-5 » · :123 « 162 contre 70 ms » · :137 « par 40 (43 ms contre 1,7 s à 262 k) » · :148 « Qwen2.5-1.5B-Instruct Q4_K_M, contexte 2 048, profondeurs 0,1/0,5/0,9 » · :152-154 « 3/3 » ×3 · :157 « +2,25 % de perplexité » · :177 « 25 à 28 minutes à contexte 8 192 »
**precision.md** — :3 « MLP 32→64→10, 2688 poids ... 76.07 % » · :12 « 1 + k·d bits/poids » · :22-41 table (60.06 %/1.08 ; 65.04 %/1.24 ; 67.29 %/1.37 ; 70.41 %/1.48 ; 72.17 %/1.99 ; 73.44 %/2.00 ; 74.22 %/2.50 ; 76.07 %/3.00 ; 76.27 %/5.00 ; 76.37 %/8.00) · :47-58 frontière de Pareto · :63 « DDR3 (9,66 Go/s) ; 312 voies » · :69 « 30-35 ALM contre ~20 pour le PE ternaire » · :71 « ~11 000 ALM, soit 6 % du FPGA au lieu de 4 % »
**prefill-par-lots.md** — :4 « 4,5 h à 32 k, 1 234 h à 1 M » · :24 « perplexité mesurée 1 614 183 » · :26 « 2 880 au lieu de 4 096 » · :31 « n_ff au lieu de h » · :33 « 768 contre 2 048 » · :34 « 7,6139 avant comme après » · :40-41 « 13,1368 | **13,1359** » / « 13,7149 | **13,7205** » · :43 « écart (6e-5 à 4e-4) » · :52-55 « 16,6 s » / « 23,2 s » / « 20,0 s » / « 18,1 s » · :57 « noyau est 2,4× plus rapide » · :60 « 229 Ko — 4 864 relectures » · :63 « groupe de 16 jetons (8 pour le 4 bits) » · :75-80 « 3,05 → 1,49 ms » / « 4,05 → 8,90 | ×2,2 ✗ » / « 25,31 → 20,92 | ÷1,2 » / « 33,14 → 31,31 | −5 % » / « 8,36 → 8,75 » / « 41,5 → 40,1 | −3 % » · :88 « rep = 7 » · :89 « 145 Mo lus par jeton » · :96 « 151 936 lignes, trente fois plus » · :115-122 « 2,58 → 0,99 | ÷2,6 » / « 2,78 → 5,59 | ×1,7 ✗ » / « 20,75 → 14,54 | ÷1,43 » / « 26,57 → 21,13 | ÷1,26 » / « ~5,63 → 5,47 » / « 34,5 → 28,2 | −18 % » · :124 « 17,1 s → 13,6 s, soit −20 % » · :126 « 33,7 / 33,9 / 34,4 s ... 13,7205 » · :131 « 5,47 contre ~5,63 ms/jeton » · :137 « 6,2 ms/jeton contre 15,6 » · :153 « src/engine.rs:473:77: index out of bounds: the len is 90 but the index is 90 » · :156 « 90 = ... (2 880 / 32) » · :168 « dix minutes ... blocage de 27 minutes » · :172 « lots de 1, 8, 9, 17 et 40 ... 256 colonnes ... blocs (8) » · :193-194 « 17,1 s → 13,6 s | −20 % » / « ≈ 50 s → 34,4 s | −31 % » · :197 « porte ... 19,3885 » · :187 « facteur ... de l'ordre de 16 »
**prefill-reparti.md** — :5 « 4 lots (ou un seul) au lieu de 255 flux » · :12 « 3,2 × latence par message » · :13 « 256 jetons coûtaient 15 secondes » · :41-44 « 0,00e0 (18,0851 = 18,0851) » / « UN lot de 917 583 octets | 0,00e0 » / « 255 | 0,00e0 (18,0206 = 18,0206) » / « 16 | 0,00e0 (9,5939 = 9,5939) » · :48 « ~1e-4 sur Qwen » · :57-59 « 1 145 ms | 1 488 ms | 2,6 s » / « 350 ms/jeton | 394 ms/jeton | 47,6 s » · :61 « 18× » · :62 « ~4 × 20 ms ... 62 sur 63 » · :73-76 « 116,7 ms » / « 358,0 | 22,4 » / « 1 185,3 | 18,5 » / « 4 255,6 | 16,6 » · :78 « 7× plus rapide » · :86 « 3 663 octets par jeton » · :89 « sous 1 Mbit/s » · :93 « 40 octets pour un TAILLE_TETE de 39 » · :101 « 5,61e0 au lieu de 0,00e0 » · :107 « ÷2,3 ... 2,7 % »
**programme-evolutif.md** — :17 « +3,0 % (96,75 s → 99,64 s) » · :18 « 7 Mo pour 2 048 tokens » · :19 « 19 Mo/s à 15,8 tok/s » · :23 « 1,2 Mo/token au lieu de 706 Mo » · :27 « 16 threads sur 40 ... 125 Go ... 1,3 Go » · :36 « η² ... 6,2 % » · :37 « 7,1× (5,51 contre 0,77) » · :39 « R² ... +0,007 » · :40 « r = +0,573 » · :41 « K=128 | r = +0,232 » · :42 « R² < 0 (−7,5 à −0,21) » · :53 « +30 % ... 17,91 contre 13,77 » · :64 « 69,2 % ... saturées » · :67 « 100,00 % » · :69 « 30,8 % ... attn_k (127/896), attn_v (128/896), ffn_down (896/4864) » · :72 « 401 856 monômes » · :84-86 « 98/h » / « 83/h » / « ~112/h » · :89 « ~100 ... 2 400 par jour » · :91 « mal en charge au-delà de 8 threads » · :96 « zéro octet » · :102 « 706 Mo/token à 10,4 Go/s ... 28,7 (2,8×) » · :105 « ~2,8 passes » · :113 « OpenBLAS à 759 GFLOP/s »
**routage-experts.md** — :19-22 « 2 — sigmoïde » / « 4 — racine de softplus » / « dense : n_expert = 0 » · :26 « 1,5 ... 2,5 ... 2,827 » · :30 « trois premières couches ... par table » · :32 « [129 280 × 6] » · :39 « 341 Go » · :64-66 « 19,3885 | 19,3885 » / « 799,8557 | 799,8557 » / « 15,1757 | 15,6017 » · :72 « 15,1757 était auto-cohérent, pas juste » · :75 « 799,8557 à 799,8152 (−0,005 %) » · :78 « x / s au lieu de x * (1/s) ... 48 couches » · :79 « 28 s de compilation » · :91-95 « 1 026 G » / « 754 G » / « 755 G » / « 284 G » / « 321 G » · :99 « aucun de ces cinq modèles n'a jamais été exécuté » · :116-118 « 5420,40 » / « 6443,13 | 0,989242 | 0,4364 | 2/4 » / « 6625,80 | 0,989142 | 0,4134 | 2/4 » · :125-127 « 166,85 » / « 15,6017 » / « 84,07 » · :132 « 174,34 contre 18,58 » · :136 « 19,3885 contre 18,9750 (2,2 %) » · :150-151 « 4286,13 » / « 42 617 589 | −0,039 | 0/3 » · :154 « MÊME jeton (106880) »
**session-2026-09-30.md** — :3 « 10h06–11h42 ... 11h46–15h00 ... 15h07–18h00 » · :12 « 0,00e0 — 144,8289 ... 9,5146 à 1 024 » · :13 « 4 lots ... 18× » · :14 « 3 663 → 1 629 (÷2,3) pour 1,3 % » · :15 « +0,023 % contre +3,01 % (130) ; +0,46 % contre +385 % (840) » · :16 « 132 396 736 → 66 370 408 → 45 079 930 (+0,074 %) » · :17 « 1,5 ko ... 3,03e-2 » · :18 « cinq modes ... (14 champs) » · :19 « 968 ms ... contre 13,2 ms » · :20 « 4,5 Mo ... ~20 au lieu de 17 869 » · :21 « 46 sur 110 » · :22 « 80 ... 38 périmées, 15 contradictoires » · :27 « vingt-sept n'ont pas été trouvés par un banc » · :31 « ×11,2 » · :46 « 16 Gio sur une trame de 83 octets » · :52 « rejeu v3 = 19,3885 ... faux positif » · :53 « 19,3045 ... vaut 19,5633 » · :60 « 17 au total » · :68 « 9/9 sondes » · :70 « 70 ms ... 162 ms ... 174 ms » · :72 « 1,7 ms (43 ms sur 24 couches) » · :74 « 0,00e0, seize lots de 64 » · :76 « 258 Mo ... état 72 393 » · :92 « 19,3885 · 15,1757 · 15,1667 » · :93 « cargo test 13/13 ... quarante commits »
**tete-garantie.md** — :9 « 12,6 fois plus lâche » · :17 « 151 936 lignes » · :31-32 « [512, 13309, 321, 1788, 12422, 84, 13, 356] » ×2 · :44-48 « +1,4283 » / « 18,0381 — ×12,6 » / « 17,6646 — ×12,4 » / « 2 048 / 2 048 = 100 % » · :52 « 151 936 lignes sur 151 936 » · :54 « 5 à 20× trop lâche » · :70-71 « ×7 sur la tête (13 %) » / « nul (12,6× trop lâche) » · :92 « 5,37 Go/s ... 31 Go/s » · :95 « 120 blocs de 4 Mo » · :99-100 « 0,26 | 0,20 | ×0,78 » / « 3,11 | 2,72 | ×0,88 » · :107 « facteur 5,8 » · :109 « cinquième fois »
**tete-restreinte.md** — :16-19 « 1 462 | 0,96 % » / « 4 659 | 3,07 % » / « 15 768 | 10,38 % » / « 19 793 | 13,03 % » · :21 « Heaps ≈ 0,21 ... 13 % est un plafond » · :28-30 « médian 3 » / « p90 250 » / « maximum 4 319 » · :32 « 16 384 tokens contient donc 100 % » · :41-42 « 9,384 s → 8,400 s | +10,5 % » / « 1,155 s → 0,982 s | +15 % » · :52-54 « [6224, 1076, 330, 438, …] » / « [1129, 269, 330, 304, …] puis boucle » / « [77455, 330, 279, …] » · :67 « 608 Ko pour 151 936 tokens » · :72 « cosinus ... 0,05 à 0,2 ... 5 à 20 fois » · :75 « tête entière prend 6,9 ms » · :93-96 « 85,4 % | 19,3885 » / « 61,5 % | 22,3563 | +15 % » / « 30,3 % | 28,7635 | +48 % » / « 5,1 % | 2 073,80 | ×107 » · :115 « retirée du code » · :124 « 4 000 premiers »
**transport-liste.md** — :4 « 897 au lieu de 3 623 ... 1 568 » · :6 « ×1,8 de perplexité » · :10 « 39 ... 79 » · :15 « 3 623 (39 + 3 584) » · :25-29 « 0,00e0 » / « 3 623 | 141,0539 | 2,6e-2 » / « 2 203 | 2 677 | 4,9e-2 » / « 897 | 993 | 8,1e-1 » / « 1 347 | 216 | 8,8e-1 » · :35 « écart 0,69 » · :47 « 16 bits ... 2,6 % » · :69 « 0,00e0 à 5,61e0 (119 contre 18,02) » · :89 « cette build parle la 5 » · :92 « écart 0,69 mesuré » · :95 « 896 ... 919 (division par 39 au lieu de 40) » · :100 « indice u16, valeur i8 » · :105-107 « 2 793 | 7,1e-2 » / « 1 778 | 2,2e-3 » / « 799 | 1,1e0 » · :122 « ÷2,3 ... 2,7 % » · :128 « référence locale vaut 18,02 » · :132-135 « 3 623 | 0,00e0 » / « 2 268 | 2,7e-2 » / « 2 159 | 1,6e-1 » · :149-152 « 1,37e-1 | 2 249 | 77,9 % » / « 1,32e-2 | 1 589 | 79,8 % » · :161 « 1,3 % à 1 024 (2,7 % à 256, 13,7 % à 64) » · :178 « 1 568 | 2,74e-2 | 21,8873 » · :183 « 0,25 Mbit/s » · :191-194 « 15,6 | 15,9 » / « 97,6 | 16,1 » / « 6,26× | 1,01× » / « 24,5 s | 8,3 s (8,2 s) » · :200 « divise l'attente par six » · :209-211 « 16,8 | 1,01× | 11,0 s » / « 33,0 | 1,99× | 15,1 s » / « 81,8 | 4,89× | 27,6 s » · :217 « 3,2 × latence » · :224 « 112 ms par jeton ... ~8 au lieu de ~60 » · :231-232 « 3 623 ... 1 989 ... moins de 1 Mbit/s »
**travail-reel.md** — :3 « 30,5 G paramètres ... 16 fils » · :21 « 89 jetons en 15,8 s (5,62 tok/s), 166 ms » · :36 « arrêt spontané après 67 jetons » · :43-44 « Q4_K / Q6_K / Q8_0 / Q4_0 / MXFP4 ✅ » / « 30 B en 17,7 Go ✅ » · :48 « 0,5 B : 32 · 1,5 B : 17 · 30 B MoE : 5,6 · 7 B : 2,8 » · :82 « 5,5 tok/s ... 117 G ... 62 Go » · :85 « perplexité de 39,8 ... de l'ordre de 6 » · :89 « 4 424 jetons » · :108 « 800 Mo à 8 k ... +100 ms/jeton » · :117 « 5,6 jetons par seconde »
**v4-couches-0-1.md** — :5 « 1e-7 ... 0,99999 » · :11-12 « 21 CSA (4), 20 HCA (128), 3 brutes (0, 1, 43) » · :28 « 20 000 octets de WikiText-2 » · :36-42 « 1,000000 | 1,5e-8 » / « 0,999993 | 1,1e-3 » / « 0,999996 | 1,9e-2 » / « 0,999811–0,999959 | 1,7e-2 » · :46-47 « 49,5 % ... 0,1 % ... 1,0e-3 sur 0,9 » · :55 « Sinkhorn à 20 itérations » · :61 « 0,99866 → 0,999993 » · :69 « position 1 fausse de 30 % » · :79 « couches 2 à 42 » · :82 « sliding_window 128 » · :84 « 32 bits » · :91 « NLL moyenne 11,077944 · perplexité 64 727,68 » · :93 « 11,737136 / 125 133 »
**v4-hca.md** — :5 « 0,999992 au 128ᵉ jeton » · :15 « 512 dimensions » · :18 « [512, 128] » · :24 « 160 000, pas 10 000 » · :26 « n_visible = (pos + 1) / ratio » · :36-38 « 1,000000 » / « 0,999992–0,999994 » / « 0,99997–0,999991 » · :46 « 0,02 sur 6,5, soit 0,3 % » · :51-53 « 10 % ... 64 dernières ... 448 premières ... 0,4 % ... 0,996 » · :64 « passe de 86 Go » · :70 « 2 × ratio » · :72 « 1024 valeurs » · :76 « 0,999990–0,999991 ... 0,99992–0,999994 » · :84 « 0,989 au lieu de 1,000000 » · :86 « 0,42 ... 0,80 » · :90 « 0,003 » · :110 « 0,1 à 0,3 % » · :112 « 2 048 jetons » · :120 « top_k (512) » · :122 « 4 × 512 = 2 048 » · :127 « swiglu_clamp_exp = 10.0 »
**valeur-unaire.md** — :3 « qwen2 ... Q4_0 (166 matrices 2-D) » · :4 « −8..+7 » · :8-10 « 12.9 % ... 87.1 % » / « 3.02 » / « 1.39 » · :28 « unaire 2.02 | 3.02 » · :30 « hybride 1.12 | 1.12 » · :45 « 2.63 contre 4,00 » · :49 « Le ×2,17 ... est FAUX » · :51 « Σ2^−l ≈ 1,99 > 1 » · :55 « 3,5-4,4 b/poids » · :57 « 3,731 b/poids (×1,07) » · :79 « 2.63 contre 4,00 » · :83 « 1.85 b/poids, soit ×2.17 ... 0.98 contre 0.87 » · :89 « 0,39 b/poids » · :99 « Q4_K_M ... à mesurer »

PARTIE 2/2 (C et D) suit dans le message suivant.

### 👤 Utilisateur

Background subagent fba448b3-e237-4eb3-b77d-fcbf7da1c93d finished and will do no further work unless you send it more.
Its closing message:
⏵ Livrable livré en 3 messages au parent ; récapitulatif final

Inventaire terminé : les 20 fichiers ont été lus intégralement (3 058 lignes), aucun fichier du dépôt n'a été modifié. Le livrable complet (sections A, B, C, D) a été transmis au parent en 3 messages :

1. **A. Termes et sigles** — ~150 entrées (AER, PE, ALM, M20K, CDC, NVLink, UPI, HMB, MLA, CSA/HCA, DRVF, mode 0-4, k-WTA, PTQ, engram, hyper-connexion, seuil_push, KvCache::assurer, toutes les `DRAVE_*` et les familles de drapeaux, outils…) avec définition, usage et première occurrence `reports/fichier.md:ligne`. Absents vérifiés par grep : Sinkhorn, Hadamard, SwiGLU, LoRA, MTP, TLB, AVX2, HBM, MTok/s, p50/p95, « greffon ».
2. **B. Chiffres et affirmations mesurées** — ~230 mesures citées entre guillemets avec `fichier:ligne`, fichier par fichier.
3. **C. Contradictions / périmés / douteux** — ~85 entrées ; **D. Fichiers du dépôt cités** — ~80 chemins avec leur rôle.

Points saillants pour la détection de contradictions :
- **×2,17** revendiqué comme gain mesuré en `rapport-8bits.md:56` alors que `bilan-multi-materiel.md:92` le déclare **retiré** (inégalité de Kraft violée).
- **Croisement push/pull** : « ~10 % » (`rapport-analyse-flux.md:14`) contre « ~22 %, pas à 10 % » (`rapport-croisement-push-pull.md:43`) — contradiction interne au corpus.
- **« Le mode liste bat le dense »** : `bilan-multi-materiel.md:96,103` reproduit exactement l'affirmation que `rapport-croisement-push-pull.md:66-77` démontre fausse (15,8/14,7 contre 15,59/36,43 tok/s).
- **FPGA** : PCIe Gen3 ×8 6,5 Go/s (`bilan:8`) contre « USB seulement, 625 Mo/s » (`rapport-architecture-memoire.md:385`), qui se contredit aussi avec « Pas de FPGA dans cette machine » (`:246`).
- **KV à 1 M** : 82 Ko/82 Go (`rapport-architecture-memoire.md:418`) contre 90 Ko/96,6 Go (`:96`) dans le même document.
- **Cache KV** : 64 %/28 % (`rapport-attribution-kv.md:33-35`) contre 75 %/50 % dans REPRISE/roadmap (relevé par `rapport-coherence-docs-2.md:97`).
- **k = 32** : 23,3302 dans le tableau de `rapport-attention-creuse.md:27` contre 23,3279 aux lignes 95/126 et dans `rapport-campagne-parcimonie.md:36`.
- Chiffres manifestement faux et signalés comme tels : dispersion `1.8e17 évts/s` (`rapport-cpu-aer.md:17-18`), 5,3 G évts/s attribué à 16 puis 32 fils (`bilan:46` vs `:54`), « 8 % plus rapide » (`bilan:96`), 11 440 vs 11 901 lignes, en-tête 39/26/79 octets, 3 623/3 663, 1 589/1 629, 1 989/≈1 419.
- Les trois rapports de cohérence sont **datés** (`ae85043` 12:30 → `a383cd7` 15:11 → révision du 02/10) et se corrigent mutuellement : VERSION_FLUX 3→4→5, 13→48 tests, 11 440→11 901 lignes.

### 🤖 Assistant

⏵ Vérification directe des contradictions que je vais citer

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"=== A contexte-long 395-401 ===\"; sed -n '393,402p' docs/contexte-long.md; echo \"=== B prefill §7 ===\"; sed -n '419,428p' docs/plan-prefill-reparti.md; echo \"=== C lecteur-multifichiers mmap ===\"; sed -n '264,270p' reports/ … [264 caractères tronqués]`

  ```
=== A contexte-long 395-401 ===
19,3885.

Un mot sur ce qui n'était PAS la cause de l'écart avec llama.cpp : l'hypothèse
« llama.cpp calcule ses clés en f16 avant de les quantifier » a été testée
(`DRAVE_KV_F16=1`, arrondi à 10 bits de mantisse dans les boucles de
quantification) — **perplexité identique au chiffre près** (10,6231 avec et sans,
à 2 048 jetons). L'écart de +3,0 % contre +0,8 % à 8 192 vient donc d'ailleurs :
probablement la quantification des VALEURS et la précision du softmax, pas
l'arrondi des clés.

=== B prefill §7 ===
## 7. Ce que ce plan ne fait pas

* **Le lot en listes** : c'est le mode 4, à écrire quand le débit gênera. Corps
  prévu, un préfixe auto-délimité par état — `u32 a_j · u32 n_blocs_j ·
  n_blocs_j × f32 · u32 longueur_j · paires (écart u8, échappement 255 → u16,
  valeur i8)` — c'est-à-dire le corps du mode 2 répété `t` fois, avec le compte
  d'actifs en tête. Gain attendu : ÷2,3 sur le fil pour ~2,7e-2 d'écart
  (`reports/rapport-transport-liste.md`) ; le critère de la phase 3.4 (0,00e0)
  reste celui du mode 3 dense.
* **Le décodage par lots** : la génération reste séquentielle, un jeton par flux
=== C lecteur-multifichiers mmap ===
  contre 15
… [2278 caractères tronqués]
  ```

### 👤 Utilisateur

Agent 8549abcb-5d9a-4594-915b-5628c80a2a08 sent a message:
INVENTAIRE DRAVE — 20 rapports de reports/ — PARTIE 2/2 (sections C et D).

## C. Contradictions, chiffres périmés, affirmations douteuses
- `reports/rapport-optimisations-auto.md:38` — « le moteur prenait `cpu × 3/4` = **30** fils sur 40 threads logiques, il en prend **20** » — contredit `reports/rapport-optimisations.md:77` (« prend `3/4 × CPU` par défaut ») et `:124` (« la valeur par défaut est `3/4 × CPU` ») : politiques de threads par défaut incompatibles.
- `reports/rapport-optimisations.md:105` — « chuter le débit de 3,09 à 0,97 G év/s (8 threads) » et `:121` — « `yield_now()` ... a tout empiré (0,97 G à 8 threads) » — le même 0,97 G/8 threads est attribué à deux causes différentes (aliasing `&mut` au piège 2, `sched_yield` au piège 3) ; au moins une attribution est fausse.
- `reports/rapport-optimisations.md:86` — « La première campagne annonçait ... **Les deux chiffres étaient faux.** » (3838 vs 3513 ; 7,53 G év/s) — périmé par le texte.
- `reports/rapport-session-2026-09-30.md:92` — « gpt-oss ctx 256 = **15,1757** » — périmé : `reports/rapport-routage-experts.md:66` donne 15,1757 → **15,6017** et `:72` « **15,1757 était auto-cohérent, pas juste** » ; `reports/rapport-p0-flux.md:118` utilise 15,6017.
- `reports/rapport-session-2026-09-30.md:17` — « **Mode 4 — lot en listes** | **1,5 ko par jeton** ... écart 3,03e-2 » — contredit par le même document `:82-83` (« Mode 4 ... Spécifié, pas écrit ») et par `reports/rapport-prefill-reparti.md:107` (« décrit, non écrit »).
- `reports/rapport-session-2026-09-30.md:52` — « Mon premier « rejeu v3 = 19,3885 » était un faux positif — la trace n'était pas chargée du tout » ; `:53` — « le chiffre 19,3045 ... ne s'est pas reproduit : il vaut 19,5633 » — chiffres auto-déclarés faux/périmés.
- `reports/rapport-phase3-reparti.md:37` — « la classe ... que ce dépôt a déjà rencontré **cinq fois** » vs `reports/rapport-session-2026-09-30.md:43` — « **huit fois** » vs `:21` — « **46 sur 110** » : trois comptages incompatibles du même phénomène.
- `reports/rapport-optimisations-auto.md:134` — « **35 tests verts** » vs `reports/rapport-session-2026-09-30.md:93` — « `cargo test` **13/13** » (et `:60` « 17 au total ») : trois totaux de tests différents.
- `reports/rapport-p0-flux.md:63` — « | **total** | **58,2 G** | 100 % | » vs `reports/rapport-p0-flux.md:101` — « | total / token | 83 104,0 M | 81 115,9 M | » — deux totaux incompatibles pour GLM-5.3 dans le même rapport (l'attention passe de 21,9 G à 29,2 G sans réconciliation).
- `reports/rapport-p0-flux.md:120` — « GLM-5.3 exerce **les deux mêmes chemins** (MLA à rang faible + experts IQ), c'est donc lui qui porte la preuve aujourd'hui » vs `reports/rapport-routage-experts.md:92` (« GLM-5.3 | 754 G | MLA à rang faible, hyper-connexions, attention par index ») et `:99` (« aucun de ces cinq modèles n'a jamais été exécuté par ce moteur ») : GLM-5.3 ne peut pas porter une mesure de forward et être refusé faute de MLA à rang faible.
- `reports/rapport-p0-flux.md:120` — « le forward de V4-Flash est refusé (hyper-connexions, sortie à rang faible) » vs `reports/rapport-v4-couches-0-1.md:3` — « les deux premières couches de **DeepSeek-V4-Flash** tournent dans Drave » : formulation globale périmée (seules les couches compressées manquent).
- `reports/rapport-routage-experts.md:161` — « La référence externe (llama.cpp) sur gpt-oss aux mêmes jetons est **lancée** ; elle doit confirmer ou contredire 15,6017 » vs `:123-127` du même fichier qui donne déjà 166,85 / 15,6017 / 84,07 : §5 non mise à jour après la §4bis.
- `reports/rapport-routage-experts.md:68` — « Le changement de gpt-oss est le seul effet visible sur les portes » vs `:75` — « a d'abord déplacé la porte Qwen3-30B de 799,8557 à 799,8152 » : « inchangée, au bit près » masque un aller-retour.
- `reports/rapport-passage-a-l-echelle.md:19` — « Le moteur ne lit que `F32`, `F16`, `Q8_0` et `Q4_0`. **Aucun modèle récent ne s'ouvre aujourd'hui** » — contredit dans le même fichier par `:89-96` (« MXFP4 : fait, et vérifié sur le vrai fichier ») et par `reports/rapport-travail-reel.md:43-44` (« Q4_K / Q6_K / Q8_0 / Q4_0 / MXFP4 ✅ », « Lecture en place, zéro copie ... ✅ ») : état périmé.
- `reports/rapport-passage-a-l-echelle.md:79` — « Les 8 magnitudes valent `{0,1,2,3,4,6,8,12}` — donc, multipliées par 2, des **entiers** qui tiennent sur 4 bits » — incohérent avec `:91` (« `{0, ½, 1, 1½, 2, 3, 4, 6}` : doublées → `{0,1,2,3,4,6,8,12}` ») ; la première version est arithmétiquement fausse.
- `reports/rapport-passage-a-l-echelle.md:47` — « contre **41,6 tok/s mesurés** » (Qwen2.5-0.5B) vs `reports/rapport-travail-reel.md:48` — « 0,5 B : **32 tok/s** » : deux débits mesurés différents, même modèle.
- `reports/rapport-passage-a-l-echelle.md:60` — « | **Qwen3-30B-A3B** (MoE) | 3,3 G | 1,7 Go | 87 ms | **11,5** | » vs `reports/rapport-travail-reel.md:48` — « 30 B MoE : **5,6** » (et 7 B : 5,4 prédit vs 2,8 mesuré) : le modèle de coût prédit ~2× le débit réel des gros modèles, sans réserve du rapport.
- `reports/rapport-programme-evolutif.md:102` — « Le moteur lit 706 Mo/token à **10,4 Go/s** alors que la machine en offre **28,7** » vs `reports/rapport-passage-a-l-echelle.md:43` (« **20–25 Go/s** ») et `reports/rapport-optimisations-auto.md:70` (« 22,5 pour la RAM ») : débit atteint incohérent d'un facteur ~2.
- `reports/rapport-optimisations-auto.md:46` vs `:48` — table 16 lecteurs = « **31,08** » Go/s, vérification « 3,42 / 21,02 / **33,19** », conclusion `:49` « **31** contre 22 Go/s » : trois valeurs pour la même mesure, nombre de lecteurs des 3 chiffres vérifiés non précisé.
- `reports/rapport-optimisations-auto.md:44-49` — « Lecteurs disque = **16** » vs `reports/rapport-tete-garantie.md:102` — « **Les lecteurs parallèles n'apportent rien, et coûtent un peu** » (×0,78 et ×0,88) : conclusions opposées (lectures explicites vs défauts de page, distinguées seulement après coup).
- `reports/rapport-optimisations-auto.md:56` — « **90 Ko par jeton en F16**, soit **96,6 Go à 1 M** » — arithmétique incohérente : 90 Ko × 1 M = 90 Go (×1 048 576 = 94,4 Go) ; 96,6 Go correspondrait à ~92 Ko/jeton.
- `reports/rapport-optimisations-auto.md:95` — « V4.1 (**365 Go** pour 115 Go de RAM) » vs `reports/rapport-routage-experts.md:39` — « ce modèle de **341 Go** » (et `:93` « 755 G ») : deux tailles de fichier incompatibles pour le même modèle.
- `reports/rapport-placement-bits-kv.md:118` — « (la ligne GPU du banc ne vaut PAS pour le moteur : `--banc-kv` installe le miroir sans appliquer la règle d'homogénéité — relevé par un relecteur) » — mesure auto-déclarée invalide pour le moteur.
- `reports/rapport-placement-bits-kv.md:157` — « l'int8 complet coûte +2,25 % de perplexité **à ce contexte** » — le +2,25 % est mesuré à 4 096 (`:89`), alors que « ce contexte » désigne l'aiguille à 2 048 (`:148`) : attribution douteuse.
- `reports/rapport-precision.md:12` — « bitmap (1 bit/poids) + k bits par non-nul = **1 + k·d** bits/poids » vs `:22-31` — les b/poids de la table utilisent la densité **réelle** (« creux 1 bits d=0.125 » → 8.4 % → 1.08 ; « d=0.500 » → 26.6 % → 1.27), pas le `d` nominal ; deux lignes de même `d` nominal ont des densités différentes (8,4 % et 11,8 % pour d=0.125).
- `reports/rapport-prefill-par-lots.md:52` — « | 1 | **16,6 s** | » vs `:193` — « | Qwen2.5-0.5B Q8_0, `--dense`, 16 fils | 512 | **17,1 s** | » : deux temps pour le même lot 1.
- `reports/rapport-prefill-par-lots.md:89` — « (145 Mo lus par jeton) » + `:95` « traiter la tête comme un GEMM » — explicitement réfuté par `:131-136` : « **La tête en lot ne gagne rien** ... L'argument de la §4 — « 145 Mo lus par jeton » — est un argument de *bande* *passante*, et il ne s'applique pas » : conclusion §4 périmée.
- `reports/rapport-prefill-reparti.md:62` — « Chaque aller-retour coûte **~4 × 20 ms** de latence pure » vs `reports/rapport-transport-liste.md:217` — « **3,2 ×** (latence par message) » ; `reports/rapport-transport-liste.md:220-221` décrit 4 messages pour justifier 3,2.
- `reports/rapport-session-2026-09-30.md:14` — « dense 3 663 octets → **1 629** par flux (÷2,3) » vs `reports/rapport-transport-liste.md:152` — « | **1 024** | **1,32e-2** | **1 589** | » et `:178` — « **1 568** » : trois octets/flux différents, correspondance non donnée.
- `reports/rapport-transport-liste.md:10` — « (39 octets à l'époque de ces mesures, **79** depuis que les top-k voyagent) » — toutes les valeurs en octets (3 623 ; 897 ; 1 568 ; 2 793...) sont périmées de 40 octets et non recalculées.
- `reports/rapport-transport-liste.md:29` — « | listes 0,10 | 36,5 % (327) | 1 347 | **216** | 35 483,0643 | 66 813,6606 | 8,8e-1 | » — activité qui remonte (24,0 % au seuil 0,05 → 36,5 %) et retour 216 < aller 1 347 : anomalie reconnue (`:43` « n'est donc pas comparable ») mais laissée dans la courbe.
- `reports/rapport-transport-liste.md:88` — « cette build parle la **5** » vs le titre du même ajout « **Version dans chaque en-tête** (3.5) » vs `reports/rapport-session-2026-09-30.md:37` — « `VERSION_FLUX` restée à **3** » : numérotation 3 / 3.5 / 5 incohérente.
- `reports/rapport-tete-restreinte.md:32` — « Un vocabulaire de **16 384** tokens contient donc **100 %** des vrais jetons d'un corpus français » — contredit par `:19` : **19 793** identifiants distincts observés (13,03 % d'un vocabulaire de 151 936) ne tiennent pas dans 16 384 ; l'affirmation ne vaut que pour le rang argmax (max 4 319).
- `reports/rapport-valeur-unaire.md:49` — « **Le ×2,17 annoncé ci-dessous est FAUX** » vs `:83` — « **1.85 b/poids, soit ×2.17** » ; et `:30` (hybride = **1.12** b/poids, 1.12 op) vs `:83` (**1.85** b/poids, 0.98 op) : tableau et verdict incompatibles pour la même stratégie.
- `reports/rapport-travail-reel.md:85` — « notre **perplexité de 39,8** sur du wikitext brut là où l'on attendrait de l'ordre de 6 » vs `reports/rapport-routage-experts.md:126` — « drave, YaRN à retardement (le défaut) | **15,6017** » et `:125` — llama.cpp 166,85 : trois régimes gpt-oss non réconciliés (le rapport dit lui-même que 39,8 reste inexpliqué).
- `reports/rapport-v4-couches-0-1.md:93` — « il remplace celui qui circulait (**11,737136 / 125 133**), mesuré sur un autre découpage » — chiffre explicitement périmé.
- `reports/rapport-session-2026-09-30.md:20` — « perplexité ~20 au lieu de **17 869** » — ancien chiffre du banc Colab périmé (confirmé `:63`).
- `reports/rapport-p0-flux.md:48` — « 313,7 M (FFN) + 136,1 M (tête) = **449,8 M** ✅ » — l'addition donne 449,9 M (313,79 + 136,13) : écart d'arrondi présenté comme validation.
- `reports/rapport-programme-evolutif.md:27` — « l'inférence occupe **16 threads** sur 40 » vs `reports/rapport-optimisations-auto.md:38` — « il en prend **20** » : threads par défaut différents.
- `reports/rapport-routage-experts.md:143` — « La comparaison à 510 jetons est lancée pour confirmer » puis `:161` — « est **lancée** » : double annonce de lancement pour une mesure déjà présentée en §4bis, signe de sections non relues.

## D. Fichiers du dépôt cités
- Les 20 rapports eux-mêmes, cités entre eux (`rapport-tete-restreinte.md`, `rapport-transport-liste.md`, `rapport-placement-bits-kv.md`, `rapport-phase3-reparti.md`, `rapport-prefill-reparti.md`...).
- `reports/rapport-cpu-aer.md` — « ni tri, ni dédoublonnage », ordre naturel des écarts ; `reports/rapport-optimisations.md:159`.
- `reports/rapport-8bits.md` — niveaux quantifiés, cas où la répétition d'adresse est optimale ; `reports/rapport-valeur-unaire.md:62`.
- `reports/rapport-compacite-trace.md` — format de trace v2/v3 (132 396 736 → 66 370 408 → 45 079 930) ; `reports/rapport-session-2026-09-30.md:16`.
- `reports/rapport-mode4-lot-listes.md` — mode 4 (lot en listes), 1,5 ko/jeton, 3,03e-2 ; `reports/rapport-session-2026-09-30.md:17`.
- `reports/rapport-drapeaux-ignores.md` — 46 drapeaux/110 ignorés, `--options-actives` ; `reports/rapport-session-2026-09-30.md:21`.
- `reports/rapport-coherence-docs.md` — 80 affirmations, 38 périmées, 15 contradictoires ; `reports/rapport-session-2026-09-30.md:22`.
- `format-flux.md` — spécification du protocole v5 (cinq modes, 14 champs) ; `reports/rapport-session-2026-09-30.md:18`.
- `plan-gpu-topk.md` — plan chiffré du noyau GPU de top-k (968 ms/couche à 1 M vs 13,2 ms) ; `reports/rapport-session-2026-09-30.md:19`.
- `docs/contexte-long.md` — coût du préremplissage séquentiel (4,5 h à 32 k, 1 234 h à 1 M) ; `reports/rapport-prefill-par-lots.md:4`.
- `REPRISE.md` — blocage de 27 minutes (worker mort) ; `reports/rapport-prefill-par-lots.md:168`.
- `colab/README.md` — kit Colab (dépôt 4,5 Mo, notebook, tunnels) ; `reports/rapport-session-2026-09-30.md:20`.
- `drave-core/` — moteur Rust `std` seul, zéro dépendance, 386 lignes ; `reports/rapport-optimisations.md:3`.
- `drave-core/src/model.rs` — `router`, `logits_garanti`, `Model::load`, `load_partiel`, `verifier_architecture`, `forward`, `forward_lot`, `forward_mla`, `attn_mla`, `logits`, `logits_lot`, `emb_imposee(_lot)` ; `reports/rapport-routage-experts.md:43`, `reports/rapport-tete-garantie.md:14`, `reports/rapport-tete-restreinte.md:116`, `reports/rapport-v4-couches-0-1.md:23`.
- `drave-core/src/engine.rs` — pool, `Pool::gemm_dense_i8`, `gemm_dense_q4`, `Shared::gs32`, `Shared::morts`, `Pool::attendre`, `catch_unwind` ; panique `src/engine.rs:473:77` ; `reports/rapport-prefill-par-lots.md:12`, `:152`, `:170`, `:178`.
- `drave-core/target/release/drave` — binaire de tous les bancs (`--ppl`, `--matrix`, `--lot`, `--q4`, `--hebbian`, `--banc-kv`...) ; `reports/rapport-placement-bits-kv.md:170`, `reports/rapport-passage-a-l-echelle.md:213`.
- `tools/aiguille.py` — Aiguille v2 (9/9 sondes) ; `reports/rapport-placement-bits-kv.md:148`.
- `tools/portes.sh` — exécute les portes de non-régression (dont gpt-oss 15,6017) ; `reports/rapport-p0-flux.md:118`.
- `tools/ref_logits.cpp` (`ref_logits`, `--tensors`, `REF_DUMP`) — référence llama.cpp, mêmes tenseurs nommés en f32 ; `reports/rapport-routage-experts.md:107`, `reports/rapport-p0-flux.md:119`, `reports/rapport-v4-couches-0-1.md:25`.
- `tools/compare_etats.py` — compare les vecteurs Drave/llama.cpp (écart max, dynamique, corrélation) ; `reports/rapport-v4-couches-0-1.md:26`.
- `tools/proxy_latence.py` — relais ajoutant un délai par message (20 ms) ; `reports/rapport-transport-liste.md:204`, `reports/rapport-prefill-reparti.md:53`.
- `tools/pair_factice.py` — faux pair parlant le protocole et disant ce qu'il reçoit ; `reports/rapport-transport-liste.md:93`.
- `tools/mla_synthetique.py` — modèle MLA jouet pour `forward_mla` ; `reports/rapport-routage-experts.md:169`.
- `tools/mesurer_lecture_experts.py` — rejoue la mesure de lecture d'experts (froid forcé, 120 blocs de 4 Mo) ; `reports/rapport-tete-garantie.md:114`.
- `tools/lire_meta_gguf.py --tenseur` — lit métadonnées/tenseurs GGUF hors moteur ; `reports/rapport-v4-hca.md:92`.
- `tools/colab_cote_local.sh` — script Colab côté local ; `reports/rapport-session-2026-09-30.md:62`.
- `run_precision.py` — génère `rapport-precision.md` ; `reports/rapport-precision.md:80`.
- `run_value_encoding.py` — génère `rapport-valeur-unaire.md` ; `reports/rapport-valeur-unaire.md:104`.
- module `gguf` : `gguf::q8_dot_at` — noyau Q8_0 de la tête, lié au calcul ; `reports/rapport-prefill-par-lots.md:133`.
- Modèles : `models/Qwen2.5-0.5B-Q8_0.gguf`, `../models/Qwen2.5-0.5B-Q8_0.gguf`, `models/Qwen2.5-0.5B-Q4_0.gguf`, `gpt-oss-120b-MXFP4.gguf`, Qwen2.5-1.5B-Instruct Q4_K_M, Qwen3-30B-A3B Q4_K_M ; `reports/rapport-phase3-reparti.md:15`, `reports/rapport-passage-a-l-echelle.md:98`, `reports/rapport-placement-bits-kv.md:148`.
- Tenseurs cités : `blk.0.ffn_gate.weight`, `blk.0.ffn_down_exps.weight` (2880,2880,128, type 39), `ffn_gate_tid2eid.weight` ([129 280 × 6], I32), `attn_k_b [64,512,192]`, `attn_v_b [64,256,512]` ; `reports/rapport-optimisations.md:4`, `reports/rapport-passage-a-l-echelle.md:101`, `reports/rapport-routage-experts.md:32`, `reports/rapport-p0-flux.md:91`.
- Fichiers temporaires (hors dépôt) : `/tmp/wt2_a.txt`, `/tmp/wt2_ids.txt`, `/tmp/ids_qwen_long.txt`, `/tmp/act_log.bin`, `/tmp/loss_log.bin`.
- Référence externe (hors dépôt) : `llama.cpp/src/llama-graph.cpp` (`build_moe_ffn`, `selection_probs`, `ggml_soft_max_ext`, `ggml_soft_max_add_sinks`, `ggml_rope_ext_back`, `dsv4_append_zero_row`, `lid_score_masked`) ; `reports/rapport-v4-hca.md:129`, `reports/rapport-routage-experts.md:69`.

FIN. Aucun fichier du dépôt n'a été modifié (lecture + greps uniquement).

### 🤖 Assistant

⏵ Rédaction de docs/glossaire.md — première partie (mode d'emploi, parcours, projet)

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "content": "# Glossaire raisonné de Drave\n\nCe document explique **tout le vocabulaire** employé dans `docs/` (18 documents) et\n`reports/` (60 rapports, plus 9 fichiers dans `sprints/`), pour quelqu'un qui ne\nconna … [32761 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 👤 Utilisateur

Background subagent 8549abcb-5d9a-4594-915b-5628c80a2a08 finished and will do no further work unless you send it more.
Its closing message:
⏵ Inventory complete and delivered to the parent agent

The exhaustive inventory of the 20 reports is complete (no repo file modified — reads and greps only), and both halves were sent to `3d5618a0-4e3a-45bb-943d-a72c753fb7da`:

- **Partie 1/2** — `## A. Termes et sigles` (~130 entrées, chacune avec définition, usage/outil, première occurrence `reports/fichier.md:ligne`) et `## B. Chiffres et affirmations mesurées` (une ligne par mesure, citation exacte, ~280 entrées).
- **Partie 2/2** — `## C. Contradictions, chiffres périmés, affirmations douteuses` (35 entrées) et `## D. Fichiers du dépôt cités` (~35 chemins + tenseurs GGUF + fichiers temporaires + référence externe llama.cpp).

Points saillants remontés au parent :

1. **Faux départs auto-signalés** : `19,3045 → 19,5633`, « rejeu v3 = 19,3885 » faux positif, chiffres périmés `11,737136 / 125 133` (remplacés par 11,077944 / 64 727,68), `×2,17` de l'unaires déclaré FAUX mais réaffirmé.
2. **Contradictions inter-rapports** : porte gpt-oss 15,1757 vs 15,6017 ; V4.1 = 341 Go vs 365 Go ; débit atteint 10,4 vs 20–25 Go/s ; Qwen 0.5B 32 vs 41,6 tok/s ; prédictions tok/s ~2× les mesures ; GLM-5.3 « exécuté » (p0-flux) vs « jamais exécuté, MLA à rang faible manquante » (routage-experts) ; mode 4 livré vs « spécifié, pas écrit » ; « cinq fois » vs « huit fois » vs « 46 sur 110 » ; 13/13 vs 35 tests.
3. **Incohérences internes** : totaux GLM-5.3 58,2 G vs 83,1 G dans le même rapport ; défaut de threads `3/4 × CPU` vs cœurs physiques ; 0,97 G év/s attribué à deux causes ; E2M1 `{0,1,2,3,4,6,8,12}` vs `{0,½,1,1½,2,3,4,6}` ; 90 Ko/jeton ≠ 96,6 Go à 1 M ; 1 629 vs 1 589 vs 1 568 octets/flux ; vocabulaire 16 384 ne pouvant contenir 19 793 identifiants distincts.
4. **Termes attendus mais absents** des 20 fichiers : DRVF/DRVF v5, PTX, RSS, IQ2_XXS, HBM, M20K, greffon, liste valuée, shard, p50/p95, MTok/s, Gbit/s, bf16, Hadamard, LoRA, MTP.

### 🤖 Assistant

⏵ Rédaction de la partie 2 : formats/quantification et le moteur Drave

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "old_string": "<!-- À SUIVRE -->", "new_string": "---\n\n## 3. Formats, quantification, encodage\n\n**b/poids (bits par poids)** — Nombre moyen de bits nécessaires pour stocker un\npoids. Un modèle 8 bits coûte 8 b/po … [25599 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Rédaction de la partie 3 : flux/transport et matériel

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "new_string": "---\n\n## 5. Flux, protocole et transport\n\n**Contrat d'activation (`Act`)** — L'ensemble des réglages qui changent les\nchiffres calculés : niveaux de quantification, seuil, top-k, renormalisation, et … [19250 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Rédaction de la partie 4 : mesure et méthode, points relevés, sources

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "new_string": "---\n\n## 7. Mesure, qualité et méthode expérimentale\n\n**Amplification chaotique** — Explication d'un écart de continuation entre deux\nchemins de calcul pourtant à perplexité identique : une différen … [21870 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Vérification des derniers liens et relecture du document

- **bash** `{"command": "for u in \"https://arxiv.org/abs/1706.03762\" \"https://arxiv.org/abs/1502.03167\" \"https://arxiv.org/abs/1607.06450\" \"https://arxiv.org/abs/1805.04833\" \"https://arxiv.org/abs/2402.17764\" \"https://www.deeplearningbook.org/contents/ml.html\" \"https://www.deeplearningbook.org/cont … [435 caractères tronqués]`

  ```
200  https://arxiv.org/abs/1706.03762
200  https://arxiv.org/abs/1502.03167
200  https://arxiv.org/abs/1607.06450
200  https://arxiv.org/abs/1805.04833
200  https://arxiv.org/abs/2402.17764
200  https://www.deeplearningbook.org/contents/ml.html
200  https://www.deeplearningbook.org/contents/mlp.html
200  https://aclanthology.org/J92-1002/
200  https://colab.research.google.com/
200  https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
200  https://arxiv.org/abs/2502.13923
200  https://arxiv.org/abs/1702.03118
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; wc -l docs/glossaire.md; grep -n \"SUIVRE\" docs/glossaire.md; grep -n \"Verilog/Synthèse\\|documentations Intel\\|du dépôt.**\" docs/glossaire.md", "description": "Check glossary size and typos"}`

  ```
1576 docs/glossaire.md
7:chaque définition renvoie au fichier du dépôt qui l'emploie.
16:> trois phrases, sans prérequis. **Où** : fichier ou outil du dépôt qui l'emploie,
22:- `chemin:ligne` renvoie à un fichier **du dépôt**, à la ligne indiquée. Exemple :
26:  auteurs, sans lien** — c'est une règle du dépôt, on n'invente pas d'URL.
51:projet n'est pas, et le nom. Tout le reste du dépôt en découle.
138:**Fait · mesuré · projeté · déduit** — Étiquettes de confiance du dépôt. *Mesuré* :
162:modification ne doit pas dégrader. Les portes du dépôt sont : Qwen2.5-0.5B à
369:mais beaucoup moins bien au milieu. Le test de l'aiguille du dépôt retrouve
515:dans trois usages distincts du dépôt : les **experts** (routeur MoE), l'**attention**
525:V4.1). Le vocabulaire du dépôt compte tout en « couches × cachés × jetons »
614:nibbles empaquetés), 256 pour int8. Le vocabulaire du dépôt les distingue de
672:questions du dépôt sont : *combien de bits* et *où sont les échelles* ; la seconde
751:`drave-core/`. Tous les bancs, mesures et bancs d'essai du dépôt l'appellent :
878:| `tools/portes.sh` | portes de non-régression du dépôt | `docs/sprints.md:40` |
941:**DRVF (Drave Flux)** — Le format bina
… [431 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; grep -n \"18 documents de \\`docs/\\`\" docs/glossaire.md; echo \"---\"; sed -n '1108,1132p' docs/glossaire.md", "description": "Inspect lines to fix"}`

  ```
1256:`reports/rapport-coherence-vision.md` (les 18 documents de `docs/`).**
---
dans la multiplication, très coûteux en surface. Le projet s'en passe comme d'un
principe (« 0 DSP ») : ses multiplications ternaires deviennent des additions et
des décalages, et le PE synthétisé tient en 176 ALM sans DSP
(`docs/histoire.md:11`, `docs/programme-recherche.md:58`, `reports/rapport-encodage.md:74`).

**Énergie par événement (nJ, pJ, TDP)** — Coût énergétique d'un événement traité :
57 nJ mesurés sur CPU, 8,3 nJ **projetés** sur FPGA (limite DDR3), ~12,7 nJ déduits
pour le GPU ; la comparaison neuromorphique cite E_AC = 0,9 pJ contre E_MAC = 4,5 pJ
sur du 45 nm (`reports/bilan-multi-materiel.md:46-48`,
`docs/comparaison-spiking.md:63`). Le *TDP* (thermal design power) est la puissance
nominale utilisée pour convertir un temps de calcul en énergie.

**FPGA (Field-Programmable Gate Array) · Stratix V · Quartus · iverilog · RTL** —
Un FPGA est un circuit dont on peut reconfigurer le câblage logique ; le projet vise
une carte Intel (Altera) **Stratix V GS « Storey Peak »**. *RTL* désigne le code
Verilog/Synthèse au niveau transfert de registres ; *iverilog* est le simulateur
libre utilisé pour
… [617 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "old_string": "`reports/rapport-coherence-vision.md` (les 18 documents de `docs/`).**\n**Où** : à lire avant de citer un chiffre ancien.", "new_string": "`reports/rapport-coherence-vision.md` (les 18 documents de `doc … [58 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "old_string": "une carte Intel (Altera) **Stratix V GS « Storey Peak »**. *RTL* désigne le code\nVerilog/Synthèse au niveau transfert de registres ; *iverilog* est le simulateur\nlibre utilisé pour vérifier, *Quartus  … [365 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Vérifications finales dans le code (noms de structures et drapeaux)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src; echo \"=== ChargeFlux ===\"; grep -n \"enum ChargeFlux\" -A 12 main.rs; echo \"=== PLAFOND ===\"; grep -n \"PLAFOND\" main.rs | head -5; echo \"=== options ===\"; grep -n \"options-strict\\|options-actives\" main.rs | he … [123 caractères tronqués]`

  ```
=== ChargeFlux ===
2016:enum ChargeFlux {
2017-    Dense(Vec<f32>),
2018-    Liste { idx: Vec<u16>, val: Vec<i16>, echelle: f32 },
2019-    Blocs { idx: Vec<u16>, val: Vec<i8>, echelles: Vec<f32> },
2020-    /// Lot d'états, aplati (`t × hidden`).
2021-    Lot(Vec<f32>),
2022-}
2023-
2024-impl ChargeFlux {
2025-    /// Rend le vecteur dense : la déquantification a besoin de la dimension, que
2026-    /// seul le modèle connaît.
2027-    fn en_dense(&self, hidden: usize) -> Vec<f32> {
2028-        match self {
=== PLAFOND ===
2002:const PLAFOND_FLUX: usize = 256 << 20;
2006:    if octets > PLAFOND_FLUX {
2008:            format!("{quoi} : {octets} octets au-delà du plafond de {} Mo — flux refusé                      (règle R4 de docs/plan-prefill-reparti.md)", PLAFOND_FLUX >> 20)));
2141:    if n.saturating_mul(2) > PLAFOND_FLUX {
2143:                           PLAFOND_FLUX >> 20));
=== options ===
393:/// **Tableau de bord des réglages en vigueur** (`--options-actives`), lus sur le
490:    /// `--options-actives` : imprime, APRÈS toutes les affectations, les réglages
499:    /// `--options-strict` : un drapeau inconnu n'est plus un avertissement mais une
618:            "--options
… [663 caractères tronqués]
  ```

### 👤 Utilisateur

Agent f2de810a-b765-444d-b3cc-d8fce1ba2105 sent a message:
LIVRABLE — dépouillement exhaustif (9 sprints lus intégralement ; 24 outils Python + 8 scripts shell ; CLI/champs de drave-core/src/*.rs). Aucun fichier modifié.

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
- **MXFP4** — Virgule flottante 4 bits à échelle microscopique : bloc de 17 octets = exposant E8M0 + 16 octets de nibbles E2M1, bloc de 32 poids ; `gguf.rs:261,1065-1089`, `list.rs:547` (`LUT_MXFP4`), `tools/pair_factice.py` non — `docs/glossaire.md:635` ; quantification.
- **E2M1 / E8M0** — Composants de MXFP4 : valeur 4 bits (table `KV` à 16 niveaux) et échelle d'exposant ; `gguf.rs:1068,1079-1089` (`echelle_e8m0`), `gpu.rs` noyaux `proj_mxfp4_warp` ; quantification.
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
- **top-k** — Sélection des k plus grandes valeurs ; décliné en `--attn-topk`, `--qk-topk`, `--moe-topk`, `--topk-q/-k/-v/-o/-gate/-up/-down`, `--topk`, `--act-topk` ; `main.rs:647,662-663,658,668-675`, `docs/glossaire.md:514` ; drapeau/terme.
- **attention creuse** — Attention restreinte aux k meilleures clés par requête ; `sprints/03:56-68`, `model.rs` top-k ; concept.
- **k-WTA (k-Winners Take All)** — Parcimonie par sélection des k plus fortes activations ; `main.rs:668` (`--act-topk`), `docs/glossaire.md:339` ; concept.
- **perplexité (PPL)** — Exponentielle de la NLL moyenne par jeton ; mesure de référence de toutes les portes (`tools/portes.sh:53,60,121`), `main.rs:4277` (`run_ppl`) ; métrique.
- **NLL** — Log-vraisemblance négative par position ; `tools/compare_logits.py:34-40,93-99`, `main.rs:2595` (`nll_logits`) ; métrique.
- **RoPE** — Plongement positionnel rotatif (rotation par paires), y compris rotation inverse pour V4 ; `model.rs:3909-3912` (`rope_inverse`), `main.rs` ; architecture.
- **YaRN / mscale / rampe** — Extension de contexte par interpolation NTK avec facteur, betas et rampe ; `DRAVE_YARN`, `DRAVE_YARN_NON`, `DRAVE_YARN_MSCALE`, `DRAVE_YARN_RAMPE` (`model.rs:2565-2571,3799`), `main.rs:693` (`--sans-yarn`) ; architecture/drapeau.
- **RMSNorm** — Normalisation par la moyenne quadratique ; `model.rs:886-889` (par tête), `main.rs:2499` (`attention.layer_norm_rms_epsilon`) ; architecture.
- **SiLU / SwiGLU / GELU / sigmoïde rapide** — Non-linéarités du FFN : `x·σ(x)` ; `g·(u+1)·σ(1,702 g)` pour gpt-oss (clamp ±7) ; `model.rs:431-435`, `model.rs:3652-3653` (`LIMITE=7.0`, `ALPHA=1.702`), `model.rs:1977` (clamp SwiGLU V4) ; architecture.
- **routage / gating (Softmax, Sigmoid, SoftmaxPoids, SqrtSoftplus)** — Enum `Gating` à 4 conventions (Qwen3-MoE, Kimi/GLM, gpt-oss, DeepSeek V4) ; `model.rs:28-63`, `main.rs:96-99` (sortie `--config` : sigmoïde, racine de softplus, softmax) ; enum Rust.
- **tid2eid** — Table de routage par jeton `ffn_gate_tid2eid.weight` (I32, `GGML_I32=26`) ; `model.rs:856`, `gguf.rs:316-318` ; format.
- **LoRA (q_lora_rank / kv_lora_rank / o_lora)** — Projections de rang faible de la MLA (« descente » puis « montée ») ; `model.rs:1150-1163`, `tools/mla_synthetique.py:32-34` (`QL=32`, `KVL=48`), `docs/glossaire.md:359` ; architecture.
- **MTP (Multi-Token Prediction) et décodage spéculatif** — Prédiction de plusieurs jetons en avance (`dspark_*`, cibles 37-39) ; `docs/plan-deepseek41-complet.md:86`, `docs/glossaire.md:399` ; architecture (absent des 9 sprints).
- **« perdu au milieu » (lost in the middle)** — Échec de récupération d'une information située au milieu d'un long contexte ; `sprints/03:62-66`, `aiguille.py` ; phénomène.
- **aiguille (needle)** — Sonde qui plante un code (« AZUR-7391 ») à une profondeur donnée et le redemande ; `tools/aiguille.py:1-46,57-122` ; outil/protocole de mesure.
- **hyper-connexion / greffon / grappe** — voir plus haut ; **greffon** = neurone ajouté sans réentraînement, format `QPAT` ; `model.rs:2025-2037` (`Patch`), `main.rs:643` (`--patch`), `tools/make_patch.py`, `docs/glossaire.md:682,800` ; terme/fichier.

**Moteur, encodage, sparsité**
- **AER (Address Event Representation)** — Représentation par adresses d'événements : pousser des listes plutôt que multiplier des matrices ; `docs/histoire.md:12` (7,79 G événements/s), `docs/vision.md:34`, `docs/glossaire.md:736` ; concept fondateur.
- **événement** — Couple (écart d'indice, valeur) poussé vers une destination ; `docs/glossaire.md:773`, `engine.rs` ; unité de calcul.
- **liste d'activation / liste creuse / liste valuée** — Représentation creuse du vecteur d'activation ; `docs/glossaire.md:805`, `main.rs:2087-2118` ; structure.
- **push / pull / auto / `seuil_push`** — Exécution par dispersion d'événements / produit scalaire dense / choix automatique ; `main.rs:689-690` (`--auto`, `--push`), `model.rs:1845-1849` (`seuil_push`, croisement **22 %**), `tools/analyse_flux.py:8` ; stratégie.
- **SparseVec / PushMat / FusedSign / SignedDelta / BitmapSign / SparseK / DenseQ8 / DenseQ4** — Structures d'encodage creux/dense du moteur ; `list.rs:342,539-547,619`, `engine.rs:39-41` (`main.rs` imports) ; structures Rust.
- **densité** — Proportion d'activations non nulles ; `tools/analyse_flux.py:8` (~22 % = croisement push/pull), `main.rs:44-46` / `fmt_bits` ; mesure.
- **b/poids (bits par poids)** — Bits moyens par poids d'un encodage ; `main.rs:44-45` (`fmt_bits`), `docs/glossaire.md:541` ; métrique.
- **spiking / SNN / LIF** — Réseau à impulsions, neurone Leaky Integrate-and-Fire, comparaison avec l'événementiel ; `docs/comparaison-spiking.md:59-63,115`, `docs/glossaire.md:488` ; concept externe.
- **Sinkhorn** — cf. supra.
- **Hadamard** — Incohérence de Hadamard citée comme référence de QuIP# pour les i-quants ; `docs/glossaire.md:625` (seule occurrence du corpus) ; concept externe.
- **SWAR** — SIMD within a register (décodage d'octets en parallèle dans un u64) ; `main.rs:194`, `engine.rs:51` (`HIGH_BITS`), `docs/glossaire.md:847` ; technique.
- **AVX2** — Jeu d'instructions x86 utilisé par `q8_dot_avx2` et `dot16_q6_avx2` ; `gguf.rs:1603-1628`, `list.rs:823-824` ; matériel/code.
- **PTX** — Code noyau CUDA compilé depuis `gpu/drave_gpu.cu`, chargé par l'API pilote ; `gpu.rs:1-3,39-40`, `gpu.rs:231-329` (15 noms de noyaux) ; technique GPU.
- **VRAM** — Mémoire des cartes ; `gpu.rs:179` (`memoire_libre`), `materiel.rs:383` (`VRAM=84.9` Go/s) ; matériel.
- **NUMA** — Nœud mémoire/CPU ; `materiel.rs:24,118,198,238`, `engine.rs:274,332` (épinglage au premier nœud) ; matériel.
- **PCIe / NVLink** — Bus hôte↔GPU (6,5 Go/s) et lien direct (25,78 Go/s) ; `gpu.rs:7`, `materiel.rs:52,339`, `main.rs:4034,4105` ; matériel.
- **DDR3 / FPGA / DSP / ALM / M20K** — Ressources du prototype matériel : mémoire DDR3 9,66 Go/s, PE sans multiplieur (176 ALMs, 0 DSP), bancs M20K ; `docs/convertisseur.md:85-93`, `main.rs:378`, `reports/bilan-multi-materiel.md:66-67`, `reports/rapport-cpu-aer.md:11`, `tools/session_report.py:46` ; matériel.
- **mmap / MADV_WILLNEED** — Fichiers mappés en mémoire (défaut, `DRAVE_MMAP=0` force la lecture) et conseil de prélecture ; `gguf.rs:45-53,103-128,155-177`, `main.rs:64` ; technique/fichier.
- **RSS** — Mémoire résidente ; `sprints/08:146`, `main.rs:1649` (`VmRSS`/`VmSize` dans `--sonder-engram`) ; métrique.
- **TLB** — Cache de traduction d'adresses, invoqué pour le coût d'un accès aléatoire ; `main.rs:4040`, `docs/convertisseur.md:247` ; matériel.
- **zstd** — Compresseur sans perte (traces DSH `.zstd`, variante `--zstd-v2` de trace_compacite) ; `tools/archive_sessions.py:40-42`, `tools/session_report.py:55-61`, `tools/trace_compacite.py:295-296` ; outil/format.
- **débit / bande passante / latence** — Débits mesurés (CPU 14–25 Go/s, PCIe 6,5, NVLink 25,78, VRAM ~750, RAM ~20, NVMe 5,5 aléatoire) et latence comme facteur décisif en réparti ; `main.rs:3981,4034,4105`, `sprints/09:57-66`, `tools/proxy_latence.py:1-10` ; métrique.
- **porte / porte de correction / porte Drave** — Seuil chiffré de non-régression (portes du dépôt) ; comparaison à une référence externe (llama.cpp) vs épreuve propre au projet ; `tools/portes.sh:2-9`, `tools/portes_formats.sh:2`, `docs/plan-deepseek41-complet.md:9,136`, `docs/glossaire.md:168-183` ; terme de méthode.
- **boxing** — Règle de sprint : 2 h chronométrées (SCRUM_DUREE) ; `tools/sprint.sh:1-15` ; terme de méthode.
- **verdict négatif / refus bruyant** — Piste fermée consignée, ou drapeau refusé au lieu d'être ignoré en silence ; `sprints/01:116-118`, `sprints/02:133`, `main.rs:618-619,714-737` ; principe.
- **drapeau inconnu / `--options-strict` / `--options-actives`** — Les drapeaux non reconnus sont retenus et affichés, ou fatals (exit 2) ; le tableau de bord des options réellement appliquées ; `main.rs:494-501,618-619,714-741` ; drapeau.

## B. Drapeaux CLI et variables d'environnement

**B.1 — Binaire `drave` (analyse manuelle unique, `drave-core/src/main.rs:580-742` ; aucun clap, aucun `--help`/`-h`/`--version` ; `argv[1]` = modèle ; aide = `main.rs:51-64`). 93 drapeaux reconnus.**
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
- `--limit N` — main.rs:654 — plafond (jetons en perplexité, lignes en --gpu-banc).
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
- `--sonder-engram N` — main.rs:697 — sonde mmap de l'engram (défaut 1000 si absent/`=N`).
- `--bloc TENSEUR:INDEX` — main.rs:698 — déquantifie un bloc (garde `i+1<len`).
- `--tete-garantie F` — main.rs:699-700 — restriction de tête prouvée exacte.
- `--tete-restreinte F` — main.rs:701-702 — restriction (génération seule).
- `--profil-neurones` — main.rs:703 — profilage PowerInfer.
- `--harmony` / `--harmony-assistant` / `--harmony-user` / `--harmony-suite` — main.rs:704-707 — modes de fenêtrage harmony.
- `--q4` (`|=3`) / `--q4-ffn` (`|1`) / `--q4-attn` (`|2`) / `--q4-tout` (`|=7`) — main.rs:708-711 — masque q4.
- Défauts par mode : inférence ctx 512/abits 8 (775-777) ; perplexité 256/16 (4303-4305) ; flux-serveur 4096 (2480) ; ppl-reparti 256 + couches_locales 12 (2606-2608) ; banc-mla 4096 figé (3449) ; banc-kv KV bits 32 (3492) ; banc-topk bits 8 (2872).
- Priorité des modes (main.rs:91-121) : materiel > config > sonder-engram > bloc > banc-vision > flux-serveur > ppl-reparti > tensors > banc-mla > banc-kv > banc-topk > gpu-banc > plan > tokenize > ppl > infer ; plusieurs modes ⇒ avertissement `[modes]` (102-105, `--bloc` absent de la liste).
- Chemin historique sans mode : `--matrix`, `--threads` seulement (main.rs:137-146).

**B.2 — Outils Python (24 scripts)**
- `aiguille.py <modele> <longueurs> <profondeurs>` — positionals l.127-129 ; `--n` (40) l.130 ; `--threads` (16) l.131 ; `--lot` (256) l.132 ; `--timeout` (7200) l.133 ; `--gpu` l.134 ; `--gpu-kv` l.135 ; `--attn-topk` (0) l.140-141 ; `--gpu-topk` l.142-143 (exige `--attn-topk`, l.149-150) ; `--journal` l.144 ; pose `DRAVE_GPU`, `DRAVE_GPU_KV`, `DRAVE_GPU_TOPK` (l.74-82).
- `analyse_empreinte.py <trace>` — `--limite N` l.71-72 ; `--modele {deepseek4,deepseek41,qwen3moe}` l.73-75 ; connus = (43,256,6,5.51)/(40,384,6,9.95)/(48,128,8,3.05) l.188-192.
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
- `vision_ref.py <sortie.bin> [poids]` — aucune option ; docstring annonce `--poids` mais c'est un 2e positional (l.9 vs l.29).

**B.3 — Scripts shell**
- `portes.sh [rapide]` — `$1=rapide` l.14,71,105 ; `D=./drave-core/target/release/drave` l.13 ; `A=…/qwen3-30b-8clusters-v2` l.56 ; `M=…/modeles/gguf` l.95 ; `O=…/gpt-oss-120b-MXFP4.gguf` l.106 ; attendus 19.3885 l.53, 799.8557 l.60, 15.6017 l.121 ; seuil tests `-ge 48` et 0 échec l.42 ; timeouts 600/900/1800/2400 l.51,58,75,119 ; aucune variable d'env lue.
- `portes_formats.sh [type ...]` — `filtre="${*:-}"` l.53 ; `DRAVE_MODELES` l.19 ; `DRAVE_LLAMA` l.20 ; `REF_GGML_BLOC` l.21 ; types testés l.26-45 (17 types ggml numérotés) ; blocs 0 et 7 l.65-66.
- `verifier_table_types.sh [chemin llama.cpp]` — `$1` défaut `…/GitHub/llama.cpp` l.19 ; `SRC=drave-core/src/gguf.rs` l.20 ; exit 1 si divergents l.120.
- `inventaire_modeles_lourds.sh [dossier]` — `$1` défaut `…/modeles/gguf` l.13 ; binaire l.14 ; lit `tools/manifeste_modeles_lourds.json` l.35,38 ; timeout 600 l.25.
- `extraire_tables_ggml.sh [verifier]` — `DRAVE_LLAMA` l.15 ; `TMPDIR` l.16 ; tables comparées l.39 (`IQ2XXS_GRID`, `KSIGNS_IQ2XS`, `IQ1S_GRID`, `IQ3XXS_GRID`, `KVALS_IQ4NL`).
- `preparer_colab.sh [modele.gguf] [port=5599]` — l.9-10 ; `/tmp/drave.bundle` l.11 ; empreinte sha256 tronquée 24 car. l.23 ; notebook `colab/Drave-reparti.ipynb` l.46.
- `colab_cote_local.sh [modele.gguf] [port=5599]` — l.12-13 ; `--flux-serveur 0.0.0.0:$PORT --ctx 256` l.30 ; `/tmp/noeud_colab.log` l.30 ; attente 60×0,5 s l.32.
- `sprint.sh <start|status|close|list> ["objectif"]` — l.26-28 ; `SCRUM_DUREE` (7200 s) l.15 ; `sprints/COURANT` l.16 ; trame de clôture l.60-67.

**B.4 — Variables `DRAVE_*` (39 noms déclarés dans `main.rs:17-27`, liste vérifiée par test ; message si l'ancien nom `QT_*` est posé, `main.rs:80-86`)**
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
- `DRAVE_MMAP` — gguf.rs:156 — `0`/`non`/`false` ⇒ lecture complète (défaut : mmap).
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
- Hors moteur : `DRAVE_MODELES` (tools/portes_formats.sh:19), `DRAVE_LLAMA` (portes_formats.sh:20, extraire_tables_ggml.sh:15), `REF_GGML_BLOC` (portes_formats.sh:21, verifier_formats.py:28), `TMPDIR` (extraire_tables_ggml.sh:16), `SCRUM_DUREE` (sprint.sh:15), `LD_LIBRARY_PATH` (verifier_table_types.sh:53), `DSH_HOME` (session_report.py:55-61). Aucune variable `RAYON_*`, `OMP_*`, `MKL_*`, `OPENBLAS_*`, `CUDA_*` n'est lue.

## C. Contradictions, chiffres périmés, affirmations douteuses
- `sprints/01:12` — « 13 480 (le chiffre avait bougé de 312 lignes) » — le commit cité deux lignes plus haut (`1f53667`, l.24) annonce 13 168 ; les deux chiffres cohabitent dans le même fichier sans dire lequel est la mesure finale (sprint 7 dira 13 758, l.95).
- `sprints/01:31` — commit « exact à 1,03e-7, 40× plus rapide » — contredit par le tableau l.42 (« 1,6–2,3e-7 ») ; l'écart « flatteur » venait d'un banc qui réutilisait la même clé (l.56).
- `sprints/01:48` — « le croisement en clés est entre 255 et 2 047 » — formulation corrigée depuis « entre 8 192 et 16 384 clés » (l.89-93) ; l'ancienne formulation confondait contexte et nombre de jetons.
- `sprints/01:116-118` — « `--attn-topk` est **ignoré par le mode lot** … **non corrigé** » — l'état « non corrigé » est périmé : le moteur imprime désormais « IGNORÉ en mode lot » (`model.rs:3969`, message unique `LOT_TOPK_IGNORE` model.rs:2465).
- `sprints/02:47` — tableau « 8 191 | 4 095 | 38,84 | (mesuré) | (calculé) » — cellules GPU/rapport étiquetées au lieu de chiffrées : ligne illisible et non vérifiable.
- `sprints/02:31` — « croisement à ~300 clés » — présenté comme mesure alors que le seuil mesuré du noyau fusionné est 131 072 clés (l.29) ; deux « croisements » différents (déport vs CPU, noyau 4 vs chaîne) mais un seul mot.
- `sprints/03:51-53` — « ~175 ms par jeton de prompt (`--infer` préremplit jeton par jeton) » — **faux**, corrigé dans le même fichier l.79-85 (le préremplissage par lots est actif).
- `sprints/03:141-143` — introspection : « une sonde d'aiguille coûte cher … parce que le préremplissage par lots n'est pas branché en inférence » — reprise de l'affirmation corrigée l.84 : la cause invoquée est fausse.
- `sprints/03:29-30` vs `sprints/05:60` — « 511/511 » réapparaît comme accord top-1 (lot 1 vs 256) après que `sprints/03:40-47` a corrigé un « 511/511 » fautif (497/511) ; même graphie, mesures différentes.
- `sprints/04:14` — commit `09adea5` « 0/3 au milieu à k=512, 3/3 à k=1024 (trois fenêtres par point) » — contredit par l.36-44 : les trois colonnes sont **trois répétitions de la même invite** (garde-fou d'offset).
- `sprints/04:39` — « l'offset avance de 200 000 » avec garde-fou à 400 000 — `sprints/05:79` décrit le même garde-fou comme « **20 000 fixes** » ; deux versions du même défaut, non réconciliées.
- `sprints/04:22-34` — tableau « 0/0/3 » présenté comme balayage en k — invalidé deux pages plus loin (l.36-44) : les répétitions ne mesurent rien ; seuls la convergence avec le premier balayage et le seuil (12,5 %, 25 %] subsistent.
- `sprints/05:77-78` — « « 7e-4 nat par position AU PLUS » — contredit par le tableau deux lignes plus haut (max 0,0068) : c'est la MOYENNE. Corrigé. » — erreur reconnue dans le fichier.
- `sprints/06:32` — tableau du taux : « k = 256 (GPU) | **NON** | (non mesuré) | … » — état périmé : `sprints/07:71` donne k=256 sur les 9 fenêtres (8/9).
- `sprints/06:53-54` — « Le « facteur 10 à 20 » est donc un minorant observé, pas une mesure » — puis l.58-62 : ce n'était pas un ralentissement mais un **LIVELOCK** (`while cap < besoin { cap = (cap*2).min(ctx) }`) ; la première qualification est fausse.
- `sprints/07:45-48` — « là où j'ai écrit « rendu la main en 312 s » … Mon script de vérification ne lisait ni le code de sortie ni le mot « panicked » : il a pris un core dump pour une réussite » — affirmation fausse reconnue (SIGABRT exit 134).
- `sprints/07:138-142` — « **DeepSeek-V4.1-Flash est un modèle d'API** … **aucun poids ouvert**, donc rien à télécharger » — contredit par le dépôt lui-même : `tools/manifeste_modeles_lourds.json:3` déclare `DeepSeek-V4.1-Flash-Q2` (repo `antirez/deepseek-v4.1-flash-gguf`, 365 713 686 528 octets), `tools/portes_formats.sh:38` teste `DeepSeek-V4.1-Flash-Q2.gguf`, et `sprints/09:5,10` mesure ses 365,7 Go.
- `sprints/07:60` — « **18 tests** au lieu de 17 » vs `sprints/08:65` « **32 verts** (20 → 32) » vs `sprints/08:278` « **30 tests verts** (20 au début) » — trois décomptes pour le même sprint dans le même fichier ; `tools/portes.sh:42` exige désormais ≥48 (53 tests dans les sources).
- `sprints/08:118-119` — « L'épreuve d'exécution : **ACQUISE**, 15,2789 des deux côtés » vs `sprints/08:257-260` (Planning #1) « Le chemin par lots sur les MoE : **établir d'abord s'il est cassé** » — contradiction interne : la même page dit qu'il fonctionne (15,2736 en `--lot 64`, l.120-126).
- `sprints/08:132-133` — « `read_to_end` charge tout le fichier : DeepSeek-V4.1-Flash fait 366 Go, il **faudra** `mmap` » — périmé dans le même fichier : le mmap est livré l.145-149 et 283 ; `sprints/08:263` (Planning #3) le redemande encore.
- `sprints/08:218-221` — « 27,8 s de chargement, est-ce mieux ? Non, c'est **plus lent** que le fichier unique annoncé à 3,9 s » — deux mesures de périmètres différents (3,20 Go d'un cluster contre 18,55 Go complet) : la comparaison est explicitement écartée, mais les deux chiffres restent côte à côte dans les Mesures (l.62).
- `sprints/09:70` — « **Huit** pistes ont été testées, trois ont survécu » vs `sprints/09:100` « **Onze** pistes mesurées, trois retenues » — et le tableau l.29-41 en compte onze : le « huit » est un vestige d'une version antérieure.
- `sprints/09` — le fichier contient **deux** « ## Rétrospective » (l.68 et l.106) et **deux** « ## Planning » (l.84 et l.120) : deux versions fusionnées, dont l'une (l.68-91) précède la section « Revue » (l.94).
- `sprints/09:5,10,19` — « Cible : **DeepSeek-V4.1-Flash** (365,7 Go) », « L'empreinte de V4.1 tombe… », engram `blk.N.engram_embd.weight` — le modèle effectivement mesuré/converti ailleurs est **DeepSeek-V4-Flash** (`sprints/07:13,140-143`, l'engram de V4.1 décrit dans `docs/plan-deepseek41-complet.md:319`) : V4.1 et V4-Flash sont employés l'un pour l'autre (voir la contradiction `sprints/07:138`).
- `sprints/09:61-64` — « NVMe, aléatoire, blocs 4 Mo **5,5 Go/s** » > « NVMe, séquentiel **2,1 Go/s** » — l'aléatoire plus rapide que le séquentiel n'est explicable que par des tailles de bloc différentes ; le tableau ne les donne pas (affirmation douteuse en l'état).
- `sprints/09:74-76` et `sprints/09:111-115` — « trois fois un chiffre absurde a sauvé la conclusion (disque à 2 211 Go/s, allocation à 4,1 %, total à 4 231 Go) » / « `pread` sans contrôle a produit un chiffre faux d'un facteur 37 000 » — chiffres faux reconnus, conservés sans la valeur correcte correspondante.
- `tools/aiguille.py:84-88` — « un prompt PLUS LONG que le contexte **ne fait pas échouer le moteur — il le ralentit d'un facteur 10 à 20 sans un mot** (mesuré : 13 à 23 min au lieu de 75 s) » — **périmé** : `sprints/06:58-62` établit un livelock (jamais terminé) et `sprints/07:38-56` un correctif (troncature annoncée, exit 0) ; le commentaire de l'outil contredit l'état du moteur.
- `tools/aiguille.py:19-22` — « depuis le **sprint 4**, le décalage de fenêtre est RÉELLEMENT appliqué » — le correctif définitif du pas/garde-fou est daté du sprint 5 (`sprints/05:79-85`, `aiguille.py:167-199`) ; le sprint 4 n'avait produit qu'un garde-fou à 20 000 fixes.
- `tools/profil_flux.py:8` — l'usage annonce `[--couche N]` — l'option n'est jamais lue ni implémentée (analyse du `main`, l.36-43) : aide qui ment.
- `tools/vision_ref.py:9` — l'usage annonce `[--poids <sortie.bin.poids>]` — ce n'est pas une option mais un 2e positional (l.28-29) ; passer `--poids` donne un chemin littéral « --poids ».
- `tools/harmony_canonique.py:17` — `Q = "/home/stephane/Data13TB/stephane/GitHub/Drave/drave-core/target/release/drave"` — chemin codé en dur vers un répertoire **inexistant** (`GitHub/Drave` ; le dépôt est `GitHub/Qtrinet`) : l'outil ne peut pas tourner tel quel.
- `drave-core/src/main.rs:454-456` — docstring de `fils()` : « sinon la moitié des cœurs » — le code (l.460-462) rend `coeurs_physiques().max(1)`, soit **tous** les cœurs physiques ; le commentaire de `Options` (l.530-533) dit encore « la moitié des cœurs contre les trois quarts ».
- `drave-core/src/main.rs:541` — champ `ppl_profil: bool` sans aucune branche dans `analyser` (580-742) — `--ppl-profil` n'existe pas : tout usage est classé drapeau inconnu ; le champ reste toujours `false` (l.4295, 4493-4585 morts).
- `drave-core/src/main.rs:51-64` — l'aide n'énumère ni `--plan`, `--tokenize`, `--config`, `--flux-serveur`, `--ppl-reparti`, `--banc-*`, `--banc-vision`, `--bloc`, `--gpu-banc`, ni `--options-*` : 15 des 16 modes sont absents de l'usage.
- `sprints/03:81` et `sprints/06:60` / `sprints/07:29` — citations `model.rs:3911` et `model.rs:1117` — ces numéros de ligne ne résolvent plus dans le fichier actuel (7022 lignes) : `3911` tombe dans `rope_inverse`, `1117` dans `CacheExperts` ; `KvCache::assurer` est à `model.rs:2169` et `kv_assurer` à `gpu.rs:440`.
- `tools/portes.sh:29-30` — commentaire « Prendre la première occurrence du motif donnait 17,431 (fenêtre 1) au lieu de 19,3885 (total) — un instrument faux qui accuse le code » — cohérent avec `sprints/01:49`, mais c'est le même genre d'erreur que `sprints/03:42-47` (sortie partielle lue comme globale) ; les deux subsistent dans deux fichiers différents.
- `sprints/05:62` — « 7e-4 nat par position suffit à changer un jeton greedy après quelques dizaines de pas » — présenté comme cause de l'écart `--lot 1` vs `--lot 256`, mais l'écart moyen mesuré est 0,0007 et le max 0,0068 (l.60) : la généralisation « suffit » n'est pas mesurée.

## D. Fichiers du dépôt cités ou définis
- `sprints/01-premier-des-trois-noyaux-gpu-du-top-k-le.md` … `09-empreinte-memoire-ce-qui-reduit-vraiment.md` — les 9 journaux de sprint dépouillés (cérémonie, chiffres, planning) ; définis par `tools/sprint.sh:33,41,68`.
- `sprints/COURANT` — fichier d'état `num debut fin` du sprint en cours ; `tools/sprint.sh:16,34`.
- `tools/aiguille.py` — sonde aiguille (récupération d'un code à une profondeur) ; 219 l. ; cité `reports/rapport-aiguille-topk.md`.
- `tools/analyse_empreinte.py` — empreinte mémoire d'un MoE depuis une trace de routage ; 208 l. ; cité `sprints/09:73,97`.
- `tools/analyse_experts_statique.py` — analyse statique des poids d'experts (jumeaux, sources, destinations) ; 244 l. ; fournit `Lecteur` à `verifier_formats.py`.
- `tools/analyse_flux.py` — analyse pure d'une trace DRVF (densité, neurones persistants) ; 95 l.
- `tools/archive_sessions.py` — archive des sessions DSH (JSONL/zstd) ; 208 l.
- `tools/clusters_moe.py` — découpage des MoE en clusters depuis une trace de routage ; 224 l. ; produit un JSON consommé par `convertir_clusters.py --trace`.
- `tools/colab_cote_local.sh` — côté local de la démonstration Colab (nœud + tunnels) ; 69 l.
- `tools/compare_etats.py` — comparaison tenseur par tenseur Drave/llama.cpp (format `REFD` et vidages `DRAVE_DUMP_COUCHES`) ; 84 l.
- `tools/compare_logits.py` — comparaison de deux fichiers de logits (NLL, rang, accord top-1) ; 109 l. ; cité `sprints/03:43`.
- `tools/convertir_clusters.py` — convertisseur GGUF → clusters (`commun.gguf`, `cluster-NN.gguf`, `manifeste.json`, `mapping.tsv`) ; 525 l.
- `tools/diff_flux.py` — diff de deux traces DRVF ; 91 l.
- `tools/extraire_tables_ggml.c` / `.sh` — extraction/vérification des grilles IQ contre libggml ; 55 l. (sh) ; compare à `drave-core/src/formats.rs`.
- `tools/flux_codec.py` — codec de référence DRVF v1/v2 (lit v3) ; 158 l.
- `tools/harmony_canonique.py` — identifiant de perplexité au format harmony canonique (canaux `analysis`/`final`) ; 72 l.
- `tools/hc_synthetique.py` — référence numpy des hyper-connexions V4 + témoins collés dans `model::tests_hc` ; 98 l.
- `tools/inventaire_modeles_lourds.sh` — inventaire des GGUF lourds confronté au manifeste HF ; 48 l.
- `tools/lire_meta_gguf.py` — lecture des métadonnées GGUF (en-tête seul) ; 117 l.
- `tools/make_patch.py` — fabrication d'un greffon `QPAT` (`--patch`) ; 59 l. ; cité `docs/glossaire.md:890`.
- `tools/manifeste_modeles_lourds.json` — manifeste des 24 fichiers lourds (nom, repo, chemin, octets) ; lu par `inventaire_modeles_lourds.sh:35` et `telecharger_modeles.py:127`.
- `tools/mesurer_lecture_experts.py` — lectures d'experts série/parallèle à froid (`posix_fadvise`) ; 81 l.
- `tools/mla_synthetique.py` — modèle MLA synthétique + référence numpy (`logits.npy`, `ids.npy`, `forme.json`) ; 250 l. ; consommé par `--banc-mla`.
- `tools/pair_factice.py` — pair factice du protocole de flux (écoute, dit ce qu'il reçoit) ; 140 l. ; sert avec `--flux-serveur`/`--ppl-reparti`.
- `tools/portes.sh` — portes de non-régression du dépôt (Qwen, clusters, gpt-oss, matériel, formats) ; 132 l.
- `tools/portes_formats.sh` — portes des décodeurs de formats contre libggml, bloc par bloc ; 74 l.
- `tools/preparer_colab.sh` — préparation de la répétition Colab (bundle git, empreinte, commandes) ; 54 l.
- `tools/profil_flux.py` — profilage par neurone d'une trace DRVF (+ CSV) ; 78 l.
- `tools/proxy_latence.py` — relais TCP ajoutant une latence par message ; 54 l.
- `tools/ref_ggml_bloc.c` / `tools/ref_logits.cpp` / `tools/ref_logits` — références C/C++ liées à libggml et à llama.cpp ; cités `portes_formats.sh:15`, `verifier_formats.py:28`.
- `tools/session_report.py` — rapport par session DSH (`journal/sessions/<id>/rapport.md`, `journal/README.md`) ; 341 l.
- `tools/sprint.sh` — boxing temps réel (`start`/`status`/`close`/`list`) ; 76 l.
- `tools/telecharger_modeles.py` — téléchargement par tranches avec reprise (sidecar `.etat.json`, curl `-r`) ; 197 l.
- `tools/trace_compacite.py` — chiffrage d'une trace DRVF sous plusieurs encodages (zstd compris) ; 432 l.
- `tools/verifier_formats.py` — comparaison d'un super-bloc déquantifié à libggml (`--bloc`) ; 108 l.
- `tools/verifier_table_types.sh` — confrontation de la table des types ggml du moteur à `libggml` ; 121 l.
- `tools/vision_mtmd.py` — référence de vision via libmtmd d'ollama ; 159 l.
- `tools/vision_ref.py` — référence numpy de l'embedding de patchs (mRoPE 2-D) ; 162 l. ; consommé par `--banc-vision`.
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
- `docs/contexte-long.md`, `docs/plan-deepseek-v4-flash.md`, `docs/plan-deepseek41-complet.md`, `docs/format-flux.md`, `docs/histoire.md`, `docs/comparaison-spiking.md`, `docs/convertisseur.md`, `docs/glossaire.md` — documents cités par les sprints/outils (contexte long, plan DeepSeek, spécification DRVF, traduction `QT_*`→`DRAVE_*`, comparatif spiking, placement PCIe/DDR3, glossaire) ; tous présents.
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

### 🤖 Assistant

⏵ Vérification du nombre de drapeaux et de l'existence de `--ppl-profil`

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src; echo \"-- match arms --\"; sed -n '580,745p' main.rs | grep -cE '^\\s+\"--'; echo \"-- ppl_profil --\"; grep -n \"ppl_profil\\|ppl-profil\" main.rs; echo \"-- variables declarees --\"; grep -n \"DRAVE_\" main.rs | sed -n … [128 caractères tronqués]`

  ```
-- match arms --
93
-- ppl_profil --
541:    logits_bin: Option<String>, ppl_profil: bool,
4295:        ppl_profil, lot, profil_neurones, neurones_sortie, trace_flux, trace_couches, flux_forcer,
4493:    let profil = ppl_profil;
-- variables declarees --
11:/// Variables d'environnement que le moteur lit, **sans** le préfixe `DRAVE_`.
63:        eprintln!("       (un dossier contenant commun.gguf EST un modèle ; DRAVE_CLUSTERS=0,3");
64:        eprintln!("        ne charge que certains clusters ; DRAVE_MMAP=0 lit au lieu de mapper)");
17:const VARS_LUES: &[&str] = &[
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; grep -rn \"ppl-profil\" docs reports sprints | head; echo \"=== VARS_LUES ===\"; sed -n '17,60p' drave-core/src/main.rs | grep -c '\"'; echo \"=== check ===\"; sed -n '17,22p' drave-core/src/main.rs", "description": "Check ppl-profil r … [25 caractères tronqués]`

  ```
docs/contexte-long.md:520:   **722,56** chez nous (1,1 %). Le profil par profondeur (`--ppl-profil`) montre
docs/vision.md:74:| `--ppl-profil` | le temps par poste (projections, rope, attention, FFN, tête) |
docs/glossaire.md:1334:**Profilage par neurone · `--ppl-profil`** — Compter quels neurones s'allument, à
docs/glossaire.md:1336:`--neurones-sortie`), et quel poste consomme le temps (`--ppl-profil`). C'est l'axe 1
reports/rapport-gpt-oss-perplexite.md:215:512 et 4 096), et le profil par profondeur (`--ppl-profil`, ajouté pour ça) le
reports/rapport-drapeaux-ignores.md:97:| `--ppl-profil` `--logits-bin` | P : 2854, 2837 | I : jamais lu | 🟡 |
=== VARS_LUES ===
20
=== check ===
const VARS_LUES: &[&str] = &[
    "BANC_KV_DEBUG", "BANC_KV_GPU_SEUL", "BANC_KV_GRAD", "BANC_KV_K0",
    "BANC_KV_KUNIT", "BANC_KV_UNIT", "BANC_KV_V1", "BANC_SANS_PUITS",
    "CLUSTERS", "DEBUG_ETAT", "DEBUG_FLUX", "DEBUG_MLA", "DUMP_COUCHES", "ETAT_ENTREE",
    "FLUX_VERIF", "GPU", "GPU_EXPERTS",
    "GPU_EXPERTS_GO", "GPU_KV", "GPU_TETE", "GPU_TOPK", "HARMONY_TRACE",
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; awk 'NR>=17 && NR<=30' drave-core/src/main.rs | grep -o '\"[A-Z0-9_]*\"' | wc -l; awk 'NR>=17 && NR<=30' drave-core/src/main.rs", "description": "Count declared DRAVE_ variables"}`

  ```
39
const VARS_LUES: &[&str] = &[
    "BANC_KV_DEBUG", "BANC_KV_GPU_SEUL", "BANC_KV_GRAD", "BANC_KV_K0",
    "BANC_KV_KUNIT", "BANC_KV_UNIT", "BANC_KV_V1", "BANC_SANS_PUITS",
    "CLUSTERS", "DEBUG_ETAT", "DEBUG_FLUX", "DEBUG_MLA", "DUMP_COUCHES", "ETAT_ENTREE",
    "FLUX_VERIF", "GPU", "GPU_EXPERTS",
    "GPU_EXPERTS_GO", "GPU_KV", "GPU_TETE", "GPU_TOPK", "HARMONY_TRACE",
    "KV_BITS", "KV_F16", "KV_K_F16", "KV_K_F32", "KV_V_F32", "MMAP",
    "PRELIRE", "PRELIRE_TOUT", "Q8_BLOCS", "SANS_EMPRUNT", "TRACE_BLOCS",
    "TRACE_EXPERTS", "VISION_TEXTE", "YARN", "YARN_MSCALE", "YARN_NON",
    "YARN_RAMPE",
];

mod clusters;
mod engine;
  ```

### 🤖 Assistant

⏵ Corrections ciblées après vérification dans le code

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "new_string": "Le moteur expose **93 drapeaux `--xxx`** reconnus et **39 variables `DRAVE_*`**\ndéclarées (`drave-core/src/main.rs:17-27`, `:580-742`). L'audit du 30/09 en\ncomptait 84 et 26, et montrait que **46 drap … [732 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "new_string": "**Lot (mode 3) · lot en listes (mode 4)** — Le *lot* transporte `t` états d'un coup\nen f32 dense, sans perte, pour que le préremplissage ne paie qu'un aller-retour par\nlot (écart mesuré 0,00e0). Le *l … [872 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "new_string": "**Trace de flux, versions 1 à 3** — v1 : indices `u32` + valeurs `i16` (6,02 octets\npar neurone actif) ; v2 : indices par écarts `u8` + valeurs `i16` (3,01 octets, sans\nperte, **défaut**) ; v3 : valeu … [580 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "new_string": "**Expert (MoE)** — Sous-réseau spécialisé qu'un routeur allume pour certains\njetons seulement. « Un expert qui ne tire pas coûte zéro octet » : c'est l'avantage\nstructurel revendiqué par le projet (`d … [561 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "new_string": "**Table de routage (`ffn_gate_tid2eid`)** — Variante de routage sans score : les\npremières couches de V4 lisent l'expert à allumer dans une table indexée par le\njeton (`I32`, forme `[129 280 × 6]`), a … [288 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "new_string": "**Nœud partiel** — Nœud qui ne charge qu'une partie des grappes\n(`DRAVE_CLUSTERS=0,3`) au lieu du modèle entier. Un cluster **demandé mais absent du\ndisque est une erreur**, pas un silence ; et rien n … [328 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

### 👤 Utilisateur

Background subagent f2de810a-b765-444d-b3cc-d8fce1ba2105 finished and will do no further work unless you send it more.
Its closing message:
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

### 🤖 Assistant

⏵ Ajout des derniers points relevés et compléments d'outils

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "new_string": "**SparseVec (vecteur creux)** — Structure `{ indices triés, valeurs contiguës }` qui\nreprésente une activation creuse explicite. C'est le type que reçoivent les\naccumulateurs `accumulate_push` / `accu … [689 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "new_string": "| `tools/profil_flux.py` | densité par couche, part des 10 % les plus forts, export CSV | `docs/roadmap.md:129-149` |\n| `tools/analyse_empreinte.py` | empreinte mémoire d'un MoE depuis une trace de rou … [1212 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "new_string": "| `tools/verifier_table_types.sh` | compare la table des types ggml à la bibliothèque | `docs/format-clusters.md:148-154` |\n| `tools/extraire_tables_ggml.sh` | relève les grilles IQ dans `libggml` et l … [314 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "new_string": "| `tools/hc_synthetique.py` | modèle à hyper-connexions jouet (référence numpy + témoins) | `docs/plan-deepseek41-complet.md:171-186` |", "old_string": "| `tools/hc_synthetique.py` | modèle à hyper-conn … [56 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "new_string": "18. **Des termes attendus sont absents du corpus.**\n    `Hadamard`, `MTP` (hors la mention `dspark_*`), `SparseVec` hors des rapports\n    d'optimisation, `speculative decoding` en toutes lettres, `MTo … [2501 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Relecture complète du glossaire et comptage des entrées

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"lignes: $(wc -l < docs/glossaire.md)\"; echo \"mots: $(wc -w < docs/glossaire.md)\"; echo \"-- entrées (lignes commençant par **) --\"; grep -c '^\\*\\*' docs/glossaire.md; echo \"-- par thème --\"; awk '/^## /{t=$0} /^\\*\\*/{c … [112 caractères tronqués]`

  ```
lignes: 1629
mots: 13947
-- entrées (lignes commençant par **) --
254
-- par thème --
72 ## 2. Modèles et architectures
41 ## 3. Formats, quantification, encodage
40 ## 6. Répartition, matériel et énergie
25 ## 4. Le moteur Drave : exécution, structures, outils
25 ## 1. Le projet, ses noms, sa méthode
23 ## 7. Mesure, qualité et méthode expérimentale
23 ## 5. Flux, protocole et transport
4 ## Mode d'emploi
1 ## Parcours de lecture conseillé
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"-- vraies entrées --\"; grep -cE '^\\*\\*[^*]+\\*\\* — ' docs/glossaire.md; echo \"-- par thème --\"; awk '/^## [0-9]/{t=$0} /^\\*\\*[^*]+\\*\\* — /{c[t]++} END{for (k in c) print c[k], k}' docs/glossaire.md | sort -rn; echo \"- … [112 caractères tronqués]`

  ```
-- vraies entrées --
187
-- par thème --
48 ## 2. Modèles et architectures
28 ## 6. Répartition, matériel et énergie
27 ## 3. Formats, quantification, encodage
23 ## 1. Le projet, ses noms, sa méthode
22 ## 4. Le moteur Drave : exécution, structures, outils
21 ## 7. Mesure, qualité et méthode expérimentale
18 ## 5. Flux, protocole et transport
-- titres --
1:# Glossaire raisonné de Drave
11:## Mode d'emploi
47:## Parcours de lecture conseillé
92:## 1. Le projet, ses noms, sa méthode
228:## 2. Modèles et architectures
549:## 3. Formats, quantification, encodage
738:## 4. Le moteur Drave : exécution, structures, outils
875:### Les outils de `tools/` et les bancs du binaire
918:### Drapeaux de ligne de commande et variables d'environnement
946:## 5. Flux, protocole et transport
1064:## 6. Répartition, matériel et énergie
1267:## 7. Mesure, qualité et méthode expérimentale
1414:## 8. Points relevés, non corrigés
1561:## 9. Sources externes citées
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; awk '{n=gsub(/\\*\\*/,\"**\"); if (n%2==1) print NR\": \"$0}' docs/glossaire.md | head -20; echo \"--- tableaux ---\"; grep -c '^|' docs/glossaire.md; echo \"--- liens ---\"; grep -c 'https\\?://' docs/glossaire.md", "description": "Ch … [28 caractères tronqués]`

  ```
25:   n'ai pas pu vérifier l'adresse, je cite l'article **par son titre et ses
26:   auteurs, sans lien** — c'est une règle du dépôt, on n'invente pas d'URL.
493: **SNN (Spiking Neural Network ; réseau de neurones à impulsions) · spike ·
494: neuromorphique** — Réseau dont les neurones communiquent par impulsions binaires
604: des tenseurs de poids, chacun avec son type de quantification. Le moteur le lit **en
605: place**, en plusieurs fichiers (multi-shards) ou en clusters
783: **Événement** — Dans ce dépôt, un événement est un **couple (écart d'indice,
784: valeur)** représentant une connexion active, sur 2 octets ; c'est l'unité de débit
950: sept top-k par projection, plus `attn_topk`, `qk_topk`, `moe_topk`. Ils **voyagent
951: dans l'en-tête** parce que sans eux le pair distant ne calculerait pas la même
1030: incompatible en nommant les deux versions. Règle écrite dans le code : **un nouveau
1031: mode ⇒ une nouvelle version** (`docs/format-flux.md:88-155`,
1215: (`DRAVE_CLUSTERS=0,3`) au lieu du modèle entier. Un cluster **demandé mais absent du
1216: disque est une erreur**, pas un silence ; et rien n'additionne encore les
1221: d'extension. Mesuré à 6,5 Go/s en x8 Gen3 ic
… [503 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des citations utilisées dans les « Points relevés »

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"=== encodage:42 ===\"; sed -n '42p' reports/rapport-encodage.md; echo \"=== deepseek41 titres P1-P5 ===\"; grep -n \"^### P[1-5]\" docs/plan-deepseek41-complet.md; echo \"=== programme-evolutif:17 ===\"; sed -n '17p' reports/rap … [235 caractères tronqués]`

  ```
=== encodage:42 ===
| 2.00 | 4971.00 % | 5.5 | dense ternaire (référence CDC) |
=== deepseek41 titres P1-P5 ===
164:### P1 — Hyper-connexions : les connexions pondérées (≈ ½ journée) — **FAIT** (02/10)
171:### P1 — Hyper-connexions : les connexions pondérées (≈ ½ journée)
188:### P2 — Épilogue d'attention : dé-rotation, puits, sortie groupée (≈ 3 h) — **FAIT** (02/10)
196:### P2 — Épilogue d'attention : dé-rotation, puits, sortie groupée (≈ 3 h)
208:### P3 — Les couches brutes, de bout en bout (≈ 2 h) — **FAIT pour V4-Flash** (02/10)
217:### P3 — Les couches brutes, de bout en bout (≈ 2 h)
226:### P4 — Compresseur et HCA : le premier flux qui n'existe nulle part (≈ ½ journée) — **HCA FAIT** (02/10)
239:### P4 — Compresseur et HCA : le premier flux qui n'existe nulle part (≈ ½ journée)
252:### P5 — Indexeur et CSA : la liste de candidats (≈ 1 à 2 journées) — **FAIT** (02/10, sauf porte longue)
267:### P5 — Indexeur et CSA : la liste de candidats (≈ 1 à 2 journées) — le gros morceau
=== programme-evolutif:17 ===
| Capteur de co-activation branché sur une projection | **+3,0 %** (96,75 s → 99,64 s sur 1 025 tokens) |
=== coherence-vision:3 ===
**En une ligne** : les **18 documents** d
… [303 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "limit": 95}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md</path>
<type>file</type>
<content>
1: # Glossaire raisonné de Drave
2: 
3: Ce document explique **tout le vocabulaire** employé dans `docs/` (18 documents) et
4: `reports/` (60 rapports, plus 9 fichiers dans `sprints/`), pour quelqu'un qui ne
5: connaît ni les grands modèles de langage, ni le matériel, ni le vocabulaire de la
6: mesure de performance. Il se lit seul : chaque notion est définie sur place, et
7: chaque définition renvoie au fichier du dépôt qui l'emploie.
8: 
9: ---
10: 
11: ## Mode d'emploi
12: 
13: **Ce que contient une entrée.** Chaque entrée suit le même patron :
14: 
15: > **Terme** *(forme développée française ; forme anglaise)* — définition en une à
16: > trois phrases, sans prérequis. **Où** : fichier ou outil du dépôt qui l'emploie,
17: > avec un numéro de ligne quand il aide. **Réf.** : source externe stable (article,
18: > spécification, documentation officielle).
19: 
20: **Conventions de lecture.**
21: 
22: - `chemin:ligne` renvoie à un fichier **du dépôt**, à la ligne indiquée. Exemple :
23:   `docs/vision.md:34`.
24: - Les liens externes pointent vers des articles ou des spécificat
… [4466 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle de l'ordre alphabétique dans chaque thème

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; python3 - <<'EOF'\nimport re, unicodedata\ntxt=open('docs/glossaire.md',encoding='utf-8').read().split('\\n')\ntheme=None\nentries={}\nfor l in txt:\n    if l.startswith('## '):\n        theme=l\n        entries.setdefault(theme,[])\n  … [603 caractères tronqués]`

  ```
## 1. Le projet, ses noms, sa méthode       23 entrées  DÉSORDRE: [('Porte (de décision)', 'Porte de correction'), ('Relire · relecture adverse · relecture déléguée', 'Rejeu')]
## 2. Modèles et architectures              48 entrées  DÉSORDRE: [('Attention (self-attention)', 'Attention creuse'), ("BPE (Byte Pair Encoding ; codage par paires d'octets)", 'Biais (bias)'), ('FFN (Feed-Forward Network ; réseau à propagation avant)', 'Fenêtre glissante (sliding window attention, SWA)'), ('« Perdu au milieu » (lost in the middle)', 'MLA (Multi-head Latent Attention ; attention latente multi-têtes)')]
## 3. Formats, quantification, encodage     27 entrées  DÉSORDRE: [('b/poids (bits par poids)', 'BitNet b1.58'), ('GGUF (GPT-Generated Unified Format)', 'ggml · type ggml · `ggml_blck_size` · `ggml_type_size`'), ('Q4_0 · Q4_1 · Q5_0 · Q5_1 · Q8_0 · Q8_1', 'Q2_K · Q3_K · Q4_K · Q5_K · Q6_K · Q8_K (k-quants)'), ('Quantification du KV', 'QPAT')]
## 4. Le moteur Drave : exécution, struc    22 entrées  OK
## 5. Flux, protocole et transport          18 entrées  DÉSORDRE: [('DRVF (Drave Flux)', 'Corps (payload) · en-tête'), ('Version (du format et du protocole)', 'Colab · notebook · tunnel')]
## 6. R
… [502 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Réordonnancement automatique des entrées par ordre alphabétique

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; cp docs/glossaire.md /tmp/glossaire.bak; python3 - <<'EOF'\nimport re, unicodedata\np='docs/glossaire.md'\nlines=open(p,encoding='utf-8').read().split('\\n')\n# repérer les sections de thème\nsec=[]\nfor i,l in enumerate(lines):\n    i … [2334 caractères tronqués]`

  ```
sections réordonnées: 6
## 1. Le projet, ses noms, sa méthode     23  OK
## 2. Modèles et architectures            48  OK
## 3. Formats, quantification, encodag    27  OK
## 4. Le moteur Drave : exécution, str    22  OK
## 5. Flux, protocole et transport        18  OK
## 6. Répartition, matériel et énergie    28  OK
## 7. Mesure, qualité et méthode expér    21  OK
lignes: 1629
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; diff <(sort /tmp/glossaire.bak) <(sort docs/glossaire.md) && echo \"AUCUNE PERTE : réordonnancement pur\"; echo \"--- titres de thème et compte ---\"; grep -cE '^\\*\\*[^*]+\\*\\* — ' docs/glossaire.md; grep -n '^## ' docs/glossaire.md … [43 caractères tronqués]`

  ```
AUCUNE PERTE : réordonnancement pur
--- titres de thème et compte ---
187
11:## Mode d'emploi
47:## Parcours de lecture conseillé
92:## 1. Le projet, ses noms, sa méthode
228:## 2. Modèles et architectures
549:## 3. Formats, quantification, encodage
738:## 4. Le moteur Drave : exécution, structures, outils
946:## 5. Flux, protocole et transport
1064:## 6. Répartition, matériel et énergie
1267:## 7. Mesure, qualité et méthode expérimentale
1414:## 8. Points relevés, non corrigés
1561:## 9. Sources externes citées
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "new_string": "**Ce que contient une entrée.** Chaque entrée suit le même patron :\n\n> **Terme** *(forme développée française ; forme anglaise)* — définition en une à\n> trois phrases, sans prérequis. La définition d … [618 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "offset": 11, "limit": 25}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md</path>
<type>file</type>
<content>
11: ## Mode d'emploi
12: 
13: **Ce que contient une entrée.** Chaque entrée suit le même patron :
14: 
15: > **Terme** *(forme développée française ; forme anglaise)* — définition en une à
16: > trois phrases, sans prérequis. **Où** : fichier ou outil du dépôt qui l'emploie,
17: > avec un numéro de ligne quand il aide. **Réf.** : source externe stable (article,
18: > spécification, documentation officielle).
19: 
20: **Conventions de lecture.**
21: 
22: - `chemin:ligne` renvoie à un fichier **du dépôt**, à la ligne indiquée. Exemple :
23:   `docs/vision.md:34`.
24: - Les liens externes pointent vers des articles ou des spécifications ; quand je
25:   n'ai pas pu vérifier l'adresse, je cite l'article **par son titre et ses
26:   auteurs, sans lien** — c'est une règle du dépôt, on n'invente pas d'URL.
27: - Un terme qui a **plusieurs sens** dans le corpus est signalé ; c'est le cas de
28:   *CDC*, *mode*, *porte*, *grappe* et *tête*.
29: - Les valeurs numériques citées ici sont celles des documents, **à leur date**.
30:   Elles ne sont pas re-mesurées par ce glossaire ; la secti
… [413 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "new_string": "> **Terme** *(forme développée française ; forme anglaise)* — définition en une à\n> trois phrases, sans prérequis. La définition dit **où** le moteur s'en sert\n> (fichier, outil ou drapeau du dépôt, a … [476 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Contrôle final : fichiers modifiés et relecture d'un échantillon

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; git status --porcelain | head -20; echo \"--- fin du fichier ---\"; tail -6 docs/glossaire.md; echo \"--- échantillon thème 5 ---\"; sed -n '946,975p' docs/glossaire.md", "description": "Check git status and sample content"}`

  ```
M drave-core/src/model.rs
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md
 M journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md
?? docs/glossaire.md
?? journal/sessions/18b8879c-f211-43b8-9908-cf65e509b21d/
?? journal/sessions/2c2a6595-b208-446e-bbd1-d0f49eca45e8/
?? journal/sessions/3d5618a0-4e3a-45bb-943d-a72c753fb7da/
?? journal/sessions/56879594-1434-4e34-83cc-de42cdf192a1/
?? journal/sessions/8549abcb-5d9a-4594-915b-5628c80a2a08/
?? journal/sessions/b13a6032-4f62-4e86-aa1f-03864a455c83/
?? journal/sessions/dcaa24d6-0017-4382-be21-8244c0fb9b7a/
?? journal/sessions/f2de810a-b765-444d-b3cc-d8fce1ba2105/
?? journal/sessions/fba448b3-e237-4eb3-b77d-fcbf7da1c93d/
--- fin du fichier ---
peripherals* ; Gerstner & Kistler, *Spiking Neuron Models* ; Cover & Thomas,
*Elements of Information Theory* ; Warren, *Hacker's Delight* ; Williams,
Waterman & Patterson, *Roofline* ; JEDEC JESD79-3 (DDR3) ; documentation Intel
« Stratix V Device Handbook » et « Quartus Prime » ; spécification OCP
*Microscaling Formats (MX) v1.0* ; PCI-SIG ; *DeepSeek-V4 Technical Report*.

--- échantillon thème 5 ---

## 5. Flux, 
… [1752 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; git diff --stat drave-core/src/model.rs; echo \"--- mtime ---\"; stat -c '%y %n' drave-core/src/model.rs docs/glossaire.md; echo \"--- diff aperçu ---\"; git diff drave-core/src/model.rs | head -30", "description": "Inspect modified mo … [8 caractères tronqués]`

  ```
drave-core/src/model.rs | 72 ++++++++++++++++++++++++++++++++++++++++---------
 1 file changed, 59 insertions(+), 13 deletions(-)
--- mtime ---
2026-10-02 15:03:11.637825878 -0400 drave-core/src/model.rs
2026-10-02 15:17:38.324912652 -0400 docs/glossaire.md
--- diff aperçu ---
diff --git a/drave-core/src/model.rs b/drave-core/src/model.rs
index 4b11017..14e5e49 100644
--- a/drave-core/src/model.rs
+++ b/drave-core/src/model.rs
@@ -151,14 +151,20 @@ pub fn manques_architecture(g: &Gguf, cfg: &Cfg, ctx: usize, clusters: bool) ->
     if quelque_part("attn_derope") {
         manques.push("attention V4 : dé-rotation de sortie");
     }
-    // La clé des ratios est `attention.compress_ratios` (liste par couche), pas
-    // `compress_ratios` : la chercher sous le mauvais nom faisait dire
-    // « calculable » à V4-Flash, dont 41 couches sur 44 sont compressées
-    // (21 CSA + 20 HCA, mesuré : `tools/lire_meta_gguf.py`). Un faux « oui » est
-    // pire qu'un refus : il fait calculer faux sans rien dire.
-    if g.cfg_ou(&["attention.compress_ratios", "compress_ratios"]).is_some()
-        || g.json_brut("compress_ratios").is_some() {
-        manques.push("attentions compressées CS
… [1019 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md", "offset": 1414, "limit": 45}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md</path>
<type>file</type>
<content>
1414: 
1415: ## 8. Points relevés, non corrigés
1416: 
1417: Ces points ont été croisés en rédigeant ce glossaire. **Aucun autre fichier n'a été
1418: modifié** : ils sont listés ici, avec leur chemin et leur citation, pour qu'un
1419: lecteur ne s'y trompe pas.
1420: 
1421: 1. **L'attribution de l'écart int8 se contredit dans le même document.**
1422:    `docs/contexte-long.md:399-401` : « L'écart de +3,0 % contre +0,8 % à 8 192 vient
1423:    donc d'ailleurs : probablement la quantification des VALEURS et la précision du
1424:    softmax, pas l'arrondi des clés. » — alors que le §4.bis.3 du même fichier
1425:    (`:176-197`) et `docs/roadmap.md:30` concluent l'inverse : « tout l'écart est
1426:    dans les CLÉS ».
1427: 
1428: 2. **Un paragraphe barré « CORRIGÉ » subsiste au milieu d'une section.**
1429:    `docs/contexte-long.md:241-248` : « ~~Le format ne change presque rien au temps
1430:    GPU (13,2 à 15,0 ms à 1 M) : le noyau est borné par la déquantification
1431:    scalaire.~~ **CORRIGÉ** ». La phrase fausse reste lisible ; la valeur corrigée
1432:    est 6,5-7,4 ms
… [1686 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle final du fichier livré

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"lignes=$(wc -l < docs/glossaire.md) mots=$(wc -w < docs/glossaire.md)\"; echo \"entrées=$(grep -cE '^\\*\\*[^*]+\\*\\* — ' docs/glossaire.md)\"; echo \"points relevés=$(sed -n '/^## 8\\./,/^## 9\\./p' docs/glossaire.md | grep -c … [264 caractères tronqués]`

  ```
lignes=1630 mots=13958
entrées=187
points relevés=21
liens externes=60
pas de sentinelle résiduelle
?? docs/glossaire.md
  ```

### 🤖 Assistant

⏵ Envoi du résultat à l'agent parent

- **send_message** `{"agent_id": "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", "message": "LIVRÉ : `docs/glossaire.md` (nouveau, 1630 lignes, ~14 000 mots). Aucun autre fichier de ma part.\n\nCONTENU : mode d'emploi + parcours de lecture néophyte (vision → histoire → roadmap → format-flux → sprints → rapport-inference → croi … [2755 caractères tronqués]`

  ```
message delivered to agent bbd6969f-0f70-42b2-8951-64d1f2f36d2e
  ```

### 🤖 Assistant

⏵ Livraison terminée

`docs/glossaire.md` est écrit (1630 lignes, ~14 000 mots) — seul fichier créé, rien d'autre modifié de mon fait.

- **187 entrées**, 7 thèmes classés alphabétiquement : le projet et sa méthode ; modèles et architectures ; formats et quantification ; le moteur Drave ; flux, protocole et transport ; répartition, matériel et énergie ; mesure et méthode. Chaque entrée donne forme développée FR/EN, définition sans prérequis, référence `chemin:ligne`, et source externe (60 liens, tous testés ; les non vérifiables cités par titre).
- Plus : mode d'emploi, parcours de lecture néophyte en 9 étapes, index des outils `tools/`, table des drapeaux CLI et des variables `DRAVE_*`, **21 points relevés non corrigés**, liste des sources.
- **Point 1** — `docs/contexte-long.md:399-401` attribue l'écart int8 aux valeurs, alors que `:176-197` du même fichier et `docs/roadmap.md:30` disent « tout l'écart est dans les CLÉS ».
- **Point 2** — `docs/vision.md:74` liste `--ppl-profil` comme existant ; `reports/rapport-drapeaux-ignores.md:97` le dit « jamais lu » et le code n'a qu'un champ mort (`main.rs:541`) : le drapeau n'existe pas.
- **Point 3** — `reports/bilan-multi-materiel.md:96` reprend « 8 % plus rapide que le dense (15,8 contre 14,7 tok/s) », le chiffre même que `reports/rapport-croisement-push-pull.md:66-71` déclare faux (pull corrigé : 36,4 tok/s).
- Autres : phases P1-P5 dupliquées dans `plan-deepseek41-complet.md` (FAIT puis à faire) ; `plan-prefill-reparti.md:421` dit le mode 4 « à écrire » alors qu'il est mesuré ; accuracy de 4 971 % en `rapport-encodage.md:42` ; `reports/` compte 60 fichiers, pas « une centaine ».
- Signalé au parent : `drave-core/src/model.rs` est modifié dans l'arbre de travail (mtime 15:03) sans que ce soit moi — probable travail parallèle, à vérifier avant commit.

