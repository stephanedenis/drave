<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# mHC retardé (chaîne retardée de V4.1)

> **Fiche glossaire — mHC retardé (chaîne retardée de V4.1).** Dans **V4** (`deepseek4`), chaque raccord (attention, FFN) replie l'entrée avec **ses propres** coefficients ; dans **V4.1** (`deepseek41`), les coefficients servent au raccord **suivant** : l'attention se replie avec la `pre` de la FFN précédente, la FFN avec la `pre` de l'attention courante, et la **tête** — qui n'a aucun poids appris chez V4.1 — avec la `pre` de la dernière…
>
> **Famille :** [2. Modèles et architectures](../02-modeles-et-architectures.md) · **Index :** [toutes les entrées](../README.md)
>
> **Définition complète :** [la famille](../02-modeles-et-architectures.md)
