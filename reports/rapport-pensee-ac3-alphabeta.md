# B13 — AC-3 et alpha-bêta : la contrainte propage, le jeu coupe

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **8/8 portes** : T0–T4, puis **AC-3** (chaîne, carte arc-consistante, contradiction) et
> **alpha-bêta** (gain en un coup, blocage, profondeur 1 qui rate). **Alpha-bêta visite
> 1 495 nœuds et coupe 296 fois là où le minimax exact en visite 18 730** — même décision, coût
> divisé par **12,5**.
>
> **Dispositif** : [`csp.py`](../tools/pensee/csp.py), [`jeux.py`](../tools/pensee/jeux.py),
> [`autotest.py`](../tools/pensee/autotest.py), contrat
> [`moteur-de-pensee.md`](../docs/implantation/moteur-de-pensee.md) ; les types `Etat`,
> `Probleme`, `Decision`, `Store`, `Trace`, `Budget` sont **les mêmes** que le moteur v0.

## 1. La question

Le state store v0 et la boucle anytime (BFS, greedy, A*, MCTS-lite) tenaient **6/6 portes**.
Restait la promesse du contrat : **AC-3** (propagation de contraintes) et **alpha-bêta**
(décision deux joueurs) sur le **même arbre** et les **mêmes opérateurs** — sans ajouter une
exception au moteur.

La réponse est **oui pour AC-3** (c'est une `Strategie` branchée sur la boucle) et **oui pour
alpha-bêta au niveau des types** (il partage `Etat`, `Probleme`, `Decision`, `Store`, `Trace`) —
mais alpha-bêta n'est **pas** une stratégie de la boucle anytime : la valeur remonte l'arbre,
alors que la boucle la propage vers l'avant. C'est un **décideur** deux joueurs, et le rapport
le dit au lieu de le cacher.

## 2. AC-3 : la chaîne propage, la carte ne se réduit pas

### 2.1 La chaîne

CSP : `A ∈ {r}`, `B ∈ {r,g}`, `C ∈ {r,g}` ; `A ≠ B`, `B ≠ C`.

| étape | domaines |
|---|---|
| départ | A {r}, B {r,g}, C {r,g} |
| A ≠ B | B perd `r` → B {g} |
| B ≠ C | C perd `g` → C {r} |
| point fixe | **A {r}, B {g}, C {r}** |

Deux valeurs retirées, **arc-consistance vraie**, solution `A=r, B=g, C=r` trouvée par
`resoudre`, état `settled`. La stratégie `AC3` tient la file des arcs, révise, empile les
voisins ; l'opérateur `retirer` est le seul opérateur ; la trace est celle du moteur.

### 2.2 La carte

Carte d'Australie : 7 variables, 3 couleurs, 9 contraintes `≠`. **AC-3 ne retire rien** : la
carte est déjà arc-consistante (chaque valeur a un support chez chaque voisin). Le point fixe
reste à 3 valeurs par variable, et `resoudre` trouve une solution
(`WA=g, NT=b, SA=r, Q=g, NSW=b, V=g, T=b`).

C'est un **contrôle**, pas un échec : AC-3 ne prouve pas une solution, il **réduit** ; quand il
n'y a rien à réduire, il ne dit rien. Le backtracking est le solveur ; AC-3 est le
pré-traitement.

### 2.3 La contradiction

CSP : `A ∈ {r}`, `B ∈ {r}`, `A ≠ B`. AC-3 retire `r` de A (aucun support), puis B reste `{r}` ;
le domaine de A est **vide** ; `resoudre` rend `None`. La contradiction est **vue**, pas
devinée.

## 3. Alpha-bêta : gagner, bloquer, couper

### 3.1 Gagner en un coup

Plateau `X X . / O O . / . . .`, X au trait. Alpha-bêta (profondeur 9) joue **case 2** et X
gagne. La décision porte le chemin racine → coup, la trace et le budget.

### 3.2 Bloquer

Plateau `X . . / O O . / X . .`, X au trait ; O menace la case 5. Alpha-bêta joue **case 5**
(blocage). Le **contrôle négatif** — profondeur 1, évaluation nulle — joue **case 1** : il ne
voit pas la menace. C'est la différence entre une évaluation et une recherche.

### 3.3 Couper

Plateau vide, profondeur 5, budget 200 000 :

| décideur | nœuds | coupes | premier coup |
|---|---:|---:|---|
| **alpha-bêta** | **1 495** | **296** | 0 |
| minimax exact | **18 730** | 0 | 0 |

Même décision, **12,5× moins de nœuds**. La coupe est comptée (`coupes`), le budget est compté
(`budget_consomme`), la trace porte chaque arête évaluée. Le minimax exact est le contrôle :
même valeur, plus de nœuds.

## 4. Les portes

| porte | résultat |
|---|---|
| T0 store canonique | ✅ |
| T1 rejeu | ✅ 93 événements identiques |
| T1 graine | ✅ deux graines divergent |
| T2 stratégies | ✅ BFS et A* atteignent le but ; l'aveugle échoue |
| T3 anytime | ✅ best-so-far non décroissant |
| T4 justification | ✅ chemin valide ; chemin inventé refusé |
| **T5 AC-3** | ✅ chaîne, carte, contradiction |
| **T6 alpha-bêta** | ✅ gain, blocage, profondeur 1 qui rate, coupe |

**8/8**. Les portes T5/T6 du contrat — « un opérateur se branche », « le coût est compté » —
sont ici **instanciées** par AC-3 (solveur branché) et alpha-bêta (nœuds/coupes comptés).

## 5. Ce que cette fiche ne dit pas

- **AC-3 n'est pas un solveur** : il réduit les domaines ; la carte le montre (aucune réduction
  sur un CSP déjà arc-consistant) ; le backtracking reste nécessaire.
