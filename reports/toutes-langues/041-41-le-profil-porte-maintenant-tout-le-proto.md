> Campagne : **toutes-langues** · expérience **41**
> Titre : 41. Le profil porte maintenant TOUT le protocole — et il révèle un écart d'invariance
> Date réelle : **2026-10-06 12:36 HAE** (source : commit `b8e8f60`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 41. Le profil porte maintenant TOUT le protocole — et il révèle un écart d'invariance

`tools/profil_langues.py` rapporte désormais, en une seule exécution : **taille du
réseau**, **invariance inter-langue et pire paire** (professeur ET notre sortie),
**fidélité et apport sur le TEST hors vivier et sur la VALIDATION du même vivier**,
et **l'écart à l'oracle sur les deux panneaux**. C'est le protocole complet.

Couche 10, 40 neurones, 1 couche, 80 caractéristiques, 896 canaux, 41 langues de test
(mesure sur la **dernière position** du texte entier — le point de contenu que l'UDHR
aligne d'une langue à l'autre) :

| | professeur | notre sortie |
|---|---:|---:|
| invariance inter-langue | 0,6529 | **0,9565** |
| **pire paire** | **0,0478** | **0,7371** |

### 41.1 Nous sommes BEAUCOUP plus invariants que le professeur

L'écart est massif et il ne va pas dans le sens qu'on croit :

- la **pire paire** du professeur vaut **0,0478** — deux langues dont la
  représentation de couche 10 est quasi orthogonale ;
- la nôtre vaut **0,7371** — nous les rendons très semblables.

Notre sortie est donc **plus uniforme que sa cible**. Deux lectures, et je ne tranche
pas :

1. **C'est la mission.** Un pont linguistico-sémantique *veut* l'invariance : si deux
   langues disent la même chose, leurs représentations doivent se ressembler. Sous cet
   angle, 0,9565 est un succès et 0,0478 dit que le professeur, lui, garde énormément
   de marque linguistique à sa couche 10.
2. **C'est un excès de lissage.** Notre fidélité n'est que de 0,5960 : nous ne
   reproduisons pas la cible, nous en produisons une version plus pauvre et plus
   consensuelle. Une invariance obtenue en effaçant les différences n'est pas de
   l'invariance, c'est de l'appauvrissement.

**Ce qui manque pour trancher** : la même mesure sur un corpus où le CONTENU diffère
d'une langue à l'autre. Si notre invariance reste à 0,95 alors que les contenus sont
différents, c'est du lissage. Sur l'UDHR, où tout le monde dit la même chose, les deux
lectures sont indiscernables — et c'est une limite du corpus, pas de la mesure.

### 41.2 Note de méthode sur les périmètres

Ces 0,6529 / 0,9565 se mesurent au **dernier pas du texte entier**. Le §30 mesurait
0,6471 au niveau des **dix unités alignées**. Les deux valent ce qu'ils valent, mais
ils ne se comparent pas : même si les chiffres sont proches, le découpage diffère. Le
périmètre est nommé à chaque fois, comme il doit l'être.

### 41.3 Le profil complet, en un bloc

```
TAILLE DU RÉSEAU : 40 neurones · 1 couche [40] · 80 caractéristiques
INVARIANCE : professeur 0,6529 (pire 0,0478) · notre sortie 0,9565 (pire 0,7371)
TEST       (hors vivier) : fidélité 0,5960 · apport +0,0282 · oracle 0,6935
VALIDATION (même vivier) : fidélité 0,6206 · apport +0,0317 · oracle 0,6318
ÉCART À L'ORACLE : TEST +0,0975 · VALIDATION +0,0112
```

C'est ce bloc qui sera produit pour la couche 8 sur les 392 langues, et c'est lui qui
rendra la comparaison des deux cibles légitime — même code, même périmètre, mêmes
quatre mesures.


---
