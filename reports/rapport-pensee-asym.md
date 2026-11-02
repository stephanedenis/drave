# B13 — la fiabilité asymétrique : 0,9 / 0,5, 20/20

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **65/65 portes** : la fiabilité alterne entre **0,9** (fiable) et **0,5** (inutile — une pièce
> de monnaie). Le filtre s'en sort : **20/20** en **8,0 pas**, v à **0,44**. Les looks inutiles
> n'apportent rien, les looks fiables portent l'information.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-asym.json`](pensee-asym.json).

## 1. La fiabilité asymétrique

Même monde que T55, mais les régimes sont **0,9 et 0,5** (alternance toutes les 1000 épisodes) :
la moitié du temps, l'observation ne dit **rien** (une pièce de monnaie).

| épisodes | buts | v final | états-Q | pas |
|---:|---|---:|---:|---:|
| **4000** | **20/20** | **0,44** | 679 | 8,0 |
| 8000 | 20/20 | 0,5 | 751 | 8,0 |
| intra symétrique (T61) | 20/20 | 0,48 | 516 | 8,0 |

**Ce que ça dit** :

- **L'asymétrie est absorbée** : quand l'observation ne dit rien (0,5), le filtre ne bouge pas ;
  quand elle dit (0,9), il apprend.
- **v ≈ 0,44** : la moyenne des deux régimes ; le filtre ne peut pas distinguer le bon du
  neutre sans le savoir, mais il **s'en sert** quand même.
- **Le but est atteint** (20/20, 8,0 pas) : les looks utiles suffisent.
- **La négative reste** : sans mise à jour (T45), 0/20.

## 2. Ce que ce banc ne dit pas

- **Deux régimes** ; une fiabilité continue serait autre.
- **La moitié du temps utile** ; 10 % du temps utile serait plus dur.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- un **v 0,44** qui serait un artefact (la moyenne exacte des 0,9/0,5) ;
- un **A* caché** (non : `seule_bayes_asym` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Utile 10 % du temps** : la limite de l'asymétrie.
2. **Vérité qui change** : la porte change de loi, pas seulement le bruit.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseBayesAsym`.
- [`autotest.py`](../tools/pensee/autotest.py) — T62, 65/65.
- [`pensee-asym.json`](pensee-asym.json) — le bilan.
