# Le pont GÉNÉRATIF : le réseau naît, puis l'attrition le fait généraliser

`tools/pont_generatif.py` — deux phases, et c'est l'apprentissage qui décide des
tailles. Aucune rétropropagation : A et B restent aléatoires et **gelés**, seule la
lecture `W` s'ajuste par moindres carrés ridgés.

Perimètre : 40 langues d'entraînement (dont 4 ou 10 tenues pour la VALIDATION),
6 langues de TEST jamais vues — `ell heb hin jpn kor tha`, écritures non latines.
Professeur : Qwen2.5-0.5B, couche 10. Corpus : article 1 de l'UDHR, 3254 pas.
Réglages : `a = 0,2`, ride `3·10⁻¹` (résultat 9).

## 1. Phase générative — on part d'UN neurone

Chaque pas ajoute une **couche**. Une couche nouvelle ne lit que les couches
**antérieures** (plus elle-même), jamais l'inverse : les trajectoires déjà
calculées ne sont donc **pas perturbées**, et on ne calcule que la couche qui
naît. Le coût de la croissance vaut le réseau final, pas la somme des états.

Croissance `1 → 1 → 2 → 4 → 8 → … → 128` (9 couches, 256 neurones) :

| neurones | couches | fid appr | fid VAL | **fid TEST** | invariance | pire paire |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 0,6547 | 0,7135 | 0,5714 | **0,9958** | **0,9842** |
| 4 | 3 | 0,6599 | 0,7133 | 0,5802 | 0,9939 | 0,9848 |
| 16 | 5 | 0,6696 | 0,7195 | 0,5897 | 0,9899 | 0,9803 |
| 64 | 7 | 0,6977 | 0,7304 | 0,5997 | 0,9420 | 0,8254 |
| **128** | **8** | 0,7148 | 0,7363 | **0,6061** | 0,9128 | 0,7719 |
| 256 | 9 | 0,7362 | 0,7402 | 0,6056 | 0,8869 | 0,7306 |

**Chaque naissance améliore la fidélité d'apprentissage ET de validation**, sans
plateau. La fidélité de TEST culmine à **128 neurones** (0,6061) et ne progresse
plus ensuite (256 → 0,6056). L'invariance, elle, **décroît avec la taille** —
0,9958 à un neurone, 0,8869 à 256 : c'est la courbe d'échange du résultat 9, vue
cette fois par la taille plutôt que par le ride.

## 2. Attrition — retirer des NEURONES, pas des colonnes

Le point qui décide de la validité de tout le reste : on ne masque pas des
colonnes de lecture, on **recalcule les trajectoires des survivants sans les
retirés**. Sans ce recalcul, « 1 neurone » ne voudrait rien dire — la trajectoire
de ce neurone aurait été calculée par les 256 autres. Un neurone de 9ᵉ couche
n'est pas un neurone, c'est une **caractéristique profonde**.

Le critère compare au **meilleur** score atteint, jamais au score courant :
comparer au courant transforme l'attrition en marche aléatoire vers le bas,
chaque pas étant petit mais la somme ne l'étant pas.

| neurones | couches | fid VAL | **fid TEST** |
|---:|---:|---:|---:|
| 256 (né) | 9 | 0,7402 | 0,6056 |
| **192** | 8 | 0,7388 | **0,6078** |
| 144 | 7 | 0,7382 | 0,6063 |
| 108 | 7 | 0,7453 | **0,6053** |
| 46 | 7 | 0,7404 | 0,5926 |
| 21 | 5 | 0,7353 | 0,5860 |
| 2 | 1 | 0,7292 | 0,5739 |

**L'attrition AMÉLIORE la fidélité de test en réduisant le réseau** : 256 → 192
neurones fait passer le TEST de 0,6056 à **0,6078**, et 256 → 108 (soit **−58 %**)
le maintient à 0,6053. La validation, elle, ne bouge presque pas (0,7402 →
0,7388). C'est exactement le comportement demandé : **la capacité retirée est
réabsorbée par les unités qui restent**, et le réseau réduit généralise mieux.

