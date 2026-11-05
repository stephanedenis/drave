# Session d300542e — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `d300542e-6e9d-47ac-875b-b44a192eec35` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 14:22 |
| Durée | 1.3 h |
| Tours | 1 |
| Messages | 77 |
| Appels d'outils | 80 |
| Fichiers touchés | 2 |
| Commandes | 62 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : mesurer le **repli « cible vide »** de l'attachement et deux autres retouches déterministes, sans modifier le code du dépôt.  Contexte : `tools/bloc_linguistique.py` (`Heuristique`, `_cible_proche`, `_tete_nom`, `_verbe_dans`, `_tete_texte`), `tools/tests/linguistique/evaluer_gold.py` (`ch … [1938 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : mesurer le … [2218 caractères tronqués]

*80 appels d'outils.* Actions notables :

- bash — Show git state and repo root
- bash — Line counts of key files
- read
- grep
- bash — Hash and list linguistics test dir
- bash — Recent history of bloc linguistique
- bash — Dump gold entries for cited cases
- bash — Dump current syntagme labels for cited cases
- bash — Baseline population and failures diagnostic
- bash — Inspect S generator output internals
- bash — Test verb detection helpers on key spans
- bash — Replicate analyser target logic for s108
- bash — Inspect model candidate scores for key cases
- bash — Exhaustive 145-target analysis
- … et 55 autres

**Synthèse produite :**

⏵ Récapitulatif final et fichiers livrés

**Trois fichiers neufs, aucun fichier existant modifié, aucun commit** (le `M tools/bloc_linguistique.py` du worktree vient d'un autre agent, je n'y ai pas touché) :

- [`tools/tests/linguistique/replis_cible.py`](tools/tests/linguistique/replis_cible.py) — prototype autonome (sous-classe + post-traitement des cibles), non importé ailleurs.
- [`reports/rapport-replis-cible.md`](reports/rapport-replis-cible.md) — fiche : protocole, Q1, tableau par retouche, contrôles négatifs, limites, recommandation.
- [`reports/pensee-replis-cible.json`](reports/pensee-replis-cible.json) — résultats, 145 audits, snapshot A3 137, dérive des empreintes.

**Empreinte mesurée** : `tools/bloc_linguistique.py = 9da6dee7` (105 156 o, 15:22:00), stable pendant le run. Le bloc a bougé pendant la session (`6e843018 → bb020516 → 64b7c520 → 9da6dee7`) : le live a déjà absorbé `g002` (`_repli_cible_gp`), `g012`/`r018` (`_cible_hors_span`) et `r230` (`_sans_enclitique`).

**Baseline live** : 141/145 exact, 143/145 top1, 142/239 top-k strict. **Baseline A3** (snapshot `bb020516`) : 137/145. 

**Q1** : sur 145 → 144 cibles remplies, **1 vide** (`s041`) ; sur 239 → **94 absentes** (48 REL, 33 SUB, 13 GP) + 1 vide = 95 sans cible utilisable. **2 cas nom prédit / verbe gold** : `s108` (`papier` vs `rêve`), `s122` (`papier` vs `saute`) ; sur le snapshot A3 il y avait aussi `r230` (depuis réparé), et 2 cas inverse (`g012`, `r018`, depuis réparés).

| retouche | gain live | régressions | net live | net A3 (137) | recommandation |
|---|---:|---:|---:|---:|---|
| R1 repli cible vide (GP only) | +1 (`s041`) | 0 | **+1** | +2 (`g002`, `s041`) | ✅ intégrer |
| R2 étroite (tête proche, GP) | +2 (`s108`, `s122`) | 0 | **+2** | +4 (forme large, 4 cas) | ✅ intégrer |
| R2 littérale (« préférer un verbe ») | 0 | 3 (`g002`, `g012`, `r018`) | **-3** | 0 | ❌ ne pas intégrer |
| R3 étroite (complétive en tête) | +1 (`r309`) | 0 | **+1** | +1 | ✅ intégrer |
| **combiné** | **+4** | **0** | **+4** | **+7** | **145/145 exact, 145/145 top1** |

