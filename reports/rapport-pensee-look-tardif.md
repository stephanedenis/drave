# B13 — le look tardif : 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **70/70 portes** : l'observation n'est fiable **qu'à l'épisode 3000** (sur 4000) ; avant et
> après, c'est une pièce de monnaie. La politique atteint le but **20/20** en **8,0 pas** : le
> look tardif est **absorbé** par la Q-table.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-look-tardif.json`](pensee-look-tardif.json).

## 1. Le look tardif

Même monde que T66, mais la fiabilité est **0,9 à l'épisode 3000** seulement ; elle est **0,5**
partout ailleurs.

| épisodes | buts | v final | états-Q | pas |
|---:|---|---:|---:|---:|
| **4000** | **20/20** | **0,54** | 530 | 8,0 |
| 8000 | 20/20 | 0,54 | 596 | 8,0 |
| look initial (T66) | 20/20 | 0,44 | 506 | 8,0 |

**Ce que ça dit** :

- **Le look tardif est absorbé** : la Q-table apprend la porte au moment du look (épisode 3000)
  et la garde ; la fenêtre de v (50) l'a peut-être oublié, mais le **Q** s'en souvient.
- **v ≈ 0,54** : la fenêtre ne voit plus le look ; elle reste au hasard, sans conséquence sur la
  politique.
- **Le coût est nul** (8,0 pas) : le look tardif ne coûte pas de pas.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Le look est unique** ; plusieurs looks tardifs ne changeraient rien.
- **La fenêtre de v** n'est pas la mémoire de la politique ; le **Q** l'est.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v 0,54** qui serait un artefact de la fenêtre (le look est sorti) ;
- un **A* caché** (non : `seule_bayes_look_tardif` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Look tardif + oubli** : une politique à mémoire courte (Q avec oubli) ; le look se perdrait.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesLookTardif`.
- [`autotest.py`](../tools/pensee/autotest.py) — T67, 70/70.
- [`pensee-look-tardif.json`](pensee-look-tardif.json) — le bilan.
