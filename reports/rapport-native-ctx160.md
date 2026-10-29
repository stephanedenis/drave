# N2.30 — curriculum 160 : PPL 3,8, négatif

> **Objet.** Éviter le saut 128→256 de N2.27 en passant par **160**, depuis le meilleur **2,708**.

## Résultat

| mesure | valeur |
|---|---:|
| PPL à 4 750 pas | **3,804** |
| PPL de départ | **2,708** |
| variation | **+40 %** |
| état | **arrêté** |

- Le run est **arrêté** : la PPL monte fortement.
- Aucun JSON final.

## Lecture

- Même **160** est trop loin de la fenêtre d'entraînement **128**.
- Un curriculum sérieux demanderait **128 → 136 → 144 → 160**, avec plus de pas par palier.
- Le meilleur reste **2,708**.

## Verdict

**N2.30 — négatif** : seq 160, **3,804**, arrêté.

## Limites

- **Arrêté** à 4 750 pas.
- **Pas de curriculum progressif**.
- **Un seul lr**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- Journal : `/tmp/distille-ctx160.log`.
