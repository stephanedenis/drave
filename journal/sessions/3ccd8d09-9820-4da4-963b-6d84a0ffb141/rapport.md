# Session 3ccd8d09 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `3ccd8d09-9820-4da4-963b-6d84a0ffb141` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 18:33 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 12 |
| Appels d'outils | 16 |
| Fichiers touchés | 0 |
| Commandes | 14 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **réparer les frontières de phrase** du bloc linguistique (P0-4 de l'audit produit `reports/rapport-fiabilite-produit.md`), sans modifier le code du dépôt.  Contexte : `tools/bloc_linguistique.py` (`Heuristique._phrases`, `_mots`, `_langue`), `tools/drave.py` (CLI), les audits `reports/rap … [1962 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **réparer  … [2242 caractères tronqués]

*16 appels d'outils.* Actions notables :

- bash — Inspect repo status and branch
- bash — Check sizes of target files
- bash — Locate Heuristique methods
- bash — Find P0-4 section in audit
- read
- bash — Find evaluation harness for syntagmes
- bash — Find dev/test harness scripts
- bash — Read bloc L report intro
- bash — Read P0-4 and boundaries details
- bash — Inspect gold evaluation tooling
- bash — Read rest of evaluator and split logic
- bash — Inspect gold structure
- bash — Check phrase tests in gold tooling
- bash — Check imports and Python version
- … et 1 autres

**Synthèse produite :**

⏵ Lecture du bloc linguistique et des audits

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Inspect repo status and branch
- **T1** Check sizes of target files
- **T1** Locate Heuristique methods
- **T1** Find P0-4 section in audit
- **T1** Find evaluation harness for syntagmes
- **T1** Find dev/test harness scripts
- **T1** Read bloc L report intro
- **T1** Read P0-4 and boundaries details
- **T1** Inspect gold evaluation tooling
- **T1** Read rest of evaluator and split logic
- **T1** Inspect gold structure
- **T1** Check phrase tests in gold tooling
- **T1** Check imports and Python version
- **T1** Probe current sentence splitting

## 4. Mesures et résultats marquants

- **T1** `39:| temps CLI (50 phrases) | **136,8–226,6 ms**, médiane **152,7 ms** |`
- **T1** `157:phrase courte, **plus de 95 % du temps CLI est le démarrage**, pas l'analyse (0,8 ms pour f01).`
- **T1** `219:| 10 000 car., phrases répétées | 0 | **590–765 ms** | 10 362 | **2 763 666 o** | spans valides, déterminisme |`
- **T1** `| graphème, mot | ✅ | 0 crash, 0 span hors texte, `valeur = texte[debut:fin]` à **100 %**, couverture **49/50 à 100 %** (x46 : 95,14 %, newlines) |`
- **T1** ``reel_new` + 160 `synthétique`), soit **100 %**. Sur `all` : **612/612**.`
- **T1** `langue=und script=Latn source=heuristique · 13 étiquettes · unités sémantiques=2 (85.7% du texte)`
- **T1** `| **P1-7** | **Compacité et lot** : `--compact`, JSONL, `--fichier`/stdin | **2,76 Mo** pour 10 k ; **11,5 Mo** pour 50 k ; 1 texte par appel | `drave.py` 50-52, 329-341 | **0,5–1 j** | faible : optio`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : #!/usr/bin/env python3 """bloc_linguistique.py — le bloc d'étiquetage linguistique, du graphème à la pragmatique.  Un seul contrat (`BlocLinguistique.analyser`) et **plusieurs implémentations** :    -

