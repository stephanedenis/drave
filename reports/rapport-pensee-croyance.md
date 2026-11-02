# B13 — la croyance : 0/20, la distribution seule ne suffit pas

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **45/45 portes** : à observation partielle, la `PolitiqueAppriseCroyance` porte une
> **distribution** sur la porte (4 niveaux de croyance, mise à jour par le saut et
> l'observation). Elle **échoue 0/20** ; elle tourne 200 pas. La croyance **seule** ne remplace
> pas l'**exploration** : il faut aller voir la porte.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-croyance.json`](pensee-croyance.json).

## 1. La croyance

L'état porte `b ∈ {0,1,2,3}` (la probabilité que la porte soit en `(3,3)` : 0,1 / 0,35 / 0,65 /
0,9). À chaque pas, la croyance est mise à jour : mélange par le saut (20 %), puis
**observation** si l'agent est adjacent (la porte vue force 0 ou 1).

| dispositif | buts | états-Q | pas |
|---|---:|---:|---:|
| **croyance (0/20)** | **0/20** | 154 | 200 |
| mémoire (T41) | 0/20 | 115 | 200 |
| complète (T39/T40) | 20/20 | 182 | 8 |

**Ce que ça dit** :

- **La croyance seule ne suffit pas** : la distribution est correctement mise à jour, mais la
  politique reste **réactive** ; elle ne va pas **chercher** l'information.
- **L'exploration manque** : pour réussir, il faut **aller voir** la porte (l'action
  d'observation), pas seulement la croire.
- **154 états** : la croyance ajoute des états sans ajouter la compétence.
- **La négative est explicite** : 0/20, 200 pas, 154 états-Q.

## 2. Ce que ce banc ne dit pas

- **La croyance est discrétisée** (4 niveaux) ; une croyance continue serait plus fine.
- **La politique n'a pas de valeur d'information** (`information gathering`) ; c'est le
  prochain levier.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (0/20, non) ;
- une **croyance qui contiendrait la vraie porte** (non : elle est mise à jour, mais la politique
  n'agit pas dessus) ;
- un **A* caché** (non : `seule_croyance` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Exploration active** : récompenser la réduction d'incertitude ; la politique ira voir.
2. **POMDP** : la valeur d'information (la croyance dans la fonction de valeur).
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseCroyance`, `seule_croyance`.
- [`autotest.py`](../tools/pensee/autotest.py) — T42, 45/45.
- [`pensee-croyance.json`](pensee-croyance.json) — le bilan.
