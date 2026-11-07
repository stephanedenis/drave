# Session 599e9c0e — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `599e9c0e-4252-43ca-a89a-3886d723c379` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 21:13 |
| Durée | 0.9 h |
| Tours | 1 |
| Messages | 54 |
| Appels d'outils | 93 |
| Fichiers touchés | 2 |
| Commandes | 68 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état de N2 et de sa porte** — lecture seule, aucun code.  Contexte : `docs/pilotage/roadmap.md` (chantier N2), `docs/pilotage/en-cours.md` (session N2), `reports/rapport-n2-*.md`, `tools/eval_n2_propre.py`, `tools/entrainer_native.py`, `tools/native_model.py`, `tools/porte-*.sh`. A23 a noté : « `tools/po … [1529 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état de N2 et de sa porte … [1809 caractères tronqués]

*93 appels d'outils.* Actions notables :

- bash — Afficher branche, derniers commits, racine
- glob
- read
- bash — Lister le répertoire models et tailles
- bash — Inventorier les checkpoints .pt dans work
- bash — Chercher N2 dans la roadmap
- bash — Chercher N2 dans en-cours
- bash — Trouver tous les checkpoints .pt du dépôt
- bash — Lister work/n2ac
- bash — Vérifier corpus propre et corpus annexes
- bash — Vérifier GPU et environnement python
- bash — Localiser le registre des portes
- bash — Chercher les usages de eval_n2_propre et porte-n2
- bash — Lire le registre des portes le plus récent
- … et 64 autres

**Synthèse produite :**

⏵ Rédaction de la fiche d'état N2 et du JSON

J'ai les mesures et les contrôles ; je rédige les deux livrables.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-n2.md` | 1 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-etat-n2.json` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Afficher branche, derniers commits, racine
- **T1** Lister le répertoire models et tailles
- **T1** Inventorier les checkpoints .pt dans work
- **T1** Chercher N2 dans la roadmap
- **T1** Chercher N2 dans en-cours
- **T1** Trouver tous les checkpoints .pt du dépôt
- **T1** Lister work/n2ac
- **T1** Vérifier corpus propre et corpus annexes
- **T1** Vérifier GPU et environnement python
- **T1** Localiser le registre des portes
- **T1** Chercher les usages de eval_n2_propre et porte-n2
- **T1** Lire le registre des portes le plus récent
- **T1** Lire mesures et chaîne de la porte propre
- **T1** Lire métadonnées des checkpoints récents et l'état git
- **T1** Lire la chaîne et le log du checkpoint récent
- **T1** Vérifier claims GPU et garde-fous
- **T1** Lire eval_longueurs.py
- **T1** Lire les sections N2 de roadmap et en-cours
- **T1** Inspecter NativeConfig/NativeModel
- **T1** Lire rope_model.py et vdc
- **T1** Inspecter la config et les clés du checkpoint récent
- **T1** Vérifier l'architecture utilisée par entrainer_rope.py
- **T1** Vérifier le corpus test temporaire et usages d'eval_n2_propre
- **T1** Lire la fiche N2 propre (référence)
- **T1** Lire le garde-fou GPU
- **T1** Lire la porte ressources
- **T1** Lire le mètre ppl et le corpus wiki
- **T1** Lire le mètre evalue_canal
- **T1** Test de chargement du checkpoint récent avec eval_n2_propre
- **T1** Évaluer le checkpoint récent avec eval_n2_propre.py
- **T1** Mesurer le checkpoint récent au mètre RoPE sur corpus propre
- **T1** Vérifier checkpoints absolus disponibles
- **T1** Traquer les chiffres de la fenêtre 1024
- **T1** Lire la fiche production fenêtre
- **T1** Chercher la note A23
- **T1** Reproduire la porte propre 2,7856 sur propre512-8k
- **T1** Contrôle eval_n2_propre sur un checkpoint absolu N2.h
- **T1** Tableau des métadonnées des checkpoints
- **T1** Inventaire des fiches N2 (titre, date, verdict)
- **T1** Mesurer la porte avec le mauvais mètre (absolu)
- … et 28 autres

## 4. Mesures et résultats marquants

- **T1** `36:| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art.,`
- **T1** `112:[N2] lasts 4 days and is 30% complete and is colored in #b26a00`
- **T1** `197:| **N2** | la distillation : corpus, professeur, [curriculum](../theorie/glossaire/entrees/curriculum.md) | 🔬 | **N2.h** — corpus dédupliqué (**0 %** de fuite) : la chaîne propre vaut **3,0904**, `
- **T1** `205:   jeu **contaminé à 32,8 %** — voir [N2.d](../../reports/rapport-n2-budget.md)) ; **N2.h3** montre que le`
- **T1** `96:- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propr`
- **T1** `131:**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+ ; **S** — poursuivre la validation ; **N4** — consigne ; **B10.3** — `z` ; **B13** `
- **T1** `137:- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `Quadro RTX 5000, 16384 MiB, 154 MiB, 2 %`
- **T1** `Quadro RTX 5000, 16384 MiB, 4 MiB, 0 %`
- **T1** `[still running after 60000ms; moved to background job bash-3915]`
- **T1** `"recette": "RoPE 34,3 M, lot 8, lr 3e-4, graine 1, init base-wiki-45m, 33 Mo vus par bras",`
- **T1** `"val et test disjoints (0 % de fuite, N2.h)",`
- **T1** `# Corpus : data/corpus_propre (train 3,24 Mo, val 180 Ko, 0 % de fuite — N2.h).`
- **T1** `# Deux bras à OCTETS ÉGAUX (33 Mo vus), init base-wiki-45m, canal :`
- **T1** `#   1. fenêtre 512, 8 000 pas × 8 × 512`
- **T1** `#   2. fenêtre 256 (seq 128), 32 000 pas × 8 × 128`
- **T1** `dans des chunks de 8192 octets, 8 lots × 16 fenêtres. On peut demander n'importe quelle`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `**100 scans simulés** : la photo passe de **55,9 %** à **6,7 %** de [WER](../theorie/glossaire/entrees/wer.md) (test **5,7 %**) et la`
- **T1** `**préservation** du lecteur atteint **90–97 %** sur **4 familles sur 5** (propre **96,7 %** ;`
- **T1** `fax **56,7 %**, la limite d'information) ; les **colonnes** tombent de **89,4 %** à **0,5 %**,`
- **T1** `les **tableaux** donnent **92,6 %** de cellules exactes, et **trois vrais scans** s'accordent à`
- **T1** `**7,10 %** et **88,4 %** de mots, l'**ordre des colonnes** prouvé (**15,3 %** contre **98,0 %**`
- **T1** `611 ms. La restitution depuis un document lu est **R31**.`
- **T1** `suivante, jamais l'attente. **N5 est gelé** jusqu'au verdict de R11 sur le contexte ; B10.3 attend un **z qui porte** : l'objectif mot a levé le décodeur (32,5 ; **26,7 sur JW, au-dessus du plancher 1`
- **T1** `[A1–A8] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[A8.0/A8.3a] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[A8.3b/c] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[A2.6] lasts 2 days and is 30% complete and is colored in #b26a00`
- **T1** `- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (`
- **T1** `| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** ; R2/R3 attendent N5/N4 | **1 024 octets entraînés** ; **2 048** fini (2×10 000 pas) ; la restitution |`
- **T1** `**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+ ; **S** — poursuivre la validation ; **N4** — consigne ; **B10.3** — `z` ; **B13** — 17`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `> (**32,8 %** des fenêtres de validation étaient verbatim dans l'entraînement) ; dédupliqué, il`
- **T1** `> perd **22,2 %** de son texte et la contamination tombe à **zéro**. La chaîne refaite vaut`
- **T1** `| octets | 4 633 889 | **3 605 306** (−22,2 %) |`
- **T1** `| validation verbatim dans l'entraînement | **32,8 %** (42 / 128 fenêtres) | **0 / 2 814** |`
- **T1** `| fenêtres de validation partageant 64 octets avec l'entraînement | — | 2,3 % (résidu de formules) |`
- **T1** `| distillation | 20 000 pas × 16 × 128 = 41 Mo vus, lr 1e-4 puis 3e-5, **3 graines** |`
- **T1** `> à **octets ajoutés constants** (61,4 Mo, le budget de N2.ac), les trois fenêtres écrasent N2.ac`
- **T1** `> seulement). En poussant la fenêtre 1 024 à **30 000 pas (307 Mo)**, le modèle de production`
- **T1** `> atteint **2,9121** en domaine à 128 octets (60 000 pas, 552 Mo), **2,5276** à 1 000, **2,4761** à`
- **T1** `> à fenêtre 128 (200 k pas, 205 Mo) donne 3,1591 à 128 et **8,2262** à 1 000 : la fenêtre n'est pas`
- **T1** `(61,4 Mo, le budget même de N2.ac) affiner le modèle de production avec **RoPE et une fenêtre`
- **T1** `de 200 000 pas avec 60 % de son compute. Trois questions restaient :`
- **T1** `| `+ RoPE 512` | 512 | 15 000 | 61,4 Mo | `mix-60k` (N2.ac) |`
- **T1** `| `+ RoPE 1 024` | 1 024 | 7 500 | 61,4 Mo | `mix-60k` (N2.ac) |`
- **T1** `| **`+ RoPE 2 048`** | 2 048 | 3 750 | 61,4 Mo | `mix-60k` (N2.ac) |`
- **T1** `| **`30 000 pas`** | 1 024 | +22 500 | +184 Mo | `mix1024-7.5k` |`
- **T1** `| **`depuis zéro`** | 512 | 15 000 | 61,4 Mo | `init-figee` (aléatoire) |`
- **T1** `| **N2.ac** (témoin) | 61 Mo | 3,4902 | 3,5169 | 7,9201 | 12,4065 | 6,0283 | 8,3352 | 9,0525 |`
- **T1** `| 200 k × 128 (témoin) | 205 Mo | 3,1591 | 3,6577 | 8,2262 | 12,8723 | 5,6056 | 7,2770 | 8,0018 |`
- **T1** `| **+ RoPE 512** | 123 Mo | **3,1588** | **2,9096** | 2,8018 | 2,7607 | **5,5247** | **7,0507** | **7,9023** |`
- **T1** `| **+ RoPE 1 024** | 123 Mo | **3,1489** | 2,9103 | **2,7858** | **2,7342** | **5,5173** | 7,1904 | 7,9521 |`
- **T1** `| **+ RoPE 2 048** | 123 Mo | 3,1862 | 2,9325 | 2,7980 | 2,7372 | 5,5485 | 7,2908 | 8,0135 |`
- **T1** `| **1 024, 30 000 pas** | **307 Mo** | **2,9943** | **2,7221** | **2,6143** | **2,5628** | **5,3122** | **6,5118** | **7,1544** |`
- **T1** `économe et sûre hors domaine ; 2 048 ne paie pas à 61,4 Mo.`
- **T1** `lp9qnz4jPO6DHumXX3daNRBjD0YJqv1OAJ3SqHZ2jK0M1zu3hx0cKBBUthjZl8s366ZzfjSXfsw97BhCAOEGJI4c79y54rehwrbXqvqiGfl5b4mx53sHpsKSbj+6MCu8PorXNdwKGJKiZdkBcoiK8/6CsqxWpyItjcHduqhEANAUF/AIJMovlXYzJVP9AWkt5ySp0BEr`
- **T1** `wd2pawMXcayjjw4GgTRJKrS6isYm3XmAg2TMvrxsrFZblAmnA0aFeh7xSoXCuMIMyZ5Xl+6WiXZAbVuwG9KFUxE0ul8kWbSUwLhi8iBH0kW/o/0e8miX7Qw5c6g0LVep2bOnWaEfT87YKb9BdA92R/CQIA0E0WrFu8PydFQ5aGm8nZI/atouUr8+GSMHnCgW0cyF7pcp`
- **T1** `# N2.n — La distillation anglaise : 4,42 → 3,94, la chaîne complète sur 204 Mo`
- **T1** `# N2.m — L'anglais seul : 4,42 sur 204 Mo, et ce que le multilingue coûte (1,6 PPL)`
- **T1** `# N2.l — Le canal de structure : +5 % de PPL, et le même alphabet`
- **T1** `date=2026-11-01 | sur les 186 Mo du corpus réel,`
- **T1** `# N2.j3 — La capacité sur 186 Mo : 21,65 M paie (4,39 → 4,20, et mieux partout)`
- **T1** `# N2.aa — Le corpus de 831 Mo à compute constant : un autre domaine, pas plus de savoir`
- **T1** `# N2.i — Le corpus élargi : 4,84 Mo uniques au lieu de 3,24`
- **T1** `# N2.j — Du vrai français : 186 Mo de Wikipédia, et ce que vaut le filtre « non ambigu »`
- **T1** `date=2026-11-01 | entraîné sur **186 Mo** de`
- **T1** `date=2026-11-02/03 | à **octets constants** (20,5 Mo vus), entraîner sur des`
- **T1** `# N2.j2 — Positions aléatoires sur 186 Mo : le verrou de longueur tombe encore (÷2,4 à 512)`
- **T1** `| 200 k × 128 | 205 Mo | 3,1591 | 3,6577 | 8,2262 | 12,8723 | 5,6056 | 7,2770 | 8,0018 |`
- **T1** `| **1 024, 30 k pas** | **307 Mo** | **2,9943** | **2,7221** | **2,6143** | **2,5628** | **5,3122** | **6,5118** | **7,1544** |`
- **T1** `La recette de production poussée une fois de plus (30 000 → **60 000 pas**, **552 Mo** au total) :`
- **T1** `| 7 500 | 122 Mo | 3,1489 | 2,9103 | 2,7858 | 2,7342 | 5,5173 | 7,1904 | 7,9521 |`
- **T1** `| 30 000 | 307 Mo | 2,9943 | 2,7221 | 2,6143 | 2,5628 | 5,3122 | 6,5118 | 7,1544 |`
- **T1** `| **60 000** | **552 Mo** | **2,9121** | **2,6341** | **2,5276** | **2,4761** | **5,1254** | **6,2043** | **6,7874** |`
- **T1** `**Chaque doublement des pas vaut ~−0,085 en domaine** (le pas de 7 500 à 30 000, ×4, valait`
- **T1** `−0,155 ; celui de 30 000 à 60 000, ×2, vaut −0,082) : c'est une loi **géométrique** en pas, et`
- **T1** `mieux, comme à toutes les tailles de la nuit. À 552 Mo vus, la PPL de queue est à **2,34** et la`
- **T1** `| T09 | N2 | La porte propre (0,29 manquant à 2,7856) : données ou capacité | reports/n2-*, work/n2ac/, tools/entrainer_native.py, GPU | recette N2 1 024 | aucun externe ; GPU libres (0 %) | python3 t`
- **T1** `POURQUOI. N2.d a mesuré que **32,8 %** des fenêtres du protocole de validation`
- **T1** `recopient (127 blocs contigus, jusqu'à 1,8 Ko). Toute PPL mesurée sur ce jeu est donc`
- **T1** `reports/rapport-n2-r12-2048.md:27:| fenêtre 256 | 128 | 20 000 | 20,5 Mo | `base-wiki-45m` |`
- **T1** `reports/rapport-n2-r12-2048.md:31:| **fenêtre 1 024, 20 k pas** | 1 024 | 20 000 | 164 Mo | `base-wiki-45m` (puis suite) |`
- **T1** `reports/rapport-n2-r12-2048.md:64:| fenêtre 256, 20 000 pas | 20,5 Mo | 3,3696 | 3,2892 | 3,2545 | 3,2459 | 3,2305 |`
- **T1** `reports/rapport-n2-r12-2048.md:65:| **fenêtre 1 024, 20 000 pas** | **164 Mo** | **2,9955** | **2,7201** | **2,6256** | **2,5757** | **2,5429** |`
- **T1** `reports/rapport-n2-r12-2048.md:70:(20 000 pas, fenêtre 256, **20,5 Mo**) contre celui-ci (20 000 pas, fenêtre 1 024, **164 Mo**) :`
- **T1** `reports/rapport-n2-r12-2048.md:163:| fenêtre 1 024, 20 000 pas | 164 Mo | **2,9955** | **2,7201** | **2,6256** | **2,5757** | **2,5429** |`
- **T1** `reports/rapport-n2-r12-2048.md:164:| **fenêtre 2 048, 20 000 pas** | **328 Mo** | **2,9121** | **2,6360** | **2,5375** | **2,4779** | **2,4383** |`
- **T1** `reports/rapport-n2-r12-2048.md:172:2. **À pas constants (20 000), 2 048 gagne** — 328 Mo contre 164 : **−0,083 à 128, −0,094 à 512,`
- **T1** `reports/rapport-n2-fenetre.md:30:| R1.1 | `data/wiki_fr` | 128 / 256 | 20 000 | 20,5 Mo | `base-wiki-45m` |`
- **T1** `reports/rapport-n2-fenetre.md:33:| R1.2-1 024 long | `data/wiki_fr` | 1 024 / 1 024 | 20 000 | 164 Mo | (suite du précédent) |`
- **T1** `donc le débit ne perd que **13 %** de 256 à 2 048. La fenêtre est presque gratuite à cette`
- **T1** `| fenêtre 1 024, 2 500 pas | 20,5 Mo | 3,3878 | 3,1098 | 2,9950 | 2,9449 | 2,9108 |`
- **T1** `| **fenêtre 2 048, 10 000 pas** | **164 Mo** | 3,0466 | 2,7581 | 2,6501 | 2,5914 | 2,5513 |`
- **T1** `| fenêtre 1 024, 20 000 pas | 164 Mo | **2,9955** | **2,7201** | **2,6256** | **2,5757** | **2,5429** |`
- **T1** `| **fenêtre 2 048, 20 000 pas** | **328 Mo** | **2,9121** | **2,6360** | **2,5375** | **2,4779** | **2,4383** |`
- **T1** `1. **À octets constants (164 Mo), 2 048 ne bat pas 1 024** — il est **derrière partout**`
- **T1** `2. **À pas constants (20 000), 2 048 gagne** — 328 Mo contre 164 : **−0,083 à 128, −0,094 à 512,`
- **T1** `**Synthèse de la loi de la fenêtre** (à 33 Mo pour les tailles, à 20,5 Mo pour la loi) : le saut`
- **T1** `bfd98892 DOC PRODUIT — RESYNCHRONISÉE : POS 85,00 %, F1 0,6482, ATTACHEMENT 235/236, GELÉ 85,32 / 0,6511 ; SORTIE D'EVALUER REJOUÉE`

