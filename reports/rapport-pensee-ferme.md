# B13 — la porte qui se referme : le moteur repasse

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **20/20 portes** : la porte `(3,3)` se **referme** dès qu'on la franchit. La bonne politique
> l'ouvre, passe, et l'A* atteint le but en **27 nœuds** (sonde 5, coût 57) : le moteur doit
> **repérer** que la porte se referme et ne pas compter sur un retour.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-ferme.json`](pensee-ferme.json).

## 1. La porte qui se referme

Même labyrinthe que T11, mais `_deplacer_pf` referme la porte dès qu'on la franchit : l'état
`(x, y, open)` passe à `open = False` sur la case `(3,3)`. La politique doit l'ouvrir **avant**
de passer ; une fois passée, elle ne peut plus revenir.

| politique | nœuds | pas | saut | sonde | coût | but |
|---|---:|---:|---:|---:|---:|---|
| **manhattan** | **27** | 12 | 10 | **5** | **57** | **oui** |

**Ce que ça dit** :

- **Le moteur gère la fermeture** : l'A* explore la porte, la franchit, la porte se referme,
  et le but est atteint sans retour.
- **La sonde reste nécessaire** (5 appels) : sans elle, la porte reste fermée.
- **Le coût baisse** (57 contre 58 sur T11) : le chemin est un peu plus court, la porte se
  refermant derrière.
- **Le vrai piège serait une porte qui se referme avant le passage** : ce banc la referme
  **après**, c'est la prochaine étape.

## 2. Ce que ce banc ne dit pas

- **Politique manhattan** (règle), pas la Q-table : la Q-table sur la porte qui se referme
  n'est pas mesurée.
- **Pas de retour** : la porte se referme derrière ; le moteur ne peut pas revenir, ce qui
  simplifie l'exploration.
- **Le coût 5** de la sonde est déclaré.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **politique chanceuse** qui ouvrirait la porte sans la viser ;
- un **chemin** qui contournerait la porte (les murs l'en empêchent) ;
- une **confusion** porte / état : l'ouverture est un état, pas un opérateur ;
- un **budget** trop grand.

## 4. La suite

1. **Porte qui se referme avant le passage** : le moteur doit rouvrir et repasser.
2. **Q-table sur la porte qui se referme** : la politique apprend le nouveau modèle.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `LABYRINTHE_PORTE_FERME`, `REGISTRE_PF`,
  `pas_pf`/`saut_pf`/`sonde_pf`.
- [`autotest.py`](../tools/pensee/autotest.py) — T17, 20/20.
- [`pensee-ferme.json`](pensee-ferme.json) — le bilan.
