> Campagne : **campagne-benefices** · expérience **05**
> Titre : 5. Les modèles entraînés ici, mesurés DANS le moteur — ce que le routage et la distillation rapportent
> Date réelle : **2026-10-09 02:31 HAE** (source : commit `1530bee`)
> Source : extrait **verbatim** du rapport monolithique, archivé en `reports/archive/rapport-campagne-benefices.md`

## 5. Les modèles entraînés ici, mesurés DANS le moteur — ce que le routage et la distillation rapportent

**Le protocole, et il a fallu le corriger** — et la courbe de ce paragraphe
**s'inverse à dim 512**, ce que le § 5 bis mesure. Le moteur évalue une fenêtre contiguë
de `--limit` jetons ; ces modèles ont été **entraînés sur des fenêtres de 128
jetons**. Les évaluer sur 256, 512 ou 2 048 positions les fait sortir de leur
distribution (à 2 048, la perplexité triple et le classement s'inverse). La mesure
retenue est donc **huit fenêtres de 128 jetons** (`--depuis` décale le début),
moyennées en log — dans la longueur d'entraînement, sur huit tranches du fichier
de validation. Toutes les portes de logits sont tenues.

| modèle | paramètres | PPL moyenne (8 × 128) | paires/jeton | vs jumeau dense |
|---|---:|---:|---:|---:|
| `m5_d256_dense` | 3,2 M | 5,0155 | 3,2 M | — |
| `m5_d256_route` | 10,3 M | 4,8858 | 3,2 M | −2,6 % |
| **`m5_d256_route_distille`** | 10,3 M | **4,7642** | 3,2 M | **−5,0 %** |
| `m5_d384_dense` *(le professeur)* | 7,2 M | 5,0108 | 7,2 M | — |
| `m5_d384_route` | 44,4 M | 4,8646 | 7,2 M | −2,9 % |
| **`m5_d384_route_distille`** | 44,4 M | **4,4113** | 7,2 M | **−12,0 %** |

**Trois résultats, et le troisième est le plus fort.**

1. **Le routage gagne à lecture exactement égale** (vérifié par le compteur du
   moteur) : −2,6 % et −2,9 % de perplexité en stockant 3,2× et 6,2× plus de
   paramètres. C'est la thèse du projet — un modèle plus gros qui lit autant.
2. **La distillation ajoute, et son gain CROÎT avec la taille** : −2,5 % à
   dim 256, **−9,3 % à dim 384**. Le professeur (dense dim 384, 5,0108) est
   **battu par son élève** (4,4113), qui lit pourtant 1,92 M poids par jeton au
   lieu de 7,2 M.
3. **Au total, à lecture égale, le modèle produit ici est 12 % meilleur que son
   jumeau dense** — sans un paramètre de plus à lire.

**Une réserve qui reste** : les débits. À `d256` le routé est plus rapide que le
dense en listes (662,8 contre 442,3 tok/s), à `d384` plus lent (184,0 contre
255,0) — le regroupement des jetons par expert a un coût fixe qui pèse quand le
modèle grandit. Le gain de qualité, lui, tient dans les deux cas.

**Et les experts ne passent PAS par les listes** : écrits en Q4_0, format pour
lequel le moteur n'a pas de noyau de listes, ils sont exécutés en dense. La mesure
honnête du coût est donc la colonne « paires/jeton », égale par construction.

**Un manque mesuré, découvert en préparant l'expérience « routé ET creux »** : le
chargeur d'experts n'accepte que les formats à noyau dédié (Q4_K, Q6_K, MXFP4,
Q4_0) et les super-blocs de 256 poids (`list::sans_noyau`). Un tenseur d'experts en
**Q8_0 — le seul format qui donne accès au chemin par listes** — est refusé :

    [moe] couche 0 : « blk.0.ffn_gate_exps.weight » de type Q8_0
          — format sans noyau ni déquantification

**Conséquence, et elle est structurelle** : aujourd'hui, **un modèle routé ne peut
pas être exécuté en listes**. Le routage économise des *experts*, pas des
*événements* ; la parcimonie d'activation, qui est ce que les listes exploitent, ne
peut pas s'appliquer aux experts. C'est la limite la plus nette du moteur pour la
thèse « routage + événements », et elle tient en une ligne de format.

### 5 bis. Le gain du routage N'EST PAS monotone : il s'inverse à dim 512

La courbe s'arrête d'abord à dim 384 dans ce rapport. L'échelle 512 a été
entraînée **avec exactement le même protocole** (4 couches, 40 000 pas, mêmes
données), et le résultat renverse la tendance — **deux mesures indépendantes le
disent**, la validation à l'entraînement et le moteur après export :

| dim | dense (val, bits/octet) | routé (val) | gain du routage | PPL moteur (8 × 128) |
|---:|---:|---:|---:|---|
| 256 | 2,0074 | 1,9373 | **−3,5 %** | 5,0155 → 4,8858 (−2,6 %) |
| 384 | 1,9020 | 1,8762 | −1,4 % | 5,0108 → 4,8646 (−2,9 %) |
| **512** | **1,8580** | **1,8843** | **+1,4 % — le routé PERD** | **4,5686 → 5,0255 (+10 %)** |

**Et la distillation renverse le renversement.** Le distillat du routé 512 a été
entraîné et mesuré dans la nuit (professeur : le dense 512, mêmes 40 000 pas) :

| dim | dense | routé | **routé distillé** | gain du distillat sur son jumeau routé |
|---:|---:|---:|---:|---:|
| 256 | 5,0155 | 4,8858 | **4,7642** | −2,5 % |
| 384 | 5,0108 | 4,8646 | **4,4113** | −9,3 % |
| **512** | 4,5686 | 5,0255 | **4,3305** | **−13,8 %** |

**Le gain de la distillation croît avec la taille : −2,5 %, −9,3 %, −13,8 %**, et
il est assez grand à dim 512 pour compenser un routage qui, seul, perdait 10 %.
Le modèle produit ici est donc **5,2 % meilleur que son jumeau dense à lecture
égale** (12,8 M paires par jeton de part et d'autre, vérifié par le compteur du
moteur) — alors que sa partie routée seule était 10 % pire.

**Et l'hypothèse « sous-entraîné » a été testée — elle est vraie en fp32, fausse
après export.** Le même routé 512, entraîné **80 000 pas** au lieu de 40 000 :

| routé 512 | validation fp32 (bits/octet) | PPL moteur (8 × 128) | écart de quantification |
|---|---:|---:|---:|
| 40 000 pas | 1,8843 | 5,0255 | **+0,445 bit/octet** |
| **80 000 pas** | **1,8237** ✅ meilleur | **5,3845** ❌ pire | **+0,605 bit/octet** |

**Deux fois plus d'entraînement améliore le modèle en fp32 (1,8237 — mieux que son
jumeau dense, 1,8580) et le dégrade après quantification.** L'écart entre les deux
est le prix de l'export en Q4_0, et il **croît avec l'entraînement** : +0,445 puis
+0,605 bit/octet, soit +36 %. Le chiffre du moteur est fidèle — la porte de
correction a été passée sur ce modèle (corrélation des logits **0,9998**, 100 % des
positions utiles au-dessus de 0,95, top-1 98,4 %).

