# B13 — l'hybride frontières/têtes : 0,3732, le chunker garde les têtes

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **114/114 portes** : l'**hybride** (frontières du générateur S, tête du chunker à l'intérieur du
> segment) est mesuré : **tête F1 0,3732**. Il bat le S (0,3552) mais **reste loin du chunker
> seul** (0,4707). Le chunker a la **précision** (0,8588) et la meilleure tête ; c'est lui qu'il
> faut garder pour les têtes.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-segmenteur-hybride.json`](pensee-segmenteur-hybride.json).

## 1. Les têtes

| segmenteur | précision | rappel | **F1** |
|---|---:|---:|---:|
| S générateur | 0,5000 | 0,2754 | 0,3552 |
| **chunker simple** | **0,8588** | **0,3242** | **0,4707** |
| hybride | 0,5255 | 0,2894 | 0,3732 |

**Ce que ça dit** :

- **Le chunker a la précision** (0,8588) : quand il place une tête, il a raison 6 fois sur 7 ;
  son rappel est faible (0,3242) — il manque des segments.
- **L'hybride n'améliore pas** : prendre la tête du chunker **à l'intérieur** du segment du S
  ne récupère que les segments communs ; le F1 (0,3732) reste sous le chunker.
- **La vraie piste** est **le rappel** : garder les têtes du chunker et **compléter les segments
  manquants** — pas fusionner les deux listes.
- **La négative est explicite** : 0,3732 < 0,4707.

## 2. Ce que ce banc ne dit pas

- **587 phrases** ; le réel donne les mêmes ordres.
- **Le rappel** est le vrai levier ; l'hybride ne le traite pas.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **les frontières** dépendent du S (un autre segmenter changerait tout) ;
- **le même token peut être tête de deux segments** (les types diffèrent) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Le rappel du chunker** : compléter les segments manquants (le S en fournit les bornes).
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — les deux segmenteurs.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `_seg`, `_tete`.
- [`autotest.py`](../tools/pensee/autotest.py) — T111, 114/114.
- [`pensee-segmenteur-hybride.json`](pensee-segmenteur-hybride.json) — l'hybride.
