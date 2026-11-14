# J12.1 — Le §334 et les 44 œuvres : le retrieval et la prédiction de l'époque vs la filiation

> **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : Panini, J12.1 · **Date** : 2026-11-14
> **Verdict** : ✅ **le §334 est une géométrie de filiation, pas d'époque — et le corpus ne permet pas
> de séparer les deux.** La loi H0 de Panini se reproduit (**R² = 0,909139** sur les **655 lignes** de
> paires ; **0,906307** sur les **488 paires uniques non auto**), et l'époque seule explique **0,258**
> de la distance lexicale ; mais elle n'ajoute que **0,0089** de R² **après** la topologie
> (p = 0,86 ; β standardisé **−0,035**). Le plan est **colinéaire** : **180** paires de même tradition
> ont **28,7 ans** d'écart en moyenne (max **230**), les **308** paires inter-traditions en ont
> **1 189** (**136** à ≤ 100 ans). Le contraste de filiation à **date fixe** est fort dans la tranche
> axiale (**Δ = −0,166**, p = 0,0005), mais **disparaît à surface contrôlée** (même langue source
> anglaise : **Δ = −0,135** contre un null de **−0,129**, p = 0,34).
> Sur les **44 signatures** (14 parts flottantes), le retrieval brut donne **61,4 %** de même tradition
> (hasard 22,4 %) et **56,8 %** de voisins à ≤ 50 ans (hasard 22,8 %) ; les contrôles croisés ramènent
> la filiation à **50,0 %** (p = 0,0492, **Holm 0,128**) et l'époque à **53,8 %** (p = 0,373). Seule une
> **petite** prédiction d'année intra-tradition survit (**R² = 0,042**, p = 0,0086, **Holm 0,034**).
> Le β époque **+0,138** de la validation v150 **n'est pas reproduit** : sur **374** paires, le
> coefficient de date est **négatif** (**−0,006**) et non significatif. L'avertissement de Panini n'est
> donc **ni confirmé ni réfuté** ici : **l'époque n'est pas séparable de la filiation dans ce corpus**, et
> la signature V14 est surtout une signature de **source/traduction**.
> **Dispositif** : les artefacts §334 de Panini/Nipada, lus en **lecture seule** — `pairs334_axes_v1.json`
> (**655 lignes**, **495 paires uniques**, **7 auto-paires**, **160 doublons** de lignes), le graphe
> `nipada_v334_graph_v35.json` (1 753 nœuds) pour les dates, les traditions et les langues,
> `analytic_sigs_v1.json` (**44 œuvres × 14 atomes**), `sources_coverage.json` / `sources_manifest.json`
> (**102/107 sources acquises**, **71 URL uniques non vides**), et la validation `nipada_v150_validation.json`
> pour la comparaison. Deux niveaux : **paire** (H0, date, filiation, contrôles) et **œuvre**
> (retrieval top-1, prédiction kNN/ridge, contrôles croisés). **Contrôles négatifs** : étiquettes de
> tradition permutées dans des tranches de **250 ans** ; années permutées **dans chaque tradition** ;
> signatures permutées entre œuvres ; années, traditions et `d_topo` permutés au niveau des textes ou
> des paires ; doublons exacts retirés ; paires `eng–eng` seules ; **4 tests principaux** corrigés par
> Holm-Bonferroni.
> **JSON** : [`panini-334.json`](panini-334.json) · **Outil** : [`../tools/panini_334.py`](../tools/panini_334.py).
> **Ce qui pourrait le rendre faux** : 44 œuvres et 10 traditions (19 GRECO), IC larges ; signatures de
> **traductions anglaises** alors que la date est celle de la **composition** ; `d_topo` est une distance
> de **transmission**, corrélée à la date (ρ ≈ 0,61) ; les **44 signatures ne sont pas** les vecteurs qui
> produisent `d_lex`/`cos` des 655 paires (r ≈ 0,37) ; les doublons et auto-paires du fichier de paires ;
> les seuils (50 ans, 250 ans, cos 0,99999) sont des conventions. Voir § 8.

