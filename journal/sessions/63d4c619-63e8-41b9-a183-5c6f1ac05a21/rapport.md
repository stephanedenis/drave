# Session 63d4c619 — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `63d4c619-63e8-41b9-a183-5c6f1ac05a21` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 13:11 |
| Durée | 0.0 h |
| Tours | 1 |
| Messages | 12 |
| Appels d'outils | 14 |
| Fichiers touchés | 0 |
| Commandes | 11 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, dépôt Python). Mission : **audit de reproductibilité** de la mesure d'attachement du bloc linguistique.  Contexte : `tools/tests/linguistique/evaluer_gold.py` expose `charger()` (gold de 612 phrases) et `evaluer_bloc(nom, bloc, phrases)` ; `tools/bloc_linguistique.py` expose `Heuristique`. Les valeurs publié … [1967 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, dépôt Python). Mission : **au … [2247 caractères tronqués]

*14 appels d'outils.* Actions notables :

- bash — Check git status, branch, and reports dir
- bash — List linguistique tests and count lines
- read
- bash — List pensee reports and sizes
- bash — Display the five JSON reports
- bash — Locate key symbols in bloc_linguistique
- bash — Find generators/references of the reports
- bash — Count phrases per gold file
- bash — Read the five markdown sheets
- bash — Run evaluer_bloc on 612 gold phrases
- bash — Check code state and submodule status
- bash — Compute lost attachment spans by type

**Synthèse produite :**

⏵ Computing lost spans by type against gold segments

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Check git status, branch, and reports dir
- **T1** List linguistique tests and count lines
- **T1** List pensee reports and sizes
- **T1** Display the five JSON reports
- **T1** Locate key symbols in bloc_linguistique
- **T1** Find generators/references of the reports
- **T1** Count phrases per gold file
- **T1** Read the five markdown sheets
- **T1** Run evaluer_bloc on 612 gold phrases
- **T1** Check code state and submodule status
- **T1** Compute lost attachment spans by type

## 4. Mesures et résultats marquants

- **T1** `- **La mesure globale cachait l'écart** : 0,6438 = moyenne pondérée (51 × 0,73 + 95 × 0,60).`

