# Session c27ff712 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `c27ff712-ac49-4750-90d4-76f59bedb5ca` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 19:25 |
| Durée | 0.4 h |
| Tours | 1 |
| Messages | 28 |
| Appels d'outils | 31 |
| Fichiers touchés | 2 |
| Commandes | 23 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **re-mesurer le split dev/test** sur l'état v7 (commit `69bd865e`) et éprouver sa robustesse.  Contexte : `tools/tests/linguistique/gold_split.py` (`dev`, `test`, `compter`), `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bloc`), `tools/bloc_linguistique.py`. La fiche `rep … [1490 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **re-mesur … [1770 caractères tronqués]

*31 appels d'outils.* Actions notables :

- bash — Check git status and current commit
- bash — List test and reports directories
- bash — List linguistique tools and gold reports
- read
- bash — Find usages of gold_split
- bash — Inspect gold JSON structure and v7 reports
- bash — Search REL/SUB/GP handling
- bash — Read v7 and v5 coverage JSON
- bash — Inspect gold stats and benchmark evaluator
- write `/tmp/mesure_dev_test_v7.py`
- bash — Run dev/test measurement script
- bash — Find v7 metric definitions
- bash — Confirm working tree matches commit for bloc_linguistique
- bash — Compare frozen and living gold
- … et 12 autres

**Synthèse produite :**

⏵ Contrôle des croisements source×langue et F1 par langue

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/mesure_dev_test_v7.py` | 1 | 0 |
| `/tmp/enrichir.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Check git status and current commit
- **T1** List test and reports directories
- **T1** List linguistique tools and gold reports
- **T1** Find usages of gold_split
- **T1** Inspect gold JSON structure and v7 reports
- **T1** Search REL/SUB/GP handling
- **T1** Read v7 and v5 coverage JSON
- **T1** Inspect gold stats and benchmark evaluator
- **T1** Run dev/test measurement script
- **T1** Find v7 metric definitions
- **T1** Confirm working tree matches commit for bloc_linguistique
- **T1** Compare frozen and living gold
- **T1** Fix absent-category check and rerun
- **T1** Print detailed canonical and shifted metrics
- **T1** Identify attachment failure and lost spans
- **T1** Inspect id formats by source
- **T1** Check size of intermediate JSON
- **T1** F1 by all segment types for dev/test
- **T1** Run enrichment and statistical controls
- **T1** Check scipy availability
- **T1** Rerun enrichment with scipy chi2
- **T1** Summarize enriched results for report writing
- **T1** Check source-language and source-type cross balance

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : nettoyé par phrase : 239 cibles, 196 labels, 195 exact — ok Monte-Carlo : {  "exact_taux_span": {   "observe_3_splits": [    1.0,    1.0,    0.9828   ],   "observe_etendue": 0.0172,   "monte_carlo_ete

