# Le moteur de pensée — state store, arbre, stratégies

> **Ce que ce document est.** Le **contrat d'implémentation** du moteur de pensée : les types, le
> **state store**, l'**arbre d'états**, la **boucle** anytime, les **stratégies**, la **trace** et les
> **portes**. La théorie est dans [`pensee-iterative.md`](../theorie/pensee-iterative.md) ; les schémas
> dans [`docs/schemas/`](../schemas/) ; le bloc impulsionnel dans [`diehl-cook.md`](diehl-cook.md).

> **Fiche concept — le moteur.** Un **state store** typé, un **arbre** de nœuds hashés, une
> **frontière**, une **boucle** anytime, un **portefeuille** de stratégies, une **trace** rejouable.
> Le moteur est un bloc N3 `state → state` ou `state → decision` ; il ne lit jamais la surface.

## 1. Les types

| type | contenu | invariant |
|---|---|---|
| `Candidate` | `corps`, `annotation`, `statut`, `provenance`, `cout`, `score` | `corps` canonique ; `H(corps)` stable |
| `State` | `id`, `parent`, `profondeur`, `budget`, `statut`, `candidats`, `frontiere`, `empreinte` | empreinte = Merkle des candidats triés |
| `Node` | `state`, `children`, `score`, `cout`, `visites` | un nœud = un état ; l'arête porte l'opérateur |
| `Proposal` | `operateur`, `params`, `state_parent` | une transition candidate, pas un état |
| `Score` | `valeur`, `cout`, `confiance` | hypothèse, pas vérité |
| `Decision` | `state` settled, `justification`, `budget` | le chemin racine → état est inclus |
| `Trace` | événements `(pas, nœud, opérateur, score, coût, stratégie)` | rejouable, diffable |

**Un candidat** :

```json
{
  "id": "c1",
  "corps": {"modalite": "vision", "glyphe": 7},
  "annotation": {"confiance_pm": 620, "format": "mnist"},
  "statut": "hypothese",
  "provenance": {"operateur": "vision.encode", "parent": "s0", "pas": 3},
  "cout": {"noeuds": 3, "ms": 12},
  "score": 0.62
}
```

**Un état** :

```json
{
  "id": "s3",
  "parent": "s1",
  "profondeur": 3,
  "budget": {"noeuds": 12, "max": 50},
  "statut": "ouvert",
  "candidats": ["c1", "c2", "c3"],
  "frontiere": ["s3", "s5", "s6"],
  "empreinte": "H(c1 ‖ c2 ‖ c3)"
}
```

**La canonicalisation** : clés triées, pas d'espaces, UTF-8, **aucun flottant dans `corps`** ; les
scores et coûts sont dans l'état, pas dans le corps. L'empreinte d'un état est le **Merkle** des
empreintes de ses candidats, **triées** : deux états identiques ont la même empreinte quel que soit
l'ordre d'insertion.

## 2. Le state store

Le store est un **bloc** `state ↔ store` : il persiste, indexe, compacte, rejoue et partage.

| opération | contrat | test |
|---|---|---|
| `put(state)` | rend l'empreinte ; idempotent | deux `put` du même état → même empreinte |
| `get(empreinte)` | rend l'état ou `None` | aller-retour exact |
| `children(empreinte)` | rend les arêtes et les nœuds enfants | l'ordre est stable |
| `frontier()` | rend le tas des nœuds ouverts | le meilleur score en tête |
| `compact(empreinte)` | remplace un sous-arbre par un résumé | la justification reste valide |
| `replay(racine)` | rejoue la trace depuis la racine | mêmes états, mêmes scores |
| `diff(a, b)` | compare deux recherches | premier nœud divergent |

**Le store ne stocke pas que des états** : il stocke les **arêtes** (opérateur, paramètres, coût,
horodatage logique), la **frontière** et les **décisions de stratégie**. Un état sans arête n'est
pas dans l'arbre ; il est orphelin, et le store le signale.

**La compaction** : un sous-arbre peut être remplacé par `{resume, empreinte, justification, cout}`.
Le résumé garde le **corps** de l'état racine du sous-arbre, pas tous ses descendants. Une
compaction qui perd la justification est refusée.

## 3. L'arbre

L'arbre est un **DAG** : deux états de même empreinte sont le même nœud (transposition). Chaque
nœud a un parent, une profondeur, un score, un coût, un nombre de visites. La **frontière** est un
tas ordonné par une politique (score, coût, UCB, heuristique).

