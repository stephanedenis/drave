# R01 — Graphe de document et registre de régions

> **Statut** : prête · **Priorité** : P0 · **Programme** : R · **Dépend de** : —
> **Ligne de roadmap** : R0.1 · **Fiche de résultat attendue** : rapport-r01-graphe-document.md (à créer dans `reports/`)
> **Résumé** : Transformer un document en un arbre de régions typées, avec offsets et provenance, sans modèle.
> **Glossaire** : [graphe de document](../../theorie/glossaire/entrees/graphe-de-document.md) · [parseur](../../theorie/glossaire/entrees/parseur.md) · [contrat](../../theorie/glossaire/entrees/contrat.md).

## Le besoin

Le modèle ne voit qu'un flux d'octets : il ne peut pas dire « lis le titre, saute la section 3, compare les colonnes ». Il faut une représentation du document qui survive au rejeu et qui serve de champ de lecture au contrôleur.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | un fichier (PDF, HTML, DOCX, Markdown, EPUB) et sa langue |
| **sortie** | un manifeste de régions : type, parent, offsets, texte, hash, ordre de lecture |
| **coût** | O(octets) ; pas de modèle ; un parseur par format |
| **trace** | la décision de découpe est tracée (région, offsets, parseur) et rejouable |

## Ce qui est mesuré

- couverture du texte : aucun octet perdu, aucun octet inventé
- exactitude du type de région sur 30 documents annotés
- exactitude des offsets et de l'ordre de lecture (colonnes, notes, légendes)

## Portes

1. 50 pages découpées ; chaque région a un offset exact et un hash vérifiable
2. « où est le tableau X ? » se résout sans modèle, par le manifeste
3. le rejeu de la découpe redonne le même manifeste

## Contrôles négatifs

- texte plat : la structure doit être perdue, et la porte doit le voir
- PDF deux colonnes : l'ordre de lecture ne doit pas entrelacer les colonnes
- notes de bas de page et légendes : elles ne doivent pas être comptées comme du corps

## Ce qui pourrait le rendre faux

- le parseur dépend d'une seule bibliothèque ou d'une version : le manifeste change sans prévenir
- le PDF contient du texte caché, des ligatures ou des colonnes non balisées
- les annotations gold fuient dans les titres ou les légendes

## Étapes

1. écrire le schéma de manifeste (type, offsets, parent, hash) et le testeur
2. brancher un parseur par format, avec un test de couverture
3. construire le corpus de 30 documents annotés (5 types × 6)
4. mesurer la couverture, les types, les offsets ; écrire la fiche

## Documents à écrire

- `document-graph.md` (spécification du manifeste, dans `docs/implantation/`)
- mettre à jour la ligne R0.1 de la roadmap

## Voir aussi

- [Programme R](../roadmap.md#programme-r--le-lecteur-la-nouvelle-cible)
- [Analyse, § 5.1](../../theorie/lecture-rapide.md#51-le-document-l2)
