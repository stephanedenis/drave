# Session session- — Restitution v2 : rôles et fidélité

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-53896e61-4a68-417d-89e0-de0de156949b` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 04:53 |
| Durée | 1.0 h |
| Tours | 1 |
| Messages | 209 |
| Appels d'outils | 232 |
| Fichiers touchés | 4 |
| Commandes | 215 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche D2 : la restitution v2 — au-delà de la surface exacte (v0) et de la forme canonique (v1), restitue les **rôles** (agent, prédicat, lieu) dans une forme lisible et mesure la fidélité des rôles sur les 46 textes de la v0 ; fiche `reports/rapport-restitution-v2.md` + JSON, tests, commit. Si les rôles ne se restituent pas, écris le négatif.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche D2 : la restitution v2 — au-delà de la surface exacte (v0) et de la forme canonique (v1), restitue les **rôles** ( … [224 caractères tronqués]

*232 appels d'outils.* Actions notables :

- bash — Inspect workspace root and git state
- bash — List reports and data directories
- bash — Find restitution references in state and reports
- bash — Locate all restitution-related files
- bash — Read v0 restitution measurement script
- bash — Read v1 restitution measurement script
- bash — Read restitution module part 1
- bash — Read restitution module part 2
- bash — Read restitution module part 3
- bash — Find D2 task in planning docs
- bash — Read v1 report
- bash — Read v0 report
- bash — Read D2 plan entry context
- bash — Read current state file
- … et 202 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py` | 1 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_restitution_v2.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_restitution_v2.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v2.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Inspect workspace root and git state
- **T1** List reports and data directories
- **T1** Find restitution references in state and reports
- **T1** Locate all restitution-related files
- **T1** Read v0 restitution measurement script
- **T1** Read v1 restitution measurement script
- **T1** Read restitution module part 1
- **T1** Read restitution module part 2
- **T1** Read restitution module part 3
- **T1** Find D2 task in planning docs
- **T1** Read v1 report
- **T1** Read v0 report
- **T1** Read D2 plan entry context
- **T1** Read current state file
- **T1** Find role definitions in code
- **T1** Find agent role references in data and tests
- **T1** Read role measurement baseline
- **T1** Inspect structures corpus sources
- **T1** Find role gold reports and JSON
- **T1** Read role analyzer report
- **T1** Inspect structures gold data
- **T1** Inspect v0 bench structure
- **T1** List the 50 v0 texts
- **T1** Read role generation in linguistic block
- **T1** Find role gold for bench ids
- **T1** Search role agent in report JSONs
- **T1** Read thought role report and JSON
- **T1** Dump v1 roles per text
- **T1** List linguistic tests and gold files
- **T1** Search role gold in linguistic tests
- **T1** Read mirror method
- **T1** Read results method
- **T1** Check overlap between bench and role gold
- **T1** Show gold role annotations for matching texts
- **T1** Inspect heuristic init options
- **T1** Read annotation construction and views
- **T1** Read restitution tests
- **T1** Inspect CLI restituter
- **T1** Read CLI restitution and rest of tests
- **T1** Prototype first-role extraction
- … et 175 autres

## 4. Mesures et résultats marquants

