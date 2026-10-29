# N2.13 — 20 000 pas de plus avec le professeur 10k : PPL 2,876

> **Objet.** Prolonger N2.12 de 20 000 pas à lr 3e-5 pour voir si la PPL continue de descendre vers
> 2,5.

## Dispositif

- Professeur : `/tmp/route-teacher-10k`, PPL **2,104**.
- Student : `/tmp/drave-n0-prof10k.pt`, PPL **2,910**.
- **20 000 pas**, lot 16, lr 3e-5, T=2, alpha 0,7, VDC.
- **1 334 s** GPU.

## Résultats

| mesure | N2.12 | N2.13 |
|---|---:|---:|
| PPL validation | **2,910** | **2,876** |
| gain | — | **−1,2 %** |
| précision principale | 69,59 % | **70,00 %** |
| tête 3 | 69,97 % | **70,21 %** |
| gap au professeur | +0,806 | **+0,772** |

## Lecture

- **20 000 pas** de plus ne donnent que **−0,034** : **2,876**.
- La précision passe à **70,00 %**, la tête 3 à **70,21 %**.
- Le gain est **faible** : le student approche de son plateau, pas de la porte **2,5**.
- Le **gap** au professeur se réduit à **+0,772**.

## Verdict

**N2.13 — gain marginal** : **2,876**. La porte **< 2,5** reste hors de portée avec ce student.

## Limites

- **Même corpus**, même professeur.
- **20 000 pas** ; la courbe est presque plate.
- **Pas de pertes locales**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-prof10k-2.json`](native-prof10k-2.json).
