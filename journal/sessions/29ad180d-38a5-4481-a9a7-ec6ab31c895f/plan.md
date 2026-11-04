# Plan de session — S, les structures (analyser, banquer, exporter)

> **Mandat vivant.** Ouvert le 2026-11-02 16 h 19 HNE depuis
> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md) (§ S) et
> [`plan-travail.md`](../../../docs/pilotage/plan-travail.md) § 9.2.
> Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.
> `en-cours` reste la seule source de l'état : ce plan est le **contrat de travail** qui le
> précède ; sa section S y est **écrite** le 02/11 16 h 52 sur demande humaine, et le hub relit.

- **Session** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f`
- **Rôle** : **S — les structures** : le banc d'interprétations candidates (outil web, générateur,
  pragmatique, banque), l'**analyseur** (rôles, subordonnées) et l'**export au corpus**.
- **Périmètre** : S (structures) — S-analyseur rôles/subordonnées · S-banque · S-export au corpus.
- **Fichiers réservés** : `tools/structures/` ; `data/structures/` ; `reports/rapport-s-*` ;
  `reports/s-banque-*` ; `journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/`.
- **Heartbeat** : 2026-11-04 16:30 EST
- **Prochaine action** : **reprise** : poursuivre la validation sur `/paragraphes` (a001–a003
  faits, 8 restants), puis la rétro-traduction API et les 71 langues.
- **État** : en pause
- **Clôture** : le 04/11 16 h 30 ; le cycle v7 (fait divers, 61/61, 144/144, 56 tests) est
  poussé ; la fiche et l'état sont sur la branche `s/v7`, à fusionner ; la reprise est la
  validation des paragraphes.
- **Reprise** : 2026-11-03 13 h 55 ; le retour humain (arrêt de la validation : arbre trop
  plat, référents non résolus) ouvre le cycle arbre/référents ; la banque partielle garde
  142 verdicts / 81 lectures / 65 phrases.

- **Plan** : 1–4) ~~plan, analyseur (gold 55), export, tests 47~~ ; 5–6) ~~fiche, pointeur,
  état~~ ; 7) **banque partielle** (142 verdicts / 81 lectures / 65 phrases, arrêt humain) ;
  8) ~~arbre + référents + SVG~~ (99 à ≥3, 294/371) ; 9) ~~page `/paragraphes`~~ (52 tests,
  responsive, SVG dans le cadre) ;
  10) ~~traduction 14/14, source anglaise page~~ ; 11) ~~v6 h050/h053/si fort (60/60)~~ ;
  12) **validation des paragraphes**.
- **Ambition** : que le banc ne soit plus un générateur de candidats seulement **typés** mais un
  analyseur qui **nomme le rôle** et **coupe la subordonnée** — et que la banque sorte du banc
  vers le corpus avec une empreinte qui se rejoue.
- **Stratégie** : petits incréments mesurés (une règle = une phrase du gold), un contrôle négatif
  par mesure (baseline à rôle constant, règles coupées, étiquettes mélangées, spans corrompus),
  40 tests verts ; le sous-module se commite **dans son dépôt** avant de bouger le pointeur.
- **Objectif final** : un **gold de 39 phrases** avec types et rôles attendus, une **mesure**
  reproductible (types, rôles, couverture) et un **corpus exporté** `data/structures/banque.jsonl`
  + manifeste SHA-256, le tout committé, fiche, manifeste et ligne d'état.
- **Ce qu'elle fait** : l'analyseur est **38/39 types, 99/100 rôles, 45/45 compléments**,
  couverture **1 156/1 161** ; les contrôles tombent à **64/100** (baseline), **66/100** (règles
  coupées) et **0,099** (rôles mélangés) ; l'échec **h033** est nommé ; le corpus **39 lignes**
  sort avec SHA `973c70a4…` et `verifier_corpus.py` le rejoue ; **40 tests** ; fiche
  [`rapport-s-analyseur-roles`](../../../reports/rapport-s-analyseur-roles.md).
- **Ce que font les autres** : le **hub** `536cd5d6` tient `en-cours`, la roadmap et l'intégration ;
  **N2** `0733c5bb` tient `data/` et les corpus ; **L/B13** (`e181ce02`) reprend le gold neuronal ;
  **D/R/A** (`fe3c05f0`) fait l'OCR CEGEP.
- **Prochaine action (après le cycle)** : la **validation humaine** de la banque (le mode `banque`
  est vide tant qu'elle n'existe pas), la frontière du GN sans auxiliaire (h033), un gold plus
  large (voix, causatives).
- **Bloquants** : **aucun** pour l'analyseur et l'export de référence ; la **banque validée par un
  humain** est un bloquant de *contenu* (0 verdict dans `donnees/validations.jsonl`), nommé et
  contourné par un corpus de **référence** explicitement étiqueté `statut: reference`.
- **Journal** : [la session](../../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).

## La réservation, en clair

Le sous-module est la source ; `data/structures/` est l'export local (tout `data/` est ignoré par
git) ; le chevauchement avec le `data/` de N2 est **nominal** (sous-dossier et fichiers distincts,
le banc ne lit aucun corpus de N2). La banque validée (`donnees/validations.jsonl`) reste dans le
sous-module ; l'export de référence va dans `data/structures/banque.jsonl` et son manifeste est
copié dans `reports/s-banque-structures.json` pour être committé.

## Ligne d'état appliquée

Appliquée à [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md) le 02/11 16 h 52,
sur demande humaine : la section S porte le fait, les contrôles, l'échec `h033` et la prochaine
action ; la roadmap porte la ligne S et la **banque validée à 0**. La session S n'écrit pas
`en-cours` de sa propre initiative ; le hub relit.
