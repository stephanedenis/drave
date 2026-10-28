# 2026-10-02 — Attention, fenêtre, puits

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (6)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 10:56 | `e0328fba` | P0 : le flux se compte par provenance — attention, experts, partagé | `REPRISE.md`, `plan-deepseek41-complet.md`, `list.rs` (+7) |
| 11:22 | `567d3b3f` | P2 (1/2) : le troisième chemin d'attention — celui de DeepSeek-V4 | `model.rs`, `MANIFEST.md`, `digest.md` (+1) |
| 12:12 | `329ce1da` | REPRISE : les trois chemins d'attention, les hyper-connexions, l'exécution bornée et les outils de comparaison | `REPRISE.md`, `MANIFEST.md`, `digest.md` (+1) |
| 22:23 | `417f8f25` | P9 : le matvec f32 de V4.1 parallélisé par LIGNES — ×9,34 sur l'attention, ×3 sur la passe, zéro bit changé | `plan-deepseek41-complet.md`, `model.rs`, `README.md` (+6) |
| 22:31 | `a0ea42d4` | Sprint 15 : le profil V4 dit maintenant où passent les 1 003 ms/token d'attention (4,5 % seulement dans le calcul) | `main.rs`, `model.rs`, `README.md` (+5) |
| 22:32 | `7df398ef` | Sprint 15 : clôture (107 min) — ×9,34 sur l'attention sans changer un bit, et le profil complété | `README.md`, `MANIFEST.md`, `digest.md` (+3) |

## Chiffres du jour

