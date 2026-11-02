# B13 — le lien automatique : 0/5, le sujet ne suffit pas

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **135/135 portes** : le **lien automatique** (la phrase précédente qui partage le **sujet** de
> la question) retrouve **0/5** des paires. Ce n'est pas un bug : dans le gold, les assertions
> (`r423`–`r427`) sont **après** les questions (`r418`–`r422`) — le lien par le sujet ne peut pas
> trouver une phrase qui **suit**. La mesure le dit, et c'est le résultat.
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-lien-auto.json`](pensee-lien-auto.json).

## 1. Le lien

| mesure | valeur |
|---|---:|
| paires (question, assertion) | 5 |
| précédente trouvée par le **sujet** | **0** |
| taux | 0,0000 |

**Ce que ça dit** :

- **Le lien par le sujet ne suffit pas** : les 5 assertions sont placées **après** les questions
  dans le gold ; `trouver_precedente` ne cherche que dans le passé — il ne trouve rien.
- **Le contexte du round précédent était donc un artefact** : la paire était codée par l'**index**
  (r418↔r423), pas par un lien réel ; c'est le **contrôle négatif** du 5/5.
- **La leçon** : un lien automatique doit être **mesuré** sur un corpus où il peut être faux ;
  le 5/5 du contexte n'était qu'une convention.
- **Le gold n'a pas de lien** : il n'y a pas de champ `precedente` — le corpus n'a pas été
  construit pour ce test.

## 2. Ce que ce banc ne dit pas

- **Le sujet partagé** marcherait si les assertions précédaient ; c'est un problème d'**ordre du
  corpus**, pas de règle.
- **5 paires** : un échantillon.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 607** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **l'ordre des phrases** dans le gold : il rend le test impossible, pas la règle fausse ;
- **le lien par le sujet** est naïf (les pronoms) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Réordonner le gold** : mettre les assertions **avant** les questions pièges, et re-mesurer
   le lien automatique (attendu > 0).
2. **Le neuronal réel** : toujours bloqué ; c'est lui qui trancherait le sens.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `trouver_precedente`, `fidelite_lien_auto`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — l'ordre actuel.
- [`autotest.py`](../tools/pensee/autotest.py) — T132, 135/135.
- [`pensee-lien-auto.json`](pensee-lien-auto.json) — le lien.
