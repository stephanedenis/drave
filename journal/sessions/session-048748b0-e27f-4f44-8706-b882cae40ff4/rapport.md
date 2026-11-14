# Session session- — Passe portes, relevé rouges, tag annoté

> **Journaux :** [le jour](../../2026-11-13/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-048748b0-e27f-4f44-8706-b882cae40ff4` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-13 23:11 |
| Durée | 1.4 h |
| Tours | 1 |
| Messages | 63 |
| Appels d'outils | 75 |
| Fichiers touchés | 1 |
| Commandes | 59 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J5.2 : la passe complète des portes (`bash tools/toutes-les-portes.sh`), le relevé des rouges, la mise à jour de `docs/pilotage/references-non-regression.md`, et un **tag annoté** `semaine-2026-11-14` sur le dernier commit vert. Ne pas forcer : si des rouges non nommées apparaissent, écris la fiche et ne tague pas.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J5.2 : la passe complète des portes (`bash tools/toutes-les-portes.sh`), le relevé des rouges, la mise à jour de ` … [202 caractères tronqués]

*75 appels d'outils.* Actions notables :

- read
- bash — Check git state, log, tags
- bash — Inspect tags and pending diff
- bash — List journal and inspect plan
- bash — Read J4-J6 tasks in plan
- bash — List journal 13 and 07
- bash — Search tag conventions
- bash — Inspect pending modifications
- bash — Check time, past passes, GPU
- bash — Check running gates
- bash — Inspect 07/11 passes
- bash — History of references file
- bash — Inspect submodule and gates script
- bash — List gates and check sessions
- … et 36 autres

**Synthèse produite :**

The gates pass is the long pole (~2 h), so I'll start it now on an idle machine (both GPUs free, no other gate running), with a durable log.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/analyse_passe.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Check git state, log, tags
- **T1** Inspect tags and pending diff
- **T1** List journal and inspect plan
- **T1** Read J4-J6 tasks in plan
- **T1** List journal 13 and 07
- **T1** Search tag conventions
- **T1** Inspect pending modifications
- **T1** Check time, past passes, GPU
- **T1** Check running gates
- **T1** Inspect 07/11 passes
- **T1** History of references file
- **T1** Inspect submodule and gates script
- **T1** List gates and check sessions
- **T1** Check mtimes and other agent processes
- **T1** Run full gates pass in background
- **T1** Read weekly report tail and plan day 5
- **T1** Read revue and en-cours checker
- **T1** Read counters checks and state freshness
- **T1** Search tag conventions in pilotage docs
- **T1** Check gates progress
- **T1** Compare table text to logs
- **T1** Find prior pass fiches
- **T1** Read pass history fiche
- **T1** Check gates progress
- **T1** Diagnose pass stall
- **T1** Inspect git hooks
- **T1** Read roadmap head
- **T1** Find pass tooling
- **T1** Check pass progress
- **T1** Read porte-tableaux
- **T1** Check pass progress
- **T1** Parse references table coverage
- **T1** Check doc size budgets
- **T1** Read doc size checker
- **T1** Measure row text lengths
- **T1** Check source line lengths
- **T1** Distribution of row text lengths
- **T1** Check 07/11 lines for special gates
- **T1** Check if dirty submodule affects gates
- **T1** Check pass progress
- … et 19 autres

## 4. Mesures et résultats marquants

- **T1** `9c7f71dc PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE`
- **T1** `0, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T1** `1, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T1** `| **R7** | Un **effet d'époque** dans le retrieval | brut 0,238 vs 0,427 ; à script contrôlé 0,710 vs 0,710 ; date −0,034, p = 0,19 | effet de **composition** (60 % vs 33 % de même écriture) |`
- **T1** `| **J2** | après-midi : corpus commun | ✅ fait | **21 textes**, 5 familles, 10 écritures, **418/438** paires exactes (95,4 %), 8/8 contrôles | `c3467170` (avec J3.1) | corpus multi-époques / multi-gen`
- **T1** `docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 c`
- **T1** `docs/pilotage/roadmap.md:180:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** +`
- **T1** `docs/pilotage/roadmap.md:255:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantiq`
- **T1** `> 449/449 au niveau 4, 11/11 paires, permutation 12/275, livre 10/10, go 9×9 10/10 contre 3/10). Les **deux`
- **T1** `> est **verte** (504 s, ×0 exact, activité monotone, dominance reproduite). Les références sont stables :`
- **T1** `> `porte-flux` **60,8135**, `porte-pont` **+2,81 % / +25,35 %**, `porte-coupe` **+0,52 % → +17,09 %**,`
- **T1** `> `porte-gain` **29,0206 → 1297,5437**, `porte-topologie` **42,5477**, `porte-reparti-moteur` **0,0000 %**,`
- **T1** `> clôture de **B5/B6**, avec la nouvelle **`porte-jeux`** (28 s, **verte** : 100 % au niveau 4, 33/33 paires`
- **T1** `> le **LoRA de référence temporaire** `/tmp/n4/rang4-lora.pt` avait été effacé ; **régénéré** par`
- **T1** `> `n4_dessin_b.py --objectif plein --train 10 --rang 4`, la porte **relancée seule passe** (`×0` exact,`
- **T1** `> activité monotone, dominance reproduite : m32 ×0,6 **−8,33 %** contre ×1,0 **−6,51 %**, m20 **−15,10 %**`
- **T1** `> contre **−15,74 %**). Les références sont stables : `porte-flux` **60,8135**, `porte-pont``
- **T1** `> **+2,81 % / +25,35 %**, `porte-coupe` **+0,52 % → +17,09 %**, `porte-gain` **29,0206 → 1297,5437**,`
- **T1** `> `porte-topologie` **42,5477**, `porte-reparti-moteur` **0,0000 %**, `porte-greffe` **branchée**.`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tranché (la tête du GN arrête `
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 07/11 18 h 30.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) réglé `
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `**100 scans simulés** : la photo passe de **55,9 %** à **6,7 %** de [WER](../theorie/glossaire/entrees/wer.md) (test **5,7 %**) et la`
- **T1** `**préservation** du lecteur atteint **90–97 %** sur **4 familles sur 5** (propre **96,7 %** ;`
- **T1** `fax **56,7 %**, la limite d'information) ; les **colonnes** tombent de **89,4 %** à **0,5 %**,`
- **T1** `les **tableaux** donnent **92,6 %** de cellules exactes, et **trois vrais scans** s'accordent à`
- **T1** `**7,10 %** et **88,4 %** de mots, l'**ordre des colonnes** prouvé (**15,3 %** contre **98,0 %**`
- **T1** `611 ms. La restitution depuis un document lu est **R31**.`
- **T1** `porte-coupe.sh 100 '✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit pour '`
- **T1** `M-bM-^\M-^E le coM-CM-;t du pont va de +0.52 % (coupe 18/24) M-CM-  +17.09 % (coupe 15/24) M-bM-^@M-^T il y a un bon endroit pour couper$`
- **T1** `- **Note** : l'attachement est à **236/237 (0,9916)**, la couverture 0,9916, POS **86,25 %**, F1 **0,7535**, 2 spans ; la seule rouge est`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 niveaux |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir 0,2276 |`
- **T1** `porte-c4-retard        ✅                          31 s  PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne`
- **T1** `porte-delais           ✅                          21 s    ✅ le temps, lui, augmente : 7.00 s → 10.42 s (+3.4 s ≈ 50 ms × 64 pas)`
- **T1** `porte-homeostasie      ✅                         529 s    ✅ porte tenue (×0 exact · activité monotone · dominance reproduite)`
- **T1** `porte-jeux             ✅                         111 s    ✅ la porte des jeux tient : 100 % au niveau 4, 33/33 paires invariantes, 0 collision,`

## 5. Erreurs rencontrées

6 sorties en erreur ou divergentes. Les premières :

- **T1** : M docs/pilotage/references-non-regression.md  M reports/pensee-coherence-fiches-v7.json  M reports/pensee-dev-test-v10.json  M reports/pensee-quatre-modes.json  M reports/rapport-audit-v7.md  M report
- **T1** : === structures status ===  M donnees/paragraphes-validations.jsonl === submodule log === 523d8c1 S — LE FAIT DIVERS EST TRANCHÉ : 61/61 TYPES, 144/144 RÔLES ; LA TÊTE DU GN ARRÊTE LE VERBE 4012729 S —
- **T1** : # Historique des passes de portes  > **Document daté — dernière vérification : 2026-10-27.** Ce fichier conserve les > passes complètes antérieures à la dernière (26/10 14 h 30). Les repères courants 
- **T1** : === PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===     journaux : work/portes/passe-1311-23h15 --- [exit code: 1]
- **T1** : === PASSE COMPLÈTE DES PORTES (84 portes, borne 1800 s) ===     journaux : work/portes/passe-1311-23h15 --- registre --- [exit code: 1]
- **T1** : (no output) [exit code: 1]

