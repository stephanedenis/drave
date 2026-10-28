# A7.16 — cache KV int8 réellement stocké : 32/32 jetons identiques

> **Objet.** A7.12–A7.15 quantifiaient les projections **avant** l'attention. Ici on quantifie le
> **cache lui-même** : `CacheInt8` remplace `DynamicCache`, quantifie `keys` et `values` après chaque
> `update`, et le pas suivant lit le **cache quantifié**.

## Résultats

| mesure | valeur |
|---|---:|
| jetons générés | **32** |
| jetons identiques | **32 / 32** |
| accord | **1,00** |
| cache | `CacheInt8` (int8 par canal, stocks réels) |

## Lecture

- La génération reste **exactement identique** sur 32 jetons avec un **vrai cache quantifié** : ce
  n'est plus un hook sur les projections, c'est le cache qui est stocké en int8.
- C'est cohérent avec A7.15 (64/64 avec hooks) et A7.13 (ΔPPL 0,0).
- Le cache **stocké** est le scénario du transport : les K/V lus par l'attention suivante sont
  déquantifiés, pas les K/V fraîchement calculés.

## Verdict

**A7.16 est positif** : un cache KV int8 **réel** conserve **32/32** jetons greedy. Le cache
quantifié peut être stocké et relu sans changer la décision sur cet échantillon.

## Limites

- **32 jetons**, un prompt, greedy ; pas d'échantillonnage.
- Quantification **par canal**, pas par bloc ; le coût des échelles n'est pas compté.
- Le cache est quantifié **après** chaque update, mais le pas courant lit les K/V **non quantifiés**.
- Un seul modèle (0,5 B).

## Fichiers

- Code : [`tools/kv_cache_int8.py`](../tools/kv_cache_int8.py).
- Test : [`tools/cerveau/tests/test_kv_cache_int8.py`](../tools/cerveau/tests/test_kv_cache_int8.py).
- JSON : [`kv-cache-int8.json`](kv-cache-int8.json).
