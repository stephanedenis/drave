# Session DSH — relecture

- identifiant : `session-614644be-9315-4734-9b97-236a792f4dc5`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-07 14:11:37
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J1.3 : le schéma v2 de l'annotation — publier `tools/schemas/drave-annotation-v2.json` (ajout de `meta.alternative` et `meta.partition`), version 2, valider avec `tools/verifier_schema_produit.py --gold 20`, mettre à jour la doc produit, commit. Rétro-compatible : version 1 reste lue.

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

- **bash** `{"command": "pwd && ls -la && git status --short | head -50 && git log --oneline -10", "description": "Inspect repo root and git state"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138  6 nov 10:08 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   180  7 nov 14:11 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   932  7 nov 00:00 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 73836  7 nov 13:03 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [2311 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/schemas/ 2>/dev/null; echo '---'; ls -la tools/ | head -60", "description": "List schemas and tools"}`

  ```
total 4
drwxr-xr-x. 1 stephane stephane    48  6 nov 18:38 .
drwxr-xr-x. 1 stephane stephane 17320  7 nov 12:50 ..
-rw-r--r--. 1 stephane stephane  2261  6 nov 18:33 drave-annotation-v1.json
---
total 4952
drwxr-xr-x. 1 stephane stephane  17320  7 nov 12:50 .
drwxr-xr-x. 1 stephane stephane    686  6 nov 09:52 ..
-rw-------. 1 stephane stephane   8428 24 oct 21:16 adaptateur_langue.py
-rwx--x--x. 1 stephane stephane  11640  1 oct 04:21 aiguille.py
-rw-r--r--. 1 stephane stephane  80950 19 oct 14:33 aligneur_litteraire.py
-rw-------. 1 stephane stephane   7797  6 oct 22:04 amplification.py
-rw-------. 1 stephane stephane   3848 21 oct 00:56 analyse_alignement.py
-rwx--x--x. 1 stephane stephane   8850  1 oct 17:40 analyse_empreinte.py
-rw-------. 1 stephane stephane   4614  2 oct 17:28 analyse_engram.py
-rwx--x--x. 1 stephane stephane  11086  1 oct 20:13 analyse_experts_statique.py
-rwxr-xr-x. 1 stephane stephane   5449  3 oct 04:19 analyse_flux.py
-rwx--x--x. 1 stephane stephane   6767  3 oct 09:42 analyse_hc.py
-rw-------. 1 stephane stephane   6681 20 oct 08:52 analyse_litteraire.py
-rwx--x--x. 1 stephane stephane   6364  3 oct 08:11 analyse_octets_par_jeton.py
-rwx--x--x. 1 steph
… [3224 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/schemas/drave-annotation-v1.json"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/schemas/drave-annotation-v1.json</path>
<type>file</type>
<content>
1: {
2:  "$schema": "https://json-schema.org/draft/2020-12/schema",
3:  "$id": "https://drave.local/schema/annotation-v1.json",
4:  "title": "drave.annotation v1",
5:  "description": "L'annotation du bloc linguistique heuristique : un texte, ses étiquettes par niveau, ses unités sémantiques et son refus éventuel.",
6:  "type": "object",
7:  "required": [
8:   "schema",
9:   "version",
10:   "texte",
11:   "langue",
12:   "script",
13:   "refus",
14:   "etiquettes",
15:   "unites_semantiques"
16:  ],
17:  "properties": {
18:   "schema": {
19:    "const": "drave.annotation"
20:   },
21:   "version": {
22:    "const": 1
23:   },
24:   "texte": {
25:    "type": "string"
26:   },
27:   "langue": {
28:    "type": "string",
29:    "pattern": "^[a-z]{2,3}$|^und$"
30:   },
31:   "script": {
32:    "type": "string"
33:   },
34:   "source": {
35:    "type": "string"
36:   },
37:   "refus": {
38:    "type": "string",
39:    "enum": [
40:     "",
41:     "vide",
42:     "non_texte",
43:     "trop_long",
44:     "neuronal"
45:    ]
46:   },
47:   "etiquettes": {
48:    
… [1810 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/verifier_schema_produit.py tools/*schema* 2>/dev/null; echo '---grep---'; grep -rl \"drave-annotation\" --exclude-dir=.git . 2>/dev/null | head -50", "description": "Locate schema verifier and references"}`

  ```
-rw-r--r--. 1 stephane stephane 4572  6 nov 18:42 tools/verifier_schema_produit.py
-rw-r--r--. 1 stephane stephane 4572  6 nov 18:42 tools/verifier_schema_produit.py
-rw-------. 1 stephane stephane 7860 30 oct 10:33 tools/verifier_schemas.py

tools/schemas:
total 4
drwxr-xr-x. 1 stephane stephane    48  6 nov 18:38 .
drwxr-xr-x. 1 stephane stephane 17320  7 nov 12:50 ..
-rw-r--r--. 1 stephane stephane  2261  6 nov 18:33 drave-annotation-v1.json
---grep---
[still running after 60000ms; moved to background job bash-3]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_kill** `{"job_id": "bash-3", "reason": "Too broad grep; replaced by targeted searches"}`

  ```
