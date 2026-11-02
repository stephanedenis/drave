# Session DSH — relecture

- identifiant : `b7d4678e-2143-4daa-a9a4-a456c5aa8dab`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-02 16:16:20
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu reprends la session L/B13 `e181ce02-cd50-488a-a6be-e84b79d40dcc`. Lis son plan, AGENTS.md  et docs/pilotage/en-cours.md. Remets `- **État** : actif` et `- **Heartbeat** : <maintenant>`  dans son plan, puis vérifie `python3 tools/sessions.py --check --strict`. Le cycle 140/140  (gold 432, 116 liens) est committé. Prochaine action : gold neuronal (qualifier un modèle  local) ; DRVM/native est bloqué par l'absence de poids/tagger. Un fait = mesure + contrôle +  fiche + en-cours + commit (`git add` explicite).

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

⏵ Reprise de la session L/B13 : lecture du plan, AGENTS.md et en-cours

- **bash** `{"command": "pwd && ls", "description": "Show working directory and top-level files"}`

  ```
/home/stephane/GitHub/Qtrinet
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

- **bash** `{"command": "python3 tools/sessions.py --help 2>&1 | head -60", "description": "Inspect sessions tool usage"}`

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
  ```

- **bash** `{"command": "ls journal/sessions/ | head -30 && echo \"---\" && ls journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/", "description": "List session directories"}`

  ```
00221850-90de-4287-90ee-324a35e504cd
04ed1834-b0f8-42a1-aa21-75a75c19647e
0733c5bb-f90b-4f58-9241-3364fa32e46c
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
29ad180d-38a5-4481-a9a7-ec6ab31c895f
2c2a6595-b208-446e-bbd1-d0f49eca45e8
2f51f17f-f47c-49d5-958f-cafecd3fe01e
2fd56aa5-7b9b-40b0-9470-05c74b032d55
31f26a6e-65f5-480d-be32-36b9f425b3dd
34e1d4be-3708-4065-ae77-eca21f86e857
3d5618a0-4e3a-45bb-943d-a72c753fb7da
3de141c0-089b-4ceb-8a2e-bd6d83044a5f
---
digest.md
plan.md
rapport.md
session.v4.jsonl.zstd
  ```

- **bash** `{"command": "python3 tools/sessions.py --status 2>&1 | head -60", "description": "Show session status"}`

  ```
sessions · plans de mandat
    0733c5bb-f90b-4f58 · actif    ·  -3 min · N2 (200 000 pas sur le mélange, PPL domaine/littérature/anglais/wikitext2, courbe de longueur), R1.1/R1.2 mesurés depuis N2
      → **200 000 pas sur `data/wiki_mix/propre`** (34,3 M, canal, positions aléatoires, graine 1) puis la mesure des cinq PPL et de la courbe 128/256/512.
    0b0a6a0d-05f5-4308 · terminé  · 1902 min · N2.h — corpus propre, porte honnête, généralité, verrou de longueur
      → close — N2.i (3,13 / 12,93 / 33,83) et Pensée v0 (6/6 portes) sont committés.
    0b69f616-5c75-4c34 · terminé  · 3976 min · R0.4, R0.5, R13, R4.1–R4.3, en-cours, roadmap, backlog
      → clôture reprise par la session `22e518ee` — commit, archives, état.
    22e518ee-81b8-4081 · terminé  · 3147 min · archives de sessions, journal, en-cours, roadmap, backlog, outillage d'archivage
      → clôture committée (`eff8d8e4`) — session close ; la suite est **N2** (la hiérarchie), portée par la session à ouvrir
    536cd5d6-94ac-4057 · actif    ·   8 min · pilotage (en-cours, roadmap, chantiers, plan-travail, références), backlog, journal (hors `sessions/<id>/`), reports/README.md, reports/INDEX.md, outillage de pilotage.

… [1728 caractères tronqués]
  ```

- **read** `{"file_path": "journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md"}`
- **read** `{"file_path": "docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md</path>
<type>file</type>
<content>
1: # Plan de session — Pensée, la RSN plurielle et le moteur N3
2: 
3: > **Mandat vivant.** Ouvert le 2026-10-31 22 h 45 HAE depuis
4: > [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md). Ce plan est le **contrat de
5: > synergie** : il dit ce que la session réserve, ce qu'elle attend des autres, et quand elle s'arrête.
6: > Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.
7: 
8: - **Session** : `e181ce02-cd50-488a-a6be-e84b79d40dcc`
9: - **Rôle** : Pensée — RSN plurielle, arbre d'états, cycle multi-niveaux, moteur N3 ; analyse de la couche heuristique ; bloc linguistique
10: - **Périmètre** : Pensée, R4.4-reste, Coloration, Bloc linguistique (R0.7)
11: - **Fichiers réservés** : `docs/theorie/pensee-iterative.md`, `docs/schemas/pensee-*.svg`,
12:   `docs/implantation/moteur-de-pensee.md`, `tools/pensee/`, `reports/pensee-*`,
13:   `reports/r44-*`, `docs/theorie/pre-traitement-linguistique.md`,
14:   `docs/schemas/heuristique-*.svg`, `tools/bloc_linguistique.py`,
15:   `tools/porte-bloc-linguistique.
… [4319 caractères tronqués]
  ```


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

- **bash** `{"command": "date \"+%Y-%m-%d %H:%M %Z (%A)\" && TZ=America/Toronto date \"+%Y-%m-%d %H:%M %Z\"", "description": "Show current date and time"}`

  ```
2026-11-02 16:17 EST (lundi)
2026-11-02 16:17 EST
  ```

- **bash** `{"command": "git status --short | head -30; echo \"--- LOG ---\"; git log --oneline -8", "description": "Check git status and recent commits"}`

  ```
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
--- LOG ---
04d75114 ÉTAT — HORODATAGE RÉEL (16 h 09) APRÈS LA REPRISE ; LE FUTUR N'EST PAS UNE HEURE
97d693b6 ÉTAT — T0 REVENU SOUS 4 000 (3 998) APRÈS LE RUNBOOK
566ac478 HUB — LE RUNBOOK EST PUBLIÉ ; HEARTBEAT À JOUR, PROCHAINE ACTION LA PASSE DE PORTES
2dab14e4 PILOTAGE — L'ÉTAT REPREND : 140/140, N2.ac, DEUX SESSIONS EN PAUSE, PORTE STRICTE
86cfb580 N2 — N2.ac EST LE MODÈLE DE PRODUCTION : LE MÉLANGE 1 Go, LE CANAL ET LA PÉNALITÉ
ca06ab0b D — L'OCR CEGEP, LE GLOSSAIRE AU RENDU ET LES LIENS DE LA FAMILLE 13
702b368c B13 — LES 
… [138 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "description": "Show current diff of the session plan"}`

  ```
diff --git a/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md b/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
index c9eae9fd..d1a3f848 100644
--- a/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
+++ b/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
@@ -15,13 +15,13 @@
   `tools/porte-bloc-linguistique.sh`, `tools/tests/linguistique/`,
   `docs/implantation/bloc-linguistique.md`, `docs/schemas/bloc-linguistique-*.svg`,
   `reports/bloc-*`, `journal/sessions/e181ce02-…/`
-- **Heartbeat** : 2026-11-02 07:50 EST
+- **Heartbeat** : 2026-11-02 16:16 EST
 - **Prochaine action** : le cycle **140/140** (T137, gold 432, 116 liens) est committé par le hub ;
   reprendre par le **gold neuronal** (qualifier un modèle local) puis **DRVM/native** (bloqué) ;
   la cascade mesurée reste la lecture.
 - **Arrêt** : 2026-11-02 15 h 06 (reboot) — dernière trace 14 h 40 ; **en pause** ; reprise par
   `dsh --profile dsh-tui --resume e181ce02-cd50-488a-a6be-e84b79d40dcc` ; rafraîchir le heartbeat.
-- **État** : en pause
+- **État** : actif
 - **Plan** : 1) ~~RSN plurielle, arbre d'états, cycle multi-niveaux~~ ; 2) ~~portefeuille de
   stratégies, 
… [197 caractères tronqués]
  ```

- **bash** `{"command": "head -5 AGENTS.md; echo \"...\"; wc -l AGENTS.md docs/methode/continuite.md docs/methode/resultats.md", "description": "Peek AGENTS.md and count doc lines"}`

  ```
# Directives de l'agent — Drave

> **Compteurs vivants.** Dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; ne pas les recopier ici.