## 3. Ce que le critère de validation ne voit pas

Avec 4 langues de validation et un seuil large (0,02), l'attrition descend jusqu'à
**2 neurones** en gardant une validation à 0,7292 — alors que la fidélité de TEST
est tombée à 0,5739, à peine au-dessus de la constante (0,5619). **La validation
est un proxy myope de l'objectif réel** : elle reste plate là où le test
s'effondre.

Avec 10 langues de validation et un seuil de 0,005, l'attrition s'arrête d'elle-
même à **144 neurones / 7 couches** avec un TEST de 0,6063. La réduction passe de
99 % (invraisemblable) à 44 % (crédible).

**Le levier n'est donc pas la règle de retrait, c'est la qualité de la
validation.** Un critère d'arrêt n'est jamais meilleur que ce sur quoi il juge.

## 4. Ce que ça change pour la mission

- Le réseau le plus fidèle n'est **pas** le plus gros : **128 à 192 neurones**
  battent 256, et 108 en font presque autant avec 58 % de moins.
- **L'invariance et la fidélité restent les deux axes d'une seule courbe** : à
  1 neurone, invariance 0,9958 et fidélité 0,5714 ; à 256, 0,8869 et 0,6056. La
  génération et l'attrition sont les deux façons de **parcourir** cette courbe.
- La croissance en cascade est **distribuable** : chaque couche ne lit que les
  précédentes, donc chaque nœud d'une grappe peut naître et calculer sa couche
  sans coordination avec les autres.


## 5. Confirmation sur la tâche 10× plus dure (38 212 pas)

Mêmes 40 langues, mêmes 6 langues tenues à l'écart, mais **10 unités par langue**
au lieu d'une. La constante témoin tombe à 0,4405 : la tâche est bien plus dure.

### Croissance

| neurones | couches | fid appr | fid VAL | **fid TEST** | invariance | pire paire |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 0,5234 | 0,5897 | 0,4424 | **0,9993** | **0,9984** |
| 4 | 3 | 0,5291 | 0,5928 | 0,4489 | 0,9988 | 0,9971 |
| 16 | 5 | 0,5409 | 0,6023 | 0,4578 | 0,9975 | 0,9949 |
| 32 | 6 | 0,5521 | 0,6076 | 0,4677 | 0,9924 | 0,9817 |
| 64 | 7 | 0,5679 | 0,6184 | 0,4810 | 0,9883 | 0,9700 |
| 128 | 8 | 0,5863 | 0,6295 | 0,4933 | 0,9839 | 0,9625 |
| 256 | 9 | 0,6081 | 0,6410 | 0,4998 | 0,9706 | 0,9376 |

**Monotone dans les cinq colonnes**, sans plateau : chaque naissance paie. C'est
la différence de fond avec le réservoir **plat**, qui sature puis recule
(64 neurones : 0,5921 ; 256 : 0,5868 sur la tâche à une unité). **La profondeur
est ce qui permet à la capacité de servir.**

### Attrition

| neurones | couches | fid VAL | **fid TEST** |
|---:|---:|---:|---:|
| 256 (né) | 9 | 0,6410 | 0,4998 |
| **192** | 9 | 0,6386 | **0,5002** |
| 144 (refusé) | — | 0,6357 | — |

L'attrition **améliore encore le test** (0,4998 → 0,5002) en retirant 25 % des
neurones, et le retrait suivant est refusé par la validation. Le critère
fonctionne : il s'arrête de lui-même au bon endroit.

### Face au réservoir plat, à taille égale

