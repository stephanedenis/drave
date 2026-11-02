# B13 — l'information très rare : utile 1 %, 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **67/67 portes** : l'observation n'est **utile qu'un épisode sur cent** (0,9) ; les 99 autres
> sont une pièce de monnaie (0,5). La politique atteint le but **20/20** en **8,0 pas** : les
> **1 %** d'information suffisent. La limite de la rareté n'est **pas** trouvée.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-tres-rare.json`](pensee-tres-rare.json).

## 1. L'information très rare

Même monde que T63, mais la fiabilité est **0,9 un épisode sur cent** et **0,5** les autres :
~40 looks utiles sur 4000 épisodes.

| épisodes | buts | v final | états-Q | pas |
|---:|---|---:|---:|---:|
| **4000** | **20/20** | **0,54** | 535 | 8,0 |
| 8000 | 20/20 | 0,52 | 579 | 8,0 |
| utile 10 % (T63) | 20/20 | 0,8 | 589 | 8,0 |

**Ce que ça dit** :

- **1 % d'information suffit** : 40 looks utiles suffisent à apprendre la politique ; le but est
  atteint en 8,0 pas.
- **v ≈ 0,54** : la fenêtre voit surtout des looks inutiles (0,5) ; elle reste proche du hasard,
  mais les 40 looks utiles ont fait le travail.
- **Le coût est nul** (8,0 pas) : la rareté ne coûte pas de pas.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Un look sur cent** ; un sur mille serait plus dur (4 looks utiles).
- **Le régime est périodique** ; un régime aléatoire rare serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v 0,54** qui serait un artefact de la fenêtre (50 looks, ~0,5 utile) ;
- un **A* caché** (non : `seule_bayes_tres_rare` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Un look sur mille** : la limite de la rareté.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesTresRare`.
- [`autotest.py`](../tools/pensee/autotest.py) — T64, 67/67.
- [`pensee-tres-rare.json`](pensee-tres-rare.json) — le bilan.
