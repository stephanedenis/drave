# N2.p — La capacité à 34,3 M : −0,19 par palier, et le verrou de longueur s'efface

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : sur les 186 Mo du corpus réel,
> la base passe de **4,3893** (11,47 M) à **4,2013** (21,65 M) puis **3,9973** (34,3 M) — **−0,19
> par palier** —, et la courbe de longueur s'aplatit : **4,1935** à 512 octets contre 5,0259 et
> 5,6691. La capacité ne paie pas seulement en domaine : elle paie aussi en **longueur**.

## La question

N2.h5 avait mesuré la capacité sur 3,24 Mo (−0,06, rien hors domaine) ; N2.j3 sur 186 Mo (−0,19
pour 21,65 M). La question : la loi continue-t-elle à 34,3 M, et sur quoi porte le gain ?

## Le dispositif

- Corpus : `data/wiki_fr/propre/train.txt` (186,1 Mo, N2.j).
- Recette : 20 000 pas × 8 × 128, lr 3e-4, graine 1, positions aléatoires [0, 384].
- Trois tailles : **11,47 M** (`224/288`), **21,65 M** (`296/416`), **34,30 M** (`384/512`).
- Évaluation : val/test, littérature, anglais, wikitext2, courbe 129→512, décomposition.

## Ce qui est mesuré

| modèle | params | val | littérature | anglais | wikitext2 | 512 | 384 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **11,47 M** | 11 814 792 | 4,3893 | 7,90 | 13,72 | 14,94 | 5,67 | 5,05 |
| **21,65 M** | 21 646 224 | 4,2013 | 7,46 | 13,55 | 14,52 | 5,03 | 4,66 |
| **34,30 M** | 34 301 224 | **3,9973** | **7,38** | **11,98** | **13,42** | **4,19** | **4,08** |
| écart 11 → 34 | ×2,9 | **−0,39** | −0,52 | −1,74 | −1,52 | **−1,48** | −0,97 |

Courbe complète du 34,3 M : **4,02 / 3,91 / 3,95 / 4,08 / 4,19** à 129/192/256/384/512.

## Lecture

La loi est **log-linéaire** : chaque palier (~×1,7 de paramètres) vaut **−0,19** en domaine. Rien
dans ces trois points ne suggère un rendement décroissant — mais 20 000 pas pour tous, et le plus
gros modèle est le moins convergé : le gain est un **minorant**.

Le résultat le plus net est **hors domaine et en longueur** : l'anglais passe de 13,72 à 11,98
(−1,74) et la PPL à 512 octets de 5,67 à **4,19** (−1,48, soit −26 %). Le verrou de longueur, qui
semblait architectural (N2.j2), est donc aussi **une affaire de capacité** : un modèle plus large
utilise mieux la fenêtre locale de 256 octets et ne s'effondre plus au-delà.

## Ce que ça change pour N2

- La recette de production peut monter à **34,3 M** pour le corpus réel : −0,39 en domaine, −1,5
  hors domaine et à 512 octets, pour ×2,9 de paramètres.
- La question de la **fenêtre** (R1) change de nature : une partie du « verrou » se règle par la
  capacité ; il reste à voir si un modèle encore plus large aplatit complètement la courbe.
- La **distillation** n'a pas été refaite pour ce modèle : le prochain élève devrait être un 34,3 M
  (ou le professeur un 34,3 M distillé dans un 11,47 M).

## Ce qui pourrait le rendre faux

- **Une seule graine** par taille ; l'écart de −0,19 est net mais l'intervalle n'est pas mesuré à
  cette échelle.
- **20 000 pas pour tous** : le 34,3 M est le moins convergé ; à convergence l'écart serait plus
  grand (le gain est un minorant).
- **Même corpus, même tokenizer d'octets** : la loi vaut pour cette architecture (FFN creux,
  attention locale 256, boucle de pensée).
- **Le texte wiki est du wikitexte nettoyé**, même réserve que N2.j.

## Fichiers

- Points de contrôle : `work/n2j/base-wiki-pos.pt` (11,47 M), `base-wiki-cap.pt` (21,65 M),
  `base-wiki-45m.pt` (34,3 M).
- Mesures : `work/n2j/eval-pos.json`, `eval-cap.json`, `eval-45m.json`.
