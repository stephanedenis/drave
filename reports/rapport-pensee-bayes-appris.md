# B13 — la vraisemblance apprise : v = 0,899, 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **53/53 portes** : la `PolitiqueAppriseBayesAppris` **estime** la fiabilité de l'observation
> (v = taux de looks corrects) au lieu de la connaître. Elle converge vers **v = 0,899** (le vrai
> 0,9) et atteint le but **20/20** en **8,6 pas**. Le filtre apprend sa propre fiabilité.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-bayes-appris.json`](pensee-bayes-appris.json).

## 1. La vraisemblance apprise

Même monde que T48/T49 (10 % d'erreur par révélation), mais la politique **ne connaît pas** la
fiabilité : elle part de `v = 0,5` et l'estime par le **taux de looks corrects** observés
(`v = n_corrects / n_looks`).

| épisodes | buts | v appris | états-Q | pas |
|---:|---|---:|---:|---:|
| 2000 | 20/20 | 0,889 | 585 | 10,0 |
| **4000** | **20/20** | **0,899** | 660 | 8,6 |
| bayes (T48, v connu) | 20/20 | 0,9 | 552 | 9,4 |

**Ce que ça dit** :

- **La fiabilité s'apprend** : v converge vers 0,899 (le vrai 0,9) ; la politique n'a pas besoin
  qu'on lui donne la qualité de l'observation.
- **Elle réussit** : 20/20 dès 2000 épisodes, 8,6 pas à 4000 (proche du 8,0 du bayésien à deux
  looks).
- **Le coût est l'apprentissage** : 4000 épisodes et 660 états, contre 2000 et 552 pour le
  bayésien à v connu.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **La vraisemblance est stationnaire** ; une fiabilité qui change (l'observation se dégrade)
  demanderait un oubli.
- **Un seul look par observation** ; deux looks affineraient v plus vite.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v mal calibré** (0,899 contre 0,9 ; l'écart est 0,001) ;
- un **A* caché** (non : `seule_bayes_appris` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Fiabilité qui dérive** : v change à mi-parcours ; la politique doit s'adapter.
2. **Deux looks** : v appris plus vite.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesAppris`.
- [`autotest.py`](../tools/pensee/autotest.py) — T50, 53/53.
- [`pensee-bayes-appris.json`](pensee-bayes-appris.json) — le bilan.
