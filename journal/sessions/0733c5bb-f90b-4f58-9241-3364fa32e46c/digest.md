# Session DSH — relecture

- identifiant : `0733c5bb-f90b-4f58-9241-3364fa32e46c`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-02 16:14:00
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu es la session N2 (le natif, GPU). Lis AGENTS.md, docs/pilotage/en-cours.md et  docs/pilotage/backlog/N2-distillation.md. Ton id est dans `printenv DSH_SESSION_ID` ; crée  journal/sessions/<id>/plan.md avec `python3 tools/sessions.py --modele` (les onze champs,  État : actif, heartbeat maintenant), puis réserve `data/`, `tools/corpus*`, `reports/n2-*`,  `work/n2*`. Prochaine action : 200 000 pas sur le mélange 1 Go (N2.ac : 3,49 domaine /  6,03 littérature), puis R1.1/R1.2. Un fait = mesure + contrôle négatif + fiche + en-cours +  commit (`git add` explicite). Ne touche pas à en-cours, roadmap, chantiers, AGENTS sans le hub.  À la fin du cycle, rends ta ligne d'état et le hash du commit.

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

⏵ Lecture des instructions et de l'état du projet

- **bash** `{"command": "printenv DSH_SESSION_ID; echo \"---\"; pwd; echo \"---\"; ls", "description": "Get session ID and workspace listing"}`

  ```
0733c5bb-f90b-4f58-9241-3364fa32e46c
---
/home/stephane/GitHub/Qtrinet
---
AGENTS.md
bench
colab
data
docs
drave-core
journal
models
__pycache__
Qtrinet-bootstrap.md
README.md
reports
REPRISE.md
run_8bit_perfection.py
run_clusters.py
run_cpu.py
run_encoding.py
run_harness.py
run_list_mode.py
run_precision.py
run_quantify.py
run_real_clusters.py
run_sparsity.py
run_value_encoding.py
sprints
src
tools
work
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

### 🤖 Assistant

⏵ Lecture de l'état courant et du backlog N2

- **bash** `{"command": "ls -la /home/stephane/GitHub | head -20; echo \"---\"; readlink -f /home/stephane/GitHub/Qtrinet; echo \"---\"; readlink -f /home/stephane/Data13TB/stephane/GitHub/Qtrinet; echo \"---\"; git -C /home/stephane/GitHub/Qtrinet log --oneline -5; echo \"---\"; git -C /home/stephane/GitHub/Qt … [89 caractères tronqués]`

  ```
lrwxrwxrwx. 1 stephane stephane 39 29 jui 14:20 /home/stephane/GitHub -> /home/stephane/Data13TB/stephane/GitHub
---
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
---
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
---
04d75114 ÉTAT — HORODATAGE RÉEL (16 h 09) APRÈS LA REPRISE ; LE FUTUR N'EST PAS UNE HEURE
97d693b6 ÉTAT — T0 REVENU SOUS 4 000 (3 998) APRÈS LE RUNBOOK
566ac478 HUB — LE RUNBOOK EST PUBLIÉ ; HEARTBEAT À JOUR, PROCHAINE ACTION LA PASSE DE PORTES
2dab14e4 PILOTAGE — L'ÉTAT REPREND : 140/140, N2.ac, DEUX SESSIONS EN PAUSE, PORTE STRICTE
86cfb580 N2 — N2.ac EST LE MODÈLE DE PRODUCTION : LE MÉLANGE 1 Go, LE CANAL ET LA PÉNALITÉ
---
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
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
19: 
20: ### Sess
… [11399 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du mandat N2 (distillation)

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/docs/pilotage/backlog/N2-distillation.md"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/docs/pilotage/backlog/N2-distillation.md</path>
<type>file</type>
<content>
1: # N2 — Distillation native (50 000 séquences)
2: 
3: > **Statut** : en cours · **Priorité** : P1 · **Programme** : N · **Dépend de** : N1
4: > **Ligne de roadmap** : N2 · **Fiche de résultat attendue** : rapport-n2-distillation.md (à créer dans `reports/`)
5: > **Résumé** : Faire tenir le natif sans professeur, sur 50 000 séquences, avec la porte < 2,5 de PPL.
6: > **Glossaire** : [distillation](../../theorie/glossaire/entrees/distillation.md) · [professeur / élève](../../theorie/glossaire/entrees/professeur-eleve.md) · [perplexité](../../theorie/glossaire/entrees/perplexite.md) · [BPE](../../theorie/glossaire/entrees/bpe.md).
7: 
8: ## Le besoin
9: 
10: Le student plafonne à 2,708 et la porte < 2,5 n'est pas atteinte. Les 130–256 de contexte sont négatifs ; il faut décider si le levier est la donnée, la capacité ou la hiérarchie.
11: 
12: **Le levier retenu le 2026-10-29 est la hiérarchie** (l'état de section), et c'est **N2 qui la porte** : R11 en mesurera la fenêtre. Les longueurs brutes ne sont plus essayées — cinq négatifs suffisent.
13: 
14: ## L'état
15: 
16: Le
… [1507 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls tools/sessions.py && python3 tools/sessions.py --help 2>&1 | head -60", "description": "Inspect sessions tool help"}`

  ```
tools/sessions.py
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
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 tools/sessions.py --modele; echo \"=== STATUS ===\"; python3 tools/sessions.py --status 2>&1 | head -60", "description": "Show session plan template and status"}`

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

=== STATUS ===
sessions · plans de mandat
    0b0a6a0d-05f5-4308 · terminé  · 1899 min · N2.h — corpus propre, porte honnête, généralité, verrou de longueur
      → close — N2.i (3,13 / 12,93 / 33,83) et Pensée v0 (6/6 portes) sont committés.
    0b69f616-5c75-4c34 · terminé  · 3973 min · R0.4, R0.5, R13, R4.1–R4.3, en-cours, roadmap, backlog
      → clôture reprise par la session `22e518ee` — commit, archives, état.
    22e518ee-81b8-4081 · terminé  · 3144 min · archives de sessions, journal, en-cours, roadmap, backlog, outillage d'archivage
      → clôture committée (`eff8d8e4`) — session close ; la suite est **N2** (la hiérarchie), portée par la session à ouvrir
    536cd5d6-94ac-4057 · actif    ·   5
… [1826 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inventaire des outils et rapports N2 existants

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls reports/ | grep -i n2; echo \"=== TOOLS ===\"; ls tools/ | head -80; echo \"=== WORK ===\"; ls work/ 2>/dev/null | head -40; echo \"=== DATA ===\"; ls -la data/ 2>/dev/null | head -40", "description": "List N2 reports, tools, work, data"}`

  ```
n2-budget.json
n2-distillation.json
n2-hierarchie.json
n2-propre.json
rapport-n2-34m-distille.md
rapport-n2-anglais-34m.md
rapport-n2-anglais-distille.md
rapport-n2-anglais.md
rapport-n2-budget.md
rapport-n2-canal-34m.md
rapport-n2-canal-distille.md
rapport-n2-canal-kd-34m.md
rapport-n2-canal.md
rapport-n2-capacite-34m.md
rapport-n2-capacite.md
rapport-n2-capacite-reelle.md
rapport-n2-combine.md
rapport-n2-corpus-1go.md
rapport-n2-corpus-elargi.md
rapport-n2-corpus-reel.md
rapport-n2-distillation.md
rapport-n2-distillation-reelle.md
rapport-n2-diversite.md
rapport-n2-echantillon.md
rapport-n2-fenetre-r1.md
rapport-n2-hierarchie.md
rapport-n2-longueur.md
rapport-n2-longueur-reelle.md
rapport-n2-melange.md
rapport-n2-multilingue-34m-distille.md
rapport-n2-multilingue-34m.md
rapport-n2-multilingue-capacite.md
rapport-n2-multilingue-distille.md
rapport-n2-multilingue.md
rapport-n2-pas-vs-texte.md
rapport-n2-professeur.md
rapport-n2-propre.md
rapport-vision-qwen2vl.md
=== TOOLS ===
adaptateur_langue.py
aiguille.py
aligneur_litteraire.py
amplification.py
analyse_alignement.py
analyse_empreinte.py
analyse_engram.py
analyse_experts_statique.py
analyse_flux.py
analyse_hc.py
analyse_litterai
… [4393 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des fiches N2.ac et du dispositif d'entraînement

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat reports/rapport-n2-corpus-1go.md", "description": "Read 1GB corpus report"}`

  ```
# N2.aa — Le corpus de 831 Mo à compute constant : un autre domaine, pas plus de savoir

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : à recette égale (34,3 M, deux
> étages de 20 000 pas, canal), le corpus de **831 Mo** (600 000 articles, offset 1 M, **0 fuite**)
> donne **3,7025** sur la validation de N2.z (3,5250) et **3,4604** sur la sienne ; N2.z donne
> **3,5250** sur la sienne et **3,7107** sur celle du grand. **Chaque modèle est meilleur sur son
> propre domaine** (écart ~0,2) : à 40 Mo vus, un corpus 5,6× plus grand ne fait pas apprendre plus
> — il fait apprendre **autre chose**.

## Le dispositif

- **Corpus** : 600 000 articles (page_id à partir de 1 000 000, disjoint du corpus N2.j qui part de
  200 000) ; brut **1 048 Mo** → dédupliqué **924 Mo (88,2 %)** → train **831 Mo**, val 46 Mo, test
  46 Mo ; **0 fuite** sur 4 000 fenêtres (`reports/corpus-wiki-big-propre.json`).
- **Modèle** : 34,3 M (`384/512`), deux étages de 20 000 pas × 8 × 128, positions [0, 384], canal de
  structure — exactement la recette de N2.z.
- **Évaluation croisée** : chaque modèle sur **les deux** validations (la même fenêtre de 4 lots ×
  16 × (L+1) octets, canal fourni),
… [2798 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls work/n2i work/n2j work/n2k work/n2w 2>/dev/null; echo \"=== tools n2 ===\"; ls tools/ | grep -i n2", "description": "List n2 work dirs and n2 tools"}`

  ```
work/n2i:
base.log
base-repo.drvm
base-repo.pt
base-repo.pt.json
coloration.py
eval-ancien.json
eval-ancien.log
eval-ancien.termine
eval.json
eval.log
eval.termine
evalue-ancien.sh
evalue.sh
fiche.md
file-gpu0.out
file-gpu0.sh
file-gpu1.out
file-gpu1.sh
gpu0.termine
gpu1.termine
I-g1.json
I-g1.log
I-g1.out
I-g1.pt
I-g2.json
I-g2.log
I-g2.out
I-g2.pt
I-g3.json
I-g3.log
I-g3.out
I-g3.pt
remplit.py
route-teacher-repo
teacher.log
typoglycemie.py

work/n2j:
base-34m-canal.drvm
base-34m-canal-g2.drvm
base-34m-canal-g2.log
base-34m-canal-g2.pt
base-34m-canal-g2.pt.json
base-34m-canal.log
base-34m-canal.pt
base-34m-canal.pt.json
base-canal.drvm
base-canal.log
base-canal.pt
base-canal.pt.json
base-curriculum.drvm
base-curriculum.log
base-curriculum.pt
base-curriculum.pt.json
base-nonambigu.drvm
base-nonambigu.log
base-nonambigu.pt
base-nonambigu.pt.json
base-placebo.drvm
base-placebo.log
base-placebo.pt
base-placebo.pt.json
base-temoin.drvm
base-temoin.log
base-temoin.pt
base-temoin.pt.json
base-unamb.drvm
base-unamb.log
base-unamb.pt
base-unamb.pt.json
base-wiki-45m.drvm
base-wiki-45m.log
base-wiki-45m.pt
base-wiki-45m.pt.json
base-wiki-cap.drvm
base-wiki-cap.log
base-wiki-cap.pt
base-wiki
… [3467 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rl \"6,03\\|6.03\" reports/*.md | head; echo \"=== 3,49 ===\"; grep -rl \"3,49\" reports/*.md | head", "description": "Find report with 3.49 / 6.03 figures"}`

  ```
reports/campagne-benefices.md
reports/INDEX.md
reports/rapport-a80-porte-bus.md
reports/rapport-a80-porte-gain.md
reports/rapport-budget-attention-allocation.md
reports/rapport-chargement-paresseux.md
reports/rapport-n2-melange.md
reports/rapport-n2-multilingue-distille.md
reports/rapport-pensee-silencieuse.md
reports/rapport-placement-bits-kv.md
=== 3,49 ===
reports/rapport-a83a-flux.md
reports/rapport-c9-echange-experts.md
reports/rapport-n2-canal-34m.md
reports/rapport-n2-canal-kd-34m.md
reports/rapport-n2-combine.md
reports/rapport-n2-corpus-1go.md
reports/rapport-n2-melange.md
reports/rapport-parcimonie-entrainee.md
reports/rapport-v41-mhc.md
reports/rapport-vram-transfert.md
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat reports/rapport-n2-canal-34m.md | head -80", "description": "Read canal 34m report"}`

  ```
# N2.z — Le canal à 34,3 M : 4,00 → 3,51, le meilleur modèle de la nuit

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : le canal de structure, qui
> valait **−0,22** à 11,47 M (N2.l), vaut **−0,47** à 34,3 M : la base passe de **3,9973** à
> **3,5250** (moyenne de **2 graines** : 3,5131 et 3,5369) à 128 octets, **3,4926** à 256,
> **3,6632** à 512 — la **meilleure PPL de la nuit**, devant le 34,3 M distillé (3,6852, N2.r).
> Le gain du canal **croît avec la capacité**, et il se reproduit d'une graine à l'autre (±0,012).

## La question

N2.l avait mesuré le canal à 11,47 M (−0,22) ; N2.x avait montré que la distillation l'absorbe à
cette taille (−0,03). La question : à 34,3 M, où la capacité paie (N2.p), le canal paie-t-il
davantage — ou la capacité l'absorbe-t-elle aussi ?

## Le dispositif

- Base : 34,3 M (`384/512`), positions [0, 384], val 3,9973 (N2.p).
- Réentraînement : 20 000 pas × 8 × 128, lr 3e-4, graine 1, positions [0, 384], **avec le canal**
  (6 classes par octet, 1 344 paramètres), depuis `base-wiki-45m.pt`.
- Évaluation : `evalue_canal.py` (canal fourni), 128/256/512, mélange.

## Ce qui est mesuré

| modèle | 128 | 256 | 512 | mélange « milieu
… [2378 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat reports/rapport-n2-melange.md", "description": "Read melange report"}`

  ```
# N2.ac — Le mélange des deux corpus : la largeur sans perdre le français

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : le modèle entraîné sur le
> **mélange** (186 Mo + 831 Mo = **1,02 Go**, 60 000 pas) vaut **3,4902** sur la validation
> française (fr-60k : 3,4365 ; big-60k : 3,5877), **6,0283** en littérature (**le meilleur**),
> **8,3352** en anglais (≈ big-60k 8,3173, bien mieux que fr-60k 9,5185) et **9,0525** sur
> wikitext2 (**le meilleur**). **La largeur sans perdre le français.**

## Le dispositif

- Corpus : `data/wiki_fr/propre/train.txt` (186 Mo) + `data/wiki_big/propre/train.txt` (831 Mo)
  concaténés = **1,02 Go** ; canal concaténé ; validation = celle de N2.z (la même pour les trois).
- Recette : 34,3 M, **60 000 pas** × 8 × 128, positions [0, 384], canal — identique à fr-60k et
  big-60k.
- Évaluation : val fr, val grand, littérature, anglais, wikitext2 (avec canal).

## Ce qui est mesuré

| modèle | val fr | val grand | littérature | anglais | wikitext2 |
|---|---:|---:|---:|---:|---:|
| **fr-60k** (186 Mo) | **3,4365** | 3,7237 | 6,0011 | 9,5185 | 10,7138 |
| **big-60k** (831 Mo) | 3,5877 | **3,3301** | 6,1381 | **8,3173** | 9,1609 |
| **mi
… [1749 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Compréhension du harnais d'entraînement (drave-core)

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat work/n2w/mix-60k.drvm; echo \"=== log head ===\"; head -40 work/n2w/mix-60k.log; echo \"=== log tail ===\"; tail -20 work/n2w/mix-60k.log", "description": "Inspect drvm config and training log"}`

  ```
<��p<r�=�U���̼����O=ˮ�
��<L�=���=wf	��W���Z��聈=
*$=Z�.=��3��P;�z�����i&<�i�=��R<|�=Z6;:h�%>��=V">˕�=O?���
�<�@�;oJ�������f�A6�s�#��1�=5S9�@����b=��+���<ސҽ��<ض
=wTżMQN��?Z�*|�="1��懼�K���)=��=m8=��=�*�<�.��.z<=l�����<,� <�Ɠ�k%g�e"= 5�<�*�<��R����=Cv�<w�,������������������=�߸��JG��^<�������H������a��%�<�^<��<�|��t6�<�7s=��6��p�]� <0C�p�P=-u�����(�=�%��a���I=0ĕ�v��h�<��(½�`=(��<�݆��֥=8��;<?�<���<�����M��&=�W�=��T<RO��Z��{Sü������<3��<����o��=��;=<@��D����3��j㕼��
>7��OH��ҝ<ܴ=��M���j��Hm=�f=�@�S�=�G�<3O�'0��j\ >�O�<�92<[�ǼݏP�sJ��
���e�~�� 0=O2=�"�'_�b>��Z�^=�՘��=�</%��C��?�+�g���|g�_�����=��K�U8=�F�< �>@�C�b����ӈ=EP�;�y�ս<eĽj�	�3�9����-$=xm=[D>�Ｅ�d���<�C=��~���=���;��ϽK�<㮕���5U�=It��`�<�Ӽ
S��@�Z��Q�>ʩ�T%��]�,<4d=)1=JE$=���<�1}<ڒ<`An�C�3�}6ҽ�-�^�<�k��F��:?<��\[��<$
=��<�7�=��a9(�=6�l��T=x;�=����Y����<�=�a�=��=�nܼ-<k��Ћ=�F�<YO =8 ˼�=��n���9=Zs�m�=�A=��;�*��=�/d=~�(��0�=m� �wh�<���<4/�<�����B>%��<~�&��c>�8d��nq=��Լnt>�������=���=��v:�X�<T<Q��Ng;�
 ���h����v����=|���f�=碗;Ĕ=��8�(p�;��������U��M9w��]u<*4����=C�U�g��=ٗ꼑ߖ=#w�;w�:��ý�����_=6����V�����=_����ҽR�=Ub�<$�L=�������<
… [48714 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls drave-core; echo \"=== src ===\"; ls src | head -30; echo \"=== data/wiki_mix ===\"; ls -la data/wiki_mix/propre/ 2>/dev/null | head; du -sh data/wiki_mix 2>/dev/null", "description": "Inspect drave-core and mix corpus"}`

  ```
Cargo.lock
Cargo.toml
gpu
README.md
src
target
tests
=== src ===
bpe_np.py
encoding.py
gguf_min.py
__pycache__
roofline.py
sparsity.py
ternary.py
tiny_model.py
transformer_np.py
=== data/wiki_mix ===
total 2007456
drwxr-xr-x. 1 stephane stephane         72  2 nov 12:25 .
drwxr-xr-x. 1 stephane stephane         12  2 nov 12:25 ..
-rw-r--r--. 1 stephane stephane 1017487092  2 nov 12:25 train.canal
-rw-r--r--. 1 stephane stephane 1017487092  2 nov 12:25 train.txt
-rw-r--r--. 1 stephane stephane   10330112  2 nov 12:25 val.canal
-rw-r--r--. 1 stephane stephane   10330112  2 nov 12:25 val.txt
2,0G	data/wiki_mix
  ```

### 🤖 Assistant

⏵ Lecture du script d'entraînement natif et état GPU

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,80p tools/entrainer_native.py; echo \"...\"; wc -l tools/entrainer_native.py", "description": "Read training script header"}`

  ```
