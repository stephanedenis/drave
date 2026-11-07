# Session session- — Rapport convention GV et règles candidates

> **Journaux :** [le jour](../../2026-11-07/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-e1ad947b-50b1-4758-a921-5267225bf642` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-07 12:41 |
| Durée | 1.5 h |
| Tours | 1 |
| Messages | 214 |
| Appels d'outils | 245 |
| Fichiers touchés | 9 |
| Commandes | 192 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J1.2 : la convention des GV (322 FP / 180 FN). Classe les erreurs, mesure 2 règles candidates (arrêt à l'adverbe final, sujet hors du GV) sur dev/test, garde celles qui font monter le F1 sans perdre d'attachement, fiche `reports/rapport-convention-gv.md` + JSON, commit. Règles : S/D/N2 intouchés ; 183/183.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J1.2 : la convention des GV (322 FP / 180 FN). Classe les erreurs, mesure 2 règles candidates (arrêt à l'adverbe f … [193 caractères tronqués]

*245 appels d'outils.* Actions notables :

- bash — List repository root
- bash — Show git status and recent commits
- bash — Find J1.2 references
- bash — List reports and tools
- bash — Find GV convention docs
- bash — List head reports and GV-related
- bash — Inspect chantier plan json
- bash — Find J1 tasks in docs
- bash — Find 322 FP 180 FN source
- bash — Read verbe-gv report and JSON
- bash — Read semaine-autonome doc
- bash — Read r035 report
- bash — Find FP FN reports
- bash — List linguistique tests and find numbers
- … et 200 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py` | 0 | 13 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-convention-gv.md` | 1 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/test_bloc_linguistique.py` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-07/mesures.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** List repository root
- **T1** Show git status and recent commits
- **T1** Find J1.2 references
- **T1** List reports and tools
- **T1** Find GV convention docs
- **T1** List head reports and GV-related
- **T1** Inspect chantier plan json
- **T1** Find J1 tasks in docs
- **T1** Find 322 FP 180 FN source
- **T1** Read verbe-gv report and JSON
- **T1** Read semaine-autonome doc
- **T1** Read r035 report
- **T1** Find FP FN reports
- **T1** List linguistique tests and find numbers
- **T1** Grep 322 in reports and session
- **T1** Find F1 0.7549 source
- **T1** Read digest around 1400-1480
- **T1** Read digest around 1600-1720
- **T1** Check /tmp/seg remnants
- **T1** Read evaluer_gold.py
- **T1** Read variantes.py
- **T1** Read classer and croisements scripts
- **T1** Locate GV logic in bloc_linguistique
- **T1** Read chunker GV section
- **T1** Read gate and autotest constants
- **T1** Read rest of evaluer_gold
- **T1** Read autotest attachment tests
- **T1** Classify GV errors on current base
- **T1** Debug classer run
- **T1** Run classer with absolute path
- **T1** Read analyser start
- **T1** Find S segmenter
- **T1** Read S segmenter and fusion
- **T1** Inspect S generator segments
- **T1** Inspect S segment attributes
- **T1** Print raw S output
- **T1** Inspect S segments more
- **T1** Find F1 assertions in autotest
- **T1** Read measure.py
- **T1** Inspect gold segments and targets
- … et 152 autres

## 4. Mesures et résultats marquants

- **T1** `./data/corpus_wiki_fr/train.txt:1276195:Băița de sub Codru (Mosóbánya en hongrois, Washwerk en allemand) est une commune roumaine du județ de Maramureș, dans la région historique de Transylvanie et da`
- **T1** `./data/corpus_wiki_fr/train.txt:1400497:Une naine blanche à pulsations est une étoile naine blanche à la luminosité variable du fait de pulsations dues à des ondes de gravité non radiales dans sa part`
- **T1** `./data/corpus_wiki_fr/train.txt:1462683:Urlați est une ville roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La ville de Urlaț`
- **T1** `./data/corpus_wiki_fr/train.txt:1470199:Păulești est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La commune de`
- **T1** `./data/corpus_wiki_fr/train.txt:1474893:Colceag est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La commune de `
- **T1** `./data/corpus_wiki_fr/train.txt:1475061:Gornet-Cricov est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La commu`
- **T1** `./data/corpus_wiki_fr/train.txt:1475449:Sângeru est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La commune de `
- **T1** `./data/corpus_wiki_fr/train.txt:1475855:Iordăcheanu est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La commune`
- **T1** `./data/corpus_wiki_fr/train.txt:1478109:Gura Vadului est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La commun`
- **T1** `./data/corpus_wiki_fr/train.txt:1478151:Călugăreni est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La commune `
- **T1** `./data/corpus_wiki_fr/train.txt:1479835:Tătaru est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La commune de T`
- **T1** `./data/corpus_wiki_fr/train.txt:1480065:Boldești-Gradiștea est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La `
- **T1** `./data/corpus_wiki_fr/train.txt:1481251:Sălciile est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La commune de`
- **T1** `./data/corpus_wiki_fr/train.txt:1485315:Dumbrăvești est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La commune`
- **T1** `./data/corpus_wiki_fr/train.txt:1487555:Brebu est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La commune rouma`
- **T1** `./data/corpus_wiki_fr/train.txt:1487585:Valea Doftanei est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La comm`
- **T1** `./data/corpus_wiki_fr/train.txt:1495369:Bălțești est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La commune de`
- **T1** `./data/corpus_wiki_fr/train.txt:1497661:Ceptura est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La commune de `
- **T1** `./data/corpus_wiki_fr/train.txt:1499147:Izvoarele est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La commune d`
- **T1** `./data/corpus_wiki_fr/train.txt:1499485:Plopu est une commune roumaine du județ de Prahova, dans la région historique de Valachie et dans la région de développement du Sud. Géographie La commune de Pl`
- **T1** `./data/corpus_wiki_fr/train.txt:1994965:(abréviation informelle ), ou , est un quasar situé dans la constellation du Lion à une distance de voyage de la lumière d'environ d'années-lumière du Système s`
- **T1** `docs/pilotage/roadmap.md:178:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** +`
- **T1** `| **exact** | 14 (0,0586) | **23 (0,0962)** | **+9 (×1,6)** |`
- **T1** `(R² 0,30) — la surface capte l'époque ; tout test de style contrôle la date, tout test de famille`
- **T1** `| 2 | **atomes V14 ↔ niveaux** (44 œuvres × 14 flottants, JSON pur) | table + 20 exemples mesurés | permuter les colonnes doit tuer le prédictif | signature lexicale : contrôler la date |`
- **T1** `reports/rapport-consolidation-structure-partagee.md:54:| **A + B** (somme) | **6,8845 (−7,3 %)** | 17,3228 (+1,2 %) |`
- **T1** `reports/rapport-corpus-pdf.md:5:> **322,5 Mo**, **39 506 tronçons** — **8 Ko à zéro** entre les splits, **0 / 40** sur les trois`
- **T1** `reports/rapport-corpus-pdf.md:78:- `data/corpus_pdf/` — le corpus (322,5 Mo, gitignoré).`
- **T1** `reports/rapport-corpus-wiki-texte.md:92:| ar | 1 000 310 | 1,994 G | 322 M | 3,57 Go | 28,9 % | **0** | XNLI 0/40 | 1/161/0 |`
- **T1** `reports/rapport-parcimonie-entrainee.md:87:| 100 % | 0,311 ms | 0,916 ms | 1,322 ms |`
- **T1** `reports/rapport-pensee-relation.md:19:| **groupe nominal** (sans rôle) | **322** | 50,6 % |`
- **T1** `reports/rapport-pensee-roles.md:17:| GN sans rôle | **322** | 100 % |`
- **T1** `./docs/pilotage/roadmap.md:38:**État au 07/11 12 h 34.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7549**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **``
- **T1** `./docs/pilotage/en-cours.md:66:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7549**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **contrat v1** va`
- **T1** `| `porte-c4-retard.sh` | 29 s | PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne |`
- **T1** `| `porte-coupe.sh` | 131 s | ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit pour  |`
- **T1** `| `porte-delais.sh` | 21 s | ✅ le temps, lui, augmente : 6.77 s → 9.67 s (+2.9 s ≈ 50 ms × 64 pas) |`
- **T1** `| `porte-homeostasie.sh` | 495 s | ✅ porte tenue (×0 exact · activité monotone · dominance reproduite) |`
- **T1** `| `porte-jeux.sh` | 104 s | ✅ la porte des jeux tient : 100 % au niveau 4, 33/33 paires invariantes, 0 collision, |`
- **T1** `| `porte-mistral.sh` | 8 s | ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= plancher  |`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 te`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7549**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **contrat v1** validé ; frontières, partition, G`
- **T1** `- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (`
- **T1** `| **R — le lecteur** | **R0.7** | R4.4 close ; **R0.7 — bloc linguistique** ; R2/R3 attendent N5/N4 | **1 024 octets entraînés** ; **2 048** fini (2×10 000 pas) ; la restitution |`
- **T1** `**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035` fait**, reste `g017` ; **S** — poursuivre la validation ; **N4** — consigne ;`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `38:**État au 07/11 12 h 34.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7549**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) rég`
- **T1** `178:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes`
- **T1** `253:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tranché (la tête du GN arrête `
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 07/11 12 h 34.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7549**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) réglé `
- **T1** `| 00:16 | `26c7b7ab` | ROADMAP ET JOURNAL — LA NUIT FINIT À F1 0,7535, POS 86,25 %, 236/237, COUVERTURE 0,9916 ; LA CONVENTION DU SUJET |`
- **T1** `**La nuit du 07/11 (00 h 00 → 01 h 10).** Le bloc finit la nuit à **POS 86,25 %**, **F1 0,7535**`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir 0,2276 |`
- **T1** `| [rapport-consolidation-c7.md](rapport-consolidation-c7.md) | C7 — la consolidation : le rejeu met bien l'expérience dans les poids (−16,4 % en domaine, **+1,3 % hors domaine**) |`
- **T1** `| [rapport-consolidation-structure-partagee.md](rapport-consolidation-structure-partagee.md) | Ce qui se consolide, c'est la STRUCTURE PARTAGÉE — même mémorisation (−22,5 %), transfert −7,4 % ou +1,2 `
- **T1** `| [rapport-r13.3-anglais.md](rapport-r13.3-anglais.md) | R13.3 — anglais 100 Mo : le BPE perd encore à octets égaux |`
- **T1** `-- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7549**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **contrat v1** validé ; frontières, partition, `
- **T1** `+- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors du GV `
- **T1** `-**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035` fait**, reste `g017` ; **S** — poursuivre la validation ; **N4** — consigne `
- **T1** `+**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035` et convention des GV faits**, reste `g017` (J1.3/J1.4) ; **S** — poursuivre `
- **T1** `-**État au 07/11 12 h 34.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7549**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) réglé`
- **T1** `+**État au 07/11 13 h 30.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) réglé`
- **T1** `[still running after 600000ms; moved to background job bash-189]`

## 5. Erreurs rencontrées

8 sorties en erreur ou divergentes. Les premières :

- **T1** : (no output) [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 24, in <module> TypeError: _est_verbe() takes 1 positional argument but 2 were given [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 5, in <module> KeyError: 'source' [exit code: 1]
- **T1** : écrit base écrit gv_adverbe écrit gv_sujet écrit gv_deux écrit gv_adverbe_large écrit placebo_adverbe placebo_sujet: motif 0 fois : '                if (n0e in _suj or nom_propre) and sv:' FAIL placeb
- **T1** : 25a6c0ff B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183 d7469b5c INDEX — RÉGÉNÉRÉ APRÈS L'INVENTAIRE PANINI (702 FICHES) ; ÉTAT HORODATÉ 34fdd4ef DOCS — README T1 TENU (
- **T1** : #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS # (`--attn-window` en r
- **T1** : (no output) [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 11, in <module>   File "/usr/lib64/python3.13/json/__init__.py", line 181, in dump     for chunk in iterable:                  ^^^^^^

## 6. Commits

- B13 — LA CONVENTION DES GV : SUJET HORS DU GV + ADVERBE FINAL, F1 0,7549 → 0,7902, ATTACHEMENT 237/238 ; 183/183" 2>&1 | tail -30

