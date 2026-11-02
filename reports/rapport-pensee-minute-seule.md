# B13 — la politique seule sur la porte minute : elle échoue, l'A* était nécessaire

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **23/23 portes** : la `PolitiqueApprise` entraînée sur la porte **déterministe** est exécutée
> **seule** sur la porte **à un tour** : elle **échoue 9/9** (200 pas, sans but). L'A* + la sonde
> réussissait (T19, 28 nœuds) ; sans l'A*, la Q-table ne sait pas **ouvrir et passer dans le
> même pas**.
>
> **Dispositif** : [`courbe.py`](../tools/pensee/courbe.py), [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-courbe.json`](pensee-courbe.json).

## 1. La politique seule sur la minute

À l'état `(3,2)`, la politique propose une direction ; la porte minute exige **ouverture et
passage dans le même pas** ; la politique seule ne le fait pas : elle **tourne** ou s'arrête,
sans atteindre le but en 200 pas.

| épisodes | graines | buts seuls | pas | A* + sonde (T19) |
|---:|---:|---:|---:|---:|
| 50 | 0,1,2 | **0/3** | 200 | 28 nœuds |
| 100 | 0,1,2 | **0/3** | 200 | 28 nœuds |
| 200 | 0,1,2 | **0/3** | 200 | 28 nœuds |

**Ce que ça dit** :

- **La politique seule échoue** sur la porte minute : la Q-table a appris la porte stable, pas
  l'ouverture-passage d'un tour.
- **L'A* était nécessaire** : c'est lui qui explore et trouve la séquence ouverture-passage ;
  la politique seule ne la connaît pas.
- **Le transfert a une limite** : la Q-table transfère à la porte stochastique (T16) mais pas à
  la porte minute seule ; le **contexte temporel** n'est pas dans sa table.
- **La négative est explicite** : 9/9 échecs, 200 pas ; la porte T20 vérifie l'échec, pas la
  réussite.

## 2. Ce que ce banc ne dit pas

- **La Q-table** n'a pas été entraînée sur la porte minute : c'est un **transfert** raté, pas une
  preuve que l'apprentissage est impossible.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le coût 5** de la sonde n'intervient pas ici.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** qui réussirait (9/9 échecs, non) ;
- un **A* caché** dans `seule_minute` (non : la boucle n'appelle que la Q-table) ;
- une **politique** initialisée avec la porte minute (non : elle vient du déterministe) ;
- un **budget** de 200 pas (le but n'est pas atteint).

## 4. La suite

1. **Entraîner sur la porte minute** : la Q-table apprend-elle l'ouverture-passage ?
2. **Porte mobile** : la porte change de case ; la politique doit s'adapter.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`courbe.py`](../tools/pensee/courbe.py) — `seule_minute()`, la politique sans A* sur la minute.
- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueApprise`, `LABYRINTHE_PORTE_MINUTE`.
- [`autotest.py`](../tools/pensee/autotest.py) — T20, 23/23.
- [`pensee-courbe.json`](pensee-courbe.json) — les 15 runs avec `min_but`/`min_pas`.
