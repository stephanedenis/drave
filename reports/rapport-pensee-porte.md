# B13 — la porte neuronale : la bonne politique ouvre, l'aveugle échoue

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : **2026-11-01** · **Verdict** : ✅
> **14/14 portes** : sur un labyrinthe **où la seule sortie est une porte**, la **bonne** politique
> l'ouvre par la **sonde** et atteint le but en **28 nœuds** (coût 58, 5 sondes) ; l'**aveugle** ne
> l'ouvre pas, consomme **200 nœuds** (coût 483, 61 sondes) et **n'atteint pas** le but. Le
> neuronal est ici **nécessaire**, pas seulement utile.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-porte.json`](pensee-porte.json).

## 1. Le labyrinthe à porte

Grille **5×5**, murs `{(0,1),(1,1),(2,1),(4,1),(4,2),(1,2),(2,2),(1,3),(3,4)}`, porte
`(3,3)`, départ `(0,0)`, but `(4,4)`. La porte ne s'ouvre que si la **politique** propose la
direction de la porte (`bas` depuis `(3,2)`) ; les `pas`/`saut` sont bloqués par la porte fermée.

| politique | nœuds | pas | saut | sonde | coût | appels | but |
|---|---:|---:|---:|---:|---:|---:|---|
| **manhattan** | **28** | 13 | 10 | **5** | **58** | 7 | **oui** |
| aveugle | 200 | 100 | 39 | 61 | 483 | 66 | **non** |

**Ce que ça dit** :

- **Le neuronal est nécessaire** : la porte ne s'ouvre que par la **bonne** politique ; l'aveugle
  propose la mauvaise direction, la porte reste fermée, le but est inatteignable.
- **L'aveugle épuise son budget** (200 nœuds) sans atteindre le but ; le coût 483 est le prix de
  ses appels inutiles à la sonde (61).
- **La bonne politique paie** 58 pour 28 nœuds, dont 5 sondes : le neuronal est **cher** et
  **décisif** ici.
- **La porte est le seul chemin** : les murs `(4,2)` et `(3,4)` bouchent les contournements.

## 2. Ce que ce banc ne dit pas

- **La politique est un double** (`manhattan`/`aveugle`), pas un modèle neuronal ; le vrai
  `drave-n0` n'a pas de poids, le `NeuronalLLM` reste refusé.
- **Le coût 5 de la sonde** est déclaré, pas mesuré.
- **L'aveugle échoue par construction** (il ne vise jamais la porte) : ce n'est pas une preuve
  qu'un mauvais modèle échoue toujours, seulement que **sans la bonne politique** la porte reste
  fermée.
- **Le labyrinthe 5×5** est un jouet ; un vrai problème demanderait une porte **apprise**.

## 3. Ce qui pourrait rendre cette fiche fausse

- une politique **chanceuse** qui ouvrirait la porte sans la viser ;
- un chemin **caché** qui contournerait la porte (les murs sont vérifiés) ;
- un budget **trop grand** qui laisserait l'aveugle trouver la porte par hasard (200 nœuds, non) ;
- une confusion **sonde / porte** : la sonde est l'opérateur, la politique est le modèle.

## 4. La suite

1. **Politique DRVM/native** : brancher un vrai modèle quand ses poids seront là ; la porte
   mesurera la **qualité** de la politique, pas seulement sa nécessité.
2. **Coût mesuré** : remplacer le coût 5 par la latence réelle.
3. **L** : 200 réels atteints ; le gold peut encore grandir.
4. **B13** : une porte **apprise** (le modèle doit découvrir la direction) plutôt que déclarée.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `LABYRINTHE_PORTE`, `REGISTRE_P`, `MURS_P`.
- [`autotest.py`](../tools/pensee/autotest.py) — T11, 14/14.
- [`pensee-porte.json`](pensee-porte.json) — les bilans.
