# 2026-09-25 — Moteur : chargement, calcul, listes, quantification

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (7)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 15:26 | `3c6df267` | Encodage de structure : les deux listes signées éliminent la valeur | `README.md`, `rapport-encodage.md`, `rapport-precision.md` (+4) |
| 18:05 | `cbfc0ba8` | Harnais de test : perplexité 20,29 sur WikiText-2 + mesure du débit variable | `.gitignore`, `rapport-harnais.md`, `rapport-mode-listes.md` (+4) |
| 18:33 | `a44dcbba` | qtrinet-core : moteur d'exécution par listes en Rust (std seul) | `Cargo.lock`, `Cargo.toml`, `README.md` (+18) |
| 18:52 | `960cd360` | qtrinet-core : pool persistant (×10 sur le coût fixe) et décodeurs rapides | `README.md`, `engine.rs`, `list.rs` (+5) |
| 19:58 | `fa87057b` | Inférence complète en Rust : Qwen2.5-0.5B sans GPU, sans BLAS, sans dépendance | `README.md`, `engine.rs`, `gguf.rs` (+5) |
| 20:02 | `896499de` | Mode dense de comparaison : l'architecture evenementielle coute 8 % sur CPU | `README.md`, `engine.rs`, `list.rs` (+3) |
| 22:06 | `14a825db` | 4 bits : non, et la raison est plus intéressante que la réponse | `gguf.rs`, `main.rs`, `model.rs` (+1) |

## Chiffres du jour

`8 %` · `×10` · `perplexité 20,29`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `22bcae27-254b-47b2-acda-87467dab060c` — Étude de Qtrinet-bootstrap.md (début 2026-09-25 11:56, 74.8 h) → [rapport](../sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md) · [digest](../sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md)
- `27c99b10-c57e-4599-a23a-f7b1a54c17a1` — Tu écris un tokenizer BPE (début 2026-09-25 19:40, 0.2 h) → [rapport](../sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/rapport.md) · [digest](../sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/digest.md)

## Mesures et rapports touchés

- [reports/rapport-encodage.md](../../reports/rapport-encodage.md)
- [reports/rapport-harnais.md](../../reports/rapport-harnais.md)
- [reports/rapport-inference.md](../../reports/rapport-inference.md)
- [reports/rapport-mode-listes.md](../../reports/rapport-mode-listes.md)
- [reports/rapport-precision.md](../../reports/rapport-precision.md)

<!-- notes -->

<!-- /notes -->
