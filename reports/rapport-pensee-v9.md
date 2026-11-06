# B13 — la garde PRON : exact 219/219 (1,0000), couverture 0,9163, F1 0,5822

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
> **État courant** · **Verdict** : ✅
> **183/183 portes** : trois corrections issues de l'audit A19 réparent les **7 régressions** de la
> fiche [R1/R3](rapport-pensee-r1r3.md) et rouvrent trois spans : **la garde PRON** (A17 R1a
> fidèle : un pronom n'est jamais un verbe par position), **`est_sub`** (subordonnants par langue
> dans **toutes** les branches, pas seulement la branche REL/SUB) et **`predicat_vu`** pour
> l'adverbe final. Résultat : **219 labels** sur 239, **exact 219/219 = 1,0000** (fr **134/134**,
> en **85/85**), **couverture 0,9163**, **F1 0,5822** (union ; S 0,5006, chunker 0,6178), tête
> **0,7381** ; **20 spans** restants (9 REL, 6 SUB, 5 GP). **dev 152/152, test 67/67.**
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`est_verbe` garde PRON,
> `est_sub`, boucle REL/SUB), [`autotest.py`](../tools/pensee/autotest.py) (23 assertions) ;
> JSON [`pensee-v9.json`](pensee-v9.json).

## 1. Les trois corrections

| # | correction | effet |
|---|---|---|
| 1 | **garde PRON** (A17 R1a fidèle) : dans `est_verbe`, un mot pronominal n'est **jamais** un verbe par la règle de position | répare les 6 REL françaises perdues (`r273`, `s032`, `s069`, `s072`, `s115`, `s135`) |
| 2 | **`est_sub`** : les subordonnants sont conditionnés par la langue dans **toutes** les branches (GN, GP, REL/SUB) ; « car » n'arrête plus un GN anglais | r280 (« The car that I bought ») |
| 3 | **`predicat_vu`** dans la règle de l'adverbe final (au lieu de `verbes_vus`, qui ne compte pas un verbe après auxiliaire) | g017 (« that she would come ») |

## 2. Avant / après

| mesure | v8 (f908d7b0) | **v9** |
|---|---:|---:|
| labels au bon span | 212 | **219** |
| **exact / labels** | 212/212 (1,0000) | **219/219 (1,0000)** |
| **couverture** | 0,8870 | **0,9163** |
| F1 syntagmes (gelé 602) | 0,5763 | **0,5822** |
| S / chunker | 0,4966 / 0,6057 | **0,5006 / 0,6178** |
| tête (gelé 602) | 0,7316 | **0,7381** |
| français | 129/129 | **134/134** |
| anglais | 83/83 | **85/85** |
| spans perdus | 27 | **20** (9 REL, 6 SUB, 5 GP) |
| top-k | 211 | **218/239 (0,9121)** |
| dev / test | 148/148, 64/64 | **152/152, 67/67** |

**Ce que ça dit** :

- **Les 7 régressions de la v8 sont réparées** : la garde PRON est la bonne forme de R1a (A17
  l'avait écrite, la v8 l'avait simplifiée en retirant les relatifs de `SUJETS`).
- **Tous les compteurs montent** : labels, couverture, F1, tête, les deux langues, dev/test.
- **Les 20 spans restants** : 9 REL, 6 SUB, 5 GP ; 17 étaient déjà inatteignables (lexique
  synthétique, gold sans préposition), 3 gains de A17 (`r153`, `r255`, `r264`) restent à prendre.
- **Le top-k suit** (218/239 = 0,9121) : les candidats contiennent la cible pour 99,5 % des
  labels prédits.

## 3. Contrôle négatif

Le dispositif de la fiche [R1/R3](rapport-pensee-r1r3.md) (audit A19) s'applique : **permutation
globale des cibles** (2000 tirages) → **2,04/212** (0,96 %) contre 212/212, p = 0 ; candidat
aléatoire → 35,9 % de top-1. Ici, l'exact est **219/219** : la marge est du même ordre.

## 4. Ce que ce banc ne dit pas

- **Les 20 spans** : non prédits, donc hors mesure d'attachement.
- **L'in-sample** : les règles sont dessinées sur ce gold ; dev/test (152/152, 67/67) limitent
  mais n'excluent pas l'ajustement.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 5. Ce qui pourrait rendre cette fiche fausse

- **la garde PRON** dépend de la liste de pronoms fermée ;
- **`est_sub`** : « car » est un nom anglais, mais « since/before/after » restent ambigus ;
- **le français** perd un label (135 → 134) sans perdre d'exact : à surveiller ;
- un **audit** qui ne vérifie pas ces mesures (voir [audit R1/R3](rapport-audit-r1r3.md)).

## 6. La suite

1. **Les 20 spans** : `r153` (garde déterminant GP), `r255`/`r264` (lexique/tokenisation), les
   17 inatteignables.
2. **dev/test** : re-mesurer après cette fiche.
3. **Le merge `master`** si autorisé.
4. **Politique DRVM/native** : quand les poids seront là.

## 7. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — les trois corrections.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`rapport-audit-r1r3.md`](rapport-audit-r1r3.md) — l'audit A19 (ablations, 7 régressions).
- [`pensee-v9.json`](pensee-v9.json) — les chiffres.
