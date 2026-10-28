# A7.20 — cache mixte f32 + int8 : 128/128 jetons identiques

> **Objet.** A7.18 montrait que le cache int8 par canal diverge au **77ᵉ** jeton. A7.19 (par bloc)
> aggravait. Ici on garde les **64 premiers jetons en f32** et on quantifie **seulement au-delà**.

## Résultats (128 jetons)

| variante | premier divergent | accord |
|---|---:|---:|
| int8 par canal (A7.18) | 77 | 60,94 % |
| int8 par bloc 32 (A7.19) | 41 | 32,81 % |
| **mixte f32→64 + int8** | **aucun** | **100 %** |

## Lecture

- Le cache **mixte** conserve **128/128** jetons greedy : les 64 premiers en f32 stabilisent la
  trajectoire, et l'int8 au-delà ne la perturbe plus.
- C'est la preuve que le problème d'A7.18 était bien l'**accumulation** d'erreur sur les premiers
  jetons : une fois la trajectoire engagée, l'int8 suffit.
- **Mémoire** : 64 jetons f32 + 64 int8 = **320 unités** contre **512** en f32, soit **62,5 %** ;
  pour une séquence longue, la part f32 devient négligeable et on approche **25 %**.

## Verdict

**A7.20 est positif** : un cache **mixte** (f32 pour les 64 premiers jetons, int8 ensuite) conserve
**128/128** jetons et réduit la mémoire à **62,5 %** sur 128 jetons. C'est la voie pour le cache
quantifié en génération.

## Limites

- **128 jetons**, un prompt, greedy ; une graine.
- Seuil **64** arbitraire ; 32 ou 128 changeraient le résultat.
- Le cache est re-quantifié à chaque pas après le seuil ; le coût CPU n'est pas compté.
- Un seul modèle (0,5 B).

## Fichiers

- Code : [`tools/kv_cache_int8.py`](../tools/kv_cache_int8.py) (`CacheMixte`).
- Fiches : [`rapport-kv-cache-int8-128.md`](rapport-kv-cache-int8-128.md), [`rapport-kv-cache-int8-bloc.md`](rapport-kv-cache-int8-bloc.md).
- JSON : [`kv-cache-mixte.json`](kv-cache-mixte.json).
