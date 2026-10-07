# Le cycle rapide : l'article 1 de l'UDHR dans 399 langues

> 07/10. Réponse à une demande précise : *« peut-on refaire nos exercices sur un
> très petit modèle afin de faire des cycles de tests plus rapides entre les
> couches d'entrée et première couche sémantique ? »*
>
> La réponse est oui, mais **le modèle n'est pas le bon levier** — et c'est
> mesuré, pas supposé.

---

## 1. D'où venait la lenteur, chiffres en main

| poste | ce qui coûtait |
|---|---|
| traçage d'une entrée | **~16 s** sur Wikipedia (un article entier, `ctx 1024`, 9 couches) |
| taille d'une entrée | **~575 positions** (l'article entier, moyenné) |
| ajustement d'un pont | **5 à 10 min** sur 1 446 entrées × 575 positions, parce que la Grammaire `AᵀA` coûte `n·d²` avec `d = 1 792` |

Le coût d'un ajustement est en `n · d²` : **n** = nombre total de positions,
**d** = 2 × dimension cachée. Les deux termes sont attaquables, mais pas au même
prix :

- **diviser `d` par 1,5** (un modèle de 576 cachés au lieu de 896) gagne **×2,4** ;
- **diviser `n` par 20** (une phrase au lieu d'un article) gagne **×20**.

C'est le second qui décide, et il ne demande aucun modèle nouveau.

## 2. Le corpus : l'article 1, pas l'article entier

L'unité d'alignement la plus solide de l'UDHR n'est pas l'article — c'est
**l'article 1**, présent dans toutes les langues, qui dit exactement la même chose
partout, et qui tient en une phrase.

**Ce que `tools/extrait_article1.py` produit** (`udhr_xml/`, 456 fichiers) :

| propriété | valeur |
|---|---|
| fichiers XML | 456 |
| **codes `iso639-3` distincts** | **400** |
| écritures écrasées | **56** — deux fichiers de même code s'écrasent (`und` en porte cinq) |
| langues avec un article 1 exploitable | **399** |
| longueur médiane | **169 caractères** (min 40, max 609) |
| positions par trace | **33 à 176** selon la langue |

Le point à retenir : **456 fichiers ne font pas 456 langues.** Le script comptait
les écritures ; il compte maintenant les codes, et dit les écrasements.

**Un second article est extrait** (`--article 2`, 399 langues aussi, médiane
541 caractères) parce que sans lui, « sémantique » ne veut rien dire : voir §4.

## 3. Le mode de traçage : la vraie économie cachée

Le mode par défaut du moteur construit ses listes d'événements **au chargement** :
sur Qwen2.5-0.5B, **15,6 M d'événements pour ~6 s**, à chaque invocation. Le
calcul par jeton, lui, est identique :

| mode | ms/jeton (mesuré) | temps total d'une trace |
|---|---:|---:|
| défaut (événementiel) | 32,4 | **8,00 s** |
| **`--dense`** | 32,3 | **1,94 s** |

**Même calcul, 6 s de moins par invocation.** Sur 399 langues tracées une par
une, ces 6 secondes fixes font **40 minutes**.

**Mais changer de mode sans le mesurer rendrait le nouveau corpus incomparable à
tout ce que ce dépôt a tracé.** La calibration a donc été faite
(`tools/calibre_modes.py`, 8 langues, 4 écritures) :

| | valeur |
|---|---:|
| cosinus **moyen** entre les deux modes | **0,9964** |
| cosinus **minimum** | 0,9160 |
| 5ᵉ centile | 0,9924 |
| rapport des normes | **1,000** |

**Verdict** : les deux modes tracent la même direction à 0,4 % près en moyenne,
8 % au pire, et à la même amplitude. Un corpus tracé en dense est donc comparable
à un corpus tracé en événementiel — **à condition de le dire**, ce qui est fait
ici.

## 4. La mesure que ce corpus rend possible : la première couche sémantique

Un chiffre qui monte ne prouve rien. La similarité entre les représentations d'une
même phrase dans 399 langues monte avec la profondeur — mais elle monterait aussi
si la couche devenait simplement **anisotrope**, c'est-à-dire si tous les vecteurs
se ressemblaient sans rien savoir du sens.

D'où **deux articles**, et une différence :

    même(c)    = cos( art1 langue i , art1 langue j )      i ≠ j
    autre(c)   = cos( art1 langue i , art2 langue j )      i ≠ j
    SÉPARATION = même(c) − autre(c)

`autre(c)` est le **plancher d'anisotropie** : ce que la couche fait ressembler
sans rien savoir du sens. La couche où la séparation culmine est la **première
couche sémantique** — celle où le modèle a fini de traduire et commence à
raisonner. C'est la cible naturelle d'un pont.

`tools/premiere_couche_semantique.py` la mesure **avec les deux poolings**
(moyenne des positions et dernière position), parce que le §84 du rapport
`rapport-toutes-langues.md` a montré qu'ils ne racontent pas la même histoire —
1,769 contre 6,275 sur le même corpus. S'ils s'accordent ici, la conclusion sera
solide ; s'ils divergent, c'est le pooling qu'il faudra interroger avant la
couche.

## 5. Ce que le cycle coûte maintenant

| étape | avant | après |
|---|---:|---:|
| traçage d'une langue | ~16 s | **3,7 s** |
| traçage du corpus entier | 2 h 30 (300 traces) | **~25 min** (399 langues) |
| positions par entrée | ~575 | **~60** |
| lignes dans la Grammaire d'ajustement | 147 000 à 830 000 | **~24 000** |
| **ajustement d'un pont** | **5 à 10 min** | **~15 s** (projection) |

**Le traçage n'est pas 20× plus rapide — il est 4× plus rapide**, parce que le
chargement du modèle est un coût fixe qu'aucun corpus ne supprime. C'est
**l'ajustement** qui change d'échelle, et c'est lui qu'on répète.

## 6. Réserves

1. **Une phrase, c'est peu.** L'article 1 porte ~50 jetons ; les mesures de
   contenu par entrée y sont plus bruitées que sur un article entier. C'est le
   prix de la vitesse, et il se paie en répétant — 399 langues au lieu de 10.
2. **Le corpus dense n'est pas identique à l'ancien** (cos 0,9964). Toute
   comparaison entre un chiffre mesuré sur ce corpus et un chiffre mesuré sur les
   anciens doit porter cette réserve.
3. **`--dense` est un chemin différent**, pas seulement plus rapide : le moteur
   documente ailleurs un écart de +0,15 % de perplexité et une corrélation 0,9981
   contre la référence. La calibration ci-dessus le chiffre sur les traces.
4. **Le contexte est de 256 jetons** alors que l'article 2 atteint 1 705
   caractères : les plus longs sont tronqués. Le dire, et le vérifier le jour où
   une langue longue portera une conclusion.
