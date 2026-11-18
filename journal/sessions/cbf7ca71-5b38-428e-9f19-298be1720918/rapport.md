# Session cbf7ca71 — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-18/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `cbf7ca71-5b38-428e-9f19-298be1720918` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-18 10:17 |
| Durée | 0.6 h |
| Tours | 1 |
| Messages | 59 |
| Appels d'outils | 59 |
| Fichiers touchés | 2 |
| Commandes | 47 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (Drave, en français). Machine dédiée (40 threads, 125 Go RAM). NE TOUCHE PAS à `data/` (lecture seule).  CONTEXTE : l'inventaire `reports/rapport-donnees-inventaire.md` a montré que `data/corpus_wiki_fr_texte/train.txt` fait **7,50 Go** et pourrait fermer l'écart du palier 1, MAIS l'outil actuel `tools/corpus_propre.py` tient tous  … [2581 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (Drave, en français). Machine dédiée (40 threads, 125 … [2861 caractères tronqués]

*59 appels d'outils.* Actions notables :

- bash — List workspace structure
- bash — Inspect data corpus size and disk
- bash — Check inventory report and corpus tool
- bash — Inspect beginning of train corpus
- read
- bash — Check Python, numpy, hardware, work dir
- bash — List related reports and style sample
- bash — Create 200MB slice for benchmarks
- bash — Measure Python set memory per entry
- bash — Benchmark pure-Python shingle hashing
- bash — Check git state, ignore rules, time binary
- bash — Micro-benchmark hash extraction variants
- bash — Check JSON manifest style and named-error conventions
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py`
- … et 41 autres

**Synthèse produite :**

⏵ Launching the full 7.5 GB pass in the background

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py` | 2 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/diagnostic_ancrage.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** List workspace structure
- **T1** Inspect data corpus size and disk
- **T1** Check inventory report and corpus tool
- **T1** Inspect beginning of train corpus
- **T1** Check Python, numpy, hardware, work dir
- **T1** List related reports and style sample
- **T1** Create 200MB slice for benchmarks
- **T1** Measure Python set memory per entry
- **T1** Benchmark pure-Python shingle hashing
- **T1** Check git state, ignore rules, time binary
- **T1** Micro-benchmark hash extraction variants
- **T1** Check JSON manifest style and named-error conventions
- **T1** Smoke test on 3 MB slice
- **T1** Run the autotest (negative control)
- **T1** Re-run the autotest
- **T1** Inspect first autotest cases
- **T1** Inspect per-block journal of control run
- **T1** Check whether identical blocks hash identically
- **T1** Inspect the hashing/insertion code
- **T1** Instrument the loop to find the insertion bug
- **T1** Compare fixed-grid vs line-anchored shingle duplication
- **T1** Word-anchored and stride-1 duplication ceiling
- **T1** True duplicate rate vs anchoring on 20 MB
- **T1** Measure anchor density and seen rate on 200 MB
- **T1** Run the autotest with content-defined anchors
- **T1** Run tool directly to see the traceback
- **T1** Regenerate control files and run directly
- **T1** Re-run the autotest after fixing nonlocal
- **T1** Measure real set memory cost per entry
- **T1** Replace calibration with measured constant
- **T1** Re-run autotest after memory model change
- **T1** Run 200 MB proof with 256 MiB budget
- **T1** Measure RSS by block size on 1 MB
- **T1** Profile allocations with tracemalloc
- **T1** Time normalization, hashing, anchoring separately
- **T1** Instrument RSS by phase
- **T1** Compare regex normalization memory
- **T1** Fix normalization memory and re-test 200 MB
- **T1** Inspect 200 MB proof JSON
- **T1** Add within-block-inclusive metric and re-run 200 MB
- … et 7 autres

## 4. Mesures et résultats marquants