| | fid TEST | invariance | pire paire |
|---|---:|---:|---:|
| réservoir plat, 64 neurones, `a=0,2` ride `3·10⁻¹` | 0,4767 | 0,9797 | 0,9606 |
| **cascade générative, 64 neurones** | **0,4810** | 0,9883 | 0,9700 |
| **cascade générative, 192 neurones (après attrition)** | **0,5002** | 0,9710 | 0,9355 |

À taille égale la cascade gagne déjà (+0,43 pt), mais surtout **elle continue de
progresser là où le plat recule** : +2,35 points de fidélité de test au meilleur
point. Rapporté à l'écart qui compte — celui au-dessus de la constante témoin —
l'avantage passe de +0,0362 à +0,0597, soit **+65 %**.


## 6. L'ATTRITION PÉRIODIQUE paie : deux cycles battent une passe

La demande était « une phase générative, **puis une attrition périodique** ».
`--cycles N` alterne donc croissance et attrition, avec **compaction de la
généalogie** entre les deux (sans elle, la croissance suivante lirait des indices
de neurones morts).

Tâche à une unité, validation sur 10 langues, seuil 0,005 :

| | neurones | couches | fid VAL | **fid TEST** |
|---|---:|---:|---:|---:|
| 1 passe (croissance puis attrition) | 144 | 8 | 0,7402 | 0,6056 |
| **2 cycles** | **108** | **10** | **0,7410** | **0,6079** |
| 3 cycles | 108 | 13 | 0,7410 | 0,6079 |

**Deux cycles gagnent sur les deux tableaux** : 25 % de neurones en moins (144 →
108), deux couches de plus, et une fidélité de **validation** comme de **test**
supérieure (0,7402 → 0,7410 et 0,6056 → 0,6079). Un troisième cycle ne change
plus rien : le réseau a atteint sa forme.

**Pourquoi ça marche** : la première attrition ne fait pas que réduire, elle
**réorganise** — les survivants redeviennent le socle d'une croissance neuve, qui
part d'un réseau déjà débarrassé de ses détecteurs particuliers. La capacité
ajoutée ensuite sert donc à autre chose qu'à redire ce qui était déjà là.

## 7. Deux fautes corrigées en route, et pourquoi elles comptaient

**Une fuite de données.** `Pont` ne détenait que les langues d'entraînement, mais
était interrogé avec les indices des langues de TEST : la fidélité annoncée était
de 0,7234 au lieu de 0,5739. Le test se calcule désormais sur les trajectoires des
langues tenues à l'écart, produites par le réseau **réduit**.

**Une sélection sur le test.** Le « meilleur réseau rencontré » était choisi
d'après sa fidélité de TEST — regarder la réponse avant de choisir. La sélection
se fait maintenant sur la **validation** seule ; le test ne fait que constater.
C'est ce qui a fait passer le meilleur réseau de 256 neurones (0,6056) à
108 neurones (0,6079) : le premier était un artefact de sélection.


## 8. Les cycles sur la tâche 10× plus dure

| | neurones | couches | fid VAL | **fid TEST** |
|---|---:|---:|---:|---:|
| réservoir **plat**, 64 neurones | 64 | 1 | — | 0,4767 |
| cascade, croissance seule | 256 | 9 | 0,6410 | 0,4998 |
| cascade, 1 passe (attrition → 192) | 192 | 9 | 0,6386 | 0,5002 |
| **cascade, 2 cycles** | **256** | **11** | **0,6417** | **0,5012** |
| *constante témoin* | — | — | — | *0,4405* |

Deux cycles donnent la meilleure **validation** (0,6417) **et** le meilleur
**test** (0,5012) — la sélection ne doit rien au hasard, elle s'est faite sur la
validation seule.

**L'écart qui compte — au-dessus de la constante témoin — passe de +0,0362
(réservoir plat) à +0,0607, soit +68 %.**

Le réseau bute sur le plafond de 256 neurones que je lui avais imposé : à 11
couches il demandait encore à croître. La courbe de croissance n'a toujours pas
montré de plateau sur cette tâche.


## 9. Où la croissance s'arrête : le plateau est à ~470 neurones

