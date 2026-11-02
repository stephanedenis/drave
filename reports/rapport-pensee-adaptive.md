# B13 — la fenêtre adaptative : v = 0,8, le régime courant

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **55/55 portes** : sur la fiabilité qui dérive (0,9 puis 0,6), la `PolitiqueAppriseBayesAdaptive`
> **resserre** sa fenêtre quand v change et l'**élargit** sinon. Elle finit à **v = 0,8** — le
> **régime courant**, pas la moyenne — et atteint le but **20/20** en **8,0 pas**.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-adaptive.json`](pensee-adaptive.json).

## 1. La fenêtre adaptative

Même monde que T51 (0,9 puis 0,6), mais `v` est calculé sur les **10 derniers looks** dès qu'ils
diffèrent de plus de 0,2 des 10 précédents ; sinon sur la fenêtre de 50.

| dispositif | buts | v final | états-Q | pas |
|---|---:|---:|---:|---:|
| **adaptative** | **20/20** | **0,8** | 781 | 8,0 |
| fenêtre fixe (T51) | 20/20 | 0,56 | 691 | 8,0 |
| v stable (T50) | 20/20 | 0,899 | 660 | 8,6 |

**Ce que ça dit** :

- **La fenêtre suit le régime courant** : v finit à 0,8 (entre 0,9 et 0,6, mais penché vers le
  récent), là où la fenêtre fixe reste à la moyenne 0,56.
- **Le but est atteint** (20/20, 8,0 pas) : l'adaptation ne casse rien et ne coûte pas de pas.
- **La table grandit** (781 états) : la détection de dérive ajoute des croyances, pas des pas.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Deux régimes** ; une dérive continue serait plus dure.
- **Le seuil 0,2** est un choix ; 0,1 ou 0,3 changeraient la réactivité.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v final 0,8** qui serait un artefact de la fin d'entraînement (le dernier régime est 0,6 ;
  0,8 est entre les deux, pas le 0,6 pur) ;
- un **A* caché** (non : `seule_bayes_adaptive` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Dérive continue** : v glisse lentement ; la fenêtre doit suivre sans à-coups.
2. **Seuil appris** : la politique estime elle-même quand la fiabilité a changé.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesAdaptive`.
- [`autotest.py`](../tools/pensee/autotest.py) — T52, 55/55.
- [`pensee-adaptive.json`](pensee-adaptive.json) — le bilan.
