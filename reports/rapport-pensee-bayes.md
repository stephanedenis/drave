# B13 — la croyance bayésienne : un seul look, 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **51/51 portes** : la `PolitiqueAppriseBayes` met à jour `p(d=0)` par la **vraisemblance**
> (0,9 / 0,1 par look) sur **10 niveaux**. Avec **un seul look** par observation, elle atteint
> le but **20/20** dès **2000 épisodes** (9,4 pas). Le filtre **pèse** le bruit au lieu de voter.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-bayes.json`](pensee-bayes.json).

## 1. La croyance bayésienne

Même monde que T44-T47 (10 % d'erreur par révélation), mais `observer` fait **un look** et met à
jour la croyance : `p' = p·v / (p·v + (1−p)(1−v))` avec `v = 0,9` (vu 0) ou `0,1` (vu 1). La
croyance est discrétisée sur **10 niveaux** (0,05 → 0,95).

| dispositif | buts | états-Q | pas |
|---|---:|---:|---:|
| **bayésien** | **20/20** | 552 | 9,4 |
| votante (T46, 2 looks) | 20/20 | 372 | 8,0 |
| trois looks (T47) | 20/20 | 481 | 9,2 |
| bruitée (T45) | 0/20 | 398 | 200 |

**Ce que ça dit** :

- **Un seul look suffit** : la mise à jour pondérée extrait l'information d'une observation
  bruitée ; la politique n'a pas besoin de voter deux ou trois fois.
- **Le coût est comparable** : 9,4 pas (un look + la mise à jour) contre 8,0 (deux looks) et
  9,2 (trois looks) ; le bayésien paie un peu plus en pas, mais **dès 2000 épisodes**.
- **La croyance est plus fine** (10 niveaux, 552 états) : plus d'états, plus de finesse.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Un seul look initial** ; un second look affinerait la croyance.
- **La vraisemblance est connue** (0,9 / 0,1) ; une vraisemblance apprise serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- une **mise à jour mal calibrée** (la vraisemblance est la vraie) ;
- un **A* caché** (non : `seule_bayes` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Deux looks bayésiens** : la croyance après deux mises à jour.
2. **Vraisemblance apprise** : la politique estime la fiabilité de l'observation.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayes`, `_BAYES_P`,
  `_bayes_bucket`.
- [`autotest.py`](../tools/pensee/autotest.py) — T48, 51/51.
- [`pensee-bayes.json`](pensee-bayes.json) — le bilan.
