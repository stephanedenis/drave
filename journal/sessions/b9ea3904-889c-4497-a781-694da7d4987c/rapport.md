# Session b9ea3904 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `b9ea3904-889c-4497-a781-694da7d4987c` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 14:47 |
| Durée | 1.5 h |
| Tours | 1 |
| Messages | 104 |
| Appels d'outils | 118 |
| Fichiers touchés | 2 |
| Commandes | 94 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer la qualité du gold anglais** (210 phrases sur 612), parce que beaucoup d'échecs d'attachement sont anglais.  Contexte : `tools/tests/linguistique/gold_reel.py` (432 phrases réelles, 20 fr / 20 en par bloc ; `gold_reel.json` généré), `tools/tests/linguistique/evaluer_gold.py` (`ch … [1835 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer  … [2115 caractères tronqués]

*118 appels d'outils.* Actions notables :

- bash — Check git status and branch
- bash — List linguistic test and reports dirs
- bash — List linguistique dir and relevant reports
- bash — Line counts of key files
- read
- bash — Inspect gold_reel.json structure
- bash — Count gold by source and language
- bash — Show tail of gold_reel.py
- bash — Locate Heuristique and verb lexicon
- bash — Inspect other gold files
- bash — Read lexicons and _est_verbe
- bash — Read Heuristique implementation
- bash — Dump English sentence list and duplicates
- bash — Check spans, overlap, coverage anomalies
- … et 95 autres

**Synthèse produite :**

⏵ Clôture de l'audit gold anglais et livraison du rapport

**Livrables**
- `reports/rapport-gold-anglais.md` — fiche complète (verdict, tableaux fr/en, annotations suspectes, contrôles, limites, recommandation).
- `reports/pensee-gold-anglais.json` — chiffres, spans, cibles, anomalies, contrôles (JSON valide).

**Annotations suspectes : 25 phrases anglaises sur 210 (11,9 %)** portent au moins une anomalie ; **16 (7,6 %)** sur les couches réellement mesurées :
- **10 tags POS divergents** : 7 erreurs probables (`is`×3, `do`, `late`×2, `far`) + 3 dus à la convention `that` (CONJ vs PRON) ;
- **6 GP sans cible** : 4 après un verbe (`r336`, `r342`, `r358`, `r367`), 2 après copule (`r328`, `r363`) ;
- **3 rôles** (2 faux : `r165`, `r239` ; 1 discutable : `r180`), **1 modalité** (`r247`), **3 phrases non grammaticales** (`r028`, `r102`, `r165`), **1 doublon** (`r336`/`r358`), **6 coref** suspectes (hors mesure).

**Écarts fr/en** (HEAD v3 `dcf7bc91`, code `9544f173`, revérifié à `8281d51e`) :

| mesure | fr | en |
|---|---:|---:|
| couverture attachement (plein) | 0,775 | **0,318** |
| couverture (réel seul) | 0,907 | **0,318** |
| exact global | 0,748 | 0,318 |
| exact sur span | 0,966 | **1,000** (28/28, tous GP) |
| spans perdus | 34/151 | **60/88** |

Les 60 spans anglais perdus sont **28/28 REL et 26/26 SUB** : l'anglais représente **60/94 spans perdus (63,8 %)** pour 36,8 % des cibles. Le gold est structurellement sain (0 span faux, 0 chevauchement, 0 cible absente/non-token, 0 GN avalant un verbe ; 97/97 cibles = tokens de surface). La cause est l'analyseur : S ne segmente pas l'anglais (277 GV, 0 GN/GP/REL/SUB, 2/702 exacts) et `_pos` tague 176 VERB gold en NOUN (`talks`→NOUN, `brother`→VERB). `_est_verbe` n'est d'accord que sur 81/97 cibles : garder le POS gold.

**Recommandation** : segmenter l'anglais d'abord (S language-aware ou chunker anglais), puis corriger `_pos` (+6,9 pts simulés, attachement inchangé), puis l'hygiène du gold ; mesurer fr/en séparément ; ne pas ajuster le lexique au gold. La v2 (137/145) est périmée : v3 = 141/145, anglais inchangé.

**Commit** : `028c8281` (A14) a intégré mes deux fichiers pendant l'audit. Mes corrections post-commit du rapport (titre, tableau des conventions, note ADJ, lignes top1/top-k) sont dans le worktree et **non commitées** ; je n'ai rien commité. Le JSON est déjà dans le commit.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md` | 1 | 8 |

### Commandes exécutées (échantillon)

- **T1** Check git status and branch
- **T1** List linguistic test and reports dirs
- **T1** List linguistique dir and relevant reports
- **T1** Line counts of key files
- **T1** Inspect gold_reel.json structure
- **T1** Count gold by source and language
- **T1** Show tail of gold_reel.py
- **T1** Locate Heuristique and verb lexicon
- **T1** Inspect other gold files
- **T1** Read lexicons and _est_verbe
- **T1** Read Heuristique implementation
- **T1** Dump English sentence list and duplicates
- **T1** Check spans, overlap, coverage anomalies
- **T1** Check POS composition, roles, targets
- **T1** Dump English token POS
- **T1** Dump English segments and targets
- **T1** Find missing targets and uncovered tokens
- **T1** Classify target forms and POS
- **T1** Compare _est_verbe with gold POS on targets
- **T1** Token-level _est_verbe vs gold POS
- **T1** Inspect Heuristique output on English samples
- **T1** Run official metrics per language subset
- **T1** Control metrics with S generator disabled
- **T1** Per-type labels for English and French
- **T1** Read span report JSON
- **T1** Reproduce span-loss categories per language
- **T1** List lost spans and overlapping predictions
- **T1** Inspect GP losses and simple chunker
- **T1** Inspect English hand gold
- **T1** Count multi-target segments
- **T1** Find English forms with multiple POS tags
- **T1** List contexts of inconsistent POS forms
- **T1** Measure POS accuracy with corrected gold
- **T1** Per-type attachment stats and target errors
- **T1** Reconcile exact counts with official evaluator
- **T1** Print exact attachment dict
- **T1** Test hash-seed determinism of metrics
- **T1** Test evaluator state dependence
- **T1** Check for concurrent modifications and file timestamps
- **T1** Check git HEAD and diffs
- … et 54 autres

## 4. Mesures et résultats marquants

- **T1** `1.40user 0.02system 0:01.43elapsed 100%CPU (0avgtext+0avgdata 30028maxresident)k`
- **T1** `e0592c59 2026-11-05 B13 — LE CACHE DU CHUNKER APPLIQUÉ : ×139 À 160 RÉPÉTITIONS, SORTIE IDENTIQUE (0/612) ; ×1 EN DÉFAUT, S DOMINE ; 181/181`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `"gold_anomalies": "25/210 phrases (11,9 %), dont 16 (7,6 %) sur les couches mesurées ; 10 tags POS divergents, 6 GP sans cible, 3 rôles",`
- **T1** `"anglais_echec": "60/94 spans perdus, 100 % des REL et SUB anglais ; la cause est la segmentation, pas le gold",`
- **T1** `"est_verbe": "83,5 % d'accord avec le POS gold sur les cibles ; 15 FN, 1 FP (flower) ; garder le POS gold comme référence",`
- **T1** `cible (36,8 %). Mais ces 60 échecs sont **des spans**, pas des cibles : sur les 28 segments anglais`
- **T1** `-| tags POS divergents (même forme, même fonction) | 7 (`est`×4, `que`×3) | 10 (7 durs + 3 `that`) |`
- **T1** `+| tags POS en contradiction avec une autre occurrence | 7 (`est`×4, `que`×3) | 10 (7 durs + 3 `that`) |`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : sha HEAD 5640809e8e6bfbd6 sha WT 64b7c5204f21e4c2 same False [stderr] Traceback (most recent call last):   File "<stdin>", line 10, in <module>   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/
- **T1** : gold pragma distinct values: [stderr] Traceback (most recent call last):   File "<stdin>", line 7, in <module>   File "/usr/lib64/python3.13/collections/__init__.py", line 614, in __init__     self.up

