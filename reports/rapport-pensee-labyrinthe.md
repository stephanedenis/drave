# B13 — le labyrinthe non linéaire : la bonne politique utilise la sonde, l'aveugle l'ignore

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **13/13 portes** : sur un **labyrinthe 5×5** à plusieurs chemins, la **bonne** politique utilise
> la **sonde** (**2 nœuds**, coût 34) ; l'**aveugle** l'ignore complètement (**0 sonde**) et laisse
> l'A* résoudre par le symbolique/numérique (15 nœuds, coût 24). Le neuronal est **utile** ici,
> pas encore **nécessaire** — la limite est écrite.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-labyrinthe.json`](pensee-labyrinthe.json).

## 1. Le labyrinthe

Grille **5×5**, murs `{(0,1),(1,1),(2,1),(4,1),(1,3),(2,3),(3,3)}`, départ `(0,0)`, but `(4,4)`.
Trois opérateurs : `pas` (symbolique, 1), `saut` (numérique, 2), `sonde` (neuronal, 5, un appel).

| politique | nœuds | pas | saut | sonde | coût | appels | but |
|---|---:|---:|---:|---:|---:|---:|---|
| **manhattan** | **17** | 6 | 9 | **2** | **34** | **4** | **oui** |
| aveugle | 15 | 6 | 9 | **0** | 24 | 4 | oui |

**Ce que ça dit** :

- **La bonne politique utilise la sonde** (2 nœuds) ; l'**aveugle** ne l'utilise **pas** : ses
  propositions tombent sur les murs ou le piège, l'A* les écarte.
- **L'aveugle résout quand même** par `pas`/`saut` : le neuronal est **utile** (il aide la bonne
  politique), pas **nécessaire** dans ce labyrinthe ; le coût plus bas de l'aveugle (24) est dû
  au fait qu'il n'appelle pas la sonde.
- **Le labyrinthe est non linéaire** (plusieurs chemins, un piège), mais le symbolique/numérique
  suffit à le résoudre ; c'est la limite de ce banc.

## 2. Ce que ce banc ne dit pas

- **La politique est un double** (manhattan/aveugle), pas un modèle neuronal ; le vrai
  `drave-n0` n'a pas de poids, le `NeuronalLLM` reste refusé.
- **Le coût 5 de la sonde** est déclaré, pas mesuré.
- **L'aveugle réussit** : le contrôle négatif porte sur l'**usage** de la sonde, pas sur la
  capacité du moteur.
- **Le labyrinthe 5×5** est un jouet ; un vrai problème non linéaire demanderait un piège qui
  **bloque** l'A* sans la sonde.

## 3. Ce qui pourrait rendre cette fiche fausse

- une politique **chanceuse** qui utiliserait la sonde sans raison ;
- un labyrinthe **trop simple** (l'A* le résout par le pas) ;
- un coût **choisi après** la mesure ;
- une confusion **sonde / opérateur** : la sonde est le point d'appel, la politique est le modèle.

## 4. La suite

1. **Un labyrinthe où l'aveugle échoue** : un piège qui **bloque** le pas/saut (une porte qui ne
   s'ouvre que par la sonde), pour que la négative échoue vraiment.
2. **Politique DRVM/native** et coût mesuré, si les poids natifs arrivent.
3. **L** : 200 réels atteints ; continuer si utile.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `LABYRINTHE`, `REGISTRE_L`, `MURS`.
- [`autotest.py`](../tools/pensee/autotest.py) — T10, 13/13.
- [`pensee-labyrinthe.json`](pensee-labyrinthe.json) — les bilans.
