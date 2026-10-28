# 2026-09-28 — Moteur : chargement, calcul, listes, quantification

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (12)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 07:40 | `6b379f5c` | Q4_K et Q6_K en place : le 7B et le 1,5B Q4_K_M tournent | `README.md`, `digest.md`, `rapport.md` (+6) |
| 07:49 | `847f9abd` | Q6_K en place (AVX2) : tete divisee par 5, fidelite gagnee | `README.md`, `digest.md`, `rapport.md` (+3) |
| 08:24 | `f4434b99` | MoE : routage top-k et tranches par expert, le 30B-A3B tourne | `README.md`, `digest.md`, `rapport.md` (+4) |
| 11:21 | `2f87190f` | Tokenizer o200k verifie, briques gpt-oss, YaRN ; 120B charge et tourne | `convertisseur.md`, `README.md`, `digest.md` (+5) |
| 12:06 | `4270573c` | Chemin GPU operationnel : noyaux PTX, API pilote, tete de sortie deportee | `README.md`, `digest.md`, `rapport.md` (+6) |
| 12:45 | `e5ac235e` | Journal : session du 28/09 (chemin GPU, seuil mesure) | `README.md` |
| 12:57 | `f3b20f91` | Courbe qualite/octets par simulation de precision (5, 6, 7, 8 bits) | `digest.md`, `rapport.md`, `MANIFEST.md` (+2) |
| 13:35 | `31c057cd` | Rapport : le moteur sur du vrai travail (deux tests reels sur le 30B MoE) | `digest.md`, `rapport.md`, `MANIFEST.md` (+1) |
| 13:45 | `4a443992` | Session multi-tours interactive : le moteur sait tenir une conversation | `README.md`, `digest.md`, `rapport.md` (+3) |
| 14:24 | `19f88756` | gpt-oss : deux diagnostics de plus, dont un bug de cablage CLI | `README.md`, `digest.md`, `rapport.md` (+2) |
| 14:40 | `df18aefd` | Gabarit harmony de gpt-oss : fait. Refactorisation CLI : abandonnee, et pourquoi. | `digest.md`, `rapport.md`, `MANIFEST.md` (+3) |
| 20:06 | `d56d81f7` | Rotation : YaRN a retardement, et la temperature est la moitie nuisible | `REPRISE.md`, `contexte-long.md`, `README.md` (+6) |

## Sessions actives ce jour

- `22bcae27-254b-47b2-acda-87467dab060c` — Étude de Qtrinet-bootstrap.md (début 2026-09-25 11:56, 74.8 h) → [rapport](../sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md) · [digest](../sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md)
- `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` — Continue avec REPRISE.md (début 2026-09-28 14:46, 222.5 h) → [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md)
- `e7dfe34f-d596-4f98-93c2-cad5a92d3b1e` — Tu travailles dans un dépôt (début 2026-09-28 14:56, 0.1 h) → [rapport](../sessions/e7dfe34f-d596-4f98-93c2-cad5a92d3b1e/rapport.md) · [digest](../sessions/e7dfe34f-d596-4f98-93c2-cad5a92d3b1e/digest.md)

## Mesures et rapports touchés

- [reports/rapport-gpt-oss-perplexite.md](../../reports/rapport-gpt-oss-perplexite.md)
- [reports/rapport-travail-reel.md](../../reports/rapport-travail-reel.md)

<!-- notes -->

<!-- /notes -->
