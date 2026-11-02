# B13 — la bascule très fréquente : 1/10, 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **61/61 portes** : la fiabilité bascule **toutes les 10 épisodes en moyenne** (0,1 ↔ 0,9) —
> ~400 bascules sur 4000. La fenêtre adaptative (50) tient encore : **20/20** en **9,4 pas**
> (le coût de l'adaptation), et **8,0 pas** à 8000 épisodes.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-rapide.json`](pensee-rapide.json).

## 1. La bascule très fréquente

Même monde que T57, mais p = 1/10 par épisode : le régime change presque à chaque observation.

| épisodes | buts | v final | états-Q | pas |
|---:|---|---:|---:|---:|
| **4000** | **20/20** | **0,28** | 766 | 9,4 |
| 8000 | 20/20 | 0,74 | 810 | 8,0 |
| bascule 1/50 (T57) | 20/20 | 0,78 | 826 | 8,0 |

**Ce que ça dit** :

- **La fenêtre tient au-delà de son échelle** : à 1/10, elle réussit encore 20/20 ; le coût est
  visible (9,4 pas contre 8,0) mais la politique ne casse pas.
- **v oscille fort** (0,28 puis 0,74) : il suit le régime courant ; la politique s'adapte.
- **Le coût de l'adaptation** : +1,4 pas à 4000 ; à 8000, le coût disparaît (8,0).
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **La limite** n'est pas trouvée : 1/10 réussit ; 1/5 ou 1/2 la trouveraient peut-être.
- **Deux régimes** ; une fiabilité continue serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v 0,28** qui serait un artefact de la fin (le dernier régime est 0,1 ou 0,9) ;
- un **A* caché** (non : `seule_bayes_rapide` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Bascule 1/5** : chercher la limite de la fenêtre.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesRapide`.
- [`autotest.py`](../tools/pensee/autotest.py) — T58, 61/61.
- [`pensee-rapide.json`](pensee-rapide.json) — le bilan.
