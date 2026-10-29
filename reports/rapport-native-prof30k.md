# N2.21 — professeur 30k, lr 3e-6 : dégradation, arrêté

> **Objet.** Distiller depuis le professeur **1,734** (N2.20) en partant du student **2,708**, à
> lr 3e-6.

## Résultat

| mesure | valeur |
|---|---:|
| PPL à 13 000 pas | **2,823** |
| PPL de départ | **2,708** |
| variation | **+4,2 %** |
| état | **arrêté** |

- Le run a été **arrêté** après 13 000 pas : la PPL **montait** au lieu de descendre.
- Aucun JSON final ; la valeur est lue dans le journal.

## Lecture

- Un professeur **plus fort** ne suffit pas : à lr 3e-6, le student **se dégrade** de **2,708** à
  **2,823**.
- L'hypothèse la plus simple : le signal KL du professeur 30k est **trop tranchant** pour ce student,
  ou le pas est trop faible pour suivre.
- Le meilleur student reste **2,708** (N2.19).

## Verdict

**N2.21 — négatif** : professeur 30k à lr 3e-6 **dégrade** le student. La piste « professeur plus
fort » ne suffit pas.

## Limites

- **Arrêté** à 13 000 pas, pas de résultat final.
- **Un seul lr**.
- **Pas de température/alpha ajustés**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- Journal : `/tmp/distille-prof30k.log`.
