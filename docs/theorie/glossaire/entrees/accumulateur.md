<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Accumulateur

> **Fiche glossaire — Accumulateur.** Vecteur de sortie dans lequel le mode « push » disperse les contributions : `acc[destination] += valeur × poids`. Sa taille décide de tout : 4 096 sorties × 3 octets = 12 Kio tiennent dans les blocs mémoire du FPGA, mais un accumulateur par fil de calcul fait 36 Mo pour une tête de 151 936 sorties (`reports/rapport-cpu-aer.md:11`, `reports/rapport-inference.md:131`).
>
> **Famille :** [4. Le moteur Drave : exécution, structures, outils](../04-le-moteur-drave-execution-structures-out.md) · **Index :** [toutes les entrées](../README.md)
>
> **Définition complète :** [la famille](../04-le-moteur-drave-execution-structures-out.md)
