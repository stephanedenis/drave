# 2026-10-01 — Modèles, entraînement, parcimonie, biologie

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (13)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 07:06 | `beacdf96` | DeepSeek-V4.1-Flash : pas de poids ouverts — c'est DeepSeek-V4-Flash qui est téléchargé, et le plan d'adaptation est écrit | `plan-deepseek-v4-flash.md`, `README.md`, `MANIFEST.md` (+2) |
| 09:42 | `e9cc44f6` | Modèles lourds : file de 1,14 To en téléchargement, plan écrit, état honnête | `plan-modeles-lourds.md`, `README.md`, `MANIFEST.md` (+3) |
| 10:08 | `7c1b9ff9` | Convertisseur GGUF → modèle éclaté en clusters : un fichier par cluster, vérifié par empreintes | `format-clusters.md`, `plan-modeles-lourds.md`, `README.md` (+5) |
| 11:14 | `3eb0af71` | Un modèle éclaté se lit comme un seul : lecteur multi-fichiers, shards et clusters | `REPRISE.md`, `clusters.rs`, `gguf.rs` (+8) |
| 12:18 | `907e5c32` | Journal : inventaire des modèles lourds et vérificateur de table dans REPRISE | `REPRISE.md`, `README.md`, `MANIFEST.md` (+2) |
| 12:18 | `ae4531bf` | Inventaire des modèles lourds : 984 Go de poids annoncés par les descripteurs, 984 Go annoncés par HuggingFace | `plan-modeles-lourds.md`, `README.md`, `MANIFEST.md` (+3) |
| 12:36 | `8e3198ab` | La file de 1 138 Go est terminée : 1 163 Go de modèles lourds, tous complets et lisibles | `plan-modeles-lourds.md`, `README.md`, `MANIFEST.md` (+3) |
| 20:17 | `dcf6d65d` | REPRISE : analyse statique des poids | `REPRISE.md`, `README.md`, `MANIFEST.md` (+2) |
| 20:17 | `958eb293` | Analyse statique : les experts sont orthogonaux, mais la periodicite de 12 est dans les POIDS | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 22:24 | `3372be41` | Plan materiel sensible au modele : il lit ses dimensions au lieu de les supposer | `main.rs`, `README.md`, `MANIFEST.md` (+2) |
| 22:33 | `7c8899ad` | Materiel : distinguer dense et MoE (un modele dense affichait « 0 experts de 9,95 Mo ») | `main.rs`, `README.md`, `MANIFEST.md` (+2) |
| 23:04 | `f041ce67` | BF16 : lu et verifie (le f32 tronque a ses 16 bits de poids fort, exactement) | `gguf.rs`, `main.rs`, `README.md` (+3) |
| 23:49 | `475bee4d` | routage des experts : quatre conventions, facteur d'échelle, routage par table | `gguf.rs`, `model.rs`, `MANIFEST.md` (+2) |

## Chiffres du jour

`9,95 Mo` · `1138 Go` · `1163 Go` · `984 Go`

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

- [reports/rapport-decoupage-moe.md](../../reports/rapport-decoupage-moe.md)
- [reports/rapport-empreinte-memoire.md](../../reports/rapport-empreinte-memoire.md)
- [reports/rapport-lecteur-multifichiers.md](../../reports/rapport-lecteur-multifichiers.md)

<!-- notes -->

<!-- /notes -->
