# A7.21 — cache mixte sur 256 jetons : divergence au 237ᵉ

> **Objet.** A7.20 tenait **128/128** avec un cache mixte (f32 sur 64 jetons, int8 ensuite). Ici on
> pousse à **256 jetons** pour trouver la limite.

## Résultats

| mesure | valeur |
|---|---:|
| jetons générés | **256** |
| identiques | **non** |
| accord | **92,58 %** |
| **premier divergent** | **237** |
| 128 premiers | **identiques** (A7.20) |

## Lecture

- Le cache mixte tient **128 jetons** (A7.20) puis **diverge au 237ᵉ** sur 256.
- L'accord reste **92,6 %** : la divergence est **tardive** et **partielle**, pas une dérive complète.
- C'est **beaucoup mieux** que l'int8 par canal (divergence au 77ᵉ) et que le bloc (41ᵉ).
- Le seuil **64** f32 retarde la divergence mais ne l'empêche pas : l'accumulation finit par gagner.

## Verdict

**A7.21 est un compromis** : le cache mixte tient **237 jetons** et **92,6 %** d'accord sur 256. Ce
n'est pas la fidélité bit-à-bit, mais c'est utilisable pour des générations moyennes ; au-delà, il
faut un **recalage f32 périodique** ou une quantification plus fine.

## Limites

- **256 jetons**, un prompt, greedy ; une graine.
- Seuil **64** arbitraire ; un seuil plus haut retarde la divergence.
- Re-quantification à chaque pas ; coût CPU non compté.
- Un seul modèle (0,5 B).

## Fichiers

- Code : [`tools/kv_cache_int8.py`](../tools/kv_cache_int8.py) (`CacheMixte`).
- Fiche : [`rapport-kv-cache-mixte.md`](rapport-kv-cache-mixte.md).
- JSON : [`kv-cache-mixte-256.json`](kv-cache-mixte-256.json).
