# B13 — la porte aléatoire : elle saute à 20 % par pas, la politique réussit 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **42/42 portes** : la porte change de position **aléatoirement** (20 % par pas, sans période).
> La `PolitiqueAppriseAleatoire` (182 états-Q, `d` dans l'état) **atteint le but 20/20** sur
> 20 exécutions avec des hasards différents. La politique **réagit** ; elle ne prédit pas.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-aleatoire.json`](pensee-aleatoire.json).

## 1. La porte aléatoire

Même labyrinthe à deux portes que T31-T38, mais la porte **saute** à chaque pas avec
probabilité 0,2, sans période : `d(t+1) = 1 - d(t)` avec p = 0,2. L'état porte `d` ; la
politique voit la porte du moment et réagit.

| dispositif | résultat |
|---|---|
| **politique seule** | **20/20 buts**, 182 états-Q |
| hasard | 20 exécutions, graines 1000–1019 |

**Ce que ça dit** :

- **La politique réagit** : 20/20 avec un hasard qui change la porte à chaque pas ; elle n'a
  pas besoin de prédire — elle voit `d` et vise la porte du moment.
- **La table est petite** (182 états) : la porte aléatoire n'ajoute pas d'états par rapport à la
  porte mobile (170) ; c'est la **réaction** qui compte.
- **La négative reste** : la politique minute (T21/T28) ne connaît que la porte fixe ; la
  politique bouge (T34) ne connaît qu'une période.
- **Le hasard est dans le monde**, pas dans la politique : `_pas` simule le saut ; la politique
  apprend à viser l'état courant.

## 2. Ce que ce banc ne dit pas

- **20 exécutions** seulement ; une étude plus large serait plus solide.
- **La porte saute après le pas** ; une porte qui saute **avant** serait plus dure.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès ; le taux est élevé) ;
- une **porte codée en dur** dans la politique (non : `d` vient de l'état) ;
- un **A* caché** (non : `seule_aleatoire` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Plus de hasard** : 40 %, 60 % ; mesurer la dégradation.
2. **Porte qui saute avant le pas** : la politique doit anticiper.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseAleatoire`, `seule_aleatoire`.
- [`autotest.py`](../tools/pensee/autotest.py) — T39, 42/42.
- [`pensee-aleatoire.json`](pensee-aleatoire.json) — les 20 exécutions.
