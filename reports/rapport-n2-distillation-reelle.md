# N2.j4 — La distillation sur le corpus réel : 4,39 → 3,88, et tout le reste baisse

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : le professeur 23,57 M entraîné
> sur les 186 Mo de Wikipédia, distillé dans la base 11,47 M à positions aléatoires, **3 graines** :
> **3,8761** sur la validation (base : **4,3893**, −11,7 %), **7,18** en littérature (7,90),
> **12,30** en anglais (13,72), **12,89** sur wikitext2 (14,94), **6,41** sur la validation du
> dépôt (7,11). L'écart entre graines est de **±0,004**.

## La question

N2.h avait montré la chaîne complète sur 3,24 Mo (professeur 23,57 M, base 11,47 M, distillation) ;
N2.j avait montré le corpus réel (186 Mo) sur la **base seule**. La question restait : le gain du
corpus réel survit-il à la **distillation** — et le professeur apporte-t-il encore quelque chose
quand la base a déjà 186 Mo ?

## Le dispositif

- **Professeur** : 23,57 M (`--famille route`, dim 384, 6 couches), 20 000 pas sur les 186 Mo,
  meilleur point val **1,6655 bit/octet**.
- **Base** : 11,47 M à positions aléatoires [0, 384] (N2.j2), val 4,3893.
- **Distillation** : 20 000 pas × 16 × 128, lr 1e-4 puis 3e-5, KD T=2 α=0,7, têtes précoces et
  locales (0,1 / 0,05), **positions aléatoires [0, 384]**, **3 graines** (décalage de corpus
  10 000 019 par graine).
- **Évaluation** : val/test du corpus, littérature, anglais, wikitext2, courbe 129→512,
  décomposition, validation du dépôt.

## Ce qui est mesuré

| | val wiki | test | littérature | anglais | wikitext2 | val du dépôt | 512 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **base** (positions) | 4,3893 | — | 7,90 | 13,72 | 14,94 | 7,11 | 5,67 |
| **W-g1** | 3,8766 | 3,9659 | 7,16 | 12,24 | 12,86 | — | 5,78 |
| **W-g2** | 3,8794 | 3,9676 | 7,18 | 12,26 | 12,84 | — | 5,81 |
| **W-g3** | 3,8722 | 3,9556 | 7,21 | 12,39 | 12,96 | 6,41 | 5,69 |
| **moyenne** | **3,8761** | **3,9630** | **7,18** | **12,30** | **12,89** | **6,41** | **5,76** |
| écart | **−0,51** | — | −0,72 | −1,42 | −2,05 | −0,70 | +0,09 |

Courbe de longueur (moyenne des graines) : **3,88 / 3,86 / 3,98 / 4,79 / 5,72** à 129/192/256/384/
512 octets — plate jusqu'à 256, puis la fenêtre locale (256) reprend la main.

## Lecture

La distillation **fonctionne sur le corpus réel** : −11,7 % en domaine, −9 % en littérature,
−10 % en anglais, −14 % sur wikitext2. Le professeur apporte donc encore quelque chose alors que la
base a 186 Mo — mais moins qu'à 3,24 Mo (N2.h : −5 % en domaine, mais la base y était meilleure :
3,24). Ici la base est faible (4,39) et le professeur fort (1,67 bit/octet) : l'écart est plus
grand, et la distillation le récupère largement.

L'**écart entre graines** (±0,004) est négligeable devant le gain (−0,51) : le résultat est stable.

Le point à surveiller : à 512 octets, la distillation **ne gagne rien** (5,67 → 5,76) — la fenêtre
locale de 256 octets reste le plafond, et le professeur (même fenêtre) ne peut pas le lever.

## Ce que ça change pour N2

- La **recette de production** du corpus réel est complète : base à positions aléatoires (N2.j2),
  professeur 23,57 M, distillation 3 graines, positions conservées (N2.j4) → **3,88** en domaine,
  **7,18 / 12,30 / 12,89** hors domaine.
- Le **canal de structure** (N2.l, −0,22) n'est pas dans cette chaîne : il reste à voir s'il
  s'ajoute à la distillation ou s'il est absorbé par elle.
- La **fenêtre locale** est le plafond qui reste : la question de R1 (un schéma pour lire plus
  loin) est maintenant chiffrée sur le corpus réel.

## Ce qui pourrait le rendre faux

- **Trois graines, une architecture** : l'écart entre graines est petit, mais un autre professeur
  (plus gros, ou un grand modèle) dirait autre chose.
- **20 000 pas** : ni le professeur ni l'élève ne sont convergés ; le gain est un minorant.
- **Le texte wiki est du wikitexte nettoyé** (titres de section collés) : la PPL n'est pas
  comparable à celle du dépôt, seule la **comparaison interne** (base vs distillé) l'est.
- **La validation du dépôt** (6,41) est un transfert croisé : elle mesure la survie du français
  général, pas la qualité du wiki.

## Fichiers

- Professeur : `work/n2j/route-wiki` ; base : `work/n2j/base-wiki-pos.pt` ; élèves :
  `work/n2j/W-g{1,2,3}.pt`.
- Mesures : `work/n2j/eval-distill.json`, `eval-distill-repo.json`.
- Corpus et manifeste : [`corpus-wiki-propre.json`](corpus-wiki-propre.json).
