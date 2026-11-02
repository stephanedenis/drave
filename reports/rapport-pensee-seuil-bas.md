# B13 — le seuil bas : un seuil gradué (~0,40)

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **78/78 portes** : les facteurs 0,36 / 0,38 / 0,40 / 0,41 sont testés sur **5 graines × 5
> exécutions**. **0,36 et 0,38 ≈ 80 %** (20/25) ; **0,40 et 0,41 = 100 %** (25/25). Le seuil
> n'est pas net : il est **gradué** — la probabilité de réussite monte de 0,80 à 1,00 entre
> 0,38 et 0,40.
>
> **Dispositif** : [`graines.py`](../tools/pensee/graines.py), [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-seuil-bas.json`](pensee-seuil-bas.json).

## 1. Le seuil bas

Même monde que T73 (look à l'épisode 3000), facteurs 0,36 à 0,41, 5 graines, 5 exécutions.

| facteur | buts | taux |
|---|---:|---:|
| 0,36 | **20/25** | 0,80 |
| 0,38 | **20/25** | 0,80 |
| **0,40** | **25/25** | 1,00 |
| **0,41** | **25/25** | 1,00 |

**Ce que ça dit** :

- **Le seuil est gradué** : 0,80 à 0,36–0,38, 1,00 à 0,40–0,41 ; il n'y a pas de marche nette.
- **Le point de bascule est ~0,40** : c'est là que la réussite passe de 80 % à 100 %.
- **La grille est cohérente** : 0,35 (T73, 0/25) < 0,36–0,38 (20/25) < 0,40+ (25/25) : la
  probabilité monte avec le facteur, sans être déterministe au bord.
- **La négative reste** : 0,35 échoue 0/25.

## 2. Ce que ce banc ne dit pas

- **5 graines** ; 20 graines lisseraient la courbe.
- **Le bord exact** (0,39 ?) n'est pas localisé.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- **le choix des graines** (0–4) ; une autre série pourrait déplacer la courbe ;
- un **facteur mal appliqué** (le `q[k] *= facteur` est fait tous les 10 épisodes) ;
- un **A* caché** (non : `seule_bayes_oubli_seuil` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Courbe complète** : 0,35 → 0,5 par pas de 0,01 ; tracer la probabilité.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`graines.py`](../tools/pensee/graines.py) — `executer_bas`, 5 graines.
- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesOubliSeuil`.
- [`autotest.py`](../tools/pensee/autotest.py) — T75, 78/78.
- [`pensee-seuil-bas.json`](pensee-seuil-bas.json) — le balayage.
