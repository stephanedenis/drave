# Session DSH — relecture

- identifiant : `b3d82ad5-bff2-49ec-9ad6-2230e68d8071`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 14:47:27
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : mesurer l'effet des **cibles multiples** du gold sur la mesure d'attachement, sans modifier le code.

Contexte : `tools/tests/linguistique/evaluer_gold.py::evaluer_bloc` compare la cible choisie à `cibles[0]` pour l'exact, mais le gold autorise parfois **plusieurs cibles** (`cibles` = liste, voir `tools/tests/linguistique/gold_reel.py`). Une auditrice (fiche `reports/rapport-annotation-independante.md`, A7) dit que 43/96 GP ont deux cibles et que la mesure n'en compare qu'une.

À faire :
1. Compte, sur les 239 cibles et sur les 145 segments au bon span : combien ont plus d'une cible (`len(cibles) > 1`), par type, et combien de cibles alternatives existent en moyenne.
2. Mesure l'exact sous trois définitions : (a) `cible == cibles[0]` (l'actuelle), (b) `cible in cibles` (n'importe laquelle), (c) `cible` égale à l'une des cibles **réduites à leur tête** (verbe plein ou dernier mot). Donne les trois taux et l'écart, par type.
3. Contrôle négatif : permutation des cibles (1000 tirages) sous la définition (b).
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-multicibles.md` (fiche : verdict, tableaux, contrôle négatif, limites, recommandation sur la définition à retenir) et `reports/pensee-multicibles.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé : les trois taux et la recommandation.
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

⏵ Exploration du dépôt et des fichiers gold/évaluation

- **bash** `{"command": "pwd && git status --short && git branch --show-current && ls", "description": "Show repo status and branch"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
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
D  journal/sessions/3f8f2bb8-781b-44a6-9e14-58025004b6fc/digest.md
D  journal/sessions/3f8f2bb8-781b-44a6-9e14-58025004b6fc/rapport.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/digest.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/rapport.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/digest.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/rapport.md
D  jou
… [2536 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/tests/linguistique/ 2>/dev/null; echo '---'; ls -la reports/ | head -40", "description": "List linguistique tools and reports"}`

  ```
total 1408
drwxr-xr-x. 1 stephane stephane    708  5 nov 13:57 .
drwxr-xr-x. 1 stephane stephane    640  4 nov 08:44 ..
-rw-r--r--. 1 stephane stephane  16090  2 nov 09:26 anaphore.py
-rw-r--r--. 1 stephane stephane  35148  5 nov 14:25 classement_cible.py
-rw-r--r--. 1 stephane stephane  14489  5 nov 13:51 evaluer_gold.py
-rw-r--r--. 1 stephane stephane 450905  2 nov 13:27 gold_gele.json
-rw-r--r--. 1 stephane stephane  20009  5 nov 14:14 gold.json
-rw-r--r--. 1 stephane stephane   7813  2 nov 12:03 gold.py
-rw-r--r--. 1 stephane stephane 470149  2 nov 14:39 gold_reel.json
-rw-r--r--. 1 stephane stephane 132934  5 nov 14:04 gold_reel.py
-rw-r--r--. 1 stephane stephane 149191  2 nov 12:04 gold_synthetique.json
-rw-r--r--. 1 stephane stephane  10124  2 nov 12:03 gold_synthetique.py
-rw-r--r--. 1 stephane stephane   2953  2 nov 12:17 juge.py
-rw-r--r--. 1 stephane stephane  22366  3 nov 14:05 miroir.py
drwxr-xr-x. 1 stephane stephane    668  5 nov 14:10 __pycache__
-rw-------. 1 stephane stephane   9951  3 nov 00:39 qualifier_cascade.py
-rw-r--r--. 1 stephane stephane   6589  3 nov 16:39 qualifier_frontiere_71.py
-rw-r--r--. 1 stephane stephane   6114  3 nov 14:09 qualifier_lien_appri
… [3263 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de `evaluer_gold.py` et de la structure du gold

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py"}`

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
… [14748 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/tests/linguistique/gold_reel.py", "description": "Read head of gold_reel.py"}`

  ```
"""gold_reel.py — 200 phrases réelles (20 françaises, 20 anglaises).

Elles ne sont pas des phrases du bloc ni du générateur : elles sont écrites après, avec leurs
POS, leurs segments GN/GV/GP/REL/SUB et leur pragmatique. Le fichier `gold_reel.json` est généré
par `construire()` ; le gold réel total devient **200 phrases** (20 de `gold.py` + 180).
"""
from __future__ import annotations

import json
import pathlib

# La **convention des cibles** d'attachement. Le gold ne la documentait pas ; elle a été lue
# sur les données le 2026-11-05 (T169/T172) et la voici, explicitement :
#
#   - **REL** : la cible est l'**antécédent** — la tête nominale du GN à gauche
#     (« l'homme que j'ai vu » → `homme`) ;
#   - **SUB** : la cible est le **verbe gouverneur** (le POS gold donne 69/69 cibles VERB :
#     « cette étoile écoute que Lucas trouve » → `écoute`), pas un antécédent ;
#   - **GP** : la cible est le **verbe qui gouverne** le complément (« au ballon » → `joue`),
#     ou, pour un génitif, le **nom qu'il complète** (« de la voisine » → `chat`) ;
#   - **GN / GV** : la cible, quand elle existe, est le **nom ou le verbe** dont le segment
#     dépend (36 cibles verbes, 82 cibles noms m
… [7772 caractères tronqués]
  ```

- **bash** `{"command": "grep -rl '\"cibles\": 239' reports/ 2>/dev/null | head; grep -rl '239' reports/*.json 2>/dev/null | head -20", "description": "Find reports with 239 targets"}`

  ```
reports/pensee-attachement.json
reports/pensee-cible-proximite.json
reports/pensee-candidats-verbes.json
reports/pensee-verbe-gv.json
reports/pensee-lexique-verbal.json
reports/pensee-spans.json
reports/pensee-denominateur.json
reports/pensee-classement.json
reports/pensee-attachement-cible.json
reports/pensee-lexique-elargi.json
reports/b102bis-corpus-jw.json
reports/b10-decodeur-mots.json
reports/cerveau-mesures-corrigees.json
reports/composition-multilingue.json
reports/composition-verne-large.json
reports/corpus-wiki-de.json
reports/corpus-wiki-en-texte-contamination.json
reports/corpus-wiki-es-texte.json
reports/corpus-wiki-fr-texte-contamination.json
reports/couche-distante.json
reports/couche-int8-canal.json
reports/couche-int8.json
reports/kfold-14b-0095.json
reports/kfold-14b-0210.json
reports/kfold-14b1000-0004.json
reports/kfold-14b1000-0066.json
reports/kfold-14b1000-0095.json
reports/kfold-14b1000-0210.json
reports/kfold-14b600-0095.json
reports/kfold-7b-amp-0095.json
  ```

- **bash** `{"command": "sed -n '120,400p' tools/tests/linguistique/gold_reel.py", "description": "Read more of gold_reel.py"}`

  ```
[("GN", "The cat", "agent"), ("GV", "sleeps", "prédicat"), ("GP", "on the chair", "lieu", "sleeps")], {"acte": "assertion"}),
    ("r028", "en", "It rains since yesterday.",
     [("It", "PRON"), ("rains", "VERB"), ("since", "PREP"), ("yesterday", "ADV")],
     [("GN", "It", "agent"), ("GV", "rains", "prédicat"), ("GP", "since yesterday", "temps", "rains")], {"acte": "assertion"}),
    ("r029", "en", "I do not understand.",
     [("I", "PRON"), ("do", "AUX"), ("not", "ADV"), ("understand", "VERB")],
     [("GN", "I", "agent"), ("GV", "do not understand", "prédicat")], {"acte": "assertion", "negation": True}),
    ("r030", "en", "You come tomorrow?",
     [("You", "PRON"), ("come", "VERB"), ("tomorrow", "ADV")],
     [("GN", "You", "agent"), ("GV", "come", "prédicat")], {"acte": "question", "reponse": "yes"}),
    ("r031", "en", "The train leaves at noon.",
     [("The", "DET"), ("train", "NOUN"), ("leaves", "VERB"), ("at", "PREP"), ("noon", "NOUN")],
     [("GN", "The train", "agent"), ("GV", "leaves", "prédicat"), ("GP", "at noon", "temps", "leaves")], {"acte": "assertion"}),
    ("r032", "en", "The car is fast.",
     [("The", "DET"), ("car", "NOUN"), ("is", "AUX"), ("fast", "ADJ
… [23061 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor f in ['reports/pensee-attachement.json','reports/pensee-cible-proximite.json','reports/pensee-spans.json','reports/pensee-denominateur.json']:\n    try:\n        d=json.load(open(f))\n        print('===',f, type(d))\n        s=json.dumps(d, ensure_asci … [139 caractères tronqués]`

  ```
=== reports/pensee-attachement.json <class 'dict'>
{"date": "2026-11-04", "ligne": "B13", "portes": "156/156", "attachement": {"cibles": 239, "labels": 145, "top1": 0.3431, "topk": 0.3264, "exact": 0.0042, "couverture": 0.6067}, "tete": {"top1": 0.5586, "topk": 0.531}, "limites": ["94 cibles sans label", "1 exact", "gold 432"]}
=== reports/pensee-cible-proximite.json <class 'dict'>
{"date": "2026-11-04", "ligne": "B13", "portes": "164/164", "gold": 612, "cibles": 239, "avant": {"top1": 82, "top1_taux": 0.3431, "exact": 1, "exact_taux": 0.0042, "tete": 81, "tete_taux": 0.5586}, "apres": {"top1": 95, "top1_taux": 0.3975, "exact": 13, "exact_taux": 0.0544, "tete": 94, "tete_taux": 0.6483}, "inchanges": {"topk": 78, "couverture": 0.6067}, "limites": ["226 échecs non qualifiés", "les passifs", "gold 612"]}
=== reports/pensee-spans.json <class 'dict'>
{"date": "2026-11-05", "ligne": "B13", "portes": "169/169", "gold": 612, "cibles": 239, "spans": {"REL": 48, "SUB": 33, "GP": 12, "total": 93}, "categories": {"aucun": 65, "plus_large": 25, "plus_etroit": 3, "coupe": 1}, "avant": {"labels": 145, "couverture": 0.6067, "f1": 0.2864, "span": 94, "cible": 13}, "apres": {"labels": 146, "couvertu
… [921 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='tools/tests/linguistique/gold_reel.json'\nd=json.load(open(p))\nprint(type(d), d.keys() if isinstance(d,dict) else len(d))\nph=d['phrases']\nprint('n phrases',len(ph))\nimport collections\nprint('keys phrase',ph[0].keys())\nprint(json.dumps(ph[0],ensure … [391 caractères tronqués]`

  ```
<class 'dict'> dict_keys(['version', 'source', 'note', 'phrases'])
n phrases 432
keys phrase dict_keys(['id', 'langue', 'texte', 'mots', 'segments', 'pragma', 'source'])
{"id": "r001", "langue": "fr", "texte": "Le chien mange une pomme.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chien", "pos": "NOUN", "debut": 3, "fin": 8}, {"texte": "mange", "pos": "VERB", "debut": 9, "fin": 14}, {"texte": "une", "pos": "DET", "debut": 15, "fin": 18}, {"texte": "pomme", "pos": "NOUN", "debut": 19, "fin": 24}], "segments": [{"type": "GN", "texte": "Le chien", "role": "agent", "debut": 0, "fin": 8}, {"type": "GV", "texte": "mange", "role": "prédicat", "debut": 9, "fin": 14}, {"type": "GN", "texte": "une pomme", "role": "patient", "debut": 15, "fin": 24}], "pragma": {"acte": "assertion"}, "source": "reel"}
n segments 1445 avec cible 171 cibles listes 171
seg keys Counter({('debut', 'fin', 'role', 'texte', 'type'): 1274, ('cible', 'cibles', 'debut', 'fin', 'role', 'texte', 'type'): 171})
{"type": "GN", "texte": "Le chien", "role": "agent", "debut": 0, "fin": 8}
  ```

### 🤖 Assistant

⏵ Lecture de la fiche d'audit A7 et comptage des cibles par source

- **bash** `{"command": "grep -n \"A7\" -A 40 -B 5 reports/rapport-annotation-independante.md | head -120", "description": "Read A7 section of audit report"}`

  ```
(no output)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json']:\n    d=json.load(open('tools/tests/linguistique/'+f))\n    ph=d['phrases']\n    seg=[s for x in ph for s in x.get('segments',[])]\n    target=[s for s in seg if s.get('cibles') or s.get('cibl … [401 caractères tronqués]`

  ```
gold.json phrases 20 segments 56 cibles 13 multi 5
  types cibles Counter({'GP': 10, 'SUB': 2, 'REL': 1}) multi types Counter({'GP': 5})
gold_reel.json phrases 432 segments 1445 cibles 171 multi 14
  types cibles Counter({'GP': 62, 'REL': 57, 'SUB': 52}) multi types Counter({'GP': 14})
gold_synthetique.json phrases 160 segments 362 cibles 55 multi 24
  types cibles Counter({'GP': 24, 'REL': 16, 'SUB': 15}) multi types Counter({'GP': 24})
  ```

### 🤖 Assistant

⏵ Inventaire des cibles multi-mots et de leurs têtes

- **bash** `{"command": "python3 - <<'PY'\nimport json, collections\nfiles=['gold.json','gold_reel.json','gold_synthetique.json']\nallseg=[]\nfor f in files:\n    d=json.load(open('tools/tests/linguistique/'+f))\n    for ph in d['phrases']:\n        for s in ph.get('segments',[]):\n            if s.get('cibles' … [358 caractères tronqués]`

  ```
total 239
multi 43
gold.json g003 | GP | dans le parc | ['vu', "l'homme"] | La femme a vu l'homme dans le parc.
gold.json g007 | GP | dans le jardin | ['jouent', 'enfants'] | Les enfants jouent dans le jardin.
gold.json g012 | GP | à manger | ['prêt', 'canard'] | Le canard est prêt à manger.
gold.json g016 | GP | in the park | ['saw', 'man'] | The woman saw the man in the park.
gold.json g020 | GP | to eat | ['ready', 'duck'] | The duck is ready to eat.
gold_reel.json r018 | GP | à manger | ['prête', 'souris'] | La souris est prête à manger.
gold_reel.json r020 | GP | dans le parc | ['jouent', 'enfants'] | Les enfants jouent dans le parc.
gold_reel.json r038 | GP | to eat | ['ready', 'mouse'] | The mouse is ready to eat.
gold_reel.json r040 | GP | in the park | ['play', 'children'] | The children play in the park.
gold_reel.json r047 | GP | dans le jardin | ['poussent', 'fleurs'] | Les fleurs poussent dans le jardin.
gold_reel.json r067 | GP | in the garden | ['grow', 'flowers'] | The flowers grow in the garden.
gold_reel.json r088 | GP | sur le toit | ['grimpe', 'chat'] | Le chat grimpe sur le toit.
gold_reel.json r108 | GP | on the roof | ['climbs', 'cat'] | The cat climbs on the
… [3175 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, collections, re\nfiles=['gold.json','gold_reel.json','gold_synthetique.json']\nvals=collections.Counter()\nfor f in files:\n    d=json.load(open('tools/tests/linguistique/'+f))\n    for ph in d['phrases']:\n        for s in ph.get('segments',[]):\n         … [351 caractères tronqués]`

  ```
distinct 187
multiword distinct 0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, collections\nfor f in ['gold_gele.json','gold.json','gold_reel.json','gold_synthetique.json']:\n    d=json.load(open('tools/tests/linguistique/'+f))\n    ph=d['phrases']\n    seg=[s for x in ph for s in x.get('segments',[])]\n    target=[s for s in seg if  … [369 caractères tronqués]`

  ```
gold_gele.json phrases 602 cibles 239 multi 43 types Counter({'GP': 96, 'REL': 74, 'SUB': 69}) multi types Counter({'GP': 43})
gold.json phrases 20 cibles 13 multi 5 types Counter({'GP': 10, 'SUB': 2, 'REL': 1}) multi types Counter({'GP': 5})
gold_reel.json phrases 432 cibles 171 multi 14 types Counter({'GP': 62, 'REL': 57, 'SUB': 52}) multi types Counter({'GP': 14})
gold_synthetique.json phrases 160 cibles 55 multi 24 types Counter({'GP': 24, 'REL': 16, 'SUB': 15}) multi types Counter({'GP': 24})
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'tools')\nsys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\nphrases=eg.charger()\nh=bl.Heuristique()\n# gather predictions for all target segments\nfrom collections import Count … [954 caractères tronqués]`

  ```
Counter({'cibles': 239, 'labels': 145})
distinct preds 102
g002 GP ['chat'] -> ''
g003 GP ['vu', "l'homme"] -> 'vu'
g004 GP ['couru'] -> 'couru'
g005 SUB ['dit'] -> 'dit'
g007 GP ['jouent', 'enfants'] -> 'jouent'
g010 GP ['Viens'] -> 'Viens'
g011 REL ['livre'] -> 'livre'
g012 GP ['prêt', 'canard'] -> 'manger'
g014 GP ['vu'] -> 'vu'
g016 GP ['saw', 'man'] -> 'saw'
r005 GP ['parle'] -> 'parle'
r007 GP ['dort'] -> 'dort'
r008 GP ['pleut'] -> 'pleut'
r011 GP ['part'] -> 'part'
r014 REL ['livre'] -> 'livre'
r015 REL ['film'] -> 'film'
r018 GP ['prête', 'souris'] -> 'manger'
r020 GP ['jouent', 'enfants'] -> 'jouent'
r025 GP ['talks'] -> 'talks'
r026 GP ['listen'] -> 'listen'
r027 GP ['sleeps'] -> 'sleeps'
r031 GP ['leaves'] -> 'leaves'
r040 GP ['play', 'children'] -> 'play'
r041 GP ['joue'] -> 'joue'
r044 GP ['parle'] -> 'parle'
r047 GP ['poussent', 'fleurs'] -> 'poussent'
r048 GP ['écrit'] -> 'écrit'
r050 GP ['partons'] -> 'partons'
r052 GP ['ouvre'] -> 'ouvre'
r054 REL ['livre'] -> 'livre'
r055 REL ['ville'] -> 'ville'
r057 GP ['aboie'] -> 'aboie'
r061 GP ['plays'] -> 'plays'
r063 GP ['listen'] -> 'listen'
r064 GP ['talks'] -> 'talks'
r067 GP ['grow', 'flowers'] -> 'grow'
r068 GP ['wri
… [125 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection de la production de `attachement.cible` dans le bloc

- **bash** `{"command": "grep -rn \"attachement\" tools/bloc_linguistique.py | head -40", "description": "Find attachement production in block"}`

  ```
703:        """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
729:            att = c.get("attachement") or {}
874:            # candidat d'attachement (diagnostic des 33 échecs de T162).
912:                        meta["attachement"] = {"segment": s.get("texte", ""), "cible": cible}
937:                    meta["attachement"] = {"segment": s["texte"], "cible": cible}
956:                    meta["attachement"] = {"segment": s["texte"], "cible": cible}
  ```

- **bash** `{"command": "grep -rn \"def .*tete\\|_tete\\|verbe plein\\|dernier mot\\|head\" tools/bloc_linguistique.py | head -40; ls tools | grep -i bloc", "description": "Find head-reduction helpers"}`

  ```
620:    def _tete_texte(texte: str) -> str | None:
621:        """La tête d'un texte de candidat : le verbe plein s'il y en a un, sinon le dernier mot.
635:    def _tete_nom(texte: str, debut: int, fin: int) -> str | None:
636:        """La tête nominale d'un span : le dernier mot, **élision séparée** (`L'homme` → `homme`)."""
645:        """Le **verbe** du span : le lexique d'abord, puis le POS `VERB`, sinon le dernier mot."""
899:                                cible = self._tete_nom(texte, g["debut"], g["fin"])
919:                            tete = self._tete_texte(nom.split("→", 1)[1])
1207:            headers={"Content-Type": "application/json"})
1341:            headers={"Content-Type": "application/json"})
1511:            headers={"Content-Type": "application/json"})
approximabilite_bloc.py
bloc_code.py
bloc_linguistique.py
bloc_maths.py
bloc_tableaux.py
essai_blocs.py
iterer_bloc.py
porte-bloc-code.sh
porte-bloc-linguistique.sh
porte-bloc-maths.sh
porte-bloc-tableaux.sh
porte-miroir-blocs.sh
ref_ggml_bloc.c
v41_attention_blocs.py
vision_bloc_ref.py
  ```

- **bash** `{"command": "sed -n '600,680p' tools/bloc_linguistique.py; echo '---'; sed -n '860,970p' tools/bloc_linguistique.py", "description": "Read head-reduction helpers and attachment code"}`

  ```
