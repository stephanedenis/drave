# B13 — la phase devinée : 10 % de bruit, 0/20 au but 0

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **83/83 portes** : l'agent reçoit un **signal bruité à 90 %** sur le but. La
> `PolitiqueAppriseVerite4` (136 états-Q) atteint **0/20 au but 0** et **20/20 au but 1** : le
> signal correct 90 % du temps **ne suffit pas**. La trace montre une **boucle** `(3,0) ↔ (4,0)`
> — la Q-table prend la case-goal du signal erroné pour un but, et tourne.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-phase-devine.json`](pensee-phase-devine.json).

## 1. La phase devinée

Même monde que T79, mais la phase n'est **pas donnée** : un signal la désigne avec 90 % de
justesse. La clé contient le **signal** (0/1), pas la phase.

| but | buts | états-Q | pas |
|---|---|---:|---:|
| **0 : (4,4)** | **0/20** | 136 | 200 |
| **1 : (4,0)** | **20/20** | 136 | 4 |

**Ce que ça dit** :

- **10 % de bruit suffisent à casser** : le signal 0 (juste 90 % du temps) mêle le but `(4,4)` au
  but `(4,0)` dans la même clé ; la Q-table donne au `(4,0)` la valeur d'un but (le signal
  erroné), et la politique tourne `(3,0) ↔ (4,0)` au lieu d'aller au `(4,4)`.
- **La trace est explicite** : `(0,0) → (1,0) → (2,0) → (3,0) → (4,0) → (3,0) → …` en boucle ;
  le `(4,0)`'s « gauche » (0,815) bat le « bas » (0,81) d'un cheveu.
- **Le coût du bruit est asymétrique** : le but 0 échoue, le but 1 réussit — l'erreur du signal
  est absorbée quand elle pointe vers le vrai but.
- **La négative est explicite** : 0/20 au but 0.

## 2. Ce que ce banc ne dit pas

- **Un seul look** ; plusieurs looks (vote) réduiraient le bruit (T49/T50).
- **Le bruit est symétrique** (10 %) ; un bruit asymétrique serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- **le tirage du signal** (le test est seedé ; un autre tirage déplacerait le 0/20) ;
- un **but dans la clé** (non : `_cle` ne contient que `(x, y, open, signal)`) ;
- un **A* caché** (non : `seule_verite4` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Vote de signaux** : 3 looks, la croyance vote ; le bruit tombe (le vrai POMDP).
2. **20 graines** : lisser la courbe du seuil.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseVerite4`, `seule_verite4`.
- [`autotest.py`](../tools/pensee/autotest.py) — T80, 83/83.
- [`pensee-phase-devine.json`](pensee-phase-devine.json) — le bilan.
