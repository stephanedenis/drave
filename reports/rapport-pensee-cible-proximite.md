# B13 — la cible par proximité : l'exact passe de 0,0042 à 0,0544 (×13)

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **164/164 portes** : la règle « la cible d'un segment est le **verbe du GV le plus proche** »
> remplit les `cible` que le générateur S laissait vides. Sur le même gold que T153 (612 phrases,
> **239 cibles**), l'attachement passe de **top1 82 (0,3431)** à **95 (0,3975)**, et surtout de
> **exact 1 (0,0042)** à **13 (0,0544)** — **×13**. La tête fait **94/145 (0,6483)** contre 81
> (0,5586).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_cible_proche`),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-cible-proximite.json`](pensee-cible-proximite.json).

## 1. Avant / après (même gold, 612 phrases, 239 cibles)

| mesure | T153 (avant) | **règle de proximité** | écart |
|---|---:|---:|---:|
| top1 | 82 (0,3431) | **95 (0,3975)** | +13 (+0,0544) |
| top-k | 78 (0,3264) | 78 (0,3264) | 0 |
| **exact** | **1 (0,0042)** | **13 (0,0544)** | **+12 (×13)** |
| tête top1 | 81/145 (0,5586) | **94/145 (0,6483)** | +13 (+0,0897) |
| couverture (span) | 0,6067 | 0,6067 | 0 (inchangé) |

Sur les **432 premières** phrases seules (184 cibles) : top1 73 (0,3967), exact 13 (0,0707).

**Ce que ça dit** :

- **La proximité est un signal réel** : +13 top1 et **×13 en exact** — le verbe le plus proche est
  souvent la bonne cible, ce que l'absence de règle laissait à 1/239.
- **Le top-k ne bouge pas** : les `candidats` sont encore des types (`GN`, `GP`), pas des verbes ;
  c'est la prochaine marche (proposer les verbes en candidats).
- **La couverture ne bouge pas** : elle mesure l'alignement de span (S), pas le remplissage de
  `cible` — c'est une autre limite, côté générateur.
- **La négative est explicite** : 226/239 restent faux en exact ; la règle se trompera sur les
  passifs et les phrases à plusieurs GV.

## 2. Ce que ce banc ne dit pas

- **Pourquoi 13 et pas plus** : les 226 échecs ne sont pas qualifiés (mauvais GV, mauvais verbe,
  cible non verbale ?).
- **Les passifs** : la règle de proximité ignore l'inversion agent/patient (T158/T160).
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.
- **Le coût** : la règle ajoute un `_syntagmes_simple` par segment dans le chemin chunker (à
  surveiller).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le repli ne s'applique qu'aux cibles manquantes** : il ne contredit pas le générateur S ;
- **la mesure** : `top1` accepte les sous-chaînes (`vu` ⊂ `aperçu`), `exact` non — deux lectures ;
- **le gold** : 612 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Les candidats verbes** : remplir `candidats` avec les verbes proches (le top-k à 0).
2. **Qualifier les 226 échecs** : mauvais GV, mauvais verbe, ou cible non verbale.
3. **Les passifs** : la règle de proximité y est fausse par construction.
4. **Politique DRVM/native** : quand les poids seront là.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `_cible_proche` (proximité).
- [`autotest.py`](../tools/pensee/autotest.py) — T153 mis à jour, T161, 164/164.
- [`pensee-cible-proximite.json`](pensee-cible-proximite.json) — avant/après.
