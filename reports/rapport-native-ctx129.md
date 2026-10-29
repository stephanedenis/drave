# N2.33 — contexte 129 : PPL 2,700, nouveau meilleur

> **Objet.** Curriculum au pas de **1** : passer de 128 à **129**, depuis le meilleur **2,708**.

## Résultat

| mesure | N2.19 (128) | N2.33 (129) |
|---|---:|---:|
| PPL validation | **2,708** | **2,6998** |
| gain | — | **−0,008** |
| précision principale | 72,80 % | **72,40 %** |
| tête 3 | 72,60 % | **72,53 %** |
| durée | 1 945 s | **1 468 s** |

- 10 000 pas, lot 15, lr 5e-6, professeur 20k.
- **Nouveau meilleur français** : **2,6998**.

## Lecture

- Le **pas de 1** fonctionne là où 130, 136, 160 et 256 échouaient.
- Le gain est **faible** (−0,008) mais le sens est **inversé** : pour la première fois, un
  entraînement supplémentaire **améliore** le meilleur.
- La précision principale **baisse** légèrement (72,40 contre 72,80) : la PPL et le top-1 ne bougent
  pas ensemble.
- La porte **2,5** reste à **0,20**.

## Verdict

**N2.33 — nouveau meilleur** : **2,6998**. Le curriculum fin est la première piste qui **améliore**
depuis N2.19.

## Limites

- **10 000 pas** seulement.
- **Une seule position** de plus ; faut-il continuer 130, 131… ?
- **Même corpus**.
- **Précision principale en baisse**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-ctx129.json`](native-ctx129.json).
