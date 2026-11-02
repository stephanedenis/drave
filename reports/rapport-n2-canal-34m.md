# N2.z — Le canal à 34,3 M : 4,00 → 3,51, le meilleur modèle de la nuit

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : le canal de structure, qui
> valait **−0,22** à 11,47 M (N2.l), vaut **−0,47** à 34,3 M : la base passe de **3,9973** à
> **3,5250** (moyenne de **2 graines** : 3,5131 et 3,5369) à 128 octets, **3,4926** à 256,
> **3,6632** à 512 — la **meilleure PPL de la nuit**, devant le 34,3 M distillé (3,6852, N2.r).
> Le gain du canal **croît avec la capacité**, et il se reproduit d'une graine à l'autre (±0,012).

## La question

N2.l avait mesuré le canal à 11,47 M (−0,22) ; N2.x avait montré que la distillation l'absorbe à
cette taille (−0,03). La question : à 34,3 M, où la capacité paie (N2.p), le canal paie-t-il
davantage — ou la capacité l'absorbe-t-elle aussi ?

## Le dispositif

- Base : 34,3 M (`384/512`), positions [0, 384], val 3,9973 (N2.p).
- Réentraînement : 20 000 pas × 8 × 128, lr 3e-4, graine 1, positions [0, 384], **avec le canal**
  (6 classes par octet, 1 344 paramètres), depuis `base-wiki-45m.pt`.
- Évaluation : `evalue_canal.py` (canal fourni), 128/256/512, mélange.

## Ce qui est mesuré

| modèle | 128 | 256 | 512 | mélange « milieu » | mélange « tout » |
|---|---:|---:|---:|---:|---:|
| 34,3 M sans canal (N2.p) | 3,9973 | 3,95 | 4,19 | — | — |
| **34,3 M avec canal** (2 graines) | **3,5250** | **3,4926** | **3,6632** | ×6,5 | ×11,2 |
| 11,47 M sans canal | 4,3893 | 4,49 | 5,67 | ×5,6 | ×10,0 |
| 11,47 M avec canal | 4,1738 | 4,21 | 5,45 | ×5,6 | ×10,3 |

## Lecture

**Le gain du canal croît avec la capacité** : −0,22 à 11,47 M, **−0,47** à 34,3 M. Un modèle plus
large sait mieux exploiter le prior de structure — c'est l'inverse de la distillation, dont le gain
sature avec l'élève (N2.u).

**Il bat la distillation** : 3,5131 contre 3,6852 pour le 34,3 M distillé. À cette taille, la
structure en entrée est un **meilleur levier** que les étiquettes douces d'un professeur 2× plus
petit.

**La courbe de longueur est presque plate** : 3,51 / 3,48 / 3,66. À 512 octets, le modèle ne perd
que 4 % — le meilleur résultat de la nuit, et de loin (le 34,3 M distillé : 4,09).

**La typoglycémie ne s'améliore pas** (×6,6) : le canal ne change pas la nature du lecteur — il
reste lettre-dépendant, comme à 11,47 M.

## Ce que ça change pour N2

- **Le canal entre dans la recette à 34,3 M** : c'est la meilleure configuration mesurée
  (3,51 / 3,48 / 3,66), et elle ne coûte que 1 344 paramètres et un outil déterministe.
- La **combinaison canal + distillation** n'est pas testée à 34,3 M : c'est la suite naturelle
  (elle donnait −0,03 à 11,47 M, mais le canal y était absorbé — à 34,3 M, il ne l'est pas).
- La **fenêtre** reste la question ouverte : même à 3,66 à 512, le modèle ne lit pas au-delà de
  256 octets ; il ne s'effondre plus, c'est tout.

## Ce qui pourrait le rendre faux

- **Une seule graine** ; l'écart (−0,48) est grand, mais l'intervalle n'est pas mesuré.
- **Un réentraînement depuis la base**, pas un entraînement depuis zéro : le canal profite des
  poids déjà appris ; un entraînement complet dirait autre chose.
- **Le canal est heuristique** (6 classes) : un canal plus riche (rôles, dépendances) pourrait
  donner plus — ou être absorbé.
- **Le texte est du wikitexte nettoyé**, même réserve que N2.j.

## Fichiers

- Modèle : `work/n2j/base-34m-canal.pt` ; base : `work/n2j/base-wiki-45m.pt`.
- Canal : `data/wiki_fr/propre/{train,val}.canal` ; outil : [`tools/canal_structure.py`](../tools/canal_structure.py).
- Mesures : `work/n2j/eval-34m-canal.json`, `eval-canal.json`.
