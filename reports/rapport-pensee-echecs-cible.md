# B13 — les 22 échecs de l'attachement ciblé : 11 hors candidats, 11 mal classés

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **175/175 portes** : sur les 145 segments au bon span, **123** ont la bonne cible et **22** ne
> l'ont pas. Ces 22 se partagent en **11 cibles absentes des candidats** et **11 cibles présentes
> mais non choisies**. Les absences sont surtout des **verbes anglais hors lexique** (`fly`,
> `climbs`, `flows`, `swims`, `get`, `smiles`, `wait`) et quelques **noms que le GP complète**
> (`chat` de « de la voisine »).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-echecs-cible.json`](pensee-echecs-cible.json).

## 1. La répartition

| catégorie | nombre |
|---|---:|
| cible **absente** des candidats | **11** |
| cible **présente** mais non choisie | **11** |
| **tout** | **22** |

Par type et nature (segments au bon span) :

| type | cible nom | cible verbe | hors candidats |
|---|---:|---:|---:|
| GP | 14 | 0 | 10 |
| SUB | 5 | 3 | 1 |
| REL | 0 | 0 | 0 |

**Ce que ça dit** :

- **Les absences sont un problème de lexique** : `fly`, `climbs`, `flows`, `swims`, `get`,
  `smiles`, `wait` ne sont pas dans `VERBES_CONNUS` ; `_verbe_dans` retombe alors sur le dernier
  mot (`lake`, `roof`, `sea`…).
- **Les noms que le GP complète** (`de la voisine` → `chat`) demandent une autre règle : le GP
  génitif se rattache au **nom qu'il complète**, pas au verbe — le gold le sait, la règle non.
- **11 cibles sont dans les candidats** : le classement n'est pas encore résolu (le choix du bon
  candidat demanderait un modèle, pas une règle).
- **La négative est explicite** : 22/145 restent faux, et 11 d'entre eux sont hors de portée
  d'une règle de proximité.

## 2. Ce que ce banc ne dit pas

- **Les 11 « présents »** : lequel des candidats est le bon n'est pas appris.
- **Les verbes anglais** : leur ajout au lexique **après** la mesure serait un ajustement au gold
  (fuite de test) — ils sont donc laissés dehors, comme mesure de couverture.
- **Le top-k est lenient** (sous-chaînes).
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 3. Ce qui pourrait rendre cette fiche fausse

- **la classification `_est_verbe`** sert à la fois de règle et de lecture des échecs ;
- **les 11 absents** incluent des noms, pas seulement des verbes ;
- **le gold** : 612 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le classement appris** : choisir parmi les candidats (le vrai levier des 11).
2. **Le GP génitif** : le nom qu'il complète (les 10 absents de type GP).
3. **Les subordonnées** : demander à S (81 spans).
4. **Politique DRVM/native** : quand les poids seront là.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `_verbe_dans`, `_tete_nom`.
- [`autotest.py`](../tools/pensee/autotest.py) — T172, 175/175.
- [`pensee-echecs-cible.json`](pensee-echecs-cible.json) — la répartition.
