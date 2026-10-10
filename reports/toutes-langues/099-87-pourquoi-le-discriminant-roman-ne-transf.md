> Campagne : **toutes-langues** · expérience **87**
> Titre : 87. POURQUOI LE DISCRIMINANT ROMAN NE TRANSFÈRE PAS : il a appris sur les paires faciles
> Date réelle : **2026-10-07 11:53 HAE** (source : commit `687cb52`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 87. POURQUOI LE DISCRIMINANT ROMAN NE TRANSFÈRE PAS : il a appris sur les paires faciles

### 87.1 Le montage

Le §86 laissait une question précise : *un discriminant appris sur les quinze paires à la
fois transfère-t-il mieux que sur trois langues ?* Pour y répondre il faut un panel qui
contienne **à la fois** les paires difficiles (de–en) et les faciles (es–pt), et une
évaluation **hors vivier sur les articles**.

Les six caches par langue `cache_wiki_{de,en,es,fr,it,pt}.npz` — couche 8, 71 articles
chacun, **les mêmes 71 articles** — sont fusionnés en un cache de **426 entrées × 6
langues**. Puis coupés **par article** : 47 articles d'apprentissage (282 entrées) et
24 articles de test (144 entrées). Le pont est appris sur les 282 entrées
d'apprentissage ; le discriminant **aussi** ; la mesure porte sur les 144 entrées de test,
que ni l'un ni l'autre n'a vues.

**Le professeur, sur ce panel de test** : `P_lang` 2 410,7 · `P_cont` 2 605,5 · **rapport
1,081** — et sa pire paire est **de–en à 1,009**, sa meilleure **es–pt à 22,364**. Le
classement des difficultés est le même que celui du §83 sur 482 articles : le panel est
cohérent.

### 87.2 Les trois panels, à pont et évaluation identiques

| discriminant appris sur | rang 0 | **rang 2** | rang 5 | **part au rang 2** |
|---|---:|---:|---:|---:|
| **les 6 langues (15 paires)** | 0,176 | **1,474** | 0,910 | **136,4 %** |
| de/en/fr (3 paires) | 0,176 | **1,368** | 0,885 | **126,6 %** |
| **es/it/pt (3 paires, panel du §80)** | 0,176 | **0,585** | 0,264 | **54,1 %** |
| *professeur* | — | *1,081* | — | *100 %* |

**Le fait, en une phrase : ce qui décide de la qualité de l'axe appris n'est pas le NOMBRE
de langues, c'est la présence des paires DIFFICILES dans le panel d'apprentissage.**

- Six langues (136,4 %) et de/en/fr (126,6 %) donnent des résultats **voisins** — alors que
  l'un a six langues et l'autre trois.
- es/it/pt (54,1 %) est **2,5 fois moins bon** que de/en/fr, alors que les deux ont trois
  langues.

Ce qui les sépare n'est pas la taille du panel : c'est que **de/en/fr contient la pire
paire, et es/it/pt ne la contient pas.** Un axe de langue appris sur trois langues qui se
ressemblent décrit « ce qui distingue des langues romanes » — et cet axe est
**orthogonal à ce qui distingue l'allemand de l'anglais**. C'était l'hypothèse du §86.1 ;
la voici confirmée sur des articles tenus à l'écart, dans les trois sens.

### 87.3 Et le revers, qui compte autant : le rapport n'est pas l'énergie

Le rang 2 « atteint 136 % du professeur ». Lu tel quel, c'est le §80 qui recommence. Il
faut regarder les deux énergies, et non leur quotient — c'est le critère du §62.3 :

| | P_lang | P_cont | RAPPORT |
|---|---:|---:|---:|
| **professeur** | 2 410,7 | 2 605,5 | 1,081 |
| notre pont, rang 0 | 1 220,9 | 215,5 | 0,176 |
| **notre pont, rang 2 (6 langues)** | **60,5** | **89,2** | **1,474** |
| *part de l'énergie du professeur* | *2,5 %* | ***3,4 %*** | *136,4 %* |

**Nous atteignons 136 % du RAPPORT avec 3,4 % de l'énergie de contenu et 2,5 % de l'énergie
de langue.** Le rapport est un quotient : deux énergies qui s'effondrent ensemble dans les
mêmes proportions le laissent intact, et le discriminant de rang 2 fait exactement cela —
il écrase les deux.

C'est la limite de l'indicateur, et elle était déjà écrite au §62.3 sans être appliquée
ici. **Un rapport sans ses deux énergies n'est pas une mesure.** La formulation qui reste
honnête est donc double :

> **Le discriminant de rang 2 obtient le RAPPORT du professeur (136 %) mais avec 3,4 % de
> son énergie de contenu. Il ne l'atteint pas — il atteint son quotient.**

### 87.4 Ce qui est acquis, et ce qui ne l'est pas

**Acquis** : la dépendance du transfert à la **composition** du panel d'apprentissage est
mesurée, elle est forte (×2,5), et elle a un sens clair — *on ne peut pas apprendre ce
qu'est la langue sur trois langues qui se ressemblent*. C'est une règle de conception, pas
un accident de réglage.

**Non acquis** : que le rapport du professeur soit atteignable **à son niveau d'énergie**.
Le §80 et le §75 l'avaient annoncé (§75 : « la cible est atteinte, 98 % du rapport ») ; le
§76 en avait mesuré la réserve ; le §87 la chiffre — **il manque un facteur 29 sur
`P_cont`**.

**La question ouverte se resserre donc encore**, et elle n'est plus celle du rapport :

> **Quel mécanisme, en forme fermée et sans rétropropagation, peut multiplier par 29
> l'énergie de contenu sans multiplier l'énergie de langue ?**

---
