<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# GPU · Quadro RTX 5000 · miroir VRAM · déport

> **Fiche glossaire — GPU · Quadro RTX 5000 · miroir VRAM · déport.** Les deux Quadro RTX 5000 (16 Go chacune) servent de *déport* : le cache KV y est recopié en **miroir** paginé, ce qui fait passer l'attention à 1 M de clés de 968 ms à 13,2 ms par couche (×73) et rend le poste « attention » plat (3,3 ms/jeton) au lieu de croître linéairement (`docs/implantation/contexte-long.md:212-297`). **Où** : `DRAVE_GPU`, `DRAVE_GPU_KV`,…
>
> **Famille :** [6. Répartition, matériel et énergie](../06-repartition-materiel-et-energie.md) · **Index :** [toutes les entrées](../README.md)
>
> **Définition complète :** [la famille](../06-repartition-materiel-et-energie.md)
