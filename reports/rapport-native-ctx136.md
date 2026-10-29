# N2.31 — contexte 136 : PPL 2,974, négatif

> **Objet.** Palier le plus proche de 128 : **136** au lieu de 160, depuis le meilleur **2,708**.

## Résultat

| mesure | valeur |
|---|---:|
| PPL à 4 250 pas | **2,974** |
| PPL de départ | **2,708** |
| variation | **+9,8 %** |
| état | **arrêté** |

- Même **136** dégrade : **2,974**.
- Aucun JSON final.

## Lecture

- Le student a une fenêtre **128** ; tout décalage, même de 8 positions, **coûte**.
- Les trois contextes testés (136, 160, 256) **échouent**.
- Un curriculum demanderait des paliers de **1 ou 2** positions et beaucoup plus de pas.
- Le meilleur reste **2,708**.

## Verdict

**N2.31 — négatif** : 136, **2,974**, arrêté.

## Limites

- **Arrêté** à 4 250 pas.
- **Pas de curriculum fin**.
- **Un seul lr**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- Journal : `/tmp/distille-ctx136.log`.
