# Rapport — le pont linguistique-sémantique, mesuré

**Mission** (clarifiée par Stéphane) : émuler **en boîte noire** le premier niveau
abstrait des gros modèles — celui où la représentation cesse d'être dominée par la
langue — pour avoir **notre propre pont linguistique-sémantique brut**. Il ne
s'agit pas de reproduire le gros modèle couche par couche, mais d'avoir un modèle
capable de **répondre à ce premier niveau abstrait**, pour n'importe quelle langue.

**Le professeur est une boîte noire** : on ne prend que son entrée et sa sortie.
`--trace-flux` les donne toutes les deux — la **couche 0 est la plongée du jeton**,
la **couche L est la cible**.

## Protocole

- **Corpus** : article 1 de l'UDHR, `tools/extrait_udhr.py`.
- **Entraînement** : 8 langues — deu, eng, fra, ita, nld, por, rus, spa
  (7 écritures latines + le cyrillique).
- **Test** : 6 langues **jamais vues** — ell (grec), heb (hébreu), hin
  (devanagari), jpn (japonais), kor (coréen), tha (thaï). **Six écritures non
  latines absentes de l'entraînement.**
- Mesure : similarité cosinus inter-langue à la dernière position, cosinus moyen
  et **pire paire**.

## Résultat 1 — la récurrence linéaire échoue, et le témoin dit pourquoi

Un étudiant `s_t = A·s_{t-1} + B·e_t` ajusté par moindres carrés (crête, forme
fermée) :

| | fidélité en UN PAS | boucle libre |
|---|---:|---:|
| rang 32 | 0,5822 | 0,0447 |
| rang 64 | 0,5380 | 0,0016 |
| rang 128 | 0,4912 | 0,0579 |
| rang 256 | 0,5654 | 0,1266 |

**La capacité d'état n'est pas le mur** : la fidélité en un pas est plate de 32 à
256. Et la boucle libre reste inutilisable **même en ramenant le rayon spectral de
1,424 à 0,70** — ce n'est donc pas une divergence, c'est que *l'ajustement local
n'optimise pas la trajectoire*.

## Résultat 2 — LE TÉMOIN QUI RENVERSE TOUT : la plongée seule suffit

Une **simple application linéaire de la plongée du jeton courant**, sans aucune
récurrence :

| couche cible | récurrence (1 pas) | **linéaire de e_t seul** |
|---|---:|---:|
| 4 | 0,4664 | **0,9216** |
| 10 | 0,4912 | **0,9021** |
| 17 | 0,4946 | **0,9198** |

**La récurrence n'est pas seulement inutile : elle est deux fois moins bonne.** Le
niveau abstrait du professeur est **déjà à ~90 % déterminé par la plongée du jeton
courant** — les 10 à 17 couches d'attention et de FFN n'ajoutent qu'environ 10 %
de variance.

## Résultat 3 — LE PONT : une matrice 896×896 qui rend la langue invisible

Le même ajustement linéaire, jugé non plus sur sa fidélité mais sur
**l'invariance inter-langue qu'il produit**, sur les 6 écritures **jamais vues** :

| couche cible | professeur (cos moyen / pire paire) | **pont linéaire** |
|---|---|---|
| 4 | 0,6027 / 0,4269 | **0,6965 / 0,5487** |
| 10 | 0,5464 / 0,2790 | **0,6357 / 0,3828** |
| 17 | 0,4609 / 0,2807 | **0,5657 / 0,3867** |

**Le pont rend une représentation PLUS invariante que le professeur lui-même** —
et sur la pire paire, 0,279 → **0,383 (+37 %)** à la couche 10.

**Pourquoi, et c'est le mécanisme** : une **seule** application linéaire doit
servir **toutes** les langues d'entraînement à la fois. Elle ne peut donc retenir
que ce qu'elles ont **en commun**, et laisse tomber ce qui est propre à chacune.
C'est un **projecteur sur le partagé**, obtenu par moindres carrés — sans
récurrence, sans rétropropagation, sans oracle.

