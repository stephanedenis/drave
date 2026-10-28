<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# mmap (memory-mapped file) · madvise · DRAVEMMAP

> **Fiche glossaire — mmap (memory-mapped file) · madvise · DRAVEMMAP.** *mmap* projette un fichier en mémoire : le noyau lit les pages à la demande au lieu de charger le fichier. C'est ce qui permet d'ouvrir un GGUF de 365,7 Go avec 47 Mo de mémoire résidente ; `DRAVE_MMAP=0` revient à `read_to_end`, qui duplique le modèle (9,32 s et 6,35 Go contre 30,68 s et 19,20 Go en clusters) (`docs/implantation/format-clusters.md:181-186`,…
>
> **Famille :** [6. Répartition, matériel et énergie](../06-repartition-materiel-et-energie.md) · **Index :** [toutes les entrées](../README.md)
>
> **Définition complète :** [la famille](../06-repartition-materiel-et-energie.md)
