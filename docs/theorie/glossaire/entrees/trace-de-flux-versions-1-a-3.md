<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Trace de flux, versions 1 à 3

> **Fiche glossaire — Trace de flux, versions 1 à 3.** V1 : indices `u32` + valeurs `i16` (6,02 octets par neurone actif) ; v2 : indices par écarts `u8` + valeurs `i16` (3,01 octets, sans perte, **défaut**) ; v3 : valeurs `i8` + échelle `f16` par bloc de 32 (≈2,08 octets pour 21 630 645 actifs, avec perte, `DRAVE_TRACE_BLOCS=1`). Le rejeu par lots n'accepte pas la v3, et le dit…
>
> **Famille :** [5. Flux, protocole et transport](../05-flux-protocole-et-transport.md) · **Index :** [toutes les entrées](../README.md)
>
> **Définition complète :** [la famille](../05-flux-protocole-et-transport.md)
