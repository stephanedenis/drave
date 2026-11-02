# B13 — le discours : acte 0,9, négation 1,0, modalité 0,9

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-02 · **Verdict** : ✅
> **94/94 portes** : vingt phrases de **discours** (r301–r320 : anaphore `il/elle`, connecteurs
> `donc/mais/car/so/but/because`, questions, ordres, négation, modalité) entrent dans le gold
> réel (320 phrases). Sur 92 tokens : **acte 0,9**, **négation 1,0**, **modalité 0,9**,
> **double sens 0,95**, **POS 0,7609**.
>
> **Dispositif** : [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-gold-discours.json`](pensee-gold-discours.json).

## 1. Le discours

| sous-ensemble | phrases | acte | négation | modalité | double sens | POS |
|---|---:|---:|---:|---:|---:|---:|
| r001–r300 | 300 | 1,0 | 1,0 | 0,9867 | 0,9767 | 0,7556 |
| **r301–r320** | **20** | **0,9** | **1,0** | **0,9** | 0,95 | **0,7609** |

**Ce que ça dit** :

- **L'acte chute à 0,9** : deux phrases (question `Viens-tu ?`, ordre `Ferme la porte !`) sont
  prises pour des assertions — le lexique d'actes est encore simple.
- **La négation tient** (1,0) : `ne … pas`, `does not` sont reconnus.
- **La modalité tient à 0,9** : `peut-être`, `dois`, `maybe`, `must` ; une des quatre échappe.
- **Le POS est bon** (0,7609) : le discours n'ajoute pas de difficulté de POS.
- **La négative reste** : le POS du hasard (0,0147).

## 2. Ce que ce banc ne dit pas

- **20 phrases** (92 tokens) : l'intervalle est ±0,06.
- **Anaphore** : la coréférence n'est pas mesurée (seule la forme est étiquetée).
- **L'heuristique** ; le neuronal réel reste bloqué.
- **Le gold 500** (320 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **les étiquettes pragmatiques** (acte, modalité à la main) ;
- **le JSON régénéré** (`gold_reel.json` doit suivre) ;
- **la taille** (92 tokens) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **La coréférence mesurée** : chaînes anaphoriques, résolution.
2. **Le neuronal réel** : toujours bloqué ; le mock reste un contrat.
3. **Politique DRVM/native** : un vrai modèle quand les poids seront là.
4. **L** : le gold peut encore grandir.

## 5. Fichiers

- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `PHRASES` (320).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `evaluer_bloc`.
- [`autotest.py`](../tools/pensee/autotest.py) — T91, 94/94.
- [`pensee-gold-discours.json`](pensee-gold-discours.json) — le bilan.
