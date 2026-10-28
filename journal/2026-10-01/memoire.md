# 2026-10-01 — Mémoire épisodique, consolidation, greffe

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (8)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 02:49 | `0d50e756` | À 8 192 clés, k=1024 (12,5 %) suffit : le k nécessaire croît plus lentement que le contexte (deux points) | `README.md`, `MANIFEST.md`, `digest.md` (+1) |
| 05:33 | `45a0c440` | Le « ralentissement » est un LIVELOCK : KvCache::assurer boucle sans fin si besoin > ctx (model.rs:1117) | `README.md`, `digest.md`, `rapport.md` (+4) |
| 05:46 | `32951e95` | Le livelock du contexte est corrigé : troncature annoncée au lieu d'une boucle infinie | `main.rs`, `model.rs`, `README.md` (+6) |
| 11:56 | `b24a2e6e` | mmap (3,3x plus rapide, 3x moins de mémoire) et nœud partiel (2,36 Go pour un huitième des experts) | `README.md`, `REPRISE.md`, `format-clusters.md` (+9) |
| 12:21 | `73b2c1fd` | Courbe du nœud partiel : 1, 2, 4, 8 clusters — perplexité et mémoire | `format-clusters.md`, `README.md`, `MANIFEST.md` (+3) |
| 17:42 | `c7c602d9` | L'empreinte memoire de DeepSeek-V4.1 : 365,7 Go -> 50-80 Go, et ce n'est pas en decoupant les experts | `README.md`, `REPRISE.md`, `.contexte-long.md.kate-swp` (+8) |
| 20:54 | `679a26e4` | REPRISE : architecture memoire | `REPRISE.md`, `README.md`, `MANIFEST.md` (+2) |
| 20:54 | `ed832cea` | Architecture memoire : ou mettre quoi, et le KV qu'on oubliait | `README.md`, `README.md`, `MANIFEST.md` (+3) |

## Chiffres du jour

`365,7 Go` · `80 Go` · `2,36 Go` · `12,5 %`

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
- [reports/rapport-empreinte-memoire.md](../../reports/rapport-empreinte-memoire.md)
- [reports/rapport-lecteur-multifichiers.md](../../reports/rapport-lecteur-multifichiers.md)

<!-- notes -->

<!-- /notes -->
