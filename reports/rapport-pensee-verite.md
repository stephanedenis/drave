# B13 — la vérité qui change : porte cachée, 20/20 aux deux phases

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **80/80 portes** : la porte **saute** de `(3,3)` à `(1,3)` à mi-entraînement, **sans que la
> phase soit dans l'état**. La `PolitiqueAppriseVerite` (116 états-Q) atteint le but **20/20**
> à la phase 0 **et** à la phase 1, en **8,0 pas** : les deux routes **coexistent** dans la Q.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-verite.json`](pensee-verite.json).

## 1. La vérité qui change

Même monde que T31/T32 (deux positions de porte), mais la **phase est cachée** : la politique ne
la voit pas ; elle reçoit seulement les récompenses. L'entraînement alterne les phases à
mi-parcours.

| phase | buts | états-Q | pas |
|---|---|---:|---:|
| **0 (porte 3,3)** | **20/20** | 116 | 8,0 |
| **1 (porte 1,3)** | **20/20** | 116 | 8,0 |

**Ce que ça dit** :

- **Les deux routes coexistent** : la Q-table garde les valeurs des deux phases ; les routes
  sont **disjointes** (l'une passe par le haut, l'autre par la gauche), donc l'argmax les sert
  sans conflit.
- **La phase n'est pas nécessaire** : l'état `(x, y, open)` suffit, parce que les **murs**
  distinguent les routes.
- **La table est petite** (116 états) : deux routes disjointes, pas deux politiques.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Les routes sont disjointes** ; des routes **concurrentes** (même état, deux actions) ne
  pourraient pas coexister dans un Q sans la phase.
- **Une seule alternance** ; plusieurs changements ne changeraient pas le résultat.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20/20 aux deux, non) ;
- une **phase codée dans l'état** (non : `_cle` ne la contient pas) ;
- un **A* caché** (non : `seule_verite` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Routes concurrentes** : même état, deux actions ; la phase **doit** entrer dans l'état.
2. **20 graines** : lisser la courbe du seuil.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseVerite`, `seule_verite`.
- [`autotest.py`](../tools/pensee/autotest.py) — T77, 80/80.
- [`pensee-verite.json`](pensee-verite.json) — le bilan.
