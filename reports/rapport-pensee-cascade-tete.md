# B13 — la tête de la cascade : la correction dégrade (0,419 contre 0,441)

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **118/118 portes** : la correction « garder la tête de l'union quand le mock ajoute un
> segment » est mesurée : **tête F1 0,419**, contre 0,441 pour la cascade seule et **0,466 pour
> l'heuristique seule**. La correction **dégrade** — elle remplace les bonnes têtes du chunker
> (dans le mock) par celles de l'union, moins bonnes sur ces segments.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-cascade-tete.json`](pensee-cascade-tete.json).

## 1. La tête de la cascade

| variante | précision | rappel | **tête F1** |
|---|---:|---:|---:|
| **heuristique (union)** | 0,5646 | **0,3971** | **0,4662** |
| cascade | 0,5960 | 0,3500 | 0,4410 |
| cascade + tête de l'union | 0,5676 | 0,3320 | 0,4190 |

**Ce que ça dit** :

- **La correction dégrade** (−0,022) : les têtes du chunker (dans le mock) sont meilleures que
  celles de l'union **sur les segments que le mock ajoute**.
- **L'heuristique seule reste la meilleure pour les têtes** (0,4662) : la cascade gagne en F1
  (0,2170) mais perd en tête.
- **Le compromis n'existe pas** : il faut choisir le F1 (cascade) ou la tête (union), pas les
  deux — à moins d'un modèle neuronal réel qui aurait les deux.
- **La négative est explicite** : 0,419 < 0,441.

## 2. Ce que ce banc ne dit pas

- **Le mock** : ses têtes viennent du chunker, pas d'un modèle.
- **587 phrases** ; le réel donne les mêmes ordres.
- **Le neuronal réel reste bloqué** : c'est la limite de la cascade.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le mock** (les segments simulés) ;
- **la correction** ne traite que les segments du mock, pas les siens propres ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le neuronal réel** : seul moyen d'avoir F1 et tête ensemble.
2. **La cascade par défaut** : F1 0,2170, tête 0,4410 — la garder comme mode « rappel ».
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `Cascade`, `_fusion`.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `_tete`.
- [`autotest.py`](../tools/pensee/autotest.py) — T115, 118/118.
- [`pensee-cascade-tete.json`](pensee-cascade-tete.json) — la comparaison.