> **Porte d'entrée.** Lis ce fichier en entier (2 min) : il porte la **vision**, les règles non négociables et le
...
  102 AGENTS.md
  139 docs/methode/continuite.md
   54 docs/methode/resultats.md
  295 total
  ```

- **read** `{"file_path": "docs/methode/continuite.md"}`

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


## Tour 2

### 👤 Utilisateur

Tu reprends la session D/R/A `fe3c05f0-834b-44f2-8739-501865d652c1`. Lis son plan, AGENTS.md
 et en-cours. Remets `État : actif` et heartbeat maintenant, puis
 `sessions.py --check --strict`. Le texte intégral, le PDF, les 20 livres, les 10 notes CEGEP,
 le glossaire (355 entrées) et docwatch sont committés. Prochaine action : OCR ~127 scans CEGEP
 (`tools/ocr_pdf.py --racine CEGEP --deja <N>`), puis la clôture de la session. Un fait =
 mesure + contrôle + fiche + en-cours + commit.

### 🤖 Assistant

⏵ Bascule sur la session D/R/A : lecture du plan, d'AGENTS.md et de l'outil OCR

- **read** `{"file_path": "journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md"}`
- **read** `{"file_path": "AGENTS.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md</path>
<type>file</type>
<content>
1: # Plan de session — D/R/A : les données, le lecteur, le moteur
2: 
3: > **Mandat ouvert** le 2026-11-01 16 h 25 HNE depuis
4: > [`docs/pilotage/plan-travail.md`](../../../docs/pilotage/plan-travail.md) (§ 2, § 3) — la session
5: > reprend la session `fe3c05f0` (R4.4 close) pour le rôle **D/R/A**. Le heartbeat est celui de
6: > l'état.
7: 
8: - **Session** : `fe3c05f0-834b-44f2-8739-501865d652c1`
9: - **Rôle** : **D/R/A — les données, le lecteur, le moteur** : le texte intégral, l'extraction
10:   PDF/OCR, la préparation de R1.1/R1.2, A2.6/A8.3.
11: - **Périmètre** : D (texte intégral, PDF/OCR, licences, stubs), R1.1/R1.2 (préparation), A2.6/A8.3
12: - **Fichiers réservés** : `data/wikipedia/` (lecture), `data/corpus_wiki_*`,
13:   `tools/corpus_wikipedia*.py`, `tools/verifie_contamination.py`, `tools/catalogue_corpus.py`,
14:   `reports/corpus-wiki-*`, `reports/corpus-wikipedia-*`, `reports/inventaire-*`,
15:   `reports/rapport-corpus-*`, `reports/r11-*`, `reports/r12-*`, `reports/a26-*`, `reports/a83-*`,
16:   `journal/sessions/f
… [2252 caractères tronqués]
  ```


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

- **get_goal** `{}`

  ```
{"goal":null}
  ```

- **bash** `{"command": "grep -n \"Heartbeat\\|État\\|Arrêt\\|strict\\|perimetre\\|périmètre\" tools/sessions.py | head -60", "description": "Inspect session check logic"}`

  ```
5:périmètre, fichiers réservés, heartbeat, prochaine action, état. Les autres
6:sessions consultent `--status` avant de claim, et `--check --strict` refuse les
7:mandats incomplets, les identifiants dupliqués, les périmètres qui se recouvrent
10:Une session arrêtée (reboot, panne) passe à `État : en pause` : elle reste dans
25:CHAMPS = ("session", "rôle", "périmètre", "fichiers réservés", "heartbeat",
44:    # un champ peut tenir sur plusieurs lignes (réservations, périmètre) : on prend la ligne du
54:    for alias, cible in (("role", "rôle"), ("perimetre", "périmètre"),
60:    per = [x.strip().strip("`") for x in re.split(r"[,;]", champs.get("périmètre", "")) if x.strip()]
74:    return {"id": sid, "chemin": chemin, "champs": champs, "perimetre": per,
140:- **Heartbeat** : {heartbeat}
142:- **État** : à confirmer
150:def verifier(racine: Path, strict: bool = False) -> tuple[list[str], list[str]]:
163:            (erreurs if strict else avertissements).append(
173:            (erreurs if strict else avertissements).append(msg)
175:            commun = sorted(set(a["perimetre"]) & set(b["perimetre"]))
177:                erreurs.append(f"périmètre recouvrant : {a['id']} et {b['id']}
… [1531 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/ocr_pdf.py --help 2>&1 | head -60", "description": "Show OCR tool usage"}`

  ```
usage: ocr_pdf.py [-h] [--max-doc MAX_DOC] [--racine RACINE] [--deja DEJA]
                  [--dpi DPI] [--langues LANGUES] [--max-pages MAX_PAGES]
                  [--min-chars MIN_CHARS] [--chunk CHUNK] [--val VAL]
                  [--test TEST] [--graine GRAINE] [--sortie SORTIE]
                  [--manifeste MANIFESTE]

ocr_pdf.py — l'OCR des PDF **scannés** (R4.4 appliqué aux documents réels).
POURQUOI. `extrait_pdf.py` extrait le texte natif ; les PDF sans couche texte
(les scans) sont comptés et écartés. Ce script les **océrise** avec le
tesseract installé sans root par `installer_ocr.sh` (5.5.3, fra+eng) :
`pdftoppm` rend les pages, `tesseract` les lit. Ce qu'il ne fait pas (encore)
: le prétraitement d'image de R4.4 (`nettoyer_scan.py` : rotation, contraste,
colonnes) — le pilote mesure l'OCR **brut** ; la WER réelle n'a pas de vérité
terrain (seule la parité R4.4 sur scans simulés la donne), donc la fiche donne
le débit, les caractères et un échantillon, pas une WER inventée. Usage :
python3 tools/ocr_pdf.py --max-doc 20 # pilote (les 20 premiers scannés)
python3 tools/ocr_pdf.py # tous les scannés des racines

options:
  -h, --help            show this help message a
… [349 caractères tronqués]
  ```

- **bash** `{"command": "date \"+%Y-%m-%d %H:%M %Z\"", "description": "Current time"}`

  ```
2026-11-02 16:17 EST
  ```

- **read** `{"file_path": "reports/rapport-ocr-cegep.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ocr-cegep.md</path>
<type>file</type>
<content>
1: # Le corpus OCR du CEGEP — 10 notes scannées, 2 519 507 caractères
2: 
3: **Date** : 2026-11-02 (pilote de 05 h 52 à 11 h 25) · **Ligne** : Données · **Session** : fe3c05f0
4: **Statut** : **pilote clos** — 10 scans océrisés, manifeste `reports/ocr-pdf-cegep.json` ; le fonds CEGEP compte 2 681 PDF, la détection n'en a examiné que 41 avant la coupure `--max-doc 5`.
5: 
6: ## 1. Ce que c'est
7: 
8: Le corpus OCR des **notes de cours du CEGEP** : les PDF sans couche texte du fonds `archives/CEGEP`, océrisés page à page par `tesseract`. C'est le complément CEGEP du corpus OCR des livres (`reports/rapport-ocr-pdf.md`).
9: 
10: ## 2. Le chiffre
11: 
12: | grandeur | valeur |
13: |---|---:|
14: | scans océrisés | **10** |
15: | PDF examinés / scannés | 41 / 5 |
16: | pages | **1596** |
17: | caractères | **2 519 507** |
18: | mots estimés (car. / 6 2) | **194 944** |
19: | train / val / test | **2 464 185 o** / **86 688 o** / 0 |
20: | documents (train / val / test) | 3 / 2 / 0 |
21: | pages / scan | 2 à 366 |
22: | langues | fra+eng |
23: | tronçons 8 Ko (manifeste) | 
… [3203 caractères tronqués]
  ```

- **bash** `{"command": "wc -l tools/ocr_pdf.py && sed -n '1,120p' tools/ocr_pdf.py", "description": "Read OCR tool part 1"}`

  ```
206 tools/ocr_pdf.py
#!/usr/bin/env python3
"""ocr_pdf.py — l'OCR des PDF **scannés** (R4.4 appliqué aux documents réels).

POURQUOI. `extrait_pdf.py` extrait le texte natif ; les PDF sans couche texte (les scans) sont
comptés et écartés. Ce script les **océrise** avec le tesseract installé sans root par
`installer_ocr.sh` (5.5.3, fra+eng) : `pdftoppm` rend les pages, `tesseract` les lit.

Ce qu'il ne fait pas (encore) : le prétraitement d'image de R4.4 (`nettoyer_scan.py` : rotation,
contraste, colonnes) — le pilote mesure l'OCR **brut** ; la WER réelle n'a pas de vérité terrain
(seule la parité R4.4 sur scans simulés la donne), donc la fiche donne le débit, les caractères et
un échantillon, pas une WER inventée.

Usage :
  python3 tools/ocr_pdf.py --max-doc 20          # pilote (les 20 premiers scannés)
  python3 tools/ocr_pdf.py                       # tous les scannés des racines
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

RACINE = pathlib.Path(__file__).resolve().parent.parent
ROOT = RACINE / "work/ocr/root"
TESS = ROOT / "usr/bin/tesseract"
E
… [3811 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '120,206p' tools/ocr_pdf.py", "description": "Read OCR tool part 2"}`

  ```
fichiers = {n: (args.sortie / f"{n}.txt").open("w", encoding="utf-8") for n in ("train", "val", "test")}
    vus, vus_troncons = set(), set()
    stats = {"pdfs": 0, "scannes": 0, "ocrises": 0, "pages_ocr": 0, "caracteres": 0,
             "troncons": 0, "documents": {"train": 0, "val": 0, "test": 0},
             "octets": {"train": 0, "val": 0, "test": 0}, "temps_s": 0,
             "echantillon": "", "racines": []}
    t0 = time.time()
    for lib, racine, lic in RACINES:
        if args.racine and lib != args.racine:
            continue
        if not racine.exists():
            continue
        pdfs = sorted(racine.rglob("*.pdf"))
        stats["racines"].append({"nom": lib, "chemin": racine.as_posix(), "pdfs": len(pdfs), "licence": lic})
        for pdf in pdfs:
            if args.max_doc and stats["ocrises"] >= args.max_doc:
                break
            npages = pages(pdf)
            if not npages:
                continue
            stats["pdfs"] += 1
            if args.deja and stats["pdfs"] <= args.deja:
                continue
            t = natif(pdf)
            if len(t.strip()) / max(npages, 1) >= 50:
                continue  # il a du texte natif : déj
… [3032 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"127\" reports/*.md docs/pilotage/*.md docs/methode/*.md 2>/dev/null | grep -i \"scan\\|cegep\\|pdf\" | head -20; echo \"--- corpus OCR dirs ---\"; ls -ld data/corpus_ocr* 2>/dev/null; echo \"--- manifests ---\"; ls -l reports/ocr-pdf* 2>/dev/null", "description": "Find the 12 … [34 caractères tronqués]`

  ```
docs/pilotage/en-cours.md:64:- **Prochaine action** : **OCR ~127 scans CEGEP** ; clôture ; R1.1/R1.2 après N2, A2.6 après A6.2.
docs/pilotage/plan-travail.md:41:| **D/R/A — en pause** | les corpus (texte intégral, PDF/OCR, licences, stubs), la préparation de R1.1/R1.2, A2.6/A8.3 | D, R1, A2.6/A8.3 | **CPU/IO**, 4–16 cœurs | 10 corpus, PDF, OCR 20 livres + 10 notes CEGEP, glossaire 355 entrées : **fait et committé**. Reprise : `fe3c05f0` (`--resume`), OCR ~127 scans, clôture. |
docs/pilotage/plan-travail.md:197:   rafraîchir le heartbeat (01/11 22:50 → maintenant). Prochaine action : **OCR ~127 scans CEGEP**
docs/pilotage/roadmap.md:36:| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67,73 G car., 81,2 Go, **8 Ko 0**) ; **PDF** (1 927 doc., 322 Mo) ; **documents** (3 384 doc., 872 M car., 8 Ko 2,07 %) ; **OCR** (20 livres, 7 381 p, 15,36 M, 8 Ko 0 ; [CEGEP](../theorie/glossaire/entrees/cegep.md) 10 notes, 1 596 p, 2,52 M car., 8 Ko 0) ; **genres** mesurés | **l'OCR complet** (le [fonds](../theorie/glossaire/entrees/fonds.md) CEGEP : ~12
… [592 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -6 -- tools/ocr_pdf.py; echo \"---\"; git status --short | grep -i \"ocr\\|cegep\\|corpus\" | head -20", "description": "History of OCR tool and pending OCR files"}`

  ```
ca06ab0b D — L'OCR CEGEP, LE GLOSSAIRE AU RENDU ET LES LIENS DE LA FAMILLE 13
56b22212 B13 — LES 19 RÉPONSES DE RÉFÉRENCE : COUVERTURE 19/19, LE JUGE EST UTILISABLE ; 127/127
a041333c DONNÉES — LE RUN DE REPRISE A ÉCRASÉ LE CORPUS CEGEP : LES 2 ALGORITHMS RESTENT, LES 10 NOTES SONT À RE-OCÉRISER (LEÇON : SORTIE SÉPARÉE)
e850644f B13 — LA RÉPONSE : 19/19, L'ACTE COMMANDE LA SORTIE ; 123/123
4f7631aa DONNÉES — LE CEGEP PASSE À 10 NOTES (2,52 M CAR.) ; LE 11E PDF (ENCYCLOPEDIA) DÉPASSE LE TIMEOUT PDFTOPPM, L'OUTIL LE RATTRAPE
6424bf7f B13 — LA SÉMANTIQUE DES VERBES : 23/30, LE DERNIER NOM RESTE LE MEILLEUR ; 102/102
---
  ```

- **bash** `{"command": "cat reports/ocr-pdf-cegep.json", "description": "Read CEGEP OCR manifest"}`

  ```
{
 "date": "2026-11-01",
 "ligne": "Données (R4.4 appliqué)",
 "nature": "corpus OCR des PDF scannés",
 "dispositif": {
  "ocr": "tesseract 5.5.3 sans root (work/ocr/root)",
  "langues": "fra+eng",
  "dpi": 300,
  "psm": 3,
  "pretraitement": "aucun (le R4.4 le fera)",
  "split": "hash salé du chemin : 5% val, 5% test",
  "deduplication": "documents + tronçons"
 },
 "pdfs": 52,
 "scannes": 10,
 "ocrises": 10,
 "pages_ocr": 1596,
 "caracteres": 2519507,
 "troncons": 312,
 "documents": {
  "train": 8,
  "val": 2,
  "test": 0
 },
 "octets": {
  "train": 2464185,
  "val": 86688,
  "test": 0
 },
 "temps_s": 5308.7,
 "echantillon": "---\nExercices de synthèse Excel 2010 Fonctions avancées\nExercices de synthèse\n\nExcel 2010\nFonctions avancées\n\nEditions Logitell inc.\n\n\nL'éditeur donne l’autorisation de reproduire des parties ou la totalité de ce document, uniquement si\nces copies sont utilisées avec les manuels de formation publiés par Les éditions Logitell inc. Le\nnombre maximum de copies ne peut dépasser le nombre de manuels de formation en usage à ce\nmoment-là.\n\nGarantie. Les éditions Logitell s’engage à remplacer tout CD-ROM fo\n---\nAMF-AO-Annexes 12 à 15 (Tech)\nAutorité
… [1172 caractères tronqués]
  ```

- **bash** `{"command": "ls -l data/corpus_ocr_cegep/ data/corpus_ocr/; echo \"--- sizes ---\"; du -sh data/corpus_ocr* 2>/dev/null; echo \"--- cegp pdf count ---\"; find /home/stephane/Data13TB/stephane/archives/CEGEP -iname '*.pdf' | wc -l", "description": "Inspect OCR corpora and CEGEP PDF count"}`

  ```
data/corpus_ocr/:
total 15172
-rw-r--r--. 1 stephane stephane        0  1 nov 20:45 test.txt
-rw-r--r--. 1 stephane stephane 14596847  2 nov 04:44 train.txt
-rw-r--r--. 1 stephane stephane   934044  2 nov 05:07 val.txt

data/corpus_ocr_cegep/:
total 2496
-rw-r--r--. 1 stephane stephane       0  2 nov 12:09 test.txt
-rw-r--r--. 1 stephane stephane 2464185  2 nov 13:37 train.txt
-rw-r--r--. 1 stephane stephane   86688  2 nov 13:37 val.txt
--- sizes ---
15M	data/corpus_ocr
2,5M	data/corpus_ocr_cegep
--- cegp pdf count ---
2711
  ```

- **bash** `{"command": "grep -rln \"scann\" reports/*.json | head; echo \"---\"; grep -rn \"127\\|scann\" reports/rapport-ocr-pdf.md reports/rapport-ocr-cegep.md 2>/dev/null | head -20", "description": "Locate scan census sources"}`

  ```
reports/corpus-pdf-documents.json
reports/corpus-pdf.json
reports/inventaire-donnees-entrainement.json
reports/ocr-pdf-cegep.json
reports/ocr-pdf.json
reports/r03-banc-extractif.json
reports/r03-banc-modele.json
reports/r07-routeur.json
reports/traduction-24langues-3b-A.json
reports/traduction-24langues-A.json
---
reports/rapport-ocr-pdf.md:1:# Le corpus OCR — les livres scannés, 20 livres, 15,4 M caractères
reports/rapport-ocr-pdf.md:8:Le corpus des **livres scannés** : les PDF sans couche texte, océrisés page à page par `tesseract`. C'est le complément des documents natifs : là où `pdftotext` ne trouve rien, l'OCR lit l'image.
reports/rapport-ocr-pdf.md:15:| PDF examinés / scannés | 22 / 22 |
reports/rapport-ocr-pdf.md:48:Les **159 PDF scannés** du corpus PDF (le run `--max-doc 20` est un pilote) ; le pipeline R4.4 (nettoyage + WER) ; la fiche finale.
reports/rapport-ocr-cegep.md:1:# Le corpus OCR du CEGEP — 10 notes scannées, 2 519 507 caractères
reports/rapport-ocr-cegep.md:15:| PDF examinés / scannés | 41 / 5 |
  ```

- **bash** `{"command": "grep -rn \"127\" reports/*.json 2>/dev/null | head; echo \"--- docs ---\"; grep -rn \"127 scans\\|~127\" docs journal reports --include='*.md' 2>/dev/null | head -20", "description": "Search 127 mentions across docs"}`

  ```
reports/bloc-linguistique.json:210:    "etiquettes": 127
reports/carte-24langues-3b.json:397: "correlation_chrf_plancher": 0.5775106095127498
reports/cerveau-mesures-corrigees.json:1355:    "surface_prefixe": 0.037914691943127965
reports/cerveau-mesures-corrigees.json:2486:     "ecart_type": 0.18379037514052127,
reports/cerveau-mesures-corrigees.json:2496:     "ecart_type": 0.10201731270722063,
reports/cerveau-mesures-corrigees.json:3473:       -0.12717713197217795,
reports/cerveau-mesures-corrigees.json:4073:      "ecart_type": 0.12750752524013434,
reports/cerveau-mesures-corrigees.json:4209:      "moyenne": 0.21257861635220127,
reports/cerveau-mesures-corrigees.json:4567:       "ecart_type": 0.12894177412740665,
reports/cerveau-mesures-corrigees.json:4572:        0.20047366671274575
--- docs ---
docs/pilotage/roadmap.md:36:| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67,73 G car., 81,2 Go, **8 Ko 0**) ; **PDF** (1 927 doc., 322 Mo) ; **documents** (3 384 doc., 872 M car., 8 Ko 2,07 %) ; **OCR** (20 livres, 7 381 p, 15,36 M, 8 Ko 
… [3482 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '9180,9220p' journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/rapport.md", "description": "Read session report around next steps"}`

  ```
**Synthèse produite :**

La fenêtre de 3 h est close (12 h 20) ; le goal est marqué **complete**.

\## Ce qui a été fait et mesuré

**Le corpus OCR du CEGEP est passé de 7 à 10 notes** : *Algorithms Illuminated (Part 4)* 274 p, *Part 1* 217 p et *Data Structures and Algorithms in C* 366 p se sont ajoutés. Total mesuré : **10 notes, 1 596 pages, 2 519 507 caractères**, train 2,46 Mo, val 87 ko, **8 Ko : 302 fenêtres train + 11 val, 0 doublon**, recouvrement éval **0/40, 0/24, 0/40** (commit `4f7631aa`).

**Le lot de 40 s'est arrêté sur un mur** : le 11e PDF, l'*Encyclopedia of Algorithms* (plus de 1 000 pages), a fait dépasser à `pdftoppm` son timeout de 1 800 s ; l'exception `subprocess.TimeoutExpired` n'était pas rattrapée et le run est tombé. C'est une limite de l'outil, nommée dans la fiche.

**Deux corrections d'outil** : `tools/ocr_pdf.py` attrape désormais le timeout (il journalise et passe au PDF suivant) ; il gagne aussi `--deja N` pour reprendre un parcours après N PDF examinés.

**Une erreur que j'ai faite et documentée** : le run de reprise (`--deja 41`) a réécrit `data/corpus_ocr_cegep/` en mode `w` et n'a laissé que les deux *Algorithms* re-océrisés — **les 10 notes me
… [1930 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib\nfor p in (\"reports/corpus-pdf.json\",\"reports/corpus-pdf-documents.json\",\"reports/inventaire-donnees-entrainement.json\"):\n    f=pathlib.Path(p)\n    if not f.exists(): continue\n    d=json.loads(f.read_text(encoding=\"utf-8\"))\n    print(\" … [249 caractères tronqués]`

  ```
== reports/corpus-pdf.json ['date', 'ligne', 'nature', 'methode', 'racines', 'pdfs', 'pages', 'documents_gardes', 'documents_scannes', 'documents_courts', 'documents_doublons', 'caracteres_gardes', 'troncons', 'troncons_doublons', 'octets', 'documents', 'echantillon', 'mots_estimes', 'note_mots', 'sha256_train']
scann 3
cegep 3
CEGEP 3
sans_texte 0
pages 1
== reports/corpus-pdf-documents.json ['date', 'ligne', 'nature', 'methode', 'racines', 'pdfs', 'pages', 'documents_gardes', 'documents_scannes', 'documents_courts', 'documents_doublons', 'caracteres_gardes', 'troncons', 'troncons_doublons', 'octets', 'documents', 'echantillon', 'mots_estimes', 'note_mots', 'sha256_train']
scann 3
cegep 0
CEGEP 0
sans_texte 0
pages 1
== reports/inventaire-donnees-entrainement.json ['date', 'ligne', 'methode', 'volumes', 'sources', 'totaux', 'recommandations', 'limites']
scann 2
cegep 3
CEGEP 3
sans_texte 0
pages 0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/corpus-pdf.json'))\nprint({k:d[k] for k in ('pdfs','pages','documents_gardes','documents_scannes','documents_courts','documents_doublons','caracteres_gardes')})\nprint(json.dumps(d['racines'],ensure_ascii=False,indent=1))\nPY", "d … [52 caractères tronqués]`

  ```
{'pdfs': 2785, 'pages': 222570, 'documents_gardes': 1927, 'documents_scannes': 159, 'documents_courts': 83, 'documents_doublons': 616, 'caracteres_gardes': 314351704}
[
 {
  "nom": "Biblio_large",
  "chemin": "/home/stephane/Data13TB/stephane/Biblio_large",
  "pdfs": 104
 },
 {
  "nom": "CEGEP",
  "chemin": "/home/stephane/Data13TB/stephane/archives/CEGEP",
  "pdfs": 2681
 }
]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/inventaire-donnees-entrainement.json'))\nfor s in d.get('sources',[]):\n    if 'CEGEP' in json.dumps(s):\n        print(json.dumps(s,ensure_ascii=False,indent=1)[:2000])\nPY", "description": "Show CEGEP inventory source"}`

  ```
{
 "chemin": "archives/CEGEP/",
 "taille": "11 Go",
 "octets": null,
 "fichiers": null,
 "format": "pdf/xlsx/docx/pptx/epub",
 "contenu": "cours de cégep : 2 711 PDF, 3 774 xlsx, 454 docx, 362 pptx, 109 epub",
 "role": "documents",
 "etat": "a_extraire",
 "note": "droits pédagogiques à vérifier ; extraction PDF puis OCR R4.4 si scanné"
}
  ```

- **bash** `{"command": "grep -n \"12[0-9] scans\\|12[0-9] PDF\\|scannés\" journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/rapport.md | tail -20", "description": "Find scan count derivation in report"}`

  ```
2476:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours.
2494:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours.
2512:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours, sans nouveau livre depuis plusieurs rounds.
2530:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours, sans nouveau livre.
2549:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours, sans nouveau livre.
2568:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours, sans nouveau livre.
2589:**L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours ; c'est le poste le plus lent.
2609:**L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours ; c'est le poste le plus lent.
2628:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours, sans nouveau livre.
2647:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détection des scannés toujours en cours.
2666:- **L'OCR** : quatre livres océrisés (2,5 Mo), la détec
… [1781 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"documents_scannes\" tools/*.py | head; echo \"---\"; grep -rn \"127\" journal/2026-11-02/*.md 2>/dev/null | head", "description": "Find scan-count code and day journal mentions"}`

  ```
tools/extrait_pdf.py:98:             "documents_scannes": 0, "documents_courts": 0, "documents_doublons": 0,
tools/extrait_pdf.py:118:                stats["documents_scannes"] += 1
tools/extrait_pdf.py:181:                                             "documents_scannes", "caracteres_gardes",
---
journal/2026-11-02/mesures.md:81:| 12:15 | `56b22212` | B13 — LES 19 RÉPONSES DE RÉFÉRENCE : COUVERTURE 19/19, LE JUGE EST UTILISABLE ; 127/127 | `moteur-de-pensee.md`, `en-cours.md`, `README.md` (+29) |
journal/2026-11-02/README.md:170:| 12:15 | `56b22212` | B13 — LES 19 RÉPONSES DE RÉFÉRENCE : COUVERTURE 19/19, LE JUGE EST UTILISABLE ; 127/127 |
  ```

- **read** `{"file_path": "tools/sessions.py", "offset": 120, "limit": 90}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/sessions.py</path>
<type>file</type>
<content>
120:     """Crée un plan *à confirmer* à partir de la section `en-cours`, sans l'inventer."""
121:     n = 0
122:     for s in sections_en_cours(racine):
123:         chemin = racine / SESSIONS / s["id"] / "plan.md"
124:         if chemin.exists():
125:             continue
126:         chemin.parent.mkdir(parents=True, exist_ok=True)
127:         heartbeat = s["heartbeat"] or datetime.now().strftime("%Y-%m-%d %H:%M HAE")
128:         role = s["role"] or "à confirmer"
129:         fichiers = s["fichiers"] or "à confirmer"
130:         prochaine = s["prochaine"] or "à confirmer"
131:         chemin.write_text(f"""# Plan de session — {s['id']}
132: 
133: > **Repris de `en-cours` le {datetime.now().strftime('%Y-%m-%d %H:%M')}** — plan *à confirmer* par la
134: > session : le heartbeat est celui de l'état, pas une preuve de vie.
135: 
136: - **Session** : `{s['id']}`
137: - **Rôle** : {role}
138: - **Périmètre** : à confirmer
139: - **Fichiers réservés** : {fichiers}
140: - **Heartbeat** : {heartbeat}
141: - **Prochaine action** : {prochaine}
142: - **État** : à confirmer
143: """
… [3700 caractères tronqués]
  ```

- **edit** `{"file_path": "journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md", "old_string": "- **Heartbeat** : 2026-11-01 22:50\n- **État** : en pause", "new_string": "- **Heartbeat** : 2026-11-02 16:21 EST\n- **État** : actif"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md has been updated successfully.
  ```

- **edit** `{"file_path": "journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md", "new_string": "- **Arrêt** : 2026-11-02 15 h 06 (reboot) — dernière trace 13 h 25 ; **reprise** le 02/11 à 16 h 21 ;\n  heartbeat rafraîchi.", "old_string": "- **Arrêt** : 2026-11-02 15 h 06 (reboot) — dernière trace 13 h … [134 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/sessions.py --check --strict; echo \"[exit $?]\"", "description": "Run strict session check"}`

  ```
⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/structures/ (29ad180d-38a5-4481-a9a7-ec6ab31c895f)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/wikipedia/` (lecture) (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/corpus_wiki_* (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : tools/corpus* (0733c5bb-f90b-4f58-9241-3364fa32e46c) / tools/corpus_wikipedia*.py (fe3c05f0-834b-44f2-8739-501865d652c1)
  ❌ /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md : heartbeat illisible
  ❌ plan actif non listé dans en-cours : 0733c5bb-f90b-4f58-9241-3364fa32e46c
  ❌ plan actif non listé dans en-cours : 29ad180d-38a5-4481-a9a7-ec6ab31c895f
[exit 1]
  ```

- **bash** `{"command": "ls -l --time-style=+%H:%M:%S journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md 2>&1; echo \"--- 29ad ---\"; cat journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md 2>&1 | head -30; echo \"--- 0733 ---\"; … [123 caractères tronqués]`

  ```
-rw-------. 1 stephane stephane 2327 16:16:12 journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md
-rw-------. 1 stephane stephane 4109 16:19:32 journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md
--- 29ad ---
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
  `reports/s-banque-*` ; `j
… [2498 caractères tronqués]
  ```

- **read** `{"file_path": "tools/sessions.py", "limit": 55, "offset": 20}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/sessions.py</path>
<type>file</type>
<content>
20: from pathlib import Path
21: 
22: RACINE = Path(__file__).resolve().parents[1]
23: SESSIONS = "journal/sessions"
24: ETAT = "docs/pilotage/en-cours.md"
25: CHAMPS = ("session", "rôle", "périmètre", "fichiers réservés", "heartbeat",
26:           "prochaine action", "état")
27: ACTIFS = {"actif", "active", "en cours", "bloqué", "bloquee", "bloqué(e)"}
28: PAUSE = {"en pause", "pause", "suspendu", "suspendue"}
29: A_CONFIRMER = {"à confirmer", "a confirmer"}
30: ETATS_CONNUS = ACTIFS | PAUSE | {"terminé", "termine", "libre", "libre."} | A_CONFIRMER
31: PEREMPTION_MIN = 45
32: 
33: 
34: def _cle(s: str) -> str:
35:     return re.sub(r"\s+", " ", s.strip().lower())
36: 
37: 
38: def _valeur(s: str) -> str:
39:     return s.strip().strip("`").strip()
40: 
41: 
42: def lire_plan(chemin: Path) -> dict:
43:     champs: dict[str, str] = {}
44:     # un champ peut tenir sur plusieurs lignes (réservations, périmètre) : on prend la ligne du
45:     # champ ET ses continuations jusqu'au prochain « - **champ** ». Sans cela, la moitié des
46:     # fichiers réservés n'était pas vérifiée 
… [1698 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport sessions, pathlib\nfor sid in ('29ad180d-38a5-4481-a9a7-ec6ab31c895f','0733c5bb-f90b-4f58-9241-3364fa32e46c','fe3c05f0-834b-44f2-8739-501865d652c1'):\n    p=sessions.lire_plan(pathlib.Path('journal/sessions')/sid/'plan.md' … [122 caractères tronqués]`

  ```
29ad180d-38a5-4481-a9a7-ec6ab31c895f '2026-11-02 16:19 EST' 0.7489906833333334 actif
0733c5bb-f90b-4f58-9241-3364fa32e46c '2026-11-02 16:20 HAE' -0.25100486666666666 actif
fe3c05f0-834b-44f2-8739-501865d652c1 '2026-11-02 16:21 EST' -1.2510011 actif
  ```

- **bash** `{"command": "python3 tools/sessions.py --check --strict; echo \"[exit $?]\"; echo \"--- mtimes ---\"; ls -l --time-style=+%H:%M:%S docs/pilotage/en-cours.md journal/sessions/*/plan.md | tail -8", "description": "Re-run strict check and show file mtimes"}`

  ```
⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/structures/ (29ad180d-38a5-4481-a9a7-ec6ab31c895f)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/wikipedia/` (lecture) (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : data/ (0733c5bb-f90b-4f58-9241-3364fa32e46c) / data/corpus_wiki_* (fe3c05f0-834b-44f2-8739-501865d652c1)
  ⚠ fichiers proches : tools/corpus* (0733c5bb-f90b-4f58-9241-3364fa32e46c) / tools/corpus_wikipedia*.py (fe3c05f0-834b-44f2-8739-501865d652c1)
  ❌ plan actif non listé dans en-cours : 0733c5bb-f90b-4f58-9241-3364fa32e46c
  ❌ plan actif non listé dans en-cours : 29ad180d-38a5-4481-a9a7-ec6ab31c895f
[exit 1]
--- mtimes ---
-rw-------. 1 stephane stephane  2335 16:09:28 journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md
-rw-r--r--. 1 stephane stephane   925 11:21:16 journal/sessions/71d57f53-8b41-4220-84dd-7bb9eedc88d9/plan.md
-rw-r--r--. 1 stephane stephane   626 11:21:10 journal/sessions/8156fdcb-5033-4ba4-a5f3-f8a078e6e57e/plan.md
-rw-r--r--. 1 stephane stephane   651 11:21:10 journal/sessions/c3d0f0bd-e344-4600-a023-0ed50d25b48b/plan.md
-rw-------. 1 stephane stephane  5209 16:16:27 journ
… [324 caractères tronqués]
  ```

- **bash** `{"command": "ps -eo pid,etime,pcpu,pmem,comm,args --sort=-pcpu | grep -E \"ocr_pdf|tesseract|pdftoppm|python3 tools\" | grep -v grep | head -10; echo \"--- cpu/mem ---\"; nproc; free -h | head -2; df -h . | tail -1", "description": "Check running OCR jobs and resources"}`

  ```
--- cpu/mem ---
40
               total        used        free      shared  buff/cache   available
Mem:           125Gi        28Gi        82Gi       301Mi        16Gi        97Gi
/dev/mapper/system-root   11T  9,0T  2,0T  83% /home/stephane/Data13TB
  ```

- **bash** `{"command": "git status --short | head -25; echo \"---\"; git log --oneline -3", "description": "Check working tree before OCR work"}`

  ```
M journal/README.md
 M journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md
?? journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md
---
dc7f9c56 N2 — MANDAT 200 k PAS SUR LE MÉLANGE 1 Go, PUIS R1.1/R1.2 (session 0733c5bb)
04d75114 ÉTAT — HORODATAGE RÉEL (16 h 09) APRÈS LA REPRISE ; LE FUTUR N'EST PAS UNE HEURE
97d693b6 ÉTAT — T0 REVENU SOUS 4 000 (3 998) APRÈS LE RUNBOOK
  ```

- **bash** `{"command": "git show --stat --oneline dc7f9c56 | head -15; echo \"---\"; git show --stat --oneline 04d75114 | head -10; echo \"--- en-cours N2 session? ---\"; grep -n \"0733c5bb\\|29ad180d\" docs/pilotage/en-cours.md || echo \"absent\"", "description": "Inspect concurrent hub commits"}`

  ```
dc7f9c56 N2 — MANDAT 200 k PAS SUR LE MÉLANGE 1 Go, PUIS R1.1/R1.2 (session 0733c5bb)
 journal/2026-11-02/README.md                       |   12 +-
 journal/2026-11-02/apprentissage.md                |    7 +-
 journal/2026-11-02/attention.md                    |    7 +-
 journal/2026-11-02/distribue.md                    |    7 +-
 journal/2026-11-02/docs.md                         |   10 +-
 journal/2026-11-02/memoire.md                      |    7 +-
 journal/2026-11-02/mesures.md                      |    7 +-
 journal/2026-11-02/modele.md                       |    7 +-
 journal/2026-11-02/outils.md                       |    7 +-
 journal/2026-11-02/portes.md                       |    7 +-
 journal/README.md                                  |    7 +-
 .../0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md | 1275 ++++++++++++++++++++
 .../0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md   |   32 +
 .../rapport.md                                     |  Bin 0 -> 9084 bytes
---
04d75114 ÉTAT — HORODATAGE RÉEL (16 h 09) APRÈS LA REPRISE ; LE FUTUR N'EST PAS UNE HEURE
 docs/pilotage/chantiers.md                         |   2 +-
 docs/pilotage/en-cours.md                          |   2 +-

… [481 caractères tronqués]
  ```

- **create_goal** `{"objective": "Session D/R/A (fe3c05f0) : OCR du fonds CEGEP restant (~127 scans) en sortie séparée, fusion et contrôle du corpus (10 notes + suite), fiche + JSON, en-cours + commit explicite, puis clôture de la session.", "max_goal_rounds": 1000}`

> **Objectif** (create) : Session D/R/A (fe3c05f0) : OCR du fonds CEGEP restant (~127 scans) en sortie séparée, fusion et contrôle du corpus (10 notes + suite), fiche + JSON, en-cours + commit explicite, puis clôture de la session.


  ```
{"goal":{"id":"goal-3245c476-82de-4e45-8c82-e9d23035ed61","revision":1,"objective":"Session D/R/A (fe3c05f0) : OCR du fonds CEGEP restant (~127 scans) en sortie séparée, fusion et contrôle du corpus (10 notes + suite), fiche + JSON, en-cours + commit explicite, puis clôture de la session.","phase":"active","roundsStarted":0,"maxGoalRounds":1000},"activation":"armed"}
  ```

- **bash** `{"command": "ls work/ocr/ 2>/dev/null | head; git check-ignore -v work/ocr/census.py 2>/dev/null || echo \"not ignored?\"", "description": "Check work dir and gitignore"}`

  ```
pages
root
rpm
.gitignore:23:work/	work/ocr/census.py
  ```

- **write** `{"file_path": "work/ocr/census_cegep.py", "content": "#!/usr/bin/env python3\n\"\"\"Recensement du fonds CEGEP avec la logique exacte de tools/ocr_pdf.py.\n\nPour chaque PDF (ordre `sorted(rglob(\"*.pdf\"))`), mesure `pdfinfo` puis le texte natif des deux\npremières pages. Un PDF est « scanné » si l … [3210 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/ocr/census_cegep.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 work/ocr/census_cegep.py", "description": "Census CEGEP PDFs and scans", "run_in_background": true}`

  ```
started background job bash-34
  ```

- **read** `{"file_path": "docs/methode/resultats.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/resultats.md</path>
<type>file</type>
<content>
1: # Ce qu'un résultat doit porter
2: 
3: > Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant d'écrire une fiche**, un JSON de
4: > résultats, ou un message de commit.
5: 
6: ## Les cinq pièces d'un résultat
7: 
8: 1. **Le chiffre** — la valeur, avec son [unité](../theorie/glossaire/entrees/unite.md) et son arrondi utile (jamais plus de chiffres que l'instrument n'en
9:    [porte](../theorie/glossaire/entrees/porte.md)) ;
10: 2. **La mesure qui le produit** — le calcul exact, la métrique ([chrF](../theorie/glossaire/entrees/chrf.md), précision, rappel, [AUC](../theorie/glossaire/entrees/auc.md)…), et ce qu'elle ne
11:    mesure pas ;
12: 3. **Le dispositif** — quel [corpus](../theorie/glossaire/entrees/corpus.md) (et sa provenance), quel modèle (taille, [quantification](../theorie/glossaire/entrees/quantification.md), date de coupure),
13:    quelles **couches de neurones** sondées, quel découpage, **quelle unité de mesure** (unité de sens ou unité
14:    grammaticale ; si c'est un [jeton](../theorie/glossaire/entrees/jeton.md), le dire co
… [2865 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/ | grep -i \"ocr\\|contamination\\|porte\" | head -20; echo \"---\"; grep -rn \"ocr\" tools/porte-*.sh 2>/dev/null | head", "description": "Find OCR gates and contamination tool"}`

  ```
exporter_gguf_dense.py
exporter_gguf.py
graphe_document_ocr.py
importer_udhr.py
installer_ocr.sh
mesurer_ocr.py
ocr_pdf.py
porte-adaptateur-sortie.sh
porte-audit-drapeaux.sh
porte-b1110-hybride.sh
porte-balayage.sh
porte-bloc-code.sh
porte-bloc-linguistique.sh
porte-bloc-maths.sh
porte-bloc-tableaux.sh
porte-budget.sh
porte-bus.sh
porte-bus-socket.sh
porte-c4-retard.sh
porte-cerveau.sh
---
tools/porte-ocr-scans.sh:2:# porte-ocr-scans.sh — R4.4 : les scans (5 familles), les colonnes, les tableaux.
tools/porte-ocr-scans.sh:13:# Usage : tools/porte-ocr-scans.sh
tools/porte-ocr-scans.sh:17:if ! bash tools/installer_ocr.sh --verifie; then
tools/porte-ocr-scans.sh:18:    echo "  ❌ OCR absent de la machine : tools/installer_ocr.sh (environnementale)"
tools/porte-ocr.sh:2:# porte-ocr.sh — R4.4 : l'OCR lit, il dit son score, et ses contrôles négatifs échouent.
tools/porte-ocr.sh:14:# Usage : tools/porte-ocr.sh
tools/porte-ocr.sh:18:if ! bash tools/installer_ocr.sh --verifie; then
tools/porte-ocr.sh:19:    echo "  ❌ OCR absent de la machine : tools/installer_ocr.sh (environnementale)"
tools/porte-ocr.sh:22:python3 tools/mesurer_ocr.py --porte --sans-ecrire
  ```

- **job_output** `{"job_id": "bash-34"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "grep -n \"OCR\\|CEGEP\" journal/2026-11-02/README.md | head -20; echo \"--- mesures ---\"; grep -n \"ocr\\|OCR\" journal/2026-11-02/mesures.md | head -10", "description": "Find prior journal entries for OCR"}`

  ```
52:| 00:20 | `47089fd7` | ÉTAT — OCR 8 LIVRES, PROCHAINE ACTION : L'OCR COMPLET ET LA CLÔTURE |
55:| 00:26 | `9b4f0208` | PLAN — LA LIGNE D/R/A PORTE SES LIVRAISONS : DIX CORPUS FAITS, PDF/OCR, PRÉPA R1 |
58:| 00:34 | `93be0a1d` | CHANTIERS — LA LIGNE D PORTE LES DIX CORPUS, LE PDF, LES DOCUMENTS ET L'OCR |
75:| 01:28 | `6eff8d8d` | DONNÉES — L'OCR DES 8 LIVRES EST FICÉ : 2 815 PAGES, 7,69 M CARACTÈRES, 8 KO 0 (VAL/TEST VIDES, LE CSS SUIT) |
78:| 01:34 | `868399c8` | DONNÉES — LA ROADMAP ET LE RÉCIT PORTENT L'OCR DES 8 LIVRES : 2 815 PAGES, 7,69 M CARACTÈRES, 951 FENÊTRES 8 KO |
79:| 01:37 | `a9a511e8` | DONNÉES — LE CONTRÔLE OCR CONTRE LES ÉVALUATIONS EST MESURÉ : 0/40, 0/24, 0/40 |
91:| 02:20 | `07e87a6f` | DONNÉES — L'OCR PASSE 10 M CARACTÈRES : 11 LIVRES, 4 042 PAGES, 1 244 FENÊTRES 8 KO, ÉVAL 0/40 |
117:| 05:10 | `15f2c8f6` | DONNÉES — L'OCR DES 20 LIVRES EST CLOS : 7 381 PAGES, 15,36 M CARACTÈRES, 8 KO 0 (VAL 115, ÉVAL 0/40) |
122:| 05:25 | `166896b4` | GENRES — L'OCR DES 20 LIVRES PASSE À 38,5 CAR/LIGNE (6,8 % DE DOUBLONS, 14,4 M) |
128:| 05:48 | `bfe57da7` | CHANTIERS — LA LIGNE D PORTE L'OCR DES 20 LIVRES (15,36 M CARACTÈRES, 8 Ko 0) |
132:| 06:30 | `ccf8bac5` | DONNÉES — 
… [2623 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_contamination.py --help 2>&1 | head -30; echo \"---\"; bash tools/porte-ocr-scans.sh 2>&1 | tail -8", "description": "Check contamination tool and OCR scan gate"}`

  ```
usage: verifie_contamination.py [-h] --train TRAIN [--val VAL] [--test TEST]
                                [--eval EVAL] [--fenetre FENETRE] [--pas PAS]
                                [--echantillon ECHANTILLON]
                                [--taille-troncon TAILLE_TRONCON]
                                [--sortie SORTIE]

verifie_contamination.py — les fuites entre splits et entre corpus, mesurées.
POURQUOI CE FICHIER. Un corpus d'entraînement sans contrôle de fuite est un
corpus qui mentira sur son évaluation. Ce script vérifie deux choses, avec des
chiffres : 1. **les doublons de tronçons entre splits** : chaque ligne des
fichiers (tronçon de 8 Ko écrit par `corpus_wikipedia.py`) est hachée ; un
tronçon qui apparaît dans deux splits est une fuite exacte (les quasi-doublons
ne sont pas détectés — c'est dit). Pour le **texte intégral**
(`corpus_wikipedia_texte.py`), l'unité est la **fenêtre** de 8 Ko coupée au
mot (`--taille-troncon 8192`), parce que les tronçons contiennent des retours
à la ligne ; 2. **le recouvrement avec les jeux d'évaluation** : des fenêtres
de `--fenetre` octets, échantillonnées dans chaque fichier d'évaluation, sont
cherchées dans l'entraînement par 
… [742 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-34 (bash: python3 work/ocr/census_cegep.py) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-34"}`

  ```
{
 "pdfs": 2681,
 "examynes": 2663,
 "scans": 807,
 "pages_scans": 179426,
 "scans_apres_52": 797,
 "pages_apres_52": 177830
}
géants > 500 p : [('Haskell Programming from First Principles (Chris A', 1971, True), ('Haskell Programming from First Principles (Chris A', 1971, True), ('Haskell Programming from First Principles (Chris A', 1971, True), ('Haskell Programming from First Principles (Chris A', 1971, True), ('Encyclopedia of Algorithms by Michele Mosca (auth.', 1628, True), ('Encyclopedia of Algorithms by Michele Mosca (auth.', 1628, True), ('The Handbook of Computer Networks, LANs, MANs, WAN', 1276, True), ('The Handbook of Computer Networks, LANs, MANs, WAN', 1276, True), ('kolban-ESP32.pdf', 1228, True), ('Learn Java for Android Development, 3rd Edition.pd', 1190, True), ('Programming Rust Fast, Safe Systems Development by', 1157, True), ('STM32英文参考手册_V15.pdf', 1128, True), ('Pro Android 4.pdf', 1008, True), ('Information Modeling and Relational Databases by T', 970, True), ('Agile Principles, Patterns, and Practices in C by ', 944, True), ('Implementing Domain-Driven Design by Vaughn Vernon', 925, True), ('Implementing Domain-Driven Design by Vaughn Vernon', 925, True), (
… [5141 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-37"}`

  ```
(no new output)
[status: running]
  ```

- **read** `{"file_path": "tools/extrait_pdf.py", "limit": 80, "offset": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/extrait_pdf.py</path>
<type>file</type>
<content>
80:     ap.add_argument("--manifeste", type=pathlib.Path,
81:                     default=RACINE / "reports/corpus-pdf.json")
82:     ap.add_argument("--max-pdf", type=int, default=0)
83:     ap.add_argument("--min-chars", type=int, default=300)
84:     ap.add_argument("--seuil-scan", type=int, default=50, help="caractères par page sous lesquels le PDF est scanné")
85:     ap.add_argument("--chunk", type=int, default=8192)
86:     ap.add_argument("--val", type=float, default=0.05)
87:     ap.add_argument("--test", type=float, default=0.05)
88:     ap.add_argument("--graine", type=int, default=1)
89:     args = ap.parse_args()
90:     racines = ([(lib, pathlib.Path(chemin)) for chemin, lib in
91:                 (r.split(":", 1) if ":" in r else (r, "") for r in args.racine)]
92:                or [(lib, chemin) for lib, chemin, _ in RACINES])
93:     args.sortie.mkdir(parents=True, exist_ok=True)
94:     seuil_val, seuil_test = int(args.val * 1000), int((args.val + args.test) * 1000)
95:     fichiers = {n: (args.sortie / f"{n}.txt").open("w", encoding="utf-8") for n in ("tr
… [3404 caractères tronqués]
  ```

- **read** `{"file_path": "tools/extrait_pdf.py", "limit": 40, "offset": 35}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/extrait_pdf.py</path>
<type>file</type>
<content>
35: 
36: 
37: def pages(pdf: pathlib.Path) -> int:
38:     try:
39:         s = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, timeout=30).stdout
40:         for ligne in s.splitlines():
41:             if ligne.startswith("Pages:"):
42:                 return int(ligne.split()[1])
43:     except Exception:
44:         pass
45:     return 0
46: 
47: 
48: def texte(pdf: pathlib.Path) -> str:
49:     try:
50:         r = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
51:                            capture_output=True, timeout=120)
52:         return r.stdout.decode("utf-8", "ignore")
53:     except Exception:
54:         return ""
55: 
56: 
57: def empreinte(t: str, taille: int = 16) -> str:
58:     return hashlib.blake2b(t.encode("utf-8"), digest_size=taille).hexdigest()
59: 
60: 
61: def troncons(t: str, taille: int):
62:     debut = 0
63:     while debut < len(t):
64:         fin = min(debut + taille, len(t))
65:         if fin < len(t):
66:             coupe = t.rfind(" ", debut + taille // 2, fin)
67:             if coupe > debut:
68
… [211 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recensement complet : la détection à 2 pages sur-classifie (807 au lieu de ~137) — je mesure le vrai fonds

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Détection *intégrale* des PDF scannés du fonds CEGEP.\n\n`tools/ocr_pdf.py` classe un PDF « scanné » sur le texte natif des **deux premières pages** ;\n`tools/extrait_pdf.py` le classe sur le **texte intégral**. Le recensement à 2 pages a trouvé\n807 « scan … [3330 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/ocr/detecte_cegep.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 work/ocr/detecte_cegep.py", "description": "Detect true scanned PDFs via full text", "run_in_background": true}`

  ```
started background job bash-38
  ```

- **job_output** `{"job_id": "bash-37"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "head -30 tools/porte-ocr-scans.sh; echo \"---\"; grep -n \"OMP\\|tesseract\" tools/mesurer_ocr.py | head", "description": "Inspect OCR scan gate and threading settings"}`

  ```
#!/bin/bash
# porte-ocr-scans.sh — R4.4 : les scans (5 familles), les colonnes, les tableaux.
#
# POURQUOI CETTE PORTE EXISTE. La première porte OCR vérifiait dix pages **rendues** ; elle ne
# voyait ni une photocopie, ni une photo, ni un fax, ni une page à deux colonnes, ni un tableau.
# Cette porte mesure ce que R4.4 promet : cinq familles de dégradation, un split dev/test, la
# parité du lecteur, la gouttière des colonnes et les cellules des tableaux — chacune avec ses
# contrôles négatifs (page noire, page mono, contrôle sans redressement, texte à plat).
#
# CE QU'ELLE NE VÉRIFIE PAS : les scans RÉELS (la validation externe est dans la fiche, sur un
# PDF d'Internet Archive) ; les seuils sont des PLANCHERS mesurés, pas des prédictions.
#
# Usage : tools/porte-ocr-scans.sh
set -u
cd "$(dirname "$0")/.."
echo "=== PORTE R4.4 — SCANS, COLONNES, TABLEAUX ==="
if ! bash tools/installer_ocr.sh --verifie; then
    echo "  ❌ OCR absent de la machine : tools/installer_ocr.sh (environnementale)"
    exit 2
fi
J=$(mktemp -d)
if [ ! -s work/r44/scans/manifeste.json ]; then
    echo "  corpus de scans absent : fabrication (10 pages dev + 10 test × 5 familles)"
    python3 tools/simuler_scan
… [283 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-38", "wait": true, "timeout_ms": 240000}`

  ```
{
 "pdfs": 2681,
 "scans": 147,
 "pages_scans": 2701,
 "deja_ocrises": 2,
 "restants": 145,
 "pages_restants": 2697
}
plus gros restants : [('Complete Us Patents Of Nikola Tesla Free Energy Electri', 499), ('Complete Us Patents Of Nikola Tesla Free Energy Electri', 499), ('MicroPython Programming with ESP32 and ESP8266 by Rui S', 359), ('ITIL service design by Vernon Lloyd Sharon Taylor Stati', 352), ('Rust in Action (MEAP) by T.S. McNamara (z-lib.org).pdf', 331), ('Information and self-organization (Hermann Haken) (z-li', 116), ('ST MCU 最新选型手册_201603.pdf', 60), ('ov2640_ds_1.8_.pdf', 45)]
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib\nd=json.load(open('work/ocr/detection-cegep.json'))\nscans=[m for m in d['detail'] if m['scan']]\nprint('scans', len(scans), 'pages', sum(m['pages'] for m in scans))\nfor m in scans:\n    n=pathlib.Path(m['chemin']).name\n    if any(k.lower() in n. … [291 caractères tronqués]`

  ```
scans 147 pages 2701
      2 p         0 car  inscription AQPC.pdf
      2 p         0 car  inscription AQPC.pdf
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib\nd=json.load(open('work/ocr/detection-cegep.json'))\nfor m in d['detail']:\n    n=pathlib.Path(m['chemin']).name\n    if any(k.lower() in n.lower() for k in (\"Algorithms Illuminated\",\"Data Structures and Algorithms in C\",\"Exercices de synthèse … [245 caractères tronqués]`

  ```
scan=False   43 p     72411 car ratio= 1684.0  Exercices de synthèse Excel 2010 Fonctions avancées.pdf
scan=False   40 p     65250 car ratio= 1631.2  AMF-AO-Annexes 1 à 11 (Admin).pdf
scan=False  121 p    186210 car ratio= 1538.9  AMF-AO-Annexes 12 à 15 (Tech).pdf
scan=False   60 p     27813 car ratio=  463.6  AMF-AO-Annexes 16 - Gabarits.pdf
scan=False  221 p    349668 car ratio= 1582.2  Algorithms Illuminated (Part 2) Graph Algorithms and Data Structures by Tim Roug
scan=False  226 p    362085 car ratio= 1602.1  Algorithms Illuminated (Part 3) Greedy Algorithms and Dynamic Programming by Tim
scan=False  274 p    467499 car ratio= 1706.2  Algorithms Illuminated (Part 4) Algorithms for NP-Hard Problems by Tim Roughgard
scan=False  217 p    346422 car ratio= 1596.4  Algorithms Illuminated Part 1 The Basics by Tim Roughgarden.pdf
scan=False  366 p    508956 car ratio= 1390.6  Data Structures and Algorithms in C by Michael McMillan.pdf
scan=False   43 p     72411 car ratio= 1684.0  Exercices de synthèse Excel 2010 Fonctions avancées.pdf
scan=False   40 p     65250 car ratio= 1631.2  AMF-AO-Annexes 1 à 11 (Admin).pdf
scan=False  121 p    186210 car ratio= 1538.9  AMF-AO-Annexes 12 à 15
… [693 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib, collections\nd=json.load(open('work/ocr/detection-cegep.json'))\nscans=[m for m in d['detail'] if m['scan']]\nprint('scans', len(scans), 'pages', sum(m['pages'] for m in scans))\ntailles=collections.defaultdict(list)\nfor m in scans:\n    p=pathli … [702 caractères tronqués]`

  ```
scans 147 pages 2701
tailles uniques 91
groupes de doublons (taille identique): 47 fichiers en trop: 56
  279533 ['inscription AQPC.pdf', 'inscription AQPC.pdf']
  357044 ['document%20de%20revision_pages_12a15_5421.pdf', 'document%20de%20revision_pages_12a15_5421.pdf']
  412274 ['document%20de%20revision_pages_16a25_8321.pdf', 'document%20de%20revision_pages_16a25_8321.pdf']
  623450 ['document%20de%20revision_pages_1a11_5218.pdf', 'document%20de%20revision_pages_1a11_5218.pdf']
  249585 ['document%20de%20revision_pages_26a30_8536.pdf', 'document%20de%20revision_pages_26a30_8536.pdf']
  380157 ['document%20de%20revision_pages_31a40_3069.pdf', 'document%20de%20revision_pages_31a40_3069.pdf']
  181695 ['document%20de%20revision_pages_41a45_8364.pdf', 'document%20de%20revision_pages_41a45_8364.pdf']
  463499 ['document%20de%20revision_pages_46a55_3011.pdf', 'document%20de%20revision_pages_46a55_3011.pdf']
  334994 ['document%20de%20revision_pages_56a64_2256.pdf', 'document%20de%20revision_pages_56a64_2256.pdf']
  34091 ['Classe informatique - option 1.pdf', 'Classe informatique - option 1.pdf']
--- distribution pages ---
min 1 max 499 médiane 1 total 2701
  >= 1 p : 147
  >= 2 p : 66

… [57 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib, hashlib, collections, concurrent.futures as cf\nd=json.load(open('work/ocr/detection-cegep.json'))\nscans=[m for m in d['detail'] if m['scan']]\ndef h(m):\n    p=pathlib.Path(m['chemin'])\n    x=hashlib.sha256()\n    with p.open('rb') as f:\n      … [1132 caractères tronqués]`

  ```
scans 147 uniques (sha256) 91 doublons 56
pages uniques 2053 vs 2701
groupes dupliqués: 47
   499 p  Complete Us Patents Of Nikola Tesla Free Energy Electricity Alternativ
   359 p  MicroPython Programming with ESP32 and ESP8266 by Rui Santos, Sara San
   352 p  ITIL service design by Vernon Lloyd Sharon Taylor Stationery Office. L
   331 p  Rust in Action (MEAP) by T.S. McNamara (z-lib.org).pdf
   116 p  Information and self-organization (Hermann Haken) (z-lib.org).pdf
    60 p  ST MCU 最新选型手册_201603.pdf
    45 p  ov2640_ds_1.8_.pdf
    42 p  MergedDocument1.pdf
    18 p  scenario 4 - tâche A2016.pdf
    12 p  StandardBusiness.pdf
    12 p  StandardBusiness.pdf
    10 p  document%20de%20revision_pages_16a25_8321.pdf
  ```

- **job_output** `{"job_id": "bash-37"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "P=$(grep -m1 \"inscription AQPC\" work/ocr/scans-uniques.txt); echo \"$P\"; rm -rf /tmp/benchocr && mkdir -p /tmp/benchocr && pdftoppm -r 300 -gray -png -f 1 -l 1 \"$P\" /tmp/benchocr/p && ls -l /tmp/benchocr/", "description": "Render a benchmark page"}`

  ```
/home/stephane/Data13TB/stephane/archives/CEGEP/import-export-2026-06-20/Documents/Enseignement/Administration/AQPC 2016/inscription AQPC.pdf
total 268
-rw-r--r--. 1 stephane stephane 270339  2 nov 16:27 p-1.png
  ```

- **bash** `{"command": "ROOT=$PWD/work/ocr/root; for mode in default omp1; do for i in 1 2; do if [ $mode = omp1 ]; then export OMP_THREAD_LIMIT=1; else unset OMP_THREAD_LIMIT; fi; /usr/bin/time -f \"$mode run$i: %e s (%P CPU)\" env LD_LIBRARY_PATH=$ROOT/usr/lib64 TESSDATA_PREFIX=$ROOT/usr/share/tessdata $ROOT … [263 caractères tronqués]`

  ```
default run1: 2.04 s (141% CPU)
default run2: 1.46 s (192% CPU)
omp1 run1: 1.56 s (99% CPU)
omp1 run2: 1.51 s (100% CPU)
 890 /tmp/benchocr/out-default-1.txt
 890 /tmp/benchocr/out-default-2.txt
 890 /tmp/benchocr/out-omp1-1.txt
 890 /tmp/benchocr/out-omp1-2.txt
3560 total
  ```

### 🤖 Assistant

⏵ Correction mesurée : 807 candidats à 2 pages, mais 147 vrais scans (91 uniques, 2 053 p) — j'adapte l'outil

- **edit** `{"file_path": "tools/ocr_pdf.py", "old_string": "Usage :\n  python3 tools/ocr_pdf.py --max-doc 20          # pilote (les 20 premiers scannés)\n  python3 tools/ocr_pdf.py                       # tous les scannés des racines\n\"\"\"", "new_string": "Usage :\n  python3 tools/ocr_pdf.py --max-doc 20     … [674 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ocr_pdf.py": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "tools/ocr_pdf.py", "limit": 40}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ocr_pdf.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """ocr_pdf.py — l'OCR des PDF **scannés** (R4.4 appliqué aux documents réels).
3: 
4: POURQUOI. `extrait_pdf.py` extrait le texte natif ; les PDF sans couche texte (les scans) sont
5: comptés et écartés. Ce script les **océrise** avec le tesseract installé sans root par
6: `installer_ocr.sh` (5.5.3, fra+eng) : `pdftoppm` rend les pages, `tesseract` les lit.
7: 
8: Ce qu'il ne fait pas (encore) : le prétraitement d'image de R4.4 (`nettoyer_scan.py` : rotation,
9: contraste, colonnes) — le pilote mesure l'OCR **brut** ; la WER réelle n'a pas de vérité terrain
10: (seule la parité R4.4 sur scans simulés la donne), donc la fiche donne le débit, les caractères et
11: un échantillon, pas une WER inventée.
12: 
13: Usage :
14:   python3 tools/ocr_pdf.py --max-doc 20          # pilote (les 20 premiers scannés)
15:   python3 tools/ocr_pdf.py                       # tous les scannés des racines
16: """
17: from __future__ import annotations
18: 
19: import argparse
20: import hashlib
21: import json
22: import os
23: import pathlib
24: import shutil
25: impor
… [748 caractères tronqués]
  ```

- **edit** `{"file_path": "tools/ocr_pdf.py", "new_string": "Usage :\n  python3 tools/ocr_pdf.py --max-doc 20          # pilote (les 20 premiers scannés)\n  python3 tools/ocr_pdf.py                       # tous les scannés des racines\n  python3 tools/ocr_pdf.py --liste scans.txt --ouvriers 8\n      # liste exp … [1099 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ocr_pdf.py has been updated successfully.
  ```

- **read** `{"file_path": "tools/ocr_pdf.py", "limit": 35, "offset": 48}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ocr_pdf.py</path>
<type>file</type>
<content>
48: 
49: def pages(pdf: pathlib.Path) -> int:
50:     try:
51:         s = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, timeout=30).stdout
52:         for ligne in s.splitlines():
53:             if ligne.startswith("Pages:"):
54:                 return int(ligne.split()[1])
55:     except Exception:
56:         pass
57:     return 0
58: 
59: 
60: def natif(pdf: pathlib.Path) -> str:
61:     try:
62:         return subprocess.run(["pdftotext", "-f", "1", "-l", "2", "-enc", "UTF-8", str(pdf), "-"],
63:                               capture_output=True, timeout=60).stdout.decode("utf-8", "ignore")
64:     except Exception:
65:         return ""
66: 
67: 
68: def ocr(pdf: pathlib.Path, dpi: int, langues: str, max_pages: int) -> tuple[str, int]:
69:     tmp = pathlib.Path(tempfile.mkdtemp(prefix="ocr-pdf-"))
70:     try:
71:         cmd = ["pdftoppm", "-r", str(dpi), "-gray", "-png"]
72:         if max_pages:
73:             cmd += ["-f", "1", "-l", str(max_pages)]
74:         cmd += [str(pdf), str(tmp / "p")]
75:         try:
76:             subprocess.run
… [438 caractères tronqués]
  ```

- **edit** `{"file_path": "tools/ocr_pdf.py", "new_string": "def ocr(pdf: pathlib.Path, dpi: int, langues: str, max_pages: int,\n        ouvriers: int = 1) -> tuple[str, int]:\n    tmp = pathlib.Path(tempfile.mkdtemp(prefix=\"ocr-pdf-\"))\n    try:\n        cmd = [\"pdftoppm\", \"-r\", str(dpi), \"-gray\", \"-p … [2388 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ocr_pdf.py has been updated successfully.
  ```

- **read** `{"file_path": "tools/ocr_pdf.py", "limit": 55, "offset": 108}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ocr_pdf.py</path>
<type>file</type>
<content>
108:     debut = 0
109:     while debut < len(t):
110:         fin = min(debut + taille, len(t))
111:         if fin < len(t):
112:             coupe = t.rfind(" ", debut + taille // 2, fin)
113:             if coupe > debut:
114:                 fin = coupe
115:         m = t[debut:fin].strip()
116:         if m:
117:             yield m
118:         debut = fin
119: 
120: 
121: def main() -> int:
122:     ap = argparse.ArgumentParser(description=__doc__)
123:     ap.add_argument("--max-doc", type=int, default=0)
124:     ap.add_argument("--racine", default="", help="restreindre à une racine : Biblio_large, CEGEP")
125:     ap.add_argument("--deja", type=int, default=0, help="sauter les N premiers PDF examinés (reprise)")
126:     ap.add_argument("--dpi", type=int, default=300)
127:     ap.add_argument("--langues", default="fra+eng")
128:     ap.add_argument("--max-pages", type=int, default=0)
129:     ap.add_argument("--min-chars", type=int, default=300)
130:     ap.add_argument("--chunk", type=int, default=8192)
131:     ap.add_argument("--val", type=float, default=0.05)
132
… [1817 caractères tronqués]
  ```

- **edit** `{"file_path": "tools/ocr_pdf.py", "new_string": "    ap.add_argument(\"--max-doc\", type=int, default=0)\n    ap.add_argument(\"--racine\", default=\"\", help=\"restreindre à une racine : Biblio_large, CEGEP\")\n    ap.add_argument(\"--deja\", type=int, default=0, help=\"sauter les N premiers PDF ex … [5072 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ocr_pdf.py has been updated successfully.
  ```

- **read** `{"file_path": "tools/ocr_pdf.py", "limit": 30, "offset": 168}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ocr_pdf.py</path>
<type>file</type>
<content>
168:             if args.max_doc and stats["ocrises"] >= args.max_doc:
169:                 break
170:             npages = pages(pdf)
171:             if not npages:
172:                 continue
173:             stats["pdfs"] += 1
174:             if args.deja and stats["pdfs"] <= args.deja:
175:                 continue
176:             t = natif(pdf)
177:             if len(t.strip()) / max(npages, 1) >= 50:
178:                 continue  # il a du texte natif : déjà dans le corpus PDF
179:             stats["scannes"] += 1
180:             texte, n = ocr(pdf, args.dpi, args.langues, args.max_pages)
181:             if len(texte) < args.min_chars:
182:                 continue
183:             marque = empreinte(texte)
184:             if marque in vus:
185:                 continue
186:             vus.add(marque)
187:             doc = f"{pdf.stem}\n{texte}"
188:             h = int(empreinte(f"{args.graine}:{pdf.as_posix()}", 8), 16) % 1000
189:             split = "val" if h < seuil_val else ("test" if h < seuil_test else "train")
190:             morceaux = []
191:    
… [373 caractères tronqués]
  ```

- **edit** `{"file_path": "tools/ocr_pdf.py", "new_string": "            if args.deja and stats[\"pdfs\"] <= args.deja:\n                continue\n            if liste is None:\n                t = natif(pdf)\n                if len(t.strip()) / max(npages, 1) >= 50:\n                    continue  # il a du tex … [531 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ocr_pdf.py has been updated successfully.
  ```

- **read** `{"file_path": "tools/ocr_pdf.py", "limit": 35, "offset": 213}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ocr_pdf.py</path>
<type>file</type>
<content>
213:     stats["mots_estimes"] = int(stats["caracteres"] / 6.2)
214:     for nom in ("train", "val", "test"):
215:         chemin = args.sortie / f"{nom}.txt"
216:         stats["octets"][nom] = chemin.stat().st_size
217:         h = hashlib.sha256()
218:         with chemin.open("rb") as f:
219:             for bloc in iter(lambda: f.read(1 << 20), b""):
220:                 h.update(bloc)
221:         stats[f"sha256_{nom}"] = h.hexdigest()
222:     args.manifeste.parent.mkdir(parents=True, exist_ok=True)
223:     args.manifeste.write_text(json.dumps({
224:         "date": "2026-11-01", "ligne": "Données (R4.4 appliqué)", "nature": "corpus OCR des PDF scannés",
225:         "dispositif": {"ocr": "tesseract 5.5.3 sans root (work/ocr/root)", "langues": args.langues,
226:                        "dpi": args.dpi, "psm": 3, "pretraitement": "aucun (le R4.4 le fera)",
227:                        "split": f"hash salé du chemin : {args.val:.0%} val, {args.test:.0%} test",
228:                        "deduplication": "documents + tronçons"},
229:         **stats,
230:         "limites":
… [650 caractères tronqués]
  ```

- **edit** `{"file_path": "tools/ocr_pdf.py", "new_string": "    args.manifeste.write_text(json.dumps({\n        \"date\": time.strftime(\"%Y-%m-%d\"), \"ligne\": \"Données (R4.4 appliqué)\",\n        \"nature\": \"corpus OCR des PDF scannés\",\n        \"dispositif\": {\"ocr\": \"tesseract 5.5.3 sans root (wor … [1936 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ocr_pdf.py has been updated successfully.
  ```

- **bash** `{"command": "python3 -m py_compile tools/ocr_pdf.py && echo \"compile OK\"; head -3 work/ocr/scans-uniques.txt > /tmp/test-liste.txt; rm -rf /tmp/test-ocr /tmp/test-ocr.json; time python3 tools/ocr_pdf.py --liste /tmp/test-liste.txt --racine CEGEP --sortie /tmp/test-ocr --manifeste /tmp/test-ocr.jso … [286 caractères tronqués]`
