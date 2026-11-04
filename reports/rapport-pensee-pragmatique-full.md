# B13 — la pragmatique sur le gold 432 : acte 0,9954, la fusion garde l'heuristique

> **Ligne de roadmap** : **B13** (moteur de pensée, règles 6 et 11) · **Date** : 2026-11-04 ·
> **Verdict** : ✅ **152/152 portes** : avec le **tagger pragmatique** branché, le neuronal rend
> l'acte à **0,9954** (contre 0,0 sans lui) sur les 432 phrases. Mais la **négation** (0,9630) et
> la **modalité** (0,9722) restent **sous l'heuristique** (0,9676 / 0,9861) : la fusion par
> niveau garde donc le pragma de l'heuristique — et c'est le bon choix mesuré.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py),
> [`pensee-quatre-modes-432-pragma.json`](pensee-quatre-modes-432-pragma.json),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-pragmatique-full.json`](pensee-pragmatique-full.json).

## 1. Les six modes (432 phrases, avec pragma)

| mode | POS | syntagmes | tête | acte | négation | modalité | double sens |
|---|---:|---:|---:|---:|---:|---:|---:|
| heuristique | 0,7444 | 0,2524 | 0,4516 | 0,9954 | **0,9676** | **0,9861** | 0,9676 |
| neuronal (3 taggers) | 0,9389 | 0,8241 | 0,8797 | 0,9954 | 0,9630 | 0,9722 | 0,9884 |
| **parallele_niveau** | **0,9389** | **0,8241** | **0,8797** | 0,9954 | 0,9676 | 0,9861 | 0,9676 |
| **cascade_niveau** | **0,9389** | **0,8241** | **0,8797** | 0,9954 | 0,9676 | 0,9861 | 0,9676 |

**Ce que ça dit** :

- **Le composite rend l'acte** (0,9954) : le tagger dédié comble la sortie manquante ; la fusion
  par niveau garde la meilleure source par niveau.
- **La négation et la modalité restent à l'heuristique** : le neuronal fait 0,9630 / 0,9722,
  l'heuristique 0,9676 / 0,9861 — la règle par niveau tranche **par la mesure**, pas par doctrine.
- **Le double sens profite au neuronal** (0,9884 contre 0,9676) — mais la fusion par niveau le
  laisse à l'heuristique (le niveau `pragmatique` est entier) ; un **sous-niveau** serait la
  prochaine finesse.
- **Le refus reste 0**, les 7/7 seuils passent, le coût est **1 287 appels** (3 taggers × 429).

## 2. Ce que ce banc ne dit pas

- **Le pragma neuronal** est mesuré globalement, pas par sous-type (acte vs négation) dans la
  fusion : la granularité est le niveau.
- **Une passe** (température 0) ; la variance du pragma n'est pas mesurée.
- **Le gold 432** : 432 phrases.
- **Le coût** : 1 287 appels, 314 369 tokens, 1 236 s de latence.

## 3. Ce qui pourrait rendre cette fiche fausse

- **la granularité** : le niveau `pragmatique` est pris en bloc, alors que les sous-types
  diverguent (acte vs négation) ;
- **une passe** : la variance du pragma n'est pas mesurée ;
- **le gold** : 432 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La fusion par sous-type** : acte au neuronal, négation/modalité à l'heuristique — la
   prochaine finesse.
2. **La variance du pragma** : une passe à 0,3.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `NeuronalLLMCompose(pragma=...)`.
- [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py) — le pragma.
- [`pensee-quatre-modes-432-pragma.json`](pensee-quatre-modes-432-pragma.json) — la passe.
- [`autotest.py`](../tools/pensee/autotest.py) — T149, 152/152.
- [`pensee-pragmatique-full.json`](pensee-pragmatique-full.json) — les modes.
