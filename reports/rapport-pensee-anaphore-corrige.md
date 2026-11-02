# B13 — l'anaphore corrigée : 12/12 en ignorant les noms des PP

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **97/97 portes** : la règle « dernier nom » est corrigée — les noms dans un **groupe
> prépositionnel** (`sur la table`, `on the table`) sont ignorés. L'anaphore passe de
> **10/12 à 12/12** (1,0) sur les 12 liens du gold. La correction est **exactement** celle que
> T93 annonçait.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-corrige.json`](pensee-anaphore-corrige.json).

## 1. La correction

`_dans_pp(mots, i)` : un nom est « dans un PP » s'il est précédé d'une `PREP` ou d'un `DET`
lui-même précédé d'une `PREP`. `resoudre(..., ignorer_pp=True)` saute ces noms.

| règle | liens | justes | taux | échecs |
|---|---:|---:|---:|---|
| naïve (T92/T93) | 12 | 10 | 0,8333 | r324, r328 |
| **corrigée (T94)** | **12** | **12** | **1,00** | — |

**Ce que ça dit** :

- **La correction est nette** : les deux échecs (le PP locatif) disparaissent ; les 10 cas
  déjà justes le restent.
- **La règle reste naïve** : elle ne résout pas les chaînes longues, les pronoms objets
  (`le`, `la`, `les`), l'ellipse ; elle ne fait que retirer le piège identifié.
- **La marge est faible** (12 liens) : le 12/12 n'est pas une preuve, c'est un **contrôle**.
- **La négative reste** : la règle naïve (T93) échoue 2/12 — elle est conservée comme porte.

## 2. Ce que ce banc ne dit pas

- **12 liens** ; 50 donneraient une courbe.
- **Les pronoms objets** et les chaînes longues ne sont pas couverts.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 508** (328 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (12 liens) ;
- **la règle `_dans_pp`** (elle suppose `PREP`/`DET` explicites) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Les pronoms objets** (`le`, `la`, `les`) : une autre règle.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `resoudre(ignorer_pp=True)`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `coref` sur 12 phrases.
- [`autotest.py`](../tools/pensee/autotest.py) — T94, 97/97.
- [`pensee-anaphore-corrige.json`](pensee-anaphore-corrige.json) — le bilan.
