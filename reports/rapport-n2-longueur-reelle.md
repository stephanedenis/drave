# N2.j2 — Positions aléatoires sur 186 Mo : le verrou de longueur tombe encore (÷2,4 à 512)

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : la base du corpus réel
> (186 Mo) entraînée avec des **positions tirées dans [0, 384]** passe de **9,28 à 4,49** à
> 256 octets et de **13,37 à 5,67** à 512, pour un coût en domaine de **+0,36** (4,0284 → 4,3893).
> Le verrou de position n'était donc pas une propriété du petit corpus : il est **architectural**,
> et la randomisation le lève à l'échelle.

## La question

N2.h3 avait montré, sur 3,24 Mo, que la **position absolue** verrouille la longueur : 14,11 à
256 octets, 3,25 avec des positions aléatoires. Le corpus réel (186 Mo de Wikipédia, N2.j) a la
même courbe — 9,28 à 256, 13,37 à 512 — mais il est 60 fois plus gros. La randomisation des
positions suffit-elle encore, ou le corpus plus diversifié apprend-il la position autrement ?

## Le dispositif

- **Corpus** : `data/wiki_fr/propre/train.txt` (186,1 Mo), val 10,3 Mo — N2.j.
- **Base** : 11,47 M, 20 000 pas × 8 × 128, lr 3e-4, graine 1 ; `--positions-aleatoires 384` :
  à chaque pas, le décalage de position est tiré dans **[0, 384]**, donc les positions 0 à 511
  sont vues pendant l'entraînement.
- **Référence** : la même base, mêmes données, positions fixes (`base-wiki.pt`, N2.j).
- **Évaluation** : courbe 129→512 (fenêtres chunk-aware), val/test, littérature, anglais,
  wikitext2, décomposition.

## Ce qui est mesuré

| | 129 | 192 | **256** | 384 | **512** | val | littérature | anglais |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **positions fixes** | 4,0685 | 7,0665 | **9,2772** | 11,8489 | **13,3744** | 4,0284 | 7,42 | 12,41 |
| **positions 0–384** | 4,3940 | 4,3709 | **4,4905** | 5,0508 | **5,6691** | 4,3893 | 7,90 | 13,72 |
| écart | +8 % | **−38 %** | **−52 %** | **−57 %** | **−58 %** | +9 % | +6 % | +11 % |

## Lecture

Le verrou tombe **exactement comme sur le petit corpus** : la PPL ne dépend plus de la longueur
(4,39 à 129, 4,49 à 256, 5,67 à 512) au lieu de doubler puis tripler. Le coût est le même qu'en
N2.h3 — un peu de précision en domaine (+0,36 ici, +0,15 là-bas) et un léger recul hors domaine
(+0,48 en littérature, +1,3 en anglais) — mais l'échange vaut la peine : à 512 octets, le modèle
avec positions est **2,4 fois meilleur**.

Ce que ça dit : la position absolue est un **défaut d'architecture**, pas une conséquence des
données. Un modèle entraîné sur un corpus 60 fois plus gros garde exactement le même verrou, et la
même randomisation le lève. C'est le second résultat qui se transporte (après le corpus réel
lui-même) — et il ne coûte qu'un paramètre d'entraînement.

## Ce que ça change pour N2

- Le **verrou 129→512** de la roadmap est levé **sur le corpus réel** : la recette de production
  peut inclure `--positions-aleatoires 384` sans changer l'architecture.
- Il reste à vérifier que le gain **survit à la distillation** (le professeur et l'élève doivent
  recevoir les mêmes positions) — c'est la prochaine étape.
- La capacité (21,65 M) reste à mesurer sur ce corpus : le plan de travail la garde en action
  suivante.

## Ce qui pourrait le rendre faux

- **Une seule graine, 11 % du corpus vu** (20 000 pas = 20,5 Mo sur 186) : le coût en domaine
  (+0,36) est peut-être du bruit d'entraînement.
- **La fenêtre d'attention locale reste 256** : au-delà, le modèle ne voit pas plus loin, même
  avec les positions — la courbe plate à 512 ne dit pas qu'il *utilise* 512 octets de contexte,
  seulement qu'il n'est plus puni par la position.
- **Le décalage est uniforme** [0, 384] : un décalage appris ou plus large dirait autre chose.
- **Le texte wiki est du wikitexte nettoyé** (titres de section collés), même réserve que N2.j.

## Fichiers

- Trainer : [`tools/entrainer_native.py`](../tools/entrainer_native.py) (`--positions-aleatoires`).
- Points de contrôle : `work/n2j/base-wiki.pt` (référence), `base-wiki-pos.pt`.
- Mesures : `work/n2j/eval-pos.json` ; corpus et manifeste : [`corpus-wiki-propre.json`](corpus-wiki-propre.json).
