# B13 — le bayésien à deux looks : 8,0 pas, 0,99 de confiance

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **52/52 portes** : la `PolitiqueAppriseBayes2` fait **deux looks** et **deux mises à jour**
> bayésiennes : la confiance monte à **0,99**. Elle atteint le but **20/20** en **8,0 pas**
> (contre 9,4 pour un look). Le second look **paie** : il coûte 0,1 et rend le chemin optimal.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-bayes2.json`](pensee-bayes2.json).

## 1. Le bayésien à deux looks

Même monde que T48 (10 % d'erreur par révélation), mais `observer` fait **deux looks** et
applique **deux fois** la mise à jour `p' = p·v / (p·v + (1−p)(1−v))`.

| dispositif | buts | états-Q | pas |
|---|---:|---:|---:|
| **bayes2** | **20/20** | 544 | 8,0 |
| bayes (T48, 1 look) | 20/20 | 552 | 9,4 |
| votante (T46, 2 looks) | 20/20 | 372 | 8,0 |

**Ce que ça dit** :

- **Le second look paie** : 8,0 pas au lieu de 9,4 ; la confiance 0,99 évite les détours.
- **Le bayésien égale le vote** (8,0) mais avec une **croyance fine** (10 niveaux) au lieu d'un
  vote binaire ; les deux voies convergent.
- **Le coût est payé une fois** : 0,2 pour deux looks, mais le chemin est optimal.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Deux looks** ; trois looks donneraient 0,999 mais coûteraient plus.
- **La vraisemblance est connue** (0,9 / 0,1) ; une vraisemblance apprise serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- une **mise à jour mal calibrée** (la vraisemblance est la vraie) ;
- un **A* caché** (non : `seule_bayes2` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Trois looks bayésiens** : la confiance 0,999 ; le coût.
2. **Vraisemblance apprise** : la politique estime la fiabilité de l'observation.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayes2`.
- [`autotest.py`](../tools/pensee/autotest.py) — T49, 52/52.
- [`pensee-bayes2.json`](pensee-bayes2.json) — le bilan.
