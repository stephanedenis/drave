> Campagne : **toutes-langues** · expérience **R**
> Titre : C.2 Le protocole exigé, et où il est fourni
> Date réelle : **2026-10-07 08:35 HAE** (source : commit `32ed5db`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## C.2 Le protocole exigé, et où il est fourni

> *« chaque affirmation porte sa mesure : fidélité d'entraînement, fidélité de TEST,
> invariance inter-langue, pire paire, TAILLE du réseau, avec le diagnostic oracle sur les
> deux panneaux (test hors vivier et validation du même vivier) »*

**Le bloc complet, produit en une commande** (`tools/profil_langues.py`, §41) :

```
TAILLE DU RÉSEAU : 147 neurones · 1 couche · 2 496 caractéristiques
fidélité apprentissage                    0,6464
fidélité VALIDATION (même vivier)         0,6312
fidélité TEST (hors vivier)               0,6299   (constante témoin 0,5762)
apport propre                            +0,0537
invariance inter-langue                   0,8958
pire paire                                0,6392
oracle TEST                               0,6721  -> écart +0,0415
oracle VALIDATION                         0,6504  -> écart +0,0194
```

**Ce bloc a été produit pour la couche 10 ET pour la couche 8, sur les 392 langues, à code
identique** (§44) — c'est ce qui rend la comparaison des deux cibles légitime.
