# B13 — les 19 réponses de référence : le juge a une couverture de 1,0

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **127/127 portes** : les **19 questions** du gold portent désormais une **réponse de
> référence** (`pragma.reponse`) : **19/19 (1,0)** de couverture. Le juge peut enfin comparer ;
> il ne juge pas encore le bloc (qui répond 0/19 au contenu), il juge la **référence**.
>
> **Dispositif** : [`juge.py`](../tools/tests/linguistique/juge.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py), [`gold.py`](../tools/tests/linguistique/gold.py),
> [`gold_synthetique.py`](../tools/tests/linguistique/gold_synthetique.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-reponses.json`](pensee-reponses.json).

## 1. La couverture

| mesure | avant | **après** |
|---|---:|---:|
| questions du gold | 19 | 19 |
| questions avec réponse de référence | 0 | **19** |
| **couverture** | 0,0000 | **1,0000** |

**Ce que ça dit** :

- **La référence existe** : les 19 questions (5 réalistes, 14 synthétiques) portent une réponse
  (`oui`/`yes` pour les questions fermées) ; `gold.json`, `gold_reel.json` et
  `gold_synthetique.json` sont régénérés.
- **Le juge devient utilisable** : `juge("oui", "oui") = 1,0`, `juge("oui", "non") = 0,0` — la
  mesure de correction est **possible**.
- **Ce n'est pas encore une mesure du bloc** : le bloc répond 0/19 au contenu (T121) ; le juge
  mesurerait donc 0/19 pour lui. La référence est la condition, pas le résultat.
- **Le biais est corrigé** : le gold annotait la forme (l'acte), il annote maintenant le fond
  (la réponse) — pour les questions fermées.

## 2. Ce que ce banc ne dit pas

- **Les réponses ouvertes** (le contenu libre) n'ont pas de référence : les 19 questions sont
  fermées (oui/non).
- **19 questions** ; le réel donne les mêmes ordres.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition de la référence** (une chaîne exacte, pas le sens) ;
- **les réponses sont fermées** : oui/non ne teste pas la compréhension ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le juge contre le bloc** : mesurer ce que le bloc répond (0/19) et ce que l'extraction
   donnerait comme réponse (le GN, à comparer aux références).
2. **Le neuronal réel** : toujours bloqué ; c'est lui qui répondrait.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`juge.py`](../tools/tests/linguistique/juge.py) — `juge`, `couverture`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — 4 réponses réalistes.
- [`gold.py`](../tools/tests/linguistique/gold.py) — 1 réponse (g013).
- [`gold_synthetique.py`](../tools/tests/linguistique/gold_synthetique.py) — 14 réponses synthétiques.
- [`autotest.py`](../tools/pensee/autotest.py) — T124, 127/127.
- [`pensee-reponses.json`](pensee-reponses.json) — la couverture.
