# B13 — un seul look : 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **69/69 portes** : l'observation n'est **fiable qu'une seule fois** (épisode 0) ; les 3999
> autres sont une pièce de monnaie (0,5). La politique atteint le but **20/20** en **8,0 pas** :
> **un look** suffit à apprendre la porte.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-un-look.json`](pensee-un-look.json).

## 1. Un seul look

Même monde que T65, mais la fiabilité n'est **0,9 qu'à l'épisode 0** ; elle est **0,5** partout
ailleurs.

| épisodes | buts | v final | états-Q | pas |
|---:|---|---:|---:|---:|
| **4000** | **20/20** | **0,44** | 506 | 8,0 |
| 8000 | 20/20 | 0,5 | 572 | 8,0 |
| 4 looks (T65) | 20/20 | 0,44 | 506 | 8,0 |

**Ce que ça dit** :

- **Un look suffit** : la première observation fiable donne la porte ; la Q-table apprend la
  politique avec les autres pas (les looks neutres ne la gênent pas).
- **v ≈ 0,44** : la fenêtre ne voit qu'un look utile au début ; le reste est neutre.
- **Le coût est nul** (8,0 pas) : le look unique ne coûte pas de pas.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Le look est à l'épisode 0** ; un look arrivé plus tard serait aussi valable (la fenêtre 50
  l'oublierait peut-être).
- **Deux régimes** ; une fiabilité continue serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v 0,44** qui serait un artefact de la fenêtre (50 looks, ~0 utile) ;
- un **A* caché** (non : `seule_bayes_un_look` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Look tardif** : le look arrive à l'épisode 3000 ; la fenêtre doit le garder.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesUnLook`.
- [`autotest.py`](../tools/pensee/autotest.py) — T66, 69/69.
- [`pensee-un-look.json`](pensee-un-look.json) — le bilan.
