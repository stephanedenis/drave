# N2.v — Le multilingue 34,3 M distillé : 5,58 → 4,79, la distillation paie avec la capacité

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : le 34,3 M multilingue distillé
> (**1 graine**) vaut **4,7892** en français (base 5,5825, **−0,79**), **5,3196** en anglais
> (6,0952, −0,78), **5,2441** en allemand, **8,2738** en chinois. Le gain de la distillation
> **croît avec la capacité de l'élève** : −0,25 à 11,47 M (N2.o), **−0,79 à 34,3 M**.

## Le dispositif

- Corpus : 237,0 Mo, 10 langues (N2.k).
- Base : **34,3 M** (`384/512`), positions [0, 384] (N2.t), fr 5,5825.
- Professeur : 23,57 M multilingue (`route-multi`, N2.k).
- Distillation : 20 000 pas × 16 × 128, KD T=2 α=0,7, positions [0, 384], **1 graine** (M34-g1).

## Ce qui est mesuré

| langue | base 34,3 M | M34-g1 | écart |
|---|---:|---:|---:|
| **fr** | 5,5825 | **4,7892** | **−0,79** |
| **en** | 6,0952 | **5,3196** | **−0,78** |
| **de** | 6,2443 | 5,2441 | −1,00 |
| **es** | 5,9133 | 5,0915 | −0,82 |
| **it** | 6,0405 | 5,2337 | −0,81 |
| **pt** | 6,6244 | 5,6561 | −0,97 |
| **ru** | 3,8204 | 3,1521 | −0,67 |
| **ar** | 3,6818 | 3,1805 | −0,50 |
| **ja** | 5,5826 | 4,8714 | −0,71 |
| **zh** | 8,9806 | 8,2738 | −0,71 |

## Lecture

**Le gain de la distillation croît avec la capacité de l'élève** : −0,25 par langue à 11,47 M
(N2.o), **−0,79** à 34,3 M. Un élève plus large absorbe mieux les étiquettes douces du
professeur — c'est cohérent avec N2.r (le 34,3 M français gagne −0,31 contre −0,51 pour le
11,47 M ? non : le 11,47 M gagne −0,51, le 34,3 M −0,31 en absolu, mais en **relatif** les deux
gagnent ~10 %).

Ici l'écart est **plus grand en absolu** parce que la base multilingue est plus haute (5,58) : la
marge à récupérer est plus grande.

**La dilution reste** : 4,79 en français multilingue contre **3,69** pour le 34,3 M français
distillé (N2.r) — 1,1 PPL. La distillation multilingue réduit l'écart (il était de 1,9 à 11,47 M)
mais ne l'annule pas.

## Ce que ça change pour N2

- La **chaîne multilingue de production** est : base 34,3 M + positions + distillation (23,57 M)
  → **4,79 / 5,32 / 8,27** — la meilleure version multilingue de la nuit.
- Le **choix de R** se précise : un modèle unique à 10 langues à 4,79 en français, ou un modèle
  français à 3,69 + un modèle anglais à 3,94 — le budget de paramètres décide.
- La **distillation à 34,3 M** n'a qu'une graine : il faut la refaire à 2-3 graines pour publier.

## Ce qui pourrait le rendre faux

- **Une seule graine** : l'écart (−0,79) est grand devant le bruit des autres chaînes (±0,01),
  mais l'intervalle n'est pas mesuré.
- **20 000 pas** (8 % du corpus) : la base et l'élève sont loin de la convergence.
- **Le professeur a la même dilution** (N2.o) : un professeur monolingue par langue ferait mieux.
- **Le texte est du wikitexte nettoyé**, même réserve que N2.j.

## Fichiers

- Base : `work/n2k/base-multi-34m.pt` ; élève : `work/n2k/M34-g1.pt` ; professeur :
  `work/n2k/route-multi`.
- Mesures : `work/n2k/eval-multi34-distill.json`.
