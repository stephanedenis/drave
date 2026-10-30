# A8.3b/c — décision : le défaut reste opt-in, la cause est le chemin lot

> **Ligne de roadmap** : A8.3b/c · **Date** : 2026-10-29 · **Verdict** : ⛔ **défaut refusé** —
> le signe du mélange 1 % bascule avec le **chemin lot binaire** (lot 1 contre lot ≥ 2), pas
> avec la taille du cache (ctx 64/256/512 identiques). A8.3 reste **opt-in**.
>
> **Dispositif** : synthèse des mesures A8.3a/b/c, aucun nouveau run ; données
> [`a83b-decision.json`](a83b-decision.json).

## Les chiffres qui décident

| régime | lot 1 | lot 2 | lot 4 |
|---|---:|---:|---:|
| f32 | **61,9920** | **60,8135** | **60,8135** |
| 1 % | **58,3200** | **62,7357** | **62,7357** |

- **Lot 1 = pas de lot** : les chiffres redonnent le mode 0.
- **Lot ≥ 2** : identiques ; la taille de lot ne porte pas l’effet.
- **Ctx 64/256/512** : 24 exécutions, aucune ligne ne bouge — le cache n’est pas la cause.
- Le signe **bascule avec le chemin** : f32 lotte mieux, 1 % lotte moins bien.

## Pourquoi le défaut est refusé

- **18 portes PPL épinglées**, mais seulement **3** ont un régime 1 % dual (flux, pont, coupe).
- Un défaut déplacerait les 15 autres ; ce serait une régression silencieuse.
- La cause est **le chemin `forward_lot`** (quantification d’activation i32, attention dense,
  ordre des passes), pas une taille de cache. Tant qu’il n’est pas instrumenté, le défaut
  ferait bouger les chiffres sans explication.

## Condition pour passer le défaut

1. instrumenter `forward_lot` (activating i32 vs chemin jeton) et isoler l’effet ;
2. donner un régime 1 % **dual** aux 18 portes épinglées ;
3. rejouer toutes les portes sous le défaut et vérifier qu’aucune ne régresse.

## Le contrôle négatif

- **24 exécutions** ctx × lot × régime ; ctx seul ne change rien.
- **Lot 1 = mode 0** ; lot 2/4 identiques.
- **A8.3a** : flux/pont/coupe passent dans les deux régimes.
- **A8.3b1** : le balayage lot 1/2/4/8/16 montre la bascule binaire.

## Ce qui pourrait le rendre faux

- **Un seul modèle**, 24 jetons ; le chemin lot peut varier avec le matériel.
- **Pas d’instrumentation** : la cause est une inférence de la bascule, pas une lecture de code.
- **La PPL n’est pas la qualité** : un chiffre qui baisse n’est pas un gain.

## Ce que ça change

A8.3b/c est **décidé** : opt-in, cause lot, condition nommée. A8.3a reste le socle dual.
Prochain : A8.3b2 (instrumentation `forward_lot`) ou B11.10.

## Fichiers

- `reports/a83b-decision.json` — la décision.
- `reports/rapport-a83b-decision.md` — cette fiche.
