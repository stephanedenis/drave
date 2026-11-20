<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# DenseQ4 · DenseQ8

> **TL;DR — DenseQ4 · DenseQ8.** Les deux noyaux denses du moteur : `DenseQ8` lit un bloc int8 à échelle par bloc de 32 et calcule un produit scalaire entier (exact au bit près en AVX2) ; `DenseQ4` fait de même sur des nibbles signés biaisés, avec une échelle `u16` par bloc (`docs/implantation/contexte-long.md:378-382`, `reports/rapport-mur-memoire-4bits.md:87-92`).
>
> **Ce que c'est, en clair.** Définition complète dans la famille.
>
> **Famille :** [4. Le moteur Drave : exécution, structures, outils](../04-le-moteur-drave-execution-structures-out.md) · **Index :** [toutes les entrées](../README.md)
> · **Définition complète :** [la famille](../04-le-moteur-drave-execution-structures-out.md)
>
> **Références externes :** voir [les sources citées](../09-sources-externes-citees.md)