#!/usr/bin/env python3
"""entrainer_native.py — entraînement de base de `drave-n0`.

Ce n'est que le **prochain octet** : les pertes locales, les têtes précoces, la
pensée et le pont viendront après. Le but est de mesurer la PPL du modèle natif
et de produire un DRVM lisible par le moteur.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import random
import time

import torch
import torch.nn.functional as F

from tools.native_model import NativeConfig, NativeModel, exporter_drvm
from tools.vdc import departs_vdc


def charger(chemin: str) -> torch.Tensor:
    b = pathlib.Path(chemin).read_bytes()
    if len(b) < 100_000:
        raise SystemExit(f"{chemin} : corpus trop court")
    return torch.tensor(list(b), dtype=torch.long)


def lot(data: torch.Tensor, n: int, seq: int, device: str, compteur: int, canal=None):
    # Van der Corput : même compteur = mêmes fenêtres, sans état aléatoire.
    i = torch.tensor(departs_vdc(compteur, n, len(data) - seq - 1, seq), dtype=torch.long)
    x = torch.stack([data[j:j + seq] for j in i]).to(device)
    y = torch.stack([data[j + 1:j + seq + 1] for j in i]).to(device)
    c = torch.stack([canal[j:
… [2238 caractères tronqués]
  ```

- **bash** `{"command": "nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv; echo \"=== processes ===\"; nvidia-smi --query-compute-apps=pid,gpu_uuid,used_memory --format=csv 2>/dev/null | head", "description": "Check GPU status"}`

  ```
index, name, memory.used [MiB], memory.total [MiB], utilization.gpu [%]
0, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %
1, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %
=== processes ===
pid, gpu_uuid, used_gpu_memory [MiB]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 80,137p tools/entrainer_native.py", "description": "Read rest of training script"}`

  ```
canal_data = charger_canal(a.canal) if a.canal else None
    n_val = max(10_000, len(data) // 20)
    train, val = data[:-n_val], data[-n_val:]
    canal_train = canal_data[:-n_val] if canal_data is not None else None
    canal_val = canal_data[-n_val:] if canal_data is not None else None
    cfg = NativeConfig(d_model=a.dim, expert_hidden=a.expert_hidden)
    modele = NativeModel(cfg).to(a.device)
    if a.init:
        ck = torch.load(a.init, map_location="cpu", weights_only=False)
        modele.load_state_dict(ck["state"], strict=False)
        print(f"  init : {a.init}", flush=True)
    opt = torch.optim.AdamW(modele.parameters(), lr=a.lr, weight_decay=0.01)
    t0 = time.time(); pertes = []
    for pas in range(1, a.pas + 1):
        modele.train()
        x, y, c = lot(train, a.lot, a.seq, a.device, pas * a.lot, canal_train)
        pos = random.randint(0, a.positions_aleatoires) if a.positions_aleatoires else 0
        sortie = modele(x, pos_debut=pos, canal=c)
        pertes = [F.cross_entropy(sortie["logits"].reshape(-1, 256), y.reshape(-1))]
        if a.tetes:
            for e in sortie["early"]:
                pertes.append(F.cross_entropy(e.reshape(-1, 256), y.resha
… [1971 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat work/n2w/analyse.py; echo \"=== eval_croise ===\"; sed -n 1,60p work/n2w/eval_croise.py", "description": "Read analysis and cross eval scripts"}`

  ```
#!/usr/bin/env python3
"""analyse.py — l'analyseur contre les structures écrites à la main (les 7 phrases du banc)."""
import json, sys
sys.path.insert(0, 'tools/structures')
import generateur

