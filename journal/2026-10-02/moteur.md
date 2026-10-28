# 2026-10-02 — Moteur : chargement, calcul, listes, quantification

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (31)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 00:33 | `76746843` | MLA à rang faible + formats sans noyau : GLM-5.3 et Kimi deviennent calculables | `gguf.rs`, `list.rs`, `main.rs` (+5) |
| 01:14 | `776409b8` | Déquantification par bloc sans allocation : 253 s/jeton → à remesurer | `REPRISE.md`, `formats.rs`, `gguf.rs` (+5) |
| 01:40 | `78e9c944` | Expert partagé (2D) et biais de sélection `exp_probs_b` : deux tenseurs lus nulle part | `model.rs`, `MANIFEST.md`, `digest.md` (+2) |
| 03:00 | `44f634ec` | MLA : dire NON VALIDÉE partout où elle est annoncée | `REPRISE.md`, `main.rs`, `model.rs` (+3) |
| 04:59 | `51dc4b7b` | MLA : `wv_b` est rangé à l'envers de `wk_b` — corrélation 0,999 après correction | `REPRISE.md`, `main.rs`, `model.rs` (+3) |
| 06:23 | `935fe711` | Quantification des activations : lire la TRANCHE utile, pas le tampon entier | `README.md`, `model.rs`, `MANIFEST.md` (+2) |
| 07:03 | `c147082e` | Tête garantie : implémentée, exacte, et mesurée sans gain | `main.rs`, `model.rs`, `MANIFEST.md` (+3) |
| 08:51 | `e3a802d2` | Test d'exécution de DeepSeek-V4.1 : tout ce qui tourne est mesuré, la passe avant est refusée en 0,33 s | `REPRISE.md`, `main.rs`, `model.rs` (+6) |
| 11:06 | `47cd68ad` | Plan V4.1 : P0 marqué fait, et les hyper-paramètres sont dans le GGUF (`deepseek41.config`) | `plan-deepseek41-complet.md`, `MANIFEST.md`, `digest.md` (+1) |
| 11:06 | `b2f48b72` | P1 (1/3) : le cœur des hyper-connexions, contre une référence indépendante | `model.rs`, `MANIFEST.md`, `digest.md` (+2) |
| 11:12 | `28ed9a15` | P1 (2/3) : les hyper-connexions sont chargées ET consommées par la passe avant | `gguf.rs`, `main.rs`, `model.rs` (+3) |
| 12:01 | `47a859d4` | P2/P3 : V4-Flash concorde avec llama.cpp sur les couches 0 et 1 | `plan-deepseek41-complet.md`, `main.rs`, `model.rs` (+5) |
| 12:38 | `8b967f72` | P4 : le compresseur HCA, validé au premier bloc complet (0,999992) | `REPRISE.md`, `plan-deepseek41-complet.md`, `gguf.rs` (+6) |
| 12:50 | `8c89068d` | P5 (1/2) : le compresseur CSA, validé — deux pièges trouvés par la comparaison | `plan-deepseek41-complet.md`, `model.rs`, `MANIFEST.md` (+4) |
| 14:03 | `4a0c99b3` | P5 (2/2) : l'indexeur — scores validés à 0,1 % contre llama.cpp | `plan-deepseek41-complet.md`, `model.rs`, `MANIFEST.md` (+3) |
| 14:36 | `d0b72330` | V4 : le clamp SwiGLU (swiglu_clamp_exp, par couche) — un manque qui ne se voyait pas dans les premières couches | `gguf.rs`, `model.rs`, `MANIFEST.md` (+3) |
| 16:59 | `362b3ede` | P9 : la mesure tranche — le goulot est la lecture (×2,8 en éclaté, même calcul), pas le déquant : noyaux natifs non justifiés aujourd'hui | `plan-deepseek41-complet.md`, `MANIFEST.md`, `digest.md` (+1) |
| 17:17 | `07f1c8fe` | P7/P8 : mes deux conclusions étaient prématurées — les sources externes existent | `plan-deepseek41-complet.md`, `model.rs`, `MANIFEST.md` (+4) |
| 17:23 | `90b588ef` | P8 : l'adressage de l'engram porté et validé — 480 000 adresses identiques à la référence | `engram.rs`, `main.rs`, `MANIFEST.md` (+4) |
| 17:27 | `32bfa3ac` | P8 : l'engram est porté en entier — adressage, lecture, injection — et validé contre la référence | `plan-deepseek41-complet.md`, `engram.rs`, `gguf.rs` (+5) |
| 17:59 | `93cb1b7c` | P7 : la chaîne mHC RETARDÉE de V4.1 — implémentée, exécutée sur 365,7 Go, vérifiée | `REPRISE.md`, `glossaire.md`, `plan-deepseek41-complet.md` (+8) |
| 18:08 | `e4331d46` | P7 : le compresseur de V4.1 (ratios 1 et 2) tourne sur les couches SOURCES, et il est vérifié | `REPRISE.md`, `plan-deepseek41-complet.md`, `model.rs` (+5) |
| 18:49 | `3ce29650` | P7 : l'engram de V4.1 branché dans la passe avant — et la première passe COMPLÈTE des 40 couches | `REPRISE.md`, `plan-deepseek41-complet.md`, `model.rs` (+7) |
| 19:21 | `8444a396` | Sprint 11 : le rétro du bloc, et le vide qui rend le CHOIX de l'indexeur vérifiable | `model.rs`, `README.md`, `MANIFEST.md` (+3) |
| 20:04 | `a1bb6ea6` | La rotation des couches compressées : le correctif YaRN est validé, et l'instrument mentait | `REPRISE.md`, `plan-deepseek41-complet.md`, `main.rs` (+16) |
| 21:34 | `81dbd2dc` | Revue adverse du bloc 13 : trois chiffres publiés corrigés, quatre trous fermés | `REPRISE.md`, `format-flux.md`, `plan-deepseek41-complet.md` (+15) |
| 23:04 | `61566b35` | Le cache RAM d'experts de V4.1 est MESURÉ PLUS LENT (+4 % à 4 Go, +21 % à 32 Go) — et un pas d'expert faux d'un facteur 8 est corrigé | `main.rs`, `model.rs`, `README.md` (+5) |
| 23:25 | `fc504781` | Bloc 17 : proj+mlp est borné par le CALCUL (mesuré), et le fil manquant vaut ×1,32 sur la passe | `model.rs`, `README.md`, `MANIFEST.md` (+4) |
| 23:44 | `11235955` | Bloc 17 : la déquantification pèse 25 % de la passe et 45 % du poste d'experts (mesuré par ablation), et clôture du bloc | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 23:55 | `191362f1` | Noyau AVX2 pour la déquantification Q2_K des experts : ×1,33 sur le poste, zéro bit changé | `gguf.rs`, `list.rs`, `README.md` (+5) |
| 23:57 | `dfbd6ea8` | Noyau AVX2 pour IQ1_M (les experts de V4-Flash) : ×1,07, et la raison du plafond | `formats.rs`, `list.rs`, `README.md` (+4) |