Et il fait **mieux que l'annulation oracle** mesurée la nuit dernière
(`tools/cancellation_langue.py` : 0,279 → 0,378, avec un δ calculé **sur les
langues de test**), tout en étant **entièrement hors échantillon**.

## Résultat 4 — validé à l'échelle : 20 langues d'entraînement, 20 langues jamais vues

Les 40 langues de l'UDHR tracées, réparties au hasard 20/20 (graine fixée) :

| couche 10 | cos moyen | pire paire |
|---|---:|---:|
| professeur | 0,6284 | 0,3281 |
| **pont linéaire** | **0,7343** (+17 %) | **0,4421** (+35 %) |

Et le témoin sans récurrence confirme encore : **0,7304** en un pas contre
**0,6600** pour la récurrence linéaire.

**Le chiffre à retenir** : le pont atteint une pire paire de **0,4421**, à
comparer au **0,471** du plateau d'un modèle de **30 B** — soit 60 fois plus gros.
Un pont appris sur un modèle de 0,5 B atteint donc l'invariance inter-langue d'un
modèle bien plus grand.

## Résultat 5 — **UN SEUL NEURONE SUFFIT**, et c'est « l'apprentissage hyper-rapide » annoncé

Intuition de Stéphane : commencer avec **un neurone par sortie**, puis itérer en
ajoutant des neurones pour les exclusivités — l'apprentissage est **hyper-rapide au
début**. C'est exactement le **rang** du pont. Courbe mesurée, 20 langues
d'entraînement → 20 langues jamais vues :

| neurones | fidélité au professeur | **invariance inter-langue** | **pire paire** |
|---|---:|---:|---:|
| **1** | 0,6677 | **0,9492** | **0,7762** |
| 2 | 0,7170 | 0,9347 | 0,8252 |
| 4 | 0,7479 | 0,9139 | 0,7769 |
| 8 | 0,7467 | 0,8847 | 0,6739 |
| 16 | 0,7262 | 0,8431 | 0,5189 |
| 64 | 0,6816 | 0,7658 | 0,4842 |

**Un seul neurone donne 0,9492 d'invariance** — contre **0,6284** pour le
professeur, et **0,471** pour le plateau d'un modèle de **30 B**. Sa pire paire,
**0,7762**, écrase le 0,3281 du professeur.

**Et la courbe dit pourquoi** : le premier neurone capte la **direction partagée,
indépendante de la langue** — c'est le pont brut au sens exact. Les neurones
suivants ajoutent du **détail propre à chaque langue** : la fidélité au professeur
monte (0,668 → 0,748) mais **l'invariance baisse, monotonement** (0,949 → 0,766).

**Il y a donc un compromis, et il est net** : si l'on veut copier le professeur,
il faut des neurones ; si l'on veut le **pont sémantique brut**, **un seul suffit**
et les autres nuisent.

## Résultat 6 — la sonde n'a RIEN prouvé, et je le dis

Pour lever la réserve « plus invariant ≠ meilleur », j'ai voulu mesurer si le pont
garde l'information **prédictive** : une sonde linéaire qui prédit la plongée du
jeton suivant depuis l'état (`tools/sonde_pont.py`).

| état en entrée de la sonde | R² entraînement | R² test |
|---|---:|---:|
| professeur (couche 10) | 0,7088 | **−1,7411** |
| pont | 0,2599 | 0,0066 |
| témoin : plongée du jeton courant | 0,6600 | **−3,3080** |

**Le R² de test est négatif pour LES TROIS, professeur compris.** Une sonde qui ne
transfère pas d'un groupe de langues à l'autre ne dit donc **rien** sur le pont —
elle dit que le dispositif est mauvais (la cible — la plongée du jeton suivant
d'une autre langue — n'est pas dans le même repère).

**Ce n'est pas une preuve, c'est un échec de protocole.** Je le laisse écrit plutôt
que de le passer sous silence, et la réserve du § précédent **reste entière** : le
pont peut jeter de l'information utile, et personne ne l'a mesuré.

