# B13 — la restitution avec les intervalles : 1,0, la perte était le rendu

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6 — le miroir) · **Date** : 2026-11-02
> · **Verdict** : ✅ **121/121 portes** : la restitution **POS avec les intervalles d'origine**
> est **exacte (1,0)**. Le 0,201 du round précédent ne mesurait pas une perte d'information : il
> mesurait le **format** (`" ".join`), qui jette la ponctuation et les espaces. **L'information
> est dans l'annotation ; la perte est dans le rendu.**
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-miroir-espaces.json`](pensee-miroir-espaces.json).

## 1. Les quatre restitutions

| restitution | source | **fidélité** |
|---|---|---:|
| graphèmes (surface) | 587 phrases | 1,0000 |
| mots (tokens, `" ".join`) | 587 phrases | 0,2095 |
| POS (`" ".join`) | 587 phrases | 0,2010 |
| **POS + intervalles d'origine** | 587 phrases | **1,0000** |

**Ce que ça dit** :

- **Le bloc est restituif** : avec les `debut/fin`, la sortie POS redonne le texte exact ; la
  perte du 0,201 était le **séparateur**, pas l'analyse.
- **La leçon du miroir change de signe** : ce n'est pas « le bloc perd 80 % », c'est « le rendu
  naïf perd 80 % ; le rendu qui garde les intervalles ne perd rien ».
- **Le contrat de sortie doit porter les spans** : c'est la conclusion pratique — une sortie
  sans `debut/fin` n'est pas restituable.
- **La cascade = l'heuristique** : le mock neuronal ne change pas le rendu.

## 2. Ce que ce banc ne dit pas

- **La fidélité parfaite** ne dit rien de la **compréhension** : restituer le texte n'est pas le
  comprendre (la restitution *sémantique* — un résumé, une réponse — reste à mesurer).
- **587 phrases** ; le réel donne les mêmes ordres.
- **Le mock** n'est pas un modèle.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition de la fidélité** (binaire, texte à texte) ;
- **les intervalles** viennent de la source : le rendu les **copie**, il ne les **produit** pas ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La restitution sémantique** : un résumé ou une réponse, pas le texte — la vraie mesure.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `rendre_pos_espaces`, `fidelite_pos_espaces`.
- [`autotest.py`](../tools/pensee/autotest.py) — T118, 121/121.
- [`pensee-miroir-espaces.json`](pensee-miroir-espaces.json) — les quatre restitutions.
