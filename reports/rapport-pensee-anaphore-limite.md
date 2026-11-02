# B13 — le plafond du gold : 27/30, quatre règles divergent

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **103/103 portes** : les quatre règles de coréférence sont mises côte à côte sur les 30 liens
> du gold. La meilleure — le **dernier nom** — fait **27/30** ; le rôle 23/30 ; l'hybride 24/30 ;
> la sémantique 23/30. Le **plafond** de ce gold est **27/30** : les trois cas restants sont
> **ambigus** ou exigent une annotation que le gold ne porte pas.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-limite.json`](pensee-anaphore-limite.json).

## 1. Les quatre règles

| règle | court (20) | long (10) | **tout (30)** |
|---|---:|---:|---:|
| **dernier nom** | **20** | 7 | **27** |
| rôle | 14 | **9** | 23 |
| hybride | 15 | **9** | 24 |
| sémantique | 15 | 8 | 23 |

**Ce que ça dit** :

- **Le plafond est 27/30** : aucune règle simple ne fait mieux ; les trois cas manquants
  (r321/r322/r337) demandent le **sens du verbe** (`voir` vs `parler`) ou une décision
  d'annotateur.
- **Les règles divergent sur les mêmes cas** : r321/r322 (proximité) vs r337 (rôle) — le gold
  n'a pas de règle unique, il a des **cas**.
- **Le désaccord est une mesure** : 27/23/24/23 ; l'écart de 4 points est la **limite du gold**,
  pas celle d'une règle.
- **La négative est explicite** : 23/30 pour le rôle et la sémantique.

## 2. Ce que ce banc ne dit pas

- **30 liens** ; 100 donneraient une courbe.
- **Les cas ambigus** ne sont pas arbitrés : le gold les tranche à la main.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 522** (342 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (30 liens) ;
- **les annotations** (les cas ambigus sont tranchés à la main) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Arbitrer les cas ambigus** : deux annotateurs, mesurer l'accord (kappa).
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — les quatre résolveurs.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `coref` sur 32 phrases.
- [`autotest.py`](../tools/pensee/autotest.py) — T100, 103/103.
- [`pensee-anaphore-limite.json`](pensee-anaphore-limite.json) — le plafond.
