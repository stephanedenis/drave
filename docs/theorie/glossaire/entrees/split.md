<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Split

> **TL;DR — Split.** La **partition** d'un corpus en trois fichiers : `train.txt` (l'entraînement), `val.txt` (le réglage), `test.txt` (la mesure finale). Le dépôt la tire d'un **hash salé** de l'identifiant du document (le `page_id` ou le chemin), avec un sel fixé par `--graine` : la même graine redonne le même split, et un document ne change jamais de camp.
>
> **Ce que c'est, en clair.** Définition complète dans la famille.
>
> **Famille :** [13. Le corpus et la mesure documentaire](../13-le-corpus-et-la-mesure-documentaire.md) · **Index :** [toutes les entrées](../README.md)
> · **Définition complète :** [la famille](../13-le-corpus-et-la-mesure-documentaire.md)
>
> **Références externes :** voir [les sources citées](../09-sources-externes-citees.md)
