# B13 — la dérive continue : v = 0,5, 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **56/56 portes** : la fiabilité **glisse** linéairement de 5 % à 50 % d'erreur sur les 4000
> épisodes. La `PolitiqueAppriseBayesGlisse` (fenêtre adaptative) finit à **v = 0,5** — le
> régime **courant** — et atteint le but **20/20** en **8,6 pas**.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-glisse.json`](pensee-glisse.json).

## 1. La dérive continue

Même monde que T51/T52, mais l'erreur **glisse** : `p_erreur = 0,05 + 0,45·i/N` à chaque
épisode (de 5 % à 50 %). La fenêtre adaptative (10 récents vs 10 précédents) suit le glissement.

| dispositif | buts | v final | états-Q | pas |
|---|---:|---:|---:|---:|
| **glisse** | **20/20** | **0,5** | 738 | 8,6 |
| dérive en deux régimes (T51) | 20/20 | 0,56 | 691 | 8,0 |
| adaptative (T52) | 20/20 | 0,8 | 781 | 8,0 |

**Ce que ça dit** :

- **La fenêtre suit le glissement** : v finit à 0,5 (le dernier régime, 50 % d'erreur) ; la
  politique ne reste pas accrochée aux anciennes fiabilités.
- **Elle réussit** : 20/20 en 8,6 pas ; la dérive continue ne casse pas la politique.
- **Le coût est faible** (738 états, +0,6 pas) : le glissement se paie en pas, pas en table.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Un seul sens** (la fiabilité se dégrade) ; une amélioration serait le miroir.
- **La pente est constante** ; un glissement brutal serait plus dur.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v final 0,5** qui serait un artefact de la fin (le dernier régime est bien 0,5) ;
- un **A* caché** (non : `seule_bayes_glisse` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Glissement brutal** : la fiabilité tombe d'un coup ; la fenêtre doit réagir vite.
2. **Seuil appris** : la politique estime quand la fiabilité a changé.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesGlisse`.
- [`autotest.py`](../tools/pensee/autotest.py) — T53, 56/56.
- [`pensee-glisse.json`](pensee-glisse.json) — le bilan.
