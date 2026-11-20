<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Position (compteur global de jeton)

> **TL;DR — Position (compteur global de jeton).** Champ de la trace qui compte les jetons **globalement**, pas la place dans la fenêtre de contexte. Ce détail a coûté un bug : avec la position dans la fenêtre, deux fenêtres réécrivaient les mêmes clés et le rejeu rendait 356 694 au lieu de 17,43 (`docs/implantation/format-flux.md:75-86`).
>
> **Ce que c'est, en clair.** Définition complète dans la famille.
>
> **Famille :** [5. Flux, protocole et transport](../05-flux-protocole-et-transport.md) · **Index :** [toutes les entrées](../README.md)
> · **Définition complète :** [la famille](../05-flux-protocole-et-transport.md)
>
> **Références externes :** voir [les sources citées](../09-sources-externes-citees.md)
