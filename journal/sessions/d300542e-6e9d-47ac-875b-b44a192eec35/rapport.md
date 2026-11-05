# Session d300542e — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-05/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `d300542e-6e9d-47ac-875b-b44a192eec35` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-05 14:22 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 25 |
| Appels d'outils | 26 |
| Fichiers touchés | 0 |
| Commandes | 16 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : mesurer le **repli « cible vide »** de l'attachement et deux autres retouches déterministes, sans modifier le code du dépôt.  Contexte : `tools/bloc_linguistique.py` (`Heuristique`, `_cible_proche`, `_tete_nom`, `_verbe_dans`, `_tete_texte`), `tools/tests/linguistique/evaluer_gold.py` (`ch … [1938 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : mesurer le … [2218 caractères tronqués]

*26 appels d'outils.* Actions notables :

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
- … et 4 autres

**Synthèse produite :**

⏵ Prototype de simulation par sous-classe et post-traitement des cibles

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

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

