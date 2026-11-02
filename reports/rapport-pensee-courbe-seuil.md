# B13 — la courbe complète du seuil : 0 → 80 % → 100 % (un creux à 0,45)

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **79/79 portes** : la courbe du seuil d'oubli est tracée de **0,35 à 0,50 par pas de 0,01**,
> sur **5 graines × 5 exécutions**. La réussite passe de **0 %** (0,35) à **80 %** (0,36–0,38)
> à **100 %** (0,39+), avec **un creux à 0,45** (80 %). Le seuil est **gradué**, pas net.
>
> **Dispositif** : [`graines.py`](../tools/pensee/graines.py), [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-seuil-courbe.json`](pensee-seuil-courbe.json).

## 1. La courbe

Même monde que T73 (look à l'épisode 3000), facteurs 0,35 → 0,50, 5 graines, 5 exécutions.

| facteur | buts | taux |
|---|---:|---:|
| 0,35 | 0/25 | 0,00 |
| 0,36–0,38 | 20/25 | 0,80 |
| 0,39–0,44 | 25/25 | 1,00 |
| **0,45** | **20/25** | **0,80** |
| 0,46–0,50 | 25/25 | 1,00 |

**Ce que ça dit** :

- **La courbe est graduée** : 0,80 puis 1,00 ; le seuil est un **plateau**, pas une marche.
- **Un creux à 0,45** (20/25) : au bord, une graine perd la porte ; le creux est **local** et
  n'inverse pas la tendance.
- **Le plateau 100 %** couvre 0,39–0,44 et 0,46–0,50 : la politique est robuste au-delà de 0,39.
- **La négative reste** : 0,35 → 0/25.

## 2. Ce que ce banc ne dit pas

- **5 graines** ; 20 lisseraient le creux.
- **Le creux de 0,45** est un effet de graine, pas une loi.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- **le choix des graines** (0–4) ; une autre série déplacerait le creux ;
- un **facteur mal appliqué** (le `q[k] *= facteur` est fait tous les 10 épisodes) ;
- un **A* caché** (non : `seule_bayes_oubli_seuil` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **20 graines** : lisser le creux et le seuil.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`graines.py`](../tools/pensee/graines.py) — `executer_courbe`, 5 graines.
- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesOubliSeuil`.
- [`autotest.py`](../tools/pensee/autotest.py) — T76, 79/79.
- [`pensee-seuil-courbe.json`](pensee-seuil-courbe.json) — la courbe.
