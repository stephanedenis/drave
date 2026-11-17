# 2026-11-17

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-17/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**10 commits** · **2 session(s)** · **5 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 1 | [distribue.md](distribue.md) |
| mesures | 1 | [mesures.md](mesures.md) |
| modele | 1 | [modele.md](modele.md) |
| moteur | 6 | [moteur.md](moteur.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `d67a9bb1-090e-4f69-baf2-a831c00aa275` | Intérêt pour le FPGA maintenant | 2026-11-17 09:50 | 5.6 h | [rapport](../sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/rapport.md) · [digest](../sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/digest.md) |
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 406.8 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 08:27 | `44fb939c` | GPU — L'AMP LIVRÉ (autocast + GradScaler dans entrainer_native), LE PAS RÉEL MESURÉ : 1 S SANS LES TÊTES (2,4× LE CPU NU), 9 S AVEC — LE 34 M RESTE TROP PETIT, LE GPU VAUT AUX PALIERS 100 M+ |
| 11:26 | `97579a55` | DRVM — LE LECTEUR REFUSE CE QU'IL N'EXÉCUTE PAS : routes/régions/têtes/pensée/pont ÉTAIENT DÉCLARÉS ET IGNORÉS EN SILENCE ; 10 REFUS NOMMÉS, LES DEUX LECTEURS D'ACCORD, 62 DRVM RELUS |
| 13:23 | `20648db7` | N3.7 — LES VARIANTES SONT UN CONTRAT : SUBSTITUTION 4,768e-07 ≤ 1e-4 · CONTRÔLE NÉGATIF 5,790e-03 > 1e-4 · COÛT 87,0/86,4 ms (0,99×) |
| 13:31 | `337715d1` | N3.7b — LE MOTEUR NUMPY EXÉCUTE LE PROFIL : BLOQUE 2,831e-07 ≤ 1e-4, FLOU REFUSÉ |
| 13:47 | `49904862` | N3.8 — LES ROUTES SONT EXÉCUTÉES : SEUIL 0 = FLOU BIT-EXACT · SEUIL 10^9 = DEFAUT BIT-EXACT · MIXTE 5,779e-03 / 1,132e-05 DÉTERMINISTE |
| 13:56 | `b480a439` | N3.9 — LES DEUX MOTEURS RENDENT LE MÊME CORPS : RUST ↔ NUMPY 3,576e-07 (DEFAUT), 2,384e-07 (BLOQUE), COMPARATEUR NON VIDE À 5,790e-03 |
| 14:35 | `de967b7b` | N3.10 — `COURT` : LE PREMIER PROFIL QUI PAIE — BIT-EXACT < 64 o · 3,633e-02 AU-DELÀ · 0,694× LE TEMPS · SUR LE 34 M PPL 23,7480 → 23,5824 ET ~5 % |
| 14:39 | `24cb295e` | A5.4 — LE MATÉRIEL FPGA EXISTE : 4 CARTES + RING 40G + ETHERNET DÉDIÉS ; LE BLOCAGE DEVIENT L'ACCÈS AU RIG ET LE RTL, ET LA DÉCISION SE MESURE |
| 14:44 | `a0d7fa3b` | P1 — LA DISPERSION GPU BAT LA PROJECTION FPGA : 29,37 G ÉV/S SUR UNE CARTE CONTRE 19,3 G PROJETÉS POUR QUATRE — LE DÉBIT NE JUSTIFIE PAS LE RING |
| 15:20 | `6d720eaa` | TESTS — LA SUITE RUST PASSE À 139/139 : NATIVE_PROFONDEUR ET POS_DESYNC ENFIN DÉCLARÉES |

## Le récit de la journée (écrit à la main)

<!-- notes -->

<!-- /notes -->
