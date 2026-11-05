# B13 — la mesure par langue : l'exact tient, la couverture anglaise non

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **183/183 portes** : la mesure d'attachement est désormais **scindée par langue**. Le français
> donne **113/117 (0,9658)** et l'anglais **28/28 (1,000)** — mais l'anglais n'a que **28 labels
> sur 88 cibles** (contre 117/151 en français). L'échec anglais est un échec de **couverture**
> (segmentation), pas d'attachement — ce que A14 avait établi (60 des 94 spans perdus sont anglais).
>
> **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py)
> (`attachement.par_langue`), [`autotest.py`](../tools/pensee/autotest.py) (T180) ;
> fiche A14 [gold anglais](rapport-gold-anglais.md) ; JSON [`pensee-par-langue.json`](pensee-par-langue.json).

## 1. Les deux langues

| langue | cibles | labels | exact | top-k | exact / spans |
|---|---:|---:|---:|---:|---:|
| **français** | 151 | **117** (77,5 %) | 113 | 114 | **0,9658** |
| **anglais** | 88 | **28** (31,8 %) | 28 | 28 | **1,0000** |
| tout | 239 | 145 | 141 | 142 | 0,9724 |

**Ce que ça dit** :

- **L'attachement est juste dans les deux langues** (0,9658 / 1,000) : les règles v3 ne sont pas
  françaises.
- **La couverture anglaise est le trou** : 28 labels sur 88 cibles (31,8 %) contre 77,5 % en
  français. Le générateur S ne segmente pas l'anglais (A14 : 277 GV, 0 GN/GP/REL/SUB), et le
  chunker ne produit pas de REL/SUB.
- **La conséquence** : le rendement global (0,59) est tiré vers le bas par les 60 spans anglais
  perdus, pas par des cibles mal attachées.
- **La négative est explicite** : 0,318 de couverture anglaise, ce n'est pas un attachement.

## 2. Ce que ce banc ne dit pas

- **Les 60 spans anglais** : leur production est chez S (ou un chunker anglais) — piste A12/A14.
- **Les 25 phrases anglaises à corriger** (A14) : hygiène du gold, hors mesure d'attachement.
- **Le gold 612** : 432 réels + 160 synthétiques + 20 de `gold.py`.

## 3. Ce qui pourrait rendre cette fiche fausse

- **la langue** vient du gold (`langue`), pas d'une détection ;
- **28 labels anglais** : petit échantillon, l'exact 1,000 est fragile ;
- un **audit** qui ne vérifie pas ces mesures (T28 les couvrent).

## 4. La suite

1. **Segmenter l'anglais** (le seul levier des 60 spans).
2. **Les deux règles de spans** de A12 (in-sample, à tenir à l'écart).
3. **Les 4 échecs** d'attachement (lexique ou n = 1).
4. **Politique DRVM/native** : quand les poids seront là.

## 5. Fichiers

- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `par_langue`.
- [`autotest.py`](../tools/pensee/autotest.py) — T180, 183/183.
- [`pensee-par-langue.json`](pensee-par-langue.json) — les deux langues.
