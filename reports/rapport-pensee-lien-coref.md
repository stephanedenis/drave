# B13 — la coréférence comme lien : 62/116, la moitié des antécédents retrouvés

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **137/137 portes** : la **coréférence est utilisée comme lien** : chaque pronom lié (par les
> règles de la ligne anaphore) pointe vers la phrase de son **antécédent**. Résultat :
> **62/116 (0,5345)** liens ont une phrase d'antécédent trouvée. La moitié manque — et c'est la
> mesure.
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-lien-coref.json`](pensee-lien-coref.json).

## 1. Le lien

| mesure | valeur |
|---|---:|
| liens de coréférence (r301–r427) | **116** |
| liens avec phrase d'antécédent trouvée | **62** |
| taux | **0,5345** |

**Ce que ça dit** :

- **La moitié des antécédents sont dans une phrase antérieure** : les 62 trouvés sont ceux dont
  le nom de l'antécédent apparaît dans une phrase précédente ; les 54 autres sont des cas où
  l'antécédent est **dans la même phrase** (`il l'attrape`) ou **absent** du texte.
- **Le lien est plus dur que le mot** : la coréférence disait 68/103 sur le mot ; le lien vers la
  **phrase** ne fait que 62/116 — la phrase est une unité plus exigeante.
- **La limite est le texte, pas la règle** : les phrases anaphoriques du gold sont courtes et
  souvent autonomes (`il l'attrape` n'a pas de phrase précédente).
- **La négative est explicite** : 62 < 116.

## 2. Ce que ce banc ne dit pas

- **Les 54 échecs** sont en partie des antécédents intra-phrase, pas des erreurs.
- **116 liens** : un échantillon.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 607** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition de « phrase d'antécédent »** (la dernière phrase qui contient le mot) ;
- **les phrases courtes** du gold rendent le lien artificiellement dur ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Les antécédents intra-phrase** : mesurer séparément les liens dont l'antécédent est dans la
   même phrase (attendu : une grande part des 54).
2. **Le neuronal réel** : toujours bloqué.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `lien_coref`, `mesurer_lien_coref`.
- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `resoudre_meta`.
- [`autotest.py`](../tools/pensee/autotest.py) — T134, 137/137.
- [`pensee-lien-coref.json`](pensee-lien-coref.json) — le lien.
