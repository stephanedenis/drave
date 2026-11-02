# B13 — les 50 phrases complexes : POS 0,7013, syntagme 0,3060

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **92/92 portes** : les phrases complexes passent de **20 à 50** (r201–r250 : REL `qui/que/dont/où/
> whose/where`, SUB `que/quand/si/parce que/bien que/although/while/as`, 25 FR + 25 EN). Sur
> **318 tokens**, le **POS est 0,7013** (−0,091 contre les 200 phrases simples) et le **syntagme
> 0,3060** (+0,12). Les effets se **stabilisent** : −0,09 / +0,12.
>
> **Dispositif** : [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-gold-complexes50.json`](pensee-gold-complexes50.json).

## 1. Les 50 complexes

| sous-ensemble | phrases | POS | tokens | syntagme F1 | tête F1 |
|---|---:|---:|---:|---:|---:|
| r001–r200 | 200 | 0,7924 | 978 | 0,1838 | 0,3198 |
| **r201–r250** | **50** | **0,7013** | 318 | **0,3060** | **0,3731** |

**Ce que ça dit** :

- **Le POS chute de 0,09** : les relatifs, auxiliaires et conjonctions restent hors du lexique
  fermé ; le POS ouvert les absorbe. Le chiffre se **stabilise** (0,6829 à 20, 0,7013 à 50).
- **Le syntagme gagne 0,12** : les segments REL/SUB longs sont mieux délimités que les GN
  courts ; l'effet se **stabilise** aussi (0,2963 à 20, 0,3060 à 50).
- **La tête suit** (0,3731) : le rôle est porté par le nom/verbe de tête.
- **La négative reste** : le POS du hasard (0,0147).

## 2. Ce que ce banc ne dit pas

- **50 phrases** (318 tokens) : l'intervalle est ±0,05.
- **REL/SUB seuls** ; la coordination, l'ellipse, le discours ne sont pas testés.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 380** (250 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **les étiquettes REL/SUB** (à la main) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- **la taille** (318 tokens) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **100 phrases complexes** : coordination, ellipse ; l'intervalle se resserre encore.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `PHRASES` (250).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `evaluer_bloc`.
- [`autotest.py`](../tools/pensee/autotest.py) — T89, 92/92.
- [`pensee-gold-complexes50.json`](pensee-gold-complexes50.json) — le bilan.
