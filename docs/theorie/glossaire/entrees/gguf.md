<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# GGUF (GPT-Generated Unified Format)

> **TL;DR — GGUF (GPT-Generated Unified Format).** Format de fichier des modèles : un en-tête de métadonnées (architecture, couches, tokenizer, hyper-paramètres) suivi des tenseurs de poids, chacun avec son type de quantification. Le moteur le lit **en place**, en plusieurs fichiers (multi-shards) ou en clusters (`drave-core/src/gguf.rs`, `Gguf::open_multi`).
>
> **Ce que c'est, en clair.** Définition complète dans la famille.
>
> **Famille :** [3. Formats, quantification, encodage](../03-formats-quantification-encodage.md) · **Index :** [toutes les entrées](../README.md)
> · **Définition complète :** [la famille](../03-formats-quantification-encodage.md)
>
> **Références externes :** voir [les sources citées](../09-sources-externes-citees.md)
