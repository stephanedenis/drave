<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Aiguillage (dispatch)

> **TL;DR — Aiguillage (dispatch).** Choix du noyau selon le format du tenseur (Q4_0, Q8_0, MXFP4, i-quant…), qui remplace un appel unique `matvec_q4`. Il évite de convertir et rend la lecture « en place » possible (`reports/rapport-mla-experts.md:98-99`).
>
> **Ce que c'est, en clair.** Définition complète dans la famille.
>
> **Famille :** [4. Le moteur Drave : exécution, structures, outils](../04-le-moteur-drave-execution-structures-out.md) · **Index :** [toutes les entrées](../README.md)
> · **Définition complète :** [la famille](../04-le-moteur-drave-execution-structures-out.md)
>
> **Références externes :** voir [les sources citées](../09-sources-externes-citees.md)
