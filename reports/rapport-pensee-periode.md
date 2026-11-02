# B13 — la période variable : 2–5 pas, la même politique

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **39/39 portes** : la `PolitiqueAppriseBouge` est entraînée avec la porte qui bouge **toutes
> les 3 pas**, puis testée **seule** avec des périodes de **2, 3, 4 et 5 pas**. Elle atteint le
> but **4/4**, en **10 pas** à chaque fois. La politique a appris l'horloge, pas une période.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-periode.json`](pensee-periode.json).

## 1. La période variable

Même labyrinthe à deux portes que T34/T35 ; la porte alterne `(3,3)`/`(1,3)` avec une période
`P`. L'entraînement utilise `P = 3` ; l'évaluation change `P` sans réentraîner.

| période | but | pas |
|---:|---|---:|
| 2 | **oui** | 10 |
| 3 | **oui** | 10 |
| 4 | **oui** | 10 |
| 5 | **oui** | 10 |

**Ce que ça dit** :

- **4/4 buts** : la politique entraînée à 3 pas **généralise** aux périodes 2, 4, 5 ; elle n'a
  pas mémorisé une période, elle a appris le **rythme** (l'horloge dans l'état).
- **Le chemin est stable** (10 pas partout) : le coût de la période est nul sur ce labyrinthe.
- **La structure bat la taille** : une seule table (236 états) couvre quatre périodes.
- **La négative reste** : la politique minute (T21/T28) ne connaît pas l'horloge.

## 2. Ce que ce banc ne dit pas

- **Périodes 2–5** seulement ; 6, 8, 10 changeraient la difficulté.
- **La période est fixe** pendant un épisode ; une période qui change serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **période codée en dur** dans la politique (non : `self.periode` est un paramètre) ;
- une **graine chanceuse** (1000 épisodes, graine 0 ; T35 montre 5/5 sur 5 graines à P=3) ;
- un **A* caché** (non : `seule_bouge` n'appelle que la Q-table) ;
- un **état qui contiendrait la période** (non : l'état porte `t % 6`, pas `P`).

## 4. La suite

1. **Période qui change** en cours d'épisode : l'état doit suivre.
2. **Porte aléatoire** : la position change sans période.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBouge(periode=…)`, `_d_bouge(t, P)`.
- [`autotest.py`](../tools/pensee/autotest.py) — T36, 39/39.
- [`pensee-periode.json`](pensee-periode.json) — les quatre périodes.
