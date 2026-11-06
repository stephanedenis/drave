# Session DSH — relecture

- identifiant : `c5910cba-e10a-4e08-8ac7-449ce150899c`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 21:12:21
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer le round R1/R2/R3** (commit `f908d7b0`) et vérifier que ses chiffres, ses règles et ses portes sont justes.

Contexte : `tools/bloc_linguistique.py` (`Heuristique`, `_syntagmes_simple`, `SUJETS`, `MODAUX`, `SUB_PAR_LANGUE`), `tools/tests/linguistique/evaluer_gold.py`, `tools/tests/linguistique/gold_split.py` (dev/test), `tools/pensee/autotest.py` (183 portes). Fiche à auditer : `reports/rapport-pensee-r1r3.md` + `reports/pensee-r1r3.json`, et la fiche amont `reports/rapport-spans-v7.md` (A17).

Revendications à rejouer (au commit `f908d7b0`) : labels 212, exact 212 (1,0000), couverture 0,887, F1 union 0,5763 (S 0,4966, chunker 0,6057), tête 0,7316, fr 129/129, en 83/83, spans 27 (16 REL, 6 SUB, 5 GP), top-k 177.

À faire :
1. Rejoue chaque valeur (viвant 612 et gelé 602) et compare à la fiche/au JSON ; note les écarts.
2. **Ablations** : mesure l'effet de chaque règle séparément (R1 : pronom/`SUJETS` ; R1b : modaux ; R1c : second prédicat ; R2 : SUB sans précédent ; R3a : subordonnants par langue ; R3c : `fall`/`call`) sur le gold 612 et sur dev/test — gain/perte, ids.
3. **Contrôles négatifs** : permutation globale des cibles (≥200 tirages), candidat aléatoire, et vérifie que les 27 spans restants sont bien ceux listés (ids, langues, types).
4. **dev/test** : re-mesure les deux moitiés et compare à la fiche `rapport-dev-test-v7.md`.
5. Écris **uniquement** deux fichiers neufs : `reports/rapport-audit-r1r3.md` et `reports/pensee-audit-r1r3.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé avec les écarts, les ablations (gain/perte par règle) et les valeurs dev/test.
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

⏵ Exploring repo state and audit target files

- **bash** `{"command": "git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet status --short | head -50; echo \"---BRANCH---\"; git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet branch --show-current; echo \"---HEAD---\"; git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet log --oneline -5", "descript … [44 caractères tronqués]`

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
D  journal/sessions/3144cf23-6004-46ef-bc3d-f05d81c0cf
… [2339 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/ | grep -iE 'r1r3|dev-test|spans' ; echo \"---\"; ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/ | head -40", "description": "List relevant report files"}`

  ```
-rw-r--r--. 1 stephane stephane   60776  5 nov 20:11 pensee-dev-test-v7.json
-rw-r--r--. 1 stephane stephane     747  5 nov 21:08 pensee-r1r3.json
-rw-r--r--. 1 stephane stephane   45975  5 nov 16:00 pensee-spans-chunker.json
-rw-r--r--. 1 stephane stephane     986  5 nov 13:37 pensee-spans.json
-rw-r--r--. 1 stephane stephane   39678  5 nov 20:50 pensee-spans-v7.json
-rw-r--r--. 1 stephane stephane   14982  5 nov 20:13 rapport-dev-test-v7.md
-rw-r--r--. 1 stephane stephane    3857  5 nov 21:08 rapport-pensee-r1r3.md
-rw-r--r--. 1 stephane stephane    3968  5 nov 14:43 rapport-pensee-spans.md
-rw-------. 1 stephane stephane   15801  5 nov 16:03 rapport-spans-chunker.md
-rw-r--r--. 1 stephane stephane   38231  5 nov 20:50 rapport-spans-v7.md
---
total 18848
drwxr-xr-x. 1 stephane stephane   70006  5 nov 21:08 .
drwxr-xr-x. 1 stephane stephane     660  1 nov 10:50 ..
drwxr-xr-x. 1 stephane stephane     102 24 oct 15:52 07
-rw-r--r--. 1 stephane stephane    4447 28 oct 09:17 07-mesures-couche-commune.md
-rw-r--r--. 1 stephane stephane     907 29 oct 16:25 a26-bilan.json
-rw-r--r--. 1 stephane stephane    1163  1 nov 20:40 a26-lot-disque.json
-rw-r--r--. 1 stephane stephane    1121 30 
… [2427 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-r1r3.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-r1r3.json"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-r1r3.md</path>
<type>file</type>
<content>
1: # B13 — R1/R2/R3 : exact 212/212 (1,0000), couverture 0,887, F1 0,5763
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **État courant** : commit à jour
4: > (après `4ebeb683`) · **Verdict** : ✅
5: > **183/183 portes** : les quatre règles de la fiche [spans v7](rapport-spans-v7.md) (A17) sont
6: > intégrées — **R1** frontière de clause (pronom, modaux, second prédicat), **R2** SUB sans
7: > précédent, **R3a** subordonnants par langue, **R3c** `fall`/`call`. Résultat : **212 labels**
8: > (sur 239), **exact 212/212 = 1,0000** (fr **129/129**, en **83/83**), **couverture 0,887**,
9: > **F1 0,5763** (union ; S 0,4966, chunker 0,6057), tête **0,7316** ; **27 spans** restants
10: > (16 REL, 6 SUB, 5 GP), dont 17 sont **inatteignables** (lexique synthétique ou bug du gold).
11: >
12: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`SUJETS`, `MODAUX`,
13: > `SUB_PAR_LANGUE`, boucle REL/SUB), [`autotest.py`](../tools/pensee/autotest.py) (24 assertions) ;
14: > JSON [`pensee-r1r3.json`](pensee-r1r3.json).
15: 
16: ## 1. L
… [3017 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-r1r3.json</path>
<type>file</type>
<content>
1: {
2:  "date": "2026-11-05",
3:  "ligne": "B13",
4:  "portes": "183/183",
5:  "avant": {
6:   "labels": 196,
7:   "exact": 195,
8:   "couverture": 0.8201,
9:   "f1": 0.5595,
10:   "spans": 43
11:  },
12:  "apres": {
13:   "labels": 212,
14:   "exact": 212,
15:   "exact_span": 1.0,
16:   "couverture": 0.887,
17:   "f1": 0.5763,
18:   "f1_s": 0.4966,
19:   "f1_chunker": 0.6057,
20:   "tete": 0.7316,
21:   "fr": "129/129",
22:   "en": "83/83",
23:   "topk": 177,
24:   "topk_taux": 0.7406,
25:   "spans": {
26:    "REL": 16,
27:    "SUB": 6,
28:    "GP": 5,
29:    "total": 27
30:   },
31:   "inevitables": 17
32:  },
33:  "regles": [
34:   "R1 frontière de clause (pronom, modaux, second prédicat)",
35:   "R2 SUB sans précédent",
36:   "R3a subordonnants par langue",
37:   "R3c fall/call"
38:  ],
39:  "limites": [
40:   "27 spans",
41:   "test non aveugle",
42:   "in-sample",
43:   "gold 612"
44:  ]
45: }

(End of file - total 45 lines)
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/gold_split.py tools/pensee/autotest.py && echo \"---\" && git status --short tools/ reports/ docs/ | head -30", "description": "Check  … [36 caractères tronqués]`

  ```
2172 tools/bloc_linguistique.py
   305 tools/tests/linguistique/evaluer_gold.py
    50 tools/tests/linguistique/gold_split.py
  2835 tools/pensee/autotest.py
  5362 total
---
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-pensee-couverture-v7.md
 M reports/rapport-spans-chunker.md
 m tools/structures
?? reports/pensee-spans-v7.json
?? reports/rapport-s-paragraphes.md
?? reports/rapport-spans-v7.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def \\|SUJETS\\|MODAUX\\|SUB_PAR_LANGUE\\|SUB_PAR\\|__version__\" tools/bloc_linguistique.py | head -80", "description": "Inspect bloc_linguistique structure"}`

  ```
63:    def json(self) -> dict:
81:    def json(self) -> dict:
105:    def par_niveau(self) -> dict[str, list[Etiquette]]:
111:    def couverture(self) -> dict[str, float]:
116:    def json(self, avec_duree: bool = False) -> dict:
133:    def analyser(self, texte: str, langue: str | None = None,
144:def _normaliser(texte: str) -> str:
148:def _trigrammes(texte: str) -> list[str]:
153:def _profil(texte: str, top: int = 200) -> dict[str, int]:
158:def charger_profils_udhr(chemin: pathlib.Path, train=(0, 14), test=(15, 30),
192:def _score_profil(tri: collections.Counter, profil: dict[str, int]) -> float:
199:def detecter_langue(texte: str, profils: dict[str, dict] | None = None,
230:def _script_char(ch: str) -> str:
256:def detecter_script(texte: str) -> str:
372:SUJETS = {"i", "you", "he", "she", "it", "we", "they", "there",
378:SUB_PAR_LANGUE = {"fr": {"car", "parce", "puisque", "comme", "quand", "si", "lorsque"},
458:def _est_adverbe_seul(g: dict) -> bool:
464:MODAUX = {"would", "must", "can", "could", "should", "will", "shall", "may", "might", "ought",
470:def _sans_enclitique(mot: str) -> str:
478:def _est_verbe(mot: str) -> bool:
497:def _role_gp(prep: str) -> str:
527:    def __
… [3959 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 360, "limit": 140}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
360:     "contraste": set("mais cependant pourtant néanmoins toutefois en revanche whereas however "
361:                      "but yet although though nevertheless".split()),
362:     "cause": set("car parce puisque comme because since".split()),
363:     "conséquence": set("donc ainsi alors par conséquent consequently therefore hence so".split()),
364:     "but": set("pour afin pour que afin que in order to so that".split()),
365: }
366: 
367: RELATIFS = {"qui", "que", "qu", "dont", "où", "which", "that", "who", "whom", "whose",
368:             "where", "when"}
369: # les subordonnants qui n'ont pas d'antécédent : toujours SUB
370: AMBIGUES_PREP = {"since", "before", "after", "until", "as", "depuis", "avant", "après", "pendant", "durant"}
371: 
372: SUJETS = {"i", "you", "he", "she", "it", "we", "they", "there",
373:           "je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles"}
374: 
375: SUBORDONNANTS = {"because", "although", "though", "if", "while", "as", "since", "unless",
376:                  "whether", "car", "parce", "puisque", "comme", "quand",
… [8289 caractères tronqués]
  ```


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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json,pathlib\nbase=pathlib.Path('tools/tests/linguistique')\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json','gold_gele.json']:\n p=base/f\n d=json.loads(p.read_text(encoding='utf-8'))\n ph=d['phr … [270 caractères tronqués]`

  ```
gold.json 20 segments 56 cibles 18
gold_reel.json 432 segments 1445 cibles 185
gold_synthetique.json 160 segments 362 cibles 79
gold_gele.json 602 segments 1831 cibles 282
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"SUJETS\\|MODAUX\\|SUB_PAR_LANGUE\\|R1\\|R2\\|R3\\|fall\\|call\\|212\\|196\\|602\\|612\\|dev\\b\\|test\\b\" tools/pensee/autotest.py | head -120", "description": "Grep autotest for audit-relevant code"}`

  ```
2:"""autotest.py — les portes du moteur de pensée : T0–T4, puis AC-3 et alpha-bêta.
25:Usage : PYTHONPATH=. ~/gpu-env/bin/python tools/pensee/autotest.py
1571:    """Le vote pondéré : poids appris (1,0,0,0), test 7/10."""
1578:            and r["justes_test"] == 7), (
1579:        f"pondéré : poids {r['poids']}, test {r['justes_test']}/{r['test']}")
1589:    return r["test"] == 30 and r["justes"] == 25, (
1590:        f"CV 5 plis : {r['justes']}/{r['test']} liens justes")
1602:    ecart = round(statistics.pstdev(taux), 4)
1632:    """Le gold complet : 602 phrases, POS 0,7603 (gelé)."""
1638:    return (len(phrases) == 602
1671:    """Le segmenteur : S F1 0,4966 (français seul), chunker 0,6057 ; tête 0,6654 / 0,7558 (gelé 602)."""
1748:    """La cascade avec l'union : F1 0,5864, tête 0,7285, 602 appels neuronaux."""
1758:            and cascade.appels_neuronal == 602), (
1794:    return abs(r["fidelite"] - 0.196) < 0.001, (
1807:    return abs(fid - 0.196) < 0.001, f"sortie POS : fidélité {round(fid, 4)}"
1944:    """Le gold gelé : 602 phrases, les portes ne cassent plus."""
1947:    return len(gele) == 602, f"gold gelé : {len(gele)} phrases"
2125:    man = {"format": "DRVM", "versi
… [1058 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "offset": 2190, "limit": 360}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
2190:     return (abs(m["double_sens"] - 0.9884) < 0.001
2191:             and m["double_sens"] > h["double_sens"]), (
2192:         f"sous-type : double sens {m['double_sens']} (niveau {h['double_sens']})")
2193: 
2194: 
2195: def t151_soustype_variance() -> tuple[bool, str]:
2196:     """La variance du sous-type : 0,9838 à 0,3, le gain tient."""
2197:     import json
2198:     import pathlib
2199:     racine = pathlib.Path(__file__).resolve().parents[2]
2200:     d = json.loads((racine / "reports/pensee-quatre-modes-432-soustype-t03.json").read_text(encoding="utf-8"))
2201:     m = d["modes"]["parallele_niveau"]["all"]["pragmatique"]
2202:     h = d["modes"]["heuristique"]["all"]["pragmatique"]
2203:     return abs(m["double_sens"] - 0.9838) < 0.001 and m["double_sens"] > h["double_sens"], (
2204:         f"sous-type 0,3 : double sens {m['double_sens']} > {h['double_sens']}")
2205: 
2206: 
2207: def t152_tirages() -> tuple[bool, str]:
2208:     """Les trois tirages : 0,9838 exactement — le modèle est déterministe sur ces invites."""
2209:     import json
2210:     imp
… [17865 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"0\\.7316\\|0\\.5763\\|0\\.4966\\|0\\.6057\\|0,887\\|0.887\\|177\\|27\" tools/pensee/autotest.py | sed -n '1,100p'", "description": "Locate fiche numbers in autotest"}`

  ```
482:def t27_correction() -> tuple[bool, str]:
1405:    return abs(r["pos"]["exactitude"] - 0.7327) < 0.001, (
1529:    """Le plafond du gold : quatre règles, la meilleure fait 27/30."""
1541:    return max(scores.values()) == 27, (
1621:          and mesurer(tout, ignorer_pp=True)["justes"] == 27
1628:    return ok, "bilan : 4/4, 10/12, 12/12, 8/8, 27/30, méta 25/30, CV ~0,85"
1684:    return (abs(f1 - 0.4966) < 0.001 and abs(f2 - 0.6057) < 0.001
1731:    return abs(f1 - 0.5763) < 0.001, f"union : segments F1 {f1} (S 0,4966)"
1743:    return abs(f1 - 0.5763) < 0.001 and abs(tete - 0.7316) < 0.001, (
1914:def t127_negatives() -> tuple[bool, str]:
1981:    ph = [p for p in charger() if 301 <= int(p["id"][1:]) <= 427]
1991:    ph = [p for p in charger() if 301 <= int(p["id"][1:]) <= 427]
2002:    ph = [p for p in charger() if 301 <= int(p["id"][1:]) <= 427]
2226:    return (r["cibles"] == 239 and abs(r["top1_taux"] - 0.887) < 0.001
2227:            and abs(r["exact_taux"] - 0.887) < 0.001), (
2355:    return (a["topk"] == 177 and th["topk"] == 178 and a["top1"] == 212), (
2378:    return span == 27 and cible == 35, (
2532:    return (a["topk"] == 177 and a["topk_exact"] == 177
2590:de
… [327 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "limit": 290, "offset": 2549}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
2549: def t175_audit_attachement() -> tuple[bool, str]:
2550:     """L'audit A1 : les 14 valeurs reproduites, écart 0, et le JSON d'audit à jour."""
2551:     import json
2552:     import pathlib
2553:     import tools.bloc_linguistique as bl
2554:     from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
2555:     racine = pathlib.Path(__file__).resolve().parents[2]
2556:     d = json.loads((racine / "reports/pensee-audit-attachement.json").read_text(encoding="utf-8"))
2557:     m = d["mesure"]
2558:     a = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
2559:     # l'audit est un **instantané daté** : la porte vérifie sa structure et ses 14 valeurs,
2560:     # pas l'égalité au courant (le courant évolue, l'audit reste la référence de son commit).
2561:     ok = (d["verdict"]["valeurs_reproduites"] == 14 and d["verdict"]["ecarts"] == 0
2562:           and m["cibles"] == 239 and m["labels"] == 145 and m["top1"] == 126
2563:           and m["topk_sous_chaine"] == 134 and m["exact"] == 123
2564:           and m["topk_strict"] == 88 and m["ver
… [15905 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", "limit": 160, "offset": 1630}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
1630: 
1631: def t107_gold_complet() -> tuple[bool, str]:
1632:     """Le gold complet : 602 phrases, POS 0,7603 (gelé)."""
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
1645:     """La coréférence à 68 liens : 52/68 par le rôle, 51/68 par le dernier nom."""
1646:     from ..tests.linguistique.anaphore import mesurer, mesurer_roles
1647:     from ..tests.linguistique.gold_reel import construire
1648:     g = construire()
1649:     ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 372]
1650:     dernier = mesurer(ps, ignorer_pp=True)
1651
… [7244 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 200, "offset": 638}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
638:     def _syntagmes_s(self, texte: str) -> list[dict] | None:
639:         if not self.segmenter_s:
640:             return None
641:         try:
642:             if str(RACINE / "tools/structures") not in sys.path:
643:                 sys.path.insert(0, str(RACINE / "tools/structures"))
644:             import generateur  # le générateur S, importé en lecture seule
645:             return generateur.analyser(texte)
646:         except Exception:
647:             return None
648: 
649:     def _cibles_s(self, texte: str) -> dict:
650:         """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).
651: 
652:         Lecture seule de l'API interne du S : `_tokens`/`_segmente` rendent les `Segment` avec
653:         `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
654:         (GP, puis GN, puis GV), comme le premier candidat de `analyser`.
655:         """
656:         if not self.segmenter_s:
657:             return {}
658:         try:
659:             import generateur
660:             base = generateur
… [9693 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 150, "offset": 845}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
845:     def _syntagmes_simple(self, texte: str, langue: str,
846:                           pos_verbes: set[int] | None = None) -> list[dict]:
847:         mots = self._mots(texte)
848:         lex = POS_FERME.get(langue, POS_FERME["fr"])
849:         pos_verbes = pos_verbes or set()
850:         par_debut = {m[0]: k for k, m in enumerate(mots)}
851: 
852:         def est_verbe(d: int, m: str) -> bool:
853:             """Le verbe : le lexique, le POS, ou la **position** après un pronom sujet."""
854:             if _est_verbe(m) or d in pos_verbes:
855:                 return True
856:             n2 = _normaliser(m)
857:             if n2 in lex.get("DET", set()) or n2 in lex.get("PREP", set()) or n2 in lex.get("CONJ", set()):
858:                 return False
859:             idx = par_debut.get(d)
860:             if idx is not None and idx > 0:
861:                 avant = _normaliser(mots[idx - 1][2])
862:                 if avant in SUJETS:
863:                     return True
864:             return False
865:         segments: list[dict] = []
866:         i 
… [8549 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"MODAUX\\|SUJETS\\|SUB_PAR_LANGUE\\|SUBORDONNANTS\\|AMBIGUES_PREP\\|fall\\|call\" tools/bloc_linguistique.py", "description": "Find all R1/R2/R3 rule sites"}`

  ```
370:AMBIGUES_PREP = {"since", "before", "after", "until", "as", "depuis", "avant", "après", "pendant", "durant"}
372:SUJETS = {"i", "you", "he", "she", "it", "we", "they", "there",
375:SUBORDONNANTS = {"because", "although", "though", "if", "while", "as", "since", "unless",
378:SUB_PAR_LANGUE = {"fr": {"car", "parce", "puisque", "comme", "quand", "si", "lorsque"},
436:fall falls fell fallen falling call calls called calling
464:MODAUX = {"would", "must", "can", "could", "should", "will", "shall", "may", "might", "ought",
595:                              r"faut|falloir|might|may|must|should|could|would|can)\b", phrase, re.I))
862:                if avant in SUJETS:
870:            if typ == "mot" and (n in RELATIFS or n in SUBORDONNANTS
871:                                 or n in SUB_PAR_LANGUE.get(langue, set())):
874:                prep_ambigue = (n in AMBIGUES_PREP and (suivant is None
885:                    stype = "SUB" if (n in SUBORDONNANTS or precedent == "GV"
933:                       and _normaliser(mots[j][2]) not in SUBORDONNANTS
956:                       and _normaliser(mots[j][2]) not in SUBORDONNANTS):
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -20 -- tools/bloc_linguistique.py && echo \"---DIFF f908d7b0---\" && git show --stat f908d7b0 | head -40", "description": "Inspect commit history and target commit stat"}`

  ```
f908d7b0 B13 — R1/R2/R3 : EXACT 212/212 (1,0000), COUVERTURE 0,887, F1 0,5763, FR 1,0 / EN 1,0 ; 27 SPANS DONT 17 INATTEIGNABLES ; 183/183
69bd865e B13 — LA COUVERTURE À 0,8201 : POS CONTEXTUEL 0,7603, F1 0,5595, EXACT 195/196 (0,9949), 43 SPANS ; 183/183
0ec6c27d B13 — L'ATTACHEMENT PARFAIT SUR LES SPANS PRÉDITS : 187/187 (1,0000), FR 1,0, EN 1,0, DEV 126/126, TEST 61/61 ; RENDEMENT 0,7824 ; 183/183
b975011b B13 — LES CANDIDATS DU PRÉCÉDENT : EXACT 186/187 (0,9947), ANGLAIS 60/60, DEV 126/126 ; 183/183
7a9f0d6a B13 — LA COUVERTURE : 187 LABELS, EXACT 185/187 (0,9893), F1 0,5156, DEV 125/126 ET TEST 60/61 ; 183/183
392f03aa B13 — S NE SEGMENTE QUE LE FRANÇAIS : F1 0,4194 → 0,4539, TÊTE 0,6432 ; EXACT 157/160, FR 0,9915 / EN 0,9524 ; 183/183
cceacc1a B13 — LA SEGMENTATION D'ABORD : F1 0,2862 → 0,4194, EXACT 158/160 (0,9875), COUVERTURE 160/239, FR 0,9915 / EN 0,9762 ; 183/183
e59ba071 B13 — MULTI-CIBLES (EXACT_ANY 143/145), AUDITS A8/A10/A13 INTÉGRÉS, DOCSTRINGS ET CODE MORT NETTOYÉS ; 182/182
b1b1292f B13 — LE CACHE COMPLET : UN SEUL CHUNKING DANS LES DEUX CHEMINS (T178), VALIDÉ PAR A11 (×11,0, ÉGALITÉ 612/612) ; 181/181
dcf7bc91 B13 — L'ATTACHEMENT V3 : EXACT 0,9448 → 0,9724, NOMS
… [2919 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show f908d7b0 -- tools/bloc_linguistique.py", "description": "Show target commit diff for linguistic block"}`

  ```
commit f908d7b0613c8a5eb8fae7fab514bfdc5fa4668b
Author: Stéphane <stephane@localhost>
Date:   Thu Nov 5 21:08:09 2026 -0500

    B13 — R1/R2/R3 : EXACT 212/212 (1,0000), COUVERTURE 0,887, F1 0,5763, FR 1,0 / EN 1,0 ; 27 SPANS DONT 17 INATTEIGNABLES ; 183/183

diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 364b3545..80eccd3c 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -369,11 +369,15 @@ RELATIFS = {"qui", "que", "qu", "dont", "où", "which", "that", "who", "whom", "
 # les subordonnants qui n'ont pas d'antécédent : toujours SUB
 AMBIGUES_PREP = {"since", "before", "after", "until", "as", "depuis", "avant", "après", "pendant", "durant"}
 
-SUJETS = {"i", "you", "he", "she", "it", "we", "they", "who", "that", "which", "there",
-          "je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles", "qui", "qu"}
+SUJETS = {"i", "you", "he", "she", "it", "we", "they", "there",
+          "je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles"}
 
 SUBORDONNANTS = {"because", "although", "though", "if", "while", "as", "since", "unless",
                  "whether", "car", "parce", "puisque", "comme", "quand", "si", "lorsq
… [5112 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_split.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v7.md", "limit": 160}`

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
… [9658 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"R1\\|R2\\|R3\\|27\\|17 \\|inatteignable\\|fall\\|call\\|car\\b\" reports/rapport-spans-v7.md | head -80", "description": "Find R1/R2/R3 claims in spans v7 report"}`

  ```
17:43 non prédits = **21 REL, 17 SUB, 5 GP**. **État final** de la meilleure combinaison :
19:**17 cibles non couvertes** (8 REL, 5 SUB, 4 GP), toutes explicitement classées au § 7.
25:| exacts (span + cible) | 195 | 222 | **+27** |
37:> utilisée ici. L'attachement (196/195) est identique sur les deux golds, car les 10 phrases
44:| **R1** | frontière de clause REL/SUB (pronom, modaux, 2e prédicat) | **+15 / −0** | **+5 / −0** | **+20 / −0** |
45:| **R2** | type REL/SUB par antécédent | **+3 / −0** (+1 label faux, r245) | 0 / −0 | **+3 / −0** |
46:| **R3** | trois gardes de lexique/contexte (a `car`, b GP/déterminant, c `fall`/`call`) | **+1 / −0** seule ; **+3** en marge de R1+R2 | **+1 / −0** | **+2 / −0** seule ; **+4** en marge |
47:| **R1+R2+R3** | combinaison | **154 / 154** | **68 / 68** | **222 / 222** |
57:- **Split** : `crc32(id) % 3 == 0` → test. **dev** = 422 phrases / **163 cibles** (fr 277,
63:  est **recopiée** et instrumentée par des drapeaux (R1, R2, R3GP, R4, NOADV). Aucun
77:| **Frontière de clause (arrêt précoce + 2e prédicat)** | **20** | 12 REL / 8 SUB / 0 GP | le scanner REL/SUB s'arrête au pronom pris pour un verbe, ou avale le 2e prédicat | R1 | 20 exacts |

… [7179 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' reports/rapport-spans-v7.md", "description": "Read start of spans v7 report"}`

  ```
# Rapport — les 43 spans non prédits de l'attachement v7

> **Ligne de roadmap** : **B13** (attachement, règle 6) · **Date** : 2026-11-05 ·
> **Commit de départ** : `69bd865ec1bae1958b6f617bde4bf685a15d7d67` (branche `s/v7`) ·
> **Périmètre** : `tools/bloc_linguistique.py` (`Heuristique`, `_syntagmes_simple`,
> `_cible_precedent`), `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bloc`),
> `tools/tests/linguistique/gold_split.py` (`dev`, `test`).
> **Livrables** : ce rapport + [`pensee-spans-v7.json`](pensee-spans-v7.json).
> **Aucun fichier existant n'a été modifié par cette session** ; les mesures viennent d'une copie locale
> (`/tmp/spans/sim3.py`, sous-classe de `Heuristique` + copie instrumentée de
> `_syntagmes_simple`), non commitée. Le dispositif officiel (`evaluer_bloc`) redonne
> **exactement** la ligne de base 196/195 et F1 0,5555 sur le gold vivant 612.

## 1. Résumé

**État de départ** : 239 cibles, **196 labels au bon span**, **195 exacts / 196** (0,9949),
43 non prédits = **21 REL, 17 SUB, 5 GP**. **État final** de la meilleure combinaison :
**222 labels, 222 exacts / 222** (1,0000), soit **222/239 = 0,9289** des cibles ; il reste
**17 cibles non couve
… [7074 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git -C tools/structures status --short | head -20; echo \"---HEAD sub---\"; git -C tools/structures log --oneline -3; echo \"---diff tools---\"; git diff --stat HEAD -- tools/bloc_linguistique.py tools/pensee/autotest.py tools/tests/ … [81 caractères tronqués]`

  ```
M donnees/paragraphes-validations.jsonl
---HEAD sub---
523d8c1 S — LE FAIT DIVERS EST TRANCHÉ : 61/61 TYPES, 144/144 RÔLES ; LA TÊTE DU GN ARRÊTE LE VERBE
4012729 S — LA BANQUE DE PARAGRAPHES PASSE À NEUF : SIX PAIRES D'ALICE, SOURCES ANGLAISES ET RÉFÉRENTS
7ccc60f S — VALIDATION HUMAINE : 8 VERDICTS DE RÉFÉRENTS SUR /PARAGRAPHES (a001–a003) + 8 VERDICTS BANQUE (p003, c010, c066, c067)
---diff tools---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 tools/tests/linguistique/evaluer_gold.py 2>&1 | tail -20; echo EXIT:$?", "description": "Run baseline evaluator on gold"}`

  ```
"cibles": 151,
      "labels": 114,
      "exact": 114,
      "topk": 106,
      "exact_taux_span": 1.0
     },
     "en": {
      "cibles": 88,
      "labels": 83,
      "exact": 83,
      "topk": 57,
      "exact_taux_span": 1.0
     }
    }
   },
   "attachement_tete": {
    "cibles": 197,
    "labels": 197,
    "top1": 19
heuristique all: {"pos": {"exactitude": 0.7581, "exactitude_ferme": 0.9004, "exactitude_ouvert": 0.6234, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 50, "NOUN": 80, "VERB": 4}, "ADV": {"ADV": 117, "NOUN": 20, "PREP": 2, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 118, "?": 3, "NOUN": 3}, "CONJ": {"CONJ": 44, "PRON": 25, "DET": 12, "?": 13, "PREP": 2, "NOUN": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 657, "ADJ": 17, "VERB": 7, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"?": 25}, "PREP": {"PREP": 114}, "PRON": {"PRON": 411, "NOUN": 8, "?": 30, "DET": 25, "CONJ": 1}, "VERB": {"VERB": 311, "NOUN": 450, "ADJ": 5, "PREP": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.6157, "rappel": 0.5341, "f1": 0.572, "tp": 995, "fp": 621, "fn": 868, "tete": {"precision": 0.8012, "rappel": 0.664, "f1": 0.7262, "tp": 1237, "fp": 307, "fn": 626}}, "pragmatique
… [121 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^RACINE\\|^import\\|^from\\|POS_FERME\" tools/bloc_linguistique.py | head -40", "description": "Check module imports and RACINE"}`

  ```
30:from __future__ import annotations
32:import os
34:import argparse
35:import collections
36:import copy
37:import json
38:import pathlib
39:import re
40:import subprocess
41:import sys
42:import threading
43:import time
44:import unicodedata
45:import urllib.request
46:from dataclasses import dataclass, field
47:from typing import Protocol, Sequence
49:RACINE = pathlib.Path(__file__).resolve().parent.parent
298:POS_FERME = {
599:        lex = POS_FERME.get(langue, POS_FERME["fr"])
848:        lex = POS_FERME.get(langue, POS_FERME["fr"])
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nd=json.load(open('reports/pensee-spans-v7.json'))\nprint(type(d), list(d)[:20])\nfor k,v in d.items():\n    if isinstance(v,dict): print(k, list(v)[:12])\n    elif isinstance(v,list): print(k, len(v), v[:2 … [81 caractères tronqués]`

  ```
<class 'dict'> ['rapport', 'ligne', 'branche', 'commit', 'date', 'objet', 'methode', 'etat_depart', 'etat_final', 'par_langue_type', 'dev_test', 'causes', 'cas', 'regles', 'variantes', 'regles_rejetees', 'non_recuperables', 'controle_negatif', 'limites', 'recommandation']
rapport spans-v7
ligne B13
branche s/v7
commit 69bd865ec1bae1958b6f617bde4bf685a15d7d67
date 2026-11-05
objet Diagnostic des 43 spans non prédits de l'attachement v7 et règles chiffrées, sans modifier le code.
methode ['gold', 'split', 'harnais', 'fidelite', 'reglage']
etat_depart ['cibles', 'labels', 'exacts', 'exact_taux_span', 'couverture', 'exact_taux_cibles', 'f1', 'fr_exacts', 'en_exacts', 'fr_cibles', 'en_cibles', 'fr_labels']
etat_final ['cibles', 'labels', 'exacts', 'exact_taux_span', 'couverture', 'exact_taux_cibles', 'f1', 'fr_exacts', 'en_exacts', 'fr_cibles', 'en_cibles', 'fr_labels']
par_langue_type ['base', 'final']
dev_test ['dev', 'test']
causes 9 [{'cause': 'Frontière de clause', 'effectif': 20, 'types': {'REL': 12, 'SUB': 8, 'GP': 0}, 'ids': ['g017', 'r034', 'r074', 'r114', 'r115', 'r205', 'r214', 'r216', 'r219', 'r224', 'r239', 'r240', 'r243', 'r247', 'r278', 'r281', 'r285', 'r291', 'r296', 'r2
… [5998 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nd=json.load(open('reports/pensee-spans-v7.json'))\nprint('ETAT FINAL'); print(json.dumps(d['etat_final'],ensure_ascii=False,indent=1))\nprint('NON RECUPERABLES'); print(json.dumps(d['non_recuperables'],ens … [316 caractères tronqués]`

  ```
ETAT FINAL
{
 "cibles": 239,
 "labels": 222,
 "exacts": 222,
 "exact_taux_span": 1.0,
 "couverture": 0.9289,
 "exact_taux_cibles": 0.9289,
 "f1": 0.5851,
 "fr_exacts": 136,
 "en_exacts": 86,
 "fr_cibles": 151,
 "en_cibles": 88,
 "fr_labels": 136,
 "en_labels": 86,
 "reste_absent": {
  "REL": 8,
  "SUB": 5,
  "GP": 4,
  "total": 17
 },
 "faux": 0
}
NON RECUPERABLES
{
 "non_recuperables_par_regle_justifiee": {
  "effectif": 13,
  "gold_synthetique_sans_preposition": {
   "n": 4,
   "ids": [
    "s027",
    "s146",
    "s148",
    "s160"
   ],
   "pourquoi": "gold_synthetique.py ligne 98 : i = v + index(prep) + 1, le GP gold démarre après la préposition",
   "que_faire": "corriger le gold (démarrer à la préposition) : contrefactuel +4 exacts, 0 perte"
  },
  "lexique_disjoint_synthetique": {
   "n": 9,
   "REL": [
    "s010",
    "s035",
    "s061",
    "s065",
    "s125",
    "s141"
   ],
   "SUB": [
    "s044",
    "s112",
    "s114"
   ],
   "pourquoi": "le lexique verbal du générateur est disjoint ; 7 lemmes manquent",
   "que_faire": "ajouter les 7 lemmes = +8 exacts mais mesure invalide ; s065 reste absent (antécédent elle non GN)"
  }
 },
 "recuperables_hors_perimetre": {
  "ef
… [2688 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 70, "offset": 520}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
520: 
521: 
522: class Heuristique:
523:     """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""
524: 
525:     nom = "heuristique"
526: 
527:     def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
528:                  seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
529:                  union: bool = True):
530:         self.profils = profils
531:         self.segmenter_s = segmenter_s
532:         self.seuil_ouvert = seuil_ouvert
533:         self.seuil_langue = seuil_langue
534:         self.union = union
535: 
536:     # -- langues / script ---------------------------------------------------
537:     def _langue(self, texte: str, indice: str | None) -> tuple[str, float, str]:
538:         langue, conf, _ = detecter_langue(texte, self.profils, indice)
539:         script = detecter_script(texte)
540:         if conf < self.seuil_langue:
541:             return "und", conf, script
542:         return langue, conf, script
543: 
544:     # -- tokens ---------------------------------
… [2317 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Building measurement harness for replay and ablations

- **bash** `{"command": "mkdir -p /tmp/audit_r1r3/mods && cat > /tmp/audit_r1r3/harness.py <<'PY'\n\"\"\"Harnais d'audit R1/R2/R3 — mesures sur le gold vivant 612 et gelé 602.\n\nAucun fichier du dépôt n'est modifié : les variantes du bloc sont copiées dans /tmp et\nimportées comme modules distincts ; le module … [19461 caractères tronqués]`

  ```
Traceback (most recent call last):
  File "/tmp/audit_r1r3/harness.py", line 392, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/tmp/audit_r1r3/harness.py", line 316, in main
    variantes = construit_variantes()
  File "/tmp/audit_r1r3/harness.py", line 107, in construit_variantes
    base = charger_module("base", [])
  File "/tmp/audit_r1r3/harness.py", line 101, in charger_module
    spec.loader.exec_module(mod)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^
  File "<frozen importlib._bootstrap_external>", line 1027, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/tmp/audit_r1r3/mods/base.py", line 58, in <module>
    @dataclass(frozen=True)
     ~~~~~~~~~^^^^^^^^^^^^^
  File "/usr/lib64/python3.13/dataclasses.py", line 1344, in wrap
    return _process_class(cls, init, repr, eq, order, unsafe_hash,
                          frozen, match_args, kw_only, slots,
                          weakref_slot)
  File "/usr/lib64/python3.13/dataclasses.py", line 997, in _process_class
    and _is_type(type, cls, dataclasses, dataclasses.KW_ONLY,
        ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
             
… [313 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_r1r3 && python3 - <<'PY'\np='harness.py'\ns=open(p).read()\ns=s.replace(\"\"\"    mod = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(mod)\"\"\",\"\"\"    mod = importlib.util.module_from_spec(spec)\n    sys.modules[spec.name] = mod\n    spec.loader.ex … [256 caractères tronqués]`

  ```
{
     "id": "s044",
     "type": "SUB",
     "langue": "fr"
    },
    {
     "id": "s114",
     "type": "SUB",
     "langue": "fr"
    }
   ]
  },
  "test": {
   "phrases": 190,
   "cibles": 76,
   "labels": 64,
   "exact": 64,
   "couverture": 0.8421,
   "exact_taux_span": 1.0,
   "f1": 0.5714,
   "tete": 0.7241,
   "par_langue": {
    "fr": {
     "cibles": 50,
     "labels": 40,
     "exact": 40,
     "topk": 38
    },
    "en": {
     "cibles": 26,
     "labels": 24,
     "exact": 24,
     "topk": 19
    }
   },
   "spans_absents": [
    {
     "id": "r153",
     "type": "GP",
     "langue": "en"
    },
    {
     "id": "s160",
     "type": "GP",
     "langue": "fr"
    },
    {
     "id": "s146",
     "type": "GP",
     "langue": "fr"
    },
    {
     "id": "s141",
     "type": "REL",
     "langue": "fr"
    },
    {
     "id": "s032",
     "type": "REL",
     "langue": "fr"
    },
    {
     "id": "s035",
     "type": "REL",
     "langue": "fr"
    },
    {
     "id": "r255",
     "type": "REL",
     "langue": "fr"
    },
    {
     "id": "s115",
     "type": "REL",
     "langue": "fr"
    },
    {
     "id": "s072",
     "type": "REL",
     "langue": "fr"
    },
    {
   
… [226 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_r1r3 && python3 - <<'PY'\nimport json\nd=json.load(open('resultats.json'))\nprint('GOLD', d['gold'])\nprint('BASELINE ATTACHEMENT VIVANT')\nprint(json.dumps(d['baseline']['attachement_vivant'], indent=1))\nprint('SEGMENTATION GELE')\nprint(json.dumps(d['baseline']['segment … [482 caractères tronqués]`

  ```
GOLD {'vivant': 612, 'gele': 602, 'dev': 422, 'test': 190}
BASELINE ATTACHEMENT VIVANT
{
 "cibles": 239,
 "labels": 212,
 "exact": 212,
 "exact_any": 212,
 "topk": 177,
 "topk_exact": 177,
 "couverture": 0.887,
 "exact_taux_span": 1.0,
 "exact_taux_cibles": 0.887,
 "topk_taux": 0.7406,
 "topk_taux_span": 0.8349,
 "par_langue": {
  "fr": {
   "cibles": 151,
   "labels": 129,
   "exact": 129,
   "topk": 120
  },
  "en": {
   "cibles": 88,
   "labels": 83,
   "exact": 83,
   "topk": 57
  }
 }
}
SEGMENTATION GELE
{
 "union": {
  "segments": {
   "precision": 0.6183,
   "rappel": 0.5396,
   "f1": 0.5763,
   "tp": 988,
   "fp": 610,
   "fn": 843
  },
  "tete": {
   "precision": 0.8047,
   "rappel": 0.6707,
   "f1": 0.7316,
   "tp": 1228,
   "fp": 298,
   "fn": 603
  }
 },
 "s": {
  "segments": {
   "precision": 0.5986,
   "rappel": 0.4244,
   "f1": 0.4966,
   "tp": 777,
   "fp": 521,
   "fn": 1054
  },
  "tete": {
   "precision": 0.802,
   "rappel": 0.5685,
   "f1": 0.6654,
   "tp": 1041,
   "fp": 257,
   "fn": 790
  }
 },
 "chunker": {
  "segments": {
   "precision": 0.7384,
   "rappel": 0.5134,
   "f1": 0.6057,
   "tp": 940,
   "fp": 333,
   "fn": 891
  },
  "tete": {
   "precision": 0
… [2844 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/audit_r1r3 && python3 - <<'PY'\nimport json, collections\nd=json.load(open('resultats.json'))\nsp=d['spans_absents']\nprint('n=',len(sp), collections.Counter(x['type'] for x in sp), collections.Counter(x['langue'] for x in sp))\nfor x in sp:\n    print(x['id'], x['langue'], x['t … [1250 caractères tronqués]`

  ```
n= 27 Counter({'REL': 16, 'SUB': 6, 'GP': 5}) Counter({'fr': 22, 'en': 5})
r153 en GP 8:19 'for the bus' -> wait
s160 fr GP 20:29 'le renard' -> nage
s027 fr GP 31:33 'il' -> marche
s146 fr GP 25:35 'les jardin' -> observe
s148 fr GP 20:39 'les ancienne lettre' -> nage
s037 fr REL 5:15 'qui marche' -> Paul
s141 fr REL 5:15 'qui trouve' -> Emma
s065 fr REL 5:17 'qui commence' -> elle
s010 fr REL 10:18 'qui nage' -> chemin
s061 fr REL 9:18 'qui saute' -> nuage
s032 fr REL 11:19 'qui crie' -> village
s035 fr REL 10:19 'qui ferme' -> papier
r280 en REL 8:21 'that I bought' -> car
s125 fr REL 11:21 'qui compte' -> renard
s135 fr REL 11:22 'qui dessine' -> fenêtre
r273 fr REL 9:23 'qui pousse ici' -> fleur
s069 fr REL 15:23 'qui crie' -> canard
r035 en REL 9:24 'she talks about' -> film
r255 fr REL 11:27 "que j'ai achetée" -> voiture
s115 fr REL 19:30 'qui observe' -> fenêtre
s072 fr REL 20:31 'qui dessine' -> chanson
r264 fr SUB 8:26 "qu'il vient demain" -> sais
g017 en SUB 9:28 'that she would come' -> said
r288 en SUB 7:29 'that he comes tomorrow' -> know
s044 fr SUB 17:29 'que ils crie' -> nage
s112 fr SUB 24:39 'que Lucas ferme' -> nage
s114 fr SUB 22:43 'que les avocat compte' -> d
… [453 caractères tronqués]
  ```

