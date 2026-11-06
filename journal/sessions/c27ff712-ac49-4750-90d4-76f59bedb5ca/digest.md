# Session DSH — relecture

- identifiant : `c27ff712-ac49-4750-90d4-76f59bedb5ca`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 19:25:28
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **re-mesurer le split dev/test** sur l'état v7 (commit `69bd865e`) et éprouver sa robustesse.

Contexte : `tools/tests/linguistique/gold_split.py` (`dev`, `test`, `compter`), `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bloc`), `tools/bloc_linguistique.py`. La fiche `reports/rapport-gold-split.md` a mesuré dev 125/126 et test 60/61 **avant** la v5/v7 ; le split n'a pas été re-mesuré depuis.

À faire :
1. Re-mesure dev et test au commit courant : exact/labels, F1, tête, couverture, par langue (fr/en) et par type (REL/SUB/GP).
2. Vérifie l'**équilibre** du split : sources, langues, types de cibles ; signale si une catégorie est absente d'une moitié.
3. Éprouve la **stabilité** : décale le split (par ex. `crc32(id) % 3 == 1` puis `== 2` pour le test) et re-mesure — les taux doivent rester proches ; donne l'écart.
4. Compare dev et test : si l'écart est > 2 cas, dis-le et propose une explication.
5. Écris **uniquement** deux fichiers neufs : `reports/rapport-dev-test-v7.md` et `reports/pensee-dev-test-v7.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé : dev, test, les trois splits, et l'écart.
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

⏵ Exploration du dépôt et des scripts du split gold

- **bash** `{"command": "git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet status --short --branch && git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet log --oneline -3", "description": "Check git status and current commit"}`

  ```
