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

### 🤖 Assistant

⏵ Recherche des 71 langues UDHR et du prototype L

- **bash** `{"command": "grep -rn \"71 langues\\|71 langue\\|71 lang\\b\" docs/ tools/ reports/ journal/ 2>/dev/null | head -30", "description": "Cherche occurrences des 71 langues"}`

  ```
docs/archive/etat-emulation-professeur.md:144:- chaque canal n'est actif qu'en moyenne dans **5,71 langues sur 6**
docs/archive/roadmap-detail-2026-10-29.md:242:### B7 — Les langues : le même sens dans 71 langues
docs/archive/roadmap-detail-2026-10-29.md:244:La couche de B5 était FR/EN. B7 ajoute un **lexique multilingue** (35 concepts, **71 langues**, **1 433
docs/archive/roadmap-detail-2026-10-29.md:251:| B7.1 | **Le lexique multilingue** (pièces, rangs, enseignes, noms de jeux, notions de maîtres) | ✅ mesuré | **71 langues**, **35 concepts**, **1 433 couples** ; **32 langues fortes** (pièces N/P + un rang et une enseigne) ; source Wikidata, licences CC0 |
docs/archive/roadmap-detail-2026-10-29.md:253:| B7.3 | **Les contrôles** : permutation des libellés, notation, détection | ✅ mesuré | permutation **12/275** items forts restants (**4,4 %**) ; notation **5 112/5 112** (72 items × 71 langues) ; détection des jeux **315/315** |
docs/archive/roadmap-detail-2026-10-29.md:337:| B11.4 | **Données synthétiques / distillation du codec** | ✅ **mesuré** | 10 556 surfaces synthétiques, 71 langues, **aucune surface réelle** à l'entraînement ; test réel **45,1 %** ; **invariance 7,4 %** |
do
… [4620 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"udhr\\|UDHR\\|universal declaration\" docs/ tools/ reports/ data/ 2>/dev/null | head -30", "description": "Cherche corpus UDHR"}`

  ```
docs/archive/campagne-benefices.md
docs/archive/etat-cerveau.md
docs/archive/etat-emulation-professeur.md
docs/archive/note-cancellation-evenementielle.md
docs/archive/note-cout-professeur.md
docs/archive/note-ingestion-corpus.md
docs/archive/note-regle-contrastive.md
docs/archive/roadmap-detail-2026-10-29.md
docs/archive/roadmap-native-2026-10-29.md
docs/schemas/protocole-semantique.svg
docs/methode/rangement.md
docs/methode/resultats.md
docs/pilotage/backlog/B10.2bis-decodeur-attention-croisee.md
docs/pilotage/roadmap.md
docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
docs/theorie/glossaire/entrees/unite.md
docs/theorie/glossaire/index.json
docs/theorie/synthese/06-comment-savoir.md
docs/theorie/synthese/07-modeles-alternatifs-entree-sortie.md
docs/theorie/protocole-semantique.md
docs/theorie/genealogie-des-langues.md
docs/theorie/architecture-native.md
docs/theorie/pre-traitement-linguistique.md
docs/implantation/llm-externe.md
docs/implantation/bloc-linguistique.md
docs/produit/README.md
tools/extrait_udhr.py
tools/extrait_wikipedia.py
tools/leviers_pont.py
tools/corpus_neuf.py
[still running after 60000ms; moved to background job bash-3904]
The command ke
… [127 caractères tronqués]
  ```

- **job_kill** `{"job_id": "bash-3904", "reason": "Recherche trop large dans data/"}`

  ```
requested cancellation of job bash-3904
  ```

- **bash** `{"command": "ls tools/jeux/ | head -40; echo \"===\"; grep -n \"71\\|langues\" tools/jeux/lexique_multilingue.py | head -20", "description": "Liste tools/jeux et lexique multilingue"}`

  ```
codecs
construire_lexique_multilingue.py
corpus_multilingue.py
corpus.py
grammaire.py
hybride.py
__init__.py
lexique_multilingue.json
lexique_multilingue.py
lexique.py
maitres.py
mesure_langues.py
mesure_maitres.py
mesure.py
pensee.py
__pycache__
regles
rsn.py
tests
===
2:"""lexique_multilingue.py — les libellés des jeux, en 53 langues.
13:La recherche est **multi-formes** : n-grammes de 1 à 4 unités pour les langues à
88:        self.langues: list[str] = list(self.donnees["langues"])
159:        On ne parcourt pas les huit domaines : un index unique (forme → langues)
173:        for forme, langues in self._detection.items():
176:                for langue in langues:
197:    def langues_du_concept(self, concept: str) -> list[str]:
223:        """La matrice langues × concepts, et les langues « fortes »."""
224:        par_langue = {l: 0 for l in self.langues}
235:        for l in self.langues:
242:            "langues": len(self.langues),
247:            "moyenne_concepts_par_langue": round(sum(par_langue.values()) / len(self.langues), 2),
248:            "langues_fortes": fortes,
249:            "n_langues_fortes": len(fortes),
  ```

- **bash** `{"command": "sed -n '1,80p' tools/extrait_udhr.py; echo \"===\"; ls data/ | grep -iE \"udhr|langue|multiling\" | head", "description": "Lecture extracteur UDHR et données associées"}`

  ```
#!/usr/bin/env python3
"""extrait_udhr.py — l'UDHR en unités alignées, prêtes à passer dans le moteur.

L'UDHR est le premier corpus parce que l'alignement y est **par construction** :
les 30 articles existent dans les 456 langues, et c'est le même énoncé. Aucun
aligneur, donc aucun décalage possible — le contraire d'un corpus apparié à la
main.

Sortie : un JSON par unité `(article, paragraphe)`, et un index. Chaque unité
porte le texte de CHAQUE langue, pour qu'on puisse la faire passer dans les
couches d'entrée langue par langue et comparer les activations.

Usage :
    extrait_udhr.py <dossier_udhr_xml> <sortie.jsonl> [--min-langues 50]
"""
import glob
import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

NS = "{http://www.unhchr.ch/udhr}"


def texte(el):
    """Le texte d'un élément, espaces normalisés — deux langues n'ont pas les
    mêmes habitudes d'espacement, et ce n'est pas ce qu'on mesure."""
    t = "".join(el.itertext())
    t = unicodedata.normalize("NFC", t)
    return re.sub(r"\s+", " ", t).strip()


def lire(chemin):
    """Rend (code, nom, {cle: texte}) pour une langue. La clé d'un article est
    `a<n>` — c'est l'unit
… [1593 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np='tools/jeux/lexique_multilingue.json'\nd=json.load(open(p))\nprint(type(d), list(d.keys())[:10])\nfor k,v in d.items():\n    if isinstance(v,list):\n        print(k, len(v), v[:5])\n    elif isinstance(v,dict):\n        print(k, 'dict', len(v), list(v)[ … [120 caractères tronqués]`

  ```
<class 'dict'> ['version', 'source', 'date', 'langues', 'variantes', 'concepts', 'manuel']
version 1
source 'Wikidata (CC0), wbgetentities props=labels ; pageprops Wikipédia pour les QID ; libellés normalisés (NFKC, casse pliée,
date '2026-10-26'
langues 71 ['ar', 'bn', 'ca', 'cs', 'da']
variantes dict 3 ['zh', 'pt', 'sr']
concepts dict 35 ['jeu.morpion', 'jeu.echecs', 'jeu.dames', 'jeu.go', 'jeu.cartes']
manuel 1 ['go.passe']
  ```

### 🤖 Assistant

⏵ Comptage et lecture des deux fichiers de verdicts

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nfor p in ['tools/structures/donnees/validations.jsonl','tools/structures/donnees/paragraphes-validations.jsonl']:\n    rows=[]\n    with open(p, encoding='utf-8') as f:\n        for i,l in enumerate(f,1):\n            l=l.strip()\n            … [673 caractères tronqués]`

  ```
