# B13 — les 127 échecs qualifiés : 94 de span, 33 de cible

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **166/166 portes** : les **127 échecs** de l'attachement se répartissent en **94 de span**
> (aucun segment prédit au même span) et **33 de cible** (le span est bon, la cible n'est pas
> dans les candidats). Le correctif testé — ajouter les GV du chunker aux GV du générateur S et
> remplir les segments d'union — ne répare **qu'un** des 33. Les 32 autres ont un GV qui couvre
> **toute la phrase** : le dernier token n'est pas le verbe (`… in the park` → `park`, pas `saw`).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-echecs-attachement.json`](pensee-echecs-attachement.json).

## 1. La répartition

| cause | nombre | part |
|---|---:|---:|
| **span faux** (aucun segment prédit au même span) | **94** | 74,0 % |
| **cible hors des candidats** (span bon) | **33** | 26,0 % |
| **tout** | **127** | 100 % |

| mesure | avant ce round | **après le correctif d'union** |
|---|---:|---:|
| top1 | 95 (0,3975) | **96 (0,4017)** |
| top-k | 112 (0,4686) | **113 (0,4728)** |
| exact | 13 (0,0544) | **14 (0,0586)** |
| tête top1 | 94 (0,6483) | **96 (0,6621)** |
| tête top-k | 111 (0,7655) | **113 (0,7793)** |

**Ce que ça dit** :

- **Le span est le premier levier** (94/127) : la segmentation ne produit pas le segment au bon
  span — c'est un problème de découpage, pas d'attachement.
- **La cible est le second** (33/127) : sur les 33, **32** viennent d'un GV qui couvre la phrase
  entière ; la règle « dernier token du GV » y prend un nom (`park`) au lieu du verbe (`saw`).
- **Le correctif d'union ne rend qu'un point** : il comble les segments d'union sans GV, mais pas
  le cas du GV-phrase. Le gain est réel mais marginal — et la fiche le dit.
- **La négative est explicite** : 32 des 33 restent faux ; ce round ne les répare pas.

## 2. Ce que ce banc ne dit pas

- **Les 94 spans** : leurs causes ne sont pas qualifiées (S, chunker, ou les deux).
- **L'identification du verbe** dans un GV-phrase : elle manque (pas de lexique verbal dans le
  chunker, pas de `cible_verbe` pour ces phrases).
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.
- **Le coût** : l'analyse complète du gold à chaque porte (quelques secondes).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le dénominateur** : 239 cibles, dont 94 sans segment prédit au même span ;
- **la définition de l'échec** : un span faux n'est pas une cible fausse ;
- **le gold** : 612 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le verbe du GV-phrase** : choisir le verbe (pas le dernier token) — le vrai correctif des 32.
2. **Les 94 spans** : qualifier la segmentation (S ou chunker).
3. **Le générateur S** : les passifs.
4. **Politique DRVM/native** : quand les poids seront là.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — union : GV et cible.
- [`autotest.py`](../tools/pensee/autotest.py) — T163, 166/166.
- [`pensee-echecs-attachement.json`](pensee-echecs-attachement.json) — la répartition.
