# Session bf49d867 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `bf49d867-4b23-49e1-b214-9a2fd542fb1b` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 11:17 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 18 |
| Appels d'outils | 17 |
| Fichiers touchés | 0 |
| Commandes | 9 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **diagnostiquer la POS anglaise** et proposer des correctifs mesurés, sans modifier le code.  Contexte : `tools/bloc_linguistique.py` (`_pos`, `POS_FERME`, `VERBES`, `ADJECTIFS`, la règle de contexte DET/PRÉP/ADJ → nom), `tools/tests/linguistique/evaluer_gold.py` (`evaluer_bloc`). État : P … [1858 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **diagnost … [2138 caractères tronqués]

*17 appels d'outils.* Actions notables :

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

**Synthèse produite :**

⏵ Computing the dev/test split and conditional gold statistics

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

