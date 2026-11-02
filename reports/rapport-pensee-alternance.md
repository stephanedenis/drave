# B13 — les ruptures répétées : 20/20, v = 0,14

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **58/58 portes** : la fiabilité **alterne** entre 0,9 et 0,1 toutes les 1000 épisodes (quatre
> phases). La fenêtre adaptative suit chaque rupture ; v finit à **0,14** (le dernier régime) et
> la politique atteint le but **20/20** en **8,0 pas**.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-alternance.json`](pensee-alternance.json).

## 1. Les ruptures répétées

Même monde que T54, mais l'erreur **alterne** : 0,1 (épisodes 0–999), 0,9 (1000–1999),
0,1 (2000–2999), 0,9 (3000–3999)…

| épisodes | buts | v final | états-Q | pas |
|---:|---|---:|---:|---:|
| 4000 | 20/20 | 0,1 | 727 | 8,0 |
| **8000** | **20/20** | **0,14** | 797 | 8,0 |
| rupture unique (T54) | 20/20 | 0,12 | 780 | 8,0 |

**Ce que ça dit** :

- **Les ruptures répétées sont absorbées** : la même fenêtre adaptative suit les alternances ;
  v finit sur le dernier régime (0,14), pas sur une moyenne.
- **Le but est atteint** (20/20, 8,0 pas) : l'alternance ne casse pas la politique.
- **Le coût est nul** (8,0 pas) : chaque régime est exploité, même antiprédictif.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Alternance régulière** (toutes les 1000) ; une alternance aléatoire serait plus dure.
- **La période 1000** est un choix ; 100 ou 500 changeraient la réactivité.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v final 0,14** qui serait un artefact de la fin (le dernier régime est bien 0,9) ;
- un **A* caché** (non : `seule_bayes_alternance` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Alternance aléatoire** : la fiabilité change sans préavis.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesAlternance`.
- [`autotest.py`](../tools/pensee/autotest.py) — T55, 58/58.
- [`pensee-alternance.json`](pensee-alternance.json) — le bilan.
