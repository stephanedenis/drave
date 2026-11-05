# Session DSH — relecture

- identifiant : `7263ca42-cd56-4c36-a6dd-8ff2d1024a43`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 14:22:47
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **qualifier et chiffrer les 8 échecs restants** de l'attachement (état v2 du 2026-11-05).

Contexte : `tools/bloc_linguistique.py` (`Heuristique`), `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bloc`). Sur les 145 segments gold dont le span est prédit, l'exact (égalité stricte avec la cible) vaut 137 ; les 8 échecs se répartissent en 3 « hors candidats » et 5 « mal classés » (voir `reports/rapport-pensee-attachement-v2.md` et `reports/pensee-attachement-v2.json`).

À faire :
1. Liste les 8 segments (id de phrase, type, texte, cible du gold, cible choisie, candidats, source hand/reel/synthétique) et qualifie chacun : cible absente des candidats / présente mais mal choisie / cible vide / tokenisation / autre.
2. Pour chacun, dis si une **règle déterministe** le réparerait, laquelle, sur combien d'autres segments elle s'appliquerait, et le gain **attendu** (nombre de segments) — sans modifier le code.
3. Vérifie les deux cas déjà connus : `r230` (« appelle-moi » vs « appelle ») et le cas de la complétive en tête (`r309`, « Peut-être qu'il viendra »).
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-echecs-v2.md` (fiche : tableau des 8, règles candidates chiffrées, contrôles négatifs, limites) et `reports/pensee-echecs-v2.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé avec les 8 qualifications et les règles candidates chiffrées.
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

⏵ Exploration du dépôt et des rapports d'attachement v2

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -20 && echo \"---BRANCH---\" && git branch --show-current && echo \"---LS reports---\" && ls -la reports/ | grep -i attachement", "description": "Check git state and reports listing"}`

  ```