![L'arbre d'états](../schemas/pensee-arbre.svg)

**Les invariants** :

1. la racine a `parent = null` et `profondeur = 0` ;
2. un nœud a au plus un parent dans l'arbre, mais peut avoir plusieurs **prédécesseurs** par
   transposition ;
3. la frontière ne contient que des nœuds `ouvert` ;
4. un nœud `settled` n'est plus développé, mais reste dans l'arbre ;
5. le chemin racine → nœud est la **justification** ; il se rejoue.

## 4. La boucle

```python
def boucle(store, strategies, budget, trace):
    racine = store.put(etat_initial())
    store.frontier.push(racine, score=0.0)
    meilleur = racine
    while budget.reste() and store.frontier:
        noeud = strategies.select(store.frontier)      # politique
        if noeud.score > store.get(meilleur).score:
            meilleur = noeud
        propositions = strategies.expand(noeud)         # opérateurs
        for p in propositions:
            enfant = p.appliquer()                     # state -> state
            empreinte = store.put(enfant)
            score = strategies.score(enfant)
            store.edge(noeud, enfant, p.operateur, p.params, score)
            if enfant.statut == "settled":
                trace.settled(enfant, chemin(store, enfant))
            elif budget.reste():
                store.frontier.push(empreinte, score)
            budget.compter(p.cout)
            trace.pas(noeud, enfant, p, score)
    return decision(store, meilleur)
```

**Les interfaces** :

- **opérateur** : `apply(state, params) -> [state]` ; il est typé, tracé, et peut être neuronal,
  classique ou matériel. C'est le seul point d'entrée d'un bloc dans le moteur.
- **stratégie** : `select(frontier) -> node` et `expand(node) -> [proposal]`. Une stratégie ne
  modifie pas l'état ; elle choisit et propose.
- **scoring** : `score(state) -> score` ; il peut être exact (une règle), approché (un réseau) ou
  simulé (un rollout). Un score sans justification est marqué `hypothese`.

**Le moteur ne lit jamais la surface** : il reçoit des états, il rend une décision ou un état
settled. Les opérateurs N1 sont les seuls à voir la surface ; ils sont appelés par le moteur comme
les autres.

## 5. Les stratégies v0

| stratégie | sélection | expansion | arrêt | usage |
|---|---|---|---|---|
| **BFS** | FIFO | tous les enfants | frontière vide | arbre petit, exhaustif |
| **greedy** | meilleur score | tous les enfants | budget | baseline |
| **A*** | `score + heuristique` | tous les enfants | but ou budget | heuristique disponible |
| **MCTS-lite** | UCB | un enfant par rollout | budget | grand arbre |
| **AC-3** | file de contraintes | révision de domaines | point fixe | CSP |
| **alpha-bêta** | profondeur | un coup | profondeur | deux joueurs |

**Le v0 implémente BFS, greedy, A* et MCTS-lite** ; **AC-3** est branché sur la boucle
(`csp.py`) et **alpha-bêta** est le décideur deux joueurs (`jeux.py`), sur les **mêmes** `Etat`,
`Probleme` et opérateurs. La stratégie est un **paramètre** de la trace, pas un type de données.

## 6. La trace

La trace est un flux **DRVF** de profil `thought` : une liste par événement, avec les champs
`nœud`, `parent`, `operateur`, `score`, `cout`, `strategie`, `pas`. Elle ne transporte pas le
`corps` complet à chaque pas : elle transporte l'**empreinte** et la **référence** au store. Le
rejeu recharge les états par empreinte.

**Le profil `thought`** (implémenté dans `trace.py`) : enveloppe `DRVF` (4 octets), version
`u16`, profil `u16 = 1`, longueur `u32`, puis une charge JSON canonique
`{probleme, racine, evenements}`. La racine porte l'état complet ; chaque événement porte
`parent`, `enfant`, `operateur`, `params`, `score`, `cout`, `strategie`, `pas`.

**Le rejeu** : mêmes empreintes, mêmes scores, mêmes décisions ; le `diff` localise le premier
nœud divergent. Un rejeu qui ne redonne pas les mêmes scores n'est pas un rejeu, c'est une
re-exécution. Un score modifié dans le fichier **lève** : une trace est une preuve, pas une
ré-exécution.

