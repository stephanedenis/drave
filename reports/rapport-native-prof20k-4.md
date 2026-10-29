# N2.18 — 30 000 pas de plus : PPL 2,714

> **Objet.** Prolonger N2.17 (2,726) de 30 000 pas à lr 8e-6.

## Résultat

| mesure | N2.17 | N2.18 |
|---|---:|---:|
| PPL validation | **2,726** | **2,714** |
| gain | — | **−0,012** |
| précision principale | 72,34 % | **72,62 %** |
| tête 3 | 72,31 % | **72,69 %** |
| gap au professeur | +0,857 | **+0,845** |

- 30 000 pas, lot 16, lr 8e-6, professeur 20k (PPL 1,869).
- **1 995 s** GPU.

## Lecture

- Le gain est **−0,012** : **2,714**, meilleur résultat français.
- La précision monte à **72,62 %**, la tête 3 à **72,69 %**.
- Le **gap** au professeur est **+0,845**.
- La porte **2,5** reste à **0,214**.

## Verdict

**N2.18 — progrès marginal** : **2,714**. Le student 11,47 M est proche de son plafond ; il reste
**0,214** au-dessus de la cible.

## Limites

- **Même corpus**, même professeur.
- **30 000 pas** ; gain faible.
- **Pas de pertes locales**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-prof20k-4.json`](native-prof20k-4.json).
