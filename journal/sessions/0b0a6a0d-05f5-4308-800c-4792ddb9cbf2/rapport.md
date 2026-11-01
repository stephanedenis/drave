# Session 0b0a6a0d — Continue session work

> **Journaux :** [le jour](../../2026-10-31/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-31 17:17 |
| Durée | 5.4 h |
| Tours | 4 |
| Messages | 356 |
| Appels d'outils | 350 |
| Fichiers touchés | 11 |
| Commandes | 288 |
| Sous-agents | 0 |
| Commits | 4 |
| Compactages de contexte | 0 |

## Objectifs déclarés

- **create** — N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / 20 000 pas, 4 sources contre français seul, puis curriculum 129), avec contrôle négatif et trois graines ; écrire la fiche dans reports/, le récit dans journal/, committer avec le chiffre et mettre docs/p
… [41 caractères tronqués]
- **complete** — N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / 20 000 pas, 4 sources contre français seul, puis curriculum 129), avec contrôle négatif et trois graines ; écrire la fiche dans reports/, le récit dans journal/, committer avec le chiffre et mettre docs/p
… [41 caractères tronqués]
- **create** — N2.h — le mètre propre : construire un corpus dédupliqué avec split train/val/test sans répétition (outil versionné + manifeste + vérification), refaire toute la chaîne sur ce corpus (professeur 23,5 M, base supervisée, distillation 20k × 3 graines, curriculum 129), mesurer la porte honnête et le pr
… [344 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — continue

**Tour 2** — <goal_round> Objective: "N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / 20 000 pas, 4 sources contre français seul, puis curriculum 129), avec contrôle négatif et trois graines ; écrire la fiche dans reports/, le récit dans journal/, committer avec le chiffre et mettre docs/pilotage/en-cours.md et la roadmap à jour." Round: 1/1000  Continue working  … [511 caractères tronqués]

**Tour 3** — je te donnes 10h de liberté totale. impressionne-moi. je serai décu si tu as terminé à temps.

**Tour 4** — en-cours.md doit contenir pour chaque session tout ton plan, ambition et stratégie et objectif final. Continue ton bon travail en maintenant ce document à jour pour que les autres sessions locales puissent être en synergie avec tes travaux.

## 2. Déroulé, étape par étape

### Tour 1 — continue

*96 appels d'outils.* Actions notables :

- get_goal
- bash — Show git status and recent commits
- bash — Check state file sizes and recent journal
- read
- bash — Inspect uncommitted changes
- bash — Check session status
- bash — Check today's journal files
- bash — Find N2 section in roadmap
- bash — Read roadmap N2 details
- bash — List N2 reports and tooling
- bash — Find curriculum references and distiller scripts
- bash — Check GPU availability
- bash — Read R12 curriculum backlog card
- bash — Read distillation script header
- … et 79 autres

**Synthèse produite :**

⏵ Réponse sur l'état et la carte des conflits

**Non, il ne l'était pas** — la page datait de 17 h 15 et disait encore « aucune session active ». C'est corrigé, validé et committé : `54dc7a26`. `tools/sessions.py --status` me voit maintenant « en cours ».

**Ce que l'autre session lira dans `en-cours`**

- Session active `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2`, rôle **N2 — le budget complet** (campagne GPU en cours : français seul, manifeste 4 sources, quotas égaux, curriculum 129 ; 3 graines).
- Fichiers réservés : `work/n2d/`, `tools/distiller_budget.py`, `reports/n2-*`, `journal/sessions/0b0a6a0d-…/`.

**Ce qu'elle peut prendre sans collision**

- La documentation, le backlog, **N4** (consigne courte, sans GPU), et les portes **documentaires** (`PORTES="..."`).
- Tout ce qui ne touche ni mes fichiers réservés ni les GPU.

**Ce qu'elle ne doit pas prendre (conflits réels, pas théoriques)**

- `bash tools/toutes-les-portes.sh` : la passe complète utilise les **deux cartes** et fausserait mes mesures (c'est écrit dans `docs/methode/portes.md` : portes et mesure GPU ne cohabitent pas). Je la lancerai moi-même à la fin, seule.
- Un entraînement GPU, pour la même raison.
- `docs/pilotage/en-cours.md` : **une session écrit à la fois**. Si elle doit y mettre un fait, qu'elle me le dise — je libère la page.
- La `roadmap` et `reports/n2-*` : je les édite à la clôture.

**Horaires** : la campagne tourne jusqu'à ~19 h 40 (6 runs restants), puis agrégation, fiche, et passe complète des portes (1 h 30–2 h) avant le commit de clôture. Si elle a besoin d'un GPU avant, elle me le dit et je réordonne.

Au passage : `work/` est désormais dans `.gitignore` — sinon un `git add -A` aurait stagé 1–2 Go de points de contrôle. `tools/docwatch` reste modifié en local (sous-module, pas à moi).

### Tour 2 — <goal_round> Objective: "N2 — mesurer le curriculum et les données sur le dispositif reconstruit (budget complet 41 Mo / … [791 caractères tronqués]

*206 appels d'outils.* Actions notables :

- bash — Check campaign status
- bash — Compute manifest source shares
- bash — Check working tree and generated journal file
- bash — Quantify the sampling-grid difference
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/evalue-final.py`
- bash — Check seed 1 completion
- bash — Check train/val overlap for contamination
- bash — Read seed 1 final results
- bash — Check run logs and processes
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/agrege.py`
- read
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/agrege.py`
- bash — Check for seed 1 final results
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/robustesse.py`
- … et 154 autres

**Synthèse produite :**

⏵ Clôture : N2.d mesuré, écrit, committé, portes vertes

\## Ce qui est établi

**La campagne N2.d** — 12 distillations, 3 graines par bras, deux GPU, ~3 h :

| bras | protocole 8×16×128 | fenêtres propres | 8×15×129 |
|---|---:|---:|---:|
| base supervisée | 3,2161 | 3,2450 | 3,2653 |
| **T5k** (5 000 pas, réf.) | 2,9355 | 3,0534 | 2,9623 |
| **A** — 20 000 pas, français seul | **2,8527** | **2,9795** | 2,8743 |
| **B** — 4 sources (82,5 % anglais) | 3,7591 | 3,8573 | 3,8218 |
| **B′** — 4 sources à quotas égaux | 3,4350 | 3,5634 | 3,4848 |
| **C** — curriculum 129 sur A | 2,8471 | 2,9783 | **2,8327** |

- **Le budget paie peu** : −0,0828, du même ordre que la chaîne historique ; la porte < 2,5 reste à 0,35 (protocole) / 0,48 (fenêtres propres).
- **Les données coûtent** : +0,91 pour le manifeste, +0,58 même à quotas égaux (professeur français sur octets anglais : confondant nommé).
- **Le curriculum 129** gagne 0,0416 à 129, 0,0056 à 128.

**Le résultat qui change la lecture** : la validation n'est **pas** tenue à l'écart. 32,8 % des fenêtres du protocole (42/128) sont **verbatim** dans l'entraînement ; 23,5 % des fenêtres d'entraînement y apparaissent plus d'une fois. Les fenêtres contaminées donnent 0,39 de PPL de moins que les propres, et l'écart croît avec le budget (0,17 → 0,35 → 0,39). **2,7078 et 2,6998 sont mesurés sur ce même jeu contaminé** : la porte < 2,5 n'a jamais été une mesure de généralisation.

\## Vérification

- Trois graines par bras, écart-type 0,002–0,008 ; comparaison appariée (mêmes fenêtres).
- Contrôles : permutation (PPL ≈ 1087), base sans distillation, distillation courte, B′ contre B, C contre A graine par graine.
- Robustesse : sur quatre grilles de fenêtres, A reste sous T5k (−0,083 à −0,118).
- **Portes** : passe complète 79 portes, **75 vertes, 4 rouges** — les quatre connues et tolérées (`porte-indice`, `porte-melange`, `porte-homéostasie`, `porte-reparti-moteur`) ; `porte-ocr` verte. Journaux `/tmp/portes-1031-n2d`, 1 h 39.
- Revue de documentation, budget de contexte, état, journal, backlog et schémas : tous verts.

\## Artefacts

- Fiche : `reports/rapport-n2-budget.md` · agrégat `reports/n2-budget.json` · récit `journal/2026-10-31/apprentissage.md`.
- Code : `tools/distiller_budget.py`, `tools/eval_n2_budget.py`.
- Points de contrôle : 542 Mo sur deux disques (`backups/n2/2026-10-31/n2d/`, `IA/artefacts/n2/2026-10-31/n2d/`).
- Commits : **`c3bcbe99`** (résultat) et `10fa4f42` (références des portes).
- État et roadmap 
… [593 caractères tronqués]

### Tour 3 — je te donnes 10h de liberté totale. impressionne-moi. je serai décu si tu as terminé à temps.

*37 appels d'outils.* Actions notables :

- bash — Determine which repo files compose the French corpus
- bash — Measure the size of duplicated passages
- bash — Check teacher time and external corpora
- bash — Extract teacher and base training durations
- bash — Read the teacher log for duration
- create_goal
- todo_write
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_propre.py`
- bash — Test dedupe on a synthetic text
- bash — Build the deduplicated corpus
- bash — Inspect clean corpus seams and trainer CLI
- bash — Check whether the teacher early-stops on validation
- bash — Check checkpoint selection in the teacher trainer
- bash — Launch teacher and base training on the clean corpus
- … et 22 autres

**Synthèse produite :**

⏵ Ajout des positions aléatoires (attaque du verrou de longueur) au modèle et au distillateur

### Tour 4 — en-cours.md doit contenir pour chaque session tout ton plan, ambition et stratégie et objectif final. Continue ton bon t … [120 caractères tronqués]

*11 appels d'outils.* Actions notables :

- bash — Check active sessions, state, and campaign
- bash — Measure the context budget headroom
- read
- bash — Rewrite the state with the full session plan
- bash — Add the Id field and restore the remaining-work section
- bash — Read the session plan file
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md`
- bash — Re-read the session plan
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md`
- bash — Write the session plan and validate
- bash — Commit the state update for other sessions

**Synthèse produite :**

⏵ Mise à jour d'`en-cours` : plan complet, ambition et stratégie de la session N2.h

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/distiller_budget.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md` | 3 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/evalue-final.py` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/agrege.py` | 3 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/robustesse.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/fiche.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_budget.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2d/journal-notes.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_propre.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/eval_n2_propre.py` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Show git status and recent commits
- **T1** Check state file sizes and recent journal
- **T1** Inspect uncommitted changes
- **T1** Check session status
- **T1** Check today's journal files
- **T1** Find N2 section in roadmap
- **T1** Read roadmap N2 details
- **T1** List N2 reports and tooling
- **T1** Find curriculum references and distiller scripts
- **T1** Check GPU availability
- **T1** Read R12 curriculum backlog card
- **T1** Read distillation script header
- **T1** Check original distillation script for curriculum
- **T1** Read original distillation report
- **T1** Locate the 2.6998 result and ctx129 report
- **T1** Find capacity result at 21.63M
- **T1** List corpus sources
- **T1** Read capacity reports
- **T1** Find 4-source distillation recipe
- **T1** Check archived checkpoints
- **T1** Read multi-source corpus report
- **T1** List archived artefacts and read backup README
- **T1** Read distillation training loop
- **T1** Inspect multi-source manifest
- **T1** Read native model config
- **T1** Read historical protocol JSON
- **T1** List native reports
- **T1** Find reports using multi corpus
- **T1** Read multi-source distillation report
- **T1** List all native PPL results sorted
- **T1** Inspect the best chain checkpoints
- **T1** Find multi-source corpus consumer
- **T1** Read native corpus builder
- **T1** Check gitignore and GPU environment
- **T1** Locate the GPU Python environment
- **T1** Verify GPU env at home
- **T1** Read campaign checkpoint notes
- **T1** Compute historical-protocol PPL for archived checkpoints
- **T1** Read model forward and VDC helpers
- **T1** Fix window shapes in campaign script
- … et 248 autres

## 4. Mesures et résultats marquants

- **T1** `4442c64c N2 — L'ÉTAT DE SECTION NE SE DISTINGUE PAS D'UN ÉTAT ÉTRANGER (+0,36 % CONTRE +0,37 %)`
- **T1** `21a361f9 R13.4 — DEUX GRAINES : BPE512 DANS LE BRUIT, BPE1024 PERD 4,09 %`
- **T1** `85:[N2] lasts 4 days and is 30% complete and is colored in #b26a00`
- **T1** `30 % sur 5 types et **249 questions**) ; **R0.4** (tête de survol) et **R0.5** (routeur) sont`
- **T1** `611 ms. La restitution depuis un document lu est **R31**.`
- **T1** `suivante, jamais l'attente. **N5 est gelé** jusqu'au verdict de R11 sur le contexte ; B10.3 attend un **z qui porte** : l'objectif mot a levé le décodeur (32,5 ; **26,7 sur JW, au-dessus du plancher 1`
- **T1** `| **N1** | `drave-n0` : 11,47 M, 6 blocs, octets, attention locale, FFN creux, 3 têtes précoces | ✅ | aucune — PPL **3,465** avec pont (**4,080** sans) ; têtes **57,6 / 61,6 / 62,1 %** contre **62,7 %`
- **T1** `2. **Le saut de calcul existe, le saut de contenu n'existe pas.** La sortie précoce gagne **24,05 %** de temps en`
- **T1** `Quadro RTX 5000, 16384 MiB, 1 MiB, 0 %`
- **T1** `/dev/mapper/system-root   11T  8,9T  2,0T  82% /home/stephane/Data13TB`
- **T1** `- Corpus : `data/corpus_fr_train.txt` ; validation : derniers 5 %.`
- **T1** `| **gain** | **−4,85 %** |`
- **T1** `- La distillation **améliore** le student de **4,85 %** sans changer son architecture.`
- **T1** `| précision principale | 72,80 % | **72,40 %** |`
- **T1** `| tête 3 | 72,60 % | **72,53 %** |`
- **T1** `| latence service 53 octets | **650,1 ms** |`
- **T1** `- **650 ms** pour 53 octets : le service paie le cache par requête, pas la qualité.`
- **T1** `**N0.15/N4.7 — meilleur student servi** : PPL **2,6998**, parité native, **650 ms**, texte plus`
- **T1** `# N2.5b — capacité à budget égal : 21,63 M bat 11,47 M de 4,1 %`
- **T1** `| **écart moyen** | — | **−8,1 %** |`
- **T1** `| précision principale (moyenne) | **59,23 %** | **60,16 %** |`
- **T1** `| tête 3 (moyenne) | **57,13 %** | **57,81 %** |`
- **T1** `- À **budget égal** et **initialisation égale**, le modèle plus gros est **meilleur de 8,1 % en moyenne**`
- **T1** `- Les précisions sont **proches** (59,1 % vs 58,8 %) : le gain de PPL ne se voit pas encore en top-1.`
- **T1** `**N2.5b — capacité : positif** (−8,1 % de PPL à budget égal sur trois graines), **mais le prior`
- **T1** `| précision principale | 67,96 % | **66,80 %** |`
- **T1** `| tête 3 | 68,01 % | **65,43 %** |`
- **T1** `- **Plus gros, toujours moins bon** : **3,381** contre **3,123**, soit **+8,3 %**.`
- **T1** `- La tête 1 reste faible (**34,7 %**) : les premières couches du gros modèle ne sont pas assez`
- **T1** `49 999 fenêtres, 4 sources ; professeur 30k 1,734 (0,794 bit/octet) ; student 3,123 à 20 000 pas ; meilleur 2,6998 ; plateau 2,708. Le 21,63 M à budget égal donne −8,1 %, mais à 20 000 pas il est pire`
- **T1** `| `corpus_fr.txt` | 4,63 Mo, 72 403 fenêtres possibles |`
- **T1** `| `udhr_train.txt` | 4,38 Mo, 68 433 |`
- **T1** `| `corpus_en.txt` | 100,28 Mo, 1 566 813 |`
- **T1** `| `corpus_mixte_litt.txt` | 12,23 Mo, 191 143 |`
- **T1** `- Quotas **équilibrés** : l'anglais, 100 Mo, est sous-représenté par rapport à son volume.`
- **T1** `| `artefacts/route-teacher-20k/` | 90 Mo | professeur byte-level 23,57 M, 20 000 pas, 0,9195 bit/octet (dossier HF) |`
- **T1** `| `artefacts/drave-n0-base-20k.pt` | 46 Mo | élève de base, 20 000 pas, PPL 3,2064 |`
- **T1** `| `artefacts/{temoin,hierarchie,controle}-g{1,2,3}.pt` | 9 × 47 Mo | les neuf points de contrôle de la distillation |`
- **T1** `| `artefacts/*.pt.drvm` | 9 × 47 Mo | exports DRVM des mêmes points (lecture par le moteur) |`
- **T1** `distillation 3 bras × 3 graines, 5 000 pas, lot 8, 4 segments de 128, lr 1e-4, T=2, α=0,7.`
- **T1** ``/home/stephane/Data13TB/stephane/backups/qtrinet/qtrinet-2026-10-31.bundle` (31 Mo, historique`
- **T1** `- Corpus : `data/corpus_multi_train.txt` (115,4 Mo) ; validation 6,08 Mo.`
- **T1** `| précision principale | — | **36,34 %** |`
- **T1** `| têtes précoces | — | **30,10 / 34,08 / 36,83 %** |`
- **T1** `- **Écart student − professeur** : **-0.055** de PPL (**-0.6 %**).`
- **T1** `- La **précision** tombe à **36,3 %** : le multi-sources est un autre problème.`
- **T1** `| précision principale | 72,62 % | **72,80 %** |`
- **T1** `| tête 3 | 72,69 % | **72,60 %** |`
- **T1** `- La précision monte à **72,80 %** ; la tête 3 recule légèrement à **72,60 %**.`
- **T1** `3 bras (temoin, hierarchie, controle) × 3 graines, 5 000 pas, lot 8, 4 segments de 128`
- **T1** `(= 20,48 Mo vus par run), lr 1e-4, T=2, alpha=0,7, distillation + CE + têtes.`
- **T1** `(4×128, état transporté). Elles ne sont **pas** comparables à 2,6998 / 3,123 : les fenêtres`
- **T1** `| bras | standard 128 | segmenté 4×128 | segmenté sans état |`
- **T1** `Écart total entre les trois bras : **0,0039** (0,13 %). L'état ne domine pas le témoin, et il est`
- **T1** ``(graine-1) × 10 000 019` ; contrôle : perte au pas 1 = 106,5571 (g1) contre 121,5763 (g2).`
- **T1** `Loading weights:   0%|          | 0/68 [00:00<?, ?it/s]`
- **T1** `Loading weights: 100%|██████████| 68/68 [00:00<00:00, 932.90it/s]`
- **T1** `[still running after 60000ms; moved to background job bash-48]`
- **T1** `0, 1164 MiB, 82 %`
- **T1** `1, 1164 MiB, 78 %`
- **T1** `À côté : 232 transcripts de sessions (413 Mo) et un bundle git du dépôt (31 Mo, historique`
- **T1** `0, 1164 MiB, 83 %`
- **T1** `1, 1164 MiB, 83 %`
- **T1** `# fenêtres (82 %). `equilibre` donne le même quota à chaque source.`
- **T1** `| 13:01 | `4442c64c` | N2 — L'ÉTAT DE SECTION NE SE DISTINGUE PAS D'UN ÉTAT ÉTRANGER (+0,36 % CONTRE +0,37 %) |`
- **T1** `[still running after 60000ms; moved to background job bash-81]`
- **T1** `4 sources, **B′** quotas égaux (le manifeste est à **82 % anglais**), **C** curriculum 129`
- **T1** `sur A ; la hiérarchie est écartée deux fois, restent **le curriculum et les données** (41 Mo,`
- **T2** `1, 1164 MiB, 81 %`
- **T2** `data/corpus_fr.txt                 1907    3.8 %`
- **T2** `data/udhr/udhr_train.txt           1802    3.6 %`
- **T2** `data/corpus_en.txt                41257   82.5 %`
- **T2** `data/corpus_mixte_litt.txt         5033   10.1 %`
- **T2** `[still running after 60000ms; moved to background job bash-95]`
- **T2** `> connues**. `porte-homeostasie` (exit 2) : **environnementale** — `/tmp/n4/rang4-lora.pt` effacé`
- **T2** `> livre 10/10, go 9×9 10/10 contre 3/10, dames 0 défaite, cartes 44,7 % contre 51,0 %). Les **deux rouges**`
- **T2** `> `porte-pont` **+2,81 % / +25,35 %**, `porte-coupe` **+0,52 % → +17,09 %**, `porte-gain` **29,0206 →`
- **T2** `> 1297,5437**, `porte-topologie` **42,5477**, `porte-reparti-moteur` **0,0000 %**, `porte-greffe` **branchée**,`
- **T2** `tools/adaptateur_langue.py:19:      --fr data/corpus_fr.txt --pas 2000 [--rang 8] [--sortie /tmp/adaptateur-fr.pt]`
- **T2** `- **Un seul corpus**, français, 4,63 Mo.`
- **T2** `fenêtres de train présentes >1 fois dans train : 47 / 200 (23.5 %)`
- **T2** `[still running after 60000ms; moved to background job bash-121]`
- **T2** `- **R0** : un contrôleur **classique** + un modèle externe atteint-il **90 %** de la compréhension à **30 %** du`
- **T2** `> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par`
- **T2** `0, 1164 MiB, 78 %`
- **T2** `1, 1164 MiB, 80 %`
- **T2** `| [2026-09-29](2026-09-29/attention.md) | `+6 %` · `×2,8` · `×1,8` · `×2,3` |`
- **T2** `| [2026-09-30](2026-09-30/attention.md) | `−61 %` · `−24 %` · `7,59 ms` |`
- **T2** `| [2026-10-01](2026-10-01/attention.md) | `85,1 s` · `× 3` |`
- **T2** `| [2026-10-02](2026-10-02/attention.md) | `×9,34` · `4,5 %` · `1003 ms` · `×3` |`
- **T2** `| bras | graines | protocole 8×16×128 | fenêtres propres | fenêtres contaminées |`
- **T2** `| B — 20 000 pas, manifeste 4 sources (82,5 % anglais) | 3 | **3.7591** | **3.8573** | **3.4554** |`
- **T2** `| Bp — 20 000 pas, 4 sources à quotas égaux (25 %) | 3 | **3.4350** | **3.5634** | **3.1177** |`
- **T2** `> complet (20 000 pas, 41 Mo) fait baisser la PPL de **2,9355 à 2,8527** sous le protocole de N2.19 ;`
- **T2** `> le corpus à quatre sources la fait **monter** à **3,7591** ; et **32,8 % des fenêtres du protocole`
- **T2** `**20,48 Mo d'un seul corpus en 5 000 pas**, la moitié du budget de N2 (41 Mo, 20 000 pas, quatre`
- **T2** `| distillation courte | 5 000 pas · 20,48 Mo · **2,9355** (3 graines) | `artefacts/temoin-g{1,2,3}.pt` |`
- **T2** `Corput), et un décalage de fenêtres par graine `(graine − 1) × 10 000 019` — sans lui, deux graines`
- **T2** `Plan des bras, **budget strictement égal** (20 000 pas × 16 × 128 = **41 Mo vus**), lr 1e-4 sur`
- **T2** `| **B** | manifeste 4 sources : fr 3,8 %, UDHR 3,6 %, **en 82,5 %**, litt. 10,1 % | la diversité, telle que le manifeste la définit |`
- **T2** `| **B′** | 4 sources à **quotas égaux** (25 % chacune) | la part de l'anglais dans l'effet de B |`
- **T2** `| bras | graines | protocole 8×16×128 | fenêtres propres | fenêtres contaminées | 8×15×129 |`
- **T2** `| **B** — 20 000 pas, manifeste 4 sources (82,5 % anglais) | 3 | 3,7591 ±0,0075 | 3,8573 ±0,0161 | 3,4554 ±0,0109 | 3,8218 ±0,0092 |`
- **T2** `| **Bp** — 20 000 pas, 4 sources à quotas égaux (25 %) | 3 | 3,4350 ±0,0022 | 3,5634 ±0,0039 | 3,1177 ±0,0052 | 3,4848 ±0,0041 |`
- **T2** `- **30,7 %** d'un échantillon de 300 fenêtres de validation apparaissent **verbatim** dans`
- **T2** `l'entraînement ; **32,8 %** des 128 fenêtres du protocole (42 sur 128) ;`
- **T2** `- **23,5 %** d'un échantillon de 200 fenêtres d'entraînement apparaissent **plus d'une fois** dans`
- **T2** `protocole. Le manifeste est à 82,5 % anglais alors que le professeur est **français** : les`
- **T2** `- **B11.10** : **hybride 4/4** — codec **161/161**, ambiguïtés refusées ; **69,3 %** natif ;`
- **T2** `-  **N2.h2** (distillation, professeur refait, 3 graines) : **2,9935** contre **2,9927** (+0,029 %) ;`
- **T2** `+- **N2** : GPU ; **N2.d** — le budget plein (20 000 pas, 41 Mo, 3 graines) paie`
- **T2** `+  **2,9355 → 2,8527** ; les quatre sources coûtent **+0,9064** (professeur français, 82,5 %`
- **T2** `+  à 129. **La validation n'est pas tenue à l'écart : 32,8 % des fenêtres du protocole sont`
- **T2** `+129 ; et **32,8 % des fenêtres du protocole de validation sont verbatim dans l'entraînement**`
- **T2** `+| **N — le natif** | DRVM, `drave-n0`, distillation, usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; N2 : budget **−0,08**, **validation contaminée (32,8 %)** ; N4 partiel | **N2** (le corpus dé`
- **T2** `+| **N2** | la distillation : 49 999 fenêtres, 4 sources, professeur Qwen/DeepSeek | 🔬 | **N2.d** — le budget plein paie **2,936 → 2,853** ; les quatre sources coûtent **+0,906** ; **la validation est`
- **T2** `+   jeu **contaminé à 32,8 %** — voir [N2.d](../../reports/rapport-n2-budget.md)) ; **130** est négatif`
- **T2** `+  recopie (32,8 % des fenêtres du protocole sont verbatim dans l'entraînement) : la question n'a de`
- **T2** `0088fc2f R4.4 — L'OCR LIT DIX PAGES À 4,48 % DE WER, LA PARITÉ DE PASSAGE TIENT À 90 %, LA PAGE « PHOTO » TOMBE À 26,7 %`
- **T2** `la question était simple : le dispositif reconstruit hier n'avait vu que **20,48 Mo** d'un seul`
- … (tronqué)

## 5. Erreurs rencontrées

22 sorties en erreur ou divergentes. Les premières :

- **T1** : __pycache__/ *.pyc reports/*.tmp models/ data/ qtrinet-core/target/  # Traces de session : la copie brute reste sur disque (volumineuse, binaire), # le digest markdown est versionné. journal/sessions/
- **T1** : -rw-r--r--. 1 stephane stephane 610 31 oct 17:24 work/n2d/essai-fr.json -rw-r--r--. 1 stephane stephane 650 31 oct 17:24 work/n2d/essai-multi.json === logs === -- A-fr-g1 pas  2250 · seq 128 · perte 5
- **T1** : 54dc7a26 ÉTAT — LA CAMPAGNE N2 BUDGET ET DONNÉES EST OUVERTE, LES GPU RÉSERVÉS JUSQU'À 19 h 40 9f1dcaae N2 — LES POINTS DE CONTRÔLE SONT CONSERVÉS SUR DEUX DISQUES (1,4 GO, EMPREINTES VÉRIFIÉES) === é
- **T2** : 17:35 -- A-fr-g1 pas  8750 · seq 128 · perte 48.6506 · PPL 128/4 2.4483 · 592 s -- B-multi-g1 pas  8750 · seq 128 · perte 91.2001 · PPL 128/4 3.7502 · 591 s -- A-fr-g2 -- B-multi-g2 [exit code: 1]
- **T2** : 17:37 pas 10250 · seq 128 · perte 51.3992 · PPL 128/4 2.4407 · 695 s pas 10500 · seq 128 · perte 48.7937 · PPL 128/4 2.4455 · 712 s [exit code: 1]
- **T2** : 17:37 pas 10750 · seq 128 · perte 53.3267 · PPL 128/4 2.4458 · 730 s pas 11000 · seq 128 · perte 44.5797 · PPL 128/4 2.4276 · 748 s [exit code: 2]
- **T2** : 17:38 pas 12000 · seq 128 · perte 49.2191 · PPL 128/4 2.4135 · 818 s [exit code: 1]
- **T2** : 17:40:04 pas 13000 · seq 128 · perte 53.7650 · PPL 128/4 2.4008 · 886 s pas 13000 · seq 128 · perte 84.8568 · PPL 128/4 3.7372 · 877 s [exit code: 1]
- **T2** : 17:42:32 pas 15250 · seq 128 · perte 45.0087 · PPL 128/4 2.4105 · 1037 s pas 15250 · seq 128 · perte 81.7393 · PPL 128/4 3.7293 · 1027 s [exit code: 1]
- **T2** : 18:19 6 -- A-fr-g3 pas  6750 · seq 128 · perte 53.3343 · PPL 128/4 2.5292 · 453 s -- B-multi-g3 pas  6500 · seq 128 · perte 87.6959 · PPL 128/4 3.7325 · 442 s -- C-129-g1 -- Bp-equilibre-g1 [exit code
- **T2** : 18:29 work/n2d/A-fr-g1.json work/n2d/A-fr-g2.json work/n2d/B-multi-g1.json work/n2d/B-multi-g2.json work/n2d/contamination.json work/n2d/evaluations-finales.json -- A-fr-g3 pas 16000 · seq 128 · perte
- **T2** : 18:40 8 -- C-129-g1 pas  6000 · seq 129 · perte 51.6991 · PPL 128/4 2.4037 · 403 s -- Bp-equilibre-g1 pas  5750 · seq 128 · perte 104.8664 · PPL 128/4 3.3953 · 377 s -- C-129-g2 -- Bp-equilibre-g2 [ex
- **T2** : 18:40 [exit code: 2]
- **T2** : 18:51 work/n2d/A-fr-g1.json work/n2d/A-fr-g2.json work/n2d/A-fr-g3.json work/n2d/B-multi-g1.json work/n2d/B-multi-g2.json work/n2d/B-multi-g3.json work/n2d/C-129-g1.json work/n2d/contamination.json wo
- **T2** : 19:03 [exit code: 2]

## 6. Commits

- ÉTAT — LA CAMPAGNE N2 BUDGET ET DONNÉES EST OUVERTE, LES GPU RÉSERVÉS JUSQU'À 19 h 40  Une seconde session peut démarrer : en-cours nomme désormais la session a
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add .gitignore docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/backlog/N2-distillatio
- RÉFÉRENCES — LA PASSE DU 31 À 19 h 42 ENTRE EN TÊTE, LA PAGE RESTE SOUS SON BUDGET  La passe complète de clôture (79 portes, 75 vertes, 4 rouges, 1 h 39, journa
- ÉTAT — LA SESSION N2.h PORTE SON PLAN, SON AMBITION ET SA STRATÉGIE DANS LA PAGE D'ÉTAT  La page d'état doit suffire à une autre session : en-cours expose maint

