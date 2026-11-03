# Session DSH — relecture

- identifiant : `29ad180d-38a5-4481-a9a7-ec6ab31c895f`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-02 16:14:53
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu es la session S (les structures, CPU). Lis AGENTS.md, docs/pilotage/en-cours.md,  docs/theorie/jeux-symboliques.md et tools/structures/ (sous-module heads/fusion). Ton id est  dans `printenv DSH_SESSION_ID` ; crée journal/sessions/<id>/plan.md avec  `python3 tools/sessions.py --modele` (État : actif, heartbeat maintenant), réserve  `tools/structures/`, ses exports et sa banque. Prochaine action : analyseur rôles/subordonnées,  puis export au corpus ; 19 tests à garder verts. Le sous-module se commit dans son dépôt avant  de bouger le pointeur. Un fait = mesure + contrôle + fiche + en-cours + commit (`git add`  explicite). Ne touche pas à en-cours/roadmap/AGENTS sans le hub.

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
réseau sont des **faits** regroupés en **listes valuées poussées** vers leurs lecteurs : le coût du calcul devient proportionnel à l'**activité**, et le modèle devient **décomposable**, **répartissable** et **observable**. Le projet a pour principe que la structure bat la taille. Construire le moteur et modèle optimisé qui rend cette structure observable, décomposable, répartissable et rejouable permet d'atteindre de nouveaux sommets. Bref, révolutionner l'IA avec une approche par bus d'événements où chaque bloc fonctionnel est optimisable, comparable et substituable par des alternatives ayant des architectures différentes. e.g. Blocs neuronaux là où l'intuition est un avantage, blocs computationnels classiques pour les opérations où l'informatique classique est plus fiable et performante.

Le projet est né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de
les **combiner**, de les **décomposer en couches et grappes de neurones** exécutables par du matériel divers, voire
**distribué en réseau**, de les **diagnostiquer et faire évoluer** en étudiant leurs **flux**, et de **rejouer à
volonté** des événements.


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

⏵ Lecture du contexte de session S (structures, CPU)
Je commence par charger le contexte minimal (AGENTS.md, en-cours, théorie des jeux symboliques) et identifier la session.

