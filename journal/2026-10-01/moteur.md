# 2026-10-01 — Moteur : chargement, calcul, listes, quantification

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (17)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 06:09 | `1b9808e6` | Le correctif du livelock finissait en SIGABRT : c'est corrigé, et vérifié par le code de sortie | `REPRISE.md`, `main.rs`, `model.rs` (+9) |
| 11:39 | `8f55e4fd` | Clusters exécutables : origine 15,2789 = clusters 15,2789, et les défauts trouvés en chemin | `format-clusters.md`, `clusters.rs`, `gguf.rs` (+9) |
| 12:11 | `f98816d8` | Revue adverse : un défaut bloquant silencieux, et le test qui manquait au correctif | `clusters.rs`, `gguf.rs`, `model.rs` (+6) |
| 12:15 | `9eea40b4` | La table des types ggml confrontée à libggml, et les huit types ajoutés après NVFP4 | `format-clusters.md`, `gguf.rs`, `README.md` (+4) |
| 12:18 | `8a2ff796` | Porte gpt-oss verte sur le binaire final : 15,1757 avec mmap, 21 minutes | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 21:37 | `b2bc093b` | Detection materielle et heuristiques de configuration automatique | `gguf.rs`, `main.rs`, `materiel.rs` (+5) |
| 21:55 | `2d4738fd` | Tete restreinte a une liste de tokens : +15 %, mais la sortie change | `main.rs`, `model.rs`, `README.md` (+4) |
| 22:16 | `302fc88d` | Restreindre la tete de sortie : trois voies explorees, une seule survit | `main.rs`, `model.rs`, `README.md` (+4) |
| 22:21 | `8b1c0b9c` | Rapport : detection materielle et configuration automatique | `main.rs`, `README.md`, `MANIFEST.md` (+3) |
| 22:26 | `60e19582` | mmap : 365,7 Go adresses en 0,08 s et 47 Mo de RSS | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 22:31 | `65036ddb` | Defauts de threads : les cœurs physiques, sans le 3/4 ni le /2 | `main.rs`, `README.md`, `MANIFEST.md` (+2) |
| 22:32 | `0c6bca8f` | Aide du moteur : les modes recents, et ce que chacun ne fait pas | `main.rs`, `README.md`, `MANIFEST.md` (+2) |
| 22:41 | `5ba051f8` | Materiel : estimation du cout par jeton, d'apres les debits mesures | `main.rs`, `materiel.rs`, `README.md` (+3) |
| 22:53 | `42917284` | Q2_K : dequantification implementee et verifiee contre ggml | `gguf.rs`, `README.md`, `MANIFEST.md` (+2) |
| 22:59 | `aa92cfc7` | IQ2_XXS : 93 Go de V4.1 debloques, et un bug que la lecture n'aurait pas vu | `formats.rs`, `gguf.rs`, `main.rs` (+4) |
| 23:02 | `0358eec9` | IQ1_M : 61 Go de DeepSeek-V4-Flash debloques (ecart 0,00e+00 avec ggml) | `formats.rs`, `main.rs`, `README.md` (+3) |
| 23:29 | `dbae4f8e` | formats : Q5_K, Q5_0/1, Q3_K, IQ3_XXS, IQ1_S, IQ4_XS — et MXFP4 corrigé d'un facteur 2 | `formats.rs`, `gguf.rs`, `main.rs` (+8) |

## Chiffres du jour

`61 Go` · `93 Go` · `0,08 s` · `365,7 Go` · `47 Mo` · `+15 %` · `15,1757` · `15,2789`

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

- [reports/rapport-aiguille-topk.md](../../reports/rapport-aiguille-topk.md)
- [reports/rapport-architecture-memoire.md](../../reports/rapport-architecture-memoire.md)
- [reports/rapport-lecteur-multifichiers.md](../../reports/rapport-lecteur-multifichiers.md)
- [reports/rapport-optimisations-auto.md](../../reports/rapport-optimisations-auto.md)
- [reports/rapport-tete-restreinte.md](../../reports/rapport-tete-restreinte.md)

<!-- notes -->

<!-- /notes -->
