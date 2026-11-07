# J3.1 — Le retrieval inter-langues à époque contrôlée

> **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J3.1 · **Date** : 2026-11-07
> **Verdict** : ✅ **la mesure est faite ; elle borne l'avertissement** —
> dans ce retrieval de **surface**, **l'écriture domine** (+0,609 ; IC 95 % [0,529 ; 0,702]), la **famille**
> compte ensuite (+0,181 [0,106 ; 0,253]), et **l'écart d'années ne pèse pas en moyenne** (−0,034 par siècle
> [−0,075 ; +0,009], p = 0,19 par permutation). À écriture contrôlée, les couples **contemporains** et
> **décalés** sont au **même niveau** : **0,710 vs 0,710**. Le renversement brut (0,238 vs 0,427) est un
> **effet de composition** : les couples décalés contiennent **60 %** de paires de même écriture, les
> contemporains **33 %**. **L'époque ne domine pas ici ; le confondant de composition, lui, n'est pas nul : sans
> contrôle, il fausse la comparaison.**
> **Dispositif** : trois corpus, un même retrieval de surface (n-grammes de caractères, TF-IDF, cosinus,
> top-1) ; **B7** (71 langues, 35 concepts, libellés Wikidata 2026), **UDHR** (21 langues du corpus commun,
> 30 articles, 1948), **BIBLE** (12 traductions datées de 1744 à 2019, 1 000 versets narratifs alignés).
> **Contrôles négatifs** : cibles mélangées (permutation sans point fixe) pour les trois bras ; années
> permutées pour la régression biblique. Les contrôles sont **au niveau (ou au voisinage) du hasard**.
> **JSON** : [`retrieval-epoque.json`](retrieval-epoque.json) · **Outil** : [`../tools/retrieval_epoque.py`](../tools/retrieval_epoque.py).
> **Ce qui pourrait le rendre faux** : le retrieval est **de surface**, pas neuronal ; les traductions
> bibliques diffèrent par le style autant que par la date ; écriture et famille sont corrélées ; le
> portugais 2018 est un outlier ; 1 000 versets, livres narratifs seulement. Voir § 6.

## 1. La question

Panini et Nipada ont trouvé que leur **signature lexicale** capte **l'époque** (β **+0,138**) bien plus que la
**filiation** (β **+0,049**) : *la surface transmet les signifiants, pas la généalogie*
([`panini-nipada.md`](../docs/methode/panini-nipada.md),
[`genealogie-des-langues.md`](../docs/theorie/genealogie-des-langues.md)). Leur remède est de **contrôler la
date** dans tout test de style et la **surface** dans tout test de famille.

J3.1 demande la même chose pour notre **retrieval** : *le même contenu se retrouve-t-il d'une langue à l'autre,
et ce taux dépend-il de l'écart d'époque ou de la surface ?* La difficulté est que les deux corpus demandés
sont à **date unique** :

- **B7** : 71 langues, 35 concepts, libellés **Wikidata 2026** — toutes les entrées sont contemporaines ;
- **UDHR** : 21 langues, 30 articles, texte de **1948** — toutes les entrées sont contemporaines.

Aucun des deux ne peut donc porter un **contraste d'époque**. On les garde pour la **surface** (écriture,
famille), et on construit un troisième corpus, **daté**, pour l'époque : la **Bible**, dont les traductions
vont de **1744** (Ostervald) à **2019** (pidgin nigérian), avec le même contenu verset par verset.

## 2. Le dispositif — trois corpus, un même retrieval

| corpus | langues | unités | dates | ce qu'il porte |
|---|---:|---|---|---|
| **B7** ([lexique](../tools/jeux/lexique_multilingue.json)) | 71 | 35 concepts | 2026 (unique) | la **surface** : écriture, famille |
| **UDHR** ([corpus commun](rapport-corpus-commun.md)) | 21 | 30 articles | 1948 (unique) | la **surface**, à date contrôlée par construction |
| **BIBLE** (eBible.org) | 10 langues / 12 traductions | 1 000 versets | **1744–2019** | l'**époque** : contemporains vs décalés |

