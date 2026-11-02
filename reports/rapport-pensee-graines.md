# B13 — la robustesse sur 5 graines : le curriculum `open` tient

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **33/33 portes** : la `PolitiqueAppriseOuverte` est entraînée (1000 épisodes) sur **5 graines**
> et exécutée seule. **5/5 atteignent le but** sur le bruit (8–10 pas, 1–3 essais) et **5/5** sur
> la porte stable (8–9 pas). Le curriculum `open` n'est pas un coup de chance d'une graine.
>
> **Dispositif** : [`graines.py`](../tools/pensee/graines.py), [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-graines.json`](pensee-graines.json).

## 1. Les 5 graines

| graine | états-Q | bruit (seule) | stable (seule) |
|---:|---:|---|---|
| 0 | 74 | but/9 (2 essais) | but/8 |
| 1 | 85 | but/8 (1 essai) | but/8 |
| 2 | 61 | but/10 (3 essais) | but/8 |
| 3 | 85 | but/8 (1 essai) | but/9 |
| 4 | 72 | but/8 (1 essai) | but/8 |

**Ce que ça dit** :

- **5/5 sur le bruit** : le curriculum `open` tient hors graine 0 ; le trou de transfert (T28)
  est comblé de façon **robuste**.
- **5/5 sur la porte stable** : la politique entraînée sur le bruit **généralise** au monde
  déterministe (8–9 pas).
- **Le coût du bruit varie** : 1 à 3 essais, 8 à 10 pas ; la Q-table apprend l'ouverture
  probabiliste, pas un chemin unique.
- **La taille varie** (61–85 états) sans changer le résultat : la structure compte plus que la
  taille.

## 2. Ce que ce banc ne dit pas

- **5 graines** seulement ; une étude de variance plus large serait plus solide.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le bruit** est indépendant (80 % à chaque essai) ; une porte qui apprend serait autre.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (5 graines testées, toutes réussissent) ;
- un **bruit simulé** différent du bruit de test (les deux à 80 %, même générateur) ;
- un **A* caché** (non : `seule_sto` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Porte mobile** : la porte change de case ; le curriculum doit suivre.
2. **Bruit variable** : 60 %, 90 % ; mesurer la dégradation.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`graines.py`](../tools/pensee/graines.py) — les 5 graines.
- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseOuverte`.
- [`autotest.py`](../tools/pensee/autotest.py) — T30, 33/33.
- [`pensee-graines.json`](pensee-graines.json) — les 5 lignes.
