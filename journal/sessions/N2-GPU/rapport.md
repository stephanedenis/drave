# Session `N2-GPU` — la distillation native, sans trace DSH

> **Journaux :** [le 29/10](../../2026-10-29/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | aucun Id DSH — **job GPU** piloté hors session |
| Mandat | [`plan.md`](plan.md) |
| Rôle | N2 — professeur, distillation, curriculum de contexte |
| Début | 2026-10-29 |
| Clôture | 2026-10-30, passage à la session unique `0b69f616` |

## Ce qui a été fait

- **Les données** : **49 999 fenêtres**, quatre sources ; le corpus diversifié remplace le
  français seul (N2.6).
- **Le professeur** : Qwen/DeepSeek distillé à 30 k pas — PPL **1,734** (0,794 bit/octet).
- **L'élève** : `drave-n0`, 11,47 M, 6 blocs, octets ; **3,123** à 20 000 pas, puis
  **2,6998** au contexte **129** — le meilleur point, et le plateau à **2,708**.
- **Les négatifs** : contextes **130, 136, 160, 256** tous au-dessus ; **8 blocs** à
  **4,84** puis **2,866** (réchauffé depuis 2,708) ; un élève de **21,63 M** à **3,381** —
  la capacité ne paie pas sans les données ni le schéma.

## La mesure

`reports/rapport-native-ctx129.md` (N2.33, 2,6998), `reports/rapport-native-ctx129-2.md`
(N2.34, 2,712), `reports/rapport-native-8b-warm.md` (N2.29, 2,866),
`reports/rapport-native-21m-20k.md` (N2.9, 3,381) ; l'export du meilleur modèle et sa parité
native sont dans `reports/rapport-native-best-2.md` (commit `c8acf22e`).

## Le contrôle négatif

Les **cinq allongements de contexte** (129 → 130, 136, 160, 256) et les **deux variantes
8 blocs** échouent : le gain de 2,6998 n'est pas un effet de l'échelle ni du hasard de graine,
c'est le point d'un curriculum qui s'arrête. La porte **< 2,5** n'est **pas** atteinte.

## Ce qui pourrait le rendre faux

- **Un seul professeur** et une seule recette de distillation : un professeur plus fort peut
  déplacer le plafond.
- **La PPL de validation** ne dit pas la lecture : N4 mesure la consigne (0/40), pas N2.
- **Le contexte 129** est un optimum local étroit ; le plateau 2,708 est à un pas.

## Limites

- **La hiérarchie n'a pas été testée ici** : elle est le levier nommé par N2, pas un résultat.
- Le corpus reste à quatre sources ; le corpus scientifique humain (B1.5) est bloqué.
- Aucun test au-delà de 11,47 M qui reproduise le point 2,6998.

## Prochaine action

**N2 — la hiérarchie** (état de section, trois graines), porte **< 2,5** ; **N5 gelé** jusqu'au
verdict de R11 sur le contexte. Les GPU sont libres.

## Blocage

Aucun ; le job est clos, les résultats sont committés dans les fiches ci-dessus.
