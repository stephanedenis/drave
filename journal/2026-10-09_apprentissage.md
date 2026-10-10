# 2026-10-09 — Règles locales, hebbien, modulateurs, distillation

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [2026-10-09.md](2026-10-09.md). Convention : `docs/organisation-du-depot.md`.

## Commits du jour (12)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 00:07 | `9321cfc` | Distillation à l'échelle 384 : -12 % au total, et le gain CROÎT avec la taille | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 01:08 | `e87e37f` | Instrument : la convention SentencePiece nommée, le k-WTA appris, la FFN en Q8 | `main.rs`, `MANIFEST.md`, `digest.md` (+3) |
| 03:26 | `b822984` | Dim 512 : le routage seul perd, le routé DISTILLÉ gagne de 5,2 % | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 07:23 | `f3673af` | Les deux leviers ne se cumulent pas : la distillation n'ajoute rien au creux appris | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 07:43 | `a310b60` | Résumé : la distillation s'ajoute au routage, pas à la parcimonie | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 12:01 | `5eaa70b` | Notre hebbien différentiel face à la biologie : pourquoi il échoue, et par quoi le remplacer | `hebbien-differentiel-et-biologie.md`, `MANIFEST.md`, `digest.md` (+1) |
| 12:13 | `0307077` | Drave en impulsion pure serait-il un meilleur apprenant ? Pas en l'état, oui sous conditions nommées | `impulsion-pure-apprenant.md`, `MANIFEST.md`, `digest.md` (+1) |
| 12:23 | `5adb39b` | E7 et E8 implémentés et mesurés : la nouveauté empire la règle, la décorrélation est inerte | `impulsion-pure-apprenant.md`, `main.rs`, `model.rs` (+3) |
| 13:50 | `5c6413f` | Nos modèles à décharges ne vont pas sur GPU : trop petits, et le noyau GPU est dense | `modele-pour-drave.md`, `MANIFEST.md`, `digest.md` (+1) |
| 14:11 | `ed9034e` | M1 dans le moteur : le bus de modulation (nouveauté ou valeur), et la persistance de D | `main.rs`, `model.rs`, `MANIFEST.md` (+2) |
| 14:25 | `9a7d708` | Signal externe mesuré : meilleur des modulateurs, et toujours pire que la règle nue | `impulsion-pure-apprenant.md`, `main.rs`, `model.rs` (+3) |
| 14:30 | `722cc34` | Décorrélation en courbe de dose : elle améliore de façon monotone et converge vers « ne rien apprendre » | `impulsion-pure-apprenant.md`, `main.rs`, `model.rs` (+3) |

## Chiffres du jour

`5,2 %` · `-12 %` · `−12 %` · `−5,2 %`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Étapes du jour (17)

*Ce que l'agent a consigné en le faisant (lignes `⏵` du journal de session) :*

- **00:07** — La distillation à l'échelle 384 donne −12 % — le gain croît avec la taille
- **03:26** — Résultat de la nuit : le distillat d512 bat le dense (−5,2 %) après un routé qui perdait
- **04:37** — Mise en file de la journée : creux+distillé, et le test de sous-entraînement à 512
- **07:23** — Résultat : la distillation n'ajoute rien au creux appris (les deux leviers ne se cumulent pas)
- **09:15** — Mise en file de l'expérience décisive : élagage APPRIS + activations creuses
- **11:40** — Résultat : l'élagage APPRIS divise encore les lectures par deux, à qualité égale
- **12:00** — Recherche de notre règle hebbienne différentielle dans le dépôt (code, rapports, mesures)
- **12:01** — Rédaction : notre règle hebbienne différentielle face à la biologie
- **12:13** — Rédaction : Drave en impulsion pure serait-il un meilleur apprenant ? (ce que nos mesures disent)
- **12:14** — Implémentation d'E7 (modulation par nouveauté) et E8 (décorrélation anti-Hebbienne)
- **12:23** — Résultat : les deux mécanismes ne sauvent PAS la règle — la nouveauté empire les choses
- **13:25** — M1 : implémentation du bus de modulation par la VALEUR (et non la nouveauté)
- **13:50** — Réponse mesurée : nos modèles à décharges ne vont PAS sur le GPU — deux raisons distinctes
- **14:21** — Test du signal EXTERNE : modulateur lu depuis un fichier (NLL d'un enseignant)
- **14:25** — Signal externe mesuré : le meilleur des modulateurs, et toujours pire que rien
- **14:28** — Vérification de l'asymptote : la décorrélation converge-t-elle vers « ne rien apprendre » ?
- **14:30** — Courbe de dose complète : la règle locale converge vers « ne rien apprendre »

## Sessions actives ce jour

- `d31b3d9b` — Où en est-on (début 2026-10-08 09:11, 49.8 h) → [rapport](sessions/d31b3d9b/rapport.md) · [digest](sessions/d31b3d9b/digest.md)

## Mesures et rapports touchés

- [reports/rapport-campagne-benefices.md](../reports/rapport-campagne-benefices.md)

<!-- notes -->

<!-- /notes -->