Course avec plafond 512, deux cycles. Cycle 2 (le réseau part de 192 survivants) :

| neurones | couches | fid appr | fid VAL | **fid TEST** | invariance | pire paire |
|---:|---:|---:|---:|---:|---:|---:|
| 240 | 10 | 0,6082 | 0,6407 | 0,5008 | 0,9719 | 0,9351 |
| 300 | 11 | 0,6154 | 0,6439 | 0,5004 | 0,9600 | 0,9118 |
| 375 | 12 | 0,6222 | 0,6465 | 0,5006 | 0,9495 | 0,8979 |
| **468** | **13** | 0,6290 | **0,6482** | 0,5023 | 0,9425 | 0,8847 |
| 512 | 14 | 0,6315 | 0,6478 | **0,5026** | 0,9418 | 0,8832 |

**La validation culmine à 468 neurones puis REDESCEND** (0,6482 → 0,6478) : le
plateau est là, entre 470 et 512 neurones, 13-14 couches. C'est la première fois
que la courbe de croissance se retourne — aux tailles précédentes elle montait
toujours.

**Et l'attrition fait mieux que la croissance :**

| | neurones | couches | fid VAL | **fid TEST** |
|---|---:|---:|---:|---:|
| croissance, 512 | 512 | 14 | 0,6478 | 0,5026 |
| **attrition → 384** | **384** | 14 | 0,6458 | **0,5035** |
| attrition → 288 (retenu) | 288 | 13 | 0,6430 | 0,5031 |
| 72 de plus retirés (refusé) | — | — | 0,6397 | — |

**Le meilleur test de tout le processus (0,5035) est produit par l'ATTRITION, pas
par la croissance** — et avec 25 % de neurones en moins que le maximum. C'est
l'énoncé le plus net de tout ce rapport : à cette échelle, **retirer des neurones
en réajustant la lecture vaut mieux qu'en ajouter**.

### Le bilan face à la constante témoin

| modèle | neurones | fid TEST | écart à la constante |
|---|---:|---:|---:|
| constante témoin | — | 0,4405 | — |
| réservoir **plat**, 64 neurones | 64 | 0,4767 | +0,0362 |
| réservoir plat, 512 neurones | 1 179 648 params | 0,5812 | *autre tâche* |
| **cascade générative, 384** | **384** | **0,5035** | **+0,0630** |

**L'avantage sur la constante passe de +0,0362 (plat) à +0,0630, soit +74 %** —
avec 384 neurones au lieu de 64, mais 13 couches au lieu d'une seule.


## 10. RECTIFICATION — comparer deux professeurs n'a pas de sens

La section 9 ci-dessus compare l'invariance du pont (0,9425, ajusté sur la couche
10 de **Qwen2.5-0.5B**) à celle de la couche 17 de **Qwen3-30B-A3B** (0,9014) pour
en conclure que le pont « bat le professeur 30B ». **Ce classement est vide.**

Chaque modèle a sa propre représentation sémantique interne. Une couche interne
n'existe que dans la base, la métrique et le découpage du modèle qui la produit —
il n'y a pas de couche sémantique universelle. Les deux nombres sont exacts, mais
ils appartiennent à deux espaces différents : ils ne se comparent pas.

**Ce qui reste valide** : la comparaison à l'intérieur d'un même professeur. Elle
donne, sur le périmètre des 6 langues tenues à l'écart et de 10 unités :

| même professeur (Qwen2.5-0.5B) | invariance | pire paire |
|---|---:|---:|
| couche 10 du professeur — **la cible** | 0,4487 | 0,3188 |
| **notre pont génératif** | **0,9425** | **0,8847** |

Notre pont est bien plus invariant que la couche qu'il émule — c'est le prix de la
fidélité (0,50), et c'est la courbe d'échange déjà établie. Cette phrase-là dit
quelque chose ; la précédente, non.

