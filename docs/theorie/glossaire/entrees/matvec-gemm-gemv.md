<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# matvec · GEMM · GEMV

> **Fiche glossaire — matvec · GEMM · GEMV.** *GEMV* : produit matrice-vecteur (un jeton à la fois) ; *GEMM* : produit matrice-matrice (plusieurs jetons ensemble, donc les poids relus une fois pour tout le lot). Le préremplissage par lots est le passage GEMV → GEMM : −20 % à −31 % de temps mesuré (`docs/implantation/contexte-long.md:52-59`, `reports/rapport-prefill-par-lots.md`).
>
> **Famille :** [4. Le moteur Drave : exécution, structures, outils](../04-le-moteur-drave-execution-structures-out.md) · **Index :** [toutes les entrées](../README.md)
>
> **Définition complète :** [la famille](../04-le-moteur-drave-execution-structures-out.md)
