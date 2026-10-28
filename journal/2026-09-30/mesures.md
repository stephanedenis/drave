# 2026-09-30 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (21)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 11:11 | `2c7271b1` | Transport : les chiffres du VRAI texte, plus sobres que ceux des identifiants synthétiques | `REPRISE.md`, `roadmap.md`, `README.md` (+5) |
| 11:14 | `fb8183a6` | L'entrée normée sur le fil : hypothèse RÉFUTÉE par la mesure | `roadmap.md`, `MANIFEST.md`, `digest.md` (+2) |
| 11:16 | `976cb818` | Transport : l'écart DÉCROÎT avec la longueur (la courbe le dit, pas moi) | `roadmap.md`, `MANIFEST.md`, `digest.md` (+2) |
| 11:29 | `9fe0c80e` | Feuille de route : les cinq mesures de la session au journal | `roadmap.md`, `MANIFEST.md`, `digest.md` (+1) |
| 12:37 | `148456fd` | Le rapport manquant de la phase 3.4, et les chiffres remis d'aplomb | `colab-reparti.md`, `format-flux.md`, `MANIFEST.md` (+6) |
| 12:46 | `f145f052` | Rapport : où mettre les bits du cache KV (facteur 130 à 840 à taille égale) | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 13:06 | `d89e3401` | Cache KV : int4/int4 mesuré (+364 %), la courbe a ses six premiers points | `rapport-placement-bits-kv.md` |
| 13:07 | `a2952f75` | Handoff : les garde-fous de l'après-midi et deux lignes de mesures | `REPRISE.md`, `roadmap.md`, `MANIFEST.md` (+2) |
| 13:08 | `00dcebc8` | Cohérence (suite) : le croisement push/pull, les comptes de lignes, et une erreur que j'avais écartée à tort | `README.md`, `REPRISE.md`, `contexte-long.md` (+7) |
| 13:09 | `5b2ec03e` | Rapport transport : l'en-tête dit maintenant ce que son tableau mesure | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 13:13 | `b1608642` | Index de la session : les huit chantiers, les défauts et par qui ils ont été trouvés | `digest.md`, `rapport.md`, `MANIFEST.md` (+3) |
| 15:30 | `ac7f593d` | Cache KV : la frontière tient à 4 096 comme à 8 192 | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 16:17 | `f28c60a5` | Mode 4 : le plafond cumulatif vérifié à l'octet près | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 17:01 | `80ba3d61` | Aiguille 9/9 dans les trois variantes de cache KV, et les vérifications de fin de journée | `MANIFEST.md`, `digest.md`, `rapport.md` (+2) |
| 17:01 | `b04dfd0f` | La politique du cache KV selon le régime : le meilleur réglage en octets n'est pas le meilleur en temps | `contexte-long.md`, `MANIFEST.md`, `digest.md` (+2) |
| 17:02 | `0c56c356` | REPRISE : la politique du cache KV complète (taille ET temps), et l'aiguille 9/9 | `REPRISE.md`, `MANIFEST.md`, `digest.md` (+1) |
| 18:12 | `fa6a4f38` | Collecte top-k : réallouer quand k GRANDIT, et un banc qui le prouve | `gpu.rs`, `main.rs`, `README.md` (+7) |
| 18:13 | `a891c310` | Rapport de sélection : le second passage k doublé, et la durée mal étiquetée | `README.md`, `digest.md`, `rapport.md` (+4) |
| 23:01 | `d29e043a` | Correction : `--infer` n'ignore PAS `--lot` (mon grep ne suivait pas la chaîne d'appels) | `README.md`, `digest.md`, `rapport.md` (+4) |
| 23:18 | `470e3e9d` | Revue adverse du sprint 3 : deux écarts graves, dans les phrases qui commentent les chiffres | `README.md`, `digest.md`, `rapport.md` (+7) |
| 23:52 | `2ae761cb` | Préremplissage déporté : ×4,5 sur un prompt de 3 961 jetons (286,6 → 63,8 s), perplexité à 2e-5 | `contexte-long.md`, `README.md`, `MANIFEST.md` (+4) |

## Chiffres du jour

