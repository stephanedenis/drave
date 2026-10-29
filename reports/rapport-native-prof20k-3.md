# N2.17 — 30 000 pas de plus : PPL 2,726

> **Objet.** Prolonger N2.16 (2,755) de 30 000 pas à lr 1e-5 pour approcher 2,5.

## Résultat

| mesure | N2.16 | N2.17 |
|---|---:|---:|
| PPL validation | **2,755** | **2,726** |
| gain | — | **−1,0 %** |
| précision principale | 71,90 % | **72,34 %** |
| tête 3 | 72,17 % | **72,31 %** |
| gap au professeur | +0,886 | **+0,857** |

- 30 000 pas, lot 16, lr 1e-5, professeur 20k (PPL 1,869).
- **1 967 s** GPU.

## Lecture

- Le gain est **−0,029** : **2,726**, meilleur résultat français.
- La précision monte à **72,34 %**, la tête 3 à **72,31 %**.
- Le **gap** au professeur est **+0,857** ; le student 11,47 M plafonne encore.
- La porte **2,5** reste **non atteinte**, mais l'écart est de **0,226**.

## Verdict

**N2.17 — progrès** : **2,726**. Le meilleur student français est à **0,226** de la porte.

## Limites

- **Même corpus**, même professeur.
- **30 000 pas** ; le gain est faible.
- **Pas de pertes locales**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-prof20k-3.json`](native-prof20k-3.json).
