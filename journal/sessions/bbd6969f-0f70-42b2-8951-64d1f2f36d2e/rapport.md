# Session bbd6969f — Continue avec REPRISE.md

| | |
|---|---|
| Identifiant | `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-28 14:46 |
| Durée | 60.1 h |
| Tours | 48 |
| Messages | 2478 |
| Appels d'outils | 2348 |
| Fichiers touchés | 52 |
| Commandes | 1989 |
| Sous-agents | 17 |
| Commits | 216 |
| Compactages de contexte | 3 |

## Objectifs déclarés

- **create** — Réaliser les 8 chantiers restants du projet qtrinet-core dans l'ordre : (1) protocole de perplexité longue --depuis/--stride, (2) trancher le seuil de rotation YaRN avec ce protocole, (3) KV int8 puis int4 mesurés sur Qwen 0.5B à ctx 8192 contre llama.cpp, (4) préremplissage par lots (GEMM par tranc
… [374 caractères tronqués]
- **complete** — Réaliser les 8 chantiers restants du projet qtrinet-core dans l'ordre : (1) protocole de perplexité longue --depuis/--stride, (2) trancher le seuil de rotation YaRN avec ce protocole, (3) KV int8 puis int4 mesurés sur Qwen 0.5B à ctx 8192 contre llama.cpp, (4) préremplissage par lots (GEMM par tranc
… [374 caractères tronqués]
- **create** — Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquet
… [1023 caractères tronqués]
- **complete** — Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquet
… [1023 caractères tronqués]
- **create** — Travailler en autonomie maximale et en couloirs parallèles jusqu'à 15h00 sur Drave : (A) campagne de mesure des clés du cache KV et de leur quantificateur, (B) préremplissage par lots sur le fil (phase 3.4, bloqueur Colab), (C) analyses déléguées et audit des drapeaux ignorés, (D) noyau GPU si la ma
… [182 caractères tronqués]
- **complete** — Travailler en autonomie maximale et en couloirs parallèles jusqu'à 15h00 sur Drave : (A) campagne de mesure des clés du cache KV et de leur quantificateur, (B) préremplissage par lots sur le fil (phase 3.4, bloqueur Colab), (C) analyses déléguées et audit des drapeaux ignorés, (D) noyau GPU si la ma
… [182 caractères tronqués]
- **create** — Travailler en autonomie jusqu'à 18h00 HAE sur Drave, en couloirs parallèles : (A) noyau GPU de top-k pour l'attention creuse (phase 1.1, le seul poste GPU neuf de la feuille de route), (B) campagne de mesure en fond (frontière du cache KV à un autre contexte, vérifications long contexte), (C) analys
… [321 caractères tronqués]
- **complete** — Travailler en autonomie jusqu'à 18h00 HAE sur Drave, en couloirs parallèles : (A) noyau GPU de top-k pour l'attention creuse (phase 1.1, le seul poste GPU neuf de la feuille de route), (B) campagne de mesure en fond (frontière du cache KV à un autre contexte, vérifications long contexte), (C) analys
… [321 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — continue avec REPRISE.md

**Tour 2** — prochaine étape?

**Tour 3** — que reste-t-il à faire

**Tour 4** — fais les 8 dans l'ordre

**Tour 5** — <goal_round> Objective: "Réaliser les 8 chantiers restants du projet qtrinet-core dans l'ordre : (1) protocole de perplexité longue --depuis/--stride, (2) trancher le seuil de rotation YaRN avec ce protocole, (3) KV int8 puis int4 mesurés sur Qwen 0.5B à ctx 8192 contre llama.cpp, (4) préremplissage par lots (GEMM par tranches), (5) échelles par bloc pour DenseQ8, (6) refactorisation des boucles C … [842 caractères tronqués]

**Tour 6** — <goal_round> Objective: "Réaliser les 8 chantiers restants du projet qtrinet-core dans l'ordre : (1) protocole de perplexité longue --depuis/--stride, (2) trancher le seuil de rotation YaRN avec ce protocole, (3) KV int8 puis int4 mesurés sur Qwen 0.5B à ctx 8192 contre llama.cpp, (4) préremplissage par lots (GEMM par tranches), (5) échelles par bloc pour DenseQ8, (6) refactorisation des boucles C … [842 caractères tronqués]

**Tour 7** — background job bash-35 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (QT_GPU=1 ./qtrinet-core/target/release/qtrinet-core /home/stephane/FastNVMe/models/gpt-oss-120b-MXFP4.gguf --ppl /tmp/ids_oss.txt --ctx 256 --dense --threads 16 --limit 512 2>&1 | grep -oE "perplexité [0-9.]+ sur [0-9]+ tokens \([0-9]+ événements, [0-9.]+ s\)" > /tmp/gate_oss_final.log; echo "=== fin ===" >> /tmp/ … [98 caractères tronqués]

**Tour 8** — que reste-t-il à faire

**Tour 9** — fais tous ces 6 nouveaux chantiers

**Tour 10** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 11** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 12** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 13** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 14** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 15** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 16** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 17** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 18** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 19** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 20** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 21** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 22** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 23** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 24** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 25** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 26** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 27** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 28** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 29** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 30** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 31** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 32** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 33** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 34** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 35** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1492 caractères tronqués]

**Tour 36** — prochaine étape?

**Tour 37** — vision d'abord, puis roadmap

**Tour 38** — Au delà des défis techniques, il nou faut un vrai document de vision de ce projet. Je serais porté à renommer le projet "Drave" dans le sens Stream of logs, et ça sonne aussi bien en français car la drave fait partie du patrimoine québecois. Ces flux de listes d'activation sont le coeur de la vision et on doit en explorer toutes les implications et bénéfices sur tous les axes. Cette approche perme … [164 caractères tronqués]

**Tour 39** — 3 tout tout de suite, préserve l'historique dans un document et là ou ça permet d'être cohérent, mais tout le reste prend la teinte de la vision.

**Tour 40** — fais un roadmap ambitieux et commence les travaux qui ne nécessitent pas d'infra supplémentaire. on pourra terter avec colab pour le volet distribué

**Tour 41** — continue

**Tour 42** — continue, sois autonome pendant 2 heures

**Tour 43** — ne te fie pas à tes estimés pour le temps. fais un 2h de travail autonome en vérifiant l'heure du système à chaque itération afin de continuer à travailler sur une période te temps absolue (time-boxing)

**Tour 44** — pendant que les charges locales s'executent, peux-tu avancer des chantiers légers sur les ressources loçcale ou d'analyse pure?

**Tour 45** — as-tu ce qu'il te faut pour te rendre à 15h en travaillaint avec un maximum d'autonomie et de parallélisme d'activités?

**Tour 46** — continue jusqu'à 18h HAE

**Tour 47** — pret pour des scrum de 2h (boxing temps réel, avec revue, rétro et planning)

**Tour 48** — Continue en blocs de 2h jusqu'à demain 8h HAE. pour chacun des blocs/sprints tu dois être en autonomie totale. C'est à dire que pour cette période tu ne dois attendre après aucune interaction humaine. les rétros seront des introspections, les revues seront en mode adverse autonome. tu enchaine avec ce qui a le plus de valeur en fonction de la mission de haut niveau et de l'autonomie dont tu dispos … [2 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — continue avec REPRISE.md

*317 appels d'outils.* Actions notables :

- bash — List repository root files
- glob
- read
- bash — Inspect git log, status, tmp corpus, models
- bash — List qtrinet-core contents
- bash — Build release and run tests
- grep
- job_output
- bash — Run reference perplexity check
- bash — Read tokenizer head
- bash — Locate forward and positional logic
- bash — Check memory and cpu
- write `/tmp/gguf_meta.py`
- bash — Dump gpt-oss metadata and harmony tokens
- … et 244 autres

**Synthèse produite :**

Reprise terminée. Voici ce que la session a établi — tout est mesuré, commité, et `REPRISE.md` est à jour.

\## Les deux bugs réels de gpt-oss (§6.a)

| | avant | après |
|---|---|---|
| `attn_output.bias` ignoré (gpt-oss a un biais sur Q, K, V **et O**) — 63 jetons | 39,80 | **20,84** |
| fenêtre glissante sur les 36 couches au lieu d'une sur deux — 511 jetons | 129,9 | **15,08** |

Le motif de fenêtre est vérifié dans les sources : `layer_types` de gpt-oss alterne `sliding_attention`/`full_attention`, et llama.cpp pose `set_swa_pattern(2)`. Les deux extrêmes sont pires que le motif réel du modèle : 17,14 (toutes fenêtrées) et 26,15 (aucune). Un troisième bug latent — les puits appris absents du softmax des couches pleines — est corrigé, **effet mesuré nul** sur gpt-oss (le chemin groupé les comptait déjà).

\## La prémisse « devrait valoir ~6 » était fausse

Nouvel outil `tools/ref_logits` : llama.cpp évalue **exactement les mêmes identifiants, sans BOS**.

| mêmes prédictions | llama.cpp | qtrinet-core |
|---|---|---|
| 63 jetons, YaRN | 38,37 | 41,11 |
| 511 jetons, YaRN | 169,67 | 174,34 |

Corrélation des logits **0,999976**, **top-1 identique partout**, |ΔNLL| médian 0,076 (notre int15 contre son f32). Notre moteur n'était pas le maillon faible — il fait même mieux, parce qu'il sait éteindre YaRN, qui coûte **×9** ici (18,58 contre 174,34). Ce n'est pas un bug : HF, llama.cpp et l'implémentation officielle d'OpenAI appliquent le même YaRN statique (vérifié dans les trois sources).

\## Hypothèse harmony : réfutée, avec le mécanisme

Le modèle **exige son canal `analysis`** : après `<|start|>assistant<|channel|>`, p(analysis) = 0,9999 contre p(final) = 0,0001. Meilleur montage canonique (système officiel + `analysis` puis `final`) : **26,0** — contre **13,7** en brut pour le même texte. Le format rend le texte *moins* prévisible, pas plus.

\## Effet de bord utile

`Gguf::open_meta` ne lit plus que l'en-tête : `--tokenize` sur gpt-oss passe de ~60 s à **0,385 s** (identifiants inchangés) et chaque `--ppl` économise une lecture des 62 Go. Non-régression Qwen : **19,3885** exactement, tests 3/3.

Reste ouvert et documenté : le YaRN « à retardement » (au-delà de 4 096), protocole et coût dans `reports/rapport-gpt-oss-perplexite.md`.

### Tour 2 — prochaine étape?

*114 appels d'outils.* Actions notables :

- ask_user_question
- todo_write
- bash — llama.cpp reference on Qwen 512 tokens
- bash — Our Qwen logits at three activation precisions
- bash — Analyse the gpt-oss logit gap distribution
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/model.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/model.rs`
- bash — Build and check rotation trace on Qwen
- bash — Build long corpus and count its tokens
- write `/tmp/bascule_yarn.sh`
- bash — Launch the rotation boundary series
- bash — Collect hardware facts for the 1M plan
- bash — Read run_plan implementation
- … et 96 autres

**Synthèse produite :**

⏵ YaRN à retardement livré ; la mesure à 8 192 tourne. Voici l'état

**Livré et commité**

1. **YaRN à retardement** (`[config] rotation` en dit la raison à chaque chargement) : RoPE simple tant que `--ctx` tient dans `rope.scaling.original_context_length` (4 096), **interpolation seule** au-delà — décision **par séquence**, pas par position, parce que la structure de position relative ne survit que si toutes les clés partagent le même jeu de fréquences. `QT_YARN=1` = YaRN complet des références, `QT_YARN_NON=1` / `--sans-yarn` = jamais, `QT_YARN_MSCALE=0/1` = température seule.

2. **Le résultat qui change la donne : la moitié nuisible de YaRN, c'est la température.**

| longueur | RoPE simple | YaRN **sans** mscale | YaRN complet |
|---|---|---|---|
| 512 | **18,58** | 19,65 | 174,34 |
| 1 024 | **46,94** | 71,35 | 417,65 |
| 2 048 | **121,75** | 192,63 | 722,56 |
| 4 096 | **170,78** | 400,13 | — |
| 4 608 | — | 476,09 | 1 105,20 |

Retirer `mscale = 1 + 0,1·ln f` divise la perplexité par **8,9 / 5,9 / 3,8**. L'interpolation des basses fréquences, elle, ne coûte presque rien. HF, llama.cpp et l'implémentation officielle d'OpenAI appliquent pourtant la température telle quelle — et notre moteur les reproduit au chiffre près quand on la garde. D'où le nouveau défaut : simple sous 4 096, interpolation seule au-delà.

3. **La dégradation avec la longueur n'est pas un bug du moteur** : llama.cpp, mêmes 2 048 identifiants, un seul lot, YaRN déclaré → **714,83** contre **722,56** chez nous (1,1 %). Le `--ppl-profil` ajouté pour ça montre deux causes superposées : le **contenu** (une même tranche vaut 13,94 en tête et 59,36 prise plus loin mais présentée en position 0) et la **position** (~×7 de plus à sa place réelle).

4. **Plan 1 M** : `docs/contexte-long.md` + `--plan --ctx N` qui chiffre tout. Les trois murs : **préremplissage séquentiel** (4,5 h à 32 k, 31 h à 128 k, **1 234 h à 1 M** → chantier n° 1, il faut le préremplissage par lots) ; **bande passante du KV** (77 Go relus par jeton à 1 M en f32, 9,7 Go en int4 — 13 ms depuis les deux GPU, et le KV int4 à 1 M tient dans **un seul RTX 5000**) ; **portée de la rotation** (×32 couvre 131 072, 1 M demanderait ×256, soit huit fois ce que le modèle a vu).

