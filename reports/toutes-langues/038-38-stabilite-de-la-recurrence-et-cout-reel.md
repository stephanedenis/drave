> Campagne : **toutes-langues** · expérience **38**
> Titre : 38. Stabilité de la récurrence et coût réel d'une implémentation par événements
> Date réelle : **2026-10-06 11:58 HAE** (source : commit `1404bac`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 38. Stabilité de la récurrence et coût réel d'une implémentation par événements

Deux questions posées : la récursion peut-elle **osciller** (« épilepsie ») au lieu de
se stabiliser, et une implémentation **par événements** ferait-elle gagner du temps ?

### 38.1 Stabilité — mesurée, la crainte n'est pas réalisée

La récurrence `s_t = (1-a)·s_{t-1} + a·tanh(P·s_{t-1} + B·e_t)` a pour jacobien
`J = (1-a)·I + a·D·P` avec `D = diag(1 - tanh²)`. Son rayon spectral décide.

| a | rayon (D = I) | **rayon (D observé)** | max \|s\| | verdict |
|---:|---:|---:|---:|---|
| 0,05 | 0,997 | 0,989 | 1,000 | stable |
| **0,20 (valeur du pont)** | 0,991 | **0,944** | 1,000 | stable |
| 0,40 | 0,983 | 0,847 | 1,000 | stable |
| 0,80 | 0,973 | 0,436 | 1,000 | stable |
| 0,95 | 0,971 | 0,154 | 1,000 | stable |
| 1,20 | **1,436** | 0,200 | **1,500** | hors régime |

**Aucune oscillation jusqu'à a = 0,95.** Et le comportement est contre-intuitif mais
sain : **un `a` plus grand est PLUS stable**, parce qu'il sature davantage le `tanh`,
ce qui réduit `D` donc le gain de boucle. À a = 0,2 la marge est encore confortable
(rayon 0,944) mais c'est la plus faible de la plage utile — c'est le point à
surveiller si l'on augmente le gain d'entrée ou si l'on vient à ajuster `P`.

À a = 1,2 le rayon calculé avec `D = I` dépasse 1 et l'état sort de `[-1, 1]`
(max 1,5) : **la limite pratique est entre 0,95 et 1,2.**

### 38.2 Événements — la dynamique actuelle n'est PAS creuse, et c'est mesuré

« Événement » = `|s_t - s_{t-1}| > seuil`. Sur du corpus réel, 40 neurones :

| seuil | a = 0,2 | a = 0,8 |
|---:|---:|---:|
| 1e-6 | 99,9 % | 99,2 % |
| 1e-4 | **99,8 %** | 97,2 % |
| 1e-2 | 98,4 % | 90,4 % |
| neurones saturés (\|s\| > 0,99) | **0,6 %** | 14,8 % |

**Une implémentation par événements paierait 0,2 % de pas en moins à a = 0,2, et
2,8 % à a = 0,8.** Autrement dit : **rien.**

**La raison que j'avais écrite ici était FAUSSE, et la mesure la corrige.** J'avais
lu « 0,6 % de saturation » comme « la dynamique vit dans son régime linéaire ». C'est
une confusion entre deux choses différentes :

| | mesure |
|---|---:|
| argument du `tanh`, `\|B·e_t\|` | **moyenne 16,9 · max 126** |
| saturation de la SORTIE du `tanh` | quasi totale |
| état `\|s_t\|` (moyenne glissante) | moyenne **0,347** · > 0,99 seulement 0,6 % du temps |

Le `tanh` **sature donc presque toujours** : son argument vaut 16,9 en moyenne, très
au-delà de ±1. Ce que le « 0,6 % » mesurait, c'est l'**état**, qui est une moyenne
glissante `s_t = 0,8·s_{t-1} + 0,2·tanh(...)` de sorties essentiellement **binaires**
(±1). Une moyenne de ±1 qui se répond au hasard reste près de zéro.

**Le réservoir calcule donc une moyenne glissante de projections aléatoires binaires
de l'entrée.** C'est pour cela que :
- les événements sont inutiles — les sorties binaires basculent constamment, 99,8 %
  des neurones changent à chaque pas ;
- une lecture linéaire de l'entrée fait presque aussi bien (§29) — une moyenne de
  projections binaires est proche d'une fonctionnelle linéaire de l'entrée récente ;
- augmenter le gain ne change RIEN (mesuré de 1 à 16 : saturation 0,6 % → 0,8 %,
  fidélité identique à 1e-4) — **le `tanh` est déjà saturé à gain 1**, en ajouter ne
  peut donc rien changer.

**La conséquence est contre-intuitive et c'est une piste : le levier n'est pas
d'augmenter le gain, c'est de le BAISSER** — pour que le `tanh` cesse de saturer et
que chaque neurone transmette une information graduée au lieu d'un signe.

### 38.3 Ce que cela implique pour le passage aux impulsions

Le passage à un modèle à impulsions n'est donc **pas une optimisation de cette
dynamique** — c'en est un **changement**. Une impulsion est creuse *par
construction* : seuil, émission, remise à zéro. Pour que la parcimonie apparaisse, il
faut **pousser la dynamique en saturation**, c'est-à-dire augmenter le gain d'entrée
jusqu'à ce que les neurones basculent au lieu de dériver.

C'est mesurable, et c'est la mesure qui manque : **quel gain d'entrée donne quel taux
de saturation ?** Si `gain = 1` sature 0,6 % et que `gain = 8` en sature 60 %, alors
la porte des impulsions est ouverte et le coût par événement devient intéressant.
Tant que la saturation reste sous quelques pour cent, l'événementiel ne peut rien
apporter — et le dire maintenant évite une réécriture qui ne paierait pas.

### 38.4 Sur le nombre de couches

L'argument « un modèle récursif devrait avoir un nombre de couches inférieur ou égal
à un FFN » est **déjà soutenu par la mesure** : D (2 couches de 20) = 0,5979 contre A
(1 couche de 40) = 0,5972 — la profondeur n'achète rien à budget constant (§29.4). Le
pont tient dans **une** couche face aux 24 du professeur.


---
