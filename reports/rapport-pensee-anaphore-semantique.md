# B13 — la sémantique des verbes : 23/30, la table ne bat pas le dernier nom

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **102/102 portes** : la **table sémantique** des verbes (intransitifs → proximité, transitifs →
> rôles) est mesurée. Elle fait **23/30** — moins bien que le dernier nom (**27/30**) et que
> l'hybride (24/30). La conclusion des quatre règles est nette : **le dernier nom est le
> meilleur** sur ce gold.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-semantique.json`](pensee-anaphore-semantique.json).

## 1. Les quatre règles

| sous-ensemble | dernier nom | rôle | hybride | **sémantique** |
|---|---:|---:|---:|---:|
| r301–r336 (court) | **20/20** | 14/20 | 15/20 | 15/20 |
| r337–r342 (long) | 7/10 | 9/10 | 9/10 | 8/10 |
| **tout** | **27/30** | 23/30 | 24/30 | 23/30 |

**Ce que ça dit** :

- **La table ne bat pas la proximité** : l'`il` de r321 reprend `chien` (proximité), pas `chat`
  (agent) ; la table sémantique se trompe dans les deux sens.
- **Les erreurs changent** : la sémantique corrige r337/r339/r341 (les longues) mais casse
  r321/r322/r323 (les courtes) — le **désaccord** est le même qu'entre rôle et proximité.
- **Le meilleur reste le dernier nom** (27/30) : sur ce gold, la règle la plus simple gagne.
- **La négative est explicite** : 23/30 < 27/30.

## 2. Ce que ce banc ne dit pas

- **30 liens** ; 100 donneraient une courbe.
- **Le gold est petit et hétérogène** : les quatre règles ne s'accordent pas sur les mêmes cas.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 522** (342 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (30 liens) ;
- **la table sémantique** (écrite à la main, incomplète) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le dernier nom comme règle de référence** : 27/30 ; documenter l'écart comme **limite du gold**, pas de la règle.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `resoudre_semantique`, `mesurer_semantique`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `coref` sur 32 phrases.
- [`autotest.py`](../tools/pensee/autotest.py) — T99, 102/102.
- [`pensee-anaphore-semantique.json`](pensee-anaphore-semantique.json) — le bilan.
