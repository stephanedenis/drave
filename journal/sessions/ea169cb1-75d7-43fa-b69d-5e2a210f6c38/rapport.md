# Session ea169cb1 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `ea169cb1-75d7-43fa-b69d-5e2a210f6c38` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 23:24 |
| Durée | 1.1 h |
| Tours | 1 |
| Messages | 102 |
| Appels d'outils | 118 |
| Fichiers touchés | 1 |
| Commandes | 99 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer l'état v10** (commit `710ec7f9`) et vérifier que ses chiffres, ses règles et ses portes sont justes.  Contexte : `tools/bloc_linguistique.py` (`Heuristique`, `_syntagmes_simple`, `est_verbe` avec garde PRON, `est_sub`, boucle REL/SUB avec `predicat_vu`, `_est_verbe` avec `-ée`),  … [1903 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer  … [2183 caractères tronqués]

*118 appels d'outils.* Actions notables :

- bash — Check git status, branch, recent commits
- bash — List relevant reports and test dirs
- read
- bash — Dump v10 and v9 JSON
- bash — Find v10 generation references
- bash — Find where aggregate metrics are computed
- bash — Search for F1 union protocol references
- bash — Find F1 union harness references
- bash — Search chunker and union in test tools
- bash — Outline bloc_linguistique
- bash — Check for previous audit harness
- bash — Inspect audit JSON structure
- bash — Inspect v10 commit diff
- bash — Verify module matches audited commit
- … et 87 autres

**Synthèse produite :**

⏵ Verifying gate docstrings at the audited commit

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v10.md` | 1 | 1 |

### Commandes exécutées (échantillon)

- **T1** Check git status, branch, recent commits
- **T1** List relevant reports and test dirs
- **T1** Dump v10 and v9 JSON
- **T1** Find v10 generation references
- **T1** Find where aggregate metrics are computed
- **T1** Search for F1 union protocol references
- **T1** Find F1 union harness references
- **T1** Search chunker and union in test tools
- **T1** Outline bloc_linguistique
- **T1** Check for previous audit harness
- **T1** Inspect audit JSON structure
- **T1** Inspect v10 commit diff
- **T1** Verify module matches audited commit
- **T1** Check where -ée rule was introduced
- **T1** Trace introduction of -ée rule
- **T1** Diff v8 to v9 module
- **T1** Check -ée commit and buy lexicon
- **T1** Measure official baseline values
- **T1** Probe -ée rule and lexicon
- **T1** Inspect key phrases
- **T1** Inspect autotest runner
- **T1** Benchmark 50 analyses
- **T1** Run autotest gates
- **T1** Check split membership of key ids
- **T1** Check gold file counts and split source
- **T1** Check module RACINE definition
- **T1** Run full audit measurements
- **T1** Re-run harness after fixes
- **T1** Show baseline and controls
- **T1** Read prior negative control JSON
- **T1** Show ablation details
- **T1** Check prior control code and gates
- **T1** Compare span sets v8 v9 v10
- **T1** Find prior top-k permutation code
- **T1** Official F1 on both golds
- **T1** List -ée words and their verb status
- **T1** Show r303 segmentation across versions
- **T1** Measure v9/v10 F1 modes
- **T1** Check -ée presence in v8/v9 commits
- **T1** Check if details saved
- … et 59 autres

## 4. Mesures et résultats marquants

- **T1** `data/corpus_en.txt:159500:Although the Amazon river remains undammed, around 412 dams are in operation on the Amazon's tributary rivers. Of these 412 dams, 151 are constructed over six of the main tri`
- **T1** `"lecture": "0.908 % moyen contre 100.0 % observé"`
- **T1** `"lecture": "0,96 % en moyenne contre 100 % observe"`
- **T1** `"lecture": "35,9 % en moyenne contre 100 % observe"`
- **T1** `"lecture": "0,85 % en moyenne contre 83,49 % observe"`

## 5. Erreurs rencontrées

4 sorties en erreur ou divergentes. Les premières :

- **T1** : Error: spawn bash ENOENT
- **T1** : Error: spawn bash ENOENT
- **T1** : {  "chiffres_rejoues": true,  "ecarts_chiffres": 2,  "regles_justes": false,  "portes": "183/183",  "resume": "Les valeurs v10 rejouent (220/220, 0,9205, 0,5880, 0,7388, 134/134, 86/86, 19 spans, top-
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 5, in <module> ValueError: invalid literal for int() with base 10: '1_rejeu' [exit code: 1]

