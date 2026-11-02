# B13 — la règle du `si` : 29/29, la dernière règle de surface

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **131/131 portes** : la règle du `si` (accord français sur les questions négatives) et le repli
> de langue (`und` → `fr`) amènent la réponse dirigée à **29/29**. Le chemin : **19/29** (la
> négation répondait `non`), **25/29** (le `si` seul), **29/29** (le repli des 4 questions
> synthétiques dont la langue n'est pas détectée).
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-si.json`](pensee-si.json).

## 1. Le chemin

| étape | justes | taux |
|---|---:|---:|
| négation seule (`non` si négation) | 19/29 | 0,6552 |
| + `si` pour les négatives françaises | 25/29 | 0,8621 |
| **+ repli `und` → `fr`** | **29/29** | **1,0000** |

**Ce que ça dit** :

- **Le `si` est une règle de langue** : une question négative française attend `si` (accord),
  l'anglaise `yes` ; la règle de surface doit porter la langue.
- **Le repli `und` → `fr` est un choix** : les 4 questions synthétiques (`Hugo écoute?`) ne sont
  pas reconnues comme françaises par le détecteur ; le repli sur le français du gold les sauve.
- **29/29 est un plafond de forme** : il ne prouve pas la compréhension — une question piège
  (`Ne viens-tu pas ?` avec la réponse `non` attendue) le ferait tomber.
- **La règle est nommée** : c'est la **dernière règle de surface** de la ligne ; au-delà, il faut
  un modèle.

## 2. Ce que ce banc ne dit pas

- **Les questions ouvertes** ne sont pas couvertes.
- **29 questions fermées** : un plafond facile.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 597** (417 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le repli `und` → `fr`** : c'est une convention, pas une détection ;
- **la référence `si`** : un autre annotateur dirait `oui` ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le neuronal réel** : la seule sortie qui reste — répondre aux questions ouvertes.
2. **Les questions pièges** : nier la réponse (le `non` attendu) pour casser la règle.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `repondre_dirigee` (si, und → fr).
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — les 29 questions.
- [`autotest.py`](../tools/pensee/autotest.py) — T128, 131/131.
- [`pensee-si.json`](pensee-si.json) — le chemin.
