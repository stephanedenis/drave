# N2.8 — distillation longue : PPL 3,123, encore loin de 2,5

> **Objet.** Prolonger la distillation de `drave-n0` (11,47 M) depuis le checkpoint 3,295, avec le
> professeur français de 23,76 M et 20 000 pas supplémentaires.

## Dispositif

- Professeur : `/tmp/route-teacher`, **23,76 M**, PPL **2,355**.
- Student : `/tmp/drave-n0-distille.pt`, **11 469 192** paramètres.
- **20 000 pas**, lot 16, séquence 128, lr 1e-4, T=2, alpha 0,7, têtes précoces, VDC.
- **1 334 s** GPU.

## Résultats

| mesure | avant | après |
|---|---:|---:|
| PPL validation | **3,295** | **3,123** |
| gain | — | **−5,2 %** |
| précision principale | 62,35 % | **67,96 %** |
| tête 3 | 62,98 % | **68,01 %** |
| gap au professeur | +0,940 | **+0,768** |

## Lecture

- **20 000 pas** font gagner **0,172** de PPL : **3,123** contre **3,295**, soit **−5,2 %**.
- La **précision** progresse nettement : **67,96 %** contre 62,35 %.
- La **tête 3** est à **68,01 %**, au-dessus de la principale (**67,96 %**) : le réflexe tardif est
  aussi bon que la sortie complète.
- Le **gap** au professeur se réduit de **0,940** à **0,768**, mais la porte **< 2,5** reste
  **inatteinte**.

## Verdict

**N2.8 — progrès mesuré, porte non atteinte** : **3,123**. La capacité du student (11,47 M) et/ou le
budget d'entraînement restent limitants ; 20 000 pas de plus ne suffisent pas.

## Limites

- **Même corpus** ; pas de test externe.
- **20 000 pas** seulement ; la courbe peut continuer.
- **Un seul professeur**, français.
- **Pas de pertes locales par bloc** ; têtes précoces seulement.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-distillation-20k.json`](native-distillation-20k.json).
