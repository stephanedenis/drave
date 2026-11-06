# B13 — dev/test en v10 : dev 152/152, test 68/68, l'exact est saturé et le split ne bouge plus que par la couverture

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
> **Commit mesuré** : `710ec7f9` (branche `s/v7`) · **Verdict** : ✅ chiffres justes,
> **3 énoncés de la fiche v10 à corriger**, et une **régression nouvelle** (`r303`).
> **dev 152/152 (1,0000)**, **test 68/68 (1,0000)**, tout **220/220** ; couverture
> **0,9325 / 0,8947 / 0,9205** ; F1 **0,5812 / 0,5890 / 0,5836** (vivant 612) ;
> tête **0,7330 / 0,7337 / 0,7332** ; POS **0,7547 / 0,7656 / 0,7581**. **19 spans**
> restants (9 REL, 6 SUB, 4 GP). Sur les trois découpages `%3==0/1/2`, l'exact/labels
> reste **1,0 partout** ; l'étendue est de **0** sur le taux exact, **3,25 pts (dev) /
> 6,03 pts (test)** sur la couverture, **1,07 / 2,09** sur la F1, **0,69 / 1,31** sur la
> tête, **0,55 / 1,11** sur la POS — toutes dans la bande Monte-Carlo (p 0,30–0,86).
> L'écart dev/test n'est plus un écart d'exactitude (**0**) ; la couverture **+3,78 pts**
> au canonique **s'inverse** aux décalés (**−5,51 / +2,19**) et n'est pas significative
> (z=1,005 ; p=0,315).
>
> **Dispositif** : [`gold_split.py`](../tools/tests/linguistique/gold_split.py) (`dev`, `test`,
> `compter`), [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`,
> `evaluer_bloc`), [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (heuristique) ; JSON
> [`pensee-dev-test-v10.json`](pensee-dev-test-v10.json).
>
> **Ancrage d'arbre.** La mesure est faite sur le **module épinglé de `710ec7f9`** (copie
> `/tmp`, `RACINE` du dépôt), pas sur l'arbre courant : depuis, `HEAD` a avancé à `653a7981`
> (`68a8717b` puis `653a7981`), qui **committe** l'essai R2 + retrait de la garde d'adverbe
> final. Cet état donne, mesuré, **dev 152/152, test 69/69, tout 221/221, couverture 0,9247,
> F1 0,5843, tête 0,7330, POS 0,7581, 18 spans** (9 REL, 5 SUB, 4 GP : `g017`, `r035`,
> `r241`, `r255`, `r264`, `s010`, `s027`, `s035`, `s044`, `s061`, `s065`, `s112`, `s114`,
> `s125`, `s141`, `s146`, `s148`, `s160` ; `s037`, `r303`, `r288` récupérés). Ce n'est **pas**
> l'état mesuré ici, et ce n'est pas l'objet de cette fiche. Voir § 8 pour le ballant
> `g017`/`r288`/`r303`. La fiche v10 a par ailleurs été corrigée dans `653a7981` (message
> « audit v10 intégré, v10 corrigée ») ; les trois énoncés de § 6.1 restent l'audit de
> l'état `710ec7f9`.

## 1. Ce qui est mesuré

- **Corpus** : `charger()` = **612 phrases** (20 `hand`, 432 `reel`, 160 `synthetique`),
  **402 fr / 210 en**, **3 179 tokens** ; **239 cibles** (REL 74, SUB 69, GP 96) ;
  **220 labels au bon span**, **19 spans perdus**.
- **Split** : `crc32(str(id)) % 3`. Canonique : test = seau 0 (190 phrases), dev = seaux 1+2
  (422) ; décalé 1 : test = seau 1 (229), dev = 383 ; décalé 2 : test = seau 2 (193), dev = 419.
  Aucune phrase dupliquée ; l'union redonne 612 ; les cibles se somment à 239.
- **Mesure** : `evaluer_bloc("heuristique", Heuristique(), sous-ensemble)`. `exact` = cible
  correcte **parmi les labels au bon span** ; `couverture` = labels / cibles ; F1 et tête sur
  les segments ; POS au token. Les F1/tête dev/test sont sur le **vivant 612**, comme la fiche
  v7 et l'audit ; le **gelé 602** est donné à part.
- **Validation** : une agrégation indépendante (par phrase, puis par sous-ensemble) redonne
  `evaluer_bloc` **au chiffre près** : écart maximal **0,0** sur 612, dev et test (`validation`
  du JSON). Deux exécutions donnent le même digest de prédictions (`determinisme: true`).
- **Vivant 612 vs gelé 602.** L'exact et la couverture sont **identiques** sur les deux bases
  (les 10 phrases ajoutées après le gel n'ont pas de cible). En revanche la F1/tête/POS
  diffèrent : **0,5836 / 0,7332 / 0,7581** sur le vivant, **0,5880 / 0,7388 / 0,7603** sur le
  gelé. La fiche v10 publie **0,5880 / 0,7388** : ce sont les valeurs **gelées**. Ne pas
  comparer une F1 vivante à une F1 gelée (voir § 6).
- **L'exact/labels est saturé.** 220 labels, 220 exacts, dans **tous** les sous-ensembles :
  le taux exact vaut **1,0** par construction, il ne peut plus distinguer dev de test. La
  seule mesure qui bouge encore est la **couverture** (19 spans non prédits), avec la F1/tête
  de segmentation. C'est le changement de nature du banc par rapport à la v7 (où r102 était le
  seul écart d'attachement, et changeait de moitié).

## 2. Le split canonique

| | phrases | tokens | cibles | labels | couverture | exact/labels | F1 | tête | POS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **dev** | 422 | 2 185 | 163 | 152 | 152/163 = **0,9325** | **152/152 = 1,0** | 0,5812 | 0,7330 | 0,7547 |
| **test** | 190 | 994 | 76 | 68 | 68/76 = **0,8947** | **68/68 = 1,0** | 0,5890 | 0,7337 | 0,7656 |
| tout | 612 | 3 179 | 239 | 220 | 220/239 = **0,9205** | **220/220 = 1,0** | 0,5836 | 0,7332 | 0,7581 |

Le top-k suit : **219/220** (une cible au bon span n'a pas sa cible dans les candidats) ;
`exact_any` = **220/220**. Verbe/nom : **149/149** et **71/71**. Tête d'attachement :
**220/220** (top-k 219/220).

### 2.1 Par langue

| groupe | dev cibles | dev labels | dev couv. | dev exact/labels | dev F1 | dev tête | dev POS | test cibles | test labels | test couv. | test exact/labels | test F1 | test tête | test POS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **fr** | 101 | 91 | 0,9010 | 91/91 | 0,5517 | 0,7041 | 0,7558 | 50 | 43 | 0,8600 | 43/43 | 0,5702 | 0,7188 | 0,7512 |
| **en** | 62 | 61 | 0,9839 | 61/61 | 0,6370 | 0,7861 | 0,7528 | 26 | 25 | 0,9615 | 25/25 | 0,6271 | 0,7627 | 0,7925 |

**Le français porte 17 des 19 spans perdus, l'anglais 2** — mais c'est un **effet de source**,
pas un effet de langue (voir § 2.4). Les F1/tête anglaises sont plus hautes, et ce n'est pas
un effet d'attachement (1,0 des deux côtés) mais de **segmentation** GN/GV.

### 2.2 Par type

| groupe | dev cibles | dev labels | dev couv. | dev exact/labels | dev F1 | dev tête | test cibles | test labels | test couv. | test exact/labels | test F1 | test tête |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **REL** | 57 | 51 | 0,8947 | 51/51 | 0,7907 | 0,9573 | 17 | 14 | **0,8235** | 14/14 | 0,7179 | 0,9444 |
| **SUB** | 45 | 42 | 0,9333 | 42/42 | 0,9247 | 0,9462 | 24 | 21 | 0,8750 | 21/21 | 0,8571 | 0,9583 |
| **GP** | 61 | 59 | 0,9672 | 59/59 | 0,8553 | 0,8609 | 35 | 33 | 0,9429 | 33/33 | 0,8571 | 0,8675 |

Le REL est le type le plus fragile en couverture (9 des 19 spans perdus), le GP le plus
solide. La F1 par type est calculée sur **tous les segments du type**, pas seulement sur les
cibles : le GP a 101 tp pour 96 cibles (5 GP non-cibles prédits exactement), et sa précision
(0,771) paie les GP en trop ; le rappel est 0,962. Le REL a une précision de 0,692 (29 fp)
pour un rappel de 0,878. La tête REL/SUB est très haute (~0,95), la tête GP plus basse
(~0,863), cohérente avec les GP en trop.

### 2.3 Le croisement fin

| croisement | dev cibles | dev labels | dev exact | test cibles | test labels | test exact |
|---|---:|---:|---:|---:|---:|---:|
| REL/fr | 34 | 29 | 29 | 12 | 9 | 9 |
| REL/en | 23 | 22 | 22 | **5** | **5** | 5 |
| SUB/fr | 29 | 26 | 26 | 14 | 12 | 12 |
| SUB/en | 16 | 16 | 16 | 10 | 9 | 9 |
| GP/fr | 38 | 36 | 36 | 24 | 22 | 22 |
| GP/en | 23 | 23 | 23 | 11 | 11 | 11 |

`REL/en` au test reste la cellule la plus mince (5 cibles), mais elle est **5/5** ; `REL/fr`
au test est la plus basse (9/12 = 0,75), avec r255, s035 et s141 perdus. `hand` au test =
**3 cibles, toutes GP** : `hand/REL` et `hand/SUB` sont **absents du test canonique**.

### 2.4 Par source — et le confond synthétique/français

| source | dev cibles/labels | dev couv. | test cibles/labels | test couv. | tout cibles/labels | tout couv. |
|---|---:|---:|---:|---:|---:|---:|
| `hand` | 10/10 | **1,0** | 3/3 | **1,0** | 13/13 | **1,0** |
| `reel` | 121/119 | 0,9835 | 50/47 | 0,9400 | 171/166 | 0,9708 |
| `synthetique` | 32/23 | 0,7188 | 23/18 | 0,7826 | 55/41 | **0,7455** |

| groupe | phrases | cibles | labels | couv. | F1 | tête | POS |
|---|---:|---:|---:|---:|---:|---:|---:|
| **réel fr** (`hand`+`reel`) | 242 | 96 | 93 | **0,9688** | 0,5379 | 0,6804 | 0,7673 |
| **réel en** | 210 | 88 | 86 | **0,9773** | 0,6341 | 0,7791 | 0,7648 |
| **synth fr** | 160 | 55 | 41 | **0,7455** | 0,5969 | 0,7682 | 0,7296 |
| tout fr | 402 | 151 | 134 | 0,8874 | 0,5575 | 0,7087 | 0,7543 |
| tout en | 210 | 88 | 86 | 0,9773 | 0,6341 | 0,7791 | 0,7648 |

**Le déficit français de couverture est un effet de composition (Simpson).** Le synthétique
est **français seulement** ; sa couverture est 0,7455, et il pèse 55 des 151 cibles
françaises. Sur le **réel**, le français est à **0,9688** et l'anglais à **0,9773** : 0,85 point
d'écart, non significatif (test de proportion : z=0,54 ; p=0,72). La différence globale
(0,8874 contre 0,9773) est donc une **composition de sources**, pas une faiblesse du français.
En revanche, la F1 française reste plus basse **sur le réel** (0,5379 contre 0,6341) : c'est
une différence de **segmentation GN/GV**, pas d'attachement. Le synthétique a la couverture
la plus basse mais la **F1 la plus haute** (0,5969 contre 0,5798 au réel) : ses phrases sont
simples à segmenter, mais le lexique/gold y perd des cibles.

Les 19 spans perdus se répartissent **14 synthétiques + 5 réels**. Les 5 réels sont
`r035` (REL/en, relative zéro), `r255` (REL/fr, lexique), `r264` (SUB/fr, tokenisation),
`r288` (SUB/en, adverbe final) et `r303` (SUB/fr, régression nouvelle). Les 14 synthétiques
sont 7 REL, 3 SUB et 4 GP ; 19 spans, 17 français, 2 anglais.

### 2.5 Les 19 spans perdus

| id | lg | type | source | span | cible | seau | classe |
|---|---|---|---|---:|---|---:|---|
| `r035` | en | REL | reel | 9:24 | `film` | 2 | A17 hors périmètre (relative zéro) |
| `r255` | fr | REL | reel | 11:27 | `voiture` | 0 | A17 hors périmètre (lexique) |
| `r264` | fr | SUB | reel | 8:26 | `sais` | 0 | A17 hors périmètre (tokenisation) |
| `r288` | en | SUB | reel | 7:29 | `know` | 0 | A17 hors périmètre (adverbe final) |
| `r303` | fr | SUB | reel | 8:23 | `pars` | 2 | **régression nouvelle (R1c)** |
| `s010` | fr | REL | synthetique | 10:18 | `chemin` | 1 | A17 non récupérable (lexique) |
| `s027` | fr | GP | synthetique | 31:33 | `marche` | 1 | A17 non récupérable (gold) |
| `s035` | fr | REL | synthetique | 10:19 | `papier` | 0 | A17 non récupérable (lexique) |
| `s037` | fr | REL | synthetique | 5:15 | `Paul` | 1 | **R2 non intégrée** |
| `s044` | fr | SUB | synthetique | 17:29 | `nage` | 2 | A17 non récupérable (lexique) |
| `s061` | fr | REL | synthetique | 9:18 | `nuage` | 2 | A17 non récupérable (lexique) |
| `s065` | fr | REL | synthetique | 5:17 | `elle` | 2 | A17 non récupérable (lexique) |
| `s112` | fr | SUB | synthetique | 24:39 | `nage` | 0 | A17 non récupérable (lexique) |
| `s114` | fr | SUB | synthetique | 22:43 | `dessine` | 2 | A17 non récupérable (lexique) |
| `s125` | fr | REL | synthetique | 11:21 | `renard` | 1 | A17 non récupérable (lexique) |
| `s141` | fr | REL | synthetique | 5:15 | `Emma` | 0 | A17 non récupérable (lexique) |
| `s146` | fr | GP | synthetique | 25:35 | `observe` | 0 | A17 non récupérable (gold) |
| `s148` | fr | GP | synthetique | 20:39 | `nage` | 2 | A17 non récupérable (gold) |
| `s160` | fr | GP | synthetique | 20:29 | `nage` | 0 | A17 non récupérable (gold) |

**Décomposition correcte : 17 inatteignables + `s037` (R2) + `r303` (régression R1c) = 19.**
La fiche v10 écrit « 17 inatteignables + r255 + r264 » : c'est un **double comptage**, car
`r255` et `r264` appartiennent déjà aux 17. Elle omet `s037` et `r303`. Le détail :

- **13 A17 non récupérables** : `s010`, `s035`, `s061`, `s065`, `s125`, `s141` (REL),
  `s044`, `s112`, `s114` (SUB), `s027`, `s146`, `s148`, `s160` (GP) ;
- **4 A17 hors périmètre** : `r035`, `r255` (REL), `r264`, `r288` (SUB) ;
- **1 R2 non intégrée** : `s037` (« Paul qui marche marche » ; la règle `precedent is None
  → SUB` n'a jamais été remplacée par `DURS`/`RELATIFS`) ;
- **1 régression nouvelle** : `r303` (« Je pars car il est tard », SUB `[8:18]` au lieu de
  `[8:23]`). La garde `predicat_vu` de `160d08ca` exclut l'adverbe final `tard`, qui est ici
  le complément du prédicat, pas un adverbe de phrase. La même garde a récupéré `g017` :
  c'est un **échange g017 ↔ r303**, net 0 sur les SUB, mais la fiche v10 le présente comme
  un gain R1c sans perte.

## 3. L'équilibre du split

| catégorie | dev | test | total |
|---|---:|---:|---:|
| phrases | 422 | 190 | 612 |
| `hand` (phrases) | 15 | **5** | 20 |
| `reel` (phrases) | 302 | 130 | 432 |
| `synthetique` (phrases) | 105 | 55 | 160 |
| fr (phrases) | 277 | 125 | 402 |
| en (phrases) | 145 | 65 | 210 |
| REL (cibles) | 57 | **17** | 74 |
| SUB (cibles) | 45 | 24 | 69 |
| GP (cibles) | 61 | 35 | 96 |
| `hand` (cibles) | 10 | **3** | 13 |
| `reel` (cibles) | 121 | 50 | 171 |
| `synthetique` (cibles) | 32 | 23 | 55 |

**Aucune catégorie demandée n'est absente d'une moitié** : les trois sources, les deux
langues et les trois types de cibles sont présents des deux côtés. Les χ² d'ajustement du
seau test aux proportions du corpus (méthode de la fiche v7) reproduisent la v7 :
sources **0,9331** (p=0,6272), langues **0,0009** (p=0,9761), types **2,6613** (p=0,2643),
types×langues **3,4887** (p=0,6251). Le test de **contingence test×dev**, plus strict, ne
rejette rien non plus : sources 1,3532 (p=0,5083), langues 0,0013 (p=0,9712), types 3,9022
(p=0,1421), types×langues 5,1153 (p=0,4020). Les tailles de seaux sont **190/229/193**
(χ²=4,6176 ; p=0,0994) : le hash **n'est pas stratifié**, il est vérifié a posteriori.

Quatre réserves de lecture :

- **`hand` est mince** : 5 phrases au test, **3 cibles, toutes GP**. `hand/REL` (1 cible) et
  `hand/SUB` (2 cibles) sont **entièrement dans dev** ; le test ne dit rien d'eux. `hand/en`
  n'a que 3 cibles, `hand/fr` 10. Le 100 % `hand` (13/13) est une perfection de 13 cas.
- **`REL/en` au test = 5 cibles** (5/5), contre 23 en dev. Toute conclusion sur l'anglais REL
  au test est fragile.
- **Le mélange des types varie** : test **REL-pauvre** (17 cibles, 22,4 %, contre 35,0 % en
  dev) et **GP-riche** (35, 46,1 %, contre 37,4 %) ; l'attendu serait 23,5 REL et 30,5 GP.
  Ce n'est pas significatif (p=0,264), mais c'est le principal levier des agrégats : le test
  a moins de REL (couverture 0,8235) et plus de GP (couverture 0,9429).
- **Le synthétique est français seulement** (160 phrases, 0 en) : source et langue y sont
  confondues. Le test est aussi **synthétique-riche** (28,9 % des phrases contre 24,9 % en
  dev ; 23/76 = 30,3 % des cibles contre 32/163 = 19,6 %). C'est ce qui explique une partie
  de l'écart de couverture français, et non une faiblesse de la langue.

**Catégories absentes du test canonique** : `hand/REL`, `hand/SUB` (fines) ; `synthetique/en`
est **globalement** absente (propriété du corpus, pas du split). Aux décalés : `hand/REL` au
dev du décalé 1 ; `hand/en` au test du décalé 1 ; `hand/REL` et `hand/fr` au test du décalé 2.
**Aucune catégorie principale** (source, langue, type de cible) n'est absente.

**Catégories jamais prédites** : le gold contient **35 ADJ, 30 ADV, 9 PONCT** segments ;
l'heuristique n'en prédit aucun. Leur F1 est 0 par construction et ils ajoutent **74 fn** au
dénominateur global de la F1. Ce n'est pas une absence du split, mais un plafond de la F1
union : les F1 par type REL/SUB/GP sont les mesures pertinentes pour l'attachement.

## 4. La stabilité : trois découpages

| split | règle test | dev phrases | dev cibles | dev labels | dev exact | dev couv. | dev F1 | dev tête | dev POS | test phrases | test cibles | test labels | test exact | test couv. | test F1 | test tête | test POS |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| canonique | `%3==0` | 422 | 163 | 152 | 152 | 0,9325 | 0,5812 | 0,7330 | 0,7547 | 190 | 76 | 68 | 68 | 0,8947 | 0,5890 | 0,7337 | 0,7656 |
| décalé 1 | `%3==1` | 383 | 150 | 135 | 135 | 0,9000 | 0,5793 | 0,7297 | 0,7602 | 229 | 89 | 85 | 85 | 0,9551 | 0,5908 | 0,7390 | 0,7545 |
| décalé 2 | `%3==2` | 419 | 165 | 153 | 153 | 0,9273 | 0,5900 | 0,7366 | 0,7596 | 193 | 74 | 67 | 67 | 0,9054 | 0,5699 | 0,7259 | 0,7549 |
| **étendue** | | | | **18** | 0 | **0,0325** | **0,0107** | **0,0069** | **0,0055** | | | **18** | 0 | **0,0603** | **0,0209** | **0,0131** | **0,0111** |

**L'exact/labels vaut 1,0 dans les six moitiés** : l'étendue du **taux** est 0, pas 1 cas.
Les 18 exacts d'étendue sont les **nombres** de labels des seaux (152/135/153 en dev,
68/85/67 en test), pas des erreurs. La seule mesure qui varie est la **couverture**, puis
F1/tête/POS par composition.

| split | écart exact | écart couverture | écart F1 | écart tête | écart POS |
|---|---:|---:|---:|---:|---:|
| canonique | 0 | **+0,0378** | −0,0078 | −0,0007 | −0,0109 |
| décalé 1 | 0 | **−0,0551** | −0,0115 | −0,0093 | +0,0057 |
| décalé 2 | 0 | **+0,0219** | +0,0201 | +0,0107 | +0,0047 |

Le **signe** de l'écart dev/test change pour la couverture, la F1 et la tête (et pour la POS
entre canonique et décalés) : ce n'est pas un effet dev/test stable, c'est la répartition
des 19 spans et la composition. Au canonique, le test est **GP-riche** ; sa couverture brute
(0,8947) est au-dessus de sa valeur **standardisée sur la composition du dev** (0,8824), donc
l'écart réel est de **−5,01 points** une fois la composition contrôlée. Mais les IC Wilson se
recouvrent largement et le test de proportion ne rejette pas : **z=1,005 ; p=0,315**. Par
type : REL z=0,79 (p=0,43), SUB z=0,82 (p=0,41), GP z=0,57 (p=0,57) ; par langue : fr z=0,75
(p=0,45), en z=0,64 (p=0,52).

**Les 19 spans sont fixes par phrase** : le split ne change pas le modèle, il répartit des
analyses identiques. Les spans perdus se répartissent **8 / 4 / 7** dans les seaux 0/1/2,
pour des attendus de **6,04 / 7,08 / 5,88** (χ²=2,372 ; p=0,3054) : compatible avec un tirage
aléatoire. L'étendue de couverture au test (6,03 points) vient des dénominateurs (76/89/74) et
de ce 8/4/7, pas d'une instabilité du modèle.

**Contrôle Monte-Carlo.** 2 000 partitions aléatoires aux tailles réelles 190/229/193, mêmes
phrases, mêmes annotations ; on compare l'étendue des trois seaux (test) et des trois
compléments (dev) :

| mesure | observé test | MC p05 | MC médiane | MC p95 | p | observé dev | MC p05 | MC médiane | MC p95 | p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| couverture | **0,0603** | 0,0143 | 0,0494 | 0,1008 | 0,345 | 0,0325 | 0,0069 | 0,0248 | 0,0510 | 0,295 |
| F1 | 0,0209 | 0,0101 | 0,0365 | 0,0743 | 0,7965 | 0,0107 | 0,0051 | 0,0184 | 0,0377 | 0,789 |
| tête | 0,0131 | 0,0076 | 0,0268 | 0,0543 | 0,86 | 0,0069 | 0,0038 | 0,0134 | 0,0275 | 0,8425 |
| POS | 0,0111 | 0,0051 | 0,0184 | 0,0378 | 0,7635 | 0,0055 | 0,0025 | 0,0092 | 0,0192 | 0,766 |
| couv. REL | 0,0797 | 0,0299 | 0,1105 | 0,2208 | 0,693 | 0,0343 | 0,0142 | 0,0547 | 0,1126 | 0,7505 |
| couv. SUB | **0,1304** | 0,0283 | 0,0964 | 0,1905 | 0,316 | 0,0624 | 0,0130 | 0,0475 | 0,0963 | 0,3085 |
| couv. GP | 0,0294 | 0,0204 | 0,0645 | 0,1111 | 0,8415 | 0,0172 | 0,0117 | 0,0285 | 0,0547 | 0,8015 |
| couv. fr | 0,0686 | 0,0204 | 0,0726 | 0,1498 | 0,5445 | 0,0378 | 0,0100 | 0,0361 | 0,0767 | 0,469 |
| couv. en | 0,0385 | 0,0323 | 0,0417 | 0,0769 | 0,662 | 0,0202 | 0,0129 | 0,0196 | 0,0385 | 0,4775 |

Toutes les étendues observées sont **dans la bande 95 %** du tirage aléatoire, et souvent
sous la médiane. La plus grande (couverture test 6,03 pts) est à p=0,345 ; la plus spectaculaire
en apparence (couv. SUB test 13,04 pts) est à p=0,316, sous le p95 de 19,05 : elle vient des
3 SUB perdus au canonique contre 0 au décalé 1, pour 24/22 cibles. **Conclusion : le split est
stable ; les variations sont du bruit de partition et de composition, pas une fragilité du
modèle.**

**Lecture par type et par langue.** Les couvertures par type aux trois splits (test) sont
REL 0,8235 / 0,9032 / 0,8846 ; SUB 0,8750 / 1,0 / 0,8696 ; GP 0,9429 / 0,9722 / 0,9600. Les
F1 par type (test) sont REL 0,7179 / 0,7778 / 0,8070 ; SUB 0,8571 / 0,9565 / 0,8936 ; GP
0,8571 / 0,8667 / 0,8387. Les couvertures par langue (test) sont fr 0,86 / 0,9286 / 0,8667 ;
en 0,9615 / 1,0 / 0,9655. Le français est plus variable (6,86 points) que l'anglais
(3,85 points), parce qu'il concentre les spans perdus ; les IC restent larges.

## 5. L'écart dev/test

- **Exact** : dev 152/152, test 68/68 → **0,0000**, **0 cas**. L'écart de la v7 (133/134
  contre 62/62, 0,75 point) a disparu avec r102 ; il ne peut plus réapparaître par
  l'attachement, qui est parfait sur les 220 labels.
- **Couverture** : dev 0,9325, test 0,8947 → **+3,78 points** au canonique. Mais le test brut
  est GP-riche : standardisé sur la composition du dev, il vaut **0,8824**, soit **−5,01
  points**. Les IC Wilson se recouvrent (dev [0,8832 ; 0,9619], test [0,8058 ; 0,9457]) et
  z=1,005 (p=0,315) : l'écart n'est pas acquis. Il s'inverse aux décalés (−5,51 et +2,19), et
  la couverture est la seule mesure dont l'étendue (6,03 points) est proche de celle du
  hasard de partition (médiane 4,94 ; p=0,345).
- **F1** : test **+0,78 point** (0,5836 contre 0,5890), mais c'est un **effet de
  composition**, pas une meilleure segmentation des cibles : le test est plus synthétique
  (30,3 % des cibles contre 19,6 %) et le synthétique a une F1 plus haute (0,6078 au test
  contre 0,5823 au réel) ; à source fixée, le réel gagne +0,35 point et le synthétique
  +1,74. Sur les types cibles, le test est **plus bas** : REL 0,7179 contre 0,7907 (−7,3),
  SUB 0,8571 contre 0,9247 (−6,8), GP 0,8571 contre 0,8553 (+0,2). La F1 globale ne mesure
  donc pas la généralisation de l'attachement ; elle mesure surtout GN/GV et la source.
- **Tête** : test **+0,07 point** (0,7337 contre 0,7330), masque un réel **−1,23** et un
  synthétique **+3,33** : la composition annule les deux. Par type, REL **−1,29** au test
  (0,9444 contre 0,9573), SUB +1,21, GP +0,66. Rien de significatif.
- **POS** : test **+1,09 point** (0,7656 contre 0,7547), exactement le motif de la v7 :
  l'anglais gagne (+3,97), le français recule (−0,46). La POS est **invariante** entre v7,
  audit, v9 et v10 : les corrections ne touchent ni les tokens ni les classes.

**Synthèse de l'écart** : l'écart dev/test d'exactitude est **nul** ; l'écart de couverture
(+3,78 au canonique) **change de signe** aux décalés, n'est pas significatif, et s'explique
par la composition (test GP-riche, synthétique-riche) et par les 19 spans fixes. Le split ne
"pénalise" pas le test ; il ne peut plus le faire par l'attachement, seulement par la
couverture.

## 6. Comparaison v7 (`69bd865e`), audit R1/R3 (`f908d7b0`), v9 (`160d08ca`)

Les trois commits ont été **rejoués** avec le même `evaluer_bloc`, le même gold et le module
`generateur` du dépôt (copie `/tmp`, `RACINE` du dépôt) : les valeurs publiées sont reproduites
au chiffre près. F1/tête sont **vivantes 612** ; les valeurs gelées 602 sont données après.

| commit | dev labels | dev exact | dev couv. | dev F1 | dev tête | test labels | test exact | test couv. | test F1 | test tête | tout labels | tout exact | tout couv. | tout F1 | tout tête |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| v7 `69bd865e` | 134 | 133 | 0,8221 | 0,5512 | 0,7132 | 62 | 62 | 0,8158 | 0,5651 | 0,7196 | 196 | 195 | 0,8201 | 0,5555 | 0,7152 |
| audit `f908d7b0` | 148 | 148 | 0,9080 | 0,5723 | 0,7270 | 64 | 64 | 0,8421 | 0,5714 | 0,7241 | 212 | 212 | 0,8870 | 0,5720 | 0,7262 |
| v9 `160d08ca` | 152 | 152 | 0,9325 | 0,5807 | 0,7327 | 67 | 67 | 0,8816 | 0,5855 | 0,7323 | 219 | 219 | 0,9163 | 0,5822 | 0,7326 |
| **v10 `710ec7f9`** | **152** | **152** | **0,9325** | **0,5812** | **0,7330** | **68** | **68** | **0,8947** | **0,5890** | **0,7337** | **220** | **220** | **0,9205** | **0,5836** | **0,7332** |

| commit | F1 gelée 602 | tête gelée 602 | POS gelée 602 |
|---|---:|---:|---:|
| v7 | 0,5595 | 0,7205 | 0,7603 |
| audit | 0,5763 | 0,7316 | 0,7603 |
| v9 | **0,5866** | 0,7381 | 0,7603 |
| **v10** | **0,5880** | **0,7388** | **0,7603** |

**Deltas v7 → v10** : dev **+18 labels, +19 exacts**, test **+6 / +6**, tout **+24 / +25** ;
couverture **+0,1104 / +0,0789 / +0,1004** ; F1 vivante **+0,0300 / +0,0239 / +0,0281** ;
tête **+0,0198 / +0,0141 / +0,0180**. Le +1 d'exact par rapport aux labels est r102, l'erreur
unique de la v7, devenue exacte. **Deltas audit → v10** : dev **+4 / +4**, test **+4 / +4**,
tout **+8 / +8** ; couverture **+0,0245 / +0,0526 / +0,0335** ; F1 **+0,0089 / +0,0176 /
+0,0116** ; tête **+0,0060 / +0,0096 / +0,0070**. **Deltas v9 → v10** : dev **0 / 0**, test
**+1 / +1**, tout **+1 / +1** ; couverture **0 / +0,0131 / +0,0042** ; F1 **+0,0005 /
+0,0035 / +0,0014** ; tête **+0,0003 / +0,0014 / +0,0006**.

### 6.1 Trois énoncés de la fiche v10 à corriger

1. **La correction `-ée` est inerte.** La fiche v10 attribue à `-ée` le gain `r255`
   (« le verbe de la relative »). Or `r255` est **toujours perdu** ; `_est_verbe("achetée")`
   est faux parce que **`acheter` n'est pas dans `VERBES_CONNUS`**, et la règle
   `n[:-2] + "er"` existe depuis `a408a909`, pas depuis `710ec7f9`. Le diff du commit sur
   `tools/bloc_linguistique.py` ne touche **que la garde GP** (3 lignes). Le **+1 test** est
   `r153` (`for the bus`, GP/en), dû à la **garde DET**. La fiche se contredit elle-même :
   elle liste `r255` parmi les 19 et le présente comme corrigé.
2. **La décomposition des 19 est fausse.** « 17 inatteignables + `r255` + `r264` » compte
   deux fois `r255` et `r264`, qui sont **dans** les 17, et omet `s037` et `r303`. La bonne
   décomposition est **17 + `s037` (R2) + `r303` (R1c)**. Le `r303` est une **régression
   nouvelle** de `160d08ca` (la garde `predicat_vu` exclut `tard` de « car il est tard ») ;
   `g017` a été récupéré par la même garde, d'où un échange net 0 sur les SUB.
3. **La ligne F1 v9 → v10 mélange les bases.** La fiche écrit « F1 (union, 602) 0,5822 » pour
   v9 et « 0,5880 » pour v10. Or **0,5822 est la F1 vivante v9** ; la F1 **gelée** v9 est
   **0,5866**. Sur base gelée, le delta est **+0,0014** (0,5866 → 0,5880), pas +0,0058 ;
   sur base vivante, il est aussi **+0,0014** (0,5822 → 0,5836). La tête 0,7381 → 0,7388
   est, elle, bien gelée et cohérente (+0,0007). L'audit R1/R3 avait déjà signalé ce piège
   vivant/gelé ; la fiche v10 le réintroduit.

**Ce qui est juste dans la fiche v10** : les 220/220, la couverture 0,9205, la F1 gelée
0,5880, la tête 0,7388, les 19 spans (9 REL, 6 SUB, 4 GP) et le top-k 219/239. Les chiffres
globaux sont bons ; ce sont l'attribution de `-ée`, la décomposition des 19 et la base de la
F1 qui ne le sont pas.

### 6.2 La garde GP : un effet plus large que `r153`

La garde DET du GP n'agit pas que sur `r153` : elle modifie **3 phrases** entre v9 et v10
(`g004`, `r147`, `r153`), et retire **4 faux positifs** :

| id | seau | v9 | v10 | effet |
|---|---:|---|---|---|
| `g004` | 1 | GP [11:27] + GP [11:31] + GV [28:31] | GP [11:31] | −2 faux positifs |
| `r147` | 0 | GP [22:31] + GP [22:37] + GV [32:37] | GP [22:37] | −2 faux positifs |
| `r153` | 0 | GP [8:15] + GV [16:19] | GP [8:19] | **+1 exact** (`wait`) |

C'est ce qui explique que la F1 test gagne +0,0035 et la tête +0,0014 pour un seul label
gagné : la précision GP s'améliore sur `g004` et `r147`. C'est un point **positif** de la
garde, que la fiche v10 ne mentionne pas.

## 7. Contrôles négatifs

- **Fidélité du harnais** : l'agrégation par phrase redonne `evaluer_bloc` avec un écart
  **0,0** sur 612, dev et test ; deux exécutions donnent le même digest ; l'union des moitiés
  redonne 612, 239 cibles et 220 labels. Le harnais n'invente rien.
- **Partitions aléatoires** : 2 000 tirages aux tailles réelles (190/229/193), mêmes
  annotations. Toutes les étendues observées sont **dans la bande p05–p95** ; les p-values
  vont de **0,295** (couverture dev) à **0,86** (tête test). Le split ne fabrique pas de
  signal : il répartit 19 spans fixes.
- **Hypergéométrie des spans** : 8/4/7 perdus pour 6,04/7,08/5,88 attendus, χ²=2,372,
  p=0,3054. Rien d'anormal.
- **Taille des seaux** : 190/229/193, χ²=4,6176, p=0,0994 : le hash n'est pas stratifié, les
  seaux ne sont pas exactement égaux, mais l'écart reste tolérable.
- **Exact saturé** : le taux exact est 1,0 dans **chaque** sous-ensemble ; il ne peut pas
  servir de contrôle de split. Les contrôles portent sur la couverture, la F1, la tête et la
  POS, et sur la **distribution des 19 spans**.
- **Contrôle de cohérence des deux corrections** : `r303` est exact à `f908d7b0`, perdu à
  `160d08ca` et à `710ec7f9` ; `r280` et `g017` sont perdus à `f908d7b0`, exacts à
  `160d08ca` ; `r153` est perdu à `160d08ca`, exact à `710ec7f9`. Ces rejeux isolent les
  effets et confirment l'attribution.

## 8. Ce que ce banc ne dit pas — et ce qui pourrait le rendre faux

- **In-sample** : les règles ont été dessinées en regardant **tout** le gold, test compris.
  Le split détecte une **fragilité au découpage**, pas le **surajustement global** ; les deux
  moitiés peuvent être surajustées ensemble. Le test n'est pas un vrai held-out.
- **Exact/labels saturé** : 220/220. La mesure ne dit rien des 19 spans non prédits ; elle ne
  dit pas non plus si une cible correcte le serait sur une phrase nouvelle. C'est un
  **plafond**, pas une preuve de généralisation.
- **Petit échantillon** : 68 labels au test, 1 label = 1,47 point ; REL test 17 cibles,
  REL/en 5, `hand` test 3 ; les IC Wilson sont larges (test couverture [0,8058 ; 0,9457]).
  La couverture SUB test varie de 13,04 points entre splits pour 22–24 cibles.
- **Confond source/langue** : le synthétique est français seulement ; la couverture
  française globale (0,8874) est un **effet de composition** (Simpson). Sur le réel, fr
  0,9688 vs en 0,9773 (0,85 point, p=0,72). Toute lecture « le français couvre moins bien »
  sans contrôler la source est fausse.
- **La F1 par type n'est pas l'attachement** : elle est calculée sur **tous** les segments du
  type (y compris les non-cibles) et inclut GN/GV dans l'agrégat. Elle ne remplace pas
  l'exact/couverture. Les types ADJ/ADV/PONCT, jamais prédits, pèsent 74 fn.
- **Arbre mouvant** : la mesure est épinglée sur `710ec7f9` ; `HEAD` a avancé à `653a7981`,
  qui committe l'essai R2 + retrait de la garde d'adverbe. Cet état corrige `s037` (R2) et
  `r303` (retrait de la garde d'adverbe), mais il **perd `g017` et `r241`** : `g017`
  (« would come yesterday ») veut l'adverbe **exclu**, `r288` (« comes tomorrow ») veut
  l'adverbe **inclus** ; `r241` (« The day when we left ») devient SUB alors que le gold
  attend REL, parce que `est_sub` ajoute `when` aux subordonnants. Le couple `g017`/`r288`
  est un **ballant** : une garde unique ne peut pas satisfaire les deux sans une distinction
  sémantique (adverbe de phrase vs complément du prédicat, ou lexique temporel). L'état
  `653a7981` donne **221/221, 18 spans** (dev 152/152, test 69/69, couverture 0,9247, F1
  0,5843, tête 0,7330, POS 0,7581), mais ce n'est pas l'état mesuré ici.
- **Rejeu des anciens commits** : les modules sont copiés dans `/tmp` avec `RACINE` du dépôt ;
  le `generateur` S est celui du dépôt (**le même pour tous les rejeux**), et le gold n'a pas
  changé entre `69bd865e` et `710ec7f9` (vérifié : aucun diff de `tools/tests/linguistique/`).
  Les valeurs publiées sont reproduites, ce qui valide la comparaison.
- **Les 17 inatteignables** sont la classification de l'audit R1/R3, pas un jugement nouveau :
  4 d'entre eux sont « hors périmètre » (récupérables en changeant le gold/le lexique), 13 sont
  non récupérables sans changer le gold. `s037` et `r303` ne sont pas dans ces 17.

## 9. La suite

1. **Corriger la fiche v10** : retirer l'attribution `-ée` → `r255`, remplacer « 17 + r255 +
   r264 » par « 17 + s037 + r303 », et remettre la F1 v9 gelée (0,5866) dans la ligne
   « 602 ». Les chiffres globaux (220/220, 0,9205, 0,5880) restent.
2. **`r303` sans perdre `g017`** : la garde `predicat_vu` doit distinguer l'adverbe de phrase
   (« yesterday » exclu) de l'adverbe complément du prédicat (« tard » inclus). Une condition
   sur le lexique/la position (adverbe final après un verbe copule ou un verbe intransitif)
   est à tester ; le retrait pur de la garde (arbre sale) récupère `r303`/`r288` mais perd
   `g017`, et `est_sub` dans la ligne `stype` perd `r241`.
3. **`s037` (R2)** : implémenter `DURS`/`RELATIFS` pour un relatif initial sans précédent
   (`qui`, `dont`, `where`…) au lieu de `precedent is None → SUB`. Vérifier `r241` : `when`
   n'est pas un relatif dur, il doit rester SUB ou REL selon l'antécédent.
4. **`r255`** : ajouter `acheter` à `VERBES_CONNUS` (ou une règle `-ée` qui vérifie le
   lexique) ; ensuite `r255` peut redevenir exact. Re-mesurer les 19 spans.
5. **Garder le split** ; publier systématiquement **par type et par langue**, et **contrôler
   la source** avant de conclure sur une langue. La couverture est la mesure primaire ; le
   taux exact est saturé.
6. **Re-mesurer quand le module sera stabilisé** : l'état `653a7981` est une exploration
   (`g017`/`r241`), pas l'état de la fiche.

## 10. Fichiers

- [`rapport-dev-test-v10.md`](rapport-dev-test-v10.md) — cette fiche.
- [`pensee-dev-test-v10.json`](pensee-dev-test-v10.json) — les trois splits, les agrégats
  par langue/type/source, les contrôles (χ², Wilson, z, hypergéométrie, Monte-Carlo), les
  19 spans, les rejeux v7/audit/v9/v10 et les deltas.
- [`gold_split.py`](../tools/tests/linguistique/gold_split.py) — le split (`dev`, `test`,
  `compter`).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `charger`,
  `evaluer_bloc`, `charger_gele`.
- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — l'heuristique mesurée
  (module épinglé `710ec7f9`).
- Fiches comparées : [`rapport-dev-test-v7.md`](rapport-dev-test-v7.md),
  [`rapport-audit-r1r3.md`](rapport-audit-r1r3.md),
  [`rapport-pensee-v10.md`](rapport-pensee-v10.md).

**Aucun fichier existant n'a été modifié ; aucun commit n'a été fait.** Les scripts de mesure
vivaient dans `/tmp/v10/` et ne sont pas livrés.
