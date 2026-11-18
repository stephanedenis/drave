# Session cbf7ca71 — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-18/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `cbf7ca71-5b38-428e-9f19-298be1720918` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-18 10:17 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 27 |
| Appels d'outils | 28 |
| Fichiers touchés | 1 |
| Commandes | 20 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (Drave, en français). Machine dédiée (40 threads, 125 Go RAM). NE TOUCHE PAS à `data/` (lecture seule).  CONTEXTE : l'inventaire `reports/rapport-donnees-inventaire.md` a montré que `data/corpus_wiki_fr_texte/train.txt` fait **7,50 Go** et pourrait fermer l'écart du palier 1, MAIS l'outil actuel `tools/corpus_propre.py` tient tous  … [2581 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (Drave, en français). Machine dédiée (40 threads, 125 … [2861 caractères tronqués]

*28 appels d'outils.* Actions notables :

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
- … et 12 autres

**Synthèse produite :**

⏵ Running the first smoke test and the autotest

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py` | 1 | 4 |

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

## 4. Mesures et résultats marquants

- **T1** `/dev/mapper/system-root   11T  9,0T  1,9T  83% /home/stephane/Data13TB`
- **T1** `"split": "hash salé (graine 1) de page_id : 5% val, 5% test"`
- **T1** `recouvrement de contexte en Mio (défaut : 2 % du bloc,`
- **T1** `{'budget_mio': 512.0, 'plancher_mio': 80.3, 'bloc_mio': 0.06, 'recouvrement_octets': 1310, 'recouvrement_origine': '2 % du bloc, plafonné à 1 Mio', 'cout_entree': {'table_octets_entree': 104.9, 'entie`

