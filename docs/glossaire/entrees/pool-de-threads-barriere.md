<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Pool de threads · barrière

> **Fiche glossaire — Pool de threads · barrière.** Le moteur parallélise ses projections sur un ensemble de fils synchronisés par une barrière atomique ; un jeton paie 168 barrières (7 matrices × 24 couches). C'est ce pool qui limite le débit : 5,3 G événements/s à 32 fils, effondrement au-delà (`reports/rapport-inference.md:88-94`, `reports/bilan-multi-materiel.md:54`).
>
> **Famille :** [4. Le moteur Drave : exécution, structures, outils](../04-le-moteur-drave-execution-structures-out.md) · **Index :** [toutes les entrées](../README.md)
>
> **Définition complète :** [la famille](../04-le-moteur-drave-execution-structures-out.md)
