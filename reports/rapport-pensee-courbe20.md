# B13 — la courbe sur 20 graines : le seuil est ~0,41

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **86/86 portes** : la courbe du seuil est retracée sur **20 graines × 5 exécutions** (100 par
> facteur). Le seuil est **~0,41** (100 % à 0,41) ; la courbe est **graduée** : 20 % à 0,35,
> 70–75 % à 0,36–0,38, 95 % à 0,39–0,40, 100 % à 0,41+. Le **0/25** du balayage à 5 graines
> était un **échantillon** : le taux réel de 0,35 est **20 %**.
>
> **Dispositif** : [`graines.py`](../tools/pensee/graines.py), [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-courbe20.json`](pensee-courbe20.json).

## 1. La courbe sur 20 graines

Même monde que T76 (look à l'épisode 3000), facteurs 0,35 → 0,50, **20 graines**, 5 exécutions.

| facteur | buts | taux |
|---|---:|---:|
| 0,35 | 20/100 | 0,20 |
| 0,36 | 75/100 | 0,75 |
| 0,37 | 70/100 | 0,70 |
| 0,38 | 75/100 | 0,75 |
| 0,39 | 95/100 | 0,95 |
| 0,40 | 95/100 | 0,95 |
| **0,41** | **100/100** | **1,00** |
| 0,42–0,44 | 100/100 | 1,00 |
| **0,45** | **95/100** | **0,95** |
| 0,46–0,50 | 100/100 | 1,00 |

**Ce que ça dit** :

- **Le seuil est ~0,41** : 100 % à 0,41 ; 95 % à 0,39–0,40 ; 70–75 % à 0,36–0,38 ; 20 % à 0,35.
- **La courbe est graduée** : pas de marche nette, une montée de 20 % à 100 % en six pas.
- **Le 0/25 de T73 était un échantillon** : 5 graines sur 0,35 ne suffisent pas à distinguer
  0 % de 20 % ; les 20 graines le font.
- **Le creux de 0,45 est réel mais faible** (95 %) : le bord reste instable, sans casser la
  tendance.
- **La négative reste** : 0,35 ne fait que 20 %.

## 2. Ce que ce banc ne dit pas

- **5 exécutions par graine** ; 20 par graine resserreraient les intervalles.
- **Le 0,35 à 20 %** : le taux exact (15 % ? 25 % ?) demande plus de graines.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- **le choix des graines** (0–19) ; une autre série déplacerait les taux de quelques points ;
- un **facteur mal appliqué** (le `q[k] *= facteur` est fait tous les 10 épisodes) ;
- un **A* caché** (non : `seule_bayes_oubli_seuil` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **20 exécutions par graine** : resserrer les intervalles au bord.
2. **Le correctif structurel** : la phase dans l'état (T79) — la leçon de la série.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`graines.py`](../tools/pensee/graines.py) — `executer_courbe(20)`.
- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesOubliSeuil`.
- [`autotest.py`](../tools/pensee/autotest.py) — T83, 86/86.
- [`pensee-courbe20.json`](pensee-courbe20.json) — la courbe.
