# N2.h4 — Les deux leviers ensemble : lire du français **et** 256 octets

> **Ligne de roadmap** : N2 · **Date** : 2026-11-01 · **Verdict** : le corpus mixte
> ([`n2-diversite`](rapport-n2-diversite.md)) et les positions aléatoires
> ([`n2-longueur`](rapport-n2-longueur.md)) **se composent** : le modèle combiné vaut **3,4679**
> en domaine, **4,10** sur la littérature jamais vue, et sa PPL à 256 octets est
> **3,49** contre **14,11** pour le modèle à positions fixes.

## La question

Deux leviers ont été mesurés séparément : la diversité du corpus répare la généralité (16,70 →
3,85 hors dépôt) pour +0,17 en domaine ; les positions aléatoires réparent la longueur (14,11 →
3,25 à 256 octets) pour +0,15 à 129. **Se composent-ils ?** Rien ne le garantit : les deux jouent
sur des mécanismes différents (distribution des données, embedding de position), mais ils
pourraient se nuire — un modèle plus général peut être moins précis sur le dépôt, et des positions
bruitées peuvent coûter en domaine.

## Le dispositif

Même recette que [`n2-diversite`](rapport-n2-diversite.md), auquel on ajoute le tirage des positions
de [`n2-longueur`](rapport-n2-longueur.md) : corpus **moitié dépôt, moitié littérature**, professeur
et base **mixtes** (déjà entraînés), 20 000 pas × 16 × 128, lr 1e-4 puis 3e-5, **o ~ U(0, 384)**
pour les positions, trois graines.

## Ce qui est mesuré

| bras | val | littérature | anglais | 129 | 256 | 512 |
|---|---:|---:|---:|---:|---:|---:|
| A — dépôt, positions fixes | 3,0904 | 16,70 | 57,58 | 3,13 | 14,11 | 32,41 |
| D — mixte, positions fixes | 3,2625 | 3,85 | 25,68 | 3,31 | 11,12 | 19,82 |
| R — dépôt, positions aléatoires | 3,2381 | 16,82 | 58,51 | 3,24 | 3,25 | 5,93 |
| **DR — mixte + positions aléatoires** | 3,4679 | 4,10 | 28,96 | 3,47 | 3,49 | 5,41 |

## Lecture

Les deux leviers se composent : DR vaut **3,4679** en domaine (A : 3,0904, D : 3,2625), **4,10** sur la littérature (A : 16,70, D : 3,85) et **3,49** à 256 octets (A : 14,11, R : 3,25). Le coût en domaine par rapport à A est de **0,378**, et la longueur ne se paie plus au-delà de 129.

## Ce que ça change

C'est le **candidat** pour la ligne R : un modèle qui lit du français (4,10 sur la
littérature, contre 16,70 pour A) **et** qui tient au-delà de 128 octets (3,49 à 256,
contre 14,11). Il paie les deux leviers en domaine (3,4679 contre 3,0904) : **les coûts
s'additionnent comme les gains**. R1 (« 1 000 octets ») n'a donc plus qu'un verrou — la fenêtre
d'attention locale — et la question devient un choix de schéma, pas une fatalité.

## Ce qui pourrait le rendre faux

- **Les deux changements ne sont pas isolés** : le corpus mixte change aussi le professeur et la
  base ; la comparaison avec A isole l'ensemble, pas chaque facteur (faits séparément dans les
  fiches 2 et 3).
- **Le tirage de positions est le même** (384) que dans `n2-longueur` : ni balayé ni optimisé.
- **Trois graines**, une seule architecture.

## Fichiers

- Code : [`tools/distiller_budget.py`](../tools/distiller_budget.py) (`--positions-aleatoires`) ·
  [`tools/eval_n2_propre.py`](../tools/eval_n2_propre.py).
- Points de contrôle : `work/n2h/DR-pos-g{1,2,3}.pt`.
