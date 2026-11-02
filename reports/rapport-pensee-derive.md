# B13 — la fiabilité qui dérive : v = 0,56, 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **54/54 portes** : la fiabilité de l'observation **dérive** — 10 % d'erreur sur la première
> moitié de l'entraînement, **40 %** sur la seconde. La `PolitiqueAppriseBayesDerive` estime
> `v` sur une **fenêtre glissante de 50 looks** : elle finit à **v = 0,56** (la moyenne des deux
> régimes) et atteint le but **20/20** en **8,0 pas**.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-derive.json`](pensee-derive.json).

## 1. La fiabilité qui dérive

Même monde que T50, mais la fiabilité **change** : 0,9 sur les 2000 premiers épisodes, 0,6 sur
les 2000 suivants. `v` est le taux de looks corrects sur les **50 derniers** ; il suit la dérive.

| dispositif | buts | v final | états-Q | pas |
|---|---:|---:|---:|---:|
| **dérive (fenêtre 50)** | **20/20** | **0,56** | 691 | 8,0 |
| appris (T50, v stable) | 20/20 | 0,899 | 660 | 8,6 |
| sans mise à jour (T45) | 0/20 | — | 398 | 200 |

**Ce que ça dit** :

- **La fenêtre suit la dérive** : v finit à 0,56, entre les deux régimes (0,9 puis 0,6) ; la
  politique n'est pas restée sur l'ancienne fiabilité.
- **Elle réussit** : 20/20 en 8,0 pas ; la dérive ne casse pas la politique.
- **Le coût est stable** (691 états, 8,0 pas) : la fenêtre n'ajoute que 50 nombres.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Deux régimes** (0,9 puis 0,6) ; une dérive continue serait autre.
- **La fenêtre est fixe** (50) ; 20 ou 200 changeraient la réactivité.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v mal calibré** (0,56 est la moyenne attendue des deux régimes) ;
- un **A* caché** (non : `seule_bayes_derive` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Dérive continue** : v glisse lentement ; la fenêtre doit suivre.
2. **Fenêtre adaptative** : s'élargir quand v est stable, se resserrer quand il bouge.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesDerive`.
- [`autotest.py`](../tools/pensee/autotest.py) — T51, 54/54.
- [`pensee-derive.json`](pensee-derive.json) — le bilan.