requested cancellation of job bash-3
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_schema_produit.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_schema_produit.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """verifier_schema_produit.py — valide une annotation `drave.annotation` contre le schéma v1.
3: 
4: Le schéma publié est `tools/schemas/drave-annotation-v1.json` (Draft 2020-12). Ce vérificateur compile le
5: schéma une fois, puis valide les annotations de cas choisis : français, anglais, refus (texte
6: vide), entrée non textuelle, texte très long. Il ne dépend que de `fastjsonschema` (sinon il se
7: rabat sur une validation minimale des 8 champs obligatoires).
8: 
9: Usage :
10:     python3 tools/verifier_schema_produit.py              # 5 cas, sortie 0/1
11:     python3 tools/verifier_schema_produit.py --json       # le détail des cas
12:     python3 tools/verifier_schema_produit.py --aide
13: """
14: from __future__ import annotations
15: 
16: import argparse
17: import json
18: import pathlib
19: import sys
20: 
21: RACINE = pathlib.Path(__file__).resolve().parents[1]
22: SCHEMA = RACINE / "tools" / "schemas" / "drave-annotation-v1.json"
23: OBLIGATOIRES = ("schema", "version", "texte", "langue", "script", "refus",
24:         
… [3962 caractères tronqués]
  ```

- **bash** `{"command": "ls docs; echo '---'; find docs -iname '*produit*' -o -iname '*schema*' | head -50; echo '---reports---'; ls reports | grep -i schema | head -30", "description": "Find product docs and schema docs"}`

  ```
agent
archive
implantation
methode
pilotage
produit
README.md
schemas
theorie
---
docs/schemas
docs/theorie/glossaire/entrees/reproduit-non-reproduit.md
docs/theorie/synthese/schemas
docs/produit
---reports---
pensee-schema-v1.json
rapport-schema-v1.md
  ```

- **bash** `{"command": "grep -rln \"drave.annotation\\|verifier_schema_produit\\|drave-annotation\" docs reports journal tools README.md 2>/dev/null | head -50", "description": "Targeted grep for annotation schema references"}`

  ```
reports/pensee-fiabilite-produit.json
reports/rapport-fiabilite-produit.md
reports/rapport-schema-v1.md
reports/pensee-schema-v1.json
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
journal/sessions/eedb7a58-2a33-4caa-8509-f46d9e328080/digest.md
journal/sessions/538288b3-117b-4daf-8d16-0cd8d6b0090d/digest.md
journal/sessions/7635f5f5-11b8-4d10-bea5-50a90e536e31/digest.md
journal/sessions/77d26bc7-1657-4c96-83c9-bba7c25dd828/digest.md
journal/2026-11-06/README.md
journal/2026-11-06/portes.md
tools/__pycache__/bloc_dbg.cpython-313.pyc
tools/__pycache__/bloc_dbg2.cpython-313.pyc
tools/__pycache__/bloc_dbg3.cpython-313.pyc
tools/__pycache__/bloc_exp.cpython-313.pyc
tools/__pycache__/bloc_exp2.cpython-313.pyc
tools/__pycache__/bloc_exp3.cpython-313.pyc
tools/__pycache__/bloc_exp4.cpython-313.pyc
tools/__pycache__/bloc_exp5.cpython-313.pyc
tools/__pycache__/bloc_exp6.cpython-313.pyc
tools/__pycache__/bloc_linguistique.cpython-313.pyc
tools/tests/test_produit.py
tools/tests/test_schema_produit.py
tools/porte-produit.sh
tools/verifier_schema_produit.py
tools/schemas/drave-annotation-v1.json
tools/chantier/plan
… [42 caractères tronqués]
  ```

- **bash** `{"command": "ls -la docs/produit; echo '---'; find docs/produit -type f | sort; echo '---tests---'; ls -la tools/tests/test_schema_produit.py tools/tests/test_produit.py tools/porte-produit.sh", "description": "List product docs and tests"}`

  ```
total 44
drwxr-xr-x. 1 stephane stephane    40  6 nov 18:38 .
drwxr-xr-x. 1 stephane stephane   138  6 nov 10:08 ..
-rw-r--r--. 1 stephane stephane 19315  6 nov 19:40 exemples.md
-rw-r--r--. 1 stephane stephane 23768  7 nov 00:39 README.md
---
docs/produit/exemples.md
docs/produit/README.md
---tests---
-rwxr-xr-x. 1 stephane stephane 3375  6 nov 22:29 tools/porte-produit.sh
-rw-------. 1 stephane stephane 9138  7 nov 00:38 tools/tests/test_produit.py
-rw-r--r--. 1 stephane stephane 3412  6 nov 18:08 tools/tests/test_schema_produit.py
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v1.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v1.md</path>
<type>file</type>
<content>
1: # B13 — le contrat v1 : `schema`/`version`, refus en JSON (code 3), entrées hostiles tolérées
2: 
3: > **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ;
4: > l'état courant du bloc est dans [`en-cours`](../docs/pilotage/en-cours.md) (POS 86,25 %,
5: > F1 0,7535, attachement 236/237, couverture 0,9916, 2 spans).
6: 
7: > **Ligne de roadmap** : **B13** (produit) · **Date** : 2026-11-06 · **Verdict** : ✅
8: > **Ce qui change pour un client** : le JSON porte désormais **`schema`** (`"drave.annotation"`)
9: > et **`version`** (`1`) ; un **refus** est une **réponse** (JSON avec `refus`, code de sortie
10: > **3**) et non plus un stdout vide ; un **surrogate isolé** et une **entrée non textuelle** ne
11: > font plus planter la CLI ; `--json` est stable (clés triées, sans durée).
12: > **Le schéma est publié** : [`tools/schemas/drave-annotation-v1.json`](../tools/schemas/drave-annotation-v1.json)
13: > (Draft 2020-12) et **validé** par `tools/verifier_schema_produit.py` (5 cas : fr, en, vide,
14: > ponctuation, long) avec `fastjsonsch
… [3027 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"alternative\\|partition\\|meta\" tools/bloc_linguistique.py | head -80", "description": "Find meta alternative/partition in bloc_linguistique"}`

  ```
79:    meta: dict = field(default_factory=dict)
87:            "script": self.script, "meta": dict(self.meta),
801:                 union: bool = True, partition: str = "alternative"):
807:        # "brut" : la sortie d'avant (chevauchements non documentés) ; "alternative" :
808:        # les deux segments restent, `meta.alternative` dit lequel est préféré ;
810:        # union du P0-3) ; "filtrer" : partition stricte, le chunker est la partition.
811:        # Dans les deux filtres, le segment retiré reste dans `meta.alternative` (`retire`).
812:        if partition not in ("brut", "alternative", "filtrer_union", "filtrer"):
813:            raise ValueError("partition attend 'brut', 'alternative', 'filtrer_union' ou 'filtrer'")
814:        self.partition = partition
1474:                                            langue=lg, script=script, meta={"ouvert": False}))
1479:                                            langue=lg, script=script, meta={"ouvert": ouvert}))
1499:                                          script=script, meta={"ouvert": True, "contexte": avant.type})
1513:                                           meta={"ouvert": True, "contexte": "pron_sujet"})
1533:          
… [3918 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_schema_produit.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_schema_produit.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """test_schema_produit.py — le **contrat** du produit : schéma v1, refus, entrées hostiles.
3: 
4: Ce que le test fige (et qu'un client peut supposer) :
5: - 8 champs **obligatoires** à la racine : `schema`, `version`, `texte`, `langue`, `script`,
6:   `refus`, `etiquettes`, `unites_semantiques` ;
7: - `schema == "drave.annotation"` et `version == 1` ;
8: - un refus est une **réponse** : JSON valide avec `refus`, code de sortie 3 ;
9: - un surrogate isolé et une entrée non textuelle ne font pas planter.
10: """
11: from __future__ import annotations
12: 
13: import json
14: import pathlib
15: import subprocess
16: import sys
17: import unittest
18: 
19: RACINE = pathlib.Path(__file__).resolve().parents[2]
20: OBLIGATOIRES = ("schema", "version", "texte", "langue", "script", "refus",
21:                 "etiquettes", "unites_semantiques")
22: 
23: 
24: def _cli(*args: str) -> subprocess.CompletedProcess:
25:     return subprocess.run([sys.executable, str(RACINE / "tools/drave.py"), *args],
26:                           capture_outpu
… [2674 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 2340, "limit": 160}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
2340:                                           "duree_s": round(time.perf_counter() - t0, 6)})
2341:         except Exception as e:
2342:             annotation = Annotation(texte=texte, langue=lg, script=script, source=self.nom,
2343:                                     refus=f"neuronal-pragmatique: {type(e).__name__}: {str(e)[:160]}",
2344:                                     trace=[{"etape": "neuronal-pragmatique", "erreur": str(e)[:160]}],
2345:                                     cout={"octets": len(texte.encode("utf-8", "replace")),
2346:                                           "duree_s": round(time.perf_counter() - t0, 6)})
2347:         if self.cache:
2348:             self._cache[cle] = annotation
2349:         return annotation
2350: 
2351: 
2352: # --------------------------------------------------------------------------- compositions
2353: 
2354: 
2355: def _relation_partition(x: Etiquette, y: Etiquette) -> str:
2356:     """La relation de `y` vue **depuis** `x` : `inclut` = x contient y."""
2357:     if x.debut == y.debut and x.fin == y.fin:
2358:    
… [7962 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"schema\\|schéma\\|version\\|meta\\|alternative\\|partition\" docs/produit/README.md | head -80; echo '====EXEMPLES===='; grep -n \"schema\\|schéma\\|version\\|meta\\|alternative\\|partition\" docs/produit/exemples.md | head -80", "description": "Search product docs for schema/ … [15 caractères tronqués]`

  ```
9:> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer` et `--version` existent, et la
22:| **développeur NLP** | un JSON déterministe, des spans, une confiance, des candidats | le schéma n'est pas encore versionné (§ 7) |
26:aucun accès réseau. Les quatre gold sont versionnés dans `tools/tests/linguistique/` ; le corpus
100:           | "\(.type) \(.valeur) → \(.meta.attachement.cible // "—")"] | join(" · ")'
108:gold). Le JSON publie aussi une **seconde lecture d'union** (`meta.union: true`, span plus
124:  vue linéaire (partition filtrer) F1 81.04 %  · attachement 93.31 % de couverture
146:traitements de corpus), chaque ligne portant le schéma v1 complet.
151:python3 tools/drave.py analyser "Le chat de la voisine qui dort sur le toit se réveille." --partition filtrer
154:Quatre vues (`--partition`) : `alternative` (défaut : les deux segments restent, `meta.alternative`
157:(l'ancienne sortie). Le défaut est `alternative`.
217:`meta.union: true`. C'est une **lecture concurrente** publiée par l'union, pas un second
242:profils UDHR (398 langues, 0,9687) ne sont pas exposés par le CLI et ne sont pas versionnés :
260:JSON change de forme — d'où le rejeu et le contrôle p
… [2281 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"J1\\.3\\|J1\\.2\\|J1\\.4\" tools docs journal reports README.md 2>/dev/null | head -50", "description": "Find J1.3 task references"}`

  ```
tools/chantier/plan.json:36:   "id": "J1.2",
tools/chantier/plan.json:39:   "mandat": "Tâche J1.2 : la convention des GV (322 FP / 180 FN). Classe les erreurs, mesure 2 règles candidates (arrêt à l'adverbe final, sujet hors du GV) sur dev/test, garde celles qui font monter le F1 sans perdre d'attachement, fiche `reports/rapport-convention-gv.md` + JSON, commit. Règles : S/D/N2 intouchés ; 183/183.",
tools/chantier/plan.json:53:   "id": "J1.3",
tools/chantier/plan.json:56:   "mandat": "Tâche J1.3 : le schéma v2 de l'annotation — publier `tools/schemas/drave-annotation-v2.json` (ajout de `meta.alternative` et `meta.partition`), version 2, valider avec `tools/verifier_schema_produit.py --gold 20`, mettre à jour la doc produit, commit. Rétro-compatible : version 1 reste lue.",
tools/chantier/plan.json:70:   "id": "J1.4",
tools/chantier/plan.json:73:   "mandat": "Tâche J1.4 : la restitution v0 — une commande `python3 tools/drave.py restituer TEXTE` qui reconstruit la surface depuis l'annotation et affiche la fidélité (miroir). Mesure le miroir sur les 50 textes libres, fiche `reports/rapport-restitution-v0.md` + JSON, tests, commit.",
docs/pilotage/en-cours.md:69:- **Prochaine action** 
… [8921 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nprint(type(p))\nif isinstance(p,dict):\n    print(list(p)[:30])\n    s=json.dumps(p,ensure_ascii=False)\n    import re\n    for m in re.finditer(r'.{120}J1\\.[0-9].{200}', s):\n        print(m.group(0))\nelif  … [208 caractères tronqués]`

  ```
<class 'dict'>
['nom', 'principe', 'taches']
"budget_min": 2, "acceptation": [{"commande": "python3 -c \"print('LIAISON-OK')\"", "attendu": "LIAISON-OK"}]}, {"id": "J1.1", "jour": 1, "titre": "r035 : la relative zéro", "mandat": "Tâche J1.1 du chantier : la relative zéro (r035, « The film she talks about is out. »). Reproduis, explique, propose UNE règle générale mes
}, {"commande": "python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?", "attendu": "REVUE-0"}]}, {"id": "J1.2", "jour": 1, "titre": "La convention des GV", "mandat": "Tâche J1.2 : la convention des GV (322 FP / 180 FN). Classe les erreurs, mesure 2 règles candidates (arrêt à l'adverbe final, sujet hors du GV
endu": "FICHE-OK"}, {"commande": "bash tools/porte-bloc-linguistique.sh 2>&1 | tail -1", "attendu": "verte"}]}, {"id": "J1.3", "jour": 1, "titre": "Le schéma v2", "mandat": "Tâche J1.3 : le schéma v2 de l'annotation — publier `tools/schemas/drave-annotation-v2.json` (ajout de `meta.alternative` et `meta.partition`), versio
"python3 tools/verifier_schema_produit.py --gold 20 >/dev/null 2>&1; echo VALIDE-$?", "attendu": "VALIDE-0"}]}, {"id": "J1.4", "jour": 1, "titre": "La restitution v0", "mandat": "T
… [143 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nfor t in p['taches']:\n    if t['id']=='J1.3':\n        print(json.dumps(t,ensure_ascii=False,indent=2))\nPY", "description": "Print J1.3 task object"}`

  ```
{
  "id": "J1.3",
  "jour": 1,
  "titre": "Le schéma v2",
  "mandat": "Tâche J1.3 : le schéma v2 de l'annotation — publier `tools/schemas/drave-annotation-v2.json` (ajout de `meta.alternative` et `meta.partition`), version 2, valider avec `tools/verifier_schema_produit.py --gold 20`, mettre à jour la doc produit, commit. Rétro-compatible : version 1 reste lue.",
  "budget_min": 90,
  "acceptation": [
    {
      "commande": "test -f tools/schemas/drave-annotation-v2.json && echo V2-OK",
      "attendu": "V2-OK"
    },
    {
      "commande": "python3 tools/verifier_schema_produit.py --gold 20 >/dev/null 2>&1; echo VALIDE-$?",
      "attendu": "VALIDE-0"
    }
  ]
}
  ```

- **bash** `{"command": "sed -n '1,180p' docs/produit/README.md", "description": "Read first part of product README"}`

  ```
# Le premier produit — analyser un texte avec Drave

> **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
> linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
> il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
> qu'il garantit.
>
> **Vérifié le 2026-11-06** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer` et `--version` existent, et la
> porte produit est verte. Les exemples du § 3 sont réels : ils ont été lancés pour ce document.
> Ce qui manque encore au contrat est nommé au § 7, sans être présenté comme acquis.
>
> **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,
> classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses
> candidats, de façon **déterministe**, et il sait **se mesurer** sur un gold de 612 phrases.

## 1. À qui s'adresse le produit

| vous êtes… | ce que vous obtenez | ce qu'il faut savoir |
|---|---|---|
| **linguiste, enseignant, curieux** | une analyse immédiate : POS, syntagmes, rôl
… [8170 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '180,430p' docs/produit/README.md", "description": "Read rest of product README"}`

  ```
**Lecture.** La commande analyse **deux fois**, compare le JSON **canonique** (clés triées,
durée exclue) et rend une empreinte sha256. Deux exécutions indépendantes rendent le même octet :
l'analyse est déterministe. C'est la garantie de base du rejeu.

### 3.5 Le refus, et la langue inconnue

```bash
python3 tools/drave.py analyser ""; echo "exit=$?"
```
```
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
exit=1
```

**Lecture.** Le CLI traite le refus comme une **erreur** : message sur `stderr`, **rien sur
`stdout`**, code **1**. Le bloc, lui, rend un JSON avec `refus: "vide"` (voir `exemples.md` § 4) :
c'est l'API qui porte l'état, le CLI qui le traduit en code. Un texte vide n'est jamais une
annotation « comme les autres ». Pour la langue, `und` est une réponse honnête : « Élodie
sourit. » rend `langue=und` (confiance 0,04 < seuil 0,12), même avec `--langue fr` — l'indice
n'est pas une contrainte. Et `--langue de` sort **2** : le CLI n'accepte que `fr` et `en`.

## 4. Ce que le produit ne fait pas encore

**1. Il n'écrit pas de texte.** Pas de restitution, pas de traduction, pas de génération : le
produit rend des **étiquettes**, jamais
… [12643 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 80, "offset": 50}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 70, "offset": 770}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
50: NIVEAUX = ("graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
51:            "pragmatique", "document")
52: SOURCES = ("heuristique", "neuronal", "humain")
53: SCRIPT_NEUTRE = "Zyyy"
54: 
55: # --------------------------------------------------------------------------- types
56: 
57: 
58: @dataclass(frozen=True)
59: class Span:
60:     debut: int
61:     fin: int
62: 
63:     def json(self) -> dict:
64:         return {"debut": self.debut, "fin": self.fin}
65: 
66: 
67: @dataclass
68: class Etiquette:
69:     niveau: str
70:     type: str
71:     valeur: str
72:     debut: int
73:     fin: int
74:     source: str = "heuristique"
75:     confiance: float = 0.5
76:     candidats: list[str] = field(default_factory=list)
77:     langue: str = "und"
78:     script: str = SCRIPT_NEUTRE
79:     meta: dict = field(default_factory=dict)
80: 
81:     def json(self) -> dict:
82:         return {
83:             "niveau": self.niveau, "type": self.type, "valeur": self.valeur,
84:             "debut": self.debut, "fin": self.fin, "source": self.source,
85:
… [2003 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
770: 
771:     while i < n:
772:         ch = texte[i]
773:         if ch in "\r\n":
774:             j = i
775:             while j < n and texte[j].isspace():
776:                 j += 1
777:             if _nouvelle_ligne_structurelle(texte, i, j):
778:                 ajouter(i, "déclarative")
779:             i = j
780:             continue
781:         if ch not in ".!?…":
782:             i += 1
783:             continue
784:         j = i + 1
785:         while j < n and texte[j] in ".!?…":
786:             j += 1
787:         if not _dans_zone(zones, i, j) and _est_frontiere(texte, i, j, zones):
788:             ajouter(_absorber_fermants(texte, j), _type_phrase(texte[i:j]))
789:         i = j
790:     ajouter(n, "déclarative")
791:     return sortie
792: 
793: 
794: class Heuristique:
795:     """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""
796: 
797:     nom = "heuristique"
798: 
799:     def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
800:                  seuil_ouvert: fl
… [2304 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"VERSION_ANNOTATION\\|SCHEMA_ANNOTATION\\|depuis_json\\|from_json\\|charger\\|version\" tools/bloc_linguistique.py | head -80", "description": "Find version and JSON loading functions"}`

  ```
91:SCHEMA_ANNOTATION = "drave.annotation"
92:VERSION_ANNOTATION = 1
125:            # le **format** est versionné : un client peut vérifier ce qu'il reçoit
126:            "schema": SCHEMA_ANNOTATION, "version": VERSION_ANNOTATION,
164:def charger_profils_udhr(chemin: pathlib.Path, train=(0, 14), test=(15, 30),
170:    de test. Un profil est une donnée, pas un prompt : il se versionne et se rejoue.
2720:    profils, tests = charger_profils_udhr(udhr, test=(15, 15), min_test=1)
2820:        profils, _ = charger_profils_udhr(pathlib.Path(args.profils))
  ```

- **bash** `{"command": "grep -rn \"VERSION_ANNOTATION\\|SCHEMA_ANNOTATION\\|version.*1\\|drave.annotation\" tools/drave.py tools/tests/test_produit.py tools/tests/test_schema_produit.py tools/porte-produit.sh | head -80", "description": "Find version references in CLI/tests"}`

  ```
tools/tests/test_produit.py:179:        self.assertEqual(json.loads(sortie.stdout)["schema"], "drave.annotation")
tools/tests/test_produit.py:206:            self.assertEqual(lignes[0]["schema"], "drave.annotation")
tools/tests/test_schema_produit.py:7:- `schema == "drave.annotation"` et `version == 1` ;
tools/tests/test_schema_produit.py:36:        self.assertEqual(d["schema"], "drave.annotation")
tools/tests/test_schema_produit.py:37:        self.assertEqual(d["version"], 1)
tools/tests/test_schema_produit.py:44:        self.assertEqual(d["schema"], "drave.annotation")
tools/tests/test_schema_produit.py:52:        self.assertEqual(d["schema"], "drave.annotation")
tools/porte-produit.sh:11:ver=$(python3 tools/drave.py --version 2>&1)
tools/porte-produit.sh:12:case "$ver" in drave*) dit ✅ "version : $ver" ;; *) dit ❌ "version : $ver"; ko=1 ;; esac
  ```

- **bash** `{"command": "grep -n \"version\\|schema\" tools/tests/test_produit.py; echo '---'; sed -n '1,130p' tools/porte-produit.sh", "description": "Read product test/version and gate"}`

  ```
39:    """Le contrat produit : version/aide, analyse, JSON, rejeu, usage."""
41:    def test_version_et_aide(self) -> None:
42:        version = drave("--version")
45:            version.returncode == 0
46:            and re.fullmatch(r"drave \d+\.\d+\.\d+\n", version.stdout)
49:            detail(version) + detail(aide),
179:        self.assertEqual(json.loads(sortie.stdout)["schema"], "drave.annotation")
206:            self.assertEqual(lignes[0]["schema"], "drave.annotation")
---
#!/usr/bin/env bash
# porte-produit — le premier produit : la CLI répond, le JSON est valide, le rejeu est identique.
#
# Ce qu'elle vérifie : `drave --version`, `analyser` (fr et en) rend un JSON parsable avec des
# étiquettes, `rejouer` rend le même sha256 deux fois, et le smoke test passe.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
ko=0
dit() { printf '  %s %s\n' "$1" "$2"; }

ver=$(python3 tools/drave.py --version 2>&1)
case "$ver" in drave*) dit ✅ "version : $ver" ;; *) dit ❌ "version : $ver"; ko=1 ;; esac

for langue in fr en; do
  case "$langue" in
    fr) texte="Le chat dort sur le toit." ;;
    en) texte="The cat sleeps on the roof." ;;
  esac
  sortie=$(python3 tools/drave.py analyser 
… [2604 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"meta.alternative\\|meta.partition\\|partition\" docs/produit/exemples.md | head -40; echo '---head---'; sed -n '1,60p' docs/produit/exemples.md", "description": "See example docs on meta fields"}`

  ```
---head---
# Cinq exemples d'analyse, commentés

> **Ce que ce document est.** Cinq exécutions **réelles** du produit, avec leur JSON commenté. Il
> complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce document dit
> *comment lire* ce qui sort. Les sorties ont été produites le **2026-11-06** sur la branche
> `s/v7`, avec le CLI `tools/drave.py` (version **0.1.0**), sans modèle, sans GPU et sans réseau.
>
> **Une commande, un JSON.** `python3 tools/drave.py analyser "…" --json` rend l'annotation
> complète (neuf niveaux). Pour la lire, ce document filtre avec `jq` ; le produit, lui, n'a pas
> besoin de `jq`.

## 0. Comment lire les JSON

- `debut` / `fin` : indices en **points de code Unicode**, 0-based, fin exclue : `[debut:fin)`.
  « Élodie » → `[0:6]` ; un emoji compte pour **un** point.
- `niveau` : `pos`, `syntagme`, `phrase` et `pragmatique` sont montrés ; `graphème`, `mot`,
  `morphème`, `discours` et `document` sont omis (ils existent dans le JSON complet).
- `confiance` : **déclarée**, pas calibrée. 0,3 pour un NOUN ouvert, 0,92 pour un DET.
- `meta.attachement` : `{segment, cible}` ; `cible` est une **chaîne**, pas un span.
- `candidats` : des **cha
… [1586 caractères tronqués]
  ```

- **bash** `{"command": "git branch --show-current; git status --porcelain=v1; echo '---'; git diff --stat; echo '---last commits files---'; git show --stat --oneline -3 | head -40", "description": "Inspect branch and dirty files"}`

  ```
s/v7
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/structures
?? reports/rapport-s-paragraphes.md
---
 reports/pensee-coherence-fiches-v7.json |  19 +
 reports/pensee-dev-test-v10.json        |   2 +-
 reports/pensee-quatre-modes.json        | 734 ++++++++++++++++++--------------
 reports/rapport-audit-v7.md             |   6 +-
 reports/rapport-coherence-fiches-v7.md  |  17 +-
 reports/rapport-dev-test-v10.md         |   2 +-
 reports/rapport-pensee-v12.md           |   4 +-
 reports/rapport-spans-chunker.md        |  13 +-
 tools/structures                        |   0
 9 files changed, 460 insertions(+), 337 deletions(-)
---last commits files---
92652984 B13 — LA CONVENTION DES GV : SUJET HORS DU GV + ADVERBE FINAL, F1 0,7549 → 0,7902, ATTACHEMENT 237/238 ; 183/183
 docs/pilotage/en-cours.md                          |   14 +-
 docs/pilotage/roadmap.md                           |    2 +-
 docs/pilotage/semaine-autonome.md        
… [2314 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifier_schema_produit.py --gold 20; echo \"exit=$?\"; python3 -c \"import fastjsonschema; print('fastjsonschema', fastjsonschema.__version__)\"", "description": "Run current schema verifier"}`

  ```
✅ fr
  ✅ en
  ✅ vide
  ✅ ponctuation
  ✅ long
  ✅ gold:g001
  ✅ gold:g002
  ✅ gold:g003
  ✅ gold:g004
  ✅ gold:g005
  ✅ gold:g006
  ✅ gold:g007
  ✅ gold:g008
  ✅ gold:g009
  ✅ gold:g010
  ✅ gold:g011
  ✅ gold:g012
  ✅ gold:g013
  ✅ gold:g014
  ✅ gold:g015
  ✅ gold:g016
  ✅ gold:g017
  ✅ gold:g018
  ✅ gold:g019
  ✅ gold:g020
  ✅ validateur JSON Schema · 25 cas
exit=0
[stderr]
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import fastjsonschema; print('fastjsonschema', fastjsonschema.__version__)
                                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'fastjsonschema' has no attribute '__version__'
[exit code: 1]
  ```

- **bash** `{"command": "grep -rn \"schema\\|version\\|alternative\\|partition\" docs/implantation/bloc-linguistique.md | head -60; echo '---'; grep -rn \"schéma v1\\|schema v1\\|version 1\\|version == 1\\|VERSION_ANNOTATION\" docs reports tools --exclude-dir=__pycache__ | head -80", "description": "Find all sc … [20 caractères tronqués]`

  ```
5:> l'**heuristique CPU** et la **version neuronale** se substituent, se **parallélisent** ou se
29:avec `source`, `confiance` et `candidats`, et que l'on peut remplacer par une version neuronale
34:![Les neuf niveaux du bloc](../schemas/bloc-linguistique-niveaux.svg)
92:| **candidats** | les alternatives plausibles ; le bloc **énumère**, il ne tranche pas l'ambigu |
127:### 5.2 La version neuronale
179:![Substituer, paralléliser, activer](../schemas/bloc-linguistique-substitution.svg)
200:- à niveau égal, les étiquettes qui se **chevauchent** sont des **alternatives** : on garde la
322:4. **Le profil de langue** versionné (`data/` ou `reports/`) et son empreinte.
337:- Schémas : [`bloc-linguistique-niveaux.svg`](../schemas/bloc-linguistique-niveaux.svg),
338:  [`bloc-linguistique-substitution.svg`](../schemas/bloc-linguistique-substitution.svg).
---
docs/archive/plan-deepseek41-complet.md:350:>    (bloc 22)** : `tools/analyse_flux.py` lisait la version 1 du format DRVF
docs/pilotage/plan-travail.md:453:**Intégré** : schéma v1 publié (`tools/schemas/`), gold corrigé (4 GP), morphologie du 1er groupe
docs/pilotage/semaine-autonome.md:27:| `meta.alternative` hors schéma v1 | le schém
… [19115 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-partition-integree.md; echo '===='; sed -n '630,700p' reports/rapport-partition-syntagmes.md", "description": "Read partition reports for schema rationale"}`

  ```
# B13 — la partition des syntagmes : les alternatives sont étiquetées, les mesures ne bougent pas

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ;
> l'état courant du bloc est dans [`en-cours`](../docs/pilotage/en-cours.md) (POS 86,25 %,
> F1 0,7535, attachement 236/237, couverture 0,9916, 2 spans).

> **Ligne de roadmap** : **B13** (produit) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Le P0-3 est fermé sans perte** : les **239 paires** de chevauchement des deux audits sont
> **toutes** des paires S × chunker (53,1 % de S qui contient le chunker, 33,5 % l'inverse,
> 2,5 % de mêmes bornes, 10,9 % de croisements). Le mode **`alternative`** (défaut) garde les deux
> segments et écrit **`meta.alternative`** (le préféré, la relation, `retire`) : **F1 0,6482,
> exact 235/236, POS 85,00 %** — les mesures de la base, **sans déduplication silencieuse**. Le mode
> **`filtrer`** (option) donne une vue linéaire : **F1 0,6954 (+0,047)** mais **217/218** (18
> attachements en moins), les S retirés restant dans `meta.alternative`.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`partition=`,
> `_expliciter_partition`, `meta.
… [6893 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"meta.alternative\\|meta.partition\" docs/pilotage/semaine-autonome.md docs/pilotage/plan-travail.md reports/rapport-partition-integree.md reports/rapport-partition-syntagmes.md | head -60", "description": "Find meta field descriptions"}`

  ```
docs/pilotage/semaine-autonome.md:27:| `meta.alternative` hors schéma v1 | le schéma publié | [`tools/schemas/`](../../tools/schemas/) |
docs/pilotage/semaine-autonome.md:88:| | après-midi | le **schéma v2** (`meta.alternative`, `meta.partition`) et la **restitution v0** | schéma validé, miroir mesuré |
docs/pilotage/plan-travail.md:449:| 1 (P0) | frontières, partition, POS R4 | 32/40 → 0 frontières fausses ; `meta.alternative` ; **POS 85,00 %** |
reports/rapport-partition-integree.md:11:> segments et écrit **`meta.alternative`** (le préféré, la relation, `retire`) : **F1 0,6482,
reports/rapport-partition-integree.md:14:> attachements en moins), les S retirés restant dans `meta.alternative`.
reports/rapport-partition-integree.md:17:> `_expliciter_partition`, `meta.alternative`) ; fiche A29
reports/rapport-partition-integree.md:41:`meta.alternative` = `{"prefere": <bool>, "relation": "inclut|inclus|meme_span|croise",
reports/rapport-partition-integree.md:47:La fusion **déduplique** les segments ; les `meta.alternative` de l'heuristique pouvaient donc
reports/rapport-partition-integree.md:65:- **`meta.alternative`** est un schéma nouveau : il n'est pas dans le schéma v1 publié ;
repo
… [2061 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '555,630p' reports/rapport-partition-syntagmes.md", "description": "Read schema sketch for meta fields"}`

  ```
```

Exemple de sortie compacte :

```text
SYNTAGMES
  GP   [29:60]  du jardin chaque matin avant de  rôle=theme     → fleurs   [g0 r1/4 · alt=3 · 2 retiré(s)]
  GV   [61:67]  partir                           rôle=prédicat  → —        [g0 r2/4 · alt=3 · 2 retiré(s)]
```

### 4.5 Schéma de `meta.alternative`

`meta.partition` et `meta.alternative` ne sont présents que sur un syntagme qui appartient à un
groupe de chevauchement (au moins deux segments). Le schéma est **additif** : les clients qui ne
lisent pas `meta` continuent de lire l'annotation comme avant.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "meta.partition et meta.alternative d'une étiquette syntagme",
  "type": "object",
  "properties": {
    "partition": {
      "type": "object",
      "required": ["groupe", "rang", "membres", "vue"],
      "properties": {
        "groupe": {"type": "integer", "minimum": 0},
        "rang": {"type": "integer", "minimum": 1},
        "membres": {"type": "integer", "minimum": 2},
        "vue": {"enum": ["alternative", "filtrer_union", "filtrer"]}
      },
      "additionalProperties": true
    },
    "alternative": {
      "type": "array",
      "
… [1850 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"partition\\|alternative\\|VERSION\" tools/tests/test_produit_libre.py tools/tests/linguistique/test_bloc_linguistique.py tools/tests/test_*.py 2>/dev/null | head -80", "description": "Find partition tests"}`

  ```
tools/tests/test_produit_libre.py:6:- la vue **`alternative`** (défaut) documente les chevauchements dans `meta.alternative` ;
tools/tests/test_produit_libre.py:47:        h = self.bl.Heuristique(partition="filtrer")
tools/tests/test_produit_libre.py:51:    def test_alternative_etiquettes(self):
tools/tests/test_produit_libre.py:52:        h = self.bl.Heuristique(partition="alternative")
tools/tests/test_produit_libre.py:56:            if "alternative" in (e.meta or {})
tools/tests/test_produit_libre.py:61:        h = self.bl.Heuristique(partition="filtrer")
tools/tests/test_produit_libre.py:67:        h = self.bl.Heuristique(partition="filtrer")
tools/tests/test_produit_libre.py:6:- la vue **`alternative`** (défaut) documente les chevauchements dans `meta.alternative` ;
tools/tests/test_produit_libre.py:47:        h = self.bl.Heuristique(partition="filtrer")
tools/tests/test_produit_libre.py:51:    def test_alternative_etiquettes(self):
tools/tests/test_produit_libre.py:52:        h = self.bl.Heuristique(partition="alternative")
tools/tests/test_produit_libre.py:56:            if "alternative" in (e.meta or {})
tools/tests/test_produit_libre.py:61:        h = self.bl.Heuristique(p
… [510 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"drave-annotation\\|verifier_schema_produit\\|schema_produit\" docs/pilotage docs/methode reports/README.md reports/INDEX.md 2>/dev/null | head -40; echo '---'; ls -la docs/produit/schema-v1.json 2>/dev/null || true", "description": "Find other references to schema"}`

  ```
---
  ```

- **bash** `{"command": "sed -n '1,100p' tools/tests/test_produit_libre.py; echo '===='; sed -n '120,160p' tools/tests/test_produit.py", "description": "Read partition tests"}`

  ```
#!/usr/bin/env python3
"""test_produit_libre.py — non-régression sur les **50 textes libres** de l'audit A26.

Ce que le test fige :
- la vue **`filtrer`** ne produit **aucun** chevauchement de syntagmes (0/50) ;
- la vue **`alternative`** (défaut) documente les chevauchements dans `meta.alternative` ;
- les **5 textes non linguistiques** (emoji, vide, espaces, ponctuation, nombre nu) n'ont
  **aucun** syntagme ;
- l'analyse est **déterministe** (deux passes identiques).
"""
from __future__ import annotations

import json
import pathlib
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))

BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
NON_LINGUISTIQUES = {"f14", "f15", "f16", "f17", "f18"}


def _textes() -> list[tuple[str, str]]:
    donnees = json.loads(BANC.read_text(encoding="utf-8"))
    return [(item["id"], item["texte"]) for item in donnees["banc_50"]["resultats"]]


def _segments(annotation) -> list:
    return [e for e in annotation.etiquettes if e.niveau == "syntagme"]


def _chevauchements(segments: list) -> int:
    return sum(1 for i, a in enumerate(segments) for b in segments[i + 1:]
           
… [3379 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json, collections\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\ntexts=[\n \"Le chat de la voisine qui dort sur le toit se réveille.\",\n \"Le livre que j'ai lu est intéressant.\",\n \"The cat that sleeps on the roof is black.\",\n \"Bonjour … [1075 caractères tronqués]`

  ```
=== mode alternative
meta keys Counter({'ouvert': 35, 'role': 15, 'niveau': 15, 'attachement': 11, 'partition': 10, 'alternative': 10, 'union': 5, 'contexte': 1})
partition keys Counter({'groupe': 10, 'rang': 10, 'membres': 10, 'vue': 10})
alt keys Counter({'type': 24, 'debut': 24, 'fin': 24, 'source': 24, 'union': 24, 'relation': 24, 'rang': 24, 'role': 24, 'attachement': 18})
alt count 10 types Counter({'REL': 11, 'alternative': 10, 'GV': 10, 'GN': 3})
=== mode filtrer_union
meta keys Counter({'ouvert': 35, 'role': 14, 'niveau': 14, 'attachement': 11, 'partition': 9, 'alternative': 9, 'union': 5, 'contexte': 1})
partition keys Counter({'groupe': 9, 'rang': 9, 'membres': 9, 'vue': 9})
alt keys Counter({'type': 21, 'debut': 21, 'fin': 21, 'source': 21, 'union': 21, 'relation': 21, 'rang': 21, 'retire': 21, 'role': 21, 'attachement': 16})
alt count 9 types Counter({'REL': 10, 'filtrer_union': 9, 'GV': 9, 'GN': 2})
=== mode filtrer
meta keys Counter({'ouvert': 35, 'role': 10, 'niveau': 10, 'attachement': 7, 'union': 5, 'partition': 5, 'alternative': 5, 'contexte': 1})
partition keys Counter({'groupe': 5, 'rang': 5, 'membres': 5, 'vue': 5})
alt keys Counter({'type': 13, 'debut': 13, '
… [179 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\nh=bl.Heuristique(partition=\"alternative\")\ntypes=collections.Counter(); rels=collections.Counter(); sources=collections.C … [579 caractères tronqués]`

  ```
syntagme types Counter({'GN': 863, 'GV': 711, 'GP': 130, 'REL': 106, 'SUB': 73})
alt types Counter({'GN': 393, 'GV': 357, 'REL': 103, 'GP': 49, 'SUB': 28})
relations Counter({'croise': 386, 'inclus': 263, 'inclut': 263, 'meme_span': 18})
sources Counter({'heuristique': 930})
  ```

- **bash** `{"command": "grep -rn \"sha256\\|b0a1709a\\|6b6def\\|11700\\|4013\\|version.*1\" tools/tests tools/porte-produit.sh tools/pensee/autotest.py | grep -v __pycache__ | head -80", "description": "Find hash/version expectations in tests"}`

  ```
tools/tests/documents/bench-pilote.json:2:  "version": 1,
tools/tests/documents/bench-pilote.json:130:          "indice": "source.sha256",
tools/tests/documents/bench-pilote.json:131:          "valeur": "sha256"
tools/tests/documents/bench-complet.json:2: "version": 1,
tools/tests/documents/bench-complet.json:398:     "indice": "version      u16          = 2 (défaut) ou 3 (`DRAVE_TRACE_BLOCS=1`)",
tools/tests/documents/bench-complet.json:400:     "passage": "version      u16          = 2 (défaut) ou 3 (`DRAVE_TRACE_BLOCS=1`)",
tools/tests/documents/bench-complet.json:405:     "indice": "puis n_actifs × ( indice u32 · valeur i16 )           [version 1]",
tools/tests/documents/bench-complet.json:407:     "passage": "puis n_actifs × ( indice u32 · valeur i16 )           [version 1]",
tools/tests/documents/bench-complet.json:496:     "indice": "source.sha256\tla découpe est attachée au fichier exact : si la source ",
tools/tests/documents/bench-complet.json:498:     "passage": "source.sha256\tla découpe est attachée au fichier exact : si la source change, le manifeste est invalide",
tools/tests/documents/bench-complet.json:510:     "indice": "Hash — sha256(region.texte) se recalcule, e
… [8623 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn '\"version\"\\]\\|\\[.version.\\]\\|version.*==.*1\\|version.*!=.*1' tools --include='*.py' | grep -v __pycache__ | head -80", "description": "Find code reading annotation version"}`

  ```
tools/diff_flux.py:47:            elif version == 1:
tools/flux_codec.py:46:            if version == 1:
tools/flux_codec.py:95:            if version == 1:
tools/analyse_flux.py:38:        if version == 1:
tools/invariance_semantique.py:31:            if version == 1:
tools/approximabilite_bloc.py:34:            if version == 1:
tools/plateau_multilingue.py:30:            if version == 1:
tools/lecture_plateau.py:34:            if version == 1:
tools/cancellation_langue.py:42:            if version == 1:
tools/contrastif_hors_echantillon.py:39:            if version == 1:
tools/pont_recurrent.py:35:            if version == 1:
tools/applique_pont.py:26:            if version == 1:
tools/sonde_pont.py:33:            if version == 1:
tools/pont_fidele.py:31:            if version == 1:
tools/pont_reservoir.py:34:            if version == 1:
tools/cache_pont.py:22:            if version == 1:
tools/compare_professeurs.py:27:            if version == 1:
tools/sous_ensemble_actif.py:26:            if version == 1:
tools/invariance_unites.py:24:            if version == 1:
tools/seuil_bruit.py:152:    propres = [d["surprisal"] for d in donnees if d["version"] == "propre"]
tools/seuil_br
… [5963 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"schema\\|version\\|partition\\|json\" tools/drave.py | head -80", "description": "Inspect CLI for schema/version"}`

  ```
7:    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
9:    python3 tools/drave.py evaluer --gold --json
11:    python3 tools/drave.py --version
26:import json
57:    return _sur(json.dumps(objet, ensure_ascii=False, indent=1)) + "\n"
62:    return _sur(json.dumps(a.json(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
166:def _analyser_jsonl(texte: str, args: argparse.Namespace) -> int:
167:    """Une **ligne JSON par phrase** (traitement de corpus : `--jsonl`)."""
168:    h = bl.Heuristique(partition=args.partition)
175:        sys.stdout.write(_sur(json.dumps(a.json(), ensure_ascii=False)) + "\n")
185:    if args.jsonl:
186:        return _analyser_jsonl(texte, args)
187:    annotation = bl.Heuristique(partition=args.partition).analyser(texte, args.langue,
191:        if args.json:
192:            sys.stdout.write(_dumps(annotation.json()))
197:    if args.json:
198:        sys.stdout.write(_dumps(annotation.json()))
261:        f"  vue linéaire (partition filtrer) F1 {_pct(rapport['syntagmes_lineaire']['f1'])}  "
279:    # transparence : la vue **fidèle** (défaut) et la vue **linéaire** (partition filtrer)
280:    _lineaire = evalu
… [1216 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '580,625p' docs/produit/exemples.md", "description": "Read exemples ending"}`

  ```
"type": "acte",
      "valeur": "assertion"
    }
  ]
}
```

**Lecture.**

- Le bloc prédit `GN « The film she » [0:12]` (trop large : il absorbe `she`), `GV « talks »`,
  `GV « about is out »`. **Aucune REL** n'est posée.
- La relative est **sans marqueur** (« the film **she talks about** » : le pronom relatif est
  absent). L'heuristique ouvre une REL sur un marqueur explicite (`qui`, `que`, `who`, `which`,
  `when` après un GN…) ; sans marqueur, elle ne la voit pas.
- C'est l'un des **17 spans inatteignables** (8 REL, 5 SUB, 4 GP). Le segment gold n'est pas
  seulement mal attaché : il n'est **pas prédit**, donc il sort du dénominateur de l'exactitude.
- `235/236 = 0,9958` est donc une exactitude **conditionnelle aux spans prédits** ; la
  couverture est **0,9874** (235/239). Les deux chiffres doivent être lus ensemble.
- Le gold attend aussi `GN « The film » [0:8]` ; le bloc le coupe à `[0:12]`. Même un attachement
  correct n'aurait pas compté : le **span** doit être exact.

**Ce qu'il faut en conclure.** Le produit est **précis sur ce qu'il voit, silencieux sur ce qu'il
ne voit pas**. Un utilisateur qui a besoin d'une REL doit vérifier qu'elle est présente dans le
JSON (`type
… [1257 caractères tronqués]
  ```

- **todo_write** `{"todos": [{"content": "Publier le schéma v2 (meta.alternative, meta.partition) et passer le produit en version 2", "status": "in_progress"}, {"content": "Adapter le vérificateur pour lire v1 et v2 (rétro-compatibilité) et valider --gold 20", "status": "pending"}, {"content": "Mettre à jour les test … [247 caractères tronqués]`

  ```
Updated todo list: 4 pending, 1 in progress, 0 completed.
  ```

- **bash** `{"command": "grep -n \"schéma v1\\|schema v1\\|v1\" tools/bloc_linguistique.py | head -30", "description": "Find v1 mentions in main module"}`

  ```
1946:    Le modèle est servi par `llama-server` (`/v1/chat/completions`, `grammar`) : le serveur est
1989:            self.endpoint + "/v1/chat/completions",
2123:            self.endpoint + "/v1/chat/completions",
2293:            self.endpoint + "/v1/chat/completions",
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/schemas/drave-annotation-v2.json", "content": "{\n \"$schema\": \"https://json-schema.org/draft/2020-12/schema\",\n \"$id\": \"https://drave.local/schema/annotation-v2.json\",\n \"title\": \"drave.annotation v2\",\n \"description\" … [5300 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/schemas/drave-annotation-v2.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "old_string": "SCHEMA_ANNOTATION = \"drave.annotation\"\nVERSION_ANNOTATION = 1", "new_string": "SCHEMA_ANNOTATION = \"drave.annotation\"\n# v2 : ajoute `meta.partition` et `meta.alternative` (partition des s … [131 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,sys\nsys.path.insert(0,'.')\nimport fastjsonschema\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\ns=json.load(open('tools/schemas/drave-annotation-v2.json'))\nv=fastjsonschema.compile(s)\nh=bl.Heuristique() … [622 caractères tronqués]`

  ```
OK gold20
OK alternative 612
OK filtrer_union 612
OK filtrer 612
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"verifier_schema_produit.py — valide une annotation `drave.annotation` contre le schéma de sa version.\n\nDeux schémas sont publiés (Draft 2020-12) :\n\n- `tools/schemas/drave-annotation-v1.json` — le contrat d'origine (version 1) ;\n- `tools/schemas/drave-a … [7322 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_schema_produit.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "python3 tools/verifier_schema_produit.py --gold 20; echo \"exit=$?\"", "description": "Run new schema verifier"}`

  ```
✅ fr (v2)
  ✅ en (v2)
  ✅ vide (v2)
  ✅ ponctuation (v2)
  ✅ long (v2)
  ✅ v1 (v1)
  ✅ gold:g001 (v2)
  ✅ gold:g002 (v2)
  ✅ gold:g003 (v2)
  ✅ gold:g004 (v2)
  ✅ gold:g005 (v2)
  ✅ gold:g006 (v2)
  ✅ gold:g007 (v2)
  ✅ gold:g008 (v2)
  ✅ gold:g009 (v2)
  ✅ gold:g010 (v2)
  ✅ gold:g011 (v2)
  ✅ gold:g012 (v2)
  ✅ gold:g013 (v2)
  ✅ gold:g014 (v2)
  ✅ gold:g015 (v2)
  ✅ gold:g016 (v2)
  ✅ gold:g017 (v2)
  ✅ gold:g018 (v2)
  ✅ gold:g019 (v2)
  ✅ gold:g020 (v2)
  ✅ rétro-compatibilité : annotation v1 lue par le schéma v1
  ✅ contrôle négatif : le schéma v2 refuse une annotation v1
  ✅ validateur JSON Schema · 26 cas
exit=0
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_schema_produit.py", "old_string": "\"\"\"test_schema_produit.py — le **contrat** du produit : schéma v1, refus, entrées hostiles.\n\nCe que le test fige (et qu'un client peut supposer) :\n- 8 champs **obligatoires** à la … [1029 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_schema_produit.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_schema_produit.py", "new_string": "RACINE = pathlib.Path(__file__).resolve().parents[2]\nSCHEMA_V1 = RACINE / \"tools\" / \"schemas\" / \"drave-annotation-v1.json\"\nSCHEMA_V2 = RACINE / \"tools\" / \"schemas\" / \"drave … [451 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_schema_produit.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_schema_produit.py", "new_string": "        self.assertEqual(d[\"schema\"], \"drave.annotation\")\n        self.assertEqual(d[\"version\"], 2)", "old_string": "        self.assertEqual(d[\"schema\"], \"drave.annotation\") … [47 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_schema_produit.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_schema_produit.py", "offset": 60}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_schema_produit.py</path>
<type>file</type>
<content>
60:         """Le surrogate ne peut pas passer par argv (l'OS l'encode) : on teste l'API puis l'écriture."""
61:         sys.path.insert(0, str(RACINE))
62:         import tools.bloc_linguistique as bl
63:         a = bl.Heuristique().analyser("Le chat \ud800 dort.", "fr")
64:         d = a.json()
65:         # l'écriture doit tolérer le surrogate (c'est le bug produit d'origine)
66:         texte = json.dumps(d, ensure_ascii=False).encode("utf-8", "replace").decode("utf-8", "replace")
67:         self.assertGreater(len(d["etiquettes"]), 3)
68:         self.assertIn("Le chat", texte)
69: 
70:     def test_rejeu_identique(self):
71:         a = _cli("rejouer", "Le chat dort.")
72:         b = _cli("rejouer", "Le chat dort.")
73:         self.assertEqual(a.returncode, 0, a.stderr[:300])
74:         self.assertEqual(a.stdout, b.stdout)
75: 
76:     def test_mutation_detectee(self):
77:         """Contrôle négatif : un JSON amputé d'un champ obligatoire est bien refusé par le test."""
78:         d = json.loads(_cli("analyser", "Le chat dort.", "--json").stdout)
7
… [261 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_schema_produit.py", "new_string": "    def test_mutation_detectee(self):\n        \"\"\"Contrôle négatif : un JSON amputé d'un champ obligatoire est bien refusé par le test.\"\"\"\n        d = json.loads(_cli(\"analyser\ … [2173 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_schema_produit.py has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"schéma v1\" tools/porte-produit.sh", "description": "Locate v1 labels in gate"}`

  ```
45:  dit ✅ "schéma v1 validé (5 cas + 20 phrases du gold)"
47:  dit ❌ "schéma v1 : validation en échec (voir /tmp/porte-produit-valide.log)"; ko=1
57:  dit ✅ "schéma v1 : $(grep -oE 'Ran [0-9]+ tests' /tmp/porte-produit-schema.log | head -1)"
59:  dit ❌ "schéma v1 en échec (voir /tmp/porte-produit-schema.log)"; ko=1
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/porte-produit.sh')\ns=p.read_text()\ns=s.replace('schéma v1 validé (5 cas + 20 phrases du gold)','schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)')\ns=s.replace('schéma v1 : validation en échec','schéma v2 : validation  … [265 caractères tronqués]`

  ```
45:  dit ✅ "schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)"
47:  dit ❌ "schéma v2 : validation en échec (voir /tmp/porte-produit-valide.log)"; ko=1
57:  dit ✅ "schéma v2 : $(grep -oE 'Ran [0-9]+ tests' /tmp/porte-produit-schema.log | head -1)"
59:  dit ❌ "schéma v2 en échec (voir /tmp/porte-produit-schema.log)"; ko=1
  ```

- **bash** `{"command": "python3 tools/tests/test_schema_produit.py 2>&1 | tail -30; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run schema product tests"}`

  ```
test_v1_reste_lue_et_v2_la_refuse (__main__.TestRetrocompatibilite.test_v1_reste_lue_et_v2_la_refuse)
Le vérificateur choisit le schéma par `version` ; v2 refuse bien une annotation v1. ... ok
test_anglais_meme_schema (__main__.TestSchemaV1.test_anglais_meme_schema) ... ok
test_les_huit_champs_obligatoires (__main__.TestSchemaV1.test_les_huit_champs_obligatoires) ... ok
test_mutation_detectee (__main__.TestSchemaV1.test_mutation_detectee)
Contrôle négatif : un JSON amputé d'un champ obligatoire est bien refusé par le test. ... ok
test_refus_est_une_reponse_json (__main__.TestSchemaV1.test_refus_est_une_reponse_json) ... ok
test_rejeu_identique (__main__.TestSchemaV1.test_rejeu_identique) ... ok
test_surrogate_isole_ne_plante_pas (__main__.TestSchemaV1.test_surrogate_isole_ne_plante_pas)
Le surrogate ne peut pas passer par argv (l'OS l'encode) : on teste l'API puis l'écriture. ... ok
test_le_schema_v2_declare_partition_et_alternative (__main__.TestSchemaV2.test_le_schema_v2_declare_partition_et_alternative)
Les deux champs ajoutés en v2 sont typés, pas seulement tolérés. ... ok

----------------------------------------------------------------------
Ran 8 tests in 1.234s

OK
exit=0
  ```

- **bash** `{"command": "python3 tools/tests/test_produit.py 2>&1 | tail -20; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run product smoke tests"}`

  ```
................
----------------------------------------------------------------------
Ran 16 tests in 3.661s

OK
exit=0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/tests/test_schema_produit.py')\ns=p.read_text()\ns=s.replace('class TestSchemaV1(unittest.TestCase):','class TestSchemaDuProduit(unittest.TestCase):')\np.write_text(s)\nPY\ngrep -n \"class Test\" tools/tests/test_schema_produit.py" … [44 caractères tronqués]`

  ```
34:class TestSchemaDuProduit(unittest.TestCase):
84:class TestSchemaV2(unittest.TestCase):
96:class TestRetrocompatibilite(unittest.TestCase):
  ```

- **bash** `{"command": "sed -n '1,140p' docs/pilotage/en-cours.md", "description": "Read current state doc"}`

  ```
# En ce moment

**Mis à jour : 2026-11-07, 13 h 30 HNE (heure locale, EST).**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
- **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.
>
> **Règle 11** : serveurs loca
… [9983 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"J1\\.3\\|schéma v2\\|B13\" docs/pilotage/roadmap.md docs/pilotage/semaine-autonome.md | head -40", "description": "Find roadmap J1.3 entries"}`

  ```
docs/pilotage/roadmap.md:31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observ
… [7291 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/pensee-schema-v1.json", "description": "Read v1 schema report JSON"}`

  ```
{
 "date": "2026-11-06",
 "ligne": "B13",
 "schema": "drave.annotation",
 "version": 1,
 "champs_obligatoires": [
  "schema",
  "version",
  "texte",
  "langue",
  "script",
  "refus",
  "etiquettes",
  "unites_semantiques"
 ],
 "avant": {
  "cles": 11,
  "refus": "stdout vide, code 1",
  "hostiles": "UnicodeEncodeError / AttributeError"
 },
 "apres": {
  "cles": 13,
  "refus": "JSON + code 3",
  "hostiles": "tolérées (U+FFFD, refus non_texte)"
 },
 "porte_produit": {
  "controles": 8,
  "tests_schema": 6,
  "tests_produit": 8,
  "autotest": "183/183"
 },
 "limites": [
  "pas de fichier JSON Schema publié",
  "codes 0/2/3/1",
  "surrogates remplacés"
 ]
}
  ```

- **bash** `{"command": "sed -n '1,80p' reports/rapport-convention-gv.md; echo '---'; cat reports/pensee-convention-gv.json | head -40", "description": "Read latest report format"}`

  ```
# B13 — la convention des GV : le sujet hors du GV, F1 0,7549 → 0,7902

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.2 · **Date** : 2026-11-07 ·
> **Verdict** : ✅
> Les **322 FP / 180 FN** du plan sont les erreurs **de GV** du gold d'avant `r035` (F1 0,7533) ;
> après `r035` (J1.1), la base courante est **320 FP / 179 FN** (F1 0,7549). Le classement ne
> change pas : **144 FP de sujet (45 %)** dominent, puis 73 d'objet, 39 de troncature. Deux règles
> candidates sont mesurées : **le sujet hors du GV** (F1 **+0,0332**, 0 perte d'attachement) et
> **l'arrêt à l'adverbe final de temps** (F1 **+0,0026**). Les deux sont **gardées** et combinées :
> **F1 0,7549 → 0,7902** (dev **0,7875**, test **0,7962**), **POS 0,8625 inchangée**, **attachement
> 237/238 inchangé** (0 cible perdue), **183/183 portes**. S/D/N2 intouchés.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_sujet_hors_gv`,
> `ADVERBES_TEMPS`, la condition d'adverbe du GV), [`autotest.py`](../tools/pensee/autotest.py)
> (T110–T115, T156 recalés) ; JSON [`pensee-convention-gv.json`](pensee-convention-gv.json).

## 1. Le chiffre du plan et le chiffre courant

Le plan J1.2 po
… [4830 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,collections,json\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\ngold=charger()\nh=bl.Heuristique(partition='alternative')\ngroupes=set(); porteurs=0; alternatives=0; vues=collections. … [1171 caractères tronqués]`

  ```
phrases 612
porteurs 437 groupes 146 alternatives 930 retires 0
vues Counter({'alternative': 437})
types {'GN': 393, 'GP': 49, 'GV': 357, 'REL': 103, 'SUB': 28}
relations {'croise': 386, 'inclus': 263, 'inclut': 263, 'meme_span': 18}
annotations validees 1836
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"\"; echo \"exit=$?\"; echo '---json---'; python3 tools/drave.py analyser \"\" --json; echo \"exit=$?\"", "description": "Check refusal output current"}`

  ```
exit=3
---json---
{
 "schema": "drave.annotation",
 "version": 2,
 "texte": "",
 "langue": "und",
 "script": "Zyyy",
 "source": "heuristique",
 "refus": "vide",
 "etiquettes": [],
 "unites_semantiques": [],
 "fraction_semantique": 0.0,
 "trace": [
  {
   "etape": "refus",
   "raison": "vide"
  }
 ],
 "cout": {
  "octets": 0
 },
 "contexte": ""
}
exit=3
[stderr]
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\" --json | head -5; echo '---'; python3 tools/drave.py analyser \"Le chat de la voisine qui dort sur le toit se réveille.\" --json | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['schema'],d['version']); print([(e['type'],e … [160 caractères tronqués]`

  ```
{
 "schema": "drave.annotation",
 "version": 2,
 "texte": "Le chat dort.",
 "langue": "fr",
---
drave.annotation 2
[('GN', None, 0), ('GP', None, 0), ('REL', {'groupe': 0, 'rang': 2, 'membres': 3, 'vue': 'alternative'}, 2), ('REL', {'groupe': 0, 'rang': 1, 'membres': 3, 'vue': 'alternative'}, 2), ('GV', {'groupe': 0, 'rang': 3, 'membres': 3, 'vue': 'alternative'}, 2)]
  ```

- **bash** `{"command": "python3 tools/drave.py --aide", "description": "Read CLI help"}`

  ```
usage: drave [-h] [-V] {analyser,evaluer,rejouer} ...

Point d'entrée produit du bloc linguistique (analyse heuristique).

arguments:
  {analyser,evaluer,rejouer}
    analyser            étiqueter un texte (POS, syntagmes, pragmatique)
    evaluer             mesurer l'heuristique sur le gold
    rejouer             analyser deux fois et vérifier le déterminisme

options:
  -h, --help, --aide    afficher cette aide et quitter
  -V, --version         afficher la version et quitter

Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse (JSON) · 1 erreur.
Options : --json, --langue fr|en, --partition brut|alternative|filtrer_union|filtrer, --contexte.
Limites : heuristique CPU, hors ligne, déterministe ; ni neuronal, ni restitution, ni traduction.
Exemples :
  python3 tools/drave.py analyser "Le chat dort."
  python3 tools/drave.py evaluer --gold --json
  ```

- **bash** `{"command": "grep -n '\"version\"\\|\"schema\"' docs/produit/exemples.md | head -30; echo '---'; grep -c '^```json' docs/produit/exemples.md; grep -n '^```json' docs/produit/exemples.md | head -20", "description": "Check example JSON version fields"}`

  ```
---
6
84:```json
191:```json
314:```json
471:```json
500:```json
524:```json
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "> **Vérifié le 2026-11-07** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est\n> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer` et `--version` existent, et la\n> porte … [844 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 60}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
1: # Le premier produit — analyser un texte avec Drave
2: 
3: > **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
4: > linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
5: > il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
6: > qu'il garantit.
7: >
8: > **Vérifié le 2026-11-06** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
9: > **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer` et `--version` existent, et la
10: > porte produit est verte. Les exemples du § 3 sont réels : ils ont été lancés pour ce document.
11: > Ce qui manque encore au contrat est nommé au § 7, sans être présenté comme acquis.
12: >
13: > **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,
14: > classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses
15: > candidats, de façon **déterministe**, et il sait **se mesurer** sur un gold de 612 phrases.
16: 
17: ## 1. À qui s'adres
… [3335 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "> **Vérifié le 2026-11-07** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est\n> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer` et `--version` existent, et la\n> porte … [844 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **développeur NLP** | un JSON déterministe, des spans, une confiance, des candidats | le format est **versionné** (schéma v2) ; v1 reste lue (§ 7) |", "old_string": "| **développeur NLP** | un JS … [105 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "Une seule opération : `analyser(texte, langue)` → une **annotation**. Elle porte neuf niveaux ;\nle produit en expose cinq, plus le coût et la trace. Le JSON est estampillé `schema`\n(`\"drave.anno … [293 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 30, "offset": 138}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
138: l'**exactitude** sur les 236 segments dont le span est prédit. Les 3 cibles restantes n'ont pas
139: de segment au bon span : c'est un plafond de **couverture**, pas d'attachement. `--gold` mesure
140: le gold gelé 602 (F1 65,11 %, POS 85,32 %). La commande sort **0** : elle ne teste pas la cascade
141: (voir § 4).
142: 
143: ### 3.3 quater Traiter un corpus
144: 
145: ```bash
146: python3 tools/drave.py analyser --fichier corpus.txt --jsonl   # une ligne JSON par phrase
147: python3 tools/drave.py analyser --fichier corpus.txt --json    # le texte entier
148: ```
149: 
150: `--fichier` lit un texte UTF-8 ; `--jsonl` rend une **ligne JSON par phrase** (le format des
151: traitements de corpus), chaque ligne portant le schéma v1 complet.
152: 
153: ### 3.3 bis La vue des syntagmes qui se chevauchent
154: 
155: ```bash
156: python3 tools/drave.py analyser "Le chat de la voisine qui dort sur le toit se réveille." --partition filtrer
157: ```
158: 
159: Quatre vues (`--partition`) : `alternative` (défaut : les deux segments restent, `meta.alternative`
160: dit lequel est
… [470 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "`--fichier` lit un texte UTF-8 ; `--jsonl` rend une **ligne JSON par phrase** (le format des\ntraitements de corpus), chaque ligne portant le schéma **v2** complet (`version: 2`).", "old_string": " … [162 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "Quatre vues (`--partition`) : `alternative` (défaut : les deux segments restent, `meta.alternative`\ndit lequel est préféré — **aucune perte**), `filtrer` (vue linéaire : **F1 +0,047** mais **18\na … [800 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 30, "offset": 186}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
186:   JSON       : 11700 octets · sha256 b0a1709a97abe8d4…
187: ```
188: 
189: **Lecture.** La commande analyse **deux fois**, compare le JSON **canonique** (clés triées,
190: durée exclue) et rend une empreinte sha256. Deux exécutions indépendantes rendent le même octet :
191: l'analyse est déterministe. C'est la garantie de base du rejeu.
192: 
193: ### 3.5 Le refus, et la langue inconnue
194: 
195: ```bash
196: python3 tools/drave.py analyser ""; echo "exit=$?"
197: ```
198: ```
199: drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
200: exit=1
201: ```
202: 
203: **Lecture.** Le CLI traite le refus comme une **erreur** : message sur `stderr`, **rien sur
204: `stdout`**, code **1**. Le bloc, lui, rend un JSON avec `refus: "vide"` (voir `exemples.md` § 4) :
205: c'est l'API qui porte l'état, le CLI qui le traduit en code. Un texte vide n'est jamais une
206: annotation « comme les autres ». Pour la langue, `und` est une réponse honnête : « Élodie
207: sourit. » rend `langue=und` (confiance 0,04 < seuil 0,12), même avec `--langue fr
… [557 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py rejouer \"Le chat de la voisine qui dort sur le toit se réveille.\"", "description": "Get current rejouer hash and size"}`

  ```
rejeu identique : oui
  texte      : 'Le chat de la voisine qui dort sur le toit se réveille.'
  langue     : fr
  étiquettes : 60
  JSON       : 13284 octets · sha256 31f3798beebe22f7…
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\" | head -4; echo '---'; python3 tools/drave.py rejouer \"Le chat dort.\"", "description": "Check simple analysis output and hash"}`

  ```
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
---
rejeu identique : oui
  texte      : 'Le chat dort.'
  langue     : fr
  étiquettes : 20
  JSON       : 4227 octets · sha256 f4b7822076a4203d…
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\"", "description": "Capture full simple analysis output"}`

  ```
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
  ```

- **bash** `{"command": "sed -n '172,190p' docs/produit/README.md", "description": "Read rejouer block"}`

  ```
Le champ `contexte` est porté dans le JSON ; il alimente la mémoire de discours (coréférence,
connecteurs) sans changer le texte analysé.

### 3.4 Rejouer et vérifier le déterminisme

```bash
python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
```
```
rejeu identique : oui
  texte      : 'Le chat de la voisine qui dort sur le toit se réveille.'
  langue     : fr
  étiquettes : 59
  JSON       : 11700 octets · sha256 b0a1709a97abe8d4…
```

**Lecture.** La commande analyse **deux fois**, compare le JSON **canonique** (clés triées,
durée exclue) et rend une empreinte sha256. Deux exécutions indépendantes rendent le même octet :
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "rejeu identique : oui\n  texte      : 'Le chat de la voisine qui dort sur le toit se réveille.'\n  langue     : fr\n  étiquettes : 60\n  JSON       : 13284 octets · sha256 31f3798beebe22f7…\n```",  … [211 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "```bash\npython3 tools/drave.py analyser \"\"; echo \"exit=$?\"\n```\n```\ndrave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)\nexit=3\n```\n\n**Lecture.** Le r … [1340 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '82,110p' docs/produit/README.md", "description": "Read simple example block"}`

  ```
```
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 19 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.92 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
```

**Lecture.** La phrase est reconnue comme française, deux syntagmes sont posés, chacun avec sa
cible : le GN « Le chat » est rattaché à « dort », le GV « dort » à « chat ». Le gold `g001`
attend exactement ces deux spans et `assertion`. `POS` est la suite des mots ; `COUVERTURE` est
la **confiance maximale déclarée** par niveau, pas une précision.

### 3.2 Analyser en JSON et lire l'attachement

```bash
python3 tools/drave.py analyser "Le livre que j'ai lu est intéressant." --json \
  | jq -r '[.etiquettes[] | select(.niveau=="syntagme")
           | "\(.type) \(.valeur) → \(.meta.attachement.cible // "—")"] | join(" · ")'
```
… [131 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "drave 0.1.0 — analyse heuristique (CPU, hors ligne)\nlangue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)\nPOS  Le/DET chat/NOUN dort/VERB ./PONCT\nSYNTA … [961 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"manque de schéma\\|Pas de texte arbitraire\\|Pas de calibration\\|Pas de schéma\" docs/produit/README.md", "description": "Locate stale schema mentions in section 4"}`

  ```
263:**9. Pas de calibration des confiances.** `confiance` est **déclarée** (0,3 pour un NOUN ouvert,
267:**10. Pas de texte arbitraire garanti.** Les mesures sont sur le gold ; les règles y ont été
269:JSON change de forme — d'où le rejeu et le contrôle par un gold à soi (§ 7, manque de schéma).
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**10. Pas de texte arbitraire garanti.** Les mesures sont sur le gold ; les règles y ont été\ndessinées. Sur un texte hors domaine, la couverture et la précision peuvent baisser sans que le\nJSON c … [461 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '300,360p' docs/produit/README.md", "description": "Read guarantees and codes section"}`

  ```
| **refus explicite** | texte vide ou sans lettre/chiffre → `refus: "vide"`, 0 étiquette | bloc : JSON ; CLI : `stderr` + code 1 |
| **pas d'invention** | chaque étiquette porte `source`, `confiance`, `candidats` ; `und` plutôt qu'une langue forcée | JSON ; `--langue` est un indice |
| **spans lisibles** | indices en **points de code Unicode**, 0-based, `[debut:fin)` | « Élodie » → `[0:6]` ; emoji = 1 point |
| **UTF-8** | le JSON est en UTF-8, non échappé, sans durée | `--json` ; `test_produit.py` vérifie l'absence de `duree_s` |
| **gold versionné** | les 4 gold sont dans le dépôt ; `evaluer` rejoue hors ligne | `tools/tests/linguistique/gold*.json` |
| **porte produit** | version, JSON fr/en, rejeu, smoke test, autotest | `bash tools/porte-produit.sh` → ✅ |

**La porte produit, mesurée le 06/11** : `✅ porte produit verte` — `drave 0.1.0`, JSON valide et
étiqueté en `fr` et `en`, `sha256 6b6def477a493444` deux fois, **6 tests** de fumée,
**183/183** portes d'autotest. Le smoke test est `tools/tests/test_produit.py`.

**Codes de sortie — ce qui existe.** Le CLI implémente **0 / 1 / 2** ; le contrat cible **3 / 4**
n'est pas encore là :

| code | sens | aujourd'hui |
|---:|---|---|
… [1731 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '360,410p' docs/produit/README.md", "description": "Read options table and missing list"}`

  ```
**Options du CLI** :

| option | commande | sens |
|---|---|---|
| `--langue fr\|en` | `analyser`, `rejouer` | **indice** de langue, pas une contrainte ; hors `fr`/`en` → code 2 |
| `--json` | `analyser`, `evaluer` | sortie machine UTF-8 |
| `--gold` | `evaluer` | gold gelé 602 au lieu du vivant 612 |
| `-V`, `--version` | global | `drave 0.1.0` |
| `-h`, `--aide` | global | l'aide, largeur fixe |

**Ce qui manque encore** (le contrat cible, non livré) :

| manque | conséquence |
|---|---|
| **`--fichier` / l'entrée standard** | on ne peut analyser qu'un texte passé en argument ; pas de pipe, pas de fichier |
| **`--sortie`** | pas d'écriture directe d'un JSON ; il faut rediriger le shell |
| **`rejouer` sur un JSON sauvegardé** | `rejouer` prend un **texte**, pas une annotation ; on ne peut pas rejouer un fichier produit hier |
| **les codes 3 et 4** | le refus est confondu avec une erreur (code 1) et n'a pas de JSON sur `stdout` ; une dépendance absente n'est pas distinguée |
| **un champ `schema` / une version de format** | impossible d'épingler un rejeu à une version ; `--version` ne donne que `0.1.0`, sans commit ni schéma |
| **`--mode` / la cascade** | le CLI n'expose que l'
… [2805 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **refus explicite** | texte vide ou sans lettre/chiffre → `refus: \"vide\"`, 0 étiquette | bloc : JSON ; CLI : JSON sur `stdout` + code 3 |", "old_string": "| **refus explicite** | texte vide ou  … [96 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **gold versionné** | les 4 gold sont dans le dépôt ; `evaluer` rejoue hors ligne | `tools/tests/linguistique/gold*.json` |\n| **format versionné** | `schema: \"drave.annotation\"`, `version: 2` ; … [233 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**Codes de sortie — ce qui existe.** Le CLI implémente **0 / 1 / 2 / 3** ; le code **4** (dépendance\nabsente) n'est pas encore là :\n\n| code | sens | aujourd'hui |\n|---:|---|---|\n| **0** | succ … [1600 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "```bash\npython3 tools/drave.py --version\npython3 tools/drave.py --aide\npython3 tools/drave.py analyser \"Le chat dort.\" [--langue fr|en] [--json] \\\n    [--partition brut|alternative|filtrer_u … [605 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --gold 2>&1 | head -20", "description": "Get current eval gold output"}`

  ```
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold gelé (référence figée) · 602 phrases · 3141 tokens · 239 cibles d'attachement

POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.14 %)
SYNTAGMES   F1 78.82 %  (P 78.18 % / R 79.46 %)
  tête      F1 90.25 %  (P 92.34 % / R 88.26 %)
  vue linéaire (partition filtrer) F1 81.27 %  · attachement 92.05 % de couverture
ATTACHEMENT exact 97.49 % · couverture 97.91 % · exact sur span 99.57 % · top-k 97.07 %
  tête      couverture 100.00 % · top-k 99.15 %
PRAGMATIQUE acte 99.67 % · négation 97.67 % · modalité 98.84 % · double sens 94.35 %
FRACTION SÉMANTIQUE 54.96 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer 2>&1 | head -20", "description": "Get current eval live output"}`

  ```
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement

POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)
SYNTAGMES   F1 79.02 %  (P 78.60 % / R 79.44 %)
  tête      F1 90.29 %  (P 92.61 % / R 88.08 %)
  vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture
ATTACHEMENT exact 99.16 % · couverture 99.58 % · exact sur span 99.58 % · top-k 98.74 %
  tête      couverture 100.00 % · top-k 99.16 %
PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %
FRACTION SÉMANTIQUE 54.76 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**Sorties réelles des commandes** (07/11 pour le format ; les valeurs d'`evaluer` sont celles\nmesurées le 06/11) :", "old_string": "**Sorties réelles des commandes** (07/11, format v2) :"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "$ python3 tools/drave.py rejouer \"Le chat dort.\"\nrejeu identique : oui\n  texte      : 'Le chat dort.'\n  langue     : fr\n  étiquettes : 20\n  JSON       : 4227 octets · sha256 f4b7822076a4203d … [229 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| option | commande | sens |\n|---|---|---|\n| `--langue fr\\|en` | `analyser`, `rejouer` | **indice** de langue, pas une contrainte ; hors `fr`/`en` → code 2 |\n| `--json` | `analyser`, `evaluer`  … [936 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **l'entrée standard** | `--fichier` lit un fichier, mais pas de pipe (`cat corpus.txt \\| drave analyser`) |", "old_string": "| **`--fichier` / l'entrée standard** | on ne peut analyser qu'un tex … [54 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **le code 4** | une dépendance absente n'est pas distinguée d'une erreur (code 1) |", "old_string": "| **les codes 3 et 4** | le refus est confondu avec une erreur (code 1) et n'a pas de JSON sur … [215 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **un répertoire** | `--fichier` lit un fichier ; pas de parcours de répertoire |", "old_string": "| **un lot de textes** | une invocation = un texte ; pas de JSONL, pas de répertoire |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**Ce qui est déjà tenu** : `--version`, `--aide`, les trois sous-commandes, le JSON déterministe,\nle rejeu par empreinte, le **format versionné** (schéma v2, v1 lue), `--fichier`/`--jsonl`,\n`--pa … [349 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **voir cinq JSON commentés** | [`exemples.md`](exemples.md) |\n| **le schéma du JSON** (v2 : `meta.partition`, `meta.alternative`) | [`tools/schemas/drave-annotation-v2.json`](../../tools/schemas … [266 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "> `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1\n> reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les exemples du § 3 ont été relancés le\n> … [593 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "limit": 45}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md</path>
<type>file</type>
<content>
1: # Cinq exemples d'analyse, commentés
2: 
3: > **Ce que ce document est.** Cinq exécutions **réelles** du produit, avec leur JSON commenté. Il
4: > complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce document dit
5: > *comment lire* ce qui sort. Les sorties ont été produites le **2026-11-06** sur la branche
6: > `s/v7`, avec le CLI `tools/drave.py` (version **0.1.0**), sans modèle, sans GPU et sans réseau.
7: >
8: > **Une commande, un JSON.** `python3 tools/drave.py analyser "…" --json` rend l'annotation
9: > complète (neuf niveaux). Pour la lire, ce document filtre avec `jq` ; le produit, lui, n'a pas
10: > besoin de `jq`.
11: 
12: ## 0. Comment lire les JSON
13: 
14: - `debut` / `fin` : indices en **points de code Unicode**, 0-based, fin exclue : `[debut:fin)`.
15:   « Élodie » → `[0:6]` ; un emoji compte pour **un** point.
16: - `niveau` : `pos`, `syntagme`, `phrase` et `pragmatique` sont montrés ; `graphème`, `mot`,
17:   `morphème`, `discours` et `document` sont omis (ils existent dans le JSON complet).
18: - `confiance` : **déclarée**, p
… [1571 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "offset": 608}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md</path>
<type>file</type>
<content>
608: 1. **Pas de restitution, pas de traduction, pas de génération** : la sortie ne contient aucun
609:    texte produit ; seulement des étiquettes. Le produit ne réécrit pas la phrase.
610: 2. **Pas de neuronal** : tout vient de `Heuristique` (CPU) ; `MockNeuronal` est un contrat, pas un
611:    tagger, et le CLI ne l'expose pas. La cascade 7B (0,9415) n'est pas un chemin livré.
612: 3. **Pas de couverture complète** : 17 cibles sur 239 restent inatteignables (8 REL, 5 SUB, 4 GP) ;
613:    l'exemple `r035` en est un cas réel.
614: 4. **Pas de lecture unique garantie** : le **doublon REL de l'union** (`union: true`) est publié ;
615:    il faut le filtrer si l'on veut un seul segment par span.
616: 5. **Pas de schéma stable** : `candidats` sont des chaînes, `role` n'est pas normalisé, et le JSON
617:    n'a pas de champ `version` (notice § 7).
618: 
619: Pour mesurer sur votre propre corpus, il faut le format du gold (mots + segments + pragma) : il
620: n'est pas publié comme schéma — c'est un des manques du CLI (notice § 7).
621: 
622: ## 7. Où aller ensuite
623: 
624:
… [556 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "new_string": "> **Ce que ce document est.** Cinq exécutions **réelles** du produit, avec leur JSON commenté. Il\n> complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce document dit\n> * … [852 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "new_string": "- `meta.attachement` : `{segment, cible}` ; `cible` est une **chaîne**, pas un span.\n- `meta.partition` : `{groupe, rang, membres, vue}` — présent sur un syntagme d'un groupe de\n  chevauchement … [545 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "new_string": "  syntagmes: [.etiquettes[] | select(.niveau==\"syntagme\")\n        | {valeur, type, debut, fin, confiance, role:.meta.role,\n           cible:.meta.attachement.cible, union:.meta.union,\n       … [295 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "new_string": "5. **Pas de valeurs normalisées** : `candidats` sont des chaînes et `role` n'est pas normalisé\n   (`predicat`/`prédicat`). Le **format** est versionné (v2 ; v1 reste lue), mais le vocabulaire\n  … [686 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md", "new_string": "| **la notice d'usage** | [`README.md`](README.md) |\n| **le schéma du JSON (v2, v1)** | [`drave-annotation-v2.json`](../../tools/schemas/drave-annotation-v2.json) · [`drave-annotation-v1.json`]( … [119 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md has been updated successfully.
  ```

- **write** `{"content": "# B13 — le schéma v2 : `meta.partition` et `meta.alternative` typés, version 2, v1 toujours lue\n\n> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.3 · **Date** : 2026-11-07 ·\n> **Verdict** : ✅\n> **Ce qui change pour un client** : l'annotation porte `schema: \"drav … [6044 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v2.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "{\n \"date\": \"2026-11-07\",\n \"ligne\": \"B13\",\n \"tache\": \"J1.3\",\n \"objet\": \"le schéma v2 de l'annotation\",\n \"schema\": \"drave.annotation\",\n \"version\": 2,\n \"schemas\": {\n  \"v2\": \"tools/schemas/drave-annotation-v2.json\",\n  \"v1\": \"tools/schemas/drave-annota … [1960 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-schema-v2.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "grep -n \"schema-v1\\|convention-gv\\|rapport-schema\" reports/INDEX.md reports/README.md | head -20; echo '---head index---'; sed -n '1,30p' reports/INDEX.md", "description": "Inspect reports index convention"}`

  ```
reports/INDEX.md:118:| [rapport-convention-gv.md](rapport-convention-gv.md) | B13 — la convention des GV : le sujet hors du GV, F1 0,7549 → 0,7902 |
reports/INDEX.md:679:| [rapport-schema-v1.md](rapport-schema-v1.md) | B13 — le contrat v1 : `schema`/`version`, refus en JSON (code 3), entrées hostiles tolérées |
reports/README.md:18:| [`rapport-convention-gv.md`](rapport-convention-gv.md) | GV : F1 **0,7902** |
reports/README.md:38:| [`rapport-schema-v1.md`](rapport-schema-v1.md) | **B13** — le contrat v1 : `schema`/`version`, refus JSON code 3, schéma publié, 9 contrôles |
---head index---
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **704 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.

| fiche | titre |
|---|---|
| [07-mesures-couche-commune.md](07-mesures-couche-commune.md) | 7. Les modèles alternatifs pour l'entrée et la sortie — vers une couche commune |
| [aiguille-30b.md](aiguille-30b.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf |
| [aiguille-gpt-oss.md](aiguille-g
… [2561 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/index_reports.py; echo '---'; grep -n \"README\" tools/index_reports.py | head -20", "description": "Inspect reports index generator"}`

  ```
#!/usr/bin/env python3
"""index_reports.py — génère reports/INDEX.md à partir des en-têtes de fiches.

L'index est **exhaustif** et **déterministe** : une ligne par fiche, triée par nom,
avec son titre (premier `# `). Les fichiers d'infrastructure (`README.md`, `INDEX.md`
et `historique-*`) sont exclus du tableau ; les compteurs de `docs/pilotage/en-cours.md`
comptent, eux, tous les `.md` de `reports/`.

Usage :
    python3 tools/index_reports.py              # réécrit reports/INDEX.md
    python3 tools/index_reports.py --verifier   # ne réécrit rien, sort 1 si périmé
    python3 tools/index_reports.py --aide       # affiche l'aide (ne touche à rien)
"""
from __future__ import annotations

import argparse
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent


def titre(p: pathlib.Path) -> str:
    for ligne in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if ligne.startswith("# "):
            return ligne[2:].strip().replace("|", "—")
    return p.stem.replace("-", " ")


def fiches() -> list[pathlib.Path]:
    return sorted(
        p for p in (RACINE / "reports").glob("*.md")
        if p.name not in ("README.md", "INDEX.md") and not p.n
… [1679 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 50}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
1: # Les rapports — données intermédiaires et références
2: 
3: > **Ce dossier porte les résultats et les données de nos travaux**, jamais la documentation de référence
4: > (elle est dans [`docs/`](../docs/)). Les fiches courantes sont citées depuis le tableau de bord
5: > [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md).
6: 
7: > **Navigation** : [la carte des sujets](../docs/theorie/carte.md) · [l'état du moment](../docs/pilotage/en-cours.md) ·
8: > [l'inventaire des docs](../docs/README.md) · [le journal](../journal/README.md).
9: >
10: > **Contexte** : la fiche [`07-mesures-couche-commune.md`](07-mesures-couche-commune.md) est un **hub** de
11: > **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par
12: > partie**, jamais en entier ; l'index exhaustif des fiches est [`INDEX.md`](INDEX.md).
13: 
14: ## Les fiches courantes
15: 
16: | fichier | ce qu'il porte |
17: |---|---|
18: | [`rapport-convention-gv.md`](rapport-convention-gv.md) | GV : F1 **0,7902** |
19: | [`rapport-r035.md`](rapport-r035.md) | **B13** — rela
… [3857 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-schema-v2.md`](rapport-schema-v2.md) | **B13** — schéma v2 : `meta.partition`/`meta.alternative`, version 2, v1 lue |\n| [`rapport-schema-v1.md`](rapport-schema-v1.md) | **B13** — le contrat … [237 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '18,34p' docs/pilotage/semaine-autonome.md; echo '---'; sed -n '82,92p' docs/pilotage/semaine-autonome.md", "description": "Read semaine autonome schema entries"}`

  ```
## 2. L'inventaire — ce qui est ouvert

### 2.1 Drave — le produit (priorité)

| reste | mesure | où |
|---|---|---|
| 1 span (`g017` arbitrage d'adverbe) ; `r035` relative zéro **réglé** | attachement exact **237/238 (0,9958)** | [`rapport-r035.md`](../../reports/rapport-r035.md) |
| la convention des GV (322 FP / 180 FN) — **réglée** (sujet hors du GV + adverbe final) | F1 **0,7902** (linéaire 0,8144) ; attachement **237/238** | [`rapport-convention-gv.md`](../../reports/rapport-convention-gv.md) |
| `meta.alternative` hors schéma v1 | le schéma publié | [`tools/schemas/`](../../tools/schemas/) |
| la restitution (annotation → texte) | miroir **0,2276** | [`../methode/miroir.md`](../methode/miroir.md) |

### 2.2 Drave — les chantiers voisins (coordination)

| chantier | état | ce qui reste | territoire |
|---|---|---|---|
| **N2** | porte propre **2,7856** à 1 024 (manque 0,29) | `porte-n2.sh` (deux seuils), le mètre RoPE à corriger | N2 (lecture seule) |
---
+ son **JSON**, la mise à jour de l'**état**, un **commit vérifié** par l'agent principal (les
sous-agents ne committent jamais).

| jour | vague | objet | livrable mesuré |
|---|---|---|---|
| **J1 · 07/11** | matin | le pr
… [668 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/index_reports.py && python3 tools/index_reports.py --verifier; echo \"index=$?\"", "description": "Regenerate reports index"}`

  ```
705 fiches → reports/INDEX.md
index=0
  ```

- **bash** `{"command": "python3 tools/tests/test_produit_libre.py 2>&1 | tail -8; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run free-text product tests"}`

  ```
test_deterministe (__main__.TestProduitLibre.test_deterministe) ... ok
test_filtrer_sans_chevauchement (__main__.TestProduitLibre.test_filtrer_sans_chevauchement) ... ok
test_non_linguistiques_sans_syntagme (__main__.TestProduitLibre.test_non_linguistiques_sans_syntagme) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.312s

OK
exit=0
  ```

- **bash** `{"command": "bash tools/porte-produit.sh 2>&1 | tee /tmp/porte-produit-schema-v2.log; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run product gate", "run_in_background": true}`

  ```
started background job bash-65
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run documentation review"}`

  ```
revue de documentation · 708 fiche(s) · 801 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 707 fichiers, le disque en a 708
     · compteurs : en-cours.md dit 800 JSON, le disque en a 801
exit=1
  ```

- **bash** `{"command": "python3 tools/verifier_schemas.py 2>&1 | tail -20; echo \"exit=${PIPESTATUS[0]}\"", "description": "Verify SVG schemas"}`

  ```
schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
exit=0
  ```

- **job_output** `{"job_id": "bash-65", "wait": true, "timeout_ms": 300000}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f4b7822076a4203d deux fois
  ✅ smoke test : Ran 16 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
exit=0
[status: completed, exit code: 0]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**La porte produit, mesurée le 07/11** : `✅ porte produit verte` — `drave 0.1.0`, JSON valide et\nétiqueté en `fr` et `en`, `sha256 f4b7822076a4203d` deux fois, **16 tests** de fumée, **8 tests**\n … [438 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M %Z'", "description": "Get current local time"}`

  ```
2026-11-07 14:21 EST
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-07, 14 h 20 HNE (heure locale, EST).**", "old_string": "**Mis à jour : 2026-11-07, 13 h 30 HNE (heure locale, EST).**"}`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-07, 13 h 30 HNE (heure locale, EST).**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11
9: 
10: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
11: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
12: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
13: - **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
14: - **Bloquants** : aucun.
15: - **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).
16: 
17: ## Sessions en cours
18: 
19: > Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
20: > [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
21: > `plan.md` (`python3 tools/sessions
… [8932 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-07, 14 h 20 HNE (heure locale, EST).**", "old_string": "**Mis à jour : 2026-11-07, 13 h 30 HNE (heure locale, EST).**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors d … [1021 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183**, gold 432, DRVM 114/114 + 5/5, sto 5/5 ; pragmatique 130/432 ; la fusion garde l'heuristique ; **`r035` réglé** (237/238, 0,9958) ; **convention des GV r … [463 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| portes | **84** (dont `porte-produit` le 07/11) | `tools/porte-*.sh` |\n| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |\n| fichiers / JSON de résultats | **708** / **801** … [290 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 et convention des GV faits (F1 0,7902, 237/238), schéma v2 publié (v1 lue)** | **J1. … [357 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
120: | **Backlog — graphe** | **37 fiches, 43 arêtes, 3 à la frontière** | 1 ligne sans fiche | `verifie_backlog.py` |
121: 
122: **C1** · **C2** · **C3** · **C4** · **C5** · **C6** · **C7** — hors graphe.
123: 
124: ## Ce qui reste
125: 
126: **N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035` et convention des GV faits**, reste `g017` (J1.3/J1.4) ; **S** — poursuivre la validation ; **N4** — consigne ; **B10.3** — `z` ; **B13** — 183/183 ; **R0.7** — tagger ; **D** — **restauré** : le corpus à **62 documents** (Choquette + Assurance ; DOC1/DOC2, quasi-doublons, écartés) est en place (`data/corpus_ocr_cegep` : train 4 440 987, val 12 536, test 10 524 ; 8 Ko 0, 500 o 0) ; [fiche](../../reports/rapport-ocr-cegep-64.md) ; **la passe complète est finie** (`work/portes/passe-2404-23h45` ; **79 vertes, 4 rouges** : `indice`, `melange` tolérées ; `lecteur` corrigée ; `sessions` → heartbeat de `e181ce02` à rafraîchir).
127: 
128: ## Les questions ouvertes
129: 
130: - **R1** : **1 024 octets** ? → **R1.2**
… [905 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035`, convention des GV et schéma v2 faits**, reste **J1.4 restitution** pui … [1355 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 10, "offset": 35}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
35: | **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **fusion réparée par niveau : 0,9309/0,8226/0,8784/0,9954 (le max)** ([fiche](../../reports/rapport-pensee-fusion-reparee.md)) | la **pragmatique neuronale** ; le **refus r353** |
36: | **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67,73 G car., 81,2 Go, **8 Ko 0**) ; **PDF** (1 927 doc., 322 Mo) ; **documents** (3 384 doc., 872 M car., 8 Ko 2,07 %) ; **OCR** (20 livres, 7 381 p, 15,36 M, 8 Ko 0 ; [CEGEP](../theorie/glossaire
… [1834 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**État au 07/11 14 h 20.** B13 : **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span (`g017`) + 1 cible fausse (`s065`)** ; **183/183** ; **`r035`** (relative zéro) r … [1250 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "limit": 14, "offset": 20}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md</path>
<type>file</type>
<content>
20: 
21: ### 2.1 Drave — le produit (priorité)
22: 
23: | reste | mesure | où |
24: |---|---|---|
25: | 1 span (`g017` arbitrage d'adverbe) ; `r035` relative zéro **réglé** | attachement exact **237/238 (0,9958)** | [`rapport-r035.md`](../../reports/rapport-r035.md) |
26: | la convention des GV (322 FP / 180 FN) — **réglée** (sujet hors du GV + adverbe final) | F1 **0,7902** (linéaire 0,8144) ; attachement **237/238** | [`rapport-convention-gv.md`](../../reports/rapport-convention-gv.md) |
27: | `meta.alternative` hors schéma v1 | le schéma publié | [`tools/schemas/`](../../tools/schemas/) |
28: | la restitution (annotation → texte) | miroir **0,2276** | [`../methode/miroir.md`](../methode/miroir.md) |
29: 
30: ### 2.2 Drave — les chantiers voisins (coordination)
31: 
32: | chantier | état | ce qui reste | territoire |
33: |---|---|---|---|

(Showing lines 20-33 of 140. Use offset=34 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "new_string": "| `meta.alternative` / `meta.partition` — **publiés en v2** (v1 lue) | 26 cas, 0 échec | [`rapport-schema-v2.md`](../../reports/rapport-schema-v2.md) |", "old_string": "| `meta.alternati … [84 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo \"exit=${PIPESTATUS[0]}\"", "description": "Re-run documentation review"}`

  ```
revue de documentation · 708 fiche(s) · 801 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo \"exit=${PIPESTATUS[0]}\"", "description": "Verify state file"}`

  ```
en-cours · 1649 mots · 7 sections · 4 session(s) · 5 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
exit=0
  ```

- **bash** `{"command": "git status --short; echo '---diff stat---'; git diff --stat; echo '---untracked---'; git status --porcelain | grep '^??'", "description": "Inspect working tree changes"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/pilotage/semaine-autonome.md
 M docs/produit/README.md
 M docs/produit/exemples.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-e1ad947b-50b1-4758-a921-5267225bf642/digest.md
 M journal/sessions/session-e1ad947b-50b1-4758-a921-5267225bf642/rapport.md
 M reports/INDEX.md
 M reports/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/bloc_linguistique.py
 M tools/chantier/superviseur.py
 M tools/porte-produit.sh
 m tools/structures
 M tools/tests/test_schema_produit.py
 M tools/verifier_schema_produit.py
?? journal/sessions/session-614644be-9315-4734-9b97-236a792f4dc5/
?? reports/pensee-schema-v2.json
?? reports/rapport-s-paragraphes.md
?? reports/rapport-schema-v2.md
?? tools/schemas/drave-annotati
… [1974 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"contrat v1\\|schéma v1\\|schema v1\" docs/produit docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/semaine-autonome.md reports/rapport-schema-v2.md | head -40", "description": "Find remaining v1 references in touched docs"}`

  ```
docs/pilotage/en-cours.md:66:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors du GV + adverbe final : 320/179 → GV F1 0,7549 → 0,7902, 0 perte d'attachement) ; **schéma v2 publié** (`meta.partition`/`meta.alternative`, version 2, v1 lue ; 26 cas, 0 échec) ; **contrat v1** validé ; frontières, partition, GN ; **`drave` v0**.
reports/rapport-schema-v2.md:59:`meta.partition`/`meta.alternative` ; elle passe le schéma v1. Le **contrôle négatif** la
reports/rapport-schema-v2.md:112:- [`tools/schemas/drave-annotation-v1.json`](../tools/schemas/drave-annotation-v1.json) — le schéma v1, inchangé.
  ```

- **bash** `{"command": "python3 tools/verifier_schema_produit.py --json | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['versions_lues']); print(d['retrocompatibilite']); print(len(d['cas']), sum(not c['ok'] for c in d['cas']))\"; echo \"exit=${PIPESTATUS[0]}\"; python3 tools/verifier_schema_pr … [74 caractères tronqués]`

  ```
[1, 2]
{'v1_lue': True, 'v2_refuse_v1': True}
6 0
exit=0
usage: verifier_schema_produit.py [-h] [--json] [--gold N] [--aide]

Valide drave.annotation contre le schéma de sa version.

options:
  -h, --help  show this help message and exit
  --json      détail JSON des cas
  --gold N    valide aussi les N premières phrases du gold (0 = aucune)
  ```

- **bash** `{"command": "python3 -m json.tool tools/schemas/drave-annotation-v2.json >/dev/null && python3 -m json.tool reports/pensee-schema-v2.json >/dev/null && echo JSON-OK; python3 tools/taille_documents.py 2>&1 | tail -12; echo \"exit=${PIPESTATUS[0]}\"", "description": "Validate JSON and doc budget"}`

  ```
JSON-OK
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4019 mots (budget 4 000)

  avertissements :
     · 38 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · reports/README.md : 2814 mots > budget 2800 (T1)
     · T0 : 4019 mots (AGENTS + en-cours + une tâche) > budget 4 000
exit=1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "> **Règle 11** : serveurs locaux arrêtés ; professeurs par l'**API DeepSeek** ; GPU à Drave.\n", "old_string": "> **Règle 11** : serveurs locaux arrêtés ; professeurs par l'**API DeepSeek** ; GP … [295 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-schema-v2.md`](rapport-schema-v2.md) | **B13** — schéma v2 : `meta.partition`, `meta.alternative`, v1 lue |", "old_string": "| [`rapport-schema-v2.md`](rapport-schema-v2.md) | **B13** — sché … [66 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-produit-v0.md`](rapport-produit-v0.md) | **B13** — `drave` v0 : anal., éval., rejeu ; 6 tests |", "old_string": "| [`rapport-produit-v0.md`](rapport-produit-v0.md) | **B13** — le premier pro … [76 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -10; echo \"exit=${PIPESTATUS[0]}\"", "description": "Recheck document budget"}`

  ```
1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3972 mots (budget 4 000)

  avertissements :
     · 38 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · reports/README.md : 2811 mots > budget 2800 (T1)
exit=1
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -10; echo \"exit=${PIPESTATUS[0]}\"; python3 tools/verifie_en_cours.py 2>&1 | tail -5; echo \"exit=${PIPESTATUS[0]}\"", "description": "Re-run doc review and state check"}`

  ```
revue de documentation · 708 fiche(s) · 801 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
  en-cours · 1602 mots · 7 sections · 4 session(s) · 5 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
exit=0
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-schema-v1.md`](rapport-schema-v1.md) | **B13** — contrat v1 : refus JSON code 3, 9 contrôles |", "old_string": "| [`rapport-schema-v1.md`](rapport-schema-v1.md) | **B13** — le contrat v1 : ` … [68 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -8; echo \"exit=${PIPESTATUS[0]}\"", "description": "Recheck budget after trim"}`

  ```
1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3972 mots (budget 4 000)

  avertissements :
     · 38 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · reports/README.md : 2807 mots > budget 2800 (T1)
exit=1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-file-taches.md`](rapport-file-taches.md) | **B13** — file des 29 tâches : 18 périmées |", "old_string": "| [`rapport-file-taches.md`](rapport-file-taches.md) | **B13** — la file des 29 tâche … [66 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -7; echo \"exit=${PIPESTATUS[0]}\"", "description": "Recheck budget"}`

  ```
1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3972 mots (budget 4 000)

  avertissements :
     · 38 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
exit=0
  ```

- **bash** `{"command": "git diff -- tools/bloc_linguistique.py tools/verifier_schema_produit.py tools/tests/test_schema_produit.py tools/porte-produit.sh | sed -n '1,260p'", "description": "Review core code diff"}`

  ```
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 3fabf083..d32101b8 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -89,7 +89,9 @@ class Etiquette:
 
 
 SCHEMA_ANNOTATION = "drave.annotation"
-VERSION_ANNOTATION = 1
+# v2 : ajoute `meta.partition` et `meta.alternative` (partition des syntagmes qui se
+# chevauchent). Le format reste additif ; le vérificateur lit encore les annotations v1.
+VERSION_ANNOTATION = 2
 
 
 @dataclass
diff --git a/tools/porte-produit.sh b/tools/porte-produit.sh
index 29b7aa40..cb58b89e 100755
--- a/tools/porte-produit.sh
+++ b/tools/porte-produit.sh
@@ -42,9 +42,9 @@ else
 fi
 
 if python3 tools/verifier_schema_produit.py --gold 20 >/tmp/porte-produit-valide.log 2>&1; then
-  dit ✅ "schéma v1 validé (5 cas + 20 phrases du gold)"
+  dit ✅ "schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)"
 else
-  dit ❌ "schéma v1 : validation en échec (voir /tmp/porte-produit-valide.log)"; ko=1
+  dit ❌ "schéma v2 : validation en échec (voir /tmp/porte-produit-valide.log)"; ko=1
 fi
 
 if python3 tools/tests/test_produit_libre.py >/tmp/porte-produit-libre.log 2>&1; then
@@ -54,9 +54,9 @@ else
 fi
 
 if pytho
… [10824 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- docs/produit/README.md docs/produit/exemples.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/semaine-autonome.md reports/README.md | sed -n '1,300p'", "description": "Review docs diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 53475073..3584cb63 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-07, 13 h 30 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-07, 14 h 20 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -22,9 +22,6 @@
 > le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.
 >
 > **Règle 11** : serveurs locaux arrêtés ; professeurs par l'**API DeepSeek** ; GPU à Drave.
->
-> **Bilan de 15 h** : reprises à 09 h ; **runs N2 arrêtés** (`kd2`, `rope2048` à 6 400/20 000) ; **perte α=0,9 0,8385 (−0,176), PPL 3,1119 (−0,06)** ;
-> **N3 clos** ; la **passe complète attend la fin des runs** (§ 11). [journal du 04/11](../../journal/2026-11-04/README.md).
 
 ### Session `536cd5d6-94ac-4057-8fe9-11709a4587c7` — le hub, l'intégration et la reprise *(en pause)*
 
@@ -63,10 +60,10 @@
 - **Stratégie** : v0 mesuré.
 - **Ambition** : un runtime cognitif tracé.
 - **Objectif final** : un moteur de pensée 
… [22840 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "> `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1\n> reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du\n> §  … [647 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifier_schema_produit.py --gold 20 >/tmp/v.log 2>&1; echo \"verifier=$?\"; tail -3 /tmp/v.log; python3 tools/tests/test_schema_produit.py >/tmp/ts.log 2>&1; echo \"schema_tests=$?\"; tail -3 /tmp/ts.log", "description": "Re-run schema verifier and tests"}`

  ```
verifier=0
  ✅ rétro-compatibilité : annotation v1 lue par le schéma v1
  ✅ contrôle négatif : le schéma v2 refuse une annotation v1
  ✅ validateur JSON Schema · 26 cas
schema_tests=0
Ran 8 tests in 1.220s

OK
  ```

- **bash** `{"command": "python3 tools/tests/test_produit.py >/tmp/tp.log 2>&1; echo \"produit=$?\"; tail -3 /tmp/tp.log; python3 tools/tests/test_produit_libre.py >/tmp/tl.log 2>&1; echo \"libre=$?\"; tail -3 /tmp/tl.log", "description": "Re-run product tests"}`

  ```
produit=0
Ran 16 tests in 3.700s

OK
libre=0
Ran 4 tests in 0.324s

OK
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py >/tmp/revue.log 2>&1; echo \"revue=$?\"; tail -2 /tmp/revue.log; python3 tools/taille_documents.py >/tmp/taille.log 2>&1; echo \"taille=$?\"; tail -3 /tmp/taille.log; python3 tools/verifie_en_cours.py >/tmp/etat.log 2>&1; echo \"etat=$?\"; tail -2 /t … [121 caractères tronqués]`

  ```
revue=0
  revue de documentation · 708 fiche(s) · 801 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
taille=0
     · 38 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
etat=0
  en-cours · 1602 mots · 7 sections · 4 session(s) · 5 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
index=0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,json,copy\nsys.path.insert(0,'.')\nimport fastjsonschema, tools.bloc_linguistique as bl\nv=fastjsonschema.compile(json.load(open('tools/schemas/drave-annotation-v2.json')))\nd=bl.Heuristique().analyser(\"Le chat de la voisine qui dort sur le toit se réveille … [862 caractères tronqués]`

  ```
rejette: vue inconnue
rejette: relation inconnue
rejette: type inconnu
rejette: alternative sans rang
NON REJETÉ: version 1
  ```

- **bash** `{"command": "git diff --check; echo \"diffcheck=$?\"", "description": "Check whitespace in diff"}`

  ```
diffcheck=0
  ```

- **bash** `{"command": "ls -la .git/hooks/pre-commit 2>/dev/null; sed -n '1,80p' .git/hooks/pre-commit 2>/dev/null; echo '---'; ls tools/hooks 2>/dev/null", "description": "Inspect pre-commit hook"}`

  ```
-rwxr-xr-x. 1 stephane stephane 1470 31 oct 12:55 .git/hooks/pre-commit
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
# Le journal d
… [321 caractères tronqués]
  ```

- **bash** `{"command": "git add tools/schemas/drave-annotation-v2.json tools/verifier_schema_produit.py tools/bloc_linguistique.py tools/tests/test_schema_produit.py tools/porte-produit.sh docs/produit/README.md docs/produit/exemples.md reports/rapport-schema-v2.md reports/pensee-schema-v2.json reports/INDEX.m … [188 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  docs/pilotage/semaine-autonome.md
M  docs/produit/README.md
M  docs/produit/exemples.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-e1ad947b-50b1-4758-a921-5267225bf642/digest.md
 M journal/sessions/session-e1ad947b-50b1-4758-a921-5267225bf642/rapport.md
M  reports/INDEX.md
M  reports/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
A  reports/pensee-schema-v2.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
A  reports/rapport-schema-v2.md
 M reports/rapport-spans-chunker.md
M  tools/bloc_linguistique.py
 M tools/chantier/superviseur.py
M  tools/porte-produit.sh
A  tools/schemas/drave-annotation-v2.json
 m tools/structures
M  tools/tests/test_schema_produit.py
M  tools/verifier_schema_produit.py
?? journal/sessions/session-614644be-9315-4734-9b97-236a792f4dc5/
?? reports/rapport-s-par
… [11 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_etat_a_jour.py --index; echo \"exit=$?\"", "description": "Verify state accompanies facts"}`

  ```
✅ index : aucun fait stagé sans état
exit=0
  ```

- **bash** `{"command": "python3 tools/tests/linguistique/test_bloc_linguistique.py 2>&1 | tail -12; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run block linguistics tests"}`

  ```
...................
----------------------------------------------------------------------
Ran 19 tests in 0.070s

OK
exit=0
  ```

- **bash** `{"command": "if [ -f tools/porte-bloc-linguistique.sh ]; then bash tools/porte-bloc-linguistique.sh 2>&1 | tail -15; echo \"exit=${PIPESTATUS[0]}\"; else echo absent; fi", "description": "Run block linguistics gate"}`

  ```
"verdicts": {
  "langue": true,
  "script": true,
  "permute_faible": true,
  "niveaux": true,
  "substitution": true,
  "parallele": true,
  "activation": true,
  "vide": true,
  "inconnue": true,
  "rejeu": true
 },
 "ok": true
}
✅ porte bloc linguistique verte
exit=0
  ```

- **bash** `{"command": "git commit -m \"B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC), v1 TOUJOURS LUE\" 2>&1 | tail -40; echo \"exit=${PIPESTATUS[0]}\"", "description": "Commit schema v2 task", "timeoutMs": 300000}`
