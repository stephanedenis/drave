# B13 — la fusion par sous-type : le double sens gagne 0,0208

> **Ligne de roadmap** : **B13** (moteur de pensée, règles 6 et 11) · **Date** : 2026-11-04 ·
> **Verdict** : ✅ **153/153 portes** : la fusion choisit maintenant **par (niveau, type)** :
> le neuronal prend l'**acte** et le **double sens**, l'heuristique garde la **négation** et la
> **modalité**. Sur le gold 432, le `_niveau` passe de **0,9676 à 0,9884** en double sens
> (+0,0208), l'acte reste à 0,9954, la négation (0,9676) et la modalité (0,9861) restent à
> l'heuristique.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py),
> [`pensee-quatre-modes-432-soustype.json`](pensee-quatre-modes-432-soustype.json),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-fusion-soustype.json`](pensee-fusion-soustype.json).

## 1. Par niveau contre par sous-type

| mesure | niveau (T149) | **sous-type** | écart |
|---|---:|---:|---:|
| POS | 0,9389 | 0,9389 | 0 |
| acte | 0,9954 | 0,9954 | 0 |
| négation | 0,9676 | 0,9676 | 0 |
| modalité | 0,9861 | 0,9861 | 0 |
| **double sens** | 0,9676 | **0,9884** | **+0,0208** |

**Ce que ça dit** :

- **Le sous-type paie** : le neuronal est meilleur en double sens (0,9884 contre 0,9676) et la
  fusion par sous-type le lui prend — sans toucher à l'acte (égal) ni à la négation/modalité
  (l'heuristique reste devant).
- **La granularité était la limite** : le niveau `pragmatique` entier cachait deux sous-types
  qui divergent ; c'est la leçon de la fiche T149.
- **Aucune perte** : le POS, les syntagmes, la tête, l'acte, la négation, la modalité sont
  identiques — le gain est net.
- **La négative est explicite** : 0,9884 < 1,0 ; un cas de double sens reste faux.

## 2. Ce que ce banc ne dit pas

- **Une passe** (température 0) : la variance du sous-type n'est pas mesurée.
- **Le gold 432** : 432 phrases.
- **Le coût** : 1 287 appels, 314 369 tokens, 1 236 s — identique (les annotations sont les mêmes,
  seule la fusion change).
- **Les autres sous-types** (la phrase `négation` est aussi un type de `phrase`) : le mécanisme
  est général, seules quatre paires sont dans `PRIORITE_TYPE`.

## 3. Ce qui pourrait rendre cette fiche fausse

- **une passe** : 0,0208 est un petit écart, la variance peut le réduire ;
- **le gold** : 432 phrases ;
- **la fusion par sous-type** ne s'applique qu'aux paires listées ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La variance du sous-type** : une passe à 0,3 (le double sens est-il stable ?).
2. **Les autres paires** : mesurer d'autres sous-types (le `discours` par exemple).
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `PRIORITE_TYPE`, `_fusion`.
- [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py) — les modes.
- [`pensee-quatre-modes-432-soustype.json`](pensee-quatre-modes-432-soustype.json) — la passe.
- [`autotest.py`](../tools/pensee/autotest.py) — T150, 153/153.
- [`pensee-fusion-soustype.json`](pensee-fusion-soustype.json) — les écarts.
