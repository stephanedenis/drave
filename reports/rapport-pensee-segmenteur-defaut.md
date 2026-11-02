# B13 — l'union par défaut : F1 0,2005, tête 0,4662

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **116/116 portes** : l'**union** des segmenteurs entre dans l'**analyseur par défaut**
> (`Heuristique.analyser`, étape 5 bis). Le gold complet donne **syntagme F1 0,2005** (S seul :
> 0,1722) et **tête F1 0,4662** (S seul : 0,3552) — la tête gagne **+0,11**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-segmenteur-defaut.json`](pensee-segmenteur-defaut.json).

## 1. L'union par défaut

| mesure | S seul | **union (défaut)** | delta |
|---|---:|---:|---:|
| syntagme F1 | 0,1722 | **0,2005** | +0,0283 |
| syntagme précision | 0,2424 | 0,2328 | −0,0096 |
| syntagme rappel | 0,1335 | **0,1761** | +0,0426 |
| **tête F1** | 0,3552 | **0,4662** | **+0,1110** |

**Ce que ça dit** :

- **La tête gagne +0,11** : l'union apporte les segments du chunker, dont les têtes sont bonnes ;
  c'est le plus gros gain de la ligne syntagme.
- **Le F1 gagne +0,028** : la précision perd 0,01, le rappel gagne 0,04.
- **Le défaut est changé** : `analyser` ajoute les segments du chunker absents du S (confiance
  0,30, `meta.union = True`), sans toucher aux segments du S.
- **La négative est explicite** : le S seul reste à 0,1722.

## 2. Ce que ce banc ne dit pas

- **587 phrases** ; le réel donne les mêmes ordres.
- **L'union dépend du S** : si le générateur S change, l'union change.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **les tests du bloc** (les segments attendus) : ils passent ;
- **le seuil `syntagme_reel`** (0,16) : la hausse aide ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La cascade** : mesurer l'union dans la cascade (heuristique + mock) et le coût.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — étape 5 bis (union).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `evaluer_bloc`.
- [`autotest.py`](../tools/pensee/autotest.py) — T113, 116/116.
- [`pensee-segmenteur-defaut.json`](pensee-segmenteur-defaut.json) — le défaut.
