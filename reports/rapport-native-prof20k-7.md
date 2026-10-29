# N2.24 — professeur 20k, température 4 : encore une dégradation

> **Objet.** Adoucir la cible (T=4, alpha 0,8) pour éviter le KL trop tranchant qui dégradait N2.21–N2.23.

## Résultat

| mesure | valeur |
|---|---:|
| PPL à 13 750 pas | **2,852** |
| PPL de départ | **2,708** |
| variation | **+5,3 %** |
| état | **arrêté** |

- Le run est **arrêté** : la PPL monte, même avec une température plus douce.
- Aucun JSON final ; valeur lue dans le journal.

## Lecture

- Adoucir la cible **ne sauve pas** l'entraînement : **2,852**.
- Les trois derniers essais (lr 3e-6, lr 1e-5, T=4) **dégradent** tous.
- Le student 11,47 M est **au plafond** de la recette distillation ; le meilleur point reste **2,708**.
- La porte **2,5** n'est **pas atteinte**.

## Verdict

**N2.24 — négatif** : T=4, **2,852**, arrêté. La distillation supplémentaire est **réfutée** à cette architecture.

## Limites

- **Arrêté** à 13 750 pas.
- **Un seul alpha/T**.
- **Pas de pertes locales**.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- Journal : `/tmp/distille-prof20k-7.log`.
