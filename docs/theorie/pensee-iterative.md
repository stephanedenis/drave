# La pensée itérative — la RSN plurielle, l'arbre d'états et les stratégies

> **Ce que ce document est.** La **théorie du moteur de pensée** de Drave. La RSN n'est pas un objet canonique
> unique : c'est une **représentation plurielle**, un **ensemble de candidats** qui sert de **mémoire de travail**
> à des **cycles de pensée** multi-niveaux. Penser, c'est **chercher** dans un **arbre d'états**, avec un
> **portefeuille de stratégies** d'IA classique et des **opérateurs** neuronaux ou classiques. Le bus ne transporte
> pas des réponses : il transporte des **états** et des **propositions** typés, tracés et rejouables.
> Les **chiffres** sont dans [`reports/`](../../reports/) ; la **séparation à trois niveaux** dans
> [`modele-natif.md`](modele-natif.md) ; l'**implémentation** dans un document dédié (à venir).

> **Fiche concept — la RSN plurielle.**
> Un **état** est un ensemble de **candidats**. Chaque candidat a un **corps canonique**, une **annotation**
> (confiance, ambiguïté, provenance), un **statut** (hypothèse, retenu, réfuté, ouvert), un **coût** et un
> **score**. L'état a un **parent**, une **profondeur**, un **budget** et une **empreinte** (Merkle des candidats
> triés). La RSN canonique unique est le **résultat d'un cycle**, pas la représentation de travail.
> **Glossaire :** [RSN](glossaire/entrees/representation-semantique-neutre.md) · [couche / étage](glossaire/entrees/couche-etage.md) ·
> [rejeu](glossaire/entrees/rejeu.md)
> **Illustration :** ![La RSN est plurielle](../schemas/pensee-rsn-plurielle.svg)

## 1. Le diagnostic : la RSN unique était un résultat, pas une représentation

La version précédente de l'architecture a fait de la RSN un **quotient canonique** : un corps, une annotation,
une empreinte. C'est **juste pour un candidat** — et c'est **faux pour la pensée**. Un corps unique ne peut pas
porter ce que la pensée exige :

| ce que la pensée exige | ce qu'un corps unique fait |
|---|---|
| **l'ambiguïté** : plusieurs lectures concurrentes | il choisit, ou il met `null` |
| **l'incomplétude** : des champs inconnus, à remplir plus tard | il remplit, ou il échoue |
| **la contradiction** : deux hypothèses incompatibles | il en garde une, ou il plante |
| **le plan** : des futurs alternatifs, des branches | il n'a pas de futur |
| **la provenance** : pourquoi ce candidat, par quel chemin | il a un hash, pas une raison |
| **la révision** : un candidat réfuté, puis restauré | il n'a pas de statut |

**La correction** : la RSN de travail est un **ensemble de candidats** ; le corps canonique est **par candidat** ;
l'état est un **nœud d'arbre**. La RSN canonique unique est le **résultat d'un cycle**, pas la représentation.

**Ce qui ne change pas** : le quotient, l'empreinte, le miroir, la neutralité. Ils s'appliquent **à un candidat**.
Ce qui change, c'est que l'état n'est pas un candidat : c'est un **ensemble ordonné, versionné, hashé**, avec une
frontière et des statuts.

**Ce que ça change pour les trois niveaux** :

- **N1** ne produit pas « la » RSN : il produit des **candidats** (plusieurs lectures, plusieurs formats) ;
- **N2** ne transforme pas « la » RSN : il **filtre, contraint, enrichit** un **état** ;
- **N3** ne répond pas en un pas : il **cherche** dans l'arbre, avec des stratégies, et rend un état **settled**
  ou une **décision**.

## 2. La RSN plurielle

### Le candidat

Un **candidat** est un quotient local, avec un état de recherche :

```json
{
  "id": "c1",
  "corps": {"modalite": "vision", "glyphe": 7},
  "annotation": {"confiance_pm": 620, "format": "mnist", "langue": null, "source": "sha256:…"},
  "statut": "hypothese",
  "provenance": {"operateur": "N1.vision", "parent": "s0", "pas": 3},
  "cout": {"noeuds": 3, "ms": 12, "evenements": 1840},
  "score": 0.62
}
```

Le **corps** reste canonique : deux candidats qui disent la même chose ont le même `H(corps)`. L'**annotation**
reste hors de l'empreinte. Ce qui s'ajoute, c'est le **statut**, la **provenance**, le **coût** et le **score** —
c'est-à-dire la **traçabilité de la recherche**.