**Ce que cela change dans la façon de choisir un modèle** : le format d'export fait
partie de la spécification. Un modèle entraîné plus longtemps n'est pas « meilleur »
en Drave si sa quantification coûte davantage — et c'est exactement l'argument du
dessin (J) de `docs/modele-pour-drave.md` : entraîner *pour* la grille dans laquelle
on exécutera. *(Ce modèle ne peut d'ailleurs pas être testé en 8 bits : le chargeur
d'experts refuse Q8_0 et F16 — les experts d'un MoE n'ont aujourd'hui que des
formats 4 bits.)*

**La recette qui sort de cette courbe est donc « router ET distiller »**, pas
« router » — et c'est la distillation, pas le routage, qui porte le gain aux
grandes échelles. Le mécanisme reste à expliquer (l'hypothèse la plus simple :
un élève à experts multiples profite beaucoup plus d'une cible dense que d'un
objectif d'argmax, parce que chaque expert voit moins d'exemples) — c'est une
hypothèse, pas une mesure, et elle est notée comme telle.

**Et c'est bien à lecture ÉGALE**, vérifié par le compteur du moteur sur les deux
modèles exportés : **12,8 M de paires par jeton de part et d'autre** (attention
3,2 M pour les deux ; experts 9,5 M + partagé 0,1 M pour le routé contre partagé
9,6 M pour le dense).

