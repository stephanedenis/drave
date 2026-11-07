# Session 3ccd8d09 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `3ccd8d09-9820-4da4-963b-6d84a0ffb141` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 18:33 |
| Durée | 1.4 h |
| Tours | 1 |
| Messages | 83 |
| Appels d'outils | 89 |
| Fichiers touchés | 0 |
| Commandes | 87 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **réparer les frontières de phrase** du bloc linguistique (P0-4 de l'audit produit `reports/rapport-fiabilite-produit.md`), sans modifier le code du dépôt.  Contexte : `tools/bloc_linguistique.py` (`Heuristique._phrases`, `_mots`, `_langue`), `tools/drave.py` (CLI), les audits `reports/rap … [1962 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **réparer  … [2242 caractères tronqués]

*89 appels d'outils.* Actions notables :

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
- … et 74 autres

**Synthèse produite :**

⏵ Finalisation des deux patchs et test sur le gold

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
- **T1** Inspect audit JSON keys
- **T1** Find boundary data in audit JSON
- **T1** Inspect 50-text bench data
- **T1** Read audit boundary case texts
- **T1** Read CLI implementation head
- **T1** Read existing linguistic tests
- **T1** Find sentence tests and gate
- **T1** Inspect markdown and no punctuation texts
- **T1** Check newlines in gold
- **T1** Check ellipses in gold
- **T1** Check closing punctuation in gold
- **T1** Check multi-sentence gold entries
- **T1** Inspect multi-sentence gold entries
- **T1** Probe current tokenization
- **T1** Check digits in gold
- **T1** Check abbreviations in gold
- **T1** Check questions in gold
- **T1** Check exclamations and non-final questions
- **T1** Benchmark gold evaluation time
- **T1** Prototype sentence boundary rules
- **T1** Debug URL final period protection
- **T1** Patch prototype and rerun
- **T1** Debug e.g. protection
- **T1** Fix dotted abbreviation zone
- **T1** Create 40-text corpus with expected spans
- **T1** Validate patched splitter on 40 texts
- … et 47 autres

## 4. Mesures et résultats marquants

- **T1** `39:| temps CLI (50 phrases) | **136,8–226,6 ms**, médiane **152,7 ms** |`
- **T1** `157:phrase courte, **plus de 95 % du temps CLI est le démarrage**, pas l'analyse (0,8 ms pour f01).`
- **T1** `219:| 10 000 car., phrases répétées | 0 | **590–765 ms** | 10 362 | **2 763 666 o** | spans valides, déterminisme |`
- **T1** `| graphème, mot | ✅ | 0 crash, 0 span hors texte, `valeur = texte[debut:fin]` à **100 %**, couverture **49/50 à 100 %** (x46 : 95,14 %, newlines) |`
- **T1** ``reel_new` + 160 `synthétique`), soit **100 %**. Sur `all` : **612/612**.`
- **T1** `langue=und script=Latn source=heuristique · 13 étiquettes · unités sémantiques=2 (85.7% du texte)`
- **T1** `| **P1-7** | **Compacité et lot** : `--compact`, JSONL, `--fichier`/stdin | **2,76 Mo** pour 10 k ; **11,5 Mo** pour 50 k ; 1 texte par appel | `drave.py` 50-52, 329-341 | **0,5–1 j** | faible : optio`
- **T1** `f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"`
- **T1** `baseline phrases 923 temps 2.98 ms`
- **T1** `patch phrases 462 temps 8.47 ms`
- **T1** `baseline 4101 12.96 ms`
- **T1** `patch 1029 8.97 ms`

## 5. Erreurs rencontrées

6 sorties en erreur ou divergentes. Les premières :

- **T1** : #!/usr/bin/env python3 """bloc_linguistique.py — le bloc d'étiquetage linguistique, du graphème à la pragmatique.  Un seul contrat (`BlocLinguistique.analyser`) et **plusieurs implémentations** :    -
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 2, in <module> ModuleNotFoundError: No module named 'bloc_linguistique' [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 2, in <module> ModuleNotFoundError: No module named 'corpus' [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 2, in <module>   File "/tmp/frontieres/final/patch_frontieres.py", line 27, in <module>     _MARQUEUR = re.compile(                 ^
- **T1** : (no output) [exit code: 2]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 3, in <module>   File "<frozen importlib._bootstrap_external>", line 1027, in exec_module   File "<frozen importlib._bootstrap>", lin

