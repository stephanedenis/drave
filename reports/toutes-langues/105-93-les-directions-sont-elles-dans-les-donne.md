> Campagne : **toutes-langues** · expérience **93**
> Titre : 93. LES DIRECTIONS SONT-ELLES DANS LES DONNÉES OU DANS LE TIRAGE ?
> Date réelle : **2026-10-07 13:21 HAE** (source : commit `256cd6a`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-toutes-langues.md`

## 93. LES DIRECTIONS SONT-ELLES DANS LES DONNÉES OU DANS LE TIRAGE ?

### 93.1 La question, et pourquoi elle décide de la validité du §92

Nos sorties dépendent d'un **tirage aléatoire gelé** (`P` et `B` tirés par
`np.random.RandomState(5)`). Le §92 montre qu'un discriminant de rang 2 appris sur ces
sorties sépare le contenu de la langue mieux que le professeur sur dix des quinze paires.
Mais si l'axe trouvé était fabriqué par le tirage, le résultat ne vaudrait que pour la
graine 5.

**Six graines indépendantes** (5 à 10), même protocole, même panel (282 entrées
d'apprentissage, 144 de test, 6 langues). Pour chacune : apprendre le pont, lire les sorties,
apprendre le discriminant, garder son sous-espace, et mesurer **les angles principaux** entre
sous-espaces deux à deux.

### 93.2 Le rapport après projection, graine par graine

C'est le chiffre qui décide, et non la ressemblance des axes :

| graine | rapport brut | **après projection rang 2** | après projection rang 5 |
|---|---:|---:|---:|
| 5 | 0,176 | 1,474 (**136,4 %**) | 0,910 (84,2 %) |
| 6 | 0,186 | 1,275 (118,0 %) | 0,793 (73,4 %) |
| 7 | 0,151 | **1,601 (148,1 %)** | 0,892 (82,5 %) |
| 8 | 0,173 | **1,071 (99,1 %)** | 0,928 (85,9 %) |
| 9 | 0,192 | — | — |
| 10 | 0,207 | — | — |
| **moyenne sur 6 graines** | 0,181 | **133,7 %** | 92,4 % |
| **écart-type** | 0,017 | **20,6 %** | 19,7 % |
| **min — max** | 0,151 – 0,207 | **99,1 % – 163,2 %** | 73,4 % – 134,2 % |

**Le §92 est représentatif, et non chanceux** : la graine 5 y donnait 136,4 %, la moyenne des
six est **133,7 %**. Le résultat n'a pas été cueilli au sommet de la distribution.

**Mais l'étalement est de ×1,65, et le minimum touche 99,1 %.** Autrement dit : **sur six
tirages, cinq dépassent le professeur et un l'égale.** La formulation honnête est donc :

> **Un discriminant de rang 2 appris sur nos sorties porte le rapport à 134 % ± 21 % de
> celui du professeur — soit de 99 % à 163 % selon le tirage.**

Ce n'est pas « la cible est atteinte ». C'est « la cible est atteinte au tirage médian, et
presque atteinte au pire ».

### 93.3 Les angles : le premier axe est dans les données, le second beaucoup moins

| | angle du **1er** axe | angle **maximal** |
|---|---:|---:|
| rang 2 | **15,7°** | **35,5°** (22,5° – 50,6°) |
| rang 5 | 13,1° | **66,2°** (38,5° – **88,0°**) |

**Le premier axe est stable** : deux projections aléatoires indépendantes le placent à 15,7°
l'une de l'autre. Un angle de 15,7°, c'est un cosinus de 0,96 — **le premier axe du
discriminant est bien une propriété des données**, pas du tirage.

**Le second ne l'est pas.** À rang 2, le désaccord maximal atteint 35,5° en moyenne (jusqu'à
50,6°) ; à rang 5, il monte à **66,2°**, avec des paires de graines à **88°** — c'est-à-dire
**orthogonales**. Au-delà du premier axe, le discriminant trouve des directions qui dépendent
du tirage.

**Et c'est cohérent avec le reste** : le rang 2 est l'optimum partout (§80, §87, §92), et
c'est aussi le rang où le premier axe porte l'essentiel. Le second axe apporte un gain réel
(99 % → 134 %) mais il est **instable**, et c'est lui qui produit l'étalement de ×1,65.

### 93.4 Ce que cela change, et ce que cela ne change pas

**Ce qui tient** : le résultat du §92 n'est pas un artefact de graine. Il est reproduit sur
six tirages indépendants, avec une moyenne à 133,7 %. **Le premier axe contenu/langue est
réellement dans les données** — c'est le résultat le plus solide de cette session, parce
qu'il est le seul qui survive à la fois au changement d'articles, au changement de panel
« dans le même sens », et au changement de graine.

**Ce qui reste fragile** : le second axe, et donc la valeur exacte du rapport. Un chiffre
unique (« nous sommes à 136 % ») est trompeur ; **il faut citer 134 % ± 21 %**.

**Et une question ouverte, maintenant bien posée** : le premier axe est stable, le second ne
l'est pas, et pourtant c'est le rang 2 qui gagne partout. **Le second axe est-il nécessaire,
ou compense-t-il seulement l'instabilité du premier ?** Un discriminant de rang 1 — un seul
axe, parfaitement reproductible — donnerait-il l'essentiel du gain ? C'est la mesure la plus
simple qui reste à faire, et elle est décisive pour un déploiement : **un axe stable et
calculable en forme fermée vaut mieux qu'un plan dont la moitié dépend d'un tirage.**

---
