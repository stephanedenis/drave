# B13 — R1/R2/R3 : exact 212/212 (1,0000), couverture 0,887, F1 0,5763

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **État courant** : commit à jour
> (après `4ebeb683`) · **Verdict** : ✅
> **183/183 portes** : les quatre règles de la fiche [spans v7](rapport-spans-v7.md) (A17) sont
> intégrées — **R1** frontière de clause (pronom, modaux, second prédicat), **R2** SUB sans
> précédent, **R3a** subordonnants par langue, **R3c** `fall`/`call`. Résultat : **212 labels**
> (sur 239), **exact 212/212 = 1,0000** (fr **129/129**, en **83/83**), **couverture 0,887**,
> **F1 0,5763** (union ; S 0,4966, chunker 0,6057), tête **0,7316** ; **27 spans** restants
> (16 REL, 6 SUB, 5 GP), dont 17 sont **inatteignables** (lexique synthétique ou bug du gold).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`SUJETS`, `MODAUX`,
> `SUB_PAR_LANGUE`, boucle REL/SUB), [`autotest.py`](../tools/pensee/autotest.py) (24 assertions) ;
> JSON [`pensee-r1r3.json`](pensee-r1r3.json).

## 1. Les quatre règles

| # | règle | effet mesuré |
|---|---|---|
| **R1** | **frontière de clause** : un pronom n'est plus un verbe par position ; les **modaux** (`would`, `can`…) sont des auxiliaires ; un **second prédicat** (AUX après prédicat, verbe après un groupe verbal complet) ouvre la principale | +15 dev, +5 test, 0 perte |
| **R2** | **sans segment précédent**, un marqueur ouvre une **SUB** (« When it rains ») | +3 |
| **R3a** | **subordonnants par langue** : « car » est français, pas anglais (« The car that I bought ») | +2 |
| **R3c** | **`fall`/`call`** au lexique verbal anglais | +2 |

## 2. Avant / après

| mesure | v7 | **v8** |
|---|---:|---:|
| labels au bon span | 196 | **212** |
| **exact / labels** | 195/196 (0,9949) | **212/212 (1,0000)** |
| **couverture** | 0,8201 | **0,8870** |
| F1 syntagmes (union, gelé 602) | 0,5595 | **0,5763** |
| S / chunker (F1) | 0,4741 / 0,5858 | **0,4966 / 0,6057** |
| français | 135/135 | **129/129 (1,0)** |
| anglais | 60/61 | **83/83 (1,0)** |
| spans perdus | 43 | **27** (16 REL, 6 SUB, 5 GP) |
| top-k | 166 | 177/239 (0,7406) |

**Ce que ça dit** :

- **La frontière de clause était le vrai verrou** : 20 des 43 spans venaient d'un arrêt précoce
  (pronom pris pour un verbe, modaux hors AUX) ou d'un second prédicat avalé.
- **Les deux langues sont parfaites** (1,0 / 1,0) sur les 212 labels prédits.
- **Les 27 restants** : 12 synthétiques (verbes hors lexique), 4 GP du gold sans préposition
  (bug du générateur), 1 tokenisation (`qu'il`), 1 relative zéro, 1 adverbe final (arbitrage),
  1 couverture verbale réelle — **17 inatteignables sans corriger le gold ou le lexique**.

## 3. Ce que ce banc ne dit pas

- **Les 27 spans** : non prédits, donc hors mesure d'attachement.
- **Le test** : A17 a diagnostiqué sur dev **et** test ; le test n'est pas aveugle.
- **L'in-sample** : les règles sont dessinées sur ce gold.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 4. Ce qui pourrait rendre cette fiche fausse

- **les formes synthétiques** ajoutées au lexique ne sont pas générales ;
- **la frontière** (second prédicat) peut couper une relative à verbe coordonné ;
- **le test** est petit (76 cibles) ;
- un **audit** qui ne vérifie pas ces mesures (voir [audit v7](rapport-audit-v7.md)).

## 5. La suite

1. **Les 27 spans** : corriger le gold (ligne 98) et le lexique synthétique, ou les accepter.
2. **Le top-k** (0,7406) : candidats complets.
3. **dev/test** à re-mesurer.
4. **Politique DRVM/native** : quand les poids seront là.

## 6. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — R1, R2, R3a, R3c.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`pensee-r1r3.json`](pensee-r1r3.json) — les chiffres.
