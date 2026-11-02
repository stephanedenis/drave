# Plan de session — S, les structures (analyser, banquer, exporter)

> **Mandat vivant.** Ouvert le 2026-11-02 16 h 19 HNE depuis
> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md) (§ S) et
> [`plan-travail.md`](../../../docs/pilotage/plan-travail.md) § 9.2.
> Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.
> `en-cours` reste la seule source de l'état : ce plan est le **contrat de travail** qui le
> précède, et la section S y est **proposée au hub**, pas écrite ici.

- **Session** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f`
- **Rôle** : **S — les structures** : le banc d'interprétations candidates (outil web, générateur,
  pragmatique, banque), l'**analyseur** (rôles, subordonnées) et l'**export au corpus**.
- **Périmètre** : S (structures) — S-analyseur rôles/subordonnées · S-banque · S-export au corpus.
- **Fichiers réservés** : `tools/structures/` ; `data/structures/` ; `reports/rapport-s-*` ;
  `reports/s-banque-*` ; `journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/`.
- **Heartbeat** : 2026-11-02 16:33 EST
- **Prochaine action** : **validation humaine de la banque** (le mode `banque` est à 0 verdict) ;
  puis la **frontière du GN sans auxiliaire** (h033) et un **gold plus large** (voix, causatives).
- **État** : actif

- **Plan** : 1) ~~plan de session et réservation~~ ; 2) ~~analyseur rôles/subordonnées~~ (gold 39
  phrases, mesure + trois contrôles) ; 3) ~~export au corpus~~ (schéma `statut` + mode gold +
  manifeste) ; 4) ~~tests : 19 verts + 21 nouveaux = 40~~ ; 5) **fiche et manifeste committés**
  (le sous-module `647205a` est committé dans son dépôt ; le pointeur et la fiche restent au hub) ;
  6) **ligne d'état** (section S proposée ci-dessous).
- **Ambition** : que le banc ne soit plus un générateur de candidats seulement **typés** mais un
  analyseur qui **nomme le rôle** et **coupe la subordonnée** — et que la banque sorte du banc
  vers le corpus avec une empreinte qui se rejoue.
- **Stratégie** : petits incréments mesurés (une règle = une phrase du gold), un contrôle négatif
  par mesure (baseline à rôle constant, règles coupées, étiquettes mélangées, spans corrompus),
  40 tests verts ; le sous-module se commite **dans son dépôt** avant de bouger le pointeur.
- **Objectif final** : un **gold de 39 phrases** avec types et rôles attendus, une **mesure**
  reproductible (types, rôles, couverture) et un **corpus exporté** `data/structures/banque.jsonl`
  + manifeste SHA-256, le tout committé et la ligne d'état intégrée par le hub.
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

## Ligne d'état proposée au hub

> Le hub remplace la section S de `en-cours` par ce bloc (et la ligne S de « Ce qui est en
> cours »), puis commite la fiche, le manifeste et le pointeur avec `en-cours`. La session S
> n'écrit pas `en-cours`.

```markdown
### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures : l'analyseur et l'export

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc d'interprétations candidates, l'**analyseur** (rôles,
  subordonnées) et l'**export au corpus**.
- **Plan** : 1) ~~plan et réservation~~ ; 2) ~~analyseur rôles/subordonnées~~ (gold 39 phrases) ;
  3) ~~export au corpus~~ (schéma `statut`, mode gold, manifeste) ; 4) ~~tests : 40~~ ;
  5) **fiche et pointeur intégrés par le hub** ; 6) **ligne d'état**.
- **Ambition** : un analyseur qui **nomme le rôle** et **coupe la subordonnée**, un corpus qui se
  rejoue.
- **Stratégie** : une règle = une phrase du gold, un contrôle négatif par mesure, 40 tests.
- **Objectif final** : gold de **39 phrases**, mesure reproductible, `data/structures/banque.jsonl`
  + manifeste SHA-256, committé.
- **Fait** : types **38/39** (97,4 %), rôles **99/100** (99 %), compléments **45/45**, couverture
  **1 156/1 161** (99,6 %) ; contrôles **64/100**, **66/100**, **0,099** [0,00–0,22] ; échec nommé
  **h033** ; corpus **39 lignes**, SHA `973c70a4…` ; **40 tests** ;
  [`rapport-s-analyseur-roles`](../../reports/rapport-s-analyseur-roles.md).
- **Ce qu'elle fait** : le sous-module **`647205a`** est committé dans son dépôt ; la fiche et le
  manifeste sont prêts ; le mode `banque` est à **0** verdict humain.
- **Ce que font les autres** : le **hub** ; **N2** `0733c5bb` (200 k pas) ; **Pensée**
  `e181ce02` (gold neuronal) ; **D/R/A** `fe3c05f0` (OCR CEGEP).
- **Prochaine action** : **validation humaine de la banque**, puis frontière du GN sans
  auxiliaire (h033) et gold plus large (voix, causatives).
- **Bloquants** : aucun pour l'analyseur et l'export ; la **banque validée** est à 0 verdict
  humain (contenu, nommé).
- **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).
```

Et la ligne de « Ce qui est en cours » :

```markdown
- **S — le banc de structures** : outil web (`tools/structures`), générateur, pragmatique
  (niveaux 0–4), **analyseur rôles/subordonnées 38/39 types, 99/100 rôles, 45/45 compléments**,
  gold **39** phrases, **40 tests** ; corpus **39** structures `data/structures/banque.jsonl`
  (SHA `973c70a4…`) ; fiche [`analyseur-rôles`](../../reports/rapport-s-analyseur-roles.md) ;
  **aucune session DSH**.
```
