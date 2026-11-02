# N2.r — Le 34,3 M distillé : **3,69**, le meilleur modèle de la nuit, et la courbe plate

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : le modèle de **34,3 M** distillé
> depuis le professeur 23,57 M vaut **3,6852** sur la validation (base 34,3 M : 3,9973, −0,31),
> **6,78** en littérature (7,38), **10,92** en anglais (11,98), **11,64** sur wikitext2 (13,42) et
> **4,10** à 512 octets (4,19) — la meilleure chaîne française de la nuit, et la courbe de longueur
> la plus plate (3,69 / 3,64 / 3,68 / 3,89 / 4,09).

## La question

N2.p a montré que la capacité paie (4,39 → 4,00 de 11,47 à 34,3 M) et que la longueur s'aplatit.
N2.j4 a montré que la distillation paie sur 11,47 M. La question : les deux **se composent-ils**, et
que vaut le meilleur modèle possible ce soir ?

## Le dispositif

- Corpus : 186,1 Mo (N2.j).
- Base : **34,3 M** (`384/512`), 20 000 pas, positions [0, 384] (N2.p), val 3,9973.
- Professeur : 23,57 M (`route`, N2.j) — **plus petit que l'élève**.
- Distillation : 20 000 pas × 16 × 128, KD T=2 α=0,7, positions [0, 384], **2 graines**.

## Ce qui est mesuré

| modèle | params | val | littérature | anglais | wikitext2 | 512 | 384 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 11,47 M base | 11,8 M | 4,3893 | 7,90 | 13,72 | 14,94 | 5,67 | 5,05 |
| 11,47 M distillé | 11,8 M | 3,8761 | 7,18 | 12,30 | 12,89 | 5,76 | 4,79 |
| 21,65 M base | 21,6 M | 4,2013 | 7,46 | 13,55 | 14,52 | 5,03 | 4,66 |
| 34,3 M base | 34,3 M | 3,9973 | 7,38 | 11,98 | 13,42 | 4,19 | 4,08 |
| **34,3 M distillé** | 34,3 M | **3,6852** | **6,78** | **10,92** | **11,64** | **4,10** | **3,89** |
| écart base → distillé | — | **−0,31** | −0,60 | −1,06 | −1,78 | −0,09 | −0,19 |

## Lecture

**Les deux leviers se composent** : la capacité fait 4,39 → 4,00, la distillation 4,00 → 3,69. Le
meilleur modèle français de la nuit vaut **3,6852** en domaine, **6,78** en littérature, **10,92**
en anglais et **4,10** à 512 octets — à comparer au 3,0904 de N2.h sur le **dépôt** (autre corpus,
autre difficulté : la PPL wiki n'est pas comparable).

**Le professeur plus petit que l'élève fonctionne.** Le 23,57 M guide un 34,3 M : les étiquettes
douces régularisent et l'élève a la capacité de les exploiter. La distillation n'exige pas un
professeur plus gros — elle exige un professeur **qui sait autre chose** (ici : les mêmes données,
mais une vue plus stable).

**La courbe de longueur est presque plate** : 3,69 / 3,64 / 3,68 / 3,89 / 4,09. À 512 octets, le
modèle ne perd que 11 % contre 40 % pour le 11,47 M (5,67) — le « verrou » de longueur est
largement une affaire de capacité (N2.p), et la distillation ne le rouvre pas.

## Ce que ça change pour N2

- La **recette de production** est fixée : corpus réel 186 Mo, positions aléatoires, base 34,3 M,
  professeur 23,57 M, distillation 2-3 graines → **3,69 / 6,78 / 10,92 / 4,10**.
- C'est le modèle à donner à R pour la lecture longue (la fenêtre de 256 octets reste, mais le
  modèle l'exploite entièrement).
- La **porte < 2,5** n'est pas franchie pour autant : elle est sur le corpus du dépôt, pas sur le
  wiki ; et le chemin qui reste est le corpus, pas la capacité (N2.i, N2.j).

## Ce qui pourrait le rendre faux

- **Deux graines** ; l'écart entre graines (0,004) est petit mais l'intervalle n'est pas mesuré.
- **20 000 pas** (11 % du corpus) : ni la base ni l'élève ne sont convergés ; le gain est un
  minorant.
- **Le professeur est plus petit que l'élève** : un professeur 34,3 M (ou un grand modèle)
  donnerait peut-être plus — c'est la question ouverte.
- **Le texte est du wikitexte nettoyé**, même réserve que N2.j.

## Fichiers

- Base : `work/n2j/base-wiki-45m.pt` ; élèves : `work/n2j/W34-g{1,2}.pt` ; professeur :
  `work/n2j/route-wiki`.
- Mesures : `work/n2j/eval-34-distill.json` ; corpus : [`corpus-wiki-propre.json`](corpus-wiki-propre.json).
