# N2.12 — distillation avec le professeur 10k : PPL 2,910

> **Objet.** Utiliser le professeur **2,104** (N2.10) au lieu de **2,355** (N2.2) pour faire descendre
> le student 11,47 M sous 3,0.

## Dispositif

- Professeur : `/tmp/route-teacher-10k`, **23,76 M**, PPL **2,104**.
- Student : `/tmp/drave-n0-distille-50k.pt`, PPL **3,082**.
- **20 000 pas**, lot 16, lr 5e-5, T=2, alpha 0,7, VDC.
- **1 334 s** GPU.

## Résultats

| mesure | avant | après |
|---|---:|---:|
| PPL validation | **3,082** | **2,910** |
| gain | — | **−5,6 %** |
| précision principale | 68,21 % | **69,59 %** |
| tête 3 | 68,70 % | **69,97 %** |
| gap au professeur | +0,727 | **+0,806** |

## Lecture

- Le professeur plus fort fait **descendre** le student sous **3,0** : **2,910**.
- La précision monte à **69,59 %**, la tête 3 à **69,97 %**.
- Le **gap** au professeur **augmente** (+0,806) : le professeur progresse plus vite que le student.
- La porte **2,5** reste **non atteinte**, mais on s'en rapproche : **2,910**.

## Verdict

**N2.12 — progrès** : **2,910** contre **3,082** (−5,6 %). Le professeur 10k est meilleur ; le
student de 11,47 M plafonne encore.

## Limites

- **20 000 pas** ; la courbe peut continuer.
- **Même corpus**.
- **Un seul professeur**.
- **Pas de pertes locales par bloc**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-prof10k.json`](native-prof10k.json).
