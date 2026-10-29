# R32 — Citations et provenance

> **Statut** : spécifiée · **Priorité** : P2 · **Programme** : R · **Dépend de** : R31, R01, R21
> **Ligne de roadmap** : R3.2 · **Fiche de résultat attendue** : rapport-r32-citations.md (à créer dans `reports/`)
> **Résumé** : Faire citer chaque réponse par sa région et son offset, et vérifier la citation.

## Le besoin

Une réponse sans provenance n'est pas une lecture vérifiable. Le bus trace déjà les événements ; il faut relier la réponse à la région lue, puis contrôler la citation.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | une réponse (R31), les régions lues (R01) et le gist (R21) |
| **sortie** | une réponse avec citations (région, offset, texte) et un indicateur de support |
| **coût** | coût négligeable par réponse |
| **trace** | la citation est tracée et vérifiable |

## Ce qui est mesuré

- précision et rappel des citations
- exactitude de la réponse avec et sans citation
- taux de réponses non supportées

## Portes

1. chaque citation pointe un span exact
2. les réponses non supportées sont signalées
3. le contrôle sans citation est plus bas

## Contrôles négatifs

- sans citation ; citation aléatoire ; citation gold
- réponse juste avec une citation fausse (doit être détectée)

## Ce qui pourrait le rendre faux

- la citation est ajoutée après coup, sans lien avec le calcul
- le chevauchement de spans est trop permissif
- le modèle cite le titre au lieu de la phrase

## Étapes

1. définir le format de citation et le vérificateur
2. brancher la réponse sur les régions lues
3. mesurer précision/rappel ; écrire la fiche

## Documents à écrire

- `citations-provenance.md` (format, vérificateur, porte, dans `docs/implantation/`)
- mettre à jour R3.2

## Voir aussi

- [Programme R](../roadmap.md#r3--la-restitution)
- [Analyse, § 5.5](../../theorie/lecture-rapide.md#55-la-restitution-et-le-banc-l5-l6)
