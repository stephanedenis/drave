# 2026-10-30

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-10-30/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**3 commits** · **0 session(s)** · **3 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| docs | 1 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| modele | 1 | [modele.md](modele.md) |

## Sessions DSH

Aucune session indexée pour ce jour ; voir
[l'index des sessions](../README.md#sessions).

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:04 | `da038e34` | R13.2 + A8.0 — VOCAB 1024 PERD 3,9 % À OCTETS ÉGAUX ; PORTE-INDICE ROUGE QUALIFIÉE |
| 00:06 | `336a2271` | ÉTAT — DATE ALIGNÉE SUR LE COMMIT DU 30 |
| 08:34 | `733232ff` | R06 v5 — LA CALIBRATION COÛTE ~50 GOLDS, LES POIDS APPRIS N'AJOUTENT RIEN, LE PILOTE EST COMPLÉTÉ |

## Le récit de la journée (écrit à la main)

<!-- notes -->
**Session `8156fdcb` — le coût de la calibration, et le pilote complété.**

La cascade à confiance calibrée (R06 v4) égalait l'oracle, mais elle exige des golds. Combien ?
La courbe le dit : **~50 questions** suffisent sur le lexical (0,906 à k=49, contre 0,911 au
maximum), **~25** sur les paraphrases (0,399 à k=25, contre 0,415). Le plateau est atteint tôt —
la calibration est bon marché.

Et les **poids appris** ne valent pas mieux que les poids fixés : identiques sur le lexical,
**pires** sur les paraphrases (0,366 contre 0,415) — une logistique sur 25 à 42 exemples
sur-apprend. Les poids fixés (0,5 couverture + 0,3 accord + 0,2 dispersion) restent.

Le **pilote** est complété : le modèle y donne 0,400 contre 0,600 pour l'extractif — le pilote
est un corpus mixte du côté lexical, cohérent avec la loi « le corpus décide du lecteur ».

La recette de déploiement du programme R est complète : 50 golds → le seuil → la cascade à
confiance, à ~1 point de l'oracle, 12 % d'appels modèle sur un corpus lexical, 85 % sur un
corpus de paraphrases.
<!-- /notes -->
