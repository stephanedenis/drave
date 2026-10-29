# N2.25 — lr 1e-6 : encore une dégradation

> **Objet.** Dernier essai de pas très petit pour éviter le plafond.

## Résultat

| mesure | valeur |
|---|---:|
| PPL à 12 500 pas | **2,758** |
| PPL de départ | **2,708** |
| variation | **+1,8 %** |
| état | **arrêté** |

- Le run est arrêté : la PPL monte, même à lr 1e-6.
- Aucun JSON final.

## Verdict

**N2.25 — négatif** : **2,758**. Le plafond de **2,708** est confirmé par quatre essais
supplémentaires (N2.21–N2.25).

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- Journal : `/tmp/distille-prof20k-8.log`.
