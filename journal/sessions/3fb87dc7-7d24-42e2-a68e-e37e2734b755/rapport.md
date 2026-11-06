# Session 3fb87dc7 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `3fb87dc7-7d24-42e2-a68e-e37e2734b755` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 23:24 |
| Durée | 1.6 h |
| Tours | 1 |
| Messages | 74 |
| Appels d'outils | 81 |
| Fichiers touchés | 3 |
| Commandes | 68 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **re-mesurer dev/test sur l'état v10** (commit `710ec7f9`) et éprouver la robustesse du split.  Contexte : `tools/tests/linguistique/gold_split.py` (`dev`, `test`, `compter`), `evaluer_gold.py` (`charger`, `evaluer_bloc`), `bloc_linguistique.py`. Les valeurs publiées 152/152 (dev) et 67/67 … [1406 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **re-mesur … [1686 caractères tronqués]

*81 appels d'outils.* Actions notables :

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
- … et 61 autres

**Synthèse produite :**

⏵ Le parent a commité l'essai (HEAD 653a7981) — vérification de l'état courant

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/v10/harnais.py` | 1 | 0 |
| `/tmp/v10/construire_json.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md` | 1 | 3 |

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
- … et 28 autres

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 13, in <module>   File "<stdin>", line 9, in charger   File "<frozen importlib._bootstrap_external>", line 1027, in exec_module   Fil
- **T1** : dev F1 par type: [stderr] Traceback (most recent call last):   File "<stdin>", line 12, in <module>   File "/tmp/v10/harnais.py", line 227, in seg_agrege     tp = sum(sum(r["seg_type"][t]["tp"] for t 
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 16, in <module>   File "<stdin>", line 11, in f1_type KeyError: 'gold_segs' [exit code: 1]

