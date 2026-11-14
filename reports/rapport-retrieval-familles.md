# J7.1 — Le retrieval approfondi par famille Glottolog

> **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : Panini, J7.1 · **Date** : 2026-11-14
> **Verdict** : ✅ **le retrieval retrouve la famille, mais seulement dans la même écriture — et il faut
> des sœurs pour le voir.** Sur les 532 textes UDHR (445 langues distinctes après déduplication, 1948),
> le top-1 de voisinage est de la même famille dans **66,1 %** des cas (hasard 10,3 %) et de la même
> branche (sœur) dans **26,1 %** (hasard 2,5 %). Mais **hors écriture, tout retombe au hasard** :
> famille 9,9 % contre 8,1 %, sœur 0,7 % contre 0,8 %. Dans la même écriture, la famille monte à
> **69,8 %** (hasard 16,2 %) et la sœur à **27,8 %** (hasard 5,7 %). Le retrieval parallèle 30 articles
> le confirme et le chiffre : sur les **25 langues LANG_TREE** disponibles, les sœurs valent **0,619**
> (60 paires), les mêmes familles d'une autre branche **0,170** (216), les familles différentes
> **0,0445** (324) — **13,9×**, Δ **+0,574** [0,490 ; 0,655], coefficient de sœur **+0,448**
> (p = 0,002) contre +0,213 pour l'écriture. Sur l'**échantillon 20**, le même contraste est **nul** :
> sœurs 0,0583 (12 paires) contre 0,0757 pour les familles-autres-branches et 0,0389 pour les
> différentes ; le coefficient de sœur (+0,0154, p = 0,078) ne se distingue pas de zéro. **J3.1 est
> reproduit à l'identique** (écart 0) ; son coefficient de famille (+0,0556) n'était pas faux, il était
> **sous-dimensionné** : l'échantillon 20 ne contient que 12 paires de sœurs, dont 8 hors écriture.
> L'époque est **mono-époque par construction** (1948) ; le placebo de dates donne −0,0013
> [−0,065 ; +0,041], et le seul bras daté de J3.1 (Bible) donne −0,034/siècle (p = 0,19) contre +0,609
> pour l'écriture. L'écriture est la **porte** : hors écriture, tout est au hasard. **À l'intérieur de
> l'écriture, sur LANG_TREE, la sœur est le premier effet** (+0,448 contre +0,213 pour l'écriture), puis la
> famille-autre-branche (+0,092), puis l'époque (nulle). L'époque ne peut pas expliquer l'effet de
> famille ici.**
> **Dispositif** : 532 textes Panini (article 1, 1948), **521 étiquetés Glottolog**, **447 groupes ISO**,
> **445 textes distincts** (74 variantes ISO et 2 doublons de texte exact retirés) ; **25 langues
> LANG_TREE** (26 codes mappés, 3 absentes de l'UDHR : `grc`, `pli`, `lzh` ; `per` et `fas` pointent vers
> le même texte) ; **20 strates** du corpus commun ; **21 langues de J3.1** ; **30 articles** Drave pour
> le parallèle. Même retrieval que J3.1 (n-grammes de caractères n = 3, TF-IDF, cosinus, top-1/MRR),
> fonctions importées de `retrieval_epoque.py` pour que la reproduction soit exacte.
> **Contrôles négatifs** : permutations d'étiquettes de famille/chemin (1 000 pour le global, 500 pour
> le parallèle), requêtes permutées (200), candidats mélangés (permutation sans point fixe des
> 30 articles), placebo de dates (200), leave-one-language-out (25/39 langues), et reproduction exacte
> de J3.1 (écart maximal 0).
> **JSON** : [`retrieval-familles.json`](retrieval-familles.json) · **Outil** :
> [`../tools/retrieval_familles.py`](../tools/retrieval_familles.py).
> **Ce qui pourrait le rendre faux** : le retrieval est de **surface**, pas neuronal ; le global ne porte
> que l'**article 1** ; l'UDHR est **mono-époque** ; les variantes proches et les doublons de texte
> gonflent le signal de sœur ; la définition de « sœur » (LCA ≥ 3) est une convention ; les paires ne
> sont pas indépendantes ; 11 textes restent non étiquetés. Voir § 6.

## 1. La question

J3.1 a mesuré le retrieval de surface sur **21 langues UDHR** (30 articles, 1948) : top-1 **0,0494**,
écriture **+0,0619**, famille **+0,0556**, R² **0,1396**. J3.2 a montré que, sur ces 21 langues, le
signal de famille vit dans **2-3 paires** (`ind–jav`, `eng–fra`) et que les **154 paires hors écriture**
sont exactement au hasard.

J7.1 demande d'**approfondir** : prendre les **532 langues UDHR de Panini** (même source XML, article 1),
mesurer le retrieval **par famille Glottolog** sur les **29 langues de `language_genealogy.py`** et sur
l'**échantillon 20** du corpus commun, avec le **contrôle d'époque**, et comparer à J3.1.

