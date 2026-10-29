# N2.11 — distillation 50 000 pas : PPL 3,082, plateau

> **Objet.** Prolonger la distillation du student 11,47 M de 20 000 à **50 000 pas** pour voir si
> la PPL descend vers 2,5.

## Dispositif

- Professeur : `/tmp/route-teacher` (5 000 pas, PPL 2,355).
- Student : `/tmp/drave-n0-distille-20k.pt` (PPL 3,123).
- **30 000 pas de plus**, lot 16, lr 5e-5, T=2, alpha 0,7, VDC.
- **1 985 s** GPU.

## Résultats

| mesure | 20 000 pas | 50 000 pas |
|---|---:|---:|
| PPL validation | **3,123** | **3,082** |
| gain | — | **−0,041** |
| précision principale | 67,96 % | **68,21 %** |
| tête 3 | 68,01 % | **68,70 %** |
| gap au professeur | +0,768 | **+0,727** |

## Lecture

- **30 000 pas** de plus ne donnent que **−0,041** de PPL : le student est sur un **plateau** à
  **3,08**.
- La précision progresse à peine : **68,21 %**.
- La **tête 3** est à **68,70 %**, au-dessus de la principale.
- Le **gap** au professeur reste **+0,727** : le student 11,47 M ne rattrape pas 23,76 M.

## Verdict

**N2.11 — plateau** : **3,082**, pas **2,5**. Le budget seul ne suffit plus ; il faut un professeur
plus fort (N2.10) ou une architecture plus adaptée.

## Limites

- **Même corpus**.
- **Un seul professeur**.
- **30 000 pas** ; la courbe est plate, pas nécessairement nulle.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-distillation-50k.json`](native-distillation-50k.json).
