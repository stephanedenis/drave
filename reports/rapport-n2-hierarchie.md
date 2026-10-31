# N2 — l'état de section ne paie pas : le contrôle étranger fait aussi bien

> **Ligne de roadmap** : N2 (la hiérarchie) · **Date** : 2026-10-31 · **Verdict** : ❌ **négatif** —
> à budget égal, l'état de section transporté d'un segment au suivant n'améliore pas la PPL, et
> son effet est **indiscernable** de celui d'un état venu d'un autre document.

## La question

N2 plafonne à **2,6998** (porte **< 2,5** non atteinte) : le contexte s'arrête à 129 octets parce
que les allongements 130, 136, 160 et 256 échouent. Le levier retenu par la roadmap était la
**hiérarchie** — un **état de section** qui résume les octets déjà lus et se transporte d'un
segment à l'autre, pour donner au modèle une portée plus longue que sa fenêtre locale.

La question de cette fiche n'est pas « le modèle peut-il porter un état ? » (oui, il s'entraîne),
mais « **cet état apporte-t-il de l'information utile ?** ».

## Le dispositif

| | |
|---|---|
| corpus | `data/corpus_fr.txt`, 4 633 889 octets ; validation = 5 % de queue |
| budget | **2 500 pas × 8 × 4 × 128 = 10,24 Mo vus** (≈ 2,3 époques) |
| modèle | `NativeModel`, **11,81 M** (témoin) · **12,17 M** (bras à état) |
| état | `GRUCell(224)` sur la moyenne des activations du segment, injecté **avant les blocs** |
| BPTT | **tronquée à 1 segment** (état détaché) |
| optimisation | AdamW, lr 3e-4, wd 0,01, gradient clipping 1,0 |
| graines | **1 et 2**, mêmes fenêtres (Van der Corput) |
| banc | [`tools/entrainer_section.py`](../tools/entrainer_section.py) · données [`n2-hierarchie.json`](n2-hierarchie.json) |

Trois bras, **mêmes octets, mêmes fenêtres, même budget** :

- **témoin** — `NativeModel` nu, les quatre segments sont indépendants ;
- **hiérarchie** — l'état du segment précédent est transporté et injecté ;
- **contrôle** — même architecture, même nombre de paramètres, mais l'état injecté est celui
  d'un **autre document** du lot (roulé sur la dimension du lot).

## Ce qui est mesuré

PPL de validation (plus bas = mieux), à 2 500 pas :

| bras | graine 1 | graine 2 | moyenne | étendue |
|---|---:|---:|---:|---:|
| **témoin** | 3,9546 | 3,9688 | **3,9617** | 0,0142 |
| **hiérarchie** | 3,9619 | 3,9899 | **3,9759** | 0,0281 |
| **contrôle** | 3,9330 | 4,0198 | **3,9764** | 0,0868 |

- **hiérarchie − témoin = +0,36 %** ; **contrôle − témoin = +0,37 %** ;
- **hiérarchie − contrôle = −0,0005** — les deux bras à état sont **confondus** ;
- la précision top-1 suit : **0,6049** (témoin) contre 0,6042 / 0,6030 (hiérarchie).

## Le contrôle négatif, et ce qu'il dit

C'est le point décisif. Si l'état apportait de l'information, le bras **hiérarchie** devait battre
le **contrôle**, qui porte la même machinerie mais un état **étranger**. Il ne le bat pas :
l'écart entre les deux est de **0,0005 PPL**, soit **trente fois plus petit** que l'étendue du
contrôle (0,0868) et **trente fois plus petit** que la dispersion entre graines du témoin.

Conclusion : la petite dégradation (+0,36 %) vient des **paramètres supplémentaires et de la
troncature du gradient**, pas de l'information transportée. L'état de section, tel qu'implémenté,
**ne lit rien d'utile**.

## Ce qui pourrait le rendre faux

- **Le budget est court** : 2,3 époques sur 4,4 Mo, avec 11,8 M de paramètres — le modèle est
  probablement en régime de sur-apprentissage, où un état de section n'a pas le temps de payer.
  Un budget long (le dispositif de distillation N2 : 49 999 fenêtres, professeur 30 k) pourrait
  changer le signe.
- **La BPTT est tronquée à un segment** : l'état ne reçoit aucun gradient du segment suivant. Une
  BPTT à deux segments est le premier réglage à essayer avant de conclure au-delà de ce budget.
- **Une seule forme d'état** : moyenne des activations + GRU. Une mémoire par attention, ou une
  injection par bloc plutôt qu'avant les blocs, n'est pas testée.
- **Les PPL ne sont pas comparables à 2,6998** : corpus, professeur et curriculum diffèrent. Cette
  fiche ne dit rien de la porte < 2,5 — elle dit que ce levier-là, à ce budget, ne la rapproche pas.

## Ce que ça change pour N2

Le levier « état de section » n'est **pas validé**. Avant de l'abandonner, la prochaine mesure est
la même ablation sur le **dispositif de distillation** (corpus 4 sources, professeur 30 k, budget
20 000 pas) et avec une **BPTT à deux segments** : si l'écart hiérarchie − contrôle reste nul là
aussi, le levier est mort et N2 doit chercher ailleurs (curriculum, données, capacité).
