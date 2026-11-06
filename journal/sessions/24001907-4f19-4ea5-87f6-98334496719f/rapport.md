# Session 24001907 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `24001907-4f19-4ea5-87f6-98334496719f` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 19:25 |
| Durée | 1.2 h |
| Tours | 1 |
| Messages | 93 |
| Appels d'outils | 126 |
| Fichiers touchés | 1 |
| Commandes | 86 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer l'état v7 de l'attachement** (commit `69bd865e`) et vérifier que ses chiffres et ses portes sont justes.  Contexte : `tools/bloc_linguistique.py` (classe `Heuristique`, `_syntagmes_simple`, `_cible_precedent`, `_cible_hors_span`), `tools/tests/linguistique/evaluer_gold.py` (`char … [2193 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer  … [2473 caractères tronqués]

*126 appels d'outils.* Actions notables :

- bash — Inspect git HEAD and status
- bash — List reports and relevant tool dirs
- read
- bash — Count lines of key files
- bash — Run gold evaluator and save JSON
- bash — Inspect gold sizes and dev/test split
- bash — Extract measured metrics per source
- bash — Compare living gold vs frozen gold
- bash — Locate cited gate definitions
- bash — Inspect autotest structure and gates count
- bash — Find gate function definitions
- bash — Run autotest gates
- bash — Read bloc_linguistique header and classes
- job_output
- … et 89 autres

**Synthèse produite :**

⏵ Recherche de résidus d'erreurs dans la fiche

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `reports/rapport-audit-v7.md` | 1 | 14 |

### Commandes exécutées (échantillon)

- **T1** Inspect git HEAD and status
- **T1** List reports and relevant tool dirs
- **T1** Count lines of key files
- **T1** Run gold evaluator and save JSON
- **T1** Inspect gold sizes and dev/test split
- **T1** Extract measured metrics per source
- **T1** Compare living gold vs frozen gold
- **T1** Locate cited gate definitions
- **T1** Inspect autotest structure and gates count
- **T1** Find gate function definitions
- **T1** Run autotest gates
- **T1** Read bloc_linguistique header and classes
- **T1** Run autotest as module
- **T1** Locate key heuristic functions
- **T1** Locate Heuristique class
- **T1** Extract cited gate outputs
- **T1** Check gate totals
- **T1** List coverage reports and history
- **T1** Inspect v7 and upstream commits
- **T1** Read v6 sheet and JSON
- **T1** Compare v5 sheet versions
- **T1** Compare v4 sheet versions
- **T1** Read upstream JSONs
- **T1** Measure all metrics across golds and splits
- **T1** Measure S and chunker on living/frozen gold
- **T1** Create local copy of bloc_linguistique for ablations
- **T1** Run POS and previous-segment ablations
- **T1** Run ablations with proper module registration
- **T1** Find dev/test and v7 value gates
- **T1** Inspect v7 code changes
- **T1** Measure v6 code on living and frozen gold
- **T1** Remeasure v6 with correct root
- **T1** Search where before-values appear
- **T1** Check v6 JSON for POS/head
- **T1** Run target permutation and random candidate controls
- **T1** Check whether gold changed since v4/v5
- **T1** Extract v4 and v5 heuristic code
- **T1** Inspect gold split commit changes
- **T1** Replay v4/v5/v6/v7 code on golds
- **T1** Measure v4/v5 component F1 values
- … et 46 autres

## 4. Mesures et résultats marquants

- **T1** `- **Le mélange des types varie** : le test canonique est **REL-pauvre** (17 cibles, 22,4 %, contre`
- **T1** `35,0 % en dev) et **GP-riche** (35, 46,1 %, contre 37,4 %) ; l'attendu serait 23,5 REL et 30,5 GP.`
- **T1** `Ce n'est pas significatif (p=0,26), mais les décalés ne donnent pas le même mélange : test REL 34,8 %`
- **T1** `(décalé 1) et 35,1 % (décalé 2). C'est le principal levier des variations agrégées ci-dessous.`
- **T1** `Toutes les étendues observées sont dans la bande 95 % du tirage aléatoire. **Conclusion : le split est`
- **T1** `sous dev, ~2,7 cas pour 76), mais cette estimation n'est pas significative : les IC Wilson 95 % se`
- **T1** `- **F1** : test **+1,39 point**, mais l'agrégat est dominé par GN/GV (81 % des segments) : GV test`
- **T1** `aucun résidu 0.7919`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : sans_pos : bloc retiré 807 caractères sans_precedent : 3 sites retirés [stderr] Traceback (most recent call last):   File "<stdin>", line 15, in <module>   File "<stdin>", line 10, in charger_module  

