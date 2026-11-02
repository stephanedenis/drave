# B13 — l'information ultra-rare : utile 0,1 %, 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **68/68 portes** : l'observation n'est **utile qu'un épisode sur mille** (0,9) — **4 looks**
> sur 4000. La politique atteint le but **20/20** en **8,0 pas** : la rareté n'est pas la limite.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-ultra-rare.json`](pensee-ultra-rare.json).

## 1. L'information ultra-rare

Même monde que T64, mais la fiabilité est **0,9 un épisode sur mille** et **0,5** les autres :
4 looks utiles sur 4000.

| épisodes | buts | v final | états-Q | pas |
|---:|---|---:|---:|---:|
| **4000** | **20/20** | **0,44** | 506 | 8,0 |
| 8000 | 20/20 | 0,5 | 572 | 8,0 |
| utile 1 % (T64) | 20/20 | 0,54 | 535 | 8,0 |

**Ce que ça dit** :

- **4 looks utiles suffisent** : la politique apprend la porte avec 4 observations fiables ;
  le reste (0,5) est neutre.
- **v ≈ 0,44** : la fenêtre ne voit presque que des looks inutiles ; elle reste au hasard, et
  cela ne l'empêche pas de réussir.
- **Le coût est nul** (8,0 pas) : la rareté ne coûte pas de pas.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **4 looks** ; 1 look (1/4000) serait peut-être la limite.
- **Le régime est périodique** ; un régime aléatoire rare serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v 0,44** qui serait un artefact de la fenêtre (50 looks, ~0 utile) ;
- un **A* caché** (non : `seule_bayes_tres_tres_rare` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Un look** (1/4000) : la limite absolue.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesTresTresRare`.
- [`autotest.py`](../tools/pensee/autotest.py) — T65, 68/68.
- [`pensee-ultra-rare.json`](pensee-ultra-rare.json) — le bilan.
