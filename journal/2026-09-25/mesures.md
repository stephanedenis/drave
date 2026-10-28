# 2026-09-25 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (7)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 15:14 | `1f601a4e` | Élagage et approche par événement : où se situe le seuil de rentabilité | `README.md`, `rapport-eparsite.md`, `run_sparsity.py` (+1) |
| 15:34 | `8058018f` | Architecture push (AER) : oui, c'est pensable sur CPU — et c'est même à faire en premier | `README.md`, `cpu_aer.c`, `rapport-cpu-aer.md` (+1) |
| 15:53 | `90643b14` | Grappes afférentes/efférentes : imposer la structure à la conversion | `rapport-grappes.md`, `run_clusters.py` |
| 16:53 | `56b7603a` | Un LLM dense n'expose pas de grappes naturelles (mesuré sur Qwen2.5-0.5B) | `.gitignore`, `rapport-modele-reel.md`, `run_real_clusters.py` (+1) |
| 17:16 | `78e6a441` | Verdict valeur-unaire : réécrit (il se contredisait) | `rapport-valeur-unaire.md`, `run_value_encoding.py` |
| 17:31 | `e230f2ff` | 8 bits : la perfection est déjà atteinte — et correction du ×2,17 annoncé | `rapport-8bits.md`, `rapport-valeur-unaire.md`, `run_8bit_perfection.py` |
| 18:10 | `3b5eded1` | Correctif majeur : promotion float64 silencieuse (×30 sur le forward) | `rapport-harnais.md`, `transformer_np.py` |

## Chiffres du jour

`×30` · `×2,17`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `22bcae27-254b-47b2-acda-87467dab060c` — Étude de Qtrinet-bootstrap.md (début 2026-09-25 11:56, 74.8 h) → [rapport](../sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md) · [digest](../sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md)
- `27c99b10-c57e-4599-a23a-f7b1a54c17a1` — Tu écris un tokenizer BPE (début 2026-09-25 19:40, 0.2 h) → [rapport](../sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/rapport.md) · [digest](../sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/digest.md)

## Mesures et rapports touchés

- [reports/rapport-8bits.md](../../reports/rapport-8bits.md)
- [reports/rapport-cpu-aer.md](../../reports/rapport-cpu-aer.md)
- [reports/rapport-eparsite.md](../../reports/rapport-eparsite.md)
- [reports/rapport-grappes.md](../../reports/rapport-grappes.md)
- [reports/rapport-harnais.md](../../reports/rapport-harnais.md)
- [reports/rapport-modele-reel.md](../../reports/rapport-modele-reel.md)
- [reports/rapport-valeur-unaire.md](../../reports/rapport-valeur-unaire.md)

<!-- notes -->

<!-- /notes -->
