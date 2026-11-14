# Session session- — Restitution v1 canonique et mesure du miroir

> **Journaux :** [le jour](../../2026-11-14/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-f198001c-49da-4e65-8a44-782f9605fd7a` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-14 01:48 |
| Durée | 1.4 h |
| Tours | 1 |
| Messages | 128 |
| Appels d'outils | 154 |
| Fichiers touchés | 11 |
| Commandes | 88 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche J8.1 : la restitution v1 — au-delà de la surface exacte (46/46), produire une **forme canonique** depuis l'annotation (segments + rôles + cibles) et la mesurer : le miroir strict (0,1087) doit-il monter ? Fiche `reports/rapport-restitution-v1.md` + JSON, tests, commit.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche J8.1 : la restitution v1 — au-delà de la surface exacte (46/46), produire une **forme canonique** depuis l'annotat … [155 caractères tronqués]

*154 appels d'outils.* Actions notables :

- bash — List workspace and git state
- grep
- read
- bash — Extract J8 tasks from plan.json
- bash — Find restitution code files
- bash — Read restitution.py first 400 lines
- bash — Read v0 measurement script
- bash — Inspect annotation API
- bash — Read Annotation and syntagme generation
- bash — Read mirror definition
- bash — Read CLI restituer handler
- bash — List J tasks in plan
- bash — Search canonical form references
- bash — Read product gate and J8 context
- … et 114 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution.py` | 0 | 12 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_restitution.py` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_restitution_v1.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v1.md` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-produit.sh` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 13 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md` | 0 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-14/README.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** List workspace and git state
- **T1** Extract J8 tasks from plan.json
- **T1** Find restitution code files
- **T1** Read restitution.py first 400 lines
- **T1** Read v0 measurement script
- **T1** Inspect annotation API
- **T1** Read Annotation and syntagme generation
- **T1** Read mirror definition
- **T1** Read CLI restituer handler
- **T1** List J tasks in plan
- **T1** Search canonical form references
- **T1** Read product gate and J8 context
- **T1** Read B18 canonical restitution report
- **T1** Inspect semantic restitution
- **T1** Inspect segments, roles, targets on sample
- **T1** Inspect partition metadata
- **T1** Read partition construction
- **T1** Read partition functions
- **T1** Search J8.1 mentions
- **T1** List restitution artifacts
- **T1** Read results method rules
- **T1** Compute exploratory canonical metrics
- **T1** Compute token coverage and canonical involution
- **T1** Check git status and branch
- **T1** Run existing restitution tests
- **T1** Read free-text test for style
- **T1** Compute linear segment coverage and target resolution
- **T1** Compute target resolution all segments
- **T1** Inspect drave CLI parser
- **T1** Inspect edge case annotations
- **T1** Check current date and journal structure
- **T1** Inspect report index generator and README
- **T1** Inspect latest journal day
- **T1** Inspect plan.json J8.1 and diff
- **T1** Read end of restitution.py
- **T1** Find insertion anchor
- **T1** Show end of restitution.py
- **T1** Append v1 formatters and check syntax
- **T1** Test canonical functions on samples
- **T1** Run full v1 bench and print summary
- … et 48 autres

## 4. Mesures et résultats marquants

- **T1** `9c7f71dc PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE`
- **T1** `f"couverture {surface['couverture']:.2%}",`
- **T1** `f"couverture {mots['couverture']:.2%}",`
- **T1** `f"couverture {pos['couverture']:.2%}",`
- **T1** `docs/archive/roadmap-detail-2026-10-29.md:355:| B12.1 | **Bus + hub M1** | ✅ **mesuré** | **528/528** exact avec contexte ; sans contexte **70,8 %** ; canonique **100 %** ; invariance **100 %** ; 1 58`
- **T1** `docs/theorie/modules-cerveau-langage.md:27:| **M1 hub** | surface → code RSN, retour canonique | **528/528** exact ; sans contexte **70,8 %** ; canonique **100 %** ; invariance **100 %** | ✅ **tient**`
- **T1** `| surfaces rendues | **528 / 528 = 100 %** |`
- **T1** `| relues sans perte | **528 / 528 = 100 %** |`
- **T1** `docs/produit/README.md:131:  vue linéaire (partition filtrer) F1 81.04 %  · attachement 93.31 % de couverture`
- **T1** `chunker le plus large **est** ce span (86,5 %) ; le S le plus large ne l'est que 25 fois sur 244.`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `| [2026-10-15](2026-10-15/outils.md) | `-7,92 %` |`
- **T1** `| [2026-10-17](2026-10-17/outils.md) | `37 %` · `37,5 %` |`
- **T1** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T1** `| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 niveaux |`
- **T1** `| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir 0,2276 |`
- **T1** `| [`rapport-pos-r4-integre.md`](rapport-pos-r4-integre.md) | **B13** — paquet POS sûr, **84,96 %** |`
- **T1** `| [`rapport-pos-anglais-v2.md`](rapport-pos-anglais-v2.md) | **B13** — POS **83,83 %** (R2a/R3/R2b), F1 **0,6181** |`
- **T1** `| [`rapport-autotest-parallele.md`](rapport-autotest-parallele.md) | **B13** — l'autotest parallèle : **183/183 en 1 min 54** (×2,4), mêmes verdicts |`
- **T1** `**521/532** étiquetées Glottolog), le top-1 de voisinage est de la même famille **66,1 %** (hasard`
- **T1** `10,3 %) et de la même branche **26,1 %** (hasard 2,5 %). Mais **hors écriture, tout est au hasard**`
- **T1** `(famille 9,9 % contre 8,1 %, sœur 0,7 % contre 0,8 %) ; dans la même écriture, la famille monte à`
- **T1** `**69,8 %** et la sœur à **27,8 %**. Le retrieval parallèle 30 articles le chiffre : sur les **25`
- **T1** `fidélité    : exacte 1.0000 · caractères 1.0000 · couverture 100.00%`
- **T1** `mots        : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `pos         : exacte 0.0000 · caractères 0.9286 · couverture 84.62%`
- **T1** `48 37 - **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ;`
- **T1** `63 62 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)**`
- **T1** `93 41 - **Panini J7.1** : 532 textes (445 langues) ; **porte d'écriture** (hors script, hasard) ; famille **66,1 %** / sœur **26,1 %** (hasard 10,`
- **T1** `133 26 - **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `134 27 - **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`
- **T1** `| `porte-c4-retard.sh` | 29 s | PORTE TENUE : un état n'est valide qu'à sa position (×633 pour un pas), et l'asynchronisme ne |`
- **T1** `| `porte-coupe.sh` | 131 s | ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit pour  |`
- **T1** `| `porte-delais.sh` | 21 s | ✅ le temps, lui, augmente : 6.77 s → 9.67 s (+2.9 s ≈ 50 ms × 64 pas) |`
- **T1** `| `porte-homeostasie.sh` | 495 s | ✅ porte tenue (×0 exact · activité monotone · dominance reproduite) |`
- **T1** `| `porte-jeux.sh` | 104 s | ✅ la porte des jeux tient : 100 % au niveau 4, 33/33 paires invariantes, 0 collision, |`
- **T1** `| `porte-mistral.sh` | 8 s | ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= plancher  |`
- **T1** `| `porte-pont.sh` | 79 s | ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux |`
- **T1** `| `porte-reflexe.sh` | 141 s | ✅ 3. l'accord est mesuré AVANT (0.4 %) et APRÈS — la mesure est branchée |`
- **T1** `| `porte-reparti-moteur.sh` | 3 s | PORTE TENUE : le découpage ne change pas la perplexité (écart relatif 0.0000 %) |`
- **T1** `0, 1 MiB, 16384 MiB, 0 %`
- **T1** `1, 1 MiB, 16384 MiB, 0 %`
- **T1** `- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 te`
- **T1** `-- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../r`
- **T1** `+- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../r`
- **T1** `- **Panini J7.1** : 532 textes (445 langues) ; **porte d'écriture** (hors script, hasard) ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p`
- **T1** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non** à parité stricte (erratum) ; la repondération vaut **−0,05**.`
- **T1** `- **R1 (nuit)** : 2 048 à 20 000 pas ? → **oui** : 2×10 000 pas finis (perte 0,9409 → 0,8965 ; PPL 2,614 → 2,4953).`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : (no output) [exit code: 1]
- **T1** : 1 porte-adaptateur-sortie.log [exit code: 1]

