# B13 — 222/222 (1,0000) : le dernier marqueur ambigu, et 17 spans inatteignables

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-06 ·
> **État courant** · **Verdict** : ✅ — **la cible de A17 est atteinte**.
> **183/183 portes** : le dernier écart était un **marqueur ambigu** — « when » après un GN est
> une **relative** (« The day when we left »), ailleurs une **subordonnée** (« When it rains »).
> Résultat : **222 labels** sur 239, **exact 222/222 = 1,0000** (fr **136/136**, en **86/86**),
> **couverture 0,9289**, **F1 0,5893** (union ; S 0,5014, chunker 0,6203), tête **0,7392** ;
> **17 spans** restants (8 REL, 5 SUB, 4 GP) — **tous inatteignables** sans corriger le gold ou
> le lexique (12 formes synthétiques, 4 GP du gold sans préposition, une tokenisation `qu'il`).
> **dev 153/153, test 69/69.**
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`AMBIGUES_REL`,
> branche REL/SUB), [`autotest.py`](../tools/pensee/autotest.py) (16 assertions) ;
> JSON [`pensee-v12.json`](pensee-v12.json).

## 1. La correction

| # | correction | effet |
|---|---|---|
| 1 | **`AMBIGUES_REL`** (`when`, `where`, `why`, `how`, `quand`, `où`, `pourquoi`, `comment`) : **REL après un GN**, **SUB** ailleurs | r241 (« The day when we left ») — le dernier écart |

## 2. Avant / après

| mesure | v11 | **v12** |
|---|---:|---:|
| labels au bon span | 221 | **222** |
| **exact / labels** | 221/221 | **222/222 (1,0000)** |
| **couverture** | 0,9247 | **0,9289** |
| F1 syntagmes (union, 602) | 0,5843 | **0,5893** |
| tête | 0,7330 | **0,7392** |
| français | 136/136 | **136/136** |
| anglais | 85/85 | **86/86** |
| spans perdus | 18 | **17** (8 REL, 5 SUB, 4 GP) |
| top-k | 220 | **221/239 (0,9247)** |
| dev / test | 152/152, 69/69 | **153/153, 69/69** |

**Ce que ça dit** :

- **Les 17 spans restants sont inatteignables** : 12 formes synthétiques (le lexique du gold
  synthétique n'est pas celui du bloc — les ajouter serait ajuster au test), 4 GP du gold sans
  préposition (défaut du générateur), une tokenisation (`qu'il`).
- **L'attachement ne peut plus progresser que par la couverture**, et la couverture par le gold
  ou le lexique — pas par une règle.
- **dev 153/153 et test 69/69** : l'exactitude est parfaite dans les deux moitiés.

## 3. Contrôle négatif

Le dispositif de l'[audit A19](rapport-audit-r1r3.md) s'applique : **permutation globale des
cibles** (2000 tirages) → **1,997/220** (0,908 %) contre l'observé, p = 0 ; candidat aléatoire
→ 42,14 % de top-1. Ici **222/222** : la marge est du même ordre.

## 4. Ce que ce banc ne dit pas

- **Les 17 spans** : non prédits, donc hors mesure d'attachement.
- **L'in-sample** : les règles sont dessinées sur ce gold ; dev/test limitent sans exclure.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 5. Ce qui pourrait rendre cette fiche fausse

- **les 12 formes synthétiques** : le lexique du gold n'est pas celui du bloc, et c'est le gold
  qui a raison dans la mesure — c'est une limite de **couverture du lexique**, pas d'attachement ;
- **le marqueur ambigu** dépend de la liste `AMBIGUES_REL` ;
- un **audit** qui ne vérifie pas ces mesures (voir [audit v10](rapport-audit-v10.md)).

## 6. La suite

1. **Les 17 spans** : corriger le gold (GP sans préposition) et étendre le lexique réel, ou les
   accepter comme couverture du gold.
2. **Politique DRVM/native** : quand les poids seront là.

## 7. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `AMBIGUES_REL`.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`pensee-v12.json`](pensee-v12.json) — les chiffres.
