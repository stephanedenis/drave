# 2026-10-02 — Documentation, état, conventions

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (11)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 10:24 | `477de44f` | docs : révision de cohérence avec la vision (18 documents, 88 sites) | `README.md`, `REPRISE.md`, `colab-reparti.md` (+33) |
| 15:33 | `4c155708` | V4-Flash tourne en ENTIER · glossaire de référence · trois points doc corrigés | `contexte-long.md`, `glossaire.md`, `plan-deepseek41-complet.md` (+25) |
| 16:55 | `c1b7197d` | P7 : le constat de provenance de V4.1, établi et nommé (aucun code à écrire, deux manques) | `plan-deepseek41-complet.md`, `model.rs`, `MANIFEST.md` (+3) |
| 17:14 | `13aae7f0` | Plan : plus de titres en double (P6, P7), et P4 dit ce qui est fait (HCA et CSA) | `plan-deepseek41-complet.md`, `MANIFEST.md`, `digest.md` (+1) |
| 21:19 | `bbd4dddd` | Sprint 13 : la cérémonie (garder / changer / doute) et le planning du bloc 14 — la vivacité de l'engram | `README.md`, `MANIFEST.md`, `digest.md` (+4) |
| 21:36 | `2edc343f` | Sprint 14 : P8 fermée — l'engram est vivant (A/B mesuré), et le masque des jetons d'image reste un no-op DÉCIDÉ | `REPRISE.md`, `plan-deepseek41-complet.md`, `README.md` (+4) |
| 22:00 | `42634076` | Sprint 14 : clôture (50 min utiles) — les trois chantiers sont livrés et mesurés | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 22:00 | `12949927` | Engram : l'ablation grandit avec le contexte (22 % → 55 %), et la formule est exclue comme cause | `REPRISE.md`, `plan-deepseek41-complet.md`, `README.md` (+4) |
| 22:32 | `8c0537f3` | Sprint 15 : l'heure de clôture réelle (31 min, pas 107 — mesurée sur l'horloge) | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 23:15 | `10b2e10b` | Sprint 16 : clôture (33 min) et planning du bloc 17 — proj+mlp est-il borné par les E/S ou par le calcul ? Le re-tri par chaleur est écarté pour une raison mesurable (253 Go libres sur le disque rapide, 365 Go demandés) | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 23:35 | `4430d7d1` | Bloc 17 : à ctx 64 aussi (330 Go relus), la seconde passe ne gagne que 4 % — le disque n'est pas la borne ; et le balayage des fils donne 16 comme optimum | `README.md`, `MANIFEST.md`, `digest.md` (+2) |

## Chiffres du jour

`4 %` · `330 Go` · `253 Go` · `365 Go` · `22 %` · `55 %`

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

- [reports/bilan-multi-materiel.md](../../reports/bilan-multi-materiel.md)
- [reports/rapport-coherence-vision.md](../../reports/rapport-coherence-vision.md)
- [reports/rapport-provenance-v41.md](../../reports/rapport-provenance-v41.md)

<!-- notes -->

<!-- /notes -->
