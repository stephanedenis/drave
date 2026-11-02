# B13 — l'action observer : 20/20, le geste qui révèle la porte

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-01 · **Verdict** : ✅
> **47/47 portes** : la `PolitiqueAppriseObservatrice` ajoute une **cinquième action** —
> `observer` — qui **révèle** la porte (coût 0,1). Sur le monde à observation partielle
> (T41/T42/T43 : 0/20), elle atteint le but **20/20** en **8,3 pas** : le geste remplace la
> croyance passive.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-observatrice.json`](pensee-observatrice.json).

## 1. L'action observer

Même monde que T42 (porte sautant à 20 %, vue à distance 1), mais la politique a 5 actions :
les 4 pas et **`observer`**, qui met la croyance à 1 (porte vue) ou 0, au coût de 0,1.

| dispositif | buts | états-Q | pas |
|---|---:|---:|---:|
| **observatrice** | **20/20** | 448 | 8,3 |
| curiosité (T43) | 0/20 | 148 | 200 |
| croyance (T42) | 0/20 | 154 | 200 |
| mémoire (T41) | 0/20 | 115 | 200 |
| complète (T39/T40) | 20/20 | 182 | 8 |

**Ce que ça dit** :

- **Le geste débloque** : la même information, obtenue par une **action**, suffit ; la croyance
  passive (T41/T42) et la curiosité (T43) échouaient.
- **Le coût est faible** : 8,3 pas contre 8 (observation complète) ; l'observation coûte 0,1 et
  un pas de temps.
- **La table grandit** (448 états, 5 actions) mais la compétence est là : c'est le prix de
  l'exploration.
- **La négative reste** : sans l'action (T41/T42/T43), 0/20.

## 2. Ce que ce banc ne dit pas

- **L'action observer** est parfaite (révèle toujours) ; une observation bruitée serait autre.
- **Le coût 0,1** est un choix ; un coût plus élevé changerait la politique.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- un **hasard favorable** (20 exécutions, 20 succès) ;
- une **révélation gratuite** (l'action coûte 0,1 et un pas ; le chemin est 8,3) ;
- un **A* caché** (non : `seule_observatrice` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Observation bruitée** : la révélation se trompe 10 % du temps.
2. **Coût variable** : observer cher ; la politique doit choisir quand.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseObservatrice`, `seule_observatrice`.
- [`autotest.py`](../tools/pensee/autotest.py) — T44, 47/47.
- [`pensee-observatrice.json`](pensee-observatrice.json) — le bilan.
