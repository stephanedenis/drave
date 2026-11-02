# B13 — la bascule limite : 1/5, 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **62/62 portes** : la fiabilité bascule **toutes les 5 épisodes en moyenne** (0,1 ↔ 0,9) —
> ~800 bascules sur 4000. La fenêtre adaptative (50) tient encore : **20/20** en **8,6 pas**.
> La limite de la fenêtre n'est **pas** trouvée sur ce jouet.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-limite.json`](pensee-limite.json).

## 1. La bascule limite

Même monde que T58, mais p = 1/5 par épisode : le régime change presque à chaque pas.

| épisodes | buts | v final | états-Q | pas |
|---:|---|---:|---:|---:|
| **4000** | **20/20** | **0,44** | 735 | 8,6 |
| 8000 | 20/20 | 0,7 | 778 | 8,0 |
| bascule 1/10 (T58) | 20/20 | 0,28 | 766 | 9,4 |

**Ce que ça dit** :

- **La fenêtre tient à 1/5** : 20/20, 8,6 pas ; le coût de l'adaptation reste faible.
- **La limite n'est pas trouvée** : l'adaptation (10 récents vs 10 précédents) est **plus rapide**
  que la fenêtre de 50, et elle suffit même quand la bascule est presque à chaque pas.
- **v oscille** (0,44) : il suit le régime courant ; la politique s'adapte.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Deux régimes** ; une fiabilité continue serait autre.
- **La limite serait peut-être à 1/2** (le régime change à chaque épisode) ; pas testé.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v 0,44** qui serait un artefact de la fin (le dernier régime est 0,1 ou 0,9) ;
- un **A* caché** (non : `seule_bayes_limite` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Bascule 1/2** : le régime change à chaque épisode ; la limite.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesLimite`.
- [`autotest.py`](../tools/pensee/autotest.py) — T59, 62/62.
- [`pensee-limite.json`](pensee-limite.json) — le bilan.
