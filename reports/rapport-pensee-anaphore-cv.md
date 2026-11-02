# B13 — la validation croisée : 25/30, le dernier nom généralise

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **107/107 portes** : les poids des quatre règles sont évalués en **validation croisée à 5
> plis** (partage aléatoire, graine 0). Le total out-of-sample est **25/30** (0,833) ; le poids
> appris est **(1,0,0,0)** dans **4 plis sur 5** — le dernier nom généralise.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-cv.json`](pensee-anaphore-cv.json).

## 1. Les cinq plis

| pli | poids | train | test | justes |
|---|---|---|---:|---:|
| 1 | (0,0,1,0) — hybride | 23 | 6 | 4 |
| 2 | (1,0,0,0) — dernier nom | 24 | 6 | 4 |
| 3 | (1,0,0,0) | 23 | 6 | 5 |
| 4 | (1,0,0,0) | 23 | 6 | 6 |
| 5 | (1,0,0,0) | 23 | 6 | 6 |
| **tout** | — | — | **30** | **25** |

**Ce que ça dit** :

- **Le dernier nom généralise** : 4 plis sur 5 le choisissent ; le pli 1 (le hasard) préfère
  l'hybride — la variance du petit échantillon.
- **Le taux out-of-sample est 0,833** (25/30) : un peu moins que le 27/30 in-sample ; l'écart
  est la **variance**, pas une régression.
- **Le vrai plafond reste 27/30** : aucun poids ne dépasse la meilleure règle seule.
- **La négative est explicite** : 25/30 CV < 27/30 in-sample.

## 2. Ce que ce banc ne dit pas

- **30 liens** ; 100 donneraient des plis plus stables.
- **La grille 0/1/2** est grossière ; des poids réels changeraient la CV.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 522** (342 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (30 liens) ;
- **la graine** (0) : une autre graine déplacerait les plis ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **50 plis / 100 liens** : la CV se stabilise-t-elle ?
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `mesurer_cv`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `coref` sur 32 phrases.
- [`autotest.py`](../tools/pensee/autotest.py) — T104, 107/107.
- [`pensee-anaphore-cv.json`](pensee-anaphore-cv.json) — les plis.
