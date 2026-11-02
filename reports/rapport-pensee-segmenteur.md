# B13 — le segmenteur : deux chunkers complémentaires, F1 0,1722 contre 0,1425

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **113/113 portes** : les deux segmenteurs de l'heuristique sont comparés sur le gold complet
> (587 phrases, 3 062 tokens). Le **générateur S** (défaut) fait **F1 0,1722 / tête 0,3552** ;
> le **chunker simple** fait **F1 0,1425 / tête 0,4707**. Les deux sont **complémentaires** :
> l'un a les bonnes frontières, l'autre les bonnes têtes.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-segmenteur.json`](pensee-segmenteur.json).

## 1. Les deux segmenteurs

| segmenteur | F1 (all) | tête (all) | F1 (réel) |
|---|---:|---:|---:|
| **générateur S** (défaut) | **0,1722** | 0,3552 | 0,1713 |
| chunker simple | 0,1425 | **0,4707** | 0,1552 |

**Ce que ça dit** :

- **Le générateur S a les meilleures frontières** (F1 0,1722 > 0,1425) : ses segments
  correspondent mieux aux bornes du gold.
- **Le chunker simple a les meilleures têtes** (0,4707 > 0,3552) : il place le début du segment
  sur le bon token, même quand la fin est fausse.
- **Les deux sont complémentaires** : un hybride (frontières du S, têtes du chunker) est la
  prochaine piste — il n'est pas implémenté.
- **La négative est explicite** : le chunker perd 0,03 de F1.

## 2. Ce que ce banc ne dit pas

- **587 phrases** ; le réel (427) donne les mêmes ordres.
- **L'hybride frontières/têtes** n'est pas mesuré.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 587** (427 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le seuil `syntagme_reel`** (0,16, ajusté deux fois) ;
- **les frontières** dépendent du générateur S (un autre segmenter changerait tout) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **L'hybride frontières/têtes** : segments du S, début du chunker ; mesurer le F1 et la tête.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `_syntagmes_simple`, `_syntagmes_s`.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `evaluer_bloc`.
- [`autotest.py`](../tools/pensee/autotest.py) — T110, 113/113.
- [`pensee-segmenteur.json`](pensee-segmenteur.json) — la comparaison.
