# B13 — les 94 spans : 48 REL, 33 SUB, 12 GP

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **169/169 portes** : les échecs d'attachement par **span** (93 après le correctif) sont
> **48 REL**, **33 SUB** et **12 GP** — les subordonnées ne sont **pas produites** (65 cas) ou le
> sont avec un span plus large (25). Le correctif testé — borner le GP au verbe et au relatif —
> gagne **un span** (couverture 0,6067 → 0,6109, F1 0,2864 → 0,2869) mais **perd une cible** :
> le total des échecs ne bouge pas (107).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-spans.json`](pensee-spans.json).

## 1. Les 93 spans

| type | échecs de span |
|---|---:|
| **REL** | **48** |
| **SUB** | **33** |
| **GP** | **12** |
| **tout** | **93** |

| catégorie | nombre |
|---|---:|
| aucun segment du même type | 65 |
| plus large | 25 |
| plus étroit | 3 |
| coupé en plusieurs | 1 |

| mesure | avant | **après le GP borné** |
|---|---:|---:|
| segments au bon span (labels) | 145 | **146** |
| couverture | 0,6067 | **0,6109** |
| F1 syntagmes | 0,2864 | **0,2869** |
| échecs span / cible | 94 / 13 | **93 / 14** |
| top1 / top-k / exact | 115 / 132 / 33 | **115 / 132 / 33** |

**Ce que ça dit** :

- **Les subordonnées sont le trou** (81 des 93) : REL et SUB ne sont pas produits — c'est
  l'analyse des subordonnées du **générateur S** (`tools/structures/`), hors de mon territoire.
- **Le GP avalait le verbe** (`de la voisine dort`) : borné au verbe et au relatif, il gagne un
  span — mais une cible se perd, et le total reste à 107 échecs.
- **Le correctif est neutre sur l'attachement** et positif sur la segmentation : la fiche le dit.
- **La négative est explicite** : 107 échecs, dont 81 hors de mon territoire.

## 2. Ce que ce banc ne dit pas

- **Les 81 REL/SUB** : leur segmentation est chez S (le générateur de structures).
- **Les 25 « plus large »** : leur cause n'est pas qualifiée (S ou chunker).
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.
- **Le coût** : l'analyse complète du gold, quelques secondes.

## 3. Ce qui pourrait rendre cette fiche fausse

- **le dénominateur** : 239 cibles ; 93 sans segment au même span ;
- **le classement « plus large »** est une heuristique de lecture des chevauchements ;
- **le gold** : 612 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Les subordonnées** : demander à S la production des REL/SUB (81 spans).
2. **Les 14 cibles** : verbes hors lexique.
3. **Le dénominateur de l'attachement** : il mélange 239 cibles et 146 segments (mesure à corriger).
4. **Politique DRVM/native** : quand les poids seront là.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — GP borné (`RELATIFS`, `_est_verbe`).
- [`autotest.py`](../tools/pensee/autotest.py) — T166, 169/169.
- [`pensee-spans.json`](pensee-spans.json) — les catégories.
