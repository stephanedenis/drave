# Pensée v0 — le state store, l'arbre hashé et six portes

> **Ligne de roadmap** : B13 (le moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : le
> **state store v0** existe et tient ses six portes — store canonique, rejeu, stratégies
> substituables, anytime, justification — sur un problème jouet qui a un but exact (les deux
> cruches). Ce qui n'est pas fait est nommé : AC-3, alpha-bêta, l'intégration DRVF, et un MCTS
> qui ne trouve pas le but à 200 nœuds.

## Ce que c'est

L'implémentation du contrat [`moteur-de-pensee.md`](../docs/implantation/moteur-de-pensee.md) :

| pièce | fichier | ce qu'elle tient |
|---|---|---|
| types | [`tools/pensee/coeur.py`](../tools/pensee/coeur.py) | `Candidat`, `Etat`, `Noeud`, `Arete`, `Decision` ; JSON **canonique** (clés triées, pas de flottant dans un corps), empreinte **Merkle** des candidats **triés** |
| store | [`tools/pensee/store.py`](../tools/pensee/store.py) | `put/get/edge/children/frontier/compact/chemin`, `Budget`, `Trace`, `replay`, `diff`, `justification_valide` |
| moteur | [`tools/pensee/moteur.py`](../tools/pensee/moteur.py) | la boucle anytime, `Probleme`, `Proposition`, `Strategie` et quatre stratégies (BFS, greedy, A*, MCTS-lite) |
| jouet | [`tools/pensee/cruches.py`](../tools/pensee/cruches.py) | les deux cruches (3 L, 5 L, mesurer 4) avec l'heuristique **exacte** (BFS sur le graphe inversé) |
| portes | [`tools/pensee/autotest.py`](../tools/pensee/autotest.py) | T0–T4 et leurs contrôles négatifs |

**L'arbre est un DAG** : deux états qui portent les mêmes candidats ont la même empreinte, donc le
même nœud — la transposition est gratuite. Le **store est content-addressed** : `put` est
idempotent, `get` rend l'état exact, `chemin` remonte la justification par les arêtes.

## Les six portes, avec leurs contrôles négatifs

| porte | question | résultat | contrôle négatif |
|---|---|---|---|
| **T0** | le store est-il canonique ? | deux ordres d'insertion → **même empreinte** ; aller-retour exact | deux états différents → empreintes différentes ✅ |
| **T1** | l'arbre se rejoue-t-il ? | **93 événements** rejoués sans divergence ; deux exécutions identiques | deux graines MCTS → divergence au premier pas différent ✅ |
| **T2** | une stratégie est-elle substituable ? | BFS et A* atteignent le **même** but | une stratégie qui ne propose rien n'atteint aucun but ✅ |
| **T3** | le moteur est-il anytime ? | best-so-far **non décroissant** sur 5 budgets (0,20 → 1,00) | un budget nul est **refusé** ✅ |
| **T4** | la justification est-elle valide ? | chemin racine → but sur **7 nœuds** | un chemin inventé est **refusé** ✅ |

Commande : `PYTHONPATH=. ~/gpu-env/bin/python -m tools.pensee.autotest` → **6/6 portes tenues**.

## Le jouet, et ce qu'il montre

Les deux cruches ont **24 états**, un but exact (`b == 4`), et une heuristique exacte calculée par
BFS sur le graphe **inversé** (les opérateurs ne sont pas inversibles un pas pour un pas : vider
`(0,4)` donne `(0,0)`, mais remplir `(0,0)` ne redonne pas `(0,4)` — c'est le piège du jouet).

| stratégie | but atteint | nœuds | états du store |
|---|---|---:|---:|
| BFS | **oui** — `(3,4)` | 92 | 14 |
| A* | **oui** — `(3,4)` | 92 | 14 |
| greedy | **oui** — `(3,4)` | 92 | 14 |
| MCTS-lite (200 nœuds) | **non** — `(0,2)` | 200 | 9 |

BFS, A* et greedy trouvent le but ; **MCTS-lite non** à 200 nœuds : un rollout d'un seul enfant
par pas n'a pas le budget pour un but à six coups. C'est une **limite mesurée**, pas une excuse :
le contrat dit MCTS-lite pour les grands arbres, pas pour ce jouet.

## Ce qui n'est pas fait

- **AC-3 et alpha-bêta** : le contrat les prévoit ; ils ne sont pas écrits.
- **L'intégration DRVF** : la trace est une liste typée, pas encore un flux `thought` du format.
- **La compaction** est minimale (un résumé par sous-arbre, justification vérifiée) ; la
  compaction récursive et la reprise de recherche ne sont pas testées.
- **Le scoring neuronal** n'est pas branché : le score est une fonction exacte du jouet.

## Ce qui pourrait le rendre faux

- **Le jouet est le jouet** : 24 états, opérateurs exacts, heuristique exacte. Un arbre large, un
  score bruité ou un opérateur neuronal diraient autre chose des stratégies.
- **Les portes sont celles du contrat**, pas des portes de performance : elles vérifient la
  cohérence (canonique, rejouable, justifiable), pas l'efficacité.
- **MCTS-lite est faible par construction** : une seule proposition par pas, sans rollout.

## Fichiers

- Code : `tools/pensee/{coeur,store,moteur,cruches,autotest}.py`.
- Commande : `python3 -m tools.pensee.autotest`.
- Contrat : [`docs/implantation/moteur-de-pensee.md`](../docs/implantation/moteur-de-pensee.md).