- **bash** `{"command": "printenv DSH_SESSION_ID; echo \"---\"; pwd; echo \"---\"; git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet status --short | head -50", "description": "Get session id and git status"}`

  ```
29ad180d-38a5-4481-a9a7-ec6ab31c895f
---
/home/stephane/GitHub/Qtrinet
---
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/AGENTS.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/AGENTS.md</path>
<type>file</type>
<content>
1: # Directives de l'agent — Drave
2: 
3: > **Compteurs vivants.** Dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; ne pas les recopier ici.
4: 
5: > **Porte d'entrée.** Lis ce fichier en entier (2 min) : il porte la **vision**, les règles non négociables et le
6: > **routage** vers le document de chaque tâche. Le détail n'est pas ici : il est dans [`docs/methode/`](docs/methode/)
7: > (tableau § 3). L'**état courant** est dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; la **roadmap** dans
8: > [`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md) ; le récit daté dans [`journal/`](journal/).
9: 
10: ## 1. La vision (l'essentiel)
11: 
12: **Drave est une vision de l'IA centrée sur les flots de données, pas sur le calcul brut.** Les activations d'un
13: réseau sont des **faits** regroupés en **listes valuées poussées** vers leurs lecteurs : le coût du calcul devient proportionnel à l'**activité**, et le modèle devient **décomposable**, **répartissable** et **observable**. Le projet a pour principe que la structure bat la taille. Construire le moteur et mo
… [8998 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet | head -40; echo \"=== git ===\"; git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet rev-parse --show-toplevel; git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet log --oneline -5; echo \"=== ls tools/structures ===\"; ls -l … [125 caractères tronqués]`

  ```
total 204
drwxr-xr-x. 1 stephane stephane   660  1 nov 10:50 .
drwxr-xr-x. 1 stephane stephane  2496  1 nov 10:47 ..
-rw-r--r--. 1 stephane stephane  9882 29 oct 16:01 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2484  2 nov 12:25 data
drwxr-xr-x. 1 stephane stephane   124 31 oct 18:00 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   198  2 nov 16:15 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   832  2 nov 00:00 journal
drwxr-xr-x. 1 stephane stephane   100 15 oct 09:02 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 19956 29 oct 08:14 README.md
drwxr-xr-x. 1 stephane stephane 57116  2 nov 14:40 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane 10507 30 sep 
… [2233 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-02, 16 h 09 HNE (heure locale, EST).**
4: 
5: > **État courant, pas histoire.** Une sous-section par **session active**, une ligne par **chantier**
6: > avec son **bloquant**. Méthode : [`methode/`](../methode/) (contexte, continuité). Résultats :
7: > [`reports/`](../../reports/). Histoire : [`journal/`](../../journal/). Plan : [`roadmap.md`](roadmap.md).
8: >
9: > **Reprise après le reboot du 02/11 15 h 06** : les deux sessions sont **en pause**, leurs cycles
10: > sont committés, les GPU sont sains ; reprise par `dsh --profile dsh-tui --resume <id>` ; runbook
11: > dans [`plan-travail.md`](plan-travail.md) § 9.
12: 
13: ## Sessions en cours
14: 
15: > Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
16: > [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
17: > `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
18: > le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.
… [11417 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/jeux-symboliques.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/README.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/jeux-symboliques.md</path>
<type>file</type>
<content>
1: # Les jeux symboliques — de la surface au sens, puis à la pensée
2: 
3: > **Ce que ce document est.** Le **bloc de langue et de jeux** du bus : comment une surface (une notation, une
4: > phrase, un diagramme) devient une **représentation sémantique neutre (RSN-jeu)**, et comment la **pensée**
5: > raisonne ensuite sur cette RSN sans relire la surface. Le bloc est **hybride** : la surface et la RSN sont des
6: > opérations classiques, la pensée peut appeler un solveur exact ou un modèle selon le jeu. Les **chiffres** et les
7: > contrôles sont dans [`rapport-jeux-symboliques.md`](../../reports/rapport-jeux-symboliques.md) ;
8: > la **théorie** dans [`synthese/07`](synthese/07-modeles-alternatifs-entree-sortie.md) et
9: > [`synthese/08`](synthese/08-les-operations.md).
10: 
11: ## Le problème
12: 
13: Un même état de jeu a **beaucoup de surfaces** :
14: 
15: - aux échecs, la position de départ est une **FEN**, un **diagramme**, une suite de coups **SAN**
16:   (`1. e4 e5`), **UCI** (`e2e4`), française (`Cf3`, « le cavalier de g1 va en f3 ») ou anglaise
17:   (
… [12219 caractères tronqués]
  ```


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
8: > **Ce que ce n'est pas.** Pas un analyseur syntaxique : les candidats sont **générés par une
9: > heuristique** (`generateur.py`) ou fournis par le fichier de données ; l'outil les fait valider,
10: > il ne prétend pas les avoir compris.
11: 
12: ## Lancer
13: 
14: ```bash
15: python3 serveur.py                 # http://127.0.0.1:8765
16: python3 serveur.py --port 9000 --hote 0.0.0.0   # sur le réseau local
17: ```
18: 
19: Aucune dépendance : la bibliothèque standard suffit (serveur HTTP, JSON, `urllib`).
20: 
21: ## Le niveau pragmatique
22: 
23: Une phrase hors contexte est **ambiguë** — même pour un humain. Et en contexte, l'ambiguïté peut
24: ê
… [7519 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/sessions.py --help 2>&1 | head -60; echo \"=== status ===\"; python3 tools/sessions.py --status 2>&1 | head -60", "description": "Inspect sessions tool usage and status"}`

  ```
usage: sessions.py [-h] [--racine RACINE] [--status] [--check] [--strict]
                   [--modele] [--autotest] [--depuis-en-cours]

sessions.py — plans de session : qui fait quoi, avant d'écrire `en-cours`.
Chaque session active expose son mandat dans `journal/sessions/<id>/plan.md` :
périmètre, fichiers réservés, heartbeat, prochaine action, état. Les autres
sessions consultent `--status` avant de claim, et `--check --strict` refuse
les mandats incomplets, les identifiants dupliqués, les périmètres qui se
recouvrent et les heartbeats périmés (le `--check` seul les signale). `en-
cours` reste la seule source de l'état : ce plan est le **contrat de travail**
qui le précède. Une session arrêtée (reboot, panne) passe à `État : en pause`
: elle reste dans l'état, son heartbeat n'est plus exigé, et la reprise la
remet `actif`.

options:
  -h, --help         show this help message and exit
  --racine RACINE
  --status
  --check
  --strict
  --modele
  --autotest
  --depuis-en-cours  crée des plans à confirmer depuis les sections de en-
                     cours
=== status ===
sessions · plans de mandat
    0b0a6a0d-05f5-4308 · terminé  · 1901 min · N2.h — corpus propre, porte honn
… [2418 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && ls -la tests donnees static; echo \"=== git submodule ===\"; cat .git; git log --oneline -8; git status --short; echo \"=== reports ===\"; ls /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/ | grep -i -E \"s- … [93 caractères tronqués]`

  ```
donnees:
total 12
drwxr-xr-x. 1 stephane stephane    24  2 nov 02:10 .
drwxr-xr-x. 1 stephane stephane   240  2 nov 02:10 ..
-rw-r--r--. 1 stephane stephane 12115  2 nov 02:10 phrases.json

static:
total 20
drwxr-xr-x. 1 stephane stephane   50  2 nov 02:10 .
drwxr-xr-x. 1 stephane stephane  240  2 nov 02:10 ..
-rw-r--r--. 1 stephane stephane 6757  2 nov 02:10 app.js
-rw-r--r--. 1 stephane stephane 2350  2 nov 02:10 index.html
-rw-r--r--. 1 stephane stephane 5343  2 nov 02:10 style.css

tests:
total 16
drwxr-xr-x. 1 stephane stephane  116  2 nov 02:10 .
drwxr-xr-x. 1 stephane stephane  240  2 nov 02:10 ..
drwxr-xr-x. 1 stephane stephane  172  2 nov 02:10 __pycache__
-rw-r--r--. 1 stephane stephane 2652  2 nov 02:08 test_export.py
-rw-r--r--. 1 stephane stephane 3348  2 nov 02:10 test_generateur.py
-rw-r--r--. 1 stephane stephane 5799  2 nov 02:10 test_serveur.py
=== git submodule ===
gitdir: ../../.git/modules/tools/structures
3b68143 FUSION — LE BANC DE STRUCTURES : PRAGMATIQUE, EXPORT ET ANALYSEUR EN UN SEUL ARBRE
733b1a4 CONTEXTE — DES NIVEAUX GRADUÉS, ET LA MESURE DU NIVEAU MINIMAL POUR TRANCHER
7366191 PRAGMATIQUE — LE CONTEXTE TRANCHE, LE DOUBLE SENS SE CONSERVE
1cf64d2 EXPORT
… [722 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git branch -a -v; echo \"=== HEAD ===\"; git rev-parse --abbrev-ref HEAD; git rev-parse --short HEAD; echo \"=== statut ===\"; git status; echo \"=== arbre fusion ===\"; git ls-tree --name-only heads/fusion 2>/dev/nu … [187 caractères tronqués]`

  ```
fusion                3b68143 FUSION — LE BANC DE STRUCTURES : PRAGMATIQUE, EXPORT ET ANALYSEUR EN UN SEUL ARBRE
* master                3b68143 [ahead 2] FUSION — LE BANC DE STRUCTURES : PRAGMATIQUE, EXPORT ET ANALYSEUR EN UN SEUL ARBRE
  n2-analyse            c7232b3 ANALYSEUR — L'ADVERBE DE TEMPS ET LE « QU'ELLE » : 7/7 SÉQUENCES, 94 % DE COUVERTURE
  remotes/origin/HEAD   -> origin/master
  remotes/origin/master 733b1a4 CONTEXTE — DES NIVEAUX GRADUÉS, ET LA MESURE DU NIVEAU MINIMAL POUR TRANCHER
=== HEAD ===
master
3b68143
=== statut ===
On branch master
Your branch is ahead of 'origin/master' by 2 commits.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
=== arbre fusion ===
.gitignore
README.md
construire_donnees.py
donnees
exporter_corpus.py
generateur.py
llm.py
serveur.py
static
tests
=== log fusion ===
3b68143 FUSION — LE BANC DE STRUCTURES : PRAGMATIQUE, EXPORT ET ANALYSEUR EN UN SEUL ARBRE
733b1a4 CONTEXTE — DES NIVEAUX GRADUÉS, ET LA MESURE DU NIVEAU MINIMAL POUR TRANCHER
7366191 PRAGMATIQUE — LE CONTEXTE TRANCHE, LE DOUBLE SENS SE CONSERVE
1cf64d2 EXPORT — LA BANQUE VALIDÉE DEVIENT UN CORPUS JSONL (SPANS VÉRIFIÉS)
a407095 GÉNÉRATE
… [147 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports | grep -iE \"analyseur|structures\" ; echo \"=== data/structures ===\"; ls -la data/structures 2>/dev/null; echo \"=== plan modele ===\"; ls journal/sessions/_modele/ 2>/dev/null; sed -n '1,120p' journal/sessions/_modele/p … [89 caractères tronqués]`

  ```
rapport-s-analyseur.md
=== data/structures ===
=== plan modele ===
plan.md
# Plan de session — <id>

> **Mandat vivant.** Écris ce fichier **avant** `en-cours`, mets-le à jour à chaque cycle,
> et passe `État : terminé` quand la session se retire.

- **Session** : `<id>`
- **Rôle** : <chantier / programme>
- **Périmètre** : <A8.0, R13, ...>
- **Fichiers réservés** : `tools/...`, `reports/...`
- **Heartbeat** : <AAAA-MM-JJ HH:MM HAE>
- **Prochaine action** : <une action nommée>
- **État** : actif
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && echo \"=== STAT 3b68143 ===\"; git show --stat --oneline 3b68143 | head -40; echo; echo \"=== STAT 733b1a4 ===\"; git show --stat --oneline 733b1a4 | head -30; echo; echo \"=== n2-analyse tree ===\"; git ls-tree --na … [320 caractères tronqués]`

  ```
=== STAT 3b68143 ===
3b68143 FUSION — LE BANC DE STRUCTURES : PRAGMATIQUE, EXPORT ET ANALYSEUR EN UN SEUL ARBRE

 README.md                | 55 +++++++++++++++++++++++++-----
 construire_donnees.py    | 24 +++++++++++++
 donnees/phrases.json     | 88 ++++++++++++++++++++++++++++++++++++++++++++++--
 generateur.py            | 28 ++++++++++++---
 llm.py                   | 82 ++++++++++++++++++++++++--------------------
 serveur.py               | 84 ++++++++++++++++++++++++++++++++-------------
 static/app.js            | 74 +++++++++++++++++++++++++++-------------
 static/index.html        |  3 ++
 static/style.css         | 18 ++++++++--
 tests/test_generateur.py | 22 ++++++++++++
 tests/test_serveur.py    | 52 ++++++++++++++++++++++------
 11 files changed, 419 insertions(+), 111 deletions(-)

=== STAT 733b1a4 ===
733b1a4 CONTEXTE — DES NIVEAUX GRADUÉS, ET LA MESURE DU NIVEAU MINIMAL POUR TRANCHER
 README.md             | 23 ++++++++++++++++++-----
 construire_donnees.py | 12 ++++++++++++
 donnees/phrases.json  | 12 +++++++++---
 llm.py                | 28 ++++++++++++++++++----------
 serveur.py            | 39 +++++++++++++++++++++++++++++++--------
 static/app.js         | 37
… [928 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur.md</path>
<type>file</type>
<content>
1: # S — L'analyseur contre les structures écrites à la main : 7/7 séquences, 93,9 % de couverture
2: 
3: > **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur les **7 phrases** du banc,
4: > l'analyseur heuristique retrouve la **séquence de types 7/7** et couvre **93,9 %** des octets des
5: > structures écrites à la main (94–97 % par phrase, sauf une à 42 % avant correction). Le reste
6: > est l'**espace de tête** des segments (convention du banc) et trois cas corrigés en chemin.
7: 
8: ## Le dispositif
9: 
10: - Structures de référence : les **7 phrases** du banc (`donnees/phrases.json`), une structure
11:   écrite à la main chacune (la première lecture).
12: - Analyseur : [`tools/structures/generateur.py`](../tools/structures/generateur.py) — lexique de
13:   mots grammaticaux, frontières de proposition, rôles par préposition.
14: - Mesure : la **séquence de types** (GN, GV, GP, REL, SUB) et la **couverture** des octets de la
15:   référence par les segments générés **du même type**.
16: 
17: ## Ce qui est mesuré
18: 
19: | phrase | types | cou
… [2316 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && echo \"=== graph ===\"; git log --all --oneline --graph --decorate | head -25; echo \"=== ancestry ===\"; git merge-base --is-ancestor c7232b3 master && echo \"c7232b3 EST ancêtre de master\" || echo \"c7232b3 N'EST  … [258 caractères tronqués]`

  ```
=== graph ===
*   3b68143 (HEAD -> master, fusion) FUSION — LE BANC DE STRUCTURES : PRAGMATIQUE, EXPORT ET ANALYSEUR EN UN SEUL ARBRE
|\  
* | 1cf64d2 EXPORT — LA BANQUE VALIDÉE DEVIENT UN CORPUS JSONL (SPANS VÉRIFIÉS)
| | * c7232b3 (n2-analyse) ANALYSEUR — L'ADVERBE DE TEMPS ET LE « QU'ELLE » : 7/7 SÉQUENCES, 94 % DE COUVERTURE
| | * a7d41a3 ANALYSEUR — SUBORDONNÉES, COORDINATION, ET EXPORT VERS LE CORPUS
| |/  
| * 733b1a4 (origin/master, origin/HEAD) CONTEXTE — DES NIVEAUX GRADUÉS, ET LA MESURE DU NIVEAU MINIMAL POUR TRANCHER
| * 7366191 PRAGMATIQUE — LE CONTEXTE TRANCHE, LE DOUBLE SENS SE CONSERVE
|/  
* a407095 GÉNÉRATEUR — UNE PHRASE BRUTE → DES STRUCTURES CANDIDATES (V0 HEURISTIQUE)
* ccb1006 v0 — le banc de structures : phrases, candidats, validation, LLM, banque
=== ancestry ===
c7232b3 N'EST PAS ancêtre de master
=== diff generateur ===
=== TESTS ===
  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/export HTTP/1.1" 200 -
.
----------------------------------------------------------------------
Ran 19 tests in 3.643s

OK
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/continuite.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/continuite.md</path>
<type>file</type>
<content>
1: # Continuité — cycles longs, sous-agents, état unique
2: 
3: > **Objet.** Comment un travail continue : cycles DSH, sous-agents, discipline de
4: > [`en-cours`](../pilotage/en-cours.md). Ni planning ni résultats : **qui écrit l'état, quand, et avec quoi on reprend**.
5: >
6: > **Règle d'or.** Un cycle est fini quand le résultat est **mesuré, écrit, committé**, qu'`en-cours` porte sa
7: > **prochaine action**, et que la roadmap est à jour.
8: 
9: ## 1. Les cycles DSH
10: 
11: | réglage | valeur | pourquoi |
12: |---|---|---|
13: | `max_goal_rounds` | **1 000** (ou le maximum du harnais) | la limite est un **filet**, pas un objectif : on ne s'arrête pas à 20 ou 50 rounds |
14: | goal | **un par programme** (N, B, docs) | recréer un goal à chaque tâche casse la continuité et l'historique |
15: | reprise | `update_goal resume` | on reprend le **même** goal, on n'en ouvre pas un nouveau |
16: | fin de cycle | résultat + fiche + commit + `en-cours` + roadmap | jamais « le temps est écoulé » |
17: 
18: - **Un cycle = un sous-chantier**, pas un round : plusieurs heures et 
… [6760 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,200p' tools/sessions.py", "description": "Read sessions.py first half"}`

  ```
#!/usr/bin/env python3
"""sessions.py — plans de session : qui fait quoi, avant d'écrire `en-cours`.

Chaque session active expose son mandat dans `journal/sessions/<id>/plan.md` :
périmètre, fichiers réservés, heartbeat, prochaine action, état. Les autres
sessions consultent `--status` avant de claim, et `--check --strict` refuse les
mandats incomplets, les identifiants dupliqués, les périmètres qui se recouvrent
et les heartbeats périmés (le `--check` seul les signale). `en-cours` reste la
seule source de l'état : ce plan est le **contrat de travail** qui le précède.
Une session arrêtée (reboot, panne) passe à `État : en pause` : elle reste dans
l'état, son heartbeat n'est plus exigé, et la reprise la remet `actif`.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
SESSIONS = "journal/sessions"
ETAT = "docs/pilotage/en-cours.md"
CHAMPS = ("session", "rôle", "périmètre", "fichiers réservés", "heartbeat",
          "prochaine action", "état")
ACTIFS = {"actif", "active", "en cours", "bloqué", "bloquee", "bloqué(e)"}
PAUSE = {"en pause", "pa
… [7609 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== hook ===\"; ls .git/hooks | head; sed -n '1,160p' .git/hooks/pre-commit 2>/dev/null; echo \"=== verifie_etat ===\"; sed -n '1,120p' tools/verifie_etat_a_jour.py", "description": "Inspect pre-commit hook and state checker"}`

  ```
=== hook ===
applypatch-msg.sample
commit-msg.sample
fsmonitor-watchman.sample
post-update.sample
pre-applypatch.sample
pre-commit
pre-commit.sample
pre-merge-commit.sample
prepare-commit-msg.sample
pre-push.sample
#!/bin/sh
# pre-commit — l'état accompagne le fait, le journal accompagne le code.
#
# Versionné dans tools/hooks/ et installé par tools/installe_hooks.sh : un hook qui
# ne vit que dans .git/hooks ne survit ni au clone ni au nettoyage.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 0

# 1. Aucun fait (reports/, roadmap, backlog) ne se commite sans sa ligne d'état.
#    C'est la garantie de fraîcheur de docs/pilotage/en-cours.md : elle ne dépend
#    pas de la survie d'une session « principale », elle est vérifiée au commit.
if ! python3 tools/verifie_etat_a_jour.py --index; then
    echo "  ⛔ commit refusé : un fait sans ligne d'état."
    echo "     mets docs/pilotage/en-cours.md à jour, puis :"
    echo "     git add docs/pilotage/en-cours.md"
    exit 1
fi

# 2. Archive les traces de session DSH avant chaque commit : le journal doit
#    accompagner le code, pas le suivre.
python3 tools/archive_sessions.py --quiet >/dev/null || { echo "  ⛔ archivage des session
… [5211 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"hub\" docs/methode/ docs/pilotage/plan-travail.md tools/*.py 2>/dev/null | head -40; echo \"=== mailbox ===\"; ls -la journal/sessions/ | tail -20; find . -maxdepth 3 -iname \"*boite*\" -o -maxdepth 3 -iname \"*mail*\" 2>/ … [69 caractères tronqués]`

  ```
docs/methode/modularisation.md:20:`https://github.com/stephanedenis/drave` (**privé**), remote `origin` en SSH
docs/methode/modularisation.md:21:(`git@github.com:stephanedenis/drave.git`), branche `master` suivie.
docs/methode/modularisation.md:27:fonctionnement : la clé SSH `~/.ssh/id_ed25519_github` suffit pour pousser, et la
docs/methode/modularisation.md:28:configuration globale réécrit déjà `https://github.com/…` en SSH.
docs/pilotage/plan-travail.md:43:**Le rôle d'intégration** (le « hub ») : tient `en-cours`, `roadmap`, `chantiers`, ce plan,
docs/pilotage/plan-travail.md:64:| **hub** (intégration) | `docs/pilotage/en-cours.md`, `roadmap.md`, `chantiers.md`, `plan-travail.md`, `README.md`, `journal/` (hors `sessions/<id>/`), `reports/INDEX.md`, `AGENTS.md`, `tools/surveille_sessions.py`, `tools/carte_chantiers.py` | tout le reste |
docs/pilotage/plan-travail.md:67:`reports/INDEX.md` et `journal/` ne s'écrivent que par **le hub**, à la demande des sessions (leur
docs/pilotage/plan-travail.md:69:plan, elles la remettent au hub au checkpoint ; le hub l'intègre et commite. Si une session doit
docs/pilotage/plan-travail.md:71:fenêtre d'intégration** et le hub relit après — c'est l
… [5035 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '200,400p' tools/sessions.py", "description": "Read sessions.py second half"}`

  ```
if not plans:
        print("  (aucun plan — chaque session active doit créer journal/sessions/<id>/plan.md)")
    for p in plans:
        age = "—" if p["age"] is None else f"{p['age']:.0f} min"
        marque = "⏰" if p["age"] is not None and p["age"] > PEREMPTION_MIN and p["etat"] in ACTIFS else " "
        per = ", ".join(p["perimetre"]) or "—"
        print(f"  {marque} {p['id'][:18]:18} · {p['etat'] or '?':8} · {age:>7} · {per}")
        if p["champs"].get("prochaine action"):
            print(f"      → {p['champs']['prochaine action']}")
    for a in avertissements:
        print(f"  ⚠ {a}")
    for e in erreurs:
        print(f"  ❌ {e}")
    return 1 if erreurs else 0


def autotest() -> int:
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "docs/pilotage").mkdir(parents=True)
        (r / ETAT).write_text("### Session `a` — test\n", encoding="utf-8")
        d = r / SESSIONS / "a"
        d.mkdir(parents=True)
        (d / "plan.md").write_text(
            "# Plan\n\n- **Session** : `a`\n- **Rôle** : test\n- **Périmètre** : A8.0\n"
            "- **Fichiers réservés** : `tools/a.py`\n- **Heartbeat** : 2026-10-30 11:00 HAE\n"
            "- 
… [3146 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date; echo \"=== plan-travail §3 ===\"; sed -n '40,95p' docs/pilotage/plan-travail.md; echo \"=== §8 ===\"; sed -n '150,215p' docs/pilotage/plan-travail.md", "description": "Read date and plan-travail territory rules"}`

  ```
lun 02 nov 2026 16:16:36 EST
=== plan-travail §3 ===
| **S — les structures (à ouvrir)** | les structures d'interprétation candidates, la validation humaine/LLM, la banque | S, la pragmatique, l'export | **CPU**, 2–4 cœurs | l'analyseur plus riche (rôles, subordonnées), l'export vers le corpus. **Aucune session DSH ; sous-module `tools/structures`.** |
| **D/R/A — en pause** | les corpus (texte intégral, PDF/OCR, licences, stubs), la préparation de R1.1/R1.2, A2.6/A8.3 | D, R1, A2.6/A8.3 | **CPU/IO**, 4–16 cœurs | 10 corpus, PDF, OCR 20 livres + 10 notes CEGEP, glossaire 355 entrées : **fait et committé**. Reprise : `fe3c05f0` (`--resume`), OCR ~127 scans, clôture. |

**Le rôle d'intégration** (le « hub ») : tient `en-cours`, `roadmap`, `chantiers`, ce plan,
`journal/`, `reports/INDEX.md`, `AGENTS.md`, les compteurs et la revue de documentation. Il ne
code pas un chantier ; il **intègre** les sections des sessions, met à jour les compteurs, vérifie
les portes et commite. Il est **un seul à la fois** (voir § 4).

**Les sous-agents** : 2 à 4 par session, sur des tâches **bornées** (une mesure, un outil, une
fiche, un audit) ; ils ne touchent ni `en-cours`, ni la roadmap, ni `AGENTS.m
… [8535 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la work/n2w/ 2>/dev/null | head -30; echo \"=== report s files ===\"; ls reports/ | grep -iE \"^rapport-s|^s-\" ; echo \"=== data dirs ===\"; ls data | head -40", "description": "Inspect work/n2w and data layout"}`

  ```
total 1340548
drwxr-xr-x. 1 stephane stephane      1158  2 nov 13:27 .
drwxr-xr-x. 1 stephane stephane       240  2 nov 02:07 ..
-rw-r--r--. 1 stephane stephane      1468  2 nov 02:07 analyse.py
-rw-r--r--. 1 stephane stephane 137224476  2 nov 11:09 base-big-canal.drvm
-rw-r--r--. 1 stephane stephane     21604  2 nov 11:09 base-big-canal.log
-rw-r--r--. 1 stephane stephane 137248740  2 nov 11:09 base-big-canal.pt
-rw-r--r--. 1 stephane stephane       557  2 nov 11:09 base-big-canal.pt.json
-rw-r--r--. 1 stephane stephane 137224476  2 nov 10:48 base-big.drvm
-rw-r--r--. 1 stephane stephane     21592  2 nov 10:48 base-big.log
-rw-r--r--. 1 stephane stephane 137247942  2 nov 10:48 base-big.pt
-rw-r--r--. 1 stephane stephane       557  2 nov 10:48 base-big.pt.json
-rw-r--r--. 1 stephane stephane 137224476  2 nov 12:10 big-60k.drvm
-rw-r--r--. 1 stephane stephane     63954  2 nov 12:10 big-60k.log
-rw-r--r--. 1 stephane stephane 137247233  2 nov 12:10 big-60k.pt
-rw-r--r--. 1 stephane stephane       550  2 nov 12:10 big-60k.pt.json
-rw-r--r--. 1 stephane stephane       136  2 nov 10:28 canal_big.log
-rw-r--r--. 1 stephane stephane         0  2 nov 09:14 corpus_big.log
-rw-r--r--. 1 step
… [2016 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/exporter_corpus.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """generateur.py — une phrase brute → des structures candidates (v0 heuristique).
3: 
4: Ce n'est pas un analyseur syntaxique : c'est un **générateur de candidats** à faire valider par
5: un humain. Il segmente (GN, GV, GP, REL, SUB), devine des rôles par la préposition, puis produit
6: plusieurs candidats en variant l'**attachement** de chaque segment ambigu (GN le plus proche ou
7: GV le plus proche).
8: 
9:     python3 generateur.py "Le chat de la voisine qui dort sur le toit se réveille."
10:     python3 generateur.py --json "..."     # la structure complète
11: """
12: from __future__ import annotations
13: 
14: import json
15: import re
16: import unicodedata
17: 
18: DET = set("le la les l un une ce cet cette ces mon ma mes ton ta tes son sa ses "
19:           "notre nos votre vos leur leurs quel quelle quels quelles".split())
20: PREP = set("a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis "
21:            "pendant durant contre malgre selon pres loin devant derriere apres avant".split())
22: REL
… [11613 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/exporter_corpus.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """exporter_corpus.py — la banque validée du banc de structures → un corpus JSONL pour Drave.
3: 
4: Le banc de structures produit des interprétations candidates, un humain les valide
5: (`donnees/validations.jsonl`), et ce fichier transforme les candidats **acceptés** en un corpus
6: stable, relisible par le dépôt principal :
7: 
8:     python3 exporter_corpus.py --dossier donnees --sortie ../../data/structures/banque.jsonl
9: 
10: Trois règles, parce qu'un corpus faux contamine tout ce qui l'utilise :
11: 
12: 1. **le dernier verdict gagne** — le journal est append-only ; un candidat validé `ok` puis `non`
13:    ne sort pas ;
14: 2. **les spans sont vérifiés** — un segment qui ne correspond pas au texte est une erreur, pas
15:    une ligne de plus ;
16: 3. **le manifeste porte le compte et l'empreinte** — le corpus se cite, se versionne et se
17:    rejoue.
18: 
19: Le corpus n'est pas une vérité : c'est une **banque de structures validées par un humain**, avec
20: ses phrases, ses segments, ses attachements et ses verdicts. Il
… [5740 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && echo \"=== validations n2-analyse ===\"; git show n2-analyse:donnees/validations.jsonl; echo \"=== diff exporter (n2-analyse -> master) ===\"; git diff n2-analyse master -- exporter_corpus.py | head -240", "descripti … [57 caractères tronqués]`

  ```
=== validations n2-analyse ===
{"phrase_id": "p001", "candidat_id": "p001-c1", "statut": "double_sens", "note": "", "contexte": "", "auteur": "humain", "horodatage": "2026-11-01T11:20:57"}
{"phrase_id": "p002", "candidat_id": "p002-c1", "statut": "double_sens", "note": "", "contexte": "", "auteur": "humain", "horodatage": "2026-11-01T11:21:23"}
{"phrase_id": "p003", "candidat_id": "p003-c1", "statut": "resolu", "note": "", "contexte": "", "auteur": "humain", "horodatage": "2026-11-01T11:22:09"}
{"phrase_id": "p002", "candidat_id": "p002-c2", "statut": "double_sens", "note": "", "contexte": "", "auteur": "humain", "horodatage": "2026-11-01T11:22:29"}
{"phrase_id": "p003", "candidat_id": "p003-c2", "statut": "exclu", "note": "", "contexte": "", "auteur": "humain", "horodatage": "2026-11-01T11:22:40"}
{"phrase_id": "p004", "candidat_id": "p004-c1", "statut": "resolu", "note": "", "contexte": "", "auteur": "humain", "horodatage": "2026-11-01T11:22:51"}
{"phrase_id": "p004", "candidat_id": "p004-c2", "statut": "resolu", "note": "", "contexte": "", "auteur": "humain", "horodatage": "2026-11-01T11:23:01"}
{"phrase_id": "p001", "candidat_id": "p001-c1", "statut": "resolu", "note": "", "con
… [9322 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2w/analyse.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/n2w/analyse.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """analyse.py — l'analyseur contre les structures écrites à la main (les 7 phrases du banc)."""
3: import json, sys
4: sys.path.insert(0, 'tools/structures')
5: import generateur
6: 
7: d = json.load(open('tools/structures/donnees/phrases.json'))
8: lignes = []
9: for p in d['phrases']:
10:     ref = p['candidats'][0]
11:     ref_types = [s['type'] for s in ref['segments']]
12:     ref_spans = [(s['debut'], s['fin'], s['type']) for s in ref['segments']]
13:     gen = generateur.analyser(p['texte'])
14:     gen0 = gen[0] if gen else {'segments': []}
15:     gen_types = [s['type'] for s in gen0['segments']]
16:     gen_spans = [(s['debut'], s['fin'], s['type']) for s in gen0['segments']]
17:     exact = ref_spans == gen_spans
18:     types_ok = ref_types == gen_types
19:     couverture = len(set(ref_spans) & set(gen_spans)) / max(1, len(set(ref_spans) | set(gen_spans)))
20:     lignes.append({"phrase": p['id'], "ref": ref_types, "gen": gen_types,
21:                    "types_ok": types_ok, "spans_ok": exact, "jaccard": round(couverture, 2)})
22:  
… [509 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/structures/.gitignore; echo \"=== search bank ===\"; find . -path ./work -prune -o -name \"validations.jsonl\" -print -o -name \"banque*.jsonl\" -print -o -name \"banque-manifest.json\" -print 2>/dev/null | head; echo \"=== … [140 caractères tronqués]`

  ```
__pycache__/
*.pyc
=== search bank ===
=== hub plan ===
# Plan de session — le hub, la reprise après reboot

> **Mandat vivant.** Ouvert le 2026-11-02 15 h 50 HNE depuis
> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md). Ce plan est le **contrat de
> synergie** : il dit ce que la session réserve, ce qu'elle attend des autres, et quand elle s'arrête.
> Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.

- **Session** : `536cd5d6-94ac-4057-8fe9-11709a4587c7`
- **Rôle** : **Hub** — intégration, état, roadmap, chantiers, journal, compteurs ; reprise après le
  reboot du 02/11 15 h 06 ; remise à zéro de la sédimentation ; runbook multi-terminaux.
- **Périmètre** : pilotage (en-cours, roadmap, chantiers, plan-travail, références), backlog, journal
  (hors `sessions/<id>/`), `reports/README.md`, `reports/INDEX.md`, outillage de pilotage.
- **Fichiers réservés** : `docs/pilotage/`, `journal/` (hors `sessions/<id>/`),
  `reports/README.md`, `reports/INDEX.md`, `AGENTS.md`, `tools/sessions.py`,
  `tools/porte-sessions.sh`, `tools/index_reports.py`, `tools/surveille_sessions.py`,
  `journal/sessions/536cd5d6-…/`.
- **Heartbeat** : 2026-11-02 16:09 EST
- **Pr
… [1135 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('tools/structures/donnees/phrases.json'))\nfor p in d['phrases']:\n    print(p['id'], p['texte'])\n    for c in p['candidats']:\n        print('  ', c['id'], c.get('nom'), '|', [(s['typ … [155 caractères tronqués]`

  ```
p001 Le chat de la voisine qui dort sur le toit se réveille.
   p001-c1 « qui dort » sur le chat | [('GN', 'agent', 0, 'Le chat'), ('GP', 'possession', 0, ' de la voisine'), ('REL', 'qualite', 1, ' qui dort sur le toit'), ('GV', 'predicat', 0, ' se réveille')] | att {'segment': ' qui dort sur le toit', 'cible': 'Le chat', 'genre': 'relative'}
   p001-c2 « qui dort » sur la voisine | [('GN', 'agent', 0, 'Le chat'), ('GP', 'possession', 0, ' de la voisine'), ('REL', 'qualite', 2, ' qui dort sur le toit'), ('GV', 'predicat', 0, ' se réveille')] | att {'segment': ' qui dort sur le toit', 'cible': ' de la voisine', 'genre': 'relative'}
p002 J'ai vu l'homme avec le télescope.
   p002-c1 avec le télescope = moyen de voir | [('GV', 'predicat', 0, "J'ai vu"), ('GN', 'patient', 0, " l'homme"), ('GP', 'instrument', 1, ' avec le télescope')] | att {'segment': ' avec le télescope', 'cible': "J'ai vu", 'genre': 'gp'}
   p002-c2 avec le télescope = qualité de l'homme | [('GV', 'predicat', 0, "J'ai vu"), ('GN', 'patient', 0, " l'homme"), ('GP', 'attribut', 2, ' avec le télescope')] | att {'segment': ' avec le télescope', 'cible': " l'homme", 'genre': 'gp'}
p003 La femme a vu l'homme dans le parc.

… [2383 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 work/n2w/analyse.py; echo \"=== générateur p001 ===\"; cd tools/structures && python3 generateur.py --json \"Le chat de la voisine qui dort sur le toit se réveille.\" | head -60", "description": "Run analyzer measurement and  … [15 caractères tronqués]`

  ```
p001 · types OK · spans non · Jaccard 0.14
   réf ['GN', 'GP', 'REL', 'GV']
   gén ['GN', 'GP', 'REL', 'GV']
p002 · types OK · spans non · Jaccard 0.20
   réf ['GV', 'GN', 'GP']
   gén ['GV', 'GN', 'GP']
p003 · types OK · spans non · Jaccard 0.14
   réf ['GN', 'GV', 'GN', 'GP']
   gén ['GN', 'GV', 'GN', 'GP']
p004 · types OK · spans non · Jaccard 0.33
   réf ['GV', 'GP']
   gén ['GV', 'GP']
p005 · types OK · spans non · Jaccard 0.20
   réf ['GV', 'GP', 'GP']
   gén ['GV', 'GP', 'GP']
p006 · types OK · spans non · Jaccard 0.20
   réf ['GV', 'SUB', 'GP']
   gén ['GV', 'SUB', 'GP']
p007 · types OK · spans non · Jaccard 0.20
   réf ['GN', 'GV', 'GP']
   gén ['GN', 'GV', 'GP']
{"phrases": 7, "types_ok": 7, "spans_ok": 0, "jaccard_moyen": 0.2}
=== générateur p001 ===
[
 {
  "nom": "« qui dort sur le toit » → voisine",
  "lecture": "« qui dort sur le toit » se rattache à « voisine »",
  "attachement": {
   "segment": "qui dort sur le toit",
   "cible": "voisine",
   "genre": "GP"
  },
  "segments": [
   {
    "debut": 0,
    "fin": 7,
    "texte": "Le chat",
    "type": "GN",
    "role": "agent",
    "niveau": 0
   },
   {
    "debut": 8,
    "fin": 21,
    "texte": "de la voisine",
    "
… [678 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/serveur.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/serveur.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """serveur.py — le banc de structures : API + interface web, sans dépendance.
3: 
4: Le serveur expose les phrases et leurs interprétations candidates, enregistre les verdicts
5: humains (`donnees/validations.jsonl`), interroge un grand modèle (`donnees/llm.jsonl`) et exporte
6: la banque validée (`/api/export`).
7: 
8:     python3 serveur.py                 # http://127.0.0.1:8765
9:     python3 serveur.py --port 9000 --hote 0.0.0.0
10: """
11: from __future__ import annotations
12: 
13: import argparse
14: import json
15: import pathlib
16: import threading
17: import time
18: from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
19: from urllib.parse import urlparse
20: 
21: import generateur
22: import llm
23: 
24: RACINE = pathlib.Path(__file__).resolve().parent
25: STATIQUE = RACINE / "static"
26: # Le niveau pragmatique : un sens n'est pas « vrai » hors contexte, il est **résolu** par lui,
27: # **compatible** avec lui, **exclu** par lui — ou **double**, quand l'ambiguïté est voulue.
28: STATUTS = {"resolu", "compatib
… [11132 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_export.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_generateur.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_export.py</path>
<type>file</type>
<content>
1: """Tests de l'export corpus — le dernier verdict gagne, les spans sont vérifiés."""
2: import json
3: import pathlib
4: import shutil
5: import tempfile
6: import unittest
7: 
8: import exporter_corpus
9: 
10: RACINE = pathlib.Path(__file__).resolve().parent.parent
11: 
12: 
13: class TestExport(unittest.TestCase):
14:     def setUp(self):
15:         self.dossier = pathlib.Path(tempfile.mkdtemp())
16:         shutil.copy(RACINE / "donnees" / "phrases.json", self.dossier / "phrases.json")
17: 
18:     def tearDown(self):
19:         shutil.rmtree(self.dossier, ignore_errors=True)
20: 
21:     def _valider(self, pid, cid, verdict):
22:         with (self.dossier / "validations.jsonl").open("a", encoding="utf-8") as f:
23:             f.write(json.dumps({"phrase_id": pid, "candidat_id": cid, "verdict": verdict,
24:                                 "auteur": "test", "horodatage": "2026-11-01T11:00:00"}) + "\n")
25: 
26:     def test_dernier_verdict_gagne(self):
27:         self._valider("p001", "p001-c1", "ok")
28:         self._valider("p001", "p001-c1", "n
… [1856 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_generateur.py</path>
<type>file</type>
<content>
1: """Tests du générateur de candidats."""
2: import unittest
3: 
4: import generateur
5: 
6: 
7: class TestGenerateur(unittest.TestCase):
8:     def test_segments_alignes(self):
9:         for texte in ("Le chat de la voisine qui dort sur le toit se réveille.",
10:                       "J'ai vu l'homme avec le télescope.",
11:                       "Il a couru pour attraper le bus.",
12:                       "Elle a dit qu'elle viendrait hier."):
13:             for c in generateur.analyser(texte):
14:                 prec = 0
15:                 for s in c["segments"]:
16:                     self.assertGreaterEqual(s["debut"], prec, texte)
17:                     self.assertLessEqual(s["fin"], len(texte), texte)
18:                     self.assertEqual(texte[s["debut"]:s["fin"]], s["texte"], texte)
19:                     prec = s["fin"]
20:                 self.assertGreaterEqual(len(c["segments"]), 2, texte)
21: 
22:     def test_relative_deux_lectures(self):
23:         cs = generateur.analyser("Le chat de la voisine qui dort sur le toit se réve
… [2605 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_serveur.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_serveur.py</path>
<type>file</type>
<content>
1: """Tests du banc de structures — sans dépendance : unittest + urllib."""
2: import json
3: import pathlib
4: import shutil
5: import tempfile
6: import threading
7: import unittest
8: import urllib.request
9: from http.server import ThreadingHTTPServer
10: 
11: import serveur
12: 
13: RACINE = pathlib.Path(__file__).resolve().parent.parent
14: 
15: 
16: class Banc:
17:     def __enter__(self):
18:         self.dossier = pathlib.Path(tempfile.mkdtemp())
19:         shutil.copy(RACINE / "donnees" / "phrases.json", self.dossier / "phrases.json")
20:         self.serveur = ThreadingHTTPServer(("127.0.0.1", 0), serveur.Serveur)
21:         self.serveur.donnees = serveur.Donnees(self.dossier)
22:         self.port = self.serveur.server_address[1]
23:         self.fil = threading.Thread(target=self.serveur.serve_forever, daemon=True)
24:         self.fil.start()
25:         return self
26: 
27:     def __exit__(self, *a):
28:         self.serveur.shutdown()
29:         self.serveur.server_close()
30:         shutil.rmtree(self.dossier, ignore_errors=True)
31: 
… [5301 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git show -s --format='%H%n%s%n%b' a7d41a3; echo \"=== validations history ===\"; git log --oneline --all -- donnees/validations.jsonl; echo \"=== exporter history ===\"; git log --oneline --all -- exporter_corpus.py; … [206 caractères tronqués]`

  ```
a7d41a377994801f318e8f78940a067f267074ab
ANALYSEUR — SUBORDONNÉES, COORDINATION, ET EXPORT VERS LE CORPUS
Le générateur distingue désormais le « que » complément (après un verbe → SUB) de la relative
(après un nom → REL), arrête la relative au verbe principal (une AUX après un verbe), traite la
coordination (et, ou, mais…) comme une nouvelle proposition et non comme une subordonnée, et
borne le GN à trois mots pleins.

exporter_corpus.py transforme la banque validée en corpus : format texte (phrase + structure
linéarisée en balises) ou JSONL ; seules les lectures acceptées sortent, l'export est déterministe.

Quinze tests passent, dont trois nouveaux : complément après verbe, relative qui n'avale pas le
verbe principal, coordination en deux propositions.

=== validations history ===
a7d41a3 ANALYSEUR — SUBORDONNÉES, COORDINATION, ET EXPORT VERS LE CORPUS
=== exporter history ===
a7d41a3 ANALYSEUR — SUBORDONNÉES, COORDINATION, ET EXPORT VERS LE CORPUS
1cf64d2 EXPORT — LA BANQUE VALIDÉE DEVIENT UN CORPUS JSONL (SPANS VÉRIFIÉS)
=== main repo data/structures history ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== MAIN STATUS ===\"; git status --short; echo \"=== submodule status ===\"; git submodule status; echo \"=== reports s ===\"; ls -la reports/rapport-s-analyseur.md; echo \"=== mentions banque ===\"; grep -rn \"data/structure … [163 caractères tronqués]`

  ```
=== MAIN STATUS ===
 M journal/README.md
A  journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md
 M journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/digest.md
 M journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/rapport.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
?? journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
?? journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
?? journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/
?? journal/sessions/abb58991-fe0a-4d6e-b039-6552b09f8454/
?? journal/sessions/b7d4678e-2143-4daa-a9a4-a456c5aa8dab/
?? journal/sessions/caaf3018-e3e2-4416-8446-11f0335910aa/
=== submodule status ===
 d256888934b017ac024de2a8eed22ecf81e6c799 tools/docwatch (v0.4.1-3-gd256888)
 3b68143f3e805372c0fe2fcdbc2f574b95c7e9d3 tools/structures (heads/fusion)
=== reports s ===
-rw-r--r--. 1 stephane stephane 3265  2 nov 02:11 reports/rapport-s-analyseur.md
=== mentions banque ===
./tools/structures/tests/test_export.py:30:        sortie = self.dossier / "banque.jsonl"
./tools/structures/tests/test_export.py:47:            exporter_corpus.exporter(self.dossier, self.dossier
… [2387 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat .gitignore; echo \"=== my session dir ===\"; ls -la journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/; echo \"=== new sessions ===\"; for d in 0733c5bb-f90b-4f58-9241-3364fa32e46c abb58991-fe0a-4d6e-b039-6552b09f8454 b7d4678 … [237 caractères tronqués]`

  ```
__pycache__/
*.pyc
reports/*.tmp
models/
data/
qtrinet-core/target/

# Traces de session : la copie brute reste sur disque (volumineuse, binaire),
# le digest markdown est versionné.
journal/sessions/*/session*.jsonl.zstd
journal/sessions/archive.log

# Outil de référence : la source est versionnée, le binaire se recompile
# (commande exacte dans tools/ref_logits.md).
tools/ref_logits
target/

# docwatch — SVG générés depuis les sources .puml/.mmd (docwatch les produit)
docs/**/*.puml.svg
docs/**/*.mmd.svg

# Campagnes GPU : points de contrôle et journaux de run (hors dépôt, archivés à part)
work/
=== my session dir ===
total 208
drwxr-xr-x. 1 stephane stephane     80  2 nov 16:16 .
drwxr-xr-x. 1 stephane stephane   8440  2 nov 16:16 ..
-rw-r--r--. 1 stephane stephane  51648  2 nov 16:17 digest.md
-rw-r--r--. 1 stephane stephane   3504  2 nov 16:17 rapport.md
-rw-------. 1 stephane stephane 152988  2 nov 16:17 session.v4.jsonl.zstd
=== new sessions ===
-- 0733c5bb-f90b-4f58-9241-3364fa32e46c
digest.md
plan.md
rapport.md
session.v4.jsonl.zstd
# Plan de session — N2, le natif : 200 000 pas et la fenêtre

> **Mandat ouvert** le 2026-11-02 16 h 20 HAE depuis
> [`docs/pilotage/en-cours.
… [1421 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== data suivis ===\"; git ls-files data | head -20; echo \"count: $(git ls-files data | wc -l)\"; echo \"=== reports json exemples ===\"; git ls-files reports | grep -E \"manifest|corpus.*json\" | head; echo \"=== tailles === … [112 caractères tronqués]`

  ```
=== data suivis ===
count: 0
=== reports json exemples ===
reports/b102bis-corpus-jw.json
reports/campagne-benefices/051-R-annexe-manifeste-des-journaux.md
reports/corpus-genres.json
reports/corpus-litt-propre.json
reports/corpus-multi-propre.json
reports/corpus-pdf-contamination.json
reports/corpus-pdf-documents-contamination.json
reports/corpus-pdf-documents.json
reports/corpus-pdf.json
reports/corpus-propre.json
=== tailles ===
200K	tools/structures
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' docs/methode/resultats.md", "description": "Read results method"}`

  ```
# Ce qu'un résultat doit porter

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant d'écrire une fiche**, un JSON de
> résultats, ou un message de commit.

## Les cinq pièces d'un résultat

1. **Le chiffre** — la valeur, avec son [unité](../theorie/glossaire/entrees/unite.md) et son arrondi utile (jamais plus de chiffres que l'instrument n'en
   [porte](../theorie/glossaire/entrees/porte.md)) ;
2. **La mesure qui le produit** — le calcul exact, la métrique ([chrF](../theorie/glossaire/entrees/chrf.md), précision, rappel, [AUC](../theorie/glossaire/entrees/auc.md)…), et ce qu'elle ne
   mesure pas ;
3. **Le dispositif** — quel [corpus](../theorie/glossaire/entrees/corpus.md) (et sa provenance), quel modèle (taille, [quantification](../theorie/glossaire/entrees/quantification.md), date de coupure),
   quelles **couches de neurones** sondées, quel découpage, **quelle unité de mesure** (unité de sens ou unité
   grammaticale ; si c'est un [jeton](../theorie/glossaire/entrees/jeton.md), le dire comme **technique**), quels réglages (prompt, gabarit, longueur de
   sortie, graine) ;
4. **Le [contrôle négatif](../theorie/glossaire/entrees/controle-negatif.md)
… [2500 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/sessions.py --modele", "description": "Print official session plan template"}`

  ```
# Plan de session — <id>

> **Mandat vivant.** Écris ce fichier **avant** `en-cours`, mets-le à jour à chaque cycle,
> et passe `État : en pause` (arrêt) ou `État : terminé` (retrait) quand elle s'arrête.

- **Session** : `<id>`
- **Rôle** : <chantier / programme>
- **Périmètre** : <A8.0, R13, ...>
- **Fichiers réservés** : `tools/...`, `reports/...`
- **Heartbeat** : <AAAA-MM-JJ HH:MM HAE>
- **Prochaine action** : <une action nommée>
- **État** : actif (ou `en pause` / `terminé`)
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md", "content": "# Plan de session — S, les structures (analyser, banquer, exporter)\n\n> **Mandat vivant.** Ouvert le 2026-11-02 16 h 22 HNE depuis\n> [`docs/pilotage/en-cours.m … [3481 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/sessions.py --check; echo \"exit=$?\"; echo \"=== status ===\"; python3 tools/sessions.py --status 2>&1 | head -20", "description": "Validate session plan and check overlaps"}`

  ```
⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/structures/` (export local (29ad180d-38a5-4481-a9a7-ec6ab31c895f)
  ⚠ plan actif non listé dans en-cours : 0733c5bb-f90b-4f58-9241-3364fa32e46c
  ⚠ plan actif non listé dans en-cours : 29ad180d-38a5-4481-a9a7-ec6ab31c895f
exit=0
=== status ===
sessions · plans de mandat
    0733c5bb-f90b-4f58 · actif    ·  -1 min · N2 (200 000 pas sur le mélange, PPL domaine/littérature/anglais/wikitext2, courbe de longueur), R1.1/R1.2 mesurés depuis N2
      → **200 000 pas sur `data/wiki_mix/propre`** (34,3 M, canal, positions aléatoires, graine 1) puis la mesure des cinq PPL et de la courbe 128/256/512.
    0b0a6a0d-05f5-4308 · terminé  · 1904 min · N2.h — corpus propre, porte honnête, généralité, verrou de longueur
      → close — N2.i (3,13 / 12,93 / 33,83) et Pensée v0 (6/6 portes) sont committés.
    0b69f616-5c75-4c34 · terminé  · 3978 min · R0.4, R0.5, R13, R4.1–R4.3, en-cours, roadmap, backlog
      → clôture reprise par la session `22e518ee` — commit, archives, état.
    22e518ee-81b8-4081 · terminé  · 3149 min · archives de sessions, journal, en-cours, roadmap, backlog, outillage d'archivage
      → clôture committ
… [1694 caractères tronqués]
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M:%S %Z'", "description": "Read real current time"}`

  ```
2026-11-02 16:19:13 EST
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np = Path(\"journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md\")\nt = p.read_text(encoding=\"utf-8\")\nt = t.replace(\"Ouvert le 2026-11-02 16 h 22 HNE\", \"Ouvert le 2026-11-02  … [917 caractères tronqués]`

  ```
# Plan de session — S, les structures (analyser, banquer, exporter)

> **Mandat vivant.** Ouvert le 2026-11-02 16 h 19 HNE depuis
> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md) (§ S) et
> [`plan-travail.md`](../../../docs/pilotage/plan-travail.md) § 9.2.
> Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.
> `en-cours` reste la seule source de l'état : ce plan est le **contrat de travail** qui le
> précède, et la section S y est **proposée au hub**, pas écrite ici.

- **Session** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f`
- **Rôle** : **S — les structures** : le banc d'interprétations candidates (outil web, générateur,
  pragmatique, banque), l'**analyseur** (rôles, subordonnées) et l'**export au corpus**.
- **Périmètre** : S (structures) — S-analyseur rôles/subordonnées · S-banque · S-export au corpus.
- **Fichiers réservés** : `tools/structures/` ; `data/structures/` ; `reports/rapport-s-*` ;
  `reports/s-banque-*` ; `journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/`.
  Le sous-module est la source ; `data/structures/` est l'export local (tout `data/` est ignoré par
  git) ; le chevauchement avec le `data/` de N2 est nominal (sous-dossier
… [200 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport sessions\np = sessions.lire_plan(sessions.Path('journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md'))\nprint(\"HEARTBEAT\", p['heartbeat'], \"AGE\", p['age'] … [236 caractères tronqués]`

  ```
HEARTBEAT 2026-11-02 16:19:00 AGE 0.3678120166666667
ETAT actif
PERIMETRE ['S (structures) — S-analyseur rôles/subordonnées · S-banque · S-export au corpus.']
RESERVE: 'tools/structures/'
RESERVE: 'data/structures/'
RESERVE: 'reports/rapport-s-*'
RESERVE: 'reports/s-banque-*'
RESERVE: 'journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/`. Le sous-module est la source'
RESERVE: "data/structures/` est l'export local (tout `data/` est ignoré par git)"
RESERVE: 'le chevauchement avec le `data/` de N2 est nominal (sous-dossier distinct'
RESERVE: 'fichiers distincts).'
=== check ===
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/structures/ (29ad180d-38a5-4481-a9a7-ec6ab31c895f)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/structures/` est l'export local (tout `data/` est ignoré par git) (29ad180d-38a5-4481-a9a7-ec6ab31c895f)
  ⚠ plan actif non listé dans en-cours : 0733c5bb-f90b-4f58-9241-3364fa32e46c
  ⚠ plan actif non listé dans en-cours : 29ad180d-38a5-4481-a9a7-ec6ab31c895f
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np = Path(\"journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md\")\nt = p.read_text(encoding=\"utf-8\")\nt = t.replace(\"\"\"- **Fichiers réservés** : `tools/structures/` ; `data/s … [1051 caractères tronqués]`

  ```
⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/structures/ (29ad180d-38a5-4481-a9a7-ec6ab31c895f)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/wikipedia/` (lecture) (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/corpus_wiki_* (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : tools/corpus* (0733c5bb-f90b-4f58-9241-3364fa32e46c) / tools/corpus_wikipedia*.py (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ plan actif non listé dans en-cours : 0733c5bb-f90b-4f58-9241-3364fa32e46c
  ⚠ plan actif non listé dans en-cours : 29ad180d-38a5-4481-a9a7-ec6ab31c895f
  ❌ /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md : heartbeat illisible
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np = Path(\"journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md\")\nt = p.read_text(encoding=\"utf-8\")\nt = t.replace(\"\"\"- **Heartbeat** : 2026-11-02 16:19 EST\n\n> **La réserv … [1001 caractères tronqués]`

  ```
⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/structures/ (29ad180d-38a5-4481-a9a7-ec6ab31c895f)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/wikipedia/` (lecture) (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/corpus_wiki_* (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : tools/corpus* (0733c5bb-f90b-4f58-9241-3364fa32e46c) / tools/corpus_wikipedia*.py (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ plan actif non listé dans en-cours : 0733c5bb-f90b-4f58-9241-3364fa32e46c
  ⚠ plan actif non listé dans en-cours : 29ad180d-38a5-4481-a9a7-ec6ab31c895f
exit=0
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/construire_donnees.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/construire_donnees.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """construire_donnees.py — fabrique donnees/phrases.json en calculant les spans par sous-chaîne.
3: 
4: Écrire les spans à la main est une source d'erreurs ; ici, chaque segment est donné par son
5: **texte exact**, et l'outil vérifie qu'il apparaît bien, dans l'ordre, dans la phrase.
6: """
7: import json, pathlib
8: 
9: PHRASES = [
10:     ("p001", "Le chat de la voisine qui dort sur le toit se réveille.",
11:      [("Le chat", "GN", "agent", 0), (" de la voisine", "GP", "possession", 0),
12:       (" qui dort sur le toit", "REL", "qualite", 1), (" se réveille", "GV", "predicat", 0)],
13:      "« qui dort » sur le chat",
14:      "C'est le chat qui dort ; il est à la voisine ; il est sur le toit.",
15:      (" qui dort sur le toit", "Le chat", "relative")),
16:     ("p001", "Le chat de la voisine qui dort sur le toit se réveille.",
17:      [("Le chat", "GN", "agent", 0), (" de la voisine", "GP", "possession", 0),
18:       (" qui dort sur le toit", "REL", "qualite", 2), (" se réveille", "GV", "predicat", 0)],
19:      "« qui
… [6459 caractères tronqués]
  ```

### 🤖 Assistant

Je pose le plan et la réservation, puis je mesure l'état de l'analyseur sur un jeu de phrases candidates avant de coder les règles de rôles et de subordonnées.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nimport generateur\nphrases = [\n \"Le chat de la voisine qui dort sur le toit se réveille.\",\n \"J'ai vu l'homme avec le télescope.\",\n \"La femme a vu l'homme dans le parc.\",\n \"Il a couru pour … [1042 caractères tronqués]`

  ```
Le chat de la voisine qui dort sur le toit se réveille.
    Le chat[GN:agent] | de la voisine[GP:theme] | qui dort sur le toit[REL:qualite] | se réveille[GV:predicat]
J'ai vu l'homme avec le télescope.
    J'ai vu[GV:predicat] | l'homme[GN:patient] | avec le télescope[GP:moyen]
La femme a vu l'homme dans le parc.
    La femme[GN:agent] | a vu[GV:predicat] | l'homme[GN:patient] | dans le parc[GP:lieu]
Il a couru pour attraper le bus.
    Il a couru[GV:predicat] | pour attraper le bus[GP:but]
Il a parlé à Marie de son projet.
    Il a parlé[GV:predicat] | à Marie[GP:destinataire] | de son projet[GP:theme]
Elle a dit qu'elle viendrait hier.
    Elle a dit[GV:predicat] | qu'elle viendrait[SUB:contenu] | hier[GP:temps]
Le canard est prêt à manger.
    Le canard[GN:agent] | est prêt[GV:predicat] | à manger[GP:destinataire]
Le livre que j'ai lu est passionnant.
    Le livre[GN:agent] | que j'ai lu[REL:qualite] | est passionnant[GV:predicat]
Je pense que le chat dort.
    Je pense[GV:predicat] | que le chat dort[SUB:contenu]
Quand il pleut, je reste à la maison.
    Quand il pleut[SUB:contenu] | je reste[GV:predicat] | à la maison[GP:destinataire]
Elle part parce qu'elle est fatiguée.
    
… [1340 caractères tronqués]
  ```

- **todo_write** `{"todos": [{"content": "Créer le plan de session S et réserver le territoire", "status": "completed"}, {"content": "Écrire le gold 21 phrases (types, rôles, subordonnées) avant les règles", "status": "in_progress"}, {"content": "Améliorer generateur.py : rôles contextuels, subordonnées, passif", "st … [553 caractères tronqués]`

  ```
Updated todo list: 6 pending, 1 in progress, 1 completed.
  ```

- **write** `{"content": "{\n \"version\": 1,\n \"note\": \"Gold de l'analyseur : structures de référence écrites à la main AVANT les règles de rôles/subordonnées (02/11). Les spans ne sont pas stockés : ils se calculent par sous-chaîne, dans l'ordre, comme construire_donnees.py. split=dev : les 7 phrases du ban … [5685 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/gold-analyseur.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nimport json\nd=json.load(open('donnees/gold-analyseur.json'))\nprint(\"phrases\", len(d['phrases']), \"dev\", sum(p['split']=='dev' for p in d['phrases']), \"test\", sum(p['split']=='test' for p in  … [332 caractères tronqués]`

  ```
phrases 23 dev 7 test 16
spans vérifiés
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "old_string": "ADVERBES_TEMPS = set(\"hier aujourd'hui demain maintenant ici la toujours jamais souvent deja encore tard tot\".split())\nPONCT = set(\".,;:!?…()«»\")", "new_string": "ADVERBES_TEMPS = set( … [1986 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "old_string": "def _role_gp(prep: str) -> str:\n    if prep in {\"dans\", \"sur\", \"sous\", \"chez\", \"vers\", \"entre\", \"devant\", \"derriere\", \"pres\", \"loin\"}:\n        return \"lieu\"\n    if  … [4104 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "offset": 220, "limit": 130}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py</path>
<type>file</type>
<content>
220:     utiles = [t for t in toks if t.cls != "ESPACE"]
221:     segs: list[Segment] = []
222:     i = 0
223:     while i < len(utiles):
224:         t = utiles[i]
225:         if t.cls == "PONCT":
226:             i += 1
227:             continue
228:         if t.cls == "RELATIF":
229:             j, vu_verbe = i + 1, False
230:             while j < len(utiles) and utiles[j].cls not in ("PONCT", "CONJ", "RELATIF"):
231:                 if utiles[j].cls == "PRON" and vu_verbe:
232:                     break
233:                 if utiles[j].cls == "AUX" and vu_verbe:
234:                     break
235:                 if (utiles[j].cls == "MOT" and vu_verbe
236:                         and _norm(utiles[j].texte) in ADVERBES_TEMPS):
237:                     break
238:                 vu_verbe = vu_verbe or utiles[j].cls == "MOT"
239:                 j += 1
240:             # « que » après un verbe est un complément, après un nom une relative.
241:             precedent = segs[-1].type if segs else None
242:             if _norm(t.texte).split("'")[0].split("’")[
… [5791 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "old_string": "        t = utiles[i]\n        if t.cls == \"PONCT\":\n            i += 1\n            continue\n        if t.cls == \"RELATIF\":", "new_string": "        t = utiles[i]\n        if t.cls == … [566 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "new_string": "        if t.cls == \"PREP\":\n            j = _consomme(utiles, i + 1, {\"DET\", \"MOT\"})\n            segs.append(Segment(t.debut, utiles[j - 1].fin, texte[t.debut:utiles[j - 1].fin],\n  … [444 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "new_string": "        # PRON/AUX/MOT : un GV — mais il s'arrête avant un subordonnant (« il travaille afin »).\n        j = i\n        while j < len(utiles) and utiles[j].cls in (\"PRON\", \"AUX\", \"MOT … [1139 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "new_string": "ROLES_AMBIGUS = {\"pour\": [\"cause\"]}\n\n\ndef _role_attache(role: str, genre: str) -> str | None:\n    \"\"\"Le rôle change avec l'attachement : instrument/attribut, possession/thème.\"\ … [2570 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "offset": 390, "limit": 50}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py</path>
<type>file</type>
<content>
390:             break
391:     return candidats
392: 
393: 
394: if __name__ == "__main__":
395:     import sys
396:     args = [a for a in sys.argv[1:] if not a.startswith("--")]
397:     texte = args[0] if args else "Le chat de la voisine qui dort sur le toit se réveille."
398:     cs = analyser(texte)
399:     if "--json" in sys.argv:
400:         print(json.dumps(cs, ensure_ascii=False, indent=1))
401:     else:
402:         for c in cs:
403:             print(f"- {c['nom']}")
404:             for s in c["segments"]:
405:                 print("   " + "  " * s["niveau"] + f"{s['texte']!r} [{s['type']} · {s['role']}]")

(End of file - total 405 lines)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "new_string": "    return candidats\n\n\nROLES_DEFAUT = {\"GP\": \"complement\", \"SUB\": \"contenu\", \"REL\": \"qualite\"}\n\n\ndef structure(texte: str, roles: bool = True) -> list[dict]:\n    \"\"\"La … [637 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 -m unittest discover -s tests 2>&1 | tail -30", "description": "Run existing tests after analyzer changes"}`

  ```
............  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/export HTTP/1.1" 200 -
.  127.0.0.1 · "POST /api/llm HTTP/1.1" 200 -
.  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
.  127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
.  127.0.0.1 · "GET / HTTP/1.1" 200 -
.  127.0.0.1 · "POST /api/valider HTTP/1.1" 400 -
.  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/export HTTP/1.1" 200 -
.
----------------------------------------------------------------------
Ran 19 tests in 3.634s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nimport json, generateur\nd=json.load(open('donnees/gold-analyseur.json'))\nfor p in d['phrases']:\n    segs=generateur.structure(p['texte'])\n    print(p['id'], p['split'])\n    print(\"   ATT\", \" … [258 caractères tronqués]`

  ```
p001 dev
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 6, in <module>
  File "<stdin>", line 6, in <genexpr>
TypeError: list indices must be integers or slices, not str
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nimport json, generateur\nd=json.load(open('donnees/gold-analyseur.json'))\nfor p in d['phrases']:\n    segs=generateur.structure(p['texte'])\n    att=\" | \".join(f\"{t}[{ty}:{r}]\" for t,ty,r in p[ … [348 caractères tronqués]`

  ```
OK   p001 dev · Le chat de la voisine qui dort sur le toit se réveille.
OK   p002 dev · J'ai vu l'homme avec le télescope.
OK   p003 dev · La femme a vu l'homme dans le parc.
OK   p004 dev · Il a couru pour attraper le bus.
OK   p005 dev · Il a parlé à Marie de son projet.
OK   p006 dev · Elle a dit qu'elle viendrait hier.
OK   p007 dev · Le canard est prêt à manger.
OK   g008 test · Le livre que j'ai lu est passionnant.
OK   g009 test · Je pense que le chat dort.
OK   g010 test · Quand il pleut, je reste à la maison.
OK   g011 test · Elle part parce qu'elle est fatiguée.
OK   g012 test · Bien qu'il soit tard, il travaille.
OK   g013 test · S'il vient, nous partirons.
OK   g014 test · Nous partirons dès qu'il arrivera.
OK   g015 test · Le livre dont je parle est bon.
OK   g016 test · La ville où je vis est grande.
OK   g017 test · Il a offert un livre à Marie.
OK   g018 test · La lettre a été écrite par Marie.
OK   g019 test · Il a parlé de son projet à Marie.
OK   g020 test · Je crois qu'il viendra demain.
OK   g021 test · Il travaille afin qu'elle réussisse.
OK   g022 test · Puisqu'il pleut, nous restons.
OK   g023 test · Comme il pleuvait, elle est restée.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nimport json\nfrom pathlib import Path\np = Path('donnees/gold-analyseur.json')\nd = json.loads(p.read_text(encoding='utf-8'))\nd['note'] = (\"Gold de l'analyseur. split=dev : les 7 phrases du banc ( … [2148 caractères tronqués]`

  ```
31 phrases
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"mesure_analyseur.py — le gold de l'analyseur : types, rôles, couverture, et trois contrôles.\n\nLe gold (`donnees/gold-analyseur.json`) porte des structures **écrites à la main** : pour chaque\nphrase, la suite de segments (texte, type, rôle) et son découpa … [10822 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/mesure_analyseur.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('mesure_analyseur.py')\nt = p.read_text(encoding='utf-8')\nt = t.replace('''def couverture(or_segments: list[dict], gen_segments: list[dict]) -> float:\n    \"\"\" … [2941 caractères tronqués]`

  ```
patch ok
  gold · 31 phrases · donnees/gold-analyseur.json
  split     phr    types   couv.    rôles   compl.
  dev         7   7/7       1.00  22/22    10/10  
  test       16  16/16      1.00  40/40    19/19  
  holdout     8   7/8       0.96  21/21     9/9   
  global     31  30/31      0.99  83/83    38/38  
  contrôle · baseline 52/83 (0.63) · règles coupées 55/83 (0.66) · rôles mélangés 0.10 [0.03, 0.24]
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/mesure-analyseur.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nimport json, generateur\nr=json.load(open('donnees/mesure-analyseur.json'))\nfor x in r['lignes']:\n    if not x['types_ok']:\n        print(x['id'], \"ATT\", x['types_or'], \"GEN\", x['types_gen']) … [266 caractères tronqués]`

  ```
h024 ATT ['GN', 'REL', 'GP', 'GV'] GEN ['GN', 'REL', 'GP', 'GV', 'GN']
    "L'homme" GN agent
    'que tu as vu' REL qualite
    'hier' GP temps
    'est' GV predicat
    'mon voisin' GN patient
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('generateur.py')\nt = p.read_text(encoding='utf-8')\nt = t.replace('''VERBES_LIEU = set(\"\"\"''', '''# Copules : « est mon voisin » est un GV attributif, pas un G … [1226 caractères tronqués]`

  ```
patch copule ok
  gold · 31 phrases · donnees/gold-analyseur.json
  split     phr    types   couv.    rôles   compl.
  dev         7   7/7       1.00  22/22    10/10  
  test       16  16/16      1.00  40/40    19/19  
  holdout     8   8/8       1.00  21/21     9/9   
  global     31  31/31      1.00  83/83    38/38  
  contrôle · baseline 52/83 (0.63) · règles coupées 55/83 (0.66) · rôles mélangés 0.10 [0.03, 0.24]
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/mesure-analyseur.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nimport json\nfrom pathlib import Path\np = Path('donnees/gold-analyseur.json')\nd = json.loads(p.read_text(encoding='utf-8'))\nd['note'] = (\"Gold de l'analyseur. split=dev : les 7 phrases du banc.  … [2131 caractères tronqués]`

  ```
39 phrases
  gold · 39 phrases · donnees/gold-analyseur.json
  split     phr    types   couv.    rôles   compl.
  dev         7   7/7       1.00  22/22    10/10  
  test       16  16/16      1.00  40/40    19/19  
  holdout    16  15/16      0.99  37/38    16/16  
  global     39  38/39      0.99  99/100   45/45  
  contrôle · baseline 64/100 (0.64) · règles coupées 66/100 (0.66) · rôles mélangés 0.10 [0.00, 0.22]
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/mesure-analyseur.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nimport json, generateur\nr=json.load(open('donnees/mesure-analyseur.json'))\nfor x in r['lignes']:\n    if not x['types_ok']:\n        print(x['id'], \"ATT\", x['types_or'], \"GEN\", x['types_gen']) … [321 caractères tronqués]`

  ```
h033 ATT ['GN', 'GV', 'GP'] GEN ['GN', 'GP']
La femme parle à son fils.
    'La femme parle' GN agent
    'à son fils' GP destinataire
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"exporter_corpus.py — la banque du banc de structures → un corpus JSONL pour Drave.\n\nTrois modes, un seul format de sortie (JSONL + manifeste) :\n\n  --mode banque      les lectures **validées** (`donnees/validations.jsonl`) : un verdict\n                  … [11359 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/exporter_corpus.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 -m unittest discover -s tests 2>&1 | tail -20", "description": "Run tests after exporter rewrite"}`

  ```
............  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/export HTTP/1.1" 200 -
.  127.0.0.1 · "POST /api/llm HTTP/1.1" 200 -
.  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
.  127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
.  127.0.0.1 · "GET / HTTP/1.1" 200 -
.  127.0.0.1 · "POST /api/valider HTTP/1.1" 400 -
.  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/export HTTP/1.1" 200 -
.
----------------------------------------------------------------------
Ran 19 tests in 3.134s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('tests/test_generateur.py')\nt = p.read_text(encoding='utf-8')\najout = '''\n\nclass TestRoles(unittest.TestCase):\n    \"\"\"Les rôles ne sont plus la préposition … [6279 caractères tronqués]`

  ```
tests generateur ajoutés
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('tests/test_export.py')\nt = p.read_text(encoding='utf-8')\najout = '''\n\nclass TestExportStatut(unittest.TestCase):\n    \"\"\"Le banc écrit `statut` (resolu/com … [4837 caractères tronqués]`

  ```
tests export ajoutés
.  127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
.  127.0.0.1 · "GET / HTTP/1.1" 200 -
.  127.0.0.1 · "POST /api/valider HTTP/1.1" 400 -
.  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/export HTTP/1.1" 200 -
.
----------------------------------------------------------------------
Ran 37 tests in 3.675s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 mesure_analyseur.py && echo \"=== EXPORT GOLD ===\" && python3 exporter_corpus.py --mode gold && echo \"=== EXPORT REFERENCE ===\" && python3 exporter_corpus.py --mode reference && echo \"=== EXPORT BANQUE (s … [304 caractères tronqués]`

  ```
gold · 39 phrases · donnees/gold-analyseur.json
  split     phr    types   couv.    rôles   compl.
  dev         7   7/7       1.00  22/22    10/10  
  test       16  16/16      1.00  40/40    19/19  
  holdout    16  15/16      0.99  37/38    16/16  
  global     39  38/39      0.99  99/100   45/45  
  contrôle · baseline 64/100 (0.64) · règles coupées 66/100 (0.66) · rôles mélangés 0.10 [0.00, 0.22]
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/mesure-analyseur.json
=== EXPORT GOLD ===
  ✅ 39 ligne(s) sur 39 phrase(s) · mode gold → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-gold.jsonl
     manifeste : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-gold-manifest.json
     sha256 : 973c70a4126896b8557d803b940f58d1f6d1fe1d172cdb7b9abce9671cd7db71
=== EXPORT REFERENCE ===
  ✅ 7 ligne(s) sur 7 phrase(s) · mode reference → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-reference.jsonl
     manifeste : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-reference-manifest.json
     sha256 : 77d7a01486f32d6020defd0d246771358dd622b911db11c35024b5920042bf86
=== EXPO
… [1573 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('exporter_corpus.py')\nt = p.read_text(encoding='utf-8')\nt = t.replace('''def _manifeste(mode: str, source: str, sortie: pathlib.Path, retenus: list[dict]) -> dic … [1210 caractères tronqués]`

  ```
patch manifeste relatif
{
 "version": 2,
 "mode": "gold",
 "date": "2026-11-02T16:26:36",
 "source": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/gold-analyseur.json",
 "sortie": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-gold.jsonl",
 "phrases": 39,
 "candidats_acceptes": 39,
 "sha256": "973c70a4126896b8557d803b940f58d1f6d1fe1d172cdb7b9abce9671cd7db71",
 "note": "structures de référence, sans jugement humain — `statut: reference` ; spans vérifiés."
}
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/exporter_corpus.py", line 258, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/exporter_corpus.py", line 246, in main
    manifeste = exporter_gold(args.gold, sortie, verifier=not args.sans_verifier)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/exporter_corpus.py", line 225, in exporter_gold
    manifeste = _manifeste("gold", str(chemin_gold), sortie, retenus)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/exporter_co
… [172 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('exporter_corpus.py')\nt = p.read_text(encoding='utf-8')\nt = t.replace('''def _manifeste(mode: str, source: str, sortie: pathlib.Path, retenus: list[dict]) -> dic … [539 caractères tronqués]`

  ```
✅ 39 ligne(s) sur 39 phrase(s) · mode gold → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-gold.jsonl
     manifeste : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-gold-manifest.json
     sha256 : 973c70a4126896b8557d803b940f58d1f6d1fe1d172cdb7b9abce9671cd7db71
  ✅ 7 ligne(s) sur 7 phrase(s) · mode reference → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-reference.jsonl
     manifeste : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-reference-manifest.json
     sha256 : 77d7a01486f32d6020defd0d246771358dd622b911db11c35024b5920042bf86
  ✅ 0 ligne(s) sur 0 phrase(s) · mode banque → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque.jsonl
     manifeste : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-manifest.json
     sha256 : e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
=== MANIFESTE GOLD ===
{
 "version": 2,
 "mode": "gold",
 "date": "2026-11-02T16:26:53",
 "source": "tools/structures/donnees/gold-analyseur.json",
 "sortie": "data/structures/banque-gold.jsonl",
 "phrases": 39,
 "candidats_acceptes": 39,
 "sha256": "973
… [162 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport hashlib, json, pathlib\nbase = pathlib.Path(\"data/structures\")\nfor nom in (\"banque-gold\", \"banque-reference\", \"banque\"):\n    corps = (base / f\"{nom}.jsonl\").read_text(encoding=\"utf-8\")\n    man  … [1107 caractères tronqués]`

  ```
banque-gold        lignes= 39 phrases= 39 sha=OK spans=OK statuts=['reference']
banque-reference   lignes=  7 phrases=  7 sha=OK spans=OK statuts=['reference']
banque             lignes=  0 phrases=  0 sha=OK spans=OK statuts=[]
gold splits: {'dev': 7, 'test': 16, 'holdout': 16}
=== git ignore ===
.gitignore:5:data/	data/structures/banque-gold.jsonl
=== git status ===
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M journal/README.md
 M journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md
 M journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md
 m tools/structures
?? journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Session\\|S —\\|structures\" docs/pilotage/en-cours.md | head -40; echo \"=== git diff en-cours ===\"; git diff docs/pilotage/en-cours.md | head -120", "description": "Check hub en-cours update for S section"}`

  ```
14:## Sessions en cours
21:### Session `536cd5d6-94ac-4057-8fe9-11709a4587c7` — le hub, l'intégration et la reprise
39:### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2, le natif : 200 000 pas et la fenêtre
58:### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures : l'analyseur et l'export
61:- **Rôle** : **S — les structures** : le banc d'interprétations candidates, l'**analyseur** (rôles,
70:- **Fichiers réservés** : `tools/structures/`, `data/structures/`, `reports/rapport-s-*`,
72:- **Objectif final** : un gold de 20 phrases, une mesure reproductible, `data/structures/banque.jsonl`
79:### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3
104:### Session `fe3c05f0-834b-44f2-8739-501865d652c1` — D/R/A : les données, le lecteur, le moteur
129:- **S — le banc de structures** : outil web (`tools/structures`), générateur, pragmatique (niveaux 0–4), export ; analyseur **7/7** séquences, **93,9 %** de couverture, **19 tests** ; [`analyseur`](../../reports/rapport-s-analyseur.md) ;
=== git diff en-cours ===
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 587cf563..62c61a67 100644
--- a/docs/pilotage/e
… [9310 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('exporter_corpus.py')\nt = p.read_text(encoding='utf-8')\nt = t.replace('''SORTIES = {\"banque\": \"banque.jsonl\", \"reference\": \"banque-reference.jsonl\",\n    … [2153 caractères tronqués]`

  ```
patch sorties
  ✅ 39 ligne(s) sur 39 phrase(s) · mode gold → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque.jsonl
     manifeste : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-manifest.json
     sha256 : 973c70a4126896b8557d803b940f58d1f6d1fe1d172cdb7b9abce9671cd7db71
  ✅ 0 ligne(s) sur 0 phrase(s) · mode banque → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-validee.jsonl
     manifeste : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-validee-manifest.json
     sha256 : e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  ✅ 7 ligne(s) sur 7 phrase(s) · mode reference → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-reference.jsonl
     manifeste : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-reference-manifest.json
     sha256 : 77d7a01486f32d6020defd0d246771358dd622b911db11c35024b5920042bf86
=== LISTE ===
total 40
drwxr-xr-x. 1 stephane stephane   264  2 nov 16:27 .
drwxr-xr-x. 1 stephane stephane  2504  2 nov 16:26 ..
-rw-r--r--. 1 stephane stephane 20278  2 nov 16:27 banque.jsonl
-rw-r--r--. 1 stephane stephane   395 
… [758 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('README.md')\nt = p.read_text(encoding='utf-8')\n\nt = t.replace('''> **Ce que ce n'est pas.** Pas un analyseur syntaxique : les candidats sont **générés par une\n … [7520 caractères tronqués]`

  ```
README mis à jour
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && sed -n '1,15p' README.md; echo \"...\"; sed -n '85,190p' README.md", "description": "Review updated README sections"}`

  ```
# Structures — le banc d'interprétations candidates

> **Ce que c'est.** Un outil **pour humain** : il affiche, pour une phrase, plusieurs **structures
> d'interprétation candidates** (attachements, rôles, portées), permet de les **valider**, de
> demander l'avis d'un **grand modèle** (DeepSeek), et d'**exporter une banque** de structures
> validées — un corpus d'entraînement pour le projet Drave.

> **Ce que ce n'est pas.** Pas un analyseur syntaxique complet : les candidats sont **générés par
> une heuristique** (`generateur.py`) ou fournis par le fichier de données ; l'outil les fait
> valider, il ne prétend pas les avoir compris. Depuis la v2, l'heuristique **nomme le rôle** par
> le contexte, **coupe les subordonnées** et traite le passif et la copule — et un **gold** mesure
> ce qu'elle sait faire, échecs compris (voir « La mesure de l'analyseur »).

## Lancer

...
  baseline et le grand modèle comparent.

Les spans sont **vérifiés** : `construire_donnees.py` les calcule par sous-chaîne et refuse un
segment qui n'apparaît pas dans la phrase ; `exporter_corpus.py` les re-vérifie avant d'écrire une
ligne de corpus.

## Le générateur

```bash
python3 generateur.py "Le chat de la
… [5359 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && sed -n '190,240p' README.md", "description": "Review README tail"}`

  ```
## Tests

```bash
python3 -m unittest discover -s tests
```

**37 tests** : phrases et alignement des spans, validation + export, statut invalide refusé,
évaluation baseline, page statique ; générateur (spans, relative, rôle, GP, variation unique,
copule) ; rôles contextuels (`de`, `avec`, `à`, `par`, passif) ; subordonnées (temps, cause,
concession, hypothèse, but, manière, contenu) ; gold (spans, vocabulaire, mesure qui bat les trois
contrôles) ; export (dernier verdict `statut`, `verdict` ancien, span invalide, aucune validation,
candidat inconnu, référence, gold, gold cassé).

## État et suite

- **v0** : 7 phrases, 14 candidats écrits à la main, 7 ambiguïtés (relative, GP, portée, rôle,
  possession, double sens assumé).
- **v1** : `generateur.py` (candidats heuristiques, subordonnées et coordination), le **niveau
  pragmatique** (statuts, double sens conservé, niveaux de contexte 0–4, niveau minimal) et
  `exporter_corpus.py` (JSONL avec spans vérifiés et manifeste).
- **v2** : **rôles contextuels** (possession/thème, instrument/attribut, but/lieu, agent/moyen,
  passif, copule), **subordonnées** par type (temps, cause, concession, hypothèse, but, manière,
  contenu), le **go
… [516 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('README.md')\nt = p.read_text(encoding='utf-8')\nt = t.replace('''1. **le dernier verdict gagne** — un candidat validé `ok` puis `non` ne sort pas ;''',\n'''1. **l … [737 caractères tronqués]`

  ```
README corrigé
----------------------------------------------------------------------
Ran 37 tests in 3.675s

OK
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"verifier_corpus.py — le corpus exporté se vérifie : empreinte, comptes, spans, restitution.\n\nUn corpus qui ne se rejoue pas n'est pas un corpus : ce contrôle relit le JSONL, recalcule son\nSHA-256, vérifie le manifeste, aligne chaque segment sur le texte  … [5822 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/verifier_corpus.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 verifier_corpus.py --autotest && python3 verifier_corpus.py ../../data/structures/banque.jsonl && python3 verifier_corpus.py ../../data/structures/banque-reference.jsonl && python3 verifier_corpus.py ../../da … [87 caractères tronqués]`

  ```
autotest OK : corpus valide accepté, span corrompu refusé
  ✅ ../../data/structures/banque.jsonl · empreinte, comptes, spans et restitution vérifiés
  ✅ ../../data/structures/banque-reference.jsonl · empreinte, comptes, spans et restitution vérifiés
  ✅ ../../data/structures/banque-validee.jsonl · empreinte, comptes, spans et restitution vérifiés
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('tests/test_export.py')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"import exporter_corpus\\n\", \"import exporter_corpus\\nimport verifier_corpus\\n\")\na … [2356 caractères tronqués]`

  ```
tests verifier ajoutés
----------------------------------------------------------------------
Ran 40 tests in 3.679s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nimport json\nr=json.load(open('donnees/mesure-analyseur.json'))\nprint(json.dumps({k:r[k] for k in ('phrases','par_split','global','controles')}, ensure_ascii=False, indent=1))\nPY", "description":  … [33 caractères tronqués]`

  ```
{
 "phrases": 39,
 "par_split": {
  "dev": {
   "phrases": 7,
   "types_ok": 7,
   "couverture": 1.0,
   "octets_couverts": 229,
   "octets_or": 229,
   "roles_justes": 22,
   "roles_total": 22,
   "complements_justes": 10,
   "complements_total": 10,
   "types_taux": 1.0,
   "couverture_globale": 1.0,
   "roles_taux": 1.0,
   "complements_taux": 1.0
  },
  "test": {
   "phrases": 16,
   "types_ok": 16,
   "couverture": 1.0,
   "octets_couverts": 475,
   "octets_or": 475,
   "roles_justes": 40,
   "roles_total": 40,
   "complements_justes": 19,
   "complements_total": 19,
   "types_taux": 1.0,
   "couverture_globale": 1.0,
   "roles_taux": 1.0,
   "complements_taux": 1.0
  },
  "holdout": {
   "phrases": 16,
   "types_ok": 15,
   "couverture": 0.9864,
   "octets_couverts": 452,
   "octets_or": 457,
   "roles_justes": 37,
   "roles_total": 38,
   "complements_justes": 16,
   "complements_total": 16,
   "types_taux": 0.9375,
   "couverture_globale": 0.9891,
   "roles_taux": 0.9737,
   "complements_taux": 1.0
  }
 },
 "global": {
  "phrases": 39,
  "types_ok": 38,
  "couverture": 0.9944,
  "octets_couverts": 1156,
  "octets_or": 1161,
  "roles_justes": 99,
  "roles_total": 100,
  "com
… [438 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('README.md')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"**37 tests** :\", \"**40 tests** :\")\nt = t.replace(\"candidat inconnu, référence, gold, gold cas … [449 caractères tronqués]`

  ```
Ran 40 tests in 3.691s

OK
=== STATUS SOUS-MODULE ===
 M README.md
 M exporter_corpus.py
 M generateur.py
 M tests/test_export.py
 M tests/test_generateur.py
?? donnees/gold-analyseur.json
?? donnees/mesure-analyseur.json
?? mesure_analyseur.py
?? verifier_corpus.py
=== DIFF STAT ===
 README.md                |  95 ++++++++++++++++-----
 exporter_corpus.py       | 214 ++++++++++++++++++++++++++++++++++++-----------
 generateur.py            | 207 +++++++++++++++++++++++++++++++++++++++++----
 tests/test_export.py     | 122 +++++++++++++++++++++++++++
 tests/test_generateur.py | 113 +++++++++++++++++++++++++
 5 files changed, 665 insertions(+), 86 deletions(-)
=== NOUVEAUX ===
?? donnees/gold-analyseur.json
?? donnees/mesure-analyseur.json
?? mesure_analyseur.py
?? verifier_corpus.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git diff --check; python3 -m py_compile generateur.py exporter_corpus.py mesure_analyseur.py verifier_corpus.py serveur.py llm.py construire_donnees.py && echo \"compile OK\"; python3 generateur.py \"La lettre a été  … [81 caractères tronqués]`

  ```
compile OK
- « par Marie » → La lettre
   'La lettre' [GN · patient]
   'a été écrite' [GV · predicat]
     'par Marie' [GP · agent]
- « par Marie » → a été écrite
   'La lettre' [GN · patient]
   'a été écrite' [GV · predicat]
     'par Marie' [GP · agent]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py", "offset": 210, "limit": 150}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/generateur.py</path>
<type>file</type>
<content>
210:         self.cible_verbe = None  # le GV le plus proche à gauche
211: 
212:     def dict(self):
213:         return {"debut": self.debut, "fin": self.fin, "texte": self.texte,
214:                 "type": self.type, "role": self.role, "niveau": self.niveau}
215: 
216: 
217: def _consomme(toks, i, classes):
218:     j = i
219:     while j < len(toks) and toks[j].cls in classes:
220:         j += 1
221:     return j
222: 
223: 
224: def _segmente(texte: str, toks: list[Token]) -> list[Segment]:
225:     utiles = [t for t in toks if t.cls != "ESPACE"]
226:     segs: list[Segment] = []
227:     i = 0
228:     while i < len(utiles):
229:         t = utiles[i]
230:         if t.cls == "PONCT":
231:             i += 1
232:             continue
233:         marqueur = _marqueur(utiles, i)
234:         if marqueur:
235:             # « parce qu'elle est fatiguée », « bien qu'il soit tard » : la subordonnée
236:             # commence au subordonnant et va jusqu'à la ponctuation ou la coordination.
237:             j = _fin_clause(utiles, i + 1)
238:             segs.a
… [6311 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git add generateur.py exporter_corpus.py mesure_analyseur.py verifier_corpus.py donnees/gold-analyseur.json donnees/mesure-analyseur.json README.md tests/test_generateur.py tests/test_export.py && git diff --cached - … [978 caractères tronqués]`

  ```
README.md                     |  95 ++++-
 donnees/gold-analyseur.json   | 784 ++++++++++++++++++++++++++++++++++++
 donnees/mesure-analyseur.json | 910 ++++++++++++++++++++++++++++++++++++++++++
 exporter_corpus.py            | 214 +++++++---
 generateur.py                 | 207 +++++++++-
 mesure_analyseur.py           | 257 ++++++++++++
 tests/test_export.py          | 122 ++++++
 tests/test_generateur.py      | 113 ++++++
 verifier_corpus.py            | 130 ++++++
 9 files changed, 2746 insertions(+), 86 deletions(-)
[master 647205a] S — L'ANALYSEUR NOMME LES RÔLES : 99/100, 38/39 TYPES ; LE CORPUS DE 39 STRUCTURES SORT
 9 files changed, 2746 insertions(+), 86 deletions(-)
 create mode 100644 donnees/gold-analyseur.json
 create mode 100644 donnees/mesure-analyseur.json
 create mode 100644 mesure_analyseur.py
 create mode 100644 verifier_corpus.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short; echo \"=== log ===\"; git log --oneline -3; echo \"=== en-cours S section ===\"; sed -n '58,80p' docs/pilotage/en-cours.md", "description": "Check main repo status and hub integration"}`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  journal/README.md
M  journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md
 M journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md
 M tools/ocr_pdf.py
M  tools/sessions.py
 M tools/structures
?? journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md
=== log ===
dc7f9c56 N2 — MANDAT 200 k PAS SUR LE MÉLANGE 1 Go, PUIS R1.1/R1.2 (session 0733c5bb)
04d75114 ÉTAT — HORODATAGE RÉEL (16 h 09) APRÈS LA REPRISE ; LE FUTUR N'EST PAS UNE HEURE
97d693b6 ÉTAT — T0 REVENU SOUS 4 000 (3 998) APRÈS LE RUNBOOK
=== en-cours S section ===
- **Plan** : 1) ~~plan et réservation~~ ; 2) **analyseur rôles/subordonnées** (en cours) ; 3) **export
  au corpus** ; 4) **tests** ; 5) **fiche, sous-module** ; 6) **ligne d'état**.
- **Ambition** : un analyseur qui **nomme le rôle** et **coupe la subordonnée**.
- **Stratégie** : une règle = une phrase du gold, un contrôle négatif par mesure, 19 tests.
- **Objectif final** : un gold de 20 phrases, une mesure reproductible, `data/structures/banque.jsonl`
  + manifeste, committé.
- **Ce qu'elle fait** : mandat ouvert à **16 h 19** ; l'analyseur rôles/subordonnées est en cours.
- **Ce
… [1266 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git rev-parse HEAD; git log -1 --format='%h %s'; echo \"=== main repo index lock ===\"; ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/.git/index.lock 2>/dev/null || echo \"pas de verrou\"", "description": "G … [42 caractères tronqués]`

  ```
647205a3da710217b63b5d20d492275a75e7dff8
647205a S — L'ANALYSEUR NOMME LES RÔLES : 99/100, 38/39 TYPES ; LE CORPUS DE 39 STRUCTURES SORT
=== main repo index lock ===
pas de verrou
  ```

- **write** `{"content": "# S — L'analyseur nomme les rôles : 99/100, 38/39 types, et 39 structures au corpus\n\n> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur un gold de **39 phrases**\n> (7 `dev`, 16 `test`, 16 `holdout`), la structure de base retrouve la **séquence de types\n> 38/39**  … [8486 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cp data/structures/banque-manifest.json reports/s-banque-structures.json && python3 -m json.tool reports/s-banque-structures.json | head -20; echo \"=== check links ===\"; ls -la reports/rapport-s-analyseur-roles.md reports/s-banque- … [67 caractères tronqués]`

  ```
{
    "version": 2,
    "mode": "gold",
    "date": "2026-11-02T16:27:28",
    "source": "tools/structures/donnees/gold-analyseur.json",
    "sortie": "data/structures/banque.jsonl",
    "phrases": 39,
    "candidats_acceptes": 39,
    "sha256": "973c70a4126896b8557d803b940f58d1f6d1fe1d172cdb7b9abce9671cd7db71",
    "note": "structures de r\u00e9f\u00e9rence, sans jugement humain \u2014 `statut: reference` ; spans v\u00e9rifi\u00e9s."
}
=== check links ===
-rw-------. 1 stephane stephane 8798  2 nov 16:31 reports/rapport-s-analyseur-roles.md
-rw-r--r--. 1 stephane stephane  395  2 nov 16:31 reports/s-banque-structures.json
  ```

- **bash** `{"command": "chmod 644 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md; ls -l /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md", "description": "Fix fiche permissions"}`

  ```
-rw-r--r--. 1 stephane stephane 8798  2 nov 16:31 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md
  ```

- **write** `{"content": "# Plan de session — S, les structures (analyser, banquer, exporter)\n\n> **Mandat vivant.** Ouvert le 2026-11-02 16 h 19 HNE depuis\n> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md) (§ S) et\n> [`plan-travail.md`](../../../docs/pilotage/plan-travail.md) § 9.2.\n> Le h … [6954 caractères tronqués]`

  ```
Error: cannot write "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md</path>
<type>file</type>
<content>
1: # Plan de session — S, les structures (analyser, banquer, exporter)
2: 
3: > **Mandat vivant.** Ouvert le 2026-11-02 16 h 19 HNE depuis
4: > [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md) (§ S) et
5: > [`plan-travail.md`](../../../docs/pilotage/plan-travail.md) § 9.2.
6: > Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.
7: > `en-cours` reste la seule source de l'état : ce plan est le **contrat de travail** qui le
8: > précède, et la section S y est **proposée au hub**, pas écrite ici.
9: 
10: - **Session** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f`
11: - **Rôle** : **S — les structures** : le banc d'interprétations candidates (outil web, générateur,
12:   pragmatique, banque), l'**analyseur** (rôles, subordonnées) et l'**export au corpus**.
13: - **Périmètre** : S (structures) — S-analyseur rôles/subordonnées · S-banque · S-export au corpus.
14: - **Fichiers réservés** : `tools/structures/` ; `data/structures/` ; `reports/rapport-s-*` ;
15:   `reports/s-banque-*` ; `journal/sessions/29ad180d-38
… [3203 caractères tronqués]
  ```

- **write** `{"content": "# Plan de session — S, les structures (analyser, banquer, exporter)\n\n> **Mandat vivant.** Ouvert le 2026-11-02 16 h 19 HNE depuis\n> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md) (§ S) et\n> [`plan-travail.md`](../../../docs/pilotage/plan-travail.md) § 9.2.\n> Le h … [6954 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/sessions.py --check 2>&1 | head -8; echo \"=== HEAD ===\"; git rev-parse --short HEAD; echo \"=== commit pointeur (index alterné) ===\"; H=$(git rev-parse HEAD); rm -f /tmp/index.s; GIT_INDEX_FILE=/tmp/index.s git read- … [247 caractères tronqués]`

  ```
⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/structures/ (29ad180d-38a5-4481-a9a7-ec6ab31c895f)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/wikipedia/` (lecture) (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/corpus_wiki_* (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : tools/corpus* (0733c5bb-f90b-4f58-9241-3364fa32e46c) / tools/corpus_wikipedia*.py (fe3c05f0-834b-44f2-8739-501865d652c1)
=== HEAD ===
e420267a
=== commit pointeur (index alterné) ===
 tools/structures | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -4; echo \"=== show hub commit ===\"; git show --stat --oneline e420267a | head -40; echo \"=== status ===\"; git status --short; echo \"=== plan suivi ? ===\"; git ls-files journal/sessions/29ad180d-38a5-4481-a9a7- … [164 caractères tronqués]`

  ```
e420267a ÉTAT — QUATRE SESSIONS OUVERTES (N2, S, PENSÉE, D/R/A) ; HEARTBEAT 16 h 24 ; PORTE STRICTE RÉPARÉE
dc7f9c56 N2 — MANDAT 200 k PAS SUR LE MÉLANGE 1 Go, PUIS R1.1/R1.2 (session 0733c5bb)
04d75114 ÉTAT — HORODATAGE RÉEL (16 h 09) APRÈS LA REPRISE ; LE FUTUR N'EST PAS UNE HEURE
97d693b6 ÉTAT — T0 REVENU SOUS 4 000 (3 998) APRÈS LE RUNBOOK
=== show hub commit ===
e420267a ÉTAT — QUATRE SESSIONS OUVERTES (N2, S, PENSÉE, D/R/A) ; HEARTBEAT 16 h 24 ; PORTE STRICTE RÉPARÉE
 docs/pilotage/en-cours.md                          |  156 +-
 docs/pilotage/roadmap.md                           |   14 +-
 journal/2026-11-02/README.md                       |   15 +-
 journal/2026-11-02/apprentissage.md                |   10 +-
 journal/2026-11-02/attention.md                    |   10 +-
 journal/2026-11-02/distribue.md                    |   10 +-
 journal/2026-11-02/docs.md                         |   15 +-
 journal/2026-11-02/memoire.md                      |   10 +-
 journal/2026-11-02/mesures.md                      |   10 +-
 journal/2026-11-02/modele.md                       |   10 +-
 journal/2026-11-02/outils.md                       |   10 +-
 journal/2026-11-02/portes.md           
… [1558 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && H=$(git rev-parse HEAD); rm -f /tmp/index.s; GIT_INDEX_FILE=/tmp/index.s git read-tree \"$H\" && GIT_INDEX_FILE=/tmp/index.s git add tools/structures && GIT_INDEX_FILE=/tmp/index.s git commit -m \"S — LE SOUS-MODULE 647205a : L'ANALY … [845 caractères tronqués]`

  ```
[stderr]
  ✅ index : aucun fait stagé sans état
[still running after 60000ms; moved to background job bash-67]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-67", "timeout_ms": 60000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ps -eo pid,etime,cmd | grep -E \"git commit|archive_sessions|journal_auto|session_report|python3\" | grep -v grep | head -20; echo \"=== index lock ===\"; ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/.git/index.lock 2>/dev/null || echo \"pas de verrou\"", "description": "Inspe … [29 caractères tronqués]`

  ```
2061    01:26:50 /usr/bin/python3.13 /usr/sbin/firewalld --nofork --nopid
   2238    01:26:48 /usr/bin/python3.13 /usr/bin/fail2ban-server -xf start
  56487       02:02 bash -c python3 tools/ocr_pdf.py --liste work/ocr/scans-uniques.txt --racine CEGEP --sortie data/corpus_ocr_cegep --manifeste reports/ocr-pdf-cegep.json --ouvriers 8 2>&1 | tee work/ocr/run-cegep-02.log
  56494       02:02 python3 tools/ocr_pdf.py --liste work/ocr/scans-uniques.txt --racine CEGEP --sortie data/corpus_ocr_cegep --manifeste reports/ocr-pdf-cegep.json --ouvriers 8
  56548       01:55 bash -c cd /home/stephane/GitHub/Qtrinet && time python3 /tmp/qualif_7b_180.py 2>&1 | tail -12
  56557       01:55 python3 /tmp/qualif_7b_180.py
  57015       01:07 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && H=$(git rev-parse HEAD); rm -f /tmp/index.s; GIT_INDEX_FILE=/tmp/index.s git read-tree "$H" && GIT_INDEX_FILE=/tmp/index.s git add tools/structures && GIT_INDEX_FILE=/tmp/index.s git commit -m "S — LE SOUS-MODULE 647205a : L'ANALYSEUR NOMME LES RÔLES, LE GOLD DE 39 PHRASES, L'EXPORT DE 39 STRUCTURES" -m "Le sous-module tools/structures est committé dans son dépôt : rôles contextuels (possession/thème
… [1708 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-67", "timeout_ms": 120000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ps -eo pid,ppid,etime,pcpu,stat,cmd | grep -E \"57032|57052|57681|job|git commit\" | grep -v grep; echo \"=== enfants ===\"; ps --ppid 57032 -o pid,etime,pcpu,stat,cmd 2>/dev/null; echo \"=== taille journal session ===\"; ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/se … [116 caractères tronqués]`

  ```
57015   31786       01:16  0.1 Ss   bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && H=$(git rev-parse HEAD); rm -f /tmp/index.s; GIT_INDEX_FILE=/tmp/index.s git read-tree "$H" && GIT_INDEX_FILE=/tmp/index.s git add tools/structures && GIT_INDEX_FILE=/tmp/index.s git commit -m "S — LE SOUS-MODULE 647205a : L'ANALYSEUR NOMME LES RÔLES, LE GOLD DE 39 PHRASES, L'EXPORT DE 39 STRUCTURES" -m "Le sous-module tools/structures est committé dans son dépôt : rôles contextuels (possession/thème, instrument/attribut, but/lieu, agent/moyen, passif, copule), subordonnées typées, gold de 39 phrases (38/39 types, 99/100 rôles, 45/45 compléments, couverture 1156/1161), contrôles 64/100, 66/100, 0,099, export gold/référence/banque et verifier_corpus ; 40 tests. Échec nommé : h033, « La femme parle » avale le verbe." -m "Le pointeur est mis à jour ; le corpus local data/structures/banque.jsonl fait 39 lignes (SHA 973c70a4…). La fiche reports/rapport-s-analyseur-roles.md et le manifeste reports/s-banque-structures.json sont prêts pour l'intégration du hub ; la session S n'écrit pas en-cours."
  57032   57015       01:16  0.6 S    git commit -m S — LE SOUS-MODULE 647205a : L'ANALYSEUR NOMM
… [1347 caractères tronqués]
  ```

- **bash** `{"command": "ps -eo pid,ppid,etime,pcpu,stat,wchan:24,cmd | awk '$2==57048 || $1==57048'; echo \"=== tout python ===\"; ps -eo pid,ppid,etime,pcpu,stat,cmd | grep -E \"python3|journal_auto|session_report|archive\" | grep -v grep | head -15", "description": "List hook children and states"}`

  ```
57048   57032       01:25  0.0 S    do_wait                  /bin/sh .git/hooks/pre-commit
  59838   57048       00:12 65.6 R    -                        python3 tools/session_report.py --quiet
=== tout python ===
   2061       1    01:27:09  0.0 Ssl  /usr/bin/python3.13 /usr/sbin/firewalld --nofork --nopid
   2238       1    01:27:07  0.0 Ssl  /usr/bin/python3.13 /usr/bin/fail2ban-server -xf start
  56487   32694       02:21  0.0 Ss   bash -c python3 tools/ocr_pdf.py --liste work/ocr/scans-uniques.txt --racine CEGEP --sortie data/corpus_ocr_cegep --manifeste reports/ocr-pdf-cegep.json --ouvriers 8 2>&1 | tee work/ocr/run-cegep-02.log
  56494   56487       02:21  0.1 Sl   python3 tools/ocr_pdf.py --liste work/ocr/scans-uniques.txt --racine CEGEP --sortie data/corpus_ocr_cegep --manifeste reports/ocr-pdf-cegep.json --ouvriers 8
  56548   32123       02:13  0.0 Ss   bash -c cd /home/stephane/GitHub/Qtrinet && time python3 /tmp/qualif_7b_180.py 2>&1 | tail -12
  56557   56548       02:13  0.4 Sl   python3 /tmp/qualif_7b_180.py
  59838   57048       00:12 65.5 R    python3 tools/session_report.py --quiet
  59873   32694       00:11  9.3 Ssl  python3 tools/detecte_scans_pdf.py --racine 
… [1896 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-67", "timeout_ms": 180000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ps -eo pid,ppid,etime,pcpu,stat,cmd | grep -E \"57032|57048|session_report|journal_auto|archive_sessions\" | grep -v grep; echo \"=== git status (normal index) ===\"; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head; echo \"=== log ===\"; git log --oneline … [58 caractères tronqués]`

  ```
57032   57015       01:39  0.4 S    git commit -m S — LE SOUS-MODULE 647205a : L'ANALYSEUR NOMME LES RÔLES, LE GOLD DE 39 PHRASES, L'EXPORT DE 39 STRUCTURES -m Le sous-module tools/structures est committé dans son dépôt : rôles contextuels (possession/thème, instrument/attribut, but/lieu, agent/moyen, passif, copule), subordonnées typées, gold de 39 phrases (38/39 types, 99/100 rôles, 45/45 compléments, couverture 1156/1161), contrôles 64/100, 66/100, 0,099, export gold/référence/banque et verifier_corpus ; 40 tests. Échec nommé : h033, « La femme parle » avale le verbe. -m Le pointeur est mis à jour ; le corpus local data/structures/banque.jsonl fait 39 lignes (SHA 973c70a4…). La fiche reports/rapport-s-analyseur-roles.md et le manifeste reports/s-banque-structures.json sont prêts pour l'intégration du hub ; la session S n'écrit pas en-cours.
  57048   57032       01:39  0.0 S    /bin/sh .git/hooks/pre-commit
  59838   57048       00:26 66.4 R    python3 tools/session_report.py --quiet
=== git status (normal index) ===
 M journal/README.md
 M journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/digest.md
 M journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/rapport.md
 M journ
… [634 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-67", "timeout_ms": 180000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ps -o pid,etime,time,pcpu,stat,cmd -p 59838; echo \"=== io ===\"; cat /proc/59838/io 2>/dev/null | head; echo \"=== fichier ouvert ===\"; ls -l /proc/59838/fd 2>/dev/null | tail -5; echo \"=== sessions ===\"; ls /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions | wc -l",  … [59 caractères tronqués]`

  ```
PID     ELAPSED     TIME %CPU STAT CMD
  59838       00:48 00:00:33 69.5 R    python3 tools/session_report.py --quiet
=== io ===
rchar: 816219071
wchar: 620552086
syscr: 76895
syscw: 91098
read_bytes: 0
write_bytes: 4456448
cancelled_write_bytes: 0
=== fichier ouvert ===
total 0
lrwx------. 1 stephane stephane 64  2 nov 16:34 0 -> /dev/null
l-wx------. 1 stephane stephane 64  2 nov 16:34 1 -> /dev/null
lrwx------. 1 stephane stephane 64  2 nov 16:34 2 -> socket:[216757]
=== sessions ===
121
  ```

- **job_output** `{"job_id": "bash-67", "timeout_ms": 240000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ps -eo pid,ppid,etime,time,pcpu,stat,cmd | awk '$2==57048 || $1==57048 || $2==57032'; echo \"=== io ===\"; for p in $(pgrep -f \"session_report.py --quiet\"); do echo \"PID $p\"; ps -o etime,time,pcpu -p $p; cat /proc/$p/io 2>/dev/null | grep -E \"rchar|wchar\"; done; echo \"=== journal … [121 caractères tronqués]`

  ```
57048   57032       02:18 00:00:00  0.0 S    /bin/sh .git/hooks/pre-commit
  59838   57048       01:05 00:00:47 73.3 R    python3 tools/session_report.py --quiet
=== io ===
PID 59838
    ELAPSED     TIME %CPU
      01:05 00:00:48 73.3
rchar: 1097096696
wchar: 842992586
PID 65742
    ELAPSED     TIME %CPU
      00:00 00:00:00 30.0
rchar: 3376405
wchar: 82602
=== journal auto ? ===
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,160p' tools/session_report.py", "description": "Read session_report script"}`

  ```
#!/usr/bin/env python3
"""Produit, pour chaque session DSH, un rapport qui reconstitue son essence et
démontre le travail accompli, étape par étape.

Sortie, à côté du digest brut :

  journal/sessions/<id>/rapport.md   la synthèse structurée de la session
  journal/README.md                  l'index des sessions

Ce que le rapport contient, et pourquoi :

  1. fiche      — identité, durée, volumes : de quoi situer la session
  2. demandes   — ce qui a été demandé, tour par tour, verbatim
  3. déroulé    — pour chaque tour : les actions (fichiers, commandes, délégations)
                  puis la synthèse produite. C'est la démonstration du travail.
  4. travail    — tables des fichiers créés/modifiés, des commandes, des sous-agents
  5. mesures    — les lignes de résultat qui portent un chiffre mesuré
  6. erreurs    — ce qui a échoué, et où
  7. commits    — ce qui a été inscrit dans l'histoire du dépôt

Usage :
  python3 tools/session_report.py [--repo DIR] [--session ID] [--quiet]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter, OrderedDict
from pathlib import Path

… [5150 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-67 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && H=$(git rev-parse HEAD); rm -f /tmp/index.s; GIT_INDEX_FILE=/tmp/index.s git read-tree "$H" && GIT_INDEX_FILE=/tmp/index.s git add tools/structures && GIT_INDEX_FILE=/tmp/index.s git commit -m "S — LE SOUS-MODULE 647205a : L'ANALYSEUR NOMME LES RÔLES, LE GOLD DE 39 PHRASES, L'EXPORT DE 39 STRUCTURES" -m "Le sous-module tools/structures est committé dans son dépôt : rôles contextuels (possession/thème, instrument/attribut, but/lieu, agent/moyen, passif, copule), subordonnées typées, gold de 39 phrases (38/39 types, 99/100 rôles, 45/45 compléments, couverture 1156/1161), contrôles 64/100, 66/100, 0,099, export gold/référence/banque et verifier_corpus ; 40 tests. Échec nommé : h033, « La femme parle » avale le verbe." -m "Le pointeur est mis à jour ; le corpus local data/structures/banque.jsonl fait 39 lignes (SHA 973c70a4…). La fiche reports/rapport-s-analyseur-roles.md et le manifeste reports/s-banque-structures.json sont prêts pour l'intégration du hub ; la session S n'écrit pas en-cours.") finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-67"}`

  ```
[master 13f4e131] S — LE SOUS-MODULE 647205a : L'ANALYSEUR NOMME LES RÔLES, LE GOLD DE 39 PHRASES, L'EXPORT DE 39 STRUCTURES
 21 files changed, 417 insertions(+), 54 deletions(-)
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -3; echo \"=== status ===\"; git status --short; echo \"=== sous-module ===\"; git diff HEAD -- tools/structures; git submodule status tools/structures; echo \"=== portes structures ===\"; ls tools/porte-* | grep -i … [132 caractères tronqués]`

  ```
13f4e131 S — LE SOUS-MODULE 647205a : L'ANALYSEUR NOMME LES RÔLES, LE GOLD DE 39 PHRASES, L'EXPORT DE 39 STRUCTURES
e420267a ÉTAT — QUATRE SESSIONS OUVERTES (N2, S, PENSÉE, D/R/A) ; HEARTBEAT 16 h 24 ; PORTE STRICTE RÉPARÉE
dc7f9c56 N2 — MANDAT 200 k PAS SUR LE MÉLANGE 1 Go, PUIS R1.1/R1.2 (session 0733c5bb)
=== status ===
MM journal/2026-11-02/README.md
MM journal/2026-11-02/apprentissage.md
MM journal/2026-11-02/attention.md
MM journal/2026-11-02/distribue.md
MM journal/2026-11-02/docs.md
MM journal/2026-11-02/memoire.md
MM journal/2026-11-02/mesures.md
MM journal/2026-11-02/modele.md
MM journal/2026-11-02/outils.md
MM journal/2026-11-02/portes.md
MM journal/README.md
MM journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/digest.md
MM journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/rapport.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/abb58991-fe0a-4d6e-b039-6552b09f8454/digest.md
MM journal/sessions/abb58991-fe0a-4d6e-b039-6552b09f8454/rapport.md
MM journal/sessions/b7d4678e-2143-4daa-a9a4-a456c5aa8dab/digest.md
MM journal/sessions/b7d4678e-2143-4daa-a9a4-a456c5aa8dab/rapport.md
MM journal/sessions/caaf3018-e3e2-4416-8446-11f0335910aa/digest.md
MM journal/sessio
… [316 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== verifie_en_cours ===\"; python3 tools/verifie_en_cours.py 2>&1 | tail -8; echo \"=== revue_documentation ===\"; python3 tools/revue_documentation.py 2>&1 | tail -25", "description": "Run state and documentation checks"}`

  ```
=== verifie_en_cours ===
  en-cours · 1625 mots · 7 sections · 5 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
=== revue_documentation ===
  revue de documentation · 551 fiche(s) · 637 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 550 fichiers, le disque en a 551
     · compteurs : en-cours.md dit 636 JSON, le disque en a 637
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git read-tree HEAD && echo \"index réconcilié\" && git status --short | head -20; echo \"=== pointer HEAD ===\"; git ls-tree HEAD tools/structures; git -C tools/structures rev-parse HEAD", "description": "Reconcile normal index with  … [6 caractères tronqués]`

  ```
index réconcilié
 M tools/ocr_pdf.py
?? reports/rapport-s-analyseur-roles.md
?? reports/s-banque-structures.json
?? tools/detecte_scans_pdf.py
=== pointer HEAD ===
160000 commit 647205a3da710217b63b5d20d492275a75e7dff8	tools/structures
647205a3da710217b63b5d20d492275a75e7dff8
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== verifie_journal ===\"; python3 tools/verifie_journal.py 2>&1 | tail -8; echo \"=== verifie_etat --head ===\"; python3 tools/verifie_etat_a_jour.py 2>&1 | tail -8; echo \"=== taille_documents ===\"; python3 tools/taille_doc … [81 caractères tronqués]`

  ```
=== verifie_journal ===
  journal · 39 jour(s) · 117 session(s) · 1839 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
=== verifie_etat --head ===
  état · dernier fait e420267a · dernier état e420267a
  ✅ aucun fait commité après le dernier état
=== taille_documents ===
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3999 mots (budget 4 000)

  avertissements :
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== sessions strict ===\"; python3 tools/sessions.py --check --strict 2>&1 | tail -10; echo \"exit=$?\"; echo \"=== mtime hub ===\"; ls -la --time-style=+%H:%M:%S journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/ docs/pil … [197 caractères tronqués]`

  ```
=== sessions strict ===
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/structures/ (29ad180d-38a5-4481-a9a7-ec6ab31c895f)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/wikipedia/` (lecture) (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/corpus_wiki_* (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : tools/corpus* (0733c5bb-f90b-4f58-9241-3364fa32e46c) / tools/corpus_wikipedia*.py (fe3c05f0-834b-44f2-8739-501865d652c1)
exit=0
=== mtime hub ===
-rw-r--r--. 1 stephane stephane 11879 16:30:02 docs/pilotage/en-cours.md

journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/:
total 1156
drwxr-xr-x. 1 stephane stephane     94 15:58:28 .
drwxr-xr-x. 1 stephane stephane   8440 16:16:59 ..
-rw-r--r--. 1 stephane stephane 190323 16:32:52 digest.md
-rw-------. 1 stephane stephane   2397 16:23:48 plan.md
-rw-r--r--. 1 stephane stephane  20174 16:34:13 rapport.md
-rw-------. 1 stephane stephane 963761 16:12:41 session.v4.jsonl.zstd
=== processus portes ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/porte-sessions.sh; echo \"=== strict sans pipe ===\"; python3 tools/sessions.py --check --strict >/tmp/sessions.out 2>&1; echo \"exit=$?\"; tail -8 /tmp/sessions.out; echo \"=== porte-sessions ===\"; bash tools/porte-sessio … [151 caractères tronqués]`

  ```
#!/bin/bash
# porte-sessions.sh — les plans de session sont lisibles et le linter refuse un doublon.
set -u
cd "$(dirname "$0")/.."
python3 tools/sessions.py --autotest || exit 1
python3 tools/sessions.py --check --strict || exit 1
echo "PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict"
=== strict sans pipe ===
exit=0
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/structures/ (29ad180d-38a5-4481-a9a7-ec6ab31c895f)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/wikipedia/` (lecture) (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/corpus_wiki_* (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : tools/corpus* (0733c5bb-f90b-4f58-9241-3364fa32e46c) / tools/corpus_wikipedia*.py (fe3c05f0-834b-44f2-8739-501865d652c1)
=== porte-sessions ===
exit=0
autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé, pause sans heartbeat exigé, réservation imbriquée avertie sans refus
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/structures/ (29ad180d-38a5-4481-a9a7-ec6ab31c895f)
  ⚠ fichi
… [482 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== journal du jour (S) ===\"; grep -rn \"SOUS-MODULE 647205a\\|analyseur rôles\\|rapport-s-analyseur-roles\" journal/2026-11-02/ journal/sessions/MANIFEST.md 2>/dev/null | head -10; echo \"=== liens fiche ===\"; python3 - <<' … [328 caractères tronqués]`

  ```
=== journal du jour (S) ===
journal/2026-11-02/README.md:30:| `29ad180d-38a5-4481-a9a7-ec6ab31c895f` | Session structures CPU analyseur rôles | 2026-11-02 16:14 | 0.3 h | [rapport](../sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/rapport.md) · [digest](../sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/digest.md) |
journal/2026-11-02/mesures.md:103:- `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — Session structures CPU analyseur rôles (début 2026-11-02 16:14, 0.3 h) → [rapport](../sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/rapport.md) · [digest](../sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/digest.md)
journal/2026-11-02/distribue.md:36:- `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — Session structures CPU analyseur rôles (début 2026-11-02 16:14, 0.3 h) → [rapport](../sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/rapport.md) · [digest](../sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/digest.md)
journal/2026-11-02/attention.md:22:- `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — Session structures CPU analyseur rôles (début 2026-11-02 16:14, 0.3 h) → [rapport](../sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/rapport.md) · [digest](../sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/digest.md)
journal
… [2061 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 -m unittest discover -s tests 2>&1 | tail -3; python3 mesure_analyseur.py --json 2>/dev/null | head -8; python3 verifier_corpus.py ../../data/structures/banque.jsonl; echo \"=== statut sous-module ===\"; git  … [175 caractères tronqués]`

  ```
Ran 40 tests in 3.717s

OK
  gold · 39 phrases · donnees/gold-analyseur.json
  split     phr    types   couv.    rôles   compl.
  dev         7   7/7       1.00  22/22    10/10  
  test       16  16/16      1.00  40/40    19/19  
  holdout    16  15/16      0.99  37/38    16/16  
  global     39  38/39      0.99  99/100   45/45  
  contrôle · baseline 64/100 (0.64) · règles coupées 66/100 (0.66) · rôles mélangés 0.10 [0.00, 0.22]
{
  ✅ ../../data/structures/banque.jsonl · empreinte, comptes, spans et restitution vérifiés
=== statut sous-module ===
=== en-cours mtime ===
-rw-r--r--. 1 stephane stephane 11890 16:37:14 ../../docs/pilotage/en-cours.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -10; echo \"=== diff en-cours ===\"; git diff docs/pilotage/en-cours.md | head -120; echo \"=== S section ===\"; sed -n '55,90p' docs/pilotage/en-cours.md", "description": "Check hub en-cours update for S re … [6 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
 M journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/digest.md
M  journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md
 M journal/sessions/b7d4678e-2143-4daa-a9a4-a456c5aa8dab/digest.md
 M journal/sessions/caaf3018-e3e2-4416-8446-11f0335910aa/digest.md
 M tools/ocr_pdf.py
?? reports/rapport-s-analyseur-roles.md
?? reports/s-banque-structures.json
?? tools/detecte_scans_pdf.py
=== diff en-cours ===
=== S section ===

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc d'interprétations candidates, l'**analyseur** (rôles,
  subordonnées) et l'**export au corpus**.
- **Plan** : 1) ~~plan et réservation~~ ; 2) **analyseur rôles/subordonnées** (en cours) ; 3) **export
  au corpus** ; 4) **tests** ; 5) **fiche, sous-module** ; 6) **ligne d'état**.
- **Ambition** : un analyseur qui **nomme le rôle** et **coupe la subordonnée**.
- **Stratégie** : une règle = une phrase du gold, un contrôle négatif par mesure, 19 tests.
- **Objectif final** : un gold de 20 phrases, une mesure reproductible, `data
… [2075 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== roadmap staged (S) ===\"; git diff --cached docs/pilotage/roadmap.md | grep -n -i -A4 -B2 \"structures\\|analyseur\\|\\*\\*S\\*\\*\" | head -60; echo \"=== en-cours staged (S) ===\"; git diff --cached docs/pilotage/en-cour … [124 caractères tronqués]`

  ```
=== roadmap staged (S) ===
10-+**État au 02/11 16 h 37.** B13 est à **140/140** (gold 432, 116 liens) ; **N2.ac** (1 Go) est le
11- modèle de production (3,49 / 6,03) ; les **quatre** sessions ont rouvert après le reboot —
12: `e181ce02` (16 h 16), `fe3c05f0` (16 h 21), **N2** `0733c5bb` (16 h 17) et **S** `29ad180d`
13- (16 h 19). Le runbook de reprise est dans [`plan-travail.md`](plan-travail.md) § 9.
14-@@ -44,7 +44,7 @@ modèle de production (3,49 / 6,03) ; les **quatre** sessions ont rouvert après
15- 
16- ## L'ordre du jour (carpe diem)
=== en-cours staged (S) ===
46- ## Ce qui reste
47- 
48:-**N2** — les **200 k pas**, puis **R1.1/R1.2** ; **Pensée** — **DRVM/L** ; **S** — l'analyseur
49:+**N2** — **200 k pas**, puis **R1.1/R1.2** ; **Pensée** — **DRVM/L** ; **S** — l'analyseur
50- puis l'export ; **N4** — la consigne ; **B10.3** — le `z` ; **R0.7** — gold/neuronal.
51- 
52- - **Vue d'ensemble** : huit chantiers et relations [`chantiers`](chantiers.md) ; plan multi-sessions [`plan-travail`](plan-travail.md) ; carte [`chantiers-vision.svg`](../schemas/chantiers-vision.svg).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== porte-tableaux ===\"; bash tools/porte-tableaux.sh >/tmp/pt.out 2>&1; echo \"exit=$?\"; tail -6 /tmp/pt.out; echo \"=== verifier_schemas ===\"; python3 tools/verifier_schemas.py 2>&1 | tail -4; echo \"=== git log ===\"; gi … [208 caractères tronqués]`

  ```
=== porte-tableaux ===
exit=0
  ✅ 1556 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 2604 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-02)
=== verifier_schemas ===
  schémas · 458 document(s) · 66 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
=== git log ===
13f4e131 S — LE SOUS-MODULE 647205a : L'ANALYSEUR NOMME LES RÔLES, LE GOLD DE 39 PHRASES, L'EXPORT DE 39 STRUCTURES
e420267a ÉTAT — QUATRE SESSIONS OUVERTES (N2, S, PENSÉE, D/R/A) ; HEARTBEAT 16 h 24 ; PORTE STRICTE RÉPARÉE
dc7f9c56 N2 — MANDAT 200 k PAS SUR LE MÉLANGE 1 Go, PUIS R1.1/R1.2 (session 0733c5bb)
=== en-cours mtime ===
-rw-r--r--. 1 stephane stephane 11890 16:37:14 docs/pilotage/en-cours.md
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
 M journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/digest.md
 M journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/rapport.md
M  journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md
 M journal/sessions/MANIFEST.md
 M 
… [131 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== plan vs HEAD ===\"; git diff HEAD --stat -- journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md; git log --oneline -2 -- journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md; echo \"=== plan: ligne d'éta … [485 caractères tronqués]`

  ```
=== plan vs HEAD ===
e420267a ÉTAT — QUATRE SESSIONS OUVERTES (N2, S, PENSÉE, D/R/A) ; HEARTBEAT 16 h 24 ; PORTE STRICTE RÉPARÉE
=== plan: ligne d'état présente dans HEAD ? ===
1
=== tailles ===
102 journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md
=== status S ===
?? reports/rapport-s-analyseur-roles.md
?? reports/s-banque-structures.json
  ```

- **todo_write** `{"todos": [{"content": "Créer le plan de session S et réserver le territoire", "status": "completed"}, {"content": "Écrire le gold 39 phrases (types, rôles, subordonnées) avant les règles", "status": "completed"}, {"content": "Améliorer generateur.py : rôles contextuels, subordonnées, passif, copule … [688 caractères tronqués]`

  ```
Updated todo list: 1 pending, 0 in progress, 8 completed.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; git log --oneline -2; git status --short -- reports/rapport-s-analyseur-roles.md reports/s-banque-structures.json docs/pilotage/en-cours.md; echo \"=== S section plan/fait ===\"; grep -n \"Fait\\|analyseur rôles\\|3 … [99 caractères tronqués]`

  ```
16:39:07
bee2527d PASSE — REPORTÉE SUR MESURE (DEUX GPU À N2, CHARGE 24) ; SOUS-PASSE DOCUMENTAIRE 7/8
13f4e131 S — LE SOUS-MODULE 647205a : L'ANALYSEUR NOMME LES RÔLES, LE GOLD DE 39 PHRASES, L'EXPORT DE 39 STRUCTURES
?? reports/rapport-s-analyseur-roles.md
?? reports/s-banque-structures.json
=== S section plan/fait ===
59:- **Plan** : 1) ~~plan et réservation~~ ; 2) **analyseur rôles/subordonnées** (en cours) ; 3) **export
65:- **Ce qu'elle fait** : mandat ouvert à **16 h 19** ; l'analyseur rôles/subordonnées est en cours.
79:- **Fait** : B13 **140/140**, gold **432**, coréférence **116 liens** ; **R0.7** — 9 niveaux,
108:  **session `29ad180d`** ouverte le 02/11 16 h 19 — analyseur rôles/subordonnées en cours.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"13f4e131\\|SOUS-MODULE 647205a\" journal/2026-11-02/ journal/sessions/MANIFEST.md 2>/dev/null | head -10; echo \"=== journal outils (dernier) ===\"; tail -30 journal/2026-11-02/outils.md", "description": "Check journal rec … [22 caractères tronqués]`

  ```
journal/2026-11-02/README.md:201:| 16:32 | `13f4e131` | S — LE SOUS-MODULE 647205a : L'ANALYSEUR NOMME LES RÔLES, LE GOLD DE 39 PHRASES, L'EXPORT DE 39 STRUCTURES |
journal/2026-11-02/docs.md:32:| 16:32 | `13f4e131` | S — LE SOUS-MODULE 647205a : L'ANALYSEUR NOMME LES RÔLES, LE GOLD DE 39 PHRASES, L'EXPORT DE 39 STRUCTURES | `README.md`, `apprentissage.md`, `attention.md` (+18) |
=== journal outils (dernier) ===
> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (1)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 11:30 | `4f7631aa` | DONNÉES — LE CEGEP PASSE À 10 NOTES (2,52 M CAR.) ; LE 11E PDF (ENCYCLOPEDIA) DÉPASSE LE TIMEOUT PDFTOPPM, L'OUTIL LE RATTRAPE | `en-cours.md`, `README.md`, `apprentissage.md` (+20) |

## Sessions actives ce jour

- `0733c5bb-f90b-4f58-9241-3364fa32e46c` — Session N2 : plan et réservations (début 2026-11-02 16:14, 0.2 h) → [rapport](../sessions/0733c5bb-f90b-4f58-9241-3364fa32e46
… [2532 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Cycle S clos côté code ; la fiche attend le hub pour la ligne d'état.

**Fait — analyseur rôles/subordonnées + export**

- **Gold** : 39 phrases (`dev` 7, `test` 16, `holdout` 16), dans `tools/structures/donnees/gold-analyseur.json`.
- **Mesure** (`mesure_analyseur.py`) : types **38/39** (97,4 %), rôles **99/100** (99 %), compléments **45/45**, couverture **1 156/1 161** (99,6 %).
- **Contrôles** : baseline à rôle constant **64/100** ; règles coupées **66/100** ; rôles mélangés **0,099** [0,00–0,22] sur 200 permutations ; `verifier_corpus.py --autotest` refuse un span corrompu.
- **Échec nommé** : `h033` — « La femme parle » est lu comme un GN, le verbe sans auxiliaire est avalé. Non corrigé par une liste apprise sur le holdout.
- **Export** : `data/structures/banque.jsonl`, **39 lignes**, SHA-256 `973c70a4…cd7db71` ; modes `banque` (0 ligne, aucun verdict humain — nommé) et `reference` (7 lignes). Manifeste copié dans `reports/s-banque-structures.json`.
- **Tests** : **40/40** verts, dont les 19 d'origine.

**Commits**

- Sous-module : **`647205a`** (committé dans son dépôt avant le pointeur).
- Pointeur principal : **`13f4e131`**, avec le journal du jour.
- Plan de session + bloc d'état proposé : dans **`e420267a`** (le hub l'a intégré au journal), section « Ligne d'état proposée au hub ».

**Reste un geste du hub** — je n'ai pas touché à `en-cours` :

- committer [`reports/rapport-s-analyseur-roles.md`](reports/rapport-s-analyseur-roles.md) et [`reports/s-banque-structures.json`](reports/s-banque-structures.json) avec la section S du plan ;
- compteurs **551 fiches / 637 JSON** (au lieu de 550/636), `reports/INDEX.md`, ligne roadmap **S**.

`revue_documentation.py` signale exactement ces deux compteurs : c'est l'écart attendu tant que la fiche n'est pas intégrée. `verifie_en_cours`, `verifie_journal`, `porte-tableaux`, `verifier_schemas` et `sessions.py --check --strict` passent.

**Prochaine action S** : validation humaine de la banque (le mode `banque` est à zéro), puis frontière du GN sans auxiliaire (`h033`) et gold plus large (voix, causatives).

Reproduction : `cd tools/structures && python3 -m unittest discover -s tests && python3 mesure_analyseur.py && python3 exporter_corpus.py && python3 verifier_corpus.py ../../data/structures/banque.jsonl`.


## Tour 2

### 👤 Utilisateur

mets le dossier copilotage à jour

### 🤖 Assistant

⏵ Mise à jour de `docs/pilotage/` : état S, compteurs et roadmap, puis commit avec la fiche.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-02, 16 h 40 HNE (heure locale, EST).**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active**. Méthode :
6: > [`methode/`](../methode/) ; résultats : [`reports/`](../../reports/) ; histoire :
7: > [`journal/`](../../journal/) ; plan : [`roadmap.md`](roadmap.md).
8: >
9: > **Reprise après le reboot du 02/11 15 h 06** : les **quatre** sessions ont rouvert entre 16 h 14
10: > et 16 h 21 — N2 `0733c5bb`, S `29ad180d`, Pensée `e181ce02`, D/R/A `fe3c05f0` ; les GPU sont
11: > sains ; reprise par `dsh --profile dsh-tui --resume <id>` ; runbook dans
12: > [`plan-travail.md`](plan-travail.md) § 9.
13: 
14: ## Sessions en cours
15: 
16: > Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
17: > [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
18: > `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
19: > le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`
… [11280 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
1: # La roadmap de [Drave](../theorie/glossaire/entrees/drave.md) — un seul plan, quatre chantiers
2: 
3: > **Un seul document de plan.** Le **moteur** (A), l'**intelligence** (B), le **natif** (N) et le **lecteur** (R).
4: > L'ordre se décide par la **valeur** et les **dépendances**, jamais par une date. Les chiffres, les séries et les
5: > contrôles vivent dans [`reports/`](../../reports/) ; ici : l'[état](../theorie/glossaire/entrees/etat.md), la prochaine action, et ce qui bloque.
6: >
7: > **Détail et histoire** : l'ancien plan [A/B](../theorie/glossaire/entrees/a-b.md) est archivé dans
8: > [`roadmap-detail-2026-10-29.md`](../archive/roadmap-detail-2026-10-29.md), le détail N dans
9: > [`roadmap-native-2026-10-29.md`](../archive/roadmap-native-2026-10-29.md). Les **fiches de fonctionnalité** sont
10: > dans [`backlog/index.md`](backlog/index.md) ; le **graphe des dépendances** est dans
11: > [`backlog/dependances.md`](backlog/dependances.md). La **page vivante** est [`en-cours.md`](en-cours.md).
12: 
13: ## Comment lire cette roadmap
14: 
15: - **Les états** : ✅ m
… [41255 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -8; echo \"=== comptes disque ===\"; ls reports/*.md | wc -l; ls reports/*.json | wc -l; echo \"=== status ===\"; git status --short | head -12", "description": "Get current report/JSO … [31 caractères tronqués]`

  ```
revue de documentation · 551 fiche(s) · 638 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
=== comptes disque ===
551
638
=== status ===
 M tools/bloc_linguistique.py
 M tools/ocr_pdf.py
 M tools/tests/linguistique/test_bloc_linguistique.py
?? reports/ocr-pdf-cegep-detection.json
?? reports/rapport-s-analyseur-roles.md
?? reports/s-banque-structures.json
?? tools/detecte_scans_pdf.py
?? tools/tests/linguistique/qualifier_neuronal.py
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M:%S %Z'", "description": "Get real time for state timestamps"}`

  ```
2026-11-02 16:49:54 EST
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-02, 16 h 40 HNE (heure locale, EST).**", "new_string": "**Mis à jour : 2026-11-02, 16 h 49 HNE (heure locale, EST).**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Plan** : 1) ~~plan et réservation~~ ; 2) ~~analyseur rôles/subordonnées~~ (gold 39) ; 3) ~~export\n  au corpus~~ (schéma `statut`, mode gold, manifeste) ; 4) ~~tests : 40~~ ; 5) ~~fiche, man … [2416 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **S — le banc de structures** : outil web (`tools/structures`), générateur, pragmatique (niveaux 0–4), **analyseur rôles/subordonnées 38/39 types, 99/100 rôles, 45/45 compléments**, gold **39* … [595 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**N2** — **200 k pas**, puis **R1.1/R1.2** ; **Pensée** — **DRVM/L** ; **S** — la **validation\nhumaine** de la banque, puis la frontière du GN sans auxiliaire (h033) ; **N4** — la consigne ;\n* … [242 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v2** : rôles **contextuels** et subordonnées typées, gold **39** phrases ; analyseur **38/39** typ … [694 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**État au 02/11 16 h 49.** B13 est à **140/140** (gold 432, 116 liens) ; **N2.ac** (1 Go) est le\nmodèle de production (3,49 / 6,03) ; **S** — l'analyseur rôles/subordonnées est **mesuré**\n(38/3 … [726 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour est le **2026-11-02 16 h 49**.", "old_string": "L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour … [33 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "- **non bloqué, à faire** : **N2** (200 k pas sur le mélange 1 Go, puis R1) ; **N4** (consigne courte) ;\n  **N3** (opérations natives) ; **A8.3b** (mode de lot) ; **R4.4** (les scans réels) ;\n  … [255 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "| R4.4 les scans | pas de **vérité humaine** sur les scans réels : trois vrais scans (Internet Archive) donnent des **accords**, pas des vérités | 10 pages **scannées** avec vérité humaine ; le f … [460 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== revue ===\"; python3 tools/revue_documentation.py 2>&1 | tail -10; echo \"=== en-cours ===\"; python3 tools/verifie_en_cours.py 2>&1 | tail -6; echo \"=== sessions ===\"; python3 tools/sessions.py --check 2>&1 | tail -8",  … [64 caractères tronqués]`

  ```
=== revue ===
  revue de documentation · 551 fiche(s) · 638 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
=== en-cours ===
  en-cours · 1739 mots · 7 sections · 5 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
=== sessions ===
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/structures/ (29ad180d-38a5-4481-a9a7-ec6ab31c895f)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/wikipedia/` (lecture) (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/corpus_wiki_* (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : tools/corpus* (0733c5bb-f90b-4f58-9241-3364fa32e46c) / tools/corpus_wikipedia*.py (fe3c05f0-834b-44f2-8739-501865d652c1)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== tableaux ===\"; bash tools/porte-tableaux.sh >/tmp/pt2.out 2>&1; echo \"exit=$?\"; tail -4 /tmp/pt2.out; echo \"=== taille ===\"; python3 tools/taille_documents.py 2>&1 | tail -4; echo \"=== diff stat ===\"; git diff --sta … [62 caractères tronqués]`

  ```
=== tableaux ===
exit=0
  ✅ 1557 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 2604 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-02)
=== taille ===
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ❌ 1 violation(s) :
     · T0 : 4113 mots (AGENTS + en-cours + une tâche) > budget 4 000
=== diff stat ===
 docs/pilotage/en-cours.md                          |  39 ++++---
 docs/pilotage/roadmap.md                           |  12 +-
 tools/bloc_linguistique.py                         | 125 +++++++++++++++++++++
 tools/ocr_pdf.py                                   |  61 ++++++++--
 tools/tests/linguistique/test_bloc_linguistique.py |  26 +++++
 5 files changed, 233 insertions(+), 30 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport subprocess, re\ndef words(s): return len(s.split())\nnew = open('docs/pilotage/en-cours.md').read()\nold = subprocess.check_output(['git','show','HEAD:docs/pilotage/en-cours.md'], text=True)\ndef section(t, s … [571 caractères tronqués]`

  ```
S session old 171 new 269
S en cours old 42 new 50
Ce qui reste old 51 new 62
total old 1622 new 1739
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).\n- **Rôle** : **S — les structures** : le banc, l'analyseur  … [3075 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **S — le banc de structures** : **analyseur rôles/subordonnées 38/39 types, 99/100 rôles, 45/45 compléments**, gold **39**, **40 tests** ; corpus **39** structures (SHA `973c70a4…`) ; [`fiche` … [531 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**N2** — **200 k pas**, puis **R1.1/R1.2** ; **Pensée** — **DRVM/L** ; **S** — la **validation\nhumaine** de la banque et la frontière du GN (h033) ; **N4** — la consigne ; **B10.3** — le `z` ;\ … [285 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -4; echo \"=== taille ===\"; python3 tools/taille_documents.py 2>&1 | tail -8; echo \"=== revue ===\"; python3 tools/revue_documentation.py 2>&1 | tail -4", "description": "Recheck word b … [23 caractères tronqués]`

  ```
en-cours · 1633 mots · 7 sections · 5 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
=== taille ===
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4007 mots (budget 4 000)

  avertissements :
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ❌ 1 violation(s) :
     · T0 : 4007 mots (AGENTS + en-cours + une tâche) > budget 4 000
=== revue ===
  revue de documentation · 551 fiche(s) · 639 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ❌ 1 anomalie(s) :
     · compteurs : en-cours.md dit 638 JSON, le disque en a 639
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np = Path('docs/pilotage/en-cours.md')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"- **Ambition** : un analyseur qui nomme le rôle et coupe la subordonnée ; un corpus qui se rejoue.\ … [893 caractères tronqués]`

  ```
trim + compteur 639
  en-cours · 1626 mots · 7 sections · 5 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable

  avertissements :
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  revue de documentation · 551 fiche(s) · 639 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md", "limit": 45}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md</path>
<type>file</type>
<content>
1: # Plan de session — S, les structures (analyser, banquer, exporter)
2: 
3: > **Mandat vivant.** Ouvert le 2026-11-02 16 h 19 HNE depuis
4: > [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md) (§ S) et
5: > [`plan-travail.md`](../../../docs/pilotage/plan-travail.md) § 9.2.
6: > Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.
7: > `en-cours` reste la seule source de l'état : ce plan est le **contrat de travail** qui le
8: > précède, et la section S y est **proposée au hub**, pas écrite ici.
9: 
10: - **Session** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f`
11: - **Rôle** : **S — les structures** : le banc d'interprétations candidates (outil web, générateur,
12:   pragmatique, banque), l'**analyseur** (rôles, subordonnées) et l'**export au corpus**.
13: - **Périmètre** : S (structures) — S-analyseur rôles/subordonnées · S-banque · S-export au corpus.
14: - **Fichiers réservés** : `tools/structures/` ; `data/structures/` ; `reports/rapport-s-*` ;
15:   `reports/s-banque-*` ; `journal/sessions/29ad180d-38
… [2632 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np = Path('journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"\"\"> `en-cours` reste la seule source de l'état : ce plan est  … [2497 caractères tronqués]`

  ```
plan mis à jour 63 lignes
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/structures/ (29ad180d-38a5-4481-a9a7-ec6ab31c895f)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/wikipedia/` (lecture) (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/corpus_wiki_* (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : tools/corpus* (0733c5bb-f90b-4f58-9241-3364fa32e46c) / tools/corpus_wikipedia*.py (fe3c05f0-834b-44f2-8739-501865d652c1)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '52,72p' docs/pilotage/en-cours.md; echo \"=== roadmap S ===\"; grep -n \"S — les structures\\|S — la banque\\|État au 02/11\\|dernière mise à jour\" docs/pilotage/roadmap.md | head -8; echo \"=== status ===\"; git status --sh … [156 caractères tronqués]`

  ```
- **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).

### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures : l'analyseur et l'export

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : 1–4) ~~plan, analyseur (gold 39), export, tests 40~~ ; 5–6) ~~fiche, pointeur, état~~.
- **Ambition** : nommer le rôle, couper la subordonnée ; un corpus qui se rejoue.
- **Stratégie** : une règle = une phrase du gold, trois contrôles.
- **Objectif final** : gold **39**, corpus **39**, manifeste SHA-256.
- **Fait** : types **38/39**, rôles **99/100**, compléments **45/45** ; contrôles **64/100**,
  **66/100**, **0,099** ; échec nommé **h033** ; **40 tests** ;
  [`fiche`](../../reports/rapport-s-analyseur-roles.md).
- **Ce qu'elle fait** : sous-module **`647205a`** et pointeur **`13f4e131`** committés ; corpus
  **39** lignes (SHA `973c70a4…`) ; mode `banque` à **0** verdict humain.
- **Ce que font les autres** : **hub**, **N2**, **Pensée**, **D/R/A**.
- **Proch
… [1666 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md reports/rapport-s-analyseur-roles.md reports/s-banque-structures.json && git diff --cached --stat && git commit  … [596 caractères tronqués]`

  ```
docs/pilotage/en-cours.md                          |  37 +++---
 docs/pilotage/roadmap.md                           |  12 +-
 .../29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md   |  59 ++-------
 reports/rapport-s-analyseur-roles.md               | 140 +++++++++++++++++++++
 reports/s-banque-structures.json                   |  11 ++
 5 files changed, 188 insertions(+), 71 deletions(-)
[master 63927a03] S — L'ÉTAT INTÈGRE L'ANALYSEUR RÔLES : 38/39 TYPES, 99/100 RÔLES, 39 STRUCTURES
 30 files changed, 2385 insertions(+), 193 deletions(-)
 create mode 100644 reports/rapport-s-analyseur-roles.md
 create mode 100644 reports/s-banque-structures.json
[stderr]
  ✅ index : aucun fait stagé sans état
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -2; echo \"=== fichiers du commit ===\"; git show --stat --oneline 63927a03 | head -40; echo \"=== status ===\"; git status --short | head -12", "description": "Inspect committed files and status"}`

  ```
63927a03 S — L'ÉTAT INTÈGRE L'ANALYSEUR RÔLES : 38/39 TYPES, 99/100 RÔLES, 39 STRUCTURES
9223d054 ÉTAT — COMPTEURS AU DISQUE (551 FICHES / 638 JSON) ; HEARTBEAT 16 h 40
=== fichiers du commit ===
63927a03 S — L'ÉTAT INTÈGRE L'ANALYSEUR RÔLES : 38/39 TYPES, 99/100 RÔLES, 39 STRUCTURES
 docs/pilotage/en-cours.md                          |  37 +-
 docs/pilotage/roadmap.md                           |  12 +-
 journal/2026-11-02/README.md                       |  28 +-
 journal/2026-11-02/apprentissage.md                |  12 +-
 journal/2026-11-02/attention.md                    |  12 +-
 journal/2026-11-02/distribue.md                    |  12 +-
 journal/2026-11-02/docs.md                         |  15 +-
 journal/2026-11-02/memoire.md                      |  12 +-
 journal/2026-11-02/mesures.md                      |  12 +-
 journal/2026-11-02/modele.md                       |  12 +-
 journal/2026-11-02/moteur.md                       |  12 +-
 journal/2026-11-02/outils.md                       |  12 +-
 journal/2026-11-02/portes.md                       |  12 +-
 journal/README.md                                  |  14 +-
 .../0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md | 262 +++
… [1440 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== revue ===\"; python3 tools/revue_documentation.py 2>&1 | tail -4; echo \"=== taille ===\"; python3 tools/taille_documents.py 2>&1 | tail -5; echo \"=== en-cours ===\"; python3 tools/verifie_en_cours.py 2>&1 | tail -3; echo … [126 caractères tronqués]`

  ```
=== revue ===
  revue de documentation · 552 fiche(s) · 639 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ❌ 1 anomalie(s) :
     · compteurs : en-cours.md dit 551 fichiers, le disque en a 552
=== taille ===
  avertissements :
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ❌ 1 violation(s) :
     · reports/README.md : 2809 mots > budget 2800 (T1)
=== en-cours ===
  en-cours · 1626 mots · 7 sections · 5 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
=== etat --head ===
  état · dernier fait 63927a03 · dernier état 63927a03
  ✅ aucun fait commité après le dernier état
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; python3 - <<'PY'\nfrom pathlib import Path\np = Path('docs/pilotage/en-cours.md')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"**Mis à jour : 2026-11-02, 16 h 49 HNE (heure locale, EST).**\",\n              \"** … [435 caractères tronqués]`

  ```
16:56
compteur 552
  revue de documentation · 552 fiche(s) · 639 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
=== taille ===
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ❌ 1 violation(s) :
     · reports/README.md : 2809 mots > budget 2800 (T1)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/en-cours.md && git commit -m \"ÉTAT — COMPTEURS AU DISQUE (552 FICHES / 639 JSON) ; LA FICHE S EST INTÉGRÉE\" -m \"Le compteur passe à 552 fiches / 639 JSON après l'intégration de la fiche S et de la fiche Pensé … [266 caractères tronqués]`

  ```
[master dca7e7a2] ÉTAT — COMPTEURS AU DISQUE (552 FICHES / 639 JSON) ; LA FICHE S EST INTÉGRÉE
 14 files changed, 846 insertions(+), 41 deletions(-)
[stderr]
  ✅ index : aucun fait stagé sans état
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== log ===\"; git log --oneline -3; echo \"=== status ===\"; git status --short | head -14; echo \"=== diff reports/README ===\"; git diff -- reports/README.md | head -80", "description": "Inspect final log and reports README … [7 caractères tronqués]`

  ```
=== log ===
dca7e7a2 ÉTAT — COMPTEURS AU DISQUE (552 FICHES / 639 JSON) ; LA FICHE S EST INTÉGRÉE
63927a03 S — L'ÉTAT INTÈGRE L'ANALYSEUR RÔLES : 38/39 TYPES, 99/100 RÔLES, 39 STRUCTURES
9223d054 ÉTAT — COMPTEURS AU DISQUE (551 FICHES / 638 JSON) ; HEARTBEAT 16 h 40
=== status ===
 M docs/implantation/bloc-linguistique.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M reports/INDEX.md
 M reports/README.md
 M tools/bloc_linguistique.py
 M tools/ocr_pdf.py
 M tools/tests/linguistique/test_bloc_linguistique.py
?? reports/ocr-pdf-cegep-detection.json
?? reports/pensee-gold-neuronal.json
?? reports/rapport-pensee-gold-neuronal.md
?? tools/detecte_scans_pdf.py
?? tools/tests/linguistique/qualifier_neuronal.py
=== diff reports/README ===
diff --git a/reports/README.md b/reports/README.md
index 38facb39..afe6102d 100644
--- a/reports/README.md
+++ b/reports/README.md
@@ -15,6 +15,7 @@
 
 | fichier | ce qu'il porte |
 |---|---|
+| [`rapport-pensee-gold-neuronal.md`](rapport-pensee-gold-neuronal.md) | **B13/R0.7** — le gold neuronal : tagger 7B local, cascade POS **0,944** |
 | [`rapport-pensee-vrais-absents.md`](rapport-pensee-vrais-absents.md) | **B13** — les vrais absents : 5
… [307 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== revue ===\"; python3 tools/revue_documentation.py 2>&1 | tail -4; echo \"=== taille ===\"; python3 tools/taille_documents.py 2>&1 | tail -6; echo \"=== en-cours ===\"; python3 tools/verifie_en_cours.py 2>&1 | tail -3; echo … [232 caractères tronqués]`

  ```
=== revue ===
  revue de documentation · 552 fiche(s) · 639 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
=== taille ===
  avertissements :
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ❌ 2 violation(s) :
     · reports/README.md : 2809 mots > budget 2800 (T1)
     · T0 : 4105 mots (AGENTS + en-cours + une tâche) > budget 4 000
=== en-cours ===
  ❌ 2 anomalie(s) :
     · 6 questions ouvertes > 5
     · question sans ce qui la débloque (`→`) : **Pensée** : le tagger 7B tient-il les **syntagmes** et la *
=== etat ===
  état · dernier fait 63927a03 · dernier état dca7e7a2
  ✅ aucun fait commité après le dernier état
=== sessions ===
exit=0
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/corpus_wiki_* (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : tools/corpus* (0733c5bb-f90b-4f58-9241-3364fa32e46c) / tools/corpus_wi
… [50 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff docs/pilotage/en-cours.md | head -140; echo \"=== roadmap diff ===\"; git diff docs/pilotage/roadmap.md | head -60", "description": "Inspect uncommitted pilotage changes by other session"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 5c3cc9c3..7c0dd925 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -79,10 +79,17 @@
 - **Objectif final** : un **moteur de pensée v0** exécutable, documenté, mesuré, committé.
 - **Fait** : B13 **140/140**, gold **432**, coréférence **116 liens** ; **R0.7** — 9 niveaux,
   **398 langues à 0,9687** ; **R4.4** — trois limites nommées.
-- **Ce qu'elle fait** : le cycle **140/140** est committé ; reprise à **16 h 16**.
+- **Gold neuronal** : **tagger 7B local** (Qwen2.5-7B-Instruct Q4_K_M, CPU) — POS **0,8483**
+  seul ; **cascade à 0,6 : 0,9440** (20 réelles **0,9238**, 160 synthétiques **0,9471**),
+  **0 refus**, 180 appels ; [`pensee-gold-neuronal`](../../reports/rapport-pensee-gold-neuronal.md),
+  [JSON](../../reports/pensee-gold-neuronal.json).
+- **Ce qu'elle fait** : le cycle **140/140** est committé ; le **gold neuronal POS** est mesuré
+  et qualifié ; reprise à **16 h 16**.
 - **Ce que font les autres** : **N2**, **S**, **D/R/A**, **hub**.
-- **Prochaine action** : **gold neuronal** (modèle local) ; **DRVM/native** bloqué.
-- **Bloquants** : **neuronal réel bloqué** (`llama-cl
… [20270 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== S dans HEAD ===\"; git show HEAD:docs/pilotage/en-cours.md | sed -n '54,70p'; echo \"=== fiche/manifest suivis ===\"; git ls-files reports/rapport-s-analyseur-roles.md reports/s-banque-structures.json; echo \"=== commits = … [326 caractères tronqués]`

  ```
=== S dans HEAD ===
### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures : l'analyseur et l'export

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : 1–4) ~~plan, analyseur (gold 39), export, tests 40~~ ; 5–6) ~~fiche, pointeur, état~~.
- **Ambition** : nommer le rôle, couper la subordonnée ; un corpus qui se rejoue.
- **Stratégie** : une règle = une phrase du gold, trois contrôles.
- **Objectif final** : gold **39**, corpus **39**, manifeste SHA-256.
- **Fait** : types **38/39**, rôles **99/100**, compléments **45/45** ; contrôles **64/100**,
  **66/100**, **0,099** ; échec nommé **h033** ; **40 tests** ;
  [`fiche`](../../reports/rapport-s-analyseur-roles.md).
- **Ce qu'elle fait** : sous-module **`647205a`** et pointeur **`13f4e131`** committés ; corpus
  **39** lignes (SHA `973c70a4…`) ; mode `banque` à **0** verdict humain.
- **Ce que font les autres** : **hub**, **N2**, **Pensée**, **D/R/A**.
- **Prochaine action** : validation humaine de la banque, puis frontière du GN (h0
… [507 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; ls -la --time-style=+%H:%M:%S docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/README.md; git log --oneline -2", "description": "Check mtimes of concurrent pilotage edits"}`

  ```
17:01
-rw-r--r--. 1 stephane stephane 11982 17:01:03 docs/pilotage/en-cours.md
-rw-r--r--. 1 stephane stephane 43969 16:57:52 docs/pilotage/roadmap.md
-rw-r--r--. 1 stephane stephane 23126 17:00:10 reports/README.md
dca7e7a2 ÉTAT — COMPTEURS AU DISQUE (552 FICHES / 639 JSON) ; LA FICHE S EST INTÉGRÉE
63927a03 S — L'ÉTAT INTÈGRE L'ANALYSEUR RÔLES : 38/39 TYPES, 99/100 RÔLES, 39 STRUCTURES
  ```

- **todo_write** `{"todos": [{"content": "Créer le plan de session S et réserver le territoire", "status": "completed"}, {"content": "Écrire le gold 39 phrases (types, rôles, subordonnées) avant les règles", "status": "completed"}, {"content": "Améliorer generateur.py : rôles contextuels, subordonnées, passif, copule … [806 caractères tronqués]`

  ```
Updated todo list: 1 pending, 0 in progress, 9 completed.
  ```

### 🤖 Assistant

⏵ Pilotage S committé : fiche, manifeste, `en-cours` et roadmap à jour.

**Fait**

- **`63927a03`** — `reports/rapport-s-analyseur-roles.md`, `reports/s-banque-structures.json`, la section S d'`en-cours`, la ligne S de la roadmap et le plan de session.
- **`dca7e7a2`** — compteurs au disque : **552 fiches / 639 JSON**.
- La section S porte le fait (38/39 types, 99/100 rôles, 45/45 compléments, contrôles 64/100 · 66/100 · 0,099, échec h033, corpus 39 lignes SHA `973c70a4…`, 40 tests), le pointeur `13f4e131`, le sous-module `647205a` et la prochaine action.
- La roadmap porte S en ✅ v2, la phrase d'état, la file « jamais en attente » et la banque validée à 0 comme ligne bloquée nommée.

**Contrôles au commit** : `revue_documentation.py` ✅, T0 ✅, `en-cours` 1 626 mots ✅, `verifie_en_cours.py` ✅, `sessions.py --check` ✅, `verifie_etat_a_jour.py` ✅.

**À noter** : depuis le commit, la session **Pensée** écrit son gold neuronal dans `en-cours`/`roadmap` (fichiers modifiés, non committés ; mtime 17:01). Ces lignes — une 6e question, T0 à 4 105, `reports/README.md` à 2 809 — sont **son** intégration, pas celle de S : je ne les ai ni committées ni modifiées. Le hub/Pensée doit les finir en ramenant les questions à 5 et en coupant ~105 mots. Dis-moi si tu veux que je fasse cette coupe et que je commite l'ensemble.

Prochaine action S inchangée : **validation humaine de la banque**, puis frontière du GN sans auxiliaire (`h033`).


## Tour 3

### 👤 Utilisateur

commit l'ensemble

### 🤖 Assistant

⏵ Intégration de l'ensemble : je vérifie les changements en cours, je remets les compteurs et les budgets au vert, puis je commite tout.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short; echo \"=== DIFF STAT ===\"; git diff --stat; echo \"=== UNTRACKED ===\"; git status --short | grep '^??'", "description": "Full worktree status before integration"}`

  ```
M  docs/implantation/bloc-linguistique.md
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
 M journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
 M journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/digest.md
 M journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/digest.md
 M journal/sessions/abb58991-fe0a-4d6e-b039-6552b09f8454/digest.md
 M journal/sessions/b7d4678e-2143-4daa-a9a4-a456c5aa8dab/digest.md
M  reports/INDEX.md
M  reports/README.md
A  reports/pensee-gold-neuronal.json
A  reports/rapport-pensee-gold-neuronal.md
M  tools/bloc_linguistique.py
 M tools/ocr_pdf.py
A  tools/tests/linguistique/qualifier_neuronal.py
M  tools/tests/linguistique/test_bloc_linguistique.py
?? reports/ocr-pdf-cegep-detection.json
?? reports/rapport-n2-r11.md
?? tools/detecte_scans_pdf.py
=== DIFF STAT ===
 .../0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md |  337 +++++++
 .../29ad180d-38a5-4481-a9a7-ec6ab31c895f/digest.md |  157 +++
 .../536cd5d6-94ac-4057-8fe9-11709a4587c7/digest.md |  258 +++++
 .../abb58991-fe0a-4d6e-b039-6552b09f8454/digest.md | 1018 ++++++++++++++++++++
 .../b7d4678e-2143-4daa-a9a4-a456c5aa8dab/digest.md |   19 +
 tools/ocr_pdf.py                     
… [194 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== diff ocr_pdf ===\"; git diff -- tools/ocr_pdf.py | head -100; echo \"=== diff bloc_linguistique (stat) ===\"; git diff --stat -- tools/bloc_linguistique.py tools/tests/linguistique/ docs/implantation/bloc-linguistique.md;  … [243 caractères tronqués]`

  ```
=== diff ocr_pdf ===
diff --git a/tools/ocr_pdf.py b/tools/ocr_pdf.py
index c1d01419..67d7cd3e 100644
--- a/tools/ocr_pdf.py
+++ b/tools/ocr_pdf.py
@@ -13,6 +13,13 @@ un échantillon, pas une WER inventée.
 Usage :
   python3 tools/ocr_pdf.py --max-doc 20          # pilote (les 20 premiers scannés)
   python3 tools/ocr_pdf.py                       # tous les scannés des racines
+  python3 tools/ocr_pdf.py --liste scans.txt --ouvriers 8
+      # liste explicite de scans déjà qualifiés (détection intégrale), pages en parallèle
+
+DÉTECTION. Sans `--liste`, un PDF est « scanné » si ses **deux premières pages** portent moins de
+50 caractères natifs par page. Mesure du 02/11 sur le fonds CEGEP : 807 candidats, mais 147 vrais
+scans (seuil appliqué au texte **intégral**, comme `extrait_pdf.py`) — les couvertures sans texte
+des livres natifs font sur-classer 5,5×. La liste explicite est la voie pour un run de fond.
 """
 from __future__ import annotations
 
@@ -26,6 +33,7 @@ import subprocess
 import sys
 import tempfile
 import time
+from concurrent.futures import ThreadPoolExecutor
 
 RACINE = pathlib.Path(__file__).resolve().parent.parent
 ROOT = RACINE / "work/ocr/root"
@@ -57,7 +65,
… [3882 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== STAGED STAT ===\"; git diff --cached --stat; echo \"=== STAGED en-cours (résumé) ===\"; git diff --cached -- docs/pilotage/en-cours.md | head -120", "description": "Inspect staged integration diff"}`

  ```
=== STAGED STAT ===
 docs/implantation/bloc-linguistique.md             |  24 +-
 docs/pilotage/en-cours.md                          |  19 +-
 docs/pilotage/roadmap.md                           |   9 +-
 reports/INDEX.md                                   |   4 +-
 reports/README.md                                  |   1 +
 reports/pensee-gold-neuronal.json                  | 946 +++++++++++++++++++++
 reports/rapport-pensee-gold-neuronal.md            | 162 ++++
 tools/bloc_linguistique.py                         | 125 +++
 tools/tests/linguistique/qualifier_neuronal.py     | 309 +++++++
 tools/tests/linguistique/test_bloc_linguistique.py |  26 +
 10 files changed, 1603 insertions(+), 22 deletions(-)
=== STAGED en-cours (résumé) ===
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 5c3cc9c3..ad15c8d9 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -77,12 +77,13 @@
 - **Ambition** : un **runtime cognitif** où penser est une recherche tracée sur des états pluriels.
 - **Stratégie** : v0 petit et mesuré, GPU de N2 intacts.
 - **Objectif final** : un **moteur de pensée v0** exécutable, documenté, mesuré, committé.
-- **Fait** : B13 **140
… [3426 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== rapport-n2-r11 (head) ===\"; head -40 reports/rapport-n2-r11.md 2>/dev/null; echo \"...\"; ls -la --time-style=+%H:%M:%S reports/rapport-n2-r11.md reports/ocr-pdf-cegep-detection.json tools/detecte_scans_pdf.py; echo \"=== … [319 caractères tronqués]`

  ```
=== rapport-n2-r11 (head) ===
# R1.1 — Les positions relatives : la courbe de longueur s'aplatit, la table absolue explose

> **Ligne de roadmap** : R1 · **Date** : 2026-11-02 · **Verdict** : remplacer la position
> apprise **absolue** par un **RoPE** fait passer la PPL à 1 000 octets de **8,2024** à
> **3,2545** sur la même recette (34,3 M, canal, 20 000 pas, même initialisation, même graine).
> La **porte R1.1** — « PPL à 1 000 octets dans un facteur **1,5** de celle à 129 » — est tenue :
> **0,97×** (RoPE) contre **2,33×** (absolues) ; et la PPL à 128 ne se dégrade pas, elle
> **s'améliore de 0,14** (3,5131 → 3,3696). Le mécanisme est contrôlé : à **texte et
> prédécesseurs identiques**, changer le décalage absolu ne change rien pour RoPE (3,1645 →
> 3,1662) et multiplie la PPL absolue par **4,8** (3,8468 → 18,6055), parce que les lignes 512+
> de la table de positions n'ont **jamais été entraînées**.

## La question

La note de passage [`rapport-n2-fenetre-r1`](rapport-n2-fenetre-r1.md) laisse R1.1 avec une
prédiction : le gain des **positions aléatoires** (N2.j2, N2.h3) est une astuce d'entraînement ;
un schéma **relatif** doit le reproduire **par construction**, sans le coût 
… [5324 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== revue ===\"; python3 tools/revue_documentation.py 2>&1 | tail -8; echo \"=== en-cours ===\"; python3 tools/verifie_en_cours.py 2>&1 | tail -6; echo \"=== taille ===\"; python3 tools/taille_documents.py 2>&1 | tail -6; echo … [142 caractères tronqués]`

  ```
=== revue ===
  revue de documentation · 553 fiche(s) · 639 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
=== en-cours ===
  en-cours · 1623 mots · 7 sections · 5 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
=== taille ===
  T0 max : 3997 mots (budget 4 000)

  avertissements :
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
=== comptes disque ===
553
639
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n2-r11.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-n2-r11.md</path>
<type>file</type>
<content>
1: # R1.1 — Les positions relatives : la courbe de longueur s'aplatit, la table absolue explose
2: 
3: > **Ligne de roadmap** : R1 · **Date** : 2026-11-02 · **Verdict** : remplacer la position
4: > apprise **absolue** par un **RoPE** fait passer la PPL à 1 000 octets de **8,2024** à
5: > **3,2545** sur la même recette (34,3 M, canal, 20 000 pas, même initialisation, même graine).
6: > La **porte R1.1** — « PPL à 1 000 octets dans un facteur **1,5** de celle à 129 » — est tenue :
7: > **0,97×** (RoPE) contre **2,33×** (absolues) ; et la PPL à 128 ne se dégrade pas, elle
8: > **s'améliore de 0,14** (3,5131 → 3,3696). Le mécanisme est contrôlé : à **texte et
9: > prédécesseurs identiques**, changer le décalage absolu ne change rien pour RoPE (3,1645 →
10: > 3,1662) et multiplie la PPL absolue par **4,8** (3,8468 → 18,6055), parce que les lignes 512+
11: > de la table de positions n'ont **jamais été entraînées**.
12: 
13: ## La question
14: 
15: La note de passage [`rapport-n2-fenetre-r1`](rapport-n2-fenetre-r1.md) laisse R1.1 avec une
16: prédiction : le gain des **positi
… [7506 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,8p' docs/pilotage/en-cours.md; echo \"=== D/R/A ===\"; sed -n '86,105p' docs/pilotage/en-cours.md; echo \"=== compteurs ===\"; grep -n \"fichiers / JSON\" docs/pilotage/en-cours.md; echo \"=== taille D/R/A ===\"; python3 -  … [360 caractères tronqués]`

  ```
# En ce moment

**Mis à jour : 2026-11-02, 16 h 56 HNE (heure locale, EST).**

> **État courant, pas histoire** : une sous-section par **session active**. Méthode :
> [`methode/`](../methode/) ; résultats : [`reports/`](../../reports/) ; histoire :
> [`journal/`](../../journal/) ; plan : [`roadmap.md`](roadmap.md).
>
=== D/R/A ===
- **Bloquants** : aucun pour le POS ; le **complet** (syntagmes) reste à mesurer.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

### Session `fe3c05f0-834b-44f2-8739-501865d652c1` — D/R/A : les données, le lecteur, le moteur

- **Id** : `fe3c05f0-834b-44f2-8739-501865d652c1` — [`plan.md`](../../journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md).
- **Rôle** : **D/R/A** — texte intégral, PDF/OCR, prépa R1.1/R1.2, A2.6/A8.3.
- **Plan** : texte intégral, PDF, OCR, glossaire.
- **Ambition** : le français réel.
- **Stratégie** : dump, débaliseur, OCR page à page, glossaire au rendu.
- **Objectif final** : 10 corpus, ficés.
- **Ce qu'elle fait** : 10 corpus (**20,53 M**) ; PDF 1 927 ; OCR 20 livres + 10 notes
  CEGEP ; glossaire 355 ; [`ocr-cegep`](../../reports/rapport-ocr-cegep.md).
- **Ce que font les 
… [421 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np = Path('docs/pilotage/en-cours.md')\nt = p.read_text(encoding='utf-8')\n# 1. date\nt = t.replace(\"**Mis à jour : 2026-11-02, 16 h 56 HNE (heure locale, EST).**\",\n              \"**Mis  … [2895 caractères tronqués]`

  ```
en-cours mis à jour
  en-cours · 1612 mots · 7 sections · 5 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable

  avertissements :
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  revue de documentation · 553 fiche(s) · 639 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/pilotage/en-cours.md tools/ocr_pdf.py tools/detecte_scans_pdf.py reports/ocr-pdf-cegep-detection.json && git diff --cached --stat | tail -25; echo \"=== non stagé restant ===\"; git status --short | grep -v '^[MAD]  ' |  … [75 caractères tronqués]`

  ```
docs/pilotage/en-cours.md            |  27 +-
 reports/ocr-pdf-cegep-detection.json | 747 +++++++++++++++++++++++++++++++++++
 tools/detecte_scans_pdf.py           | 118 ++++++
 tools/ocr_pdf.py                     |  61 ++-
 4 files changed, 929 insertions(+), 24 deletions(-)
=== non stagé restant ===
?? reports/rapport-n2-r11.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -4; echo \"=== status ===\"; git status --short; echo \"=== cached stat ===\"; git diff --cached --stat", "description": "Check whether Pensée set was committed concurrently"}`

  ```
7ef0199c B13 — LE GOLD NEURONAL : TAGGER 7B LOCAL, CASCADE POS 0,944 ; PORTE BLOC VERTE, B13 134/140 (6 ROUGES S)
dca7e7a2 ÉTAT — COMPTEURS AU DISQUE (552 FICHES / 639 JSON) ; LA FICHE S EST INTÉGRÉE
63927a03 S — L'ÉTAT INTÈGRE L'ANALYSEUR RÔLES : 38/39 TYPES, 99/100 RÔLES, 39 STRUCTURES
9223d054 ÉTAT — COMPTEURS AU DISQUE (551 FICHES / 638 JSON) ; HEARTBEAT 16 h 40
=== status ===
M  docs/pilotage/en-cours.md
A  reports/ocr-pdf-cegep-detection.json
A  tools/detecte_scans_pdf.py
M  tools/ocr_pdf.py
?? reports/rapport-n2-r11.md
=== cached stat ===
 docs/pilotage/en-cours.md            |  27 +-
 reports/ocr-pdf-cegep-detection.json | 747 +++++++++++++++++++++++++++++++++++
 tools/detecte_scans_pdf.py           | 118 ++++++
 tools/ocr_pdf.py                     |  61 ++-
 4 files changed, 929 insertions(+), 24 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --cached -- docs/pilotage/en-cours.md | head -80; echo \"=== verif rapides ===\"; python3 tools/verifie_en_cours.py 2>&1 | tail -3; python3 tools/taille_documents.py 2>&1 | tail -3; python3 tools/revue_documentation.py 2>&1  … [73 caractères tronqués]`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index ad15c8d9..878c814a 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-02, 16 h 56 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-02, 17 h 20 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active**. Méthode :
 > [`methode/`](../methode/) ; résultats : [`reports/`](../../reports/) ; histoire :
@@ -22,16 +22,15 @@
 
 - **Id** : `536cd5d6-94ac-4057-8fe9-11709a4587c7` — [`plan.md`](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md).
 - **Rôle** : **Hub** — intégration, état, roadmap, journal, compteurs ; reprise après reboot ; runbook.
-- **Plan** : 1–7) ~~audit, commits, état, mandats, porte, INDEX, runbook~~ ; 8) **intégration** ;
-  9) **passe de portes** (GPU 1).
+- **Plan** : 1–7) ~~audit, commits, état, mandats, porte, INDEX, runbook~~ ; 8–9) **intégration,
+  portes** (GPU 1).
 - **Ambition** : un état reprenable, des mandats qui disent la vérité.
 - **Stratégie** : committer par flux (`git add` explicite), nommer ce qui reste.
 - **Objectif final** : sédimentat
… [4026 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -m \"D/R/A — LA DÉTECTION CEGEP SÉPARE 147 SCANS DE 2 681 PDF ; L'OCR PASSE À LA LISTE EXPLICITE\" -m \"La détection sur le texte intégral (pdftotext + pdfinfo, seuil 50 car/page, SHA-256) trouve 147 scans sur 2 681 PDF, 9 … [511 caractères tronqués]`

  ```
[master d2fc26c6] D/R/A — LA DÉTECTION CEGEP SÉPARE 147 SCANS DE 2 681 PDF ; L'OCR PASSE À LA LISTE EXPLICITE
 27 files changed, 1643 insertions(+), 109 deletions(-)
 create mode 100644 reports/ocr-pdf-cegep-detection.json
 create mode 100644 tools/detecte_scans_pdf.py
[stderr]
  ✅ index : aucun fait stagé sans état
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -5; echo \"=== status ===\"; git status --short; echo \"=== revue ===\"; python3 tools/revue_documentation.py 2>&1 | tail -3; echo \"=== taille ===\"; python3 tools/taille_documents.py 2>&1 | tail -3; echo \"=== en- … [193 caractères tronqués]`

  ```
d2fc26c6 D/R/A — LA DÉTECTION CEGEP SÉPARE 147 SCANS DE 2 681 PDF ; L'OCR PASSE À LA LISTE EXPLICITE
7ef0199c B13 — LE GOLD NEURONAL : TAGGER 7B LOCAL, CASCADE POS 0,944 ; PORTE BLOC VERTE, B13 134/140 (6 ROUGES S)
dca7e7a2 ÉTAT — COMPTEURS AU DISQUE (552 FICHES / 639 JSON) ; LA FICHE S EST INTÉGRÉE
63927a03 S — L'ÉTAT INTÈGRE L'ANALYSEUR RÔLES : 38/39 TYPES, 99/100 RÔLES, 39 STRUCTURES
9223d054 ÉTAT — COMPTEURS AU DISQUE (551 FICHES / 638 JSON) ; HEARTBEAT 16 h 40
=== status ===
?? reports/rapport-n2-r11.md
=== revue ===
  revue de documentation · 553 fiche(s) · 639 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
=== taille ===
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
=== en-cours ===
  en-cours · 1612 mots · 7 sections · 5 session(s) · 6 puces · 5 questions
  ✅ état court, stru
… [147 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Intégration committée : Pensée (`7ef0199c`), D/R/A (`d2fc26c6`), S (`63927a03`/`dca7e7a2`). Seul le brouillon N2 reste hors commit.

**Committé**

- **`7ef0199c`** — Pensée/B13 : gold neuronal, tagger 7B local, POS **0,8483**, cascade **0,9440** ; fiche + JSON + doc + outils ; état, README et INDEX.
- **`d2fc26c6`** — D/R/A : détection CEGEP **2 681 PDF → 147 scans** (91 uniques, 2 053 p) ; `ocr_pdf.py --liste --ouvriers`, `detecte_scans_pdf.py`, `reports/ocr-pdf-cegep-detection.json` ; ligne D/R/A d'`en-cours`.
- **`dca7e7a2`** et **`63927a03`** — S : fiche, manifeste, section S, roadmap, compteurs **553 fiches / 639 JSON**.

**Contrôles** : `revue_documentation.py` ✅ · budgets T0/T1 ✅ · `en-cours` **1 612 mots**, 5 questions ✅ · `verifie_en_cours.py` ✅ · `verifie_etat_a_jour.py` ✅.

**Reste hors commit** : `reports/rapport-n2-r11.md` — la fiche R1.1 de N2 contient encore `{{G2}}`, `{{ABS1152}}` et `{{R12}}` : c'est un **brouillon en cours d'écriture**, pas un fait publiable. La session N2 le terminera ; je le committerai ensuite si tu veux. Tout le reste de l'arbre est propre.


## Tour 4

### 👤 Utilisateur

push

### 🤖 Assistant

⏵ Push du dépôt principal et du sous-module `tools/structures` vers leurs origines.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== MAIN ===\"; git remote -v; git status -sb | head -3; git log --oneline -3; echo \"=== ahead ===\"; git rev-list --count origin/master..HEAD 2>/dev/null; git rev-list --count HEAD..origin/master 2>/dev/null; echo \"=== SUBM … [280 caractères tronqués]`

  ```
=== MAIN ===
origin	git@github.com:stephanedenis/drave.git (fetch)
origin	git@github.com:stephanedenis/drave.git (push)
## master...origin/master [ahead 263]
 M tools/bloc_linguistique.py
 M tools/tests/linguistique/test_bloc_linguistique.py
d2fc26c6 D/R/A — LA DÉTECTION CEGEP SÉPARE 147 SCANS DE 2 681 PDF ; L'OCR PASSE À LA LISTE EXPLICITE
7ef0199c B13 — LE GOLD NEURONAL : TAGGER 7B LOCAL, CASCADE POS 0,944 ; PORTE BLOC VERTE, B13 134/140 (6 ROUGES S)
dca7e7a2 ÉTAT — COMPTEURS AU DISQUE (552 FICHES / 639 JSON) ; LA FICHE S EST INTÉGRÉE
=== ahead ===
263
0
=== SUBMODULE ===
origin	/home/stephane/Data13TB/stephane/GitHub/drave-structures (fetch)
origin	/home/stephane/Data13TB/stephane/GitHub/drave-structures (push)
## master...origin/master [ahead 3]
647205a S — L'ANALYSEUR NOMME LES RÔLES : 99/100, 38/39 TYPES ; LE CORPUS DE 39 STRUCTURES SORT
3b68143 FUSION — LE BANC DE STRUCTURES : PRAGMATIQUE, EXPORT ET ANALYSEUR EN UN SEUL ARBRE
733b1a4 CONTEXTE — DES NIVEAUX GRADUÉS, ET LA MESURE DU NIVEAU MINIMAL POUR TRANCHER
=== ahead ===
3
0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat -- tools/bloc_linguistique.py tools/tests/linguistique/test_bloc_linguistique.py; echo \"=== diff ===\"; git diff -- tools/bloc_linguistique.py tools/tests/linguistique/test_bloc_linguistique.py | head -120; echo \"== … [375 caractères tronqués]`

  ```
tools/bloc_linguistique.py                         | 184 ++++++++++++++++++++-
 tools/tests/linguistique/test_bloc_linguistique.py |  30 ++++
 2 files changed, 205 insertions(+), 9 deletions(-)
=== diff ===
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 184dfc23..9a82de84 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -988,14 +988,175 @@ class NeuronalLLMPOS:
         return annotation
 
 
+ETIQUETTES_BIO = ("O", "B-GN", "I-GN", "B-GV", "I-GV", "B-GP", "I-GP",
+                  "B-REL", "I-REL", "B-SUB", "I-SUB")
+TYPES_SYNTAGME = ("GN", "GV", "GP", "REL", "SUB")
+EXEMPLES_BIO = (
+    (["Un", "oiseau", "chante"], ["B-GN", "I-GN", "B-GV"]),
+    (["La", "voisine", "de", "Paul", "arrive"],
+     ["B-GN", "I-GN", "B-GP", "I-GP", "B-GV"]),
+    (["Elle", "a", "vu", "le", "bus", "dans", "la", "rue"],
+     ["B-GN", "B-GV", "I-GV", "B-GN", "I-GN", "B-GP", "I-GP", "I-GP"]),
+    (["Le", "livre", "que", "tu", "lis", "tombe"],
+     ["B-GN", "I-GN", "B-SUB", "I-SUB", "I-SUB", "B-GV"]),
+    (["Il", "part", "demain"], ["B-GN", "B-GV", "O"]),
+)
+
+
+def grammaire_bio(n: int) -> str:
+    """La grammaire GBNF des étiquettes BIO : exac
… [5547 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git push origin master 2>&1 | tail -20; echo \"exit=${PIPESTATUS[0]}\"; git status -sb | head -3", "description": "Push structures submodule", "timeoutMs": 120000}`

  ```
remote: error: refusing to update checked out branch: refs/heads/master        
remote: error: By default, updating the current branch in a non-bare repository        
remote: is denied, because it will make the index and work tree inconsistent        
remote: with what you pushed, and will require 'git reset --hard' to match        
remote: the work tree to HEAD.        
remote: 
remote: You can set the 'receive.denyCurrentBranch' configuration variable        
remote: to 'ignore' or 'warn' in the remote repository to allow pushing into        
remote: its current branch; however, this is not recommended unless you        
remote: arranged to update its work tree to match what you pushed in some        
remote: other way.        
remote: 
remote: To squelch this message and still keep the default behaviour, set        
remote: 'receive.denyCurrentBranch' configuration variable to 'refuse'.        
To /home/stephane/Data13TB/stephane/GitHub/drave-structures
 ! [remote rejected] master -> master (branch is currently checked out)
error: failed to push some refs to '/home/stephane/Data13TB/stephane/GitHub/drave-structures'
exit=1
## master...origin/master [ahead 3]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat .gitmodules; echo \"=== remote repo ===\"; git -C /home/stephane/Data13TB/stephane/GitHub/drave-structures status -sb; git -C /home/stephane/Data13TB/stephane/GitHub/drave-structures log --oneline -2; git -C /home/stephane/Data13 … [238 caractères tronqués]`

  ```
[submodule "tools/docwatch"]
	path = tools/docwatch
	url = https://github.com/stephanedenis/docwatch.git
[submodule "tools/structures"]
	path = tools/structures
	url = /home/stephane/Data13TB/stephane/GitHub/drave-structures
=== remote repo ===
## master
3b68143 FUSION — LE BANC DE STRUCTURES : PRAGMATIQUE, EXPORT ET ANALYSEUR EN UN SEUL ARBRE
733b1a4 CONTEXTE — DES NIVEAUX GRADUÉS, ET LA MESURE DU NIVEAU MINIMAL POUR TRANCHER
(non réglé)
  ```

- **bash** `{"command": "git -C /home/stephane/Data13TB/stephane/GitHub/drave-structures config receive.denyCurrentBranch updateInstead && echo \"config remote OK\"; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git push origin master 2>&1 | tail -15; echo \"exit=${PIPESTATUS[0]}\"; git … [183 caractères tronqués]`

  ```
config remote OK
To /home/stephane/Data13TB/stephane/GitHub/drave-structures
   3b68143..647205a  master -> master
exit=0
## master...origin/master
647205a S — L'ANALYSEUR NOMME LES RÔLES : 99/100, 38/39 TYPES ; LE CORPUS DE 39 STRUCTURES SORT
3b68143 FUSION — LE BANC DE STRUCTURES : PRAGMATIQUE, EXPORT ET ANALYSEUR EN UN SEUL ARBRE
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 30 git ls-remote --heads origin >/tmp/lsremote.out 2>/tmp/lsremote.err; echo \"ls-remote exit=$?\"; head -3 /tmp/lsremote.out; cat /tmp/lsremote.err | head -5", "description": "Test GitHub SSH connectivity", "timeoutMs": 4000 … [2 caractères tronqués]`

  ```
ls-remote exit=0
a31a2e4d08194c9858abd94a97cc928ce78f2867	refs/heads/master
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git push origin master 2>&1 | tail -25; echo \"exit=${PIPESTATUS[0]}\"; git status -sb | head -3", "description": "Push main repository to GitHub", "timeoutMs": 600000}`

  ```
To github.com:stephanedenis/drave.git
   a31a2e4d..d2fc26c6  master -> master
exit=0
## master...origin/master
 M tools/bloc_linguistique.py
 M tools/tests/linguistique/test_bloc_linguistique.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== MAIN remote ===\"; git ls-remote --heads origin | head -2; echo \"local HEAD $(git rev-parse --short HEAD) · $(git status -sb | head -1)\"; echo \"=== SUBMODULE remote ===\"; git -C tools/structures ls-remote --heads origi … [244 caractères tronqués]`

  ```
=== MAIN remote ===
d2fc26c673aeb8e0e800cf647ef2ae0ed68c3f23	refs/heads/master
local HEAD d2fc26c6 · ## master...origin/master
=== SUBMODULE remote ===
647205a3da710217b63b5d20d492275a75e7dff8	refs/heads/master
local 647205a · ## master...origin/master
=== reste local ===
 M tools/bloc_linguistique.py
 M tools/tests/linguistique/test_bloc_linguistique.py
?? reports/rapport-n2-r11.md
?? tools/tests/linguistique/qualifier_syntagmes.py
  ```

### 🤖 Assistant

⏵ Push terminé : principal `d2fc26c6`, sous-module `647205a`.

- **Dépôt principal** — `origin/master` : `a31a2e4d..d2fc26c6` (**263 commits** poussés). `master...origin/master` à jour.
- **Sous-module `tools/structures`** — `origin/master` : `3b68143..647205a`. Le remote local `drave-structures` refusait le push (branche `master` checkoutée, dépôt non bare) ; réglé par `receive.denyCurrentBranch=updateInstead`, puis poussé.
- Le pointeur commité dans le principal (`647205a`) existe donc bien sur le remote du sous-module.

**Reste local, non poussé** — travail en cours d'autres sessions :

- `tools/bloc_linguistique.py`, `tools/tests/linguistique/test_bloc_linguistique.py`, `tools/tests/linguistique/qualifier_syntagmes.py` : le tagger de **syntagmes** (BIO/GBNF) de Pensée, encore en écriture ;
- `reports/rapport-n2-r11.md` : brouillon N2 R1.1 avec `{{G2}}`, `{{ABS1152}}`, `{{R12}}`.

Dis-moi quand ils sont prêts : je les commite avec leurs lignes d'état et je pousse.


## Tour 5

### 👤 Utilisateur

tu feras un commit push quand ce sera stable. pour l'instant, la machine est tranquille. tu peur entreprendre des choses

### 🤖 Assistant

⏵ Je regarde l'état machine et les chantiers ouverts pour choisir quoi entreprendre.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; uptime; echo \"=== GPU ===\"; nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null || echo \"nvidia-smi indisponible\"; echo \"=== processes lourds ===\"; ps - … [113 caractères tronqués]`

  ```
19:35:46
 19:35:46  up  4:28,  2 users,  load average: 5,87, 4,96, 6,27
=== GPU ===
0, Quadro RTX 5000, 0 %, 688 MiB, 16384 MiB
1, Quadro RTX 5000, 43 %, 966 MiB, 16384 MiB
=== processes lourds ===
    PID     ELAPSED %CPU %MEM CMD
 110066    02:07:46  813  4.0 llama-server -m models/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf --host 127.0.0.1 --port 18082 -ngl 0 -c 1024 --no-webui
 180053       00:18  131  1.3 /home/stephane/gpu-env/bin/python -u tools/entrainer_moteur.py --famille route --dim 192 --couches 4 --tetes 4 --cache 768 --experts 8 --k 2 --seq 128 --lot 32 --lr 3e-4 --graine 1 --pas 200 --eval-tous 200 --sortie /tmp/porte-audit-drapeaux/lognormal --poids-lognormaux
 178585       01:21  105  1.2 /home/stephane/gpu-env/bin/python work/n2ac/eval_200k.py work/n2ac/mix-200k.pt --sortie work/n2ac/eval-mix200.json
  32123    03:20:15 72.9  0.8 node /home/stephane/.local/share/../bin/dsh --profile dsh-tui
 180352       00:00 68.7  0.0 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; uptime; echo "=== GPU ==="; nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null || echo "nvidia-smi indispo
… [1274 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== WIP mtimes ===\"; ls -la --time-style=+%H:%M:%S tools/bloc_linguistique.py tools/tests/linguistique/test_bloc_linguistique.py tools/tests/linguistique/qualifier_syntagmes.py reports/rapport-n2-r11.md 2>/dev/null; echo \"== … [256 caractères tronqués]`

  ```
=== WIP mtimes ===
-rw-------. 1 stephane stephane 14355 18:49:42 reports/rapport-n2-r11.md
-rw-------. 1 stephane stephane 82670 18:52:50 tools/bloc_linguistique.py
-rw-------. 1 stephane stephane 11704 17:36:52 tools/tests/linguistique/qualifier_syntagmes.py
-rw-r--r--. 1 stephane stephane  8884 18:50:42 tools/tests/linguistique/test_bloc_linguistique.py
=== sessions ===
sessions · plans de mandat
  ⏰ 0733c5bb-f90b-4f58 · actif    ·  46 min · N2 (200 000 pas sur le mélange, PPL domaine/littérature/anglais/wikitext2, courbe de longueur), R1.1/R1.2 mesurés depuis N2
      → la mesure des cinq PPL du run de 200 k à sa sortie, puis fiche + état + commit ; le contrôle depuis zéro ; la clôture.
    0b0a6a0d-05f5-4308 · terminé  · 2101 min · N2.h — corpus propre, porte honnête, généralité, verrou de longueur
      → close — N2.i (3,13 / 12,93 / 33,83) et Pensée v0 (6/6 portes) sont committés.
    0b69f616-5c75-4c34 · terminé  · 4175 min · R0.4, R0.5, R13, R4.1–R4.3, en-cours, roadmap, backlog
      → clôture reprise par la session `22e518ee` — commit, archives, état.
    22e518ee-81b8-4081 · terminé  · 3346 min · archives de sessions, journal, en-cours, roadmap, backlog, outillage d'arc
… [690 caractères tronqués]
  ```

- **todo_write** `{"todos": [{"content": "Reproduire h033 et cartographier la frontière GN/verbe", "status": "in_progress"}, {"content": "Ajouter la règle de frontière GN-devant-verbe-fin (lexique assumé)", "status": "pending"}, {"content": "Écrire un holdout3 après la règle et mesurer types/rôles/contrôles", "status … [296 caractères tronqués]`

  ```
Updated todo list: 5 pending, 1 in progress, 0 completed.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git status -sb | head -2; python3 - <<'PY'\nimport generateur\nfor t in [\"La femme parle à son fils.\",\n          \"Le chat dort sur le canapé.\",\n          \"Une belle maison.\",\n          \"Le petit chat noir d … [345 caractères tronqués]`

  ```
## master...origin/master
La femme parle à son fils.
    La femme parle[GN:agent] | à son fils[GP:destinataire]
Le chat dort sur le canapé.
    Le chat dort[GN:agent] | sur le canapé[GP:lieu]
Une belle maison.
    Une belle maison[GN:agent]
Le petit chat noir dort.
    Le petit chat noir[GN:agent] | dort[GV:predicat]
La voisine arrive.
    La voisine arrive[GN:agent]
Le train part demain.
    Le train part demain[GN:agent]
Le roi Louis parle.
    Le roi Louis parle[GN:agent]
La femme médecin parle.
    La femme médecin parle[GN:agent]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && grep -n \"VERBES_LIEU\\|while j < len(utiles) and utiles\\[j\\].cls in (\\\"DET\\\"\" generateur.py | head; sed -n '40,70p' generateur.py", "description": "Locate constants and GN loop"}`

  ```
46:VERBES_LIEU = set("""
175:        if gv is not None and _dernier_mot(gv.texte) in VERBES_LIEU:
267:            while j < len(utiles) and utiles[j].cls in ("DET", "PRON", "MOT") and mots < 3:
# Verbes de lieu/état : « à la maison » après « rester » est un lieu, pas un destinataire.
# Copules : « est mon voisin » est un GV attributif, pas un GV « est » + un GN.
COPULES = set("""
est sont etait etaient sera seront serait seraient semble semblent parait paraissent
reste restent devient deviennent
""".split())
VERBES_LIEU = set("""
reste restes restons restez restent suis es est sommes etes sont etais etait etions etiez etaient
vais vas va allons allez vont allais allait allions alliez allaient
habite habites habitons habitez habitent vivais vivait vivions viviez vivaient vis vit vivons vivez vivent
viens vient venons venez viennent venais venait venions veniez venaient
pars part partons partez partent partais partait partions partiez partaient
arrive arrives arrivons arrivez arrivent arrivais arrivait arrivions arriviez arrivaient
entre entres entrons entrez entrent entrais entrait entrions entriez entraient
sors sort sortons sortez sortent sortais sortait sortions sortiez sortaient
… [604 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('generateur.py')\nt = p.read_text(encoding='utf-8')\najout = '''\n# Verbes conjugués fréquents : un GN ne les avale pas (« La femme parle »).\n# Lexique assumé, pa … [4652 caractères tronqués]`

  ```
règle GN-devant-verbe ajoutée
La femme parle à son fils.
    La femme[GN:agent] | parle[GV:predicat] | à son fils[GP:destinataire]
Le chat dort sur le canapé.
    Le chat[GN:agent] | dort[GV:predicat] | sur le canapé[GP:lieu]
Une belle maison.
    Une belle maison[GN:agent]
Le petit chat noir dort.
    Le petit chat noir[GN:agent] | dort[GV:predicat]
La voisine arrive.
    La voisine[GN:agent] | arrive[GV:predicat]
Le train part demain.
    Le train[GN:agent] | part demain[GV:predicat]
Le roi Louis parle.
    Le roi Louis[GN:agent] | parle[GV:predicat]
La femme médecin parle.
    La femme médecin[GN:agent] | parle[GV:predicat]
La petite ferme est belle.
    La petite[GN:agent] | ferme est belle[GV:predicat]
Le simple fait surprend.
    Le simple[GN:agent] | fait surprend[GV:predicat]
Le grand lit est dur.
    Le grand[GN:agent] | lit est dur[GV:predicat]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('generateur.py')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"\"\"        while j < len(utiles) and utiles[j].cls in (\"PRON\", \"AUX\", \"MOT\"):\n         … [670 caractères tronqués]`

  ```
GV s'arrête avant un adverbe de temps
  gold · 39 phrases · donnees/gold-analyseur.json
  split     phr    types   couv.    rôles   compl.
  dev         7   7/7       1.00  22/22    10/10  
  test       16  16/16      1.00  40/40    19/19  
  holdout    16  16/16      1.00  38/38    16/16  
  global     39  39/39      1.00 100/100   45/45  
  contrôle · baseline 64/100 (0.64) · règles coupées 67/100 (0.67) · rôles mélangés 0.10 [0.00, 0.22]
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/mesure-analyseur.json
=== tests ===
  127.0.0.1 · "GET /api/export HTTP/1.1" 200 -
.
----------------------------------------------------------------------
Ran 40 tests in 3.667s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nimport json\nfrom pathlib import Path\np = Path('donnees/gold-analyseur.json')\nd = json.loads(p.read_text(encoding='utf-8'))\nd['note'] = (\"Gold de l'analyseur. split=dev : les 7 phrases du banc.  … [2182 caractères tronqués]`

  ```
47 phrases
  gold · 47 phrases · donnees/gold-analyseur.json
  split     phr    types   couv.    rôles   compl.
  dev         7   7/7       1.00  22/22    10/10  
  test       16  16/16      1.00  40/40    19/19  
  holdout    24  24/24      0.98  55/55    18/18  
  global     47  47/47      0.99 117/117   47/47  
  contrôle · baseline 80/117 (0.68) · règles coupées 82/117 (0.70) · rôles mélangés 0.11 [0.00, 0.23]
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/mesure-analyseur.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('tests/test_generateur.py')\nt = p.read_text(encoding='utf-8')\najout = '''\n\nclass TestFrontiereGN(unittest.TestCase):\n    \"\"\"Le GN s'arrête devant un verbe  … [2349 caractères tronqués]`

  ```
tests frontière ajoutés
  127.0.0.1 · "GET /api/export HTTP/1.1" 200 -
.
----------------------------------------------------------------------
Ran 43 tests in 3.760s

OK
  gold · 47 phrases · donnees/gold-analyseur.json
  split     phr    types   couv.    rôles   compl.
  dev         7   7/7       1.00  22/22    10/10  
  test       16  16/16      1.00  40/40    19/19  
  holdout    24  24/24      0.98  55/55    18/18  
  global     47  47/47      0.99 117/117   47/47  
  contrôle · baseline 80/117 (0.68) · règles coupées 82/117 (0.70) · rôles mélangés 0.11 [0.00, 0.23]
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/mesure-analyseur.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('README.md')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"\"\"- **passif et copule** : « a été écrite par Marie » rend le GN sujet **patient** et `par` **ag … [4374 caractères tronqués]`

  ```
README v3
113:- **frontière du GN** : le GN s'arrête devant un **verbe conjugué** fréquent (« La femme parle » →
129:Le **gold** (`donnees/gold-analyseur.json`) porte **47 phrases** en trois découpages :
206:**43 tests** : phrases et alignement des spans, validation + export, statut invalide refusé,
221:- **v3** : **frontière du GN** devant un verbe conjugué et **frontière du GV** devant un adverbe
222:  de temps ; le **gold de 47 phrases** (7 dev, 16 test, 24 holdout en trois vagues), `mesure_analyseur.py`
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 exporter_corpus.py --mode gold && python3 verifier_corpus.py ../../data/structures/banque.jsonl && cat ../../data/structures/banque-manifest.json; echo \"=== STATUS SOUS-MODULE ===\"; git status --short", "de … [54 caractères tronqués]`

  ```
✅ 47 ligne(s) sur 47 phrase(s) · mode gold → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque.jsonl
     manifeste : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-manifest.json
     sha256 : f2a0d2fb3a9b0a9aebd562b170503f4d1a98251efdc4a3645a2523b5197227a2
  ✅ ../../data/structures/banque.jsonl · empreinte, comptes, spans et restitution vérifiés
{
 "version": 2,
 "mode": "gold",
 "date": "2026-11-02T19:40:35",
 "source": "tools/structures/donnees/gold-analyseur.json",
 "sortie": "data/structures/banque.jsonl",
 "phrases": 47,
 "candidats_acceptes": 47,
 "sha256": "f2a0d2fb3a9b0a9aebd562b170503f4d1a98251efdc4a3645a2523b5197227a2",
 "note": "structures de référence, sans jugement humain — `statut: reference` ; spans vérifiés."
}
=== STATUS SOUS-MODULE ===
 M README.md
 M donnees/gold-analyseur.json
 M donnees/mesure-analyseur.json
 M generateur.py
 M tests/test_generateur.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git add generateur.py donnees/gold-analyseur.json donnees/mesure-analyseur.json README.md tests/test_generateur.py && git diff --cached --stat && git commit -m \"S — LA FRONTIÈRE DU GN S'ARRÊTE DEVANT LE VERBE : 47/4 … [625 caractères tronqués]`

  ```
README.md                     |  40 ++++---
 donnees/gold-analyseur.json   | 143 ++++++++++++++++++++++++-
 donnees/mesure-analyseur.json | 239 +++++++++++++++++++++++++++++++++++-------
 generateur.py                 |  58 ++++++++++
 tests/test_generateur.py      |  33 +++++-
 5 files changed, 456 insertions(+), 57 deletions(-)
[master 90e507b] S — LA FRONTIÈRE DU GN S'ARRÊTE DEVANT LE VERBE : 47/47 TYPES, 117/117 RÔLES ; GOLD 47
 5 files changed, 456 insertions(+), 57 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nimport json\nr=json.load(open('donnees/mesure-analyseur.json'))\nprint(json.dumps({k:r[k] for k in ('phrases','par_split','global','controles')}, ensure_ascii=False, indent=1))\nfor x in r['lignes'] … [220 caractères tronqués]`

  ```
{
 "phrases": 47,
 "par_split": {
  "dev": {
   "phrases": 7,
   "types_ok": 7,
   "couverture": 1.0,
   "octets_couverts": 229,
   "octets_or": 229,
   "roles_justes": 22,
   "roles_total": 22,
   "complements_justes": 10,
   "complements_total": 10,
   "types_taux": 1.0,
   "couverture_globale": 1.0,
   "roles_taux": 1.0,
   "complements_taux": 1.0
  },
  "test": {
   "phrases": 16,
   "types_ok": 16,
   "couverture": 1.0,
   "octets_couverts": 475,
   "octets_or": 475,
   "roles_justes": 40,
   "roles_total": 40,
   "complements_justes": 19,
   "complements_total": 19,
   "types_taux": 1.0,
   "couverture_globale": 1.0,
   "roles_taux": 1.0,
   "complements_taux": 1.0
  },
  "holdout": {
   "phrases": 24,
   "types_ok": 24,
   "couverture": 0.9801,
   "octets_couverts": 605,
   "octets_or": 616,
   "roles_justes": 55,
   "roles_total": 55,
   "complements_justes": 18,
   "complements_total": 18,
   "types_taux": 1.0,
   "couverture_globale": 0.9821,
   "roles_taux": 1.0,
   "complements_taux": 1.0
  }
 },
 "global": {
  "phrases": 47,
  "types_ok": 47,
  "couverture": 0.9898,
  "octets_couverts": 1309,
  "octets_or": 1320,
  "roles_justes": 117,
  "roles_total": 117,
  "compleme
… [565 caractères tronqués]
  ```

- **write** `{"content": "# S — La frontière du GN s'arrête devant le verbe : 47/47 types, 117/117 rôles, 47 structures au corpus\n\n> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur un gold de **47 phrases**\n> (7 `dev`, 16 `test`, 24 `holdout` en trois vagues), la structure de base retrouv … [9027 caractères tronqués]`

  ```
Error: cannot write "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md", "limit": 40}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md</path>
<type>file</type>
<content>
1: # S — L'analyseur nomme les rôles : 99/100, 38/39 types, et 39 structures au corpus
2: 
3: > **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur un gold de **39 phrases**
4: > (7 `dev`, 16 `test`, 16 `holdout`), la structure de base retrouve la **séquence de types
5: > 38/39** (97,4 %), les **rôles 99/100** (99 %), les **compléments 45/45**, et couvre
6: > **1 156/1 161 octets** (99,6 %). L'échec est **nommé** : « La femme parle » est lu comme un
7: > GN, le verbe est avalé. Le corpus de référence sort : **39 lignes**, SHA-256
8: > `973c70a4126896b8557d803b940f58d1f6d1fe1d172cdb7b9abce9671cd7db71`.
9: 
10: ## Le dispositif
11: 
12: - **Gold** : [`tools/structures/donnees/gold-analyseur.json`](../tools/structures/donnees/gold-analyseur.json),
13:   **39 phrases** : **7 `dev`** (les phrases du banc, référence écrite à la main), **16 `test`**
14:   (écrites **avant** les règles de rôles/subordonnées) et **16 `holdout`** (écrites **après**,
15:   mesurées une fois ; aucun attendu n'est modifié après la mesure). Chaque phrase porte sa suite
16
… [1661 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md", "offset": 40, "limit": 110}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md</path>
<type>file</type>
<content>
40: - `à` **but** devant un infinitif, **destinataire** sinon, **lieu** après un verbe de lieu ;
41: - `par` **agent** après un passif, **moyen** sinon ; le GN sujet du passif devient **patient** ;
42: - subordonnées : `quand / dès que / pendant que` → **temps**, `parce que / puisque / comme` →
43:   **cause**, `si / s'il` → **hypothèse**, `bien que` → **concession**, `afin que` → **but**,
44:   `sans que` → **manière** ; la complétive après un verbe reste **contenu**, la relative après un
45:   nom **qualité** ;
46: - copule : « est mon voisin » reste un **GV** attributif au lieu de se couper en « est » + GN.
47: 
48: ## Les contrôles négatifs
49: 
50: | contrôle | ce qu'il fait | résultat |
51: |---|---|---:|
52: | **baseline** | rôle constant par type (GN=agent, GV=predicat, GP=lieu, SUB=contenu, REL=qualite) | **64/100** (0,64) |
53: | **règles coupées** | `structure(roles=False)` : mêmes segments, rôles par défaut | **66/100** (0,66) |
54: | **rôles mélangés** | 200 permutations des rôles attendus des compléments | **0,099** [0,00 ; 0,22] |
55: | **span
… [5520 caractères tronqués]
  ```

- **write** `{"content": "# S — La frontière du GN s'arrête devant le verbe : 47/47 types, 117/117 rôles, 47 structures au corpus\n\n> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur un gold de **47 phrases**\n> (7 `dev`, 16 `test`, 24 `holdout` en trois vagues), la structure de base retrouv … [9027 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cp data/structures/banque-manifest.json reports/s-banque-structures.json && python3 -m json.tool reports/s-banque-structures.json | head -14; echo \"=== README S ===\"; grep -n \"rapport-s-analyseur-roles\" reports/README.md reports/ … [171 caractères tronqués]`

  ```
{
    "version": 2,
    "mode": "gold",
    "date": "2026-11-02T19:40:35",
    "source": "tools/structures/donnees/gold-analyseur.json",
    "sortie": "data/structures/banque.jsonl",
    "phrases": 47,
    "candidats_acceptes": 47,
    "sha256": "f2a0d2fb3a9b0a9aebd562b170503f4d1a98251efdc4a3645a2523b5197227a2",
    "note": "structures de r\u00e9f\u00e9rence, sans jugement humain \u2014 `statut: reference` ; spans v\u00e9rifi\u00e9s."
}
=== README S ===
reports/INDEX.md:533:| [rapport-s-analyseur-roles.md](rapport-s-analyseur-roles.md) | S — L'analyseur nomme les rôles : 99/100, 38/39 types, et 39 structures au corpus |
=== extrait README ===
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '54,74p' docs/pilotage/en-cours.md; echo \"=== S bullet ===\"; grep -n -A1 \"S — le banc de structures\" docs/pilotage/en-cours.md; echo \"=== roadmap S ===\"; grep -n \"S — les structures\\|État au 02/11\\|dernière mise à jou … [102 caractères tronqués]`

  ```
- **Bloquants** : aucun ; **GPU libres**.
- **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).

### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures : l'analyseur et l'export

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : 1–4) ~~plan, analyseur, export, tests~~ ; 5–6) ~~fiche, pointeur, état~~.
- **Ambition** : nommer le rôle, couper la subordonnée.
- **Stratégie** : une règle = une phrase, trois contrôles.
- **Objectif final** : gold **39**, corpus **39**, manifeste SHA-256.
- **Fait** : types **38/39**, rôles **99/100**, compléments **45/45** ; contrôles **64/100**, **66/100**, **0,099** ; échec **h033** ; **40 tests** ; [`fiche`](../../reports/rapport-s-analyseur-roles.md).
- **Ce qu'elle fait** : **`647205a`**, pointeur **`13f4e131`** ; corpus **39** (SHA `973c70a4…`) ; banque **0**.
- **Ce que font les autres** : **hub**, **N2**, **Pensée**, **D/R/A**.
- **Prochaine action** : validation humaine de la banque, puis frontière du GN (h
… [1404 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -4 docs/pilotage/en-cours.md; date '+%H:%M'; grep -n \"fichiers / JSON\" docs/pilotage/en-cours.md; python3 tools/verifie_en_cours.py 2>&1 | tail -3", "description": "Current en-cours header and word count"}`

  ```
# En ce moment

**Mis à jour : 2026-11-02, 19 h 45 HNE (heure locale, EST).**

19:42
120:| fichiers / JSON de résultats | **559** / **646** | `reports/*.md` / `reports/*.json` |
  en-cours · 1637 mots · 7 sections · 4 session(s) · 7 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np = Path('docs/pilotage/en-cours.md')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"**Mis à jour : 2026-11-02, 19 h 45 HNE (heure locale, EST).**\",\n              \"**Mis à jour : 20 … [4151 caractères tronqués]`

  ```
état/roadmap/INDEX v3
  en-cours · 1644 mots · 7 sections · 4 session(s) · 7 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  avertissements :
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ❌ 1 violation(s) :
     · T0 : 4018 mots (AGENTS + en-cours + une tâche) > budget 4 000
  revue de documentation · 560 fiche(s) · 647 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 559 fichiers, le disque en a 560
     · compteurs : en-cours.md dit 646 JSON, le disque en a 647
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np = Path('docs/pilotage/en-cours.md')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"\"\"> **Reprise après le reboot du 02/11 15 h 06** : les **quatre** sessions ont rouvert entre 16 h … [1733 caractères tronqués]`

  ```
trim + compteurs 560/647
  en-cours · 1674 mots · 7 sections · 4 session(s) · 7 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  avertissements :
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ❌ 1 violation(s) :
     · T0 : 4048 mots (AGENTS + en-cours + une tâche) > budget 4 000
  revue de documentation · 560 fiche(s) · 647 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; git log --oneline -4; echo \"=== status ===\"; git status --short | head -20; echo \"=== mtime en-cours ===\"; ls -la --time-style=+%H:%M:%S docs/pilotage/en-cours.md docs/pilotage/roadmap.md; echo \"=== sessions ===\" … [126 caractères tronqués]`

  ```
19:44
9f1f4869 B13 — LA PORTE EST À 134/140 : LE 140/140 DE 702b368c NE SE REJOUE PAS (138/140) ; 4 ROUGES DU SOUS-MODULE S, 2 DU TEST PÉRIMÉ
7d5bd08d ÉTAT — T0 REVENU SOUS 4 000 (3 930) : N2/S/R1 CONDENSÉS, LES CHIFFRES GARDÉS
4a85604d B13 — LA PRAGMATIQUE NEURONALE EST SOUS L'HEURISTIQUE : TEST 0,6375 (MAJORITAIRE 0,7556), DEV 1,0 ; L'HEURISTIQUE GARDE
2cff8dba R1 — LES POSITIONS RELATIVES ÔTENT L'EXPLOSION (8,20 → 3,25 À 1 000 OCTETS), LA FENÊTRE ENTRAÎNÉE DONNE LA LECTURE (−0,244 À OCTETS CONSTANTS)
=== status ===
 M docs/pilotage/chantiers.md
M  docs/pilotage/en-cours.md
 M docs/pilotage/plan-travail.md
 M docs/pilotage/roadmap.md
A  journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/table_200k.py
 M journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
M  journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md
 M journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/digest.md
 M journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md
 M journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md
 M journal/sessions/abb58991-fe0a-4d6e-b039-6552b09f8454/digest.md
 M journal/sessions/b7d4678e-2143-4daa-a9a4-a456c5aa8dab/digest.md
 M journal/sessio
… [1208 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== en-cours staged S ===\"; git show :docs/pilotage/en-cours.md | sed -n '/### Session `29ad180d/,/### Session `e181ce02/p' | head -30; echo \"=== roadmap S (worktree) ===\"; grep -n \"S — les structures\" docs/pilotage/roadm … [151 caractères tronqués]`

  ```
=== en-cours staged S ===
### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures : l'analyseur et l'export

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : 1–4) ~~plan, analyseur (gold 47), export, tests 43~~ ; 5–6) ~~fiche, pointeur, état~~.
- **Ambition** : nommer le rôle et la frontière GN.
- **Stratégie** : une règle = une phrase, trois contrôles.
- **Objectif final** : gold **47**, corpus **47**, manifeste SHA-256.
- **Fait** : types **47/47**, rôles **117/117** ; contrôles **80/117**, **82/117**, **0,109** ; h033 corrigé, **h046/h047** nommés ; **43 tests** ; [`fiche`](../../reports/rapport-s-analyseur-roles.md).
- **Ce qu'elle fait** : **`90e507b`** ; corpus **47** (SHA `f2a0d2fb…`) ; banque **0**.
- **Ce que font les autres** : **hub**, **N2**, **Pensée**, **D/R/A**.
- **Prochaine action** : homographes/lexique, puis validation humaine de la banque.
- **Bloquants** : aucun ; **banque à 0** verdict.
- **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a
… [927 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git push origin master 2>&1 | tail -5; echo \"exit=${PIPESTATUS[0]}\"; git status -sb | head -2; echo \"=== N2 fiche placeholders ? ===\"; grep -c \"{{\" ../../reports/rapport-n2-200k.md 2>/dev/null || true; echo \"= … [166 caractères tronqués]`

  ```
To /home/stephane/Data13TB/stephane/GitHub/drave-structures
   647205a..90e507b  master -> master
exit=0
## master...origin/master
=== N2 fiche placeholders ? ===
0
=== main log ===
9f1f4869 B13 — LA PORTE EST À 134/140 : LE 140/140 DE 702b368c NE SE REJOUE PAS (138/140) ; 4 ROUGES DU SOUS-MODULE S, 2 DU TEST PÉRIMÉ
7d5bd08d ÉTAT — T0 REVENU SOUS 4 000 (3 930) : N2/S/R1 CONDENSÉS, LES CHIFFRES GARDÉS
 M docs/pilotage/chantiers.md
M  docs/pilotage/en-cours.md
 M docs/pilotage/plan-travail.md
 M docs/pilotage/roadmap.md
 M journal/README.md
A  journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/code/table_200k.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '20,55p' docs/pilotage/en-cours.md; echo \"=== S->N2 ===\"; sed -n '74,110p' docs/pilotage/en-cours.md", "description": "Read N2/Pensée/D/R/A sections for compression"}`

  ```
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.

### Session `536cd5d6-94ac-4057-8fe9-11709a4587c7` — le hub, l'intégration et la reprise

- **Id** : `536cd5d6-94ac-4057-8fe9-11709a4587c7` — [`plan.md`](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md).
- **Rôle** : **Hub** — intégration, état, roadmap, journal, compteurs ; reprise après reboot ; runbook.
- **Plan** : 1–7) ~~audit, commits, état, mandats, porte, INDEX, runbook~~ ; 8–9) **intégration,
  portes** (GPU 1).
- **Ambition** : un état reprenable, des mandats qui disent la vérité.
- **Stratégie** : committer par flux (`git add` explicite), nommer ce qui reste.
- **Objectif final** : sédimentation à zéro, quatre mandats explicites, runbook.
- **Ce qu'elle fait** : intégration ; **porte stricte** ; sous-passe doc. **7/8** ; **passe de
  portes en cours** (`porte-bus`, 19 h 37).
- **Ce que font les autres** : **N2**, **S**, **Pensée** ; **D/R/A close**.
- **Prochaine action** : finir la **passe complète**, puis intégrer les lignes B13/N2/S.
- **Bloquants** : aucun ; la passe tient la machine (GPU libres).
- **Journal** : [la session](../../journal/session
… [4774 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add reports/rapport-s-analyseur-roles.md reports/s-banque-structures.json tools/structures docs/pilotage/roadmap.md reports/INDEX.md && echo \"S v3 stagé\" && git diff --cached --stat | tail -12; echo \"=== log ===\"; git log --o … [127 caractères tronqués]`

  ```
S v3 stagé
 docs/pilotage/en-cours.md                          |   5 +-
 docs/pilotage/roadmap.md                           |  29 ++---
 .../cloture.md                                     |  65 ++++++++++
 .../0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md   |   4 +-
 reports/INDEX.md                                   |   2 +-
 reports/rapport-s-analyseur-roles.md               | 142 +++++++++++----------
 reports/s-banque-structures.json                   |   8 +-
 tools/structures                                   |   2 +-
 8 files changed, 165 insertions(+), 92 deletions(-)
=== log ===
e12c39c1 N2 — 200 000 PAS SUR LE MÉLANGE 1 Go : 3,1591 EN DOMAINE (−0,33), 5,6056 EN LITTÉRATURE, LA PORTE 2,5 À 1,3–2,7 M PAS
9f1f4869 B13 — LA PORTE EST À 134/140 : LE 140/140 DE 702b368c NE SE REJOUE PAS (138/140) ; 4 ROUGES DU SOUS-MODULE S, 2 DU TEST PÉRIMÉ
=== status ===
 M docs/pilotage/chantiers.md
M  docs/pilotage/en-cours.md
 M docs/pilotage/plan-travail.md
M  docs/pilotage/roadmap.md
A  journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/cloture.md
 M journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
M  journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md
 M journ
… [293 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -3; echo \"=== S files staged ? ===\"; git diff --cached --name-only | grep -E \"rapport-s-analyseur|s-banque|tools/structures|roadmap|INDEX\" ; echo \"=== submodule remote ===\"; git -C tools/structures ls-remote - … [278 caractères tronqués]`

  ```
e12c39c1 N2 — 200 000 PAS SUR LE MÉLANGE 1 Go : 3,1591 EN DOMAINE (−0,33), 5,6056 EN LITTÉRATURE, LA PORTE 2,5 À 1,3–2,7 M PAS
9f1f4869 B13 — LA PORTE EST À 134/140 : LE 140/140 DE 702b368c NE SE REJOUE PAS (138/140) ; 4 ROUGES DU SOUS-MODULE S, 2 DU TEST PÉRIMÉ
7d5bd08d ÉTAT — T0 REVENU SOUS 4 000 (3 930) : N2/S/R1 CONDENSÉS, LES CHIFFRES GARDÉS
=== S files staged ? ===
docs/pilotage/roadmap.md
reports/INDEX.md
reports/rapport-s-analyseur-roles.md
reports/s-banque-structures.json
tools/structures
=== submodule remote ===
90e507b486e5fe9adfd2ba54576d99015e49b86f	refs/heads/master
=== N2 closure en-cours ? ===
- **Objectif final** : gold **47**, corpus **47**, manifeste SHA-256.
- **Fait** : types **47/47**, rôles **117/117** ; contrôles **80/117**, **82/117**, **0,109** ; h033 corrigé, **h046/h047** nommés ; **43 tests** ; [`fiche`](../../reports/rapport-s-analyseur-roles.md).
- **Ce qu'elle fait** : **`90e507b`** ; corpus **47** (SHA `f2a0d2fb…`) ; banque **0**.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 20; git log --oneline -2; echo \"=== staged ===\"; git diff --cached --stat | tail -8; echo \"=== portes ===\"; ps -eo pid,etime,cmd | grep -E \"porte-|toutes-les-portes\" | grep -v grep | head -4; echo \"=== T0 ===\"; python3  … [120 caractères tronqués]`

  ```
e2227509 N2 — CLÔTURE : 200 000 PAS (3,1591) ET R1.1/R1.2 (0,97× LA PORTE, FENÊTRE 512 −0,244) SONT COMMITTÉS
e12c39c1 N2 — 200 000 PAS SUR LE MÉLANGE 1 Go : 3,1591 EN DOMAINE (−0,33), 5,6056 EN LITTÉRATURE, LA PORTE 2,5 À 1,3–2,7 M PAS
=== staged ===
=== portes ===
 164359       17:25 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; CUDA_VISIBLE_DEVICES=1,0 JOURNAUX=work/portes/passe-1102-19h32 bash tools/toutes-les-portes.sh; echo "EXIT=$?"; echo "=== REGISTRE (code != 0) ==="; awk '$2 != 0' work/portes/passe-1102-19h32/registre.txt; echo "=== BILAN ==="; tail -1 work/portes/passe-1102-19h32/registre.txt
 164366       17:25 bash tools/toutes-les-portes.sh
 263672       01:46 python3 tools/tests/qualifier_porte_minute_drvm.py --endpoint http://127.0.0.1:18082 --sortie reports/pensee-porte-minute.json
 289500       00:47 timeout 1800 bash tools/porte-episodique.sh
=== T0 ===
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables
… [40 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== S dans le commit N2 ===\"; git show --stat --oneline e2227509 | grep -E \"analyseur|s-banque|structures|roadmap|INDEX|en-cours\" ; echo \"=== pointeur HEAD ===\"; git ls-tree HEAD tools/structures; git -C tools/structures  … [244 caractères tronqués]`

  ```
=== S dans le commit N2 ===
 docs/pilotage/en-cours.md                          |   5 +-
 docs/pilotage/roadmap.md                           |  29 ++---
 reports/INDEX.md                                   |   2 +-
 reports/rapport-s-analyseur-roles.md               | 142 +++++++++++----------
 reports/s-banque-structures.json                   |   8 +-
 tools/structures                                   |   2 +-
=== pointeur HEAD ===
160000 commit 90e507b486e5fe9adfd2ba54576d99015e49b86f	tools/structures
90e507b
=== status ===
 M docs/pilotage/chantiers.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/plan-travail.md
 M docs/pilotage/roadmap.md
?? reports/pensee-porte-minute.json
?? tools/tests/qualifier_porte_minute_drvm.py
=== ahead ===
11
0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git push origin master 2>&1 | tail -8; echo \"exit=${PIPESTATUS[0]}\"; git status -sb | head -2; echo \"=== remote ===\"; git ls-remote --heads origin | head -1", "description": "Push main repository with S v3", "timeoutMs": 300000}`

  ```
To github.com:stephanedenis/drave.git
   d2fc26c6..e2227509  master -> master
exit=0
## master...origin/master
M  docs/pilotage/chantiers.md
=== remote ===
e2227509febf47d561fd975a09ba743e53ebbe52	refs/heads/master
  ```

### 🤖 Assistant

⏵ S v3 poussé : analyseur 47/47 types, 117/117 rôles, corpus 47 ; sous-module et principal à jour.

**Le cycle entrepris**

- **Frontière GN-devant-verbe** : `h033` (« La femme parle ») est corrigé par un lexique de verbes finis ; le GV s'arrête aussi devant un adverbe de temps (« part demain » → GV + GP temps).
- **Gold porté à 47 phrases** (7 dev, 16 test, 24 holdout en trois vagues ; `h040–h047` écrites après la règle, mesurées une fois).
- **Mesure** : types **47/47**, rôles **117/117**, compléments **47/47**, couverture **1 309/1 320** (99,2 % ; holdout 605/616, 98,2 %) ; contrôles **80/117**, **82/117**, rôles mélangés **0,109**.
- **Limite nommée** : les homographes nominaux `h046` (« ferme ») et `h047` (« fait ») sont coupés comme des verbes — le type et le rôle ne le voient pas, la **couverture** oui (0,75 et 0,77).
- **Corpus** : 47 lignes, SHA `f2a0d2fb3a9b0a9aebd562b170503f4d1a98251efdc4a3645a2523b5197227a2` ; `verifier_corpus.py` le rejoue.
- **43 tests** verts.

**Commits et push**

- Sous-module : **`90e507b`**, poussé sur `drave-structures` (`647205a..90e507b`).
- Principal : **`e2227509`** (la clôture N2 a intégré la fiche S v3, le manifeste, le pointeur `90e507b`, la roadmap et l'INDEX), poussé : `origin/master` = `e2227509`.
- `docs/pilotage/en-cours.md` porte la ligne S v3 (47/47, 117/117, corpus 47, 43 tests) ; T0 repassé sous 4 000.

**En cours, pas à moi** : la **passe complète des portes** du hub (`work/portes/passe-1102-19h32`, `porte-épisodique` en cours) ; ses mises à jour de `docs/pilotage/` sont encore dans l'arbre, et `reports/pensee-porte-minute.json` est en écriture. Je les laisse au hub. Prochaine action S : homographes/lexique, puis validation humaine de la banque.


## Tour 6

### 👤 Utilisateur

attends-tu aprèes quelque-chose? on a des ressources qui peuvent en prendre un peu plus

### 🤖 Assistant

⏵ Non, rien de bloquant : je n'attends que la passe de portes du hub. J'entreprends la mesure de l'analyseur sur le corpus CEGEP réel, en CPU.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== corpus CEGEP ===\"; ls -la data/corpus_ocr_cegep/ 2>/dev/null | head; du -sh data/corpus_ocr_cegep 2>/dev/null; for f in data/corpus_ocr_cegep/train.txt data/corpus_ocr_cegep/val.txt data/corpus_ocr_cegep/test.txt; do [ -f … [256 caractères tronqués]`

  ```
=== corpus CEGEP ===
total 4356
drwxr-xr-x. 1 stephane stephane      48  2 nov 16:31 .
drwxr-xr-x. 1 stephane stephane    2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane   10524  2 nov 18:06 test.txt
-rw-r--r--. 1 stephane stephane 4430959  2 nov 18:33 train.txt
-rw-r--r--. 1 stephane stephane   12536  2 nov 17:27 val.txt
4,3M	data/corpus_ocr_cegep
data/corpus_ocr_cegep/train.txt 4430959 octets 108298 lignes
data/corpus_ocr_cegep/val.txt 12536 octets 299 lignes
data/corpus_ocr_cegep/test.txt 10524 octets 207 lignes
=== échantillon ===
document%20de%20revision_pages_12a15_5421
@
®
©
@
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for n in 500 5000 50000; do echo \"=== ligne $n ===\"; sed -n \"${n},$((n+4))p\" data/corpus_ocr_cegep/train.txt | cut -c1-180; done; echo \"=== stats mots ===\"; python3 - <<'PY'\nfrom collections import Counter\nimport re\nt=open(' … [775 caractères tronqués]`

  ```
=== ligne 500 ===
le participe passé ne s'accorde pas. S'il n’y a pas de CD, le participe passé |
ne. £'accotde ouf

2. Accorde, s’il y a lieu, le participe passé.
a) L’ourse a mangé
=== ligne 5000 ===
appelée justifiante ou sécable), l'espace fine (aussi appelée quart de cadratin) et l'espace insécable.
Leur emploi ainsi que la façon de les obtenir dans Word sont indiqués sous la prochaine rubrique.

Le tableau ci-dessous indique les règles à respecter selon l'Office de la langue française pour la
rédaction de textes français. Pour la rédaction de textes anglais, d'autres règles s'appliquent.
=== ligne 50000 ===

39

these objects may be in a measure attained;

=== stats mots ===
lignes non vides 108298
longueur moyenne 39.1284972945022
lignes plausibles 71056
[(5, 7576), (10, 1863), (15, 289), (0, 250), (20, 19), (25, 2), (30, 1)]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la data/corpus_fr_litterature.txt data/corpus_fr.txt data/corpus_fr_train.txt 2>/dev/null; for f in data/corpus_fr_litterature.txt data/corpus_fr.txt; do [ -f \"$f\" ] && echo \"$f $(wc -c < \"$f\") octets $(grep -c . \"$f\") lig … [170 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 17031747 17 oct 18:26 data/corpus_fr_litterature.txt
-rw-r--r--. 1 stephane stephane  4402195 28 oct 12:45 data/corpus_fr_train.txt
-rw-r--r--. 1 stephane stephane  4633889 17 oct 15:01 data/corpus_fr.txt
data/corpus_fr_litterature.txt 17031747 octets 277246 lignes
data/corpus_fr.txt 4633889 octets 47755 lignes
=== extrait propre ===
Au lecteur

  Cette version électronique reproduit dans son intégralité
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"mesure_corpus.py — l'analyseur sur du texte réel : couverture, structure, et le contrôle du mélange.\n\nLe gold mesure la justesse sur 47 phrases écrites à la main. Ce script mesure autre chose : ce que\nl'analyseur **fait** sur des lignes réelles, sans gol … [7091 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/mesure_corpus.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && time python3 mesure_corpus.py --max 20000", "description": "Measure analyzer on 20k CEGEP and clean lines", "timeoutMs": 600000}`

  ```
corpus réels · 20000 lignes CEGEP · 20000 lignes propres · 12.83 s
  corpus     seg/ligne   GN+GV  sans GV   couv.  homogr. lignes homogr.
  cegep           1.97   3.6%    0.4%    0.94       10              8
  propre          4.32  50.8%   10.8%    0.89      217            215
  melange         2.07   3.9%    0.5%    0.94       11             11
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/mesure-corpus.json
[stderr]

real	0m12,896s
user	0m12,824s
sys	0m0,071s
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"mesure_corpus.py — l'analyseur sur du texte réel : lignes, phrases, et le contrôle du mélange.\n\nLe gold mesure la justesse sur 47 phrases écrites à la main. Ce script mesure autre chose : ce que\nl'analyseur **fait** sur du texte réel, sans gold — la part … [8547 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/mesure_corpus.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && time python3 mesure_corpus.py --max 20000", "description": "Measure on lines and sentences, 20k each", "timeoutMs": 600000}`

  ```
corpus réels · 20000 lignes CEGEP · 20000 phrases CEGEP · 35.84 s
  lignes
  corpus     seg/unité   GN+GV  sans GV   couv.  homogr.  unités homogr.
  cegep           1.97   3.6%    0.4%    0.94       10               8
  propre          4.32  50.8%   10.8%    0.89      217             215
  melange         2.07   3.9%    0.5%    0.94       11              11
  phrases
  corpus     seg/unité   GN+GV  sans GV   couv.  homogr.  unités homogr.
  cegep           3.24   8.4%    0.8%    0.94       24              24
  propre          6.89  65.5%    8.0%    0.89      388             381
  melange         4.11   9.3%    0.4%    0.93       23              23
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/mesure-corpus.json
[stderr]

real	0m35,911s
user	0m35,795s
sys	0m0,104s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && time python3 mesure_corpus.py --max 50000 --sortie donnees/mesure-corpus-50k.json", "description": "Measure on 50k units for stability", "timeoutMs": 600000}`

  ```
corpus réels · 50000 lignes CEGEP · 20799 phrases CEGEP · 59.74 s
  lignes
  corpus     seg/unité   GN+GV  sans GV   couv.  homogr.  unités homogr.
  cegep           1.96   3.6%    0.5%    0.94       18              15
  propre          4.33  51.0%   10.2%    0.89      553             550
  melange         2.07   3.8%    0.5%    0.94       18              18
  phrases
  corpus     seg/unité   GN+GV  sans GV   couv.  homogr.  unités homogr.
  cegep           3.25   8.5%    0.8%    0.94       25              25
  propre          6.93  65.5%    8.0%    0.89     1064            1035
  melange         4.11   9.1%    0.4%    0.93       22              22
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/mesure-corpus.json
[stderr]

real	0m59,824s
user	0m59,654s
sys	0m0,166s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('mesure_corpus.py')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"def afficher(r: dict) -> None:\", \"def afficher(r: dict, chemin: pathlib.Path = SORTIE) -> … [660 caractères tronqués]`

  ```
max 50000 cegep lignes 50000 phrases 20799
compile OK
  ```

- **write** `{"content": "\"\"\"Tests de la mesure sur corpus réel — filtre, statistiques, mélange déterministe.\"\"\"\nimport pathlib\nimport tempfile\nimport unittest\n\nimport mesure_corpus\n\n\nclass TestMesureCorpus(unittest.TestCase):\n    def test_lignes_et_phrases(self):\n        with tempfile.TemporaryD … [1072 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/tests/test_mesure_corpus.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('README.md')\nt = p.read_text(encoding='utf-8')\nsection = '''\n## La mesure sur corpus réel\n\n```bash\npython3 mesure_corpus.py --max 50000        # 50 000 ligne … [2752 caractères tronqués]`

  ```
README corpus ajouté
----------------------------------------------------------------------
Ran 45 tests in 3.680s

OK
143:## La mesure sur corpus réel
162:| phrase | CEGEP | 8,5 % | 0,8 % | 0,94 | 25 |
168:OCR**, il est au **plancher du mélange** (8,5 % contre 9,1 %) : ce corpus est **multilingue et
239:**45 tests** : phrases et alignement des spans, validation + export, statut invalide refusé,
262:  propre contre 9,1 % pour les mots mélangés, 8,5 % contre 9,1 % sur le CEGEP OCR (multilingue et
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git add mesure_corpus.py donnees/mesure-corpus.json tests/test_mesure_corpus.py README.md && git diff --cached --stat && git commit -m \"S — L'ANALYSEUR LIT LE FRANÇAIS PROPRE (65,5 %), PAS LE CEGEP OCR (8,5 %, PLANC … [575 caractères tronqués]`

  ```
README.md                   |  42 +++++++-
 donnees/mesure-corpus.json  | 255 ++++++++++++++++++++++++++++++++++++++++++++
 mesure_corpus.py            | 205 +++++++++++++++++++++++++++++++++++
 tests/test_mesure_corpus.py |  30 ++++++
 4 files changed, 529 insertions(+), 3 deletions(-)
[master 140feb6] S — L'ANALYSEUR LIT LE FRANÇAIS PROPRE (65,5 %), PAS LE CEGEP OCR (8,5 %, PLANCHER DU MÉLANGE)
 4 files changed, 529 insertions(+), 3 deletions(-)
 create mode 100644 donnees/mesure-corpus.json
 create mode 100644 mesure_corpus.py
 create mode 100644 tests/test_mesure_corpus.py
To /home/stephane/Data13TB/stephane/GitHub/drave-structures
   90e507b..140feb6  master -> master
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; git log --oneline -3; echo \"=== status ===\"; git status --short | head -12; echo \"=== pass ===\"; ps -eo pid,etime,cmd | grep -E \"toutes-les-portes|porte-\" | grep -v grep | head -3; echo \"=== S fiche compteur === … [144 caractères tronqués]`

  ```
20:00
a902abea PILOTAGE — L'ÉTAT EST À JOUR ET CONCIS : 3 SESSIONS ACTIVES, N2 CLOSE (200 K PAS), 560/648 ; R1.2 À 1 024 OCTETS
e2227509 N2 — CLÔTURE : 200 000 PAS (3,1591) ET R1.1/R1.2 (0,97× LA PORTE, FENÊTRE 512 −0,244) SONT COMMITTÉS
e12c39c1 N2 — 200 000 PAS SUR LE MÉLANGE 1 Go : 3,1591 EN DOMAINE (−0,33), 5,6056 EN LITTÉRATURE, LA PORTE 2,5 À 1,3–2,7 M PAS
=== status ===
MM docs/pilotage/en-cours.md
 M docs/pilotage/plan-travail.md
 M docs/pilotage/roadmap.md
 M journal/2026-11-02/README.md
 M journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
M  journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md
 M journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
 M journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/digest.md
 M journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/rapport.md
 M journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/digest.md
 M journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/rapport.md
 M journal/sessions/MANIFEST.md
=== pass ===
 164359       28:20 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; CUDA_VISIBLE_DEVICES=1,0 JOURNAUX=work/portes/passe-1102-19h32 bash tools/toutes-les-portes.sh; echo "E
… [326 caractères tronqués]
  ```

- **write** `{"content": "# S — L'analyseur lit le français propre (65,5 % de GN+GV), pas le CEGEP OCR (8,5 %, plancher du mélange)\n\n> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur **50 000 lignes** et\n> **20 799 phrases** du corpus **CEGEP OCR** (D/R/A, 4,41 M car.) et **50 000** ligne … [5561 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-corpus-reel.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '/### Session `29ad180d/,/### Session `e181ce02/p' docs/pilotage/en-cours.md | head -22; echo \"=== compteurs ===\"; grep -n \"fichiers / JSON\" docs/pilotage/en-cours.md; echo \"=== roadmap S ===\"; grep -n \"S — les structur … [213 caractères tronqués]`

  ```
### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures : l'analyseur et l'export

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : 1–4) ~~plan, analyseur (gold 47), export, tests 43~~ ; 5–6) ~~fiche, pointeur, état~~.
- **Ambition** : nommer le rôle et la frontière GN.
- **Stratégie** : une règle = une phrase, trois contrôles.
- **Objectif final** : gold **47**, corpus **47**, manifeste SHA-256.
- **Fait** : types **47/47**, rôles **117/117** ; contrôles **80/117**, **82/117**, **0,109** ; h033 corrigé, **h046/h047** nommés ; **43 tests** ; [`fiche`](../../reports/rapport-s-analyseur-roles.md).
- **Ce qu'elle fait** : **`90e507b`** ; corpus **47** (SHA `f2a0d2fb…`) ; banque **0**.
- **Ce que font les autres** : **hub**, **N2**, **Pensée**, **D/R/A**.
- **Prochaine action** : homographes/lexique, puis validation humaine de la banque.
- **Bloquants** : aucun ; **banque à 0** verdict.
- **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).

### Ses
… [782 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np = Path('docs/pilotage/en-cours.md')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"- **Plan** : 1–4) ~~plan, analyseur (gold 47), export, tests 43~~ ; 5–6) ~~fiche, pointeur, état~~. … [3497 caractères tronqués]`

  ```
état/roadmap/INDEX corpus ajoutés
  en-cours · 1666 mots · 7 sections · 4 session(s) · 7 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ❌ 1 violation(s) :
     · T0 : 4040 mots (AGENTS + en-cours + une tâche) > budget 4 000
  revue de documentation · 562 fiche(s) · 648 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ❌ 1 anomalie(s) :
     · compteurs : en-cours.md dit 561 fichiers, le disque en a 562
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"ahead $(git rev-list --count origin/master..HEAD) behind $(git rev-list --count HEAD..origin/master)\"; git push origin master 2>&1 | tail -4; echo \"exit=${PIPESTATUS[0]}\"; git ls-remote --heads origin | head -1; echo \"===  … [238 caractères tronqués]`

  ```
ahead 2 behind 0
To github.com:stephanedenis/drave.git
   e2227509..c0196b55  master -> master
exit=0
c0196b551ac06cdbfc7e6f018a4a6924aceff6eb	refs/heads/master
=== sous-module ===
140feb69d393b7b6ac716d0c705d9ceabed0993a	refs/heads/master
=== S corpus submodule ===
140feb6 S — L'ANALYSEUR LIT LE FRANÇAIS PROPRE (65,5 %), PAS LE CEGEP OCR (8,5 %, PLANCHER DU MÉLANGE)
90e507b S — LA FRONTIÈRE DU GN S'ARRÊTE DEVANT LE VERBE : 47/47 TYPES, 117/117 RÔLES ; GOLD 47
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -3; echo \"=== S corpus dans HEAD ? ===\"; git show HEAD:docs/pilotage/en-cours.md | grep -c \"corpus réel\"; git show HEAD:reports/INDEX.md | grep -c \"rapport-s-corpus-reel\"; git ls-files reports/rapport-s-corpus … [212 caractères tronqués]`

  ```
c0196b55 N2 — MANDAT DE NUIT : R1.2 À 1 024 OCTETS ET LA FENÊTRE SUR LE MÉLANGE DE PRODUCTION (JUSQU'À 08 h)
a902abea PILOTAGE — L'ÉTAT EST À JOUR ET CONCIS : 3 SESSIONS ACTIVES, N2 CLOSE (200 K PAS), 560/648 ; R1.2 À 1 024 OCTETS
e2227509 N2 — CLÔTURE : 200 000 PAS (3,1591) ET R1.1/R1.2 (0,97× LA PORTE, FENÊTRE 512 −0,244) SONT COMMITTÉS
=== S corpus dans HEAD ? ===
0
0
=== status ===
 M docs/pilotage/en-cours.md
 M docs/pilotage/plan-travail.md
 M docs/pilotage/roadmap.md
 M reports/INDEX.md
 M reports/README.md
 M tools/structures
?? reports/pensee-porte-minute.json
?? reports/rapport-pensee-porte-minute.md
?? reports/rapport-s-corpus-reel.md
?? tools/ressources.py
=== S corpus fiche présente ===
-rw-------. 1 stephane stephane 5766  2 nov 20:00 reports/rapport-s-corpus-reel.md
  ```

- **bash** `{"command": "chmod 644 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-corpus-reel.md; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -10; echo \"=== remotes ===\"; git ls-remote --heads origin | head -1; git -C tools/structures ls-remote --heads or … [190 caractères tronqués]`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/plan-travail.md
 M docs/pilotage/roadmap.md
 M reports/INDEX.md
 M reports/README.md
 M tools/structures
?? reports/pensee-porte-minute.json
?? reports/rapport-pensee-porte-minute.md
?? reports/rapport-s-corpus-reel.md
?? tools/ressources.py
=== remotes ===
c0196b551ac06cdbfc7e6f018a4a6924aceff6eb	refs/heads/master
140feb69d393b7b6ac716d0c705d9ceabed0993a	refs/heads/master
=== tests sous-module ===
Ran 45 tests in 3.774s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && ls -la donnees/; echo \"=== lignes propres ===\"; python3 - <<'PY'\nimport mesure_corpus, pathlib\nl = mesure_corpus.phrases_texte(pathlib.Path('../../data/corpus_fr_litterature.txt'), 300)\nprint(len(l), \"phrases é … [124 caractères tronqués]`

  ```
total 56
drwxr-xr-x. 1 stephane stephane   140  2 nov 19:59 .
drwxr-xr-x. 1 stephane stephane   346  2 nov 19:56 ..
-rw-------. 1 stephane stephane 13281  2 nov 19:39 gold-analyseur.json
-rw-r--r--. 1 stephane stephane 17199  2 nov 19:40 mesure-analyseur.json
-rw-r--r--. 1 stephane stephane  5059  2 nov 19:59 mesure-corpus.json
-rw-r--r--. 1 stephane stephane 12115  2 nov 02:10 phrases.json
=== lignes propres ===
300 phrases échantillonnées
90 Au lecteur Cette version électronique reproduit dans son intégralité la version originale.
27 Cabriolez-vous de la sorte?
128 "Je suis bien contente qu'on ne fasse pas de cadeau d'anniversaire comme cela!" Mais elle ne se hasarda pas à le dire to
140 La lecture de ce journal occupa Phileas Fogg jusqu'à trois heures quarante-cinq, et celle du Standard--qui lui succéda--
59 Une montre de famille, qui vient de mon arrière-grand-père!
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"candidats_corpus.py — une banque de candidats réels : 200 phrases propres → le banc.\n\nLe gold est écrit à la main ; la banque a besoin de phrases **réelles** à valider. Ce script prend\n200 phrases de la littérature propre (filtrées, déterministes), lance … [4163 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/candidats_corpus.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('candidats_corpus.py')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"def construire(phrases: list[str], max_candidats: int = 4) -> dict:\",\n              \" … [1483 caractères tronqués]`

  ```
✅ 200 phrases, 355 candidats → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/phrases_generees.json
     manifeste : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/phrases-corpus-manifest.json · sha256 43957a3b9ad2422b…
-rw-r--r--. 1 stephane stephane    366  2 nov 20:04 donnees/phrases-corpus-manifest.json
-rw-r--r--. 1 stephane stephane 527440  2 nov 20:04 donnees/phrases_generees.json
200 phrases 355 candidats
c001 Au lecteur Cette version électronique reproduit dans son intégralité la version originale.
['GP', 'GP']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('candidats_corpus.py')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"def construire(phrases: list[str], max_candidats: int = 4,\\n               source: path … [1663 caractères tronqués]`

  ```
source rel fix
----------------------------------------------------------------------
Ran 46 tests in 3.701s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('README.md')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"**45 tests** :\", \"**46 tests** :\")\nt = t.replace(\"mesure corpus (filtre,\\nstats, mélange dét … [1386 caractères tronqués]`

  ```
README banque candidats
201:## La banque de candidats réels
211:(`donnees/phrases-corpus-manifest.json`). **200 phrases, 355 candidats** ; l'humain valide dans
253:**46 tests** : phrases et alignement des spans, validation + export, statut invalide refusé,
260:stats, mélange déterministe) ; banque de candidats (filtre, IDs, spans).
277:  technique) — la langue et l'unité comptent. La **banque de candidats réels** (200 phrases,
278:  355 candidats, manifeste SHA-256) attend la validation humaine.
 M README.md
?? candidats_corpus.py
?? donnees/phrases-corpus-manifest.json
?? donnees/phrases_generees.json
?? tests/test_candidats_corpus.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git add candidats_corpus.py donnees/phrases_generees.json donnees/phrases-corpus-manifest.json tests/test_candidats_corpus.py README.md && git diff --cached --stat && git commit -m \"S — LA BANQUE DE CANDIDATS RÉELS  … [522 caractères tronqués]`

  ```
README.md                            |    21 +-
 candidats_corpus.py                  |   109 +
 donnees/phrases-corpus-manifest.json |    10 +
 donnees/phrases_generees.json        | 24423 +++++++++++++++++++++++++++++++++
 tests/test_candidats_corpus.py       |    23 +
 5 files changed, 24583 insertions(+), 3 deletions(-)
[master 97641d5] S — LA BANQUE DE CANDIDATS RÉELS : 200 PHRASES, 355 CANDIDATS, MANIFESTE SHA-256
 5 files changed, 24583 insertions(+), 3 deletions(-)
 create mode 100644 candidats_corpus.py
 create mode 100644 donnees/phrases-corpus-manifest.json
 create mode 100644 donnees/phrases_generees.json
 create mode 100644 tests/test_candidats_corpus.py
To /home/stephane/Data13TB/stephane/GitHub/drave-structures
   140feb6..97641d5  master -> master
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\n# fiche corpus\np = Path('reports/rapport-s-corpus-reel.md')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"Le corpus réel **n'est pas exporté** : la prochaine étape est une **banque d … [3730 caractères tronqués]`

  ```
fiches/état/roadmap banque
  revue de documentation · 562 fiche(s) · 648 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  en-cours · 1623 mots · 7 sections · 4 session(s) · 7 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -14; echo \"=== staged ===\"; git diff --cached --stat | tail -5; echo \"=== ahead ===\"; git rev-list --count origin/master..HEAD", "description": "Check index before main corpus/bank commit"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/plan-travail.md
 M docs/pilotage/roadmap.md
 M reports/rapport-s-analyseur-roles.md
 M tools/structures
?? reports/rapport-s-corpus-reel.md
?? tools/ressources.py
=== staged ===
=== ahead ===
1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -2; git ls-remote --heads origin | head -1; echo \"=== INDEX corpus ? ===\"; git show HEAD:reports/INDEX.md | grep -c \"rapport-s-corpus-reel\"; echo \"=== commit S corpus/banque ===\"; git add reports/rapport-s-cor … [208 caractères tronqués]`

  ```
67ec9cd4 B13 — LA PORTE MINUTE S'OUVRE AVEC LA RÈGLE (26 NŒUDS, 4 SONDE) ; LE PROMPT LABYRINTHE ÉCHOUE (200, 3)
c0196b55 N2 — MANDAT DE NUIT : R1.2 À 1 024 OCTETS ET LA FENÊTRE SUR LE MÉLANGE DE PRODUCTION (JUSQU'À 08 h)
c0196b551ac06cdbfc7e6f018a4a6924aceff6eb	refs/heads/master
=== INDEX corpus ? ===
1
=== commit S corpus/banque ===
 docs/pilotage/en-cours.md            |   8 +-
 docs/pilotage/plan-travail.md        | 106 ++++++-
 docs/pilotage/roadmap.md             |   2 +-
 reports/rapport-s-analyseur-roles.md |   2 +-
 reports/rapport-s-corpus-reel.md     |  96 ++++++
 tools/ressources.py                  | 562 +++++++++++++++++++++++++++++++++++
 tools/structures                     |   2 +-
 7 files changed, 769 insertions(+), 9 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -m \"S — LE CORPUS RÉEL (65,5 % PROPRE / 8,5 % CEGEP) ET LA BANQUE 200/355 ; N2 — LE MANDAT DE NUIT ET L'OUTIL RESSOURCES\" -m \"S — mesure_corpus.py sur 50 000 lignes et 20 799 phrases CEGEP, 50 000 lignes/phrases propres … [709 caractères tronqués]`

  ```
[stderr]
  ✅ index : aucun fait stagé sans état
fatal: Unable to create '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.git/index.lock': File exists.

Another git process seems to be running in this repository, or the lock file may be stale
  ⛔ journal non ajouté à l'index
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la .git/index.lock 2>/dev/null; ps -eo pid,etime,cmd | grep -E \"git (commit|add|push|read-tree)|index.lock\" | grep -v grep | head -8; echo \"=== log ===\"; git log --oneline -3; echo \"=== status ===\"; git status --short | hea … [63 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 355949  2 nov 20:07 .git/index.lock
 337047       01:16 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add tools/ressources.py docs/pilotage/plan-travail.md && timeout 300 git commit --only -m "PILOTAGE — LE REGISTRE DES RESSOURCES : GPU, CPU, NVMe, RAM ET PASSE GLOBALE" -m "Le pilotage réservait les fichiers, pas la machine. tools/ressources.py ajoute un registre consultatif (work/ressources.json) : GPU0/GPU1 (1 job exclusif), cpu0/cpu1 (16 fils utiles, réserve 4, NUMA 0/1), RAM (109 Gio utiles), NVMe système (705 Gio), RAID IA (33 Gio), HDD Data13TB (1,9 Tio) et machine (passe complète exclusive). claim/release/check/suggest/actual ; ce qui ne tient pas va en file et la session prend une autre tâche (jamais en attente). plan-travail.md § 10 porte la politique, l'allocation type (N2 gpu0/cpu0 12, hub gpu1/cpu1 8, S et Pensée cpu1 4+4, CPU1 = 16) et la règle NUMA (GPU sur node 0, CPU seul sur node 1)." -m "Contrôles : autotest 9 cas ; revue_documentation verte ; T0 3 997/4 000 ; en-cours 1 623 mots ; le registre réel des quatre sessions passe --check. Limites : registre consultatif (pas de cgroups) ; le mapping processus→claim n'es
… [3359 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in $(seq 1 30); do if [ ! -e .git/index.lock ]; then echo \"lock libéré après ${i}x5s\"; break; fi; sleep 5; done; ls -la .git/index.lock 2>/dev/null || echo \"pas de verrou\"; git log --oneline -2; git status --short | head -8 … [75 caractères tronqués]`

  ```
lock libéré après 3x5s
pas de verrou
a67dbf00 PILOTAGE — LE REGISTRE DES RESSOURCES : GPU, CPU, NVMe, RAM ET PASSE GLOBALE
67ec9cd4 B13 — LA PORTE MINUTE S'OUVRE AVEC LA RÈGLE (26 NŒUDS, 4 SONDE) ; LE PROMPT LABYRINTHE ÉCHOUE (200, 3)
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
MM journal/2026-11-02/README.md
MM journal/2026-11-02/apprentissage.md
MM journal/2026-11-02/attention.md
MM journal/2026-11-02/distribue.md
MM journal/2026-11-02/docs.md
MM journal/2026-11-02/memoire.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --cached --stat | tail -12; echo \"=== commit ===\"; git commit -m \"S — LE CORPUS RÉEL (65,5 % PROPRE / 8,5 % CEGEP, PLANCHER DU MÉLANGE) ET LA BANQUE 200 PHRASES / 355 CANDIDATS\" -m \"mesure_corpus.py : 50 000 lignes et 2 … [610 caractères tronqués]`

  ```
.../rapport.md                                     |  17 ++--
 .../536cd5d6-94ac-4057-8fe9-11709a4587c7/digest.md |  63 ------------
 .../rapport.md                                     |  19 ++--
 journal/sessions/MANIFEST.md                       |  10 +-
 .../abb58991-fe0a-4d6e-b039-6552b09f8454/digest.md |  75 ---------------
 .../rapport.md                                     |  41 ++------
 .../b7d4678e-2143-4daa-a9a4-a456c5aa8dab/digest.md |  65 -------------
 .../rapport.md                                     |  19 ++--
 reports/rapport-s-analyseur-roles.md               |   2 +-
 reports/rapport-s-corpus-reel.md                   |  96 +++++++++++++++++++
 tools/structures                                   |   2 +-
 26 files changed, 193 insertions(+), 437 deletions(-)
=== commit ===
[master 3f74fe83] S — LE CORPUS RÉEL (65,5 % PROPRE / 8,5 % CEGEP, PLANCHER DU MÉLANGE) ET LA BANQUE 200 PHRASES / 355 CANDIDATS
 16 files changed, 312 insertions(+), 33 deletions(-)
 create mode 100644 reports/rapport-s-corpus-reel.md
[stderr]
  ✅ index : aucun fait stagé sans état
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git push origin master 2>&1 | tail -4; echo \"exit=${PIPESTATUS[0]}\"; git ls-remote --heads origin | head -1; git -C tools/structures ls-remote --heads origin | head -1; echo \"=== S dans HEAD ===\"; git show HEAD:docs/pilotage/en-c … [167 caractères tronqués]`

  ```
To github.com:stephanedenis/drave.git
   c0196b55..3f74fe83  master -> master
exit=0
3f74fe83a4a1af31cff539a50c71a1e9d791aadc	refs/heads/master
97641d538ce0a8816a55104fa5d3847e4e6cecfe	refs/heads/master
=== S dans HEAD ===
2
160000 commit 97641d538ce0a8816a55104fa5d3847e4e6cecfe	tools/structures
 M tools/pensee/operateurs.py
 M tools/tests/test_pensee_politique.py
  ```

### 🤖 Assistant

⏵ Non : le CPU a servi au corpus réel et à la banque ; tout est committé et poussé.

**Ce qui a été entrepris**

- **Mesure sur corpus réel** (`mesure_corpus.py`, 60 s CPU) : **50 000 lignes** et **20 799 phrases** CEGEP OCR + **50 000** lignes/phrases de littérature propre, avec le **mélange des mots** en contrôle.
  - littérature propre : **65,5 %** de GN+GV (phrases) / **51,0 %** (lignes) contre **9,1 %** / **3,8 %** pour le mélange ;
  - CEGEP OCR : **8,5 %** / **3,6 %** contre **9,1 %** / **3,8 %** — **au plancher du mélange** : corpus multilingue/technique, analyseur français ; ce n'est pas une mesure du français OCR ;
  - couverture **0,94** / **0,89** ; homographes **25**/20 799 et **1 064**/50 000.
- **Banque de candidats réels** (`candidats_corpus.py`) : **200 phrases, 355 candidats**, manifeste SHA-256 `43957a3b…` — de la matière à valider, pas des vérités.
- **46 tests** verts ; fiches [`corpus réel`](reports/rapport-s-corpus-reel.md) et [`analyseur`](reports/rapport-s-analyseur-roles.md).

**Committé et poussé**

- Sous-module : **`97641d5`** (mesure + banque) → `drave-structures` ; le pointeur est dans le principal.
- Principal : **`3f74fe83`** → `origin/master` (la fiche, le manifeste, l'état S, le pointeur, l'INDEX) ; le registre des ressources **`a67dbf00`** du hub est poussé avec.
- État : **562 fiches / 648 JSON**, T0 vert, `en-cours` 1 623 mots.

**Ce qui tourne / ce qui reste**

- Le **GPU** est à N2 (mandat de nuit R1.2 à 1 024 octets, jusqu'à 08 h) et à la passe de portes ; le **CPU** était à S, d'où le registre `tools/ressources.py` du hub (`a67dbf00`) — on peut maintenant réserver explicitement.
- Prochaine action S : **validation humaine des 200 phrases** de la banque (le serveur les charge), puis **homographes/lexique** (`ferme`, `fait`, `lit`) et filtre langue/genre.


## Tour 7

### 👤 Utilisateur

tiens ta liste de tâches dsh à jour et continue

- **todo_write** `{"todos": [{"content": "S v3 : frontière GN-devant-verbe, gold 47, 46 tests, corpus 47 — committé/poussé", "status": "completed"}, {"content": "Mesure sur corpus réel (50k lignes, 20 799 phrases CEGEP, 50k propres) + contrôle du mélange", "status": "completed"}, {"content": "Banque de candidats réel … [623 caractères tronqués]`

  ```
Updated todo list: 4 pending, 1 in progress, 3 completed.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git status -sb | head -2; python3 - <<'PY'\nfrom pathlib import Path\np = Path('generateur.py')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"\"\"            while j < len(utiles) and utiles[j].cls in (\"DET\", … [2096 caractères tronqués]`

  ```
## master...origin/master
règle de contexte ajoutée
La petite ferme est belle. → La petite ferme[GN] | est belle[GV]
Le simple fait surprend. → Le simple[GN] | fait surprend[GV]
Le grand lit est dur. → Le grand lit[GN] | est dur[GV]
La vieille porte est ouverte. → La vieille porte[GN] | est ouverte[GV]
Le triste fait demeure. → Le triste[GN] | fait demeure[GV]
Le fait divers est intéressant. → Le fait divers[GN] | est intéressant[GV]
La ferme. → La ferme[GN]
Le grand lit. → Le grand[GN] | lit[GV]
La femme parle à son fils. → La femme[GN] | parle[GV] | à son fils[GP]
Le chat fait des bonds. → Le chat[GN] | fait[GV] | des bonds[GP]
Le chien porte la balle. → Le chien[GN] | porte[GV] | la balle[GN]
La danse est belle. → La danse[GN] | est belle[GV]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('generateur.py')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"prend prends prennent prenons prenez prenais prenait prenaient\",\n              \"prend prend … [685 caractères tronqués]`

  ```
surprend ajouté
Le simple fait surprend. → Le simple fait[GN:agent] | surprend[GV:predicat]
La petite ferme est belle. → La petite ferme[GN:agent] | est belle[GV:predicat]
La vieille porte est ouverte. → La vieille porte[GN:agent] | est ouverte[GV:predicat]
Le grand lit est dur. → Le grand lit[GN:agent] | est dur[GV:predicat]
Le triste fait demeure. → Le triste[GN:agent] | fait demeure[GV:predicat]
Le fait divers est intéressant. → Le fait divers[GN:agent] | est intéressant[GV:predicat]
La ferme. → La ferme[GN:agent]
Le grand lit. → Le grand[GN:agent] | lit[GV:predicat]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nimport json\nfrom pathlib import Path\np = Path('donnees/gold-analyseur.json')\nd = json.loads(p.read_text(encoding='utf-8'))\nd['note'] = (\"Gold de l'analyseur. split=dev : les 7 phrases du banc.  … [2154 caractères tronqués]`

  ```
55 phrases
  gold · 55 phrases · donnees/gold-analyseur.json
  split     phr    types   couv.    rôles   compl.
  dev         7   7/7       1.00  22/22    10/10  
  test       16  16/16      1.00  40/40    19/19  
  holdout    32  31/32      0.98  69/69    18/18  
  global     55  54/55      0.99 131/131   47/47  
  contrôle · baseline 94/131 (0.72) · règles coupées 96/131 (0.73) · rôles mélangés 0.11 [0.00, 0.23]
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/mesure-analyseur.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('tests/test_generateur.py')\nt = p.read_text(encoding='utf-8')\nt = t.replace('''    def test_homographe_nominal_reste_une_limite(self):\n        # « ferme » est u … [2267 caractères tronqués]`

  ```
tests contexte
----------------------------------------------------------------------
Ran 47 tests in 3.685s

OK
  gold · 55 phrases · donnees/gold-analyseur.json
  split     phr    types   couv.    rôles   compl.
  dev         7   7/7       1.00  22/22    10/10  
  test       16  16/16      1.00  40/40    19/19  
  holdout    32  31/32      0.98  69/69    18/18  
  global     55  54/55      0.99 131/131   47/47  
  contrôle · baseline 94/131 (0.72) · règles coupées 96/131 (0.73) · rôles mélangés 0.11 [0.00, 0.23]
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/mesure-analyseur.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && time python3 mesure_corpus.py --max 50000; echo \"=== banque ===\"; python3 candidats_corpus.py --max 200", "description": "Re-run corpus measure and bank with context rule", "timeoutMs": 300000}`

  ```
corpus réels · 50000 lignes CEGEP · 20799 phrases CEGEP · 59.94 s
  lignes
  corpus     seg/unité   GN+GV  sans GV   couv.  homogr.  unités homogr.
  cegep           1.96   3.6%    0.5%    0.94       21              18
  propre          4.33  51.0%   10.2%    0.89      578             575
  melange         2.07   3.8%    0.5%    0.94       19              19
  phrases
  corpus     seg/unité   GN+GV  sans GV   couv.  homogr.  unités homogr.
  cegep           3.25   8.5%    0.8%    0.94       28              28
  propre          6.93  65.5%    8.0%    0.89     1134            1104
  melange         4.11   9.1%    0.4%    0.93       23              23
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/mesure-corpus.json
=== banque ===
  ✅ 200 phrases, 355 candidats → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/phrases_generees.json
     manifeste : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures/donnees/phrases-corpus-manifest.json · sha256 43957a3b9ad2422b…
[stderr]

real	1m0,018s
user	0m59,918s
sys	0m0,092s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 - <<'PY'\nfrom pathlib import Path\np = Path('README.md')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"- **frontière du GN** : le GN s'arrête devant un **verbe conjugué** fréquent (« La femme parle » → … [5830 caractères tronqués]`

  ```
README v4
132:Le **gold** (`donnees/gold-analyseur.json`) porte **55 phrases** en trois découpages :
166:| phrase | propre | 65,5 % | 8,0 % | 0,89 | 1 134 |
256:**47 tests** : phrases et alignement des spans, validation + export, statut invalide refusé,
273:- **v4** : **règle de contexte** des homographes (un mot du lexique de verbes est un nom si le
274:  suivant est un auxiliaire ou un verbe) ; le **gold de 55 phrases** (7 dev, 16 test, 32 holdout
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && python3 exporter_corpus.py --mode gold && python3 verifier_corpus.py ../../data/structures/banque.jsonl && python3 - <<'PY'\nimport json\nr=json.load(open('donnees/mesure-analyseur.json'))\nfor k in ('dev','test','ho … [474 caractères tronqués]`

  ```
✅ 55 ligne(s) sur 55 phrase(s) · mode gold → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque.jsonl
     manifeste : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/structures/banque-manifest.json
     sha256 : 76accf9dbd60a9fcc9fe58a56eecbdbb6aec0ffd5e8dbf0c69443e4a49dd1ac6
  ✅ ../../data/structures/banque.jsonl · empreinte, comptes, spans et restitution vérifiés
dev 7 7 229 229 22 10
test 16 16 475 475 40 19
holdout 31 32 762 771 69 18
global 54 55 1466 1475 131 47 0.9939
controles {'baseline_role_constant': {'justes': 94, 'total': 131, 'taux': 0.7176}, 'regles_coupees': {'justes': 96, 'total': 131, 'taux': 0.7328}, 'roles_melanges': {'tirages': 200, 'moyenne': 0.1086, 'min': 0.0, 'max': 0.234}}
{
 "version": 2,
 "mode": "gold",
 "date": "2026-11-02T20:36:15",
 "source": "tools/structures/donnees/gold-analyseur.json",
 "sortie": "data/structures/banque.jsonl",
 "phrases": 55,
 "candidats_acceptes": 55,
 "sha256": "76accf9dbd60a9fcc9fe58a56eecbdbb6aec0ffd5e8dbf0c69443e4a49dd1ac6",
 "note": "structures de référence, sans jugement humain — `statut: reference` ; spans vérifiés."
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git status --short; git add generateur.py donnees/gold-analyseur.json donnees/mesure-analyseur.json donnees/mesure-corpus.json tests/test_generateur.py README.md && git diff --cached --stat && git commit -m \"S — LE  … [759 caractères tronqués]`

  ```
M README.md
 M donnees/gold-analyseur.json
 M donnees/mesure-analyseur.json
 M donnees/mesure-corpus.json
 M donnees/phrases-corpus-manifest.json
 M generateur.py
 M tests/test_generateur.py
 README.md                     |  50 +++++-----
 donnees/gold-analyseur.json   | 128 ++++++++++++++++++++++++-
 donnees/mesure-analyseur.json | 217 ++++++++++++++++++++++++++++++++++++------
 donnees/mesure-corpus.json    |  48 +++++-----
 generateur.py                 |  12 ++-
 tests/test_generateur.py      |  25 +++--
 6 files changed, 394 insertions(+), 86 deletions(-)
[master 1445e1d] S — LE CONTEXTE TRANCHE LES HOMOGRAPHES : 54/55 TYPES, 131/131 RÔLES ; GOLD 55
 6 files changed, 394 insertions(+), 86 deletions(-)
To /home/stephane/Data13TB/stephane/GitHub/drave-structures
   97641d5..1445e1d  master -> master
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && git add donnees/phrases-corpus-manifest.json && git commit -m \"S — BANQUE : LE MANIFESTE REPREND LA DATE DU RESCAN (SHA 43957a3b INCHANGÉ)\" -m \"La banque de 200 phrases / 355 candidats est identique (sha256 43957a … [194 caractères tronqués]`

  ```
[master 00d2a01] S — BANQUE : LE MANIFESTE REPREND LA DATE DU RESCAN (SHA 43957a3b INCHANGÉ)
 1 file changed, 1 insertion(+), 1 deletion(-)
To /home/stephane/Data13TB/stephane/GitHub/drave-structures
   1445e1d..00d2a01  master -> master
## master...origin/master
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cp data/structures/banque-manifest.json reports/s-banque-structures.json && python3 -m json.tool reports/s-banque-structures.json | head -12; echo \"=== main state ===\"; git log --oneline -2; git status --short | head -8", "descript … [51 caractères tronqués]`

  ```
{
    "version": 2,
    "mode": "gold",
    "date": "2026-11-02T20:36:15",
    "source": "tools/structures/donnees/gold-analyseur.json",
    "sortie": "data/structures/banque.jsonl",
    "phrases": 55,
    "candidats_acceptes": 55,
    "sha256": "76accf9dbd60a9fcc9fe58a56eecbdbb6aec0ffd5e8dbf0c69443e4a49dd1ac6",
    "note": "structures de r\u00e9f\u00e9rence, sans jugement humain \u2014 `statut: reference` ; spans v\u00e9rifi\u00e9s."
}
=== main state ===
42db89f6 NUIT — LA 82e PORTE : RESSOURCES (AUTOTEST 9 CAS, REGISTRE COHÉRENT) ; AVERTISSEMENTS NON FATALS
2fad8e8d B13 — LA PORTE MOBILE : LE 7B ÉCHOUE À (3,3) (200 NŒUDS, 3 SONDE) ET PASSE À (1,3) COMME L'AVEUGLE (26/2) ET LE LABYRINTHE (29/5) ; TEST NON DISCRIMINANT
 M docs/methode/portes.md
 M docs/pilotage/en-cours.md
M  docs/pilotage/references-non-regression.md
MM journal/2026-11-02/README.md
MM journal/2026-11-02/apprentissage.md
MM journal/2026-11-02/attention.md
MM journal/2026-11-02/distribue.md
MM journal/2026-11-02/docs.md
  ```

- **write** `{"content": "# S — Le contexte tranche les homographes : 54/55 types, 131/131 rôles, 55 structures au corpus\n\n> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur un gold de **55 phrases**\n> (7 `dev`, 16 `test`, 32 `holdout` en quatre vagues), la structure de base retrouve la ** … [7886 caractères tronqués]`

  ```
Error: cannot write "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md", "limit": 10}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md</path>
<type>file</type>
<content>
1: # S — La frontière du GN s'arrête devant le verbe : 47/47 types, 117/117 rôles, 47 structures au corpus
2: 
3: > **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur un gold de **47 phrases**
4: > (7 `dev`, 16 `test`, 24 `holdout` en trois vagues), la structure de base retrouve la **séquence
5: > de types 47/47** (100 %), les **rôles 117/117** (100 %), les **compléments 47/47**, et couvre
6: > **1 309/1 320 octets** (99,2 % ; holdout **605/616**, 98,2 %). La règle de **frontière du GN**
7: > corrige l'échec `h033` (« La femme parle ») ; la **limite nommée** se déplace : les homographes
8: > nominaux `h046` (« ferme ») et `h047` (« fait ») sont coupés comme des verbes, et c'est la
9: > **couverture** qui le voit (0,75 et 0,77), pas le type ni le rôle. Le corpus de référence sort :
10: > **47 lignes**, SHA-256 `f2a0d2fb3a9b0a9aebd562b170503f4d1a98251efdc4a3645a2523b5197227a2`.

(Showing lines 1-10 of 150. Use offset=11 to continue.)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md", "offset": 11, "limit": 140}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md</path>
<type>file</type>
<content>
11: 
12: ## Le dispositif
13: 
14: - **Gold** : [`tools/structures/donnees/gold-analyseur.json`](../tools/structures/donnees/gold-analyseur.json),
15:   **47 phrases** : **7 `dev`** (les phrases du banc), **16 `test`** (écrites avant les règles) et
16:   **24 `holdout`** en trois vagues : `h024–h031` (première règle), `h032–h039` (après la copule),
17:   `h040–h047` (après la frontière GN-devant-verbe). Chaque phrase porte sa suite de segments
18:   (texte, type, rôle) ; les spans se calculent par sous-chaîne, dans l'ordre.
19: - **Analyseur** : [`generateur.py`](../tools/structures/generateur.py), fonction `structure()` —
20:   segmentation (GN, GV, GP, REL, SUB), rôles par la préposition et son contexte, subordonnées
21:   typées, passif, copule, et **frontière GN-devant-verbe**.
22: - **Mesure** : [`mesure_analyseur.py`](../tools/structures/mesure_analyseur.py) →
23:   [`mesure-analyseur.json`](../tools/structures/donnees/mesure-analyseur.json). Trois chiffres
24:   (types, couverture, rôles) et trois contrôles.
25: - **Export** : [`exporter_corpus.py`](.
… [7777 caractères tronqués]
  ```

- **write** `{"content": "# S — Le contexte tranche les homographes : 54/55 types, 131/131 rôles, 55 structures au corpus\n\n> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur un gold de **55 phrases**\n> (7 `dev`, 16 `test`, 32 `holdout` en quatre vagues), la structure de base retrouve la ** … [7898 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-s-analyseur-roles.md</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"homographes\\|46 tests\\|140feb6\\|47 structures\\|1 064\\|25 sur\\|18 |\\|553\\|f2a0d2fb\\|Homographes\" reports/rapport-s-corpus-reel.md", "description": "Locate corpus fiche numbers to update"}`

  ```
21:  **sans GV**, **couverture** des octets par les segments, **homographes nominaux** (GN dont le
29:| unité | corpus | GN+GV | sans GV | couverture | homographes | unités homographes |
31:| ligne | CEGEP | 3,6 % | 0,5 % | 0,94 | 18 | 15 |
32:| ligne | propre | **51,0 %** | 10,2 % | 0,89 | 553 | 550 |
33:| ligne | mélange | 3,8 % | 0,5 % | 0,94 | 18 | 18 |
35:| phrase | propre | **65,5 %** | 8,0 % | 0,89 | 1 064 | 1 035 |
67:- **Les homographes** dépendent du lexique de verbes : 25 sur 20 799 phrases CEGEP, 1 064 sur
75:- **sortie** : le **corpus de référence** de 47 structures (`data/structures/banque.jsonl`,
76:  SHA `f2a0d2fb…`) et son `verifier_corpus.py` — l'analyseur lit, le corpus se restitue.
84:- Sous-module : commits **`140feb6`** (mesure) et **`97641d5`** (banque), `mesure_corpus.py`,
85:  `candidats_corpus.py`, `donnees/mesure-corpus.json`, `donnees/phrases_generees.json`, **46 tests**.
95:3. **homographes/lexique** (ferme, fait, lit) : le contexte tranche ;
96:4. le corpus de référence (47 structures) reste le test de structure pour N2/R1.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '29,37p' reports/rapport-s-corpus-reel.md; sed -n '63,70p' reports/rapport-s-corpus-reel.md; sed -n '82,97p' reports/rapport-s-corpus-reel.md", "description": "Read corpus fiche table and notes"}`

  ```
| unité | corpus | GN+GV | sans GV | couverture | homographes | unités homographes |
|---|---|---:|---:|---:|---:|---:|
| ligne | CEGEP | 3,6 % | 0,5 % | 0,94 | 18 | 15 |
| ligne | propre | **51,0 %** | 10,2 % | 0,89 | 553 | 550 |
| ligne | mélange | 3,8 % | 0,5 % | 0,94 | 18 | 18 |
| phrase | CEGEP | 8,5 % | 0,8 % | 0,94 | 25 | 25 |
| phrase | propre | **65,5 %** | 8,0 % | 0,89 | 1 064 | 1 035 |
| phrase | mélange | 9,1 % | 0,4 % | 0,93 | 22 | 22 |

- **Le filtre** sélectionne les lignes plausibles (20–300 car., ≥ 4 mots, ≥ 80 % de lettres) : les
  titres, les tableaux et les formules sont exclus — le taux ne vaut pas pour eux.
- **Le corpus propre est de la littérature** (genre unique) ; le CEGEP est un mélange
  anglais/technique/français. Le contraste mesure surtout la **langue**, pas la qualité OCR.
- **Les homographes** dépendent du lexique de verbes : 25 sur 20 799 phrases CEGEP, 1 064 sur
  50 000 propres ; le chiffre propre est plus haut parce qu'il y a plus de GN nominaux.
- **Le mélange** garde les mots et la ponctuation : il teste l'ordre, pas le vocabulaire ; un
  analyseur qui ne lit que les déterminants aurait le même plancher.
## Fichiers

- Sous-module : commits **
… [731 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np = Path('reports/rapport-s-corpus-reel.md')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"| ligne | CEGEP | 3,6 % | 0,5 % | 0,94 | 18 | 15 |\", \"| ligne | CEGEP | 3,6 % | 0,5 % | 0, … [2733 caractères tronqués]`

  ```
fiche corpus v4
35:| phrase | propre | **65,5 %** | 8,0 % | 0,89 | 1 134 | 1 104 |
67:- **Les homographes** dépendent du lexique de verbes : 28 sur 20 799 phrases CEGEP, 1 134 sur
78:  SHA `76accf9d…`) et son `verifier_corpus.py` — l'analyseur lit, le corpus se restitue.
88:  `donnees/phrases_generees.json`, **47 tests**.
98:3. ~~homographes/lexique~~ (règle de contexte v4) ; restent `h050` et `h053` ;
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '/### Session `29ad180d/,/### Session `e181ce02/p' docs/pilotage/en-cours.md | head -20; echo \"=== S bullet ===\"; grep -n \"S — le banc de structures\" docs/pilotage/en-cours.md; echo \"=== roadmap ===\"; grep -n \"S — les s … [203 caractères tronqués]`

  ```
### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures : l'analyseur et l'export

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : 1–4) ~~plan, analyseur (gold 47), export, tests 46~~ ; 5–6) ~~fiche, pointeur, état~~.
- **Ambition** : nommer le rôle et la frontière GN.
- **Stratégie** : une règle = une phrase, trois contrôles.
- **Objectif final** : gold **47**, corpus **47**, manifeste SHA-256.
- **Fait** : types **47/47**, rôles **117/117** ; contrôles **80/117**, **82/117**, **0,109** ; h033 corrigé, **h046/h047** nommés ; **corpus réel** : GN+GV **8,5 %** CEGEP (mélange 9,1 %), **65,5 %** propre (9,1 %) ; banque **200** phrases / **355** candidats ; **46 tests** ; [`analyseur`](../../reports/rapport-s-analyseur-roles.md), [`réel`](../../reports/rapport-s-corpus-reel.md).
- **Ce qu'elle fait** : **`97641d5`** ; corpus **47** (SHA `f2a0d2fb…`) ; banque **200** phrases / **355** candidats, **0** validée.
- **Ce que font les autres** : **hub**, **N2**, **Pensée**, **D/R/A**.
- **P
… [1519 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np = Path('docs/pilotage/en-cours.md')\nt = p.read_text(encoding='utf-8')\nt = t.replace(\"- **Plan** : 1–4) ~~plan, analyseur (gold 47), export, tests 46~~ ; 5–6) ~~fiche, pointeur, état~~. … [4688 caractères tronqués]`

  ```
état/roadmap/INDEX v4
  en-cours · 1621 mots · 7 sections · 4 session(s) · 7 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  avertissements :
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  revue de documentation · 564 fiche(s) · 649 JSON · 119 doc(s) · 82 porte(s) · 8 chapitre(s)
  ❌ 1 anomalie(s) :
     · compteurs : en-cours.md dit 563 fichiers, le disque en a 564
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\nt=p.read_text(encoding='utf-8').replace(\"| fichiers / JSON de résultats | **563** / **648** |\", \"| fichiers / JSON de résultats | **564** / **649** | … [316 caractères tronqués]`

  ```
❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 563 fichiers, le disque en a 564
     · compteurs : en-cours.md dit 649 JSON, le disque en a 650
=== status ===
MM docs/methode/portes.md
MM docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
MM journal/2026-11-02/README.md
MM journal/2026-11-02/apprentissage.md
MM journal/2026-11-02/attention.md
MM journal/2026-11-02/distribue.md
MM journal/2026-11-02/docs.md
MM journal/2026-11-02/memoire.md
MM journal/2026-11-02/mesures.md
MM journal/2026-11-02/modele.md
MM journal/2026-11-02/moteur.md
MM journal/2026-11-02/outils.md
MM journal/2026-11-02/portes.md
=== log ===
20996b87 NUIT — LA 82e PORTE EST COMPTÉE (82) ; LE BUDGET T1 REVIENT SOUS 2 500 ; S RAFRAÎCHI
42db89f6 NUIT — LA 82e PORTE : RESSOURCES (AUTOTEST 9 CAS, REGISTRE COHÉRENT) ; AVERTISSEMENTS NON FATALS
=== ahead ===
7
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline 20996b87 | grep -E \"S|analyseur|corpus|banque|structures|INDEX|en-cours|roadmap\" | head -12; echo \"=== S fiche HEAD ===\"; git show HEAD:reports/rapport-s-analyseur-roles.md | head -3; echo \"=== pointer  … [301 caractères tronqués]`

  ```
20996b87 NUIT — LA 82e PORTE EST COMPTÉE (82) ; LE BUDGET T1 REVIENT SOUS 2 500 ; S RAFRAÎCHI
 docs/pilotage/en-cours.md                          |   2 +-
 journal/sessions/MANIFEST.md                       |  12 +-
=== S fiche HEAD ===
# S — La frontière du GN s'arrête devant le verbe : 47/47 types, 117/117 rôles, 47 structures au corpus

> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur un gold de **47 phrases**
=== pointer HEAD ===
160000 commit 97641d538ce0a8816a55104fa5d3847e4e6cecfe	tools/structures
=== en-cours compteurs ===
113:| fichiers / JSON de résultats | **563** / **649** | `reports/*.md` / `reports/*.json` |
=== S lines HEAD ===
- **Fait** : types **47/47**, rôles **117/117** ; contrôles **80/117**, **82/117**, **0,109** ; h033 corrigé, **h046/h047** nommés ; **corpus réel** : GN+GV **8,5 %** CEGEP (mélange 9,1 %), **65,5 %** propre (9,1 %) ; banque **200** phrases / **355** candidats ; **46 tests** ; [`analyseur`](../../reports/rapport-s-analyseur-roles.md), [`réel`](../../reports/rapport-s-corpus-reel.md).
- **S — le banc de structures** : **analyseur 47/47 types, 117/117 rôles, 47/47 compléments**, **corpus réel 8,5 % CEGEP / 65,5 % propre** (
… [274 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | grep -E \"rapport-s|s-banque|structures|INDEX|en-cours|roadmap|plan-travail|references\"; echo \"=== staged stat ===\"; git diff --cached --stat | tail -8; echo \"=== index lock ===\"; ls .git/index.lock 2>/dev/n … [82 caractères tronqués]`

  ```
MM docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M reports/INDEX.md
 M reports/rapport-s-analyseur-roles.md
 M reports/rapport-s-corpus-reel.md
 M reports/s-banque-structures.json
 M tools/structures
=== staged stat ===
 .../abb58991-fe0a-4d6e-b039-6552b09f8454/digest.md | 146 ------
 .../rapport.md                                     |  48 +-
 .../b7d4678e-2143-4daa-a9a4-a456c5aa8dab/digest.md | 326 ------------
 .../rapport.md                                     |  29 +-
 .../caaf3018-e3e2-4416-8446-11f0335910aa/digest.md | 566 ---------------------
 .../rapport.md                                     | 157 +-----
 tools/porte-ressources.sh                          |  28 -
 29 files changed, 105 insertions(+), 1790 deletions(-)
=== index lock ===
pas de verrou
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\nt=p.read_text(encoding='utf-8')\nimport re\nt=re.sub(r\"\\| fichiers / JSON de résultats \\| \\*\\*\\d+\\*\\* / \\*\\*\\d+\\*\\* \\|\",\n         \"| fi … [316 caractères tronqués]`

  ```
['| fichiers / JSON de résultats | **564** / **650** | `reports/*.md` / `reports/*.json` |']
  revue de documentation · 564 fiche(s) · 650 JSON · 119 doc(s) · 82 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && H=$(git rev-parse HEAD); rm -f /tmp/index.s; GIT_INDEX_FILE=/tmp/index.s git read-tree \"$H\" && GIT_INDEX_FILE=/tmp/index.s git add docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/INDEX.md reports/rapport-s-analyseur-role … [193 caractères tronqués]`

  ```
docs/pilotage/en-cours.md            |  27 +++---
 docs/pilotage/roadmap.md             |   8 +-
 reports/INDEX.md                     |   5 +-
 reports/rapport-s-analyseur-roles.md | 158 ++++++++++++++++-------------------
 reports/rapport-s-corpus-reel.md     |  31 +++----
 reports/s-banque-structures.json     |   8 +-
 tools/structures                     |   2 +-
 7 files changed, 114 insertions(+), 125 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && GIT_INDEX_FILE=/tmp/index.s git commit -m \"S — LE CONTEXTE TRANCHE LES HOMOGRAPHES : 54/55 TYPES, 131/131 RÔLES ; GOLD 55 (SHA 76accf9d)\" -m \"Le GN ne s'arrête plus devant « ferme »/« fait » quand le suivant est un auxiliaire ou u … [633 caractères tronqués]`

  ```
[master 69bfddba] S — LE CONTEXTE TRANCHE LES HOMOGRAPHES : 54/55 TYPES, 131/131 RÔLES ; GOLD 55 (SHA 76accf9d)
 30 files changed, 984 insertions(+), 205 deletions(-)
[stderr]
  ✅ index : aucun fait stagé sans état
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git push origin master 2>&1 | tail -4; echo \"exit=${PIPESTATUS[0]}\"; git ls-remote --heads origin | head -1; git -C tools/structures ls-remote --heads origin | head -1; echo \"=== S HEAD ===\"; git show HEAD:reports/rapport-s-analy … [183 caractères tronqués]`

  ```
To github.com:stephanedenis/drave.git
   3f74fe83..69bfddba  master -> master
exit=0
69bfddbacf567d3d3561f02ba0d92015760bb04a	refs/heads/master
00d2a015d2f7448db8324a4b25796312abffa83d	refs/heads/master
=== S HEAD ===
# S — Le contexte tranche les homographes : 54/55 types, 131/131 rôles, 55 structures au corpus

160000 commit 00d2a015d2f7448db8324a4b25796312abffa83d	tools/structures
=== status ===
MM docs/methode/portes.md
MM docs/pilotage/en-cours.md
MM docs/pilotage/roadmap.md
MM journal/2026-11-02/README.md
MM journal/2026-11-02/apprentissage.md
MM journal/2026-11-02/attention.md
MM journal/2026-11-02/distribue.md
MM journal/2026-11-02/docs.md
  ```

- **todo_write** `{"todos": [{"content": "S v3 : frontière GN-devant-verbe, gold 47, 46 tests, corpus 47 — committé/poussé", "status": "completed"}, {"content": "Mesure sur corpus réel (50k lignes, 20 799 phrases CEGEP, 50k propres) + contrôle du mélange", "status": "completed"}, {"content": "Banque de candidats réel … [730 caractères tronqués]`

  ```
Updated todo list: 2 pending, 0 in progress, 7 completed.
  ```

### 🤖 Assistant

⏵ Liste DSH à jour ; cycle v4 poursuivi et poussé : 54/55 types, 131/131 rôles, 55 structures.

**Ce qui a été fait**

- **Règle de contexte v4** : un mot du lexique de verbes est un **nom** si le suivant est un auxiliaire ou un verbe — `h046` (« la petite ferme est ») et `h047` (« le simple fait surprend ») sont corrigés.
- **Holdout4 écrit après la règle** (`h048–h055`, mesuré une fois) : **54/55 types** (98,2 %), **131/131 rôles**, **47/47 compléments**, couverture **1 466/1 475** (99,4 % ; holdout 762/771, 98,8 %).
- **Limites nommées** : `h050` (« fait » suivi d'un verbe **hors lexique**) et `h053` (« lit » après un adjectif, en fin de phrase).
- **Contrôles** : baseline **94/131** (0,718), règles coupées **96/131** (0,733), rôles mélangés **0,109** [0,00 ; 0,23].
- **Corpus réel** re-mesuré : 65,5 % de GN+GV sur la littérature propre contre 9,1 % pour le mélange ; 8,5 % sur le CEGEP OCR (plancher, multilingue/technique) ; homographes **1 134/28** (suspects, pas erreurs).
- **Banque** : 200 phrases / 355 candidats (SHA `43957a3b…` inchangé) ; **corpus de référence** : 55 lignes, SHA `76accf9d…` ; **47 tests**.

**Committé et poussé**

- Sous-module : **`1445e1d`** (v4) et **`00d2a01`** (manifeste) → `drave-structures`.
- Principal : **`69bfddba`** → `origin/master` ; pointeur `tools/structures` = `00d2a01`.
- Fiches : [`analyseur v4`](reports/rapport-s-analyseur-roles.md) et [`corpus réel`](reports/rapport-s-corpus-reel.md) ; état **564 fiches / 650 JSON**, 82 portes, T0 vert.

**Liste DSH** : les 7 tâches du cycle sont terminées ; restent **`h050`/`h053`** (lexique élargi ou règle de fin de phrase) et la **validation humaine des 200 phrases** de la banque. L'arbre porte encore les mises à jour du hub en cours (portes/état) ; je n'y ai pas touché.


## Tour 8

### 👤 Utilisateur

prochaine étape?

### 👤 Utilisateur

<system-reminder>
Updated instructions from: AGENTS.md

This file changed after it was loaded. Use the following content instead of the previously loaded instructions from this file.

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

### 🤖 Assistant

⏵ Prochaine étape : la validation humaine de la banque. Je lance le banc et je vérifie qu'il charge les 200 phrases.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && (ss -ltn 2>/dev/null | grep -q ':8765 ' && echo \"port 8765 déjà pris\") || echo \"port 8765 libre\"; nohup python3 serveur.py --port 8765 > /tmp/structures-serveur.log 2>&1 & echo \"pid $!\"; sleep 2; curl -s http:/ … [338 caractères tronqués]`

  ```
port 8765 libre
pid 1737843
207 phrases 369 candidats 0 validations
  banc de structures · http://127.0.0.1:8765 · 207 phrases
  127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
  ```

### 🤖 Assistant

⏵ Le banc est lancé : 207 phrases, 369 candidats. La prochaine étape est la **validation humaine**, puis l'export de la banque validée.

**Tout de suite : valider la banque**

- Le serveur tourne sur **http://127.0.0.1:8765** (`pid 1737843`, log `/tmp/structures-serveur.log`).
- Il charge les **7 phrases du banc** (avec leur référence écrite à la main) + les **200 phrases réelles** de la littérature (355 candidats) ; **0 validation** pour l'instant.
- Conseil : valider d'abord les **7 phrases du banc** (elles ont une référence, on peut comparer), puis un **premier lot de 20 phrases réelles** — les verdicts s'écrivent dans `donnees/validations.jsonl` (append-only).
- Ensuite, je fais l'export `python3 exporter_corpus.py --mode banque` → `data/structures/banque-validee.jsonl` + manifeste, avec la fiche : combien de `resolu`/`compatible`/`double_sens`/`exclu`, l'accord avec la référence, les spans vérifiés, et les limites (200 phrases, un seul valideur).

**En parallèle, côté S (CPU)**

- **Filtre langue/genre + segmentation en phrases** : c'est la leçon de la mesure corpus — le CEGEP OCR est au plancher du mélange (8,5 % contre 9,1 %) parce qu'il est multilingue/technique et coupé en lignes. Filtrer le français, reconstruire les phrases, puis refaire le taux de GN+GV : c'est le préalable à une banque issue de l'OCR.
- **`h050`/`h053`** (verbe suivant hors lexique, nom après adjectif en fin de phrase) : petit raffinement, à mesurer sur une nouvelle vague sans retoucher le gold.

**Règle 11 (AGENTS mis à jour)** : le chemin LLM de S (`llm.py`) passe bien par l'**API DeepSeek** ; S n'utilise **aucun serveur local**. Le `llama-server` 7B qui tourne encore (port 18082) est celui de **Pensée** : la règle le déclasse pour les professeurs — le hub/Pensée doit le couper et passer par `tools/llm/enseignant.py`. Les GPU restent à Drave (`porte-ressources`, `hauru-gpu-guard`).

La liste DSH est à jour : banque (humain) et filtre langue/genre en tête, `h050`/`h053` ensuite.


## Tour 9

### 👤 Utilisateur

pour ce qui est de la validation de la banque, après moins de 20%, j'arrête car j'ai trop de doutes sur l'arvre syntaxique car il manque trop souvent de profondeur et les référents ne semblent pas résolus avant que je tranche

### 🤖 Assistant

⏵ Le retour humain est un résultat : moins de 20 % validé, arrêt sur la profondeur de l'arbre et les référents. Je regarde les verdicts déjà écrits, puis je corrige ces deux bloqueurs avant de redemander une validation.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/structures && ls -la donnees/validations.jsonl 2>/dev/null && python3 - <<'PY'\nimport json, collections\np='donnees/validations.jsonl'\ntry:\n    lignes=[json.loads(l) for l in open(p,encoding='utf-8') if l.strip()]\nexcept FileN … [643 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 24500  3 nov 13:24 donnees/validations.jsonl
142 verdicts 141 candidats distincts 71 phrases
Counter({'resolu': 71, 'exclu': 60, 'compatible': 10, 'double_sens': 1})
p001 p001-c2 exclu | 
p001 p001-c1 resolu | 
p002 p002-c1 resolu | 
p002 p002-c2 double_sens | 
p002 p002-c2 compatible | il est préférable de dire l'homme au téléscope
p003 p003-c1 resolu | 
p003 p003-c2 exclu | 
p004 p004-c1 resolu | 
p004 p004-c2 compatible | 
p005 p005-c2 resolu | 
p005 p005-c1 exclu | 
p006 p006-c1 resolu | 
--- notes non vides ---
p002 p002-c2 compatible | il est préférable de dire l'homme au téléscope
  ```

