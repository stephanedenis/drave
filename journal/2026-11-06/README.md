# 2026-11-06

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-06/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**8 commits** · **3 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 2 | [distribue.md](distribue.md) |
| docs | 1 | [docs.md](docs.md) |
| mesures | 3 | [mesures.md](mesures.md) |
| portes | 2 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `3fb87dc7-7d24-42e2-a68e-e37e2734b755` | Tu travailles dans le dépôt | 2026-11-05 23:24 | 1.7 h | [rapport](../sessions/3fb87dc7-7d24-42e2-a68e-e37e2734b755/rapport.md) · [digest](../sessions/3fb87dc7-7d24-42e2-a68e-e37e2734b755/digest.md) |
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 129.3 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |
| `ea169cb1-75d7-43fa-b69d-5e2a210f6c38` | Tu travailles dans le dépôt | 2026-11-05 23:24 | 1.3 h | [rapport](../sessions/ea169cb1-75d7-43fa-b69d-5e2a210f6c38/rapport.md) · [digest](../sessions/ea169cb1-75d7-43fa-b69d-5e2a210f6c38/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:09 | `41cae3e5` | JOURNAL — LE 06/11 S'OUVRE SUR LA NUIT DU DÉCOUPAGE : 220/220, COUVERTURE 0,9205, 19 SPANS |
| 00:12 | `68a8717b` | JOURNAL — LE 06/11 AU FORMAT DE L'INDEX (EN-TÊTE, LIENS, BLOC NOTES) |
| 00:28 | `653a7981` | B13 — LES DEUX DERNIÈRES RÉGRESSIONS (s037, r303) : EXACT 221/221 (1,0000), COUVERTURE 0,9247, 18 SPANS ; AUDIT V10 INTÉGRÉ, V10 CORRIGÉE ; 183/183 |
| 00:56 | `9a1b3914` | PORTES — 11 DOCSTRINGS ALIGNÉES SUR LA V11 (221/221, 18 SPANS, TOP-K 220) ; AUDIT V10 FINAL COMMITTÉ ; 183/183 |
| 01:00 | `3ab768f7` | B13 — LA CLÔTURE DE LA NUIT : EXACT 221/221, COUVERTURE 0,9247, DEV 152/152, TEST 69/69 ; 18 SPANS DONT 17 INATTEIGNABLES |
| 01:26 | `0911ae29` | B13 — 222/222 (1,0000) : LE DERNIER MARQUEUR AMBIGU (when APRÈS UN GN), COUVERTURE 0,9289, 17 SPANS TOUS INATTEIGNABLES ; 183/183 |
| 01:29 | `5523de51` | JOURNAL ET ROADMAP — LA CIBLE DE A17 ATTEINTE : 222/222, COUVERTURE 0,9289, 17 SPANS INATTEIGNABLES |
| 01:57 | `17078889` | PORTES — LA ROUGE TOLÉRÉE cascade_pos DOCUMENTÉE : LA FUSION AVEC LE CONTRAT PASSE SOUS L'HEURISTIQUE (0,7465 < 0,7581) APRÈS LE POS CONTEXTUEL |

## Le récit de la journée (écrit à la main)

<!-- notes -->
La tranche autonome commencée le 05/11 à 16 h 40 continue jusqu'à 8 h. Elle porte sur la même
ligne : **B13**, l'attachement et son découpage.

**État au passage de minuit.** L'attachement est à **220/220 (1,0000)** sur les **220 labels** dont
le span est prédit (sur 239 cibles), la **couverture** à **0,9205**, la **F1 syntagmes** à
**0,5880** (union ; S 0,5014, chunker 0,6203), la tête à **0,7388** ; **fr 134/134, en 86/86** ;
**183/183 portes**. Les **19 spans** restants sont, pour 17 d'entre eux, inatteignables sans
corriger le gold ou le lexique (12 formes synthétiques, 4 GP du gold sans préposition, une
tokenisation `qu'il`).

**Les fiches du jour** : `rapport-pensee-v9.md` (la garde PRON), `rapport-pensee-v10.md` (le `-ée`
et la garde déterminant du GP), `rapport-audit-r1r3.md` (l'audit A19 : +17 net, 7 régressions
corrigées depuis), et les audits de cohérence `rapport-coherence-fiches-v8.md`.
**La clôture de la nuit (1 h 15).** L'exact est **saturé** : **221/221 (1,0000)** sur les labels
prédits, **couverture 0,9247**, **F1 0,5843**, **dev 152/152, test 69/69**. Les **18 spans**
restants sont, pour 17, inatteignables (12 formes synthétiques, 4 GP du gold sans préposition, une
tokenisation `qu'il`) ; le dernier (`g017`) est un arbitrage d'adverbe assumé. Les fiches
`rapport-pensee-v9.md`, `-v10.md`, `-v11.md` et les audits `rapport-audit-r1r3.md`,
`rapport-audit-v10.md`, `rapport-dev-test-v10.md` portent les mesures et les corrections.
**La cible de A17 (1 h 30).** Le dernier écart était un marqueur ambigu : « when » après un GN est
une **relative** (« The day when we left »), ailleurs une subordonnée. Avec `AMBIGUES_REL`,
l'attachement est à **222/222 (1,0000)** — **fr 136/136, en 86/86** —, la **couverture** à
**0,9289**, la **F1** à **0,5893** ; **dev 153/153, test 69/69**. Les **17 spans** restants sont
**tous inatteignables** (12 formes synthétiques, 4 GP du gold sans préposition, une tokenisation).
La journée referme ainsi le chantier ouvert le matin à 137/145 sur 145 labels (couverture 0,6067).
<!-- /notes -->