## s/v7
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
D  journal/sessions/63d4c619-63e8-41b9-a183-5c
… [3143 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/ /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/ | head -60", "description": "List test and reports directories"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/:
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
-rw-r--r--. 1 stephane stephane     600 29 oct 20:06 
… [3107 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des scripts du split et de l'évaluation gold

- **bash** `{"command": "ls -la tools/tests/linguistique/ && ls -la reports/ | grep -i -E \"gold|split|dev-test\"", "description": "List linguistique tools and gold reports", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
total 1464
drwxr-xr-x. 1 stephane stephane    764  5 nov 17:52 .
drwxr-xr-x. 1 stephane stephane    640  4 nov 08:44 ..
-rw-r--r--. 1 stephane stephane  16090  2 nov 09:26 anaphore.py
-rw-r--r--. 1 stephane stephane  35148  5 nov 14:25 classement_cible.py
-rw-r--r--. 1 stephane stephane  15579  5 nov 16:18 evaluer_gold.py
-rw-r--r--. 1 stephane stephane 450905  2 nov 13:27 gold_gele.json
-rw-r--r--. 1 stephane stephane  20009  5 nov 16:37 gold.json
-rw-r--r--. 1 stephane stephane   7813  2 nov 12:03 gold.py
-rw-r--r--. 1 stephane stephane 470149  2 nov 14:39 gold_reel.json
-rw-r--r--. 1 stephane stephane 132934  5 nov 14:04 gold_reel.py
-rw-r--r--. 1 stephane stephane   1939  5 nov 17:52 gold_split.py
-rw-r--r--. 1 stephane stephane 149191  2 nov 12:04 gold_synthetique.json
-rw-r--r--. 1 stephane stephane  10124  2 nov 12:03 gold_synthetique.py
-rw-r--r--. 1 stephane stephane   2953  2 nov 12:17 juge.py
-rw-r--r--. 1 stephane stephane  22366  3 nov 14:05 miroir.py
drwxr-xr-x. 1 stephane stephane    720  5 nov 17:52 __pycache__
-rw-------. 1 stephane stephane   9951  3 nov 00:39 qualifier_cascade.py
-rw-r--r--. 1 stephane stephane   6589  3 nov 16:39 qualifier_frontiere_71.py
-rw-r-
… [3377 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_split.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_split.py</path>
<type>file</type>
<content>
1: """gold_split.py — le gold 612 coupé en **dev** et **test**, de façon déterministe.
2: 
3: Le problème. Toutes les mesures de la session sont **in-sample** : les règles de segmentation et
4: d'attachement ont été dessinées en regardant les échecs du même gold qui les mesure. Pour juger
5: une règle, il faut un gold **tenu à l'écart** : on règle sur `dev`, on évalue sur `test`.
6: 
7: Protocole (fixé ici). Le split est un **hash stable de l'identifiant** (`crc32(id) % 3 == 0` →
8: test, sinon dev), donc reproductible, insensible à l'ordre et indépendant du contenu. Il est
9: **stratifié par source** (`hand`, `reel`, `synthetique`) et par langue : on vérifie l'équilibre
10: dans la fiche. Aucune phrase n'est dupliquée entre les deux ; l'union redonne les 612.
11: 
12: Usage :
13:     from tools.tests.linguistique.gold_split import dev, test, compter
14:     ph = charger(); d = dev(ph); t = test(ph)
15: """
16: from __future__ import annotations
17: 
18: import zlib
19: 
20: PART_TEST = 3  # une phrase sur trois va au test
21: 
22: 
23: def _est_test(phras
… [1070 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-split.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py</path>
<type>file</type>
<content>
1: """evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) + synthétique (160).
2: 
3: Trois niveaux : POS (token, exact), syntagmes (exact + **par tête**), pragmatique. Quatre
4: lectures : heuristique, mock neuronal, parallèle, cascade. Le vrai modèle est optionnel
5: (`--reel`) : s'il ne répond pas, il est refusé, pas simulé.
6: """
7: from __future__ import annotations
8: 
9: import argparse
10: import json
11: import pathlib
12: import sys
13: from collections import Counter, defaultdict
14: 
15: RACINE = pathlib.Path(__file__).resolve().parents[3]
16: sys.path.insert(0, str(RACINE / "tools"))
17: import bloc_linguistique as bl  # noqa: E402
18: 
19: GOLD = pathlib.Path(__file__).with_name("gold.json")
20: REEL = pathlib.Path(__file__).with_name("gold_reel.json")
21: SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")
22: 
23: 
24: def charger() -> list[dict]:
25:     hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
26:     reel = json.loads(REEL.read_text(encoding="utf-8"))["phrases"]
27:     synth = json.
… [15928 caractères tronqués]
  ```


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

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-split.json"}`

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

- **bash** `{"command": "grep -rn \"gold_split\" --include=*.py --include=*.md --include=*.sh . | head -40", "description": "Find usages of gold_split", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
./reports/rapport-gold-split.md:10:> **Dispositif** : [`gold_split.py`](../tools/tests/linguistique/gold_split.py) (`dev`, `test`,
./reports/rapport-gold-split.md:62:- [`gold_split.py`](../tools/tests/linguistique/gold_split.py) — le split.
./reports/rapport-pensee-couverture-v5.md:12:> [`gold_split.py`](../tools/tests/linguistique/gold_split.py) pour dev/test ; JSON
./reports/rapport-pensee-couverture-v5.md:78:- [`gold_split.py`](../tools/tests/linguistique/gold_split.py) — dev/test.
./reports/rapport-pensee-attachement-parfait.md:11:> [`autotest.py`](../tools/pensee/autotest.py) ; dev/test [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ;
./tools/tests/linguistique/gold_split.py:1:"""gold_split.py — le gold 612 coupé en **dev** et **test**, de façon déterministe.
./tools/tests/linguistique/gold_split.py:13:    from tools.tests.linguistique.gold_split import dev, test, compter
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:44870:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > tools/tests/linguistique/gold_split.py <<'PY'\n\"\"\"gold_split.py — le gold 612 coupé en **dev** et **test**, de façon déterministe.\n\nLe
… [3943 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la fiche v7 et du gold pour comprendre les mesures récentes

- **bash** `{"command": "ls -la reports/*v7* reports/pensee-couverture* 2>/dev/null; echo ---; python3 - <<'PY'\nimport json\nfor f in [\"tools/tests/linguistique/gold.json\",\"tools/tests/linguistique/gold_reel.json\",\"tools/tests/linguistique/gold_synthetique.json\"]:\n    d=json.load(open(f))\n    ph=d[\"ph … [359 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 1228  5 nov 18:43 reports/pensee-couverture-v5.json
-rw-r--r--. 1 stephane stephane  841  5 nov 19:22 reports/pensee-couverture-v7.json
-rw-r--r--. 1 stephane stephane  841  5 nov 19:22 reports/pensee-couverture-v7.json
-rw-r--r--. 1 stephane stephane 3620  5 nov 19:22 reports/rapport-pensee-couverture-v7.md
---
tools/tests/linguistique/gold.json 20 phrases 56 segments
 keys: ['id', 'langue', 'texte', 'mots', 'segments', 'pragma']
 seg0: {"type": "GN", "texte": "Le chat", "role": "agent", "debut": 0, "fin": 7}
tools/tests/linguistique/gold_reel.json 432 phrases 1445 segments
 keys: ['id', 'langue', 'texte', 'mots', 'segments', 'pragma', 'source']
 seg0: {"type": "GN", "texte": "Le chien", "role": "agent", "debut": 0, "fin": 8}
tools/tests/linguistique/gold_synthetique.json 160 phrases 362 segments
 keys: ['id', 'langue', 'texte', 'pragma', 'source', 'mots', 'segments']
 seg0: {"type": "GN", "texte": "nous", "role": "gn", "debut": 0, "fin": 4}
  ```

- **bash** `{"command": "grep -rn \"REL\\|SUB\\|GP\" tools/bloc_linguistique.py | head -30; echo ===; grep -rn \"par_type\\|type_cible\\|types\" reports/pensee-couverture-v7.json 2>/dev/null | head", "description": "Search REL/SUB/GP handling", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
9:    substitution et le parallèle sans GPU ;
367:RELATIFS = {"qui", "que", "qu", "dont", "où", "which", "that", "who", "whom", "whose",
369:# les subordonnants qui n'ont pas d'antécédent : toujours SUB
375:SUBORDONNANTS = {"because", "although", "though", "if", "while", "as", "since", "unless",
382:# tague « talks » NOUN et « brother » VERB (mesuré le 05/11 sur les 22 GP restants).
645:        (GP, puis GN, puis GV), comme le premier candidat de `analyser`.
659:        """REL → tête du GN précédent ; SUB après un GV → son verbe (le gouverneur)."""
662:        if segment.get("type") == "REL" and precedent.get("type") == "GN":
664:        if segment.get("type") == "SUB" and precedent.get("type") == "GV":
672:        """Les candidats que le **précédent** impose : l'antécédent d'une REL, le verbe d'une SUB."""
675:        if segment.get("type") == "REL" and precedent.get("type") == "GN":
678:        if segment.get("type") == "SUB" and precedent.get("type") == "GV":
685:        """Cible vide d'un GP : génitif → tête du GN à gauche (sinon None, le GV tranchera)."""
686:        if segment.get("type") != "GP":
700:        """Sans gouverneur extérieur, une SUB/REL prend son propre verbe («
… [1258 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-couverture-v7.md"}`

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

- **bash** `{"command": "cat reports/pensee-couverture-v7.json; echo ===V5===; cat reports/pensee-couverture-v5.json", "description": "Read v7 and v5 coverage JSON", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "183/183",
 "avant": {
  "labels": 187,
  "exact": 187,
  "couverture": 0.7824,
  "f1": 0.513,
  "tete": 0.6826,
  "pos": 0.7475,
  "spans": 52
 },
 "apres": {
  "labels": 196,
  "exact": 195,
  "exact_span": 0.9949,
  "couverture": 0.8201,
  "f1": 0.5595,
  "f1_s": 0.4741,
  "f1_chunker": 0.5858,
  "tete": 0.7205,
  "pos": 0.7603,
  "fr": "135/135",
  "en": "60/61",
  "topk": 166,
  "topk_taux": 0.6946,
  "spans": {
   "REL": 21,
   "SUB": 17,
   "GP": 5,
   "total": 43
  }
 },
 "corrections": [
  "POS contextuel (DET/PRÉP/ADJ → nom)",
  "GV avant GP",
  "prépositions composées",
  "prépositions ambiguës (since/before/after/until/as)",
  "verbe après pronom sujet + adverbe final"
 ],
 "limites": [
  "43 spans",
  "top-k incomplet",
  "in-sample",
  "heuristiques"
 ]
}
===V5===
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "183/183",
 "avant": {
  "labels": 160,
  "exact": 157,
  "exact_span": 0.9812,
  "topk": 156,
  "couverture": 0.6695,
  "f1": 0.4539,
  "tete": 0.6432,
  "fr": 0.9915,
  "en": 0.9524,
  "spans": 79,
  "echecs_cible": 3
 },
 "apres": {
  "labels": 187,
  "exact": 186,
  "exact_span": 0.9947,
  "topk": 16
… [852 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport time, sys\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\nimport tools.bloc_linguistique as bl\nph=charger()\nprint(len(ph), \"phrases\")\nfrom collections import Counter\nprint(\"sources\", Counter(p.get(\"sourc … [708 caractères tronqués]`

  ```
612 phrases
sources Counter({'reel': 432, 'synthetique': 160, 'hand': 20})
langues Counter({'fr': 402, 'en': 210})
types avec cible Counter({'GP': 96, 'REL': 74, 'SUB': 69})
types tout Counter({'GN': 828, 'GV': 712, 'GP': 105, 'REL': 74, 'SUB': 70, 'ADJ': 35, 'ADV': 30, 'PONCT': 9})
ids uniques 612
init 0.0 s
30 phrases 0.028 s -> 612 ~ 0.6 s
  ```

### 🤖 Assistant

⏵ Écriture du script de mesure (dev/test + deux splits décalés)

- **write** `{"file_path": "/tmp/mesure_dev_test_v7.py", "content": "\"\"\"Mesure dev/test du gold 612 au commit v7, avec deux splits décalés.\n\nUsage : python3 /tmp/mesure_dev_test_v7.py /tmp/dev-test-v7.json\nN'écrit rien dans le dépôt.\n\"\"\"\nfrom __future__ import annotations\n\nimport collections\nimport … [15919 caractères tronqués]`

  ```
<path>/tmp/mesure_dev_test_v7.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport re\np='/tmp/mesure_dev_test_v7.py'\ns=open(p).read()\ns=s.replace('            vals = [splits[n][moitie][chemin] if False else chemin(splits[n][moitie])\\n                    for n in (\"canonique\", \"decale1\", \"decale2\")]',\n            '         … [281 caractères tronqués]`

  ```
ok
analyses: 612 en 0.38 s
validation contre evaluer_bloc : {'exact': (195, 195), 'labels': (196, 196), 'cibles': (239, 239), 'f1': (0.5555, 0.5555), 'tete_f1': (0.7152, 0.7152), 'pos': (0.7581, 0.7581), 'couverture': (0.8201, 0.8201)}
écrit /tmp/dev-test-v7.json
{
 "canonique": {
  "dev": {
   "phrases": 422,
   "cibles": 163,
   "labels": 134,
   "exact": 133,
   "exact_taux": 0.9925
  },
  "test": {
   "phrases": 190,
   "cibles": 76,
   "labels": 62,
   "exact": 62,
   "exact_taux": 1.0
  }
 },
 "decale1": {
  "dev": {
   "phrases": 383,
   "cibles": 150,
   "labels": 120,
   "exact": 119,
   "exact_taux": 0.9917
  },
  "test": {
   "phrases": 229,
   "cibles": 89,
   "labels": 76,
   "exact": 76,
   "exact_taux": 1.0
  }
 },
 "decale2": {
  "dev": {
   "phrases": 419,
   "cibles": 165,
   "labels": 138,
   "exact": 138,
   "exact_taux": 1.0
  },
  "test": {
   "phrases": 193,
   "cibles": 74,
   "labels": 58,
   "exact": 57,
   "exact_taux": 0.9828
  }
 }
}
écart: {"exact_cas_dev": 133, "labels_dev": 134, "echecs_dev": 1, "exact_cas_test": 62, "labels_test": 62, "echecs_test": 0, "ecart_taux_span": -0.0075, "ecart_f1": -0.0139, "ecart_tete": -0.0064, "ecart_couverture": 0.0063
… [2237 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des écarts avec la fiche v7 et correction du contrôle d'équilibre

- **bash** `{"command": "grep -rn \"0.5595\\|0.5555\\|0.7603\\|0.7581\\|union\" tools/pensee/autotest.py tools/bloc_linguistique.py tools/tests/linguistique/*.py 2>/dev/null | head -40", "description": "Find v7 metric definitions", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
tools/pensee/autotest.py:1639:            and abs(r["pos"]["exactitude"] - 0.7603) < 0.001), (
tools/pensee/autotest.py:1675:    h1 = bl.Heuristique(union=False)
tools/pensee/autotest.py:1676:    h2 = bl.Heuristique(union=False)
tools/pensee/autotest.py:1694:    h1 = bl.Heuristique(union=False)
tools/pensee/autotest.py:1695:    h2 = bl.Heuristique(union=False)
tools/pensee/autotest.py:1714:def t112_union() -> tuple[bool, str]:
tools/pensee/autotest.py:1715:    """L'union des segmenteurs : segments F1 0,2833 (S 0,1722), tête 0,5027."""
tools/pensee/autotest.py:1719:    h1 = bl.Heuristique(union=False)
tools/pensee/autotest.py:1720:    h2 = bl.Heuristique(union=False)
tools/pensee/autotest.py:1731:    return abs(f1 - 0.5595) < 0.001, f"union : segments F1 {f1} (S 0,4741)"
tools/pensee/autotest.py:1734:def t113_union_defaut() -> tuple[bool, str]:
tools/pensee/autotest.py:1735:    """L'union par défaut : F1 0,2833, tête 0,5027 dans l'analyseur."""
tools/pensee/autotest.py:1743:    return abs(f1 - 0.5595) < 0.001 and abs(tete - 0.7205) < 0.001, (
tools/pensee/autotest.py:1744:        f"union par défaut : F1 {f1}, tête {tete}")
tools/pensee/autotest.py:1747:def t114_cascade_union() -> tu
… [1500 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat 69bd865e | head -30; echo ===; git show 69bd865e:tools/bloc_linguistique.py | sha256sum; sha256sum tools/bloc_linguistique.py", "description": "Confirm working tree matches commit for bloc_linguistique", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

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
… [567 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "offset": 1625, "limit": 135}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
1625:           and abs(statistics.mean([mesurer_cv(tout, graine=k)["taux"]
1626:                                    for k in range(5)]) - 0.86) < 0.06
1627:           and abs(accords(tout)["paires"]["role/semantique"] - 1.0) < 1e-9)
1628:     return ok, "bilan : 4/4, 10/12, 12/12, 8/8, 27/30, méta 25/30, CV ~0,85"
1629: 
1630: 
1631: def t107_gold_complet() -> tuple[bool, str]:
1632:     """Le gold complet : 522 phrases, POS 0,7586."""
1633:     import tools.bloc_linguistique as bl
1634:     from ..tests.linguistique.evaluer_gold import charger_gele as charger, evaluer_bloc
1635:     phrases = charger()
1636:     h = bl.Heuristique()
1637:     r = evaluer_bloc("h", h, phrases)
1638:     return (len(phrases) == 602
1639:             and abs(r["pos"]["exactitude"] - 0.7603) < 0.001), (
1640:         f"gold complet : {len(phrases)} phrases, POS {round(r['pos']['exactitude'], 4)}, "
1641:         f"tête {round(r['syntagme']['tete']['f1'], 4)}")
1642: 
1643: 
1644: def t108_anaphore_68() -> tuple[bool, str]:
1645:     """La coréférence à 68 liens : 52/68 par le rôle, 51/68 
… [6030 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json, collections\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger, charger_gele, evaluer_bloc\nimport tools.bloc_linguistique as bl\nge=charger_gele(); vi=charger()\nprint(\"gele\", len(ge), \"cibles\", sum(1 for p in ge f … [1055 caractères tronqués]`

  ```
gele 602 cibles 239
vivant 612 cibles 239
sources gele Counter({'reel': 422, 'synthetique': 160, 'hand': 20})
langues gele Counter({'fr': 394, 'en': 208})
types gele Counter({'GP': 96, 'REL': 74, 'SUB': 69})
ids gele absents du vivant 0 vivant absents du gele 10
gele: exact 195 / 196 cibles 239 f1 0.5595 tete 0.7205 pos 0.7603
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/mesure_dev_test_v7.py'\ns=open(p).read()\nold='''        # catégories absentes (par rapport à l'ensemble)\n        absentes = {}\n        for cat, cle in ((\"sources\", \"sources\"), (\"langues\", \"langues\"),\n                         (\"types\", \ … [1564 caractères tronqués]`

  ```
ok
 "test_pos": {
  "valeurs": [
   0.7656,
   0.7545,
   0.7549
  ],
  "min": 0.7545,
  "max": 0.7656,
  "dispersion": 0.0111
 }
}
canonique absentes: {'sources': [], 'langues': [], 'types': [], 'types_langues': []}
  dev: {"hand": 15, "reel": 302, "synthetique": 105} {"fr": 277, "en": 145} {"GP": 61, "SUB": 45, "REL": 57}
  test: {"hand": 5, "reel": 130, "synthetique": 55} {"fr": 125, "en": 65} {"GP": 35, "REL": 17, "SUB": 24}
decale1 absentes: {'sources': [], 'langues': [], 'types': [], 'types_langues': []}
  dev: {"hand": 9, "reel": 272, "synthetique": 102} {"fr": 252, "en": 131} {"GP": 60, "SUB": 47, "REL": 43}
  test: {"hand": 11, "reel": 160, "synthetique": 58} {"fr": 150, "en": 79} {"GP": 36, "SUB": 22, "REL": 31}
decale2 absentes: {'sources': [], 'langues': [], 'types': [], 'types_langues': []}
  dev: {"hand": 16, "reel": 290, "synthetique": 113} {"fr": 275, "en": 144} {"GP": 71, "SUB": 46, "REL": 48}
  test: {"hand": 4, "reel": 142, "synthetique": 47} {"fr": 127, "en": 66} {"GP": 25, "SUB": 23, "REL": 26}
  ```

### 🤖 Assistant

⏵ Inspection détaillée des résultats par langue et par type

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/dev-test-v7.json'))\nfor n in (\"canonique\",\"decale1\",\"decale2\"):\n    print(\"=\"*20, n, d[\"splits\"][n][\"regle\"])\n    for moitie in (\"dev\",\"test\"):\n        m=d[\"splits\"][n][moitie]\n        a=m[\"attachement\"]\n    … [1115 caractères tronqués]`

  ```
==================== canonique crc32(id)%3==0 -> test
 dev: 422 phr, cibles 163, labels 134, exact 133, taux 0.9925, couv 0.8221, F1 0.5512, tete 0.7132, POS 0.7547
   langues: {'fr': (101, 92, 92, 1.0, 0.9109), 'en': (62, 42, 41, 0.9762, 0.6774)}
   types  : {'REL': (57, 42, 42, 1.0, 0.7368, 0.6176, 0.9016, 42, 37, 15), 'SUB': (45, 33, 33, 1.0, 0.7333, 0.7727, 0.9091, 34, 8, 12), 'GP': (61, 59, 58, 0.9831, 0.9672, 0.8497, 0.8609, 65, 21, 2)}
   type/langue: {'REL/fr': (34, 29, 29, 1.0), 'REL/en': (23, 13, 13, 1.0), 'SUB/fr': (29, 27, 27, 1.0), 'SUB/en': (16, 6, 6, 1.0), 'GP/fr': (38, 36, 36, 1.0), 'GP/en': (23, 23, 22, 0.9565)}
   spans perdus: {'SUB': 12, 'REL': 15, 'GP': 2}
   sources: {'hand': (10, 9, 9, 1.0), 'reel': (121, 101, 100, 0.9901), 'synthetique': (32, 24, 24, 1.0)}
 test: 190 phr, cibles 76, labels 62, exact 62, taux 1.0, couv 0.8158, F1 0.5651, tete 0.7196, POS 0.7656
   langues: {'fr': (50, 43, 43, 1.0, 0.86), 'en': (26, 19, 19, 1.0, 0.7308)}
   types  : {'REL': (17, 11, 11, 1.0, 0.6471, 0.55, 0.9444, 11, 12, 6), 'SUB': (24, 19, 19, 1.0, 0.7917, 0.76, 0.9388, 19, 7, 5), 'GP': (35, 32, 32, 1.0, 0.9143, 0.8095, 0.8537, 34, 12, 4)}
   type/langue: {'REL/fr': (12, 9, 9
… [3849 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Identification de l'unique échec d'attachement et des 43 spans perdus

- **bash** `{"command": "python3 - <<'PY'\nimport sys, zlib, json, collections\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger\nimport tools.bloc_linguistique as bl\nph=charger(); h=bl.Heuristique()\nechecs=[]; perdus=[]\nfor p in ph:\n    a=h.analyser(p[\"texte\"], p[\"langue … [1471 caractères tronqués]`

  ```
ECHECS exact: 1
('r102', 'en', 'GP', 'since this morning', 'falls', '', 2, 'The rain falls since this morning.')

PERDUS: 43 par type Counter({'REL': 21, 'SUB': 17, 'GP': 5}) par bucket Counter({2: 16, 0: 14, 1: 13}) par langue Counter({('SUB', 'en'): 13, ('REL', 'en'): 13, ('REL', 'fr'): 8, ('SUB', 'fr'): 4, ('GP', 'fr'): 4, ('GP', 'en'): 1})

par type/language: Counter({('SUB', 'en'): 13, ('REL', 'en'): 13, ('REL', 'fr'): 8, ('SUB', 'fr'): 4, ('GP', 'fr'): 4, ('GP', 'en'): 1})
bucket 0: Counter({'REL': 6, 'SUB': 5, 'GP': 3})
bucket 1: Counter({'REL': 7, 'SUB': 5, 'GP': 1})
bucket 2: Counter({'REL': 8, 'SUB': 7, 'GP': 1})
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger\nph=charger()\nfor src in (\"hand\",\"reel\",\"synthetique\"):\n    ids=[p[\"id\"] for p in ph if p.get(\"source\")==src]\n    print(src, len(ids), \"exemples:\", … [143 caractères tronqués]`

  ```
hand 20 exemples: ['g001', 'g002', 'g003', 'g004', 'g005', 'g006'] ... ['g018', 'g019', 'g020']
reel 432 exemples: ['r001', 'r002', 'r003', 'r004', 'r005', 'r006'] ... ['r420', 'r421', 'r422']
synthetique 160 exemples: ['s001', 's002', 's003', 's004', 's005', 's006'] ... ['s158', 's159', 's160']
  ```

- **bash** `{"command": "ls -l /tmp/dev-test-v7.json; head -c 600 /tmp/dev-test-v7.json", "description": "Check size of intermediate JSON"}`

  ```
-rw-r--r--. 1 stephane stephane 47917  5 nov 19:33 /tmp/dev-test-v7.json
{
 "commit": "69bd865e",
 "valide_contre_evaluer_gold": true,
 "validation": {
  "exact": [
   195,
   195
  ],
  "labels": [
   196,
   196
  ],
  "cibles": [
   239,
   239
  ],
  "f1": [
   0.5555,
   0.5555
  ],
  "tete_f1": [
   0.7152,
   0.7152
  ],
  "pos": [
   0.7581,
   0.7581
  ],
  "couverture": [
   0.8201,
   0.8201
  ]
 },
 "analyses_secondes": 0.367,
 "equilibre_global": {
  "phrases": 612,
  "ids_uniques": 612,
  "sources": {
   "hand": 20,
   "reel": 432,
   "synthetique": 160
  },
  "langues": {
   "fr": 402,
   "en": 210
  },
  "types_tout": {
   "GN": 828,
   "GV": 712,
  ```

### 🤖 Assistant

⏵ Décomposition F1 par type (GN/GV inclus) pour expliquer l'écart agrégé

- **bash** `{"command": "python3 - <<'PY'\nimport sys, zlib\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger\nimport tools.bloc_linguistique as bl\nph=charger(); h=bl.Heuristique()\ncache={p[\"id\"]:h.analyser(p[\"texte\"],p[\"langue\"]) for p in ph}\ndef f1(tp,fp,fn):\n    p=t … [1099 caractères tronqués]`

  ```
dev segments 1748
   ADJ (0.0, 0, 0, 30) n_gold 30 n_pred 0
   ADV (0.0, 0, 0, 18) n_gold 18 n_pred 0
   GN (0.4827, 230, 143, 350) n_gold 580 n_pred 373
   GP (0.8497, 65, 21, 2) n_gold 67 n_pred 86
   GV (0.572, 294, 243, 197) n_gold 491 n_pred 537
   PONCT (0.0, 0, 0, 7) n_gold 7 n_pred 0
   REL (0.6176, 42, 37, 15) n_gold 57 n_pred 79
   SUB (0.7727, 34, 8, 12) n_gold 46 n_pred 42
test segments 772
   ADJ (0.0, 0, 0, 5) n_gold 5 n_pred 0
   ADV (0.0, 0, 0, 12) n_gold 12 n_pred 0
   GN (0.4751, 100, 73, 148) n_gold 248 n_pred 173
   GP (0.8095, 34, 12, 4) n_gold 38 n_pred 46
   GV (0.6061, 140, 101, 81) n_gold 221 n_pred 241
   PONCT (0.0, 0, 0, 2) n_gold 2 n_pred 0
   REL (0.55, 11, 12, 6) n_gold 17 n_pred 23
   SUB (0.76, 19, 7, 5) n_gold 24 n_pred 26
  ```

### 🤖 Assistant

⏵ Ajout des contrôles statistiques (équilibre, hypergéométrie, Monte-Carlo)

- **write** `{"content": "\"\"\"Enrichit /tmp/dev-test-v7.json de contrôles : équilibre, hypergéométrie, Monte-Carlo, Wilson.\"\"\"\nfrom __future__ import annotations\n\nimport collections\nimport json\nimport math\nimport pathlib\nimport random\nimport sys\nimport zlib\n\nRACINE = pathlib.Path(\"/home/stephane … [15075 caractères tronqués]`

  ```
<path>/tmp/enrichir.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/enrichir.py'\ns=open(p).read()\nstart=s.index('        obs = [d[\"splits\"][n][\"test\"]')\nend=s.index('        obs = []\\n', start)\ns=s[:start]+s[end:]\nopen(p,'w').write(s)\nprint(\"nettoyé\")\nPY\npython3 /tmp/enrichir.py", "description": "Run e … [55 caractères tronqués]`

  ```
nettoyé
par phrase : 239 cibles, 196 labels, 195 exact — ok
Monte-Carlo : {
 "exact_taux_span": {
  "observe_3_splits": [
   1.0,
   1.0,
   0.9828
  ],
  "observe_etendue": 0.0172,
  "monte_carlo_etendue": {
   "p05": 0.0125,
   "p50": 0.0152,
   "p95": 0.0185
  },
  "monte_carlo_valeur": {
   "p05": 0.9828,
   "p50": 1.0,
   "p95": 1.0
  },
  "dans_intervalle_95": true
 },
 "couverture": {
  "observe_3_splits": [
   0.8158,
   0.8539,
   0.7838
  ],
  "observe_etendue": 0.0701,
  "monte_carlo_etendue": {
   "p05": 0.0195,
   "p50": 0.0678,
   "p95": 0.1445
  },
  "monte_carlo_valeur": {
   "p05": 0.7614,
   "p50": 0.8202,
   "p95": 0.878
  },
  "dans_intervalle_95": true
 },
 "f1": {
  "observe_3_splits": [
   0.5651,
   0.5598,
   0.541
  ],
  "observe_etendue": 0.0241,
  "monte_carlo_etendue": {
   "p05": 0.01,
   "p50": 0.0361,
   "p95": 0.0772
  },
  "monte_carlo_valeur": {
   "p05": 0.5243,
   "p50": 0.5557,
   "p95": 0.5866
  },
  "dans_intervalle_95": true
 },
 "tete_f1": {
  "observe_3_splits": [
   0.7196,
   0.718,
   0.7076
  ],
  "observe_etendue": 0.012,
  "monte_carlo_etendue": {
   "p05": 0.0072,
   "p50": 0.026,
   "p95": 0.0555
  },
  "monte_carlo_valeur": {
   "
… [772 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"import scipy; print(scipy.__version__)\" 2>&1 | head -2", "description": "Check scipy availability"}`

  ```
1.18.1
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/enrichir.py'\ns=open(p).read()\nold='''    df = len(attendu) - 1\n    if df == 1:\n        p = math.erfc(math.sqrt(x2 / 2))\n    elif df == 2:\n        p = math.exp(-x2 / 2)\n    else:\n        raise ValueError(df)\n'''\nnew='''    df = len(attendu)  … [254 caractères tronqués]`

  ```
ok
  "attendu": {
   "hand": 6.21,
   "reel": 134.12,
   "synthetique": 49.67
  }
 },
 "langues": {
  "chi2": 0.0009,
  "ddl": 1,
  "p": 0.9761,
  "observe": {
   "fr": 125,
   "en": 65
  },
  "attendu": {
   "fr": 124.8,
   "en": 65.2
  }
 },
 "types_cibles": {
  "chi2": 2.6613,
  "ddl": 2,
  "p": 0.2643,
  "observe": {
   "GP": 35,
   "REL": 17,
   "SUB": 24
  },
  "attendu": {
   "GP": 30.53,
   "SUB": 21.94,
   "REL": 23.53
  }
 },
 "types_langues": {
  "chi2": 3.4887,
  "ddl": 5,
  "p": 0.6251,
  "observe": {
   "GP/fr": 24,
   "GP/en": 11,
   "REL/fr": 12,
   "REL/en": 5,
   "SUB/fr": 14,
   "SUB/en": 10
  },
  "attendu": {
   "GP/fr": 19.72,
   "SUB/fr": 13.67,
   "REL/fr": 14.63,
   "GP/en": 10.81,
   "SUB/en": 8.27,
   "REL/en": 8.9
  }
 }
}
hyper: {"canonique": {"cibles_test": 76, "perdus_observes": 14, "perdus_attendus": 13.67, "ecart_type": 2.77, "z": 0.12}, "decale1": {"cibles_test": 89, "perdus_observes": 13, "perdus_attendus": 16.01, "ecart_type": 2.88, "z": -1.05}, "decale2": {"cibles_test": 74, "perdus_observes": 16, "perdus_attendus": 13.31, "ecart_type": 2.75, "z": 0.98}, "total": {"cibles": 239, "perdus": 43, "par_type": {"REL": 21, "SUB": 17, "GP": 5}}}
wilson 
… [1909 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Récapitulatif des contrôles pour la fiche

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/pensee-dev-test-v7.json'))\nprint(\"taille JSON\", len(json.dumps(d)), \"octets\")\nfor n in (\"canonique\",\"decale1\",\"decale2\"):\n    s=d[\"splits\"][n]\n    print(\"\\n\",n, s[\"regle\"], \"test phrases\", s[\"test\"][\"phrases … [812 caractères tronqués]`

  ```
taille JSON 40586 octets

 canonique crc32(id)%3==0 -> test test phrases 190 cibles 76
  chi2 p: {'sources': 0.6272, 'langues': 0.9761, 'types_cibles': 0.2643, 'types_langues': 0.6251}
  mix types test %: {'GP': 46.05, 'REL': 22.37, 'SUB': 31.58}

 decale1 crc32(id)%3==1 -> test test phrases 229 cibles 89
  chi2 p: {'sources': 0.4216, 'langues': 0.9532, 'types_cibles': 0.6178, 'types_langues': 0.9629}
  mix types test %: {'GP': 40.45, 'SUB': 24.72, 'REL': 34.83}

 decale2 crc32(id)%3==2 -> test test phrases 193 cibles 74
  chi2 p: {'sources': 0.5156, 'langues': 0.9727, 'types_cibles': 0.5241, 'types_langues': 0.8729}
  mix types test %: {'GP': 33.78, 'SUB': 31.08, 'REL': 35.14}

STABILITE
  dev_exact_taux_span      [0.9925, 0.9917, 1.0] etendue 0.0083
  dev_couverture           [0.8221, 0.8, 0.8364] etendue 0.0364
  dev_f1                   [0.5512, 0.5529, 0.5622] etendue 0.011
  dev_tete_f1              [0.7132, 0.7135, 0.7187] etendue 0.0055
  dev_pos                  [0.7547, 0.7602, 0.7596] etendue 0.0055
  test_exact_taux_span     [1.0, 1.0, 0.9828] etendue 0.0172
  test_couverture          [0.8158, 0.8539, 0.7838] etendue 0.0701
  test_f1                  [0.5651, 0.5598, 0.
… [1087 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle des croisements source×langue et F1 par langue

- **bash** `{"command": "python3 - <<'PY'\nimport sys, zlib, collections\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger\nph=charger()\ndef tab(sous):\n    return dict(collections.Counter(f'{p.get(\"source\")}/{p.get(\"langue\")}' for p in sous))\nprint(\"global:\", tab(ph))\n … [807 caractères tronqués]`

  ```
global: {'hand/fr': 14, 'hand/en': 6, 'reel/fr': 228, 'reel/en': 204, 'synthetique/fr': 160}
split 0 dev {'hand/fr': 11, 'hand/en': 4, 'reel/fr': 161, 'reel/en': 141, 'synthetique/fr': 105} test {'hand/fr': 3, 'hand/en': 2, 'reel/fr': 67, 'reel/en': 63, 'synthetique/fr': 55}
split 1 dev {'hand/fr': 4, 'hand/en': 5, 'reel/fr': 146, 'reel/en': 126, 'synthetique/fr': 102} test {'hand/fr': 10, 'hand/en': 1, 'reel/fr': 82, 'reel/en': 78, 'synthetique/fr': 58}
split 2 dev {'hand/fr': 13, 'hand/en': 3, 'reel/fr': 149, 'reel/en': 141, 'synthetique/fr': 113} test {'hand/fr': 1, 'hand/en': 3, 'reel/fr': 79, 'reel/en': 63, 'synthetique/fr': 47}
dev cibles source/type {'hand/GP': 7, 'hand/REL': 1, 'hand/SUB': 2, 'reel/GP': 43, 'reel/REL': 45, 'reel/SUB': 33, 'synthetique/GP': 11, 'synthetique/REL': 11, 'synthetique/SUB': 10}
test cibles source/type {'hand/GP': 3, 'reel/GP': 19, 'reel/REL': 12, 'reel/SUB': 19, 'synthetique/GP': 13, 'synthetique/REL': 5, 'synthetique/SUB': 5}
  ```

- **bash** `{"command": "cat > /tmp/complement.py <<'PY'\nimport sys, json, zlib, collections, pathlib\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nfrom tools.tests.linguistique.evaluer_gold import charger\nimp … [3475 caractères tronqués]`

  ```
ok
{"fr": {"syntagme": {"precision": 0.5581, "rappel": 0.536, "f1": 0.5468, "tp": 432, "fp": 342, "fn": 374}, "tete": {"precision": 0.7379, "rappel": 0.6638, "f1": 0.6989, "tp": 535, "fp": 190, "fn": 271}, "pos": 0.7558, "tokens": 1384}, "en": {"syntagme": {"precision": 0.6793, "rappel": 0.4755, "f1": 0.5594, "tp": 233, "fp": 110, "fn": 257}, "tete": {"precision": 0.898, "rappel": 0.6286, "f1": 0.7395, "tp": 308, "fp": 35, "fn": 182}, "pos": 0.7528, "tokens": 801}}
{"fr": {"syntagme": {"precision": 0.5562, "rappel": 0.5718, "f1": 0.5639, "tp": 203, "fp": 162, "fn": 152}, "tete": {"precision": 0.7365, "rappel": 0.693, "f1": 0.7141, "tp": 246, "fp": 88, "fn": 109}, "pos": 0.7512, "tokens": 647}, "en": {"syntagme": {"precision": 0.7014, "rappel": 0.4764, "f1": 0.5674, "tp": 101, "fp": 43, "fn": 111}, "tete": {"precision": 0.9028, "rappel": 0.6132, "f1": 0.7303, "tp": 130, "fp": 14, "fn": 82}, "pos": 0.7925, "tokens": 347}}
croisements canonical: {"dev": {"source_langue_phrases": {"hand/fr": 11, "hand/en": 4, "reel/fr": 161, "reel/en": 141, "synthetique/fr": 105}, "source_type_cibles": {"hand/GP": 7, "hand/SUB": 2, "hand/REL": 1, "reel/GP": 43, "reel/REL": 45, "reel/SUB": 33, "syntheti
… [539 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Nettoyage des champs ambigus et régénération du JSON final

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/mesure_dev_test_v7.py'\ns=open(p).read()\ns=s.replace('''    return {\"cibles\": 0, \"labels\": 0, \"exact\": 0, \"exact_any\": 0, \"phrases\": 0,\n            \"tp\": 0, \"fp\": 0, \"fn\": 0, \"ttp\": 0, \"tfp\": 0, \"tfn\": 0}''',\n'''    return {\ … [1860 caractères tronqués]`

  ```
patché
  test: {"hand": 11, "reel": 160, "synthetique": 58} {"fr": 150, "en": 79} {"GP": 36, "SUB": 22, "REL": 31}
decale2 absentes: {'sources': [], 'langues': [], 'types': [], 'types_langues': []}
  dev: {"hand": 16, "reel": 290, "synthetique": 113} {"fr": 275, "en": 144} {"GP": 71, "SUB": 46, "REL": 48}
  test: {"hand": 4, "reel": 142, "synthetique": 47} {"fr": 127, "en": 66} {"GP": 25, "SUB": 23, "REL": 26}
wilson exact: {"dev_exact": {"k": 133, "n": 134, "taux": 0.9925, "wilson95": [0.9589, 0.9987]}, "test_exact": {"k": 62, "n": 62, "taux": 1.0, "wilson95": [0.9417, 1.0]}, "dev_exact_fr": {"k": 92, "n": 92, "taux": 1.0, "wilson95": [0.9599, 1.0]}, "test_exact_fr": {"k": 43, "n": 43, "taux": 1.0, "wilson95": [0.918, 1.0]}, "dev_exact_en": {"k": 41, "n": 42, "taux": 0.9762, "wilson95": [0.8768, 0.9958]}, "test_exact_en": {"k": 19, "n": 19, "taux": 1.0, "wilson95": [0.8318, 1.0]}, "dev_exact_REL": {"k": 42, "n": 42, "taux": 1.0, "wilson95": [0.9162, 1.0]}, "test_exact_REL": {"k": 11, "n": 11, "taux": 1.0, "wilson95": [0.7412, 1.0]}, "dev_exact_SUB": {"k": 33, "n": 33, "taux": 1.0, "wilson95": [0.8957, 1.0]}, "test_exact_SUB": {"k": 19, "n": 19, "taux": 1.0, "wilson95": [0.8318, 1.
… [2240 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/pensee-dev-test-v7.json'))\ns=d[\"splits\"][\"canonique\"][\"dev\"]\nprint(list(s))\nprint(json.dumps({k:s[k] for k in (\"phrases\",\"tokens\",\"pos\",\"syntagme\",\"tete\",\"acte\",\"attachement\",\"par_langue\",\"par_type\",\"par_l … [202 caractères tronqués]`

  ```
['phrases', 'tokens', 'pos', 'syntagme', 'tete', 'acte', 'attachement', 'par_langue', 'par_type', 'par_type_langue', 'par_source', 'spans_perdus', 'par_langue_f1']
{
 "phrases": 422,
 "tokens": 2185,
 "pos": {
  "exactitude": 0.7547,
  "ferme": 0.8952,
  "ouvert": 0.6201,
  "tokens": 2185
 },
 "syntagme": {
  "precision": 0.5953,
  "rappel": 0.5131,
  "f1": 0.5512,
  "tp": 665,
  "fp": 452,
  "fn": 631
 },
 "tete": {
  "precision": 0.7893,
  "rappel": 0.6505,
  "f1": 0.7132,
  "tp": 843,
  "fp": 225,
  "fn": 453
 },
 "acte": 1.0,
 "attachement": {
  "cibles": 163,
  "labels": 134,
  "exact": 133,
  "exact_any": 133,
  "tp": 0,
  "fp": 0,
  "fn": 0,
  "ttp": 0,
  "tfp": 0,
  "tfn": 0,
  "couverture": 0.8221,
  "exact_taux_span": 0.9925,
  "exact_taux_cibles": 0.816,
  "exact_any_taux_span": 0.9925
 },
 "par_langue": {
  "fr": {
   "cibles": 101,
   "labels": 92,
   "exact": 92,
   "exact_any": 92,
   "tp": 0,
   "fp": 0,
   "fn": 0,
   "ttp": 0,
   "tfp": 0,
   "tfn": 0,
   "couverture": 0.9109,
   "exact_taux_span": 1.0,
   "exact_taux_cibles": 0.9109,
   "exact_any_taux_span": 1.0
  },
  "en": {
   "cibles": 62,
   "labels": 42,
   "exact": 41,
   "exact_any": 41,
   "tp": 0,
   "
… [3225 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/mesure_dev_test_v7.py'\ns=open(p).read()\n# ajouter finir_att\nold='''    def finir(b: dict) -> dict:\n        d = dict(b)\n        d[\"couverture\"] = round(b[\"labels\"] / max(1, b[\"cibles\"]), 4)\n        d[\"exact_taux_span\"] = round(b[\"exact\ … [4227 caractères tronqués]`

  ```
mesure patché
enrichir patché
  dev: {"hand": 16, "reel": 290, "synthetique": 113} {"fr": 275, "en": 144} {"GP": 71, "SUB": 46, "REL": 48}
  test: {"hand": 4, "reel": 142, "synthetique": 47} {"fr": 127, "en": 66} {"GP": 25, "SUB": 23, "REL": 26}
corpus: {"vivant": {"phrases": 612, "cibles": 239, "labels": 196, "exact": 195, "couverture": 0.8201, "f1": 0.5555, "tete": 0.7152, "pos": 0.7581}, "gele": {"phrases": 602, "cibles": 239, "labels": 196, "exact": 195, "couverture": 0.8201, "f1": 0.5595, "tete": 0.7205, "pos": 0.7603}, "note": "les 10 phrases réelles ajoutées au vivant après le gel n'ont pas de cibles : mêmes 239 cibles, 196 labels, 195 exact ; seules F1/tête/POS bougent"}
croisements canonical: {"dev": {"source_langue_phrases": {"hand/fr": 11, "hand/en": 4, "reel/fr": 161, "reel/en": 141, "synthetique/fr": 105}, "source_type_cibles": {"hand/GP": 7, "hand/SUB": 2, "hand/REL": 1, "reel/GP": 43, "reel/REL": 45, "reel/SUB": 33, "synthetique/GP": 11, "synthetique/REL": 11, "synthetique/SUB": 10}, "type_langue_cibles": {"GP/fr": 38, "SUB/fr": 29, "REL/fr": 34, "GP/en": 23, "SUB/en": 16, "REL/en": 23}}, "test": {"source_langue_phrases": {"hand/fr": 3, "hand/en": 2, "reel/fr": 67, "
… [730 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction des chiffres définitifs pour la fiche

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/pensee-dev-test-v7.json'))\nfor n in (\"canonique\",\"decale1\",\"decale2\"):\n    print(\"#\",n)\n    for moitie in (\"dev\",\"test\"):\n        m=d[\"splits\"][n][moitie]; a=m[\"attachement\"]\n        print(f\" {moitie}: {m['phras … [1999 caractères tronqués]`

  ```
# canonique
 dev: 422 phr 2185 tok | cibles 163 labels 134 exact 133 | couv 0.8221 exact/span 0.9925 exact/cibles 0.816 | F1 0.5512 P 0.5953 R 0.5131 | tete 0.7132 | POS 0.7547 | acte 1.0
  par langue: {'fr': (101, 92, 92, 0.9109, 1.0), 'en': (62, 42, 41, 0.6774, 0.9762)}
  F1 langue: {'fr': (0.5468, 0.6989, 0.7558), 'en': (0.5594, 0.7395, 0.7528)}
  par type: {'REL': (57, 42, 42, 0.7368, 1.0, 0.6176, 0.9016), 'SUB': (45, 33, 33, 0.7333, 1.0, 0.7727, 0.9091), 'GP': (61, 59, 58, 0.9672, 0.9831, 0.8497, 0.8609)}
  type/langue: {'REL/fr': (34, 29, 29, 0.8529, 1.0), 'REL/en': (23, 13, 13, 0.5652, 1.0), 'SUB/fr': (29, 27, 27, 0.931, 1.0), 'SUB/en': (16, 6, 6, 0.375, 1.0), 'GP/fr': (38, 36, 36, 0.9474, 1.0), 'GP/en': (23, 23, 22, 1.0, 0.9565)}
  spans perdus: {'SUB': 12, 'REL': 15, 'GP': 2}
 test: 190 phr 994 tok | cibles 76 labels 62 exact 62 | couv 0.8158 exact/span 1.0 exact/cibles 0.8158 | F1 0.5651 P 0.5972 R 0.5362 | tete 0.7196 | POS 0.7656 | acte 0.9895
  par langue: {'fr': (50, 43, 43, 0.86, 1.0), 'en': (26, 19, 19, 0.7308, 1.0)}
  F1 langue: {'fr': (0.5639, 0.7141, 0.7512), 'en': (0.5674, 0.7303, 0.7925)}
  par type: {'REL': (17, 11, 11, 0.6471, 1.0, 0.55, 0.9444), 'SUB': (24, 
… [8363 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de l'échec unique dans la fiche v5 avant de l'affirmer

- **bash** `{"command": "grep -n \"r102\\|échec\\|echec\" reports/rapport-pensee-couverture-v5.md | head -30; echo ===; git log --oneline -3 -- reports/pensee-couverture-v5.json", "description": "Check v5 report for the failing phrase", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
40:| échecs de cible | 3 | **1** (r309) |
47:- **Les 27 échecs de cible** sont le prix de la couverture : les REL/SUB nouvelles sont plus
53:- **Les 27 échecs** : à qualifier (REL sans antécédent, GP, SUB en tête).
63:- **les règles ont été réglées en regardant les échecs** : le test limite le surajustement, il
70:2. **Les 27 échecs de cible** : qualifier.
===
b975011b B13 — LES CANDIDATS DU PRÉCÉDENT : EXACT 186/187 (0,9947), ANGLAIS 60/60, DEV 126/126 ; 183/183
7a9f0d6a B13 — LA COUVERTURE : 187 LABELS, EXACT 185/187 (0,9893), F1 0,5156, DEV 125/126 ET TEST 60/61 ; 183/183
  ```

- **bash** `{"command": "cd /tmp && git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet show b975011b:tools/bloc_linguistique.py > /tmp/bloc_v5.py && python3 - <<'PY'\nimport sys, importlib.util, zlib, collections\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nsys.path.insert(0,'/home … [2424 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 7, in <module>
  File "<frozen importlib._bootstrap_external>", line 1027, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/tmp/bloc_v5.py", line 58, in <module>
    @dataclass(frozen=True)
     ~~~~~~~~~^^^^^^^^^^^^^
  File "/usr/lib64/python3.13/dataclasses.py", line 1344, in wrap
    return _process_class(cls, init, repr, eq, order, unsafe_hash,
                          frozen, match_args, kw_only, slots,
                          weakref_slot)
  File "/usr/lib64/python3.13/dataclasses.py", line 997, in _process_class
    and _is_type(type, cls, dataclasses, dataclasses.KW_ONLY,
        ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                 _is_kw_only))):
                 ^^^^^^^^^^^^
  File "/usr/lib64/python3.13/dataclasses.py", line 757, in _is_type
    ns = sys.modules.get(cls.__module__).__dict__
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute '__dict__'. Did you mean: '__dir__'?
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport sys, importlib.util\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nfrom tools.tests.linguistique.evaluer_gold import charger\nimport tools.bloc_linguis … [2240 caractères tronqués]`

  ```
v5 chargé True
v5 labels 187 exact 186 | v7 labels 196 exact 195
r309 v5 {('SUB', 10, 23): ('Peut-être', False, 'viendra', 'r309')} v7 {('SUB', 10, 23): ('viendra', True, 'viendra', 'r309')}
r102 v5 {('GP', 15, 33): None} v7 {('GP', 15, 33): ('', False, 'falls', 'r102')}
gagnés 21 dont exacts 20
perdus 12 dont exacts 12
changés 1
 + ('r025', ('GP', 10, 24), ('talks', True, 'talks', 'r025'))
 + ('r026', ('GP', 20, 34), ('listen', True, 'listen', 'r026'))
 + ('r027', ('GP', 15, 27), ('sleeps', True, 'sleeps', 'r027'))
 + ('r028', ('GP', 9, 24), ('rains', True, 'rains', 'r028'))
 + ('r060', ('GP', 19, 35), ('volent', True, 'volent', 'r060'))
 + ('r068', ('GP', 19, 32), ('writes', True, 'writes', 'r068'))
 + ('r083', ('GP', 15, 22), ('entre', True, 'entre', 'r083'))
 + ('r102', ('GP', 15, 33), ('', False, 'falls', 'r102'))
 + ('r156', ('GP', 15, 27), ('swims', True, 'swims', 'r156'))
 + ('r160', ('GP', 19, 33), ('passes', True, 'passes', 'r160'))
 + ('r169', ('GP', 16, 29), ('smiles', True, 'smiles', 'r169'))
 + ('r204', ('REL', 8, 18), ('man', True, 'man', 'r204'))
 + ('r217', ('REL', 12, 26), ('student', True, 'student', 'r217'))
 + ('r248', ('REL', 9, 25), ('girl', True, 'girl', 'r2
… [1302 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport zlib\nfor i in (\"r309\",\"r102\"):\n    print(i, zlib.crc32(i.encode())%3)\nPY", "description": "Check buckets of v5 and v7 errors"}`

  ```
r309 0
r102 2
  ```

### 🤖 Assistant

⏵ Correction de la comparaison v5→v7 (r309 corrigé, r102 nouveau)

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/enrichir.py'\ns=open(p).read()\nold='''    v5 = json.load(open(RACINE / \"reports/pensee-couverture-v5.json\"))[\"dev\"]\n    d[\"comparaison_v5\"] = {\n        \"v5\": {\"labels\": 187, \"exact\": 186, \"dev\": \"126/126\", \"test\": \"60/61\"},\n   … [1962 caractères tronqués]`

  ```
patché
corpus: {"vivant": {"phrases": 612, "cibles": 239, "labels": 196, "exact": 195, "couverture": 0.8201, "f1": 0.5555, "tete": 0.7152, "pos": 0.7581}, "gele": {"phrases": 602, "cibles": 239, "labels": 196, "exact": 195, "couverture": 0.8201, "f1": 0.5595, "tete": 0.7205, "pos": 0.7603}, "note": "les 10 phrases réelles ajoutées au vivant après le gel n'ont pas de cibles : mêmes 239 cibles, 196 labels, 195 exact ; seules F1/tête/POS bougent"}
croisements canonical: {"dev": {"source_langue_phrases": {"hand/fr": 11, "hand/en": 4, "reel/fr": 161, "reel/en": 141, "synthetique/fr": 105}, "source_type_cibles": {"hand/GP": 7, "hand/SUB": 2, "hand/REL": 1, "reel/GP": 43, "reel/REL": 45, "reel/SUB": 33, "synthetique/GP": 11, "synthetique/REL": 11, "synthetique/SUB": 10}, "type_langue_cibles": {"GP/fr": 38, "SUB/fr": 29, "REL/fr": 34, "GP/en": 23, "SUB/en": 16, "REL/en": 23}}, "test": {"source_langue_phrases": {"hand/fr": 3, "hand/en": 2, "reel/fr": 67, "reel/en": 63, "synthetique/fr": 55}, "source_type_cibles": {"hand/GP": 3, "reel/REL": 12, "reel/GP": 19, "reel/SUB": 19, "synthetique/GP": 13, "synthetique/REL": 5, "synthetique/SUB": 5}, "type_langue_cibles": {"GP/fr": 24, "GP/en": 11, "R
… [780 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger\nph=charger()\nfor src in (\"hand\",\"reel\",\"synthetique\"):\n    c=collections.Counter(f'{p.get(\"langue\")}/{s[\"type\"]}' for p in ph if p.get(\"source\")==s … [247 caractères tronqués]`

  ```
hand {'fr/GP': 8, 'fr/SUB': 1, 'fr/REL': 1, 'en/GP': 2, 'en/SUB': 1} total 13
reel {'fr/GP': 30, 'fr/REL': 29, 'en/GP': 32, 'en/REL': 28, 'fr/SUB': 27, 'en/SUB': 25} total 171
synthetique {'fr/GP': 24, 'fr/REL': 16, 'fr/SUB': 15} total 55
  ```

### 🤖 Assistant

⏵ Ajout des métadonnées de méthode au JSON final

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/complement.py'\ns=open(p).read()\nold='''d[\"controles\"][\"croisements\"]=c\n'''\nnew='''d[\"controles\"][\"croisements\"]=c\nd[\"date\"]=\"2026-11-05\"\nd[\"ligne\"]=\"B13\"\nd[\"objet\"]=\"re-mesure dev/test du gold 612 et robustesse du split sur  … [1324 caractères tronqués]`

  ```
ok
croisements canonical: {"dev": {"source_langue_phrases": {"hand/fr": 11, "hand/en": 4, "reel/fr": 161, "reel/en": 141, "synthetique/fr": 105}, "source_type_cibles": {"hand/GP": 7, "hand/SUB": 2, "hand/REL": 1, "reel/GP": 43, "reel/REL": 45, "reel/SUB": 33, "synthetique/GP": 11, "synthetique/REL": 11, "synthetique/SUB": 10}, "type_langue_cibles": {"GP/fr": 38, "SUB/fr": 29, "REL/fr": 34, "GP/en": 23, "SUB/en": 16, "REL/en": 23}}, "test": {"source_langue_phrases": {"hand/fr": 3, "hand/en": 2, "reel/fr": 67, "reel/en": 63, "synthetique/fr": 55}, "source_type_cibles": {"hand/GP": 3, "reel/REL": 12, "reel/GP": 19, "reel/SUB": 19, "synthetique/GP": 13, "synthetique/REL": 5, "synthetique/SUB": 5}, "type_langue_cibles": {"GP/fr": 24, "GP/en": 11, "REL/fr": 12, "REL/en": 5, "SUB/fr": 14, "SUB/en": 10}}}
['commit', 'valide_contre_evaluer_gold', 'validation', 'analyses_secondes', 'equilibre_global', 'splits', 'ecart_dev_test', 'stabilite']
{
 "date": "2026-11-05",
 "ligne": "B13",
 "objet": "re-mesure dev/test du gold 612 et robustesse du split sur trois découpages (commit 69bd865e)",
 "commit": "69bd865e",
 "methode": {
  "corpus": "gold vivant 612 = 20 hand + 432 reel + 160 synthetique ;
… [676 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/pensee-dev-test-v7.json'))\nfor n in (\"canonique\",\"decale1\",\"decale2\"):\n    print(n)\n    for k,v in d[\"splits\"][n][\"equilibre\"][\"chi2_test\"].items():\n        print(\" \",k,\"chi2\",v[\"chi2\"],\"ddl\",v[\"ddl\"],\"p\", … [113 caractères tronqués]`

  ```
canonique
  sources chi2 0.9331 ddl 2 p 0.6272 obs {'hand': 5, 'reel': 130, 'synthetique': 55} att {'hand': 6.21, 'reel': 134.12, 'synthetique': 49.67}
  langues chi2 0.0009 ddl 1 p 0.9761 obs {'fr': 125, 'en': 65} att {'fr': 124.8, 'en': 65.2}
  types_cibles chi2 2.6613 ddl 2 p 0.2643 obs {'GP': 35, 'REL': 17, 'SUB': 24} att {'GP': 30.53, 'SUB': 21.94, 'REL': 23.53}
  types_langues chi2 3.4887 ddl 5 p 0.6251 obs {'GP/fr': 24, 'GP/en': 11, 'REL/fr': 12, 'REL/en': 5, 'SUB/fr': 14, 'SUB/en': 10} att {'GP/fr': 19.72, 'SUB/fr': 13.67, 'REL/fr': 14.63, 'GP/en': 10.81, 'SUB/en': 8.27, 'REL/en': 8.9}
decale1
  sources chi2 1.7274 ddl 2 p 0.4216 obs {'hand': 11, 'reel': 160, 'synthetique': 58} att {'hand': 7.48, 'reel': 161.65, 'synthetique': 59.87}
  langues chi2 0.0034 ddl 1 p 0.9532 obs {'fr': 150, 'en': 79} att {'fr': 150.42, 'en': 78.58}
  types_cibles chi2 0.9633 ddl 2 p 0.6178 obs {'GP': 36, 'SUB': 22, 'REL': 31} att {'GP': 35.75, 'SUB': 25.69, 'REL': 27.56}
  types_langues chi2 0.9961 ddl 5 p 0.9629 obs {'GP/fr': 23, 'SUB/fr': 14, 'REL/fr': 19, 'GP/en': 13, 'REL/en': 12, 'SUB/en': 8} att {'GP/fr': 23.09, 'SUB/fr': 16.01, 'REL/fr': 17.13, 'GP/en': 12.66, 'SUB/en': 9.68, 'REL/en': 10
… [605 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction de la fiche `reports/rapport-dev-test-v7.md`

- **bash** `{"command": "ls -l reports/rapport-dev-test-v7.md reports/pensee-dev-test-v7.json 2>&1 | head", "description": "Confirm target files do not exist", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
ls: cannot access 'reports/rapport-dev-test-v7.md': No such file or directory
ls: cannot access 'reports/pensee-dev-test-v7.json': No such file or directory
  ```

- **write** `{"content": "# B13 — dev/test en v7 : dev 133/134, test 62/62, le split tient sur trois découpages\n\n> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Commit mesuré** : `69bd865e` · **Verdict** : ✅\n> Le gold 612 est re-coupé par `crc32(id) % 3 == 0` (test) :  … [14502 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v7.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Relecture de la fiche et vérification des chiffres

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v7.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v7.md</path>
<type>file</type>
<content>
1: # B13 — dev/test en v7 : dev 133/134, test 62/62, le split tient sur trois découpages
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Commit mesuré** : `69bd865e` · **Verdict** : ✅
4: > Le gold 612 est re-coupé par `crc32(id) % 3 == 0` (test) : **dev 133/134 (0,9925)**, **test 62/62 (1,0)**
5: > — mais le test ne couvre que **62 des 76 cibles** (0,8158). En décalant le split (`%3==1`, `%3==2`),
6: > l'exact reste à **1 cas près** (étendue 0,0172), la couverture à **3 spans près** (14/13/16 des 43),
7: > la F1 à **2,4 points**. **Aucune catégorie demandée n'est absente** ; les écarts dev/test tiennent à
8: > **un échec unique (r102)** et à la **composition par type**, pas au split.
9: >
10: > **Dispositif** : [`gold_split.py`](../tools/tests/linguistique/gold_split.py) (`dev`, `test`, `compter`),
11: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`),
12: > [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (heuristique) ; JSON
13: > [`pensee-dev-test-v7.json`](pense
… [14437 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Correction de la fiche (quatre réserves, part GN/GV) et ajout des contrôles F1 au JSON

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/complement.py'\ns=open(p).read()\nold='''d[\"controles\"][\"croisements\"]=c\n'''\nnew='''d[\"controles\"][\"croisements\"]=c\nd[\"controles\"][\"f1_gn_gv\"]={\n \"dev\":{\"GN\":{\"f1\":0.4827,\"gold\":580,\"pred\":373},\"GV\":{\"f1\":0.5720,\"gold\" … [1877 caractères tronqués]`

  ```
patché
croisements canonical: {"dev": {"source_langue_phrases": {"hand/fr": 11, "hand/en": 4, "reel/fr": 161, "reel/en": 141, "synthetique/fr": 105}, "source_type_cibles": {"hand/GP": 7, "hand/SUB": 2, "hand/REL": 1, "reel/GP": 43, "reel/REL": 45, "reel/SUB": 33, "synthetique/GP": 11, "synthetique/REL": 11, "synthetique/SUB": 10}, "type_langue_cibles": {"GP/fr": 38, "SUB/fr": 29, "REL/fr": 34, "GP/en": 23, "SUB/en": 16, "REL/en": 23}}, "test": {"source_langue_phrases": {"hand/fr": 3, "hand/en": 2, "reel/fr": 67, "reel/en": 63, "synthetique/fr": 55}, "source_type_cibles": {"hand/GP": 3, "reel/REL": 12, "reel/GP": 19, "reel/SUB": 19, "synthetique/GP": 13, "synthetique/REL": 5, "synthetique/SUB": 5}, "type_langue_cibles": {"GP/fr": 24, "GP/en": 11, "REL/fr": 12, "REL/en": 5, "SUB/fr": 14, "SUB/en": 10}}}
f1_gn_gv {"dev": {"GN": {"f1": 0.4827, "gold": 580, "pred": 373}, "GV": {"f1": 0.572, "gold": 491, "pred": 537}, "part_gold_gn_gv": 0.8264}, "test": {"GN": {"f1": 0.4751, "gold": 248, "pred": 173}, "GV": {"f1": 0.6061, "gold": 221, "pred": 241}, "part_gold_gn_gv": 0.8272}, "note": "F1 micro sur GN/GV, les deux types qui dominent l'agrégat ; REL/SUB/GP ne font que ~17 % des segments go
… [410 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/complement.py'\ns=open(p).read()\ns=s.replace('\"note\":\"le test, ramené au mélange de cibles du dev, couvrirait 0,7869 ; son brut 0,8158 est tiré par les GP\"',\n            '\"note\":\"le test, ramené au mélange de cibles du dev, couvrirait 0,7870 … [246 caractères tronqués]`

  ```
ok
croisements canonical: {"dev": {"source_langue_phrases": {"hand/fr": 11, "hand/en": 4, "reel/fr": 161, "reel/en": 141, "synthetique/fr": 105}, "source_type_cibles": {"hand/GP": 7, "hand/SUB": 2, "hand/REL": 1, "reel/GP": 43, "reel/REL": 45, "reel/SUB": 33, "synthetique/GP": 11, "synthetique/REL": 11, "synthetique/SUB": 10}, "type_langue_cibles": {"GP/fr": 38, "SUB/fr": 29, "REL/fr": 34, "GP/en": 23, "SUB/en": 16, "REL/en": 23}}, "test": {"source_langue_phrases": {"hand/fr": 3, "hand/en": 2, "reel/fr": 67, "reel/en": 63, "synthetique/fr": 55}, "source_type_cibles": {"hand/GP": 3, "reel/REL": 12, "reel/GP": 19, "reel/SUB": 19, "synthetique/GP": 13, "synthetique/REL": 5, "synthetique/SUB": 5}, "type_langue_cibles": {"GP/fr": 24, "GP/en": 11, "REL/fr": 12, "REL/en": 5, "SUB/fr": 14, "SUB/en": 10}}}
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v7.md", "old_string": "| GP | 0,8497 | 0,8609 | 0,8095 | 0,8537 |\n\nLe croisement fin montre les cellules réellement minces :", "new_string": "| GP | 0,8497 | 0,8609 | 0,8095 | 0,8537 |\n\nLa F1 et la tête sont  … [231 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v7.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v7.md", "old_string": "Trois réserves de lecture, même sans catégorie absente :", "new_string": "Quatre réserves de lecture, même sans catégorie absente :"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v7.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v7.md", "old_string": "  76 cibles. Après standardisation sur la composition du dev, le test serait à **0,7869** (3,5 points\n  sous dev, ~2,7 cas pour 76), mais cette estimation n'est pas significative : les IC  … [445 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v7.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v7.md", "old_string": "- **F1** : test **+1,39 point**, mais l'agrégat est dominé par GN/GV (81 % des segments) : GV test", "new_string": "- **F1** : test **+1,39 point**, mais l'agrégat est dominé par GN/GV (83  … [32 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v7.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Publication du JSON et contrôle de l'état git

- **bash** `{"command": "cp /tmp/pensee-dev-test-v7.json reports/pensee-dev-test-v7.json && python3 -m json.tool reports/pensee-dev-test-v7.json >/dev/null && echo \"JSON valide\" && ls -l reports/rapport-dev-test-v7.md reports/pensee-dev-test-v7.json && git status --short reports/ && echo \"--- tracked diff na … [163 caractères tronqués]`

  ```
JSON valide
-rw-r--r--. 1 stephane stephane 61349  5 nov 20:10 reports/pensee-dev-test-v7.json
-rw-------. 1 stephane stephane 14980  5 nov 20:10 reports/rapport-dev-test-v7.md
 M reports/pensee-quatre-modes.json
 M reports/rapport-spans-chunker.md
?? reports/pensee-dev-test-v7.json
?? reports/rapport-coherence-fiches-v7.md
?? reports/rapport-dev-test-v7.md
?? reports/rapport-s-paragraphes.md
--- tracked diff names ---
journal/2026-11-05/README.md
journal/2026-11-05/distribue.md
journal/2026-11-05/docs.md
journal/2026-11-05/memoire.md
journal/2026-11-05/mesures.md
journal/2026-11-05/modele.md
journal/2026-11-05/moteur.md
journal/2026-11-05/portes.md
journal/README.md
journal/THEMES.md
journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rapport.md
journal/sessions/MANIFEST.md
journal/sessions/aeafe951-9c3d-4bb5-8af7-0246a4f3d51d/digest.md
journal/sessions/aeafe951-9c3d-4bb5-8af7-0246a4f3d51d/rapport.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/e181ce02-
… [71 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dédoublonnage des limites et régénération propre du JSON

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np='/tmp/complement.py'\ns=open(p).read()\nold='''pathlib.Path('/tmp/pensee-dev-test-v7.json').write_text(json.dumps(d,ensure_ascii=False,indent=1)+\"\\\\n\",encoding='utf-8')\n'''\nnew='''vus=set()\nd[\"limites\"]=[x for x in d[\"limites\"] if not (x in vus  … [777 caractères tronqués]`

  ```
patché
mesure-ok
enrichir-ok
complement-ok
limites: 7
 - in-sample : les règles v7 ont été dessinées sur ce gold, dev/test ne mesure pas le surajus
 - 160 phrases synthétiques sur 612 ; 20 seulement de gold.py
 - cellules petites : REL/en test = 5 cibles, hand test = 5 phrases
 - le hash n'est pas stratifié par construction ; l'équilibre est vérifié a posteriori
 - les 43 spans perdus restent hors de la mesure exact/labels (196/239)
 - cibles hand au test canonique : 3, toutes GP ; hand/REL (1) et hand/SUB (2) sont dans dev
 - synthétique = français seulement : source et langue sont confondues pour ces 160 phrases
taille chars 43704
  ```

- **bash** `{"command": "cp /tmp/pensee-dev-test-v7.json reports/pensee-dev-test-v7.json && chmod 644 reports/rapport-dev-test-v7.md reports/pensee-dev-test-v7.json && python3 -m json.tool reports/pensee-dev-test-v7.json >/dev/null && echo \"JSON valide\" && ls -l reports/rapport-dev-test-v7.md reports/pensee-d … [498 caractères tronqués]`

  ```
JSON valide
-rw-r--r--. 1 stephane stephane 60776  5 nov 20:11 reports/pensee-dev-test-v7.json
-rw-r--r--. 1 stephane stephane 14980  5 nov 20:10 reports/rapport-dev-test-v7.md
clés: ['commit', 'valide_contre_evaluer_gold', 'validation', 'analyses_secondes', 'equilibre_global', 'splits', 'ecart_dev_test', 'stabilite', 'resume', 'controles', 'wilson', 'wilson_couverture', 'corpus_vs_gele', 'comparaison_v5', 'limites', 'date', 'ligne', 'objet', 'methode']
splits: ['canonique', 'decale1', 'decale2']
controles: ['hypergeometrie_spans_perdus', 'bucket_sizes', 'echec_unique', 'monte_carlo', 'croisements', 'f1_gn_gv', 'couverture_standardisee', 'f1_ecart_par_type']
canonique dev: {'cibles': 163, 'labels': 134, 'exact': 133, 'exact_any': 133, 'couverture': 0.8221, 'exact_taux_span': 0.9925, 'exact_taux_cibles': 0.816, 'exact_any_taux_span': 0.9925}
canonique test: {'cibles': 76, 'labels': 62, 'exact': 62, 'exact_any': 62, 'couverture': 0.8158, 'exact_taux_span': 1.0, 'exact_taux_cibles': 0.8158, 'exact_any_taux_span': 1.0}
  ```

### 🤖 Assistant

⏵ Vérification finale : tableaux, liens et cohérence des chiffres

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path(\"reports/rapport-dev-test-v7.md\")\ns=p.read_text(encoding=\"utf-8\")\n# 1) tableaux : nombre de colonnes constant par tableau\nlignes=s.splitlines()\ni=0; problemes=[]\nwhile i < l … [691 caractères tronqués]`

  ```
tableaux incohérents: aucun
OK ../tools/tests/linguistique/gold_split.py
OK ../tools/tests/linguistique/evaluer_gold.py
OK ../tools/bloc_linguistique.py
OK pensee-dev-test-v7.json
OK rapport-pensee-couverture-v7.md
OK ../tools/tests/linguistique/gold_split.py
OK ../tools/tests/linguistique/evaluer_gold.py
OK ../tools/bloc_linguistique.py
OK pensee-dev-test-v7.json
OK rapport-gold-split.md
OK rapport-pensee-couverture-v7.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path(\"reports/rapport-dev-test-v7.md\")\ns=p.read_text(encoding=\"utf-8\")\ns=s.replace(\"(83 % des segments gold)\", \"(82,7 % des segments gold)\")\np.write_text(s, encoding=\"utf-8\") … [174 caractères tronqués]`

  ```
corrigé 82,7 %
166:- **F1** : test **+1,39 point**, mais l'agrégat est dominé par GN/GV (82,7 % des segments gold) : GV test
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-dev-test-v7.json'))\nprint(\"commit\", d[\"commit\"], \"| ligne\", d[\"ligne\"], \"| date\", d[\"date\"])\nprint(\"validation\", d[\"validation\"])\nprint(\"resume\", js … [617 caractères tronqués]`

  ```
commit 69bd865e | ligne B13 | date 2026-11-05
validation {'exact': [195, 195], 'labels': [196, 196], 'cibles': [239, 239], 'f1': [0.5555, 0.5555], 'tete_f1': [0.7152, 0.7152], 'pos': [0.7581, 0.7581], 'couverture': [0.8201, 0.8201]}
resume {"canonique": {"dev": {"phrases": 422, "cibles": 163, "labels": 134, "exact": 133, "exact_taux": 0.9925}, "test": {"phrases": 190, "cibles": 76, "labels": 62, "exact": 62, "exact_taux": 1.0}}, "decale1": {"dev": {"phrases": 383, "cibles": 150, "labels": 120, "exact": 119, "exact_taux": 0.9917}, "test": {"phrases": 229, "cibles": 89, "labels": 76, "exact": 76, "exact_taux": 1.0}}, "decale2": {"dev": {"phrases": 419, "cibles": 165, "labels": 138, "exact": 138, "exact_taux": 1.0}, "test": {"phrases": 193, "cibles": 74, "labels": 58, "exact": 57, "exact_taux": 0.9828}}}
stabilite exact {'valeurs': {'canonique': 1.0, 'decale1': 1.0, 'decale2': 0.9828}, 'min': 0.9828, 'max': 1.0, 'dispersion': 0.0172}
stabilite couv {'valeurs': {'canonique': 0.8158, 'decale1': 0.8539, 'decale2': 0.7838}, 'min': 0.7838, 'max': 0.8539, 'dispersion': 0.0701}
hyper {'canonique': {'cibles_test': 76, 'perdus_observes': 14, 'perdus_attendus': 13.67, 'ecart_type': 2.77, 'z': 0
… [1265 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle final de l'état git (aucune modification existante de notre fait)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== modifiés suivis ===\" && git status --short | grep -v '^??' && echo \"=== nouveaux non suivis ===\" && git status --short | grep '^??'", "description": "List tracked modifications and untracked files"}`

  ```
=== modifiés suivis ===
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
D  journal/sessions/3144cf23-6
… [3700 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== occurrences historiques ===\" && grep -n \"125/126\\|126/126\\|60/61\\|133/134\\|62/62\" reports/rapport-dev-test-v7.md && echo \"=== corrections ===\" && grep -n \"0,7869\\|Trois réserves\\|81 %\" reports/rapport-dev-test … [153 caractères tronqués]`

  ```
=== occurrences historiques ===
1:# B13 — dev/test en v7 : dev 133/134, test 62/62, le split tient sur trois découpages
4:> Le gold 612 est re-coupé par `crc32(id) % 3 == 0` (test) : **dev 133/134 (0,9925)**, **test 62/62 (1,0)**
37:| **dev** | 422 | 163 | 134 | 134/163 = **0,8221** | 133/134 = **0,9925** | 0,5512 | 0,7132 |
38:| **test** | 190 | 76 | 62 | 62/76 = **0,8158** | 62/62 = **1,0** | 0,5651 | 0,7196 |
136:  splits 0 et 1, et dans test pour le split 2 — d'où 62/62, 62/62, 57/58.
156:- **Exact** : dev **133/134**, test **62/62** → **1 échec contre 0**, soit **0,75 point** et **1 cas**.
175:est passée à 187 labels (dev 125/126 puis 126/126 selon le commit, test 60/61) ; la v7 est à 196 labels
176:(dev 133/134, test 62/62). Au dernier état v5 (`b975011b`), l'unique échec était **r309**, dans le
177:**seau 0** (donc test), d'où 60/61 au test et 126/126 en dev. En v7, **r309 est corrigé** et **r102**
=== corrections ===
=== 82,7 ===
166:- **F1** : test **+1,39 point**, mais l'agrégat est dominé par GN/GV (82,7 % des segments gold) : GV test
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-dev-test-v7.json'))\ns=open('reports/rapport-dev-test-v7.md',encoding='utf-8').read()\ndef check(txt, label):\n    assert txt in s, (label, txt)\n    print(\"OK\", label … [1260 caractères tronqués]`

  ```
OK dev exact 133/134
OK dev couv 134/163
OK test exact 62/62
OK test couv 62/76
OK detail fr 92/92
OK detail en 41/42
OK detail REL 42/42
OK detail GP 32/32
OK dispersion test_exact_taux_span 0,0172
OK dispersion test_couverture 0,0701
OK dispersion test_f1 0,0241
OK dispersion test_tete_f1 0,012
OK dispersion test_pos 0,0111
OK source dev hand 15
OK source dev reel 302
OK source dev synthetique 105
OK hyper attendu 13,67
OK v5 r309 r309
OK v7 r102 r102
Toutes les chaînes clés sont présentes.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger, charger_gele\nv={p[\"id\"] for p in charger_gele()}; l=charger()\nextra=[p for p in l if p[\"id\"] not in v]\nprint([(p[ … [218 caractères tronqués]`

  ```
[('r423', 'reel', 'fr', 0), ('r424', 'reel', 'fr', 0), ('r425', 'reel', 'fr', 0), ('r426', 'reel', 'fr', 0), ('r427', 'reel', 'en', 0), ('r428', 'reel', 'fr', 0), ('r429', 'reel', 'fr', 0), ('r430', 'reel', 'fr', 0), ('r431', 'reel', 'fr', 0), ('r432', 'reel', 'en', 0)]
2026-11-05
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"104/106\\|53/54\\|160 labels\\|TODO\\|FIXME\\|XXX\" reports/rapport-dev-test-v7.md; echo \"---\"; tail -12 reports/rapport-dev-test-v7.md; echo \"---\"; git status --short reports/rapport-dev-test-v7.md reports/pensee-dev-t … [72 caractères tronqués]`

  ```
174:**Continuité v5 → v7.** La fiche d'origine mesurait dev 104/106 et test 53/54 avec 160 labels ; la v5
225:- [`rapport-gold-split.md`](rapport-gold-split.md) — la fiche d'origine (160 labels).
---
   systématiquement le par-type) ; changer le split maintenant casserait la comparaison avec la v5.
4. **Re-mesurer après la prochaine règle** : c'est le seul moyen de savoir si le gain est un gain.

## 9. Fichiers

- [`gold_split.py`](../tools/tests/linguistique/gold_split.py) — le split (`dev`, `test`, `compter`).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `charger`, `evaluer_bloc`.
- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — l'heuristique mesurée.
- [`pensee-dev-test-v7.json`](pensee-dev-test-v7.json) — les trois splits, l'équilibre, les contrôles
  (χ², hypergéométrie, Wilson, Monte-Carlo), la comparaison v5 → v7.
- [`rapport-gold-split.md`](rapport-gold-split.md) — la fiche d'origine (160 labels).
- [`rapport-pensee-couverture-v7.md`](rapport-pensee-couverture-v7.md) — la fiche v7 (gelé 602).
---
A  reports/pensee-dev-test-v7.json
A  reports/rapport-dev-test-v7.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -2 && echo \"--- fichiers dans HEAD ? ---\" && git ls-tree -r --name-only HEAD reports/ | grep -E \"dev-test-v7\" || echo \"non présents dans HEAD\" && echo \"--- index ---\" && git diff --cached --name-only | grep  … [96 caractères tronqués]`

  ```
e4cd4408 DOCS — LE TABLEAU DES PORTES T163-T180 PASSE AUX VALEURS V7 (43 SPANS, EXACT 195/196, FR 1,0 / EN 0,9836)
4ccf06e1 JOURNAL — LA SOIRÉE DU DÉCOUPAGE : F1 0,2862 → 0,5595, COUVERTURE 196/239, ATTACHEMENT 195/196
--- fichiers dans HEAD ? ---
non présents dans HEAD
--- index ---
reports/pensee-dev-test-v7.json
reports/rapport-dev-test-v7.md
  ```

### 🤖 Assistant

⏵ Vérification que le code mesuré n'a pas bougé depuis `69bd865e`

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat 69bd865e -- tools/bloc_linguistique.py tools/tests/linguistique/gold_split.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json tools/tests/linguistiqu … [178 caractères tronqués]`

  ```
exit=0
  ```

### 🤖 Assistant

⏵ Envoi du résultat complet à l'agent parent

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Terminé. Deux fichiers neufs (non committés) : `reports/rapport-dev-test-v7.md` et `reports/pensee-dev-test-v7.json`. Mesure au commit `69bd865e` (les fichiers mesurés n'ont pas bougé ; HEAD a seulement avancé sur docs/journal depuis). … [2985 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

### 🤖 Assistant

⏵ Résumé final de la re-mesure dev/test v7

Deux fichiers neufs créés, aucun fichier existant modifié, aucun commit :
`reports/rapport-dev-test-v7.md` et `reports/pensee-dev-test-v7.json`.

**Split canonique (`crc32(id)%3==0` → test), commit `69bd865e`**

| | phrases | cibles | labels | couverture | exact/labels | F1 | tête |
|---|---:|---:|---:|---:|---:|---:|---:|
| dev | 422 | 163 | 134 | 0,8221 | **133/134 = 0,9925** | 0,5512 | 0,7132 |
| test | 190 | 76 | 62 | 0,8158 | **62/62 = 1,0** | 0,5651 | 0,7196 |
| tout | 612 | 239 | 196 | 0,8201 | **195/196 = 0,9949** | 0,5555 | 0,7152 |

Par langue : fr 92/92 dev, 43/43 test ; en 41/42 dev, 19/19 test.
Par type : REL 42/42 dev, 11/11 test ; SUB 33/33, 19/19 ; GP 58/59, 32/32 (l'unique échec est r102, GP/en).

**Les trois splits**

| split | dev exact | test exact |
|---|---:|---:|
| `%3==0` (canonique) | 133/134 | 62/62 |
| `%3==1` | 119/120 | 76/76 |
| `%3==2` | 138/138 | 57/58 |

**Écart** : **1 cas** sur l'exact (étendue 0,0172 au test, 0,0083 en dev), **3 spans** sur la couverture (14/13/16 perdus sur 43, attendus 13,67/16,01/13,31), **2,4 pts** de F1, **1,2 pt** de tête. Un Monte-Carlo de 2 000 partitions aléatoires place toutes ces étendues dans la bande 95 % : le split est stable.

**Équilibre** : aucune catégorie demandée absente, mais `hand` est mince (5 phrases, 3 cibles au test, toutes GP ; `hand/REL` et `hand/SUB` uniquement en dev) et REL/en ne compte que 5 cibles au test. Le test canonique est REL-pauvre (22,4 % contre 35,0 % en dev) et GP-riche (46,1 % contre 37,4 % ; χ² p=0,26).

**Dev vs test** : 1 échec contre 0 → **< 2 cas**, pas d'alerte. En v5, l'échec unique était r309 (seau 0/test) ; en v7 il est corrigé et r102 (seau 2/dev) apparaît : l'écart s'inverse parce que l'échec change de phrase et de seau, pas parce que le test progresse. La F1 agrégée +1,39 pt est portée par GN/GV, pas par l'attachement ; sur REL/SUB/GP le test est plus bas de 6,8/1,3/4,0 pts.

