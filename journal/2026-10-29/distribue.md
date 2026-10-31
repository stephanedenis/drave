# 2026-10-29 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (16)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 04:25 | `1d57756a` | DOCS — COMPTEURS 261/325 ET LIENS DE FICHES NON ÉCRITES | `en-cours.md`, `README.md`, `docs.md` (+1) |
| 11:50 | `4ffa34b7` | R0.1 — 51 PAGES, 1 423 RÉGIONS, FIDÉLITÉ 1,000 : LE GRAPHE DE DOCUMENT EST MESURÉ | `document-graph.md`, `R01-graphe-document.md`, `index.md` (+16) |
| 12:04 | `08149617` | R0.2 — À 30 % DU BUDGET, LE CONTRÔLEUR RÉCUPÈRE 100 % DES PASSAGES ; LE LECTEUR PLAFONNE À 25–75 % | `banc-lecture.md`, `lecteur-controleur.md`, `R02-controleur-lecture.md` (+15) |
| 12:24 | `7a8a441e` | DOCS — REPORTS/README SOUS BUDGET : 1 724 MOTS, INDEX EXHAUSTIF RENVOYÉ | `README.md`, `distribue.md`, `THEMES.md` (+1) |
| 15:51 | `2fc844b3` | A8.0 — PORTE-FLUX ÉPINGLÉE : PPL 61,9920 / 60,8135, TOLÉRANCE 5e-4 | `README.md`, `mesures.md`, `a80-porte-flux.json` (+3) |
| 15:52 | `4ccf641f` | R4.2 — LE BLOC CODE : 294 FICHIERS, 453 038 NŒUDS, 24/24 EXTRAITS EXÉCUTÉS | `bloc-code.md`, `R42-bloc-code.md`, `index.md` (+13) |
| 16:09 | `6872bef1` | A8.0 — PORTE-TOPOLOGIE ÉPINGLÉE : 17,4702 / 30,4363 / 42,5477 ; ÉTAT 3/33 | `en-cours.md`, `README.md`, `mesures.md` (+4) |
| 16:36 | `b49daabf` | A8.0 — PORTE-REPARTI ÉPINGLÉE : PPL 9,1748 ; ÉTAT 5/33 | `en-cours.md`, `README.md`, `mesures.md` (+5) |
| 16:44 | `f900db9a` | A8.3a — PORTE-FLUX : RÉGIME 1 % ÉPINGLÉ (58,3200 / 62,7357) | `en-cours.md`, `README.md`, `mesures.md` (+3) |
| 17:31 | `8c3ba915` | B10.2bis + A8.3b — LES PAS NE SUFFISENT PAS (1800 PAS : 10,2–11,4) ; LA TOPOLOGIE ENTRE DANS LE TABLEAU | `B10.2bis-decodeur-attention-croisee.md`, `en-cours.md`, `README.md` (+5) |
| 20:53 | `c1a9c37b` | A8.0 — PORTE-TRACE ÉPINGLÉE : 59,0790 ; ÉTAT 12/33 | `en-cours.md`, `README.md`, `modele.md` (+4) |
| 22:08 | `30a0c341` | A8.0 — PORTE-BUS ÉPINGLÉE : 64,1160 / 59,0790 / 66,0379 ; ÉTAT 15/33 | `en-cours.md`, `README.md`, `portes.md` (+4) |
| 22:19 | `36aa6bd5` | A8.0 — PORTE-BUS-SOCKET ÉPINGLÉE : 113,0068 / 148,7080 / 42,3176 / 148,9144 ; ÉTAT 17/33 | `en-cours.md`, `README.md`, `docs.md` (+4) |
| 22:28 | `7a46498b` | C11 — LA PANNE NOMME RÉGION, PAS ET OCTETS : PORTE-PANNES VERTE | `en-cours.md`, `main.rs`, `README.md` (+3) |
| 22:52 | `6eca9a15` | N3.5a — DÉCOUPAGE 0..k / k..n BIT-EXACT, K=0..4 ; 2 BUGS LATENTS CORRIGÉS ; PORTE 70 | `N3-operations-natives.md`, `en-cours.md`, `roadmap.md` (+8) |
| 23:23 | `50db63c0` | N3.5e — GÉNÉRATION RÉPARTIE TCP, DEUX CACHES, BIT-IDENTIQUE ; PORTE 74 | `N3-operations-natives.md`, `en-cours.md`, `roadmap.md` (+6) |

## Chiffres du jour

