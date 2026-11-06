# B13 — l'attachement v3 : exact 0,9448 → 0,9724, les noms à 1,0

> **Instantané historique** : état au commit `dcf7bc91` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **181/181 portes** : trois règles **générales** issues du diagnostic des 8 échecs (A9) sont
> intégrées — **R2** (un GP n'est pas gouverné par un mot de son span), **R3** (cible vide :
> génitif → tête du GN à gauche), **R4** (enclitique `appelle-moi` → `appelle`). Sur les 145
> segments au bon span : **exact 137 → 141 (0,9724)**, top1 **140 → 143 (0,9862)**, top-k 142
> (0,9793), **top-k strict 142 (0,9793)** ; les **cibles noms atteignent 29/29 = 1,0**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_cible_hors_span`,
> `_repli_cible_gp`, `_sans_enclitique`), [`autotest.py`](../tools/pensee/autotest.py) ;
> fiche A9 [échecs v2](rapport-echecs-v2.md) ; JSON [`pensee-attachement-v3.json`](pensee-attachement-v3.json).

## 1. Avant / après (145 segments au bon span)

| mesure | v2 | **v3** | écart |
|---|---:|---:|---:|
| top1 | 140 (0,9655) | **143 (0,9862)** | +3 |
| top-k | 142 (0,9793) | 142 (0,9793) | 0 |
| **exact** | **137 (0,9448)** | **141 (0,9724)** | **+4** |
| top-k strict | 141 (0,9724) | **142 (0,9793)** | +1 |
| cibles verbes (POS gold) | 111/116 (0,9569) | **112/116 (0,9655)** | +1 |
| **cibles noms (POS gold)** | 26/29 (0,8966) | **29/29 (1,0000)** | **+3** |
| exact multi-cibles (`cible in cibles`) | — | **143/145 (0,9862)** | mesure secondaire (A13) |

> **Note A13 (multi-cibles)** : le gold admet deux cibles pour **43/96 GP** ; adopter `cible in cibles`
> donnerait **143/145 (98,62 %)** et 143/239 (59,83 %), avec « +2 cas, dont 2 synthétiques »
> (s108, s122) — McNemar p=0,5 : correction de 2 cas, pas un gain de population. L'exact
> conservateur (`cibles[0]`) reste la mesure principale ; `exact_any` est publié à côté (T179).

Rendement global (÷ 239 cibles) : top1 **0,5983**, top-k 0,5941, exact **0,5900**.

## 2. Les trois règles (et celles qui ne le sont pas)

| règle | répare | portée | régression | intégrée |
|---|---|---:|---:|---|
| **R2** — un GP n'est pas gouverné par un mot de son span (`est prêt à manger` → `prêt`) | g012, r018 | 2 | 0 | oui |
| **R3** — cible vide d'un GP génitif → tête du GN à gauche (`de la voisine` → `chat`) | g002 | 1 | 0 | oui |
| **R4** — enclitiques (`appelle-moi` → `appelle`) | r230 | 1 | 0 | oui |
| R1 — lexique `rêver/sauter/marcher` | s108, s122, s041 | 2–3 | 0 | **non** (formes du gold) |
| R5 — ignorer un pseudo-GV `ADV` | r309 | 1 | 0 | **non** (n = 1) |

**Ce que ça dit** :

- **Les trois règles intégrées sont générales** : aucune forme lexicale du gold, aucune
  condition dépendant d'une phrase.
- **Les noms sont parfaits** (29/29) : la convention REL/GP nominale est comprise.
- **Les 4 échecs restants** sont : `s041` (`marche` hors lexique), `s108`/`s122` (`rêve`/`saute`
  hors lexique), `r309` (pseudo-GV `Peut-être` du S). Les trois premiers ne se réparent que par
  un **lexique** (risque d'ajustement au gold), le dernier par une règle étroite (n = 1).
- **A9 a mesuré les contrôles négatifs** : complétion naïve des GV (tout `VERB` = GV) → **132
  (−5)** ; R5 sans condition `ADV` → **131 (−6)** ; R3(a) n'est juste que **2/4** sur ses
  déclencheurs. Ces règles « évidentes » sont **nuisibles** et ne sont pas intégrées.
- **Convention de comptage** : la ventilation des échecs en « hors candidats / mal classés »
  dépend de la lecture (sous-chaîne : 3/5 ; égalité stricte : 4/4) — les deux sont publiées.

## 3. Ce que ce banc ne dit pas

- **Les 4 échecs** : non réparés (lexique ou n = 1).
- **Les 94 spans perdus** (48 REL, 33 SUB, 13 GP) : chez S ; le rendement global plafonne à
  145/239 = 0,6067.
- **Le lexique** : R1 dirait 145/145 sur ce gold, mais c'est une borne haute.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 4. Ce qui pourrait rendre cette fiche fausse

- **R3** ne s'applique qu'aux cibles vides (1 cas) : sa généralité n'est pas mesurée ;
- **R2** dépend de la liste de GV fournie par S et le chunker ;
- **R4** dépend de la liste d'enclitiques (`-moi`, `-toi`…) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 5. La suite

1. **Les 4 échecs** : un lexique verbal plus large (assumé) ou une règle `ADV` tenue à l'écart.
2. **Les 94 spans** : demander à S les REL/SUB (81 spans).
3. **Une seule passe S** par analyse (coût restant).
4. **Politique DRVM/native** : quand les poids seront là.

## 6. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — R2, R3, R4.
- [`autotest.py`](../tools/pensee/autotest.py) — valeurs v3, 181/181.
- [`rapport-echecs-v2.md`](rapport-echecs-v2.md) — le diagnostic A9 (8 échecs, 5 règles).
- [`pensee-attachement-v3.json`](pensee-attachement-v3.json) — les chiffres.
