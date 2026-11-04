# B13 — les passifs sans `par` : le chunker les détecte, le générateur S les ignore

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **163/163 portes** : le **chunker simple** détecte le passif sans `par` (`être` + participe) et
> donne **`patient`** au sujet — **3/3** sur les tests. Mais l'heuristique par défaut passe par le
> **générateur S**, qui ignore cette règle : l'annotation reste `agent`. Le correctif est
> **dans mon territoire**, mais **pas dans le chemin**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-passifs-sans-par.json`](pensee-passifs-sans-par.json).

## 1. Les deux chemins

| chemin | `Le livre est lu.` | état |
|---|---|---|
| `_syntagmes_simple` (chunker, mon code) | **patient** | ✅ corrigé |
| générateur S (`tools/structures/`, S) | `agent` | ❌ hors territoire |
| annotation finale | `agent` | ❌ |

| test | `_syntagmes_simple` |
|---|---|
| `Le livre est lu.` | patient ✅ |
| `La porte est ouverte.` | patient ✅ |
| `Les enfants sont partis.` | patient ✅ |

**Ce que ça dit** :

- **La règle `être + participe` est dans le chunker** : 3/3, mais le générateur S (le segmenter
  par défaut) ne l'a pas — l'annotation finale ne change pas.
- **Le correctif du chemin est chez S** : `tools/structures/generateur.py`, ligne 251, connaît le
  passif (« par Marie (agent, après un passif) ») mais ne l'applique pas au GN sujet.
- **Deux corrections pour un seul problème** : `_role_gp` (fait) et le chunker (fait) ; il manque
  le générateur S, hors de mon territoire.
- **La négative est explicite** : la porte du bloc reste verte, la sortie ne change pas.

## 2. Ce que ce banc ne dit pas

- **Le générateur S** : sa règle du passif est à corriger par la session S.
- **Les 5 passifs avec `par`** : le GP est corrigé (`agent`), le sujet reste `agent` (S).
- **Le gold 432** : les passifs y sont rares.
- **Le gold 612** (432 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le générateur S** : il peut appliquer une autre règle que celle lue ;
- **trois phrases** : un échantillon ;
- **le gold** : 432 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La session S** : `être + participe` → `patient` dans `generateur.py`.
2. **Le gold des passifs** : en ajouter pour mesurer.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `_syntagmes_simple` (passif).
- [`autotest.py`](../tools/pensee/autotest.py) — T160, 163/163.
- [`pensee-passifs-sans-par.json`](pensee-passifs-sans-par.json) — les deux chemins.