## 7. Les portes

| porte | question | critère | contrôle négatif |
|---|---|---|---|
| **T0** | le store est-il canonique ? | aller-retour exact, empreinte stable | deux ordres d'insertion → même empreinte |
| **T1** | l'arbre se rejoue-t-il ? | mêmes états, mêmes scores ; le flux `thought` se relit | une graine changée diverge ; un score corrompu est refusé |
| **T2** | une stratégie est-elle substituable ? | même arbre, deux stratégies, traces comparables | une stratégie qui ne visite rien doit échouer |
| **T3** | le moteur est-il anytime ? | best-so-far non décroissant | un budget nul rend le meilleur courant |
| **T4** | la justification est-elle valide ? | chemin racine → settled | un chemin inventé est refusé |
| **T5** | un solveur se branche-t-il ? | AC-3 sur la boucle, sans toucher au moteur | une contradiction CSP (domaine vide) |
| **T6** | le coût est-il compté ? | nœuds, coupes, budget de l'alpha-bêta | le minimax exact visite plus de nœuds |
| **T7** | le banc anytime est-il mesuré ? | AUC, regret, budget du but ; best-so-far monotone | une stratégie aléatoire a une AUC basse |
| **T8** | les opérateurs sont-ils hétérogènes ? | trois genres, coût, appels, but ; le DRVM rend le bilan | la sonde aveugle n'aide pas |
| **T9** | le neuronal est-il nécessaire ? | le seul opérateur est la sonde ; la bonne politique atteint le but, l'aveugle non | l'aveugle échoue |
| **T10** | le non-linéaire est-il mesuré ? | plusieurs chemins ; la bonne politique utilise la sonde, l'aveugle l'ignore | l'aveugle reste inefficace |
| **T11** | la porte est-elle nécessaire ? | la porte ne s'ouvre que par la bonne politique ; l'aveugle échoue | l'aveugle n'atteint pas le but |
| **T12** | la porte peut-elle être apprise ? | la Q-table apprend la porte ; le modèle la trouve seul | la Q-table part de zéro |
| **T13** | la courbe est-elle plate ? | 5 budgets × 3 graines : le but est atteint, les nœuds stables | la Q-table grandit sans gain |
| **T14** | la politique seule conduit-elle ? | sans A*, la Q-table atteint le but en 8 pas | l'argmax Q suit le chemin |
| **T15** | la porte stochastique tient-elle ? | 80 % d'ouverture ; la politique réessaie | le but est atteint malgré le bruit |
| **T16** | la politique seule résiste-t-elle au bruit ? | sans A*, la Q-table réessaie et atteint le but | 8–10 pas, 1–3 essais |
| **T17** | la porte qui se referme tient-elle ? | la porte se referme après le passage ; le moteur repasse | le but est atteint sans retour |
| **T18** | la porte à un tour tient-elle ? | la porte ne s'ouvre qu'un pas ; la sonde ouvre et passe | le pas/saut ne trichent pas |
| **T19** | la Q-table transfère-t-elle à la porte minute ? | la politique apprise ouvre et passe ; 28 nœuds | la règle fait 27 nœuds |
| **T20** | la politique seule/minute échoue-t-elle ? | sans A*, la Q-table échoue 9/9 | l'A* était nécessaire |
| **T21** | la Q-table entraînée/minute réussit-elle ? | la politique seule atteint le but en 8 pas | (mesure corrigée au round 31) |
| **T22** | le shaping suffit-il ? | le shaping atteint le but en 8 pas | 56 états-Q (corrigé) |
| **T23** | le réseau linéaire généralise-t-il ? | l'imitation échoue ; le réseau seul ne va pas au but | 12 poids, 200 pas |
| **T24** | le MLP généralise-t-il ? | le MLP échoue seul ; l'imitation hérite du professeur incomplet | 60 poids, 200 pas |
| **T25** | le professeur complet réussit-il seul ? | oui : but en 8 pas (mesure corrigée) | 56 états-Q |
| **T26** | la politique sans None réussit-elle ? | oui : but en 8 pas (mesure corrigée) | 56 états-Q |
| **T27** | la mesure corrigée tient-elle ? | minute but/8 ; stable échec/200 | contrôle positif + négatif |
| **T28** | les mesures sont-elles cohérentes ? | 15/15 : but == état final, pas == chemin | la politique minute ne transfère pas au bruit |
| **T29** | le curriculum `open` comble-t-il le trou ? | ouverte but/9 (bruit) et but/8 (stable) | la minute échoue sur le bruit |
| **T30** | le curriculum est-il robuste ? | 5 graines : 5/5 bruits, 5/5 stables | 8–10 pas, 1–3 essais |
| **T31** | la porte mobile est-elle apprise ? | A* 2/2, politique seule but/8 aux deux positions | 170 états-Q |
| **T32** | la porte mobile est-elle robuste ? | 5 graines : 5/5 d0, 5/5 d1 | 147–184 états-Q |
| **T33** | le bruit variable tient-il ? | entraînée à 80 %, 6/6 buts de 50 % à 95 % | l'effort s'adapte (3 → 1 essai) |
| **T34** | la porte qui bouge est-elle suivie ? | porte toutes les 3 pas : A* 28 nœuds, politique but/10 | l'horloge `t % 6` dans l'état |
| **T35** | la porte qui bouge est-elle robuste ? | 5 graines : 5/5 buts en 10 pas | 230–253 états-Q |
| **T36** | la période est-elle apprise ? | entraînée à 3 pas, 4/4 buts de 2 à 5 pas | le rythme, pas la période |

