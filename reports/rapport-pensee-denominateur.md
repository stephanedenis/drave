# B13 — le dénominateur de l'attachement : 239 cibles, 146 segments

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **170/170 portes** : les taux d'attachement étaient divisés par **239** (toutes les cibles)
> alors que `top1`, `top-k` et `exact` ne mesurent que les **146 segments prédits au bon span**.
> Les deux lectures sont désormais nommées : **rendement global** (0,4812 / 0,5523 / 0,1381) et
> **exactitude sur les spans** (0,7877 / 0,9041 / 0,2260). Aucune mesure ne change ; c'est la
> lecture qui devient honnête.
>
> **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-denominateur.json`](pensee-denominateur.json).

## 1. Les deux lectures

| mesure | rendement global (÷ 239) | **exactitude spans (÷ 146)** |
|---|---:|---:|
| top1 | 0,4812 | **0,7877** |
| top-k | 0,5523 | **0,9041** |
| exact | 0,1381 | **0,2260** |
| couverture | 0,6109 | — |

**Ce que ça dit** :

- **La couverture explique la moitié de l'écart** : 94 cibles n'ont pas de segment au bon span
  (REL/SUB de S) ; les compter comme des échecs d'attachement mélangeait deux problèmes.
- **Sur les segments qu'on sait segmenter, l'attachement tient** : top-k **90,4 %**, top1
  **78,8 %**, exact **22,6 %** — la bonne cible est presque toujours proposée.
- **L'exact reste faible** (22,6 %) : le classement des candidats n'est pas appris, la règle de
  proximité+lexique ne tranche pas toujours.
- **La négative est explicite** : 0,2260 d'exact sur les spans, ce n'est pas un attachement.

## 2. Ce que ce banc ne dit pas

- **Les 93 spans manquants** : chez S (REL/SUB), pas dans ce dénominateur.
- **Le classement** : la proximité n'est pas un modèle appris.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.
- **Le coût** : nul, c'est la même passe relue.

## 3. Ce qui pourrait rendre cette fiche fausse

- **le choix des dénominateurs** : les deux sont défendables, ils mesurent deux choses ;
- **les 146 labels** dépendent de la segmentation (S) ;
- **le gold** : 612 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Les 14 cibles** : verbes hors lexique.
2. **Le classement** : apprendre l'ordre des candidats (le prochain levier).
3. **Les subordonnées** : demander à S (81 spans).
4. **Politique DRVM/native** : quand les poids seront là.

## 5. Fichiers

- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `*_taux_span`.
- [`autotest.py`](../tools/pensee/autotest.py) — T167, 170/170.
- [`pensee-denominateur.json`](pensee-denominateur.json) — les deux lectures.
