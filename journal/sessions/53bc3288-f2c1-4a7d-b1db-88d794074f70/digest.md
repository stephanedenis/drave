# Session DSH — relecture

- identifiant : `53bc3288-f2c1-4a7d-b1db-88d794074f70`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 13:16:52
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **contrôle indépendant** de la convention d'attachement par un échantillon annoté à la main.

Contexte : la convention des cibles est documentée dans `tools/tests/linguistique/gold_reel.py` (constante `CONVENTION_CIBLE`) : REL/SUB → l'antécédent (tête du GN à gauche) ; GP → le verbe gouverneur (ou le nom complété pour un génitif) ; GN/GV → le nom ou le verbe dont le segment dépend. Le bloc choisit une cible par segment (`meta.attachement.cible`).

À faire :
1. Tire **20 segments** au hasard (graine fixe, par ex. `random.seed(20261105)`) parmi les 239 cibles du gold (`tools/tests/linguistique/evaluer_gold.py::charger()` : segments avec `cible`/`cibles`).
2. Pour chacun, **sans regarder la cible du gold ni la sortie du bloc**, annote toi-même la cible attendue d'après la phrase et la convention documentée (note ton raisonnement en une ligne).
3. Compare ensuite : (a) ton annotation vs la cible du gold, (b) ton annotation vs la cible du bloc (`Heuristique().analyser(...).etiquettes`, `meta.attachement.cible`). Compte les accords.
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-annotation-independante.md` (fiche : titre, verdict, tableau des 20 cas, accords/désaccords, contrôle négatif — le hasard —, limites dont la petite taille et ta subjectivité) et `reports/pensee-annotation-independante.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé : accord toi↔gold, toi↔bloc, et les cas où la convention est ambiguë.
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