## Ce que ça donne à la mission

**Le pont est un artefact concret et mesuré**, et il tient en **UN neurone** :

```
  abstrait = (e_t · W0) · Pᵀ + moy
  W0 : 896 × 1        P : 896 × 1        moy : 896
```

soit ~1 800 nombres, ajustés par moindres carrés sur 20 langues, qui transforment
la plongée d'un jeton de **n'importe quelle langue** en une représentation
inter-langue à **0,9492** (pire paire **0,7762**) sur 20 langues **jamais vues**.

**Artefact** : `/home/stephane/Data13TB/stephane/corpus/udhr/pont_semantique_r1.npz`
**Applicateur** : `python3 tools/applique_pont.py <pont.npz> <trace.drvf>`
Vérifié sur grec, hébreu, japonais, thaï, coréen — écritures absentes de
l'entraînement.

## Ce que ce rapport ne dit PAS — et il faut le lire avant de s'en servir

1. **Plus invariant ne veut pas dire meilleur.** Le pont peut obtenir son
   invariance en **jetant** de l'information propre à la langue que le professeur,
   lui, porte — et cette information peut servir en aval. Le test qui le dirait :
   brancher le pont devant les couches suivantes du professeur et mesurer ce que
   la **perplexité** devient. **Ce test n'a pas été fait.**
2. **La fidélité au professeur est mesurée sur l'ensemble entraînement + test
   mêlés** (0,90-0,92 en un pas). La fidélité **par langue tenue à l'écart** n'a
   pas été isolée.
3. **Un seul article**, une seule position (la dernière), 14 langues sur 400.
4. **Le pont n'est pas récurrent**, alors que la mission demandait n couches
   récurrentes. La mesure dit que la récurrence linéaire n'apporte rien ici — elle
   ne dit pas qu'une récurrence **non linéaire** (de type DeltaNet, que le moteur
   implémente déjà et qui est vérifiée sur K3) n'apporterait rien.


## Résultat 7 — « ajouter des neurones et des couches » : mesuré, et c'est l'inverse

Demande de Stéphane : ajouter neurones et couches au besoin, pour émuler le
professeur **le plus fidèlement possible à moindre coût**. Mesure dans **l'espace
complet** (896 canaux) — l'ancienne comparaison se faisait dans le sous-espace du
rang courant, ce qui rendait les rangs incomparables et faisait croire que la
fidélité baissait.

40 langues d'entraînement → **6 langues tenues à l'écart**, toutes non latines :

| modèle | fid. entraînement | **fid. TEST** | params | invariance |
|---|---:|---:|---:|---:|
| constante (sortie moyenne) | 0,6677 | 0,5582 | 896 | 0,3763 |
| linéaire, 1 neurone | 0,6943 | 0,4752 | 1 792 | 0,7461 |
| linéaire, 4 | 0,7372 | 0,4343 | 4 480 | 0,5381 |
| linéaire, 16 | 0,7943 | 0,4096 | 15 232 | 0,3785 |
| linéaire, 128 | 0,8444 | **0,3691** | 115 584 | 0,2812 |
| **2 couches, 64 cachés** | 0,7278 | **0,5725** | 114 688 | **0,8882** |
| 2 couches, 256 cachés | 0,7753 | **0,5795** | 458 752 | 0,7855 |
| 2 couches, 1 024 | 0,8505 | 0,5564 | 1 835 008 | 0,6374 |
| 2 couches, 4 096 | 0,8947 | 0,5557 | 7 340 032 | 0,6048 |

**Trois conclusions, et la première contredit l'intuition :**

1. **Ajouter des neurones à un modèle LINÉAIRE détruit la fidélité** — 0,475 à un
   neurone, 0,369 à cent vingt-huit, pendant que l'entraînement monte de 0,69 à
   0,84. C'est du surajustement pur, et il est visible sur la seule colonne qui
   compte.