`×4,5` · `63,8 s` · `3961 jetons` · `+364 %`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `15fd322f-7e9e-48c0-a970-f36335eb622a` — Tu travailles dans le dépôt (début 2026-09-30 11:47, 0.2 h) → [rapport](../sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md) · [digest](../sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/digest.md)
- `42059fde-f06f-4e2c-9a23-8292d887fb6e` — Tu es vérificateur de documentation (début 2026-09-30 12:20, 0.2 h) → [rapport](../sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md) · [digest](../sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/digest.md)
- `4d7a793b-74d1-4c46-bb53-21953fe91d87` — Tu es relecteur ADVERSARIAL, en (début 2026-09-30 22:59, 0.3 h) → [rapport](../sessions/4d7a793b-74d1-4c46-bb53-21953fe91d87/rapport.md) · [digest](../sessions/4d7a793b-74d1-4c46-bb53-21953fe91d87/digest.md)
- `5185ccb1-be24-4716-89df-62621e790444` — Tu es relecteur ADVERSARIAL dans (début 2026-09-30 17:03, 0.4 h) → [rapport](../sessions/5185ccb1-be24-4716-89df-62621e790444/rapport.md) · [digest](../sessions/5185ccb1-be24-4716-89df-62621e790444/digest.md)
- `564fbe3a-a859-4b3b-bd17-4da73a2f4e22` — Tu es relecteur ADVERSARIAL de (début 2026-09-30 18:07, 0.1 h) → [rapport](../sessions/564fbe3a-a859-4b3b-bd17-4da73a2f4e22/rapport.md) · [digest](../sessions/564fbe3a-a859-4b3b-bd17-4da73a2f4e22/digest.md)
- `5ce3f080-2d3d-467a-8ee1-df697f3f3e68` — Tu es relecteur ADVERSARIAL dans (début 2026-09-30 15:32, 0.3 h) → [rapport](../sessions/5ce3f080-2d3d-467a-8ee1-df697f3f3e68/rapport.md) · [digest](../sessions/5ce3f080-2d3d-467a-8ee1-df697f3f3e68/digest.md)
- `6d0c1d28-76e1-42f8-9e8c-7f88395f9e55` — Tu es relecteur ADVERSARIAL de (début 2026-09-30 20:04, 0.1 h) → [rapport](../sessions/6d0c1d28-76e1-42f8-9e8c-7f88395f9e55/rapport.md) · [digest](../sessions/6d0c1d28-76e1-42f8-9e8c-7f88395f9e55/digest.md)
- `7c876089-605c-4836-930e-925a66028509` — Tu es relecteur ADVERSARIAL dans (début 2026-09-30 13:10, 0.3 h) → [rapport](../sessions/7c876089-605c-4836-930e-925a66028509/rapport.md) · [digest](../sessions/7c876089-605c-4836-930e-925a66028509/digest.md)
- `7d0d2578-0048-4998-8494-7d2daef56769` — Tu travailles dans le dépôt (début 2026-09-30 11:47, 0.1 h) → [rapport](../sessions/7d0d2578-0048-4998-8494-7d2daef56769/rapport.md) · [digest](../sessions/7d0d2578-0048-4998-8494-7d2daef56769/digest.md)
- `8e04c99a-8ba1-4675-9f80-fa3338449b17` — Tu es VÉRIFICATEUR de documentation (début 2026-09-30 18:07, 0.2 h) → [rapport](../sessions/8e04c99a-8ba1-4675-9f80-fa3338449b17/rapport.md) · [digest](../sessions/8e04c99a-8ba1-4675-9f80-fa3338449b17/digest.md)
- `aa5f9fc5-9450-4118-b65f-e8b99a28519d` — Tu es vérificateur de documentation (début 2026-09-30 15:07, 0.2 h) → [rapport](../sessions/aa5f9fc5-9450-4118-b65f-e8b99a28519d/rapport.md) · [digest](../sessions/aa5f9fc5-9450-4118-b65f-e8b99a28519d/digest.md)
- `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` — Continue avec REPRISE.md (début 2026-09-28 14:46, 222.5 h) → [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md)
- `bcfe0b97-1795-4610-8e8b-b598ca1ba6cb` — Tu es relecteur ADVERSARIAL dans (début 2026-09-30 12:20, 0.3 h) → [rapport](../sessions/bcfe0b97-1795-4610-8e8b-b598ca1ba6cb/rapport.md) · [digest](../sessions/bcfe0b97-1795-4610-8e8b-b598ca1ba6cb/digest.md)
- `c25f97d1-9a4d-41da-b983-004f793afe43` — Tu travailles dans le dépôt (début 2026-09-30 11:47, 0.2 h) → [rapport](../sessions/c25f97d1-9a4d-41da-b983-004f793afe43/rapport.md) · [digest](../sessions/c25f97d1-9a4d-41da-b983-004f793afe43/digest.md)
- `c776b71f-525a-4bad-b83c-eff1c2d204ff` — Tu es relecteur ADVERSARIAL de (début 2026-09-30 18:36, 0.1 h) → [rapport](../sessions/c776b71f-525a-4bad-b83c-eff1c2d204ff/rapport.md) · [digest](../sessions/c776b71f-525a-4bad-b83c-eff1c2d204ff/digest.md)
- `da69b1fa-91b0-4c69-bb2b-58bf00e92e28` — Tu travailles dans le dépôt (début 2026-09-30 15:07, 0.1 h) → [rapport](../sessions/da69b1fa-91b0-4c69-bb2b-58bf00e92e28/rapport.md) · [digest](../sessions/da69b1fa-91b0-4c69-bb2b-58bf00e92e28/digest.md)

## Mesures et rapports touchés

- [reports/rapport-aiguille-topk.md](../../reports/rapport-aiguille-topk.md)
- [reports/rapport-coherence-docs.md](../../reports/rapport-coherence-docs.md)
- [reports/rapport-gpu-topk-selection.md](../../reports/rapport-gpu-topk-selection.md)
- [reports/rapport-logits-gpu-vs-cpu.md](../../reports/rapport-logits-gpu-vs-cpu.md)
- [reports/rapport-mode4-lot-listes.md](../../reports/rapport-mode4-lot-listes.md)
- [reports/rapport-phase3-reparti.md](../../reports/rapport-phase3-reparti.md)
- [reports/rapport-placement-bits-kv.md](../../reports/rapport-placement-bits-kv.md)
- [reports/rapport-prefill-reparti.md](../../reports/rapport-prefill-reparti.md)
- [reports/rapport-session-2026-09-30.md](../../reports/rapport-session-2026-09-30.md)
- [reports/rapport-transport-liste.md](../../reports/rapport-transport-liste.md)

<!-- notes -->

<!-- /notes -->
