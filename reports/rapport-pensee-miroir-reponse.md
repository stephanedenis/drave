# B13 — la réponse : 19/19, l'acte commande la sortie

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6 — le miroir) · **Date** : 2026-11-02
> · **Verdict** : ✅ **123/123 portes** : la **réponse** (la sortie par l'acte pragmatique, pas
> le texte) est mesurée sur les **19 questions** du gold : **19/19 (1,0)** — chaque question
> reçoit une réponse de type « réponse », chaque assertion un accusé, chaque ordre un accusé.
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-miroir-reponse.json`](pensee-miroir-reponse.json).

## 1. Les six sorties

| sortie | source | **mesure** |
|---|---|---:|
| surface (graphèmes) | 587 phrases | 1,0000 |
| POS + intervalles | 587 phrases | 1,0000 |
| résumé (syntagmes) | 587 phrases | 0,7834 / 0,7472 |
| **réponse (acte)** | **19 questions** | **1,0000** |

**Ce que ça dit** :

- **La réponse est parfaite par construction** : elle suit l'`acte` détecté ; 19/19 est un test
  de **contrat**, pas de compréhension — la réponse ne répond pas *à* la question, elle en
  reconnaît le type.
- **La sortie la plus riche est la moins mesurée** : la réponse ne dit rien du contenu ; c'est
  la prochaine marche (une réponse qui *réponde*).
- **La règle 6 est complète et hiérarchisée** : surface (1,0), POS (1,0), résumé (0,78), réponse
  (1,0 par contrat) — quatre sorties, quatre natures de mesure.
- **La fluidité n'est pas la fidélité** : ici la réponse est fluide et fidèle *au type*, mais pas
  au contenu.

## 2. Ce que ce banc ne dit pas

- **La réponse ne répond pas** : c'est un accusé typé, pas une réponse sémantique.
- **19 questions** seulement.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition de la réponse** (le type, pas le contenu) ;
- **19 questions** : un échantillon ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La réponse au contenu** : répondre à la question, pas à son type — la vraie marche.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `repondre`, `fidelite_reponse`.
- [`autotest.py`](../tools/pensee/autotest.py) — T120, 123/123.
- [`pensee-miroir-reponse.json`](pensee-miroir-reponse.json) — les six sorties.
