# B13 — les pronoms objets : 8/8

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **98/98 portes** : huit phrases à **pronoms objets** (r329–r336 : `le, la, les, lui, them,
> her`) entrent dans le gold (336 phrases). La règle complétée (`OBJETS`, `pos == PRON`) résout
> **8/8** liens justes ; les sujets restent à **12/12**. La coréférence est à **20/20**.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-objets.json`](pensee-anaphore-objets.json).

## 1. Les pronoms objets

| phrase | pronom | attendu | obtenu |
|---|---|---|---|
| r329 `… il la voit` | `la` | `souris` | `souris` |
| r330 `… elle le lit` | `le` | `livre` | `livre` |
| r331 `… ils les cueillent` | `les` | `fleurs` | `fleurs` |
| r332 `… il lui parle` | `lui` | `marie` | `marie` |
| r333 `… it sees it` | `it` | `mouse` | `mouse` |
| r334 `… she reads it` | `it` | `book` | `book` |
| r335 `… they pick them` | `them` | `flowers` | `flowers` |
| r336 `… he speaks to her` | `her` | `marie` | `marie` |

**Ce que ça dit** :

- **8/8** : la même règle (dernier nom, PP ignorés) couvre les objets — le pronom objet suit
  son antécédent de près.
- **La contrainte `pos == PRON`** est nécessaire : `le/la/les` sont aussi des **déterminants**
  (`la souris`) ; sans elle, la règle se déclencherait sur les DET.
- **12/12 + 8/8 = 20/20** : la coréférence est complète sur le gold, mais elle reste **facile**.
- **La négative reste** : la règle naïve (T93) échoue 2/12.

## 2. Ce que ce banc ne dit pas

- **20 liens** ; 50 donneraient une courbe.
- **Les chaînes longues**, l'ellipse, les pronoms disjoints (`lui`, `elle` après préposition)
  ne sont pas couverts au-delà de r332/r336.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 516** (336 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (8 liens objets) ;
- **`pos == PRON`** : le gold doit étiqueter correctement les DET et les PRON ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Les chaînes longues** : trois noms, deux pronoms ; la règle doit tenir.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `PRONOMS`, `OBJETS`, `resoudre`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `coref` sur 20 phrases.
- [`autotest.py`](../tools/pensee/autotest.py) — T95, 98/98.
- [`pensee-anaphore-objets.json`](pensee-anaphore-objets.json) — le bilan.
