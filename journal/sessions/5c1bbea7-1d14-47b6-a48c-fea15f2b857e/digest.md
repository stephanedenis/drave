# Session DSH — relecture

- identifiant : `5c1bbea7-1d14-47b6-a48c-fea15f2b857e`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-02 09:52:23
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu es relecteur ADVERSE. Tu ne modifies AUCUN fichier : tu produis un rapport de constats, avec citations exactes et numéros de ligne.

Contexte : le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet contient un moteur d'inférence nommé **Drave**. Sa vision est définie dans `docs/vision.md` et `docs/programme-recherche.md` — lis-les ENTIER d'abord (textes de référence), puis audite les documents ci-dessous.

Résumé de la vision à faire respecter :
- Drave conduit un **flux de listes d'activation** (AER, « push ») ; le coût suit l'ACTIVITÉ, pas la taille du modèle.
- Encodages : listes valuées **par source** ; **deux listes** (trinaires, le signe porté par l'appartenance) ; cas général **connexions pondérées**.
- Le cœur est de **router ces flux sur des grappes de neurones** réparties entre composants (CPU, GPU, FPGA) et entre **machines**.
- Le flux est un **journal** : tracer, rejouer, comparer, transporter — et il sert à **analyser le comportement du modèle pour adapter l'architecture à la tâche**.
- Le dense existe et gagne au-dessus d'environ 22 % de densité (mesuré) : la vision ne prétend pas que le sparse gagne toujours.
- Chaque chiffre publié a sa source ; un échec se documente au lieu de disparaître.

Faits À JOUR au 02/10/2026 (toute divergence est à signaler) :
- porte gpt-oss ctx 256 = **15,6017** (15,1757 avant le 02/10) ; Qwen2.5-0.5B ctx 256 = **19,3885** ; clusters Qwen3-30B = **799,8557** ; `cargo test --release` = **48 tests** ;
- protocole de transport des flux = **v5**, avec les modes 0 (f32 dense), 1 (liste quantifiée), 2 (listes à échelle par bloc), 3 (LOT dense), 4 (LOT en listes) ;
- 18 formats lisibles (dont IQ1_S/IQ1_M/IQ2_XXS/IQ3_XXS/IQ4_XS/Q3_K/Q5_K/Q5_0), vérifiés contre libggml ;
- DeepSeek-V4-Flash (86,9 Go) est le modèle ouvert de la famille V4 ; llama.cpp l'exécute (`deepseek4`) ; **V4.1 ne se calcule pas encore** (hyper-connexions, sortie à rang faible groupée, dé-rotation + puits, attentions compressées CSA/HCA) et son GGUF Q2 n'a pas les tenseurs `output_hc_*` alors qu'il déclare `hc_mult = 4` ;
- le plan V4.1 à jour est `docs/plan-deepseek41-complet.md` (« les flux d'abord ») ; il remplace toute intention antérieure sur V4.1 ;
- `docs/plan-deepseek-v4-flash.md` date du 01/10 : le lecteur multi-fichiers et la lecture des métadonnées y sont décrits comme à faire — ils sont faits depuis.

DOCUMENTS À AUDITER (lis-les en entier) :
1. docs/plan-mode4-lot-listes.md
2. docs/plan-deepseek-v4-flash.md
3. docs/plan-deepseek41-complet.md
4. docs/comparaison-spiking.md

Ce que tu cherches, par ordre d'importance :
1. **Périmé** : un document qui décrit comme « à faire » ce qui est fait (lecteur multi-fichiers, métadonnées DeepSeek, MLA rang faible, formats IQ), ou qui annonce un plan remplacé.
2. **Contradictions avec la vision** : but affiché qui fait du dense ou de llama.cpp la référence de valeur ; listes traitées comme une option.
3. **Chiffres périmés** (portes, tests, protocole, formats).
4. **Absence des deux dimensions structurantes** : grappes/machines, et lecture des flux pour adapter l'architecture à la tâche.
5. **Affirmations non sourcées.**

Format de sortie, strictement : un tableau markdown

| fichier:ligne | citation exacte (≤ 25 mots) | problème | correction minimale proposée (texte de remplacement exact) | gravité |

puis une liste courte « ce qui est déjà cohérent et ne doit pas être touché », et une liste « points à trancher par l'humain » s'il y en a.

Règles : corrections MINIMALES uniquement (une phrase, un chiffre, un encadré de deux lignes en tête de document pour dire qu'il est remplacé) — jamais de réécriture. Aucun faux positif : cite la ligne exacte. Si un document est cohérent, dis-le en une ligne. Maximum 25 constats.
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

⏵ Reading the reference vision docs first, then auditing the four target documents.

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/ && wc -l /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/*.md", "description": "List docs and count lines"}`

  ```
total 304
drwxr-xr-x. 1 stephane stephane   636  2 oct 09:17 .
drwxr-xr-x. 1 stephane stephane   612 30 sep 17:59 ..
-rw-r--r--. 1 stephane stephane  6751 30 sep 16:06 colab-reparti.md
-rw-------. 1 stephane stephane  8505 30 sep 08:44 comparaison-spiking.md
-rw-------. 1 stephane stephane 32210  1 oct 01:07 contexte-long.md
-rw-------. 1 stephane stephane 16030 28 sep 11:57 convertisseur.md
-rw-------. 1 stephane stephane  9291  1 oct 12:35 format-clusters.md
-rw-r--r--. 1 stephane stephane 10788 30 sep 16:03 format-flux.md
-rw-------. 1 stephane stephane  4360 30 sep 13:08 histoire.md
-rw-------. 1 stephane stephane 17742  2 oct 09:17 plan-deepseek41-complet.md
-rw-------. 1 stephane stephane  5600  1 oct 09:38 plan-deepseek-v4-flash.md
-rw-r--r--. 1 stephane stephane  9430 30 sep 19:20 plan-gpu-topk.md
-rw-------. 1 stephane stephane 38731  1 oct 09:38 plan-mla-vision.md
-rw-------. 1 stephane stephane 29749 30 sep 17:34 plan-mode4-lot-listes.md
-rw-------. 1 stephane stephane  9336  1 oct 12:36 plan-modeles-lourds.md
-rw-------. 1 stephane stephane 23415 30 sep 15:31 plan-prefill-reparti.md
-rw-------. 1 stephane stephane 11951 27 sep 16:09 programme-recherche.md
-rw-------. 1 
… [1599 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading vision.md and programme-recherche.md in full as reference texts.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/programme-recherche.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md</path>
<type>file</type>
<content>
1: # Drave — la vision
2: 
3: > *« Stream of logs »* : le flux des listes. Et, en français d'ici, **la drave** —
4: > ces billots qu'on confiait à la rivière au printemps, qu'on guidait de
5: > l'estacade jusqu'à la scierie. Le nom dit exactement ce que fait ce moteur :
6: > il ne lit pas des matrices, il conduit un flux.
7: 
8: Ce document est la **vision** du projet : ce qu'il cherche, pourquoi la
9: représentation qu'il a choisie change la nature des problèmes, et ce que cela
10: ouvre sur chaque axe. Il ne remplace pas les rapports — chaque affirmation
11: mesurée renvoie à celui qui la porte — et il distingue partout ce qui est
12: **mesuré**, ce qui est **raisonné**, et ce qui est **à faire**.
13: 
14: Le projet s'appelait `Qtrinet`, du nom de son origine : un cahier des charges
15: d'inférence ternaire sur un cluster de cartes Stratix V
16: (`Qtrinet-bootstrap.md`). Ce cahier des charges reste l'acte de naissance ; le
17: nom, lui, ne dit plus ce que le projet est devenu. **Drave** le dit.
18: 
19: ---
20: 
21: ## 1. Le cœur : des listes, pas des matrices
22: 
23: Un moteu
… [12746 caractères tronqués]
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
… [11362 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the two shorter audit targets: v4-flash plan and spiking comparison.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-deepseek-v4-flash.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/comparaison-spiking.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-deepseek-v4-flash.md</path>
<type>file</type>
<content>
1: # Chantier — adapter les tests de contexte à DeepSeek-V4-Flash
2: 
3: **État au 01/10 09h40** : le modèle **est téléchargé** dans la bibliothèque du
4: disque mécanique (`/home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/`,
5: 3 shards, 86,9 Go). Le NVMe ne sert plus qu'aux artefacts que nous produisons. Le moteur **lit déjà ses métadonnées** : `--plan` affiche
6: « deepseek4, 43 couches, 256 experts (top-6) ». Mais il ne peut pas encore le
7: FAIRE TOURNER, pour deux raisons précises, et c'est ce document qui les cadre.
8: 
9: ## Ce qui a été téléchargé, et pourquoi celui-là
10: 
11: | nom | nature | poids ouverts ? |
12: |---|---|---|
13: | **DeepSeek-V4.1-Flash** | modèle d'API ([api-docs](https://api-docs.deepseek.com/news/news260910/), [deepseek.com](https://www.deepseek.com/news/deepseek-v4-1-flash/)) | **non** — aucun GGUF publié |
14: | **DeepSeek-V4-Flash** | poids ouverts (base de V4.1) : [unsloth/DeepSeek-V4-Flash-GGUF](https://huggingface.co/unsloth/DeepSeek-V4-Flash-GGUF), [huihui-ai](https://huggingface.co/huihui-ai/Huihui-D
… [4708 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/comparaison-spiking.md</path>
<type>file</type>
<content>
1: # SpikeGPT, Spikformer, Spikingformer — ce qu'ils nous apprennent
2: 
3: Comparaison des trois architectures neuromorphiques de référence avec la nôtre,
4: et inventaire des astuces transposables.
5: 
6: Sources : [Spikformer](https://ar5iv.labs.arxiv.org/html/2209.15425) (Zhang et
7: al., ICLR 2023), [SpikeGPT](https://ar5iv.labs.arxiv.org/html/2302.13939) (Zhu
8: et al., 2023), [Spikingformer](https://ar5iv.labs.arxiv.org/html/2304.11954)
9: (Zhou et al., AAAI 2024).
10: 
11: ---
12: 
13: ## 1. Ce que fait chacun
14: 
15: **Spikformer** remplace la self-attention par une **Spiking Self Attention** :
16: Q, K, V sont des trains de spikes (0 ou 1), la carte d'attention est donc
17: naturellement non négative et **le softmax devient inutile**. L'opération
18: devient `SN(Q·Kᵀ·V·s)` — des ET logiques et des additions, **aucune
19: multiplication**. Deux conséquences : c'est décomposable (`Kᵀ·V` d'abord, en
20: O(N·d²) au lieu de O(N²·d)), et la consommation théorique de l'attention passe
21: de 77-88 µJ à **0,594 µJ**. Résultat : 74,81 % sur ImageNet en 4 pas de tem
… [7773 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the two long audit targets: DeepSeek 4.1 plan and mode-4 LOT plan.

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
… [17572 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading plan-mode4-lot-listes.md in full.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mode4-lot-listes.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mode4-lot-listes.md</path>
<type>file</type>
<content>
1: # Spécification — mode 4 : le **lot en listes** (protocole v5)
2: 
3: > **État : ÉCRIT, mesuré et relu** (voir `reports/rapport-mode4-lot-listes.md`) — ce plan
4: > reste la référence de conception, et les écarts constatés à la mise en œuvre sont
5: > consignés dans ce rapport (version 5, borne des actifs, garde cumulatif). Ce document est la spécification à implémenter ; aucun
6: > fichier de code n'a été touché pour l'écrire. Il suppose connus
7: > `docs/format-flux.md` (protocole v4, modes 0–3) et `docs/plan-prefill-reparti.md`
8: > (le mode 3, mis en œuvre, et ses leçons). Les numéros de ligne sont ceux de
9: > l'arbre au moment de la rédaction (`VERSION_FLUX = 4`, `TAILLE_TETE = 79`,
10: > `MODE_LOT = 3`).
11: 
12: **En une ligne** : le mode 3 transporte `t` états en f32 dense — 3 589 octets par
13: jeton à `t = 16` pour Qwen2.5-0.5B ; le mode 4 transporte **les mêmes `t` états
14: encodés en listes à échelle par bloc de 32 canaux**, soit ≈ 1 530 octets par état
15: au seuil 0,01, **÷2,3 sur le fil**, au prix exact que le mode 2 paie déjà
16: (2,7e-2 d'écar
… [29842 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying repo state: git log, gates, formats, protocol, and reader features.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -25 && echo \"---STATUS---\" && git status --short | head -20 && echo \"---REPORTS---\" && ls -la reports/ | head -40", "description": "Show git log, status, reports list"}`

  ```
5a6ac96 Plan V4.1, version 2 : les flux d'abord — c'est ce qui distingue Drave
386c857 Plan pour exécuter DeepSeek-V4.1 : neuf phases, chacune avec sa porte
e3a802d Test d'exécution de DeepSeek-V4.1 : tout ce qui tourne est mesuré, la passe avant est refusée en 0,33 s
acc3498 L'écart naît APRÈS la couche 0 : 1,9 % / 1,3 % / 3,8 % / 4,0 % aux positions 0-3
9d20a8b Rapport MLA : annexe sur l'écart à la position 3 — ce qui est exclu, ce qui reste
118445c Outils de comparaison : les POSITIONS, pas seulement la position 0
d5dff45 REPRISE : chantiers 3 et 4 de la feuille de route, mesurés
7844b18 Chargeur d'experts : les lecteurs parallèles ne donnent rien, et on sait pourquoi
68487f3 REPRISE : le chantier 2 (tête garantie) est clos par une mesure
c147082 Tête garantie : implémentée, exacte, et mesurée sans gain
eea8f0c REPRISE : bilan de la session (16 commits, 5 changements, 5 chantiers ouverts)
c4f55fd La validation MLA s'arrête à la position 2, et c'est maintenant écrit partout
935fe71 Quantification des activations : lire la TRANCHE utile, pas le tampon entier
86b403f ref_logits : --tensors REGEX, l'outil qui a trouvé le bug MLA
3c6eef5 Kimi-K2.7 (1 026 G poids) calcule : 161 s de c
… [3839 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"15,6017\\|15.6017\\|15,1757\\|15.1757\" --include=*.md --include=*.rs --include=*.py . | head -30", "description": "Grep gpt-oss gate values"}`

  ```
./reports/rapport-coherence-docs.md:116:| 55 | `README.md:344` | gpt-oss-120b : perplexité « **—** » | 15,1757 (REPRISE §2) et 20,8361 à 63 jetons : le chiffre existe | MANQUANT |
./reports/rapport-session-2026-09-30.md:92:Qwen ctx 256 = **19,3885** · gpt-oss ctx 256 = **15,1757** · gpt-oss avec
./reports/rapport-coherence-docs-2.md:113:| 49 | `README.md:345` | ligne gpt-oss : `\| … \| MXFP4 \| **blocs lus** \| **15,1757 (ctx 256)** \| 60 Go \|` | la ligne est **décalée d'une colonne** : « blocs lus » occupe la colonne perplexité et 15,1757 la colonne débit ; la référence est 15,1757 (`REPRISE.md:70`) | CONTRADICTOIRE |
./reports/rapport-coherence-docs-2.md:187:    (« blocs lus » en perplexité, 15,1757 en débit) ; remettre perplexité =
./reports/rapport-coherence-docs-2.md:188:    15,1757 (ctx 256), débit = « blocs lus » ou la valeur réelle, mémoire = 60 Go.
./reports/rapport-gpu-topk-selection.md:234:| référence CPU (sans miroir VRAM) | 15,1757 |
./reports/rapport-gpu-topk-selection.md:295:dense (15,1667), l'écart de 6,6e-5 avec le CPU (15,1757) étant celui, connu et
./reports/rapport-gpu-topk-selection.md:345:| 6 | portes de non-régression : 19,3885 et 15,1757 | ✅ inchangées, mes
… [8092 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking the four audited docs for numeric claims and protocol/config terms.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in docs/plan-mode4-lot-listes.md docs/plan-deepseek-v4-flash.md docs/plan-deepseek41-complet.md docs/comparaison-spiking.md; do echo \"=== $f ===\"; grep -n \"format\\|tests\\|protocole\\|VERSION_FLUX\\|version\\|19,3885\\|15,1 … [150 caractères tronqués]`

  ```
=== docs/plan-mode4-lot-listes.md ===
1:# Spécification — mode 4 : le **lot en listes** (protocole v5)
5:> consignés dans ce rapport (version 5, borne des actifs, garde cumulatif). Ce document est la spécification à implémenter ; aucun
7:> `docs/format-flux.md` (protocole v4, modes 0–3) et `docs/plan-prefill-reparti.md`
9:> l'arbre au moment de la rédaction (`VERSION_FLUX = 4`, `TAILLE_TETE = 79`,
25:| la version change ? | **oui, 4 → 5** | dans `recevoir_flux`, un mode inconnu n'est refusé qu'APRÈS la lecture de `n × 4` octets (repli `_ => {}` puis `autre => Err`) : un pair v4 lirait `4·t` octets d'un corps qui en fait ≈ 1 500·t, se désynchroniserait, puis dirait « mode inconnu » — exact, tardif, muet sur la cause |
34:### 1.1 En-tête : 79 octets, identique aux modes 0–3
39:| 4 | 1 | version | **5** |
44:| 18 | 4 | `n` | **nombre d'ÉTATS `t`** — pas le nombre d'actifs |
145:## 3. Compatibilité : le protocole passe en **version 5**
147:**Oui, il faut une version 5**, et c'est le critère 3.5 (« pas de silence, pas de
150:* un pair **v4** lit l'en-tête, ne connaît pas le mode 4, tombe dans le repli
155:  n'est pas le mode qui manque, c'est la version).
156:* Avec la version 5 : le te
… [4656 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying implementation state in code: protocol v5, mode 4, reader, tests, formats.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== VERSION_FLUX / MODE ===\" && grep -rn \"VERSION_FLUX\\s*[:=]\\|MODE_LOT_LISTES\\|const MODE_LOT\" drave-core/src/main.rs | head -20 && echo \"=== mode 4 non écrit ===\" && grep -rn \"mode 4 non écrit\\|mode 4\" drave-core/ … [307 caractères tronqués]`

  ```
=== VERSION_FLUX / MODE ===
1862:const VERSION_FLUX: u8 = 5;
1879:const MODE_LOT: u8 = 3;
1886:const MODE_LOT_LISTES: u8 = 4;
2216:    let tete = tete_flux(MODE_LOT_LISTES, debut, fin, pos0, t, 0.0, Some(mdl));
2265:    if n == 0 && matches!(mode, MODE_DENSE | MODE_LOT | MODE_LOT_LISTES) {
2271:        MODE_DENSE | MODE_LISTE | MODE_BLOCS | MODE_LOT | MODE_LOT_LISTES => {}
2274:{MODE_LOT_LISTES}, protocole v{VERSION_FLUX})"))),
2277:        MODE_LOT_LISTES => {
2472:                   && !(f.mode == MODE_LOT || f.mode == MODE_LOT_LISTES) {
2490:                if f.mode == MODE_LOT || f.mode == MODE_LOT_LISTES {
2515:                    let reponse = if f.mode == MODE_LOT_LISTES {
2578:    let mode_lot = if mode == MODE_BLOCS { MODE_LOT_LISTES } else { MODE_LOT };
2659:            let o = match (if mode_lot == MODE_LOT_LISTES {
2791:                 if mode_lot == MODE_LOT_LISTES { "lot en LISTES" } else { "lot dense f32" },
4775:        let f = decoder_une_trame(MODE_LOT_LISTES, 1, corps, 896).unwrap();
4790:        let f = decoder_une_trame(MODE_LOT_LISTES, 2, corps, 896).unwrap();
4802:        let r = decoder_une_trame(MODE_LOT_LISTES, 1, corps, 896);
4807:        let r = decode
… [4188 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking the format gate count and router gate count precisely.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"FORMATS\\|formats\" tools/portes_formats.sh | head -30 && echo \"=== count entries ===\" && sed -n '/^FORMATS=/,/^)/p' tools/portes_formats.sh | head -40 && echo \"=== README formats ===\" && grep -n \"formats\" README.md | … [67 caractères tronqués]`

  ```
2:# Portes des FORMATS : chaque déquantificateur comparé à libggml, bloc par bloc.
4:#   tools/portes_formats.sh [type ...]
22:VERIF=tools/verifier_formats.py
73:echo "formats : $ok concorde(s), $ko divergence(s), $abs absent(s)"
=== count entries ===
=== README formats ===
75:quantifié selon plusieurs formats. Trois questions, chiffres en main :
179:comme les formats de graphes compressés (WebGraph/LLP).
356:contiguës adressées par un pointeur et un pas. Les formats de super-bloc sans
364:tools/portes_formats.sh                   # 17 formats × 2 blocs, contre libggml
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"routage\" tools/portes.sh | head -20 && sed -n '80,140p' tools/portes.sh", "description": "Inspect routing gate in portes.sh"}`

  ```
74:# 6. Convention de routage annoncée : elle doit correspondre à ce que le GGUF
79:    v=$($D "$2" --config 2>/dev/null | grep -oE "routage +: .*" | head -1)
    case "$v" in
        *"$3"*) printf "  %-42s %s  ✅\n" "$1" "$3" ;;
        *)      printf "  %-42s %s  ❌ (attendu %s)\n" "$1" "${v:-—}" "$3"; ECHEC=1 ;;
    esac
}
M=/home/stephane/Data13TB/stephane/modeles/gguf
route "GLM-5.3 : sigmoïde ×2,5" "$M/GLM-5.3-UD-IQ1_S/GLM-5.3-UD-IQ1_S-00001-of-00006.gguf" "sigmoïde"
route "Kimi-K2.7 : sigmoïde ×2,827" "$M/Kimi-K2.7-Code-UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00001-of-00008.gguf" "sigmoïde"
route "V4-Flash : racine de softplus" "$M/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf" "racine de softplus"
route "Qwen3-235B : softmax" "$M/Qwen3-235B-A22B-Q2_K/Qwen3-235B-A22B-Instruct-2507-Q2_K-00001-of-00002.gguf" "softmax"

# 7. gpt-oss : le seul long.
if [ "$RAPIDE" != "rapide" ]; then
    echo "  (gpt-oss ~20 min et les portes de formats : lancez-les, ils sont hors de ce script)"
fi

echo ""
[ "$ECHEC" = 0 ] && echo "toutes les portes sont vertes" || echo "AU MOINS UNE PORTE A DIVERGÉ"
exit $ECHEC
  ```

### 🤖 Assistant

⏵ Counting the engine's readable formats from source and docs.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"18 formats\" --include=*.md --include=*.rs --include=*.sh . | grep -v journal/ | head -20 && echo \"=== source formats list ===\" && grep -rn \"IQ1_S\\|IQ3_XXS\\|Q5_0\" drave-core/src/*.rs | head -20", "description": "Find … [30 caractères tronqués]`

  ```
./REPRISE.md:1109:   avec la grille doublée). 18 formats lisibles, 17 vérifiés contre libggml.
=== source formats list ===
drave-core/src/formats.rs:326:/// Déquantifie un bloc **IQ1_S** (50 octets, 256 poids).
drave-core/src/formats.rs:335:    assert!(bloc.len() >= 50, "bloc IQ1_S trop court : {}", bloc.len());
drave-core/src/formats.rs:402:/// Déquantifie un bloc **IQ3_XXS** (98 octets, 256 poids).
drave-core/src/formats.rs:415:    assert!(bloc.len() >= 98, "bloc IQ3_XXS trop court : {}", bloc.len());
drave-core/src/formats.rs:446:// Grille IQ1_S : 2048 codes de 8 niveaux signes (extraits de ggml-common.h).
drave-core/src/formats.rs:2503:// Grille IQ3_XXS : 256 codes de 4 octets (extraits de ggml-common.h).
drave-core/src/gguf.rs:243:/// Bloc **Q5_0** (22 octets, 32 poids) et **Q5_1** (24 octets, 32 poids) :
drave-core/src/gguf.rs:245:/// quants 4 bits. Q5_0 est le type de `token_embd` et des `ffn_gate/up` de
drave-core/src/gguf.rs:248:pub const GGML_Q5_0: u32 = 6;
drave-core/src/gguf.rs:256:/// IQ3_XXS : 98 octets par super-bloc de 256 poids (30 % des poids de Kimi,
drave-core/src/gguf.rs:258:pub const GGML_IQ3_XXS: u32 = 18;
drave-core/src/gguf.rs:259:/// IQ1_S : 50 octets par 
… [920 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"formats\" drave-core/src/main.rs | grep -i \"lisib\\|connu\\|géré\\|noms\\|liste\" | head -20; echo \"=== verifier_formats ===\"; sed -n '1,60p' tools/verifier_formats.py 2>/dev/null", "description": "Locate readable forma … [16 caractères tronqués]`

  ```
=== verifier_formats ===
#!/usr/bin/env python3
"""Compare notre déquantification d'un super-bloc à celle de **libggml**.

    tools/verifier_formats.py <modele.gguf> <tenseur> [index] [--type N]

La référence est la bibliothèque ggml elle-même (`tools/ref_ggml_bloc.c`), pas
une seconde lecture du format écrite ici : une réimplémentation Python partage
les mêmes erreurs de lecture et validerait un déquantificateur faux — c'est
exactement ce qui est arrivé pour IQ2_XXS (pas de 8 octets sur `qs` au lieu de
4), IQ1_M (échelles lues en premier alors qu'elles sont en dernier) et Q2_K
(mauvais indice d'échelle).

Le côté Rust est interrogé par `drave <modele> --bloc <tenseur>:<index>`, qui
passe par `row_f32` — le chemin du chargement réel du modèle. Vérifier un
déquantificateur par un chemin qui n'est pas celui du moteur ne prouve rien.

Sortie : écart max et verdict ; code de retour 1 si divergence.
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyse_experts_statique import Lecteur  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRAVE = os.path.join(RACINE, "drave-core/target/release
… [843 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Cross-checking density, sparsity, and format-flux protocol claims against reports.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== format-flux.md ===\" && grep -n \"version\\|v4\\|v5\\|mode\" docs/format-flux.md | head -30 && echo \"=== localite ===\" && cat reports/rapport-localite-activation.md | head -60", "description": "Check format-flux version  … [20 caractères tronqués]`

  ```
=== format-flux.md ===
20:          version      u16          = 2 (défaut) ou 3 (`DRAVE_TRACE_BLOCS=1`)
28:          puis n_actifs × ( indice u32 · valeur i16 )           [version 1]
29:          puis n_actifs × ( écart u8 · valeur i16 )             [version 2]
45:| | version 1 | version 2 |
56:| | version 2 | version 3 |
66:Le lecteur lit **les trois versions** (1, 2 et 3) ; une version inconnue est refusée en la
84:## Transport (phase 3, TCP) — protocole v5
89:          version      u8           5   (refusée si différente, en le disant)
90:          mode         u8           0 = f32 dense · 1 = liste quantifiée
92:                                    4 = LOT en listes (mode 2 répété par état)
96:          n            u32          dimension (mode 0) ou actifs (mode 1)
97:          échelle      f32          mode 1 uniquement
106:corps     mode 0 : n × f32
107:          mode 1 : n × ( indice u16 · valeur i16 )
108:          mode 2 : n_blocs u32 · n_blocs × f32 · longueur u32 · paires
109:          mode 3 : n × dimension × f32   (n = nombre d'ÉTATS, pas de canaux)
110:          mode 4 : n × [ a_j u32 · n_blocs_j u32 · longueur_j u32 ·
114:Le **mode 4 est le même lot, en listes** : ch
… [4488 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== epasite ===\" && cat reports/rapport-eparsite.md && echo \"=== croisement ===\" && grep -n \"22\\|densit\\|zéro\\|zero\" reports/rapport-croisement-push-pull.md | head -30", "description": "Read sparsity and crossover repo … [5 caractères tronqués]`

  ```
=== epasite ===
# Drave — élagage et approche par événement

Modèle minimal (MLP 32→64→10), accuracy float **76.07 %**, ternaire (non élagué) **49.71 %**.

## 1. Densité naturelle du ternaire

- poids non nuls : **26.3 %** (densité d = 0.263)
- activations non nulles après ReLU : **52.8 %**
- événements réels (poids ∧ activation) : **13.9 %**

## 2. Coût des encodages (bits par poids)

| Encodage | Coût | À d = 50 % | À d = 25 % |
|---|---|---|---|
| dense 2 bits | 2,00 | 2,00 | 2,00 |
| **bitmap + signe** | **1 + d** | **1,50** | **1,25** |
| CSR bloc 16 b | 17·d | 8,50 | 4,25 |
| CSR plat 32 b | 33·d | 16,50 | 8,25 |
| N:M structuré (2:4) | (m+n)/m | 1,50 | — |

> Un poids ternaire non nul ne porte **qu'un signe**. Le bitmap dit *où* sont
> les non-nuls, le signe dit *lequel*. C'est pourquoi « bitmap + signe » est
> toujours ≤ au code dense 2 bits, et strictement meilleur dès qu'il y a un zéro.

## 3. Frontière précision ↔ bits/poids (mesurée)

| Gardés | Densité | Accuracy | dense | bitmap | CSR16 | CSR32 | gain bitmap |
|---|---|---|---|---|---|---|---|
| 100.0 % | 26.3 % | 49.71 % | 2.00 | 1.26 | 4.48 | 8.69 | ×1.58 |
| 75.0 % | 19.8 % | 49.41 % | 2.00 | 1.20 | 3.36 | 6.52 | ×
… [4257 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the multi-file reader report and V4.1 execution report for current state.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' reports/rapport-lecteur-multifichiers.md", "description": "Read multi-file reader report"}`

  ```
# Rapport — un modèle éclaté se lit comme un seul

Sprint 08 · 11:13 → 13:13 · binaire `drave-core` (release), commit à venir.

## La question

Un modèle trop gros pour un nœud, ou un MoE dont un nœud ne sert qu'un huitième
des experts, doit pouvoir être lu **par morceaux** — sans requantification, sans
recopier les poids, et sans que le moteur ait à savoir que le modèle est découpé.
Le sprint précédent a produit le format (convertisseur, 1 587 tenseurs vérifiés
par SHA-256) ; celui-ci devait le rendre **lisible**, et le prouver.

## Ce qui a été mesuré

### L'épreuve décisive : origine contre clusters

Mêmes jetons, même contexte, même quantification, chemin par jeton. Le modèle
d'origine (18,56 Go, un fichier, sur le disque mécanique) contre le même modèle
éclaté en `commun.gguf` + 8 × `cluster-XX.gguf` (sur le NVMe) :

| | perplexité | temps |
|---|---|---|
| modèle d'origine | **15,2789** | 12,2 s |
| modèle en clusters | **15,2789** | 11,6 s |

**Identiques au chiffre près**, sur 63 jetons. C'est la preuve que la traduction
expert global → (fichier, ligne locale) est juste, et que rien n'est perdu ni
décalé dans l'assemblage.

### Les gros fichiers découpés en shards

DeepSeek
… [4030 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat reports/rapport-execution-v41.md && echo \"=== energies ===\" && grep -n \"nJ\\|8,3\\|57 \" reports/bilan-multi-materiel.md | head -20", "description": "Read V4.1 execution report and energy figures"}`

  ```
# Rapport — test d'exécution locale de DeepSeek-V4.1-Flash, avec toutes les optimisations

02/10, sur la copie NVMe `/home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf`
(365,71 Go, 1 046 tenseurs, 40 couches, 384 experts dont 6 par jeton).

**Verdict en une ligne : ce que le moteur sait faire de ce modèle marche et est
mesuré ; la passe avant est refusée en 0,33 s avec la liste exacte de ce qui
manque. Aucun chiffre de calcul sur V4.1 n'existe, ici ou ailleurs dans ce
dépôt — uniquement des mesures statiques.**

## 1. Ce qui tourne, avec les optimisations

| test | commande | résultat mesuré |
|---|---|---|
| en-têtes seuls (`--tensors`) | mmap, aucune copie | 1 046 tenseurs, **365,70 Go** lus en **63,8 ms** |
| configuration (`--config`) | en-tête seul | **74 ms** au total, aucune donnée lue |
| plan matériel (`--materiel`) | détection + heuristiques | 20 threads, 16 lecteurs disque, cache experts 19,5 Go, cache KV 32 bits |
| sonde engram (`--sonder-engram 10000`) | mmap, 16 lecteurs | table 1 : 10 000 entrées en **524 ms** (2,6 Mo touchés sur 101,4 Go) · table 2 : **219 ms** · RSS max **120 Mo** pour 365,7 Go adressés |
| passe avant (`--ppl`) | `DRAVE_PRELIRE_TO
… [4314 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking whether Drave implements deepseek4 at all, and MLA option names.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== deepseek in model.rs ===\" && grep -in \"deepseek\" drave-core/src/model.rs | head -20 && echo \"=== deepseek4 anywhere ===\" && grep -rn \"deepseek4\\|deepseek41\" drave-core/src/*.rs | head -20 && echo \"=== banc-mla === … [144 caractères tronqués]`

  ```
=== deepseek in model.rs ===
40:    /// renormalisation. DeepSeek V4-Flash (`expert_gating_func = 4`) et V4.1.
77:/// Kimi-K2.7 (1 026 G poids), GLM-5.3 (754 G), DeepSeek-V4-Flash (284 G) et
118:    // DeepSeek-V4 : l'attention n'est pas la MLA « simple » de GLM/Kimi.
176:/// de DeepSeek, puis dans le JSON `<arch>.config`.
180:/// pour DeepSeek-V4.1-Flash, dont tout le bloc `text_config` vit dans le JSON
197:/// nom d'origine de DeepSeek, du JSON `<arch>.config`, ou d'un défaut choisi par
218:    // d'origine de DeepSeek, puis le JSON `<arch>.config` recopié par le
286:/// `tid2eid` : les `hash_layer_count` premières couches de DeepSeek-V4 routent
405:    /// DeepSeek, GLM et Kimi ; faux chez gpt-oss, où le softmax sur les k
545:    // refusait en silence, et l'expert partagé des modèles DeepSeek/GLM/Kimi
589:    // Expert partagé (Qwen3-MoE d'origine, DeepSeek) : toujours actif.
605:    //   - `exp_probs_b.bias` (DeepSeek-V3/V4, GLM-5.3, Kimi) : le
624:    // Routage par TABLE (couches `hash_layer_count` de DeepSeek-V4) : la
811:    /// le routage des `hash_layer_count` premières couches de DeepSeek-V4 est une
1102:    /// (`attn_k_b` + `attn_v_b`), qui est celle de Kimi-K2.7 et D
… [1077 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"plan\\b\\|--plan\" drave-core/src/main.rs | head -10; echo \"=== open_multi ===\"; grep -n \"open_multi\\|fn open\" drave-core/src/gguf.rs | head -20; echo \"=== v4-flash report mention ===\"; grep -rn \"DeepSeek-V4-Flash\" … [88 caractères tronqués]`

  ```
55:        eprintln!("       drave <modele> --materiel     détection matérielle et plan de");
66:    // Une seule analyse, puis un aiguillage : `--plan`, `--tokenize`,
98:        (opt.plan, "--plan"), (opt.tokenize, "--tokenize"),
117:    if opt.plan { run_plan(opt); return; }
466:/// Les modes (inférence, perplexité, plan, tokenize) la remplissent par la MÊME
475:    infer: bool, ppl: bool, plan: bool, tokenize: bool, gpu_banc: bool,
541:    /// Détection du matériel et plan de configuration, sans charger de modèle.
569:    // --- tokenize / plan
603:            "--plan" => { o.plan = true; 1 }
1638:/// Détection du matériel et plan de configuration, **sans charger de modèle**.
=== open_multi ===
382:    pub fn open<P: AsRef<Path>>(path: P) -> std::io::Result<Self> {
405:    pub fn open_meta<P: AsRef<Path>>(path: P) -> std::io::Result<Self> {
447:    pub fn open_multi<P: AsRef<Path>>(chemins: &[P]) -> std::io::Result<Self> {
452:    /// Comme [`Gguf::open_multi`], en préfixant les tenseurs de chaque fichier.
455:    pub fn open_avec_prefixes<P: AsRef<Path>>(chemins: &[P], prefixes: &[&str])
460:                                           "open_multi : aucun fichier"));
582:    pub 
… [1601 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the fresh MLA/experts report to see V4-Flash's real current status.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mla-experts.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-mla-experts.md</path>
<type>file</type>
<content>
1: # Rapport — MLA à rang faible et formats sans noyau : GLM-5.3 et Kimi deviennent calculables
2: 
3: Session du 02/10, en autonomie, suite du [rapport sur le
4: routage](rapport-routage-experts.md). Le point de départ était un refus : le
5: moteur ne savait pas calculer DeepSeek-V4-Flash. Le trajet, lui, a traversé
6: quatre verrous qui accusaient tous le fichier alors que c'était le moteur.
7: 
8: ## 1. Les quatre verrous, dans l'ordre où ils sont tombés
9: 
10: | ce qui échouait | ce que le moteur disait | ce qui manquait vraiment |
11: |---|---|---|
12: | V4-Flash, V4.1 | `tenseur blk.3.attn_q.weight absent` | attention MLA à rang faible |
13: | GLM-5.3, Kimi | `mélanges d'experts chargés : 0/79` | formats d'experts IQ sans noyau |
14: | GLM-5.3 | `projection sans aucun format` | FFN dense des 3 premières couches |
15: | V4, GLM-Flash | *(rien : ça tournait)* | hyper-connexions, index, sortie à rang faible |
16: 
17: Aucun de ces messages ne nommait la cause. Un GGUF de 216 Go ne perd pas ses
18: tenseurs : c'est le moteur qui ne les lisait pas.
19: 
20: ## 2
… [12111 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Cross-checking spiking numbers and the mode-4 measured report.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat reports/rapport-mode4-lot-listes.md", "description": "Read mode-4 measured report"}`

  ```
# Mode 4 — le lot en listes : ÷2,3 sur les octets, et ce qu'il coûte

**En une ligne** : un préremplissage de N états peut voyager en **listes creuses**
au lieu de f32 dense — 1,5 ko par jeton contre 3,5 — au prix d'une quantification
dont l'effet **dépend de la longueur du lot**, ce que ce rapport chiffre au lieu de
le cacher.

## Ce que le mode ajoute

Le mode 3 (lot dense) envoie `t × dimension × f32` : simple, sans perte, et c'est
lui qui a rendu le préremplissage réparti fidèle (0,00e0). Le mode 4 envoie le même
lot **en listes** : chaque état est encodé comme le mode 2 (indices par écarts u8
avec échappement vers u16, valeurs i8, une échelle f32 par bloc de 32 canaux) et
**auto-délimité** par un préfixe de 12 octets — `a_j · n_blocs_j · longueur_j` —
dont les trois tailles se lisent avant toute allocation.

Le mode est **avec perte**, comme le mode 2. Le critère n'est donc pas l'égalité
mais la comparaison à ce que le mode 2 coûte déjà.

## Mesuré

Corpus WikiText-2, 256 jetons, 16 jetons par lot, seuil 0,01, deux processus
locaux :

| | octets par jeton | écart local/réparti |
|---|---|---|
| mode 2, un flux par jeton (référence) | 1 608 par flux | 2,74e-2 |
| **mode 4, lots
… [4405 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== cpu-aer ===\" && grep -n \"352\\|63 ms\\|5,3 G\\|tok/s\" reports/rapport-cpu-aer.md reports/rapport-inference.md reports/rapport-minimal.md 2>/dev/null | head -30 && echo \"=== attention timings ===\" && grep -rn \"12,7 ms … [296 caractères tronqués]`

  ```
=== cpu-aer ===
reports/rapport-cpu-aer.md:34:| Cible | ms/token | tok/s |
reports/rapport-cpu-aer.md:49:3. **Une carte FPGA ≈ ce CPU** (23 contre 22 tok/s) : le CPU a
reports/rapport-inference.md:18:généré  : 38 tokens en 3.86 s  (9.85 tok/s)
reports/rapport-inference.md:80:| Événements par token | **352,8 M** |
reports/rapport-inference.md:81:| **Débit de génération** | **10,5 tok/s** (int16) · 10,6 (int8) · **11,4 en dense** |
reports/rapport-inference.md:90:| tok/s | 1,51 | 8,22 | **10,52** | 10,15 | 9,83 |
reports/rapport-inference.md:97:soit 7,6 tok/s. **Le moteur d'événements est 38 % plus rapide que numpy+BLAS** — sans
reports/rapport-inference.md:106:| | mémoire des poids | tok/s (16 threads) |
reports/rapport-inference.md:116:(8,5 tok/s) parce que sa boucle de produit scalaire était limitée par une chaîne
reports/rapport-inference.md:118:11,4 tok/s. La comparaison ci-dessus est celle de deux implémentations soignées.*
reports/rapport-inference.md:144:| activation | événements/token | accord avec la référence | tok/s |
reports/rapport-inference.md:189:1. **Le débit variable reste hors d'atteinte** : 352 M événements par token, tous les
reports/rapport-inference.md:212:| Ve
… [1176 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspecting the flux receiver to confirm the immediate unknown-mode refusal.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "offset": 2240, "limit": 70}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
2240:     }
2241:     let (debut, fin, pos) = (u(6), u(10), u(14));
2242:     let n = u(18) as usize;
2243:     let echelle = f32::from_le_bytes([tete[22], tete[23], tete[24], tete[25]]);
2244:     let mut topk_proj = [0u32; 7];
2245:     for (i, v) in topk_proj.iter_mut().enumerate() { *v = u(39 + i * 4); }
2246:     let act = Act {
2247:         levels: f32::from_le_bytes([tete[26], tete[27], tete[28], tete[29]]),
2248:         thresh: f32::from_le_bytes([tete[30], tete[31], tete[32], tete[33]]),
2249:         topk: u(34),
2250:         renorm: tete[38] != 0,
2251:         topk_proj,
2252:         attn_topk: u(67),
2253:         qk_topk: u(71),
2254:         moe_topk: u(75),
2255:     };
2256:     // Le mode est vérifié AVANT de lire le moindre octet de corps : un mode
2257:     // inconnu se refusait après avoir lu `n × 4` octets et s'être désynchronisé,
2258:     // en disant « mode inconnu » — exact, tardif, et muet sur la cause.
2259:     // Un flux à zéro élément n'est illégitime que là où `n` est une DIMENSION
2260:     // (mode 0) ou un nombre d'ÉTATS (modes 3 et
… [3530 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"TAILLE_TETE\" drave-core/src/main.rs | head -20 && echo \"=== mode4 tests ===\" && grep -n \"fn test\\|#\\[test\\]\" drave-core/src/main.rs | sed -n '1,10p' && echo \"=== count tests ===\" && grep -c \"#\\[test\\]\" drave-c … [159 caractères tronqués]`

  ```
1897:const TAILLE_TETE: usize = 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 1
2048:    let mut t = Vec::with_capacity(TAILLE_TETE);
2065:    assert_eq!(t.len(), TAILLE_TETE,
2066:               "en-tête de flux de {} octets pour {TAILLE_TETE}", t.len());
2169:    Ok((TAILLE_TETE + corps.len(), n))
2186:    Ok(TAILLE_TETE + corps.len())
2220:    Ok(TAILLE_TETE + corps.len())
2226:    let mut tete = [0u8; TAILLE_TETE];
2688:            octets_recus += TAILLE_TETE as u64 + rep.octets_corps as u64;
2757:        octets_recus += TAILLE_TETE as u64 + rep.octets_corps as u64;
4629:        assert_eq!(TAILLE_TETE, 79, "l'en-tête de flux doit faire 79 octets");
4678:        assert_eq!(octets, TAILLE_TETE + 32,
4711:        assert_eq!(t.len(), TAILLE_TETE);
4898:            assert_eq!(tete.len(), TAILLE_TETE);
=== mode4 tests ===
4627:    #[test]
4636:    #[test]
4649:    #[test]
4660:    #[test]
4735:    #[test]
4768:    #[test]
4782:    #[test]
4797:    #[test]
4811:    #[test]
4838:    #[test]
=== count tests ===
drave-core/src/clusters.rs:6
drave-core/src/engine.rs:2
drave-core/src/formats.rs:1
drave-core/src/gguf.rs:10
drave-core/src/gpu.rs:0
drave-core/src/list.rs:5
drave-core/src/main.r
… [106 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Resolving the 17-vs-18 formats question before judging the plan's gate number.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/portes_formats.sh && echo \"=== README autour 340-370 ===\" && sed -n '335,370p' README.md && echo \"=== REPRISE 1095-1115 ===\" && sed -n '1095,1115p' REPRISE.md", "description": "Inspect format gate script and  … [15 caractères tronqués]`

  ```
#!/usr/bin/env bash
# Portes des FORMATS : chaque déquantificateur comparé à libggml, bloc par bloc.
#
#   tools/portes_formats.sh [type ...]
#
# Pourquoi : nos déquantificateurs sont écrits d'après le C de ggml, et les cinq
# premiers essais se sont tous trompés (IQ2_XXS : pas de 8 octets sur `qs` ;
# IQ1_M : échelles lues en premier alors qu'elles sont en DERNIER ; Q2_K : indice
# d'échelle ; Q5_K : bits hauts relus au lieu d'avancés ; Q6_K : quants
# entrelacés au lieu de groupés). Aucun n'a été trouvé par relecture : tous l'ont
# été par comparaison à la bibliothèque. Cette porte rend la comparaison
# reproductible, et refuse de « passer » si le témoin a disparu du disque — un
# test qui saute est un test qui ne dit rien.
#
# La référence est liée à libggml (voir tools/ref_ggml_bloc.c).
set -u
cd "$(dirname "$0")/.."
RACINE=$PWD
MODELES=${DRAVE_MODELES:-/home/stephane/Data13TB/stephane/modeles/gguf}
LLAMA=${DRAVE_LLAMA:-/home/stephane/Data13TB/stephane/GitHub/llama.cpp}
REF=${REF_GGML_BLOC:-/tmp/ref_ggml_bloc}
VERIF=tools/verifier_formats.py
IFS=$'\n'

ok=0; ko=0; abs=0
# libellé | fichier | tenseur | type ggml
BATTERIE=(
  "F32        | $MODELES/codestral-22b-v0.1-q4_k_m.gguf 
… [6709 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Searching the four docs for IQ-format and other to-do claims.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in docs/plan-mode4-lot-listes.md docs/plan-deepseek-v4-flash.md docs/plan-deepseek41-complet.md docs/comparaison-spiking.md; do echo \"=== $f ===\"; grep -n \"IQ\\|MLA\\|multifichiers\\|multi-shards\\|shard\" \"$f\"; done", "de … [58 caractères tronqués]`

  ```
=== docs/plan-mode4-lot-listes.md ===
=== docs/plan-deepseek-v4-flash.md ===
4:disque mécanique (`/home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/`,
5:3 shards, 86,9 Go). Le NVMe ne sert plus qu'aux artefacts que nous produisons. Le moteur **lit déjà ses métadonnées** : `--plan` affiche
17:récupéré, en quantification **UD-IQ1_M** : la plus petite publiée, 86,9 Go en trois
18:shards — les autres vont de ~120 Go (IQ2) à plusieurs centaines de Go, et le dépôt
27:| shard 1 (5,3 Mo) | ✅ l'**architecture** (`--plan` : « deepseek4, 43 couches, 256 experts (top-6) ») et le **tokenizer** : 129 280 jetons, aller-retour texte→jetons→texte **identique** sur `data/wikitext2_test.txt` |
28:| shard 2 (49,97 Go) | ✅ **784 tenseurs** lisibles avec leurs noms, formes et quantifications (`Q4_K output.weight [129280, 4096]`, `F32 output_hc_base.weight [4]`…) — mais **sans métadonnées** : « 0 couches », architecture « ? » |
29:| shard 3 (36,92 Go) | ✅ téléchargé (mêmes propriétés que le shard 2) |
37:1. **Le GGUF est découpé en shards.** Le moteur ouvre UN fichier
38:   (`Gguf::open(path)`) ; le shard 1 ne contient **aucun tenseur** (« 0 tenseurs »)
40:   **lecteur multi-fichie
… [1443 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking the llama.cpp V4-Flash reference figures cited by the plan.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"1 325\\|11,737\\|11.737\\|deepseek4\" reports/rapport-routage-experts.md | head -20 && echo \"=== trace compacite 66,4 ===\" && grep -rn \"66,4\\|66.4\" reports/rapport-compacite-trace.md docs/*.md | head -10", "description … [54 caractères tronqués]`

  ```
21:| DeepSeek-V4-Flash | `deepseek4` | **4 — racine de softplus** | softmax ✗ |
22:| DeepSeek-V4.1-Flash | `deepseek41` | *(dans le JSON `config`)* | **dense : `n_expert = 0`** ✗ |
=== trace compacite 66,4 ===
docs/plan-deepseek41-complet.md:17:| **listes d'activation** | `(indice, valeur)` par vecteur, encodage DRVF v1/v2/v3 ; v2 = **3 octets par neurone actif** | trace dense 512 jetons : 66,4 Mo, rejeu **identique** (19,3885) |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"V4.1-Flash-Q2\\|V4.1\" reports/rapport-routage-experts.md | head -20 && echo \"=== hc tensors ===\" && grep -rn \"output_hc\" reports/*.md drave-core/src/*.rs | head -20", "description": "Check V4.1 Q2 provenance facts"}`

  ```
22:| DeepSeek-V4.1-Flash | `deepseek41` | *(dans le JSON `config`)* | **dense : `n_expert = 0`** ✗ |
27:  V4.1, **2,5** pour GLM-5.3, **2,827** pour Kimi-K2.7. C'est un facteur
35:Enfin, V4.1-Flash-Q2 ne déclare ses experts que sous les noms d'origine de
53:| `racine de softplus` | `√log(1+eˣ)` → top-k → renormalisation | V4-Flash, V4.1 |
93:| DeepSeek-V4.1-Flash | 755 G | les trois + engram + sortie à rang faible |
=== hc tensors ===
  ```

### 🤖 Assistant

⏵ Locating the source of the 1 325 tensors / NLL 11,737 reference figures.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"11,737\\|11.737\\|1325\\|1 325\" --include=*.md . 2>/dev/null | grep -v \"journal/\" | head -20; echo \"=== journal ===\"; grep -rn \"11,737\\|1 325\" journal/*.md 2>/dev/null | head -10", "description": "Search repo for V … [27 caractères tronqués]`

  ```
./docs/plan-deepseek41-complet.md:80:2. **llama.cpp exécute V4-Flash** (`deepseek4`) : 1 325 tenseurs chargés,
./docs/plan-deepseek41-complet.md:81:   NLL 11,737 sur un jeton froid. V4-Flash porte **les mêmes mécanismes** en
./REPRISE.md:1181:2. **llama.cpp exécute V4-Flash** (`deepseek4`, 1 325 tenseurs chargés,
./REPRISE.md:1182:   NLL 11,737 sur un jeton froid) — c'est donc **V4-Flash le banc d'essai**, avec
=== journal ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls *.md && echo \"=== REPRISE head ===\" && sed -n '1,80p' REPRISE.md", "description": "List root docs and read REPRISE head"}`

  ```
Qtrinet-bootstrap.md
README.md
REPRISE.md
=== REPRISE head ===
# Reprise — état du projet et mode d'emploi pour une nouvelle session

> Rédigé à la fin d'une session longue. Tout ce qui suit est **mesuré**, pas
> déduit. Les valeurs de perplexité sont des **références de non-régression** :
> si une modification les change, c'est qu'elle a changé le calcul.
>
> **Nom** : le projet s'appelle **Drave** (binaire `drave`, paquet `drave-core`,
> variables `DRAVE_*`, histoire du renommage dans `docs/histoire.md`). Le dossier
> de travail, lui, s'appelle encore `Qtrinet` — les chemins ci-dessous sont ceux
> qui existent.

---

## 1. En une phrase

`drave-core` est un moteur d'inférence Rust (~13 758 lignes, `std` seul) qui
charge les GGUF **en place** (aucune copie, aucune requantification), exécute les
projections soit en listes d'événements, soit en produit scalaire dense, gère les
MoE, tient une conversation, et déporte au GPU ce qui y gagne. Il fait tourner du
0,5 B au 120 B sur le CPU de cette machine.

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo build --release
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --infer --chat --flux --pro
… [3278 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking how the repo currently words MLA validation status.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"NON VALIDÉE\\|non validée\\|position 2\\|0,999024\\|corrélation 0,999\" --include=*.md --include=*.rs . 2>/dev/null | grep -v \"journal/\" | head -30", "description": "Grep MLA validation wording"}`

  ```
./reports/rapport-logits-gpu-vs-cpu.md:48:maximum global (1,3708 nat, position 284) est l'une d'elles — mais seules 3 des 14
./reports/rapport-mla-experts.md:112:| corrélation des logits (pos. 0) | **0,999024** |
./reports/rapport-mla-experts.md:172:### La validation s'arrête à la position 2, et c'est mesuré
./reports/rapport-execution-v41.md:49:faible** validée contre llama.cpp sur GLM-5.3 (corrélation 0,999024).
./docs/plan-deepseek41-complet.md:72:| MLA à rang faible | **validée** contre llama.cpp sur GLM-5.3 (corrélation 0,999024) |
./REPRISE.md:112:un à un à llama.cpp** sur les mêmes identifiants (corrélation 0,999976 au premier
./REPRISE.md:1035:forme. Après correction : **corrélation 0,999024**, **top-1 3/3**, perplexité
./REPRISE.md:1040:position 2, puis **+4,070 à la position 3** et redescend ensuite (perplexité
./REPRISE.md:1069:| GLM-5.3 (glm-dsa) | 754 G | **oui**, et validé contre llama.cpp (corrélation 0,999) |
./REPRISE.md:1113:   `wk_b` (corrélation −0,04 → **0,999024**) et l'indexation de tranche dans le
./drave-core/src/model.rs:138:corrélation des logits 0,999024, top-1 3/3 (voir reports/rapport-mla-experts.md).");
./README.md:375:| **GLM-5.3** (79 couches MLA, 2
… [236 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying gpt-oss expert count/top-k to test a claim in the v4-flash doc.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"top-4\\|top 4\\|n_expert_used\\|experts par jeton\\|top-8\" --include=*.md README.md REPRISE.md reports/rapport-localite-activation.md reports/rapport-routage-experts.md | head -25", "description": "Check gpt-oss top-k exp … [19 caractères tronqués]`

  ```
README.md:373:| **Qwen3-30B-A3B** (MoE 128 experts, top-8) | Q4_K_M | **7,61** | 5,4 tok/s | **17,7 Go** |
REPRISE.md:501:les décale de **0,038 nat** sur gpt-oss (MxFP4, 128 experts top-8), avec le même
REPRISE.md:504:c'est le **routage des experts** — un top-8 est une opération discrète, qu'un écart
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"top-8\\|top-4\\|128 experts\\|256 experts\\|384 experts\" README.md | head -25 && echo \"=== config output ===\" && grep -rn \"experts par jeton\\|top-k\\|topk\" drave-core/src/main.rs | grep -i \"expert\" | head -10", "de … [52 caractères tronqués]`

  ```
373:| **Qwen3-30B-A3B** (MoE 128 experts, top-8) | Q4_K_M | **7,61** | 5,4 tok/s | **17,7 Go** |
375:| **GLM-5.3** (79 couches MLA, 256 experts) | IQ1_S/IQ3_XXS/IQ4_XS | pos. 0 : corrélation **0,999024** · au-delà, l'écart croît (4 nats à la pos. 3) | 190 s/jeton | 90 Go |
376:| **Kimi-K2.7** (61 couches MLA, 384 experts) | IQ1_M/IQ2_XXS/IQ3_XXS | non validé | 73 s/jeton | 1 026 G mmap |
=== config output ===
1768:        // Les experts relus par jeton : top-k × couches. On lit le top-k déclaré,
1772:        let go = topk * couches * mo_expert / 1000.0;
  ```

### 🤖 Assistant

⏵ Checking the actual gpt-oss expert top-k from its GGUF metadata.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la drave-core/target/release/drave 2>/dev/null; M=/home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf; ls -la \"$M\" 2>/dev/null | head -3", "description": "Check binary and gpt-oss model presence"}`

  ```
-rwxr-xr-x. 2 stephane stephane 2118960  2 oct 08:51 drave-core/target/release/drave
-rw-r--r--. 1 stephane stephane 63387346208 24 sep 13:14 /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 ./drave-core/target/release/drave /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf --config 2>&1 | head -30; echo \"exit=$?\"", "description": "Run drave --config on gpt-oss"}`

  ```
modèle        : /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf
architecture  : gpt-oss
couches       : 36 · cachés 2880
experts       : 128 par couche, 4 par jeton · FFN expert 2880
routage       : top-k brut + softmax (source : défaut du moteur) · renormalisation non · échelle aucune
calculable    : NON — il manque : attention V4 : dé-rotation de sortie et puits par tête
exit=0
  ```

### 🤖 Assistant

⏵ Checking the spiking doc for the crossover/density framing and energy sourcing.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"densit\\|22 %\\|croisement\\|push\\|pull\\|grappe\\|machine\\|cluster\\|répart\" docs/comparaison-spiking.md; echo \"--- bilan energies 40-60 ---\"; sed -n '38,60p' reports/bilan-multi-materiel.md; sed -n '105,120p' reports … [88 caractères tronqués]`

  ```
--- bilan energies 40-60 ---
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

1. **Les listes sont portables.** Les mêmes octets nourrissent le CPU, le FPGA et
même machine. Il reste 2,8× de marge avant la limite mémoire (10,4 Go/s utilisés
sur 28,7). C'est l'implémentation l
… [746 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying I32 coverage and the 66.4 Mo trace figure.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== I32 ===\" && grep -rn \"I32\\|GGML_I32\" drave-core/src/gguf.rs tools/verifier_formats.py tools/portes_formats.sh | head -15 && echo \"=== 66,4 / trace 512 ===\" && grep -rn \"compacité\\|Mo\\b\" reports/rapport-compacite- … [80 caractères tronqués]`

  ```
=== I32 ===
drave-core/src/gguf.rs:181:    U8(u8), I8(i8), U16(u16), I16(i16), U32(u32), I32(i32),
drave-core/src/gguf.rs:190:            Meta::I32(v) => Some(*v as u64),
drave-core/src/gguf.rs:293:/// I32 : entiers signés 32 bits, sans quantification. Utilisé par la table de
drave-core/src/gguf.rs:295:pub const GGML_I32: u32 = 26;
drave-core/src/gguf.rs:364:            5 => Meta::I32(self.i32()),
drave-core/src/gguf.rs:767:            24 => "I8", 25 => "I16", 26 => "I32", 27 => "I64", 28 => "F64",
drave-core/src/gguf.rs:1225:    /// Lit un tenseur **I32** (entiers 32 bits signés), tel quel.
drave-core/src/gguf.rs:1234:        assert_eq!(t.ttype, GGML_I32, "tenseur {name} : type {} au lieu d'I32",
=== 66,4 / trace 512 ===
61:Ce sont les deux traces citées par le projet (« 132 Mo pour 512 jetons, 53 Mo en
82:## 3. Le tableau — trace creuse (53 Mo, 256 jetons)
98:été vérifié en compressant les 53 Mo entiers.
109:  payés sur 35 Mo). C'est le poste le plus gros **et** le moins coûteux à
116:  échelles : le gain net est de 5,94 Mo (−22 % de plus), pour une erreur RMS de
117:  **0,077 % du max de la liste**. Les échelles en f16 reprennent encore 1,38 Mo
126:53 Mo : ce n'est pas un levier
… [887 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Investigating the 66.4 Mo trace figure against the trace report.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"66,4 Mo\\|66.4 Mo\\|66,4\\|66.4\" journal/ 2>/dev/null | head -10; echo \"=== compacite 55-100 ===\"; sed -n '40,100p' reports/rapport-compacite-trace.md", "description": "Search journal and read trace report section"}`

  ```
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:11922:=== perplexité 24.8995 sur 2040 tokens (722856664851 événements, 366.8 s) ===
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:15686:=== perplexité 24.8995 sur 2040 tokens (722856664851 événements, 150.3 s) ===
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:15843:=== perplexité 24.8995 sur 2040 tokens (722856664851 événements, 155.8 s) ===
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:16426:=== perplexité 24.8995 sur 2040 tokens (722856664851 événements, 157.8 s) ===
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:18681:=== perplexité 24.8995 sur 2040 tokens (722856664851 événements, 141.6 s) ===
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:23096:  référence : (3.1458443837458254e-18, 1.1418320111981964e-17, 2.5181688781950482e-19, -1.141701316661413e-17, -6.42446035479315e-17, 3.3701941270179832e-21)
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:23097:  calculé   : [0.007151, -0.039173, 0.005596, -0.016614, 0.012514, 0.007462]
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:23124:     calc : [0.
… [3967 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Searching for any documented v2 size of the dense 512-token trace.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"008 776\\|008776\\|66 0\\|66,0 Mo\\|flux_f32\" reports/*.md REPRISE.md README.md 2>/dev/null | head -20; echo \"=== v2 3 octets ===\"; grep -rn \"3 octets par neurone\\|3 o/actif\\|3,04\" reports/*.md | head -10", "descrip … [42 caractères tronqués]`

  ```
reports/rapport-coherence-docs.md:96:| 40 | `docs/format-flux.md:47`, `reports/rapport-compacite-trace.md:8` | 24 576 listes · 22 008 776 actifs | conforme au commit `6b3b53f` et au tableau du rapport ; non recompté ici (ré-encodage Python interrompu au-delà de 60 s) | OK (source) |
reports/rapport-coherence-docs.md:226:| OK | **17** | formats des modes 2 et 3 · `flux_brut` · `hôte:port` · trace dense 66 370 408 o (fichier réellement relu) · 66 370 406 hors sentinelle · 24 576 listes / 22 008 776 actifs (source) · 918 ko · 24,90 / 25,00 · +9,1 % · rejeu 17,4294 · corrections de l'audit drapeaux · table `DRAVE_*` de REPRISE · `profil_flux.py` · outils FPGA · `flux_codec.py` lit la v3 · `DRAVE_TRACE_BLOCS` documentée |
reports/rapport-compacite-trace.md:8:> mêmes 24 576 listes et 22 008 776 neurones actifs. Le rejeu annonce maintenant
reports/rapport-compacite-trace.md:59:| `/tmp/flux_f32.bin` | même modèle, 512 jetons, `--abits 16` (rien n'est seuillé) | **132 396 736 o** | 22 008 776 | 99,9 % |
reports/rapport-compacite-trace.md:149:1. **Aucun échappement** sur 22 008 776 indices : quand la liste est presque
=== v2 3 octets ===
reports/rapport-attribution-kv.md:14:| cache int8 comp
… [1308 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Testing current multi-file metadata reading on the V4-Flash shards.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && M=/home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M; ls \"$M\" 2>/dev/null | head; timeout 300 ./drave-core/target/release/drave \"$M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf\" --config 2>&1 | head -25",  … [48 caractères tronqués]`

  ```
DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf
DeepSeek-V4-Flash-UD-IQ1_M-00002-of-00003.gguf
DeepSeek-V4-Flash-UD-IQ1_M-00002-of-00003.gguf.etat.json
DeepSeek-V4-Flash-UD-IQ1_M-00002-of-00003.gguf.part5
DeepSeek-V4-Flash-UD-IQ1_M-00003-of-00003.gguf
modèle        : /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf
architecture  : deepseek4
couches       : 43 · cachés 4096
experts       : 256 par couche, 6 par jeton · FFN expert 2048
routage       : racine de softplus (source : expert_gating_func) · renormalisation oui · échelle 1.500
routage table : 3/43 premières couches par `ffn_gate_tid2eid`
[mla] attention MLA à rang faible : cache LATENT (c_kv + k_rope), pas de fenêtre glissante ni de YaRN sur ce chemin. Validée contre llama.cpp sur GLM-5.3 : corrélation des logits 0,999024, top-1 3/3 (voir reports/rapport-mla-experts.md).
calculable    : NON — il manque : hyper-connexions (hc_attn_fn, hc_ffn_fn, hc_mult), projection de sortie à rang faible groupée (attn_output_a/attn_output_b, o_groups), attention V4 : dé-rotation de sortie et puits par tête
  ```

### 🤖 Assistant

⏵ Sanity-checking --config on a known-calculable model before reporting the gpt-oss anomaly.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --config 2>&1 | head -12; echo \"=== V4.1 file exists? ===\"; ls -la /home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf 2>/dev/null; ls /home … [131 caractères tronqués]`

  ```
modèle        : models/Qwen2.5-0.5B-Q8_0.gguf
architecture  : qwen2
couches       : 24 · cachés 896
experts       : 0 par couche, 0 par jeton · FFN expert 0
calculable    : oui (passe avant implémentée)
=== V4.1 file exists? ===
-rw-r--r--. 1 stephane stephane 365713686528  1 oct 22:59 /home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf
DeepSeek-V4.1-Flash-Q2
  ```

### 🤖 Assistant

⏵ Extracting exact line texts for the citations.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for spec in \"docs/plan-deepseek-v4-flash.md:13\" \"docs/plan-deepseek-v4-flash.md:31\" \"docs/plan-deepseek-v4-flash.md:32\" \"docs/plan-deepseek-v4-flash.md:40\" \"docs/plan-deepseek-v4-flash.md:63\" \"docs/plan-deepseek-v4-flash.m … [965 caractères tronqués]`

  ```
docs/plan-deepseek-v4-flash.md:13 | | **DeepSeek-V4.1-Flash** | modèle d'API ([api-docs](https://api-docs.deepseek.com/news/news260910/), [deepseek.com](https://www.deepseek.com/news/deepseek-v4-1-flash/)) | **non** — aucun GGUF publié |
docs/plan-deepseek-v4-flash.md:31 | Autrement dit : le lecteur GGUF sait déjà tout lire, **séparément**. Ce qui manque
docs/plan-deepseek-v4-flash.md:32 | est le lien entre les deux — les métadonnées d'un fichier, les tenseurs de trois —
docs/plan-deepseek-v4-flash.md:40 |    **lecteur multi-fichiers** : ouvrir les N shards, résoudre un nom de tenseur dans
docs/plan-deepseek-v4-flash.md:63 | | 1 | lecteur GGUF **multi-shards** | les 3 shards ouverts, un tenseur résolu depuis le shard 2, le placement total affiché |
docs/plan-deepseek-v4-flash.md:47 |    * l'**attention** (V4 utilise une attention latente de type MLA — le moteur en a
docs/plan-deepseek-v4-flash.md:48 |      une implémentation validée sur un modèle synthétique, `--banc-mla`, écart
docs/plan-deepseek-v4-flash.md:50 |    * le **MoE 256 experts / top-6** (le moteur en gère 128/top-8 sur gpt-oss et
docs/plan-deepseek-v4-flash.md:51 |      Qwen3) ;
docs/plan-deepseek-v4-flash.md:61 | | # 
… [2127 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking V4.1's tensor type inventory for the I32 verification claim.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 180 ./drave-core/target/release/drave /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4.1-Flash-Q2/DeepSeek-V4.1-Flash-Q2.gguf --tensors 2>&1 | tail -8; echo \"---types---\"; timeout 180 ./drave-core/target/release/dr … [247 caractères tronqués]`

  ```
Q8_0     blk.39.ffn_gate_shexp.weight           [2304, 5120] · 11.8 M poids · fichier 0
  IQ2_XXS  blk.39.ffn_gate_exps.weight            [384, 2304, 5120] · 4529.8 M poids · fichier 0
  Q8_0     blk.39.ffn_up_shexp.weight             [2304, 5120] · 11.8 M poids · fichier 0
  IQ2_XXS  blk.39.ffn_up_exps.weight              [384, 2304, 5120] · 4529.8 M poids · fichier 0
  Q8_0     blk.39.ffn_down_shexp.weight           [5120, 2304] · 11.8 M poids · fichier 0
  Q2_K     blk.39.ffn_down_exps.weight            [384, 5120, 2304] · 4529.8 M poids · fichier 0
  I8       blk.1.engram_embd.weight               [384006168, 264] · 101377.6 M poids · fichier 0
  I8       blk.14.engram_embd.weight              [384016682, 264] · 101380.4 M poids · fichier 0
---types---
  ```

### 🤖 Assistant

⏵ Counting all tensor types in the V4.1 file.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 180 ./drave-core/target/release/drave /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4.1-Flash-Q2/DeepSeek-V4.1-Flash-Q2.gguf --tensors 2>&1 > /tmp/v41_tensors.txt; wc -l /tmp/v41_tensors.txt; awk '{print $1}' /tmp/v … [189 caractères tronqués]`

  ```
1048 /tmp/v41_tensors.txt
    493 F32
    321 Q8_0
    110 F16
     80 IQ2_XXS
     40 Q2_K
      2 I8
      1 deepseek41
      1 ·
=== I32 lines ===
3:  F16      token_embd.weight                      [129280, 5120] · 661.9 M poids · fichier 0
4:  F32      output_norm.weight                     [5120] · 0.0 M poids · fichier 0
6:  F16      blk.0.hc_attn_fn.weight                [24, 20480] · 0.5 M poids · fichier 0
7:  F32      blk.0.hc_attn_base.weight              [24] · 0.0 M poids · fichier 0
8:  F32      blk.0.hc_attn_scale.weight             [3] · 0.0 M poids · fichier 0
9:  F32      blk.0.attn_norm.weight                 [5120] · 0.0 M poids · fichier 0
10:  F16      blk.0.hc_ffn_fn.weight                 [24, 20480] · 0.5 M poids · fichier 0
11:  F32      blk.0.hc_ffn_base.weight               [24] · 0.0 M poids · fichier 0
12:  F32      blk.0.hc_ffn_scale.weight              [3] · 0.0 M poids · fichier 0
13:  F32      blk.0.ffn_norm.weight                  [5120] · 0.0 M poids · fichier 0
  ```

### 🤖 Assistant

⏵ Comparing the two V4.1 copies to confirm the real tensor types.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -3 /tmp/v41_tensors.txt; ls -la /home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4.1-Flash-Q2/DeepSeek-V4.1-Flash-Q2.gguf 2>/dev/null; echo \"=== FastNVMe … [361 caractères tronqués]`

  ```
deepseek41 · 1 fichiers · 1046 tenseurs · 365.70 Go de poids · en-têtes lus en 62.720311ms
 · vocab_size 129280
  F16      token_embd.weight                      [129280, 5120] · 661.9 M poids · fichier 0
-rw-r--r--. 1 stephane stephane 365713686528  1 oct 10:26 /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4.1-Flash-Q2/DeepSeek-V4.1-Flash-Q2.gguf
-rw-r--r--. 1 stephane stephane 365713686528  1 oct 22:59 /home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf
=== FastNVMe copy types ===
    493 F32
    321 Q8_0
    110 F16
     80 IQ2_XXS
     40 Q2_K
      2 I8
      1 deepseek41
      1 ·
=== I8/I32 grep ===
1047:  I8       blk.1.engram_embd.weight               [384006168, 264] · 101377.6 M poids · fichier 0
1048:  I8       blk.14.engram_embd.weight              [384016682, 264] · 101380.4 M poids · fichier 0
  ```

### 🤖 Assistant

⏵ Inspecting the architecture check that flags gpt-oss as non-calculable.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"dé-rotation de sortie\\|manque : \\|il manque\" drave-core/src/*.rs | head -20", "description": "Locate architecture check message"}`

  ```
drave-core/src/main.rs:1689:        println!("calculable    : NON — il manque : {}", manques.join(", "));
drave-core/src/model.rs:126:        manques.push("attention V4 : dé-rotation de sortie et puits par tête");
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 60, "offset": 95}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
95:         manques.push("hyper-connexions (hc_attn_fn, hc_ffn_fn, hc_mult)");
96:     }
97:     // Attention par index (DSA) : l'indexeur choisit les clés gardées. Il ne
98:     // sert QUE si la séquence dépasse `index_topk` — en deçà, llama.cpp garde
99:     // toutes les clés et l'indexeur n'est pas appelé. On refuse donc seulement
100:     // les contextes où il changerait le résultat.
101:     if quelque_part("indexer.") {
102:         let topk = g.cfg("index_topk").and_then(|m| m.as_u64()).unwrap_or(0) as usize;
103:         if topk == 0 || ctx > topk {
104:             manques.push("attention par index appris (indexer) au-delà de index_topk");
105:         }
106:     }
107:     // L'engram est une table mmappée que le moteur sait ADRESSER (`--sonder-engram`)
108:     // mais pas encore CALCULER. llama.cpp l'ignore aussi : ce n'est donc pas un
109:     // obstacle à une exécution comparable à la sienne, et le dire évite de
110:     // compter un manque qui n'en est pas un pour la validation croisée.
111:     if quelque_part("engram_embd.weight") || quelque_part("e
… [2795 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking whether the engine implements attention sinks for gpt-oss.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"sinks\\|puits\" drave-core/src/model.rs | head -20; echo \"=== main.rs ===\"; grep -rn \"sinks\" drave-core/src/main.rs | head -10", "description": "Grep attention sinks implementation"}`

  ```
120:    // les sinks sont des logits appris par tête, et surtout `compress_ratios`
125:    if quelque_part("attn_derope") || a("blk.0.attn_sinks.weight") {
126:        manques.push("attention V4 : dé-rotation de sortie et puits par tête");
852:    pub sinks: Option<Vec<f32>>,
1488:    /// clés, plus `attn_sinks` jetons puits au début de la séquence.
1517:    pub attn_sinks: usize,
1535:    /// Nombre de couches dont les puits appris ont été trouvés (diagnostic).
1536:    pub sinks_vus: usize,
2317:                sinks: if g.tensor(&p("attn_sinks.weight")).is_some() {
2318:                    Some(g.dequant(&p("attn_sinks.weight"))) } else { None },
2378:        let sinks_vus = layers.iter().filter(|l| l.sinks.is_some()).count();
2409:        println!("[config] puits appris sur {sinks_vus}/{n_layer} couches · n_rot {} · ffn {} · experts {}{}",
2620:            attn_sinks: if fenetre > 0 { 0 } else { 4 },
2627:            sinks_vus, kv_gpu, attn_gpu_part: Vec::new(),
3456:                    let puits: Option<Vec<f32>> = lay.sinks.as_ref()
3468:                                           puits.as_deref(), nsplit, part, sortie) {
3489:                            let puits = lay.sinks.
… [1012 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying the absence of cluster/machine/analysis wording in three docs.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in docs/plan-deepseek-v4-flash.md docs/plan-mode4-lot-listes.md docs/comparaison-spiking.md; do echo \"=== $f ===\"; grep -n -i \"cluster\\|grappe\\|machine\\|répart\\|adapter l'architecture\\|analyser\\|journal\" \"$f\" | head … [82 caractères tronqués]`

  ```
=== docs/plan-deepseek-v4-flash.md ===
80:Le journal est `/tmp/telechargement_lourds.log`.
=== docs/plan-mode4-lot-listes.md ===
234:   `logits_lot`, avec **le même découpage** que le chemin réparti.
=== docs/comparaison-spiking.md ===
  ```

### 🤖 Assistant

⏵ Confirming README line numbers for the 18-format claim.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Le moteur lit\\|Q4_K, Q6_K\\|formats × 2 blocs\" README.md | head; echo \"=== analyse tools exist ===\"; ls tools/ | grep -E \"^(profil_flux|analyse_flux|diff_flux|trace_compacite|analyse_empreinte|aiguille)\\.py$\"", "desc … [54 caractères tronqués]`

  ```
352:Le moteur lit **Q4_K, Q6_K, Q4_0, Q5_0, Q5_1, Q8_0, Q2_K, Q3_K, Q5_K, MXFP4,
364:tools/portes_formats.sh                   # 17 formats × 2 blocs, contre libggml
=== analyse tools exist ===
aiguille.py
analyse_empreinte.py
analyse_flux.py
diff_flux.py
profil_flux.py
trace_compacite.py
  ```

### 🤖 Assistant

⏵ Writing the adversarial report with exact citations and minimal corrections.

# Rapport de relecture adverse — 4 documents

Faits de référence vérifiés dans l'arbre (02/10) : `VERSION_FLUX = 5`, `MODE_LOT_LISTES = 4` (main.rs:1862, 1886) ; refus des modes inconnus après l'en-tête (main.rs:2256-2275) ; lecteur multi-fichiers `Gguf::open_multi` (gguf.rs:447) et métadonnées résolues depuis le shard 1 (`drave …-00001-of-00003.gguf --config` → « deepseek4, 43 couches, 256 experts, 6 par jeton ») ; MLA à rang faible faite, validation arrêtée à la position 2 (rapport-mla-experts.md §7) ; 48 `#[test]` ; 18 formats lisibles (README.md:352), 17 à la porte (README.md:364) ; 4 routages (tools/portes.sh:88-91) ; gpt-oss = 128 experts **top-4** (`--config`) ; porte gpt-oss **15,6017** (rapport-routage-experts.md:66) ; 1 046 tenseurs / 365,70 Go (run `--tensors` : 62,7 ms), types réels F32 493, Q8_0 321, F16 110, IQ2_XXS 80, Q2_K 40, **I8 2** — aucun I32.

| fichier:ligne | citation exacte (≤ 25 mots) | problème | correction minimale proposée (texte de remplacement exact) | gravité |
|---|---|---|---|---|
| docs/plan-deepseek-v4-flash.md:13 | `**non** — aucun GGUF publié` | Faux : `DeepSeek-V4.1-Flash-Q2.gguf` (365 713 686 528 o) existe et est mesuré (rapport-execution-v41.md ; plan41 §3.1) | `**oui** — GGUF Q2 communautaire (365,71 Go), incomplet (`output_hc_*` absents) : voir `plan-deepseek41-complet.md` §3.2` | élevée |
| docs/plan-deepseek-v4-flash.md:32 | `est le lien entre les deux — les métadonnées d'un fichier, les tenseurs de trois —` | Décrit comme manquant ce qui est fait : `--config` sur le shard 1 lit l'architecture, le tokenizer et les 1 328 tenseurs (rapport-lecteur-multifichiers.md ; vérifié) | `est fait : `Gguf::open_multi` résout les métadonnées et les tenseurs des trois shards (`reports/rapport-lecteur-multifichiers.md`) —` | élevée |
| docs/plan-deepseek-v4-flash.md:40 | `**lecteur multi-fichiers** : ouvrir les N shards, résoudre un nom de tenseur dans` | La suite « C'est le premier chantier » (l.42) est périmée : fait le 01/10 (gguf.rs:447, rapport-lecteur-multifichiers.md) | `**lecteur multi-fichiers** : **fait** (`Gguf::open_multi`, `reports/rapport-lecteur-multifichiers.md`) — ouvrir les N shards, résoudre un nom de tenseur dans` | moyenne |
| docs/plan-deepseek-v4-flash.md:63 | `| 1 | lecteur GGUF **multi-shards** | les 3 shards ouverts, un tenseur résolu depuis le shard 2, le placement total affiché |` | Étape 1 du plan déjà satisfaite (3 shards, 1 328 tenseurs, 86,90 Go annoncés = 86,90 Go sur disque) | `| 1 | ~~lecteur GGUF multi-shards~~ **fait** | 3 shards ouverts, 1 328 tenseurs, 86,90 Go (`reports/rapport-lecteur-multifichiers.md`) |` | moyenne |
| docs/plan-deepseek-v4-flash.md:47 | `* l'**attention** (V4 utilise une attention latente de type MLA — le moteur en a` | Présenté comme à couvrir ; la MLA à rang faible est faite (rapport-mla-experts.md §2), et la liste omet ce qui bloque V4-Flash (`--config` : hyper-connexions, sortie à rang faible, dé-rotation/puits) | `* l'**attention** : MLA à rang faible **faite** (`reports/rapport-mla-experts.md`) ; restent les hyper-connexions, la sortie à rang faible groupée et la dé-rotation/puits (`--config` les nomme) ;` | élevée |
| docs/plan-deepseek-v4-flash.md:50 | `* le **MoE 256 experts / top-6** (le moteur en gère 128/top-8 sur gpt-oss et` | gpt-oss est 128 experts **top-4**, pas top-8 : `drave …gpt-oss-120b-MXFP4.gguf --config` affiche « 128 par couche, 4 par jeton » | `* le **MoE 256 experts / top-6** (le moteur en gère 128/top-4 sur gpt-oss et 128/top-8 sur` | moyenne |
| docs/plan-deepseek-v4-flash.md:69 | `## Reprendre le téléchargement` | Le fichier de 365,7 Go est téléchargé et mesuré (`rapport-execution-v41.md`) ; « Le NVMe ne sert plus qu'aux artefacts » (l.5) est faux depuis | `## Téléchargement terminé (365,71 Go, mesuré le 02/10 — `reports/rapport-execution-v41.md`)` | moyenne |
| docs/plan-deepseek-v4-flash.md:61 | `| # | étape | critère de succès |` | Le plan ne comporte ni **grappes/machines** ni **lecture des flux pour adapter l'architecture** (dimensions du plan courant, plan41 P6) | ajouter la ligne : `| 6 | **grappes + `--ppl-reparti`** (deux processus, voire deux machines) | mêmes listes, même perplexité qu'un nœud unique — `plan-deepseek41-complet.md` P6 |` | moyenne |
| docs/plan-mode4-lot-listes.md:5 | `Ce document est la spécification à implémenter ; aucun` | Contredit l'état l.3 (« ÉCRIT, mesuré et relu ») et le code : mode 4 implémenté, testé, mesuré (main.rs:1886 ; rapport-mode4-lot-listes.md) ; §8 (l.408) se lit comme un reste-à-faire | `Ce document reste la référence de conception ; l'implémentation est faite, mesurée et relue (`reports/rapport-mode4-lot-listes.md`) ; aucun` | élevée |
| docs/plan-mode4-lot-listes.md:7 | `> `docs/format-flux.md` (protocole v4, modes 0–3) et `docs/plan-prefill-reparti.md`` | `docs/format-flux.md` documente désormais le protocole **v5**, modes 0–4 (format-flux.md:84-92) | `> `docs/format-flux.md` (protocole v5, modes 0–4) et `docs/plan-prefill-reparti.md`` | moyenne |
| docs/plan-mode4-lot-listes.md:172 | `**Durcissement à faire dans le même passage** (indépendant du mode 4, mais c'est` | Fait : mode inconnu refusé juste après l'en-tête, avant tout octet de corps (main.rs:2256-2275) | `**Durcissement fait dans le même passage** (indépendant du mode 4, mais c'était` | moyenne |
| docs/plan-mode4-lot-listes.md:238 | `repli silencieux. Le message actuel « mode 4 non écrit » (main.rs:1987) doit` | Le message n'existe plus : `--lot > 1 --flux-blocs` produit le mode 4 (main.rs:2575-2578, `envoyer_lot_listes`) | `repli silencieux. Le message « mode 4 non écrit » a été remplacé par le branchement mode 4 (`main.rs:2575`) :` | moyenne |
| docs/plan-mode4-lot-listes.md:293 | `### 6.1 Commande exacte (localhost, Qwen2.5-0.5B, 12 couches par nœud)` | La seule vérification est locale ; le mot « machine » n'apparaît nulle part alors que c'est le transport des grappes (vision §3-4) | `### 6.1 Commande exacte (localhost ; la même campagne reste à faire entre deux machines, `docs/colab-reparti.md`)` | faible |
| docs/plan-mode4-lot-listes.md:17 | `ni au cache KV, ni à la norme finale : il s'arrête au transport.` | Rien ne dit que le flux transporté est aussi le journal que relisent les outils pour analyser/adapter l'architecture (vision §2) | `ni au cache KV, ni à la norme finale : il s'arrête au transport — le flux transporté est aussi le journal que relisent les outils d'analyse (`docs/vision.md` §2).` | faible |
| docs/plan-deepseek41-complet.md:72 | `| MLA à rang faible | **validée** contre llama.cpp sur GLM-5.3 (corrélation 0,999024) |` | Surestimé : la validation s'arrête à la position 2, +4,070 nat d'écart à la position 3 (rapport-mla-experts.md:172-178) | `| MLA à rang faible | **validée à la position 0** contre llama.cpp sur GLM-5.3 (corrélation 0,999024 ; l'écart croît ensuite — `reports/rapport-mla-experts.md` §7) |` | élevée |
| docs/plan-deepseek41-complet.md:71 | `| formats | IQ2_XXS, Q2_K, Q8_0, F16, F32, I32 — **vérifiés contre libggml** |` | Le fichier V4.1 ne contient **aucun I32** ; ses types sont F32/Q8_0/F16/IQ2_XXS/Q2_K et **I8** (2 tenseurs engram, `--tensors` sur les deux copies) | `| formats | IQ2_XXS, Q2_K, Q8_0, F16, F32, I8 (engram) — déquantificateurs vérifiés contre libggml |` | moyenne |
| docs/plan-deepseek41-complet.md:201 | `17 formats, 4 routages).` | Divergence : 18 formats **lisibles** (README.md:352), 17 est le nombre **vérifié par la porte** (README.md:364) | `18 formats lisibles (17 vérifiés à la porte), 4 routages).` | faible |
| docs/plan-deepseek41-complet.md:200 | `4. les portes du dépôt vertes (48 tests, Qwen 19,3885, clusters 799,8557,` | La porte gpt-oss est omise, et sa valeur a changé le 02/10 : **15,6017** (rapport-routage-experts.md:66) | `4. les portes du dépôt vertes (48 tests, Qwen 19,3885, gpt-oss 15,6017, clusters 799,8557,` | moyenne |
| docs/plan-deepseek41-complet.md:273 | `**Aucun chiffre de V4.1 n'est publié avant P7.** Jusque-là s'applique la phrase` | Contredit le §3.1 du même document, qui publie des chiffres V4.1 (1 046 tenseurs, 365,70 Go, 63,8 ms, 219–524 ms, 120 Mo de RSS) — mesures statiques, pas calculs | `**Aucun chiffre de calcul de V4.1 n'est publié avant P7** (les mesures statiques de §3.1 restent permises). Jusque-là s'applique la phrase` | faible |
| docs/comparaison-spiking.md:3 | `Comparaison des trois architectures neuromorphiques de référence avec la nôtre,` | Le document ne nomme jamais les deux dimensions structurantes : grappes/machines (vision §3-4) et lecture des flux pour adapter l'architecture à la tâche (vision §2) | `Comparaison des trois architectures neuromorphiques de référence avec la nôtre — le cœur de Drave (router des flux sur des grappes réparties entre composants et machines, et lire ces flux pour adapter l'architecture à la tâche) n'est pas remis en cause : le spike est un moyen d'obtenir la parcimonie,` | moyenne |
| docs/comparaison-spiking.md:6 | `Sources : [Spikformer](https://ar5iv.labs.arxiv.org/html/2209.15425) (Zhang et` | Seules les sources externes sont citées ; les chiffres internes (352,8 M évts/jeton, 5,3 G évts/s, 2,0/12,7 ms, 8,3/57 nJ) ne renvoient à aucun rapport | insérer avant : `Mesures internes : `reports/rapport-inference.md`, `reports/rapport-attention-creuse.md`, `reports/bilan-multi-materiel.md`. ` | moyenne |
| docs/comparaison-spiking.md:52 | `8,3 nJ/événement (FPGA) contre 57 nJ (CPU) — rapport 6,9×` | Le 8,3 nJ FPGA est **projeté** (« 4,83 G évts/s *projeté* (limite DDR3) », bilan-multi-materiel.md:47), et la l.143 l'appelle « notre mesure » | `8,3 nJ/événement (FPGA, **projeté**) contre 57 nJ (CPU, mesuré) — rapport 6,9×` | faible |
| docs/comparaison-spiking.md:58 | `notre débit est donc constant, et l'argument « on ne paie que ce qui s'active »` | Contredit la vision (§1 : coût proportionnel à l'activité ; densité mesurée 17,9 %, croisement push/pull à 22 %) en ignorant ce cadrage mesuré | `notre débit est constant **à seuil nul** ; à seuil 5 % du max, la densité mesurée est de 17,9 %, sous le croisement de 22 % (`reports/rapport-localite-activation.md`, `reports/rapport-croisement-push-pull.md`) :` | moyenne |

## Ce qui est déjà cohérent et ne doit pas être touché

- **plan-deepseek41-complet.md** — cadre conforme à la vision : llama.cpp est une *porte de correction*, pas le but (l.4-9) ; les deux dimensions structurantes sont présentes (grappes l.20 et P6, lecture des flux l.22 et l.32-36) ; les mesures V4.1 recoupées sont justes (1 046 tenseurs, 365,70 Go, 62,7 ms mesuré vs 63,8 ms, 74 ms, engram 219–524 ms, 120 Mo de RSS, 40 couches, 384 experts top-6, 48 tests, Qwen 19,3885, clusters 799,8557, protocole v5 modes 0-4) ; les interdits (§6) sont dans l'esprit de la vision.
- **plan-mode4-lot-listes.md** — le corps de spécification est exact : en-tête 79 o, version 5, préfixe d'état 12 o, R1–R7, plafonds avant allocation ; conforme au code (main.rs:1862-1886, 2256-2309) et au rapport mesuré (2,74e-2 / 3,03e-2, critère 1,11× ≤ 1,5×, ÷2,2 sur le fil).
- **plan-deepseek-v4-flash.md** — le diagnostic de fond reste vrai : GGUF découpé en shards, `deepseek4` non implémenté, 43 couches / 256 experts / top-6 et tokenizer 129 280 confirmés par `--config`.
- **comparaison-spiking.md** — les chiffres des trois articles sont sourcés (liens arXiv en tête) et les réserves §6 (gains théoriques, retard de qualité, aucun SNN à l'échelle LLM) sont honnêtes ; la comparaison ligne à ligne avec Drave ne contient pas d'erreur factuelle relevée.
- À ne pas casser : la règle « pas de forward muet », les deux portes par phase (correction + Drave), l'encadré « laissé à l'implémenteur » du mode 4.

## Points à trancher par l'humain

1. **Deux chemins ou un seul ?** La vision garde dense et listes et « choisit par la mesure » (22 % de densité) ; `comparaison-spiking.md` §5 et `programme-recherche.md` §2bis font de la cible spiking la seule qui « donne le débit variable ». Faut-il nuancer la cible ou la vision ?
2. **Sort de `plan-deepseek-v4-flash.md`** : encadré « remplacé par plan41 » en tête, ou réécriture ?
3. **Porte gpt-oss 15,6017** : absente de plan41 et de `tools/portes.sh` (section 7 renvoie gpt-oss hors script) — à inscrire comme porte de plein droit ?
4. **Hors des quatre documents** : `docs/vision.md:163` porte encore `15,1757` (périmé depuis le 02/10) ; `REPRISE.md` porte « protocole v4 », « 15,1757 » et « cargo test 17/17 ». À corriger ?
5. **Bug de contrôle découvert en vérifiant (hors périmètre docs)** : `model.rs:125` traite tout tenseur `attn_sinks` comme un manque V4, donc `drave gpt-oss-120b-MXFP4.gguf --config` répond « calculable : NON — il manque : attention V4 : dé-rotation de sortie et puits par tête » alors que les puits sont implémentés (model.rs:2317, 3456-3518) et que la porte 15,6017 a été mesurée. La porte P0 de plan41 (« `--config` annonce la bonne liste de manques ») n'est donc pas encore franchie.

Aucun fichier n'a été modifié.