d = json.load(open('tools/structures/donnees/phrases.json'))
lignes = []
for p in d['phrases']:
    ref = p['candidats'][0]
    ref_types = [s['type'] for s in ref['segments']]
    ref_spans = [(s['debut'], s['fin'], s['type']) for s in ref['segments']]
    gen = generateur.analyser(p['texte'])
    gen0 = gen[0] if gen else {'segments': []}
    gen_types = [s['type'] for s in gen0['segments']]
    gen_spans = [(s['debut'], s['fin'], s['type']) for s in gen0['segments']]
    exact = ref_spans == gen_spans
    types_ok = ref_types == gen_types
    couverture = len(set(ref_spans) & set(gen_spans)) / max(1, len(set(ref_spans) | set(gen_spans)))
    lignes.append({"phrase": p['id'], "ref": ref_types, "gen": gen_types,
                   "types_ok": types_ok, "spans_ok": exact, "jaccard": round(couverture, 2)})
    print(f"{p['id']} · types {'OK' if types_ok else 'non'} · spans {'OK' if exact else 'non'} · "
          f"Jaccard {couverture:.2f}\n   réf {ref_types}\n   gén {gen_types}")
print(json.
… [989 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche de la commande exacte du run N2.ac (mix-60k)

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"mix-60k\" --include=*.sh --include=*.md --include=*.py --include=*.log -l . 2>/dev/null | head -20", "description": "Find references to mix-60k"}`

  ```
./reports/rapport-n2-melange.md
./journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md
./journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/rapport.md
./journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/digest.md
./work/n2w/mix-60k.log
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"mix-60k\" journal/ docs/ 2>/dev/null | head -20", "description": "Grep mix-60k in journal and docs"}`

  ```
journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md:20686:- **bash** `{"command": "sleep 300; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -2 work/n2w/mix-60k.log 2>/dev/null; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader; free -g | head -2", "description": "Check the mix training start"}`
journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md:20706:- **bash** `{"command": "sleep 1800; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -1 work/n2w/mix-60k.log 2>/dev/null", "description": "Wait for the mix training"}`
journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md:20720:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -1 work/n2w/mix-60k.log 2>/dev/null; ls work/n2w/mix-60k.pt 2>/dev/null && echo OK", "description": "Check the mix training"}`
journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md:20728:- **bash** `{"command": "sleep 1500; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%H:%M'; tail -1 work/n2w/mix-60k.log 2>/dev/null", "description": "Wait for the mix training"}`
journal/ses
… [4353 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"mix-60k.drvm\\|mix-60k.pt.*--pas\\|--sortie work/n2w\" journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md | head -10", "description": "Find training command for mix-60k"}`

  ```
20256:3485460       00:50  106 /home/stephane/gpu-env/bin/python tools/entrainer_native.py --corpus data/wiki_big/propre/train.txt --canal data/wiki_big/propre/train.canal --pas 20000 --seq 128 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 --positions-aleatoires 384 --init work/n2w/base-big.pt --sortie work/n2w/base-big-canal.pt --drvm work/n2w/base-big-canal.drvm
20417:3497463       13:51  2132 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nohup bash -c 'cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=0 PYTHONPATH=. ~/gpu-env/bin/python tools/entrainer_native.py --corpus data/wiki_fr/propre/train.txt --canal data/wiki_fr/propre/train.canal --pas 60000 --seq 128 --lot 8 --lr 3e-4 --graine 1 --dim 384 --expert-hidden 512 --positions-aleatoires 384 --sortie work/n2w/fr-60k.pt --drvm work/n2w/fr-60k.drvm > work/n2w/fr-60k.log 2>&1' > /dev/null 2>&1 & echo "fr60 $!" nohup bash -c 'cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=1 PYTHONPATH=. ~/gpu-env/bin/python tools/entrainer_native.py --corpus data/wiki_big/propre/train.txt --canal data/wiki_big/propre/train.canal --pas 60000 --seq 128 --lot 8 --lr 3
… [246 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '20417p' journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md | tr ';' '\\n' | grep -n \"mix\" ", "description": "Extract mix training command"}`

  ```
(no output)
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"wiki_mix\\|mix-60k.pt --drvm\\|mix-60k.drvm\" journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md | head -6", "description": "Find mix corpus training invocation"}`

  ```
20658:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && mkdir -p data/wiki_mix/propre && cat data/wiki_fr/propre/train.txt data/wiki_big/propre/train.txt > data/wiki_mix/propre/train.txt && cat data/wiki_fr/propre/train.canal data/wiki_big/propre/train.canal > data/wiki_mix/propre/train.c … [234 caractères tronqués]`
20669:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && nohup bash -c 'cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=0 PYTHONPATH=. ~/gpu-env/bin/python tools/entrainer_native.py --corpus data/wiki_mix/propre/train.txt --canal data/wiki_mix/propre/train.canal  … [427 caractères tronqués]`
20961:- Corpus : `data/wiki_big/propre/` (831 Mo) et `data/wiki_mix/propre/` (1,02 Go), manifeste [`corpus-wiki-big-propre.json`](reports/corpus-wiki-big-propre.json).
  ```

### 🤖 Assistant

⏵ Lecture d'un plan de session existant et du vérificateur de sessions

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md", "description": "Read example session plan"}`

  ```
# Plan de session — D/R/A : les données, le lecteur, le moteur

> **Mandat ouvert** le 2026-11-01 16 h 25 HNE depuis
> [`docs/pilotage/plan-travail.md`](../../../docs/pilotage/plan-travail.md) (§ 2, § 3) — la session
> reprend la session `fe3c05f0` (R4.4 close) pour le rôle **D/R/A**. Le heartbeat est celui de
> l'état.

- **Session** : `fe3c05f0-834b-44f2-8739-501865d652c1`
- **Rôle** : **D/R/A — les données, le lecteur, le moteur** : le texte intégral, l'extraction
  PDF/OCR, la préparation de R1.1/R1.2, A2.6/A8.3.
- **Périmètre** : D (texte intégral, PDF/OCR, licences, stubs), R1.1/R1.2 (préparation), A2.6/A8.3
- **Fichiers réservés** : `data/wikipedia/` (lecture), `data/corpus_wiki_*`,
  `tools/corpus_wikipedia*.py`, `tools/verifie_contamination.py`, `tools/catalogue_corpus.py`,
  `reports/corpus-wiki-*`, `reports/corpus-wikipedia-*`, `reports/inventaire-*`,
  `reports/rapport-corpus-*`, `reports/r11-*`, `reports/r12-*`, `reports/a26-*`, `reports/a83-*`,
  `journal/sessions/fe3c05f0-…/`
- **Heartbeat** : 2026-11-01 22:50
- **État** : en pause
- **Prochaine action** : le **fonds CEGEP** (~127 scans) ; la **clôture** de la session ;
  R1.1/R1.2 après N2, A2.6 après A6.2. Les 20 l
… [1847 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,120p tools/sessions.py", "description": "Read sessions.py beginning"}`

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
… [3993 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 tools/sessions.py --check --strict 2>&1 | tail -30; echo \"=== exit $? ===\"", "description": "Run strict session check"}`

  ```
