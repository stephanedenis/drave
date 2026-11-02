# B13 — la cascade avec l'union : F1 0,2170, tête 0,4410, 1 601 appels

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **117/117 portes** : la **cascade** (heuristique + mock neuronal) est mesurée avec l'union :
> **syntagme F1 0,2170** (heuristique seule : 0,2005), **tête 0,4410** (heuristique : 0,4662),
> **587 appels neuronaux** pour une évaluation du gold complet (**1 601** pour les 5 sources de
> l'évaluateur). La cascade **gagne en F1** (+0,0165) et **perd en tête** (−0,025).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-cascade-union.json`](pensee-cascade-union.json).

## 1. La cascade

| bloc | POS (all) | syntagme F1 | tête F1 | pragma (acte) |
|---|---:|---:|---:|---:|
| heuristique (union) | 0,7502 | 0,2005 | **0,4662** | 0,9966 |
| **cascade** | 0,7502 | **0,2170** | 0,4410 | 0,9966 |

| bloc | POS (réel) | syntagme F1 (réel) | tête F1 (réel) |
|---|---:|---:|---:|
| heuristique (union) | 0,7575 | 0,2095 | **0,4432** |
| **cascade** | 0,7575 | **0,2283** | 0,4081 |

**Ce que ça dit** :

- **La cascade gagne en F1** (+0,0165) : le mock neuronal ajoute des segments que l'heuristique
  rate ; le rappel monte.
- **Elle perd en tête** (−0,025) : ses segments supplémentaires ont de moins bonnes têtes que
  l'union.
- **Le coût est réel** : **587 appels neuronaux** pour 587 phrases (1 par phrase), **1 601**
  pour les 5 sources de l'évaluateur — la cascade n'est pas gratuite, et le mock est un
  **contrat**, pas un modèle.
- **Aucun verdict ne casse** : tous les seuils passent.

## 2. Ce que ce banc ne dit pas

- **Le mock** n'est pas un modèle : les 1 601 appels sont un coût de contrat, pas une inférence.
- **587 phrases** ; le réel donne les mêmes ordres.
- **Le neuronal réel reste bloqué** : c'est la limite de la cascade.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le mock** (les segments sont simulés) ;
- **le seuil tête** (0,35) et `syntagme_reel` (0,16) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le neuronal réel** : débloquer la cascade (modèle local / poids / cascade actée).
2. **La tête de la cascade** : garder la tête de l'union quand le mock ajoute un segment.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `Cascade`, `MockNeuronal`.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `evaluer_bloc`.
- [`autotest.py`](../tools/pensee/autotest.py) — T114, 117/117.
- [`pensee-cascade-union.json`](pensee-cascade-union.json) — la cascade.
