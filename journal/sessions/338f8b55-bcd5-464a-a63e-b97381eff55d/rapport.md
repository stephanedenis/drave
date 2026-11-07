# Session 338f8b55 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `338f8b55-bcd5-464a-a63e-b97381eff55d` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-06 18:33 |
| Durée | 0.5 h |
| Tours | 1 |
| Messages | 35 |
| Appels d'outils | 40 |
| Fichiers touchés | 0 |
| Commandes | 32 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **les deux derniers leviers POS** — R4 (copule → ADJ) et les classes fermées anglaises — mesurés sur dev/test, sans modifier le code du dépôt.  Contexte : `tools/bloc_linguistique.py` (`_pos`, `POS_FERME`, `ADJECTIFS`, `SUJETS`, les boucles 3 a/3 b/3 a bis), la fiche `reports/rapport-pos-a … [1722 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **les deux … [2002 caractères tronqués]

*40 appels d'outils.* Actions notables :

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
- … et 20 autres

**Synthèse produite :**

⏵ Construction du harnais hors dépôt (copie en mémoire)

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

## 4. Mesures et résultats marquants

- **T1** `[{"id": "R1", "nom": "le lexique verbal tranche le défaut ouvert", "enonce": "un mot inconnu n'est pas un nom par défaut : si _est_verbe le connaît (formes irrégulières + base + -s/-ed/-ing), il est V`
- **T1** `2ba393b0 B13 — LA POS À 83,83 % (R2a/R3/R2b) : F1 0,5849 → 0,6181, ANGLAIS 0,6341 → 0,7273, ATTACHEMENT INCHANGÉ (222/222) ; 183/183`

