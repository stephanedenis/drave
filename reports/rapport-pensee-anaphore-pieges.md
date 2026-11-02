# B13 — les pièges d'anaphore : 10/12, la règle naïve échoue sur 2 cas

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **96/96 portes** : huit **cas pièges** entrent dans le gold (r321–r328 : deux noms, pronoms
> sujets inversés, PP locatif). L'heuristique « dernier nom » passe de **4/4 à 10/12**
> (0,8333) : elle échoue sur **r324** (`il → table` au lieu de `livre`) et **r328**
> (`it → table` au lieu de `book`). La négative qui manquait est là.
>
> **Dispositif** : [`anaphore.py`](../tools/tests/linguistique/anaphore.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-anaphore-pieges.json`](pensee-anaphore-pieges.json).

## 1. Les pièges

| phrase | pronom | attendu | obtenu | verdict |
|---|---|---|---|---|
| r321 `Le chat voit le chien ; il dort` | `il` | `chien` | `chien` | ✅ (le piège ne piège pas : le dernier nom est le bon) |
| r322 `Le chien voit le chat ; il dort` | `il` | `chat` | `chat` | ✅ |
| r323 `Marie appelle Sophie ; elle répond` | `elle` | `sophie` | `sophie` | ✅ |
| r324 `Le livre est sur la table ; il est rouge` | `il` | `livre` | `table` | ❌ |
| r325 `Paul et Marie lisent ; ils rient` | `ils` | `marie` | `marie` | ✅ |
| r326 `The cat sees the dog; it sleeps` | `it` | `dog` | `dog` | ✅ |
| r327 `Marie calls Sophie; she answers` | `she` | `sophie` | `sophie` | ✅ |
| r328 `The book is on the table; it is red` | `it` | `book` | `table` | ❌ |

**Ce que ça dit** :

- **10/12** : la règle « dernier nom » tient sur les deux noms et les pronoms inversés, mais
  **échoue sur le PP locatif** (`sur la table`, `on the table`) : le dernier nom est le lieu,
  pas l'antécédent.
- **Le taux baisse** (1,0 → 0,8333) : c'est la **première négative** de l'anaphore ; elle est
  due au gold, pas au hasard.
- **La correction est claire** : ignorer les noms dans un PP (ou pondérer par le rôle `agent`).
- **La marge est faible** (12 liens) : l'intervalle reste large.

## 2. Ce que ce banc ne dit pas

- **12 liens** ; 50 donneraient une courbe.
- **Le PP locatif** est le seul échec ; les chaînes longues, l'ellipse ne sont pas testées.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 508** (328 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la taille** (12 liens) ;
- **les ancres** (annotation à la main) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Ignorer les PP** : la règle corrigée ; remonter à 12/12.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`anaphore.py`](../tools/tests/linguistique/anaphore.py) — `resoudre`, `mesurer`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `coref` sur 12 phrases.
- [`autotest.py`](../tools/pensee/autotest.py) — T93, 96/96.
- [`pensee-anaphore-pieges.json`](pensee-anaphore-pieges.json) — le bilan.
