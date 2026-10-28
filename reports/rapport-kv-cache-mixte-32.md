# A7.24 — seuil f32 à 32 : le plus mauvais des trois

> **Objet.** A7.21 (seuil 64) et A7.23 (seuil 128) montraient un effet non monotone. On teste le
> seuil **32** sur **256 jetons**.

## Résultats

| seuil f32 | premier divergent | accord |
|---|---:|---:|
| **32** | **41** | **16,41 %** |
| **64** (A7.21) | **237** | **92,58 %** |
| **128** (A7.23) | **215** | **83,98 %** |

## Lecture

- Le seuil **32** est **le plus mauvais** : divergence au **41ᵉ**, accord **16,4 %**.
- Le **64** est **le meilleur** des trois ; le **128** est intermédiaire.
- L'optimum n'est donc ni le plus petit ni le plus grand : **64** protège assez les premiers jetons
  sans retarder inutilement l'int8.

## Verdict

**A7.24 est négatif** : le seuil **32** est pire que **64** et **128**. Le seuil **64** reste le
meilleur compromis sur cet échantillon.

## Limites

- **256 jetons**, un prompt, greedy ; une graine.
- Seuls **32, 64, 128** testés ; 48 ou 96 pourraient faire mieux.
- Re-quantification à chaque pas ; coût CPU non compté.
- Un seul modèle (0,5 B).

## Fichiers

- Code : [`tools/kv_cache_int8.py`](../tools/kv_cache_int8.py) (`CacheMixte32`).
- Fiches : [`rapport-kv-cache-mixte.md`](rapport-kv-cache-mixte.md), [`rapport-kv-cache-mixte-128.md`](rapport-kv-cache-mixte-128.md).
- JSON : [`kv-cache-mixte-32.json`](kv-cache-mixte-32.json).
