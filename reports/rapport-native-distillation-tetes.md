# N2.4 — têtes précoces dans la distillation : pas de gain de PPL

> **Objet.** Ajouter les trois têtes précoces à la distillation de `drave-n0`, sur 5 000 pas, pour
> voir si elles améliorent la PPL ou seulement le réflexe.

## Dispositif

- Professeur byte-level : **23,76 M**, PPL **2,355**.
- Student : `drave-n0`, **11 469 192** paramètres, initialisé depuis `/tmp/drave-n0-pont.pt`.
- **5 000 pas**, lot 16, séquence 128, lr 2e-4, température 2, alpha 0,7 ; **+0,1 × CE** sur chaque
  tête précoce.
- Durée : **343 s** GPU.

## Résultats

| mesure | valeur |
|---|---:|
| PPL après 2 000 pas (N2.3) | **3,297** |
| **PPL après 5 000 pas + têtes** | **3,295** |
| variation | **−0,002** |
| précision principale | **62,35 %** |
| têtes précoces | **54,96 / 60,99 / 62,98 %** |
| gap au professeur | **+0,940** |

## Lecture

- Les têtes précoces **n'améliorent pas** la PPL : **3,295** contre **3,297**, dans le bruit.
- La **tête 3** (après 6 blocs) atteint **62,98 %**, **au-dessus** de la tête principale à **62,35 %** :
  le réflexe tardif est **aussi bon** que la sortie complète sur ce corpus.
- 3 000 pas de plus n'ont **rien changé** : le plateau est là, pas dans le nombre de pas.
- Le **gap** au professeur reste **+0,940** : la capacité du student, pas l'entraînement, est la limite.

## Verdict

**N2.4 — négatif** : les têtes précoces n'ajoutent pas de PPL. Elles donnent un **réflexe** mesuré, pas
une meilleure langue. La porte N2 (**PPL < 2,5**) n'est pas atteinte.

## Limites

- **Même corpus** ; pas de test externe.
- Les têtes sont **entraînées** mais pas **utilisées** pour sortir tôt dans cette mesure.
- **5 000 pas** ; le plateau peut être local.
- Pas de pertes **locales par bloc** : seulement les têtes de sortie.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-distillation-tetes.json`](native-distillation-tetes.json).
