# 2026-10-09 — Modèles, entraînement, parcimonie, biologie

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (23)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 00:05 | `9cdfbd7b` | Le banc des encodages ne plante plus sur les modèles K-quant (c'était la première ligne de l'aide) | `gguf.rs`, `main.rs`, `MANIFEST.md` (+2) |
| 03:35 | `a5c4d499` | Rapport du modèle : la courbe d'échelle 256/384/512, et le routage qui s'inverse | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 04:04 | `b15d1a0e` | Spéculatif : c'est le RAPPORT DE COÛT qui décide, et il est minimal sur un modèle plus gros que la RAM | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 04:26 | `67c13a6a` | Parcimonie IMPOSÉE ou APPRISE : la réponse est mesurée, et elle est nette | `MANIFEST.md`, `digest.md`, `rapport.md` (+2) |
| 05:07 | `cc8f1e1a` | Parcimonie apprise : le tableau complet à trois modèles, et la recette qui en sort | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 05:36 | `a595bf72` | Le lot sur un modèle plus gros que la RAM : le moteur refuse, et il dit pourquoi | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 06:24 | `b61cc969` | Échelle 512 : la recette creuse tient, et le débit ne distingue plus les deux chemins | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 08:23 | `2ee0305a` | Rapport du modèle : la recette du modèle nativement événementiel | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 09:15 | `ff3ae75e` | Distinguer le moteur du modèle : évaluer un modèle ad hoc pour Drave | `modele-pour-drave.md`, `MANIFEST.md`, `digest.md` (+2) |
| 09:53 | `5e32971e` | 80 000 pas : meilleur en fp32, PIRE après export — le format fait partie du modèle | `modele-pour-drave.md`, `MANIFEST.md`, `digest.md` (+2) |
| 10:02 | `f27530e6` | Moteur contre modèle : un tableau qui dit, pour chaque mesure, de qui elle parle | `modele-pour-drave.md`, `MANIFEST.md`, `digest.md` (+1) |
| 10:27 | `1f6889e8` | Biologie : ce que les connectomes imposent comme contraintes, et l'expérience E1 outillée | `biologie-pour-drave.md`, `MANIFEST.md`, `digest.md` (+2) |
| 10:58 | `2919789b` | Le fait biologique que nos modèles ne reproduisent pas : des poids à queue lourde | `biologie-pour-drave.md`, `MANIFEST.md`, `digest.md` (+1) |
| 11:10 | `33cc4551` | E6 outillée : poids log-normaux (theta = log|w| appris, signes figés à la naissance) | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 11:40 | `458e3082` | Les deux axes appris se cumulent : +poids élagués appris = ÷2 lectures à qualité égale | `modele-pour-drave.md`, `MANIFEST.md`, `digest.md` (+2) |
| 12:12 | `47a180da` | E1 : un connectome inné ALÉATOIRE coûte 1 % de perplexité et divise les lectures par 4 | `biologie-pour-drave.md`, `MANIFEST.md`, `digest.md` (+1) |
| 12:51 | `d222f9d8` | E6 (poids log-normaux) : échec de code, consigné comme tel — le modèle sauvegardé n'est pas le modèle entraîné | `biologie-pour-drave.md`, `MANIFEST.md`, `digest.md` (+1) |
| 12:52 | `e164570a` | E6 : le soupçon de matérialisation est testé et ÉLIMINÉ (écart 0,000e+00) — le défaut est ailleurs | `biologie-pour-drave.md`, `MANIFEST.md`, `digest.md` (+2) |
| 13:03 | `323b572b` | E6 : mesure définitive — le fichier sauvé ne reproduit pas le modèle entraîné | `biologie-pour-drave.md`, `MANIFEST.md`, `digest.md` (+2) |
| 13:24 | `255088df` | L'architecture du cerveau face à Drave : les briques y sont, les formes non | `architecture-cerveau-et-drave.md`, `biologie-pour-drave.md`, `MANIFEST.md` (+2) |
| 13:50 | `3609f076` | Statuts d'expériences à jour : E1 et E3 faits, E2/E4 cadrées, et le pendant GPU du noyau de listes ajouté au plan | `biologie-pour-drave.md`, `modele-pour-drave.md`, `MANIFEST.md` (+2) |
| 15:23 | `d29147cc` | Dim 512 : la structure innée coûte +6,7 % (contre +1,0 % à dim 384) pour ÷3,7 de lectures | `biologie-pour-drave.md`, `MANIFEST.md`, `digest.md` (+2) |
| 16:25 | `f8bd3f6e` | Dim 512 : le prix de la parcimonie croît avec l'échelle (+6,7 % et +8,0 % contre +1,0 % et +3,8 % à 384) | `biologie-pour-drave.md`, `MANIFEST.md`, `digest.md` (+2) |

## Chiffres du jour

`+6,7 %` · `+8,0 %` · `+1,0 %` · `+3,8 %` · `÷3,7` · `1 %` · `÷2`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `d31b3d9b-58e4-4d34-85fa-381b6f6a6a76` — Où en est-on (début 2026-10-08 09:11, 71.0 h) → [rapport](../sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/rapport.md) · [digest](../sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/digest.md)

## Mesures et rapports touchés

- [reports/rapport-campagne-benefices.md](../../reports/rapport-campagne-benefices.md)
- [reports/rapport-modele-moteur.md](../../reports/rapport-modele-moteur.md)

<!-- notes -->
` … `
<!-- /notes -->
