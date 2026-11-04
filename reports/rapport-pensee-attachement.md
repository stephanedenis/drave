# B13 — l'attachement sur le gold 432 : top1 0,3431, exact 0,0042

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **156/156 portes** : l'**attachement** (le segment → sa cible) est mesuré sur le gold 432 :
> **top1 0,3431**, **top-k 0,3264**, **exact 0,0042**, **couverture 0,6067**. La couverture est la
> première limite : **145 cibles sur 239** sont annotées, et l'attachement exact est **quasi nul**
> (1 sur 239).
>
> **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-attachement.json`](pensee-attachement.json).

## 1. Les deux mesures

| mesure | cibles | labels | top1 | top-k | exact | couverture |
|---|---:|---:|---:|---:|---:|---:|
| attachement | 239 | 145 | 82 (0,3431) | 78 (0,3264) | **1 (0,0042)** | 0,6067 |
| attachement (tête) | 145 | 145 | 81 (0,5586) | 77 (0,5310) | — | 1,0000 |

**Ce que ça dit** :

- **L'attachement exact est quasi nul** (1/239) : le bloc propose des candidats, pas la bonne
  cible — c'est le point le plus faible de la ligne L.
- **La couverture est la première limite** : 145 cibles sur 239 sont annotées (60,7 %) — les
  autres n'ont pas de `cible`, et le dénominateur les compte quand même.
- **La tête est meilleure** (0,5586) : quand on restreint aux cibles annotées, le top1 monte —
  le problème est autant l'annotation que la règle.
- **La négative est explicite** : 0,0042 exact, ce n'est pas un attachement.

## 2. Ce que ce banc ne dit pas

- **Les 94 cibles sans label** : elles comptent comme des échecs dans le taux exact.
- **Le gold 432** : 432 phrases.
- **L'heuristique** ; le neuronal ne fait pas l'attachement (le contrat le laisse à l'heuristique).
- **Le gold 612** (432 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **le dénominateur** : 239 inclut les cibles non annotées ;
- **l'attachement exact** : un seul cas réussi, la mesure est fragile ;
- **le gold** : 432 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Annoter les 94 cibles manquantes** : la couverture est le vrai levier.
2. **La règle d'attachement** : revoir le choix de la cible (le top-k à 0,53 est déjà là).
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `attachement`.
- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — les candidats `cible`.
- [`autotest.py`](../tools/pensee/autotest.py) — T153, 156/156.
- [`pensee-attachement.json`](pensee-attachement.json) — les mesures.
