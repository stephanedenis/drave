# B13 — le bord fin : 0,41 est le seuil robuste

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **87/87 portes** : le bord du seuil est mesuré sur **20 graines × 20 exécutions** (400 essais
> par facteur). **× 0,38 : 73 %** (292/400) ; **× 0,39–0,40 : 95 %** (380/400) ; **× 0,41 :
> 100 %** (400/400) ; **× 0,42 : 100 %** (400/400). Le seuil **robuste** est **0,41**.
>
> **Dispositif** : [`graines.py`](../tools/pensee/graines.py), [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-bord-fin.json`](pensee-bord-fin.json).

## 1. Le bord fin

Même monde que T83 (look à l'épisode 3000), facteurs 0,38 → 0,42, **20 graines**, **20 exécutions**.

| facteur | buts | taux | erreur-type |
|---|---:|---:|---:|
| 0,38 | 292/400 | 0,73 | ±0,022 |
| 0,39 | 380/400 | 0,95 | ±0,011 |
| 0,40 | 380/400 | 0,95 | ±0,011 |
| **0,41** | **400/400** | **1,00** | **0,00** |
| 0,42 | 400/400 | 1,00 | 0,00 |

**Ce que ça dit** :

- **0,41 est le seuil robuste** : 400/400 ; l'erreur-type est nulle au bord haut.
- **La marche est étroite** : 0,38 (73 %) → 0,39–0,40 (95 %) → 0,41 (100 %) ; trois points.
- **Le taux de 0,38 est précis** (73 % ± 2,2 %) : le 0/25 de T73 était bien un échantillon
  pessimiste, le 20/100 (T83) un échantillon chanceux — la vraie valeur est 73 %.
- **La montée est monotone** : pas de creux entre 0,38 et 0,42 à 400 essais.

## 2. Ce que ce banc ne dit pas

- **L'erreur-type** suppose des essais indépendants ; les 20 exécutions par graine partagent le
  même apprentissage, donc les intervalles réels sont plus larges.
- **20 graines** ; 50 resserreraient encore.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- **la dépendance intra-graine** : les 20 exécutions d'une graine ne sont pas indépendantes ;
- **le choix des graines** (0–19) ;
- un **A* caché** (non : `seule_bayes_oubli_seuil` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **50 graines** : resserrer le bord.
2. **Le correctif structurel** : la phase dans l'état (T79) — la leçon de la série.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`graines.py`](../tools/pensee/graines.py) — `executer_bord_fin`.
- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesOubliSeuil`.
- [`autotest.py`](../tools/pensee/autotest.py) — T84, 87/87.
- [`pensee-bord-fin.json`](pensee-bord-fin.json) — le bord.