`113,0068` · `148,7080` · `42,3176` · `148,9144` · `64,1160` · `59,0790` · `66,0379` · `1 %` · `58,3200` · `62,7357` · `9,1748` · `17,4702`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `1f9394fb-6435-4928-9a03-2b258e5a28c5` — — (début 2026-10-29 14:10, 0.0 h) → [rapport](../sessions/1f9394fb-6435-4928-9a03-2b258e5a28c5/rapport.md) · [digest](../sessions/1f9394fb-6435-4928-9a03-2b258e5a28c5/digest.md)
- `3de141c0-089b-4ceb-8a2e-bd6d83044a5f` — Tu travailles dans le dépôt (début 2026-10-29 11:32, 0.3 h) → [rapport](../sessions/3de141c0-089b-4ceb-8a2e-bd6d83044a5f/rapport.md) · [digest](../sessions/3de141c0-089b-4ceb-8a2e-bd6d83044a5f/digest.md)
- `4a342d0f-bf6c-433f-bac9-c5a960b89a7f` — Tu travailles dans le dépôt (début 2026-10-29 11:32, 0.2 h) → [rapport](../sessions/4a342d0f-bf6c-433f-bac9-c5a960b89a7f/rapport.md) · [digest](../sessions/4a342d0f-bf6c-433f-bac9-c5a960b89a7f/digest.md)
- `71d57f53-8b41-4220-84dd-7bb9eedc88d9` — Évaluation des techniques de lecture rapide pour Drave (début 2026-10-29 07:42, 29.9 h) → [rapport](../sessions/71d57f53-8b41-4220-84dd-7bb9eedc88d9/rapport.md) · [digest](../sessions/71d57f53-8b41-4220-84dd-7bb9eedc88d9/digest.md)
- `8156fdcb-5033-4ba4-a5f3-f8a078e6e57e` — Réviser roadmap et backlog, établir priorités (début 2026-10-29 08:40, 28.9 h) → [rapport](../sessions/8156fdcb-5033-4ba4-a5f3-f8a078e6e57e/rapport.md) · [digest](../sessions/8156fdcb-5033-4ba4-a5f3-f8a078e6e57e/digest.md)
- `c3d0f0bd-e344-4600-a023-0ed50d25b48b` — Chantier inactif à examiner (début 2026-10-29 14:37, 18.7 h) → [rapport](../sessions/c3d0f0bd-e344-4600-a023-0ed50d25b48b/rapport.md) · [digest](../sessions/c3d0f0bd-e344-4600-a023-0ed50d25b48b/digest.md)
- `cf0456ab-e3f0-4f81-a4f5-bec4b3455f9f` — Mécanisme de mise à jour pair douteux (début 2026-10-29 15:51, 21.6 h) → [rapport](../sessions/cf0456ab-e3f0-4f81-a4f5-bec4b3455f9f/rapport.md) · [digest](../sessions/cf0456ab-e3f0-4f81-a4f5-bec4b3455f9f/digest.md)
- `d58fb6be-cedc-4236-a298-aa953dfb21b7` — Tu es dans /home/stephane/Data13TB/steph (début 2026-10-29 22:25, 0.5 h) → [rapport](../sessions/d58fb6be-cedc-4236-a298-aa953dfb21b7/rapport.md) · [digest](../sessions/d58fb6be-cedc-4236-a298-aa953dfb21b7/digest.md)
- `d622230d-649c-43cf-9202-da1eeb230259` — Tu es dans /home/stephane/Data13TB/steph (début 2026-10-29 22:25, 0.3 h) → [rapport](../sessions/d622230d-649c-43cf-9202-da1eeb230259/rapport.md) · [digest](../sessions/d622230d-649c-43cf-9202-da1eeb230259/digest.md)
- `f0969e87-af0c-43b1-93cf-f278d9c90846` — Optimiser couches linguistiques jeux symboliques (début 2026-10-25 21:28, 89.0 h) → [rapport](../sessions/f0969e87-af0c-43b1-93cf-f278d9c90846/rapport.md) · [digest](../sessions/f0969e87-af0c-43b1-93cf-f278d9c90846/digest.md)

## Mesures et rapports touchés

- [reports/INDEX.md](../../reports/INDEX.md)
- [reports/README.md](../../reports/README.md)
- [reports/rapport-a80-porte-bus-socket.md](../../reports/rapport-a80-porte-bus-socket.md)
- [reports/rapport-a80-porte-bus.md](../../reports/rapport-a80-porte-bus.md)
- [reports/rapport-a80-porte-flux.md](../../reports/rapport-a80-porte-flux.md)
- [reports/rapport-a80-porte-reparti.md](../../reports/rapport-a80-porte-reparti.md)
- [reports/rapport-a80-porte-topologie.md](../../reports/rapport-a80-porte-topologie.md)
- [reports/rapport-a80-porte-trace.md](../../reports/rapport-a80-porte-trace.md)
- [reports/rapport-a80-portes-ppl.md](../../reports/rapport-a80-portes-ppl.md)
- [reports/rapport-a83a-flux.md](../../reports/rapport-a83a-flux.md)
- [reports/rapport-a83b-regimes.md](../../reports/rapport-a83b-regimes.md)
- [reports/rapport-b102bis-decodeur.md](../../reports/rapport-b102bis-decodeur.md)
- [reports/rapport-n3.5a-deux-regions.md](../../reports/rapport-n3.5a-deux-regions.md)
- [reports/rapport-n3.5e-generation.md](../../reports/rapport-n3.5e-generation.md)
- [reports/rapport-pannes-nommees.md](../../reports/rapport-pannes-nommees.md)
- [reports/rapport-r01-graphe-document.md](../../reports/rapport-r01-graphe-document.md)
- [reports/rapport-r02-controleur.md](../../reports/rapport-r02-controleur.md)
- [reports/rapport-r42-bloc-code.md](../../reports/rapport-r42-bloc-code.md)

<!-- notes -->

<!-- /notes -->
