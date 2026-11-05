# B13 — le verbe du GV-phrase : l'exact passe de 0,0586 à 0,0962

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **167/167 portes** : quand le générateur S produit un GV qui couvre **toute la phrase**
> (`The boy saw the cat in the park`), la règle « dernier token » prenait `park` au lieu de `saw`.
> Le bloc prend désormais le **premier token étiqueté `VERB`** à l'intérieur du GV. Sur le gold
> de T153 (612 phrases, 239 cibles) : **exact 14 → 23 (0,0586 → 0,0962)**, top1 **96 → 105**
> (0,4393), top-k **113 → 122** (0,5105), tête **0,7241 / 0,8414**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_verbe_dans`),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-verbe-gv.json`](pensee-verbe-gv.json).

## 1. Avant / après (même gold, 239 cibles)

| mesure | avant | **verbe du GV** | écart |
|---|---:|---:|---:|
| top1 | 96 (0,4017) | **105 (0,4393)** | +9 |
| top-k | 113 (0,4728) | **122 (0,5105)** | +9 |
| **exact** | 14 (0,0586) | **23 (0,0962)** | **+9 (×1,6)** |
| tête top1 | 96 (0,6621) | **105 (0,7241)** | +9 |
| tête top-k | 113 (0,7793) | **122 (0,8414)** | +9 |

## 2. Les échecs après le correctif

| cause | avant | **après** |
|---|---:|---:|
| span faux | 94 | 94 |
| cible hors des candidats | 32 | **23** |
| **tout** | **126** | **117** |

Les 23 restants sont **22 GP et 1 SUB** ; ils ont un GV qui contient bien un verbe, mais le POS
tague ce verbe en `NOUN` (`play`, `talks`, `leaves`, `writes`, `barks`…) — la règle tombe alors
sur le dernier token (`park`, `brother`, `noon`).

**Ce que ça dit** :

- **Le verbe est dans le GV, pas à sa fin** : +9 exact d'un coup, sans toucher à la segmentation.
- **Le POS est le bon oracle** quand il tague juste (`saw`, `joue`, `vu`) ; il devient la limite
  quand il hésite sur les classes ouvertes (verbe/nom en anglais).
- **La négative est explicite** : 23/239 restent faux, dont 22 GP à cause du POS.

## 3. Ce que ce banc ne dit pas

- **Les 94 spans** : inchangés, non qualifiés (S ou chunker).
- **Le POS anglais** : la confusion verbe/nom n'est pas mesurée séparément.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.
- **Le coût** : le POS est déjà calculé, aucun appel de modèle en plus.

## 4. Ce qui pourrait rendre cette fiche fausse

- **le POS** est une heuristique de classe ouverte : le premier `VERB` du GV peut être un nom ;
- **le choix du GV** reste la proximité (les passifs l'inversent) ;
- **le gold** : 612 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 5. La suite

1. **Le POS verbe/nom en anglais** : la cause des 22 GP restants.
2. **Les 94 spans** : qualifier la segmentation.
3. **Le générateur S** : les passifs.
4. **Politique DRVM/native** : quand les poids seront là.

## 6. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `_verbe_dans`, `_cible_proche`.
- [`autotest.py`](../tools/pensee/autotest.py) — T164, 167/167.
- [`pensee-verbe-gv.json`](pensee-verbe-gv.json) — avant/après.
