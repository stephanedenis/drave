# B13 — la porte qui bouge sur 5 graines : 5/5 buts en 10 pas

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **38/38 portes** : la `PolitiqueAppriseBouge` (horloge `t % 6` dans l'état) est entraînée
> (1000 épisodes) sur **5 graines** et exécutée seule. **5/5 atteignent le but en 10 pas** ;
> la Q-table passe de **230 à 253 états**. La porte qui bouge n'est pas un accident de graine.
>
> **Dispositif** : [`graines.py`](../tools/pensee/graines.py), [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-bouge-graines.json`](pensee-bouge-graines.json).

## 1. Les 5 graines

| graine | états-Q | but | pas |
|---:|---:|---|---:|
| 0 | 236 | **oui** | 10 |
| 1 | 235 | **oui** | 10 |
| 2 | 238 | **oui** | 10 |
| 3 | 230 | **oui** | 10 |
| 4 | 253 | **oui** | 10 |

**Ce que ça dit** :

- **5/5 buts en 10 pas** : la re-planification avec la porte qui bouge tient sur toutes les
  graines ; le pas est **stable** (10), pas seulement le but.
- **La taille varie** (230–253 états) sans changer le chemin : l'horloge `t % 6` et la position
  suffisent ; le reste est du bruit d'exploration.
- **Le coût de la mobilité est constant** : +2 pas par rapport à la porte fixe (8), sur les
  5 graines.
- **La négative reste** : la politique minute (T21/T28) ne connaît pas l'horloge ; le contraste
  est le contrôle.

## 2. Ce que ce banc ne dit pas

- **5 graines** seulement ; une étude de variance plus large serait plus solide.
- **Une seule période** (3 pas) ; 2, 4, 5 pas changeraient la difficulté.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (5 graines testées, toutes réussissent) ;
- une **période codée en dur** dans la politique (non : `t` vient de l'état) ;
- un **A* caché** dans `seule_bouge` (non : la boucle n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Période variable** : 2, 4, 5 pas ; mesurer la dégradation.
2. **Porte qui bouge aléatoirement** : la position change sans période fixe.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`graines.py`](../tools/pensee/graines.py) — `executer_bouge`, 5 graines.
- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBouge`.
- [`autotest.py`](../tools/pensee/autotest.py) — T35, 38/38.
- [`pensee-bouge-graines.json`](pensee-bouge-graines.json) — les 5 lignes.
