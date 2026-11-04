# Session 0733c5bb — Session N2 : plan et réservations

> **Journaux :** [le jour](../../2026-11-02/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `0733c5bb-f90b-4f58-9241-3364fa32e46c` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-02 16:14 |
| Durée | 44.8 h |
| Tours | 8 |
| Messages | 787 |
| Appels d'outils | 730 |
| Fichiers touchés | 27 |
| Commandes | 540 |
| Sous-agents | 0 |
| Commits | 30 |
| Compactages de contexte | 0 |

## Objectifs déclarés

- **create** — Session N2 (0733c5bb), cycle de nuit jusqu'à 2026-11-03 08 h : (1) R1.2 à 1 024 octets entraînés — comparer à octets constants et à pas constants, contrôles « même texte » et miroir de copie, fiche + JSON + commit ; (2) la fenêtre sur le modèle de production (mélange 1 Go) — affiner mix-60k avec une
… [431 caractères tronqués]
- **edit** — Session N2 (0733c5bb), phase du 03/11 après la nuit : (1) le run long de production à fenêtre 1 024 (30 000 pas de plus, 60 000 au total) — mesurer si le domaine passe sous 2,9 et si la validation du grand corpus tient sous 2,5 ; (2) la capacité sur le corpus propre — trois tailles (11,47 / 21,65 / 
… [442 caractères tronqués]
- **resume** — Session N2 (0733c5bb), phase du 03/11 après la nuit : (1) le run long de production à fenêtre 1 024 (30 000 pas de plus, 60 000 au total) — mesurer si le domaine passe sous 2,9 et si la validation du grand corpus tient sous 2,5 ; (2) la capacité sur le corpus propre — trois tailles (11,47 / 21,65 / 
… [442 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — Tu es la session N2 (le natif, GPU). Lis AGENTS.md, docs/pilotage/en-cours.md et  docs/pilotage/backlog/N2-distillation.md. Ton id est dans `printenv DSH_SESSION_ID` ; crée  journal/sessions/<id>/plan.md avec `python3 tools/sessions.py --modele` (les onze champs,  État : actif, heartbeat maintenant), puis réserve `data/`, `tools/corpus*`, `reports/n2-*`,  `work/n2*`. Prochaine action : 200 000 pas … [298 caractères tronqués]

**Tour 2** — vérifie ce que les autres sessions font et continue avec des tâches jusqu'à demain matin 8h

**Tour 3** — background job bash-354 (bash: sleep 900; cd /home/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; cat work/n2ac/chaine_prod_zero.out work/n2ac/cap2165.out work/n2ac/cap1147.out 2>/dev/null; ls work/n2ac/mix512-zero-15k.pt 2>/dev/null && echo OKZERO) finished [status: completed, exit code: 0]. Read its output with job_output.

**Tour 4** — background job bash-356 (bash: cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 ~/gpu-env/bin/python work/n2ac/eval_production.py work/n2ac/mix512-zero-15k.pt --rope --longueurs 128,512,1000,2000 --sortie work/n2ac/eval-mix512-zero-15k.json 2>&1 | grep -E '"(128|512|1000|2000)"|litterature|anglais|wikitext2|permute_fr') finished [status: completed, exit code: 0]. Read its ou … [21 caractères tronqués]

**Tour 5** — continue

**Tour 6** — continue

**Tour 7** — <goal_round> Objective: "Session N2 (0733c5bb), phase du 03/11 après la nuit : (1) le run long de production à fenêtre 1 024 (30 000 pas de plus, 60 000 au total) — mesurer si le domaine passe sous 2,9 et si la validation du grand corpus tient sous 2,5 ; (2) la capacité sur le corpus propre — trois tailles (11,47 / 21,65 / 34,3 M) à fenêtre 512 et octets constants, depuis une init aléatoire identi … [912 caractères tronqués]

**Tour 8** — reprends

## 2. Déroulé, étape par étape

### Tour 1 — Tu es la session N2 (le natif, GPU). Lis AGENTS.md, docs/pilotage/en-cours.md et  docs/pilotage/backlog/N2-distillation. … [578 caractères tronqués]

*240 appels d'outils.* Actions notables :

- bash — Get session ID and workspace listing
- read
- bash — Resolve workspace paths and git state
- bash — Inspect sessions tool help
- bash — Show session plan template and status
- bash — List N2 reports, tools, work, data
- bash — Read 1GB corpus report
- bash — List n2 work dirs and n2 tools
- bash — Find report with 3.49 / 6.03 figures
- bash — Read canal 34m report
- bash — Read melange report
- bash — Inspect drvm config and training log
- bash — Inspect drave-core and mix corpus
- bash — Read training script header
- … et 189 autres

**Synthèse produite :**

⏵ Cycle clos : je rends la ligne d'état et les commits

Cycle terminé, mesuré, écrit et committé. Voici l'essentiel.

\## Les deux faits du cycle

**1. 200 000 pas sur le mélange 1 Go** (recette N2.ac inchangée, 3 h 10 de GPU 0, 11 410 s) :

| mesure | 60 k | **200 k** | écart |
|---|---:|---:|---:|
| validation française (L128) | 3,4902 | **3,1591** | −0,33 |
| grand corpus (L128) | 3,3565 | **3,0035** | −0,35 |
| littérature | 6,0283 | **5,6056** | −0,42 |
| anglais | 8,3352 | **7,2770** | −1,06 |
| wikitext2 | 9,0525 | **8,0018** | −1,05 |
| permutation (contrôle) | 215,6 | **181,9** | — |

Le français tient et **la largeur progresse** — mais **la porte 2,5 n'est pas atteinte** : 3,1591 en domaine, et la loi de puissance de la trajectoire (b = 0,0987 sur 20 k–200 k, 0,0894 sur 40 k–200 k, exposant **décroissant**) place 2,5 à **1,3–2,7 M pas**, soit 21 à 44 h de GPU. Surtout, le gain **s'inverse à 512 octets** (+0,14, +0,31 à 1 000) : entraîner plus longtemps sans entraîner plus long **durcit** le verrou de longueur.

**2. R1.1/R1.2 — la fenêtre** (RoPE, 34,3 M, même budget) : la PPL à 1 000 octets passe de **8,2024** à **3,2545** (porte 1,5 tenue à **0,97×** contre 2,33×), avec deux contrôles : à texte et prédécesseurs identiques, RoPE est **invariant** au décalage (Δ 0,0017) quand la table absolue **×4,8** ; et entraîner les positions 0–1279 fait tomber l'explosion à 4,0956. **Mais** depuis une initialisation figée, RoPE se dégrade dès 160 octets et ne se redresse pas à 40 k pas — la platitude vient de l'initialisation, pas du schéma seul. **R1.2 tranche** : à **octets constants**, la fenêtre 512 gagne partout, **−0,244 à 1 000**, et le modèle **utilise** le contexte (2,9654 → 2,8819). Le miroir de copie est muet (0,0078) : la PPL n'est pas la lecture.

Découverte de méthode au passage : **la graine est inerte sous `--init`** (deux lancements, même `sha256_drvm`) — l'« intervalle de graine » ±0,012 de N2.z n'en était pas un, c'était la séquence de décalages de position, précisément ce que RoPE supprime.

\## Ma ligne d'état (déjà intégrée par le hub)

> **N2** : N2.ac 1 Go — 3,49 domaine, 6,03 littérature ; **200 k pas** — val_fr **3,1591** (−0,33), grand corpus **3,0035**, littérature **5,6056**, anglais **7,2770**, wikitext2 **8,0018** : **< 2,5 non atteinte** (la loi place 2,5 à **1,3–2,7 M pas**), et le gain **s'inverse à 512 octets** (+0,14) — le compute ne remplace pas une fenêtre entraînée ; N4 0/40.
>
> **R1 — la fenêtre native** : R1.1 RoPE **3
… [958 caractères tronqués]

### Tour 2 — vérifie ce que les autres sessions font et continue avec des tâches jusqu'à demain matin 8h

*241 appels d'outils.* Actions notables :

- bash — Check active sessions status
- bash — Check recent commits and hardware state
- bash — Check which gates use GPU and which device
- bash — Check running gate processes
- create_goal
- bash — Reopen session plan for the night cycle
- write `/home/stephane/GitHub/Qtrinet/work/n2ac/chaine_1024.sh`
- bash — Launch 1024-window training chain
- bash — Read state header and closed sessions block
- bash — Add night session section to state
- bash — Fix typo and check budget/review
- bash — Condense section and fix counters
- bash — Trim header duplication and recheck gates
- bash — Read required session fields
- … et 170 autres

**Synthèse produite :**

⏵ Évaluation du contrôle « production depuis zéro »

### Tour 3 — background job bash-354 (bash: sleep 900; cd /home/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; cat work/n2ac/chaine_pro … [204 caractères tronqués]

### Tour 4 — background job bash-356 (bash: cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 ~/gpu-env/bin/pyt … [301 caractères tronqués]

### Tour 5 — continue

*13 appels d'outils.* Actions notables :

- bash — Read zero control results and 128 arms state
- bash — Evaluate capacity experiment arms
- bash — Fill zero control and capacity sections
- bash — Update state with zero control and capacity
- bash — Inspect budget violation detail
- bash — Run closure gates before commit
- bash — Commit the night's three facts
- job_output
- bash — Close the night cycle in plan and récit
- bash — Mark session closed in state
- bash — Fix counter and commit night closure
- bash — Final verification pass and summary

**Synthèse produite :**

⏵ Cycle de nuit clos : je rends les résultats, l'état et les commits

Le cycle de nuit est terminé et committé. Il a débordé du créneau (la session a été suspendue vers 04 h et reprise à 11 h 20) : je l'ai clos à 11 h 32, GPU libres.

\## Ce que font les autres sessions

- **Hub / pilotage** : passe de portes terminée — `porte-homeostasie` **verte** (elle régénère son LoRA au lieu d'échouer, 10 min) ; **règle 11 ajoutée à AGENTS** (GPU réservés à Drave, professeurs par l'API DeepSeek, jamais de serveur local) avec un **blocage nommé** : la clé API DeepSeek est absente ; discipline de budget (AGENTS 1 196–1 198 mots, T0 sous 4 000).
- **L/B13 (Pensée)** : **gold réel 432** — POS 0,9065, syntagmes 0,4598, tête 0,5633, acte 0,9954, **verdict FALSE** ; la « fenêtre » (labyrinthe) est **non discriminante** (BFS 228, aveugle 215, 7B 238 : tout le monde passe) ; **parité DRVM/native 114/114 poids, 5/5 prompts**, mais le point de contrôle est volatil.
- **S (structures)** : analyseur **54/55 types, 131/131 rôles, 47/47 compléments** ; corpus réel 8,5 % CEGEP / 65,5 % propre ; banque 200 phrases / 355 candidats.
- **D/R/A** : close (OCR CEGEP 91 scans uniques, 60 documents, 1 982 p).

\## Mes quatre faits de la nuit

**1. La loi de la fenêtre** (à octets constants, 20,5 Mo) : à 1 000 octets, 3,2545 (fenêtre 256) → 3,0107 (512) → **2,9950** (1 024) → 3,0202 (2 048). Le **point d'équilibre est 1 024** à ce budget — et il **se déplace avec le budget** (à 246 Mo, 2 048 donne 2,5114 à 4 000 octets). Le contrôle « même texte » montre que **chaque modèle sature exactement à sa fenêtre** (256 se dégrade au-delà ; 1 024 = 2 000 au millième).

**2. La fenêtre est la recette de production** : N2.ac affiné avec RoPE + fenêtre entraînée **écrase N2.ac et le run de 200 k pas** à octets ajoutés constants. Poussé à **30 000 pas à 1 024 (307 Mo)** : **2,9943** en domaine à 128, 2,6143 à 1 000, 2,5628 à 2 000, et **2,4759 / 2,4373 sur la validation du grand corpus — sous 2,5**, une première. Contrôle depuis zéro : la **fenêtre fait la longueur**, l'**initialisation fait le niveau** (−0,16).

**3. La porte < 2,5 sur le corpus propre** : **non atteinte** — 2,7856 en val (0,29 manquant), 2,8566 en test — mais la fenêtre est le **seul bras dont la courbe descend** (2,9726 → 2,7856 contre 2,9027 → 3,1107 pour la fenêtre 128), et les deux bras battent la chaîne honnête de N2.h (3,0904). Le corpus (3,24 Mo) est épuisé : la suite est la **capacité**, pas les pas.

**4. La fenêtre paie à toute
… [1692 caractères tronqués]

### Tour 6 — continue

*149 appels d'outils.* Actions notables :

- bash — Check current repo and hardware state
- get_goal
- update_goal
- bash — Check state presence of my session
- bash — Launch long production run and capacity on clean corpus
- bash — Reopen plan and state
- bash — Fix T0 and commit reopening
- bash — Trim T0 and retry commit after lock
- job_output
- bash — Read current session block and T0
- bash — Rewrite session block compactly
- bash — Commit state and check runs
- bash — Check disk space and git index state
- bash — Check inodes and git index health
- … et 99 autres

**Synthèse produite :**

⏵ Phase close (session en pause, un run en vol) — je rends les résultats et les commits

La phase « continue » est mesurée, écrite et committée. Quatre faits de plus aujourd'hui, tous avec fiche, JSON, ligne d'état et commit.

\## Les quatre faits

**1. La capacité sature sur le corpus propre** — trois tailles, même recette (RoPE, fenêtre 512, init aléatoire identique, 33 Mo), val à 1 024 octets :

| capacité | 1 024 octets (val) |
|---|---:|
| 11,47 M | 2,8960 |
| 21,65 M | 2,8688 |
| **34,3 M** | **2,8662** |

Rien entre 21,65 et 34,3 M (+0,011 à 512, −0,003 à 1 024 : le bruit). **Ni les pas (3,24 Mo vus dix fois), ni la capacité ne ferment la porte < 2,5** (il reste 0,37) : la suite est un corpus propre plus large, ou la distillation.

**2. Le run long de production** — 60 000 pas à fenêtre 1 024 (552 Mo) : **2,9121** en domaine à 128, **2,5276** à 1 000, **2,4761** à 2 000 ; au grand corpus **2,3911 / 2,3522** ; littérature 5,13, anglais 6,20, wikitext2 6,79. Chaque doublement des pas vaut **−0,085** en domaine — loi géométrique, la même à toutes les longueurs. À 128 octets il reste 0,41 au-dessus de 2,5, soit ≈ 2 M de pas.

**3. La distillation native** (nouveau distillateur `work/n2ac/distiller_natif.py`) — le professeur long dans un élève 11,47 M à fenêtre 512, même init, mêmes 33 Mo :

| élève 11,47 M / 512 | 128 | 512 | 1 024 |
|---|---:|---:|---:|
| dur (α = 0) | 3,6452 | 3,4493 | 3,3628 |
| α = 0,5 | 3,5861 | 3,4330 | 3,3819 |
| **α = 0,9** | **3,5090** | **3,2835** | **3,1863** |

**La douceur forte est la bonne cible** (mélanger dilue le professeur) et le gain **croît avec la longueur** (−0,18 à 1 024) alors que l'élève ne voit que 512 octets. Coût : **+25 % par pas** (259 contre 208 ms), pas ×2 comme le laissait croire un premier run sous contention.

**4. La distillation de production** — le même professeur distillé dans la recette 512 (34,3 M, même init, mêmes 61,4 Mo que l'affinage dur) : **3,0550 / 2,8062 / 2,7015 / 2,6601** contre 3,1588 / 2,9096 / 2,8018 / 2,7607, soit **−0,10 partout** en domaine et **−0,29 / −0,52** hors domaine. La recette de production devient « professeur 1 024 + élève 512 distillé » : **9× moins d'octets** que le run de 552 Mo pour 0,14 de PPL.

\## Ma ligne d'état

> **N2** — 1 024 = recette de production (2,48–2,91 ; sous 2,5 au grand corpus) ; le compute à 128 : 3,1591/8,2262 ; **distillé : −0,10** (3,0550).
> **porte propre** : 2,8662 à 34,3 M, **capacité saturée** ; il reste 0,37.

\## Commits

- **`ad070205`** 
… [896 caractères tronqués]

### Tour 7 — <goal_round> Objective: "Session N2 (0733c5bb), phase du 03/11 après la nuit : (1) le run long de production à fenêtre 1 … [1192 caractères tronqués]

*29 appels d'outils.* Actions notables :

- bash — Check overnight distillation run and repo state
- bash — Launch 2048 same-steps run
- job_output
- bash — Cross-check fiche numbers against JSONs
- bash — Audit numbers with mixed formats
- bash — Run output mirror and same-text controls on production models
- bash — Add output controls to production fiche
- bash — Commit output controls complement
- bash — Trim T0 after complement
- bash — Commit T0 fix and check review
- bash — Retry T0 fix commit after lock
- bash — Read hub's night plan and GPU expectations
- bash — Check state content and T0 after hub rewrite
- bash — Update state with current runs and commit
- … et 8 autres

**Synthèse produite :**

⏵ Préparation des deux compléments (2 048 mêmes pas, distillation 30 k) pendant les runs

### Tour 8 — reprends

*58 appels d'outils.* Actions notables :

- bash — Check time, runs, GPU and git state
- bash — Inspect relaunched runs and reboot commit
- bash — Read my plan and state block after reboot
- bash — Check for leftover placeholders in fiches
- bash — Check relaunch commands and plan diff
- bash — Reopen plan after reboot
- bash — Write post-reboot narrative and commit
- job_output
- bash — Compare loss normalization with reference trainer
- bash — Fix loss normalization and launch parity controls
- bash — Check parity control alpha=0 progress
- bash — Wait for the corrected alpha=0 control
- bash — Poll corrected alpha=0 run
- bash — Wait for corrected alpha=0 completion
- … et 29 autres

**Synthèse produite :**

⏵ La repondération vaut −0,05 (pas −0,14) : correction du point 3 de l'erratum

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/GitHub/Qtrinet/journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/eval_200k.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/rope_model.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/entrainer_rope.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/eval_longueurs.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/chaine_r1.sh` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/mirroir_copie.py` | 2 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/eval_fenetre.py` | 2 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/agrege_r11.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-n2-r11.md` | 3 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/init_figee.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/chaine_zero.sh` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/trajectoire.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/table_200k.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-n2-200k.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/cloture.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/chaine_1024.sh` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/chaine_production.sh` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/eval_production.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/chaine_2048.sh` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-n2-fenetre.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/agrege_fenetre.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-n2-r12-2048.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-n2-production-fenetre.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-n2-porte-propre.md` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/work/n2ac/distiller_natif.py` | 1 | 0 |
| `/home/stephane/GitHub/Qtrinet/reports/rapport-n2-distillation-native.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Get session ID and workspace listing
- **T1** Resolve workspace paths and git state
- **T1** Inspect sessions tool help
- **T1** Show session plan template and status
- **T1** List N2 reports, tools, work, data
- **T1** Read 1GB corpus report
- **T1** List n2 work dirs and n2 tools
- **T1** Find report with 3.49 / 6.03 figures
- **T1** Read canal 34m report
- **T1** Read melange report
- **T1** Inspect drvm config and training log
- **T1** Inspect drave-core and mix corpus
- **T1** Read training script header
- **T1** Check GPU status
- **T1** Read rest of training script
- **T1** Read analysis and cross eval scripts
- **T1** Find references to mix-60k
- **T1** Grep mix-60k in journal and docs
- **T1** Find training command for mix-60k
- **T1** Extract mix training command
- **T1** Find mix corpus training invocation
- **T1** Read example session plan
- **T1** Read sessions.py beginning
- **T1** Run strict session check
- **T1** Read sessions.py check logic
- **T1** Read full modele template
- **T1** Read previous N2 session plan
- **T1** List session dirs and journal
- **T1** Check date and R1.1/R1.2 in roadmap
- **T1** Read N2 to R1 handoff report
- **T1** Read native model definition
- **T1** Read model forward and export
- **T1** Read journal verifier
- **T1** Inspect session dir contents and README
- **T1** Read journal rules for session report
- **T1** Validate and commit session plan
- **T1** Check RAM, CPUs, gpu python
- **T1** Launch 200k training run in background
- **T1** Check training start and GPU processes
- **T1** Identify GPU holder and wait for training log
- … et 500 autres

## 4. Mesures et résultats marquants

- **T1** `# N2.aa — Le corpus de 831 Mo à compute constant : un autre domaine, pas plus de savoir`
- **T1** `> étages de 20 000 pas, canal), le corpus de **831 Mo** (600 000 articles, offset 1 M, **0 fuite**)`
- **T1** `> propre domaine** (écart ~0,2) : à 40 Mo vus, un corpus 5,6× plus grand ne fait pas apprendre plus`
- **T1** `200 000) ; brut **1 048 Mo** → dédupliqué **924 Mo (88,2 %)** → train **831 Mo**, val 46 Mo, test`
- **T1** `46 Mo ; **0 fuite** sur 4 000 fenêtres (`reports/corpus-wiki-big-propre.json`).`
- **T1** `- **Modèle** : 34,3 M (`384/512`), deux étages de 20 000 pas × 8 × 128, positions [0, 384], canal de`
- **T1** `| modèle | val N2.z (186 Mo) | val grand (831 Mo) |`
- **T1** `| **N2.z** (186 Mo, canal) | **3,5250** | 3,7107 |`
- **T1** `| **grand** (831 Mo, canal) | 3,7025 | **3,4604** |`
- **T1** `**Le corpus ne paie pas à compute constant.** Les deux modèles ont vu **40 Mo** de texte (2 × 20 000`
- **T1** `pas × 8 × 128) ; le grand en a vu 5 % et le petit 21 %. Le grand ne peut donc pas « savoir plus » :`
- **T1** `**La bonne question n'est donc pas « plus de données ? » mais « plus de pas ? ».** À 40 Mo vus, le`
- **T1** `(le contrôle : 200 000 pas sur 186 Mo, puis sur 831 Mo).`
- **T1** `- **40 Mo vus** : c'est le point le plus limitant ; à 200 000 pas, la conclusion pourrait s'inverser.`
- **T1** `- Réentraînement : 20 000 pas × 8 × 128, lr 3e-4, graine 1, positions [0, 384], **avec le canal**`
- **T1** `| **34,3 M avec canal** (2 graines) | **3,5250** | **3,4926** | **3,6632** | ×6,5 | ×11,2 |`
- **T1** `| 11,47 M sans canal | 4,3893 | 4,49 | 5,67 | ×5,6 | ×10,0 |`
- **T1** `| 11,47 M avec canal | 4,1738 | 4,21 | 5,45 | ×5,6 | ×10,3 |`
- **T1** `que 4 % — le meilleur résultat de la nuit, et de loin (le 34,3 M distillé : 4,09).`
- **T1** `**La typoglycémie ne s'améliore pas** (×6,6) : le canal ne change pas la nature du lecteur — il`
- **T1** `> **mélange** (186 Mo + 831 Mo = **1,02 Go**, 60 000 pas) vaut **3,4902** sur la validation`
- **T1** `- Corpus : `data/wiki_fr/propre/train.txt` (186 Mo) + `data/wiki_big/propre/train.txt` (831 Mo)`
- **T1** `- Recette : 34,3 M, **60 000 pas** × 8 × 128, positions [0, 384], canal — identique à fr-60k et`
- **T1** `| **fr-60k** (186 Mo) | **3,4365** | 3,7237 | 6,0011 | 9,5185 | 10,7138 |`
- **T1** `| **big-60k** (831 Mo) | 3,5877 | **3,3301** | 6,1381 | **8,3173** | 9,1609 |`
- **T1** `��"�<vl	���=�����4=Z� =Iݖ=KH�;��=�ȸ=턅=�	�=̑��J�)��1�Sj�;������\3%==f�<��ڼ��Z��$�=jr���<`
- **T1** `=��1�ʽ�ID<�b�<�#�=���~��=̶%<�����@�<�V���-y=�g������n="=���"���N;C�O=����|6;��3%���ȼAǼ=`
- **T1** `=/�0��?�</����=��=G��<!�ʼ{=�<$%�%ڼ���<��=�T=RA���I�=�V�����=ɢ<4ױ< 3%�hp=ov۽:������ ����ފ;���=��=��=�C�<�*=�䭼'������<��� ��; ,�\6v=�H��	���Lu�<�.=j�*�mԨ�k����(�<g�="�;��<	�=��*��ܼ`
- **T1** `0, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T1** `1, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %`
- **T1** `20961:- Corpus : `data/wiki_big/propre/` (831 Mo) et `data/wiki_mix/propre/` (1,02 Go), manifeste [`corpus-wiki-big-propre.json`](reports/corpus-wiki-big-propre.json).`
- **T1** `- **Objectif final** : un **mètre honnête** pour N2 — corpus dédupliqué (0 % de fenêtres de`
- **T1** `- **Résultat** : corpus 4,63 → 3,61 Mo (−22,2 %), **0 / 2 814** fenêtres de validation dans`
- **T1** `l'entraînement (contre 32,8 %) ; chaîne propre **3,09** en domaine, **16,70** sur la littérature`
- **T1** `33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)**`
- **T1** `36:| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art.,`
- **T1** `188:| **N2** | la distillation : corpus, professeur, [curriculum](../theorie/glossaire/entrees/curriculum.md) | 🔬 | **N2.h** — corpus dédupliqué (**0 %** de fuite) : la chaîne propre vaut **3,0904**, `
- **T1** `1. **La position absolue est un défaut d'architecture, pas une propriété du corpus.** Sur 3,24 Mo`
- **T1** `(N2.h3) comme sur 186 Mo (N2.j2), la PPL à 256 octets tombe de **14,11 → 3,25** et de`
- **T1** `181-- Points de contrôle : 542 Mo sur deux disques (`backups/n2/2026-10-31/n2d/`, `IA/artefacts/n2/2026-10-31/n2d/`).`
- **T1** `[still running after 60000ms; moved to background job bash-36]`
- **T1** `0, 620 MiB, 0 %`
- **T1** `1, 710 MiB, 0 %`
- **T1** `[still running after 60000ms; moved to background job bash-40]`
- **T1** `0, 1 MiB, 0 %`
- **T1** `1, 1 MiB, 0 %`
- **T1** `0, 1322 MiB, 96 %`
- **T1** `1, 1304 MiB, 85 %`
- **T1** `0, 1642 MiB, 99 %`
- **T1** `1, 1422 MiB, 95 %`
- **T1** `[still running after 60000ms; moved to background job bash-65]`
- **T1** `[still running after 60000ms; moved to background job bash-66]`
- **T1** `[still running after 60000ms; moved to background job bash-69]`
- **T1** `[still running after 60000ms; moved to background job bash-71]`
- **T1** `[still running after 60000ms; moved to background job bash-72]`
- **T1** `- un chiffre sans dispositif (« 73 % ») ;`
- **T1** `210:| [rapport-n2-anglais-distille.md](rapport-n2-anglais-distille.md) | N2.n — La distillation anglaise : 4,42 → 3,94, la chaîne complète sur 204 Mo |`
- **T1** `211:| [rapport-n2-anglais.md](rapport-n2-anglais.md) | N2.m — L'anglais seul : 4,42 sur 204 Mo, et ce que le multilingue coûte (1,6 PPL) |`
- **T1** `216:| [rapport-n2-canal.md](rapport-n2-canal.md) | N2.l — Le canal de structure : +5 % de PPL, et le même alphabet |`
- **T1** `[still running after 60000ms; moved to background job bash-83]`
- **T1** `> connues**. `porte-homeostasie` (exit 2) : **environnementale** — `/tmp/n4/rang4-lora.pt` effacé`
- **T1** `> `porte-pont` **+2,81 / +25,35 %**, `porte-coupe` **+0,52 → +17,09 %**, `porte-gain` **29,0206 →`
- **T1** `[still running after 60000ms; moved to background job bash-97]`
- **T1** `[still running after 60000ms; moved to background job bash-98]`
- **T1** `[still running after 60000ms; moved to background job bash-100]`
- **T1** `[still running after 60000ms; moved to background job bash-101]`
- **T1** `[still running after 60000ms; moved to background job bash-108]`
- **T1** `[still running after 60000ms; moved to background job bash-118]`
- **T1** `[still running after 60000ms; moved to background job bash-119]`
- **T1** `[still running after 60000ms; moved to background job bash-120]`
- **T1** `[still running after 60000ms; moved to background job bash-131]`
- **T1** `[still running after 60000ms; moved to background job bash-134]`
- **T1** `[still running after 60000ms; moved to background job bash-135]`
- **T1** `[still running after 60000ms; moved to background job bash-141]`
- **T1** `[still running after 60000ms; moved to background job bash-142]`
- **T1** `[still running after 60000ms; moved to background job bash-151]`
- **T1** `1 982 p, 4 408 811 caractères**, **8 Ko 0** ; recouvrement éval `fr-xnli` **0/40**,`
- **T1** `[still running after 60000ms; moved to background job bash-154]`
- **T1** `[still running after 60000ms; moved to background job bash-155]`
- **T1** `[still running after 60000ms; moved to background job bash-156]`
- **T1** `[still running after 60000ms; moved to background job bash-157]`
- **T1** `[still running after 60000ms; moved to background job bash-159]`
- **T1** `[still running after 60000ms; moved to background job bash-173]`
- **T1** `[still running after 60000ms; moved to background job bash-177]`
- **T1** `- **R4.1–R4.4** : **mesurés** (R4.4 : 4/5 ≥ **90 %**) ; **typoglycémie** ×17,8 intérieur, ×62,7 tout ; [`r44-scans`](../../reports/rapport-r44-scans.md), [`typoglycemie`](../../reports/rapport-typogly`
- **T2** `→ la **passe de portes** est **en cours** (`porte-bus`, 19 h 37 ; GPU libres) ; à son verdict, **intégrer les lignes B13/N2/S** et mettre `en-cours` à jour. La sous-passe documentaire (8 portes) rend `
- **T2** `0, 490 MiB, 0 %`
- **T2** `1, 122 MiB, 0 %`
- **T2** `0, 5766 MiB, 100 %`
- **T2** `[still running after 60000ms; moved to background job bash-198]`
- **T2** `[still running after 60000ms; moved to background job bash-202]`
- **T2** `[still running after 60000ms; moved to background job bash-203]`
- **T2** `[still running after 60000ms; moved to background job bash-205]`
- **T2** `[still running after 60000ms; moved to background job bash-209]`
- **T2** `[still running after 60000ms; moved to background job bash-210]`
- **T2** `[still running after 60000ms; moved to background job bash-211]`
- **T2** `[still running after 60000ms; moved to background job bash-216]`
- **T2** `[still running after 60000ms; moved to background job bash-220]`
- **T2** `[still running after 60000ms; moved to background job bash-222]`
- **T2** `0, 5646 MiB, 100 %`
- **T2** `[still running after 60000ms; moved to background job bash-225]`
- **T2** `[still running after 60000ms; moved to background job bash-226]`
- **T2** `- **S — le banc de structures** : **analyseur 54/55 types, 131/131 rôles, 47/47 compléments**, **corpus réel 8,5 % CEGEP / 65,5 % propre** (mélange 9,1 %), gold **55**, **47 tests** ; corpus **55** st`
- **T2** `[still running after 60000ms; moved to background job bash-236]`
- **T2** `[still running after 60000ms; moved to background job bash-245]`
- **T2** `[still running after 60000ms; moved to background job bash-246]`
- **T2** `[still running after 60000ms; moved to background job bash-249]`
- **T2** `[still running after 60000ms; moved to background job bash-250]`
- **T2** `0, 370 MiB, 0 %`
- **T2** `1, 10068 MiB, 100 %`
- **T2** `1024 (2,5k pas, 20,5 Mo) {'128': 3.3878, '256': 3.2542, '512': 3.1098, '1000': 2.995, '2000': 2.9449}`
- **T2** `1024 (20k pas, 164 Mo) {'128': 2.9955, '256': 2.8513, '512': 2.7201, '1000': 2.6256, '2000': 2.5757, '4000': 2.5429}`
- **T2** `2048 (1,25k pas, 20,5 Mo) {'128': 3.4179, '256': 3.2924, '512': 3.145, '1000': 3.0202, '2000': 2.963, '4000': 2.9265}`
- **T2** `> **octets constants** (20,5 Mo vus sur `data/wiki_fr`), la fenêtre entraînée paie jusqu'à`
- **T2** `[still running after 60000ms; moved to background job bash-265]`
- **T2** `[still running after 60000ms; moved to background job bash-267]`
- **T2** `[still running after 60000ms; moved to background job bash-269]`
- **T2** `[still running after 60000ms; moved to background job bash-273]`
- **T2** `[still running after 60000ms; moved to background job bash-275]`
- **T2** `[still running after 60000ms; moved to background job bash-278]`
- … (tronqué)

## 5. Erreurs rencontrées

25 sorties en erreur ou divergentes. Les premières :

- **T1** : journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md:20686:- **bash** `{"command": "sleep 300; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -2 work/n2w/mix-60k.
- **T1** : (no output) [exit code: 1]
- **T1** : #!/bin/sh # pre-commit — l'état accompagne le fait, le journal accompagne le code. # # Versionné dans tools/hooks/ et installé par tools/installe_hooks.sh : un hook qui # ne vit que dans .git/hooks ne
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 9, in <module> RuntimeError: shape '[8, 512]' is invalid for input of size 36096 [exit code: 1]
- **T1** : File "/home/stephane/gpu-env/lib64/python3.13/site-packages/torch/serialization.py", line 795, in _open_file_like     return _open_file(name_or_buffer, mode)   File "/home/stephane/gpu-env/lib64/pytho
- **T1** : 560 647 [stderr] Traceback (most recent call last):   File "<stdin>", line 21, in <module> AssertionError [exit code: 1]
- **T1** : [stderr] Traceback (most recent call last):   File "<stdin>", line 23, in <module> AssertionError [exit code: 1]
- **T2** : 21:26:35 pas   3950 · perte 0.9907 · PPL val 2.701 · 1684 s pas   8950 · perte 1.0638 · PPL val 2.673 · 4136 s [exit code: 2]
- **T2** : fiche corrigée 0 [exit code: 1]
- **T2** : 23:06:53 pas   1300 · perte 1.0420 · PPL val 2.720 · 1436 s [exit code: 2]
- **T2** : 23:42:44 pas   3250 · perte 1.0465 · PPL val 2.630 · 3570 s [exit code: 2]
- **T2** : 01:10:11 rope2048-1.25k fini 22:22:47 [exit code: 2]
- **T2** : 02:14:56 propre512-8k fini 02:01:51 e 1.0496 · PPL val 2.489 · 8127 s pas  18300 · perte 0.9682 · PPL val 2.491 · 8149 s [exit code: 2]
- **T2** : 02:26:07 propre512-8k fini 02:01:51 e 1.1004 · PPL val 2.477 · 8813 s pas  19850 · perte 0.9055 · PPL val 2.469 · 8836 s [exit code: 2]
- **T2** : prod-zero lancé pid 855944 02:36:45 � PPL val 2.481 · 9433 s pas  21250 · perte 1.0120 · PPL val 2.481 · 9455 s [exit code: 2]

## 6. Commits

- N2 — MANDAT 200 k PAS SUR LE MÉLANGE 1 Go, PUIS R1.1/R1.2 (session 0733c5bb)" && git log --oneline -1
- cd /home/stephane/GitHub/Qtrinet && git add reports/rapport-n2-r11.md reports/n2-r11.json docs/pilotage/en-cours.md journal/sessions/0733c5bb-f90b-4f58-9241-336
- cd /home/stephane/GitHub/Qtrinet && cp work/n2ac/table_200k.py work/n2ac/agrege_200k.py journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/ 2>/dev/null;
- cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md") t = p.read_text(encoding="utf-8") vieux = """-
- N2 — MANDAT DE NUIT : R1.2 À 1 024 OCTETS ET LA FENÊTRE SUR LE MÉLANGE DE PRODUCTION (JUSQU'À 08 h)" && git log --oneline -1; echo "=== run ==="; tail -2 work/n
- cd /home/stephane/GitHub/Qtrinet && cp work/n2ac/*.py work/n2ac/*.sh journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/ && python3 -c " import pathlib,
- cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib, re p = pathlib.Path("docs/pilotage/en-cours.md") t = p.read_text(encoding="utf-8") md = len
- cd /home/stephane/GitHub/Qtrinet && git commit -q -- reports/rapport-n2-fenetre.md reports/n2-fenetre.json docs/pilotage/en-cours.md -F - <<'MSG' FENÊTRE — LE C
- cd /home/stephane/GitHub/Qtrinet && git commit -q -F - -- reports/rapport-n2-fenetre.md reports/n2-fenetre.json docs/pilotage/en-cours.md <<'MSG' FENÊTRE — LE C
- cd /home/stephane/GitHub/Qtrinet && git add reports/rapport-n2-r12-2048.md reports/n2-r12-2048.json docs/pilotage/en-cours.md && git commit -q -F - -- reports/r
- cd /home/stephane/GitHub/Qtrinet && cp work/n2ac/*.py work/n2ac/*.sh journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/ 2>/dev/null; python3 -c " impor
- cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib, re p = pathlib.Path("docs/pilotage/en-cours.md") t = p.read_text(encoding="utf-8") md = len
- cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib q = pathlib.Path("docs/pilotage/en-cours.md") s = q.read_text(encoding="utf-8") s = s.replac
- cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib q = pathlib.Path("docs/pilotage/en-cours.md") s = q.read_text(encoding="utf-8") s = s.replac
- cd /home/stephane/GitHub/Qtrinet && git add docs/pilotage/en-cours.md && git commit -q -F - -- docs/pilotage/en-cours.md <<'MSG' ÉTAT — LA SESSION N2 REPREND : 
- cd /home/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -2; python3 tools/verifie_en_cours.py 2>&1 | tail -1; for i in $(seq 1 20);
- cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib, re p = pathlib.Path("docs/pilotage/en-cours.md") t = p.read_text(encoding="utf-8") vieux = 
- cd /home/stephane/GitHub/Qtrinet && cp work/n2ac/distiller_natif.py work/n2ac/chaine_kd.sh journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/ && python
- cd /home/stephane/GitHub/Qtrinet && for i in $(seq 1 20); do [ -f .git/index.lock ] || break; sleep 4; done; git add reports/rapport-n2-production-fenetre.md re
- cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md") t = p.read_text(encoding="utf-8") t = t.replac
- cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md") t = p.read_text(encoding="utf-8") t = t.replac
- cd /home/stephane/GitHub/Qtrinet && for i in $(seq 1 20); do [ -f .git/index.lock ] || break; sleep 4; done; git add journal/sessions/0733c5bb-f90b-4f58-9241-33
- cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md") t = p.read_text(encoding="utf-8") t = t.replac
- cd /home/stephane/GitHub/Qtrinet && git add docs/pilotage/en-cours.md && git commit -q -F - -- docs/pilotage/en-cours.md <<'MSG' ÉTAT — T0 REVENU À 3 994 APRÈS 
- cd /home/stephane/GitHub/Qtrinet && for i in $(seq 1 40); do [ -f .git/index.lock ] || break; sleep 4; done; git add docs/pilotage/en-cours.md && git commit -q 
- cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md") t = p.read_text(encoding="utf-8") t = t.replac
- cd /home/stephane/GitHub/Qtrinet && cat >> journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/cloture.md <<'EOF'  ## 04/11 — reprise après le reboot : les de
- cd /home/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -2; for i in $(seq 1 15); do [ -f .git/index.lock ] || break; sleep 4; done
- cd /home/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | grep T0; python3 tools/revue_documentation.py 2>&1 | tail -2; for i in $(seq 1 15);
- cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY' import pathlib p = pathlib.Path("docs/pilotage/en-cours.md") t = p.read_text(encoding="utf-8") vieux = "**r

