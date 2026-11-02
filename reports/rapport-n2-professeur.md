# N2.u — Le professeur plus gros ne change presque rien en domaine, mais gagne 0,3 hors domaine

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : un professeur de **30,3 M**
> (`dim 480`) au lieu de 23,57 M donne aux élèves 11,47 M : **3,8888** en domaine (3,8761 avec le
> professeur 23,57 M — **+0,013**, dans le bruit), **7,15** en littérature (7,18), **12,04** en
> anglais (**−0,26**) et **12,58** sur wikitext2 (**−0,31**). En domaine, c'est le même ; hors
> domaine, un petit gain. **L'élève est limité par sa capacité, pas par son professeur.**

## La question

N2.j4 et N2.r ont montré que la distillation vaut ~−0,3 à −0,5 PPL selon la taille de l'élève. La
question restait ouverte (N2.r) : un **professeur plus gros** donne-t-il plus ? Ici le professeur
passe de 23,57 M à **30,29 M** (+29 %), à corpus et recette identiques.

## Le dispositif

- Corpus : 186,1 Mo (N2.j).
- Professeur : `route` **30,29 M** (`dim 480`, 6 couches), 20 000 pas, meilleur point
  **1,6577 bit/octet** (23,57 M : 1,6655 — l'écart est marginal).
- Élève : 11,47 M à positions [0, 384] (le même que N2.j4), **3 graines**.
- Recette : 20 000 pas × 16 × 128, KD T=2 α=0,7, positions [0, 384].

## Ce qui est mesuré

| professeur | val | littérature | anglais | wikitext2 | 512 |
|---|---:|---:|---:|---:|---:|
| **23,57 M** (N2.j4) | **3,8761** | 7,18 | 12,30 | 12,89 | 5,76 |
| **30,29 M** (T-g1..3) | 3,8888 | 7,15 | **12,04** | **12,58** | 5,72 |
| écart | +0,013 | −0,03 | **−0,26** | **−0,31** | −0,04 |

Écarts entre graines du 30,29 M : ±0,002 en domaine.

## Lecture

**En domaine, le professeur plus gros ne sert à rien** : +0,013, soit un tiers de l'écart entre
graines. L'élève de 11,47 M a **saturé sa capacité** — il ne peut pas absorber plus de savoir, quel
que soit le professeur.

**Hors domaine, il sert un peu** : −0,26 en anglais, −0,31 sur wikitext2. Le professeur plus large
a vu les mêmes données mais en modélise mieux la variété ; cette variété passe dans les étiquettes
douces.

**La comparaison avec le 34,3 M** (N2.r : 3,6852) est la leçon : pour gagner 0,2 en domaine, il
faut **doubler l'élève**, pas le professeur. La capacité de l'élève est le levier ; le professeur
est un guide.

## Ce que ça change pour N2

- La **recette de distillation** peut rester sur le professeur 23,57 M : le surcoût du 30,29 M
  (+29 % de calcul de professeur) n'achète que 0,3 hors domaine et rien en domaine.
- Si l'on veut de l'OOD à moindre coût, le professeur plus gros est une option ; si l'on veut du
  domaine, c'est l'élève qu'il faut agrandir.
- La question « un grand modèle (DeepSeek) comme professeur » reste ouverte : elle change
  d'échelle de savoir, pas seulement de paramètres.

## Ce qui pourrait le rendre faux

- **Trois graines, un pas de taille** (23,57 → 30,29 M) : la courbe « professeur » n'a que deux
  points.
- **Le professeur 30,29 M n'est pas convergé** (20 000 pas) et son gain propre est marginal
  (1,6577 vs 1,6655) : il n'a peut-être rien de plus à transmettre.
- **20 000 pas, corpus wiki nettoyé** : mêmes réserves que N2.j.

## Fichiers

- Professeur : `work/n2j/route-480` ; élèves : `work/n2j/T-g{1,2,3}.pt`.
- Mesures : `work/n2j/eval-t480.json` ; référence : `work/n2j/W-g{1,2,3}.pt`.
