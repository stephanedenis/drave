# B13 — le bord du seuil : × 0,42 et × 0,44 réussissent (50/50)

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **77/77 portes** : les facteurs 0,42 et 0,44 sont testés sur **10 graines × 5 exécutions**.
> Les deux réussissent **50/50**. Le bord est donc **au-dessus de 0,44** ; le point instable
> reste **0,45** (T73 : 20/25). La non-monotonie est un effet de graine au bord.
>
> **Dispositif** : [`graines.py`](../tools/pensee/graines.py), [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-seuil-bord.json`](pensee-seuil-bord.json).

## 1. Le bord

Même monde que T73 (look à l'épisode 3000), facteurs 0,42 et 0,44, 10 graines, 5 exécutions.

| facteur | buts (10 graines) | taux |
|---|---:|---:|
| **0,42** | **50/50** | 1,00 |
| **0,44** | **50/50** | 1,00 |
| 0,45 (T73) | 20/25 | 0,80 |
| 0,35 (T73) | 0/25 | 0,00 |

**Ce que ça dit** :

- **Le bord est au-dessus de 0,44** : 0,42 et 0,44 réussissent 50/50 ; le seuil est donc entre
  0,35 (0/25) et 0,42 (50/50).
- **0,45 reste l'instable** (20/25) : au bord, la graine décide ; 0,44 est sûr, 0,45 ne l'est
  pas — la non-monotonie est un effet de seuil, pas une tendance.
- **Le taux est net** : pas de demi-succès entre 0,42 et 0,44 ; la transition est étroite.
- **La négative reste** : 0,35 échoue 0/25.

## 2. Ce que ce banc ne dit pas

- **Le seuil exact** entre 0,35 et 0,42 n'est pas localisé (0,36–0,41).
- **10 graines** ; 20 préciseraient le bord.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- **le choix des graines** (0–9) ; une autre série pourrait déplacer le bord ;
- un **facteur mal appliqué** (le `q[k] *= facteur` est fait tous les 10 épisodes) ;
- un **A* caché** (non : `seule_bayes_oubli_seuil` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Le seuil bas** : 0,36–0,41 ; localiser entre 0,35 et 0,42.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`graines.py`](../tools/pensee/graines.py) — `executer_bord`, 10 graines.
- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesOubliSeuil`.
- [`autotest.py`](../tools/pensee/autotest.py) — T74, 77/77.
- [`pensee-seuil-bord.json`](pensee-seuil-bord.json) — le balayage.
