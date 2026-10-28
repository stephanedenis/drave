# 2026-09-29 — Moteur : chargement, calcul, listes, quantification

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (27)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 07:23 | `51a14a0b` | Item 3 : cache KV quantifie int8 et int4 empaquete | `contexte-long.md`, `README.md`, `MANIFEST.md` (+3) |
| 07:48 | `aa70d548` | Item 6 : une seule analyse de la ligne de commande pour les quatre modes | `REPRISE.md`, `README.md`, `MANIFEST.md` (+3) |
| 08:55 | `21ac631d` | Item 7 (1/2) : noyau GPU une warp par ligne, la tete redevient deportable | `REPRISE.md`, `README.md`, `MANIFEST.md` (+10) |
| 09:46 | `fba67b61` | Item 4 : prefill par lots -- justesse corrigee, debit a mesurer au calme | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 10:08 | `3091473d` | Item 7 (2/2) : noyaux GPU 4 bits -- MXFP4 et Q4_K, une warp par ligne | `REPRISE.md`, `README.md`, `MANIFEST.md` (+6) |
| 10:36 | `5719501b` | Item 4 : MoE par lots -- regroupement des jetons par expert | `REPRISE.md`, `README.md`, `MANIFEST.md` (+4) |
| 11:31 | `6a64b354` | Item 3 : KV quantifie mesure aussi a 4 600 jetons, et compare a llama.cpp | `contexte-long.md`, `README.md`, `MANIFEST.md` (+4) |
| 12:09 | `71dbcf5c` | Item 4 : le GEMM sur le pool, et le gain reel attribue poste par poste | `REPRISE.md`, `README.md`, `MANIFEST.md` (+5) |
| 14:06 | `f5788625` | noyau Q6_K sur GPU, et tête Q6_K déportée dans le moteur | `REPRISE.md`, `MANIFEST.md`, `digest.md` (+6) |
| 14:30 | `8438883b` | docs: préciser que QT_GPU_KV exige QT_GPU (le pilote ne s'ouvre que sur QT_GPU) | `contexte-long.md`, `README.md`, `MANIFEST.md` (+2) |
| 14:44 | `e6a5effd` | KV déporté : corriger la copie du chemin par lots | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 15:45 | `19535755` | rotation : le seuil de bascule à 4 096 était trop bas (mesuré à 5 120) | `REPRISE.md`, `contexte-long.md`, `MANIFEST.md` (+3) |
| 16:53 | `54f9fa61` | KV quantifié mesuré à 8 192 jetons, la longueur de la comparaison llama.cpp | `REPRISE.md`, `contexte-long.md`, `README.md` (+3) |
| 17:05 | `45948e2d` | porte gpt-oss : préciser qu'elle se mesure SANS QT_GPU | `REPRISE.md`, `MANIFEST.md`, `digest.md` (+1) |
| 18:46 | `bc5aa9a6` | Chantier 3 : cache KV CPU paginé (0,03 Go à ctx 1 M au lieu de 25,77 Go) | `contexte-long.md`, `MANIFEST.md`, `digest.md` (+2) |
| 20:08 | `d5ee7a05` | MLA : le moteur retrouve la référence numpy à 5,2e-7 près | `plan-mla-vision.md`, `MANIFEST.md`, `digest.md` (+4) |
| 20:48 | `15170886` | Rotation à 16 384 jetons : le RoPE simple gagne encore (35,18 contre 1 133,02) | `REPRISE.md`, `contexte-long.md`, `MANIFEST.md` (+3) |
| 20:49 | `a50a5a58` | vision : inventaire exact des tenseurs (et deux corrections du plan) | `plan-mla-vision.md`, `MANIFEST.md`, `digest.md` (+2) |
| 20:51 | `2ca9e0d4` | Vision : l'embedding de patchs est fait et validé (5,4e-7 contre numpy) | `REPRISE.md`, `plan-mla-vision.md`, `MANIFEST.md` (+4) |
| 20:53 | `c165fcfd` | Vision : le projecteur est validé aussi (1,7e-6) — les deux extrémités du chemin image tiennent | `REPRISE.md`, `plan-mla-vision.md`, `MANIFEST.md` (+4) |
| 20:57 | `9cdc4aea` | Vision : une couche du ViT est validée aussi (1,8e-6) | `REPRISE.md`, `plan-mla-vision.md`, `README.md` (+5) |
| 21:01 | `7802cc85` | Vision : la tour entière tourne (32 couches + v.post_ln) | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 21:05 | `43eee825` | Vision : le point d'injection des embeddings est en place | `plan-mla-vision.md`, `MANIFEST.md`, `digest.md` (+2) |
| 21:23 | `1961ea4b` | vision : le chemin image est complet (224 × 224 → 64 jetons de 3584 dimensions) | `plan-mla-vision.md`, `MANIFEST.md`, `digest.md` (+3) |
| 21:37 | `081c669a` | vision : rotation corrigée d'après ggml — et un défaut d'ordre mis au jour | `plan-mla-vision.md`, `MANIFEST.md`, `digest.md` (+2) |
| 21:41 | `c13232dc` | vision : l'ordre du pipeline est corrigé — et la preuve est que le chiffre CHANGE | `plan-mla-vision.md`, `MANIFEST.md`, `digest.md` (+2) |
| 21:46 | `d084e437` | vision : la chaîne complète est démontrée, de l'image aux logits | `plan-mla-vision.md`, `MANIFEST.md`, `digest.md` (+2) |

## Chiffres du jour

`× 224` · `64 jetons` · `32 couches` · `16384 jetons` · `0,03 Go` · `25,77 Go` · `8192 jetons` · `4600 jetons`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` — Continue avec REPRISE.md (début 2026-09-28 14:46, 222.5 h) → [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md)

## Mesures et rapports touchés

- [reports/rapport-prefill-par-lots.md](../../reports/rapport-prefill-par-lots.md)

<!-- notes -->

<!-- /notes -->
