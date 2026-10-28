# 2026-10-03 — Attention, fenêtre, puits

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (10)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 04:06 | `82a2f7e3` | Le chemin des experts de V4.1 est VÉRIFIÉ en numpy (écart 4e-5) — il ne reste que la composition de l'attention | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 04:10 | `2a96b148` | Attention V4.1 : projections et normes VÉRIFIÉES (1e-6), un écart isolé sur la rotation du Q — instrument fourni, conclusion suspendue | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 04:11 | `3dfa69e3` | Attention V4.1, premiers étages TOUS vérifiés à 1e-6 — l'écart sur q_rope était une faute de MON script | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 04:14 | `7401db81` | Le cœur de l'attention V4.1 est vérifié — blocs compressés et règle de visibilité compris (7e-07) | `README.md`, `MANIFEST.md`, `digest.md` (+4) |
| 04:57 | `170d2900` | Plan P6 : la fenêtre de 63 prédictions ne juge pas la perplexité (seuil à 64), et elle le dit | `plan-deepseek41-complet.md`, `README.md`, `MANIFEST.md` (+2) |
| 06:07 | `11d80f44` | Plan et sprint 23 : le coût du contexte long est attribué à ce qui est MESURÉ (proj+mlp double, l'attention reste plate), l'empreinte des experts reste une hypothèse nommée | `plan-deepseek41-complet.md`, `README.md`, `MANIFEST.md` (+3) |
| 10:55 | `a648f9e1` | KimI-K3 : les deux mathématiques neuves implémentées et testées SANS poids (SiTU, attention résiduelle) | `model.rs`, `README.md`, `MANIFEST.md` (+4) |
| 11:04 | `05a906b4` | CORRECTION : un jeton de Kimi-K3 lit 87 Go de poids (pas 35) — et c'est l'ATTENTION qui domine, pas les experts | `architecture-kimi-k3.md`, `plan-kimi-k3.md`, `README.md` (+6) |
| 11:06 | `69cbff0c` | Sprint 29 : 87 Go par jeton (l'attention dépasse les experts), outils qui disent leur périmètre, et la récurrence du KDA vérifiée | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 12:05 | `20e40578` | Croisement des maths K3 avec le code PUBLIÉ de Moonshot : SiTU, attention résiduelle, projections, convolution, porte bornée — identiques | `architecture-kimi-k3.md`, `README.md`, `MANIFEST.md` (+2) |

## Chiffres du jour

`87 Go`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` — Continue avec REPRISE.md (début 2026-09-28 14:46, 222.5 h) → [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md)

## Mesures et rapports touchés

- [reports/rapport-budget-kimi-k3.md](../../reports/rapport-budget-kimi-k3.md)
- [reports/rapport-gpu-tandem-nvlink.md](../../reports/rapport-gpu-tandem-nvlink.md)

<!-- notes -->

<!-- /notes -->
