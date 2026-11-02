# B13 — la phase sur 5 graines : 5/5 buts, 10–14 pas

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **41/41 portes** : la `PolitiqueApprisePhase` (période 3 puis 2, cycle de 10) est entraînée
> (1000 épisodes) sur **5 graines** et exécutée seule. **5/5 atteignent le but** ; le chemin
> reste à **10 pas** sauf une graine à **14 pas**. La Q-table passe de **376 à 422 états**.
>
> **Dispositif** : [`graines.py`](../tools/pensee/graines.py), [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-phase-graines.json`](pensee-phase-graines.json).

## 1. Les 5 graines

| graine | états-Q | but | pas |
|---:|---:|---|---:|
| 0 | 376 | **oui** | 10 |
| 1 | 408 | **oui** | 10 |
| 2 | 422 | **oui** | 10 |
| 3 | 385 | **oui** | 10 |
| 4 | 399 | **oui** | 14 |

**Ce que ça dit** :

- **5/5 buts** : la phase (3 puis 2) est apprise sur toutes les graines ; la politique n'est pas
  un accident de la graine 0.
- **Un détour sur une graine** (14 pas contre 10) : l'exploration de la graine 4 laisse un
  chemin plus long ; le but est atteint quand même.
- **La taille varie** (376–422 états) sans casser le résultat : la structure `t % 10` suffit.
- **La négative reste** : la politique minute (T21/T28) ne connaît pas l'horloge ; la politique
  bouge (T34) ne connaît qu'une période.

## 2. Ce que ce banc ne dit pas

- **5 graines** seulement ; une étude de variance plus large serait plus solide.
- **Une seule séquence** (3 puis 2) ; une période aléatoire serait plus dure.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (5 graines testées, toutes réussissent) ;
- un **cycle codé en dur** dans la politique (non : `t % 10` vient de l'état) ;
- un **A* caché** dans `seule_phase` (non : la boucle n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Période aléatoire** : le rythme change sans préavis.
2. **Plus de phases** : 3, 2, 4, 2 ; la table grandit-elle ?
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`graines.py`](../tools/pensee/graines.py) — `executer_phase`, 5 graines.
- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueApprisePhase`.
- [`autotest.py`](../tools/pensee/autotest.py) — T38, 41/41.
- [`pensee-phase-graines.json`](pensee-phase-graines.json) — les 5 lignes.
