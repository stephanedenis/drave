# B13 — les routes concurrentes : 0/20 au but 0, 20/20 au but 1

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **81/81 portes** : le **but** change à mi-entraînement (le `(4,4)` puis le `(4,0)`) sans être
> dans l'état. La `PolitiqueAppriseVerite2` (86 états-Q) atteint **0/20** au but 0 et **20/20**
> au but 1 : la Q-table ne retient que le **dernier** but. Les routes **concurrentes** ne
> coexistent pas ; la phase **doit** entrer dans l'état.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-concurrentes.json`](pensee-concurrentes.json).

## 1. Les routes concurrentes

Même monde que T77, mais la **phase cachée change le but** : `(4,4)` (bas-droite) ou `(4,0)`
(haut-droite). Les routes partagent le début (la rangée du haut) et divergent à la fin.

| but | buts | états-Q | pas |
|---|---|---:|---:|
| **0 : (4,4)** | **0/20** | 86 | 200 |
| **1 : (4,0)** | **20/20** | 86 | 0 |

**Ce que ça dit** :

- **Le but caché casse la politique** : la Q-table conflate les deux buts ; l'argmax suit le
  **dernier** entraîné (le `(4,0)`), et le `(4,4)` échoue 0/20.
- **Contraste avec T77** : la **porte** cachée marchait (les routes disjointes) ; le **but**
  caché échoue (les routes concurrentes) — c'est la **disjonction** qui compte, pas la cache.
- **86 états** : la politique n'a pas la place de deux buts dans un état unique.
- **La négative est explicite** : 0/20 au but 0.

## 2. Ce que ce banc ne dit pas

- **Deux buts** ; trois ou plus aggraveraient.
- **Les routes partagent la rangée du haut** ; des routes totalement concurrentes seraient pires.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- **le dernier but entraîné** (le `(4,0)` est le phase 1) : l'ordre d'entraînement décide ;
- un **but dans l'état** (non : `_cle` ne le contient pas) ;
- un **A* caché** (non : `seule_verite2` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **But dans l'état** : la phase entre dans `_cle` ; les deux buts coexistent.
2. **20 graines** : lisser la courbe du seuil.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseVerite2`, `seule_verite2`.
- [`autotest.py`](../tools/pensee/autotest.py) — T78, 81/81.
- [`pensee-concurrentes.json`](pensee-concurrentes.json) — le bilan.