La question n'est donc pas « la famille compte-t-elle ? » — J3.1 et J3.2 ont déjà répondu *un peu, mais
moins que l'écriture* — mais : **de quelle famille parle-t-on ?** Un échantillon de 21 langues peut
contenir beaucoup de familles et peu de **sœurs** ; un jeu choisi pour la généalogie peut en contenir
beaucoup. Le retrieval doit être lu à ce niveau, sinon le coefficient de « famille » mélange deux
choses : la **sœur** (même branche proche) et la **famille lointaine** (même macro-famille, autre
branche). C'est cette séparation que J7.1 mesure.

## 2. Le matériau — 532 textes, 445 langues, trois jeux

### 2.1 Le corpus et sa couverture

| étape | n | lecture |
|---|---:|---|
| textes Panini (article 1) | **532** | le fonds, même source XML que Drave |
| étiquetés Glottolog | **521** | 97,9 % ; 11 restent non étiquetés |
| groupes ISO | **447** | 74 variantes d'une même langue (même ISO3) |
| **textes distincts** | **445** | 2 doublons de texte exact entre codes ISO différents retirés |

Les **11 textes non étiquetés** sont **dix variantes numériques** de l'UDHR dont le nom est entre
parenthèses (`013`, `014`, `016`, `017`, `021`, `022`, `023`, `025`, `026`, `050`) et **`062`**
(`Swahili (Chimwiini)`, dont le code `swb` est le maore, pas le chimwiini : on ne devine pas). Ils ne
sont pas devinés : ils sortent des mesures de famille, pas du comptage des textes.

Les **12 groupes de textes identiques** (24 textes) sont un fait du fonds : l'UDHR réutilise parfois la
même traduction sous deux codes. Neuf groupes sont déjà dédupliqués par l'ISO3 (`deu_1901`/`deu_1996`,
`ell_monotonic`/`ell_polytonic`, `ron_1993`/`ron_2006`, etc.) ; **deux** survivent à la déduplication ISO
et sont retirés par le texte : `ckb`/`kmr` (kurde central / kurde du nord) et `kng`/`ktu`
(kikongo / kituba). Sans ce retrait, deux textes identiques fabriqueraient un top-1 « famille » trivial.
Le troisième doublon cross-ISO (`bos_latn`/`hrv`) n'est pas dans les représentants : le groupe `bos`
a choisi `bos_cyrl`, qui n'est pas identique à `hrv`.

**Ce que « 445 langues » veut dire.** Le global mesure **445 textes distincts**, pas 532 textes
indépendants. Les 532 restent la base ; les 445 sont la base **dédupliquée** qui rend les top-1
interprétables. La sensibilité sur les 504 textes non dédupliqués (avant retrait des doublons) donne des
valeurs du même ordre (top-1 famille 66,4 %, sœur 25,9 %) : la déduplication ne change pas la conclusion,
elle enlève des évidences.

### 2.2 Les trois jeux de langues

| jeu | définition | langues | paires 30 articles |
|---|---|---:|---:|
| **LANG_TREE** | les 29 de `language_genealogy.py`, mappées sur l'UDHR | **25** uniques | **600** |
| **échantillon 20** | les 20 strates du corpus commun (5 familles × 4, sans `fra`) | **20** | **380** |
| **J3.1** | les 21 du corpus commun (20 strates + `fra`) | **21** | **420** |
| **union** | LANG_TREE ∪ échantillon 20 | **39** | **1 482** |

Le mapping LANG_TREE → UDHR est explicite (table dans le JSON) :

- **26 codes mappés** sur 25 textes : `per` et `fas` pointent tous deux vers `pes_1` (même texte) ;
- **3 absents** de l'UDHR : `grc` (grec ancien), `pli` (pali), `lzh` (chinois littéraire) ;
- choix assumés : `nor → nob` (bokmål), `zho → cmn_hant` (mandarin traditionnel),
  `por → por_PT`, `ron → ron_2006`, `deu → deu_1996`.

Les 25 langues LANG_TREE couvrent **7 familles** : indo-européen (17), afro-asiatique (2),
ouralien (2), sino-tibétain (1), japonique (1), coréen (1), turcique (1). L'union avec l'échantillon 20
ajoute l'**atlantique-congo** (4) et l'**austronésien** (4), et complète l'afro-asiatique (4) et le
sino-tibétain (4) : **9 familles, 39 langues**.

## 3. Le protocole — deux mesures, un même retrieval

### 3.1 Le global 532 — le voisinage généalogique

Chaque texte de l'article 1 est une **requête** ; on classe les **444 autres** textes par similarité de
surface, et on regarde si le **top-1** est :