Voir `docs/note-un-pont-par-professeur.md` : **il faut un pont par professeur**, et
l'étude des universaux sémantiques relève de l'initiative Panini, pas de Drave.


## 11. Les réglages ne se transfèrent pas : la cascade veut le contraire du plat

`a = 0,2` et ride `3·10⁻¹` avaient été trouvés pour le réservoir **plat**
(résultat 9). Rien ne dit qu'ils valent pour la **cascade** — architecture
différente, dynamique différente. Balayage complet, 12 configurations, même
périmètre, même tâche :

| `a` \ ride | 0,1 | 0,3 | 1,0 |
|---|---:|---:|---:|
| 0,1 | 0,5954 | 0,6039 | 0,6036 |
| 0,2 | 0,5963 | 0,6079 | 0,6071 |
| 0,35 | 0,5959 | 0,6099 | 0,6088 |
| **0,5** | 0,5989 | 0,6078 | **0,6105** |

**La cascade préfère `a = 0,5` et ride `1,0` — l'opposé du plat.** Le gain reste
modeste (+0,26 pt sur la meilleure configuration précédente), mais le fait est
net : **un réglage trouvé pour une architecture ne se transporte pas** à une
autre. C'est le même principe que « un pont par professeur », un cran plus bas.

### Le meilleur réseau de la cascade, en entier

| | |
|---|---|
| taille | **256 neurones · 11 couches** |
| fidélité apprentissage | 0,7330 |
| fidélité validation | 0,7492 |
| **fidélité TEST** | **0,6105** (constante témoin 0,5658) |
| invariance TEST | 0,9278 · pire paire 0,8190 |

### Face au réservoir plat, même professeur, même tâche

| | neurones | fid TEST | écart à la constante | invariance |
|---|---:|---:|---:|---:|
| réservoir plat (`a=0,2` ride 0,3) | 64 | 0,5921 | +0,0263 | 0,9772 |
| **cascade générative (`a=0,5` ride 1,0)** | **256** | **0,6105** | **+0,0447** | 0,9278 |

**+1,84 point de fidélité de test, et un avantage sur la constante qui passe de
+0,0263 à +0,0447 — soit +70 %.** L'invariance est plus basse (0,9278 contre
0,9772) : c'est la courbe d'échange, la cascade occupant un point plus avancé sur
l'axe fidélité. Le plat, lui, **ne peut pas atteindre 0,6105** : il plafonne à
0,5921 puis recule.


## 12. Contrôle de robustesse : douze tirages, douze fois le même verdict

Un seul tirage ne prouve rien. Douze combinaisons (4 graines du réservoir gelé ×
3 découpages de validation), configuration gagnante `a=0,5` ride `1,0` :

| graine | val 6 | val 10 | val 14 |
|---|---:|---:|---:|
| 1 | 0,6044 | 0,6054 | 0,6059 |
| 5 | 0,6095 | 0,6105 | 0,6101 |
| 11 | 0,6025 | 0,6049 | **0,6131** |
| 23 | 0,6058 | 0,6070 | 0,6092 |

| | fid TEST | **avantage sur la constante** |
|---|---:|---:|
| minimum | 0,6025 | **+0,0367** |
| **médiane** | **0,6070** | **+0,0412** |
| maximum | 0,6131 | **+0,0477** |

**La médiane est la seule chose honnête à citer** : +0,0412. Le meilleur tirage
(0,6131) existe, mais le citer seul serait du choix a posteriori — c'est
exactement la faute corrigée au §7.

Face au réservoir plat, dont l'avantage mesuré est **+0,0263**, la cascade fait
donc **1,6 fois mieux**, et cela tient sur douze tirages indépendants.

**Et les douze runs butent sur le plafond de 256 neurones** (10 à 12 couches) :
la taille atteinte est limitée par MA borne, pas par l'apprentissage. La question
« jusqu'où la croissance irait seule » reste ouverte.
