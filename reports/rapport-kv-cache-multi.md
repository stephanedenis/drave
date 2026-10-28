# A7.26 — cache mixte sur 3 prompts : un décrochage à 75

> **Objet.** A7.21–A7.25 ne testaient qu'un prompt. Ici on mesure **3 prompts** (mesure, train,
> droits) avec le cache mixte seuil **64** sur **256 jetons**.

## Résultats

| prompt | premier divergent | accord |
|---|---:|---:|
| « La mesure est reine parce que » | **237** | **92,58 %** |
| « Un train part de Montréal… » | **75** | **71,31 %** |
| « Toute personne a droit à la liberté… » | **225** | **88,67 %** |
| **moyenne** | — | **84,19 %** |

## Lecture

- Le cache mixte **n'est pas robuste** : sur le prompt « train », il diverge dès le **75ᵉ** et
  l'accord tombe à **71,3 %**.
- Sur les deux autres, il tient **225–237** jetons avec **89–93 %**.
- La **moyenne** est **84,2 %** : ce n'est pas la fidélité bit-à-bit, c'est un compromis qui dépend
  du contenu.
- Le prompt « train » est **raisonnement** (calcul de rencontre) : la divergence précoce suggère que
  les tokens à forte incertitude sont plus sensibles au cache quantifié.

## Verdict

**A7.26 est un compromis, pas une victoire** : le cache mixte tient **84,2 %** en moyenne sur 3
prompts, avec un **décrochage à 75** sur le prompt de raisonnement. Il faut un **recalage f32** ou
une **quantification plus fine** pour les tokens incertains.

## Limites

- **3 prompts**, 256 jetons, greedy ; une graine.
- Seuil **64** seulement.
- Re-quantification à chaque pas ; coût CPU non compté.
- Un seul modèle (0,5 B).

## Fichiers

- Code : [`tools/kv_cache_int8.py`](../tools/kv_cache_int8.py) (`mesurer_multi`).
- Fiche : [`rapport-kv-cache-mixte.md`](rapport-kv-cache-mixte.md).
- JSON : [`kv-cache-multi.json`](kv-cache-multi.json).
