# R21 — Mémoire de travail et gist

> **Statut** : spécifiée · **Priorité** : P1 · **Programme** : R · **Dépend de** : R01, R11 · **Contraint par** : la mémoire à 8 pas est négative (mesuré)
> **Ligne de roadmap** : R2.1 · **Fiche de résultat attendue** : rapport-r21-memoire-gist.md (à créer dans `reports/`)
> **Résumé** : Tenir un état de résumé, une table d'entités et de faits, et un tampon en entrée.

## Le besoin

Sans gist, le modèle ne comprend pas un document en plusieurs sections. N5 est négatif : le réseau ne retient pas le signal à 8 pas, mais le tampon gelé lit +0,879. Il faut donc commencer par le tampon, pas par un entraînement de mémoire.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | les sections lues (R01), les états de section (R11) et une question éventuelle |
| **sortie** | un gist : résumé, entités, faits, dates, citations ; état borné |
| **coût** | coût linéaire en sections ; le gist ne dépasse pas une taille fixée |
| **trace** | chaque fait du gist porte sa région et son offset |

## Ce qui est mesuré

- exactitude sur des questions multi-sections
- exactitude de citation (la région source est-elle la bonne ?)
- taux d'oubli : une information de la section 2 est-elle encore là après la 5 ?

## Portes

1. le gist bat le closed-book sur les questions dont l'indice est loin
2. la citation est exacte
3. pas de perte sur les documents courts

## Contrôles négatifs

- sans gist (closed-book) ; gist aléatoire ; gist complet (oracle)
- question dont la réponse est dans une seule section (contrôle facile)

## Ce qui pourrait le rendre faux

- le gist contient la réponse gold
- les questions d'évaluation portent sur le résumé lui-même
- la table d'entités grossit jusqu'à contenir le document

## Étapes

1. définir le gist (champs, taille, provenance)
2. implémenter le tampon en entrée et le résumé par section
3. mesurer multi-sections et citation ; écrire la fiche

## Documents à écrire

- `memoire-gist.md` (champs, taille, tampon, porte, dans `docs/implantation/`)
- mettre à jour R2.1

## Voir aussi

- [Programme R](../roadmap.md#r2--la-mémoire)
- [Analyse, § 5.4](../../theorie/lecture-rapide.md#54-la-mémoire-de-travail-et-épisodique-l4)
