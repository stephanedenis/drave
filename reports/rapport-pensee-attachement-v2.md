# B13 — l'attachement v2 : exact 0,8483 → 0,9448, top-k strict 0,6069 → 0,9724

> **Instantané historique** : état au commit `9d5337ce` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **180/180 portes** : trois corrections **mesurées**, issues de trois sous-agents indépendants :
> (1) la règle du **segment précédent** (un SUB après un GV est une complétive → cible = le verbe ;
> après un GN, une relative → cible = l'antécédent), (2) les **têtes des candidats** de S
> (« « … » → Le livre » → `livre`), (3) le **lexique verbal anglais** complété. Sur les 145
> segments au bon span : **exact 123 → 137 (0,9448)**, top1 **126 → 140 (0,9655)**, top-k
> **134 → 142 (0,9793)**, **top-k strict 88 → 141 (0,9724)**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) (`CONVENTION_CIBLE`),
> [`autotest.py`](../tools/pensee/autotest.py) ; fiches des sous-agents :
> [audit](rapport-audit-attachement.md) (A1), [top-k](rapport-topk-diagnostic.md) (A2),
> [annotation indépendante](rapport-annotation-independante.md) (A7), [classement appris](rapport-classement-appris.md) (A3).
> JSON : [`pensee-attachement-v2.json`](pensee-attachement-v2.json).

## 1. Avant / après (145 segments au bon span)

| mesure | avant | **v2** | écart |
|---|---:|---:|---:|
| top1 | 126 (0,8690) | **140 (0,9655)** | +14 |
| top-k (sous-chaîne) | 134 (0,9241) | **142 (0,9793)** | +8 |
| **exact** | **123 (0,8483)** | **137 (0,9448)** | **+14** |
| **top-k strict** | **88 (0,6069)** | **141 (0,9724)** | **+53** |
| cibles verbes (POS gold) | 63 (0,9524) | **111/116 (0,9569)** | +48 cibles |
| cibles noms (POS gold) | 82 (0,7683) | **26/29 (0,8966)** | +… |
| échecs de cible | 22 (11/11) | **8 (3 hors candidats, 5 mal classés)** | −14 |

Rendement global (÷ 239 cibles) : top1 **0,5858**, top-k **0,5941**, exact **0,5732**.

## 2. Les trois corrections

| # | correction | gain | source |
|---|---|---|---|
| 1 | **segment précédent** (SUB après GV → verbe ; REL après GN → antécédent) | **+6 exact** (s012, s030, s052, s097, s124, s139) | **A7** (annotation indépendante) |
| 2 | **têtes des candidats S** (« … → Le livre » → `livre`) | **+45 top-k strict**, 0 exact | **A2** (diagnostic) |
| 3 | **lexique verbal anglais** (`fly`, `climb`, `flow`, `swim`, `get`, `smile`, `wait`, `belong`) | **+8 exact, +8 top1** | **A2** (F2) |

**Ce que ça dit** :

- **A7 a trouvé une erreur de convention** : `CONVENTION_CIBLE` disait « SUB → antécédent » ;
  le POS gold donne **69/69 cibles SUB = VERB**. La règle littérale ciblait le sujet (« cuisine »)
  au lieu du verbe gouverneur (« ouvre »). Corrigé et documenté.
- **A2 a trouvé que le top-k strict mesurait l'emballage des candidats**, pas la règle : 46 des
  57 échecs étaient des candidats non réduits à leur tête. Réduits → **+45**.
- **A2 a aussi chiffré F2** : 8 verbes anglais hors lexique coûtaient 8 points d'exact.
- **Le split verbe/nom était faux** : `_est_verbe` donnait 63/82, le POS gold donne **116/29** —
  la correction change la lecture des fiches antérieures (voir la note dans
  [conventions](rapport-pensee-conventions.md)).

## 3. Le modèle appris : **rejeté** (négatif documenté)

A3 a construit un classement appris (features de distance, côté, nature, rang ; validation
croisée pairs/impairs) : **142/145** en exact. Mais face à la règle vivante (**137**), le gain
tombe à **+5**, McNemar **7/2, p = 0,18**, bootstrap IC95 **[−0,7 ; +7,6] points** — **non
significatif** ; il introduit même 2 régressions (r048, r068). Le **prior de liste** seul
(rang 0, ordre gauche→droite→dedans) donne **139/145** (+2). Conclusion : **ne pas intégrer**
25 poids pour +5 non significatif ; une retouche déterministe (cible vide, verbe gouverneur à
distance 1) coûterait moins. Décision consignée, pas cachée.

## 4. Ce que ce banc ne dit pas

- **Les 8 échecs restants** : 3 hors candidats, 5 mal classés (non qualifiés plus finement).
- **Les 94 spans perdus** (48 REL, 33 SUB, 13 GP) : chez S, inchangés.
- **Le lexique anglais** est étendu **après** la mesure : le gain de +8 est une **borne haute**
  (risque d'ajustement au gold), dit explicitement.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 5. Ce qui pourrait rendre cette fiche fausse

- **la règle du segment précédent** dépend de la segmentation S (un GV mal délimité la trompe) ;
- **le lexique** peut avantager les phrases du gold (F2) ;
- **le split** dépend du POS gold, qui n'étiquette que les tokens présents ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 6. La suite

1. **Les 8 échecs** : les qualifier (3 hors candidats, 5 mal classés).
2. **Les 94 spans** : demander à S les REL/SUB (81 spans).
3. **La retouche déterministe** suggérée par A3 (cible vide, verbe à distance 1).
4. **Politique DRVM/native** : quand les poids seront là.

## 7. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — segment précédent, têtes, lexique.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — split sur le POS gold.
- [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) — `CONVENTION_CIBLE` corrigée.
- [`autotest.py`](../tools/pensee/autotest.py) — T176, T177, 180/180.
- [`pensee-attachement-v2.json`](pensee-attachement-v2.json) — les chiffres.
