# B13 — la mémoire courte : 20/20, 10,0 pas

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **71/71 portes** : la Q-table **s'oublie** (× 0,9 tous les 10 épisodes), le look utile est à
> l'épisode 3000. La politique atteint le but **20/20** en **10,0 pas** : l'oubli **coûte**
> 2 pas, mais il ne casse pas la politique.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-oubli.json`](pensee-oubli.json).

## 1. La mémoire courte

Même monde que T67 (look à l'épisode 3000), mais chaque 10 épisodes la Q-table est multipliée
par **0,9** : l'ancien s'efface, le récent reste.

| épisodes | buts | v final | états-Q | pas |
|---:|---|---:|---:|---:|
| **4000** | **20/20** | **0,56** | 463 | 10,0 |
| 8000 | 20/20 | 0,54 | 515 | 10,0 |
| sans oubli (T67) | 20/20 | 0,54 | 530 | 8,0 |

**Ce que ça dit** :

- **L'oubli coûte 2 pas** (10,0 contre 8,0) : la politique réapprend la porte à chaque passage,
  sans la perdre.
- **Il ne casse pas** : 20/20 ; la décroissance est compensée par l'apprentissage (0,25).
- **La Q-table est plus petite** (463 états) : les valeurs faibles s'effondrent, mais les
  décisions restent.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **L'oubli est uniforme** ; un oubli sélectif (les vieux états) serait autre.
- **Le look est à l'épisode 3000** ; un look plus tôt serait plus durement oublié.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v 0,56** qui serait un artefact de la fenêtre (le look est sorti) ;
- un **A* caché** (non : `seule_bayes_oubli` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Oubli fort** (× 0,5) : la limite de la mémoire courte.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesOubli`.
- [`autotest.py`](../tools/pensee/autotest.py) — T68, 71/71.
- [`pensee-oubli.json`](pensee-oubli.json) — le bilan.