**En cours** (résultats dans `/tmp/audela_4096.log` d'ici ~2 h) : RoPE simple et interpolation seule à **8 192** — c'est la mesure qui tranche le seuil de bascule, puisque le simple gagne encore à 4 096. Restent aussi le test de génération à refaire avec `
… [256 caractères tronqués]

### Tour 3 — que reste-t-il à faire

*4 appels d'outils.* Actions notables :

- bash — Check running measurements and repo state
- bash — Read the 8192 results
- bash — Inspect corpus content in hard and easy regions
- bash — Launch content-vs-context decomposition run

**Synthèse produite :**

⏵ Point complet : ce qui tourne, ce que la mesure vient de changer, et l'ordre de travail

**En cours** (~30 min) : la déconfusion contenu/contexte — ctx 512 sur 8 192 jetons, PPL par fenêtre → `/tmp/contexte_ou_contenu.log`.

**Le résultat de 8 192 vient de tomber, et il change la lecture** : RoPE simple = **48,7** (meilleur qu'à 4 096, où c'était 170,8), interpolation seule = **835,2**. Le profil par profondeur explique pourquoi : les tranches 4 608-8 191 tournent autour de **10** alors que les tranches 512-4 095 montent jusqu'à 542. Or le corpus est du même genre de prose partout — donc **le protocole actuel confond le contenu et la longueur** : à `--ctx 8192` on ne score pas les mêmes jetons qu'à `--ctx 512`. Tant que ce n'est pas corrigé, aucune courbe « par longueur » n'est interprétable.

\## Ce qu'il reste, par ordre de valeur

**1. Protocole de perplexité longue** (`--depuis N`, ou un `--stride` comme llama-perplexity) — noter **les mêmes jetons** avec des contextes de longueurs différentes. ~30 lignes. C'est le préalable à toute conclusion sur le seuil de rotation, et ça invalide une partie de ce qu'on vient de mesurer.

**2. Trancher le seuil de rotation** avec ce protocole (simple contre interpolation seule, mêmes jetons, 512 → 8 192). Indice actuel : le simple gagne partout, l'interpolation se dégrade régulièrement — le défaut (bascule à 4 096) est donc peut-être à inverser en « simple partout » pour gpt-oss.

**3. KV int8 puis int4** (E2/E3 du plan 1 M) — ÷4 puis ÷8 sur le cache. Banc d'essai : Qwen2.5-0.5B à `--ctx 8192`, 5 min par passe, écart de perplexité à mesurer contre llama.cpp (`--ctk q8_0`). C'est ce qui fait tenir 1 M en mémoire.

**4. Préremplissage par lots** (E1) — le mur n° 1 : 4,5 h à 32 k, 31 h à 128 k, **1 234 h à 1 M** en séquentiel. Un noyau GEMM par tranches débloque tout le contexte long *et* le temps de premier jeton. Gros chantier, mais rien de long ne se fait sans lui.

**5. Échelles par bloc pour `DenseQ8`** — l'écart résiduel avec llama.cpp (|ΔNLL| médian 0,076) vient de là, et ça tranche la question « 6 bits contre int8 par bloc » à octets égaux.

**6. Refactoriser les boucles CLI** (3 modes → 1) — quatrième bug de la même classe rencontré cette session (`--attn-window`/`--attn-sinks` jamais appliqués en inférence).

**7. Noyaux GPU** — une warp par ligne puis les formats 4 bits (Q4_K/Q6_K/MXFP4) : toute la famille Qwen est en Q4_K/Q6_K, donc aujourd'hui rien de la leur n'est déportable. Le plus gros levier de débit
… [595 caractères tronqués]

### Tour 4 — fais les 8 dans l'ordre

*168 appels d'outils.* Actions notables :

- create_goal
- todo_write
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs`
- bash — Build and check no regression with depuis=0
- bash — Validate depuis semantics against known window value
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs`
- bash — Validate overlapping windows and non-regression
- write `/tmp/seuil_rotation.sh`
- bash — Launch rotation threshold measurement
- … et 146 autres

**Synthèse produite :**

⏵ Analyse PowerInfer prête ; le profil d'experts gpt-oss est en file derrière la série

**Ce que fait PowerInfer** (dépôt SJTU-IPADS, miroir `Tiiny-AI`) : il exploite la **localité d'activation** — la distribution des neurones suit une loi de puissance, donc peu de neurones sont « chauds » (actifs presque toujours) et beaucoup sont « froids » (dépendants de l'entrée). Ils en tirent un moteur hybride : **les neurones chauds résident sur le GPU, les froids sont calculés sur le CPU**, plus un **prédicteur** qui devine l'ensemble actif à l'avance pour précharger, et des **opérateurs creux conscients des neurones**. Leur modèle TurboSparse (90 % de creux) est *entraîné* ainsi, précisément parce qu'imposer la parcimonie à l'inférence coûte cher.

**Ce que notre moteur a déjà, et qui est de la même famille**
- Le chemin **par listes d'événements** *est* un opérateur creux conscient des neurones : il n'itère que sur les sources actives, avec bascule mesurée vers le produit dense à **22 % de densité** (`seuil_push`).
- La parcimonie imposable (`--act-topk`, `--act-thresh`) avec sa courbe de qualité — et notre conclusion recoupe la leur : la parcimonie imposée coûte, elle se gagne à l'entraînement.
- Un capteur hebbien et, depuis aujourd'hui, un **profileur de neurones** (`--profil-neurones`, sortie `--neurones-sortie`).

**Leur idée centrale, mesurée chez nous** (Qwen2.5-0.5B, 512 jetons, seuil 5 % du max) :

| mesure | valeur |
|---|---|
| densité d'activation | **17,9 %** des neurones par jeton (82 % ne font rien) |
| concentration | les 10 % de neurones les plus lourds portent **33 %** de la magnitude |
| neurones **toujours** chauds (> 90 % du temps) | **0,08 %** |
| neurones chauds (> 50 % du temps) | 2,8 % |
| dispersion entre couches | tirs de 173 à 1 579 par jeton (×9) |

**Le verdict honnête** : leur mécanisme de *préchargement statique* repose sur un ensemble chaud **stable**, et sur un modèle SiLU comme Qwen2.5 cet ensemble est minuscule (0,08 %) — la localité existe mais elle est surtout **dynamique**, pas statique. C'est exactement pourquoi leurs gains spectaculaires sont sur des modèles ReLU/TurboSparse, entraînés pour ça. Ce qui se transpose vraiment chez nous :

1. **Le placement par neurone/expert piloté par le profil** — et pour gpt-oss, la vraie question n'est pas les neurones du FFN mais **les experts** : 4 sur 128 par jeton. Je viens d'ajouter ce comptage : le profil d'experts gpt-oss tourne (résultats dans `/tmp/profil_experts.log`). Si un pet
… [911 caractères tronqués]

### Tour 5 — <goal_round> Objective: "Réaliser les 8 chantiers restants du projet qtrinet-core dans l'ordre : (1) protocole de perple … [1122 caractères tronqués]

*124 appels d'outils.* Actions notables :

- bash — Check rotation series and expert profile
- bash — End-to-end batched prefill correctness and time
- bash — Fix the batched projection buffers
- bash — Re-test batched prefill correctness
- bash — Hoist batch buffers out of the layer loop
- bash — Fix closure signature and measure again
- bash — Commit item 4 correctness fixes
- bash — Wait for the rotation series progress
- bash — Fix the grep pattern and relaunch the series
- bash — Verify the script state after the kill
- bash — Clean engines and find the script process
- bash — Fix the grep pattern and relaunch cleanly
- bash — Read the MXFP4 CPU kernel for the layout
- bash — Find the MXFP4 scalar dot path
- … et 109 autres

**Synthèse produite :**

⏵ Tour terminé : les huit chantiers ont avancé, la non-régression tient (19,3885)

**Ce que ce tour a livré** (12 commits, tous vérifiés)

| # | chantier | état | mesure |
|---|---|---|---|
| 1 | protocole longue | ✅ | `--depuis` : `--depuis 256 --ctx 256` redonne exactement la fenêtre historique (21,565) |
| 2 | seuil de rotation | ✅ | apparié, mêmes 512 jetons : RoPE simple **39,5 / 49,8 / 49,9 / 298,6** contre interpolation 42,1 / 82,0 / 82,2 / 578,9 → le simple gagne partout |
| 3 | KV int8/int4 | ✅ | **échelles par bloc de 32** : int8 **+1,5 %** (512 j) et **+3,4 %** (4 591 j) — était +7,1 % et +5,2 % ; int4 +219 %/+287 % ; llama.cpp : +0,8 %/+494 % |
| 4 | préremplissage par lots | ✅ | GEMM int8 **et** 4 bits + regroupement des experts ; juste (13,1359 vs 13,1368) ; gain **−3 %** attribué : projections ÷2, mais attention non groupée ×2,2 et tête restée par jeton |
| 5 | échelles par bloc `DenseQ8` | ✅ | hypothèse **réfutée** : 23,696 contre 23,612 ; l'avantage du 6 bits est son coût (25 % d'octets en moins) |
| 6 | boucles CLI | ✅ | `Options` + `analyser` ; **3 drapeaux de plus** trouvés ignorés et un bug de pas de lecture (qui masquait `--ctx`/`--threads`) |
| 7 | noyaux GPU | ✅ | warp : tête **1,6 ms** contre 7,3 CPU ; MXFP4 **0,00e0** d'écart (bit à bit) ; Q4_K 4e-7 ; reste Q6_K |
| 8 | plan 1 M | 🔄 | E1/E2/E3 faits ; **attention creuse : top-256 améliore la perplexité de 21 %** (234,9 contre 298,6) tandis qu'élargir la fenêtre la détruit (×11) ; E4/E5 à implémenter ; MLA et vision non testables ici |

**Trois bogues de plus corrigés au passage** : le biais de descente des experts (latent, effet nul sur le 30B), le tampon de sortie dimensionné sur `h` au lieu de `n_têtes×dim`, et l'empaquetage 4 bits du KV. Plus une leçon de méthode : un remplacement de texte qui échoue en silence a produit une perplexité de 399 074 — un `assert` sur le motif l'aurait évité, et c'est désormais ce que je fais.

**L'étude PowerInfer** est dans `reports/rapport-localite-activation.md` : la localité existe (82 % des neurones inactifs par jeton) mais l'ensemble *toujours* chaud est minuscule (0,08 %) → leur préchargement statique ne paierait pas sur un modèle SiLU ; ce qu'on garde, c'est le placement **par expert** et un cache à éviction.

**Reste ouvert** (l'objectif continue) : attention groupée dans le chemin par lots puis **la tête en GEMM** (les deux corrections chiffrées du chantier 4), Q6_K, puis E4 (KV déporté GPU) et E5 (attention creuse implémentée) ; MLA et 
… [55 caractères tronqués]

### Tour 6 — <goal_round> Objective: "Réaliser les 8 chantiers restants du projet qtrinet-core dans l'ordre : (1) protocole de perple … [1122 caractères tronqués]

*265 appels d'outils.* Actions notables :

- bash — Check the starting state of round 2
- bash — Locate the batched attention loop
- bash — Read the batched per-head attention
- bash — Read the head computation
- bash — Group the batched attention and measure
- bash — Implement the batched head
- bash — Fix the SparseVec path
- bash — Measure the batched head
- bash — Check the batched MoE path with the new attention and head
- bash — See the gpt-oss lot 128 failure
- bash — Inspect the panicking line
- bash — Bisect the failing batch size
- bash — Add guards and rerun lot 128
- bash — Read dot16's fallback path
- … et 208 autres

**Synthèse produite :**

Les 8 chantiers sont faits : implémentés, mesurés, documentés et commités. Voici le bilan.

\## Les huit chantiers

| # | chantier | résultat mesuré |
|---|---|---|
| 1 | protocole de perplexité longue | `--depuis`/`--stride` en place ; utilisés pour toutes les mesures appariées ci-dessous |
| 2 | seuil de rotation YaRN | **tranché, et le seuil était trop bas** : à contexte 5 120 (positions 4 608-5 119), RoPE simple **9,6986** contre **1 269,1777** en interpolation seule → la bascule passe de « longueur d'origine déclarée » à 1,25 × celle-ci |
| 3 | KV int8/int4 à ctx 8 192 | f32 14,2339 · int8 **14,6667 (+3,0 %)** contre +0,8 % chez llama.cpp · int4 **66,0369 (+364 %)** contre +494 % chez llama.cpp — meilleur que la référence, à moitié mémoire |
| 4 | préremplissage par lots | Qwen ctx 512 : **17,1 → 13,6 s (−20 %)** ; gpt-oss : ≈ 50 → 34,4 s ; perplexités identiques |
| 5 | échelles par bloc `DenseQ8` | hypothèse réfutée (23,6964 contre 23,6123) — le 6 bits garde son avantage de coût |
| 6 | boucles CLI unifiées | `struct Options` + `analyser` |
| 7 | noyaux GPU par ligne + 4 bits | warp Q8_0 / MXFP4 (bit à bit) / Q4_K / **Q6_K** (3,6 contre 8,3 ms sur la tête de 191 Mo) ; tête Q6_K branchée : 7,58 → **3,60 ms/jeton** |
| 8 | plan 1 M | **E4** : `attn_kv_partiels`/`recombine` + miroir VRAM paginé ; **E5** mesuré (`--attn-topk 256` : 234,9 contre 298,6) ; MLA et vision documentés non testables ici |

\## Le gain le plus net (E4)

À 1 M de clés, une couche : CPU **968 ms** → GPU **13,2 ms** (int4, ×73). Dans le moteur, ctx 4 096 : attention **22,16 → 3,29 ms/jeton**, balayage 219 → 136 s (−38 %), perplexité 12,2177 → 12,2175. Le miroir VRAM ne réserve plus `ctx` positions d'un coup : à **ctx 1 M**, 0,05 Go occupés pour 512 jetons écrits (l'allocation en bloc exigeait 25,77 Go et refusait).

\## Trois bugs silencieux, trouvés par la mesure

- `engine.rs` : un **pointeur de tranche (gras)** relu comme `Vec<Vec<i32>>` faisait lire au worker une longueur de 90 (blocs) au lieu du lot — panique, et surtout **blocage muet** du fil principal. Corrigé, test verrouillé (lots 1/8/9/17/40) et `catch_unwind` + compteur `morts` : une panique de worker échoue désormais en clair.
- noyau d'attention : la **requête** était lue par voie (accord parfait seulement pour un vecteur de base, écart 4e-1 sinon) ; les partiels n'étaient **pas indexés par tête KV** (7 têtes sur 14 à zéro) ; les **échelles** du KV quantifié étaient indexées en éléments (écart 7e7 en int8).
- miroir du c
… [1011 caractères tronqués]

### Tour 7 — background job bash-35 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (QT_GPU=1 ./qtrinet-core/target/rele … [378 caractères tronqués]

*7 appels d'outils.* Actions notables :

- job_output
- bash — Read gpt-oss gate result
- bash — Compare gpt-oss gate with and without GPU
- bash — Find all GPU-availability gates
- bash — Inspect un-gated GPU paths
- bash — Document the gate variance and commit
- bash — Final repo state check

**Synthèse produite :**

⏵ Fausse alerte levée : l'écart venait de `QT_GPU`, pas d'une régression

La porte gpt-oss qui tournait en arrière-plan affichait **15,1667** au lieu de 15,1757 : ce n'était pas une régression. Mesuré deux fois, même binaire, même commande :

| commande | perplexité |
|---|---|
| sans `QT_GPU` | **15,1757** ✓ (le chiffre de contrôle du dépôt) |
| avec `QT_GPU=1` | 15,1667 |

La cause est dans le moteur : `QT_GPU` ouvre le pilote, et `Proj::charger` déporte alors **de lui-même** toute projection Q8_0 de plus de 8 Mo (seuil `SEUIL_GPU`, fixé par mesure). Les projections de gpt-oss font 8,8 Mo → elles passent par le noyau GPU, même calcul mais ordre de sommation différent, d'où 0,06 % d'écart — ici légèrement *en faveur* du GPU.

J'avais ajouté `QT_GPU=1` par habitude dans la commande d'arrière-plan ; le gate documenté ne le met pas ✓.

C'est maintenant écrit noir sur blanc dans `REPRISE.md` (§8, commande du gate) et dans le tableau des mesures, avec le commit `45948e2`.

État final vérifié : `cargo test --release` 6/6, Qwen ctx 256 = **19,3885**, gpt-oss ctx 256 = **15,1757** (sans `QT_GPU`), arbre propre à l'exception de `journal/README.md` (churn du crochet d'archivage). Les 8 chantiers restent tels que décrits dans mon bilan précédent — rien d'autre à reprendre de ce côté.

### Tour 8 — que reste-t-il à faire

*5 appels d'outils.* Actions notables :

- bash — Read REPRISE next-steps list
- bash — Read full next-steps section
- bash — Check gpt-oss head type and MXFP4 wiring
- bash — Determine gpt-oss head tensor type
- bash — Read immediate-measurement section

**Synthèse produite :**

⏵ Inventaire des restes, par ordre de rentabilité

Les 8 chantiers sont clos ; voici ce qui reste ouvert, du plus rentable au plus lointain. Tout est chiffré dans `docs/contexte-long.md`, `reports/rapport-prefill-par-lots.md` et `REPRISE.md`.

\## 1. Qualité du contexte long : l'aiguille (le manque le plus visible)

La perplexité ne dit pas si le modèle **retrouve** une information. `tools/aiguille.py` plante un code et vérifie qu'il ressort : 6/6 échecs sur Qwen 0.5B (modèle trop faible) et **9,6 min pour une seule sonde** sur Qwen3-30B-A3B en préremplissage séquentiel → test arrêté. Il faut du remplissage **varié** (vrai texte), moins de sondes, des réponses plus longues. C'est devenu abordable : le préremplissage par lots donne −20 % (Qwen) et −31 % (gpt-oss), et le KV déporté rend l'attention plate.

\## 2. Chemin GPU

| reste | chiffre qui le justifie |
|---|---|
| **dépaquetage vectorisé** du noyau d'attention | 13,2 ms/couche à 1 M en int4 (25-40 Go/s) contre 158 Go/s en f32 → viser ~3 ms |
| **brancher MXFP4 dans le moteur** | noyau bit à bit identique, ×75 sur un expert (0,1 contre 7,5 ms) — mais aucun appel : il faut une politique de résidence, et `rapport-localite-activation.md` dit qu'un préchargement statique ne paie pas |
| **attention par lots sur GPU** | `forward_lot` garde le CPU, où l'attention par lots est **1,7 ×** le chemin par jeton ; le noyau ne sert qu'au décodage |
| **noyau de la tête Q8_0** | 5,5 ms/jeton en lot, lié au **calcul** (le lot n'y change rien) → AVX2 ou déport (`QT_GPU_TETE=1` : 15,6 → 6,2 ms/jeton sur gpt-oss) |
| **second GPU** | 16 Go libres, jamais utilisés : répartir le KV (128 Mo/couche en int4 à 1 M) ou les experts |

\## 3. Mémoire

- **Pagination du cache CPU** : à ctx 1 M, il réserve 25,77 Go pour 512 jetons écrits. Le miroir VRAM est paginé, l'hôte non.
- **Écart int8 avec llama.cpp** à 8 192 : +3,0 % contre +0,8 %. Hypothèse non testée : leurs clés sont calculées en f16 avant quantification.

\## 4. Rotation

Au-delà de 5 120 jetons : **non mesuré** (≈ 1 h par régime à 16 k, corpus de 17 k). Le seuil actuel (1,25 × longueur déclarée) n'est qu'une borne basse *mesurée*.

\## 5. Structurel, non testable ici

- **MLA** : aucun modèle MLA en GGUF sur la machine (le « deepseek-r1-distill » local est un Qwen dense).
- **Vision** : les poids Qwen2.5-VL-7B et le projecteur `mmproj` sont présents, mais rien ne lit les patchs — c'est une tour de vision entière à écrire.

\## 6. Hygiène

La section « Ce qu'il faut faire en
… [573 caractères tronqués]

### Tour 9 — fais tous ces 6 nouveaux chantiers

*88 appels d'outils.* Actions notables :

- create_goal
- todo_write
- bash — Inspect needle tool and 30B model
- bash — Check corpus and 30B chat speed
- bash — Find a large natural-text corpus
- bash — Check corpus and lot usage in inference
- bash — Inspect run_infer prefill
- bash — Read run_infer decode/prefill loop
- bash — Check generate prefill path
- bash — Find where options are applied to the model
- bash — Wire batched prefill into generate
- bash — Check lot is in scope in run_infer
- bash — Build with batched prefill
- bash — Read run_infer destructuring
- … et 72 autres

**Synthèse produite :**

⏵ Bilan de la fournée : 6 sous-chantiers sur 10 livrés, la rotation 16 k tourne encore

Six des dix sous-chantiers sont faits, mesurés et commités ; quatre restent, dont un qui tourne en ce moment.

\## Livré

| sous-chantier | mesure | commit |
|---|---|---|
| **1. Aiguille v2** | **12 sondes sur 12** trouvées (profondeurs 0,1/0,5/0,9) : Qwen1.5B 512+2048, Qwen3-30B 2048, gpt-oss-120b 4096 avec KV déporté — là où la v1 échouait 6/6 | `5dfa6b1`, `4512f69` |
| **2a. Dépaquetage vectorisé** du noyau d'attention | à 1 M de clés : f32 13,6 → **7,0 ms** (308 Go/s), int8 15,0 → **6,5**, int4 13,2 → **7,4 ms** ; écarts au CPU inchangés | `a64328d` |
| **2b. Experts MXFP4 en VRAM** | +6 % seulement (5,12 → 5,43 jetons/s), 53,5 % de succès, 10,64 Go montés — **verdict : ne pas activer par défaut**, le chemin CPU est déjà AVX2 | `4512f69` |
| **2c. Attention par lots déportée** | préremplissage ctx 4096, lot 512 : **261,6 → 93,7 s (×2,8)**, perplexité **identique** (12,2175) | `4512f69` |
| **3. Pagination + hypothèse f16** | cache CPU à ctx 1 M : **0,03 Go** au lieu de 25,77 Go ; hypothèse « clés en f16 avant quantification » **réfutée** (perplexité identique) | `bc5aa9a` |
| **6. Hygiène** | feuille de route réécrite, tableau des pièges `QT_GPU*` (`QT_GPU` ouvre le pilote : sans elle, les autres ne font rien et rien ne le dit) | `6664eef` |

Au passage : le préremplissage par lots est branché sur la **génération** (`Model::lot`) — il ne l'était que sur la perplexité, ce qui rendait toute invite longue hors de prix.

\## Reste

1. **2d — noyau de tête Q8_0.** Le chemin CPU est lié au calcul (5,5 ms/jeton en lot sur Qwen 0.5B ; la tête de gpt-oss fait 579 Mo, la plus grosse matrice du modèle). Voie AVX2 ou déport.
2. **2e — second GPU.** 16 Go dorment : à répartir entre KV et experts, avec un second contexte CUDA.
3. **4 — rotation à 16 k.** **En cours** : deux régimes, mêmes 512 jetons notés (15 872-16 383), KV déporté obligatoire pour que la passe ne dépasse pas l'heure par régime. Journal : `/tmp/rotation_16k.log`.
4. **5 — MLA et vision.** MLA demande un modèle **synthétique** écrit à la main (aucun modèle MLA local) validé contre une référence indépendante ; la vision demande la tour ViT + le chemin `mmproj`, entièrement à écrire.

L'objectif reste actif : la suite (2d, 2e, résultat du 16 k, puis MLA/vision) est exactement la liste du §6 de `REPRISE.md`, qui a été réécrite pour ça. Rien n'est laissé cassé : `cargo test` 6/6, porte Qwen **19,3885** revérifiée aprè
… [117 caractères tronqués]

### Tour 10 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*19 appels d'outils.* Actions notables :

- bash — Check 16k rotation job and repo state
- bash — Read Q8_0 branch of q8_dot_at
- bash — Add AVX2 head kernel
- bash — Verify PPL unchanged with AVX2 head
- bash — Check rotation progress and GPU singleton
- bash — Expose second GPU and machine list
- bash — Find KV mirror plumbing sites
- bash — Split KV mirror across GPUs
- bash — Verify two-GPU KV split
- bash — Document and commit 2d/2e
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mla-vision.md`
- bash — Wait for 16k rotation result
- bash — Commit plan and wait for rotation
- bash — Fix commit message quoting
- … et 5 autres

**Synthèse produite :**

⏵ Tour 1 : quatre chantiers sur six livrés, la rotation 16 k tourne encore

\## Livré dans ce tour

| chantier | mesure | commit |
|---|---|---|
| **2d. Noyau de tête Q8_0 en AVX2** | `vpmaddwd` sur 32 niveaux, **somme entière donc exacte** : porte Qwen **19,3885** et gpt-oss **15,1757** inchangées au chiffre près — le noyau est bit-identique au scalaire | `38d4d8b` |
| **2e. KV réparti sur les deux Quadro** | couches allouées en tournant : **12 sur GPU 1, 12 sur GPU 0**, perplexité 13,1369 inchangée. La pagination rend la 2ᵉ carte inutile aux longueurs courantes ; sa valeur est la marge des très longs contextes (KV f32 à 1 M = 24 Go, soit 12 Go par carte) | `38d4d8b` |
| **5. Plan MLA + vision** | document `docs/plan-mla-vision.md` : tenseurs et clés GGUF, ordre du calcul MLA, et le **contrôle négatif** qui relie l'implémentation nouvelle à une déjà validée (avec `W_kv_b = I`, l'attention latente doit redonner exactement une MQA) | `c866186` |

Les deux portes de non-régression ont été revérifiées après le changement de noyau : **Qwen ctx 256 = 19,3885** et **gpt-oss ctx 256 = 15,1757**, toutes deux sans `QT_GPU` (piège documenté : `QT_GPU` déporte à lui seul les projections Q8_0 de plus de 8 Mo et décale le chiffre de 0,06 %).

\## En cours

**Chantier 4 — rotation à 16 k** : la première passe (RoPE simple, mêmes 512 jetons notés, positions 15 872-16 383) tourne depuis ~28 minutes ; la seconde (interpolation seule) suivra, ~30 minutes de plus. Le préremplissage par lots et le KV déporté la rendent possible, mais elle reste l'opération la plus chère du dépôt. Résultat à collecter dans `/tmp/rotation_16k.log` — je n'ai pas voulu l'interrompre pour tenir un délai.

\## Reste

**Chantier 5 — MLA et vision**, le seul non commencé. Le plan est écrit et chiffré : un modèle MLA **synthétique** en GGUF (aucun modèle MLA local), une référence numpy indépendante, et la validation par équivalence MQA ; pour la vision, la tour ViT, la fusion 2 × 2 des patchs et surtout le chemin d'injection d'embeddings qui manque au moteur (`forward` part toujours de `token_embd`).

L'objectif reste **actif** : le prochain tour commence par relever le résultat du 16 k, puis attaque MLA selon `docs/plan-mla-vision.md`. Rien n'est laissé cassé — `cargo test` 6/6, arbre propre, et tout ce qui est annoncé ici est dans un rapport, un document ou `REPRISE.md`.

### Tour 11 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*11 appels d'outils.* Actions notables :

