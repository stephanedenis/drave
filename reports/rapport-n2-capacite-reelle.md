# N2.j3 — La capacité sur 186 Mo : 21,65 M paie (4,39 → 4,20, et mieux partout)

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : à données et budget égaux
> (20 000 pas, positions 0–384), le modèle de **21,65 M** vaut **4,2013** contre **4,3893** pour
> 11,47 M, **7,46** contre **7,90** en littérature, **13,55** contre **13,72** en anglais, **5,03**
> contre **5,67** à 512 octets. Sur 3,24 Mo, N2.h5 ne gagnait que **−0,06** ; sur 186 Mo, la
> capacité paie — **quand les données suivent**.

## La question

N2.h5 avait mesuré la capacité sur le petit corpus (3,24 Mo) : 21,65 M contre 11,47 M, **−0,06** en
domaine, aucun gain hors domaine — « un gain de précision, pas de couverture », et surtout un gain
minuscule. La question restait ouverte : était-ce la capacité qui ne paie pas, ou les **données**
qui ne la nourrissent pas ? Le corpus réel (186 Mo, N2.j) permet de trancher.

## Le dispositif

- **Corpus** : `data/wiki_fr/propre/train.txt` (186,1 Mo) — N2.j.
- **Recette identique** : 20 000 pas × 8 × 128, lr 3e-4, graine 1, **positions aléatoires [0, 384]**
  (N2.j2) pour les deux modèles.
- **Deux tailles** : 11,47 M (`d_model 224, expert_hidden 288`) et 21,65 M (`296 / 416`, ×1,89).
- **Évaluation** : val/test du wiki, littérature, anglais, wikitext2, courbe 129→512,
  décomposition ; plus la validation du dépôt.

## Ce qui est mesuré

| modèle | params | val wiki | littérature | anglais | wikitext2 | 512 octets | val du dépôt |
|---|---:|---:|---:|---:|---:|---:|---:|
| **11,47 M** | 11 814 792 | 4,3893 | 7,90 | 13,72 | 14,94 | 5,67 | 7,11 |
| **21,65 M** | 21 646 224 | **4,2013** | **7,46** | **13,55** | **14,52** | **5,03** | **6,88** |
| écart | ×1,89 | **−0,19** | **−0,44** | −0,17 | −0,41 | **−0,64** | −0,24 |

## Lecture

La capacité **paie** dès que le corpus suit : −4,3 % en domaine, −5,6 % en littérature, −5,6 % à
512 octets. Le contraste avec N2.h5 est net : sur 3,24 Mo, le même doublement ne donnait que
−0,06 (et rien hors domaine) ; sur 186 Mo, il donne −0,19 et un gain partout.

C'est une **interaction données × capacité** : un modèle plus gros a besoin de plus de texte pour
amortir ses paramètres. À 3,24 Mo, les 21,65 M mémorisaient ; à 186 Mo, ils apprennent. La
conséquence pratique : la taille du modèle doit se choisir **après** le corpus, pas avant — et le
prochain palier (40-50 M) ne se justifiera qu'avec quelques centaines de Mo de plus.

## Ce que ça change pour N2

- Le plan de travail garde « la capacité » comme action : elle est **faite sur le corpus réel**,
  et elle est positive.
- La recette de production peut passer à 21,65 M pour le corpus réel — le coût est de ×1,89 en
  paramètres pour −4 à −6 % de PPL.
- Reste la question de la **distillation** : le professeur 23,57 M et l'élève 21,65 M sont
  proches en taille ; c'est l'élève 11,47 M qui a le plus à gagner d'un professeur plus gros.

## Ce qui pourrait le rendre faux

- **Une seule graine, 11 % du corpus vu** : l'écart (−0,19) est au-dessus du bruit observé sur les
  petites bases (±0,005), mais l'intervalle n'est pas mesuré sur ce corpus.
- **Le budget est le même** (20 000 pas) : le modèle plus gros a peut-être besoin de plus de pas
  pour converger — le gain est donc un **minorant** de ce qu'il donnerait à convergence.
- **Les positions aléatoires** sont communes aux deux : le résultat vaut pour cette recette.
- **Le texte wiki est du wikitexte nettoyé**, même réserve que N2.j.

## Fichiers

- Points de contrôle : `work/n2j/base-wiki-pos.pt` (11,47 M), `base-wiki-cap.pt` (21,65 M).
- Mesures : `work/n2j/eval-pos.json`, `eval-cap.json`.
- Corpus et manifeste : [`corpus-wiki-propre.json`](corpus-wiki-propre.json).
