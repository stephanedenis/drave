# 2026-10-09 — Règles locales, hebbien, modulateurs, distillation

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (12)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 00:07 | `9321cfcf` | Distillation à l'échelle 384 : -12 % au total, et le gain CROÎT avec la taille | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 01:08 | `e87e37f6` | Instrument : la convention SentencePiece nommée, le k-WTA appris, la FFN en Q8 | `main.rs`, `MANIFEST.md`, `digest.md` (+3) |
| 03:26 | `b8229844` | Dim 512 : le routage seul perd, le routé DISTILLÉ gagne de 5,2 % | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 07:23 | `f3673af8` | Les deux leviers ne se cumulent pas : la distillation n'ajoute rien au creux appris | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 07:43 | `a310b60e` | Résumé : la distillation s'ajoute au routage, pas à la parcimonie | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 12:01 | `5eaa70b6` | Notre hebbien différentiel face à la biologie : pourquoi il échoue, et par quoi le remplacer | `hebbien-differentiel-et-biologie.md`, `MANIFEST.md`, `digest.md` (+1) |
| 12:13 | `03070779` | Drave en impulsion pure serait-il un meilleur apprenant ? Pas en l'état, oui sous conditions nommées | `impulsion-pure-apprenant.md`, `MANIFEST.md`, `digest.md` (+1) |
| 12:23 | `5adb39bd` | E7 et E8 implémentés et mesurés : la nouveauté empire la règle, la décorrélation est inerte | `impulsion-pure-apprenant.md`, `main.rs`, `model.rs` (+3) |
| 13:50 | `5c6413fa` | Nos modèles à décharges ne vont pas sur GPU : trop petits, et le noyau GPU est dense | `modele-pour-drave.md`, `MANIFEST.md`, `digest.md` (+1) |
| 14:11 | `ed9034ec` | M1 dans le moteur : le bus de modulation (nouveauté ou valeur), et la persistance de D | `main.rs`, `model.rs`, `MANIFEST.md` (+2) |
| 14:25 | `9a7d7086` | Signal externe mesuré : meilleur des modulateurs, et toujours pire que la règle nue | `impulsion-pure-apprenant.md`, `main.rs`, `model.rs` (+3) |
| 14:30 | `722cc343` | Décorrélation en courbe de dose : elle améliore de façon monotone et converge vers « ne rien apprendre » | `impulsion-pure-apprenant.md`, `main.rs`, `model.rs` (+3) |

## Chiffres du jour

`5,2 %` · `-12 %`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `d31b3d9b-58e4-4d34-85fa-381b6f6a6a76` — Où en est-on (début 2026-10-08 09:11, 71.0 h) → [rapport](../sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/rapport.md) · [digest](../sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/digest.md)

## Mesures et rapports touchés

- [reports/rapport-campagne-benefices.md](../../reports/rapport-campagne-benefices.md)

<!-- notes -->

<!-- /notes -->
