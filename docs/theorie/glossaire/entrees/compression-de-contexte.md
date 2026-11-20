<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Compression de contexte (ratio 1, 2, 4, 128)

> **TL;DR — Compression de contexte (ratio 1, 2, 4, 128).** Résumer `ratio` jetons en un seul latent de clé, afin que l'attention ne croisse plus avec la longueur. V4-Flash mélange **CSA** (ratio 4, fenêtre à chevauchement) et **HCA** (ratio 128) ; V4.1 utilise **2** (softmax par canal sur le groupe, apprise porte) et **1** (un latent par jeton, sans porte ni `ape`).
>
> **Ce que c'est, en clair.** Définition complète dans la famille.
>
> **Famille :** [2. Modèles et architectures](../02-modeles-et-architectures.md) · **Index :** [toutes les entrées](../README.md)
> · **Définition complète :** [la famille](../02-modeles-et-architectures.md)
>
> **Références externes :** voir [les sources citées](../09-sources-externes-citees.md)
