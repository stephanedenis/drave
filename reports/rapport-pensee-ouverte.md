# B13 — le curriculum des états `open` : le trou de transfert est comblé

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **32/32 portes** : l'audit (T28) avait montré que la politique entraînée sur la porte **minute**
> échoue sur la porte **stochastique** (état `open=True` jamais vu). `PolitiqueAppriseOuverte`,
> entraînée **sur le bruit** (80 %), apprend ces états : elle réussit **seule** sur les deux
> mondes — **but/9 (2 essais)** sur le bruit, **but/8** sur la porte stable.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-ouverte.json`](pensee-ouverte.json).

## 1. Le curriculum

Même labyrinthe que T16-T21, mais la récompense **simule la porte stochastique** à l'entraînement
(80 % d'ouverture, sinon l'état reste) : la Q-table voit les états `open=True` et `open=False`.
1000 épisodes, graine 0, 74 états-Q. Puis exécution **seule**, sans A*.

| politique | états-Q | bruit (seule) | stable (seule) |
|---|---:|---|---|
| **ouverte** | **74** | **but/9 (2 essais)** | **but/8** |
| minute (T21) | 60 | échec/200 | but/8 |

**Ce que ça dit** :

- **Le trou de transfert est comblé** : la politique entraînée sur le bruit réussit seule sur le
  bruit **et** sur la porte stable ; les deux mondes partagent la structure.
- **Le coût du bruit est faible** : +1 pas et 2 essais sur la porte stochastique, par rapport au
  chemin optimal (8).
- **La robustesse s'apprend** : ce n'est pas la porte qui change, c'est la **distribution des
  états** visités à l'entraînement ; le curriculum `open` suffit.
- **La négative reste** : la politique minute (T21/T28) échoue sur le bruit ; le contraste
  `minute` vs `ouverte` est le contrôle.

## 2. Ce que ce banc ne dit pas

- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le bruit est indépendant** (80 % à chaque essai) ; une porte qui apprend serait autre.
- **Le curriculum** est une simulation du bruit à l'entraînement, pas une **randomisation de
  domaine** complète.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (1000 épisodes, graine 0 ; à vérifier sur d'autres graines) ;
- un **bruit simulé** différent du bruit de test (les deux sont à 80 %, même générateur) ;
- un **A* caché** (non : `seule_sto` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces deux mesures (T28 les couvre).

## 4. La suite

1. **Plusieurs graines** : la robustesse tient-elle hors graine 0 ?
2. **Porte mobile** : la porte change de case ; le curriculum doit suivre.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseOuverte`.
- [`autotest.py`](../tools/pensee/autotest.py) — T29, 32/32.
- [`pensee-ouverte.json`](pensee-ouverte.json) — le bilan.
