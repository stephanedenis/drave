# B13 — l'observation partielle : 0/20, la mémoire ne suffit pas

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **44/44 portes** : quand la porte n'est **vue qu'à distance 1** (sinon inconnue), la
> `PolitiqueApprisePartielle` (le dernier `d` vu dans l'état) **échoue 0/20** ; elle tourne
> 200 pas sans but. Le contraste avec T39/T40 (observation complète : 20/20) est net :
> **la réaction suffisait, la mémoire ne suffit pas**.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-partielle.json`](pensee-partielle.json).

## 1. L'observation partielle

Le monde est le même que T39 (porte à `(3,3)`/`(1,3)`, saut à 20 %), mais l'agent ne voit la
porte que s'il est **adjacent** (Manhattan ≤ 1) ; sinon l'observation vaut « inconnue » (-1).
L'état de la politique est `(x, y, open, vu)` où `vu` est la **dernière porte vue**.

| dispositif | buts | états-Q | pas |
|---|---:|---:|---:|
| **partielle (0/20)** | **0/20** | 115 | 200 |
| complète (T39/T40) | 20/20 | 182 | 8 |

**Ce que ça dit** :

- **La mémoire d'un pas ne suffit pas** : le dernier `d` vu ne dit pas où est la porte
  maintenant ; la politique croit une porte qui a bougé (20 % par pas).
- **L'observation complète était la clé** : la réaction (T39/T40) marchait parce que l'état
  voyait la porte ; sans elle, la Q-table n'a pas de **modèle du monde**.
- **115 états seulement** : la politique a appris des choses, mais pas la croyance ; elle
  tourne.
- **La négative est explicite** : 0/20, 200 pas, 115 états-Q.

## 2. Ce que ce banc ne dit pas

- **La mémoire est d'un pas** ; une mémoire plus longue (les dernières positions) pourrait
  aider.
- **Aucune exploration active** (pas de « chercher la porte ») ; la politique est réactive.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (0/20, non) ;
- une **mémoire qui contiendrait la vraie porte** (non : `vu` est la dernière vue) ;
- un **A* caché** (non : `seule_partielle` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Croyance** : l'état porte une **distribution** sur `d`, pas le dernier vu.
2. **Exploration active** : la politique doit aller voir la porte avant de viser.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueApprisePartielle`, `seule_partielle`.
- [`autotest.py`](../tools/pensee/autotest.py) — T41, 44/44.
- [`pensee-partielle.json`](pensee-partielle.json) — le bilan.
