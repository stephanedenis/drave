# R22 — Mémoire épisodique et relecture

> **Statut** : spécifiée · **Priorité** : P2 · **Programme** : R · **Dépend de** : R01, R21
> **Ligne de roadmap** : R2.2 · **Fiche de résultat attendue** : rapport-r22-memoire-episodique.md (à créer dans `reports/`)
> **Résumé** : Stocker les régions, les offsets et les états pour pouvoir revenir sur un passage.
> **Glossaire** : [gist](../../theorie/glossaire/entrees/gist.md) · [KV](../../theorie/glossaire/entrees/kv.md) · [retrieval](../../theorie/glossaire/entrees/retrieval.md).

## Le besoin

La relecture humaine n'est possible que si le texte et son état sont encore là. Le KV cache est un cache, pas une mémoire de document ; il faut un store de régions et un déclencheur de retour.

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | la trajectoire de lecture (R02) et les régions (R01) |
| **sortie** | un store interrogeable (région, offset, état, résumé) et une politique d'éviction |
| **coût** | le store est borné ; la relecture coûte le prix de la région relue |
| **trace** | chaque accès au store est tracé |

## Ce qui est mesuré

- rappel de l'information après éviction
- gain de la relecture sur des questions ciblées
- coût du store et de la relecture

## Portes

1. la relecture récupère une information que le gist a perdue
2. sans le store, la même question échoue
3. le store reste borné sur 50 documents

## Contrôles négatifs

- sans store ; store aléatoire ; store complet (oracle)
- relecture de la même région sans information nouvelle

## Ce qui pourrait le rendre faux

- le store est une copie intégrale du document (ce n'est pas une mémoire, c'est un fichier)
- la récupération se fait par chaîne exacte seulement
- la question contient l'offset de la réponse

## Étapes

1. définir le store et l'éviction
2. implémenter la récupération et le déclencheur (R06)
3. mesurer le rappel et le coût ; écrire la fiche

## Documents à écrire

- `memoire-episodique.md` (store, éviction, relecture, porte, dans `docs/implantation/`)
- mettre à jour R2.2

## Voir aussi

- [Programme R](../roadmap.md#r2--la-mémoire)
- [Analyse, § 5.4](../../theorie/lecture-rapide.md#54-la-mémoire-de-travail-et-épisodique-l4)
