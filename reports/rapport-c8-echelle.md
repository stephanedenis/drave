# C8 à l'échelle : la courbe monte encore, mais plus de capacité NUIT — la limite est la donnée

> Campagne : **cerveau** · expérience : la tête réflexe à l'échelle (plan § 6.9, « reste l'échelle »)
> Question : la tête réflexe de C8 lit un état de profondeur 16 et le rend au vocabulaire. Elle
> avait été mesurée à **7 et 30 morceaux** d'entraînement (202,17 → 84,99). Deux questions restaient :
> la qualité **continue-t-elle** de monter avec la donnée, et la limite est-elle la **donnée** ou la
> **capacité** de l'adaptateur ?
> Verdict : **la courbe monte encore, à rendements décroissants, et la capacité n'est PAS la
> limite.** Sur un morceau **jamais vu** : **1 032,58** (4 morceaux) · **369,22** (8) · **260,81**
> (15) · **179,59** (30) — soit **÷5,75** pour ×7,5 de données, et **÷1,4** par doublement en fin de
> courbe. Et à données **égales**, un adaptateur **non linéaire** (896→512→896, GELU) rend
> **376,01**, soit **2,1× PIRE** que le linéaire (179,59) : ajouter de la capacité dégrade.
> Date réelle : **2026-10-13, 09 h 33-10 h 10 HAE** (heure lue sur la machine)
> Protocole : `tools/c8_corpus.sh 33 1024 16` (33 morceaux de 1 024 jetons répartis dans tout le
> corpus, états de profondeur 16) puis `tools/c8_entrainer_tete.py` — entraînement sur les k
> **premiers** morceaux, **validation** sur m30+m31, **test** sur **m32** (jamais vu), 20 époques,
> graine 0, GPU (`gpu-env`, torch 2.11)

## 1. La courbe

| morceaux d'entraînement (k) | meilleure époque (validation) | perplexité **TEST** (morceau jamais vu) | écart au modèle complet (14,2342) |
|---:|---:|---:|---:|
| 4 | 8 | **1 032,5798** | ×72,5 |
| 8 | 4 | **369,2207** | ×25,9 |
| 15 | 4 | **260,8050** | ×18,3 |
| **30** | 2 | **179,5909** | **×12,6** |
| *(tête empruntée, chemin tronqué — pour mémoire)* | — | *449 500,6184* | *×31 580* |