- de la **même famille** Glottolog ;
- de la **même branche** (sœur) : même famille **et** LCA de profondeur ≥ 3, en excluant les couples
  **ancêtre/descendant** (un chemin est préfixe de l'autre : `lat`/`fra`, `san`/`hin`, `san`/`ben`) ;
- de la **même famille, autre branche** : même famille, LCA < 3 (ou ancêtre/descendant) ;
- de **famille différente**.

Ce n'est **pas** un retrieval parallèle : il n'y a pas de « bon article » à retrouver, seulement un
**voisin** dont on lit la parenté. C'est la mesure de la **proximité généalogique de la surface**. Elle
est complémentaire du parallèle, qui, lui, teste le contenu.

On rapporte aussi le **top-5 famille**, le **MRR famille** (rang du premier même-famille) et l'**AP
famille** (précision moyenne sur tous les mêmes-famille). Les hasards sont les parts de chaque catégorie
dans le pool de candidats, **par requête** : 10,3 % pour la famille, 2,5 % pour la sœur, 61,5 % pour
l'écriture.

### 3.2 Le parallèle 30 articles — la mesure de J3.1, sur des jeux choisis

Pour chaque paire ordonnée (A, B), on demande : *l'article `i` de A se retrouve-t-il parmi les 30
articles de B ?* C'est exactement J3.1. Le hasard est **1/30 = 3,33 %**. On agrège par écriture, famille,
sœur, famille-autre-branche, et on estime :

- `top1 ~ script_match + famille_match + chance` — le modèle **J3.1-compatible** (avec `chance`
  constant, comme J3.1, pour la reproduction exacte) ;
- `top1 ~ script_match + soeur + famille_autre_branche` — la **décomposition** qui sépare la sœur de la
  famille lointaine (le hasard est absorbé par la constante, puisqu'il vaut 1/30 pour toutes les paires) ;
- la variante **stricte** (`soeur_stricte` : LCA ≥ 4).

Les IC sont des **bootstrap sur les paires** (1 000) ; les p-values des coefficients sont des
**permutations des étiquettes de famille/chemin** (500) ; le **leave-one-language-out** retire chaque
langue et refait le modèle de décomposition.

### 3.3 Le contrôle d'époque

L'UDHR est **mono-époque** : toutes les entrées portent **1948** (date de l'œuvre ; la date de chaque
traduction n'est pas documentée). Le contrôle d'époque est donc **par construction**, pas une
estimation : on ne peut pas estimer un effet de date dans un corpus où la date ne varie pas.

Deux contrôles le disent :

1. **Placebo de dates** : on assigne à chaque langue une fausse année uniforme 1900–2000, on refait
   `top1 ~ |Δ année|/siècle + script + famille` 200 fois. Le coefficient de la fausse date doit être
   **nul** : c'est un test que le pipeline ne fabrique pas de signal de date.
2. **Le seul bras daté de J3.1** (Bible, 1744–2019) : date **−0,0338/siècle** [−0,0749 ; +0,0094],
   p = 0,1896 ; écriture **+0,6086**. C'est le seul endroit où l'époque varie, et elle ne pèse pas.

### 3.4 Les contrôles négatifs

| contrôle | ce qu'il doit faire | où |
|---|---|---|
| **familles différentes vs sœurs** | les sœurs doivent dominer les familles différentes ; l'écart doit disparaître sous permutation | § 4.2–4.3 |
| **étiquettes de famille/chemin permutées** | top-1 famille/sœur au hasard | § 4.1, § 4.2 |
| **requêtes permutées** | remplacer le texte de la requête par celui d'une autre langue ramène le top-1 famille au hasard | § 4.1 |
| **candidats mélangés** | une permutation sans point fixe des 30 articles de B ramène le top-1 à 1/30 | § 4.2 |
| **placebo de dates** | le coefficient de date fausse est nul | § 4.5 |
| **reproduction J3.1** | mêmes 21 langues, mêmes 30 articles, mêmes chiffres | § 4.4 |

## 4. Les résultats

### 4.1 Global 532 — l'écriture d'abord, la famille ensuite, la sœur au bout

**445 textes, 445 requêtes, 444 candidats.** Top-1 famille **0,6607** (hasard 0,1030) ; top-1 sœur
**0,2607** (hasard 0,0254) ; top-1 famille-autre-branche **0,4000** ; top-1 famille différente
**0,3393**. Le top-1 est de la même écriture dans **93,5 %** des cas (hasard 61,5 %).

| pool | n | top1 famille | hasard | top1 sœur | hasard | top1 famille-autre | top1 famille diff. | top1 script |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **toutes** | 445 | **0,6607** | 0,1030 | **0,2607** | 0,0254 | 0,4000 | 0,3393 | 0,9348 |
| **même écriture** | 417 | **0,6978** | 0,1618 | **0,2782** | 0,0574 | 0,4197 | 0,3022 | 1,0 |
| **écriture différente** | 445 | 0,0989 | 0,0810 | 0,0067 | 0,0076 | 0,0921 | 0,9011 | 0,0 |

La lecture est nette : **dans la même écriture**, la famille est enrichie **4,3×** (0,698 / 0,162) et la
sœur **4,8×** (0,278 / 0,057) ; **hors écriture**, la famille est à **1,2×** (0,099 / 0,081) et la sœur
à **0,9×** (0,0067 / 0,0076) — le hasard. C'est le même mur d'écriture que J3.1 et J3.2, mais mesuré
cette fois sur **445 langues** et non 21 : **le retrieval de surface ne traverse pas l'écriture.**

Le MRR famille vaut **0,7086** (le premier même-famille est en moyenne au rang 1,4) et l'AP famille
**0,3820** : la famille est présente tôt dans le classement, mais pas seulement au top-1.

**Par famille** (familles ≥ 3 requêtes, les plus représentées) :

| famille | n | top1 famille | hasard | top1 sœur | hasard |
|---|---:|---:|---:|---:|---:|
| Indo-European | 105 | **0,800** | 0,233 | **0,295** | 0,045 |
| Atlantic-Congo | 81 | **0,802** | 0,179 | **0,444** | 0,071 |
| Austronesian | 38 | **0,868** | 0,083 | **0,289** | 0,010 |
| Sino-Tibetan | 22 | **0,727** | 0,047 | **0,227** | 0,004 |
| Afro-Asiatic | 19 | **0,526** | 0,040 | 0,105 | 0,008 |
| Turkic | 19 | **0,895** | 0,040 | **0,316** | 0,008 |
| Quechuan | 14 | **1,000** | 0,029 | 0,143 | 0,004 |
| Uralic | 12 | **0,750** | 0,025 | **0,250** | 0,003 |
| Mayan | 9 | **1,000** | 0,018 | **0,444** | 0,003 |

Toutes les familles sont enrichies ; l'**afro-asiatique** l'est moins (0,526 contre 0,040) parce qu'il
mêle des écritures (arabe, hébreu, éthiopien, latin) : la porte de l'écriture le coupe. C'est un
contrôle interne, pas une exception.

**Contrôles.** Les étiquettes de famille/chemin permutées (1 000) donnent **0,1023** de top-1 famille
(IC 95 % [0,0719 ; 0,1348]) et **0,0251** de sœur (IC [0,0090 ; 0,0449]) ; l'observé est **0,6607** et
**0,2607**, p = **0,001** dans les deux cas. Les **requêtes permutées** (200) donnent **0,1110** de
top-1 famille (IC [0,0854 ; 0,1349]) contre une baseline de **0,1030** : le texte de la requête porte
bien l'information, pas seulement la composition du pool.

**Les paires les plus proches** confirment la lecture : `ckb`/`kmr` et `kng`/`ktu` étaient des doublons
exacts (retirés) ; restent `cnr`/`hrv` 0,917, `bos_cyrl`/`srp_cyrl` 0,909, `pes_1`/`pes_2` 0,887,
`041`/`lav` 0,860, `046`/`ind` 0,840 (sœurs), `cjy`/`hsn` 0,791 (même famille, autre branche),
`glg`/`spa` 0,763 (sœurs), `dan`/`nob` 0,737 (sœurs). Les **20 paires les plus proches sont toutes
de la même famille** : dans le global, la proximité maximale est d'abord une proximité de famille et
d'écriture. Les paires de **familles différentes** ne remontent qu'avec l'écriture partagée (voir
§ 4.2 : `arb`/`pes_1` 0,567, `jpn`/`cmn_hant` 0,500).

### 4.2 LANG_TREE 25 — les sœurs dominent, et le coefficient de famille était dilué

**25 langues, 600 paires ordonnées, 30 articles.** Top-1 moyen **0,1471** ; même écriture **0,3480** ;
écriture différente **0,0357** (proche du hasard 0,0333). Le 2×2 :

| | même écriture | écriture différente |
|---|---:|---:|
| **sœurs** | **0,7360** (50) | 0,0333 (10) |
| **même famille, autre branche** | **0,3760** (86) | 0,0333 (130) |
| **familles différentes** | **0,0684** (78) | 0,0370 (246) |

La ligne des sœurs est le résultat : **0,619** toutes écritures, **0,736** à écriture contrôlée, contre
**0,0445** pour les familles différentes (toutes) et **0,0684** à écriture contrôlée. Le gradient est
net **à écriture contrôlée** : sœur 0,736 > famille-autre 0,376 > différente 0,068. **Hors écriture,
les trois cellules sont au hasard** (0,0333 / 0,0333 / 0,0370) : le retrieval de surface ne traverse
aucune frontière d'écriture, exactement comme les 154/154 paires de J3.2. Le contrôle par écriture est
donc une **frontière dure** dans ce corpus, pas une simple covariable.

| groupe | n | top1 | MRR |
|---|---:|---:|---:|
| toutes | 600 | 0,1471 | — |
| même écriture | 214 | 0,3480 | — |
| écriture différente | 386 | 0,0357 | — |
| **sœurs** | **60** | **0,6189** | **0,6899** |
| **sœurs strictes** (LCA ≥ 4) | **54** | **0,6840** | **0,7517** |
| **même famille, autre branche** | **216** | **0,1698** | **0,2707** |
| **familles différentes** | **324** | **0,0445** | **0,1474** |
| même écriture + sœurs | 50 | 0,7360 | 0,8012 |
| même écriture + famille autre | 86 | 0,3760 | 0,4786 |
| même écriture + familles différentes | 78 | 0,0684 | 0,1815 |
| écriture différente + sœurs | 10 | 0,0333 | 0,1332 |

**Les régressions.**

| modèle | variable | coefficient | IC 95 % | p (permutation) | R² |
|---|---|---:|---|---:|---:|
| **J3.1-compatible** | écriture | **+0,2701** | [0,2359 ; 0,3077] | — | **0,4737** |
| | famille | **+0,1548** | [0,1271 ; 0,1818] | 0,004 | |
| | hasard | −0,00068 | [−0,00105 ; −0,00029] | — | |
| **décomposition** | écriture | **+0,2133** | — | — | **0,6306** |
| | **sœur** | **+0,4479** | — | **0,002** | |
| | famille autre branche | **+0,0916** | — | **0,026** | |
| **décomposition stricte** | écriture | **+0,1931** | — | — | **0,6630** |
| | **sœur stricte** | **+0,5065** | — | — | |
| | famille autre branche | **+0,0942** | — | — | |

Le point décisif : le coefficient de **famille** du modèle J3.1-compatible (+0,155) est **2,9× plus
petit** que le coefficient de **sœur** (+0,448). Le premier est une **moyenne** entre sœurs et
familles-autres-branches ; le second isole l'effet de proximité. Le R² passe de **0,474** à **0,631**
quand on sépare les deux. **La famille n'est pas une variable, c'est un mélange.**

**Le contraste demandé — sœurs vs familles différentes.**

| contraste | n sœurs | n diff. | Δ top-1 | IC 95 % | ratio |
|---|---:|---:|---:|---|---:|
| **toutes** | 60 | 324 | **+0,5743** | [0,4899 ; 0,6552] | **13,89×** |
| **même écriture** | 50 | 78 | **+0,6676** | [0,5962 ; 0,7384] | **10,76×** |

Le contraste apparié par langue (même script, au moins une sœur et une famille différente) donne
**11 langues, 11 positives**, Δ moyen **+0,6912**, p du signe **0,00098**, p de Wilcoxon **0,00098** :
le sens est le même pour **toutes** les langues concernées (`dan`, `deu`, `eng`, `fra`, `ita`, `nld`,
`nob`, `por`, `ron`, `spa`, `swe`). Ce n'est pas un effet de quelques paires.

**Robustesse.** Le leave-one-language-out du coefficient de sœur va de **+0,404** à **+0,518**
(médiane **+0,452**) ; l'écriture de **+0,183** à **+0,252** ; la famille-autre de **+0,064** à
**+0,109**. La direction et l'ordre ne dépendent d'aucune langue. Les **candidats mélangés** donnent
**0,0303** de top-1 (hasard 0,0333) : le retrieval est bien dans les articles, pas dans le hasard.

**Exemples.** Sœurs à **1,0** : `dan`/`nob`, `fra`/`spa`, `fra`/`por`, `spa`/`por` ; à **0,967** :
`fra`/`ron`, `swe`/`dan` ; à **0,933** : `ita`/`fra`. Familles différentes les plus proches :
`arb`/`pes_1` 0,567 et `jpn`/`cmn_hant` 0,500 — même écriture, familles différentes. Le retrieval
capte donc **aussi** la proximité d'écriture et d'emprunt, pas seulement la généalogie ; c'est
pourquoi le contrôle de script et la décomposition sont nécessaires.

### 4.3 L'échantillon 20 — le contraste s'éteint, et c'est le résultat

**20 langues, 380 paires.** Top-1 **0,0441** ; même écriture **0,0779** ; écriture différente
**0,0333** (exactement le hasard). Le 2×2 :

| | même écriture | écriture différente |
|---|---:|---:|
| **sœurs** | **0,1083** (4) | 0,0333 (8) |
| **même famille, autre branche** | **0,2367** (10) | 0,0333 (38) |
| **familles différentes** | **0,0560** (78) | 0,0333 (242) |

Les **12 paires de sœurs** sont dominées par les paires **hors écriture** (`arb`/`heb`, `arb`/`amh`,
`heb`/`amh`, `ind`/`mly_arab`) : **8 sur 12** sont hors écriture et au plancher 0,0333. Les sœurs de
même écriture sont `cnh`/`ctd` (0,233 et 0,167) et `ibo`/`kin` (0,033 et 0,0) : quatre paires, dont
**deux au plancher** ; au total **10 des 12 paires** sont à ≤ 0,0333, trop peu pour porter une moyenne. Le **même famille-autre-branche** toutes écritures (0,0757) est
**supérieur** aux sœurs (0,0583) : le signal de l'échantillon est porté par `jav`/`ind` (0,900 et
0,833), deux langues austronésiennes de branches différentes, pas par des sœurs. **Hors écriture, les
trois cellules sont au plancher 0,0333** : comme dans le global et J3.2, le retrieval ne traverse pas
l'écriture.