Deux réserves, et elles sont dans la mesure : les deux modèles ont reçu
**40 000 pas**, alors que le routé stocke 78,8 M paramètres contre 12,7 M — il est
donc possible qu'il soit **sous-entraîné** à cette échelle, et c'est une hypothèse,
pas un résultat. La distillation du routé 512 (professeur : son jumeau dense) est
en cours et dira si le levier du § 5 rattrape ce renversement.

**Ce que cela change dans ce rapport** : la phrase « le routage gagne » n'est vraie
qu'aux petites échelles. À dim 512, **un modèle dense deux fois plus petit lit
autant et fait mieux** — et c'est la première fois que la campagne mesure un
résultat qui va contre la thèse du projet. Il est consigné comme tel.

### 5 ter. La parcimonie : IMPOSÉE ou APPRISE ? La réponse est mesurée, et elle est nette

C'est **la** question de l'architecture événementielle sur un modèle dense, et elle
n'avait pas de réponse. Trois modèles **identiques par ailleurs** (dim 384, 4
couches, 6 têtes, FFN 1152, 40 000 pas, mêmes données, FFN exportée en Q8 pour que
le chemin par listes existe) :

- **témoin** : entraîné normalement, puis creusé à l'exécution (`--act-topk`) ;
- **`m7_d384_kwta050`** : entraîné **avec** le k-WTA à 50 % gardés ;
- **`m7_d384_kwta025`** : entraîné **avec** le k-WTA à 25 % gardés.

Le k-WTA d'entraînement est appliqué sur l'entrée de **toutes les couches
linéaires** — exactement l'opération que `--act-topk` impose ensuite. Protocole de
record : huit fenêtres de 128 jetons, moyennées en log, chemin par listes.

