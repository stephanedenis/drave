# Session 1e7ef596 — Session status update

> **Journaux :** [le jour](../../2026-11-04/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-04 07:25 |
| Durée | 5.6 h |
| Tours | 12 |
| Messages | 223 |
| Appels d'outils | 401 |
| Fichiers touchés | 15 |
| Commandes | 244 |
| Sous-agents | 0 |
| Commits | 22 |
| Compactages de contexte | 0 |

## Objectifs déclarés

- **create** — Suivre et maintenir la cohérence de docs/ et du pilotage pendant la reprise parallèle : auditer à chaque cycle (revue_documentation, verifier_liens, verifie_backlog, porte-tableaux, verifie_journal, taille_documents, verifie_en_cours), intégrer dans en-cours/roadmap/backlog les faits committés par l
… [207 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — où en est-on?

**Tour 2** — background job bash-12 (bash: uptime ; echo "---REBOOT---" ; last reboot 2>/dev/null | head -4 ; echo "---DISK---" ; df -h /home/stephane/Data13TB | tail -1 ; echo "---REGISTRE---" ; grep -rln "nuit-kd2" --include="*.txt" --include="*.md" --include="*.json" . 2>/dev/null | grep -v ".git/" | head) finished [status: completed, exit code: 0]. Read its output with job_output.

**Tour 3** — fais des tâches courtes aprèes avoir analysé l'état de chacune des sessions qui ont été interrompues par le redémarrage.

**Tour 4** — la machine est stabilisée. tu peux reprentre tous les chantiers en parallèle. dis-moi si je dois démarer d'autres sessions dsh

**Tour 5** — les sessions ont été démarées et tu dois faire un suivi de tout le dossier docs pourt maintenir la cohérence de la documentation et du pilotage

**Tour 6** — <goal_round> Objective: "Suivre et maintenir la cohérence de docs/ et du pilotage pendant la reprise parallèle : auditer à chaque cycle (revue_documentation, verifier_liens, verifie_backlog, porte-tableaux, verifie_journal, taille_documents, verifie_en_cours), intégrer dans en-cours/roadmap/backlog les faits committés par les sessions N2/S/L, corriger les incohérences (compteurs, dates, liens, man … [677 caractères tronqués]

**Tour 7** — <goal_round> Objective: "Suivre et maintenir la cohérence de docs/ et du pilotage pendant la reprise parallèle : auditer à chaque cycle (revue_documentation, verifier_liens, verifie_backlog, porte-tableaux, verifie_journal, taille_documents, verifie_en_cours), intégrer dans en-cours/roadmap/backlog les faits committés par les sessions N2/S/L, corriger les incohérences (compteurs, dates, liens, man … [677 caractères tronqués]

**Tour 8** — <goal_round> Objective: "Suivre et maintenir la cohérence de docs/ et du pilotage pendant la reprise parallèle : auditer à chaque cycle (revue_documentation, verifier_liens, verifie_backlog, porte-tableaux, verifie_journal, taille_documents, verifie_en_cours), intégrer dans en-cours/roadmap/backlog les faits committés par les sessions N2/S/L, corriger les incohérences (compteurs, dates, liens, man … [677 caractères tronqués]

**Tour 9** — <goal_round> Objective: "Suivre et maintenir la cohérence de docs/ et du pilotage pendant la reprise parallèle : auditer à chaque cycle (revue_documentation, verifier_liens, verifie_backlog, porte-tableaux, verifie_journal, taille_documents, verifie_en_cours), intégrer dans en-cours/roadmap/backlog les faits committés par les sessions N2/S/L, corriger les incohérences (compteurs, dates, liens, man … [677 caractères tronqués]

**Tour 10** — <goal_round> Objective: "Suivre et maintenir la cohérence de docs/ et du pilotage pendant la reprise parallèle : auditer à chaque cycle (revue_documentation, verifier_liens, verifie_backlog, porte-tableaux, verifie_journal, taille_documents, verifie_en_cours), intégrer dans en-cours/roadmap/backlog les faits committés par les sessions N2/S/L, corriger les incohérences (compteurs, dates, liens, man … [677 caractères tronqués]

**Tour 11** — <goal_round> Objective: "Suivre et maintenir la cohérence de docs/ et du pilotage pendant la reprise parallèle : auditer à chaque cycle (revue_documentation, verifier_liens, verifie_backlog, porte-tableaux, verifie_journal, taille_documents, verifie_en_cours), intégrer dans en-cours/roadmap/backlog les faits committés par les sessions N2/S/L, corriger les incohérences (compteurs, dates, liens, man … [677 caractères tronqués]

**Tour 12** — <goal_round> Objective: "Suivre et maintenir la cohérence de docs/ et du pilotage pendant la reprise parallèle : auditer à chaque cycle (revue_documentation, verifier_liens, verifie_backlog, porte-tableaux, verifie_journal, taille_documents, verifie_en_cours), intégrer dans en-cours/roadmap/backlog les faits committés par les sessions N2/S/L, corriger les incohérences (compteurs, dates, liens, man … [677 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — où en est-on?

*40 appels d'outils.* Actions notables :

- read
- bash — Show recent commits and working tree status
- bash — Show current date and session status
- bash — Check GPU usage and running processes
- bash — List commits since midday and diff stats
- bash — Check journal directories and night plan files
- bash — Show plan-travail section headings
- bash — Show uncommitted state file changes
- bash — Find files modified after the last commit
- bash — List newest session and report files
- bash — Read the night plan section
- bash — Check HEAD state file and kd2 artifacts
- bash — Check uptime, reboot history, disk and registry
- bash — Read headers of uncommitted N2 reports
- … et 24 autres

**Synthèse produite :**

⏵ Bilan de la nuit interrompue et de l'état du dépôt

**Au 04/11, 07 h 55 — la nuit a été coupée net.**

- **Dernier commit** : hier **18 h 48** (`8854fe8f`, S v6). **Reboot à 19 h 33** : depuis, **GPU au repos** (0 %, 1 MiB), **aucun run**, 12 h sans calcul. Les acquis de la veille sont committés ; seuls les WIP de 19 h 18 ne le sont pas.
- **Les acquis** (fiche + JSON + commit) :
  - **N2** : la **fenêtre 1 024** est la recette de production — 60 k pas : **2,9121** en domaine, **2,3911 / 2,3522** au grand corpus (**< 2,5**) ; capacité **saturée** (2,8662 à 34,3 M) ; distillation native **+0,10** à budget égal ; le contrôle depuis zéro (3,3184 → 2,9213) sépare ce que la recette donne (la longueur) de ce que l'init donne (le niveau).
  - **S** : v6 — gold **60**, **60/60** types, **142/142** rôles, 50/50 compléments, **55 tests** ; traduction **14/14** ; page `/paragraphes`.
  - **L/B13** : **140/140** ; gold 432 **true** (acte 0,9954) ; DRVM/native **114/114 + 5/5** ; sto **5/5** ; fusion réparée **0,9309/0,8226/0,8784/0,9954** ; fenêtre **non discriminante**.
  - **D** : OCR clos.
- **Ce qui est cassé / risqué** :
  - **Deux runs N2 tués sans checkpoint** : `kd2` **8 250/30 000** pas et `rope2048` **3 350/20 000**. Leurs fiches, écrites à 19 h 18, contiennent des **placeholders** (`{{K128}}`, `{{LECTUREKD2}}`, `{{W128}}`) : **non publiables en l'état**.
  - **Index réparé à l'instant** : le piège d'index alterné du runbook § 9 s'était reproduit — 5 fichiers S (4 fiches + le SVG) étaient *staged en suppression* alors qu'ils sont sur disque. `git read-tree HEAD` les a rétablis. Restent **13 entrées** : journal régénéré (07 h 17), WIP N2, WIP Pensée (`store.py`, test BFS), 3 données S dans le sous-module, 2 JSON non suivis.
  - **La dernière passe de portes est antérieure aux commits du soir** (82, 80/2) : à rejouer.
  - **L'état est daté 13 h 45** et croit `kd2` en cours (« fin ~22 h 15 ») ; aucune session n'a rouvert depuis le reboot ; les claims de la nuit sont périmés.
- **La suite** : (1) passe de portes sur machine au repos + bilan de 08 h ; (2) état au 04/11 et mandats rouverts ; (3) relancer `kd2` et `rope2048` (≈ 4 h et ≈ 5 h 40 depuis zéro) ou figer les fiches sans les sections à trous ; (4) la file : **porte propre N2 (0,29)**, **S validation `/paragraphes`**, **B13 gold 200+**.

**Ma recommandation** : la passe d'abord (cartes libres, elle valide les commits du soir), puis la relance des deux runs ce matin ; pendant qu'ils tournent, l'état et le
… [43 caractères tronqués]

### Tour 2 — background job bash-12 (bash: uptime ; echo "---REBOOT---" ; last reboot 2>/dev/null | head -4 ; echo "---DISK---" ; df  … [254 caractères tronqués]

*6 appels d'outils.* Actions notables :

- job_output
- bash — Read gate script header and gate protocol
- bash — Read pass precautions and existing log dirs
- bash — Confirm machine idle and pass directory naming
- bash — Run complete gate pass on idle machine

**Synthèse produite :**

⏵ Passe de portes lancée sur machine au repos (82 portes)

Le job de recherche a confirmé que `nuit-kd2` ne vit que là où on l'attend : `work/ressources.json`, `work/msg-claims.txt`, `docs/pilotage/plan-travail.md` (et un ancien rapport de session). Rien à corriger de ce côté.

J'ai lancé la **passe complète** sur la machine au repos (GPU à 0 %, aucun run) :

- **Commande** : `JOURNAUX=work/portes/passe-1104-08h00 bash tools/toutes-les-portes.sh` — job `bash-40`, 82 portes, borne 1 800 s.
- **Pourquoi** : la dernière passe (82, 80/2) est antérieure aux commits du soir (S v6, N2, L) ; il faut le verdict avant de conclure quoi que ce soit.
- **Lecture** : `awk '$2 != 0' work/portes/passe-1104-08h00/registre.txt`, puis comparaison avec les rouges tolérées de [`references-non-regression.md`](docs/pilotage/references-non-regression.md). Durée observée : 1 h 30 – 2 h.
- **Pendant la passe** : je ne touche pas au dépôt (sinon le verdict est faussé). Ensuite : état au 04/11 + commit, puis les deux runs N2 (`kd2` ≈ 4 h, `rope2048` ≈ 5 h 40).

Si tu préfères les runs **avant** la passe, dis-le et je coupe `bash-40` — sinon je te donne le verdict dès qu'elle finit.

### Tour 3 — fais des tâches courtes aprèes avoir analysé l'état de chacune des sessions qui ont été interrompues par le redémarrage.

*127 appels d'outils.* Actions notables :

- job_kill
- read
- bash — Verify pass stopped and read claims tool usage
- bash — Inspect S submodule data and tests
- bash — Inspect Pensée window-gate test
- bash — Read N2 report WIP sections
- bash — Inspect commit hooks and state check
- bash — Read S JSON and locate Pensée store tests
- bash — Read claims usage and S test command
- bash — Read state-check index logic
- bash — Find S bank export command
- bash — Inspect store fix and Pensée test style
- bash — Read S untracked validation data
- bash — Read S export flow and data writers
- … et 105 autres

**Synthèse produite :**

⏵ Bilan par session, tâches courtes exécutées et deux commits de reprise

**Analyse des quatre sessions interrompues par le reboot du 03/11 à 19 h 33**, puis les tâches courtes faites.

| session | état au reboot | tâche courte faite |
|---|---|---|
| **Hub `536cd5d6`** | dernier commit 18 h 48 ; état daté 13 h 45 ; index périmé (5 fichiers S *staged en suppression*, journal en retard) ; 4 claims de nuit | index réparé (`git read-tree HEAD`) ; claims libérés ; état au 04/11 ; plan de reprise `1e7ef596` |
| **S `29ad180d`** | v6 committée à 18 h 48 ; **8 verdicts de référents** (a001–a003) + **8 verdicts banque** (p003, c010, c066, c067) non committés ; sous-module sale | sous-module **`7ccc60f`** ; **55/55 tests** ; banque régénérée **84/67** (SHA `3ca1ac20…`, avant 81/65) ; manifeste committé |
| **Pensée `e181ce02`** | B13 **140/140**, gold **432**, DRVM committés ; WIP `store.py` FIFO + qualifier BFS 500 ; JSON 500 non suivi mais cité par la fiche | **fix FIFO + 3 tests** (l'ancien code échoue **2/3**) ; qualifier archivé en patch (`work/pensee/`) ; JSON 500 committé |
| **N2 `0733c5bb`** | phase close à 18 h 30 ; `kd2` **8 250/30 000**, `rope2048` **3 350/20 000**, tués à 19 h 33 **sans checkpoint** ; fiches à placeholders | fiches passées à **« run interrompu, non mesuré »** avec les chiffres exacts ; claim `nuit-kd2` libéré |

**Commits** : `59329788` (intégration, 23 fichiers) et `0582a6e1` (mandats alignés sur l'état). Sous-module S : `7ccc60f`.

**Contrôles** : revue de documentation ✅ tout passe · `en-cours` **1 627 mots** ✅ · T0 **3 997 / 4 000** ✅ · journal **1 943 liens** ✅ · 4 mandats en pause + le hub actif · aucun claim · arbre propre.

**Ce qui reste (pas court)** :
- **Passe de portes** : la dernière complète est le 03/11 11 h 30 (82, 80/2), avant les commits du soir ; celle du 04/11 a été arrêtée à 08 h 40 pour faire ces tâches → à relancer (1 h 30–2 h).
- **N2** : `kd2` ≈ 4 h et `rope2048` ≈ 5 h 40, **depuis zéro** (aucun checkpoint) ; la question de la distillation à 30 000 pas reste ouverte.
- Ensuite : N2 porte propre (0,29) ; S validation `/paragraphes` + rétro-traduction API ; Pensée T132/T133 et gold 200+.

Rien n'est perdu : l'interruption est écrite avec ses chiffres, les validations S sont dans le sous-module, le fix FIFO a son contrôle, et l'état du 04/11 est reprenable.

### Tour 4 — la machine est stabilisée. tu peux reprentre tous les chantiers en parallèle. dis-moi si je dois démarer d'autres sessio … [6 caractères tronqués]

*31 appels d'outils.* Actions notables :

- bash — Search run commands in shell scripts
- bash — Search session transcript for run command
- bash — Read run script arguments
- bash — Read kd2 and rope2048 chain scripts
- bash — Find the Python environment used by the runs
- bash — Verify GPU Python environment and corpora
- bash — Claim GPUs for relaunched N2 runs
- bash — Relaunch both N2 runs and verify start
- bash — Check run processes and launch logs
- bash — Kill racy rope launch and restart cleanly
- bash — Check run processes, logs and GPU allocation
- bash — Monitor run progress after one minute
- job_output
- edit `docs/pilotage/en-cours.md`
- … et 17 autres

**Synthèse produite :**

⏵ Trois sessions à ouvrir, les deux runs N2 déjà relancés

**Oui — trois sessions, pas quatre.** Le hub reste cette session ; N2, S et L reprennent chacune dans son terminal. Pas de 4e pour l'instant : **A2.6 attend les GPU** (les deux sont pris par N2 jusqu'à ~15 h) et **R0.7 est dans le mandat de L**.

**À lancer (un terminal par ligne) :**
```bash
dsh --profile dsh-tui --resume 0733c5bb-f90b-4f58-9241-3364fa32e46c   # N2 — GPU
dsh --profile dsh-tui --resume 29ad180d-38a5-4481-a9a7-ec6ab31c895f   # S  — CPU
dsh --profile dsh-tui --resume e181ce02-cd50-488a-a6be-e84b79d40dcc   # L/Pensée — CPU+API
```

**Prompt à coller (le même, adapté) :**
> Tu es la session <rôle>. Lis `AGENTS.md`, `docs/pilotage/en-cours.md` (état du 04/11, 09 h 35) et seulement le document de ta tâche. Reprends `journal/sessions/<id>/plan.md`. La machine est stable ; les runs N2 sont **déjà relancés** (kd2 gpu0, rope2048 gpu1) — **ne les relance pas**. Exécute la prochaine action de ton plan ; un fait = mesure + contrôle + fiche + ligne d'état (proposée au hub) + commit (`git add` explicite). Ne touche pas `en-cours`/`roadmap`/`AGENTS` sans le hub.

- **N2** : surveille `work/n2ac/kd2-mix512-30k.log` et `rope2048-20k.log` ; à la fin, remplis les §5/§6 des deux fiches et committe.
- **S** : poursuis la validation `/paragraphes` (a001–a003 faits) ; banque **84/67**, **55/55 tests**.
- **L** : le **fix FIFO** est testé ; reprends **T132/T133** et le **gold 200+** ; le qualifier fenêtre attend l'API (pas de serveur local).

**Déjà fait par le hub :**
- **kd2** sur gpu0 : 350 pas en 163 s (~0,47 s/pas), GPU à 100 % → fin estimée **~13 h 25**.
- **rope2048** sur gpu1 : 250 pas en 254 s (~1,0 s/pas) → fin estimée **~15 h 10**.
- Claim `n2-jour` (gpu0+gpu1, cpu0 12, ram 60) ; anciens logs préservés en `.interrompu.log` ; état et plan N2 committés (`55243f42`).
- Une session vide `aeafe951` (0 tour, ouverte à 09:25) est apparue : sans plan, elle ne compte pas — tu peux la fermer.

**La passe de portes** : elle attend la fin des runs (règle §11 — une passe et une mesure GPU ne cohabitent pas). Dernière complète : 03/11 11 h 30. Je la lance vers **15 h 15**, ou sur gpu1 avec la dérogation si tu veux le verdict plus tôt — mais les portes de temps seront bruitées.

**Le hub** : je surveille les deux runs, je tiens l'état, je lance la passe à la fin et j'intègre les résultats. Dis-moi si tu ouvres les trois sessions ou si tu préfères que je pousse S et L par sous-agents à la place.

### Tour 5 — les sessions ont été démarées et tu dois faire un suivi de tout le dossier docs pourt maintenir la cohérence de la docum … [23 caractères tronqués]

*82 appels d'outils.* Actions notables :

- bash — Check sessions, recent commits and tree
- bash — Run documentation review and state freshness
- bash — Check runs and list doc tools
- bash — Inspect uncommitted state and worktree changes
- bash — List active sessions and new session plan
- bash — Inspect recent session commit contents
- bash — Full status, N3 tools and gate count
- bash — Read N3 report verdict and proposed integration
- bash — Inspect current state structure and counters
- todo_write
- bash — Inspect staged and unstaged state changes
- bash — Read current full state
- bash — Read B13 state-line updates in recent commits
- bash — Read N3 report conclusion and backlog page
- … et 54 autres

**Synthèse produite :**

⏵ Audit docs terminé, N3 intégré, suivi continu armé

**Audit de `docs/` — tout passe, et les corrections sont committées.**

- **Revue** : `revue_documentation` ✅ (classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation) — **608 fiches, 693 JSON, 120 docs, 83 portes**.
- **Liens** : 2 888 liens relatifs ✅ (le lien mort de la fiche N3 est corrigé) · **tableaux** : 1 631 fichiers ✅ · **journal** : 41 jours, 119 sessions, 1 968 liens ✅ · **schémas** : 67 SVG ✅.
- **Budget** : `en-cours` **1 566 mots**, **T0 3 936 / 4 000** ✅ · **backlog** : 37 fiches, 43 arêtes, **frontière 3** (N3 en est sorti) ✅ · **mandats** : `sessions.py --check` sans erreur.

**Intégré** :
- **N3 clos** : backlog `partiel` → **`mesurée`** (étapes 3/4 ✅, fiche `n3-inventaire`), roadmap **N3 ✅ couvert**, **83e porte** `porte-n3-inventaire` dans les références, **§ 12** du runbook (reprise et suivi docs).
- **État** : S **61/61** types, **144/144** rôles, **56 tests** ; B13 **146/146** (défaut conditionnel) ; N2/S/L **actifs**, hub actif, 536c en pause ; N3 dans « Ce qui est en cours ».
- **Commits** : `d390136a` (le commit B13 a emporté l'index : N3, backlog, roadmap, références, § 12, plans) et `29122912` (état : B13 146/146, compteurs 608/693, heure corrigée).

**Deux constats** :
- **Écritures concurrentes** : les sessions écrivent et committent `en-cours` alors que le hub doit tenir la plume ; le commit B13 a ainsi emporté l'index préparé. J'ai repris le fil — mais il faut leur rappeler de **proposer** leur ligne, pas d'écrire l'état.
- **Horloge** : les sessions écrivent « 13 h 50 » à **11 h 57** (dérive ~+1 h 50) ; l'état est remis à l'heure locale réelle (12 h 02). À surveiller à chaque cycle.

**Ce qui reste** (WIP de leurs sessions, pas du hub) : B13 `seuil parallèle` (fiche/JSON non committés), S `rapport-s-paragraphes.md` ; les runs `kd2` (12 050+/30 000, log bufferisé) et `rope2048` (4 600/20 000, ~2 s/pas) tournent à 99–100 % des GPU ; la passe complète après.

**Le suivi est armé** (goal) : à chaque cycle, j'audite les outils, j'intègre les faits **committés** des sessions, je corrige compteurs/dates/liens/mandats et je committe. Je continue tant que les sessions n'ont pas clos leurs faits et que la passe n'est pas passée.

### Tour 6 — <goal_round> Objective: "Suivre et maintenir la cohérence de docs/ et du pilotage pendant la reprise parallèle : auditer … [957 caractères tronqués]

*13 appels d'outils.* Actions notables :

- bash — Snapshot commits, tree and sessions
- bash — Run review, state and budget checks
- bash — Run links, backlog, journal and table gates
- bash — Check run progress and GPU load
- bash — Update N2 progress and ETA in state
- bash — Commit corrected N2 progress in state
- bash — Inspect concurrent commit and state inclusion
- bash — Check HEAD state B13 fact and commit diff
- bash — Inspect worktree state diff and counts
- bash — Update state with B13 147 fact and verify
- bash — Commit only the updated state
- bash — Verify cycle commit and state checks
- bash — Verify links, journal, backlog and runs

**Synthèse produite :**

⏵ Cycle 1 : B13 147/147 intégré, état et docs verts, suivi actif

**Audit du cycle — tout est vert** : revue ✅ (**609 fiches, 695 JSON, 120 docs, 83 portes**), **2 904 liens** ✅, backlog **frontière 3** (A2.6, N2, N4) ✅, journal **1 968 liens** ✅, tableaux ✅, `en-cours` **1 590 mots** ✅, **T0 3 960 / 4 000** ✅.

**Intégré** :
- **B13 147/147** — le seuil du parallèle : la confiance plafonne à **0,9326** sous le max **0,9389** ; fiche [`seuil parallèle`](../../reports/rapport-pensee-seuil-parallele.md) citée ; le fait est dans `25d631fe`, l'état dans **`b58cd52f`**.
- **N2** — progression corrigée : `kd2` **~19 400/30 000** (le log s'arrête à 12 050 : sortie **bufferisée**, GPU à 99 %), `rope2048` **4 800/20 000** (≈2 s/pas, ralenti par kd2) ; ETA **~13 h 30 / ~19–20 h** (l'ancienne, 15 h 10, était fausse).
- Heure locale corrigée (**12 h 09** ; les sessions écrivaient 14 h 05) ; compteurs **609/695**.

**Ce qui reste** (aux sessions, pas au hub) : B13 troisième passe (`432 run3`, `troisieme-passe` non committés), S `rapport-s-paragraphes.md`, les journaux dérivés en cours de régénération. Les runs tournent (GPU 99–100 %) ; la **passe complète** attend leur fin.

**Le goal reste actif** : je ré-audite et j'intègre à chaque cycle ; il sera complet quand les sessions auront clos leurs faits et que la passe complète sera passée.

### Tour 7 — <goal_round> Objective: "Suivre et maintenir la cohérence de docs/ et du pilotage pendant la reprise parallèle : auditer … [957 caractères tronqués]

*17 appels d'outils.* Actions notables :

- bash — Snapshot commits, tree and sessions
- bash — Run review, state and budget checks
- bash — Run links, backlog, journal and table gates
- bash — Check state facts, time and runs
- bash — Check and regenerate reports catalog
- bash — Update state time and stage catalog
- bash — Commit regenerated reports catalog and state
- bash — Read third-pass result and current status
- bash — Integrate B13 third pass into state and verify
- bash — Commit only the state with third-pass fact
- bash — Verify cycle commits and checks
- bash — Verify links, journal, backlog and runs
- bash — Inspect session state update
- bash — Correct state time and verify counters
- … et 3 autres

**Synthèse produite :**

⏵ Cycle 2 clos : catalogue 606, B13 148/148, compteurs 610/696, état vert

**Cycle 2 — trois commits, docs verts.**

- **Catalogue** : il était périmé de 10 fiches (596) ; régénéré à **606** et committé (`625271c8`) — N3, S, B13 (élision, quatre modes, run2, défaut, défaut conditionnel, seuil, troisième passe).
- **B13 148/148** : la **troisième passe** donne exactement le run 2 (POS **0,9389**, syntagmes **0,8241**, tête **0,8797**, refus **0**) — variance **nulle** ; le `parallele` passe de **0,9326** à **0,9389** avec la clé. Intégré à l'état (`7b11a93f`), puis compteurs/heure (`70c9df7e`).
- **État** : **610 fiches / 696 JSON / 120 docs / 83 portes** ; `en-cours` **1 603 mots** ; **T0 3 973 / 4 000** ; **2 920 liens** ✅ ; backlog **frontière 3** ✅ ; journal **1 968 liens** ✅ ; tableaux ✅ ; heure remise à **12 h 18** (les sessions écrivaient 14 h 15 — dérive d'horloge persistante).

**WIP de leurs sessions** (le hub les intégrera aux prochains commits) : B13 **DRVM N0/N1** (`pensee-drvm-n01.json`, `rapport-drvm-n01.md`, `tools/drvm.py`), S `rapport-s-paragraphes.md`, `reports/pensee-quatre-modes.json`. Les runs tournent : `kd2` (log bufferisé, ~19 400 estimé), `rope2048` **5 100/20 000** (≈2 s/pas), GPU 99–100 %.

**Le goal reste actif** : les sessions n'ont pas clos leurs faits et la passe complète n'est pas passée. Je ré-audite et j'intègre au cycle suivant.

### Tour 8 — <goal_round> Objective: "Suivre et maintenir la cohérence de docs/ et du pilotage pendant la reprise parallèle : auditer … [957 caractères tronqués]

*21 appels d'outils.* Actions notables :

- bash — Snapshot commits, tree and sessions
- bash — Run review, state and budget checks
- bash — Run links, backlog, journal and table gates
- bash — Check state facts, time and runs
- bash — Inspect roadmap B/S rows and S backlog
- bash — List backlog pages and read B narrative
- read
- edit `docs/pilotage/roadmap.md`
- edit `docs/pilotage/roadmap.md`
- edit `docs/pilotage/roadmap.md`
- edit `docs/pilotage/roadmap.md`
- edit `docs/pilotage/roadmap.md`
- edit `docs/pilotage/roadmap.md`
- edit `docs/pilotage/roadmap.md`
- … et 5 autres

**Synthèse produite :**

⏵ Cycle 3 clos : roadmap alignée sur S v7 et B13 148/148, état et docs verts

**Cycle 3 — la roadmap rattrape les faits committés.**

- **Roadmap** : S passe en **v7** (**61/61** types, **144/144** rôles, **56 tests**, le fait divers tranché — la tête du GN arrête le verbe, [fiche](../../reports/rapport-s-fait-divers.md)) ; B13 passe de 140/140 à **148/148** (T0–T148) dans les deux lignes ; N2 porte les **runs `kd2`/`rope2048`** ; R1.2 porte `rope2048` ; l'état B13 daté du 04/11. Commit **`1b4be681`**.
- **État** : heure remise à **12 h 24** (les sessions écrivaient 14 h 15), compteurs **610 fiches / 696 JSON / 120 docs / 83 portes**.
- **Contrôles** : revue ✅ (classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation) ; **2 920 liens** ✅ ; backlog **frontière 3** ✅ ; journal **1 968 liens** ✅ ; tableaux ✅ ; `en-cours` **1 603 mots**, **T0 3 973 / 4 000** ✅.

**WIP de leurs sessions** : B13 **DRVM N0/N1** (`pensee-drvm-n01.json`, `rapport-drvm-n01.md`, `tools/drvm.py`), S `rapport-s-paragraphes.md`, `reports/pensee-quatre-modes.json` — non committés, donc non intégrés.

**Runs** : `kd2` (log bufferisé, ~19 400 estimé), `rope2048` **5 450/20 000** (≈2 s/pas) ; GPU 99–99 %. La passe complète attend leur fin.

**Le goal reste actif** : les sessions n'ont pas clos (DRVM, paragraphes) et la passe n'est pas passée.

### Tour 9 — <goal_round> Objective: "Suivre et maintenir la cohérence de docs/ et du pilotage pendant la reprise parallèle : auditer … [957 caractères tronqués]

*26 appels d'outils.* Actions notables :

- bash — Snapshot commits, tree and sessions
- bash — Run review, state and budget checks
- bash — Run links, backlog, journal and table gates
- bash — Check state facts, time and runs
- bash — Sweep stale facts in docs
- bash — Audit resource claims and mandates
- read
- bash — Update stale B13/S/gate facts in pilotage docs
- bash — Update state time and verify pilotage docs
- bash — Commit pilotage docs alignment
- bash — Verify cycle 4 commits and checks
- bash — Verify links, journal, backlog and runs
- bash — Correct JSON counter and verify
- bash — Commit corrected JSON counter
- … et 8 autres

**Synthèse produite :**

⏵ Cycle 4 : erratum N2 propagé, pilotage aligné, docs verts

**Cycle 4 — un erratum majeur, et la documentation corrigée.**

- **ERratum N2** : le gain de distillation **+0,14–0,18** (et le **+0,10** de la production) venait d'un **poids de tête principale à 1 au lieu de 1/4**. La paire propre donne **−0,030 / −0,009 / −0,004**, dans le bruit ; la §4 de la fiche production est **sous contrôle**, la paire propre (α = 0 / 0,9) tourne. Corrigé dans l'**état**, la **roadmap** (ligne N2) et le **plan-travail** (§ 11) — commits `84c28889` (fait) et `6b0e9c83` (propagation).
- **Pilotage aligné** : `chantiers.md`, `plan-travail.md` et `portes.md` passent à **B13 148/148**, **S v7** (61/61, 144/144, 56 tests), **83 portes** (la 83e, `porte-n3-inventaire`) — commit `d94c3a4b`. Claims : registre cohérent, `n2-jour` actif ; seul avertissement `nvme_raid` 33 Gio.
- **B13 DRVM N0.1 : 149/149** (payload corrompu refusé, le hash manquait) — commit `9593718e`, fiche/JSON désormais committés ; l'état garde **148/148** (dernier fait complet) et sera mis à 149 au prochain cycle.
- **Contrôles** : revue ✅ **611 fiches / 698 JSON / 120 docs / 83 portes** ; **2 928 liens** ✅ ; backlog **frontière 3** ✅ ; journal **1 971 liens** ✅ ; tableaux ✅ ; `en-cours` **1 624 mots**, **T0 3 994 / 4 000** ✅.
- **WIP** : B13 variance (`pensee-variance`, t03), S `rapport-s-paragraphes.md` ; **runs** `kd2` (log bufferisé) et `rope2048` **5 950/20 000** (GPU 100 %).

**Le goal reste actif** : la passe complète attend les runs, et les faits B13 149 / variance et S paragraphes seront intégrés dès leurs commits.

### Tour 10 — <goal_round> Objective: "Suivre et maintenir la cohérence de docs/ et du pilotage pendant la reprise parallèle : auditer … [957 caractères tronqués]

*13 appels d'outils.* Actions notables :

- bash — Snapshot commits, tree and sessions
- bash — Run review, state and budget checks
- bash — Run links, backlog, journal and table gates
- bash — Check state facts, time and runs
- bash — Read DRVM N0.1 verdict and doc counts
- bash — Integrate B13 149 and DRVM N0.1 in pilotage docs
- bash — Commit B13 149 and DRVM N0.1 integration
- bash — Inspect concurrent commit and staged integration
- bash — Check HEAD state for 150 and counters
- bash — Integrate B13 150 variance across pilotage docs
- bash — Commit B13 150 variance integration
- bash — Verify cycle 5 commits and checks
- bash — Verify links, journal, backlog and runs

**Synthèse produite :**

⏵ Cycle 5 : B13 149→150 intégré (DRVM, variance), état et docs verts

**Cycle 5 — la chaîne B13 est intégrée, de 149 à 150.**

- **B13 149/149 — DRVM N0.1** : porte re-jouée sur mini-conteneur, **6/6** ; le lecteur vérifiait le hash du **manifeste** mais pas celui du **payload** — corrigé (`read_drvm(verifier=True)`), le payload corrompu est refusé. Commit `9593718e`, fiche `rapport-drvm-n01` + JSON committés.
- **B13 150/150 — variance à 0,3** : **±0,0074 au pire, 7/7 seuils, refus 0**. Commit `8cea841f` (le commit B13 a emporté l'index : l'intégration 149/DRVM est passée avec lui), puis l'état/roadmap/chantiers/plan-travail à **150/150** (T0–T150) — commit `96c96ae9`.
- **ERratum N2** (rappel) : le +0,10 de distillation était une **repondération** ; la paire propre donne −0,03/−0,01/−0,004 ; propagé dans l'état, la roadmap et le plan-travail (`6b0e9c83`).
- **Contrôles** : revue ✅ **611 fiches / 698 JSON / 120 docs / 83 portes** ; **2 928 liens** ✅ ; backlog **frontière 3** ✅ ; journal **1 971 liens** ✅ ; tableaux ✅ ; `en-cours` **1 628 mots**, **T0 3 998 / 4 000** ✅.

**WIP de leurs sessions** : S `rapport-s-paragraphes.md` (non committé), B13 `pensee-quatre-modes.json` / `bloc_linguistique.py` / `qualifier_quatre_modes.py` ; **runs** `kd2` (log bufferisé) et `rope2048` **6 200/20 000**, GPU 100 %.

**Le goal reste actif** : la passe complète attend la fin des runs, et les faits S paragraphes (et la suite B13) seront intégrés à leurs commits.

### Tour 11 — <goal_round> Objective: "Suivre et maintenir la cohérence de docs/ et du pilotage pendant la reprise parallèle : auditer … [957 caractères tronqués]

*12 appels d'outils.* Actions notables :

- bash — Snapshot commits, tree and sessions
- bash — Run review, state and budget checks
- bash — Run links, backlog, journal and table gates
- bash — Check state facts, time and runs
- bash — Check index, README rows and claim
- read
- bash — Inspect index regeneration diff
- edit `reports/README.md`
- bash — Add variance row and stage catalog updates
- bash — Commit index and readme catalog updates
- bash — Verify cycle 6 commits and checks
- bash — Verify links, journal and runs

**Synthèse produite :**

⏵ Cycle 6 : catalogue 608 fiches, README variance, état 611/699 — docs verts

**Cycle 6 — le catalogue rattrape, le pilotage reste vert.**

- **Catalogue** : `reports/INDEX.md` passe de **606 à 608 fiches** (DRVM N0.1, variance 0,3) et le README courbe reçoit la ligne **variance 150/150** ; commit `34a25a93`.
- **État** : **611 fiches / 699 JSON / 120 docs / 83 portes**, B13 **150/150**, S **v7**, N2 avec l'**erratum** ; T0 **3 998 / 4 000**, `en-cours` **1 628 mots**.
- **Contrôles** : revue ✅ ; **2 932 liens** ✅ ; backlog **frontière 3** ✅ ; journal **1 971 liens** ✅ ; tableaux ✅.
- **Ressources** : le claim `n2-jour` (360 min, créé 09 h 30 → ~15 h 30) sera **plus court que `rope2048`** (~19–20 h) — à étendre par la session N2 ; les GPU sont à 99–100 %.

**WIP de leurs sessions** : B13 pragmatique 130 phrases (`pensee-pragmatique-130.json`, `rapport-pensee-pragmatique-neuronale.md`), `pensee-quatre-modes.json`, `bloc_linguistique.py` ; S `rapport-s-paragraphes.md`. **Runs** : `kd2` (log bufferisé), `rope2048` **6 300/20 000**.

**Le goal reste actif** : les sessions n'ont pas clos (pragmatique, paragraphes) et la passe complète attend la fin des runs.

### Tour 12 — <goal_round> Objective: "Suivre et maintenir la cohérence de docs/ et du pilotage pendant la reprise parallèle : auditer … [957 caractères tronqués]

*13 appels d'outils.* Actions notables :

- bash — Snapshot commits, tree and sessions
- bash — Run review, state and budget checks
- bash — Run links, backlog, journal and table gates
- bash — Check state facts, time and runs
- bash — Extend N2 resource claim for rope ETA
- bash — Trim state B13 history and verify
- bash — Commit trimmed state and extended claim note
- bash — Verify cycle 7 commits and checks
- bash — Verify links, journal, claim and runs
- bash — Check pragmatique fiche and JSON commit status
- bash — Integrate B13 151 pragmatique across docs
- bash — Commit B13 151 pragmatique integration
- bash — Wait for lock and retry pragmatique commit

**Synthèse produite :**

⏵ Verrou git tenu par une session : j'attends puis je retente le commit

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `tools/tests/test_pensee_store.py` | 1 | 0 |
| `reports/rapport-n2-production-fenetre.md` | 0 | 3 |
| `reports/rapport-n2-r12-2048.md` | 0 | 4 |
| `journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md` | 1 | 4 |
| `journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md` | 0 | 2 |
| `journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md` | 0 | 5 |
| `journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md` | 0 | 5 |
| `journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md` | 0 | 5 |
| `docs/pilotage/en-cours.md` | 2 | 60 |
| `reports/rapport-n3-inventaire.md` | 0 | 1 |
| `docs/pilotage/backlog/N3-operations-natives.md` | 0 | 6 |
| `docs/pilotage/roadmap.md` | 0 | 10 |
| `docs/pilotage/references-non-regression.md` | 0 | 3 |
| `docs/pilotage/plan-travail.md` | 0 | 1 |
| `reports/README.md` | 0 | 1 |

### Commandes exécutées (échantillon)

- **T1** Show recent commits and working tree status
- **T1** Show current date and session status
- **T1** Check GPU usage and running processes
- **T1** List commits since midday and diff stats
- **T1** Check journal directories and night plan files
- **T1** Show plan-travail section headings
- **T1** Show uncommitted state file changes
- **T1** Find files modified after the last commit
- **T1** List newest session and report files
- **T1** Read the night plan section
- **T1** Check HEAD state file and kd2 artifacts
- **T1** Check uptime, reboot history, disk and registry
- **T1** Read headers of uncommitted N2 reports
- **T1** Read resource claims and N2 JSON files
- **T1** Summarize working tree state
- **T1** Inspect uncommitted code and report diffs
- **T1** Show non-worktree status and check missing files
- **T1** Inspect last commit and kd2 artifacts
- **T1** Show tails of interrupted run logs
- **T1** Check for checkpoints from interrupted runs
- **T1** Find the from-scratch control in the N2 report
- **T1** Read night run queue files
- **T1** Check run starts and kd2 artifacts
- **T1** Check provenance of uncommitted code changes
- **T1** Check WIP store fix and window gate JSON
- **T1** Check state dates and gate counter
- **T1** Check reflog and index modification time
- **T1** Locate S reports and inspect submodule state
- **T1** Check whether S files were in last commit
- **T1** Inspect unstaged journal changes
- **T1** Inspect staged journal changes
- **T1** Read reboot recovery runbook
- **T1** Check session environment and tool options
- **T1** Resync index from HEAD and show status
- **T1** Verify submodule pointer and untracked artifacts
- **T1** Compare manifest versions
- **T2** Read gate script header and gate protocol
- **T2** Read pass precautions and existing log dirs
- **T2** Confirm machine idle and pass directory naming
- **T2** Run complete gate pass on idle machine
- … et 204 autres

## 4. Mesures et résultats marquants

- **T1** `0, Quadro RTX 5000, 0 %, 1 MiB, 16384 MiB`
- **T1** `1, Quadro RTX 5000, 0 %, 1 MiB, 16384 MiB`
- **T1** `-- **Fait** : types **60/60**, rôles **142/142** ; **corpus réel** 8,5 %/65,5 % ; **banque partielle** 142/71, 81/65 ; **arbre** 99 à ≥3, **référents** 294/371, **traduction** 14/14 ; **page `/paragra`
- **T1** `+- **Fait** : types **60/60**, rôles **142/142** ; **corpus réel** 8,5 %/65,5 % ; **banque partielle** 142/71, 81/65 ; **arbre** 99 à ≥3, **référents** 294/371, **traduction** 14/14 ; **page `/paragra`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `+| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v6** : h050, h053 et « si fort que » **fermés**, gold **60** (vague 5) ; **60/60** types, **142/142** `
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `encore** (`kd2-mix512-30k`, les deux GPU à 100 %, fin vers 22 h 40). **S** a repris à 13 h 55 sur`
- **T1** `/dev/mapper/system-root   11T  9,0T  1,9T  83% /home/stephane/Data13TB`
- **T1** `[still running after 60000ms; moved to background job bash-12]`
- **T1** `> à **octets ajoutés constants** (61,4 Mo, le budget de N2.ac), les trois fenêtres écrasent N2.ac`
- **T1** `> seulement). En poussant la fenêtre 1 024 à **30 000 pas (307 Mo)**, le modèle de production`
- **T1** `> atteint **2,9121** en domaine à 128 octets (60 000 pas, 552 Mo), **2,5276** à 1 000, **2,4761** à`
- **T1** `> à fenêtre 128 (200 k pas, 205 Mo) donne 3,1591 à 128 et **8,2262** à 1 000 : la fenêtre n'est pas`
- **T1** `(61,4 Mo, le budget même de N2.ac) affiner le modèle de production avec **RoPE et une fenêtre`
- **T1** `de 200 000 pas avec 60 % de son compute. Trois questions restaient :`
- **T1** `| `+ RoPE 512` | 512 | 15 000 | 61,4 Mo | `mix-60k` (N2.ac) |`
- **T1** `| `+ RoPE 1 024` | 1 024 | 7 500 | 61,4 Mo | `mix-60k` (N2.ac) |`
- **T1** `| **`+ RoPE 2 048`** | 2 048 | 3 750 | 61,4 Mo | `mix-60k` (N2.ac) |`
- **T1** `| **`30 000 pas`** | 1 024 | +22 500 | +184 Mo | `mix1024-7.5k` |`
- **T1** `| **`depuis zéro`** | 512 | 15 000 | 61,4 Mo | `init-figee` (aléatoire) |`
- **T1** `> **octets constants** (20,5 Mo vus sur `data/wiki_fr`), la fenêtre entraînée paie jusqu'à`
- **T1** `| fenêtre 256 | 128 | 20 000 | 20,5 Mo | `base-wiki-45m` |`
- **T1** `| fenêtre 512 | 512 | 5 000 | 20,5 Mo | `base-wiki-45m` |`
- **T1** `| fenêtre 1 024 | 1 024 | 2 500 | 20,5 Mo | `base-wiki-45m` |`
- **T1** `| **fenêtre 2 048** | 2 048 | 1 250 | 20,5 Mo | `base-wiki-45m` |`
- **T1** `| **fenêtre 1 024, 20 k pas** | 1 024 | 20 000 | 164 Mo | `base-wiki-45m` (puis suite) |`
- **T1** `@@ -173,6 +173,19 @@ constant, l'élève voit ~26 Mo au lieu de 33 (≈ −0,02 de PPL), le gain net`
- **T1** `+(122 Mo), même init `mix-60k` :`
- **T1** `+| affinage dur, 15 000 pas | 61 Mo | 3,1588 | 2,9096 | 2,8018 | 2,7607 | 5,5247 | 7,0507 | 7,9023 |`
- **T1** `+| distillé, 15 000 pas | 61 Mo | 3,0550 | 2,8062 | 2,7015 | 2,6601 | 5,4309 | 6,7639 | 7,3816 |`
- **T1** `+| **distillé, 30 000 pas** | **122 Mo** | {{K128}} | {{K512}} | {{K1000}} | {{K2000}} | {{KLIT}} | {{KEN}} | {{KWT}} |`
- **T1** `+## 6. Le complément 2 048 « mêmes pas » : 20 000 pas, 328 Mo`
- **T1** `+fois plus d'octets** : 328 Mo contre 164) :`
- **T1** `+| fenêtre 1 024 | 164 Mo | 2,9955 | 2,7201 | 2,6256 | 2,5757 | 2,5429 |`
- **T1** `+| **fenêtre 2 048** | **328 Mo** | {{W128}} | {{W512}} | {{W1000}} | {{W2000}} | {{W4000}} |`
- **T1** `h050, h053 et le « si fort que » (l'intensif si + le que de conséquence) sont corrigés ; « demeure » et « crier » entrent au lexique. Le holdout gagne la vague 5 h056-h060 : 60/60 types, 142/142 rôles`
- **T1** `38-| **`+ RoPE 2 048`** | 2 048 | 3 750 | 61,4 Mo | `mix-60k` (N2.ac) |`
- **T1** `39-| **`30 000 pas`** | 1 024 | +22 500 | +184 Mo | `mix1024-7.5k` |`
- **T1** `40:| **`depuis zéro`** | 512 | 15 000 | 61,4 Mo | `init-figee` (aléatoire) |`
- **T1** `46-| **N2.ac** (témoin) | 61 Mo | 3,4902 | 3,5169 | 7,9201 | 12,4065 | 6,0283 | 8,3352 | 9,0525 |`
- **T1** `47-| 200 k × 128 (témoin) | 205 Mo | 3,1591 | 3,6577 | 8,2262 | 12,8723 | 5,6056 | 7,2770 | 8,0018 |`
- **T1** `48-| **+ RoPE 512** | 123 Mo | **3,1588** | **2,9096** | 2,8018 | 2,7607 | **5,5247** | **7,0507** | **7,9023** |`
- **T1** `128-Même recette (RoPE, seq 512, **61,4 Mo**) et **même budget d'octets ajoutés**, mais départ depuis`
- **T1** `131-| départ (61,4 Mo à 512) | octets totaux | 128 | 512 | 1 000 | 2 000 | litt. | angl. | wt2 |`
- **T1** `133-| **N2.ac** (témoin) | 61 Mo | 3,4902 | 3,5169 | 7,9201 | 12,4065 | 6,0283 | 8,3352 | 9,0525 |`
- **T1** `134:| **depuis zéro** | 61 Mo | 3,3184 | 3,0709 | 2,9588 | 2,9213 | 5,7295 | 7,6921 | 8,3665 |`
- **T1** `135-| **affinage de N2.ac** | 122 Mo | **3,1588** | **2,9096** | **2,8018** | **2,7607** | **5,5247** | **7,0507** | **7,9023** |`
- **T1** `139-61 Mo) et **2,9213** à 2 000 octets ; l'affinage de N2.ac ajoute **−0,16** en domaine et −0,19 en`
- **T1** `201-donc le débit ne perd que **13 %** de 256 à 2 048. La fenêtre est presque gratuite à cette`
- **T1** `205-- **Le run à 30 000 pas** part de N2.ac : 61 Mo de base + 246 Mo à 1 024 ; le comparer au 200 k`
- **T1** `206:  (205 Mo depuis zéro) avantage la fenêtre **et** l'initialisation — le contrôle depuis zéro`
- **T1** `| `00221850` | 2026-10-27 11:34 | 2.6 Mo | 558 Ko | 6 | 469 | 529 | 7 | 0 |`
- **T1** `| `04ed1834` | 2026-10-08 09:18 | 0.3 Mo | 67 Ko | 1 | 27 | 42 | 0 | 0 |`
- **T1** `| `0733c5bb` | 2026-11-02 16:14 | 2.7 Mo | 480 Ko | 7 | 721 | 672 | 1 | 0 |`
- **T1** `| `0b0a6a0d` | 2026-10-31 17:17 | 6.4 Mo | 1148 Ko | 20 | 1709 | 1565 | 5 | 4 |`
- **T1** `| `0b2c86eb` | 2026-10-27 10:29 | 0.9 Mo | 148 Ko | 1 | 123 | 128 | 0 | 0 |`
- **T1** `-| `0733c5bb` | 2026-11-02 16:14 | 2.5 Mo | 429 Ko | 6 | 633 | 598 | 1 | 0 |`
- **T1** `+| `0733c5bb` | 2026-11-02 16:14 | 2.7 Mo | 480 Ko | 7 | 721 | 672 | 1 | 0 |`
- **T1** `| `0b69f616` | 2026-10-30 21:46 | 0.8 Mo | 197 Ko | 1 | 180 | 200 | 0 | 0 |`
- **T1** `| `22e518ee` | 2026-10-31 11:13 | 0.6 Mo | 175 Ko | 1 | 129 | 171 | 5 | 0 |`
- **T1** `| `235066f5` | 2026-10-27 11:38 | 0.3 Mo | 60 Ko | 1 | 31 | 39 | 0 | 0 |`
- **T1** `| `27c99b10` | 2026-09-25 19:40 | 1.0 Mo | 61 Ko | 1 | 57 | 54 | 1 | 0 |`
- **T1** `-| `29ad180d` | 2026-11-02 16:14 | 3.1 Mo | 446 Ko | 12 | 360 | 353 | 4 | 2 |`
- **T1** `+| `29ad180d` | 2026-11-02 16:14 | 3.7 Mo | 505 Ko | 14 | 415 | 404 | 4 | 2 |`
- **T1** `| `2c2a6595` | 2026-10-02 15:03 | 0.4 Mo | 66 Ko | 1 | 29 | 44 | 0 | 0 |`
- **T1** `| `2f51f17f` | 2026-10-22 08:14 | 0.1 Mo | 26 Ko | 1 | 18 | 17 | 0 | 0 |`
- **T1** `| `2fd56aa5` | 2026-10-27 18:48 | 0.3 Mo | 57 Ko | 1 | 30 | 37 | 0 | 0 |`
- **T1** `| `a4eaa4c8` | 2026-10-08 09:18 | 0.3 Mo | 60 Ko | 1 | 28 | 38 | 0 | 0 |`
- **T1** `| `a9e308b7` | 2026-10-08 09:19 | 0.3 Mo | 44 Ko | 1 | 20 | 20 | 0 | 0 |`
- **T1** `| `aa5f9fc5` | 2026-09-30 15:07 | 0.8 Mo | 129 Ko | 1 | 78 | 100 | 0 | 0 |`
- **T1** `-| `abb58991` | 2026-11-02 16:15 | 8.2 Mo | 1452 Ko | 173 | 1250 | 1018 | 12 | 8 |`
- **T1** `+| `abb58991` | 2026-11-02 16:15 | 8.2 Mo | 1459 Ko | 173 | 1254 | 1021 | 12 | 8 |`
- **T1** `| `b13a6032` | 2026-10-02 15:03 | 0.3 Mo | 88 Ko | 1 | 17 | 43 | 0 | 0 |`
- **T1** `| `b6a672ec` | 2026-11-01 13:28 | 0.3 Mo | 67 Ko | 2 | 59 | 59 | 1 | 0 |`
- **T1** `**147 scans détectés** (91 uniques, 2 053 p), **60 documents, 1 982 p, 4,41 M car.**, 8 Ko 0 ;`
- **T1** `| `0733c5bb` | 2026-11-02 16:14 | 2.7 Mo | 477 Ko | 7 | 714 | 666 | 1 | 0 |`
- **T1** `| `29ad180d` | 2026-11-02 16:14 | 3.7 Mo | 501 Ko | 14 | 413 | 403 | 4 | 2 |`
- **T1** `| `29ad180d` | 2026-11-02 16:14 | 3.7 Mo | 505 Ko | 14 | 415 | 404 | 4 | 2 |`
- **T2** `0, 0 %, 1 MiB`
- **T2** `1, 0 %, 1 MiB`
- **T3** `(α = 0,9) — **3,0550** en domaine pour **61,4 Mo**, à **0,14** du run de 60 000 pas (2,9121)`
- **T3** `**Le coût** : le professeur est évalué à chaque pas (+25–30 % par pas) ; à budget de temps`
- **T3** `constant, l'élève voit ~26 Mo au lieu de 33 (≈ −0,02 de PPL), le gain net reste **~+0,08**.`
- **T3** `(122 Mo), même init `mix-60k` :`
- **T3** `| affinage dur, 15 000 pas | 61 Mo | 3,1588 | 2,9096 | 2,8018 | 2,7607 | 5,5247 | 7,0507 | 7,9023 |`
- **T3** `| distillé, 15 000 pas | 61 Mo | 3,0550 | 2,8062 | 2,7015 | 2,6601 | 5,4309 | 6,7639 | 7,3816 |`
- **T3** `| **distillé, 30 000 pas** | **122 Mo** | {{K128}} | {{K512}} | {{K1000}} | {{K2000}} | {{KLIT}} | {{KEN}} | {{KWT}} |`
- **T3** `## 6. Le complément 2 048 « mêmes pas » : 20 000 pas, 328 Mo`
- **T3** `fois plus d'octets** : 328 Mo contre 164) :`
- **T3** `| fenêtre 1 024 | 164 Mo | 2,9955 | 2,7201 | 2,6256 | 2,5757 | 2,5429 |`
- **T3** `| **fenêtre 2 048** | **328 Mo** | {{W128}} | {{W512}} | {{W1000}} | {{W2000}} | {{W4000}} |`
- **T3** `[still running after 60000ms; moved to background job bash-67]`
- **T4** `# 30 000 pas (122 Mo), même init mix-60k. Question : un meilleur professeur donne-t-il un`
- **T4** `0, 274 MiB, 0 %`
- **T4** `1, 1 MiB, 0 %`
- **T4** `1, 9948 MiB, 100 %`
- **T4** `[still running after 60000ms; moved to background job bash-100]`
- **T4** `0, 5200 MiB, 100 %`
- **T4** `1, 9950 MiB, 100 %`
- **T5** `0, 5280 MiB, 100 %`
- **T5** `1, 13200 MiB, 100 %`
- **T5** `- **Fait** : types **60/60**, rôles **142/142** ; **corpus réel** 8,5 %/65,5 % ; **arbre** 99 à ≥3, **référents** 294/371, **traduction** 14/14 ; **page `/paragraphes`**, **banque 9 paragraphes** ; **`
- **T5** `- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → **non mesuré** (run interrompu).`
- **T5** `**Partiel** — mesuré : la **sortie précoce** (**−24,05 %** de temps pour **−1,61** point de`
- **T5** `moteur** : **÷1,47 / ÷1,24** à profondeur 8, avec une variabilité de ±10 % ; le chemin court`
- **T5** `entraîné est le facteur limitant (**23,19 %** contre **47,73 %** pour le long).`
- **T5** `| [`rapport-s-corpus-reel.md`](rapport-s-corpus-reel.md) | **S** — le corpus réel : GN+GV 8,5 % CEGEP (mélange 9,1 %), 65,5 % propre (9,1 %) ; plancher du mélange ; banque 200 phrases / 355 candidats `
- **T5** `- la variabilité ±10 % entre exécutions peut masquer le gain ;`
- **T5** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4, A6.2 bloqués** ; A2.6 partiel ; A3.2/A3.3 mesurée`
- **T5** `| **N1** | `drave-n0` : 11,47 M, 6 blocs, octets, [attention](../theorie/glossaire/entrees/attention.md) locale, [FFN](../theorie/glossaire/entrees/ffn.md) creux, 3 têtes précoces | ✅ | aucune — PPL *`
- **T5** `| **N2** | la distillation : corpus, professeur, [curriculum](../theorie/glossaire/entrees/curriculum.md) | 🔬 | **N2.h** — corpus dédupliqué (**0 %** de fuite) : la chaîne propre vaut **3,0904**, pas `
- **T5** `90-| `porte-mistral.sh` | 8 s | ✅ porte de correction tenue (100.0 % des positions UTILES au-dessus de 0.95, min 1.0000 >= plancher  |`
- **T5** `-- **Fait** : types **60/60**, rôles **142/142** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **55 t`
- **T5** `+- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 t`
- **T5** `0, 5280 MiB, 99 %`
- **T8** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v6** : h050, h053 et « si fort que » **fermés**, gold **60** (vague 5) ; **60/60** types, **142/142** r`
- **T9** `437181 bash -c cd /home/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -2; for i in $(seq 1 15); do [ -f .git/index.lock ] || break; sleep 4; done; git add reports/rapport`
- **T9** `136:- **N2 (nuit)** : la distillation tient-elle à 30 000 pas / 122 Mo ? → runs relancés, réponse attendue.`
- **T9** `Paire propre (même code, même harnais, même init, mêmes 33 Mo, seul α change) :`
- … (tronqué)

## 5. Erreurs rencontrées

7 sorties en erreur ou divergentes. Les premières :

- **T3** : (§ 3) sépare les deux.  ## Fichiers  - Modèles : `work/n2ac/mix512-15k.pt`, `mix1024-7.5k.pt`, `mix2048-3.75k.pt`,   `mix512-zero-15k.pt` ; `mix1024-30k.pt` **non écrit — run interrompu** ; témoins   
- **T5** : M	docs/implantation/moteur-de-pensee.md M	docs/pilotage/backlog/N3-operations-natives.md M	docs/pilotage/backlog/index.md M	docs/pilotage/en-cours.md M	docs/pilotage/plan-travail.md M	docs/pilotage/re
- **T6** : M  docs/implantation/moteur-de-pensee.md M  docs/pilotage/en-cours.md  M journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md  M journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rappor
- **T8** : 31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees
- **T9** : [stderr]   ✅ index : aucun fait stagé sans état fatal: Unable to create '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.git/index.lock': File exists.  Another git process seems to be running in this
- **T10** : [stderr]   ✅ index : aucun fait stagé sans état fatal: cannot lock ref 'HEAD': is at 8cea841f41bd691bd941bd198ce9132f805321f7 but expected 6b0e9c833c6d33ced86fe7bc9857850c48515f4f [exit code: 128]
- **T12** : [stderr]   ✅ index : aucun fait stagé sans état fatal: Unable to create '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.git/index.lock': File exists.  Another git process seems to be running in this

## 6. Commits

- S — VALIDATION HUMAINE : 8 VERDICTS DE RÉFÉRENTS SUR /PARAGRAPHES (a001–a003) + 8 VERDICTS BANQUE (p003, c010, c066, c067)" && git log --oneline -1 && git statu
- REPRISE — LES QUATRE SESSIONS INTERROMPUES SONT TRIÉES ; ÉTAT AU 04/11" -m "N2 : les deux runs de la nuit sont interrompus par le reboot de 19 h 33 (kd2 8 250/3
- MANDATS — LES PROCHAINES ACTIONS SONT ALIGNÉES SUR L'ÉTAT DU 04/11" -m "N2 : relancer kd2/rope2048 puis la porte propre. S : poursuivre la validation /paragraph
- N2 — LES DEUX RUNS SONT RELANCÉS APRÈS LE REBOOT : KD2 GPU0, ROPE2048 GPU1 ; LA PASSE ATTEND LES RUNS" -m "Les anciens logs sont préservés en .interrompu.log ; 
- PILOTAGE — N3 INTÉGRÉ, S 61/61 ET B13 145/145 DANS L'ÉTAT ; 83e PORTE, § 12 ET LE SUIVI DOCS" -m "Backlog N3 mesurée, roadmap N3 couvert, 83e porte dans les réf
- ÉTAT — B13 146/146 (DÉFAUT CONDITIONNEL) ; 608 FICHES / 693 JSON ; HEURE LOCALE CORRIGÉE" -m "Le fait B13 146/146 (défaut conditionnel : le niveau si le réel es
- ÉTAT — N2 : KD2 ~19 400/30 000 (LOG BUFFERISÉ), ROPE2048 4 650/20 000 ; ETA CORRIGÉE (~13 H 30 / ~19–20 H)" -m "Le log kd2 s'arrête à 12 050 pas (11 h 07) alors
- ÉTAT — B13 147/147 (SEUIL DU PARALLÈLE : 0,9326 < 0,9389) ; COMPTEURS 609/695 ; HEURE CORRIGÉE" -m "Le fait 147/147 et sa fiche (rapport-pensee-seuil-parallele)
- INDEX — LE CATALOGUE PASSE DE 596 À 606 FICHES (N3, S, B13, TROISIÈME PASSE) ; ÉTAT 12 H 16" -m "Le catalogue généré était périmé de 10 fiches : N3 (inventaire)
- ÉTAT — B13 148/148 (TROISIÈME PASSE : VARIANCE NULLE, PARALLÈLE 0,9326 → 0,9389) ; ÉTAT 12 H 19" -m "La troisième passe (rapport-pensee-troisieme-passe, JSON pe
- ÉTAT — COMPTEURS 610/696 ; HEURE CORRIGÉE (12 H 18)" -m "Les nouveaux rapports de la session B13 (DRVM N0/N1, pensee-drvm-n01.json) et de S (rapport-s-paragraph
- ROADMAP — S v7 (61/61, 144/144, 56 TESTS), B13 148/148, RUNS N2 ET ROPE2048 ; ÉTAT 12 H 24" -m "La roadmap gardait B13 à 140/140 et S à la v6 : mis à jour des d
- PILOTAGE — CHANTIERS, PLAN-TRAVAIL ET PORTES ALIGNÉS : B13 148/148, S v7, 83 PORTES ; ÉTAT 12 H 34" -m "chantiers.md : B 148/148, L porte B13 148/148, B13 148/1
- ÉTAT — COMPTEURS 610/697 (WIP B13 t03) ; HEURE 12 H 37" -m "Le nouveau JSON pensee-quatre-modes-432-t03.json (B13, non committé) porte le disque à 697 JSON ; l'
- ÉTAT — COMPTEURS 610/697 (WIP B13 t03) ; HEURE 12 H 37" -m "Le nouveau JSON pensee-quatre-modes-432-t03.json (B13, non committé) porte le disque à 697 JSON ; l'
- ERRATUM N2 — LA DISTILLATION NATIVE NE GAGNE RIEN À PARITÉ STRICTE ; ÉTAT, ROADMAP ET PLAN-TRAVAIL CORRIGÉS" -m "Le +0,14–0,18 (et le +0,10 de la production) ve
- B13 149/149 — DRVM N0.1 : LE PAYLOAD CORROMPU EST REFUSÉ (LE HASH MANQUAIT) ; ÉTAT, ROADMAP, CHANTIERS, PLAN-TRAVAIL" -m "Le fait est committé (9593718e, rappor
- B13 150/150 — LA VARIANCE À 0,3 : ±0,0074 AU PIRE, 7/7 SEUILS, REFUS 0 ; ÉTAT, ROADMAP, CHANTIERS, PLAN-TRAVAIL" -m "Le fait est committé (8cea841f, rapport-pen
- INDEX — 606 → 608 (DRVM N0.1, VARIANCE) ; README — LA VARIANCE 150/150 AJOUTÉE ; ÉTAT 12 H 54" -m "Le catalogue généré rattrape les deux dernières fiches (DRVM 
- ÉTAT — B13 150/150 ALLÉGÉ (T0 3 986) ; CLAIM N2 PROLONGÉ À 720 MIN (ROPE ~19–20 H)" -m "L'historique B13 (seuil, défaut conditionnel, run 2, élision, troisième 
- B13 151/151 — LA PRAGMATIQUE NEURONALE QUALIFIE (1,0 / 1,0 / 0,9846 / 0,9769 SUR 130 PHRASES) ; ÉTAT, ROADMAP, CHANTIERS, PLAN-TRAVAIL" -m "Le fait est committé
- B13 151/151 — LA PRAGMATIQUE NEURONALE QUALIFIE (1,0 / 1,0 / 0,9846 / 0,9769 SUR 130 PHRASES) ; ÉTAT, ROADMAP, CHANTIERS, PLAN-TRAVAIL" -m "Le fait est committé