**T5/T6 sont les portes de la modularité et du coût** : AC-3, alpha-bêta et un encodeur RSN doivent
se brancher sur le **même** contrat, sans modifier le moteur. Si l'un demande une exception, le
contrat est faux ; si le coût n'est pas dans la trace, l'anytime est décoratif.

## 8. Le plan v0

| étape | fichier | ce qu'on fait | porte |
|---|---|---|---|
| **0** | `docs/implantation/moteur-de-pensee.md` | ce contrat | — |
| **1** | `tools/pensee/` (`state.py`) | `Candidate`, `State`, canonicalisation, Merkle | T0 |
| **2** | `tools/pensee/` (`tree.py`) | nœuds, arêtes, frontière, transposition, compaction | T1 |
| **3** | `tools/pensee/` (`engine.py`) | boucle, budget, anytime, trace | T1, T3 |
| **4** | `tools/pensee/` (`moteur.py`) | BFS, greedy, A*, MCTS-lite | T2 |
| **4 bis** | `tools/pensee/` (`csp.py`, `jeux.py`) | AC-3, alpha-bêta, minimax | T5, T6 |
| **4 ter** | `tools/pensee/` (`taquin.py`, `banc.py`) | taquin 3×3, AUC/regret, aléatoire | T7 |
| **4 quater** | `tools/pensee/` (`operateurs.py`, `courbe.py`, `audit.py`, `graines.py`) | genres, politiques, DRVM, cadenas, labyrinthe, porte, Q-learning, courbe, politique seule, bruit, portes, transfert, minute, shaping, réseau, MLP, professeur, sans None, correction, audit, curriculum, graines, mobile, bruit variable, porte qui bouge, période | T8–T36 |
| **5** | `tools/pensee/` (`trace.py`) | DRVF `thought`, rejeu, diff | T1, T6 |
| **6** | `tools/pensee/autotest.py` | T0–T36, contrôles négatifs | toutes |

**Le corpus v0** : un jeu de petits graphes (morpion, taquin 3×3, un CSP jouet) et un jeu de
RSN-visuelles déjà produit par N1. Pas de GPU ; le CPU suffit pour 10³–10⁴ nœuds.

## 9. Ce qui rendrait le moteur faux

- **L'empreinte n'est pas canonique** : deux états identiques ont deux empreintes, la
  transposition ne marche pas.
- **Le score n'est pas monotone** : le best-so-far baisse, l'anytime est faux.
- **Le budget n'est pas compté** : le moteur ne peut pas s'arrêter, ni être anytime.
- **La trace ne contient pas les décisions de stratégie** : le rejeu ne redonne pas la recherche.
- **Un opérateur contourne le contrat** : la modularité est décorative.
- **Le moteur lit la surface** : la séparation à trois niveaux est perdue.
- **La justification est reconstruite après coup** : le chemin n'est pas la preuve, c'est un récit.

**La phrase** : un moteur de pensée n'est pas un modèle qui répond ; c'est un **store** qui garde
les états, un **arbre** qui garde les choix, et une **trace** qui garde les raisons.
