# B13 — le MLP : 60 poids, l'imitation échoue encore seule

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **27/27 portes** : un **MLP** (2 → 8 → 4, tanh, **60 poids**, rétropropagation manuelle),
> entraîné par **imitation** du professeur (la Q-table de la porte minute sur 23 états), est
> exécuté **seul** : il **échoue** (200 pas, sans but). La couche cachée ne suffit pas ; l'A*
> reste nécessaire.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-mlp.json`](pensee-mlp.json).

## 1. Le MLP

Forward `(x/4, y/4)` → 8 tanh → 4 softmax ; cross-entropy et rétropropagation **manuelles**
(pas de torch dans l'environnement), 500 époques, lr 0,10, imitation du professeur sur les
23 états hors but. Puis exécution **seule**, sans A*.

| politique | poids | buts seuls | pas | A* + sonde (T19) |
|---|---:|---:|---:|---:|
| **MLP** | **60** | **0** | **200** | 28 nœuds |
| réseau linéaire (T23) | 12 | 0 | 200 | 28 nœuds |

**Ce que ça dit** :

- **Le MLP échoue encore** : la couche cachée et la rétropropagation ne suffisent pas à
  reproduire la politique du professeur ; la politique seule tourne.
- **Le professeur est lui-même incomplet** (T21 : la Q-table seule échoue) : l'imitation d'un
  professeur incomplet ne peut pas dépasser le professeur.
- **L'A* reste nécessaire** : c'est lui qui explore et atteint le but (T19).
- **La négative est explicite** : 0 but, 200 pas, 60 poids.

## 2. Ce que ce banc ne dit pas

- **Le MLP est petit** (8 cachés, 23 états) et l'imitation est **hors-ligne** : un apprentissage
  par renforcement ou un professeur **complet** pourrait faire mieux.
- **La rétropropagation manuelle** est correcte mais simple (pas d'Adam, pas de batch).
- **Le labyrinthe 5×5** est un jouet.
- **Le vrai modèle neuronal** reste bloqué (`llama-cli` refusé, pas de poids `drave-n0`).

## 3. Ce qui pourrait rendre cette fiche fausse

- un **professeur incomplet** (T21) : l'imitation hérite de ses limites ;
- une **entrée** trop pauvre (x, y seulement) ;
- un **surapprentissage** ou un **sous-apprentissage** (500 époques) ;
- un **budget** de 200 pas (le MLP tourne, sans but).

## 4. La suite

1. **Professeur complet** : d'abord une Q-table qui réussit seule (T21), puis imitation.
2. **Apprentissage par renforcement** : le MLP apprend par essais, pas par imitation.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueMLP`.
- [`autotest.py`](../tools/pensee/autotest.py) — T24, 27/27.
- [`pensee-mlp.json`](pensee-mlp.json) — le bilan.
