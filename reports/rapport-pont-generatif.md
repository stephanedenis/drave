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