`×9,34` · `4,5 %` · `1003 ms` · `×3`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `1820cf6b-c8a4-411c-894c-31195b9ff7a8` — Tu es un vérificateur ADVERSARIAL (début 2026-10-02 19:29, 0.1 h) → [rapport](../sessions/1820cf6b-c8a4-411c-894c-31195b9ff7a8/rapport.md) · [digest](../sessions/1820cf6b-c8a4-411c-894c-31195b9ff7a8/digest.md)
- `18b8879c-f211-43b8-9908-cf65e509b21d` — Tu travailles dans le dépôt (début 2026-10-02 15:03, 0.2 h) → [rapport](../sessions/18b8879c-f211-43b8-9908-cf65e509b21d/rapport.md) · [digest](../sessions/18b8879c-f211-43b8-9908-cf65e509b21d/digest.md)
- `2c2a6595-b208-446e-bbd1-d0f49eca45e8` — Tu travailles dans le dépôt (début 2026-10-02 15:03, 0.1 h) → [rapport](../sessions/2c2a6595-b208-446e-bbd1-d0f49eca45e8/rapport.md) · [digest](../sessions/2c2a6595-b208-446e-bbd1-d0f49eca45e8/digest.md)
- `31f26a6e-65f5-480d-be32-36b9f425b3dd` — Tu es un relecteur ADVERSARIAL (début 2026-10-02 19:26, 0.4 h) → [rapport](../sessions/31f26a6e-65f5-480d-be32-36b9f425b3dd/rapport.md) · [digest](../sessions/31f26a6e-65f5-480d-be32-36b9f425b3dd/digest.md)
- `34e1d4be-3708-4065-ae77-eca21f86e857` — Tu es relecteur ADVERSE. Tu (début 2026-10-02 09:52, 0.1 h) → [rapport](../sessions/34e1d4be-3708-4065-ae77-eca21f86e857/rapport.md) · [digest](../sessions/34e1d4be-3708-4065-ae77-eca21f86e857/digest.md)
- `3d5618a0-4e3a-45bb-943d-a72c753fb7da` — Tu écris un **document de (début 2026-10-02 15:02, 0.3 h) → [rapport](../sessions/3d5618a0-4e3a-45bb-943d-a72c753fb7da/rapport.md) · [digest](../sessions/3d5618a0-4e3a-45bb-943d-a72c753fb7da/digest.md)
- `4b146dfd-ce0b-4af8-910f-610ab438d4e6` — Tu es relecteur ADVERSE. Tu (début 2026-10-02 09:52, 0.1 h) → [rapport](../sessions/4b146dfd-ce0b-4af8-910f-610ab438d4e6/rapport.md) · [digest](../sessions/4b146dfd-ce0b-4af8-910f-610ab438d4e6/digest.md)
- `4e786d3f-0b66-4b23-8dc4-b452bc383bea` — Tu es un relecteur ADVERSARIAL. (début 2026-10-02 10:08, 0.2 h) → [rapport](../sessions/4e786d3f-0b66-4b23-8dc4-b452bc383bea/rapport.md) · [digest](../sessions/4e786d3f-0b66-4b23-8dc4-b452bc383bea/digest.md)
- `56879594-1434-4e34-83cc-de42cdf192a1` — Tu travailles dans le dépôt (début 2026-10-02 15:03, 0.1 h) → [rapport](../sessions/56879594-1434-4e34-83cc-de42cdf192a1/rapport.md) · [digest](../sessions/56879594-1434-4e34-83cc-de42cdf192a1/digest.md)
- `5c1bbea7-1d14-47b6-a48c-fea15f2b857e` — Tu es relecteur ADVERSE. Tu (début 2026-10-02 09:52, 0.1 h) → [rapport](../sessions/5c1bbea7-1d14-47b6-a48c-fea15f2b857e/rapport.md) · [digest](../sessions/5c1bbea7-1d14-47b6-a48c-fea15f2b857e/digest.md)
- `7f3f463f-9213-4721-b9a7-82858ef93f8c` — Tu es un vérificateur ADVERSARIAL (début 2026-10-02 19:29, 0.1 h) → [rapport](../sessions/7f3f463f-9213-4721-b9a7-82858ef93f8c/rapport.md) · [digest](../sessions/7f3f463f-9213-4721-b9a7-82858ef93f8c/digest.md)
- `8549abcb-5d9a-4594-915b-5628c80a2a08` — Tu travailles dans le dépôt (début 2026-10-02 15:03, 0.1 h) → [rapport](../sessions/8549abcb-5d9a-4594-915b-5628c80a2a08/rapport.md) · [digest](../sessions/8549abcb-5d9a-4594-915b-5628c80a2a08/digest.md)
- `8734fc13-aeb8-4cdf-b005-c182f77be0dc` — Tu es un relecteur ADVERSARIAL (début 2026-10-02 18:10, 0.2 h) → [rapport](../sessions/8734fc13-aeb8-4cdf-b005-c182f77be0dc/rapport.md) · [digest](../sessions/8734fc13-aeb8-4cdf-b005-c182f77be0dc/digest.md)
- `8b315bb2-abba-4033-b3d4-177d04b4f194` — Tu es relecteur ADVERSE. Tu (début 2026-10-02 09:51, 0.1 h) → [rapport](../sessions/8b315bb2-abba-4033-b3d4-177d04b4f194/rapport.md) · [digest](../sessions/8b315bb2-abba-4033-b3d4-177d04b4f194/digest.md)
- `8b6d46ab-6ad0-4648-92a8-0bec40a02526` — Tu dois LIRE TOUT le (début 2026-10-02 08:44, 0.2 h) → [rapport](../sessions/8b6d46ab-6ad0-4648-92a8-0bec40a02526/rapport.md) · [digest](../sessions/8b6d46ab-6ad0-4648-92a8-0bec40a02526/digest.md)
- `b13a6032-4f62-4e86-aa1f-03864a455c83` — Tu travailles dans le dépôt (début 2026-10-02 15:03, 0.1 h) → [rapport](../sessions/b13a6032-4f62-4e86-aa1f-03864a455c83/rapport.md) · [digest](../sessions/b13a6032-4f62-4e86-aa1f-03864a455c83/digest.md)
- `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` — Continue avec REPRISE.md (début 2026-09-28 14:46, 222.5 h) → [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md)
- `dcaa24d6-0017-4382-be21-8244c0fb9b7a` — Tu travailles dans le dépôt (début 2026-10-02 15:03, 0.0 h) → [rapport](../sessions/dcaa24d6-0017-4382-be21-8244c0fb9b7a/rapport.md) · [digest](../sessions/dcaa24d6-0017-4382-be21-8244c0fb9b7a/digest.md)
- `e14c26ae-6d52-41f9-a72f-6ebdcef172d5` — Tu es relecteur ADVERSARIAL, en (début 2026-10-02 21:15, 0.2 h) → [rapport](../sessions/e14c26ae-6d52-41f9-a72f-6ebdcef172d5/rapport.md) · [digest](../sessions/e14c26ae-6d52-41f9-a72f-6ebdcef172d5/digest.md)
- `f2de810a-b765-444d-b3cc-d8fce1ba2105` — Tu travailles dans le dépôt (début 2026-10-02 15:03, 0.2 h) → [rapport](../sessions/f2de810a-b765-444d-b3cc-d8fce1ba2105/rapport.md) · [digest](../sessions/f2de810a-b765-444d-b3cc-d8fce1ba2105/digest.md)
- `fba448b3-e237-4eb3-b77d-fcbf7da1c93d` — Tu travailles dans le dépôt (début 2026-10-02 15:03, 0.1 h) → [rapport](../sessions/fba448b3-e237-4eb3-b77d-fcbf7da1c93d/rapport.md) · [digest](../sessions/fba448b3-e237-4eb3-b77d-fcbf7da1c93d/digest.md)

## Mesures et rapports touchés

- [reports/rapport-coherence-vision.md](../../reports/rapport-coherence-vision.md)
- [reports/rapport-matvec-f32-parallele.md](../../reports/rapport-matvec-f32-parallele.md)
- [reports/rapport-p0-flux.md](../../reports/rapport-p0-flux.md)

<!-- notes -->

<!-- /notes -->
