# Session DSH — relecture

- identifiant : `cdc16e57-4a69-4890-8b3c-270539c64ff2`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-06 21:13:31
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état du chantier S** (le lecteur) — lecture seule, aucun code.

Contexte : `docs/pilotage/roadmap.md` (chantier S), `docs/pilotage/en-cours.md` (session S), les fiches `reports/rapport-s-*.md`, `tools/structures/` (données S : `validations.jsonl` 150 verdicts, `paragraphes-validations.jsonl` 19 verdicts sur a001–a009), la page `/paragraphes`, les 71 langues.

À faire :
1. **Inventaire mesuré** : les 71 langues (lesquelles, où, combien testées) ; la page `/paragraphes` (a001–a009 faits, les 8 restants) ; la **rétro-traduction** (existe-t-elle ? où ? mesurée ?) ; les blocages restants.
2. **Lis** `validations.jsonl` et `paragraphes-validations.jsonl` : compte, statuts, couverture ; ce que les verdicts humains disent de la qualité.
3. **Propose** les 3 prochaines actions de S (mesurables, sans écrire dans `tools/structures/` ni `data/`), avec la commande exacte si elle existe.
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-etat-s.md` et `reports/pensee-etat-s.json`.
5. Ne commite rien ; ne modifie aucun existant ; pas de `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`.

Rends un résumé : les 71 langues, la rétro-traduction, les 3 prochaines actions.
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

⏵ Inventaire initial du dépôt et des fichiers S

- **bash** `{"command": "git branch --show-current && git status --porcelain | head -20 && echo \"---\" && ls reports/ | head -80", "description": "Vérifie branche, statut et liste reports"}`

  ```
s/v7
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
MM journal/2026-11-06/README.md
D  journal/2026-11-06/distribue.md
D  journal/2026-11-06/docs.md
D  journal/2026-11-06/memoire.md
D  journal/2026-11-06/mesures.md
D  journal/2026-11-06/modele.md
D  journal/2026-11-06/outils.md
D  journal/2026-11-06/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
---
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
a80
… [1212 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/structures/ && echo \"---\" && wc -l tools/structures/*.jsonl 2>/dev/null", "description": "Liste tools/structures et compte les JSONL"}`

  ```
arbre_svg.py
candidats_corpus.py
construire_donnees.py
donnees
exporter_corpus.py
generateur.py
llm.py
mesure_analyseur.py
mesure_arbre.py
mesure_corpus.py
__pycache__
README.md
serveur.py
static
tests
verifier_corpus.py
---
[exit code: 1]
  ```

### 🤖 Assistant

⏵ Localisation des données S et des fiches de session

- **bash** `{"command": "find tools/structures -name \"*.jsonl\" -o -name \"*.json\" | head -40; echo \"---\"; ls -la tools/structures/donnees/ 2>/dev/null | head -30", "description": "Trouve les JSONL dans tools/structures"}`

  ```
tools/structures/donnees/phrases.json
tools/structures/donnees/gold-analyseur.json
tools/structures/donnees/mesure-analyseur.json
tools/structures/donnees/mesure-corpus.json
tools/structures/donnees/phrases_generees.json
tools/structures/donnees/phrases-corpus-manifest.json
tools/structures/donnees/validations.jsonl
tools/structures/donnees/llm.jsonl
tools/structures/donnees/mesure-arbre.json
tools/structures/donnees/paragraphes.json
tools/structures/donnees/paragraphes-validations.jsonl
---
total 636
drwxr-xr-x. 1 stephane stephane    414  3 nov 16:49 .
drwxr-xr-x. 1 stephane stephane    438  3 nov 16:22 ..
-rw-------. 1 stephane stephane  16806  4 nov 11:42 gold-analyseur.json
-rw-r--r--. 1 stephane stephane    659  3 nov 12:36 llm.jsonl
-rw-r--r--. 1 stephane stephane  21646  4 nov 11:42 mesure-analyseur.json
-rw-r--r--. 1 stephane stephane    886  3 nov 16:23 mesure-arbre.json
-rw-r--r--. 1 stephane stephane   5099  3 nov 18:36 mesure-corpus.json
-rw-r--r--. 1 stephane stephane   7217  4 nov 09:44 paragraphes.json
-rw-r--r--. 1 stephane stephane   6047  4 nov 15:10 paragraphes-validations.jsonl
-rw-r--r--. 1 stephane stephane    366  2 nov 20:35 phrases-corpus-manifest.json
-rw
… [205 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/rapport-s-*.md 2>/dev/null; echo \"---\"; ls reports/ | grep -iE \"rapport-s|paragraphe|retro|lecteur\" | head -40", "description": "Liste les fiches rapport-s et assimilées"}`

  ```
