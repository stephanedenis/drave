# 2026-10-21 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [2026-10-21.md](2026-10-21.md). Convention : `docs/organisation-du-depot.md`.

## Commits du jour (8)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 03:45 | `a8788cd8` | MESURE 87 — LA COMPOSITION PLAFONNE ENTRE 7 ET 14 B : 0,68 / 0,855 au 14 B (couche 16) contre 0,76 / 0,865 au 7 B (couche 14) — le gain de taille s'arrete, et l'OOM de la repartition invite a la prudence. Le sens reste a mi-profondeur (16/48 = 33 %) et la derniere couche s'effondre (0,050) | `en-cours.md`, `05-la-pensee-sans-verbaliser.md`, `2026-10-21.md` (+6) |
| 05:30 | `59a12737` | MESURE 93 — BBC SEUL : L'ECRITURE MONTE DE -4,1 A -0,5 (+3,6) MAIS NE PASSE PAS LE PLANCHER. Sur les 50 pages, la marge reste negative (IC [-3,3 ; +2,2]) ; la lecture est stable (+0,2 -> +1,0) et la traduction generale perd 1,2. Le corpus monolingue seul ne suffit pas : il manque les PAIRES | `en-cours.md`, `2026-10-21.md`, `2026-10-21_memoire.md` (+4) |
| 06:07 | `0bd8f485` | MESURE 95 — LES 2 832 PAIRES TRANSLATEWIKI AMELIORENT L'ECRITURE : marge poolee +1,3 [-0,9 ; +3,5] sur les 50 pages (28/50), contre -2,3 sans les paires — +3,6 points. L'ecriture passe de significativement negative a positivement marginale ; les PAIRES sont le levier, il en faut plus pour reduire l'IC | `en-cours.md`, `2026-10-21.md`, `2026-10-21_apprentissage.md` (+6) |
| 06:21 | `236b24fd` | MESURE 96 — LES PAIRES BIBLIQUES DEGRADENT L'ECRITURE : marge poolee -4,6 [-7,9 ; -1,1] sur les 50 pages (14/50), pire que sans paires (-2,3) et que translatewiki (+1,3). LE REGISTRE COMPTE PLUS QUE LE VOLUME : 30 950 paires archaiques/religieuses (KJV vs PCMWBT 2019) apprennent la langue de la Bible, pas celle des contes | `en-cours.md`, `2026-10-21.md`, `2026-10-21_distribue.md` (+5) |
| 06:34 | `1878edf7` | MESURE 97 — LA BIBLE MODERNE (WEB) NE SAUVE RIEN : marge -6,2 [-10,5 ; -2,1] (17/50), PIRE que le KJV (-4,6). C'est le REGISTRE religieux qui nuit, pas l'archaisme. Il faut des paires NARRATIVES MODERNES (contes, actualites, dialogues), pas des textes sacres | `en-cours.md`, `2026-10-21.md`, `2026-10-21_distribue.md` (+5) |
| 06:38 | `14521b49` | DOCUMENTATION — LA LECON DU REGISTRE entre dans la synthese : 30 950 paires bibliques DEGRADENT la traduction du pidgin (-4,6 avec le KJV, -6,2 avec le WEB moderne), quand 2 832 paires modernes l'ameliorent (+1,3). Le registre compte plus que le volume et que la modernite (mesures 96-97) | `en-cours.md`, `07-modeles-alternatifs-entree-sortie.md`, `2026-10-21.md` (+1) |
| 06:51 | `f7f9069e` | MESURE 98 — LA VALIDATION CROISEE A 7 CONTES (71 pages) CONFIRME LE SEUIL : marge +0,9 [-0,9 ; +2,9], 36/71 pages — positive, pas significative. Les deux contes manquants (0066 : +3,1 ; 0327 : +0,0) ont ete recuperes dans le depot GitHub (pages en level3-txt) ; l'ecriture reste au seuil et demande plus de paires narratives | `en-cours.md`, `2026-10-21.md`, `2026-10-21_distribue.md` (+5) |
| 07:04 | `4f062d44` | OUTIL — k-fold : option --repartir pour le 7 B ; le 7 B OOM sur 2x16 Go avec les logits plein vocabulaire (batch 2, 256 jetons). Le 3 B reste le modele mesure ; un 7 B batch 1 + gradient checkpointing est a essayer | `en-cours.md`, `2026-10-21.md`, `2026-10-21_distribue.md` (+1) |

## Chiffres du jour

`16 Go` · `256 jetons` · `30950 paires` · `2832 paires` · `33 %` · `0,855` · `0,865` · `0,050`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Mesures et rapports touchés

- [reports/07-mesures-couche-commune.md](../reports/07-mesures-couche-commune.md)
- [reports/README.md](../reports/README.md)

<!-- notes -->

<!-- /notes -->
