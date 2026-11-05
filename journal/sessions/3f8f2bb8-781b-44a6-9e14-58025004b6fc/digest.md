# Session DSH — relecture

- identifiant : `3f8f2bb8-781b-44a6-9e14-58025004b6fc`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 14:22:47
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer l'attachement v2** (l'intégration du 2026-11-05 14 h) et vérifier que ses chiffres et ses portes sont justes.

Contexte : `tools/bloc_linguistique.py` (classe `Heuristique`), `tools/tests/linguistique/evaluer_gold.py` (`charger()`, `evaluer_bloc`), `tools/tests/linguistique/gold_reel.py` (`CONVENTION_CIBLE`), `tools/pensee/autotest.py` (portes T153, T161–T177). La fiche à auditer est `reports/rapport-pensee-attachement-v2.md` et son JSON `reports/pensee-attachement-v2.json`.

Revendications à rejouer : labels 145, top1 140, top-k 142, exact 137, top-k strict 141 ; rendement top1 0,5858 / topk 0,5941 / exact 0,5732 ; exactitude spans 0,9655 / 0,9793 / 0,9448 / top-k strict 0,9724 ; split POS gold 116 verbes (111 justes, 0,9569) et 29 noms (26 justes, 0,8966) ; 8 échecs de cible (3 hors candidats, 5 mal classés) ; spans 94 = 48 REL / 33 SUB / 13 GP.

À faire :
1. Rejoue chaque valeur depuis la racine (`sys.path.insert(0,'.')`) et compare à la fiche et au JSON ; note tout écart, même d'arrondi.
2. Vérifie que les portes citées (T153, T161, T162, T163, T164, T166, T167, T168, T169, T170, T172, T173, T175, T176, T177) attendent bien ces valeurs (lis `tools/pensee/autotest.py`) et signale toute porte périmée ou tout chiffre non couvert.
3. Contrôles : permutation des cibles (1000 tirages), candidat aléatoire, et vérifie que le +45 du top-k strict vient bien de la réduction des candidats (compare en désactivant mentalement l'ajout des têtes, sans modifier le fichier — tu peux le simuler sur une copie locale).
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-audit-v2.md` (fiche : verdict, tableau mesuré/revendiqué, portes, contrôles, limites) et `reports/pensee-audit-v2.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé avec les écarts et les portes périmées.
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

⏵ Reading the audit target (fiche + JSON) and the code it describes.

- **bash** `{"command": "pwd && git -C . branch --show-current && git status --porcelain | head -50 && ls reports/ | grep -i attachement", "description": "Check repo state and locate attachment reports"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
s/v7
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
D  journal/sessions/65495a29-10c0-4571-96be-e7729f1efebf/digest.md
D  journal/sessions/65495a29-10c0-4571-96be-e7729f1efebf/rapport.md
MM journal/sessions/MANIFEST.md
D  journal/sessions/a8035275-c7b9-4713-a6ab-7b859cd72306/digest.md
D  journ
… [1783 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-v2.md"}`

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

### 🤖 Assistant

⏵ Reading the JSON and the evaluation pipeline sources.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-attachement-v2.json"}`

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

- **bash** `{"command": "wc -l tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/gold_reel.py tools/pensee/autotest.py reports/rapport-pensee-attachement.md reports/pensee-attachement.json 2>/dev/null; ls -la tools/tests/linguistique/", "description": "Line counts of k … [10 caractères tronqués]`

  ```
1929 tools/bloc_linguistique.py
   287 tools/tests/linguistique/evaluer_gold.py
  1385 tools/tests/linguistique/gold_reel.py
  2785 tools/pensee/autotest.py
    56 reports/rapport-pensee-attachement.md
    22 reports/pensee-attachement.json
  6464 total
total 1408
drwxr-xr-x. 1 stephane stephane    708  5 nov 13:57 .
drwxr-xr-x. 1 stephane stephane    640  4 nov 08:44 ..
-rw-r--r--. 1 stephane stephane  16090  2 nov 09:26 anaphore.py
-rw-r--r--. 1 stephane stephane  34857  5 nov 13:57 classement_cible.py
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
drwxr-xr-x. 1 stephane stephane  
… [640 caractères tronqués]
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

### 🤖 Assistant

⏵ Locating the cited gates in autotest.py.

- **bash** `{"command": "grep -n '\"T1[5-7][0-9]\"\\|T153\\|T161\\|T162\\|T163\\|T164\\|T166\\|T167\\|T168\\|T169\\|T170\\|T172\\|T173\\|T175\\|T176\\|T177' tools/pensee/autotest.py | head -80", "description": "Find cited gate definitions"}`

  ```
2751:              ("T153 attachement", t153_attachement()),
2759:              ("T161 cible proximité", t161_cible_proximite()),
2760:              ("T162 candidats verbes", t162_candidats_verbes()),
2761:              ("T163 échecs attachement", t163_echecs_attachement()),
2762:              ("T164 verbe du GV", t164_verbe_gv()),
2764:              ("T166 spans perdus", t166_spans()),
2765:              ("T167 dénominateur", t167_denominateur()),
2766:              ("T168 classement", t168_classement()),
2767:              ("T169 conventions", t169_conventions()),
2768:              ("T170 attachement ciblé", t170_attachement_cible()),
2770:              ("T172 échecs de cible", t172_echecs_cible()),
2771:              ("T173 top-k strict", t173_topk_strict()),
2773:              ("T175 audit attachement", t175_audit_attachement()),
2774:              ("T176 segment précédent", t176_segment_precedent()),
2775:              ("T177 candidats têtes", t177_candidats_tete())]
  ```

- **bash** `{"command": "grep -n 'attachement\\|CONVENTION_CIBLE\\|cible' tools/pensee/autotest.py | head -100", "description": "Find attachment references in autotest"}`

  ```
