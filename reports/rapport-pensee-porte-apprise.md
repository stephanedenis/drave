# B13 — la porte apprise : la Q-table trouve la porte seule

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **15/15 portes** : la politique **apprise** (`PolitiqueApprise`, Q-learning tabulaire,
> 200 épisodes) découvre la **porte** sans qu'on lui donne sa direction. Elle apprend
> **67 états-Q** et atteint le but en **30 nœuds** (coût 68, 7 sondes). Le modèle n'est plus
> une règle : il a **appris** où ouvrir.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-porte-apprise.json`](pensee-porte-apprise.json).

## 1. L'apprentissage

Le labyrinthe à porte (T11) : la porte `(3,3)` ne s'ouvre que si la politique propose `bas`
depuis `(3,2)`. La `PolitiqueApprise` ne connaît **pas** cette règle : elle apprend par
Q-learning (récompense +1 au but, -0,01 par pas, +0,1 à l'ouverture), 200 épisodes, ε-greedy.

| politique | états-Q | nœuds | sonde | coût | but |
|---|---:|---:|---:|---:|---|
| **apprise (200 épisodes)** | **67** | **30** | **7** | **68** | **oui** |
| manhattan (règle) | — | 28 | 5 | 58 | oui |
| aveugle | — | 200 | 61 | 483 | non |

**Ce que ça dit** :

- **Le modèle apprend la porte** : 67 états-Q suffisent, sans la règle déclarée ; le but est
  atteint en 30 nœuds.
- **Il paie un peu plus que la règle** (68 contre 58, 30 contre 28) : l'apprentissage tabulaire
  est **proche** de la règle, pas identique.
- **L'aveugle reste le négatif** (200 nœuds, sans but) : la Q-table n'est pas l'aveugle.
- **La Q-table est petite** (67 états) : le labyrinthe 5×5 est un jouet, mais il prouve que le
  **modèle** peut être une **table apprise**, pas seulement une règle.

## 2. Ce que ce banc ne dit pas

- **Q-learning tabulaire** sur 5×5 : pas un réseau ; le vrai modèle neuronal reste bloqué
  (`llama-cli` refusé, pas de poids `drave-n0`).
- **Le coût 5** de la sonde est déclaré, pas mesuré.
- **200 épisodes** sont un choix ; la courbe d'apprentissage n'est pas tracée (le prochain banc
  devrait la tracer).
- **La porte est déterministe** ; un vrai problème demanderait une porte **stochastique** ou
  **cachée**.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **surapprentissage** de la graine (200 épisodes, graine 0 : à vérifier sur d'autres graines) ;
- une Q-table **initialisée** par la règle (non : les Q partent à 0) ;
- un budget **trop grand** qui laisserait le hasard trouver la porte ;
- une confusion **Q-learning / politique** : la Q-table est le modèle, la sonde l'opérateur.

## 4. La suite

1. **Courbe d'apprentissage** : tracer le but/nœuds contre les épisodes (50, 100, 200, 400, 800).
2. **Plusieurs graines** : vérifier que la porte est apprise sans chance.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueApprise`.
- [`autotest.py`](../tools/pensee/autotest.py) — T12, 15/15.
- [`pensee-porte-apprise.json`](pensee-porte-apprise.json) — les bilans.
