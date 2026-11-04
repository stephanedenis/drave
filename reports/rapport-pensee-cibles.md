# B13 — les cibles de l'attachement : 1624 segments sans cible sur 1863

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **157/157 portes** : le dénominateur de l'attachement est **1863 segments**, dont **1624 sans
> cible** (87,2 %). Le « 94 cibles sans label » de la fiche précédente était une **sous-estimation** :
> c'est bien **1624** segments qui n'ont pas de `cible` dans le gold. La couverture réelle est
> **239/1863 = 0,1283**.
>
> **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-cibles.json`](pensee-cibles.json).

## 1. Le dénominateur

| mesure | valeur |
|---|---:|
| segments du gold 432 | **1863** |
| segments **sans cible** | **1624** (87,2 %) |
| segments avec cible | **239** (12,8 %) |

**Ce que ça dit** :

- **L'attachement est à peine annoté** : 12,8 % des segments ont une cible ; le taux exact de
  0,0042 se lit sur 239 cibles, pas sur 1863 segments.
- **La fiche T153 sous-estimait** : elle parlait de « 94 cibles sans label » ; le vrai chiffre
  est **1624 segments sans cible**. La nuance est importante : le gold n'annote pas l'attachement
  de la plupart des segments, il annote **quelques** cibles.
- **La couverture 0,6067 de T153** est un autre calcul (145 labels sur 239 cibles) : deux
  dénominateurs, deux lectures — il faut les nommer.
- **La négative est explicite** : 0,1283 de couverture, ce n'est pas un gold d'attachement.

## 2. Ce que ce banc ne dit pas

- **Les 1624 segments** : leur attachement n'est pas annoté, donc pas mesurable.
- **Le gold 432** : 432 phrases.
- **Les cibles** : 239, annotées à la main.
- **Le gold 612** (432 réels + 160 synthétiques + 20 de `gold.py`).

## 3. Ce qui pourrait rendre cette fiche fausse

- **la définition de la cible** : un segment sans `cible` n'est pas forcément sans attachement ;
- **le gold** : 432 phrases ;
- **les deux dénominateurs** (239 cibles / 1863 segments) sont légitimes mais différents ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Annoter l'attachement** : 1863 segments est un travail réel ; commencer par les 500 premiers.
2. **La règle d'attachement** : le top-k 0,3264 sur les 239 cibles est le seul signal.
3. **Politique DRVM/native** : quand les poids seront là.
4. **L** : le gold vivant peut grandir.

## 5. Fichiers

- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `attachement`.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — les `cible`.
- [`autotest.py`](../tools/pensee/autotest.py) — T154, 157/157.
- [`pensee-cibles.json`](pensee-cibles.json) — le dénominateur.
