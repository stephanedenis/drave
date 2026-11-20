<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# YaRN (Yet another RoPE extensioN) · mscale · facteur

> **TL;DR — YaRN (Yet another RoPE extensioN) · mscale · facteur.** Méthode pour étendre la portée positionnelle d'un modèle au-delà de sa longueur d'entraînement, en interpolant les basses fréquences et en mettant le softmax à l'échelle par un facteur `mscale = 1 + 0,1·ln(f)`. Le dépôt mesure que l'interpolation **dégrade** sur du texte brut et que `mscale` en est la moitié nuisible : le YaRN n'est donc appliqué qu'au-delà de 4…
>
> **Ce que c'est, en clair.** Définition complète dans la famille.
>
> **Famille :** [2. Modèles et architectures](../02-modeles-et-architectures.md) · **Index :** [toutes les entrées](../README.md)
> · **Définition complète :** [la famille](../02-modeles-et-architectures.md)
>
> **Références externes :** voir [les sources citées](../09-sources-externes-citees.md)
