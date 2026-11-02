# B13 — l'accord entre règles : kappa de −0,16 à 1,0

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **104/104 portes** : les quatre règles de coréférence sont comparées par le **kappa de Cohen**
> sur les 30 liens du gold. `role` et `sémantique` sont **identiques** (κ = 1,0) ; `hybride`
> suit (0,90) ; le **dernier nom** est **anti-corrélé** aux trois autres (κ ≈ −0,16). Le
> désaccord n'est pas du bruit : c'est une **autre règle**.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-kappa.json`](pensee-anaphore-kappa.json).

## 1. Les kappas

| paire | κ |
|---|---:|
| role / sémantique | **1,00** |
| role / hybride | 0,90 |
| hybride / sémantique | 0,90 |
| dernier nom / role | **−0,16** |
| dernier nom / hybride | −0,15 |
| dernier nom / sémantique | **−0,16** |

**Ce que ça dit** :

- **`role` et `sémantique` sont la même règle** sur ce gold (κ = 1,0) : la table sémantique
  n'ajoute rien aux rôles des segments.
- **`hybride` est presque `role`** (0,90) : il n'emprunte à la proximité que pour l'objet.
- **Le dernier nom est une autre règle** (κ négatif) : il se trompe **là où les autres
  réussissent** et vice-versa — c'est la définition d'une règle complémentaire, pas d'un bruit.
- **La négative est explicite** : κ = −0,16, pas 0.

## 2. Ce que ce banc ne dit pas

- **30 liens** ; 100 donneraient des kappas stables.
- **Les κ sont entre règles**, pas entre annotateurs humains.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 522** (342 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (30 liens) ;
- **le kappa** sur des verdicts binaires, sensible aux classes rares ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Un vote pondéré** : les règles en désaccord, une méta-règle (forêt) ; mesurer.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `kappa`, `accords`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `coref` sur 32 phrases.
- [`autotest.py`](../tools/pensee/autotest.py) — T101, 104/104.
- [`pensee-anaphore-kappa.json`](pensee-anaphore-kappa.json) — les accords.
