# R52 — Décodeur multilingue (lecture en traduction)

> **Statut** : spécifiée · **Priorité** : P3 · **Programme** : R · **Dépend de** : B10.3, R31, R32
> **Ligne de roadmap** : R5.2 · **Fiche de résultat attendue** : rapport-r52-multilingue.md (à créer dans `reports/`)
> **Résumé** : Lire un document dans une langue et répondre dans une autre, sans que la réponse dépende de la surface.
> **Glossaire** : [chrF](../../theorie/glossaire/entrees/chrf.md) · [RSN](../../theorie/glossaire/entrees/representation-semantique-neutre.md).

## Le besoin

Lire toutes les langues est dans la mission, mais le décodeur sémantique est sous le plancher chrF (12,7 / 5,3 contre 39,6). Tant qu'il n'y arrive pas, la lecture multilingue n'est pas une lecture, c'est une traduction approximative.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | un document en L1 et une question en L2 |
| **sortie** | une réponse en L2 avec citations, indépendante de la langue source |
| **coût** | coût de traduction + lecture ; le décodeur est le goulot |
| **trace** | la langue source, la traduction et la réponse sont tracées |

## Ce qui est mesuré

- chrF de reconstruction et de traduction contre le plancher
- exactitude de la réponse par paire de langues
- sonde de langue sur `z`

## Portes

1. chrF > 39,6 (au-dessus du plancher)
2. la réponse ne dépend pas de la langue source
3. la sonde de langue reste basse

## Contrôles négatifs

- surface source contre référence (plancher chrF)
- langue non vue ; réponse monolingue

## Ce qui pourrait le rendre faux

- le corpus parallèle fuit dans l'entraînement
- un chrF élevé sans sens (surface)
- la langue reste dans `z`

## Étapes

1. améliorer le décodeur (attention croisée) sur 20–30 articles
2. mesurer chrF et la sonde
3. brancher la lecture en traduction ; écrire la fiche

## Documents à écrire

- `multilingue-decodeur.md` (décodeur, paires, porte, dans `docs/implantation/`)
- mettre à jour R5.2

## Voir aussi

- [Programme R](../roadmap.md#r5--la-lecture-croisée-et-le-multilingue)
- [Protocole sémantique](../../theorie/protocole-semantique.md)
