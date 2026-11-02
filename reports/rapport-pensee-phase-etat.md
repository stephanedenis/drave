# B13 — la phase dans l'état : le correctif, 20/20 aux deux buts

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **82/82 portes** : la phase entre dans la clé (`(x, y, open, phase)`). La
> `PolitiqueAppriseVerite3` (145 états-Q) atteint **20/20 au but 0** et **20/20 au but 1**, en
> **6,0 pas** — contre **0/20** au but 0 pour T78. Le correctif est net : les routes concurrentes
> **coexistent** dès que la phase est dans l'état.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-phase-etat.json`](pensee-phase-etat.json).

## 1. Le correctif

Même monde que T78 (but caché `(4,4)` ou `(4,0)`), mais la clé contient la **phase**.

| version | but 0 | but 1 | états-Q | pas |
|---|---:|---:|---:|---:|
| T78 (sans phase) | **0/20** | 20/20 | 86 | 200 |
| **T79 (avec phase)** | **20/20** | **20/20** | 145 | 6,0 |

**Ce que ça dit** :

- **Le correctif est net** : 0/20 → 20/20 au but 0 ; les deux politiques sont **séparées** par la
  phase.
- **Le coût est nul** : 6,0 pas, mieux que T78 au but 1 (0 pas, mais 200 au but 0) ; la moyenne
  est meilleure.
- **145 états** : deux buts × deux routes, la table double (86 → 145) — le prix de la
  séparation.
- **La négative reste** : sans la phase, 0/20 (T78).

## 2. Ce que ce banc ne dit pas

- **La phase est fournie** (pas devinée) : un agent réel devrait l'**inférer** de l'observation.
- **Deux phases** ; trois ou plus multiplieraient la table.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- **la phase donnée** (ce n'est pas un POMDP résolu) ;
- un **but dans la clé par accident** (non : `_cle` ajoute `self.phase` explicitement) ;
- un **A* caché** (non : `seule_verite3` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **La phase devinée** : l'agent infère la phase de ses observations (le vrai POMDP).
2. **20 graines** : lisser la courbe du seuil.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseVerite3`, `seule_verite3`.
- [`autotest.py`](../tools/pensee/autotest.py) — T79, 82/82.
- [`pensee-phase-etat.json`](pensee-phase-etat.json) — le bilan.
