# B13 — le correctif des passifs : `par` → agent, mais le generateur S court-circuite

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **162/162 portes** : la fonction `_role_gp` rend désormais **`agent`** pour `par`/`by` (au lieu de
> `moyen`). Mais l'heuristique en production passe par le **generateur S**, qui a **sa propre**
> table de rôles : le GP `par le chien` reste `moyen` dans l'annotation. Le correctif est
> **partiel** — et la fiche le dit.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-passifs-corriges.json`](pensee-passifs-corriges.json).

## 1. Le correctif

| chemin | `par le chien` | état |
|---|---|---|
| `_role_gp` (le chunker simple) | **agent** | ✅ corrigé |
| generateur S (le défaut de l'heuristique) | `moyen` | ❌ non corrigé |
| annotation finale | `moyen` | ❌ |

**Ce que ça dit** :

- **Le correctif est local** : `_role_gp` est utilisée par le chunker simple, pas par le
  generateur S (le segmenter par défaut) — la correction ne change pas l'annotation.
- **Deux tables de rôles** : le bloc a deux segmenteurs, chacun avec sa logique ; corriger l'un
  ne corrige pas l'autre.
- **Le test est honnête** : 5/5 faux avant, 5/5 faux après dans l'annotation — le correctif du
  rôle est dans le code mais pas dans le chemin.
- **La négative est explicite** : la porte du bloc reste verte, mais la sortie ne change pas.

## 2. Ce que ce banc ne dit pas

- **Le generateur S** : sa table de rôles est à corriger à son tour (le prochain round).
- **Les passifs sans `par`** : non traités.
- **Le gold 432** : les passifs y sont rares.
- **Le gold 612** (432 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le generateur S** : la correction peut y être déjà faite autrement ;
- **les 5 passifs** : un échantillon ;
- **le gold** : 432 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le generateur S** : sa table de rôles (`par` → agent) — le vrai correctif.
2. **Les passifs sans `par`**.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `_role_gp`.
- [`autotest.py`](../tools/pensee/autotest.py) — T159, 162/162.
- [`pensee-passifs-corriges.json`](pensee-passifs-corriges.json) — l'état.
