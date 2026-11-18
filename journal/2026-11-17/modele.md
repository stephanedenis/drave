# 2026-11-17 — Modèles, entraînement, parcimonie, biologie

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (2)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 08:27 | `44fb939c` | GPU — L'AMP LIVRÉ (autocast + GradScaler dans entrainer_native), LE PAS RÉEL MESURÉ : 1 S SANS LES TÊTES (2,4× LE CPU NU), 9 S AVEC — LE 34 M RESTE TROP PETIT, LE GPU VAUT AUX PALIERS 100 M+ | `en-cours.md`, `README.md`, `README.md` (+5) |
| 15:29 | `0e5da7bd` | PROFILS SUR UN MODÈLE ENTRAÎNÉ (34 M) : BLOQUE +0,04 % DE PPL · FLOU +2,09 % · COURT −0,70 % — LE CONTRAT TIENT SUR LES LOGITS, PAS SUR LA PERPLEXITÉ | `drvm_profils.py`, `en-cours.md`, `README.md` (+14) |

## Chiffres du jour

`+0,04 %` · `+2,09 %` · `−0,70 %`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `d67a9bb1-090e-4f69-baf2-a831c00aa275` — Intérêt pour le FPGA maintenant (début 2026-11-17 09:50, 10.5 h) → [rapport](../sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/rapport.md) · [digest](../sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/digest.md)
- `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Documentation Drave avec diagrammes et implémentation (début 2026-10-31 17:40, 411.6 h) → [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md)

## Mesures et rapports touchés

- [reports/rapport-gpu-tandem.md](../../reports/rapport-gpu-tandem.md)
- [reports/rapport-profils-modele.md](../../reports/rapport-profils-modele.md)

<!-- notes -->

<!-- /notes -->
