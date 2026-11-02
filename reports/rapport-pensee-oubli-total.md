# B13 — l'oubli total : 0/20, la mémoire est nécessaire

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **73/73 portes** : la Q-table est **vidée** tous les 10 épisodes. La politique **échoue
> 0/20** (86 états-Q seulement) : sans mémoire, elle ne peut pas accumuler la porte. La limite
> de l'oubli est trouvée : **la mémoire est nécessaire** ; le Q doit persister.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-oubli-total.json`](pensee-oubli-total.json).

## 1. L'oubli total

Même monde que T69 (look à l'épisode 3000), mais la Q-table est **vidée** tous les 10 épisodes.

| oubli | buts | états-Q | pas |
|---|---|---:|---:|
| **total (× 0)** | **0/20** | 86 | 200 |
| × 0,5 (T69) | 20/20 | 586 | 8,0 |
| aucun (T67) | 20/20 | 530 | 8,0 |

**Ce que ça dit** :

- **La mémoire est nécessaire** : sans elle, la politique ne peut pas garder la porte ; elle
  tourne (0/20).
- **La limite est trouvée** : entre × 0,5 (réussit) et × 0 (échoue), il y a un seuil ; ce banc
  ne le localise pas.
- **86 états** : la politique n'a que les états des dix derniers épisodes ; trop peu.
- **La négative est explicite** : 0/20, 200 pas, 86 états-Q.

## 2. Ce que ce banc ne dit pas

- **Le seuil** entre × 0,5 et × 0 n'est pas localisé (× 0,1, × 0,2).
- **L'oubli est uniforme** ; un oubli sélectif serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (0/20, non) ;
- un **v 0,6** qui serait un artefact de la fenêtre (le look est sorti) ;
- un **A* caché** (non : `seule_bayes_oubli_total` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Seuil d'oubli** : × 0,1, × 0,2 ; localiser la limite.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesOubliTotal`.
- [`autotest.py`](../tools/pensee/autotest.py) — T70, 73/73.
- [`pensee-oubli-total.json`](pensee-oubli-total.json) — le bilan.
