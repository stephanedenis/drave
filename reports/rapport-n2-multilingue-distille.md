# N2.o — La distillation multilingue : dix langues s'améliorent, la dilution reste

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : le professeur 23,57 M entraîné
> sur les 237 Mo des **dix langues**, distillé dans la base multilingue (**2 graines**), améliore
> **les dix langues** de **−0,04 à −0,47** (moyenne **−0,25**) — mais il ne récupère **pas** la
> dilution : le français reste à **5,41** contre **3,88** pour la chaîne française seule, l'anglais
> à **5,98** contre **3,94** pour la chaîne anglaise.

## La question

N2.k avait mesuré la dilution (fr +57 %, en −1,7 PPL face au monolingue) ; N2.n et N2.j4 ont montré
que la distillation vaut ~−0,5 PPL sur une langue seule. La question : la distillation
**récupère-t-elle** la dilution, ou ne fait-elle que l'adoucir ?

## Le dispositif

- **Corpus** : 237,0 Mo, 10 langues (N2.k).
- **Professeur** : 23,57 M, 20 000 pas sur les 237 Mo — **il a la même dilution** que l'élève.
- **Base** : 11,47 M, 20 000 pas (N2.k), fr 5,6842 / en 6,3024.
- **Distillation** : 20 000 pas × 16 × 128, KD T=2 α=0,7, positions [0, 384], **2 graines**.

## Ce qui est mesuré

| langue | base | M-g1 | M-g2 | moyenne | écart |
|---|---:|---:|---:|---:|---:|
| **fr** | 5,6842 | 5,4193 | 5,4056 | **5,4125** | **−0,27** |
| **en** | 6,3024 | 5,9856 | 5,9741 | **5,9799** | **−0,32** |
| **de** | 6,5047 | 6,0508 | 6,0285 | **6,0397** | **−0,47** |
| **es** | 6,0866 | 5,7610 | 5,7491 | **5,7551** | **−0,33** |
| **it** | 6,0605 | 5,8603 | 5,8642 | **5,8623** | **−0,20** |
| **pt** | 6,8002 | 6,4052 | 6,4131 | **6,4092** | **−0,39** |
| **ru** | 3,6809 | 3,6061 | 3,6062 | **3,6062** | **−0,07** |
| **ar** | 3,6064 | 3,5657 | 3,5648 | **3,5653** | **−0,04** |
| **ja** | 5,7423 | 5,5718 | 5,5814 | **5,5766** | **−0,17** |
| **zh** | 9,6509 | 9,4781 | 9,4517 | **9,4649** | **−0,19** |

## Lecture

La distillation **améliore les dix langues**, mais deux fois moins que sur une langue seule
(−0,25 contre −0,48/−0,51). La raison est simple : **le professeur a la même dilution** — il est
entraîné sur les mêmes 237 Mo, dix langues à la fois. Il ne peut pas enseigner à l'élève une
précision qu'il n'a pas.

Le résultat central est donc un **plafond de capacité** : à 11,47 M, la chaîne multilingue
(5,41 / 5,98) reste à 1,5–2,0 PPL des chaînes monolingues (3,88 / 3,94). La distillation ne
remplace pas la capacité — elle transporte ce que le professeur sait, et le professeur sait la même
chose en plus petit.

Les langues déjà bien apprises (ru 3,61, ar 3,57) gagnent presque rien (−0,07, −0,04) : le
professeur n'a rien de plus à leur donner.

## Ce que ça change pour N2

- **Pour R** (lire dix langues avec un modèle) : la chaîne multilingue est **meilleure que la
  base** partout — c'est la version à livrer si le budget est d'un modèle.
- **Pour la précision par langue** : un modèle par langue reste 1,5–2,0 PPL devant ; le choix est
  un choix de budget, pas de recette.
- **La loi d'échelle** : à 21,65 M (N2.j3, où la capacité paie sur le corpus réel), le coût par
  langue baisserait — c'est la mesure qui manque.

## Ce qui pourrait le rendre faux

- **Deux graines** seulement ; les écarts entre graines sont petits (±0,01) mais l'intervalle n'est
  pas mesuré.
- **Un professeur de même taille** que l'élève×2 : un grand modèle (ou un professeur monolingue par
  langue) changerait la conclusion.
- **20 000 pas** (8 % du corpus) : aucune des deux chaînes n'est convergée.
- **Le texte est du wikitexte nettoyé**, même réserve que N2.j.

## Fichiers

- Professeur : `work/n2k/route-multi` ; base : `work/n2k/base-multi.pt` ; élèves :
  `work/n2k/M-g{1,2}.pt`.
- Mesures : `work/n2k/eval-multi-distill.json`, `eval-multi-g2.json` ; corpus :
  [`corpus-multi-propre.json`](corpus-multi-propre.json).