## Chiffres du jour

`×1,07` · `×1,33` · `25 %` · `45 %` · `×1,32` · `+4 %` · `+21 %` · `4 Go` · `32 Go` · `40 couches` · `365,7 Go` · `×2,8`

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

- [reports/rapport-decoupage-v41.md](../../reports/rapport-decoupage-v41.md)
- [reports/rapport-engram-etat.md](../../reports/rapport-engram-etat.md)
- [reports/rapport-execution-v41.md](../../reports/rapport-execution-v41.md)
- [reports/rapport-mla-experts.md](../../reports/rapport-mla-experts.md)
- [reports/rapport-provenance-v41.md](../../reports/rapport-provenance-v41.md)
- [reports/rapport-routage-experts.md](../../reports/rapport-routage-experts.md)
- [reports/rapport-tete-garantie.md](../../reports/rapport-tete-garantie.md)
- [reports/rapport-v4-couches-0-1.md](../../reports/rapport-v4-couches-0-1.md)
- [reports/rapport-v4-hca.md](../../reports/rapport-v4-hca.md)
- [reports/rapport-v4-yarn-compresse.md](../../reports/rapport-v4-yarn-compresse.md)
- [reports/rapport-v41-mhc.md](../../reports/rapport-v41-mhc.md)

<!-- notes -->

<!-- /notes -->
