# N2.14 — distillation avec le professeur 20k : PPL 2,787

> **Objet.** Utiliser le professeur **1,869** (N2.15) pour faire passer le student 11,47 M sous **2,8**.

## Dispositif

- Professeur : `/tmp/route-teacher-20k`, **23,76 M**, PPL **1,869**.
- Student : `/tmp/drave-n0-prof10k-2.pt`, PPL **2,876**.
- **20 000 pas**, lot 16, lr 3e-5, T=2, alpha 0,7, VDC.
- **1 293 s** GPU.

## Résultats

| mesure | avant | après |
|---|---:|---:|
| PPL validation | **2,876** | **2,787** |
| gain | — | **−3,1 %** |
| précision principale | 70,00 % | **71,30 %** |
| tête 3 | 70,21 % | **71,53 %** |
| gap au professeur | +0,772 | **+0,918** |

## Lecture

- Le professeur **1,869** fait gagner **0,089** de PPL : **2,787**.
- La précision monte à **71,30 %**, la tête 3 à **71,53 %**.
- Le **gap** au professeur **augmente** encore (+0,918) : plus le professeur est fort, plus le student
  de 11,47 M paraît limité.
- La porte **2,5** reste **non atteinte**.

## Verdict

**N2.14 — progrès** : **2,787**. Le student se rapproche, mais la capacité 11,47 M et/ou la
distillation plafonnent.

## Limites

- **20 000 pas**.
- **Même corpus**.
- **Pas de pertes locales**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-prof20k.json`](native-prof20k.json).
