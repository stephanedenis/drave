# 2026-11-02 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (31)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 00:03 | `48e35264` | JOURNAL — LE 2 NOVEMBRE : LIEN VERS L'INDEX DES SESSIONS | `README.md`, `mesures.md`, `README.md` (+5) |
| 03:45 | `cc65ff92` | B13 — LE BORD FIN : 73 % À 0,38, 100 % À 0,41 (400 ESSAIS), SEUIL ROBUSTE 0,41 ; 87/87 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+29) |
| 05:21 | `8c82d029` | B13 — L'ANAPHORE : 4/4 LIENS JUSTES, PREMIÈRE MESURE DE CORÉFÉRENCE ; 95/95 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+26) |
| 05:44 | `a880c538` | ÉTAT — LE BUDGET REVIENT À 4000 MOTS (N2.z SUR DEUX GRAINES) | `en-cours.md`, `README.md`, `apprentissage.md` (+14) |
| 09:39 | `4d8c9905` | B13 — LA CORÉFÉRENCE À 68 LIENS : LE RÔLE PASSE DEVANT (52/51), GOLD 372 ; 111/111 | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+28) |
| 09:52 | `41c7d1f1` | B13 — LA CORÉFÉRENCE À 103 LIENS : 86/103, CIBLE 100 ATTEINTE, GOLD 407 ; 112/112 | `moteur-de-pensee.md`, `en-cours.md`, `README.md` (+24) |
| 12:55 | `52c530ce` | ÉTAT — T0 DANS LE BUDGET (3996 MOTS) APRÈS LE GOLD 417 | `en-cours.md`, `README.md`, `apprentissage.md` (+16) |
| 12:57 | `80c37a25` | GLOSSAIRE — LES 10 PAGES PIVOTS LIENT LA PREMIÈRE OCCURRENCE DES TERMES (269 LIENS) ; LE SCRIPT LIE PAR PAGE, PAS « PARTOUT » | `README.md`, `format-flux.md`, `contexte.md` (+13) |
| 13:53 | `81d74433` | B13 — LE LIEN AUTOMATIQUE : 0/5, LE SUJET NE SUFFIT PAS ; 135/135 | `moteur-de-pensee.md`, `en-cours.md`, `README.md` (+18) |
| 14:06 | `651c1fc0` | B13 — LE LIEN AUTOMATIQUE RÉPARÉ : 5/5 APRÈS RÉORDONNANCEMENT ET REPLI PRON/NOUN ; 136/136 | `moteur-de-pensee.md`, `en-cours.md`, `README.md` (+20) |
| 14:13 | `49ca52fb` | B13 — LA CORÉFÉRENCE COMME LIEN : 62/116, LA MOITIÉ DES ANTÉCÉDENTS ; 137/137 | `moteur-de-pensee.md`, `en-cours.md`, `README.md` (+18) |
| 14:20 | `004c5f64` | B13 — LES LIENS CLASSÉS : 50 INTRA, 62 INTER, 4 ABSENTS ; 138/138 | `moteur-de-pensee.md`, `en-cours.md`, `README.md` (+20) |
| 15:57 | `702b368c` | B13 — LES VRAIS ABSENTS : 5 PHRASES, 0 LIEN, GOLD 432 ; 140/140 | `bloc-linguistique.md`, `moteur-de-pensee.md`, `en-cours.md` (+30) |
| 15:59 | `ca06ab0b` | D — L'OCR CEGEP, LE GLOSSAIRE AU RENDU ET LES LIENS DE LA FAMILLE 13 | `README.md`, `format-flux.md`, `contexte.md` (+48) |
| 18:41 | `9250b1c3` | B13 — LA POLITIQUE DRVM/NATIVE : LE CADENAS S'OUVRE AVEC LA RÈGLE (3 NŒUDS), PAS SANS (0) ; PORTE NÉGATIVE | `moteur-de-pensee.md`, `en-cours.md`, `roadmap.md` (+27) |
| 18:47 | `aeace14b` | B13 — LA PORTE DRVM S'OUVRE AVEC LA RÈGLE : 27 NŒUDS, 4 SONDE (200 SANS ; PAS DE BUT) | `moteur-de-pensee.md`, `chantiers.md`, `en-cours.md` (+25) |
| 20:04 | `67ec9cd4` | B13 — LA PORTE MINUTE S'OUVRE AVEC LA RÈGLE (26 NŒUDS, 4 SONDE) ; LE PROMPT LABYRINTHE ÉCHOUE (200, 3) | `en-cours.md`, `roadmap.md`, `README.md` (+29) |
| 20:07 | `a67dbf00` | PILOTAGE — LE REGISTRE DES RESSOURCES : GPU, CPU, NVMe, RAM ET PASSE GLOBALE | `plan-travail.md`, `README.md`, `apprentissage.md` (+20) |
| 20:13 | `a097f650` | NUIT — LE RÉCIT S'OUVRE : QUATRE CLAIMS, LA PASSE DES PORTES ET LE REGISTRE VIVANT | `README.md`, `apprentissage.md`, `attention.md` (+22) |
| 20:18 | `76862005` | PORTES — LE REGISTRE EST DANS `work/`, PAS DANS `/tmp` ; LA PASSE PEUT TOURNER SUR UN SEUL GPU LIBRE | `portes.md`, `README.md`, `apprentissage.md` (+18) |
| 20:20 | `2bbd45e2` | DOCS — LE REGISTRE DES RESSOURCES ENTRE DANS LE ROUTAGE | `ressources.md`, `README.md`, `README.md` (+20) |
| 20:26 | `9a17d0cc` | PILOTAGE — LA NUIT DU 02/11 : QUATRE SESSIONS, UNE PASSE, UN REGISTRE, BILAN 08 H | `plan-travail.md`, `README.md`, `apprentissage.md` (+21) |
| 20:29 | `2fad8e8d` | B13 — LA PORTE MOBILE : LE 7B ÉCHOUE À (3,3) (200 NŒUDS, 3 SONDE) ET PASSE À (1,3) COMME L'AVEUGLE (26/2) ET LE LABYRINTHE (29/5) ; TEST NON DISCRIMINANT | `en-cours.md`, `roadmap.md`, `README.md` (+29) |
| 20:33 | `42db89f6` | NUIT — LA 82e PORTE : RESSOURCES (AUTOTEST 9 CAS, REGISTRE COHÉRENT) ; AVERTISSEMENTS NON FATALS | `references-non-regression.md`, `README.md`, `apprentissage.md` (+24) |
| 20:35 | `20996b87` | NUIT — LA 82e PORTE EST COMPTÉE (82) ; LE BUDGET T1 REVIENT SOUS 2 500 ; S RAFRAÎCHI | `portes.md`, `en-cours.md`, `references-non-regression.md` (+24) |
| 20:49 | `b1c0bcda` | PILOTAGE — UN MANDAT LONG AVEC UN CLAIM ACTIF N'EST PAS PÉRIMÉ ; LA PORTE SESSIONS LIT LE REGISTRE | `README.md`, `apprentissage.md`, `attention.md` (+24) |
| 21:17 | `35ca1461` | B13 — LA PORTE QUI BOUGE : LE 7B LA PASSE (25 NŒUDS, 2 SONDE) MAIS L'AVEUGLE (25/2) ET LE LABYRINTHE (28/5) AUSSI ; TEST NON DISCRIMINANT | `en-cours.md`, `roadmap.md`, `README.md` (+28) |
| 21:26 | `7d2c0a2d` | B13 — LA PORTE STOCHASTIQUE DISCRIMINE : LE 7B L'OUVRE (31 NŒUDS, 6 SONDE) ; SANS LA RÈGLE, 200/3/182,6 S | `en-cours.md`, `roadmap.md`, `README.md` (+30) |
| 21:30 | `0713f4e6` | NUIT — LA PASSE DU 19 h 32 EST AU REGISTRE (76/5) ; B13 140/140 PARTOUT ; T1 À 2 428 MOTS | `chantiers.md`, `en-cours.md`, `plan-travail.md` (+25) |
| 21:35 | `89e0c2c5` | PORTE HOMEOSTASIE — LE MESSAGE N'EXÉCUTE PLUS SA COMMANDE | `README.md`, `portes.md`, `README.md` (+8) |
| 21:53 | `212c23d7` | NUIT — LE JOURNAL DU 03/11 PORTE LE LIEN VERS L'INDEX DES SESSIONS | `README.md`, `apprentissage.md`, `attention.md` (+18) |

