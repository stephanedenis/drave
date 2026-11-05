# B13 — la segmentation d'abord : F1 0,2862 → 0,4194, exact 158/160 (0,9875), couverture 160/239

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **183/183 portes** : le diagnostic de A12/A14 était juste — le trou n'était pas l'attachement mais le
> **découpage**. Six corrections générales du chunker font passer la **F1 syntagmes de 0,2862 à
> 0,4194**, la **tête de 0,4989 à 0,5930**, et la **couverture de 145 à 160 labels** (sur 239) ;
> l'attachement suit : **exact 158/160 = 0,9875**, **top-k 158/239**, par langue **fr 0,9915**
> (117/118) et **en 0,9762** (41/42) — l'anglais passe de **28 à 42 labels**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
> `_verbe_dans`, `_cible_hors_span`), [`autotest.py`](../tools/pensee/autotest.py) (38 assertions
> recalées) ; fiches amont [spans](rapport-spans-chunker.md) (A12), [gold anglais](rapport-gold-anglais.md)
> (A14) ; JSON [`pensee-segmentation-v4.json`](pensee-segmentation-v4.json).

## 1. Les six corrections

| # | correction | effet mesuré |
|---|---|---|
| 1 | **REL vs SUB par le segment précédent** : après un GN → relative, après un GV → complétive ; `because/although/if/while/as/since…` toujours SUB | labels 145 → 159, exact 141 → 145 |
| 2 | **GV à tête verbale** (pas seulement l'auxiliaire) + frontière à la préposition/déterminant/relatif | F1 0,2937 → 0,4033 |
| 3 | **GN s'arrête au verbe** (la tête après le déterminant est toujours prise) | passif 3/3, F1 0,4194 |
| 4 | **GP préposition + infinitif** (« à manger », « to eat ») | répare g012/r018 |
| 5 | **`_cible_hors_span` partout** (union et chunker, GP **et** SUB) | exact 144 → 152, anglais 30 → 38 |
| 6 | **`_verbe_dans` ne rend plus un auxiliaire** ; lexique de verbes communs (`go`, `cry`, `read`, `sleep`…, `rêver`, `sauter`, `marcher`) | exact 152 → 158 |

## 2. Les mesures (avant / après)

| mesure | avant (v3) | **après (v4)** |
|---|---:|---:|
| F1 syntagmes | 0,2862 | **0,4194** |
| F1 tête | 0,4989 | **0,5930** |
| labels au bon span | 145 | **160** |
| **exact / labels** | 141/145 (**0,9724**) | **158/160 (0,9875)** |
| top-k (sous-chaîne) | 142/239 | **158/239 (0,6611)** |
| couverture (labels / cibles) | 145/239 (0,6067) | **160/239 (0,6695)** |
| français (exact / spans) | 113/117 (0,9658) | **117/118 (0,9915)** |
| anglais (exact / spans) | 28/28 (1,000) | **41/42 (0,9762)** |
| spans perdus | 94 (48 REL, 33 SUB, 13 GP) | **79 (48 REL, 21 SUB, 10 GP)** |
| échecs de cible | 4 | **2** (r162, r309) |

**Ce que ça dit** :

- **Les 15 labels gagnés** viennent du découpage (REL/SUB anglais et français), pas d'un lexique.
- **L'anglais rattrape** : 28 → 42 labels, et l'exact tient (41/42).
- **Le rendement global monte** (0,6067 → 0,6695) sans perdre l'exactitude (0,9724 → 0,9875).
- **Les deux échecs restants** : `r162` (GP « on the wall » attaché au nom à gauche) et `r309`
  (pseudo-GV `Peut-être` du générateur S).

## 3. Ce que ce banc ne dit pas

- **Les 79 spans perdus** : 48 REL et 21 SUB, dont une partie reste chez S ; les deux règles de
  A12 (in-sample) en récupéreraient 84 — **non intégrées**.
- **Les 38 assertions recalées** : elles suivent la mesure, elles ne la valident pas.
- **Le lexique** : les verbes ajoutés sont **communs**, mais choisis après avoir vu les échecs ;
  c'est une extension ciblée, pas un lexique complet.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 4. Ce qui pourrait rendre cette fiche fausse

- **le test REL/SUB par le segment précédent** est une heuristique : dans « Pendant qu'il dort »,
  le GP « Pendant qu'il » précède la SUB, et c'est le GV qui tranche ;
- **la frontière du GV** au déterminant peut couper un GV à objet direct prépositionnel ;
- **le lexique** peut créer des faux positifs (un nom pris pour un verbe) ;
- **la mesure** est in-sample sur le gold de développement ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 5. La suite

1. **Les 2 échecs** (r162, r309).
2. **Les deux règles de spans** (A12), avec un gold tenu à l'écart.
3. **Le lexique anglais** : POS `_pos` (176 VERB tagués NOUN, A14).
4. **Politique DRVM/native** : quand les poids seront là.

## 6. Fichiers

- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — les six corrections.
- [`autotest.py`](../tools/pensee/autotest.py) — 38 assertions recalées, 183/183.
- [`pensee-segmentation-v4.json`](pensee-segmentation-v4.json) — les chiffres.
