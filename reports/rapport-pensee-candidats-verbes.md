# B13 — les candidats verbes : le top-k passe de 0,3264 à 0,4686

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **165/165 portes** : les `candidats` d'un segment portent maintenant, en plus de son type, les
> **verbes des trois GV les plus proches**. Sur le gold de T153 (612 phrases, 239 cibles), le
> **top-k passe de 78 (0,3264) à 112 (0,4686)**, et la tête de **77/145 (0,5310) à 111/145
> (0,7655)**. Le top1 (0,3975) et l'exact (0,0544) ne bougent pas : la cible proposée est la même,
> c'est la **liste des alternatives** qui s'enrichit.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_verbes_proches`),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-candidats-verbes.json`](pensee-candidats-verbes.json).

## 1. Avant / après (même gold, 239 cibles)

| mesure | avant | **candidats verbes** | écart |
|---|---:|---:|---:|
| top1 | 95 (0,3975) | 95 (0,3975) | 0 |
| **top-k** | 78 (0,3264) | **112 (0,4686)** | **+34 (+0,1422)** |
| exact | 13 (0,0544) | 13 (0,0544) | 0 |
| **tête top-k** | 77/145 (0,5310) | **111/145 (0,7655)** | **+34 (+0,2345)** |
| tête top1 | 94/145 (0,6483) | 94/145 (0,6483) | 0 |

**Ce que ça dit** :

- **La bonne cible est dans la liste 3 fois plus souvent qu'avant** en tête (0,7655) et
  **+0,1422** en top-k global — le rappel des candidats était le trou, pas le classement.
- **Le top1 ne bouge pas** : la règle de proximité propose toujours le même verbe ; ce round
  n'améliore que le **rappel** (les alternatives), ce qui est exactement son objet.
- **La tête est le bon régime** : quand le span est bon (145/145 en couverture), le top-k atteint
  **76,6 %** — c'est là que la liste sert.
- **La négative est explicite** : 127/239 cibles restent hors des trois verbes proposés (mauvais
  GV, mauvais span, ou cible non verbale).

## 2. Ce que ce banc ne dit pas

- **Les 127 échecs** ne sont pas qualifiés (span faux, mauvais GV, cible non verbale).
- **Le classement** des candidats n'est pas appris : l'ordre est la proximité.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.
- **Le coût** : trois verbes calculés par segment, sans appel de modèle.

## 3. Ce qui pourrait rendre cette fiche fausse

- **`candidats` change de sens** : il portait le type (ou le nom de segmentation), il porte aussi
  des verbes ; les lecteurs qui l'interprétaient comme un type verraient autre chose ;
- **la métrique top-k** accepte les sous-chaînes (`vu` ⊂ `aperçu`) ;
- **le gold** : 612 phrases ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Qualifier les 127 échecs** : span faux, mauvais GV, ou cible non verbale.
2. **Classer les candidats** : la proximité est un ordre, pas un apprentissage.
3. **Le générateur S** : les passifs.
4. **Politique DRVM/native** : quand les poids seront là.

## 5. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — `_verbes_proches`.
- [`autotest.py`](../tools/pensee/autotest.py) — T162, 165/165.
- [`pensee-candidats-verbes.json`](pensee-candidats-verbes.json) — avant/après.
