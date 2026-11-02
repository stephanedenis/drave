# B13 — le hasard variable : 20–60 %, 20/20 à chaque taux

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **43/43 portes** : la `PolitiqueAppriseAleatoire` est entraînée avec un saut de porte à
> **20 %**, puis exécutée avec des sauts de **20 %, 40 % et 60 %**. Elle atteint le but
> **20/20 à chaque taux**, en **8 pas** en moyenne. Quand l'état voit la porte, le hasard ne
> coûte **rien** : la politique **réagit** à chaque pas.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-hasard.json`](pensee-hasard.json).

## 1. Le hasard variable

Même labyrinthe à deux portes que T39 ; la porte saute avec `p_saut` après chaque pas.
L'entraînement utilise `p_saut = 0,2` ; l'évaluation balaie 0,2 / 0,4 / 0,6, 20 exécutions
chacune.

| p(saut) | buts | pas moyen |
|---:|---:|---:|
| 0,2 | **20/20** | 8,0 |
| 0,4 | **20/20** | 8,0 |
| 0,6 | **20/20** | 8,0 |

**Ce que ça dit** :

- **Le hasard ne coûte rien** : 20/20 aux trois taux, 8 pas (le chemin optimal) ; la politique
  voit `d` à chaque pas et vise la porte du moment.
- **La réaction remplace la prédiction** : inutile de modéliser le hasard ; l'état suffit.
- **La table est la même** (182 états) : le taux de saut ne change pas la politique.
- **La négative reste** : la politique minute (T21/T28) ne voit pas `d` ; elle échoue.

## 2. Ce que ce banc ne dit pas

- **Trois taux** (20/40/60) ; 80 % ou 100 % seraient plus durs.
- **La porte saute après le pas** ; une porte qui saute **avant** (pendant le pas) serait
  différente.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions par taux, 20 succès) ;
- une **porte codée en dur** dans la politique (non : `d` vient de l'état) ;
- un **A* caché** (non : `seule_aleatoire` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Porte qui saute avant le pas** : la politique doit anticiper ou attendre.
2. **Observation partielle** : la porte n'est vue qu'à distance 1 ; le hasard redevient un
   problème.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseAleatoire(p_saut=…)`.
- [`autotest.py`](../tools/pensee/autotest.py) — T40, 43/43.
- [`pensee-hasard.json`](pensee-hasard.json) — les trois taux.
