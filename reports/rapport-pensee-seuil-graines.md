# B13 — le seuil sur 5 graines : le seuil est ~0,4

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **76/76 portes** : le facteur d'oubli est balayé sur **5 graines × 5 exécutions** par facteur.
> **× 0,3 et × 0,35 échouent** (0/25) ; **× 0,4 réussit** (25/25) ; **× 0,45** est à la limite
> (20/25, 4 graines sur 5) ; **× 0,5 réussit** (25/25). Le seuil est **~0,4**.
>
> **Dispositif** : [`graines.py`](../tools/pensee/graines.py), [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-seuil-graines.json`](pensee-seuil-graines.json).

## 1. Le seuil sur 5 graines

Même monde que T72 (look à l'épisode 3000), 5 facteurs × 5 graines, 5 exécutions par graine.

| facteur | buts | taux |
|---|---:|---:|
| 0,30 | **0/25** | 0,00 |
| 0,35 | **0/25** | 0,00 |
| **0,40** | **25/25** | **1,00** |
| 0,45 | **20/25** | 0,80 |
| 0,50 | **25/25** | 1,00 |

**Ce que ça dit** :

- **Le seuil est ~0,4** : à 0,35 la mémoire est trop courte (0/25), à 0,4 elle suffit (25/25).
- **× 0,45 est le bord** (20/25) : 4 graines sur 5 réussissent ; la 5ᵉ perd la porte.
- **× 0,5 est sûr** (25/25) : la moitié de la Q survit par cycle.
- **La non-monotonie de T72 est un effet de graine** : avec 5 graines, l'ordre 0,35 < 0,4 ≤ 0,5 est
  propre ; 0,45 reste le point instable.

## 2. Ce que ce banc ne dit pas

- **5 graines** ; 10 ou 20 graines préciseraient le bord (0,42 ?).
- **L'oubli est uniforme** ; un oubli sélectif serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- **le choix des graines** (0–4) ; une autre série pourrait déplacer le bord ;
- un **facteur mal appliqué** (le `q[k] *= facteur` est fait tous les 10 épisodes) ;
- un **A* caché** (non : `seule_bayes_oubli_seuil` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Bord fin** : 0,42, 0,44 ; 10 graines.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`graines.py`](../tools/pensee/graines.py) — `executer_seuil`, 5 graines.
- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesOubliSeuil`.
- [`autotest.py`](../tools/pensee/autotest.py) — T73, 76/76.
- [`pensee-seuil-graines.json`](pensee-seuil-graines.json) — le balayage.
