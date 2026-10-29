# N2.16 — 20 000 pas de plus : PPL 2,755, plateau

> **Objet.** Prolonger N2.14 de 20 000 pas à lr 2e-5 pour approcher 2,5.

## Résultat

| mesure | N2.14 | N2.16 |
|---|---:|---:|
| PPL validation | **2,787** | **2,755** |
| gain | — | **−1,2 %** |
| précision principale | 71,30 % | **71,90 %** |
| tête 3 | 71,53 % | **72,17 %** |
| gap au professeur | +0,918 | **+0,886** |

- 20 000 pas, lot 16, lr 2e-5, professeur 20k (PPL 1,869).
- **1 326 s** GPU.

## Lecture

- Le gain tombe à **−0,032** : **2,755**.
- La précision monte à **71,90 %**, la tête 3 à **72,17 %**.
- Le **gap** au professeur reste **+0,886** : le student 11,47 M plafonne.
- La porte **2,5** reste **non atteinte** ; **2,755** est le meilleur résultat français.

## Verdict

**N2.16 — plateau** : **2,755**. Le budget et le professeur ne suffisent plus ; la capacité ou
l'architecture du student est la limite.

## Limites

- **Même corpus**, même professeur.
- **20 000 pas** ; la courbe est presque plate.
- **Un seul student**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-prof20k-2.json`](native-prof20k-2.json).
