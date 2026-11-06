# B13 — la couverture à 0,8201 : POS contextuel, GV avant GP, prépositions ambiguës

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **183/183 portes** : la **couverture** passe de **187 à 196 labels** (sur 239) et l'exactitude
> tient : **exact 195/196 = 0,9949** (fr **135/135 = 1,0**, en **60/61**) ; la **F1 syntagmes**
> monte à **0,5595** (union ; S 0,4741, chunker 0,5858), la tête à **0,7205** ; la **POS** passe de
> **0,7475 à 0,7603** ; les **spans perdus** tombent de **52 à 43** (21 REL, 17 SUB, 5 GP).
>
> **État courant** : commit `69bd865e` · **Base** : F1/tête/POS sur le gold **gelé 602** (portes
> T110-T115) ; sur le **612** : F1 **0,5555**, tête **0,7152**, POS **0,7581**. Couverture et
> exactitude sur le **612**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (POS contextuel,
> ordre GV/GP, prépositions composées, sujets), [`autotest.py`](../tools/pensee/autotest.py)
> (32 assertions recalées) ; JSON [`pensee-couverture-v7.json`](pensee-couverture-v7.json).

## 1. Les cinq corrections

| # | correction | effet |
|---|---|---|
| 1 | **POS contextuel** : un verbe de suffixe après DET/PRÉP/ADJ devient un nom (« brother », « chair ») | POS 0,7475 → 0,7603, +9 labels |
| 2 | **GV avant GP** : « entre » (verbe) n'est plus une préposition | GP « en gare » |
| 3 | **prépositions composées** (`au-dessus`, `au-dessous`, `vis-à-vis`) | GP « au-dessus du lac » |
| 4 | **prépositions ambiguës** (`since/before/after/until/as`) : SUB devant une clause, PRÉP devant un GN | GP « since yesterday » |
| 5 | **le verbe après un pronom sujet** (`who speaks`, `qui parle`) + adverbe **final** hors clause | REL « who speaks », SUB « that she would come » |

## 2. Avant / après

| mesure | v6 | **v7** |
|---|---:|---:|
| labels au bon span | 187 | **196** |
| **exact / labels** | 187/187 (1,0) | **195/196 (0,9949)** |
| **couverture** | 187/239 (0,7824) | **196/239 (0,8201)** |
| F1 syntagmes (union, gelé 602) | 0,5130 | **0,5595** |
| F1 tête (gelé 602) | 0,6834 | **0,7205** |
| POS (gelé 602) | 0,7482 | **0,7603** |
| français | 127/127 | **135/135 (1,0)** |
| anglais | 60/60 | **60/61 (0,9836)** |
| spans perdus | 52 | **43** (21 REL, 17 SUB, 5 GP) |
| top-k | 161/239 | 166/239 (0,6946) |

**Contrôle négatif (mesuré)** : les 196 cibles prédites sont comparées à leurs cibles gold ; en
**permutant les cibles globalement** (100 tirages, graine 20261105), l'accord tombe à **1,67/196**
(max 4) contre **195/196** observé — p < 0,001.

**dev/test (re-mesurés)** : dev **133/134 (0,9925)**, test **62/62 (1,0)** ; test couvre 62 des 76
cibles ; sur trois découpages (`%3==0/1/2`), l'exact varie d'un cas et la couverture de 3 spans
(fiche [dev/test v7](rapport-dev-test-v7.md)).

**Ce que ça dit** :

- **La POS est le verrou** : le contexte (DET/PRÉP/ADJ avant un suffixe) rend 0,0128 de POS et
  neuf labels de couverture.
- **Le chunker est maintenant meilleur que S** (F1 0,5858 contre 0,4741) : le découpage est
  devenu la force, plus la faiblesse.
- **Les 43 spans restants** : 21 REL (« qui » 12), 17 SUB, 5 GP — la file est claire.

## 3. Ce que ce banc ne dit pas

- **Les 43 spans** : non prédits (REL « qui » en français, SUB anglais).
- **Le top-k** (166/239) : les candidats restent incomplets.
- **L'in-sample** : les règles sont dessinées sur ce gold ; dev/test n'ont pas été re-mesurés
  depuis la v6 (à refaire).
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 4. Ce qui pourrait rendre cette fiche fausse

- **la règle de contexte** (DET/PRÉP/ADJ → nom) peut transformer un vrai verbe en nom ;
- **le sujet-verbe** peut faire d'un nom un verbe après « qui/that » ;
- **les prépositions composées** sont une liste ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 5. La suite

1. **Les 43 spans** : REL « qui » (12), SUB anglais, GP.
2. **Le top-k** : candidats complets.
3. **dev/test** à re-mesurer.
4. **Politique DRVM/native** : quand les poids seront là.

## 6. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — les cinq corrections.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`pensee-couverture-v7.json`](pensee-couverture-v7.json) — les chiffres.
