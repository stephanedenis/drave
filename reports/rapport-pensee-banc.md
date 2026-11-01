# B13 — le banc anytime : l'A* atteint le but en 32 nœuds, l'aléatoire n'y arrive pas

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **10/10 portes** : le banc mesure l'**AUC**, le **regret** et le **budget du but** par problème
> et par stratégie. Sur les cruches, l'**A*** atteint le but en **32 nœuds** (AUC **0,528**,
> regret **0**) quand l'**aléatoire** n'y arrive pas (AUC **0,246**, regret **0,5**) ; sur le
> taquin, l'A* est à **32 nœuds** (AUC **0,624**) contre **0,116** à l'aléatoire.
>
> **Dispositif** : [`banc.py`](../tools/pensee/banc.py), [`taquin.py`](../tools/pensee/taquin.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-banc.json`](pensee-banc.json).

## 1. Le banc

Pour chaque budget croissant, le moteur repart **à froid** ; on lit la meilleure qualité
**visitée** (le score des états du store). Trois nombres :

- **AUC** : moyenne des meilleures qualités aux budgets (1 = parfait) ;
- **regret** : `1 − meilleure qualité au budget maximal` ;
- **budget du but** : premier budget où la qualité atteint 1.

Le score des deux problèmes est `1/(1+distance)` (1 au but) ; l'heuristique est `−distance`.
Le contrôle négatif est une stratégie **aléatoire** de même budget.

## 2. Les cruches

| stratégie | AUC | regret | budget du but |
|---|---:|---:|---:|
| BFS | 0,328 | 0 | 128 |
| greedy | **0,528** | **0** | **32** |
| **A*** | **0,528** | **0** | **32** |
| MCTS-lite | 0,227 | 0,75 | — |
| **aléatoire** | 0,246 | 0,50 | — |

L'A* et le greedy trouvent le but en 32 nœuds ; le BFS en 128 ; le MCTS-lite et l'aléatoire
n'y arrivent pas dans 128 nœuds. L'AUC de l'A* est **2,1×** celle de l'aléatoire.

## 3. Le taquin 3×3 (départ à 8 coups)

| stratégie | AUC | regret | budget du but |
|---|---:|---:|---:|
| BFS | 0,281 | 0 | 1024 |
| greedy | **0,624** | **0** | **32** |
| **A*** | **0,624** | **0** | **32** |
| MCTS-lite | 0,130 | 0,857 | — |
| **aléatoire** | 0,116 | 0,833 | — |

L'A* est **5,4×** l'aléatoire en AUC ; le BFS paie 1024 nœuds ; le MCTS-lite et l'aléatoire ne
trouvent pas le but dans 1024 nœuds.

## 4. Ce que le banc dit — et ce qu'il ne dit pas

**Ce qu'il dit** : à budget égal, une stratégie informée (A*/greedy) atteint le but et une
stratégie sans information (aléatoire, MCTS-lite mal réglé) n'y arrive pas ; le BFS est correct
mais lent ; l'AUC et le regret ordonnent les stratégies.

**Ce qu'il ne dit pas** :

- **A* = greedy** sur ces deux problèmes : le score `1/(1+distance)` contient déjà la distance,
  et l'heuristique `−distance` ajoute la même information. Ce n'est pas une victoire de l'A* :
  c'est une **limite du score**. Un score sans distance (0/1) séparerait A* et greedy.
- **L'AUC est une moyenne** sur une grille de budgets grossière, pas une intégrale continue ;
  une autre grille change le chiffre.
- **Le taquin est un 3×3 à 8 coups** ; un taquin 4×4 ou 20 coups demanderait un autre budget et
  une autre heuristique.
- **Le MCTS-lite est volontairement nu** (pas de rollout, pas de valeur) : son AUC basse est un
  contrôle, pas un verdict sur MCTS.
- **Le score `1/(1+distance)`** est une commodité de banc ; le moteur, lui, ne connaît que les
  scores qu'on lui donne.

## 5. Ce qui pourrait rendre cette fiche fausse

- une grille de budgets qui **favorise** l'A* (les budgets 32/64) ;
- un départ de taquin **trop facile** (8 coups) ;
- un aléatoire **mal seedé** (une graine chanceuse) — la graine 0 est fixe et publiée ;
- un score qui **mélange** la distance et la qualité (c'est le cas, et c'est dit) ;
- un MCTS **non réglé** (le contrôle négatif est faible par construction).

## 6. Fichiers

- [`tools/pensee/banc.py`](../tools/pensee/banc.py) — AUC, regret, budget du but.
- [`tools/pensee/taquin.py`](../tools/pensee/taquin.py) — le taquin 3×3, 8 coups.
- [`tools/pensee/autotest.py`](../tools/pensee/autotest.py) — 10/10.
- [`pensee-banc.json`](pensee-banc.json) — les courbes.
- [`rapport-pensee-drvf.md`](rapport-pensee-drvf.md) — le DRVF, 9/9.