**Les régressions.**

| modèle | variable | coefficient | p (permutation) | R² |
|---|---|---:|---:|---:|
| J3.1-compatible | écriture | +0,0448 | — | 0,1185 |
| | famille | +0,0338 | — | |
| décomposition | écriture | +0,0452 | — | **0,1215** |
| | **sœur** | **+0,0154** | **0,078** | |
| | famille autre branche | **+0,0384** | **0,016** | |

Le coefficient de sœur **n'est pas significatif** (p = 0,078) ; celui de famille-autre l'est
(p = 0,016). Le contraste sœurs vs différentes donne Δ **+0,0195** [−0,0106 ; +0,0615], ratio
**1,50×** ; à écriture contrôlée, Δ **+0,0524** [−0,0427 ; +0,1462], ratio **1,94×** ; le contraste
apparié ne porte que sur **4 langues** (2 positives, p = 1,0). **L'échantillon 20 ne peut pas résoudre
les sœurs.** Ce n'est pas un échec du retrieval : c'est un **défaut de puissance** de l'échantillon,
qui contient 12 paires de sœurs dont 8 hors écriture, et dont les paires de même famille les plus
proches sont des **non-sœurs**.

C'est exactement le résultat de J3.2 : sur les 21 langues, le signal de famille vit dans **2-3 paires**
(`ind–jav`, `eng–fra`). J7.1 le chiffre et le déplace : **le coefficient de famille de J3.1 était un
mélange de sœurs et de familles-autres-branches, sur un échantillon qui ne contenait presque pas de
sœurs.**

