# Session f2f82297 — Dépôt /home/stephane/GitHub/Qtrinet, s

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `f2f82297-793b-4538-952f-cb8da809229c` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 12:03 |
| Durée | 0.6 h |
| Tours | 1 |
| Messages | 97 |
| Appels d'outils | 106 |
| Fichiers touchés | 2 |
| Commandes | 72 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Dépôt /home/stephane/GitHub/Qtrinet, sprint autonome 24 h. Sous-agent A10 : mesurer M1 (codec typé) sur le corpus **multilingue** déjà présent, sans modifier les modules existants.  État : - `tools/cerveau/hub.py` M1 : 528/528 sur les surfaces réelles avec contexte, 70,8 % sans contexte, canonique 100 %, invariance 100 %. - Corpus : `jeux/corpus.py`, `jeux/corpus_multilingue.py`, `semantique/typed … [1564 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Dépôt /home/stephane/GitHub/Qtrinet, sprint autonome 24 h. Sous-agent A10 : mesurer M1 (codec typé) sur le corpus **mult … [1844 caractères tronqués]

*106 appels d'outils.* Actions notables :

- bash — List repo structure and key directories
- bash — Show git status and recent commits
- bash — Find corpus modules and list src
- bash — Find references to multilingual corpus modules
- bash — Show sizes of key modules and tests
- bash — Outline hub.py
- read
- bash — Search B5/B7 references in Python code
- bash — List jeux modules and inspect multilingual lexicon
- bash — Inspect codecs package interface
- bash — Inspect codec base contract
- bash — Read rest of multilingual lexicon module
- bash — Compute corpus and lexicon statistics
- bash — Inspect test style and init
- … et 79 autres

**Synthèse produite :**

⏵ Closing with the summary, results, and file paths

Travail terminé. J’ai créé uniquement les deux fichiers demandés, sans toucher aux modules, docs, reports, journal, `batterie.py` ni à git en écriture.

\## Fichiers

- Code : [`tools/cerveau/multilingue.py`](/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py)
- Tests : [`tools/cerveau/tests/test_multilingue.py`](/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_multilingue.py)
- Rapport : [`/tmp/a10-multilingue.md`](/tmp/a10-multilingue.md)
- JSON : [`/tmp/a10-multilingue.json`](/tmp/a10-multilingue.json)

\## Résumé mesuré

Périmètre : 528 coups B5+B7, 66 langues réelles, 30 paires.

| mesure | valeur |
|---|---|
| exact avec contexte | **528 / 528 (100 %)** |
| exact sans contexte | **374 / 528 (70,8 %)** |
| canonique | **528 / 528 (100 %)** |
| invariance interlangues, contexte | **15 / 15 (100 %)** |
| invariance interlangues, sans contexte | **14 / 15 (93,3 %)** |
| invariance toutes variantes, contexte | **26 / 26 (100 %)** |
| invariance toutes variantes, sans contexte | **21 / 26 (80,8 %)** |

**B7 seul** (449 surfaces, 66 langues, 11 paires) : 449/449 avec contexte, 331/449 sans (73,7 %), canonique 449/449, invariance interlangues **11/11 dans les deux conditions**. L’unique échec global sans contexte est B5 `echecs-nf3` (`Cf3`, SAN français court qui exige la position) — B7 reste donc à 100 %.

**Baseline surface** (code majoritaire des autres surfaces de la paire, leave-one-out) : 514/514 avec contexte, 369/514 (71,8 %) sans, contre M1 368/514 (71,6 %) sur le même périmètre : **+1 item seulement**, avec −4,8 pt sur le morpion et +2,8 pt sur les échecs.

**Contrôle surface permutée stricte** : 369 items appariés, exact attendu **0/369**, exact donneur **332/369 (90,0 %)** ; B7 **298/300 (99,3 %)** ; variante large 518 items, donneur 423/518 (81,7 %).

**Invariance ≠ exactitude** : sans contexte, les paires B7 go (62 langues) et morpion (42 langues) restent invariantes avec un code faux (exact 0 %).

\## Langues

71 langues au lexique, **66 présentes** dans le corpus ; absentes déclarées : **ky, lo, mt, si, yo**. Cinq langues à n=1 : am, km, pa, so, zu.

\## Tests

- `PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools` → **123 tests OK, 19 skip**.
- Mon module seul : **20 tests OK en 3,3 s**.

\## Limites (dans le rapport)

Corpus construit par le code (attendus et contextes issus des mêmes règles que le codec), couche lexicale seulement, pas d’intervalle de 
… [417 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py` | 1 | 12 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_multilingue.py` | 3 | 1 |

### Commandes exécutées (échantillon)

- **T1** List repo structure and key directories
- **T1** Show git status and recent commits
- **T1** Find corpus modules and list src
- **T1** Find references to multilingual corpus modules
- **T1** Show sizes of key modules and tests
- **T1** Outline hub.py
- **T1** Search B5/B7 references in Python code
- **T1** List jeux modules and inspect multilingual lexicon
- **T1** Inspect codecs package interface
- **T1** Inspect codec base contract
- **T1** Read rest of multilingual lexicon module
- **T1** Compute corpus and lexicon statistics
- **T1** Inspect test style and init
- **T1** Run existing M1 battery measurement
- **T1** Inspect typed universals module
- **T1** Search prior baseline and permutation definitions
- **T1** List reports and M1 references
- **T1** Search M1 multilingual findings in report
- **T1** Inspect jeux-mesures JSON structure
- **T1** Inspect corpus and invariance sections
- **T1** Inspect universaux measurements JSON
- **T1** Compute per-language exact and detection rates
- **T1** Inspect pair invariance and language coverage
- **T1** Inspect pair invariance sorted safely
- **T1** Compute language coverage in B7
- **T1** Prototype invariance and leave-one-out baseline
- **T1** Compute cross-language invariance counts
- **T1** Search for A10 or multilingue module references
- **T1** Inspect sprint docs for measurement conventions
- **T1** Count items without pair
- **T1** Prototype strict and broad surface permutations
- **T1** Break down permutation control by source and game
- **T1** Inspect B7-specific pair invariance
- **T1** Inspect go no-context code
- **T1** Baseline per game without context
- **T1** Inspect B5 pair variants without context
- **T1** Show current date and Python version
- **T1** Check expected code consistency within pairs
- **T1** Inspect codec factory and lit contract
- **T1** Compute B7-only M1 metrics
- … et 32 autres

## 4. Mesures et résultats marquants

- **T1** `08a9cf18 B13 — CHAÎNE M1→M5→M6→M8 : 528/528, M5 CONTEXTE 18,7 % VS 12,6 %, M6 94,3 %, M8 57,95 (BORNE HAUTE)`
- **T1** `tools/semantique/hybride.py:4:Le codec classique lit les surfaces de jeux à 100 % sur B5/B7. On mesure ici`
- **T1** `reports/rapport-hc-permutation.md:89:  négligeables, 99 % de la masse), et ils forment une **permutation** ; la`
- **T1** `reports/rapport-portes-p0-p9.md:23:| **P1** — hyper-connexions | `hc_attn_pre` concorde à **1e-7** (arrondi f32), quatre positions (`reports/rapport-v4-couches-0-1.md`) | **TENUE le 03/10 (bloc 27)** `
- **T1** `reports/alignement-verne.md:5:**Verdict** : **VALIDE** — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent `
- **T1** `reports/alignement-verne.md:132:| chapitres permutés #1 | 26,3 % | 0,3 % | 0,2 % |`
- **T1** `reports/alignement-verne.md:133:| chapitres permutés #2 | 23,9 % | 0,5 % | 0,3 % |`
- **T1** `reports/alignement-verne.md:134:| chapitres permutés #3 | 25,8 % | 0,2 % | 0,0 % |`
- **T1** `reports/alignement-verne.md:140:**Hasard pur, phrase contre phrase dans le même chapitre** : 38 400 tirages, **15,62 %** de rencontres d'ancres. C'est un plancher **phrase contre phrase** — conservate`
- **T1** `reports/alignement-verne.md:174:4. **Le contrôle négatif « chapitres permutés » n'est pas un hasard parfait** : les chapitres voisins partagent des personnages, et l'anglais d'un chapitre peut conteni`
- **T1** `reports/alignement-verne.md:183:**VALIDE** — les ancres distinctives se retrouvent à 93,2 % à ±2, contre 0,3 % quand les chapitres sont permutés (×272) ; les 37 chapitres se correspondent par leur con`
- **T1** `reports/alignement-verne.md:190:- ✓ **contrôle négatif (chapitres permutés)** : 0,3 % à ±2 (seuil 10,0 %)`
- **T1** `reports/07/p3.md:457:| — contrôle (une permutation **différente** par langue) | **0,00 %** | — |`
- **T1** `reports/07/p3.md:466:  (permutation différente par langue ✓) donne **0,00 %** ✓✓. *Le signal existe, il est ténu* ✓✓ ;`
- **T1** `reports/07/p3.md:554:| — contrôle (permutation différente par langue) | **0,90 %** | 3,3 % |`
- **T1** `reports/07/p4.md:481:permutés ✓✗ — **×272,5** ; la matrice chapitres × chapitres place le bon chapitre en **n° 1 pour 37/37** ✓✓. Les`
- **T1** `reports/rapport-jeux-symboliques.md:70:| **étiquettes mélangées** : attendus permutés | **7 / 112** (6,25 %) | le comparateur ne valide pas au hasard |`
- **T1** `63:1. **M1** est un **hub de lecture fiable** : 528/528 avec contexte, 100 % en canonique et en invariance.`
- **T1** `/controles list len 4 ['split par paire sans fuite', 'majoritaire 0 %', 'base gelée 0 %']`
- **T1** `/lecture = codec 100 % ; natif normalisé 55,7/37,0 ; suffixe 59,8/40,7 ; vecteur contexte 59,1/40,7 ; préfixe 0,4/88,9 (collapse) ;`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:11534:- Plateau multilingue à l'échelle : 10 langues, 4 écritures, pic à 42 % de la profondeur  tools/plateau_multilingue.py étend in`
- **T1** `docs/modules-cerveau-langage.md:40:| **M8 sommeil** | prototypes par (jeu, action), test **non stocké** | **96,48 %** sur 106 épisodes non stockés ; baseline épisodique **0 %** | ✅ **généralise** |`
- **T1** `docs/roadmap.md:360:| B12.8 | **M8 sommeil** | ❌ **marginal** | 96,48 % de champs mais exact **65,1 %**, baseline par jeu **96,10 %** ; leave-one-code-out exact **0 % par construction**, non nuls 63,5`
- **T1** `docs/en-cours.md:56:- **B12 les modules cerveau-langage** — **corrigé** : M1 **528/528** solide ; M2 `aug-formes` **de 95,2 %, inédit 13/20, chemin 88,1 %, 6/14** ; `aug-pos` **vers 95,4 %, 13,3/20** `
- **T1** `A10 — M1 multilingue : 528 items, exact ctx 100,0 %, sans ctx 70,8 %, invariance interlangues 100,0 %`
- **T1** `- **Avec contexte** : M1 lit **528 / 528 (100,0 %)** et le canonique revient à **528 / 528 (100,0 %)**.`
- **T1** `- **Sans contexte** : **374 / 528 (70,8 %)** ; c'est là que se voient les dépendances au contexte (go, morpion, notations courtes).`
- **T1** `- **Invariance interlangues** : **15 / 15 (100,0 %)** des paires avec contexte et **14 / 15** sans contexte. Les variantes de langue d'une même paire donnent bien le même code.`
- **T1** `- **Baseline surface** : 369 / 514 (71,8 %) sans contexte, contre 368 / 514 (71,6 %) pour M1 sur le même périmètre.`
- **T1** `- **Contrôle surface permutée** : exact attendu **0 / 369 (0,0 %)**, exact donneur **332 / 369 (90,0 %)** avec contexte (B7 : **298 / 300 (99,3 %)**). La lecture suit la surface, pas l'étiquette de pa`
- **T1** `| exact avec contexte | 528 / 528 (100,0 %) |`
- **T1** `| exact sans contexte | 374 / 528 (70,8 %) |`
- **T1** `| canonique | 528 / 528 (100,0 %) |`
- **T1** `| invariance interlangues (ctx, 15 paires) | 15 / 15 (100,0 %) |`
- **T1** `| invariance interlangues (sans ctx, 15 paires) | 14 / 15 (93,3 %) |`
- **T1** `| invariance toutes variantes (ctx, 26 paires) | 26 / 26 (100,0 %) |`
- **T1** `| invariance toutes variantes (sans ctx, 26 paires) | 21 / 26 (80,8 %) |`
- **T1** `| baseline surface (ctx, 514 items) | 514 / 514 (100,0 %) |`
- **T1** `| baseline surface (sans ctx, 514 items) | 369 / 514 (71,8 %) |`
- **T1** `| M1 sans contexte, même périmètre que la baseline | 368 / 514 (71,6 %) |`
- **T1** `| exact attendu (ctx) | 0 / 369 (0,0 %) |`
- **T1** `| exact donneur (ctx) | 332 / 369 (90,0 %) |`
- **T1** `| exact attendu (sans ctx) | 0 / 369 (0,0 %) |`
- **T1** `| exact donneur (sans ctx) | 313 / 369 (84,8 %) |`
- **T1** `| exact donneur B7 (ctx) | 298 / 300 (99,3 %) |`
- **T1** `| exact donneur, variante large (ctx) | 423 / 518 (81,7 %) |`
- **T1** `| morpion | 64 | 42 | 100,0 % | 7,8 % | 100,0 % | 1 / 1 (100,0 %) | 1 / 1 (100,0 %) | 2 / 4 (50,0 %) |`
- **T1** `| echecs | 146 | 62 | 100,0 % | 94,5 % | 100,0 % | 4 / 4 (100,0 %) | 3 / 4 (75,0 %) | 4 / 7 (57,1 %) |`
- **T1** `| dames | 70 | 56 | 100,0 % | 100,0 % | 100,0 % | 1 / 1 (100,0 %) | 1 / 1 (100,0 %) | 4 / 4 (100,0 %) |`
- **T1** `| go | 87 | 62 | 100,0 % | 0,0 % | 100,0 % | 2 / 2 (100,0 %) | 2 / 2 (100,0 %) | 4 / 4 (100,0 %) |`
- **T1** `| cartes | 161 | 36 | 100,0 % | 100,0 % | 100,0 % | 7 / 7 (100,0 %) | 7 / 7 (100,0 %) | 7 / 7 (100,0 %) |`
- **T1** `| cartes-carte-a | cartes | 4 | 2 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |`
- **T1** `| cartes-carte-b | cartes | 4 | 2 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |`
- **T1** `| echecs-e4 | echecs | 7 | 2 | 1 | 2 | oui | oui | 100,0 % | 71,4 % |`
- **T1** `| echecs-nf3 | echecs | 6 | 2 | 1 | 2 | oui | non | 100,0 % | 66,7 % |`
- **T1** `| ml-cartes-10h | cartes | 36 | 36 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |`
- **T1** `| ml-cartes-ah | cartes | 30 | 30 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |`
- **T1** `| ml-cartes-jc | cartes | 30 | 30 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |`
- **T1** `| ml-cartes-ks | cartes | 29 | 29 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |`
- **T1** `| ml-cartes-qd | cartes | 28 | 28 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |`
- **T1** `| ml-dames-b6c5 | dames | 56 | 56 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |`
- **T1** `| ml-echecs-e4 | echecs | 61 | 61 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |`
- **T1** `| ml-echecs-nf3 | echecs | 61 | 61 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |`
- **T1** `| ml-go-d4 | go | 62 | 62 | 1 | 1 | oui | oui | 100,0 % | 0,0 % |`
- **T1** `| ml-go-passe | go | 14 | 14 | 1 | 1 | oui | oui | 100,0 % | 0,0 % |`
- **T1** `| ml-morpion-a1 | morpion | 42 | 42 | 1 | 1 | oui | oui | 100,0 % | 0,0 % |`
- **T1** `| morpion | 62 | 8,1 % | 3,2 % | −4,84 pt | 21 | 0,0 % | 71,4 % |`
- **T1** `| echecs | 141 | 96,5 % | 99,3 % | +2,84 pt | 140 | 0,0 % | 91,4 % |`
- **T1** `| dames | 66 | 100,0 % | 100,0 % | +0,00 pt | 13 | 0,0 % | 15,4 % |`
- **T1** `| go | 84 | 0,0 % | 0,0 % | +0,00 pt | 37 | 0,0 % | 100,0 % |`
- **T1** `| cartes | 161 | 100,0 % | 100,0 % | +0,00 pt | 158 | 0,0 % | 94,9 % |`
- **T1** `- n par langue de 1 à 55 ; 5 langue(s) à n=1 (am, km, pa, so, zu) : un taux de 0 ou 100 % sur un seul item n'est pas une estimation.`
- **T1** `- Invariance n'est pas exactitude : sans contexte, les paires go et morpion restent souvent invariantes (même code pour toutes les langues) alors que le code est faux (go : 0,0 %, morpion : 7,8 % d'ex`
- **T1** `- Contrôle permuté strict : exact_attendu = 0,0 % par construction (le donneur a un code attendu différent) ; le signal utile est exact_donateur = 90,0 % (B7 : 99,3 %).`
- **T1** `69-| morpion | 64 | 42 | 100,0 % | 7,8 % | 100,0 % | 1 / 1 (100,0 %) | 1 / 1 (100,0 %) | 2 / 4 (50,0 %) |`
- **T1** `70-| echecs | 146 | 62 | 100,0 % | 94,5 % | 100,0 % | 4 / 4 (100,0 %) | 3 / 4 (75,0 %) | 4 / 7 (57,1 %) |`
- **T1** `71-| dames | 70 | 56 | 100,0 % | 100,0 % | 100,0 % | 1 / 1 (100,0 %) | 1 / 1 (100,0 %) | 4 / 4 (100,0 %) |`
- **T1** `72-| go | 87 | 62 | 100,0 % | 0,0 % | 100,0 % | 2 / 2 (100,0 %) | 2 / 2 (100,0 %) | 4 / 4 (100,0 %) |`
- **T1** `73-| cartes | 161 | 36 | 100,0 % | 100,0 % | 100,0 % | 7 / 7 (100,0 %) | 7 / 7 (100,0 %) | 7 / 7 (100,0 %) |`
- **T1** `f"100 % sur un seul item n'est pas une estimation.")`
- **T1** `- **Sans contexte** : **374 / 528 (70,8 %)** ; c'est là que se voient les dépendances au contexte (go, morpion, notations courtes). Sur B7 seul : 331 / 449 (73,7 %).`
- **T1** `- **Invariance interlangues** : **15 / 15 (100,0 %)** des paires avec contexte et **14 / 15** sans contexte. **Sur B7 seul : 11 / 11 (100,0 %) avec contexte et 11 / 11 (100,0 %) sans contexte. L'uniqu`
- **T1** `| B5 | 79 | 2 | 19 | 100,0 % | 54,4 % | 100,0 % | 4 / 4 (100,0 %) | 3 / 4 (75,0 %) |`
- **T1** `| B7 | 449 | 66 | 11 | 100,0 % | 73,7 % | 100,0 % | 11 / 11 (100,0 %) | 11 / 11 (100,0 %) |`
- **T1** `| fr | 55 | 9c 9d 8e 8g 21m | 100,0 % | 54,5 % | 100,0 % | 100,0 % / 93,3 % (15) | 28 / 55 (50,9 %) |`
- **T1** `| notation | 31 | 2c 6d 16e 5g 2m | 100,0 % | 54,8 % | 100,0 % | — | 14 / 17 (82,4 %) |`
- **T1** `| en | 15 | 7c 1d 4e 2g 1m | 100,0 % | 80,0 % | 100,0 % | 100,0 % / 93,3 % (15) | 12 / 15 (80,0 %) |`
- **T1** `| de | 11 | 5c 1d 2e 2g 1m | 100,0 % | 72,7 % | 100,0 % | 100,0 % / 100,0 % (11) | 8 / 11 (72,7 %) |`
- **T1** `| es | 11 | 5c 1d 2e 2g 1m | 100,0 % | 72,7 % | 100,0 % | 100,0 % / 100,0 % (11) | 8 / 11 (72,7 %) |`
- **T1** `| it | 11 | 5c 1d 2e 2g 1m | 100,0 % | 72,7 % | 100,0 % | 100,0 % / 100,0 % (11) | 8 / 11 (72,7 %) |`
- **T1** `| ja | 11 | 5c 1d 2e 2g 1m | 100,0 % | 72,7 % | 100,0 % | 100,0 % / 100,0 % (11) | 8 / 11 (72,7 %) |`
- **T1** `| nl | 11 | 5c 1d 2e 2g 1m | 100,0 % | 72,7 % | 100,0 % | 100,0 % / 100,0 % (11) | 8 / 11 (72,7 %) |`
- **T1** `| pl | 11 | 5c 1d 2e 2g 1m | 100,0 % | 72,7 % | 100,0 % | 100,0 % / 100,0 % (11) | 8 / 11 (72,7 %) |`
- **T1** `| pt | 11 | 5c 1d 2e 2g 1m | 100,0 % | 72,7 % | 100,0 % | 100,0 % / 100,0 % (11) | 8 / 11 (72,7 %) |`
- **T1** `| ru | 11 | 5c 1d 2e 2g 1m | 100,0 % | 72,7 % | 100,0 % | 100,0 % / 100,0 % (11) | 8 / 11 (72,7 %) |`
- **T1** `| zh | 11 | 5c 1d 2e 2g 1m | 100,0 % | 72,7 % | 100,0 % | 100,0 % / 100,0 % (11) | 8 / 11 (72,7 %) |`
- **T1** `| cs | 10 | 5c 1d 2e 1g 1m | 100,0 % | 80,0 % | 100,0 % | 100,0 % / 100,0 % (10) | 8 / 10 (80,0 %) |`
- **T1** `| da | 10 | 5c 1d 2e 1g 1m | 100,0 % | 80,0 % | 100,0 % | 100,0 % / 100,0 % (10) | 8 / 10 (80,0 %) |`
- **T1** `| eo | 10 | 5c 1d 2e 1g 1m | 100,0 % | 80,0 % | 100,0 % | 100,0 % / 100,0 % (10) | 8 / 10 (80,0 %) |`
- **T1** `| et | 10 | 5c 1d 2e 1g 1m | 100,0 % | 80,0 % | 100,0 % | 100,0 % / 100,0 % (10) | 8 / 10 (80,0 %) |`
- **T1** `| fa | 10 | 5c 1d 2e 1g 1m | 100,0 % | 80,0 % | 100,0 % | 100,0 % / 100,0 % (10) | 8 / 10 (80,0 %) |`
- **T1** `| fi | 10 | 5c 1d 2e 1g 1m | 100,0 % | 80,0 % | 100,0 % | 100,0 % / 100,0 % (10) | 8 / 10 (80,0 %) |`
- **T1** `| hu | 10 | 5c 1d 2e 1g 1m | 100,0 % | 80,0 % | 100,0 % | 100,0 % / 100,0 % (10) | 8 / 10 (80,0 %) |`
- **T1** `| nb | 10 | 5c 1d 2e 1g 1m | 100,0 % | 80,0 % | 100,0 % | 100,0 % / 100,0 % (10) | 8 / 10 (80,0 %) |`
- **T1** `| sl | 10 | 5c 1d 2e 1g 1m | 100,0 % | 80,0 % | 100,0 % | 100,0 % / 100,0 % (10) | 8 / 10 (80,0 %) |`
- **T1** `| sr | 10 | 5c 1d 2e 1g 1m | 100,0 % | 80,0 % | 100,0 % | 100,0 % / 100,0 % (10) | 8 / 10 (80,0 %) |`
- **T1** `| sv | 10 | 5c 1d 2e 1g 1m | 100,0 % | 80,0 % | 100,0 % | 100,0 % / 100,0 % (10) | 8 / 10 (80,0 %) |`
- **T1** `| uk | 10 | 5c 1d 2e 1g 1m | 100,0 % | 80,0 % | 100,0 % | 100,0 % / 100,0 % (10) | 8 / 10 (80,0 %) |`
- **T1** `| vi | 10 | 5c 1d 2e 1g 1m | 100,0 % | 80,0 % | 100,0 % | 100,0 % / 100,0 % (10) | 8 / 10 (80,0 %) |`
- **T1** `| sq | 9 | 5c 1d 2e 1g | 100,0 % | 88,9 % | 100,0 % | 100,0 % / 100,0 % (9) | 8 / 9 (88,9 %) |`
- **T1** `| af | 8 | 5c 2e 1g | 100,0 % | 87,5 % | 100,0 % | 100,0 % / 100,0 % (8) | 7 / 8 (87,5 %) |`
- **T1** `| ar | 8 | 2c 1d 2e 2g 1m | 100,0 % | 62,5 % | 100,0 % | 100,0 % / 100,0 % (8) | 5 / 8 (62,5 %) |`
- **T1** `| be | 8 | 3c 1d 2e 1g 1m | 100,0 % | 75,0 % | 100,0 % | 100,0 % / 100,0 % (8) | 6 / 8 (75,0 %) |`
- **T1** `| bn | 8 | 5c 2e 1g | 100,0 % | 87,5 % | 100,0 % | 100,0 % / 100,0 % (8) | 7 / 8 (87,5 %) |`
- **T1** `| ca | 8 | 3c 1d 2e 1g 1m | 100,0 % | 75,0 % | 100,0 % | 100,0 % / 100,0 % (8) | 6 / 8 (75,0 %) |`
- **T1** `| eu | 8 | 3c 1d 2e 1g 1m | 100,0 % | 75,0 % | 100,0 % | 100,0 % / 100,0 % (8) | 6 / 8 (75,0 %) |`
- **T1** `| lv | 7 | 2c 1d 2e 1g 1m | 100,0 % | 71,4 % | 100,0 % | 100,0 % / 100,0 % (7) | 5 / 7 (71,4 %) |`
- **T1** `| tr | 7 | 1c 1d 2e 2g 1m | 100,0 % | 57,1 % | 100,0 % | 100,0 % / 100,0 % (7) | 4 / 7 (57,1 %) |`
- **T1** `| el | 6 | 2c 1d 2e 1g | 100,0 % | 83,3 % | 100,0 % | 100,0 % / 100,0 % (6) | 5 / 6 (83,3 %) |`
- **T1** `| ko | 6 | 1d 2e 2g 1m | 100,0 % | 50,0 % | 100,0 % | 100,0 % / 100,0 % (6) | 3 / 6 (50,0 %) |`
- … (tronqué)

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 15, in <module> TypeError: '<' not supported between instances of 'NoneType' and 'str' [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", line 1051, in <module>     raise SystemExit(main())                  

