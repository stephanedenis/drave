<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Q2K · Q3K · Q4K · Q5K · Q6K · Q8K (k-quants)

> **TL;DR — Q2K · Q3K · Q4K · Q5K · Q6K · Q8K (k-quants).** Types ggml à **super-blocs** de 256 poids, avec échelles et minima sur 6 bits ; `Q4_K_M` est la quantification la plus courante des modèles publiés (Qwen3-30B, Qwen2.5-1.5B). Un bug historique : ggml écrit les quatre quants d'un `Q6_K` en quarts successifs, le moteur les entrelaçait — trouvé en comparant à une référence F16 des mêmes poids (`docs/implantation/convertisseur.md:210-226`).
>
> **Ce que c'est, en clair.** Définition complète dans la famille.
>
> **Famille :** [3. Formats, quantification, encodage](../03-formats-quantification-encodage.md) · **Index :** [toutes les entrées](../README.md)
> · **Définition complète :** [la famille](../03-formats-quantification-encodage.md)
>
> **Références externes :** voir [les sources citées](../09-sources-externes-citees.md)
