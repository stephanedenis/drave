# B13 — le seuil d'oubli : dans (0,2 ; 0,5]

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **74/74 portes** : le facteur d'oubli est balayé. **× 0,5 réussit** (T69, 20/20) ; **× 0,2,
> × 0,1 et × 0,05 échouent** (0/20). Le seuil est **localisé** : il est dans l'intervalle
> **(0,2 ; 0,5]**. La mémoire de la Q-table doit garder au moins ~la moitié par cycle.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-seuil.json`](pensee-seuil.json).

## 1. Le seuil

Même monde que T69 (look à l'épisode 3000), mais le facteur d'oubli est un **paramètre**.

| facteur | buts | états-Q | pas |
|---|---:|---:|---:|
| 0,5 (T69) | **20/20** | 586 | 8,0 |
| 0,2 | **0/20** | 646 | 200 |
| 0,1 | **0/20** | 647 | 200 |
| 0,05 | **0/20** | 649 | 200 |

**Ce que ça dit** :

- **Le seuil est dans (0,2 ; 0,5]** : à 0,5 la politique réussit, à 0,2 elle échoue.
- **Le nombre d'états ne fait pas la différence** (646–649) : c'est la **valeur** qui compte,
  pas la couverture.
- **La mémoire doit durer** : un oubli trop fort efface la porte avant que la politique ne
  l'utilise.
- **La négative est explicite** : 0/20 à × 0,2.

## 2. Ce que ce banc ne dit pas

- **Le seuil exact** (0,3 ? 0,4 ?) n'est pas localisé.
- **L'oubli est uniforme** ; un oubli sélectif serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (0/20 à × 0,2, non) ;
- un **facteur mal appliqué** (le `q[k] *= facteur` est fait tous les 10 épisodes) ;
- un **A* caché** (non : `seule_bayes_oubli_seuil` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Seuil fin** : 0,3 et 0,4 ; localiser.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesOubliSeuil`.
- [`autotest.py`](../tools/pensee/autotest.py) — T71, 74/74.
- [`pensee-seuil.json`](pensee-seuil.json) — le balayage.
