# 2026-09-30 — Moteur : chargement, calcul, listes, quantification

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (31)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 07:18 | `d349063e` | vision : la permutation colonne-majeur des couches fenêtrées est implémentée | `plan-mla-vision.md`, `MANIFEST.md`, `digest.md` (+2) |
| 10:01 | `a44414d2` | Hygiène : sortir les artefacts de compilation du dépôt, et committer la sentinelle | `.gitignore`, `main.rs`, `.rustc_info.json` (+48) |
| 10:14 | `2cb7b46e` | Phase 1.4 : les deux variantes d'attribution de l'écart int8 | `model.rs`, `MANIFEST.md`, `digest.md` (+1) |
| 11:34 | `86ddf120` | Le CODE de l'encodage par écarts, oublié dans le commit précédent | `main.rs`, `MANIFEST.md`, `digest.md` (+1) |
| 11:37 | `af18f299` | Transport en listes à 1 024 jetons : ÷2,3 pour 1,3 % d'écart | `roadmap.md`, `MANIFEST.md`, `digest.md` (+2) |
| 12:02 | `cda31629` | Phase 3.4 : préremplissage par LOTS sur le fil — écart 0,00e0 | `format-flux.md`, `plan-prefill-reparti.md`, `roadmap.md` (+14) |
| 12:05 | `75222897` | Plomberie : huit drapeaux qui ne faisaient rien, d'après l'audit délégué | `main.rs`, `MANIFEST.md`, `digest.md` (+1) |
| 12:57 | `1bc04702` | Règle R4 : plafond des allocations pilotées par le réseau (256 Mo) | `main.rs`, `MANIFEST.md`, `digest.md` (+1) |
| 13:04 | `1a4beb37` | `--options-actives` : le tableau de bord des réglages qui agissent | `main.rs`, `model.rs`, `MANIFEST.md` (+2) |
| 13:06 | `01b7274a` | Un drapeau inconnu n'est plus avalé en silence | `main.rs`, `MANIFEST.md`, `digest.md` (+1) |
| 13:10 | `63a0e129` | REPRISE : le noyau GPU de top-k en tête des prochains chantiers | `REPRISE.md`, `digest.md`, `rapport.md` (+3) |
| 13:18 | `ace24b5b` | Chemin GPU revérifié : 15,1667 avec le pilote, noyau exact à 1,99e-7 | `REPRISE.md`, `digest.md`, `rapport.md` (+3) |
| 13:36 | `320b6123` | Seconde relecture adversariale : huit défauts, dont deux graves dans mes propres correctifs | `main.rs`, `digest.md`, `rapport.md` (+3) |
| 15:11 | `a383cd75` | Plan du noyau GPU de top-k (phase 1.1), chiffré, et la perplexité attendue du notebook | `Drave-reparti.ipynb`, `plan-gpu-topk.md`, `MANIFEST.md` (+6) |
| 15:29 | `8e132aad` | Mode 4 : le lot en LISTES sur le fil — ÷2,3 sur les octets, écart tenu | `plan-mode4-lot-listes.md`, `main.rs`, `MANIFEST.md` (+6) |
| 15:36 | `69296427` | REPRISE : le créneau 15h-18h (mode 4, frontière KV confirmée, plan GPU écrit) | `REPRISE.md`, `digest.md`, `rapport.md` (+3) |
| 15:41 | `b9e8ada7` | README : la perplexité de gpt-oss était dans la colonne du débit | `README.md`, `digest.md`, `rapport.md` (+3) |
| 16:03 | `998d4095` | Relecture du mode 4 : dix défauts, dont deux graves — corrigés, et le rapport écrit | `format-flux.md`, `plan-mode4-lot-listes.md`, `main.rs` (+8) |
| 16:04 | `d36f93e4` | Documents : dernières mentions de la version 4 remplacées par la 5 (mode lot en listes) | `REPRISE.md`, `roadmap.md`, `MANIFEST.md` (+3) |
| 16:15 | `59994697` | Index de session : le créneau 15h-18h (mode 4, plan GPU, 32 défauts relevés) | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 16:20 | `0259bf1c` | Préremplissage par lots : fidélité vérifiée à 1 024 jetons (0,00e0, 16 lots) | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 17:52 | `d00c01cc` | Noyau 2a du top-k GPU : histogramme d'octet, seuil exact sur 14/14 lignes | `cuda_stub.h`, `drave_gpu.cu`, `drave_gpu.ptx` (+8) |
| 18:16 | `47ce9b7a` | Relecture adversariale : 7 défauts corrigés, dont un bloquant sur les chemins d'échec | `drave_gpu.cu`, `gpu.rs`, `main.rs` (+9) |
| 18:36 | `d221eadf` | Étape 4 : le top-k déporté tourne dans le moteur (opt-in), et l'étape 5 est chiffrée | `REPRISE.md`, `plan-gpu-topk.md`, `gpu.rs` (+7) |
| 18:59 | `b58f4418` | Plan et REPRISE : l'étape 6 est verte, et la prochaine étape est la FUSION de la chaîne, pas un noyau de plus | `REPRISE.md`, `plan-gpu-topk.md`, `README.md` (+3) |
| 18:59 | `abcfab7a` | Relecture du branchement : un faux résultat silencieux dans attn_kv_recombine, et le top-k gagne à 16 k | `REPRISE.md`, `plan-gpu-topk.md`, `drave_gpu.cu` (+10) |
| 19:20 | `c1fdfd44` | Rapport et plan : 14 noyaux et 956 lignes (le noyau 3 est arrivé après le comptage), ordre réel de la collecte | `plan-gpu-topk.md`, `README.md`, `MANIFEST.md` (+3) |
| 19:24 | `22d30048` | --options-actives dit si le top-k déporté s'applique, et pourquoi sinon | `main.rs`, `README.md`, `MANIFEST.md` (+2) |
| 20:03 | `8342f175` | Noyau 4 : le top-k complet d'une ligne en UN lancement (8 lancements → 2) | `drave_gpu.cu`, `drave_gpu.ptx`, `gpu.rs` (+9) |
| 20:07 | `ea1d1557` | Le filet du noyau 4 doit agir AVANT la somme (test du filet, saboté exprès) | `drave_gpu.cu`, `drave_gpu.ptx`, `README.md` (+5) |
| 20:17 | `ed4ce477` | Revue adverse du noyau fusionné : une course bloquante, et cinq autres points | `drave_gpu.cu`, `drave_gpu.ptx`, `gpu.rs` (+8) |

