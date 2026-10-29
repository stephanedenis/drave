# R41 — Bloc tableaux

> **Statut** : spécifiée · **Priorité** : P2 · **Programme** : R · **Dépend de** : R01
> **Ligne de roadmap** : R4.1 · **Fiche de résultat attendue** : rapport-r41-bloc-tableaux.md (à créer dans `reports/`)
> **Résumé** : Lire un tableau en 2D : en-têtes, cellules, lignes, colonnes, et opérations classiques.
> **Glossaire** : [tableau](../../theorie/glossaire/entrees/tableau.md) · [parseur](../../theorie/glossaire/entrees/parseur.md) · [contrat](../../theorie/glossaire/entrees/contrat.md).

## Le besoin

Un tableau n'est pas du texte plat : il faut retrouver les en-têtes, les cellules, les fusions, puis comparer, filtrer, agréger. Un parseur classique et un opérateur relationnel suffisent pour l'essentiel.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | un tableau (HTML, CSV, Markdown ou région de R01) |
| **sortie** | une grille typée (lignes, colonnes, en-têtes, cellules, fusions) + résultats d'opérations |
| **coût** | coût linéaire en cellules ; opérations classiques |
| **trace** | la grille et chaque opération sont tracées |

## Ce qui est mesuré

- exactitude des cellules et des en-têtes
- exactitude des opérations (filtre, jointure, agrégat)
- taux d'échec sur les fusions et les tableaux multi-niveaux

## Portes

1. 100 cellules extraites exactement
2. l'opération relationnelle redonne le résultat attendu
3. le contrôle « texte plat » échoue

## Contrôles négatifs

- texte plat ; colonnes mélangées ; cellules fusionnées
- tableau sans en-tête (doit être signalé)

## Ce qui pourrait le rendre faux

- le corpus ne contient que des tableaux simples
- le CSV est déjà structuré (ce n'est pas un parseur de tableau)
- les erreurs d'OCR sont comptées comme des erreurs de parseur

## Étapes

1. définir la grille et le parseur (HTML/CSV/Markdown)
2. implémenter les opérations classiques
3. mesurer cellules, en-têtes, opérations ; écrire la fiche

## Documents à écrire

- `bloc-tableaux.md` (grille, parseur, opérations, porte, dans `docs/implantation/`)
- mettre à jour R4.1

## Voir aussi

- [Programme R](../roadmap.md#r4--les-blocs-structurels)
- [Analyse, § 6](../../theorie/lecture-rapide.md#6-par-type-de-document)
