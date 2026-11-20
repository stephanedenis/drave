<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Contrat d'activation (Act)

> **TL;DR — Contrat d'activation (Act).** L'ensemble des réglages qui changent les chiffres calculés : niveaux de quantification, seuil, top-k, renormalisation, et les sept top-k par projection, plus `attn_topk`, `qk_topk`, `moe_topk`. Ils **voyagent dans l'en-tête** parce que sans eux le pair distant ne calculerait pas la même chose — et « le client impose les siens au serveur » (`docs/implantation/format-flux.md:100-109`, `:187`).
>
> **Ce que c'est, en clair.** Définition complète dans la famille.
>
> **Famille :** [5. Flux, protocole et transport](../05-flux-protocole-et-transport.md) · **Index :** [toutes les entrées](../README.md)
> · **Définition complète :** [la famille](../05-flux-protocole-et-transport.md)
>
> **Références externes :** voir [les sources citées](../09-sources-externes-citees.md)
