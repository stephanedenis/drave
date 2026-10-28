<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Cache compressé partagé (kvsourcelayerids)

> **Fiche glossaire — Cache compressé partagé (kvsourcelayerids).** Dans V4.1, seules quelques couches (**2, 8, 14, 20**) portent un compresseur et publient les clés compressées ; les couches suivantes (3..7, 9..13, 15..19, 21..39) **lisent les mêmes clés** au lieu de calculer les leurs. Un compresseur calculé couche par couche donnerait d'autres clés — un résultat faux qui ne casse rien.
>
> **Famille :** [2. Modèles et architectures](../02-modeles-et-architectures.md) · **Index :** [toutes les entrées](../README.md)
>
> **Définition complète :** [la famille](../02-modeles-et-architectures.md)
