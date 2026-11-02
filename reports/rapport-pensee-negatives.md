# B13 — les questions négatives : 19/29, la règle ne s'inverse pas

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **130/130 portes** : dix **questions négatives** (`Ne viens-tu pas demain ?`, `Ne mange-t-il
> pas ?`) entrent dans le gold (**417 phrases**, **29 questions**). La réponse dirigée tombe de
> **19/19 à 19/29 (0,6552)** : elle répond `non` à une question négative, alors que le français
> attend `si`. **La négation ne s'inverse pas toute seule.**
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-negatives.json`](pensee-negatives.json).

## 1. Les 29 questions

| sous-ensemble | questions | **dirigée juste** |
|---|---:|---:|
| affirmatives (oui/yes) | 19 | **19/19** |
| **négatives (si)** | **10** | **0/10** |
| **tout** | **29** | **19/29 (0,6552)** |

**Ce que ça dit** :

- **La règle de surface ne suffit plus** : `repondre_dirigee` répond `non` dès qu'elle voit une
  négation ; or une question négative française attend `si` (l'accord), pas `non`.
- **Le piège est mesuré** : 19/19 était un plafond facile (toutes les références étaient
  `oui`/`yes`) ; 19/29 est la **vraie** mesure, et elle est plus honnête.
- **La langue compte deux fois** : `si` n'existe pas en anglais (`Don't you come?` → `yes`), et
  la réponse dépend de la **langue de la question** — un cas que le test précédent avait déjà
  révélé (17/19 → 19/19).
- **La négative est explicite** : la même règle qui faisait 19/19 fait 0/10 sur les négatives.

## 2. Ce que ce banc ne dit pas

- **Le `si` français** est une règle de langue, pas de logique : la réponse `si` = « oui, malgré
  la négation » ; l'heuristique pourrait l'implémenter (`si` pour les négatives françaises).
- **10 questions négatives** : un échantillon.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 417 réels** (587 phrases avec le synthétique).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la référence `si`** (choix d'annotateur : `oui` serait défendable) ;
- **les 10 négatives** sont toutes de la même forme (`Ne ... pas ?`) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La règle `si`** : répondre `si` aux négatives françaises, `yes` aux anglaises négatives —
   puis re-mesurer (attendu 29/29, mais c'est encore une règle de surface).
2. **Le neuronal réel** : toujours bloqué ; c'est lui qui répondrait aux questions ouvertes.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `repondre_dirigee`, `fidelite_dirigee`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — les 10 négatives (r408–r417).
- [`autotest.py`](../tools/pensee/autotest.py) — T127, 130/130.
- [`pensee-negatives.json`](pensee-negatives.json) — les 29 questions.
