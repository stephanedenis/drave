<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# NVMe · SSD · ODIRECT · pread

> **TL;DR — NVMe · SSD · ODIRECT · pread.** *NVMe* est le protocole des SSD rapides branchés en PCIe ; *pread* lit à une position donnée sans déplacer le curseur ; *O_DIRECT* demande à contourner le cache du noyau (il échoue ici, errno 29). Le NVMe parallélisé à 16 lecteurs (31 Go/s) dépasse la RAM (22 Go/s) : c'est le chemin retenu pour les experts (`reports/rapport-architecture-memoire.md:181-195`).
>
> **Ce que c'est, en clair.** Définition complète dans la famille.
>
> **Famille :** [6. Répartition, matériel et énergie](../06-repartition-materiel-et-energie.md) · **Index :** [toutes les entrées](../README.md)
> · **Définition complète :** [la famille](../06-repartition-materiel-et-energie.md)
>
> **Références externes :** voir [les sources citées](../09-sources-externes-citees.md)
