# Session 6e7ba93b — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-18/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `6e7ba93b-7eb8-400a-8457-6f6a8fe67f54` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-18 11:47 |
| Durée | 0.0 h |
| Tours | 1 |
| Messages | 9 |
| Appels d'outils | 9 |
| Fichiers touchés | 0 |
| Commandes | 8 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (Drave, en français). Machine dédiée. `data/` est en LECTURE SEULE.  CONTEXTE : `reports/rapport-dedup-blocs.md` vient d'établir que le dédoublonnage par blocs n'écarte rien (0 %) sur `data/corpus_wiki_fr_texte/train.txt` (7,50 Go) parce que la duplication est courte et diffuse : la mesure exacte donne **53,98 % des lignes répétées … [2657 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (Drave, en français). Machine dédiée. `data/` est en  … [2937 caractères tronqués]

*9 appels d'outils.* Actions notables :

- bash — List workspace, tools, reports, work
- bash — Inspect data dir and machine resources
- bash — Find dedup-related files
- read
- bash — Read dedup_blocs.py header and CLI
- bash — Inspect proof JSON, env, gitignore
- bash — Map functions and CLI in dedup_blocs.py
- bash — Read execute core of dedup_blocs.py
- bash — Read JSON skeleton, autotest and main

**Synthèse produite :**

⏵ Reading `dedup_blocs.py` conventions (CLI, errors, JSON)

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List workspace, tools, reports, work
- **T1** Inspect data dir and machine resources
- **T1** Find dedup-related files
- **T1** Read dedup_blocs.py header and CLI
- **T1** Inspect proof JSON, env, gitignore
- **T1** Map functions and CLI in dedup_blocs.py
- **T1** Read execute core of dedup_blocs.py
- **T1** Read JSON skeleton, autotest and main

## 4. Mesures et résultats marquants

- **T1** `/dev/mapper/system-root   11T  9,0T  1,9T  83% /home/stephane/Data13TB`
- **T1** `-rw-r--r--. 1 stephane stephane       7513 18 nov 11:11 prouve-200Mo.json`
- **T1** `-rw-r--r--. 1 stephane stephane       2237 18 nov 11:11 prouve-200Mo.log`
- **T1** `-rw-r--r--. 1 stephane stephane       1032 18 nov 11:11 prouve-200Mo.out`
- **T1** `-rw-r--r--. 1 stephane stephane  200000000 18 nov 11:11 slice-200Mo-garde.txt`
- **T1** `-rw-r--r--. 1 stephane stephane  200000000 18 nov 10:46 slice-200Mo.txt`
- **T1** `n'est coupée), plus une marge de contexte **après** le bloc (2 % du bloc, au plus`
- **T1** `1 chance sur pas (mesuré : 0,01 % de shingles vus à pas 96 contre 0,24 % avec`
- **T1** `l'ancrage, sur 20 Mo — voir `work/dedup/diagnostic_ancrage.py`). Les hachages sont`
- **T1** `"chemin": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/slice-200Mo.txt",`
- **T1** `"chemin": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/slice-200Mo-garde.txt",`
- **T1** `"recouvrement_origine": "2 % du bloc, plafonné à 1 Mio",`
- **T1** `[bloc 1] 0/191 Mio, 0.0% vu, gardé, RSS 63 Mio, 0 s`
- **T1** `[bloc 2] 8/191 Mio, 0.0% vu, gardé, RSS 79 Mio, 1 s`
- **T1** `[bloc 3] 16/191 Mio, 0.1% vu, gardé, RSS 81 Mio, 1 s`
- **T1** `[bloc 4] 24/191 Mio, 0.1% vu, gardé, RSS 90 Mio, 2 s`
- **T1** `[bloc 5] 32/191 Mio, 0.1% vu, gardé, RSS 90 Mio, 2 s`
- **T1** `[bloc 6] 40/191 Mio, 0.0% vu, gardé, RSS 90 Mio, 3 s`
- **T1** `[bloc 7] 48/191 Mio, 0.7% vu, gardé, RSS 90 Mio, 3 s`
- **T1** `[bloc 8] 56/191 Mio, 0.1% vu, gardé, RSS 97 Mio, 4 s`
- **T1** `[bloc 9] 64/191 Mio, 0.1% vu, gardé, RSS 98 Mio, 4 s`
- **T1** `[bloc 10] 72/191 Mio, 1.0% vu, gardé, RSS 107 Mio, 5 s`
- **T1** `[bloc 11] 80/191 Mio, 0.4% vu, gardé, RSS 108 Mio, 5 s`
- **T1** `[bloc 12] 88/191 Mio, 0.7% vu, gardé, RSS 110 Mio, 6 s`
- **T1** `[bloc 13] 96/191 Mio, 0.4% vu, gardé, RSS 111 Mio, 6 s`
- **T1** `[bloc 14] 104/191 Mio, 0.3% vu, gardé, RSS 112 Mio, 6 s`
- **T1** `[bloc 15] 112/191 Mio, 3.8% vu, gardé, RSS 121 Mio, 7 s`
- **T1** `[bloc 16] 120/191 Mio, 6.3% vu, gardé, RSS 121 Mio, 7 s`
- **T1** `[bloc 17] 128/191 Mio, 0.3% vu, gardé, RSS 121 Mio, 8 s`
- **T1** `[bloc 18] 136/191 Mio, 15.9% vu, gardé, RSS 121 Mio, 8 s`
- **T1** `[bloc 19] 144/191 Mio, 7.6% vu, gardé, RSS 121 Mio, 9 s`
- **T1** `[bloc 20] 152/191 Mio, 2.8% vu, gardé, RSS 121 Mio, 9 s`
- **T1** `[bloc 21] 160/191 Mio, 3.7% vu, gardé, RSS 121 Mio, 10 s`
- **T1** `[bloc 22] 168/191 Mio, 1.3% vu, gardé, RSS 121 Mio, 10 s`
- **T1** `[bloc 23] 176/191 Mio, 0.3% vu, gardé, RSS 121 Mio, 11 s`
- **T1** `[bloc 24] 184/191 Mio, 0.6% vu, gardé, RSS 121 Mio, 11 s`
- **T1** `Command being timed: "python3 tools/dedup_blocs.py --entree work/dedup/slice-200Mo.txt --sortie work/dedup/slice-200Mo-garde.txt --bloc-mo 8 --memoire-mo 256 --json work/dedup/prouve-200Mo.json"`
- **T1** `Percent of CPU this job got: 97%`
- **T1** `rec_origine = "2 % du bloc, plafonné à 1 Mio"`
- **T1** `"""Remplace `fraction` des mots par d'autres, dispersés : la copie « 10 % modifiée »."""`
- **T1** `# C : un paragraphe sur dix remplacé → ≈ 9,4 % des octets neufs, uniformément par bloc`
- **T1** `# seuil 0,95 : C (≈ 90 % vu) repasse`
- **T1** `# 10 % dispersé : les shingles sont locaux, la copie est gardée`
- **T1** `"(défaut : 2 %% du bloc, max 1 Mio)")`

