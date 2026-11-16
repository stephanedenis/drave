# Session session- — Passe complète des portes et rapport

> **Journaux :** [le jour](../../2026-11-16/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-e466b49c-4fcb-4b34-b5a8-5bc193487415` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-16 04:11 |
| Durée | 1.0 h |
| Tours | 1 |
| Messages | 35 |
| Appels d'outils | 44 |
| Fichiers touchés | 0 |
| Commandes | 34 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche Z2 (clôture technique) : la **passe complète** — `bash tools/toutes-les-portes.sh` avec `JOURNAUX=work/portes/passe-1611` ; lis le registre par `awk '$2 != 0'` (jamais par un tail) ; note les rouges, compare aux **rouges tolérées** de `docs/pilotage/references-non-regression.md`, mets à jour la section « passe » du document, et écris `reports/rapport-passe-1611.md` + JSON (portes, vertes, ro … [16 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche Z2 (clôture technique) : la **passe complète** — `bash tools/toutes-les-portes.sh` avec `JOURNAUX=work/portes/pass … [296 caractères tronqués]

*44 appels d'outils.* Actions notables :

- bash — Inspect workspace structure
- read
- bash — Inspect the gates launcher script
- bash — List previous gate run dirs and reports
- bash — Inspect latest pass dir and registry format
- bash — Find Z2 references and current state
- bash — Read prior pass report format
- bash — Check date, git, GPU and load
- bash — Read the Z session plan
- bash — Count gates and check resources gate
- bash — Check for a running pass
- bash — Run the complete gates pass
- bash — Read example result JSON files
- bash — Read modern pass report and verification registry
- … et 18 autres

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Inspect workspace structure
- **T1** Inspect the gates launcher script
- **T1** List previous gate run dirs and reports
- **T1** Inspect latest pass dir and registry format
- **T1** Find Z2 references and current state
- **T1** Read prior pass report format
- **T1** Check date, git, GPU and load
- **T1** Read the Z session plan
- **T1** Count gates and check resources gate
- **T1** Check for a running pass
- **T1** Run the complete gates pass
- **T1** Read example result JSON files
- **T1** Read modern pass report and verification registry
- **T1** Inspect modified chantier plan
- **T1** Read session rapport and digest around Z2
- **T1** See how prior pass updated the reference doc
- **T1** Check acceptance string and pass progress
- **T1** Check pass directory progress
- **T1** Read prior red gate failure reasons
- **T1** Check pass progress by registry count
- **T1** Check whether the pass process is alive
- **T1** Inspect journal day structure
- **T1** Inspect roadmap and state pass references
- **T1** Read documentation review checks
- **T1** Read state and size validators
- **T1** Read rest of documentation review
- **T1** Read tableaux gate
- **T1** Verify counters against disk
- **T1** Check pass progress after wait
- **T1** Check pass progress
- **T1** Check pass progress
- **T1** Check pass progress
- **T1** Check pass progress
- **T1** Check pass progress

## 4. Mesures et résultats marquants

- **T1** `snov2mZ/qTiDmwihsIlntN/8yFnTmERH9sdx2tbp49DkD3wlanP16g0qFGo5tC96oCyVCUZQ7jiHY280Xnd4touHx6mES51eAGnSI0JHVeDwbKzRDGaEQT6P3aLj5So32u1heV74Xik8snB0rpCxApGX2xBWV8OpVO10tZQ2ST9UdjJmy22u2ku8I5h8HDnYasa6Cjuq`
- **T1** `l edge-pattern-solid flowchart-link" style="stroke-dasharray: 0 0 393.2394714355469 4; stroke-dashoffset: 0;;" data-edge="true" data-et="edge" data-id="L_B_C_0" data-points="W3sieCI6MzM3LjI0OTk4MDkyNj`
- **T1** `journal/sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/rapport.md:142:- **T1** `FUZZ2 (20015 cas, alphabet avec marques combinantes) : 5274 divergences (26.4%)``
- **T1** `journal/sessions/27c99b10-c57e-4599-a23a-f7b1a54c17a1/digest.md:681:FUZZ2 (20015 cas, alphabet avec marques combinantes) : 5274 divergences (26.4%)`
- **T1** `- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.`
- **T1** `| `porte-coupe.sh` | 132 s | ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit |`
- **T1** `| `porte-delais.sh` | 21 s | ✅ le temps, lui, augmente : 6.79 s → 9.45 s (+2.7 s ≈ 50 ms × 64 pas) |`
- **T1** `| `porte-mistral.sh` | 10 s | ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= p |`
- **T1** `| `porte-pont.sh` | 89 s | ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux |`
- **T1** `| `porte-reflexe.sh` | 102 s | ✅ le gain de temps est réel : 5.9 ms par jeton à 1 couche(s) contre 126.8 ms à 24 — 21.5× plus |`
- **T1** `| `porte-reparti-moteur.sh` | 1 s | PORTE TENUE : le découpage ne change pas la perplexité (écart relatif 0.0000 %) |`
- **T1** `désormais la bonne conclusion (25,4 % contre 4,8 %).`
- **T1** `| `porte-coupe.sh` | 121 s | ✅ le coût du pont va de +0.52 % (coupe 18/24) à +17.09 % (coupe 15/24) — il y a un bon endroit |`
- **T1** `| `porte-delais.sh` | 19 s | ✅ le temps, lui, augmente : 5.80 s → 9.13 s (+3.3 s ≈ 50 ms × 64 pas) |`
- **T1** `| `porte-mistral.sh` | 8 s | ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= p |`
- **T1** `| `porte-pont.sh` | 74 s | ✅ 448 fibres : +2.81 % · 392 fibres : +25.35 % — la marche est entre les deux |`
- **T1** `| `porte-reflexe.sh` | 101 s | ✅ l'état de 16 couches CONTIENT le prochain jeton : 25.4 % contre 4.8 % pour la classe majorit |`
- **T1** `état n'est valide qu'à sa position — ×633 pour un pas — et manquer coûte ×1,06 contre ×633 pour`
- **T1** `0, 154 MiB, 16384 MiB, 1 %`
- **T1** `1, 4 MiB, 16384 MiB, 0 %`
- **T1** `> chaud — quatre fois plus — et réduire de 25 % les experts lus ne change rien.`
- **T1** `> Hypothèse non mesurée : la dispersion (~144 lectures par couple × ~10 ms de`
- **T1** `La réponse est **le disque**, et elle est exacte à 0,1 % près. La sonde est`
- **T1** `10,9 To**. Le NVMe de 931 Go est ailleurs, et **occupé 0,7 % du temps**.`
- **T1** `| état de `/proc/PID/stat` | 66,2 % en « S » (sommeil) | c'est le fil **principal** ; il dort pendant que ses ouvriers travaillent — il a fallu un second observateur qui agrège `/proc/PID/task/*/stat``
- **T1** `| CPU travaillé (utime+stime) | **333 s — 21,0 %** |`
- **T1** `| échantillons en état D (E/S) | 18,0 % |`
- **T1** `| échantillons en état R (travail) | 15,8 % |`
- **T1** `| échantillons en état S (sommeil) | 66,2 % |`
- **T1** `| débit de lecture effectif | **130 Mo/s** (468,6 Go/h) |`
- **T1** `| **`dm-1` (donc `sda`) occupé** | **1 390 s — 87,6 %** |`
- **T1** `| `nvme0n1` occupé | **0,7 %** |`
- **T1** `+   "mandat": "Tâche Z3 (le bilan pour l'humain) : un **bilan court** (le matin) — `reports/rapport-bilan-final.md` + JSON : ce qui est installable (les 3 voies : editable, roue, le chemin historique)`
- **T1** `| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO |`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `/paragraphes`** (11 accepté`
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 15/11 (nuit).** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **F1 0,7902**, `
- **T1** `**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (hasard`

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : -rwxr-xr-x. 1 stephane stephane 4422  2 nov 15:55 tools/toutes-les-portes.sh #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 1
- **T1** : digest.md rapport.md session.v4.jsonl.zstd ---plan--- [exit code: 2]
- **T1** : absent (attendu) ---registre count--- ---rouges--- [exit code: 2]

