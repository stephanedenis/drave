# B13 — la CV sur 20 graines : 0,8467 ± 0,051

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **108/108 portes** : la validation croisée à 5 plis est répétée sur **20 graines** (partage
> aléatoire différent à chaque fois). Le taux moyen est **0,8467** (25,4/30), l'écart-type
> **0,051**, le min **0,7333** (22/30), le max **0,9000** (27/30). Le dernier nom généralise,
> avec la variance d'un échantillon de 30 liens.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-cv-graines.json`](pensee-anaphore-cv-graines.json).

## 1. Les 20 graines

| statistique | valeur |
|---|---:|
| moyenne | **0,8467** |
| écart-type | 0,051 |
| min | 0,7333 (22/30) |
| max | 0,9000 (27/30) |

**Ce que ça dit** :

- **La CV est stable** : 0,85 ± 0,05 ; le pire pli aléatoire fait 22/30, le meilleur 27/30 —
  exactement le plafond du gold.
- **Le dernier nom généralise** : le taux moyen (0,847) est cohérent avec le 27/30 in-sample
  (0,90) ; l'écart est la **variance du partage**, pas une régression.
- **Le plafond revient** : le max des 20 graines = 27/30 = la meilleure règle seule.
- **La négative est explicite** : min 22/30 < 27/30.

## 2. Ce que ce banc ne dit pas

- **30 liens** ; 100 liens resserreraient l'intervalle.
- **Les poids** sont une grille grossière (0/1/2).
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 522** (342 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (30 liens) ;
- **les 20 graines** (0–19) ; une autre série déplacerait la moyenne de ±0,02 ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **100 liens** : la CV se resserre-t-elle ?
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `mesurer_cv`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `coref` sur 32 phrases.
- [`autotest.py`](../tools/pensee/autotest.py) — T105, 108/108.
- [`pensee-anaphore-cv-graines.json`](pensee-anaphore-cv-graines.json) — les 20 graines.
