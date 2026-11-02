# B13 — le professeur complet : 56 états-Q, il échoue encore seul

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **28/28 portes** : la `PolitiqueAppriseComplete` — shaping + récompense **+1 au but**, 1000
> épisodes, 56 états-Q — est exécutée **seule** sur la porte minute : elle **échoue** en 8 pas.
> Le professeur **complet** n'est pas complet ; l'imitation (T23/T24) ne pouvait pas le dépasser.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-professeur.json`](pensee-professeur.json).

## 1. Le professeur complet

Même porte minute que T21, mais la récompense inclut **+1 au but** en plus du shaping
(-0,01/pas + 0,1/case + 0,1/ouverture), 1000 épisodes, graine 0. Puis exécution **seule**.

| politique | états-Q | buts seuls | pas | A* + sonde (T19) |
|---|---:|---:|---:|---:|
| **professeur complet** | **56** | **0** | **8** | 28 nœuds |
| apprise minute (T21) | 60 | 0 | 8 | 28 nœuds |

**Ce que ça dit** :

- **Le professeur complet échoue encore** : la `seule_minute` s'arrête quand la politique ne
  propose plus d'action ; la Q-table n'a pas la **séquence complète**.
- **+1 au but ne change rien** (56 états) : la récompense rare n'est pas la cause ; c'est la
  **structure** de la politique (le `propose` renvoie `None` avant le but).
- **L'imitation ne pouvait pas dépasser** ce professeur (T23/T24) ; c'est cohérent.
- **L'A* reste nécessaire** (T19) : c'est lui qui explore et atteint le but.

## 2. Ce que ce banc ne dit pas

- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **La `seule_minute`** s'arrête au `None` : c'est la **politique incomplète**, pas la Q-table
  seule.
- **Le +1 au but** est rare (23 états) ; un **curriculum** ou un **shaping potentiel** serait
  plus juste.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (1000 épisodes, graine 0) ;
- un **A* caché** dans `seule_minute` (non : la boucle n'appelle que la Q-table) ;
- une **Q-table** initialisée (non : elle part de zéro) ;
- un **budget** de 200 pas (le `None` arrive en 8).

## 4. La suite

1. **Politique sans `None`** : au pire, une action par défaut (attendre) au lieu de `None`.
2. **Curriculum** : commencer par des états proches du but, puis reculer.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseComplete`.
- [`autotest.py`](../tools/pensee/autotest.py) — T25, 28/28.
- [`pensee-professeur.json`](pensee-professeur.json) — le bilan.
