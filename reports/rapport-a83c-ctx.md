# A8.3c.1 — le signe du mélange ne dépend pas de la taille du contexte

> **Ligne de roadmap** : A8.3b/c · **Date** : 2026-10-29 · **Verdict** : ✅ **le cache n’est pas
> la cause** — à ctx 64, 256 et 512, les PPL sont **identiques** : f32 lot 0/1 = **61,9920**,
> lot 2/4 = **60,8135** ; 1 % lot 0/1 = **58,3200**, lot 2/4 = **62,7357**. Le basculement est
> le **chemin lot** (lot 1 contre lot ≥ 2), pas la capacité du cache.
>
> **Dispositif** : `--ppl-reparti`, Qwen2.5-0.5B Q8_0, 12 couches locales, 24 jetons, ctx variable ;
> 24 exécutions ; données [`a83c-ctx.json`](a83c-ctx.json).

## Ce qui est mesuré

| régime | ctx | lot 0 | lot 1 | lot 2 | lot 4 |
|---|---:|---:|---:|---:|---:|
| f32 | 64 | 61,9920 | 61,9920 | 60,8135 | 60,8135 |
| f32 | 256 | 61,9920 | 61,9920 | 60,8135 | 60,8135 |
| f32 | 512 | 61,9920 | 61,9920 | 60,8135 | 60,8135 |
| 1 % | 64 | 58,3200 | 58,3200 | 62,7357 | 62,7357 |
| 1 % | 256 | 58,3200 | 58,3200 | 62,7357 | 62,7357 |
| 1 % | 512 | 58,3200 | 58,3200 | 62,7357 | 62,7357 |

Aucune ligne ne bouge avec ctx : **24 exécutions, six combinaisons, deux régimes**.

## Le contrôle négatif

- **ctx seul varie** : les chiffres restent identiques — la capacité du cache n’est pas la cause.
- **Lot 1 contre ≥ 2** : le basculement est reproductible aux trois contextes.
- **Régime f32 contre 1 %** : le signe change avec la règle KV, pas avec ctx.

## Ce qui pourrait le rendre faux

- **Un seul modèle**, 24 jetons, 12 couches locales.
- **Le chemin lot n’est pas instrumenté** : on sait que ce n’est pas ctx, pas ce qu’il fait.
- **La PPL n’est pas la qualité** : un chiffre qui baisse n’est pas une amélioration.
- **D’autres tailles de cache** (batch, KV paginé) ne sont pas testées.

## Ce que ça décide

A8.3 reste **opt-in**. Le prochain pas est le **code du chemin lot** (lot 1 contre ≥ 2), pas la
capacité du cache KV. A8.3b/c est rétréci à un **chemin d’exécution**, pas à une taille.

## Fichiers

- `reports/a83c-ctx.json` — les 24 mesures.
- `reports/rapport-a83c-ctx.md` — cette fiche.