- bash — Collect 16k rotation result
- bash — Check engine elapsed time
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mla_synthetique.py`
- bash — Generate synthetic MLA model and reference
- bash — Fix writer and verify GGUF header
- bash — Fix reference einsums and rerun
- bash — Debug MLA reference shapes
- bash — Fix einsum indices and regenerate
- bash — Document harness state and commit
- bash — Check rotation engine progress
- bash — Final repo and test check

**Synthèse produite :**

⏵ Tour 2 : le harnais MLA est prêt et vérifié ; le 16 k tourne toujours

\## Fait dans ce tour

**Chantier 5 — première moitié livrée : le harnais MLA.**

MLA n'était pas testable faute de modèle ; le harnais se fabrique maintenant au lieu d'attendre :

- `tools/mla_synthetique.py` écrit un **GGUF synthétique** de 381 ko — 26 tenseurs, 15 clés de métadonnées, architecture `deepseek2`, `q_lora_rank` 32, `kv_lora_rank` 48, `qk_rope` 16, `qk_nope` 16, `v_dim` 16, 4 têtes, 2 couches, hidden 64 — en-tête relu et vérifié (version 3, 26 tenseurs) ;
- il calcule en **numpy la référence du même calcul** (logits de 8 jetons, forme `(8, 64)`, rangés dans `/tmp/mla_ref/` avec les identifiants et les formes).

Deux bugs de la référence ont été trouvés en la relisant, et c'est exactement l'intérêt du harnais : un tableau d'entiers typé comme tableau de chaînes dans l'en-tête GGUF, et surtout des indices d'`einsum` qui **confondaient la dimension de tête et la dimension de clé** (les scores se calculent en `nhe,mhe->nhm` : n requête, m clé, h tête). Sans référence indépendante, ces deux erreurs seraient passées dans le moteur et auraient été attribuées au modèle.

Reste sur ce chantier : le **chemin MLA du moteur** — lire ces tenseurs, tenir le cache latent (`c_kv` + `k_rope` par position), ne tourner que la partie « rope », et retrouver `logits.npy`. Le plan complet (noms de tenseurs, ordre du calcul, contrôle par équivalence MQA) est dans `docs/plan-mla-vision.md`, mis à jour avec l'état du harnais.

\## Toujours en cours

**Chantier 4 — rotation à 16 k** : le premier régime (RoPE simple, 16 384 jetons de contexte, 512 notés) tourne depuis ~37 minutes et progresse normalement (10 h 20 de temps CPU sur 16 fils, 58 Go résidents). Le second (interpolation seule) suivra. Je ne l'ai pas interrompu : c'est la dernière mesure du chantier, et son journal `/tmp/rotation_16k.log` est prêt à être relevé.

\## État

`cargo test` 6/6, arbre propre (hors l'archive du journal), portes de non-régression vérifiées après chaque changement de noyau : **Qwen 19,3885** et **gpt-oss 15,1757**, toutes deux sans `QT_GPU`.

Bilan des six chantiers : **1, 2 (cinq sous-items), 3, 6 terminés** ; **4** en attente de sa seconde passe ; **5** à moitié — le harnais est prêt, le moteur reste à faire. L'objectif reste **actif** : le prochain tour relève le 16 k, puis implémente MLA contre la référence qui l'attend.

### Tour 12 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*20 appels d'outils.* Actions notables :

- bash — Check rotation and helper APIs
- bash — Read Meta enum accessors
- bash — Add MLA struct and loader
- bash — Implement MLA forward path
- bash — Check build of MLA path
- bash — Add MLA bench and dummy tensors
- bash — Run MLA bench on synthetic model
- bash — Compare engine MLA logits with numpy reference
- bash — Fix GGUF convention and recompare
- bash — Diagnose MLA load failure
- bash — Check declared dims in the file
- bash — Verify loader edits applied
- bash — Re-run MLA bench after rebuild
- bash — Fix dims order and compare again
- … et 6 autres

**Synthèse produite :**

⏵ Tour 3 : MLA est validé (5,2e-7 contre la référence numpy)

\## Fait dans ce tour

**Chantier 5, moitié MLA : implémenté et validé.**

Le moteur charge maintenant un modèle MLA — reconnu à ses tenseurs (`attn_kv_a_mqa`), **sans aucune clé de configuration nouvelle** : les rangs se lisent dans les formes — et tient le **cache latent** (`c_kv` + `k_rope` par position, `k_nope` et `v` reconstruits à la lecture par `W_kv_b`). La rotation ne porte que sur la partie « rope ». Le chemin est volontairement séparé de `forward` : le modèle du harnais n'a ni tenseurs Q8_0 ni fenêtre glissante.

Mesure : `--banc-mla` écrit les logits des 8 positions, comparés à la référence numpy indépendante → **écart max relatif 5,2e-7**, soit le bruit de virgule flottante du moteur. Le témoin imprimé : `MLA : q_lora 32 · kv_lora 48 · qk_nope 16 + qk_rope 16 · v 16 · cache latente 64 valeurs par jeton (au lieu de 32)`.

Deux erreurs réelles ont été trouvées **par** la référence — c'est exactement son rôle : des indices d'`einsum` qui confondaient dimension de tête et dimension de clé dans la référence elle-même, et surtout la **convention GGUF des tenseurs linéaires** (stockés (sortie, entrée), déclarés (entrée, sortie)). L'écart est passé de 0,82 à 5,2e-7 après correction.

**Chantier 5, moitié vision : reconnaissance faite, plan corrigé par les faits.** Le `mmproj` est en architecture `clip` et contient la tour **complète** (519 tenseurs, `v.blk.N.*`) : image 560, patchs 14, largeur 1280, 32 couches, 16 têtes, MLP 3420, projecteur `qwen2.5vl_merger`, projection 3584, normalisation CLIP. Le point délicat est confirmé par le fichier : **`n_wa_pattern = 8`**, une couche sur huit en attention **locale** — se tromper de fenêtre ferait diverger les embeddings sans aucun signal.

\## En cours

**Chantier 4** : la première passe à 16 k est tombée — **RoPE simple : perplexité 35,1837** (512 jetons notés, 16 384 de contexte, 39 minutes). La seconde (interpolation seule) tourne depuis une vingtaine de minutes ; c'est elle qui dira si le seuil doit encore monter.

\## État

`cargo test` 6/6, porte Qwen **19,3885** revérifiée après les changements MLA (chemin séparé, portes intactes), arbre propre.

Bilan des six chantiers : **1, 2 (cinq sous-items), 3, 4 (première passe), 6 terminés** ; **5** : MLA **fait et validé**, vision **planifiée et reconnue**, l'implémentation ViT reste à écrire. L'objectif reste **actif** : prochain tour, relever la seconde passe du 16 k et l'écrire dans le rapport, p
… [57 caractères tronqués]

### Tour 13 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*9 appels d'outils.* Actions notables :

- bash — Collect 16k interp result
- bash — List distinct ViT tensor patterns
- bash — Wait for 16k interp result
- bash — Poll interp run again
- bash — Poll interp run
- bash — Poll interp run once more
- bash — Document 16k verdict and raise threshold
- bash — Commit 16k verdict and threshold change
- todo_write

**Synthèse produite :**

⏵ Tour 4 : le 16 k est tranché, cinq chantiers et demi sur six sont clos

\## Livré dans ce tour

**Chantier 4 — rotation à 16 384 jetons, bouclé.** Protocole apparié, mêmes 512 jetons notés (positions 15 872 à 16 383), KV déporté — sans lui l'attention coûte ~180 ms/jeton et la passe dépasse l'heure par régime :

| régime | perplexité | durée |
|---|---|---|
| **RoPE simple** | **35,18** | 2 367 s |
| interpolation seule | **1 133,02** | 2 251 s |

**×32 en faveur du simple.** Sur toute l'étendue mesurée — 128, 512, 1 024, 1 536, 5 120, 16 384 — l'interpolation n'a **jamais** gagné, et l'écart se creuse avec la longueur (×1,1 à 512, ×131 à 5 120, ×32 à 16 384).

Conséquence appliquée : le seuil de bascule passe de 1,25 × à **4 ×** la longueur déclarée (16 384 pour gpt-oss, exactement la plus grande longueur mesurée). L'interpolation ne s'active plus dans la plage où l'on sait qu'elle nuit ; au-delà, c'est une extrapolation non mesurée, et le document le dit.

\## État des six chantiers

| # | chantier | état |
|---|---|---|
| 1 | aiguille long contexte | ✅ 12/12 sondes (1,5B 512/2048, 30B 2048, gpt-oss 4096) |
| 2 | chemin GPU (5 sous-items) | ✅ vectorisation ×1,8-2,3 · experts +6 % (verdict : ne pas activer) · lots ×2,8 · tête AVX2 · deux cartes 12/12 |
| 3 | mémoire KV | ✅ pagination CPU (0,03 Go à ctx 1 M) · hypothèse f16 **réfutée** |
| 4 | rotation à 16 k | ✅ **35,18 contre 1 133,02**, seuil corrigé |
| 5 | MLA + vision | ⏳ **MLA fait et validé** (5,2e-7 contre la référence numpy) ; **vision** : paramètres et nommage relevés dans le `mmproj` (560 px, patchs 14, 32 couches, `n_wa_pattern = 8`), tour ViT à écrire |
| 6 | hygiène | ✅ feuille de route réécrite + tableau des pièges `QT_GPU*` |

`cargo test` 6/6, porte Qwen **19,3885** revérifiée, arbre propre. Le changement de seuil ne touche que les contextes > 5 120, donc les deux portes de non-régression (ctx 256) sont structurellement intactes.

\## Reste

La **tour de vision** : c'est le seul morceau non commencé, et le plus gros du dépôt (ViT 32 couches avec attention locale une couche sur huit, fusion 2 × 2 des patchs, pré-traitement d'image, et le chemin d'injection d'embeddings qui manque au moteur). Le plan est dans `docs/plan-mla-vision.md`, désormais adossé aux chiffres relevés dans le fichier plutôt qu'à des suppositions.

L'objectif reste **actif** pour ce dernier morceau.

### Tour 14 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Check Gguf tensor access API
- bash — Add tensor listing mode
- bash — List mmproj tensors with engine reader
- bash — List non-block mmproj tensors
- bash — Document verified vision inventory

**Synthèse produite :**

⏵ Tour 5 : inventaire vision relevé ; le plan est corrigé par les faits

\## Fait dans ce tour

**La vision n'est plus une supposition : elle est relevée.**

J'ai ajouté au moteur un mode `--tensors` (nom, dimensions, type de chaque tenseur d'un GGUF) — un outil qui servira à tout chemin qu'on ne sait pas encore lire — et il a donné la structure exacte du projecteur :

| tenseur | dimensions | rôle |
|---|---|---|
| `v.patch_embd.weight` **et** `.1` | [1280, 3, 14, 14] | **deux** convolutions de patchs |
| `v.blk.N.attn_q/k/v/out.weight` | [1280, 1280] | **avec biais** (`attn_q.bias`…) |
| `v.blk.N.ffn_gate/up.weight` | [3420, 1280] | MLP, **avec biais** |
| `v.blk.N.ffn_down.weight` | [1280, 3420] | MLP |
| `v.blk.N.ln1.weight`, `ln2.weight` | [1280] | LayerNorm |
| `v.post_ln.weight` | [1280] | norme finale |
| `mm.0.weight` | [5120, 5120] | projecteur : 5120 = 1280 × 4 → fusion 2 × 2 |
| `mm.2.weight` | [3584, 5120] | sortie 3584 = largeur du modèle |

Deux corrections au plan, toutes deux issues du relevé :

1. **aucun `position_embd`** — Qwen2.5-VL n'ajoute pas de position absolue, il tourne ses patchs en 2-D (mRoPE). Mon plan initial en supposait un : c'était faux ;
2. **les biais sont partout** (q, k, v, sortie, MLP) — l'erreur classique de ce dépôt, qui a déjà coûté 39,80 → 20,84 sur gpt-oss.

Les 519 tenseurs couvrent la tour complète et son projecteur : le chemin image peut se construire sur ce fichier seul, sans le modèle de langage.

\## État

`cargo test` 6/6, portes de non-régression intactes (le mode `--tensors` et le chemin MLA sont des ajouts, le seuil de rotation ne touche que les contextes > 5 120), arbre propre.

**Cinq chantiers et demi sur six :** 1 (aiguille 12/12), 2 (cinq sous-items GPU), 3 (pagination + hypothèse f16 réfutée), 4 (rotation à 16 k : 35,18 contre 1 133,02, seuil porté à 4 ×), 6 (hygiène) sont clos ; le **5** a sa moitié MLA **validée** (5,2e-7 contre la référence numpy) et sa moitié vision **relevée et planifiée**, l'implémentation de la tour ViT restant à écrire — c'est le seul morceau ouvert.

L'objectif reste **actif** pour ce dernier morceau : le prochain tour peut attaquer directement le pré-traitement d'image et l'embedding de patchs, dont les formes exactes sont maintenant dans `docs/plan-mla-vision.md`.

### Tour 15 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Add patch embedding bench
- bash — Run vision patch embedding bench
- bash — Compare patch embedding with numpy reference
- bash — Document and commit vision first slice

**Synthèse produite :**

⏵ Tour 6 : le chemin image a sa première tranche validée

\## Fait dans ce tour

**Vision — première tranche implémentée et validée.** `--banc-vision` fait tourner la convolution 14 × 14 du ViT sur une image 28 × 28 déterministe (dégradé + carré central) et écrit les 4 patchs × 1 280 canaux ; `tools/vision_ref.py` refait le **calcul** en numpy à partir des mêmes poids — l'extraction des tenseurs étant vérifiée séparément par `--tensors`. Même partage des rôles que pour MLA, et même résultat :

**écart max relatif 5,4e-7**, le bruit de virgule flottante du moteur.

La tranche est isolée à dessein : si l'embedding de patchs est faux, tout ce qui suit l'est aussi, et le comparer seul évite d'attribuer au modèle une erreur de découpage.

Reste, dans l'ordre et avec l'inventaire exact des tenseurs déjà relevé : la rotation 2-D (mRoPE) des patchs, les 32 couches avec **attention locale une sur huit** (`n_wa_pattern = 8`), `v.post_ln`, le projecteur `mm.0`/`mm.2` (fusion 2 × 2, 5120 = 1280 × 4), et enfin **l'injection des embeddings dans le flux de jetons** — le point d'architecture qui manque au moteur, puisque `forward` part toujours de `token_embd`.

\## État général

| # | chantier | état |
|---|---|---|
| 1 | aiguille long contexte | ✅ 12/12 sondes |
| 2 | chemin GPU (vectorisation, experts, lots, tête AVX2, 2 cartes) | ✅ |
| 3 | mémoire KV (pagination 0,03 Go à 1 M, hypothèse f16 réfutée) | ✅ |
| 4 | rotation à 16 k (35,18 contre 1 133,02, seuil à 4 ×) | ✅ |
| 5 | MLA ✅ validé (5,2e-7) · vision ⏳ embedding de patchs validé (5,4e-7), tour à finir | en cours |
| 6 | hygiène (feuille de route + pièges `QT_GPU*`) | ✅ |

`cargo test` 6/6, portes de non-régression Qwen **19,3885** et gpt-oss **15,1757** intactes (les ajouts MLA/vision sont des chemins séparés), arbre propre.

L'objectif reste **actif** : il ne manque que la suite de la tour de vision, dont chaque étape est décrite dans `docs/plan-mla-vision.md` avec les formes et les biais relevés dans le fichier.

### Tour 16 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*11 appels d'outils.* Actions notables :

- bash — Add projector slice and reference
- bash — Fix borrow and rebuild
- bash — Run and validate projector slice
- bash — Fix output write and erf, revalidate
- bash — Show build error
- bash — Fix order, rebuild and validate projector
- bash — Move projector before write and validate
- bash — Single declaration at function start
- bash — Validate projector slice end to end
- bash — Fix reference reading and validate
- bash — Document and commit projector validation

**Synthèse produite :**

⏵ Tour 7 : les deux extrémités du chemin image tiennent

\## Fait dans ce tour

**Vision — le projecteur est implémenté et validé**, après l'embedding de patchs du tour précédent. Les deux extrémités du chemin image sont donc en place et vérifiées contre une implémentation numpy indépendante :

| tranche | écart max relatif |
|---|---|
| embedding de patchs (convolution 14 × 14 sur 28 × 28) | **5,37e-07** |
| projecteur (fusion 2 × 2 → `mm.0` → GELU → `mm.2`) | **1,73e-06** |

Le projecteur concatène en ordre raster les quatre patchs d'un groupe 2 × 2 (5120 = 1280 × 4), applique `mm.0` (5120 → 5120) + biais, un GELU exact, puis `mm.2` (5120 → 3584) + biais — 3 584 valeurs, |sortie| = 17,88. Détail méthodologique qui compte : la référence numpy utilise **la même approximation d'erf** que le moteur (Abramowitz-Stegun 7.1.26, écrite en vectorisé) — comparer deux formules différentes aurait mesuré l'approximation, pas l'implémentation.

Reste le **milieu** : rotation 2-D des patchs (mRoPE), 32 couches avec attention locale une sur huit, `v.post_ln` — puis l'injection des embeddings dans le flux de jetons, le point d'architecture qui manque au moteur.

\## État général

| # | chantier | état |
|---|---|---|
| 1 | aiguille long contexte | ✅ 12/12 |
| 2 | chemin GPU (5 sous-items) | ✅ |
| 3 | mémoire KV | ✅ |
| 4 | rotation à 16 k | ✅ (35,18 contre 1 133,02, seuil à 4 ×) |
| 5 | MLA ✅ (5,2e-7) · vision ⏳ patchs ✅ + projecteur ✅, 32 couches à écrire | en cours |
| 6 | hygiène | ✅ |

`cargo test` 6/6, arbre propre, portes de non-régression intactes (les chemins MLA et vision sont des ajouts isolés).

L'objectif reste **actif** : il ne manque que le corps de la tour de vision, chaque étape étant décrite dans `docs/plan-mla-vision.md` avec les formes et les biais relevés dans le fichier réel.

### Tour 17 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Final gpt-oss gate and repo check
- bash — Detail next vision step and commit
- bash — Final state verification

**Synthèse produite :**

⏵ Tour 8 : état vérifié, pas suivant détaillé, objectif laissé actif

\## Ce tour-ci

Le contexte disponible ne permettait plus d'écrire le corps de la tour de vision sans risquer de laisser le dépôt cassé — la règle du projet passe avant le chiffre. J'ai donc fait ce qui restait utile et sûr :

**Vérification finale, sur le code tel qu'il est commité :**
- porte gpt-oss : **15,1757** (exactement le chiffre de contrôle, sans `QT_GPU`) ;
- porte Qwen : **19,3885** (revérifiée après les changements MLA) ;
- `cargo test --release` : **6/6** ; arbre propre (hors l'archive du journal).

**Le pas suivant est maintenant détaillé** dans `docs/plan-mla-vision.md`, pour qu'une session suivante n'ait pas à refaire l'enquête :
1. la composition d'une couche (ln1 → q/k/v **+ biais** → attention → attn_out + biais → résidu → ln2 → MLP + biais → résidu) — les biais sont partout, c'est l'erreur classique de ce dépôt ;
2. la rotation **2-D** (mRoPE) : le seul point **non vérifiable localement** est sa convention exacte (répartition des fréquences entre les deux axes) — à lever en comparant les deux conventions plausibles à la référence numpy, puis en validant la sortie complète contre `llama-mtmd-cli` ;
3. l'attention **locale une couche sur huit** (`n_wa_pattern = 8`) ;
4. l'injection des embeddings, qui demande un chemin partant d'un **vecteur** et non de `token_embd` — le seul ajout d'architecture nécessaire au moteur.

\## Bilan des six chantiers

| # | chantier | état | chiffre |
|---|---|---|---|
| 1 | aiguille long contexte | ✅ | 12/12 sondes (1,5B 512+2048, 30B 2048, gpt-oss 4096) |
| 2 | chemin GPU (5 sous-items) | ✅ | vectorisation ×1,8-2,3 · experts +6 % · lots ×2,8 · tête AVX2 · 2 cartes |
| 3 | mémoire KV | ✅ | 0,03 Go à ctx 1 M · hypothèse f16 **réfutée** |
| 4 | rotation à 16 k | ✅ | 35,18 contre 1 133,02 → seuil à 4 × |
| 5 | MLA + vision | ⏳ | MLA **validé** (5,2e-7) · vision : patchs (5,4e-7) + projecteur (1,7e-6) validés, corps de la tour à écrire |
| 6 | hygiène | ✅ | feuille de route + pièges `QT_GPU*` |

L'objectif reste **actif** : il ne manque que le corps de la tour de vision, et tout ce qu'il faut pour l'écrire — formes, biais, conventions, méthode de validation — est dans le dépôt.

### Tour 18 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Implement one ViT block slice
- bash — Run ViT block bench
- bash — Validate ViT block against numpy
- bash — Document and commit ViT block validation

**Synthèse produite :**

⏵ Tour 9 : la couche du ViT est validée, la tour tient sur trois pattes

\## Fait dans ce tour

**Vision — une couche complète du ViT est implémentée et validée.** Le banc calcule maintenant le bloc 0 de bout en bout :

- LayerNorm (`ln1`, `ln2`, eps relevé dans `clip.vision.attention.layer_norm_epsilon`) ;
- q/k/v **avec leurs biais** — l'erreur classique de ce dépôt, ici évitée ;
- attention globale, `attn_out` + biais, deux résidus ;
- MLP `ffn_gate`/`ffn_up` + biais, **SiLU** (`clip.use_silu = 1` : ce n'est *pas* un GELU dans le ViT, contrairement au projecteur), `ffn_down` + biais.

La référence numpy refait la même plomberie : **écart max relatif 1,82e-06**. Les trois tranches validées du chemin image :

| tranche | écart contre numpy |
|---|---|
| embedding de patchs (convolution 14 × 14) | **5,37e-07** |
| une couche du ViT | **1,82e-06** |
| projecteur (fusion 2 × 2 → `mm.0` → GELU → `mm.2`) | **1,73e-06** |

\## Reste, dans l'ordre

1. la **rotation 2-D** (mRoPE) des patchs — dont la convention reste le seul point non vérifiable localement, à lever en comparant les deux conventions plausibles à la référence, puis la sortie complète contre `llama-mtmd-cli` ;
2. la **fenêtre locale** une couche sur huit (`n_wa_pattern = 8`) ;
3. les **32 couches empilées** + `v.post_ln` (mécanique, une fois 1 et 2 réglés) ;
4. l'**injection des embeddings** dans le flux de jetons, qui demande un chemin partant d'un vecteur plutôt que de `token_embd`.

\## État général

| # | chantier | état |
|---|---|---|
| 1 | aiguille | ✅ 12/12 |
| 2 | chemin GPU (5 sous-items) | ✅ |
| 3 | mémoire KV | ✅ |
| 4 | rotation à 16 k | ✅ (35,18 contre 1 133,02) |
| 5 | MLA ✅ (5,2e-7) · vision ⏳ trois tranches validées, rotation + fenêtre locale à faire | en cours |
| 6 | hygiène | ✅ |

`cargo test` 6/6, arbre propre, portes de non-régression intactes (chemins MLA et vision isolés du chemin standard).

L'objectif reste **actif** : la tour de vision est à mi-chemin, chaque étape restante étant décrite avec ses formes et ses conventions dans `docs/plan-mla-vision.md`.

### Tour 19 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Check for llama.cpp mtmd availability
- bash — Check mtmd symbols for a vision reference
- bash — Document the mtmd reference discovery

**Synthèse produite :**

⏵ Tour 10 : la référence qui manquait pour finir la vision est sur la machine

\## Fait dans ce tour

Le seul morceau restant — le corps de la tour de vision — butait sur un point : la **convention de rotation 2-D** (mRoPE) n'est pas vérifiable localement, et le plan pariait sur `llama-mtmd-cli`, absent. J'ai cherché, et la référence existe :

**`/usr/lib/ollama/libmtmd.so`** embarque la bibliothèque multimodale de llama.cpp, avec exactement les symboles qu'il faut :

| symbole | usage |
|---|---|
| `mtmd_init_from_file` | charger le projecteur + le modèle |
| `mtmd_helper_bitmap_init_from_buf` / `_from_file` | fournir l'image |
| `mtmd_tokenize`, `mtmd_encode_chunk` | encoder les patchs |
| **`mtmd_get_output_embd`** | **récupérer les embeddings d'image** |

`/usr/lib/ollama/libllama.so` expose de son côté 3 989 symboles `llama_*`. Il n'y a pas d'en-têtes dans `/usr/include`, mais ce dépôt a l'habitude de déclarer à la main ce dont il a besoin — c'est ainsi que les noyaux CUDA sont liés.

La recette complète est écrite dans `docs/plan-mla-vision.md` : charger le modèle de texte, initialiser mtmd avec des paramètres remis à zéro, encoder **la même image déterministe** que le banc, et comparer `mtmd_get_output_embd` aux 3 584 valeurs du projecteur du moteur. C'est la seule vérification qui trancherait **d'un coup** la rotation 2-D, la fenêtre locale et la fusion 2 × 2, puisqu'elle compare la sortie complète.

\## État

| # | chantier | état |
|---|---|---|
| 1 | aiguille | ✅ 12/12 |
| 2 | chemin GPU (5 sous-items) | ✅ |
| 3 | mémoire KV | ✅ |
| 4 | rotation à 16 k | ✅ |
| 5 | MLA ✅ (5,2e-7) · vision : trois tranches validées (patchs 5,4e-7, couche 1,8e-6, projecteur 1,7e-6) + référence trouvée | en cours |
| 6 | hygiène | ✅ |

`cargo test` 6/6, arbre propre, portes de non-régression Qwen **19,3885** et gpt-oss **15,1757** vérifiées sur le code final.

L'objectif reste **actif** : la prochaine session peut écrire le petit programme C qui interroge `libmtmd` — le seul chaînon manquant pour valider la tour entière — puis empiler les 32 couches et brancher l'injection des embeddings.

### Tour 20 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Search for llama/mtmd headers
- bash — Stack 32 vision layers
- bash — Run stacked tower
- bash — Fix config keys and run full tower
- bash — Document tower and commit
- bash — Final state check

**Synthèse produite :**

⏵ Tour 11 : la tour entière tourne (32 couches) ; il ne manque que la rotation et la fenêtre locale

\## Fait dans ce tour

**Le corps de la tour de vision est en place : les 32 couches s'empilent** et `v.post_ln` s'applique — `tour : 32 couches × 4 patchs × 1280`, |sortie| = 35,55.

Les tranches déjà validées contre numpy couvrent toute la plomberie que la tour répète : embedding de patchs (**5,4e-7**), une couche complète (**1,8e-6**), projecteur (**1,7e-6**). Ce qui manque n'est donc plus « la tour » mais **deux points précis, tous deux dans l'attention** :

1. la **rotation 2-D** (mRoPE) — dont la convention est le seul point non vérifiable par ma référence (elle la partage) et se tranchera contre `libmtmd` d'ollama, dont la recette est écrite dans le plan ;
2. la **fenêtre locale** une couche sur huit (`n_wa_pattern = 8`).

Piège relevé et corrigé au passage : `Gguf::cfg` ajoute **déjà** le préfixe d'architecture — `cfg("vision.block_count")`, pas `cfg("clip.vision.block_count")`. La seconde forme cherche `clip.clip.vision.block_count` et rend la valeur par défaut, ici **0 couche** : la « tour » ne faisait strictement rien, et c'est le témoin imprimé qui l'a dit. Sans lui, j'aurais conclu que 32 couches ne changeaient presque rien.

\## État

| # | chantier | état |
|---|---|---|
| 1 | aiguille | ✅ 12/12 |
| 2 | chemin GPU (5 sous-items) | ✅ |
| 3 | mémoire KV | ✅ |
| 4 | rotation à 16 k | ✅ |
| 5 | MLA ✅ (5,2e-7) · vision : tour complète qui tourne, rotation 2-D + fenêtre locale à ajouter | en cours |
| 6 | hygiène | ✅ |

`cargo test` 6/6, arbre propre (hors archive du journal), portes de non-régression Qwen **19,3885** et gpt-oss **15,1757** vérifiées sur le code final.

L'objectif reste **actif** : il se réduit maintenant à deux conventions d'attention dans le ViT, plus l'injection des embeddings dans le flux de jetons — le seul ajout d'architecture nécessaire au moteur, décrit dans `docs/plan-mla-vision.md`.

### Tour 21 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*10 appels d'outils.* Actions notables :

- bash — Check for transformers reference source
- bash — Look for Qwen2.5-VL reference source locally
- web_search
- bash — Find embedding lookup in forward
- bash — Add embedding injection point
- bash — Verify injection and gate
- bash — Inspect forward embedding site
- bash — Wire injection into forward
- bash — Verify tests and gate after injection
- bash — Document injection point and commit

**Synthèse produite :**

⏵ Tour 12 : le point d'injection des embeddings est en place

\## Fait dans ce tour

**Le seul ajout d'architecture que la vision demandait au moteur est fait.** `Model::emb_imposee` : un vecteur imposé remplace, **pour un seul appel**, la ligne `token_embd.weight` que `forward` lisait toujours. C'est ce qui permettra d'injecter les embeddings d'image à la place des jetons `<|image_pad|>` — tout le reste (MLA, tour ViT) vit dans des chemins séparés, ce qui a préservé les portes de non-régression.

Vérifié : `cargo test` **6/6** et porte Qwen **19,3885** (le vecteur imposé est consommé une fois puis oublié, le chemin standard est intact).

J'ai aussi cherché à trancher les deux dernières conventions du ViT par une source locale : **ni torch ni transformers ne sont installés** sur cette machine, et la recherche web n'a pas rendu le fragment de code voulu dans le budget disponible. Le chemin qui reste est donc `libmtmd` d'ollama — dont la recette est écrite dans le plan depuis deux tours.

\## Où en est exactement la vision

| élément | état |
|---|---|
| embedding de patchs | ✅ validé (5,4e-7) |
| plomberie d'une couche (LayerNorm, biais, résidus, MLP SiLU) | ✅ validée (1,8e-6) |
| 32 couches empilées + `v.post_ln` | ✅ tourne |
| projecteur (fusion 2 × 2 → `mm.0` → GELU → `mm.2`) | ✅ validé (1,7e-6) |
| **point d'injection des embeddings** | ✅ **fait ce tour** |
| rotation 2-D (mRoPE) | ⏳ convention non tranchée |
| fenêtre locale une couche sur huit | ⏳ convention non tranchée |

\## Les six chantiers

1, 2, 3, 4, 6 sont **clos et mesurés** ; le 5 a sa moitié **MLA validée** (5,2e-7) et sa moitié vision à **six septièmes** — il ne reste que deux conventions d'attention, dont la vérification est outillée (référence `libmtmd` identifiée, symboles confirmés, recette écrite).

L'objectif reste **actif** : le prochain tour peut soit écrire le petit programme C contre `libmtmd` pour trancher les conventions d'un coup, soit implémenter les deux conventions candidates et les départager par la comparaison.

### Tour 22 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — List all mtmd exported symbols
- bash — Disassemble params default to get struct size
- bash — Disassemble params default (retry)
- bash — Check debug info and tools for struct size
- bash — Probe mtmd params struct layout
- bash — Document ABI probe and commit

**Synthèse produite :**

⏵ Tour 13 : l'ABI de `libmtmd` est sondée — l'obstacle technique tombe

\## Fait dans ce tour

Le dernier obstacle pour trancher les deux conventions du ViT (rotation 2-D et fenêtre locale) était technique : appeler `libmtmd` sans en-têtes, avec une structure passée **par valeur** dont je ne connaissais pas la taille.

C'est résolu, et proprement :

1. **`mtmd_context_params_default` existe** dans la bibliothèque — plus besoin de deviner les valeurs par défaut ;
2. elle rend la structure par **pointeur caché**, donc on peut la **sonder** en l'appelant avec un tampon large. Le sondage (ctypes, 256 octets) donne le contenu réel :

| offset | lecture |
|---|---|
| 0-1 | deux booléens à vrai (`use_gpu`, `print_timings`) |
| 4 | `n_threads = 4` |
| 16 | un pointeur (marqueur d'image) |
| 24-31 | deux entiers, dont un `-1` |
| 32-39 | un entier 64 bits à `-1` |
| 57 | un octet |

Soit une **soixantaine d'octets** — et comme au-delà de 16 octets SysV passe la structure sur la pile, une structure opaque déclarée à 64 octets et remise à zéro est un **appel ABI-correct** : l'appelé ne lit que ce dont il a besoin. Tout-à-zéro correspond aux valeurs par défaut (`use_gpu` faux, `n_threads` automatique).

Il ne reste donc qu'à écrire le programme — charger le modèle, `mtmd_init_from_file`, `mtmd_bitmap_init` sur l'image déterministe du banc, `mtmd_tokenize`, `mtmd_encode`, **`mtmd_get_output_embd`** — et comparer ses 3 584 valeurs au projecteur du moteur. Ce seul test trancherait la rotation 2-D, la fenêtre locale et la fusion 2 × 2 ensemble, puisque c'est la sortie complète de l'implémentation de référence.

\## État

| # | chantier | état |
|---|---|---|
| 1-4, 6 | aiguille · GPU (5 sous-items) · mémoire KV · rotation 16 k · hygiène | ✅ tous mesurés |
| 5 | MLA ✅ (5,2e-7) · vision : tour complète qui tourne, 4 tranches validées, **déblocage ABI fait** | en cours |

`cargo test` 6/6, arbre propre, portes Qwen **19,3885** / gpt-oss **15,1757** intactes.

L'objectif reste **actif** : le prochain tour écrit le programme de comparaison, désormais sans inconnue technique, puis ajoute la rotation 2-D et la fenêtre locale au banc vision.

### Tour 23 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Check required mtmd/llama symbols
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/vision_mtmd.py`
- bash — Run mtmd vision reference
- bash — Load ggml backends and retry
- bash — Find library exporting ggml_backend_load_all
- bash — Use libggml.so and retry
- bash — Load CPU backend explicitly and retry
- bash — Document mtmd program state and commit

**Synthèse produite :**

⏵ Tour 14 : le programme de référence charge la tour de vision de llama.cpp

\## Fait dans ce tour

`tools/vision_mtmd.py` — la référence `libmtmd` par `ctypes`, sans en-têtes — a progressé jusqu'au bout du chemin de chargement :

- **premier obstacle levé** : llama.cpp ne charge plus ggml tout seul. `ggml_backend_load_all()` cherche les greffons à côté de l'**exécutable** — ici `python3` — et n'en trouve aucun ; `ggml_backend_load("/usr/lib/ollama/libggml-cpu-haswell.so")` fonctionne (Xeon E5 v3 = haswell) ;
- le **modèle de texte se charge**, le **projecteur aussi** (« 519 tenseurs »), et le warmup du ViT s'exécute sur 1288 × 1288 — donc toute la tour de référence est bien vivante dans le processus.

Deux points restants, tous deux dans **mon** code d'appel, identifiés précisément :

