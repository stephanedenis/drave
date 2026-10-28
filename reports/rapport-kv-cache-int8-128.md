# A7.18 — cache KV int8 sur 128 jetons : la divergence commence à 77

> **Objet.** A7.17 tenait **64/64** jetons avec `CacheInt8`. Ici on pousse à **128 jetons** pour
> trouver le point où le cache quantifié décroche.

## Résultats

| mesure | valeur |
|---|---:|
| jetons générés | **128** |
| jetons identiques | **non** |
| accord global | **60,94 %** |
| **premier jeton divergent** | **77** |
| 64 premiers jetons | **identiques** (A7.17) |

## Lecture

- Le cache int8 par canal tient **64 jetons** (A7.17), puis **diverge au 77ᵉ**.
- Une fois la divergence engagée, l'accord tombe à **60,9 %** : la génération suit une autre
  trajectoire.
- Ce n'est pas une erreur de mesure : le cache **stocké** est bien celui que lit l'attention
  suivante, et la quantification est **lossy**.
- Le seuil **77** est cohérent avec une accumulation d'erreurs : plus la séquence est longue, plus
  les K/V quantifiés s'écartent.

## Verdict

**A7.18 est négatif pour 128 jetons** : le cache KV int8 par canal **diverge à 77** et l'accord
tombe à **60,9 %**. Il faut une quantification **par bloc** ou un **cache mixte** (f32 pour les
premiers jetons) avant de l'utiliser en génération longue.

## Limites

- **128 jetons**, un prompt, greedy ; une seule graine.
- Quantification **par canal**, pas par bloc (le point faible probable).
- Le pas courant lit les K/V **non quantifiés** ; seule la mémoire l'est.
- Un seul modèle (0,5 B).

## Fichiers

- Code : [`tools/kv_cache_int8.py`](../tools/kv_cache_int8.py).
- Fiche : [`rapport-kv-cache-int8-64.md`](rapport-kv-cache-int8-64.md).
- JSON : [`kv-cache-int8-128.json`](kv-cache-int8-128.json).
