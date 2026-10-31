# R13 — Tokenisation : octets ou BPE (décision mesurée)

> **Statut** : mesurée · **Priorité** : P2 · **Programme** : R · **Dépend de** : — · **Plafonné par** : N2 (la qualité du corpus)
> **Ligne de roadmap** : R1.3 · **Fiche de résultat** : [rapport-r13-decision.md](../../../reports/rapport-r13-decision.md) — **décision : octets** ; BPE 512 **+0,39 %**, BPE 1024 **+4,09 %**, anglais **+4,22 / +6,59 %** à octets égaux. Spécification : [tokenisation.md](../../implantation/tokenisation.md).
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

## Le résultat (2026-10-30)

À budget d'**octets** égal — la seule comparaison qui vaille entre deux tokenisations — les
octets gagnent partout :

| dispositif | bytes | BPE 512 | BPE 1024 |
|---|---:|---:|---:|
| français, 10 k / 5 k pas | **1,8021** | 1,8142 | — |
| français, 4 k pas | **1,8021** | — | 1,8726 |
| anglais 100 Mo | **2,6408** | 2,7522 | 2,8147 |
| français, deux graines | **1,8001** | 1,8071 | 1,8738 |

Le pilote à 200/400 pas qui donnait **11 %** au BPE était un **artefact de budget** : à pas
égaux, le BPE voit deux fois plus d'octets. Décision : le natif **reste en octets**.

## Étapes

1. ✅ implémenter les deux tokenisations et le même entraînement
2. ✅ mesurer PPL, coût, empan ; écrire les fiches
3. ✅ décider et documenter dans la roadmap

## Documents

- ✅ [`implantation/tokenisation.md`](../../implantation/tokenisation.md) — spécification et décision.
- ✅ R1.3 mis à jour ; la réouverture est conditionnée (modèle 50–100 M, contexte égal).

## Voir aussi

- [Programme R](../roadmap.md#r1--la-fenêtre-native)
- [Architecture native](../../theorie/architecture-native.md)
