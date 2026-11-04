# B13 — les trois tirages à 0,3 : 0,9838 exactement, le cache masque la variance

> **Ligne de roadmap** : **B13** (moteur de pensée, règles 6 et 11) · **Date** : 2026-11-04 ·
> **Verdict** : ✅ **155/155 portes** : trois tirages à **température 0,3** donnent **0,9838,
> 0,9838, 0,9838** — variance **nulle**. Ce n'est pas une preuve de stabilité : c'est le **cache**
> de l'API (mêmes invites, mêmes réponses). La variance réelle du modèle n'est pas mesurée par
> ce banc ; elle est **masquée**.
>
> **Dispositif** : [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py),
> [`pensee-quatre-modes-432-soustype-t03b.json`](pensee-quatre-modes-432-soustype-t03b.json),
> [`…-t03c.json`](pensee-quatre-modes-432-soustype-t03c.json),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-tirages.json`](pensee-tirages.json).

## 1. Les trois tirages

| tirage | double sens | POS | tête |
|---|---:|---:|---:|
| 1 | 0,9838 | 0,9385 | 0,8723 |
| 2 | **0,9838** | 0,9385 | 0,8723 |
| 3 | **0,9838** | 0,9385 | 0,8723 |
| **moyenne** | **0,9838** | 0,9385 | 0,8723 |
| écart-type | **0,0000** | 0,0000 | 0,0000 |

**Ce que ça dit** :

- **La variance est nulle** — et c'est **suspect** : à 0,3, un modèle non déterministe devrait
  varier. L'explication est le **cache** de l'API (mêmes invites, mêmes réponses).
- **Le banc ne mesure pas la variance du modèle** : il mesure la **stabilité du cache**. C'est
  une limite de méthode, pas un résultat de stabilité.
- **Le gain du sous-type reste** : 0,9838 > 0,9676 (l'heuristique) sur les trois tirages.
- **La négative est explicite** : écart-type 0 n'est pas une qualité, c'est un artefact.

## 2. Ce que ce banc ne dit pas

- **La variance réelle** : il faudrait désactiver le cache (ou changer les invites) pour la voir.
- **Le gold 432** : 432 phrases.
- **Le coût** : 1 287 appels × 3, ~314 k tokens, ~1 236 s par passe.
- **Le cache** : il est légitime pour la reproductibilité, trompeur pour la variance.

## 3. Ce qui pourrait rendre cette fiche fausse

- **le cache** : c'est l'hypothèse la plus simple pour expliquer l'identité parfaite ;
- **trois tirages** : un seul échantillon de la distribution ;
- **le gold** : 432 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Sans cache** : une passe avec `cache=False` (si l'API le permet) pour la variance réelle.
2. **Le sous-type** : le gain 0,0162–0,0208 est robuste sur les tirages (cache compris).
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`qualifier_quatre_modes.py`](../tools/tests/linguistique/qualifier_quatre_modes.py) — les passes.
- [`pensee-quatre-modes-432-soustype-t03b.json`](pensee-quatre-modes-432-soustype-t03b.json) — tirage 2.
- [`pensee-quatre-modes-432-soustype-t03c.json`](pensee-quatre-modes-432-soustype-t03c.json) — tirage 3.
- [`autotest.py`](../tools/pensee/autotest.py) — T152, 155/155.
- [`pensee-tirages.json`](pensee-tirages.json) — les trois.
