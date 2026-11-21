# L'anti-boucle du moteur de pensée — mesurée, pas promise

> **Ce que ce document est.** Les **cinq gardes** qui empêchent le moteur de pensée de tourner en
> rond, le **rapport de circularité** qu'elles produisent, et les **cinq invariants** qui les
> verrouillent. Le code : [`tools/moteur_pensee.py`](../tools/moteur_pensee.py) ; les tests :
> [`tools/tests/test_moteur.py`](../tools/tests/test_moteur.py) ; le contrat :
> [`moteur-de-pensee.md`](../docs/implantation/moteur-de-pensee.md).

## 1. Le problème

La boucle anytime du contrat (`while budget and frontier`) explore sans garde : elle **re-pousse**
les états déjà vus, elle **re-explore** les échecs connus, elle **ne sait pas** dire si elle
progresse. Une boucle sans garde **tourne en rond par construction** — même avec un arbre parfait.

## 2. Les cinq gardes

| garde | ce qu'elle fait | ce qu'elle compte |
|---|---|---|
| **le `visited` explicite** | un état **exploré** n'est jamais ré-empilé (l'empreinte, pas l'identité) | les répétitions évitées |
| **la nouveauté** | `nouveaux / (nouveaux + répétitions + échecs)` ; sous le seuil (0,30), on arrête | le taux de nouveauté |
| **la mémoire des échecs** | un état `refute` est **exclu** avant d'être empilé, et mémorisé | les échecs évités |
| **trois terminaisons** | le **budget** (le nombre de pas), le **fixpoint** (la frontière vide), la **contradiction** (p et non-p) | la raison de la fin |
| **la trace** | chaque pas est écrit (nouveau / déjà vu / échec / réfuté), rejouable | les pas |

## 3. La mesure (les quatre cas, le 21/11)

| cas | nouveaux | répétitions évitées | échecs évités | contradictions | taux de nouveauté | terminaison |
|---|---:|---:|---:|---:|---:|---|
| **l'opérateur identité** (la boucle pure) | 1 | **1** | 0 | 0 | 0,50 | fixpoint |
| **l'opérateur qui avance** (n → n+1) | 21 | 0 | 0 | 0 | **1,00** | budget |
| **l'échec connu** (le refus revient) | 2 | 0 | **1** | 0 | 0,67 | fixpoint |
| **la contradiction** (p et non-p) | 1 | 0 | 0 | **1** | 1,00 | contradiction |

**La lecture.** La boucle pure produit **une seule** exploration et **compte** la répétition ; le
progrès a un taux de nouveauté de **1,0** ; l'échec est **mémorisé** (1 évité) ; la contradiction
**arrête** le moteur. Chaque garde a son cas, et chaque cas est **mesuré**.

## 4. Les cinq invariants (les tests)

`tools/tests/test_moteur.py` : **5/5**.

1. **la boucle pure** : 1 nouveau, 1 répétition comptée, fixpoint ;
2. **le progrès** : 1,0 de nouveauté, budget ;
3. **la mémoire des échecs** : 1 état réfuté exclu et compté ;
4. **la contradiction** : p et non-p → terminaison ;
5. **la trace** : 10 pas tracés, gardes `{nouveau, deja_vu}`.

## 5. Ce que ça garantit, et ce que ça ne garantit pas

**Garantit** : un état **exploré** n'est plus jamais traité comme neuf ; les échecs sont évités ;
la fin est **nommée** (budget, fixpoint, contradiction, nouveauté) ; tout est **tracé**.

**Ne garantit pas** : que le moteur **atteigne** le but (il peut s'arrêter au budget sans l'avoir) ;
que le **score** soit bon (il est fourni, pas appris) ; que la **stratégie** soit optimale (le tas
est ordonné par le score, la politique est à écrire).

## 6. Le chemin

1. **Le branchement sur l'interface** : le moteur consomme les cinq verbes (`assert`, `query`,
   `promote`, `explain`, `context`) — aujourd'hui il prend des `Etat` bruts.
2. **La stratégie** : le portefeuille (BFS, DFS, A*, MCTS) — le `select`/`expand` du contrat.
3. **Le test sur une question réelle** : une question à réponse connue (la RSN du 21/11), avec le
   taux de nouveauté à chaque pas — c'est la **vraie** mesure de « réfléchir sans tourner en rond ».