### 2.1 B7 — 71 langues, 35 concepts

Le lexique B7 est celui des jeux : noms des cinq jeux, pièces des échecs, rangs et enseignes des cartes,
couleurs, notions de maîtres. Il donne, pour chaque concept, les libellés dans **71 langues**. La mesure
demande : *le libellé du concept `c` en langue A ressemble-t-il plus au libellé de `c` qu'à celui des 34
autres concepts en langue B ?* C'est un retrieval de **concepts**, à date unique (2026). Les 71 langues sont
étiquetées par **écriture dominante** (comptage des points de code) et par **famille** (Glottolog macro,
table manuelle dans l'outil) ; 4 004 paires ordonnées ont au moins 5 concepts communs.

### 2.2 UDHR — 21 langues, 30 articles

Les 21 langues du corpus commun ont toutes leurs **30 articles** dans `data/udhr/articles_propres.jsonl` ;
l'article 1 est celui qui est **identique des deux côtés** (418/438 paires exactes), les 29 autres sont la
version Drave. La mesure demande : *l'article `i` en langue A se retrouve-t-il parmi les 30 articles de la
langue B ?* Le hasard est **1/30 = 3,33 %**. Toutes les entrées portent **1948** : la date est contrôlée par
construction.

### 2.3 BIBLE — 12 traductions datées, 1 000 versets

La Bible est le seul corpus **parallèle et daté** disponible ici : le même verset existe dans toutes les
traductions, et chaque traduction a une date. Les 12 traductions retenues :

| id | traduction | langue | écriture | famille | année | licence | SHA-256 |
|---|---|---|---|---:|---|---|---|
| `OST` | Ostervald | français | Latn | Indo-European | 1744 | domaine public | `4631037b5b9e…` |
| `KJV` | King James (texte standard 1769) | anglais | Latn | Indo-European | 1769 | domaine public | `67561758cf58…` |
| `RUS` | Synodal | russe | Cyrl | Indo-European | 1876 | domaine public | `9af20fe73fff…` |
| `SPA` | Reina-Valera 1909 | espagnol | Latn | Indo-European | 1909 | domaine public | `56937c2be9ad…` |
| `LSG` | Louis Segond 1910 | français | Latn | Indo-European | 1910 | domaine public | `64c4fe2a84d9…` |
| `LUT` | Luther 1912 | allemand | Latn | Indo-European | 1912 | domaine public | `76fb83f108dd…` |
| `CUV` | Chinese Union Version | chinois | Hani | Sino-Tibetan | 1919 | domaine public | `496f17f4daa6…` |
| `WEB` | World English Bible | anglais | Latn | Indo-European | 2000 | domaine public | `37aac697f5d9…` |
| `ARB` | New Arabic Version | arabe | Arab | Afro-Asiatic | 2012 | CC BY-SA 4.0 | `0fcb07ae4ade…` |
| `HIN` | Indian Revised Version | hindi | Deva | Indo-European | 2017 | CC BY-SA 4.0 | `7fe5d5b089c4…` |
| `POR` | Bíblia Livre | portugais | Latn | Indo-European | 2018 | CC BY 4.0 | `7ca6742fc1a3…` |
| `PCM` | Nigerian Pidgin | pidgin nigérian | Latn | Creole anglais | 2019 | © Wycliffe, redistribution | `94f8c52a8a47…` |

Les fichiers USFM sont lus par l'outil, **7 499 versets** communs aux 12 traductions dans les livres
narratifs (GEN, EXO, MAT, MRK, LUK, JHN, ACT), puis **1 000** sont retenus (longueur 20–600 caractères dans
toutes les traductions, versets non répétés, graine 0). Le hasard est **1/1 000 = 0,1 %**.

## 3. La mesure

Un texte est représenté par ses **n-grammes de caractères** (n = 3), après NFKC, casse pliée, diacritiques
retirés et ponctuation remplacée par des espaces. Les n-grammes sont pondérés **TF-IDF** (idf lissé, tf
sous-linéaire), les vecteurs sont normalisés L2, et la similarité est le **cosinus**. Pour chaque requête de
A, on classe les candidats de B ; le **top-1** est la proportion de requêtes dont le bon candidat est rang 1.
Le **MRR** et le **rang médian** sont dans le JSON.

**Ce que ce n'est pas.** C'est un retrieval de **surface** : il ne teste pas le sens profond, il teste si la
signature lexicale/orthographique suffit à retrouver le bon contenu. C'est exactement la grandeur de
l'avertissement de Panini (*signature lexicale*), mais **ce n'est pas un modèle neuronal** ; la réplication
neuronale reste à faire (voir § 6).

**Contrôles négatifs.** (a) Pour chaque paire, la cible correcte est remplacée par une **permutation sans
point fixe** : le top-1 doit retomber au hasard. (b) Pour B7, on apparie A avec une **autre langue** que B :
si le retrieval suit la surface et pas la langue, le score doit rester proche du score global. (c) Pour la
Bible, on **permute les années** des traductions et on refait la régression : si l'époque compte, le
coefficient observé doit sortir de la distribution permutée. Les IC des coefficients sont des **bootstrap**
sur les paires (1 000) ; les contrastes appariés sont testés par **McNemar** ; les agrégats B7/UDHR sont des
intervalles **inter-paires** (2,5–97,5 %).

## 4. Les résultats

### 4.1 B7 — l'écriture d'abord, la famille ensuite

**4 004 paires ordonnées**, 71 langues au lexique, 35 concepts. Le top-1 moyen est **0,138** ; le hasard moyen
est **0,055** (1/k, k variable). **64 langues** ont au moins 5 concepts communs avec une autre et entrent dans
les paires ; les **7** autres (`am`, `km`, `ky`, `lo`, `mt`, `si`, `yo`) n'ont que 1 à 4 concepts et sortent de
la mesure appariée. Les 2×2 :

| | famille même | famille différente |
|---|---:|---:|
| **écriture même** | **0,266** (742 paires) | **0,176** (944 paires) |
| **écriture différente** | **0,086** (840 paires) | **0,079** (1 478 paires) |

La régression `top1 ~ script_match + famille_match + chance` donne :

| variable | coefficient | IC 95 % |
|---|---:|---:|
| écriture même | **+0,132** | [0,126 ; 0,137] |
| famille même | **+0,046** | [0,040 ; 0,051] |
| chance (1/k) | +0,355 | [0,280 ; 0,424] |
| constante | +0,045 | [0,040 ; 0,050] |

**R² = 0,400.** L'écriture pèse **près de trois fois** la famille. Les coefficients ne se comparent pas
d'un bras à l'autre (le hasard B7 est 1/k, celui de la Bible 1/1 000) ; seule la **hiérarchie** se compare.
Les meilleures paires sont des langues
sœurs de même écriture : `nb–nn` 0,875, `bs–hr` 0,857, `cs–sk` 0,826, `mk–sr` 0,800. Les paires de même
écriture mais de familles différentes restent au-dessus du hasard (`fr–tr` 0,259, `en–id` 0,105…), mais loin des sœurs.
**Contrôle négatif** : cibles permutées **0,070** contre un hasard de **0,055** — proche du hasard ; le
léger excès est attendu, des libellés de concepts différents peuvent se ressembler (roi/dame, blanc/noir).
**Contrôle de langue** : apparier A à une **autre** langue donne **0,154**, proche du score global 0,138 :
le retrieval suit la **surface**, pas l'identité de la langue.

### 4.2 UDHR — la même hiérarchie, à date unique

**21 langues, 30 articles, 420 paires**, toutes de **1948**. Top-1 moyen **0,049** ; hasard **0,0333**.

| | famille même | famille différente |
|---|---:|---:|
| **écriture même** | **0,292** (16 paires) | **0,061** (96 paires) |
| **écriture différente** | **0,033** (52 paires) | **0,033** (256 paires) |

Les paires d'**écritures différentes** sont **exactement au hasard** (0,0333) : aucune ne dépasse le hasard.
Les meilleures paires sont `eng–fra` 0,933, `jav–ind` 0,900, `ind–jav` 0,833. La régression
`top1 ~ script_match + famille_match + chance` : écriture **+0,062** [0,034 ; 0,094], famille **+0,056**
[0,014 ; 0,111], R² = 0,140. **Contrôle négatif** : cibles permutées **0,0323** contre 0,0333 de hasard —
au hasard.

### 4.3 BIBLE — le renversement apparent, et ce qu'il cache

**12 traductions, 10 langues, 132 paires, 1 000 versets.** Top-1 moyen **0,293** ; hasard **0,001**.

| groupe | n paires | top-1 moyen |
|---|---:|---:|
| toutes | 132 | 0,293 |
| **écriture même** | 56 | **0,688** |
| **écriture différente** | 76 | **0,0026** |
| **langue même** | 4 | **0,997** |
| langue différente | 128 | 0,271 |
| **contemporain** (≤ 50 ans) | 42 | **0,238** |
| **décalé** (≥ 150 ans) | 30 | **0,427** |
| **écriture même + contemporain** | 14 | **0,710** |
| **écriture même + décalé** | 18 | **0,710** |
| écriture différente + contemporain | 28 | 0,0021 |
| écriture différente + décalé | 12 | 0,0030 |

**Le renversement.** Brut, les couples **décalés** semblent mieux marcher (0,427) que les **contemporains**
(0,238) : c'est l'inverse de l'avertissement. Mais les couples décalés contiennent **60 %** de paires de
même écriture (18/30), contre **33 %** chez les contemporains (14/42). **À écriture contrôlée, les deux
groupes sont identiques : 0,710 vs 0,710.** C'est un **effet de composition** (Simpson) : l'époque n'est pas
la variable qui explique le classement brut, c'est l'écriture.

**Les contrastes appariés.** On fixe la paire de langues et on ne change que la date du pivot :

- **pivot anglais** (KJV 1769 → WEB 2000), cibles de même écriture (OST, SPA, LSG, LUT, POR, PCM) :
  Δ moyen **+0,52 point**, IC 95 % **[−2,9 ; +4,3]**. Les effets par cible ne sont pas monotones :
  **PCM +8,7** (p < 0,001), **POR +2,7** (p = 0,024), mais **SPA −3,6**, **LUT −4,9** (p < 0,001).
- **pivot français** (OST 1744 → LSG 1910), cibles de même écriture (KJV, SPA, LUT, WEB, POR, PCM) :
  Δ moyen **+0,52 point**, IC 95 % **[−1,2 ; +1,9]**. Positifs : **LUT +2,6**, **KJV +2,1**,
  **WEB +1,6** ; négatif : **POR −3,2**.

**Le 2×2 anglais × français.** Quatre cellules, même paire de langues, dates croisées :

| | Ostervald 1744 | Segond 1910 |
|---|---:|---:|
| **KJV 1769** | 0,971 | 0,970 |
| **WEB 2000** | 0,976 | 0,967 |

Interaction **(WEB−LSG) − (WEB−OST) − (KJV−LSG) + (KJV−OST)** = **−0,008** : aucune. À écriture et famille
contrôlées, 231 ans d'écart ne déplacent pas le retrieval.

**La régression des 132 paires.** `top1 ~ |Δ années|/siècle + script_match + famille_match + langue_match` :

| variable | coefficient | IC 95 % |
|---|---:|---:|
| **Δ années par siècle** | **−0,034** | **[−0,075 ; +0,009]** |
| écriture même | **+0,609** | [0,529 ; 0,702] |
| famille même | **+0,181** | [0,106 ; 0,253] |
| langue même | **+0,311** | [0,209 ; 0,402] |
| constante | −0,037 | [−0,091 ; +0,013] |

**R² = 0,763.** Le coefficient de dates n'est **pas significatif** ; le contrôle par **permutation des
années** donne **p = 0,19** (500 permutations). Le coefficient d'écriture (0,609) vaut **18 fois** celui des dates par siècle (0,034) ; la famille
(0,181) vaut **5 fois**. **Contrôle négatif** : versets permutés **0,00070** contre 0,001 de hasard —
au hasard.

**Ce que le retrieval suit.** Les paires de **même langue** sont à **0,997** (KJV–WEB, OST–LSG, etc.) :
231 ans d'écart dans une même langue ne coûtent **rien** à la surface. Les paires d'**écriture différente**
sont **quasi au hasard** (0,0026, 2,6× le hasard de 0,001) : hindi, arabe, chinois et russe ne partagent pas
assez de n-grammes avec les langues latines. Entre les deux, les paires latines de même famille vont de
**0,90 à 1,00**, sauf les paires du portugais 2018 avec les autres langues latines (0,14–0,48 ; l'espagnol
fait exception à 0,948) ; les paires avec le pidgin vont de 0,16 à 0,66. **La date n'ordonne pas ces
valeurs ; l'écriture et la tradition de traduction le font.**

## 5. Ce que cela dit de l'avertissement de Panini

L'avertissement de Panini est **vrai dans son instrument** : leur signature de 14 atomes, sur des textes
philosophiques, capte l'époque (β +0,138) plus que la filiation (β +0,049). **Il ne se transporte pas
mécaniquement à ce retrieval de surface** : ici, l'écriture domine (+0,609), la famille compte (+0,181), et
l'écart d'années n'a **aucun effet détectable en moyenne** à écriture contrôlée (−0,034 par siècle, IC
incluant 0) ; les contrastes par cible montrent des effets **locaux opposés** (PCM +8,7, LUT −4,9), qui ne
s'additionnent pas en un effet d'époque.

