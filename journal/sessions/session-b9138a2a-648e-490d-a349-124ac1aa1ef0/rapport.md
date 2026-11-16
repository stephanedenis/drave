# Session session- — CI GitHub Actions matrice tests

> **Journaux :** [le jour](../../2026-11-16/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-b9138a2a-648e-490d-a349-124ac1aa1ef0` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-16 03:27 |
| Durée | 0.7 h |
| Tours | 1 |
| Messages | 186 |
| Appels d'outils | 239 |
| Fichiers touchés | 13 |
| Commandes | 144 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche Z1 (exploitable, la protection) : l'**intégration continue** — un `.github/workflows/ci.yml` : la matrice **Python 3.10 / 3.13**, `pip install -e .`, `python3 tools/tests/test_produit.py`, `python3 tools/tests/test_tagger_api.py`, `bash tools/porte-produit.sh`, `python3 tools/tests/test_schema_produit.py` ; le **contrôle négatif** : un test qui casse doit faire échouer le job (le prouver en  … [191 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche Z1 (exploitable, la protection) : l'**intégration continue** — un `.github/workflows/ci.yml` : la matrice **Python … [471 caractères tronqués]

*239 appels d'outils.* Actions notables :

- bash — Explore repository structure
- bash — Check git status and recent commits
- bash — Read pyproject, gate script, test head
- bash — Check act, python versions, yaml
- bash — Check python version managers and pip
- bash — Read tests and find CI-related reports
- bash — Search for Z1 and CI references
- bash — Read a recent report and JSON
- bash — Check uv Python availability
- bash — Read current state and roadmap
- bash — Search plan.json for Z1
- bash — Read report registry conventions
- bash — Print all Z tasks from plan
- bash — Read plan around Z1
- … et 194 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.github/workflows/ci.yml` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py` | 1 | 13 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/ci.md` | 1 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md` | 1 | 12 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.github/ci/structures/README.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_structures_secours.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 2 |

### Commandes exécutées (échantillon)

- **T1** Explore repository structure
- **T1** Check git status and recent commits
- **T1** Read pyproject, gate script, test head
- **T1** Check act, python versions, yaml
- **T1** Check python version managers and pip
- **T1** Read tests and find CI-related reports
- **T1** Search for Z1 and CI references
- **T1** Read a recent report and JSON
- **T1** Check uv Python availability
- **T1** Read current state and roadmap
- **T1** Search plan.json for Z1
- **T1** Read report registry conventions
- **T1** Print all Z tasks from plan
- **T1** Read plan around Z1
- **T1** Inspect recent task commit contents
- **T1** Inspect another task commit and JSON naming
- **T1** Run product smoke test
- **T1** Run schema product test
- **T1** Run tagger API test
- **T1** Run product gate
- **T1** Inspect tagger test failures
- **T1** Find gele argument usage
- **T1** Read failing test code and drave call
- **T1** Find monkeypatches of _module_evaluation
- **T1** noop
- **T1** Count lines in test file
- **T1** Rerun tagger API test
- **T1** Try installing Python 3.10 with uv
- **T1** Show test fix diff
- **T1** Create Python 3.10 venv and editable install
- **T1** Create Python 3.13 venv and editable install
- **T1** Run three tests on Python 3.10 venv
- **T1** Run three tests on Python 3.13 venv
- **T1** Inspect submodules and remotes
- **T1** Check submodule dependency in tests
- **T1** Find code depending on structures submodule
- **T1** Check optional structures import
- **T1** Test editable install from archive without submodules
- **T1** Inspect product docs structure
- **T1** Read product README start and end
- … et 104 autres

## 4. Mesures et résultats marquants

- **T1** `langues stratifiées** (5 familles × 4, 10 écritures), choisies pour l'égalité exacte de`
- **T1** `ne dit pas que les 398 langues font 100 %. L'autotest complet le dit :`
- **T1** `- **La roue n'est pas minimale** : l'artefact ajoute ~0,33 Mo compressés à la roue U2`
- **T1** `- **`--profils` est une option** : elle charge l'artefact (~800 Ko) et score 398 profils par`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.`
- **T1** `| **R4.4** | **vision/OCR** : scans, figures, layout | 🔬 **mesuré sur scans simulés ; ouvert sur les scans réels** : 5 familles (photo **55,9 → 6,7 %** de WER, test **5,7 %**), **préservation 90–97 %*`
- **T1** `pour 11,47 M ; la capacité à budget égal donne **−8,1 %**, mais le prior domine. La structure d'abord.`
- **T1** `| S — la banque validée | **`/paragraphes` fini** : 9/9 paragraphes, 19/19 candidats, 11 acceptés, 8 exclus, **11 verdicts committés (`389b99f`)** ; **banque 150 verdicts / 74 des 207 phrases** (35,7 `
- **T1** `- **R0** : un contrôleur **classique** + un modèle externe atteint-il **90 %** de la compréhension à **30 %** du`
- **T1** `journal/sessions/564fbe3a-a859-4b3b-bd17-4da73a2f4e22/rapport.md:130:- **T1** `mov.b64 	%rd28, _ZZ15attn_topk_histoE2sh;``
- **T1** `journal/sessions/564fbe3a-a859-4b3b-bd17-4da73a2f4e22/digest.md:765:	mov.b64 	%rd28, _ZZ15attn_topk_histoE2sh;`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `| [rapport-a83-defaut.md](rapport-a83-defaut.md) | A8.3 — le défaut place+perte n'est pas neutre : les portes épinglées bougent de −5,9 % à +19,5 % |`
- **T1** `| [rapport-a83a-coupe.md](rapport-a83a-coupe.md) | A8.3a — `porte-coupe` : le régime 1 % écrase la variance du point de coupe |`
- **T1** `| [rapport-a83a-flux.md](rapport-a83a-flux.md) | A8.3a — `porte-flux` : le régime 1 % a ses propres références |`
- **T1** `| [rapport-a83a-pont.md](rapport-a83a-pont.md) | A8.3a — `porte-pont` : le régime 1 % change la falaise |`
- **T1** `| [rapport-a83d-lot-threads.md](rapport-a83d-lot-threads.md) | A8.3d — le lot n'est pas les threads : l'écart de 1,90 % survit à 1 thread |`
- **T1** `"mandat": "Tâche Z3 (le bilan pour l'humain) : un **bilan court** (le matin) — `reports/rapport-bilan-final.md` + JSON : ce qui est installable (les 3 voies : editable, roue, le chemin historique), le`
- **T1** `d19f0fc7 U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO`
- **T1** `83adaa2b T6 — LE BILAN EXPLOITABLE : T1-T5 LIÉES (INSTALLABLE, JSON V2 2 139 OBJETS, QUICKSTART 3/3, 10 000 MOTS 4,01 S, CLI 20/20) ; TROIS LIMITES NOMMÉES (CLONE PUBLIC 88,70 %, O(K²) α 1,55, GOLD DE`
- **T1** `9a291c8b T5 — LA CLI ROBUSTE : --DUREE (4,7–5,9 MS), CODES 0/3/4/5 (2 → 5, FICHIER 1 → 4/5), AIDE 8/8, --FICHIER SANS TRACE ; 20/20 CAS, 30 TESTS`
- **T1** `7f0e8320 T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))`
- **T1** `[still running after 60000ms; moved to background job bash-20]`
- **T1** `self.assertEqual(donnees["tagger"]["cout"]["appels"], 2)  # 2 phrases × 1 tagger`
- **T1** `self.assertEqual(cout["appels"], 500)     # 1 appel pour 2 phrases, × 500`
- **T1** `self.assertEqual(cout["tokens"], 8500)    # 17 tokens pour 2 phrases, × 500`
- **T1** `| **unités sémantiques** | les spans candidats à la RSN et la fraction du texte | **55,4 %** du texte en moyenne |`
- **T1** `| **la performance du cache** (×139, conditions) | [`reports/rapport-cache-chunker-applique.md`](../../reports/rapport-cache-chunker-applique.md) |`
- **T1** `| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO |`
- **T1** `| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO | `en`
- **T1** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T1** `35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1`
- **T1** `393:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `/paragraphes`** (11 accepté`
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 15/11 (nuit).** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **F1 0,7902**, `
- **T1** `**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (hasard`
- **T1** `langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)`
- **T1** `[still running after 60000ms; moved to background job bash-87]`
- **T1** `"analyser": "rôle=agent", "cible": "→ chat", "f1": "F1 79.02 %",`
- **T1** `"attachement": "ATTACHEMENT exact 99.58 %",`
- **T1** `POS         exactitude 86.25 %  (fermé 93.73 %, ou`
- **T1** `[still running after 60000ms; moved to background job bash-144]`

## 6. Commits

- Z1 — L'INTÉGRATION CONTINUE : MATRICE 3.10/3.13, 10/10 ÉTAPES VERTES (ARCHIVE SANS SOUS-MODULE, COPIE DE SECOURS S) ; PORTE 183/183 ; TEST CASSÉ → 1, JOB ARRÊTÉ