M docs/pilotage/en-cours.md
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
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/digest.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/rapport.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/digest.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/rapport.md
---BRANCH---
s/v7
---LS reports---
-rw-r--r--. 1 stephane stephane     655  5 nov 10:13 pensee-attachement-cible.json
-rw-r--r--. 1 stephane stephane     318  4 nov 13:50 pensee-attachement.json
-rw-r--r--. 1 stephane stephane    1371  5 nov 14:11 pensee-attachement-v2.json
-rw-r--r--. 1 stephan
… [575 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py 2>&1", "description": "Check key files exist"}`

  ```
-rw-------. 1 stephane stephane 101568  5 nov 13:51 tools/bloc_linguistique.py
-rw-r--r--. 1 stephane stephane  14489  5 nov 13:51 tools/tests/linguistique/evaluer_gold.py
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-v2.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-attachement-v2.json"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-v2.md</path>
<type>file</type>
<content>
1: # B13 — l'attachement v2 : exact 0,8483 → 0,9448, top-k strict 0,6069 → 0,9724
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **180/180 portes** : trois corrections **mesurées**, issues de trois sous-agents indépendants :
5: > (1) la règle du **segment précédent** (un SUB après un GV est une complétive → cible = le verbe ;
6: > après un GN, une relative → cible = l'antécédent), (2) les **têtes des candidats** de S
7: > (« « … » → Le livre » → `livre`), (3) le **lexique verbal anglais** complété. Sur les 145
8: > segments au bon span : **exact 123 → 137 (0,9448)**, top1 **126 → 140 (0,9655)**, top-k
9: > **134 → 142 (0,9793)**, **top-k strict 88 → 141 (0,9724)**.
10: >
11: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
12: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
13: > [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) (`CONVENTION_CIBLE`),
14: > [`autotest.py`](../tools/pensee/autotest.py) ; fiches des sous-agents :
15: >
… [4730 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-attachement-v2.json</path>
<type>file</type>
<content>
1: {
2:  "date": "2026-11-05",
3:  "ligne": "B13",
4:  "portes": "180/180",
5:  "labels": 145,
6:  "cibles": 239,
7:  "avant": {
8:   "exact": 123,
9:   "exact_span": 0.8483,
10:   "top1": 126,
11:   "topk": 134,
12:   "topk_exact": 88,
13:   "verbe_est": 0.9524,
14:   "nom_est": 0.7683
15:  },
16:  "apres": {
17:   "exact": 137,
18:   "exact_span": 0.9448,
19:   "top1": 140,
20:   "topk": 142,
21:   "topk_exact": 141,
22:   "top1_span": 0.9655,
23:   "topk_span": 0.9793,
24:   "topk_exact_span": 0.9724,
25:   "verbe_pos": 0.9569,
26:   "nom_pos": 0.8966,
27:   "verbe_cibles": 116,
28:   "nom_cibles": 29
29:  },
30:  "rendement": {
31:   "top1": 0.5858,
32:   "topk": 0.5941,
33:   "exact": 0.5732
34:  },
35:  "corrections": {
36:   "segment_precedent": {
37:    "gain_exact": 6,
38:    "source": "A7",
39:    "ids": [
40:     "s012",
41:     "s030",
42:     "s052",
43:     "s097",
44:     "s124",
45:     "s139"
46:    ]
47:   },
48:   "lexique_anglais": {
49:    "gain_exact": 8,
50:    "gain_top1": 8,
51:    "source": "A2",
52:    "risque": "borne haute"
53:   }
… [676 caractères tronqués]
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
… [14748 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique && ls -la gold*.json && python3 -c \"\nimport json\nfor f in ('gold.json','gold_reel.json','gold_synthetique.json'):\n    d=json.loads(open(f,encoding='utf-8').read())\n    print(f, list(d.keys()), len(d['phrase … [146 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 450905  2 nov 13:27 gold_gele.json
-rw-r--r--. 1 stephane stephane  20009  5 nov 14:14 gold.json
-rw-r--r--. 1 stephane stephane 470149  2 nov 14:39 gold_reel.json
-rw-r--r--. 1 stephane stephane 149191  2 nov 12:04 gold_synthetique.json
gold.json ['version', 'phrases', 'note'] 20
{"id": "g001", "langue": "fr", "texte": "Le chat dort.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chat", "pos": "NOUN", "debut": 3, "fin": 7}, {"texte": "dort", "pos": "VERB", "debut": 8, "fin": 12}], "segments": [{"type": "GN", "texte": "Le chat", "role": "agent", "debut": 0, "fin": 7}, {"type": "GV", "texte": "dort", "role": "prédicat", "debut": 8, "fin": 12}], "pragma": {"acte": "assertion"}}

gold_reel.json ['version', 'source', 'note', 'phrases'] 432
{"id": "r001", "langue": "fr", "texte": "Le chien mange une pomme.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chien", "pos": "NOUN", "debut": 3, "fin": 8}, {"texte": "mange", "pos": "VERB", "debut": 9, "fin": 14}, {"texte": "une", "pos": "DET", "debut": 15, "fin": 18}, {"texte": "pomme", "pos": "NOUN", "debut": 19, "fin": 24}], "segments": [{"type": "GN", "tex
… [1042 caractères tronqués]
  ```

- **bash** `{"command": "mkdir -p /tmp/ech && cat > /tmp/ech/find8.py <<'PY'\nimport json, pathlib, sys\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.insert(0, str(RACINE/\"tools\"))\nsys.path.insert(0, str(RACINE/\"tools/tests/linguistique\"))\nimport bloc_linguistique a … [2388 caractères tronqués]`

  ```
Traceback (most recent call last):
  File "/tmp/ech/find8.py", line 36, in <module>
    "tous_segments": [{"type": x.type, "d": x.debut, "f": x.fin, "t": x.texte,
                                                                      ^^^^^^^
AttributeError: 'Etiquette' object has no attribute 'texte'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -i 's/\"t\": x.texte,/\"t\": phrase[\"texte\"][x.debut:x.fin],/' /tmp/ech/find8.py && python3 /tmp/ech/find8.py 2>&1 | tail -100", "description": "Rerun reproduction script"}`

  ```
{"cibles": 239, "labels": 145, "exact": 137}
NB ECHECS: 8
====================================================================================================
g002 hand fr | Le chat de la voisine dort.
  SEG: {'type': 'GP', 'texte': 'de la voisine', 'debut': 8, 'fin': 21, 'role': 'possession', 'cibles': ['chat'], 'cible': 'chat'}
  CHOISI: '' | CANDIDATS: ['GP']
  META: {}
====================================================================================================
g012 hand fr | Le canard est prêt à manger.
  SEG: {'type': 'GP', 'texte': 'à manger', 'debut': 19, 'fin': 27, 'role': 'but', 'cibles': ['prêt', 'canard'], 'cible': 'prêt'}
  CHOISI: 'manger' | CANDIDATS: ['« à manger » → Le canard', '« à manger » → est prêt', 'manger', 'est', 'canard', 'prêt']
  META: {"segment": "à manger", "cible": "manger"}
====================================================================================================
r018 reel fr | La souris est prête à manger.
  SEG: {'type': 'GP', 'texte': 'à manger', 'debut': 20, 'fin': 28, 'role': 'but', 'cibles': ['prête', 'souris'], 'cible': 'prête'}
  CHOISI: 'manger' | CANDIDATS: ['« à manger » → La souris', '« à manger » → est prête', 'manger', 
… [2127 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"attachement\\|candidat\\|_cible\\|cible\" tools/bloc_linguistique.py | head -120", "description": "Locate attachment logic lines"}`

  ```
7:    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
19:`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script` et ses `candidats`.
76:    candidats: list[str] = field(default_factory=list)
86:            "candidats": list(self.candidats), "langue": self.langue,
602:    def _cibles_s(self, texte: str) -> dict:
603:        """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).
606:        `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
607:        (GP, puis GN, puis GV), comme le premier candidat de `analyser`.
614:            return {(s.debut, s.fin, s.type): (s.cible_gp or s.cible_nom or s.cible_verbe)
621:        """La tête d'un texte de candidat : le verbe plein s'il y en a un, sinon le dernier mot.
661:    def _cible_proche(texte: str, segment: dict, gvs: list[dict],
663:        """La cible d'un segment : le **verbe du GV le plus proche** (règle de proximité).
678:        # un GV réduit à l'auxiliaire (« a », « est ») ne donne pas la cible : on prend le
690:        """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
707:    def _cible_s_par_ge
… [4913 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 540, "limit": 380}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
540:     def _negation(phrase: str) -> bool:
541:         return bool(re.search(r"\b(?:ne|n['’])\b.{0,40}\b(?:pas|plus|jamais|rien|guère)\b", phrase, re.I)
542:                     or re.search(r"\b(?:not|no|never|none|nothing|n't)\b", phrase, re.I))
543: 
544:     @staticmethod
545:     def _modalite(phrase: str) -> bool:
546:         return bool(re.search(r"\b(?:peut|peuvent|peux|pouvons|pouvez|doit|doivent|devons|devez|"
547:                               r"pourrait|pourraient|pourrais|devrait|devraient|voudrais|voudrait|"
548:                               r"faut|falloir|might|may|must|should|could|would|can)\b", phrase, re.I))
549: 
550:     # -- POS ----------------------------------------------------------------
551:     def _pos(self, langue: str, mot: str) -> tuple[str, bool, float]:
552:         lex = POS_FERME.get(langue, POS_FERME["fr"])
553:         n = _normaliser(mot).split("'")[0].split("’")[0]
554:         for classe, mots in lex.items():
555:             if n in mots:
556:                 return classe, False, 0.92
557:         if n in VERBES.get(lan
… [21461 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/ech/trace.py <<'PY'\nimport json, pathlib, sys\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.insert(0, str(RACINE/\"tools\"))\nimport bloc_linguistique as bl\n\nCAS = {\n \"g002\": \"Le chat de la voisine dort.\",\n \"g012\": \"Le canar … [1548 caractères tronqués]`

  ```
====================================================================================================
g002 | Le chat de la voisine dort.
  S cands (nb): 1
   cand 0 nom= '« de la voisine dort » → Le chat'
       GN (0, 7) 'Le chat' role= agent att= None
       GP (8, 26) 'de la voisine dort' role= possession att= None
  cibles_s: {(0, 7, 'GN'): None, (8, 26, 'GP'): 'Le chat'}
  simple: [('GN', 0, 7, 'Le chat'), ('GP', 8, 21, 'de la voisine')]
  verbes POS: [(22, 26, 'dort')]
  gvs_simple: []
====================================================================================================
g012 | Le canard est prêt à manger.
  S cands (nb): 2
   cand 0 nom= '« à manger » → Le canard'
       GN (0, 9) 'Le canard' role= agent att= None
       GV (10, 18) 'est prêt' role= predicat att= None
       GP (19, 27) 'à manger' role= but att= None
   cand 1 nom= '« à manger » → est prêt'
       GN (0, 9) 'Le canard' role= agent att= None
       GV (10, 18) 'est prêt' role= predicat att= None
       GP (19, 27) 'à manger' role= but att= None
  cibles_s: {(0, 9, 'GN'): None, (10, 18, 'GV'): 'Le canard', (19, 27, 'GP'): 'Le canard'}
  simple: [('GN', 0, 9, 'Le canard'), ('GV', 10, 27, 'est prêt 
… [3509 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/ech/labels.py <<'PY'\nimport json, pathlib, sys\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.insert(0, str(RACINE/\"tools\"))\nsys.path.insert(0, str(RACINE/\"tools/tests/linguistique\"))\nimport bloc_linguistique as bl\nCAS = [\"g002\ … [1096 caractères tronqués]`

  ```
==============================================================================================================
g002 | Le chat de la voisine dort.
  gold segments:
     GN (0, 7) 'Le chat' cible= None cibles= None
     GP (8, 21) 'de la voisine' cible= 'chat' cibles= ['chat']
     GV (22, 26) 'dort' cible= None cibles= None
  pred syntagmes:
     GN (0, 7) 'Le chat' conf= 0.55 att= None cand= ['« de la voisine dort » → Le chat', 'chat']
     GP (8, 21) 'de la voisine' conf= 0.3 att= None cand= ['GP']
     GP (8, 26) 'de la voisine dort' conf= 0.55 att= {'segment': 'de la voisine dort', 'cible': 'chat'} cand= ['« de la voisine dort » → Le chat', 'chat']
  pred pos: [('DET', 'Le', 0, 2), ('NOUN', 'chat', 3, 7), ('PREP', 'de', 8, 10), ('DET', 'la', 11, 13), ('NOUN', 'voisine', 14, 21), ('VERB', 'dort', 22, 26)]
==============================================================================================================
g012 | Le canard est prêt à manger.
  gold segments:
     GN (0, 9) 'Le canard' cible= None cibles= None
     GV (10, 18) 'est prêt' cible= None cibles= None
     GP (19, 27) 'à manger' cible= 'prêt' cibles= ['prêt', 'canard']
  pred syntagmes:
     GN (0, 9) 'Le canard
… [5617 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^VERBES\\|^AUXILIAIRES\\|^ADJECTIFS\\|^RELATIFS\\|def _est_verbe\\|^POS_FERME\\|VERBES =\" tools/bloc_linguistique.py | head -20 && echo \"---\" && sed -n '/def _est_verbe/,/^def /p' tools/bloc_linguistique.py | head -40",  … [55 caractères tronqués]`

  ```
298:POS_FERME = {
319:VERBES = {
340:ADJECTIFS = {
367:RELATIFS = {"qui", "que", "qu", "dont", "où", "which", "that", "who", "whom", "whose"}
369:VERBES_IMPERATIFS = set("va viens prends fais dis regarde écoute donne cherche trouve ouvre ferme "
374:VERBES_CONNUS = set("""
422:AUXILIAIRES = set("""
431:def _est_verbe(mot: str) -> bool:
---
def _est_verbe(mot: str) -> bool:
    """Le mot est-il un verbe ? Lexique + désinences courantes (fr/en)."""
    n = _normaliser(mot)
    if not n:
        return False
    if n in VERBES_CONNUS:
        return True
    for suf in ("er", "ir", "e", "es", "ent", "ait", "aient", "é", "ée", "és", "i", "u",
                "ez", "ons", "iez", "ais", "ra", "rai", "ras", "rons", "rez", "ront",
                "s", "ed", "ing", "en"):
        if n.endswith(suf) and n[:-len(suf)] in VERBES_CONNUS:
            return True
    # participes en -é/-és/-ée : `accroché` → `accrocher`
    for suf in ("ées", "ées", "ée", "és", "é"):
        if n.endswith(suf) and (n[:-len(suf)] + "er") in VERBES_CONNUS:
            return True
    return False


def _role_gp(prep: str) -> str:
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '298,445p' tools/bloc_linguistique.py", "description": "Read lexicons"}`

  ```
POS_FERME = {
    "fr": {
        "DET": set("le la les l un une ce cet cette ces mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs quel quelle quels quelles".split()),
        "PREP": set("à a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis pendant durant contre malgré selon près loin devant derrière après avant".split()),
        "PRON": set("je j tu il elle on nous vous ils elles me te se lui leur moi toi soi y en ce cela ça qui que quoi dont où".split()),
        "CONJ": set("et ou mais donc or ni car quand comme si parce puisque lorsque pendant qu".split()),
        "AUX": set("est sont était étaient été être ai as a avons avez ont avait avaient eu avoir suis es sommes êtes".split()),
        "ADV": set("ne n pas plus jamais rien très bien mal ici hier demain aujourd'hui peut-être fort souvent toujours déjà encore tard tôt ainsi alors aussi".split()),
        "NUM": set("deux trois quatre cinq six sept huit neuf dix".split()),
    },
    "en": {
        "DET": set("the a an this that these those my your his her its our their".split()),
        "PREP": set("of to in on at by with from for about into over under between through during w
… [9759 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-echecs-attachement.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-echecs-attachement.md</path>
<type>file</type>
<content>
1: # B13 — les 127 échecs qualifiés : 94 de span, 33 de cible
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
4: > **166/166 portes** : les **127 échecs** de l'attachement (avant ce round) se répartissent en
5: > **94 de span** (aucun segment prédit au même span) et **33 de cible** (le span est bon, la cible
6: > n'est pas dans les candidats) — **32** après le correctif. Le correctif testé — ajouter les GV du chunker aux GV du générateur S et
7: > remplir les segments d'union — ne répare **qu'un** des 33. Les 32 autres ont un GV qui couvre
8: > **toute la phrase** : le dernier token n'est pas le verbe (`… in the park` → `park`, pas `saw`).
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
11: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
12: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-echecs-attachement.json`](pensee-echecs-attachement.json).
13: 
14: ## 1. La répartition
15: 
16: | cause | nombre | part |
17: |---|
… [2625 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"r230\\|r309\\|appelle-moi\\|Peut-être qu\" reports/ docs/ journal/ tools/tests/linguistique/ 2>/dev/null | head -40", "description": "Grep for r230/r309 references"}`

  ```
reports/pensee-topk-diagnostic.json:152:   "raison": "Le candidat est `appelle-moi`, la cible est la base verbale `appelle` : le trait d'union n'est pas découpé.",
reports/pensee-topk-diagnostic.json:164:    "r230 · SUB « Quand tu arrives » → appelle"
reports/pensee-topk-diagnostic.json:182:    "r309 · SUB « qu'il viendra » → viendra"
reports/pensee-topk-diagnostic.json:219:   "detail": "(a) pour un GP, ajouter la tête du GN à gauche (`_tete_nom`) ; (b) si aucun GV, balayer les verbes reconnus dans une fenêtre autour du segment ; (c) découper les enclitiques (`appelle-moi` → `appelle`) ; (d) compléter VERBES_CONNUS (`marche`, `appelle`, `viendra`).",
reports/pensee-topk-diagnostic.json:836:   "id": "r230",
reports/pensee-topk-diagnostic.json:842:   "cible_choisie": "appelle-moi",
reports/pensee-topk-diagnostic.json:845:    "appelle-moi"
reports/pensee-topk-diagnostic.json:850:   "raison_detail": "Le candidat est `appelle-moi`, la cible est la base verbale `appelle` : le trait d'union n'est pas découpé.",
reports/pensee-topk-diagnostic.json:1071:   "id": "r309",
reports/rapport-topk-diagnostic.md:56:| C7 | **candidat tokenisé avec enclitique** (`appelle-moi`) | 1 | 1 | SUB 1 | reel 
… [3393 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-topk-diagnostic.md</path>
<type>file</type>
<content>
1: # B13 — le top-k strict de l'attachement : 57 échecs, dont 45 d'emballage
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
4: > **Verdict** : ✅ **les 57 échecs du top-k strict sont qualifiés** (0 « autre »). Sur les
5: > **145 segments gold dont le span est prédit**, la cible est dans les candidats **134 fois en
6: > sous-chaîne** (0,9241) mais **88 fois en égalité exacte** (0,6069) : **57 échecs**. **45** sont
7: > des **candidats du générateur S non réduits à leur tête** — la cible est déjà dans la chaîne
8: > « « segment » → … », il suffit d'en extraire la tête ; **8** sont des **verbes anglais hors
9: > lexique** ; **4** sont de la **couverture locale** (génitif, enclitique, GV mal délimité).
10: > Le **top-1 est déjà juste 41 fois sur 57** : le top-k strict mesure surtout l'**emballage** des
11: > candidats, pas le choix de la cible. Trois correctifs **simulés, non appliqués**, couvrent
12: > **45 + 8 + 4 = 57** — borne haute, mesurée sur le même gold.
13: >
14: > **Dispositif** : [`bloc_linguistique.py`](..
… [12662 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Construit un harnais de mesure des règles (sans toucher au code)

- **bash** `{"command": "cat > /tmp/ech/harness.py <<'PY'\nimport json, pathlib, sys, re\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.insert(0, str(RACINE/\"tools\"))\nsys.path.insert(0, str(RACINE/\"tools/tests/linguistique\"))\nimport bloc_linguistique as bl\nimport ev … [3772 caractères tronqués]`

  ```
labels: 145 exact: 137
par type: Counter({'GP': 83, 'SUB': 36, 'REL': 26})
par source: Counter({'reel': 105, 'synthetique': 30, 'hand': 10})
cible vide: [('g002', 'GP'), ('s041', 'GP')]
cible non-verbe pour SUB: [('r202', 'pense', 'pense'), ('r212', 'faut', 'faut'), ('r225', 'crois', 'crois'), ('r227', 'lit', 'lit'), ('r229', 'pleure', 'pleure'), ('r230', 'appelle-moi', 'appelle'), ('r232', 'pense', 'pense'), ('r254', 'restons', 'restons'), ('r266', 'pleure', 'pleure'), ('r274', 'continue', 'continue'), ('r309', 'Peut-être', 'viendra'), ('s022', 'nage', 'nage'), ('s054', 'trouve', 'trouve'), ('s088', 'crie', 'crie'), ('s097', 'commence', 'commence'), ('s103', 'dessine', 'dessine'), ('s124', 'commence', 'commence'), ('s139', 'crie', 'crie')]
cible auto (dans le segment): [('g012', 'GP', 'manger', 'à manger'), ('r018', 'GP', 'manger', 'à manger'), ('s022', 'SUB', 'nage', 'que vous nage')]
cible avec trait d'union: [('r230', 'appelle-moi', 'appelle'), ('r309', 'Peut-être', 'viendra')]
GP role possession: [('g002', 'de la voisine', '', 'chat')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, sys, pathlib\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/tests/linguistique\")\nimport bloc_linguistique as bl, evaluer_gold as eg\nph = {p[\"id\"]:p for p in eg.charger()}\nh = bl.Heuristi … [642 caractères tronqués]`

  ```
==========================================================================================
s022 | ils nage que vous nage
 gold: [('GN', 'ils', None), ('GV', 'nage', None), ('SUB', 'que vous nage', 'nage')]
 pred: [('GV', 0, 8, 'ils nage', None), ('SUB', 9, 22, 'que vous nage', {'segment': 'que vous nage', 'cible': 'nage'}), ('REL', 9, 22, 'que vous nage', {'segment': 'que vous nage', 'cible': 'nage'})]
==========================================================================================
r202 | Je pense que tu as raison.
 gold: [('GN', 'Je', None), ('GV', 'pense', None), ('SUB', 'que tu as raison', 'pense')]
 pred: [('GV', 0, 8, 'Je pense', None), ('SUB', 9, 25, 'que tu as raison', {'segment': 'que tu as raison', 'cible': 'pense'}), ('REL', 9, 25, 'que tu as raison', {'segment': 'que tu as raison', 'cible': 'pense'})]
==========================================================================================
r212 | Il faut que tu partes.
 gold: [('GN', 'Il', None), ('GV', 'faut', None), ('SUB', 'que tu partes', 'faut')]
 pred: [('GV', 0, 7, 'Il faut', None), ('SUB', 8, 21, 'que tu partes', {'segment': 'que tu partes', 'cible': 'faut'}), ('REL', 8, 21, 'que tu partes', {'segment'
… [5990 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/ech/sim_lex.py <<'PY'\nimport json, sys, pathlib\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.insert(0, str(RACINE/\"tools\")); sys.path.insert(0, str(RACINE/\"tools/tests/linguistique\"))\nimport bloc_linguistique as bl, evaluer_gold  … [876 caractères tronqués]`

  ```
skip
  ```

- **bash** `{"command": "cat > /tmp/ech/sim_lex.py <<'PY'\nimport json, sys, pathlib\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.insert(0, str(RACINE/\"tools\")); sys.path.insert(0, str(RACINE/\"tools/tests/linguistique\"))\nimport bloc_linguistique as bl, evaluer_gold  … [4113 caractères tronqués]`

  ```
base: 145 exact: 137
V0 base: exact=137 portee=0 gagne=0 perd=0
   gagne: []
L1 lexique (rêver/sauter/marcher): exact=139 portee=2 gagne=2 perd=0
   gagne: ['s108', 's122']
L2 L1 + GV tokens (non chevauchant): exact=132 portee=11 gagne=2 perd=7
   gagne: ['s108', 's122']
   PERD: [('r147', ('attendent', 'porte')), ('r222', ('partirons', 'viens')), ('r227', ('lit', 'dort')), ('r258', ('pars', 'vient')), ('r262', ('travaille', 'dort')), ('r268', ('dansait', 'chantait')), ('r270', ('partons', 'veux'))]
   neutres: [('g002', ('', 'dort')), ('r230', ('appelle-moi', 'arrives'))]
L3 L1 + GV tokens (chevauchant): exact=132 portee=13 gagne=3 perd=8
   gagne: ['s041', 's108', 's122']
   PERD: [('r041', ('joue', 'au')), ('r147', ('attendent', 'porte')), ('r222', ('partirons', 'viens')), ('r227', ('lit', 'dort')), ('r258', ('pars', 'vient')), ('r262', ('travaille', 'dort')), ('r268', ('dansait', 'chantait')), ('r270', ('partons', 'veux'))]
   neutres: [('g002', ('', 'dort')), ('r230', ('appelle-moi', 'arrives'))]
NEG1 placebo verbes hors corpus: exact=137 portee=0 gagne=0 perd=0
   gagne: []
NEG2 L1 sans complétion GV: exact=139 portee=2 gagne=2 perd=0
   gagne: ['s108', 's122']
  ```

- **bash** `{"command": "cat > /tmp/ech/sim_rules.py <<'PY'\nimport json, sys, pathlib, re\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.insert(0, str(RACINE/\"tools\")); sys.path.insert(0, str(RACINE/\"tools/tests/linguistique\"))\nimport bloc_linguistique as bl, evaluer … [5526 caractères tronqués]`

  ```
R-B1 GP possession -> tete GN gauche (sur L1): exact=141 portee=2 gagne=2 perd=0
   touches: [('g002', '', 'chat'), ('s041', '', 'marche')]
R-B2 cible vide -> verbe reconnu le plus proche: exact=141 portee=0 gagne=0 perd=0
R-C enclitique (appelle-moi -> appelle): exact=142 portee=1 gagne=1 perd=0
   touches: [('r230', 'appelle-moi', 'appelle')]
R-D SUB pseudo-GV -> GV suivant / dernier mot du SUB: exact=131 portee=13 gagne=1 perd=12
   touches: [('r202', 'pense', 'raison'), ('r212', 'faut', 'partes'), ('r225', 'crois', 'raison'), ('r229', 'pleure', 'triste'), ('r232', 'pense', 'partir'), ('r266', 'pleure', 'seule'), ('r309', 'Peut-être', 'viendra'), ('s054', 'trouve', 'écoute'), ('s088', 'crie', 'cherche'), ('s097', 'commence', 'nage'), ('s103', 'dessine', 'range'), ('s124', 'commence', 'compte'), ('s139', 'crie', 'observe')]
   PERD: ['r202', 'r212', 'r225', 'r229', 'r232', 'r266', 's054', 's088', 's097', 's103', 's124', 's139']

FINAL exact: 131 / 145
restants faux: [('g012', 'prêt', 'manger'), ('r018', 'prête', 'manger'), ('r202', 'pense', 'raison'), ('r212', 'faut', 'partes'), ('r225', 'crois', 'raison'), ('r229', 'pleure', 'triste'), ('r232', 'pense', 'partir'), ('r266', 'pleu
… [194 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/ech/sim_rules2.py <<'PY'\nimport json, sys, pathlib, re\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.insert(0, str(RACINE/\"tools\")); sys.path.insert(0, str(RACINE/\"tools/tests/linguistique\"))\nimport bloc_linguistique as bl, evalue … [7257 caractères tronqués]`

  ```
R-E GP sans auto-attachement: exact=139 portee=2 gagne=0 perd=0
   touches: [('g012', 'manger', 'est'), ('r018', 'manger', 'est')]
R-B1 GP de possession -> tete du GN gauche: exact=140 portee=1 gagne=1 perd=0
   touches: [('g002', '', 'chat')]
R-B2 cible vide -> verbe reconnu le plus proche: exact=141 portee=1 gagne=1 perd=0
   touches: [('s041', '', 'marche')]
R-C enclitique: exact=142 portee=1 gagne=1 perd=0
   touches: [('r230', 'appelle-moi', 'appelle')]
R-D SUB pseudo-GV ADV -> GV suivant / dernier mot du SUB: exact=143 portee=1 gagne=1 perd=0
   touches: [('r309', 'Peut-être', 'viendra')]

FINAL exact: 143 / 145
restants faux: [('g012', 'prêt', 'est'), ('r018', 'prête', 'est')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, pathlib, re\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/tests/linguistique\")\nimport bloc_linguistique as bl, evaluer_gold as eg\nh = bl.Heuristique()\nfor txt, d, f in [(\"Le canard est pr … [396 caractères tronqués]`

  ```
'est prêt à manger' _tete_texte: 'manger' _verbe_dans: 'manger'
'est prêt' _tete_texte: 'prêt' _verbe_dans: 'est'
'est prête' _tete_texte: 'prête' _verbe_dans: 'est'
'de la voisine' _tete_texte: 'voisine' _verbe_dans: 'voisine'
  ```

- **bash** `{"command": "cat > /tmp/ech/sim_final.py <<'PY'\nimport json, sys, pathlib, re\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.insert(0, str(RACINE/\"tools\")); sys.path.insert(0, str(RACINE/\"tools/tests/linguistique\"))\nimport bloc_linguistique as bl, evaluer … [8791 caractères tronqués]`

  ```
[
 {
  "regle": "R-A lexique verbal",
  "portee": 2,
  "gagne": 2,
  "perd": 0,
  "exact": 139,
  "touches": [
   [
    "s108",
    "papier",
    "rêve"
   ],
   [
    "s122",
    "papier",
    "saute"
   ]
  ]
 },
 {
  "regle": "R-E GP sans auto-attachement",
  "portee": 2,
  "gagne": 2,
  "perd": 0,
  "exact": 141,
  "touches": [
   [
    "g012",
    "manger",
    "prêt"
   ],
   [
    "r018",
    "manger",
    "prête"
   ]
  ]
 },
 {
  "regle": "R-B1 GP possession -> tête GN gauche",
  "portee": 1,
  "gagne": 1,
  "perd": 0,
  "exact": 142,
  "touches": [
   [
    "g002",
    "",
    "chat"
   ]
  ]
 },
 {
  "regle": "R-B2 cible vide -> verbe proche",
  "portee": 0,
  "gagne": 0,
  "perd": 0,
  "exact": 142,
  "touches": []
 },
 {
  "regle": "R-C enclitique",
  "portee": 1,
  "gagne": 1,
  "perd": 0,
  "exact": 143,
  "touches": [
   [
    "r230",
    "appelle-moi",
    "appelle"
   ]
  ]
 },
 {
  "regle": "R-D SUB pseudo-GV ADV",
  "portee": 1,
  "gagne": 1,
  "perd": 0,
  "exact": 144,
  "touches": [
   [
    "r309",
    "Peut-être",
    "viendra"
   ]
  ]
 }
]
FINAL: 144 / 145
restants: [('s041', 'marche', '')]
[stderr]
Traceback (most recent call last):
  File "/tmp/ech/sim_
… [200 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, sys, pathlib, re\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/tests/linguistique\")\nimport bloc_linguistique as bl, evaluer_gold as eg\n\n# --- déclencheurs sur les 239 cibles\nphrases = eg … [2819 caractères tronqués]`

  ```
{
 "total": 239,
 "R-E": {
  "n": 0,
  "ids": []
 },
 "R-B1": {
  "n": 4,
  "ids": [
   "g002",
   "g006",
   "s081",
   "s120"
  ]
 },
 "R-C": {
  "n": 0,
  "ids": []
 },
 "R-D": {
  "n": 1,
  "ids": [
   "r309"
  ]
 },
 "R-A": {
  "n": 13,
  "ids": [
   "s003",
   "s015",
   "s027",
   "s032",
   "s037",
   "s041",
   "s047",
   "s050",
   "s058",
   "s061",
   "s108",
   "s122",
   "s132"
  ]
 }
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, re\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/tests/linguistique\")\nimport bloc_linguistique as bl, evaluer_gold as eg\nph = {p[\"id\"]:p for p in eg.charger()}\nfor pid in (\"g002\",\"g00 … [474 caractères tronqués]`

  ```
==========================================================================================
g002 | Le chat de la voisine dort.
   GN (0, 7) 'Le chat' cible= []
   GP (8, 21) 'de la voisine' cible= ['chat']
   GV (22, 26) 'dort' cible= []
  POS gold: [('Le', 'DET'), ('chat', 'NOUN'), ('de', 'PREP'), ('la', 'DET'), ('voisine', 'NOUN'), ('dort', 'VERB')]
==========================================================================================
g006 | Le chien du voisin aboie la nuit.
   GN (0, 8) 'Le chien' cible= []
   GP (9, 18) 'du voisin' cible= ['chien']
   GV (19, 24) 'aboie' cible= []
   GN (25, 32) 'la nuit' cible= []
  POS gold: [('Le', 'DET'), ('chien', 'NOUN'), ('du', 'PREP'), ('voisin', 'NOUN'), ('aboie', 'VERB'), ('la', 'DET'), ('nuit', 'NOUN')]
==========================================================================================
s081 | cette secrète fenêtre trouve de Alice
   GN (0, 21) 'cette secrète fenêtre' cible= []
   GV (22, 28) 'trouve' cible= []
   GP (29, 37) 'de Alice' cible= ['trouve', 'fenêtre']
  POS gold: [('cette', 'DET'), ('secrète', 'ADJ'), ('fenêtre', 'NOUN'), ('trouve', 'VERB'), ('de', 'PREP'), ('Alice', 'NOUN')]
===================================
… [385 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, re, json\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/tests/linguistique\")\nimport bloc_linguistique as bl, evaluer_gold as eg\nph = {p[\"id\"]:p for p in eg.charger()}\nh = bl.Heuristique() … [751 caractères tronqués]`

  ```
===============================================================================================
g002 | Le chat de la voisine dort.
  nom: « de la voisine dort » → Le chat
    GN (0, 7) 'Le chat'
    GP (8, 26) 'de la voisine dort'
  cibles_s: {(0, 7, 'GN'): None, (8, 26, 'GP'): 'Le chat'}
  gold: [('GN', (0, 7), "'Le chat'", None), ('GP', (8, 21), "'de la voisine'", 'chat'), ('GV', (22, 26), "'dort'", None)]
===============================================================================================
g006 | Le chien du voisin aboie la nuit.
  nom: « du voisin aboie la nuit » → Le chien
    GN (0, 8) 'Le chien'
    GP (9, 32) 'du voisin aboie la nuit'
  cibles_s: {(0, 8, 'GN'): None, (9, 32, 'GP'): 'Le chien'}
  gold: [('GN', (0, 8), "'Le chien'", None), ('GP', (9, 18), "'du voisin'", 'chien'), ('GV', (19, 24), "'aboie'", None), ('GN', (25, 32), "'la nuit'", None)]
===============================================================================================
s081 | cette secrète fenêtre trouve de Alice
  nom: « de Alice » → cette secrète fenêtre
    GN (0, 21) 'cette secrète fenêtre'
    GV (22, 28) 'trouve'
    GP (29, 37) 'de Alice'
  cibles_s: {(0, 21, 'GN'): None, (22, 28, 'G
… [2049 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/linguistique/evaluer_gold.py 2>&1 | tail -5 && echo \"--- exact line from JSON ---\" && python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/ech/eval_base.json >/dev/null 2>&1; python3 -c \"\nimport json\n … [322 caractères tronqués]`

  ```
"exactitude_ouvert": 0.6061,
    "tokens": 2480,
    "confusions": {
     
heuristique all: {"pos": {"exactitude": 0.7455, "exactitude_ferme": 0.8984, "exactitude_ouvert": 0.6007, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 50, "NOUN": 80, "VERB": 4}, "ADV": {"ADV": 117, "NOUN": 21, "PREP": 1, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 118, "?": 3, "NOUN": 3}, "CONJ": {"CONJ": 44, "PRON": 25, "DET": 12, "?": 13, "PREP": 2, "NOUN": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 617, "ADJ": 17, "VERB": 47, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"?": 25}, "PREP": {"PREP": 111, "NOUN": 3}, "PRON": {"PRON": 411, "NOUN": 8, "?": 30, "DET": 25, "CONJ": 1}, "VERB": {"VERB": 314, "NOUN": 447, "ADJ": 5, "PREP": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.3154, "rappel": 0.2619, "f1": 0.2862, "tp": 488, "fp": 1059, "fn": 1375, "tete": {"precision": 0.5862, "rappel": 0.4342, "f1": 0.4989, "tp": 809, "fp": 571, "fn": 1054}}, "pragmatique": {"acte": 0.9967, "negation": 0.9771, "modalite": 0.9886, "double_sens": 0.9444}, "fraction_semantique": 0.5551}
--- exact line from JSON ---
{'cibles': 239, 'labels': 145, 'exact': 137, 'top1': 140, 'topk': 142, 'topk_exact': 141, 'ex
… [181 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/ech/controls.py <<'PY'\nimport json, sys, pathlib, re\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.insert(0, str(RACINE/\"tools\")); sys.path.insert(0, str(RACINE/\"tools/tests/linguistique\"))\nimport bloc_linguistique as bl, evaluer_ … [3625 caractères tronqués]`

  ```
base exact: 137
N3 split any hyphen: portee 2 gagne 1 perd 0 touches [('r230', 'appelle-moi', 'appelle'), ('r309', 'Peut-être', 'Peut')]
[stderr]
Traceback (most recent call last):
  File "/tmp/ech/controls.py", line 58, in <module>
    n4()
    ~~^^
  File "/tmp/ech/controls.py", line 48, in n4
    cands = h._syntagmes_s(texte) or []
            ^
NameError: name 'h' is not defined
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, re\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/tests/linguistique\")\nimport bloc_linguistique as bl, evaluer_gold as eg\nh = bl.Heuristique()\nph = {p[\"id\"]:p for p in eg.charger()}\n# N4 … [1915 caractères tronqués]`

  ```
N4 :
  s022 SUB 'que vous nage' pred='nage' inside=True gold='nage' recalcul='nage'
  g012 GP 'à manger' pred='manger' inside=True gold='prêt' recalcul='prêt'
  r018 GP 'à manger' pred='manger' inside=True gold='prête' recalcul='prête'
N6 :
  g002 GP='de la voisine' tete_GN_gauche='chat' gold='chat' OK
  g006 GP='du voisin' tete_GN_gauche='chien' gold='chien' OK
  s081 GP='de Alice' tete_GN_gauche='fenêtre' gold='trouve' FAUX
  s120 GP='de une chanson' tete_GN_gauche='lettre' gold='prépare' FAUX
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/tests/linguistique\")\nimport bloc_linguistique as bl, evaluer_gold as eg\nph={p[\"id\"]:p for p in eg.charger()}\nh=bl.Heuristique()\nfor pid in ( … [584 caractères tronqués]`

  ```
==========================================================================================
g002 | Le chat de la voisine dort. | cibles: [['chat']]
   'Le'             gold=DET   heur=DET   est_verbe=False
   'chat'           gold=NOUN  heur=NOUN  est_verbe=False
   'de'             gold=PREP  heur=PREP  est_verbe=False
   'la'             gold=DET   heur=DET   est_verbe=False
   'voisine'        gold=NOUN  heur=NOUN  est_verbe=False
   'dort'           gold=VERB  heur=VERB  est_verbe=True
==========================================================================================
g012 | Le canard est prêt à manger. | cibles: [['prêt', 'canard']]
   'Le'             gold=DET   heur=DET   est_verbe=False
   'canard'         gold=NOUN  heur=NOUN  est_verbe=False
   'est'            gold=AUX   heur=AUX   est_verbe=True
   'prêt'           gold=ADJ   heur=ADJ   est_verbe=False
   'à'              gold=PREP  heur=PREP  est_verbe=False
   'manger'         gold=VERB  heur=VERB  est_verbe=True
==========================================================================================
r018 | La souris est prête à manger. | cibles: [['prête', 'souris']]
   'La'             gold=DET   heur=DET   
… [2659 caractères tronqués]
  ```

- **bash** `{"command": "date -I && cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | tail -5 && git log -1 --format='%h %ad %s' --date=short && python3 - <<'PY'\nimport json\nd=json.load(open('/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-topk-diagnostic.json'))\nprint(list(d … [74 caractères tronqués]`

  ```
2026-11-05
xnli-3b.json
xnli-3b-l30.json
xnli-entrainement-3b.json
xnli-mlp-3b.json
xnli-train-complet-3b.json
a914c1e7 2026-11-05 FICHES — LES 3 DIVERGENCES ET LEURS RÉSIDUS CORRIGÉS (SPANS, DÉNOMINATEUR, LEXIQUE ÉLARGI) ; COHÉRENCE A4 À JOUR
['date', 'ligne', 'titre', 'verdict', 'non_applique', 'gold', 'mesure', 'causes', 'correctifs', 'controle_negatif', 'limites', 'segments', 'methode']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-topk-diagnostic.json'))\nprint(json.dumps({k:d[k] for k in d if k!='segments'}, ensure_ascii=False, indent=1)[:3000])\nprint(\"--- un segment ---\")\nfor s in d['segment … [188 caractères tronqués]`

  ```
{
 "date": "2026-11-05",
 "ligne": "B13",
 "titre": "Top-k strict de l'attachement : 57 échecs qualifiés, 45 d'emballage",
 "verdict": "57/57 échecs classés (0 « autre ») ; 3 correctifs simulés couvrent 45 + 8 + 4 = 57, soit un plafond de 145/145 en top-k strict — borne haute, même gold, code non modifié.",
 "non_applique": true,
 "gold": {
  "fichier": "tools/tests/linguistique/gold.json + gold_reel.json + gold_synthetique.json",
  "phrases": 612,
  "charger": "evaluer_gold.charger()"
 },
 "mesure": {
  "phrases": 612,
  "cibles_gold": 239,
  "segments_span_predit": 145,
  "topk_sous_chaine": 134,
  "topk_exact": 88,
  "echecs_stricts": 57,
  "top1_exact": 123,
  "taux_span": {
   "topk_sous_chaine": 0.9241,
   "topk_exact": 0.6069,
   "top1_exact": 0.8483
  },
  "rendement_239": {
   "topk_sous_chaine": 0.5607,
   "topk_exact": 0.3682
  }
 },
 "causes": [
  {
   "code": "C1",
   "libelle": "candidat S non réduit à sa tête — cible nominale",
   "raison": "La cible est un nom (antécédent REL) présent seulement dans la chaîne de présentation « « segment » → Le X » ; la liste des candidats garde la chaîne entière, pas `X`.",
   "effectif": 26,
   "dont_sous_chaine": 26,
   "types": {
… [4555 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nd=json.load(open('/tmp/ech/eval_base.json'))\nprint('hasard:', d['attachement_hasard'])\nprint('verdict ok:', d['ok'])\nprint('heur all att:', {k:d['heuristique']['all']['attachement'][k] for k in ('cibles … [239 caractères tronqués]`

  ```
hasard: {'cibles': 239, 'top1_taux': 0.0042}
verdict ok: True
heur all att: {'cibles': 239, 'labels': 145, 'exact': 137, 'top1': 140, 'topk': 142, 'topk_exact': 141, 'couverture': 0.6067}
hasard vs top1: 139.48
  ```

- **bash** `{"command": "cat > /tmp/ech/final_measure.py <<'PY'\nimport json, sys, pathlib, re\nRACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nsys.path.insert(0, str(RACINE/\"tools\")); sys.path.insert(0, str(RACINE/\"tools/tests/linguistique\"))\nimport bloc_linguistique as bl, eva … [7240 caractères tronqués]`

  ```
{
 "R1 lexique verbal (rêver, sauter, marcher)": {
  "portee": 2,
  "gagne": 2,
  "perd": 0,
  "exact": 139
 },
 "R2 GP sans auto-attachement": {
  "portee": 2,
  "gagne": 2,
  "perd": 0,
  "exact": 141
 },
 "R3a GP possession -> tête du GN gauche": {
  "portee": 1,
  "gagne": 1,
  "perd": 0,
  "exact": 142
 },
 "R3b cible vide -> verbe reconnu le plus proche": {
  "portee": 1,
  "gagne": 1,
  "perd": 0,
  "exact": 143
 },
 "R4 enclitique": {
  "portee": 1,
  "gagne": 1,
  "perd": 0,
  "exact": 144
 },
 "R5 SUB pseudo-GV ADV": {
  "portee": 1,
  "gagne": 1,
  "perd": 0,
  "exact": 145
 }
}
FINAL: 145 restants: []
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"reports\" tools/revue_documentation.py | head -30 && echo \"---\" && grep -n \"def \\|REQUIS\\|lien\" tools/revue_documentation.py | head -40", "description": "Check doc review constraints on reports"}`

  ```
5:  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
7:  3. annotation : les liens relatifs des docs/ et reports/ résolvent, et leur libellé ne
30:    r"`((?:docs|reports|tools|journal|data|drave-core|sprints)/"
76:    return list((RACINE / "reports").glob("*.md"))
95:            + [RACINE / "reports/07-mesures-couche-commune.md",
96:               RACINE / "reports/fiche-nuit-17-10.md",
113:    return len(list((RACINE / "reports").glob("*.json")))
167:        if not (RACINE / "reports" / nom).exists():
168:            alertes.append(f"classement : la fiche courante reports/{nom} manque")
169:    if not (RACINE / "reports/README.md").exists():
170:        alertes.append("classement : reports/ n'a pas d'index (reports/README.md)")
219:            if not (re.match(r"^(docs|reports|tools|journal)/", lab)
---
7:  3. annotation : les liens relatifs des docs/ et reports/ résolvent, et leur libellé ne
35:def liens(texte: str):
39:def cible_generee(f: pathlib.Path, cible: str) -> bool:
43:def date_dernier_commit() -> str:
52:def date_dernier_changement(chemin: str) -> str:
62:def est_carte(p: pathlib.Path) -> bool:
66:def docs_vivants():
71:def docs_t
… [986 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,\"tools\"); sys.path.insert(0,\"tools/tests/linguistique\")\nimport bloc_linguistique as bl, evaluer_gold as eg\nh=bl.Heuristique()\nfor txt in (\"Quand tu arrives, appelle-moi.\",\"Peu … [292 caractères tronqués]`

  ```
================================================================================
Quand tu arrives, appelle-moi.
 _mots: [(0, 5, 'Quand', 'mot'), (6, 8, 'tu', 'mot'), (9, 16, 'arrives', 'mot'), (16, 17, ',', 'ponctuation'), (18, 29, 'appelle-moi', 'mot'), (29, 30, '.', 'ponctuation')]
 pos: [('CONJ', 'Quand', 0, 5), ('PRON', 'tu', 6, 8), ('VERB', 'arrives', 9, 16), ('NOUN', 'appelle-moi', 18, 29)]
================================================================================
Peut-être qu'il viendra.
 _mots: [(0, 9, 'Peut-être', 'mot'), (10, 15, "qu'il", 'mot'), (16, 23, 'viendra', 'mot'), (23, 24, '.', 'ponctuation')]
 pos: [('ADV', 'Peut-être', 0, 9), ('CONJ', "qu'il", 10, 15), ('NOUN', 'viendra', 16, 23)]
  ```

