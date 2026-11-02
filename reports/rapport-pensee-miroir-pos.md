# B13 — la sortie POS : 0,201, la restitution sémantique ne restitue pas

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6 — le miroir) · **Date** : 2026-11-02
> · **Verdict** : ✅ **120/120 portes** : la **sortie sémantique** (les mots reconstruits depuis
> leurs étiquettes POS) est mesurée : **fidélité 0,201** (mots 0,2095, surface 1,0). La
> restitution POS **perd 80 %** de la source : la ponctuation n'a pas d'étiquette POS, et la
> tokenisation ne recopie pas les espaces. C'est la mesure que la règle 6 demandait.
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-miroir-pos.json`](pensee-miroir-pos.json).

## 1. Les trois restitutions

| restitution | source | **fidélité** | fluidité |
|---|---|---:|---:|
| graphèmes (surface) | 587 phrases | **1,0000** | 1,0 |
| mots (tokens) | 587 phrases | 0,2095 | 1,0 |
| **POS (sémantique)** | 587 phrases | **0,2010** | 1,0 |

**Ce que ça dit** :

- **La sortie POS est la plus faible** (0,201) : elle perd la ponctuation (pas de POS) **et** les
  espaces ; c'est la **vraie** sortie du bloc, et elle n'est pas restitutive.
- **La surface est une tautologie** (1,0) : elle garde tout ; elle ne mesure rien.
- **La cascade = l'heuristique** (0,201) : le mock neuronal ne change pas la sortie.
- **La leçon de la règle 6 est chiffrée** : la **fluidité** (1,0) n'est pas la **fidélité**
  (0,20) ; 80 % du texte est perdu à la sortie.

## 2. Ce que ce banc ne dit pas

- **La restitution depuis les POS avec les espaces** (le `" ".join`) masque une partie de la
  perte ; une mesure par caractères serait plus dure.
- **587 phrases** ; le réel donne les mêmes ordres.
- **Le mock** n'est pas un modèle.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition de la fidélité** (binaire, token à token) ;
- **le `" ".join`** normalise les espaces et cache la ponctuation ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La restitution avec les espaces d'origine** : mesurer la perte réelle, caractère par
   caractère, et la réduire (conserver la ponctuation dans la sortie).
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `rendre_pos`, `fidelite_pos`.
- [`autotest.py`](../tools/pensee/autotest.py) — T117, 120/120.
- [`pensee-miroir-pos.json`](pensee-miroir-pos.json) — les trois restitutions.
