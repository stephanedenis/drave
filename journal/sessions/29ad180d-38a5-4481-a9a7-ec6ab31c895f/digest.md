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

