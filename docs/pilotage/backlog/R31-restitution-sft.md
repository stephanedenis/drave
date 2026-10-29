# R31 — Restitution : SFT de lecture (réponse, résumé, extraction)

> **Statut** : spécifiée · **Priorité** : P1 · **Programme** : R · **Dépend de** : R01, R03, R21 · **Plafonné par** : N4
> **Ligne de roadmap** : R3.1 · **Fiche de résultat attendue** : rapport-r31-restitution-sft.md (à créer dans `reports/`)
> **Résumé** : Apprendre au modèle à répondre, résumer et extraire depuis ce qu'il a lu, sur des jeux tenus à l'écart.

## Le besoin

La PPL ne prouve pas la lecture. Le SFT actuel mémorise (24/24 vus, 0/4 tenus). Il faut une tâche de restitution avec un partage par document, pas par exemple.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | un document lu (gist et régions) et une instruction (répondre, résumer, extraire, refuser) |
| **sortie** | une réponse courte, avec citation et refus explicite si l'information manque |
| **coût** | coût de génération borné ; pas de document entier en entrée |
| **trace** | la réponse, la citation et le refus sont tracés |

## Ce qui est mesuré

- exactitude tenue à l'écart (documents non vus)
- format et refus (pas d'invention)
- exactitude de citation

## Portes

1. ≥ 80 % des instructions tenues à l'écart
2. le contrôle 24/24 vus ne compte pas
3. le refus est explicite quand l'information manque

## Contrôles négatifs

- vus/non vus ; closed-book ; réponses mélangées
- instruction impossible (le modèle doit refuser)

## Ce qui pourrait le rendre faux

- les documents de test sont dans l'entraînement
- le modèle apprend le format, pas la lecture
- petit N de documents tenus à l'écart

## Étapes

1. construire les jeux (réponse, résumé, extraction, refus) avec partage par document
2. entraîner le SFT sur le natif ou un adaptateur
3. évaluer tenu à l'écart ; écrire la fiche

## Documents à écrire

- `restitution-sft.md` (jeux, partage, métriques, porte, dans `docs/implantation/`)
- mettre à jour R3.1

## Voir aussi

- [Programme R](../roadmap.md#r3--la-restitution)
- [Analyse, § 5.5](../../theorie/lecture-rapide.md#55-la-restitution-et-le-banc-l5-l6)
