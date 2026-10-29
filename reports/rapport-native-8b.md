# N2.28 — 8 blocs : PPL 4,84, négatif

> **Objet.** Tester une architecture plus **profonde** (8 blocs, `d=208`, 13 M) au lieu de 6 blocs,
> avec le même professeur et 30 000 pas.

## Résultat

| mesure | valeur |
|---|---:|
| PPL à 9 750 pas | **4,838** |
| PPL du 6 blocs 2,708 | **2,708** |
| état | **arrêté** |

- Initialisation **aléatoire** ; le 8 blocs n'a pas l'historique du 6 blocs.
- Le run est **arrêté** : la PPL reste à **4,84**, très loin de **2,708**.

## Lecture

- **Plus profond, moins bon** à budget égal : **4,84** contre **2,708**.
- Le résultat est **confondu** : le 8 blocs part de zéro, le 6 blocs d'un checkpoint.
- Il confirme cependant que **la profondeur seule** ne suffit pas à ce budget.
- Le meilleur reste **2,708**.

## Verdict

**N2.28 — négatif et confondu** : 8 blocs, **4,838**, arrêté.

## Limites

- **Initialisation aléatoire** contre checkpoint.
- **30 000 pas** seulement.
- **Un seul lr**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- Journal : `/tmp/distille-8b.log`.
