# R41 — Bloc tableaux

> **Statut** : mesurée · **Priorité** : P2 · **Programme** : R · **Dépend de** : R01
> **Ligne de roadmap** : R4.1 · **Fiche de résultat** : [`rapport-r41-bloc-tableaux.md`](../../../reports/rapport-r41-bloc-tableaux.md)
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

## L'état

**Mesurée le 2026-10-29** — 35 tableaux, **996 cellules**, **802** cellules Markdown rendues
exactement à leur tranche de source (en-têtes compris) ; **8/8** opérations justes ; le
contrôle **texte plat échoue 3/3** ; **4 refus nommés** (irrégulier, en-tête fusionnée,
tableau imbriqué, colonne de texte non sommable). Coût **≈ 25 ms / 1 000 cellules**, linéaire
(×3,8 pour ×4). Fiche : [`rapport-r41-bloc-tableaux.md`](../../../reports/rapport-r41-bloc-tableaux.md) ;
spécification : [`bloc-tableaux.md`](../../implantation/bloc-tableaux.md) ; porte :
`tools/porte-bloc-tableaux.sh` ; JSON : [`r41-bloc-tableaux.json`](../../../reports/r41-bloc-tableaux.json).

**Ce que R4.1 ne fait pas** : les tableaux PDF non balisés (R0.1 les laisse en texte, R4.4
les prendra) ; les en-têtes fusionnées (refusées, pas devinées).

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

1. ✅ définir la grille et le parseur (HTML/CSV/Markdown)
2. ✅ implémenter les opérations classiques
3. ✅ mesurer cellules, en-têtes, opérations ; écrire la fiche

## Documents

- ✅ [`bloc-tableaux.md`](../../implantation/bloc-tableaux.md) — la grille, le parseur, les opérations, la porte, les limites.
- ✅ R4.1 marquée mesurée dans la roadmap ; prochaine action : **R4.2**.

## Voir aussi

- [Programme R](../roadmap.md#r4--les-blocs-structurels)
- [Analyse, § 6](../../theorie/lecture-rapide.md#6-par-type-de-document)
