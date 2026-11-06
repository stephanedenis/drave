# B13 — 220/220 (1,0000), couverture 0,9205 : le féminin `-ée` et la garde déterminant du GP

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
> **Instantané historique** : état au commit `710ec7f9` · **Verdict** : ✅ chiffres, ⚠️ attribution corrigée
> **183/183 portes** : **une seule** des deux corrections annoncées est **effective** — la
> **garde déterminant** du GP (A17 R3b : un « verbe » précédé d'un déterminant est un nom,
> `for the bus`), **+1 exact** (`r153`). Le **féminin `-ée`** est **inerte sur ce gold** (0
> différence d'annotation ; `r255` reste absent car `acheter` n'est pas au lexique). L'attachement
> est à **220/220 (1,0000)** sur **220 labels** (sur 239), **couverture 0,9205**, **F1 0,5880**
> (gelé 602 ; 0,5843 vivant), tête **0,7388** ; **fr 134/134**, **en 86/86** ; **19 spans** dont
> **17 déjà inatteignables** + `s037` et `r303` (deux régressions, corrigées en v11).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_est_verbe`, boucle GP),
> [`autotest.py`](../tools/pensee/autotest.py) (19 assertions) ;
> JSON [`pensee-v10.json`](pensee-v10.json).

## 1. Les deux corrections

| # | correction | effet |
|---|---|---|
| 1 | **le féminin `-ée`** : `n[:-2] + "er"` dans le lexique (`achetée` → `acheter`) | r255 (le verbe de la relative) |
| 2 | **la garde déterminant du GP** (A17 R3b) : un mot « verbe » précédé d'un DET **dans le GP** est un nom | r153 (`for the bus`, `bus` est un verbe français) |

## 2. Avant / après

| mesure | v9 | **v10** |
|---|---:|---:|
| labels au bon span | 219 | **220** |
| **exact / labels** | 219/219 | **220/220 (1,0000)** |
| **couverture** | 0,9163 | **0,9205** |
| F1 syntagmes (union, 602) | 0,5822 | **0,5880** |
| S / chunker | 0,5006 / 0,6178 | **0,5014 / 0,6203** |
| tête | 0,7381 | **0,7388** |
| français | 134/134 | **134/134** |
| anglais | 85/85 | **86/86** |
| spans perdus | 20 | **19** (9 REL, 6 SUB, 4 GP) |
| top-k | 218 | **219/239 (0,9163)** |

**Ce que ça dit** :

- **19 spans restants** : 17 sont inatteignables (lexique synthétique, gold sans préposition,
  tokenisation `qu'il`), `r255` (le lexique ne connaît pas `acheter`) et `r264` (élision `qu'il`).
- **Le français est à 134/134 et l'anglais à 86/86** : l'attachement est parfait dans les deux
  langues sur les labels prédits.
- **La couverture (0,9205)** est désormais le seul levier : le rendement global est
  220/239 = 0,9205.

## 3. Contrôle négatif

Le dispositif de l'[audit A19](rapport-audit-r1r3.md) s'applique (permutation globale des
cibles : 2,04/212, p = 0). Ici l'exact est 220/220 : la marge est du même ordre.

## 4. Ce que ce banc ne dit pas

- **Les 19 spans** : non prédits.
- **L'in-sample** : les règles sont dessinées sur ce gold.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 5. Ce qui pourrait rendre cette fiche fausse

- **la garde déterminant** peut empêcher un vrai verbe d'arrêter un GP (« de la voir ») ;
- **le `-ée`** peut créer un faux verbe (« idée » → « ider ») ;
- un **audit** qui ne vérifie pas ces mesures (voir [audit R1/R3](rapport-audit-r1r3.md)).

## 6. La suite

1. **Les 19 spans** : `r255`/`r264`, puis les 17 inatteignables.
2. **dev/test** : re-mesurer après ces corrections.
3. **Politique DRVM/native** : quand les poids seront là.

## 7. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — les deux corrections.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`pensee-v10.json`](pensee-v10.json) — les chiffres.
