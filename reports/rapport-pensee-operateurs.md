# B13 — les opérateurs hétérogènes : trois genres, un coût, des appels

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **11/11 portes** : le moteur mélange **symbolique**, **numérique** et **neuronal** sur une
> grille 5×5. L'A* atteint le but en **23 nœuds** avec **4 appels** à la politique et un
> **coût 48** ; le contrôle négatif (politique **aveugle**) atteint aussi le but mais la sonde
> n'y sert à rien (**1 nœud**, coût 33). Le **DRVM** rend le bilan (nœuds, genres, coût, appels).
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-operateurs.json`](pensee-operateurs.json).

## 1. Le problème

Grille **5×5**, départ `(0,0)`, but `(4,4)`. Trois opérateurs de genres différents :

| opérateur | genre | coût | ce qu'il fait |
|---|---|---:|---|
| `pas` | **symbolique** | 1 | un pas orthogonal, règle discrète |
| `saut` | **numérique** | 2 | un saut de deux cases |
| `sonde` | **neuronal** | 5 | la politique propose une direction ; **un appel** est compté |

La politique est un **double de contrat** (`PolitiqueManhattan`), pas un modèle : le vrai
modèle natif n'a pas de poids dans cet environnement. Le `DRVM` est le **conteneur d'exécution**
(registre, politique, moteur, trace, bilan) ; il ne faut pas le confondre avec le **format DRVM**
du programme N.

## 2. Les résultats

| stratégie | politique | nœuds | pas | saut | sonde | coût | appels | but |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **A*** | **manhattan** | **23** | 10 | 9 | **4** | **48** | **4** | **oui** |
| A* | aveugle | 20 | 10 | 9 | **1** | 33 | 4 | oui |
| BFS | manhattan | 130 | 63 | 47 | 20 | 257 | 20 | oui |
| BFS | aveugle | 119 | 63 | 47 | 9 | 202 | 20 | oui |

**Ce que ça dit** :

- **Les trois genres coexistent** et sont **tracés** : le registre rend les genres, le bilan
  compte chaque opérateur, le coût est la somme `coût × occurrences`.
- **La sonde sert** avec la politique manhattan : **4 nœuds**, **4 appels**, coût 48 ; sans elle
  (aveugle), elle n'est **presque pas utilisée** (1 nœud) et la recherche résout par `pas`/`saut`
  — le contrôle négatif du **mauvais** opérateur.
- **Le coût est un choix** : l'A* paie 48 pour 23 nœuds, le BFS 257 pour 130 ; le **neuronal**
  est cher (5) et doit être **justifié** par la politique, pas par le moteur.
- **A* = greedy** sur ce score : `1/(1+distance)` contient déjà l'information que l'heuristique
  ajoute ; c'est la limite déjà vue au banc, pas un bug des opérateurs.

## 3. Le DRVM

`DRVM(registre, politique).penser(probleme, strategie, budget)` rend un **instantané** :
`noeuds`, `par_operateur`, `genres`, `cout`, `appels`, `budget`, `but`, `score`, `politique`.
Le conteneur **ne cache pas** le coût : il le rend lisible et **comparable** entre stratégies.

## 4. Ce que ce banc ne dit pas

- **La politique est un double** (manhattan/aveugle), pas un modèle neuronal ; le vrai modèle
  natif est **absent** (pas de poids `drave-n0` dans l'environnement) ; le `NeuronalLLM` local
  reste **refusé**.
- **Le genre neuronal n'est pas prouvé** : c'est le **contrat** d'un opérateur neuronal, pas sa
  qualité ; le coût 5 est une **déclaration**, pas une mesure de latence.
- **A* = greedy** sur ce score ; un score 0/1 les séparerait.
- **Le DRVM** est le **runtime** du moteur, pas le format DRVM de N0 ; le nom est surchargé,
  le rapport le dit.
- **La grille 5×5** est un jouet : un vrai problème hétérogène demanderait des opérateurs qui
  ne se recouvrent pas.

## 5. Ce qui pourrait rendre cette fiche fausse

- une politique **chanceuse** (manhattan) qui ferait croire au gain neuronal ;
- un coût **choisi après** la mesure (5 pour la sonde) : il est déclaré dans le registre ;
- un contrôle **aveugle** qui résout quand même (c'est le cas) : le négatif porte sur
  **l'utilité** de la sonde, pas sur la capacité du moteur ;
- une grille **trop petite** pour que le saut change la décision ;
- une confusion **DRVM runtime / format N** dans la lecture.

## 6. La suite

1. **Politique DRVM** : brancher le modèle natif (N2) comme politique réelle quand ses poids
   seront là ; le `DRVM` est prêt.
2. **Coût mesuré** : remplacer le coût déclaré (5) par la **latence** réelle de la politique.
3. **Opérateurs qui ne se recouvrent pas** : un problème où le neuronal est **nécessaire**
   (pas seulement utile), pour que le contrôle négatif échoue vraiment.
4. **L** : lecture double du gold et cascade avec un vrai modèle.

## 7. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — registre, politiques, DRVM.
- [`autotest.py`](../tools/pensee/autotest.py) — T8, 11/11.
- [`pensee-operateurs.json`](pensee-operateurs.json) — les bilans.
- [`moteur-de-pensee.md`](../docs/implantation/moteur-de-pensee.md) — le contrat.