- **T1** `docs/pilotage/en-cours.md:64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **re`
- **T1** `docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 c`
- **T1** `docs/pilotage/roadmap.md:38:**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL `
- **T1** `docs/pilotage/roadmap.md:188:   611 ms. La restitution depuis un document lu est **R31**.`
- **T1** `docs/pilotage/roadmap.md:307:| **N2** | la distillation : corpus, professeur, [curriculum](../theorie/glossaire/entrees/curriculum.md) | 🔬 | **N2.h** — corpus dédupliqué (**0 %** de fuite) : la chaîne`
- **T1** `"Les segments ne couvrent que 65,84 % des jetons et 75,19 % des caractères en "`
- **T1** `f"couverture {surface['couverture']:.2%}",`
- **T1** `f"couverture {mots['couverture']:.2%}",`
- **T1** `f"couverture {pos['couverture']:.2%}",`
- **T1** `> **65,84 % des jetons** et **75,19 % des caractères** ; stabilité structurelle`
- **T1** `**Lecture.** Les segments ne couvrent que **65,84 %** des jetons : le plancher lexical`
- **T1** `- **La complétude de la structure** : les segments ne couvrent que 65,84 % des jetons.`
- **T1** `86,5 % des groupes ambigus). Une autre préférence changerait le squelette et la`
- **T1** `fidélité    : exacte 1.0000 · caractères 1.0000 · couverture 100.00%`
- **T1** `mots        : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `pos         : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `de caractères (0,9286) dit, elle, que 93 % des caractères sont au bon endroit.`
- **T1** `(`evaluer` : POS 86,25 %, F1 79,02 %, attachement 237/238).`
- **T1** `"mandat": "Tâche B2 : les 14 atomes comme prédicteurs des 8 niveaux Drave — sur les 44 œuvres × 14 flottants (JSON plat, lecture seule chez Panini), mesure la prédiction d'un niveau (POS, syntagmes, a`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **5`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canoniq`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](../..`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `> de types 54/55** (98,2 %), les **rôles 131/131** (100 %), les **compléments 47/47**, et couvre`
- **T1** `> **1 466/1 475 octets** (99,4 % ; holdout **762/771**, 98,8 %). La **règle de contexte** corrige`
- **T1** `| `dev` | 7 | **7/7** | 229/229 (100 %) | **22/22** | **10/10** |`
- **T1** `| `test` | 16 | **16/16** | 475/475 (100 %) | **40/40** | **19/19** |`
- **T1** `| `holdout` | 32 | **31/32** | 762/771 (98,8 %) | **69/69** | **18/18** |`
- **T1** `| **global** | **55** | **54/55** (98,2 %) | **1 466/1 475** (99,4 %) | **131/131** (100 %) | **47/47** |`
- **T1** `[still running after 60000ms; moved to background job bash-25]`
- **T1** `| GN sans rôle | **322** | 100 % |`
- **T1** `| dont avec un GV | **301** | 93,5 % |`
- **T1** `| **avant le GV** (sujet probable) | **129** | 40,0 % |`
- **T1** `| **après le GV** (objet probable) | **172** | 53,4 % |`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `chunker le plus large **est** ce span (86,5 %) ; le S le plus large ne l'est que 25 fois sur 244.`
- **T1** `f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `/paragraphes`** (11 accepté`
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du`
- **T1** `**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (hasard`
- **T1** `devant, mais l'anglais est **100 % réel** quand le français ajoute **160 synthétiques** ; sur le`
- **T1** `| **R1.3** | **tokenisation** : octets ou BPE ; la décision est **mesurée**, pas doctrinale | ✅ **décidée : octets** (R13 close) | à octets égaux, français 2 graines BPE512 **+0,39 %** (bruit), BPE102`
- **T1** `| **R3.1** | **SFT de lecture** : réponse, résumé, extraction, refus ; jeux tenus à l'écart | ⏳ | **≥ 80 %** des instructions tenues à l'écart ; le contrôle 24/24 vus ne compte pas |`
- **T1** `| **R4.4** | **vision/OCR** : scans, figures, layout | 🔬 **mesuré sur scans simulés ; ouvert sur les scans réels** : 5 familles (photo **55,9 → 6,7 %** de WER, test **5,7 %**), **préservation 90–97 %*`
- **T1** `| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |`
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) | `en-cours.md`, `README.md`, `
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) | `en-cours.md`, `README.md`, `me`
- **T1** ``0,092` · `0,160` · `0,811` · `0,657` · `0,440` · `0,429` · `2,7856` · `40,0658` · `95,00 %` · `95,75 %``
- **T1** `64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 cano`
- **T1** `38:**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet`
- **T1** `[still running after 600000ms; moved to background job bash-111]`
- **T1** `- **T1** `docs/pilotage/en-cours.md:64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des G`
- **T1** `- **T1** `docs/pilotage/roadmap.md:38:**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` rég`
- **T1** `- **T1** `docs/pilotage/roadmap.md:188:   611 ms. La restitution depuis un document lu est **R31**.``
- **T1** `- **T1** `docs/pilotage/roadmap.md:307:| **N2** | la distillation : corpus, professeur, [curriculum](../theorie/glossaire/entrees/curriculum.md) | 🔬 | **N2.h** — corpus dédupliqué (**0 %** de fuite) :`
- **T1** `- **T1** `"Les segments ne couvrent que 65,84 % des jetons et 75,19 % des caractères en "``
- **T1** `- **T1** `f"couverture {surface['couverture']:.2%}",``
- **T1** `- **T1** `f"couverture {mots['couverture']:.2%}",``
- **T1** `- **T1** `f"couverture {pos['couverture']:.2%}",``
- **T1** `- **T1** `> **65,84 % des jetons** et **75,19 % des caractères** ; stabilité structurelle``
- **T1** `- **T1** `**Lecture.** Les segments ne couvrent que **65,84 %** des jetons : le plancher lexical``
- **T1** `- **T1** `- **La complétude de la structure** : les segments ne couvrent que 65,84 % des jetons.``
- **T1** `- **T1** `86,5 % des groupes ambigus). Une autre préférence changerait le squelette et la``
- **T1** `- **T1** `fidélité    : exacte 1.0000 · caractères 1.0000 · couverture 100.00%``
- **T1** `- **T1** `mots        : exacte 0.0000 · caractères 0.9286 · couverture 84.62%``
- **T1** `- **T1** `pos         : exacte 0.0000 · caractères 0.9286 · couverture 84.62%``
- **T1** `- **T1** `de caractères (0,9286) dit, elle, que 93 % des caractères sont au bon endroit.``
- **T1** `- **T1** `(`evaluer` : POS 86,25 %, F1 79,02 %, attachement 237/238).``
- **T1** `#     couche 0 à 0,75 → **12,9635** contre **14,6496** sans réglage (**−11,5 %**), et couche`
- **T1** `#     1 à 0,5 → 13,7907 (−5,9 %) ; la couche 2 n'a plus d'optimum utile.`
- **T1** `# Mesuré sur les 24 couches à 0,75 : seules les couches 0 (−11,5 %) et 1 (−4,5 %) gagnent ;`
- **T1** `# les couches 2 et 3 perdent beaucoup (+9,2 %, +10,6 %) et les suivantes restent dans ±1 %`
- **T1** `# (sauf 17, 21, 23 : +3,8 à +5,7 %). Le déséquilibre est donc à l'ENTRÉE, pas réparti.`
- **T1** `reports/INDEX.md:263:| [rapport-modules-famille.md](rapport-modules-famille.md) | C3.2b — un module de restitution par famille : l'indo-européen recopie à 100 % |`
- **T1** `reports/INDEX.md:532:| [rapport-pensee-miroir-resume.md](rapport-pensee-miroir-resume.md) | B13 — la restitution sémantique : le résumé rappelle 78 % |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `| `porte-c4-retard.sh` | 29 s | PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne |`
- **T1** `| `porte-coupe.sh` | 131 s | ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit pour  |`
- **T1** `| `porte-delais.sh` | 21 s | ✅ le temps, lui, augmente : 6.77 s → 9.67 s (+2.9 s ≈ 50 ms × 64 pas) |`
- **T1** `| `porte-homeostasie.sh` | 495 s | ✅ porte tenue (×0 exact · activité monotone · dominance reproduite) |`
- **T1** `| `porte-jeux.sh` | 104 s | ✅ la porte des jeux tient : 100 % au niveau 4, 33/33 paires invariantes, 0 collision, |`
- **T1** `| `porte-mistral.sh` | 8 s | ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= plancher  |`
- **T1** `| `porte-pont.sh` | 79 s | ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux |`
- **T1** `| `porte-reflexe.sh` | 141 s | ✅ 3. l'accord est mesuré AVANT (0.4 %) et APRÈS — la mesure est branchée |`
- **T1** `| `porte-reparti-moteur.sh` | 3 s | PORTE TENUE : le découpage ne change pas la perplexité (écart relatif 0.0000 %) |`
- **T1** `✅ optimum intérieur : 12.9635 contre 14.1057, 15.4298 et 14.6496 sans réglage (11.5 % de mieux)`
- **T1** `SYNTAGMES   F1 78.82 %  (P 78.18 % / R 79.46 %)`
- **T1** `tête      F1 90.25 %  (P 92.34 % / R 88.26 %)`
- **T1** `CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)`

## 5. Erreurs rencontrées

5 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 8, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py", line 569, in mesurer_banc_v2     m =
- **T1** : #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS # (`--attn-window` en r
- **T1** : (no output) [exit code: 1]
- **T1** : (no output) [exit code: 1]
- **T1** : 32:> [`gold_restitution_v2.json`](../tools/tests/linguistique/gold_restitution_v2.json) ; 33:> tests [`test_restitution_v2.py`](../tools/tests/test_restitution_v2.py) ; 104:[`gold_restitution_v2.json`

