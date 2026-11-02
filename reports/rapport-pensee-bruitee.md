# B13 — l'observation bruitée : 10 % d'erreur casse la politique

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **48/48 portes** : la `PolitiqueAppriseObservatriceBruitee` observe avec **10 % d'erreur**
> (la porte annoncée est fausse une fois sur dix). Elle **échoue 0/20** ; l'observation
> parfaite de T44 (20/20) ne survit pas au bruit. La politique croit une seule révélation ;
> elle ne **répète** pas l'observation.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-bruitee.json`](pensee-bruitee.json).

## 1. L'observation bruitée

Même monde que T44 (porte sautant à 20 %, observation révélée par l'action), mais la
révélation se trompe avec probabilité **0,1** : la croyance est mise à la **mauvaise** porte.

| dispositif | buts | états-Q | pas |
|---|---:|---:|---:|
| **observatrice bruitée (0/20)** | **0/20** | 398 | 200 |
| observatrice (T44) | 20/20 | 448 | 8,3 |
| complète (T39/T40) | 20/20 | 182 | 8 |

**Ce que ça dit** :

- **Le bruit casse la politique** : une seule révélation fausse envoie la politique vers la
  mauvaise porte ; elle ne réessaie pas.
- **La croyance n'intègre pas le bruit** : la politique met la certitude à 1 sur une
  observation bruitée ; il faudrait **répéter** et **compter** (le Bayes).
- **La table est plus petite** (398 états) : la politique a appris moins, pas mieux.
- **La négative est explicite** : 0/20, 200 pas, 398 états-Q.

## 2. Ce que ce banc ne dit pas

- **Une seule observation** ; une politique qui observe **deux fois** pourrait voter.
- **La croyance est discrète** (4 niveaux) ; un filtre bayésien serait plus juste.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (0/20, non) ;
- une **croyance qui corrigerait** le bruit (non : elle passe à 1) ;
- un **A* caché** (non : `seule_observatrice_bruitee` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Deux observations** : observer deux fois, voter ; le bruit tombe à 1 % en majorité.
2. **Croyance bayésienne** : mettre à jour la distribution avec la fiabilité de l'observation.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseObservatriceBruitee`.
- [`autotest.py`](../tools/pensee/autotest.py) — T45, 48/48.
- [`pensee-bruitee.json`](pensee-bruitee.json) — le bilan.
