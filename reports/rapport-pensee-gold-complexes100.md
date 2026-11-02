# B13 — les 100 phrases complexes : POS 0,6984, syntagme 0,2677

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **93/93 portes** : les phrases complexes passent de **50 à 100** (r201–r300, 50 FR + 50 EN :
> REL/SUB, coordination `et/and`, ellipse). Sur **630 tokens**, le **POS est 0,6984** (−0,094
> contre les 200 phrases simples) et le **syntagme 0,2677** (+0,084). Le POS est **stable**
> autour de 0,70 ; le gain de syntagme se **réduit** à +0,08.
>
> **Dispositif** : [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-gold-complexes100.json`](pensee-gold-complexes100.json).

## 1. Les 100 complexes

| sous-ensemble | phrases | POS | tokens | syntagme F1 | tête F1 |
|---|---:|---:|---:|---:|---:|
| r001–r200 | 200 | 0,7924 | 978 | 0,1838 | 0,3198 |
| **r201–r300** | **100** | **0,6984** | 630 | **0,2677** | **0,3494** |

**Ce que ça dit** :

- **Le POS est stable** (0,6984 ; 0,7013 à 50) : les relatifs, auxiliaires et conjonctions
  coûtent ~0,09 de POS, un point c'est tout.
- **Le syntagme se réduit** (+0,084 contre +0,122 à 50) : les 50 nouvelles (coordination,
  ellipse) ont des segments plus courts, que l'heuristique délimite moins bien.
- **La tête suit** (0,3494) : le rôle est porté par le nom/verbe de tête.
- **La négative reste** : le POS du hasard (0,0147).

## 2. Ce que ce banc ne dit pas

- **100 phrases** (630 tokens) : l'intervalle est ±0,035.
- **REL/SUB/coordination** ; le discours, l'anaphore, l'ellipse longue ne sont pas testés.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 480** (300 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **les étiquettes** (REL/SUB/coordination à la main) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- **la taille** (630 tokens) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le discours** : anaphore, connecteurs ; le niveau pragmatique.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `PHRASES` (300).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `evaluer_bloc`.
- [`autotest.py`](../tools/pensee/autotest.py) — T90, 93/93.
- [`pensee-gold-complexes100.json`](pensee-gold-complexes100.json) — le bilan.