2221:def t153_attachement() -> tuple[bool, str]:
2222:    """L'attachement sur le gold 612 (239 cibles) : top1 0,5272, exact 0,5105."""
2225:    r = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
2226:    return (r["cibles"] == 239 and abs(r["top1_taux"] - 0.5858) < 0.001
2228:        f"attachement : top1 {r['top1_taux']}, exact {r['exact_taux']}, "
2232:def t154_cibles() -> tuple[bool, str]:
2233:    """Les cibles de l'attachement : 1624 segments sans cible sur 1863."""
2237:    sans = sum(1 for p in ph for s in p["segments"] if not s.get("cible"))
2239:        f"cibles : {sans}/{tot} segments sans cible (couverture {round((tot-sans)/tot,4)})")
2242:def t155_cibles_500() -> tuple[bool, str]:
2250:            if not s.get("cible"):
2338:def t161_cible_proximite() -> tuple[bool, str]:
2339:    """La cible par proximité : le verbe du GV le plus proche."""
2343:    a, th = r["attachement"], r["attachement_tete"]
2344:    return (a["cibles"] == 239 and a["top1"] == 140 and a["exact"] == 137), (
2354:    a, th = r["attachement"], r["attachement_tete"]
2359:def t163_echecs_attachement() -> tuple[bool, str]:
2360:    """Les échecs de l'attachement : 94 de span, 33 de cible.
… [4910 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading all cited gate bodies in detail.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "offset": 2200, "limit": 420}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
2200:     d = json.loads((racine / "reports/pensee-quatre-modes-432-soustype-t03.json").read_text(encoding="utf-8"))
2201:     m = d["modes"]["parallele_niveau"]["all"]["pragmatique"]
2202:     h = d["modes"]["heuristique"]["all"]["pragmatique"]
2203:     return abs(m["double_sens"] - 0.9838) < 0.001 and m["double_sens"] > h["double_sens"], (
2204:         f"sous-type 0,3 : double sens {m['double_sens']} > {h['double_sens']}")
2205: 
2206: 
2207: def t152_tirages() -> tuple[bool, str]:
2208:     """Les trois tirages : 0,9838 exactement, le cache masque la variance."""
2209:     import json
2210:     import pathlib
2211:     racine = pathlib.Path(__file__).resolve().parents[2]
2212:     val = []
2213:     for suffixe in ("", "b", "c"):
2214:         f = racine / f"reports/pensee-quatre-modes-432-soustype-t03{suffixe}.json"
2215:         d = json.loads(f.read_text(encoding="utf-8"))
2216:         val.append(round(d["modes"]["parallele_niveau"]["all"]["pragmatique"]["double_sens"], 4))
2217:     return val == [0.9838, 0.9838, 0.9838], (
2218:         f"tirages : {val} (éca
… [21553 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the gate registry and the gold convention.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "limit": 60, "offset": 2735}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
2735:               ("T137 vrais absents", t137_vrais_absents()),
2736:               ("T138 défaut fusion", t138_defaut_niveau()),
2737:               ("T139 quatre modes", t139_quatre_modes()),
2738:               ("T140 refus r353", t140_r353()),
2739:               ("T141 élision", t141_elision()),
2740:               ("T142 confirmation", t142_run2()),
2741:               ("T143 défaut conditionnel", t143_defaut_conditionnel()),
2742:               ("T144 seuil parallèle", t144_seuil_parallele()),
2743:               ("T145 troisième passe", t145_troisieme_passe()),
2744:               ("T146 DRVM N0.1", t146_drvm_n01()),
2745:               ("T147 variance", t147_variance()),
2746:               ("T148 pragmatique neuronale", t148_pragmatique()),
2747:               ("T149 pragma 432", t149_pragmatique_full()),
2748:               ("T150 fusion sous-type", t150_fusion_soustype()),
2749:               ("T151 variance sous-type", t151_soustype_variance()),
2750:               ("T152 trois tirages", t152_tirages()),
2751:               ("T153 attachement", t153_attac
… [1996 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'CONVENTION_CIBLE' -A 40 tools/tests/linguistique/gold_reel.py | head -60", "description": "Read CONVENTION_CIBLE definition"}`

  ```
27:CONVENTION_CIBLE = {
28-    "REL": "antécédent (tête du GN à gauche) quand le segment précédent est un GN",
29-    "SUB": "verbe gouverneur (69/69 cibles sont des VERB au POS gold)",
30-    "GP": "verbe gouverneur, ou nom complété pour un génitif",
31-    "GN": "nom ou verbe dont le segment dépend",
32-    "GV": "nom ou verbe dont le segment dépend",
33-    "note": "deux conventions dans le même champ ; mesurées séparément (verbe / nom)",
34-}
35-
36-PHRASES = [
37-    ("r001", "fr", "Le chien mange une pomme.",
38-     [("Le", "DET"), ("chien", "NOUN"), ("mange", "VERB"), ("une", "DET"), ("pomme", "NOUN")],
39-     [("GN", "Le chien", "agent"), ("GV", "mange", "prédicat"), ("GN", "une pomme", "patient")], {"acte": "assertion"}),
40-    ("r002", "fr", "La fille lit le journal.",
41-     [("La", "DET"), ("fille", "NOUN"), ("lit", "VERB"), ("le", "DET"), ("journal", "NOUN")],
42-     [("GN", "La fille", "agent"), ("GV", "lit", "prédicat"), ("GN", "le journal", "patient")], {"acte": "assertion"}),
43-    ("r003", "fr", "Nous aimons la musique.",
44-     [("Nous", "PRON"), ("aimons", "VERB"), ("la", "DET"), ("musique", "NOUN")],
45-     [("GN", "Nous", "agent"), ("GV", "aimons", "pr
… [1902 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Replaying all claimed attachment metrics from the repo root.

- **bash** `{"command": "mkdir -p /tmp/audit_v2 && cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' > /tmp/audit_v2/mesure.json 2>/tmp/audit_v2/mesure.err\nimport sys, json\nsys.path.insert(0, '.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import cha … [446 caractères tronqués]`

  ```
{"phrases": 612, "tokens": 3179, "segments": 1863}
{"bloc": "h", "phrases": 612, "pos": {"exactitude": 0.7455, "exactitude_ferme": 0.8984, "exactitude_ouvert": 0.6007, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 50, "NOUN": 80, "VERB": 4}, "ADV": {"ADV": 117, "NOUN": 21, "PREP": 1, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 118, "?": 3, "NOUN": 3}, "CONJ": {"CONJ": 44, "PRON": 25, "DET": 12, "?": 13, "PREP": 2, "NOUN": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 617, "ADJ": 17, "VERB": 47, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"?": 25}, "PREP": {"PREP": 111, "NOUN": 3}, "PRON": {"PRON": 411, "NOUN": 8, "?": 30, "DET": 25, "CONJ": 1}, "VERB": {"VERB": 314, "NOUN": 447, "ADJ": 5, "PREP": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.3154, "rappel": 0.2619, "f1": 0.2862, "tp": 488, "fp": 1059, "fn": 1375, "tete": {"precision": 0.5862, "rappel": 0.4342, "f1": 0.4989, "tp": 809, "fp": 571, "fn": 1054}}, "pragmatique": {"acte": 0.9967, "negation": 0.9771, "modalite": 0.9886, "double_sens": 0.9444}, "fraction_semantique": 0.5551, "attachement": {"cibles": 239, "labels": 145, "top1": 140, "topk": 142, "exact": 137, "top1_taux": 0.5858, "topk_taux": 0.5941, "exact
… [455 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Replaying succeeds; now checking the “before” baseline and the head-candidate mechanism.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-attachement.json"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement.md</path>
<type>file</type>
<content>
1: # B13 — l'attachement sur le gold 432 : top1 0,3431, exact 0,0042
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
4: > **156/156 portes** : l'**attachement** (le segment → sa cible) est mesuré sur le gold 432 :
5: > **top1 0,3431**, **top-k 0,3264**, **exact 0,0042**, **couverture 0,6067**. La couverture est la
6: > première limite : **145 cibles sur 239** sont annotées, et l'attachement exact est **quasi nul**
7: > (1 sur 239).
8: >
9: > **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
10: > [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
11: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-attachement.json`](pensee-attachement.json).
12: 
13: ## 1. Les deux mesures
14: 
15: | mesure | cibles | labels | top1 | top-k | exact | couverture |
16: |---|---:|---:|---:|---:|---:|---:|
17: | attachement | 239 | 145 | 82 (0,3431) | 78 (0,3264) | **1 (0,0042)** | 0,6067 |
18: | attachement (tête) | 145 | 145 | 81 (0,5586) | 77 (0,5310) | — | 1,000
… [1958 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-attachement.json</path>
<type>file</type>
<content>
1: {
2:  "date": "2026-11-04",
3:  "ligne": "B13",
4:  "portes": "156/156",
5:  "attachement": {
6:   "cibles": 239,
7:   "labels": 145,
8:   "top1": 0.3431,
9:   "topk": 0.3264,
10:   "exact": 0.0042,
11:   "couverture": 0.6067
12:  },
13:  "tete": {
14:   "top1": 0.5586,
15:   "topk": 0.531
16:  },
17:  "limites": [
18:   "94 cibles sans label",
19:   "1 exact",
20:   "gold 432"
21:  ]
22: }

(End of file - total 22 lines)
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'candidat\\|tete\\|tête' tools/bloc_linguistique.py | head -80", "description": "Find candidate head logic"}`

  ```
7:    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
19:`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script` et ses `candidats`.
76:    candidats: list[str] = field(default_factory=list)
86:            "candidats": list(self.candidats), "langue": self.langue,
607:        (GP, puis GN, puis GV), comme le premier candidat de `analyser`.
620:    def _tete_texte(texte: str) -> str | None:
621:        """La tête d'un texte de candidat : le verbe plein s'il y en a un, sinon le dernier mot.
624:        `« … → est prêt »` → `prêt` (l'auxiliaire n'est pas la tête).
635:    def _tete_nom(texte: str, debut: int, fin: int) -> str | None:
636:        """La tête nominale d'un span : le dernier mot, **élision séparée** (`L'homme` → `homme`)."""
690:        """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
745:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
758:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
767:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
776:                                 "texte": tex
… [2652 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the A1 audit snapshot used as the “before” baseline.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-audit-attachement.json"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-audit-attachement.json</path>
<type>file</type>
<content>
1: {
2:  "date": "2026-11-05",
3:  "ligne": "B13",
4:  "objet": "audit de reproductibilité de la mesure d'attachement du bloc linguistique",
5:  "verdict": {
6:   "statut": "reproduit",
7:   "valeurs_publiees": 14,
8:   "valeurs_reproduites": 14,
9:   "ecarts": 0,
10:   "reserve": "3 JSON sur 5 (conventions, attachement-cible, spans) sont des instantanés antérieurs, reproduits à leur commit mais pas à l'état courant ; dans sa version committée, pensee-spans.json publie 12 GP / 93 spans dans son bloc `spans`, pas 13 / 94. L'audit n'a modifié aucun fichier existant et n'a fait aucun commit."
11:  },
12:  "dispositif": {
13:   "date": "2026-11-05",
14:   "branche": "s/v7",
15:   "commit": "e1171032906de46f1a93fee0f6275f39b5d67692",
16:   "commit_sujet": "PILOTAGE — PROTOCOLE D'INTÉGRATION DES SOUS-AGENTS (REJOUER, REJETER, COMMITTER VÉRIFIÉ) ; § 9",
17:   "heure_mesure": "2026-11-05T13:29:44-0500",
18:   "bloc_linguistique_sha256": "d9c9d5592b0ba8a942860518b67b5dce04223e47c47904fbf8e185f0511b186d",
19:   "evaluer_gold_sha256": "dbbcfe9007f1d7ee66f6b7a28b064b3c
… [24640 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' reports/rapport-audit-attachement.md", "description": "Read audit attachment report"}`

  ```
# Audit de reproductibilité — l'attachement du bloc linguistique (B13)

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
> **Verdict** : ✅ **reproduit — 14/14 valeurs, écart 0** ; ⚠️ **réserve documentaire** :
> **3 des 5 JSON sont des instantanés antérieurs**, reproduits à leur commit mais pas à
> l'état courant. L'audit n'a modifié aucun fichier existant et n'a fait aucun commit.

> **Dispositif** : depuis la racine, `sys.path.insert(0, '.')` ;
> `from tools.bloc_linguistique import Heuristique` ;
> `from tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc` ;
> `evaluer_bloc("heuristique", Heuristique(), charger())` pour l'attachement ; pour les spans,
> même boucle que `T166` : chaque `segment` du gold est comparé aux étiquettes de niveau
> `syntagme` par `(type, debut, fin)`. Mesure rejouée sur `s/v7`, commit **`e1171032`**,
> `bloc_linguistique.py` sha256 **`d9c9d559…`**, `evaluer_gold.py` sha256 **`dbbcfe90…`**,
> gold inchangé (612 phrases : 20 `hand` + 432 `reel` + 160 synthétiques). Durée : 0,45–0,55 s.
> Les cinq JSON sont lus dans leur version du commit **`e1171032`** ; la note de concurrence
> du § 3 dit ce qui a boug
… [6388 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reconstructing the v2 commit chain to isolate each claimed gain.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -12 && echo '--- v2 files history ---' && git log --oneline -8 -- reports/rapport-pensee-attachement-v2.md reports/pensee-attachement-v2.json tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools … [85 caractères tronqués]`

  ```
de292c7d ÉTAT — B13 180/180, T0 DANS LE BUDGET ; VAGUE 3 LANCÉE (AUDIT V2, ÉCHECS, REPLIS, CACHE)
2e08cbc7 B13 — LA VAGUE 1 COMPLÈTE : CONTRAT S, COÛT DU CHUNKER, COHÉRENCE DES FICHES ; 3 DIVERGENCES CORRIGÉES
9d5337ce B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180
e1171032 PILOTAGE — PROTOCOLE D'INTÉGRATION DES SOUS-AGENTS (REJOUER, REJETER, COMMITTER VÉRIFIÉ) ; § 9
4a65d44f PILOTAGE — VAGUE 1 DES SOUS-AGENTS NOTÉE ; HORODATAGES ALIGNÉS SUR 13 H 15
dfc860a4 ÉTAT — LE LIEN VERS PLAN-TRAVAIL EST RÉPARÉ (../PLAN-TRAVAIL.MD → PLAN-TRAVAIL.MD) ; LA REVUE DE DOCUMENTATION REPASSE VERTE
56d70431 ÉTAT — B13 177/177, TRIM T0 ; LA TRANCHE SOUS-AGENTS CONTINUE
6bbd9c54 PILOTAGE — LA TRANCHE 11 H 15 → 18 H LANCE QUATRE SOUS-AGENTS (AUDIT, TOP-K, CLASSEMENT, COHÉRENCE) ; § 9 DU PLAN-TRAVAIL
0ddd4fb9 B13 — LA CONVENTION DES CIBLES EST DOCUMENTÉE DANS LE GOLD (REL/SUB → ANTÉCÉDENT, GP → VERBE) ; 177/177
efaab321 ÉTAT — B13 176/176 : TOP-K STRICT 0,6069 DANS LE PILOTAGE ; PROCHAINE ACTION LES CANDIDATS RÉDUITS
e223a98d B13 — LE TOP-K STRICT : 0,6069 EN ÉGALITÉ EXACTE, PAS 0,9241 (SOUS-CHAÎNES) ; 176/17
… [1042 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -15 --all --decorate | cat", "description": "List recent commits all branches"}`

  ```
de292c7d (HEAD -> s/v7) ÉTAT — B13 180/180, T0 DANS LE BUDGET ; VAGUE 3 LANCÉE (AUDIT V2, ÉCHECS, REPLIS, CACHE)
2e08cbc7 B13 — LA VAGUE 1 COMPLÈTE : CONTRAT S, COÛT DU CHUNKER, COHÉRENCE DES FICHES ; 3 DIVERGENCES CORRIGÉES
9d5337ce B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180
e1171032 PILOTAGE — PROTOCOLE D'INTÉGRATION DES SOUS-AGENTS (REJOUER, REJETER, COMMITTER VÉRIFIÉ) ; § 9
4a65d44f PILOTAGE — VAGUE 1 DES SOUS-AGENTS NOTÉE ; HORODATAGES ALIGNÉS SUR 13 H 15
dfc860a4 ÉTAT — LE LIEN VERS PLAN-TRAVAIL EST RÉPARÉ (../PLAN-TRAVAIL.MD → PLAN-TRAVAIL.MD) ; LA REVUE DE DOCUMENTATION REPASSE VERTE
56d70431 ÉTAT — B13 177/177, TRIM T0 ; LA TRANCHE SOUS-AGENTS CONTINUE
6bbd9c54 PILOTAGE — LA TRANCHE 11 H 15 → 18 H LANCE QUATRE SOUS-AGENTS (AUDIT, TOP-K, CLASSEMENT, COHÉRENCE) ; § 9 DU PLAN-TRAVAIL
0ddd4fb9 B13 — LA CONVENTION DES CIBLES EST DOCUMENTÉE DANS LE GOLD (REL/SUB → ANTÉCÉDENT, GP → VERBE) ; 177/177
efaab321 ÉTAT — B13 176/176 : TOP-K STRICT 0,6069 DANS LE PILOTAGE ; PROCHAINE ACTION LES CANDIDATS RÉDUITS
e223a98d B13 — LE TOP-K STRICT : 0,6069 EN ÉGALITÉ EXACTE, PAS 0,9241 (SOUS-CH
… [440 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspecting the v2 diff and the exact head-candidate code block.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat 9d5337ce | cat && echo '=== diff bloc ===' && git show 9d5337ce -- tools/bloc_linguistique.py | head -200", "description": "Show v2 commit stat and bloc diff"}`

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
… [8747 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 120, "offset": 600}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
600:             return None
601: 
602:     def _cibles_s(self, texte: str) -> dict:
603:         """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).
604: 
605:         Lecture seule de l'API interne du S : `_tokens`/`_segmente` rendent les `Segment` avec
606:         `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
607:         (GP, puis GN, puis GV), comme le premier candidat de `analyser`.
608:         """
609:         if not self.segmenter_s:
610:             return {}
611:         try:
612:             import generateur
613:             base = generateur._segmente(texte, generateur._tokens(texte))
614:             return {(s.debut, s.fin, s.type): (s.cible_gp or s.cible_nom or s.cible_verbe)
615:                     for s in base}
616:         except Exception:
617:             return {}
618: 
619:     @staticmethod
620:     def _tete_texte(texte: str) -> str | None:
621:         """La tête d'un texte de candidat : le verbe plein s'il y en a un, sinon le dernier mot.
622: 
623:         `« … → Le livre 
… [5165 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Locating lexicon set and head-helper usages for ablation.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '_tete_texte\\|VERBES\\b\\|^VERBES\\|VERBES =' tools/bloc_linguistique.py | head -30 && echo '--- context 390-430 ---' && sed -n '385,425p' tools/bloc_linguistique.py && echo '--- imports ---' && sed -n '1,45p' tools/bloc_lin … [69 caractères tronqués]`

  ```
319:VERBES = {
369:VERBES_IMPERATIFS = set("va viens prends fais dis regarde écoute donne cherche trouve ouvre ferme "
374:VERBES_CONNUS = set("""
557:        if n in VERBES.get(langue, VERBES["fr"]):
620:    def _tete_texte(texte: str) -> str | None:
904:                            tete = self._tete_texte(nom.split("→", 1)[1])
--- context 390-430 ---
chanter chante chantes chantent chantait danser danse danses dansent dansait travailler travaille
accrocher accroche accroches accrochent accrochait porter porte portes portent portait montrer
montre montres montrent montrait tomber tombe tombes tombent tombait rester reste restes restent
restait arriver arrive arrives arrivent arrivait entrer entre entres entrent entrait rentrer
rentre rentres rentrent rentrait retourner retourne retournes retournent retournait passer passe
passes passent passait monter monte montes montent montait descendre descends descend descendent
descendait sortir sors sort sortent sortait perdre perds perd perdent perdait rendre rends rend
rendent rendait vendre vends vend vendent vendait attendre attends attend attendent attendait
entendre entends entend entendent entendait répondre réponds répond répondent r
… [4578 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 9d5337ce -- tools/tests/linguistique/evaluer_gold.py tools/pensee/autotest.py | head -260", "description": "Show evaluer_gold and autotest v2 diff"}`

  ```
commit 9d5337ce1c23c4d70f51490d2fcdfa2c390e3faa
Author: Stéphane <stephane@localhost>
Date:   Thu Nov 5 14:14:38 2026 -0500

    B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180

diff --git a/tools/pensee/autotest.py b/tools/pensee/autotest.py
index ffb42e0d..da05e88c 100644
--- a/tools/pensee/autotest.py
+++ b/tools/pensee/autotest.py
@@ -2223,8 +2223,8 @@ def t153_attachement() -> tuple[bool, str]:
     import tools.bloc_linguistique as bl
     from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
     r = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
-    return (r["cibles"] == 239 and abs(r["top1_taux"] - 0.5272) < 0.001
-            and abs(r["exact_taux"] - 0.5146) < 0.001), (
+    return (r["cibles"] == 239 and abs(r["top1_taux"] - 0.5858) < 0.001
+            and abs(r["exact_taux"] - 0.5732) < 0.001), (
         f"attachement : top1 {r['top1_taux']}, exact {r['exact_taux']}, "
         f"couverture {r['couverture']}")
 
@@ -2341,7 +2341,7 @@ def t161_cible_proximite() -> tuple[bool, str]:
     from ..tests.linguistique.evaluer_gold import charger, eva
… [10532 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Preparing ablation copies in /tmp (heads, lexicon, segment rule).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '^fly\\|^swim\\|^wait\\|^belong\\|^close closes' tools/bloc_linguistique.py && sed -n '545,575p' tools/bloc_linguistique.py && git show a408a909:tools/bloc_linguistique.py | sed -n '845,885p'", "description": "Locate ablation … [32 caractères tronqués]`

  ```
416:fly flies flew flown flying climb climbs climbed climbing flow flows flowed flowing
417:swim swims swam swum swimming get gets got gotten getting smile smiles smiled smiling
418:wait waits waited waiting belong belongs belonged belonging
    def _modalite(phrase: str) -> bool:
        return bool(re.search(r"\b(?:peut|peuvent|peux|pouvons|pouvez|doit|doivent|devons|devez|"
                              r"pourrait|pourraient|pourrais|devrait|devraient|voudrais|voudrait|"
                              r"faut|falloir|might|may|must|should|could|would|can)\b", phrase, re.I))

    # -- POS ----------------------------------------------------------------
    def _pos(self, langue: str, mot: str) -> tuple[str, bool, float]:
        lex = POS_FERME.get(langue, POS_FERME["fr"])
        n = _normaliser(mot).split("'")[0].split("’")[0]
        for classe, mots in lex.items():
            if n in mots:
                return classe, False, 0.92
        if n in VERBES.get(langue, VERBES["fr"]):
            return "VERB", True, 0.72
        if n in ADJECTIFS.get(langue, ADJECTIFS["fr"]):
            return "ADJ", True, 0.68
        if re.fullmatch(r"\d+(?:[.,]\d+)*", mot):
            return
… [3562 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 80, "offset": 850}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
850:                                             self.nom, 0.25, candidats=["littéral", "figuré"],
851:                                             langue=lg, script=script))
852: 
853:         # 5. syntagmes : le générateur S (candidats) ou un chunker simple
854:         verbes = [(e.debut, e.fin, e.valeur) for e in etiquettes
855:                   if e.niveau == "pos" and e.type == "VERB"]
856:         cands = self._syntagmes_s(texte)
857:         cibles_s = self._cibles_s(texte) if cands else {}
858:         if cands:
859:             # les GV du chunker complètent ceux du générateur S : sans eux, un GP n'a aucun
860:             # candidat d'attachement (diagnostic des 33 échecs de T162).
861:             gvs_simple = [x for x in self._syntagmes_simple(texte, lg) if x["type"] == "GV"]
862:             for c in cands[:1]:
863:                 noms = [x.get("nom", "") for x in cands]
864:                 gvs_s = [x for x in c.get("segments", []) if x.get("type") == "GV"]
865:                 deja = {(x["debut"], x["fin"]) for x in gvs_s}
866:                 gvs = 
… [4931 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Running ablations to decompose the +6/+8/+45 gains.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/audit_v2/ablate.py <<'PY'\nimport importlib.util, json, pathlib, sys\nsys.path.insert(0, '.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\n\nSRC = pathlib. … [5585 caractères tronqués]`

  ```
exit=1
Traceback (most recent call last):
  File "/tmp/audit_v2/ablate.py", line 37, in <module>
    res['sans_tetes'] = measure(variant('sans_tetes', SRC.replace(head_block, '')))
                                ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/audit_v2/ablate.py", line 14, in variant
    spec.loader.exec_module(m)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "<frozen importlib._bootstrap_external>", line 1027, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/tmp/audit_v2/sans_tetes.py", line 58, in <module>
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
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  
… [818 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Fixing module registration and rerunning ablations.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np = pathlib.Path('/tmp/audit_v2/ablate.py')\ns = p.read_text()\ns = s.replace(\"    m = importlib.util.module_from_spec(spec)\\n    spec.loader.exec_module(m)\",\n              \"    m = importlib.ut … [776 caractères tronqués]`

  ```
exit=0
courant                    labels=145 top1=140 topk=142 exact=137 strict=141 | t1sp=0.9655 tksp=0.9793 exsp=0.9448 stsp=0.9724 | verbe 111/116 nom 26/29
sans_tetes                 labels=145 top1=140 topk=142 exact=137 strict=96 | t1sp=0.9655 tksp=0.9793 exsp=0.9448 stsp=0.6621 | verbe 111/116 nom 26/29
sans_lexique               labels=145 top1=132 topk=134 exact=129 strict=133 | t1sp=0.9103 tksp=0.9241 exsp=0.8897 stsp=0.9172 | verbe 103/116 nom 26/29
sans_segment_total         labels=145 top1=134 topk=142 exact=131 strict=141 | t1sp=0.9241 tksp=0.9793 exsp=0.9034 stsp=0.9724 | verbe 105/116 nom 26/29
sans_segment_regle_seule   labels=145 top1=134 topk=142 exact=131 strict=141 | t1sp=0.9241 tksp=0.9793 exsp=0.9034 stsp=0.9724 | verbe 105/116 nom 26/29
sans_genre_s_seul          labels=145 top1=140 topk=142 exact=137 strict=141 | t1sp=0.9655 tksp=0.9793 exsp=0.9448 stsp=0.9724 | verbe 111/116 nom 26/29
avant_a408a909             labels=145 top1=126 topk=134 exact=123 strict=88 | t1sp=0.869 tksp=0.9241 exsp=0.8483 stsp=0.6069 | verbe 97/116 nom 26/29
  ```

### 🤖 Assistant

⏵ Running the cited gates directly and counting the registry.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' 2>&1 | tee /tmp/audit_v2/portes.txt\nimport ast, pathlib, sys, time\np = pathlib.Path('tools/pensee/autotest.py')\ntree = ast.parse(p.read_text(encoding='utf-8'))\nmain = next(n for n in tree.body if isinstance(n, as … [981 caractères tronqués]`

  ```
portes listées : 180
noms : ['T0 store canonique', 'T1 rejeu', 'T1 graine', 'T1 DRVF thought', 'T2 stratégies'] ... ['T173 top-k strict', 'T174 convention documentée', 'T175 audit attachement', 'T176 segment précédent', 'T177 candidats têtes']
✅ t153_attachement | attachement : top1 0.5858, exact 0.5732, couverture 0.6067 (0.56s)
✅ t161_cible_proximite | proximité : top1 140/239, exact 137/239, tête 140/145 (0.44s)
✅ t162_candidats_verbes | candidats : top-k 142/239 (0.5941), tête 142/145 (0.43s)
✅ t163_echecs_attachement | échecs : 94 de span, 3 de cible (33 avant les correctifs) (0.42s)
✅ t164_verbe_gv | verbe du GV : saw (attendu saw) ; exact 137/239 (0.44s)
✅ t166_spans | spans : 48 REL, 33 SUB, 13 GP (0.42s)
✅ t167_denominateur | dénominateur : spans 0.9655 / 0.9793 / 0.9448 (0.45s)
✅ t168_classement | classement : exact 137/146 ; cibles 116 verbes, 29 noms (0.87s)
✅ t169_conventions | conventions : verbes 111/116 (0.9569), noms 26/29 (0.8966) (0.44s)
✅ t170_attachement_cible | ciblé : REL « homme » homme, GP « joue » joue (0.00s)
✅ t172_echecs_cible | échecs de cible : 3 hors candidats, 5 mal classés (0.43s)
✅ t173_topk_strict | top-k : 142 sous-chaîne, 141 exacts (0.9724) (0
… [210 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Launching the full 180-gate registry in the background while I verify the raw counts.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (time python3 tools/pensee/autotest.py) > /tmp/audit_v2/autotest_full.txt 2>&1; echo \"exit=$?\" >> /tmp/audit_v2/autotest_full.txt", "description": "Run full autotest gate registry", "run_in_background": true}`

  ```
started background job bash-1063
  ```

### 🤖 Assistant

⏵ Computing independent counts: failures, spans, POS split, SUB convention.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' > /tmp/audit_v2/comptes.json\nimport sys, json, collections\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\nph = charger()\nh = bl.Heuristique … [3076 caractères tronqués]`

  ```
sources {'hand': 20, 'reel': 432, 'synthetique': 160} phrases 612 segments 1863
labels 145 fail 8 spans {'GP': 13, 'SUB': 33, 'REL': 48} spans_all {'GP': 96, 'SUB': 69, 'REL': 74}
split {'NOM': 29, 'VERB': 116} missing []
SUB pos {'VERB': 36}
taux {'top1_span': 0.9655, 'topk_span': 0.9793, 'exact_span': 0.9448, 'strict_span': 0.9724, 'top1/239': 0.5858, 'topk/239': 0.5941, 'exact/239': 0.5732}
--- échecs ---
g002  GP  gold='chat'             pred=''                 pos=NOUN strict=False substr=False cands=['GP']
g012  GP  gold='prêt'             pred='manger'           pos=ADJ strict=True substr=True cands=['« à manger » → Le canard', '« à manger » → est prêt', 'manger', 'est', 'canard', 'prêt']
r018  GP  gold='prête'            pred='manger'           pos=ADJ strict=True substr=True cands=['« à manger » → La souris', '« à manger » → est prête', 'manger', 'est', 'souris', 'prête']
r230  SUB gold='appelle'          pred='appelle-moi'      pos=VERB strict=False substr=True cands=['structure la plus proche', 'appelle-moi']
r309  SUB gold='viendra'          pred='Peut-être'        pos=VERB strict=False substr=False cands=['structure la plus proche', 'Peut-être']
s041  GP  gold='marche'
… [383 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-1063 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (time python3 tools/pensee/autotest.py) > /tmp/audit_v2/autotest_full.txt 2>&1; echo "exit=$?" >> /tmp/audit_v2/autotest_full.txt) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Full registry finished; checking it and the 69/69 SUB convention.

- **bash** `{"command": "tail -8 /tmp/audit_v2/autotest_full.txt && grep -c '✅' /tmp/audit_v2/autotest_full.txt && grep '❌' /tmp/audit_v2/autotest_full.txt | head", "description": "Check full autotest result"}`

  ```
File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", line 32, in <module>
    from .coeur import Candidat, Etat
ImportError: attempted relative import with no known parent package

real	0m0,119s
user	0m0,102s
sys	0m0,017s
exit=1
0
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\nph=charger(); h=bl.Heuristique()\nsub=collections.Counter(); allsub=[ … [3014 caractères tronqués]`

  ```
cibles par type {'GP': 96, 'SUB': 69, 'REL': 74}
SUB POS (tous, 69) : {'VERB': 69} total 69
SUB non-VERB: []
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 36, in <module>
  File "<stdin>", line 31, in split_lex
AttributeError: 'Heuristique' object has no attribute '_est_verbe'
[exit code: 1]
  ```

### 🤖 Assistant

⏵ Fixing the gate runner invocation and the `_est_verbe` reference.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (time python3 -m tools.pensee.autotest) > /tmp/audit_v2/autotest_full.txt 2>&1; echo \"exit=$?\" >> /tmp/audit_v2/autotest_full.txt; tail -5 /tmp/audit_v2/autotest_full.txt; echo '--- échecs ---'; grep '❌' /tmp/audit_v2/autotest_full … [59 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-1077]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, collections, importlib.util, pathlib, subprocess\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\nph=charger()\ndef split_lex(bloc … [2242 caractères tronqués]`

  ```
split _est_verbe courant : (71, 71, 1.0, 74, 66, 0.8919)
split _est_verbe ancien bloc : (71, 60, 0.8451, 74, 63, 0.8514)
split POS gold ancien bloc : (116, 97, 0.8362, 29, 26, 0.8966)
split POS gold courant : (116, 111, 0.9569, 29, 26, 0.8966)
  ```

### 🤖 Assistant

⏵ Verifying the historical 63/82 split with the old lexicon.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, importlib.util, pathlib, subprocess\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\nph=charger()\nold=subprocess.run(['git','show … [1471 caractères tronqués]`

  ```
ancien bloc + ancien _est_verbe : (41, 0, 0.0, 36, 0, 0.0)
ancien bloc + courant _est_verbe: (49, 0, 0.0, 28, 0, 0.0)
courant bloc + courant _est_verbe: (71, 71, 1.0, 74, 66, 0.8919)
courant bloc + ancien _est_verbe: (63, 63, 1.0, 82, 74, 0.9024)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 9d5337ce -- tools/tests/linguistique/gold_reel.py | head -40 && echo '--- old convention ---' && git show a408a909:tools/tests/linguistique/gold_reel.py | sed -n '20,40p'", "description": "Check old CONVENTION_CIBLE text"}`

  ```
commit 9d5337ce1c23c4d70f51490d2fcdfa2c390e3faa
Author: Stéphane <stephane@localhost>
Date:   Thu Nov 5 14:14:38 2026 -0500

    B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180

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
 #   - **GP** : la cible est le **verbe qui gouverne** le comp
… [2608 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Debugging the odd old-bloc manual loop; verifying the 63/82 provenance.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, importlib.util, pathlib, subprocess\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\nph=charger()\nold=subprocess.ru … [1515 caractères tronqués]`

  ```
evaluer_bloc old labels/exact/top1: 77 0 0
manual labels 77 avec attachement 0
extrait: [('GN', None)]
ancien _est_verbe sur chat/mange/écoute: False True True
--- old convention ---
  ```

### 🤖 Assistant

⏵ Investigating why the pre-v2 copy scores differently across runs.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l /tmp/audit_v2/bloc_avant*.py && diff -q /tmp/audit_v2/bloc_avant.py /tmp/audit_v2/bloc_avant2.py; echo '--- rerun ablate (just old) ---'; python3 - <<'PY'\nimport sys, importlib.util, pathlib\nsys.path.insert(0,'.')\nfrom tools … [554 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 99032  5 nov 14:36 /tmp/audit_v2/bloc_avant2.py
-rw-r--r--. 1 stephane stephane 99032  5 nov 14:29 /tmp/audit_v2/bloc_avant.py
--- rerun ablate (just old) ---
bloc_avant.py labels 77 top1 0 exact 0 topk 0 strict 0
bloc_avant2.py labels 77 top1 0 exact 0 topk 0 strict 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, importlib.util, pathlib\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\nprint('courant:', {k:evaluer_bloc('h',bl.He … [536 caractères tronqués]`

  ```
courant: {'labels': 145, 'top1': 140, 'exact': 137}
bloc_avant.py après courant: labels 145 top1 126 exact 123
bloc_avant2.py après courant: labels 145 top1 126 exact 123
  ```

### 🤖 Assistant

⏵ Finding the warm-up dependency in the S generator (reproducibility risk).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && globout=$(find tools -name 'generateur.py' -o -name 'generateur*.py' | head); echo \"$globout\"; grep -rn 'lru_cache\\|_CACHE\\|cache\\|^S \\|^_S\\|global ' tools/structures/generateur.py 2>/dev/null | head -40", "description": "Loca … [30 caractères tronqués]`

  ```
tools/structures/generateur.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git ls-tree a408a909 tools/structures && git ls-tree HEAD tools/structures && git -C tools/structures status --porcelain | head && git -C tools/structures log --oneline -3 | cat", "description": "Check submodule commits across versio … [4 caractères tronqués]`

  ```
160000 commit 523d8c1e8c6ca29ca415360a71bfab6c5b56102c	tools/structures
160000 commit 523d8c1e8c6ca29ca415360a71bfab6c5b56102c	tools/structures
 M donnees/paragraphes-validations.jsonl
523d8c1 S — LE FAIT DIVERS EST TRANCHÉ : 61/61 TYPES, 144/144 RÔLES ; LA TÊTE DU GN ARRÊTE LE VERBE
4012729 S — LA BANQUE DE PARAGRAPHES PASSE À NEUF : SIX PAIRES D'ALICE, SOURCES ANGLAISES ET RÉFÉRENTS
7ccc60f S — VALIDATION HUMAINE : 8 VERDICTS DE RÉFÉRENTS SUR /PARAGRAPHES (a001–a003) + 8 VERDICTS BANQUE (p003, c010, c066, c067)
  ```

### 🤖 Assistant

⏵ Checking whether the old copy can import `generateur` cold (sys.path setup).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'structures\\|sys.path' tools/bloc_linguistique.py | head -20 && echo '--- old ---' && grep -n 'structures\\|sys.path' /tmp/audit_v2/bloc_avant2.py | head -20 && echo '--- generateur imports ---' && sed -n '1,50p' tools/struc … [84 caractères tronqués]`

  ```
595:            if str(RACINE / "tools/structures") not in sys.path:
596:                sys.path.insert(0, str(RACINE / "tools/structures"))
--- old ---
592:            if str(RACINE / "tools/structures") not in sys.path:
593:                sys.path.insert(0, str(RACINE / "tools/structures"))
--- generateur imports ---
#!/usr/bin/env python3
"""generateur.py — une phrase brute → des structures candidates (v0 heuristique).

Ce n'est pas un analyseur syntaxique : c'est un **générateur de candidats** à faire valider par
un humain. Il segmente (GN, GV, GP, REL, SUB), devine des rôles par la préposition, puis produit
plusieurs candidats en variant l'**attachement** de chaque segment ambigu (GN le plus proche ou
GV le plus proche).

    python3 generateur.py "Le chat de la voisine qui dort sur le toit se réveille."
    python3 generateur.py --json "..."     # la structure complète
"""
from __future__ import annotations

import json
import re
import unicodedata

DET = set("le la les l un une ce cet cette ces mon ma mes ton ta tes son sa ses "
          "notre nos votre vos leur leurs quel quelle quels quelles".split())
PREP = set("a au aux de du des d en dans par pour sur sous avec sans
… [2181 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '580,605p' /tmp/audit_v2/bloc_avant2.py && echo '--- current ---' && sed -n '583,608p' tools/bloc_linguistique.py", "description": "Read _syntagmes_s path setup"}`

  ```
break
        for pre in PREFIXES:
            if len(n) > len(pre) + 2 and n.startswith(pre):
                sortie.append(("préfixe", 0, len(pre), pre))
                break
        return sortie

    # -- syntagmes ----------------------------------------------------------
    def _syntagmes_s(self, texte: str) -> list[dict] | None:
        if not self.segmenter_s:
            return None
        try:
            if str(RACINE / "tools/structures") not in sys.path:
                sys.path.insert(0, str(RACINE / "tools/structures"))
            import generateur  # le générateur S, importé en lecture seule
            return generateur.analyser(texte)
        except Exception:
            return None

    def _cibles_s(self, texte: str) -> dict:
        """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).

        Lecture seule de l'API interne du S : `_tokens`/`_segmente` rendent les `Segment` avec
        `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
        (GP, puis GN, puis GV), comme le premier candidat de `analyser`.
        """
--- current ---
                break
        for pre in PREFIXES:
            
… [1073 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-1077 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (time python3 -m tools.pensee.autotest) > /tmp/audit_v2/autotest_full.txt 2>&1; echo "exit=$?" >> /tmp/audit_v2/autotest_full.txt; tail -5 /tmp/audit_v2/autotest_full.txt; echo '--- échecs ---'; grep '❌' /tmp/audit_v2/autotest_full.txt | head) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Reading the full gate run and tracing the cold S-generator failure.

- **bash** `{"command": "tail -6 /tmp/audit_v2/autotest_full.txt; echo '--- ❌ ---'; grep '❌' /tmp/audit_v2/autotest_full.txt | head; echo '--- count ✅ ---'; grep -c '✅' /tmp/audit_v2/autotest_full.txt", "description": "Read full autotest results"}`

  ```
181/181 portes tenues

real	5m17,375s
user	5m17,013s
sys	0m0,305s
exit=0
--- ❌ ---
--- count ✅ ---
181
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, importlib.util, pathlib, traceback\nsys.path.insert(0,'.')\np=pathlib.Path('/tmp/audit_v2/bloc_avant2.py')\nspec=importlib.util.spec_from_file_location('bloc_avant2',p); m=importlib.util.module_from_spec … [579 caractères tronqués]`

  ```
segmenter_s True
_syntagmes_s cold -> None
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 11, in <module>
ModuleNotFoundError: No module named 'generateur'
  ```

### 🤖 Assistant

⏵ Checking the A2 diagnostic’s 46/57 claim and the A3 learned-model numbers.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '46\\|57\\|45\\|tête' reports/rapport-topk-diagnostic.md | head -40 && echo '=== A3 ===' && sed -n '1,90p' reports/rapport-classement-appris.md", "description": "Read A2 top-k and A3 learned-model reports"}`

  ```
1:# B13 — le top-k strict de l'attachement : 57 échecs, dont 45 d'emballage
4:> **Verdict** : ✅ **les 57 échecs du top-k strict sont qualifiés** (0 « autre »). Sur les
5:> **145 segments gold dont le span est prédit**, la cible est dans les candidats **134 fois en
6:> sous-chaîne** (0,9241) mais **88 fois en égalité exacte** (0,6069) : **57 échecs**. **45** sont
7:> des **candidats du générateur S non réduits à leur tête** — la cible est déjà dans la chaîne
8:> « « segment » → … », il suffit d'en extraire la tête ; **8** sont des **verbes anglais hors
10:> Le **top-1 est déjà juste 41 fois sur 57** : le top-k strict mesure surtout l'**emballage** des
12:> **45 + 8 + 4 = 57** — borne haute, mesurée sur le même gold.
17:> (57 lignes, une par échec) · script de diagnostic exécuté par heredoc, **lecture seule** :
22:Gold de **612 phrases** (20 `hand` + 432 `reel` + 160 `synthetique`), **239 cibles**, **145
25:| mesure (sur 145 segments au bon span) | valeur | taux |
29:| **échecs stricts** | **57** | 0,3931 |
31:| top-1 exact (rendement sur les 145) | 123 | 0,8483 |
35:de span : **145/239 = 0,6067**, même si les 57 échecs sont tous réparés.
37:**Ce que ça dit.** L'écart 134 − 88 = **46
… [11627 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, importlib.util, pathlib\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\nph=charger()\n# old bloc with RACINE corrected, cold\nold … [1470 caractères tronqués]`

  ```
old bloc cold RACINE fix: labels 145 fail 22 strict 123
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 31, in <module>
  File "<stdin>", line 28, in tete
AttributeError: type object 'Heuristique' has no attribute '_tete_texte'
[exit code: 1]
  ```

### 🤖 Assistant

⏵ Verifying the disputed “46 of 57” figure against the A2 diagnostic.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, importlib.util, pathlib\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\nph=charger()\nspec=importlib.util.spec_from_file_location … [1469 caractères tronqués]`

  ```
old: labels 145 exact 123 fail 22
échecs avec tête candidate == cible : 4 / 57
détail: [('g012', 'GP', 'prêt'), ('r018', 'GP', 'prête'), ('s108', 'GP', 'rêve'), ('s122', 'GP', 'saute')]
échecs sous-chaîne (cible dans un candidat) : 11 ; échecs stricts : 22
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, importlib.util, pathlib\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\nph=charger()\nspec=importlib.util.spec_from_file_location … [1399 caractères tronqués]`

  ```
labels 145 strict_fail 57
tête candidate == cible : 45 / 57
par type des réparables: Counter({'REL': 26, 'GP': 19})
ids: ['g011', 'g012', 'r014', 'r015', 'r018', 'r047', 'r054', 'r055', 'r057', 'r088', 'r094', 'r095', 'r100', 'r126', 'r139', 'r150', 'r201', 'r203', 'r209', 'r213', 'r221', 'r226', 'r228', 'r231', 'r233', 'r235', 'r253', 'r257', 'r259', 'r261', 'r263', 'r265', 'r267', 'r269', 'r275', 's045', 's047', 's058', 's064', 's108', 's109', 's120', 's122', 's144', 's150']
  ```

### 🤖 Assistant

⏵ Rebuilding the A2 ladder (F1 heads, F2 lexicon) on the pre-v2 base.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, importlib.util, pathlib\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as cur\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\nold_src=pathlib.Path('/tmp/audit_v2/bloc_a … [2331 caractères tronqués]`

  ```
old_F1 {'labels': 145, 'top1': 126, 'topk': 134, 'exact': 123, 'topk_exact': 133} | span 0.8483
old_F1_F2 {'labels': 145, 'top1': 134, 'topk': 142, 'exact': 131, 'topk_exact': 141} | span 0.9034
  ```

### 🤖 Assistant

⏵ Counting gates at the v2 commit and HEAD, and identifying the added gate.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for c in 9d5337ce 2e08cbc7 de292c7d; do echo \"=== $c ===\"; git show $c:tools/pensee/autotest.py > /tmp/audit_v2/at_$c.py; python3 - \"$c\" <<'PY'\nimport ast,sys\nc=sys.argv[1]\nt=ast.parse(open(f'/tmp/audit_v2/at_{c}.py').read())\ … [510 caractères tronqués]`

  ```
=== 9d5337ce ===
=== 2e08cbc7 ===
=== de292c7d ===
=== diff autotest 9d5337ce..HEAD ===
diff --git a/tools/pensee/autotest.py b/tools/pensee/autotest.py
index da05e88c..f4331ec6 100644
--- a/tools/pensee/autotest.py
+++ b/tools/pensee/autotest.py
@@ -2596,6 +2596,26 @@ def t177_candidats_tete() -> tuple[bool, str]:
         f"candidats têtes : {a['topk_exact']}/145 ({a['topk_exact_taux_span']})")
 
 
+def t178_cache_chunker() -> tuple[bool, str]:
+    """Le cache du chunker : un seul `_syntagmes_simple` par analyse (1+2S → 1)."""
+    import tools.bloc_linguistique as bl
+    appels = {"n": 0}
+    orig = bl.Heuristique._syntagmes_simple
+
+    def compte(self, *a, **k):
+        appels["n"] += 1
+        return orig(self, *a, **k)
+
+    bl.Heuristique._syntagmes_simple = compte
+    try:
+        h = bl.Heuristique(segmenter_s=False)
+        h.analyser(" ".join(["Le garçon joue au ballon dans le jardin."] * 20), "fr")
+    finally:
+        bl.Heuristique._syntagmes_simple = orig
+    return appels["n"] == 1, (
+        f"cache : {appels['n']} chunking(s) pour 20 répétitions (1+2S avant)")
+
+
 def main() -> int:
     portes = [("T0 store canonique", t0_store()), ("T1 rejeu", t1
… [1035 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for c in 9d5337ce 2e08cbc7 de292c7d; do git show $c:tools/pensee/autotest.py > /tmp/audit_v2/at_$c.py; python3 - \"$c\" <<'PY'\nimport ast,sys\nc=sys.argv[1]\nt=ast.parse(open(f'/tmp/audit_v2/at_{c}.py').read())\nfor n in t.body:\n   … [385 caractères tronqués]`

  ```
9d5337ce portes: 180 | derniers: ['T175 audit attachement', 'T176 segment précédent', 'T177 candidats têtes']
2e08cbc7 portes: 180 | derniers: ['T175 audit attachement', 'T176 segment précédent', 'T177 candidats têtes']
de292c7d portes: 180 | derniers: ['T175 audit attachement', 'T176 segment précédent', 'T177 candidats têtes']
  ```

### 🤖 Assistant

⏵ Resolving the 180 vs 181 discrepancy in the registry count.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport ast\nfor label, path in [('worktree','tools/pensee/autotest.py'), ('HEAD','/tmp/audit_v2/at_de292c7d.py')]:\n    src=open(path).read()\n    t=ast.parse(src)\n    main=next(n for n in t.body if isinstance(n,as … [726 caractères tronqués]`

  ```
worktree direct assign len 181
  last 5: ['T174 convention documentée', 'T175 audit attachement', 'T176 segment précédent', 'T177 candidats têtes', 'T178 cache chunker']
worktree T178 count 1 portes.append 0
HEAD direct assign len 180
  last 5: ['T173 top-k strict', 'T174 convention documentée', 'T175 audit attachement', 'T176 segment précédent', 'T177 candidats têtes']
HEAD T178 count 0 portes.append 0
2:"""autotest.py — les portes du moteur de pensée : T0–T4, puis AC-3 et alpha-bêta.
1944:    """Le gold gelé : 602 phrases, les portes ne cassent plus."""
2620:    portes = [("T0 store canonique", t0_store()), ("T1 rejeu", t1_rejeu()),
2798:    for nom, (ok, msg) in portes:
2801:    print(f"  {len(portes) - échecs}/{len(portes)} portes tenues")
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git rev-parse HEAD && git show HEAD:tools/pensee/autotest.py | grep -c 'T178' ; git diff 9d5337ce..HEAD -- tools/pensee/autotest.py | grep -c 'T178' ; git status --porcelain tools/pensee/autotest.py ; git diff --stat HEAD -- tools/pe … [108 caractères tronqués]`

  ```
a2def5eeea5c54cb67397c68777f2ff5f5fc7cf1
1
1
a2def5eeea5c54cb67397c68777f2ff5f5fc7cf1 PILOTAGE — LE CACHE DU CHUNKER AU JOURNAL ; T0 DANS LE BUDGET ; 181/181
  ```

### 🤖 Assistant

⏵ Running the 1000-draw permutation and random-candidate controls on v2.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' > /tmp/audit_v2/controles.json\nimport sys, json, random, statistics, importlib.util, pathlib\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\n … [2572 caractères tronqués]`

  ```
{
 "v2": {
  "labels": 145,
  "exact": 137,
  "permutation": {
   "tirages": 1000,
   "observe": 137,
   "moyenne": 1.786,
   "ecart_type": 1.3469,
   "min": 0,
   "max": 8,
   "p_empirique": 0.0,
   "ratio": 76.708
  },
  "candidat_aleatoire": {
   "tirages": 1000,
   "observe": 137,
   "moyenne": 58.566,
   "ecart_type": 5.517,
   "min": 42,
   "max": 75,
   "p_empirique": 0.0,
   "ratio": 2.339
  },
  "topk_sous_chaine": 142,
  "topk_strict": 141
 },
 "sans_tetes": {
  "labels": 145,
  "exact": 137,
  "permutation": {
   "tirages": 1000,
   "observe": 137,
   "moyenne": 1.786,
   "ecart_type": 1.3469,
   "min": 0,
   "max": 8,
   "p_empirique": 0.0,
   "ratio": 76.708
  },
  "candidat_aleatoire": {
   "tirages": 1000,
   "observe": 137,
   "moyenne": 43.742,
   "ecart_type": 4.6177,
   "min": 30,
   "max": 58,
   "p_empirique": 0.0,
   "ratio": 3.132
  }
 }
}
  ```

### 🤖 Assistant

⏵ Compiling the per-type breakdown and split-matrix evidence.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' > /tmp/audit_v2/detail.json\nimport sys, json, collections, importlib.util, pathlib\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger\nph=charger … [3127 caractères tronqués]`

  ```
courant {"GP": {"labels": 83, "exact": 77, "top1": 77, "topk_sub": 81, "topk_strict": 81}, "SUB": {"labels": 36, "exact": 34, "top1": 35, "topk_sub": 35, "topk_strict": 34}, "REL": {"labels": 26, "exact": 26, "top1": 26, "topk_sub": 26, "topk_strict": 26}}
avant   {"GP": {"labels": 83, "exact": 69, "top1": 69, "topk_sub": 73, "topk_strict": 54}, "SUB": {"labels": 36, "exact": 28, "top1": 29, "topk_sub": 35, "topk_strict": 34}, "REL": {"labels": 26, "exact": 26, "top1": 26, "topk_sub": 26}}
matrice avant {"lex=True,pos=True": {"n": 63, "justes": 60}, "lex=True,pos=False": {"n": 0, "justes": 0}, "lex=False,pos=True": {"n": 53, "justes": 37}, "lex=False,pos=False": {"n": 29, "justes": 26}}
matrice courant {"lex=True,pos=True": {"n": 71, "justes": 71}, "lex=True,pos=False": {"n": 0, "justes": 0}, "lex=False,pos=True": {"n": 45, "justes": 40}, "lex=False,pos=False": {"n": 29, "justes": 26}}
fails courant:
  ['g002', 'GP', 'chat', '', False, False]
  ['g012', 'GP', 'prêt', 'manger', True, True]
  ['r018', 'GP', 'prête', 'manger', True, True]
  ['r230', 'SUB', 'appelle', 'appelle-moi', False, True]
  ['r309', 'SUB', 'viendra', 'Peut-être', False, False]
  ['s041', 'GP', 'marche', '', Fals
… [104 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reconciling a discrepancy in the pre-v2 top-k strict count (88 vs 114).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, importlib.util, pathlib, collections\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\nspec=importlib.util.spec_from_file_location('bloc_avant_x',pathlib.P … [1279 caractères tronqués]`

  ```
evaluer_bloc old: {'labels': 145, 'top1': 126, 'topk': 134, 'exact': 123, 'topk_exact': 88}
loop old: n 145 sub 134 strict 88 by {'GP': 54, 'SUB': 34}
evaluer_bloc old 2e: {'labels': 145, 'top1': 126, 'topk': 134, 'exact': 123, 'topk_exact': 88}
  ```

### 🤖 Assistant

⏵ Re-measuring each variant in isolated processes for a clean per-type table.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/audit_v2/measure_variant.py <<'PY'\nimport sys, json, pathlib, collections\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\npath = sys.argv[1]\nif path == 'current':\n    im … [2352 caractères tronqués]`

  ```
current                  top1=140 topk=142 exact=137 strict=141 | exact GP/SUB/REL=77/34/26 | strict GP/SUB/REL=81/34/26 | labels=83/36/26
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
KeyError: 'strict'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nfor line in open('/tmp/audit_v2/variants.jsonl'):\n    d=json.loads(line); t=d['totaux']; pt=d['par_type']\n    g=lambda typ,k: pt.get(typ,{}).get(k,0)\n    print(f\"{d['path'].split('/')[-1]:24s} top1= … [421 caractères tronqués]`

  ```
current                  top1=140 topk=142 exact=137 strict=141 | exact GP/SUB/REL=77/34/26 | strict GP/SUB/REL=81/34/26 | labels=83/36/26
bloc_avant2.py           top1=126 topk=134 exact=123 strict= 88 | exact GP/SUB/REL=69/28/26 | strict GP/SUB/REL=54/34/0 | labels=83/36/26
old_F1.py                top1=126 topk=134 exact=123 strict=133 | exact GP/SUB/REL=69/28/26 | strict GP/SUB/REL=73/34/26 | labels=83/36/26
old_F1_F2.py             top1=134 topk=142 exact=131 strict=141 | exact GP/SUB/REL=77/28/26 | strict GP/SUB/REL=81/34/26 | labels=83/36/26
sans_tetes.py            top1=140 topk=142 exact=137 strict= 96 | exact GP/SUB/REL=77/34/26 | strict GP/SUB/REL=62/34/0 | labels=83/36/26
sans_lexique.py          top1=132 topk=134 exact=129 strict=133 | exact GP/SUB/REL=69/34/26 | strict GP/SUB/REL=73/34/26 | labels=83/36/26
sans_segment_total.py    top1=134 topk=142 exact=131 strict=141 | exact GP/SUB/REL=77/28/26 | strict GP/SUB/REL=81/34/26 | labels=83/36/26
7 /tmp/audit_v2/variants.jsonl
  ```

### 🤖 Assistant

⏵ Checking target-token ambiguity and multi-target segments.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, collections, json\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger\nph=charger()\nmulti=0; multi_lab=0; ambiguous=[]; absent=0; occ=collections.Counter()\nfor p in ph:\n … [1648 caractères tronqués]`

  ```
segments avec cibles>1 : 43 / 239
cibles absentes des tokens : 0
occurrences du texte cible : {1: 238, 2: 1}
cibles avec POS ambigu (plusieurs POS) : 0
labels avec cibles>1 : 36 /145
labels avec POS ambigu : 0
  ```

### 🤖 Assistant

⏵ Inspecting the learned-model script to see if its block is replayable.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'def main\\|__main__\\|argparse\\|def charger\\|def evaluer\\|def entrainer\\|def cross\\|def bootstrap\\|mcnemar' tools/tests/linguistique/classement_cible.py | head -40 && echo '--- JSON keys ---' && python3 - <<'PY'\nimpor … [299 caractères tronqués]`

  ```
53:import argparse
285:def entrainer(segments: list[dict], epochs: int = 6000, lr: float = 0.6,
359:def evaluer(modele: list[float], segments: list[dict]) -> dict:
375:def evaluer_regle(segments: list[dict]) -> dict:
390:def evaluer_hasard(segments: list[dict], rng: random.Random) -> dict:
399:def _mcnemar_exact(b: int, c: int) -> float:
453:    def entrainer_sur(parite: int):
517:    mcnemar = {"modele_juste_regle_fausse": b, "regle_juste_modele_fausse": c,
518:               "p_exact": _mcnemar_exact(b, c)}
678:            "mcnemar": mcnemar,
700:def main() -> int:
701:    ap = argparse.ArgumentParser(description=__doc__,
702:                                 formatter_class=argparse.RawDescriptionHelpFormatter)
742:    print("McNemar:", resultat["controle_negatif"]["mcnemar"])
758:if __name__ == "__main__":
--- JSON keys ---
['titre', 'date', 'graine', 'empreinte_bloc_linguistique', 'note_regle_actuelle', 'hyperparametres', 'corpus', 'protocole', 'features', 'poids', 'resultats', 'controle_negatif', 'stabilite_decoupages_aleatoires', 'limites', 'segments']
resultats {"sens": {"pairs->impairs": {"entrainement": {"segments": 79, "lignes": 224, "positifs": 79, "negatifs": 145, "epoc
… [685 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '700,758p' tools/tests/linguistique/classement_cible.py", "description": "Read learned-model CLI main"}`

  ```
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", default=str(SORTIE_DEFAUT),
                    help="chemin du JSON de résultat (défaut : reports/pensee-classement-appris.json)")
    ap.add_argument("--graine", type=int, default=0)
    ap.add_argument("--stabilite", type=int, default=10,
                    help="nombre de découpages aléatoires (0 pour désactiver)")
    ap.add_argument("--epochs", type=int, default=6000)
    ap.add_argument("--lr", type=float, default=0.6)
    ap.add_argument("--l2", type=float, default=0.01)
    ap.add_argument("--verbeux", action="store_true")
    args = ap.parse_args()

    phrases = charger()
    resultat = executer(phrases, graine=args.graine, stabilite=args.stabilite,
                        epochs=args.epochs, lr=args.lr, l2=args.l2)

    sortie = pathlib.Path(args.json)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n",
                      encoding="utf-8")

    r = resultat["resultats"]
    print("== corpus ==")
   
… [1939 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Launching the learned-model replay to /tmp and checking post-v2 code drift.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (time python3 tools/tests/linguistique/classement_cible.py --json /tmp/audit_v2/classement_rejoue.json) > /tmp/audit_v2/classement.txt 2>&1; echo \"exit=$?\" >> /tmp/audit_v2/classement.txt", "description": "Replay learned-model clas … [39 caractères tronqués]`

  ```
started background job bash-1254
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo '--- HEAD ---' && git rev-parse HEAD && git log -1 --format='%h %s' | cat && echo '--- drift 9d5337ce..HEAD ---' && git diff --stat 9d5337ce..HEAD -- tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/test … [306 caractères tronqués]`

  ```
--- HEAD ---
1ec7286c0aed1bdb64379b96b093c47d7ef554b5
1ec7286c PILOTAGE — LES QUATRE VAGUES DE SOUS-AGENTS DOCUMENTÉES (§ 9) ; VAGUES 3 ET 4 EN COURS
--- drift 9d5337ce..HEAD ---
 tools/bloc_linguistique.py | 48 ++++++++++++++++++++++++++++++++--------------
 tools/pensee/autotest.py   | 23 +++++++++++++++++++++-
 2 files changed, 56 insertions(+), 15 deletions(-)
--- status measured files ---
  ```

### 🤖 Assistant

⏵ Post-v2 drift detected in the measured block; isolating the exact v2 blob.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff 9d5337ce..HEAD -- tools/bloc_linguistique.py | head -220", "description": "Show post-v2 changes to bloc_linguistique"}`

  ```
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 5cc3858f..07a41ec9 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -657,9 +657,21 @@ class Heuristique:
                     return v
         return None if strict else (mots[-1][1] if mots else None)
 
+    @staticmethod
+    def _verbe_gv(texte: str, g: dict, verbes, cache: dict | None = None):
+        """`_verbe_dans` mémoïsé par span de GV : le même GV est relu pour chaque segment."""
+        cle = (g["debut"], g["fin"])
+        if cache is not None and cle in cache:
+            return cache[cle]
+        v = Heuristique._verbe_dans(texte, g["debut"], g["fin"], verbes)
+        if cache is not None:
+            cache[cle] = v
+        return v
+
     @staticmethod
     def _cible_proche(texte: str, segment: dict, gvs: list[dict],
-                      verbes: list[tuple[int, int, str]] | None = None) -> str | None:
+                      verbes: list[tuple[int, int, str]] | None = None,
+                      cache: dict | None = None) -> str | None:
         """La cible d'un segment : le **verbe du GV le plus proche** (règle de proximité).
 
         Rend `None` si le 
… [6451 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Replaying the exact v2 blob (9d5337ce) rather than the drifted HEAD.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 9d5337ce:tools/bloc_linguistique.py > /tmp/audit_v2/bloc_v2.py && python3 - <<'PY'\nimport sys, importlib.util, pathlib, json\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\n … [604 caractères tronqués]`

  ```
{
 "cibles": 239,
 "labels": 145,
 "top1": 140,
 "topk": 142,
 "exact": 137,
 "topk_exact": 141,
 "top1_taux": 0.5858,
 "topk_taux": 0.5941,
 "exact_taux": 0.5732,
 "top1_taux_span": 0.9655,
 "topk_taux_span": 0.9793,
 "exact_taux_span": 0.9448,
 "topk_exact_taux_span": 0.9724,
 "verbe": {
  "cibles": 116,
  "justes": 111,
  "taux": 0.9569
 },
 "nom": {
  "cibles": 29,
  "justes": 26,
  "taux": 0.8966
 },
 "couverture": 0.6067
}
  ```

### 👤 Utilisateur

background job bash-1254 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (time python3 tools/tests/linguistique/classement_cible.py --json /tmp/audit_v2/classement_rejoue.json) > /tmp/audit_v2/classement.txt 2>&1; echo "exit=$?" >> /tmp/audit_v2/classement.txt) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Replaying v2 ablations and checking the learned-model result.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\nSRC=pathlib.Path('/tmp/audit_v2/bloc_v2.py').read_text(encoding='utf-8')\nhead='''                    # la **tête** de chaque candidat S (« « … » → Le livre » → livre ; « … → Les\n                    … [3766 caractères tronqués]`

  ```
written ['v2_sans_tetes', 'v2_sans_lexique', 'v2_sans_segment', 'v2_sans_genre']
bloc_v2.py             top1=140 topk=142 exact=137 strict=141 | span 0.9655/0.9793/0.9448/0.9724
v2_sans_tetes.py       top1=140 topk=142 exact=137 strict= 96 | span 0.9655/0.9793/0.9448/0.6621
v2_sans_lexique.py     top1=132 topk=134 exact=129 strict=133 | span 0.9103/0.9241/0.8897/0.9172
v2_sans_segment.py     top1=134 topk=142 exact=131 strict=141 | span 0.9241/0.9793/0.9034/0.9724
v2_sans_genre.py       top1=140 topk=142 exact=137 strict=141 | span 0.9655/0.9793/0.9448/0.9724
=== classement appris ===
== par sens ==
pairs->impairs: modèle 66/66 (1.0000) | règle 64/66 (0.9697) | hasard 0.3485
impairs->pairs: modèle 76/79 (0.9620) | règle 73/79 (0.9241) | hasard 0.3671
== regroupé hors-pli ==
modèle 142/145 (0.9793) | règle 137/145 (0.9448)
moyenne des sens: {'modele': 0.981, 'regle_actuelle': 0.9469, 'gain': 0.0341}
McNemar: {'modele_juste_regle_fausse': 7, 'regle_juste_modele_fausse': 2, 'p_exact': 0.179688}
bootstrap: {'tirages': 2000, 'difference': 0.0345, 'ic95': [-0.0069, 0.0759]}
hasard vivier attendu: 0.3876
repères: {'exactitude_entrainement': 0.9931, 'rang0_justes': 139, 'rang0_taux': 0.958
… [742 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extracting exact gate docstrings and assertion expectations for the stale-gate table.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, inspect\nsys.path.insert(0,'.')\nfrom tools.pensee import autotest as at\nfor n in ['t153_attachement','t161_cible_proximite','t162_candidats_verbes','t163_echecs_attachement','t164_verbe_gv','t166_spans … [319 caractères tronqués]`

  ```
### t153_attachement
L'attachement sur le gold 612 (239 cibles) : top1 0,5272, exact 0,5105.
### t161_cible_proximite
La cible par proximité : le verbe du GV le plus proche.
### t162_candidats_verbes
Les candidats verbes : le top-k passe de 78 à 112 (0,4686).
### t163_echecs_attachement
Les échecs de l'attachement : 94 de span, 33 de cible.
### t164_verbe_gv
Le verbe du GV-phrase : le POS VERB, pas le dernier mot.
### t166_spans
Les spans perdus : 48 REL, 33 SUB, 12 GP.
### t167_denominateur
Le dénominateur : rendement global (÷ 239) et exactitude spans (÷ 146).
### t168_classement
Le classement : la cible réduite à sa tête (exact 94) et les deux conventions du gold.
### t169_conventions
Les deux conventions du gold : cibles verbes et cibles noms, mesurées séparément.
### t170_attachement_cible
L'attachement ciblé : REL → antécédent (nom à gauche), GP → verbe du GV.
### t172_echecs_cible
Les échecs de cible : 11 hors candidats, 11 mal classés.
### t173_topk_strict
Le top-k strict : 88/145 (0,6069), contre 0,9241 en sous-chaîne.
### t175_audit_attachement
L'audit A1 : les 14 valeurs reproduites, écart 0, et le JSON d'audit à jour.
### t176_segment_precedent
La règle du segment précé
… [132 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Computing v2 metric overlap (exact/top1/strict) for the limits section.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, importlib.util, pathlib, collections\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger\nspec=importlib.util.spec_from_file_location('bloc_v2o',pathlib.Path('/tmp/audit_v2 … [1641 caractères tronqués]`

  ```
overlap (exact,top1,strict):
  (False, False, False) 3
  (False, False, True) 2
  (False, True, False) 1
  (False, True, True) 2
  (True, True, True) 137
top1 sans exact: [('r230', 'SUB', 'appelle', 'appelle-moi'), ('s108', 'GP', 'rêve', 'papier'), ('s122', 'GP', 'saute', 'papier')]
strict sans exact: 4 dont pred vide 0
ni exact ni strict: 4
exact et strict: 137
exact hors strict: 0
  ```

### 🤖 Assistant

⏵ Inspecting the tricky gold segments (multi-cible and substring cases).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger\nph={p['id']:p for p in charger()}\nfor pid in ['s108','s122','r230','g012','r018','g002','s041','r309','s012','s03 … [452 caractères tronqués]`

  ```
--- s108 ce calme papier rêve sous le nuage
   GP 'sous le nuage' cibles= ['rêve', 'papier'] mots= [('ce', 'DET'), ('calme', 'ADJ'), ('papier', 'NOUN'), ('rêve', 'VERB'), ('sous', 'PREP'), ('le', 'DET'), ('nuage', 'NOUN')]
--- s122 mon papier saute vers les montagne
   GP 'vers les montagne' cibles= ['saute', 'papier'] mots= [('mon', 'DET'), ('papier', 'NOUN'), ('saute', 'VERB'), ('vers', 'PREP'), ('les', 'DET'), ('montagne', 'NOUN')]
--- r230 Quand tu arrives, appelle-moi.
   SUB 'Quand tu arrives' cibles= ['appelle'] mots= [('Quand', 'CONJ'), ('tu', 'PRON'), ('arrives', 'VERB'), ('appelle', 'VERB'), ('moi', 'PRON')]
--- g012 Le canard est prêt à manger.
   GP 'à manger' cibles= ['prêt', 'canard'] mots= [('Le', 'DET'), ('canard', 'NOUN'), ('est', 'AUX'), ('prêt', 'ADJ'), ('à', 'PREP'), ('manger', 'VERB')]
--- r018 La souris est prête à manger.
   GP 'à manger' cibles= ['prête', 'souris'] mots= [('La', 'DET'), ('souris', 'NOUN'), ('est', 'AUX'), ('prête', 'ADJ'), ('à', 'PREP'), ('manger', 'VERB')]
--- g002 Le chat de la voisine dort.
   GP 'de la voisine' cibles= ['chat'] mots= [('Le', 'DET'), ('chat', 'NOUN'), ('de', 'PREP'), ('la', 'DET'), ('voisine', 'NOUN'), ('dort', 'VERB')]
-
… [1856 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Collecting commit hashes, file hashes, and final state for the audit JSON.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo '--- commits ---' && git log -1 --format='v2 %H %ci %s' 9d5337ce && git log -1 --format='head %H %ci %s' HEAD && git log --oneline 9d5337ce..HEAD | cat && echo '--- blob hashes ---' && git rev-parse 9d5337ce:tools/bloc_linguisti … [565 caractères tronqués]`

  ```
--- commits ---
v2 9d5337ce1c23c4d70f51490d2fcdfa2c390e3faa 2026-11-05 14:14:38 -0500 B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180
head 15ee10d3cd54dcdf3419144d23445765c8910ba2 2026-11-05 14:55:27 -0500 PILOTAGE — LES LIGNES B13 DU ROADMAP ET DES CHANTIERS PASSENT À LA V2 (ATTACHEMENT 0,9448, 181/181)
15ee10d3 PILOTAGE — LES LIGNES B13 DU ROADMAP ET DES CHANTIERS PASSENT À LA V2 (ATTACHEMENT 0,9448, 181/181)
1ec7286c PILOTAGE — LES QUATRE VAGUES DE SOUS-AGENTS DOCUMENTÉES (§ 9) ; VAGUES 3 ET 4 EN COURS
a914c1e7 FICHES — LES 3 DIVERGENCES ET LEURS RÉSIDUS CORRIGÉS (SPANS, DÉNOMINATEUR, LEXIQUE ÉLARGI) ; COHÉRENCE A4 À JOUR
a2def5ee PILOTAGE — LE CACHE DU CHUNKER AU JOURNAL ; T0 DANS LE BUDGET ; 181/181
e0592c59 B13 — LE CACHE DU CHUNKER APPLIQUÉ : ×139 À 160 RÉPÉTITIONS, SORTIE IDENTIQUE (0/612) ; ×1 EN DÉFAUT, S DOMINE ; 181/181
de292c7d ÉTAT — B13 180/180, T0 DANS LE BUDGET ; VAGUE 3 LANCÉE (AUDIT V2, ÉCHECS, REPLIS, CACHE)
2e08cbc7 B13 — LA VAGUE 1 COMPLÈTE : CONTRAT S, COÛT DU CHUNKER, COHÉRENCE DES FICHES ; 3 DIVERGENCES CORRIGÉES
--- blob hashes ---
5cc3858f871b2057b4875708994cecb
… [1772 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying the six A7 IDs and the eight lexicon gains by segment diff.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' > /tmp/audit_v2/ids.json\nimport sys, importlib.util, pathlib, json\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger\ndef load(path):\n    n=pathlib.Path(path).stem\n    spec=importl … [1566 caractères tronqués]`

  ```
{
 "segment_fix": [
  [
   "s012",
   "SUB",
   "écoute"
  ],
  [
   "s030",
   "SUB",
   "cherche"
  ],
  [
   "s052",
   "SUB",
   "ouvre"
  ],
  [
   "s097",
   "SUB",
   "commence"
  ],
  [
   "s124",
   "SUB",
   "commence"
  ],
  [
   "s139",
   "SUB",
   "crie"
  ]
 ],
 "lexique_fix": [
  [
   "r080",
   "GP",
   "fly"
  ],
  [
   "r108",
   "GP",
   "climbs"
  ],
  [
   "r120",
   "GP",
   "flows"
  ],
  [
   "r156",
   "GP",
   "swims"
  ],
  [
   "r166",
   "GP",
   "get"
  ],
  [
   "r169",
   "GP",
   "smiles"
  ],
  [
   "r177",
   "GP",
   "wait"
  ],
  [
   "r180",
   "GP",
   "belongs"
  ]
 ],
 "tetes_fix": [
  [
   "g011",
   "REL",
   "livre"
  ],
  [
   "g012",
   "GP",
   "prêt"
  ],
  [
   "r014",
   "REL",
   "livre"
  ],
  [
   "r015",
   "REL",
   "film"
  ],
  [
   "r018",
   "GP",
   "prête"
  ],
  [
   "r047",
   "GP",
   "poussent"
  ],
  [
   "r054",
   "REL",
   "livre"
  ],
  [
   "r055",
   "REL",
   "ville"
  ],
  [
   "r057",
   "GP",
   "aboie"
  ],
  [
   "r088",
   "GP",
   "grimpe"
  ],
  [
   "r094",
   "REL",
   "film"
  ],
  [
   "r095",
   "REL",
   "maison"
  ],
  [
   "r100",
   "GP",
   "coule"
  ],
  [
   "r126",
   "GP",
   "nage"
  ],
… [1309 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Confirming span losses are unchanged between the pre-v2 and v2 blobs.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, importlib.util, pathlib, collections, json\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger\nph=charger()\ndef spans(path):\n    spec=importlib.util.spec_from_file_locat … [817 caractères tronqués]`

  ```
{"avant_a408a909": {"GP": 13, "SUB": 33, "REL": 48}, "v2_9d5337ce": {"GP": 13, "SUB": 33, "REL": 48}}
  ```

### 🤖 Assistant

⏵ Checking the two target files are new, then drafting the audit JSON.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l reports/rapport-audit-v2.md reports/pensee-audit-v2.json 2>&1; echo '---'; git status --porcelain reports/rapport-audit-v2.md reports/pensee-audit-v2.json", "description": "Verify target audit files are absent"}`

  ```
ls: cannot access 'reports/rapport-audit-v2.md': No such file or directory
ls: cannot access 'reports/pensee-audit-v2.json': No such file or directory
---
  ```

### 🤖 Assistant

⏵ Verifying the pre-v2 11/11 failure split and old rates.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, importlib.util, pathlib, collections, json\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\nspec=importlib.util.spec_from_file_location('bloc_avant_y',pat … [1191 caractères tronqués]`

  ```
old rates {'top1': 126, 'top1_taux': 0.5272, 'top1_taux_span': 0.869, 'topk': 134, 'topk_taux': 0.5607, 'topk_taux_span': 0.9241, 'exact': 123, 'exact_taux': 0.5146, 'exact_taux_span': 0.8483, 'topk_exact': 88, 'topk_exact_taux': 0.3682, 'topk_exact_taux_span': 0.6069}
old failures: 11 hors candidats, 11 mal classés (sous-chaîne)
  ```

### 🤖 Assistant

⏵ Reproducing the A1 pre-v2 controls for comparison with v2.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, importlib.util, pathlib, random, statistics, json\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger\nspec=importlib.util.spec_from_file_location('bloc_avant_c',pathlib.Pa … [1477 caractères tronqués]`

  ```
permutation mean 1.642 sd 1.321 min 0 max 8 n 1000
candidat mean 39.754 sd 4.53 min 27 max 52 n 1000
labels 145 exact 123
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/audit_v2/classement_rejoue.json'))\nprint(json.dumps(d['controle_negatif'],ensure_ascii=False,indent=1)[:3000])\nprint('--- resultats ---')\nr=d['resultats']\nprint(json.dumps({k: … [147 caractères tronqués]`

  ```
{
 "regle_actuelle_regroupee": {
  "justes": 137,
  "taux": 0.9448,
  "par_type": {
   "GP": {
    "n": 83,
    "justes": 77,
    "taux": 0.9277
   },
   "REL": {
    "n": 26,
    "justes": 26,
    "taux": 1.0
   },
   "SUB": {
    "n": 36,
    "justes": 34,
    "taux": 0.9444
   }
  }
 },
 "hasard_vivier_attendu": 0.3876,
 "hasard_cibles_distinctes": 0.0097,
 "mcnemar": {
  "modele_juste_regle_fausse": 7,
  "regle_juste_modele_fausse": 2,
  "p_exact": 0.179688
 },
 "bootstrap_difference": {
  "tirages": 2000,
  "difference": 0.0345,
  "ic95": [
   -0.0069,
   0.0759
  ]
 },
 "repere": {
  "exactitude_entrainement": 0.9931,
  "rang0_justes": 139,
  "rang0_taux": 0.9586,
  "rang0_par_type": {
   "GP": {
    "n": 83,
    "justes": 78,
    "taux": 0.9398
   },
   "REL": {
    "n": 26,
    "justes": 26,
    "taux": 1.0
   },
   "SUB": {
    "n": 36,
    "justes": 35,
    "taux": 0.9722
   }
  }
 }
}
--- resultats ---
{
 "regroupe_hors_pli": {
  "n": 145,
  "modele": {
   "justes": 142,
   "taux": 0.9793,
   "par_type": {
    "GP": {
     "n": 83,
     "justes": 81,
     "taux": 0.9759
    },
    "REL": {
     "n": 26,
     "justes": 26,
     "taux": 1.0
    },
    "SUB": {
     "n": 36
… [451 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, random\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger\nph=charger()\ncibles=[s['cible'] for p in ph for s in p['segments'] if s.get('cible')]\nrng=random.Random(0)\nok … [157 caractères tronqués]`

  ```
239 1 0.0042
  ```

### 🤖 Assistant

⏵ Writing the audit JSON with all measured values, ablations, and gate findings.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/audit_v2/build_json.py <<'PY'\nimport json, pathlib\n\nd = {\n \"date\": \"2026-11-05\",\n \"ligne\": \"B13\",\n \"objet\": \"audit de la fiche d'attachement v2 (rapport-pensee-attachement-v2.md et pensee-attachement-v2.js … [26410 caractères tronqués]`

  ```
wrote reports/pensee-audit-v2.json bytes 26145
comparaison rows 43 ecarts 2
JSON valide
987 reports/pensee-audit-v2.json
  ```

### 🤖 Assistant

⏵ Correcting the JSON verdict counts and rounding notes.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('/tmp/audit_v2/build_json.py')\ns=p.read_text()\ns=s.replace('\"valeurs_comparees\": 31,\\n  \"valeurs_reproduites\": 31,\\n  \"ecarts_numeriques\": 0,',\n            '\"valeurs_compar … [1601 caractères tronqués]`

  ```
patched generator
wrote reports/pensee-audit-v2.json bytes 26395
comparaison rows 43 ecarts 2
JSON valide
verdict {
 "statut": "chiffres reproduits ; reserves documentaires",
 "valeurs_comparees": 43,
 "valeurs_reproduites": 43,
 "ecarts_mesure": 0,
 "ecarts_arrondi": 2,
 "detail_arrondi": "p 0,18 (0,179688) et IC [-0,7 ; +7,6] ([-0,69 ; +7,59]) : arrondis de la fiche, pas des erreurs",
 "erreurs_de_prose": 1,
 "erreurs_de_table": 1,
 "portes_citees": 15,
 "portes_vertes": 15,
 "portes_docstrings_perimees": 8,
 "portes_total_commit_v2": 180,
 "portes_total_head": 181,
 "resume": "Toutes les mesures revendiquees reproduisent sans ecart d'arrondi, y compris les 14 valeurs de l'audit A1 (T175). Une erreur de prose : 46 des 57 echecs doit se lire 45 (le 46 est l'ecart 134-88 ; 45 tetes candidates sont reparables). Une erreur de table : la colonne avant du split est etiquetee POS gold alors que 63/82 est l
rows 43 zeros 41 arrondis ['modele_appris.p', 'modele_appris.ic95']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('/tmp/audit_v2/build_json.py')\ns=p.read_text()\ns=s.replace(\"Toutes les mesures revendiquees reproduisent sans ecart d'arrondi, y compris les 14 valeurs de l'audit A1 (T175).\",\n    … [420 caractères tronqués]`

  ```
wrote reports/pensee-audit-v2.json bytes 26464
comparaison rows 43 ecarts 2
Toutes les mesures revendiquees reproduisent ; les deux seuls ecarts sont des arrondis de la fiche (p 0,18 et IC [-0,7 ; +7,6]), et les 14 valeurs de l'audit A1 (T175) sont intactes. Une erreur de prose : 46 des 57 echecs doit se lire 45 (le 46 est l'ecart 134-88 ; 45 tetes candidates sont reparables). Une erreur de table : la colonne avant du split est etiquetee POS gold alors que 63/82 est l'ancien split lexical ; le POS gold sur l'ancien bloc donne 116/29 (97/116 et 26/29). Huit docstrings de portes sont perimees, dont T168 qui imprime encore /146.
  ```

### 🤖 Assistant

⏵ Writing the audit report fiche in `reports/rapport-audit-v2.md`.

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v2.md", "content": "# Audit B13 — l'attachement v2 : 43 valeurs rejouées, 2 arrondis, 1 erreur de prose (46 → 45), 8 docstrings de portes périmées\n\n> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · ** … [18828 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v2.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Verifying the F3 target cases before finalizing the report.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '84,135p' reports/rapport-topk-diagnostic.md", "description": "Read A2 F3 description and cause table"}`

  ```
## 3. Trois correctifs, ordonnés par gain

Tous sont **simulés** (greffe de lexique et ajout de candidats en mémoire), **aucun n'est
appliqué** : le code du dépôt est inchangé. La colonne « gain » est **incrémentale** dans
l'ordre proposé. Fichier commun : [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py).

| ordre | correctif | fonction à modifier | gain top-k strict | top-1 |
|---|---|---|---:|---:|
| 1 | **F1 — réduire chaque candidat S à sa tête** | `Heuristique.analyser`, branche « 5. syntagmes » (construction de `noms` l. 826 et de `candidats` l. 858/874/892) ; helper existant `_tete_nom` (l. 616) | **+45** | 0 |
| 2 | **F2 — compléter le lexique verbal anglais** | `_est_verbe` (l. 428) via `VERBES_CONNUS` (l. 374) ; pour le POS, `VERBES["en"]` (l. 319) | **+8** | +8 |
| 3 | **F3 — repli par tokens** (GN à gauche, verbes reconnus, enclitiques) | `Heuristique._verbes_proches` (l. 670) et `Heuristique._cible_proche` (l. 643) ; compléter `VERBES_CONNUS` | **+4** | +4* |

\* top-1 conditionnel : F3 ne le rend que si `_cible_proche` suit la même règle (non simulé).

**F1 — 45 segments (C1 26 + C2 17 + C3 2).** Pour chaque candidat S de la forme
`« segment » → queue`, p
… [1975 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Correcting the F3 attribution (token fallback, four cases) in both files.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\nmd=pathlib.Path('reports/rapport-audit-v2.md'); s=md.read_text()\nold='''- A2 proposait aussi **F3** (tête du GN à gauche d'un GP) à **+4 exact/+4 strict** ; la fiche\n  v2 n'en dit rien, ni intégrat … [1630 caractères tronqués]`

  ```
md patched
json patched True
165:- A2 proposait aussi **F3** (repli par tokens : tête du GN à gauche d'un GP, balayage des
167:  fiche v2 n'en dit rien, ni intégration ni rejet. F3 visait **g002, s041, r309 et r230** ;
168:  les quatre autres (g012, r018, s108, s122) resteraient faux même avec F3. Décision non
272:- **F3** (+4 exact/+4 strict selon A2) n'est ni intégré ni discuté dans la fiche ; les cas
JSON valide
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '268,276p' reports/rapport-audit-v2.md", "description": "Check remaining F3 bullet"}`

  ```
du HEAD est 181/181, le commit v2 180/180.
- **Les 94 spans perdus** (48 REL, 33 SUB, 13 GP) sont inchangés : le 0,9448 est conditionnel
  aux 145 labels ; le rendement /239 (0,5732) est plafonné par la couverture 0,6067. Une
  correction d'attachement ne répare pas les spans.
- **F3** (+4 exact/+4 strict selon A2) n'est ni intégré ni discuté dans la fiche ; les cas
  g002/s041 (génitif) et g012/r018 (« à manger » → `prêt`) restent ouverts.
- **Le gold est vivant** ; les sha256 des trois JSON sont épinglés dans
  `pensee-audit-v2.json` (mêmes empreintes que l'audit A1). Le sous-module `tools/structures`
  est au commit `523d8c1` ; sa modification de travail (`donnees/paragraphes-validations.jsonl`)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-audit-v2.md'); s=p.read_text()\nold='''- **F3** (+4 exact/+4 strict selon A2) n'est ni intégré ni discuté dans la fiche ; les cas\n  g002/s041 (génitif) et g012/r018 ( … [395 caractères tronqués]`

  ```
patched
  aux 145 labels ; le rendement /239 (0,5732) est plafonné par la couverture 0,6067. Une
  correction d'attachement ne répare pas les spans.
- **F3** (+4 exact/+4 strict selon A2) n'est ni intégré ni discuté dans la fiche ; il visait
  g002, s041, r309 et r230. g012, r018, s108 et s122 resteraient faux même avec F3.
- **Le gold est vivant** ; les sha256 des trois JSON sont épinglés dans
  ```

### 🤖 Assistant

⏵ Verifying the submodule data-file claim and reading the final report for consistency.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'paragraphes-validations' tools/structures/*.py tools/*.py 2>/dev/null | head -10; echo '---'; grep -rn 'paragraphes-validations' tools/structures 2>/dev/null | head -10", "description": "Check who reads the submodule data f … [5 caractères tronqués]`

  ```
tools/structures/serveur.py:58:        validations = self._journal("paragraphes-validations.jsonl")
tools/structures/serveur.py:92:            with (self.dossier / "paragraphes-validations.jsonl").open("a", encoding="utf-8") as f:
tools/structures/serveur.py:101:        p = self.dossier / "paragraphes-validations.jsonl"
---
tools/structures/tests/test_serveur.py:112:            self.assertTrue((b.dossier / "paragraphes-validations.jsonl").exists())
tools/structures/README.md:202:`donnees/paragraphes-validations.jsonl`) ; le banc de phrases reste `/`.
tools/structures/serveur.py:58:        validations = self._journal("paragraphes-validations.jsonl")
tools/structures/serveur.py:92:            with (self.dossier / "paragraphes-validations.jsonl").open("a", encoding="utf-8") as f:
tools/structures/serveur.py:101:        p = self.dossier / "paragraphes-validations.jsonl"
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v2.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v2.md</path>
<type>file</type>
<content>
1: # Audit B13 — l'attachement v2 : 43 valeurs rejouées, 2 arrondis, 1 erreur de prose (46 → 45), 8 docstrings de portes périmées
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅ **chiffres reproduits** ;
4: > ⚠️ **réserves documentaires** (§ 3, § 4, § 6) — aucune ne change les totaux.
5: >
6: > **Audité** : commit **`9d5337ce`** (2026-11-05 14:14), fiche
7: > [`rapport-pensee-attachement-v2.md`](rapport-pensee-attachement-v2.md) et JSON
8: > [`pensee-attachement-v2.json`](pensee-attachement-v2.json).
9: >
10: > **Dispositif** : depuis la racine, `sys.path.insert(0, '.')` ;
11: > `evaluer_bloc("h", Heuristique(), charger())` ; le **blob exact du commit v2**
12: > (`git show 9d5337ce:tools/bloc_linguistique.py`, sha256 `6e843018…`) chargé depuis `/tmp`
13: > avec `RACINE` forcé à la racine du dépôt. Les ablations sont des copies `/tmp` du même
14: > blob ; **aucun fichier existant n'a été modifié, aucun commit**. HEAD a bougé pendant
15: > l'audit (de `de292c7d` à `15ee10d3`) ; le bloc courant (sha256 `bb020
… [6984 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v2.md", "offset": 120, "limit": 180}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v2.md</path>
<type>file</type>
<content>
120: | | POS gold VERB | POS gold nom |
121: |---|---:|---:|
122: | `_est_verbe` **vrai** | **63** (60 justes) | 0 |
123: | `_est_verbe` **faux** | **53** (37 justes) | **29** (26 justes) |
124: 
125: - L'ancien split lexical donne **63/60** (0,9524) et **82/63** (0,7683) ;
126: - le POS gold sur le **même ancien bloc** donne **116/97** (0,8362) et **29/26** (0,8966) ;
127: - le POS gold sur le **v2** donne **116/111** (0,9569) et **29/26** (0,8966).
128: 
129: Il n'y a **aucune** cible verbe lexical qui devienne nom POS : les 53 sont des noms lexicaux
130: reclassés en verbes par le POS gold. Le « +48 cibles » de la fiche est `111 − 63`, soit des
131: justes après moins des cibles avant : ce n'est ni un gain de cibles ni un gain de justes. Le
132: nombre de cibles verbes passe 63 → 116 (+53) ; les justes 60 → 111 (+51) en comparaison
133: mixte, ou **97 → 111 (+14) à split POS constant**. Le côté nom est **inchangé** à 26/29. Le
134: gain d'exact +14 est donc **entièrement du côté verbe** : GP +8 (lexique) et SUB +6 (segment),
135: REL 0. La fiche le dit en prose («
… [11209 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Fixing the dated-snapshot wording in the gates section.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-audit-v2.md'); s=p.read_text()\nold=\"La mention « 180/180 » de la fiche est donc un\\n**instantané daté**, juste à son commit, plus au HEAD.\"\nnew=\"La mention « 180 … [317 caractères tronqués]`

  ```
patched
**Portes au total** : **180** au commit v2 ; **181** au HEAD (T178, cache du chunker, ajoutée
après), run complet **181/181** en 5 min 17 s. La mention « 180/180 » de la fiche est donc un
**instantané daté** : juste au commit v2, périmée au HEAD. Le JSON `pensee-attachement-v2.json`
porte encore `"portes": "180/180"`.
  ```

### 🤖 Assistant

⏵ Validating JSON, links, and the no-extra-files constraint.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, re, pathlib\np=pathlib.Path('reports/pensee-audit-v2.json'); d=json.loads(p.read_text())\nprint('JSON OK, top keys:', list(d.keys()))\nprint('verdict:', d['verdict']['statut'], d['verdict']['valeurs_com … [1199 caractères tronqués]`

  ```
JSON OK, top keys: ['date', 'ligne', 'objet', 'verdict', 'dispositif', 'mesure', 'comparaison', 'decomposition', 'split', 'echecs', 'controles', 'portes', 'modele_appris', 'erreurs', 'limites', 'fichiers']
verdict: chiffres reproduits ; reserves documentaires 43 rows 43
decomposition v2: {'top1': 140, 'topk': 142, 'exact': 137, 'strict': 141}
gains: {'tetes_candidats': (0, 0, 0, 45), 'lexique_anglais': (8, 8, 8, 8), 'segment_precedent': (6, 6, 0, 0), 'genre_s': (0, 0, 0, 0)}
portes citees 15 ok 15
docstrings perimees 8
erreurs prose 1 table 1
links 13 bad []
--- new files status ---
?? reports/pensee-audit-v2.json
?? reports/rapport-audit-v2.md
--- accidental new reports/tools? ---
?? reports/pensee-audit-v2.json
?? reports/pensee-cache-chunker.json
?? reports/pensee-replis-cible.json
?? reports/rapport-audit-v2.md
?? reports/rapport-cache-chunker.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/replis_cible.py
  ```

### 🤖 Assistant

⏵ Checking whether concurrent commits moved HEAD or the measured block after the audit.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git rev-parse HEAD && git log -1 --format='%h %ci %s' | cat && sha256sum tools/bloc_linguistique.py tools/pensee/autotest.py && git diff --stat 15ee10d3..HEAD -- tools/bloc_linguistique.py tools/pensee/autotest.py 2>/dev/null | cat", … [56 caractères tronqués]`

  ```
dcf7bc912caeebe940793888d88723f0bbb57f58
dcf7bc91 2026-11-05 15:18:56 -0500 B13 — L'ATTACHEMENT V3 : EXACT 0,9448 → 0,9724, NOMS 29/29 = 1,0 ; R2/R3/R4 DE A9 ; 181/181
9da6dee7118cfa576d159ccdf5d1241232e974544cd3a6c5cebaddcbbaccd059  tools/bloc_linguistique.py
165b4861c0dcaa2fdd6c0455dd5bf09b69ce4d35197e38cacd6157ddb7c31dc2  tools/pensee/autotest.py
 tools/bloc_linguistique.py | 66 +++++++++++++++++++++++++++++++++++++++++++---
 tools/pensee/autotest.py   | 30 ++++++++++-----------
 2 files changed, 77 insertions(+), 19 deletions(-)
  ```

### 🤖 Assistant

⏵ A v3 integration landed during the audit; inspecting it to keep the v2 report scoped correctly.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat dcf7bc91 | head -60 && echo '=== bloc diff v3 ===' && git show dcf7bc91 -- tools/bloc_linguistique.py | head -200", "description": "Inspect v3 integration scope"}`

  ```
commit dcf7bc912caeebe940793888d88723f0bbb57f58
Author: Stéphane <stephane@localhost>
Date:   Thu Nov 5 15:18:56 2026 -0500

    B13 — L'ATTACHEMENT V3 : EXACT 0,9448 → 0,9724, NOMS 29/29 = 1,0 ; R2/R3/R4 DE A9 ; 181/181

 docs/pilotage/en-cours.md                          |   6 +-
 docs/pilotage/roadmap.md                           |   2 +-
 journal/2026-11-05/README.md                       |  21 +-
 journal/2026-11-05/attention.md                    |  16 +-
 journal/2026-11-05/distribue.md                    |  16 +-
 journal/2026-11-05/docs.md                         |  21 +-
 journal/2026-11-05/memoire.md                      |  16 +-
 journal/2026-11-05/mesures.md                      |  16 +-
 journal/2026-11-05/modele.md                       |  16 +-
 journal/2026-11-05/moteur.md                       |  16 +-
 journal/2026-11-05/portes.md                       |  16 +-
 journal/README.md                                  |  16 +-
 journal/THEMES.md                                  |   2 +-
 .../1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/digest.md | 494 ++++++++++++++++
 .../rapport.md                                     |  42 +-
 .../3144cf23-6004-46ef-bc3d-f05d81c0cff6/digest.
… [7955 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking how v3 changed the gate assertions, to keep the v2 gate audit precise.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show dcf7bc91 -- tools/pensee/autotest.py", "description": "Inspect v3 gate assertion changes"}`

  ```
commit dcf7bc912caeebe940793888d88723f0bbb57f58
Author: Stéphane <stephane@localhost>
Date:   Thu Nov 5 15:18:56 2026 -0500

    B13 — L'ATTACHEMENT V3 : EXACT 0,9448 → 0,9724, NOMS 29/29 = 1,0 ; R2/R3/R4 DE A9 ; 181/181

diff --git a/tools/pensee/autotest.py b/tools/pensee/autotest.py
index f4331ec6..17c522e2 100644
--- a/tools/pensee/autotest.py
+++ b/tools/pensee/autotest.py
@@ -2223,8 +2223,8 @@ def t153_attachement() -> tuple[bool, str]:
     import tools.bloc_linguistique as bl
     from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
     r = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
-    return (r["cibles"] == 239 and abs(r["top1_taux"] - 0.5858) < 0.001
-            and abs(r["exact_taux"] - 0.5732) < 0.001), (
+    return (r["cibles"] == 239 and abs(r["top1_taux"] - 0.5983) < 0.001
+            and abs(r["exact_taux"] - 0.59) < 0.001), (
         f"attachement : top1 {r['top1_taux']}, exact {r['exact_taux']}, "
         f"couverture {r['couverture']}")
 
@@ -2341,7 +2341,7 @@ def t161_cible_proximite() -> tuple[bool, str]:
     from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
     r = evaluer_bloc("h", bl.Heuristique()
… [5207 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Updating the report for the v3 integration that landed after the v2 measurements.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-audit-v2.md'); s=p.read_text()\nrepls=[]\nrepls.append((\n\"\"\"> blob ; **aucun fichier existant n'a été modifié, aucun commit**. HEAD a bougé pendant\n> l'audit (de  … [7410 caractères tronqués]`

  ```
md patched, len 20306
json patched
JSON valide
17:> une intégration v3 (`dcf7bc91`, 15:18) a atterri** : elle change les valeurs (exact 141/145,
44:  revendiquées. Le registre v2 a **180** portes. **Depuis, v3 `dcf7bc91` a réécrit la plupart
46:  **181** portes ; le run complet au moment de l'audit (avant v3) donnait **181/181**, et le
47:  commit v3 annonce 181/181 avec ses valeurs — hors périmètre. Huit docstrings sont périmées
201:après), run complet **181/181** en 5 min 17 s **au moment de l'audit (avant v3)**. La mention
205:**Depuis, v3 `dcf7bc91` (15:18) a réécrit les assertions** : T153 0,5983/0,59 ; T161 top1 143,
209:comparée aux portes du HEAD** : les mêmes numéros de porte y attendent les valeurs v3.
280:  mémoïsation (`bb020516…` contre `6e843018…` au v2) : mêmes chiffres. **Puis v3 `dcf7bc91` a
282:  Les chiffres v2 de cette fiche sont donc **historiques** ; v3 est hors périmètre et ne doit
296:  **n'audite pas v3** (`dcf7bc91`), arrivé après les mesures.
315:- [`rapport-pensee-attachement-v3.md`](rapport-pensee-attachement-v3.md) — l'état suivant,
  ```

### 🤖 Assistant

⏵ Tightening the JSON concurrency fields so “HEAD” cannot be read as v3.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib\np=pathlib.Path('reports/pensee-audit-v2.json'); d=json.loads(p.read_text())\nprint(json.dumps(d['dispositif'],ensure_ascii=False,indent=1)[:2000])\nprint('--- portes total ---')\nprint(json.dum … [189 caractères tronqués]`

  ```
{
 "branche": "s/v7",
 "commit_v2": "9d5337ce1c23c4d70f51490d2fcdfa2c390e3faa",
 "commit_v2_date": "2026-11-05 14:14:38 -0500",
 "commit_v2_sujet": "B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180",
 "head_audit": "15ee10d3cd54dcdf3419144d23445765c8910ba2",
 "head_audit_date": "2026-11-05 14:55:27 -0500",
 "head_a_bouge_pendant_audit": "de de292c7d a 15ee10d3 (commits concurrents : cache, T178, fiches, pilotage) ; les fichiers mesures sont propres au HEAD final",
 "sha256_bloc_v2": "6e8430180ccca615e330c33596ff3c4020666b9feb452c7b25f771b4066d3c65",
 "sha256_bloc_head": "bb0205165cc2b0f880f3df26c65ab56349c77301a7d9325025b35c28e145eb44",
 "sha256_evaluer_gold": "c4d2dbc07b4e4c0b1c81889b61fd517d5d5953b4a3efae2094834a398ac5d599",
 "sha256_gold": {
  "gold.json": "3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a",
  "gold_reel.json": "05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11",
  "gold_synthetique.json": "e3e704ce9cb599db07ab31d1b0651f0aa12ea9ecad31ca8bf558efdeed84a654"
 },
 "appel": "sys.path.insert(0,'.'); import tools.bloc_linguistique as bl; from tool
… [978 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib\np=pathlib.Path('reports/pensee-audit-v2.json'); d=json.loads(p.read_text())\nd['dispositif']['head_a_bouge_pendant_audit']=\"de de292c7d a 15ee10d3 pendant les mesures v2 (commits concurrents : … [1091 caractères tronqués]`

  ```
patched
JSON valide
de de292c7d a 15ee10d3 pendant les mesures v2 (commits concurrents : cache, T178, fiches, pilotage) ; puis v3 dcf7bc91 apres les mesures. Les mesures v2 sont sur le blob 9d5337ce.
nge les valeurs. Les ablations ont ete faites sur des copies /tmp du blob v2, jamais sur le fichier du depot. v3 (dcf7bc91) est arrive apres les mesures et n'est pas melange au v2.
T178 (cache chunker) ajoutee apres le v2 ; run complet au moment de l'audit (avant v3) : 181/181 en 5 min 17 s. v3 dcf7bc91 (15:18) conserve 181 portes mais reecrit les assertions.
  ```

### 🤖 Assistant

⏵ Final consistency pass: links, JSON, and HEAD/v3 wording.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, re, pathlib\nmd=pathlib.Path('reports/rapport-audit-v2.md').read_text()\nlinks=re.findall(r'\\[[^\\]]+\\]\\(([^)]+)\\)', md)\nbad=[]\nfor l in links:\n    if l.startswith('http') or l.startswith('#'): c … [739 caractères tronqués]`

  ```
links 14 bad []
json keys 16 comparison 43
v3 fields: dcf7bc912caeebe940793888d88723f0bbb57f58 9da6dee7118c v3 (dcf7bc91, 15:18) a reecrit les assertions : T153 0,5983/0,59 ; T161 top1 143
resume:  donne 116/29 (97/116 et 26/29). Huit docstrings de portes sont perimees, dont T168 qui imprime encore /146. v3 (dcf7bc91) est arrive apres les mesures : les chiffres v2 sont historiques, les portes du HEAD attendent v3.
--- HEAD mentions in MD ---
14:> blob ; **aucun fichier existant n'a été modifié, aucun commit**. HEAD a bougé pendant
45:  de ces assertions** (exact 141, top1 143, noms 29/29, strict 142, T172 2/2) et le HEAD a
200:**Portes au total** : **180** au commit v2 ; **181** au HEAD (T178, cache du chunker, ajoutée
202:« 180/180 » de la fiche est donc un **instantané daté** : juste au commit v2, périmée au HEAD.
209:comparée aux portes du HEAD** : les mêmes numéros de porte y attendent les valeurs v3.
279:- **Le HEAD a bougé** (de `de292c7d` à `15ee10d3`) et le bloc v2-compatible a reçu une
305:  `6e843018…`, le HEAD `bb020516…` (mémoïsation seule).
--- file status ---
?? reports/pensee-audit-v2.json
?? reports/rapport-audit-v2.md
  316 reports/rapport-audit-v2.md
 1003 reports
… [33 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Fixing the last stale “HEAD = memoization” line in the files section.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-audit-v2.md'); s=p.read_text()\nold=\"\"\"- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — le bloc ; le blob v2 est\n  `6e843018…`, le HEAD `bb020516…` (mém … [517 caractères tronqués]`

  ```
patched
- [`pensee-audit-v2.json`](pensee-audit-v2.json) — les 43 comparaisons, la décomposition, les
  contrôles et le détail des portes.
- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — le bloc ; le blob v2 mesuré est
  `6e843018…`. Le HEAD v2-compatible était `bb020516…` (mémoïsation seule) ; le HEAD v3
  actuel est `9da6dee7…` (hors périmètre).
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `charger()`,
  `evaluer_bloc`.
JSON valide
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-v2.json'))\ndef walk(o,path=''):\n    if isinstance(o,dict):\n        for k,v in o.items(): yield from walk(v,path+'/'+k)\n    elif isinstance(o,list):\n        fo … [249 caractères tronqués]`

  ```
/verdict/resume : Toutes les mesures revendiquees reproduisent ; les deux seuls ecarts sont des arrondis de la fiche (p 0,18 et IC [-0,7 ; +7,6]), et les 14 valeurs de l'audit A1 (T175) sont intactes. Une erreur de prose : 46 des 57 echecs doit se lire 45 (l
/dispositif/methode : Le blob exact du commit v2 (git show 9d5337ce:tools/bloc_linguistique.py) a ete charge depuis /tmp avec RACINE force a la racine du depot (indispensable pour que l'import de generateur, dans tools/structures, resolve). Le HEAD au moment des
/portes/non_couverts[3] : le compte 180/180 : la liste des portes est imprimee, pas assertee ; le HEAD est a 181/181
/limites[6] : Le HEAD a bouge pendant l'audit (de292c7d -> 15ee10d3) et le bloc courant a recu une memoisation (sha256 bb020516... contre 6e843018... au v2) : les valeurs sont identiques, verifie sur le blob v2 exact et sur le HEAD.
/limites[10] : v3 (dcf7bc91, 15:18) est arrive apres les mesures v2 : exact 141/145, top1 143, noms 29/29, strict 142 ; il reecrit les assertions des memes portes. Les chiffres v2 de cette fiche sont historiques et ne doivent pas etre compares aux portes
  ```

### 🤖 Assistant

⏵ Removing the last stale claim that the current HEAD is v2-equivalent.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib\np=pathlib.Path('reports/pensee-audit-v2.json'); d=json.loads(p.read_text())\nold=\"Le HEAD a bouge pendant l'audit (de292c7d -> 15ee10d3) et le bloc courant a recu une memoisation (sha256 bb020 … [1061 caractères tronqués]`

  ```
patched
JSON valide
Le HEAD a bouge pendant l'audit (de292c7d -> 15ee10d3) et le bloc v2-compatible a recu une memoisation (sha256 bb020516... contre 6e843018... au v2) : les valeurs v2 sont identiques, verifie sur le blob v2 exact et sur ce HEAD v2-compatible. Puis v3 (dcf7bc91) est arrive apres les mesures et change les valeurs ; voir la limite suivante.
le compte 180/180 : la liste des portes est imprimee, pas assertee ; le HEAD v3 est a 181/181 (valeurs v3)
  ```

### 🤖 Assistant

⏵ Final numeric cross-check between the JSON and the raw measurements.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json, importlib.util, pathlib\nsys.path.insert(0,'.')\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\nd=json.load(open('reports/pensee-audit-v2.json'))\nspec=importlib.util.spec … [1733 caractères tronqués]`

  ```
OK  cibles 239 239
OK  labels 145 145
OK  top1 140 140
OK  topk 142 142
OK  exact 137 137
OK  strict 141 141
OK  top1_span 0.9655 0.9655
OK  topk_span 0.9793 0.9793
OK  exact_span 0.9448 0.9448
OK  strict_span 0.9724 0.9724
OK  verbe 111/116 111/116
OK  nom 26/29 26/29
raw variants {"bloc_v2": {"top1": 140, "topk": 142, "exact": 137, "strict": 141}, "v2_sans_tetes": {"top1": 140, "topk": 142, "exact": 137, "strict": 96}, "v2_sans_lexique": {"top1": 132, "topk": 134, "exact": 129, "strict": 133}, "v2_sans_segment": {"top1": 134, "topk": 142, "exact": 131, "strict": 141}, "v2_sans_genre": {"top1": 140, "topk": 142, "exact": 137, "strict": 141}}
json variants {"avant_a408a909": {"top1": 126, "topk": 134, "exact": 123, "strict": 88}, "avant_plus_tetes": {"top1": 126, "topk": 134, "exact": 123, "strict": 133}, "avant_plus_tetes_plus_lexique": {"top1": 134, "topk": 142, "exact": 131, "strict": 141}, "v2": {"top1": 140, "topk": 142, "exact": 137, "strict": 141}, "v2_sans_tetes": {"top1": 140, "topk": 142, "exact": 137, "strict": 96}, "v2_sans_lexique": {"top1": 132, "topk": 134, "exact": 129, "strict": 133}, "v2_sans_segment": {"top1": 134, "topk": 142, "exact": 131, "strict": 141}, "v2_s
… [70 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Confirming the v3 numbers cited in the concurrency note against the v3 fiche.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,30p' reports/rapport-pensee-attachement-v3.md 2>/dev/null && echo '--- v3 json ---' && python3 - <<'PY'\nimport json\ntry:\n d=json.load(open('reports/pensee-attachement-v3.json'))\n print(json.dumps({k:d[k] for k in d if k … [200 caractères tronqués]`

  ```
# B13 — l'attachement v3 : exact 0,9448 → 0,9724, les noms à 1,0

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **181/181 portes** : trois règles **générales** issues du diagnostic des 8 échecs (A9) sont
> intégrées — **R2** (un GP n'est pas gouverné par un mot de son span), **R3** (cible vide :
> génitif → tête du GN à gauche), **R4** (enclitique `appelle-moi` → `appelle`). Sur les 145
> segments au bon span : **exact 137 → 141 (0,9724)**, top1 **140 → 143 (0,9862)**, top-k 142
> (0,9793), **top-k strict 142 (0,9793)** ; les **cibles noms atteignent 29/29 = 1,0**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_cible_hors_span`,
> `_repli_cible_gp`, `_sans_enclitique`), [`autotest.py`](../tools/pensee/autotest.py) ;
> fiche A9 [échecs v2](rapport-echecs-v2.md) ; JSON [`pensee-attachement-v3.json`](pensee-attachement-v3.json).

## 1. Avant / après (145 segments au bon span)

| mesure | v2 | **v3** | écart |
|---|---:|---:|---:|
| top1 | 140 (0,9655) | **143 (0,9862)** | +3 |
| top-k | 142 (0,9793) | 142 (0,9793) | 0 |
| **exact** | **137 (0,9448)** | **141 (0,9724)** | **+4** |
| top-k strict
… [645 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Final read of the JSON verdict and gate blocks before reporting.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-v2.json'))\nprint(json.dumps(d['verdict'],ensure_ascii=False,indent=1))\nprint('--- portes summary ---')\nprint(json.dumps({k:d['portes'][k] for k in ('total_commi … [401 caractères tronqués]`

  ```
{
 "statut": "chiffres reproduits ; reserves documentaires",
 "valeurs_comparees": 43,
 "valeurs_reproduites": 43,
 "ecarts_mesure": 0,
 "ecarts_arrondi": 2,
 "detail_arrondi": "p 0,18 (0,179688) et IC [-0,7 ; +7,6] ([-0,69 ; +7,59]) : arrondis de la fiche, pas des erreurs",
 "erreurs_de_prose": 1,
 "erreurs_de_table": 1,
 "portes_citees": 15,
 "portes_vertes": 15,
 "portes_docstrings_perimees": 8,
 "portes_total_commit_v2": 180,
 "portes_total_head": 181,
 "resume": "Toutes les mesures revendiquees reproduisent ; les deux seuls ecarts sont des arrondis de la fiche (p 0,18 et IC [-0,7 ; +7,6]), et les 14 valeurs de l'audit A1 (T175) sont intactes. Une erreur de prose : 46 des 57 echecs doit se lire 45 (le 46 est l'ecart 134-88 ; 45 tetes candidates sont reparables). Une erreur de table : la colonne avant du split est etiquetee POS gold alors que 63/82 est l'ancien split lexical ; le POS gold sur l'ancien bloc donne 116/29 (97/116 et 26/29). Huit docstrings de portes sont perimees, dont T168 qui imprime encore /146. v3 (dcf7bc91) est arrive apres les mesures : les chiffres v2 sont historiques, les portes du HEAD attendent v3.",
 "portes_total_head_commit": "dcf7bc91",
 "portes_total
… [1734 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Sending the self-contained audit result to the parent agent.

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "AUDIT V2 TERMINÉ — deux fichiers neufs : reports/rapport-audit-v2.md et reports/pensee-audit-v2.json. Aucun fichier existant modifié, aucun commit.\n\nVERDICT : les chiffres v2 reproduisent tous, sur le blob exact 9d5337ce (sha256 6e84 … [3037 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

### 🤖 Assistant

⏵ Checking HEAD one last time and confirming the two deliverables are intact.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git rev-parse HEAD && git log -1 --format='%h %s' | cat && echo '--- deliverables ---' && ls -l reports/rapport-audit-v2.md reports/pensee-audit-v2.json && python3 -m json.tool reports/pensee-audit-v2.json > /dev/null && echo 'JSON v … [142 caractères tronqués]`

  ```
b1b1292f7983a5f7349bc81dc92404be5cd99a36
b1b1292f B13 — LE CACHE COMPLET : UN SEUL CHUNKING DANS LES DEUX CHEMINS (T178), VALIDÉ PAR A11 (×11,0, ÉGALITÉ 612/612) ; 181/181
--- deliverables ---
-rw-r--r--. 1 stephane stephane 28371  5 nov 15:32 reports/pensee-audit-v2.json
-rw-------. 1 stephane stephane 20912  5 nov 15:32 reports/rapport-audit-v2.md
JSON valide
?? reports/pensee-audit-v2.json
?? reports/rapport-audit-v2.md
  ```

### 🤖 Assistant

⏵ HEAD advanced again (cache commit after v3); checking gate drift and fixing the “current” wording.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat dcf7bc91..HEAD -- tools/bloc_linguistique.py tools/pensee/autotest.py && git diff --stat 15ee10d3..HEAD -- tools/bloc_linguistique.py tools/pensee/autotest.py && sha256sum tools/bloc_linguistique.py && git show HEAD:t … [140 caractères tronqués]`

  ```
tools/bloc_linguistique.py | 14 ++++++--------
 tools/pensee/autotest.py   | 13 +++++++++----
 2 files changed, 15 insertions(+), 12 deletions(-)
 tools/bloc_linguistique.py | 80 +++++++++++++++++++++++++++++++++++++++-------
 tools/pensee/autotest.py   | 43 ++++++++++++++-----------
 2 files changed, 92 insertions(+), 31 deletions(-)
9544f173f92e55ccb6eed7b9f096f4a6bf100449d3b1d7875440a23badbda7ff  tools/bloc_linguistique.py
2226:    return (r["cibles"] == 239 and abs(r["top1_taux"] - 0.5983) < 0.001
2344:    return (a["cibles"] == 239 and a["top1"] == 143 and a["exact"] == 141), (
2434:            and abs(a["exact_taux_span"] - 0.9724) < 0.001), (
  ```

### 🤖 Assistant

⏵ Fixing the final “current HEAD = v3” wording after the post-v3 cache commit.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib, json\np=pathlib.Path('reports/rapport-audit-v2.md'); s=p.read_text()\nold=\"\"\"- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — le bloc ; le blob v2 mesuré est\n  `6e843018…`. Le HEAD v2- … [1309 caractères tronqués]`

  ```
md patched
json patched
JSON valide
- [`pensee-audit-v2.json`](pensee-audit-v2.json) — les 43 comparaisons, la décomposition, les
  contrôles et le détail des portes.
- [`bloc_linguistique.py`](../tools/bloc_linguistique.py) — le bloc ; le blob v2 mesuré est
  `6e843018…`. Le HEAD v2-compatible était `bb020516…` (mémoïsation seule) ; le commit v3
  `dcf7bc91` est `9da6dee7…` (hors périmètre), et le HEAD a encore avancé (`b1b1292f`, cache
  T178) après v3.
- [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) — `charger()`,
  `evaluer_bloc`.
  ```

### 🤖 Assistant

⏵ Normalizing file permissions to match the reports directory.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && chmod 644 reports/rapport-audit-v2.md reports/pensee-audit-v2.json && ls -l reports/rapport-audit-v2.md reports/pensee-audit-v2.json && python3 -m json.tool reports/pensee-audit-v2.json > /dev/null && echo 'JSON valide' && python3 -  … [367 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 28567  5 nov 15:39 reports/pensee-audit-v2.json
-rw-r--r--. 1 stephane stephane 20984  5 nov 15:39 reports/rapport-audit-v2.md
JSON valide
links 14 bad []
  ```

### 🤖 Assistant

⏵ Delivering the audit summary.

## Livrables

Deux fichiers neufs, aucun fichier existant modifié, aucun commit :

- `reports/rapport-audit-v2.md`
- `reports/pensee-audit-v2.json` (JSON valide, 43 comparaisons)

L'audit porte sur le **commit v2 `9d5337ce`**, avec le blob exact `git show 9d5337ce:tools/bloc_linguistique.py` (sha256 `6e843018…`) chargé depuis `/tmp` et `RACINE` forcé à la racine.

## Verdict

**Toutes les valeurs v2 reproduisent** : labels 145, top1 140, top-k 142, exact 137, top-k strict 141 ; taux 0,9655 / 0,9793 / 0,9448 / 0,9724 ; rendement 0,5858 / 0,5941 / 0,5732 ; split 116/111 (0,9569) et 29/26 (0,8966) ; 8 échecs (3/5) ; spans 94 = 48/33/13 ; avant 126/134/123/88 ; gold 612. Le modèle appris a été rejoué : 142/145, +5, McNemar 7/2, p = 0,1797, IC [-0,69 ; +7,59] → rejeté, conforme.

**Deux arrondis seulement** : `p = 0,18` pour `0,179688` ; IC `[-0,7 ; +7,6]` pour `[-0,69 ; +7,59]`.

## Écarts documentaires

1. **« 46 des 57 échecs » → 45.** A2 dit 45 ; le comptage indépendant donne 45 têtes candidates égales à la cible. Le 46 est `134 − 88` (sous-chaîne vs strict), une autre quantité. Le gain « +45 » est correct.
2. **Colonne avant du split** : elle est étiquetée « (POS gold) » mais **63/82 est l'ancien split lexical** (`_est_verbe`, lexique pré-v2). Le POS gold sur l'ancien bloc donne **116/97 (0,8362)** et **29/26 (0,8966)**. Le « **+48 cibles** » est `111 − 63`, un mélange de justes et de cibles ; ce n'est pas un gain. Le JSON nomme correctement les valeurs avant `verbe_est` / `nom_est`.
3. **Attributions incomplètes** : le segment précédent fait **+6 exact et +6 top1** ; le lexique fait **+8 exact/+8 top1/+8 top-k/+8 strict** ; les têtes font **+45 strict (26 REL + 19 GP), 0 exact**. Les totaux 137/140/142/141 sont justes, mais le tableau des corrections omet +6 top1 et +8 top-k/strict. Le helper `_cible_s_par_genre`, ajouté au v2, a **0 effet mesuré** et n'est pas documenté.

## Portes

- **Au commit v2, les 15 portes citées passent** (T153, T161–T164, T166–T170, T172, T173, T175–T177). Registre v2 : **180** portes. Run complet au moment de l'audit (avant v3) : **181/181**.
- **8 docstrings périmées** : T153, T162, T163, T166, T167, T168, T172, T173. T168 imprime encore `/146` au lieu de `/145` ; T163 dit « 33 avant les correctifs » alors que 33 était un compte d'exacts à `d400e188` (A1 compte 22 échecs).
- **Chiffres non couverts** : `topk_taux` 0,5941 ; les taux avant et le split nom 82/63 ; le 69/69 SUB = VERB ; le compte 180/180 ; les chiffres du modèle appris ; le 46/57.
- **Concurrence importante** : après les mesures, le dépôt est passé à la **v3 `dcf7bc91`** (exact 141/145, top1 143, noms 29/29, strict 142, T172 2/2) ; les mêmes portes ont été réécrites pour v3. Le HEAD a encore avancé (`b1b1292f`, cache T178). **La fiche v2 et ses 180/180 sont historiques : ne pas les comparer aux portes du HEAD.**

## Contrôles

- **Permutation des cibles** (1 000 tirages) : moyenne 1,786/145, max 8, observé 137 → `p < 0,001`.
- **Candidat aléatoire** (1 000 tirages) : moyenne 58,566/145, max 75, observé 137 → `p < 0,001` ; sans les têtes : 43,742. Le +45 des têtes vient bien de la réduction des candidats, mais gonfle la ligne de base du candidat aléatoire de **+10,2 pts** : le top-k strict est une **couverture de candidats**, pas une exactitude.
- **Recouvrement** : 137 exact = strict = top1 ; 4 stricts-sans-exact ; 1 top1-only (r230) ; 3 ni l'un ni l'autre.

## Limites

Le replay pré-v2 depuis `/tmp` exige `RACINE` = racine (sinon 77 labels / 0 exact) ; le lexique +8 est une borne haute (les 8 cibles anglaises exactement) ; 36/145 labels multi-cibles ; le split 3/5 utilise la sous-chaîne (4/4 en strict) ; F3 (+4/+4 selon A2) n'est ni intégré ni discuté.