### 4.4 La reproduction de J3.1 — écart nul

Les 21 langues de J3.1, les mêmes 30 articles, le même TF-IDF, les mêmes fonctions : **tous les
chiffres sont identiques**, écart maximal **0**.

| grandeur | J3.1 | J7.1 | écart |
|---|---:|---:|---:|
| paires | 420 | 420 | 0 |
| top-1 moyen | 0,04944 | 0,04944 | 0 |
| même écriture | 0,09375 | 0,09375 | 0 |
| écriture différente | 0,03333 | 0,03333 | 0 |
| même famille | 0,09412 | 0,09412 | 0 |
| famille différente | 0,04081 | 0,04081 | 0 |
| même écriture + même famille | 0,29167 | 0,29167 | 0 |
| même écriture + famille différente | 0,06076 | 0,06076 | 0 |
| coefficient écriture | +0,06186 | +0,06186 | 0 |
| coefficient famille | +0,05562 | +0,05562 | 0 |
| R² | 0,13957 | 0,13957 | 0 |

C'est le contrôle de mise en œuvre : J7.1 ne mesure pas autre chose que J3.1 sur le même corpus.

### 4.5 La comparaison J3.1 / J7.1

| mesure | J3.1 (21) | échantillon 20 | LANG_TREE 25 | union 39 |
|---|---:|---:|---:|---:|
| langues / paires | 21 / 420 | 20 / 380 | 25 / 600 | 39 / 1 482 |
| top-1 moyen | 0,0494 | 0,0441 | **0,1471** | **0,0878** |
| même écriture | 0,0938 | 0,0779 | **0,3480** | **0,1758** |
| écriture différente | 0,0333 | 0,0333 | 0,0357 | 0,0343 |
| même famille | 0,0941 | 0,0722 | **0,2674** | **0,2209** |
| famille différente | 0,0408 | 0,0389 | 0,0445 | 0,0457 |
| **sœurs** | 0,0583 (12) | 0,0583 (12) | **0,6189 (60)** | **0,5405 (70)** |
| famille autre branche | 0,1018 (56) | 0,0757 (48) | 0,1698 (216) | 0,1427 (286) |
| coefficient écriture | +0,0619 | +0,0448 | **+0,2701** | **+0,1341** |
| coefficient famille | +0,0556 | +0,0338 | **+0,1548** | **+0,1675** |
| **coefficient sœur** | +0,0137 | +0,0154 | **+0,4479** | **+0,4502** |
| coefficient famille autre | +0,0646 | +0,0384 | +0,0916 | +0,1001 |
| R² | 0,1396 | 0,1185 | **0,4737** | **0,3484** |

