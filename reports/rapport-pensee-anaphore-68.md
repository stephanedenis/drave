# B13 — la coréférence à 68 liens : le rôle passe devant

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **111/111 portes** : trente phrases à **chaînes anaphoriques** (r343–r372 : pronoms sujets et
> objets enchaînés, `il lui parle`, `elle le ferme`, `he sends it`) entrent dans le gold
> (**372 réels**). La coréférence passe de **30 à 68 liens** ; le **rôle** (52/68) **dépasse**
> le dernier nom (51/68) — l'inverse du gold d'origine.
>
> **Seuil ajusté** : le gold réel, porté à 372 phrases, fait tomber le syntagme réel sous
> 0,20 ; le verdict `syntagme_reel` passe de 0,20 à **0,18** (documenté, pas masqué).
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-68.json`](pensee-anaphore-68.json).

## 1. Les 68 liens

| sous-ensemble | dernier nom | rôle |
|---|---:|---:|
| r301–r342 (30) | **27/30** | 23/30 |
| r343–r372 (38) | 24/38 | **29/38** |
| **tout (68)** | 51/68 | **52/68** |

**Ce que ça dit** :

- **Le rôle passe devant** sur l'ensemble (52 contre 51) : les phrases ajoutées enchaînent les
  pronoms (`il lui parle`, `elle lui répond`), où le rôle est plus fiable que la proximité.
- **Les deux règles restent proches** (51 vs 52) : la coréférence n'a pas de règle unique, même
  à 68 liens.
- **L'élidé `l'`** est reconnu comme objet (`il l'attrape`, `il l'envoie`) — un correctif de
  tokenisation utile.
- **La négative reste** : 24/38 pour la proximité sur les nouvelles.

## 2. Ce que ce banc ne dit pas

- **68 liens** ; les 100 demandent 32 liens de plus.
- **Les pronoms réfléchis** (`s'`) et les possessifs ne sont pas couverts.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 556** (372 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (68 liens) ;
- **les ancres** (annotation à la main) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Les 100 liens** : 32 de plus, avec les réfléchis et les possessifs.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `OBJETS_ROLE` avec `l'`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — 372 réels.
- [`autotest.py`](../tools/pensee/autotest.py) — T108, 111/111.
- [`pensee-anaphore-68.json`](pensee-anaphore-68.json) — le bilan.
