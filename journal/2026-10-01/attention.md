# 2026-10-01 — Attention, fenêtre, puits

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (8)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 00:54 | `09adea5a` | Le k est un réglage : 0/3 au milieu à k=512, 3/3 à k=1024 (trois fenêtres par point) | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 01:07 | `1425c79c` | Revue du sprint 4 : « trois fenêtres » étaient trois fois la même invite, et la portée du k était surestimée | `contexte-long.md`, `README.md`, `digest.md` (+6) |
| 03:37 | `13a5c9cc` | Sprint 5 : cérémonie (le taux remplace le verdict, la revue adverse, le pas de fenêtre corrigé) | `README.md`, `MANIFEST.md`, `digest.md` (+4) |
| 03:38 | `783f1f94` | Sprint 6 : le taux de récupération (9 fenêtres × 3 chemins) et le point 16 384 | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 04:59 | `e4b3ebc5` | Le taux par fenêtre : 9 fenêtres contiguës, 8/9 en attention complète, et le mur du préremplissage | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 05:25 | `361c1863` | Nuance : le facteur de ralentissement est un minorant (les deux exécutions à ctx 4608 n'ont jamais fini ; la même fenêtre rend en 85,1 s à ctx 5120) | `README.md`, `digest.md`, `rapport.md` (+4) |
| 05:39 | `3209dc50` | Sprint 6 : cérémonie (le taux par fenêtre, le livelock du contexte, planning du sprint 7) | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 06:53 | `17282a7e` | Le résultat de la nuit : à k=256 le taux est le MÊME que l'attention complète (8/9), et les échecs sont sur d'autres fenêtres | `REPRISE.md`, `README.md`, `MANIFEST.md` (+3) |

## Chiffres du jour

`85,1 s` · `× 3`

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

<!-- notes -->

<!-- /notes -->