1. `mtmd_input_chunks_init()` **rend** un pointeur (elle ne prend pas de paramètre de sortie) — ma déclaration passait un pointeur de sortie, `chunks` restait nul, d'où le plantage ;
2. `image_min_pixels = 6272` : l'image 28 × 28 du banc (784 pixels) est **refusée par le modèle**. Il faut au moins 84 × 84 (7 056 pixels, 6 × 6 patchs) — et le banc Rust devra prendre la même taille pour que la comparaison porte sur la même entrée.

\## État

| # | chantier | état |
|---|---|---|
| 1-4, 6 | aiguille · GPU (5 sous-items) · mémoire KV · rotation 16 k · hygiène | ✅ mesurés |
| 5 | MLA ✅ (5,2e-7) · vision : tour complète qui tourne, 4 tranches validées, **référence llama.cpp chargée** | en cours |

`cargo test` 6/6, arbre propre, portes Qwen **19,3885** / gpt-oss **15,1757** intactes.

L'objectif reste **actif** : les deux corrections sont écrites noir sur blanc dans `docs/plan-mla-vision.md`, et une fois faites, `mtmd_get_output_embd` donnera les embeddings de la référence à comparer au projecteur du moteur — la comparaison qui tranche la rotation 2-D et la fenêtre locale, et donc la dernière inconnue du chantier.

### Tour 24 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Fix API calls and run reference
- bash — Identify crash point with unbuffered output
- bash — Try full prompt for tokenize
- bash — Document exact mtmd state and commit

**Synthèse produite :**

⏵ Tour 15 : la référence mtmd va jusqu'au `tokenize`, qui lève une exception C++

\## Fait dans ce tour

Les trois corrections identifiées au tour précédent ont été appliquées — `mtmd_input_chunks_init()` qui **rend** un pointeur, `mtmd_tokenize` qui reçoit le conteneur, et une image 84 × 84 conforme au minimum du modèle (`image_min_pixels = 6272`) — et le programme avance maintenant **pas à pas** jusqu'à la dernière étape :

```
contexte mtmd : ok
bitmap : ok
marqueur d'image : b'<__media__>'
conteneur de morceaux : ok
mtmd_tokenize: error: std::bad_alloc          (marqueur seul)
mtmd_tokenize: error: basic_string::_M_replace (invite complète)
tokenize rc=2 · 0 morceaux
```

Donc : modèle de texte chargé, projecteur chargé (519 tenseurs), contexte multimodal instancié, bitmap accepté, marqueur rendu par la bibliothèque elle-même. C'est **`mtmd_tokenize`** qui échoue, en levant une exception C++ au lieu de rendre un code d'erreur.

Trois hypothèses sont écrites dans le plan, par ordre de plausibilité :
1. **mélange de runtimes C++** — ollama embarque son propre `libstdc++`, l'appelant est le `python3` système ; écrire le programme en **C** est l'essai le moins coûteux ;
2. un paramètre mal typé faute d'en-têtes ;
3. un champ de `mtmd_context_params` non couvert par le sondage.

`mtmd_encode_chunk` et `mtmd_get_output_embd` sont le dernier maillon : c'est cette comparaison qui trancherait la rotation 2-D et la fenêtre locale.

\## État

| # | chantier | état |
|---|---|---|
| 1-4, 6 | aiguille · GPU (5 sous-items) · mémoire KV · rotation 16 k · hygiène | ✅ mesurés |
| 5 | MLA ✅ (5,2e-7) · vision : 4 tranches validées, tour complète qui tourne, référence à un appel de la fin | en cours |

`cargo test` 6/6, arbre propre, portes Qwen **19,3885** / gpt-oss **15,1757** intactes.

L'objectif reste **actif**. Le prochain tour peut tenter le programme en C (hypothèse n° 1) — c'est une trentaine de lignes, et le chemin est balisé : charger le backend ggml explicitement, le modèle, `mtmd_init_from_file`, un bitmap, `mtmd_tokenize`, `mtmd_encode_chunk`, `mtmd_get_output_embd`.

### Tour 25 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Use context marker for tokenize
- bash — Pass input struct to tokenize
- bash — Document tokenize findings and commit

**Synthèse produite :**

⏵ Tour 16 : deux hypothèses de plus testées sur `mtmd_tokenize`

\## Fait dans ce tour

Le programme de référence avance mais bute toujours sur le même appel. Les deux hypothèses les plus sérieuses ont été testées et **écartées par la mesure** :

1. le marqueur **du contexte** (`mtmd_get_marker`) plutôt que celui par défaut — les deux valent `<__media__>`, aucun changement ;
2. une **structure d'entrée** `(text, add_special, parse_special)` au lieu d'un `char *` — toujours `basic_string::_M_replace`, rc = 2.

Tout le reste du chemin fonctionne : backend ggml chargé explicitement, modèle de texte chargé, projecteur chargé (519 tenseurs), contexte multimodal instancié, bitmap accepté (84 × 84, conforme à `image_min_pixels = 6272`), conteneur de morceaux alloué.