## Chiffres du jour

`73 %` · `100 %`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `0733c5bb-f90b-4f58-9241-3364fa32e46c` — Session N2 : plan et réservations (début 2026-11-02 16:14, 6.5 h) → [rapport](../sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md) · [digest](../sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md)
- `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — Continue session work (début 2026-10-31 17:17, 45.3 h) → [rapport](../sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/rapport.md) · [digest](../sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md)
- `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — Session structures CPU analyseur rôles (début 2026-11-02 16:14, 4.4 h) → [rapport](../sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/rapport.md) · [digest](../sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/digest.md)
- `536cd5d6-94ac-4057-8fe9-11709a4587c7` — Étude des sessions et du pilotage (début 2026-11-02 15:33, 7.2 h) → [rapport](../sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/rapport.md) · [digest](../sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/digest.md)
- `abb58991-fe0a-4d6e-b039-6552b09f8454` — Reprise session L/B13 et mise à jour plan (début 2026-11-02 16:15, 6.6 h) → [rapport](../sessions/abb58991-fe0a-4d6e-b039-6552b09f8454/rapport.md) · [digest](../sessions/abb58991-fe0a-4d6e-b039-6552b09f8454/digest.md)
- `b6a672ec-3349-4a4c-9e23-4478aa823170` — Git push to origin remote (début 2026-11-01 13:28, 25.2 h) → [rapport](../sessions/b6a672ec-3349-4a4c-9e23-4478aa823170/rapport.md) · [digest](../sessions/b6a672ec-3349-4a4c-9e23-4478aa823170/digest.md)
- `b7d4678e-2143-4daa-a9a4-a456c5aa8dab` — Reprise session L/B13 et vérification stricte (début 2026-11-02 16:16, 6.5 h) → [rapport](../sessions/b7d4678e-2143-4daa-a9a4-a456c5aa8dab/rapport.md) · [digest](../sessions/b7d4678e-2143-4daa-a9a4-a456c5aa8dab/digest.md)
- `caaf3018-e3e2-4416-8446-11f0335910aa` — Reprise du hub et passe de portes (début 2026-11-02 16:16, 6.5 h) → [rapport](../sessions/caaf3018-e3e2-4416-8446-11f0335910aa/rapport.md) · [digest](../sessions/caaf3018-e3e2-4416-8446-11f0335910aa/digest.md)
- `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Documentation Drave avec diagrammes et implémentation (début 2026-10-31 17:40, 46.0 h) → [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md)
- `fe3c05f0-834b-44f2-8739-501865d652c1` — Lecture de en-cours.md et choix de tâche (début 2026-10-31 17:35, 44.8 h) → [rapport](../sessions/fe3c05f0-834b-44f2-8739-501865d652c1/rapport.md) · [digest](../sessions/fe3c05f0-834b-44f2-8739-501865d652c1/digest.md)

## Mesures et rapports touchés

- [reports/INDEX.md](../../reports/INDEX.md)
- [reports/README.md](../../reports/README.md)
- [reports/historique-passes-portes.md](../../reports/historique-passes-portes.md)
- [reports/rapport-genres.md](../../reports/rapport-genres.md)
- [reports/rapport-n2-anglais-34m.md](../../reports/rapport-n2-anglais-34m.md)
- [reports/rapport-n2-canal-kd-34m.md](../../reports/rapport-n2-canal-kd-34m.md)
- [reports/rapport-n2-echantillon.md](../../reports/rapport-n2-echantillon.md)
- [reports/rapport-n2-fenetre-r1.md](../../reports/rapport-n2-fenetre-r1.md)
- [reports/rapport-n2-multilingue-34m-distille.md](../../reports/rapport-n2-multilingue-34m-distille.md)
- [reports/rapport-n2-multilingue-34m.md](../../reports/rapport-n2-multilingue-34m.md)
- [reports/rapport-n2-professeur.md](../../reports/rapport-n2-professeur.md)
- [reports/rapport-ocr-cegep.md](../../reports/rapport-ocr-cegep.md)
- [reports/rapport-ocr-pdf.md](../../reports/rapport-ocr-pdf.md)
- [reports/rapport-pensee-anaphore-103.md](../../reports/rapport-pensee-anaphore-103.md)
- [reports/rapport-pensee-anaphore-68.md](../../reports/rapport-pensee-anaphore-68.md)
- [reports/rapport-pensee-anaphore.md](../../reports/rapport-pensee-anaphore.md)
- [reports/rapport-pensee-bord-fin.md](../../reports/rapport-pensee-bord-fin.md)
- [reports/rapport-pensee-gold-342.md](../../reports/rapport-pensee-gold-342.md)
- [reports/rapport-pensee-lien-auto-fixe.md](../../reports/rapport-pensee-lien-auto-fixe.md)
- [reports/rapport-pensee-lien-auto.md](../../reports/rapport-pensee-lien-auto.md)
- [reports/rapport-pensee-lien-coref.md](../../reports/rapport-pensee-lien-coref.md)
- [reports/rapport-pensee-liens-classes.md](../../reports/rapport-pensee-liens-classes.md)
- [reports/rapport-pensee-partielle.md](../../reports/rapport-pensee-partielle.md)
- [reports/rapport-pensee-politique-llm.md](../../reports/rapport-pensee-politique-llm.md)
- [reports/rapport-pensee-porte-bouge.md](../../reports/rapport-pensee-porte-bouge.md)
- [reports/rapport-pensee-porte-llm.md](../../reports/rapport-pensee-porte-llm.md)
- [reports/rapport-pensee-porte-minute.md](../../reports/rapport-pensee-porte-minute.md)
- [reports/rapport-pensee-porte-mobile.md](../../reports/rapport-pensee-porte-mobile.md)
- [reports/rapport-pensee-porte-sto.md](../../reports/rapport-pensee-porte-sto.md)
- [reports/rapport-pensee-vrais-absents.md](../../reports/rapport-pensee-vrais-absents.md)
- [reports/rapport-s-analyseur.md](../../reports/rapport-s-analyseur.md)

<!-- notes -->

<!-- /notes -->
