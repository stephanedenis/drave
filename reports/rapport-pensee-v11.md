# B13 — les deux dernières régressions : exact 221/221 (1,0000), couverture 0,9247, 18 spans

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-06 ·
> **État courant** · **Verdict** : ✅
> **183/183 portes** : les deux régressions ouvertes par l'[audit v10](rapport-audit-v10.md) sont
> corrigées — **`s037`** (une relative en tête était classée SUB par R2) et **`r303`** (« car il
> est tard » : la règle de l'adverbe final coupait avant `tard`). L'adverbe final est **retiré**
> (arbitrage : `g017` est perdu, `r303` et `r264` gagnés, net **+1**). Résultat : **221 labels**
> sur 239, **exact 221/221 = 1,0000** (fr **136/136**, en **85/85**), **couverture 0,9247**,
> **F1 0,5843** (union), **18 spans** (9 REL, 5 SUB, 4 GP), **top-k 220/239 (0,9205)** ;
> **dev 152/152 (0,9325)**, **test 69/69 (0,9079)** — l'écart dev/test d'exactitude est **nul**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (R2, adverbe final),
> [`autotest.py`](../tools/pensee/autotest.py) (14 assertions) ; JSON [`pensee-v11.json`](pensee-v11.json).

## 1. Les deux corrections

| # | correction | effet |
|---|---|---|
| 1 | **R2** : un **subordonnant** ouvre une SUB ; une **relative en tête** reste une REL (`Paul qui marche`) | s037 |
| 2 | **l'adverbe final est retiré** : il coupait `car il est tard` (r303) et `qu'il vient demain` (r264) ; il ne servait qu'à `g017` | r303, r264 (−g017) |

## 2. Avant / après

| mesure | v10 | **v11** |
|---|---:|---:|
| labels au bon span | 220 | **221** |
| **exact / labels** | 220/220 | **221/221 (1,0000)** |
| **couverture** | 0,9205 | **0,9247** |
| F1 syntagmes (612) | 0,5843 | **0,5843** |
| français | 134/134 | **136/136** |
| anglais | 86/86 | **85/85** |
| spans perdus | 19 | **18** (9 REL, 5 SUB, 4 GP) |
| top-k | 219 | **220/239 (0,9205)** |
| dev / test | 152/152, 68/68 | **152/152, 69/69** |

**Ce que ça dit** :

- **18 spans restants** : **17 inatteignables** (12 formes synthétiques, 4 GP du gold sans
  préposition, la tokenisation `qu'il`) + **g017** (arbitrage de l'adverbe final, assumé).
- **Le français gagne 2 labels** (136/136), l'anglais en perd 1 (85/85) : le solde est +1.
- **La couverture 0,9247** est le plafond : le rendement global est 221/239.

## 3. Contrôle négatif

Le dispositif de l'[audit A19](rapport-audit-r1r3.md) s'applique (permutation globale des cibles :
2,04/212, p = 0). Ici 221/221 : la marge est du même ordre.

## 4. Ce que ce banc ne dit pas

- **Les 18 spans** : non prédits.
- **L'in-sample** : les règles sont dessinées sur ce gold.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 5. Ce qui pourrait rendre cette fiche fausse

- **l'arbitrage de l'adverbe** (g017 perdu) est un choix, pas une vérité ;
- **la règle R2** dépend de la liste des subordonnants par langue ;
- un **audit** qui ne vérifie pas ces mesures (voir [audit v10](rapport-audit-v10.md)).

## 6. La suite

1. **Les 18 spans** : les 17 inatteignables (gold, lexique), `g017`.
2. **dev/test** : re-mesurer (vague 7).
3. **Politique DRVM/native** : quand les poids seront là.

## 7. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — R2 et l'adverbe final.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`pensee-v11.json`](pensee-v11.json) — les chiffres.
