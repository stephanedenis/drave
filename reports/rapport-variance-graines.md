# La variance du run-à-run : trois graines de `wiki_big` à 30 000 pas

> **Ligne de roadmap** : N · **Date** : 2026-11-20 · **Verdict** : ✅ mesuré — à 30 000 pas, les
trois graines de `wiki_big` donnent **7,2237 / 7,3531 / 7,4240 / 7,5607** (deux exécutions de la
graine 1, puis les graines 2 et 3), soit une **étendue de 4,7 %** — plus grande que les écarts fins
que la sélection prétendait mesurer (**0,5 %** avec v1, **3,6 %** avec v2). Le même corpus (`wiki_big`, 831 Mo), la même recette (lr 1e-4, AMP, `d=896`), trois
> graines (1, 2, 3) et deux exécutions de la graine 1 (l'après-midi et la nuit). Le juge est
> **wikitext2** (352 256 jetons).
>
> **Pourquoi** : la nuit du 19-20/11 a montré que le rejeu de la graine 1 donne **7,3531** contre
> **7,2237** l'après-midi (**+1,8 %**), alors que le pas 1 est bit-identique. Si le bruit est de cet
> ordre, les écarts fins de la sélection (2-3 %) ne sont pas significatifs — il faut le chiffrer.

## Les résultats

| graine | 10 000 | 20 000 | 30 000 |
|---|---:|---:|---:|
| 1 (après-midi) | — | — | **7,2237** |
| 1 (nuit) | 8,8598 | 7,8340 | **7,3531** |
| 2 | 8,7836 | 7,8909 | **7,4240** |
| 3 | 9,4978 | 8,1700 | **7,5607** |

À 30 000 pas : moyenne **7,39**, écart-type **0,13** (1,8 %), étendue **4,7 %**.

## Ce que le tableau dit déjà

1. **À 10 000 pas, l'écart entre graines est de 8 %** (8,78 à 9,50) — l'initialisation et les
   premiers pas dominent ; un point de mesure à 10k ne juge rien.
2. **À 20 000 pas, il se resserre** (7,83 à 8,17, ~4 %) ;
3. **La même graine ne rejoue pas** : 7,2237 contre 7,3531 (+1,8 %) — le non-déterminisme GPU
   s'ajoute à l'effet de graine ; l'étendue totale (4,7 %) est la somme des deux.

## Ce qui pourrait le rendre faux

- Trois graines, deux points de rejeu : c'est une **estimation** de la dispersion, pas une
  distribution.
- Le corpus est le même pour toutes les graines : la variance mesurée est celle de
  **l'entraînement**, pas celle du corpus.
- wikitext2 est un val **unique** : sa propre variance d'échantillonnage n'est pas mesurée ici.

## Voir aussi

- [la sélection du contenu](rapport-selection-contenu.md) · [la nuit](rapport-nuit-wikibig.md) ·
  [les runs](rapport-150m-nuit.md)
