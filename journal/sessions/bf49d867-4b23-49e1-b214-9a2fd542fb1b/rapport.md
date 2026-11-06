# Session bf49d867 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `bf49d867-4b23-49e1-b214-9a2fd542fb1b` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 11:17 |
| Durée | 0.7 h |
| Tours | 1 |
| Messages | 35 |
| Appels d'outils | 34 |
| Fichiers touchés | 0 |
| Commandes | 26 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **diagnostiquer la POS anglaise** et proposer des correctifs mesurés, sans modifier le code.  Contexte : `tools/bloc_linguistique.py` (`_pos`, `POS_FERME`, `VERBES`, `ADJECTIFS`, la règle de contexte DET/PRÉP/ADJ → nom), `tools/tests/linguistique/evaluer_gold.py` (`evaluer_bloc`). État : P … [1858 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **diagnost … [2138 caractères tronqués]

*34 appels d'outils.* Actions notables :

- bash — Check repo state and branch
- bash — List repo and tools directories
- bash — List test harness directories
- grep
- read
- bash — Inspect gold dataset composition
- bash — Run gold evaluation baseline
- bash — Print baseline POS metrics
- bash — Diagnose English POS errors
- bash — Decompose EN errors by mechanism
- bash — Compute dev/test split and conditional stats
- bash — Audit rule risks on gold
- bash — Run POS rule variants on dev and test
- bash — Fix patch anchor and rerun variants
- … et 14 autres

**Synthèse produite :**

⏵ Locating the R2s break and residual EN errors with sentence context

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Check repo state and branch
- **T1** List repo and tools directories
- **T1** List test harness directories
- **T1** Inspect gold dataset composition
- **T1** Run gold evaluation baseline
- **T1** Print baseline POS metrics
- **T1** Diagnose English POS errors
- **T1** Decompose EN errors by mechanism
- **T1** Compute dev/test split and conditional stats
- **T1** Audit rule risks on gold
- **T1** Run POS rule variants on dev and test
- **T1** Fix patch anchor and rerun variants
- **T1** Token-level fixes and breaks per rule
- **T1** Debug R3 brother/mother breaks
- **T1** Fix R3 lookahead and rerun
- **T1** Print full metrics table
- **T1** Check split membership and branch counts
- **T1** Run final measurement script
- **T1** Inspect breaks and transitions
- **T1** Inspect flowers/books breaks
- **T1** Inspect R2S patch text
- **T1** Instrument R2s on the break phrases
- **T1** Trace R2s decisions
- **T1** Rerun measurements with reordered R2s
- **T1** List breaks and residual errors
- **T1** Print breaks and residual list from file

## 4. Mesures et résultats marquants

- **T1** `ADJ   n=  40 ok=  24 (60.0%)  NOUN:12  VERB:4`
- **T1** `ADV   n=  34 ok=  17 (50.0%)  NOUN:15  PREP:1  ?:1`
- **T1** `AUX   n=  61 ok=  60 (98.4%)  NOUN:1`
- **T1** `CONJ  n=  36 ok=  22 (61.1%)  DET:12  NOUN:2`
- **T1** `DET   n= 213 ok= 213 (100.0%)`
- **T1** `NOUN  n= 248 ok= 238 (96.0%)  ADJ:5  VERB:5`
- **T1** `NUM   n=   1 ok=   1 (100.0%)`
- **T1** `PONCT n=   3 ok=   0 (0.0%)  ?:3`
- **T1** `PREP  n=  43 ok=  43 (100.0%)`
- **T1** `PRON  n= 200 ok= 177 (88.5%)  DET:14  NOUN:8  CONJ:1`
- **T1** `VERB  n= 269 ok=  83 (30.9%)  NOUN:176  ADJ:5  AUX:4  ?:1`
- **T1** `VERB   186 (68.9%)`
- **T1** `PRON    23 (8.5%)`
- **T1** `ADV     17 (6.3%)`
- **T1** `ADJ     16 (5.9%)`
- **T1** `CONJ    14 (5.2%)`
- **T1** `NOUN    10 (3.7%)`
- **T1** `PONCT    3 (1.1%)`
- **T1** `AUX      1 (0.4%)`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : V0 dev 0.7547 test 0.7656 | dev_en 0.7528 test_en 0.7925 [stderr] Traceback (most recent call last):   File "/tmp/qpos/sim.py", line 125, in <module>     mod = charger('bl_' + nom.replace('+','_'), pa

