# Session 3144cf23 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `3144cf23-6004-46ef-bc3d-f05d81c0cff6` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 14:47 |
| Durée | 1.3 h |
| Tours | 1 |
| Messages | 82 |
| Appels d'outils | 83 |
| Fichiers touchés | 6 |
| Commandes | 70 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **mesurer ce que le chunker seul peut couvrir** des 94 spans perdus de l'attachement REL/SUB, sans toucher au code.  Contexte : `tools/bloc_linguistique.py` (`Heuristique(segmenter_s=False)` = chunker seul, `_syntagmes_simple`), `tools/tests/linguistique/evaluer_gold.py` (`charger`). Sur l … [1947 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **mesurer  … [2227 caractères tronqués]

*83 appels d'outils.* Actions notables :

- bash — Show git status, branch, and top-level files
- bash — List linguistic tests and reports directories
- bash — Count lines of key files and list test dir
- bash — Find key definitions in chunker
- read
- bash — Read lexicons POS_RELATIFS and helpers
- bash — Reproduce 239 targets and 94 lost spans
- bash — Compare default vs chunker-only coverage
- bash — Inspect the 94 lost spans by source and language
- bash — Detailed diagnostic of each lost span
- bash — Compute marker tallies and near-miss features
- bash — Inspect synthetic gold builder and S generator API
- bash — Read S generator head and tail
- bash — Compare S generator spans against the 94 lost
- … et 65 autres

**Synthèse produite :**

⏵ Clôture — livrables écrits et résultat transmis au parent

Mission terminée. J'ai écrit **deux fichiers neufs seulement**, sans committer ni modifier de fichier existant :

- `reports/rapport-spans-chunker.md` — fiche complète (verdict, tableaux, règles, contrôles négatifs, limites)
- `reports/pensee-spans-chunker.json` — agrégats + détail des 94 spans

**Chunker seul** (`Heuristique(segmenter_s=False)`) sur les 94 spans perdus : **0 exact** (0 REL, 0 SUB, 0 GP). C'est structurel : le mode par défaut est l'union S + chunker, donc un span exact du chunker serait déjà compté bon. Sur tout le gold, il ne produit que **77 exacts, tous GP**.

**Causes primaires (94)** : avalé par un GN **31** (REL) · type SUB absent **33** · marqueur hors lexique/branche **15** (REL 12 : where 6, whom 3, whose 1, when 1, zéro 1 ; GP 3) · fin de clause/frontière **7** (REL 4, GP 3) · tête avalée par le GN **1** · avalé par un GV **3** (GP) · gold GP sans préposition **4**.

**Couverture des deux règles** :
- (a) marqueur + frontière : **+79/94** (47 REL, 32 SUB, 0 GP) → **224/239**
- (b) un prédicat par clause : **+41/94** (36 REL, 0 SUB, 5 GP) → **186/239**
- (a)+(b) : **+84/94** (47 REL, 32 SUB, 5 GP) → **229/239 (95,8 %)**

**Régression** : 0 des 77 spans exacts du chunker seul perdu, 0/145 en union ; le prix est le FP (1059 → 852, −207) ; F1 global 0,2862 → 0,4043 ; F1 REL 0,371 → 0,844, SUB 0,685 → 0,926.

**Contrôles** : sans frontière, (a) ne gagne que 32 SUB (0 REL, F1 0,162) ; sans l'arrêt du GN sur le relatif, (b) ne gagne que 5 GP (0 REL, F1 0,283) ; hasard mêmes longueurs 6,08 % ; décalage +1 = 0/94 ; oracle frontière tête donnée REL 48/48, SUB 32/33. L'attachement global monte (top-k 0,594 → 0,707) mais le top-k conditionnel au bon span tombe de 0,979 à 0,738 : les 84 spans récupérés sont plus durs à attacher.

Limite majeure : mesure **in-sample**, sur copie locale, portes non lancées — à ne pas committer sans gold tenu à l'écart.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/spans/regles.py` | 2 | 0 |
| `/tmp/spans/simuler.py` | 1 | 0 |
| `/tmp/spans/analyse.py` | 1 | 0 |
| `/tmp/spans/final.py` | 1 | 0 |
| `/tmp/spans/construire_json.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-spans-chunker.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Show git status, branch, and top-level files
- **T1** List linguistic tests and reports directories
- **T1** Count lines of key files and list test dir
- **T1** Find key definitions in chunker
- **T1** Read lexicons POS_RELATIFS and helpers
- **T1** Reproduce 239 targets and 94 lost spans
- **T1** Compare default vs chunker-only coverage
- **T1** Inspect the 94 lost spans by source and language
- **T1** Detailed diagnostic of each lost span
- **T1** Compute marker tallies and near-miss features
- **T1** Inspect synthetic gold builder and S generator API
- **T1** Read S generator head and tail
- **T1** Compare S generator spans against the 94 lost
- **T1** List chunker-only exact matches by type
- **T1** Dump token POS sequences of REL/SUB lost spans
- **T1** Trace chunker segmentation for sample sentences
- **T1** Measure verb lexicon coverage inside lost clauses
- **T1** Measure POS-based verb detection on clause verbs
- **T1** Show synthetic phrases with bare-noun GP gold spans
- **T1** Check gold GV heads and subject inclusion
- **T1** Copy chunker to /tmp for local simulation
- **T1** Probe verb/POS recognition of tricky words
- **T1** Probe POS recognition correctly
- **T1** List all sentences containing lost spans
- **T1** Execute first simulation run
- **T1** Fix POS helper and rerun simulation
- **T1** Show simulation summary head
- **T1** Rerun with corrected baselines
- **T1** Run simulation showing exit code
- **T1** Inspect script tail after edit
- **T1** Append main guard and rerun
- **T1** Show union results and AB misses
- **T1** Debug rule outputs on missed examples
- **T1** Apply principled fixes and rerun
- **T1** Rerun with strict rule B lexicons
- **T1** Summarize metrics per mode
- **T1** Inspect existing pensee JSON structure
- **T1** Inspect sibling report and existing style
- **T1** Read prior 94-span fiche
- **T1** Read prior pensee-spans JSON
- … et 30 autres

## 4. Mesures et résultats marquants

- **T1** `> substituables, un parallèle et une cascade, une activation sémantique à **51–76 %** ; la`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 5, in <module> TypeError: Heuristique._pos() missing 1 required positional argument: 'mot' [exit code: 1]
- **T1** : 94 langue Counter({'en': 60, 'fr': 34}) source Counter({('reel', 'REL'): 32, ('reel', 'SUB'): 27, ('synthetique', 'REL'): 16, ('reel', 'GP'): 7, ('synthetique', 'SUB'): 5, ('synthetique', 'GP'): 4, ('