- **T1** `/dev/mapper/system-root   11T  9,0T  1,9T  83% /home/stephane/Data13TB`
- **T1** `"split": "hash salé (graine 1) de page_id : 5% val, 5% test"`
- **T1** `recouvrement de contexte en Mio (défaut : 2 % du bloc,`
- **T1** `{'budget_mio': 512.0, 'plancher_mio': 80.3, 'bloc_mio': 0.06, 'recouvrement_octets': 1310, 'recouvrement_origine': '2 % du bloc, plafonné à 1 Mio', 'cout_entree': {'table_octets_entree': 104.9, 'entie`
- **T1** `grille pas=96 : 2083333 shingles, 27942 vus (1.34 %) en 2.7s`
- **T1** `grille pas=48 : 4166665 shingles, 64493 vus (1.55 %) en 5.4s`
- **T1** `lignes        : 1741348 shingles, 48527 vus (2.79 %) en 2.6s`
- **T1** `ancrage mots  : 7596803 shingles, 23735 vus (0.31 %) en 12.5s`
- **T1** `stride 1 (/8) : 6249988 shingles, 5080 vus (0.08 %) en 19.5s`
- **T1** `tous, hash 1/16: 1249191 éch., 3035 vus (0.24 %) en 21.8s`
- **T1** `grille 96      : 208333 éch., 17 vus (0.01 %) en 0.3s`
- **T1** `grille 48      : 416665 éch., 57 vus (0.01 %) en 0.5s`
- **T1** `lignes         : 145317 éch., 462 vus (0.32 %) en 0.2s`
- **T1** `débuts de ligne seuls: 1279914 ancres (0.006/octet), 34632 vus (2.71 %), 2.5s`
- **T1** `lignes + pas 192: 1905640 ancres (0.010/octet), 49546 vus (2.60 %), 3.6s`
- **T1** `lignes + pas 96: 2829425 ancres (0.014/octet), 70820 vus (2.50 %), 5.1s`
- **T1** `lignes + pas 48: 4830662 ancres (0.024/octet), 116448 vus (2.41 %), 8.3s`
- **T1** `-rw-r--r--. 1 stephane stephane 200000000 18 nov 10:46 work/dedup/slice-200Mo.txt`
- **T1** `[bloc 1] 0/1 Mio, 0.0% vu, gardé, RSS 70 Mio, 7 s`
- **T1** `[bloc 1] 0/1 Mio, 0.0% vu, gardé, RSS 58 Mio, 0 s`
- **T1** `1+ (actuel): 60.8 ms, pic RSS 45.9 Mio (+33.3), len=1000000`
- **T1** `2+ (proposé): 19.0 ms, pic RSS 45.9 Mio (+0.0), len=1000000`
- **T1** `=== 1 Mo ===`
- **T1** `=== 200 Mo, budget 256 ===`
- **T1** `[bloc 18] 136/191 Mio, 15.9% vu, gardé, RSS 121 Mio, 8 s`
- **T1** `[bloc 19] 144/191 Mio, 7.6% vu, gardé, RSS 121 Mio, 9 s`
- **T1** `[bloc 20] 152/191 Mio, 2.8% vu, gardé, RSS 121 Mio, 9 s`
- **T1** `[bloc 21] 160/191 Mio, 3.7% vu, gardé, RSS 126 Mio, 10 s`
- **T1** `[bloc 22] 168/191 Mio, 1.3% vu, gardé, RSS 127 Mio, 10 s`
- **T1** `[bloc 23] 176/191 Mio, 0.3% vu, gardé, RSS 128 Mio, 10 s`
- **T1** `[bloc 24] 184/191 Mio, 0.6% vu, gardé, RSS 128 Mio, 11 s`
- **T1** `"recouvrement_origine": "2 % du bloc, plafonné à 1 Mio",`
- **T1** `[bloc 5] 256/7156 Mio, 3.3% vu, gardé, RSS 437 Mio, 18 s`
- **T1** `[bloc 6] 320/7156 Mio, 1.5% vu, gardé, RSS 439 Mio, 22 s`
- **T1** `[bloc 7] 384/7156 Mio, 1.9% vu, gardé, RSS 442 Mio, 26 s`
- **T1** `[bloc 14] 832/7156 Mio, 1.8% vu, gardé, RSS 504 Mio, 52 s`
- **T1** `[bloc 15] 896/7156 Mio, 7.0% vu, gardé, RSS 506 Mio, 56 s`
- **T1** `[still running after 60000ms; moved to background job bash-646]`
- **T1** `[bloc 37] 2304/7156 Mio, 1.4% vu, gardé, RSS 587 Mio, 139 s`
- **T1** `[bloc 38] 2368/7156 Mio, 2.0% vu, gardé, RSS 589 Mio, 143 s`
- **T1** `[bloc 64] 4032/7156 Mio, 2.0% vu, gardé, RSS 716 Mio, 243 s`
- **T1** `[bloc 65] 4096/7156 Mio, 2.1% vu, gardé, RSS 718 Mio, 247 s`

