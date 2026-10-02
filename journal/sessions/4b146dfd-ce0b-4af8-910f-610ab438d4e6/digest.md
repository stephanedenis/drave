# Session DSH — relecture

- identifiant : `4b146dfd-ce0b-4af8-910f-610ab438d4e6`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-02 09:52:10
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
- protocole de transport = **v5** ;
- 18 formats lisibles (dont IQ1_S/IQ1_M/IQ2_XXS/IQ3_XXS/IQ4_XS/Q3_K/Q5_K/Q5_0), vérifiés contre libggml ; les formats sans noyau sont lus par déquantification + produit f32 (assumé, plus lent) ;
- l'attention MLA à rang faible est implémentée et **validée** contre llama.cpp sur GLM-5.3 (corrélation 0,999024, top-1 3/3) ; GLM-5.3 (754 G) et Kimi-K2.7 (1 026 G) se calculent ; **DeepSeek-V4.1 ne se calcule pas encore** (hyper-connexions, sortie à rang faible groupée, dé-rotation + puits, attentions compressées CSA/HCA) ; llama.cpp ne connaît pas `deepseek41` mais exécute `deepseek4` (V4-Flash, 86,9 Go) ;
- le plan V4.1 à jour est `docs/plan-deepseek41-complet.md` (« les flux d'abord ») : ne le critique que s'il contredit la vision.

DOCUMENTS À AUDITER (lis-les en entier) :
1. docs/plan-modeles-lourds.md
2. docs/plan-gpu-topk.md
3. docs/plan-mla-vision.md
4. docs/plan-prefill-reparti.md

Ce que tu cherches, par ordre d'importance :
1. **Objectifs de plan qui contredisent la vision** : un plan dont le but affiché est « égaler llama.cpp », « accélérer le forward dense », ou qui traite les listes comme un mode optionnel plutôt que comme le contrat.
2. **Chiffres périmés** (portes, tests, version de protocole, formats, état de la MLA, état de V4.1).
3. **Plans qui ne disent pas ce qu'ils changent à la sortie** (la règle du dépôt : aucune optimisation ne change une sortie sans le dire).
4. **Absence des deux dimensions structurantes** : grappes/machines, et lecture des flux pour adapter l'architecture à la tâche.
5. **Affirmations non sourcées.**

Format de sortie, strictement : un tableau markdown

| fichier:ligne | citation exacte (≤ 25 mots) | problème | correction minimale proposée (texte de remplacement exact) | gravité |

puis une liste courte « ce qui est déjà cohérent et ne doit pas être touché », et une liste « points à trancher par l'humain » s'il y en a.

Règles : corrections MINIMALES uniquement (une phrase, un chiffre, une phrase de cadrage) — jamais de réécriture. Aucun faux positif : cite la ligne exacte. Si un document est cohérent, dis-le en une ligne. Maximum 25 constats.
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

⏵ Reading the reference vision documents first, then auditing the four plans.

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/ | head -60; echo \"---\"; wc -l /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/programme-recherche.md /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pl … [365 caractères tronqués]`

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
… [750 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md"}`

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

### 🤖 Assistant

⏵ Vision lue ; lecture du programme de recherche puis des quatre plans.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/programme-recherche.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-modeles-lourds.md"}`

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
… [8703 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des plans GPU/top-k, MLA, préfill réparti et du plan V4.1 de référence.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-gpu-topk.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-prefill-reparti.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-gpu-topk.md</path>
<type>file</type>
<content>
1: # Plan — le top-k de l'attention dans le noyau GPU (phase 1.1)
2: 
3: **En une ligne** : l'attention creuse (`--attn-topk`) ne peut pas se servir du KV
4: déporté en VRAM — le code l'interdit explicitement — donc à long contexte elle
5: retombe sur le CPU et coûte **~70 fois** le chemin GPU complet. Ce plan
6: chiffre l'écart et décrit les trois noyaux qui le comblent.
7: 
8: ## Pourquoi (mesuré, pas supposé)
9: 
10: Le chemin GPU de l'attention est conditionné à `groupe = fen == 0 &&
11: self.attn_topk == 0 && rep > 1` (`model.rs:3150`) : **dès que le top-k est
12: demandé, le miroir VRAM est ignoré**. Les deux mesures qui existent déjà disent ce
13: que ça coûte :
14: 
15: | mesure (dépôt) | valeur |
16: |---|---|
17: | attention 1 M de clés, **CPU** (int4, host) | **968 ms** par couche |
18: | la même, **KV en VRAM** (`DRAVE_GPU_KV=1`, noyaux `attn_kv_*`) | **13,2 ms** (×73) |
19: | « masquer sans réécrire les boucles » en top-k CPU | 12,4 → 12,5 ms : **aucun gain** |
20: 
21: La troisième ligne est la clé : en top-k, le coût n'est pas le softmax mais la
22: **notati
… [8614 caractères tronqués]
  ```


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
… [23747 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du plan MLA (725 lignes) et du plan V4.1 de référence.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mla-vision.md", "limit": 380}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-deepseek41-complet.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mla-vision.md</path>
<type>file</type>
<content>
1: # Plan : MLA et vision (chantier 5)
2: 
3: Ces deux-là ne sont pas « à moitié faits » : ils ne sont pas commencés, et ce
4: document dit exactement par quoi commencer, pour qu'une session suivante n'ait
5: pas à refaire l'enquête. Rien ici n'est mesuré — c'est une feuille de route, et
6: elle est marquée comme telle.
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
22: DeepSeek-V3, contre 2 × 128 × 128 = 32 768 
… [20310 caractères tronqués]
  ```


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

⏵ Lecture de la suite du plan MLA et vérification des faits dans le dépôt.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mla-vision.md", "offset": 381, "limit": 345}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mla-vision.md</path>
<type>file</type>
<content>
381: Autrement dit : le modèle de texte se charge, le projecteur se charge (519
382: tenseurs), le contexte multimodal s'instancie, le bitmap aussi, le marqueur est
383: rendu par la bibliothèque — et c'est **`mtmd_tokenize`** qui échoue, en levant une
384: exception C++ (`std::bad_alloc`, puis `basic_string::_M_replace`) au lieu de
385: rendre un code d'erreur.
386: 
387: Hypothèses, par ordre de plausibilité, pour la suite :
388: 
389: 1. **mélange de runtimes C++** : la bibliothèque d'ollama est liée à son propre
390:    `libstdc++`, l'appelant est un `python3` système. Écrire le programme en **C**
391:    (ou en C++ compilé avec le même runtime) est l'essai le moins coûteux ;
392: 2. déclaration d'un paramètre mal typé (le 3e de `tokenize` est `const char *`,
393:    le 2e `mtmd_input_chunks *` — c'est ce que déclare le script, mais sans
394:    en-tête rien ne le garantit) ;
395: 3. `mtmd_context_params` : la valeur par défaut rendue par la bibliothèque est
396:    passée telle quelle (les octets au-delà de la taille réelle sont à zéro) ;
397:    un champ non couver
… [18877 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"15,6017\\|15.6017\\|15,1757\\|15.1757\" --include=*.md --include=*.sh --include=*.rs --include=*.py . 2>/dev/null | head -40; echo \"=== TESTS ===\"; grep -rn \"48 tests\\|17/17\\|19,3885\\|799,8557\" --include=*.md --incl … [86 caractères tronqués]`

  ```
./reports/rapport-coherence-docs.md:116:| 55 | `README.md:344` | gpt-oss-120b : perplexité « **—** » | 15,1757 (REPRISE §2) et 20,8361 à 63 jetons : le chiffre existe | MANQUANT |
./reports/rapport-session-2026-09-30.md:92:Qwen ctx 256 = **19,3885** · gpt-oss ctx 256 = **15,1757** · gpt-oss avec
./reports/rapport-coherence-docs-2.md:113:| 49 | `README.md:345` | ligne gpt-oss : `\| … \| MXFP4 \| **blocs lus** \| **15,1757 (ctx 256)** \| 60 Go \|` | la ligne est **décalée d'une colonne** : « blocs lus » occupe la colonne perplexité et 15,1757 la colonne débit ; la référence est 15,1757 (`REPRISE.md:70`) | CONTRADICTOIRE |
./reports/rapport-coherence-docs-2.md:187:    (« blocs lus » en perplexité, 15,1757 en débit) ; remettre perplexité =
./reports/rapport-coherence-docs-2.md:188:    15,1757 (ctx 256), débit = « blocs lus » ou la valeur réelle, mémoire = 60 Go.
./reports/rapport-gpu-topk-selection.md:234:| référence CPU (sans miroir VRAM) | 15,1757 |
./reports/rapport-gpu-topk-selection.md:295:dense (15,1667), l'écart de 6,6e-5 avec le CPU (15,1757) étant celui, connu et
./reports/rapport-gpu-topk-selection.md:345:| 6 | portes de non-régression : 19,3885 et 15,1757 | ✅ inchangées, mes
… [18987 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des portes courantes, du nombre de formats et de l'état des forwards.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== portes.sh ===\"; sed -n '1,80p' tools/portes.sh; echo \"=== formats ===\"; grep -rn \"18 formats\\|18 types\\|dix-huit formats\\|IQ3_XXS\" --include=*.md docs README.md 2>/dev/null | head -20", "description": "Inspect port … [25 caractères tronqués]`

  ```
=== portes.sh ===
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
D=./drave-core/target/release/drave
RAPIDE=${1:-}
ECHEC=0

[ -x "$D" ] || { echo "compiler d'abord : (cd drave-core && cargo build --release)"; exit 2; }

compare() {  # nom, attendu, obtenu
    if [ "$2" = "$3" ]; then
        printf "  %-42s %s  ✅\n" "$1" "$3"
    else
        printf "  %-42s %s  ❌ (attendu %s)\n" "$1" "${3:-—}" "$2"
        ECHEC=1
    fi
}

# Attention : le moteur affiche AUSSI une perplexité cumulée par fenêtre, avant
# le total. Prendre la première occurrence du motif donnait 17,431 (fenêtre 1) au
# lieu de 19,3885 (total) — un instrument faux qui accuse le code.
valeur() { grep -oE "=== perplexité [0-9]+\.[0-9]+" | grep -oE "[0-9]+\.[0-9]+" | head -1; }

echo "=== Portes ==="

# 1. Tests unitaires.
n=$( (cd dra
… [2687 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== VERSION_FLUX ===\"; grep -rn \"VERSION_FLUX\" drave-core/src/main.rs | head -5; echo \"=== arch forward support ===\"; grep -rn \"glm-dsa\\|glm5next\\|kimi_k25\\|deepseek41\" drave-core/src/*.rs | head -30; echo \"=== 754  … [198 caractères tronqués]`

  ```
=== VERSION_FLUX ===
1862:const VERSION_FLUX: u8 = 5;
2050:    t.push(VERSION_FLUX);
2235:    if version != VERSION_FLUX {
2238:            format!("flux en version {version}, cette build parle la {VERSION_FLUX} \
2274:{MODE_LOT_LISTES}, protocole v{VERSION_FLUX})"))),
=== arch forward support ===
=== 754 / 1026 ===
reports/rapport-mla-experts.md:96:- **Kimi-K2.7 (1 026 G poids)** : `--config` annonce « calculable : oui »,
reports/rapport-mla-experts.md:151:## 6ter. Kimi-K2.7 : 1 026 G poids, premier calcul
reports/rapport-mla-experts.md:166:Aucune référence externe n'a été calculée pour Kimi (1 026 G, deux chargements de
reports/rapport-routage-experts.md:91:| Kimi-K2.7-Code | 1 026 G | MLA à rang faible, hyper-connexions |
reports/rapport-routage-experts.md:92:| GLM-5.3 | 754 G | MLA à rang faible, hyper-connexions, attention par index |
  ```

### 🤖 Assistant

⏵ Recoupement des états MLA/V4.1 et des rapports cités dans les plans.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '330,400p' README.md; echo \"=== REPORTS ===\"; ls reports/ | head -60", "description": "Read README model table and list reports"}`

  ```
ce qui s'active » est vérifié à l'échelle du moteur.

**Montée en charge** (densité 100 %, meilleur de 3 passes) : 1 thread 0,41 G év/s →
8 threads 2,75 → 16 threads 4,45 → **32 threads 4,84** → 39 threads **2,04** ❌.
L'attente active ne tolère aucune sursouscription : le pool est borné à `CPU − 1`
et vaut `3/4 × CPU` par défaut.

**Sans multiplieur** : décalages + additions donnent le résultat exact en 112,3 ms
contre 2,5 ms pour i8×i8 (×44,9 sur CPU) — mais **sur FPGA le multiplieur n'existe
pas**, et la contrainte du CDC est satisfaite sans réentraînement ni élagage.

> ⚠️ Trois pièges ont coûté une campagne de mesures fausses chacun : un état
> partagé avec **deux contrats de nettoyage** (d'où une « divergence » fantôme et
> un débit surestimé à 7,53 G év/s), un `&mut` dans la boucle chaude (barrière
> d'aliasing : 3,09 → 0,97 G év/s), et la **sursouscription** de l'attente active
> (39+1 threads sur 40 CPU : effondrement ×2,4 — et le `yield_now()` censé le
> corriger a tout empiré). Détail dans le rapport.

---

## Formats et modèles réellement lisibles

Le moteur lit **Q4_K, Q6_K, Q4_0, Q5_0, Q5_1, Q8_0, Q2_K, Q3_K, Q5_K, MXFP4,
IQ1_S, IQ1_M, IQ2_XXS, IQ3_XXS, IQ4_XS, BF16, F
… [4236 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '80,110p' reports/rapport-mla-experts.md; echo \"=== 151-175 ===\"; sed -n '151,175p' reports/rapport-mla-experts.md; echo \"=== formats ports ===\"; grep -rn \"formats\" tools/portes_formats.sh | head -20; echo \"=== nb types … [141 caractères tronqués]`

  ```
Proj::vide() }` supposait qu'un modèle à experts n'a *que* des couches à
  experts. Faux pour GLM-5.3 (3 couches denses puis 76) et pour Kimi (1 puis
  60). La décision se prend maintenant **couche par couche**, sur la présence
  effective du mélange.
- **Un garde-fou a cassé une porte verte.** Le contrôle « le modèle déclare des
  experts mais aucun tenseur d'experts n'est lisible » refusait le modèle en
  clusters de la porte publiée (`qwen3-30b-8clusters-v2`), où les experts sont
  préfixés `cl0/…`. Détecté tout de suite parce que la porte existait ; le
  contrôle ne s'applique plus quand un mapping est actif.

## 5. Ce qui est mesuré

- **GLM-5.3 (216 Go)** : 79 couches MLA, 76/79 mélanges d'experts chargés (les
  3 autres sont denses, c'est le modèle), ~85 Go de RSS au chargement, dont
  ~52 Go de tenseurs MLA déquantifiés en f32 — un coût réel, pas un détail :
  ces huit tenseurs par couche ne sont pas empruntés au fichier.
- **Kimi-K2.7 (1 026 G poids)** : `--config` annonce « calculable : oui »,
  61 couches MLA, routage sigmoïde ×2,827, 384 experts dont 8 par jeton.
- **Portes inchangées au bit près** après le remplacement de `matvec_q4` par un
  aiguillage : Qwen2.5-0.5B 
… [2214 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des portes de routage, du compte de formats et des sources des chiffres MLA/vision.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '80,140p' tools/portes.sh; echo \"=== verifier formats types ===\"; grep -oE '\"[A-Z0-9_]+\"' tools/verifier_formats.py | sort -u | head -30", "description": "Check routing gates and format type list"}`

  ```
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
=== verifier formats types ===
"CONCORDE"
"DIVERGE"
"REF_GGML_BLOC"
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 5,2e-7 sources ===\"; grep -rn \"5,2e-7\\|5.2e-7\\|5,37e-07\\|1,73e-06\" docs/*.md reports/*.md | head -20; echo \"=== 0,999024 sources ===\"; grep -rln \"0,999024\" docs reports | head; echo \"=== 234,88 ===\"; grep -rn \ … [107 caractères tronqués]`

  ```
=== 5,2e-7 sources ===
docs/plan-deepseek-v4-flash.md:49:     5,2e-7 : c'est la brique la plus proche du but) ;
docs/plan-mla-vision.md:65:numpy indépendante — **écart max relatif 5,2e-7**, soit le bruit de virgule
docs/plan-mla-vision.md:77:   transposée. L'écart est passé de 0,82 (relatif) à 5,2e-7 après correction.
docs/plan-mla-vision.md:179:| embedding de patchs (convolution 14 × 14) | **5,37e-07** |
docs/plan-mla-vision.md:181:| projecteur (fusion 2 × 2 → `mm.0` → GELU → `mm.2`) | **1,73e-06** |
docs/plan-modeles-lourds.md:83:| DeepSeek-V4 / V4-Flash / V4.1-Flash | `deepseek4` (43 couches, 256 experts top-6, 1 M ctx) | lecture des métadonnées et du tokenizer ✅ (129 280 jetons, aller-retour identique) ; MoE 128/top-8 (gpt-oss, Qwen3) ; attention MLA validée sur modèle synthétique (5,2e-7) | le forward `deepseek4`, et le **lecteur multi-shards** |
docs/vision.md:166:  indépendante** (MLA à **5,2e-7** contre numpy ; vision : patchs 5,4e-7,
=== 0,999024 sources ===
docs/plan-deepseek41-complet.md
reports/rapport-mla-experts.md
reports/rapport-execution-v41.md
=== 234,88 ===
docs/contexte-long.md:105:| E5 | **Attention creuse** | **fait pour la mesure** — `--attn-topk 256` : 234,8
… [1548 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dernières vérifications : sources des chiffres du banc MLA/vision et cohérence des mesures clusters.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== banc-mla / banc-vision dans reports ===\"; grep -rln \"banc-mla\\|banc-vision\" reports/ | head; echo \"---\"; grep -rn \"5,37e-07\\|1,82e-06\" reports/ | head; echo \"=== clusters 3,20 / 1587 ===\"; grep -rn \"3,20 Go\\|1 … [175 caractères tronqués]`

  ```
=== banc-mla / banc-vision dans reports ===
reports/rapport-drapeaux-ignores.md
---
=== clusters 3,20 / 1587 ===
reports/rapport-decoupage-moe.md:105:Qwen3-30B-A3B : **3,20 Go chargés au lieu de 18,56** pour un nœud qui sert un
reports/rapport-decoupage-moe.md:106:cluster, 625 ms au lieu de 3,9 s, 1 587 tenseurs vérifiés — le format est décrit
reports/rapport-lecteur-multifichiers.md:10:Le sprint précédent a produit le format (convertisseur, 1 587 tenseurs vérifiés
reports/rapport-lecteur-multifichiers.md:18:d'origine (18,56 Go, un fichier, sur le disque mécanique) contre le même modèle
reports/rapport-lecteur-multifichiers.md:55:| tenseurs | **1 587** = le compte de la conversion |
reports/rapport-lecteur-multifichiers.md:239:| conversion | 435 + 8 × 144 = **1 587 tenseurs**, 18,60 Go, 351,7 s |
reports/rapport-lecteur-multifichiers.md:241:| vérification par empreintes | **1 587 tenseurs · TOUT CONCORDE** |
=== MiniMax ===
27:| **MiniMax-H3** | famille différente (vision+langage) | 22,8 Go (2 × Q4_K) | — | en file |
87:| MiniMax-H3 | vision+langage | vision Qwen2.5-VL ✅ | à relever |
124:| MiniMax-H3 | `?` | 1 | 532 | **11,42 Go** | 11,4 Go |
137:* **MiniMax-H3 n'est pas un modèle
… [207 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -3 -- docs/plan-modeles-lourds.md docs/plan-gpu-topk.md docs/plan-mla-vision.md docs/plan-prefill-reparti.md; echo \"=== dates rapports ===\"; ls -la reports/rapport-mla-experts.md reports/rapport-routage-experts.md … [182 caractères tronqués]`

  ```
8e3198a La file de 1 138 Go est terminée : 1 163 Go de modèles lourds, tous complets et lisibles
ae4531b Inventaire des modèles lourds : 984 Go de poids annoncés par les descripteurs, 984 Go annoncés par HuggingFace
7c1b9ff Convertisseur GGUF → modèle éclaté en clusters : un fichier par cluster, vérifié par empreintes
=== dates rapports ===
-rw-r--r--. 1 stephane stephane  5248  2 oct 08:51 reports/rapport-execution-v41.md
-rw-------. 1 stephane stephane 12409  2 oct 07:56 reports/rapport-mla-experts.md
-rw-------. 1 stephane stephane  9510  2 oct 02:37 reports/rapport-routage-experts.md
=== README tests ===
  ```

### 🤖 Assistant

⏵ Contrôle final des sources en journal et des mentions de modes optionnels.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== 5,2e-7 journal ===\"; grep -rn \"5,2e-7\\|5.2e-7\" journal/sessions/*/digest.md 2>/dev/null | head -5; echo \"=== optionnel/dense dans les 4 plans ===\"; grep -n \"optionnel\\|option\\b\\|--dense\" docs/plan-modeles-lourds … [238 caractères tronqués]`

  ```
=== 5,2e-7 journal ===
journal/sessions/4d7a793b-74d1-4c46-bb53-21953fe91d87/digest.md:1041:docs/plan-mla-vision.md:65:numpy indépendante — **écart max relatif 5,2e-7**, soit le bruit de virgule
journal/sessions/4d7a793b-74d1-4c46-bb53-21953fe91d87/digest.md:1042:docs/plan-mla-vision.md:77:   transposée. L'écart est passé de 0,82 (relatif) à 5,2e-7 après correction.
journal/sessions/4d7a793b-74d1-4c46-bb53-21953fe91d87/digest.md:1047:docs/vision.md:166:  indépendante** (MLA à **5,2e-7** cont
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:18399:⏵ MLA validé : le moteur retrouve la référence numpy à 5,2e-7 près
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:18405:d5ee7a0 MLA : le moteur retrouve la référence numpy à 5,2e-7 près
=== optionnel/dense dans les 4 plans ===
=== liste contrat ===
  ```

### 🤖 Assistant

⏵ Vérification terminologique finale sur « listes » et « événements » dans les quatre plans.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in plan-modeles-lourds plan-gpu-topk plan-mla-vision plan-prefill-reparti; do echo \"== $f ==\"; for w in liste événement grappe machine cluster flux topk; do printf \"  %-10s %s\\n\" \"$w\" \"$(grep -ic \"$w\" docs/$f.md)\"; d … [60 caractères tronqués]`

  ```
== plan-modeles-lourds ==
  liste      1
  événement 1
  grappe     0
  machine    0
  cluster    6
  flux       1
  topk       0
== plan-gpu-topk ==
  liste      0
  événement 0
  grappe     0
  machine    1
  cluster    0
  flux       0
  topk       14
== plan-mla-vision ==
  liste      1
  événement 0
  grappe     0
  machine    3
  cluster    0
  flux       5
  topk       0
== plan-prefill-reparti ==
  liste      5
  événement 0
  grappe     0
  machine    0
  cluster    0
  flux       38
  topk       1
  ```

### 🤖 Assistant

⏵ Dernier contrôle lexical, puis rédaction du rapport adverse.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -in \"machine\" docs/plan-gpu-topk.md; echo \"---noeud modeles-lourds---\"; grep -in \"nœud\\|noeud\" docs/plan-modeles-lourds.md; echo \"---noeud prefill---\"; grep -ic \"nœud\" docs/plan-prefill-reparti.md", "description": "Ch … [27 caractères tronqués]`

  ```
31:* `drave-core/src/gpu.rs` : `Machine::attn_kv(...)` (FFI, allocations, partiels) ;
---noeud modeles-lourds---
73:   * **disposition contiguë par cluster** : un nœud ne lit que sa tranche, en
101:| 5 | **format** : manifeste + index + disposition contiguë | ✅ **écrit et mesuré sur Qwen3-30B-A3B** : `commun.gguf` + 8 `cluster-XX.gguf`, un nœud charge **3,20 Go au lieu de 18,56** et 625 ms au lieu de 3,9 s, 1 587 tenseurs vérifiés par empreinte — [`docs/format-clusters.md`](format-clusters.md) |
---noeud prefill---
13
  ```

### 🤖 Assistant

⏵ Relecture ciblée des lignes citées pour garantir l'exactitude des citations.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for spec in \"docs/plan-modeles-lourds.md:22\" \"docs/plan-modeles-lourds.md:75\" \"docs/plan-modeles-lourds.md:76\" \"docs/plan-modeles-lourds.md:77\" \"docs/plan-modeles-lourds.md:83\" \"docs/plan-modeles-lourds.md:84\" \"docs/plan … [665 caractères tronqués]`

  ```
docs/plan-modeles-lourds.md:22 | | **DeepSeek-V4.1-Flash** | le plus lourd des ouverts, MoE, agentique | **365,7 Go** (Q2) | — | **en cours** (26 % à 09h36) |
docs/plan-modeles-lourds.md:75 | 4. **Le banc de bout en bout** : perplexité sur 512 jetons, comparable à
docs/plan-modeles-lourds.md:76 |    llama.cpp, ou l'écart expliqué — c'est la définition de « capable de rouler du
docs/plan-modeles-lourds.md:77 |    best of breed ».
docs/plan-modeles-lourds.md:83 | | DeepSeek-V4 / V4-Flash / V4.1-Flash | `deepseek4` (43 couches, 256 experts top-6, 1 M ctx) | lecture des métadonnées et du tokenizer ✅ (129 280 jetons, aller-retour identique) ; MoE 128/top-8 (gpt-oss, Qwen3) ; attention MLA validée sur modèle synthétique (5,2e-7) | le forward `deepseek4`, et le **lecteur multi-shards** |
docs/plan-modeles-lourds.md:84 | | Kimi-K2.7 | `kimi_k25` | — | tout le forward |
docs/plan-modeles-lourds.md:85 | | GLM-5.3 | à relever | — | tout le forward |
docs/plan-modeles-lourds.md:99 | | 3 | **forward deepseek4** (attention latente + MoE 256/top-6) | perplexité sur 512 jetons comparable à llama.cpp, ou l'écart expliqué |
docs/plan-modeles-lourds.md:135 | * **Les architectures lourdes sont lues** 
… [2044 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rapport rédigé ; envoi au parent puis restitution.

- **send_message** `{"agent_id": "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", "message": "RAPPORT DE RELECTURE ADVERSE — 4 plans audités contre docs/vision.md + docs/programme-recherche.md + faits du 02/10/2026. Aucun fichier modifié ; toutes les citations sont vérifiées ligne par ligne. 19 constats (≤25).\n\n| fichier:lign … [9583 caractères tronqués]`

  ```
message delivered to agent bbd6969f-0f70-42b2-8951-64d1f2f36d2e
  ```

### 🤖 Assistant

⏵ Restitution du rapport adverse, 19 constats, aucune écriture.

Rapport adverse — 4 plans audités contre `docs/vision.md`, `docs/programme-recherche.md` et les faits du 02/10/2026. Aucun fichier modifié ; chaque citation a été revérifiée à la ligne. **19 constats.**

| fichier:ligne | citation exacte (≤ 25 mots) | problème | correction minimale proposée (texte de remplacement exact) | gravité |
|---|---|---|---|---|
| docs/plan-modeles-lourds.md:75-77 | « comparable à llama.cpp, ou l'écart expliqué — c'est la définition de « capable de rouler du best of breed » » | Objectif affiché = égaler llama.cpp ; la vision fait du flux de listes le contrat et llama.cpp une porte de correction (cf. plan-deepseek41-complet.md:9). | Remplacer par : « comparable à llama.cpp, ou l'écart expliqué — la conformité à llama.cpp est une porte de correction, pas le but : le but est de conduire des flux. » | élevée |
| docs/plan-modeles-lourds.md:99 | « perplexité sur 512 jetons comparable à llama.cpp, ou l'écart expliqué » | Critère de succès du forward réduit à la référence externe, sans porte de flux (tracé puis rejoué à l'identique) que le plan V4.1 impose (P0/P3). | Remplacer par : « perplexité comparable à llama.cpp **et** flux tracé puis rejoué à l'identique (portes Drave) ; sinon l'écart est expliqué » | moyenne |
| docs/plan-mla-vision.md:55 | « ### ÉTAT : MLA EST FAIT ET VALIDÉ » | Le chemin MLA validé est dense (numpy, 5,2e-7) ; le plan ne dit nulle part qu'il doit produire des listes/événements — le plan V4.1 en fait le premier écart (« 0 événements », P0). | Remplacer par : « ### ÉTAT : MLA EST FAIT ET VALIDÉ (chemin dense ; compteur d'événements à instrumenter, cf. plan-deepseek41-complet.md P0) » | moyenne |
| docs/plan-modeles-lourds.md:83 | « \| DeepSeek-V4 / V4-Flash / V4.1-Flash \| `deepseek4` (43 couches, 256 experts top-6, 1 M ctx) \| » | V4.1-Flash est `deepseek41` (même doc, l.120), 40 couches, 384 experts top-6 (plan V4.1, l.69) ; llama.cpp ne connaît pas `deepseek41`. | Remplacer par : « \| DeepSeek-V4 / V4-Flash \| `deepseek4` (43 couches, 256 experts top-6, 1 M ctx) ; V4.1-Flash : `deepseek41` (40 couches, 384 experts top-6) \| » | élevée |
| docs/plan-modeles-lourds.md:135-136 | « Aucune n'a de `forward` dans le moteur — c'est le chantier suivant. » | Faux depuis le 02/10 : `deepseek2` (Kimi-K2.7, 1 026 G) et `glm-dsa` (GLM-5.3, 754 G) se calculent (README, rapport-mla-experts) ; restent `deepseek4`/`deepseek41`. | Remplacer par : « `deepseek4` et `deepseek41` n'ont pas encore de `forward` ; `deepseek2` et `glm-dsa` se calculent (Kimi-K2.7, GLM-5.3). » | élevée |
| docs/plan-modeles-lourds.md:84 | « \| Kimi-K2.7 \| `kimi_k25` \| — \| tout le forward \| » | Architecture fausse (le même doc relève `deepseek2`, l.122) et état périmé : Kimi se calcule (1 026 G, 73 s/jeton ; non validé). | Remplacer par : « \| Kimi-K2.7 \| `deepseek2` \| MLA à rang faible ✅ (1 026 G, 73 s/jeton ; non validé) \| la validation au-delà de la position 2 \| » | élevée |
| docs/plan-modeles-lourds.md:85 | « \| GLM-5.3 \| à relever \| — \| tout le forward \| » | Architecture relevée depuis (`glm-dsa`, l.121) et GLM-5.3 se calcule (216 Go ; validé pos. 0, corrélation 0,999024). | Remplacer par : « \| GLM-5.3 \| `glm-dsa` \| MLA à rang faible ✅ (216 Go, validé pos. 0) \| la validation au-delà de la position 2 \| » | élevée |
| docs/plan-modeles-lourds.md:83 | « attention MLA validée sur modèle synthétique (5,2e-7) » | État MLA périmé : la MLA à rang faible est aussi validée contre llama.cpp sur GLM-5.3 (corrélation 0,999024, top-1 3/3). | Remplacer par : « attention MLA validée contre llama.cpp sur GLM-5.3 (0,999024, pos. 0 ; écart croissant au-delà) » | moyenne |
| docs/plan-gpu-topk.md:96 | « porte de non-régression : les deux valeurs restent 19,3885 et 15,1757 » | Porte gpt-oss périmée : 15,6017 depuis le 02/10 (YaRN à retardement ; 15,1757 « était auto-cohérent, pas juste », rapport-routage-experts). | Remplacer par : « porte de non-régression : les deux valeurs restent 19,3885 et 15,6017 » | élevée |
| docs/plan-gpu-topk.md:96 | « `cargo test` 17/17 » | Compte périmé : `cargo test --release` = 48 tests, et c'est le seuil de tools/portes.sh. | Remplacer par : « `cargo test --release` 48/48 » | moyenne |
| docs/plan-mla-vision.md:3 | « ils ne sont pas commencés » | Faux : le même document conclut « MLA EST FAIT ET VALIDÉ » (l.55), « Le chemin image est COMPLET » (l.553), « La chaîne complète est DÉMONTRÉE » (l.645). | Remplacer par : « ces deux chantiers ont été menés depuis : ce document consigne ce qui a été fait et ce qui reste, » | élevée |
| docs/plan-mla-vision.md:84 | « cache ÷50 sur un vrai modèle MLA, ce qu'on n'a pas ici) » | Faux depuis le 01/10 : GLM-5.3 (79 couches MLA) et Kimi-K2.7 (61) sont sur la machine et se calculent ; le point ouvert réel est la validation au-delà de la position 2 (4,07 nats d'écart à llama.cpp au jeton 7). | Remplacer par : « cache ÷50 sur un vrai modèle MLA — GLM-5.3, 79 couches MLA, est présent ici — et la validation au-delà de la position 2, où l'écart à llama.cpp atteint 4,07 nats au jeton 7) » | élevée |
| docs/plan-mla-vision.md:5 | « Rien ici n'est mesuré — c'est une feuille de route » | Faux : le document porte des mesures (5,2e-7, 5,37e-7, 1,73e-6) et des sections d'état « FAIT ». | Remplacer par : « Les sections d'état ci-dessous portent les mesures ; ce qui reste à faire est marqué comme tel, » | moyenne |
| docs/plan-gpu-topk.md:83-84 | « la perplexité de `--attn-topk 256` à contexte 2 048 doit rester **234,88** (la valeur CPU mesurée) » | Le même plan déclare ce chiffre non reproductible (l.94) et il n'est pas sourcé ici, alors que docs/contexte-long.md §6 le documente et que la vision le cite (l.79). | Remplacer par : « la perplexité de `--attn-topk 256` à contexte 2 048 doit rester celle du CPU à la tolérance près (critère d'origine 234,88, docs/contexte-long.md §6 — non reproduit, voir étape 4) » | moyenne |
| docs/plan-gpu-topk.md:94 | « 234,88 ne correspond à aucun réglage reproductible » | Affirmation non sourcée qui invalide un chiffre publié (contexte-long §6, vision l.79) sans dire quel réglage l'avait produit ni ce qui a changé. | Remplacer par : « 234,88 (docs/contexte-long.md §6) n'est pas reproduit par ce binaire » | moyenne |
| docs/plan-modeles-lourds.md:22 | « **en cours** (26 % à 09h36) » | État périmé : le même document (l.144) dit les 24 fichiers arrivés à 12h40, et les lignes 24–30 disent encore « en file ». | Remplacer par : « **✅ arrivé** (12h40) » | faible |
| docs/plan-mla-vision.md:297 | « Vérifié : `cargo test` 6/6 » | Chiffre périmé (48 tests aujourd'hui) ; un lecteur y voit l'état courant. | Remplacer par : « Vérifié : `cargo test` 6/6 à cette étape (48 aujourd'hui) » | faible |
| docs/plan-gpu-topk.md:6 | « chiffre l'écart et décrit les trois noyaux qui le comblent. » | Le document ne nomme jamais les deux dimensions structurantes (0 occurrence de « liste »/« événement », aucune grappe/machine) ; le noyau y reste un objet local. | Remplacer par : « chiffre l'écart et décrit les trois noyaux qui le comblent. Ce noyau reste local à une machine : sa place entre composants et son effet sur les flux ne sont pas traités ici. » | faible |
| docs/plan-mla-vision.md:286-287 | « (cache ÷50) est mesurable sur le plan 1 M. » | Le plan ne dit jamais où ce chemin se place dans les axes 1 et 3 (flux, grappes/machines) — ni occurrence de « liste » ni de répartition. | Remplacer par : « (cache ÷50) est mesurable sur le plan 1 M. Ce plan ne traite ni la répartition entre grappes/machines ni la lecture des flux, qui ont leurs propres chantiers. » | faible |

### Ce qui est déjà cohérent et ne doit pas être touché
- **docs/plan-prefill-reparti.md** : cohérent de bout en bout — en-tête à jour (protocole v5, écart 0,00e0, R4 dans le code, échappement sur deux octets), corps conservé comme plan d'origine non réécrit, dimension machines (deux nœuds), et le changement de sortie est dit (l.317-324 : les lots changent l'ordre des accumulations, 6e-5 à 4e-4).
- **plan-gpu-topk** : la règle « aucune optimisation ne change une sortie sans le dire » est respectée — même ensemble retenu aux ex æquo près, écart ≤ 1e-6, ordre de sommation GPU annoncé comme différent (l.109-111), PPL A/B donnée (l.94).
- **plan-modeles-lourds** : décisions de format appuyées sur des empreintes (1 587 tenseurs) et la trace de routage ; dimension grappes présente (nœud/cluster, l.73-74 et 101).
- **docs/plan-deepseek41-complet.md** (hors tableau, conforme à la vision) : « les flux d'abord », llama.cpp = porte de correction (l.9), grappes/machines en P6, 48 tests et clusters 799,8557 (l.200-201), protocole v5 (l.21).
- Les quatre plans respectent le croisement mesuré à ~22 % : aucun ne prétend que le sparse gagne toujours, aucun ne supprime le chemin dense.

### Points à trancher par l'humain
1. **Textes de référence** : `docs/vision.md:121` dit « protocole v4 » (fait : v5) ; `docs/vision.md:162-163` donne gpt-oss à 15,1757 (fait : 15,6017) ; `docs/vision.md:222` dit l'axe 3 « rien — hypothèse écrite » alors que son §4 (l.120) dit que le transport existe et que c'est l'axe le plus avancé — faut-il amender la vision ?
2. **234,88** : mesuré (`docs/contexte-long.md` §6, cité par `vision.md:79`) ou non reproductible (`plan-gpu-topk.md:94`) ? Trancher et écrire la source.
3. `docs/plan-deepseek41-complet.md:201` dit « 17 formats » ; le fait à jour est **18** (non compté comme constat, le plan V4.1 étant sinon conforme à la vision).
4. `docs/plan-modeles-lourds.md` donne MiniMax-H3 à **22,8 Go** (l.27, l.146) et **11,42 Go** (l.124) : lequel est le poids total ?
5. Les plans du 30/09-01/10 accumulent des sections d'état sans date de fin : ajouter un en-tête « état au … » (ou les marquer historiques) pour que les états intermédiaires ne passent pas pour l'état courant.