==================== tools/structures/donnees/validations.jsonl 150
cles union: ['auteur', 'candidat_id', 'contexte', 'horodatage', 'niveau', 'note', 'phrase_id', 'statut']
  auteur {'humain': 150}
  candidat_id {'p003-c2': 3, 'p002-c2': 2, 'p001-c2': 1, 'p001-c1': 1, 'p002-c1': 1, 'p003-c1': 1, 'p004-c1': 1, 'p004-c2': 1, 'p005-c2': 1, 'p005-c1': 1, 'p006-c1': 1, 'p006-c2': 1}
  contexte {'': 143, "Le détective surveille la maison d'en face. Il a vu l'homme avec le télescope qu'il venait d'acheter — un instrument neuf, encore dans sa boîte.": 3, 'La voisine est partie en vacances. Son chat, lui, est resté sur le toit : il y dort toute la journée, au soleil.': 2, 'Dans ce dessin animé, le canard parle et réclame son dîner : il est prêt à manger, et il le fait savoir.': 2}
  horodatage {'2026-11-03T10:31:17': 1, '2026-11-03T10:31:18': 1, '2026-11-03T10:31:42': 1, '2026-11-03T10:31:46': 1, '2026-11-03T10:32:17': 1, '2026-11-03T10:32:35': 1, '2026-11-03T10:32:37': 1, '2026-11-03T10:32:46': 1, '2026-11-03T10:32:48': 1, '2026-11-03T10:33:14': 1, '2026-11-03T10:33:15': 1, '2026-11-03T10:33:40': 1}
  niveau {'0': 143, '2': 5, '3': 2}
  note {'': 149, "il est préférable de dire l'homme au 
… [3067 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np='tools/structures/donnees/paragraphes.json'\nd=json.load(open(p))\nprint(type(d), list(d.keys())[:10] if isinstance(d,dict) else len(d))\nif isinstance(d,dict):\n    for k,v in d.items():\n        print(k, type(v).__name__, len(v) if hasattr(v,'__len__' … [264 caractères tronqués]`

  ```
<class 'dict'> ['version', 'note', 'source', 'paragraphes', 'note_en', 'source_en_url']
version int 1
note str 254
source str 30
paragraphes list 9
  ex: {"id": "a001", "contexte": "Allons, à quoi bon pleurer ainsi, se dit Alice vivement.", "cible": "Elle avait pour habitude de se donner de très-bons conseils (bien qu'elle les suivît rarement), et quelquefois elle se grondait si fort que les larmes lui en venaient aux yeux.", "antecedent": "Alice", "contexte_en": "\"Come, there's no use in crying like that!\" said Alice to herself, rather sharply; \"I advise you to leave off this minute!\"", "source_en": "She generally gave herself very good advi
note_en str 222
source_en_url str 43
  ```

### 🤖 Assistant

⏵ Cartographie des 19 verdicts et logique de validation de la page

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\np='tools/structures/donnees/paragraphes-validations.jsonl'\nrows=[json.loads(l) for l in open(p,encoding='utf-8') if l.strip()]\nfor r in rows:\n    print(r['horodatage'], r['phrase_id'], r['candidat_id'], r['statut'], '|', r.get('note',''),  … [296 caractères tronqués]`

  ```
2026-11-03T16:49:32 a001 a001-c1 resolu |  | [('Elle', 'Alice'), ('se', 'Alice'), ('elle', 'Alice'), ('lui', 'Alice')]
2026-11-03T16:49:59 a001 a001-c2 resolu |  | [('Elle', 'Alice'), ('se', 'Alice'), ('elle', 'Alice'), ('lui', 'Alice')]
2026-11-03T17:02:06 a002 a002-c1 resolu |  | [('Elle', 'Alice'), ('en', 'Alice'), ('y', 'Alice')]
2026-11-03T17:02:30 a002 a002-c2 exclu |  | [('Elle', 'Alice'), ('en', 'Alice'), ('y', 'Alice')]
2026-11-03T17:02:43 a002 a002-c3 exclu |  | [('Elle', 'Alice'), ('en', 'Alice'), ('y', 'Alice')]
2026-11-03T17:05:31 a003 a003-c1 exclu |  | [('Elle', 'Alice'), ('sa', 'Alice'), ('elle', 'Alice'), ('se', 'Alice')]
2026-11-03T17:05:40 a003 a003-c2 resolu |  | [('Elle', 'Alice'), ('sa', 'Alice'), ('elle', 'Alice'), ('se', 'Alice')]
2026-11-03T17:06:16 a003 a003-c3 exclu |  | [('Elle', 'Alice'), ('sa', 'Alice'), ('elle', 'Alice'), ('se', 'Alice')]
2026-11-04T15:03:43 a004 a004-c1 resolu |  | [('sa', 'ALICE')]
2026-11-04T15:04:02 a004 a004-c2 exclu |  | [('sa', 'ALICE')]
2026-11-04T15:06:12 a005 a005-c1 resolu |  | [('elle', 'Alice'), ('son', 'Alice'), ('en', 'coup')]
2026-11-04T15:06:26 a005 a005-c2 exclu |  | [('elle', 'Alice'), ('son', 'Alice'), ('en', 'coup
… [1230 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"valid\\|paragraphe\\|candidat\" tools/structures/serveur.py | head -60", "description": "Cherche la logique de validation dans serveur.py"}`

  ```
4:Le serveur expose les phrases et leurs interprétations candidates, enregistre les verdicts
5:humains (`donnees/validations.jsonl`), interroge un grand modèle (`donnees/llm.jsonl`) et exporte
6:la banque validée (`/api/export`).
10:    #   /paragraphes les paragraphes complets : arbre SVG, référents, verdict
33:NIVEAUX = {0: "sans contexte", 1: "phrase d'avant", 2: "paragraphe", 3: "section / document",
41:    """Les phrases fixes + deux journaux append-only : validations humaines et évaluations LLM."""
47:        self.fichier_paragraphes = self.dossier / "paragraphes.json"
53:    def paragraphes(self) -> list[dict]:
54:        """Les paragraphes complets : cible, contexte, antécédent, candidats, référents, arbre SVG."""
55:        if not self.fichier_paragraphes.exists():
57:        source = json.loads(self.fichier_paragraphes.read_text(encoding="utf-8"))
58:        validations = self._journal("paragraphes-validations.jsonl")
60:        for p in source.get("paragraphes", []):
70:                "candidats": cands, "referents": refs,
73:                "validations": [v for v in validations if v.get("phrase_id") == p["id"]],
77:    def valider_paragraphe(self, phrase_id: str, cand
… [3009 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"valid\\|statut\\|restant\\|fait\\|référent\\|structure\\|candidat\" tools/structures/static/paragraphes.html | head -60; echo \"===\"; wc -l tools/structures/static/paragraphes.html tools/structures/static/paragraphes.js", "description": "Examine la page paragraphes"}`

  ```
43:  .refs-validees { color: #6b4f12; font-size: .88em; margin: 0 20px 12px; }
50:    <p class="sous">Neuf paragraphes complets : l'arbre, les référents à trancher, puis le verdict.
56:    <div><strong id="s-valides">–</strong><span>verdicts</span></div>
69:  <span class="astuce">l'indentation = la profondeur réelle ; les flèches pointillées = référents → antécédent ; l'arbre défile dans son cadre</span>
71:  <span class="astuce">tranchez d'abord les référents, puis la structure ; le verdict garde les deux</span>
===
  77 tools/structures/static/paragraphes.html
 117 tools/structures/static/paragraphes.js
 194 total
  ```

- **bash** `{"command": "grep -n \"statut\\|valid\\|restant\\|fetch\\|api\" tools/structures/static/paragraphes.js | head -80", "description": "Examine le JS de la page"}`

  ```
26:  const v = (p.validations || []).filter((x) => x.candidat_id === c.id);
59:  const vals = ps.reduce((n, p) => n + (p.validations || []).length, 0);
60:  const ok = ps.reduce((n, p) => n + (p.validations || [])
61:    .filter((v) => ["resolu", "compatible", "double_sens"].includes(v.statut)).length, 0);
63:  $("#s-valides").textContent = vals;
68:      const badge = v ? `<span class="verdict ${v.statut}">${v.statut.replace("_", " ")}</span>` : "";
81:        ${refsV ? `<p class="refs-validees">référents enregistrés : ${refsV}</p>` : ""}
96:  etat = await (await fetch("/api/paragraphes")).json();
109:  await fetch("/api/valider-paragraphe", {
112:      statut: b.dataset.s, referents, note }),
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('tools/structures/donnees/paragraphes.json'))\ntot=0\nfor p in d['paragraphes']:\n    print(p['id'], len(p.get('candidats',[])), [c['id'] for c in p.get('candidats',[])], '| refs:', len(p.get('referents',{})))\n    tot+=len(p.get('candida … [99 caractères tronqués]`

  ```
a001 0 [] | refs: 0
a002 0 [] | refs: 0
a003 0 [] | refs: 0
a004 0 [] | refs: 0
a005 0 [] | refs: 0
a006 0 [] | refs: 0
a007 0 [] | refs: 0
a008 0 [] | refs: 0
a009 0 [] | refs: 0
total candidats 0
  ```

- **bash** `{"command": "sed -n '50,85p' tools/structures/static/paragraphes.html; echo \"===\"; sed -n '1,60p' tools/structures/serveur.py", "description": "Lis la structure HTML et le début du serveur"}`

  ```
<p class="sous">Neuf paragraphes complets : l'arbre, les référents à trancher, puis le verdict.
      Le contexte ne se devine plus, il est là.</p>
    <p class="nav"><a href="/">← le banc de phrases</a></p>
  </div>
  <div class="stats">
    <div><strong id="s-par">–</strong><span>paragraphes</span></div>
    <div><strong id="s-valides">–</strong><span>verdicts</span></div>
    <div><strong id="s-ok">–</strong><span>acceptés</span></div>
    <a class="export" href="/api/paragraphes-export" download>⤓ exporter les verdicts</a>
  </div>
</header>

<section class="legende">
  <span class="leg t-GN">GN</span> groupe nominal
  <span class="leg t-GV">GV</span> groupe verbal
  <span class="leg t-GP">GP</span> groupe prépositionnel
  <span class="leg t-REL">REL</span> relative
  <span class="leg t-SUB">SUB</span> subordonnée
  <span class="sep">·</span>
  <span class="astuce">l'indentation = la profondeur réelle ; les flèches pointillées = référents → antécédent ; l'arbre défile dans son cadre</span>
  <span class="sep">·</span>
  <span class="astuce">tranchez d'abord les référents, puis la structure ; le verdict garde les deux</span>
</section>

<main id="paragraphes"></main>
<script src
… [2705 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '53,130p' tools/structures/serveur.py", "description": "Lis la construction des candidats de paragraphes"}`

  ```
def paragraphes(self) -> list[dict]:
        """Les paragraphes complets : cible, contexte, antécédent, candidats, référents, arbre SVG."""
        if not self.fichier_paragraphes.exists():
            return []
        source = json.loads(self.fichier_paragraphes.read_text(encoding="utf-8"))
        validations = self._journal("paragraphes-validations.jsonl")
        sortie = []
        for p in source.get("paragraphes", []):
            cands = generateur.analyser(p["cible"])
            for k, c in enumerate(cands, 1):
                c["id"] = f'{p["id"]}-c{k}'
            refs = generateur.referents(p["cible"], p.get("contexte", ""))
            liens = tuple(dict.fromkeys(r["forme"] for r in refs))
            sortie.append({
                "id": p["id"], "contexte": p.get("contexte", ""), "cible": p["cible"],
                "antecedent": p.get("antecedent", ""),
                "contexte_en": p.get("contexte_en", ""), "source_en": p.get("source_en", ""),
                "candidats": cands, "referents": refs,
                "svg": arbre_svg.svg_arbre(p["cible"], p.get("contexte", ""),
                                           p.get("antecedent", ""), liens=liens),
       
… [3066 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,117p' tools/structures/static/paragraphes.js", "description": "Lis tout le JS paragraphes"}`

  ```
const $ = (s) => document.querySelector(s);
const esc = (t) => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const STATUTS = [["resolu", "✓ résolu"], ["compatible", "~ compatible"],
                 ["exclu", "✗ exclu"], ["double_sens", "⇄ double sens"]];
let etat = { paragraphes: [] };

function phraseColoree(p, cand) {
  let html = "", curseur = 0;
  for (const s of cand.segments) {
    if (s.debut > curseur) html += esc(p.cible.slice(curseur, s.debut));
    html += `<span class="seg t-${s.type}" title="${s.type} · ${s.role}">${esc(s.texte)}</span>`;
    curseur = s.fin;
  }
  if (curseur < p.cible.length) html += esc(p.cible.slice(curseur));
  return html;
}

function blocs(cand) {
  return cand.segments.map((s) =>
    `<div class="bloc" style="margin-left:${s.niveau * 1.4}em">
       <span class="t-${s.type}">${esc(s.texte.trim())}</span>
       <em>${s.type} · ${s.role} · profondeur ${s.profondeur ?? s.niveau}</em></div>`).join("");
}

function dernier(p, c) {
  const v = (p.validations || []).filter((x) => x.candidat_id === c.id);
  return v.length ? v[v.length - 1] : null;
}

function referentsDe(p) {
  const uniques = new Map();
  for (const 
… [4018 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"8 restants\\|a010\\|a001–a009\\|a001-a009\\|a001–a003\" docs/ reports/ journal/ tools/ 2>/dev/null | head -20", "description": "Cherche les 8 restants et a010"}`

  ```
docs/pilotage/chantiers.md:87:| **S — les structures** | quelles structures d'interprétation candidates, et lesquelles un humain valide ? | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests**, gold **60**, corpus **60**, banque **84/67**, page **`/paragraphes`** ; **h050/h053** et le fait divers **fermés** | **poursuivre la validation sur `/paragraphes`** (a001–a003 faits) ; rétro-traduction API | L (annotations), D (corpus), B (sens) | L (banque), B (pragmatique), D (corpus) |
docs/pilotage/roadmap.md:34:| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tranché (la tête du GN arrête le verbe) ; [fiche](../../reports/rapport-s-fait-divers.md). **v6** : h050, h053 et « si fort que » **fermés**, gold **60** (vague 5) ; **60/60** types, **142/142** rôles, **50/50** compléments, couverture 1,00 ; corpus 65,5 %/9,1 %, 596/1 184 homographes ; **55 tests**. **v5** : arbre parent/enfant (**99 candidats à ≥3**, 37 à 1) et **référents proposés** (294/371 formes, 77 sans contexte) ; **SVG** d'Alice, page **`/paragraphes`** (arbre, référents, verdict), **traduction** 
… [6054 caractères tronqués]
  ```

- **bash** `{"command": "cd tools/structures && python3 - <<'EOF'\nimport json, generateur\nsrc=json.load(open('donnees/paragraphes.json'))\nvals=[json.loads(l) for l in open('donnees/paragraphes-validations.jsonl',encoding='utf-8') if l.strip()]\nfor p in src['paragraphes']:\n    cands=generateur.analyser(p['c … [396 caractères tronqués]`

  ```
a001 candidats 2 ['a001-c1', 'a001-c2'] | vus 2 | restants []
   noms: ['« de très-bons conseils » → habitude', '« de très-bons conseils » → se donner']
a002 candidats 3 ['a002-c1', 'a002-c2', 'a002-c3'] | vus 3 | restants []
   noms: ['« de Corinthe » → raisins', '« de Corinthe » → un tout petit gâteau', '« de Corinthe » → étaient admirablement tracés']
a003 candidats 3 ['a003-c1', 'a003-c2', 'a003-c3'] | vus 3 | restants []
   noms: ['« sur sa tête » → gâteau', '« sur sa tête » → sa main', '« sur sa tête » → portant']
a004 candidats 2 ['a004-c1', 'a004-c2'] | vus 2 | restants []
   noms: ['« à ne rien faire » → rester', '« à ne rien faire » → commençait']
a005 candidats 2 ['a005-c1', 'a005-c2'] | vus 2 | restants []
   noms: ['« à trois pieds » → table', '« à trois pieds » → elle rencontra']
a006 candidats 1 ['a006-c1'] | vus 1 | restants []
   noms: ['« vers la table » → elle retourna']
a007 candidats 2 ['a007-c1', 'a007-c2'] | vus 2 | restants []
   noms: ["« à l'aveuglette » → obéir", "« à l'aveuglette » → Alice était trop fine"]
a008 candidats 1 ['a008-c1'] | vus 1 | restants []
   noms: ['structure la plus proche']
a009 candidats 3 ['a009-c1', 'a009-c2', 'a009-c3'] | vus 3 |
… [116 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Analyse fine des 150 verdicts et de la couverture de la banque

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nrows=[json.loads(l) for l in open('tools/structures/donnees/validations.jsonl',encoding='utf-8') if l.strip()]\nprint('n lignes',len(rows))\n# unique pairs & last\nlast={}\nfor r in rows: last[(r['phrase_id'],r['candidat_id'])]=r\nprint('pair … [1303 caractères tronqués]`

  ```
n lignes 150
paires uniques 147
phrases uniques 74
candidats uniques 147
statuts derniers: Counter({'resolu': 73, 'exclu': 63, 'compatible': 11})
statuts toutes lignes: Counter({'resolu': 74, 'exclu': 64, 'compatible': 11, 'double_sens': 1})
niveaux derniers: Counter({0: 141, 2: 4, 3: 2})
avec contexte: 6
avec note: 1
auteurs: Counter({'humain': 150})
paires revues >1: [(('p002', 'p002-c2'), 2), (('p003', 'p003-c2'), 3)]
niveau 0 {'resolu': 70, 'exclu': 62, 'compatible': 9} n= 141
niveau 2 {'exclu': 1, 'resolu': 2, 'compatible': 1} n= 4
niveau 3 {'resolu': 1, 'compatible': 1} n= 2
phrases avec 1/2/3 candidats jugés: Counter({2: 39, 1: 18, 3: 17})
phrases >1 candidat: [('p001', ['p001-c1', 'p001-c2']), ('p002', ['p002-c1', 'p002-c2']), ('p003', ['p003-c1', 'p003-c2']), ('p004', ['p004-c1', 'p004-c2']), ('p005', ['p005-c1', 'p005-c2']), ('p006', ['p006-c1', 'p006-c2']), ('p007', ['p007-c1', 'p007-c2']), ('c002', ['c002-c1', 'c002-c2']), ('c004', ['c004-c1', 'c004-c2']), ('c007', ['c007-c1', 'c007-c2']), ('c008', ['c008-c1', 'c008-c2']), ('c009', ['c009-c1', 'c009-c2', 'c009-c3']), ('c011', ['c011-c1', 'c011-c2']), ('c013', ['c013-c1', 'c013-c2', 'c013-c3']), ('c014', ['c014-c1', 'c01
… [189 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfixe=json.load(open('tools/structures/donnees/phrases.json'))\ngen=json.load(open('tools/structures/donnees/phrases_generees.json'))\nprint('phrases.json cles',list(fixe.keys()),'n',len(fixe['phrases']))\nprint('gen cles',list(gen.keys()),'n',len(gen['phr … [459 caractères tronqués]`

  ```
phrases.json cles ['version', 'note', 'phrases'] n 7
gen cles ['version', 'note', 'source', 'phrases'] n 200
total phrases 207
total candidats 369
phrase ids ex ['p001', 'p002', 'p003', 'p004', 'p005', 'p006', 'p007', 'c001', 'c002', 'c003']
gen ids ex ['c001', 'c002', 'c003', 'c004', 'c005', 'c006', 'c007', 'c008', 'c009', 'c010']
candidats/phrase Counter({1: 86, 2: 80, 3: 41})
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nrows=[json.loads(l) for l in open('tools/structures/donnees/validations.jsonl',encoding='utf-8') if l.strip()]\nfixe=json.load(open('tools/structures/donnees/phrases.json'))\ngen=json.load(open('tools/structures/donnees/phrases_generees.json' … [1580 caractères tronqués]`

  ```
verdicts sur candidats inconnus/actuels: 0 []
phrases jugees en entier 74 partielles 0 sans verdict 133
candidats jugés 147 / 369 = 39.8 %
phrases touchées 207 / 207 = 100.0 %
p jugées 7 /7; c jugées 200 /200
p full 7 c full 67

REVISIONS:
2026-11-03T10:31:46 p002 p002-c2 double_sens 2 Le détective surveille la maison d'en face. Il a v
2026-11-03T10:32:17 p002 p002-c2 compatible 2 Le détective surveille la maison d'en face. Il a v
2026-11-03T10:32:37 p003 p003-c2 exclu 0 
2026-11-03T16:39:24 p003 p003-c2 resolu 0 
2026-11-03T16:40:00 p003 p003-c2 exclu 0
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nrows=[json.loads(l) for l in open('tools/structures/donnees/validations.jsonl',encoding='utf-8') if l.strip()]\n# distribution over time, per day, per phrase prefix\nprint('jours:',collections.Counter(r['horodatage'][:10] for r in rows))\npri … [464 caractères tronqués]`

  ```
jours: Counter({'2026-11-03': 150})
heures 11-03: Counter({'13': 41, '11': 40, '12': 34, '10': 27, '16': 8})
prefixes phrases: Counter({'c': 133, 'p': 17})
2026-11-03T10:31:17 p001 p001-c2 exclu niv 2 | La voisine est partie en vacances. Son chat, lui, est resté sur le toit : il y dort toute 
2026-11-03T10:31:18 p001 p001-c1 resolu niv 2 | La voisine est partie en vacances. Son chat, lui, est resté sur le toit : il y dort toute 
2026-11-03T10:31:42 p002 p002-c1 resolu niv 2 | Le détective surveille la maison d'en face. Il a vu l'homme avec le télescope qu'il venait
2026-11-03T10:31:46 p002 p002-c2 double_sens niv 2 | Le détective surveille la maison d'en face. Il a vu l'homme avec le télescope qu'il venait
2026-11-03T10:32:17 p002 p002-c2 compatible niv 2 | Le détective surveille la maison d'en face. Il a vu l'homme avec le télescope qu'il venait
2026-11-03T10:34:04 p007 p007-c1 resolu niv 3 | Dans ce dessin animé, le canard parle et réclame son dîner : il est prêt à manger, et il l
2026-11-03T10:34:09 p007 p007-c2 compatible niv 3 | Dans ce dessin animé, le canard parle et réclame son dîner : il est prêt à manger, et il l
  ```

- **bash** `{"command": "sed -n '128,180p' tools/structures/serveur.py; echo \"===\"; sed -n '180,240p' tools/structures/serveur.py", "description": "Lis niveaux minimaux et export du serveur"}`

  ```
def niveaux_minimaux(self) -> dict:
        """Le plus petit niveau de contexte où une lecture a été *tranchée* (résolue ou exclue).

        C'est la mesure de « combien de contexte il faut » : 0 = la phrase seule suffit,
        2 = il faut le paragraphe, 3 = le document, 4 = le genre.
        """
        decisifs = {}
        for v in self._journal("validations.jsonl"):
            if v.get("statut") not in ("resolu", "exclu"):
                continue
            pid = v["phrase_id"]
            n = int(v.get("niveau", 0))
            decisifs[pid] = min(decisifs.get(pid, 9), n)
        return decisifs

    def evaluer(self, phrase_id: str, fournisseur: str = "baseline", contexte: str = "",
                niveau: int = 0) -> dict:
        phrase = next((p for p in self.phrases if p["id"] == phrase_id), None)
        if phrase is None:
            raise KeyError(f"phrase inconnue : {phrase_id}")
        r = llm.evaluer(phrase["texte"], phrase["candidats"], fournisseur, contexte, niveau)
        ligne = {"phrase_id": phrase_id, **r, "horodatage": time.strftime("%Y-%m-%dT%H:%M:%S")}
        with self.verrou:
            with (self.dossier / "llm.jsonl").open("a", encoding="utf-8"
… [4125 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nrows=[json.loads(l) for l in open('tools/structures/donnees/validations.jsonl',encoding='utf-8') if l.strip()]\nlast={}\nfor r in rows: last[(r['phrase_id'],r['candidat_id'])]=r\nfor pref in ['p','c']:\n    sub=[v for (p,c),v in last.items()  … [492 caractères tronqués]`

  ```
p 14 Counter({'resolu': 7, 'compatible': 4, 'exclu': 3})
  contextes: Counter({False: 8, True: 6})
c 133 Counter({'resolu': 66, 'exclu': 60, 'compatible': 7})
  contextes: Counter({False: 133})

phrases contexte:
p001 [('p001-c2', 'exclu'), ('p001-c1', 'resolu')]
p002 [('p002-c1', 'resolu'), ('p002-c2', 'compatible')]
p003 [('p003-c1', 'resolu'), ('p003-c2', 'exclu')]
p004 [('p004-c1', 'resolu'), ('p004-c2', 'compatible')]
p005 [('p005-c2', 'resolu'), ('p005-c1', 'exclu')]
p006 [('p006-c1', 'resolu'), ('p006-c2', 'compatible')]
p007 [('p007-c1', 'resolu'), ('p007-c2', 'compatible')]
  ```

### 🤖 Assistant

⏵ Inventaire des 71 langues, de l'UDHR et des mesures B7

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('tools/jeux/lexique_multilingue.json'))\nlangs=d['langues']\nprint('n langues',len(langs))\nprint(langs)\nprint('concepts',len(d['concepts']),'couples',sum(len(v) for v in d['concepts'].values()) if isinstance(d['concepts'],dict) else '?' … [537 caractères tronqués]`

  ```
n langues 71
['ar', 'bn', 'ca', 'cs', 'da', 'de', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'gl', 'he', 'hi', 'hr', 'hu', 'id', 'is', 'it', 'ja', 'ka', 'kk', 'ko', 'lt', 'lv', 'mk', 'ms', 'mt', 'nb', 'nl', 'nn', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'sq', 'sr', 'sv', 'sw', 'ta', 'th', 'tr', 'uk', 'ur', 'vi', 'zh', 'af', 'am', 'az', 'be', 'bs', 'cy', 'ga', 'hy', 'km', 'ky', 'lo', 'mn', 'ne', 'pa', 'si', 'so', 'uz', 'yo', 'zu']
concepts 35 couples 105
variantes {'zh': ['zh-hans', 'zh-cn', 'zh-sg', 'zh-hant'], 'pt': ['pt-br'], 'sr': ['sr-ec', 'sr-el']}
source Wikidata (CC0), wbgetentities props=labels ; pageprops Wikipédia pour les QID ; libellés normalisés (NFKC, casse pliée, accents retirés, parenthèses retirées)
langues avec items: 4 min 1 max 35
fortes (>=?): [('qid', 35), ('qids', 34), ('labels', 35)]
distribution Counter({35: 2, 34: 1, 1: 1})
  ```

- **bash** `{"command": "ls data/udhr | head -5; echo \"...\"; ls data/udhr | wc -l; echo \"===\"; ls data/udhr/*.jsonl 2>/dev/null | head; find data/udhr -maxdepth 1 -type f | sed 's/.*\\.//' | sort | uniq -c", "description": "Compte les fichiers UDHR"}`

  ```
articles.jsonl
articles_propres.jsonl
_eng.txt
familles
_fra.txt
...
18
===
data/udhr/articles.jsonl
data/udhr/articles_propres.jsonl
data/udhr/langues.jsonl
      2 json
      3 jsonl
     12 txt
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nd=json.load(open('tools/jeux/lexique_multilingue.json'))\nprint(type(d['concepts']), len(d['concepts']))\nk=next(iter(d['concepts']))\nprint('ex concept',k, type(d['concepts'][k]), json.dumps(d['concepts'][k],ensure_ascii=False)[:300])\nprint … [676 caractères tronqués]`

  ```
<class 'dict'> 35
ex concept jeu.morpion <class 'dict'> {"qid": "Q210339", "qids": ["Q210339"], "labels": {"ar": ["لعبة اكس-او"], "ca": ["tres en ratlla"], "cs": ["piskvorky"], "da": ["kryds og bolle"], "de": ["tic-tac-toe"], "en": ["tic-tac-toe"], "eo": ["tiktakto"], "es": ["tres en raya"], "et": ["trips-traps-trull"], "eu": ["hiruko artzain-joko"], "fa
keys first ['jeu.morpion', 'jeu.echecs', 'jeu.dames', 'jeu.go', 'jeu.cartes']
langues avec >=1 concept: 4 couples concept-langue: 105 items 106
distribution concepts/langue: Counter({35: 2, 34: 1, 1: 1})
fortes >=5: 3
langues faibles: [('manuel', 1)]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor p in ['data/udhr/langues.jsonl','data/udhr/articles_propres.jsonl','data/udhr/articles.jsonl']:\n    rows=[json.loads(l) for l in open(p,encoding='utf-8') if l.strip()]\n    print('='*10,p,len(rows))\n    print('cles',list(rows[0].keys()))\n    print( … [96 caractères tronqués]`

  ```
========== data/udhr/langues.jsonl 456
cles ['fichier', 'iso3', 'nom', 'script', 'sens', 'titre', 'nb_articles', 'preambule_car', 'attrs']
{"fichier": "udhr_007.xml", "iso3": "cri", "nom": "Sãotomense", "script": "Latn", "sens": "ltr", "titre": "Declaraçón Universal di Dirêtu di Hómé", "nb_articles": 30, "preambule_car": 1593, "attrs": "iso639-3=cri key=007 n=Sãotomense dir=ltr iso15924=Latn"}
========== data/udhr/articles_propres.jsonl 13222
cles ['fichier', 'iso3', 'nom', 'script', 'art', 'texte', 'variante']
{"fichier": "udhr_007.xml", "iso3": "cri", "nom": "Sãotomense", "script": "Latn", "art": 1, "texte": "Tudu nguê di mundu ca nancê livli e igual ni dignidade e ni dirêtu. Punda nen ca pensá e nen tê cunxensa, selá nen fé tudu cuá cu tençón de lumón.", "variante": "007"}
========== data/udhr/articles.jsonl 13996
cles ['fichier', 'iso3', 'nom', 'script', 'art', 'titre', 'texte']
{"fichier": "udhr_007.xml", "iso3": "cri", "nom": "Sãotomense", "script": "Latn", "art": 0, "titre": "Préambule", "texte": "Punda dignidade di tudo nguê di mundu e dirêtu d'inem igual e andeji cu a na pô bêndê fa sá stê di liberdade, di justiça e di paz ni mundu; Punda fata di conheximentu e displêzu di
… [95 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nd=json.load(open('tools/jeux/lexique_multilingue.json'))\nlangs=d['langues']\nc=collections.Counter(); items=0; manuel=0\nfor concept,v in d['concepts'].items():\n    labels=v.get('labels',{})\n    for l,forms in labels.items():\n        c[l] … [588 caractères tronqués]`

  ```
langues déclarées: 71
langues avec >=1 label: 75
couples concept-langue: 1433
formes (surfaces): 1491
distribution labels/langue: [(1, 5), (2, 1), (3, 2), (4, 3), (5, 1), (6, 2), (9, 1), (10, 2), (11, 1), (12, 1), (13, 1), (14, 4), (15, 3), (16, 5), (17, 1), (18, 2), (19, 3), (20, 2), (21, 2), (22, 2), (23, 2), (24, 1), (25, 2), (26, 3), (27, 3), (28, 3), (30, 2), (31, 5), (32, 5), (33, 1), (34, 2), (35, 2)]
fortes >=? {1: 75, 5: 64, 10: 60, 15: 51, 20: 37, 25: 28, 30: 17, 34: 4}
faibles <=2: 2 ['ky', 'lo']
absentes: []
  ```

- **bash** `{"command": "sed -n '1,120p' tools/jeux/mesure_langues.py", "description": "Lis le script de mesure des langues"}`

  ```
#!/usr/bin/env python3
"""mesure_langues.py — 71 langues, le même sens.

Trois mesures, trois contrôles :
1. **couverture** : combien de concepts du lexique ont un libellé dans combien
   de langues (Wikidata, 35 concepts, 71 langues) ;
2. **corpus** : les surfaces multilingues du corpus (pièces, cartes, noms de
   jeux + coordonnées), lues au niveau 4, comparées à la RSN attendue ;
3. **invariance** : les variantes d'une même paire (le même coup dans toutes
   les langues) doivent donner la même empreinte.

Contrôles : **permutation** des libellés entre concepts (le sens doit
s'effondrer), **notation** (les 112 items de notation sont lus dans chacune des
71 langues : la notation ne dépend pas de la langue), et **détection** des noms
de jeux.
"""
from __future__ import annotations

import time
from collections import Counter, defaultdict

from .codecs import base as B
from .codecs import cartes as CC
from .codecs import dames as CD
from .codecs import echecs as CE
from .codecs import go as CG
from .codecs import morpion as CM
from .codecs import detecte_jeu, lit
from .corpus import construire_corpus
from .corpus_multilingue import construire_corpus_multilingue
from .lexique_multili
… [3209 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '120,260p' tools/jeux/mesure_langues.py", "description": "Lis la fin du script de mesure des langues"}`

  ```
return {"total": total, "bons": bons, "par_jeu": par_jeu}


def _langue_detectee() -> dict:
    corpus = construire_corpus_multilingue()
    exacts = 0
    for it in corpus.items:
        lec = lit(it.texte, jeu=it.jeu, niveau=4, contexte=it.contexte)
        if lec.langue == it.langue:
            exacts += 1
    return {"items": len(corpus.items), "exacts": exacts}


_NOTATION_CARTE = __import__("re").compile(r"^[2-9TJQKA][CDHS]$")


def _est_notation(it) -> bool:
    """La surface est-elle une notation, indépendante de la langue ?"""
    import re
    t = it.texte.strip()
    f = it.format
    if f in ("fen", "grille", "diagramme", "compact", "donne", "pgn", "sgf",
             "gtp", "uci", "algebrique"):
        return True
    if f == "san":
        return bool(re.fullmatch(r"(?:O-O(?:-O)?|[KQRBNCDFT]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#]?)", t))
    if f == "numerique":
        return bool(re.fullmatch(r"[a-h]?[1-9][0-9]?(?:x[a-h]?[1-9][0-9]?)*(?:[-][1-9][0-9]?)?", t))
    if f == "cellule":
        return bool(re.fullmatch(r"[A-Ca-c][1-3]|\(\d,\d\)|\d \d", t))
    if f == "carte":
        return bool(_NOTATION_CARTE.fullmatch(t))
    if f == "liste":
        return all(_
… [2488 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('tools/jeux/lexique_multilingue.json'))\nlangs=set(d['langues'])\nalll=set()\nfor v in d['concepts'].values(): alll|=set(v.get('labels',{}))\nprint('déclarées',len(langs),'labels',len(alll))\nprint('hors liste:',sorted(alll-langs))\nprint … [248 caractères tronqués]`

  ```
déclarées 71 labels 75
hors liste: ['pt-br', 'sr-ec', 'zh-hans', 'zh-hant']
déclarées sans label: []
pt-br 1
sr-ec 1
zh-hans 1
zh-hant 1
  ```

### 🤖 Assistant

⏵ Exécution lecture-seule de la mesure des 71 langues

- **bash** `{"command": "PYTHONDONTWRITEBYTECODE=1 timeout 180 python3 -m tools.jeux.mesure_langues 2>&1 | tail -120", "description": "Mesure les 71 langues sans écrire", "timeoutMs": 200000}`

  ```
},
   "ga": {
    "items": 3,
    "bons": 3,
    "forts": 2,
    "forts_bons": 2
   },
   "hy": {
    "items": 5,
    "bons": 5,
    "forts": 2,
    "forts_bons": 2
   },
   "km": {
    "items": 1,
    "bons": 1,
    "forts": 1,
    "forts_bons": 1
   },
   "mn": {
    "items": 4,
    "bons": 4,
    "forts": 2,
    "forts_bons": 2
   },
   "ne": {
    "items": 2,
    "bons": 2,
    "forts": 2,
    "forts_bons": 2
   },
   "pa": {
    "items": 1,
    "bons": 1,
    "forts": 0,
    "forts_bons": 0
   },
   "so": {
    "items": 1,
    "bons": 1,
    "forts": 1,
    "forts_bons": 1
   },
   "uz": {
    "items": 4,
    "bons": 4,
    "forts": 2,
    "forts_bons": 2
   },
   "zu": {
    "items": 1,
    "bons": 1,
    "forts": 0,
    "forts_bons": 0
   }
  },
  "minimum": 1.0,
  "maximum": 1.0
 },
 "invariance": {
  "paires": 11,
  "invariantes": 11,
  "detail": {
   "ml-cartes-10h": 1,
   "ml-cartes-ah": 1,
   "ml-cartes-jc": 1,
   "ml-cartes-ks": 1,
   "ml-cartes-qd": 1,
   "ml-dames-b6c5": 1,
   "ml-echecs-e4": 1,
   "ml-echecs-nf3": 1,
   "ml-go-d4": 1,
   "ml-go-passe": 1,
   "ml-morpion-a1": 1
  }
 },
 "permutation": {
  "items": 449,
  "bons": 186,
  "forts": 275,
  "forts_bons": 1
… [495 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-langues-maitres.md", "description": "Lis la fiche langues et maîtres"}`

  ```
# B7/B8 — 71 langues pour les jeux, et les livres des maîtres mesurés

> Mesure du **26/10/2026**, sur `Hauru` (Python 3.13, sans GPU), `tools/jeux/` et
> `tools/porte-jeux.sh`. Deux extensions de B5/B6 : un **lexique multilingue** de 35 concepts dans
> **71 langues** (Wikidata, CC0) et une **base de 17 principes** tirés de neuf sources (sept ouvrages du
> domaine public, les proverbes traditionnels du go, le morpion résolu), avec leurs évaluations, leur livre,
> leurs parties et leurs politiques. JSON bruts :
> [`jeux-langues-mesures.json`](jeux-langues-mesures.json) et
> [`jeux-maitres-mesures.json`](jeux-maitres-mesures.json). Concept :
> [`docs/theorie/jeux-symboliques.md`](../docs/theorie/jeux-symboliques.md). Durées : **3,1 s** (langues), **468,8 s**
> (maîtres), **188,7 s** (jeux, régénéré avec le lexique Unicode).

## Ce qui est mesuré

1. **Les langues** — le même sens (pièce + cases, rang + enseigne, nom du jeu + coordonnée) dans 71 langues ;
   couverture du corpus au niveau 4, invariance inter-langues, contrôle par permutation des libellés,
   notation indépendante de la langue, détection des noms de jeux.
2. **Les maîtres** — 17 principes encodés dans la pensée, et ce 
… [5148 caractères tronqués]
  ```

- **bash** `{"command": "PYTHONDONTWRITEBYTECODE=1 python3 - <<'EOF'\nimport json\nfrom tools.jeux.mesure_langues import mesure_langues\nr=mesure_langues(rapide=True)\nc=r['couverture']\nprint('COUVERTURE cles:',list(c.keys()))\nfor k in ['langues','concepts','couples','moyenne_concepts_par_langue','n_langues_f … [913 caractères tronqués]`

  ```
COUVERTURE cles: ['langues', 'concepts', 'couples', 'par_concept', 'par_langue', 'moyenne_concepts_par_langue', 'langues_fortes', 'n_langues_fortes', 'pieces', 'rangs', 'couleurs', 'jeux']
langues 71
concepts 35
couples 1433
moyenne_concepts_par_langue 20.13
n_langues_fortes 32
langues_fortes 32 ['ar', 'bn', 'ca', 'cs', 'da', 'de', 'el', 'en', 'eo', 'es']
pieces {'K': 62, 'Q': 63, 'R': 61, 'B': 60, 'N': 61, 'P': 61}
rangs {14: 36, 13: 33, 12: 32, 11: 32}
couleurs {'C': 35, 'D': 34, 'H': 36, 'S': 35}
jeux {'morpion': 42, 'echecs': 69, 'dames': 60, 'go': 62, 'cartes': 59, 'whist': 27}
CORPUS items 449 bons 449 langues_avec_items 66 fortes 62 min/max 1.0 1.0
INVARIANCE 11 11
PERMUTATION {'items': 449, 'bons': 186, 'forts': 275, 'forts_bons': 12}
DETECTION 315 315
LANGUE {'items': 449, 'exacts': 342}
NOTATION {'items': 72, 'langues': 12, 'parses': 864, 'bons': 864}
DUREE 1.833
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 17, in <module>
TypeError: 'int' object is not iterable
[exit code: 1]
  ```

- **bash** `{"command": "grep -rn \"data/udhr\\|extrait_udhr\\|UDHR\" tools/ docs/pilotage/ reports/ --include=\"*.py\" --include=\"*.md\" --include=\"*.sh\" 2>/dev/null | grep -v \"archive\" | head -30", "description": "Cherche usages de l'UDHR"}`

  ```
tools/extrait_udhr.py:2:"""extrait_udhr.py — l'UDHR en unités alignées, prêtes à passer dans le moteur.
tools/extrait_udhr.py:4:L'UDHR est le premier corpus parce que l'alignement y est **par construction** :
tools/extrait_udhr.py:14:    extrait_udhr.py <dossier_udhr_xml> <sortie.jsonl> [--min-langues 50]
tools/extrait_wikipedia.py:9:apparié. L'invariance reste mesurée sur l'UDHR et les œuvres traduites.
tools/corpus_neuf.py:4:LE DOUTE, ET IL EST SÉRIEUX. L'UDHR est UN SEUL texte traduit en 392 langues. À la
tools/corpus_neuf.py:110:    print(f"#   rappel UDHR (texte ALIGNÉ) : C_quad 0,6536 · A40 0,5972 "
tools/position_seule.py:2:"""LA POSITION SEULE — de combien l'alignement de l'UDHR gonfle-t-il la fidélité ?
tools/position_seule.py:4:LE DOUTE À LEVER. L'UDHR est UN texte traduit en 392 langues : à la position t,
tools/position_seule.py:15:Sur l'UDHR il devrait être élevé (le contenu est le même partout). Sur Wikipedia, où
tools/profil_langues.py:157:        # l'UDHR aligne d'une langue à l'autre, et le périmètre du résultat de tête.
tools/wiki_apparie.py:4:POURQUOI. Le pont a été mesuré sur l'UDHR : **un seul texte** traduit en 392 langues.
tools/domaine_ou_langue.py:15:exactem
… [2167 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des fiches S (limites, banque, arbre) et du README structures

- **bash** `{"command": "cat reports/rapport-s-limites-v6.md; echo \"======\"; cat reports/rapport-s-banque-partielle.md", "description": "Lis fiches limites et banque partielle"}`

  ```
# S — Les trois limites de la v4 sont fermées : h050, h053 et « si fort que » ; 60/60 types, 142/142 rôles

> **Ligne de roadmap** : S · **Date** : 2026-11-03 · **Verdict** : les trois limites nommées du
> cycle précédent sont **fermées**. `h050` (« le triste **fait** demeure ») et `h053` (« le grand
> **lit** ») trouvaient un nom après un adjectif ; le « **si fort que** » était étiqueté
> hypothèse alors que la traduction anglaise en faisait une **conséquence**. Le gold passe de
> **55 à 60 phrases** (la vague 5, `h056–h060`, écrite après les règles et mesurée une fois) et la
> mesure donne **60/60 types**, **142/142 rôles**, **50/50 compléments**, couverture **1,00** ;
> les contrôles restent à **102/142**, **104/142** et **0,10**. Le corpus réel re-mesuré garde ses
> taux (65,5 % de GN+GV sur la littérature propre contre 9,1 % pour le mélange) et compte
> **596/1 184** homographes.

## Les trois fermetures

La première est un **nom après un adjectif devant un verbe** : « Le triste **fait** demeure. »
L'analyseur s'arrêtait au déterminant parce que « fait » est dans le lexique des verbes ; la règle
v6 regarde le mot **précédent** (l'adjectif « triste », ou le déterminant) et le m
… [10322 caractères tronqués]
  ```

- **bash** `{"command": "cat tools/structures/README.md; echo \"===\"; ls tools/structures/tests/; echo \"===\"; cd tools/structures && git status --porcelain 2>/dev/null | head; git log --oneline -5 2>/dev/null", "description": "Lis README et état git du sous-module"}`

  ```
# Structures — le banc d'interprétations candidates

> **Ce que c'est.** Un outil **pour humain** : il affiche, pour une phrase, plusieurs **structures
> d'interprétation candidates** (attachements, rôles, portées), permet de les **valider**, de
> demander l'avis d'un **grand modèle** (DeepSeek), et d'**exporter une banque** de structures
> validées — un corpus d'entraînement pour le projet Drave.

> **Ce que ce n'est pas.** Pas un analyseur syntaxique complet : les candidats sont **générés par
> une heuristique** (`generateur.py`) ou fournis par le fichier de données ; l'outil les fait
> valider, il ne prétend pas les avoir compris. Depuis la v2, l'heuristique **nomme le rôle** par
> le contexte, **coupe les subordonnées** et traite le passif et la copule — et un **gold** mesure
> ce qu'elle sait faire, échecs compris (voir « La mesure de l'analyseur »).

## Lancer

```bash
python3 serveur.py                 # http://127.0.0.1:8765
python3 serveur.py --port 9000 --hote 0.0.0.0   # sur le réseau local
```

Aucune dépendance : la bibliothèque standard suffit (serveur HTTP, JSON, `urllib`).

## Le niveau pragmatique

Une phrase hors contexte est **ambiguë** — même pour un humain. Et 
… [20632 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des outils LLM, de la clé API et de l'état git

- **bash** `{"command": "test -n \"${DEEPSEEK_API_KEY:-}\" && echo \"DEEPSEEK_API_KEY: présent (longueur ${#DEEPSEEK_API_KEY})\" || echo \"DEEPSEEK_API_KEY: absent\"; echo \"---\"; ls tools/llm/ 2>/dev/null; echo \"---\"; grep -rn \"deepseek\\|DEEPSEEK\\|chat/completions\" tools/llm/ tools/structures/llm.py 2>/ … [69 caractères tronqués]`

  ```
DEEPSEEK_API_KEY: absent
---
deepseek.py
distillation.py
enseignant.py
entrainer_masque.py
__init__.py
masque.py
mesure.py
prompts_publics_300.jsonl
prompts_publics.jsonl
prompts_publics.py
__pycache__
tests
---
tools/llm/deepseek.py:2:"""deepseek.py — le professeur externe, sans poids locaux.
tools/llm/deepseek.py:18:- `DEEPSEEK_API_KEY` (ou `DSH_API_KEY`) : la clé, lue dans l'environnement ;
tools/llm/deepseek.py:19:- `DEEPSEEK_BASE_URL` (ou `DSH_BASE_URL`) : `https://api.deepseek.com` par défaut ;
tools/llm/deepseek.py:20:- `DEEPSEEK_MODEL` (ou `DSH_MODEL`) : `deepseek-chat` par défaut ;
tools/llm/deepseek.py:21:- cache : `data/deepseek/cache/<sha256>.json` (gitignoré), clé = modèle + messages
tools/llm/deepseek.py:26:    python3 tools/llm/deepseek.py --prompt "Explique le ko au go." --json
tools/llm/deepseek.py:27:    DEEPSEEK_API_KEY=... python3 tools/llm/deepseek.py --prompt ... --json
tools/llm/deepseek.py:28:    python3 tools/llm/deepseek.py --prompt ... --dry-run --json
tools/llm/deepseek.py:44:CACHE_DEFAUT = RACINE / "data" / "deepseek" / "cache"
tools/llm/deepseek.py:45:BASE_DEFAUT = "https://api.deepseek.com"
tools/llm/deepseek.py:46:MODELE_DEFAUT = "deepseek-chat"
tool
… [830 caractères tronqués]
  ```

- **bash** `{"command": "cd tools/structures && git status -sb && echo \"---\" && git diff --stat && echo \"---\" && git diff -- donnees/paragraphes-validations.jsonl | head -30; echo \"===\"; cd ../.. && git submodule status 2>/dev/null | head; git status --short tools/structures 2>/dev/null | head", "descript … [41 caractères tronqués]`

  ```
## master...origin/master
 M donnees/paragraphes-validations.jsonl
---
 donnees/paragraphes-validations.jsonl | 11 +++++++++++
 1 file changed, 11 insertions(+)
---
diff --git a/donnees/paragraphes-validations.jsonl b/donnees/paragraphes-validations.jsonl
index 2ada51b..b34f8f5 100644
--- a/donnees/paragraphes-validations.jsonl
+++ b/donnees/paragraphes-validations.jsonl
@@ -6,3 +6,14 @@
 {"phrase_id": "a003", "candidat_id": "a003-c1", "statut": "exclu", "referents": {"Elle": "Alice", "sa": "Alice", "elle": "Alice", "se": "Alice"}, "note": "", "contexte": "Allons, à quoi bon pleurer ainsi, se dit Alice vivement.", "niveau": 2, "auteur": "humain", "horodatage": "2026-11-03T17:05:31"}
 {"phrase_id": "a003", "candidat_id": "a003-c2", "statut": "resolu", "referents": {"Elle": "Alice", "sa": "Alice", "elle": "Alice", "se": "Alice"}, "note": "", "contexte": "Allons, à quoi bon pleurer ainsi, se dit Alice vivement.", "niveau": 2, "auteur": "humain", "horodatage": "2026-11-03T17:05:40"}
 {"phrase_id": "a003", "candidat_id": "a003-c3", "statut": "exclu", "referents": {"Elle": "Alice", "sa": "Alice", "elle": "Alice", "se": "Alice"}, "note": "", "contexte": "Allons, à quoi bon pleurer ainsi, 
… [3911 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/llm/deepseek.py; echo \"===\"; sed -n '180,280p' tools/llm/deepseek.py", "description": "Lis l'API DeepSeek et son CLI"}`

  ```
#!/usr/bin/env python3
"""deepseek.py — le professeur externe, sans poids locaux.

POURQUOI CE MODULE. Le dépôt garde ses GPU et ses CPU pour le **modèle natif**
Drave (`entrainer_moteur.py`, `drave-core`) et pour les mesures **boîte blanche**
(perplexité, activations, flux, sondes). Le **langage** — traduire, juger,
générer, évaluer — passe par une API : on ne charge plus un Qwen de 7/14/32 B
pour cela. DeepSeek est ce **professeur externe** ; ses sorties peuvent servir à
entraîner/distiller l'élève natif (autorisation explicite du propriétaire de la
licence).

CE QUE LE MODULE NE FAIT PAS. Il ne remplace pas les mesures d'états internes :
une API ne donne pas les poids ni les activations. Il ne met **jamais** la clé
dans le dépôt, dans un cache ou dans un message d'erreur. Il ne dépend d'aucun
paquet externe : `urllib` suffit.

CONTRAT.
- `DEEPSEEK_API_KEY` (ou `DSH_API_KEY`) : la clé, lue dans l'environnement ;
- `DEEPSEEK_BASE_URL` (ou `DSH_BASE_URL`) : `https://api.deepseek.com` par défaut ;
- `DEEPSEEK_MODEL` (ou `DSH_MODEL`) : `deepseek-chat` par défaut ;
- cache : `data/deepseek/cache/<sha256>.json` (gitignoré), clé = modèle + messages
  + température + max_tokens, **jamais
… [6057 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"tradu\\|translate\\|retro\\|rétro\" tools/llm/ tools/*.py reports/rapport-s-*.md 2>/dev/null | head -30", "description": "Cherche une fonction de traduction existante"}`

  ```
tools/llm/deepseek.py:6:(perplexité, activations, flux, sondes). Le **langage** — traduire, juger,
tools/llm/tests/test_pipeline.py:28:        self.assertEqual(sum(1 for p in prompts if p["meta"]["categorie"] == "traduction"), 50)
tools/llm/tests/test_mesure.py:26:             "meta": {"categorie": "traduction", "cible_iso3": "fra",
tools/llm/tests/test_mesure.py:34:             "meta": {"categorie": "traduction"}},
tools/llm/tests/test_mesure.py:40:        self.assertEqual(r["traductions"], 1)
tools/llm/prompts_publics.py:6:   domaine public) : cinq articles en anglais, traduits vers dix langues, avec la
tools/llm/prompts_publics.py:7:   **traduction humaine officielle** comme référence pour le chrF ;
tools/llm/prompts_publics.py:68:                "system": "Tu es un traducteur professionnel. Réponds uniquement par la traduction, sans commentaire.",
tools/llm/prompts_publics.py:70:                           f"des droits de l'homme. Réponds uniquement par la traduction.\n\n{source}"),
tools/llm/prompts_publics.py:73:                         "categorie": "traduction"},
tools/llm/prompts_publics.jsonl:1:{"id": "udhr-01-fra", "system": "Tu es un traducteur professionnel. Réponds uniq
… [22618 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,70p' tools/llm/mesure.py; echo \"===\"; grep -n \"def main\\|argparse\\|__main__\\|chrF\\|chrf\" tools/llm/mesure.py | head -20; echo \"===\"; sed -n '1,45p' tools/llm/prompts_publics.py", "description": "Examine l'outil de mesure de traduction"}`

  ```
#!/usr/bin/env python3
"""mesure.py — ce que le banc DeepSeek coûte et ce qu'il rend.

Deux mesures, sans dépendance :
- **coût** : tokens d'entrée/sortie, latence, taux de cache ;
- **qualité des traductions** : chrF (n-grammes de caractères, β=2) contre la
  traduction humaine officielle de l'UDHR, avec le **plancher** source→référence
  (le même chrF sans traduction). On ne prétend pas mesurer « la compréhension » :
  on mesure une reproduction de traduction humaine sur cinq articles publics.

Les entrées `dry_run` sont ignorées : elles ne sont pas des sorties du professeur.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
from collections import Counter, defaultdict


def chrf(hyp: str, ref: str, n_max: int = 6, beta: float = 2.0) -> float:
    from collections import Counter
    hyp = " ".join(hyp.split())
    ref = " ".join(ref.split())
    if not hyp or not ref:
        return 0.0
    prec, rec = [], []
    for n in range(1, n_max + 1):
        H = [hyp[i:i + n] for i in range(max(0, len(hyp) - n + 1))]
        R = [ref[i:i + n] for i in range(max(0, len(ref) - n + 1))]
        ch, cr = Counter(H), Counter(R)
        inter = sum((ch & cr).val
… [4976 caractères tronqués]
  ```

- **bash** `{"command": "cd tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests 2>&1 | tail -15", "description": "Lance les 56 tests du banc S", "timeoutMs": 180000}`

  ```
.  127.0.0.1 · "GET /api/paragraphes HTTP/1.1" 200 -
  127.0.0.1 · "POST /api/valider-paragraphe HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/paragraphes HTTP/1.1" 200 -
.  127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
.  127.0.0.1 · "GET / HTTP/1.1" 200 -
.  127.0.0.1 · "POST /api/valider HTTP/1.1" 400 -
.  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "POST /api/valider HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/phrases HTTP/1.1" 200 -
  127.0.0.1 · "GET /api/export HTTP/1.1" 200 -
.
----------------------------------------------------------------------
Ran 56 tests in 4.343s

OK
  ```

### 🤖 Assistant

⏵ Contrôle d'intégrité après les tests (aucune écriture attendue)

- **bash** `{"command": "cd tools/structures && wc -l donnees/paragraphes-validations.jsonl && git status --porcelain && git diff --stat", "description": "Vérifie si les tests ont écrit dans les données"}`

  ```
19 donnees/paragraphes-validations.jsonl
 M donnees/paragraphes-validations.jsonl
 donnees/paragraphes-validations.jsonl | 11 +++++++++++
 1 file changed, 11 insertions(+)
  ```

- **bash** `{"command": "grep -n \"TemporaryDirectory\\|tempfile\\|dossier\\|donnees\\|paragraphes-validations\" tools/structures/tests/test_serveur.py | head -30", "description": "Vérifie le répertoire des tests serveur"}`

  ```
5:import tempfile
18:        self.dossier = pathlib.Path(tempfile.mkdtemp())
19:        shutil.copy(RACINE / "donnees" / "phrases.json", self.dossier / "phrases.json")
20:        if (RACINE / "donnees" / "paragraphes.json").exists():
21:            shutil.copy(RACINE / "donnees" / "paragraphes.json", self.dossier / "paragraphes.json")
23:        self.serveur.donnees = serveur.Donnees(self.dossier)
32:        shutil.rmtree(self.dossier, ignore_errors=True)
112:            self.assertTrue((b.dossier / "paragraphes-validations.jsonl").exists())
154:            self.assertTrue((b.dossier / "llm.jsonl").exists())
  ```

### 🤖 Assistant

⏵ Relecture des 9 paragraphes et de leurs référents enregistrés

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('tools/structures/donnees/paragraphes.json'))\nrows=[json.loads(l) for l in open('tools/structures/donnees/paragraphes-validations.jsonl',encoding='utf-8') if l.strip()]\nfor p in d['paragraphes']:\n    print('='*80)\n    print(p['id'],'| … [374 caractères tronqués]`

  ```
================================================================================
a001 | antécédent: Alice
CIBLE: Elle avait pour habitude de se donner de très-bons conseils (bien qu'elle les suivît rarement), et quelquefois elle se grondait si fort que les larmes lui en venaient aux yeux.
CTX  : Allons, à quoi bon pleurer ainsi, se dit Alice vivement.
EN   : She generally gave herself very good advice, (though she very seldom followed it), and sometimes she scolded herself so severely as to bring tears into her eyes; and once she remembered trying to box her own ears for having cheated herself in a game of croquet she was playing against herself, for this curious child was very fond of pretending to be two people.
   a001-c1 resolu | refs: {'Elle': 'Alice', 'se': 'Alice', 'elle': 'Alice', 'lui': 'Alice', 'en': 'Alice'}
   a001-c2 resolu | refs: {'Elle': 'Alice', 'se': 'Alice', 'elle': 'Alice', 'lui': 'Alice', 'en': 'Alice'}
================================================================================
a002 | antécédent: Alice
CIBLE: Elle aperçut alors une petite boîte en verre qui était sous la table, l'ouvrit et y trouva un tout petit gâteau sur lequel les mots "MANGEZ-MOI" étai
… [5347 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de l'export de la banque et des 8 derniers verdicts

- **bash** `{"command": "ls -la data/structures/ 2>/dev/null; echo \"---\"; wc -l data/structures/banque-validee.jsonl 2>/dev/null; sha256sum data/structures/banque-validee.jsonl 2>/dev/null; echo \"---\"; cat reports/s-banque-validee.json 2>/dev/null | head -30; echo \"---\"; cat tools/structures/donnees/llm.j … [73 caractères tronqués]`

  ```
total 136
drwxr-xr-x. 1 stephane stephane   264  2 nov 16:27 .
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane 27387  2 nov 20:36 banque.jsonl
-rw-r--r--. 1 stephane stephane   395  2 nov 20:36 banque-manifest.json
-rw-r--r--. 1 stephane stephane  4857  2 nov 16:27 banque-reference.jsonl
-rw-r--r--. 1 stephane stephane   388  2 nov 16:27 banque-reference-manifest.json
-rw-r--r--. 1 stephane stephane 89016  4 nov 08:42 banque-validee.jsonl
-rw-r--r--. 1 stephane stephane   411  4 nov 08:42 banque-validee-manifest.json
---
84 data/structures/banque-validee.jsonl
3ca1ac2002e225f69d689a929ab6bb9c6c8b6a06c6b3895af71e1406830c79f2  data/structures/banque-validee.jsonl
---
{
 "version": 2,
 "mode": "banque",
 "date": "2026-11-04T08:42:21",
 "source": "tools/structures/donnees",
 "sortie": "data/structures/banque-validee.jsonl",
 "phrases": 67,
 "candidats_acceptes": 84,
 "sha256": "3ca1ac2002e225f69d689a929ab6bb9c6c8b6a06c6b3895af71e1406830c79f2",
 "note": "verdicts du banc (`resolu`, `compatible`, `double_sens`) ; le dernier verdict d'un candidat gagne ; spans vérifiés."
}
---
{"phrase_id": "c001", "fournisseur": "baseline", "modele": "attachement-le-
… [581 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nrows=[json.loads(l) for l in open('tools/structures/donnees/validations.jsonl',encoding='utf-8') if l.strip()]\nfor r in rows:\n    if r['horodatage'] >= '2026-11-03T16:30':\n        print(r['horodatage'],r['phrase_id'],r['candidat_id'],r['st … [204 caractères tronqués]`

  ```
2026-11-03T16:39:24 p003 p003-c2 resolu 0 
2026-11-03T16:40:00 p003 p003-c2 exclu 0 
2026-11-03T16:40:38 c010 c010-c1 resolu 0 
2026-11-03T16:43:06 c066 c066-c1 exclu 0 
2026-11-03T16:44:55 c066 c066-c2 resolu 0 
2026-11-03T16:45:08 c066 c066-c3 compatible 0 
2026-11-03T16:46:37 c067 c067-c1 exclu 0 
2026-11-03T16:46:42 c067 c067-c2 exclu 0 
--- 8 derniers ids phrases ['p003', 'p003', 'c010', 'c066', 'c066', 'c066', 'c067', 'c067']
total 150
  ```

### 🤖 Assistant

⏵ Lecture ciblée des fiches analyseur et arbre/référents

- **bash** `{"command": "sed -n '1,35p' reports/rapport-s-analyseur.md; echo \"======\"; sed -n '1,40p' reports/rapport-s-arbre-referents.md; echo \"======\"; sed -n '1,25p' reports/rapport-s-fait-divers.md", "description": "Lis les verdicts des fiches analyseur/arbre/fait divers"}`

  ```
# S — L'analyseur contre les structures écrites à la main : 7/7 séquences, 93,9 % de couverture

> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur les **7 phrases** du banc,
> l'analyseur heuristique retrouve la **séquence de types 7/7** et couvre **93,9 %** des octets des
> structures écrites à la main (94–97 % par phrase, sauf une à 42 % avant correction). Le reste
> est l'**espace de tête** des segments (convention du banc) et trois cas corrigés en chemin.

## Le dispositif

- Structures de référence : les **7 phrases** du banc (`donnees/phrases.json`), une structure
  écrite à la main chacune (la première lecture).
- Analyseur : [`tools/structures/generateur.py`](../tools/structures/generateur.py) — lexique de
  mots grammaticaux, frontières de proposition, rôles par préposition.
- Mesure : la **séquence de types** (GN, GV, GP, REL, SUB) et la **couverture** des octets de la
  référence par les segments générés **du même type**.

## Ce qui est mesuré

| phrase | types | couverture | segments (réf / gén) |
|---|---|---:|---|
| p001 — « Le chat de la voisine qui dort… » | **OK** | 94 % | 4 / 4 |
| p002 — « J'ai vu l'homme avec le télescope. » | **OK** | 94 % 
… [5255 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nfrom tools.jeux.lexique_multilingue import MULTI\nfrom tools.jeux.corpus_multilingue import construire_corpus_multilingue\ncov=MULTI.couverture()\npar=cov['par_langue']\ncor=construire_corpus_multilingue()\nitems=collections.Counter(); forts= … [739 caractères tronqués]`

  ```
langues couverture 71 fortes 32
fortes list ['ar', 'bn', 'ca', 'cs', 'da', 'de', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'hu', 'it', 'ja', 'lv', 'nb', 'nl', 'pl', 'pt', 'ru', 'sl', 'sq', 'sr', 'sv', 'uk', 'vi', 'zh', 'af']
sans item ['mt', 'ky', 'lo', 'si', 'yo']
avec item 66 avec fort 62
top par items [('de', 11), ('en', 11), ('es', 11), ('fr', 11), ('it', 11), ('ja', 11), ('nl', 11), ('pl', 11), ('pt', 11), ('ru', 11)]
bas [('am', 1), ('km', 1), ('pa', 1), ('so', 1), ('zu', 1), ('kk', 2), ('ne', 2), ('sw', 3), ('ga', 3), ('hi', 4)]
ar	28	8	4
bn	20	8	7
ca	31	8	5
cs	31	10	7
da	27	10	7
de	34	11	7
el	22	6	4
en	35	11	7
eo	32	10	7
es	33	11	7
et	25	10	7
eu	22	8	5
fa	26	10	7
fi	32	10	7
fr	35	11	7
gl	16	5	2
he	24	5	2
hi	16	4	2
hr	15	5	2
hu	26	10	7
id	19	5	2
is	14	4	2
it	28	11	7
ja	31	11	7
ka	14	4	2
kk	9	2	0
ko	27	6	2
lt	15	5	2
lv	21	7	4
mk	19	4	2
ms	16	5	2
mt	4	0	0
nb	28	10	7
nl	32	11	7
nn	16	4	2
pl	30	11	7
pt	31	11	7
ro	19	5	2
ru	34	11	7
sk	23	6	3
sl	30	10	7
sq	21	9	7
sr	25	10	7
sv	31	10	7
sw	11	3	2
ta	17	4	2
th	18	6	3
tr	27	7	3
uk	32	10	7
ur	14	4	2
vi	26	10	7
zh	32	11	7
af	20	8	7
am	4	1	0
az	15	4	2
be	23	8	5
bs	18	4	2
cy	14	4	2
ga	12	3	2
hy	16	5	2
km	3	1	1
ky	2	0	0
lo	1	0	
… [76 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche exhaustive de la rétro-traduction et des mesures associées

- **bash** `{"command": "grep -rniE \"r[ée]tro[- ]?traduction|retro[- ]?traduction|back[- ]?translation|round[- ]?trip\" --include=\"*.py\" --include=\"*.md\" --include=\"*.json\" --include=\"*.sh\" --include=\"*.js\" --include=\"*.html\" . 2>/dev/null | grep -v \"/archive/\" | grep -v \"journal/sessions\" | he … [75 caractères tronqués]`

  ```
./reports/campagne-benefices/027-24-memoire-episodique-c6-ce-qui-marche-et-c.md:15:- **round-trip 300/300** — relire avec sa propre clé rend l'état écrit, au bit près,
./reports/campagne-benefices/027-24-memoire-episodique-c6-ce-qui-marche-et-c.md:36:- **à petit k, l'invariant de round-trip CASSE.** k = 8 : **81 des 300 états
./reports/campagne-benefices/027-24-memoire-episodique-c6-ce-qui-marche-et-c.md:37:  partagent la clé d'un autre** (pire multiplicité 7) et le round-trip tombe à
./reports/campagne-benefices/027-24-memoire-episodique-c6-ce-qui-marche-et-c.md:97:- round-trip : **300/300 au bit près**, y compris à travers le disque. Le magasin
./reports/campagne-benefices/027-24-memoire-episodique-c6-ce-qui-marche-et-c.md:118:| round-trip | 300/300 | **240/240 au bit près** |
./reports/campagne-benefices/027-24-memoire-episodique-c6-ce-qui-marche-et-c.md:154:Sur ce même magasin de **2 048 épisodes** : round-trip **2 048/2 048 au bit près**,
./reports/rapport-consolidation-c7.md:82:  deux mécanismes sont mesurés séparément (C6 : rappel 96,3 %, round-trip exact), pas côte à côte
./reports/07/p4.md:427:- **la source fra→eng est elle-même une traduction officielle** ✓✗ : la paire fr
… [3878 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -iE \"traduc|tradu|langue|udhr|retro\" ; echo \"---\"; find reports -maxdepth 2 -iname \"*tradu*\" -o -iname \"*retro*\" -o -iname \"*udhr*\" | head -20; echo \"---\"; ls data/udhr/", "description": "Cherche fiches/JSON de traduction et UDHR"}`

  ```
carte-24langues-3b.json
carte-24langues.json
contamination-udhr-A.json
contamination-udhr-B.json
jeux-langues-mesures.json
pensee-par-langue.json
rapport-c8-inter-langue.md
rapport-langues-maitres.md
rapport-pensee-par-langue.md
rapport-s-traductions.md
restitution-udhr-flux.json
restitution-udhr.json
toutes-langues
toutes-langues.md
traduction-24langues-3b-A.json
traduction-24langues-3b-B.json
traduction-24langues-A.json
traduction-24langues-B.json
traduction-eurlex-0.5b.json
traduction-eurlex-14b.json
traduction-eurlex-1.5b.json
traduction-eurlex2509-3b.json
traduction-eurlex2509-7b.json
traduction-eurlex-3b-fraeng.json
traduction-eurlex-3b.json
traduction-eurlex-7b-fraeng.json
traduction-eurlex-7b.json
traduction-jw-A.json
traduction-jw-B.json
traduction-langues-3b.json
traduction-langues-7b.json
traduction-legal-0.5b-6.json
traduction-legal-1.5b.json
traduction-legal-3b.json
traduction-legal-7b.json
traduction-legal.json
traduction-litteraire-3b.json
traduction-litteraire-7b.json
traduction-onu-3b.json
traduction-onu6-3b.json
traduction-onu6-7b.json
traduction-onu-7b.json
traduction-pidgin-14b.json
traduction-pidgin-7b.json
traduction-presse-3b.json
traduction-presse-7b.json
tr
… [1156 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification d'un éventuel corpus UDHR à 71 langues dans reports

- **bash** `{"command": "sed -n '1,60p' reports/toutes-langues.md; echo \"===\"; ls reports/toutes-langues | head; echo \"===\"; wc -l reports/toutes-langues.md; grep -n \"71\\|456\\|392\" reports/toutes-langues.md | head -20", "description": "Inspecte le rapport toutes-langues"}`

  ```
# Extension à toutes les langues, puis aux grands corpus

Objectif : passer de **46 langues** à **toutes celles disponibles**, puis aux grands
corpus multilingues pour obtenir des professeurs plus riches.

Professeur unique : **Qwen2.5-0.5B, couche 10**. Boîte noire : on ne lit de lui que
la couche à émuler. Aucune rétropropagation : `A` et `B` aléatoires et gelés, seule
la lecture s'ajuste en forme fermée.

---

## Index des expériences

| # | expérience | date réelle (git) | fichier |
|---|---|---|---|
| 001 · 01 | 1. Le périmètre, inventorié | 2026-10-05 23:50 HAE (`1424c5d`) | [001-01-le-perimetre-inventorie.md](toutes-langues/001-01-le-perimetre-inventorie.md) |
| 002 · 02 | 2. La convention de traçage, unique et vérifiée | 2026-10-05 23:50 HAE (`1424c5d`) | [002-02-la-convention-de-tracage-unique-et-verif.md](toutes-langues/002-02-la-convention-de-tracage-unique-et-verif.md) |
| 003 · 03 | 3. Le découpage : stratifié par écriture, déduit du texte | 2026-10-05 23:50 HAE (`1424c5d`) | [003-03-le-decoupage-stratifie-par-ecriture-dedu.md](toutes-langues/003-03-le-decoupage-stratifie-par-ecriture-dedu.md) |
| 004 · 04 | 4. Les cinq phases, chaînées | 2026-10-05 23:50 HAE (`1424c5d
… [11668 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor p in ['reports/traduction-udhr-propre-7b-fraeng.json','reports/traduction-24langues-3b-A.json','reports/carte-24langues.json']:\n    try:\n        d=json.load(open(p))\n        print('='*10,p,type(d).__name__)\n        if isinstance(d,dict): print('cl … [194 caractères tronqués]`

  ```
========== reports/traduction-udhr-propre-7b-fraeng.json list
n 1 ex {'paire': 'fra:eng', 'n': 30, 'chrf': 80.00454879409124, 'ic95': [76.3, 83.6], 'plancher_source': 31.577068379460247, 'hasard': 27.139249347650605, 'tronque': 0, 'recopie': 24, 'ratio_longueur': 1.04,
========== reports/traduction-24langues-3b-A.json list
n 12 ex {'paire': 'eng:bul', 'n': 40, 'chrf': 46.53022980281709, 'ic95': [44.2, 48.8], 'plancher_source': 4.1348331752632745, 'hasard': 24.43019806240859, 'tronque': 3, 'recopie': 5, 'ratio_longueur': 0.94, '
========== reports/carte-24langues.json dict
cles ['langues', 'moyenne_annoncees', 'moyenne_non_annoncees', 'correlation_chrf_plancher']
  ```

### 🤖 Assistant

⏵ Inspection du format des JSON « pensée » existants

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor p in ['reports/pensee-file-taches.json','reports/pensee-fiabilite-produit.json','reports/pensee-par-langue.json']:\n    try:\n        d=json.load(open(p))\n        print('='*20,p,type(d).__name__)\n        if isinstance(d,dict):\n            print('cl … [366 caractères tronqués]`

  ```
==================== reports/pensee-file-taches.json dict
cles ['date', 'heure', 'branche', 'head', 'mission', 'methode', 'comptes', 'taches', 'doublons', 'perimes', 'dependances_cachees', 'ordre', 'commandes_verifiees', 'limites', 'fichiers']
  date str 10
  heure str 9
  branche str 4
  head str 8
==================== reports/pensee-fiabilite-produit.json dict
cles ['rapport', 'ligne', 'branche', 'commit_mesure', 'commit_module', 'date', 'objet', 'verdict', 'snapshot', 'dispositif', 'banc_50', 'robustesse', 'contrat', 'schema_propose', 'test_non_regression', 'correctifs', 'controle_negatif', 'limites', 'fichiers']
  rapport str 17
  ligne str 3
  branche str 4
  commit_mesure str 8
==================== reports/pensee-par-langue.json dict
cles ['date', 'ligne', 'portes', 'fr', 'en', 'tout', 'limites']
  date str 10
  ligne str 3
  portes str 7
  fr dict 5
  ```

- **bash** `{"command": "sed -n '1,80p' tools/structures/mesure_arbre.py; echo \"===\"; grep -n \"argparse\\|__main__\\|json\" tools/structures/mesure_arbre.py | tail -15", "description": "Lis mesure_arbre et son CLI"}`

  ```
#!/usr/bin/env python3
"""mesure_arbre.py — la profondeur actuelle de l'arbre et les référents non résolus de la banque.

Le retour humain du 03/11 : « il manque trop souvent de profondeur » et « les référents ne
semblent pas résolus avant que je tranche ». Ce script mesure les deux sur les 207 phrases du
banc : la distribution de `niveau` (l'indentation) et des profondeurs maximales des candidats, et
les pronoms/possessifs qui n'ont aucun antécédent proposé. C'est le dispositif du négatif, pas un
jugement : il dit ce que l'outil ne montrait pas.

    python3 mesure_arbre.py
"""
from __future__ import annotations

import json
import pathlib
from collections import Counter

import generateur

RACINE = pathlib.Path(__file__).resolve().parent
DONNEES = RACINE / "donnees"
SORTIE = DONNEES / "mesure-arbre.json"
POSSESSIFS = set("mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs".split())


def phrases() -> list[dict]:
    sortie = json.loads((DONNEES / "phrases.json").read_text(encoding="utf-8"))["phrases"]
    g = DONNEES / "phrases_generees.json"
    if g.exists():
        sortie += json.loads(g.read_text(encoding="utf-8"))["phrases"]
    return sortie


def mesurer() ->
… [2205 caractères tronqués]
  ```

- **bash** `{"command": "cd tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 -c 'import json, mesure_arbre; r=mesure_arbre.mesurer(); print(json.dumps({k:r[k] for k in [\"phrases\",\"candidats\",\"segments\",\"profondeur_max\",\"niveaux\",\"phrases_avec_referent\",\"referents\",\"avec_candidat\",\"sans_can … [139 caractères tronqués]`

  ```
{
 "phrases": 207,
 "candidats": 359,
 "segments": 2308,
 "profondeur_max": {
  "0": 2,
  "1": 37,
  "2": 221,
  "3": 84,
  "4": 13,
  "5": 2
 },
 "niveaux": {
  "0": 359,
  "1": 1268,
  "2": 556,
  "3": 108,
  "4": 15,
  "5": 2
 },
 "phrases_avec_referent": 170,
 "referents": 371,
 "avec_candidat": 294,
 "sans_candidat": 77,
 "formes": {
  "y": 109,
  "en": 67,
  "se": 44,
  "me": 19,
  "il": 18,
  "son": 18,
  "elle": 9,
  "je": 9,
  "vous": 9,
  "lui": 8,
  "sa": 8,
  "on": 5,
  "nous": 5,
  "tu": 5,
  "ses": 4,
  "leurs": 4,
  "te": 4,
  "vos": 4,
  "ils": 3,
  "moi": 3,
  "nos": 3,
  "cela": 2,
  "votre": 2,
  "mon": 2,
  "notre": 2,
  "leur": 2,
  "j'ai": 1,
  "j'avais": 1,
  "j'aurais": 1
 }
}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-file-taches.json'))\nfor k in ['comptes','limites','fichiers','commandes_verifiees']:\n    print('==',k); print(json.dumps(d.get(k),ensure_ascii=False,indent=1)[:1200])\nprint('== tache ex'); print(json.dumps(d['taches'][0 … [117 caractères tronqués]`

  ```
== comptes
{
 "taches": 29,
 "A": 8,
 "B": 11,
 "C": 10,
 "doublons": 6,
 "perimes": 18,
 "dependances_cachees": 12,
 "vagues": 3,
 "sous_agents_max_par_vague": 4
}
== limites
[
 "Instantané 10 h 20, HEAD 7679a2d4 ; l'arbre bouge.",
 "Pas de passe complète (2 h 11 à 2 h 29) ; 4 rouges du registre du 06/11, seuls bloc-linguistique et sessions rejouées.",
 "S lu, pas rejoué : 19 + 150 verdicts ; couverture par phrase à vérifier.",
 "gold 200+ non défini : classé en coordination, pas inventé.",
 "L'audit de fiabilité produit est en cours (14114f3d), sa fiche est absente.",
 "Cette fiche change les compteurs : 679/772 ; trois fiches de vague : 682/775.",
 "Aucun existant modifié ; INDEX restauré après un --help destructif."
]
== fichiers
[
 "reports/rapport-file-taches.md",
 "reports/pensee-file-taches.json"
]
== commandes_verifiees
[
 {
  "commande": "bash tools/toutes-les-portes.sh",
  "existe": "oui",
  "executee": "non (2 h 11 à 2 h 29)",
  "etat": "84 portes ; la passe du 06/11 a 79 vertes et 4 rouges"
 },
 {
  "commande": "bash tools/porte-bloc-linguistique.sh",
  "existe": "oui",
  "executee": "oui",
  "etat": "exit 1 ; cascade_pos 0,7465 < 0,7581"
 },
 {
  "commande": "bash too
… [1487 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification si la page banque sert les anciens candidats ou la v7

- **bash** `{"command": "python3 - <<'EOF'\nimport json\ng=json.load(open('tools/structures/donnees/phrases_generees.json'))\np=g['phrases'][0]\nc=p['candidats'][0]\nprint('phrase',p['id'],'stored candidats',len(p['candidats']))\nprint('cles candidat',sorted(c.keys()))\nprint('cles segment',sorted(c['segments'] … [595 caractères tronqués]`

  ```
phrase c001 stored candidats 1
cles candidat ['attachement', 'id', 'lecture', 'nom', 'segments']
cles segment ['debut', 'fin', 'niveau', 'role', 'texte', 'type']
ex segment {"debut": 0, "fin": 47, "texte": "Au lecteur Cette version électronique reproduit", "type": "GP", "role": "destinataire", "niveau": 1}
===
dyn candidats 1
cles candidat ['attachement', 'lecture', 'nom', 'segments']
cles segment ['debut', 'fin', 'niveau', 'parent', 'profondeur', 'role', 'texte', 'type']
ex segment {"debut": 0, "fin": 47, "texte": "Au lecteur Cette version électronique reproduit", "type": "GP", "role": "destinataire", "niveau": 0, "parent": null, "profondeur": 0}
  ```

- **bash** `{"command": "stat -c '%y %n' tools/structures/donnees/phrases_generees.json tools/structures/donnees/mesure-arbre.json tools/structures/generateur.py 2>/dev/null; echo \"===\"; grep -n \"candidats\\|analyser\\|phrases_generees\" tools/structures/serveur.py | head -20", "description": "Dates des donn … [27 caractères tronqués]`

  ```
2026-11-02 20:35:33.102281270 -0500 tools/structures/donnees/phrases_generees.json
2026-11-03 16:23:01.747926807 -0500 tools/structures/donnees/mesure-arbre.json
2026-11-04 11:41:49.129836555 -0500 tools/structures/generateur.py
===
46:        self.fichier_generees = self.dossier / "phrases_generees.json"
54:        """Les paragraphes complets : cible, contexte, antécédent, candidats, référents, arbre SVG."""
61:            cands = generateur.analyser(p["cible"])
70:                "candidats": cands, "referents": refs,
84:        if not any(c["id"] == candidat_id for c in p["candidats"]):
117:        if not any(c["id"] == candidat_id for c in phrase["candidats"]):
148:        r = llm.evaluer(phrase["texte"], phrase["candidats"], fournisseur, contexte, niveau)
156:        """Génère les candidats d'une phrase libre et la persiste dans phrases_generees.json."""
160:        candidats = generateur.analyser(texte)
161:        if not candidats:
168:                      "candidats": [{"id": f"{pid}-c{i + 1}", **c}
169:                                    for i, c in enumerate(candidats)]}
188:        par_id = {(p["id"], c["id"]): (p, c) for p in self.phrases for c in p["candidats"]}
  ```

### 🤖 Assistant

⏵ Mesure de l'écart entre les candidats stockés (page /) et la v7

- **bash** `{"command": "cd tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'EOF'\nimport json, hashlib, collections\nimport generateur\nfixe=json.load(open('donnees/phrases.json'))['phrases']\ngen=json.load(open('donnees/phrases_generees.json'))['phrases']\nstored={p['id']:p for p in fixe+gen}\ndiff_ … [2035 caractères tronqués]`

  ```
phrases 207 candidats stockés 369 dynamiques 359
candidats stockés sans profondeur 369 / 369
phrases avec compte différent 9 [('p006', 2, 1), ('c023', 3, 2), ('c056', 3, 1), ('c064', 2, 1), ('c084', 2, 1), ('c176', 2, 1), ('c185', 2, 1), ('c194', 3, 2), ('c198', 3, 2)]
appariés identiques 304 changés 55 orphelins 10
verdicts dont l index n existe plus en dynamique 5
profondeur max stockée {0: 10, 1: 277, 2: 82}
profondeur max dynamique {0: 2, 1: 37, 2: 221, 3: 84, 4: 13, 5: 2}
  ```

### 🤖 Assistant

⏵ Collecte des identifiants de version et de la date

- **bash** `{"command": "date '+%Y-%m-%d %H:%M %Z'; echo \"---\"; git rev-parse --short HEAD; git log -1 --format='%h %ad %s' --date=short; echo \"---\"; cd tools/structures && git rev-parse --short HEAD && git log -1 --format='%h %ad %s' --date=short && git status --porcelain", "description": "Date et HEAD des … [9 caractères tronqués]`

  ```
2026-11-06 21:49 EST
---
de7c9113
de7c9113 2026-11-06 B13 — LES NOMBRES ONT UNE POS (NUM, 45 TOKENS) ; GOLD INCHANGÉ (85,00 / 0,6482 / 235-236) ; 183/183
---
523d8c1
523d8c1 2026-11-04 S — LE FAIT DIVERS EST TRANCHÉ : 61/61 TYPES, 144/144 RÔLES ; LA TÊTE DU GN ARRÊTE LE VERBE
 M donnees/paragraphes-validations.jsonl
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\n# accepted phrases / exports reconciliation\nrows=[json.loads(l) for l in open('tools/structures/donnees/validations.jsonl',encoding='utf-8') if l.strip()]\nlast={}\nfor r in rows: last[(r['phrase_id'],r['candidat_id'])]=r\nacc=[(k,v) for k,v … [965 caractères tronqués]`

  ```
acceptés 84 phrases 67
exclus 63
paires 147
phrases 207 candidats stockés 369
phrases jugées entièrement 74
phrases avec >=1 verdict 74
p 14 Counter({'resolu': 7, 'compatible': 4, 'exclu': 3})
c 133 Counter({'resolu': 66, 'exclu': 60, 'compatible': 7})
  ```

### 🤖 Assistant

⏵ Vérification des noms de fichiers et des compteurs UDHR

- **bash** `{"command": "ls -la reports/rapport-etat-s.md reports/pensee-etat-s.json 2>&1; echo \"---\"; python3 - <<'EOF'\nimport json\nlangs=[json.loads(l) for l in open('data/udhr/langues.jsonl',encoding='utf-8') if l.strip()]\narts=[json.loads(l) for l in open('data/udhr/articles.jsonl',encoding='utf-8') if … [458 caractères tronqués]`

  ```
ls: cannot access 'reports/rapport-etat-s.md': No such file or directory
ls: cannot access 'reports/pensee-etat-s.json': No such file or directory
---
UDHR langues 456 articles 13996 propres 13222
scripts 42 sens 2
langues uniques iso3 400 fichiers 456
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nd=json.load(open('tools/jeux/lexique_multilingue.json'))\nlangs=d['langues']\nnoms={'ar':'arabe','bn':'bengali','ca':'catalan','cs':'tchèque','da':'danois','de':'allemand','el':'grec','en':'anglais','eo':'espéranto','es':'espagnol','et':'esto … [1184 caractères tronqués]`

  ```
noms 71 langues 71 manquants [] en trop []
ar arabe | bn bengali | ca catalan | cs tchèque | da danois | de allemand | el grec | en anglais | eo espéranto | es espagnol | et estonien | eu basque | fa persan | fi finnois | fr français | gl galicien | he hébreu | hi hindi | hr croate | hu hongrois | id indonésien | is islandais | it italien | ja japonais | ka géorgien | kk kazakh | ko coréen | lt lituanien | lv letton | mk macédonien | ms malais | mt maltais | nb norvégien (bokmål) | nl néerlandais | nn norvégien (nynorsk) | pl polonais | pt portugais | ro roumain | ru russe | sk slovaque | sl slovène | sq albanais | sr serbe | sv suédois | sw swahili | ta tamoul | th thaï | tr turc | uk ukrainien | ur ourdou | vi vietnamien | zh chinois | af afrikaans | am amharique | az azéri | be biélorusse | bs bosnien | cy gallois | ga irlandais | hy arménien | km khmer | ky kirghize | lo lao | mn mongol | ne népalais | pa pendjabi | si cingalais | so somali | uz ouzbek | yo yoruba | zu zoulou
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nrows=[json.loads(l) for l in open('tools/structures/donnees/validations.jsonl',encoding='utf-8') if l.strip()]\nlast={}\nfor r in rows: last[(r['phrase_id'],r['candidat_id'])]=r\nctx=[(k,v) for k,v in last.items() if v.get('contexte')]\nprint('avec contex … [334 caractères tronqués]`

  ```
avec contexte final 6
('p001', 'p001-c1') resolu 2 La voisine est partie en vacances. Son chat, lui, est resté 
('p001', 'p001-c2') exclu 2 La voisine est partie en vacances. Son chat, lui, est resté 
('p002', 'p002-c1') resolu 2 Le détective surveille la maison d'en face. Il a vu l'homme 
('p002', 'p002-c2') compatible 2 Le détective surveille la maison d'en face. Il a vu l'homme 
('p007', 'p007-c1') resolu 3 Dans ce dessin animé, le canard parle et réclame son dîner :
('p007', 'p007-c2') compatible 3 Dans ce dessin animé, le canard parle et réclame son dîner :
niveaux final {0: 141, 1: 0, 2: 4, 3: 2, 4: 0}
contexte non vide lignes 7
  ```

### 🤖 Assistant

⏵ Vérification des commandes de traduction existantes (aller simple)

- **bash** `{"command": "sed -n '100,140p' tools/llm/mesure.py; echo \"===\"; sed -n '1,45p' tools/llm/enseignant.py; echo \"===\"; grep -n \"argparse\\|__main__\\|--\" tools/llm/enseignant.py | head -20", "description": "Lis CLI mesure et enseignant"}`

  ```
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--entree", default="data/deepseek/enseignant.jsonl")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    r = mesure(a.entree)
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n",
                                        encoding="utf-8")
    print(json.dumps(r, ensure_ascii=False, indent=1))
    raise SystemExit(0 if not r.get("vide") else 1)
===
#!/usr/bin/env python3
"""enseignant.py — construire le corpus du professeur DeepSeek.

Le corpus est un **JSONL** : chaque ligne porte le prompt, la réponse du professeur,
l'usage (tokens), la latence et le cache. Il ne contient **aucune clé**. Les
réponses peuvent ensuite servir à entraîner/distiller l'élève natif `route`
(autorisation explicite de la licence DeepSeek).

Le script est **reprenable** : une ligne déjà présente n'est pas redemandée. Le
mode `--dry-run` ne fait aucune requête : il écrit des réponses factices, que
`distillation.py` ignore — un dry-run ne doit jamais devenir un corpus
d'entraînement.

Usage :
    python3 tools/llm/enseignant.py --prompts
… [1998 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"prompts_publics\\|mesure.py\\|enseignant.py\" tools/*.sh tools/*.py docs/ --include=\"*.sh\" --include=\"*.py\" --include=\"*.md\" 2>/dev/null | grep -v archive | head -20", "description": "Cherche l'usage du banc de traduction"}`

  ```
tools/porte-deepseek.sh:34:python3 - "$PWD/tools/llm/prompts_publics.jsonl" "$PWD/tools/llm/prompts_publics_300.jsonl" <<'PY' || exit 1
tools/porte-deepseek.sh:47:python3 tools/llm/enseignant.py --sortie "$T/enseignant-dry.jsonl" --limite 2 --dry-run >/dev/null || exit 1
tools/mesure_jeux.py:7:Le module est `tools/jeux/mesure.py` ; ce pilote ne fait que rendre l'appel
docs/methode/ressources.md:94:(annotation, distillation, corpus) passent par l'**API DeepSeek en ligne** — `tools/llm/enseignant.py`
docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md:195:validation alignée. **Où** : `tools/llm/enseignant.py`, `tools/llm/distillation.py`,
docs/theorie/jeux-symboliques.md:176:| [`tools/jeux/mesure.py`](../../tools/jeux/mesure.py) | les séries et les contrôles |
docs/theorie/contrat-bloc-langue.md:146:- Le neuronal passe par l'**API DeepSeek** (`tools/llm/enseignant.py`) ou le **DRVM natif** ; les
docs/implantation/llm-externe.md:27:   `tools/llm/enseignant.py`.
docs/implantation/llm-externe.md:29:   `tools/llm/mesure.py`.
docs/implantation/llm-externe.md:72:| [`tools/llm/prompts_publics.jsonl`](../../tools/llm/prompts_publics.jsonl) | 60 prompts (pilote) et 310 (`prompts_public
… [259 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection du JSON de mesure des langues et de ses chiffres

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/jeux-langues-mesures.json'))\nprint('cles',list(d.keys()))\nfor k in ['couverture','corpus','invariance','permutation','detection','langue_detectee','notation','duree_s']:\n    v=d.get(k)\n    if isinstance(v,dict):\n        prin … [184 caractères tronqués]`

  ```
cles ['couverture', 'corpus', 'invariance', 'permutation', 'detection', 'langue_detectee', 'notation', 'duree_s']
couverture {'langues': 71, 'concepts': 35, 'couples': 1433, 'moyenne_concepts_par_langue': 20.13, 'n_langues_fortes': 32}
corpus {'items': 449, 'bons': 449, 'langues_avec_items': 66, 'langues_avec_items_forts': 62, 'minimum': 1.0, 'maximum': 1.0}
invariance {'paires': 11, 'invariantes': 11}
permutation {'items': 449, 'bons': 186, 'forts': 275, 'forts_bons': 12}
detection {'total': 315, 'bons': 315}
langue_detectee {'items': 449, 'exacts': 343}
notation {'items': 72, 'langues': 71, 'parses': 5112, 'bons': 5112}
duree_s 3.136
date? None
  ```

- **bash** `{"command": "grep -n \"53 langues\" tools/jeux/lexique_multilingue.py; grep -n \"71\" tools/jeux/lexique_multilingue.py | head -5; echo \"---\"; sed -n '1,15p' reports/rapport-s-fait-divers.md; echo \"---\"; sed -n '35,50p' reports/rapport-s-fait-divers.md", "description": "Vérifie docstring 53 et s … [24 caractères tronqués]`

  ```
2:"""lexique_multilingue.py — les libellés des jeux, en 53 langues.
---
# S — Le fait divers est tranché : 61/61 types, 144/144 rôles ; la tête du GN arrête le verbe

> **Ligne de roadmap** : S · **Date** : 2026-11-03 · **Verdict** : « Le fait divers surprend »
> ne coupe plus le verbe dans le GN. La règle v7 suit la **tête du GN** — dès qu'un nom est vu,
> un homographe qui suit un adjectif n'est plus le nom — et accepte un adjectif après
> l'homographe quand le verbe vient après. Le gold gagne `h061` (sixième vague) : **61/61
> types**, **144/144 rôles**, **50/50 compléments**, couverture **1,00** ; les contrôles restent
> à **104/144**, **106/144** et **0,10**. Les **56 tests** passent.

## La règle

L'analyseur butait sur « Le fait divers surprend » : « fait » est un homographe nom/verbe,
« divers » est un adjectif, et « surprend » un verbe. La v6 traitait « surprend » comme le nom
final (règle « adjectif + fin de phrase »), avalant tout le groupe. La v7 introduit la **tête du
GN** : dès que le GN a un nom (« fait », ou « lit » après « grand »), l'homographe suivant qui
---
« Lequel est-ce ? » (*Which way?*).

## La suite

La validation des neuf paragraphes sur `/paragraphes` (
… [495 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dernière lecture des fiches corpus et rôles pour les chiffres de l'analyseur

- **bash** `{"command": "sed -n '1,25p' reports/rapport-s-corpus-reel.md; echo \"===\"; sed -n '1,20p' reports/rapport-s-analyseur-roles.md", "description": "Lis verdicts corpus réel et rôles"}`

  ```
# S — L'analyseur lit le français propre (65,5 % de GN+GV), pas le CEGEP OCR (8,5 %, plancher du mélange)

> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur **50 000 lignes** et
> **20 799 phrases** du corpus **CEGEP OCR** (D/R/A, 4,41 M car.) et **50 000** lignes/phrases de
> **littérature propre** (17 M car.), l'analyseur trouve un **GN et un GV** dans **65,5 %** des
> phrases propres contre **9,1 %** quand les mots sont mélangés — le signal est la **langue**. Sur
> le CEGEP OCR, il est au **plancher du mélange** : **8,5 %** contre **9,1 %**. Le corpus CEGEP
> est **multilingue et technique** (les scans anglais de réseaux et d'algorithmique) et
> l'analyseur est **français** : ce n'est pas une mesure du français OCR, c'est une mesure de ce
> que le corpus n'est pas. L'unité compte : la ligne coupe les phrases (3,6 % contre 51,0 %).

## Le dispositif

- **CEGEP** : `data/corpus_ocr_cegep/train.txt` (D/R/A, 4,41 M car., OCR) ; **propre** :
  `data/corpus_fr_litterature.txt` (17 M car., texte natif).
- **Filtre** : lignes de 20–300 caractères (phrases 20–400), au moins 4 mots alphabétiques, au
  moins 80 % de lettres/espace/ponctuation ; échantillon **régulier**
… [2193 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"61/61\\|144/144\\|56 tests\\|gold\" reports/rapport-s-analyseur-roles.md | head -15; echo \"===\"; grep -n \"65,5\\|9,1\\|8,5\\|596\\|1 184\" reports/rapport-s-corpus-reel.md | head -15", "description": "Vérifie les chiffres dans les fiches"}`

  ```
3:> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur un gold de **55 phrases**
15:- **Gold** : [`tools/structures/donnees/gold-analyseur.json`](../tools/structures/donnees/gold-analyseur.json),
73:**Les deux limites sont fermées en v6** (le nom après adjectif devant un verbe, et en fin de phrase) ; la v6 ajoute la vague 5, le gold de 60 phrases (60/60 types, 142/142 rôles), et corrige le « si fort que » de conséquence — voir [`rapport-s-limites-v6.md`](rapport-s-limites-v6.md).
85:| **gold** (défaut) | `data/structures/banque.jsonl` | **55** | `reference` | `76accf9d…49dd1ac6` |
114:- **Le gold est de la même main que les règles** : les 16 `test` sont antérieurs, mais la vague 4
126:- Gold : `tools/structures/donnees/gold-analyseur.json` ; mesure :
136:3. **gold plus large** (voix, causatives, verbes à double complément) ;
===
1:# S — L'analyseur lit le français propre (65,5 % de GN+GV), pas le CEGEP OCR (8,5 %, plancher du mélange)
5:> **littérature propre** (17 M car.), l'analyseur trouve un **GN et un GV** dans **65,5 %** des
6:> phrases propres contre **9,1 %** quand les mots sont mélangés — le signal est la **langue**. Sur
7:> le CEGEP OCR, il est au **plan
… [730 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Construction de la table d'audit des 28 référents

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nsrc={p['id']:p for p in json.load(open('tools/structures/donnees/paragraphes.json'))['paragraphes']}\nvals=[json.loads(l) for l in open('tools/structures/donnees/paragraphes-validations.jsonl',encoding='utf-8') if l.strip()]\n# valeurs attendues (jugement … [1700 caractères tronqués]`

  ```
n 28 corrects 15 faux 13
('a001', 'Elle', 'Alice', 'Alice', True)
('a001', 'se', 'Alice', 'Alice', True)
('a001', 'elle', 'Alice', 'Alice', True)
('a001', 'lui', 'Alice', 'Alice', True)
('a001', 'en', 'Alice', None, False)
('a002', 'Elle', 'Alice', 'Alice', True)
('a002', 'en', 'Alice', None, False)
('a002', 'y', 'Alice', 'la boîte', False)
('a003', 'Elle', 'Alice', 'Alice', True)
('a003', 'sa', 'Alice', 'Alice', True)
('a003', 'elle', 'Alice', 'Alice', True)
('a003', 'se', 'Alice', 'Alice', True)
('a004', 'sa', 'ALICE', 'Alice', True)
('a005', 'elle', 'Alice', 'Alice', True)
('a005', 'son', 'Alice', 'Alice', True)
('a005', 'en', 'coup', 'la salle', False)
('a006', 'cela', 'Comme', 'attendre à la petite porte', False)
('a006', 'son', 'Alice', 'Alice', True)
('a006', 'elle', 'Alice', 'Alice', True)
('a006', 'y', 'table', 'la table', False)
('a008', 'Je', 'le contenu', 'Alice', False)
('a008', 'me', 'le contenu', 'Alice', False)
('a008', 'on', 'Je me sens toute drôle', None, False)
('a008', 'je', 'Je me sens toute drôle', 'Alice', False)
('a008', 'en', 'Je me sens toute drôle', None, False)
('a009', 'se', 'Un moment', 'Alice', False)
('a009', 'elle', 'Alice', 'Alice', True)
('a009', 
… [180 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Identification des 5 verdicts à risque lors d'une régénération

- **bash** `{"command": "cd tools/structures && PYTHONDONTWRITEBYTECODE=1 python3 - <<'EOF'\nimport json, generateur\nfixe=json.load(open('donnees/phrases.json'))['phrases']\ngen=json.load(open('donnees/phrases_generees.json'))['phrases']\nrows=[json.loads(l) for l in open('donnees/validations.jsonl',encoding=' … [458 caractères tronqués]`

  ```
('p006', 'p006-c2') compatible | stockés 2 dyn 1 | Elle a dit qu'elle viendrait hier.
('c023', 'c023-c3') exclu | stockés 3 dyn 2 | Le temps était assez beau, mais l'air froid, par ce vent d'est.
('c056', 'c056-c2') exclu | stockés 3 dyn 1 | Une fois à San Francisco, il verrait à se tirer d'affaire.
('c056', 'c056-c3') resolu | stockés 3 dyn 1 | Une fois à San Francisco, il verrait à se tirer d'affaire.
('c064', 'c064-c2') exclu | stockés 2 dyn 1 | Heureusement pour lui, la gare n'avait ni portes ni barrières.
  ```