### L'état

Un **état** est un ensemble de candidats, plus les métadonnées de la recherche :

```json
{
  "id": "s3",
  "parent": "s1",
  "profondeur": 3,
  "budget": {"noeuds": 12, "max": 50},
  "statut": "ouvert",
  "candidats": ["c1", "c2", "c3", "c4"],
  "frontiere": ["s3", "s5", "s6"],
  "empreinte": "H(c1 ‖ c2 ‖ c3 ‖ c4)"
}
```

**Trois propriétés, et chacune est mesurable** :

1. **canonique** : l'empreinte de l'état est le hash des empreintes de ses candidats, **triées** ; deux états
   identiques ont la même empreinte, même si l'ordre d'insertion diffère ;
2. **versionné** : chaque état a un parent ; la chaîne des parents est la **justification** ;
3. **ouvert** : un état peut être `ouvert`, `settled`, `contradictoire` ou `épuisé` ; le statut est une donnée,
   pas une impression.

![La RSN est plurielle](../schemas/pensee-rsn-plurielle.svg)

**Le quotient reste local.** Le quotient `S/~` décrit **un** candidat ; l'état est un **ensemble de quotients**,
pas le quotient d'un ensemble. C'est la distinction qui manquait : on ne compare pas des états par leur corps,
on les compare par leur **empreinte** et par leur **contenu** (les candidats, leurs statuts, leurs scores).

### Les statuts

| statut | sens | ce qu'il autorise |
|---|---|---|
| `hypothese` | candidat proposé, pas encore évalué | être développé, réfuté, promu |
| `retenu` | candidat qui passe les contraintes | être raffiné, comparé |
| `refute` | candidat contredit par une contrainte ou une preuve | rester dans l'état comme trace |
| `ambigu` | deux candidats non départageables | être tranché par un opérateur ou un budget |
| `ouvert` | ni retenu ni réfuté | attendre |
| `settled` | état stable, plus d'amélioration connue | être rendu comme réponse |

**Un candidat réfuté n'est pas supprimé.** Il reste dans l'état, avec sa raison ; c'est ce qui permet de
**rejouer** la recherche et d'expliquer pourquoi on ne l'a pas choisi.

## 3. L'arbre d'états

**Un nœud est un état.** Une **arête** est l'application d'un **opérateur** (un bloc N1, N2 ou N3, neuronal ou
classique). La **frontière** est l'ensemble des nœuds ouverts. Le **score** est une hypothèse de valeur, pas la
vérité. Le **coût** est mesuré. La **profondeur** est le nombre d'opérateurs depuis la racine.

![L'arbre d'états](../schemas/pensee-arbre.svg)

**Quatre mécanismes, et ils sont tous dans le format** :

1. **transposition** : deux états de même empreinte sont le même nœud ; on mémoïse le sous-arbre, et l'arbre
   devient un **DAG** ;
2. **élagage** : un nœud peut être coupé par une contrainte, un budget, une borne ; il reste dans la trace ;
3. **frontière** : une file de priorité (tas) des nœuds ouverts, ordonnée par score, coût ou une politique ;
4. **justification** : le chemin racine → nœud est la **preuve** de l'état ; il se rejoue.

**Le retour arrière n'est pas un échec** : c'est une arête de plus. Un moteur qui ne sait pas revenir sur un
choix ne pense pas ; il exécute un plan.

**La persistance** : l'arbre est la **mémoire épisodique** de la pensée. Il se stocke, se requête, s'élague, se
compacte ; il se rejoue par l'empreinte de ses nœuds. Un arbre sans trace n'est pas une pensée : c'est un nuage
de nœuds.

## 4. Le cycle de pensée multi-niveaux

Un cycle n'est pas une passe : c'est une **boucle** avec un point d'arrêt explicite.

**Les sept gestes** :

1. **observer** : N1 transforme une surface en candidats (plusieurs lectures) ;
2. **proposer** : N2/N3 génèrent des transitions (raffiner, contraindre, planifier) ;
3. **contraindre** : les contraintes éliminent ou marquent des candidats ;
4. **évaluer** : un score, une preuve, une simulation ;
5. **sélectionner** : une stratégie choisit le prochain nœud/opérateur ;
6. **commettre ou revenir** : on développe, on élague, on backtracke ;
7. **arrêter** : settled, budget, contradiction, méta-décision.

