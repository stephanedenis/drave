# A7.19 — quantification par bloc : pire que par canal

> **Objet.** A7.18 montrait que le cache int8 **par canal** diverge au **77ᵉ** jeton sur 128. On
> teste une quantification **par bloc de 32 jetons** pour rapprocher les échelles des valeurs.

## Résultats (128 jetons)

| variante | premier divergent | accord |
|---|---:|---:|
| int8 par canal (A7.18) | **77** | **60,94 %** |
| **int8 par bloc 32** | **41** | **32,81 %** |

## Lecture

- La quantification par bloc est **pire** : la divergence arrive au **41ᵉ** jeton et l'accord tombe
  à **32,8 %**.
- Ce n'est pas intuitif : des échelles plus locales devraient réduire l'erreur. Ici, les blocs de
  32 jetons créent des **discontinuités** entre blocs voisins, et l'attention lit un cache dont les
  échelles changent brutalement.
- Le **cache par canal** reste le meilleur des deux, mais il diverge quand même après 64.

## Verdict

**A7.19 est négatif** : la quantification par bloc **aggrave** la divergence. Le problème n'est pas
la granularité de l'échelle, c'est l'**accumulation d'erreur** dans le cache relu pas à pas.

## Limites

- **128 jetons**, un prompt, greedy ; une graine.
- Bloc **32** seulement ; 16 ou 64 pourraient se comporter autrement.
- Le cache est quantifié **après** chaque update ; le pas courant lit les K/V non quantifiés.
- Un seul modèle (0,5 B).

## Fichiers

- Code : [`tools/kv_cache_int8.py`](../tools/kv_cache_int8.py) (`CacheInt8Bloc`).
- Fiche : [`rapport-kv-cache-int8-128.md`](rapport-kv-cache-int8-128.md).
- JSON : [`kv-cache-int8-bloc.json`](kv-cache-int8-bloc.json).
