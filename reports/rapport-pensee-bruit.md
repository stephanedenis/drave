# B13 — le bruit variable : la politique tient de 50 % à 95 %

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **36/36 portes** : la `PolitiqueAppriseOuverte` est entraînée à **80 %** d'ouverture, puis
> testée **seule** de **50 % à 95 %**. Elle atteint le but **6/6** ; l'effort s'adapte : 3 essais
> à 50–70 %, 2 à 80 %, 1 à 90–95 %, et 10 → 8 pas.
>
> **Dispositif** : [`courbe.py`](../tools/pensee/courbe.py), [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-bruit.json`](pensee-bruit.json).

## 1. Le bruit variable

Même labyrinthe que T16-T29 ; la politique est entraînée à **80 %** (un seul entraînement,
1000 épisodes, graine 0, 74 états-Q) puis évaluée **seule** à six taux d'ouverture.

| p(ouverture) | but | pas | essais |
|---:|---|---:|---:|
| 0,50 | **oui** | 10 | 3 |
| 0,60 | **oui** | 10 | 3 |
| 0,70 | **oui** | 10 | 3 |
| 0,80 | **oui** | 9 | 2 |
| 0,90 | **oui** | 8 | 1 |
| 0,95 | **oui** | 8 | 1 |

**Ce que ça dit** :

- **6/6 buts** : la politique entraînée à 80 % **généralise** à des taux très différents ; elle
  n'a pas mémorisé un taux, elle a appris la **structure** (viser la porte, réessayer).
- **L'effort s'adapte** : 3 essais quand la porte résiste (50–70 %), 1 quand elle s'ouvre
  presque toujours ; 10 pas contre 8.
- **Le bruit est un coût, pas un mur** : la politique ralentit mais n'échoue pas.
- **La négative reste** : la politique minute (T21/T28) échoue sur le bruit ; le contraste est
  le contrôle.

## 2. Ce que ce banc ne dit pas

- **La politique est entraînée à 80 %** ; un entraînement à 50 % serait peut-être meilleur à
  50 % — le **taux d'entraînement** n'est pas optimisé ici.
- **Le bruit est indépendant** ; une porte qui apprend ou se corrompt serait autre.
- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (1000 épisodes, graine 0 ; T30 montre 5/5 sur 5 graines) ;
- un **bruit de test** différent du bruit d'entraînement (même générateur, taux variable) ;
- un **A* caché** (non : `seule_sto` n'appelle que la Q-table) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvre).

## 4. La suite

1. **Entraînement au taux le plus dur** : 50 % ; comparer.
2. **Porte qui bouge** : `d` change en cours d'épisode ; l'état doit suivre.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`courbe.py`](../tools/pensee/courbe.py) — `seule_sto` (paramètre `p_ouvre`).
- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueAppriseOuverte`.
- [`autotest.py`](../tools/pensee/autotest.py) — T33, 36/36.
- [`pensee-bruit.json`](pensee-bruit.json) — les six taux.
