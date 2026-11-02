# B13 — l'observation à trois looks : 20/20, mais 4000 épisodes

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **50/50 portes** : l'action `observer` fait **trois looks** et vote (10 % d'erreur par look,
> **0,1 %** sur le vote). La `PolitiqueAppriseVotante3` atteint le but **20/20** en **9,2 pas**,
> mais il lui faut **4000 épisodes** (2000 échouent : 0/20). Le vote coûte un pas de plus que
> les deux looks.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-votante3.json`](pensee-votante3.json).

## 1. Les trois looks

Même monde que T46 (10 % d'erreur par révélation), mais `observer` fait **trois looks** et
prend la majorité : l'erreur effective tombe à **0,1 %**.

| épisodes | buts | états-Q | pas |
|---:|---|---:|---:|
| 2000 | **0/20** | 457 | 200 |
| **4000** | **20/20** | 481 | 9,2 |
| 2 looks (T46, 2000) | 20/20 | 372 | 8,0 |

**Ce que ça dit** :

- **Le vote à trois exige plus d'entraînement** : à 2000 épisodes, la politique n'a pas encore
  appris à payer 0,3 pour observer ; à 4000, elle le fait et réussit 20/20.
- **Le coût est visible** : 9,2 pas contre 8,0 (deux looks) ; l'observation plus fiable se paie.
- **Le bruit devient négligeable** (0,1 %), mais le **toy** ne distingue pas 1 % de 0,1 % :
  les deux font 20/20.
- **La négative reste** : à 2000 épisodes, 0/20 ; l'apprentissage est le facteur.

## 2. Ce que ce banc ne dit pas

- **Le toy** (20 exécutions) ne sépare pas 1 % et 0,1 % ; il faudrait 1000 exécutions.
- **Le coût 0,3** est linéaire ; un coût par look différent changerait la politique.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **vote qui ne compterait pas** (non : la majorité des trois) ;
- un **A* caché** (non : `seule_votante3` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **1000 exécutions** : séparer 1 % et 0,1 %.
2. **Croyance bayésienne** : pondérer chaque look par sa fiabilité.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseVotante3`.
- [`autotest.py`](../tools/pensee/autotest.py) — T47, 50/50.
- [`pensee-votante3.json`](pensee-votante3.json) — le bilan.
