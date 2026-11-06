# B13 — dev/test en v7 : dev 133/134, test 62/62, le split tient sur trois découpages

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Commit mesuré** : `69bd865e` · **Verdict** : ✅
> Le gold 612 est re-coupé par `crc32(id) % 3 == 0` (test) : **dev 133/134 (0,9925)**, **test 62/62 (1,0)**
> — mais le test ne couvre que **62 des 76 cibles** (0,8158). En décalant le split (`%3==1`, `%3==2`),
> l'exact reste à **1 cas près** (étendue 0,0172), la couverture à **3 spans près** (14/13/16 des 43),
> la F1 à **2,4 points**. **Aucune catégorie demandée n'est absente** ; les écarts dev/test tiennent à
> **un échec unique (r102)** et à la **composition par type**, pas au split.
>
> **Dispositif** : [`gold_split.py`](../tools/tests/linguistique/gold_split.py) (`dev`, `test`, `compter`),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`),
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (heuristique) ; JSON
> [`pensee-dev-test-v7.json`](pensee-dev-test-v7.json).

## 1. Ce qui est mesuré

- **Corpus** : `charger()` = **612 phrases** (20 `hand`, 432 `reel`, 160 `synthetique`), 402 fr / 210 en,
  **239 cibles** (REL 74, SUB 69, GP 96) ; **196 labels au bon span**, **43 spans perdus**.
- **Split** : `crc32(str(id)) % 3`. Canonique : test = 0 ; décalé 1 : test = 1 ; décalé 2 : test = 2 ;
  dev = complément. Aucune phrase dupliquée ; l'union redonne 612 (vérifié).
- **Mesure** : `evaluer_bloc("heuristique", Heuristique(), sous-ensemble)`. `exact` = cible correcte
  **parmi les labels au bon span** ; `couverture` = labels / cibles ; F1 et tête sur les syntagmes ;
  POS au token. On mesure les deux moitiés, puis on agrège par langue et par type.
- **Validation** : une agrégation indépendante par phrase redonne exactement `evaluer_bloc` sur les 612 :
  195/196, 196/239, F1 0,5555, tête 0,7152, POS 0,7581 (champ `validation` du JSON).

> **Vivant 612 vs gelé 602.** La fiche v7 ([couverture-v7](rapport-pensee-couverture-v7.md)) chiffre
> **F1 0,5595, tête 0,7205, POS 0,7603** sur le **gelé 602**. Ici, le split vit sur le **vivant 612** :
> les 10 phrases réelles ajoutées après le gel **n'ont pas de cible**, donc **195/196 et 196/239 sont
> identiques**, mais la F1/tête/POS valent **0,5555 / 0,7152 / 0,7581**. Ne pas comparer les F1 des deux
> fiches sans ce décalage ; seuls les 239 cibles et l'exact/labels sont directement comparables.

## 2. Le split canonique

| | phrases | cibles | labels | couverture | exact/labels | F1 | tête |
|---|---:|---:|---:|---:|---:|---:|---:|
| **dev** | 422 | 163 | 134 | 134/163 = **0,8221** | 133/134 = **0,9925** | 0,5512 | 0,7132 |
| **test** | 190 | 76 | 62 | 62/76 = **0,8158** | 62/62 = **1,0** | 0,5651 | 0,7196 |
| tout | 612 | 239 | 196 | 196/239 = **0,8201** | 195/196 = **0,9949** | 0,5555 | 0,7152 |

### Par langue et par type

| groupe | dev cibles | dev labels | dev couv. | dev exact/labels | test cibles | test labels | test couv. | test exact/labels |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **fr** | 101 | 92 | 0,9109 | 92/92 = 1,0 | 50 | 43 | 0,8600 | 43/43 = 1,0 |
| **en** | 62 | 42 | 0,6774 | 41/42 = **0,9762** | 26 | 19 | 0,7308 | 19/19 = 1,0 |
| **REL** | 57 | 42 | 0,7368 | 42/42 = 1,0 | 17 | 11 | 0,6471 | 11/11 = 1,0 |
| **SUB** | 45 | 33 | 0,7333 | 33/33 = 1,0 | 24 | 19 | 0,7917 | 19/19 = 1,0 |
| **GP** | 61 | 59 | 0,9672 | 58/59 = **0,9831** | 35 | 32 | 0,9143 | 32/32 = 1,0 |

| groupe | dev F1 | dev tête | test F1 | test tête |
|---|---:|---:|---:|---:|
| fr | 0,5468 | 0,6989 | 0,5639 | 0,7141 |
| en | 0,5594 | 0,7395 | 0,5674 | 0,7303 |
| REL | 0,6176 | 0,9016 | 0,5500 | 0,9444 |
| SUB | 0,7727 | 0,9091 | 0,7600 | 0,9388 |
| GP | 0,8497 | 0,8609 | 0,8095 | 0,8537 |

La F1 et la tête sont calculées sur les **segments du type**, pas seulement sur les cibles ; les
colonnes « cibles/labels » du tableau précédent mesurent l'attachement, pas la segmentation.

Le croisement fin montre les cellules réellement minces :

| croisement | dev cibles | dev labels | dev exact | test cibles | test labels | test exact |
|---|---:|---:|---:|---:|---:|---:|
| REL/fr | 34 | 29 | 29 | 12 | 9 | 9 |
| REL/en | 23 | 13 | 13 | **5** | **2** | 2 |
| SUB/fr | 29 | 27 | 27 | 14 | 12 | 12 |
| SUB/en | 16 | 6 | 6 | 10 | 7 | 7 |
| GP/fr | 38 | 36 | 36 | 24 | 22 | 22 |
| GP/en | 23 | 23 | 22 | 11 | 10 | 10 |

**Les 43 spans perdus** (hors du dénominateur exact, mesurés par la couverture) : **REL 21, SUB 17,
GP 5** ; dev 29 = 15 REL + 12 SUB + 2 GP ; test 14 = 6 REL + 5 SUB + 3 GP. Le test perd donc
3 des 5 GP perdus, ce qui pèse sur sa couverture GP (0,9143 contre 0,9672 en dev) et sur sa F1 GP.

## 3. L'équilibre du split

| catégorie | dev | test | total |
|---|---:|---:|---:|
| `hand` (phrases) | 15 | **5** | 20 |
| `reel` (phrases) | 302 | 130 | 432 |
| `synthetique` (phrases) | 105 | 55 | 160 |
| fr (phrases) | 277 | 125 | 402 |
| en (phrases) | 145 | 65 | 210 |
| REL (cibles) | 57 | **17** | 74 |
| SUB (cibles) | 45 | 24 | 69 |
| GP (cibles) | 61 | 35 | 96 |

**Aucune catégorie demandée n'est absente d'une moitié** : les trois sources, les deux langues et les
trois types de cibles sont présents des deux côtés. Le χ² d'homogénéité du test canonique contre
l'ensemble ne rejette rien : sources χ²=0,93 (p=0,63), langues χ²=0,0009 (p=0,98), types de cibles
χ²=2,66 (p=0,26), types×langues χ²=3,49 (p=0,63) ; les splits décalés donnent des p entre 0,42 et 0,97.
L'équilibre tient donc **en espérance**, pas par construction : le hash n'est **pas stratifié**, il est
vérifié a posteriori.

Quatre réserves de lecture, même sans catégorie absente :

- **`hand` est mince** : 5 phrases au test (4 au décalé 2, 11 au décalé 1), et **3 cibles seulement**,
  **toutes GP**. `hand/REL` (1 cible) et `hand/SUB` (2 cibles) sont entièrement dans dev. Les taux
  `hand` du test ne disent donc rien des REL/SUB.
- **REL/en est la cellule la plus mince** : 5 cibles au test (2 labels), contre 23 en dev. Toute
  conclusion sur l'anglais REL au test est fragile.
- **Le mélange des types varie** : le test canonique est **REL-pauvre** (17 cibles, 22,4 %, contre
  35,0 % en dev) et **GP-riche** (35, 46,1 %, contre 37,4 %) ; l'attendu serait 23,5 REL et 30,5 GP.
  Ce n'est pas significatif (p=0,26), mais les décalés ne donnent pas le même mélange : test REL 34,8 %
  (décalé 1) et 35,1 % (décalé 2). C'est le principal levier des variations agrégées ci-dessous.
- **Le synthétique est français seulement** (160 phrases) : source et langue y sont confondues ; ce
  n'est pas un défaut du split, mais une propriété du corpus.

## 4. La stabilité : trois découpages

| split | règle test | dev phrases | dev cibles | dev labels | dev exact | test phrases | test cibles | test labels | test exact |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| canonique | `%3==0` | 422 | 163 | 134 | 133 | 190 | 76 | 62 | 62 |
| décalé 1 | `%3==1` | 383 | 150 | 120 | 119 | 229 | 89 | 76 | 76 |
| décalé 2 | `%3==2` | 419 | 165 | 138 | 138 | 193 | 74 | 58 | 57 |

| split | dev couv. | dev F1 | dev tête | dev POS | test couv. | test F1 | test tête | test POS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| canonique | 0,8221 | 0,5512 | 0,7132 | 0,7547 | 0,8158 | 0,5651 | 0,7196 | 0,7656 |
| décalé 1 | 0,8000 | 0,5529 | 0,7135 | 0,7602 | 0,8539 | 0,5598 | 0,7180 | 0,7545 |
| décalé 2 | 0,8364 | 0,5622 | 0,7187 | 0,7596 | 0,7838 | 0,5410 | 0,7076 | 0,7549 |
| **étendue dev** | 0,0364 | 0,0110 | 0,0055 | 0,0055 | — | — | — | — |
| **étendue test** | — | — | — | — | **0,0701** | **0,0241** | **0,0120** | **0,0111** |

**L'écart demandé** : sur l'exact, l'étendue est de **1 cas** (dev 0,0083 ; test 0,0172) ; sur la
couverture, de **3 spans** (test 14/13/16 perdus sur 43) ; sur la F1, de **2,4 points** ; sur la tête,
de **1,2 point** ; sur la POS, de **1,1 point**. Les taux restent proches ; la couverture est la seule
mesure dont l'étendue relative (7,0 points) paraît grande, et elle s'explique :

- **Les issues sont fixes par phrase.** Le split ne change pas le modèle : il répartit 612 analyses
  identiques. L'exact global reste **195/196** et les spans perdus **43** quel que soit le découpage.
- **L'exact ne bouge que d'un cas** : l'unique échec est **r102** (GP/en, « since this morning »,
  cible gold `falls`, attachement prédit vide), dans le **seau 2**. Il est donc dans dev pour les
  splits 0 et 1, et dans test pour le split 2 — d'où 62/62, 62/62, 57/58.
- **La couverture est hypergéométrique** : les 43 spans perdus se répartissent 14/13/16 dans les trois
  tests, pour des attendus de 13,67/16,01/13,31 (z = 0,12 / −1,05 / +0,98). La dispersion de 7 points
  vient des dénominateurs (76/89/74 cibles) et du mélange REL/GP, pas d'une instabilité du modèle.
- **Un split aléatoire reproduit la même dispersion.** 2 000 partitions aléatoires aux tailles réelles
  190/229/193 (mêmes phrases, mêmes annotations) donnent, pour l'étendue des trois seaux :

| mesure | étendue observée | MC p05 | MC médiane | MC p95 |
|---|---:|---:|---:|---:|
| exact | 0,0172 | 0,0125 | 0,0152 | 0,0185 |
| couverture | 0,0701 | 0,0195 | 0,0678 | 0,1445 |
| F1 | 0,0241 | 0,0100 | 0,0361 | 0,0772 |
| tête | 0,0120 | 0,0072 | 0,0260 | 0,0555 |
| POS | 0,0111 | 0,0052 | 0,0182 | 0,0386 |

Toutes les étendues observées sont dans la bande 95 % du tirage aléatoire. **Conclusion : le split est
stable ; les variations sont du bruit de partition et de la composition, pas une fragilité du modèle.**

## 5. Dev contre test : l'écart

- **Exact** : dev **133/134**, test **62/62** → **1 échec contre 0**, soit **0,75 point** et **1 cas**.
  C'est **< 2 cas** : pas d'alerte. L'écart n'est pas un effet dev/test : c'est **r102**, une phrase
  fixe, qui tombe dans dev (seau 2) au split canonique. Au décalé 2, r102 est dans test (57/58) et
  dev est à 138/138 : le même écart s'inverse mécaniquement.
- **Couverture** : 0,8221 (dev) contre 0,8158 (test), soit **0,63 point** — environ **0,5 cas** pour
  76 cibles. Après standardisation sur la composition du dev, le test serait à **0,7870** (3,5 points
  sous dev, ~2,7 cas pour 76), mais l'incertitude est grande : les IC Wilson 95 % des composantes se
  recouvrent (REL test [0,413 ; 0,827] contre dev [0,610 ; 0,834] ; GP test [0,776 ; 0,970] contre dev
  [0,888 ; 0,991]). Autrement dit, le test **paraît** aussi couvrant que dev surtout parce qu'il a plus
  de GP (faciles) et moins de REL (difficiles). C'est le point à surveiller, pas un écart acquis.
- **F1** : test **+1,39 point**, mais l'agrégat est dominé par GN/GV (82,7 % des segments gold) : GV test
  0,6061 contre dev 0,5720, GN test 0,4751 contre dev 0,4827. Sur les cibles REL/SUB/GP, le test est
  **plus bas** : REL 0,5500 contre 0,6176 (−6,8 pts), SUB 0,7600 contre 0,7727 (−1,3), GP 0,8095
  contre 0,8497 (−4,0). La F1 globale ne mesure donc pas la généralisation de l'attachement ; elle
  mesure surtout la segmentation GN/GV.
- **Tête** : test **+0,64 point**, mélangé : REL +4,3, SUB +3,0, GP −0,7 ; fr +1,5, en −0,9.
- **POS** : test **+1,09 point**, porté par l'anglais (+4,0) alors que le français recule de 0,5.

**Continuité v5 → v7.** La fiche d'origine mesurait dev 104/106 et test 53/54 avec 160 labels ; la v5
est passée à 187 labels (dev 125/126 puis 126/126 selon le commit, test 60/61) ; la v7 est à 196 labels
(dev 133/134, test 62/62). Au dernier état v5 (`b975011b`), l'unique échec était **r309**, dans le
**seau 0** (donc test), d'où 60/61 au test et 126/126 en dev. En v7, **r309 est corrigé** et **r102**
apparaît (seau 2, donc dev) : l'écart dev/test s'inverse parce que l'échec unique change de phrase et de
seau, **pas parce que le test progresse plus vite**. Le solde est +9 labels et +9 exacts, mais il cache
21 labels gagnés (20 exacts, r102 faux) et 12 perdus (tous exacts).

## 6. Le contrôle négatif

Le contrôle est un **split aléatoire** de même taille, à annotations identiques : si le découpage
fabriquait un signal, les étendues observées sortiraient de la bande Monte-Carlo. Elles n'en sortent
pas (tableau § 4). Deux contrôles indépendants confirment :

- le taux exact change de **1 cas** exactement quand r102 change de seau, et pas autrement ;
- les 43 spans perdus se répartissent selon l'hypergéométrie (14/13/16, z ≤ 1,05), et l'union des
  moitiés redonne toujours 195/196 et 43 spans.

## 7. Ce que ce banc ne dit pas

- **Le split n'est pas un vrai held-out** : les règles v7 ont été dessinées en regardant tout le gold,
  test compris. Le split détecte une **fragilité au découpage**, pas le **surajustement global** ; les
  deux moitiés peuvent être surajustées ensemble.
- **Petit échantillon** : 62 labels au test canonique, 1 cas = 1,6 point ; REL/en = 5 cibles ;
  `hand` = 3 cibles au test. Les IC Wilson sont larges.
- **Le hash n'est pas stratifié** : seaux 190/229/193 phrases (χ²=4,62, p=0,099) ; les taux doivent
  être lus avec leur dénominateur, et le mélange des types change d'un seau à l'autre.
- **L'exact/labels exclut les 43 spans perdus** : il ne dit rien de la couverture, qui est mesurée à
  part (196/239). Un span perdu n'est ni un vrai ni un faux dans l'exact.
- **Vivant vs gelé** : F1/tête/POS diffèrent de la fiche v7 (0,5555/0,7152/0,7581 contre
  0,5595/0,7205/0,7603) ; l'exact et la couverture sont identiques.
- **Un seul lecteur** : l'heuristique. La cascade, le mock neuronal et le modèle réel ne sont pas
  mesurés ici.

## 8. La suite

1. **Garder la règle** : régler sur dev, n'accepter que si test ne baisse pas — mais lire aussi la
   **couverture par type**, car l'agrégat est sensible à la composition.
2. **Les 43 spans** : REL 21, SUB 17, GP 5 ; les prochains gains sont REL/en et SUB/en (13 perdus
   chacun), pas les GP.
3. **Si un split plus fin est souhaité**, stratifier le hash par source, langue et type (ou publier
   systématiquement le par-type) ; changer le split maintenant casserait la comparaison avec la v5.
4. **Re-mesurer après la prochaine règle** : c'est le seul moyen de savoir si le gain est un gain.

## 9. Fichiers

- [`gold_split.py`](../tools/tests/linguistique/gold_split.py) — le split (`dev`, `test`, `compter`).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `charger`, `evaluer_bloc`.
- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — l'heuristique mesurée.
- [`pensee-dev-test-v7.json`](pensee-dev-test-v7.json) — les trois splits, l'équilibre, les contrôles
  (χ², hypergéométrie, Wilson, Monte-Carlo), la comparaison v5 → v7.
- [`rapport-gold-split.md`](rapport-gold-split.md) — la fiche d'origine (160 labels).
- [`rapport-pensee-couverture-v7.md`](rapport-pensee-couverture-v7.md) — la fiche v7 (gelé 602).