✅ plans cohérents
=== exit 0 ===
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 120,260p tools/sessions.py", "description": "Read sessions.py check logic"}`

  ```
"""Crée un plan *à confirmer* à partir de la section `en-cours`, sans l'inventer."""
    n = 0
    for s in sections_en_cours(racine):
        chemin = racine / SESSIONS / s["id"] / "plan.md"
        if chemin.exists():
            continue
        chemin.parent.mkdir(parents=True, exist_ok=True)
        heartbeat = s["heartbeat"] or datetime.now().strftime("%Y-%m-%d %H:%M HAE")
        role = s["role"] or "à confirmer"
        fichiers = s["fichiers"] or "à confirmer"
        prochaine = s["prochaine"] or "à confirmer"
        chemin.write_text(f"""# Plan de session — {s['id']}

> **Repris de `en-cours` le {datetime.now().strftime('%Y-%m-%d %H:%M')}** — plan *à confirmer* par la
> session : le heartbeat est celui de l'état, pas une preuve de vie.

- **Session** : `{s['id']}`
- **Rôle** : {role}
- **Périmètre** : à confirmer
- **Fichiers réservés** : {fichiers}
- **Heartbeat** : {heartbeat}
- **Prochaine action** : {prochaine}
- **État** : à confirmer
""", encoding="utf-8")
        n += 1
        print(f"  + {chemin.relative_to(racine)}")
    print(f"  {n} plan(s) créé(s) à confirmer ; les sessions les complètent, elles ne sont pas actives.")
    return 0


def verifier(racine: Pat
… [5436 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 260,340p tools/sessions.py; echo \"=== _modele ===\"; cat journal/sessions/_modele/plan.md 2>/dev/null", "description": "Read full modele template"}`

  ```
> et passe `État : en pause` (arrêt) ou `État : terminé` (retrait) quand elle s'arrête.

- **Session** : `<id>`
- **Rôle** : <chantier / programme>
- **Périmètre** : <A8.0, R13, ...>
- **Fichiers réservés** : `tools/...`, `reports/...`
- **Heartbeat** : <AAAA-MM-JJ HH:MM HAE>
- **Prochaine action** : <une action nommée>
- **État** : actif (ou `en pause` / `terminé`)
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--racine", default=str(RACINE))
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--modele", action="store_true")
    ap.add_argument("--autotest", action="store_true")
    ap.add_argument("--depuis-en-cours", action="store_true",
                    help="crée des plans à confirmer depuis les sections de en-cours")
    a = ap.parse_args()
    if a.modele:
        print(MODELE)
        return 0
    if a.autotest:
        return autotest()
    r = Path(a.racine).resolve()
    if a.depuis_en_cours:
        return depuis_en_cours(r)
    if a.check:
        e, w = verifier(r, strict=a.strict)
      
… [726 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md", "description": "Read previous N2 session plan"}`

  ```
# Plan de session — N2.h, le mètre propre

> **Mandat ouvert** le 2026-10-31 22 h 30 HAE depuis [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md)
> — mandat libre de 10 h (nuit du 31/10 au 1/11). Le heartbeat est celui de l'état.

- **Session** : `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2`
- **Rôle** : calcul : distillation ; corpus ; évaluation
- **Périmètre** : N2.h — corpus propre, porte honnête, généralité, verrou de longueur
- **Fichiers réservés** : `data/`, `tools/corpus*`, `tools/eval_n2_propre.py`,
  `tools/distiller_budget.py`, `reports/n2-*`, `work/n2h/`,
  `journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/`
- **Heartbeat** : 2026-11-01 08:35 EST
- **Objectif final** : un **mètre honnête** pour N2 — corpus dédupliqué (0 % de fenêtres de
  validation dans l'entraînement), chaîne refaite dessus, porte < 2,5 redéfinie — puis trancher
  ce que les chiffres contaminés ne pouvaient pas trancher : la **généralité hors dépôt** et le
  **verrou de longueur**.
- **Résultat** : corpus 4,63 → 3,61 Mo (−22,2 %), **0 / 2 814** fenêtres de validation dans
  l'entraînement (contre 32,8 %) ; chaîne propre **3,09** en domaine, **16,70** sur la littérature
  jamais vue ; di
… [403 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls journal/sessions/ | head -30; echo \"=== dernier journal ===\"; ls journal/ | tail -5", "description": "List session dirs and journal"}`

  ```
00221850-90de-4287-90ee-324a35e504cd
04ed1834-b0f8-42a1-aa21-75a75c19647e
0b0a6a0d-05f5-4308-800c-4792ddb9cbf2
0b2c86eb-7a8d-4eed-a3dd-fb165f1a8630
0b69f616-5c75-4c34-b97a-ae05564812af
0c631fa9-58cb-4d77-a7e0-fc77e5b3f93f
0f3b6070-57ce-4642-b9ec-3b3956f75978
11b2d312-9a7e-4a4e-814f-ed0384ed9d4d
13446299-79d8-497c-ba83-673c176a4637
15d4e6f4-b2ba-44c7-8c0e-03c141280f9b
15fd322f-7e9e-48c0-a970-f36335eb622a
163d631a-6528-4324-b7b3-6487d24feeb5
1820cf6b-c8a4-411c-894c-31195b9ff7a8
18b8879c-f211-43b8-9908-cf65e509b21d
18c3f6d0-5bb1-45bb-9f94-ab0e7812218d
1966e052-ebc6-4f4b-b7f9-6d1c6cb4b445
1f9394fb-6435-4928-9a03-2b258e5a28c5
22bcae27-254b-47b2-acda-87467dab060c
22e518ee-81b8-4081-ae1b-f0d7a777a1d7
235066f5-307a-4285-a882-14bc2d06cb7b
27c99b10-c57e-4599-a23a-f7b1a54c17a1
2c2a6595-b208-446e-bbd1-d0f49eca45e8
2f51f17f-f47c-49d5-958f-cafecd3fe01e
2fd56aa5-7b9b-40b0-9470-05c74b032d55
31f26a6e-65f5-480d-be32-36b9f425b3dd
34e1d4be-3708-4065-ae77-eca21f86e857
3d5618a0-4e3a-45bb-943d-a72c753fb7da
3de141c0-089b-4ceb-8a2e-bd6d83044a5f
42059fde-f06f-4e2c-9a23-8292d887fb6e
482522d1-31f1-43eb-ae9c-a681336404f7
=== dernier journal ===
2026-11-01
2026-11-02
README.md
sessions
THEMES.md
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M %Z'; echo \"---\"; cd /home/stephane/GitHub/Qtrinet && grep -n \"R1.1\\|R1.2\" docs/pilotage/roadmap.md | head -20", "description": "Check date and R1.1/R1.2 in roadmap"}`

  ```
2026-11-02 16:15 EST
---
32:| **N — le natif** | DRVM, `drave-n0`, [distillation](../theorie/glossaire/entrees/distillation.md), usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; N2.h : 3,0904 domaine, 3,85 hors dépôt ; **N2.ac (1 Go) : 3,49 domaine / 6,03 littérature / 8,34 anglais — production** ; N4 partiel | **N2** : 200 k pas sur le mélange 1 Go, puis **R1.1/R1.2** ; **N4** (consigne) |
33:| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **R4.1–R4.4 mesurées** (R4.4 : 4/5 familles ≥ 90 % de parité) ; **R0.7 — bloc linguistique** (398 langues, 0,9687) | **R4.4 close** (limites nommées) ; **R1.1/R1.2** ([contexte](../theorie/glossaire/entrees/contexte.md) natif) ; R2/R3 attendent N5/N4 |
36:| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67,73 G car., 81,2 Go, **8 Ko 0**) ; **PDF** (1 927 doc., 322 Mo) ; **documents** (3 384 doc., 872 M car., 8 Ko 2,07 %) ; **OCR** (20 livres, 7 3
… [4450 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la note de passage N2 → R1 (fenêtre)

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat reports/rapport-n2-fenetre-r1.md", "description": "Read N2 to R1 handoff report"}`

  ```
# N2 → R1 — Ce que la nuit dit à la ligne « fenêtre »

> **Objet.** Une note de **passage** : ce que N2 a mesuré sur la longueur, la position et la
> fenêtre, et ce que R1.1/R1.2 devraient tester en premier. Les chiffres sont dans les fiches
> citées ; ici, seulement les conséquences.

## Trois faits mesurés

1. **La position absolue est un défaut d'architecture, pas une propriété du corpus.** Sur 3,24 Mo
   (N2.h3) comme sur 186 Mo (N2.j2), la PPL à 256 octets tombe de **14,11 → 3,25** et de
   **9,28 → 4,49** quand les positions sont tirées au hasard à l'entraînement. Le coût est petit
   (+0,15 et +0,36 en domaine) ; le gain à 512 est de **÷2,1 à ÷2,4**.
2. **La fenêtre locale (256) est le second plafond, mais elle n'est pas seule.** Élargir le masque
   à l'inférence ne récupère rien (N2.h3b : 6,13 → 6,37) : c'est l'entraînement sur des contextes
   longs qui manque. Et la **capacité** compte : à 34,3 M, la PPL à 512 passe de 5,67 à **4,19**
   (N2.p), sans changer la fenêtre.
3. **La distillation ne lève pas le plafond.** Les élèves reproduisent la courbe du professeur
   (N2.j4, N2.n) : à 512, la distillation ne gagne rien (5,67 → 5,76) parce que le professeur a la
   même fe
… [1544 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du modèle natif (positions, attention)

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,120p tools/native_model.py", "description": "Read native model definition"}`

  ```
#!/usr/bin/env python3
"""native_model.py — `drave-n0`, le modèle natif du programme N.

Ce n'est pas un Qwen3-MoE : c'est un graphe de blocs en **octets**, avec
attention locale, FFN creux routé, sorties précoces, cellule de pensée et pont.
Le modèle est petit (12 M) : c'est un **banc de mécanismes**, pas un assistant.

Le fichier définit l'architecture, l'export DRVM et les tests de forme. Il ne
prétend pas que l'entraînement est fait : N1.2 reste à mesurer.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F

from tools.drvm import TensorSpec, write_drvm


@dataclass
class NativeConfig:
    vocab: int = 256
    d_model: int = 224
    n_blocks: int = 6
    n_heads: int = 4
    expert_hidden: int = 288
    n_experts: int = 8
    top_k: int = 2
    kwta: float = 0.25
    window: int = 256
    max_pos: int = 2048
    thought_steps: int = 2
    early_blocks: tuple[int, ...] = (1, 3, 5)  # 0-based : après 2, 4, 6
    rsn_dim: int = 120


class SparseFFN(nn.Module):
    def __init__(self, cfg: NativeConfig):
        super().__init__()
        self.cfg = cfg
        self.rou
… [3793 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 120,220p tools/native_model.py", "description": "Read model forward and export"}`

  ```
b, s = ids.shape
        x = self.embed(ids) + self.pos(torch.arange(s, device=ids.device) + pos_debut)[None]
        if canal is not None:
            x = x + self.embed_canal(canal)
        early = []; local = []
        for i, bloc in enumerate(self.blocks):
            x = bloc(x)
            if i == self.cfg.n_blocks // 2 - 1:
                # Pont de région : projection apprise entre les deux moitiés.
                x = x + self.bridge(x)
            local.append(self.local_heads[i](x))
            if i in self.cfg.early_blocks:
                early.append(self.early_heads[self.cfg.early_blocks.index(i)](x))
        h0 = x
        for _ in range(self.cfg.thought_steps):
            # Pas CONTRACTANT : tanh(W x + U h0), sans résidu x + ….
            # Le résidu garantissait λ ≈ 1,42 ; le pas contractant ramène λ < 1
            # tout en gardant le contenu par l'injection h0.
            x = torch.tanh(self.thought(x) + self.thought_in(h0))
        return {"logits": self.head_byte(x), "early": early, "local": local,
                "thought": x, "rsn": self.head_rsn(x)}

    def forward_jusqua(self, ids, n_blocs: int, pos_debut: int = 0, canal=None):
        """Passe avant
… [3663 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Préparation du plan de session et vérification des conventions journal

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,60p tools/verifie_journal.py", "description": "Read journal verifier"}`

  ```
#!/usr/bin/env python3
"""verifie_journal.py — un dossier par jour, et les sessions ancrées.

Règles vérifiées :
  1. aucun fichier `journal/AAAA-MM-JJ*.md` à la racine : chaque jour est un **dossier** ;
  2. chaque dossier `journal/AAAA-MM-JJ/` a un `README.md` ;
  3. chaque `README.md` de jour porte une section « Sessions DSH » et un lien vers
     `../README.md#sessions` ;
  4. chaque `journal/sessions/<id>/rapport.md` porte le bloc « Journaux » avec un lien vers
     son jour (ou le journal), vers `en-cours.md` et vers l'index des sessions ;
  5. les liens relatifs de `journal/README.md`, `journal/THEMES.md`, des `README.md` de jour
     et des rapports de session résolvent.

