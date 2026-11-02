# B13 — la curiosité : 0/20, le bonus de certitude ne suffit pas

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **46/46 portes** : la `PolitiqueAppriseCurieuse` ajoute un **bonus de certitude** (0,5 × le
> gain de |p − 0,5|) au reward de la croyance. Elle **échoue 0/20** : récompenser la certitude
> ne suffit pas ; il manque un **geste** pour aller voir la porte.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-curieuse.json`](pensee-curieuse.json).

## 1. La curiosité

Même monde que T42 (porte sautant à 20 %, vue à distance 1), mais la récompense ajoute
`0,5 × (|p' − 0,5| − |p − 0,5|)` : la politique est payée quand sa croyance devient plus
certaine.

| dispositif | buts | états-Q | pas |
|---|---:|---:|---:|
| **curiosité** | **0/20** | 148 | 200 |
| croyance (T42) | 0/20 | 154 | 200 |
| complète (T39/T40) | **20/20** | 182 | 8 |

**Ce que ça dit** :

- **Le bonus ne suffit pas** : la politique reste réactive ; elle ne va pas **chercher**
  l'observation, qui n'arrive que par hasard (l'adjacence).
- **Il manque un geste** : sans action « observer » (ou un plan POMDP), la certitude ne se gagne
  qu'en passant près de la porte, ce que la politique ne fait pas exprès.
- **148 états** : la curiosité ne change pas la compétence.
- **La négative est explicite** : 0/20, 200 pas, 148 états-Q.

## 2. Ce que ce banc ne dit pas

- **Le bonus** est une somme ; un **POMDP** avec la valeur d'information serait plus principled.
- **L'action « observer »** n'existe pas encore ; c'est le prochain levier.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (0/20, non) ;
- une **récompense mal placée** (le bonus est sur la certitude, pas sur l'action) ;
- un **A* caché** (non : `seule_curieuse` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Action « observer »** : un geste explicite qui révèle la porte ; la politique apprendra à
   l'utiliser.
2. **POMDP** : la valeur d'information dans la fonction de valeur.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseCurieuse`, `seule_curieuse`.
- [`autotest.py`](../tools/pensee/autotest.py) — T43, 46/46.
- [`pensee-curieuse.json`](pensee-curieuse.json) — le bilan.
