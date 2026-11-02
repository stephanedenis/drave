# B13 — la période qui change : 3 pas puis 2 pas

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **40/40 portes** : la porte change de position avec une **période qui change** en cours
> d'épisode — 3 pas, puis 2 pas (cycle de 10). L'**A*** la suit (28 nœuds, sonde 5, coût 58) ;
> la `PolitiqueApprisePhase` (376 états-Q, `t % 10` dans l'état) **atteint le but seule en
> 10 pas**.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-phase.json`](pensee-phase.json).

## 1. La période qui change

Même labyrinthe à deux portes que T34-T36 ; la fonction de position de la porte est :

```
d(t) = (t // 3) % 2      si t < 6
       ((t - 6) // 2) % 2 sinon          (cycle de 10)
```

L'état porte `t % 10` ; la politique voit la **phase** et re-planifie.

| dispositif | résultat |
|---|---|
| **A* + sonde** | but, 28 nœuds, sonde 5, coût 58 |
| **politique seule** | **but/10 pas**, 376 états-Q |

**Ce que ça dit** :

- **La politique suit le rythme** : l'état `t % 10` suffit à apprendre une période qui change
  deux fois ; le but est atteint en 10 pas.
- **Le coût est constant** (58, 10 pas) : la phase ne coûte pas plus que la période fixe.
- **La table grandit** (376 états, cycle de 10) sans changer le chemin : la structure `t` porte
  l'information.
- **La négative reste** : la politique minute (T21/T28) ne connaît pas l'horloge ; la politique
  bouge (T34) ne connaît qu'une période.

## 2. Ce que ce banc ne dit pas

- **Une seule séquence** (3 puis 2) ; une période **aléatoire** serait plus dure.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **La phase est connue** (déterministe) ; une phase **cachée** demanderait une exploration.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (1000 épisodes, graine 0 ; à vérifier sur plusieurs graines) ;
- un **cycle codé en dur** dans la politique (non : `t % 10` vient de l'état) ;
- un **A* caché** dans `seule_phase` (non : la boucle n'appelle que la Q-table) ;
- une **case de l'autre porte** qui bloquerait (le `_libre_pp` la libère).

## 4. La suite

1. **Plusieurs graines** : la phase tient-elle hors graine 0 ?
2. **Période aléatoire** : le rythme change sans préavis.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `LABYRINTHE_PORTE_PHASE`, `REGISTRE_PP`,
  `PolitiqueApprisePhase`, `seule_phase`.
- [`autotest.py`](../tools/pensee/autotest.py) — T37, 40/40.
- [`pensee-phase.json`](pensee-phase.json) — le bilan.
