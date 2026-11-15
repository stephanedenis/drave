# Session DSH — relecture

- identifiant : `session-e3fa8f1c-e304-4a0b-922a-79e5a1a580e5`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 12:27:52
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche X1 (J4 après-midi, la part du pilote) : mesure la page `/` de S **en lecture seule** — lis les données du sous-module (`tools/structures/`) et la fiche `reports/rapport-coordination-s-v2.md` ; compare **`/` (le banc ancien : 369 candidats, 0 verdict)** et **la v7 (359 candidats, 99 verdicts)** : la couverture, les verdicts, les référents (14 occurrences / 12 formes), les 106 conservés / 41 en quarantaine. Écris `reports/rapport-page-s-mesure.md` + JSON avec le **contrôle négatif** (les deux bancs doivent différer). **Ne modifie rien dans `tools/structures/`.**

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

I'll start by exploring the repository structure and the relevant files.

- **bash** `{"command": "pwd && ls -la && echo \"---\" && ls tools/structures/ 2>/dev/null | head -50", "description": "List repo root and structures submodule"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138 15 nov 06:29 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   198 15 nov 12:27 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 01:33 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 78238 15 nov 12:17 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [1196 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/ 2>/dev/null | head -60; echo \"---\"; ls reports/rapport-coordination-s-v2.md 2>/dev/null && wc -l reports/rapport-coordination-s-v2.md", "description": "List reports and check target report"}`

  ```
total 29672
drwxr-xr-x. 1 stephane stephane   78238 15 nov 12:17 .
drwxr-xr-x. 1 stephane stephane     686  6 nov 09:52 ..
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
… [3182 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s-v2.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s-v2.md</path>
<type>file</type>
<content>
1: # S — la page `/` ne sert pas la v7, le service ne tourne pas, et les 11 verdicts sont committés
2: 
3: > **Ligne de roadmap** : S · **Date** : 2026-11-15 · **HEAD parent mesuré** : `292c70b5`
4: > · **Sous-module `tools/structures`** : `389b99f` · **Verdict** : les **11 verdicts**
5: > a004–a009 sont **committés** (sous-module `389b99f`, pointeur parent `31ce36fd`) :
6: > **19/19 candidats, 11 acceptés, 8 exclus**. La page **`/`** **ne sert pas la v7** : elle
7: > charge **369 candidats stockés** (0 avec `profondeur`) et son rendu lit `niveau` ; la mesure
8: > v7 sur les mêmes **207 phrases** donne **359 candidats**, dont **99 à profondeur ≥ 3**. Le
9: > service S **n'est pas en écoute** : le port **8765** est tenu par un autre projet
10: > (`financemeteo`, pid 2725542), et un lancement de mesure sur **9000** répond 200. Le
11: > pare-feu **firewalld** est actif mais **non interrogeable sans root** ; le serveur écoute
12: > **127.0.0.1** par défaut. **Aucun fichier suivi de `tools/structures/` n'est modifié.**
13: 
14: **En trois lignes.** (1) Les 11 ver
… [24286 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/structures/donnees/ | head -40; echo \"---README---\"; wc -l tools/structures/README.md", "description": "List data dir and README size"}`

  ```
total 636
drwxr-xr-x. 1 stephane stephane    414  3 nov 16:49 .
drwxr-xr-x. 1 stephane stephane    438  3 nov 16:22 ..
-rw-------. 1 stephane stephane  16806  4 nov 11:42 gold-analyseur.json
-rw-r--r--. 1 stephane stephane    659  3 nov 12:36 llm.jsonl
-rw-r--r--. 1 stephane stephane  21646  4 nov 11:42 mesure-analyseur.json
-rw-r--r--. 1 stephane stephane    886  3 nov 16:23 mesure-arbre.json
-rw-r--r--. 1 stephane stephane   5099  3 nov 18:36 mesure-corpus.json
-rw-r--r--. 1 stephane stephane   7217  4 nov 09:44 paragraphes.json
-rw-r--r--. 1 stephane stephane   6047  4 nov 15:10 paragraphes-validations.jsonl
-rw-r--r--. 1 stephane stephane    366  2 nov 20:35 phrases-corpus-manifest.json
-rw-r--r--. 1 stephane stephane 527440  2 nov 20:35 phrases_generees.json
-rw-r--r--. 1 stephane stephane  12115  2 nov 02:10 phrases.json
-rw-r--r--. 1 stephane stephane  25828  3 nov 16:46 validations.jsonl
---README---
352 tools/structures/README.md
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/README.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/README.md</path>
<type>file</type>
<content>
1: # Structures — le banc d'interprétations candidates
2: 
3: > **Ce que c'est.** Un outil **pour humain** : il affiche, pour une phrase, plusieurs **structures
4: > d'interprétation candidates** (attachements, rôles, portées), permet de les **valider**, de
5: > demander l'avis d'un **grand modèle** (DeepSeek), et d'**exporter une banque** de structures
6: > validées — un corpus d'entraînement pour le projet Drave.
7: 
8: > **Ce que ce n'est pas.** Pas un analyseur syntaxique complet : les candidats sont **générés par
9: > une heuristique** (`generateur.py`) ou fournis par le fichier de données ; l'outil les fait
10: > valider, il ne prétend pas les avoir compris. Depuis la v2, l'heuristique **nomme le rôle** par
11: > le contexte, **coupe les subordonnées** et traite le passif et la copule — et un **gold** mesure
12: > ce qu'elle sait faire, échecs compris (voir « La mesure de l'analyseur »).
13: 
14: ## Lancer
15: 
16: ```bash
17: python3 serveur.py                 # http://127.0.0.1:8765
18: python3 serveur.py --port 9000 --hote 0.0.0.0   # sur le réseau local
19: 
… [21689 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git -C tools/structures log --oneline -3 && git -C tools/structures status --porcelain && echo \"--- HEAD parent ---\" && git log --oneline -3 && echo \"--- branch ---\" && git branch --show-current", "description": "Check submodule  … [25 caractères tronqués]`

  ```
389b99f S — LES 11 VERDICTS HUMAINS DE /paragraphes (a004–a009) : 19/19 CANDIDATS JUGÉS, 11 ACCEPTÉS, 8 EXCLUS ; DÉCISION DU 14/11 (3B), EXCEPTION AUTORISÉE
523d8c1 S — LE FAIT DIVERS EST TRANCHÉ : 61/61 TYPES, 144/144 RÔLES ; LA TÊTE DU GN ARRÊTE LE VERBE
4012729 S — LA BANQUE DE PARAGRAPHES PASSE À NEUF : SIX PAIRES D'ALICE, SOURCES ANGLAISES ET RÉFÉRENTS
--- HEAD parent ---
6f862993 SEMAINE 2 — W6 : LA CLÔTURE (5 VAGUES, 3 POSITIVES, 1 BLOQUÉE, 1 MIXTE) ; 85 PORTES LUES (81/4), CIBLAGE 9/9 ; TAG ANNOTÉ semaine-2-2026-11-20 SUR 73edb3dd
73edb3dd SEMAINE 2 — W5 : LA RESTITUTION v3 SÉPARE LES CINQ RÔLES (GOLD S 144/144, 18/18, PERMUTATION 0/18) ; LE GOLD v2 NE GAGNE QU'UN CADRE (20/46, F1 0,5406, LIEU 0,60) ; --roles-v3 OPT-IN
93e046f7 SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE
--- branch ---
s/v7
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"14 occurrences\\|12 formes\\|106\\|quarantaine\" reports/*.md | head -20; echo \"---\"; grep -rn \"14 occurrences\\|12 formes\" reports/ docs/ journal/ 2>/dev/null | head -30", "description": "Search referent audit terms  … [12 caractères tronqués]`

  ```
reports/inventaire-donnees-entrainement.md
reports/rapport-atomes-niveaux.md
reports/rapport-atomes-prediction.md
reports/rapport-bilan-chantier.md
reports/rapport-cache-chunker.md
reports/rapport-cerveau-corrections.md
reports/rapport-cerveau-modules.md
reports/rapport-coherence-fiches-v7.md
reports/rapport-coherence-fiches-v8.md
reports/rapport-coordination-s-v2.md
reports/rapport-dev-test-v7.md
reports/rapport-etat-n2.md
reports/rapport-etat-s.md
reports/rapport-fiabilite-produit.md
reports/rapport-file-taches.md
reports/rapport-gold-452.md
reports/rapport-gold-anglais.md
reports/rapport-gold-reel-50.md
reports/rapport-gold-split.md
reports/rapport-n2-multilingue-34m.md
---
reports/rapport-gold-anglais.md:217:| faux négatifs | 15 (12 formes) | 15 |
reports/rapport-gold-anglais.md:227:`cries`, `call`, `stayed`, `goes`, `continue` (12 formes, 15 occurrences) ; le faux positif est
reports/rapport-pensee-v11.md:39:- **18 spans restants** : **17 inatteignables** (12 formes synthétiques, 4 GP du gold sans
reports/rapport-pensee-v12.md:12:> le lexique (12 formes synthétiques, 4 GP du gold sans préposition, une tokenisation `qu'il`).
reports/rapport-pensee-v12.md:42:- **Les 17 spans res
… [5233 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,240p' tools/structures/mesure_arbre.py", "description": "Read mesure_arbre.py"}`

  ```
#!/usr/bin/env python3
"""mesure_arbre.py — la profondeur actuelle de l'arbre et les référents non résolus de la banque.

Le retour humain du 03/11 : « il manque trop souvent de profondeur » et « les référents ne
semblent pas résolus avant que je tranche ». Ce script mesure les deux sur les 207 phrases du
banc : la distribution de `niveau` (l'indentation) et des profondeurs maximales des candidats, et
les pronoms/possessifs qui n'ont aucun antécédent proposé. C'est le dispositif du négatif, pas un
jugement : il dit ce que l'outil ne montrait pas.

    python3 mesure_arbre.py
"""
from __future__ import annotations

import json
import pathlib
from collections import Counter

import generateur

RACINE = pathlib.Path(__file__).resolve().parent
DONNEES = RACINE / "donnees"
SORTIE = DONNEES / "mesure-arbre.json"
POSSESSIFS = set("mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs".split())


def phrases() -> list[dict]:
    sortie = json.loads((DONNEES / "phrases.json").read_text(encoding="utf-8"))["phrases"]
    g = DONNEES / "phrases_generees.json"
    if g.exists():
        sortie += json.loads(g.read_text(encoding="utf-8"))["phrases"]
    return sortie


def mesurer() ->
… [1980 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '120,200p' reports/rapport-etat-s.md && echo \"=====300-420=====\" && sed -n '300,420p' reports/rapport-etat-s.md", "description": "Read referent audit sections"}`

  ```
|---|---:|---:|---:|---:|---:|
| a001 | 2 | 2 | 2 | 0 | 4/5 |
| a002 | 3 | 3 | 1 | 2 | 1/3 |
| a003 | 3 | 3 | 1 | 2 | 4/4 |
| a004 | 2 | 2 | 1 | 1 | 1/1 |
| a005 | 2 | 2 | 1 | 1 | 2/3 |
| a006 | 1 | 1 | 1 | 0 | 3/4 |
| a007 | 2 | 2 | 1 | 1 | 0/0 |
| a008 | 1 | 1 | 1 (`compatible`) | 0 | 0/5 |
| a009 | 3 | 3 | 2 | 1 | 1/3 |
| **total** | **19** | **19** | **11** | **8** | **16/28** |

**Le « 8 restants » est faux, et il mélange verdicts et paragraphes.** La page a 9 paragraphes,
pas 17. Après a001–a003, il restait **6** paragraphes (a004–a009), pas 8. Le chiffre **8** est
celui des **verdicts committés** sur a001–a003 (commit `7ccc60f` : 8 verdicts), pas celui des
paragraphes restants. Les **11 verdicts** a004–a009 ont été ajoutés le **2026-11-04** et sont
**toujours non committés** : un clone à `523d8c1` voit 8 verdicts et 6 paragraphes sans verdict ;
le working tree local voit 19/19. C'est pourquoi `docs/pilotage/en-cours.md:59` et
`docs/pilotage/roadmap.md:34` disent encore « a001–a003 faits » alors que
`docs/pilotage/roadmap.md:356` dit déjà « a001–a009 faits ». **Les données arbitrent : 9/9 et
19/19 dans le working tree ; 8 verdicts dans git.**

**Les référents ne sont pas vali
… [11411 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def \\|^RACINE\\|^DONNEES\\|^LEXIQUE\" tools/structures/generateur.py | head -60; echo \"---\"; wc -l tools/structures/generateur.py tools/structures/serveur.py tools/structures/exporter_corpus.py", "description": "List gen … [18 caractères tronqués]`

  ```
134:def _norm(mot: str) -> str:
142:    def __init__(self, texte, debut, fin, espace):
175:def _tokens(texte: str) -> list[Token]:
179:def _est_que(tok: Token) -> bool:
184:def _si_intensif(utiles: list[Token], i: int) -> bool:
192:def _marqueur(utiles: list[Token], i: int) -> str | None:
223:def _fin_clause(utiles: list[Token], j: int) -> int:
235:def _dernier_mot(texte: str) -> str:
241:def _infinitif(tok: Token) -> bool:
246:def _role_gp(prep: str, segs: list["Segment"], utiles: list[Token], i: int) -> str:
253:    def _proche(types: tuple[str, ...]) -> "Segment | None":
297:    def __init__(self, debut, fin, texte, typ, role, niveau=0):
306:    def dict(self):
312:def _consomme(toks, i, classes):
319:def construire_arbre(segs: list["Segment"]) -> None:
346:def _segmente(texte: str, toks: list[Token]) -> list[Segment]:
486:    def _tete_gp(g):
505:def _role_attache(role: str, genre: str) -> str | None:
516:def analyser(texte: str, max_candidats: int = 4) -> list[dict]:
575:def referents(texte: str, contexte: str = "") -> list[dict]:
585:    def noms_propres(texte_partiel: str) -> list[str]:
590:    def avant(pos: int) -> list[str]:
621:def structure(texte: str, roles: bool = Tru
… [146 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la work/ | head -50; echo \"--- banque-v7 ---\"; ls -la work/banque-v7/ 2>/dev/null; echo \"--- referents ---\"; ls -la work/referents/ 2>/dev/null; echo \"--- page-s ---\"; ls -la work/page-s* 2>/dev/null", "description": "Inspe … [28 caractères tronqués]`

  ```
total 240
drwxr-xr-x. 1 stephane stephane  2300 15 nov 12:20 .
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 ..
-rw-r--r--. 1 stephane stephane  1040 15 nov 03:23 atomes_cohortes.py
-rwxr-xr-x. 1 stephane stephane  2133  2 nov 16:46 attente_portes.sh
drwxr-xr-x. 1 stephane stephane   240 15 nov 08:56 chantier
drwxr-xr-x. 1 stephane stephane   168  7 nov 15:06 corpus-commun
-rw-r--r--. 1 stephane stephane  6879  1 nov 12:49 corpus-wiki-langues.log
-rw-r--r--. 1 stephane stephane  1004  1 nov 11:14 corpus-wiki.log
-rw-r--r--. 1 stephane stephane  3985  1 nov 12:49 corpus-wiki-reste.log
drwxr-xr-x. 1 stephane stephane     8  1 nov 18:44 dr
-rw-r--r--. 1 stephane stephane   479  2 nov 20:32 entete-references.txt
-rw-------. 1 stephane stephane  5759  2 nov 01:21 finaliser_ocr.py
-rw-r--r--. 1 stephane stephane  9625  3 nov 05:55 hub-nuit.md
drwxr-xr-x. 1 stephane stephane   200  7 nov 18:06 j32
drwxr-xr-x. 1 stephane stephane   312 14 nov 01:34 j71
-rw-r--r--. 1 stephane stephane  3604  3 nov 05:52 maj_references2.py
-rw-r--r--. 1 stephane stephane  2954  3 nov 13:17 maj_references3.py
-rw-r--r--. 1 stephane stephane  3735  2 nov 20:41 maj_references.py
-rw-r--r--. 1 stephane step
… [2003 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,110p' docs/pilotage/semaine-2.md", "description": "Read semaine-2 pilotage doc"}`

  ```
# La semaine 2 — cinq jours, deux vagues, quatre chantiers et une décision

> **Ce que ce document est.** Le plan du **16 au 22 novembre 2026** : ce qui se fait, dans quel
> ordre, avec quelles dépendances, quels contrôles et quels livrables. Il **succède** à
> [`semaine-autonome.md`](semaine-autonome.md), qui reste l'**archive** de la semaine 1 et n'est
> **pas modifié**. L'état courant est dans [`en-cours.md`](en-cours.md) ; les chiffres sont dans
> les fiches citées, jamais recopiés ici.
>
> **Sources.** Le [bilan de la semaine](../../reports/rapport-bilan-semaine.md) et les fiches des
> tâches C/B/D/E : [C1](../../reports/rapport-coordination-n2-v2.md), [C2](../../reports/rapport-coordination-s-v2.md),
> [C3](../../reports/rapport-gold-reel-50.md), [B1](../../reports/rapport-protocole-date.md),
> [B2](../../reports/rapport-atomes-prediction.md), [B3](../../reports/rapport-cic-v2.md),
> [D1](../../reports/rapport-exemples-tagger.md), [D2](../../reports/rapport-restitution-v2.md),
> [D3](../../reports/rapport-faq.md), [E1](../../reports/rapport-faq-sommaire.md),
> [E2](../../reports/rapport-tagger-erreurs.md). Le plan ne promet aucun chiffre : il nomme la
> mesure, son **contrôle
… [11458 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, pathlib\nD=pathlib.Path('donnees')\nfor f in ['phrases.json','phrases_generees.json']:\n    d=json.loads((D/f).read_text(encoding='utf-8'))\n    ps=d['phrases' … [681 caractères tronqués]`

  ```
phrases.json clés: ['version', 'note', 'phrases'] phrases: 7 candidats: 14
  première phrase clés: ['id', 'texte', 'candidats', 'contexte_exemple', 'niveau_exemple']
  premier candidat clés: ['id', 'nom', 'lecture', 'segments', 'attachement']
  validations embarquées: 0
  profondeur candidates: 0
  profondeur segments: 0
phrases_generees.json clés: ['version', 'note', 'source', 'phrases'] phrases: 200 candidats: 355
  première phrase clés: ['id', 'texte', 'source', 'candidats']
  premier candidat clés: ['id', 'nom', 'lecture', 'attachement', 'segments']
  validations embarquées: 0
  profondeur candidates: 0
  profondeur segments: 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, pathlib, collections\nD=pathlib.Path('donnees')\nfor f in ['validations.jsonl','paragraphes-validations.jsonl']:\n    ls=[json.loads(l) for l in (D/f).read_tex … [372 caractères tronqués]`

  ```
validations.jsonl 150 clés: ['auteur', 'candidat_id', 'contexte', 'horodatage', 'niveau', 'note', 'phrase_id', 'statut']
  statuts: Counter({'resolu': 74, 'exclu': 64, 'compatible': 11, 'double_sens': 1})
  auteurs: Counter({'humain': 150})
  première: {'phrase_id': 'p001', 'candidat_id': 'p001-c2', 'statut': 'exclu', 'note': '', 'contexte': 'La voisine est partie en vacances. Son chat, lui, est resté sur le toit : il y dort toute la journée, au soleil.', 'niveau': 2, 'auteur': 'humain', 'horodatage': '2026-11-03T10:31:17'}
paragraphes-validations.jsonl 19 clés: ['auteur', 'candidat_id', 'contexte', 'horodatage', 'niveau', 'note', 'phrase_id', 'referents', 'statut']
  statuts: Counter({'resolu': 10, 'exclu': 8, 'compatible': 1})
  auteurs: Counter({'humain': 19})
  première: {'phrase_id': 'a001', 'candidat_id': 'a001-c1', 'statut': 'resolu', 'referents': {'Elle': 'Alice', 'se': 'Alice', 'elle': 'Alice', 'lui': 'Alice', 'en': 'Alice'}, 'note': '', 'contexte': 'Allons, à quoi bon pleurer ainsi, se dit Alice vivement.', 'niveau': 2, 'auteur': 'humain', 'horodatage': '2026-11-03T16:49:32'}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, pathlib, collections\nD=pathlib.Path('donnees')\nfor f in ['phrases.json','phrases_generees.json']:\n    ps=json.loads((D/f).read_text(encoding='utf-8'))['phra … [278 caractères tronqués]`

  ```
phrases.json segment key sets: Counter({('debut', 'fin', 'niveau', 'role', 'texte', 'type'): 44})
  exemple seg: {'debut': 0, 'fin': 7, 'texte': 'Le chat', 'type': 'GN', 'role': 'agent', 'niveau': 0}
phrases_generees.json segment key sets: Counter({('debut', 'fin', 'niveau', 'role', 'texte', 'type'): 2370})
  exemple seg: {'debut': 0, 'fin': 47, 'texte': 'Au lecteur Cette version électronique reproduit', 'type': 'GP', 'role': 'destinataire', 'niveau': 1}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && sed -n '1,120p' serveur.py && echo \"...\" && grep -n \"def api_phrases\\|validations\\|phrases_generees\\|def main\\|--port\" serveur.py | head -40", "description": "Read server routes and defaults"}`

  ```
#!/usr/bin/env python3
"""serveur.py — le banc de structures : API + interface web, sans dépendance.

Le serveur expose les phrases et leurs interprétations candidates, enregistre les verdicts
humains (`donnees/validations.jsonl`), interroge un grand modèle (`donnees/llm.jsonl`) et exporte
la banque validée (`/api/export`).

    python3 serveur.py                 # http://127.0.0.1:8765
    #   /            le banc de phrases
    #   /paragraphes les paragraphes complets : arbre SVG, référents, verdict
    python3 serveur.py --port 9000 --hote 0.0.0.0
"""
from __future__ import annotations

import argparse
import json
import pathlib
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

import arbre_svg
import generateur
import llm

RACINE = pathlib.Path(__file__).resolve().parent
STATIQUE = RACINE / "static"
# Le niveau pragmatique : un sens n'est pas « vrai » hors contexte, il est **résolu** par lui,
# **compatible** avec lui, **exclu** par lui — ou **double**, quand l'ambiguïté est voulue.
STATUTS = {"resolu", "compatible", "exclu", "double_sens"}
# Les niveaux de contexte : il en faut parfois plus d'un
… [5909 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && sed -n '297,360p' generateur.py && sed -n '480,620p' generateur.py", "description": "Read Segment, analyser, referents"}`

  ```
def __init__(self, debut, fin, texte, typ, role, niveau=0):
        self.debut, self.fin, self.texte = debut, fin, texte
        self.type, self.role, self.niveau = typ, role, niveau
        self.cible_nom = None   # le GN le plus proche à gauche
        self.cible_gp = None    # la tête du GP le plus proche à gauche
        self.cible_verbe = None  # le GV le plus proche à gauche
        self.parent = None      # l'index du segment père dans la liste
        self.profondeur = 0     # la profondeur dans l'arbre (le GV racine = 0)

    def dict(self):
        return {"debut": self.debut, "fin": self.fin, "texte": self.texte,
                "type": self.type, "role": self.role, "niveau": self.niveau,
                "parent": self.parent, "profondeur": self.profondeur}


def _consomme(toks, i, classes):
    j = i
    while j < len(toks) and toks[j].cls in classes:
        j += 1
    return j


def construire_arbre(segs: list["Segment"]) -> None:
    """Le père et la profondeur : le GV principal est la racine, les GN ses enfants, et les
    GP/REL/SUB s'accrochent au plus proche segment à gauche (GN, GP ou GV). L'indentation
    (`niveau`) devient la profondeur réelle, pas un niveau 
… [7286 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/rapport-s-traductions.md && sed -n '1,220p' reports/rapport-s-traductions.md", "description": "Read translation/referent report"}`

  ```
reports/rapport-s-traductions.md
# S — La traduction contrôle le sens : 14/14 référents anaphoriques confirmés par l'anglais, le « les » → « it » retrouvé

> **Ligne de roadmap** : S · **Date** : 2026-11-03 · **Verdict** : les trois paragraphes français
> sont des traductions d'*Alice's Adventures in Wonderland* (1865) ; l'original anglais, qui dit
> explicitement *she / her / herself / it*, tranche les référents que le français laisse flotter.
> Les **14 formes anaphoriques** des trois paragraphes sont confirmées — les **2 que l'outil
> manquait** sont retrouvées (« les » → *it* → les conseils ; « l' » → *it* → la boîte) — et la
> traduction **corrige le contexte** de a003, où Alice n'était pas nommée. La page
> `/paragraphes` affiche désormais la source anglaise à côté du français.

## Le dispositif

Le corpus français (`data/corpus_fr_litterature.txt`) contient la traduction d'Alice ; la source
anglaise est l'original de Lewis Carroll, dans l'édition du Project Gutenberg (#11,
[`gutenberg.org/files/11/11-0.txt`](https://www.gutenberg.org/files/11/11-0.txt)). Les trois
paragraphes de `donnees/paragraphes.json` portent maintenant leur `source_en` (la phrase cible en
anglais) et le
… [5751 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json\nd=json.load(open('donnees/paragraphes.json'))\nprint(list(d.keys()))\nfor p in d['paragraphes']:\n    print(p['id'], '|', p.get('cible','')[:90])\n    print('  … [227 caractères tronqués]`

  ```
['version', 'note', 'source', 'paragraphes', 'note_en', 'source_en_url']
a001 | Elle avait pour habitude de se donner de très-bons conseils (bien qu'elle les suivît rarem
   source_en: She generally gave herself very good advice, (though she very seldom followed it), and sometimes she
   contexte: Allons, à quoi bon pleurer ainsi, se dit Alice vivement.
   antecedent: Alice | keys: ['antecedent', 'cible', 'contexte', 'contexte_en', 'id', 'source_en']
a002 | Elle aperçut alors une petite boîte en verre qui était sous la table, l'ouvrit et y trouva
   source_en: Soon her eye fell on a little glass box that was lying under the table: she opened it, and found in 
   contexte: Allons, à quoi bon pleurer ainsi, se dit Alice vivement.
   antecedent: Alice | keys: ['antecedent', 'cible', 'contexte', 'contexte_en', 'id', 'source_en']
a003 | Elle mangea donc un petit morceau du gâteau, et, portant sa main sur sa tête, elle se dit 
   source_en: She ate a little bit, and said anxiously to herself, "Which way? Which way?", holding her hand on th
   contexte: Allons, à quoi bon pleurer ainsi, se dit Alice vivement. Elle aperçut alors une 
   antecedent: Alice | keys: ['antecedent', 'cible', 'co
… [2377 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, hashlib\nD='donnees/'\n# old phrases\nphr=json.load(open(D+'phrases.json'))['phrases']+json.load(open(D+'phrases_generees.json'))['phrases']\nold= … [1676 caractères tronqués]`

  ```
phrases 207 cands 369
old niveau max {0: 10, 1: 277, 2: 82}
old profondeur cands 0
old cands with any niveau !=0 0
vals lines 150 unique pairs 147
phrases with verdict 74
full 74 partial 0 none 133
judged candidates 147 / 369
last statuts Counter({'resolu': 73, 'exclu': 63, 'compatible': 11})
all statuts Counter({'resolu': 74, 'exclu': 64, 'compatible': 11, 'double_sens': 1})
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys\nsys.path.insert(0,'.')\nimport mesure_arbre, generateur\nr=mesure_arbre.mesurer()\nprint(json.dumps({k:v for k,v in r.items() if k!='formes'} … [166 caractères tronqués]`

  ```
{
 "phrases": 207,
 "candidats": 359,
 "segments": 2308,
 "profondeur_max": {
  "0": 2,
  "1": 37,
  "2": 221,
  "3": 84,
  "4": 13,
  "5": 2
 },
 "niveaux": {
  "0": 359,
  "1": 1268,
  "2": 556,
  "3": 108,
  "4": 15,
  "5": 2
 },
 "phrases_avec_referent": 170,
 "referents": 371,
 "avec_candidat": 294,
 "sans_candidat": 77,
 "note": "profondeur = parent/enfant réel (GV racine) ; référents = pronoms/possessifs ; avec_candidat = au moins un antécédent proposé dans la phrase (sans contexte)."
}
nb formes uniques 29 top [('y', 109), ('en', 67), ('se', 44), ('me', 19), ('il', 18), ('son', 18), ('elle', 9), ('je', 9), ('vous', 9), ('lui', 8)]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, hashlib, re, sys\nsys.path.insert(0,'.')\nimport generateur\nD='donnees/'\nphr=json.load(open(D+'phrases.json'))['phrases']+json.load(open(D+'phra … [2602 caractères tronqués]`

  ```
pairs 147
v7 counts 359 phrases differing count 9
kept pairs 106 quar pairs 44
quar lines concerned (all revisions): 41
noindex [('p006', 'p006-c2', 2, 1), ('c023', 'c023-c3', 3, 2), ('c056', 'c056-c2', 2, 1), ('c056', 'c056-c3', 3, 1), ('c064', 'c064-c2', 2, 1)]
sameindex_changed count 39
sameindex_changed [('p001', 'p001-c2', 2), ('p001', 'p001-c1', 1), ('p002', 'p002-c1', 1), ('p002', 'p002-c2', 2), ('p002', 'p002-c2', 2), ('p003', 'p003-c1', 1), ('p003', 'p003-c2', 2), ('p004', 'p004-c1', 1), ('p004', 'p004-c2', 2), ('p005', 'p005-c2', 2), ('p005', 'p005-c1', 1), ('p006', 'p006-c1', 1), ('p007', 'p007-c1', 1), ('p007', 'p007-c2', 2), ('c002', 'c002-c1', 1), ('c002', 'c002-c2', 2), ('c004', 'c004-c2', 2), ('c004', 'c004-c1', 1), ('c009', 'c009-c1', 1), ('c009', 'c009-c2', 2), ('c009', 'c009-c3', 3), ('c011', 'c011-c1', 1), ('c011', 'c011-c2', 2), ('c013', 'c013-c1', 1), ('c013', 'c013-c2', 2), ('c013', 'c013-c3', 3), ('c020', 'c020-c1', 1), ('c020', 'c020-c2', 2), ('c020', 'c020-c3', 3), ('c023', 'c023-c1', 1), ('c023', 'c023-c2', 2), ('c043', 'c043-c2', 2), ('c043', 'c043-c1', 1), ('c056', 'c056-c1', 1), ('c064', 'c064-c1', 1), ('c065', 'c065-c1', 1), ('c065', 'c065-c2', 2), ('
… [400 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, re, sys\nsys.path.insert(0,'.')\nimport generateur\nD='donnees/'\nphr=json.load(open(D+'phrases.json'))['phrases']+json.load(open(D+'phrases_gener … [1130 caractères tronqués]`

  ```
Counter({'identique': 304, 'change': 55, 'orphelin': 10})
changed sample [('p001', 'p001-c1', 1, False), ('p001', 'p001-c2', 2, False), ('p002', 'p002-c1', 1, False), ('p002', 'p002-c2', 2, False), ('p003', 'p003-c1', 1, False)]
orphans [('p006', 'p006-c2', 2, 1), ('c023', 'c023-c3', 3, 2), ('c056', 'c056-c2', 2, 1), ('c056', 'c056-c3', 3, 1), ('c064', 'c064-c2', 2, 1), ('c084', 'c084-c2', 2, 1), ('c176', 'c176-c2', 2, 1), ('c185', 'c185-c2', 2, 1), ('c194', 'c194-c3', 3, 2), ('c198', 'c198-c3', 3, 2)]
old candidates whose sig exists at another index 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections\nD='donnees/'\nparas=json.load(open(D+'paragraphes.json'))['paragraphes']\nvals=[json.loads(l) for l in open(D+'paragraphes-validations.jsonl') if  … [445 caractères tronqués]`

  ```
a001 5 {'Elle': 'Alice', 'se': 'Alice', 'elle': 'Alice', 'lui': 'Alice', 'en': 'Alice'}
a002 3 {'Elle': 'Alice', 'en': 'Alice', 'y': 'Alice'}
a003 4 {'Elle': 'Alice', 'sa': 'Alice', 'elle': 'Alice', 'se': 'Alice'}
a004 1 {'sa': 'ALICE'}
a005 3 {'elle': 'Alice', 'son': 'Alice', 'en': 'coup'}
a006 4 {'cela': 'Comme', 'son': 'Alice', 'elle': 'Alice', 'y': 'table'}
a007 0 {}
a008 5 {'Je': 'le contenu', 'me': 'le contenu', 'on': 'Je me sens toute drôle', 'je': 'Je me sens toute drôle', 'en': 'Je me sens toute drôle'}
a009 3 {'se': 'Un moment', 'elle': 'Alice', 'en': 'Un moment'}
total mappings 28
a001 a001-c1 resolu {'Elle': 'Alice', 'se': 'Alice', 'elle': 'Alice', 'lui': 'Alice', 'en': 'Alice'}
a001 a001-c2 resolu {'Elle': 'Alice', 'se': 'Alice', 'elle': 'Alice', 'lui': 'Alice', 'en': 'Alice'}
a002 a002-c1 resolu {'Elle': 'Alice', 'en': 'Alice', 'y': 'Alice'}
a002 a002-c2 exclu {'Elle': 'Alice', 'en': 'Alice', 'y': 'Alice'}
a002 a002-c3 exclu {'Elle': 'Alice', 'en': 'Alice', 'y': 'Alice'}
a003 a003-c1 exclu {'Elle': 'Alice', 'sa': 'Alice', 'elle': 'Alice', 'se': 'Alice'}
a003 a003-c2 resolu {'Elle': 'Alice', 'sa': 'Alice', 'elle': 'Alice', 'se': 'Alice'}
a003 a003-c3 exclu {'Elle': 'Al
… [776 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"9/16\\|16/28\\|12/28\" reports/rapport-etat-s.md reports/rapport-coordination-s.md reports/rapport-coordination-s-v2.md reports/*.json 2>/dev/null | head -40", "description": "Search mapping ratios"}`

  ```
reports/rapport-etat-s.md:130:| **total** | **19** | **19** | **11** | **8** | **16/28** |
reports/rapport-etat-s.md:147:- **16/28 justes** ; **12/28 faux** ; **2 formes manquantes**.
reports/rapport-etat-s.md:313:**La référence n'est pas validée.** 12/28 mappings faux, 2 formes absentes, 0 note : le journal
reports/rapport-etat-s.md:345:| **les référents ne sont pas validés** | **12/28** faux, **2** manquants, **0 note** ; valeurs = défauts de la page | auditer/corriger les 14 formes (action A2) ; forcer la résolution avant le verdict |
reports/rapport-etat-s.md:450:  justes ; ils en portent **9/12** sur a001–a003 et **16/28** sur les 9. La source anglaise est
reports/rapport-coordination-s-v2.md:78:- Les référents enregistrés restent ceux de la v1 : **9/16 mappings uniques faux** (l'audit
reports/rapport-coordination-s-v2.md:79:  large compte **12/28 occurrences**), et le seul `compatible` est **a008**, le paragraphe à
reports/rapport-coordination-s-v2.md:143:| segments avec `profondeur` | **169/169** | **0/369** |
reports/rapport-coordination-s-v2.md:148:19/19, 169/169 `profondeur`. S'il désigne **la page `/`**, il ne fonctionne pas : la page `/`
reports/rapport-coordination-s-v
… [1821 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"référent\\|referent\" reports/rapport-coordination-s.md | head -40; echo \"---\"; sed -n '1,120p' reports/rapport-coordination-s.md", "description": "Read v1 coordination referent section"}`

  ```
26:- **Ne tranche pas** la qualité des référents enregistrés : elle la signale (§ 1.1), parce que le
75:### 1.1 Les référents enregistrés (inchangés par le commit)
80:| phrase | référents enregistrés | justes |
91:16 référents sont faux ou restés aux défauts de la page** (`a008` en porte 5 à lui seul). Committer
92:le fichier tel quel **fige ces référents** avec `auteur: humain` et `note: ""`. Deux options, à
96:  puis ouvrir une correction de référents séparée (le fichier est append-only, la correction peut
148:- Le seul `compatible` est **a008**, précisément le paragraphe à **0/5** référents : le statut dit
149:  « pas tranché », mais 5 référents faux sont enregistrés.
261:- **Ne change pas** : les 9 référents faux, l'absence de note, le `compatible` de a008, et le
274:- **L'audit des référents est cité, pas re-mesuré ici** : les 16 mappings et le 7/16 viennent de
290:- `reports/rapport-etat-s.md` (audit des référents, § 2)
299:- [rapport-etat-s.md](rapport-etat-s.md) — l'audit 19/19 et les 12 référents faux.
---
# S — les 11 verdicts de `/paragraphes` ne sont pas dans git

> **Ligne de roadmap** : S · **Date** : 2026-11-13 · **HEAD parent mesuré** : `ced21933`
> · **Sous-module 
… [6686 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (ss -ltnp 2>/dev/null | grep -E ':8765|:9000|:8771|:3080' || true); echo \"--- procs ---\"; ps -eo pid,comm,args | grep -E \"serveur\\.py|src/app\\.py\" | grep -v grep || true", "description": "Check listening ports and server proces … [5 caractères tronqués]`

  ```
LISTEN 0      511          0.0.0.0:3080       0.0.0.0:*    users:(("node-MainThread",pid=2999,fd=21))
LISTEN 0      5          127.0.0.1:8765       0.0.0.0:*    users:(("python3",pid=2725542,fd=3))
LISTEN 0      5          127.0.0.1:8771       0.0.0.0:*    users:(("docwatch",pid=3291,fd=3))
--- procs ---
2725526 bash            bash -c sleep 2; cd /home/stephane/Data13TB/stephane/GitHub/financemeteo && python3 src/app.py --no-browser
2725542 python3         python3 src/app.py --no-browser
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && stat -c '%y %s %n' donnees/phrases_generees.json donnees/validations.jsonl donnees/paragraphes-validations.jsonl generateur.py static/app.js static/paragraphes.js; echo \"--- git status ---\"; git status --porcelain; … [165 caractères tronqués]`

  ```
2026-11-02 20:35:33.102281270 -0500 527440 donnees/phrases_generees.json
2026-11-03 16:46:42.000780784 -0500 25828 donnees/validations.jsonl
2026-11-04 15:10:08.811109760 -0500 6047 donnees/paragraphes-validations.jsonl
2026-11-04 11:41:49.129836555 -0500 30580 generateur.py
2026-11-02 02:10:03.536776349 -0500 6757 static/app.js
2026-11-03 17:47:50.239449461 -0500 5251 static/paragraphes.js
--- git status ---
--- parent status (structures only) ---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && sed -n '120,220p' serveur.py && sed -n '220,312p' serveur.py", "description": "Read server API state methods"}`

  ```
ligne = {"phrase_id": phrase_id, "candidat_id": candidat_id, "statut": statut,
                 "note": note[:500], "contexte": contexte[:4000], "niveau": niveau,
                 "auteur": auteur[:80], "horodatage": time.strftime("%Y-%m-%dT%H:%M:%S")}
        with self.verrou:
            with (self.dossier / "validations.jsonl").open("a", encoding="utf-8") as f:
                f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
        return ligne

    def niveaux_minimaux(self) -> dict:
        """Le plus petit niveau de contexte où une lecture a été *tranchée* (résolue ou exclue).

        C'est la mesure de « combien de contexte il faut » : 0 = la phrase seule suffit,
        2 = il faut le paragraphe, 3 = le document, 4 = le genre.
        """
        decisifs = {}
        for v in self._journal("validations.jsonl"):
            if v.get("statut") not in ("resolu", "exclu"):
                continue
            pid = v["phrase_id"]
            n = int(v.get("niveau", 0))
            decisifs[pid] = min(decisifs.get(pid, 9), n)
        return decisifs

    def evaluer(self, phrase_id: str, fournisseur: str = "baseline", contexte: str = "",
                niveau: int = 0) 
… [8104 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 serveur.py --port 9000 --hote 127.0.0.1 > /tmp/recette-s-serveur-9000.log 2>&1 & echo $! > /tmp/recette-s-serveur-9000.pid\nsleep 1.5\ncat /tmp/recette-s-serveur-9000.log\necho \"--- … [922 caractères tronqués]`

  ```
banc de structures · http://127.0.0.1:9000 · 207 phrases
--- GET / ---
code=200 taille=2350
<title>Structures — le banc d'interprétations</title>
--- GET /api/phrases ---
code=200 taille=403437
--- GET /paragraphes ---
code=200 taille=3493
--- GET /api/paragraphes ---
code=200 taille=95470
serveur arrêté
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections\nd=json.load(open('/tmp/recette-s-api-phrases.json'))\nprint('keys', sorted(d.keys()))\nprint('phrases',len(d['phrases']),'cands',sum(len(p['candidats']) for p in d … [1271 caractères tronqués]`

  ```
keys ['llm', 'niveaux', 'niveaux_minimaux', 'phrases', 'validations']
phrases 207 cands 369
validations 150
cands with profondeur 0
segments 2414
niveau max {0: 10, 1: 277, 2: 82}
statuts Counter({'resolu': 74, 'exclu': 64, 'compatible': 11, 'double_sens': 1})
unique pairs 147
phrases with val 74
niveaux_minimaux 73
paragraphes 9 cands 19
cands with profondeur 19
validations 19
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '380,470p' reports/rapport-etat-s.md", "description": "Read A2 action details"}`

  ```
```

**Commande du harnais** (à écrire dans `work/banque-v7/preparer.py` ; n'existe pas encore) :

```bash
cd tools/structures && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
  python3 ../../work/banque-v7/preparer.py
```

**Garde-fou.** Ne pas régénérer par index : `p006-c2`, `c023-c3`, `c056-c2`, `c056-c3`,
`c064-c2` seraient perdus. La signature est la clé.

### A2 — Auditer les 28 référents des 19 verdicts (P1, immédiat)

**Pourquoi.** Le journal enregistre 12 mappings faux et 2 formes manquantes ; si on l'utilise
comme gold, on apprend le défaut de la page, pas la référence. C'est le préalable à tout usage
des 19 verdicts comme banque de référents.

**Livrable.** `work/referents/verdicts-corriges.jsonl` (14 occurrences, 12 formes uniques) +
`reports/rapport-s-referents-verdicts.md` : table des 28 mappings, 12 corrections, 2 ajouts,
0 contradiction avec l'anglais.

**Mesure.** 28 mappings audités ; **14/14** occurrences avec un verdict ; **0** mapping faux ;
**0** forme manquante ; 6/9 paragraphes fautifs → **0/9**.

**Commande existante (extraction, lecture seule) :**

```bash
cd tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json
src = {p["id"]: p for p in 
… [3449 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, re, sys\nsys.path.insert(0,'.')\nimport generateur\nD='donnees/'\nphr=json.load(open(D+'phrases.json'))['phrases']+json.load(open(D+'phrases_gener … [2789 caractères tronqués]`

  ```
kept 106 quar 41
distinct v7 cands matched 65
v7 depth buckets {'>=3': 99, '2': 221, '1': 37, '0': 2}
v7 judged by depth {'1': 10, '2': 32, '>=3': 23}
v7 phrases full/part/none 21 35 151
quar statuses Counter({'resolu': 18, 'exclu': 17, 'compatible': 6})
kept statuses Counter({'resolu': 55, 'exclu': 46, 'compatible': 5})
quar accepted 24 excluded 17
kept accepted 60 excluded 46
kept v7 depth Counter({2: 50, 3: 35, 1: 10, 4: 9, 5: 2})
old niveau max all Counter({1: 277, 2: 82, 0: 10})
quar old niveau max Counter({1: 29, 2: 12})
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys\nsys.path.insert(0,'.')\nimport generateur\nD='donnees/'\nphr=json.load(open(D+'phrases.json'))['phrases']+json.load(open(D+'phrases_generees. … [1501 caractères tronqués]`

  ```
groups with >1 judged old candidate sharing signature: 49
c002 n= 2 v7matches= []
    c002-c1 resolu att= {'segment': 'qui court à toutes jambes', 'cible': 'le Lapin Blanc', 'genre': 'GN'}
    c002-c2 compatible att= {'segment': 'qui court à toutes jambes', 'cible': 'Elle voit', 'genre': 'GV'}
c004 n= 2 v7matches= []
    c004-c2 resolu att= {'segment': "d'une voix conciliante", 'cible': 'dit Alice', 'genre': 'GV'}
    c004-c1 compatible att= {'segment': "d'une voix conciliante", 'cible': "l'intention", 'genre': 'GN'}
c007 n= 2 v7matches= [1, 2]
    c007-c2 resolu att= {'segment': "que je vais devenir d'une minute à l'autre", 'cible': 'sûre', 'genre': 'GV'}
    c007-c1 exclu att= {'segment': "que je vais devenir d'une minute à l'autre", 'cible': 'jamais', 'genre': 'GP'}
c008 n= 2 v7matches= [1, 2]
    c008-c1 resolu att= {'segment': 'à attraper le bébé', 'cible': 'peine', 'genre': 'GP'}
    c008-c2 exclu att= {'segment': 'à attraper le bébé', 'cible': 'Alice eut', 'genre': 'GV'}
c009 n= 3 v7matches= []
    c009-c1 exclu att= {'segment': 'sur', 'cible': 'autres', 'genre': 'GP'}
    c009-c2 exclu att= {'segment': 'sur', 'cible': 'le coude appuyé', 'genre': 'GN'}
    c009-c3 exclu att=
… [10683 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys, re\nsys.path.insert(0,'.')\nimport generateur\nD='donnees/'\nphr=json.load(open(D+'phrases.json'))['phrases']+json.load(open(D+'phrases_gener … [1475 caractères tronqués]`

  ```
tcr: kept 119 quar 28 distinct 74 duplicates 45
tt: kept 120 quar 27 distinct 63 duplicates 57
text: kept 120 quar 27 distinct 63 duplicates 57
tcr+att: kept 115 quar 32 distinct 115 duplicates 0
tcr+cible: kept 115 quar 32 distinct 115 duplicates 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys\nsys.path.insert(0,'.')\nimport generateur\nD='donnees/'\nphr=json.load(open(D+'phrases.json'))['phrases']+json.load(open(D+'phrases_generees. … [1257 caractères tronqués]`

  ```
norm=False att=False: kept 106 quar 41 distinct 65 dup 41
norm=False att=True: kept 106 quar 41 distinct 106 dup 0
norm=True att=False: kept 119 quar 28 distinct 74 dup 45
norm=True att=True: kept 115 quar 32 distinct 115 dup 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys, re\nsys.path.insert(0,'.')\nimport generateur\nD='donnees/'\nphr=json.load(open(D+'phrases.json'))['phrases']+json.load(open(D+'phrases_gener … [2010 caractères tronqués]`

  ```
sets exact tcr vs exact tcr+att same? True True
exact tcr+att vs norm tcr+att kept diff: 0 9
rescued by norm+att (in q1, in k3): [('p001', 'p001-c1'), ('p002', 'p002-c1'), ('p002', 'p002-c2'), ('p003', 'p003-c1'), ('p003', 'p003-c2'), ('p004', 'p004-c1'), ('p005', 'p005-c1'), ('p006', 'p006-c2'), ('p007', 'p007-c1')]
newly quarantined by norm+att (in k1, in q3): []
RESCUED p001 p001-c1 oldidx 1 newidx 2 status resolu
  old texts [("'Le chat'", 'GN', 'agent'), ("' de la voisine'", 'GP', 'possession'), ("' qui dort sur le toit'", 'REL', 'qualite'), ("' se réveille'", 'GV', 'predicat')]
  v7  texts [("'Le chat'", 'GN', 'agent'), ("'de la voisine'", 'GP', 'possession'), ("'qui dort sur le toit'", 'REL', 'qualite'), ("'se réveille'", 'GV', 'predicat')]
RESCUED p002 p002-c1 oldidx 1 newidx 2 status resolu
  old texts [('"J\'ai vu"', 'GV', 'predicat'), ('" l\'homme"', 'GN', 'patient'), ("' avec le télescope'", 'GP', 'instrument')]
  v7  texts [('"J\'ai vu"', 'GV', 'predicat'), ('"l\'homme"', 'GN', 'patient'), ("'avec le télescope'", 'GP', 'instrument')]
RESCUED p002 p002-c2 oldidx 2 newidx 1 status compatible
  old texts [('"J\'ai vu"', 'GV', 'predicat'), ('" l\'homme"', 'GN', 'patient'),
… [1944 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain | head -30; echo \"count:\"; git status --porcelain | wc -l", "description": "Check parent working tree status"}`

  ```
M docs/produit/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
count:
12
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && grep -rn \"write_text\\|open(.*[\\\"']w\\|open(.*[\\\"']a\\|mkdir\\|unlink\\|remove(\" tests/ | head -30; echo \"---\"; ls tests/", "description": "Check tests for writes"}`

  ```
tests/test_export.py:23:        with (self.dossier / "validations.jsonl").open("a", encoding="utf-8") as f:
tests/test_export.py:45:        (self.dossier / "phrases.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
tests/test_export.py:73:        with (self.dossier / "validations.jsonl").open("a", encoding="utf-8") as f:
tests/test_export.py:98:        with (self.dossier / "validations.jsonl").open("a", encoding="utf-8") as f:
tests/test_export.py:137:        chemin.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
tests/test_export.py:163:        sortie.write_text(corps, encoding="utf-8")
tests/test_export.py:169:        manifeste.write_text(json.dumps(m), encoding="utf-8")
tests/test_export.py:179:        manifeste.write_text(json.dumps(m), encoding="utf-8")
tests/test_mesure_corpus.py:13:            p.write_text("Le chat dort sur le canapé du salon.\n"
tests/test_candidats_corpus.py:13:            p.write_text("Le chat dort sur le canapé du salon, tranquillement.\n"
---
__pycache__
test_arbre_svg.py
test_candidats_corpus.py
test_export.py
test_generateur.py
test_mesure_corpus.py
test_serveur.py
[stderr]
grep: tests/__pycache__/test_export.cpyth
… [194 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys, hashlib, re\nsys.path.insert(0,'.')\nimport generateur, mesure_arbre\nD='donnees/'\nphr=json.load(open(D+'phrases.json'))['phrases']+json.loa … [3265 caractères tronqués]`

  ```
kept 106 quar 41 distinct 106
old full 74
old full -> Counter({'none': 74})
v7 coverage full/part/none 0 0 207
distinct v7 judged by depth {} deep judged 0
v7 all depth Counter({2: 221, 3: 84, 1: 37, 4: 13, 5: 2, 0: 2})
kept statuses Counter({'resolu': 55, 'exclu': 46, 'compatible': 5})
quar statuses Counter({'resolu': 18, 'exclu': 17, 'compatible': 6})
quar accepted 24
kept same index 106 different index 0
QUAR LIST
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 73, in <module>
TypeError: 'NoneType' object is not subscriptable
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys, hashlib, re\nsys.path.insert(0,'.')\nimport generateur\nD='donnees/'\nphr=json.load(open(D+'phrases.json'))['phrases']+json.load(open(D+'phra … [2849 caractères tronqués]`

  ```
kept 106 quar 41 distinct 106
old full 74
old full -> Counter({'full': 56, 'none': 18})
v7 coverage full/part/none 56 0 151
distinct v7 judged by depth {1: 10, 2: 50, 3: 35, 4: 9, 5: 2} deep judged 46
kept statuses Counter({'resolu': 55, 'exclu': 46, 'compatible': 5})
quar statuses Counter({'resolu': 18, 'exclu': 17, 'compatible': 6})
quar accepted 24
kept same index 106 different index 0
QUAR LIST
c002 c002-c1 oldidx 1 n_new 2 status resolu reason meme_index_change
c002 c002-c2 oldidx 2 n_new 2 status compatible reason meme_index_change
c004 c004-c1 oldidx 1 n_new 2 status compatible reason meme_index_change
c004 c004-c2 oldidx 2 n_new 2 status resolu reason meme_index_change
c009 c009-c1 oldidx 1 n_new 3 status exclu reason meme_index_change
c009 c009-c2 oldidx 2 n_new 3 status exclu reason meme_index_change
c009 c009-c3 oldidx 3 n_new 3 status exclu reason meme_index_change
c011 c011-c1 oldidx 1 n_new 2 status exclu reason meme_index_change
c011 c011-c2 oldidx 2 n_new 2 status resolu reason meme_index_change
c013 c013-c1 oldidx 1 n_new 3 status exclu reason meme_index_change
c013 c013-c2 oldidx 2 n_new 3 status resolu reason meme_index_change
c013 c013-c3 oldidx 3 n_new 3 status
… [2002 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 timeout 180 python3 -m unittest discover -s tests -v 2>&1 | tail -25", "description": "Run 56 submodule tests"}`

  ```
ok
test_niveau_minimal (test_serveur.TestBanc.test_niveau_minimal) ...   127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
ok
test_paragraphes (test_serveur.TestBanc.test_paragraphes) ...   127.0.0.1 · "GET /api/paragraphes HTTP/1.1" 200 -
  127.0.0.1 · "POST /api/valider-paragraphe HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/paragraphes HTTP/1.1" 200 -
ok
test_phrases (test_serveur.TestBanc.test_phrases) ...   127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
ok
test_static (test_serveur.TestBanc.test_static) ...   127.0.0.1 · "GET / HTTP/1.1" 200 -
ok
test_statut_invalide (test_serveur.TestBanc.test_statut_invalide) ...   127.0.0.1 · "POST /api/valider HTTP/1.1" 400 -
ok
test_valider_et_export (test_serveur.TestBanc.test_valider_et_export) ...   127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/export HTTP/1.1" 200 -
ok

----------------------------------------------------------------------
Ran 56 tests in 4.333s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git status --porcelain && echo \"clean=$?\"; git rev-parse HEAD; git rev-parse --short HEAD; echo \"--- parent ---\"; cd ../.. && git rev-parse --short HEAD", "description": "Verify submodule clean after tests"}`

  ```
clean=0
389b99f8383eb47c0cc008f5d3211c9d65d895fc
389b99f
--- parent ---
6f862993
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-coordination-s-v2.json'))\nprint(json.dumps(d, ensure_ascii=False, indent=1)[:4000])\nPY", "description": "Inspect v2 JSON structure"}`

  ```
{
 "version": 2,
 "date": "2026-11-15",
 "heure": "02:20 HNE",
 "head": "292c70b5",
 "head_parent": "292c70b52a5656c16360db2570950abbe51c56b6",
 "ligne": "S",
 "objet": "coordination S, suite de J4.2 : l'état de la page /, le service de la v7, le pare-feu, la commande de lancement et ce qui reste à S ; les 11 verdicts sont committés (389b99f)",
 "fiche": "reports/rapport-coordination-s-v2.md",
 "v1": "reports/rapport-coordination-s.md",
 "verdict": "Les 11 verdicts a004–a009 sont committés (sous-module 389b99f, pointeur parent 31ce36fd) : 19/19 candidats, 11 acceptés, 8 exclus. La page / ne sert pas la v7 : 369 candidats stockés, 0 avec profondeur, distribution des niveau 10/277/82 ; la v7 dynamique donne 359 candidats, 2/37/221/84/13/2 et 99 à profondeur >= 3. Aucun service S n'est en écoute ; le port 8765 est tenu par financemeteo (pid 2725542), et un lancement de mesure sur 9000 répond 200. firewalld est actif mais non interrogeable sans root ; le serveur écoute 127.0.0.1 par défaut. 41 paires de verdicts de la banque n'ont pas de correspondance v7 exacte, pas 5.",
 "aucune_modification_s": [
  "tools/structures/"
 ],
 "lecture_seule": true,
 "verdicts": {
  "sous_module": {
   
… [2800 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/rapport-s-paragraphes* reports/rapport-etat-s.json 2>/dev/null; python3 - <<'PY'\nimport json,glob\nfor f in glob.glob('reports/rapport-etat-s.json'):\n d=json.load(open(f)); print(f, type(d), list(d)[:20] if isinstance(d, … [122 caractères tronqués]`

  ```
reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-coordination-s-v2.json'))\nprint(list(d.keys()))\nfor k in d:\n    if k in ('verdicts',): continue\n    print('\\n###',k)\n    print(json.dumps(d[k], ensure_ascii=False … [78 caractères tronqués]`

  ```
['version', 'date', 'heure', 'head', 'head_parent', 'ligne', 'objet', 'fiche', 'v1', 'verdict', 'aucune_modification_s', 'lecture_seule', 'verdicts', 'page', 'migration', 'pare_feu', 'commande_lancement', 'reste_a_s', 'ce_qui_pourrait_le_rendre_faux', 'fichiers_lus_non_modifies', 'references']

### version
2

### date
"2026-11-15"

### heure
"02:20 HNE"

### head
"292c70b5"

### head_parent
"292c70b52a5656c16360db2570950abbe51c56b6"

### ligne
"S"

### objet
"coordination S, suite de J4.2 : l'état de la page /, le service de la v7, le pare-feu, la commande de lancement et ce qui reste à S ; les 11 verdicts sont committés (389b99f)"

### fiche
"reports/rapport-coordination-s-v2.md"

### v1
"reports/rapport-coordination-s.md"

### verdict
"Les 11 verdicts a004–a009 sont committés (sous-module 389b99f, pointeur parent 31ce36fd) : 19/19 candidats, 11 acceptés, 8 exclus. La page / ne sert pas la v7 : 369 candidats stockés, 0 avec profondeur, distribution des niveau 10/277/82 ; la v7 dynamique donne 359 candidats, 2/37/221/84/13/2 et 99 à profondeur >= 3. Aucun service S n'est en écoute ; le port 8765 est tenu par financemeteo (pid 2725542), et un lancement de mesure sur 9000 répond 200.
… [13118 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys, hashlib\nsys.path.insert(0,'.')\nimport generateur\nD='donnees/'\nphr=json.load(open(D+'phrases.json'))['phrases']+json.load(open(D+'phrases_ … [1687 caractères tronqués]`

  ```
old sha 569a61fa6ecef9b03c612acffee09cfdcb9b6808c8de310c4e425fd084cd371b
v7  sha 4620252570a8ff532c92b2dd82ae6cdff37789c2452400b538b4fdaa8444392e
old self True v7 self True
unique old 241 v7 239 inter 204 jaccard_global 0.73913
perphrase common 304 oldonly 65 newonly 55
jaccard_multiset 0.716981
donnees/phrases.json 51e07f1c7695cdf91298e4657d4ac767f3948f53fa4e6924223f04a4ac41a331
donnees/phrases_generees.json 43957a3b9ad2422b7897a29462086ebe36877eb0d856eda4fd26ad55b5620307
donnees/validations.jsonl ed7b0765440afc83bbc466eb7cc8b46a9e81c5fd9183ca2851c1205645dd64fd
donnees/paragraphes.json 877e829245d0053745c4a4b0989cae0441f0170041998e205ce4c12e6d00d7af
donnees/paragraphes-validations.jsonl a3c54c9cf2b81904ce43b43685be78f18ed675df2745e7b72ddcf0943d531123
generateur.py 291df65a43693aac4cdd3fb7fd25955b5eb7f103e24e57d8c505e31d765202d5
mesure_arbre.py 568ab6429b0fbe4528d61e97479c6bf71163fbacad864f95f0224c6cfd522531
serveur.py 0829c3caeda800b92f391bb5f7a340430d56158463857f7c614a76b5c5f5f1a6
static/app.js fceab2b2245675ab6bd24effaedc7dcc005f4bbfc044f58e18d60dcb28f2e41f
static/paragraphes.js c7203773a906540b0c868d62dc20211f4540e2430ee991aeea0fde4ef9aaecc5
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys, re\nsys.path.insert(0,'.')\nimport generateur\nD='donnees/'\nphr=json.load(open(D+'phrases.json'))['phrases']+json.load(open(D+'phrases_gener … [2326 caractères tronqués]`

  ```
norm+att kept 115 quar 32 distinct 115
32 quarantine:
  c002 c002-c1 oldidx 1 nnew 2 status resolu reason meme_index_change
  c002 c002-c2 oldidx 2 nnew 2 status compatible reason meme_index_change
  c004 c004-c1 oldidx 1 nnew 2 status compatible reason meme_index_change
  c004 c004-c2 oldidx 2 nnew 2 status resolu reason meme_index_change
  c009 c009-c1 oldidx 1 nnew 3 status exclu reason meme_index_change
  c009 c009-c2 oldidx 2 nnew 3 status exclu reason meme_index_change
  c009 c009-c3 oldidx 3 nnew 3 status exclu reason meme_index_change
  c011 c011-c1 oldidx 1 nnew 2 status exclu reason meme_index_change
  c011 c011-c2 oldidx 2 nnew 2 status resolu reason meme_index_change
  c013 c013-c1 oldidx 1 nnew 3 status exclu reason meme_index_change
  c013 c013-c2 oldidx 2 nnew 3 status resolu reason meme_index_change
  c013 c013-c3 oldidx 3 nnew 3 status resolu reason meme_index_change
  c020 c020-c1 oldidx 1 nnew 3 status exclu reason meme_index_change
  c020 c020-c2 oldidx 2 nnew 3 status exclu reason meme_index_change
  c020 c020-c3 oldidx 3 nnew 3 status exclu reason meme_index_change
  c023 c023-c1 oldidx 1 nnew 2 status resolu reason meme_index_change
  c023 c023-c2 oldidx 2 nn
… [1892 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections\nD='donnees/'\nparas=json.load(open(D+'paragraphes.json'))['paragraphes']\nvals=[json.loads(l) for l in open(D+'paragraphes-validations.jsonl') if  … [1761 caractères tronqués]`

  ```
('a001', 'Elle', 'Alice', 'Alice', 'juste')
('a001', 'elle', 'Alice', 'Alice', 'juste')
('a001', 'en', 'Alice', None, 'faux')
('a001', 'les', None, 'les conseils', 'manquant')
('a001', 'lui', 'Alice', 'Alice', 'juste')
('a001', 'se', 'Alice', 'Alice', 'juste')
('a002', 'Elle', 'Alice', 'Alice', 'juste')
('a002', 'en', 'Alice', None, 'faux')
('a002', "l'", None, 'la boîte', 'manquant')
('a002', 'y', 'Alice', 'la boîte', 'faux')
('a003', 'Elle', 'Alice', 'Alice', 'juste')
('a003', 'elle', 'Alice', 'Alice', 'juste')
('a003', 'sa', 'Alice', 'Alice', 'juste')
('a003', 'se', 'Alice', 'Alice', 'juste')
('a004', 'sa', 'ALICE', 'Alice', 'juste')
('a005', 'elle', 'Alice', 'Alice', 'juste')
('a005', 'en', 'coup', 'la salle', 'faux')
('a005', 'son', 'Alice', 'Alice', 'juste')
('a006', 'cela', 'Comme', 'attendre à la petite porte', 'faux')
('a006', 'elle', 'Alice', 'Alice', 'juste')
('a006', 'son', 'Alice', 'Alice', 'juste')
('a006', 'y', 'table', 'table', 'juste')
('a008', 'Je', 'le contenu', 'Alice', 'faux')
('a008', 'en', 'Je me sens toute drôle', None, 'faux')
('a008', 'je', 'Je me sens toute drôle', 'Alice', 'faux')
('a008', 'me', 'le contenu', 'Alice', 'faux')
('a008', 'on', 'Je me sens t
… [350 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys, re\nsys.path.insert(0,'.')\nimport generateur\nD='donnees/'\nphr=json.load(open(D+'phrases.json'))['phrases']+json.load(open(D+'phrases_gener … [1340 caractères tronqués]`

  ```
norm+att quar 32 accepted 17 excluded 15
phrases 16 Counter({'c009': 3, 'c013': 3, 'c020': 3, 'c023': 3, 'c056': 3, 'c002': 2, 'c004': 2, 'c011': 2, 'c043': 2, 'c064': 2, 'c065': 2, 'p001': 1, 'p004': 1, 'p005': 1, 'p006': 1, 'p007': 1})
all last accepted 84 excluded 63
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys\nsys.path.insert(0,'.')\nimport generateur\nD='donnees/'\nphr=json.load(open(D+'phrases.json'))['phrases']+json.load(open(D+'phrases_generees. … [1783 caractères tronqués]`

  ```
kept 115 distinct 115
v7 coverage full/part/none 59 4 144
old full -> Counter({'full': 59, 'none': 11, 'part': 4})
judged depth {1: 13, 2: 55, 3: 36, 4: 9, 5: 2} deep 47
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && sed -n '1,80p' static/app.js", "description": "Read app.js rendering"}`

  ```
const $ = (s) => document.querySelector(s);
const esc = (t) => t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

let etat = { phrases: [], validations: [], llm: [] };
let dernierModele = null;

function phraseColoree(phrase, cand) {
  let html = "", curseur = 0;
  for (const s of cand.segments) {
    if (s.debut > curseur) html += esc(phrase.texte.slice(curseur, s.debut));
    html += `<span class="seg t-${s.type}" title="${s.type} · ${s.role}">${esc(s.texte)}</span>`;
    curseur = s.fin;
  }
  if (curseur < phrase.texte.length) html += esc(phrase.texte.slice(curseur));
  return html;
}

function blocs(cand) {
  return cand.segments.map((s) =>
    `<div class="bloc" style="margin-left:${s.niveau * 1.4}em">
       <span class="t-${s.type}">${esc(s.texte.trim())}</span>
       <em>${s.type} · ${s.role}</em></div>`).join("");
}

function statutDe(phraseId, candId) {
  const v = etat.validations.filter((x) => x.phrase_id === phraseId && x.candidat_id === candId);
  return v.length ? v[v.length - 1] : null;
}

function contexteDe(phrase) {
  const v = etat.validations.filter((x) => x.phrase_id === phrase.id && (x.contexte || "").trim());
  if (v.length) return v[v.
… [2820 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l reports/rapport-coordination-s-v2.json; python3 -c \"import json; d=json.load(open('reports/rapport-coordination-s-v2.json')); print(len(json.dumps(d,ensure_ascii=False)))\"", "description": "Check v2 JSON size"}`

  ```
-rw-r--r--. 1 stephane stephane 22126 15 nov 02:30 reports/rapport-coordination-s-v2.json
18066
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M:%S %Z'; date -u '+%Y-%m-%dT%H:%M:%SZ'", "description": "Check system date"}`

  ```
2026-11-15 12:33:17 EST
2026-11-15T17:33:17Z
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git ls-tree HEAD tools/structures && git log --oneline -1 -- tools/structures && git -C tools/structures log -1 --format='%H %cI %s'", "description": "Check submodule pointer at parent HEAD"}`

  ```
160000 commit 389b99f8383eb47c0cc008f5d3211c9d65d895fc	tools/structures
31ce36fd S — LE POINTEUR DU SOUS-MODULE AVANCE : LES 11 VERDICTS HUMAINS SONT DANS GIT (19/19, 11 ACCEPTÉS, 8 EXCLUS)
389b99f8383eb47c0cc008f5d3211c9d65d895fc 2026-11-14T09:49:39-05:00 S — LES 11 VERDICTS HUMAINS DE /paragraphes (a004–a009) : 19/19 CANDIDATS JUGÉS, 11 ACCEPTÉS, 8 EXCLUS ; DÉCISION DU 14/11 (3B), EXCEPTION AUTORISÉE
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys, re\nsys.path.insert(0,'.')\nimport generateur\nD='donnees/'\nphr=json.load(open(D+'phrases.json'))['phrases']+json.load(open(D+'phrases_gener … [1103 caractères tronqués]`

  ```
head att kept 117 quar 30 distinct 117
quar 30
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys, re\nsys.path.insert(0,'.')\nimport generateur\nD='donnees/'\nphr=json.load(open(D+'phrases.json'))['phrases']+json.load(open(D+'phrases_gener … [1434 caractères tronqués]`

  ```
117 minus 115 [('p001', 'p001-c2'), ('p005', 'p005-c2')]
targets [(('p001', 'p001-c2'), 1), (('p005', 'p005-c2'), 1)]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections\nvals=[json.loads(l) for l in open('donnees/validations.jsonl') if l.strip()]\nprint('notes non vides',sum(1 for v in vals if (v.get('note') or '') … [619 caractères tronqués]`

  ```
notes non vides 1
niveaux all Counter({0: 143, 2: 5, 3: 2})
niveaux last Counter({0: 141, 2: 4, 3: 2})
contextes non vides 6
p notes 0
p statuts Counter({'resolu': 10, 'exclu': 8, 'compatible': 1})
  ```

### 🤖 Assistant

I have the core measurements. Let me build a reproducible read-only harness that generates the JSON.

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/page-s-mesure/mesurer.py", "content": "#!/usr/bin/env python3\n\"\"\"mesurer.py — la recette de la page `/` de S (J4 après-midi, part du pilote).\n\nLecture seule dans `tools/structures/` :\n\n- lit `phrases.json`, `phrases_generees … [56578 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/page-s-mesure/mesurer.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 work/page-s-mesure/mesurer.py --sortie /tmp/rapport-page-s-mesure.json 2>&1 | tail -30", "description": "Run measurement harness"}`

  ```
207 phrases · 369 candidats anciens · 359 v7
  migration exacte : 106 gardés / 41 en quarantaine · 65 cibles distinctes
  référents : 16 justes / 12 faux / 2 manquants
  contrôle négatif : H0 rejetée : 369 ≠ 359, 0/369 contre 359/359 `profondeur`, 0 contre 99 candidats à ≥3, empreintes différentes, Jaccard 0,717 ; le banc ancien et la v7 ne sont pas le même banc.
  tests : 56 · OK
  → /tmp/rapport-page-s-mesure.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l /tmp/rapport-page-s-mesure.json && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/rapport-page-s-mesure.json'))\nprint('top keys:', list(d))\nprint('\\nVERDICT:\\n', d['verdict'][:1000])\nprint('\\nBANC ANCIEN:', {k:d['b … [546 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 61985 15 nov 12:34 /tmp/rapport-page-s-mesure.json
top keys: ['version', 'date', 'heure', 'tache', 'fiche', 'ligne', 'objet', 'lecture_seule', 'aucune_modification_s', 'head_parent', 'head_parent_court', 'sous_module', 'sous_module_court', 'branche', 'verdict', 'banc_ancien', 'v7', 'comparaison', 'migration', 'referent', 'page', 'controle_negatif', 'tests_sous_module', 'git', 'ce_qui_pourrait_le_rendre_faux', 'fichiers_lus_non_modifies', 'references']

VERDICT:
 La page `/` sert toujours le banc ancien : 369 candidats, 0 avec `profondeur`, 0 à ≥3, distribution 10/277/82 ; la v7 dynamique donne 359 candidats, 2/37/221/84/13/2 et 99 à ≥3. Attention : « 369/0 » et « 359/99 » ne sont pas des comptes de verdicts — `/` porte 150 verdicts / 147 paires, et la v7 n'a aucun verdict natif. La migration exacte reproduit 106 conservés / 41 en quarantaine, mais la signature nue ne donne que 65 cibles distinctes (41 collisions) ; avec l'attachement, 106/41 devient injectif. Les référents sont toujours 28 mappings / 16 justes / 12 faux / 2 manquants (0 note), et la cible « 14 occurrences / 12 formes » ne couvre que a001–a003. Contrôle négatif : les deux bancs diffèr
… [2570 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/rapport-page-s-mesure.json'))\nm=d['migration']\nprint('MIGRATION KEYS', list(m))\nfor k in ['exacte','exacte_attachement','quarantaine_exacte','cinq_sans_index','variantes','recu … [215 caractères tronqués]`

  ```
MIGRATION KEYS ['signature_v2', 'verdicts_banque', 'exacte', 'exacte_attachement', 'quarantaine_exacte', 'cinq_sans_index', 'variantes', 'recuperes_par_normalisation', 'recuperes_par_tete_de_cible', 'attachement_qui_separe', 'conclusion']

### exacte
{
 "label": "texte exact, type, rôle",
 "convention": {
  "normaliser_espaces": false,
  "avec_attachement": false,
  "cible_reduite_a_la_tete": false
 },
 "gardes": 106,
 "quarantaine": 41,
 "cibles_distinctes": 65,
 "collisions": 41,
 "phrases_couvertes": {
  "anciennes_completes": 74,
  "transitions_anciennes_completes": {
   "aucune": 18,
   "partielle": 35,
   "complete": 21
  },
  "v7_completes": 21,
  "v7_partielles": 35,
  "v7_aucune": 151
 },
 "candidats_juges": 65,
 "profondeurs_jugees": {
  "1": 10,
  "2": 32,
  "3": 18,
  "4": 4,
  "5": 1
 },
 "profonds_juges": 23,
 "statuts_gardes": {
  "compatible": 5,
  "resolu": 55,
  "exclu": 46
 },
 "statuts_quarantaine": {
  "exclu": 17,
  "resolu": 18,
  "compatible": 6
 },
 "quarantaine_acceptes": 24,
 "quarantaine_exclus": 17
}

### exacte_attachement
{
 "label": "texte exact, type, rôle + attachement",
 "convention": {
  "normaliser_espaces": false,
  "avec_attachement": true,
  
… [10650 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/rapport-page-s-mesure.json'))\nr=d['referent']\nprint('journal',json.dumps(r['journal'],ensure_ascii=False,indent=1))\nfor k in ['total_9_paragraphes','a001_a003','a004_a009','par … [354 caractères tronqués]`

  ```
journal {
 "fichier": "tools/structures/donnees/paragraphes-validations.jsonl",
 "lignes": 19,
 "paragraphes": 9,
 "statuts": {
  "resolu": 10,
  "exclu": 8,
  "compatible": 1
 },
 "acceptes": 11,
 "exclus": 8,
 "notes_non_vides": 0,
 "auteur": {
  "humain": 19
 },
 "mtime": "2026-11-04 15:10:08",
 "sha256": "a3c54c9cf2b81904ce43b43685be78f18ed675df2745e7b72ddcf0943d531123"
}

### total_9_paragraphes
{
 "lignes": 30,
 "mappings_presents": 28,
 "justes": 16,
 "faux": 12,
 "manquants": 2,
 "non_referents_ok": 0,
 "formes_attendues": 25,
 "occurrences_attendues": 27,
 "formes_actuelles": 28,
 "faux_detail": [
  {
   "paragraphe": "a001",
   "forme": "en",
   "observe": "Alice",
   "attendu": null
  },
  {
   "paragraphe": "a002",
   "forme": "en",
   "observe": "Alice",
   "attendu": null
  },
  {
   "paragraphe": "a002",
   "forme": "y",
   "observe": "Alice",
   "attendu": "la boîte"
  },
  {
   "paragraphe": "a005",
   "forme": "en",
   "observe": "coup",
   "attendu": "la salle"
  },
  {
   "paragraphe": "a006",
   "forme": "cela",
   "observe": "Comme",
   "attendu": "attendre à la petite porte"
  },
  {
   "paragraphe": "a008",
   "forme": "Je",
   "observe": "le contenu",
   "a
… [4781 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/rapport-page-s-mesure.json'))\nprint('PAGE:',json.dumps(d['page'],ensure_ascii=False,indent=1)[:8000])\nprint('\\nCONTROL:',json.dumps(d['controle_negatif'],ensure_ascii=False,ind … [68 caractères tronqués]`

  ```
PAGE: {
 "service": {
  "ports": [
   "LISTEN 0      511          0.0.0.0:3080       0.0.0.0:*    users:((\"node-MainThread\",pid=2999,fd=21))",
   "LISTEN 0      5          127.0.0.1:8765       0.0.0.0:*    users:((\"python3\",pid=2725542,fd=3))",
   "LISTEN 0      5          127.0.0.1:8771       0.0.0.0:*    users:((\"docwatch\",pid=3291,fd=3))",
   "LISTEN 0      5          127.0.0.1:9000       0.0.0.0:*    users:((\"python3\",pid=602059,fd=3))"
  ],
  "processus": [
   " 602059 python3         python3 serveur.py --port 9000 --hote 127.0.0.1",
   "2725526 bash            bash -c sleep 2; cd /home/stephane/Data13TB/stephane/GitHub/financemeteo && python3 src/app.py --no-browser",
   "2725542 python3         python3 src/app.py --no-browser"
  ],
  "s_serveur_en_ecoute": true,
  "get_8765": {
   "code": 200,
   "octets": 174051,
   "titre": "Portefeuille iA — tableau de bord"
  },
  "port_9000_libre": false,
  "note": "8765 est tenu par financemeteo ; le serveur de mesure utilise un port éphémère et est arrêté après les GET"
 },
 "http": {
  "port": 29415,
  "log": "banc de structures · http://127.0.0.1:29415 · 207 phrases",
  "routes": {
   "/": {
    "code": 200,
    "octets": 23
… [3733 caractères tronqués]
  ```

- **bash** `{"command": "ps -o pid,ppid,lstart,args -p 602059; echo \"--- cwd ---\"; readlink /proc/602059/cwd 2>/dev/null; echo \"--- cmdline ---\"; tr '\\0' ' ' < /proc/602059/cmdline; echo; echo \"--- pid file ---\"; cat /tmp/recette-s-serveur-9000.pid 2>/dev/null; echo; ss -ltnp 2>/dev/null | grep ':9000' | … [58 caractères tronqués]`

  ```
PID    PPID                  STARTED COMMAND
 602059    2886 dim nov 15 12:29:38 2026 python3 serveur.py --port 9000 --hote 127.0.0.1
--- cwd ---
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures
--- cmdline ---
python3 serveur.py --port 9000 --hote 127.0.0.1 
--- pid file ---
602057

LISTEN 0      5          127.0.0.1:9000       0.0.0.0:*    users:(("python3",pid=602059,fd=3))
  ```

- **bash** `{"command": "kill 602059 2>/dev/null || true; sleep 1; ps -eo pid,comm,args | grep 'serveur\\.py' | grep -v grep || echo \"aucun serveur.py\"; echo \"--- ports ---\"; ss -ltnp 2>/dev/null | grep -E ':9000|:8765' || true", "description": "Kill leftover server and verify"}`

  ```
aucun serveur.py
--- ports ---
LISTEN 0      5          127.0.0.1:8765       0.0.0.0:*    users:(("python3",pid=2725542,fd=3))
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/rapport-page-s-mesure.json'))\nprint('GIT:',json.dumps(d['git'],ensure_ascii=False,indent=1))\nprint('\\nTESTS:',json.dumps(d['tests_sous_module'],ensure_ascii=False,indent=1)[:30 … [55 caractères tronqués]`

  ```
GIT: {
 "parent": {
  "head": "9960b37f7d28fd77d85f0868fefa53d0ab7aa67b",
  "head_court": "9960b37f",
  "branche": "",
  "ls_tree_structures": "160000 commit 389b99f8383eb47c0cc008f5d3211c9d65d895fc\ttools/structures",
  "status_structures": ""
 },
 "sous_module": {
  "head": "389b99f8383eb47c0cc008f5d3211c9d65d895fc",
  "head_court": "389b99f",
  "branche": "master",
  "status": "",
  "dernier_commit": "389b99f8383eb47c0cc008f5d3211c9d65d895fc\t2026-11-14T09:49:39-05:00\tS — LES 11 VERDICTS HUMAINS DE /paragraphes (a004–a009) : 19/19 CANDIDATS JUGÉS, 11 ACCEPTÉS, 8 EXCLUS ; DÉCISION DU 14/11 (3B), EXCEPTION AUTORISÉE",
  "origin_master": "389b99f8383eb47c0cc008f5d3211c9d65d895fc"
 },
 "work": {
  "banque_v7": false,
  "referents": false
 },
 "mtime": {
  "phrases_generees": "2026-11-02 20:35:33",
  "validations": "2026-11-03 16:46:42",
  "paragraphes_validations": "2026-11-04 15:10:08",
  "generateur": "2026-11-04 11:41:49",
  "app_js": "2026-11-02 02:10:03",
  "paragraphes_js": "2026-11-03 17:47:50"
 },
 "sha256": {
  "phrases_generees": "43957a3b9ad2422b7897a29462086ebe36877eb0d856eda4fd26ad55b5620307",
  "validations": "ed7b0765440afc83bbc466eb7cc8b46a9e81c5fd9183ca2851c1205645
… [1576 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -3 && echo \"--- describe ---\" && git describe --tags --always 2>/dev/null; echo \"--- status count ---\"; git status --porcelain | wc -l; echo \"--- submodule ---\"; git -C tools/structures status --porcelain; git … [86 caractères tronqués]`

  ```
049343d3 SEMAINE 2 — W6 : LA CLÔTURE (5 VAGUES, 3 POSITIVES, 1 BLOQUÉE, 1 MIXTE) ; 85 PORTES LUES (81/4), CIBLAGE 9/9 ; TAG ANNOTÉ semaine-2-2026-11-20 SUR 73edb3dd
9960b37f SEMAINE 2 — W5 : LA RESTITUTION v3 SÉPARE LES CINQ RÔLES (GOLD S 144/144, 18/18, PERMUTATION 0/18) ; LE GOLD v2 NE GAGNE QU'UN CADRE (20/46, F1 0,5406, LIEU 0,60) ; --roles-v3 OPT-IN
93e046f7 SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE
--- describe ---
semaine-2-2026-11-20-1-g049343d3
--- status count ---
12
--- submodule ---
160000 commit 389b99f8383eb47c0cc008f5d3211c9d65d895fc	tools/structures
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"formes_attendues\\|occurrences_attendues\\|def resume\\|branche.*show-current\\|describe\" work/page-s-mesure/mesurer.py | head -30", "description": "Locate lines to patch"}`

  ```
409:    def resume(prefixes: tuple[str, ...]) -> dict:
422:            "formes_attendues": sum(1 for l in sous if l["type_attendu"] == "anaphore"),
423:            "occurrences_attendues": sum((l["occurrences_texte"] or 0) for l in sous
454:            "formes_attendues_corrigees": 12,
455:            "occurrences_attendues_corrigees": 14,
729:            "branche": cmd(["git", "branch", "--show-current"]),
736:            "branche": cmd(["git", "-C", "tools/structures", "branch", "--show-current"]),
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/page-s-mesure/mesurer.py", "offset": 405, "limit": 45}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/page-s-mesure/mesurer.py</path>
<type>file</type>
<content>
405:                 "occurrences_texte": OCCURRENCES.get((pid, forme), 1) if valeur_attendue is not None else None,
406:                 "source_en": par_id[pid].get("source_en", ""),
407:             })
408: 
409:     def resume(prefixes: tuple[str, ...]) -> dict:
410:         sous = [l for l in lignes if l["paragraphe"].startswith(prefixes)]
411:         c = collections.Counter(l["verdict"] for l in sous)
412:         presentes = [l for l in sous if l["observe"] is not None]
413:         manquants = [l for l in sous if l["verdict"] == "manquant"]
414:         faux = [l for l in sous if l["verdict"] == "faux"]
415:         return {
416:             "lignes": len(sous),
417:             "mappings_presents": len(presentes),
418:             "justes": c["juste"],
419:             "faux": c["faux"],
420:             "manquants": c["manquant"],
421:             "non_referents_ok": c["non_referent_ok"],
422:             "formes_attendues": sum(1 for l in sous if l["type_attendu"] == "anaphore"),
423:             "occurrences_attendues": sum((l["occurrences_texte"] or 0
… [1686 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/page-s-mesure/mesurer.py", "old_string": "            \"non_referents_ok\": c[\"non_referent_ok\"],\n            \"formes_attendues\": sum(1 for l in sous if l[\"type_attendu\"] == \"anaphore\"),\n            \"occurrences_attendues … [903 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/page-s-mesure/mesurer.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/page-s-mesure/mesurer.py", "old_string": "                if set(prefixes) <= {\"a001\", \"a002\", \"a003\"} else None),\n            \"mappings_presents_detail\": len(presentes),", "new_string": "                if set(prefixes) <= … [45 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/page-s-mesure/mesurer.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/page-s-mesure/mesurer.py", "offset": 720, "limit": 28}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/page-s-mesure/mesurer.py</path>
<type>file</type>
<content>
720:         "resume": sortie.splitlines()[-1] if sortie else "",
721:         "queue": sortie[-800:],
722:     }
723: 
724: 
725: def git_etat() -> dict:
726:     def cmd(args):
727:         return lancer(args, RACINE, 10).stdout.strip()
728: 
729:     return {
730:         "parent": {
731:             "head": cmd(["git", "rev-parse", "HEAD"]),
732:             "head_court": cmd(["git", "rev-parse", "--short", "HEAD"]),
733:             "branche": cmd(["git", "branch", "--show-current"]),
734:             "ls_tree_structures": cmd(["git", "ls-tree", "HEAD", "tools/structures"]),
735:             "status_structures": cmd(["git", "status", "--porcelain", "--", "tools/structures"]),
736:         },
737:         "sous_module": {
738:             "head": cmd(["git", "-C", "tools/structures", "rev-parse", "HEAD"]),
739:             "head_court": cmd(["git", "-C", "tools/structures", "rev-parse", "--short", "HEAD"]),
740:             "branche": cmd(["git", "-C", "tools/structures", "branch", "--show-current"]),
741:             "status": cmd(["git", "-C", "tools/structur
… [475 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/page-s-mesure/mesurer.py", "old_string": "            \"branche\": cmd([\"git\", \"branch\", \"--show-current\"]),\n            \"ls_tree_structures\": cmd([\"git\", \"ls-tree\", \"HEAD\", \"tools/structures\"]),\n            \"stat … [583 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/page-s-mesure/mesurer.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 work/page-s-mesure/mesurer.py --sortie /tmp/rapport-page-s-mesure.json 2>&1 | tail -20; echo \"--- serveur.py restants ---\"; ps -eo pid,args | grep 'serveur\\.py' | grep -v grep || echo aucun; echo  … [120 caractères tronqués]`

  ```
207 phrases · 369 candidats anciens · 359 v7
  migration exacte : 106 gardés / 41 en quarantaine · 65 cibles distinctes
  référents : 16 justes / 12 faux / 2 manquants
  contrôle négatif : H0 rejetée : 369 ≠ 359, 0/369 contre 359/359 `profondeur`, 0 contre 99 candidats à ≥3, empreintes différentes, Jaccard 0,717 ; le banc ancien et la v7 ne sont pas le même banc.
  tests : 56 · OK
  → /tmp/rapport-page-s-mesure.json
--- serveur.py restants ---
aucun
--- 9000 ---
libre
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/rapport-page-s-mesure.json'))\nr=d['referent']\nfor k in ['total_9_paragraphes','a001_a003','a004_a009']:\n    x=r[k]; print(k, {kk:x[kk] for kk in x if kk not in ('faux_detail',' … [315 caractères tronqués]`

  ```
total_9_paragraphes {'lignes': 30, 'mappings_presents': 28, 'justes': 16, 'faux': 12, 'manquants': 2, 'non_referents_ok': 0, 'formes_anaphoriques_attendues': 25, 'occurrences_texte_auditees': None}
a001_a003 {'lignes': 14, 'mappings_presents': 12, 'justes': 9, 'faux': 3, 'manquants': 2, 'non_referents_ok': 0, 'formes_anaphoriques_attendues': 12, 'occurrences_texte_auditees': 14, 'formes_attendues_corrigees': 12, 'occurrences_attendues_corrigees': 14, 'cible': {'formes': 12, 'occurrences': 14, 'justes': 14, 'faux': 0, 'manquants': 0}, 'note': '12 formes uniques (clés par paragraphe) et 14 occurrences dans le texte : `se` deux fois (a001), `sa` deux fois (a003).'}
a004_a009 {'lignes': 16, 'mappings_presents': 16, 'justes': 7, 'faux': 9, 'manquants': 0, 'non_referents_ok': 0, 'formes_anaphoriques_attendues': 13, 'occurrences_texte_auditees': None}
page.service: {
 "s_serveur_en_ecoute": false,
 "port_9000_libre": true,
 "get_8765": {
  "code": 200,
  "octets": 174051,
  "titre": "Portefeuille iA — tableau de bord"
 }
}
git parent: {
 "head": "049343d3fc41a3003d2dac8dfd41db63db7ec59d",
 "head_court": "049343d3",
 "branche": "s/v7",
 "detache": false,
 "describe": "semaine-2-2026-11-20-
… [139 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/rapport-page-s-mesure.json'))\na=d['banc_ancien']; v=d['v7']; m=d['migration']; r=d['referent']; c=d['controle_negatif']; p=d['page']\nprint('HEAD',d['head_parent_court'],'sub',d[ … [2031 caractères tronqués]`

  ```
HEAD 049343d3 sub 389b99f date 2026-11-15 12:35 EST
old 207 369 2414 0/369 {'0': 10, '1': 277, '2': 82} 0
old verdicts {'lignes': 150, 'paires_uniques': 147, 'revisions': 3, 'statuts_lignes': {'exclu': 64, 'resolu': 74, 'double_sens': 1, 'compatible': 11}, 'statuts_dernier': {'exclu': 63, 'resolu': 73, 'compatible': 11}, 'acceptes_dernier': 84, 'exclus_dernier': 63, 'notes_non_vides': 1, 'niveaux_dernier': {'0': 141, '2': 4, '3': 2}, 'contextes_non_vides': 6, 'auteurs': {'humain': 150}}
old cov {'phrases_jugees_en_entier': 74, 'phrases_partielles': 0, 'phrases_sans_verdict': 133, 'phrases_avec_au_moins_un_verdict': 74, 'candidats_juges': 147, 'candidats_total': 369, 'taux_candidats': 0.398374, 'taux_phrases_completes': 0.357488, 'detail': {'banc_7': {'phrases': 7, 'jugees': '7/7'}, 'litterature_200': {'phrases': 200, 'jugees': '67/200'}}}
v7 207 359 2308 {'0': 2, '1': 37, '2': 221, '3': 84, '4': 13, '5': 2} 99 0.275766
v7 refs {'occurrences': 371, 'formes_uniques': 29, 'avec_candidat': 294, 'sans_candidat': 77, 'phrases_avec_referent': 170, 'phrases_sans_referent': 37, 'note': 'occurrences = pronoms/possessifs comptés ; formes_uniques = types de forme ; avec_candidat = au moins un 
… [5549 caractères tronqués]
  ```

### 🤖 Assistant

The measurements are stable. Now I'll write the report.

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-page-s-mesure.md", "content": "# La page `/` de S : 369/0 contre 359/99 — la recette, et pourquoi « 0 » n'est pas « zéro verdict »\n\n> **Ligne de roadmap** : S · **Tâche** : X1 / J4 après-midi (la part du pilote) · **Dat … [26430 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-page-s-mesure.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-page-s-mesure.md", "old_string": "Les **3 révisions** sont des paires de la quarantaine jugées plusieurs fois : **44 lignes = 41\npaires + 3 révisions**. Les **41 paires** sont réparties sur **18 phrases** :", "new_string … [318 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-page-s-mesure.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log -1 --format='%h %s' && git branch --show-current; echo \"--- submodule ---\"; git -C tools/structures status --porcelain; git -C tools/structures rev-parse --short HEAD", "description": "Check current HEAD before final JSON"}`

  ```
049343d3 SEMAINE 2 — W6 : LA CLÔTURE (5 VAGUES, 3 POSITIVES, 1 BLOQUÉE, 1 MIXTE) ; 85 PORTES LUES (81/4), CIBLAGE 9/9 ; TAG ANNOTÉ semaine-2-2026-11-20 SUR 73edb3dd
s/v7
--- submodule ---
389b99f
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 work/page-s-mesure/mesurer.py 2>&1 | tail -15; echo \"--- final state ---\"; git -C tools/structures status --porcelain; ps -eo pid,args | grep 'serveur\\.py' | grep -v grep || echo \"aucun serveur.p … [126 caractères tronqués]`

  ```
207 phrases · 369 candidats anciens · 359 v7
  migration exacte : 106 gardés / 41 en quarantaine · 65 cibles distinctes
  référents : 16 justes / 12 faux / 2 manquants
  contrôle négatif : H0 rejetée : 369 ≠ 359, 0/369 contre 359/359 `profondeur`, 0 contre 99 candidats à ≥3, empreintes différentes, Jaccard 0,717 ; le banc ancien et la v7 ne sont pas le même banc.
  tests : 56 · OK
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-page-s-mesure.json
--- final state ---
aucun serveur.py
9000 libre
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\np='reports/rapport-page-s-mesure.json'\nd=json.load(open(p))\nprint('size',len(open(p,'rb').read()))\nprint('date/heure',d['date'],d['heure'])\nprint('HEAD',d['head_parent_court'],d['sous_module_court'] … [1053 caractères tronqués]`

  ```
size 61859
date/heure 2026-11-15 12:37 EST
HEAD 049343d3 389b99f s/v7
verdict len 809
old 369 0/369
v7 359 99
exact 106 41 65
exact+att 106 41 106
refs 16 12 2
service False True
tests 56 True 4.346
git status submodule ''
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain | wc -l && git status --porcelain | head -15", "description": "Check current parent modifications count"}`

  ```
26
M  docs/pilotage/en-cours.md
 M docs/produit/README.md
M  journal/2026-11-15/README.md
M  journal/2026-11-15/mesures.md
M  journal/2026-11-15/portes.md
 M journal/README.md
M  journal/THEMES.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-f71c99b5-4cd1-41cd-81b4-87e7e7c8bfeb/digest.md
 M journal/sessions/session-f71c99b5-4cd1-41cd-81b4-87e7e7c8bfeb/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"12 h 35\\|12 modifications\" reports/rapport-page-s-mesure.md", "description": "Locate time and count strings"}`

  ```
4:> 2026-11-15 12 h 35 HNE · **HEAD parent mesuré** : `049343d3` · **Sous-module
43:  12 h 35 HNE**. Le parent a bougé pendant la session (`6f862993` → `9960b37f` → `049343d3`) ;
402:**12 modifications hors périmètre** ; le sous-module, lui, est resté à `389b99f` et **propre**.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-page-s-mesure.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('2026-11-15 12 h 35 HNE','2026-11-15 12 h 37 HNE')\ns=s.replace('12 h 35 HNE**. Le parent','12 h 37  … [284 caractères tronqués]`

  ```
ok
4:> 2026-11-15 12 h 37 HNE · **HEAD parent mesuré** : `049343d3` · **Sous-module
43:  12 h 37 HNE**. Le parent a bougé pendant la session (`6f862993` → `9960b37f` → `049343d3`) ;
402:**des modifications hors périmètre** ; le sous-module, lui, est resté à `389b99f` et **propre**.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-page-s-mesure.md", "limit": 140}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-page-s-mesure.md</path>
<type>file</type>
<content>
1: # La page `/` de S : 369/0 contre 359/99 — la recette, et pourquoi « 0 » n'est pas « zéro verdict »
2: 
3: > **Ligne de roadmap** : S · **Tâche** : X1 / J4 après-midi (la part du pilote) · **Date** :
4: > 2026-11-15 12 h 37 HNE · **HEAD parent mesuré** : `049343d3` · **Sous-module
5: > `tools/structures`** : `389b99f` · **Verdict** : la page `/` sert **toujours l'ancien banc** —
6: > **369 candidats**, **0 avec `profondeur`**, **0 à ≥ 3**, distribution des `niveau` **10 / 277 /
7: > 82** — alors que la v7 dynamique donne **359 candidats**, **2 / 37 / 221 / 84 / 13 / 2** et
8: > **99 à ≥ 3**. Le **106 conservés / 41 en quarantaine** de la v2 est **reproduit à la lettre**
9: > (signature exacte), mais la signature nue ne donne que **65 cibles distinctes** : **41
10: > collisions**. Avec l'attachement, **106/41** devient injectif ; avec les espaces normalisés et
11: > l'attachement, **115/32** ; avec la cible réduite à sa tête, **117/30**. Les référents sont
12: > **28 mappings / 16 justes / 12 faux / 2 manquants**, **0 note** ; la cible **14 occurrences /
13: >
… [8011 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-page-s-mesure.md", "offset": 141, "limit": 180}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-page-s-mesure.md</path>
<type>file</type>
<content>
141: `/paragraphes` est la fenêtre v7 : **9 paragraphes**, **19 candidats**, **19 verdicts**,
142: **169/169** segments avec `profondeur`. C'est le seul endroit où l'arbre v7 est réellement
143: visible aujourd'hui.
144: 
145: ## 3. La couverture et les verdicts
146: 
147: ### 3.1 La couverture du banc ancien
148: 
149: La couverture est **partielle et datée** : **74/207** phrases complètes (35,7 %), **133** sans
150: aucun verdict (64,3 %), **147/369** candidats (39,8 %). Les 7 phrases du banc sont **7/7**
151: jugées ; les 200 phrases de littérature sont **67/200** (33,5 %). Un seul annotateur, une seule
152: journée (2026-11-03), **1 note**, **0 double-codage**, **0 test-retest**. Ce n'est pas une
153: accuracy.
154: 
155: ### 3.2 Ce que la migration fait à cette couverture
156: 
157: Sous la **signature exacte de la v2** — `(texte, type, rôle)` des segments, dans l'ordre —,
158: **106 paires** ont une correspondance v7 et **41** n'en ont pas. Mais **106 paires tombent sur
159: seulement 65 candidats v7 distincts** : **41 collisions**. Autrement dit, migrer p
… [9326 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-page-s-mesure.md", "offset": 321, "limit": 150}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-page-s-mesure.md</path>
<type>file</type>
<content>
321: | c023 | 3 | c1–c2 `resolu`, c3 `exclu` | c3 sans index |
322: | c043 | 2 | c1 `exclu`, c2 `resolu` | même index, contenu changé |
323: | c056 | 3 | c1 `exclu`, c2 `exclu`, c3 `resolu` | c2–c3 sans index |
324: | c064 | 2 | c1 `resolu`, c2 `exclu` | c2 sans index |
325: | c065 | 2 | c1 `exclu`, c2 `resolu` | même index, contenu changé |
326: 
327: La liste complète, avec l'index ancien, le nombre de candidats v7, l'attachement et le niveau
328: max, est dans le JSON (`migration.quarantaine_exacte.detail`).
329: 
330: ### 5.2 Les 5 sans index ne sont pas 5 verdicts perdus
331: 
332: Les **5 candidats sans index** sont `p006-c2`, `c023-c3`, `c056-c2`, `c056-c3`, `c064-c2`. Un
333: seul est récupérable par la signature normalisée : **`p006-c2`** a une correspondance en
334: **v7-c1** (l'index 2 n'existe plus, mais le contenu y est). Les **4 autres** n'ont aucune
335: correspondance, même normalisée. La v1 disait « 5 verdicts à risque » : c'est vrai **par
336: l'index**, pas **par le contenu**. La v2 a raison de dire que **5 sans index ≠ 41 sans
337: correspond
… [8114 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-page-s-mesure.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('deux ensemble de 41 **différents**','deux ensembles de 41 **différents**')\ns=s.replace('La signatu … [252 caractères tronqués]`

  ```
ok
344:quarantaine** — deux ensembles de 41 **différents**, ce qui prête à confusion. Avec
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '348,354p' reports/rapport-page-s-mesure.md", "description": "Check line 352"}`

  ```
### 5.4 Le contrôle par index

La migration **par index** recollerait **36/147** verdicts à un **autre contenu** (les 36
candidats « même index, contenu changé »), en plus des 5 sans index. La signature exacte n'en
recollé **aucun** (0/106), au prix des 41 quarantaines. Le contrôle est net : **l'index est
faux**, la signature est la bonne clé — à condition d'y mettre l'attachement.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-page-s-mesure.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('La signature exacte n\\'en\\nrecollé **aucun**','La signature exacte n\\'en\\nrecolle **aucun**')\n … [145 caractères tronqués]`

  ```
ok
La migration **par index** recollerait **36/147** verdicts à un **autre contenu** (les 36
candidats « même index, contenu changé »), en plus des 5 sans index. La signature exacte n'en
recolle **aucun** (0/106), au prix des 41 quarantaines. Le contrôle est net : **l'index est
faux**, la signature est la bonne clé — à condition d'y mettre l'attachement.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/rapport-page-s-mesure.json > /dev/null && echo \"JSON valide\"; python3 - <<'PY'\nimport re, pathlib\np=pathlib.Path('reports/rapport-page-s-mesure.md')\ns=p.read_text(encoding='utf-8')\nliens=re.findall( … [254 caractères tronqués]`

  ```
JSON valide
OK  rapport-coordination-s-v2.md
OK  rapport-page-s-mesure.json
OK  ../work/page-s-mesure/mesurer.py
OK  rapport-etat-s.md
OK  rapport-coordination-s-v2.md
OK  rapport-etat-s.md
OK  rapport-s-traductions.md
OK  rapport-s-paragraphes.md
OK  ../docs/pilotage/semaine-2.md
OK  ../work/page-s-mesure/mesurer.py
OK  rapport-page-s-mesure.json
OK  ../tools/structures/generateur.py
OK  ../tools/structures/mesure_arbre.py
OK  ../tools/structures/static/app.js
OK  ../tools/structures/static/paragraphes.js
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/revue_documentation.py", "description": "Inspect documentation review tool"}`

  ```
#!/usr/bin/env python3
"""revue_documentation.py — LA REVUE DE FIN DE SOUS-CHANTIER (AGENTS.md §4).

Ce qu'elle vérifie, et qu'il faut corriger AVANT le commit de clôture :
  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
  2. structure  : les sept chantiers de en-cours.md ont leur entrée, leur état et leur fiche ;
  3. annotation : les liens relatifs des docs/ et reports/ résolvent, et leur libellé ne
     ment pas sur la cible ; les sources externes sont citées ;
  4. fraîcheur  : en-cours.md date du dernier commit, ET aucun fait n'a été commité après
     le dernier état (comparaison de commits, pas de dates : voir verifie_etat_a_jour.py) ;
  5. cohérence  : la synthèse (index.md) liste les huit chapitres, le chapitre 7 et B10–B12 ;
     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
  6. vocabulaire : « jeton » ne désigne **jamais** la représentation sémantique neutre (RSN) ;
  7. navigation : aucun document vivant n'est orphelin, et aucun chemin en code inline
     ne pointe vers un fichier absent (hors gabarits `AAAA`, `<...>`, `*`).

Sortie : un rapport lisible, code 0 si tout passe, 1 sinon (u
… [1781 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 python3 tools/revue_documentation.py 2>&1 | tail -60; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run documentation review"}`

  ```
revue de documentation · 755 fiche(s) · 848 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 754 fichiers, le disque en a 755
     · compteurs : en-cours.md dit 847 JSON, le disque en a 848
exit=1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"754\\|847\\|fichiers\\|JSON\" docs/pilotage/en-cours.md | head -30; echo \"--- mtime ---\"; stat -c '%y' docs/pilotage/en-cours.md; echo \"--- git diff stat ---\"; git diff --stat docs/pilotage/en-cours.md", "description":  … [28 caractères tronqués]`

  ```
66:- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144** (cinq **18/18**), gold v2 **20/46** (F1 **0,5406**), permutation **0/18** ; `--roles-v3` opt-in ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/rapport-semaine-2.md) + [JSON](../../reports/rapport-semaine-2.json) ; tag annoté `semaine-2-2026-11-20` sur `73edb3dd` ; **85** portes lues (**81** vertes, **4** rouges nommées).
105:| fichiers / JSON de résultats | **754** / **847** | `reports/*.md` / `reports/*.json` |
--- mtime ---
2026-11-15 12:35:40.349951984 -0500
--- git diff stat ---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\ns=p.read_text(encoding='utf-8')\nold='| fichiers / JSON de résultats | **754** / **847** |'\nnew='| fichiers / JSON de résultats | **755** / **848** |'\ … [206 caractères tronqués]`

  ```
ok
105:| fichiers / JSON de résultats | **755** / **848** | `reports/*.md` / `reports/*.json` |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 python3 tools/revue_documentation.py 2>&1 | tail -30; echo \"exit=${PIPESTATUS[0]}\"", "description": "Re-run documentation review"}`

  ```
revue de documentation · 755 fiche(s) · 848 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo \"exit=${PIPESTATUS[0]}\"", "description": "Verify en-cours state file"}`

  ```
en-cours · 1622 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
exit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -20; echo \"exit=${PIPESTATUS[0]}\"", "description": "Check document sizes"}`

  ```
3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2663    229   T1   2800  reports/README.md
    2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3992 mots (budget 4 000)

  avertissements :
     · 61 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-p
… [142 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- docs/pilotage/en-cours.md; echo \"--- staged ---\"; git diff --cached --stat -- docs/pilotage/en-cours.md", "description": "Check en-cours diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index be629f05..9d6c13ce 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -102,7 +102,7 @@
 |---|---|---|
 | portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
 | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
-| fichiers / JSON de résultats | **754** / **847** | `reports/*.md` / `reports/*.json` |
+| fichiers / JSON de résultats | **755** / **848** | `reports/*.md` / `reports/*.json` |
 | documents de `docs/` | **124** (hors archive et README) | `docs/**/*.md` |
 | dernière passe | **15/11 09 h 53 → 12 h 15** (85, **81/4**) ; rouges `indice`, `melange` (structurelles), `sessions` (**réparée** à 12 h 20), `prechargement` (**environnementale**) ; ciblage W6 **9/9** | `work/portes-1115-09h53/registre.txt` ; `work/portes/w6-final/` |
 
--- staged ---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain | head -40; echo \"count\"; git status --porcelain | wc -l; echo \"HEAD\"; git log -1 --format='%h %s'", "description": "Check current git status"}`

  ```
M docs/pilotage/en-cours.md
 M docs/produit/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? reports/rapport-page-s-mesure.json
?? reports/rapport-page-s-mesure.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
count
15
HEAD
2b5bd1cd JOURNAL — RÉGÉNÉRÉ APRÈS LA CLÔTURE DE LA SEMAINE 2 (W1-W6) ; LE TAG semaine-2-2026-11-20 REPOSÉ SUR LE COMMIT W5
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log -1 --format='%h %cI %s'; git branch --show-current; git ls-tree HEAD tools/structures; git -C tools/structures status --porcelain; git -C tools/structures rev-parse --short HEAD", "description": "Check final parent HEAD and s … [10 caractères tronqués]`

  ```
2b5bd1cd 2026-11-15T12:35:40-05:00 JOURNAL — RÉGÉNÉRÉ APRÈS LA CLÔTURE DE LA SEMAINE 2 (W1-W6) ; LE TAG semaine-2-2026-11-20 REPOSÉ SUR LE COMMIT W5
s/v7
160000 commit 389b99f8383eb47c0cc008f5d3211c9d65d895fc	tools/structures
389b99f
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 python3 tools/revue_documentation.py 2>&1 | tail -30; echo \"exit=${PIPESTATUS[0]}\"", "description": "Re-run doc review after parent commit"}`

  ```
revue de documentation · 755 fiche(s) · 848 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain -- tools/structures; echo \"submodule status above (empty=clean)\"; git -C tools/structures status --porcelain; echo \"--- our files ---\"; ls -l reports/rapport-page-s-mesure.md reports/rapport-page-s-mesure.j … [178 caractères tronqués]`

  ```
submodule status above (empty=clean)
--- our files ---
-rw-r--r--. 1 stephane stephane 61859 15 nov 12:37 reports/rapport-page-s-mesure.json
-rw-------. 1 stephane stephane 26916 15 nov 12:37 reports/rapport-page-s-mesure.md
-rw-------. 1 stephane stephane 53944 15 nov 12:35 work/page-s-mesure/mesurer.py
--- parent diff stat ---
 docs/pilotage/en-cours.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && chmod 644 reports/rapport-page-s-mesure.md work/page-s-mesure/mesurer.py && ls -l reports/rapport-page-s-mesure.md reports/rapport-page-s-mesure.json work/page-s-mesure/mesurer.py", "description": "Normalize file permissions"}`

  ```
-rw-r--r--. 1 stephane stephane 61859 15 nov 12:37 reports/rapport-page-s-mesure.json
-rw-r--r--. 1 stephane stephane 26916 15 nov 12:37 reports/rapport-page-s-mesure.md
-rw-r--r--. 1 stephane stephane 53944 15 nov 12:35 work/page-s-mesure/mesurer.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-page-s-mesure.md')\ns=p.read_text(encoding='utf-8')\nold=(\"**106 paires** ont une correspondance v7 et **41** n'en ont pas. Mais **106 paires tombent sur\\n\"\n     … [1018 caractères tronqués]`

  ```
ok
### 3.2 Ce que la migration fait à cette couverture

Sous la **signature exacte de la v2** — `(texte, type, rôle)` des segments, dans l'ordre —,
**106 paires** ont une correspondance v7 et **41** n'en ont pas. Mais **106 paires tombent sur
seulement 65 candidats v7 distincts** : **41 collisions**. Autrement dit, cette signature ne
peut pas attacher **106 verdicts distincts** : **41 se disputent les mêmes 65 candidats**, et
une table indexée par candidat en perdrait 41. L'attachement (segment + cible) sépare ces
variantes : on garde **106/41** et on obtient **106 cibles distinctes**.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && find . -name '__pycache__' -newermt '2026-11-15 12:20' -print 2>/dev/null | head; echo \"--- pycache mtimes ---\"; find . -name '*.pyc' -newermt '2026-11-15 12:20' -printf '%TY-%Tm-%Td %TH:%TM %p\\n' 2>/dev/null | he … [57 caractères tronqués]`

  ```
--- pycache mtimes ---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-page-s-mesure.md')\ns=p.read_text(encoding='utf-8')\nold=(\"`donnees/paragraphes-validations.jsonl` : **19 lignes**, **9 paragraphes**, **19/19 candidats**,\\n\"\n   … [1195 caractères tronqués]`

  ```
ok

### 4.1 Ce que le journal contient

`donnees/paragraphes-validations.jsonl` : **19 lignes**, **9 paragraphes**, **19/19 candidats**,
**11 acceptés / 8 exclus**, **0 note**, `auteur: humain`, mtime **2026-11-04 15:10:08**, SHA-256
`a3c54c9c…`. Ces 19 verdicts sont **committés** à `389b99f` ; ils ne sont **pas** dans le lot
des 41, qui sont des verdicts de la banque `/` (`validations.jsonl`). Les 19 verdicts portent **28 mappings uniques** (les mêmes valeurs sont répétées
d'un candidat à l'autre), comparés à la source anglaise et à la table de l'audit
[`rapport-etat-s.md`](rapport-etat-s.md) § 2 :

---

### 5.1 Le compte exact

Sous la signature de la v2, **106 paires** ont une correspondance v7 et **41** n'en ont pas.
Ces 41 sont des verdicts de la **banque `/`** (`validations.jsonl`), pas les 19 verdicts de
`/paragraphes` :

| mesure | valeur |
|---|---:|
| paires uniques | **147** |
| conservées (signature exacte) | **106** |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 python3 tools/revue_documentation.py 2>&1 | tail -12; echo \"exit=${PIPESTATUS[0]}\"", "description": "Re-run doc review after edits"}`

  ```
revue de documentation · 755 fiche(s) · 848 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-page-s-mesure.md')\ns=p.read_text(encoding='utf-8')\nold=(\"La migration **par index** recollerait **36/147** verdicts à un **autre contenu** (les 36\\n\"\n     \"ca … [656 caractères tronqués]`

  ```
ok

La migration **par index** recollerait **36/147** verdicts à un **autre contenu** (les 36
candidats « même index, contenu changé ») ; les **5 sans index** n'auraient plus de cible. La
signature exacte n'en recolle **aucun** (0/106), au prix des 41 quarantaines. Le contrôle est net : **l'index est
faux**, la signature est la bonne clé — à condition d'y mettre l'attachement.

## 6. Le contrôle négatif : les deux bancs diffèrent
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-page-s-mesure.md')\ns=p.read_text(encoding='utf-8')\nold=(\"**4/9** à être fautifs (a005, a006, a008, a009). Corriger seulement les 12 formes de a001–a003\\n\"\n     … [873 caractères tronqués]`

  ```
ok
| cible corrigée | **12/12 justes, 14/14 occurrences, 0 faux, 0 manquant** |

La cible **14/12** est donc bien définie — mais elle **ne couvre que a001–a003**. Les
**a004–a009** portent **16 mappings**, **7 justes**, **9 faux**, **0 manquant** ; ils sont
**4/9** à être fautifs (a005, a006, a008, a009). Corriger seulement les 12 formes de a001–a003
laisse donc **9 faux** dans les six autres paragraphes. Pour atteindre le **0/9 fautif** de
l'action A2, il faut aussi corriger ces 9 ; la cible 14/12 ne suffit pas. Autrement dit, la
cible **14/12** et la mesure **0/9** ne portent pas sur le même périmètre : 14/12 = a001–a003 ;
0/9 = les neuf paragraphes, donc **9 faux de plus** à corriger.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/rapport-s-referents* 2>/dev/null || echo \"aucun rapport-s-referents\"; ls work/referents 2>/dev/null || echo \"aucun work/referents\"; find work -maxdepth 2 -iname '*referent*' -o -iname '*banque-v7*' 2>/dev/null | head", … [61 caractères tronqués]`

  ```
aucun rapport-s-referents
aucun work/referents
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/*migration* reports/*banque-v7* 2>/dev/null || echo \"aucun\"; grep -rln \"106 conservés\\|106/41\\|quarantaine\" reports/*.md | tail -10", "description": "Search for S migration report"}`

  ```
aucun
reports/inventaire-donnees-entrainement.md
reports/rapport-coordination-s-v2.md
reports/rapport-page-s-mesure.md
reports/rapport-semaine-2.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== submodule ===\"; git -C tools/structures status --porcelain; git -C tools/structures rev-parse --short HEAD; echo \"=== parent tools/structures ===\"; git status --porcelain -- tools/structures; echo \"=== our files ===\"; … [240 caractères tronqués]`

  ```
=== submodule ===
389b99f
=== parent tools/structures ===
=== our files ===
 M docs/pilotage/en-cours.md
?? reports/rapport-page-s-mesure.json
?? reports/rapport-page-s-mesure.md
=== HEAD ===
2b5bd1cd JOURNAL — RÉGÉNÉRÉ APRÈS LA CLÔTURE DE LA SEMAINE 2 (W1-W6) ; LE TAG semaine-2-2026-11-20 REPOSÉ SUR LE COMMIT W5
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"work\" .gitignore; git check-ignore -v work/page-s-mesure/mesurer.py || echo \"non ignoré\"", "description": "Check if work dir is ignored"}`

  ```
23:work/
.gitignore:23:work/	work/page-s-mesure/mesurer.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-page-s-mesure.md')\ns=p.read_text(encoding='utf-8')\nold=(\"  **référents** et fournit le **contrôle négatif** qui sépare les deux bancs. Le JSON est\\n\"\n     \"   … [1211 caractères tronqués]`

  ```
ok
- **Est** : la **recette indépendante** de la page `/` de S, en **lecture seule**. Elle rejoue la
  mesure de la v7, vérifie les chiffres de [`rapport-coordination-s-v2.md`](rapport-coordination-s-v2.md),
  liste les **41 paires en quarantaine**, mesure le **106** en cibles distinctes, audite les
  **référents** et fournit le **contrôle négatif** qui sépare les deux bancs. Le JSON archivé est
  [`rapport-page-s-mesure.json`](rapport-page-s-mesure.json) ; le harnais **local** qui l'a produit
  est [`work/page-s-mesure/mesurer.py`](../work/page-s-mesure/mesurer.py) (`work/` est ignoré par
  git ; le JSON, lui, est dans `reports/`).
- **N'est pas** : une migration, un patch, un commit de S, ni une correction des référents. Le
---
- [rapport-s-traductions.md](rapport-s-traductions.md) — les 14 occurrences / 12 formes de
  a001–a003 et la source anglaise.
- [rapport-s-paragraphes.md](rapport-s-paragraphes.md) — les neuf paragraphes d'Alice.
- [semaine-2.md](../docs/pilotage/semaine-2.md) — la ligne J4, les 106/41 et le 369/0.
- [mesurer.py](../work/page-s-mesure/mesurer.py) — le harnais **local** (ignoré par git) qui a
  produit le JSON ; la mesure se rejoue avec `PYTHONDONTWRITEBYTE
… [220 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 python3 tools/revue_documentation.py 2>&1 | tail -8; echo \"exit=${PIPESTATUS[0]}\"", "description": "Final doc review"}`

  ```
revue de documentation · 755 fiche(s) · 848 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-page-s-mesure.md')\ns=p.read_text(encoding='utf-8')\nold=(\"Le parent a bougé **pendant** la session (`6f862993` → `9960b37f` → `049343d3`), et il porte\\n\"\n     \ … [642 caractères tronqués]`

  ```
ok
| `work/referents/` | **absent** |
| écritures dans `tools/structures/` | **aucune** |
| HEAD parent à la mesure | `049343d3` (branche `s/v7`, `describe` `semaine-2-2026-11-20-1-g049343d3`) |

Le parent a bougé **pendant** la session (`6f862993` → `9960b37f` → `049343d3`), puis
**après** la mesure (`2b5bd1cd`, journal régénéré) ; il porte **des modifications hors
périmètre**. Le sous-module, lui, est resté à `389b99f` et **propre**, et le pointeur du parent
est toujours `389b99f`.
Un premier lancement manuel du serveur sur **9000** a laissé un processus (pid **602059**) : il
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 python3 tools/revue_documentation.py 2>&1 | tail -6; echo \"exit=${PIPESTATUS[0]}\"; python3 -m json.tool reports/rapport-page-s-mesure.json > /dev/null && echo \"JSON valide\"", "description": "Final review and JSON vali … [8 caractères tronqués]`

  ```
revue de documentation · 755 fiche(s) · 848 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
JSON valide
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-page-s-mesure.md')\ns=p.read_text(encoding='utf-8')\nold=(\"Sous **exact + attachement**, la couverture v7 est **56 phrases complètes / 0 partielle / 151\\n\"\n      … [949 caractères tronqués]`

  ```
ok
   chiffre dépend de la convention, et la fiche doit le dire.

Sous **exact + attachement**, la couverture v7 est **56 phrases complètes / 0 partielle / 151
sans verdict** ; les 74 phrases complètes de l'ancien banc se répartissent en **56 conservées**
et **18 perdues en entier** (dans ces données, les 18 sont perdues en bloc, pas en partie).
Sous **normalisé + attachement**, **59 complètes + 4 partielles + 144 sans verdict**.
  ```

### 🤖 Assistant

Fait. Fichiers écrits :

- [`reports/rapport-page-s-mesure.md`](reports/rapport-page-s-mesure.md)
- [`reports/rapport-page-s-mesure.json`](reports/rapport-page-s-mesure.json)
- harnais local : `work/page-s-mesure/mesurer.py` (`work/` est ignoré par git)

**Ce que la mesure dit**

- **`/` sert toujours l'ancien banc** : **369 candidats**, **0/369** avec `profondeur`, **0** à ≥ 3, distribution **10/277/82**. La v7 dynamique donne **359 candidats**, **2/37/221/84/13/2**, **99** à ≥ 3.
- **Correction de lecture importante** : « 369/0 » et « 359/99 » ne sont **pas** des comptes de verdicts. `/` porte **150 verdicts / 147 paires** (74/207 phrases complètes, 147/369 candidats jugés) ; la v7 n'a **aucun verdict natif**. **0** et **99** sont des candidats à profondeur ≥ 3, pas des verdicts.
- **106/41 reproduit à la lettre** sous la signature exacte de la v2, mais **106 paires tombent sur 65 candidats distincts** : **41 collisions**. Avec l'attachement : **106/41, 106 cibles, 0 collision**. Espaces normalisés + attachement : **115/32** ; cible réduite à sa tête : **117/30**. Le **41 n'est donc pas un invariant**.
- **Référents** : **28 mappings, 16 justes, 12 faux, 2 manquants, 0 note** ; **6/9** paragraphes fautifs. La cible **14 occurrences / 12 formes** ne couvre que **a001–a003** (9/12 justes, 3 faux, 2 manquants). Les **a004–a009** gardent **9 faux** : la cible 14/12 ne suffit pas pour le « 0/9 » d'A2. La v2 écrit « 9/16 faux » : c'est une transposition, les données disent **16/28 justes / 12 faux**.
- **S n'a rien intégré** : `work/banque-v7/` et `work/referents/` absents ; `phrases_generees.json` du **02/11** ; `/api/phrases` rend **0/369** `profondeur`.

**Contrôle négatif** : H0 « les deux bancs sont le même » est rejetée — **369 ≠ 359**, **0/369** contre **359/359** `profondeur`, **0** contre **99** à ≥ 3, empreintes SHA-256 différentes, Jaccard **0,7170** (multiset) et **0,7391** (global), migration **106/147** au lieu de 147/147. Contrôle positif : chaque banc comparé à lui-même est identique. **304 identiques / 55 changés / 10 orphelins** ; l'index recollerait **36/147** verdicts au mauvais contenu.

**Intégrité** : **56/56 tests OK** en **4,3 s**, sous-module `389b99f` **propre**, **8765 intact** (`financemeteo`), **9000 libre**, aucune écriture dans `tools/structures/`. Le parent a bougé pendant la session ; HEAD mesuré **`049343d3`** (puis `2b5bd1cd` après la mesure). Seuls les deux compteurs de `docs/pilotage/en-cours.md` ont été ajustés pour la revue de documentation (755/848), qui passe. Fichiers **non committés**.

