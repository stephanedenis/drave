# Session session- — Benchmark performance de l'analyseur NLP

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-cbce9c66-4423-4a44-a112-b8c9f8b333dc` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 22:35 |
| Durée | 0.6 h |
| Tours | 1 |
| Messages | 146 |
| Appels d'outils | 174 |
| Fichiers touchés | 4 |
| Commandes | 164 |
| Sous-agents | 0 |
| Commits | 4 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche T4 (exploitable, 4/5) : la **performance** — mesure `analyser` sur un texte réel de **10 000 mots** (le corpus du dépôt ou un texte assemblé), le **temps** (s), le **débit** (mots/s), la **mémoire** (pic RSS), la **taille du JSON**, et le même sur 100 phrases courtes (le coût fixe par appel) ; compare avec `--tagger` (le coût réseau) ; le **contrôle négatif** : le temps doit croître linéaire … [144 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche T4 (exploitable, 4/5) : la **performance** — mesure `analyser` sur un texte réel de **10 000 mots** (le corpus du  … [424 caractères tronqués]

*174 appels d'outils.* Actions notables :

- bash — Inspect repo root and git state
- bash — List tools and reports directories
- bash — Find analyser and tagger implementations
- bash — Locate analyser and tagger in CLI
- bash — Check file sizes and data corpus
- bash — Look for existing perf work and current state
- bash — Find T4 task definition
- bash — Search for performance bench spec
- bash — Read drave CLI header
- bash — Find exploitable task series
- bash — Read work plan
- bash — Search git history for T4
- bash — Read analyser formatting and command
- bash — Read analyser command implementation
- … et 157 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/banc_performance.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance.md` | 2 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_banc_performance.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-banc-performance.sh` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Inspect repo root and git state
- **T1** List tools and reports directories
- **T1** Find analyser and tagger implementations
- **T1** Locate analyser and tagger in CLI
- **T1** Check file sizes and data corpus
- **T1** Look for existing perf work and current state
- **T1** Find T4 task definition
- **T1** Search for performance bench spec
- **T1** Read drave CLI header
- **T1** Find exploitable task series
- **T1** Read work plan
- **T1** Search git history for T4
- **T1** Read analyser formatting and command
- **T1** Read analyser command implementation
- **T1** Read result method doc
- **T1** Read tagger cost accounting
- **T1** Inspect heuristic API
- **T1** Inspect corpus candidates
- **T1** Read heuristic analyser internals
- **T1** Read Annotation json contract
- **T1** Check time utility and API key presence
- **T1** Inspect clean corpora heads
- **T1** Count words in candidate corpora
- **T1** Check sentence segmentation of corpus
- **T1** Probe 10k prefix and short sentences
- **T1** Test one tagger API call
- **T1** Inspect DeepSeek client cache behavior
- **T1** Find tagger cache files
- **T1** Test tagger network call with fresh cache
- **T1** Find roadmap line for T tasks
- **T1** Inspect T3 and T2 commits
- **T1** Read T3 report style
- **T1** Inspect roadmap product lines
- **T1** Inspect journal day structure
- **T1** Read full current state file
- **T1** Run doc review baseline
- **T1** Prototype 10k analyser measurement
- **T1** Collect machine info
- **T1** Prototype 100 short sentence in-process calls
- **T1** Prototype scaling sizes
- … et 124 autres

## 4. Mesures et résultats marquants

- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/r`
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:3201:- **T4** `/dev/nvme0n1p2  828G  243G  586G  30% /home``
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:3202:- **T4** `Creating uninstaller 25%``
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:3203:- **T4** `Creating uninstaller 50%``
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:3204:- **T4** `Creating uninstaller 75%``
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:3205:- **T4** `Creating uninstaller 100%``
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:17056:- **T4** `/dev/nvme0n1p2  828G  243G  586G  30% /home``
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:17057:- **T4** `Creating uninstaller 25%``
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:17058:- **T4** `Creating uninstaller 50%``
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:17059:- **T4** `Creating uninstaller 75%``
- **T1** `journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md:17060:- **T4** `Creating uninstaller 100%``
- **T1** `| **N2 — le natif (session `0733c5bb`)** | entraîner et évaluer le modèle natif sur les corpus D, mesurer longueur, capacité, diversité | N2, N4, le mètre honnête | **GPU** (1 des 2), 8–16 cœurs | **N`
- **T1** `| **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**, 2–8 cœurs | **166/166** (6 S fi`
- **T1** `**0,7539**, acte **1,0**) ; **DRVM/native** par la règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **gold 432 : acte 0,9954** ; **fusion p`
- **T1** `**147 scans détectés** (91 uniques, 2 053 p), **60 documents, 1 982 p, 4,41 M car.**, 8 Ko 0 ;`
- **T1** `5e53c744 Bloc 0-9 : première borne d'approximabilité — 19 % de la variance après dix couches avec DEUX directions`
- **T1** `f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `Le seuil de restriction (50 %, 75 %…) n'a pas été optimisé : c'est un curseur,`
- **T1** `| **coût caché** | poids touchés = 100 % | mise à jour pré symétrique | compteur | règle post-only, ou mise à jour différée`
- **T1** `docs/pilotage/roadmap.md:288:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** +`
- **T1** `> `agent` / `chat`, et `evaluer` **81,88 %** / **88,70 %** au lieu de **79,02 %** / **99,58 %**.`
- **T1** `| `drave evaluer` | `/tmp/qs-doc/drave` | **0** | **86,25 %** | **81,88 %** | **88,70 %** |`
- **T1** `La sortie complète (612 phrases, 239 cibles, base réelle 452, contrôle négatif **1,67 %**) est`
- **T1** `dans le document (§ 3.3). Le contrôle négatif est **1,67 %** dans les deux configurations : il`
- **T1** `"stdout": "drave 0.1.0 — analyse heuristique (CPU, hors ligne)\nlangue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)\nPOS  Le/DET chat/NOUN dort/VERB ./PONC`
- **T1** `"stdout": "drave 0.1.0 — évaluation de l'heuristique sur le gold\ngold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement\n\nPOS         exactitude 86.25 %  (fer`
- **T1** `35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1`
- **T1** `38:**État au 15/11.** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact`
- **T1** `48:**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (has`
- **T1** `106:sources acquises ne sont pas 102 URL (71 URL uniques). La loi H0 se reproduit (**R² = 0,909139** sur`
- **T1** `288:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes`
- **T1** `363:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** ([tête](../theorie/glossaire/entrees/tete.md) de survol) et **R0.5** ([routeur](../theorie/glossaire/entrees/routeur.md)) sont`
- **T1** `**100 scans simulés** : la photo passe de **55,9 %** à **6,7 %** de [WER](../theorie/glossaire/entrees/wer.md) (test **5,7 %**) et la`
- **T1** `| **A2** | placer sur une machine : [KV](../theorie/glossaire/entrees/kv.md) paginé, [GPU](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md), [top-k](../theorie/glossaire/entrees`
- **T1** `| **A5** | formats, matériels, énergie : SIMD, PTX, FPGA, KV | ✅ / 🧱 | **A5.4 bloqué** (FPGA) ; le 8 bits tardif est gratuit (+0,03 %) |`
- **T1** `| **A8** | l'ordonnanceur place **et** perte : `choisir_avec_perte` | ✅ **opt-in** ; 6 portes épinglées, A8.3 **échoue** (−5,9 % … +19,5 %) | **A8.3c/d** : le lot change la PPL, pas les threads ; rédu`
- **T1** `| **B5** | la sémantique des jeux : contrat [RSN-jeu](../theorie/glossaire/entrees/rsn-jeu.md), cinq niveaux, bruit | ✅ | aucune — 112 items, **100 %** au niveau 4 |`
- **T1** `| **B6** | la logique dans la pensée : règles, recherche, cartes, invariance | ✅ | aucune — perft, **3/3** mats, dames **20/20**, cartes **79,7 %** |`
- **T1** `| **B8** | les maîtres : 17 principes, 9 sources, livre, parties | ✅ | aucune — livre **10/10**, go 9×9 **10/10** contre 3/10, cartes **44,7 %** |`
- **T1** `| **B11** | la base d'universaux typés : schéma, [parseur](../theorie/glossaire/entrees/parseur.md), codec, contexte | ✅ | **B11.10 close** (cartes, ambiguïtés refusées) ; le codec lit **100 %** |`
- **T1** `| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes** +`
- **T1** `| **C3.2** | les modules par famille de langues | ✅ | aucune — **7/9 > 30 %**, moyenne **69,5 %**, contrôle **≤ 0,5 %** |`
- **T1** `**Ce qui compte pour R** : le **codec classique** lit **100 %** des surfaces ; c'est la preuve qu'un bloc`
- **T1** `| **N1** | `drave-n0` : 11,47 M, 6 blocs, octets, [attention](../theorie/glossaire/entrees/attention.md) locale, [FFN](../theorie/glossaire/entrees/ffn.md) creux, 3 têtes précoces | ✅ | aucune — PPL *`
- **T1** `| **N2** | la distillation : corpus, professeur, [curriculum](../theorie/glossaire/entrees/curriculum.md) | 🔬 | **N2.h** — corpus dédupliqué (**0 %** de fuite) : la chaîne propre vaut **3,0904**, pas `
- **T1** `| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE PAR DÉFAUT ; 20 TESTS |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) |`
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) |`
- **T1** `| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) | `en-cours.md`, `README.md`, `
- **T1** `| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) | `en-cours.md`, `README.md`, `me`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `CPU(s) scaling MHz:                      56%`
- **T1** `chunker le plus large **est** ce span (86,5 %) ; le S le plus large ne l'est que 25 fois sur 244.`
- **T1** `f"({a.fraction_semantique:.1%} du texte)")`
- **T1** `[still running after 180000ms; moved to background job bash-48]`
- **T1** `[still running after 60000ms; moved to background job bash-74]`
- **T1** `| taille du JSON | **14,795,890 octets** (14.8 Mo) |`
- **T1** `| 100 appels CLI séparés | **186.7 ms/appel** (19.20 s pour 100) |`
- **T1** `| 100 appels fonction | **1.10 ms/appel** (0.116 s) |`
- **T1** `| coût fixe (ordonnée) | **1.18 ms** · pente **0.00 ms/mot** |`
- **T1** `- pente log-log **α = 1.55** (R² 0.995) — 1 = linéaire, 2 = quadratique ;`
- **T1** `- linéaire : R² 0.957, RMSE 1.032 s ;`
- **T1** `- quadratique : R² 1.000, c = 1.313e-07 s/mot², RMSE 0.036 s ;`
- **T1** `| 100 appels CLI séparés | **191.6 ms/appel** (19.43 s pour 100) |`
- **T1** `| un appel `--jsonl` pour les 100 | **0.369 s** (soit 3.69 ms/phrase) |`
- **T1** `| accélération du lot vs 100 CLI | **×52.6** |`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `/paragraphes`** (11 accepté`
- **T1** `65:- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144** (cinq **18/18**), gold v2 **20/46**, permutation **0/18** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture*`
- **T1** `88:- **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports/rapport-restitution-v2.md), [v`
- **T1** `164 17 `--json`, **126 Mio** de pic RSS et **14,8 Mo** de JSON ; **1,10 ms/appel** sur **100 phrases`
- **T1** `165 16 courtes**, **191,6 ms** pour un CLI par phrase, **0,369 s** pour les 100 en un `--jsonl`.`
- **T1** `167 12 explique **R² 0,99995** contre **0,957** pour le linéaire ; `_groupes_partition` (toutes les`
- **T1** `170 10 estimation), le réseau portant **99 %** du temps. [Fiche](../../reports/rapport-performance.md) ·`
- **T1** `+**14,8 Mo** JSON ; 100 phrases **1,10 ms** ; `--tagger` **1,17 s/phrase**.`
- **T1** `+**Contrôle de linéarité négatif** : **α = 1,55**, **R² 0,99995** ;`
- **T1** `| [rapport-a80-porte-delais.md](rapport-a80-porte-delais.md) | A8.0 — `porte-delais` épingle la PPL : 59,0790 à 0 et 50 ms |`
- **T1** `| [rapport-a80-porte-pont.md](rapport-a80-porte-pont.md) | A8.0 — `porte-pont` épingle sa PPL et sa falaise : 113,0068 / 111,9225, +2,81 % / +25,35 % |`
- **T1** `[s/v7 7f0e8320] T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))`
- **T1** `7f0e8320 T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))`
- **T1** `**2 493 mots/s**, **128 972 Ko** de pic RSS, **14 795 890 octets** de JSON,`
- **T1** `**54 522 étiquettes**, **2 726 syntagmes**. Sur **100 phrases courtes** : **1,10 ms/appel**`
- **T1** `pour la fonction, **1,18 ms** de coût fixe, **191,6 ms** pour un CLI par phrase, **0,369 s**`
- **T1** `pour les 100 en un `--jsonl` (×52,6). Avec `--tagger` et un cache froid : **110,2 s** pour`
- **T1** `**92 appels**, **14 677 tokens**, **109,1 s** de réseau, soit **1,17 s/phrase** et **×299** le`
- **T1** `**R² 0,99995** contre **0,957** pour le linéaire. Le contrôle de l'instrument retrouve bien`
- **T1** `d'ajustement. Le profil du bloc ×16 désigne `_groupes_partition` (toutes les paires de`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:3201:- **T4** `/dev/nvme0n1p2  828G  243G  586G  30% /home` journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:3202:- **T
- **T1** : --- [exit code: 1]
- **T1** : #!/usr/bin/env bash # porte-produit — le premier produit : la CLI répond, le JSON est valide, le rejeu est identique. # # Ce qu'elle vérifie : `drave --version`, `analyser` (fr et en) rend un JSON par

## 6. Commits

- git commit -F - <<'EOF' T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ É
- git add reports/rapport-performance.md && git commit --amend --no-edit 2>&1 | tail -20; echo "rc=$?"
- git add docs/pilotage/en-cours.md && git commit --amend --no-edit 2>&1 | tail -20; echo "rc=$?"
- python3 - <<'PY' p='docs/pilotage/en-cours.md' s=open(p,encoding='utf-8').read() s=s.replace('**Mis à jour : 2026-11-15, 23 h 06 HNE (T4 : la performance)**',  

