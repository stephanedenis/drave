# B13 — la ponctuation a une POS (PONCT) : POS 85,75 %, miroir 0,2276

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Le P1-6 de l'audit produit** : la **ponctuation** n'avait aucun POS (25 tokens du gold,
> 257 dans les textes libres). Elle est désormais **PONCT** (0,95) ; le POS passe de **0,8500 à
> **0,8575** et le **miroir** (la fidélité de sortie) de **0,196 à 0,2276**. F1 et attachement
> inchangés (0,6482 ; 235/236) ; **183/183**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`analyser`, typ
> `ponctuation`), [`autotest.py`](../tools/pensee/autotest.py) (5 assertions) ; JSON
> [`pensee-pos-ponctuation.json`](pensee-pos-ponctuation.json).

## 1. Ce que ça répare

| avant | après |
|---|---|
| `?`, `.`, `!` : aucun POS | **PONCT** (0,95) |
| 25 tokens du gold (P1) | 0 |
| miroir : fidélité de sortie 0,196 | **0,2276** |

**Les élisions** (`j'` → `je`, `l'` → `le`, `qu'` → `que`) sont aussi traitées : **neutre** sur le
gold (les tokens du gold ne sont pas les mêmes), gardé pour la robustesse.

## 2. Ce que ce banc ne dit pas

- **Le miroir** gagne parce que la ponctuation est **reconstruite** : ce n'est pas la qualité
  sémantique de la sortie, c'est sa **surface POS**.
- **Les particules** (`-t-il`, `-elle`) ne sont pas traitées.
- **Le gold** n'a que 25 tokens de ponctuation.

## 3. Ce qui pourrait rendre cette fiche fausse

- **PONCT** n'est pas dans `POS_FERME` : il est produit par la règle ;
- **le miroir** dépend de la définition de `fidelite_pos` (à relire).

## 4. La suite

1. **Les participes irréguliers** (testés : F1 −0,0023 → **non intégrés**).
2. **R4-fr filtré** (adjectif connu ou suffixe) : **intégré**, POS 85,75 → **85,84 %**.
3. **`que` CONJ vs PRON** : **intégré** (PRON après un nom, CONJ ailleurs) — POS 85,84 → **86,25 %**.

## 4 bis. Les règles **rejetées** (mesurées puis retirées)

| règle | effet | décision |
|---|---|---|
| participes irréguliers dans le lexique | F1 −0,0023 | retirée |
| **R4-fr générique** (toute copule) | 5/8 changements faux sur les textes libres | rejetée (A27) |
| **participe après `avoir`** (NOUN → VERB) | POS 86,25 → **86,06** (−0,19) : « Il a faim » | retirée |

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — PONCT et les élisions.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`pensee-pos-ponctuation.json`](pensee-pos-ponctuation.json).
