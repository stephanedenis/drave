# B13 — le gold complet : 522 phrases, POS 0,7586

> **Note (post-372)** : après l'ajout des 30 phrases d'anaphore, le gold complet est à
> **552 phrases**, POS **0,7574**, tête **0,3704** ; le seuil `syntagme_reel` est passé à 0,18.
>
> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **110/110 portes** : le gold est évalué **en entier** pour la première fois depuis l'ajout des
> 22 dernières phrases : **522 phrases** (**342 réels** + 160 synthétiques + 20 de `gold.py`),
> **2 676 tokens**. POS **0,7586** (fermé 0,8974, ouvert 0,6243), syntagme F1 **0,1963**,
> tête **0,3807**, pragmatique **0,9962 / 1,0 / 0,9866 / 0,9406**. **Tous les verdicts passent.**
>
> **Dispositif** : [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-gold-342.json`](pensee-gold-342.json).

## 1. Le gold complet

| mesure | 320 phrases (T91) | **522 phrases** | delta |
|---|---:|---:|---:|
| POS (all) | 0,7544 | **0,7586** | +0,0042 |
| POS fermé | 0,8974 | 0,8974 | 0 |
| POS ouvert | 0,6145 | 0,6243 | +0,0098 |
| syntagme F1 | 0,2074 | 0,1963 | −0,0111 |
| tête F1 | 0,3954 | 0,3807 | −0,0147 |
| acte | 0,996 | 0,9962 | +0,0002 |

**Ce que ça dit** :

- **Le POS est stable** (+0,004) : les 22 phrases ajoutées (discours, anaphore, pièges) ne
  changent pas la tendance.
- **La tête baisse** (−0,015) : les pièges d'anaphore ont des GN courts, plus durs à segmenter.
- **Tous les verdicts passent** : `pos_hand`, `pos_reel`, `pos_synthetique`, `syntagme_*`,
  `tete` (seuil 0,35), `acte`, `cascade`, `attachement` — aucun échec.
- **La négative reste** : le POS du hasard (0,0147) est 50 fois plus bas.

## 2. Ce que ce banc ne dit pas

- **522 phrases** ; 1 000 resserreraient les intervalles.
- **Le gold réel (342)** est le sous-ensemble qui compte ; le synthétique dilue.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 522** est un jouet à l'échelle des corpus.

## 3. Ce qui pourrait rendre cette fiche fausse

- **les étiquettes des 22 dernières** (à la main) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- **le seuil tête** (0,35 depuis T91) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Les 100 liens de coréférence** : resserrer la CV.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — 342 réels.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — l'évaluation complète.
- [`autotest.py`](../tools/pensee/autotest.py) — T107, 110/110.
- [`pensee-gold-342.json`](pensee-gold-342.json) — le bilan.
