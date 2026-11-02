# B13 — le gold à 200 phrases réelles : POS 0,7738

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **88/88 portes** : le gold réel passe de **180 à 200 phrases** (r181–r200, 10 françaises et 10
> anglaises, écrites à la main). Le POS global gagne **+0,0023** (0,7715 → **0,7738**), sur
> **1 782 tokens** : la cible « 200 phrases réelles » est **atteinte**.
>
> **Dispositif** : [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-gold-200.json`](pensee-gold-200.json).

## 1. Le gold à 200 réels

| mesure | 180 réels (T?) | **200 réels** | delta |
|---|---:|---:|---:|
| tokens | 1 698 | **1 782** | +84 |
| POS (all) | 0,7715 | **0,7738** | +0,0023 |
| syntagme F1 | 0,1988 | 0,1941 | −0,0047 |
| pragmatique (acte) | 1,0 | 1,0 | 0 |
| tête (F1) | 0,4359 | 0,4274 | −0,0085 |

**Ce que ça dit** :

- **La cible est atteinte** : 200 phrases réelles (180 + 20), la ligne B13 tient sa promesse
  « 200 réels ».
- **Le POS est stable** (+0,0023) : les 20 nouvelles phrases sont du même registre (SVQ simple,
  GN/GV/GP) ; elles ne changent pas la tendance.
- **Le syntagme recule un peu** (−0,005) : les 20 nouvelles ont des GV à ADV (`souffle fort`,
  `roule vite`) que l'heuristique segmente mal.
- **La négative reste** : le POS du hasard (0,0147) est toujours 50 fois plus bas.

## 2. Ce que ce banc ne dit pas

- **20 phrases** ; le gold peut encore grandir (500 ?).
- **Le registre est simple** ; des phrases complexes (REL, SUB) testeraient mieux.
- **L'heuristique** ; le neuronal réel reste bloqué (pas de tagger, pas de poids).
- **Le gold 380** (200 réels + 160 synthétiques + 20 de `gold.py`) est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- **les étiquettes des 20 nouvelles** (écrites à la main ; une erreur d'étiquette fausse la
  mesure) ;
- **le JSON régénéré** (`gold_reel.json` doit être reconstruit après toute édition) ;
- **l'évaluation** (le `all` inclut le synthétique, pas seulement le réel) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Des phrases complexes** : REL, SUB, coordination ; le POS ouvert doit progresser.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `PHRASES` (200).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — l'évaluation.
- [`autotest.py`](../tools/pensee/autotest.py) — T85, 88/88.
- [`pensee-gold-200.json`](pensee-gold-200.json) — le bilan.