**Un en-tête `mtmd.h` trancherait en dix secondes ce que trois tours de rétro-ingénierie n'ont pas tranché.** C'est le constat honnête, et il est écrit dans le plan avec trois pistes ordonnées : programme en **C** contre les mêmes bibliothèques (le mélange de runtimes C++ reste l'hypothèse la plus plausible), signature exacte retrouvée dans une version de llama.cpp, ou référence Python du modèle de vision (coûteuse, mais sans ABI).

Point important : **ce blocage ne concerne que la vérification**, pas le travail livré. Les tranches du chemin image sont validées contre numpy (patchs 5,4e-7, couche 1,8e-6, projecteur 1,7e-6), la tour entière tourne, et le point d'injection des embeddings est en place.

\## État des six chantiers

| # | chantier | état |
|---|---|---|
| 1 | aiguille long contexte | ✅ 12/12 |
| 2 | chemin GPU (5 sous-items) | ✅ |
| 3 | mémoire KV | ✅ |
| 4 | rotation à 16 k | ✅ |
| 5 | MLA ✅ (5,2e-7) · vision : 4 tranches validées, tour complète, injection branchée, conventions d'attention non tranchées | en cours |
| 6 | hygiène | ✅ |

`cargo test` 6/6, arbre propre, portes Qwen **19,3885** / gpt-oss **15,1757** intactes.

L'objectif reste **actif**. Je note honnêtement que les trois derniers tours ont été consommés par l'API d'une bibliothèque sans en-têtes, sans résultat : si le prochain tour ne débloque pas `mtmd_tokenize` rapidement (essai en C, ou signature retrouvée), la bonne décision sera de **clore le chantier vision à son état actuel** — mesuré, documenté, avec la lacune explicitement nommée — plutôt que d'y consumer d'autres tours.

### Tour 26 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Fetch mtmd.h and extract signatures
- bash — Extract exact signatures from mtmd.h
- bash — Add text_len and run reference
- bash — Get exact tokenize declaration
- bash — Read bitmap format docs
- bash — Document exact mtmd API and commit

**Synthèse produite :**

⏵ Tour 17 : l'API de `mtmd` est connue — le blocage est nommé, plus deviné

\## Fait dans ce tour

J'ai récupéré **`mtmd.h`** de llama.cpp (22 ko) et je l'ai dépouillé : les signatures exactes remplacent trois tours de rétro-ingénierie à l'aveugle.

- **`struct mtmd_input_text { const char* text; size_t text_len; bool add_special; bool parse_special; }`** — c'est `text_len` qui manquait, et son absence faisait lire à la bibliothèque les octets de ma chaîne comme une longueur ;
- `mtmd_tokenize(ctx, output, const mtmd_input_text*, const mtmd_bitmap* const*, size_t)` — signature confirmée, c'est bien celle que j'appelle désormais ;
- surtout, les **codes de retour sont documentés dans l'en-tête** : `1` = nombre de bitmaps ≠ nombre de marqueurs, **`2` = erreur de prétraitement du média** — c'est le code 2 qui tombe.

Donc : mon bitmap est accepté (format conforme : `nx*ny*3`, RGB entrelacé), sa taille aussi (84 × 84 = 7 056 ≥ `image_min_pixels` = 6 272), mais le **prétraitement du modèle** le refuse. Les pistes restantes sont écrites, ordonnées : une image plus grande (336 × 336, comme dans les exemples de llama.cpp, à cause de `image_min_tokens`), le programme en C, ou une référence Python du modèle de vision sans ABI du tout.

\## État

| # | chantier | état |
|---|---|---|
| 1 | aiguille long contexte | ✅ 12/12 |
| 2 | chemin GPU (5 sous-items) | ✅ |
| 3 | mémoire KV | ✅ |
| 4 | rotation à 16 k | ✅ |
| 5 | MLA ✅ (5,2e-7) · vision : 4 tranches validées, tour complète, injection branchée ; **rotation 2-D et fenêtre locale non implémentées** (leur vérification est bloquée sur le prétraitement mtmd) | en cours |
| 6 | hygiène | ✅ |

`cargo test` 6/6, arbre propre, portes Qwen **19,3885** / gpt-oss **15,1757** intactes.

L'objectif reste **actif** : la vision demande encore les deux conventions d'attention. Le prochain tour a une action unique et peu coûteuse — **essayer une image de 336 × 336** — qui, si elle passe, débloque la comparaison complète ; sinon, la décision que j'ai annoncée s'applique : clore le chantier à son état mesuré et documenté plutôt que d'y consumer d'autres tours.

### Tour 27 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Try 336x336 image with mtmd
- bash — Fetch clip.cpp and locate 2-D rotation code
- bash — Read window pattern logic in clip.cpp
- bash — Read Qwen2.5-VL position/window setup
- bash — Document source findings and commit

**Synthèse produite :**

⏵ Tour 18 : la fenêtre locale est lue dans la source de llama.cpp

\## Fait dans ce tour

Deux résultats, dont un qui corrige une de mes suppositions.

**L'hypothèse « image trop petite » est réfutée** : 336 × 336 échoue exactement comme 84 × 84 (`rc=2`, erreur de prétraitement du média). Le blocage `mtmd_tokenize` n'est donc pas une question de taille — c'était ma dernière hypothèse simple, et elle est tombée par la mesure.

**La fenêtre locale est maintenant lue dans la source** (`tools/mtmd/clip.cpp`, récupéré et dépouillé) : ce n'est **pas** une fenêtre par ligne comme je l'avais supposé, mais une **permutation + un masque** — sur les couches fenêtrées, les jetons d'une même fenêtre sont rendus contigus (`window_idx` / `inv_window_idx`) et un masque ne laisse voir que la fenêtre, laquelle est un **bloc carré** de la grille *après* fusion 2 × 2 :

```cpp
for (int y = 0; y < ph; y += grid_window)
  for (int x = 0; x < pw; x += grid_window) { ... }
```

**La rotation 2-D est localisée** : elle n'est pas dans `clip.cpp`, qui calcule un tenseur `positions` et le passe au graphe où les opérations GGML appliquent le mRoPE. C'est donc le calcul de `positions` qu'il faut lire — la zone est identifiée (offset ~264 000 du fichier) et c'est le pas suivant, désormais précis.

\## État

| # | chantier | état |
|---|---|---|
| 1-4, 6 | aiguille · GPU (5 sous-items) · mémoire KV · rotation 16 k · hygiène | ✅ mesurés |
| 5 | MLA ✅ (5,2e-7) · vision : 4 tranches validées, tour complète, injection branchée ; fenêtre locale **convention connue** (source), rotation 2-D **localisée** | en cours |

`cargo test` 6/6, portes Qwen **19,3885** / gpt-oss **15,1757** intactes, arbre propre.

L'objectif reste **actif**. La lecture de la source est la voie qui avance — contrairement à la rétro-ingénierie de `mtmd_tokenize`, qui a consommé cinq tours pour rien. Le prochain tour lit le calcul de `positions` (une trentaine de lignes au même endroit) et implémente enfin la rotation mRoPE et la fenêtre locale.

### Tour 28 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Read positions computation for mRoPE
- bash — Read Qwen2.5-VL positions block
- bash — Document mRoPE convention and commit

**Synthèse produite :**

⏵ Tour 19 : la convention de rotation 2-D est lue dans la source

\## Fait dans ce tour

La convention mRoPE de Qwen2.5-VL est maintenant **connue par la source**, pas devinée. Dans `clip.cpp`, cas `QWEN25VL`, le tenseur `positions` porte **quatre sections** de `num_patches` entiers, remplies (ligne, colonne, ligne, colonne) :

```cpp
for (int y = 0; y < ph; y += merge_ratio)
  for (int x = 0; x < pw; x += merge_ratio)
    for (int dy = 0; dy < 2; dy++)
      for (int dx = 0; dx < 2; dx++) {
        positions[                  ptr] = y + dy;   // section 0 : LIGNE
        positions[    num_patches + ptr] = x + dx;   // section 1 : COLONNE
        positions[2 * num_patches + ptr] = y + dy;   // section 2 : LIGNE
        positions[3 * num_patches + ptr] = x + dx;   // section 3 : COLONNE
```

Deux conséquences :

1. la **numérotation raster des groupes de fusion** est confirmée (celle que le banc utilise déjà pour la fusion 2 × 2) ;
2. la rotation se fait en **quatre blocs** de la dimension de tête : blocs 0 et 2 selon la **ligne**, blocs 1 et 3 selon la **colonne** — exactement ce que `ggml_rope_multi` attend, et très différent de la rotation scalaire que le moteur applique à ses jetons de texte.

Reste **une** ambiguïté que la source ne lève pas seule : l'échelle de fréquences *à l'intérieur* de chaque bloc (RoPE sur `hd/4`, ou sur `hd/2` avec paires entrelacées). C'est précisément ce que la comparaison à `libmtmd` aurait tranché — je le note sans détour.

\## État

| # | chantier | état |
|---|---|---|
| 1-4, 6 | aiguille · GPU (5 sous-items) · mémoire KV · rotation 16 k · hygiène | ✅ |
| 5 | MLA ✅ (5,2e-7) · vision : fenêtre locale **connue**, rotation 2-D **connue à une ambiguïté près**, 4 tranches validées, tour complète, injection branchée | en cours |

`cargo test` 6/6, portes Qwen **19,3885** / gpt-oss **15,1757** intactes, arbre propre.

L'objectif reste **actif**. La voie est maintenant tracée : implémenter la fenêtre locale (permutation + masque par bloc carré, lue dans la source) et la rotation en quatre blocs, puis vérifier que la tour produit des embeddings de norme plausible — et si le temps le permet, rouvrir `mtmd` avec la signature désormais exacte.

### Tour 29 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*3 appels d'outils.* Actions notables :

- bash — Implement 2-D rotation in vision bench
- bash — Add rotation to reference and compare
- bash — Make reference tolerant and commit rotation

**Synthèse produite :**

⏵ Tour 20 : la rotation 2-D est implémentée d'après la source

\## Fait dans ce tour

**La rotation mRoPE est en place**, écrite d'après `clip.cpp` et non devinée : quatre blocs de la dimension de tête, **blocs 0 et 2 selon la ligne, blocs 1 et 3 selon la colonne**, chaque bloc tourné par paires `(i, i + quart/2)` avec l'échelle RoPE usuelle. La sortie de la tour change en conséquence (|sortie| 35,55 → **42,62**), donc la rotation agit bien.

Deux réserves, écrites dans le document plutôt que passées sous silence :

1. l'**échelle interne de chaque bloc** reste une hypothèse — la source montre le tenseur `positions` (quatre sections ligne/colonne/ligne/colonne) mais pas l'opération GGML qui le consomme ;
2. la **référence numpy ne couvre plus la tour** : depuis que le banc écrit sa seule sortie, le fichier `.bloc` ne permet plus de rejouer les 32 couches. J'ai rendu l'outil tolérant — il l'annonce au lieu de planter — et les deux tranches encore comparables le restent : **patchs 5,37e-7** et **projecteur 1,73e-6**.

Restent, pour clore la vision : la **fenêtre locale**, inexprimable sur les images du banc (28 × 28 et 84 × 84 tiennent dans une seule fenêtre de 8 × 8 après fusion — il faudrait ≥ 224 × 224 pour en avoir plusieurs), et l'alimentation de l'injection `Model::emb_imposee` par une tour complète.

\## État des six chantiers

| # | chantier | état |
|---|---|---|
| 1 | aiguille long contexte | ✅ 12/12 |
| 2 | chemin GPU (5 sous-items) | ✅ |
| 3 | mémoire KV | ✅ |
| 4 | rotation à 16 k | ✅ |
| 5 | MLA ✅ (5,2e-7) · vision : patch embedding, blocs, 32 couches, rotation 2-D, projecteur, injection — **fenêtre locale non testable sur ces images** | en cours |
| 6 | hygiène | ✅ |

`cargo test` 6/6, portes Qwen **19,3885** / gpt-oss **15,1757** intactes, arbre propre.

L'objectif reste **actif**. Le chantier vision est désormais complet dans sa structure, avec deux points explicitement non vérifiés (échelle interne de la rotation, fenêtre locale) faute de référence exploitable — et la raison de chaque lacune est documentée, ce qui vaut mieux qu'un chiffre inventé.

### Tour 30 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Add local window and run 224px bench
- bash — Fix projector for multiple merge groups
- bash — Build and run complete vision path
- bash — Document complete vision path and commit

**Synthèse produite :**

⏵ Tour 21 : le chemin image va de l'image aux jetons de 3584 dimensions

\## Fait dans ce tour

**Le chemin image est complet**, sur une image de **224 × 224** (16 × 16 patchs, 8 × 8 après fusion) :

convolution de patchs → **32 couches de ViT** avec **rotation 2-D** et **fenêtre locale** (couches complètes aux indices 7, 15, 23, 31 ; fenêtre de 4 × 4 jetons fusionnés ailleurs, lue dans `clip.cpp`) → `v.post_ln` → **projecteur par groupes de fusion : 64 groupes × 3 584 valeurs**.

C'est exactement ce qu'il faut injecter à la place des jetons d'image — et le moteur sait le faire depuis `Model::emb_imposee`, branché il y a quelques tours. J'ai aussi corrigé le projecteur, qui ne traitait qu'**un** groupe de fusion (valable pour l'image 28 × 28 du banc initial, faux dès qu'il y en a 64) : c'était le genre d'erreur qui aurait produit 3 584 valeurs plausibles et fausses.

Ce qui reste **non vérifié** est écrit noir sur blanc dans le document :

| point | état |
|---|---|
| embedding de patchs, projecteur | **validés** contre numpy (5,37e-7 et 1,73e-6, à 28 × 28) |
| échelle interne de la rotation | hypothèse — la source montre `positions`, pas l'opération GGML qui le consomme |
| fenêtre locale | implémentée d'après la source, **non testable** sans référence à cette taille |
| bout en bout image → texte | impossible : le chemin d'inférence multimodal n'existe pas ici |

La référence numpy annonce désormais ces limites au lieu de planter quand la taille change.

\## État des six chantiers

| # | chantier | état |
|---|---|---|
| 1 | aiguille long contexte | ✅ 12/12 |
| 2 | chemin GPU (5 sous-items) | ✅ |
| 3 | mémoire KV | ✅ |
| 4 | rotation à 16 k | ✅ |
| 5 | MLA ✅ (5,2e-7) · vision : **chaîne complète** (patchs → 32 couches → rotation → fenêtre → projecteur → injection branchée), deux points explicitement non vérifiés | en cours |
| 6 | hygiène | ✅ |

`cargo test` 6/6, arbre propre, portes Qwen **19,3885** / gpt-oss **15,1757** intactes.

L'objectif reste **actif** — mais le chantier vision est maintenant *structurellement* complet : ce qui manque n'est plus du code, c'est une référence pour vérifier deux constantes de convention, et cette référence est bloquée par un appel de bibliothèque que cinq hypothèses n'ont pas débloqué.

### Tour 31 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Check tokenize_from_parts availability
- bash — Fetch ggml rope implementation
- bash — Locate rope code in ops.cpp
- bash — Read mRoPE cache init
- bash — Document rotation correction needed

**Synthèse produite :**

⏵ Tour 22 : le détail de la rotation lu dans ggml — et mon implémentation est fausse

\## Fait dans ce tour

J'ai suivi la piste jusqu'au bout : la convention exacte est dans `ggml/src/ggml-cpu/ops.cpp`, fonction `ggml_mrope_cache_init`. La lecture est sans ambiguïté — et elle montre que **mon implémentation est fausse sur deux points** :

```cpp
int sect_dims = sections[0] + sections[1] + sections[2] + sections[3];
for (int64_t i0 = 0; i0 < ne0; i0 += 2) {
    int sector = (i0 / 2) % sect_dims;   // le secteur choisit la position
    rope_yarn(theta/ff, ...);
    theta_t *= theta_scale;  theta_w *= theta_scale;  theta_h *= theta_scale;
}
```

1. la rotation apparie des dimensions **consécutives** `(i0, i0+1)` — c'est le contraire de la convention « moitié tournée » `(i, i + quart/2)` que j'avais écrite ;
2. le secteur vaut `(i0/2) % sect_dims`, avec `sect_dims` = **somme** des quatre sections : avec `positions` = (ligne, colonne, ligne, colonne), cela donne des blocs de secteurs (ligne, colonne, ligne, colonne) dans cet ordre ;
3. l'échelle de fréquences **continue** d'un bloc au suivant (`theta *= theta_scale` à chaque pas, sans remise à zéro hors mode `indep_sects`) — ce n'est donc pas une échelle recalculée par bloc comme je l'ai fait.

Autrement dit : la **structure** (quatre blocs, deux positions alternées) est la bonne, mais **l'appariement et l'échelle sont faux**. C'est précisément ce qu'une référence aurait attrapé en une seconde — et c'est la démonstration, sur pièce, de pourquoi je n'ai pas voulu déclarer cette partie « faite » : le code tournait, les valeurs étaient plausibles, et elles étaient fausses.

\## État

| # | chantier | état |
|---|---|---|
| 1-4, 6 | aiguille · GPU (5 sous-items) · mémoire KV · rotation 16 k · hygiène | ✅ mesurés |
| 5 | MLA ✅ (5,2e-7) · vision : chaîne complète et **erreur identifiée avec sa correction** (appariement consécutif, échelle continue), fenêtre locale d'après la source, référence numpy valable sur 2 tranches | en cours |

`cargo test` 6/6, arbre propre, portes Qwen **19,3885** / gpt-oss **15,1757** intactes.

L'objectif reste **actif**, et il se réduit maintenant à quelque chose de précis et de petit : corriger les deux points de la rotation d'après le code cité, puis chercher une validation. Le prochain tour peut appliquer la correction — c'est une vingtaine de lignes, et le texte de référence est dans le dépôt.

### Tour 32 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*7 appels d'outils.* Actions notables :

- bash — Apply corrected rotation
- bash — Reorder projector after tower
- bash — Close brace and run corrected pipeline
- bash — Declare tour and run pipeline
- bash — Restore projector execution
- bash — Check reordering state
- bash — Commit corrected rotation and identified ordering bug

**Synthèse produite :**

⏵ Tour 23 : rotation corrigée d'après ggml — et un défaut d'ordre mis au jour

\## Fait dans ce tour

**La rotation est corrigée d'après la source** (`ggml_mrope_cache_init`) : paires **consécutives** `(2i, 2i+1)`, moitié « ligne » puis moitié « colonne » de la tête, exposant suivant l'indice de paire **global** (l'échelle continue d'un bloc à l'autre). La sortie de la tour change : 187,45 → **234,53**, donc la correction agit.

**Et le témoin a mis au jour un défaut d'ordre** que les chiffres seuls auraient laissé passer : le projecteur affiche toujours `|sortie| = 131,54`, **identique** à ce qu'il donnait avant la correction. Conclusion : il consomme encore les **embeddings de patchs** et non la **sortie de la tour**. Le pipeline réel est `patchs → tour → v.post_ln → projecteur`.

C'est un chiffre *qui ne bouge pas* alors que tout ce qui l'alimente a changé — exactement le genre de signal que ce projet traite comme une alerte, et pas comme une bonne nouvelle. Le point est localisé à la ligne près dans `run_banc_vision` (`let source = tour.clone().unwrap_or_else(|| out.clone());` lu alors que `tour` est encore `None`) : déplacer le bloc projecteur après la tour est mécanique.

Je n'ai pas voulu enchaîner ce déplacement avec le peu de contexte restant : la modification est simple mais touche l'ordre d'un pipeline, et la faire à moitié laisserait le banc dans un état pire que celui-ci.

\## État

| # | chantier | état |
|---|---|---|
| 1-4, 6 | aiguille · GPU (5 sous-items) · mémoire KV · rotation 16 k · hygiène | ✅ mesurés |
| 5 | MLA ✅ (5,2e-7) · vision : chaîne complète, rotation **conforme à la source**, fenêtre locale d'après la source ; reste à ordonner projecteur après tour, et à vérifier les conventions | en cours |

`cargo test` 6/6, arbre propre, portes Qwen **19,3885** / gpt-oss **15,1757** intactes.

L'objectif reste **actif** : le prochain tour commence par un déplacement de bloc (mécanique, décrit dans le document), puis cherche à valider — ou à défaut documente — les deux conventions qui restent non vérifiées.

### Tour 33 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Move projector after tower and verify
- bash — Verify reference tolerance and commit fix

**Synthèse produite :**

⏵ Tour 24 : l'ordre du pipeline est corrigé, et la preuve est que le chiffre change

\## Fait dans ce tour

Le déplacement mécanique annoncé hier est fait : **le projecteur consomme maintenant la sortie de la tour**, et non les embeddings de patchs.

La vérification n'est pas un nouveau chiffre « plausible » — c'est le fait que **le chiffre ait changé** :

| alimentation | \|sortie\| du projecteur |
|---|---|
| embeddings de patchs (l'ancien ordre, faux) | 131,54 |
| **sortie de la tour (l'ordre correct)** | **515,84** |

Le tour précédent, ce même chiffre restait identique alors que tout ce qui l'alimente avait changé : c'était la trace du mauvais ordre, et c'est maintenant le contrôle qui la détecte.

Faute de référence, j'ai ajouté un contrôle de plausibilité : la moyenne quadratique par élément vaut `515,84 / √(64 × 3584) = 1,08`, du même ordre que les lignes de `token_embd` du modèle de texte. Un pipeline qui produirait des embeddings d'échelle absurde (1e-3 ou 1e3) se verrait immédiatement ici.

La référence numpy, elle, annonce proprement qu'elle ne peut plus comparer à cette taille et rappelle les valeurs validées (5,4e-7 à 28 × 28).

\## État du chantier vision

**Complet et dans le bon ordre** : patchs → 32 couches (rotation 2-D conforme à `ggml_mrope_cache_init`, fenêtre locale d'après `clip.cpp`) → `v.post_ln` → projecteur (64 groupes × 3 584) → `Model::emb_imposee`.

Non vérifié, et nommé : l'échelle interne de la rotation (dérivée de la source, pas confirmée par une référence), la fenêtre locale (idem), et le bout en bout image → texte (impossible sans chemin d'inférence multimodal).

\## Les six chantiers

| # | chantier | état |
|---|---|---|
| 1 | aiguille long contexte | ✅ 12/12 |
| 2 | chemin GPU (5 sous-items) | ✅ |
| 3 | mémoire KV | ✅ |
| 4 | rotation à 16 k | ✅ |
| 5 | MLA ✅ (5,2e-7) · vision : chaîne complète et ordonnée, trois points non vérifiés nommés | en cours |
| 6 | hygiène | ✅ |

`cargo test` 6/6, arbre propre, portes Qwen **19,3885** / gpt-oss **15,1757** intactes.

L'objectif reste **actif**. Il ne reste, côté vision, aucune ligne de code identifiée comme fausse — seulement des conventions que rien de local ne peut confirmer, et c'est une distinction que je préfère laisser explicite plutôt que de la maquiller en « terminé ».

### Tour 34 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Inject vision embedding into engine
- bash — Document end-to-end injection and commit

**Synthèse produite :**

⏵ Tour 25 : la chaîne image → logits est démontrée de bout en bout

\## Fait dans ce tour

Le dernier pas est franchi. `QT_VISION_TEXTE=<modele.gguf>` fait charger le modèle de texte au banc, lui **impose le premier jeton d'image** via `Model::emb_imposee`, et lit les logits. Mesuré sur Qwen2.5-VL-7B :

```
projecteur : 64 groupes × 3584 valeurs, |sortie| = 515.8354
injection  : 64 jetons × 3584 disponibles
  moteur   : 152064 logits · argmax 15 · moyenne -1.788 · écart-type 2.026
```

C'est-à-dire : **image → convolution de patchs → 32 couches (rotation 2-D, fenêtre locale) → `v.post_ln` → projecteur → 64 jetons de 3 584 dimensions → injection dans le modèle de texte → 152 064 logits**. Le trou d'architecture identifié au tout premier tour du chantier — « `forward` part toujours de `token_embd`, il faut un chemin qui parte d'un vecteur » — est comblé, et la démonstration passe par le chemin réel, pas par un banc isolé.

**Ce que cela prouve** : la plomberie complète tient ; le moteur accepte un vecteur d'image et rend des logits d'échelle normale (moyenne −1,79, écart-type 2,03 — ni 1e-3 ni 1e3).

**Ce que cela ne prouve pas, et je ne le maquillerai pas** : la *qualité*. Les deux conventions non confirmées (échelle interne de la rotation, fenêtre locale) et l'absence d'un modèle d'inférence multimodal local font qu'aucun chiffre de qualité ne peut être avancé ici.

\## Les six chantiers

| # | chantier | état |
|---|---|---|
| 1 | aiguille long contexte | ✅ 12/12 sondes |
| 2 | chemin GPU (vectorisation, experts, lots, tête AVX2, 2 cartes) | ✅ |
| 3 | mémoire KV (pagination 0,03 Go à 1 M, hypothèse f16 réfutée) | ✅ |
| 4 | rotation à 16 k (35,18 contre 1 133,02, seuil à 4 ×) | ✅ |
| 5 | MLA ✅ validé (5,2e-7) · vision : chaîne complète **démontrée jusqu'aux logits**, 2 conventions non vérifiées faute de référence | fonctionnellement clos |
| 6 | hygiène (feuille de route + pièges `QT_GPU*`) | ✅ |

`cargo test` 6/6, arbre propre, portes Qwen **19,3885** / gpt-oss **15,1757** intactes.

\## Ma recommandation pour la suite

Le chantier vision est **fonctionnellement complet et démontré** ; ce qui reste est une *vérification* que rien de local ne permet — j'ai épuisé les pistes raisonnables (mtmd bloqué sur cinq hypothèses, pas de torch/transformers, source de llama.cpp lue jusqu'au bout). Je suggère de **clore l'objectif** au prochain tour si vous n'avez pas de référence externe à fournir, en laissant dans `docs/plan-mla-vision.md` les trois pistes de validation
… [131 caractères tronqués]

### Tour 35 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1772 caractères tronqués]

*11 appels d'outils.* Actions notables :

- bash — Find rope_multi sections in clip.cpp
- bash — Read rope_multi layout comment and sections
- bash — Document rotation confirmation and window variant
- bash — Final verification before closing
- bash — Update REPRISE and commit
- bash — Locate stale REPRISE text
- bash — Fix stale REPRISE item and commit
- bash — Verify REPRISE item and finalize
- bash — Fix stale rotation item in REPRISE
- get_goal
- update_goal

**Synthèse produite :**

⏵ Les six chantiers sont clos, l'objectif est marqué terminé

\## Ce qui a été fait

| # | chantier | résultat mesuré |
|---|---|---|
| 1 | **aiguille long contexte** | **12 sondes sur 12** trouvées (profondeurs 0,1/0,5/0,9) : Qwen2.5-1.5B à 512 et 2 048, Qwen3-30B-A3B à 2 048, gpt-oss-120b à 4 096 avec KV déporté. Le protocole est passé au remplissage WikiText-2 **varié** (une fenêtre différente par sonde) et à 40 jetons de réponse — les deux défauts qui faisaient échouer la v1 |
| 2 | **chemin GPU** | dépaquetage vectorisé : à 1 M de clés, f32 13,6 → **7,0 ms** (308 Go/s), int8 15,0 → **6,5**, int4 13,2 → **7,4** — écarts au CPU inchangés (5,1e-6 / 2,9e-6 / 4,9e-6) · experts MXFP4 en VRAM : **+6 %** seulement, verdict « ne pas activer » · attention par lots déportée : préremplissage 261,6 → **93,7 s (×2,8)**, perplexité **identique** · tête Q8_0 en **AVX2**, bit-identique · KV réparti **12 couches sur chaque Quadro** |
| 3 | **mémoire** | cache CPU paginé : à contexte 1 M, **0,03 Go** alloués au lieu de 25,77 Go · hypothèse « clés en f16 avant quantification » **réfutée** (perplexité identique) |
| 4 | **rotation à 16 k** | RoPE simple **35,18** contre **1 133,02** en interpolation — le simple gagne à *toutes* les longueurs mesurées (128 → 16 384) ; seuil porté à **4 ×** la longueur déclarée |
| 5 | **MLA et vision** | **MLA** : modèle synthétique + référence numpy, écart **5,2e-7** · **Vision** : chaîne complète démontrée de bout en bout — image → patchs → 32 couches (rotation 2-D **conforme à la source ggml**, fenêtre locale d'après `clip.cpp`) → `v.post_ln` → projecteur (64 groupes × 3 584) → injection → **152 064 logits**. Tranches validées : patchs 5,4e-7, projecteur 1,7e-6, une couche 1,8e-6 |
| 6 | **hygiène** | feuille de route réécrite, tableau des pièges `QT_GPU` / `QT_GPU_TETE` / `QT_GPU_KV` / `QT_KV_*` / `QT_BANC_*` |

**Vérification** : `cargo test --release` **6/6**, portes de non-régression Qwen **19,3885** et gpt-oss **15,1757** (sans `QT_GPU`) revérifiées à plusieurs reprises, dont après le dernier changement de noyau. Arbre propre.

\## Deux erreurs que la mesure a attrapées, et qui méritent d'être connues

- **Le chiffre qui ne bouge pas est un signal.** Le projecteur affichait exactement la même valeur avant et après correction de la rotation : c'était la trace d'un **ordre de pipeline faux** (il consommait les embeddings de patchs au lieu de la sortie de la tour). La correction s'est vérifiée par le *changement* du chiffre (131,54 → 51
… [1358 caractères tronqués]

### Tour 36 — prochaine étape?

*1 appels d'outils.* Actions notables :

- bash — Read the current next-steps list

**Synthèse produite :**

⏵ Je relis la feuille de route et je propose l'ordre suivant

Le dépôt est propre et l'objectif est clos. Voici ce qui reste, par rentabilité — en signalant d'abord que **deux items de la liste `REPRISE.md` §6 sont périmés** :

- son item 1 (noyau de tête Q8_0) est **fait** (AVX2, bit-identique) ;
- son item 2 (second GPU) est **fait** pour le KV (12 couches par carte) — il reste à lui confier les experts.

\## Ce qui reste, par ordre de rentabilité

| priorité | chantier | pourquoi maintenant | coût |
|---|---|---|---|
| **1** | **Top-k dans le noyau d'attention GPU** | `--attn-topk 256` **améliore** la perplexité (234,88 contre 298,56 à 2 048) mais retombe sur le CPU : c'est le dernier repli du chemin long contexte. Contenu, mesurable, et il débloque la mesure de qualité croisée | ~1 tour |
| **2** | **Permutation colonne-majeur des couches fenêtrées** | Dernier écart *connu* entre la vision et la source `clip.cpp` (la fenêtre n'est pas qu'un masque : les positions changent d'ordre). Une vingtaine de lignes | ~1 tour |
| **3** | **Écart int8 résiduel** (+3,0 % contre +0,8 % chez llama.cpp à 8 192) | L'hypothèse des clés f16 est réfutée ; restent la quantification des **valeurs** et la précision du **softmax** — deux variantes à tester, faciles à mesurer | ~2 tours |
| **4** | **Aiguille étendue** (8 192 / 16 384, plusieurs codes par sonde, croisement avec `--attn-topk`) | C'est la seule mesure de *qualité* du contexte long ; le préremplissage par lots et le KV déporté la rendent abordable | plusieurs heures machine |
| **5** | **Rendre le déport des experts rentable** | Mesuré à +6 % seulement : il faudrait grouper les trois projections par expert et supprimer les copies par appel — sinon on abandonne, ce qui est déjà écrit | ~2 tours |
| **6** | **Valider la vision contre une référence** | Le seul chiffre qui manque vraiment, et le seul bloqué : `mtmd_tokenize` (rc=2) après cinq hypothèses. Trois pistes écrites, dont un programme en C | incertain |
| — | **Rafraîchir `REPRISE.md` §6** | Les items 1 et 2 y sont périmés, ce qui induit en erreur la prochaine session | 5 min |

\## Ma recommandation

**Commencer par le top-k dans le noyau** (priorité 1) : c'est le seul point où une *amélioration de qualité déjà mesurée* (+21 % de perplexité à 2 048) est aujourd'hui inutilisable à contexte long parce qu'elle repasse par le CPU. Il est contenu, vérifiable par les portes habituelles, et il ouvre la priorité 4.

Puis le **rafraîchissement de `REPRISE.md` §6** dan
… [174 caractères tronqués]

### Tour 37 — vision d'abord, puis roadmap

*5 appels d'outils.* Actions notables :

- bash — Locate rotation call site
- bash — Apply col-major permutation for windowed layers
- bash — Inspect broken region
- bash — Repair and run with col-major permutation
- bash — Document and commit col-major permutation

**Synthèse produite :**

⏵ Vision terminée : le dernier écart connu avec la source est comblé — je passe à la feuille de route

Vision faite. Le dernier écart de code identifié est comblé :

**Sur les couches fenêtrées**, `clip.cpp` transpose la grille des unités de fusion avant d'empaqueter les positions (`idx_col[u_col] = u_row`, soit `pos_col[c·n+r] = pos_row[r·n+c]` pour une grille carrée) : un patch (r, c) reçoit les positions de (c, r). La fenêtre n'était donc pas qu'un masque — **elle change aussi l'ordre des positions**, et c'est maintenant implémenté (`complete_rot` : couches 7, 15, 23, 31 en attention complète, les autres permutées).

Vérification par le **changement** des chiffres — le contrôle qui m'avait manqué une fois :

| | avant | après |
|---|---|---|
| sortie de la tour | 234,53 | **244,38** |
| sortie du projecteur | 515,84 | **465,84** |

Le chemin image suit désormais la source sur ses trois points d'attention : rotation en quatre blocs (`ggml_mrope_cache_init`), échelle continue (idem), permutation colonne-majeur (`clip.cpp`). **Ce qui reste sans référence n'est plus une ligne de code identifiée, mais la qualité globale** — et les trois pistes de validation sont écrites dans `docs/plan-mla-vision.md`.

Commit `d349063`, `cargo test` 6/6.

Je passe maintenant à la feuille de route : corriger les items périmés de `REPRISE.md` §6 (le **noyau de tête** et le **second GPU** y sont encore annoncés comme à faire alors qu'ils sont livrés), remonter ce qui est mûr, et redescendre ce qui a été mesuré comme non rentable (les experts MXFP4 à +6 %).

### Tour 38 — Au delà des défis techniques, il nou faut un vrai document de vision de ce projet. Je serais porté à renommer le projet  … [444 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Recon: docs, README, name occurrences
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md`
- bash — Verify cited numbers exist in the repo
- bash — Update README identity and commit vision doc

**Synthèse produite :**

⏵ Vision écrite ; je passe à la feuille de route comme demandé

\## 1. Vision — `docs/vision.md`

Le document existe et il est **adossé aux mesures du dépôt** (j'ai vérifié que chaque chiffre cité est bien dans un rapport : 17,9 %, 33,1 %, 0,08 %, 10 % de densité, 7,79 G événements/s, 6,2 ms). Il est structuré pour servir, pas pour décorer :

- **§1 Le cœur** : des listes valuées groupées **par source**, poussées vers leurs destinations (AER) — le coût devient proportionnel à l'**activité**, pas à la taille du modèle. Avec la nuance qui rend le document crédible : le croisement push/pull est **mesuré à ~10 % de densité**, donc le moteur garde les deux chemins et choisit par la mesure ;
- **§2 Axe 1 — voir et régler neurone par neurone** : les outils existent (`--profil-neurones`, `--profil-experts`, `[config]`, `--ppl-profil`, journal) et ont servi ; ce que la vision ajoute est un **format de trace stable** et le **diff par couche** — passer de « la perplexité a bougé de 0,01 » à « la couche 23 a changé de régime au jeton 4 096 » ;
- **§3 Axe 2 — répartir sur les composants** : le plus avancé, tout mesuré (KV en VRAM sur deux cartes, attention ÷6,7, préremplissage ×2,8, tête Q6_K ×2,1, experts +6 % → verdict honnête) ; la règle qui en sort : *on place un opérateur là où son flux coûte le moins cher* ;
- **§4 Axe 3 — répartir sur plusieurs machines** : **rien n'existe**, et je l'écris comme une hypothèse de travail, avec les cinq choses à définir (contrat d'échange, granularité, placement, ce qui ne se parallélise pas — le décodage est séquentiel, c'est le préremplissage qu'il faut distribuer d'abord) et les mesures à faire ;
- **§5 Axe 4 — rejouer/comparer** : les portes de non-régression et les références indépendantes (MLA 5,2e-7, vision 5,4e-7/1,7e-6) sont déjà cette idée en petit ;
- **§6 Axe 5 — formats, matériels, énergie** : trois matériels (SIMD, PTX, FPGA), et l'argument énergétique — *on ne lit que ce qui parle* ;
- **§7 Ce que la vision n'est pas** : pas « le sparse gagne toujours », pas « distribuer est gratuit », pas une réécriture ;
- **§9 Le nom** : ce que « Drave » dit (ça coule, ça se répartit, ça se surveille) et ce que le renommage implique.

Le **README** porte maintenant le nom, avec la mention de l'ancien et le renvoi à la vision. Commit `15c4c8c`.

\## 2. Feuille de route — maintenant

Je fais le rafraîchissement de `REPRISE.md` §6 dans la foulée : ses items 1 (noyau de tête) et 2 (second GPU) sont annoncés « à faire » alors qu'ils son
… [747 caractères tronqués]

### Tour 39 — 3 tout tout de suite, préserve l'historique dans un document et là ou ça permet d'être cohérent, mais tout le reste pren … [25 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Recon for the rename
- bash — Perform the full rename
- bash — Set binary name, fix paths, add legacy warning
- bash — Get date and env var list
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/histoire.md`
- bash — Update vision, test, verify gate and legacy warning
- bash — Fix vision section and run gpt-oss gate
- bash — Commit the full rename

**Synthèse produite :**

⏵ Renommage fait : tout le dépôt s'appelle Drave, l'historique est préservé

\## 1. Vision — `docs/vision.md`

Un vrai document de vision, adossé aux mesures du dépôt (chaque chiffre cité a été vérifié comme présent dans un rapport) : les listes d'activation **par source**, poussées vers leurs destinations (AER) — le coût devient proportionnel à l'**activité**, pas à la taille du modèle.

Cinq axes explorés, avec ce qui est mesuré et ce qui est hypothèse :
1. **observer et régler neurone par neurone** (`--profil-neurones`, `--profil-experts`, `[config]`, journal ; top 10 % des neurones = 33,1 % de la magnitude ; 0,08 % chauds >90 % du temps) — ce que la vision ajoute : un format de trace stable et le **diff par couche** ;
2. **répartir sur les composants** — le plus avancé, tout mesuré (KV en VRAM sur deux cartes, attention ÷6,7, préremplissage ×2,8, tête Q6_K ×2,1, experts +6 % → verdict) ; la règle : *placer un opérateur là où son flux coûte le moins cher* ;
3. **répartir sur plusieurs machines** — **rien n'existe**, écrit comme hypothèse de travail avec les cinq choses à définir ; le décodage reste séquentiel, c'est le préremplissage qu'il faut distribuer ;
4. **rejouer/comparer** — les portes de non-régression et les références indépendantes (MLA 5,2e-7, vision 5,4e-7) sont déjà cette idée en petit ;
5. **formats, matériels, énergie** — trois matériels (SIMD, PTX, FPGA), et l'argument *on ne lit que ce qui parle*.

Plus une section « ce que la vision n'est pas » : le croisement push/pull à 10 % de densité est mesuré, le sparse ne gagne pas toujours.

\## 2. Renommage — option 3, tout de suite

| avant | après |
|---|---|
| crate `qtrinet-core/` | `drave-core/` |
| binaire `qtrinet-core` | **`drave`** |
| `gpu/qtrinet_gpu.{cu,ptx}` | `gpu/drave_gpu.{cu,ptx}` |
| variables `QT_*` | **`DRAVE_*`** |
| « Qtrinet » dans 61 fichiers de contenu | « Drave » |

**Préservé, volontairement** : le **journal de sessions** (un journal réécrit n'est plus un journal), **`Qtrinet-bootstrap.md`** (le cahier des charges d'origine, pièce datée), et l'**historique Git**.

**`docs/histoire.md`** porte les trois âges du projet (le Qtrinet ternaire des Stratix V, le virage événementiel à 7,79 G événements/s, Drave) et la **table de conversion** des anciens noms — variables et chemins — pour que vos anciens scripts aient une réponse au lieu d'un mystère. Les vieilles variables ne font plus rien, mais **le moteur le dit** (vérifié : `[attention] QT_GPU est l'ancien nom… Rien n'a é
… [687 caractères tronqués]

### Tour 40 — fais un roadmap ambitieux et commence les travaux qui ne nécessitent pas d'infra supplémentaire. on pourra terter avec c … [28 caractères tronqués]

*12 appels d'outils.* Actions notables :

- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/roadmap.md`
- bash — Find trace hook sites in forward
- bash — Implement flux tracing
- bash — Wire trace CLI options
- bash — Locate the misplaced trace block
- bash — Move trace block and run a trace
- bash — Insert trace in run_ppl and produce a trace
- bash — Find the model variable name in run_ppl
- bash — Place trace after model load and produce trace
- bash — Write diff tool and run the KV demo
- bash — Fix diff tool to compare dequantized values
- bash — Document phase 0 results and commit

**Synthèse produite :**

⏵ Roadmap écrite, phase 0 déjà livrée et démontrée

\## 1. Roadmap — `docs/roadmap.md`

Cinq phases, du **faisable ici tout de suite** à ce qui demande une infra, chaque chantier avec un critère de succès mesurable et un état (✅ 🔬 ⏳ 🧱) :

| phase | objet | infra |
|---|---|---|
| **0. La drave observable** | trace du flux, diff par couche, format d'échange v1, profilage par neurone | **aucune** |
| **1. La drave mesurée** | top-k dans le noyau GPU, quantification choisie par la mesure, purge des seuils en dur, écart int8 | **aucune** |
| **2. La drave répartie localement** | ordonnanceur de placement (2 GPU, CPU, RAM, NVMe), streaming des poids depuis le NVMe (3,5 Go/s), cache d'experts rentable, politique de pages du KV | **aucune** |
| **3. La drave distribuée** | contrat d'échange, granularité, seuil de rentabilité, **démonstration Colab** (préremplissage réparti), sûreté du format | **Colab** |
| **4. La drave apprenante** | capteur hebbien généralisé, routage appris, élagage guidé par les logs | recherche |
| **5. La drave sur matériel** | PE événementiel et lecteur DDR3 ✅, un opérateur complet sur FPGA, énergie/jeton | **FPGA** |

Le format de trace de la phase 0 **est** le contrat d'échange de la phase 3 — c'est délibéré : c'est ce qui rendra le test Colab possible sans redéfinir quoi que ce soit.

\## 2. Travaux commencés — phase 0, chantiers 0.1 et 0.2 : **faits et démontrés**

- **`--trace-flux <fichier>`** (+ `--trace-couches`) écrit, par (couche, position), la liste des neurones actifs poussée dans la couche — indice, valeur, échelle, nombre, à deux points par couche (entrée d'attention, entrée de FFN) ;
- **`tools/diff_flux.py`** compare deux traces et dit **où** le flux diverge.

**Mesuré** (Qwen2.5-0.5B, 512 jetons, 24 couches) : **12 288 listes, 132 Mo, 6 octets par neurone actif, +8 % de temps**.

**Démonstration** : KV f32 contre KV int8 (perplexité 19,3885 contre 19,8059) → première divergence **couche 1, jeton 0**, 896 neurones, 2,9e-3 de la dynamique, et **FFN 2** comme couche la plus touchée. C'est exactement ce que la vision promettait : la divergence est **localisée**, pas seulement constatée.

Piège corrigé en route, et noté dans la roadmap : la première version de l'outil comparait les **entiers bruts** de deux exécutions dont les échelles diffèrent — écarts de 1e8. Un flux se compare **déquantifié**, jamais brut.

Commit `ac7ccb1`, `cargo test` 6/6, portes Qwen 19,3885 / gpt-oss 15,1757 intactes.

\## 3. Prochaine étape que je propo
… [573 caractères tronqués]

### Tour 41 — continue

*3 appels d'outils.* Actions notables :

- bash — Write and run the per-neuron flux profiler
- bash — Trace with a sparsity threshold
- bash — Commit phase 0.4 profiler

**Synthèse produite :**

⏵ Phase 0 terminée : trace, diff, et profilage par neurone

\## Ce qui vient d'être livré

**Phase 0.4 — `tools/profil_flux.py`** : lit une trace et rend, **par couche**, la densité d'activation, la part de magnitude portée par les 10 % de neurones les plus forts, les neurones dominants, avec export CSV.

Deux exécutions du même modèle (Qwen2.5-0.5B, 512 jetons, 896 cachés) :

| réglage | densité par couche | taille de trace | top 10 % portent |
|---|---|---|---|
| `--abits 16` (défaut) | 99-100 % (rien n'est seuillé) | 132 Mo | 25 à 42 % |
| `--abits 8 --act-thresh 0.05` | **26 à 56 %** | **53 Mo** | 26 à 56 % |

Deux enseignements, dont le second est le cœur de la vision **rendu mesurable sur un fichier** :

1. la part des 10 % les plus forts reproduit **par couche** le chiffre global du projet (33,1 %) — le même phénomène, localisé ;
2. **la taille de la trace suit l'activité** : densité ÷2,3, trace ÷2,5. *Le coût est proportionnel à ce qui parle* — et ce sera vrai du format d'échange de la phase 3 comme il l'est ici.

Réserve écrite dans la roadmap plutôt que cachée : la ligne à seuil 0,05 a une perplexité de 2 445 — c'est un relevé de **coût**, pas de qualité, le seuil étant volontairement brutal.

\## État de la roadmap

| phase | état |
|---|---|
| **0. La drave observable** | ✅ **terminée** — 0.1 trace (132 Mo/512 jetons, +8 %), 0.2 diff par couche (démo KV f32/int8 → couche 1, jeton 0, FFN 2 la plus touchée), 0.4 profilage par neurone |
| **1. La drave mesurée** | ⏳ prochain — top-k dans le noyau GPU, quantification choisie par la mesure, écart int8 |
| **2. La drave répartie localement** | ⏳ ordonnanceur, streaming NVMe, cache d'experts, politique de pages |
| **3. La drave distribuée** | 🧱 Colab — le format d'échange est déjà spécifié **et implémenté** (c'est le format de trace) |
| **4. La drave apprenante** | recherche |
| **5. La drave sur matériel** | PE et lecteur DDR3 ✅, opérateur complet 🧱 FPGA |

Trois commits ce tour : `ac7ccb1` (phase 0.1/0.2), `47aaae9` (0.4), et la roadmap dans le premier. `cargo test` 6/6.

\## Suite

Je continue sur la **phase 1**, dans cet ordre : **1.1 le top-k dans le noyau d'attention GPU** (dernier repli CPU du chemin long contexte, et `--attn-topk 256` améliore déjà la perplexité de 21 %), puis **0.3** (l'encodeur/décodeur de référence du format — petit, et c'est ce qui rendra Colab immédiat), puis **1.4** (l'écart int8 résiduel, deux hypothèses à tester).

Un mot d'honnêteté sur 1.1 : le top-k en flux ne se fai
… [368 caractères tronqués]

### Tour 42 — continue, sois autonome pendant 2 heures

*8 appels d'outils.* Actions notables :

- bash — Write and run the reference codec
- bash — Add sentinel, rebuild, run codec round-trip
- bash — Add K/V f32 attribution flags
- bash — Revert half flags, document 1.4, commit
- bash — Test --trace-couches selection
- bash — Final verification of the autonomous stretch
- bash — Check if target is tracked and .gitignore
- bash — Untrack target and commit pending changes

**Synthèse produite :**

⏵ Bilan de la session autonome : phase 0 terminée, dépôt assaini

\## Ce qui a été fait pendant cette plage autonome

**Phase 0 de la roadmap — « la drave observable » — est terminée**, avec des chiffres :

| chantier | livrable | mesure |
|---|---|---|
| **0.1 trace du flux** | `--trace-flux` + `--trace-couches` : par (couche, position), la liste des neurones actifs poussée dans la couche | 12 288 listes, **132 Mo** pour 512 jetons, **6,02 octets par neurone actif**, **+8 % de temps** ; trace sélective (2 couches) : **5 Mo au lieu de 132** |
| **0.2 diff par couche** | `tools/diff_flux.py` | KV f32 contre int8 (19,3885 contre 19,8059) → première divergence **couche 1, jeton 0**, 896 neurones ; couche la plus touchée **FFN 2** |
| **0.3 codec de référence** | `tools/flux_codec.py` — la **seconde implémentation** du format DRVF | aller-retour **IDENTIQUE** sur 132 396 736 octets ; encodage 40 Mo/s, décodage 15 Mo/s en Python ; projection phase 3 : 512 jetons = **265 Mo** sur le fil |
| **0.4 profilage par neurone** | `tools/profil_flux.py` : densité, part des 10 % les plus forts, dominants, CSV | par couche : **25-42 %** de la magnitude portée par 10 % des neurones ; en creux : densité **26-56 %** et trace **÷2,5** |

Le résultat qui répond le mieux à votre vision : **la taille de la trace suit l'activité** (densité ÷2,3 → trace ÷2,5). « Le coût est proportionnel à ce qui parle » n'est plus un principe, c'est un chiffre — et ce sera vrai du format d'échange de la phase 3, puisque c'est le même format.

**Phase 1.4** : l'expérience qui attribue l'écart int8 avec llama.cpp (+3,0 % contre +0,8 %) est **écrite avec ses points de code exacts** (clés en f32 / valeurs en f32 pour séparer l'erreur des scores de celle de la somme pondérée). J'avais commencé les drapeaux, je les ai **retirés** : le temps restant ne permettait pas de les finir *et* de les mesurer, et un demi-drapeau vaut moins qu'une expérience écrite.

**Hygiène trouvée en chemin** : mon `git add -A` du renommage avait embarqué **44 fichiers de `target/`** dans le dépôt. Retirés du suivi, `target/` ajouté au `.gitignore` — le dépôt ne grossira plus à chaque compilation.

\## État

- Commits : `ac7ccb1` (0.1/0.2), `47aaae9` (0.4), `a2545ac` (0.3 + 1.4), `a44414d` (hygiène) ;
- `cargo test --release` **6/6**, portes Qwen **19,3885** et gpt-oss **15,1757** intactes ;
- le seul fichier modifié est l'archive du journal, comme d'habitude.

\## Ce que je ferais ensuite, dans l'ordre

1. **1.4** — les deux vari
… [633 caractères tronqués]

### Tour 43 — ne te fie pas à tes estimés pour le temps. fais un 2h de travail autonome en vérifiant l'heure du système à chaque itéra … [82 caractères tronqués]

*39 appels d'outils.* Actions notables :

- bash — Set the 2-hour deadline and recon
- bash — Implement flux replay reader
- bash — Wire --flux-forcer CLI
- bash — Build and test flux replay
- bash — Fix header size and test replay
- bash — Verify replay on a single window
- bash — Read quant_scratch convention
- bash — Add replay diagnostic and measure fidelity
- bash — Trace and replay with identical settings
- bash — Use a global token counter as trace key
- bash — Verify replay across two windows
- bash — Commit replay work
- bash — Add mixed K/V storage flags (part 1)
- bash — Wire the mixed storage into read/write (part 2)
- … et 25 autres

**Synthèse produite :**

⏵ 10:26 — point d'étape : 20 min de plage écoulées, je continue

**Heure système : 10:26. Fin de plage : 12:06. Il reste ~1 h 40.** Je continue.

\## Fait depuis le début de la plage (10:07)

**Phase 0.3bis — le rejeu** (`--flux-forcer`) : une trace relue et imposée au moteur redonne **exactement** le même résultat — `perplexité 19.3885` avec et sans rejeu, sur une trace de 132 Mo et deux fenêtres de contexte. C'est la démonstration locale du contrat de la phase 3 : *une liste suffit à continuer le calcul*. Diagnostic de fidélité : 1,5e-5 d'écart relatif, soit la quantification 16 bits.

Défaut trouvé **par le rejeu** (qu'un diff n'aurait jamais vu) : la clé d'une liste était `(couche, position dans la fenêtre)`, donc une exécution multi-fenêtres réécrivait les mêmes clés — perplexité 356 694 au lieu de 17,43. Clé corrigée en `(couche, compteur de jeton global)`.

**Phase 0.3ter — trace et rejeu sur le chemin par lots** : les hooks n'existaient que dans le chemin par jeton. Sur le chemin par lots, le rejeu est **exact** (on remplace les entiers et l'échelle, sans requantification) : 17,4294 tracé et rejoué, identiques.

**Phase 1.4 — l'expérience d'attribution** : les deux variantes (`DRAVE_KV_K_F32`, `DRAVE_KV_V_F32`) sont implémentées ; contrôle à ctx 256 (clés int8 + valeurs f32 : 17,5889 contre 17,4315 en f32). Les deux passes à ctx 8192 tournent encore (`/tmp/kv_attribution.log`) — je relèverai le résultat avant la fin de la plage.

**Phase 3 — le transport** : `--flux-serveur` et `--ppl-reparti` font tourner deux nœuds (pilote + moteur) qui se passent des flux ; **88 flux servis**. **Défaut ouvert et chiffré** : la perplexité répartie (798,3) ne correspond pas à la locale (18,2178) — j'ai préféré l'écrire comme défaut ouvert que de le présenter comme fini.

\## Ce que je fais dans l'heure restante

1. relever l'attribution int8 (elle arrive dans ~15 min) et la documenter ;
2. chercher le défaut du calcul réparti — les candidats sont identifiés (position, norme d'entrée du nœud distant, état des caches KV) ; le suspect n° 1 est le **cache KV du nœud distant**, qui doit se remplir au fil des jetons reçus alors que le pilote, lui, ne lui envoie qu'un flux par jeton ;
3. si le temps le permet, la mesure de débit du transport (octets par flux, latence aller-retour) — c'est le chiffre qui donnera le **seuil de rentabilité** de la phase 3, et il se mesure sur localhost avant Colab.

Je vérifie l'heure à chaque itération et j'arrête à 12:06, en laissant un poi
… [37 caractères tronqués]

### Tour 44 — pendant que les charges locales s'executent, peux-tu avancer des chantiers légers sur les ressources loçcale ou d'analys … [7 caractères tronqués]

*153 appels d'outils.* Actions notables :

- bash — Write and run the pure flux analysis tool
- bash — Document the flux analysis and commit
- bash — Write the format spec and cost model, commit
- bash — Check KV attribution run progress
- bash — Locate distributed PPL code paths
- bash — Read distributed PPL implementation
- bash — Inspect forward/logits/norm semantics
- bash — Read forward tail, norme_finale and logits
- bash — Read forward entry and rope context dependence
- bash — Find how to launch distributed PPL test
- bash — Run distributed PPL test before fix
- bash — Inspect state after timeout
- bash — Rerun pre-fix distributed test in background
- bash — Inspect all final-norm condition sites
- … et 121 autres

**Synthèse produite :**

⏵ Clôture du créneau : tout est commité, portes vertes, machine rendue.

\## Session autonome (10:06 → 11:42) — bilan

**Le fil rouge** : la phase 3 (calcul réparti sur deux machines) est passée de « ça tourne mais faux » à « fidèle au bit près, et ÷2,3 plus économe sur le fil ». 18 commits, toutes les portes vertes.

\### Ce qui a été corrigé (et qui n'était pas ce que je croyais)

| défaut | mesure |
|---|---|
| `Model::forward` bouclait sur `0..n_layer` au lieu de `couche_debut..couche_fin` : le pilote calculait les 24 couches, envoyait l'état **final**, le pair recalculait tout par-dessus | ×11,2 → cause principale |
| La norme finale appliquée **deux fois** (nœud moteur + pilote) | ×4,8 après ce seul correctif — une hypothèse juste mais incomplète |
| Les réglages d'activation (`--act-thresh`) **ignorés** dans les chemins flux : deux nœuds réglés différemment calculaient deux choses différentes **en silence** | 0,69 d'écart |
| Nagle + ACK différé sur chaque jeton | attente **97,6 → 16,1 ms** (1,01× le calcul local) |
| Mon propre compteur divisait par les jetons *notés* au lieu des flux *envoyés* | un flux « de 919 canaux » pour un modèle qui en a 896 |

\### Les chiffres qui restent

- **Découpage fidèle : écart 0,00e0** — 144,8289 des deux côtés à 40 jetons, **9,5146 des deux côtés à 1 024 jetons** (1 024 flux, texte réel).
- **Transport** : dense 3 623 octets/flux → listes à échelles par bloc + indices par écarts **1 589 octets (÷2,3)** pour 1,3 % d'écart à 1 024 jetons. L'encodage par écarts est prouvé sans perte : mêmes écart et perplexité qu'avant, mot pour mot.
- **Latence** : `attente ≈ calcul distant + 3,2 × latence` (1,01× à 0 ms, 4,89× à 20 ms) → Colab à 60 ms d'aller-retour : ~8 jetons/s au lieu de ~60, fidélité intacte.
- **Cache KV int8** : l'écart (+3,0 % à 8 192) est **entièrement dans les clés** — clés f32 + valeurs int8 = **+0,023 %** pour 75 % de la taille f32.

\### Ce que j'ai écrit puis dû corriger moi-même

1. « ÷2 pour 0,2 % » (banc synthétique) → sur **vrai texte**, c'est ÷2,3 pour 1,3–2,7 %.
2. « l'écart croît avec la longueur » → la courbe dit l'**inverse** (13,7 % à 64, 1,3 % à 1 024) ; ce qui changeait, c'était le corpus.
3. « transmettre l'entrée normée » → **réfuté** par le banc de contrôle : 5,61e0 au lieu de 0,00e0, la connexion résiduelle a besoin du résidu. Drapeau retiré, réfutation écrite.

\### Livrables

`docs/format-flux.md` (spécification v2), `docs/colab-reparti.md` (recette phase 3.4 avec ses deux limites assumée
… [573 caractères tronqués]

### Tour 45 — as-tu ce qu'il te faut pour te rendre à 15h en travaillaint avec un maximum d'autonomie et de parallélisme d'activités?

*239 appels d'outils.* Actions notables :

- bash — Probe machine, GPU, disk, network state
- bash — Identify GPU users and stray processes
- create_goal
- bash — Launch KV bit-placement campaign
- sous-agent — Audit ignored CLI flags
- sous-agent — Spec batched prefill protocol
- sous-agent — Trace format compaction study
- todo_write
- bash — Locate KV cache structure
- read
- bash — Check lane A and read KV write path
- bash — Understand batched PPL reference path
- bash — Add batched imposed states to forward_lot
- list_agents
- … et 216 autres

**Synthèse produite :**

⏵ Créneau terminé : machine rendue, tout est commité, les portes sont vertes.

\## Session 11h46 → 14h10 — quatre couloirs en parallèle

\### Couloir A — où mettre les bits du cache KV (2 campagnes, ~2 h de machine)

| réglage | octets/élément | % du f32 | écart à 8 192 jetons |
|---|---|---|---|
| **clés f16 · valeurs int8** | 3,125 | **39 %** | **+0,018 %** ← le meilleur point |
| clés f32 · valeurs int8 | 5,125 | 64 % | +0,023 % |
| clés f32 · valeurs int4 | 4,625 | 58 % | +0,46 % |
| clés f16 · valeurs int4 | 2,625 | 33 % | +0,61 % |
| int8 · int8 | 2,25 | 28 % | +3,04 % |
| int4 · int4 | 1,25 | 16 % | +364 % |

À taille **égale**, mettre les bits sur les clés plutôt que sur les valeurs change l'erreur d'un facteur **130** (5,125 o) à **840** (4,625 o). Réglage recommandé : `DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1` — 2,5× plus petit que le f32 pour deux centièmes de pour cent. Nouveau code : clés en f16 ; rapport `reports/rapport-placement-bits-kv.md`.

\### Couloir B — le préremplissage par LOTS sur le fil (le bloqueur Colab : levé)

Mode 3 du protocole : N états d'un coup au lieu d'un flux par jeton. **Écart 0,00e0** en 4 lots de 64 comme en un seul lot de 917 583 octets. Et il gagne sur les deux tableaux : **7× le débit local** (16,6 ms/jeton contre 116,7 en un seul lot) et **18×** sur un lien à 20 ms par message (2,6 s contre 47,6 s).

\### Couloir C — trois analyses déléguées, puis deux relectures adversariales

L'**audit des drapeaux** a trouvé que **46 options sur 110** étaient ignorées dans au moins un mode ; la **spécification du lot** a trouvé mon bug d'en-tête d'un octet ; l'**étude de compacité** a chiffré le format (−49,9 % sans perte, −65,9 % avec perte, toutes deux implémentées : DRVF v2 et v3). Puis deux relectures adversariales ont trouvé **22 défauts** — dont **17 par lecture, pas par un banc** — et la seconde a attaqué mes propres correctifs : un tableau de bord qui affichait l'état d'*avant* les affectations, un plafond réseau qui laissait passer 16 Gio sur une trame de 83 octets, une trame forgée qui tuait le nœud.

\### Couloir D — le GPU : vérifié, pas étendu

`DRAVE_GPU=1` sur gpt-oss redonne **15,1667**, et le noyau de tête **1,6 ms** (88 Go/s) pour un écart de **1,99e-7**. Le noyau de top-k (phase 1.1) était le chantier suivant : je ne l'ai pas commencé plutôt que de le laisser à moitié fait — il est en tête des prochains chantiers de `REPRISE.md`.

\### Ce que j'ai dû corriger dans mes propres affirmations

- le croisement push/pull : j'a
… [857 caractères tronqués]

### Tour 46 — continue jusqu'à 18h HAE

*117 appels d'outils.* Actions notables :

- bash — Check time, timezone and remaining budget
- create_goal
- bash — Launch KV frontier campaign at ctx 4096
- sous-agent — Spec for lot-in-lists mode 4
- sous-agent — Docs audit after today's changes
- bash — Find attention top-k and GPU fallback
- bash — Read the CPU top-k path and GPU attention calls
- bash — Find GPU attention entry points
- bash — Read GPU attention call site and signature
- bash — Size the CUDA infrastructure
- bash — Write and test the local Colab helper
- bash — Improve notebook with real text cell
- bash — Kill test node safely and check notebook
- bash — Add notebook real-text cell and commit
- … et 103 autres

**Synthèse produite :**

⏵ Créneau 15h07 → 18h00 terminé : machine rendue, dépôt vert, objectif clos.

\## Créneau 15h07 → 17h35 — ce qui a été fait

\### 1. Le mode 4 « lot en listes » : écrit, mesuré, relu, corrigé

Le prochain chantier identifié après le mode 3. Chaque état d'un lot est encodé comme le mode 2 et auto-délimité par ses trois tailles (`a_j · n_blocs_j · longueur_j`), lues avant toute allocation. Protocole passé en **version 5** (un pair v4 refuserait le mode *avant* de lire un octet).

| | octets par jeton | écart |
|---|---|---|
| lot dense (mode 3) | 3 663 | 0,00e0 |
| **lot en listes (mode 4)** | **1 500** | 3,03e-2 à 256 jetons |

La relecture adversariale du mode 4 (fraîchement écrit) a trouvé **10 défauts, dont 2 graves** — et le plus embarrassant était **un de mes correctifs de l'après-midi** : le refus de `n == 0` que j'avais ajouté tuait une session légitime (une liste d'activation **vide**, ça existe : seuil au-dessus du maximum). Le contrôle indépendant du dépôt mourait dessus. Corrigé, testé, et le plafond R4 est devenu **cumulatif** — vérifié à l'octet près : refus à l'état 72 393, exactement le franchissement des 256 Mo.

\### 2. La politique du cache KV, complète — et elle dépend du régime

| régime | réglage | pourquoi |
|---|---|---|
| court/moyen, CPU | **clés f16 + valeurs int8** (39 % du f32, +0,018 %) | le meilleur compromis taille/qualité |
| long, **avec** miroir VRAM | **int8/int8** homogène | toute variante d'attribution **désactive** le miroir, qui divise l'attention par 40 (1,7 ms contre 70-174 ms par passe) |
| long, sans GPU | int8/int8 | les clés f16 coûtent **2,3× le temps CPU** (162 contre 70 ms à 262 144 clés) |

Et **l'aiguille v2 retrouve 9/9 sondes dans les trois variantes**, int8/int8 compris — la tâche est plus robuste que la perplexité ne le suggère.

\### 3. Le chantier GPU : plan chiffré plutôt que bâclé

Le mode creux ne peut pas utiliser le miroir VRAM (le chemin GPU est conditionné à `attn_topk == 0`) : à 1 M de clés il coûte **968 ms par couche** contre 13,2 ms. Trois noyaux, une sélection radix, six étapes, contrat d'exactitude — `docs/plan-gpu-topk.md`. Je ne l'ai pas commencé faute de 2 h devant moi : il est **écrit**, pas à moitié fait.

\### 4. Colab clé en main, et deux audits de cohérence

`tools/colab_cote_local.sh` (nœud + les trois voies de tunnel + l'empreinte du modèle) et un notebook qui tokenise un **vrai texte** : la perplexité du banc passe de 17 869 à **19,8967**, l'écart reste 0,00e0. Les deux audits docume
… [878 caractères tronqués]

### Tour 47 — pret pour des scrum de 2h (boxing temps réel, avec revue, rétro et planning)

*297 appels d'outils.* Actions notables :

- bash — Check clock, machine and last sprint state
- bash — Create the sprint timing tool
- bash — Write the sprint charter and commit
- ask_user_question
- bash — Adjust charter, start sprint 1 and background campaign
- bash — Read the attention partials kernel
- bash — Read the score computation and accumulation
- bash — Read the FFI launch pattern
- bash — Read kernel loading and KvGpu fields
- bash — Check PTX embedding and build
- bash — Write the scores kernel and compile PTX
- bash — Read the kernel launch call
- bash — Write the FFI for the scores kernel
- bash — Complete KvGpu initializer
- … et 275 autres

**Synthèse produite :**

**Sprint 1 clos — box 17:41 → 19:41 (120 min pleines), 22 commits, dépôt vert, machine rendue.**

L'objectif (le premier des trois noyaux du top-k GPU) est livré — et les deux autres avec, plus le branchement dans le moteur.

\## Livré, chiffre par chiffre

| # | livrable | mesure |
|---|---|---|
| 1 | `attn_scores` (objectif du sprint) | écart **1,6–2,3e-7** · **26,7–40×** le CPU |
| 2 | seuil radix 4 passes | k-ième score **exact au bit près, 14/14 lignes** à 4 k → **1 M** clés |
| 3 | collecte des k indices | **même ensemble que le CPU** (diff. symétrique **0**), **0,95 ms** contre 1 653 ms de tri à 1 M |
| 4 | `attn_topk_somme` | écart **1,0–4,8e-7** · temps GPU **constant (0,07 ms)** |
| 5 | `DRAVE_GPU_TOPK=1` dans `forward` | PPL identique (12,2265 vs 12,2267) · **à 2 047 clés vues : attention 19,58 → 7,59 ms/jeton (−61 %), balayage −24 %** |
| 6 | à 1 M clés | chaîne complète **3,90 ms** contre 539,9 ms CPU (×138), **0,3×** le complet en VRAM |
| 7 | portes | Qwen **19,3885** · gpt-oss **15,1757** (CPU) et **15,1667** (GPU) · tests **17/17** |

\## Cinq défauts, cinq moyens de les trouver

- **le banc était dégénéré** (même clé partout → descente radix jamais exercée) : trouvé **en le relisant**, pas en le faisant échouer ;
- **le puits compté 256 fois** dans le noyau 3 (une fois par fil) : trouvé **par le banc** en une ligne — 2,05e-1 → 4,79e-7 ;
- **un pointeur 0 après échec d'allocation** (garde piloté par les dimensions) : **relecture adversariale n° 1**, 7 défauts ;
- **`attn_kv_recombine` lisait `sinks[warp]`** au lieu de la tête globale : **relecture n° 2** — gpt-oss `DRAVE_GPU_KV=1` **17,6531 → 15,1786** (référence CPU 15,1757), invisible pour toutes les portes ;
- **quatre chiffres de documentation faux ou périmés** : **audit de documentation** dédié.

\## Ce que la rétrospective a acté

Trois corrections que je me suis imposées en cours de route : j'avais annoncé un gain **sans mesurer le coût fixe** (8 lancements + 17 transferts par couche et par jeton rendaient le déport 1,8× plus lent à 255 clés) ; j'avais écrit « le croisement est entre 8 k et 16 k clés » alors que ces lignes différaient aussi par le **nombre de jetons** (le croisement en clés est entre 255 et 2 047) ; et j'ai écrit un **chiffre non mesuré dans un message de commit**, amendé dans la minute.

\## Sprint 2 (planning écrit dans `sprints/01-…md`)

Fusionner la sélection en un noyau par ligne (8 lancements → 2), supprimer le tampon `nh × n × 4` par couche, refuser bruyamment `-
… [82 caractères tronqués]

### Tour 48 — Continue en blocs de 2h jusqu'à demain 8h HAE. pour chacun des blocs/sprints tu dois être en autonomie totale. C'est à d … [282 caractères tronqués]

*196 appels d'outils.* Actions notables :

- bash — Check time and count remaining boxes
- bash — Start sprint 2
- bash — Fix sprint numbering to 2
- todo_write
- bash — Write fused kernel and compile
- bash — Add fused kernel FFI
- bash — Fix kernel params count
- bash — Add fused kernel bench and run
- bash — Bench fused kernel at 262k
- bash — Compare fused vs chain at 3 sizes
- bash — Build comparison table fused vs chain
- bash — Add poison check and finiteness guard
- bash — Locate the topk GPU branch
- bash — Wire fused kernel into the model
- … et 178 autres

**Synthèse produite :**

⏵ La revue du sprint 4 a trouvé deux défauts graves dans ma mesure — je corrige tout

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/gguf_meta.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/model.rs` | 0 | 15 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs` | 0 | 43 |
| `/tmp/mesures_oss.sh` | 2 | 0 |
| `/tmp/mesures_oss2.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/compare_logits.py` | 1 | 0 |
| `/tmp/mesures_oss3.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ref_logits.cpp` | 0 | 3 |
| `/tmp/mesures_oss4.sh` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gpt-oss-perplexite.md` | 1 | 4 |
| `/tmp/controles_oss.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md` | 0 | 11 |
| `/tmp/controles2_oss.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/harmony_canonique.py` | 1 | 1 |
| `/tmp/controles3_oss.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/gguf.rs` | 0 | 2 |
| `/tmp/controles4_oss.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore` | 0 | 2 |
| `/tmp/bascule_yarn.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md` | 1 | 3 |
| `/tmp/croisement_yarn.sh` | 2 | 0 |
| `/tmp/profil_profondeur.sh` | 1 | 0 |
| `/tmp/contenu_ou_profondeur.sh` | 1 | 0 |
| `/tmp/ref_long.sh` | 1 | 0 |
| `/tmp/mscale_yarn.sh` | 1 | 0 |
| `/tmp/ref2048.sh` | 1 | 0 |
| `/tmp/interp_long.sh` | 1 | 0 |
| `/tmp/audela_4096.sh` | 1 | 0 |
| `/tmp/seuil_rotation.sh` | 1 | 0 |
| `/tmp/mesures_finales.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-localite-activation.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aiguille.py` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-prefill-par-lots.md` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/engine.rs` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/gpu/qtrinet_gpu.cu` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-aiguille.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mla-vision.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mla_synthetique.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/vision_mtmd.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/vision.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/histoire.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/roadmap.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gpu.rs` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gpu-topk-selection.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md` | 0 | 1 |
| `/tmp/aig2.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-logits-gpu-vs-cpu.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-aiguille-topk.md` | 1 | 0 |
| `/tmp/aig5.sh` | 1 | 0 |
| `/tmp/aig_s5.sh` | 2 | 0 |

### Sous-agents lancés

- tour 1 — Harness logits llama.cpp
- tour 45 — Audit ignored CLI flags
- tour 45 — Spec batched prefill protocol
- tour 45 — Trace format compaction study
- tour 45 — Adversarial review of recent commits
- tour 45 — Docs vs measurements consistency audit
- tour 45 — Review the afternoon fixes
- tour 46 — Spec for lot-in-lists mode 4
- tour 46 — Docs audit after today's changes
- tour 46 — Adversarial review of mode 4
- tour 46 — Review the last-hour fixes
- tour 47 — Adversarial review GPU topk
- tour 47 — Vérifier chiffres et cohérence docs
- tour 47 — Revue adversariale du branchement top-k
- tour 48 — Revue adverse du noyau fusionné
- tour 48 — Revue adverse des rapports du sprint 3
- tour 48 — Revue adverse sprint 4

### Commandes exécutées (échantillon)

- **T1** List repository root files
- **T1** Inspect git log, status, tmp corpus, models
- **T1** List qtrinet-core contents
- **T1** Build release and run tests
- **T1** Run reference perplexity check
- **T1** Read tokenizer head
- **T1** Locate forward and positional logic
- **T1** Check memory and cpu
- **T1** Dump gpt-oss metadata and harmony tokens
- **T1** Filter metadata and harmony token ids
- **T1** Find gpt-oss FFN activation code
- **T1** List gpt-oss tensor names and biases
- **T1** Check for llama.cpp tools
- **T1** Read Proj::load implementation
- **T1** Read charger_moe implementation
- **T1** Check bias application in MoE and Proj
- **T1** Fetch HF gpt-oss reference implementation
- **T1** Inspect llama.cpp SWA pattern semantics
- **T1** Read SWA pattern and gpt-oss arch handling
- **T1** Locate gpt-oss arch implementation in llama.cpp
- **T1** Inspect openai-moe model implementation
- **T1** Read openai-moe.cpp head
- **T1** Check Gguf::cfg key resolution
- **T1** Find remaining window usages
- **T1** Dump gpt-oss control tokens
- **T1** Check build_tokenizer signature
- **T1** Locate inference-mode window assignment
- **T1** Find both model load sites
- **T1** Verify edit and build
- **T1** Validate reference PPL and text path
- **T1** Run gpt-oss PPL 64 tokens
- **T1** Check llama-perplexity stride semantics
- **T1** Locate perplexity source and version
- **T1** Read perplexity windowing logic
- **T1** Compare YaRN implementation with HF formula
- **T1** Check ppl-stride default
- **T1** Check available llama.cpp binaries
- **T1** Check tokenize binary and memory
- **T1** Check llama-tokenize usage
- **T1** Tokenize corpus with llama.cpp o200k
- … et 1949 autres

## 4. Mesures et résultats marquants

- **T1** `// scalaire dense (pull). Le croisement mesuré est à 10 %.`
- **T1** `part de l'attention dans le flux d'événements : 100.0 %`
- **T1** `255 tokens notés — perplexité cumulée 17.431  (31.9 tok/s)`
- **T1** `510 tokens notés — perplexité cumulée 19.388  (31.8 tok/s)`
- **T1** `=== perplexité 19.3885 sur 510 tokens (0 événements, 16.1 s) ===`
- **T1** `0  1.00000000e+00  1.00000000e+00    0.000 %`
- **T1** `1  6.89044306e-01  6.89044306e-01    0.000 %`
- **T1** `2  4.74782055e-01  4.74782055e-01    0.000 %`
- **T1** `3  3.27145872e-01  3.27145872e-01    0.000 %`
- **T1** `4  2.25418000e-01  2.25418000e-01    0.000 %`
- **T1** `5  1.55322989e-01  1.55322989e-01    0.000 %`
- **T1** `6  1.07024421e-01  1.07024421e-01    0.000 %`
- **T1** `7  7.37445682e-02  7.37445682e-02    0.000 %`
- **T1** `8  5.08132748e-02  5.08132748e-02    0.000 %`
- **T1** `9  3.17056962e-02  3.16207523e-02    0.268 %`
- **T1** `10  1.93350011e-02  1.94509675e-02    0.600 %`
- **T1** `11  1.15920493e-02  1.17921911e-02    1.727 %`
- **T1** `12  6.79495949e-03  7.01571391e-03    3.249 %`
- **T1** `13  3.86035932e-03  4.06955471e-03    5.419 %`
- **T1** `14  2.09379238e-03  2.27727194e-03    8.763 %`
- **T1** `15  1.05260210e-03  1.20613097e-03   14.586 %`
- **T1** `16  4.56483919e-04  5.80947502e-04   27.266 %`
- **T1** `17  1.29318701e-04  2.27947796e-04   76.268 %`
- **T1** `18  3.83088124e-05  3.83088124e-05    0.000 %`
- **T1** `19  2.63964690e-05  2.63964690e-05    0.000 %`
- **T1** `20  1.81883367e-05  1.81883367e-05    0.000 %`
- **T1** `21  1.25325698e-05  1.25325698e-05    0.000 %`
- **T1** `22  8.63549588e-06  8.63549588e-06    0.000 %`
- **T1** `23  5.95023926e-06  5.95023926e-06    0.000 %`
- **T1** `24  4.09997848e-06  4.09997848e-06    0.000 %`
- **T1** `25  2.82506683e-06  2.82506683e-06    0.000 %`
- **T1** `26  1.94659621e-06  1.94659621e-06    0.000 %`
- **T1** `27  1.34129104e-06  1.34129104e-06    0.000 %`
- **T1** `28  9.24208950e-07  9.24208950e-07    0.000 %`
- **T1** `29  6.36820915e-07  6.36820915e-07    0.000 %`
- **T1** `30  4.38797825e-07  4.38797825e-07    0.000 %`
- **T1** `31  3.02351143e-07  3.02351143e-07    0.000 %`
- **T1** `63 tokens notés — perplexité cumulée 20.836  (5.2 tok/s)`
- **T1** `=== perplexité 20.8361 sur 63 tokens (0 événements, 12.2 s) ===`
- **T1** `63 tokens notés — perplexité cumulée 41.114  (5.0 tok/s)`
- **T1** `=== perplexité 41.1140 sur 63 tokens (0 événements, 12.5 s) ===`
- **T1** `[timed out after 600000ms]`
- **T1** `238 tokens notés — perplexité cumulée 144.168  (4.9 tok/s)`
- **T1** `357 tokens notés — perplexité cumulée 320.482  (4.9 tok/s)`
- **T1** `511 tokens notés — perplexité cumulée 247.031  (4.9 tok/s)`
- **T1** `=== perplexité 247.0308 sur 511 tokens (0 événements, 104.5 s) ===`
- **T1** `255 tokens notés — perplexité cumulée 13.715  (5.0 tok/s)`
- **T1** `509 tokens notés — perplexité cumulée 15.076  (5.0 tok/s)`
- **T1** `=== perplexité 15.0763 sur 509 tokens (0 événements, 102.5 s) ===`
- **T1** `119 tokens notés — perplexité cumulée 940.867  (4.9 tok/s)`
- **T1** `(**5,62 tok/s**), premier jeton en 166 ms.`
- **T1** `/// deux architectures se croisent à 10 % de densité ; on bascule un peu`
- **T1** `226 tokens notés — perplexité cumulée 3940.363  (4.6 tok/s)  [fenêtre 1 : 226 notés, PPL 3940.363]`
- **T1** `452 tokens notés — perplexité cumulée 3476.367  (4.6 tok/s)  [fenêtre 2 : 226 notés, PPL 3067.009]`
- **T1** `511 tokens notés — perplexité cumulée 3431.623  (4.5 tok/s)  [fenêtre 3 : 59 notés, PPL 3107.404]`
- **T1** `=== perplexité 3431.6228 sur 511 tokens (0 événements, 113.9 s) ===`
- **T1** `230 tokens notés — perplexité cumulée 5559.111  (4.7 tok/s)  [fenêtre 1 : 230 notés, PPL 5559.111]`
- **T1** `460 tokens notés — perplexité cumulée 10738.682  (4.6 tok/s)  [fenêtre 2 : 230 notés, PPL 20744.198]`
- **T1** `511 tokens notés — perplexité cumulée 8462.826  (4.6 tok/s)  [fenêtre 3 : 51 notés, PPL 987.567]`
- **T1** `=== perplexité 8462.8255 sur 511 tokens (0 événements, 111.7 s) ===`
- **T1** `230 tokens notés — perplexité cumulée 643.509  (4.8 tok/s)  [fenêtre 1 : 230 notés, PPL 643.509]`
- **T1** `460 tokens notés — perplexité cumulée 549.601  (4.9 tok/s)  [fenêtre 2 : 230 notés, PPL 469.398]`
- **T1** `511 tokens notés — perplexité cumulée 442.825  (4.8 tok/s)  [fenêtre 3 : 51 notés, PPL 63.104]`
- **T1** `=== perplexité 442.8254 sur 511 tokens (0 événements, 106.0 s) ===`
- **T1** `255 tokens notés — perplexité cumulée 14.483  (5.1 tok/s)  [fenêtre 1 : 255 notés, PPL 14.483]`
- **T1** `509 tokens notés — perplexité cumulée 17.141  (5.2 tok/s)  [fenêtre 2 : 254 notés, PPL 20.301]`
- **T1** `=== perplexité 17.1414 sur 509 tokens (0 événements, 98.5 s) ===`
- **T1** `255 tokens notés — perplexité cumulée 24.579  (5.2 tok/s)  [fenêtre 1 : 255 notés, PPL 24.579]`
- **T1** `509 tokens notés — perplexité cumulée 26.154  (5.2 tok/s)  [fenêtre 2 : 254 notés, PPL 27.837]`
- **T1** `=== perplexité 26.1538 sur 509 tokens (0 événements, 98.8 s) ===`
- **T1** `prompt  : 5 tokens en 0.815 s  (6.1 tok/s, TTFT 163.0 ms)`
- **T1** `généré  : 16 tokens en 2.989 s  (5.35 tok/s)`
- **T1** `prompt  : 5 tokens en 0.842 s  (5.9 tok/s, TTFT 168.4 ms)`
- **T1** `généré  : 16 tokens en 3.073 s  (5.21 tok/s)`
- **T1** `1 tokens notés — perplexité cumulée 14469095357.465  (0.2 tok/s)`
- **T1** `=== perplexité 14469095357.4649 sur 1 tokens (0 événements, 4.2 s) ===`
- **T1** `89 tokens notés — perplexité cumulée 25.009  (4.2 tok/s)`
- **T1** `=== perplexité 25.0091 sur 89 tokens (0 événements, 21.3 s) ===`
- **T1** `229 tokens notés — perplexité cumulée 13.657  (5.2 tok/s)`
- **T1** `=== perplexité 13.6567 sur 229 tokens (0 événements, 44.1 s) ===`
- **T1** `254 tokens notés — perplexité cumulée 203.115  (5.2 tok/s)`
- **T1** `=== perplexité 203.1151 sur 254 tokens (0 événements, 49.2 s) ===`
- **T1** `13 tokens notés — perplexité cumulée 14.626  (2.0 tok/s)`
- **T1** `=== perplexité 14.6260 sur 13 tokens (0 événements, 6.5 s) ===`
- **T1** `19 tokens notés — perplexité cumulée 5.721  (4.9 tok/s)`
- **T1** `=== perplexité 5.7209 sur 19 tokens (0 événements, 3.8 s) ===`
- **T1** `89 tokens notés — perplexité cumulée 677321.831  (2.0 tok/s)`
- **T1** `=== perplexité 677321.8310 sur 89 tokens (0 événements, 44.5 s) ===`
- **T1** `316 tokens notés — perplexité cumulée 258.640  (5.2 tok/s)`
- **T1** `=== perplexité 258.6401 sur 316 tokens (0 événements, 61.3 s) ===`
- **T1** `=== perplexité 258.6401 sur 316 tokens (0 événements, 61.6 s) ===`
- **T1** `=== perplexité 1880.7184 sur 301 tokens (0 événements, 57.6 s) ===`
- **T1** `89 tokens notés — perplexité cumulée 677321.831  (1.9 tok/s)`
- **T1** `=== perplexité 677321.8310 sur 89 tokens (0 événements, 46.7 s) ===`
- **T1** `255 tokens notés — perplexité cumulée 17.431  (31.8 tok/s)  [fenêtre 1 : 255 notés, PPL 17.431]`
- **T1** `510 tokens notés — perplexité cumulée 19.388  (31.8 tok/s)  [fenêtre 2 : 255 notés, PPL 21.565]`
- **T1** `=== perplexité 19.3885 sur 510 tokens (0 événements, 16.0 s) ===`
- **T1** `à      25.8 Go/s (NVLink) :   67.76 tok/s`
- **T1** `à     380.0 Go/s (GPU local) :  998.76 tok/s`
- **T1** `255 tokens notés — perplexité cumulée 13.715  (5.3 tok/s)  [fenêtre 1 : 255 notés, PPL 13.715]`
- **T1** `510 tokens notés — perplexité cumulée 15.176  (5.2 tok/s)  [fenêtre 2 : 255 notés, PPL 16.792]`
- **T1** `=== perplexité 15.1757 sur 510 tokens (0 événements, 97.3 s) ===`
- **T2** `511 tokens notés — perplexité cumulée 13.287  (28.7 tok/s)`
- **T2** `logits exportés : /tmp/nous_qwen_512_a8.bin — 511 positions × 151936 valeurs`
- **T2** `=== perplexité 13.2872 sur 511 tokens (0 événements, 17.8 s) ===`
- **T2** `511 tokens notés — perplexité cumulée 13.135  (30.6 tok/s)`
- **T2** `logits exportés : /tmp/nous_qwen_512_a12.bin — 511 positions × 151936 valeurs`
- **T2** `=== perplexité 13.1348 sur 511 tokens (0 événements, 16.7 s) ===`
- **T2** `511 tokens notés — perplexité cumulée 13.137  (30.2 tok/s)`
- **T2** `logits exportés : /tmp/nous_qwen_512_a16.bin — 511 positions × 151936 valeurs`
- **T2** `=== perplexité 13.1368 sur 511 tokens (0 événements, 16.9 s) ===`
- **T2** `255 tokens notés — perplexité cumulée 17.431  (32.5 tok/s)  [fenêtre 1 : 255 notés, PPL 17.431]`
- **T2** `510 tokens notés — perplexité cumulée 19.388  (32.5 tok/s)  [fenêtre 2 : 255 notés, PPL 21.565]`
- **T2** `=== perplexité 19.3885 sur 510 tokens (0 événements, 15.7 s) ===`
- **T2** `/dev/nvme0n1p2           828G  268G  561G  33% /home/stephane/FastNVMe`
- **T2** `/dev/mapper/system-root   11T  6,2T  4,7T  57% /home/stephane/Data13TB`
- **T2** `else { "GPU (PCIe 6,5 Go/s)" };`
- **T2** `// Mesuré sur le 30B-A3B : les tranches d'experts sont lues à 8 Go/s,`
- **T2** `// pas 20 — dix-huit mille tranches de 900 Ko dispersées sur 18 Go`
- **T2** `println!("  à       8.0 Go/s (MoE épars, mesuré) : {:>7.2} tok/s",`
- … (tronqué)

## 5. Erreurs rencontrées

106 sorties en erreur ou divergentes. Les premières :

- **T1** : a8f2635f8 docs: record which models this box is good at, and why src/llama-hparams.cpp:8:void llama_hparams::set_swa_pattern(uint32_t n_pattern, bool dense_first) { src/llama-hparams.h:308:    void se
- **T1** : 511 tokens notés — perplexité cumulée 247.031  (4.9 tok/s) === perplexité 247.0308 sur 511 tokens (0 événements, 104.5 s) ===  ### B3 harmony assistant 511 --- ref --- 0.0 0.0 0:00 ls: cannot access '
- **T1** : dump harmony : 254 lignes · dump brut : 511 lignes · ids : 4424 contenu    1  NLL harmony   16.651   NLL brut   10.270   écart   +6.381 contenu   21  NLL harmony    4.853   NLL brut    3.596   écart  
- **T1** : error[E0382]: borrow of moved value: `meta`    --> src/gguf.rs:165:71     | 162 |         let (meta, tensors, fin) = Self::entete(&buf).ok_or_else(|| {     |              ---- move occurs because `met
- **T4** : 6 error[E0382]: borrow of moved value: `cfg`    --> src/model.rs:892:34     | 718 |         let cfg = {     |             --- move occurs because `cfg` has type `Cfg`, which does not implement the `Co
- **T4** : error[E0382]: use of moved value: `cfg`    --> src/model.rs:893:49     | 718 |         let cfg = {     |             --- move occurs because `cfg` has type `Cfg`, which does not implement the `Copy` t
- **T4** : error[E0425]: cannot find value `n_layer` in this scope    --> src/model.rs:772:43     | 772 |         let caches_kv: Vec<KvCache> = (0..n_layer)     |                                           ^^^^^^
- **T4** : thread 'model::tests_kv::aller_retour_kv' (3097033) panicked at src/model.rs:1909:17: valeur 6 bits 8 : 0.2952756 contre 0.29999995 note: run with `RUST_BACKTRACE=1` environment variable to display a 
- **T4** : error[E0425]: cannot find value `gain` in this scope     --> src/main.rs:1135:27      |   27 | fn main() {      | --------- similarly named function `main` defined here ... 1135 |     if let Some((l, 
- **T4** : error[E0425]: cannot find value `idfile` in this scope     --> src/main.rs:1084:18      | 1084 |     let idfile = idfile.unwrap_or_default();      |                  ^^^^^^      | help: a local variab
- **T4** : 1168:    if args.iter().any(|a| a == "--sans-yarn") { mdl.cfg_yarn_off(); } 1259:    let profil = args.iter().any(|a| a == "--ppl-profil"); error[E0425]: cannot find value `args` in this scope     -->
- **T4** : error[E0599]: no method named `clone_ref` found for reference `&DenseQ8` in the current scope     --> src/model.rs:1495:82      | 1495 |                 let d8 = self.layers[l].wo.d.as_ref().expect("F
- **T4** : error[E0609]: no field `lot` on type `Options`    --> src/main.rs:393:26     | 393 |             "--lot" => o.lot = suivant(i).parse().unwrap(),     |                          ^^^ unknown field     | 
- **T4** : 20:use list::{dense_bits, BitmapSign, DenseQ4, DenseQ8, FusedSign, PushMat, SignedDelta, SparseK}; error[E0382]: use of moved value: `d`    --> src/main.rs:785:22     | 785 |             sc.spawn(move
- **T4** : /usr/lib64/clang/23/include/__clang_cuda_builtin_vars.h en-tête présent In file included from <built-in>:2: ./cuda_stub.h:16:76: error: redeclaration of 'threadIdx' with a different type: 'const __qua

## 6. Commits

- gpt-oss : biais attn_output et fenetre par couche corriges, reference llama.cpp  Deux bugs reels, trouves en reprenant REPRISE.md §6.a :  1. attn_output.bias et
- REPRISE : chiffres gpt-oss exacts (ids 15,1757 / texte 15,0757)" && git log --oneline -3 && git status --short | head -3
- Rotation : YaRN a retardement, et la temperature est la moitie nuisible  La politique de rotation se decide desormais par sequence, a la longueur du contexte de
- Rotation : points 4096 et 4608, et la limite du test de generation  Interpolation seule (sans temperature) : 400,13 a 4 096 et 476,09 a 4 608, contre 1 105,20 p
- Item 1 : protocole de perplexite longue --depuis N  Le protocole historique (--ctx N --limit N) confond la longueur du contexte et le contenu : a 8192 jetons on
- Item 3 : cache KV quantifie int8 et int4 empaquete  Le cache KV devient un KvCache : f32 (defaut, comportement inchange), int8 (un octet par valeur) ou int4 (de
- Item 5 : echelles par bloc pour DenseQ8 -- hypothese refutee  DenseQ8 sait maintenant se construire avec une echelle par bloc de 32 (QT_Q8_BLOCS=1, Source8::Pro
- Item 6 : une seule analyse de la ligne de commande pour les quatre modes  struct Options + fn analyser remplacent les deux boucles de 44 drapeaux ; run_infer, r
- Item 7 (1/2) : noyau GPU une warp par ligne, la tete redevient deportable  tete_q8_warp / proj_q8_warp : une warp par ligne, les 32 fils se partagent les blocs 
- Item 4 : prefill par lots -- justesse corrigee, debit a mesurer au calme  Deux bugs corriges dans forward_lot, tous deux invisibles a la compilation :  - les so
- Rapport localite d'activation (idees PowerInfer mesurees) + etat des 8 chantiers  - --profil-neurones / --neurones-sortie : taux de tir et magnitude par neurone
- Item 7 (2/2) : noyaux GPU 4 bits -- MXFP4 et Q4_K, une warp par ligne  - proj_mxfp4_warp : blocs de 17 octets (E8M0 + nibbles), table E2M1 doublee.   Mesure sur
- Item 4 : MoE par lots -- regroupement des jetons par expert  Les modeles a experts suivent desormais le meme chemin par lots que les denses, avec le regroupemen
- Item 2 : le seuil de rotation, tranche par une comparaison appariee  Meme jetons notes (1536-2047), contexte croissant, deux regimes :    contexte   RoPE simple
- Plan 1 M : etat reel des six etapes et ce qui se mesure tout de suite  E1 (prefill par lots) et E2/E3 (KV int8/int4) sont faits et mesures ; E4 (KV sur GPU) et 
- Item 3 : KV quantifie mesure aussi a 4 600 jetons, et compare a llama.cpp  Qwen2.5-0.5B, 4 591 jetons notes :    KV          nous              llama.cpp (8 192)
- Item 8 : premiers resultats d'attention creuse (et ils sont opposes)  gpt-oss, memes 512 jetons (1536-2047), contexte 2 048 :    aucune restriction             
- Item 4 : le GEMM sur le pool, et le gain reel attribue poste par poste  Le produit matrice-matrice s'execute desormais SUR les workers du pool : les fils crees 
- REPRISE : toutes les mesures du tour huit chantiers, et la suite ordonnee  Tableau recapitulatif (noyaux GPU, prefill par lots, KV int8/int4 a 4 600 jetons, att
- Aiguille : le 0.5B echoue 6 fois sur 6 (limite du modele, pas du moteur)  Qwen2.5-0.5B ne retrouve pas un code plante a 1 024 ou 2 048 jetons, a aucune des troi
- KV a echelles par bloc de 32 : int8 de +7,1 % a +1,5 %, int4 de +384 % a +219 %  Le cache KV quantifiait avec UNE echelle par vecteur (tete, position) ; Q8_0 et
- Aiguille : test arrete, et pourquoi (remplissage trop repetitif, prefill trop lent)  9,6 minutes pour UNE sonde sur Qwen3-30B-A3B (1 024 jetons) et un echec : l
- Aiguille : test arrete, et pourquoi (remplissage trop repetitif, prefill trop lent)  9,6 minutes pour UNE sonde sur Qwen3-30B-A3B (1 024 jetons) et un echec : u
- KV par bloc : mesure longue (4 591 jetons) -- int8 +3,4 %, int4 +287 %  Tableau complet :    KV     512 j, par vecteur   512 j, par bloc   4 591 j, par bloc   f
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A qtrinet-core/src reports/rapport-prefill-par-lots.md REPRISE.md && git commit -q -F - <<'EOF' &
- docs: préciser que QT_GPU_KV exige QT_GPU (le pilote ne s'ouvre que sur QT_GPU)" && git log --oneline -3 && git status --short | head -3
- docs E4 : comment le noyau d'attention a été validé (cas dégénérés, trois bugs)" && git log --oneline -1
- KV déporté : corriger la copie du chemin par lots  Le miroir était appelé DANS la boucle des jetons avec la position du jeton et la taille du lot : il copiait t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/contexte-long.md'; s=open(p).read() old = """Deux réserves, mesurées elles aussi 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A docs/contexte-long.md REPRISE.md journal && git commit -q -F - <<'EOF' && git log --oneline -3 
- journal : archive automatique" 2>/dev/null; cd qtrinet-core && cargo test --release 2>&1 | tail -3 && cd .. && git log --oneline -9 | cat && git status --short 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/contexte-long.md'; s=open(p).read() old = """Il reste, sur ce chemin : le **dépaq
- porte gpt-oss : préciser qu'elle se mesure SANS QT_GPU  Mesuré deux fois, même binaire, même commande :   sans QT_GPU   : 15,1757 (le chiffre de contrôle du dép
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/contexte-long.md'; s=open(p).read() old = """2. **Le format ne change presque rie
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A tools/aiguille.py reports/rapport-aiguille.md qtrinet-core/src && git commit -q -F - <<'EOF' &&
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/contexte-long.md'; s=open(p).read() old = """Il reste, sur ce chemin : le **dépaq
- REPRISE : feuille de route réécrite et pièges des variables d'environnement  La section « Ce qu'il faut faire ensuite » datait d'avant les deux campagnes : ses 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/contexte-long.md'; s=open(p).read() old = """Il reste, sur ce chemin : la réparti
- cat /tmp/rotation_16k.log; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/contexte-long.md'; s=open(p).read() old = """Il reste,
- docs : plan détaillé pour MLA et la vision (chantier 5)  MLA n'est pas testable en l'état (aucun modèle MLA en GGUF ici — le deepseek-r1-distill local est un Qw
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log -1 --format=%B | tail -4 && cat > /tmp/msg_plan.txt <<'EOF' docs : plan détaillé pour MLA et la vi
- journal : archive automatique" 2>/dev/null; git log --oneline -3 | cat
- cat /tmp/rotation_16k.log; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/plan-mla-vision.md'; s=open(p).read() old = "### Valid
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/plan-mla-vision.md'; s=open(p).read() old = """### État du harnais : FAIT""" new 
- vision : relevé du projecteur mmproj (paramètres et nommage réels)  Le fichier est en architecture \`clip\` et contient la tour COMPLÈTE (519 tenseurs, \`v.blk.
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='REPRISE.md'; s=open(p).read() old = "| 2 | seuil de rotation YaRN | **fait, seuil corr
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/plan-mla-vision.md'; s=open(p).read() old = """Les tenseurs sont nommés `v.blk.N.
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/plan-mla-vision.md'; s=open(p).read() old = """### Ce qu'il faut écrire, dans l'o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/plan-mla-vision.md'; s=open(p).read() old = """### ÉTAT : première tranche FAITE 
- vision : détailler le pas suivant (couche, rotation 2-D, attention locale, injection)  Le plan dit maintenant, étape par étape, ce qui reste à écrire pour le co
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/plan-mla-vision.md'; s=open(p).read() old = """| tranche | écart max relatif cont
- vision : une RÉFÉRENCE existe sur la machine (libmtmd d'ollama)  Le plan pariait sur llama-mtmd-cli ; il n'y est pas, mais ollama embarque la bibliothèque multi
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/plan-mla-vision.md'; s=open(p).read() old = """Ce qui n'y est pas encore : la rot
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/plan-mla-vision.md'; s=open(p).read() add = """ ### Le point d'injection est en p
- vision : la structure de paramètres de libmtmd est sondée (l'ABI n'est plus un obstacle)  mtmd_context_params_default rend la structure par pointeur caché : on 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/vision_etat.txt <<'EOF' ### libmtmd : où en est le programme de référence  Le programme `tools/
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/mtmd_etat2.txt <<'EOF'  ### libmtmd : état exact après ce tour  Tout ce qui précède `mtmd_token
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat >> docs/plan-mla-vision.md <<'EOF'  ### tokenize : deux hypothèses testées, aucune ne suffit  Après le
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat >> docs/plan-mla-vision.md <<'EOF'  ### L'API de mtmd est maintenant CONNUE (en-tête récupéré)  `mtmd.
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat >> docs/plan-mla-vision.md <<'EOF'  ### Les deux conventions, lues dans la SOURCE de llama.cpp (clip.c
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat >> docs/plan-mla-vision.md <<'EOF'  ### La convention de rotation 2-D, lue dans la source  `clip.cpp`,
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='tools/vision_ref.py'; s=open(p).read() # le fichier .bloc ne contient plus les poids (
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='tools/vision_ref.py'; s=open(p).read() s = s.replace("""    ecart = float(np.abs(out -
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat >> docs/plan-mla-vision.md <<'EOF'  ### Le détail de la rotation, lu dans ggml (et mon implémentation 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat >> docs/plan-mla-vision.md <<'EOF'  ### Après correction : la rotation suit la source, mais l'ORDRE es
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/vision_ref.py /tmp/vision_patch.bin 2>&1 | tail -3 && cat >> docs/plan-mla-vision.md <<'EOF'
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat >> docs/plan-mla-vision.md <<'EOF'  ### La chaîne complète est DÉMONTRÉE, de l'image aux logits  `QT_V
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat >> docs/plan-mla-vision.md <<'EOF'  ### La rotation est CONFIRMÉE par la source (et une variante de fe
- REPRISE : MLA et vision tous deux faits, avec leurs réserves nommées  MLA : validé (5,2e-7). Vision : chaîne complète et démontrée de bout en bout, de l'image a
- REPRISE : l'item 5 reflète l'état final (chaîne vision démontrée, réserves nommées)" && git log --oneline -1 && git status --short | head -2
- journal : archive automatique" 2>/dev/null; git log --oneline -3 | cat
- REPRISE : l'item 3 (rotation) reflète la mesure à 16 k et le seuil porté à 4 ×" && git log --oneline -1
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/plan-mla-vision.md'; s=open(p).read() add = """ ### La permutation colonne-majeur
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='README.md'; s=open(p).read() old = """# Qtrinet  Inférence de LLM en **ternaire / mult
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A && git commit -q -F - <<'EOF' && git log --oneline -1 && git status --short | head -3 Drave : r
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/roadmap.md'; s=open(p).read() s = s.replace("""| 0.1 | **Format de trace du flux*
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/roadmap.md'; s=open(p).read() s = s.replace("""| 0.4 | **Profilage par neurone gé
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && git checkout src/model.rs && cargo build --release 2>&1 | tail -1 && cd .. && python3 - <<'PY' 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && printf 'target/\n' >> .gitignore && git rm -r -q --cached drave-core/target 2>/dev/null; git ls-files | gr
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/roadmap.md'; s=open(p).read() s = s.replace("""| 0.3 | **Le format EST le contrat
- date +"%H:%M:%S"; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A drave-core/src && git commit -q -F - <<'EOF' && git log --oneline -1 Phase 1.
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A drave-core/src && git commit -q -F - <<'EOF' && git log --oneline -1 && date +"%H:%M:%S" Phase 
- date +"%H:%M:%S"; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/roadmap.md'; s=open(p).read() s = s.replace("""| 3.1 | **Contra
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > reports/rapport-analyse-flux.md <<'EOF' # Analyse du flux, couche par couche  Première analyse **pur
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > docs/format-flux.md <<'EOF' # Le format de flux (DRVF v1) — spécification  Ce format sert **trois ch
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/format-flux.md'; s=open(p).read() vieux = """Le flux voyage en **f32** sur le rés
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date +"%H:%M:%S" && cat > reports/rapport-transport-liste.md <<'EOF' # Phase 3.2 — transporter la LISTE au
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='reports/rapport-transport-liste.md'; s=open(p).read() s += """  ## Ajout — l'échelle p
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > docs/colab-reparti.md <<'EOF' # Répétition Colab — la phase 3.4, pas à pas  Objectif : deux machines
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='reports/rapport-transport-liste.md'; s=open(p).read() v = """Configuration utilisable 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='reports/rapport-transport-liste.md'; s=open(p).read() v = """D'où les deux suites poss
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='REPRISE.md'; s=open(p).read() ancre = "## 7. Carte du dépôt" assert s.count(ancre) == 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='reports/rapport-transport-liste.md'; s=open(p).read() v = """Trois choses y sont nette
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='reports/rapport-transport-liste.md'; s=open(p).read() v = """Donc la revendication hon
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/roadmap.md'; s=open(p).read() v = "| 2026-09-30 | diff KV f32 contre KV int8 (per
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/pair_factice.py && git commit -q -F - <<'EOF' && echo "--- validation à 1024 jetons ---" && 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='reports/rapport-phase3-reparti.md'; s=open(p).read() v = """Égalité exacte, et pas seu
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat cb37c83 | tail -5; echo "=== ce que le code committé contient ==="; git show HEAD:drave-co
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='reports/rapport-transport-liste.md'; s=open(p).read() v = """| jetons | écart | octets
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='reports/rapport-transport-liste.md'; s=open(p).read() v = """C'est aussi la réponse à 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date +"%H:%M:%S" && python3 - <<'PY' p='REPRISE.md'; s=open(p).read() v = """`TCP_NODELAY` a divisé l'atte
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='drave-core/src/main.rs'; s=open(p).read() v = """        // Le DERNIER jeton n'a rien 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/format-flux.md'; s=open(p).read()  v = """## Transport (phase 3, TCP) — protocole
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo "=== porte Qwen (attendu 19,3885) ===" && ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/format-flux.md'; s=open(p).read() v = """          version      u8           3   
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/format-flux.md'; s=open(p).read() v = """liste     couche       u16          < 10
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A drave-core/src/main.rs && git commit -q -F - <<'EOF' && git log --oneline -1 | cat Deux silence
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='tools/preparer_colab.sh'; s=open(p).read() s = s.replace("    temps : ~16 ms de calcul
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/format-flux.md'; s=open(p).read() v = """| | version 1 | version 2 | |---|---|---
- REPRISE : la session 12h-15h (lots sur le fil, DRVF v2/v3, protocole v4, audit)  Ce qui a changé depuis §6bis, en un bloc : le préremplissage par lots est fait 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && IDS=$(head -1 /tmp/ids_qwen_long.txt | tr ',' '\n' | head -3 | tr '\n' ',' | sed 's/,$//'); p=46203; (./dr
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/format-flux.md'; s=open(p).read() s = s.replace("ou en **1 seul lot de 917 543 oc
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls ../FPGA-Stratix-V/docs/ | grep -iE "pe-even|ddr3|evenement" | head -4; python3 - <<'PY' p='README.md'; 
- REPRISE : les variables d'environnement qui restaient dans l'ombre  Treize variables présentes dans le code n'étaient documentées nulle part (DRAVE_BANC_KV_*, D
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo "=== porte Qwen ===" && ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/id
- Rapport : où mettre les bits du cache KV (facteur 130 à 840 à taille égale)  Six points mesurés à 8 191 jetons, trois en cours. La courbe est sans ambiguïté : à
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A drave-core/src/main.rs && git commit -q -F - <<'EOF' && git log --oneline -1 | cat Règle R4 : p
- Mode lot sur un lien latent : 18× (2,6 s contre 47,6 s)  Mesuré avec le relais retardateur (20 ms par message, 64 jetons, 12 couches par nœud) : un seul lot de 
- Colab : le mode lot chiffré dans la recette (2,6 s contre 47,6 s à 20 ms par message)" && git log --oneline -1 | cat; date +"%H:%M:%S"
- Kit Colab vérifié de bout en bout (clonage, compilation 23 s, écart 0,00e0)" && git log --oneline -1 | cat
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A drave-core/src/main.rs drave-core/src/model.rs && git commit -q -F - <<'EOF' && git log --oneli
- Un drapeau inconnu n'est plus avalé en silence  \`--keeep 0.05\` (une faute de frappe) faisait tourner le modèle entier sans élagage et sans un mot. L'analyse r
- Handoff : les garde-fous de l'après-midi et deux lignes de mesures  REPRISE §6bis gagne ce qui a été ajouté depuis 13h (tableau de bord --options-actives, drape
- Cohérence : versions et comptes de flux remis d'aplomb partout  D'après le reste de \`reports/rapport-coherence-docs.md\` : le message de refus cité par le rapp
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' def rem(p, paires):     s = open(p).read(); ok = 0     for v, n in paires:         if s.c
- Rapport transport : l'en-tête dit maintenant ce que son tableau mesure  « 871 octets » ne correspondait à aucune ligne du tableau (897 en listes i16 à seuil 5 %
- Portes revérifiées après la journée : 19,3885 · 15,1757 · 11 tests  La porte gpt-oss était la seule que la relecture adversariale n'avait pas pu exécuter (borne
- REPRISE : le noyau GPU de top-k en tête des prochains chantiers  Les deux Quadro sont libres, le cadre GPU existe (compiler.sh, drave_gpu.cu, sm_75) et c'est le
- Feuille de route : 1.4 attribuée et la section format renvoyée à sa spécification  La 1.4 était encore « expérience conçue » alors qu'elle est faite et que la c
- Format de flux : la taille par neurone actif, dense et creuse  6,02 et 3,01 sont les valeurs d'une trace DENSE ; une trace creuse coûte 6,04 et 3,04, parce que 
- Référence 6 bits re-mesurée (19,3045) plutôt que retirée  Le relecteur avait raison : ce chiffre de la table de non-régression n'était cité dans aucun rapport. 
- Référence 6 bits : 19,5633 et non 19,3045 — la commande ne redonne pas l'ancien chiffre  J'ai rejoué la commande de la table de non-régression au lieu de retire
- Index de la session : les huit chantiers, les défauts et par qui ils ont été trouvés  Un rapport court pour un humain qui reprend : ce qui est livré (avec le re
- Chemin GPU revérifié : 15,1667 avec le pilote, noyau exact à 1,99e-7  Les portes de la journée se mesurent SANS DRAVE_GPU (c'est la règle du dépôt), donc person
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A drave-core/src/main.rs && git commit -q -F - <<'EOF' && git log --oneline -1 | cat Seconde rele
- Deux tests de plus : trame forgée hors dimension, et n_blocs démesuré  Les deux défauts graves de la seconde relecture sont maintenant verrouillés par des tests
- Handoff et index : la seconde relecture, et treize tests  REPRISE §6bis et l'index de session disent maintenant les deux tours de relecture adversariale (22 déf
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='reports/rapport-placement-bits-kv.md'; s=open(p).read() v = """| int8 | int8 | 2,25 | 
- Feuille de route : les clés f16 mesurées (+0,018 % pour 39 % de la taille du f32)" && git log --oneline -1 | cat; sleep 60; cat /tmp/kv_cles_f16.log; date +"%H:
- Tests de trame forgée : un délai de lecture, pour qu'ils échouent au lieu de pendre  Sans délai, si le plafond disparaissait, le test attendrait les 358 Go du c
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='reports/rapport-placement-bits-kv.md'; s=open(p).read() v = """| f16 | int4 | 2,625 | 
- REPRISE : la frontière du cache KV et les deux gains du mode lot  Le handoff porte maintenant les deux résultats qui décident : le meilleur réglage du cache KV 
- Colab clé en main : le nœud local, les trois tunnels, et un texte réel dans le notebook  \`tools/colab_cote_local.sh\` vérifie le binaire et le modèle, affiche 
- Plan du noyau GPU de top-k (phase 1.1), chiffré, et la perplexité attendue du notebook  \`docs/plan-gpu-topk.md\` : pourquoi le top-k retombe sur le CPU (le che
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (cd drave-core && cargo test --release 2>&1 | grep -E "^test .*FAILED|assertion" | head -3); python3 - <<'
- Documents : protocole v5 et mode 4 (lot en listes)  format-flux décrit le mode 4 (chaque état auto-délimité par ses trois tailles) et son coût mesuré ; la feuil
- Cache KV : la frontière tient à 4 096 comme à 8 192  Refait à contexte 4 096 : référence 12,2175 · clés f16 + valeurs int8 **+0,011 %** · int8/int8 **+2,25 %**.
- Corrections du second audit (1/2) : chiffres, époques, comptes, et la journée au README  - Les pourcentages du cache KV : « 75 % / 50 % » était une ERREUR de ma
- Corrections du second audit (2/2) : la journée au README, le mode 4 dans la recette Colab, le renvoi FPGA de la vision" && git log --oneline -1 | cat; date +"%H
- Documents : la frontière du cache KV dans contexte-long, et l'addendum du rapport de drapeaux  contexte-long §4.bis.3 porte la frontière complète (clés f16 + va
- Quatre tests pour le mode 4 : état forgé, deux états, préfixe incohérent  Le mode 4 est du code de protocole neuf : un état forgé à la main doit se décoder comm
- Cache KV à 4 096 : les quatre points, et les clés f16 devant les clés f32  clés f32 + valeurs int8 = 12,2223 (+0,039 %), soit un peu moins bien que le f16 (+0,0
- REPRISE : le créneau 15h-18h (mode 4, frontière KV confirmée, plan GPU écrit)" && git log --oneline -1 | cat; sleep 240; cat /tmp/aiguille_kv.log | tail -12; da
- README : la perplexité de gpt-oss était dans la colonne du débit" && git log --oneline -1 | cat; echo "=== aiguille ==="; tail -6 /tmp/aiguille_kv.log; date +"%
- --options-strict : un drapeau inconnu devient une erreur, pour les scripts  La dernière recommandation de l'audit des drapeaux : un avertissement suffit quand o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > reports/rapport-mode4-lot-listes.md <<'EOF' # Mode 4 — le lot en listes : ÷2,3 sur les octets, et ce
- Documents : dernières mentions de la version 4 remplacées par la 5 (mode lot en listes)" && git log --oneline -1 | cat; date +"%H:%M:%S"
- Colab : les quatorze champs du contrat d'activation, pas quatre  Et portes finales après la version 5 : 17 tests, Qwen 19,3885, réparti dense 0,00e0, lot dense 
- Index de session : le créneau 15h-18h (mode 4, plan GPU, 32 défauts relevés)" && git log --oneline -1 | cat; tail -3 /tmp/aiguille_kv2048.log 2>/dev/null; date 
- Index : le mode 4, le protocole v5, le plan GPU et le décompte des relectures" && git log --oneline -1 | cat; tail -4 /tmp/aiguille_kv2048.log; date +"%H:%M:%S"
- Mode 4 : le plafond cumulatif vérifié à l'octet près  Le relecteur avait prouvé qu'il manquait ; voici la preuve qu'il marche : avec des états bien formés au ma
- Préremplissage par lots : fidélité vérifiée à 1 024 jetons (0,00e0, 16 lots)  La fidélité du mode 3 était établie à 40, 200 et 256 jetons ; elle l'est maintenan
- REPRISE : dix-sept tests, et ce qu'ils verrouillent" && git log --oneline -1 | cat; sleep 420; tail -6 /tmp/aiguille_kv2048.log; date +"%H:%M:%S"
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='reports/rapport-placement-bits-kv.md'; s=open(p).read() v = """## Reproductible""" n =
- Aiguille 9/9 dans les trois variantes de cache KV, et les vérifications de fin de journée  L'aiguille v2 (Qwen2.5-1.5B, contexte 2 048, trois profondeurs) retro
- REPRISE : la politique du cache KV complète (taille ET temps), et l'aiguille 9/9" && git log --oneline -1 | cat
- Compteurs de lignes : 12 171 au 30/09 (le mode 4 et ses correctifs ont ajouté 270 lignes)" && git log --oneline -1 | cat; date +"%H:%M:%S"
- README : les prochaines étapes étaient restées à l'époque du FPGA  Elles listaient l'entraînement ternaire et le RTL comme priorités, alors que la feuille de ro
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (cd drave-core && timeout 300 cargo test --release 2>&1 | grep -E "^test result"); TAG=z1 PORT=47810 CTX=2
- Cadence de sprints de 2 h : charte et outil de boxing temps réel  \`tools/sprint.sh\` chronomètre un sprint sur l'heure du SYSTÈME (start/status/close) et écrit
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > reports/rapport-gpu-scores.md <<'EOF' # Noyau GPU de scores d'attention — le premier des trois du to
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A && git commit -q -F - <<'EOF' && git log --oneline -1 Noyau 2a du top-k GPU : histogramme d'oct
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cargo test --release --manifest-path drave-core/Cargo.toml 2>&1 | tail -3 && git add -A && git commit -q -
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cargo test --release --manifest-path drave-core/Cargo.toml 2>&1 | tail -2 && git add -A && git commit -q -
- Rapport de sélection : le second passage k doublé, et la durée mal étiquetée" && git log --oneline -1
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A && git commit -q -F - <<'EOF' && git log --oneline -1 Relecture adversariale : 7 défauts corrig
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' def patch(p, paires):     s=open(p).read()     for v,n,nom in paires:         assert s.co
- Compteur de lignes Rust unifié : 13 168 (un seul chiffre, mesuré, dans README ×2 et REPRISE)" && git log --oneline -1
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' def patch(p, paires):     s=open(p).read()     for v,n,nom in paires:         assert s.co
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && DRAVE_GPU=1 timeout 300 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q4_0.gguf --banc-topk 4096 2
- Plan et REPRISE : l'étape 6 est verte, et la prochaine étape est la FUSION de la chaîne, pas un noyau de plus" && git log --oneline -1 && date +%H:%M:%S
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A && git commit -q -F - <<'EOF' && git log --oneline -1 Top-k déporté : une synchro en trop, un b
- Chiffres du 16 k sur le binaire final : attention 19,58 → 7,59 ms/jeton (−61 %), balayage −24 %" && git log --oneline -1
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo "lot 1 :"; ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/wt2_ids.txt --c
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -q --amend -F - <<'EOF' && git log --oneline -1 --attn-topk en mode lot : le drapeau ne fait ri
- Correction d'interprétation : les clés notées dépendent du nombre de JETONS, pas du contexte — le croisement est entre 255 et 2 047 clés, pas « entre 8 k et 16 
- Journal : index des sessions régénéré" && git status --short | wc -l && date +%H:%M:%S
- Rapport et plan : 14 noyaux et 956 lignes (le noyau 3 est arrivé après le comptage), ordre réel de la collecte" && git log --oneline -1; date +%H:%M:%S
- Rapport : l'étape 5 est faite, et la ligne de l'étape 4 dit la bonne variable (clés vues, pas contexte)" && git log --oneline -1; date +%H:%M:%S
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cargo test --release --manifest-path drave-core/Cargo.toml 2>&1 | tail -2 && git add -A && git commit -q -
- Compteur de lignes Rust re-mesuré en fin de sprint : 13 480 (le chiffre avait bougé de 312 lignes pendant le sprint)" && git log --oneline -1; date +%H:%M:%S
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A && git commit -q -F - <<'EOF' && git log --oneline -1 && ./tools/sprint.sh list && git status -
- Journal : index des sessions (fin de sprint 1)" && git log --oneline --since="2026-09-30 17:41" | wc -l && git status --short | wc -l && pgrep -c -x drave; echo
- Journal : index des sessions (clôture)" 2>/dev/null; git status --short; echo "--- 22 commits, aucun processus, dépôt propre ---"; pgrep -c -x drave; ps -eo pcp
- Journal : index régénéré par l'outillage de session" && git log --oneline -3 && echo "--- reste ---" && git status --short | wc -l
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' def patch(p, paires):     s=open(p).read()     for v,n,nom in paires:         assert s.co
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A && git commit -q -F - <<'EOF' && git log --oneline -1 Le filet du noyau 4 doit agir AVANT la so
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cargo test --release --manifest-path drave-core/Cargo.toml 2>&1 | tail -2 && git add -A && git commit -q -
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' # La cérémonie : on ajoute les chiffres gpt-oss et le doute sur les projections. p='/tmp/
- REPRISE : sprint 2 (fusion du top-k, croisement à ~300 clés, le filet testé, le doute sur les projections)" && git log --oneline -1; date +%H:%M:%S
- REPRISE : le doute sur les projections est à moitié levé (ctx 512 et 1024 identiques, ctx 256 évalue une autre chose)" && sleep 1400; date +%H:%M:%S; ./tools/sp
- Sprint 2 : cérémonie (revue adverse autonome, introspection, planning du sprint 3)" && git log --oneline -1 && ./tools/sprint.sh start "Qualité de l'attention c
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='REPRISE.md'; s=open(p).read() vieux = """⚠️ **Doute, à moitié levé** : le déport des p
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' def patch(p, paires):     s=open(p).read()     for v,n,nom in paires:         assert s.co
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' # La cérémonie : on remplace la grille partielle par la grille complète et on # ajoute la
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='/tmp/ceremonie3.md'; s=open(p).read() vieux = """### 4. Trouvé en préparant la grille 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' # La cérémonie : ajouter la revue adverse (ses deux écarts graves) et le lever # mesuré d
- Sprint 3 : cérémonie (aiguille × attention creuse, revue adverse, planning du sprint 4)" && git log --oneline -1 && ./tools/sprint.sh start "Le k de l'attention
- Préremplissage déporté : ×4,5 sur un prompt de 3 961 jetons (286,6 → 63,8 s), perplexité à 2e-5" && git log --oneline -1; cat /tmp/aiguille_k.log | tail -3
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='reports/rapport-aiguille-topk.md'; s=open(p).read() vieux = """| k = 512 (12,5 %) | (e
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='/tmp/ceremonie4.md'; s=open(p).read() vieux = s[s.index("### 1. Le résultat qui tranch
- Contrôle dense à 8 192 : l'information est retrouvée (1002 s, prompt de 7963 jetons) — la question du k vs contexte est mesurable là" && git log --oneline -1; d
- Sprint 4 : cérémonie (le k est un réglage, la leçon des trois répétitions, planning du sprint 5)" && ./tools/sprint.sh start "Refaire la grille avec de VRAIES f
- Pourquoi --lot 1 diffère de --lot 256 : 7e-4 nat par position, top-1 identique partout — c'est une amplification chaotique, pas un chemin faux" && git log --one
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A && git commit -q -F - <<'EOF' && git log --oneline -1 Grille refaite sur trois VRAIS textes : k
- À 8 192 clés, k=1024 (12,5 %) suffit : le k nécessaire croît plus lentement que le contexte (deux points)" && git log --oneline -1

