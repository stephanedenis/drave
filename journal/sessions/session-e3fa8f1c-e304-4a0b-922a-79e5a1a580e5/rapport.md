# Session session- — Rapport de mesure page S en lecture seule

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-e3fa8f1c-e304-4a0b-922a-79e5a1a580e5` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 12:27 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 88 |
| Appels d'outils | 97 |
| Fichiers touchés | 2 |
| Commandes | 84 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche X1 (J4 après-midi, la part du pilote) : mesure la page `/` de S **en lecture seule** — lis les données du sous-module (`tools/structures/`) et la fiche `reports/rapport-coordination-s-v2.md` ; compare **`/` (le banc ancien : 369 candidats, 0 verdict)** et **la v7 (359 candidats, 99 verdicts)** : la couverture, les verdicts, les référents (14 occurrences / 12 formes), les 106 conservés / 41 e … [172 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche X1 (J4 après-midi, la part du pilote) : mesure la page `/` de S **en lecture seule** — lis les données du sous-mod … [452 caractères tronqués]

*97 appels d'outils.* Actions notables :

- bash — List repo root and structures submodule
- bash — List reports and check target report
- read
- bash — List data dir and README size
- bash — Check submodule state and parent branch
- bash — Search referent audit terms in reports
- bash — Read mesure_arbre.py
- bash — Read referent audit sections
- bash — List generator functions
- bash — Inspect work dirs for S outputs
- bash — Read semaine-2 pilotage doc
- bash — Inspect phrases JSON structure
- bash — Inspect validation journals
- bash — Inspect segment keys
- … et 77 autres

**Synthèse produite :**

The measurements are stable. Now I'll write the report.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/page-s-mesure/mesurer.py` | 1 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-page-s-mesure.md` | 1 | 1 |

### Commandes exécutées (échantillon)

- **T1** List repo root and structures submodule
- **T1** List reports and check target report
- **T1** List data dir and README size
- **T1** Check submodule state and parent branch
- **T1** Search referent audit terms in reports
- **T1** Read mesure_arbre.py
- **T1** Read referent audit sections
- **T1** List generator functions
- **T1** Inspect work dirs for S outputs
- **T1** Read semaine-2 pilotage doc
- **T1** Inspect phrases JSON structure
- **T1** Inspect validation journals
- **T1** Inspect segment keys
- **T1** Read server routes and defaults
- **T1** Read Segment, analyser, referents
- **T1** Read translation/referent report
- **T1** Inspect paragraphs data
- **T1** Compute old bench and verdict coverage
- **T1** Run v7 measure read-only
- **T1** Compute migration signatures 106/41
- **T1** Categorize 304/55/10 candidates
- **T1** Aggregate referent mappings
- **T1** Search mapping ratios
- **T1** Read v1 coordination referent section
- **T1** Check listening ports and server processes
- **T1** Check mtimes and clean submodule
- **T1** Read server API state methods
- **T1** Launch server on 9000 and GET routes
- **T1** Compute API measurements
- **T1** Read A2 action details
- **T1** Compute v7 coverage by depth and status
- **T1** Inspect signature collisions among judged candidates
- **T1** Test alternate signature definitions
- **T1** Compare signature conventions
- **T1** Compare quarantine sets across conventions
- **T1** Check parent working tree status
- **T1** Check tests for writes
- **T1** Compute coverage transitions and quarantine list
- **T1** Fix coverage computation
- **T1** Run 56 submodule tests
- … et 44 autres

## 4. Mesures et résultats marquants

- **T1** `candidats jugés (**35,7 %**), **0 phrase partielle**, **133 phrases sans aucun verdict**`
- **T1** `(64,3 %) ; **147/369 candidats** sont jugés (**39,8 %**). Les 7 phrases du banc sont **7/7**`
- **T1** `jugées ; les 200 phrases de littérature sont **67/200** (33,5 %).`
- **T1** `| phrases jugées en entier | **74/207** (35,7 %) |`
- **T1** `| phrases sans verdict | **133** (64,3 %) |`
- **T1** `| candidats jugés | **147/369** (39,8 %) |`
- **T1** `| lectures acceptées (dernier verdict) | **84** (73 + 11), **57,1 %** de 147 |`
- **T1** `| lectures exclues | **63**, **42,9 %** |`
- **T1** `| verdicts avec contexte | **6/147** (4,1 %) |`
- **T1** `(57,1 %, dont 73 `resolu` = 49,7 % et 11 `compatible` = 7,5 %) et **63/147** exclues (42,9 %).`
- **T1** `**La couverture est partielle et datée.** 74/207 phrases (35,7 %), 147/369 candidats (39,8 %),`
- **T1** `**Le contexte est un décor.** 141/147 verdicts finaux au niveau 0, 6 avec contexte (4,1 %). Le`
- **T1** `règles, les vagues 5 et 6 ont été écrites **après** les règles, et le corpus réel donne **65,5 %**`
- **T1** `de GN+GV sur la littérature propre contre **9,1 %** pour le mélange — et **8,5 %** sur le CEGEP`
- **T1** `| **le gold est de la même main** | 61/61, contrôles 104/106/0,10 ; corpus 65,5 % vs 9,1 % | nouvelle vague holdout, autre main, après les règles |`
- **T1** `de double-codage, pas de test-retest. Les 57,1 % de la banque et les 57,9 % des paragraphes`
- **T1** `"etat": "74/207 phrases complètes (35,7 %), 133 sans verdict, 147/369 candidats, 1 note, 1 annotateur",`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : total 240 drwxr-xr-x. 1 stephane stephane  2300 15 nov 12:20 . drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .. -rw-r--r--. 1 stephane stephane  1040 15 nov 03:23 atomes_cohortes.py -rwxr-xr-x. 1
- **T1** : kept 106 quar 41 distinct 106 old full 74 old full -> Counter({'none': 74}) v7 coverage full/part/none 0 0 207 distinct v7 judged by depth {} deep judged 0 v7 all depth Counter({2: 221, 3: 84, 1: 37, 