## 1. La question

Panini et Nipada ont trouvé que leur **signature lexicale** capte **l'époque** (β **+0,138**) bien plus
que la **filiation** (β **+0,049**) : *la surface transmet les signifiants, pas la généalogie*
([`panini-nipada.md`](../docs/methode/panini-nipada.md)). Leur remède est de **contrôler la date** dans
tout test de style et la **surface** dans tout test de famille.

J3.1 avait mesuré le retrieval de surface sur des langues et trouvé que le **brut** est un effet de
composition (l'écriture domine) ; J3.2 avait montré que la « filiation » de Panini est une distance de
**tradition**, pas de famille de langues ; J7.1 avait séparé la **sœur** de la famille lointaine. J12.1
attaque la **deuxième vague** : le corpus **§334** (l'étiquette « 114 textes, 655 paires, 102 sources »)
et les **signatures de 44 œuvres** (14 flottants). La question est double :

1. **Retrieval** — le plus proche voisin d'une œuvre dans l'espace des 14 atomes partage-t-il sa
   **filiation** (tradition, auteur) ou son **époque** (année proche) ?
2. **Prédiction** — la signature prédit-elle mieux l'**année** ou la **tradition** ? Et que restent ces
   deux prédictions quand on **contrôle l'autre variable** ?

La réponse courte est que le corpus **ne permet pas** de poser la question dans les deux sens : la
filiation et l'époque y sont presque confondues, et les deux signaux bruts sont largement des effets de
composition — de tradition, de date et de **source/traduction**.

## 2. Le matériau et son audit — 114, 655, 102, 48, 44

Le corpus est annoncé comme **114 textes actifs** (104 traditions + 10 références), **655 paires** et
**102 sources**. La lecture des fichiers donne une image plus étroite, qu'il faut poser avant toute
mesure :

| ce qui est annoncé | ce que le fichier contient | lecture |
|---|---:|---|
| **114 textes actifs** | **48 identifiants distincts** dans les 655 paires | **66** des 114 n'apparaissent dans aucune paire finie ; « 114 » est une étiquette de corpus, pas un échantillon de retrieval |
| **655 paires** | **495 paires uniques** (non ordonnées) ; **488** sans auto-paire | **160 doublons** de lignes et **7 auto-paires** (toutes `aristotle_*`, `d_topo = 0`) |
| **102 sources** | **102/107** acquisitions `ok` ; **80 URL non vides**, **71 URL uniques** | 102 est le nombre de **sources acquises**, pas 102 URL distinctes ; **45/48** textes des paires et **44/44** œuvres signées ont une source |
| **44 œuvres signées** | **44** signatures V14 (14 parts, somme 1) | les **4** textes sans signature sont `an7_64_kodhana`, `aristotle_de_anima`, `brahma_sutra_badarayana`, `zadeh_1965` |
| **traductions** | **24** sources `eng`, **1** `fra`, **19** langue inconnue | la surface est massivement **anglaise** ; 19 œuvres n'ont pas de langue source documentée |

Les **655 lignes** se répartissent en **459** intra-tradition (`a`), **180** référence × tradition (`b`)
et **16** intra-références (`c`). Les **160 doublons** ne sont pas anodins : les couples
`aristote × aristote` apparaissent jusqu'à **4 fois**, et les **7 auto-paires** sont l'artefact déjà
documenté par Panini (`nid_b == nid_a`). L'inférence est donc faite sur les **488 paires uniques non
auto** ; la reproduction officielle reste calculée sur les **655 lignes**.

**Deux instruments, pas un.** Les **44 signatures** de `analytic_sigs_v1.json` ne sont **pas** les
vecteurs qui ont produit `d_lex` et `cos` dans le fichier de paires : sur les **490 lignes** où les deux
existent, le cosinus recalculé sur les 14 atomes et le `cos` du fichier de paires ont **r ≈ 0,37** ; la
distance L2 des signatures et `d_lex` ont **r ≈ 0,48**. Les deux niveaux mesurent donc deux choses
différentes : une **distance lexicale** (655 paires) et une **signature d'atomes** (44 œuvres). On ne
peut pas transporter mécaniquement l'une dans l'autre ; c'est une limite, pas un détail.

## 3. Le protocole

### 3.1 Niveau paire — la loi H0, l'époque, la filiation

Sur les **488 paires uniques non auto**, on ajuste :

- **H0 (filiation/topologie)** : `d_lex ~ 1 + d_topo^0,67` ;
- **époque seule** : `d_lex ~ 1 + |Δannée|/100` ;
- **joint** : `d_lex ~ 1 + d_topo^0,67 + |Δannée|/100` ;
- **inverse** : `d_topo^0,67 ~ 1 + |Δannée|/100` ;
- **tradition** : `d_lex ~ 1 + même_tradition_large`, puis avec `d_topo^0,67`.

Les coefficients standardisés et les **R² partiels** disent quelle variable porte la variance **quand
l'autre est présente**. Les IC sont des **bootstrap par texte** (1 000 tirages) ; les p-values sont des
**permutations au niveau des textes** (2 000), pas des p-values OLS — les paires ne sont pas
indépendantes.

### 3.2 Niveau œuvre — retrieval et prédiction

Pour les **44 signatures**, on classe les autres œuvres par **cosinus** (les doublons exacts sont
retirés des candidats). Le **top-1** est dit :

- **filiation** s'il partage la **tradition large** (GRECO, ABRAHAMIC, BUDDHIST, CHINESE, MILLENARIAN,
  FORMAL_LOGIC, COGNITIVE_SCIENCE, etc.) ou l'**auteur canonique** ;
- **époque** s'il est à **≤ 50 ans** (seuil de J3.1 ; 100 ans en sensibilité).

La **tradition large** est un regroupement explicite : `GRECO_LATIN_AXIAL` + `GRECO_PLATONIC` → `GRECO`,
`ABRAHAMIC_PROPHETIC_AXIAL` + `JUDEAN_APOCALYPTIC_LATE` → `ABRAHAMIC`, les logiques → `FORMAL_LOGIC`,
les sciences cognitives → `COGNITIVE_SCIENCE`. Ce regroupement est nécessaire parce que les étiquettes
brutes séparent le **même texte** (`plato_gorgias` vs `plato_gorgias_jowett`) et le **même auteur**
(`plato` vs `Platon (Jowett)`). La version fine est dans le JSON ; les résultats ne changent pas de
sens, mais les taux de la version fine sont plus bas.

La prédiction est **leave-one-out** : kNN (k = 1, 3, 5) sur les signatures pour l'**année** et pour la
**tradition**, plus une **ridge** standardisée pour l'année. Les nulls :

- **date contrôlée** : étiquettes de tradition permutées **dans chaque tranche de 250 ans** ;
- **filiation contrôlée** : années permutées **dans chaque tradition** ;
- **signatures permutées** : signatures assignées aux mauvaises œuvres ;
- **surface** : paires `eng–eng` seulement (24 œuvres, 276 paires).

### 3.3 Les tests principaux et la correction

Quatre tests sont déclarés **principaux** avant lecture : retrieval de filiation (date contrôlée),
retrieval d'époque (filiation contrôlée), prédiction de tradition (date contrôlée), prédiction d'année
(filiation contrôlée). Ils sont corrigés par **Holm-Bonferroni** (m = 4). Les autres chiffres sont
descriptifs ou secondaires ; les p-values brutes sont données pour permettre au lecteur de refaire la
correction.

## 4. Résultats au niveau paire — la filiation porte, l'époque n'ajoute rien

### 4.1 La H0 se reproduit, et elle est robuste à la dé-duplication

| modèle | n | R² | lecture |
|---|---:|---:|---|
| **H0 officielle** (655 lignes) | 655 | **0,909139** | reproduction bit-exacte de Panini (écart 3 × 10⁻⁷) |
| **H0 sur paires uniques non auto** | 488 | **0,906307** | la loi ne dépend pas des doublons ; écart 0,0028 |
| **époque seule** | 488 | **0,257876** | la date seule explique 25,8 % |
| **joint** | 488 | **0,907142** | la date n'ajoute que **0,0089** de R² partiel après la topologie |
| **inverse** (`d_topo^0,67 ~ date`) | 488 | **0,312020** | la topologie est elle-même datée : ρ = 0,61 |

Le modèle joint standardisé donne **β(d_topo^0,67) = 0,971** et **β(|Δannée|/100) = −0,035** : à
topologie fixée, l'écart de dates **n'augmente pas** la distance lexicale ; il la diminue très
légèrement, et le R² partiel de la date est **0,0089** (p = 0,86 par permutation des années entre
textes). La **date seule** est significative (p = 0,0005), mais elle est **absorbée** par la topologie.
Le bootstrap par texte donne : R² H0 **[0,852 ; 0,942]**, R² date **[0,028 ; 0,517]**, R² partiel de la
date **[−0,025 ; 0,133]**, R² partiel de la topologie **[0,759 ; 0,930]**.

### 4.2 Le plan est colinéaire — et c'est le résultat principal

| groupe | n | Δannée moyen | médiane | max | queue |
|---|---:|---:|---:|---:|---|
| **même tradition large** | 180 | **28,7 ans** | 20 | **230** | 5 paires > 100 ans |
| **tradition différente** | 308 | **1 189,2 ans** | 1 200 | 2 412 | **136** paires ≤ 100 ans |

Autrement dit : **les couples de même tradition sont presque tous contemporains**, et **les couples
longs sont presque tous inter-traditions**. Il n'existe que **5** paires de même tradition à plus de
100 ans (toutes des prophètes hébreux), contre **136** paires inter-traditions à moins de 100 ans. Un
modèle qui met `d_topo` et `|Δannée|` côte à côte ne peut donc pas identifier les deux effets : la
topologie **contient** la date, et la date **contient** la tradition.

### 4.3 À date fixe, la filiation survit — mais la surface la retire

Dans la tranche axiale (**−500 à −250 ans**, 300 paires uniques non auto), les paires de même
tradition ont une distance lexicale de **0,106** contre **0,272** pour les autres : **Δ = −0,166**. Le
contrôle de date (étiquettes permutées dans chaque tranche de 250 ans) donne un null à **−0,001**,
p = **0,0005**. C'est le contraste de filiation le plus net du corpus.

Mais il **ne survit pas à la surface**. En se restreignant aux paires de **même langue source connue**
(`eng–eng`, 98 paires, 27 de même tradition), le contraste tombe à **Δ = −0,135** et le null de
permutation à date contrôlée vaut **−0,129** : p = **0,335**. Dans la tranche axiale et à même langue
source, il ne reste que **21 paires** (7 de même tradition) et **Δ = −0,054**. Le contraste de
filiation à date fixe est donc **concentré dans les paires grecques / non grecques**, où la langue
source n'est pas documentée : on ne peut pas le distinguer d'un effet de **source/traduction**.

### 4.4 La tradition seule, et ce qu'elle devient après la topologie

`d_lex ~ 1 + même_tradition_large` donne **R² = 0,369** et **β = −0,189** : les paires de même
tradition sont plus proches. Mais après `d_topo^0,67`, le coefficient de la tradition devient
**−0,0067** et le R² partiel **0,0030** (p = 0,49) : la topologie **absorbe** la tradition. Ce n'est
pas une contradiction : `d_topo` est la distance de transmission qui **définit** la filiation ; le label
de tradition n'ajoute presque rien à sa version topologique. La question « filiation vs époque » au
niveau paire est donc, de fait, « **topologie vs date** » — et la topologie gagne.

## 5. Résultats au niveau œuvre — le retrieval brut, et ce que les contrôles en gardent

### 5.1 Le top-1 brut

| cible du top-1 | observé | hasard | enrichissement | n/44 |
|---|---:|---:|---:|---:|
| **même tradition large** | **61,4 %** | 22,4 % | **2,74×** | **27** |
| **même auteur canonique** | **36,4 %** | 10,0 % | **3,64×** | **16** |
| **à ≤ 50 ans** | **56,8 %** | 22,8 % | **2,49×** | **25** |

Le retrieval brut « voit » donc **les deux** : la tradition et l'époque. C'est exactement le piège que
J3.1 avait trouvé sur les langues : un brut qui mélange deux variables corrélées. Les contrôles croisés
séparent.

### 5.2 Date contrôlée vs filiation contrôlée

| contrôle | observé | null | p brut | p Holm |
|---|---:|---:|---:|---:|
| **filiation** (top-1 même tradition, étiquettes permutées dans les tranches de 250 ans) | **61,4 %** | **50,0 %** | **0,0492** | **0,128** |
| **époque** (top-1 ≤ 50 ans, années permutées dans chaque tradition) | **56,8 %** | **53,8 %** | **0,373** | 0,373 |
| **filiation, exactitude équilibrée** (même null) | **30,6 %** | **22,0 %** | **0,092** | — |

La filiation **perd 11,4 points** au contrôle de date (61,4 → 50,0) et devient **marginale** après
Holm (0,128). L'époque **perd 3 points** au contrôle de filiation (56,8 → 53,8) et n'est **pas**
significative (0,373). Le top-1 d'époque **brut** (56,8 %) est donc presque entièrement expliqué par
la tradition : les œuvres d'une même tradition sont aussi proches dans le temps.

Le **top-1 moyen** garde une petite trace : **235 ans** d'écart contre **270 ans** sous le null de
filiation (p = 0,0094). Mais le seuil **≤ 50 ans** ne la voit pas (p = 0,373) : la trace est dans la
queue, pas dans le voisinage immédiat.

### 5.3 Prédiction — l'année brute, la tradition, et le résidu

| prédiction | observé | baseline / null | lecture |
|---|---:|---:|---|
| **année, kNN k=1** | MAE **235,4** ; R² **0,614** | médiane **612,4** ; null global **945,3** | l'année brute est très prédite |
| **année, null dans chaque tradition** | MAE **235,4** | **270,1** ; p = **0,0086** | il reste un petit signal **au-delà** de la tradition |
| **année, résidu intra-tradition** | MAE **55,7** ; R² **0,042** | **82,2** ; p = **0,033** | 4,2 % de la variance intra-tradition |
| **tradition, kNN k=1** | exactitude **61,4 %** ; équilibrée **30,6 %** | majorité **43,2 %** ; null date **50,0 %** (p = 0,043) | l'exactitude est portée par GRECO (19/44) |
| **tradition, équilibrée** | **30,6 %** | null date **22,0 %** (p = 0,092) | pas significatif après date |

La lecture est nette : **l'année brute est très prédite** (R² 0,614), mais **presque toute** cette
prédiction est de la **tradition** (le null intra-tradition monte à 270 ans de MAE, contre 945 ans en
global). Il reste **4,2 %** de variance intra-tradition (p = 0,033), et c'est le **seul** test qui
survit à Holm (p = 0,034). La tradition est prédite au-dessus de la majorité, mais **l'exactitude
équilibrée** (30,6 %) et le null de date (22,0 %, p = 0,092) montrent que le modèle retrouve surtout
**GRECO** (17/19) et **ABRAHAMIC** (6/8) ; les petites traditions (BUDDHIST, CHINESE, MILLENARIAN,
NORSE, etc.) échouent.

### 5.4 Surface — `eng–eng`, et les doublons

Sur les **24 œuvres de source anglaise** (276 paires), le modèle `cos ~ même_tradition + log(1+|Δannée|)`
donne **R² = 0,016** : la tradition n'explique presque rien de la similarité des signatures, et la date
encore moins (β ≈ 8,7 × 10⁻⁶). Le top-1 reste à **50 %** de même tradition (hasard 15,2 %) et **37,5 %**
à ≤ 50 ans (hasard 9,1 %) — mais avec **24 requêtes**, ces taux sont fragiles et ne sont pas le même
objet que le modèle continu. **La surface ne confirme pas la filiation** ; elle ne la réfute pas non
plus, elle montre que le signal est surtout **entre** groupes de sources, pas **dans** une langue.

Les **doublons exacts** (`plato_gorgias`/`plato_gorgias_jowett`, `plato_meno`/`plato_meno_jowett`,
cos = 1) sont retirés des candidats : le top-1 tradition reste **61,4 %**, le top-1 ≤ 50 ans monte à
**59,1 %**. Ils ne portent donc pas la conclusion ; ils la rendent seulement plus propre.

## 6. La tentative de reproduction de la v150 — le β époque n'est pas là

La validation `nipada_v150_validation.json` publie, sur 10 œuvres :
`d_sig ≈ 0,159 + 0,049·d_graph + 0,138·(Δyear/1000) + 0,002·même_tradition`, **R² = 0,3004**.
On reconstruit la même forme sur les **374 paires uniques non auto** des 44 signatures, avec
`d_sig` = distance L2 des 14 atomes et `d_topo` à la place de `d_graph` :

| terme | β brut (nous) | β standardisé (nous) | β publié (v150) |
|---|---:|---:|---:|
| `d_topo` | **+0,0027** | **+0,264** | +0,0489 |
| `Δannée/1000` | **−0,0060** | **−0,148** | **+0,1378** |
| même tradition | **−0,0366** | **−0,879** | +0,0022 |
| **R²** | **0,3092** | — | 0,3004 |

Le R² est du même ordre (0,309 contre 0,300), mais le **signe du coefficient de date est inversé** :
il est **négatif** (**−0,0060**) et non significatif (p = **0,093** par 2 000 permutations des
années entre œuvres). Le **+0,138** de la v150 n'est donc **pas reproduit** sur les
44 signatures du §334. Deux réserves :

1. **Les échelles diffèrent** : comparer 0,138 (par 1 000 ans) et 0,049 (par unité de `d_graph`) est
   **dépendant de l'unité**. La v150 compare des β bruts dont les régresseurs n'ont pas la même
   échelle ; notre version standardisée donne **0,264 vs −0,148**, ce qui renverse la hiérarchie.
2. **Le `d_sig` reconstruit n'est pas celui de la v150** : la v150 utilise peut-être une autre
   normalisation, et son corpus de 10 œuvres n'est pas les 44 signatures. Ce n'est donc pas une
   réfutation de la v150 ; c'est la **non-reproduction sur le §334**, avec un instrument voisin.

## 7. Ce que cela dit de l'avertissement de Panini

1. **La loi H0 du §334 est une loi de filiation/topologie**, pas d'époque : R² = 0,909139 sur les 655
   lignes, 0,906307 sur les 488 paires uniques ; la date seule explique 0,258, mais n'ajoute que
   0,0089 après la topologie (p = 0,86).
2. **Le plan est colinéaire** : 180 paires de même tradition à 28,7 ans d'écart (max 230), 308 paires
   inter-traditions à 1 189 ans (136 à ≤ 100 ans). Le corpus **ne peut pas** identifier un effet
   d'époque indépendant de la filiation ; il ne peut pas non plus identifier une filiation indépendante
   de la date.
3. **À date fixe, la filiation est forte** dans la tranche axiale (Δ = −0,166, p = 0,0005), mais
   **elle disparaît à surface contrôlée** (Δ = −0,135 contre null −0,129, p = 0,335). Le signal est
   donc au moins autant **source/traduction** que tradition.
4. **Sur les 44 signatures**, le brut penche pour la filiation (61,4 % vs 22,4 %) et pour l'époque
   (56,8 % vs 22,8 %), mais les contrôles croisés ramènent la filiation à 50,0 % (p = 0,0492, Holm
   0,128) et l'époque à 53,8 % (p = 0,373). **Aucun des deux n'est fort**.
5. **La seule prédiction qui survit à Holm** est une **petite** prédiction d'année intra-tradition
   (R² = 0,042, p = 0,0086, Holm 0,034) : il reste une trace d'époque, mais 96 % de la variance
   intra-tradition n'est pas expliquée.
6. **Le β époque +0,138 de la v150 n'est pas reproduit** sur le §334 : le coefficient de date
   reconstruit est **négatif** (−0,006) et non significatif. L'avertissement doit être **indexé à son
   corpus et à son instrument** : il décrit la validation v150, pas le §334.

**La convergence avec J3.1/J3.2/J7.1** est de forme : partout, le **brut** fait apparaître un effet
que les contrôles attribuent à une **composition** (écriture, famille, date, source). Ici, la
composition est **date × tradition × source** ; le §334 ne permet pas de démêler les trois. La
divergence avec Panini est réelle mais **bornée** : leur signature d'atomes est peut-être un bon
détecteur d'époque sur leur corpus de validation ; elle ne l'est pas sur les 44 œuvres du §334, et
leur propre loi H0 est une loi de **filiation**, pas d'époque.

## 8. Ce qui pourrait rendre ce résultat faux

1. **Petit n et classes déséquilibrées.** 44 œuvres, 10 traditions, **19 GRECO** ; le top-1 de
   filiation vaut 27/44, l'IC bootstrap est **[0,467 ; 0,724]**, et le p = 0,0492 devient **0,128**
   après Holm. Un corpus de 100 œuvres pourrait renverser la conclusion.
2. **La date est celle de la composition, pas de la traduction.** 24/44 sources sont anglaises, 1
   française, 19 de langue inconnue ; les signatures sont calculées sur des traductions
   majoritairement du XIXe–XXe siècle. Le test d'époque est donc **biaisé contre** un effet de la date
   de composition. Un corpus avec les dates de traduction pourrait montrer l'époque que celui-ci ne
   peut pas voir.
3. **La colinéarité n'est pas un détail.** Les 5 seules paires de même tradition à > 100 ans sont des
   prophètes hébreux ; les 136 paires inter-traditions à ≤ 100 ans sont surtout des grecs/Chinois. Le
   plan n'a pas de **support commun** : on ne peut pas distinguer « même tradition » de « même
   époque » par régression, seulement par stratification — et les strates sont minces.
4. **`d_topo` est une distance de transmission, pas de famille.** Elle est corrélée à la date
   (ρ = 0,61) et construite sur le même graphe qui a servi à sélectionner le corpus. La H0 n'est donc
   pas une preuve **indépendante** que la signature capte la filiation ; c'est une loi de cohérence
   interne au graphe.
5. **Deux instruments.** Les 44 signatures ne sont pas les vecteurs de `d_lex`/`cos` (r ≈ 0,37). Les
   conclusions du niveau paire ne se transportent pas au niveau œuvre, et réciproquement. On l'a
   traité comme deux mesures, pas comme une seule.
6. **Doublons et auto-paires.** 160 doublons de lignes, 7 auto-paires ; la H0 passe de 0,909139 (655
   lignes) à 0,906307 (488 paires). Les doublons sont surtout des couples d'Aristote ; ils peuvent
   modifier les moyennes et les tests. On a rapporté les deux bases.
7. **Dates estimées.** Les années sont des estimations (`year_uncertainty` non utilisée), les
   négatifs sont des siècles, et les modernes vont de 1920 à 2013. Un décalage de 50 ans n'a pas le
   même sens à −400 et à 2000.
8. **Seuils et tests multiples.** 50 ans, 250 ans, cos 0,99999 sont des conventions ; les sensibilités
   sont dans le JSON, mais pas toutes les combinaisons. Les 4 tests principaux sont corrigés ; les
   autres p-values sont descriptives.
9. **Le corpus n'est pas les 114 textes.** 48 textes dans les paires, 44 signatures ; 66 textes actifs
   n'apparaissent pas. Les résultats ne disent rien de ces 66 textes, ni des 5 sources non acquises.
10. **Qualité des textes.** Certaines sources sont des fragments, des traductions anciennes ou des
    pages web ; la signature de 14 atomes peut être dominée par le **genre**, la **longueur** ou le
    **traducteur**, pas par la tradition.

## 9. Fichiers et reproduction

| fichier | rôle |
|---|---|
| [`../tools/panini_334.py`](../tools/panini_334.py) | le dispositif complet (paires, signatures, retrieval, prédiction, contrôles) |
| [`panini-334.json`](panini-334.json) | tous les chiffres : audit, 488 paires, 44 signatures, modèles, permutations, bootstrap, p-values |
| `../Panini/research/nipada/falsification/pairs334_axes_v1.json` | les 655 lignes de paires (SHA-256 dans le JSON) |
| `../Panini/research/nipada/falsification/nipada_v334_graph_v35.json` | le graphe v35, les dates, traditions, langues |
| `../Panini/research/nipada/falsification/analytic_sigs_v1.json` | les 44 signatures V14 |
| `../Panini/research/nipada/corpus/_cache/sources_coverage.json` | les 102/107 sources acquises |
| `../Panini/research/nipada/falsification/nipada_v150_validation.json` | la validation v150 (β +0,138) |

Reproduction :

```bash
python3 tools/panini_334.py                 # ~65 s, 5 000 permutations, 1 000 bootstraps
python3 tools/panini_334.py --rapide        # ~10 s, 500 permutations, 300 bootstraps
python3 tools/panini_334.py --sortie /tmp/panini-334.json
```

Le script lit Panini en **lecture seule** (SHA-256 et commit dans le JSON) et écrit
`reports/panini-334.json`. Les contrôles négatifs sont dans `paires.permutations`,
`oeuvres.retrieval_nulls`, `oeuvres.prediction.*.nulls`, `paires.contraste_date_surface` et
`oeuvres.signatures_permutees`.

## 10. Verdict et suite

- **J12.1 est mesuré, écrit, contrôlé.** Le §334 est une **géométrie de filiation** : la H0 se
  reproduit, la date n'ajoute rien après la topologie, et le plan est **colinéaire**. Le retrieval brut
  des 44 signatures donne la filiation et l'époque, mais les contrôles croisés ne gardent qu'une
  **petite** prédiction d'année intra-tradition (R² = 0,042, Holm 0,034) ; la filiation est **marginale**
  après Holm (0,128).
- **La leçon pour la roadmap** : l'avertissement de Panini ne se transporte pas au §334 sans son
  corpus et son instrument. Toute mesure de style sur ce corpus doit **strater par tradition, date et
  source** ; toute mesure de famille doit **strater par surface**. La prochaine mesure est **J12.2**
  (le vérificateur indépendant du corpus d'or CIC, 42 verdicts), puis **J13.1** (la table des mesures).
- **Ce qui reste ouvert** : les dates de **traduction** (pour tester l'époque de la surface), une
  signature V14 **multilingue** (pour séparer langue et tradition), et un corpus avec **support commun**
  same-tradition × longue époque (pour identifier les deux effets). Ces trois mesures manquent ; elles
  ne sont pas des résultats négatifs.
