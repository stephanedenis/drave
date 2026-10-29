# N2.35 — contexte 130 après 129 : PPL 2,715, négatif

> **Objet.** Dernier palier du curriculum : passer de 129 à **130**, depuis le meilleur **2,6998**.

## Résultat

| mesure | valeur |
|---|---:|
| PPL | **2,7149** |
| PPL de départ | **2,6998** |
| variation | **+0,56 %** |
| précision principale | **72,64 %** |

- 5 000 pas, lot 15, lr 5e-6, professeur 20k.
- **340,7 s** GPU.

## Lecture

- Le palier **130** dégrade : **2,7149** contre **2,6998**.
- Le meilleur reste **2,6998** (N2.33).
- Le curriculum **129** était un **point isolé**, pas le début d'une descente.
- La porte **2,5** reste à **0,20**.

## Verdict

**N2.35 — négatif** : 130, **2,7149**.

## Limites

- **5 000 pas** seulement.
- **Un seul lr**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-ctx130-2.json`](native-ctx130-2.json).
