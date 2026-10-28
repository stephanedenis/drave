# 2026-10-03 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (9)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 03:34 | `e5ce21c6` | Localisation V4.1 : la tête (1e-4) et le routeur (sélection identique à la trace) sont vérifiés en numpy — il ne reste que la COMPOSITION des experts | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 04:18 | `859d2b7b` | Porte Drave de P6 : DEUX des quatre points ne tiennent pas — flux illisible par l'outil d'analyse, rejeu non identique (mesuré) | `plan-deepseek41-complet.md`, `README.md`, `MANIFEST.md` (+2) |
| 04:30 | `293051a7` | Porte de correction de P6, mesurée sur V4-Flash avec des protocoles ALIGNÉS : logits à 1-2 %, corrélations ≥ 0,9979 — mais la perplexité n'est pas le bon instrument | `plan-deepseek41-complet.md`, `README.md`, `MANIFEST.md` (+2) |
| 08:30 | `1aa234cb` | Sprint 25 : le « coût qui croît avec la position » était le DISQUE DUR, pas le moteur — protocole rejoué à l'identique sur NVMe | `plan-deepseek41-complet.md`, `README.md`, `MANIFEST.md` (+3) |
| 09:52 | `90709486` | Audit : préciser ce que « flux » veut dire pour V4 — les paires sont comptées (16,2 G/jeton) mais la part en listes est NULLE, le calcul est dense. Le contrat d'échange est tenu, pas encore l'unité de calcul | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 10:37 | `7f330f10` | Défaut SILENCIEUX corrigé : le motif de pré-découpage kimi manquait (Kimi-K2.7 ET Kimi-K3) | `tokenizer.rs`, `README.md`, `MANIFEST.md` (+2) |
| 10:42 | `8f73c6d2` | Deuxième défaut trouvé par un test unitaire : le découpage par casse enjambait les majuscules | `tokenizer.rs`, `README.md`, `MANIFEST.md` (+5) |
| 11:45 | `d541216d` | Protocole de vérification de Kimi-K3 : les 13 points de comparaison de la référence, l'ordre, les tolérances, et le premier jalon (couche 0) | `verification-kimi-k3.md`, `README.md`, `MANIFEST.md` (+2) |
| 11:49 | `45c757f1` | Débits remesurés : RAM 40 Go/s à 8 fils (pas 20), NVMe 3,4 Go/s à 4 flux — le budget de Kimi-K3 refait | `README.md`, `MANIFEST.md`, `digest.md` (+5) |

## Chiffres du jour

`40 Go` · `3,4 Go` · `-2 %` · `0,9979`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` — Continue avec REPRISE.md (début 2026-09-28 14:46, 222.5 h) → [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md)

## Mesures et rapports touchés

- [reports/rapport-budget-kimi-k3.md](../../reports/rapport-budget-kimi-k3.md)
- [reports/rapport-portes-p0-p9.md](../../reports/rapport-portes-p0-p9.md)
- [reports/rapport-reutilisation-experts.md](../../reports/rapport-reutilisation-experts.md)

<!-- notes -->

<!-- /notes -->