Usage : python3 tools/verifie_journal.py   (code 0 = journal propre)
"""
from __future__ import annotations
import pathlib
import re

RACINE = pathlib.Path(__file__).resolve().parent.parent
JOURNAL = RACINE / "journal"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# les liens markdown, sans les ancres ni les liens externes
LIEN = re.compile(r"\]\(([^)#]+?)(?:#[^)]*)?\)")
EXTERNE = ("http://", "https://", "mailto:", "#")


def liens(texte: str) -> list[str]:
    return [c for c in LIEN.findall(texte)
          
… [1088 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/; echo \"=== README sessions ===\"; sed -n 1,40p journal/sessions/README.md", "description": "Inspect session dir contents and README"}`

  ```
digest.md
plan.md
rapport.md
session.v4.jsonl.zstd
=== README sessions ===
# Sessions — plans vivants et archives

Deux choses différentes vivent ici :

- **`<id>/plan.md`** — le **mandat vivant** d'une session active : périmètre, fichiers réservés,
  heartbeat, prochaine action, état. Il s'écrit **avant** de modifier `docs/pilotage/en-cours.md`
  et se consulte avec `python3 tools/sessions.py --status`.
- **`<id>/rapport.md`** et **`<id>/digest.md`** — l'**archive** d'une session terminée, générée
  par `tools/session_report.py` / `tools/archive_sessions.py` ; les deux outils lisent
  `session.jsonl.zstd` **et** `session.v4.jsonl.zstd` (les traces récentes).
- **`<id>/cloture.md`** — la **clôture écrite à la main** quand le rapport automatique ne dit pas
  ce qui est livré et ce qui reste (`c3d0f0bd`, `f0969e87`) ; `N2-GPU` n'a pas de trace DSH et son
  rapport est écrit à la main.

Un plan n'est pas un état : `en-cours` reste la seule source de l'état. Un plan périmé (heartbeat
> 45 min) est signalé ; une session qui reprend un périmètre périmé le rafraîchit d'abord.

Modèle : [`_modele/plan.md`](_modele/plan.md). Vérification : `python3 tools/sessions.py --check`.

Migration dou
… [297 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 60,140p tools/verifie_journal.py; echo \"=== exemple bloc Journaux ===\"; grep -n -A8 \"Journaux\" journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/rapport.md | head -20", "description": "Read journal rules for session report"}`

  ```
for d in jours:
        index = d / "README.md"
        if not index.exists():
            alertes.append(f"jour sans README.md : {d.relative_to(RACINE)}")
            continue
        t = index.read_text(encoding="utf-8", errors="ignore")
        if "## Sessions DSH" not in t:
            alertes.append(f"section « Sessions DSH » absente : {index.relative_to(RACINE)}")
        if "../README.md#sessions" not in t:
            alertes.append(f"lien vers l'index des sessions absent : {index.relative_to(RACINE)}")

    # 4. rapports de session
    sessions = sorted((JOURNAL / "sessions").glob("*/rapport.md"))
    for r in sessions:
        t = r.read_text(encoding="utf-8", errors="ignore")
        if "**Journaux :**" not in t:
            alertes.append(f"bloc « Journaux » absent : {r.relative_to(RACINE)}")
        if "docs/pilotage/en-cours.md" not in t:
            alertes.append(f"lien vers en-cours absent : {r.relative_to(RACINE)}")

    # 5. liens des index et des rapports de session
    n_liens = 0
    for p in [JOURNAL / "README.md", JOURNAL / "THEMES.md"] + [d / "README.md" for d in jours]:
        if p.exists():
            n_liens += verifier_liens(p, alertes)
    # Les rapp
… [2212 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Création du mandat de session (11 champs, heartbeat maintenant)

- **write** `{"file_path": "/home/stephane/GitHub/Qtrinet/journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md", "content": "# Plan de session — N2, le natif : 200 000 pas et la fenêtre\n\n> **Mandat ouvert** le 2026-11-02 16 h 20 HAE depuis\n> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cou … [2121 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 tools/sessions.py --check 2>&1 | tail -8; echo \"=== commit plan ===\"; git add journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md && git commit -q -m \"N2 — MANDAT 200 k PAS SUR LE MÉLANGE 1 Go, PUIS R1.1/R1.2 (session 0733c5bb)\"  … [76 caractères tronqués]`

  ```
⚠ plan actif non listé dans en-cours : 0733c5bb-f90b-4f58-9241-3364fa32e46c
=== commit plan ===
[stderr]
  ✅ index : aucun fait stagé sans état
[still running after 60000ms; moved to background job bash-36]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-36", "wait": true, "timeout_ms": 120000}`

  ```
dc7f9c56 N2 — MANDAT 200 k PAS SUR LE MÉLANGE 1 Go, PUIS R1.1/R1.2 (session 0733c5bb)
[status: completed, exit code: 0]
  ```

### 🤖 Assistant

⏵ Lancement des 200 000 pas sur le mélange 1 Go (GPU 0)

- **bash** `{"command": "free -g | head -2; nproc; ls -la ~/gpu-env/bin/python", "description": "Check RAM, CPUs, gpu python"}`

  ```
total        used        free      shared  buff/cache   available
Mem:             125          13         102           0          11         112
40
lrwxrwxrwx. 1 stephane stephane 7 31 jui 08:53 /home/stephane/gpu-env/bin/python -> python3
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && mkdir -p work/n2ac && nohup bash -c 'cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=0 PYTHONPATH=. ~/gpu-env/bin/python tools/entrainer_native.py --corpus data/wiki_mix/propre/train.txt --canal data/wiki_mix/propre/train.ca … [421 caractères tronqués]`

  ```
pid 35563
0, 620 MiB, 0 %
1, 710 MiB, 0 %
  ```

- **bash** `{"command": "sleep 45; cd /home/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; tail -3 work/n2ac/mix-200k.log; echo \"--- procs ---\"; nvidia-smi --query-compute-apps=pid,used_memory --format=csv; ps aux | grep entrainer_native | grep -v grep | awk '{print $2, $3, $4, $10}'", "description": "Check tra … [31 caractères tronqués]`

  ```
16:19:10
--- procs ---
pid, used_gpu_memory [MiB]
34404, 616 MiB
34404, 706 MiB
35563 0.0 0.0 0:00
35568 0.0 0.0 0:00
35572 60.0 9.0 0:42
  ```

- **bash** `{"command": "ps -p 34404 -o pid,etime,cmd --no-headers | cut -c1-160; echo \"---\"; sleep 60; cd /home/stephane/GitHub/Qtrinet && tail -3 work/n2ac/mix-200k.log; date '+%H:%M:%S'", "description": "Identify GPU holder and wait for training log"}`

  ```
34404       01:57 llama-cli -m models/Qwen2.5-0.5B-Q4_0.gguf -p Réponds uniquement: {"langue":"fr"} -n 32 --temp 0 --no-display-prompt
---
[still running after 60000ms; moved to background job bash-40]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-40", "timeout_ms": 60000, "wait": true}`

  ```
16:20:12
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-40 (bash: ps -p 34404 -o pid,etime,cmd --no-headers | cut -c1-160; echo "---"; sleep 60; cd /home/stephane/GitHub/Qtrinet && tail -3 work/n2ac/mix-200k.log; date '+%H:%M:%S') finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Chargement du corpus en cours ; lecture du banc d'évaluation

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,80p work/n2w/eval_ood_canal.py", "description": "Read OOD eval script"}`

  ```
#!/usr/bin/env python3
"""eval_ood_canal.py — la PPL hors domaine avec le canal (littérature, anglais, wikitext2)."""
import json, pathlib, sys
import torch
sys.path.insert(0, '.')
sys.path.insert(0, 'work/n2j')
from tools.eval_n2_propre import charge, charger_bytes
from tools.canal_structure import canal as canal_de
import evalue_canal as ec

pt = sys.argv[1]
m = charge(pt)
jeux = [("litterature", "data/corpus_fr_litterature.txt"),
        ("anglais", "data/corpus_en.txt"),
        ("wikitext2", "data/wikitext2_test.txt")]
res = {"fichier": pathlib.Path(pt).name}
for nom, chemin in jeux:
    texte = pathlib.Path(chemin).read_text(encoding='utf-8', errors='replace')
    data = charger_bytes(chemin)
    ct = torch.tensor(list(canal_de(texte)), dtype=torch.long)
    res[nom] = ec.ppl(m, data, ct, 128, avec_canal=True)
print(json.dumps(res), flush=True)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,70p tools/eval_n2_propre.py", "description": "Read propre eval tool"}`

  ```
#!/usr/bin/env python3
"""eval_n2_propre.py — la porte honnête : PPL sur un corpus dédupliqué, et hors domaine.

Le corpus de `data/corpus_propre/` est construit par `tools/corpus_propre.py` : passages
répétés retirés, split par chunks contigus, **zéro fenêtre de validation dans
l'entraînement** (vérifié). Ce script évalue un point de contrôle :

  val / test        : in-domain, fenêtres tirées **dans** un chunk (jamais à cheval sur le
                      collage de deux chunks, qui est un artefact du split) ;
  litterature       : `data/corpus_fr_litterature.txt` (Verne, public domain) — jamais vu ;
  anglais           : `data/corpus_en.txt` (Wikipédia) — jamais vu ;
  wikitext2         : `data/wikitext2_test.txt` — jamais vu ;
  permute           : contrôle négatif, mêmes octets de validation, ordre détruit ;
  decomposition     : PPL des têtes précoces (après 2, 4, 6 blocs) et sans la boucle de
                      pensée — ce que chaque pièce porte, et ce que l'arrêt précoce coûte ;
  longueurs         : PPL à 129, 192, 256, 384, 512 octets — le verrou de longueur, mesuré
                      sur un texte propre.

Usage :
  PYTHONPATH=. ~/gpu-env/bin/python tools/eval_n2_pr
… [1529 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat work/n2j/evalue_canal.py; echo \"=== canal_structure ===\"; sed -n 1,40p tools/canal_structure.py", "description": "Read canal eval and canal tool"}`

  ```
