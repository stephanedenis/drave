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

> **Rectification du 2026-10-14** — deux chiffres de cette fiche sont faux, et l'ancien est gardé à
> côté du nouveau (règle du dépôt). **(1) m20 n'était pas « jamais vu »** : aux runs à k = 30, la
> liste d'entraînement était construite par `seq 0 29`, donc `etat-m20` figurait **dans `--train`
> et dans `--test`** (commande du 13/10 retrouvée dans le journal de session). La fuite vaut
> **×8,0** à profondeur 8 et **×14,4** à profondeur 4 (mesuré le 14/10, même morceau, même
> protocole, même validation, avec et sans le morceau dans la liste). Conséquences : le « **×10**
> du morceau de test » (§ 2ter), la « **falaise ÷22,8** » de 15 à 30 morceaux (§ 2quinquies) et le
> rapport 8/16 « **×1,17** » mesuré sur m20 (§ 2quater) tombent ; **m32 est propre** (absent de
> toutes les listes) et la courbe de profondeur du § 2bis reste debout. **(2) « modèle complet
> (14,2342) » est un chiffre de CORPUS**, pas un chiffre de morceau : la moyenne géométrique des 33
> morceaux vaut 14,4283 (torch, fp32) et sur m32 le modèle complet rend **7,4242** (moteur) —
> l'écart du § 2bis est donc **×24,2**, pas ×12,6, et tous les rapports « ×N du modèle complet » de
> cette fiche sont deux fois trop optimistes. Détail et mesures :
> [`rapport-n4-dessin-b.md`](rapport-n4-dessin-b.md) § 4 et § 4bis.

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

| profondeur de sortie (sur 24 couches) | tête **empruntée** (chemin tronqué) | tête **entraînée** (k = 30) | écart tête entraînée / modèle complet | × par 4 couches de moins |
|---:|---:|---:|---:|---:|
| **4** | 24 656 438,5178 | **534,9072** | ×37,6 | ×2,00 |
| **8** | 4 481 378,8799 | **267,9833** | ×18,8 | ×1,30 |
| **12** | 2 632 689,6916 | **205,5773** | ×14,4 | ×1,14 |
| **16** | 449 500,6184 | **179,5909** | ×12,6 | — |

Ce que ça dit :

* **la tête empruntée s'effondre** quand on sort plus tôt : 24,7 M (profondeur 4) contre 449 k
  (profondeur 16), soit **×55** — et la chute est encore plus raide en dessous (÷5,5 puis ÷10 par
  doublement) ;
* **la tête entraînée, elle, décroît doucement** : 535 (4 couches) → 268 (8) → 206 (12) → 180 (16),
  soit **×2,00 · ×1,30 · ×1,14 par 4 couches** — la pénalité **s'accélère** quand on sort très tôt,
  mais elle reste loin de l'effondrement de la tête empruntée ;
* **donc l'état précoce EST lisible** : à profondeur 4 (un sixième du réseau), un lecteur entraîné
  rend 535 là où la tête du modèle rend 24,7 millions (÷46 000). L'information utile est déjà là ;
  ce qui manquait, c'est le **lecteur** ;
* conséquence de dessin : la **profondeur de sortie est un levier bon marché** dès lors que le
  lecteur est entraîné — c'est l'inverse de ce que dit la tête empruntée, et c'est la tête
  entraînée qui compte pour un chemin court **appris** (le manque N4).

## 2quater. Les deux leviers se multiplient (données × profondeur)

Même protocole, deux profondeurs de sortie, trois volumes de données :

| morceaux (k) | profondeur 16 (TEST) | profondeur 8 (TEST) | rapport 8/16 |
|---:|---:|---:|---:|
| 4 | 1 032,5798 | 1 745,5154 | ×1,69 |
| 15 | 260,8050 | 382,4743 | ×1,47 |
| 30 | 179,5909 | 267,9833 | ×1,49 |

* **le rapport est presque le même à 4, 15 et 30 morceaux** (×1,69 · ×1,47 · ×1,49) : les deux
  leviers — **données** et **profondeur** — agissent donc largement **indépendamment** et se
  multiplient ;
* **mais il dépend du TEXTE** : mesuré sur un second morceau de test (m20, jamais vu, le plus
  facile des deux), le rapport 8/16 tombe à **×1,17** (20,37 contre 17,35). Ma première version de
  cette fiche disait « ~×1,5 constant » : trop fort — le facteur va de **1,2 à 1,7** selon le
  morceau. La direction, elle, ne change pas ;
* **corollaire pratique** : on ne « rattrape » pas une sortie précoce avec plus de données (le
  rapport ne se referme pas quand k monte), et on n'économise pas de données en sortant plus tard.
  Le choix de la profondeur se fait donc sur le **coût** (couches sautées) — avec la réserve que le
  facteur exact dépend du texte (1,2 à 1,7) ;
