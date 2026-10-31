# Session d093c795 — Dépôt /home/stephane/GitHub/Qtrinet, s

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `d093c795-b4c9-4270-bea8-e2673f86057b` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 14:55 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 27 |
| Appels d'outils | 40 |
| Fichiers touchés | 0 |
| Commandes | 40 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A13 : tester la **seule niche non mesurée de M2** — les surfaces que M1 ne lit pas — sans modifier les modules existants.  État : - M1 `hub.py` lit 528/528 surfaces réelles ; M2 `voies.py` lit 93,4/93,6 % sur `de`/`vers`, toujours **sous M1** ; aucun étage ne consomme M2 (B14). - A9 note : « M2 ne pourrait servir que de secours sur des s … [1732 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A13 : tester la **seule niche non mesurée de M2** — les sur … [2012 caractères tronqués]

*40 appels d'outils.* Actions notables :

- bash — List repo root and cerveau tools
- bash — Check git status and recent commits
- bash — Line counts of modules and list tests
- bash — Read start of hub.py
- bash — Read start of voies.py
- bash — Structure of voies.py
- bash — Read M2 entry construction and training
- bash — Read M2 evaluation functions
- bash — Inspect checkpoint directory
- bash — Read pipeline_semantique_m2 start
- bash — Find model loading in pipeline
- bash — Read pipeline M2 model loading region
- bash — Read pipeline training cache region
- bash — Read pipeline remainder
- … et 26 autres

**Synthèse produite :**

⏵ Écriture de `tools/cerveau/m2_secours.py`

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List repo root and cerveau tools
- **T1** Check git status and recent commits
- **T1** Line counts of modules and list tests
- **T1** Read start of hub.py
- **T1** Read start of voies.py
- **T1** Structure of voies.py
- **T1** Read M2 entry construction and training
- **T1** Read M2 evaluation functions
- **T1** Inspect checkpoint directory
- **T1** Read pipeline_semantique_m2 start
- **T1** Find model loading in pipeline
- **T1** Read pipeline M2 model loading region
- **T1** Read pipeline training cache region
- **T1** Read pipeline remainder
- **T1** Read typed_corpus
- **T1** Read CHAMPS and check M2 cache
- **T1** Read synth corpus
- **T1** Compute M2 cache keys
- **T1** Inventory corpus items
- **T1** Verify M1 on all 528 original surfaces
- **T1** Inspect cached M2 head configs
- **T1** Read sequences module
- **T1** Check A9 outputs and masks
- **T1** Compare de/vers class coverage synth vs real
- **T1** Show A9 verdict and M2 figures
- **T1** Inspect M2 A9 errors and unseen items
- **T1** Read normalization and codecs
- **T1** Find codec rendering formats
- **T1** Find codecs module file
- **T1** Check normalise_forme lowercase behavior
- **T1** Read codecs init
- **T1** Find rendering implementation
- **T1** Read echecs parse/render
- **T1** Find chess RSN helpers
- **T1** Read jeux.corpus
- **T1** Map typed items to source contexts and verify M1
- **T1** Check python environments
- **T1** Run baseline test suite
- **T1** List distinct chess codes in de/vers items
- **T1** Test SAN/UCI/FR rendering from code+context

## 4. Mesures et résultats marquants

- **T1** `"M2 n'ajoute rien à la chaîne : M1 lit 100 % des 146 items réels, "`
- **T1** `"M2 93–94 %, et aucun étage ne consomme M2. Remplacer M1 par M2 "`
- **T1** `"phrase": "M2 n'ajoute rien à la chaîne : M1 lit 100 % des 146 items réels, M2 93–94 %, et aucun étage ne consomme M2. Remplacer M1 par M2 ne peut que dégrader le champ dorsal.",`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : 'point': 288, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None} {'jeu': 'go', 'action': 'poser', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': None, 'symbole':
- **T1** : #!/usr/bin/env python3 """normalisation.py — la surface vers des concepts, avant le parseur natif.  Le lexique multilingue connaît les noms de jeux, les pièces, les rangs et les enseignes dans 66 lang

