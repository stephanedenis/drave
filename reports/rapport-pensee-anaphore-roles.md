# B13 — la résolution par rôle : 23/30, complémentaire du dernier nom

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **100/100 portes** : la résolution par le **rôle du segment** (`agent` → sujet, `patient` →
> objet) est mesurée. Elle **gagne** sur les chaînes longues (7/10 → **9/10**) et **perd** sur
> les cas courts (20/20 → **14/20**) : les deux règles sont **complémentaires**, pas
> substituables.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-roles.json`](pensee-anaphore-roles.json).

## 1. Les deux règles

| sous-ensemble | dernier nom | **rôle** | écart |
|---|---:|---:|---:|
| r301–r336 (court) | **20/20** | 14/20 | −6 |
| r337–r342 (long) | 7/10 | **9/10** | +2 |
| **tout** | **27/30** | 23/30 | −4 |

**Ce que ça dit** :

- **Le rôle gagne sur les chaînes** (`il`/`elle`/`she` reprennent le sujet, pas le dernier nom) ;
  il perd sur les cas courts où le pronom reprend l'**objet** le plus proche (`Le chat voit le
  chien ; il dort` → `chien`).
- **Les deux règles sont complémentaires** : la bonne n'est ni l'une ni l'autre, c'est un
  **hybride** (rôle pour le sujet, proximité pour l'objet) — la prochaine mesure.
- **Le total baisse** (27 → 23) : le rôle seul est **moins bon** que le dernier nom sur ce gold.
- **La négative est explicite** : 23/30 contre 27/30.

## 2. Ce que ce banc ne dit pas

- **30 liens** ; 100 donneraient une courbe.
- **L'hybride** n'est pas implémenté ; il est la suite.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 522** (342 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (30 liens) ;
- **les rôles** (annotation à la main) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **L'hybride** : rôle pour le sujet, proximité pour l'objet ; viser 29–30/30.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `resoudre_roles`, `mesurer_roles`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `coref` sur 32 phrases.
- [`autotest.py`](../tools/pensee/autotest.py) — T97, 100/100.
- [`pensee-anaphore-roles.json`](pensee-anaphore-roles.json) — le bilan.
