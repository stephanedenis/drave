# B13 — le vote de signaux : 5 looks, toujours 0/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **84/84 portes** : la croyance **vote** sur 3, 5 ou 9 looks (majorité). Le bruit du signal tombe
> de 10 % à 0,9 % — et la politique **échoue toujours 0/20 au but 0** : le problème n'est **pas**
> le bruit, c'est le **cycle structurel** `(3,0) ↔ (4,0)`.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-vote.json`](pensee-vote.json).

## 1. Le vote

Même monde que T80, mais la phase est décidée par un **vote majoritaire** de 3, 5 ou 9 looks.

| looks | erreur de vote | but 0 | but 1 |
|---|---:|---:|---:|
| 3 | 2,8 % | **0/20** | 20/20 |
| 5 | 0,9 % | **0/20** | 20/20 |
| 9 | 0,1 % | **0/20** | 19/20 |

**Ce que ça dit** :

- **Le vote ne corrige rien** : l'erreur passe de 10 % à 0,1 %, le 0/20 reste. Le bruit n'est pas
  la cause.
- **La cause est le cycle** : la trace de T80 montrait `(3,0) ↔ (4,0)` ; elle est **identique**
  avec 5 looks. Le `(4,0)` est un **but** en phase 1 et une **case vide** en phase 0 : sa valeur
  est à la fois reward et chemin, et l'argmax tourne.
- **La Q-table est stale** : le `(3,0)`'s « droite » (1,708) n'est pas mis à jour quand le
  `(4,0)`'s best descend à 0,815 ; le cycle se self-entretient.
- **La négative est explicite** : 0/20 au but 0, même à 0,1 % d'erreur.

## 2. Ce que ce banc ne dit pas

- **Le cycle** pourrait être cassé par un **reward négatif** au `(4,0)` hors phase, ou par la
  phase dans l'état (T79).
- **Un seul tirage** ; 20 graines confirmeraient.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- **le tirage du signal** (le test est seedé) ;
- un **but dans la clé** (non : `_cle` ne contient que `(x, y, open, vote)`) ;
- un **A* caché** (non : `seule_verite5` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Casser le cycle** : reward négatif au `(4,0)` hors phase, ou la phase dans l'état.
2. **20 graines** : lisser la courbe du seuil.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseVerite5`, `seule_verite5`.
- [`autotest.py`](../tools/pensee/autotest.py) — T81, 84/84.
- [`pensee-vote.json`](pensee-vote.json) — le bilan.
