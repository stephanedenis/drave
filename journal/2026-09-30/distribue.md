# 2026-09-30 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (30)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 08:58 | `ac7ccb11` | Phase 0 : la trace du flux et le diff par couche sont en place et démontrés | `roadmap.md`, `main.rs`, `model.rs` (+4) |
| 09:01 | `47aaae91` | Phase 0.4 : profilage par neurone depuis une trace | `roadmap.md`, `MANIFEST.md`, `digest.md` (+2) |
| 10:12 | `6d0bb1d1` | Phase 0.3bis : le rejeu d'un flux redonne exactement le même résultat | `roadmap.md`, `main.rs`, `model.rs` (+3) |
| 10:16 | `98ed93e1` | Phase 0.3ter : trace et rejeu sur le chemin par LOTS | `model.rs`, `MANIFEST.md`, `digest.md` (+1) |
| 10:26 | `5d131288` | Phase 3 : le transport de flux entre deux nœuds (défaut ouvert, chiffré) | `roadmap.md`, `main.rs`, `model.rs` (+3) |
| 10:36 | `0fdd4c91` | Spécification du format de flux, et modèle de coût par couche | `format-flux.md`, `MANIFEST.md`, `digest.md` (+2) |
| 10:36 | `7e028daf` | Analyse pure du flux : densité, persistance et recouvrement par couche | `roadmap.md`, `MANIFEST.md`, `digest.md` (+3) |
| 10:44 | `8037ba80` | Phase 3 : le calcul réparti redevient fidèle — écart 0,00e0 | `.roadmap.md.kate-swp`, `format-flux.md`, `roadmap.md` (+7) |
| 11:02 | `7b88131f` | Phase 3.2 : le flux voyage en LISTE — courbe taille/fidélité | `format-flux.md`, `main.rs`, `model.rs` (+6) |
| 11:08 | `27f46c1f` | Répétition Colab : nœud moteur écoutable au-delà de localhost + recette | `colab-reparti.md`, `main.rs`, `README.md` (+3) |
| 11:14 | `4396f257` | REPRISE : le calcul réparti tient debout (§6bis) et les commandes pour le rejouer | `REPRISE.md`, `MANIFEST.md`, `digest.md` (+1) |
| 11:30 | `f4bce59e` | tools/pair_factice.py : les trois modes, et plusieurs clients | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 11:34 | `3ae3f455` | Découpage fidèle à 1 024 jetons : 0,00e0 sur 1 024 flux | `REPRISE.md`, `MANIFEST.md`, `digest.md` (+2) |
| 11:39 | `1cf47143` | REPRISE et journal : la formule de latence et la validation à 1 024 jetons | `REPRISE.md`, `roadmap.md`, `MANIFEST.md` (+2) |
| 11:39 | `e80ceb1f` | Phase 3.3 : le coût du découpage en fonction de la latence, mesuré | `colab-reparti.md`, `roadmap.md`, `MANIFEST.md` (+4) |
| 11:41 | `2184fc52` | Banc réparti : plus de flux pour le dernier jeton | `main.rs`, `MANIFEST.md`, `digest.md` (+1) |
| 12:11 | `d59d0618` | Protocole v4 : les top-k voyagent aussi (défaut n°1 de l'audit) | `format-flux.md`, `main.rs`, `MANIFEST.md` (+4) |
| 12:17 | `6b3b53f0` | DRVF v2 sur le disque : −49,87 % de trace, rejeu identique | `format-flux.md`, `main.rs`, `model.rs` (+5) |
| 12:19 | `25c42c38` | Deux silences de plus, relevés par l'audit : trace en inférence, modes concurrents | `main.rs`, `MANIFEST.md`, `digest.md` (+1) |
| 12:30 | `ae850435` | DRVF v3 : −66 % de trace au total, pour +0,074 % de perplexité | `format-flux.md`, `main.rs`, `model.rs` (+9) |
| 12:31 | `bd4eac84` | REPRISE : la session 12h-15h (lots sur le fil, DRVF v2/v3, protocole v4, audit) | `REPRISE.md`, `digest.md`, `rapport.md` (+5) |
| 12:36 | `a9fff24e` | Deux bugs de protocole trouvés par la relecture, pas par un banc | `main.rs`, `digest.md`, `rapport.md` (+5) |
| 12:59 | `c2ff9a8c` | Mode lot sur un lien latent : 18× (2,6 s contre 47,6 s) | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 13:00 | `da6415b4` | Colab : le mode lot chiffré dans la recette (2,6 s contre 47,6 s à 20 ms par message) | `colab-reparti.md`, `MANIFEST.md`, `digest.md` (+1) |
| 13:07 | `d0d0edeb` | Cohérence : versions et comptes de flux remis d'aplomb partout | `format-flux.md`, `plan-prefill-reparti.md`, `roadmap.md` (+5) |
| 13:11 | `7c6bd5d4` | Format de flux : la taille par neurone actif, dense et creuse | `format-flux.md`, `digest.md`, `rapport.md` (+3) |
| 15:29 | `6b6ac177` | Documents : protocole v5 et mode 4 (lot en listes) | `format-flux.md`, `roadmap.md`, `MANIFEST.md` (+2) |
| 16:16 | `1dd39521` | Index : le mode 4, le protocole v5, le plan GPU et le décompte des relectures | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 17:34 | `645c3eed` | Quatrième relecture : deux défauts graves (client et nœud tués par 83 octets) — corrigés | `plan-mode4-lot-listes.md`, `main.rs`, `digest.md` (+6) |
| 19:00 | `64c9d262` | Top-k déporté : une synchro en trop, un budget de scores, un échec dit une seule fois | `gpu.rs`, `model.rs`, `README.md` (+3) |

## Chiffres du jour

`2,6 s` · `47,6 s` · `20 ms` · `−66 %` · `+0,074 %` · `0,074` · `−49,87 %` · `1024 jetons`

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

- [reports/rapport-analyse-flux.md](../../reports/rapport-analyse-flux.md)
- [reports/rapport-compacite-trace.md](../../reports/rapport-compacite-trace.md)
- [reports/rapport-drapeaux-ignores.md](../../reports/rapport-drapeaux-ignores.md)
- [reports/rapport-mode4-lot-listes.md](../../reports/rapport-mode4-lot-listes.md)
- [reports/rapport-phase3-reparti.md](../../reports/rapport-phase3-reparti.md)
- [reports/rapport-placement-bits-kv.md](../../reports/rapport-placement-bits-kv.md)
- [reports/rapport-prefill-reparti.md](../../reports/rapport-prefill-reparti.md)
- [reports/rapport-session-2026-09-30.md](../../reports/rapport-session-2026-09-30.md)
- [reports/rapport-transport-liste.md](../../reports/rapport-transport-liste.md)

<!-- notes -->

<!-- /notes -->
