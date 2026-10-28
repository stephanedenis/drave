# 2026-09-29 — Attention, fenêtre, puits

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (10)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 11:57 | `fd695bc5` | Item 8 : premiers resultats d'attention creuse (et ils sont opposes) | `contexte-long.md`, `README.md`, `MANIFEST.md` (+2) |
| 13:54 | `2383eaea` | préremplissage par lots : attention groupée, tête en lot, et un pointeur gras | `REPRISE.md`, `MANIFEST.md`, `digest.md` (+5) |
| 14:29 | `bc168979` | E4 : KV déporté en VRAM, attention sur le GPU, mesuré à 1 M de clés | `REPRISE.md`, `contexte-long.md`, `MANIFEST.md` (+8) |
| 14:32 | `a5936037` | docs E4 : comment le noyau d'attention a été validé (cas dégénérés, trois bugs) | `contexte-long.md`, `MANIFEST.md`, `digest.md` (+1) |
| 18:05 | `a64328d3` | GPU : dépaquetage vectorisé du noyau d'attention (×1,8 à ×2,3 à 1 M de clés) | `contexte-long.md`, `MANIFEST.md`, `digest.md` (+7) |
| 18:28 | `5dfa6b19` | Chantier 1-2 : aiguille v2, experts MXFP4 en VRAM, attention par lots déportée | `MANIFEST.md`, `digest.md`, `rapport.md` (+3) |
| 19:27 | `4512f697` | Chantiers 1, 2b, 2c : aiguille 12/12, attention par lots déportée ×2,8, experts +6 % | `REPRISE.md`, `contexte-long.md`, `MANIFEST.md` (+5) |
| 20:56 | `0c7d3166` | vision : détailler le pas suivant (couche, rotation 2-D, attention locale, injection) | `plan-mla-vision.md`, `README.md`, `MANIFEST.md` (+2) |
| 21:11 | `1e9a350c` | vision : la fenêtre locale lue dans la source de llama.cpp (et la rotation localisée) | `plan-mla-vision.md`, `MANIFEST.md`, `digest.md` (+1) |
| 21:46 | `c1c100eb` | vision : la rotation est confirmée par la source, et une variante de fenêtre découverte | `plan-mla-vision.md`, `MANIFEST.md`, `digest.md` (+1) |

## Chiffres du jour

`+6 %` · `×2,8` · `×1,8` · `×2,3`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` — Continue avec REPRISE.md (début 2026-09-28 14:46, 222.5 h) → [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md)

## Mesures et rapports touchés

- [reports/aiguille-30b.md](../../reports/aiguille-30b.md)
- [reports/aiguille-gpt-oss.md](../../reports/aiguille-gpt-oss.md)
- [reports/rapport-aiguille.md](../../reports/rapport-aiguille.md)
- [reports/rapport-prefill-par-lots.md](../../reports/rapport-prefill-par-lots.md)

<!-- notes -->

<!-- /notes -->
