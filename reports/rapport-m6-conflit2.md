# B26 — le conflit M6 reste à zéro

> **Objet.** A6 mesurait un sélecteur de tâche à **94,95 %** avec un conflit **0** et une commutation
> **0**. B26 en fait une **réplication indépendante** avec la même porte, pour vérifier que le
> résultat ne dépend pas d'une graine de composition.

## Résultats

| mesure | valeur |
|---|---:|
| exact | **94,95 %** (792 cas) |
| conflit | **0,00** |
| commutation | **0,00** |
| base (tout non) | 50 % |
| sensibilité / spécificité | non renseignées par la porte |

## Lecture

- La réplication **retrouve exactement** A6 : **94,95 %**, conflit **0**, commutation **0**.
- Le **conflit nul** n'est pas un artefact d'une graine : la porte sélectionne la bonne tâche sans
  être perturbée par l'autre canal.
- La **commutation nulle** signifie que changer de tâche ne coûte rien dans ce dispositif — ce qui
  est **suspect** pour un contrôle exécutif : la porte n'a probablement pas de **mémoire** de la
  tâche précédente.
- C'est un **sélecteur**, pas un **conflit** : les deux canaux sont indépendants et la réponse est
  une conjonction, pas une compétition.

## Verdict

**B26 confirme A6** : le conflit est **0**, mais ce n'est pas une preuve de contrôle exécutif — c'est
la conséquence d'un **aiguillage** sans compétition. Un vrai conflit demanderait une **réponse
motrice unique** et des essais **incongruents** où les deux canaux se disputent la même sortie.

## Limites

- **Même porte** qu'A6 ; ce n'est pas une implémentation indépendante.
- Pas de **réponse motrice** : la sortie est une acceptation, pas un choix entre deux actions.
- Pas de **mémoire** de la tâche précédente ; la commutation nulle le montre.
- Sensibilité/spécificité non renseignées.

## Fichiers

- Code : [`tools/cerveau/gating_conflit2.py`](../tools/cerveau/gating_conflit2.py).
- Test : [`tools/cerveau/tests/test_gating_conflit2.py`](../tools/cerveau/tests/test_gating_conflit2.py).
- JSON : [`m6-conflit2.json`](m6-conflit2.json).
