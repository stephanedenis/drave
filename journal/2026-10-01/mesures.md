# 2026-10-01 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (11)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 01:18 | `b14e4f28` | Contrôle dense à 8 192 : l'information est retrouvée (1002 s, prompt de 7963 jetons) — la question du k vs contexte est mesurable là | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 01:40 | `ee595197` | Pourquoi --lot 1 diffère de --lot 256 : 7e-4 nat par position, top-1 identique partout — c'est une amplification chaotique, pas un chemin faux | `README.md`, `MANIFEST.md`, `digest.md` (+4) |
| 02:20 | `508d3d87` | Grille refaite sur trois VRAIS textes : k=256 échoue 1 fois sur 3, pas 3 sur 3 | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 02:58 | `a3691a53` | Revue du sprint 5 : la section 8 192 manquait, et « au plus » dépassait la mesure d'un facteur 10 | `README.md`, `digest.md`, `rapport.md` (+5) |
| 09:42 | `aea1b10c` | Politique de stockage : la bibliothèque brute sur le mécanique, le NVMe pour nos artefacts (mesures à l'appui) | `plan-modeles-lourds.md`, `README.md`, `MANIFEST.md` (+2) |
| 12:11 | `400047e3` | Rapports et sprint : les cinq défauts de la revue n°2 et le test qui manquait | `format-clusters.md`, `README.md`, `MANIFEST.md` (+4) |
| 17:43 | `418b5325` | Sprint 09 : ceremonie (onze pistes mesurees, trois retenues) | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 17:43 | `65860083` | Trois dernieres pistes mesurees et ecartees : localite temporelle, ordre des experts, prechargement | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 21:08 | `3b2e0d81` | CPU, hyperthreading, NUMA et NVMe : mesures, et la conclusion qui se retourne | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 21:39 | `954e0861` | Prelecture parallele : implementee, mesuree, sans effet (0,3 %) | `.contexte-long.md.kate-swp`, `.roadmap.md.kate-swp`, `README.md` (+4) |
| 22:47 | `f9a143bc` | Prelecture : quatrieme mecanisme mesure, quatrieme fois sans effet | `gguf.rs`, `README.md`, `MANIFEST.md` (+3) |

## Chiffres du jour

`0,3 %` · `1002 s` · `7963 jetons`

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
- [reports/rapport-optimisations-auto.md](../../reports/rapport-optimisations-auto.md)

<!-- notes -->

<!-- /notes -->
