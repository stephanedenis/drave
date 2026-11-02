# B13 — la porte mobile : deux positions, une seule politique

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **34/34 portes** : la porte peut être à `(3,3)` (le haut) ou à `(1,3)` (la gauche). L'**A*** la
> trouve aux deux positions (29 nœuds, sonde 5, coût 60/59) ; la `PolitiqueAppriseMobile`
> (170 états-Q) **atteint le but seule en 8 pas aux deux positions**. L'état porte la position
> de la porte : la politique **généralise** au lieu d'apprendre deux chemins.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-mobile.json`](pensee-mobile.json).

## 1. La porte mobile

Deux labyrinthes jumeaux : la porte est à `(3,3)` (route du haut, par `(3,2)`) ou à `(1,3)`
(route de gauche, par `(0,3)`). La case de l'autre porte est **libre**. L'état est
`(x, y, open, d)` où `d` est la position de la porte.

| d | A* + sonde | politique seule | états-Q |
|---|---|---:|---:|
| 0 (porte 3,3) | but, 29 nœuds, sonde 5, coût 60 | **but/8** | 170 |
| 1 (porte 1,3) | but, 29 nœuds, sonde 5, coût 59 | **but/8** | 170 |

**Ce que ça dit** :

- **La politique généralise** : une seule Q-table (170 états, `d` dans l'état) réussit aux deux
  positions ; elle n'apprend pas deux politiques séparées.
- **L'A* aussi** : la sonde ouvre la porte visée, la route est trouvée aux deux positions.
- **Le coût est stable** (59–60) : la porte mobile ne coûte pas plus cher que la porte fixe
  (57–58).
- **La mobilité est gratuite en états** : 170 états pour deux labyrinthes, contre 56–74 pour un
  seul ; la structure `d` dans l'état porte l'information.

## 2. Ce que ce banc ne dit pas

- **Deux positions** seulement ; une porte qui se déplace **pendant** l'épisode serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **La porte** est connue à l'état initial ; une porte **cachée** demanderait une exploration.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (1000 épisodes, graine 0 ; à vérifier sur plusieurs graines) ;
- un **A* caché** dans `seule_mobile` (non : la boucle n'appelle que la Q-table) ;
- une **position codée en dur** dans la politique (non : `d` vient de l'état) ;
- une **case de l'autre porte** qui ne serait pas libre (le `_libre_pmob` la libère).

## 4. La suite

1. **Plusieurs graines** : la porte mobile tient-elle hors graine 0 ?
2. **Porte qui bouge** : `d` change en cours d'épisode ; l'état doit suivre.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PORTES_MOBILE`, `LABYRINTHE_PORTE_MOBILE_*`,
  `PolitiqueAppriseMobile`, `seule_mobile`.
- [`autotest.py`](../tools/pensee/autotest.py) — T31, 34/34.
- [`pensee-mobile.json`](pensee-mobile.json) — les deux positions.
