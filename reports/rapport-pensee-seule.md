# B13 — la politique seule : 8 pas, 15/15 buts, sans A*

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **17/17 portes** : la `PolitiqueApprise` entraînée est exécutée **seule**, sans A* : elle suit
> son argmax Q et atteint le but en **8 pas** sur **15/15 runs** (5 budgets × 3 graines).
> L'apprentissage n'est donc **pas masqué** par l'A* : la Q-table sait **conduire** le labyrinthe
> à porte.
>
> **Dispositif** : [`courbe.py`](../tools/pensee/courbe.py), [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-courbe.json`](pensee-courbe.json).

## 1. La politique seule

À chaque état `(x, y, open)`, la politique choisit l'action d'argmax Q, avance d'un pas
(la porte s'ouvre si l'action la vise), et recommence. Aucun A*, aucun budget de recherche :
seulement la **table apprise**.

| épisodes | graines | états-Q | buts seuls | pas | but avec A* |
|---:|---:|---:|---:|---:|---:|
| 50 | 0,1,2 | 52–74 | **3/3** | **8** | 3/3 |
| 100 | 0,1,2 | 52–74 | **3/3** | **8** | 3/3 |
| 200 | 0,1,2 | 61–74 | **3/3** | **8** | 3/3 |
| 400 | 0,1,2 | 62–83 | **3/3** | **8** | 3/3 |
| 800 | 0,1,2 | 62–83 | **3/3** | **8** | 3/3 |

**Ce que ça dit** :

- **La politique seule atteint le but en 8 pas** : c'est le **chemin optimal** (Manhattan 8) ;
  la Q-table n'a pas seulement appris la porte, elle a appris le **chemin**.
- **15/15 runs**, y compris à **50 épisodes** : l'apprentissage est **complet** très tôt sur ce
  jouet ; les épisodes supplémentaires ne changent pas le chemin.
- **L'A* n'était pas nécessaire** pour exécuter : il servait de **cadre** à la sonde ; la
  politique seule est le **vrai** test de ce qui est appris.
- **La Q-table reste petite** (52–83 états) : le jouet est déterministe, mais la preuve est
  claire : le modèle peut être une **table** qui **conduit**.

## 2. Ce que ce banc ne dit pas

- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué (`llama-cli`
  refusé, pas de poids `drave-n0`).
- **Le labyrinthe 5×5 déterministe** : 8 pas, pas de bruit ; une porte stochastique serait
  plus dure.
- **Les 8 pas** sont l'optimum Manhattan ; un labyrinthe plus long testerait la **généralisation**
  de la table.
- **Le coût 5** de la sonde n'intervient pas ici (la politique seule ne paie pas la sonde du
  moteur) : c'est un test de **politique**, pas de coût.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** : 15 runs, 3 graines, tous réussissent ;
- un **argmax dégénéré** qui suivrait un chemin trivial (le labyrinthe a une seule sortie) ;
- un **A* caché** dans l'exécution (non : la boucle `seule` n'appelle que la Q-table) ;
- un **budget** de 200 pas (le but est atteint en 8).

## 4. La suite

1. **Porte stochastique** : 80 % d'ouverture ; la politique doit réessayer.
2. **Labyrinthe plus long** : tester la **généralisation** de la table (ou un réseau).
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`courbe.py`](../tools/pensee/courbe.py) — `seule()`, la politique sans A*.
- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueApprise`.
- [`autotest.py`](../tools/pensee/autotest.py) — T14, 17/17.
- [`pensee-courbe.json`](pensee-courbe.json) — les 15 runs avec `seule_but`/`seule_pas`.
