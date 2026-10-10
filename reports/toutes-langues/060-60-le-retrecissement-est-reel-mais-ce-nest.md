> Campagne : **toutes-langues** · expérience **60**
> Titre : 60. Le rétrécissement est réel — mais ce n'est pas la cause. Et la cible du §58 n'est pas stable
> Date réelle : **2026-10-06 20:47 HAE** (source : commit `a41a27b`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 60. Le rétrécissement est réel — mais ce n'est pas la cause. Et la cible du §58 n'est pas stable

### 60.1 Un défaut quantifié qui n'avait jamais été regardé

Depuis quatre paragraphes, on cherchait pourquoi notre sortie ne sépare plus contenu et
langue. Une chose n'avait jamais été mesurée : **notre sortie est-elle seulement plus
PETITE que sa cible, autour du même point ?**

Si les caractéristiques ne peuvent pas produire toute l'amplitude de la cible, le
moindres carrés **rétrécit** la prédiction vers la moyenne — régression vers la
moyenne, phénomène classique. Or `mt` est le **même pour toutes les entrées** : une
prédiction dominée par `mt` a des moyennes par entrée presque identiques, ce qui
produit exactement le tableau du §57.

**Mesuré**, rapport `‖écart à la moyenne‖ / ‖moyenne‖` par ligne :

| | rapport |
|---|---:|
| **notre sortie** | **0,6234** |
| professeur | **2,1454** |
| **rapport** | **0,291** |

**Nous écrasons l'écart à la moyenne d'un facteur 3,4.** Le défaut est réel, il est
net, et il n'avait pas été vu.

### 60.2 Mais amplifier ne rétablit pas l'ordre

On écrit la sortie `mt + α·(O − mt)` et on balaie α — un simple facteur d'échelle sur
l'écart, donc **linéaire** et dans les règles.

| α | fid TEST | S_langue | S_domaine | **SÉPARATION** |
|---:|---:|---:|---:|---:|
| 0,50 | 0,4701 | 0,9958 | 0,9966 | −0,0008 |
| **1,00** | **0,4769** | 0,9835 | 0,9866 | −0,0031 |
| 1,50 | 0,4553 | 0,9643 | 0,9711 | −0,0068 |
| 2,00 | 0,4291 | 0,9404 | 0,9520 | −0,0117 |
| 3,00 | 0,3817 | 0,8872 | 0,9102 | −0,0230 |

**Amplifier fait MONOTONEMENT BAISSER les deux similarités et rend la séparation PLUS
négative.** À α=3 on approche les niveaux absolus du professeur (0,887/0,910 contre
0,945/0,894) — **mais l'ORDRE reste inversé**. Le problème n'est donc pas une question
d'amplitude : il est dans l'ordre lui-même.

### 60.3 Le contrôle qui change la lecture : la cible du §58 n'est PAS stable

Le contrôle était indiqué par le résultat : dans le jeu de test, les paires « même
article, langues différentes » sont **entre langues inconnues**, tandis que les paires
« même langue, articles différents » sont **dans une langue inconnue**. On refait donc
la mesure sur les langues d'**apprentissage** :

| | S_langue | S_domaine | **SÉPARATION** |
|---|---:|---:|---:|
| **notre sortie** (α=1) | 0,9153 | 0,9844 | **−0,0691** |
| notre sortie (α=2) | 0,7077 | 0,9475 | −0,2398 |
| **professeur, mêmes entrées** | 0,8624 | 0,8776 | **−0,0152** |

**Et là est le résultat gênant : la séparation du PROFESSEUR vaut −0,0152 sur les
langues d'apprentissage et +0,0517 sur celles de test.** Elle **change de signe** selon
le jeu de langues.

L'explication est simple : les langues de test (es, it, pt) sont **trois langues
romanes très proches**, donc le même article y est naturellement très similaire
(0,9454) ; les langues d'apprentissage (de, en, fr) sont **plus mêlées**, et la
similarité entre langues y tombe à 0,8624, **sous** celle entre articles (0,8776).

### 60.4 Ce que cela retire au §58

Le §58 annonçait avoir « atteint la séparation du professeur » (+0,0519 contre
+0,0517). **C'est exact sur ce jeu de langues, et cela reste une preuve que la
structure est linéairement accessible.** Mais **la cible n'est pas une constante du
professeur** : elle dépend de quelles langues composent le panel. La comparaison
« notre séparation contre celle du professeur » n'est donc **valide qu'à panel
identique** — ce qu'elle était ici, mais ce qui doit être dit à chaque fois.

### 60.5 Bilan de la traque, en quatre paragraphes

| piste | verdict |
|---|---|
| §58 — objectif à deux curseurs | **atteint la cible**, mais non convexe et non monotone |
| §59 — pondération de l'objectif (centrage, normalisation, blanchiment) | **écartée** — prémisse réfutée par le spectre |
| §60 — rétrécissement vers la moyenne | **réel (3,4×)**, mais l'amplifier n'inverse pas l'ordre |
| §60 — la cible elle-même | **n'est pas stable** — elle change de signe selon le panel |

**La cause de l'inversion contenu/langue reste non identifiée.** Ce qui est établi, et
c'est beaucoup : elle n'est ni dans la taille du réseau, ni dans la richesse des
caractéristiques, ni dans la pondération de l'objectif, ni dans l'amplitude de la
sortie. Quatre causes plausibles écartées, chacune par une mesure.

### 60.6 Une erreur de ma part, corrigée

La première version découpait les sorties par pas fixe `len(Yte[0])`, en supposant
toutes les entrées de même longueur. **Elles ne le sont pas** — numpy a signalé
`Mean of empty slice` et les moyennes par entrée étaient fausses. Corrigé par des
bornes cumulées. C'est la troisième fois de la session qu'une hypothèse de forme
régulière se glisse dans un outil de mesure.


---
