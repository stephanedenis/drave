# B13 — l'attachement ciblé : l'exact passe de 0,6438 à 0,8082

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **173/173 portes** : la nature de la cible dépend du **type du segment**, et la règle le dit
> maintenant : pour un **REL/SUB**, l'attachement est l'**antécédent** (la tête du GN à gauche,
> élision séparée : `L'homme` → `homme`) ; pour un **GP**, c'est le **verbe du GV** le plus
> proche. Sur les 146 segments au bon span : **exact 94 → 118** (0,6438 → **0,8082**), top1
> 0,8356, top-k 0,9041. Par convention : **verbes 48/51 (0,9412)**, **noms 70/95 (0,7368)**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_tete_nom`),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-attachement-cible.json`](pensee-attachement-cible.json).

## 1. Avant / après (146 segments au bon span)

| mesure | avant | **attachement ciblé** | écart |
|---|---:|---:|---:|
| top1 | 114 (0,7808) | **122 (0,8356)** | +8 |
| top-k | 132 (0,9041) | 132 (0,9041) | 0 |
| **exact** | **94 (0,6438)** | **118 (0,8082)** | **+24** |
| **verbes** | 37/51 (0,7255) | **48/51 (0,9412)** | +11 |
| **noms** | 57/95 (0,6000) | **70/95 (0,7368)** | +13 |

Rendement global (÷ 239 cibles) : top1 0,5105, top-k 0,5523, exact **0,4937**.

**Ce que ça dit** :

- **La convention se commande par le type** : REL/SUB → antécédent nominal, GP → verbe
  gouverneur. C'est la lecture que le gold suggérait (T169) ; la règle l'applique.
- **L'élision était un piège** : `L'homme` est un seul token pour un regex naïf ; la tête
  nominale sépare `L'` et rend `homme` (4 REL réparés d'un coup).
- **Les verbes atteignent 0,9412** : quand la cible est un verbe, la règle de proximité + lexique
  ne se trompe plus que 3 fois sur 51.
- **Les noms restent à 0,7368** : les antécédents hors GN à gauche (REL sans antécédent proche,
  SUB à cible verbale) sont la limite.
- **La négative est explicite** : 28/146 restent faux.

## 2. Ce que ce banc ne dit pas

- **Les 28 échecs** : non qualifiés (antécédent absent, cible verbale d'un SUB, GV multiple).
- **La convention voulue par le gold** : elle n'est toujours pas documentée ; la règle est une
  hypothèse mesurée, pas une vérité du gold.
- **Le top-k est lenient** (sous-chaînes).
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 3. Ce qui pourrait rendre cette fiche fausse

- **la règle REL** prend le GN à gauche dans **la segmentation S**, pas dans la phrase ;
- **l'élision** est traitée par un motif (`l'`, `d'`, `qu'`…) : les cas `aujourd'hui` sont à part ;
- **le gold** : 612 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Les 28 échecs** : qualifier (antécédent absent, SUB à cible verbale).
2. **Documenter la convention** dans le gold.
3. **Les subordonnées** : demander à S (81 spans).
4. **Politique DRVM/native** : quand les poids seront là.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `_tete_nom`, cible par type.
- [`autotest.py`](../tools/pensee/autotest.py) — T170, 173/173.
- [`pensee-attachement-cible.json`](pensee-attachement-cible.json) — avant/après.
