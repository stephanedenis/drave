# A7.25 — balayage des seuils f32 : 64 reste le meilleur

> **Objet.** A7.21 (64), A7.23 (128) et A7.24 (32) montraient un effet non monotone. On complète
> avec **48** et **96** sur **256 jetons**.

## Résultats

| seuil f32 | premier divergent | accord |
|---|---:|---:|
| 32 | 41 | 16,41 % |
| **48** | **96** | **40,23 %** |
| **64** | **237** | **92,58 %** |
| **96** | **96** | **38,28 %** |
| 128 | 215 | 83,98 % |

## Lecture

- **64** est **nettement** le meilleur : **237** jetons avant divergence, **92,6 %** d'accord.
- **48** et **96** sont **mauvais** (divergence au **96ᵉ**, ~**40 %**) : le seuil n'est pas une
  fonction lisse de la quantité de f32.
- Le résultat suggère que **64** coïncide avec une **unité** du modèle (64 = head_dim) : protéger
  exactement une **longueur de tête** f32 stabilise la trajectoire.
- Les autres seuils tombent sur des frontières moins favorables.

## Verdict

**A7.25 confirme 64** : c'est le meilleur seuil testé. L'hypothèse **64 = head_dim** est
**plausible** mais non prouvée ; il faudrait tester sur un autre modèle ou une autre tête.

## Limites

- **256 jetons**, un prompt, greedy ; une graine.
- Seuils testés : **32, 48, 64, 96, 128**.
- Re-quantification à chaque pas ; coût CPU non compté.
- Un seul modèle (0,5 B, head_dim 64).

## Fichiers

- Code : [`tools/kv_cache_int8.py`](../tools/kv_cache_int8.py) (`CacheMixte48`, `CacheMixte96`).
- Fiches : [`rapport-kv-cache-mixte.md`](rapport-kv-cache-mixte.md), [`rapport-kv-cache-mixte-32.md`](rapport-kv-cache-mixte-32.md), [`rapport-kv-cache-mixte-128.md`](rapport-kv-cache-mixte-128.md).
- JSON : [`kv-cache-seuils.json`](kv-cache-seuils.json).