Trois lectures :

1. **J3.1 et l'échantillon 20 sont cohérents** : top-1 ~0,044–0,049, famille ~+0,034–0,056, sœurs
   ~0,058 sur 12 paires, coefficient de sœur non significatif. J3.1 n'est pas un outlier ; c'est le
   même régime.
2. **LANG_TREE 25 change de régime** : top-1 0,147, même écriture 0,348, sœurs 0,619 sur 60 paires,
   coefficient de sœur +0,448. Le facteur **8** entre le coefficient de sœur LANG_TREE (+0,448) et le
   coefficient de famille J3.1 (+0,056) n'est pas un effet de corpus : c'est un effet de **design**.
   Le jeu LANG_TREE contient 60 paires de sœurs, dont 50 de même écriture ; l'échantillon 20 en contient
   12, dont 4 de même écriture.
3. **L'union 39** est le compromis : sœurs 0,540, coefficient +0,450, mais un top-1 plus bas (0,088)
   parce que l'échantillon 20 apporte beaucoup de paires hors écriture. C'est le jeu le plus proche de
   la réalité multilingue : le signal de sœur est fort **quand la paire est dans la même écriture**, et
   nul sinon.

### 4.6 Le contrôle d'époque

| contrôle | valeur | lecture |
|---|---:|---|
| époques distinctes (UDHR) | **1948** | mono-époque par construction |
| placebo de dates (200) | **−0,0013** [−0,0654 ; +0,0412], 51,5 % positif | le pipeline ne fabrique pas de date |
| Bible J3.1 — date | **−0,0338/siècle** [−0,0749 ; +0,0094], p = 0,1896 | le seul bras daté : la date ne pèse pas |
| Bible J3.1 — écriture | **+0,6086** | l'écriture domine |

