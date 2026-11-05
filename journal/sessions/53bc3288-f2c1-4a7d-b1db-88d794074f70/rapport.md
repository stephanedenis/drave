# Session 53bc3288 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `53bc3288-f2c1-4a7d-b1db-88d794074f70` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 13:16 |
| Durée | 1.0 h |
| Tours | 1 |
| Messages | 99 |
| Appels d'outils | 105 |
| Fichiers touchés | 6 |
| Commandes | 88 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **contrôle indépendant** de la convention d'attachement par un échantillon annoté à la main.  Contexte : la convention des cibles est documentée dans `tools/tests/linguistique/gold_reel.py` (constante `CONVENTION_CIBLE`) : REL/SUB → l'antécédent (tête du GN à gauche) ; GP → le verbe gouver … [1806 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **contrôle … [2086 caractères tronqués]

*105 appels d'outils.* Actions notables :

- bash — Check repo state and list linguistique tools
- bash — List reports directory
- read
- grep
- bash — Count gold targets and sources
- bash — Diagnose import path issue
- bash — List actual filenames with repr
- bash — Retry import with absolute path
- bash — Load module via spec_from_file_location
- bash — Debug PathFinder lookup
- bash — Test direct import one-liner
- bash — Inspect import machinery and test temp module
- bash — Inspect FileFinder behavior on directory
- bash — Trace PathFinder.find_spec during import
- … et 83 autres

**Synthèse produite :**

⏵ Contrôle livré : deux fiches neuves, aucun commit

**Livrables**
- `reports/rapport-annotation-independante.md`
- `reports/pensee-annotation-independante.json`

**Résultats**
- **Moi ↔ gold : 20/20** (100 %, IC95 83,9–100 % ; 19/19 sans `r057`, seule cible vue avant le tirage).
- **Moi ↔ bloc HEAD `e1171032`** : **10/20** au sens strict (même type + span), **17/20** si l'on ne juge que la cible d'attachement. Sur les 10 désaccords stricts, 7 sont des erreurs de span/type (3 spans REL trop longs, 4 segments typés `GN`) et 3 de vraies cibles fausses (`r293`, `s052`, `r230`).
- **Après le correctif SUB appliqué pendant la session** (snapshot `6e843018`, post-hoc) : **11/20** strict, **18/20** cible ; global **137/145 = 94,5 %** (contre 123/145), couverture inchangée 145/239, échecs SUB au span exact **8 → 2**. Restent faux : `r293` (`here` vs `person`) et `r230` (`appelle-moi` vs `appelle`).
- **Contrôle négatif** : hasard uniforme sur les 239 cibles = **0,77 %** (IC95 0–5 % ; max 3/20 sur 10 000 simulations).

**Ambiguïtés principales**
1. **`SUB`** : la ligne `CONVENTION_CIBLE` « antécédent » est contredite par **69/69 cibles SUB verbes** (POS gold), 9/9 dans l'échantillon. Le bloc appliquait la lettre (`s052` → `cuisine` au lieu de `ouvre`) ; le correctif de bloc et de doc est intervenu pendant la session et les données le valident.
2. **`_est_verbe` / split verbe-nom** : encore faux — 53 verbes comptés comme noms sur 145 labels (HEAD), 45 après correctif ; utiliser le POS gold.
3. **`GP`** : 4/96 gouverneurs adjectivaux absents de la doc ; 43/96 GP ont deux cibles mais la mesure ne compare qu'à `cibles[0]`.
4. **`REL`** : 26/74 spans exacts seulement, mais 26/26 cibles justes quand le span est bon — problème de découpage, pas de convention.

**Note** : le bloc et `gold_reel.py` ont été modifiés pendant la session (pas par moi) ; les deux versions du bloc sont pinées et datées dans la fiche. Aucun fichier existant modifié par moi, aucun commit.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/qtrinet_annotation/extraire_aveugle.py` | 1 | 0 |
| `/tmp/qtrinet_annotation/mes_annotations.json` | 1 | 0 |
| `/tmp/qtrinet_annotation/comparer.py` | 1 | 0 |
| `/tmp/qtrinet_annotation/fabriquer.py` | 1 | 0 |
| `/tmp/qtrinet_annotation/mesurer_versions.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-annotation-independante.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Check repo state and list linguistique tools
- **T1** List reports directory
- **T1** Count gold targets and sources
- **T1** Diagnose import path issue
- **T1** List actual filenames with repr
- **T1** Retry import with absolute path
- **T1** Load module via spec_from_file_location
- **T1** Debug PathFinder lookup
- **T1** Test direct import one-liner
- **T1** Inspect import machinery and test temp module
- **T1** Inspect FileFinder behavior on directory
- **T1** Trace PathFinder.find_spec during import
- **T1** Check sys.modules and verbose import traceback
- **T1** Generate blind 20-case sample
- **T1** Fix import typo and run sampling
- **T1** Correct spelling via Python and run
- **T1** Relax leak check to JSON keys only and run
- **T1** Print readable blind cases
- **T1** Inspect block attachment output format
- **T1** Compare annotations with gold and block; compute random baseline
- **T1** Run comparison and random baseline
- **T1** Inspect block segmentation on mismatches
- **T1** Inspect block segmentation on mismatched cases
- **T1** Inspect block segmentation with fixed path
- **T1** Find similar existing report fiches
- **T1** Check target report names and existing report styles
- **T1** Inspect existing pensee JSON formats
- **T1** Compute population distribution and global block context
- **T1** Inspect gold source entries for multi-target GP cases
- **T1** Analyze target types and multi-target patterns
- **T1** Sample SUB cases by first target type
- **T1** Inspect _est_verbe heuristic
- **T1** Measure _est_verbe misclassification against gold POS
- **T1** Split first targets by gold POS and heuristic
- **T1** List adjective/noun GP governors and pronoun REL
- **T1** Verify seed reproducibility and ordinals
- **T1** Compute Wilson confidence intervals
- **T1** Global block coverage and accuracy by type
- **T1** Record revision, hash, and confirm pre-annotation leak case
- **T1** List SUB target errors at exact span
- … et 48 autres

## 4. Mesures et résultats marquants

- **T1** `20 / 20 = 1.0 Wilson 95% (0.8389, 1)`
- **T1** `17 / 20 = 0.85 Wilson 95% (0.6396, 0.9476)`
- **T1** `13 / 20 = 0.65 Wilson 95% (0.4329, 0.8188)`
- **T1** `10 / 20 = 0.5 Wilson 95% (0.2993, 0.7007)`
- **T1** `12 / 20 = 0.6 Wilson 95% (0.3866, 0.7812)`
- **T1** `10 / 12 = 0.8333 Wilson 95% (0.552, 0.953)`
- **T1** `4 / 9 = 0.4444 Wilson 95% (0.1888, 0.7333)`
- **T1** `7 / 9 = 0.7778 Wilson 95% (0.4526, 0.9368)`
- **T1** `5 / 9 = 0.5556 Wilson 95% (0.2667, 0.8112)`
- **T1** `178:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes`
- **T1** `253:| **R0.7** | **la couche linguistique** : neuf niveaux (graphème → pragmatique), heuristique CPU + neuronal de contrat, substitution/parallèle/cascade, activation sémantique 51–76 % | ✅ **398 lang`
- **T1** `"moi_gold": "20/20 (100 %) ; 19/19 sans le cas r057 (cible vue avant le tirage)",`
- **T1** `"moi_bloc_strict": "10/20 (50 %) contre HEAD d9c9d559 (mesure aveugle) ; 11/20 sur le snapshot post-correctif 6e843018",`
- **T1** `"moi_bloc_attachement_seul": "17/20 (85 %) contre HEAD ; 18/20 (90 %) après le correctif SUB",`
- **T1** `"controle_negatif": "hasard uniforme 0,77 % (IC95 0-5 %) ; 20/20 observé"`
- **T1** `"n = 20 : les IC Wilson sont larges (20/20 -> 83,9-100 % ; 10/20 -> 29,9-70,1 %) ; aucune conclusion sur les 239.",`
- **T1** `{'moi_gold': '20/20 (100 %) ; 19/19 sans le cas r057 (cible vue avant le tirage)', 'moi_bloc_strict': '10/20 (50 %) contre HEAD d9c9d559 (mesure aveugle) ; 11/20 sur le snapshot post-correctif 6e84301`

## 5. Erreurs rencontrées

9 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 3, in <module> ModuleNotFoundError: No module named 'evaler_gold' [exit code: 1]
- **T1** : exists: True abspath: /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py stat: 14095 [stderr] Traceback (most recent call last):   File "<stdin>", line 6, in <mod
- **T1** : [stderr] Traceback (most recent call last):   File "/tmp/qtrinet_annotation/extraire_aveugle.py", line 9, in <module>     import evaler_gold as eg  # noqa: E402     ^^^^^^^^^^^^^^^^^^^^^^^^ ModuleNotF
- **T1** : 9:import evaler_gold as eg  # noqa: E402 [stderr] Traceback (most recent call last):   File "/tmp/qtrinet_annotation/extraire_aveugle.py", line 9, in <module>     import evaler_gold as eg  # noqa: E40
- **T1** : import evaluer_gold as eg  # noqa: E402 [stderr] Traceback (most recent call last):   File "/tmp/qtrinet_annotation/extraire_aveugle.py", line 49, in <module>     assert '"cible' not in blob and "'cib
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 7, in <module> ModuleNotFoundError: No module named 'evaler_gold' [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 5, in <module> KeyError: 'id' [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 5, in <module>   File "/usr/lib64/python3.13/importlib/__init__.py", line 88, in import_module     return _bootstrap._gcd_import(name
- **T1** : [stderr] Traceback (most recent call last):   File "/tmp/qtrinet_annotation/fabriquer.py", line 283, in <module>     json.dump(pensee, f, ensure_ascii=False, indent=1)     ~~~~~~~~~^^^^^^^^^^^^^^^^^^^

