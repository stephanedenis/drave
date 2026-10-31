# Session 0b69f616 — Continue AI coding session

> **Journaux :** [le jour](../../2026-10-30/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `0b69f616-5c75-4c34-b97a-ae05564812af` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-30 21:46 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 180 |
| Appels d'outils | 200 |
| Fichiers touchés | 6 |
| Commandes | 177 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — continue

## 2. Déroulé, étape par étape

### Tour 1 — continue

*200 appels d'outils.* Actions notables :

- get_goal
- bash — Show git status and recent commits
- bash — Check state file sizes and date
- read
- bash — Inspect uncommitted changes
- bash — Read roadmap head
- bash — Check sessions status and recent journal files
- bash — List recent reports and roadmap R13 lines
- bash — Inspect journal diffs
- bash — History of deleted files and last commit
- bash — Inspect worktree vs index diffs
- bash — Show staged changes summary
- bash — Check running processes and reflog
- bash — Detailed status and docwatch submodule state
- … et 176 autres

**Synthèse produite :**

⏵ Stabilisation du dépôt : état de l'index, hook, puis chantiers restants

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `tools/routeur.py` | 0 | 3 |
| `reports/rapport-r07-routeur.md` | 0 | 4 |
| `reports/rapport-r13-decision.md` | 1 | 0 |
| `docs/implantation/tokenisation.md` | 1 | 0 |
| `journal/sessions/0b69f616/plan.md` | 1 | 0 |
| `docs/pilotage/en-cours.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Show git status and recent commits
- **T1** Check state file sizes and date
- **T1** Inspect uncommitted changes
- **T1** Read roadmap head
- **T1** Check sessions status and recent journal files
- **T1** List recent reports and roadmap R13 lines
- **T1** Inspect journal diffs
- **T1** History of deleted files and last commit
- **T1** Inspect worktree vs index diffs
- **T1** Show staged changes summary
- **T1** Check running processes and reflog
- **T1** Detailed status and docwatch submodule state
- **T1** Check commit time and journal tooling
- **T1** Find journal index generator
- **T1** Inspect journal_auto git behaviour
- **T1** Read pre-commit hook
- **T1** Read roadmap tail (never-wait queue)
- **T1** Reset index to HEAD and inspect clean status
- **T1** Inspect untracked bloc JSONs
- **T1** Read roadmap R section
- **T1** Grep R4/R13 roadmap rows
- **T1** Find references to untracked evidence files
- **T1** Check bloc scripts output naming
- **T1** List R4 reports and index mentions
- **T1** Verify junk filenames and content duplication
- **T1** Compare JSON top-level keys
- **T1** Diff junk vs canonical JSON
- **T1** List R0/R13 fiches and read R13.4
- **T1** Check backlog entries for R13/R0.4/R0.5
- **T1** Check tracked R0.4 files and v4 content
- **T1** Read sessions manifest
- **T1** Check GPU and training processes
- **T1** Read session plans
- **T1** Locate router artifacts
- **T1** Find router report text
- **T1** Read router report
- **T1** Read survol report
- **T1** Dump router JSON structure
- **T1** Inspect router transfers
- **T1** Inspect R0.4 v4 JSON
- … et 137 autres

## 4. Mesures et résultats marquants

- **T1** `21a361f9 R13.4 — DEUX GRAINES : BPE512 DANS LE BRUIT, BPE1024 PERD 4,09 %`
- **T1** `277103ff A8.3d — LE LOT N'EST PAS LES THREADS : L'ÉCART DE 1,90 % SURVIT À 1 THREAD`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** (tête de survol) est un **pilote négatif**`
- **T1** `611 ms. La restitution depuis un document lu est **R31**.`
- **T1** `suivante, jamais l'attente. **N5 est gelé** jusqu'au verdict de R11 sur le contexte ; B10.3 attend un **z qui porte** : l'objectif mot a levé le décodeur (32,5 ; **26,7 sur JW, au-dessus du plancher 1`
- **T1** `[A1–A8] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[A8.0/A8.3a] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[A8.3b/c] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[A2.6] lasts 2 days and is 30% complete and is colored in #b26a00`
- **T1** `[B1–B12] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[B10.2bis] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[B10.3] lasts 2 days and is 15% complete and is colored in #b03a2e`
- **T1** `[B11.10] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[R0.1–R0.3] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[R4.1–R4.3] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[R0.5] lasts 2 days and is 60% complete and is colored in #b26a00`
- **T1** `[N0/N1] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `[N2] lasts 4 days and is 30% complete and is colored in #b26a00`
- **T1** `| **A2** | placer sur une machine : KV paginé, GPU, top-k, ordonnanceur | ✅ / ⚠️ | **partielle** — tête 4 bits refusée (+10 % PPL), experts bloqués par **A6.2** ; [`bilan`](../../reports/rapport-a26-b`
- **T1** `| **A5** | formats, matériels, énergie : SIMD, PTX, FPGA, KV | ✅ / 🧱 | **A5.4 bloqué** (FPGA) ; le 8 bits tardif est gratuit (+0,03 %) |`
- **T1** `+| 20:20 | `a1aae534` | A8.3c — LE LOT N'EST PAS NEUTRE (1,90 %) : LA NON-MONOTONIE DU KV ÉTAIT UN EFFET DE CHEMIN |`
- **T1** `+| 20:46 | `51a3dc91` | N3.2b2 — LE SAUT DE CALCUL N'EST PAS GRATUIT : 5,2 → 2,0 MS, SORTIE DIFFÉRENTE ; PORTE 66 |`
- **T1** `+| 22:41 | `0668ef4e` | R13.1 — LE BPE NATIF BAT L'OCTET : 3,249 CONTRE 3,689 BITS/OCTET, −11,9 % À OCTETS ÉGAUX |`
- **T1** `+| 22:56 | `2a653d12` | R13.1 — CORRECTION D'AUDIT : 11,0 % BITS/OCTET EXACT (VAL), PAS 11,9 % |`
- **T1** `c766ef93 R13.3 — ANGLAIS 100 MO : LE BPE PERD 4,2/6,6 % À OCTETS ÉGAUX`
- **T1** `21a361f9 HEAD@{2}: commit: R13.4 — DEUX GRAINES : BPE512 DANS LE BRUIT, BPE1024 PERD 4,09 %`
- **T1** `277103ff HEAD@{5}: commit: A8.3d — LE LOT N'EST PAS LES THREADS : L'ÉCART DE 1,90 % SURVIT À 1 THREAD`
- **T1** `pour 11,47 M ; la capacité à budget égal donne **−8,1 %**, mais le prior domine. La structure d'abord.`
- **T1** `- **R0** : un contrôleur **classique** + un modèle externe atteint-il **90 %** de la compréhension à **30 %** du`
- **T1** `| **R0.2** | **contrôleur de lecture** : `survol`, `balayage`, `lecture`, `relecture`, `arrêt` ; budget en octets ; classique d'abord (TOC, titres, premières/dernières phrases, BM25/regex) | ✅ **1,000`
- **T1** `| **R0.3** | **banc de lecture rapide** : 30 documents, 5 types, 10 questions/spans gold, modes intégral/écrémage/balayage/sélectif, contrôles closed-book, régions aléatoires, sections mélangées | ✅ *`
- **T1** `| **R3.1** | **SFT de lecture** : réponse, résumé, extraction, refus ; jeux tenus à l'écart | ⏳ | **≥ 80 %** des instructions tenues à l'écart ; le contrôle 24/24 vus ne compte pas |`
- **T1** `79:[R4.1–R4.3] lasts 1 day and is 100% complete and is colored in #2e7d32`
- **T1** `> égaux** — sur deux graines, BPE 512 est à **+0,39 %** (dans le bruit : +0,67 % puis +0,10 %)`
- **T1** `> et BPE 1024 à **+4,09 %** contre bytes. Le signe négatif est stable ; l’ampleur du 512 ne l’est pas.`
- **T1** `| BPE 512 | 1,8142 | 1,8000 | **1,8071** | **+0,39 %** |`
- **T1** `| BPE 1024 | 1,8726 | 1,8750 | **1,8738** | **+4,09 %** |`
- **T1** `- **BPE 512** : +0,67 % à la graine 1, +0,10 % à la graine 2 ; la moyenne est positive mais`
- **T1** `l’écart entre graines (0,78 %) est plus grand que l’effet.`
- **T1** `- **BPE 1024** : +3,91 % et +4,27 % ; l’effet est stable et clairement négatif.`
- **T1** `- **Bytes** : 1,8021 / 1,7982 ; le bruit de graine est de **0,21 %**.`
- **T1** `| `04ed1834` | 2026-10-08 09:21 | 0.3 Mo | 67 Ko | 1 | 27 | 42 | 0 | 0 |`
- **T1** `| `11b2d312` | 2026-10-01 02:56 | 0.5 Mo | 82 Ko | 1 | 42 | 60 | 0 | 0 |`
- **T1** `| `13446299` | 2026-10-01 01:07 | 0.5 Mo | 84 Ko | 1 | 50 | 68 | 0 | 0 |`
- **T1** `| `15fd322f` | 2026-09-30 12:00 | 0.6 Mo | 66 Ko | 1 | 57 | 67 | 0 | 0 |`
- **T1** `| `1820cf6b` | 2026-10-02 19:36 | 0.3 Mo | 30 Ko | 1 | 23 | 21 | 0 | 0 |`
- **T1** `| `18b8879c` | 2026-10-02 15:12 | 0.4 Mo | 78 Ko | 1 | 33 | 55 | 3 | 0 |`
- **T1** `| `18c3f6d0` | 2026-10-01 05:26 | 0.3 Mo | 51 Ko | 1 | 26 | 38 | 0 | 0 |`
- **T1** `| `1966e052` | 2026-10-08 09:20 | 0.3 Mo | 57 Ko | 1 | 22 | 33 | 0 | 0 |`
- **T1** `| `22bcae27` | 2026-09-28 14:45 | 14.8 Mo | 1398 Ko | 54 | 1250 | 1227 | 19 | 4 |`
- **T1** `| `27c99b10` | 2026-09-25 19:50 | 1.0 Mo | 61 Ko | 1 | 57 | 54 | 1 | 0 |`
- **T1** `| `2c2a6595` | 2026-10-02 15:11 | 0.4 Mo | 66 Ko | 1 | 29 | 44 | 0 | 0 |`
- **T1** `| `31f26a6e` | 2026-10-02 19:48 | 0.9 Mo | 171 Ko | 1 | 85 | 111 | 0 | 0 |`
- **T1** `| `34e1d4be` | 2026-10-02 10:00 | 0.6 Mo | 105 Ko | 1 | 38 | 53 | 0 | 0 |`
- **T1** `| `3d5618a0` | 2026-10-02 15:18 | 1.1 Mo | 387 Ko | 1 | 73 | 85 | 1 | 0 |`
- **T1** `| `42059fde` | 2026-09-30 12:32 | 1.0 Mo | 158 Ko | 1 | 112 | 157 | 1 | 0 |`
- **T1** `| `482522d1` | 2026-10-08 09:23 | 0.5 Mo | 138 Ko | 1 | 54 | 58 | 0 | 0 |`
- **T1** `| `48ec07ab` | 2026-10-08 09:23 | 0.5 Mo | 121 Ko | 1 | 50 | 62 | 0 | 0 |`
- **T1** `| `4b146dfd` | 2026-10-02 09:57 | 0.4 Mo | 47 Ko | 1 | 18 | 23 | 0 | 0 |`
- **T1** `| `4d7a793b` | 2026-09-30 23:15 | 0.7 Mo | 93 Ko | 1 | 43 | 63 | 0 | 0 |`
- **T1** `| `4e786d3f` | 2026-10-02 10:18 | 0.8 Mo | 178 Ko | 1 | 80 | 129 | 0 | 0 |`
- **T1** `| `5185ccb1` | 2026-09-30 17:27 | 1.2 Mo | 158 Ko | 1 | 102 | 123 | 0 | 0 |`
- **T1** `| `564fbe3a` | 2026-09-30 18:14 | 0.7 Mo | 60 Ko | 1 | 25 | 35 | 0 | 0 |`
- **T1** `| `56879594` | 2026-10-02 15:10 | 0.5 Mo | 137 Ko | 1 | 17 | 29 | 0 | 0 |`
- **T1** `| `5c1bbea7` | 2026-10-02 10:01 | 0.6 Mo | 88 Ko | 1 | 43 | 52 | 0 | 0 |`
- **T1** `| `5ce3f080` | 2026-09-30 15:50 | 0.9 Mo | 101 Ko | 1 | 70 | 77 | 0 | 0 |`
- **T1** `| `6551e4dc` | 2026-10-01 12:04 | 0.6 Mo | 87 Ko | 1 | 50 | 63 | 0 | 0 |`
- **T1** `| `67637ea9` | 2026-10-08 09:20 | 0.2 Mo | 45 Ko | 1 | 19 | 28 | 0 | 0 |`
- **T1** `| `6d0c1d28` | 2026-09-30 20:11 | 0.6 Mo | 58 Ko | 1 | 31 | 36 | 0 | 0 |`
- **T1** `| `7c876089` | 2026-09-30 13:26 | 0.6 Mo | 93 Ko | 1 | 45 | 62 | 0 | 0 |`
- **T1** `| `7d0d2578` | 2026-09-30 11:53 | 0.6 Mo | 68 Ko | 1 | 41 | 53 | 0 | 0 |`
- **T1** `| `7f3f463f` | 2026-10-02 19:34 | 0.2 Mo | 45 Ko | 1 | 21 | 28 | 0 | 0 |`
- **T1** `| `8288d350` | 2026-10-01 05:57 | 0.4 Mo | 75 Ko | 1 | 33 | 51 | 1 | 0 |`
- **T1** `| `850eebf1` | 2026-10-08 09:21 | 0.4 Mo | 95 Ko | 1 | 35 | 60 | 0 | 0 |`
- **T1** `| `8549abcb` | 2026-10-02 15:11 | 0.6 Mo | 124 Ko | 1 | 20 | 28 | 0 | 0 |`
- **T1** `| `8734fc13` | 2026-10-02 18:24 | 1.1 Mo | 158 Ko | 1 | 96 | 108 | 0 | 0 |`
- **T1** `| `8a0aa6e5` | 2026-10-01 11:26 | 0.5 Mo | 91 Ko | 1 | 47 | 66 | 0 | 0 |`
- **T1** `| `8b315bb2` | 2026-10-02 09:57 | 0.4 Mo | 61 Ko | 1 | 23 | 30 | 0 | 0 |`
- **T1** `| `8b6d46ab` | 2026-10-02 08:55 | 0.9 Mo | 163 Ko | 1 | 100 | 155 | 3 | 0 |`
- **T1** `| `8e04c99a` | 2026-09-30 18:17 | 0.7 Mo | 118 Ko | 1 | 59 | 85 | 0 | 0 |`
- **T1** `| `a4277668` | 2026-10-08 09:21 | 0.2 Mo | 68 Ko | 1 | 24 | 54 | 0 | 0 |`
- **T1** `| `a4eaa4c8` | 2026-10-08 09:21 | 0.3 Mo | 60 Ko | 1 | 28 | 38 | 0 | 0 |`
- **T1** `| `a9e308b7` | 2026-10-08 09:22 | 0.3 Mo | 44 Ko | 1 | 20 | 20 | 0 | 0 |`
- **T1** `| `aa5f9fc5` | 2026-09-30 15:17 | 0.8 Mo | 129 Ko | 1 | 78 | 100 | 0 | 0 |`
- **T1** `| `b13a6032` | 2026-10-02 15:09 | 0.3 Mo | 88 Ko | 1 | 17 | 43 | 0 | 0 |`
- **T1** `| `bbc0b8e2` | 2026-10-12 08:59 | 0.6 Mo | 62 Ko | 2 | 38 | 52 | 0 | 0 |`
- **T1** `| `bbd6969f` | 2026-10-07 21:14 | 56.9 Mo | 9009 Ko | 205 | 9630 | 9050 | 63 | 26 |`
- **T1** `| `bcfe0b97` | 2026-09-30 12:39 | 1.0 Mo | 145 Ko | 1 | 102 | 110 | 0 | 0 |`
- **T1** `| `c25f97d1` | 2026-09-30 11:59 | 0.8 Mo | 126 Ko | 1 | 73 | 104 | 0 | 0 |`
- **T1** `| `c776b71f` | 2026-09-30 18:43 | 0.7 Mo | 82 Ko | 1 | 35 | 54 | 0 | 0 |`
- **T1** `| `d04ed7a2` | 2026-10-08 09:23 | 0.5 Mo | 105 Ko | 1 | 43 | 60 | 0 | 0 |`
- **T1** `| `d31b3d9b` | 2026-10-11 08:14 | 25.1 Mo | 3236 Ko | 104 | 3396 | 3157 | 31 | 8 |`
- **T1** `| `da69b1fa` | 2026-09-30 15:13 | 0.5 Mo | 56 Ko | 1 | 37 | 45 | 0 | 0 |`
- **T1** `| `dcaa24d6` | 2026-10-02 15:06 | 0.2 Mo | 39 Ko | 1 | 11 | 13 | 0 | 0 |`
- **T1** `| `e14c26ae` | 2026-10-02 21:25 | 0.7 Mo | 109 Ko | 1 | 49 | 76 | 0 | 0 |`
- **T1** `| `e7dfe34f` | 2026-09-28 14:59 | 0.2 Mo | 28 Ko | 1 | 20 | 21 | 0 | 0 |`
- **T1** `| `ee19a880` | 2026-10-08 09:22 | 0.4 Mo | 89 Ko | 1 | 30 | 43 | 0 | 0 |`
- **T1** `| `f2de810a` | 2026-10-02 15:15 | 0.7 Mo | 315 Ko | 1 | 56 | 63 | 0 | 0 |`
- **T1** `| `f3ca67c4` | 2026-10-08 09:21 | 0.3 Mo | 61 Ko | 1 | 26 | 46 | 0 | 0 |`
- **T1** `| `fba448b3` | 2026-10-02 15:10 | 0.5 Mo | 39 Ko | 1 | 19 | 26 | 0 | 0 |`
- **T1** `| `ff364db0` | 2026-10-01 05:58 | 0.5 Mo | 120 Ko | 1 | 63 | 75 | 0 | 0 |`
- **T1** `Total : 129.1 Mo de traces brutes.`
- **T1** `0, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T1** `1, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T1** `reports/rapport-a83c-lot.md:61:  coupe et du routeur ; il peut être plus petit ailleurs (0,15 % sur le 30B).`
- **T1** `reports/rapport-design-H-carte-sorties.md:12:> (3) un routeur **réel** (seuil de confiance) n'atteint la parité qu'à la sortie **22** : 4,7 % des`
- **T1** `reports/rapport-design-H-profondeur-routee.md:13:> 31 % des jetons) — et il faudrait un routeur **parfait** ;`
- **T1** `Avec le banc élargi (84 questions × 6 paires = 504, 498 après écart d'un gold déplacé), la tête`
- **T1** `**Ce que ça dit** : la donnée est bien le facteur limitant (×5,5 de paires → +13 points d'AUC),`
- **T1** `> porte 1 est franchie sur le lexical** (rappel@10 **0,984** ≥ 0,95) à **0,1 ms par requête** ;`
- **T1** `| lexical (249 questions) | 249 | **0,984** | 0,1 ms |`
- **T1** `| paraphrases (84 questions) | 84 | **0,702** | 0,1 ms |`
- **T1** `document, le span qui porte la valeur est dans les dix premiers, en 0,1 ms. **Il ne suffit pas`
- **T1** `1. **Le balayage classique est acquis** : offsets exacts, rejeu, 0,1 ms. Il peut devenir une`
- **T1** `| **span** (top-1) | **0,944** | 0,405 | 3/20 | 0,1 ms |`
- **T1** `| extractif | 0,851 | 0,286 | **12/20** | ~1 ms |`
- **T1** `| **A8** | l'ordonnanceur place **et** perte : `choisir_avec_perte` | ✅ **opt-in** ; 6 portes épinglées, A8.3 **échoue** (−5,9 % … +19,5 %) | **A8.3c/d** : le lot change la PPL, pas les threads ; rédu`
- **T1** `| **B5** | la sémantique des jeux : contrat RSN-jeu, cinq niveaux, bruit | ✅ | aucune — 112 items, **100 %** au niveau 4 |`
- **T1** `| **B6** | la logique dans la pensée : règles, recherche, cartes, invariance | ✅ | aucune — perft, **3/3** mats, dames **20/20**, cartes **79,7 %** |`
- **T1** `| **B8** | les maîtres : 17 principes, 9 sources, livre, parties | ✅ | aucune — livre **10/10**, go 9×9 **10/10** contre 3/10, cartes **44,7 %** |`
- … (tronqué)

## 5. Erreurs rencontrées

5 sorties en erreur ou divergentes. Les premières :

- **T1** : 981e4bbf CORPUS GELÉ — LA DÉRIVE DES BANCS EST CLOSE : 30 DOCUMENTS, MANIFESTE SHA256, 0 PROBLÈME === commit body === 981e4bbf706103f231a00c6eca0fffd15525fad0 CORPUS GELÉ — LA DÉRIVE DES BANCS EST CLO
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 3, in <module> TypeError: unhashable type: 'dict' [exit code: 1]
- **T1** : tools/porte-etat.sh --- [exit code: 1]
- **T1** : === PASSE COMPLÈTE DES PORTES (78 portes, borne 1800 s) ===     journaux : /tmp/portes-cloture-2156 --- 0 [exit code: 1]
- **T1** : M journal/2026-10-30/README.md  M journal/2026-10-30/docs.md  M journal/sessions/8156fdcb/plan.md  M journal/sessions/N2-GPU/plan.md  M journal/sessions/c3d0f0bd/plan.md ?? journal/sessions/0b69f616/ 