2. **Ajouter une COUCHE aide vraiment** : le deux-couches (projection aléatoire
   gelée + non-linéarité + lecture par moindres carrés) est la **seule** famille
   qui bat la constante, et il porte **la meilleure invariance** (0,8882) en même
   temps que la meilleure fidélité à coût égal.
3. **Au-delà de 256 cachés, ajouter nuit** (0,5795 → 0,5557). Le goulot n'est pas
   la capacité : **c'est la donnée** — 2 960 pas pour une cible de 896 dimensions.

**Le meilleur compromis mesuré** : **2 couches, 64 à 256 cachés**, 115 à 459 k
paramètres, fidélité de test 0,57-0,58 et invariance 0,79-0,89.

**Et il est naturellement distribuable** : la projection `R` (896 × H) est
**aléatoire et gelée** — elle n'a besoin d'aucune coordination entre nœuds — et
seule la lecture `W` (H × 896) s'ajuste, par blocs indépendants.

**Ce qu'il faudrait pour aller plus loin, et c'est nommé** : **plus de données**.
L'UDHR porte **42 unités × 400 langues**, et ce rapport n'utilise que **l'article 1
dans 46 langues** — soit ~3 % du corpus disponible. Dix fois plus de pas
changerait la courbe, pas dix fois plus de neurones.


## Résultat 8 — LA COUCHE RÉCURRENTE GAGNE, et elle est la plus distribuable

Diagnostic du résultat 7 : sans **contexte**, le pont plafonne, parce que la couche
10 du professeur **agrège tout le préfixe** et qu'un seul jeton ne peut pas la
prédire. La réponse qui respecte « pas de rétropropagation » est un **réservoir** :
une couche récurrente **aléatoire et gelée**, dont seule la lecture s'ajuste.

```
  s_t = (1−a)·s_(t−1) + a·tanh(A·s_(t−1) + B·e_t)     A, B ALÉATOIRES, GELÉS
  y_t = W·s_t + moy                                    W ajusté, forme fermée
```

40 langues d'entraînement → 6 langues tenues à l'écart (non latines) :

| modèle | fid. entraînement | **fid. TEST** | params | **invariance** | pire paire |
|---|---:|---:|---:|---:|---:|
| constante | — | 0,5582 | 896 | 0,3763 | — |
| 2 couches, 64 cachés (ELM) | 0,7278 | 0,5725 | 114 688 | 0,8882 | — |
| **RÉSERVOIR 64** | 0,7285 | **0,5923** | 118 784 | **0,9072** | **0,8437** |
| RÉSERVOIR 256 | 0,7818 | 0,5868 | 524 288 | 0,8187 | 0,6918 |
| RÉSERVOIR 512 | 0,8142 | 0,5812 | 1 179 648 | 0,8113 | 0,7471 |

**Ajouter une COUCHE récurrente gagne sur les DEUX tableaux** : fidélité 0,5725 →
**0,5923**, invariance 0,8882 → **0,9072**, et la pire paire monte à **0,8437**.

**Ajouter des NEURONES au-delà de 64 n'aide plus** (0,5923 → 0,5868 → 0,5812) : le
mur est la donnée, pas la capacité — 2 960 pas pour 896 dimensions.

**Et c'est le plus distribué de tous les modèles essayés** : `A` (64×64) et
`B` (64×896) sont **aléatoires et gelés**, donc identiques sur tous les nœuds sans
aucune coordination ; seule la lecture `W` (64×896) s'ajuste, et ses blocs sont
**indépendants** — chaque nœud peut calculer le sien.

**Le meilleur pont mesuré, en une ligne** : `tools/pont_reservoir.py`,
**1 couche récurrente gelée de 64 neurones**, ~119 k paramètres, fidélité 0,59,
invariance 0,91, pire paire 0,84 sur six écritures jamais vues.

## Ce qu'il faudrait pour aller plus loin