return None

    def _cibles_s(self, texte: str) -> dict:
        """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).

        Lecture seule de l'API interne du S : `_tokens`/`_segmente` rendent les `Segment` avec
        `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
        (GP, puis GN, puis GV), comme le premier candidat de `analyser`.
        """
        if not self.segmenter_s:
            return {}
        try:
            import generateur
            base = generateur._segmente(texte, generateur._tokens(texte))
            return {(s.debut, s.fin, s.type): (s.cible_gp or s.cible_nom or s.cible_verbe)
                    for s in base}
        except Exception:
            return {}

    @staticmethod
    def _tete_texte(texte: str) -> str | None:
        """La tête d'un texte de candidat : le verbe plein s'il y en a un, sinon le dernier mot.

        `« … → Le livre »` → `livre` ; `« … → Les fleurs poussent »` → `poussent` ;
        `« … → est prêt »` → `prêt` (l'auxiliaire n'est pas la tête).
        """
        mots = re.findall(r"\b[ldmtsnLDMTNS]['’](?=\w)|[\wÀ-ÿ]+(?:['’\-][\wÀ-ÿ]+)*", texte)
        if not
… [9756 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/rapport-annotation-independante.md && wc -l reports/rapport-annotation-independante.md && sed -n '1,120p' reports/rapport-annotation-independante.md", "description": "Read annotation audit report"}`

  ```
-rw-------. 1 stephane stephane 19335  5 nov 14:10 reports/rapport-annotation-independante.md
283 reports/rapport-annotation-independante.md
# Contrôle indépendant de la convention d'attachement — 20 segments annotés à la main

**Date** 2026-11-05 · **Branche** `s/v7` · **HEAD** `e1171032` · **Graine** `20261105` · **Statut** contrôle
externe ; aucun fichier existant modifié **par moi** ; aucun commit.

**Deux versions du bloc, pinées.** La mesure aveugle porte sur `HEAD e1171032`,
`tools/bloc_linguistique.py` sha256 `d9c9d559…`. Pendant la rédaction, le fichier de travail a changé
(correctif `SUB`) : j'ai copié le snapshot à 13:51:26, sha256 `6e843018…`, et je le mesure à part. Les
tableaux des § 2, 3.1 et 3.2 sont la mesure aveugle ; la § 3.3 est une re-exécution **post-hoc**, pas un
résultat aveugle. La doc `gold_reel.py` a aussi changé pendant la session : `CONVENTION_CIBLE["SUB"]`
est passée de « antécédent » à « verbe gouverneur (69/69 cibles VERB) » ; la mesure aveugle reste celle de
HEAD, la correction est citée et validée à part.

## Verdict

| mesure | accord | IC95 Wilson |
|---|---:|---:|
| **moi ↔ gold**, cible top-1 | **20/20 = 100 %** | 83,9–100 % |
| moi ↔ gold, san
… [7854 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '120,283p' reports/rapport-annotation-independante.md", "description": "Read rest of audit report"}`

  ```
| SUB | 9 | 6 | 4 | 0 | 3 | 2 |
| REL | 4 | 0 | 0 | 3 | 0 | 1 |
| **total** | **20** | **12** | **10** | **3** | **4** | **3** |

Le span exact (12/20 = 60 %) et la justesse au span exact (10/12 = 83,3 %) sont dans la même zone que le
gold entier : **145/239 = 60,7 %** de spans exacts et **123/145 = 84,8 %** de cibles justes au span exact.
L'échantillon n'est pas atypique — mais il est petit.

### 3.3 Après le correctif SUB (post-hoc, snapshot `6e843018`)

Le fichier de travail a changé pendant la session : la cible d'un SUB est désormais le verbe quand le
segment précédent est un GV, l'antécédent quand c'est un GN. J'ai copié le fichier à 13:51:26 et mesuré
cette copie (hash identique au live au moment de la mesure ; il peut encore bouger).

| version | hash | strict | tête | attachement seul | cible fausse | global juste / labels | GP | SUB | REL |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HEAD `e1171032` (aveugle) | `d9c9d559` | 10/20 | 13/20 | 17/20 | 3 | 123/145 = 84,8 % | 69/83 | 28/36 | 26/26 |
| snapshot 13:51:26 | `6e843018` | **11/20** | 14/20 | **18/20** | **2** | **137/145 = 94,5 %** | 77/83 | 34/36 | 26/26 |

- Seul changement de cible sur les 20 : `s052` `cu
… [8732 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, collections\nfiles=['gold.json','gold_reel.json','gold_synthetique.json']\nvals=collections.Counter()\nfor f in files:\n    d=json.load(open('tools/tests/linguistique/'+f))\n    for ph in d['phrases']:\n        for s in ph.get('segments',[]):\n             … [505 caractères tronqués]`

  ```
"l'homme" 1
total distinct 175
AUX targets []
  ```

- **bash** `{"command": "grep -rn \"rapport-multicibles\\|multicibles\\|multi-cibles\\|cibles multiples\" reports/ docs/ journal/ 2>/dev/null | head -30", "description": "Search existing multi-target work"}`

  ```
reports/rapport-annotation-independante.md:179:### 4.2 `GP` : quatre adjectifs gouverneurs, et 43 multi-cibles
reports/rapport-annotation-independante.md:189:4 GP sont multi-cibles (cas 1, 6, 12, 17) ; j'ai toujours choisi la première (le verbe) et le bloc aussi,
docs/pilotage/plan-travail.md:430:| **4** | A12 spans sans S, A13 multi-cibles, A14 gold anglais | couverture, définition de la mesure, qualité du gold | en cours |
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:42380:⏵ Vague 4 (3 sous-agents) : couverture des spans, multi-cibles, qualité du gold anglais
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:42383:- **subagent** `{"description": "Mesure multi-cibles du gold", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : mesurer l'effet des **cibles multiples** du gold sur la mesure d'attachement, sans modifier le code.\n\nContexte : `tools/tests/ling … [1389 caractères tronqués]`
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md:9461:⏵ Vague 4 (3 sous-agents) : couverture des spans, multi-cibles, qualité du gold anglais
journal/sessions/e181ce02-cd50-488a-a6
… [1511 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/rapport-multicibles.md reports/pensee-multicibles.json 2>&1; sed -n '790,860p' journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/digest.md", "description": "Check target files and prior multi-target analysis"}`

  ```
ls: cannot access 'reports/rapport-multicibles.md': No such file or directory
ls: cannot access 'reports/pensee-multicibles.json': No such file or directory
ls: cannot access 'reports/rapport-annotation-independante.md': No such file or directory
ls: cannot access 'reports/pensee-annotation-independante.json': No such file or directory
---
 M reports/pensee-quatre-modes.json
?? reports/rapport-s-paragraphes.md
[stderr]
grep: write error: Broken pipe
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nfor f in [\"reports/pensee-attachement-cible.json\", \"reports/pensee-attachement.json\", \"reports/pensee-echecs-attachement.json\"]:\n    try:\n        d = json.load(open(f))\n        print(\"==\", f … [364 caractères tronqués]`

  ```
== reports/pensee-attachement-cible.json dict
clés: ['date', 'ligne', 'portes', 'gold', 'cibles', 'labels', 'avant', 'apres', 'rendement', 'regle', 'limites']
  date : 2026-11-05
  ligne : B13
  portes : 173/173
  gold : 612
== reports/pensee-attachement.json dict
clés: ['date', 'ligne', 'portes', 'attachement', 'tete', 'limites']
  date : 2026-11-04
  ligne : B13
  portes : 156/156
  at
… [3505 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/ | grep -i \"annot\\|multi\" ; echo '---'; wc -l journal/sessions/b3d82ad5-bff2-49ec-9ad6-2230e68d8071/digest.md; tail -80 journal/sessions/b3d82ad5-bff2-49ec-9ad6-2230e68d8071/digest.md", "description": "Check sibling session digest tail"}`

  ```
-rw-------. 1 stephane stephane    9416  2 oct 15:32 bilan-multi-materiel.md
-rw-r--r--. 1 stephane stephane   22034 21 oct 01:10 composition-multilingue.json
-rw-r--r--. 1 stephane stephane    1352  1 nov 13:34 corpus-multi-propre.json
-rw-r--r--. 1 stephane stephane     488 27 oct 23:26 kv-cache-multi.json
-rw-r--r--. 1 stephane stephane  486460 27 oct 12:24 multilingue.json
-rw-r--r--. 1 stephane stephane     739 28 oct 13:24 native-corpus-multi.json
-rw-r--r--. 1 stephane stephane     628 28 oct 14:15 native-distillation-multi.json
-rw-r--r--. 1 stephane stephane   30539  5 nov 14:09 pensee-annotation-independante.json
-rw-r--r--. 1 stephane stephane   13957 21 oct 00:21 pensee-multilingue.json
-rw-r--r--. 1 stephane stephane     360 22 oct 01:29 plan-multi-3b.json
-rw-r--r--. 1 stephane stephane     151 22 oct 22:06 plan-multi-tache-3b.json
-rw-r--r--. 1 stephane stephane     207 22 oct 11:10 pont-multi-3b.json
-rw-r--r--. 1 stephane stephane     913 22 oct 00:14 position-multilingue.json
-rw-r--r--. 1 stephane stephane     203 22 oct 16:43 raisonnement-multilingue-3b.json
-rw-------. 1 stephane stephane   19335  5 nov 14:10 rapport-annotation-independante.md
-rw-r--r--. 1 ste
… [4634 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de l'état du code puis calcul des trois définitions

- **bash** `{"command": "git log -1 --format='%H %ad %s' --date=iso; git status --short tools/tests/linguistique/evaluer_gold.py tools/bloc_linguistique.py tools/tests/linguistique/gold_reel.py; sha256sum tools/tests/linguistique/evaluer_gold.py tools/bloc_linguistique.py tools/tests/linguistique/gold_reel.json … [130 caractères tronqués]`

  ```
1ec7286c0aed1bdb64379b96b093c47d7ef554b5 2026-11-05 14:48:04 -0500 PILOTAGE — LES QUATRE VAGUES DE SOUS-AGENTS DOCUMENTÉES (§ 9) ; VAGUES 3 ET 4 EN COURS
c4d2dbc07b4e4c0b1c81889b61fd517d5d5953b4a3efae2094834a398ac5d599  tools/tests/linguistique/evaluer_gold.py
5640809e8e6bfbd661b86babdf0ed6ce351c8d1bce93a5546f4d22d69575ba2c  tools/bloc_linguistique.py
05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11  tools/tests/linguistique/gold_reel.json
3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a  tools/tests/linguistique/gold.json
e3e704ce9cb599db07ab31d1b0651f0aa12ea9ecad31ca8bf558efdeed84a654  tools/tests/linguistique/gold_synthetique.json
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor f in ['reports/pensee-attachement-cible.json','reports/pensee-echecs-attachement.json','reports/pensee-classement.json','reports/pensee-lexique-elargi.json']:\n    d=json.load(open(f))\n    print('===',f)\n    print(json.dumps(d,ensure_ascii=False,inde … [76 caractères tronqués]`

  ```
=== reports/pensee-attachement-cible.json
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "173/173",
 "gold": 612,
 "cibles": 239,
 "labels": 146,
 "avant": {
  "exact": 94,
  "exact_span": 0.6438,
  "top1": 114,
  "top1_span": 0.7808,
  "verbe": 0.7255,
  "nom": 0.6
 },
 "apres": {
  "exact": 118,
  "exact_span": 0.8082,
  "top1": 122,
  "top1_span": 0.8356,
  "verbe": 0.9412,
  "nom": 0.7368
 },
 "rendement": {
  "top1": 0.5105,
  "topk": 0.5523,
  "exact": 0.4937
 },
 "regle": "REL/SUB → antécédent (tête du GN à gauche, élision séparée) ; GP → verbe du GV",
 "limites": [
  "28 échecs non qualifiés",
  "convention non documentée",
  "top-k lenient",
  "gold 612"
 ]
}
=== reports/pensee-echecs-attachement.json
{
 "date": "2026-11-04",
 "ligne": "B13",
 "portes": "166/166",
 "echecs": {
  "span": 94,
  "cible_avant": 33,
  "cible_apres": 32,
  "total_avant": 127,
  "total_apres": 126
 },
 "avant": {
  "top1": 95,
  "topk": 112,
  "exact": 13,
  "tete_top1": 94,
  "tete_topk": 111
 },
 "apres": {
  "top1": 96,
  "topk": 113,
  "exact": 14,
  "tete_top1": 96,
  "tete_topk": 113
 },
 "cause_32": "le GV couvre la phrase : le dernier token n'est pas le verbe",
 "limites": [
  "les 
… [1559 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'tools')\nsys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\nph=eg.charger()\nfor nom,bloc in [('heuristique',bl.Heuristique()),('mock',bl.MockNeuronal()),('cascade',bl.Cascade(b … [197 caractères tronqués]`

  ```
heuristique {"cibles": 239, "labels": 145, "top1": 140, "topk": 142, "exact": 137, "top1_taux": 0.5858, "topk_taux": 0.5941, "exact_taux": 0.5732, "top1_taux_span": 0.9655, "topk_taux_span": 0.9793, "topk_exact": 141, "topk_exact_taux": 0.59, "topk_exact_taux_span": 0.9724, "exact_taux_span": 0.9448, "verbe": {"cibles": 116, "justes": 111, "taux": 0.9569}, "nom": {"cibles": 29, "justes": 26, "taux": 0.8966}, "couverture": 0.6067}
mock {"cibles": 239, "labels": 77, "top1": 0, "topk": 0, "exact": 0, "top1_taux": 0.0, "topk_taux": 0.0, "exact_taux": 0.0, "top1_taux_span": 0.0, "topk_taux_span": 0.0, "topk_exact": 0, "topk_exact_taux": 0.0, "topk_exact_taux_span": 0.0, "exact_taux_span": 0.0, "verbe": {"cibles": 76, "justes": 0, "taux": 0.0}, "nom": {"cibles": 1, "justes": 0, "taux": 0.0}, "couverture": 0.3222}
cascade {"cibles": 239, "labels": 136, "top1": 132, "topk": 134, "exact": 129, "top1_taux": 0.5523, "topk_taux": 0.5607, "exact_taux": 0.5397, "top1_taux_span": 0.9706, "topk_taux_span": 0.9853, "topk_exact": 133, "topk_exact_taux": 0.5565, "topk_exact_taux_span": 0.9779, "exact_taux_span": 0.9485, "verbe": {"cibles": 107, "justes": 103, "taux": 0.9626}, "nom": {"cibles": 29, "j
… [49 caractères tronqués]
  ```

- **bash** `{"command": "git log --all --oneline --decorate -15; echo '---'; git log --all --oneline --grep='multi-cible\\|multicible\\|cibles multiples' -i | head -20", "description": "Inspect git history for multi-target work"}`

  ```
1ec7286c (HEAD -> s/v7) PILOTAGE — LES QUATRE VAGUES DE SOUS-AGENTS DOCUMENTÉES (§ 9) ; VAGUES 3 ET 4 EN COURS
a914c1e7 FICHES — LES 3 DIVERGENCES ET LEURS RÉSIDUS CORRIGÉS (SPANS, DÉNOMINATEUR, LEXIQUE ÉLARGI) ; COHÉRENCE A4 À JOUR
a2def5ee PILOTAGE — LE CACHE DU CHUNKER AU JOURNAL ; T0 DANS LE BUDGET ; 181/181
e0592c59 B13 — LE CACHE DU CHUNKER APPLIQUÉ : ×139 À 160 RÉPÉTITIONS, SORTIE IDENTIQUE (0/612) ; ×1 EN DÉFAUT, S DOMINE ; 181/181
de292c7d ÉTAT — B13 180/180, T0 DANS LE BUDGET ; VAGUE 3 LANCÉE (AUDIT V2, ÉCHECS, REPLIS, CACHE)
2e08cbc7 B13 — LA VAGUE 1 COMPLÈTE : CONTRAT S, COÛT DU CHUNKER, COHÉRENCE DES FICHES ; 3 DIVERGENCES CORRIGÉES
9d5337ce B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180
e1171032 PILOTAGE — PROTOCOLE D'INTÉGRATION DES SOUS-AGENTS (REJOUER, REJETER, COMMITTER VÉRIFIÉ) ; § 9
4a65d44f PILOTAGE — VAGUE 1 DES SOUS-AGENTS NOTÉE ; HORODATAGES ALIGNÉS SUR 13 H 15
dfc860a4 ÉTAT — LE LIEN VERS PLAN-TRAVAIL EST RÉPARÉ (../PLAN-TRAVAIL.MD → PLAN-TRAVAIL.MD) ; LA REVUE DE DOCUMENTATION REPASSE VERTE
56d70431 ÉTAT — B13 177/177, TRIM T0 ; LA TRANCHE SOUS-AGENTS CONTINUE
6
… [449 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"A13\\|multi-cibles\\|multicibles\" docs/pilotage/ docs/methode/ 2>/dev/null | head -30", "description": "Search roadmap for A13"}`

  ```
docs/pilotage/plan-travail.md:430:| **4** | A12 spans sans S, A13 multi-cibles, A14 gold anglais | couverture, définition de la mesure, qualité du gold | en cours |
  ```

- **bash** `{"command": "git show --stat 9d5337ce | head -60; echo '==='; git show 9d5337ce -- tools/tests/linguistique/evaluer_gold.py | head -200", "description": "Inspect attachement v2 commit"}`

  ```
commit 9d5337ce1c23c4d70f51490d2fcdfa2c390e3faa
Author: Stéphane <stephane@localhost>
Date:   Thu Nov 5 14:14:38 2026 -0500

    B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180

 docs/implantation/moteur-de-pensee.md              |    7 +-
 docs/pilotage/chantiers.md                         |    8 +-
 docs/pilotage/en-cours.md                          |   12 +-
 docs/pilotage/roadmap.md                           |    6 +-
 journal/2026-11-05/README.md                       |   28 +-
 journal/2026-11-05/attention.md                    |   16 +-
 journal/2026-11-05/distribue.md                    |   19 +-
 journal/2026-11-05/docs.md                         |   16 +-
 journal/2026-11-05/memoire.md                      |   16 +-
 journal/2026-11-05/mesures.md                      |   16 +-
 journal/2026-11-05/modele.md                       |   16 +-
 journal/2026-11-05/moteur.md                       |   16 +-
 journal/2026-11-05/portes.md                       |   16 +-
 journal/README.md                                  |   16 +-
 .../53bc3288-f2c1-4a7d-b1db-88d794074f70/digest.md | 1555 
… [3863 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/pensee-attachement-v2.json; echo '==='; sed -n '1,120p' reports/rapport-pensee-attachement-v2.md", "description": "Read attachment v2 report"}`

  ```
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "180/180",
 "labels": 145,
 "cibles": 239,
 "avant": {
  "exact": 123,
  "exact_span": 0.8483,
  "top1": 126,
  "topk": 134,
  "topk_exact": 88,
  "verbe_est": 0.9524,
  "nom_est": 0.7683
 },
 "apres": {
  "exact": 137,
  "exact_span": 0.9448,
  "top1": 140,
  "topk": 142,
  "topk_exact": 141,
  "top1_span": 0.9655,
  "topk_span": 0.9793,
  "topk_exact_span": 0.9724,
  "verbe_pos": 0.9569,
  "nom_pos": 0.8966,
  "verbe_cibles": 116,
  "nom_cibles": 29
 },
 "rendement": {
  "top1": 0.5858,
  "topk": 0.5941,
  "exact": 0.5732
 },
 "corrections": {
  "segment_precedent": {
   "gain_exact": 6,
   "source": "A7",
   "ids": [
    "s012",
    "s030",
    "s052",
    "s097",
    "s124",
    "s139"
   ]
  },
  "lexique_anglais": {
   "gain_exact": 8,
   "gain_top1": 8,
   "source": "A2",
   "risque": "borne haute"
  },
  "tetes_candidats": {
   "gain_topk_strict": 45,
   "source": "A2"
  }
 },
 "modele_appris": {
  "exact": 0.9793,
  "vs_regle": 137,
  "gain": 5,
  "mcnemar": "7/2",
  "p": 0.18,
  "ic95": [
   -0.7,
   7.6
  ],
  "decision": "rejete"
 },
 "echecs": {
  "hors_candidats": 3,
  "mal_classes": 5,
  "total": 8
 },
 "spans": {

… [5573 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -i \"multi\\|cibles\\[0\\]\\|alternative\" reports/rapport-audit-attachement.md reports/rapport-pensee-attachement-v2.md reports/rapport-topk-diagnostic.md | head -40", "description": "Search multi-target mentions in recent reports"}`

  ```
(no output)
  ```

