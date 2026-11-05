# B13 — le lexique verbal : l'exact passe de 0,0962 à 0,1381

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **168/168 portes** : le POS de surface se trompe sur les classes ouvertes anglaises
> (`talks` → `NOUN`, `brother` → `VERB`). Un **lexique verbal bilingue** (≈ 200 formes, avec
> désinences) arbitre : le verbe est le premier mot du GV qui appartient au lexique, sinon le
> premier `VERB` du POS, sinon le dernier mot. Sur le gold de T153 (612 phrases, 239 cibles) :
> **exact 23 → 33 (0,1381)**, top1 **115 (0,4812)**, top-k **132 (0,5523)**, tête **0,7862 /
> 0,9034**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`VERBES_CONNUS`,
> `_est_verbe`), [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-lexique-verbal.json`](pensee-lexique-verbal.json).

## 1. Avant / après (même gold, 239 cibles)

| mesure | avant | **lexique verbal** | écart |
|---|---:|---:|---:|
| top1 | 105 (0,4393) | **115 (0,4812)** | +10 |
| top-k | 122 (0,5105) | **132 (0,5523)** | +10 |
| **exact** | 23 (0,0962) | **33 (0,1381)** | **+10** |
| tête top1 | 105 (0,7241) | **114 (0,7862)** | +9 |
| tête top-k | 122 (0,8414) | **131 (0,9034)** | +9 |

| cause d'échec | avant | **après** |
|---|---:|---:|
| span faux | 94 | 94 |
| cible hors des candidats | 23 | **13** |
| **tout** | **117** | **107** |

## 2. Ce que ça dit

- **Le POS de surface n'est pas fiable sur les classes ouvertes** : mesuré, `She talks to her
  brother` donne `talks` NOUN et `brother` VERB — la règle du premier `VERB` prenait `brother`.
- **Le lexique arbitre** : `talks` y est, `brother` n'y est pas → la cible devient `talks`.
- **Le exact gagne 10 points** (23 → 33) et la tête atteint **90,3 % en top-k** : la bonne cible
  est dans la liste 9 fois sur 10 quand le span est bon.
- **La négative est explicite** : 13 cibles restent fausses, toutes des verbes **hors lexique**
  (`fly`, `climbs`, `flows`, `wait`, `swims`, `passes`, `get`, `smiles`).

## 3. Ce que ce banc ne dit pas

- **Les 13 verbes manquants** : je ne les ai **pas** ajoutés — ce serait ajuster le lexique au
  gold (fuite de test). Ils restent la mesure de la couverture du lexique.
- **Les 94 spans** : inchangés.
- **Le lexique** est petit (≈ 200 formes) ; sa couverture réelle n'est pas mesurée hors gold.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 4. Ce qui pourrait rendre cette fiche fausse

- **le lexique** est écrit à la main : il peut avantager les phrases du gold qu'il connaît ;
- **les désinences** (`-s`, `-ed`, `-ing`, `-e`, `-ent`…) peuvent faire entrer des noms ;
- **le gold** : 612 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 5. La suite

1. **Les 13 verbes** : les mesurer comme couverture du lexique, sans les y ajouter.
2. **Les 94 spans** : qualifier la segmentation.
3. **Le générateur S** : les passifs.
4. **Politique DRVM/native** : quand les poids seront là.

## 6. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `VERBES_CONNUS`, `_est_verbe`.
- [`autotest.py`](../tools/pensee/autotest.py) — T165, 168/168.
- [`pensee-lexique-verbal.json`](pensee-lexique-verbal.json) — avant/après.
