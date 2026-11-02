# B13 — les vrais absents : 5 phrases sans antécédent, 0 lien

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **140/140 portes** : cinq phrases à **pronom sans antécédent** (`Il pleut.`, `On dit que c'est
> vrai.`, `Elle est partie.`, `Ils sont arrivés.`, `It rains.`) entrent dans le gold
> (**432 phrases réelles**). Elles ne produisent **aucun lien** : le `coref` du gold n'est pas
> renseigné pour elles, et `resoudre_meta` ne les voit pas. Le **vrai** absent n'est pas mesuré —
> il est **absent du gold**.
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-vrais-absents.json`](pensee-vrais-absents.json).

## 1. Les 5 phrases

| phrase | pronom | antécédent | **lien produit** |
|---|---|---|---|
| `Il pleut.` | il | aucun | **non** |
| `On dit que c'est vrai.` | on | aucun | **non** |
| `Elle est partie.` | elle | aucun | **non** |
| `Ils sont arrivés.` | ils | aucun | **non** |
| `It rains.` | it | aucun | **non** |

| mesure | valeur |
|---|---:|
| phrases réelles | **432** |
| liens de coréférence | **116** (inchangé) |
| absents mesurés | **0** |

**Ce que ça dit** :

- **Le vrai absent n'est pas dans le gold** : les 5 phrases n'ont pas de `coref` ; la mesure ne
  peut pas les compter — le corpus ne porte pas l'annotation « pas d'antécédent ».
- **Le lien est stable** (116) : les phrases ajoutées n'ont pas de pronom lié, elles ne changent
  rien aux classes (51/65/0).
- **La limite est dans l'annotation, pas dans la règle** : pour mesurer les absents, il faut un
  champ `coref: {}` **explicite** (l'absence est une information, pas un vide).
- **La négative est explicite** : 0 absent mesuré, 5 absents réels non mesurés.

## 2. Ce que ce banc ne dit pas

- **Le pronom `on`** est un indéfini : il n'a pas d'antécédent par nature, ce n'est pas une
  anaphore.
- **432 phrases** ; le réel donne les mêmes ordres.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 612** (432 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **l'absence de champ `coref`** n'est pas distinguée de « pas encore annoté » ;
- **les 5 phrases** sont un échantillon ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Annoter l'absence** : `coref: {}` explicite + un champ `sans_antecedent: true` — puis
   mesurer les vrais absents (attendu 5).
2. **Le neuronal réel** : toujours bloqué.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `liens_absents`, `classer_liens_coref`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — les 5 phrases (r428–r432).
- [`autotest.py`](../tools/pensee/autotest.py) — T137, 140/140.
- [`pensee-vrais-absents.json`](pensee-vrais-absents.json) — l'état.
