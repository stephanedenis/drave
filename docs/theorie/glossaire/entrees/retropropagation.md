<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Rétropropagation

> **TL;DR — Rétropropagation.** L'algorithme standard qui ajuste les poids d'un réseau en propageant l'erreur de la sortie vers l'entrée. **Le pont ne l'utilise pas.** C'est une contrainte du projet, pour deux raisons : elle exige de connaître la sortie désirée partout, et elle rend l'apprentissage dépendant d'un calcul global, donc peu compatible avec une croissance locale par corrélation.
>
> **Ce que c'est, en clair.** Définition complète dans la famille.
>
> **Famille :** [10. Le pont linguistico-sémantique — le vocabulaire de l'émulation](../10-le-pont-linguistico-semantique-le-vocabu.md) · **Index :** [toutes les entrées](../README.md)
> · **Définition complète :** [la famille](../10-le-pont-linguistico-semantique-le-vocabu.md)
>
> **Références externes :** voir [les sources citées](../09-sources-externes-citees.md)
