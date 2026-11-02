# B13 — le régime intra-épisode : 20/20, v = 0,48

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **64/64 portes** : la fiabilité change **à chaque observation** (p = 1/2 entre 0,9 et 0,1).
> La politique atteint le but **20/20** en **8,0 pas** : l'observation reste **informative**
> quel que soit son signe ; v se stabilise à **0,48** (la moyenne). La limite de l'adaptation
> n'est **pas** trouvée.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-intra.json`](pensee-intra.json).

## 1. Le régime intra-épisode

Même monde que T60, mais la fiabilité bascule **à chaque look** : l'observation est fiable
(0,9) ou antiprédictive (0,1), au hasard, sans que l'agent le sache.

| épisodes | buts | v final | états-Q | pas |
|---:|---|---:|---:|---:|
| **4000** | **20/20** | **0,48** | 516 | 8,0 |
| 8000 | 20/20 | 0,8 | 570 | 8,0 |
| régime par épisode (T60) | 20/20 | 0,42 | 632 | 8,0 |

**Ce que ça dit** :

- **L'information est dans le signe inconnu** : que l'observation soit fiable ou antiprédictive,
  elle porte la même information (0,8 de log-odds) ; le filtre s'en sert sans savoir lequel.
- **v = 0,48** : la fenêtre ne peut pas trancher (le régime change à chaque look) ; elle reste
  à la moyenne, et cela suffit.
- **Le coût est nul** (8,0 pas) : même au plafond du hasard, la politique ne perd rien.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Deux régimes symétriques** (0,9 / 0,1) ; une fiabilité asymétrique (0,9 / 0,5) serait autre
  et **casserait** probablement le filtre.
- **Le signe est inconnu** ; si l'agent devait le connaître, il faudrait une méta-observation.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v 0,48** qui serait un artefact (la moyenne exacte des deux régimes) ;
- un **A* caché** (non : `seule_bayes_intra` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Fiabilité asymétrique** : 0,9 / 0,5 ; le filtre doit la distinguer.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesIntra`.
- [`autotest.py`](../tools/pensee/autotest.py) — T61, 64/64.
- [`pensee-intra.json`](pensee-intra.json) — le bilan.
