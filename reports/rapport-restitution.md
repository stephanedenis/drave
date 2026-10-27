# B18 — restitution canonique : 528/528, mais pas un décodeur

> **Objet.** Le **miroir** de M1 : rendre un code typé en surface canonique et le relire. C'est le
> codec, pas un décodeur neuronal ; B10 reste négatif.

## Mesure

| mesure | valeur |
|---|---:|
| items | **528** |
| surfaces rendues | **528 / 528 = 100 %** |
| relues sans perte | **528 / 528 = 100 %** |
| échecs | **0** |

Le rendu utilise la **position RSN** du corpus réel (le SAN exige le contexte) ; la relecture
reproduit le code exact. C'est une **involution du codec**, pas une génération de langage.

## Ce que ce n'est pas

- Ce n'est **pas** le décodeur neuronal B10 (chrF 14,0/5,4 contre plancher 38,8).
- Ce n'est **pas** une paraphrase ni une traduction : c'est la **forme canonique** du code.
- La sortie est **déterministe** et **exacte** ; elle ne prouve pas la fidélité sémantique.

## Verdict

**M1 est un codec bidirectionnel exact** : 528/528 à l’aller et au retour. C'est le seul étage
réellement solide du prototype. La génération libre reste un **négatif** (B10).

## Fichiers

- Code : [`tools/cerveau/restitution.py`](../tools/cerveau/restitution.py).
- Test : [`tools/cerveau/tests/test_restitution.py`](../tools/cerveau/tests/test_restitution.py).
- JSON : [`restitution.json`](restitution.json).