L'époque ne peut donc pas expliquer l'effet de famille : elle est **constante** dans l'UDHR, le placebo
est nul, et dans le seul corpus où elle varie (la Bible), elle n'est pas significative. La hiérarchie
mesurée est **porte d'écriture → sœur > famille-autre-branche > époque** : l'écriture est un **seuil**
(la franchir change tout), et **dans le même script, sur LANG_TREE**, la sœur est le premier effet (coefficient
+0,448 contre +0,213 pour l'écriture). C'est le renversement de J3.1 : le coefficient de famille
(+0,056) était plus petit que celui d'écriture (+0,062) parce qu'il mélangeait sœurs et familles
lointaines ; séparé, l'effet de sœur **dépasse** celui de l'écriture.

## 5. Ce que cela dit de J3.1, de J3.2 et de l'avertissement de Panini

**J3.1 avait raison, mais son coefficient de famille était un résumé.** Sur 21 langues, le coefficient
de famille (+0,0556) mélange 12 paires de sœurs et 56 paires de même-famille-autre-branche ; les
premières sont à 0,058, les secondes à 0,102. Le coefficient est donc **tiré par les non-sœurs** et
sous-estime l'effet de proximité. En séparant les deux, sur un jeu qui contient assez de sœurs, le
coefficient de sœur est **+0,448** (8×) et le coefficient de famille-autre **+0,092**. La conclusion de
J3.1 — « l'écriture domine, la famille compte ensuite, l'époque ne pèse pas » — **tient** ; elle est
seulement **plus fine** : la famille qui compte est la **branche proche**, pas la macro-famille.

**J3.2 avait raison sur son échantillon, et J7.1 en montre la limite.** J3.2 disait : « le signal de
famille vit dans 2-3 paires ». C'est vrai pour les 21 langues (`ind–jav`, `eng–fra`) et pour
l'échantillon 20 (`jav–ind` 0,900). Ce n'est **pas** vrai pour les 25 langues LANG_TREE : 11 langues
sur 11 ont un avantage de sœur positif, et le leave-one-language-out ne renverse jamais le coefficient.
Le signal n'était pas absent ; il était **hors de l'échantillon**.

**L'avertissement de Panini n'est pas contredit.** Leur signature de 14 atomes, sur des textes
philosophiques, capte l'époque (β +0,138) plus que la filiation (β +0,049). Notre instrument est
différent (n-grammes de caractères) et notre corpus aussi (UDHR, article 1). Ce que J7.1 établit, c'est
que **la surface retrouve la filiation quand la branche est proche et l'écriture partagée** ; elle ne
la retrouve pas à travers l'écriture, et elle ne la retrouve pas sur un échantillon sans sœurs. Le
remède de Panini — **contrôler la surface dans tout test de famille** — est donc plus que jamais
nécessaire : ici, sans le contrôle d'écriture, la famille paraît 6,4× au-dessus du hasard ; avec le
contrôle, elle est 4,3× dans la même écriture et **1,2× hors écriture**. Une part importante du
« signal de famille » brut est un signal d'écriture.

## 6. Ce qui pourrait rendre ce résultat faux

1. **Retrieval de surface, pas de sens.** Les n-grammes capturent l'orthographe, les cognates, les
   emprunts et les noms propres, pas la syntaxe ni le sens. Une réplication neuronale (états cachés)
   peut donner une autre hiérarchie. **C'est la limite principale.**
2. **Le global ne porte que l'article 1.** Panini ne publie que cet article ; les 30 articles ne sont
   disponibles que pour les 25 + 20 langues de Drave. Le global mesure donc la **proximité de
   l'article 1**, pas la proximité de 30 articles. Le parallèle corrige, mais sur un sous-ensemble.
3. **L'UDHR est mono-époque.** Le contrôle d'époque est par construction, pas une estimation ; le
   placebo ne prouve pas l'absence d'un effet d'époque, il vérifie que le pipeline ne fabrique pas de
   date. Le seul bras daté (Bible) est un autre corpus, un autre genre.
4. **Les variantes proches et les doublons.** 12 groupes de textes identiques, 2 doublons cross-ISO
   retirés ; il reste des variantes très proches (`cnr`/`hrv` 0,917, `bos_cyrl`/`srp_cyrl` 0,909,
   `pes_1`/`pes_2` 0,887) qui gonflent le **signal de famille-autre-branche**, pas le signal de
   sœur. Le signal de sœur reste massif après retrait des doublons exacts, mais il inclut une part de
   **même tradition de traduction** pour les paires très proches.
5. **La définition de « sœur » est une convention.** LCA ≥ 3, hors ancêtre/descendant. La variante
   stricte (LCA ≥ 4) donne des chiffres **plus forts** (0,684, coefficient +0,507) : la conclusion ne
   dépend pas du seuil, mais les valeurs, oui. Un seuil plus large (LCA ≥ 2) inclurait `ind`/`jav` et
   `eng`/`fra` comme sœurs, et changerait le tableau.
6. **Les paires ne sont pas indépendantes.** Une langue apparaît dans plusieurs paires ; les IC sont
   des intervalles **inter-paires**, pas des IC de langue. Le leave-one-language-out donne la
   sensibilité ; il ne corrige pas la dépendance.
7. **L'échantillon 20 n'est pas aléatoire.** Il est stratifié (5 familles × 4) et choisi pour la
   diversité des écritures ; il sur-représente les petites familles et sous-représente
   l'indo-européen. Le contraste sœurs y est **sous-puissant** par construction.
8. **Le mapping LANG_TREE → UDHR est manuel.** 26 codes → 25 textes ; `nor → nob`, `zho → cmn_hant`,
   `per`/`fas` → `pes_1`, `por → por_PT`, `ron → ron_2006`, `deu → deu_1996`. Ces choix sont
   explicites et pourraient être variés (par exemple `nor → nno`, `zho → cmn_hans`) ; les conclusions
   de sœur ne portent pas sur ces choix, mais les valeurs, si.
9. **11 textes non étiquetés.** Ce sont des variantes numériques de l'UDHR ; ils sortent des mesures
   de famille. Le taux de couverture Glottolog est **521/532 = 97,9 %**.
10. **L'écriture n'est pas le seul confondant.** La tradition de traduction, l'arealité, les emprunts
    et les cognates latins (pour l'indo-européen) pèsent aussi. Le contrôle par écriture réduit le
    confondant, il ne l'élimine pas.

## 7. Fichiers et reproduction

| fichier | rôle |
|---|---|
| [`../tools/retrieval_familles.py`](../tools/retrieval_familles.py) | le dispositif complet (global 532, LANG_TREE, échantillon 20, J3.1, contrôles) |
| [`retrieval-familles.json`](retrieval-familles.json) | tous les chiffres, les 445 lignes du global, les 600 + 380 + 420 + 1 482 paires, les contrôles |
| [`retrieval-epoque.json`](retrieval-epoque.json) | J3.1, pour la reproduction exacte |
| [`../data/udhr/genealogie.json`](../data/udhr/genealogie.json) | Glottolog : familles et chemins de 441 fichiers Drave |
| [`../data/udhr/articles_propres.jsonl`](../data/udhr/articles_propres.jsonl) | les 30 articles Drave |
| `../Panini/research/data/udhr_corpus.json` | les 532 textes Panini (lecture seule) |
| `../Panini/research/src/nipada/signing/language_genealogy.py` | les 29 langues LANG_TREE (lecture seule) |

Reproduction :

```bash
python3 tools/retrieval_familles.py
python3 tools/retrieval_familles.py --rapide    # permutations réduites, pour vérifier
```

L'outil lit Panini **en lecture seule** (SHA-256 dans le JSON), calcule les métriques et écrit
`reports/retrieval-familles.json`. Les contrôles négatifs sont dans `controles_negatifs` et dans les
champs `controle_permutation` de chaque paire.

## 8. Verdict et suite

- **J7.1 est mesuré, écrit, contrôlé.** Le retrieval de surface a une **porte d'écriture** (hors
  écriture, tout est au hasard) ; **dans la même écriture, sur LANG_TREE et l'union**, l'ordre est
  **sœur > famille-autre > époque**. La famille est réelle, mais **conditionnelle à l'écriture** et **visible seulement si le
  design contient des sœurs**.
- **J3.1 est reproduit à l'identique** ; son coefficient de famille (+0,056) est un **minorant** de
  l'effet de sœur (+0,448 sur LANG_TREE). **J3.2 est confirmé pour son échantillon** (2-3 paires) et
  **dépassé pour le jeu LANG_TREE** (11/11 langues).
- **La prochaine mesure** : la **réplication neuronale** sur les 30 articles (états cachés, comme
  `retrieval_udhr.py`), pour voir si le **sens** suit la même hiérarchie que la surface. C'est le seul
  moyen de dire si la sœur est une propriété de la surface ou du contenu.
- **La ligne de roadmap** : R0.7 (le bloc langue) / L. Le corpus commun et la table LANG_TREE → UDHR
  sont réutilisables pour la suite (V14 multilingue, rétro-traduction).
