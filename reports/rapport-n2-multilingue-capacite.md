# N2.q — La capacité multilingue : à recette égale, 21,65 M gagne 0,79

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : à recette égale (20 000 pas,
> positions aléatoires [0, 384]), le modèle **21,65 M** bat le 11,47 M sur **les dix langues** :
> français **5,8871** contre **6,6781** (−0,79), anglais **6,5663** contre 7,4888 (−0,92),
> allemand −1,08, chinois −0,79. La capacité paie aussi en multilingue. Mais la **randomisation des
> positions coûte cher** dans cette configuration (+1,0 en français contre +0,36 en monolingue).

## La question

N2.k avait comparé le multilingue au monolingue ; N2.o avait montré que la distillation ne
récupère pas la dilution. La question de la **loi d'échelle multilingue** : à récipe constant, la
capacité réduit-elle le coût par langue ? Et que coûte la randomisation des positions sur un corpus
mélangé ?

## Le dispositif

- Corpus : `data/wiki_multi/propre/train.txt` (237,0 Mo, 10 langues, N2.k).
- Trois points : **11,47 M sans positions** (N2.k, la référence d'origine), **11,47 M avec
  positions** (contrôle), **21,65 M avec positions** (`296/416`).
- Recette : 20 000 pas × 8 × 128, lr 3e-4, graine 1 ; évaluation par langue sur les vals de N2.k.

## Ce qui est mesuré

| modèle | fr | en | de | es | it | pt | ru | ar | ja | zh |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **11,47 M, sans positions** | 5,6842 | 6,3024 | 6,5047 | 6,0866 | 6,0605 | 6,8002 | 3,6809 | 3,6064 | 5,7423 | 9,6509 |
| **11,47 M, positions** | 6,6781 | 7,4888 | 7,8737 | 7,1575 | 7,1267 | 7,9627 | 4,1871 | 4,0108 | 6,4343 | 10,3512 |
| **21,65 M, positions** | **5,8871** | **6,5663** | **6,7893** | **6,4093** | **6,4180** | **7,1318** | **3,9106** | **3,7429** | **5,8242** | **9,5640** |
| écart 21,65 / 11,47 (positions) | **−0,79** | −0,92 | −1,08 | −0,75 | −0,71 | −0,83 | −0,28 | −0,27 | −0,61 | −0,79 |

## Lecture

**La capacité paie en multilingue** : le 21,65 M gagne 0,27 à 1,08 PPL sur les dix langues, à
recette identique — la loi de N2.p (monolingue) se transporte. Mais le gain est **inégal** : fort
sur les langues latines et le chinois, faible sur le russe et l'arabe (déjà à 3,6-4,0, peu de marge).

**Les positions coûtent cher en multilingue** : +1,0 en français (5,68 → 6,68) et +1,2 en anglais,
contre +0,36 en monolingue (N2.j2). Apprendre une position relative sur dix langues à la fois est
plus difficile — et c'est justement ce que la capacité récupère en partie (6,68 → 5,89).

**La dilution reste** : le meilleur multilingue (5,89) est encore à 1,9 PPL du français seul
distillé (3,88) et à 1,6 de l'anglais seul (3,94). La capacité réduit le coût, elle ne l'annule pas.

## Ce que ça change pour N2

- **La loi d'échelle est générale** : à recette égale, chaque palier de capacité vaut ~−0,2 à −0,8
  selon la langue — le multilingue n'échappe pas à la règle.
- **Le choix de R** : le multilingue 21,65 M (5,89 / 6,57) est la version à livrer avec la
  robustesse de longueur ; les chaînes monolingues restent devant pour la précision.
- **La randomisation des positions** doit être **entraînée plus longtemps** en multilingue (20 000
  pas = 8 % du corpus) : son coût est peut-être un coût de convergence.

## Ce qui pourrait le rendre faux

- **Une graine** par point ; les écarts sont grands (0,3 à 1,1), l'intervalle n'est pas mesuré.
- **20 000 pas** (8 % du corpus) : les trois modèles sont loin de la convergence, et le plus gros
  l'est le plus.
- **Les vals par langue** (1 000 articles chacune) : la difficulté varie d'une langue à l'autre ;
  seules les **comparaisons entre modèles** pour une même langue sont valides.
- **Le texte est du wikitexte nettoyé**, même réserve que N2.j.

## Fichiers

- Points de contrôle : `work/n2k/base-multi.pt` (11,47 M sans positions), `base-multi-11m-pos.pt`,
  `base-multi-21m.pt`.
- Mesures : `work/n2k/eval-multi-11m-pos.json`, `eval-multi-21m.json`, `eval-multi.json`.
