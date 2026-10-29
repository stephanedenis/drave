# A8.3b.1 — le signe du mélange vient du **chemin lot**, pas de la taille de lot

> **Ligne de roadmap** : A8.3b · **Date** : 2026-10-29 · **Verdict** : ✅ **le basculement est
> binaire** — `--lot 1` (pas de lot) et `--lot ≥ 2` sont deux régimes ; à l’intérieur de `≥ 2`, la
> taille ne change rien à quatre décimales. Le signe du mélange 1 % bascule avec ce chemin.
>
> **Dispositif** : `drave --ppl-reparti`, Qwen2.5-0.5B Q8_0, 12 couches locales, 24 jetons,
> ctx 64 ; cinq tailles de lot × deux régimes ; données [`a83b-lot.json`](a83b-lot.json).

## Ce qui est mesuré

| lot | f32 | mélange 1 % |
|---:|---:|---:|
| **1** | **61,9920** | **58,3200** |
| 2 | **60,8135** | **62,7357** |
| 4 | **60,8135** | **62,7357** |
| 8 | **60,8135** | **62,7357** |
| 16 | **60,8135** | **62,7357** |

- **Lot 1 = pas de lot** : les valeurs sont exactement celles du mode 0 de `porte-flux`.
- **Lot ≥ 2** : identiques à quatre décimales dans chaque régime ; la taille de lot ne porte pas
  l’effet.
- En f32, lotter **améliore** (61,9920 → 60,8135, −1,9 %) ; sous la règle 1 %, lotter
  **dégrade** (58,3200 → 62,7357, +7,6 %). Le signe **bascule avec le chemin**, pas avec la taille.

## Le contrôle négatif

- **Lot 2/4/8/16** : même chiffre dans chaque régime — si la taille comptait, la courbe bougerait.
- **Lot 1** : redonne exactement le mode 0 (61,9920 / 58,3200) — le chemin « pas de lot » est
  identifié, pas supposé.
- **Déterminisme** : les valeurs sont stables à quatre décimales sur les répétitions.

## Ce qui pourrait le rendre faux

- **Un seul modèle**, 24 jetons, 12 couches locales, ctx 64 ; la bascule peut dépendre du cache
  ou du contexte.
- **Le mécanisme n’est pas isolé** : « chemin lot » est une inférence de la bascule 1/≥2, pas une
  lecture du code de cache.
- **La PPL n’est pas la qualité** : un chiffre qui baisse n’est pas une amélioration démontrée.
- **Une seule graine** ; le cache et l’ordre des passes ne sont pas vérifiés au bit près.

## Ce que ça décide

A8.3b est **rétréci** : ce n’est ni « la règle » ni « la taille de lot », c’est le **chemin de lot**
(lot 1 vs lot ≥ 2). A8.3 reste **opt-in**. Le prochain pas est d’isoler le **cache/occupation**
(même lot, ctx/cache différents) ou de lire le code du chemin lot, pas de balayer d’autres tailles.

## Fichiers

- `reports/a83b-lot.json` — les dix mesures.
- `reports/rapport-a83b-lot.md` — cette fiche.