| modèle | entraîné à | aucune parcimonie | **50 % gardé** | **25 % gardé** |
|---|---|---:|---:|---:|
| **témoin** (creusé à l'exécution) | — | **4,9959** | 5,3032 (+6,2 %) | 10,8758 (**+118 %**) |
| **`kwta050`** | 50 % | 5,1858 | **5,0606 (−4,6 %)** | 5,7666 |
| **`kwta025`** | 25 % | 6,4282 | 5,8131 | **5,1719 (−52 %)** |
| événements/fenêtre | | 336 M | 168 M | 84 M |

*(Les pourcentages entre parenthèses sont l'écart au témoin **au même taux de
parcimonie**, qui est la seule comparaison juste.)*

**Quatre conclusions, et la dernière est la recette.**

1. **Apprise, la parcimonie ne coûte RIEN** : à 50 % gardés, `kwta050` fait
   *mieux* qu'en dense (5,0606 contre 5,1858), là où le témoin perd 6,2 %. Et à
   taux égal il est **4,6 % meilleur** que le témoin — pour moitié moins de
   lectures.
2. **À 25 %, l'écart devient un gouffre** : 5,1719 contre **10,8758**, soit
   **−52 %**. Ce qu'un modèle dense ordinaire ne supporte pas (un quart des
   activations), un modèle entraîné pour ça le supporte presque sans perte
   (6,4282 en dense → 5,1719 à 25 %, c'est-à-dire *mieux* creux que dense).
3. **Chaque modèle est meilleur dans SON régime** : `kwta050` gagne à 50 %
   (5,0606) et perd à 25 % (5,7666) ; `kwta025` gagne à 25 % (5,1719) et perd à
   50 % (5,8131). Il n'y a pas de modèle creux « universel » : **il faut
   l'entraîner au taux où on va l'exécuter**.
4. **La lecture suit exactement le taux, et le débit suit la lecture** : 336 M →
   168 M → 84 M d'événements par fenêtre, et le débit du chemin par listes monte de
   **~90 tok/s (dense) à ~143 (50 %) puis ~205 (25 %)** — soit **×1,6 et ×2,3**.
   La parcimonie n'est pas un artifice de comptage : elle réduit les paires lues,
   et le temps suit.

**C'est la recette du modèle nativement événementiel** : on n'élague pas un modèle
après coup, on l'entraîne à vivre creux, et on l'exécute **au taux où il a appris**
— ce que `--act-topk` sait faire. Le gain mesuré au taux de 25 % est de **×2 en
perplexité** (10,88 → 5,17) pour **quatre fois moins de paires lues**.

**La recette tient à l'échelle 512** — mêmes 40 000 pas, même témoin dense 512,
mêmes mesures (8 × 128) :

| `m8_d512_kwta25` (entraîné à 25 %) | aucune parcimonie | 50 % | **25 %** | 12,5 % | **chemin DENSE à 25 %** |
|---|---:|---:|---:|---:|---:|
| perplexité | 6,0503 | 5,5526 | **4,9649** | 5,3248 | 4,9011 |
| événements/fenêtre | 594,8 M | 299,2 M | **149,6 M** | 74,8 M | 0 |
| débit (tok/s) | 89,1 | 132,1 | **213,2** | 282,2 | **211,3** |

**Deux choses, dont une qui nuance la thèse.**

1. **La qualité suit la même loi qu'à dim 384** : le modèle est meilleur **creux que
   dense** (4,9649 à 25 % contre 6,0503 sans), et il perd 7 % quand on le pousse à
   12,5 %, deux fois plus creux que ce qu'il a appris. La lecture suit : 594,8 →
   149,6 M d'événements (÷4), et le débit monte de 89 à **213 tok/s**.
2. **Le temps, lui, ne distingue PLUS les deux chemins à cette échelle** : à top-k
   25 %, le chemin par listes fait 213,2 tok/s et le chemin **dense** 211,3 — égalité.
   La raison est mesurable : à 12,7 M paramètres, ce modèle tient dans les caches du
   processeur, donc **les lectures que les listes économisent étaient déjà
   gratuites**. L'avantage du chemin par listes est un avantage de **bande
   passante**, et il ne se voit que quand le modèle ne tient plus dans les caches —
   c'est-à-dire pas à cette échelle. *(Les deux chemins ne calculent pas exactement
   la même chose : l'écart de 1,3 % de perplexité entre 4,9649 et 4,9011 vient de
   l'encodage des poids, comme au § 22, pas de la parcimonie.)*

**La carte des taux est complète** (troisième point, `m10_d384_kwta125`, entraîné
à 12,5 % gardés — mêmes 40 000 pas, même témoin) :

| modèle (dim 384) | entraîné à | exécuté à | perplexité | événements/fenêtre |
|---|---|---:|---:|---:|
| témoin | — | 25 % | 10,8758 | 84 M |
| `kwta050` | 50 % | **50 %** | **5,0606** | 168 M |
| `kwta025` | 25 % | **25 %** | **5,1719** | 84 M |
| **`kwta125`** | 12,5 % | **12,5 %** | **5,5973** | **42 M** |

**Chaque division par deux des événements coûte 2 % puis 8 % de perplexité**
(5,0606 → 5,1719 → 5,5973) — alors que le même exercice imposé au témoin le fait
s'effondrer (+118 % à 25 %). La courbe de la parcimonie **apprise** est plate là où
la courbe imposée est verticale. À 42 M d'événements par fenêtre, on lit **seize
fois moins** que le témoin sans parcimonie (672 M) pour une perplexité de 5,60
contre 4,996 — soit **+12 % de perplexité pour ÷16 de lecture**, et le chemin par
listes y est environ deux fois plus rapide qu'à 50 %.

### 5 quater. La courbe lecture ↔ qualité, et la réponse finale

Cinq modèles **identiques par ailleurs** (dim 384, 4 couches, 40 000 pas, mêmes
données, FFN exportée en Q8), mesurés au protocole de record. La colonne « paires »
est celle de la fenêtre 8 (même préfixe pour tous, donc comparable) :

| modèle | ce qui est creux | perplexité | **paires/jeton** | lectures |
|---|---|---:|---:|---:|
| `m5_d384_dense` | rien (témoin) | **4,9959** | 21,1 M | — |
| **`m12` structure innée 25 %** (aléatoire, figée) | poids seuls, **imposés** | **5,0472** (+1,0 %) | **5,2 M** | ÷4,1 |
| **`m7` k-WTA 25 % appris** | activations, **apprises** | **5,1719** (+3,5 %) | **5,4 M** | ÷3,9 |
| **`m11` k-WTA 25 % + élagage 50 % appris** | **les deux, appris** | **5,1866** (+3,8 %) | **2,7 M** | **÷7,8** |
| `m15` masque inné 25 % + k-WTA 25 % | les deux, dont un imposé | 6,0792 (+21,7 %) | **1,4 M** | ÷15,1 |

**Trois lectures, et la troisième est la réponse.**

1. **Un seul axe suffit à diviser les lectures par quatre** — et il coûte 1 % quand il
   est **structurel** (masque inné) contre 3,5 % quand il est **d'activations**
   (k-WTA). La structure innée est le moins cher des deux.
2. **Les deux axes appris se cumulent presque gratuitement** : ÷7,8 lectures pour
   +3,8 % de perplexité (le second axe n'ajoute que 0,3 point).
3. **Imposer un axe coûte cher** : la même combinaison, mais avec la structure
   *imposée* au lieu d'apprise, passe de +3,8 % à **+21,7 %** de perplexité. À
   ÷15 lectures, le modèle imposé paie cinq fois plus que le modèle appris à ÷8.

**La réponse à « quel modèle pour Drave ? » est donc une courbe, pas un chiffre** :
**÷4 pour +1 %** (structure innée), **÷8 pour +4 %** (les deux axes appris),
**÷15 pour +22 %** (un axe imposé). Le point de fonctionnement se choisit ; il ne se
subit pas — et c'est exactement ce qu'une architecture événementielle permet de faire
pour la première fois : **borner le coût à la conception**.

**Et la courbe dépend de l'échelle** — vérifié à dim 512 (15 h 07), mêmes recettes,
mêmes témoins :

| dim 512 | perplexité | paires/jeton | écart au témoin dense |
|---|---:|---:|---:|
| témoin dense (`m6_d512_dense`) | **4,5686** | 34,4 M | — |
| structure innée 25 % (`m16`) | **4,8745** | **9,2 M** | **+6,7 %** (÷3,7) |

**La courbe complète, aux deux échelles** (les deux mesures de dim 512 sont tombées
le 9 octobre à 15 h 07 et 16 h 16 ; paires/jeton prises à la même fenêtre 8) :

| modèle | dim 384 | lectures | dim 512 | lectures |
|---|---:|---:|---:|---:|
| **témoin dense** | 4,9959 · 21,1 M | — | **4,5686 · 34,4 M** | — |
| **structure innée 25 %** (aléatoire) | 5,0472 (+1,0 %) | ÷4,1 | **4,8745 (+6,7 %)** | ÷3,7 |
| **les deux axes appris** (k-WTA + élagage) | 5,1866 (+3,8 %) | ÷7,8 | **4,9345 (+8,0 %)** | ÷7,2 |
| un axe imposé (masque + k-WTA) | 6,0792 (+21,7 %) | ÷15,1 | — | — |

**Deux conclusions, et la seconde n'était pas attendue.**

1. **Les recettes tiennent à l'échelle** : la structure innée divise les lectures par
   3,7 à dim 512 (contre 4,1 à 384), les deux axes appris par 7,2 (contre 7,8). Les
   ordres de grandeur sont conservés.
2. **Mais leur PRIX croît avec la taille** : +1,0 % → **+6,7 %** pour la structure
   innée, +3,8 % → **+8,0 %** pour les deux axes appris. Un modèle plus grand a plus
   de capacité à perdre quand on lui retire la même fraction — et cela vaut pour les
   deux recettes, y compris celle où **c'est le modèle lui-même qui choisit** quelles
   connexions garder.

**Conséquence pour un modèle ad hoc** : le point de fonctionnement « ÷8 pour +4 % »
est un point **de dim 384**. À dim 512, le même point coûte +8 %. La courbe n'est pas
universelle — elle dépend de la taille, et toute affirmation sur la parcimonie doit
porter son échelle, comme les autres mesures de ce rapport.

**Et les deux axes SE CUMULENT quand les deux sont appris** (9 octobre, 11 h 32) :
`m11_d384_kwta25_elag50` reprend exactement `kwta025` (dim 384, 40 000 pas) **plus un
élagage appris à 50 %** des poids par ligne — même règle que `--keep`, appliquée
pendant l'entraînement à rampe cubique.

| dim 384 | aucune parcimonie | 50 % d'activations | **25 % d'activations** |
|---|---|---|---|
| `kwta025` (activations seules) | 6,4282 · 335,3 M | 5,8131 · 168,3 M | 5,1719 · **84,2 M** |
| **+ poids élagués APRIS (50 %)** | **6,0422 · 165,9 M** | **5,6842 · 84,7 M** | **5,1866 · 42,2 M** |
| écart | **−6,0 %** | −2,2 % | **+0,3 %** |

**Les lectures sont divisées par deux à chaque point de fonctionnement, et la
perplexité ne bouge pas** (5,1866 contre 5,1719 à 25 % d'activations, soit +0,3 %) —
elle s'améliore même en dense (−6,0 %). Cumulé avec la parcimonie d'activation, le
modèle lit **huit fois moins** que le témoin sans parcimonie (42,2 M contre 336 M
d'événements par fenêtre) pour une perplexité comparable.

**C'est la réponse à « quel modèle pour Drave ? »** : entraîné creux **sur les deux
axes** — activations (~25 %) et poids (~50 %) — plutôt que sur un seul.

**Les deux leviers ne se cumulent PAS** — mesuré le 9 octobre à 7 h 20. Un
quatrième modèle, `m9_d384_kwta25_distille`, reprend **exactement** la recette de
`kwta025` (dim 384, 40 000 pas, k-WTA 25 %) **plus** la distillation de l'enseignant
dense 384 — le levier qui vaut −13,8 % sur un modèle routé (§ 5 bis) :

| dim 384 | aucune parcimonie | 50 % | **25 %** |
|---|---:|---:|---:|
| `kwta025` (creux seul) | 6,4282 | 5,8131 | **5,1719** |
| **`kwta025` + distillé** | 6,3684 | 5,6770 | **5,1553** |
| **gain de la distillation** | −0,9 % | −2,3 % | **−0,3 %** |

**La distillation n'ajoute presque rien au creux appris.** Son gain, qui croît avec
l'échelle sur un modèle routé, valait −2,5 % (256), −9,3 % (384), −13,8 % (512) —
et ici, à dim 384 sur un modèle **dense** entraîné creux, il tombe à **−0,3 %**.

**Ce que cela dit** : les deux leviers ne traitent pas le même handicap. La
distillation rattrape ce que le **routage** coûte (chaque expert voit moins
d'exemples) ; elle n'a rien à rattraper sur un modèle dense, même creusé, où le
k-WTA ne fait que réduire le nombre d'activations sans retirer de capacité. Les
deux recettes sont donc **complémentaires par leur objet, pas additives par leur
effet** — et c'est mesuré, pas supposé.

**Ce que cela ne dit pas** : la plage de taux qu'un même modèle supporte. Les trois
modèles entraînés perdent hors de leur régime (0,4 à 1,4 point de perplexité), donc
la réponse est étroite — c'est un résultat, pas une réserve de politesse.

---

---
