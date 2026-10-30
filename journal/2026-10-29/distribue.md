# 2026-10-29 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (15)

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

## Chiffres du jour

`113,0068` · `148,7080` · `42,3176` · `148,9144` · `64,1160` · `59,0790` · `66,0379` · `1 %` · `58,3200` · `62,7357` · `9,1748` · `17,4702`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

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
- [reports/rapport-pannes-nommees.md](../../reports/rapport-pannes-nommees.md)
- [reports/rapport-r01-graphe-document.md](../../reports/rapport-r01-graphe-document.md)
- [reports/rapport-r02-controleur.md](../../reports/rapport-r02-controleur.md)
- [reports/rapport-r42-bloc-code.md](../../reports/rapport-r42-bloc-code.md)

<!-- notes -->

<!-- /notes -->
