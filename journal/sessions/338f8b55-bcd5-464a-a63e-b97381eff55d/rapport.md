# Session 338f8b55 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `338f8b55-bcd5-464a-a63e-b97381eff55d` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 18:33 |
| Durée | 2.1 h |
| Tours | 1 |
| Messages | 97 |
| Appels d'outils | 101 |
| Fichiers touchés | 0 |
| Commandes | 84 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **les deux derniers leviers POS** — R4 (copule → ADJ) et les classes fermées anglaises — mesurés sur dev/test, sans modifier le code du dépôt.  Contexte : `tools/bloc_linguistique.py` (`_pos`, `POS_FERME`, `ADJECTIFS`, `SUJETS`, les boucles 3 a/3 b/3 a bis), la fiche `reports/rapport-pos-a … [1722 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **les deux … [2002 caractères tronqués]

*101 appels d'outils.* Actions notables :

- bash — Check git status and repo layout
- bash — List reports and tools
- bash — Check sizes of POS files
- grep
- read
- bash — Locate POS structures in module
- bash — Inspect linguistic test tooling
- bash — Find A25/R4 references
- bash — Read evaluer_gold and split
- bash — Inspect fiabilite JSON structure
- bash — Dump top-level JSON keys
- bash — Find producer of fiabilite JSON
- bash — Inspect banc_50 entries
- bash — Locate classes and attachment logic
- … et 74 autres

**Synthèse produite :**

⏵ Contrôle final des deux livrables et de l’état du dépôt

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Check git status and repo layout
- **T1** List reports and tools
- **T1** Check sizes of POS files
- **T1** Locate POS structures in module
- **T1** Inspect linguistic test tooling
- **T1** Find A25/R4 references
- **T1** Read evaluer_gold and split
- **T1** Inspect fiabilite JSON structure
- **T1** Dump top-level JSON keys
- **T1** Find producer of fiabilite JSON
- **T1** Inspect banc_50 entries
- **T1** Locate classes and attachment logic
- **T1** Reproduce baseline metrics
- **T1** Look for R4 patch in previous JSON
- **T1** Inspect v2 JSON keys
- **T1** Search R4 entry in v1 JSON
- **T1** Dump R4 entry
- **T1** Inspect gold structure
- **T1** List gold contexts for candidate closed words
- **T1** List English closed-class gold words and predictions
- **T1** Probe _pos on key words
- **T1** List 50 free texts
- **T1** Read normalizer and _est_verbe
- **T1** Probe verb guard on adjectives/participles
- **T1** Build and smoke-test harness
- **T1** Measure R4 variants on gold
- **T1** Compare imported vs exec module baseline
- **T1** Check module hash and submodule state
- **T1** Inspect latest POS commit
- **T1** Extract B13 source and check gold unchanged
- **T1** Baseline on B13 source with current gold
- **T1** Reproduce B13 with B13 gold
- **T1** Run full variant matrix on B13 and HEAD
- **T1** Fix sys.path and rerun matrix
- **T1** Detailed corrections/breaks for R4 and per-word CC
- **T1** Run 200-draw placebo for R4 and CC
- **T1** Check baseline POS counts on 50 free texts
- **T1** Run variants on 50 free texts and diff
- **T1** Print free-text change contexts
- **T1** Compute full metrics for selected variants
- … et 44 autres

## 4. Mesures et résultats marquants

- **T1** `[{"id": "R1", "nom": "le lexique verbal tranche le défaut ouvert", "enonce": "un mot inconnu n'est pas un nom par défaut : si _est_verbe le connaît (formes irrégulières + base + -s/-ed/-ing), il est V`
- **T1** `2ba393b0 B13 — LA POS À 83,83 % (R2a/R3/R2b) : F1 0,5849 → 0,6181, ANGLAIS 0,6341 → 0,7273, ATTACHEMENT INCHANGÉ (222/222) ; 183/183`
- **T1** `[still running after 60000ms; moved to background job bash-3547]`
- **T1** `base                     POS all=0.8383 dev=0.8375 (+0.00%) test=0.8400 (+0.00%) en=0.9103 fr=0.7976`
- **T1** `r4_en                    POS all=0.8421 dev=0.8416 (+0.41%) test=0.8431 (+0.31%) en=0.9207 fr=0.7976`
- **T1** `r4_fr                    POS all=0.8418 dev=0.8407 (+0.32%) test=0.8441 (+0.41%) en=0.9103 fr=0.8031`
- **T1** `r4_bilingue              POS all=0.8455 dev=0.8449 (+0.74%) test=0.8471 (+0.71%) en=0.9207 fr=0.8031`
- **T1** `cc_core                  POS all=0.8459 dev=0.8449 (+0.74%) test=0.8481 (+0.81%) en=0.9312 fr=0.7976`
- **T1** `cc_fast                  POS all=0.8465 dev=0.8453 (+0.78%) test=0.8491 (+0.91%) en=0.9329 fr=0.7976`
- **T1** `r4_bilingue+cc_core      POS all=0.8531 dev=0.8522 (+1.47%) test=0.8551 (+1.51%) en=0.9416 fr=0.8031`
- **T1** `r4_bilingue+cc_fast      POS all=0.8534 dev=0.8526 (+1.51%) test=0.8551 (+1.51%) en=0.9425 fr=0.8031`
- **T1** `r4_en+cc_core            POS all=0.8496 dev=0.8490 (+1.15%) test=0.8511 (+1.11%) en=0.9416 fr=0.7976`
- **T1** `r4_en+cc_fast            POS all=0.8500 dev=0.8494 (+1.19%) test=0.8511 (+1.11%) en=0.9425 fr=0.7976`
- **T1** `cc_core                  POS all=0.8462 dev=0.8453 (+0.78%) test=0.8481 (+0.81%) en=0.9321 fr=0.7976`
- **T1** `cc_fast                  POS all=0.8468 dev=0.8458 (+0.83%) test=0.8491 (+0.91%) en=0.9338 fr=0.7976`
- **T1** `r4_bilingue+cc_core      POS all=0.8534 dev=0.8526 (+1.51%) test=0.8551 (+1.51%) en=0.9425 fr=0.8031`
- **T1** `r4_bilingue+cc_fast      POS all=0.8537 dev=0.8531 (+1.56%) test=0.8551 (+1.51%) en=0.9434 fr=0.8031`
- **T1** `r4_en+cc_core            POS all=0.8500 dev=0.8494 (+1.19%) test=0.8511 (+1.11%) en=0.9425 fr=0.7976`
- **T1** `r4_en+cc_fast            POS all=0.8503 dev=0.8499 (+1.24%) test=0.8511 (+1.11%) en=0.9434 fr=0.7976`
- **T1** `patch checks {'checks': {'copules_en': True, 'copules_fr': True, 'insert': True, 'bloc_en': True}, 'patch_applique_a': '/tmp/pos_r4/bloc_patche.py', 'sha256': '0bf4d3eb0e2a51603534001284718e625346a61c`
- **T1** `5c5d3b52 B13 — LE PAQUET POS SÛR (CLASSES FERMÉES + R4-EN) : POS 83,83 → 84,96 %, 37 CORRIGÉS / 0 CASSÉ, ATTACHEMENT INCHANGÉ ; 183/183`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "/tmp/pos_r4/run_matrix.py", line 4, in <module>     from tools.tests.linguistique.evaluer_gold import evaluer_bloc ModuleNotFoundError: No module na
- **T1** : ### r4_bilingue textes 6 pos 8 transitions {('NOUN', 'ADJ'): 8} seg 0 att 0 inval 0    ('f20', 'fr', 'arrivés', 'NOUN', 'ADJ', 42, 49)    ('f28', 'fr', 'gratuite', 'NOUN', 'ADJ', 29, 37)    ('f38', 'f
- **T1** : [stderr] Traceback (most recent call last):   File "/tmp/pos_r4/compute_final.py", line 32, in <module>     CC_LARGE['add']['DET'].update("some any no every each either neither both all another other 

