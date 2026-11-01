# N2.h5 — La capacité sur le mètre propre : 21,65 M contre 11,47 M

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : à données, professeur et
> budget égaux, le modèle de **21,65 M** (×1,89) vaut **3,0286** en domaine contre **3,0904**
> et **17,02** sur la littérature jamais vue contre **16,70** — la capacité **paie**.

## La question

La roadmap laissait une question ouverte après N2.5b et N2.9 : la capacité paie-t-elle ? Les deux
mesures historiques étaient faites sur le jeu **contaminé** (5 000 pas : −8,1 % pour 21,63 M ;
20 000 pas : 3,381 contre 3,123, négatif). Sur le corpus propre, avec le même professeur et le
même budget, la réponse est-elle la même ?

## Le dispositif

Même recette que [`n2-propre`](rapport-n2-propre.md), à un seul changement près : le modèle passe
de `d_model = 224, expert_hidden = 288` (**11 469 192** paramètres) à `d_model = 296,
expert_hidden = 416` (**21 646 224**, ×1,89) — la même famille, deux fois plus large.

| pièce | valeur |
|---|---|
| corpus | `data/corpus_propre/train.txt` (dédupliqué, 0 % de fuite) |
| professeur | le même (23,57 M, corpus propre) |
| base | 21,65 M, 20 000 pas supervisés |
| distillation | 20 000 pas × 16 × 128, lr 1e-4 puis 3e-5, **2 graines** |

## Ce qui est mesuré

| bras | params | val | test | littérature | anglais | 256 octets |
|---|---:|---:|---:|---:|---:|---:|
| **A — 11,47 M** | 11 469 192 | 3,0904 | 3,1960 | 16,70 | 57,58 | 14,11 |
| **CAP — 21,65 M** | 21 646 224 | 3,0286 | 3,1500 | 17,02 | 57,17 | 14,07 |

## Lecture

En domaine, le modèle de 21,65 M vaut **3,0286** contre **3,0904** (**−0,062**) : la capacité **paie**, mais peu. Sur la littérature, **17,02** contre **16,70** — elle ne répare rien ; en anglais, **57,17** contre **57,58** — rien ; et à 256 octets, **14,07** contre **14,11** — rien non plus. La capacité est un gain de **précision en domaine**, pas de **couverture**.

## Ce que ça change pour N2

La capacité **paie**, mais elle ne **couvre pas** : +89 % de paramètres donnent **−0,062** en domaine, alors que la généralité (littérature : 17,02 contre 16,70) et la longueur (256 : 14,07 contre 14,11) ne bougent pas. C'est un gain de **précision**, pas de **couverture** : le levier de la généralité reste le corpus (÷ 4,3 hors dépôt, fiche `n2-diversite`), et celui de la longueur les positions (`n2-longueur`).

## Ce qui pourrait le rendre faux

- **Deux graines** seulement : l'écart entre graines de la distillation vaut ~0,005 en domaine, et
  l'effet mesuré est −0,062 — au-dessus du bruit, mais sans l'intervalle de trois graines.
- **Le budget est le même** (20 000 pas) : un modèle plus gros n'a peut-être pas convergé ; c'est
  exactement le reproche fait à N2.9.
- **Le corpus est petit** (3,24 Mo d'entraînement) : la capacité peut n'être utile qu'avec plus de
  données — c'est la limite de l'expérience, pas une conclusion sur la capacité en général.

## Fichiers

- Code : [`tools/entrainer_native.py`](../tools/entrainer_native.py) (`--dim`, `--expert-hidden`) ·
  [`tools/distiller_budget.py`](../tools/distiller_budget.py).
- Points de contrôle : `work/n2h/base-capacite.pt`, `work/n2h/CAP-g{1,2}.pt`.