reports/rapport-s-analyseur.md
reports/rapport-s-analyseur-roles.md
reports/rapport-s-arbre-referents.md
reports/rapport-s-banque-partielle.md
reports/rapport-s-corpus-reel.md
reports/rapport-s-fait-divers.md
reports/rapport-s-limites-v6.md
reports/rapport-s-paragraphes.md
reports/rapport-s-traductions.md
---
r03-lecteur-modele-couverture.json
r03-lecteur-modele.json
rapport-lecteur-multifichiers.md
rapport-r03-lecteur-modele.md
rapport-s4-prechargement-moteur.md
rapport-s-analyseur.md
rapport-s-analyseur-roles.md
rapport-s-arbre-referents.md
rapport-s-banque-partielle.md
rapport-schema-v1.md
rapport-s-corpus-reel.md
rapport-semantique.md
rapport-session-2026-09-30.md
rapport-sessions-plans.md
rapport-seuil-reseau.md
rapport-s-fait-divers.md
rapport-s-limites-v6.md
rapport-sommeil-budget.md
rapport-sommeil-deux-nuits.md
rapport-sommeil-selection.md
rapport-sous-familles-autres.md
rapport-spans-chunker.md
rapport-spans-v7.md
rapport-s-paragraphes.md
rapport-speculatif-reflexe.md
rapport-sprint-24h.md
rapport-s-traductions.md
  ```

### 🤖 Assistant

⏵ Lecture du chantier S dans la roadmap et de la session S

- **bash** `{"command": "grep -n \"^## \\|^### \\|^| S\" docs/pilotage/roadmap.md | head -60", "description": "Structure de la roadmap"}`

  ```
13:## Comment lire cette roadmap
26:## En un coup d'œil
54:## L'ordre du jour (carpe diem)
85:## Le Gantt indicatif
138:## Programme A — Le moteur (la drave, les flux)
159:## Programme B — L'intelligence (les deux étages)
187:## Programme N — Le natif (DRVM, `drave-n0`, distillation)
219:## Programme R
231:### Les six phases
242:### R0 — le lecteur v0 (système, sans entraînement)
263:### R1 — la fenêtre native
277:### R2 — la mémoire
287:### R3 — la restitution
297:### R4 — les blocs structurels
309:### R5 — la lecture croisée et le multilingue
316:### Ce que R ne fait pas
333:## La file « jamais en attente »
346:## Ce qui est bloqué, et par quoi
356:| S — la banque validée | **150 verdicts humains** (`tools/structures/donnees/validations.jsonl`) et **19 verdicts sur les paragraphes** (`paragraphes-validations.jsonl`, 10 résolus / 8 exclus / 1 compatible) | poursuivre la validation sur `/paragraphes` (a001–a009 faits) et la rétro-traduction |
358:## Les questions ouvertes
370:## Le détail et l'histoire
  ```

- **bash** `{"command": "grep -n \"S\" docs/pilotage/en-cours.md | grep -iE \"session s|chantier s|lecteur|paragraphe|71 langue|rétro\" | head -40", "description": "Cherche session S dans en-cours"}`

  ```
95:- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
131:**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+ ; **S** — poursuivre la validation ; **N4** — consigne ; **B10.3** — `z` ; **B13** — 178/178 ; **R0.7** — tagger ; **D** — **restauré** : le corpus à **62 documents** (Choquette + Assurance ; DOC1/DOC2, quasi-doublons, écartés) est en place (`data/corpus_ocr_cegep` : train 4 440 987, val 12 536, test 10 524 ; 8 Ko 0, 500 o 0) ; [fiche](../../reports/rapport-ocr-cegep-64.md) ; **la passe complète est finie** (`work/portes/passe-2404-23h45` ; **79 vertes, 4 rouges** : `indice`, `melange` tolérées ; `lecteur` corrigée ; `sessions` → heartbeat de `e181ce02` à rafraîchir).
  ```

- **bash** `{"command": "sed -n '340,375p' docs/pilotage/roadmap.md", "description": "Lis la section S de roadmap"}`

  ```
- **gelé** : **N5** (50–100 M) — après le verdict de R11 sur le schéma ;
- **bloqué, nommé** : B1.5 (corpus d'articles), A3.4 (compte Colab), A5.4 (FPGA), A6.2 (pas de MoE local),
  B10.3 (B10.2bis mesurée, fiche au backlog) ;
- **clos** : B2.6 (le plan multi-tâches), B3 (le plan résiste), B4 (les opérateurs), B5/B6 (les jeux), B7/B8
  (langues et maîtres), C3.2 (familles), N0.3b (parité DRVM ↔ GGUF), B12.10 (intégration, négatif).

## Ce qui est bloqué, et par quoi

| ligne | bloqué par | ce qu'il faudrait |
|---|---|---|
| B1.5 prose scientifique | aucun corpus parallèle humain d'articles FR/EN | un corpus (revue, actes, manuel) traduit par des humains |
| A3.4 Colab | le compte et le runtime Colab | un compte (la recette est dans `docs/archive/colab-reparti.md`) |
| A5.4 FPGA | l'accès au matériel Stratix V | la carte (le design existe) |
| A6.2 MoE local | aucun MoE local ne tient dans 16 Go de VRAM | un MoE qui tient, ou une machine plus grande |
| B10.3 raisonnement sur `z` | le décodeur est sous le plancher chrF | une attention croisée, 20–30 articles, 3 graines |
| R4.4 les scans | pas de **vérité humaine** sur les scans réels : trois vrais scans (Internet Archive) donnent 
… [1499 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"71 langues\\|71 langue\\|rétro-traduction\\|retro-traduction\\|retro_traduction\\|langues\" docs/pilotage/en-cours.md | head -30; echo \"===\"; wc -l docs/pilotage/en-cours.md docs/pilotage/roadmap.md", "description": "Cherche les 71 langues et rétro-traduction"}`

  ```
59:- **Prochaine action** : **reprise** : poursuivre la validation sur `/paragraphes` (a001–a003 faits, 8 restants), puis la rétro-traduction API et les 71 langues.
===
  145 docs/pilotage/en-cours.md
  382 docs/pilotage/roadmap.md
  527 total
  ```

- **bash** `{"command": "sed -n '40,75p' docs/pilotage/en-cours.md", "description": "Lis la section S dans en-cours"}`

  ```
- **Stratégie** : committer par flux.
- **Objectif final** : sédimentation à zéro.
- **Ce qu'elle fait** : intégration ; passe **11 h 30 — 82, 80/2** ; plan de nuit.
- **Ce que font les autres** : **N2**, **S**, **Pensée**.
- **Prochaine action** : reprise par le hub `1e7ef596` ; l'état du 04/11 est la source.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/).

### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures *(en pause)*

- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
- **Rôle** : **S — les structures** : le banc, l'analyseur rôles/subordonnées et l'export.
- **Plan** : analyseur, export, arbre, validation.
- **Ambition** : nommer le rôle et la frontière GN.
- **Stratégie** : une règle = trois contrôles.
- **Objectif final** : gold 60, corpus 60.
- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 tests** ; fiches [analyseur](../../reports/rapport-s-analyseur-roles.
… [1799 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '231,340p' docs/pilotage/roadmap.md", "description": "Lis le programme R / phases et S"}`

  ```
### Les six phases

| phase | livrable | ce qui est mesuré | dépend de |
|---|---|---|---|
| **R0 — le lecteur v0** | [graphe de document](../theorie/glossaire/entrees/graphe-de-document.md), contrôleur classique, banc | exactitude, citation, événements, octets, secondes ; courbe par type | **rien** (modèle externe) |
| **R1 — la fenêtre native** | contexte hiérarchique, curriculum, tokenisation | PPL à 1 000 octets, aiguille native, stabilité | R0, N1 ; plafonné par N2 |
| **R2 — la mémoire** | gist, entités, store épisodique, [relecture](../theorie/glossaire/entrees/relecture.md) | réponse multi-sections, citation, relecture | R1, et le négatif de mémoire (acquis) |
| **R3 — la restitution** | SFT de lecture, réponse/résumé/extraction, citations | exactitude tenue à l'écart, [fidélité](../theorie/glossaire/entrees/fidelite.md) | R0, R2 ; plafonné par N4 |
| **R4 — les blocs structurels** | tableaux ✅, code ✅, maths ✅, vision/OCR 🧱 | extraction exacte, exécution, [layout](../theorie/glossaire/entrees/layout.md) | R0 |
| **R5 — la lecture croisée** | multi-documents, [retrieval](../theorie/glossaire/entrees/retrieval.md), multilingue | comparaison, provenance, traduction | R3 ; enc
… [10217 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des fiches S existantes (traductions, paragraphes, analyseur)

- **bash** `{"command": "wc -l reports/rapport-s-*.md; echo \"===\"; cat reports/rapport-s-traductions.md", "description": "Poids des fiches et lecture traductions"}`

  ```
58 reports/rapport-s-analyseur.md
  137 reports/rapport-s-analyseur-roles.md
  101 reports/rapport-s-arbre-referents.md
  110 reports/rapport-s-banque-partielle.md
   99 reports/rapport-s-corpus-reel.md
   47 reports/rapport-s-fait-divers.md
   78 reports/rapport-s-limites-v6.md
   58 reports/rapport-s-paragraphes.md
  105 reports/rapport-s-traductions.md
  793 total
===
# S — La traduction contrôle le sens : 14/14 référents anaphoriques confirmés par l'anglais, le « les » → « it » retrouvé

> **Ligne de roadmap** : S · **Date** : 2026-11-03 · **Verdict** : les trois paragraphes français
> sont des traductions d'*Alice's Adventures in Wonderland* (1865) ; l'original anglais, qui dit
> explicitement *she / her / herself / it*, tranche les référents que le français laisse flotter.
> Les **14 formes anaphoriques** des trois paragraphes sont confirmées — les **2 que l'outil
> manquait** sont retrouvées (« les » → *it* → les conseils ; « l' » → *it* → la boîte) — et la
> traduction **corrige le contexte** de a003, où Alice n'était pas nommée. La page
> `/paragraphes` affiche désormais la source anglaise à côté du français.

## Le dispositif

Le corpus français (`data/corpus_fr_litteratu
… [6092 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/rapport-s-paragraphes.md", "description": "Lecture fiche paragraphes"}`

  ```
# S — La banque de paragraphes passe à neuf : six paires d'Alice, sources anglaises et référents

> **Ligne de roadmap** : S · **Date** : 2026-11-03 · **Verdict** : la banque passe de **3 à 9
> paragraphes complets**. Les six nouveaux — l'ouverture d'Alice, la table de verre, l'attente à
> la petite porte, « Buvez-moi », « Je me sens toute drôle » et le gâteau oublié — portent chacun
> leur **contexte**, leur **antécédent** (Alice) et leur **source anglaise** (Project Gutenberg
> #11). La page `/paragraphes` en affiche neuf, avec l'arbre, les référents et la source ; les
> **55 tests** passent.

## Les six paires

| id | cible (français) | source (anglais) | réf. |
|---|---|---|---:|
| a004 | « ALICE, assise auprès de sa sœur… commençait à s'ennuyer… » | *Alice was beginning to get very tired…* | 1 |
| a005 | « Tout à coup elle rencontra… une petite table à trois pieds, en verre massif… » | *Suddenly she came upon a little three-legged table…* | 3 |
| a006 | « Comme cela n'avançait à rien… elle retourna vers la table… » | *There seemed to be no use in waiting by the little door…* | 4 |
| a007 | « C'est bien facile à dire « Buvez-moi », mais Alice était trop fine… » | *It was all ve
… [2496 caractères tronqués]
  ```

