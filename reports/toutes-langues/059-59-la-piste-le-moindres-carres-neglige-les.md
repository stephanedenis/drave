> Campagne : **toutes-langues** · expérience **59**
> Titre : 59. La piste « le moindres carrés néglige les petites composantes » est RÉFUTÉE — par sa propre prémisse
> Date réelle : **2026-10-06 20:26 HAE** (source : commit `603b7a6`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 59. La piste « le moindres carrés néglige les petites composantes » est RÉFUTÉE — par sa propre prémisse

### 59.1 L'idée, et elle était plausible

Le §58 laissait une question nette : les caractéristiques du réservoir **contiennent**
la structure contenu/langue du professeur (une lecture linéaire l'atteint), mais
l'objectif des moindres carrés ne l'extrait pas. L'explication la plus simple était
que la fidélité est un **cosinus par ligne** tandis que le fit minimise une erreur
**quadratique absolue** : si la cible est dominée par une masse commune, la lecture est
payée pour la reproduire et les petites composantes — celles qui distinguent les
contenus — pèsent peu.

Trois variantes **convexes** et en forme fermée découlaient de cette idée : centrer la
cible par entrée, normaliser chaque ligne, et **blanchir** la cible (la multiplier par
`C^(−α/2)`, ce qui égalise l'importance de toutes les directions). Toutes restent des
moindres carrés ordinaires.

### 59.2 La mesure qui tue l'idée avant même de la tester

**Spectre de la cible** : 896 directions, **la première ne porte que 4,1 % de
l'énergie**, les dix premières 21,5 %.

**Il n'y a pas de masse dominante.** L'idée de départ supposait une structure qui
n'existe pas : l'énergie de la cible est **étalée** sur un très grand nombre de
directions. Le moindres carrés ne néglige donc rien de « petit » — il n'y a pas de
gros à négliger devant.

### 59.3 Et les variantes ne marchent pas

| variante | fid TEST | S_langue | S_domaine | **SÉPARATION** |
|---|---:|---:|---:|---:|
| **A** référence | **0,4706** | 0,9957 | 0,9965 | −0,0008 |
| **B** cible centrée | 0,4708 | 0,9869 | 0,9909 | −0,0040 |
| **C** lignes normées | 0,4197 | **1,0000** | **1,0000** | **−0,0000** |
| **D** blanchiment α=0,25 | 0,4383 | 0,9996 | 0,9997 | −0,0001 |
| **D** blanchiment α=0,50 | 0,4226 | 1,0000 | 1,0000 | −0,0000 |
| | | | **cible** | **+0,0517** |

**Aucune n'améliore la séparation, deux la détruisent complètement.** Normaliser les
lignes de la cible donne `S_langue = S_domaine = 1,0000` **exactement** : toutes les
sorties deviennent parallèles. Et le blanchiment — l'idée la plus prometteuse sur le
papier — coûte 0,05 de fidélité pour **zéro** gain de séparation.

### 59.4 Ce qui reste debout, et ce qui tombe

**Tombe** : « le moindres carrés néglige les petites composantes ». La prémisse est
fausse (pas de masse dominante), et les remèdes qui en découlaient ne fonctionnent pas.

**Reste debout** : le constat du §58 — **une** lecture linéaire atteint la séparation
du professeur. Mais il faut le regarder avec méfiance : cette configuration était
**non convexe**, la courbe était **non monotone** (+0,052 à μ=0,1, **−0,012** à μ=0,3,
**−0,140** à μ=1), et rien ne dit que le point gagnant soit autre chose qu'une
coïncidence d'un paysage instable.

**Reste donc ouvert** : *par quel objectif convexe* extraire la structure contenu/langue
que les caractéristiques contiennent manifestement. Les quatre pistes essayées
(deux curseurs quadratiques, centrage, normalisation, blanchiment) sont toutes
écartées, chacune par une mesure.

### 59.5 Ce que cela dit de la démarche

Ce paragraphe est **négatif du début à la fin** : une hypothèse plausible, une
prémisse réfutée par le spectre avant même d'être testée, trois variantes sans effet,
une quatrième contre-productive. Il est écrit parce qu'une piste écartée par une mesure
vaut mieux qu'une piste gardée par politesse — et parce que le §58, seul, aurait laissé
croire que le problème était résolu.


---
