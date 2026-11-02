# B13 — l'observation votante : deux looks, 20/20, 1 % d'erreur

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **49/49 portes** : l'action `observer` fait **deux looks** et **vote**. Avec 10 % d'erreur
> par look, l'erreur effective tombe à **1 %** ; la `PolitiqueAppriseVotante` atteint le but
> **20/20** en **8,0 pas**. Le bruit de T45 (0/20) est **absorbé par la répétition**.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-votante.json`](pensee-votante.json).

## 1. L'observation votante

Même monde que T45 (10 % d'erreur par révélation), mais `observer` fait **deux looks** :
s'ils concordent, la croyance est certaine ; s'ils diffèrent, elle reste hésitante (b = 1 ou 2).

| dispositif | buts | états-Q | pas |
|---|---:|---:|---:|
| **votante** | **20/20** | 372 | 8,0 |
| bruitée (T45) | 0/20 | 398 | 200 |
| observatrice (T44) | 20/20 | 448 | 8,3 |

**Ce que ça dit** :

- **La répétition restaure la robustesse** : 0/20 (T45) → 20/20 ; le vote absorbe le bruit
  (1 % d'erreur effective au lieu de 10 %).
- **Le coût est nul** : 8,0 pas (mieux que l'observatrice simple, 8,3) ; la politique observe
  une fois et le vote interne ne coûte pas de pas.
- **La croyance hésitante** (b = 1/2) est un signal : la politique peut réobserver.
- **La table est plus petite** (372 états) : moins d'états, plus de compétence.

## 2. Ce que ce banc ne dit pas

- **Deux looks** ; trois looks donneraient 0,1 % mais coûteraient plus.
- **L'erreur est indépendante** entre les looks ; une erreur corrélée serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **vote qui ne compterait pas** (non : la croyance reflète les deux looks) ;
- un **A* caché** (non : `seule_votante` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Trois looks** : 0,1 % d'erreur ; le coût.
2. **Croyance bayésienne** : mettre à jour la distribution avec la fiabilité.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseVotante`.
- [`autotest.py`](../tools/pensee/autotest.py) — T46, 49/49.
- [`pensee-votante.json`](pensee-votante.json) — le bilan.
