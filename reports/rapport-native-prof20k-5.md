# N2.19 — 30 000 pas de plus : PPL 2,708

> **Objet.** Prolonger N2.18 (2,714) de 30 000 pas à lr 5e-6.

## Résultat

| mesure | N2.18 | N2.19 |
|---|---:|---:|
| PPL validation | **2,714** | **2,708** |
| gain | — | **−0,006** |
| précision principale | 72,62 % | **72,80 %** |
| tête 3 | 72,69 % | **72,60 %** |
| gap au professeur | +0,845 | **+0,839** |

- 30 000 pas, lot 16, lr 5e-6, professeur 20k (PPL 1,869).
- **1 945 s** GPU.

## Lecture

- Le gain est **−0,006** : **2,708**, meilleur français.
- La précision monte à **72,80 %** ; la tête 3 recule légèrement à **72,60 %**.
- Le **gap** au professeur est **+0,839**.
- La porte **2,5** reste à **0,208**.

## Verdict

**N2.19 — gain marginal** : **2,708**. Le student est à **0,208** de la cible ; la courbe s'aplatit.

## Limites

- **Même corpus**, même professeur.
- **30 000 pas** ; gain presque nul.
- **Pas de pertes locales**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-prof20k-5.json`](native-prof20k-5.json).
