# N2.n — La distillation anglaise : 4,42 → 3,94, la chaîne complète sur 204 Mo

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : le professeur 23,57 M entraîné
> sur les 204,6 Mo d'anglais, distillé dans la base anglaise à positions aléatoires, **3 graines** :
> **3,9403** sur la validation (base **4,4234**, −10,9 %), **4,6440** sur le banc anglais (5,2967),
> **4,9545** sur wikitext2 (5,5607). Écart entre graines **±0,007**. La chaîne française et la
> chaîne anglaise donnent le même gain : la distillation vaut ~−0,5 PPL sur un corpus réel.

## Le dispositif

- **Corpus** : anglais, 120 000 articles, 204,6 Mo d'entraînement (N2.m).
- **Professeur** : 23,57 M, 20 000 pas sur l'anglais.
- **Base** : 11,47 M à positions aléatoires [0, 384] (N2.m), val 4,4234.
- **Distillation** : 20 000 pas × 16 × 128, KD T=2 α=0,7, têtes 0,1/0,05, positions [0, 384],
  **3 graines**.
- **Évaluation** : val/test anglais, banc anglais, wikitext2, courbe 129→512.

## Ce qui est mesuré

| | val anglais | banc anglais | wikitext2 | 512 |
|---|---:|---:|---:|---:|
| **base** | 4,4234 | 5,2967 | 5,5607 | 6,60 |
| **E-g1** | 3,9487 | 4,6388 | 4,9515 | 6,32 |
| **E-g2** | 3,9349 | 4,6426 | 4,9675 | 6,38 |
| **E-g3** | 3,9374 | 4,6506 | 4,9445 | — |
| **moyenne** | **3,9403** | **4,6440** | **4,9545** | **6,35** |
| écart | **−0,48** | **−0,65** | **−0,61** | −0,25 |

## Lecture

La chaîne anglaise **reproduit la chaîne française** : −10,9 % en domaine (le français : −11,7 %),
−12 % sur le banc (le français : −9 %), −11 % sur wikitext2 (le français : −14 %). Le gain de la
distillation ne dépend donc pas de la langue : c'est un **effet de la chaîne** (professeur plus
gros, même corpus), pas du français.

La courbe de longueur reste plate jusqu'à 256 (3,94 / 3,94 / 4,07) puis monte (5,05 à 384, 6,35 à
512) : le même plafond de **fenêtre locale** que le français.

## Ce que ça change pour N2

- La recette est **portable** : elle donne le même gain sur deux langues et deux corpus.
- Le plafond de longueur est lui aussi portable : la fenêtre de 256 octets, pas la position.
- Il reste à voir si un **professeur plus gros** (ou un grand modèle) apporte plus — c'est la
  question de la distillation « de qualité » (les fiches N2.h/N2.j4 utilisent un professeur de
  23,57 M, soit 2× l'élève).

## Ce qui pourrait le rendre faux

- **Trois graines, une architecture** ; l'écart entre graines (±0,007) est petit, mais un autre
  professeur dirait autre chose.
- **20 000 pas** (10 % du corpus) : ni le professeur ni l'élève ne sont convergés.
- **Le texte est du wikitexte nettoyé** (titres de section collés), même réserve que N2.j.

## Fichiers

- Professeur : `work/n2k/route-en` ; base : `work/n2k/base-en.pt` ; élèves : `work/n2k/E-g{1,2,3}.pt`.
- Mesures : `work/n2k/eval-en-distill.json` ; corpus : [`corpus-wiki-en-propre.json`](corpus-wiki-en-propre.json).
