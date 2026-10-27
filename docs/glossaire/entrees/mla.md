<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# MLA (Multi-head Latent Attention ; attention latente multi-têtes)

> **Fiche glossaire — MLA (Multi-head Latent Attention ; attention latente multi-têtes).** Variante d'attention qui ne stocke qu'un **latent** par jeton (une petite dizaine de valeurs) et reconstruit clés et valeurs à la lecture ; le cache KV devient ~50× plus petit. Validée contre numpy à 5,2e-7 et contre llama.cpp à 0,999024 sur GLM-5.3 (`docs/plan-mla-vision.md:8-90`, `reports/rapport-mla-experts.md`).
>
> **Famille :** [2. Modèles et architectures](../02-modeles-et-architectures.md) · **Index :** [toutes les entrées](../README.md)
>
> **Définition complète :** [la famille](../02-modeles-et-architectures.md)
