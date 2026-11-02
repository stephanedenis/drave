# B13 — les questions pièges : 0/5, la règle du `si` est cassée

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **132/132 portes** : cinq **questions pièges** (`Tu ne viens pas demain ?` avec la réponse
> attendue `non`, `You don't come tomorrow?` → `no`) entrent dans le gold (**422 phrases**,
> **34 questions**). La réponse dirigée tombe de **29/29 à 29/34 (0,8529)** : elle répond `si`
> là où il faut `non`. **Le `si` n'est pas l'accord, c'est une convention.**
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-pieges.json`](pensee-pieges.json).

## 1. Les 34 questions

| sous-ensemble | questions | **dirigée juste** |
|---|---:|---:|
| affirmatives | 19 | **19/19** |
| négatives (accord `si`) | 10 | **10/10** |
| **pièges (`non` attendu)** | **5** | **0/5** |
| **tout** | **34** | **29/34 (0,8529)** |

**Ce que ça dit** :

- **Le `si` n'est pas une règle, c'est une convention** : `Ne viens-tu pas ?` attend `si` quand
  la question est rhétorique ou quand on veut l'accord, `non` quand on constate. La **surface**
  ne peut pas décider ; il faut le **contexte** ou le **sens**.
- **Les 5 pièges sont la vraie mesure** : 29/29 était un plafond ; 29/34 dit ce que la règle ne
  sait pas faire.
- **La langue ne suffit pas** : le piège anglais (`You don't come tomorrow?` → `no`) tombe aussi.
- **La frontière est nette** : la séparation accord/constat est **sémantique**, pas
  morphologique — c'est exactement ce qu'un modèle apporte et que l'heuristique ne peut pas.

## 2. Ce que ce banc ne dit pas

- **La définition de la réponse juste** est un choix d'annotateur : `si` reste défendable pour
  certaines questions négatives ; le gold tranche ici par `non`.
- **5 pièges** : un échantillon.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 602** (422 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **l'annotation `non`** (choix) : un autre annotateur dirait `si` ;
- **les 5 pièges** sont tous de la même forme ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le neuronal réel** : le seul à pouvoir trancher accord/constat — la frontière est atteinte.
2. **Le contexte** : une heuristique qui regarde la phrase précédente (l'accord explicite) —
   peut-être un début de solution sans modèle.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `repondre_dirigee`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — les 5 pièges (r418–r422).
- [`autotest.py`](../tools/pensee/autotest.py) — T129, 132/132.
- [`pensee-pieges.json`](pensee-pieges.json) — les 34 questions.
