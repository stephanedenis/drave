# A7.17 — cache KV int8 stocké sur 64 jetons : 64/64 identiques

> **Objet.** A7.16 validait le cache int8 stocké sur 32 jetons. Ici on génère **64 jetons** avec
> `CacheInt8` et on compare au modèle intact.

## Résultats

| mesure | valeur |
|---|---:|
| jetons générés | **64** |
| jetons identiques | **64 / 64** |
| accord | **1,00** |
| cache | `CacheInt8` (int8 par canal) |

## Lecture

- La génération reste **exactement identique** sur **64 jetons** avec un **vrai cache quantifié**.
- C'est cohérent avec A7.15 (64/64 avec hooks) et A7.16 (32/32 avec cache).
- Le cache **stocké** est bien celui que lit l'attention suivante : ce n'est pas seulement une
  quantification des projections courantes.

## Verdict

**A7.17 est positif** : le cache KV int8 stocké tient **64/64** jetons greedy. Le cache quantifié
est stable sur une génération courte.

## Limites

- **64 jetons**, un prompt, greedy ; pas d'échantillonnage.
- Quantification **par canal** ; le coût des échelles n'est pas compté.
- Le pas courant lit les K/V **non quantifiés** ; seuls les pas suivants lisent le cache quantifié.
- Un seul modèle (0,5 B).

## Fichiers

- Code : [`tools/kv_cache_int8.py`](../tools/kv_cache_int8.py).
- Fiche : [`rapport-kv-cache-int8.md`](rapport-kv-cache-int8.md).
- JSON : [`kv-cache-int8-64.json`](kv-cache-int8-64.json).