Ce n'est pas une réfutation de Panini : c'est une **borne de validité**. Deux instruments différents (leur
signature d'atomes, nos n-grammes de caractères) ne mesurent pas la même chose. Ce que J3.1 établit, c'est
que **le contrôle de date reste obligatoire** : sans lui, le brut **inverse** la conclusion (0,238 vs 0,427)
par simple composition d'écritures. *Contrôler la date ne veut pas dire que la date gagne ; cela veut dire
qu'on ne peut pas lire le brut.*

Pour la généalogie (J3.2), la conséquence est directe : **toute mesure de retrieval doit être stratifiée par
écriture** avant d'être lue comme un effet de famille ou d'époque. C'est le même remède que celui de
[`genealogie-des-langues.md`](../docs/theorie/genealogie-des-langues.md) § 3, appliqué au retrieval.

## 6. Ce qui pourrait rendre ce résultat faux

1. **Retrieval de surface, pas de sens.** Les n-grammes de caractères capturent les cognates, les noms
   propres et l'orthographe, pas la syntaxe ni le sens profond. Un retrieval neuronal pourrait montrer un
   effet d'époque que la surface ne voit pas. **C'est la limite principale.**
2. **Les traductions bibliques diffèrent par le style autant que par la date.** KJV est archaïque et formel,
   WEB est moderne ; OST et LSG sont deux traditions françaises. Le « facteur date » est confondu avec le
   **choix de traduction**. Les contrastes appariés (même paire de langues) réduisent ce confondant, pas
   l'éliminent.
3. **Écriture et famille sont corrélées.** Les paires latines sont surtout indo-européennes ; les paires
   d'écritures différentes sont surtout de familles différentes. Le B7 et l'UDHR permettent de croiser les
   deux (écriture même × famille différente, écriture différente × famille même), mais les cellules ne sont
   pas aléatoires : elles dépendent des 71 langues et des 21 du corpus commun.
4. **Le portugais 2018 est un outlier.** `POR` (Bíblia Livre) est plus libre et tire les couples vers le bas
   (0,14–0,48) ; il pèse dans les moyennes et dans la régression. Sans lui, les conclusions de § 4.3
   tiennent (le coefficient de dates reste petit), mais les valeurs changent.
5. **Échantillon biblique.** 1 000 versets sur 7 499, livres narratifs seulement, longueur 20–600
   caractères, versets non répétés. Les épîtres, les psaumes et les généalogies sont absents.
6. **Dates.** KJV est daté **1769** (texte standard) et non 1611 (traduction) ; les dates des traductions
   modernes sont les dates de publication/édition, pas les dates de chaque révision. L'écart de 231 ans
   KJV–WEB est donc un **majorant** de l'écart réel des textes.
7. **B7 et UDHR sont à date unique.** Ils ne testent **pas** l'époque ; ils testent la surface. Leur
   inclusion est un **contrôle de surface**, pas une preuve d'absence d'époque.
8. **Familles B7 grossières.** La table `FAMILLE_B7` est au niveau **macro** (Glottolog), pas à la feuille ;
   deux langues « même famille » peuvent être très éloignées (hindi et anglais). Le coefficient de famille
   est donc un **minorant** de l'effet de branche.
9. **Les libellés B7 sont des lemmes, souvent empruntés.** `tic-tac-toe`, `chess`, `poker` circulent tels
   quels ; le retrieval B7 mesure la **surface partagée**, pas la filiation. Le coefficient de famille
   (+0,046) est un **minorant** de la structure généalogique, et l'écriture (+0,132) inclut les emprunts.

## 7. Fichiers et reproduction

| fichier | rôle |
|---|---|
| [`../tools/retrieval_epoque.py`](../tools/retrieval_epoque.py) | le dispositif complet (B7, UDHR, Bible, contrôles) |
| [`retrieval-epoque.json`](retrieval-epoque.json) | tous les chiffres, les 4 004 paires B7, les 420 paires UDHR, les 132 paires Bible |
| `work/retrieval-epoque/bibles/*.zip` | les 12 USFM (non versionnés, `work/` est ignoré) ; SHA-256 dans le JSON |
| `data/udhr/articles_propres.jsonl`, `meta.json`, `genealogie.json` | l'UDHR et ses métadonnées |
| [`../tools/jeux/lexique_multilingue.json`](../tools/jeux/lexique_multilingue.json) | le lexique B7 |

Reproduction :

```bash
python3 tools/retrieval_epoque.py --n-versets 1000
```

L'outil télécharge les USFM dans `work/retrieval-epoque/bibles/` s'ils manquent, calcule leur SHA-256
(inscrit dans le JSON) et écrit `reports/retrieval-epoque.json`. Les contrôles négatifs sont dans le JSON (`controles`) et dans les
champs `controle_permutation` de chaque paire.

## 8. Verdict et suite

- **J3.1 est mesuré, écrit, contrôlé.** Le retrieval de surface est **dominé par l'écriture** ; l'époque
  n'ajoute rien **en moyenne** à écriture contrôlée, mais **le brut la fait paraître dominante** par composition.
- **La leçon pour la roadmap R0.7** : les scores de retrieval du corpus commun (21 langues, 1948) sont des
  scores **à date unique** ; ils ne doivent pas être comparés à des scores d'une autre époque sans
  stratification par écriture. La prochaine mesure (J3.2, la généalogie à deux faces) doit **apparier
  écriture et date** avant de lire la famille.
- **La réplication neuronale** (états cachés, comme `retrieval_udhr.py`) reste ouverte : c'est le seul
  moyen de dire si le **sens** se comporte comme la surface. Elle est nommée comme prochaine action, pas
  comme résultat.