## Chiffres du jour

`1024 jetons` · `÷2,3` · `15,1667` · `256 Mo` · `1,3 %`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `15fd322f-7e9e-48c0-a970-f36335eb622a` — Tu travailles dans le dépôt (début 2026-09-30 11:47, 0.2 h) → [rapport](../sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/rapport.md) · [digest](../sessions/15fd322f-7e9e-48c0-a970-f36335eb622a/digest.md)
- `42059fde-f06f-4e2c-9a23-8292d887fb6e` — Tu es vérificateur de documentation (début 2026-09-30 12:20, 0.2 h) → [rapport](../sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/rapport.md) · [digest](../sessions/42059fde-f06f-4e2c-9a23-8292d887fb6e/digest.md)
- `4d7a793b-74d1-4c46-bb53-21953fe91d87` — Tu es relecteur ADVERSARIAL, en (début 2026-09-30 22:59, 0.3 h) → [rapport](../sessions/4d7a793b-74d1-4c46-bb53-21953fe91d87/rapport.md) · [digest](../sessions/4d7a793b-74d1-4c46-bb53-21953fe91d87/digest.md)
- `5185ccb1-be24-4716-89df-62621e790444` — Tu es relecteur ADVERSARIAL dans (début 2026-09-30 17:03, 0.4 h) → [rapport](../sessions/5185ccb1-be24-4716-89df-62621e790444/rapport.md) · [digest](../sessions/5185ccb1-be24-4716-89df-62621e790444/digest.md)
- `564fbe3a-a859-4b3b-bd17-4da73a2f4e22` — Tu es relecteur ADVERSARIAL de (début 2026-09-30 18:07, 0.1 h) → [rapport](../sessions/564fbe3a-a859-4b3b-bd17-4da73a2f4e22/rapport.md) · [digest](../sessions/564fbe3a-a859-4b3b-bd17-4da73a2f4e22/digest.md)
- `5ce3f080-2d3d-467a-8ee1-df697f3f3e68` — Tu es relecteur ADVERSARIAL dans (début 2026-09-30 15:32, 0.3 h) → [rapport](../sessions/5ce3f080-2d3d-467a-8ee1-df697f3f3e68/rapport.md) · [digest](../sessions/5ce3f080-2d3d-467a-8ee1-df697f3f3e68/digest.md)
- `6d0c1d28-76e1-42f8-9e8c-7f88395f9e55` — Tu es relecteur ADVERSARIAL de (début 2026-09-30 20:04, 0.1 h) → [rapport](../sessions/6d0c1d28-76e1-42f8-9e8c-7f88395f9e55/rapport.md) · [digest](../sessions/6d0c1d28-76e1-42f8-9e8c-7f88395f9e55/digest.md)
- `7c876089-605c-4836-930e-925a66028509` — Tu es relecteur ADVERSARIAL dans (début 2026-09-30 13:10, 0.3 h) → [rapport](../sessions/7c876089-605c-4836-930e-925a66028509/rapport.md) · [digest](../sessions/7c876089-605c-4836-930e-925a66028509/digest.md)
- `7d0d2578-0048-4998-8494-7d2daef56769` — Tu travailles dans le dépôt (début 2026-09-30 11:47, 0.1 h) → [rapport](../sessions/7d0d2578-0048-4998-8494-7d2daef56769/rapport.md) · [digest](../sessions/7d0d2578-0048-4998-8494-7d2daef56769/digest.md)
- `8e04c99a-8ba1-4675-9f80-fa3338449b17` — Tu es VÉRIFICATEUR de documentation (début 2026-09-30 18:07, 0.2 h) → [rapport](../sessions/8e04c99a-8ba1-4675-9f80-fa3338449b17/rapport.md) · [digest](../sessions/8e04c99a-8ba1-4675-9f80-fa3338449b17/digest.md)
- `aa5f9fc5-9450-4118-b65f-e8b99a28519d` — Tu es vérificateur de documentation (début 2026-09-30 15:07, 0.2 h) → [rapport](../sessions/aa5f9fc5-9450-4118-b65f-e8b99a28519d/rapport.md) · [digest](../sessions/aa5f9fc5-9450-4118-b65f-e8b99a28519d/digest.md)
- `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` — Continue avec REPRISE.md (début 2026-09-28 14:46, 222.5 h) → [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md)
- `bcfe0b97-1795-4610-8e8b-b598ca1ba6cb` — Tu es relecteur ADVERSARIAL dans (début 2026-09-30 12:20, 0.3 h) → [rapport](../sessions/bcfe0b97-1795-4610-8e8b-b598ca1ba6cb/rapport.md) · [digest](../sessions/bcfe0b97-1795-4610-8e8b-b598ca1ba6cb/digest.md)
- `c25f97d1-9a4d-41da-b983-004f793afe43` — Tu travailles dans le dépôt (début 2026-09-30 11:47, 0.2 h) → [rapport](../sessions/c25f97d1-9a4d-41da-b983-004f793afe43/rapport.md) · [digest](../sessions/c25f97d1-9a4d-41da-b983-004f793afe43/digest.md)
- `c776b71f-525a-4bad-b83c-eff1c2d204ff` — Tu es relecteur ADVERSARIAL de (début 2026-09-30 18:36, 0.1 h) → [rapport](../sessions/c776b71f-525a-4bad-b83c-eff1c2d204ff/rapport.md) · [digest](../sessions/c776b71f-525a-4bad-b83c-eff1c2d204ff/digest.md)
- `da69b1fa-91b0-4c69-bb2b-58bf00e92e28` — Tu travailles dans le dépôt (début 2026-09-30 15:07, 0.1 h) → [rapport](../sessions/da69b1fa-91b0-4c69-bb2b-58bf00e92e28/rapport.md) · [digest](../sessions/da69b1fa-91b0-4c69-bb2b-58bf00e92e28/digest.md)

## Mesures et rapports touchés

- [reports/rapport-compacite-trace.md](../../reports/rapport-compacite-trace.md)
- [reports/rapport-drapeaux-ignores.md](../../reports/rapport-drapeaux-ignores.md)
- [reports/rapport-gpu-topk-selection.md](../../reports/rapport-gpu-topk-selection.md)
- [reports/rapport-mode4-lot-listes.md](../../reports/rapport-mode4-lot-listes.md)
- [reports/rapport-prefill-reparti.md](../../reports/rapport-prefill-reparti.md)
- [reports/rapport-session-2026-09-30.md](../../reports/rapport-session-2026-09-30.md)
- [reports/rapport-transport-liste.md](../../reports/rapport-transport-liste.md)

<!-- notes -->

<!-- /notes -->