#!/usr/bin/env python3
"""evalue_canal.py — PPL avec et sans le canal de structure, par longueur, et au mélange."""
import json, math, pathlib, random, sys
import torch, torch.nn.functional as F
sys.path.insert(0, '.')
from tools.eval_n2_propre import charge, charger_bytes, departs_vdc
from tools.canal_structure import canal as canal_de

CHUNK = 8192


def fenetres(data, canal, n, long, compteur):
    n_chunks = max(1, len(data) // CHUNK)
    xs, cs = [], []
    for k in range(n):
        c = departs_vdc(compteur + k, 1, n_chunks, long)[0]
        debut = c * CHUNK
        marge = min(CHUNK, len(data) - debut) - long - 1
        if marge <= 0:
            continue
        r = departs_vdc(compteur + 10_000_003 + k, 1, marge, long)[0]
        j = debut + r
        xs.append(data[j:j + long])
        cs.append(canal[j:j + long] if canal is not None else torch.zeros(long, dtype=torch.long))
    return torch.stack(xs).cuda(), (torch.stack(cs).cuda() if canal is not None else None)


def ppl(m, data, canal, long=128, n_lots=8, avec_canal=True):
    m.eval(); tot, n = 0.0, 0
    with torch.no_grad():
        for k in range(n_lots):
            x, c = fenetres(data, canal, 16, long + 1, k 
… [3543 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; tail -2 work/n2ac/mix-200k.log; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader; free -g | sed -n 2p", "description": "Check 200k training progress"}`

  ```
16:20:28
0, 1 MiB, 0 %
1, 1 MiB, 0 %
Mem:             125          20          89           0          16         104
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ps aux | grep -c \"[e]ntrainer_native\"; ls -la work/n2ac/; echo \"--- log ---\"; cat work/n2ac/mix-200k.log; echo \"--- dmesg oom ---\"; dmesg 2>/dev/null | tail -5", "description": "Check if training process died"}`

  ```
3
total 0
drwxr-xr-x. 1 stephane stephane  24  2 nov 16:17 .
drwxr-xr-x. 1 stephane stephane 248  2 nov 16:17 ..
-rw-r--r--. 1 stephane stephane   0  2 nov 16:17 mix-200k.log
--- log ---
--- dmesg oom ---
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"permut\" -A12 tools/eval_n2_propre.py | head -40", "description": "Read permutation control implementation"}`

  ```
13:  permute           : contrôle négatif, mêmes octets de validation, ordre détruit ;
14-  decomposition     : PPL des têtes précoces (après 2, 4, 6 blocs) et sans la boucle de
15-                      pensée — ce que chaque pièce porte, et ce que l'arrêt précoce coûte ;
16-  longueurs         : PPL à 129, 192, 256, 384, 512 octets — le verrou de longueur, mesuré
17-                      sur un texte propre.
18-
19-Usage :
20-  PYTHONPATH=. ~/gpu-env/bin/python tools/eval_n2_propre.py <point.pt> \
21-      [--longueurs] [--decomposition] [--sortie work/n2h/eval.json]
22-"""
23-from __future__ import annotations
24-
25-import argparse
--
141:         "permute": round(ppl_protocole(m, perm, 128, 16, a.chunk, 900_000, device=a.device), 4)}
142-    if a.decomposition:
143-        r["decomposition"] = decompose(m, val, a.chunk, a.device)
144-    if a.longueurs:
145-        r["longueurs"] = {str(L): round(ppl_protocole(m, val, L, 16, a.chunk, device=a.device), 4)
146-                          for L in (129, 192, 256, 384, 512)}
147-    print(json.dumps(r, ensure_ascii=False), flush=True)
148-    if a.sortie:
149-        p = pathlib.Path(a.sortie)
150-        existant = json.loads(p.read
… [150 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 118,145p tools/eval_n2_propre.py", "description": "Read main eval and permutation construction"}`

  ```
ap.add_argument("--device", default="cuda")
    a = ap.parse_args()

    corpus = RACINE / a.corpus_dir
    val = charger_bytes(corpus / "val.txt")
    test = charger_bytes(corpus / "test.txt")
    lit = charger_bytes(RACINE / "data/corpus_fr_litterature.txt")
    litt_propre = charger_bytes(RACINE / "data/corpus_litt_propre/val.txt")
    ang = charger_bytes(RACINE / "data/corpus_en.txt")
    wt = charger_bytes(RACINE / "data/wikitext2_test.txt")
    perm = val[torch.tensor(ordre_vdc(len(val)), dtype=torch.long)]

    m = charge(a.point, a.device)
    r = {"fichier": pathlib.Path(a.point).name, "params": m.nb_parametres(),
         "val": round(ppl_protocole(m, val, 128, 16, a.chunk, device=a.device), 4),
         "test": round(ppl_protocole(m, test, 128, 16, a.chunk, 5_000_000, device=a.device), 4),
         "litterature": round(ppl_protocole(m, lit, 128, 16, a.chunk, 1_000_000,
                                            device=a.device), 4),
         "litterature_propre": round(ppl_protocole(m, litt_propre, 128, 16, a.chunk, 3_000_000,
                                                   device=a.device), 4),
         "anglais": round(ppl_protocole(m, ang, 128, 16, a.chunk, 5_000_
… [465 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Écriture du banc d'évaluation du run 200k (5 PPL + longueurs + permutation)

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"eval_200k.py — les cinq PPL du run long, la courbe de longueur et le contrôle par permutation.\n\nProtocole identique à N2.ac (rapport-n2-melange) : canal fourni à l'évaluation, fenêtres\ntirées par Van der Corput dans des chunks de 8192 octets, 8 lots de 1 … [2812 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/work/n2ac/eval_200k.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; tail -3 work/n2ac/mix-200k.log; free -g | sed -n 2p; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader", "description": "Check training startup again"}`

  ```
16:20:52
Mem:             125          21          88           0          17         104
0, 1 MiB, 0 %
1, 1 MiB, 0 %
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -E '\"pas\"|\"duree_s\"|ppl_val' work/n2j/base-34m-canal.pt.json; echo \"--- 200k ---\"; date '+%H:%M:%S'; tail -2 work/n2ac/mix-200k.log; free -g|sed -n 2p", "description": "Check control run duration and 200k progress"}`

  ```
"pas": 20000,
 "ppl_val": 3.683441230210883,
 "duree_s": 1067.5820379257202
--- 200k ---
16:21:13
Mem:             125          21          88           0          17         104
  ```

### 🤖 Assistant

⏵ Implémentation du schéma de position relatif (RoPE) pour R1.1

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"rope_model.py — la variante **positions relatives** du modèle natif (R1.1/R1.2).\n\nLe modèle de `tools/native_model.py` ajoute une **position apprise absolue** (`self.pos`) et\ncompte sur les positions aléatoires à l'entraînement (N2.j2) : le gain à 512 oc … [5086 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/work/n2ac/rope_model.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/rope_model.py 2>&1 | tail -5; echo \"=== 200k ===\"; date '+%H:%M:%S'; tail -2 work/n2ac/mix-200k.log; free -g|sed -n 2p", "description": "Autotest RoPE and check training"}`

  ```
autotest rope OK : forme, pos_debut neutre, norme préservée
=== 200k ===
16:22:25
Mem:             125          33          73           0          20          92
  ```

### 🤖 Assistant

⏵ Écriture du lanceur d'entraînement RoPE (banc R1.1/R1.2)

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"entrainer_rope.py — la recette N2 avec positions **relatives** (R1.1/R1.2).\n\nIdentique à `tools/entrainer_native.py` (mêmes fenêtres Van der Corput, même mètre, même\nsupervision des têtes précoces) à trois exceptions près, toutes déclarées :\n\n  - les b … [5136 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/work/n2ac/entrainer_rope.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"eval_longueurs.py — la courbe de longueur d'un point de contrôle (absolu ou RoPE).\n\nLe mètre est celui de N2 (`work/n2j/evalue_canal.py`) : canal fourni, fenêtres Van der Corput\ndans des chunks de 8192 octets, 8 lots × 16 fenêtres. On peut demander n'imp … [1833 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/work/n2ac/eval_longueurs.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; tail -3 work/n2ac/mix-200k.log; free -g|sed -n 2p; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader", "description": "Check training startup status"}`

  ```
16:22:42
Mem:             125          34          71           0          21          91
0, 1 MiB, 0 %
1, 1 MiB, 0 %
  ```

- **bash** `{"command": "ps -eo pid,stat,etime,time,rss,cmd --no-headers | grep \"[e]ntrainer_native.py\" | cut -c1-110", "description": "Check process state and CPU time"}`

  ```
35563 S          04:46 00:00:00  2124 bash -c cd /home/stephane/GitHub/Qtrinet && mkdir -p work/n2ac && nohu
  35568 S          04:46 00:00:00  4332 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VIS
  35572 Rl         04:46 00:03:20 22636060 /home/stephane/gpu-env/bin/python tools/entrainer_native.py --corpu
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat work/n2j/base-wiki-45m.pt.json | head -30; echo \"=== canal de base-34m-canal ===\"; python3 -c \"\nimport json;d=json.load(open('work/n2j/base-34m-canal.pt.json'));print({k:d[k] for k in ('parametres','pas','corpus','octets','ppl_val','duree_s')  … [62 caractères tronqués]`

  ```
{
 "modele": "drave-n0",
 "parametres": 34301224,
 "corpus": "data/wiki_fr/propre/train.txt",
 "octets": 186089472,
 "pas": 20000,
 "seq": 128,
 "lot": 8,
 "lr": 0.0003,
 "graine": 1,
 "perte_finale": 1.4665288925170898,
 "ppl_val": 4.186314178234731,
 "jetons_val": 8192,
 "tetes": true,
 "precision_main": 0.571044921875,
 "precision_early": [
  0.51708984375,
  0.558349609375,
  0.570556640625
 ],
 "drvm": "work/n2j/base-wiki-45m.drvm",
 "sha256_drvm": "b0d5c0866b19f82e944c6e279dc16a840cda081d4e8582df58de26f2e234a37d",
 "duree_s": 1075.5144882202148
}
=== canal de base-34m-canal ===
{'parametres': 34301224, 'pas': 20000, 'corpus': 'data/wiki_fr/propre/train.txt', 'octets': 186089472, 'ppl_val': 3.683441230210883, 'duree_s': 1067.5820379257202}
  ```

### 🤖 Assistant

⏵ Lancement de R1.1 (RoPE, 20k pas, GPU 1)

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && nohup bash -c 'cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=1 PYTHONPATH=. ~/gpu-env/bin/python work/n2ac/entrainer_rope.py --corpus data/wiki_fr/propre/train.txt --canal data/wiki_fr/propre/train.canal --pas 20000 --seq  … [458 caractères tronqués]`

  ```
pid 44707
16:23:26
0, 1322 MiB, 96 %
1, 1 MiB, 0 %
  ```

- **bash** `{"command": "sleep 40; cd /home/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; echo \"--- 200k ---\"; tail -2 work/n2ac/mix-200k.log; echo \"--- rope ---\"; tail -2 work/n2ac/rope-20k.log; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader", "description": "Check both runs  … [12 caractères tronqués]`

  ```
16:24:13
--- 200k ---
pas 1000 · perte 2.4110 · PPL val 10.192 · 56 s
pas 1050 · perte 2.2704 · PPL val 10.119 · 58 s
--- rope ---
pas    300 · perte 1.3655 · PPL val 4.132 · 19 s
pas    350 · perte 1.5058 · PPL val 4.125 · 21 s
0, 1322 MiB, 96 %
1, 1304 MiB, 85 %
  ```

### 🤖 Assistant

⏵ Lecture du hook d'état et des portes tolérées

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,80p tools/verifie_etat_a_jour.py", "description": "Read state hook"}`

  ```
#!/usr/bin/env python3
"""verifie_etat_a_jour.py — aucun fait commité sans sa ligne d'état.

POURQUOI CET OUTIL EXISTE. `en-cours` est la seule source de l'état, et le contrat
disait « seul le principal écrit ». Ce n'est pas une garantie : l'identité se déduit
d'une variable d'environnement absente — un « pair » est autodéclaré — et si la
principale s'arrête, l'état se fige. Surtout, rien ne comparait les commits : la
revue ne regardait que la DATE, donc deux commits du même jour passaient. Le 29/10,
A8.0 (15 h 51) a été commité après le dernier état (15 h 34) sans aucune alerte.

La garantie est au commit, pas dans la discipline d'un écrivain :
  --index  (hook pre-commit) : un commit qui prépare un fait (reports/, roadmap,
           backlog) sans toucher `en-cours` est REFUSÉ ;
  --head   : si un fait a été commité après le dernier commit d'`en-cours`, l'état
           est en retard — la session qui le voit le corrige, sans attendre.

Le journal est du récit dérivé (le hook l'archive) : il n'exige pas de ligne d'état.

Usage :
  python3 tools/verifie_etat_a_jour.py             # --head
  python3 tools/verifie_etat_a_jour.py --index     # pour le hook
  python3 tools/verifie_eta
… [2088 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git log --oneline -3 --name-only -- reports/rapport-n2-melange.md | head -20; echo \"=== dernier commit touchant en-cours ===\"; git log -1 --format='%h %s' -- docs/pilotage/en-cours.md", "description": "Check how N2 reports were committed with state" … [1 caractères tronqués]`

  ```
2c394fbc N2.ac — LE MÉLANGE DES DEUX CORPUS : LA LARGEUR SANS PERDRE LE FRANÇAIS
reports/rapport-n2-melange.md
=== dernier commit touchant en-cours ===
04d75114 ÉTAT — HORODATAGE RÉEL (16 h 09) APRÈS LA REPRISE ; LE FUTUR N'EST PAS UNE HEURE
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat .git/hooks/pre-commit 2>/dev/null | head -60; echo \"=== core.hooksPath ===\"; git config core.hooksPath", "description": "Inspect pre-commit hook"}`

  ```
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
python3 tools/archive_sessions.py --quiet >/dev/null || { echo "  ⛔ archivage des sessions en échec"; exit 1; }
python3 tools/session_report.py --quiet >/dev/null || { echo "  ⛔ rapport de session en échec"; exit 1; }
# Le journal du jour, par thème (sources : git + journal/sessions). L'index README est
… [272 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"no-verify\\|hook\\|en-cours\" docs/methode/continuite.md | head -30", "description": "Read continuity doc on commits and hooks"}`

  ```
4:> [`en-cours`](../pilotage/en-cours.md). Ni planning ni résultats : **qui écrit l'état, quand, et avec quoi on reprend**.
6:> **Règle d'or.** Un cycle est fini quand le résultat est **mesuré, écrit, committé**, qu'`en-cours` porte sa
16:| fin de cycle | résultat + fiche + commit + `en-cours` + roadmap | jamais « le temps est écoulé » |
19:- **On ne s'arrête pas sur un compteur** : si la limite tombe avant un résultat, écrire `en-cours` +
31:**On ne délègue pas** : une édition triviale d'une ligne, l'écriture de `en-cours`/`roadmap`/`AGENTS`,
50:7. **interdits** : `en-cours`, `roadmap`, `AGENTS`, les fichiers d'un autre agent.
64:8. **diff d'état** — la ligne exacte à mettre dans `en-cours` ;
72:La session **vérifie** (porte, lien, contrôle), **met à jour `en-cours`**, **commite** et
76:## 3. La discipline de `en-cours`
78:`docs/pilotage/en-cours.md` est **la seule source de l'état**. Le journal est de l'histoire, les
87:| **écriture** | toute session écrit `en-cours`, **une à la fois** ; aucun fait (`reports/`, roadmap, backlog) ne se commite sans sa ligne (hook `pre-commit`) |
98:**Lecture** : `AGENTS.md` + `en-cours` (« Sessions en cours », « Les chantiers et leurs bloquants »,
… [856 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 25,75p docs/methode/continuite.md", "description": "Read subagent delegation rules"}`

  ```
### Quand déléguer

- **deux tâches indépendantes** : **2 à 4** en parallèle ;
- une tâche **longue et isolée** ;
- une **revue adverse** ou une **continuation** : `subagent_fork`.

**On ne délègue pas** : une édition triviale d'une ligne, l'écriture de `en-cours`/`roadmap`/`AGENTS`,
la décision humaine, ou deux agents sur le **même fichier**.

### Comment

| outil | usage |
|---|---|
| `subagent` | tâche autonome, sans contexte de la conversation |
| `subagent_fork` | revue, continuation, analyse qui s'appuie sur la conversation |
| `workflow` | **fan-out** sur beaucoup d'items indépendants (audit, migration) |

**Contrat de prompt** (obligatoire) :

1. **objectif** en une phrase, et le résultat attendu ;
2. **fichiers autorisés** — rien d'autre ;
3. **livrable** : fichier, mesure, diff, rapport ;
4. **critères d'acceptation** et **contrôle négatif** ;
5. **condition d'arrêt** (temps, essais, succès) ;
6. **format de rapport** : les **10 lignes** ci-dessous ;
7. **interdits** : `en-cours`, `roadmap`, `AGENTS`, les fichiers d'un autre agent.

**Un seul écrivain par fichier** : la session qui clôt garde l'état, la roadmap et les directives ; le sous-agent
possède son périmètre.

###
… [827 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"no-verify\" docs/ tools/ journal/2026-11-0*/README.md 2>/dev/null | head -20", "description": "Search for documented no-verify use"}`

  ```
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/commands/wheel.py:69:            "--no-verify",
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git show --stat --oneline 2c394fbc | head -20; echo \"=== 86cfb580 ===\"; git show --stat --oneline 86cfb580 | head -20", "description": "Inspect N2.ac commit contents"}`

  ```
2c394fbc N2.ac — LE MÉLANGE DES DEUX CORPUS : LA LARGEUR SANS PERDRE LE FRANÇAIS
 docs/pilotage/en-cours.md                          |  4 +-
 journal/2026-11-02/README.md                       |  9 ++-
 journal/2026-11-02/apprentissage.md                |  4 +-
 journal/2026-11-02/attention.md                    |  4 +-
 journal/2026-11-02/distribue.md                    |  4 +-
 journal/2026-11-02/docs.md                         |  8 +-
 journal/2026-11-02/memoire.md                      |  4 +-
 journal/2026-11-02/mesures.md                      |  4 +-
 journal/2026-11-02/modele.md                       |  4 +-
 journal/2026-11-02/outils.md                       |  4 +-
 journal/2026-11-02/portes.md                       |  4 +-
 journal/README.md                                  |  4 +-
 .../0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md | 48 ++++++++++++
 .../rapport.md                                     | 17 +++--
 journal/sessions/MANIFEST.md                       |  8 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 85 ++++++++++++++++++++++
 .../rapport.md                                     | 63 ++++++++++++++--
 .../fe3c05f0-834b-44f2-8739-501865d652c1/digest.md
… [1421 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && for c in $(git log --format=%h -40 -- reports/); do files=$(git show --name-only --format= $c); if echo \"$files\" | grep -q \"reports/\" && ! echo \"$files\" | grep -q \"docs/pilotage/en-cours.md\"; then echo \"$c | $(git log -1 --format=%s $c | cut  … [89 caractères tronqués]`

  ```
(no output)
  ```

### 🤖 Assistant

⏵ Question de gouvernance (en-cours) pendant que les runs tournent

- **ask_user_question** `{"questions": [{"id": "en_cours", "header": "en-cours", "question": "Le hook pre-commit refuse tout fait dans reports/ sans modifier docs/pilotage/en-cours.md — or tu m'interdis d'y toucher sans le hub (qui est actif et vient d'écrire l'état à 16 h 09). Comment veux-tu que je commite la fiche N2 ?", … [767 caractères tronqués]`

  ```
{"answers":[{"id":"en_cours","selected":["J'ajoute ma seule ligne N2 dans en-cours, puis commit via le hook (Recommandé)"]}]}
  ```

### 🤖 Assistant

⏵ Autorisation actée ; suivi des deux runs

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; echo \"--- 200k ---\"; tail -1 work/n2ac/mix-200k.log; echo \"--- rope ---\"; tail -1 work/n2ac/rope-20k.log; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader", "description": "Check both training runs"}`

  ```
16:43:56
--- 200k ---
pas 21350 · perte 1.3747 · PPL val 3.997 · 1241 s
--- rope ---
pas  19750 · perte 1.2453 · PPL val 3.517 · 1203 s
0, 1642 MiB, 99 %
1, 1422 MiB, 95 %
  ```

- **bash** `{"command": "sleep 75; cd /home/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; tail -6 work/n2ac/rope-20k.log; ls -la work/n2ac/", "description": "Wait for RoPE run completion"}`

  ```
[still running after 60000ms; moved to background job bash-65]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-65", "timeout_ms": 90000, "wait": true}`

  ```
16:45:25
 "jetons_val": 8192,
 "tetes": true,
 "drvm": "work/n2ac/rope-20k.drvm",
 "sha256_drvm": "67d81ab3fce8af14eb92b7008bd3d4a307f9e7a325e46974228fa8bbde9130f0",
 "duree_s": 1220.1019806861877
}
total 268120
drwxr-xr-x. 1 stephane stephane       268  2 nov 16:44 .
drwxr-xr-x. 1 stephane stephane       294  2 nov 16:44 ..
-rw-------. 1 stephane stephane      5149  2 nov 16:22 entrainer_rope.py
-rw-------. 1 stephane stephane      2920  2 nov 16:20 eval_200k.py
-rw-------. 1 stephane stephane      1940  2 nov 16:22 eval_longueurs.py
-rw-r--r--. 1 stephane stephane     24079  2 nov 16:45 mix-200k.log
drwxr-xr-x. 1 stephane stephane        52  2 nov 16:22 __pycache__
-rw-r--r--. 1 stephane stephane 137224476  2 nov 16:44 rope-20k.drvm
-rw-r--r--. 1 stephane stephane     22201  2 nov 16:44 rope-20k.log
-rw-r--r--. 1 stephane stephane 137247942  2 nov 16:44 rope-20k.pt
-rw-r--r--. 1 stephane stephane       524  2 nov 16:44 rope-20k.pt.json
-rw-------. 1 stephane stephane      5158  2 nov 16:21 rope_model.py
[status: completed, exit code: 0]
  ```

### 🤖 Assistant

⏵ Courbes de longueur RoPE vs positions absolues (contrôle apparié)

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat work/n2ac/rope-20k.pt.json; echo \"=== launch curves ===\"; nohup bash -c 'cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && export PYTHONPATH=. CUDA_VISIBLE_DEVICES=1; ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2ac/rope-20k.pt --r … [445 caractères tronqués]`

  ```
{
 "modele": "drave-n0-rope",
 "parametres": 34301224,
 "corpus": "data/wiki_fr/propre/train.txt",
 "octets": 186089472,
 "pas": 20000,
 "seq": 128,
 "lot": 8,
 "lr": 0.0003,
 "graine": 1,
 "window": 256,
 "positions": "rope",
 "init": "work/n2j/base-wiki-45m.pt",
 "perte_finale": 1.3000273704528809,
 "ppl_val": 3.5371263065339433,
 "jetons_val": 8192,
 "tetes": true,
 "drvm": "work/n2ac/rope-20k.drvm",
 "sha256_drvm": "67d81ab3fce8af14eb92b7008bd3d4a307f9e7a325e46974228fa8bbde9130f0",
 "duree_s": 1220.1019806861877
}
=== launch curves ===
pid 78769
[still running after 60000ms; moved to background job bash-66]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-66", "timeout_ms": 120000, "wait": true}`

  ```
L384 : 3.33
  L512 : 3.2892
  L1000 : 3.2545
{"fichier": "rope-20k.pt", "val": "data/wiki_fr/propre", "positions": "rope", "L128": 3.3696, "L192": 3.3217, "L256": 3.3217, "L384": 3.33, "L512": 3.2892, "L1000": 3.2545}
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-66 (bash: cd /home/stephane/GitHub/Qtrinet && cat work/n2ac/rope-20k.pt.json; echo "=== launch curves ==="; nohup bash -c 'cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && export PYTHONPATH=. CUDA_VISIBLE_DEVICES=1; ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2ac/rope-20k.pt --rope --longueurs 128,192,256,384,512,1000 --sortie work/n2ac/courbe-rope.json > work/n2ac/courbe-rope.log 2>&1; ~/gpu-env/bin/python work/n2ac/eval_longueurs.py work/n2j/base-34m-canal.pt --longueurs 128,192,256,384,512,1000 --sortie work/n2ac/courbe-absolu.json > work/n2ac/courbe-absolu.log 2>&1' > /dev/null 2>&1 & echo "pid $!"; sleep 60; tail -4 work/n2ac/courbe-rope.log) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Résultat R1.1 prometteur ; vérification du contrôle absolu

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; cat work/n2ac/courbe-absolu.json 2>/dev/null || tail -4 work/n2ac/courbe-absolu.log; echo \"=== 200k ===\"; tail -1 work/n2ac/mix-200k.log", "description": "Read absolute control curve"}`

  ```
16:47:00
{
 "fichier": "base-34m-canal.pt",
 "val": "data/wiki_fr/propre",
 "positions": "absolues",
 "L128": 3.5131,
 "L192": 3.4619,
 "L256": 3.4836,
 "L384": 3.5849,
 "L512": 3.6558,
 "L1000": 8.2024
}
=== 200k ===
pas 24500 · perte 1.3929 · PPL val 3.916 · 1426 s
  ```

### 🤖 Assistant

⏵ Lancement de la chaîne : R1.1 graine 2, puis R1.2 (fenêtre 512, budget constant)

- **write** `{"content": "#!/usr/bin/env bash\n# chaine_r1.sh — le reste du banc R1, sur le GPU que N2 ne prend pas (le 200 k est sur 0).\n#\n#   1. R1.1 graine 2 (contrôle de graine)            : 20 000 pas × 8 × 128, fenêtre 256\n#   2. R1.2 budget constant (mêmes octets vus)       :  5 000 pas × 8 × 512, fenê … [1350 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/work/n2ac/chaine_r1.sh</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && nohup bash work/n2ac/chaine_r1.sh > work/n2ac/chaine_r1.out 2>&1 & echo \"pid $!\"; sleep 45; date '+%H:%M:%S'; tail -2 work/n2ac/rope-20k-g2.log; tail -1 work/n2ac/mix-200k.log", "description": "Launch R1 chain in background"}`

  ```
pid 79387
16:48:08
pas 25600 · perte 1.4733 · PPL val 3.855 · 1493 s
  ```

### 🤖 Assistant

⏵ Évaluation du témoin 60 k avec le même banc (comparaison appariée)

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && nohup bash -c 'cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python work/n2ac/eval_200k.py work/n2w/mix-60k.pt --sortie work/n2ac/eval-mix60.json > work/n2ac/eval-mix60.log 2>&1' > /dev/null 2> … [154 caractères tronqués]`

  ```
pid 79670
[still running after 60000ms; moved to background job bash-69]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-69", "timeout_ms": 180000, "wait": true}`

  ```
16:49:53
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat work/n2ac/eval-mix60.json 2>/dev/null; echo \"--- log ---\"; tail -5 work/n2ac/eval-mix60.log", "description": "Read 60k reference eval results"}`

  ```
--- log ---
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ps aux | grep \"[e]val_200k\" | awk '{print $2,$3,$4}'; sleep 60; date '+%H:%M:%S'; cat work/n2ac/eval-mix60.log | tail -30", "description": "Check eval process and output"}`

  ```
79670 0.0 0.0
79672 0.0 0.0
79673 102 1.2
[still running after 60000ms; moved to background job bash-71]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-71", "timeout_ms": 90000, "wait": true}`

  ```
16:51:04
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-71 (bash: cd /home/stephane/GitHub/Qtrinet && ps aux | grep "[e]val_200k" | awk '{print $2,$3,$4}'; sleep 60; date '+%H:%M:%S'; cat work/n2ac/eval-mix60.log | tail -30) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "sleep 120; cd /home/stephane/GitHub/Qtrinet && date '+%H:%M:%S'; echo \"--- mix60 ---\"; cat work/n2ac/eval-mix60.json 2>/dev/null || tail -3 work/n2ac/eval-mix60.log; echo \"--- chaine ---\"; cat work/n2ac/chaine_r1.out; tail -1 work/n2ac/rope-20k-g2.log 2>/dev/null; echo \"--- 200k -- … [88 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-72]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-72", "timeout_ms": 120000, "wait": true}`

  ```
16:53:15
--- mix60 ---
{
 "fichier": "mix-60k.pt",
 "params": 34301224,
 "val_fr_L128": 3.4902,
 "val_fr_L256": 3.4615,
 "val_fr_L512": 3.5169,
 "val_fr_permute": 215.5638,
 "val_big_L128": 3.3565,
 "val_big_L256": 3.2716,
 "val_big_L512": 3.3685,
 "val_big_permute": 226.8678,
 "litterature": 6.0283,
 "anglais": 8.3352,
 "wikitext2": 9.0525
}
--- chaine ---
pas   4450 · perte 1.2191 · PPL val 3.843 · 294 s
--- 200k ---
pas 30850 · perte 1.3787 · PPL val 3.711 · 1799 s
[status: completed, exit code: 0]
  ```

### 🤖 Assistant

⏵ Contrôle mécaniste : quelles lignes de la table de positions ont été entraînées

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=. ~/gpu-env/bin/python - <<'PY'\nimport torch\nfor pt in (\"work/n2j/base-wiki-45m.pt\", \"work/n2j/base-34m-canal.pt\", \"work/n2ac/rope-20k.pt\"):\n    ck = torch.load(pt, map_location=\"cpu\", weights_only=False)\n    w = ck[\"state\"][\ … [438 caractères tronqués]`

  ```
work/n2j/base-wiki-45m.pt          max_pos=2048 norme moyenne par bloc de 64 positions :
    [18.1936, 17.9179, 17.8632, 17.9766, 17.9018, 17.8059, 17.9547, 18.0741, 18.3571, 18.4997, 18.3569, 18.3473, 18.4917, 18.453, 18.5365, 18.4917, 18.4963]
    moyenne 0-511 : 17.9610 · 512-1023 : 18.4417 · 1024+ : 18.4588
work/n2j/base-34m-canal.pt         max_pos=2048 norme moyenne par bloc de 64 positions :
    [16.8655, 16.5904, 16.5271, 16.6384, 16.568, 16.4932, 16.6202, 16.8005, 17.2951, 17.4294, 17.2948, 17.2858, 17.4218, 17.3854, 17.464, 17.4218, 17.4262]
    moyenne 0-511 : 16.6379 · 512-1023 : 17.3748 · 1024+ : 17.3908
work/n2ac/rope-20k.pt              max_pos=2048 norme moyenne par bloc de 64 positions :
    [18.1936, 17.9179, 17.8632, 17.9766, 17.9018, 17.8059, 17.9547, 18.0741, 18.3571, 18.4997, 18.3569, 18.3473, 18.4917, 18.453, 18.5365, 18.4917, 18.4963]
    moyenne 0-511 : 17.9610 · 512-1023 : 18.4417 · 1024+ : 18.4588
  ```

### 🤖 Assistant

⏵ Contrôle causal : table absolue avec positions 0–1279 entraînées

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && nohup bash -c 'cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=1 PYTHONPATH=. ~/gpu-env/bin/python tools/entrainer_native.py --corpus data/wiki_fr/propre/train.txt --canal data/wiki_fr/propre/train.canal --pas 20000 --seq 12 … [548 caractères tronqués]`

  ```
pid 82052
16:54:40
--- chaine ---
pas   5950 · perte 1.1231 · PPL val 3.745 · 381 s
--- absolu-1152 ---
pas   50 · perte 2.4076 · PPL val 4.774 · 6 s
--- 200k ---
pas 32450 · perte 1.4397 · PPL val 3.684 · 1886 s
  ```

