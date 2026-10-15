# La sélection du rejeu — à volume égal, *ce qu'on rejoue* compte moins que *rejouer*

> Campagne : **cerveau** · expérience : le protocole de sommeil, deuxième question — après
> « combien rejouer » (`rapport-sommeil-budget.md`), **quoi** rejouer ?
> Question : à **volume égal** (3 morceaux, 3 072 jetons), la **règle de sélection** change-t-elle
> le gain ? Et l'intuition « rejouer ce qui a surpris » (les exemples difficiles) se vérifie-t-elle ?
> Verdict : **la règle pèse peu, et l'intuition est FAUSSE ici.** Sur un texte jamais rejoué (m32) :
> **hasard −6,49 %** · premiers −5,51 % · **surprise −4,82 %** · faciles −4,26 %. L'étendue des
> quatre règles est de **1,3 point**, à comparer aux **4,4 points** que donne le seul *volume*
> (3 → 20 morceaux) : **rejouer compte plus que choisir**. Et « rejouer les plus difficiles » est
> **deuxième en partant de la fin** — l'intuition pédagogique ne se transpose pas telle quelle.
> Date réelle : **2026-10-14 23 h 15-23 h 45 HAE** (heure lue sur la machine)
> Protocole : `tools/n4_dessin_b.py --objectif plein --rejeu <liste>` (nouveau : une liste
> **explicite** de morceaux) · 3 morceaux rejoués parmi les **vingt premiers** du corpus · LoRA
> rang 8 sur les 8 premières couches, 12 époques, époque choisie sur **m29** · test **m32** (jamais
> rejoué) · hors domaine : `data/corpus_en_val.txt` (1 024 jetons jamais rejoués) · graine 0.

## 1. Les quatre règles

| règle de sélection | morceaux rejoués | m32 (jamais rejoué) | écart | hors domaine | écart |
|---|---|---:|---:|---:|---:|
| **au hasard** (graine fixée) | m5, m12, m17 | 6,6611 | **−7,21 %** | 16,6747 | −0,35 % |
| **les premiers** (le défaut) | m0, m1, m2 | 6,7487 | −5,99 % | 16,7654 | +0,20 % |
| **par surprise** (les plus durs) | m13, m2, m7 | 6,8301 | −4,86 % | 16,6439 | −0,53 % |
| **les plus faciles** | m16, m0, m5 | 6,8869 | −4,06 % | 17,0787 | **+2,07 %** |

*(chiffres **refaits** avec le harnais reproductible — `rapport-consolidation-balayage.md` § 4bis :
les premiers, tirés avec un RNG non semé, donnaient −6,49 / −5,51 / −4,82 / −4,26 %. **L'ordre est
le même**, l'étendue passe de 2,2 à **3,15 points**, et l'écart hasard ↔ premiers de 1,0 à
**1,2 point**.)*

*la « surprise » est mesurée, pas supposée : la perplexité du modèle complet sur les vingt premiers
morceaux va de **7,38** (m5) à **25,91** (m13) — les trois plus durs sont m13, m2, m7, les trois
plus faciles m16, m0, m5.*

Ce que ça dit :

* **la règle pèse 1,3 point, le volume en pèse 4,4** : entre 3 et 20 morceaux rejoués, le gain passe
  de −5,57 % à −9,98 % (`rapport-sommeil-budget.md`) ; entre quatre règles de sélection, il va de
  −4,26 % à −6,49 %. **Rejouer beaucoup (ou souvent) bat bien choisir** — à cette échelle ;
* **l'intuition « les exemples difficiles » ne paie pas** : la sélection par surprise est **avant-
  dernière** (−4,82 %). Trois hypothèses, aucune mesurée ici : les morceaux durs sont durs
  *pour des raisons locales* (vocabulaire rare) qui ne se transfèrent pas ; l'objectif de
  consolidation est une **moyenne** sur le morceau, donc un texte dur pèse autant qu'un facile ; et
  trois morceaux ne font pas une politique ;
* **le hasard gagne, et c'est cohérent avec la diversité** : les trois morceaux tirés au hasard
  (m5, m12, m17) sont **répartis** dans le corpus, alors que « les premiers » sont voisins. C'est la
  seule règle qui **couvre** — et c'est aussi ce que la courbe du budget disait (le gain vient de
  la couverture, pas de la difficulté) ;
* **le hors-domaine ne bouge pas** : −0,53 % à +2,07 %, du bruit (±1,5 point) — sauf « les plus
  faciles », qui coûte **+2,07 %** : rejouer ce que le modèle sait déjà est le seul choix qui
  **dégrade ailleurs**, ce qui est cohérent avec « on ne consolide pas ce qu'on sait ».

