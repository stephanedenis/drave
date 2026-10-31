# Session b80df26d — Nous sommes dans /home/stephane/GitHub/Q

> **Journaux :** [le jour](../../2026-10-27/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `b80df26d-3dc3-49ea-98b8-fa5a7e0c4cdf` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-27 09:52 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 39 |
| Appels d'outils | 43 |
| Fichiers touchés | 2 |
| Commandes | 34 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Nous sommes dans /home/stephane/GitHub/Qtrinet (dépôt Drave), sprint autonome de 24 h. Tu es un sous-agent chargé de stresser M3 (mémoire de travail) et M4 (mémoire épisodique), sans toucher aux modules déjà confiés à d'autres sous-agents.  État mesuré : - M3 `tools/cerveau/memoire_travail.py` : span 12/12, exact 1,0 ; n-back contrôle 1,0 ; n-back brut très faible (test invalide). - M4 `tools/cerv … [1905 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Nous sommes dans /home/stephane/GitHub/Qtrinet (dépôt Drave), sprint autonome de 24 h. Tu es un sous-agent chargé de str … [2185 caractères tronqués]

*43 appels d'outils.* Actions notables :

- bash — List repo and cerveau directory
- read
- bash — Inspect semantics package and typed_corpus
- bash — Read universaux module
- bash — Find M3/M4 usages and tests
- bash — Inspect existing cerveau tests
- bash — Read batterie harness for M3/M4 baselines
- bash — Read M8 sommeil/prototypes module
- bash — Read pipeline usage of M3/M4
- bash — Run cerveau unit tests baseline
- bash — Corpus statistics for typed items
- bash — List unique codes and pair membership
- bash — Find existing M3/M4 reports
- bash — Locate M3/M4 documentation references
- … et 26 autres

**Synthèse produite :**

⏵ Livraison du rapport M3/M4 et des fichiers de mesures

**Livrables**
- `/tmp/a4-m3-m4.json` — toutes les mesures, courbes, détails et verdicts.
- `/tmp/a4-m3-m4.md` — rapport (protocoles, tableaux, commandes, limites).

**M3 — le 12/12 est tautologique**
- `span=12`, exact 1,0 même avec 40 séquences de **codes aléatoires** : `charger()` copie exactement et `span` ne teste que `n ≤ capacité`. Le n-back « contrôle » à 1,0 vient des 5 premiers items du corpus, qui ont le même code.
- Interférence : 5 cibles + D distracteurs. Similaires (mutants 1 champ) vs dissemblables → **effet 0,0** ; rétention purement FIFO (C=12 : D=8 → 0,8 ; D=10 → 0,4 ; D=12 → 0,0). Proactif → 1,0.
- Bruit : p50(span 12) = **5,5 %** (analytique 5,6 %) ; à p=5 %, champs exacts 99,64 % mais 12 codes exacts 52,5 % → aucune correction d’erreur.
- Saturation : C=3/5/7/12 → span=3/5/7/12, mur net ; débordement = décalage silencieux (0/12 positions originales justes).

**M4 — négatif net : pas de généralisation**
- 528 items → **29 codes uniques**. Le rappel 1,0 est un lookup de doublons ; la complétion 97,9 % se décompose en 72,35 % `vers=None` (15/15) + 27,65 % à 14/15 = 0,9816 : de l’identité.
- Split par code (23 train / 6 test) : codes non stockés rappelés **0/6** ; complétion exacte **0/10** ; **0/7** valeurs de champ inédites. M8 prototypes : **0/7** aussi.
- Fausse mémoire : `exact` strict 0/2412, mais 98,96 % des leurres 1-champ reçoivent une valeur fausse sur le champ modifié. Cue ambigu : marge 0 à 100 %, choix dépendant de l’ordre (55/55). Aucun seuil ne sépare complétion partielle légitime (0,867–0,933) et leurre (0,933).

**Modifications** (additives, existant inchangé) : `memoire_travail.py` (+`pousser`, `distance`, `retrouver`), `episodique.py` (+`classer`, `_marge`, clés `similarite`/`marge`), et les deux nouveaux fichiers de tests (12 tests A4 ; suite complète 58 OK au dernier passage). Aucun git/docs/reports/journal touché.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/memoire_travail.py` | 0 | 2 |
| `/home/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** List repo and cerveau directory
- **T1** Inspect semantics package and typed_corpus
- **T1** Read universaux module
- **T1** Find M3/M4 usages and tests
- **T1** Inspect existing cerveau tests
- **T1** Read batterie harness for M3/M4 baselines
- **T1** Read M8 sommeil/prototypes module
- **T1** Read pipeline usage of M3/M4
- **T1** Run cerveau unit tests baseline
- **T1** Corpus statistics for typed items
- **T1** List unique codes and pair membership
- **T1** Find existing M3/M4 reports
- **T1** Locate M3/M4 documentation references
- **T1** Read M3/M4 state lines in en-cours
- **T1** Read published cerveau measures
- **T1** Prototype held-out and false-memory M4 measurements
- **T1** Fix invalid blanked fields and rerun prototype
- **T1** Run full M4 held-out and false-memory protocol
- **T1** Run M3 interference, noise, saturation protocol
- **T1** Fix distractor collisions and rerun M3 protocol
- **T1** Debug retention computation
- **T1** Run cerveau tests after additive changes
- **T1** Run final consolidated M3/M4 measurements and write JSON
- **T1** Summarize final JSON measurements
- **T1** Recompute absent near-miss lure stats and update JSON
- **T1** Add hard M3/M4 tests and run full suite
- **T1** Fix ambiguous-code fixture and rerun tests
- **T1** Write final markdown report
- **T1** Add metadata to JSON and verify tests
- **T1** Inspect test discovery duplication
- **T1** Locate test count references in MD
- **T1** Correct test counts in deliverables
- **T1** Run A4 tests and full suite final validation
- **T1** Fix A4 test counts in deliverables

## 4. Mesures et résultats marquants

- **T1** `56:  70,8 %), **M4 mémoire épisodique 1,0** (complétion 97,9 %, séparation 1,0), **M3** tampon 12/12 et n-back contrôle 1,0 ;`
- **T1** `60:- **B12 pipeline** — **M1 → M4 → M8** : **528/528** surfaces, **7** prototypes, **96,33 %** de complétion`
- **T1** `[still running after 60000ms; moved to background job bash-1486]`
- **T1** `M4 ne generalise pas au-dela des codes stockes : table de hachage exacte ; les 97.9% de completion sont de l'identite de doublons (72.35% vers=None + 27.65% a 14/15).`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : items 528 codes 29 vers None 382 0.7234848484848485 completion_champs attente 0.9815656565656565 codes uniques list 29 train/test codes 24 5 test: [('echecs', 'deplacer', {'jeu': 'echecs', 'action': '
- **T1** : items 528 codes 29 vers None 382 0.7234848484848485 completion_champs attente 0.9815656565656565 codes uniques list 29 train/test codes 24 5 test: [('echecs', 'deplacer', {'jeu': 'echecs', 'action': '

