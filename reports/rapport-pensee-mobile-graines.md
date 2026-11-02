# B13 — la porte mobile sur 5 graines : 5/5 aux deux positions

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **35/35 portes** : la `PolitiqueAppriseMobile` est entraînée (1000 épisodes) sur **5 graines**,
> puis exécutée seule aux deux positions de la porte. **5/5 atteignent le but aux deux** (d0 et
> d1) en **8 pas** ; la Q-table passe de **147 à 184 états**. La porte mobile n'est pas un
> accident de la graine 0.
>
> **Dispositif** : [`graines.py`](../tools/pensee/graines.py), [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-mobile-graines.json`](pensee-mobile-graines.json).

## 1. Les 5 graines

| graine | états-Q | d0 (porte 3,3) | d1 (porte 1,3) |
|---:|---:|---|---|
| 0 | 170 | but/8 | but/8 |
| 1 | 176 | but/8 | but/8 |
| 2 | 184 | but/8 | but/8 |
| 3 | 147 | but/8 | but/8 |
| 4 | 174 | but/8 | but/8 |

**Ce que ça dit** :

- **5/5 aux deux positions** : la politique unique (l'état porte `d`) réussit aux deux routes
  quelque soit la graine ; la mobilité est **apprise**, pas chanceuse.
- **Le chemin est stable** (8 pas partout) : les deux routes font la même longueur ; le coût de
  la mobilité est nul sur ce labyrinthe.
- **La taille varie** (147–184 états) sans changer le résultat : la structure `d` dans l'état
  suffit.
- **La négative reste** : la politique fixe (T21) ne connaît qu'une position ; la comparaison
  T31/T32 contre T21 est le contrôle.

## 2. Ce que ce banc ne dit pas

- **5 graines** seulement ; une étude de variance plus large serait plus solide.
- **Deux positions** ; une porte qui se déplace **pendant** l'épisode serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (5 graines testées, toutes réussissent) ;
- une **position codée en dur** dans la politique (non : `d` vient de l'état) ;
- un **A* caché** (non : `seule_mobile` n'appelle que la Q-table) ;
- une **case de l'autre porte** qui bloquerait (le `_libre_pmob` la libère).

## 4. La suite

1. **Porte qui bouge** : `d` change en cours d'épisode ; l'état doit suivre.
2. **Bruit variable** : 60 %, 90 % ; mesurer la dégradation.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`graines.py`](../tools/pensee/graines.py) — `executer_mobile`, 5 graines.
- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseMobile`.
- [`autotest.py`](../tools/pensee/autotest.py) — T32, 35/35.
- [`pensee-mobile-graines.json`](pensee-mobile-graines.json) — les 5 lignes.