## 1bis. La PROXIMITÉ temporelle ne compte pas non plus

Dernière règle de sélection essayée, et la plus « cognitive » : rejouer ce qui **précède
immédiatement** ce qu'on veut prédire. Le rejeu des **vingt derniers** morceaux (m12..m31, dont m31
est le voisin direct de m32) contre les **vingt premiers** (m0..m19) :

| rejeu (20 morceaux, 12 époques, graine 0) | m32 (jamais rejoué) | écart | hors domaine |
|---|---:|---:|---:|
| les **vingt premiers** (m0..m19) | 6,4622 | −9,98 % | +3,30 % |
| les **vingt derniers** (m12..**m31** — le voisin immédiat de m32) | **6,4097** | **−10,71 %** | +1,91 % |

* **0,7 point de mieux** pour le rejeu **adjacent** : c'est **dans le bruit** de ces bras (la graine
  pèse 0,14 point, le morceau de test ×10 sur les valeurs absolues). La proximité temporelle
  **n'apporte rien de mesurable** à ce volume — vingt morceaux du même corpus valent vingt morceaux,
  qu'ils précèdent ou non le texte mesuré ;
* c'est **cohérent avec les deux autres règles** : le hasard bat les premiers (−6,49 % contre
  −5,51 % sur 3 morceaux), la surprise perd (−4,82 %), et la proximité ne se distingue pas. Ce qui
  décide, c'est **le volume** — et le corpus, pas la position ;
* **et le hors-domaine confirme l'absence de tendance** : +3,30 % (premiers) contre +1,91 %
  (derniers) — deux mesures du même ordre, sans direction.

## 1ter. Le PREMIER critère qui tient : rejouer les morceaux RÉPÉTITIFS (sur un test, trois graines)

Les trois règles du § 1 et la proximité du § 1bis ne départageaient rien. Une quatrième a été
essayée, et elle **départage** — sur un des deux morceaux de test :

| lot de 5 morceaux (rang 4, 10 époques) | m32 | m20 |
|---|---|---|
| les plus **VARIÉS** (trigrammes distincts / jetons : 0,917 à 0,954) | −6,19 / −6,57 / −6,22 % *(graines 0/1/2, harnais d'avant)* | −9,70 / −10,97 / −10,94 % |
| les plus **RÉPÉTITIFS** (0,662 à 0,812) | −6,53 / −6,37 / −6,50 % | **−14,46 / −14,64 / −14,47 %** |
| **refaits avec le harnais EXACT** (§ 4bis) | variés **−6,78 %** · répétitifs **−7,85 %** | variés **−10,31 %** · répétitifs **−14,54 %** |

* **sur m20, l'écart est net et reproductible** : **−14,5 %** contre **−10,9 %**, soit **3,6 points**,
  avec une dispersion de graine de 1,3 point **à l'intérieur** de chaque bras — l'écart est **trois
  fois** la dispersion ;
* **sur m32, les deux lots étaient équivalents** (−6,2 à −6,6 %) — mais **refaits avec le harnais
  reproductible, les répétitifs y gagnent aussi** (−7,85 % contre −6,78 %, soit 1,1 point) : le
  critère se voit donc **sur les deux morceaux de test**, et plus fort qu'annoncé (4,2 points sur
  m20) ;
* **le critère est bon marché** : compter les trigrammes distincts d'un morceau coûte **quelques
  millisecondes**, sans le modèle — à comparer au tri par surprise, qui exigeait une passe complète
  sur les vingt morceaux… pour perdre ;
* **et le mécanisme est cohérent avec la fiche « structure partagée »** : un texte répétitif porte
  **plus de régularité par jeton** — il y a donc plus à consolider. Un texte très varié ressemble
  davantage à du bruit, et le rejeu n'y trouve rien de transférable. C'est une **hypothèse**, et
  elle est nommée comme telle ;
* **ce que ça ne prouve pas** : que le critère soit un **gradient**. La courbe du § 1quater (cinq
  lots, trois tests) montre un **seuil** : au-delà d'environ 0,9 trigramme distinct par jeton, le
  rejeu ne trouve plus rien ; en dessous, les lots se valent — et c'est le seuil, pas le tri, qui
  est établi.

## 1quater. La COURBE « diversité du lot → transfert » : un SEUIL, pas un gradient

La suite annoncée au § 1ter (« les deux lots sur quatre morceaux de test, et la courbe ») est faite :
**cinq lots de quatre morceaux** couvrant toute l'étendue de diversité, trois morceaux de test
(m20, m32, m30), rang 4, dix époques, graine 0.

