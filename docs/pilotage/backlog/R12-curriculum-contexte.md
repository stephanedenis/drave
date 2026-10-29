# R12 — Curriculum de contexte long (129 → 1 000 octets)

> **Statut** : spécifiée · **Priorité** : P1 · **Programme** : R · **Dépend de** : R11 · **Contraint par** : les cinq négatifs 129–256
> **Ligne de roadmap** : R1.2 · **Fiche de résultat attendue** : rapport-r12-curriculum-contexte.md (à créer dans `reports/`)
> **Résumé** : Trouver une recette d'allongement du contexte qui ne refait pas les négatifs 130/136/160/256.

## Le besoin

Les essais 130, 136, 160 et 256 sont tous négatifs ; le point 129 est isolé. Allonger le contexte demande un autre schéma (états de résumé, données, curriculum), pas un pas de plus.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | un plan d'entraînement (longueurs, données, état, pas) et un jeu d'évaluation |
| **sortie** | une courbe de PPL et d'aiguille de 129 à 1 000+ octets |
| **coût** | même budget de calcul que les essais négatifs, pour comparer |
| **trace** | chaque essai est tracé (longueur, données, graine, pas) |

## Ce qui est mesuré

- PPL par longueur (129, 256, 512, 1 000, 2 000)
- aiguille native par longueur
- stabilité entre graines et entre étapes

## Portes

1. 1 000 octets stable, pas un point isolé
2. la courbe ne remonte pas entre 129 et 1 000
3. le coût par octet reste comparable

## Contrôles négatifs

- même calcul à 129 ; longueur aléatoire ; sans curriculum
- évaluation sur une longueur non vue

## Ce qui pourrait le rendre faux

- une seule graine ; la PPL moyenne cache la chute sur les longues sections
- les données de test ont la même longueur que l'entraînement
- le curriculum change aussi les données, pas seulement la longueur

## Étapes

1. rejouer les négatifs 130/136/160/256 dans un même tableau
2. tester les états de résumé et les données longues
3. mesurer la courbe et la stabilité ; écrire la fiche

## Documents à écrire

- `curriculum-contexte.md` (plan, courbes, portes, dans `docs/implantation/`)
- mettre à jour R1.2

## Voir aussi

- [Programme R](../roadmap.md#r1--la-fenêtre-native)
- [N, leçon 1](../roadmap.md#programme-n--le-natif-drvm-drave-n0-distillation)
