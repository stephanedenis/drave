# B13 — la restitution sémantique : le résumé rappelle 78 %

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6 — le miroir) · **Date** : 2026-11-02
> · **Verdict** : ✅ **122/122 portes** : la **sortie sémantique** (un résumé par les syntagmes
> GN/GV, pas le texte) est mesurée : **rappel 0,7834** pour l'heuristique, **0,7472** pour la
> cascade. Le résumé couvre 78 % des mots de la source ; la cascade **perd** 3,6 points.
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-miroir-resume.json`](pensee-miroir-resume.json).

## 1. Les cinq restitutions

| restitution | source | **mesure** |
|---|---|---:|
| graphèmes (surface) | 587 phrases | 1,0000 |
| POS + intervalles | 587 phrases | 1,0000 |
| **résumé (syntagmes)** | 587 phrases | **0,7834** (heur) / 0,7472 (cascade) |

**Ce que ça dit** :

- **Le résumé n'est pas le texte** : 78 % des mots couverts, 22 % perdus (les déterminants,
  les pronoms, la ponctuation) — c'est la **vraie** restitution sémantique.
- **La cascade perd 3,6 points** (0,7472) : ses syntagmes supplémentaires ont des `valeur` plus
  courtes (le mock) ; le résumé est moins complet.
- **La règle 6 est complète** : la surface (1,0), le POS (1,0 avec spans), le sémantique (0,78)
  — trois sorties, trois mesures, pas une.
- **La fluidité (1,0) n'est toujours pas la fidélité** (0,78).

## 2. Ce que ce banc ne dit pas

- **Le résumé n'est pas une réponse** : il répète les syntagmes, il ne reformule pas ; la
  fidélité *sémantique* (le sens conservé) n'est pas mesurée.
- **587 phrases** ; le réel donne les mêmes ordres.
- **Le mock** n'est pas un modèle.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition du rappel** (tokens, pas le sens) ;
- **le résumé** répète la surface : il ne prouve pas la compréhension ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La réponse** : une reformulation, pas une répétition — la mesure suivante.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `resume`, `rappel_resume`.
- [`autotest.py`](../tools/pensee/autotest.py) — T119, 122/122.
- [`pensee-miroir-resume.json`](pensee-miroir-resume.json) — les cinq restitutions.
