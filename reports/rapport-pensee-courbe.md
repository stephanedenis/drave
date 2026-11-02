# B13 — la courbe d'apprentissage : la porte est apprise dès 50 épisodes

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **16/16 portes** : la `PolitiqueApprise` est entraînée sur **5 budgets d'épisodes**
> (50, 100, 200, 400, 800) × **3 graines** (15 runs). **15/15 atteignent le but** en
> **30 nœuds** (coût 68, 7 sondes) ; la Q-table passe de **52 à 83 états**. La porte est
> apprise **dès 50 épisodes** : la courbe est **plate** en performance, pas en taille.
>
> **Dispositif** : [`courbe.py`](../tools/pensee/courbe.py), [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-courbe.json`](pensee-courbe.json).

## 1. La courbe

| épisodes | graines | états-Q (min–max) | nœuds | sonde | coût | buts |
|---:|---:|---:|---:|---:|---:|---:|
| 50 | 0,1,2 | 52–74 | 30 | 7 | 68 | **3/3** |
| 100 | 0,1,2 | 52–74 | 30 | 7 | 68 | **3/3** |
| 200 | 0,1,2 | 61–74 | 30 | 7 | 68 | **3/3** |
| 400 | 0,1,2 | 62–83 | 30 | 7 | 68 | **3/3** |
| 800 | 0,1,2 | 62–83 | 30 | 7 | 68 | **3/3** |

**Ce que ça dit** :

- **La porte est apprise dès 50 épisodes** : 15/15 runs atteignent le but ; le Q-learning
  tabulaire n'a pas besoin de 200 épisodes pour trouver la direction.
- **La performance est plate** (30 nœuds, coût 68) : une fois la porte connue, l'A* fait le
  reste ; les épisodes supplémentaires n'améliorent pas le chemin.
- **La Q-table grandit** (52 → 83 états) : plus d'exploration, plus de couples état-action,
  mais pas de gain de chemin.
- **Les 3 graines convergent** : la porte n'est pas un coup de chance d'une graine.

## 2. Ce que ce banc ne dit pas

- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **La courbe est plate en performance** parce que l'A* complète la politique : un vrai banc
  devrait mesurer **la politique seule** (sans A*), pour voir l'apprentissage.
- **Le coût 5** de la sonde est déclaré.
- **Le labyrinthe 5×5** est un jouet déterministe ; une porte stochastique serait plus dure.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (3 graines testées, toutes réussissent) ;
- un **A* qui masque** la politique (la politique seule n'est pas mesurée) ;
- un **budget** trop grand (le but est atteint en 30 nœuds sur 200) ;
- une **Q-table** initialisée (non : elle part de zéro).

## 4. La suite

1. **La politique seule** (sans A*) : mesurer le taux de but et les nœuds par épisodes.
2. **Porte stochastique** : l'ouverture réussit à 80 % ; la politique doit réessayer.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`courbe.py`](../tools/pensee/courbe.py) — 5 budgets × 3 graines.
- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueApprise`.
- [`autotest.py`](../tools/pensee/autotest.py) — T13, 16/16.
- [`pensee-courbe.json`](pensee-courbe.json) — les 15 runs.
