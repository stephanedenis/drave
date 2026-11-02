# B13 — les phrases complexes : POS 0,6471, syntagme 0,4828

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **90/90 portes** : cinq phrases **complexes** (REL `qui parle`, SUB `que tu as raison`) sont
> ajoutées au gold réel (r201–r205). Le **POS chute** (0,6471 contre 0,7924) mais le
> **syntagme bondit** (F1 0,4828 contre 0,1838) : les segments REL/SUB sont longs et
> l'heuristique les attrape mieux que les GN courts.
>
> **Dispositif** : [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-gold-complexes.json`](pensee-gold-complexes.json).

## 1. Les phrases complexes

| sous-ensemble | phrases | POS | tokens | syntagme F1 | tête F1 |
|---|---:|---:|---:|---:|---:|
| r001–r200 | 200 | 0,7924 | 978 | 0,1838 | 0,3198 |
| **r201–r205** | **5** | **0,6471** | 34 | **0,4828** | **0,5517** |

**Ce que ça dit** :

- **Le POS chute** (−0,145) : les pronoms relatifs (`qui`, `que`, `who`), les auxiliaires
  (`as`, `ai`, `are`) et les conjonctions (`that`) ne sont pas dans le lexique fermé ; le POS
  ouvert (verbe/nom) les absorbe.
- **Le syntagme bondit** (+0,30) : les REL/SUB sont des **segments longs** (4–5 mots) que
  l'heuristique segmente bien ; les GN courts des phrases simples sont plus souvent coupés.
- **La tête suit** (0,5517) : le rôle des REL/SUB est porté par le nom/verbe de tête.
- **La négative reste** : le POS du hasard (0,0147).

## 2. Ce que ce banc ne dit pas

- **5 phrases** (34 tokens) : l'intervalle est très large (±0,15).
- **Le registre** ; il faudrait 20–50 phrases complexes.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 380** (205 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le nombre de phrases** (5 : un seul cas peut renverser le syntagme) ;
- **les étiquettes** (REL/SUB à la main) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **20 phrases complexes** : REL/SUB, coordination ; l'intervalle se resserre.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `PHRASES` (205).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `evaluer_bloc`.
- [`autotest.py`](../tools/pensee/autotest.py) — T87, 90/90.
- [`pensee-gold-complexes.json`](pensee-gold-complexes.json) — le bilan.