| lot | diversité (trigrammes distincts / jetons) | m20 | m32 | m30 |
|---|---|---:|---:|---:|
| **Q1** plus répétitif | 0,662 – 0,829 | −11,20 % | −6,29 % | −6,11 % |
| **Q2** | 0,833 – 0,857 | −11,15 % | **−7,25 %** | −5,98 % |
| **Q3** médian | 0,859 – 0,874 | **−14,42 %** | −7,10 % | −3,71 % |
| **Q4** | 0,874 – 0,891 | −12,87 % | −7,05 % | **−6,60 %** |
| **Q5** plus varié | **0,917 – 0,954** | **−7,85 %** | **−4,96 %** | −5,41 % |

* **le lot le plus VARIÉ est le pire, et sur deux tests sur trois** : −7,85 % sur m20 (contre −11,2
  à −14,4 pour les quatre autres) et −4,96 % sur m32 (contre −6,3 à −7,3). L'écart avec le médian
  est de **6,6 points** sur m20 — bien au-dessus de toute dispersion mesurée cette nuit ;
* **mais entre Q1 et Q4, il n'y a AUCUN ordre** : Q3 est le meilleur sur m20, Q4 sur m30, Q2 sur
  m32. Ce n'est donc **pas un gradient** (« plus répétitif = mieux ») mais un **seuil** :
  **au-delà d'environ 0,9 trigramme distinct par jeton, le rejeu ne trouve plus rien à consolider** ;
* **le critère final est donc plus faible et plus honnête que celui du § 1ter** : il ne dit pas
  « rejouer les plus répétitifs » (Q1 n'est pas meilleur que Q3), il dit **« éviter les plus
  variés »** — et c'est un tri qui coûte des millisecondes, sans le modèle ;
* **l'hypothèse reste la même** et elle explique le seuil : un texte très varié ressemble à du bruit
  (peu de régularité par jeton), donc il n'y a rien à extraire ; en dessous du seuil, tout texte
  ordinaire porte assez de structure, et le volume redevient le seul levier — c'est la conclusion de
  toute la nuit (« la quantité domine le placement »), avec **une exception** : le bruit ne
  s'apprend pas.

## 2. Ce que ça change pour le protocole de sommeil

1. **rejouer court et divers** — 3 morceaux répartis donnent −6,5 % en domaine pour un coût hors
   domaine indétectable ;
2. **ne pas trier par difficulté** : le tri par surprise est mesuré **sous** le hasard, et il coûte
   une passe de mesure préalable (20 morceaux × 1 024 jetons) pour un résultat négatif ;
3. **ne pas rejouer ce qui est déjà su** : c'est la seule règle qui **coûte** ailleurs (+2,07 %) ;
4. **et le seul critère qui tient est un SEUIL, pas un tri** : **éviter les morceaux les plus
   variés** (> 0,9 trigramme distinct par jeton : −7,9 % contre −11 à −14 % sur m20) — au-dessous du
   seuil, tous les lots se valent (§ 1quater). C'est le premier critère de la nuit qui départage
   quoi que ce soit, et il est **négatif** : il dit quoi éviter, pas quoi choisir ;
5. et **la question qui reste** : un rejeu *répété* (plusieurs nuits sur les mêmes morceaux) ou un
   rejeu *séquentiel* (les morceaux dans l'ordre du texte) ne sont pas mesurés — le plan de sommeil
   les demanderait.

## 3. Ce que cette fiche ne dit pas

* **trois morceaux, une graine, un seul corpus** : la « règle au hasard » est **un tirage** (m5,
  m12, m17), pas une espérance — il faudrait plusieurs tirages pour dire que le hasard *bat* les
  premiers, et l'écart (1 point) est du même ordre que le **bruit du harnais à graine égale**
  (**0,4 point**, mesuré en fin de nuit : `rapport-consolidation-balayage.md` § 4bis). **Ce qui est
  solide, c'est que la surprise ne gagne pas**, et que l'ordre des règles du milieu (0,7 point) est
  à la limite du mesurable ;
* **rien sur la sélection par nouveauté au sens du dépôt** (la règle hebbienne mesurée en E7, qui
  *empire* la règle locale) : les deux « nouveautés » ne sont pas la même chose et ne sont pas
  comparées ;
* **rien sur l'ordre** : les trois morceaux sont présentés dans un ordre fixe, mélangé au niveau des
  lots — l'effet d'un ordre *curriculaire* n'est pas mesuré ;
* **le budget d'époque n'est pas ajusté par règle** : 12 époques pour les quatre, alors que la
  « surprise » demanderait peut-être un autre pas d'apprentissage — c'est une faiblesse assumée du
  protocole, et elle est écrite.
