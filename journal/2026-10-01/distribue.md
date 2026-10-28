# 2026-10-01 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (7)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 07:40 | `e7db33bc` | DeepSeek-V4-Flash téléchargé (86,9 Go, 3 shards) : architecture et tokenizer lus depuis le shard 1, 784 tenseurs depuis le shard 2 — il manque le lien entre les deux | `plan-deepseek-v4-flash.md`, `README.md`, `MANIFEST.md` (+2) |
| 09:40 | `b83d284f` | Découpage des MoE : la fréquence suffit, la co-activation n'ajoute rien (accord 1,000) | `REPRISE.md`, `plan-deepseek-v4-flash.md`, `plan-mla-vision.md` (+13) |
| 11:58 | `6a2dfcb6` | Journal du bloc : mmap, nœud partiel, et le défaut prédit par la revue confirmé en vrai | `REPRISE.md`, `README.md`, `digest.md` (+5) |
| 21:13 | `4dc1c577` | README : la topologie et la conclusion qui se retourne | `README.md`, `README.md`, `MANIFEST.md` (+2) |
| 21:13 | `887d7514` | Topologie materielle : NVLink 25,8 Go/s, NUMA negligeable, pas de FPGA | `engine.rs`, `main.rs`, `README.md` (+4) |
| 21:21 | `3de46239` | Paires hyperthread : +27 % quand les cœurs manquent, rien quand on les a tous | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 21:22 | `d79f934c` | REPRISE : topologie materielle et affinites | `REPRISE.md`, `README.md`, `MANIFEST.md` (+2) |

## Chiffres du jour

`+27 %` · `25,8 Go` · `1,000` · `86,9 Go`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `11b2d312-9a7e-4a4e-814f-ed0384ed9d4d` — Tu es relecteur ADVERSARIAL autonome (début 2026-10-01 02:50, 0.1 h) → [rapport](../sessions/11b2d312-9a7e-4a4e-814f-ed0384ed9d4d/rapport.md) · [digest](../sessions/11b2d312-9a7e-4a4e-814f-ed0384ed9d4d/digest.md)
- `13446299-79d8-497c-ba83-673c176a4637` — Tu es relecteur ADVERSARIAL autonome (début 2026-10-01 00:54, 0.2 h) → [rapport](../sessions/13446299-79d8-497c-ba83-673c176a4637/rapport.md) · [digest](../sessions/13446299-79d8-497c-ba83-673c176a4637/digest.md)
- `18c3f6d0-5bb1-45bb-9f94-ab0e7812218d` — Relecture ADVERSARIALE ciblée (10 minut (début 2026-10-01 05:20, 0.1 h) → [rapport](../sessions/18c3f6d0-5bb1-45bb-9f94-ab0e7812218d/rapport.md) · [digest](../sessions/18c3f6d0-5bb1-45bb-9f94-ab0e7812218d/digest.md)
- `6551e4dc-b73d-4df7-8fc4-b8c9fdbb0688` — Tu es un relecteur adverse. (début 2026-10-01 11:57, 0.1 h) → [rapport](../sessions/6551e4dc-b73d-4df7-8fc4-b8c9fdbb0688/rapport.md) · [digest](../sessions/6551e4dc-b73d-4df7-8fc4-b8c9fdbb0688/digest.md)
- `8288d350-b68e-4245-b903-5ef6d71910b4` — You are doing an ADVERSARIAL (début 2026-10-01 05:52, 0.1 h) → [rapport](../sessions/8288d350-b68e-4245-b903-5ef6d71910b4/rapport.md) · [digest](../sessions/8288d350-b68e-4245-b903-5ef6d71910b4/digest.md)
- `8a0aa6e5-1a5e-450f-a6ea-070eed249d63` — Tu es un relecteur adverse. (début 2026-10-01 11:15, 0.2 h) → [rapport](../sessions/8a0aa6e5-1a5e-450f-a6ea-070eed249d63/rapport.md) · [digest](../sessions/8a0aa6e5-1a5e-450f-a6ea-070eed249d63/digest.md)
- `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` — Continue avec REPRISE.md (début 2026-09-28 14:46, 222.5 h) → [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md)
- `ff364db0-d28f-47eb-973e-f13bdafd35a2` — Relecture ADVERSARIALE de clôture, dans (début 2026-10-01 05:50, 0.1 h) → [rapport](../sessions/ff364db0-d28f-47eb-973e-f13bdafd35a2/rapport.md) · [digest](../sessions/ff364db0-d28f-47eb-973e-f13bdafd35a2/digest.md)

## Mesures et rapports touchés

- [reports/aiguille-30b.md](../../reports/aiguille-30b.md)
- [reports/aiguille-gpt-oss.md](../../reports/aiguille-gpt-oss.md)
- [reports/rapport-architecture-memoire.md](../../reports/rapport-architecture-memoire.md)
- [reports/rapport-decoupage-moe.md](../../reports/rapport-decoupage-moe.md)

<!-- notes -->

<!-- /notes -->
