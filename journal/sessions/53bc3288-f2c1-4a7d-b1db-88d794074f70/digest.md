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