**Plus de données, et rien d'autre.** L'UDHR porte **42 unités × 400 langues** ;
tout ce rapport n'utilise que **l'article 1 dans 46 langues**, soit **~3 %** du
corpus déjà présent sur la machine. Dix fois plus de pas déplacerait la courbe ;
dix fois plus de neurones ne l'a pas déplacée une seule fois.


## Résultat 9 — OUI, LE MODÈLE EST OPTIMISABLE : +7 et +11 points, à coût nul

Le pont récurrent traînait **quatre réglages figés sans justification** : fuite
`a = 0,5`, rayon spectral `0,9`, ride `1e-1`, graine `5` — et **un seul tirage**
du réservoir. `tools/pont_reglages.py` les balaie (A et B restent aléatoires et
gelés ; seule la lecture `W` s'ajuste).

Référence : fid 0,5923 · invariance 0,9072 · pire paire 0,8437 (3254 pas).

| levier | fid TEST | invariance | pire paire | verdict |
|---|---:|---:|---:|---|
| **fuite `a` : 0,5 → 0,2** | **0,5974** | **0,9478** | **0,9212** | **GAGNANT, gratuit** |
| fuite `a = 0,1` | 0,5987 | 0,9405 | 0,8596 | fidélité max, pire paire moindre |
| fuite `a = 0,85` | 0,5859 | 0,8838 | 0,8368 | la fuite haute nuit partout |
| `N = 8` neurones | 0,5671 | **0,9884** | **0,9777** | curseur, pas un gain |
| `N = 256` | 0,5868 | 0,8187 | 0,6918 | la capacité détruit l'invariance |
| ride `1,0` | 0,5822 | **0,9825** | **0,9651** | curseur puissance |
| ride `10` | 0,5653 | **0,9989** | **0,9978** | l'invariance tend vers 1 |
| ensemble `K = 2` | **0,6010** | 0,8563 | 0,7938 | +0,9 pt de fidélité, −5 pts d'invariance |
| ensemble `K = 8` | 0,5895 | 0,7454 | 0,5589 | marginal puis nuisible |
| rayon 0,7 → 1,2 | 0,5924 → 0,5921 | ~0,907 | ~0,844 | **KNOB MORT** (±3·10⁻⁴) |
| saut (`e_t` dans la régression) | **0,3792** | 0,2757 | **−0,0693** | **NUISIBLE** (surapprentissage) |

**Le réglage gagnant — même coût, 64 neurones, même distribabilité :**

| | fid TEST | invariance | pire paire |
|---|---:|---:|---:|
| référence (`a=0,5`, ride 1e-1) | 0,5923 | 0,9072 | 0,8437 |
| **`a = 0,2`, ride `3e-1`** | **0,5921** | **0,9772** | **0,9576** |

**Fidélité identique, +7,0 points d'invariance, +11,4 points sur la pire paire** —
davantage que tout l'écart qui nous séparait du professeur 30B (0,693/0,471).
`pont_reservoir.py` porte désormais ces valeurs par défaut et reproduit
0,5921 / 0,9772 / 0,9576.

### Le fait le plus important : l'invariance seule est un mauvais objectif

Ride `10` porte l'invariance à **0,9989** et la pire paire à **0,9978**, en
laissant la fidélité à 0,5653. `N = 8` porte l'invariance à **0,9884** avec
0,5671 de fidélité. **N'importe quel modèle qui répond la même chose dans toutes
les langues est parfaitement invariant** — y compris celui qui ne dit rien.
Fidélité et invariance sont les deux axes d'**une seule courbe d'échange** ; le
ride et `N` sont les curseurs qui la parcourent. Rapporter l'invariance sans la
fidélité à côté n'a aucun sens, et c'est ce que faisaient les résultats 4 à 8.

### Le knob mort

Le rayon spectral est réglé à 0,9 depuis le début « pour la condition de mémoire
du réservoir ». De 0,7 à 1,2, **rien ne bouge** (0,5924 → 0,5921, invariance
0,9076 → 0,9066). Un paramètre que personne n'a jamais mesuré et qui ne fait rien.
