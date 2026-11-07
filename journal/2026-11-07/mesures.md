# 2026-11-07 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (7)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 00:05 | `295e0d7b` | B13 — LES PRONOMS SUJETS ANGLAIS AUSSI : F1 0,7013 → 0,7438, TÊTE 0,8561, ATTACHEMENT PRÉSERVÉ ; 183/183 | `en-cours.md`, `README.md`, `README.md` (+7) |
| 00:13 | `efbae885` | B13 — LE NOM PROPRE SUJET EST UN GN : F1 0,7438 → 0,7535, TÊTE 0,865, ATTACHEMENT 236/237 ; 183/183 | `en-cours.md`, `README.md`, `mesures.md` (+9) |
| 00:45 | `149ecc5d` | FICHE — LES TROIS RÈGLES DE SEGMENTATION REJETÉES (ADVERBE FINAL, ROGNAGE S, ADJ/ADV) ; LE F1 RESTE À 0,7535 | `en-cours.md`, `README.md`, `docs.md` (+7) |
| 11:09 | `fffbbe5d` | PANINI — L'INVENTAIRE INTÉGRÉ AU PLAN : 14 DÉPÔTS, 7 AXES, 14 ATOMES, 9 CORPUS, TROIS INTÉGRATIONS MÛRES (UDHR+GÉNÉALOGIE, ATOMES↔NIVEAUX, CORPUS CIC) AVEC LEURS CONTRÔLES NÉGATIFS | `en-cours.md`, `semaine-autonome.md`, `README.md` (+14) |
| 12:40 | `25a6c0ff` | B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183 | `en-cours.md`, `roadmap.md`, `semaine-autonome.md` (+7) |
| 14:23 | `9a259953` | B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC), v1 TOUJOURS LUE | `en-cours.md`, `roadmap.md`, `semaine-autonome.md` (+27) |
| 14:45 | `8eb0cc49` | B13 — RESTITUTION v0 : 46/46 SURFACES EXACTES, MIROIR STRICT 0,1087, LE MIROIR TROUVE LES SAUTS DE LIGNE | `en-cours.md`, `roadmap.md`, `semaine-autonome.md` (+12) |

## Chiffres du jour

`0,1087` · `0,7535` · `0,7438` · `0,865` · `0,7013` · `0,8561`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `77d26bc7-1657-4c96-83c9-bba7c25dd828` — Tu travailles dans /home/stephane/Data13 (début 2026-11-07 00:49, 1.4 h) → [rapport](../sessions/77d26bc7-1657-4c96-83c9-bba7c25dd828/rapport.md) · [digest](../sessions/77d26bc7-1657-4c96-83c9-bba7c25dd828/digest.md)
- `7f247e9c-00ab-4bdf-bfba-2dc5c20d7cf0` — Tu travailles dans /home/stephane/Data13 (début 2026-11-07 02:09, 0.1 h) → [rapport](../sessions/7f247e9c-00ab-4bdf-bfba-2dc5c20d7cf0/rapport.md) · [digest](../sessions/7f247e9c-00ab-4bdf-bfba-2dc5c20d7cf0/digest.md)
- `b8f0bcb1-5609-4053-818b-ade88583a99b` — Tu travailles dans /home/stephane/Data13 (début 2026-11-07 00:49, 1.3 h) → [rapport](../sessions/b8f0bcb1-5609-4053-818b-ade88583a99b/rapport.md) · [digest](../sessions/b8f0bcb1-5609-4053-818b-ade88583a99b/digest.md)
- `bdefb627-485e-44d1-b11c-d15dd2e6b640` — Tu travailles en **lecture seule** (début 2026-11-07 09:56, 1.2 h) → [rapport](../sessions/bdefb627-485e-44d1-b11c-d15dd2e6b640/rapport.md) · [digest](../sessions/bdefb627-485e-44d1-b11c-d15dd2e6b640/digest.md)
- `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Documentation Drave avec diagrammes et implémentation (début 2026-10-31 17:40, 166.3 h) → [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md)

## Mesures et rapports touchés

- [reports/INDEX.md](../../reports/INDEX.md)
- [reports/README.md](../../reports/README.md)
- [reports/rapport-gn-pronom-sujet.md](../../reports/rapport-gn-pronom-sujet.md)
- [reports/rapport-inventaire-panini.md](../../reports/rapport-inventaire-panini.md)
- [reports/rapport-r035.md](../../reports/rapport-r035.md)
- [reports/rapport-restitution-v0.md](../../reports/rapport-restitution-v0.md)
- [reports/rapport-schema-v2.md](../../reports/rapport-schema-v2.md)

<!-- notes -->
**13 h 30 — la convention des GV.** Le classement des erreurs de GV (320 FP / 179 FN après
`r035`, 322/180 avant) donnait **144 FP de sujet (45 %)** et 73 d'objet. La règle **sujet hors du
GV** (le GV du générateur S commence au prédicat, le sujet est un GN) rend **F1 0,7549 → 0,7881** ;
l'**arrêt à l'adverbe final de temps** rend **+0,0026** ; les deux ensemble **0,7902** (dev
**0,7875**, test **0,7962**), **attachement 237/238 inchangé**, POS **0,8625**, **183/183**. Le
gold est **unanime** sur le sujet (**712/712 GV** commencent par VERB/AUX/ADV, aucun par un sujet)
mais **contradictoire** sur l'adverbe final (`r019`/`r186`, `r051`/`r189`). Fiche
[rapport-convention-gv.md](../../reports/rapport-convention-gv.md) · JSON
[pensee-convention-gv.json](../../reports/pensee-convention-gv.json).
<!-- /notes -->