Le combiné atteint **145/145 exact (1,0000)** et **145/145 top1** sur les 145, et **145/239 (0,6067)** sur les 239 : le plafond global reste les 94 spans non prédits. La R2 large de A3 donne le même +2 marginal que l'étroite mais change 12 étiquettes (10 hors gold) contre 4 (2 hors gold : `r121`, `r227`) ; la R2 littérale est néfaste (elle défait `g002`/`g012`/`r018`). La R3 large coûte 33 régressions. Le +4 live (contre +7 sur A
… [173 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/replis_cible.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-replis-cible.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Show git state and repo root
- **T1** Line counts of key files
- **T1** Hash and list linguistics test dir
- **T1** Recent history of bloc linguistique
- **T1** Dump gold entries for cited cases
- **T1** Dump current syntagme labels for cited cases
- **T1** Baseline population and failures diagnostic
- **T1** Inspect S generator output internals
- **T1** Test verb detection helpers on key spans
- **T1** Replicate analyser target logic for s108
- **T1** Inspect model candidate scores for key cases
- **T1** Exhaustive 145-target analysis
- **T1** Evaluate candidate rules on 145 targets
- **T1** Test GP-targeted rules and narrow SUB rule
- **T1** Run evaluator against simulated variants
- **T1** Fix simulation post-processing and rerun
- **T1** Count changed labels outside measured set
- **T1** Debug T2 garde variant on s108
- **T1** Inspect modifier source
- **T1** Surface of change by scope
- **T1** List unmeasured changed labels
- **T1** Check normalisation helper
- **T1** Inspect JSON thought-record conventions
- **T1** List unpredicted span ids by type
- **T1** Run the new prototype end to end
- **T1** Inspect concurrent change to bloc linguistique
- **T1** Current fingerprint of bloc
- **T1** Inspect variant gains and baseline failures in JSON
- **T1** Inspect unmeasured changes for key variants
- **T1** Test narrow R2 forms and their surface
- **T1** Re-check current bloc hash and baseline
- **T1** Inspect latest accumulated diff
- **T1** Current baseline failures and key cases
- **T1** Add narrow R2 and start/end fingerprint
- **T1** Locate return section for dynamic recommendation
- **T1** Dynamic recommendation and limits, add no-op control
- **T1** Fix remaining-error computation and check bloc hash
- **T1** Run updated prototype on live bloc
- **T1** Inspect R3 regression and combination details
- **T1** Check verb recognition for R3 guard
- … et 22 autres

## 4. Mesures et résultats marquants

- **T1** `rang0 partout                          n=145 exact=139/145 (base 137) top1=142/145 (base 140) fix=7 reg=5 net=+2`
- **T1** `T1 repli vide rang0                    n=145 exact=139/145 (base 137) top1=142/145 (base 140) fix=2 reg=0 net=+2`
- **T1** `T2 si base nom -> rang0                n=145 exact=139/145 (base 137) top1=140/145 (base 140) fix=2 reg=0 net=+2`
- **T1** `== variantes autour du rang 0 sur les GP ==`
- **T1** `T2b GP base dedans -> rang0            n=145 exact=139/145 (base 137) top1=142/145 (base 140) fix=2 reg=0 net=+2`
- **T1** `T2c GP (nom ou dedans) -> rang0        n=145 exact=141/145 (base 137) top1=142/145 (base 140) fix=4 reg=0 net=+4`
- **T1** `T2d GP rang0 sauf verbe garde          n=145 exact=141/145 (base 137) top1=142/145 (base 140) fix=4 reg=0 net=+4`
- **T1** `T1_rang0               exact=137/239 (0.5732) top1=140/239 (0.5858) span exact=0.9448 top1span=0.9655 fix=0 reg=0 time=1.0s`
- **T1** `T2_rang0               exact=137/239 (0.5732) top1=140/239 (0.5858) span exact=0.9448 top1span=0.9655 fix=0 reg=0 time=1.0s`
- **T1** `T2_rang0_garde         exact=137/239 (0.5732) top1=140/239 (0.5858) span exact=0.9448 top1span=0.9655 fix=0 reg=0 time=1.0s`
- **T1** `T1_rang0               exact=139/239 (0.5816) top1=142/239 (0.5941) span exact=0.9586 top1span=0.9793 fix=2 reg=0 time=0.9s`
- **T1** `T2_rang0               exact=141/239 (0.5900) top1=142/239 (0.5941) span exact=0.9724 top1span=0.9793 fix=4 reg=0 time=0.9s`
- **T1** `T2_rang0_garde         exact=141/239 (0.5900) top1=142/239 (0.5941) span exact=0.9724 top1span=0.9793 fix=4 reg=0 time=0.9s`
- **T1** `T2_rang0_garde total labels 863`
- **T1** `T2_rang0 total labels 863`
- **T1** `T2_rang0_garde   total= 863 changes=  0 dont gold=0 autres=0`
- **T1** `T2_rang0         total= 863 changes=  7 dont gold=4 autres=3`
- **T1** `{'t2': 'rang0'} [('GN', 0, 20, {'role': 'agent', 'niveau': 0}), ('GP', 21, 34, {'role': 'lieu', 'niveau': 1, 'attachement': {'segment': 'sous le nuage', 'cible': 'rêve'}})]`
- **T1** `{'t2': 'rang0_garde'} [('GN', 0, 20, {'role': 'agent', 'niveau': 0}), ('GP', 21, 34, {'role': 'lieu', 'niveau': 1, 'attachement': {'segment': 'sous le nuage', 'cible': 'papier'}})]`
- **T1** `if self.t1=='rang0': cible=cands[0]['texte']`
- **T1** `elif self.t2=='rang0':`
- **T1** `elif self.t2=='rang0_verbe_garde':`
- **T1** `rang0_partout_A3                 exact 139/145 (0.9586) Δ+2 top1 142/145 (0.9793) Δ+2 reg  5 | surface 472 (12 gold / 460 hors)`
- **T1** `e0592c59 B13 — LE CACHE DU CHUNKER APPLIQUÉ : ×139 À 160 RÉPÉTITIONS, SORTIE IDENTIQUE (0/612) ; ×1 EN DÉFAUT, S DOMINE ; 181/181`
- **T1** `== rang0_partout_A3 | exact {'justes': 139, 'n': 145, 'taux': 0.9586, 'gain': 7, 'regressions': 5, 'net': 2} | top1 {'justes': 142, 'n': 145, 'taux': 0.9793, 'gain': 5, 'regressions': 3, 'net': 2} | m`
- **T1** `"R1": {"integrer": True, "forme": "GP seulement, rang 0 du vivier",`
- **T1** `"R2": {"integrer": True, "forme": "rang 0 gardé (verbe gouverneur reconnu "`
- **T1** `rang0_partout_A3                 exact 139/145 (0.9586) Δ-2 top1 142/145 (0.9793) Δ-1 reg  6 | surface 470 (10 gold / 460 hors)`
- **T1** `"forme": "GP seulement, rang 0 du vivier",`
- **T1** `"note": "mesure intermédiaire de ce prototype, avant l'intégration live ; baseline 137 = les 8 erreurs de la fiche A3. R2 y est la forme large (rang 0 gardé), R3 la forme étroite.",`
- **T1** `variantes ['temoin_noop', 'R1_repli_vide_GP', 'R1_repli_vide_tous_non_GV', 'R1_dernier_temoin', 'R1_verbe_lexique_temoin', 'R2_litterale', 'R2_litterale_POS', 'R2_litterale_lexique_etendu', 'R2_large'`
- **T1** `== R1_repli_vide_GP | cible vide sur un GP → rang 0 du vivier (gauche d'abord)`
- **T1** `== R1_dernier_temoin | témoin : dernier candidat au lieu du rang 0`
- **T1** `== R1_verbe_lexique_temoin | témoin : premier verbe reconnu du lexique au lieu du rang 0`
- **T1** `== R2_large | large : GP → rang 0, sauf verbe gouverneur reconnu hors segment (forme qui valait +4 sur le baseline A3)`
- **T1** `== combinaison_R2_large | comparaison : R1 + R2 large (rang 0 gardé) + R3`
- **T1** `== rang0_partout_A3 | contrôle A3 §7.1 : rang 0 pour tous les segments, sans garde`
- **T1** `[still running after 60000ms; moved to background job bash-1491]`

