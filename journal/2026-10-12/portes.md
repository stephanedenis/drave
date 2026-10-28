# 2026-10-12 — Portes et vérifications

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (2)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 20:49 | `7a118fb9` | Docs : note de conception des lecteurs paralleles — le chiffre qui ouvre le chantier (pread par 8 fils : 3 995 Mo/s contre 1 126 a la demande), ce qui existe deja, MADV_POPULATE_READ a trancher avant tout, et les portes a tenir ecrites avant le code | `note-lecteurs-paralleles.md`, `2026-10-12.md`, `2026-10-12_modele.md` (+2) |
| 23:06 | `1793d189` | La porte de la paresse : l'inference prend le chemin push (93 tenseurs construits a la demande), les passes --ppl aucun — meme texte gourmand, chargement 5,2x plus rapide, et vue ROUGE avec un defaut volontaire | `gguf.rs`, `main.rs`, `model.rs` (+4) |

## Chiffres du jour

`3995 Mo`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `bbc0b8e2-1c7f-4d43-b1e5-7b7b72bd6ccf` — Avis sur le dépôt GitHub Strata (début 2026-10-12 08:44, 0.2 h) → [rapport](../sessions/bbc0b8e2-1c7f-4d43-b1e5-7b7b72bd6ccf/rapport.md) · [digest](../sessions/bbc0b8e2-1c7f-4d43-b1e5-7b7b72bd6ccf/digest.md)

## Mesures et rapports touchés

- [reports/rapport-chargement-paresseux.md](../../reports/rapport-chargement-paresseux.md)

<!-- notes -->

<!-- /notes -->