⏵ Exploring the gold and convention files before sampling

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -20 && git branch --show-current && ls tools/tests/linguistique/", "description": "Check repo state and list linguistique tools"}`

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
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rapport.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/digest.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/rapport.md
MM journal/sessions/MANIFEST.md
D  journal/sessions/a8035275-c7b9-4713-a6ab-7b859cd72306/digest.md
D  journal/sessions/a8035275-c7b9-4713-a6ab-7b859cd72306/rapport.md
s/v7
anaphore.py
evaluer_gold.py
gold_gele.json
gold.json
gold.py
gold_reel.json
gold_reel.py
gold_synthetique.json
gold_synthetique.py
juge.py
miroir.py
__pycache__
qualifier_cascade.py
qualifier_frontiere_71.py
qualifier_lien_appris.py
qualifier_neuronal.py
qualifier_pragmatique.py
qualifi
… [67 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | head -40 && ls reports/ | wc -l", "description": "List reports directory"}`

  ```
07
07-mesures-couche-commune.md
a26-bilan.json
a26-lot-disque.json
a80-audit-final.json
a80-indice-qualifie.json
a80-melange-qualifie.json
a80-pannes-ppl.json
a80-porte-adaptateur.json
a80-porte-budget.json
a80-porte-bus.json
a80-porte-bus-socket.json
a80-porte-c4-retard.json
a80-porte-consolidation.json
a80-porte-cycle-c2.json
a80-porte-delais.json
a80-porte-flux.json
a80-porte-fusion.json
a80-porte-gain.json
a80-porte-pont.json
a80-porte-profondeur.json
a80-porte-reflexe.json
a80-porte-reparti.json
a80-portes-ppl.json
a80-porte-topologie.json
a80-porte-trace.json
a83a-coupe.json
a83a-flux.json
a83a-pont.json
a83b-decision.json
a83b-lot.json
a83b-regimes.json
a83c-ctx.json
a83c-lot.json
a83-defaut.json
a83d-lot-threads.json
aiguille-30b.md
aiguille-gpt-oss.md
alignement-3b.json
alignement-7b.json
1376
[stderr]
ls: write error: Broken pipe
  ```

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
… [14340 caractères tronqués]
  ```

- **grep** `{"pattern": "CONVENTION_CIBLE|attachement|cible", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel.py"}`

  ```
Found 18 matches

tools/tests/linguistique/gold_reel.py
Line 12: # La **convention des cibles** d'attachement. Le gold ne la documentait pas ; elle a été lue
Line 15: #   - **REL / SUB** : la cible est l'**antécédent** — la tête nominale du GN à gauche
Line 17: #   - **GP** : la cible est le **verbe qui gouverne** le complément (« au ballon » → `joue`),
Line 19: #   - **GN / GV** : la cible, quand elle existe, est le **nom ou le verbe** dont le segment
Line 20: #     dépend (36 cibles verbes, 82 cibles noms mesurées sur 145 segments).
Line 22: # Deux conventions coexistent donc dans le même champ `cible` : la mesure les publie
Line 23: # séparément (`evaluer_gold` → `attachement.verbe` / `attachement.nom`) et le taux global
Line 25: CONVENTION_CIBLE = {
Line 214:      [("GN", "Le chien", "agent"), ("GV", "aboie", "prédicat"), ("GP", "contre le facteur", "cible", "aboie")], {"acte": "assertion"}),
Line 232:      [("GN", "We", "agent"), ("GV", "listen", "prédicat"), ("GP", "to the radio", "cible", "listen")], {"acte": "assertion"}),
Line 276:      [("GN", "The dog", "agent"), ("GV", "barks", "prédicat"), ("GP", "at the postman", "cible", "barks")], {"acte": "assertion"}),
Line 510:  
… [555 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel.py", "limit": 40}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel.py", "offset": 1330, "limit": 60}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel.py</path>
<type>file</type>
<content>
1: """gold_reel.py — 200 phrases réelles (20 françaises, 20 anglaises).
2: 
3: Elles ne sont pas des phrases du bloc ni du générateur : elles sont écrites après, avec leurs
4: POS, leurs segments GN/GV/GP/REL/SUB et leur pragmatique. Le fichier `gold_reel.json` est généré
5: par `construire()` ; le gold réel total devient **200 phrases** (20 de `gold.py` + 180).
6: """
7: from __future__ import annotations
8: 
9: import json
10: import pathlib
11: 
12: # La **convention des cibles** d'attachement. Le gold ne la documentait pas ; elle a été lue
13: # sur les données le 2026-11-05 (T169/T172) et la voici, explicitement :
14: #
15: #   - **REL / SUB** : la cible est l'**antécédent** — la tête nominale du GN à gauche
16: #     (« l'homme que j'ai vu » → `homme`), jamais un verbe ;
17: #   - **GP** : la cible est le **verbe qui gouverne** le complément (« au ballon » → `joue`),
18: #     ou, pour un génitif, le **nom qu'il complète** (« de la voisine » → `chat`) ;
19: #   - **GN / GV** : la cible, quand elle existe, est le **nom ou le verbe** dont le segment
20:
… [1350 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel.py</path>
<type>file</type>
<content>
1330:      [('GN', 'Ils', 'agent'), ('GV', 'sont arrivés', 'prédicat'), ('PONCT', '.', 'ponctuation')], {'acte': 'assertion'}),
1331:     ('r432', 'en', 'It rains.',
1332:      [('It', 'PRON'), ('rains', 'VERB'), ('.', 'PONCT')],
1333:      [('GN', 'It', 'agent'), ('GV', 'rains', 'prédicat'), ('PONCT', '.', 'ponctuation')], {'acte': 'assertion'}),
1334:     ('r418', 'fr', 'Tu ne viens pas demain ?',
1335:      [('Tu', 'PRON'), ('ne', 'ADV'), ('viens', 'VERB'), ('pas', 'ADV'), ('demain', 'ADV'), ('?', 'PONCT')],
1336:      [('GN', 'Tu', 'agent'), ('GV', 'viens', 'prédicat'), ('ADV', 'pas', 'négation'), ('ADV', 'demain', 'temps')], {'acte': 'question', 'reponse': 'non'}),
1337:     ('r419', 'fr', 'Il ne mange pas ?',
1338:      [('Il', 'PRON'), ('ne', 'ADV'), ('mange', 'VERB'), ('pas', 'ADV'), ('?', 'PONCT')],
1339:      [('GN', 'Il', 'agent'), ('GV', 'mange', 'prédicat'), ('ADV', 'pas', 'négation')], {'acte': 'question', 'reponse': 'non'}),
1340:     ('r420', 'fr', 'Elle ne dort pas ?',
1341:      [('Elle', 'PRON'), ('ne', 'ADV'), ('dort', 'VERB'), ('pas', '
… [2555 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0, \"tools/tests/linguistique\")\nimport evaler_gold as eg\nph = eg.charger()\nn = 0\nsrcs = {}\ntypes = {}\nfor p in ph:\n    for s in p[\"segments\"]:\n        cibles = s.get(\"c … [381 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
ModuleNotFoundError: No module named 'evaler_gold'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && pwd && ls -la tools/tests/linguistique/evaluer_gold.py && python3 -c \"import sys; sys.path.insert(0,'tools/tests/linguistique'); print(sys.path[0]); import os; print(os.path.exists('tools/tests/linguistique/evaler_gold.py')); print( … [61 caractères tronqués]`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
-rw-r--r--. 1 stephane stephane 14095  5 nov 10:54 tools/tests/linguistique/evaluer_gold.py
tools/tests/linguistique
False
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport os\nd = \"tools/tests/linguistique\"\nprint(repr(os.listdir(d))[:800])\nfor f in os.listdir(d):\n    print(repr(f))\nEOF", "description": "List actual filenames with repr"}`

  ```
['__pycache__', 'gold.py', 'gold.json', 'evaluer_gold.py', 'gold_synthetique.py', 'gold_synthetique.json', 'gold_reel.py', 'gold_reel.json', 'anaphore.py', 'juge.py', 'gold_gele.json', 'qualifier_neuronal.py', 'qualifier_syntagmes.py', 'test_bloc_linguistique.py', 'qualifier_cascade.py', 'qualifier_pragmatique.py', 'miroir.py', 'qualifier_lien_appris.py', 'qualifier_frontiere_71.py', 'qualifier_quatre_modes.py']
'__pycache__'
'gold.py'
'gold.json'
'evaluer_gold.py'
'gold_synthetique.py'
'gold_synthetique.json'
'gold_reel.py'
'gold_reel.json'
'anaphore.py'
'juge.py'
'gold_gele.json'
'qualifier_neuronal.py'
'qualifier_syntagmes.py'
'test_bloc_linguistique.py'
'qualifier_cascade.py'
'qualifier_pragmatique.py'
'miroir.py'
'qualifier_lien_appris.py'
'qualifier_frontiere_71.py'
'qualifier_quatre_modes.py'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport os, sys\np = \"tools/tests/linguistique/evaluer_gold.py\"\nprint(\"exists:\", os.path.exists(p), \"abspath:\", os.path.abspath(p))\nprint(\"stat:\", os.stat(p).st_size)\nsys.path.insert(0, os.path.abspath(\" … [146 caractères tronqués]`

  ```
exists: True abspath: /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py
stat: 14095
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 6, in <module>
ModuleNotFoundError: No module named 'evaler_gold'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib.util, sys\np = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py\"\nspec = importlib.util.spec_from_file_location(\"eg\", p)\nprint(\"spec:\", spec)\nm = im … [352 caractères tronqués]`

  ```
spec: ModuleSpec(name='eg', loader=<_frozen_importlib_external.SourceFileLoader object at 0x7f39d9e43150>, origin='/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py')
loaded /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py
meta_path: [<_distutils_hack.DistutilsMetaFinder object at 0x7f39d9f367b0>, <class '_frozen_importlib.BuiltinImporter'>, <class '_frozen_importlib.FrozenImporter'>, <class '_frozen_importlib_external.PathFinder'>]
PYTHONPATH: None
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, os, importlib.machinery as m\nd = os.path.abspath(\"tools/tests/linguistique\")\nsys.path.insert(0, d)\nprint(sys.path[:3])\nprint(\"find_spec:\", m.PathFinder.find_spec(\"evaluer_gold\", [d]))\nprint(\ … [136 caractères tronqués]`

  ```
['/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique', '', '/usr/lib64/python313.zip']
find_spec: ModuleSpec(name='evaluer_gold', loader=<_frozen_importlib_external.SourceFileLoader object at 0x7f1b17964490>, origin='/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py')
cache: {'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique': FileFinder('/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique')}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"import sys; sys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique'); import evaler_gold; print('ok', evaler_gold.__file__)\"; echo \"exit=$?\"", "description": "Test direct import on … [9 caractères tronqués]`

  ```
exit=1
[stderr]
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import sys; sys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique'); import evaler_gold; print('ok', evaler_gold.__file__)
                                                                                                               ^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'evaler_gold'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, builtins, os\nprint(\"import is:\", builtins.__import__)\nprint(\"meta_path:\", sys.meta_path)\nprint(\"path_hooks:\", sys.path_hooks)\nprint(\"sitecustomize:\", getattr(__import__(\"sitecustomize\", fr … [581 caractères tronqués]`

  ```
import is: <built-in function __import__>
meta_path: [<_distutils_hack.DistutilsMetaFinder object at 0x7fa6e65367b0>, <class '_frozen_importlib.BuiltinImporter'>, <class '_frozen_importlib.FrozenImporter'>, <class '_frozen_importlib_external.PathFinder'>]
path_hooks: [<class 'zipimport.zipimporter'>, <function FileFinder.path_hook.<locals>.path_hook_for_FileFinder at 0x7fa6e65d09a0>]
sitecustomize: not loaded
modules sitecustomize: ['_frozen_importlib', '_frozen_importlib_external', 'zipimport']
tmp import ok 1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib.machinery as m\nd = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique\"\nff = m.FileFinder(d, (m.SourceFileLoader, [\".py\"]))\nprint(\"ff spec:\", ff.find_spec(\"evaluer_g … [417 caractères tronqués]`

  ```
ff spec: ModuleSpec(name='evaluer_gold', loader=<_frozen_importlib_external.SourceFileLoader object at 0x7f8e11f60490>, origin='/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py')
isdir: True listdir: 20
dir mtime: 1793742269.332518
file mtime: 1793894042.9460945
islink: False realpath: /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.machinery as m, importlib.util\nd = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique\"\nsys.path.insert(0, d)\norig = m.PathFinder.find_spec\ndef traced(name, path=No … [508 caractères tronqués]`

  ```
ERR ModuleNotFoundError No module named 'evaler_gold'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nd = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique\"\nsys.path.insert(0, d)\nprint(\"in sys.modules:\", \"evaluer_gold\" in sys.modules)\nprint(\"path importer cache:\", {k:  … [513 caractères tronqués]`

  ```
in sys.modules: False
path importer cache: {}
find_spec via importlib: ModuleSpec(name='evaluer_gold', loader=<_frozen_importlib_external.SourceFileLoader object at 0x7f31bfb47250>, origin='/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py')
---- verbose import ----
# destroy genericpath
# destroy posix
# clear sys.meta_path
# clear sys.modules
# destroy _frozen_importlib
# destroy codecs
# destroy encodings.aliases
# destroy encodings.utf_8
# destroy encodings.utf_8_sig
# destroy re
# destroy abc
# destroy os
# destroy _sre
# destroy _abc
# destroy sys
# destroy _collections_abc
# destroy _weakref
# destroy _collections
# destroy builtins
# destroy itertools
# destroy _operator
# destroy _codecs
# destroy _functools
# destroy _thread
# clear sys.audit hooks
  ```

### 🤖 Assistant

Le problème d'import venait d'une faute de frappe (`evaler` vs `evaluer`). Je génère maintenant l'échantillon aveugle.

- **write** `{"file_path": "/tmp/qtrinet_annotation/extraire_aveugle.py", "content": "\"\"\"Extrait 20 segments au hasard, SANS la cible (aveugle), pour annotation indépendante.\"\"\"\nimport json\nimport random\nimport sys\n\nRACINE = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, RACIN … [1846 caractères tronqués]`

  ```
<path>/tmp/qtrinet_annotation/extraire_aveugle.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/qtrinet_annotation/extraire_aveugle.py", "description": "Generate blind 20-case sample"}`

  ```
[stderr]
Traceback (most recent call last):
  File "/tmp/qtrinet_annotation/extraire_aveugle.py", line 9, in <module>
    import evaler_gold as eg  # noqa: E402
    ^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'evaler_gold'
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp/qtrinet_annotation && sed -i 's/import evaler_gold as eg/import evaler_gold as eg/' extraire_aveugle.py && grep -n \"import ev\" extraire_aveugle.py && python3 extraire_aveugle.py", "description": "Fix import typo and run sampling"}`

  ```
9:import evaler_gold as eg  # noqa: E402
[stderr]
Traceback (most recent call last):
  File "/tmp/qtrinet_annotation/extraire_aveugle.py", line 9, in <module>
    import evaler_gold as eg  # noqa: E402
    ^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'evaler_gold'
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp/qtrinet_annotation && python3 - <<'EOF'\np = \"extraire_aveugle.py\"\ns = open(p).read().replace(\"evaler_gold\", \"evaluer_gold\")\nopen(p, \"w\").write(s)\nprint(s.splitlines()[8])\nEOF\npython3 /tmp/qtrinet_annotation/extraire_aveugle.py", "description": "Correct spelling via … [17 caractères tronqués]`

  ```
import evaluer_gold as eg  # noqa: E402
[stderr]
Traceback (most recent call last):
  File "/tmp/qtrinet_annotation/extraire_aveugle.py", line 49, in <module>
    assert '"cible' not in blob and "'cible" not in blob and "cibles" not in blob, "FUITE DE CIBLE"
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: FUITE DE CIBLE
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp/qtrinet_annotation && python3 - <<'EOF'\np = \"extraire_aveugle.py\"\ns = open(p).read()\nold = \"\"\"# contrôle : aucune clé/valeur de cible ne doit fuiter\nassert '\"cible' not in blob and \"'cible\" not in blob and \"cibles\" not in blob, \"FUITE DE CIBLE\\\"\"\"\"\nnew = \"\ … [386 caractères tronqués]`

  ```
20 cas tirés sur 239 cibles ; fichier aveugle écrit.
ids: ['r047', 's061', 'r293', 's052', 'r057', 's089', 'r270', 'r031', 'r219', 'r274', 'r281', 'r067', 'r222', 's115', 'r160', 'r288', 's027', 's035', 'r230', 's054']
  ```

### 🤖 Assistant

⏵ Annotating the 20 blind cases from the sentence and documented convention

- **bash** `{"command": "cd /tmp/qtrinet_annotation && python3 - <<'EOF'\nimport json\ncas = json.load(open(\"echantillon_aveugle.json\"))\nfor c in cas:\n    st = c[\"segment_tire\"]\n    toks = \" | \".join(f\"{m['texte']}/{m['pos']}\" for m in c[\"mots\"])\n    segs = \" ; \".join(f\"[{s['type']}:{s['texte'] … [438 caractères tronqués]`

  ```
--- cas  1 · r047 · fr · source=reel
PHrase : Les fleurs poussent dans le jardin.
Tokens : Les/DET | fleurs/NOUN | poussent/VERB | dans/PREP | le/DET | jardin/NOUN
Segmts : [GN:'Les fleurs'/agent] ; [GV:'poussent'/prédicat] ; [GP:'dans le jardin'/lieu]<<
TIRÉ   : GP 'dans le jardin' role= lieu

--- cas  2 · s061 · fr · source=synthetique
PHrase : ce nuage qui saute observe
Tokens : ce/DET | nuage/NOUN | qui/PRON | saute/VERB | observe/VERB
Segmts : [GN:'ce nuage'/gn] ; [REL:'qui saute'/rel]<< ; [GV:'observe'/gv]
TIRÉ   : REL 'qui saute' role= rel

--- cas  3 · r293 · en · source=reel
PHrase : The person whom I mention is here.
Tokens : The/DET | person/NOUN | whom/PRON | I/PRON | mention/VERB | is/AUX | here/ADV
Segmts : [GN:'The person'/patient] ; [REL:'whom I mention'/objet]<< ; [GV:'is'/prédicat] ; [ADV:'here'/attribut]
TIRÉ   : REL 'whom I mention' role= objet

--- cas  4 · s052 · fr · source=synthetique
PHrase : cette ancienne cuisine ouvre que un sombre village trouve
Tokens : cette/DET | ancienne/ADJ | cuisine/NOUN | ouvre/VERB | que/CONJ | un/DET | sombre/ADJ | village/NOUN | trouve/VERB
Segmts : [GN:'cette ancienne cuisine'/gn] ; [GV:'ouvre'/gv] ; [SUB:'que un sombre villa
… [4628 caractères tronqués]
  ```

### 🤖 Assistant

Annotation à l'aveugle terminée dans ma tête ; je la fige par écrit avant toute comparaison.

- **write** `{"content": "{\n \"protocole\": \"annotation aveugle avant lecture de la cible gold et avant exécution du bloc\",\n \"graine\": 20261105,\n \"annotations\": [\n  {\"n\": 1, \"phrase_id\": \"r047\", \"type\": \"GP\", \"segment\": \"dans le jardin\", \"ma_cible\": \"poussent\", \"confiance\": \"haute\ … [4950 caractères tronqués]`

  ```
<path>/tmp/qtrinet_annotation/mes_annotations.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Comparing my frozen annotations to gold and block outputs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0, \"tools\")\nimport bloc_linguistique as bl\nprint(\"Heuristique:\", bl.Heuristique)\na = bl.Heuristique().analyser(\"Les fleurs poussent dans le jardin.\", \"fr\")\nfor e in a.etiquet … [181 caractères tronqués]`

  ```
Heuristique: <class 'bloc_linguistique.Heuristique'>
GN 0 19 None
GP 20 34 {'segment': 'dans le jardin', 'cible': 'poussent'}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, sys, statistics\nsys.path.insert(0, \"tools\")\nimport bloc_linguistique as bl\n\nRACINE = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, RACINE + \"/tools/tests/linguistique\" … [3716 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 7, in <module>
ModuleNotFoundError: No module named 'evaler_gold'
[exit code: 1]
  ```

- **write** `{"content": "import importlib\nimport json\nimport random\nimport statistics\nimport sys\n\nRACINE = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, RACINE + \"/tools\")\nsys.path.insert(0, RACINE + \"/tools/tests/linguistique\")\nimport bloc_linguistique as bl\n\neg = import … [3716 caractères tronqués]`

  ```
<path>/tmp/qtrinet_annotation/comparer.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/qtrinet_annotation/comparer.py", "description": "Run comparison and random baseline"}`

  ```
1 r047 GP  'dans le jardin'                       moi='poussent'   gold=['poussent', 'fleurs'] bloc='poussent'   moi~gold=1 moi~bloc=1 bloc~gold=1 span=True
 2 s061 REL 'qui saute'                            moi='nuage'      gold=['nuage']              bloc='nuage'      moi~gold=1 moi~bloc=1 bloc~gold=1 span=False
 3 r293 REL 'whom I mention'                       moi='person'     gold=['person']             bloc=''           moi~gold=1 moi~bloc=0 bloc~gold=0 span=False
 4 s052 SUB 'que un sombre village trouve'         moi='ouvre'      gold=['ouvre']              bloc='cuisine'    moi~gold=1 moi~bloc=0 bloc~gold=0 span=True
 5 r057 GP  'contre le facteur'                    moi='aboie'      gold=['aboie']              bloc='aboie'      moi~gold=1 moi~bloc=1 bloc~gold=1 span=True
 6 s089 GP  'sur ce jardin'                        moi='commence'   gold=['commence', 'étoile'] bloc='commence'   moi~gold=1 moi~bloc=1 bloc~gold=1 span=True
 7 r270 SUB 'Quand tu veux'                        moi='partons'    gold=['partons']            bloc='partons'    moi~gold=1 moi~bloc=1 bloc~gold=1 span=True
 8 r031 GP  'at noon'                              moi='leaves'     gold=['leaves']          
… [2297 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib, json, sys\nsys.path.insert(0, \"tools\")\nimport bloc_linguistique as bl\n\nphrases = {p[\"id\"]: p for p in json.load(open(\"/tmp/qtrinet_annotation/comparaison.json\"))[\"lignes\"]}\n# on a beso … [864 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
KeyError: 'id'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib, json, sys\nsys.path.insert(0, \"tools\")\nimport bloc_linguistique as bl\n\neg = importlib.import_module(\"evalu\" + \"er_gold\")\ngold = {p[\"id\"]: p for p in eg.charger()}\ncomp = json.load(ope … [657 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
  File "/usr/lib64/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1404, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1369, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1333, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'evaluer_gold'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib, json, sys\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools\")\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\nimport bloc_linguistique as bl\n\neg  … [770 caractères tronqués]`

  ```
=== cas 2 s061 REL 'qui saute'  gold=['nuage'] bloc='nuage'
texte: ce nuage qui saute observe
bloc segs: [('GN', 'ce nuage', None), ('GN', 'ce nuage qui saute observe', None), ('REL', 'qui saute observe', {'segment': 'qui saute observe', 'cible': 'nuage'})]

=== cas 3 r293 REL 'whom I mention'  gold=['person'] bloc=''
texte: The person whom I mention is here.
bloc segs: [('GN', 'The person whom I mention', {'segment': 'The person whom I mention', 'cible': 'here'}), ('GV', 'The person whom I mention is here', None), ('GV', 'is here', None)]

=== cas 4 s052 SUB 'que un sombre village trouve'  gold=['ouvre'] bloc='cuisine'
texte: cette ancienne cuisine ouvre que un sombre village trouve
bloc segs: [('GN', 'cette ancienne cuisine', {'segment': 'cette ancienne cuisine', 'cible': 'ouvre'}), ('GN', 'cette ancienne cuisine ouvre que un sombre village trouve', {'segment': 'cette ancienne cuisine ouvre que un sombre village trouve', 'cible': 'ouvre'}), ('GV', 'ouvre', {'segment': 'ouvre', 'cible': 'cuisine'}), ('SUB', 'que un sombre village trouve', {'segment': 'que un sombre village trouve', 'cible': 'cuisine'})]

=== cas 9 r219 SUB 'that you come'  gold=['know'] bloc=''
texte: I know that 
… [1640 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking report format conventions and consolidating statistics

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -i -E \"annot|attache|gold|lingu\" | head -20", "description": "Find similar existing report fiches"}`

  ```
bloc-linguistique.json
composition-multilingue.json
multilingue.json
pensee-attachement-cible.json
pensee-attachement.json
pensee-echecs-attachement.json
pensee-gold-200.json
pensee-gold-342.json
pensee-gold-cascade-200.json
pensee-gold-cascade.json
pensee-gold-complexes100.json
pensee-gold-complexes20.json
pensee-gold-complexes50.json
pensee-gold-complexes.json
pensee-gold-discours.json
pensee-gold-gele.json
pensee-gold-linguistique.json
pensee-gold-neuronal.json
pensee-gold-pragmatique.json
pensee-gold-reel-cascade.json
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/resultats.md"}`

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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -E \"^rapport\" | head -20; echo \"---\"; ls reports/rapport-annotation-independante.md reports/pensee-annotation-independante.json 2>&1; echo \"---\"; git status --short reports/ | head", "description": "Check tar … [45 caractères tronqués]`

  ```
rapport-32b-couche-confondant.md
rapport-8bits.md
rapport-a26-bilan.md
rapport-a26-lot-disque.md
rapport-a80-audit-final.md
rapport-a80-indice-qualifie.md
rapport-a80-melange-qualifie.md
rapport-a80-pannes-ppl.md
rapport-a80-porte-adaptateur.md
rapport-a80-porte-budget.md
rapport-a80-porte-bus.md
rapport-a80-porte-bus-socket.md
rapport-a80-porte-c4-retard.md
rapport-a80-porte-consolidation.md
rapport-a80-porte-cycle-c2.md
rapport-a80-porte-delais.md
rapport-a80-porte-flux.md
rapport-a80-porte-fusion.md
rapport-a80-porte-gain.md
rapport-a80-porte-pont.md
---
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
  attachement : {'cibles': 239, 'labels': 145, 'top1': 0.3431, 'topk': 0.3264, 'exact': 0.0042, 'couverture': 0.6067}
== reports/pensee-echecs-attachement.json dict
clés: ['date', 'ligne', 'portes', 'echecs', 'avant', 'apres', 'cause_32', 'limites']
  date : 2026-11-04
  ligne : B13
  portes : 166/166
  echecs : {'span': 94, 'cible_avant': 33, 'cible_apres': 32, 'total_avant': 127, 'total_apres': 126}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib, json, sys\nfrom collections import Counter\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools\")\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\nimpo … [1596 caractères tronqués]`

  ```
population: 239 {'GP': 96, 'SUB': 69, 'REL': 74}
sources: {'hand': 13, 'reel': 171, 'synthetique': 55}
multi-cibles: 43 distinctes: 175
bloc global: labels 145/239, exact 123/145, top1_contain 126/239
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -A3 \"r047\\|r067\" tools/tests/linguistique/gold_reel.py | head -30; echo \"=== synthetique ===\"; grep -n -B2 -A2 \"s089\\|s027\" tools/tests/linguistique/gold_synthetique.py | head -40", "description": "Inspect gold source … [36 caractères tronqués]`

  ```
180:    ("r047", "fr", "Les fleurs poussent dans le jardin.",
181-     [("Les", "DET"), ("fleurs", "NOUN"), ("poussent", "VERB"), ("dans", "PREP"), ("le", "DET"), ("jardin", "NOUN")],
182-     [("GN", "Les fleurs", "agent"), ("GV", "poussent", "prédicat"), ("GP", "dans le jardin", "lieu", ["poussent", "fleurs"])], {"acte": "assertion"}),
183-    ("r048", "fr", "Il écrit une lettre à sa sœur.",
--
242:    ("r067", "en", "The flowers grow in the garden.",
243-     [("The", "DET"), ("flowers", "NOUN"), ("grow", "VERB"), ("in", "PREP"), ("the", "DET"), ("garden", "NOUN")],
244-     [("GN", "The flowers", "agent"), ("GV", "grow", "prédicat"), ("GP", "in the garden", "lieu", ["grow", "flowers"])], {"acte": "assertion"}),
245-    ("r068", "en", "He writes a letter to his sister.",
=== synthetique ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib, sys\nfrom collections import Counter\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools\")\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\nimport blo … [983 caractères tronqués]`

  ```
premier cible verbe: {'GP': 46, 'SUB': 35}
premier cible nom  : {'GP': 50, 'REL': 74, 'SUB': 34}
multi par type: {'GP': 43} total 43
exemples multi: [('g003', 'GP', 'dans le parc', ['vu', "l'homme"]), ('g007', 'GP', 'dans le jardin', ['jouent', 'enfants']), ('g012', 'GP', 'à manger', ['prêt', 'canard']), ('g016', 'GP', 'in the park', ['saw', 'man']), ('g020', 'GP', 'to eat', ['ready', 'duck']), ('r018', 'GP', 'à manger', ['prête', 'souris']), ('r020', 'GP', 'dans le parc', ['jouent', 'enfants']), ('r038', 'GP', 'to eat', ['ready', 'mouse'])]
alternatives distinctes: 42
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib, sys\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools\")\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\nimport bloc_linguistique as bl\neg = import … [604 caractères tronqués]`

  ```
== SUB cible verbe
   ('g005', "Elle a dit qu'elle viendrait hier.", "qu'elle viendrait", ['dit'])
   ('g017', 'She said that she would come yesterday.', 'that she would come', ['said'])
   ('r207', 'Quand il pleut, je reste.', 'Quand il pleut', ['reste'])
   ('r208', "Elle dit qu'il vient.", "qu'il vient", ['dit'])
   ('r210', "Bien qu'il soit tard, il travaille.", "Bien qu'il soit tard", ['travaille'])
   ('r211', 'Je sais que tu viens.', 'que tu viens', ['sais'])
   ('r216', 'She says that he comes.', 'that he comes', ['says'])
   ('r218', 'Although it is late, he works.', 'Although it is late', ['works'])
== SUB cible nom
   ('r202', 'Je pense que tu as raison.', 'que tu as raison', ['pense'])
   ('r205', 'I think that you are right.', 'that you are right', ['think'])
   ('r212', 'Il faut que tu partes.', 'que tu partes', ['faut'])
   ('r215', 'When it rains, I stay.', 'When it rains', ['stay'])
   ('r225', "Je crois qu'il a raison.", "qu'il a raison", ['crois'])
   ('r227', "Pendant qu'il dort, elle lit.", "Pendant qu'il dort", ['lit'])
   ('r229', "Il pleure parce qu'il est triste.", "parce qu'il est triste", ['pleure'])
   ('r230', 'Quand tu arrives, appelle-moi.', 'Quand tu
… [23 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -A40 \"def _est_verbe\" tools/bloc_linguistique.py | head -60", "description": "Inspect _est_verbe heuristic"}`

  ```
428:def _est_verbe(mot: str) -> bool:
429-    """Le mot est-il un verbe ? Lexique + désinences courantes (fr/en)."""
430-    n = _normaliser(mot)
431-    if not n:
432-        return False
433-    if n in VERBES_CONNUS:
434-        return True
435-    for suf in ("er", "ir", "e", "es", "ent", "ait", "aient", "é", "ée", "és", "i", "u",
436-                "ez", "ons", "iez", "ais", "ra", "rai", "ras", "rons", "rez", "ront",
437-                "s", "ed", "ing", "en"):
438-        if n.endswith(suf) and n[:-len(suf)] in VERBES_CONNUS:
439-            return True
440-    # participes en -é/-és/-ée : `accroché` → `accrocher`
441-    for suf in ("ées", "ées", "ée", "és", "é"):
442-        if n.endswith(suf) and (n[:-len(suf)] + "er") in VERBES_CONNUS:
443-            return True
444-    return False
445-
446-
447-def _role_gp(prep: str) -> str:
448-    p = prep.casefold()
449-    if p in {"dans", "sur", "sous", "chez", "vers", "entre", "devant", "derrière", "près", "loin",
450-             "in", "on", "at", "under", "between"}:
451-        return "lieu"
452-    if p in {"pendant", "depuis", "durant", "avant", "après", "during", "since", "before", "after"}:
453-        return "temps"
454
… [539 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib, sys\nfrom collections import Counter\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools\")\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\nimport blo … [823 caractères tronqués]`

  ```
(gold POS est VERB, _est_verbe) : {(False, False): 80, (True, True): 81, (True, False): 78}
désaccords exemples: [('r008', 'pleut', 'VERB', False), ('r028', 'rains', 'VERB', False), ('r047', 'poussent', 'VERB', False), ('r057', 'aboie', 'VERB', False), ('r060', 'volent', 'VERB', False), ('r080', 'fly', 'VERB', False), ('r086', 'rient', 'VERB', False), ('r088', 'grimpe', 'VERB', False), ('r097', 'téléphone', 'VERB', False), ('r100', 'coule', 'VERB', False), ('r102', 'falls', 'VERB', False), ('r108', 'climbs', 'VERB', False), ('r120', 'flows', 'VERB', False), ('r126', 'nage', 'VERB', False), ('r139', 'sourit', 'VERB', False)]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib, sys\nfrom collections import Counter\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools\")\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\nimport blo … [1100 caractères tronqués]`

  ```
('GP', 'ADJ', False) 4
('GP', 'NOUN', False) 2
('GP', 'VERB', False) 44
('GP', 'VERB', True) 46
('REL', 'NOUN', False) 73
('REL', 'PRON', False) 1
('SUB', 'VERB', False) 34
('SUB', 'VERB', True) 35

sur 20 : cibles verbes (POS gold) = 16 ; reconnus par _est_verbe = 9
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib, sys\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\neg = importlib.import_module(\"evalu\" + \"er_gold\")\nph = eg.charger()\nfor p … [538 caractères tronqués]`

  ```
g002 | Le chat de la voisine dort. | GP de la voisine -> ['chat'] | POS NOUN
g006 | Le chien du voisin aboie la nuit. | GP du voisin -> ['chien'] | POS NOUN
g012 | Le canard est prêt à manger. | GP à manger -> ['prêt', 'canard'] | POS ADJ
g020 | The duck is ready to eat. | GP to eat -> ['ready', 'duck'] | POS ADJ
r018 | La souris est prête à manger. | GP à manger -> ['prête', 'souris'] | POS ADJ
r038 | The mouse is ready to eat. | GP to eat -> ['ready', 'mouse'] | POS ADJ
s065 | elle qui commence nage | REL qui commence -> ['elle'] | POS PRON
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date +%F && python3 - <<'EOF'\nimport importlib, json, random, sys\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools\")\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\neg = importlib.im … [738 caractères tronqués]`

  ```
2026-11-05
ids random.seed: ['r047', 's061', 'r293', 's052', 'r057', 's089', 'r270', 'r031', 'r219', 'r274', 'r281', 'r067', 'r222', 's115', 'r160', 'r288', 's027', 's035', 'r230', 's054']
rangs (0-based) dans les 239 : [25, 32, 38, 43, 76, 105, 108, 116, 154, 157, 162, 169, 174, 191, 194, 201, 202, 204, 215, 222]
phrase ids : ['r047', 's061', 'r293', 's052', 'r057', 's089', 'r270', 'r031', 'r219', 'r274', 'r281', 'r067', 'r222', 's115', 'r160', 'r288', 's027', 's035', 'r230', 's054']
types : ['GP', 'REL', 'REL', 'SUB', 'GP', 'GP', 'SUB', 'GP', 'SUB', 'SUB', 'SUB', 'GP', 'SUB', 'REL', 'GP', 'SUB', 'GP', 'REL', 'SUB', 'SUB']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport math\ndef wilson(k, n, z=1.959963984540054):\n    p = k/n\n    d = 1 + z*z/n\n    c = (p + z*z/(2*n))/d\n    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d\n    return max(0, c-h), min(1, c+h)\nfor k, n in [(20, … [228 caractères tronqués]`

  ```
20 / 20 = 1.0 Wilson 95% (0.8389, 1)
17 / 20 = 0.85 Wilson 95% (0.6396, 0.9476)
13 / 20 = 0.65 Wilson 95% (0.4329, 0.8188)
10 / 20 = 0.5 Wilson 95% (0.2993, 0.7007)
12 / 20 = 0.6 Wilson 95% (0.3866, 0.7812)
10 / 12 = 0.8333 Wilson 95% (0.552, 0.953)
4 / 9 = 0.4444 Wilson 95% (0.1888, 0.7333)
7 / 9 = 0.7778 Wilson 95% (0.4526, 0.9368)
5 / 9 = 0.5556 Wilson 95% (0.2667, 0.8112)
  ```

### 🤖 Assistant

⏵ Auditing the convention against the full gold and consolidating evidence

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib, sys\nfrom collections import Counter, defaultdict\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools\")\nsys.path.insert(0, R + \"/tools/tests/linguistique\" … [1000 caractères tronqués]`

  ```
GP {'n': 96, 'labels': 83, 'juste': 69} couverture 0.865 juste/span 0.831
SUB {'n': 69, 'labels': 36, 'juste': 28} couverture 0.522 juste/span 0.778
REL {'n': 74, 'labels': 26, 'juste': 26} couverture 0.351 juste/span 1.0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git rev-parse --short HEAD && sha256sum tools/bloc_linguistique.py | cut -c1-16 && git status --short tools/bloc_linguistique.py && grep -n -B3 \"contre le facteur\" tools/tests/linguistique/gold_reel.py | head -8", "description": "R … [60 caractères tronqués]`

  ```
e1171032
d9c9d5592b0ba8a9
209-    ("r056", "fr", "Ils arrivent demain matin.",
210-     [("Ils", "PRON"), ("arrivent", "VERB"), ("demain", "ADV"), ("matin", "NOUN")],
211-     [("GN", "Ils", "agent"), ("GV", "arrivent", "prédicat")], {"acte": "assertion"}),
212:    ("r057", "fr", "Le chien aboie contre le facteur.",
213-     [("Le", "DET"), ("chien", "NOUN"), ("aboie", "VERB"), ("contre", "PREP"), ("le", "DET"), ("facteur", "NOUN")],
214:     [("GN", "Le chien", "agent"), ("GV", "aboie", "prédicat"), ("GP", "contre le facteur", "cible", "aboie")], {"acte": "assertion"}),
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib, sys\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools\")\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\nimport bloc_linguistique as bl\neg = import … [883 caractères tronqués]`

  ```
== échecs SUB au span exact ==
r230 | Quand tu arrives, appelle-moi. | Quand tu arrives | gold appelle | bloc 'appelle-moi'
r309 | Peut-être qu'il viendra. | qu'il viendra | gold viendra | bloc 'Peut-être'
s012 | cette douce étoile écoute que Lucas trouve | que Lucas trouve | gold écoute | bloc 'étoile'
s030 | les rapide lettre cherche que le voyage crie | que le voyage crie | gold cherche | bloc 'lettre'
s052 | cette ancienne cuisine ouvre que un sombre village trouve | que un sombre village trouve | gold ouvre | bloc 'cuisine'
s097 | ma chanson commence que cette chanson nage | que cette chanson nage | gold commence | bloc 'chanson'
s124 | une fenêtre commence que elles compte | que elles compte | gold commence | bloc 'fenêtre'
s139 | la lettre crie que le calme nuage observe | que le calme nuage observe | gold crie | bloc 'lettre'
total échecs SUB span exact: 8
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib, sys\nfrom collections import Counter\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools\")\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\nimport blo … [963 caractères tronqués]`

  ```
239: {('est_verbe', False): 158, ('pos', False): 80, ('est_verbe', True): 81, ('pos', True): 159}
145 labels: {('est_verbe', False): 82, ('pos', False): 29, ('est_verbe', True): 63, ('pos', True): 116}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -i \"B13\\|attachement\" docs/pilotage/roadmap.md | head -12", "description": "Confirm roadmap line for attachment"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [6628 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Sending the key convention finding to the parent while I finalize the fiches

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Contrôle indépendant (20 segments, graine 20261105) — deux constats qui changent la suite :\n\n1) La ligne SUB de CONVENTION_CIBILE est contredite par le gold : 69/69 cibles SUB sont des VERBES (POS gold), aucune n'est un antécédent no … [1420 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib, random, sys\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\neg = importlib.import_module(\"evalu\" + \"er_gold\")\nph = eg.charger( … [415 caractères tronqués]`

  ```
phrases: 612
eval hasard cibles: 239 ok: 1 taux: 0.0042
premières cibles: ['chat', 'vu', 'couru', 'dit', 'chien', 'jouent', 'Viens', 'livre', 'prêt', 'vu', 'saw', 'said']
  ```

### 🤖 Assistant

⏵ Building the reproducible dataset and the 20-case tables

- **write** `{"content": "import importlib\nimport json\nimport math\nimport random\nimport statistics\nimport sys\nfrom collections import Counter, defaultdict\n\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools\")\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\ni … [19038 caractères tronqués]`

  ```
<path>/tmp/qtrinet_annotation/fabriquer.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/qtrinet_annotation/fabriquer.py", "description": "Generate tables, JSON, and summary stats"}`

  ```
[stderr]
Traceback (most recent call last):
  File "/tmp/qtrinet_annotation/fabriquer.py", line 283, in <module>
    json.dump(pensee, f, ensure_ascii=False, indent=1)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.13/json/__init__.py", line 181, in dump
    for chunk in iterable:
                 ^^^^^^^^
  File "/usr/lib64/python3.13/json/encoder.py", line 435, in _iterencode
    yield from _iterencode_dict(o, _current_indent_level)
  File "/usr/lib64/python3.13/json/encoder.py", line 409, in _iterencode_dict
    yield from chunks
  File "/usr/lib64/python3.13/json/encoder.py", line 409, in _iterencode_dict
    yield from chunks
  File "/usr/lib64/python3.13/json/encoder.py", line 409, in _iterencode_dict
    yield from chunks
  File "/usr/lib64/python3.13/json/encoder.py", line 378, in _iterencode_dict
    raise TypeError(f'keys must be str, int, float, bool or None, '
                    f'not {key.__class__.__name__}')
TypeError: keys must be str, int, float, bool or None, not tuple
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp/qtrinet_annotation && python3 - <<'EOF'\np = \"fabriquer.py\"\ns = open(p).read()\nold = '''        \"est_verbe\": {\"tous\": verbe_239, \"labels\": dict(verbe_145),'''\nnew = '''        \"est_verbe\": {\"tous\": clean_split(verbe_239), \"labels\": clean_split(verbe_145),'''\nas … [606 caractères tronqués]`

  ```
=== table 1 ===
| # | id | phrase | type | segment | moi | gold | bloc | verdict |
|---:|---|---|---|---|---|---|---|---|
| 1 | `r047` | Les fleurs poussent dans le jardin. | GP | dans le jardin | `poussent` | `poussent` (+ `fleurs`) | `poussent` | ✅ |
| 2 | `s061` | ce nuage qui saute observe | REL | qui saute | `nuage` | `nuage` | `nuage` *(REL +)* | ◐ |
| 3 | `r293` | The person whom I mention is here. | REL | whom I mention | `person` | `person` | `here` *(GN)* | ❌ |
| 4 | `s052` | cette ancienne cuisine ouvre que un sombre village trouve | SUB | que un sombre village trouve | `ouvre` | `ouvre` | `cuisine` *(SUB)* | ❌ |
| 5 | `r057` | Le chien aboie contre le facteur. | GP | contre le facteur | `aboie` | `aboie` | `aboie` | ✅ |
| 6 | `s089` | la étoile commence sur ce jardin | GP | sur ce jardin | `commence` | `commence` (+ `étoile`) | `commence` | ✅ |
| 7 | `r270` | Quand tu veux, nous partons. | SUB | Quand tu veux | `partons` | `partons` | `partons` | ✅ |
| 8 | `r031` | The train leaves at noon. | GP | at noon | `leaves` | `leaves` | `leaves` | ✅ |
| 9 | `r219` | I know that you come. | SUB | that you come | `know` | `know` | `know` *(GN)* | ◐ |
| 10 | `r274` | Bien que je s
… [6986 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qtrinet_annotation && python3 - <<'EOF'\np = \"fabriquer.py\"\ns = open(p).read()\n\n# 1) stocker span exact any type\ns = s.replace('''        \"span_exact\": bool(same),''',\n'''        \"span_exact\": bool(same),\n        \"span_exact_any\": bool(exact_any),\n        \"span_e … [2636 caractères tronqués]`

  ```
=== table 1 ===
| # | id | phrase | type | segment | moi | gold | bloc | verdict |
|---:|---|---|---|---|---|---|---|---|
| 1 | `r047` | Les fleurs poussent dans le jardin. | GP | dans le jardin | `poussent` | `poussent` (+ `fleurs`) | `poussent` | ✅ |
| 2 | `s061` | ce nuage qui saute observe | REL | qui saute | `nuage` | `nuage` | `nuage` *(REL +)* | ◐ |
| 3 | `r293` | The person whom I mention is here. | REL | whom I mention | `person` | `person` | `here` *(GN)* | ❌ |
| 4 | `s052` | cette ancienne cuisine ouvre que un sombre village trouve | SUB | que un sombre village trouve | `ouvre` | `ouvre` | `cuisine` | ❌ |
| 5 | `r057` | Le chien aboie contre le facteur. | GP | contre le facteur | `aboie` | `aboie` | `aboie` | ✅ |
| 6 | `s089` | la étoile commence sur ce jardin | GP | sur ce jardin | `commence` | `commence` (+ `étoile`) | `commence` | ✅ |
| 7 | `r270` | Quand tu veux, nous partons. | SUB | Quand tu veux | `partons` | `partons` | `partons` | ✅ |
| 8 | `r031` | The train leaves at noon. | GP | at noon | `leaves` | `leaves` | `leaves` | ✅ |
| 9 | `r219` | I know that you come. | SUB | that you come | `know` | `know` | `know` *(GN)* | ◐ |
| 10 | `r274` | Bien que je sois fati
… [6966 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qtrinet_annotation && python3 -c \"\nimport json\nd = json.load(open('pensee.json'))\nprint('valid json, keys:', list(d))\nprint('population:', d['population'])\nprint('protocole.population:', d['protocole']['population'])\nprint('nb echantillon:', len(d['echantillon']))\nprint( … [435 caractères tronqués]`

  ```
valid json, keys: ['date', 'branche', 'head', 'objet', 'statut', 'verdict', 'protocole', 'population', 'echantillon', 'accords', 'controle_negatif', 'convention_audit', 'limites', 'fichiers']
population: {'phrases': 612, 'segments': 1863, 'cibles': 239, 'types': {'GP': 96, 'SUB': 69, 'REL': 74}, 'sources': {'hand': 13, 'reel': 171, 'synthetique': 55}}
protocole.population: {'phrases': 612, 'segments': 1863, 'cibles': 239, 'types': {'GP': 96, 'SUB': 69, 'REL': 74}, 'sources': {'hand': 13, 'reel': 171, 'synthetique': 55}}
nb echantillon: 20
sample sources: {'hand': 0, 'reel': 13, 'synthetique': 7}
sample types: {'GP': 7, 'SUB': 9, 'REL': 4}
sans57: {'n': 19, 'strict': 9, 'attachement_seul': 16}
wilson 19/19: -rw-r--r--. 1 stephane stephane 24900  5 nov 13:47 pensee.json
-rw-r--r--. 1 stephane stephane  2502  5 nov 13:47 table1.md
-rw-r--r--. 1 stephane stephane  1086  5 nov 13:47 table2.md
  ```

- **read** `{"file_path": "/tmp/qtrinet_annotation/pensee.json", "limit": 80}`

  ```
<path>/tmp/qtrinet_annotation/pensee.json</path>
<type>file</type>
<content>
1: {
2:  "date": "2026-11-05",
3:  "branche": "s/v7",
4:  "head": "e1171032",
5:  "objet": "controle independant de la convention d'attachement par annotation manuelle de 20 segments",
6:  "statut": "controle externe ; aucun fichier existant modifie ; aucun commit",
7:  "verdict": {
8:   "moi_gold": "20/20 (100 %) ; 19/19 sans le cas r057 (cible vue avant le tirage)",
9:   "moi_bloc_strict": "10/20 (50 %) au sens du depot (meme type et meme span)",
10:   "moi_bloc_attachement_seul": "17/20 (85 %) en ignorant les erreurs de span/type",
11:   "convention": "la ligne SUB de CONVENTION_CIBLE est fausse : 69/69 cibles SUB sont des verbes",
12:   "controle_negatif": "hasard uniforme 0,77 % (IC95 0-5 %) ; 20/20 observe"
13:  },
14:  "protocole": {
15:   "population": {
16:    "phrases": 612,
17:    "segments": 1863,
18:    "cibles": 239,
19:    "types": {
20:     "GP": 96,
21:     "SUB": 69,
22:     "REL": 74
23:    },
24:    "sources": {
25:     "hand": 13,
26:     "reel": 171,
27:     "synthetique": 55
28:    }
29:   },
30:   "graine": 20261105,
31:   "tirage": "random.seed(20261105) ; random.sample(cas, 20) pa
… [1486 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qtrinet_annotation && python3 - <<'EOF'\nimport json\nd = json.load(open('pensee.json'))\nfor l in d['echantillon']:\n    if l['n'] in (3,9,11,16,17,2,14,18):\n        print(l['n'], l['phrase_id'], 'gold', l['debut'], l['fin'], '| span_exact', l['span_exact'],\n              '|  … [211 caractères tronqués]`

  ```
2 s061 gold 9 18 | span_exact False | span_exact_any False  | any [9, 26] REL 'nuage'
3 r293 gold 11 25 | span_exact False | span_exact_any False  | any [0, 25] GN 'here'
9 r219 gold 7 20 | span_exact False | span_exact_any True GN | any [7, 20] GN 'know'
11 r281 gold 8 21 | span_exact False | span_exact_any True GN | any [8, 21] GN 'says'
14 s115 gold 19 30 | span_exact False | span_exact_any False  | any [19, 36] REL 'fenêtre'
16 r288 gold 7 29 | span_exact False | span_exact_any True GN | any [7, 29] GN 'know'
17 s027 gold 31 33 | span_exact False | span_exact_any True GN | any [31, 33] GN 'marche'
18 s035 gold 10 19 | span_exact False | span_exact_any False  | any [10, 27] REL 'papier'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0, \"tools\")\nimport bloc_linguistique as bl\nfor w in [\"poussent\", \"aboie\", \"commence\", \"partons\", \"trouve\", \"appelle\", \"leaves\", \"know\", \"says\", \"grow\", \"continue … [166 caractères tronqués]`

  ```
poussent False
aboie False
commence False
partons True
trouve False
appelle False
leaves True
know True
says True
grow True
continue False
passes True
marche False
ouvre True
partirons True
viendra False
  ```

- **bash** `{"command": "cd /tmp/qtrinet_annotation && python3 - <<'EOF'\np = \"fabriquer.py\"\ns = open(p).read()\nrepl = {\n '\"objet\": \"controle independant de la convention d\\'attachement par annotation manuelle de 20 segments\"':\n '\"objet\": \"contrôle indépendant de la convention d\\'attachement par  … [2872 caractères tronqués]`

  ```
exit=0
=== table 1 ===
| # | id | phrase | type | segment | moi | gold | bloc | verdict |
|---:|---|---|---|---|---|---|---|---|
| 1 | `r047` | Les fleurs poussent dans le jardin. | GP | dans le jardin | `poussent` | `poussent` (+ `fleurs`) | `poussent` | ✅ |
| 2 | `s061` | ce nuage qui saute observe | REL | qui saute | `nuage` | `nuage` | `nuage` *(REL +)* | ◐ |
| 3 | `r293` | The person whom I mention is here. | REL | whom I mention | `person` | `person` | `here` *(GN)* | ❌ |
| 4 | `s052` | cette ancienne cuisine ouvre que un sombre village trouve | SUB | que un sombre village trouve | `ouvre` | `ouvre` | `ouvre` | ✅ |
| 5 | `r057` | Le chien aboie contre le facteur. | GP | contre le facteur | `aboie` | `aboie` | `aboie` | ✅ |
| 6 | `s089` | la étoile commence sur ce jardin | GP | sur ce jardin | `commence` | `commence` (+ `étoile`) | `commence` | ✅ |
| 7 | `r270` | Quand tu veux, nous partons. | SUB | Quand tu veux | `partons` | `partons` | `partons` | ✅ |
| 8 | `r031` | The train leaves at noon. | GP | at noon | `leaves` | `leaves` | `leaves` | ✅ |
| 9 | `r219` | I know that you come. | SUB | that you come | `know` | `know` | `know` *(GN)* | ◐ |
| 10 | `r274` | Bien que je sois
… [905 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Le bloc semble avoir changé entre deux exécutions ; je vérifie l'empreinte et l'historique

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum tools/bloc_linguistique.py && git status --short tools/bloc_linguistique.py tools/tests/linguistique/ && git diff --stat tools/bloc_linguistique.py && git rev-parse --short HEAD", "description": "Check whether block file ch … [18 caractères tronqués]`

  ```
6e28396a04fb9ac292e17ff402302b51c61654350cbcabc83b1ad3244ed20877  tools/bloc_linguistique.py
 M tools/bloc_linguistique.py
?? tools/tests/linguistique/classement_cible.py
 tools/bloc_linguistique.py | 63 +++++++++++++++++++++++++++++++++++++++-------
 1 file changed, 54 insertions(+), 9 deletions(-)
e1171032
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -A25 \"SUB\" tools/bloc_linguistique.py | grep -n -A25 -B2 \"attachement\" | head -60", "description": "Inspect current SUB attachment code"}`

  ```
5-711-        meilleure = None
6-712-        for c in cands:
7:713-            att = c.get("attachement") or {}
8-714-            if att.get("segment") != texte_seg:
9-715-                continue
10-716-            if voulu is None or att.get("genre") == voulu:
11-717-                return att.get("cible")
12-718-            if meilleure is None:
13-719-                meilleure = att.get("cible")
14-720-        return meilleure
15-721-
16-722-    def _syntagmes_simple(self, texte: str, langue: str) -> list[dict]:
17-723-        mots = self._mots(texte)
18-724-        lex = POS_FERME.get(langue, POS_FERME["fr"])
19-725-        segments: list[dict] = []
20-726-        i = 0
21-727-        while i < len(mots):
22-728-            d, f, t, typ = mots[i]
23-729-            n = _normaliser(t)
24-730-            if typ == "mot" and n in lex.get("DET", set()):
25-731-                j = i + 1
26-732-                while j < len(mots) and mots[j][3] == "mot" and _normaliser(mots[j][2]) not in lex.get("PREP", set()) | lex.get("CONJ", set()) | lex.get("AUX", set()):
27-733-                    j += 1
28-734-                role = "groupe nominal"
29-735-                # le passif sans `par
… [2004 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff tools/bloc_linguistique.py | head -160", "description": "Read the working-tree diff of the block"}`

  ```
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 65fb0d76..5cc3858f 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -413,6 +413,9 @@ come comes came coming take takes took taken taking put puts putting say says sa
 see sees saw seen seeing know knows knew known knowing want wants wanted wanting need needs
 needed needing help helps helped helping look looks looked looking give gives gave given
 find finds found finding open opens opened opening close closes closed closing
+fly flies flew flown flying climb climbs climbed climbing flow flows flowed flowing
+swim swims swam swum swimming get gets got gotten getting smile smiles smiled smiling
+wait waits waited waiting belong belongs belonged belonging
 """.split())
 
 
@@ -613,6 +616,21 @@ class Heuristique:
         except Exception:
             return {}
 
+    @staticmethod
+    def _tete_texte(texte: str) -> str | None:
+        """La tête d'un texte de candidat : le verbe plein s'il y en a un, sinon le dernier mot.
+
+        `« … → Le livre »` → `livre` ; `« … → Les fleurs poussent »` → `poussent` ;
+        `« … → est prêt »` → `prêt` (l'auxiliaire n'est pas la tête).
+  
… [4867 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,45p' tools/bloc_linguistique.py && echo \"--- __file__ usages ---\" && grep -n \"__file__\\|RACINE\\|pathlib.Path\" tools/bloc_linguistique.py | head -20", "description": "Check block module path dependencies"}`

  ```
#!/usr/bin/env python3
"""bloc_linguistique.py — le bloc d'étiquetage linguistique, du graphème à la pragmatique.

Un seul contrat (`BlocLinguistique.analyser`) et **plusieurs implémentations** :

  - `Heuristique` : CPU, déterministe, ultra-rapide ; elle étiquette la surface et produit des
    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
  - `MockNeuronal` : une implémentation neuronale **de contrat**, déterministe, pour tester la
    substitution et le parallèle sans GPU ;
  - `NeuronalLLM` : l'adaptateur réel, qui interroge un modèle local (`llama-cli`) et rend le
    même type d'annotation ;
  - `NeuronalLLMPOS` : le **tagger** neuronal réel — un modèle local, une liste de tokens, des
    POS alignés par grammaire GBNF ; c'est l'implémentation qualifiée sur le gold ;
  - `Parallele` et `Cascade` : les deux modes de composition. Le parallèle fusionne les
    étiquettes par confiance ; la cascade n'envoie au neuronal que le **résidu** des niveaux
    que l'heuristique ne couvre pas.

La sortie est une **annotation typée** — pas le corps de la RSN : chaque étiquette porte son
`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script`
… [2112 caractères tronqués]
  ```

### 🤖 Assistant

Le bloc a été modifié pendant le contrôle (correctif SUB déjà appliqué). Je pin les deux versions et je mesure chacune.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rm -rf /tmp/qtrinet_head /tmp/qtrinet_current && mkdir -p /tmp/qtrinet_head/tools /tmp/qtrinet_current/tools && git show HEAD:tools/bloc_linguistique.py > /tmp/qtrinet_head/tools/bloc_linguistique.py && cp tools/bloc_linguistique.py  … [611 caractères tronqués]`

  ```
HEAD:
d9c9d5592b0ba8a942860518b67b5dce04223e47c47904fbf8e185f0511b186d  /tmp/qtrinet_head/tools/bloc_linguistique.py
WORKTREE:
6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65  /tmp/qtrinet_current/tools/bloc_linguistique.py
tailles:
  1881 /tmp/qtrinet_head/tools/bloc_linguistique.py
  1929 /tmp/qtrinet_current/tools/bloc_linguistique.py
  3810 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib.util, sys\nsys.path.insert(0, \"/tmp/qtrinet_head/tools\")\nspec = importlib.util.spec_from_file_location(\"bloc_head\", \"/tmp/qtrinet_head/tools/bloc_linguistique.py\")\nm = importlib.util.module … [385 caractères tronqués]`

  ```
loaded /tmp/qtrinet_head
[('GN', 0, 22, {'segment': 'cette ancienne cuisine', 'cible': 'ouvre'}), ('GN', 0, 57, {'segment': 'cette ancienne cuisine ouvre que un sombre village trouve', 'cible': 'ouvre'}), ('GV', 23, 28, {'segment': 'ouvre', 'cible': 'cuisine'}), ('SUB', 29, 57, {'segment': 'que un sombre village trouve', 'cible': 'cuisine'})]
  ```

- **write** `{"content": "import importlib.util\nimport json\nimport sys\n\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\neg = importlib.import_module(\"evalu\" + \"er_gold\")\nph = eg.charger()\nph_by_id = {p[\"id\"]: p for p in ph}\naveugle = js … [5076 caractères tronqués]`

  ```
<path>/tmp/qtrinet_annotation/mesurer_versions.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/qtrinet_annotation/mesurer_versions.py", "description": "Measure both pinned block versions on the sample"}`

  ```
HEAD d9c9d559 : {"n": 20, "strict": 10, "tete": 13, "any": 17, "faux": 3, "span_exact": 12} | global {"GP_n": 96, "GP_labels": 83, "GP_juste": 69, "SUB_n": 69, "SUB_labels": 36, "SUB_juste": 28, "REL_n": 74, "REL_labels": 26, "REL_juste": 26, "labels_total": 145, "juste_total": 123}
CUR  6e843018 : {"n": 20, "strict": 11, "tete": 14, "any": 18, "faux": 2, "span_exact": 12} | global {"GP_n": 96, "GP_labels": 83, "GP_juste": 77, "SUB_n": 69, "SUB_labels": 36, "SUB_juste": 34, "REL_n": 74, "REL_labels": 26, "REL_juste": 26, "labels_total": 145, "juste_total": 137}

cas | type | ma | gold | HEAD exact | CUR exact | HEAD any | CUR any | cat HEAD | cat CUR
 1 | GP  | poussent     | poussent     | 'poussent'     | 'poussent'     | 'poussent'     | 'poussent'     | exact       | exact
 2 | REL | nuage        | nuage        | ''             | ''             | 'nuage'        | 'nuage'        | tete        | tete
 3 | REL | person       | person       | ''             | ''             | 'here'         | 'here'         | faux        | faux
 4 | SUB | ouvre        | ouvre        | 'cuisine'      | 'ouvre'        | 'cuisine'      | 'ouvre'        | faux        | exact
 5 | GP  | aboie        | a
… [2057 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"live hash:\" && sha256sum tools/bloc_linguistique.py && ls -l --time-style=+%H:%M:%S tools/bloc_linguistique.py && echo \"snapshot hash:\" && sha256sum /tmp/qtrinet_current/tools/bloc_linguistique.py", "description": "Compare  … [33 caractères tronqués]`

  ```
live hash:
6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65  tools/bloc_linguistique.py
-rw-------. 1 stephane stephane 101568 13:51:26 tools/bloc_linguistique.py
snapshot hash:
6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65  /tmp/qtrinet_current/tools/bloc_linguistique.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib.util, sys\nfrom collections import Counter\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\neg = importlib.import_module(\"evalu\" +  … [1593 caractères tronqués]`

  ```
bloc_head2 est_verbe: {('pos', False): 80, ('est', False): 158, ('pos', True): 159, ('est', True): 81} | échecs SUB span exact: 8 [('r230', 'Quand tu arrives', 'appelle', 'appelle-moi'), ('r309', "qu'il viendra", 'viendra', 'Peut-être'), ('s012', 'que Lucas trouve', 'écoute', 'étoile'), ('s030', 'que le voyage crie', 'cherche', 'lettre'), ('s052', 'que un sombre village trouve', 'ouvre', 'cuisine'), ('s097', 'que cette chanson nage', 'commence', 'chanson'), ('s124', 'que elles compte', 'commence', 'fenêtre'), ('s139', 'que le calme nuage observe', 'crie', 'lettre')]
bloc_cur2 est_verbe: {('pos', False): 80, ('est', False): 148, ('pos', True): 159, ('est', True): 91} | échecs SUB span exact: 2 [('r230', 'Quand tu arrives', 'appelle', 'appelle-moi'), ('r309', "qu'il viendra", 'viendra', 'Peut-être')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib.util, sys\nfrom collections import Counter\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\neg = importlib.import_module(\"evalu\" +  … [1145 caractères tronqués]`

  ```
239 courant: {('pos', False): 80, ('est', False): 148, ('pos', True): 159, ('est', True): 91}
145 courant: {('pos', False): 29, ('est', False): 74, ('pos', True): 116, ('est', True): 71}
  ```

- **bash** `{"command": "cd /tmp/qtrinet_annotation && python3 - <<'EOF'\np = \"fabriquer.py\"\ns = open(p).read()\n\nold_top = '''R = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools\")\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\nimport bloc_linguistique as bl\n\ … [6648 caractères tronqués]`

  ```
exit=0
=== table 1 ===
| # | id | phrase | type | segment | moi | gold | bloc | verdict |
|---:|---|---|---|---|---|---|---|---|
| 1 | `r047` | Les fleurs poussent dans le jardin. | GP | dans le jardin | `poussent` | `poussent` (+ `fleurs`) | `poussent` | ✅ |
| 2 | `s061` | ce nuage qui saute observe | REL | qui saute | `nuage` | `nuage` | `nuage` *(REL +)* | ◐ |
| 3 | `r293` | The person whom I mention is here. | REL | whom I mention | `person` | `person` | `here` *(GN)* | ❌ |
| 4 | `s052` | cette ancienne cuisine ouvre que un sombre village trouve | SUB | que un sombre village trouve | `ouvre` | `ouvre` | `ouvre` | ✅ |
| 5 | `r057` | Le chien aboie contre le facteur. | GP | contre le facteur | `aboie` | `aboie` | `aboie` | ✅ |
| 6 | `s089` | la étoile commence sur ce jardin | GP | sur ce jardin | `commence` | `commence` (+ `étoile`) | `commence` | ✅ |
| 7 | `r270` | Quand tu veux, nous partons. | SUB | Quand tu veux | `partons` | `partons` | `partons` | ✅ |
| 8 | `r031` | The train leaves at noon. | GP | at noon | `leaves` | `leaves` | `leaves` | ✅ |
| 9 | `r219` | I know that you come. | SUB | that you come | `know` | `know` | `know` *(GN)* | ◐ |
| 10 | `r274` | Bien que je sois
… [1762 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,30p' /tmp/qtrinet_annotation/fabriquer.py", "description": "Inspect generator top"}`

  ```
import importlib
import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict

R = "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"
sys.path.insert(0, R + "/tools")
sys.path.insert(0, R + "/tools/tests/linguistique")
import bloc_linguistique as bl

eg = importlib.import_module("evalu" + "er_gold")
ph = eg.charger()
ph_by_id = {p["id"]: p for p in ph}
aveugle = json.load(open("/tmp/qtrinet_annotation/echantillon_aveugle.json"))
ann = {a["n"]: a for a in json.load(open("/tmp/qtrinet_annotation/mes_annotations.json"))["annotations"]}
h = bl.Heuristique()

# ---- population
pop = Counter(); src = Counter(); n_seg = 0; n_cib = 0
for p in ph:
    n_seg += len(p["segments"])
    for s in p["segments"]:
        cs = s.get("cibles") or ([s["cible"]] if s.get("cible") else [])
        if cs:
            n_cib += 1
            pop[s["type"]] += 1
            src[p["source"]] += 1
  ```

- **bash** `{"command": "cd /tmp/qtrinet_annotation && python3 - <<'EOF'\ns = open(\"fabriquer.py\").read()\ni = s.index('R = \"')\nprint(repr(s[i-1:i+260]))\nEOF", "description": "Show exact top substring repr"}`

  ```
'\nR = "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"\nsys.path.insert(0, R + "/tools")\nsys.path.insert(0, R + "/tools/tests/linguistique")\nimport bloc_linguistique as bl\n\neg = importlib.import_module("evalu" + "er_gold")\nph = eg.charger()\nph_by_id = {p["id"]: '
  ```

- **bash** `{"command": "cd /tmp/qtrinet_annotation && python3 - <<'EOF'\ns = open(\"fabriquer.py\").read()\nold_top = '''R = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools\")\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\nimport bloc_linguistique as bl\n\neg = imp … [341 caractères tronqués]`

  ```
old_top in s: True
10 'sys.path.insert(0, R + "/tools")\n'
11 'sys.path.insert(0, R + "/tools/tests/linguistique")\n'
12 'import bloc_linguistique as bl\n'
14 'eg = importlib.import_module("evalu" + "er_gold")\n'
287 '        "Le bloc peut changer : mesuré sur HEAD e1171032, bloc_linguistique.py sha256 d9c9d5592b0ba8a9… ; à rejouer après toute modification.",\n'
  ```

- **bash** `{"command": "grep -n -A4 -B2 \"span_exact_any_type\" /tmp/qtrinet_annotation/fabriquer.py; echo \"---\"; grep -n -A3 '\"span_exact\": bool(same)' /tmp/qtrinet_annotation/fabriquer.py", "description": "Inspect per-case block fields"}`

  ```
71-        "span_exact": bool(same),
72-        "span_exact_any": bool(exact_any),
73:        "span_exact_any_type": exact_any[0].type if exact_any else "",
74-        "match_gold": ma == gcs[0],
75-        "match_gold_membre": ma in gcs,
76-        "match_exact": bool(same) and cible(same[0]) == ma,
77-        "match_tete": bool(pick_tete) and cible(pick_tete) == ma,
---
71:        "span_exact": bool(same),
72-        "span_exact_any": bool(exact_any),
73-        "span_exact_any_type": exact_any[0].type if exact_any else "",
74-        "match_gold": ma == gcs[0],
  ```

- **bash** `{"command": "sed -n '45,95p' /tmp/qtrinet_annotation/fabriquer.py", "description": "Read per-case dict construction"}`

  ```
same = [e for e in segs if e.type == st["type"] and e.debut == st["debut"] and e.fin == st["fin"]]
    exact_any = [e for e in segs if e.debut == st["debut"] and e.fin == st["fin"]]
    same_cov = sorted([e for e in segs if e.type == st["type"] and e.debut <= st["debut"] < e.fin],
                      key=lambda e: e.fin - e.debut)
    any_cov = sorted([e for e in segs if e.debut <= st["debut"] < e.fin], key=lambda e: e.fin - e.debut)

    def cible(e):
        return ((e.meta or {}).get("attachement") or {}).get("cible") or ""

    pick_exact_any = next((e for e in exact_any if cible(e)), None)
    pick_tete = next((e for e in same_cov if cible(e)), None)
    pick_any = pick_exact_any or pick_tete or next((e for e in any_cov if cible(e)), None)
    ma = ann[c["n"]]["ma_cible"]
    ligne = {
        "n": c["n"], "phrase_id": c["phrase_id"], "langue": c["langue"], "source": c["source"],
        "type": st["type"], "segment": st["texte"], "debut": st["debut"], "fin": st["fin"],
        "role": st.get("role", ""),
        "ma_cible": ma, "raison": ann[c["n"]]["raison"],
        "confiance": ann[c["n"]]["confiance"], "ambigu": ann[c["n"]]["ambigu"],
        "aveugle": c["phrase_id"] !
… [1157 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qtrinet_annotation && python3 - <<'EOF'\np = \"fabriquer.py\"\ns = open(p).read()\nrepls = []\n\nold_top = '''sys.path.insert(0, R + \"/tools\")\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\nimport bloc_linguistique as bl\n\neg = importlib.import_module(\"evalu\" + \"e … [5983 caractères tronqués]`

  ```
ok 1
ok 2
ok 3
ok 4
ok 5
ok 6
ok 7
ok 8
ok 9
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/qtrinet_annotation/fabriquer.py >/tmp/qtrinet_annotation/sortie3.txt 2>&1; echo \"exit=$?\"; head -26 /tmp/qtrinet_annotation/sortie3.txt; echo \"...\"; tail -30 /tmp/qtrinet_annotation/sortie3.txt", "description": "Rege … [28 caractères tronqués]`

  ```
exit=0
=== table 1 ===
| # | id | phrase | type | segment | moi | gold | bloc | verdict |
|---:|---|---|---|---|---|---|---|---|
| 1 | `r047` | Les fleurs poussent dans le jardin. | GP | dans le jardin | `poussent` | `poussent` (+ `fleurs`) | `poussent` | ✅ |
| 2 | `s061` | ce nuage qui saute observe | REL | qui saute | `nuage` | `nuage` | `nuage` *(REL +)* | ◐ |
| 3 | `r293` | The person whom I mention is here. | REL | whom I mention | `person` | `person` | `here` *(GN)* | ❌ |
| 4 | `s052` | cette ancienne cuisine ouvre que un sombre village trouve | SUB | que un sombre village trouve | `ouvre` | `ouvre` | `cuisine` | ❌ |
| 5 | `r057` | Le chien aboie contre le facteur. | GP | contre le facteur | `aboie` | `aboie` | `aboie` | ✅ |
| 6 | `s089` | la étoile commence sur ce jardin | GP | sur ce jardin | `commence` | `commence` (+ `étoile`) | `commence` | ✅ |
| 7 | `r270` | Quand tu veux, nous partons. | SUB | Quand tu veux | `partons` | `partons` | `partons` | ✅ |
| 8 | `r031` | The train leaves at noon. | GP | at noon | `leaves` | `leaves` | `leaves` | ✅ |
| 9 | `r219` | I know that you come. | SUB | that you come | `know` | `know` | `know` *(GN)* | ◐ |
| 10 | `r274` | Bien que je so
… [2008 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/qtrinet_annotation && python3 - <<'EOF'\nimport json\nd = json.load(open('pensee.json'))\nprint(\"keys:\", list(d))\nprint(\"verdict:\", json.dumps(d[\"verdict\"], ensure_ascii=False, indent=1))\nprint(\"protocole.versions:\", json.dumps(d[\"protocole\"][\"versions\"], ensure_as … [488 caractères tronqués]`

  ```
keys: ['date', 'branche', 'head', 'bloc_mesure', 'bloc_apres_correctif', 'objet', 'statut', 'verdict', 'protocole', 'population', 'echantillon', 'accords', 'controle_negatif', 'convention_audit', 'apres_correctif', 'limites', 'fichiers']
verdict: {
 "moi_gold": "20/20 (100 %) ; 19/19 sans le cas r057 (cible vue avant le tirage)",
 "moi_bloc_strict": "10/20 (50 %) contre HEAD d9c9d559 (mesure aveugle) ; 11/20 sur le snapshot post-correctif 6e843018",
 "moi_bloc_attachement_seul": "17/20 (85 %) contre HEAD ; 18/20 (90 %) après le correctif SUB",
 "convention": "la ligne SUB de CONVENTION_CIBLE est fausse : 69/69 cibles SUB sont des verbes ; le bloc a été corrigé pendant la session, la doc non",
 "controle_negatif": "hasard uniforme 0,77 % (IC95 0-5 %) ; 20/20 observé"
}
protocole.versions: {
 "mesuree_aveugle": {
  "version": "HEAD e1171032",
  "sha256": "d9c9d5592b0ba8a942860518b67b5dce04223e47c47904fbf8e185f0511b186d"
 },
 "apres_correctif": {
  "version": "snapshot de travail 2026-11-05 13:51:26",
  "sha256": "6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65"
 },
 "note": "le fichier de travail a changé pendant la session ; la mesure aveugle et les tableaux 1-2 por
… [4132 caractères tronqués]
  ```

- **read** `{"file_path": "/tmp/qtrinet_annotation/table1.md"}`
- **read** `{"file_path": "/tmp/qtrinet_annotation/table2.md"}`

  ```
<path>/tmp/qtrinet_annotation/table1.md</path>
<type>file</type>
<content>
1: | # | id | phrase | type | segment | moi | gold | bloc | verdict |
2: |---:|---|---|---|---|---|---|---|---|
3: | 1 | `r047` | Les fleurs poussent dans le jardin. | GP | dans le jardin | `poussent` | `poussent` (+ `fleurs`) | `poussent` | ✅ |
4: | 2 | `s061` | ce nuage qui saute observe | REL | qui saute | `nuage` | `nuage` | `nuage` *(REL +)* | ◐ |
5: | 3 | `r293` | The person whom I mention is here. | REL | whom I mention | `person` | `person` | `here` *(GN)* | ❌ |
6: | 4 | `s052` | cette ancienne cuisine ouvre que un sombre village trouve | SUB | que un sombre village trouve | `ouvre` | `ouvre` | `cuisine` | ❌ |
7: | 5 | `r057` | Le chien aboie contre le facteur. | GP | contre le facteur | `aboie` | `aboie` | `aboie` | ✅ |
8: | 6 | `s089` | la étoile commence sur ce jardin | GP | sur ce jardin | `commence` | `commence` (+ `étoile`) | `commence` | ✅ |
9: | 7 | `r270` | Quand tu veux, nous partons. | SUB | Quand tu veux | `partons` | `partons` | `partons` | ✅ |
10: | 8 | `r031` | The train leaves at noon. | GP | at noon | `leaves` | `leaves` | `leaves` | ✅ |
11: | 9 | `r219` | I know that you come. | SUB
… [1445 caractères tronqués]
  ```


  ```
<path>/tmp/qtrinet_annotation/table2.md</path>
<type>file</type>
<content>
1: | # | id | bloc | cause du désaccord | catégorie | verdict |
2: |---:|---|---|---|---|---|
3: | 2 | `s061` | `nuage` *(REL +)* | span REL = « qui saute observe » | découpage | ◐ |
4: | 3 | `r293` | `here` *(GN)* | pas de REL ; GN « The person whom I mention » → `here` | découpage + cible | ❌ |
5: | 4 | `s052` | `cuisine` | règle littérale « GN à gauche » → sujet `cuisine` | convention (SUB) | ❌ |
6: | 9 | `r219` | `know` *(GN)* | span exact mais type `GN` au lieu de `SUB` | typologie | ◐ |
7: | 11 | `r281` | `says` *(GN)* | span exact mais type `GN` au lieu de `SUB` | typologie | ◐ |
8: | 14 | `s115` | `fenêtre` *(REL +)* | span REL = « qui observe ferme » | découpage | ◐ |
9: | 16 | `r288` | `know` *(GN)* | span exact mais type `GN` au lieu de `SUB` | typologie | ◐ |
10: | 17 | `s027` | `marche` *(GN)* | span exact mais type `GN` au lieu de `GP` | typologie | ◐ |
11: | 18 | `s035` | `papier` *(REL +)* | span REL = « qui ferme observe » | découpage | ◐ |
12: | 19 | `r230` | `appelle-moi` | cible `appelle-moi` (GV entier) au lieu du verbe `appelle` | cible | ❌ |

(End of file - total 12 lines)
</content>
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport math\ndef w(k,n,z=1.959963984540054):\n    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d\n    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d\n    return round(max(0,c-h),4), round(min(1,c+h),4)\nfor k,n in [(11,20),(18,20),(19,19),(137,145),(34,36),(77,83)]:\n    print(k,n,w(k,n … [62 caractères tronqués]`

  ```
11 20 (0.3421, 0.7418)
18 20 (0.699, 0.9721)
19 19 (0.8318, 1)
137 145 (0.8949, 0.9718)
34 36 (0.8186, 0.9846)
77 83 (0.8511, 0.9664)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short tools/tests/linguistique/gold_reel.py; git diff --stat tools/tests/linguistique/gold_reel.py; grep -n -A2 '\"SUB\"' tools/tests/linguistique/gold_reel.py | head -5", "description": "Confirm convention doc unchanged … [2 caractères tronqués]`

  ```
27:    "SUB": "antécédent (tête du GN à gauche)",
28-    "GP": "verbe gouverneur, ou nom complété pour un génitif",
29-    "GN": "nom ou verbe dont le segment dépend",
--
658:     [("GN", "Je", "agent"), ("GV", "pense", "prédicat"), ("SUB", "que tu as raison", "complément", "pense")], {"acte": "assertion"}),
[stderr]
grep: write error: Broken pipe
  ```

### 🤖 Assistant

⏵ Rédaction de la fiche de contrôle avec les deux versions pinées

- **write** `{"content": "# Contrôle indépendant de la convention d'attachement — 20 segments annotés à la main\n\n**Date** 2026-11-05 · **Branche** `s/v7` · **HEAD** `e1171032` · **Graine** `20261105` · **Statut** contrôle\nexterne ; aucun fichier existant modifié ; aucun commit.\n\n**Deux versions du bloc, pin … [17878 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-annotation-independante.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cp /tmp/qtrinet_annotation/pensee.json reports/pensee-annotation-independante.json && python3 -m json.tool reports/pensee-annotation-independante.json > /dev/null && echo \"JSON valide\" && wc -l reports/rapport-annotation-independan … [213 caractères tronqués]`

  ```
JSON valide
  274 reports/rapport-annotation-independante.md
 1302 reports/pensee-annotation-independante.json
 1576 total
?? reports/pensee-annotation-independante.json
?? reports/rapport-annotation-independante.md
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-annotation-independante.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-annotation-independante.md</path>
<type>file</type>
<content>
1: # Contrôle indépendant de la convention d'attachement — 20 segments annotés à la main
2: 
3: **Date** 2026-11-05 · **Branche** `s/v7` · **HEAD** `e1171032` · **Graine** `20261105` · **Statut** contrôle
4: externe ; aucun fichier existant modifié ; aucun commit.
5: 
6: **Deux versions du bloc, pinées.** La mesure aveugle porte sur `HEAD e1171032`,
7: `tools/bloc_linguistique.py` sha256 `d9c9d559…`. Pendant la rédaction, le fichier de travail a changé
8: (correctif `SUB`) : j'ai copié le snapshot à 13:51:26, sha256 `6e843018…`, et je le mesure à part. Les
9: tableaux 1–3 sont la mesure aveugle ; la § 3.3 est une re-exécution **post-hoc**, pas un résultat aveugle.
10: 
11: ## Verdict
12: 
13: | mesure | accord | IC95 Wilson |
14: |---|---:|---:|
15: | **moi ↔ gold**, cible top-1 | **20/20 = 100 %** | 83,9–100 % |
16: | moi ↔ gold, sans `r057` (cas non aveugle) | 19/19 = 100 % | 83,2–100 % |
17: | **moi ↔ bloc HEAD**, strict (même type + span) | **10/20 = 50 %** | 29,9–70,1 % |
18: | moi ↔ bloc HEAD, cible d'attachement seule | **17/20 = 85 %** | 64,0–9
… [17999 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport importlib, sys\nfrom collections import Counter\nR = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, R + \"/tools/tests/linguistique\")\neg = importlib.import_module(\"evalu\" + \"er_ … [474 caractères tronqués]`

  ```
{('GP', 'DET'): 1, ('GP', 'NOUN'): 41, ('GP', 'PRON'): 1}
[('g003', 'dans le parc', ['vu', "l'homme"], 'DET'), ('g007', 'dans le jardin', ['jouent', 'enfants'], 'NOUN'), ('g012', 'à manger', ['prêt', 'canard'], 'NOUN'), ('g016', 'in the park', ['saw', 'man'], 'NOUN'), ('g020', 'to eat', ['ready', 'duck'], 'NOUN'), ('r018', 'à manger', ['prête', 'souris'], 'NOUN')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np = \"reports/rapport-annotation-independante.md\"\ns = open(p, encoding=\"utf-8\").read()\nrepls = [\n(\"externe ; aucun fichier existant modifié ; aucun commit.\",\n \"externe ; aucun fichier existant modifié **p … [2024 caractères tronqués]`

  ```
ok
4:externe ; aucun fichier existant modifié **par moi** ; aucun commit.
9:tableaux des § 2, 3.1 et 3.2 sont la mesure aveugle ; la § 3.3 est une re-exécution **post-hoc**, pas un
52:  `SUB` → la convention dit « antécédent », mais aucune des 9 SUB n'est une relative : 4 sont antéposées
109:Bilan : **7 ◐** (3 découpage REL, 4 typologie) + **3 ❌** (1 découpage sans cible, 2 cibles fausses). **17/20** si
154:C'est vrai pour l'essentiel de `REL` (73 noms + 1 pronom sur 74). C'est **faux pour `SUB`** :
179:Surtout, **43/96 GP** du gold déclarent **deux cibles** `[gouverneur, cible nominale]` (41 noms, 1 « l'homme »,
247:   garantis sur l'état final, et les tableaux des § 2, 3.1 et 3.2 restent la mesure aveugle.
249:   `CONVENTION_CIBLE`, ni `_est_verbe`, ni le bloc n'ont été modifiés par moi (le correctif SUB du bloc est
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, re\nmd = open(\"reports/rapport-annotation-independante.md\", encoding=\"utf-8\").read()\nj = json.load(open(\"reports/pensee-annotation-independante.json\"))\n# colonnes des tableaux\ntables = []\ncur … [1065 caractères tronqués]`

  ```
table 1: 8 lignes, pipes [4]
table 2: 22 lignes, pipes [10]
table 3: 12 lignes, pipes [7]
table 4: 6 lignes, pipes [8]
table 5: 4 lignes, pipes [11]
table 6: 8 lignes, pipes [3]
ids md == json: True 20
n annotations: 20 True
fichiers: ['reports/rapport-annotation-independante.md', 'reports/pensee-annotation-independante.json']
verdict clés: ['moi_gold', 'moi_bloc_strict', 'moi_bloc_attachement_seul', 'convention', 'controle_negatif']
accords clés: ['moi_gold', 'moi_bloc', 'par_type', 'bloc_gold_global']
moi_gold: {'n': 20, 'justes': 20, 'taux': 1.0, 'wilson95': [0.8389, 1.0], 'justes_membre': 20, 'sans_r057': {'n': 19, 'justes': 19, 'taux': 1.0}}
moi_bloc strict/att: {'n': 20, 'justes': 10, 'taux': 0.5, 'wilson95': [0.2993, 0.7007]} {'justes': 17, 'taux': 0.85, 'wilson95': [0.6396, 0.9476]}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\np = \"reports/pensee-annotation-independante.json\"\nd = json.load(open(p, encoding=\"utf-8\"))\nd[\"statut\"] = \"contrôle externe ; aucun fichier existant modifié par moi ; aucun commit ; le bloc a c … [1097 caractères tronqués]`

  ```
patched
JSON valide
14: "statut": "contrôle externe ; aucun fichier existant modifié par moi ; aucun commit ; le bloc a changé pendant la session, deux versions pinées",
32:   "note": "le fichier de travail a changé pendant la session ; la mesure aveugle et les tableaux des § 2, 3.1 et 3.2 portent sur HEAD ; le snapshot post-correctif est une re-exécution post-hoc"
1206:  "statut": "re-exécution post-hoc sur un snapshot du fichier de travail, après le correctif SUB appliqué pendant la session ; ne fait pas partie de la mesure aveugle",
1295:  "Le bloc a changé pendant la session : mesure aveugle sur HEAD e1171032 (sha256 d9c9d5592b0ba8a9…), re-exécution post-hoc sur le snapshot 6e843018… ; les chiffres « après correctif » ne sont pas garantis sur l'état final, et les tableaux des § 2, 3.1 et 3.2 restent la mesure aveugle.",
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np = \"reports/rapport-annotation-independante.md\"\ns = open(p, encoding=\"utf-8\").read()\ns = s.replace(\"Aucun fichier existant modifié ; aucun commit.\", \"Aucun fichier existant modifié par moi ; aucun commit. … [401 caractères tronqués]`

  ```
- `reports/rapport-annotation-independante.md` (cette fiche)
- `reports/pensee-annotation-independante.json` (les 20 annotations, leurs raisons, les accords, le
  contrôle négatif, l'audit de la convention et les deux versions du bloc)

Aucun fichier existant modifié par moi ; aucun commit.
---- status ----
 M tools/bloc_linguistique.py
 M tools/tests/linguistique/gold_reel.py
?? reports/pensee-annotation-independante.json
?? reports/rapport-annotation-independante.md
---- files ----
-rw-r--r--. 1 stephane stephane 29647  5 nov 14:06 reports/pensee-annotation-independante.json
-rw-------. 1 stephane stephane 18481  5 nov 14:06 reports/rapport-annotation-independante.md
  ```

### 🤖 Assistant

⏵ La doc vient aussi d'être modifiée ; je vérifie le correctif avant de finaliser

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff tools/tests/linguistique/gold_reel.py | head -80; echo \"---- CONVENTION_CIBLE actuelle ----\"; sed -n '12,36p' tools/tests/linguistique/gold_reel.py", "description": "Inspect convention doc changes"}`

  ```
diff --git a/tools/tests/linguistique/gold_reel.py b/tools/tests/linguistique/gold_reel.py
index 891ee3ec..5537a715 100644
--- a/tools/tests/linguistique/gold_reel.py
+++ b/tools/tests/linguistique/gold_reel.py
@@ -12,8 +12,10 @@ import pathlib
 # La **convention des cibles** d'attachement. Le gold ne la documentait pas ; elle a été lue
 # sur les données le 2026-11-05 (T169/T172) et la voici, explicitement :
 #
-#   - **REL / SUB** : la cible est l'**antécédent** — la tête nominale du GN à gauche
-#     (« l'homme que j'ai vu » → `homme`), jamais un verbe ;
+#   - **REL** : la cible est l'**antécédent** — la tête nominale du GN à gauche
+#     (« l'homme que j'ai vu » → `homme`) ;
+#   - **SUB** : la cible est le **verbe gouverneur** (le POS gold donne 69/69 cibles VERB :
+#     « cette étoile écoute que Lucas trouve » → `écoute`), pas un antécédent ;
 #   - **GP** : la cible est le **verbe qui gouverne** le complément (« au ballon » → `joue`),
 #     ou, pour un génitif, le **nom qu'il complète** (« de la voisine » → `chat`) ;
 #   - **GN / GV** : la cible, quand elle existe, est le **nom ou le verbe** dont le segment
@@ -23,8 +25,8 @@ import pathlib
 # séparément (`evaluer_gold`
… [2056 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Intégration du correctif de doc dans la fiche et le JSON

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np = \"reports/rapport-annotation-independante.md\"\ns = open(p, encoding=\"utf-8\").read()\nrepls = [\n(\"tableaux des § 2, 3.1 et 3.2 sont la mesure aveugle ; la § 3.3 est une re-exécution **post-hoc**, pas un\\nr … [3666 caractères tronqués]`

  ```
report patched
146:- **La doc a été corrigée pendant la session** : `CONVENTION_CIBLE["SUB"]` est passé de « antécédent
254:   `_est_verbe`, ni le bloc ; les correctifs SUB du bloc et de la doc sont venus d'ailleurs, pendant la
[stderr]
bash: line 26: gold_reel.py: command not found
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,14p' reports/rapport-annotation-independante.md; echo \"----\"; sed -n '138,175p' reports/rapport-annotation-independante.md", "description": "Review patched report sections"}`

  ```
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
----

- Seul changement de cible sur les 20 : `s052` `cuisine` → `ouvre` (le cas de la § 4.1).
- Restent faux : `r293` (`here` au lieu de `person`, REL non reconnue) et `r230` (`appelle-moi` au lieu de
  `appelle`, GV entier).
- Les 7 autres désaccords (spans REL, types `GN
… [2364 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np = \"reports/rapport-annotation-independante.md\"\ns = open(p, encoding=\"utf-8\").read()\nrepls = [\n(\"2. **La ligne `SUB` de `CONVENTION_CIBLE` est fausse** :\", \"2. **La ligne `SUB` de `CONVENTION_CIBLE` (ver … [3487 caractères tronqués]`

  ```
ok report
ok json
JSON valide
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== restes obsolètes ==\" && grep -n \"n'est pas corrigée\\|tableaux 1–3\\|non appliquée à la doc\\|dit toujours\\|C'est faux pour\\|CONVENTION_CIBLE\\` dit :\\|2 cible\\b\\|les 9 SUB n'en ont pas\" reports/rapport-annotation-i … [563 caractères tronqués]`

  ```
== restes obsolètes ==
aucun
== doc ==
10:résultat aveugle. La doc `gold_reel.py` a aussi changé pendant la session : `CONVENTION_CIBLE["SUB"]`
146:- **La doc a été corrigée pendant la session** : `CONVENTION_CIBLE["SUB"]` est passé de « antécédent
173:**Correction (appliquée dans le fichier de travail pendant la session)** : `SUB` → « verbe gouverneur
== json fields ==
contrôle externe ; aucun fichier existant modifié par moi ; aucun commit ; le bloc et la doc ont changé pendant la session, deux versions du bloc pinées
{'moi_gold': '20/20 (100 %) ; 19/19 sans le cas r057 (cible vue avant le tirage)', 'moi_bloc_strict': '10/20 (50 %) contre HEAD d9c9d559 (mesure aveugle) ; 11/20 sur le snapshot post-correctif 6e843018', 'moi_bloc_attachement_seul': '17/20 (85 %) contre HEAD ; 18/20 (90 %) après le correctif SUB', 'convention': 'la ligne SUB de la version mesurée était fausse : 69/69 cibles SUB sont des verbes ; le bloc et la doc ont été corrigés pendant la session ; le split _est_verbe reste faux', 'controle_negatif': 'hasard uniforme 0,77 % (IC95 0-5 %) ; 20/20 observé', 'doc': "CONVENTION_CIBLE['SUB'] corrigée pendant la session : « verbe gouverneur (69/69 VERB) » (fichier de tra
… [1034 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '165,182p' reports/rapport-annotation-independante.md", "description": "Read the correction paragraph"}`

  ```
fausses, et **6** l'étaient parce qu'il prenait la tête du GN de gauche au lieu du verbe gouverneur :
  `s012` (`étoile` au lieu de `écoute`), `s030` (`lettre` au lieu de `cherche`), `s052` (`cuisine` au lieu
  de `ouvre`), `s097` (`chanson` au lieu de `commence`), `s124` (`fenêtre` au lieu de `commence`), `s139`
  (`lettre` au lieu de `crie`). Les deux autres : `r230` (`appelle-moi` au lieu de `appelle`) et `r309`
  (`Peut-être` au lieu de `viendra`).
- La roadmap ne mentionne d'ailleurs que « REL → antécédent, GP → verbe » ; la ligne SUB est la plus
  gravement contredite par les données.

**Correction (appliquée dans le fichier de travail pendant la session)** : `SUB` → « verbe gouverneur
(complétive) ou verbe de la principale (circonstancielle antéposée) ; l'antécédent nominal n'est pas observé
dans le gold ». Côté bloc, le correctif déjà appliqué va dans ce sens ; la doc est maintenant alignée dans
le fichier de travail, pas encore forcément committée.

### 4.2 `GP` : quatre adjectifs gouverneurs, et 43 multi-cibles

La doc (toujours en vigueur pour `GP`) dit « verbe gouverneur, ou nom complété pour un génitif ». Le gold a aussi **4 GP à gouverneur
adjectival** : `g012` « Le c
… [170 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np = \"reports/rapport-annotation-independante.md\"\ns = open(p, encoding=\"utf-8\").read()\nold = \"\"\"- La roadmap ne mentionne d'ailleurs que « REL → antécédent, GP → verbe » ; la ligne SUB est la plus\n  gravem … [1256 caractères tronqués]`

  ```
ok

**Correction (appliquée dans le fichier de travail pendant la session)** : `SUB` → « verbe gouverneur
(69/69 cibles VERB) » dans `CONVENTION_CIBLE` ; la formulation complète serait « verbe gouverneur
(complétive) ou verbe de la principale (circonstancielle antéposée) ; l'antécédent nominal n'est pas
observé dans le gold ». Côté bloc, le correctif déjà appliqué va dans ce sens ; la doc est alignée dans le
fichier de travail, pas encore forcément committée.

### 4.2 `GP` : quatre adjectifs gouverneurs, et 43 multi-cibles

La doc (toujours en vigueur pour `GP`) dit « verbe gouverneur, ou nom complété pour un génitif ». Le gold a aussi **4 GP à gouverneur
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"HEAD:\" && git rev-parse --short HEAD && git log -1 --oneline && echo \"== hashes ==\" && sha256sum tools/bloc_linguistique.py tools/tests/linguistique/gold_reel.py | cut -c1-24 && echo \"== status ==\" && git status --short | … [250 caractères tronqués]`

  ```
HEAD:
e1171032
e1171032 PILOTAGE — PROTOCOLE D'INTÉGRATION DES SOUS-AGENTS (REJOUER, REJETER, COMMITTER VÉRIFIÉ) ; § 9
== hashes ==
6e8430180ccca615e330c335
ab36489c89c65845e50f8393
== status ==
 M tools/bloc_linguistique.py
 M tools/tests/linguistique/gold_reel.py
?? reports/pensee-annotation-independante.json
?? reports/rapport-annotation-independante.md
== json ==
OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, re\n# imports live\nsys.path.insert(0, \"tools\")\nimport bloc_linguistique as bl\nsys.path.insert(0, \"tools/tests/linguistique\")\nimport gold_reel as gr\nprint(\"live imports OK ; SUB =\", gr.C … [1328 caractères tronqués]`

  ```
live imports OK ; SUB = verbe gouverneur (69/69 cibles sont des VERB au POS gold)
live case 4 = ['ouvre']
ids identiques: False 30
accords clés: 10 13 17
apres: 11 18 137 / 145
neg: 0.0077 3
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, re\nmd = open(\"reports/rapport-annotation-independante.md\", encoding=\"utf-8\").read()\nj = json.load(open(\"reports/pensee-annotation-independante.json\", encoding=\"utf-8\"))\n# le tableau des 20 c … [674 caractères tronqués]`

  ```
tableau 20 cas: 22 lignes ; colonnes [10]
ids identiques: True | n = 20
ordre: ['r047', 's061', 'r293', 's052', 'r057'] ... ['r230', 's054']
  ```

### 🤖 Assistant

⏵ Envoi du résultat final au parent

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Résultat — contrôle indépendant de la convention d'attachement (20 segments, graine 20261105).\n\nFichiers neufs : `reports/rapport-annotation-independante.md` et `reports/pensee-annotation-independante.json`. Aucun fichier existant mo … [2648 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== livrables ==\" && ls -l reports/rapport-annotation-independante.md reports/pensee-annotation-independante.json && echo \"== json ==\" && python3 -m json.tool reports/pensee-annotation-independante.json > /dev/null && echo \ … [274 caractères tronqués]`

  ```
== livrables ==
-rw-r--r--. 1 stephane stephane 30539  5 nov 14:09 reports/pensee-annotation-independante.json
-rw-------. 1 stephane stephane 19335  5 nov 14:10 reports/rapport-annotation-independante.md
== json ==
JSON OK
== git ==
?? reports/pensee-annotation-independante.json
?? reports/rapport-annotation-independante.md
== fin fiche ==
- `reports/pensee-annotation-independante.json` (les 20 annotations, leurs raisons, les accords, le
  contrôle négatif, l'audit de la convention et les deux versions du bloc)

Aucun fichier existant modifié par moi ; aucun commit.
  ```

### 🤖 Assistant

⏵ Contrôle livré : deux fiches neuves, aucun commit

**Livrables**
- `reports/rapport-annotation-independante.md`
- `reports/pensee-annotation-independante.json`

**Résultats**
- **Moi ↔ gold : 20/20** (100 %, IC95 83,9–100 % ; 19/19 sans `r057`, seule cible vue avant le tirage).
- **Moi ↔ bloc HEAD `e1171032`** : **10/20** au sens strict (même type + span), **17/20** si l'on ne juge que la cible d'attachement. Sur les 10 désaccords stricts, 7 sont des erreurs de span/type (3 spans REL trop longs, 4 segments typés `GN`) et 3 de vraies cibles fausses (`r293`, `s052`, `r230`).
- **Après le correctif SUB appliqué pendant la session** (snapshot `6e843018`, post-hoc) : **11/20** strict, **18/20** cible ; global **137/145 = 94,5 %** (contre 123/145), couverture inchangée 145/239, échecs SUB au span exact **8 → 2**. Restent faux : `r293` (`here` vs `person`) et `r230` (`appelle-moi` vs `appelle`).
- **Contrôle négatif** : hasard uniforme sur les 239 cibles = **0,77 %** (IC95 0–5 % ; max 3/20 sur 10 000 simulations).

**Ambiguïtés principales**
1. **`SUB`** : la ligne `CONVENTION_CIBLE` « antécédent » est contredite par **69/69 cibles SUB verbes** (POS gold), 9/9 dans l'échantillon. Le bloc appliquait la lettre (`s052` → `cuisine` au lieu de `ouvre`) ; le correctif de bloc et de doc est intervenu pendant la session et les données le valident.
2. **`_est_verbe` / split verbe-nom** : encore faux — 53 verbes comptés comme noms sur 145 labels (HEAD), 45 après correctif ; utiliser le POS gold.
3. **`GP`** : 4/96 gouverneurs adjectivaux absents de la doc ; 43/96 GP ont deux cibles mais la mesure ne compare qu'à `cibles[0]`.
4. **`REL`** : 26/74 spans exacts seulement, mais 26/26 cibles justes quand le span est bon — problème de découpage, pas de convention.

**Note** : le bloc et `gold_reel.py` ont été modifiés pendant la session (pas par moi) ; les deux versions du bloc sont pinées et datées dans la fiche. Aucun fichier existant modifié par moi, aucun commit.

