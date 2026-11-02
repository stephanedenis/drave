# B13 — l'information rare : utile 10 % du temps, 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **66/66 portes** : l'observation n'est **utile qu'un épisode sur dix** (0,9) ; les neuf autres
> sont une pièce de monnaie (0,5). La politique atteint le but **20/20** en **8,0 pas** : les
> **10 %** d'information suffisent.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-rare.json`](pensee-rare.json).

## 1. L'information rare

Même monde que T62, mais la fiabilité est **0,9 un épisode sur dix** et **0,5** les autres :
l'observation est le plus souvent inutile.

| épisodes | buts | v final | états-Q | pas |
|---:|---|---:|---:|---:|
| **4000** | **20/20** | **0,8** | 589 | 8,0 |
| 8000 | 20/20 | 0,6 | 636 | 8,0 |
| asymétrie 50/50 (T62) | 20/20 | 0,44 | 679 | 8,0 |

**Ce que ça dit** :

- **10 % d'information suffisent** : la politique trouve la porte avec un look utile sur dix.
- **v monte à 0,8** : la fenêtre attrape les looks utiles récents et les pèse ; le filtre
  exploite la rareté.
- **Le coût est nul** (8,0 pas) : les looks inutiles ne coûtent pas de pas.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Un look sur dix** ; un sur cent serait plus dur.
- **Le régime est périodique** (tous les dix) ; un régime aléatoire rare serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v 0,8** qui serait un artefact de la fenêtre (50 looks, ~5 utiles) ;
- un **A* caché** (non : `seule_bayes_rare` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Un look sur cent** : la limite de la rareté.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesRare`.
- [`autotest.py`](../tools/pensee/autotest.py) — T63, 66/66.
- [`pensee-rare.json`](pensee-rare.json) — le bilan.
