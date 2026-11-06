# Session 3fb87dc7 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `3fb87dc7-7d24-42e2-a68e-e37e2734b755` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 23:24 |
| Durée | 1.7 h |
| Tours | 1 |
| Messages | 92 |
| Appels d'outils | 99 |
| Fichiers touchés | 3 |
| Commandes | 75 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **re-mesurer dev/test sur l'état v10** (commit `710ec7f9`) et éprouver la robustesse du split.  Contexte : `tools/tests/linguistique/gold_split.py` (`dev`, `test`, `compter`), `evaluer_gold.py` (`charger`, `evaluer_bloc`), `bloc_linguistique.py`. Les valeurs publiées 152/152 (dev) et 67/67 … [1406 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **re-mesur … [1686 caractères tronqués]

*99 appels d'outils.* Actions notables :

- bash — Show branch, HEAD and status
- bash — List linguistique tools and reports
- read
- bash — Show recent commits and HEAD stat
- bash — Find dev-test and audit reports
- bash — Inspect v7 JSON structure
- bash — Show diffs of the two recent corrections
- bash — Locate the -ée correction in HEAD
- bash — Search -ée handling and v10 JSON
- bash — Measure canonical dev/test globally
- bash — Check corpus counts and scipy availability
- bash — Trace origin of -ée handling
- bash — Inspect autotest changes in v10
- bash — Inspect Annotation and analyser API
- … et 73 autres

**Synthèse produite :**

⏵ Récapitulatif final de la mission

**Mission terminée.** Deux fichiers neufs, aucun commit, aucun fichier existant modifié :

- `reports/rapport-dev-test-v10.md` (490 lignes ; porte-tableaux OK, liens OK)
- `reports/pensee-dev-test-v10.json` (145 Ko ; JSON valide, `spans.par_source` ajouté, `reserves` synchronisées)

Mesure **ancrée sur `710ec7f9`** (module épinglé dans `/tmp`, `RACINE` du dépôt) ; l'arbre a depuis avancé à `653a7981`, qui committe l'essai R2 + retrait de la garde d'adverbe — la fiche le signale et ne le confond pas avec la mesure.

\## dev / test / tout

| | phrases | cibles | labels | couverture | exact/labels | F1 | tête | POS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| dev | 422 | 163 | 152 | **0,9325** | **152/152 = 1,0** | 0,5812 | 0,7330 | 0,7547 |
| test | 190 | 76 | 68 | **0,8947** | **68/68 = 1,0** | 0,5890 | 0,7337 | 0,7656 |
| tout | 612 | 239 | 220 | **0,9205** | **220/220 = 1,0** | 0,5836 | 0,7332 | 0,7581 |

F1/tête **gelées 602** : 0,5880 / 0,7388. **19 spans** perdus : 9 REL, 6 SUB, 4 GP (17 fr / 2 en ; 14 synthétiques / 5 réels).

**Par langue** : fr 91/101 dev, 43/50 test, 134/151 tout ; en 61/62, 25/26, 86/88. **Par type** : REL 51/57, 14/17, 65/74 ; SUB 42/45, 21/24, 63/69 ; GP 59/61, 33/35, 92/96.

**Point clé** : le déficit français global est un **effet de source** (le synthétique est français seulement). Sur le réel : fr **0,9688** vs en **0,9773** (p=0,72) ; le synthétique est à 0,7455. La F1 française reste plus basse **sur le réel** (0,5379 vs 0,6341) : segmentation GN/GV, pas attachement.

\## Trois découpages

| split | dev labels/exact | dev couv. | dev F1 | dev tête | test labels/exact | test couv. | test F1 | test tête |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `%3==0` | 152/152 | 0,9325 | 0,5812 | 0,7330 | 68/68 | 0,8947 | 0,5890 | 0,7337 |
| `%3==1` | 135/135 | 0,9000 | 0,5793 | 0,7297 | 85/85 | 0,9551 | 0,5908 | 0,7390 |
| `%3==2` | 153/153 | 0,9273 | 0,5900 | 0,7366 | 67/67 | 0,9054 | 0,5699 | 0,7259 |
| **étendue** | 18 (nombres) | **0,0325** | **0,0107** | **0,0069** | 18 (nombres) | **0,0603** | **0,0209** | **0,0131** |

L'exact/labels est **1,0 partout** : l'étendue du taux exact est **0**, pas 1 cas. POS : étendue 0,0055 / 0,0111. Monte-Carlo 2 000 partitions : p 0,295–0,86, toutes les étendues dans p05–p95 ; **stable**.

**Écart dev/test** : exact **0** ; couverture **+0,0378** au canonique, mais **−0,0551** et **+0,0219** aux décalés (le signe s'inverse), z=1,005, p=0,315 ; standard
… [2143 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/v10/harnais.py` | 1 | 0 |
| `/tmp/v10/construire_json.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md` | 1 | 7 |

### Commandes exécutées (échantillon)

- **T1** Show branch, HEAD and status
- **T1** List linguistique tools and reports
- **T1** Show recent commits and HEAD stat
- **T1** Find dev-test and audit reports
- **T1** Inspect v7 JSON structure
- **T1** Show diffs of the two recent corrections
- **T1** Locate the -ée correction in HEAD
- **T1** Search -ée handling and v10 JSON
- **T1** Measure canonical dev/test globally
- **T1** Check corpus counts and scipy availability
- **T1** Trace origin of -ée handling
- **T1** Inspect autotest changes in v10
- **T1** Inspect Annotation and analyser API
- **T1** Inspect annotation objects and attachment metadata
- **T1** List current lost spans with bucket
- **T1** Inspect predictions for key lost/recovered spans
- **T1** Compare living and frozen gold global metrics
- **T1** Inspect module imports and resource loading
- **T1** Check gold and module changes since audit
- **T1** Compute chi-square both ways for canonical split
- **T1** Run measurement harness
- **T1** Fix digest and rerun harness
- **T1** Find harness vs evaluer_bloc discrepancies
- **T1** Patch denominators and rerun harness
- **T1** Compare old module versions on key spans
- **T1** Compare old modules on key spans
- **T1** Print canonical detailed metrics
- **T1** Print split details, stability, MC, spans, comparison
- **T1** Measure old commits with same evaluator
- **T1** Find lexicon loading and evaluator changes
- **T1** Check gold history and diffs
- **T1** Compare old and current Heuristique classes
- **T1** Inspect tools/structures import in old module
- **T1** Replay historical commits with repo RACINE
- **T1** Compute controls, Wilson CIs, GP guard side effects
- **T1** Inspect GP guard side-effect phrases
- **T1** Print global aggregates
- **T1** Compute GN/GV F1 and three-split per-type values
- **T1** Compute per-type F1 including GN/GV
- **T1** Compute GN/GV F1 and print splits
- … et 35 autres

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 13, in <module>   File "<stdin>", line 9, in charger   File "<frozen importlib._bootstrap_external>", line 1027, in exec_module   Fil
- **T1** : dev F1 par type: [stderr] Traceback (most recent call last):   File "<stdin>", line 12, in <module>   File "/tmp/v10/harnais.py", line 227, in seg_agrege     tp = sum(sum(r["seg_type"][t]["tp"] for t 
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 16, in <module>   File "<stdin>", line 11, in f1_type KeyError: 'gold_segs' [exit code: 1]

