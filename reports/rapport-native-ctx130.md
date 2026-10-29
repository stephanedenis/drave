# N2.32 — contexte 130 : PPL 2,78, encore au-dessus

> **Objet.** Palier **130**, le plus proche testé de 128.

## Résultat

| mesure | valeur |
|---|---:|
| PPL à 2 250 pas | **2,786** |
| PPL de départ | **2,708** |
| variation | **+2,9 %** |
| état | **arrêté** |

- Même **+2 positions** dégradent : **2,786**.
- Aucun JSON final.

## Lecture

- Le student 128 est **très** sensible à la longueur ; le curriculum devrait commencer à **129**.
- Les quatre contextes testés (130, 136, 160, 256) **échouent**.
- Le meilleur reste **2,708**.

## Verdict

**N2.32 — négatif** : 130, **2,786**, arrêté.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- Journal : `/tmp/distille-ctx130.log`.
