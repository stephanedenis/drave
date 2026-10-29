# N2.26 — têtes locales : encore une dégradation

> **Objet.** Ajouter une sortie après **chaque bloc** (supervision profonde, 6 têtes locales) et
> repartir du meilleur student **2,708**.

## Dispositif

- Têtes locales : une par bloc, poids 0,05 dans la perte.
- Student : `/tmp/drave-n0-prof20k-5.pt`, PPL **2,708**.
- **20 000 pas**, lot 16, lr 5e-6, professeur 20k (1,869).
- Chargement `strict=False` : les têtes locales sont neuves.

## Résultat

| mesure | valeur |
|---|---:|
| PPL à 13 000 pas | **2,763** |
| PPL de départ | **2,708** |
| variation | **+2,0 %** |
| état | **arrêté** |

## Lecture

- La supervision profonde **ne sauve pas** le plafond : **2,763**.
- Les têtes locales ajoutent du gradient mais **ne changent pas** la limite de la recette.
- Sept essais supplémentaires (N2.21–N2.26) **dégradent** tous.
- Le meilleur reste **2,708**.

## Verdict

**N2.26 — négatif** : têtes locales, **2,763**, arrêté. Le plafond **2,708** tient.

## Limites

- **Arrêté** à 13 000 pas.
- **Poids 0,05** non balayé.
- **Têtes locales** non utilisées à l'inférence.

## Fichiers

- Code : [`tools/native_model.py`](../tools/native_model.py), [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- Journal : `/tmp/distille-local.log`.
