<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Contrat d'activation (Act)

> **Fiche glossaire — Contrat d'activation (Act).** L'ensemble des réglages qui changent les chiffres calculés : niveaux de quantification, seuil, top-k, renormalisation, et les sept top-k par projection, plus `attn_topk`, `qk_topk`, `moe_topk`. Ils **voyagent dans l'en-tête** parce que sans eux le pair distant ne calculerait pas la même chose — et « le client impose les siens au serveur » (`docs/format-flux.md:100-109`, `:187`).
>
> **Famille :** [5. Flux, protocole et transport](../05-flux-protocole-et-transport.md) · **Index :** [toutes les entrées](../README.md)
>
> **Définition complète :** [la famille](../05-flux-protocole-et-transport.md)
