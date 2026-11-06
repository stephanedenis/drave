# B13 — le gold coupé en dev/test : les gains généralisent (test 0,9814, dev 0,9811)

> **Instantané historique** : état au commit `85e4082b` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> Le gold 612 est coupé en **dev** (422 phrases, 163 cibles, 106 labels) et **test** (190, 76, 54)
> par un **hash stable de l'identifiant** (`crc32(id) % 3 == 0` → test), stratifié par source et
> par langue. Mesuré : **dev exact 104/106 (0,9811)**, **test 53/54 (0,9814)** — les règles de la
> journée ne sont donc pas un surajustement visible à ce niveau ; la F1 est même meilleure sur le
> test (0,4719 contre 0,4414).
>
> **Dispositif** : [`gold_split.py`](../tools/tests/linguistique/gold_split.py) (`dev`, `test`,
> `compter`), [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) ; JSON
> [`pensee-gold-split.json`](pensee-gold-split.json).

## 1. L'équilibre du split

| | phrases | cibles | labels | sources | langues |
|---|---:|---:|---:|---|---|
| **dev** | 422 | 163 | 106 | 15 hand / 302 reel / 105 synth | 277 fr / 145 en |
| **test** | 190 | 76 | 54 | 5 hand / 130 reel / 55 synth | 125 fr / 65 en |
| tout | 612 | 239 | 160 | 20 / 432 / 160 | 402 fr / 210 en |

## 2. La mesure sur les deux moitiés

| | dev | test |
|---|---:|---:|
| exact / labels | 104/106 (**0,9811**) | 53/54 (**0,9814**) |
| F1 syntagmes | 0,4414 | **0,4719** |
| F1 tête | 0,6347 | 0,6470 |
| français (exact / spans) | 79/79 (1,000) | 38/39 (0,9744) |
| anglais (exact / spans) | 25/27 (0,9259) | 15/15 (1,000) |

**Ce que ça dit** :

- **Le test n'est pas plus mauvais que le dev** : la segmentation et l'attachement généralisent.
- **Les deux langues tiennent** : fr 1,0 / 0,9744 ; en 0,9259 / 1,0.
- **Le test est petit** (54 labels) : un cas vaut 1,9 point ; les écarts < 2 cas ne sont pas lisibles.
- **La règle de conduite** : toute nouvelle règle se règle sur **dev** et ne s'accepte que si
  **test** ne baisse pas.

## 3. Ce que ce banc ne dit pas

- **Les 79 spans perdus** : la couverture est **106/163 = 0,6503 en dev** et **54/76 = 0,7105 en test** (total 160/239 = 0,6695) — pas identique.
- **Le surajustement fin** : un split ne détecte pas un ajustement qui profite aux deux moitiés
  (les règles ont été dessinées sur l'ensemble, donc sur test aussi) — c'est une limite de méthode.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 4. Ce qui pourrait rendre cette fiche fausse

- **le hash** : si les identifiants changeaient, le split changerait ;
- **l'échantillon test** (54 labels) : petit, les taux sont fragiles ;
- **la stratification** n'est pas exacte (5 hand au test) ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 5. La suite

1. **Les deux règles de spans** (A12) : réglées sur dev, évaluées sur test.
2. **`_pos` anglais** : 176 VERB tagués NOUN (A14).
3. **Les 3 échecs** d'attachement (r162, r309, r194).

## 6. Fichiers

- [`gold_split.py`](../tools/tests/linguistique/gold_split.py) — le split.
- [`pensee-gold-split.json`](pensee-gold-split.json) — l'équilibre et les mesures.
