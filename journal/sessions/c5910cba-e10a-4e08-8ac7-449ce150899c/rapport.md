# Session c5910cba — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `c5910cba-e10a-4e08-8ac7-449ce150899c` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 21:12 |
| Durée | 1.2 h |
| Tours | 1 |
| Messages | 97 |
| Appels d'outils | 105 |
| Fichiers touchés | 1 |
| Commandes | 87 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer le round R1/R2/R3** (commit `f908d7b0`) et vérifier que ses chiffres, ses règles et ses portes sont justes.  Contexte : `tools/bloc_linguistique.py` (`Heuristique`, `_syntagmes_simple`, `SUJETS`, `MODAUX`, `SUB_PAR_LANGUE`), `tools/tests/linguistique/evaluer_gold.py`, `tools/test … [1965 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer  … [2245 caractères tronqués]

*105 appels d'outils.* Actions notables :

- bash — Check git status and current branch
- bash — List relevant report files
- read
- bash — Check audit target file sizes and status
- bash — Inspect bloc_linguistique structure
- bash — Count phrases and segments in gold files
- bash — Grep autotest for audit-relevant code
- bash — Locate fiche numbers in autotest
- bash — Find all R1/R2/R3 rule sites
- bash — Inspect commit history and target commit stat
- bash — Show target commit diff for linguistic block
- bash — Find R1/R2/R3 claims in spans v7 report
- bash — Read start of spans v7 report
- bash — Check submodule state and tool file cleanliness
- … et 77 autres

**Synthèse produite :**

⏵ Finalisation du résumé d'audit

Audit terminé au commit `f908d7b0`. Deux fichiers neufs, aucun commit, aucun fichier existant modifié par moi :

- `reports/rapport-audit-r1r3.md`
- `reports/pensee-audit-r1r3.json`

\## Verdict

**Les chiffres rejouent tous. Les règles, non.** La fiche annonce **+27 exacts (222)** ; le code livré produit **+24 gains bruts pour 7 pertes = +17 (212)**. R1a perd 6 spans français, R1c en perd 1, R2 en perd 1, R3a est inerte, R3b n'est pas intégré.

\## 1. Rejeu — 0 écart

| grandeur | fiche / JSON | vivant 612 | gelé 602 |
|---|---:|---:|---:|
| labels | 212 | **212** | **212** |
| exact / labels | 212/212 = 1,0000 | **212/212** | **212/212** |
| couverture | 0,887 | **0,8870** | **0,8870** |
| F1 union | 0,5763 | 0,5720 | **0,5763** |
| S / chunker | 0,4966 / 0,6057 | 0,4910 / 0,6018 | **0,4966 / 0,6057** |
| tête | 0,7316 | 0,7262 | **0,7316** |
| fr / en | 129/129, 83/83 | **idem** | **idem** |
| spans | 27 (16 REL, 6 SUB, 5 GP) | **idem** | **idem** |
| top-k | 177 ; 0,7406 | **idem** | **idem** |
| « inatteignables » | 17 | **17** (même ensemble que A17) | **17** |

L'état **avant** est également reproduit exactement : 196 labels, 195 exacts, couverture 0,8201, F1 0,5595 gelé / 0,5555 vivant, 43 spans (21/17/5), top-k 166. **183/183 portes** passent avec `PYTHONPATH=. python3 -m tools.pensee.autotest` (le lancement direct `python3 tools/pensee/autotest.py` échoue sur l'import relatif).

\## 2. Ablations — gain/perte par règle

« Gain » = exact livré qui disparaît sans la règle ; « perte » = exact rétabli sans la règle. Net = gains − pertes.

| règle retirée | exact restant | gains dev/test | pertes dev/test | net | pertes (ids) |
|---|---:|---:|---:|---:|---|
| **R1a** SUJETS/pronom | 203 | 12 / 3 | **3 / 3** | **+9** | `r273 s069 s135` / `s032 s072 s115` |
| **R1b** modaux | 211 | 1 / 0 | 0 / 0 | +1 | — |
| **R1c** 2e prédicat | 209 | 2 / 2 | **1 / 0** | **+3** | `g017` |
| **R1** (faisceau) | 199 | 14 / 5 | **3 / 3** | **+13** | les 6 de R1a |
| **R2** SUB sans précédent | 209 | 4 / 0 | **1 / 0** | **+3** | `s037` |
| **R3a** subordonnants/langue | 212 | 0 / 0 | 0 / 0 | **0** | — |
| **R3c** `fall`/`call` | 210 | 2 / 0 | 0 / 0 | **+2** | — |
| *tout éteint* | 195 | **24** | **7** | **+17** | 7 pertes ci-dessus |

- **R1a** : gains `r034 r074 r114 r205 r219 r240 r243 r247 r278 r285 r296 r299` (dev), `r214 r216 r281` (test) ; pertes `r273 s069 s135` (dev), `s032 s072 s115` (test). Le code retire les relatifs de `SUJETS` ; i
… [4435 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-r1r3.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Check git status and current branch
- **T1** List relevant report files
- **T1** Check audit target file sizes and status
- **T1** Inspect bloc_linguistique structure
- **T1** Count phrases and segments in gold files
- **T1** Grep autotest for audit-relevant code
- **T1** Locate fiche numbers in autotest
- **T1** Find all R1/R2/R3 rule sites
- **T1** Inspect commit history and target commit stat
- **T1** Show target commit diff for linguistic block
- **T1** Find R1/R2/R3 claims in spans v7 report
- **T1** Read start of spans v7 report
- **T1** Check submodule state and tool file cleanliness
- **T1** Run baseline evaluator on gold
- **T1** Check module imports and RACINE
- **T1** Inspect spans v7 JSON structure
- **T1** Inspect A17 final state and negative control
- **T1** Run audit harness baseline and ablations
- **T1** Fix module registration and rerun harness
- **T1** Summarize harness results
- **T1** List 27 missing spans and compare with A17 17
- **T1** Run the 183-gate autotest suite
- **T1** Show dev/test baseline details
- **T1** Inspect autotest gate results
- **T1** Run autotest as module in background
- **T1** Add bundle ablations and live F1 to harness
- **T1** Run extended harness with bundle ablations
- **T1** Read A17 rule implementation details
- **T1** Validate all-off module equals parent commit
- **T1** Show extended ablation results
- **T1** Measure before-state, faithful R3a, top-k control
- **T1** List SUBORDONNANTS occurrences
- **T1** Read autotest results
- **T1** Run complements with faithful R3a
- **T1** Locate SUBORDONNANTS lines in tail
- **T1** Rerun complements after fixing replacement order
- **T1** Verify frozen, per-type, missing recoverables, stale docstrings
- **T1** List A17 causes and case statuses
- **T1** Print docstrings for late gates
- **T1** Inspect predicted spans for regression cases
- … et 47 autres

## 4. Mesures et résultats marquants

- **T1** `b1b1292f B13 — LE CACHE COMPLET : UN SEUL CHUNKING DANS LES DEUX CHEMINS (T178), VALIDÉ PAR A11 (×11,0, ÉGALITÉ 612/612) ; 181/181`
- **T1** `e0592c59 B13 — LE CACHE DU CHUNKER APPLIQUÉ : ×139 À 160 RÉPÉTITIONS, SORTIE IDENTIQUE (0/612) ; ×1 EN DÉFAUT, S DOMINE ; 181/181`
- **T1** `"lecture": "0,91 % en moyenne contre 100 % observé"`
- **T1** `"lecture": "0.963 % en moyenne contre 100.0 % observ\u00e9"`
- **T1** `- Un seul split deterministe (crc32 % 3), sans validation croisee.`
- **T1** `- **Un seul split déterministe** (`crc32 % 3`), sans validation croisée ; les chiffres`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : Traceback (most recent call last):   File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", line 32, in <module>     from .coeur import Candidat, Etat ImportError: attempted 
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 12, in <module> AssertionError: | `s065` | fr | REL | synthetique | 5:17 | « qui commence »  [exit code: 1]

