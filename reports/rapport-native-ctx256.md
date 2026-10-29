# N2.27 — contexte 256 : chute à 5,7

> **Objet.** Entraîner le student sur des séquences de **256** octets au lieu de 128, depuis le
> meilleur checkpoint **2,708**.

## Résultat

| mesure | valeur |
|---|---:|
| PPL à 12 750 pas | **5,675** |
| PPL de départ | **2,708** |
| variation | **+110 %** |
| état | **arrêté** |

- Le run est **arrêté** : la PPL explose.
- Aucun JSON final ; valeur lue dans le journal.

## Lecture

- Le modèle a été entraîné **128** ; le passer à **256** sans curriculum **casse** l'apprentissage.
- Le `max_pos` à 2 048 ne suffit pas : les **positions** et l'attention locale n'ont pas vu 256.
- Il faudrait un **curriculum 128 → 192 → 256**, pas un saut direct.
- Le meilleur reste **2,708**.

## Verdict

**N2.27 — négatif** : contexte 256, **5,675**, arrêté.

## Limites

- **Arrêté** à 12 750 pas.
- **Pas de curriculum**.
- **Un seul lr**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- Journal : `/tmp/distille-ctx256.log`.
