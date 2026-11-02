# B13 — le réseau linéaire : l'imitation échoue, il ne généralise pas seul

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **26/26 portes** : un **réseau linéaire** (x, y, biais → 4 actions, **12 poids**), entraîné par
> **imitation** du professeur (la Q-table de la porte minute sur les 25 états), est exécuté
> **seul** sur la porte minute : il **échoue** (200 pas, sans but). Le réseau ne **généralise**
> pas la politique du professeur ; l'A* reste nécessaire.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-reseau.json`](pensee-reseau.json).

## 1. Le réseau linéaire

Le perceptron prend `(x/4, y/4, 1)` et produit 4 scores ; il apprend l'action du professeur
sur les 25 états (mise à jour +1/-1). 200 époques, 12 poids. Il est ensuite exécuté **seul**,
sans A*.

| politique | poids | buts seuls | pas | A* + sonde (T19) |
|---|---:|---:|---:|---:|
| **réseau linéaire** | **12** | **0** | **200** | 28 nœuds |

**Ce que ça dit** :

- **L'imitation ne suffit pas** : le réseau linéaire apprend des **scores** mais pas la
  **séquence** de la porte minute ; la politique seule échoue.
- **12 poids ne peuvent pas représenter** la politique du professeur (la table a 60 états) ;
  c'est une **sous-capacité**, pas seulement un défaut d'entraînement.
- **L'A* reste nécessaire** : c'est lui qui explore et atteint le but (T19) ; le réseau seul ne
  le fait pas.
- **La négative est explicite** : 0 but, 200 pas, 12 poids.

## 2. Ce que ce banc ne dit pas

- **Réseau linéaire** : un MLP ou un réseau plus large pourrait généraliser ; ce banc teste la
  **capacité minimale**, pas l'idée du réseau.
- **L'imitation** est un perceptron naïf ; une **distillation** avec plus d'époques ou une
  **perte** différente serait plus juste.
- **La `seule_minute`** s'arrête au `None` ou au budget : le réseau tourne.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **réseau sous-entraîné** (200 époques) ;
- une **entrée** trop pauvre (x, y seulement ; pas la porte) ;
- une **Q-table** professeur incomplète (elle aussi échoue seule, T21) ;
- un **budget** de 200 pas (le réseau tourne, sans but).

## 4. La suite

1. **MLP** : une couche cachée, plus de capacité, la même imitation.
2. **Distillation** : entraîner sur les **chemins** du professeur, pas seulement les états.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueReseau`.
- [`autotest.py`](../tools/pensee/autotest.py) — T23, 26/26.
- [`pensee-reseau.json`](pensee-reseau.json) — le bilan.
