# B13 — le seuil fin : × 0,4 réussit, × 0,45 échoue (non monotone)

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **75/75 portes** : le facteur d'oubli est balayé finement. **× 0,4 réussit** (20/20) ;
> **× 0,3, × 0,35 et × 0,45 échouent** (0/20). Le seuil n'est **pas monotone** : le résultat
> dépend de la graine autant que du facteur. La limite est **floue**, pas un seuil net.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-seuil-fin.json`](pensee-seuil-fin.json).

## 1. Le balayage fin

Même monde que T71 (look à l'épisode 3000), facteur balayé de 0,3 à 0,45.

| facteur | buts | états-Q | pas |
|---|---:|---:|---:|
| 0,3 | **0/20** | 694 | 200 |
| 0,35 | **0/20** | 627 | 200 |
| **0,4** | **20/20** | 644 | 10,0 |
| 0,45 | **0/20** | 617 | 200 |

**Ce que ça dit** :

- **Le seuil n'est pas monotone** : × 0,4 réussit, × 0,45 échoue ; le résultat dépend de la
  **graine** (une seule graine testée) autant que du facteur.
- **La limite est floue** : ce n'est pas un seuil net ; la Q-table est sensible au chemin.
- **× 0,4 réussit** (1 point sur 5 du balayage) : la politique tient à ce facteur, pas au voisin.
- **La négative est explicite** : 0/20 à × 0,3, × 0,35 et × 0,45.

## 2. Ce que ce banc ne dit pas

- **Une seule graine** ; il faudrait 5 graines par facteur pour trancher.
- **L'oubli est uniforme** ; un oubli sélectif serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- **le hasard de la graine** : c'est la limite principale de cette fiche ; × 0,4 pourrait échouer
  sur une autre graine ;
- un **facteur mal appliqué** (le `q[k] *= facteur` est fait tous les 10 épisodes) ;
- un **A* caché** (non : `seule_bayes_oubli_seuil` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **5 graines par facteur** : trancher le seuil (le prochain round).
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesOubliSeuil`.
- [`autotest.py`](../tools/pensee/autotest.py) — T72, 75/75.
- [`pensee-seuil-fin.json`](pensee-seuil-fin.json) — le balayage.
