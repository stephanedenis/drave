<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Engram

> **Fiche glossaire — Engram.** Table d'adresses creuse, adressée par hachage de n-grammes (motifs de 1 à 4 jetons) : le modèle y lit des rangées de mémoire externe plutôt que de recalculer. Dans V4.1, deux couches d'engram pèsent 203 Go sur 365,7 Go, mais une session de 10 000 jetons n'en touche que ~4,6 Mo — d'où l'intérêt du `mmap` (`docs/plan-deepseek41-complet.md:53`, `reports/rapport-empreinte-memoire.md:7-10`).
>
> **Famille :** [2. Modèles et architectures](../02-modeles-et-architectures.md) · **Index :** [toutes les entrées](../README.md)
>
> **Définition complète :** [la famille](../02-modeles-et-architectures.md)