**Trois niveaux de boucle** :

| niveau | ce qu'il choisit | exemple |
|---|---|---|
| **objet** | le prochain candidat/opérateur | raffiner le glyphe 7 |
| **stratégie** | la stratégie de recherche | passer de greedy à MCTS |
| **méta** | la politique de sélection des stratégies | apprendre que MCTS paie sur ce jeu |

**Le cycle est indenté, pas plat** : le niveau stratégie peut suspendre le niveau objet, changer de stratégie,
puis reprendre. La trace garde les deux.

![Le cycle de pensée multi-niveaux](../schemas/pensee-cycle.svg)

**La règle** : un cycle sans **point d'arrêt explicite** est une boucle infinie ; un cycle sans **trace** est une
boîte noire. Les deux sont des bugs, pas des fonctionnalités.

## 5. Le portefeuille de stratégies

Une stratégie n'est pas un algorithme codé en dur : c'est une **politique de choix** sur l'arbre. Le moteur
embarque un **portefeuille**, et le méta-niveau choisit.

![Le portefeuille de stratégies](../schemas/pensee-portefeuille.svg)

| famille | stratégies | ce qu'elles demandent | quand |
|---|---|---|---|
| **non informée** | BFS, DFS, IDDFS | une frontière, un coût | arbre petit, pas d'heuristique |
| **informée** | A*, IDA*, best-first, beam | une heuristique, un coût | heuristique disponible |
| **adversariale** | minimax, alpha-bêta | une alternance, une évaluation | deux joueurs |
| **stochastique** | MCTS/UCT, rollouts | un simulateur, un budget | grand arbre, incertitude |
| **contraintes** | AC-3, forward checking, backtracking | des domaines, des contraintes | CSP |
| **SAT/SMT** | DPLL, CDCL, théories | des clauses, un modèle | preuve, cohérence |
| **planification** | STRIPS/PDDL, HTN, means-ends | des opérateurs, des préconditions | plans |
| **probabiliste** | belief propagation, particle filter | des croyances, des observations | incertitude |
| **locale** | hill climbing, recuit, génétique | un voisinage, un score | optimisation |
| **cas-based** | analogie, réutilisation | des cas, une similarité | expérience |
| **méta** | bandit, portfolio, RL | un historique, une récompense | choisir |

**Le point** : ces stratégies ne sont pas des blocs neufs ; ce sont des **politiques** qui appellent les mêmes
**opérateurs** sur le même **arbre**, avec les mêmes **types**. Le bus ne voit que des états et des propositions.

**Le portefeuille est un bloc N3.** Il a la signature `state → stratégie` (ou `state → décision`), il est tracé,
et il peut être classique (une règle) ou appris (un bandit). La stratégie choisie est un **paramètre** de la
trace, pas un nouveau type de données.

## 6. Ce que la suite doit résoudre

Ce document est le **premier tour** d'une refonte en **dix tours**. Les tours suivants :

1. ~~le diagnostic et la RSN plurielle~~ ;
2. ~~l'arbre d'états~~ ;
3. ~~le cycle de pensée multi-niveaux~~ : observer, proposer, contraindre, évaluer, sélectionner, revenir,
   commettre, arrêter ;
4. ~~le portefeuille de stratégies~~ : recherche non informée, A*, beam, MCTS, alpha-bêta, contraintes, SAT/SMT,
   planification, probabiliste, locale, cas-based, méta ;
5. **le contrat de la pensée** : types `state`, `proposal`, `score`, `constraint`, `decision`, `trace` ;
6. **l'itération indéfinie et l'arrêt** : anytime, budget, settled, contradiction, méta-décision ;
7. **le méta-apprentissage** : choisir la stratégie, apprendre des traces, portfolio ;
8. **la mémoire et le rejeu** : stocker, requêter, compacter, rejouer l'arbre ;
9. **la mesure** : anytime AUC, taux de solution, gap, nœuds, regret, justification, contrôles ;
10. **la révision des documents** : `modele-natif.md`, `diehl-cook.md`, index, schémas, portes.

**Ce qui ne changera pas** : la RSN est un **type**, pas un bloc ; le niveau est un **contrat** ; le bus ne voit
pas des neurones, il voit des types ; la pensée est une **recherche tracée**, pas un forward pass.
