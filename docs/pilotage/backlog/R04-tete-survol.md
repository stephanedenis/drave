# R04 — Tête de survol (pertinence d'une région)

> **Statut** : spécifiée · **Priorité** : P1 · **Programme** : R · **Dépend de** : R03, R01
> **Ligne de roadmap** : R0.4 · **Fiche de résultat attendue** : rapport-r04-tete-survol.md (à créer dans `reports/`)
> **Résumé** : Prédire, depuis le début d'une région, si elle vaut la peine d'être lue pour le but courant.
> **Glossaire** : [lecture rapide](../../theorie/glossaire/entrees/lecture-rapide.md) · [AUC](../../theorie/glossaire/entrees/auc.md) · [contrat](../../theorie/glossaire/entrees/contrat.md).

## Le besoin

Le contrôleur classique décide avec des mots-clés et des titres. Une petite tête peut apprendre la pertinence à partir du début de la région et remplacer le scoreur manuel — à condition de battre le classique à budget égal.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | le préfixe d'une région (titre + premières phrases) et le but |
| **sortie** | un score de pertinence 0-1, avec la décision lire/sauter |
| **coût** | moins de 5 % du coût d'une lecture intégrale |
| **trace** | le score et la décision sont tracés par région |

## Ce qui est mesuré

- AUC et exactitude de la pertinence contre le scoreur classique
- coût de la tête et temps par région
- gains sur la courbe vitesse-compréhension (R03)

## Portes

1. la tête bat le scoreur classique à budget égal sur 3 types
2. le score est calibré (pas seulement un classement)
3. la tête ne lit pas le but dans le titre (contrôle sans but)

## Contrôles négatifs

- titres mélangés ; scores aléatoires ; but absent
- régions de même longueur et même position (pour éviter le raccourci)

## Ce qui pourrait le rendre faux

- la tête apprend la position ou la longueur, pas la pertinence
- le but apparaît dans le titre de la région
- le jeu d'entraînement et le jeu de test partagent le même document

## Étapes

1. construire le jeu (région, but, pertinence gold)
2. entraîner une petite tête sur les états précoces
3. évaluer contre le classique et le hasard
4. brancher dans le contrôleur ; écrire la fiche

## Documents à écrire

- `tete-survol.md` (contrat, données, entraînement, porte, dans `docs/implantation/`)
- mettre à jour R0.4

## Voir aussi

- [Programme R](../roadmap.md#r0--le-lecteur-v0-système-sans-entraînement)
- [Analyse, § 5.3](../../theorie/lecture-rapide.md#53-la-politique-de-lecture-l3--le-cœur-du-sujet)
