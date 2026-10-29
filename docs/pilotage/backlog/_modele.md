# <ID> — <TITRE>

> **Statut** : idée · **Priorité** : P? · **Programme** : R · **Dépend de** : —
> **Ligne de roadmap** : R?.? · **Fiche de résultat attendue** : `<rapport-attendu>.md` (à créer dans `reports/`)
> **Résumé** : une phrase qui dit ce que la fonctionnalité rend possible.

## Le besoin

Pourquoi elle existe, pour qui, et ce qui est impossible aujourd'hui sans elle. Deux à quatre phrases.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | ce qu'elle reçoit, avec le type et la provenance |
| **sortie** | ce qu'elle rend, avec le type et la provenance |
| **coût** | ce qu'elle coûte, dans l'unité du projet (événements, paires, octets, secondes) |
| **trace** | ce qui est tracé, et ce qui permet de rejouer |

## Ce qui est mesuré

- la mesure principale, avec son unité ;
- la mesure de qualité (exactitude, fidélité, citation) ;
- la mesure de coût (événements, octets, temps).

## Portes

1. un critère **numérique** et **reproductible** ;
2. un second critère qui empêche la triche (tenu à l'écart, langue changée, etc.) ;
3. un troisième qui vérifie le rejeu ou la stabilité.

## Contrôles négatifs

- le contrôle qui doit **échouer** si la fonctionnalité ne marche pas ;
- le contrôle qui doit **être plus bas** que la fonctionnalité (hasard, texte plat, sans mémoire) ;
- le contrôle de **fuite** (réponse dans le titre, dans le gold, dans l'entraînement).

## Ce qui pourrait le rendre faux

- la fuite de données ;
- le réglage sur le test ;
- la mesure qui dépend d'un cache, d'une graine ou d'une version ;
- le petit N.

## Étapes

1. écrire le contrat et les tests ;
2. implémenter le chemin minimal ;
3. mesurer et écrire la fiche de résultat ;
4. mettre à jour la roadmap et l'état.

## Documents à écrire

- la spécification d'implantation (dans `docs/implantation/`) ;
- la fiche de résultat (dans `reports/`) ;
- la ligne de roadmap et l'état.

## Voir aussi

- [Le programme R](../roadmap.md#programme-r--le-lecteur-la-nouvelle-cible)
- [L'analyse de la lecture rapide](../../theorie/lecture-rapide.md)
- [Le backlog](index.md)

---

*Ce fichier est un **modèle** : on le copie, on remplace les `<...>`, et on supprime cette ligne.*
