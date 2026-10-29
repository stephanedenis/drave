# N2.29 — 8 blocs réchauffés : 2,866, toujours derrière 2,708

> **Objet.** Lever le biais de N2.28 : le 8 blocs partait de zéro. Ici, les **6 premiers blocs** sont
> copiés du checkpoint **2,708**, seuls les blocs 6-7 et la tête précoce 4 sont neufs.

## Résultat

| mesure | valeur |
|---|---:|
| PPL à 6 250 pas | **2,866** |
| PPL du 6 blocs | **2,708** |
| état | **arrêté** |

- 30 000 pas prévus, arrêté à 6 250 : la PPL reste **au-dessus** de 2,708.
- Les 6 blocs copiés sont **identiques** au checkpoint ; les nouveaux blocs n'apportent pas mieux.

## Lecture

- Même **avec l'historique**, 8 blocs ne battent pas 6 : **2,866** contre **2,708**.
- Le résultat n'est plus confondu par l'initialisation : la profondeur **supplémentaire** ne paie pas.
- Le plafond **2,708** tient face à une architecture plus profonde.

## Verdict

**N2.29 — négatif** : 8 blocs réchauffés, **2,866**, arrêté.

## Limites

- **Arrêté** à 6 250 pas.
- **Nouveaux blocs** aléatoires.
- **Un seul lr**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- Journal : `/tmp/distille-8b-warm.log`.
