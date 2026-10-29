# R42 — Bloc code (AST, flux de données, exécution)

> **Statut** : spécifiée · **Priorité** : P2 · **Programme** : R · **Dépend de** : R01
> **Ligne de roadmap** : R4.2 · **Fiche de résultat attendue** : rapport-r42-bloc-code.md (à créer dans `reports/`)
> **Résumé** : Lire du code par son AST et son exécution, pas comme un texte.

## Le besoin

Lire du code demande la portée, le flux de données, les appels et l'exécution. Un parseur et un interpréteur classiques sont plus fiables qu'un modèle pour l'exactitude ; le modèle intervient pour l'intention.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | un fichier de code (langage supporté) et une question |
| **sortie** | un AST, un graphe de symboles, un résultat d'exécution ou une trace |
| **coût** | coût linéaire en nœuds ; l'exécution est bornée (sable) |
| **trace** | l'AST et l'exécution sont tracés |

## Ce qui est mesuré

- couverture du parseur (fichiers acceptés)
- exactitude de l'exécution
- exactitude des questions de code (valeur, flux, bug)

## Portes

1. 20 extraits exécutés exactement
2. le contrôle « texte seul » échoue sur les questions de valeur
3. l'exécution est isolée et reproductible

## Contrôles négatifs

- texte seul ; AST aléatoire ; sans exécuteur
- extrait avec une erreur volontaire (doit être signalé)

## Ce qui pourrait le rendre faux

- les tests contiennent la réponse
- le langage supporté est un sous-ensemble trop petit
- l'exécution n'est pas isolée (sécurité)

## Étapes

1. choisir le langage et le parseur
2. implémenter l'AST, les symboles et l'exécuteur
3. mesurer parseur et exécution ; écrire la fiche

## Documents à écrire

- `bloc-code.md` (langage, AST, exécuteur, porte, dans `docs/implantation/`)
- mettre à jour R4.2

## Voir aussi

- [Programme R](../roadmap.md#r4--les-blocs-structurels)
- [Analyse, § 6](../../theorie/lecture-rapide.md#6-par-type-de-document)
