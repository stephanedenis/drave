# 2026-10-28 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (19)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 08:14 | `4bb0ed7b` | DOCS — RETRAIT DES EN-TÊTES « RÉVISION DOCUMENTAIRE » ; ÉTAT, CARTE, ROADMAP ET INDEX COMPACTÉS (215/282/54) | `AGENTS.md`, `REPRISE.md`, `README.md` (+17) |
| 10:56 | `e8b4e2c7` | N1.2 — DRAVE-N0 : PPL 3,353 EN 10 000 PAS, DRVM 110 TENSEURS, 11,37 M | `en-cours.md`, `2026-10-28.md`, `2026-10-28_docs.md` (+4) |
| 11:07 | `098de56b` | N1.4 — TÊTES PRÉCOCES : 55,15 / 60,94 / 62,13 % CONTRE 62,55 %, TÉMOIN 0,39 % | `en-cours.md`, `roadmap-native.md`, `2026-10-28.md` (+6) |
| 11:21 | `ba4fd592` | N1.5 — PENSÉE CONTRACTANTE : λ = 0,709 ; SANS PENSÉE PPL 721 726, AVEC 3,53 | `en-cours.md`, `roadmap-native.md`, `2026-10-28.md` (+8) |
| 11:36 | `75fe635d` | N0.3b — DRVM ↔ CHECKPOINT : 114/114 TENSEURS IDENTIQUES | `en-cours.md`, `roadmap-native.md`, `2026-10-28.md` (+6) |
| 11:38 | `2bd25490` | N1.7 — RÉFLEXE : 4 BLOCS 5,978 MS CONTRE 6 BLOCS 7,871 MS, −24,05 % POUR −1,61 POINT | `en-cours.md`, `roadmap-native.md`, `2026-10-28.md` (+6) |
| 12:12 | `2958f80b` | N0.3b — PPL DU RETOUR DRVM : 28,7355 IDENTIQUE, MAIS PAS D'EXÉCUTION NATIVE | `en-cours.md`, `roadmap-native.md`, `2026-10-28.md` (+4) |
| 13:25 | `acd9c623` | MÉTHODE — ÉCHANTILLONNAGE VAN DER CORPUT, DÉTERMINISTE ET REPRODUCTIBLE | `README.md`, `echantillonnage-vdc.md`, `en-cours.md` (+10) |
| 14:52 | `32195457` | N4.1 — GÉNÉRATION : COHÉRENT 12 OCTETS PUIS DÉRIVE, PAS UN ASSISTANT | `en-cours.md`, `roadmap-native.md`, `README.md` (+6) |
| 15:00 | `bedeebae` | MÉTHODE — REPRENDRE UN GOAL EN PAUSE (GET_GOAL → UPDATE_GOAL RESUME) ; INDEX 230 | `REPRISE.md`, `continuite.md`, `README.md` (+3) |
| 15:38 | `f71565c3` | N4.2 — SERVICE LOCAL : /SANTE ET /GENERER, 69 OCTETS, CPU, GREEDY | `en-cours.md`, `roadmap-native.md`, `README.md` (+6) |
| 15:45 | `641a48c6` | N0.8 — PARITÉ NATIVE AUTOMATISÉE : 5/5 PROMPTS, TOP-5 IDENTIQUE, ÉCART < 0,0001 | `en-cours.md`, `roadmap-native.md`, `README.md` (+5) |
| 16:26 | `d97076b8` | N0.11 — TEST RUST AUTONOME DE LA PASSE AVANT NATIVE, FIXTURE 36 KO | `en-cours.md`, `roadmap-native.md`, `native.rs` (+5) |
| 16:52 | `1daa8741` | N2.9 — 21,63 M SUR 20 000 PAS : PPL 3,381, PIRE QUE 11,47 M (3,123) | `en-cours.md`, `README.md`, `moteur.md` (+3) |
| 20:11 | `8b28f889` | N4.4 — SERVICE DURCI : JETON 401/200, CORPS 64 KO, N ≤ 256 ; PAS DE SFT | `en-cours.md`, `roadmap-native.md`, `native.rs` (+6) |
| 20:22 | `923d70ed` | N2.10 — PROFESSEUR 10 000 PAS : 1,073 BIT/OCTET, PPL 2,104 | `en-cours.md`, `README.md`, `mesures.md` (+3) |
| 20:59 | `678eb20f` | N2.12 — PROFESSEUR 10K : PPL 2,910 CONTRE 3,082, TÊTE 3 69,97 % | `en-cours.md`, `README.md`, `apprentissage.md` (+4) |
| 21:22 | `8c40af98` | N2.13 — 20 000 PAS DE PLUS : PPL 2,876, PRÉCISION 70,00 % | `en-cours.md`, `README.md`, `mesures.md` (+4) |
| 21:28 | `29c4fd1b` | N2.15 — PROFESSEUR 20 000 PAS : 0,904 BIT/OCTET, PPL 1,869 | `en-cours.md`, `README.md`, `mesures.md` (+4) |

## Chiffres du jour

`0,904` · `1,869` · `70,00 %` · `2,876` · `69,97 %` · `2,910` · `3,082` · `1,073` · `2,104` · `3,381` · `3,123` · `0,0001`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Mesures et rapports touchés

- [reports/INDEX.md](../../reports/INDEX.md)
- [reports/README.md](../../reports/README.md)
- [reports/rapport-coherence-docs-3.md](../../reports/rapport-coherence-docs-3.md)
- [reports/rapport-drvm-parite.md](../../reports/rapport-drvm-parite.md)
- [reports/rapport-drvm-ppl.md](../../reports/rapport-drvm-ppl.md)
- [reports/rapport-native-21m-20k.md](../../reports/rapport-native-21m-20k.md)
- [reports/rapport-native-generation.md](../../reports/rapport-native-generation.md)
- [reports/rapport-native-n0.md](../../reports/rapport-native-n0.md)
- [reports/rapport-native-parite.md](../../reports/rapport-native-parite.md)
- [reports/rapport-native-pensee.md](../../reports/rapport-native-pensee.md)
- [reports/rapport-native-prof10k-2.md](../../reports/rapport-native-prof10k-2.md)
- [reports/rapport-native-prof10k.md](../../reports/rapport-native-prof10k.md)
- [reports/rapport-native-professeur-10k.md](../../reports/rapport-native-professeur-10k.md)
- [reports/rapport-native-professeur-20k.md](../../reports/rapport-native-professeur-20k.md)
- [reports/rapport-native-reflexe.md](../../reports/rapport-native-reflexe.md)
- [reports/rapport-native-service-auth.md](../../reports/rapport-native-service-auth.md)
- [reports/rapport-native-service.md](../../reports/rapport-native-service.md)
- [reports/rapport-native-test.md](../../reports/rapport-native-test.md)
- [reports/rapport-native-tetes.md](../../reports/rapport-native-tetes.md)

<!-- notes -->

<!-- /notes -->
