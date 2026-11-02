# B13 — la pénalité -1 ne casse pas le cycle : 0/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **85/85 portes** : le but de la phase 1 (`(4,0)`) coûte **-1** en phase 0. La
> `PolitiqueAppriseVerite6` (144 états-Q) atteint **0/20 au but 0** et **20/20 au but 1** : le
> cycle `(3,0) ↔ (4,0)` **tient**. La trace montre que le `(3,0)`'s « droite » est **stale**
> (1,517) et bat le « bas » (1,463) d'un cheveu : la pénalité ne suffit pas.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-cycle.json`](pensee-cycle.json).

## 1. La pénalité

Même monde que T80, mais `_pas` renvoie **-1** quand l'agent entre dans `(4,0)` en phase 0 (le but
de la phase 1).

| version | but 0 | but 1 | états-Q |
|---|---:|---:|---:|
| T80 (signal) | 0/20 | 20/20 | 136 |
| **T82 (pénalité -1)** | **0/20** | **20/20** | 144 |

**Ce que ça dit** :

- **La pénalité ne suffit pas** : le `(4,0)`'s « gauche » garde 0,815 ; le `(3,0)`'s « droite »
  garde 1,517 (stale) ; le cycle est un **point fixe** de la mise à jour (le `(3,0)` est peu
  visité, l'alpha 0,25 met longtemps à le corriger).
- **La trace est explicite** : `(0,0) → (1,0) → (2,0) → (3,0) → (4,0) → (3,0) → …`, le `(4,0)`
  n'est pas pénalisé **à l'entrée** — la pénalité est sur la case, pas sur la transition.
- **Le vrai correctif** est structurel : la **phase dans l'état** (T79, 20/20) sépare les deux
  politiques ; le reward shaping (T82) ne suffit pas.
- **La négative est explicite** : 0/20 au but 0.

## 2. Ce que ce banc ne dit pas

- **Une pénalité plus forte** (-5, -10) ou une pénalité **de transition** pourraient casser le
  cycle ; pas testé.
- **L'alpha 0,25** ralentit la correction ; un alpha plus grand aiderait.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition de la pénalité** (sur la case, pas la transition) : c'est la limite ;
- un **but dans la clé** (non : `_cle` ne contient que `(x, y, open, signal)`) ;
- un **A* caché** (non : `seule_verite6` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le correctif structurel** : la phase dans l'état (déjà T79, 20/20) — la pénalité est un
   détour inutile.
2. **20 graines** : lisser la courbe du seuil.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseVerite6`, `seule_verite6`.
- [`autotest.py`](../tools/pensee/autotest.py) — T82, 85/85.
- [`pensee-cycle.json`](pensee-cycle.json) — le bilan.
