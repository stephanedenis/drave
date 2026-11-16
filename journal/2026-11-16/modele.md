# 2026-11-16 — Modèles, entraînement, parcimonie, biologie

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (12)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 03:12 | `3c10e3ee` | V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON | `en-cours.md`, `references-non-regression.md`, `roadmap.md` (+18) |
| 07:57 | `6f5e0f0c` | SOUS-MODULES — LE DOCWATCH REPINÉ SUR 95e94c4 (LE PIN d256888 N'EXISTE PAS SUR LE REMOTE) ; LE CLONE --recurse-submodules PASSE | `en-cours.md`, `README.md`, `docs.md` (+10) |
| 10:44 | `cf3f9bc7` | NATIF — LE BANC DE GÉNÉRATION (20 PROMPTS, 3 RÉGLAGES, LE CONTRÔLE ALÉATOIRE) : LE MODÈLE A APPRIS LES MOTS (0,87 CONTRE 0,34) PAS LA PHRASE (RÉPÉTITION 15 EN GREEDY) | `en-cours.md`, `README.md`, `docs.md` (+15) |
| 10:53 | `b2dfc1cc` | NATIF — LE BANC DE GRAMMATICALITÉ : NOTRE ANALYSEUR JUGE LE MODÈLE (GV 6,9 CONTRE 2,3 AU HASARD, MAIS LE CIMENT EST BAS : DES MOTS SANS LA GLU) | `en-cours.md`, `README.md`, `distribue.md` (+14) |
| 11:00 | `90fb737a` | NATIF — LA SYNTHÈSE HONNÊTE : L'ÉCHELLE, LA DONNÉE, L'ALIGNEMENT, LE RUNTIME (LE TOKENIZER MESURÉ N'EST PAS LE LEVIER) ; LES 4 PALIERS CHIFFRÉS | `en-cours.md`, `README.md`, `distribue.md` (+13) |
| 11:09 | `4a389c08` | NATIF — drave generer : LE MODÈLE ACCESSIBLE (torch + checkpoint, JSON), LES REFUS PROPRES (4 SANS TORCH OU SANS MODÈLE), LE CAVEAT EXPÉRIMENTAL DOCUMENTÉ | `en-cours.md`, `README.md`, `README.md` (+14) |
| 11:16 | `4c3d502a` | NATIF — LA CARTE DU MODÈLE (IDENTITÉ, DONNÉES, MESURES, LIMITES, USAGE PRÉVU, LICENCE) ; LE README DES FICHES ALLÉGÉ | `en-cours.md`, `README.md`, `distribue.md` (+13) |
| 11:52 | `60c40aa6` | NATIF — L'ÉCHELLE MESURÉE (11 M → 21 M → 34 M) : LES MOTS VALIDES 0,247 → 0,494 → 0,870, LA RÉPÉTITION 1 → 6 → 15 ; L'ÉCHELLE ACHÈTE LE VOCABULAIRE, PAS LA COMPOSITION | `en-cours.md`, `README.md`, `distribue.md` (+14) |
| 11:56 | `d251babf` | NATIF — LE BILAN DU 16/11 : LE DIAGNOSTIC EST TRANCHÉ (LA COMPOSITION MANQUE ; L'ÉCHELLE ACHÈTE LE VOCABULAIRE ; LE PLAN AUX 4 PALIERS) | `en-cours.md`, `README.md`, `distribue.md` (+14) |
| 14:53 | `ac19793a` | NATIF — LE PLAN MIS À JOUR : ÉPINGLER LE CORPUS AVANT D'ENTRAÎNER (LE 2,40 N'EST PAS REPRODUCTIBLE) ; C'EST LE PREMIER PAS DU PALIER 1 | `en-cours.md`, `natif-plan.md`, `README.md` (+5) |
| 15:00 | `86fde794` | ÉTAT — LA LIGNE N À JOUR : LE DIAGNOSTIC TRANCHÉ (LE BANC, L'ÉCHELLE, LA NUMPY, LE 2,40 NON REPRODUCTIBLE) ; LA SUITE : ÉPINGLER LE CORPUS | `en-cours.md`, `README.md`, `distribue.md` (+10) |
| 15:04 | `956bdd5b` | NATIF — LA SYNTAXE À L'ÉCHELLE : GV 1,90 → 2,65 → 6,90, CIMENT 0,137 → 0,278 → 0,335 ; L'ÉCHELLE AIDE LA STRUCTURE, LA GLU RESTE SOUS LE HASARD | `en-cours.md`, `README.md`, `distribue.md` (+12) |

## Chiffres du jour

`0,137` · `0,278` · `0,335` · `0,247` · `0,494` · `0,870`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Documentation Drave avec diagrammes et implémentation (début 2026-10-31 17:40, 382.4 h) → [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md)

## Mesures et rapports touchés

- [reports/INDEX.md](../../reports/INDEX.md)
- [reports/README.md](../../reports/README.md)
- [reports/fiche-modele-natif.md](../../reports/fiche-modele-natif.md)
- [reports/rapport-banc-generation.md](../../reports/rapport-banc-generation.md)
- [reports/rapport-bilan-exploitable-2.md](../../reports/rapport-bilan-exploitable-2.md)
- [reports/rapport-bilan-natif.md](../../reports/rapport-bilan-natif.md)
- [reports/rapport-natif-exploitable.md](../../reports/rapport-natif-exploitable.md)

<!-- notes -->

<!-- /notes -->
