# B13 — l'union des segmenteurs : F1 0,2005, le rappel paie

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **115/115 portes** : l'**union** des segments du générateur S et du chunker fait **F1 0,2005**
> contre 0,1722 pour le S seul : le **rappel** passe de 0,1335 à **0,1761**, la précision ne perd
> que 0,01. C'est le premier gain de syntagme depuis longtemps. Pour les **têtes**, l'union
> (0,4662) reste sous le chunker seul (0,4707).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-segmenteur-union.json`](pensee-segmenteur-union.json).

## 1. L'union

| segmenteur | précision | rappel | **F1** |
|---|---:|---:|---:|
| S générateur | 0,2424 | 0,1335 | 0,1722 |
| chunker simple | 0,2600 | 0,0981 | 0,1425 |
| **union des segments** | 0,2328 | **0,1761** | **0,2005** |
| **union des têtes** | 0,5646 | 0,3971 | 0,4662 |

**Ce que ça dit** :

- **Le rappel paie** : l'union ajoute les segments que chaque segmenteur rate seul ; +0,028 de
  F1, le premier gain depuis le début de la ligne gold.
- **La précision tient** (0,2328 contre 0,2424) : l'union ajoute peu de faux positifs.
- **Les têtes ne gagnent pas** (0,4662 < 0,4707) : le chunker reste le meilleur pour les têtes.
- **La négative est explicite** : l'union des têtes perd 0,004 contre le chunker.

## 2. Ce que ce banc ne dit pas

- **587 phrases** ; le réel donne les mêmes ordres.
- **L'union est un plafond bas** : 0,20 de F1 reste loin d'un segmenteur entraîné.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le seuil `syntagme_reel`** (0,16) ;
- **l'union** dépend des deux segmenteurs (un troisième changerait tout) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le segmenteur par défaut** : passer à l'union (le S + le chunker) et mesurer la cascade.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — les deux segmenteurs.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `_seg`, `_tete`.
- [`autotest.py`](../tools/pensee/autotest.py) — T112, 115/115.
- [`pensee-segmenteur-union.json`](pensee-segmenteur-union.json) — l'union.
