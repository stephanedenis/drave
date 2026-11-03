# Session caaf3018 — Reprise du hub et passe de portes

> **Journaux :** [le jour](../../2026-11-02/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `caaf3018-e3e2-4416-8446-11f0335910aa` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-02 16:16 |
| Durée | 3.5 h |
| Tours | 3 |
| Messages | 119 |
| Appels d'outils | 148 |
| Fichiers touchés | 2 |
| Commandes | 108 |
| Sous-agents | 0 |
| Commits | 3 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu reprends le hub `536cd5d6-94ac-4057-8fe9-11709a4587c7`. Lis son plan, en-cours et  plan-travail §9. Prochaine action : la passe de portes complète  (`bash tools/toutes-les-portes.sh`, ~1 h 46, machine au repos), puis l'intégration des lignes  d'état des sessions ouvertes. Rafraîchis le heartbeat.

**Tour 2** — oui

**Tour 3** — un des gpu est libre

## 2. Déroulé, étape par étape

### Tour 1 — Tu reprends le hub `536cd5d6-94ac-4057-8fe9-11709a4587c7`. Lis son plan, en-cours et  plan-travail §9. Prochaine action  … [180 caractères tronqués]

*128 appels d'outils.* Actions notables :

- bash — List working directory and check hub directory
- bash — Find hub id references in repo
- job_kill
- bash — List pilotage dir and find hub/plan-travail files
- bash — Look for plan file and heartbeat references
- bash — Check gitmodules and repo status
- bash — Find hub session directory
- bash — Read sessions.py head
- bash — Read hub session plan
- read
- bash — List plan-travail sections
- bash — Find heartbeat mentions
- bash — Check current time and gates scripts
- bash — Read gates method doc
- … et 103 autres

**Synthèse produite :**

⏵ Bilan du cycle hub

**La passe complète n'est pas lancée — la machine n'est pas au repos, et je l'ai mesuré avant de décider.**

À 16 h 32 puis 16 h 41 :

| ressource | mesure |
|---|---|
| GPU 0 | **99 %**, 2 014 MiB — N2 `entrainer_native.py` (pas 18 900/200 000, PPL val 4,102) |
| GPU 1 | **95 %**, 1 540 MiB — `work/n2ac/entrainer_rope.py` (banc R1.1/R1.2 de N2) |
| charge | 10–24 sur 40 cœurs ; quatre sessions actives écrivent |

`portes.md` est explicite : *les portes et une mesure GPU ne cohabitent pas*. Lancer 1 h 46 de portes ici aurait mesuré la contention, pas les portes. J'ai quand même fait la **sous-passe documentaire** (8 portes, `work/portes/sous-passe-1102-16h35`) : **7/8**. La seule rouge, `porte-bloc-maths`, ne l'est que sur son critère de **coût** (×8,31 pour ×4) ; rejouée seule trois fois, elle est **verte** (×4,24 / ×2,84 / ×4,12), les 32 formules, 10 dérivées, 6 équations et 42 restitutions restant exactes. Bruit de charge, pas régression.

**Ce qui est fait et committé**

- `e420267a` — **intégration** : cinq sections d'état (deux nouvelles : N2 `0733c5bb`, S `29ad180d` ; Pensée et D/R/A passées de « en pause » à « reprises à 16 h 16 / 16 h 21 »), roadmap au réel, heartbeat rafraîchi — en-cours **1 622 mots**, **T0 3 996**.
- `e420267a` — **porte sessions réparée** : le strict sortait en 1 avec **0 erreur et 4 avertissements** (`data/` ⊃ `data/structures/`). L'imbrication d'un territoire partagé est le régime normal ; le strict ne refuse plus que les quatre classes documentées. Autotest étendu (réservation imbriquée avertie, non refusée).
- `bee2527d` — **report de la passe** avec ses mesures et la preuve du bruit.
- `9223d054` — compteurs au disque (551 fiches / 638 JSON) et heartbeat **16 h 40**.

Vérifications de clôture : revue de documentation ✅ · `en-cours` 1 622 mots ✅ · T0 3 996/4 000 ✅ · `sessions --check --strict` 0 ✅ · `verifie_journal` ✅ · `verifie_etat_a_jour --head` ✅.

**Deux points à savoir**

1. La passe complète est à relancer **dès que les deux runs N2 seront finis** (200 k pas à ~17 pas/s ≈ 3 h 20, soit vers **19 h 50**), avec `JOURNAUX=work/portes/<date>` pour des journaux durables — ceux de `/tmp` ont été effacés au reboot. Prévoir aussi que `porte-sessions` peut rougir en fin de passe sur des heartbeats périmés (1 h 46 de durée) : c'est structurel, pas une régression, et se rejoue seul.
2. **S a livré** un cycle mesuré (analyseur : types 38/39, rôles 99/100, couverture 99,6 %, 39 structures exportées, contrôl
… [360 caractères tronqués]

### Tour 2 — oui

*10 appels d'outils.* Actions notables :

- bash — Write and syntax-check the gate watcher
- bash — Arm gate watcher and full pass on free window
- job_output
- bash — List processes matching trainer pattern
- bash — Check current GPU compute apps
- bash — Identify the new GPU process
- job_kill
- bash — Rewrite watcher with GPU-process criterion and syntax-check
- bash — Arm improved gate watcher in background

**Synthèse produite :**

⏵ Passe armée — j'attends la fenêtre libre

**Oui — la passe est armée, pas encore lancée.** Le veilleur tourne (`bash-103`) : à 16 h 46, il lit `calculs_gpu=1, gpu_max=85 %, charge=26 → fenêtre 0/3`, donc il attend.

**Le critère de déclenchement** (toutes les 2 min, 3 relevés consécutifs = 6 min stables) :

- aucun calcul GPU hors `llama-server` (le serveur garde un contexte mais ne calcule pas) ;
- utilisation GPU ≤ 15 %, charge ≤ 16 ;
- plafond **6 h** (jusqu'à ~22 h 45) : au-delà, il s'arrête en le nommant plutôt que de lancer une passe bruitée.

Quand la fenêtre s'ouvre, il lance `bash tools/toutes-les-portes.sh` avec `JOURNAUX=work/portes/passe-1102-apres-n2` (journaux durables, le registre est là), puis écrit le relevé de déclenchement dans `FENETRE.txt`.

**Ce que je ferai à la notification** : lire le registre par `awk '$2 != 0'` (jamais les marqueurs), confronter aux cinq rouges tolérées (`indice`, `melange`, `homeostasie`, `reparti-moteur`, `greffe`), rejouer seule toute autre rouge — en particulier `porte-bloc-maths` si la charge n'était pas parfaitement retombée —, puis mettre à jour `references-non-regression.md`, l'état et le journal, et committer le verdict.

Deux réserves annoncées : N2 enchaîne des évaluations courtes entre ses runs, la fenêtre peut mettre du temps à se stabiliser ; et `porte-sessions` peut rougir en fin de passe sur des heartbeats périmés — c'est structurel, elle se rejoue seule. Rien d'autre ne tourne de mon côté : les budgets sont tenus (en-cours 1 622 mots, T0 3 996), la revue et le hook sont verts, et les trois commits de l'intégration sont en place.

### Tour 3 — un des gpu est libre

*10 appels d'outils.* Actions notables :

- bash — Check which GPU is free and current load
- job_output
- job_kill
- bash — Check device count handling and GPU state
- bash — Verify CUDA device mapping in venv
- bash — Prove logical cuda:0 maps to physical GPU 1
- bash — Run full gate pass on free GPU 1

**Synthèse produite :**

⏵ Passe en cours : 13 portes vertes, dont `bloc-maths` et les portes GPU

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `docs/pilotage/en-cours.md` | 0 | 12 |
| `tools/sessions.py` | 0 | 5 |

### Commandes exécutées (échantillon)

- **T1** List working directory and check hub directory
- **T1** Find hub id references in repo
- **T1** List pilotage dir and find hub/plan-travail files
- **T1** Look for plan file and heartbeat references
- **T1** Check gitmodules and repo status
- **T1** Find hub session directory
- **T1** Read sessions.py head
- **T1** Read hub session plan
- **T1** List plan-travail sections
- **T1** Find heartbeat mentions
- **T1** Check current time and gates scripts
- **T1** Read gates method doc
- **T1** Check GPU and CPU load
- **T1** Show session mandates status
- **T1** Inspect N2 training process and GPU compute apps
- **T1** List DSH session processes and git status
- **T1** Check cores, memory, N2 work dir
- **T1** Read N2 and S session plans
- **T1** Check trainer device usage and GPU state
- **T1** Read tolerated reds list
- **T1** Recheck GPU and training progress after 45s
- **T1** Read Pensée plan and D/R/A plan diff
- **T1** Inspect N2 process threads, IO, and OCR activity
- **T1** Read sessions gate and find CUDA device references
- **T1** Locate durable gate logs and last registry
- **T1** Read sessions check logic
- **T1** Check gate device usage and references
- **T1** Find git and GPU dependent gates
- **T1** Read tolerated reds header
- **T1** Check journal diff and file movement
- **T1** Find session references in roadmap
- **T1** List roadmap structure
- **T1** Apply roadmap updates with assertions
- **T1** Show exact roadmap state lines
- **T1** Apply corrected roadmap updates
- **T1** Update hub plan heartbeat and next action
- **T1** Set timestamps to real local time
- **T1** Run sessions and en-cours checks
- **T1** Run document budget and journal checks
- **T1** Inspect sessions check exit logic and rerun
- … et 68 autres

## 4. Mesures et résultats marquants

- **T1** `[still running after 60000ms; moved to background job bash-2]`
- **T1** `0, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T1** `1, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T1** `1 MiB, 0 %`
- **T1** `0, 1 MiB, 0 %`
- **T1** `1, 1 MiB, 0 %`
- **T1** `> connues**. `porte-homeostasie` (exit 2) : **environnementale** — `/tmp/n4/rang4-lora.pt` effacé`
- **T1** `> `porte-pont` **+2,81 / +25,35 %**, `porte-coupe` **+0,52 → +17,09 %**, `porte-gain` **29,0206 →`
- **T1** `- **R4.1–R4.4** : **mesurés** (R4.4 : 4/5 ≥ **90 %**) ; **typoglycémie** ×17,8 au mélange intérieur, ×62,7 tout ; fiches [`r44-scans`](../../reports/rapport-r44-scans.md), [`typoglycemie`](../../repor`
- **T1** `- **S — le banc de structures** : outil web (`tools/structures`), générateur, pragmatique (niveaux 0–4), export ; analyseur **7/7** séquences, **93,9 %** de couverture, **19 tests** ; [`analyseur`](..`
- **T1** `[still running after 60000ms; moved to background job bash-72]`
- **T1** `0, 1650 MiB, 92 %`
- **T1** `1, 1422 MiB, 84 %`
- **T1** `6. coût        : ×8.31 de temps pour ×4 termes (0.42 ms / 50 additions)`
- **T1** `- coût non linéaire : ×8.31 pour ×4`
- **T1** `6. coût        : ×4.24 de temps pour ×4 termes (0.67 ms / 50 additions)`
- **T1** `6. coût        : ×2.84 de temps pour ×4 termes (0.81 ms / 50 additions)`
- **T1** `6. coût        : ×4.12 de temps pour ×4 termes (0.86 ms / 50 additions)`
- **T1** `[still running after 60000ms; moved to background job bash-87]`
- **T1** `0, 1918 MiB, 90 %`
- **T1** `1, 1540 MiB, 74 %`
- **T1** `> 38/39** (97,4 %), les **rôles 99/100** (99 %), les **compléments 45/45**, et couvre`
- **T1** `> **1 156/1 161 octets** (99,6 %). L'échec est **nommé** : « La femme parle » est lu comme un`
- **T1** `| `dev` | 7 | **7/7** | 229/229 (100 %) | **22/22** | **10/10** |`
- **T1** `| `test` | 16 | **16/16** | 475/475 (100 %) | **40/40** | **19/19** |`
- **T1** `| `holdout` | 16 | **15/16** | 452/457 (98,9 %) | **37/38** | **16/16** |`
- **T1** `| **global** | **39** | **38/39** (97,4 %) | **1 156/1 161** (99,6 %) | **99/100** (99 %) | **45/45** |`
- **T1** `0, 1688 MiB, 90 %`
- **T1** `1, 1422 MiB, 95 %`
- **T1** `[still running after 60000ms; moved to background job bash-94]`
- **T1** `0, 2014 MiB, 99 %`
- **T1** `1, 1540 MiB, 95 %`
- **T2** `0, 1642 MiB, 85 %`
- **T2** `1, 2334 MiB, 98 %`
- **T3** `0, 1690 MiB, 96 %`
- **T3** `1, 122 MiB, 0 %`
- **T3** `alloue 200 Mo sur cuda:0`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 21, in <module> AssertionError: (0, '> **État au 02/11 16 h 09.** B13 est à **140/140** (gold 432') [exit code: 1]

## 6. Commits

- ÉTAT — QUATRE SESSIONS OUVERTES (N2, S, PENSÉE, D/R/A) ; HEARTBEAT 16 h 24 ; PORTE STRICTE RÉPARÉE  Le hub intègre les quatre mandats rouverts après le reboot d
- PASSE — REPORTÉE SUR MESURE (DEUX GPU À N2, CHARGE 24) ; SOUS-PASSE DOCUMENTAIRE 7/8  La passe complète n'est pas lancée : à 16 h 32, GPU 0 à 92 % (N2 200 k pas
- ÉTAT — COMPTEURS AU DISQUE (551 FICHES / 638 JSON) ; HEARTBEAT 16 h 40  Les quatre sessions actives écrivent : les compteurs bougent sous le hub. Mis à jour sur

