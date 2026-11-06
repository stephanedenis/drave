# Session ea169cb1 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `ea169cb1-75d7-43fa-b69d-5e2a210f6c38` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 23:24 |
| Durée | 1.3 h |
| Tours | 1 |
| Messages | 120 |
| Appels d'outils | 136 |
| Fichiers touchés | 1 |
| Commandes | 116 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer l'état v10** (commit `710ec7f9`) et vérifier que ses chiffres, ses règles et ses portes sont justes.  Contexte : `tools/bloc_linguistique.py` (`Heuristique`, `_syntagmes_simple`, `est_verbe` avec garde PRON, `est_sub`, boucle REL/SUB avec `predicat_vu`, `_est_verbe` avec `-ée`),  … [1903 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer  … [2183 caractères tronqués]

*136 appels d'outils.* Actions notables :

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
- … et 105 autres

**Synthèse produite :**

⏵ Clôture de l'audit et résumé final

Audit terminé. Deux fichiers neufs écrits :

- [`reports/rapport-audit-v10.md`](reports/rapport-audit-v10.md)
- [`reports/pensee-audit-v10.json`](reports/pensee-audit-v10.json)

Aucun fichier existant modifié par moi, aucun commit de ma part.

\## Valeurs rejouées (commit `710ec7f9`)

| grandeur | fiche | vivant 612 | gelé 602 |
|---|---:|---:|---:|
| labels / exact | 220 / 220 (1,0000) | **220 / 220** | **220 / 220** |
| couverture | 0,9205 | **0,9205** | **0,9205** |
| F1 union | 0,5880 | 0,5836 | **0,5880** |
| S / chunker | 0,5014 / 0,6203 | 0,4957 / 0,6163 | **0,5014 / 0,6203** |
| tête | 0,7388 | 0,7332 | **0,7388** |
| fr / en | 134/134, 86/86 | **idem** | **idem** |
| spans | 19 (9 REL, 6 SUB, 4 GP) | **19** | **19** |
| top-k | 219 (0,9163) | **219** | **219** |

**Écarts**
1. Le F1 « avant » **0,5822** est la valeur du **vivant 612**, pas du gelé ; le **gelé v9 vaut 0,5866**. Le gain v9→v10 est **+0,0014**, pas +0,0058.
2. Le **test courant v10 est 68/68** (0,8947), pas 67/67 (le 67/67 est la v9).

\## Règles

Le commit `710ec7f9` ne modifie, dans le bloc, que la **garde DET du GP** : **+1 exact (`r153`, test)**, 0 perte. Le **`-ée` est antérieur** (`a408a909`, déjà dans v8/v9) et **totalement inerte** : 0 différence d'annotation sur 612 phrases ; `r255` reste absent car `acheter` n'est pas dans `VERBES_CONNUS`.

\## Ablations (base 220 ; F1 gelé)

| ablation | exact | Δ | gains / pertes | F1 |
|---|---:|---:|---|---:|
| garde PRON retirée | 203 | **−17** | 17 gains, 0 perte | 0,5718 (−0,0162) |
| expansion SUJETS retirée | 214 | **−6** | 6 gains (r273 s032 s069 s072 s115 s135) | 0,5833 |
| PRON + SUJETS retirées | 214 | **−6** | mêmes 6 gains ; garde inerte sans expansion | 0,5808 |
| `est_sub` retiré | 219 | **−1** | r280 | 0,5849 |
| `predicat_vu` retiré | 220 | **0** | gagne g017, perd r303 | 0,5880 |
| `-ée` retiré | 220 | **0** | 0 / 0 | 0,5880 |
| garde DET GP retirée | 219 | **−1** | r153 | 0,5866 |

**Les 19 spans** = **17 résiduels A17 + `s037` + `r303`**. La fiche « 17 inatteignables + r255 + r264 » double compte r255/r264 et omet s037/r303. `r303` est la perte cachée de `predicat_vu` (net 0 avec g017) ; `s037` est la 7e régression v8, toujours ouverte.

\## dev/test

| moitié | v8 | v9 | **v10** |
|---|---:|---:|---:|
| dev | 148/148 | 152/152 | **152/152** (0,9325) |
| test | 64/64 | 67/67 | **68/68** (0,8947) |

Le +1 test est `r153` ; le `-ée` n'ajoute rien.

\## Contrôles et portes

- Permutation g
… [779 caractères tronqués]

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
- … et 76 autres

## 4. Mesures et résultats marquants

- **T1** `data/corpus_en.txt:159500:Although the Amazon river remains undammed, around 412 dams are in operation on the Amazon's tributary rivers. Of these 412 dams, 151 are constructed over six of the main tri`
- **T1** `"lecture": "0.908 % moyen contre 100.0 % observé"`
- **T1** `"lecture": "0,96 % en moyenne contre 100 % observe"`
- **T1** `"lecture": "35,9 % en moyenne contre 100 % observe"`
- **T1** `"lecture": "0,85 % en moyenne contre 83,49 % observe"`
- **T1** `candidats laisse 1,17 % de réussite, le top-1 aléatoire 42,14 % ; les deux donnent p = 0.`

## 5. Erreurs rencontrées

4 sorties en erreur ou divergentes. Les premières :

- **T1** : Error: spawn bash ENOENT
- **T1** : Error: spawn bash ENOENT
- **T1** : {  "chiffres_rejoues": true,  "ecarts_chiffres": 2,  "regles_justes": false,  "portes": "183/183",  "resume": "Les valeurs v10 rejouent (220/220, 0,9205, 0,5880, 0,7388, 134/134, 86/86, 19 spans, top-
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 5, in <module> ValueError: invalid literal for int() with base 10: '1_rejeu' [exit code: 1]

