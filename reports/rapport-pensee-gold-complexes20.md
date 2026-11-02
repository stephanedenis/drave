# B13 — les 20 phrases complexes : POS 0,6829, syntagme 0,2963

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **91/91 portes** : les phrases complexes passent de **5 à 20** (r201–r220 : REL `qui/que/dont`,
> SUB `quand/que/bien que/although`, 10 FR + 10 EN). Sur 123 tokens, le **POS est 0,6829**
> (−0,11 contre les 200 phrases simples) et le **syntagme 0,2963** (+0,11). Les deux effets de
> T87 se **confirment** et se **modèrent**.
>
> **Dispositif** : [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-gold-complexes20.json`](pensee-gold-complexes20.json).

## 1. Les 20 complexes

| sous-ensemble | phrases | POS | tokens | syntagme F1 | tête F1 |
|---|---:|---:|---:|---:|---:|
| r001–r200 | 200 | 0,7924 | 978 | 0,1838 | 0,3198 |
| **r201–r220** | **20** | **0,6829** | 123 | **0,2963** | **0,3704** |

**Ce que ça dit** :

- **Le POS chute de 0,11** : les relatifs (`qui`, `que`, `dont`, `who`, `whom`, `that`), les
  auxiliaires (`ai`, `as`, `est`, `soit`, `is`, `are`) et les conjonctions (`quand`, `bien que`,
  `although`, `that`) restent hors du lexique fermé ; le POS ouvert les absorbe.
- **Le syntagme gagne 0,11** : les segments REL/SUB sont **longs** et l'heuristique les délimite
  mieux que les GN courts ; l'effet de T87 (+0,30 sur 5 phrases) se **modère** à +0,11 sur 20.
- **La tête suit** (0,3704) : le rôle des REL/SUB est porté par le nom/verbe de tête.
- **La négative reste** : le POS du hasard (0,0147).

## 2. Ce que ce banc ne dit pas

- **20 phrases** (123 tokens) : l'intervalle est encore large (±0,08).
- **REL/SUB seuls** ; la coordination, l'ellipse, le discours ne sont pas testés.
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 380** (220 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **les étiquettes REL/SUB** (à la main) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- **la taille** (123 tokens : l'intervalle est large) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **50 phrases complexes** : coordination, ellipse ; l'intervalle se resserre.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `PHRASES` (220).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `evaluer_bloc`.
- [`autotest.py`](../tools/pensee/autotest.py) — T88, 91/91.
- [`pensee-gold-complexes20.json`](pensee-gold-complexes20.json) — le bilan.