- **La chaîne est petite** : 3 variables, 2 contraintes ; c'est un test de propagation, pas une
  campagne CSP.
- **Le morpion est petit** : 9 cases, profondeur 9 pour les coups gagnants/blocages, profondeur 5
  pour la comparaison de coupe ; un jeu plus grand demanderait une table de transposition et une
  évaluation.
- **Alpha-bêta n'est pas la boucle anytime** : il partage les types et les opérateurs, pas la
  boucle ; le contrat le dit, et la porte T2 (stratégie) ne le confond pas avec une stratégie.
- **Le DRVF n'est pas encore branché** : la trace a les événements, le rejeu du moteur v0 existe ;
  l'écriture du flux `thought` et le diff restent à faire.
- **Le banc anytime** (AUC, regret) n'est pas mesuré ici : il vient après le DRVF.

## 6. Ce qui pourrait rendre cette fiche fausse

- un CSP où le point fixe d'AC-3 est une **impasse** sans domaine vide (arc-consistance ≠
  solution) — la carte en est un cas bénin, un cas pathologique serait un contre-exemple ;
- une contradiction que l'ordre des arcs **ne voit pas** (le test ne couvre qu'un cas) ;
- un jeu où l'évaluation de profondeur 0 **trompe** alpha-bêta (le morpion gagne/bloque avec une
  recherche profonde, mais un jeu plus grand dépend de l'évaluation) ;
- un budget qui **tronque** la recherche et change le coup (le test utilise un budget suffisant) ;
- une trace qui **ne permet pas** de rejouer alpha-bêta (le store enregistre les arêtes, le rejeu
  du décideur n'est pas encore testé).

## 7. Fichiers

- [`tools/pensee/csp.py`](../tools/pensee/csp.py) — CSP, AC-3, carte, chaîne, contradiction.
- [`tools/pensee/jeux.py`](../tools/pensee/jeux.py) — morpion, alpha-bêta, minimax.
- [`tools/pensee/autotest.py`](../tools/pensee/autotest.py) — 8/8 portes.
- [`moteur-de-pensee.md`](../docs/implantation/moteur-de-pensee.md) — le contrat.
- [`rapport-pensee-v0.md`](rapport-pensee-v0.md) — le state store et la boucle, 6/6.
