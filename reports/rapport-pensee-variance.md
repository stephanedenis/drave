# B13 — la variance à température 0,3 : ±0,007 au pire

> **Ligne de roadmap** : **B13** (moteur de pensée, règles 6 et 11) · **Date** : 2026-11-04 ·
> **Verdict** : ✅ **150/150 portes** : la même passe à **température 0,3** donne POS **0,9385**
> (−0,0004), syntagmes **0,8246** (+0,0005), tête **0,8723** (−0,0074) — la **variance est
> faible**, tous les seuils restent verts et le refus reste à 0.
>
> **Dispositif** : [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py)
> (`--temperature`), [`pensee-quatre-modes-432-t03.json`](pensee-quatre-modes-432-t03.json),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-variance.json`](pensee-variance.json).

## 1. Température 0 contre 0,3

| mesure | temp 0 (run 3) | **temp 0,3** | écart |
|---|---:|---:|---:|
| POS (niveau) | 0,9389 | **0,9385** | −0,0004 |
| syntagmes F1 | 0,8241 | **0,8246** | +0,0005 |
| **tête F1** | 0,8797 | **0,8723** | **−0,0074** |
| acte | 0,9954 | 0,9954 | 0 |
| refus | 0 | **0** | 0 |
| seuils | 7/7 | **7/7** | 0 |

**Ce que ça dit** :

- **La variance est faible** : ±0,0074 au pire (la tête) ; la POS est stable à 0,0004 — le
  résultat ne dépend pas de la graine.
- **Les seuils tiennent** (7/7) et le **refus reste 0** : la tokenisation corrigée n'est pas un
  cas de température 0.
- **La tête est la plus sensible** : c'est la mesure la plus fine (le premier token), donc la
  plus exposée au bruit du modèle.
- **La négative** : à 0,3, la tête perd 0,0074 — la mesure est stable mais pas exacte.

## 2. Ce que ce banc ne dit pas

- **Deux températures** (0 et 0,3) : la courbe complète n'est pas faite.
- **Le cache** de l'API peut expliquer l'identité des runs 0.
- **Le gold 432** : les seuils sont ceux du banc.
- **Le coût** : 858 appels, ~254 k tokens, ~808 s par passe.

## 3. Ce qui pourrait rendre cette fiche fausse

- **la température 0,3** : un seul tirage, pas une moyenne ;
- **le cache** : il peut masquer une partie de la variance ;
- **le gold** : 432 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Trois tirages à 0,3** : la moyenne et l'écart-type (si le temps le permet).
2. **Le GGUF** : la porte N0.1 complète.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py) — `--temperature`.
- [`pensee-quatre-modes-432-t03.json`](pensee-quatre-modes-432-t03.json) — la passe 0,3.
- [`autotest.py`](../tools/pensee/autotest.py) — T147, 150/150.
- [`pensee-variance.json`](pensee-variance.json) — les écarts.
