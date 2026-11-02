# B13 — les sous-ensembles du gold : POS 0,8214 sur les 20 nouvelles

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **89/89 portes** : le gold réel de 200 phrases est scindé en deux sous-ensembles. Les **20
> nouvelles** (r181–r200) ont un **meilleur POS** (**0,8214**) que les **180 anciennes**
> (**0,7897**) — mais un **syntagme plus faible** (F1 0,1053 contre 0,1916) : le POS simple
> monte, la segmentation des GV à ADV baisse.
>
> **Dispositif** : [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-gold-subsets.json`](pensee-gold-subsets.json).

## 1. Les deux sous-ensembles

| sous-ensemble | phrases | POS | tokens | syntagme F1 | tête F1 |
|---|---:|---:|---:|---:|---:|
| r001–r180 | 180 | 0,7897 | 894 | 0,1916 | 0,3255 |
| **r181–r200** | **20** | **0,8214** | 84 | 0,1053 | 0,2632 |

**Ce que ça dit** :

- **Le POS des nouvelles est meilleur** (+0,0317) : les phrases sont plus régulières (SVQ simple,
  GN/GV/GN), le POS fermé y domine.
- **Le syntagme des nouvelles est plus faible** (−0,0863) : les GV à ADV (`souffle fort`,
  `roule vite`) et les GP (`à midi`, `sur le toit`) sont mal délimités par l'heuristique.
- **Le sous-ensemble est petit** (84 tokens) : ±0,04 d'intervalle à 95 %.
- **La négative reste** : le POS du hasard (0,0147) sur le même gold.

## 2. Ce que ce banc ne dit pas

- **20 phrases** ; 100 nouvelles stabiliseraient la comparaison.
- **Le registre** ; les phrases complexes (REL/SUB) manquent.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 380** (200 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **les étiquettes des 20 nouvelles** (à la main) ;
- **le JSON régénéré** (le `gold_reel.json` doit suivre `gold_reel.py`) ;
- **la taille du sous-ensemble** (84 tokens : l'intervalle est large) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Des phrases complexes** : REL, SUB ; le POS ouvert doit progresser.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `PHRASES` (200).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `evaluer_bloc`.
- [`autotest.py`](../tools/pensee/autotest.py) — T86, 89/89.
- [`pensee-gold-subsets.json`](pensee-gold-subsets.json) — les deux sous-ensembles.
