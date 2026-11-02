# 2026-11-01 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (16)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 01:17 | `9366a219` | ÉTAT — LE BUDGET DE CONTEXTE REPASSE SOUS 4 000 MOTS (5 MOTS RETIRÉS) | `en-cours.md`, `README.md`, `mesures.md` (+5) |
| 01:38 | `bbee7a11` | ÉTAT — BUDGET DE CONTEXTE : LA LIGNE R4.4 SE RESSUERRE (T0 ≤ 4 000) | `en-cours.md`, `README.md`, `mesures.md` (+5) |
| 16:28 | `3c749d27` | B13 — AC-3 ET ALPHA-BÊTA : 8/8 PORTES, 1 495 NŒUDS/296 COUPES CONTRE 18 730 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+29) |
| 17:07 | `993f147e` | ÉTAT — LE BUDGET T0 REVIENT À 3 998 (TRIM DU BLOC D/R/A) | `en-cours.md`, `README.md`, `docs.md` (+4) |
| 18:40 | `deb0f96f` | B13 — LE BANC ANYTIME : A* BUT EN 32 NŒUDS, AUC 0,528/0,624 CONTRE 0,246/0,116 À L'ALÉATOIRE | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+27) |
| 20:21 | `0e5d99fe` | B13 — LE LABYRINTHE NON LINÉAIRE : BONNE POLITIQUE 17 NŒUDS/34 (SONDE 2), AVEUGLE 15/24 (SONDE 0) ; 13/13 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+24) |
| 20:25 | `5853b206` | B13 — LA PORTE NEURONALE : BONNE POLITIQUE 28 NŒUDS/58 (SONDE 5), AVEUGLE 200/483 SANS BUT ; 14/14 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+27) |
| 20:33 | `ad3da0b6` | B13 — LA PORTE APPRISE : Q-TABLE 67 ÉTATS, 30 NŒUDS/BUT (SONDE 7), 200 ÉPISODES ; 15/15 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+24) |
| 20:38 | `039e0500` | B13 — LA COURBE : 15/15 BUTS (50–800 ÉPISODES × 3 GRAINES), 30 NŒUDS, Q 52–83 ; 16/16 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+25) |
| 20:46 | `f9c112fd` | B13 — LA PORTE STOCHASTIQUE : 80 %, 30 NŒUDS/BUT, SONDE 7 ; 18/18 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+24) |
| 20:52 | `bcf6c281` | B13 — LA PORTE QUI SE REFERME : 27 NŒUDS/BUT, SONDE 5, COÛT 57 ; 20/20 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+24) |
| 20:55 | `e2770e7a` | B13 — LA PORTE À UN TOUR : 27 NŒUDS/BUT, SONDE 5, COÛT 57 ; 21/21 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+24) |
| 21:00 | `55b1523c` | B13 — LA Q-TABLE SUR LA PORTE MINUTE : 28 NŒUDS/BUT, SONDE 6, COÛT 62 ; 22/22 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+25) |
| 22:36 | `efaaa945` | B13 — LA ROBUSTESSE SUR 5 GRAINES : 5/5 BRUITS, 5/5 STABLES ; 33/33 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+17) |
| 22:52 | `75a03e15` | B13 — LA PORTE QUI BOUGE : HORLOGE t % 6, A* 28 NŒUDS, POLITIQUE BUT/10, 236 ÉTATS-Q ; 37/37 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+27) |
| 23:02 | `c7f4b8d7` | B13 — LA PÉRIODE QUI CHANGE : 3 PUIS 2 PAS, A* 28 NŒUDS, POLITIQUE BUT/10, 376 ÉTATS-Q ; 40/40 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+26) |

## Chiffres du jour

`80 %` · `× 3` · `0,528` · `0,624` · `0,246` · `0,116`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — Continue session work (début 2026-10-31 17:17, 31.6 h) → [rapport](../sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/rapport.md) · [digest](../sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md)
- `b6a672ec-3349-4a4c-9e23-4478aa823170` — Git push to origin remote (début 2026-11-01 13:28, 0.1 h) → [rapport](../sessions/b6a672ec-3349-4a4c-9e23-4478aa823170/rapport.md) · [digest](../sessions/b6a672ec-3349-4a4c-9e23-4478aa823170/digest.md)
- `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Documentation Drave avec diagrammes et implémentation (début 2026-10-31 17:40, 31.3 h) → [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md)
- `fe3c05f0-834b-44f2-8739-501865d652c1` — Lecture de en-cours.md et choix de tâche (début 2026-10-31 17:35, 31.4 h) → [rapport](../sessions/fe3c05f0-834b-44f2-8739-501865d652c1/rapport.md) · [digest](../sessions/fe3c05f0-834b-44f2-8739-501865d652c1/digest.md)

## Mesures et rapports touchés

- [reports/README.md](../../reports/README.md)
- [reports/rapport-pensee-ac3-alphabeta.md](../../reports/rapport-pensee-ac3-alphabeta.md)
- [reports/rapport-pensee-banc.md](../../reports/rapport-pensee-banc.md)
- [reports/rapport-pensee-bouge.md](../../reports/rapport-pensee-bouge.md)
- [reports/rapport-pensee-courbe.md](../../reports/rapport-pensee-courbe.md)
- [reports/rapport-pensee-ferme.md](../../reports/rapport-pensee-ferme.md)
- [reports/rapport-pensee-graines.md](../../reports/rapport-pensee-graines.md)
- [reports/rapport-pensee-labyrinthe.md](../../reports/rapport-pensee-labyrinthe.md)
- [reports/rapport-pensee-minute-apprise.md](../../reports/rapport-pensee-minute-apprise.md)
- [reports/rapport-pensee-minute.md](../../reports/rapport-pensee-minute.md)
- [reports/rapport-pensee-phase.md](../../reports/rapport-pensee-phase.md)
- [reports/rapport-pensee-porte-apprise.md](../../reports/rapport-pensee-porte-apprise.md)
- [reports/rapport-pensee-porte.md](../../reports/rapport-pensee-porte.md)
- [reports/rapport-pensee-stochastique.md](../../reports/rapport-pensee-stochastique.md)

<!-- notes -->

<!-- /notes -->
