# B13 — le régime aléatoire : 1/2, 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **63/63 portes** : la fiabilité change de régime **à chaque épisode avec p = 1/2** — le
> maximum du hasard. La fenêtre adaptative tient encore : **20/20** en **8,0 pas**. La limite
> de la fenêtre n'est **pas** trouvée : l'adaptation est plus rapide que la fenêtre.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-hasard2.json`](pensee-hasard2.json).

## 1. Le régime aléatoire

Même monde que T59, mais p = 1/2 par épisode : à chaque épisode, le régime (0,1 ou 0,9) peut
changer ; c'est le hasard maximal sur deux régimes.

| épisodes | buts | v final | états-Q | pas |
|---:|---|---:|---:|---:|
| **4000** | **20/20** | **0,42** | 632 | 8,0 |
| 8000 | 20/20 | 0,66 | 684 | 8,0 |
| bascule 1/5 (T59) | 20/20 | 0,44 | 735 | 8,6 |

**Ce que ça dit** :

- **Le hasard maximal est absorbé** : 20/20, 8,0 pas ; la politique s'adapte à chaque épisode.
- **v oscille** (0,42) : il suit le régime du moment ; il ne peut pas faire mieux.
- **Le coût est nul** (8,0 pas) : l'observation reste informative, quel que soit le régime.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Deux régimes** ; une fiabilité continue serait autre.
- **La limite** serait peut-être dans la **fréquence intra-épisode** (le régime change à chaque
  pas) ; pas testé.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v 0,42** qui serait un artefact de la fin (le dernier régime est 0,1 ou 0,9) ;
- un **A* caché** (non : `seule_bayes_hasard` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Régime intra-épisode** : la fiabilité change à chaque pas ; la limite.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesHasard`.
- [`autotest.py`](../tools/pensee/autotest.py) — T60, 63/63.
- [`pensee-hasard2.json`](pensee-hasard2.json) — le bilan.