*(les 33 morceaux couvrent le corpus de 85 625 jetons, un toutes les ~2 500 positions ; m32 est le
dernier, jamais vu à l'entraînement ni à la validation.)*

Ce que ça dit :

* **la donnée paie encore** : ÷5,75 de perplexité pour ×7,5 de morceaux, et la validation suit
  (906,89 → 405,45 → 243,97 → 185,11) — ce n'est donc pas un artefact du test ;
* **mais les rendements décroissent** : ×2 de données donnent ÷2,80 (4→8), puis ÷1,42 (8→15), puis
  ÷1,45 (15→30). La pente en loi de puissance est faible : ~k^(−0,5) ;
* **l'époque choisie s'effondre** (8 → 4 → 4 → 2) : plus de données, convergence plus rapide et
  moins de surapprentissage — l'adaptateur n'a que 896×896 paramètres ;
* **et la capacité n'est pas la limite** : le même entraînement avec une couche cachée de 512
  neurones (GELU) rend **376,01** au lieu de **179,59** — **2,1× pire**, avec la même donnée, la
  même graine et la même validation. Ajouter des paramètres ne remplace pas des exemples.

## 2. Ce que ça change pour C8

* **la voie « adaptateur sur un chemin gelé » ne rattrapera pas le modèle** : au rythme mesuré
  (÷1,4 par doublement), fermer l'écart de ×12,6 demanderait ~7 doublements, soit **~4 000
  morceaux** *(extrapolation : c'est une hypothèse, pas une mesure — la pente peut changer)* ;
* **le manque reste N4** — la qualité du **chemin court** lui-même. Un adaptateur linéaire sur
  16 couches gelées plafonne parce que l'information perdue n'est pas dans l'état, pas parce
  qu'il manque de paramètres ;
* **conséquence de dessin** : entraîner le chemin court (ou router la profondeur, `--routee`) est
  la seule voie qui reste pour C8 ; agrandir la tête est mesuré **contre-productif**.

## 2bis. La profondeur de sortie : le chemin court est LISIBLE, même très tôt

Même protocole, mêmes 33 morceaux, mêmes 30 morceaux d'entraînement — seule la **profondeur de
sortie** change (l'état lu par l'adaptateur) :

| profondeur de sortie (sur 24 couches) | tête **empruntée** (chemin tronqué) | tête **entraînée** (k = 30) | écart tête entraînée / modèle complet | ÷ par rapport à la profondeur double |
|---:|---:|---:|---:|---:|
| **4** | 24 656 438,5178 | **534,9072** | ×37,6 | ×2,0 |
| **8** | 4 481 378,8799 | **267,9833** | ×18,8 | ×1,5 |
| **16** | 449 500,6184 | **179,5909** | ×12,6 | — |

Ce que ça dit :

* **la tête empruntée s'effondre** quand on sort plus tôt : 24,7 M (profondeur 4) contre 449 k
  (profondeur 16), soit **×55** — et la chute est encore plus raide en dessous (÷5,5 puis ÷10 par
  doublement) ;
* **la tête entraînée, elle, décroît doucement** : 535 → 268 → 180, soit **×2,0 puis ×1,5 par
  doublement de profondeur** — une loi de puissance faible, pas un effondrement ;
* **donc l'état précoce EST lisible** : à profondeur 4 (un sixième du réseau), un lecteur entraîné
  rend 535 là où la tête du modèle rend 24,7 millions (÷46 000). L'information utile est déjà là ;
  ce qui manquait, c'est le **lecteur** ;
* conséquence de dessin : la **profondeur de sortie est un levier bon marché** dès lors que le
  lecteur est entraîné — c'est l'inverse de ce que dit la tête empruntée, et c'est la tête
  entraînée qui compte pour un chemin court **appris** (le manque N4).

## 2ter. Robustesse : la graine ne change rien, le morceau de test change TOUT

Deux contrôles sur la même configuration (k = 30, validation m30+m31) :

| contrôle | perplexité TEST |
|---|---:|
| test sur **m32**, graine **0** | 179,5909 |
| test sur **m32**, graine **1** | **178,3852** (−0,7 %) |
| test sur **m20** (autre morceau jamais vu), graine 0 | **17,3503** |

* **la graine ne pèse rien** : 178,39 contre 179,59, soit **0,7 %** — les écarts de la courbe
  (÷1,4 par doublement) sont donc **très au-dessus** du bruit d'initialisation, et la courbe du § 1
  tient ;
* **le morceau de test pèse tout** : 17,35 sur m20 contre 179,59 sur m32, pour le **même**
  entraînement — un facteur **10**. Les morceaux du corpus n'ont pas la même difficulté (la tête
  empruntée le dit aussi : 147 k à 4,5 M selon le morceau) ;
* **conséquence de lecture** : la courbe du § 1 est une courbe **à morceau de test fixé** (m32, le
  plus difficile des deux mesurés), et ses valeurs **absolues** ne se transposent pas d'un texte à
  l'autre. Ce qui se transpose, c'est la **tendance** ; une loi chiffrée demanderait une moyenne
  sur plusieurs morceaux de test — ce n'est pas fait ici, et c'est écrit.

## 3. Ce que cette fiche ne dit pas

* elle ne sépare pas **quantité** et **diversité** : les k premiers morceaux sont des textes
  *différents* (c'est voulu), mais leur position dans le corpus varie aussi avec k — un tirage
  aléatoire de k morceaux donnerait la même tendance ou non, ce n'est pas mesuré ici ;
* elle ne dit rien du **chemin court entraîné** (N4) : c'est justement ce qu'elle désigne comme la
  suite ;
* la pente (~k^(−0,5)) est mesurée sur quatre points, **une seule graine** (mais le contrôle de
  graine du § 2ter montre qu'elle pèse 0,7 %) et **un seul morceau de test** (et le même contrôle
  montre que le morceau, lui, pèse ×10) : assez pour dire « ça monte encore, lentement », pas assez
  pour une loi.
