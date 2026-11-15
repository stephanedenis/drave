# 2026-11-15 — Outils et harnais

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (1)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 06:23 | `503da67e` | BILAN DE LA SEMAINE — LE PRODUIT (F1 0,7902, 238/239, TAGGER 95,75), PANINI BORNÉ (DEUX NÉGATIFS), LA COORDINATION, LE HARNAIS (38 LANCEMENTS) ; LES 5 DÉCISIONS EXÉCUTÉES | `en-cours.md`, `README.md`, `mesures.md` (+7) |

## Chiffres du jour

`0,7902`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Documentation Drave avec diagrammes et implémentation (début 2026-10-31 17:40, 357.3 h) → [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md)

## Mesures et rapports touchés

- [reports/INDEX.md](../../reports/INDEX.md)
- [reports/README.md](../../reports/README.md)
- [reports/rapport-bilan-semaine.md](../../reports/rapport-bilan-semaine.md)

<!-- notes -->
### W5 — la règle de rôle et son banc

Nouveau module pur [`tools/roles_gp.py`](../../tools/roles_gp.py) (règle + 24 cas), mesure
[`tools/restitution_v3.py`](../../tools/restitution_v3.py) (préparation, appariement v2/v3,
`mesurer_banc_v3`, `mesurer_gold_analyseur_v3`, contrôles), script
[`tools/mesurer_restitution_v3.py`](../../tools/mesurer_restitution_v3.py) et **29** tests
[`tools/tests/test_restitution_v3.py`](../../tools/tests/test_restitution_v3.py). Le CLI gagne
`restituer --roles-v3` (opt-in) ; `--roles` v2 est inchangé et la suite v2 (17 tests) passe.
<!-- /notes -->
