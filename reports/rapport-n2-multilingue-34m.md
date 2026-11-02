# N2.t — Le multilingue à 34,3 M : 6,68 → 5,89 → 5,58, le rendement décroît

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : à recette égale (positions
> [0, 384]), le français multilingue passe de **6,6781** (11,47 M) à **5,8871** (21,65 M) puis
> **5,5825** (34,3 M) : la capacité paie encore, mais **le gain par palier diminue** (−0,79 puis
> −0,31). À 34,3 M, le multilingue rejoint presque le 11,47 M **sans** positions (5,6842) : la
> capacité a payé le coût de la randomisation.

## Le dispositif

- Corpus : `data/wiki_multi/propre/train.txt` (237,0 Mo, 10 langues).
- Trois tailles, même recette : 20 000 pas × 8 × 128, lr 3e-4, graine 1, positions [0, 384].
- Évaluation par langue, sur les vals de N2.k (1 000 articles par langue).

## Ce qui est mesuré

| modèle | fr | en | de | es | it | pt | ru | ar | ja | zh |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 11,47 M, sans positions | 5,6842 | 6,3024 | 6,5047 | 6,0866 | 6,0605 | 6,8002 | 3,6809 | 3,6064 | 5,7423 | 9,6509 |
| 11,47 M, positions | 6,6781 | 7,4888 | 7,8737 | 7,1575 | 7,1267 | 7,9627 | 4,1871 | 4,0108 | 6,4343 | 10,3512 |
| 21,65 M, positions | 5,8871 | 6,5663 | 6,7893 | 6,4093 | 6,4180 | 7,1318 | 3,9106 | 3,7429 | 5,8242 | 9,5640 |
| **34,3 M, positions** | **5,5825** | **6,0952** | **6,2443** | **5,9133** | **6,0405** | **6,6244** | **3,8204** | **3,6818** | **5,5826** | **8,9806** |
| écart 34 / 21 | **−0,30** | −0,47 | −0,55 | −0,50 | −0,38 | −0,51 | −0,09 | −0,06 | −0,24 | −0,58 |

## Lecture

**Le rendement décroît** : −0,79 (11 → 21) puis −0,31 (21 → 34). C'est la première fois que la loi
log-linéaire de N2.p (monolingue : −0,19 par palier, sans décroissance) montre une **saturation** —
et elle apparaît en multilingue, là où le corpus par langue est le plus petit (21 Mo par langue).

**La capacité paie le coût des positions** : le 34,3 M avec positions (5,58) rejoint le 11,47 M
sans positions (5,68) ; autrement dit, à budget de calcul égal, on peut avoir la **robustesse de
longueur** sans payer en PPL — mais il faut ×3 de paramètres.

**La dilution reste** : 5,58 en français multilingue contre **3,69** pour le 34,3 M français
distillé (N2.r) — 1,9 PPL. La capacité réduit le coût par langue, elle ne l'annule pas : à
paramètres égaux, un modèle par langue reste devant.

## Ce que ça change pour N2

- La **loi d'échelle multilingue** a maintenant trois points et une saturation visible : le
  prochain palier utile n'est pas 60 M sur ce corpus, c'est **plus de texte par langue** (le wiki
  complet, pas 12 000 articles).
- Le **34,3 M multilingue** (5,58 / 6,10 / 8,98 en chinois) est la meilleure base multilingue de la
  nuit — à distiller si R veut un modèle unique pour dix langues.
- La **distillation multilingue** (N2.o) n'a pas été refaite à 34,3 M : c'est la suite naturelle.

## Ce qui pourrait le rendre faux

- **Une graine** par point ; les écarts (0,3 à 0,6) sont grands mais l'intervalle n'est pas mesuré.
- **20 000 pas** (8 % du corpus) : le 34,3 M est le moins convergé — la saturation est peut-être un
  artefact de budget.
- **1 000 articles par langue** en validation : la difficulté varie ; seules les comparaisons entre
  modèles pour une même langue sont valides.
- **Le texte est du wikitexte nettoyé**, même réserve que N2.j.

## Fichiers

- Points de contrôle : `work/n2k/base-multi-34m.pt` (34,3 M), `base-multi-21m.pt`,
  `base-multi-11m-pos.pt`, `base-multi.pt`.
- Mesures : `work/n2k/eval-multi-34m.json`, `eval-multi-21m.json`, `eval-multi-11m-pos.json`.
