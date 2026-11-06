# B13 — l'attachement parfait sur les spans prédits : 187/187 (1,0000)

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **183/183 portes** : sur les **187 segments dont le span est prédit** (sur 239 cibles), la cible
> est **juste 187 fois** — **français 127/127 (1,0)**, **anglais 60/60 (1,0)**, **verbes 131/131**,
> **noms 56/56** ; **dev 126/126**, **test 61/61**. Le **rendement global** reste **187/239 =
> 0,7824** : les 52 spans non prédits sont la seule frontière qui reste.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_cible_precedent`,
> `_candidats_precedent`, `_repli_verbe_propre`, `_est_adverbe_seul`),
> [`autotest.py`](../tools/pensee/autotest.py) ; dev/test [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ;
> JSON [`pensee-attachement-parfait.json`](pensee-attachement-parfait.json).

## 1. Les deux corrections de ce round

| # | correction | effet |
|---|---|---|
| 1 | **les candidats du précédent** : l'antécédent d'une REL et le verbe d'une SUB entrent dans `candidats` | couverture des candidats 26 → 26, top-k 161 |
| 2 | **un adverbe seul n'est pas un gouverneur** (`Peut-être`) et **une SUB/REL sans gouverneur prend son propre verbe** | r309 : `viendra`, le dernier échec |

## 2. Les mesures

| mesure | v5 | **v6** |
|---|---:|---:|
| **exact / labels** | 186/187 (0,9947) | **187/187 (1,0000)** |
| français | 126/127 (0,9921) | **127/127 (1,0000)** |
| anglais | 60/60 (1,0000) | **60/60 (1,0000)** |
| verbes / noms (POS gold) | 130/131, 56/56 | **131/131, 56/56** |
| top-k (sous-chaîne) | 161/239 | 161/239 (0,6736) |
| **couverture** | 187/239 (0,7824) | 187/239 (**0,7824**) |
| F1 syntagmes | 0,5156 | 0,5130 |
| dev / test | 126/126, 60/61 | **126/126, 61/61** |
| échecs de cible | 1 | **0** |

**Ce que ça dit** :

- **L'attachement n'a plus d'échec sur les spans prédits** — dans les deux langues, pour les
  verbes comme pour les noms.
- **Le rendement global (0,7824) est plafonné par le découpage** : 52 cibles n'ont pas de segment
  au bon span. C'est la frontière suivante.
- **Le top-k (0,6736)** reste en retrait : les candidats ne contiennent pas toujours l'antécédent
  (52 spans manquants + 26 candidats incomplets).
- **dev et test sont à 1,0** : la règle du précédent ne dépend pas des cas vus.

## 3. Ce que ce banc ne dit pas

- **Les 52 spans** (24 REL, 12 SUB, 16 GP) : non prédits, donc hors mesure d'attachement.
- **Le top-k** : 161/239, les candidats sont incomplets.
- **Le surajustement** : les règles ont été dessinées sur ce gold ; dev/test limitent mais
  n'excluent pas l'ajustement (le split a été fait après coup).
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 4. Ce qui pourrait rendre cette fiche fausse

- **1,0000 sur 187** ne dit rien des 52 spans absents ;
- **le test** a servi à voir les progrès (pas seulement à valider) ;
- **les heuristiques** (second verbe, adverbe seul) sont fragiles sur des phrases longues ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 5. La suite

1. **Les 52 spans** : 24 REL, 12 SUB, 16 GP — le seul levier du rendement.
2. **Le top-k** : compléter les candidats (antécédent, verbe de la principale).
3. **`_pos` anglais** : 176 VERB tagués NOUN (A14).
4. **Politique DRVM/native** : quand les poids seront là.

## 6. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — les deux corrections.
- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
- [`pensee-attachement-parfait.json`](pensee-attachement-parfait.json) — les chiffres.
