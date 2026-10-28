# 2026-09-30 — Documentation, état, conventions

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (21)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 08:36 | `15c4c8c9` | Drave : document de vision, et le nom dans le README | `README.md`, `vision.md`, `MANIFEST.md` (+2) |
| 08:48 | `b97d1290` | Drave : renommage complet (crate, binaire, variables, documents) | `README.md`, `REPRISE.md`, `comparaison-spiking.md` (+114) |
| 10:00 | `a2545ac2` | Phase 0.3 et 1.4 : codec de référence du format, et l'expérience int8 écrite | `roadmap.md`, `MANIFEST.md`, `digest.md` (+1) |
| 12:38 | `ea754dfd` | Corrections documentaires : le renommage, les chiffres, et une affirmation fausse en moins | `README.md`, `REPRISE.md`, `roadmap.md` (+6) |
| 13:01 | `809763df` | Kit Colab vérifié de bout en bout (clonage, compilation 23 s, écart 0,00e0) | `README.md`, `MANIFEST.md`, `digest.md` (+1) |
| 13:11 | `b2767fe4` | Feuille de route : 1.4 attribuée et la section format renvoyée à sa spécification | `roadmap.md`, `digest.md`, `rapport.md` (+3) |
| 15:31 | `57f0fc6c` | Corrections du second audit (2/2) : la journée au README, le mode 4 dans la recette Colab, le renvoi FPGA de la vision | `README.md`, `colab-reparti.md`, `vision.md` (+3) |
| 15:31 | `64a86cae` | Corrections du second audit (1/2) : chiffres, époques, comptes, et la journée au README | `README.md`, `REPRISE.md`, `format-flux.md` (+12) |
| 15:32 | `64bf7451` | Documents : la frontière du cache KV dans contexte-long, et l'addendum du rapport de drapeaux | `contexte-long.md`, `digest.md`, `rapport.md` (+4) |
| 16:06 | `e6d6ce99` | Colab : les quatorze champs du contrat d'activation, pas quatre | `colab-reparti.md`, `MANIFEST.md`, `digest.md` (+1) |
| 17:03 | `a4735aa0` | Compteurs de lignes : 12 171 au 30/09 (le mode 4 et ses correctifs ont ajouté 270 lignes) | `README.md`, `REPRISE.md`, `digest.md` (+4) |
| 17:08 | `f1c265e0` | README : les prochaines étapes étaient restées à l'époque du FPGA | `README.md`, `digest.md`, `rapport.md` (+3) |
| 18:23 | `1f536671` | Compteur de lignes Rust unifié : 13 168 (un seul chiffre, mesuré, dans README ×2 et REPRISE) | `README.md`, `REPRISE.md`, `README.md` (+3) |
| 19:20 | `dada69ad` | Journal : index des sessions régénéré | `README.md`, `MANIFEST.md`, `digest.md` (+1) |
| 19:24 | `03243f7f` | Compteur de lignes Rust re-mesuré en fin de sprint : 13 480 (le chiffre avait bougé de 312 lignes pendant le sprint) | `README.md`, `REPRISE.md`, `README.md` (+3) |
| 19:41 | `a6eedd8d` | Sprint 1 : cérémonie (revue chiffrée, rétrospective, planning du sprint 2) | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 19:42 | `04c817bc` | Journal : index régénéré par l'outillage de session | `README.md`, `MANIFEST.md`, `digest.md` (+1) |
| 19:42 | `37f96927` | Journal : index des sessions (clôture) | `README.md`, `MANIFEST.md`, `digest.md` (+1) |
| 19:42 | `0f768790` | Journal : index des sessions (fin de sprint 1) | `README.md`, `MANIFEST.md`, `digest.md` (+1) |
| 21:20 | `a76d8c8b` | REPRISE : le doute sur les projections est à moitié levé (ctx 512 et 1024 identiques, ctx 256 évalue une autre chose) | `REPRISE.md`, `README.md`, `MANIFEST.md` (+2) |
| 21:49 | `b795f09b` | Sprint 2 : cérémonie (revue adverse autonome, introspection, planning du sprint 3) | `README.md`, `MANIFEST.md`, `digest.md` (+3) |

## Chiffres du jour

`×2` · `23 s`

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

- [reports/bilan-multi-materiel.md](../../reports/bilan-multi-materiel.md)
- [reports/rapport-8bits.md](../../reports/rapport-8bits.md)
- [reports/rapport-attention-creuse.md](../../reports/rapport-attention-creuse.md)
- [reports/rapport-attribution-kv.md](../../reports/rapport-attribution-kv.md)
- [reports/rapport-campagne-parcimonie.md](../../reports/rapport-campagne-parcimonie.md)
- [reports/rapport-capteur-hebbien.md](../../reports/rapport-capteur-hebbien.md)
- [reports/rapport-coherence-docs-2.md](../../reports/rapport-coherence-docs-2.md)
- [reports/rapport-cpu-aer.md](../../reports/rapport-cpu-aer.md)
- [reports/rapport-croisement-push-pull.md](../../reports/rapport-croisement-push-pull.md)
- [reports/rapport-drapeaux-ignores.md](../../reports/rapport-drapeaux-ignores.md)
- [reports/rapport-encodage.md](../../reports/rapport-encodage.md)
- [reports/rapport-eparsite.md](../../reports/rapport-eparsite.md)
- [reports/rapport-gpt-oss-perplexite.md](../../reports/rapport-gpt-oss-perplexite.md)
- [reports/rapport-grappes.md](../../reports/rapport-grappes.md)
- [reports/rapport-greffon.md](../../reports/rapport-greffon.md)
- [reports/rapport-harnais.md](../../reports/rapport-harnais.md)
- [reports/rapport-inference.md](../../reports/rapport-inference.md)
- [reports/rapport-minimal.md](../../reports/rapport-minimal.md)
- [reports/rapport-mode-listes.md](../../reports/rapport-mode-listes.md)
- [reports/rapport-modele-reel.md](../../reports/rapport-modele-reel.md)
- [reports/rapport-mur-memoire-4bits.md](../../reports/rapport-mur-memoire-4bits.md)
- [reports/rapport-optimisations.md](../../reports/rapport-optimisations.md)
- [reports/rapport-parcimonie-imposee.md](../../reports/rapport-parcimonie-imposee.md)
- [reports/rapport-passage-a-l-echelle.md](../../reports/rapport-passage-a-l-echelle.md)
- [reports/rapport-phase3-reparti.md](../../reports/rapport-phase3-reparti.md)
- [reports/rapport-placement-bits-kv.md](../../reports/rapport-placement-bits-kv.md)
- [reports/rapport-precision.md](../../reports/rapport-precision.md)
- [reports/rapport-prefill-par-lots.md](../../reports/rapport-prefill-par-lots.md)
- [reports/rapport-programme-evolutif.md](../../reports/rapport-programme-evolutif.md)
- [reports/rapport-session-2026-09-30.md](../../reports/rapport-session-2026-09-30.md)
- [reports/rapport-transport-liste.md](../../reports/rapport-transport-liste.md)
- [reports/rapport-valeur-unaire.md](../../reports/rapport-valeur-unaire.md)

<!-- notes -->

<!-- /notes -->
