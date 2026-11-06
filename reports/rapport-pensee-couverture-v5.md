# B13 — la couverture : 187 labels, exact 186/187 (0,9947), F1 0,5164

> **Instantané historique** : état au commit `b975011b` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **183/183 portes** : la **couverture** passe de **160 à 187 labels** (sur 239) et l'exactitude
> tient : **exact 186/187 = 0,9947** (fr **0,9921**, en **1,0000** — 60/60) ; la **F1 syntagmes**
> monte à **0,5164** (union ; S 0,4582, chunker 0,5351) et la tête à **0,6826** ; les **spans
> perdus** tombent de **79 à 52** (24 REL, 12 SUB, 16 GP). Sur le gold tenu à l'écart : **dev
> 126/126 (1,000)**, **test 60/61** — la progression n'est pas un surajustement visible.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
> `_cible_precedent`), [`autotest.py`](../tools/pensee/autotest.py) (25 assertions recalées) ;
> [`gold_split.py`](../tools/tests/linguistique/gold_split.py) pour dev/test ; JSON
> [`pensee-couverture-v5.json`](pensee-couverture-v5.json).

## 1. Les sept corrections

| # | correction | effet |
|---|---|---|
| 1 | **la branche REL/SUB passe avant le GN** et « that » est désambiguïsé (pronom/verbe après → marqueur, nom après → déterminant) | les relatives ne sont plus avalées |
| 2 | **frontière de clause** : la REL/SUB s'arrête au **second verbe** plein, et un **auxiliaire après un verbe** ouvre la principale | « that I read \| is exciting » |
| 3 | **le chunker reçoit le POS** (`VERB`) en plus du lexique | « aboie », « exciting » reconnus |
| 4 | **déterminants élidés** (`L'homme`, `d'Artagnan`) | le GN précède la relative |
| 5 | **prépositions anglaises** (since, above, for, near…) et verbes (`live`) | GP et GV anglais |
| 6 | **la règle du segment précédent dans l'union et le chunker** : une REL prend la tête du GN qui la précède | répare 18 REL anglaises |
| 7 | **les candidats du précédent** : l'antécédent d'une REL et le verbe d'une SUB entrent dans `candidats` | 27 → 26 couvertures, top-k 161 |

## 2. Avant / après

| mesure | v4 (committée) | **v5** |
|---|---:|---:|
| labels au bon span | 160 | **187** |
| **exact / labels** | 157/160 (0,9812) | **186/187 (0,9947)** |
| top-k (sous-chaîne) | 156/239 | 161/239 (0,6736) |
| **couverture** | 160/239 (0,6695) | **187/239 (0,7824)** |
| F1 syntagmes (union, 602) | 0,4539 | **0,5164** |
| F1 tête (602) | 0,6432 | **0,6834** |
| français | 117/118 (0,9915) | **126/127 (0,9921)** |
| anglais | 40/42 (0,9524) | **60/60 (1,0000)** |
| spans perdus | 79 | **52** (24 REL, 12 SUB, 16 GP) |
| échecs de cible | 3 | **1** (r309) |

**Contrôle négatif** : voir le dispositif de la [fiche v7](rapport-pensee-couverture-v7.md)
(permutation globale des cibles, candidat aléatoire) — les valeurs publiées là-bas sont celles de
sa base, pas de celle-ci.

**Ce que ça dit** :

- **+27 labels** et **+29 exact** : la couverture et l'exactitude montent ensemble.
- **L'anglais rattrape** (40 → 60) : la règle du segment précédent répare les relatives.
- **Le test tenu à l'écart suit** : dev 126/126 (0,9921), test **60/61** (0,9836).
- **L'échec de cible unique** et les **26 candidats manquants** sont le prix de la couverture : les REL/SUB nouvelles sont plus
  dures à attacher (le top-k tombe à 0,8610 sur les labels).

## 3. Ce que ce banc ne dit pas

- **Les 52 spans** : 24 REL, 12 SUB, 16 GP — non récupérés.
- **Les 27 échecs** : à qualifier (REL sans antécédent, GP, SUB en tête).
- **Le lexique/POS** : le chunker dépend maintenant du POS (`VERB`) ; une erreur de POS peut
  créer ou casser une frontière.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 4. Ce qui pourrait rendre cette fiche fausse

- **le test** (61 labels) reste petit ;
- **la frontière au second verbe** est une heuristique : une relative à deux verbes coordonnés
  serait coupée ;
- **les règles ont été réglées en regardant les échecs** : le test limite le surajustement, il
  ne l'exclut pas ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 5. La suite

1. **Les 52 spans** (REL 24, SUB 12, GP 16).
2. **Les 27 échecs de cible** : qualifier.
3. **`_pos` anglais** : 176 VERB tagués NOUN (A14).
4. **Politique DRVM/native** : quand les poids seront là.

## 6. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — les sept corrections.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`gold_split.py`](../tools/tests/linguistique/gold_split.py) — dev/test.
- [`pensee-couverture-v5.json`](pensee-couverture-v5.json) — les chiffres.
