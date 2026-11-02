# B13 — la politique sans None : elle tourne, sans but

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **29/29 portes** : la `PolitiqueAppriseComplete` **ne renvoie plus `None`** (au but, la
> meilleure action). La `seule_minute` ne s'arrête plus : la politique **tourne** pendant
> **200 pas** et **n'atteint pas** le but. Le `None` n'était pas le problème de fond ; la
> politique apprise reste **incomplète**.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-sans-none.json`](pensee-sans-none.json).

## 1. La politique sans None

Même professeur que T25 (56 états-Q), mais `propose` renvoie **toujours** une action (au but,
l'argmax). La `seule_minute` ne s'arrête donc plus au `None` : elle tourne jusqu'au budget.

| politique | états-Q | buts seuls | pas | A* + sonde (T19) |
|---|---:|---:|---:|---:|
| **sans None** | **56** | **0** | **200** | 28 nœuds |
| avec None (T25) | 56 | 0 | 8 | 28 nœuds |

**Ce que ça dit** :

- **Le `None` n'était pas la cause** : sans lui, la politique **tourne** (200 pas) au lieu de
  s'arrêter ; elle n'atteint toujours pas le but.
- **La politique est incomplète** : la Q-table apprend des actions locales, pas la **séquence**
  de la porte minute.
- **L'A* reste nécessaire** (T19) : c'est lui qui explore et atteint le but.
- **La note de cohérence** : le T25 (l'ancien 8 pas) passe à 200 pas avec ce changement ; sa
  **négative** (échec) reste vraie.

## 2. Ce que ce banc ne dit pas

- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **La politique sans `None`** est une rustine : elle évite l'arrêt, pas l'incomplétude.
- **Le budget** de 200 pas est arbitraire ; un vrai problème demanderait un **critère d'arrêt**.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (1000 épisodes, graine 0) ;
- un **A* caché** dans `seule_minute` (non : la boucle n'appelle que la Q-table) ;
- une **Q-table** initialisée (non : elle part de zéro) ;
- un **budget** plus grand qui laisserait la politique trouver le but par hasard (200, non).

## 4. La suite

1. **Curriculum** : commencer près du but, reculer.
2. **Critère d'arrêt** : une politique qui **s'arrête** au but, pas une rustine.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseComplete.propose`.
- [`autotest.py`](../tools/pensee/autotest.py) — T26, 29/29.
- [`pensee-sans-none.json`](pensee-sans-none.json) — le bilan.
