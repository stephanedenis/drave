# R13 — Tokenisation : octets ou BPE (décision mesurée)

> **Statut** : spécifiée · **Priorité** : P2 · **Programme** : R · **Dépend de** : — · **Plafonné par** : N2 (la qualité du corpus)
> **Ligne de roadmap** : R1.3 · **Fiche de résultat attendue** : rapport-r13-tokenisation.md (à créer dans `reports/`)
> **Résumé** : Décider par la mesure si le natif doit rester en octets ou passer au BPE.
> **Glossaire** : [BPE](../../theorie/glossaire/entrees/bpe.md) · [tokeniseur](../../theorie/glossaire/entrees/tokeniser-tokenizer.md) · [perplexité](../../theorie/glossaire/entrees/perplexite.md).

## Le besoin

Les octets allongent les séquences de 3–4× et réduisent l'empan utile. Le BPE est une décision de v1, pas un prérequis : il faut la chiffrer, pas la supposer.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | deux tokenisations (octets, BPE) sur le même corpus et le même budget |
| **sortie** | PPL, bits/octet, octets par jeton, temps, empan utile |
| **coût** | même calcul, même données, même évaluation |
| **trace** | le vocabulaire et les règles de découpage sont versionnés |

## Ce qui est mesuré

- PPL et bits/octet à budget égal
- nombre de jetons par octet et mots couverts à contexte égal
- temps par octet et mémoire du vocabulaire

## Portes

1. même qualité avec moins de pas ou un coût plus bas
2. pas de régression sur les langues et les scripts non latins
3. le découpage est réversible (surface exacte)

## Contrôles négatifs

- même graine, même budget, même corpus
- vocabulaire vide ou aléatoire (le gain doit disparaître)

## Ce qui pourrait le rendre faux

- le BPE change les données effectives (mêmes octets, autres frontières)
- le vocabulaire contient les réponses du test
- la comparaison ne tient pas compte des longueurs de séquence

## Étapes

1. implémenter les deux tokenisations et le même entraînement
2. mesurer PPL, coût, empan ; écrire la fiche
3. décider et documenter dans la roadmap

## Documents à écrire

- `tokenisation.md` (vocabulaire, découpage, mesures, décision, dans `docs/implantation/`)
- mettre à jour R1.3

## Voir aussi

- [Programme R](../roadmap.md#r1--la-fenêtre-native)
- [Architecture native](../../theorie/architecture-native.md)
