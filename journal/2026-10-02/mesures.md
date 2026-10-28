# 2026-10-02 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (13)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 02:08 | `44288ff5` | Rapports : la référence externe (llama.cpp) mesurée — gpt-oss cohérent, MLA fausse | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 05:00 | `3b9c04a1` | Rapport MLA : le bug, la méthode qui l'a trouvé, et ce qui reste ouvert | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 06:57 | `c4f55fdc` | La validation MLA s'arrête à la position 2, et c'est maintenant écrit partout | `README.md`, `REPRISE.md`, `MANIFEST.md` (+3) |
| 07:04 | `68487f34` | REPRISE : le chantier 2 (tête garantie) est clos par une mesure | `REPRISE.md`, `MANIFEST.md`, `digest.md` (+1) |
| 07:05 | `7844b18e` | Chargeur d'experts : les lecteurs parallèles ne donnent rien, et on sait pourquoi | `MANIFEST.md`, `digest.md`, `rapport.md` (+2) |
| 07:49 | `9d20a8b3` | Rapport MLA : annexe sur l'écart à la position 3 — ce qui est exclu, ce qui reste | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 07:56 | `acc34986` | L'écart naît APRÈS la couche 0 : 1,9 % / 1,3 % / 3,8 % / 4,0 % aux positions 0-3 | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 16:52 | `b983d892` | P6 : V4-Flash éclaté en 8 grappes — perplexité identique au chiffre près, et 2,8× plus vite | `plan-deepseek41-complet.md`, `MANIFEST.md`, `digest.md` (+3) |
| 16:57 | `259f24c5` | Portes : V4-Flash entre dans tools/portes.sh (--config calculable + perplexité 8430,2968) — un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien | `REPRISE.md`, `MANIFEST.md`, `digest.md` (+2) |
| 16:58 | `a26d407e` | P8 : l'engram inventorié, et l'issue (b) retenue — pas d'implémentation sans référence | `plan-deepseek41-complet.md`, `MANIFEST.md`, `digest.md` (+2) |
| 17:11 | `2145e0a2` | P5 : le top-k de l'indexeur validé sans run de 2 048 jetons (metadata top_k 512 → 1 sur une copie du shard 1) — l_last-2 concorde à 0,99992 | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 17:12 | `6c08aabb` | Plan : P5 sans réserve — la porte longue du top-k est fermée par la mesure | `plan-deepseek41-complet.md`, `MANIFEST.md`, `digest.md` (+1) |
| 23:05 | `c64e3aa0` | Docs : la vitesse V4.1 (×3, zéro bit changé) et le cache d'experts refusé par la mesure entrent dans le plan et dans REPRISE | `REPRISE.md`, `plan-deepseek41-complet.md`, `README.md` (+4) |

## Chiffres du jour

`×3` · `2048 jetons` · `perplexité 8430,2968` · `8430,2968` · `1,9 %` · `1,3 %` · `3,8 %` · `4,0 %`

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

- [reports/rapport-engram-etat.md](../../reports/rapport-engram-etat.md)
- [reports/rapport-mla-experts.md](../../reports/rapport-mla-experts.md)
- [reports/rapport-routage-experts.md](../../reports/rapport-routage-experts.md)
- [reports/rapport-tete-garantie.md](../../reports/rapport-tete-garantie.md)
- [reports/rapport-v4-hca.md](../../reports/rapport-v4-hca.md)
- [reports/rapport-v4-reparti.md](../../reports/rapport-v4-reparti.md)

<!-- notes -->

<!-- /notes -->
