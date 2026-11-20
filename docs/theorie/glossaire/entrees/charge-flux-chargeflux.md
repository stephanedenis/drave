<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Charge · Flux · ChargeFlux

> **TL;DR — Charge · Flux · ChargeFlux.** Structures internes du protocole : `ChargeFlux::Dense(Vec<f32>)` porte un vecteur, `ChargeFlux::Liste(...)` une liste quantifiée, `ChargeFlux::Lot(Vec<f32>)` un lot d'états aplati. `plat()` rend le vecteur plat d'un lot ; `en_dense()` panique nommément sur un lot, pour qu'on n'appelle pas la mauvaise conversion (`drave-core/src/main.rs`, `docs/plan-prefill-reparti.md:116-126`).
>
> **Ce que c'est, en clair.** Définition complète dans la famille.
>
> **Famille :** [4. Le moteur Drave : exécution, structures, outils](../04-le-moteur-drave-execution-structures-out.md) · **Index :** [toutes les entrées](../README.md)
> · **Définition complète :** [la famille](../04-le-moteur-drave-execution-structures-out.md)
>
> **Références externes :** voir [les sources citées](../09-sources-externes-citees.md)