* c'est cohérent avec le § 2bis : l'état précoce est **lisible** (le lecteur extrait l'essentiel),
  et ce qui manque à la sortie précoce est une **petite** partie de l'information — ×1,5, pas ×10.

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
  plus difficile des deux mesurés), et ni ses valeurs **absolues** ni sa **forme** ne se transposent
  d'un texte à l'autre (§ 2quinquies : ÷1,45 sur m32 contre ÷22,8 sur m20 pour le même doublement).
  Ce qui se transpose, c'est la **direction** (plus de données aide) ; une loi chiffrée demanderait une moyenne
  sur plusieurs morceaux de test — ce n'est pas fait ici, et c'est écrit.

## 2quinquies. La courbe elle-même ne se transporte pas d'un texte à l'autre

Le contrôle qui manquait, fait à la fin de la matinée : la **même** courbe de données, mesurée sur
le second morceau de test (m20) :

| morceaux (k) | TEST sur **m32** | TEST sur **m20** | rapport m20/m32 |
|---:|---:|---:|---:|
| 4 | 1 032,58 | 2 816,29 | ×2,73 |
| 15 | 260,81 | 396,37 | ×1,52 |
| 30 | 179,59 | **17,35** | **×0,10** |

* **la direction tient** : les deux textes s'améliorent de façon monotone avec la donnée — c'est le
  seul énoncé robuste de cette fiche ;
* **la FORME ne tient pas** : de 15 à 30 morceaux, m32 gagne **÷1,45** et m20 gagne **÷22,8** — un
  facteur 16 entre les deux textes pour le même doublement de données. Sur m20, la courbe a une
  **falaise** (le lecteur « prend » ce texte d'un coup) ; sur m32, une pente douce ;
* **donc aucune « loi » chiffrée ne peut être tirée d'un seul morceau de test** — et c'est
  exactement ce que le § 2ter annonçait (le morceau pèse ×10). Une loi demanderait une **moyenne
  sur plusieurs morceaux de test**, avec sa dispersion : ce n'est pas fait, et c'est écrit ici.

## 2septies. Un état précoce prédit-il un état profond ? Oui à 65 % — le reste est CRÉÉ

La question N4 (« entraîner le chemin court ») suppose que sortir tôt **perd** de l'information.
Demandé directement aux états : ce que la profondeur ajoute est-il **déjà dans l'état précoce**, ou
est-il **créé** par les couches intermédiaires ? Mesure : régression **ridge linéaire** d'une
profondeur vers une autre, sur les mêmes 33 morceaux (30 d'entraînement, 3 de test jamais vus),
30 600 positions × 896 canaux (`tools/predictibilite_etats.py`) :

| prédiction | R² TEST | contrôle : l'identité |
|---|---:|---:|
| profondeur **8 → 16** | **0,6547** | 0,1913 |
| profondeur **16 → 8** | **0,7226** | −0,4997 |
| profondeur 8 → 12 | **0,7825** | — |
| profondeur 12 → 16 | **0,7531** | — |

* **65 % de l'état profond est linéairement déterminé par l'état précoce** (contre 19 % pour
  l'identité) : la profondeur ne *crée* donc pas tout — un bon lecteur peut extraire beaucoup d'un
  état précoce, ce qui recoupe la courbe du § 2bis (×1,14 à ×2,00 par 4 couches) ;
* **mais les pas élémentaires sont MIEUX prédits que le saut direct** (0,78 et 0,75 contre 0,65) :
  si la composition était linéaire, le saut direct serait au moins aussi bon. Donc **~35 % de la
  variance profonde apparaît dans les couches intermédiaires** — c'est de l'information **créée**,
  et c'est exactement ce qu'un adaptateur sur un chemin gelé ne peut pas fabriquer ;
* **le sens inverse est encore plus prédictible** (0,72) : l'état précoce est mieux contenu dans le
  profond que l'inverse — la flèche du temps de l'information va bien de la profondeur vers la
  surface, pas l'inverse ;
* **conséquence pour N4** : entraîner le chemin court n'est pas un pis-aller, c'est le seul moyen
  d'obtenir les ~35 % que la profondeur fabrique. La note
  [`docs/note-chemin-court-n4.md`](../docs/note-chemin-court-n4.md) propose trois dessins ; cette
  mesure dit pourquoi le **B** (adaptateurs par couche) est le premier qui puisse marcher.

## 3. Ce que cette fiche ne dit pas

* elle ne sépare pas **quantité** et **diversité** : les k premiers morceaux sont des textes
  *différents* (c'est voulu), mais leur position dans le corpus varie aussi avec k — un tirage
  aléatoire de k morceaux donnerait la même tendance ou non, ce n'est pas mesuré ici ;
* elle ne dit rien du **chemin court entraîné** (N4) : le § 2septies dit seulement que ~35 % de
  l'état profond est **créé** par les couches intermédiaires — la suite est d'entraîner ces couches
  (dessin B de la note), pas d'adapter une sortie ;
* la pente (~k^(−0,5)) est mesurée sur quatre points, **une seule graine** (mais le contrôle de
  graine du § 2ter montre qu'elle pèse 0,7 %) et **un seul morceau de test** (et le même contrôle
  montre que le morceau, lui, pèse ×10) : assez pour dire « ça monte encore, lentement », pas assez
  pour une loi.
