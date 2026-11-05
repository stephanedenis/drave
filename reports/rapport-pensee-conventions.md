# B13 — les deux conventions du gold : verbes 0,7255, noms 0,6000

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **172/172 portes** : la cible d'attachement du gold n'est pas homogène — **51 cibles sont des
> verbes** (le gouverneur : `joue`, `vu`) et **95 sont des noms** (l'antécédent d'un REL, la tête
> d'un GP : `livre`, `frère`). Mesurées séparément : **verbes 37/51 (0,7255)**, **noms 57/95
> (0,6000)**. Le 0,6438 global de T168 était la moyenne de deux choses différentes.
>
> **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-conventions.json`](pensee-conventions.json).

## 1. Les deux mesures

| nature de la cible | cibles | justes | taux |
|---|---:|---:|---:|
| **verbe** (le gouverneur) | 51 | 37 | **0,7255** |
| **nom** (antécédent de REL, tête de GP) | 95 | 57 | **0,6000** |
| tout | 146 | 94 | 0,6438 |

**Ce que ça dit** :

- **Le gold n'a pas une convention, il en a deux** : `cible` désigne tantôt le verbe qui gouverne
  le segment, tantôt la tête nominale à laquelle il se rattache. Aucune documentation du gold ne
  tranche.
- **L'attachement verbe marche mieux** (0,7255) que l'attachement nom (0,6000) : la règle de
  proximité + lexique verbal est faite pour les verbes ; les antécédents de REL demandent une
  autre règle (le nom à gauche, hors du relatif).
- **La mesure globale cachait l'écart** : 0,6438 = moyenne pondérée (51 × 0,73 + 95 × 0,60).
- **La négative est explicite** : 14 verbes et 38 noms restent faux.


> **Note du 2026-11-05 (intégration v2)** : la ligne « SUB » de ce tableau est **fausse** —
> elle avait été lue avec `_est_verbe`, qui classe 53 verbes comme des noms. Le **POS du gold**
> donne **69/69 cibles SUB = VERB** et, sur les 145 segments, **116 verbes / 29 noms** (et non
> 63/82). La convention a été corrigée dans `gold_reel.py` (`CONVENTION_CIBLE`) et la mesure
> suit désormais le POS du gold ; voir [attachement v2](rapport-pensee-attachement-v2.md).

## 2. Ce que ce banc ne dit pas

- **La convention voulue** : elle n'est pas écrite ; tant qu'elle ne l'est pas, les deux mesures
  doivent être publiées ensemble.
- **Les 52 échecs** : non qualifiés (verbe hors lexique, nom hors du relatif, GV multiple).
- **Le top-k est lenient** (sous-chaînes).
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 3. Ce qui pourrait rendre cette fiche fausse

- **la classification verbe/nom** utilise `_est_verbe` (lexique + désinences), pas une annotation ;
- **les 146 segments** dépendent de la segmentation (S) ;
- **le gold** : 612 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Documenter la convention** dans le gold (ou la choisir : verbe pour les compléments,
   antécédent pour les relatifs).
2. **L'attachement nominal** : une règle dédiée aux REL/SUB (le nom à gauche, hors du relatif).
3. **Les 52 échecs** : les qualifier.
4. **Politique DRVM/native** : quand les poids seront là.

## 5. Fichiers

- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `verbe` / `nom`.
- [`autotest.py`](../tools/pensee/autotest.py) — T169, 172/172.
- [`pensee-conventions.json`](pensee-conventions.json) — la scission.
