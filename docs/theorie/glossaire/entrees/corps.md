<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Corps (payload) · en-tête

> **Fiche glossaire — Corps (payload) · en-tête.** Un message de flux = un **en-tête** de taille fixe (79 octets en v5, `TAILLE_TETE`, verrouillé par `assert_eq!`) suivi d'un **corps** variable. L'en-tête porte la magie, la version, le mode, la plage de couches, la position, le compte `n`, l'échelle et le contrat d'activation ; le corps porte les données du mode (`docs/implantation/format-flux.md:88-116`, `docs/plan-mode4-lot-listes.md:54-55`).
>
> **Famille :** [5. Flux, protocole et transport](../05-flux-protocole-et-transport.md) · **Index :** [toutes les entrées](../README.md)
>
> **Définition complète :** [la famille](../05-flux-protocole-et-transport.md)
