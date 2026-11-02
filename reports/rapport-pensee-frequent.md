# B13 — la bascule fréquente : 1/50, 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **60/60 portes** : la fiabilité bascule **toutes les 50 épisodes en moyenne** (0,1 ↔ 0,9) —
> environ 160 bascules sur 8000 épisodes. La fenêtre adaptative (50) suit encore ; la politique
> atteint le but **20/20** en **8,0 pas**.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-frequent.json`](pensee-frequent.json).

## 1. La bascule fréquente

Même monde que T56, mais p = 1/50 par épisode (au lieu de 1/500) : le régime change ~16 fois
plus souvent, la fenêtre de 50 ne voit qu'un régime à la fois.

| épisodes | buts | v final | états-Q | pas |
|---:|---|---:|---:|---:|
| 4000 | 20/20 | 0,32 | 783 | 8,0 |
| **8000** | **20/20** | **0,78** | 826 | 8,0 |
| bascule rare (T56) | 20/20 | 0,12 | 820 | 8,0 |

**Ce que ça dit** :

- **Même la bascule fréquente est absorbée** : 20/20, 8,0 pas ; la fenêtre de 50 est à l'échelle
  du régime (50 épisodes).
- **v oscille** (0,32 puis 0,78) : il suit le dernier régime, pas une moyenne — c'est le
  comportement voulu.
- **Le coût est nul** (8,0 pas) : la politique ne perd pas de temps à douter.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Deux régimes** ; une fiabilité continue serait autre.
- **La fenêtre 50** est adaptée à la bascule 1/50 ; 1/10 dépasserait sa capacité.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v 0,78** qui serait un artefact de la fin (le dernier régime est 0,1 ou 0,9) ;
- un **A* caché** (non : `seule_bayes_frequent` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Bascule 1/10** : la fenêtre 50 devient trop lente ; mesurer la limite.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesFrequent`.
- [`autotest.py`](../tools/pensee/autotest.py) — T57, 60/60.
- [`pensee-frequent.json`](pensee-frequent.json) — le bilan.
