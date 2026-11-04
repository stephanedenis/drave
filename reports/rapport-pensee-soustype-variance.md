# B13 — la variance du sous-type : 0,9838 à 0,3, le gain tient

> **Ligne de roadmap** : **B13** (moteur de pensée, règles 6 et 11) · **Date** : 2026-11-04 ·
> **Verdict** : ✅ **154/154 portes** : la passe à **température 0,3** avec la fusion par
> sous-type donne **double sens 0,9838** (−0,0046 contre 0,9884 à 0) — **toujours au-dessus** de
> l'heuristique (0,9676). Le gain de la fusion par sous-type **tient** sur deux températures.
>
> **Dispositif** : [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py),
> [`pensee-quatre-modes-432-soustype-t03.json`](pensee-quatre-modes-432-soustype-t03.json),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-soustype-variance.json`](pensee-soustype-variance.json).

## 1. Température 0 contre 0,3 (sous-type)

| mesure | temp 0 | **temp 0,3** | écart |
|---|---:|---:|---:|
| POS | 0,9389 | 0,9385 | −0,0004 |
| syntagmes | 0,8241 | 0,8246 | +0,0005 |
| tête | 0,8797 | 0,8723 | −0,0074 |
| acte | 0,9954 | 0,9954 | 0 |
| négation | 0,9676 | 0,9676 | 0 |
| modalité | 0,9861 | 0,9861 | 0 |
| **double sens** | **0,9884** | **0,9838** | −0,0046 |

**Ce que ça dit** :

- **Le gain du sous-type tient** : 0,9838 contre 0,9676 (l'heuristique) — +0,0162 à 0,3, +0,0208
  à 0. Le choix par sous-type est robuste.
- **La variance est faible** : ±0,0074 au pire (tête), comme les passes par niveau.
- **Les autres sous-types sont stables** : acte, négation, modalité ne bougent pas.
- **La négative est explicite** : 0,9838 < 1,0 ; deux cas de double sens restent faux.

## 2. Ce que ce banc ne dit pas

- **Deux températures** : la courbe complète n'est pas faite.
- **Le gold 432** : 432 phrases.
- **Le coût** : 1 287 appels, ~314 k tokens, ~1 236 s par passe.
- **Le cache** peut expliquer une partie de la stabilité des runs à 0.

## 3. Ce qui pourrait rendre cette fiche fausse

- **deux tirages** : la moyenne du double sens n'est pas établie ;
- **le gold** : 432 phrases ;
- **la fusion par sous-type** ne couvre que quatre paires ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Trois tirages** : la moyenne du double sens (si le temps le permet).
2. **Les autres paires** : mesurer d'autres sous-types.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py) — `--temperature`.
- [`pensee-quatre-modes-432-soustype-t03.json`](pensee-quatre-modes-432-soustype-t03.json) — la passe.
- [`autotest.py`](../tools/pensee/autotest.py) — T151, 154/154.
- [`pensee-soustype-variance.json`](pensee-soustype-variance.json) — les écarts.
