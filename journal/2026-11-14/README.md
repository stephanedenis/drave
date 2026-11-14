# 2026-11-14

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-14/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**1 commits** · **1 session(s)** · **1 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| docs | 1 | [docs.md](docs.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 320.4 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:52 | `64d9dd23` | J6.1 — g017 : LA RÈGLE DE L'ADVERBE FINAL HORS SUB EST REJETÉE (G017 GAGNÉ EN DEV, R264/R288 PERDUS EN TEST ; F1 0,7901, TEST −0,0028, ATTACHEMENT 236/237) ; CONVENTION DU GOLD À TRANCHER |

## Le récit de la journée (écrit à la main)

<!-- notes -->
**J6.1 — g017 : la règle de l'adverbe final hors de la SUB est rejetée.** Le bloc inclut
`yesterday` dans la SUB de `g017` (span 9:38 au lieu de 9:28). La règle demandée corrige
`g017` et retire un faux positif de `g005`, mais casse `r264` (« qu'il vient demain ») et
`r288` (« that he comes tomorrow ») : F1 **0,7902 → 0,7901**, dev **+0,0011**, test
**−0,0028**, attachement **237/238 → 236/237**. Les deux cas favorables sont en **dev**, les
deux défavorables en **test**. Rejet ; la convention du gold (inclure ou exclure l'adverbe
final) doit être tranchée avant toute règle. Fiche [`reports/rapport-g017.md`](../../reports/rapport-g017.md),
JSON [`reports/pensee-g017.json`](../../reports/pensee-g017.json).

**J6.2 — s065 : la REL « qui commence » prend le sujet du GV qui la suit.** Le gold attend
`elle`, le bloc prédisait `nage` (le GV le plus proche). La règle **REL suivie d'un GV → le
sujet de ce GV** corrige la seule cible fausse : **F1 0,7902 inchangé**, **POS 0,8625
inchangée**, **attachement 237/238 → 238/238 labels** (238/239 cibles, **0,9958**),
**exactitude sur les spans 0,9958 → 1,0**. Le gain est en **dev** (161/162 → 162/162) ; le
test reste à 76/76 car il n'a aucun cas déclencheur. Une seule annotation change, `s065` :
REL 5:17, `nage` → `elle`. Règle intégrée avec un test ; porte du bloc verte. Fiche
[`reports/rapport-s065.md`](../../reports/rapport-s065.md), JSON
[`reports/pensee-s065.json`](../../reports/pensee-s065.json).
<!-- /notes -->
