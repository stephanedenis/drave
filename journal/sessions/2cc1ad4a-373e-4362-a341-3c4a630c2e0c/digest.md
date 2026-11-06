# Session DSH — relecture

- identifiant : `2cc1ad4a-373e-4362-a341-3c4a630c2e0c`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 19:25:28
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : vérifier la **cohérence des fiches de la journée** (v2 → v7) avec leurs JSON et avec l'état committé `69bd865e`.

Fiches à vérifier (chacune avec son JSON) :
- `reports/rapport-pensee-attachement-v2.md` / `pensee-attachement-v2.json`
- `reports/rapport-pensee-attachement-v3.md` / `pensee-attachement-v3.json`
- `reports/rapport-pensee-segmentation-v4.md` / `pensee-segmentation-v4.json`
- `reports/rapport-pensee-couverture-v5.md` / `pensee-couverture-v5.json`
- `reports/rapport-pensee-attachement-parfait.md` / `pensee-attachement-parfait.json`
- `reports/rapport-pensee-couverture-v7.md` / `pensee-couverture-v7.json`
- `reports/rapport-gold-split.md` / `pensee-gold-split.json`

À faire :
1. Pour chaque fiche : les chiffres du texte == ceux du JSON == ce que le code donne au commit `69bd865e` **si la fiche décrit l'état courant** ; sinon (fiche historique) vérifie qu'elle est cohérente **avec son propre instantané** et qu'elle porte une mention d'historique.
2. Signale : les valeurs contradictoires entre deux fiches, les tableaux dont la somme ne tombe pas, les renvois de § faux (« cf. § 3 » qui n'existe pas), les chiffres d'un JSON absents du texte et réciproquement, les fiches sans contrôle négatif.
3. Vérifie que chaque fiche nomme sa **ligne de roadmap** (B13), sa **date** et son **verdict**, et que `reports/README.md` les référence.
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-coherence-fiches-v7.md` et `reports/pensee-coherence-fiches-v7.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant (pas même les fiches fautives — tu les décris dans ton rapport) ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé : nombre de fiches, nombre de divergences, liste des corrections à faire.
Your parent agent id is "e181ce02-cd50-488a-a6be-e84b79d40dcc". Before you finish, send your result to that agent with send_message({ agent_id: "e181ce02-cd50-488a-a6be-e84b79d40dcc", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

# Directives de l'agent — Drave

> **Compteurs vivants.** Dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; ne pas les recopier ici.

> **Porte d'entrée.** Lis ce fichier en entier (2 min) : il porte la **vision**, les règles non négociables et le
> **routage** vers le document de chaque tâche. Le détail n'est pas ici : il est dans [`docs/methode/`](docs/methode/)
> (tableau § 3). L'**état courant** est dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; la **roadmap** dans
> [`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md) ; le récit daté dans [`journal/`](journal/).

## 1. La vision (l'essentiel)

**Drave est une vision de l'IA centrée sur les flots de données, pas sur le calcul brut.** Les activations d'un
réseau sont des **faits** regroupés en **listes valuées poussées** vers leurs lecteurs : le coût du calcul devient proportionnel à l'**activité**, et le modèle devient **décomposable**, **répartissable** et **observable**. Le principe : la structure bat la taille. Construire le moteur et modèle optimisé qui rend cette structure observable, décomposable, répartissable et rejouable permet d'atteindre de nouveaux sommets. L'approche par **bus d'événements** rend chaque bloc fonctionnel optimisable, comparable et substituable (neuronal là où l'intuition aide, computationnel là où la fiabilité prime).

Né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de les
**combiner**, de les **décomposer** en couches et grappes exécutables par du matériel divers, voire **distribué
en réseau**, de les **diagnostiquer** en étudiant leurs **flux**, et de **rejouer** des événements.


## 2. Les règles non négociables

1. **Rangement** : `docs/` = état, vision, concepts (ce qui reste vrai quand les chiffres changent) ; `reports/` =
   résultats mesurés, fiches, JSON ; `journal/` = récit daté ; `data/` = corpus. *Un résultat qui traîne dans
   `docs/` **déménage**.* → [`docs/methode/rangement.md`](docs/methode/rangement.md)
2. **Un résultat** porte le chiffre, la mesure, le dispositif, un **contrôle négatif**, et **ce qui pourrait le
   rendre faux** — puis un **commit**, la **fiche** dans `reports/`, le **récit** dans `journal/`, l'**état** dans
   `docs/pilotage/en-cours.md`, et il **nomme sa ligne de roadmap** (A… / B… / N… / R…). *Sans contrôle négatif, ce n'est pas un
   résultat.* → [`docs/methode/resultats.md`](docs/methode/resultats.md)
3. **Les portes** : `bash tools/toutes-les-portes.sh` ; le registre est dans `$JOURNAUX/registre.txt` (affiché au
   lancement) et le verdict se lit par `awk '$2 != 0'` — **jamais** par les marqueurs ni à travers un tube. Rouges
   tolérées : **celles listées dans [`docs/pilotage/references-non-regression.md`](docs/pilotage/references-non-regression.md)** ; toute autre est une régression. →
   [`docs/methode/portes.md`](docs/methode/portes.md)
4. **La revue de documentation** avant chaque commit de clôture : `python3 tools/revue_documentation.py` (et
   `tools/porte-tableaux.sh`) ; **corriger** ce qu'elle signale. → [`docs/methode/rangement.md`](docs/methode/rangement.md)
5. **Panini et Nipada** à chaque cycle : lire ce qui a bougé chez eux, confronter ; la théorie va dans
   [`docs/theorie/genealogie-des-langues.md`](docs/theorie/genealogie-des-langues.md), **jamais** les chiffres. Leur avertissement :
   la surface capte **l'époque** (β +0,138) bien plus que la **filiation** (β +0,049) — contrôler la date dans tout
   test de style, la surface dans tout test de famille. → [`docs/methode/panini-nipada.md`](docs/methode/panini-nipada.md)
6. **Le miroir entrée/sortie** : toute mesure d'entrée se double d'une mesure de **sortie** (restitution, boucle) ;
   la **fluidité n'est pas la fidélité**. → [`docs/methode/miroir.md`](docs/methode/miroir.md)
7. **La roadmap** ([`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md)) : chaque chantier a une **prochaine action** ; l'ordre est la **valeur** et les **dépendances**, jamais une date. Un chantier est **fini** quand il est
   mesuré, écrit et committé ; il est **marqué**, et le suivant désigné.
8. **Ne jamais bloquer, ne jamais rester en attente** : une question humaine se **consolide** dans `en-cours` et on **continue** ; si une ligne est bloquée (corpus, compte, matériel), on prend la suivante
   — la **file « jamais en attente »** de la roadmap. → [`docs/methode/ressources.md`](docs/methode/ressources.md)
9. **Les illustrations sont des SVG.** Aucun **ASCII art** dans un bloc de code. Un schéma est un
   **`.svg`** — direct, ou généré par **docwatch** depuis `.mmd`/`.puml` (l'image pointe vers
   `<source>.svg`) — avec `viewBox`, `<title>`, `<desc>`, liens relatifs ; il vit dans
   `docs/schemas/` ou `docs/theorie/synthese/schemas/`. Vérifier : `python3 tools/verifier_schemas.py`.
   → [`docs/methode/illustrations.md`](docs/methode/illustrations.md)
10. **Pilotage : cycles longs, sous-agents, état unique.** Un goal par programme (`max_goal_rounds`
    1 000) ; on s'arrête sur un résultat mesuré, écrit, committé, ou un blocage. Les tâches
    indépendantes : **sous-agents** (2–4), sans toucher `en-cours`/`roadmap`/`AGENTS` ; ils
    rendent un **diff**. **État** : une session écrit `en-cours` à la fois ; aucun fait
    sans sa ligne (hook `verifie_etat_a_jour.py`). Git : `git add` explicite. La clôture met `en-cours` à jour (≤ 2 000 mots).
    → [`docs/methode/continuite.md`](docs/methode/continuite.md)

11. **Les GPU sont exclusivement réservés à Drave** ; les **professeurs** passent par l'**API
    DeepSeek** (`tools/llm/enseignant.py`), jamais par un serveur local (`llama-server`,
    `ollama`). Garde-fous : `hauru-gpu-guard` (timer 30 s), `porte-ressources` (contrôle GPU).
    → [`docs/methode/ressources.md`](docs/methode/ressources.md)

## 3. Routage : lire le document de sa tâche, pas les autres

| si la tâche est… | lire |
|---|---|
| comprendre la **vision** (les flots, les cinq axes, ce qu'elle n'est pas) | [`docs/theorie/vision.md`](docs/theorie/vision.md) |
| la **roadmap** (A/B/N/R, l'ordre, la file « jamais en attente ») | [`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md) |
| **la lecture rapide** et son backlog (techniques, couches, fiches) | [`docs/theorie/lecture-rapide.md`](docs/theorie/lecture-rapide.md) · [`docs/pilotage/backlog/index.md`](docs/pilotage/backlog/index.md) |
| comprendre la mission et les priorités | [`docs/methode/mission.md`](docs/methode/mission.md) |
| écrire un résultat (fiche, JSON, commit, journal) | [`docs/methode/resultats.md`](docs/methode/resultats.md) |
| ranger un fichier, revue de documentation, synthèse | [`docs/methode/rangement.md`](docs/methode/rangement.md) |
| **charger le contexte** (budget, protocole, ce qu'on ne charge pas) | [`docs/methode/contexte.md`](docs/methode/contexte.md) |
| **cycles DSH, sous-agents, reprise** | [`docs/methode/continuite.md`](docs/methode/continuite.md) |
| **rapporter à l'humain, un round** | [`docs/methode/relations-humaines.md`](docs/methode/relations-humaines.md) |
| **dessiner un schéma**, convertir un diagramme, améliorer une illustration | [`docs/methode/illustrations.md`](docs/methode/illustrations.md) |
| lancer ou lire les portes | [`docs/methode/portes.md`](docs/methode/portes.md) |
| étudier Panini/Nipada, la généalogie | [`docs/methode/panini-nipada.md`](docs/methode/panini-nipada.md) |
| concevoir un test d'entrée/sortie, corriger | [`docs/methode/miroir.md`](docs/methode/miroir.md) |
| planifier une campagne, le matériel, carpe diem | [`docs/methode/ressources.md`](docs/methode/ressources.md) |
| **les jeux symboliques** (surface → RSN-jeu → pensée, 71 langues, maîtres) | [`docs/theorie/jeux-symboliques.md`](docs/theorie/jeux-symboliques.md) |
| **le protocole sémantique** (rejouer, convergence, sens → texte, raisonnement gelé) | [`docs/theorie/protocole-semantique.md`](docs/theorie/protocole-semantique.md) |
| **l'état courant** (synthèse + chantiers + questions) | [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) |
| le **vocabulaire** (couche vs étage, termes du dépôt) | [`docs/theorie/glossaire.md`](docs/theorie/glossaire.md) |
| **trouver un sujet** (un concept, un chantier, une phase) | [`docs/theorie/carte.md`](docs/theorie/carte.md) |
| la carte de la documentation | [`docs/README.md`](docs/README.md) |

> **Chargement facultatif.** Les documents de cette table, `docs/pilotage/en-cours.md`, `docs/pilotage/roadmap.md`, `reports/` et
> `journal/` ne se lisent **que pour la tâche en cours** : le fichier de tâche suffit. Ne pas les
> charger « pour être complet » : c'est du contexte qui coûte et périme.

> **Le contexte est un budget.** Par défaut : `AGENTS.md` + `docs/pilotage/en-cours.md` + **un** document de
> tâche. Le protocole, les budgets et les cas « ne pas charger » sont dans
> [`docs/methode/contexte.md`](docs/methode/contexte.md) ; la vérification est
> `python3 tools/taille_documents.py`.

## 4. Le minimum avant de conclure

- l'état est à jour dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) (synthèse, chantiers, questions en attente) ;
- la **roadmap** est à jour : le chantier fini y est marqué, le suivant est désigné ;
- la fiche est dans `reports/`, le récit dans `journal/`, le commit porte le chiffre ;
- les portes sont vertes, **hors les rouges tolérées listées dans `docs/pilotage/references-non-regression.md`** ;
- la revue de documentation passe, et les liens résolvent.
- le budget de contexte est vérifié : `python3 tools/taille_documents.py`.
- l'état est court et reprenable : `python3 tools/verifie_en_cours.py`.
- journal : dossiers/jour, sessions liées → `tools/verifie_journal.py`.
- les schémas sont des SVG valides et référencés : `python3 tools/verifier_schemas.py`.

</system-reminder>

### 👤 Utilisateur

Current runtime context. This snapshot supersedes earlier runtime-context snapshots.

Current DSH file policy: danger-full-access. The DSH file sandbox does not restrict file modifications by available operations.

Approval prompts are disabled in this session: actions that require approval are rejected automatically — do not request sandbox escalation (do not set `sandbox_permissions`).

You are a delegated subagent: your permission scope was fixed when you were started and cannot be widened from inside this session — operations that require approval are rejected automatically. When the task needs access beyond that scope, do not retry the denied operation; state the limitation in your reply so the delegating agent can handle it.

### 👤 Utilisateur

<system-reminder>
A skill is a reusable set of task-specific instructions. The following skills are available in this session:

<available_skills>
- `microsoft-foundry`: Deploy, evaluate, fine-tune, and manage Foundry agents end-to-end with azd: hosted agent scaffold/run/deploy, prompt agent create, batch eval, continuous eval, prompt optimizer, Agent Optimizer scaffold, agent.yaml, dataset curation from traces, model fine-tuning (SFT/DPO/RFT). USE FOR: azd ai agent, azd provision/deploy, deploy agent, hosted agent, create agent, add tool to agent, invoke agent, evaluate agent, continuous eval, continuous monitoring, agent CI/CD, optimize prompt, improve prom...
</available_skills>

If the user names a skill, or the task clearly matches a skill's description, call the `skill` tool with the exact skill name before taking task actions. Load all applicable skills, then follow their full instructions. This catalog contains summaries only; do not infer or follow a skill's instructions until it has been loaded.
A user may also invoke a skill directly; its <skill_content> block then appears in this conversation. Follow it, and do not call the `skill` tool again for that skill.
</system-reminder>

### 🤖 Assistant

⏵ Inspection du dépôt et de l'état Git avant lecture des fiches

- **bash** `{"command": "git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet status --short | head -50; echo \"---BRANCH---\"; git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet rev-parse --abbrev-ref HEAD; echo \"---LOG---\"; git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet log --oneline -8; echo  … [163 caractères tronqués]`

  ```
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
D  journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/digest.md
D  journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/rapport.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rapport.md
D  journal/sessions/3144cf23-6004-46ef-bc3d-f05d81c0cff6/digest.md
D  journal/sessions/3144cf23-6004-46ef-bc3d-f05d81c0cff6/rapport.md
D  journal/sessions/3f8f2bb8-781b-44a6-9e14-58025004b6fc/digest.md
D  journal/sessions/3f8f2bb8-781b-44a6-9e14-58025004b6fc/rapport.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/digest.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/rapport.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a
… [2767 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports | head -60; echo \"---COUNT---\"; ls /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports | wc -l", "description": "List reports directory"}`

  ```
total 18560
drwxr-xr-x. 1 stephane stephane   69562  5 nov 19:22 .
drwxr-xr-x. 1 stephane stephane     660  1 nov 10:50 ..
drwxr-xr-x. 1 stephane stephane     102 24 oct 15:52 07
-rw-r--r--. 1 stephane stephane    4447 28 oct 09:17 07-mesures-couche-commune.md
-rw-r--r--. 1 stephane stephane     907 29 oct 16:25 a26-bilan.json
-rw-r--r--. 1 stephane stephane    1163  1 nov 20:40 a26-lot-disque.json
-rw-r--r--. 1 stephane stephane    1121 30 oct 08:57 a80-audit-final.json
-rw-r--r--. 1 stephane stephane     560 30 oct 00:04 a80-indice-qualifie.json
-rw-r--r--. 1 stephane stephane     672 29 oct 23:42 a80-melange-qualifie.json
-rw-r--r--. 1 stephane stephane     430 30 oct 08:57 a80-pannes-ppl.json
-rw-r--r--. 1 stephane stephane     630 29 oct 17:07 a80-porte-adaptateur.json
-rw-r--r--. 1 stephane stephane     521 29 oct 16:40 a80-porte-budget.json
-rw-r--r--. 1 stephane stephane     625 29 oct 22:07 a80-porte-bus.json
-rw-r--r--. 1 stephane stephane     654 29 oct 22:19 a80-porte-bus-socket.json
-rw-r--r--. 1 stephane stephane     677 29 oct 21:05 a80-porte-c4-retard.json
-rw-r--r--. 1 stephane stephane     600 29 oct 20:06 a80-porte-consolidation.json
-rw-r--r--. 1 stephane stepha
… [3132 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des sept fiches et de leurs JSON

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; for f in reports/rapport-pensee-attachement-v2.md reports/rapport-pensee-attachement-v3.md reports/rapport-pensee-segmentation-v4.md reports/rapport-pensee-couverture-v5.md reports/rapport-pensee-attachement-parfait.md reports/rapport- … [565 caractères tronqués]`

  ```
=== reports/rapport-pensee-attachement-v2.md ===
  91 5580 reports/rapport-pensee-attachement-v2.md
9d5337ce B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180
=== reports/rapport-pensee-attachement-v3.md ===
  84 4968 reports/rapport-pensee-attachement-v3.md
e1903e2d B13 — L'ANGLAIS EST LE TROU (60/94 SPANS, S NE SEGMENTE PAS L'ANGLAIS) ; TABLEAU V3 RÉPARÉ ; 182/182
=== reports/rapport-pensee-segmentation-v4.md ===
  79 4881 reports/rapport-pensee-segmentation-v4.md
392f03aa B13 — S NE SEGMENTE QUE LE FRANÇAIS : F1 0,4194 → 0,4539, TÊTE 0,6432 ; EXACT 157/160, FR 0,9915 / EN 0,9524 ; 183/183
=== reports/rapport-pensee-couverture-v5.md ===
  79 4356 reports/rapport-pensee-couverture-v5.md
b975011b B13 — LES CANDIDATS DU PRÉCÉDENT : EXACT 186/187 (0,9947), ANGLAIS 60/60, DEV 126/126 ; 183/183
=== reports/rapport-pensee-attachement-parfait.md ===
  71 3686 reports/rapport-pensee-attachement-parfait.md
0ec6c27d B13 — L'ATTACHEMENT PARFAIT SUR LES SPANS PRÉDITS : 187/187 (1,0000), FR 1,0, EN 1,0, DEV 126/126, TEST 61/61 ; RENDEMENT 0,7824 ; 183/183
=== reports/rapport-pensee-couverture-v7.md ===
… [1842 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; git show --stat 69bd865e | head -60; echo \"=== files changed at 69bd865e ===\"; git show --name-status --format=\"\" 69bd865e | head -80", "description": "Show commit 69bd865e stats and files"}`

  ```
commit 69bd865ec1bae1958b6f617bde4bf685a15d7d67
Author: Stéphane <stephane@localhost>
Date:   Thu Nov 5 19:22:37 2026 -0500

    B13 — LA COUVERTURE À 0,8201 : POS CONTEXTUEL 0,7603, F1 0,5595, EXACT 195/196 (0,9949), 43 SPANS ; 183/183

 docs/pilotage/en-cours.md                          |   4 +-
 docs/pilotage/roadmap.md                           |   2 +-
 journal/2026-11-05/README.md                       |   7 +-
 journal/2026-11-05/attention.md                    |   2 +-
 journal/2026-11-05/distribue.md                    |   2 +-
 journal/2026-11-05/docs.md                         |   2 +-
 journal/2026-11-05/memoire.md                      |   2 +-
 journal/2026-11-05/mesures.md                      |   8 +-
 journal/2026-11-05/modele.md                       |   2 +-
 journal/2026-11-05/moteur.md                       |   2 +-
 journal/2026-11-05/portes.md                       |   2 +-
 journal/README.md                                  |   2 +-
 journal/THEMES.md                                  |   2 +-
 journal/sessions/MANIFEST.md                       |   4 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 360 +++++++++++++++++++++
 .../rapport.md             
… [1134 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture intégrale des fiches et JSON pour comparaison chiffrée

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-v2.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-attachement-v2.json"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-v2.md</path>
<type>file</type>
<content>
1: # B13 — l'attachement v2 : exact 0,8483 → 0,9448, top-k strict 0,6069 → 0,9724
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **180/180 portes** : trois corrections **mesurées**, issues de trois sous-agents indépendants :
5: > (1) la règle du **segment précédent** (un SUB après un GV est une complétive → cible = le verbe ;
6: > après un GN, une relative → cible = l'antécédent), (2) les **têtes des candidats** de S
7: > (« « … » → Le livre » → `livre`), (3) le **lexique verbal anglais** complété. Sur les 145
8: > segments au bon span : **exact 123 → 137 (0,9448)**, top1 **126 → 140 (0,9655)**, top-k
9: > **134 → 142 (0,9793)**, **top-k strict 88 → 141 (0,9724)**.
10: >
11: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
12: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
13: > [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) (`CONVENTION_CIBLE`),
14: > [`autotest.py`](../tools/pensee/autotest.py) ; fiches des sous-agents :
15: >
… [4730 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-attachement-v2.json</path>
<type>file</type>
<content>
1: {
2:  "date": "2026-11-05",
3:  "ligne": "B13",
4:  "portes": "180/180",
5:  "labels": 145,
6:  "cibles": 239,
7:  "avant": {
8:   "exact": 123,
9:   "exact_span": 0.8483,
10:   "top1": 126,
11:   "topk": 134,
12:   "topk_exact": 88,
13:   "verbe_est": 0.9524,
14:   "nom_est": 0.7683
15:  },
16:  "apres": {
17:   "exact": 137,
18:   "exact_span": 0.9448,
19:   "top1": 140,
20:   "topk": 142,
21:   "topk_exact": 141,
22:   "top1_span": 0.9655,
23:   "topk_span": 0.9793,
24:   "topk_exact_span": 0.9724,
25:   "verbe_pos": 0.9569,
26:   "nom_pos": 0.8966,
27:   "verbe_cibles": 116,
28:   "nom_cibles": 29
29:  },
30:  "rendement": {
31:   "top1": 0.5858,
32:   "topk": 0.5941,
33:   "exact": 0.5732
34:  },
35:  "corrections": {
36:   "segment_precedent": {
37:    "gain_exact": 6,
38:    "source": "A7",
39:    "ids": [
40:     "s012",
41:     "s030",
42:     "s052",
43:     "s097",
44:     "s124",
45:     "s139"
46:    ]
47:   },
48:   "lexique_anglais": {
49:    "gain_exact": 8,
50:    "gain_top1": 8,
51:    "source": "A2",
52:    "risque": "borne haute"
53:   }
… [676 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-v3.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-attachement-v3.json"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-v3.md</path>
<type>file</type>
<content>
1: # B13 — l'attachement v3 : exact 0,9448 → 0,9724, les noms à 1,0
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **181/181 portes** : trois règles **générales** issues du diagnostic des 8 échecs (A9) sont
5: > intégrées — **R2** (un GP n'est pas gouverné par un mot de son span), **R3** (cible vide :
6: > génitif → tête du GN à gauche), **R4** (enclitique `appelle-moi` → `appelle`). Sur les 145
7: > segments au bon span : **exact 137 → 141 (0,9724)**, top1 **140 → 143 (0,9862)**, top-k 142
8: > (0,9793), **top-k strict 142 (0,9793)** ; les **cibles noms atteignent 29/29 = 1,0**.
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_cible_hors_span`,
11: > `_repli_cible_gp`, `_sans_enclitique`), [`autotest.py`](../tools/pensee/autotest.py) ;
12: > fiche A9 [échecs v2](rapport-echecs-v2.md) ; JSON [`pensee-attachement-v3.json`](pensee-attachement-v3.json).
13: 
14: ## 1. Avant / après (145 segments au bon span)
15: 
16: | mesure | v2 | **v3** | écart |
17:
… [4109 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-attachement-v3.json</path>
<type>file</type>
<content>
1: {
2:  "date": "2026-11-05",
3:  "ligne": "B13",
4:  "portes": "181/181",
5:  "labels": 145,
6:  "cibles": 239,
7:  "avant": {
8:   "exact": 137,
9:   "exact_span": 0.9448,
10:   "top1": 140,
11:   "topk": 142,
12:   "topk_exact": 141,
13:   "verbe": 0.9569,
14:   "nom": 0.8966
15:  },
16:  "apres": {
17:   "exact": 141,
18:   "exact_span": 0.9724,
19:   "top1": 143,
20:   "top1_span": 0.9862,
21:   "topk": 142,
22:   "topk_span": 0.9793,
23:   "topk_exact": 142,
24:   "topk_exact_span": 0.9793,
25:   "verbe": 0.9655,
26:   "nom": 1.0
27:  },
28:  "rendement": {
29:   "top1": 0.5983,
30:   "topk": 0.5941,
31:   "exact": 0.59
32:  },
33:  "regles_integrees": {
34:   "R2": "un GP n'est pas gouverné par un mot de son span (+2)",
35:   "R3": "cible vide génitive → tête du GN à gauche (+1)",
36:   "R4": "enclitiques (+1)"
37:  },
38:  "regles_rejetees": {
39:   "R1": "lexique rêver/sauter/marcher (formes du gold)",
40:   "R5": "pseudo-GV ADV (n=1)"
41:  },
42:  "controles_negatifs": {
43:   "completion_naive": "132 (−5)",
44:   "R5_sans_ADV": "131 (−6)",
45:   "R
… [350 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-segmentation-v4.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-segmentation-v4.json"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-segmentation-v4.md</path>
<type>file</type>
<content>
1: # B13 — la segmentation d'abord : F1 0,2862 → 0,4194, exact 158/160 (0,9875), couverture 160/239
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **183/183 portes** : le diagnostic de A12/A14 était juste — le trou n'était pas l'attachement mais le
5: > **découpage**. Sept corrections générales font passer la **F1 syntagmes de 0,2862 à 0,4539**
6: > (union ; S 0,4285, chunker 0,4143), la **tête de 0,4989 à 0,6432**, et la **couverture de 145 à
7: > 160 labels** (sur 239) ; l'attachement suit : **exact 157/160 = 0,9812**, **top-k 156/239**,
8: > par langue **fr 0,9915** (117/118) et **en 0,9524** (40/42) — l'anglais passe de **28 à 42 labels**.
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
11: > `_verbe_dans`, `_cible_hors_span`), [`autotest.py`](../tools/pensee/autotest.py) (38 assertions
12: > recalées) ; fiches amont [spans](rapport-spans-chunker.md) (A12), [gold anglais](rapport-gold-anglais.md)
13: > (A14) ; JSON [`pensee-s
… [4017 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-segmentation-v4.json</path>
<type>file</type>
<content>
1: {
2:  "date": "2026-11-05",
3:  "ligne": "B13",
4:  "portes": "183/183",
5:  "avant": {
6:   "f1": 0.2862,
7:   "tete": 0.4989,
8:   "labels": 145,
9:   "exact": 141,
10:   "exact_span": 0.9724,
11:   "couverture": 0.6067,
12:   "fr": 0.9658,
13:   "en": 1.0,
14:   "spans_perdus": 94,
15:   "echecs_cible": 4
16:  },
17:  "apres": {
18:   "f1": 0.4539,
19:   "tete": 0.6432,
20:   "labels": 160,
21:   "exact": 157,
22:   "exact_span": 0.9812,
23:   "couverture": 0.6695,
24:   "topk": 156,
25:   "topk_taux": 0.6527,
26:   "fr": 0.9915,
27:   "en": 0.9524,
28:   "spans_perdus": {
29:    "REL": 48,
30:    "SUB": 21,
31:    "GP": 10,
32:    "total": 79
33:   },
34:   "echecs_cible": [
35:    "r162",
36:    "r309",
37:    "r194"
38:   ],
39:   "f1_s": 0.4285,
40:   "f1_chunker": 0.4143
41:  },
42:  "corrections": [
43:   "REL/SUB par segment précédent",
44:   "GV à tête verbale + frontières",
45:   "GN s'arrête au verbe",
46:   "GP préposition+infinitif",
47:   "_cible_hors_span partout",
48:   "_verbe_dans sans auxiliaire + lexique commun",
49:   "S ne segmente 
… [204 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-couverture-v5.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-couverture-v5.json"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-couverture-v5.md</path>
<type>file</type>
<content>
1: # B13 — la couverture : 187 labels, exact 185/187 (0,9893), F1 0,5156
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **183/183 portes** : la **couverture** passe de **160 à 187 labels** (sur 239) et l'exactitude
5: > tient : **exact 186/187 = 0,9947** (fr **0,9921**, en **1,0000** — 60/60) ; la **F1 syntagmes**
6: > monte à **0,5156** (union ; S 0,4582, chunker 0,5351) et la tête à **0,6826** ; les **spans
7: > perdus** tombent de **79 à 52** (24 REL, 12 SUB, 16 GP). Sur le gold tenu à l'écart : **dev
8: > 126/126 (1,000)**, **test 60/61** — la progression n'est pas un surajustement visible.
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
11: > `_cible_precedent`), [`autotest.py`](../tools/pensee/autotest.py) (25 assertions recalées) ;
12: > [`gold_split.py`](../tools/tests/linguistique/gold_split.py) pour dev/test ; JSON
13: > [`pensee-couverture-v5.json`](pensee-couverture-v5.json).
14: 
15: ## 1. Les six corrections
16: 
17: 
… [3515 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-couverture-v5.json</path>
<type>file</type>
<content>
1: {
2:  "date": "2026-11-05",
3:  "ligne": "B13",
4:  "portes": "183/183",
5:  "avant": {
6:   "labels": 160,
7:   "exact": 157,
8:   "exact_span": 0.9812,
9:   "topk": 156,
10:   "couverture": 0.6695,
11:   "f1": 0.4539,
12:   "tete": 0.6432,
13:   "fr": 0.9915,
14:   "en": 0.9524,
15:   "spans": 79,
16:   "echecs_cible": 3
17:  },
18:  "apres": {
19:   "labels": 187,
20:   "exact": 186,
21:   "exact_span": 0.9947,
22:   "topk": 161,
23:   "couverture": 0.7824,
24:   "f1": 0.5156,
25:   "f1_s": 0.4582,
26:   "f1_chunker": 0.5351,
27:   "tete": 0.6826,
28:   "fr": 0.9921,
29:   "en": 1.0,
30:   "spans": {
31:    "REL": 24,
32:    "SUB": 12,
33:    "GP": 16,
34:    "total": 52
35:   },
36:   "echecs_cible": 1,
37:   "topk_taux": 0.6736,
38:   "candidats_manquants": 26
39:  },
40:  "dev": {
41:   "exact": 126,
42:   "labels": 126,
43:   "f1": 0.5091,
44:   "couverture": 0.773
45:  },
46:  "test": {
47:   "exact": 60,
48:   "labels": 61,
49:   "f1": 0.5217,
50:   "couverture": 0.8026
51:  },
52:  "corrections": [
53:   "REL/SUB avant le GN + « that » désambiguïsé
… [435 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-parfait.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-attachement-parfait.json"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-parfait.md</path>
<type>file</type>
<content>
1: # B13 — l'attachement parfait sur les spans prédits : 187/187 (1,0000)
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **183/183 portes** : sur les **187 segments dont le span est prédit** (sur 239 cibles), la cible
5: > est **juste 187 fois** — **français 127/127 (1,0)**, **anglais 60/60 (1,0)**, **verbes 131/131**,
6: > **noms 56/56** ; **dev 126/126**, **test 61/61**. Le **rendement global** reste **187/239 =
7: > 0,7824** : les 52 spans non prédits sont la seule frontière qui reste.
8: >
9: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_cible_precedent`,
10: > `_candidats_precedent`, `_repli_verbe_propre`, `_est_adverbe_seul`),
11: > [`autotest.py`](../tools/pensee/autotest.py) ; dev/test [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ;
12: > JSON [`pensee-attachement-parfait.json`](pensee-attachement-parfait.json).
13: 
14: ## 1. Les deux corrections de ce round
15: 
16: | # | correction | effet |
17: |---|---|---|
18: | 1 | **les 
… [2870 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-attachement-parfait.json</path>
<type>file</type>
<content>
1: {
2:  "date": "2026-11-05",
3:  "ligne": "B13",
4:  "portes": "183/183",
5:  "exact": {
6:   "labels": 187,
7:   "justes": 187,
8:   "taux": 1.0,
9:   "fr": "127/127",
10:   "en": "60/60",
11:   "verbe": "131/131",
12:   "nom": "56/56"
13:  },
14:  "dev": {
15:   "exact": 126,
16:   "labels": 126
17:  },
18:  "test": {
19:   "exact": 61,
20:   "labels": 61
21:  },
22:  "global": {
23:   "exact": 187,
24:   "cibles": 239,
25:   "taux": 0.7824,
26:   "spans_non_predits": {
27:    "REL": 24,
28:    "SUB": 12,
29:    "GP": 16,
30:    "total": 52
31:   }
32:  },
33:  "topk": {
34:   "justes": 161,
35:   "taux": 0.6736
36:  },
37:  "f1": 0.513,
38:  "corrections": [
39:   "candidats du précédent (antécédent REL, verbe SUB)",
40:   "adverbe seul non gouverneur + repli propre verbe (SUB/REL)"
41:  ],
42:  "limites": [
43:   "52 spans hors mesure",
44:   "top-k incomplet",
45:   "in-sample",
46:   "heuristiques"
47:  ]
48: }

(End of file - total 48 lines)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-couverture-v7.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-couverture-v7.json"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-couverture-v7.md</path>
<type>file</type>
<content>
1: # B13 — la couverture à 0,8201 : POS contextuel, GV avant GP, prépositions ambiguës
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **183/183 portes** : la **couverture** passe de **187 à 196 labels** (sur 239) et l'exactitude
5: > tient : **exact 195/196 = 0,9949** (fr **135/135 = 1,0**, en **60/61**) ; la **F1 syntagmes**
6: > monte à **0,5595** (union ; S 0,4741, chunker 0,5858), la tête à **0,7205** ; la **POS** passe de
7: > **0,7475 à 0,7603** ; les **spans perdus** tombent de **52 à 43** (21 REL, 17 SUB, 5 GP).
8: >
9: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (POS contextuel,
10: > ordre GV/GP, prépositions composées, sujets), [`autotest.py`](../tools/pensee/autotest.py)
11: > (32 assertions recalées) ; JSON [`pensee-couverture-v7.json`](pensee-couverture-v7.json).
12: 
13: ## 1. Les cinq corrections
14: 
15: | # | correction | effet |
16: |---|---|---|
17: | 1 | **POS contextuel** : un verbe de suffixe après DET/PRÉP/ADJ devient un nom (« brothe
… [2780 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-couverture-v7.json</path>
<type>file</type>
<content>
1: {
2:  "date": "2026-11-05",
3:  "ligne": "B13",
4:  "portes": "183/183",
5:  "avant": {
6:   "labels": 187,
7:   "exact": 187,
8:   "couverture": 0.7824,
9:   "f1": 0.513,
10:   "tete": 0.6826,
11:   "pos": 0.7475,
12:   "spans": 52
13:  },
14:  "apres": {
15:   "labels": 196,
16:   "exact": 195,
17:   "exact_span": 0.9949,
18:   "couverture": 0.8201,
19:   "f1": 0.5595,
20:   "f1_s": 0.4741,
21:   "f1_chunker": 0.5858,
22:   "tete": 0.7205,
23:   "pos": 0.7603,
24:   "fr": "135/135",
25:   "en": "60/61",
26:   "topk": 166,
27:   "topk_taux": 0.6946,
28:   "spans": {
29:    "REL": 21,
30:    "SUB": 17,
31:    "GP": 5,
32:    "total": 43
33:   }
34:  },
35:  "corrections": [
36:   "POS contextuel (DET/PRÉP/ADJ → nom)",
37:   "GV avant GP",
38:   "prépositions composées",
39:   "prépositions ambiguës (since/before/after/until/as)",
40:   "verbe après pronom sujet + adverbe final"
41:  ],
42:  "limites": [
43:   "43 spans",
44:   "top-k incomplet",
45:   "in-sample",
46:   "heuristiques"
47:  ]
48: }

(End of file - total 48 lines)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-split.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-split.json"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-split.md</path>
<type>file</type>
<content>
1: # B13 — le gold coupé en dev/test : les gains généralisent (test 0,9814, dev 0,9811)
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > Le gold 612 est coupé en **dev** (422 phrases, 163 cibles, 106 labels) et **test** (190, 76, 54)
5: > par un **hash stable de l'identifiant** (`crc32(id) % 3 == 0` → test), stratifié par source et
6: > par langue. Mesuré : **dev exact 104/106 (0,9811)**, **test 53/54 (0,9814)** — les règles de la
7: > journée ne sont donc pas un surajustement visible à ce niveau ; la F1 est même meilleure sur le
8: > test (0,4719 contre 0,4414).
9: >
10: > **Dispositif** : [`gold_split.py`](../tools/tests/linguistique/gold_split.py) (`dev`, `test`,
11: > `compter`), [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) ; JSON
12: > [`pensee-gold-split.json`](pensee-gold-split.json).
13: 
14: ## 1. L'équilibre du split
15: 
16: | | phrases | cibles | labels | sources | langues |
17: |---|---:|---:|---:|---|---|
18: | **dev** | 422 | 163 | 106 | 15 hand / 302 reel / 105 syn
… [2201 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-split.json</path>
<type>file</type>
<content>
1: {
2:  "date": "2026-11-05",
3:  "ligne": "B13",
4:  "split": "crc32(id)%3==0 → test",
5:  "dev": {
6:   "phrases": 422,
7:   "cibles": 163,
8:   "labels": 106,
9:   "exact": 104,
10:   "exact_taux": 0.9811,
11:   "f1": 0.4414,
12:   "tete": 0.6347,
13:   "fr": 1.0,
14:   "en": 0.9259
15:  },
16:  "test": {
17:   "phrases": 190,
18:   "cibles": 76,
19:   "labels": 54,
20:   "exact": 53,
21:   "exact_taux": 0.9814,
22:   "f1": 0.4719,
23:   "tete": 0.647,
24:   "fr": 0.9744,
25:   "en": 1.0
26:  },
27:  "regle": "toute règle se règle sur dev et ne s'accepte que si test ne baisse pas",
28:  "limites": [
29:   "test petit (54 labels)",
30:   "règles dessinées sur l'ensemble",
31:   "gold 612"
32:  ]
33: }

(End of file - total 33 lines)
</content>
  ```

### 🤖 Assistant

⏵ Vérification des références README, roadmap et liens des fiches

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"=== STATUS reports/tools ===\"; git status --porcelain -- reports tools/pensee tools/bloc_linguistique.py tools/tests/linguistique docs/pilotage/roadmap.md; echo \"=== README refs ===\"; grep -n -E \"attachement-v2|attachement-v … [255 caractères tronqués]`

  ```
=== STATUS reports/tools ===
 M reports/pensee-quatre-modes.json
 M reports/rapport-spans-chunker.md
?? reports/rapport-s-paragraphes.md
=== README refs ===
18:| [`rapport-pensee-couverture-v7.md`](rapport-pensee-couverture-v7.md) | **B13** — la couverture **0,8201** : POS contextuel 0,7603, F1 **0,5595**, exact 195/196 |
19:| [`rapport-pensee-attachement-parfait.md`](rapport-pensee-attachement-parfait.md) | **B13** — l'attachement **187/187 (1,0000)** sur les spans prédits, fr 1,0 / en 1,0, dev 126/126, test 61/61 ; le rendement reste 0,7824 |
20:| [`rapport-pensee-couverture-v5.md`](rapport-pensee-couverture-v5.md) | **B13** — la couverture : **187 labels**, exact **185/187 (0,9893)**, F1 **0,5156**, dev/test 125/126 et 60/61 |
21:| [`rapport-gold-split.md`](rapport-gold-split.md) | **B13** — le gold dev/test : **test 0,9814**, dev 0,9811, la règle « régler sur dev, accepter si test ne baisse pas » |
22:| [`rapport-pensee-segmentation-v4.md`](rapport-pensee-segmentation-v4.md) | **B13** — la segmentation d'abord : F1 **0,4194**, exact **158/160**, couverture **160/239**, 183/183 |
30:| [`rapport-pensee-attachement-v3.md`](rapport-pensee-attachement-v3.md) | **B13** — l'attachemen
… [6572 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"=== roadmap B13 ===\"; grep -n -A4 -B2 \"B13\" docs/pilotage/roadmap.md | head -80; echo \"=== en-cours B13 ===\"; grep -n -A3 -B1 \"B13\" docs/pilotage/en-cours.md | head -60", "description": "Inspect roadmap and en-cours B13 r … [11 caractères tronqués]`

  ```
=== roadmap B13 ===
29-|---|---|---|---|
30-| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4, A6.2 bloqués** ; A2.6 partiel ; A3.2/A3.3 mesurées ; **A8.3c/d expliqués** ; **A2.6/A8.3 : le [lot](../theorie/glossaire/entrees/lot.md) ne divise pas les lectures denses (+27 % calcul, PPL −0,006 %)** | **A2.6** (experts : A6.2 bloqué) ; le lot ≥ 2 assumé |
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute appris
… [17607 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"=== link targets existence ===\"; for f in tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/gold_reel.py tools/pensee/autotest.py reports/rapport-audit-attachement.md reports/rapport-t … [391 caractères tronqués]`

  ```
=== link targets existence ===
OK   tools/bloc_linguistique.py
OK   tools/tests/linguistique/evaluer_gold.py
OK   tools/tests/linguistique/gold_reel.py
OK   tools/pensee/autotest.py
OK   reports/rapport-audit-attachement.md
OK   reports/rapport-topk-diagnostic.md
OK   reports/rapport-annotation-independante.md
OK   reports/rapport-classement-appris.md
OK   reports/rapport-pensee-conventions.md
OK   reports/rapport-echecs-v2.md
OK   reports/rapport-spans-chunker.md
OK   reports/rapport-gold-anglais.md
OK   tools/tests/linguistique/gold_split.py
  ```

### 🤖 Assistant

⏵ Inspection du code et des assertions au commit 69bd865e

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; git show 69bd865e:tools/pensee/autotest.py | grep -n -E \"195|196|0\\.8201|0\\.5595|0\\.7603|0\\.7205|166|0\\.6946|135/135|60/61|21.*REL|43\" | head -60", "description": "Grep v7 numbers in autotest at target commit"}`

  ```
694:def t43_curieuse() -> tuple[bool, str]:
1639:            and abs(r["pos"]["exactitude"] - 0.7603) < 0.001), (
1731:    return abs(f1 - 0.5595) < 0.001, f"union : segments F1 {f1} (S 0,4741)"
1743:    return abs(f1 - 0.5595) < 0.001 and abs(tete - 0.7205) < 0.001, (
1794:    return abs(r["fidelite"] - 0.196) < 0.001, (
1807:    return abs(fid - 0.196) < 0.001, f"sortie POS : fidélité {round(fid, 4)}"
2011:    ph = [p for p in charger() if 301 <= int(p["id"][1:]) <= 432]
2012:    sans = [p for p in ph if p["id"] in ("r428", "r429", "r430", "r431", "r432")]
2018:    """Le défaut de la fusion : la confiance (0,7424) bat le niveau (0,3432)."""
2034:    d = json.loads((racine / "reports/pensee-quatre-modes-432.json").read_text(encoding="utf-8"))
2054:    """L'élision : POS 0,7455 (+0,0011) sur les 432 phrases."""
2068:    d = json.loads((racine / "reports/pensee-quatre-modes-432-run2.json").read_text(encoding="utf-8"))
2074:def t143_defaut_conditionnel() -> tuple[bool, str]:
2097:    d = json.loads((racine / "reports/pensee-quatre-modes-432-run2.json").read_text(encoding="utf-8"))
2110:    d = json.loads((racine / "reports/pensee-quatre-modes-432-run3.json").read_text(encoding="utf-8
… [1790 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; git show 69bd865e:tools/bloc_linguistique.py | grep -n -E \"195|196|0\\.8201|0\\.5595|0\\.7603|0\\.7205|166|0\\.6946|135/135|60/61\" | head -40; echo \"=== autotest head ===\"; git show 69bd865e:tools/pensee/autotest.py | head -40", "d … [73 caractères tronqués]`

  ```
=== autotest head ===
#!/usr/bin/env python3
"""autotest.py — les portes du moteur de pensée : T0–T4, puis AC-3 et alpha-bêta.

  T0  le store est canonique          aller-retour exact, empreinte stable, ordres différents
  T1  l'arbre se rejoue               mêmes empreintes, mêmes scores ; une graine changée diverge
  T1  le flux DRVF thought se relit   enveloppe, racine, rejeu ; un score corrompu est refusé
  T2  une stratégie est substituable  même arbre, deux stratégies ; une stratégie aveugle échoue
  T3  le moteur est anytime           best-so-far non décroissant ; un budget nul est refusé
  T4  la justification est valide     chemin racine → settled ; un chemin inventé est refusé
  T5  AC-3 se branche                 une chaîne propage, une contradiction se voit, la carte
                                      arc-consistante ne se réduit pas (contrôle)
  T6  alpha-bêta décide               gagner en un coup, bloquer, couper ; le minimax exact
                                      visite plus de nœuds ; la profondeur 1 sans évaluation rate
  T6  alpha-bêta décide               gagner en un coup, bloquer, couper ; le minimax exact
                                      visite 
… [1399 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; sed -n '2320,2660p' tools/pensee/autotest.py", "description": "Inspect v7 assertion block in autotest"}`

  ```
return _role_gp("par") == "agent" and _role_gp("avec") == "moyen", (
        f"par → {_role_gp('par')}, avec → {_role_gp('avec')}")


def t160_passifs_sans_par() -> tuple[bool, str]:
    """Les passifs sans par : le chunker 3/3 patient."""
    import tools.bloc_linguistique as bl
    h = bl.Heuristique(segmenter_s=False)
    ok = 0
    for txt in ("Le livre est lu.", "La porte est ouverte.", "Les enfants sont partis."):
        a = h.analyser(txt, "fr")
        roles = [(e.meta or {}).get("role") for e in a.etiquettes
                 if e.niveau == "syntagme" and e.type == "GN"]
        if roles and roles[0] == "patient":
            ok += 1
    return ok == 3, f"passif sans par (chunker) : {ok}/3 patient"


def t161_cible_proximite() -> tuple[bool, str]:
    """La cible par proximité : le verbe du GV le plus proche."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    r = evaluer_bloc("h", bl.Heuristique(), charger())
    a, th = r["attachement"], r["attachement_tete"]
    return (a["cibles"] == 239 and a["top1"] == 195 and a["exact"] == 195), (
        f"proximité : top1 {a['top1']}/239, exact {a['exact']}/239, "
… [15363 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; sed -n '1,120p' tools/tests/linguistique/evaluer_gold.py; echo \"=== grep write ===\"; grep -n -E \"write|open\\(|json.dump|Path.*write|sauver\" tools/tests/linguistique/evaluer_gold.py | head -20", "description": "Inspect evaluer_gold … [33 caractères tronqués]`

  ```
"""evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) + synthétique (160).

Trois niveaux : POS (token, exact), syntagmes (exact + **par tête**), pragmatique. Quatre
lectures : heuristique, mock neuronal, parallèle, cascade. Le vrai modèle est optionnel
(`--reel`) : s'il ne répond pas, il est refusé, pas simulé.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections import Counter, defaultdict

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl  # noqa: E402

GOLD = pathlib.Path(__file__).with_name("gold.json")
REEL = pathlib.Path(__file__).with_name("gold_reel.json")
SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")


def charger() -> list[dict]:
    hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
    reel = json.loads(REEL.read_text(encoding="utf-8"))["phrases"]
    synth = json.loads(SYNTH.read_text(encoding="utf-8"))["phrases"]
    for p in hand:
        p["source"] = "hand"
    for p in reel:
        p["source"] = "reel"
    return hand + reel + synth


GELE = pathlib.Path(__file__).with_name("gold_ge
… [4108 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; sed -n '1600,1660p' tools/pensee/autotest.py; echo '=== tests 1725-1750 ==='; sed -n '1720,1755p' tools/pensee/autotest.py", "description": "Inspect POS and F1 assertions"}`

  ```
taux = [mesurer_cv(ps, graine=k)["taux"] for k in range(20)]
    moyenne = round(statistics.mean(taux), 4)
    ecart = round(statistics.pstdev(taux), 4)
    return abs(moyenne - 0.8467) < 0.01, (
        f"CV 20 graines : {moyenne} ± {ecart} (min {min(taux)}, max {max(taux)})")


def t106_bilan_anaphore() -> tuple[bool, str]:
    """Le bilan de l'anaphore : les huit mesures de la ligne en un seul contrôle."""
    import statistics
    from ..tests.linguistique.anaphore import (accords, mesurer, mesurer_cv,
                                               mesurer_hybride, mesurer_meta,
                                               mesurer_roles)
    from ..tests.linguistique.gold_reel import construire
    g = construire()
    court = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 328]
    court20 = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 320]
    objets = [p for p in g["phrases"] if 329 <= int(p["id"][1:]) <= 336]
    longs = [p for p in g["phrases"] if 337 <= int(p["id"][1:]) <= 342]
    tout = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 342]
    ok = (mesurer(court20, ignorer_pp=True)["taux"] == 1.0
          and mesurer(tout, ignorer_pp=True)["ju
… [3478 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; sed -n '1695,1735p' tools/pensee/autotest.py; echo \"=== eval attachement block ===\"; sed -n '120,240p' tools/tests/linguistique/evaluer_gold.py", "description": "Inspect union test gold source and attachment computation"}`

  ```
h2 = bl.Heuristique(union=False)
    h2.segmenter_s = False
    tp = fp = fn = 0
    for phrase in ph:
        a1 = h1.analyser(phrase["texte"], phrase["langue"])
        a2 = h2.analyser(phrase["texte"], phrase["langue"])
        gold = {(s["type"], s["debut"]) for s in phrase["segments"]}
        seg_s = [(e.type, e.debut, e.fin) for e in a1.etiquettes if e.niveau == "syntagme"]
        seg_c = [(e.type, e.debut, e.fin) for e in a2.etiquettes if e.niveau == "syntagme"]
        pred = set()
        for (t, d, f) in seg_s:
            cand = [cd for (ct, cd, cf) in seg_c if ct == t and d <= cd < f]
            pred.add((t, cand[0] if cand else d))
        tp += len(pred & gold); fp += len(pred - gold); fn += len(gold - pred)
    p = tp / max(1, tp + fp); r = tp / max(1, tp + fn); f1 = round(2 * p * r / max(1e-9, p + r), 4)
    return abs(f1 - 0.7265) < 0.001, (
        f"hybride : tête F1 {f1} (S 0,3552, chunker 0,4707)")


def t112_union() -> tuple[bool, str]:
    """L'union des segmenteurs : segments F1 0,2833 (S 0,1722), tête 0,5027."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger, _seg, _tete
    ph = charger
… [7816 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Exécution du code du commit pour reproduire les chiffres de la v7

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. timeout 600 python3 - <<'PY'\nimport json\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger, charger_gele, evaluer_bloc, _seg, _tete\n\ndef spans_cat … [2345 caractères tronqués]`

  ```
n living 612 n gele 602
=== living phrases 612
pos 0.7581 tokens 3179
syntagme 0.5555 tete 0.7152 tp/fp/fn 969 657 894
attachement {"cibles": 239, "labels": 196, "top1": 195, "topk": 166, "exact": 195, "top1_taux": 0.8159, "topk_taux": 0.6946, "exact_taux": 0.8159, "exact_any": 195, "exact_any_taux_span": 0.9949, "top1_taux_span": 0.9949, "topk_taux_span": 0.8469, "topk_exact": 166, "topk_exact_taux": 0.6946, "topk_exact_taux_span": 0.8469, "exact_taux_span": 0.9949, "verbe": {"cibles": 137, "justes": 136, "taux": 0.9927}, "nom": {"cibles": 59, "justes": 59, "taux": 1.0}, "couverture": 0.8201}
par_langue {"fr": {"cibles": 151, "labels": 135, "exact": 135, "topk": 121, "exact_taux_span": 1.0}, "en": {"cibles": 88, "labels": 61, "exact": 60, "topk": 45, "exact_taux_span": 0.9836}}
union (0.5555, 0.7152, (969, 657, 894))
=== gele phrases 602
pos 0.7603 tokens 3141
syntagme 0.5595 tete 0.7205 tp/fp/fn 962 646 869
attachement {"cibles": 239, "labels": 196, "top1": 195, "topk": 166, "exact": 195, "top1_taux": 0.8159, "topk_taux": 0.6946, "exact_taux": 0.8159, "exact_any": 195, "exact_any_taux_span": 0.9949, "top1_taux_span": 0.9949, "topk_taux_span": 0.8469, "topk_exact": 166, "topk_exac
… [478 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; grep -n -E \"0\\.4741|0\\.5858|0\\.7475|0\\.7603|0\\.5595|0\\.5555|0\\.7205|0\\.7152\" tools/pensee/autotest.py tools/bloc_linguistique.py | head -40", "description": "Search for per-segmenter F1 and POS before values"}`

  ```
tools/pensee/autotest.py:1639:            and abs(r["pos"]["exactitude"] - 0.7603) < 0.001), (
tools/pensee/autotest.py:1684:    return (abs(f1 - 0.4741) < 0.001 and abs(f2 - 0.5858) < 0.001
tools/pensee/autotest.py:1731:    return abs(f1 - 0.5595) < 0.001, f"union : segments F1 {f1} (S 0,4741)"
tools/pensee/autotest.py:1743:    return abs(f1 - 0.5595) < 0.001 and abs(tete - 0.7205) < 0.001, (
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; git log --oneline --all -S\"0.5555\" -- tools/pensee/autotest.py tools/bloc_linguistique.py | head; echo \"=== v6 commit tests ===\"; git show 0ec6c27d:tools/pensee/autotest.py | grep -n -E \"0\\.5595|0\\.5555|0\\.7603|0\\.7475|0\\.513 … [95 caractères tronqués]`

  ```
=== v6 commit tests ===
1634:    from ..tests.linguistique.evaluer_gold import charger_gele as charger, evaluer_bloc
1639:            and abs(r["pos"]["exactitude"] - 0.7475) < 0.001), (
1673:    from ..tests.linguistique.evaluer_gold import charger_gele as charger, evaluer_bloc
1692:    from ..tests.linguistique.evaluer_gold import charger_gele as charger, _tete
1717:    from ..tests.linguistique.evaluer_gold import charger_gele as charger, _seg, _tete
1737:    from ..tests.linguistique.evaluer_gold import charger_gele as charger, evaluer_bloc
1743:    return abs(f1 - 0.5156) < 0.001 and abs(tete - 0.6826) < 0.001, (
1750:    from ..tests.linguistique.evaluer_gold import charger_gele as charger, evaluer_bloc
1765:    from ..tests.linguistique.evaluer_gold import charger_gele as charger
1790:    from ..tests.linguistique.evaluer_gold import charger_gele as charger
1801:    from ..tests.linguistique.evaluer_gold import charger_gele as charger
1813:    from ..tests.linguistique.evaluer_gold import charger_gele as charger
1825:    from ..tests.linguistique.evaluer_gold import charger_gele as charger
1841:    from ..tests.linguistique.evaluer_gold import charger_gele as charger
1853:  
… [466 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle des mentions d'historique et des instantanés de chaque fiche

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; for f in reports/rapport-pensee-attachement-v2.md reports/rapport-pensee-attachement-v3.md reports/rapport-pensee-segmentation-v4.md reports/rapport-pensee-couverture-v5.md reports/rapport-pensee-attachement-parfait.md reports/rapport- … [294 caractères tronqués]`

  ```
=== reports/rapport-pensee-attachement-v2.md
3:> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
=== reports/rapport-pensee-attachement-v3.md
3:> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
=== reports/rapport-pensee-segmentation-v4.md
3:> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
=== reports/rapport-pensee-couverture-v5.md
3:> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
29:| mesure | v4 (committée) | **v5** |
=== reports/rapport-pensee-attachement-parfait.md
3:> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
=== reports/rapport-pensee-couverture-v7.md
3:> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
=== reports/rapport-gold-split.md
3:> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"=== v3 MD diff dcf7bc91 -> HEAD ===\"; git diff dcf7bc91..HEAD -- reports/rapport-pensee-attachement-v3.md; echo \"=== v3 JSON diff dcf7bc91 -> HEAD ===\"; git diff dcf7bc91..HEAD -- reports/pensee-attachement-v3.json", "descrip … [47 caractères tronqués]`

  ```
=== v3 MD diff dcf7bc91 -> HEAD ===
diff --git a/reports/rapport-pensee-attachement-v3.md b/reports/rapport-pensee-attachement-v3.md
index 59fc8a63..67506b58 100644
--- a/reports/rapport-pensee-attachement-v3.md
+++ b/reports/rapport-pensee-attachement-v3.md
@@ -21,18 +21,24 @@
 | top-k strict | 141 (0,9724) | **142 (0,9793)** | +1 |
 | cibles verbes (POS gold) | 111/116 (0,9569) | **112/116 (0,9655)** | +1 |
 | **cibles noms (POS gold)** | 26/29 (0,8966) | **29/29 (1,0000)** | **+3** |
+| exact multi-cibles (`cible in cibles`) | — | **143/145 (0,9862)** | mesure secondaire (A13) |
+
+> **Note A13 (multi-cibles)** : le gold admet deux cibles pour **43/96 GP** ; adopter `cible in cibles`
+> donnerait **143/145 (98,62 %)** et 143/239 (59,83 %), avec « +2 cas, dont 2 synthétiques »
+> (s108, s122) — McNemar p=0,5 : correction de 2 cas, pas un gain de population. L'exact
+> conservateur (`cibles[0]`) reste la mesure principale ; `exact_any` est publié à côté (T179).
 
 Rendement global (÷ 239 cibles) : top1 **0,5983**, top-k 0,5941, exact **0,5900**.
 
 ## 2. Les trois règles (et celles qui ne le sont pas)
 
-| règle | répare | portée | régression |
-|---|---|---:|---:|
-| **R2** — un 
… [1083 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de l'audit de cohérence antérieur comme modèle

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; ls -la reports/*coherence* 2>&1; echo \"=== audit v2 ===\"; sed -n '1,140p' reports/rapport-audit-v2.md 2>&1 | head -140", "description": "List coherence files and read audit v2"}`

  ```
-rw-r--r--. 1 stephane stephane 34150  5 nov 14:41 reports/pensee-coherence-fiches.json
-rw-r--r--. 1 stephane stephane 30570 28 oct 14:07 reports/rapport-coherence-docs-2.md
-rw-r--r--. 1 stephane stephane 12367 28 oct 14:07 reports/rapport-coherence-docs-3.md
-rw-r--r--. 1 stephane stephane 29105 28 oct 09:17 reports/rapport-coherence-docs.md
-rw-------. 1 stephane stephane 38511  5 nov 14:41 reports/rapport-coherence-fiches.md
-rw-r--r--. 1 stephane stephane 14824 28 oct 09:17 reports/rapport-coherence-vision.md
=== audit v2 ===
# Audit B13 — l'attachement v2 : 43 valeurs rejouées, 2 arrondis, 1 erreur de prose (46 → 45), 8 docstrings de portes périmées

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅ **chiffres reproduits** ;
> ⚠️ **réserves documentaires** (§ 3, § 4, § 6) — aucune ne change les totaux.
>
> **Audité** : commit **`9d5337ce`** (2026-11-05 14:14), fiche
> [`rapport-pensee-attachement-v2.md`](rapport-pensee-attachement-v2.md) et JSON
> [`pensee-attachement-v2.json`](pensee-attachement-v2.json).
>
> **Dispositif** : depuis la racine, `sys.path.insert(0, '.')` ;
> `evaluer_bloc("h", Heuristique(), charger())` ; l
… [8259 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; sed -n '1,160p' reports/rapport-coherence-fiches.md 2>&1", "description": "Read previous coherence report"}`

  ```
# Cohérence des fiches B13 du 2026-11-05 — vérification

> **Date de vérification** : 2026-11-05T13:54-05:00, **arrêtée avant l'intégration v2, committée
> à 14:11 dans `9d5337ce`** · **Branche** : `s/v7` · **Périmètre** : les **11 fiches B13 datées du 2026-11-05** et
> leurs 11 JSON homonymes (`reports/`), confrontés aux portes de `tools/pensee/autotest.py`
> (T153, T161, T162, T163, T166, T167, T168, T169, T172, T173, plus les portes propres des
> fiches : T164, T165, T170, T171, T174).
> **Verdict global** : ✅ **8 fiches cohérentes** avec leur JSON et leur porte d'époque ; ❌ **3 fiches
> portaient une divergence réelle** (7 écarts : 4 valeurs fausses dans `lexique-elargi`, 2 incohérences
> de dénombrement dans `spans`, 1 attribution inexacte dans `denominateur`) **au blob d'origine** ;
> elles ont été **corrigées par le parent** dans `9d5337ce` (v2) et `2e08cbc7` (`lexique-elargi`,
> `denominateur`) — **je n'ai corrigé aucune fiche**. Les corrections sont partielles : **3 résidus**
> subsistent (§ 4.5) ; 🕓 **7 paliers historiques reconnus** (verbe-gv → attachement-cible), plus les
> colonnes « avant » de `lexique-elargi`.
> **⚠️ v2 committée** : `9d5337ce` (HEAD) change les port
… [14368 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction des assertions de chaque commit pour confronter les fiches historiques

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; for c in 9d5337ce e1903e2d 392f03aa b975011b 0ec6c27d 85e4082b 69bd865e; do echo \"########## $c ##########\"; git show $c:tools/pensee/autotest.py | grep -n -E \"0\\.9448|0\\.9724|0\\.9655|0\\.9793|111|112/116|26/29|29/29|0\\.4539|0\\ … [251 caractères tronqués]`

  ```
########## 9d5337ce ##########
2:"""autotest.py — les portes du moteur de pensée : T0–T4, puis AC-3 et alpha-bêta.
25:Usage : PYTHONPATH=. ~/gpu-env/bin/python tools/pensee/autotest.py
1263:def t80_phase_devinee() -> tuple[bool, str]:
1264:    """La phase devinée : signal bruité à 90 %, 0/20 au but 0, 20/20 au but 1 (négatif)."""
1279:    return ok0 == 0 and ok1 == 20, (f"phase devinée : but 0 {ok0}/20, "
1343:    from ..tests.linguistique.gold_reel import construire
1352:    from ..tests.linguistique.gold_reel import construire
1353:    from ..tests.linguistique.evaluer_gold import evaluer_bloc
1371:    from ..tests.linguistique.gold_reel import construire
1372:    from ..tests.linguistique.evaluer_gold import evaluer_bloc
1385:    from ..tests.linguistique.gold_reel import construire
1386:    from ..tests.linguistique.evaluer_gold import evaluer_bloc
1399:    from ..tests.linguistique.gold_reel import construire
1400:    from ..tests.linguistique.evaluer_gold import evaluer_bloc
1413:    from ..tests.linguistique.gold_reel import construire
1414:    from ..tests.linguistique.evaluer_gold import evaluer_bloc
1427:    from ..tests.linguistique.gold_reel import construire
1428:    f
… [17568 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; for c in 9d5337ce e1903e2d 392f03aa b975011b 0ec6c27d 85e4082b; do git show $c:tools/pensee/autotest.py > /tmp/autotest_$c.py; echo \"########## $c ##########\"; grep -n -E \"def t1(6[1-9]|7[0-9]|8[0-9])|exact.*==|labels.*==|topk.*==|t … [200 caractères tronqués]`

  ```
########## 9d5337ce ##########
2338:def t161_cible_proximite() -> tuple[bool, str]:
2343:    a, th = r["attachement"], r["attachement_tete"]
2344:    return (a["cibles"] == 239 and a["top1"] == 140 and a["exact"] == 137), (
2346:        f"tête {th['top1']}/145")
2349:def t162_candidats_verbes() -> tuple[bool, str]:
2354:    a, th = r["attachement"], r["attachement_tete"]
2355:    return (a["topk"] == 142 and th["topk"] == 142 and a["top1"] == 140), (
2356:        f"candidats : top-k {a['topk']}/239 ({a['topk_taux']}), tête {th['topk']}/145")
2359:def t163_echecs_attachement() -> tuple[bool, str]:
2367:        labels = {(e.type, e.debut, e.fin): e for e in a.etiquettes if e.niveau == "syntagme"}
2382:def t164_verbe_gv() -> tuple[bool, str]:
2391:    return cible == "saw" and r["exact"] == 137, (
2395:def t165_lexique_verbal() -> tuple[bool, str]:
2406:def t166_spans() -> tuple[bool, str]:
2426:def t167_denominateur() -> tuple[bool, str]:
2431:    return (a["cibles"] == 239 and a["labels"] == 145
2432:            and abs(a["top1_taux_span"] - 0.9655) < 0.001
2433:            and abs(a["topk_taux_span"] - 0.9793) < 0.001
2434:            and abs(a["exact_taux_span"] - 0.9448) < 0.001)
… [20242 caractères tronqués]
  ```

- **bash** `{"command": "for c in 392f03aa b975011b 0ec6c27d 85e4082b; do echo \"########## $c ##########\"; grep -n -E \"def t11[23]|0\\.4539|0\\.4194|0\\.5156|0\\.513|0\\.6826|0\\.6432|head|gold_split|104|53/54|0\\.9811|0\\.9814|0\\.4414|0\\.4719|0\\.6347|0\\.647\" /tmp/autotest_$c.py | head -30; done", "desc … [58 caractères tronqués]`

  ```
########## 392f03aa ##########
1582:def t104_cv() -> tuple[bool, str]:
1714:def t112_union() -> tuple[bool, str]:
1731:    return abs(f1 - 0.4539) < 0.001, f"union : segments F1 {f1} (S 0,4285)"
1734:def t113_union_defaut() -> tuple[bool, str]:
1743:    return abs(f1 - 0.4539) < 0.001 and abs(tete - 0.6432) < 0.001, (
2749:              ("T104 validation croisée", t104_cv()),
########## b975011b ##########
1582:def t104_cv() -> tuple[bool, str]:
1714:def t112_union() -> tuple[bool, str]:
1731:    return abs(f1 - 0.5156) < 0.001, f"union : segments F1 {f1} (S 0,4577)"
1734:def t113_union_defaut() -> tuple[bool, str]:
1743:    return abs(f1 - 0.5156) < 0.001 and abs(tete - 0.6826) < 0.001, (
2749:              ("T104 validation croisée", t104_cv()),
########## 0ec6c27d ##########
1582:def t104_cv() -> tuple[bool, str]:
1714:def t112_union() -> tuple[bool, str]:
1731:    return abs(f1 - 0.5156) < 0.001, f"union : segments F1 {f1} (S 0,4577)"
1734:def t113_union_defaut() -> tuple[bool, str]:
1743:    return abs(f1 - 0.5156) < 0.001 and abs(tete - 0.6826) < 0.001, (
2749:              ("T104 validation croisée", t104_cv()),
########## 85e4082b ##########
1582:def t104_cv() -> tuple[bool
… [315 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; for c in 0ec6c27d b975011b; do echo \"########## $c t168-t169 ##########\"; awk '/^def t168_classement/,/^def t170/' /tmp/autotest_$c.py | head -40; done; echo \"=== v6 gold split tests ===\"; grep -n -i \"gold_split\\|dev\\b\\|test\\b … [104 caractères tronqués]`

  ```
########## 0ec6c27d t168-t169 ##########
def t168_classement() -> tuple[bool, str]:
    """Le classement : la cible réduite à sa tête et les deux conventions du gold (POS gold)."""
    import tools.bloc_linguistique as bl
    h = bl.Heuristique()
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    r = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
    bl2 = bl
    ch2 = charger
    verbes = noms = 0
    for ph in ch2():
        a2 = h.analyser(ph["texte"], ph["langue"])
        lab = {(e.type, e.debut, e.fin): e for e in a2.etiquettes if e.niveau == "syntagme"}
        for s2 in ph["segments"]:
            c2 = s2.get("cibles") or ([s2["cible"]] if s2.get("cible") else [])
            if not c2 or (s2["type"], s2["debut"], s2["fin"]) not in lab:
                continue
            pos = next((m["pos"] for m in ph.get("mots", [])
                        if ph["texte"][m["debut"]:m["fin"]] == c2[0]), None)
            if (pos == "VERB") if pos else bl2._est_verbe(c2[0]):
                verbes += 1
            else:
                noms += 1
    return (r["exact"] == 187 and verbes == 131 and noms == 56), (
        f"classement : exact {r['exac
… [3378 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mesure de la v6 sur le gold vivant et le gold gelé

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; rm -rf /tmp/qtrinet-v6; git worktree add --detach /tmp/qtrinet-v6 0ec6c27d >/tmp/wt.log 2>&1 && echo \"worktree OK\" || (cat /tmp/wt.log; exit 1); cd /tmp/qtrinet-v6; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. timeout 600 python3 - <<'PY'\ … [789 caractères tronqués]`

  ```
worktree OK
living n 612 pos 0.7461 f1 0.5321 tete 0.6966
  cibles 239 labels 156 top1 136 topk 94 exact 135 fr {'cibles': 151, 'labels': 96, 'exact': 75, 'topk': 52, 'exact_taux_span': 0.7812} en {'cibles': 88, 'labels': 60, 'exact': 60, 'topk': 42, 'exact_taux_span': 1.0} verbe {'cibles': 110, 'justes': 90, 'taux': 0.8182} nom {'cibles': 46, 'justes': 45, 'taux': 0.9783}
gele n 602 pos 0.7482 f1 0.5351 tete 0.7006
  cibles 239 labels 156 top1 136 topk 94 exact 135 fr {'cibles': 151, 'labels': 96, 'exact': 75, 'topk': 52, 'exact_taux_span': 0.7812} en {'cibles': 88, 'labels': 60, 'exact': 60, 'topk': 42, 'exact_taux_span': 1.0} verbe {'cibles': 110, 'justes': 90, 'taux': 0.8182} nom {'cibles': 46, 'justes': 45, 'taux': 0.9783}
  ```

- **bash** `{"command": "cd /tmp/qtrinet-v6; git status --short | head; echo \"=== hashes ===\"; sha256sum tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py; git show 0ec6c27d:tools/bloc_linguistique.py | sha256sum; git show 0ec6c27d:tools/tests/linguistique/evaluer_gold.py | sha256sum; echo \ … [401 caractères tronqués]`

  ```
=== hashes ===
8358c99d3e08d933d6b81555687b731c783502249f82f8f0cdbd7d15a00596f7  tools/bloc_linguistique.py
630bc8eab79213203c97ef87f425e92e540a3d50270dbd75482c409e4623b221  tools/tests/linguistique/evaluer_gold.py
8358c99d3e08d933d6b81555687b731c783502249f82f8f0cdbd7d15a00596f7  -
630bc8eab79213203c97ef87f425e92e540a3d50270dbd75482c409e4623b221  -
=== module files ===
/tmp/qtrinet-v6/tools/bloc_linguistique.py
/tmp/qtrinet-v6/tools/tests/linguistique/evaluer_gold.py
g001 612
['/tmp/qtrinet-v6/tools', '/tmp/qtrinet-v6']
  ```

- **bash** `{"command": "awk '/^def t161_cible_proximite/,/^def t163/' /tmp/autotest_0ec6c27d.py; echo '--- t167 ---'; awk '/^def t167_denominateur/,/^def t168/' /tmp/autotest_0ec6c27d.py; echo '--- eval head 0ec6 ---'; cd /tmp/qtrinet-v6; grep -n \"def charger\\|GOLD\\|REEL\\|SYNTH\\|GELE\" tools/tests/linguis … [142 caractères tronqués]`

  ```
def t161_cible_proximite() -> tuple[bool, str]:
    """La cible par proximité : le verbe du GV le plus proche."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    r = evaluer_bloc("h", bl.Heuristique(), charger())
    a, th = r["attachement"], r["attachement_tete"]
    return (a["cibles"] == 239 and a["top1"] == 187 and a["exact"] == 187), (
        f"proximité : top1 {a['top1']}/239, exact {a['exact']}/239, "
        f"tête {th['top1']}/145")


def t162_candidats_verbes() -> tuple[bool, str]:
    """Les candidats verbes : le top-k atteint 142/145 (0,9793) après les têtes."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    r = evaluer_bloc("h", bl.Heuristique(), charger())
    a, th = r["attachement"], r["attachement_tete"]
    return (a["topk"] == 161 and th["topk"] == 161 and a["top1"] == 187), (
        f"candidats : top-k {a['topk']}/239 ({a['topk_taux']}), tête {th['topk']}/145")


def t163_echecs_attachement() -> tuple[bool, str]:
--- t167 ---
def t167_denominateur() -> tuple[bool, str]:
    """Le dénominateur : rendement global (÷ 239) et e
… [1576 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qtrinet-v6; echo \"=== tracked? ===\"; git ls-files -s tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json tools/tests/linguistique/gold_synthetique.json tools/tests/linguistique/gold_gele.json; echo \"=== blobs vs HEAD worktree ===\"; for f in gold.json g … [516 caractères tronqués]`

  ```
=== tracked? ===
100644 246a2ea2cd8c635d5b5cc6cc73b1e4b6f6919bff 0	tools/tests/linguistique/gold.json
100644 ecde7bf9be5616850f989f26e2a52462cb91a178 0	tools/tests/linguistique/gold_gele.json
100644 d45d743c183411da7067f59a1ea5cbb4cb0e6203 0	tools/tests/linguistique/gold_reel.json
100644 4307946ca1b672d260052a348611fdfc1e4cc45f 0	tools/tests/linguistique/gold_synthetique.json
=== blobs vs HEAD worktree ===
gold.json
3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a  -
3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a  tools/tests/linguistique/gold.json
gold_reel.json
05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11  -
05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11  tools/tests/linguistique/gold_reel.json
gold_synthetique.json
e3e704ce9cb599db07ab31d1b0651f0aa12ea9ecad31ca8bf558efdeed84a654  -
e3e704ce9cb599db07ab31d1b0651f0aa12ea9ecad31ca8bf558efdeed84a654  tools/tests/linguistique/gold_synthetique.json
gold_gele.json
f2632969fbe38f67320deae3dc0052b607ffd79fcbeec29cb55d08dbb34105f1  -
f2632969fbe38f67320deae3dc0052b607ffd79fcbeec29cb55d08dbb34105f1  tools/tests/linguistique/gold_gele.json
=== run t167 ===
t161_cible_pr
… [233 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"=== diff b975011b..0ec6c27d bloc ===\"; git diff --stat b975011b..0ec6c27d -- tools/bloc_linguistique.py tools/pensee/autotest.py tools/tests/linguistique/gold*.json; echo \"=== diff 0ec6c27d..69bd865e bloc ===\"; git diff --sta … [345 caractères tronqués]`

  ```
=== diff b975011b..0ec6c27d bloc ===
 tools/bloc_linguistique.py | 31 ++++++++++++++++++++++++++++---
 tools/pensee/autotest.py   | 28 ++++++++++++++--------------
 2 files changed, 42 insertions(+), 17 deletions(-)
=== diff 0ec6c27d..69bd865e bloc ===
 tools/bloc_linguistique.py | 89 +++++++++++++++++++++++++++-------------------
 tools/pensee/autotest.py   | 82 +++++++++++++++++++++---------------------
 2 files changed, 94 insertions(+), 77 deletions(-)
=== v6 code grep externes ===
25:    python3 tools/bloc_linguistique.py --autotest --udhr data/udhr/articles.jsonl
49:RACINE = pathlib.Path(__file__).resolve().parent.parent
158:def charger_profils_udhr(chemin: pathlib.Path, train=(0, 14), test=(15, 30),
167:    for ligne in chemin.read_text(encoding="utf-8").splitlines():
170:        d = json.loads(ligne)
627:            if str(RACINE / "tools/structures") not in sys.path:
628:                sys.path.insert(0, str(RACINE / "tools/structures"))
1262:    def __init__(self, modele: str | pathlib.Path, llama_cli: str = "llama-cli",
1283:        if not pathlib.Path(self.modele).exists():
1298:            d = json.loads(texte_sortie[debut:fin + 1])
1351:    def __init__(self, modele:
… [1434 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; git diff b975011b..0ec6c27d -- tools/bloc_linguistique.py | head -120", "description": "Show v6 code diff from v5"}`

  ```
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 28d12dc5..4db853e2 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -438,6 +438,17 @@ am is are was were be been being have has had having do does did done
 """.split())
 
 
+ADVERBES_SEULS = {"peut-être", "vite", "bien", "mal", "hier", "demain", "aujourd'hui", "ici",
+                  "là", "souvent", "toujours", "jamais", "déjà", "encore", "enfin", "alors",
+                  "puis", "donc", "aussi", "très", "trop", "plus", "moins", "maybe", "perhaps"}
+
+
+def _est_adverbe_seul(g: dict) -> bool:
+    """Un GV d'un seul token adverbe n'est pas un gouverneur (« Peut-être »)."""
+    return (len((g.get("texte") or "").split()) == 1
+            and _normaliser(g.get("texte") or "") in ADVERBES_SEULS)
+
+
 ENCLITIQUES = ("-moi", "-toi", "-nous", "-vous", "-le", "-la", "-les", "-lui", "-leur", "-y", "-en")
 
 
@@ -645,6 +656,8 @@ class Heuristique:
         if segment.get("type") == "REL" and precedent.get("type") == "GN":
             return Heuristique._tete_nom(texte, precedent["debut"], precedent["fin"])
         if segment.get("type") == "SUB" and precedent.get("type") == "GV":
… [4513 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; git show 0ec6c27d:tools/bloc_linguistique.py > /tmp/bloc_v6.py; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. timeout 600 python3 - <<'PY'\nimport importlib.util, pathlib, sys\nspec = importlib.util.spec_from_file_location(\"bloc_v6\", \"/tmp … [962 caractères tronqués]`

  ```
living n 612 labels 187 exact 187 topk 161 fr 127 / 127 en 60 / 60 f1 0.513 tete 0.6785 pos 0.7461
gele n 602 labels 187 exact 187 topk 161 fr 127 / 127 en 60 / 60 f1 0.5164 tete 0.6834 pos 0.7482
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; for c in 9d5337ce e1903e2d 392f03aa b975011b 0ec6c27d 69bd865e; do echo \"=== $c ===\"; for f in gold.json gold_reel.json gold_synthetique.json gold_gele.json; do printf \"%-22s \" \"$f\"; git show $c:tools/tests/linguistique/$f 2>/dev … [258 caractères tronqués]`

  ```
=== 9d5337ce ===
gold.json              3663be6cea2f22e2
gold_reel.json         05d4f6dfae67dc72
gold_synthetique.json  e3e704ce9cb599db
gold_gele.json         f2632969fbe38f67
=== e1903e2d ===
gold.json              3663be6cea2f22e2
gold_reel.json         05d4f6dfae67dc72
gold_synthetique.json  e3e704ce9cb599db
gold_gele.json         f2632969fbe38f67
=== 392f03aa ===
gold.json              3663be6cea2f22e2
gold_reel.json         05d4f6dfae67dc72
gold_synthetique.json  e3e704ce9cb599db
gold_gele.json         f2632969fbe38f67
=== b975011b ===
gold.json              3663be6cea2f22e2
gold_reel.json         05d4f6dfae67dc72
gold_synthetique.json  e3e704ce9cb599db
gold_gele.json         f2632969fbe38f67
=== 0ec6c27d ===
gold.json              3663be6cea2f22e2
gold_reel.json         05d4f6dfae67dc72
gold_synthetique.json  e3e704ce9cb599db
gold_gele.json         f2632969fbe38f67
=== 69bd865e ===
gold.json              3663be6cea2f22e2
gold_reel.json         05d4f6dfae67dc72
gold_synthetique.json  e3e704ce9cb599db
gold_gele.json         f2632969fbe38f67
=== evaluer_gold diffs ===
 tools/tests/linguistique/evaluer_gold.py | 20 ++++++++++++-
 tools/tests/linguistique/gold_split.py   | 50 +++
… [79 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; git diff 9d5337ce..69bd865e -- tools/tests/linguistique/evaluer_gold.py", "description": "Show evaluer_gold changes"}`

  ```
diff --git a/tools/tests/linguistique/evaluer_gold.py b/tools/tests/linguistique/evaluer_gold.py
index c8e05b00..b25e8677 100644
--- a/tools/tests/linguistique/evaluer_gold.py
+++ b/tools/tests/linguistique/evaluer_gold.py
@@ -85,6 +85,9 @@ def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
     fractions = []
     att_n = att_labels = att_top1 = att_topk = att_exact = 0
     att_topk_exact = 0
+    att_exact_any = 0
+    par_langue = {"fr": {"cibles": 0, "labels": 0, "exact": 0, "topk": 0},
+                  "en": {"cibles": 0, "labels": 0, "exact": 0, "topk": 0}}
     att_v_n = att_v_ok = att_n_n = att_n_ok = 0
     att_t_n = att_t_labels = att_t_top1 = att_t_topk = 0
     for phrase in phrases:
@@ -113,20 +116,28 @@ def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
         tfp += len(pred_tete - gold_tete)
         tfn += len(gold_tete - pred_tete)
         labels = {(e.type, e.debut, e.fin): e for e in a.etiquettes if e.niveau == "syntagme"}
+        langue = phrase.get("langue", "fr")
+        bloc_langue = par_langue.get(langue, par_langue["fr"])
         for s in phrase["segments"]:
             cibles = s.get("cibles") or ([s["cible"]] if s.get("c
… [3246 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reproduction des mesures historiques v2→v6 avec les blobs du commit

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; cat > /tmp/mesure_hist.py <<'PY'\nimport importlib.util, pathlib, sys, json\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.insert(0, str(RACINE))\nfrom tools.tests.linguistique.evaluer_gold import … [1924 caractères tronqués]`

  ```
{"commit": "9d5337ce", "living": {"n": 612, "labels": 145, "exact": 137, "top1": 140, "topk": 142, "topk_exact": 141, "exact_any": 139, "fr": [109, 117], "en": [28, 28], "verbe": [111, 116], "nom": [26, 29], "f1": 0.2862, "tete": 0.4989, "pos": 0.7455, "couverture": 0.6067, "topk_taux": 0.5941, "exact_span": 0.9448}, "gele": {"n": 602, "labels": 145, "exact": 137, "top1": 140, "topk": 142, "topk_exact": 141, "exact_any": 139, "fr": [109, 117], "en": [28, 28], "verbe": [111, 116], "nom": [26, 29], "f1": 0.2895, "tete": 0.5053, "pos": 0.7475, "couverture": 0.6067, "topk_taux": 0.5941, "exact_span": 0.9448}}
{"commit": "e1903e2d", "living": {"n": 612, "labels": 145, "exact": 141, "top1": 143, "topk": 142, "topk_exact": 142, "exact_any": 143, "fr": [113, 117], "en": [28, 28], "verbe": [112, 116], "nom": [29, 29], "f1": 0.2862, "tete": 0.4989, "pos": 0.7455, "couverture": 0.6067, "topk_taux": 0.5941, "exact_span": 0.9724}, "gele": {"n": 602, "labels": 145, "exact": 141, "top1": 143, "topk": 142, "topk_exact": 142, "exact_any": 143, "fr": [113, 117], "en": [28, 28], "verbe": [112, 116], "nom": [29, 29], "f1": 0.2895, "tete": 0.5053, "pos": 0.7475, "couverture": 0.6067, "topk_taux": 0.594
… [1856 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; sed -n '1,160p' tools/tests/linguistique/gold_split.py", "description": "Read gold_split API"}`

  ```
"""gold_split.py — le gold 612 coupé en **dev** et **test**, de façon déterministe.

Le problème. Toutes les mesures de la session sont **in-sample** : les règles de segmentation et
d'attachement ont été dessinées en regardant les échecs du même gold qui les mesure. Pour juger
une règle, il faut un gold **tenu à l'écart** : on règle sur `dev`, on évalue sur `test`.

Protocole (fixé ici). Le split est un **hash stable de l'identifiant** (`crc32(id) % 3 == 0` →
test, sinon dev), donc reproductible, insensible à l'ordre et indépendant du contenu. Il est
**stratifié par source** (`hand`, `reel`, `synthetique`) et par langue : on vérifie l'équilibre
dans la fiche. Aucune phrase n'est dupliquée entre les deux ; l'union redonne les 612.

Usage :
    from tools.tests.linguistique.gold_split import dev, test, compter
    ph = charger(); d = dev(ph); t = test(ph)
"""
from __future__ import annotations

import zlib

PART_TEST = 3  # une phrase sur trois va au test


def _est_test(phrase: dict) -> bool:
    return zlib.crc32(str(phrase.get("id", "")).encode()) % PART_TEST == 0


def dev(phrases: list[dict]) -> list[dict]:
    """Les phrases de développement (2/3)."""
    return [p for p in phr
… [708 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reproduction des splits dev/test et des mesures de la fiche gold-split

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; cat > /tmp/mesure_split.py <<'PY'\nimport importlib.util, pathlib, sys, json\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.insert(0, str(RACINE))\nfrom tools.tests.linguistique.evaluer_gold impor … [1562 caractères tronqués]`

  ```
{"commit": "392f03aa", "dev": {"phrases": 422, "cibles": 163, "sources": {"hand": 15, "reel": 302, "synthetique": 105}, "langues": {"fr": 277, "en": 145}, "labels": 106, "exact": 104, "f1": 0.4414, "tete": 0.6347, "fr": [79, 79], "en": [25, 27], "couverture": 0.6503}, "test": {"phrases": 190, "cibles": 76, "sources": {"hand": 5, "reel": 130, "synthetique": 55}, "langues": {"fr": 125, "en": 65}, "labels": 54, "exact": 53, "f1": 0.4719, "tete": 0.647, "fr": [38, 39], "en": [15, 15], "couverture": 0.7105}}
{"commit": "b975011b", "dev": {"phrases": 422, "cibles": 163, "sources": {"hand": 15, "reel": 302, "synthetique": 105}, "langues": {"fr": 277, "en": 145}, "labels": 126, "exact": 126, "f1": 0.5091, "tete": 0.6782, "fr": [88, 88], "en": [38, 38], "couverture": 0.773}, "test": {"phrases": 190, "cibles": 76, "sources": {"hand": 5, "reel": 130, "synthetique": 55}, "langues": {"fr": 125, "en": 65}, "labels": 61, "exact": 60, "f1": 0.5217, "tete": 0.6792, "fr": [38, 39], "en": [22, 22], "couverture": 0.8026}}
{"commit": "0ec6c27d", "dev": {"phrases": 422, "cibles": 163, "sources": {"hand": 15, "reel": 302, "synthetique": 105}, "langues": {"fr": 277, "en": 145}, "labels": 126, "exact": 126
… [326 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des renvois de section et des liens internes fautifs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; for f in reports/rapport-pensee-attachement-v2.md reports/rapport-pensee-attachement-v3.md reports/rapport-pensee-segmentation-v4.md reports/rapport-pensee-couverture-v5.md reports/rapport-pensee-attachement-parfait.md reports/rapport- … [214 caractères tronqués]`

  ```
=== reports/rapport-pensee-attachement-v2.md
(aucun renvoi §)
=== reports/rapport-pensee-attachement-v3.md
(aucun renvoi §)
=== reports/rapport-pensee-segmentation-v4.md
(aucun renvoi §)
=== reports/rapport-pensee-couverture-v5.md
(aucun renvoi §)
=== reports/rapport-pensee-attachement-parfait.md
(aucun renvoi §)
=== reports/rapport-pensee-couverture-v7.md
(aucun renvoi §)
=== reports/rapport-gold-split.md
(aucun renvoi §)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; for f in reports/rapport-pensee-attachement-v2.md reports/rapport-pensee-attachement-v3.md reports/rapport-pensee-segmentation-v4.md reports/rapport-pensee-couverture-v5.md reports/rapport-pensee-attachement-parfait.md reports/rapport- … [359 caractères tronqués]`

  ```
=== reports/rapport-pensee-attachement-v2.md
=== reports/rapport-pensee-attachement-v3.md
=== reports/rapport-pensee-segmentation-v4.md
=== reports/rapport-pensee-couverture-v5.md
=== reports/rapport-pensee-attachement-parfait.md
=== reports/rapport-pensee-couverture-v7.md
=== reports/rapport-gold-split.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; for f in reports/pensee-attachement-v2.json reports/pensee-attachement-v3.json reports/pensee-segmentation-v4.json reports/pensee-couverture-v5.json reports/pensee-attachement-parfait.json reports/pensee-couverture-v7.json reports/pens … [237 caractères tronqués]`

  ```
=== reports/pensee-attachement-v2.json
69:  "decision": "rejete"
71: "echecs": {
82: "limites": [
=== reports/pensee-attachement-v3.json
38: "regles_rejetees": {
42: "controles_negatifs": {
47: "echecs_restants": [
59: "limites": [
=== reports/pensee-segmentation-v4.json
15:  "echecs_cible": 4
34:  "echecs_cible": [
51: "limites": [
=== reports/pensee-couverture-v5.json
16:  "echecs_cible": 3
36:  "echecs_cible": 1,
61: "limites": [
=== reports/pensee-attachement-parfait.json
42: "limites": [
=== reports/pensee-couverture-v7.json
42: "limites": [
=== reports/pensee-gold-split.json
28: "limites": [
  ```

### 🤖 Assistant

⏵ Lecture du format du JSON de cohérence antérieur

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; python3 - <<'PY'\nimport json\np='reports/pensee-coherence-fiches.json'\nd=json.load(open(p))\nprint(type(d), list(d)[:20] if isinstance(d,dict) else len(d))\nif isinstance(d,dict):\n    for k,v in d.items():\n        print(k, type(v). … [166 caractères tronqués]`

  ```
<class 'dict'> ['date_verification', 'branche', 'ligne', 'objet', 'note_portes', 'perimetre', 'methode', 'etat_verifie_pre_v2', 'v2_concurrente', 'synthese', 'fiches', 'controles', 'divergences', 'chiffres_historiques', 'note_chiffres_historiques', 'dettes_portes', 'concurrence', 'ambiguites_non_comptees', 'limites', 'fichiers']
date_verification str 2026-11-05T13:54:11-05:00
branche str s/v7
ligne str B13
objet str Cohérence des fiches B13 datées du 2026-11-05 avec leurs JSON et les portes
note_portes str Les champs porte_actuelle/portes_actuelles sont ceux du 2026-11-05T13:54 (pré-v2). La v2 committée `9d5337ce` a changé T
perimetre dict ['fiches', 'json', 'date_fiches', 'commits', 'portes_ciblees', 'portes_fiches', 'hors_perimetre']
methode dict ['lecture', 'valeur_porte', 'historique', 'execution', 'aucune_modification']
etat_verifie_pre_v2 dict ['date', 'note', 'portes', 'cibles', 'labels', 'top1', 'topk', 'exact']
v2_concurrente dict ['date', 'statut', 'portes', 'fichiers_modifies', 'fichiers_ajoutes', 'mesure', 'gates_changes', 'gates_ajoutees']
synthese dict ['fiches_verifiees', 'fiches_coherentes', 'fiches_avec_divergence', 'fiches_historiques', 'fiches_actuelles', 'palier
… [621 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de quelques chiffres textuels isolés (v3, v5, v7)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 - <<'PY'\nimport json\nd=json.load(open('tools/tests/linguistique/gold.json'))\nr=json.load(open('tools/tests/linguistique/gold_reel.json'))\ns=json.load(open('tools/tests/linguistique/gol … [710 caractères tronqués]`

  ```
GP 105 multi 43 ratio 0.4095
segments avec cible 239 {'GP': 96, 'SUB': 69, 'REL': 74}
Counter({'fr': 402, 'en': 210})
phrases 612
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; python3 - <<'PY'\nimport json, collections\ng=json.load(open('tools/tests/linguistique/gold_gele.json'))['phrases']\nprint(len(g), collections.Counter(p.get('source') for p in g), collections.Counter(p.get('langue') for p in g))\nprint … [147 caractères tronqués]`

  ```
602 Counter({'reel': 422, 'synthetique': 160, 'hand': 20}) Counter({'fr': 394, 'en': 208})
segments 239
  ```

### 🤖 Assistant

⏵ Collecte des métadonnées de commits et vérification de l'état du dépôt

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; for c in 9d5337ce dcf7bc91 e1903e2d 392f03aa b975011b 0ec6c27d 85e4082b 69bd865e; do git show -s --format=\"$c %ci %s\" $c; done", "description": "Get commit dates and subjects"}`

  ```
9d5337ce 2026-11-05 14:14:38 -0500 B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180
dcf7bc91 2026-11-05 15:18:56 -0500 B13 — L'ATTACHEMENT V3 : EXACT 0,9448 → 0,9724, NOMS 29/29 = 1,0 ; R2/R3/R4 DE A9 ; 181/181
e1903e2d 2026-11-05 16:16:07 -0500 B13 — L'ANGLAIS EST LE TROU (60/94 SPANS, S NE SEGMENTE PAS L'ANGLAIS) ; TABLEAU V3 RÉPARÉ ; 182/182
392f03aa 2026-11-05 17:50:01 -0500 B13 — S NE SEGMENTE QUE LE FRANÇAIS : F1 0,4194 → 0,4539, TÊTE 0,6432 ; EXACT 157/160, FR 0,9915 / EN 0,9524 ; 183/183
b975011b 2026-11-05 18:43:42 -0500 B13 — LES CANDIDATS DU PRÉCÉDENT : EXACT 186/187 (0,9947), ANGLAIS 60/60, DEV 126/126 ; 183/183
0ec6c27d 2026-11-05 19:03:53 -0500 B13 — L'ATTACHEMENT PARFAIT SUR LES SPANS PRÉDITS : 187/187 (1,0000), FR 1,0, EN 1,0, DEV 126/126, TEST 61/61 ; RENDEMENT 0,7824 ; 183/183
85e4082b 2026-11-05 17:53:37 -0500 B13 — LE GOLD DEV/TEST : TEST 0,9814, DEV 0,9811, LES GAINS GÉNÉRALISENT ; RÈGLE « RÉGLER SUR DEV, ACCEPTER SI TEST NE BAISSE PAS »
69bd865e 2026-11-05 19:22:37 -0500 B13 — LA COUVERTURE À 0,8201 : POS CONTEXTUEL 0,7603, F1 0,5595, EXACT 195/196 (0,9949), 43 SPANS 
… [9 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"=== status before write ===\"; git status --porcelain | grep -v '^ M journal' | head -30; echo \"=== worktrees ===\"; git worktree list", "description": "Check repo status and worktrees before writing"}`

  ```
=== status before write ===
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
D  journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/digest.md
D  journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/rapport.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rapport.md
D  journal/sessions/24001907-4f19-4ea5-87f6-98334496719f/digest.md
D  journal/sessions/24001907-4f19-4ea5-87f6-98334496719f/rapport.md
D  journal/sessions/24529ced-6556-4491-9633-9401c2dffb0c/digest.md
D  journal/sessions/24529ced-6556-4491-9633-9401c2dffb0c/rapport.md
D  journal/sessions/2cc1ad4a-373e-4362-a341-3c4a630c2e0c/digest.md
D  journal/sessions/2cc1ad4a-373e-4362-a341-3c4a630c2e0c/rapport.md
D  journal/sessions/3144cf
… [968 caractères tronqués]
  ```

### 🤖 Assistant

⏵ HEAD a bougé ; vérification que les sept fiches sont inchangées depuis 69bd865e

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"=== HEAD ===\"; git rev-parse --short HEAD; echo \"=== commits after 69bd865e ===\"; git log --oneline 69bd865e..HEAD | head -20; echo \"=== diff for 7 fiches/json ===\"; git diff --stat 69bd865e..HEAD -- reports/rapport-pensee- … [577 caractères tronqués]`

  ```
=== HEAD ===
e4cd4408
=== commits after 69bd865e ===
e4cd4408 DOCS — LE TABLEAU DES PORTES T163-T180 PASSE AUX VALEURS V7 (43 SPANS, EXACT 195/196, FR 1,0 / EN 0,9836)
4ccf06e1 JOURNAL — LA SOIRÉE DU DÉCOUPAGE : F1 0,2862 → 0,5595, COUVERTURE 196/239, ATTACHEMENT 195/196
=== diff for 7 fiches/json ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; git status --porcelain -- reports/rapport-pensee-attachement-v2.md reports/pensee-attachement-v2.json reports/rapport-pensee-attachement-v3.md reports/pensee-attachement-v3.json reports/rapport-pensee-segmentation-v4.md reports/pensee- … [411 caractères tronqués]`

  ```
(fin)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; grep -n -E \"22 \\(11/11\\)|11/11|avant.*22|échecs.*22\" reports/rapport-audit-v2.md | head -20; echo \"=== audit v2 §? ===\"; grep -n -E \"46|45|63/60|82/63|\\+48|split\" reports/rapport-audit-v2.md | head -30", "description": "Check  … [48 caractères tronqués]`

  ```
50:  d'échecs ; l'audit A1 en compte 22).
73:| verbe (POS gold) | 111/116 (0,9569) | **111/116 (0,9569)** | 0 |
217:| T163 | « 94 de span, 33 de cible » | 94 / **3** ; « 33 avant les correctifs » est faux (33 = exacts à `d400e188` ; A1 compte 22 échecs) |
270:  `RACINE` corrigé, les 126/134/123/88 et 11/11 reproduisent exactement.
=== audit v2 §? ===
1:# Audit B13 — l'attachement v2 : 43 valeurs rejouées, 2 arrondis, 1 erreur de prose (46 → 45), 8 docstrings de portes périmées
17:> une intégration v3 (`dcf7bc91`, 15:18) a atterri** : elle change les valeurs (exact 141/145,
25:- **Toutes les mesures revendiquées reproduisent** : 145 labels, top1 140, top-k 142, exact
27:  / 0,5732 ; split 116/111 (0,9569) et 29/26 (0,8966) ; 8 échecs (3 hors candidats, 5 mal
32:  **142/145**, règle **137/145**, gain **+5**, McNemar **7/2**, `p = 0,1797`, bootstrap
34:- **Une erreur de prose** : « **46** des 57 échecs étaient des candidats non réduits à leur
35:  tête » doit se lire « **45** ». Le 46 est l'écart `134 − 88` (sous-chaîne vs strict) ; le
36:  nombre de têtes candidates égales à la cible est **45** (A2 le dit, le comptage
37:  indépendant le confirme). Le gain « +45 » est, lui, correct.

… [1922 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction du rapport de cohérence et de son JSON

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-fiches-v7.md", "content": "# Cohérence des fiches B13 du 2026-11-05 — v2 → v7\n\n> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ❌\n> **7 fiches auditées** (1 … [26635 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-fiches-v7.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Écriture du registre JSON structuré

- **bash** `{"command": "date -Is; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; git rev-parse --short HEAD", "description": "Get timestamp and HEAD"}`

  ```
2026-11-05T20:10:36-05:00
e4cd4408
  ```

- **write** `{"content": "{\n \"date_verification\": \"2026-11-05T20:10:36-05:00\",\n \"branche\": \"s/v7\",\n \"ligne\": \"B13\",\n \"objet\": \"Cohérence des fiches B13 de la journée v2 → v7 avec leurs JSON et l'état 69bd865e\",\n \"commit_audite\": \"69bd865e\",\n \"head_au_moment_de_l_ecriture\": \"e4cd4408\ … [32578 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-coherence-fiches-v7.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Validation du JSON, des compteurs et de l'intégrité du dépôt

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; python3 - <<'PY'\nimport json\np='reports/pensee-coherence-fiches-v7.json'\nd=json.load(open(p, encoding='utf-8'))\nprint('JSON OK')\nprint('fiches', len(d['fiches']))\nprint('divergences', len(d['divergences']))\nfrom collections impo … [492 caractères tronqués]`

  ```
JSON OK
fiches 7
divergences 23
gravites Counter({'majeure': 17, 'critique': 4, 'mineure': 2})
synthese {'fiches_verifiees': 7, 'fiches_courantes': 1, 'fiches_historiques': 6, 'fiches_sans_divergence_numerique': 1, 'fiches_avec_divergence_numerique': 6, 'divergences_numeriques': 23, 'divergences_critiques': 4, 'divergences_majeures': 17, 'divergences_mineures': 2, 'fiches_avec_lacune_json_texte': 7, 'fiches_sans_controle_negatif': 5, 'fiches_historiques_sans_mention': 6, 'lignes_readme_a_corriger': 2, 'renvois_section_faux': 0, 'liens_casses': 0, 'tableaux_somme_fausse': 1, 'verdict_global': "❌ 0 fiche entièrement conforme (chiffres + JSON + mention d'historique + contrôle négatif) ; 1 fiche sans écart numérique (v3) ; 4 écarts critiques (v4, v5, v7)."}
ids ['V2-1', 'V2-2', 'V2-3', 'V4-1', 'V4-2', 'V4-3', 'V4-4', 'V4-5', 'V4-6', 'V4-7', 'V5-1', 'V5-2', 'V5-3', 'V5-4', 'V5-5', 'V5-6', 'V5-7', 'V5-8', 'V6-1', 'V7-1', 'V7-2', 'V7-3', 'GS-1']
=== markdown headings ===
1:# Cohérence des fiches B13 du 2026-11-05 — v2 → v7
22:## 1. Synthèse
51:## 2. Les sept fiches
66:## 3. Mesures reproduites
68:### 3.1 Attachement, couverture, spans
85:### 3.2 F1, tête, POS : la base de mesure n'est pas
… [1044 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"=== git status for our files ===\"; git status --porcelain -- reports/rapport-coherence-fiches-v7.md reports/pensee-coherence-fiches-v7.json; echo \"=== existing files unchanged? ===\"; git status --porcelain -- reports/rapport- … [877 caractères tronqués]`

  ```
=== git status for our files ===
?? reports/pensee-coherence-fiches-v7.json
?? reports/rapport-coherence-fiches-v7.md
=== existing files unchanged? ===
 M reports/rapport-gold-split.md
 M reports/rapport-pensee-attachement-parfait.md
 M reports/rapport-pensee-attachement-v2.md
 M reports/rapport-pensee-attachement-v3.md
 M reports/rapport-pensee-couverture-v5.md
 M reports/rapport-pensee-couverture-v7.md
 M reports/rapport-pensee-segmentation-v4.md
(fin)
=== untracked pycache? ===
=== worktree cleanup ===
/home/stephane/Data13TB/stephane/GitHub/Qtrinet e4cd4408 [s/v7]
  ```

### 🤖 Assistant

⏵ Les fiches ont changé dans l'arbre de travail ; inspection des diffs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; git diff --stat -- reports/rapport-pensee-attachement-v2.md reports/rapport-pensee-attachement-v3.md reports/rapport-pensee-segmentation-v4.md reports/rapport-pensee-couverture-v5.md reports/rapport-pensee-attachement-parfait.md report … [216 caractères tronqués]`

  ```
reports/rapport-gold-split.md                 |  4 +++-
 reports/rapport-pensee-attachement-parfait.md |  2 ++
 reports/rapport-pensee-attachement-v2.md      |  2 ++
 reports/rapport-pensee-attachement-v3.md      |  2 ++
 reports/rapport-pensee-couverture-v5.md       |  2 ++
 reports/rapport-pensee-couverture-v7.md       | 20 ++++++++++++++++----
 reports/rapport-pensee-segmentation-v4.md     |  2 ++
 7 files changed, 29 insertions(+), 5 deletions(-)
=== v4 diff ===
diff --git a/reports/rapport-pensee-segmentation-v4.md b/reports/rapport-pensee-segmentation-v4.md
index e5f306b8..d6899a0a 100644
--- a/reports/rapport-pensee-segmentation-v4.md
+++ b/reports/rapport-pensee-segmentation-v4.md
@@ -1,5 +1,7 @@
 # B13 — la segmentation d'abord : F1 0,2862 → 0,4194, exact 158/160 (0,9875), couverture 160/239
 
+> **Instantané historique** : état au commit `392f03aa` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).
+
 > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
 > **183/183 portes** : le diagnostic de A12/A14 était juste — le trou n'était pas l'attachement
… [104 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; git diff -- reports/rapport-pensee-couverture-v7.md reports/rapport-gold-split.md | head -120", "description": "Inspect v7 and gold-split concurrent edits"}`

  ```
diff --git a/reports/rapport-gold-split.md b/reports/rapport-gold-split.md
index 76e9ba91..d16c5655 100644
--- a/reports/rapport-gold-split.md
+++ b/reports/rapport-gold-split.md
@@ -1,5 +1,7 @@
 # B13 — le gold coupé en dev/test : les gains généralisent (test 0,9814, dev 0,9811)
 
+> **Instantané historique** : état au commit `85e4082b` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).
+
 > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
 > Le gold 612 est coupé en **dev** (422 phrases, 163 cibles, 106 labels) et **test** (190, 76, 54)
 > par un **hash stable de l'identifiant** (`crc32(id) % 3 == 0` → test), stratifié par source et
@@ -39,7 +41,7 @@
 
 ## 3. Ce que ce banc ne dit pas
 
-- **Les 79 spans perdus** : la couverture reste 160/239, identique sur les deux moitiés.
+- **Les 79 spans perdus** : la couverture est **106/163 = 0,6503 en dev** et **54/76 = 0,7105 en test** (total 160/239 = 0,6695) — pas identique.
 - **Le surajustement fin** : un split ne détecte pas un ajustement qui profite aux deux moitiés
   (les règles ont été dessinées sur l'e
… [2568 caractères tronqués]
  ```

