# R51 — Lecture croisée / multi-documents

> **Statut** : spécifiée · **Priorité** : P3 · **Programme** : R · **Dépend de** : R31, R32, R03, R01 · **Contraint par** : le manque M4 (aucun encodeur exécutable)
> **Ligne de roadmap** : R5.1 · **Fiche de résultat attendue** : rapport-r51-lecture-croisee.md (à créer dans `reports/`)
> **Résumé** : Comparer plusieurs documents, suivre les citations et signaler les contradictions.

## Le besoin

La lecture réelle compare des sources. Il faut un index, un retrieval, une provenance et un moyen de dire « ces deux documents se contredisent » — sans quoi la lecture reste mono-document.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | plusieurs documents (R01) et une question comparative |
| **sortie** | une réponse comparative avec citations, accords et contradictions |
| **coût** | coût de retrieval + lecture des régions retenues |
| **trace** | chaque source et chaque contradiction sont tracées |

## Ce qui est mesuré

- rappel du retrieval multi-documents
- exactitude de la comparaison
- détection de contradiction (précision/rappel)

## Portes

1. réponse avec deux sources citées
2. le contrôle à une seule source échoue
3. les contradictions sont signalées, pas moyennées

## Contrôles négatifs

- une seule source ; documents mélangés ; sans index
- documents quasi identiques (doit être signalé)

## Ce qui pourrait le rendre faux

- les documents sont des doublons
- la réponse est dans un seul document
- l'index contient la réponse gold

## Étapes

1. construire l'index et le retrieval
2. implémenter la comparaison et la provenance
3. mesurer retrieval, comparaison, contradictions ; écrire la fiche

## Documents à écrire

- `lecture-croisee.md` (index, retrieval, comparaison, porte, dans `docs/implantation/`)
- mettre à jour R5.1

## Voir aussi

- [Programme R](../roadmap.md#r5--la-lecture-croisée-et-le-multilingue)
- [Analyse, § 4](../../theorie/lecture-rapide.md#4-les-14-techniques-et-leur-état)
