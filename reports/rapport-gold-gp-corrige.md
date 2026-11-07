# B13 — le gold corrigé : 4 GP retrouvés, exact 226/226, couverture 0,9456

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Un défaut du générateur de gold**, pas du bloc : dans le mode `sv` de
> `gold_synthetique.py`, le span d'un GP partait **après** la préposition (`i = v + index(prep) + 1`)
> alors que le mode `sv_gp` l'inclut (`i - 1`). Quatre GP du gold étaient donc **sans préposition** —
> inatteignables par construction. Corrigé, le gold garde **les mêmes 160 phrases** (mêmes ids,
> mêmes segments) et **4 GP** sont réparés : l'attachement passe de **222/222 à 226/226**,
> la **couverture de 0,9289 à 0,9456**, les **spans perdus de 17 à 13** (les 4 GP ont disparu de
> la liste). **dev 155/155, test 71/71.**
>
> **Dispositif** : [`gold_synthetique.py`](../tools/tests/linguistique/gold_synthetique.py) (mode
> `sv`), [`gold_synthetique.json`](../tools/tests/linguistique/gold_synthetique.json) régénéré
> (graine 42, 160 phrases), [`autotest.py`](../tools/pensee/autotest.py) (14 assertions) ;
> JSON [`pensee-gold-gp-corrige.json`](pensee-gold-gp-corrige.json).

## 1. Le défaut

```python
# avant (mode sv) : le span commence après la préposition
i = v + [t[0] for t in gv].index(prep) + 1
segs.append(("GP", i, i + len(g), ...))     # « les jardin », sans « avec »
# après : le GP inclut sa préposition, comme le mode sv_gp
i = v + [t[0] for t in gv].index(prep)
segs.append(("GP", i, i + 1 + len(g), ...)) # « avec les jardin »
```

Les 4 GP corrigés : `s027` (31 → 26), `s146` (25 → 20), `s148` (20 → 15), `s160` (20 → 15).

## 2. Avant / après

| mesure | avant | **après** |
|---|---:|---:|
| exact / labels | 222/222 | **226/226** |
| **couverture** | 0,9289 | **0,9456** |
| spans perdus | 17 (8 REL, 5 SUB, 4 GP) | **13 (8 REL, 5 SUB, 0 GP)** |
| dev / test | 153/153, 69/69 | **155/155, 71/71** |
| F1 syntagmes | 0,6181 | 0,6198 |

**Ce que ça dit** :

- **Le défaut était dans l'instrument**, pas dans la règle : aucun code du bloc n'a changé pour ces
  4 GP.
- **Les 13 spans restants** sont 9 synthétiques (REL/SUB dont les verbes sont hors du lexique du
  bloc — un choix de lexique, pas une règle) et 4 réels (`r035` relative zéro, `r255` « roule » hors
  lexique, `r264` tokenisation `qu'il`, `g017` arbitrage d'adverbe).
- **La couverture 0,9456** est le nouveau plafond : 13 cibles n'ont pas de segment au bon span.

## 3. Contrôle négatif

Les **160 phrases** sont identiques (mêmes ids, mêmes textes, mêmes nombres de segments) : seule la
borne des 4 GP change. Un test de non-régression le vérifie (comparaison des segments avant/après
sur les 160 phrases).

## 4. Ce que ce banc ne dit pas

- **Les 9 synthétiques** : ils demandent une décision de lexique (les ajouter serait ajuster au
  test) — non tranchée ici.
- **Les 4 réels** : chacun est un cas isolé (relative zéro, lexique, tokenisation, arbitrage).
- **Les mesures antérieures** : les fiches v12 et antérieures publient 222/222 et 17 spans — ce
  sont des **instantanés** de leur commit, pas l'état courant.

## 5. Ce qui pourrait rendre cette fiche fausse

- **le générateur** : d'autres modes peuvent avoir le même défaut (non audités) ;
- **la graine** : le gold est régénéré à graine 42 ; un changement de graine change les phrases ;
- **le JSON committé** : c'est lui que lisent les mesures, pas le générateur.

## 6. La suite

1. **Trancher les 9 synthétiques** (lexique disjoint) : les exclure de la mesure ou étendre le
   lexique, avec la mention du choix.
2. **Les 4 réels** : `r035` (relative zéro), `r255` (« rouler »), `r264` (élision), `g017` (adverbe).
3. **Auditer les autres modes** du générateur (le même défaut de borne peut s'y cacher).

## 7. Fichiers

- [`gold_synthetique.py`](../tools/tests/linguistique/gold_synthetique.py) — la correction.
- [`gold_synthetique.json`](../tools/tests/linguistique/gold_synthetique.json) — régénéré.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`pensee-gold-gp-corrige.json`](pensee-gold-gp-corrige.json).
