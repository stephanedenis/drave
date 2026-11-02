> **⚠ Correction (2026-11-02, round 31)** : la mesure `seule_minute` avait un bug de
> comparaison (triplet contre couple) et rendait de **faux échecs**. Après correction, cette
> politique **atteint le but en 8 pas**. Les chiffres ci-dessous sont ceux de la mesure
> buguée ; voir [rapport-pensee-correction.md](rapport-pensee-correction.md).

# B13 — la Q-table entraînée sur la minute : la politique seule échoue encore

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **24/24 portes** : la `PolitiqueAppriseMinute`, entraînée **sur la porte minute** (60 états-Q),
> est exécutée **seule** : elle **échoue** en 8 pas. La `seule_minute` s'arrête quand la
> politique ne propose plus d'action ; l'A* + la sonde (T19, 28 nœuds) réussit.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-minute-entrainee.json`](pensee-minute-entrainee.json).

## 1. La Q-table entraînée sur la minute

`PolitiqueAppriseMinute` (Q-learning, 200 épisodes, graine 0) apprend **l'ouverture-passage** :
à `(3,2)`, l'action `bas` passe directement à `(3,3)` (récompense +0,1). Elle est ensuite
exécutée **seule**, sans A*.

| politique | états-Q | buts seuls | pas | A* + sonde (T19) |
|---|---:|---:|---:|---:|
| **apprise minute** | **60** | **0** | **8** | 28 nœuds |

**Ce que ça dit** :

- **Même entraînée sur la minute, la politique seule échoue** : la `seule_minute` s'arrête
  quand la politique ne propose plus d'action ; la Q-table n'a pas la **politique complète**
  (le `propose` renvoie `None` avant le but).
- **L'A* reste nécessaire** : c'est lui qui explore et atteint le but (T19) ; la politique
  seule ne le fait pas, même entraînée.
- **La Q-table apprend l'ouverture-passage** (60 états, +0,1) mais pas la **séquence
  complète** : la récompense +1 au but est trop rare pour la table.
- **La négative est explicite** : 0 but, 8 pas, 60 états-Q.

## 2. Ce que ce banc ne dit pas

- **La Q-table** est tabulaire et petite ; un réseau ou un **reward shaping** pourrait faire
  mieux.
- **La `seule_minute`** s'arrête au `None` : ce n'est pas une erreur de la Q-table seule, c'est
  la **politique incomplète**.
- **Le coût 5** de la sonde n'intervient pas ici.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (200 épisodes, graine 0) ;
- un **A* caché** dans `seule_minute` (non : la boucle n'appelle que la Q-table) ;
- une **Q-table** initialisée (non : elle part de zéro) ;
- un **budget** de 200 pas (le `None` arrive en 8).

## 4. La suite

1. **Reward shaping** : récompenser l'approche de la porte pour compléter la politique.
2. **Réseau** : une politique paramétrique au lieu de la table.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseMinute`.
- [`autotest.py`](../tools/pensee/autotest.py) — T21, 24/24.
- [`pensee-minute-entrainee.json`](pensee-minute-entrainee.json) — le bilan.
