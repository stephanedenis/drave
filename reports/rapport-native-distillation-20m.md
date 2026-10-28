# N2.5 — un student de 21,6 M distillé : 4,294, pire que 11,5 M

> **Objet.** Tester si le plateau de **3,295** vient de la **capacité** du student (11,47 M) ou de
> l'entraînement. On double presque la taille et on distille 5 000 pas.

## Dispositif

- Professeur byte-level : **23,76 M**, PPL **2,355**.
- Student : `drave-n0` **21 634 536** paramètres (`d=320`, 6 blocs, 8 têtes, experts 384).
- Initialisation **aléatoire** (pas de checkpoint 11 M compatible).
- **5 000 pas**, lot 8, séquence 128, lr 2e-4, température 2, alpha 0,7, têtes précoces.
- **327 s** GPU.

## Résultats

| mesure | valeur |
|---|---:|
| PPL student 11,47 M (N2.4) | **3,295** |
| **PPL student 21,63 M** | **4,294** |
| variation | **+30,3 %** |
| précision principale | **58,81 %** |
| têtes précoces | **36,82 / 47,85 / 57,81 %** |
| gap au professeur | **+1,939** |

## Lecture

- **Plus gros, moins bon** : 21,63 M à **4,294** contre 3,295 à 11,47 M.
- Ce n'est **pas** une preuve que la capacité ne sert à rien : le modèle de 21,6 M part de **zéro** et
  n'a que **5 000 pas** ; le 11,47 M part d'un checkpoint déjà entraîné.
- La **tête 1** s'effondre à **36,82 %** : le modèle n'a pas eu le temps d'apprendre les premières couches.
- La comparaison **taille** est donc **confondue** avec la comparaison **temps d'entraînement**.

## Verdict

**N2.5 — négatif et confondu** : le student plus gros est pire à budget de pas égal, mais il part de
zéro. Il faut **either** entraîner plus longtemps, **either** partir d'un checkpoint compatible, avant de
conclure sur la capacité.

## Limites

- **5 000 pas** ; le 21,6 M n'est pas convergé.
- **Initialisation aléatoire** contre checkpoint entraîné.
- Lot 8 au lieu de 16.
- Même corpus.

## Fichiers

- Code : [`tools/distiller_natif.py`](../tools/distiller_natif.py).
- JSON : [`native-distillation-20m.json`](native-distillation-20m.json).
