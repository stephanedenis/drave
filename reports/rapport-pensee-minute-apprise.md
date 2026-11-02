# B13 — la Q-table sur la porte minute : elle apprend l'ouverture-passage

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **22/22 portes** : la `PolitiqueApprise` (Q-learning, 200 épisodes) affronte la **porte à un
> tour** : elle doit ouvrir **et** passer dans le même pas. L'A* + la sonde atteignent le but en
> **28 nœuds** (sonde 6, coût 62) — la politique apprise **transfère** à la porte minute.
>
> **Dispositif** : [`operateurs.py`](../tools/pensee/operateurs.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-minute-apprise.json`](pensee-minute-apprise.json).

## 1. La porte minute apprise

Même labyrinthe que T18, mais la politique est la `PolitiqueApprise` (entraînée sur la porte
**déterministe** T11) au lieu de la règle manhattan. La porte ne s'ouvre qu'un pas ; la sonde
ouvre **et** passe.

| politique | nœuds | pas | saut | sonde | coût | but |
|---|---:|---:|---:|---:|---:|---|
| **apprise** | **28** | 13 | 10 | **6** | **62** | **oui** |
| manhattan (T18) | 27 | 12 | 10 | 5 | 57 | oui |

**Ce que ça dit** :

- **La Q-table transfère** à la porte minute : elle vise la porte, la sonde ouvre et passe ; le
  but est atteint en 28 nœuds.
- **Elle paie +1 nœud et +1 sonde** par rapport à la règle (62 contre 57) : l'apprentissage
  tabulaire est proche, pas identique.
- **La politique apprise n'a pas été entraînée sur la porte minute** : c'est un **transfert**
  du déterministe vers la porte à un tour.
- **Le coût reste modeste** (62) : la porte minute ne coûte pas plus cher que la porte stable.

## 2. Ce que ce banc ne dit pas

- **Q-learning tabulaire** : pas un réseau ; le vrai modèle neuronal reste bloqué.
- **Le transfert** est testé sur un seul changement (la porte minute) ; une porte **mobile**
  serait plus dure.
- **Le coût 5** de la sonde est déclaré.
- **Le labyrinthe 5×5** est un jouet.

## 3. Ce qui pourrait rendre cette fiche fausse

- une **graine chanceuse** (200 épisodes, graine 0) ;
- un **A* qui masque** la politique (la politique seule sur la porte minute n'est pas mesurée) ;
- une **confusion** ouverture / passage : la sonde fait les deux ;
- un **budget** trop grand.

## 4. La suite

1. **La politique seule sur la porte minute** : sans A*, la Q-table ouvre et passe-t-elle ?
2. **Porte mobile** : la porte change de case ; la politique doit s'adapter.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : 200 réels atteints ; le gold peut encore grandir.

## 5. Fichiers

- [`operateurs.py`](../tools/pensee/operateurs.py) — `PolitiqueApprise`, `LABYRINTHE_PORTE_MINUTE`.
- [`autotest.py`](../tools/pensee/autotest.py) — T19, 22/22.
- [`pensee-minute-apprise.json`](pensee-minute-apprise.json) — le bilan.
