# B13 — le miroir entrée/sortie : surface 1,0, mots 0,2095

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6 — le miroir) · **Date** : 2026-11-02
> · **Verdict** : ✅ **119/119 portes** : la restitution du bloc est mesurée pour la première
> fois. Depuis les **graphèmes**, elle est **exacte (1,0)** — c'est une tautologie (la couche
> graphème est la surface). Depuis les **mots**, elle est **0,2095** : la tokenisation perd la
> ponctuation et les espaces. **La fluidité (1,0) n'est pas la fidélité (0,21).**
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-miroir.json`](pensee-miroir.json).

## 1. Les deux restitutions

| restitution | source | **fidélité** | fluidité |
|---|---|---:|---:|
| graphèmes (surface) | 587 phrases | **1,0000** | 1,0 |
| mots (tokens) | 587 phrases | **0,2095** | 1,0 |
| cascade (mots) | 587 phrases | 0,2095 | 1,0 |

**Ce que ça dit** :

- **La surface est fidèle par construction** : la couche graphème recopie le texte ; ce n'est pas
  un résultat, c'est un **contrôle** (la restitution ne perd rien *si* on garde tout).
- **Les mots perdent 0,79** : la ponctuation et les espaces ne sont pas restitués ; c'est la
  **vraie** mesure — la sortie du bloc n'est pas le texte.
- **Cascade = heuristique** sur cette mesure : le mock neuronal ne change pas la restitution.
- **La règle 6 est armée** : une mesure d'entrée (POS, syntagme) se double désormais d'une mesure
  de sortie ; les deux ne sont pas la même chose.

## 2. Ce que ce banc ne dit pas

- **La restitution depuis les POS** (la sortie *sémantique*) n'est pas mesurée : c'est la
  prochaine étape — reconstruire le texte depuis les étiquettes, pas depuis la surface.
- **587 phrases** ; le réel donne les mêmes ordres.
- **Le mock** n'est pas un modèle.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition de la fidélité** (binaire, token à token) ;
- **le `" ".join`** normalise les espaces et cache les pertes de ponctuation ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La restitution depuis les POS** : la sortie *sémantique*, la vraie mesure de fidélité.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`miroir.py`](../tools/tests/linguistique/miroir.py) — `rendre`, `rendre_mots`, `fidelite`, `fidelite_mots`, `mesurer`.
- [`autotest.py`](../tools/pensee/autotest.py) — T116, 119/119.
- [`pensee-miroir.json`](pensee-miroir.json) — les deux mesures.
