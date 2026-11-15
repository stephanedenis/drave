# Session session- — Matrice tagger et recommandation par défaut

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-bc92a84f-e2ea-4c23-8227-525822d29662` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 09:44 |
| Durée | 1.0 h |
| Tours | 1 |
| Messages | 141 |
| Appels d'outils | 156 |
| Fichiers touchés | 7 |
| Commandes | 118 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche W3 (J2 après-midi) : la matrice du tagger — **défaut** (sans clé, hors ligne, code 0), **avec clé**, **clé invalide**, **réseau coupé**, le coût pour 1 000 phrases, le repli ; la recommandation (défaut hors ligne, `--tagger` opt-in, un mode `auto` seulement si la clé existe et sans changer le code de sortie). Fiche `reports/rapport-tagger-defaut.md` + JSON, avec un test par cas dans `tools/t … [25 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche W3 (J2 après-midi) : la matrice du tagger — **défaut** (sans clé, hors ligne, code 0), **avec clé**, **clé invalid … [305 caractères tronqués]

*156 appels d'outils.* Actions notables :

- bash — Show repo root and recent commits
- bash — List tests and reports directories
- bash — Find tagger-related Python files
- bash — Read existing tagger API test
- bash — Read rest of tagger API test
- bash — Find tagger wiring in drave CLI
- bash — Locate W3 task definition
- bash — Inspect recent journal entries
- bash — Read tagger H50 report
- bash — List and inspect tagger JSON reports
- bash — Read tagger errors report
- bash — Read tagger option report
- bash — Check API key presence without printing it
- bash — Search for token pricing references
- … et 113 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-defaut.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-defaut.json` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/mesures.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** Show repo root and recent commits
- **T1** List tests and reports directories
- **T1** Find tagger-related Python files
- **T1** Read existing tagger API test
- **T1** Read rest of tagger API test
- **T1** Find tagger wiring in drave CLI
- **T1** Locate W3 task definition
- **T1** Inspect recent journal entries
- **T1** Read tagger H50 report
- **T1** List and inspect tagger JSON reports
- **T1** Read tagger errors report
- **T1** Read tagger option report
- **T1** Check API key presence without printing it
- **T1** Search for token pricing references
- **T1** Check for existing auto mode
- **T1** Read drave tagger implementation
- **T1** Inspect today's journal
- **T1** Find W3 in state and roadmap
- **T1** Find W3 in planning docs
- **T1** Run tagger API tests baseline
- **T1** Measure default without key
- **T1** Inspect DeepSeek client cache config
- **T1** Read client retry logic
- **T1** Run real API with key on one sentence
- **T1** Run real invalid key case
- **T1** Run real network-down fallback case
- **T1** Inspect cost fields in W2 JSON
- **T1** Find cost usage sites
- **T1** Read evaluer implementation
- **T1** Find planning text about tagger default
- **T1** Look for week 2 plan
- **T1** Read analyser command
- **T1** Check tests reading reports
- **T1** Search previous dollar estimates
- **T1** Read pricing approach in prior reports
- **T1** Check if W2 API cache still exists
- **T1** Aggregate W2 cache token usage
- **T1** Compute exact cost at published tariff
- **T1** Collect real matrix measurements
- **T1** Inspect collected matrix details
- … et 78 autres

## 4. Mesures et résultats marquants

- **T1** `self.assertEqual(donnees["tagger"]["cout"]["appels"], 2)  # 2 phrases × 1 tagger`
- **T1** `"sortie": "drave 0.1.0 \u2014 analyse cascade POS (tagger API DeepSeek, r\u00e9seau)\nlangue=fr script=Latn source=cascade \u00b7 20 \u00e9tiquettes \u00b7 unit\u00e9s s\u00e9mantiques=2 (61.5% du tex`
- **T1** `"sortie": "drave 0.1.0 \u2014 analyse cascade POS (tagger API DeepSeek, r\u00e9seau)\nlangue=fr script=Latn source=cascade \u00b7 43 \u00e9tiquettes \u00b7 unit\u00e9s s\u00e9mantiques=3 (48.6% du tex`
- **T1** `"sortie": "drave 0.1.0 \u2014 analyse cascade POS (tagger API DeepSeek, r\u00e9seau)\nlangue=en script=Latn source=cascade \u00b7 38 \u00e9tiquettes \u00b7 unit\u00e9s s\u00e9mantiques=3 (45.7% du tex`
- **T1** `> **88,57 % → 97,14 %** sur 20 phrases `hand` (**+8,57 pts**), cohérent avec le **0,9475 contre`
- **T1** `- **Classe tirée au hasard** (12 classes, graine 0) : **10,48 %** ; **classe majoritaire**`
- **T1** `(`VERB`) : **22,86 %**. Le tagger (97,14 %) et l'heuristique (88,57 %) sont très au-dessus :`
- **T1** `reports/rapport-exemples-tagger.json:26:    "sortie": "drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)\nlangue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.`
- **T1** `reports/rapport-exemples-tagger.json:52:    "sortie": "drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)\nlangue=fr script=Latn source=cascade · 43 étiquettes · unités sémantiques=3 (48.`
- **T1** `reports/rapport-exemples-tagger.json:78:    "sortie": "drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)\nlangue=en script=Latn source=cascade · 38 étiquettes · unités sémantiques=3 (45.`
- **T1** `reports/rapport-exemples-tagger.json:131:    "sortie": "drave 0.1.0 — évaluation de l'heuristique sur le gold\ngold réel (hand + reel, sans synthétique) · 452 phrases · 2480 tokens · 184 cibles d'atta`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) | `en-cours.md`, `README.md`, `
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) | `en-cours.md`, `README.md`, `me`
- **T1** `docs/pilotage/en-cours.md:64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; **D1–D3**, **E1–E2** livrés ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../..`
- **T1** `docs/pilotage/roadmap.md:33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 c`
- **T1** `docs/pilotage/roadmap.md:363:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantiq`
- **T1** `reports/rapport-c4-retard.md:1:# C4 — le prix d'un état en retard : **×633 pour UN pas**, et ce que ça impose à un ordonnanceur`
- **T1** `reports/rapport-c4-retard.md:71:état reçu. Le prix est ×633 par pas, mesuré.`
- **T1** `reports/rapport-compacite-trace.md:15:> (−65,9 % par rapport à la v1, −32,1 % par rapport à la v2), au prix de`
- **T1** `reports/rapport-couche-int8-canal.md:23:- Le **volume** tombe à **36–39 %** du dense : **2,6× moins** d'octets, au prix des 896 échelles`
- **T1** `reports/rapport-dessin-B-poids-creux.md:82:densité (E1 mesure le prix d'un connectome aléatoire à 12,9 % : **+18,4 %** de perplexité) — et`
- **T1** `reports/rapport-e5-distillation.md:13:> **l'accord fait ×1,8** (m20 : 40,5 % → **68,1 %**) au prix d'une perplexité **×3,2**. Et au niveau`
- **T1** `| tokens | ~360 000 | **358 962** | −0,3 % |`
- **T1** `| durée | ~20 min | **20 min 59 s** (1 259,2 s) | +5 % |`
- **T1** `| latence moyenne / appel | 0,94 s (run 432) | **1,033 s** | +10 % |`
- **T1** `**27 326 tokens de sortie** (totaux à ±0,5 % près, six prompts dupliqués).`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `| [rapport-a83-defaut.md](rapport-a83-defaut.md) | A8.3 — le défaut place+perte n'est pas neutre : les portes épinglées bougent de −5,9 % à +19,5 % |`
- **T1** `| [rapport-a83a-coupe.md](rapport-a83a-coupe.md) | A8.3a — `porte-coupe` : le régime 1 % écrase la variance du point de coupe |`
- **T1** `| [rapport-a83a-flux.md](rapport-a83a-flux.md) | A8.3a — `porte-flux` : le régime 1 % a ses propres références |`
- **T1** `| [rapport-a83a-pont.md](rapport-a83a-pont.md) | A8.3a — `porte-pont` : le régime 1 % change la falaise |`
- **T1** `| [rapport-a83d-lot-threads.md](rapport-a83d-lot-threads.md) | A8.3d — le lot n'est pas les threads : l'écart de 1,90 % survit à 1 thread |`
- **T1** `| [rapport-autotest-parallele.md](rapport-autotest-parallele.md) | B13 — la vérification parallèle : 183/183 en 1 min 54 (×2,4) |`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T1** `383:**88,91 %**, F1 **79,06 %**, attachement **99,46 %**. Sans lui, `evaluer` publie la ligne`
- **T1** `33 - **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** /`
- **T1** `+        self.assertEqual(cout["appels"], 1000)    # 2 appels mesurés × 500`
- **T1** `+        self.assertEqual(cout["tokens"], 17000)   # 34 tokens mesurés × 500`
- **T1** `-- **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](../.`
- **T1** `+- **Panini** : **14 atomes** ; UDHR **418/438** ; J3.2 **5/21** langues (Glottolog **21/21**), **154/154** hors script au hasard, **V14 3/21** ; B2 **négatif** (niveaux non prédits) ; J7.1 famille **`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `-| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ;`
- **T1** `+| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ;`
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `/paragraphes`** (11 accepté`
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `- **Panini** : **14 atomes** ; UDHR **418/438** ; J3.2 **5/21** langues (Glottolog **21/21**), **154/154** hors script au hasard, **V14 3/21** ; B2 **négatif** (niveaux non prédits) ; J7.1 famille **6`
- **T1** `.....................                                                    [100%]`
- **T1** `reports/rapport-tagger-defaut.md:51:| **coût 1 000 phrases** | `evaluer --tagger --json` (2 phrases, transport factice) | **0** | `cout_pour_1000_phrases` | extrapolation ×500 | `TestMatriceW3.test_co`

## 5. Erreurs rencontrées

5 sorties en erreur ou divergentes. Les premières :

- **T1** : == defaut_analyser code 0 octets 5852 duree 0.161 stderr:  source heuristique refus '' pos [(0, 2, 'DET', 'heuristique'), (3, 7, 'NOUN', 'heuristique'), (8, 12, 'VERB', 'heuristique'), (12, 13, 'PONCT
- **T1** : 1 [exit code: 1]
- **T1** : #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS # (`--attn-window` en r
- **T1** : (no output) [exit code: 1]
- **T1** : drwxr-xr-x. 1 stephane stephane 54 15 nov 09:53 work/portes-1115-09h53 porte-adaptateur-sortie.log [exit code: 1]

