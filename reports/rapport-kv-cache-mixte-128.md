# A7.23 — seuil f32 à 128 : moins bon qu'à 64

> **Objet.** A7.21 tenait **237 jetons** avec un seuil f32 de **64**. On teste un seuil de **128**
> (plus de jetons en f32, moins d'int8) sur **256 jetons**.

## Résultats (256 jetons)

| seuil f32 | premier divergent | accord |
|---|---:|---:|
| **64** (A7.21) | **237** | **92,58 %** |
| **128** | **215** | **83,98 %** |

## Lecture

- Contre-intuitivement, **plus de f32** donne un **moins bon** résultat : la divergence arrive au
  **215ᵉ** au lieu du **237ᵉ**, et l'accord baisse à **84,0 %**.
- Le seuil **64** est donc un meilleur compromis sur cet échantillon ; l'effet n'est pas monotone.
- Une explication possible : avec un seuil plus haut, l'int8 commence plus tard mais porte sur une
  séquence déjà plus longue, et l'erreur relative y est plus grande.

## Verdict

**A7.23 est négatif par rapport à A7.21** : le seuil **128** est **moins bon** que **64**. Le seuil
optimal n'est pas le plus grand ; il faudra le chercher (32, 48, 64, 96) sur plusieurs prompts.

## Limites

- **256 jetons**, un prompt, greedy ; une graine.
- Un seul seuil testé (128) contre 64.
- Re-quantification à chaque pas ; coût CPU non compté.
- Un seul modèle (0,5 B).

## Fichiers

- Code : [`tools/kv_cache_int8.py`](../tools/kv_cache_int8.py) (`CacheMixte128`).
- Fiche : [`rapport-kv-cache-mixte-256.md`](rapport-kv-cache-mixte-256.md).
- JSON : [`kv-cache-mixte-128.json`](kv-cache-mixte-128.json).
