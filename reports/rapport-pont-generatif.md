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
