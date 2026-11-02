# Session DSH — relecture

- identifiant : `536cd5d6-94ac-4057-8fe9-11709a4587c7`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-02 15:33:01
- agent : standard


## Tour 1

### 👤 Utilisateur

étudie l'état de toutes les sessions et le pilotage

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
réseau sont des **faits** regroupés en **listes valuées poussées** vers leurs lecteurs : le coût du calcul devient proportionnel à l'**activité**, et le modèle devient **décomposable**, **répartissable** et **observable**. Le projet a pour principe que la structure bat la taille. Construire le moteur et modèle optimisé qui rend cette structure observable, décomposable, répartissable et rejouable permet d'atteindre de nouveaux sommets. Bref, révolutionner l'IA avec une approche par bus d'événements où chaque bloc fonctionnel est optimisable, comparable et substituable par des alternatives ayant des architectures différentes. e.g. Blocs neuronaux là où l'intuition est un avantage, blocs computationnels classiques pour les opérations où l'informatique classique est plus fiable et performante.

Le projet est né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de
les **combiner**, de les **décomposer en couches et grappes de neurones** exécutables par du matériel divers, voire
**distribué en réseau**, de les **diagnostiquer et faire évoluer** en étudiant leurs **flux**, et de **rejouer à
volonté** des événements.


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

### 🤖 Assistant

⏵ Je vais d'abord lire l'état courant du pilotage.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-02, 15 h 20 HNE (heure locale, EST).**
4: 
5: > **État courant, pas histoire.** Une sous-section par **session active**, une ligne par **chantier**
6: > avec son **bloquant**. Méthode : [`methode/`](../methode/) (contexte, continuité). Résultats :
7: > [`reports/`](../../reports/). Histoire : [`journal/`](../../journal/). Plan : [`roadmap.md`](roadmap.md).
8: 
9: ## Sessions en cours
10: 
11: > Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
12: > [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
13: > `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
14: > le hook pre-commit refuse un fait sans ligne d'état ; une session qui trouve l'état en retard
15: > le corrige.
16: 
17: ### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3
18: 
19: - **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
20: -
… [11960 caractères tronqués]
  ```

- **bash** `{"command": "ls -la && echo \"---\" && ls docs/pilotage/ && echo \"---\" && git log --oneline -15", "description": "List repo root, pilotage dir, recent commits"}`

  ```
total 204
drwxr-xr-x. 1 stephane stephane   660  1 nov 10:50 .
drwxr-xr-x. 1 stephane stephane  2496  1 nov 10:47 ..
-rw-r--r--. 1 stephane stephane  9882 29 oct 16:01 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2484  2 nov 12:25 data
drwxr-xr-x. 1 stephane stephane   124 31 oct 18:00 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   198  2 nov 14:38 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   832  2 nov 00:00 journal
drwxr-xr-x. 1 stephane stephane   100 15 oct 09:02 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 19956 29 oct 08:14 README.md
drwxr-xr-x. 1 stephane stephane 57116  2 nov 14:40 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane 10507 30 sep 
… [2259 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lance l'inventaire des sessions et des documents de pilotage.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== journal/sessions ===\" && ls -1 journal/sessions/ && echo && echo \"=== plans ===\" && for d in journal/sessions/*/; do echo \"--- $d\"; ls -1 \"$d\" | head -20; done", "description": "List sessions dirs and their contents … [2 caractères tronqués]`

  ```
=== journal/sessions ===
00221850-90de-4287-90ee-324a35e504cd
04ed1834-b0f8-42a1-aa21-75a75c19647e
0b0a6a0d-05f5-4308-800c-4792ddb9cbf2
0b2c86eb-7a8d-4eed-a3dd-fb165f1a8630
0b69f616-5c75-4c34-b97a-ae05564812af
0c631fa9-58cb-4d77-a7e0-fc77e5b3f93f
0f3b6070-57ce-4642-b9ec-3b3956f75978
11b2d312-9a7e-4a4e-814f-ed0384ed9d4d
13446299-79d8-497c-ba83-673c176a4637
15d4e6f4-b2ba-44c7-8c0e-03c141280f9b
15fd322f-7e9e-48c0-a970-f36335eb622a
163d631a-6528-4324-b7b3-6487d24feeb5
1820cf6b-c8a4-411c-894c-31195b9ff7a8
18b8879c-f211-43b8-9908-cf65e509b21d
18c3f6d0-5bb1-45bb-9f94-ab0e7812218d
1966e052-ebc6-4f4b-b7f9-6d1c6cb4b445
1f9394fb-6435-4928-9a03-2b258e5a28c5
22bcae27-254b-47b2-acda-87467dab060c
22e518ee-81b8-4081-ae1b-f0d7a777a1d7
235066f5-307a-4285-a882-14bc2d06cb7b
27c99b10-c57e-4599-a23a-f7b1a54c17a1
2c2a6595-b208-446e-bbd1-d0f49eca45e8
2f51f17f-f47c-49d5-958f-cafecd3fe01e
2fd56aa5-7b9b-40b0-9470-05c74b032d55
31f26a6e-65f5-480d-be32-36b9f425b3dd
34e1d4be-3708-4065-ae77-eca21f86e857
3d5618a0-4e3a-45bb-943d-a72c753fb7da
3de141c0-089b-4ceb-8a2e-bd6d83044a5f
42059fde-f06f-4e2c-9a23-8292d887fb6e
482522d1-31f1-43eb-ae9c-a681336404f7
48ec07ab-ec9d-4297-a7bf-d84974667e61
49721012-99c1-4d9c-967a-eee4
… [14170 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/sessions.py --status 2>&1 | head -80", "description": "Run sessions status tool"}`

  ```
sessions · plans de mandat
    0b0a6a0d-05f5-4308 · terminé  · 1859 min · N2.h — corpus propre, porte honnête, généralité, verrou de longueur
      → close — N2.i (3,13 / 12,93 / 33,83) et Pensée v0 (6/6 portes) sont committés.
    0b69f616-5c75-4c34 · terminé  · 3933 min · R0.4, R0.5, R13, R4.1–R4.3, en-cours, roadmap, backlog
      → clôture reprise par la session `22e518ee` — commit, archives, état.
    22e518ee-81b8-4081 · terminé  · 3104 min · archives de sessions, journal, en-cours, roadmap, backlog, outillage d'archivage
      → clôture committée (`eff8d8e4`) — session close ; la suite est **N2** (la hiérarchie), portée par la session à ouvrir
    71d57f53-8b41-4220 · terminé  · 4437 min · docs/pilotage/en-cours.md, docs/methode/continuite.md, tools/sessions.py, journal/sessions/README.md, journal/sessions/_modele/plan.md, tools/porte-sessions.sh
      → aucune — coordination close ; les trois plans migrés et les sessions archivées par `22e518ee`.
    8156fdcb-5033-4ba4 · terminé  · 4441 min · R0.1–R0.5
      → la boucle de lecture (R11, dépend de N2) ou la restitution (R31, dépend de R21) — toutes deux hors R0 ; sinon consolidation.
    N2-GPU             · terminé  · 4469 
… [1079 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vais lire la roadmap, les chantiers et le backlog, puis confronter aux outils.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
1: # La roadmap de [Drave](../theorie/glossaire/entrees/drave.md) — un seul plan, quatre chantiers
2: 
3: > **Un seul document de plan.** Le **moteur** (A), l'**intelligence** (B), le **natif** (N) et le **lecteur** (R).
4: > L'ordre se décide par la **valeur** et les **dépendances**, jamais par une date. Les chiffres, les séries et les
5: > contrôles vivent dans [`reports/`](../../reports/) ; ici : l'[état](../theorie/glossaire/entrees/etat.md), la prochaine action, et ce qui bloque.
6: >
7: > **Détail et histoire** : l'ancien plan [A/B](../theorie/glossaire/entrees/a-b.md) est archivé dans
8: > [`roadmap-detail-2026-10-29.md`](../archive/roadmap-detail-2026-10-29.md), le détail N dans
9: > [`roadmap-native-2026-10-29.md`](../archive/roadmap-native-2026-10-29.md). Les **fiches de fonctionnalité** sont
10: > dans [`backlog/index.md`](backlog/index.md) ; le **graphe des dépendances** est dans
11: > [`backlog/dependances.md`](backlog/dependances.md). La **page vivante** est [`en-cours.md`](en-cours.md).
12: 
13: ## Comment lire cette roadmap
14: 
15: - **Les états** : ✅ m
… [40804 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l docs/pilotage/*.md docs/pilotage/backlog/*.md journal/sessions/README.md journal/sessions/MANIFEST.md 2>/dev/null", "description": "Word counts of pilotage docs"}`

  ```
241 docs/pilotage/chantiers.md
   144 docs/pilotage/en-cours.md
   107 docs/pilotage/manques.md
   160 docs/pilotage/plan-travail.md
   345 docs/pilotage/programme-r.md
    64 docs/pilotage/README.md
   177 docs/pilotage/references-non-regression.md
   366 docs/pilotage/roadmap.md
   217 docs/pilotage/utilisation.md
    63 docs/pilotage/backlog/A2.6-ordonnanceur.md
    45 docs/pilotage/backlog/A3.2-granularite.md
    47 docs/pilotage/backlog/A3.3-seuil.md
    31 docs/pilotage/backlog/A3.4-colab.md
    31 docs/pilotage/backlog/A5.4-fpga.md
    31 docs/pilotage/backlog/A6.2-moe-local.md
    57 docs/pilotage/backlog/A8.0-portes-ppl.md
    60 docs/pilotage/backlog/A8.3-defaut.md
   115 docs/pilotage/backlog/B10.2bis-decodeur-attention-croisee.md
    32 docs/pilotage/backlog/B10.3-raisonnement-z.md
    31 docs/pilotage/backlog/B11.10-cartes-ambiguites.md
    32 docs/pilotage/backlog/B12.10-pipeline-m1-m4-m8.md
    31 docs/pilotage/backlog/B1.5-prose-scientifique.md
   244 docs/pilotage/backlog/dependances.md
   134 docs/pilotage/backlog/index.md
    67 docs/pilotage/backlog/_modele.md
    33 docs/pilotage/backlog/N0.3b-parite-ppl.md
    43 docs/pilotage/backlog/N2-distillation.md
    93
… [1243 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lance les vérificateurs du pilotage pour objectiver les écarts.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for t in tools/verifie_en_cours.py tools/verifie_backlog.py tools/revue_documentation.py; do echo \"===== $t\"; timeout 300 python3 \"$t\" 2>&1 | tail -40; echo \"[exit $?]\"; done", "description": "Run state and doc checkers", "time … [15 caractères tronqués]`

  ```
===== tools/verifie_en_cours.py
  en-cours · 1622 mots · 7 sections · 2 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
[exit 0]
===== tools/verifie_backlog.py
=== GRAPHE DU BACKLOG ===
  fiches 37 · lignes sans fiche 1 · arêtes dures 43 · plafonds 3
  profondeur 5 : R01 → R02 → R03 → R31 → R32 → R51
  frontière (4) : A2.6, N2, N3, N4

✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.
[exit 0]
===== tools/revue_documentation.py
  revue de documentation · 550 fiche(s) · 636 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
[exit 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/ | head -60 && echo \"--- portes\" && ls tools/porte-*.sh | wc -l && echo \"--- registre\" && ls -la work/ 2>/dev/null | head", "description": "List tools and gate scripts"}`

  ```
adaptateur_langue.py
aiguille.py
aligneur_litteraire.py
amplification.py
analyse_alignement.py
analyse_empreinte.py
analyse_engram.py
analyse_experts_statique.py
analyse_flux.py
analyse_hc.py
analyse_litteraire.py
analyse_octets_par_jeton.py
analyse_reutilisation_experts.py
analyse_union_experts.py
ancre_professeur.py
applique_pont.py
approximabilite_bloc.py
apres-telechargement-k3.sh
archive_sessions.py
audit_drapeaux_harnais.py
banc_complet.py
banc_durci.py
banc-experts.py
banc_lecteur.py
banc_lecture.py
banc-prelire.py
blanchiment_entree.py
bloc_code.py
bloc_linguistique.py
bloc_maths.py
bloc_tableaux.py
boucle-cerveau.sh
boucle_directe.py
bruit_entree.py
budget_execution_locale.py
c4_retard.sh
c8_carte_profondeur.sh
c8_corpus.sh
c8_entrainer_tete.py
c8_sonde_lineaire.py
cache_pont.py
calibre_modes.py
calibrer.py
campagne-benefices.sh
campagne_synthese.py
canal_structure.py
cancellation_langue.py
carte_chantiers.py
carte_coupe.sh
carte_decisions.py
carte-facultes.sh
carte-fenetre-puits.sh
carte_langues.py
carte_latence.sh
carte-sortie-profondeur.sh
catalogue_corpus.py
cca_raisonnement.py
census_routage.py
cerveau
chat.py
--- portes
81
--- registre
total 24
drwxr-xr-x. 1 stephane
… [560 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Les vérificateurs passent ; je cherche maintenant les écarts réels (git, mandats, manifest).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== HEAD ==\" && git log -1 --format='%h %ci %s' && echo \"== status ==\" && git status --short | head -30 && echo \"== count ==\" && git status --short | wc -l && echo \"== last 10 commit dates ==\" && git log -10 --format='%c … [91 caractères tronqués]`

  ```
== HEAD ==
139a8b16 2026-11-02 14:37:11 -0500 B13 — LES ABSENTS : 0, LES QUATRE ÉTAIENT DES FAUX (TOKENISATION) ; 139/139
== status ==
 M docs/README.md
 M docs/implantation/bloc-linguistique.md
 M docs/implantation/format-flux.md
 M docs/implantation/moteur-de-pensee.md
 M docs/methode/contexte.md
 M docs/methode/portes.md
 M docs/methode/resultats.md
 M docs/pilotage/en-cours.md
 M docs/theorie/carte.md
 M docs/theorie/glossaire.md
 M docs/theorie/glossaire/README.md
 M docs/theorie/glossaire/index.json
 M docs/theorie/lecture-rapide.md
 M docs/theorie/vision.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/b6a672ec-3349-4a4c-9e23-4478aa823170/digest.md
 M journal/sessions/b6a672ec-3349-4a4c-9e23-4478aa823170/rapport.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M reports/README.md
 M reports/corpus-genres.json
 M reports/native-generation.json
 M reports/rapport-genres.md
 M reports/rapport-ocr-pdf.md
 M tools/distiller_budget.py
 M tools/docwatch
 M tools/generer_natif.py
 M tools/glossaire_cartes.py
 M tools/ocr_pdf.py
== count ==
67
== last 10 commit dates =
… [999 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/MANIFEST.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/MANIFEST.md</path>
<type>file</type>
<content>
1: # Sessions DSH archivées
2: 
3: Régénéré par `tools/archive_sessions.py`. Le digest est versionnable ; la
4: trace brute (`session*.jsonl.zstd`) reste sur disque et n'est pas suivie par git.
5: 
6: | Session | Début | Trace | Digest | Tours | Messages | Outils | Erreurs | Compactages |
7: |---|---|---|---|---|---|---|---|---|
8: | `00221850` | 2026-10-27 11:34 | 2.6 Mo | 558 Ko | 6 | 469 | 529 | 7 | 0 |
9: | `04ed1834` | 2026-10-08 09:18 | 0.3 Mo | 67 Ko | 1 | 27 | 42 | 0 | 0 |
10: | `0b0a6a0d` | 2026-10-31 17:17 | 6.4 Mo | 1148 Ko | 20 | 1709 | 1565 | 5 | 4 |
11: | `0b2c86eb` | 2026-10-27 10:29 | 0.9 Mo | 148 Ko | 1 | 123 | 128 | 0 | 0 |
12: | `0b69f616` | 2026-10-30 21:46 | 0.8 Mo | 197 Ko | 1 | 180 | 200 | 0 | 0 |
13: | `0c631fa9` | 2026-10-27 14:55 | 0.2 Mo | 33 Ko | 1 | 16 | 15 | 0 | 0 |
14: | `0f3b6070` | 2026-10-31 18:02 | 0.0 Mo | 12 Ko | 1 | 4 | 0 | 0 | 0 |
15: | `11b2d312` | 2026-10-01 02:50 | 0.5 Mo | 82 Ko | 1 | 42 | 60 | 0 | 0 |
16: | `13446299` | 2026-10-01 00:54 | 0.5 Mo | 84 Ko | 1 | 50 | 68 | 0 | 0 |
17: | `15d4e6f4` | 2026-10-22 08:28 | 0.1 Mo |
… [7986 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je creuse les mandats, les plans et l'historique d'archivage.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== README sessions ==\" && cat journal/sessions/README.md && echo && echo \"== archive.log tail ==\" && tail -20 journal/sessions/archive.log && echo && echo \"== registre ==\" && ls -la journal/registre.txt work/registre.txt  … [168 caractères tronqués]`

  ```
== README sessions ==
# Sessions — plans vivants et archives

Deux choses différentes vivent ici :

- **`<id>/plan.md`** — le **mandat vivant** d'une session active : périmètre, fichiers réservés,
  heartbeat, prochaine action, état. Il s'écrit **avant** de modifier `docs/pilotage/en-cours.md`
  et se consulte avec `python3 tools/sessions.py --status`.
- **`<id>/rapport.md`** et **`<id>/digest.md`** — l'**archive** d'une session terminée, générée
  par `tools/session_report.py` / `tools/archive_sessions.py` ; les deux outils lisent
  `session.jsonl.zstd` **et** `session.v4.jsonl.zstd` (les traces récentes).
- **`<id>/cloture.md`** — la **clôture écrite à la main** quand le rapport automatique ne dit pas
  ce qui est livré et ce qui reste (`c3d0f0bd`, `f0969e87`) ; `N2-GPU` n'a pas de trace DSH et son
  rapport est écrit à la main.

Un plan n'est pas un état : `en-cours` reste la seule source de l'état. Un plan périmé (heartbeat
> 45 min) est signalé ; une session qui reprend un périmètre périmé le rafraîchit d'abord.

Modèle : [`_modele/plan.md`](_modele/plan.md). Vérification : `python3 tools/sessions.py --check`.

Migration douce : `python3 tools/sessions.py --depuis-en-cours` cr
… [284 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/sessions.py | head -80 && echo \"...\" && grep -n \"mandat\\|heartbeat\\|périmé\\|perime\" tools/sessions.py | head -30", "description": "Inspect sessions.py mandate logic"}`

  ```
#!/usr/bin/env python3
"""sessions.py — plans de session : qui fait quoi, avant d'écrire `en-cours`.

Chaque session active expose son mandat dans `journal/sessions/<id>/plan.md` :
périmètre, fichiers réservés, heartbeat, prochaine action, état. Les autres
sessions consultent `--status` avant de claim, et `--check` refuse les mandats
incomplets, les identifiants dupliqués, les périmètres qui se recouvrent et
les heartbeats périmés. `en-cours` reste la seule source de l'état : ce plan
est le **contrat de travail** qui le précède.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
SESSIONS = "journal/sessions"
ETAT = "docs/pilotage/en-cours.md"
CHAMPS = ("session", "rôle", "périmètre", "fichiers réservés", "heartbeat",
          "prochaine action", "état")
ACTIFS = {"actif", "active", "en cours", "bloqué", "bloquee", "bloqué(e)"}
A_CONFIRMER = {"à confirmer", "a confirmer"}
ETATS_CONNUS = ACTIFS | {"terminé", "termine", "libre", "libre."} | A_CONFIRMER
PEREMPTION_MIN = 45


def _cle(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lowe
… [3729 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je contrôle les mandats actifs et leur cohérence avec l'état.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/sessions.py --check; echo \"[exit $?]\"; echo \"== archive.log ==\"; ls -l journal/sessions/archive.log; echo \"== plans mtimes ==\"; ls -l journal/sessions/*/plan.md | tail -10; echo \"== digests mtimes récents ==\"; l … [111 caractères tronqués]`

  ```
⚠ mandat périmé (464 min) : e181ce02-cd50-488a-a6be-e84b79d40dcc — heartbeat à rafraîchir
  ⚠ mandat périmé (1004 min) : fe3c05f0-834b-44f2-8739-501865d652c1 — heartbeat à rafraîchir
[exit 0]
== archive.log ==
-rw-r--r--. 1 stephane stephane 0 27 sep 11:17 journal/sessions/archive.log
== plans mtimes ==
-rw-------. 1 stephane stephane 1667  1 nov 08:33 journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md
-rw-------. 1 stephane stephane  910 31 oct 11:21 journal/sessions/0b69f616-5c75-4c34-b97a-ae05564812af/plan.md
-rw-------. 1 stephane stephane 1008 31 oct 11:41 journal/sessions/22e518ee-81b8-4081-ae1b-f0d7a777a1d7/plan.md
-rw-r--r--. 1 stephane stephane  925 31 oct 11:21 journal/sessions/71d57f53-8b41-4220-84dd-7bb9eedc88d9/plan.md
-rw-r--r--. 1 stephane stephane  626 31 oct 11:21 journal/sessions/8156fdcb-5033-4ba4-a5f3-f8a078e6e57e/plan.md
-rw-r--r--. 1 stephane stephane  651 31 oct 11:21 journal/sessions/c3d0f0bd-e344-4600-a023-0ed50d25b48b/plan.md
-rw-------. 1 stephane stephane 4828  2 nov 07:32 journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
-rw-r--r--. 1 stephane stephane 2836  1 nov 22:47 journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md
… [1168 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md</path>
<type>file</type>
<content>
1: # Plan de session — Pensée, la RSN plurielle et le moteur N3
2: 
3: > **Mandat vivant.** Ouvert le 2026-10-31 22 h 45 HAE depuis
4: > [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md). Ce plan est le **contrat de
5: > synergie** : il dit ce que la session réserve, ce qu'elle attend des autres, et quand elle s'arrête.
6: > Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.
7: 
8: - **Session** : `e181ce02-cd50-488a-a6be-e84b79d40dcc`
9: - **Rôle** : Pensée — RSN plurielle, arbre d'états, cycle multi-niveaux, moteur N3 ; analyse de la couche heuristique ; bloc linguistique
10: - **Périmètre** : Pensée, R4.4-reste, Coloration, Bloc linguistique (R0.7)
11: - **Fichiers réservés** : `docs/theorie/pensee-iterative.md`, `docs/schemas/pensee-*.svg`,
12:   `docs/implantation/moteur-de-pensee.md`, `tools/pensee/`, `reports/pensee-*`,
13:   `reports/r44-*`, `docs/theorie/pre-traitement-linguistique.md`,
14:   `docs/schemas/heuristique-*.svg`, `tools/bloc_linguistique.py`,
15:   `tools/porte-bloc-linguistique.
… [3932 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie la fraîcheur réelle des traces et la porte des sessions.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== porte-sessions ==\" && cat tools/porte-sessions.sh && echo && echo \"== traces actives ==\" && ls -l journal/sessions/e181ce02-*/ journal/sessions/fe3c05f0-*/ | grep -E 'session|digest|rapport' && echo \"== dates dans diges … [160 caractères tronqués]`

  ```
== porte-sessions ==
#!/bin/bash
# porte-sessions.sh — les plans de session sont lisibles et le linter refuse un doublon.
set -u
cd "$(dirname "$0")/.."
python3 tools/sessions.py --autotest || exit 1
python3 tools/sessions.py --check || exit 1
python3 tools/sessions.py --status | grep -q '71d57f53' || {
    echo "  ❌ le plan de la session de coordination n'est pas lisible"; exit 1; }
echo "PORTE TENUE : plan lisible · autotest doublon/champ manquant · check en-cours"

== traces actives ==
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/:
-rw-r--r--. 1 stephane stephane  2046666  2 nov 15:17 digest.md
-rw-r--r--. 1 stephane stephane   567408  2 nov 15:18 rapport.md
-rw-------. 1 stephane stephane 12011245  2 nov 14:40 session.v4.jsonl.zstd
journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/:
-rw-r--r--. 1 stephane stephane  2474971  2 nov 15:17 digest.md
-rw-r--r--. 1 stephane stephane   763951  2 nov 15:18 rapport.md
-rw-------. 1 stephane stephane 13568675  2 nov 13:25 session.v4.jsonl.zstd
== dates dans digest e181 (fin) ==

  ```
ok
432 phrases réelles → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel.json
absents []
classes {'liens': 
… [1156 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md</path>
<type>file</type>
<content>
1: # Plan de session — D/R/A : les données, le lecteur, le moteur
2: 
3: > **Mandat ouvert** le 2026-11-01 16 h 25 HNE depuis
4: > [`docs/pilotage/plan-travail.md`](../../../docs/pilotage/plan-travail.md) (§ 2, § 3) — la session
5: > reprend la session `fe3c05f0` (R4.4 close) pour le rôle **D/R/A**. Le heartbeat est celui de
6: > l'état.
7: 
8: - **Session** : `fe3c05f0-834b-44f2-8739-501865d652c1`
9: - **Rôle** : **D/R/A — les données, le lecteur, le moteur** : le texte intégral, l'extraction
10:   PDF/OCR, la préparation de R1.1/R1.2, A2.6/A8.3.
11: - **Périmètre** : D (texte intégral, PDF/OCR, licences, stubs), R1.1/R1.2 (préparation), A2.6/A8.3
12: - **Fichiers réservés** : `data/wikipedia/` (lecture), `data/corpus_wiki_*`,
13:   `tools/corpus_wikipedia*.py`, `tools/verifie_contamination.py`, `tools/catalogue_corpus.py`,
14:   `reports/corpus-wiki-*`, `reports/corpus-wikipedia-*`, `reports/inventaire-*`,
15:   `reports/rapport-corpus-*`, `reports/r11-*`, `reports/r12-*`, `reports/a26-*`, `reports/a83-*`,
16:   `journal/sessions/f
… [1963 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je mesure le delta non committé et je lis le plan multi-sessions.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== diffstat ==\" && git diff --stat | tail -15 && echo && echo \"== en-cours diff ==\" && git diff docs/pilotage/en-cours.md | head -80 && echo && echo \"== mtimes modifiés (top 12) ==\" && git status --porcelain | awk '{print … [110 caractères tronqués]`

  ```
== diffstat ==
 .../rapport.md                                     |  61 ++++-
 reports/README.md                                  |   2 +-
 reports/corpus-genres.json                         |  22 +-
 reports/native-generation.json                     |  16 +-
 reports/rapport-genres.md                          |   8 +-
 reports/rapport-ocr-pdf.md                         |  40 ++-
 tools/distiller_budget.py                          |  29 +-
 tools/docwatch                                     |   2 +-
 tools/generer_natif.py                             |   9 +-
 tools/glossaire_cartes.py                          |   3 +-
 tools/ocr_pdf.py                                   |  12 +-
 tools/pensee/autotest.py                           |  13 +-
 tools/tests/linguistique/gold_reel.json            | 296 +++++++++++++++++++++
 tools/tests/linguistique/gold_reel.py              |  15 ++
 33 files changed, 1030 insertions(+), 224 deletions(-)

== en-cours diff ==
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 93908075..10083ce2 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-02, 15 h 0
… [3069 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/plan-travail.md</path>
<type>file</type>
<content>
1: # Le plan de travail — plusieurs sessions sur une même machine
2: 
3: > **Ce que ce document est.** Le **pont** entre l'état ([`en-cours.md`](en-cours.md), ce qui se
4: > passe maintenant) et l'ordre ([`roadmap.md`](roadmap.md), ce qu'il faut faire et dans quel
5: > ordre) : **qui fait quoi, dans quel territoire, à quelle cadence, et comment on surveille les
6: > fichiers qui bougent**. Il ne remplace ni l'un ni l'autre : l'état reste la source du présent,
7: > la roadmap la source de l'ordre.
8: >
9: > **Date** : 2026-11-01. **Machine** : une seule — 40 cœurs, 125 Go de RAM, 2 GPU de 16 Go,
10: > 2,0 To libres sur `Data13TB`, 34 Go sur `IA`. **Capacité** : voir
11: > [`chantiers.md`](chantiers.md) § 8 (4 sessions, 4 à 6 chantiers, 2 à 4 sous-agents par session).
12: >
13: > **Chargement** : ce document avant d'ouvrir une session ; puis la fiche du chantier.
14: 
15: ## 1. Où ce plan se situe
16: 
17: ```
18: en-cours.md          ce qui se passe maintenant (état court, une section par session active)
19: plan-travail.md      qui fait quoi, où, à quelle cadence (
… [12175 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lance la surveillance des fichiers en mouvement et les contrôles de clôture.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for t in tools/surveille_sessions.py tools/verifie_etat_a_jour.py tools/taille_documents.py tools/verifie_journal.py; do echo \"===== $t\"; timeout 120 python3 \"$t\" 2>&1 | tail -30; echo \"[exit ${PIPESTATUS[0]}]\"; done", "descrip … [84 caractères tronqués]`

  ```
===== tools/surveille_sessions.py
surveille-sessions · 2 session(s) active(s) · 67 fichier(s) en mouvement
  e181ce02-cd50-488a · actif   · 465 min · 15 réservation(s)
  fe3c05f0-834b-44f2 · en cours · 1005 min · 14 réservation(s)
  e181ce02-cd50-488a · 7 fichier(s) : docs/implantation/bloc-linguistique.md, docs/implantation/moteur-de-pensee.md, tools/pensee/autotest.py, tools/tests/linguistique/gold_reel.json, tools/tests/linguistique/gold_reel.py, reports/pensee-partielle.json …
  fe3c05f0-834b-44f2 · 3 fichier(s) : reports/corpus-wiki-big-propre.json, reports/corpus-wiki-it-texte-contamination.json, reports/corpus-wiki-it-texte.json
  hub (partagé)      · 3 fichier(s) : docs/README.md, docs/pilotage/en-cours.md, tools/docwatch

  orphelins (54) — à attribuer, commiter ou supprimer :
    · docs/implantation/format-flux.md
    · docs/methode/contexte.md
    · docs/methode/portes.md
    · docs/methode/resultats.md
    · docs/theorie/carte.md
    · docs/theorie/glossaire.md
    · docs/theorie/glossaire/13-le-corpus-et-la-mesure-documentaire.md
    · docs/theorie/glossaire/README.md
    · docs/theorie/glossaire/entrees/blake2b.md
    · docs/theorie/glossaire/entrees/catalogue.md
    
… [2587 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/chantiers.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/chantiers.md</path>
<type>file</type>
<content>
1: # Les chantiers — la vision à jour et leurs relations
2: 
3: > **Ce que ce document est.** La **vue d'ensemble des chantiers** : ce que les demandes des
4: > 48 dernières heures ont déplacé, l'inventaire élargi (A, B, N, R, **S**, **L**, **D**, B13),
5: > leurs **relations** (ce que chacun attend et ce qu'il fournit) et les **tensions** à trancher.
6: > Il ne remplace ni la [roadmap](roadmap.md) (l'ordre et les états), ni l'[en-cours](en-cours.md)
7: > (l'état courant), ni le [backlog](backlog/index.md) (les contrats par fonctionnalité) : il dit
8: > **comment les morceaux tiennent ensemble**.
9: >
10: > **Date** : 2026-11-01. **Méthode** : relecture des messages humains des sessions des 48 h
11: > (`0b69f616`, `22e518ee`, `0b0a6a0d`, `fe3c05f0`, `e181ce02`, les sessions de QA visuelle),
12: > des plans et rapports de session, et des documents de vision, roadmap, programme R et backlog.
13: >
14: > **Chargement** : ce document (une fois), puis la roadmap pour l'ordre. Ne pas charger le
15: > backlog entier.
16: 
17: ## 1. Ce que les 48 heures ont demandé
18: 
19: L
… [23021 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie les manques déjà connus, les rouges tolérées et le journal du jour.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/manques.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/manques.md</path>
<type>file</type>
<content>
1: # Registre des manques
2: 
3: > **Dernière vérification : 2026-10-27.**
4: 
5: > **Résumé —** Le registre des manques mesurés (M1–M9, N1–N5, architecture) ; chaque ligne porte la
6: > mesure qui l'établit et ce qu'elle bloque. **Chargement :** document daté ; **ne pas charger par
7: > défaut**. Lire ce résumé, puis la section utile.
8: 
9: > **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
10: > **feuille de route courante** est [`roadmap.md`](roadmap.md) ; l'**état** est
11: > [`en-cours.md`](en-cours.md).
12: 
13: > 9 octobre 2026 (**dernière vérification : 2026-10-27**). Ce que le dépôt **ne sait pas faire**,
14: > consigné comme manque — pas comme résultat. Chaque ligne porte la mesure qui l'établit, ce
15: > qu'elle bloque, et où c'est documenté. Rien ici n'est une feuille de route : la feuille de route
16: > courante est [`roadmap.md`](roadmap.md) ; le plan d'origine est archivé
17: > (`docs/archive/plan-cerveau-complet.md`).
18: 
19: ---
20: 
21: ## 1. Les manques du MOTEUR
22: 
23: | # | manque | ce qui l'établit
… [11356 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== status complet ==\" && git status --short && echo && echo \"== journal 02/11 ==\" && ls journal/2026-11-02/ && sed -n '1,60p' journal/2026-11-02/README.md", "description": "Full git status and today's journal"}`

  ```
== status complet ==
 M docs/README.md
 M docs/implantation/bloc-linguistique.md
 M docs/implantation/format-flux.md
 M docs/implantation/moteur-de-pensee.md
 M docs/methode/contexte.md
 M docs/methode/portes.md
 M docs/methode/resultats.md
 M docs/pilotage/en-cours.md
 M docs/theorie/carte.md
 M docs/theorie/glossaire.md
 M docs/theorie/glossaire/README.md
 M docs/theorie/glossaire/index.json
 M docs/theorie/lecture-rapide.md
 M docs/theorie/vision.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/b6a672ec-3349-4a4c-9e23-4478aa823170/digest.md
 M journal/sessions/b6a672ec-3349-4a4c-9e23-4478aa823170/rapport.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M reports/README.md
 M reports/corpus-genres.json
 M reports/native-generation.json
 M reports/rapport-genres.md
 M reports/rapport-ocr-pdf.md
 M tools/distiller_budget.py
 M tools/docwatch
 M tools/generer_natif.py
 M tools/glossaire_cartes.py
 M tools/ocr_pdf.py
 M tools/pensee/autotest.py
 M tools/tests/linguistique/gold_reel.json
 M tools/tests/linguistique/gold_reel.py
?? docs/theorie/glossaire/13-le-corpus-et-
… [5924 caractères tronqués]
  ```

### 🤖 Assistant

⏵ J'identifie les écrivains réels d'aujourd'hui et l'état des portes.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== traces modifiées aujourd'hui ==\" && find journal/sessions -name 'session*.zstd' -newermt '2026-11-02 00:00' -printf '%TH:%TM %10s %p\\n' | sort && echo && echo \"== rapports/digests après 12h ==\" && find journal/sessions  … [183 caractères tronqués]`

  ```
== traces modifiées aujourd'hui ==
13:25   13568675 journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/session.v4.jsonl.zstd
13:37    6447568 journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/session.v4.jsonl.zstd
14:40   12011245 journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/session.v4.jsonl.zstd
14:41     278139 journal/sessions/b6a672ec-3349-4a4c-9e23-4478aa823170/session.v4.jsonl.zstd

== rapports/digests après 12h ==
15:17 journal/sessions/00221850-90de-4287-90ee-324a35e504cd/digest.md
15:17 journal/sessions/00221850-90de-4287-90ee-324a35e504cd/rapport.md
15:17 journal/sessions/04ed1834-b0f8-42a1-aa21-75a75c19647e/digest.md
15:17 journal/sessions/04ed1834-b0f8-42a1-aa21-75a75c19647e/rapport.md
15:17 journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md
15:17 journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/rapport.md
15:17 journal/sessions/0b2c86eb-7a8d-4eed-a3dd-fb165f1a8630/digest.md
15:17 journal/sessions/0b2c86eb-7a8d-4eed-a3dd-fb165f1a8630/rapport.md
15:17 journal/sessions/0b69f616-5c75-4c34-b97a-ae05564812af/digest.md
15:17 journal/sessions/0b69f616-5c75-4c34-b97a-ae05564812af/rapport.md
15:17 journal/sessions/0c631fa9-58cb-4d77-a7e0-fc77e5b
… [728 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md", "limit": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/references-non-regression.md</path>
<type>file</type>
<content>
1: # Références de non-régression
2: 
3: > **Dernière passe complète — 2026-11-01 à 00 h 56 :** **80 portes, 76 vertes, 4 rouges, 1 h 46**
4: > (journaux `/tmp/portes-1101-n2h`). Mêmes rouges que la passe du 31/10 : `porte-indice` (921 s),
5: > `porte-melange` (112 s), `porte-homeostasie` (environnementale) et `porte-reparti-moteur`.
6: > Aucune régression ; `porte-vision` et `porte-ocr-scans` sont vertes.
7: 
8: > **Passe précédente — 2026-10-31 à 19 h 42 :** **79 portes, 75 vertes, 4 rouges, 1 h 39**
9: > (journaux `/tmp/portes-1031-n2d`) : mêmes rouges ; `porte-ocr` (48 s) était verte.
10: 
11: > **Passe précédente — 2026-10-31 à 12 h 54 :** **78 portes, 73 vertes, 5 rouges, 1 h 37**
12: > (journaux `/tmp/portes-1031-11h17`). `porte-indice`, `porte-melange` : les **structurelles
13: > connues**. `porte-homeostasie` (exit 2) : **environnementale** — `/tmp/n4/rang4-lora.pt` effacé
14: > au démarrage. `porte-jeux` : **vraie régression** corrigée le jour même (`2edb3079` — le SAN
15: > perdait contre la case, 110/112). `porte-reparti-moteur` : PPL éping
… [4806 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je date la scène et je lis la fin des traces des sessions non déclarées.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date && stat -c '%y %n' docs/pilotage/en-cours.md journal/sessions/e181ce02-*/session.v4.jsonl.zstd journal/sessions/fe3c05f0-*/session.v4.jsonl.zstd && echo && echo \"===== 0b0a6a0d (plan=terminé) digest tail =====\" && tail -c 2500 … [122 caractères tronqués]`

  ```
lun 02 nov 2026 15:35:39 EST
2026-11-02 14:40:02.182407666 -0500 docs/pilotage/en-cours.md
2026-11-02 14:40:07.862722665 -0500 journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/session.v4.jsonl.zstd
2026-11-02 13:25:52.218863691 -0500 journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/session.v4.jsonl.zstd

===== 0b0a6a0d (plan=terminé) digest tail =====

**N2.ac — le mélange prend le meilleur des deux.** 1,02 Go (les deux corpus concaténés), 60 000 pas : **3,4902** en domaine (à 0,05 du meilleur), **6,0283** en littérature (le meilleur), **8,3352** en anglais (≈ le big), **9,0525** sur wikitext2 (le meilleur). C'est le **modèle de production** pour R — la largeur sans perdre le français.

## Les fichiers

- Fiches : [`rapport-n2-corpus-1go.md`](reports/rapport-n2-corpus-1go.md), [`rapport-n2-pas-vs-texte.md`](reports/rapport-n2-pas-vs-texte.md), [`rapport-n2-melange.md`](reports/rapport-n2-melange.md).
- Corpus : `data/wiki_big/propre/` (831 Mo) et `data/wiki_mix/propre/` (1,02 Go), manifeste [`corpus-wiki-big-propre.json`](reports/corpus-wiki-big-propre.json).
- Modèles : `work/n2w/{fr-60k,big-60k,mix-60k}.pt` ; outils : `work/n2w/{deduit_leger,pipeline_big,eval_croise,eva
… [752 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"===== b6a672ec digest (head) =====\" && head -c 1800 journal/sessions/b6a672ec-*/digest.md | tr -d '\\000' && echo && echo \"===== b6a672ec digest (tail) =====\" && tail -c 1800 journal/sessions/b6a672ec-*/digest.md | tr -d '\ … [65 caractères tronqués]`

  ```
===== b6a672ec digest (head) =====
# Session DSH — relecture

- identifiant : `b6a672ec-3349-4a4c-9e23-4478aa823170`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-01 13:28:57
- agent : standard


## Tour 1

### 👤 Utilisateur

git push origin

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

## 1. La vi
… [2386 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie l'état GPU et les collisions de commits signalées par N2.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== nvidia-smi ==\" && timeout 20 nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv 2>&1; echo \"[exit $?]\"; echo; echo \"== derniers processus dsh/python ==\" && ps -eo pid,etime,pcpu,pme … [162 caractères tronqués]`

  ```
== nvidia-smi ==
index, name, memory.used [MiB], memory.total [MiB], utilization.gpu [%]
0, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %
1, Quadro RTX 5000, 1 MiB, 16384 MiB, 0 %
[exit 0]

== derniers processus dsh/python ==
   7293       02:58  118  0.5 node-MainThread node /home/stephane/.local/share/../bin/dsh --profile dsh-tui
   3209       28:40  1.5  0.0 docwatch        /home/stephane/.local/share/pipx/venvs/docwatch/bin/python -E /home/stephane/.local/bin/docwatch --config /home/stephane/.config/docwatch/config.toml --no-browser
   2948       28:46  0.4  0.1 node-MainThread node /home/stephane/.local/bin/dsh web --no-open
   2238       28:50  0.0  0.0 fail2ban-server /usr/bin/python3.13 /usr/bin/fail2ban-server -xf start
   2061       28:52  0.0  0.0 firewalld       /usr/bin/python3.13 /usr/sbin/firewalld --nofork --nopid
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== commits aujourd'hui ==\" && git log --since='2026-11-02 00:00' --oneline | wc -l && echo \"== collisions ==\" && for c in edb54a29 26e4df27 b788ba04 26b8c442; do echo \"--- $c\"; git show --stat --oneline $c | head -12; don … [73 caractères tronqués]`

  ```
== commits aujourd'hui ==
149
== collisions ==
--- edb54a29
edb54a29 B13 — LES PRONOMS OBJETS : 8/8, 20/20 AU TOTAL, GOLD 336 ; 98/98
 docs/implantation/moteur-de-pensee.md              |   5 +-
 docs/pilotage/chantiers.md                         |   2 +-
 docs/pilotage/en-cours.md                          |   2 +-
 docs/pilotage/roadmap.md                           |   4 +-
 journal/2026-11-02/README.md                       |   9 +-
 journal/2026-11-02/apprentissage.md                |   4 +-
 journal/2026-11-02/attention.md                    |   4 +-
 journal/2026-11-02/distribue.md                    |   7 +-
 journal/2026-11-02/docs.md                         |   4 +-
 journal/2026-11-02/memoire.md                      |   4 +-
 journal/2026-11-02/mesures.md                      |   4 +-
--- 26e4df27
26e4df27 B13 — LES QUESTIONS PIÈGES : 29/34, LE SI EST UNE CONVENTION ; 132/132
 docs/implantation/moteur-de-pensee.md              |   5 +-
 docs/pilotage/en-cours.md                          |   6 +-
 docs/theorie/synthese/index.md                     |  40 +--
 journal/2026-11-02/README.md                       |  11 +-
 journal/2026-11-02/apprentissage.md                |   6
… [1912 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je confirme le redémarrage, puis je mesure la dérive documentaire.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== uptime ==\" && uptime -s && uptime && echo && echo \"== en-cours : GPU/reboot/N2.ac ==\" && grep -n -i 'gpu\\|redémar\\|reboot\\|N2.ac\\|mélange 1' docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/plan-trava … [250 caractères tronqués]`

  ```
== uptime ==
[stderr]
uptime: invalid option -- 's'
Try 'uptime --help' for more information.
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib\nrows=[]\nfor line in pathlib.Path('journal/sessions/MANIFEST.md').read_text().splitlines():\n    m=re.match(r'\\|\\s*`([0-9a-f]{8})`\\s*\\|\\s*([^|]+)\\|\\s*([^|]+)\\|\\s*([^|]+)\\|\\s*(\\d+)\\s* … [1286 caractères tronqués]`

  ```
sessions: 110
tours total: 1791 | messages: 39978 | outils: 37327
0 tour: ['163d631a', '1f9394fb', '7557cea8']
1 tour: 89 | 2-10: 5 | >10: 13

Top 12 (tours):
  fe3c05f0   390 tours   2426 msgs  2026-10-31 17:35  trace 13.6 Mo
  d629d7d7   286 tours   4096 msgs  2026-10-19 12:03  trace 20.0 Mo
  bbd6969f   205 tours   9630 msgs  2026-09-28 14:46  trace 56.9 Mo
  fc167f70   187 tours   2792 msgs  2026-10-14 13:07  trace 13.7 Mo
  f0969e87   172 tours   3959 msgs  2026-10-25 21:28  trace 16.6 Mo
  e181ce02   155 tours   1820 msgs  2026-10-31 17:40  trace 12.0 Mo
  d31b3d9b   104 tours   3396 msgs  2026-10-08 09:11  trace 25.1 Mo
  71d57f53    55 tours   1174 msgs  2026-10-29 07:42  trace 7.5 Mo
  22bcae27    54 tours   1250 msgs  2026-09-25 11:56  trace 14.8 Mo
  8156fdcb    23 tours    750 msgs  2026-10-29 08:40  trace 4.5 Mo
  0b0a6a0d    20 tours   1709 msgs  2026-10-31 17:17  trace 6.4 Mo
  bc3c0b97    15 tours    478 msgs  2026-10-27 08:56  trace 4.2 Mo

Top 10 (trace):
  bbd6969f   56.9 Mo  205 tours
  d31b3d9b   25.1 Mo  104 tours
  d629d7d7   20.0 Mo  286 tours
  f0969e87   16.6 Mo  172 tours
  22bcae27   14.8 Mo  54 tours
  fc167f70   13.7 Mo  187 tours
  fe3c05f0   13.6 Mo 
… [160 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie l'heure du redémarrage et les livrables non committés de la dernière session.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== boot ==\" && (who -b 2>/dev/null; cat /proc/uptime) && python3 - <<'PY'\nimport time\nup=float(open('/proc/uptime').read().split()[0]); print('uptime', round(up/60,1), 'min → boot', time.strftime('%Y-%m-%d %H:%M:%S', time.l … [340 caractères tronqués]`

  ```
== boot ==
         system boot  2026-11-02 15:06
1780.11 69247.91
uptime 29.7 min → boot 2026-11-02 15:06:42

== rapport-pensee-vrais-absents (non committé) ==
# B13 — les vrais absents : 5 phrases sans antécédent, 0 lien

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **140/140 portes** : cinq phrases à **pronom sans antécédent** (`Il pleut.`, `On dit que c'est
> vrai.`, `Elle est partie.`, `Ils sont arrivés.`, `It rains.`) entrent dans le gold
> (**432 phrases réelles**). Elles ne produisent **aucun lien** : le `coref` du gold n'est pas
> renseigné pour elles, et `resoudre_meta` ne les voit pas. Le **vrai** absent n'est pas mesuré —
> il est **absent du gold**.
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-vrais-absents.json`](pensee-vrais-absents.json).

## 1. Les 5 phrases

| phrase | pronom | antécédent | **lien produit** |
|---|---|---|---|
| `Il pleut.` | il | aucun | **non** |
| `On dit que c'est vrai.` | on | aucun | **non** |
| `Elle est partie.` | elle | aucun | 
… [1174 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== fe3c05f0 digest tail ==\" && tail -c 2200 journal/sessions/fe3c05f0-*/digest.md | tr -d '\\000' | tail -20 && echo && echo \"== e181ce02 rapport head ==\" && sed -n '1,40p' journal/sessions/e181ce02-*/rapport.md", "descript … [47 caractères tronqués]`

  ```
== fe3c05f0 digest tail ==

- `pipx install --editable …/tools/docwatch` : le serveur tourne désormais **depuis le dépôt**, version **0.6.0** (plus de réinstallation à chaque modification).
- CSS durci : `text-decoration: underline dotted **currentColor**`, **`text-decoration-thickness: 1.5px`**, offset 2,5 px. Survol : fond jaune pâle et trait plein.
- Serveur arrêté puis relancé : PID **3573290**, port **8771**, `HTTP 200`.

## Les preuves

- `GET /render?mount=drave&path=docs/pilotage/plan-travail.md` → **23 spans `class="glossaire"`**.
- **Chrome headless, DOM réel de ta page** (`/drave/docs/pilotage/plan-travail.md`) → **19 spans `class="glossaire"`** rendus par le JS, donc la page elle-même les affiche.
- La page shell sert bien le CSS : `grep "1.5px"` → **3 occurrences** (la règle glossaire est dans le `<style>` inline).
- Capture écrite : `/tmp/docwatch-plan.png` (223 Ko). Je ne peux pas la lire moi-même (le modèle courant n'accepte pas les images) — **ouvre-la**, ou recharge ton onglet avec `Ctrl+Shift+R`.

## Si ce n'est toujours pas visible chez toi

Deux choses à vérifier de ton côté :
- que l'onglet pointe bien sur **`/drave/...`** (le montage `drave`), et pas sur une 
… [3772 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je mesure la fraîcheur de chaque document de pilotage et ce que le dernier commit d'état a réellement changé.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/chantiers.md docs/pilotage/plan-travail.md docs/pilotage/manques.md docs/pilotage/references-non-regression.md docs/pilotage/backlog/index.md docs/pilotage/bac … [383 caractères tronqués]`

  ```
docs/pilotage/en-cours.md                        2026-11-02 14:37:11 -0500 139a8b16
docs/pilotage/roadmap.md                         2026-11-02 13:33:07 -0500 6e6e9f61
docs/pilotage/chantiers.md                       2026-11-02 11:27:29 -0500 7e1b15de
docs/pilotage/plan-travail.md                    2026-11-02 11:27:29 -0500 7e1b15de
docs/pilotage/manques.md                         2026-10-28 09:21:57 -0400 4035fe3d
docs/pilotage/references-non-regression.md       2026-11-01 02:45:47 -0500 585d5a09
docs/pilotage/backlog/index.md                   2026-10-31 18:09:15 -0400 09fff61b
docs/pilotage/backlog/dependances.md             2026-10-31 12:51:30 -0400 90ae6b39
AGENTS.md                                        2026-10-29 16:02:45 -0400 727d13e0

== show 6e6e9f61 (état/roadmap) ==
6e6e9f61 ÉTAT ET ROADMAP — LE MÉLANGE 1 Go EST LE MODÈLE DE PRODUCTION
 docs/pilotage/en-cours.md                          |  8 ++++----
 docs/pilotage/roadmap.md                           |  2 +-
 journal/2026-11-02/README.md                       |  7 ++++---
 journal/2026-11-02/apprentissage.md                |  2 +-
 journal/2026-11-02/attention.md                    |  2 +-
 journal/2026-11-02/distri
… [4119 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== N2.ac dans les docs de pilotage ==\" && grep -c 'N2\\.ac' docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/plan-travail.md docs/pilotage/chantiers.md; echo && echo \"== B10.2bis dans index ==\" && grep -n 'B … [316 caractères tronqués]`

  ```
== N2.ac dans les docs de pilotage ==
docs/pilotage/en-cours.md:1
docs/pilotage/roadmap.md:1
docs/pilotage/plan-travail.md:0
docs/pilotage/chantiers.md:0

== B10.2bis dans index ==
docs/pilotage/backlog/index.md:81:| B10.2bis | [Décodeur à attention croisée](B10.2bis-decodeur-attention-croisee.md) | mesurée | P2 | — | B10.2bis |
docs/pilotage/backlog/index.md:82:| B10.3 | [Raisonnement sur `z` gelé](B10.3-raisonnement-z.md) | bloquée | P2 | B10.2bis | B10.3 |
docs/pilotage/backlog/dependances.md:77:| **B10.2bis** | mesurée | — | B10.2 négatif (chrF **12,7 / 5,3** contre un plancher **39,6**) | B10.3 | [B10.2bis-decodeur-attention-croisee.md](B10.2bis-decodeur-attention-croisee.md) |
docs/pilotage/backlog/dependances.md:78:| **B10.3** | bloquée | B10.2bis (dure) | B10.2bis négatif (chrF 11.2 / 16.4 contre 39,6) | R52 | [B10.3-raisonnement-z.md](B10.3-raisonnement-z.md) |
docs/pilotage/backlog/dependances.md:130:   est nommé `B10.2bis`, depuis mesuré (fiche du 31/10) : le trou nommé est comblé.
docs/pilotage/backlog/dependances.md:158:négatif de B10.2bis, R44 par l'OCR) en sont exclues par leur statut.
docs/pilotage/backlog/dependances.md:206:| **P3** | `R43`, `R44`, `R51`, `R52`, `B
… [274 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie la composition des 81 portes et la frontière du backlog.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== toutes-les-portes (tête) ==\" && sed -n '1,60p' tools/toutes-les-portes.sh && echo && echo \"== portes par famille ==\" && ls tools/porte-*.sh | sed 's#tools/porte-##; s#\\.sh##' | awk -F- '{print $1}' | sort | uniq -c | so … [64 caractères tronqués]`

  ```
== toutes-les-portes (tête) ==
#!/bin/bash
# toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait.
#
# POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS
# (`--attn-window` en réparti) que le v7 avait **délibérément retiré** en faisant voyager les
# trois réglages dans la trame (`main.rs:4432`). La porte ne pouvait donc plus passer — et
# personne ne l'a vu, parce que les portes étaient lancées **une par une**, à la main, quand
# on touchait la fonctionnalité du jour. Une porte qu'on croit verte et qui n'a pas tourné est
# exactement le défaut que ce dépôt traque (un drapeau inerte, une mesure qui ne mesure rien) :
# ici, appliqué aux instruments eux-mêmes.
#
# Ce que fait ce script, et ce qu'aucun autre ne faisait :
#   1. il lance **TOUTES** les `tools/porte-*.sh`, séquentiellement ;
#   2. il ne s'arrête PAS à la première rouge — il veut le tableau, pas la première tuile ;
#   3. il borne chaque porte dans le temps (`DELAI`, 1800 s par défaut) : une porte qui pend
#      est une porte ROUGE, pas une porte qu'on attend ;
#   4. il garde le journal de chacune (`JOURNAUX`) et n'affiche qu'une ligne par porte ;
#   5. il sort en 
… [2521 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/index.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/index.md</path>
<type>file</type>
<content>
1: # Le backlog des fonctionnalités — index
2: 
3: > **Ce que ce dossier est.** Une **fiche par fonctionnalité** à documenter et à implémenter : le programme
4: > **R (le lecteur)** et les lignes ouvertes des programmes A, B et N. Une fiche n'est **pas** un résultat :
5: > elle porte le besoin, le contrat, la porte, les contrôles négatifs et ce qui pourrait la rendre fausse. Le
6: > résultat, quand il existe, vit dans `reports/`.
7: >
8: > **La roadmap** est [`../roadmap.md`](../roadmap.md) ; l'**analyse** qui a ouvert le programme R est
9: > [`../../theorie/lecture-rapide.md`](../../theorie/lecture-rapide.md) ; l'**état courant** est
10: > [`../en-cours.md`](../en-cours.md). **Chargement** : une fiche à la fois, jamais le dossier entier. **37 fiches** : 20 pour R, 17 pour les lignes
11: > ouvertes A/B/N ; le **graphe** des dépendances est dans [`dependances.md`](dependances.md).
12: 
13: ## Comment utiliser une fiche
14: 
15: 1. **Lire le besoin et le contrat** — c'est ce qui dit si la fonctionnalité est prête à être codée.
16: 2. **Vérifier la porte et les contr
… [8239 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je confronte le processus à ses propres règles de continuité.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/continuite.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/continuite.md</path>
<type>file</type>
<content>
1: # Continuité — cycles longs, sous-agents, état unique
2: 
3: > **Objet.** Comment un travail continue : cycles DSH, sous-agents, discipline de
4: > [`en-cours`](../pilotage/en-cours.md). Ni planning ni résultats : **qui écrit l'état, quand, et avec quoi on reprend**.
5: >
6: > **Règle d'or.** Un cycle est fini quand le résultat est **mesuré, écrit, committé**, qu'`en-cours` porte sa
7: > **prochaine action**, et que la roadmap est à jour.
8: 
9: ## 1. Les cycles DSH
10: 
11: | réglage | valeur | pourquoi |
12: |---|---|---|
13: | `max_goal_rounds` | **1 000** (ou le maximum du harnais) | la limite est un **filet**, pas un objectif : on ne s'arrête pas à 20 ou 50 rounds |
14: | goal | **un par programme** (N, B, docs) | recréer un goal à chaque tâche casse la continuité et l'historique |
15: | reprise | `update_goal resume` | on reprend le **même** goal, on n'en ouvre pas un nouveau |
16: | fin de cycle | résultat + fiche + commit + `en-cours` + roadmap | jamais « le temps est écoulé » |
17: 
18: - **Un cycle = un sous-chantier**, pas un round : plusieurs heures et 
… [6760 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '145,200p' tools/sessions.py && echo \"== autotest ==\" && grep -n 'autotest\\|--check\\|erreurs\\|avertissements' tools/sessions.py | head -30", "description": "Inspect session checker exit logic"}`

  ```
def verifier(racine: Path, strict: bool = False) -> tuple[list[str], list[str]]:
    erreurs: list[str] = []
    avertissements: list[str] = []
    plans = decouvrir(racine)
    actifs = [p for p in plans if p["etat"] in ACTIFS]
    vus: dict[str, str] = {}
    for p in plans:
        manquants = [c for c in CHAMPS if c not in p["champs"]]
        if manquants:
            erreurs.append(f"{p['chemin']} : champ(s) manquant(s) — {', '.join(manquants)}")
        if p["etat"] not in ETATS_CONNUS:
            erreurs.append(f"{p['chemin']} : état inconnu {p['etat']!r}")
        if p["etat"] in A_CONFIRMER:
            (erreurs if strict else avertissements).append(
                f"plan à confirmer : {p['id']} — la session doit le compléter")
        if p["age"] is None:
            erreurs.append(f"{p['chemin']} : heartbeat illisible")
        if p["id"] in vus:
            erreurs.append(f"id dupliqué : {p['id']} ({vus[p['id']]} et {p['chemin']})")
        vus[p["id"]] = str(p["chemin"])
    for i, a in enumerate(actifs):
        if a["age"] is not None and a["age"] > PEREMPTION_MIN:
            msg = f"mandat périmé ({a['age']:.0f} min) : {a['id']} — heartbeat à rafraîchir"
       
… [3075 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je teste le mode strict et la trace de la dernière passe de portes.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== --check --strict ==\" && python3 tools/sessions.py --check --strict; echo \"[exit $?]\"; echo; echo \"== portes.md ==\" && sed -n '1,50p' journal/2026-11-02/portes.md", "description": "Run strict session check and read gate … [10 caractères tronqués]`

  ```
== --check --strict ==
  ❌ mandat périmé (467 min) : e181ce02-cd50-488a-a6be-e84b79d40dcc — heartbeat à rafraîchir
  ❌ mandat périmé (1007 min) : fe3c05f0-834b-44f2-8739-501865d652c1 — heartbeat à rafraîchir
[exit 1]

== portes.md ==
# 2026-11-02 — Portes et vérifications

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (7)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 00:26 | `9b4f0208` | PLAN — LA LIGNE D/R/A PORTE SES LIVRAISONS : DIX CORPUS FAITS, PDF/OCR, PRÉPA R1 | `plan-travail.md`, `README.md`, `apprentissage.md` (+12) |
| 00:34 | `93be0a1d` | CHANTIERS — LA LIGNE D PORTE LES DIX CORPUS, LE PDF, LES DOCUMENTS ET L'OCR | `chantiers.md`, `README.md`, `mesures.md` (+5) |
| 00:55 | `2bf24422` | ÉTAT — PASSE COMPLÈTE DES PORTES DU 02/11 00 h 03 : 77 VERTES, 4 ROUGES (LES CONNUES) | `en-cours.md`, `README.md`, `apprentissage.md` (+15) |
| 02:23 | `58f47624` | B13 — LA VÉRITÉ QUI CHANGE : PORTE CACHÉE, 
… [2186 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib\nrows=[]\nfor line in pathlib.Path('journal/sessions/MANIFEST.md').read_text().splitlines():\n    m=re.match(r'\\|\\s*`([0-9a-f]{8})`\\s*\\|\\s*([^|]+)\\|\\s*([^|]+)\\|\\s*([^|]+)\\|\\s*(\\d+)\\s* … [549 caractères tronqués]`

  ```
fe3c05f0 | 390 tours | 2026-10-31 17:35 | Lecture de en-cours.md et choix de tâche
d629d7d7 | 286 tours | 2026-10-19 12:03 | Continue the work
bbd6969f | 205 tours | 2026-09-28 14:46 | Continue avec REPRISE.md
fc167f70 | 187 tours | 2026-10-14 13:07 | Projet Drave continuer
f0969e87 | 172 tours | 2026-10-25 21:28 | Optimiser couches linguistiques jeux symboliques
e181ce02 | 155 tours | 2026-10-31 17:40 | Documentation Drave avec diagrammes et implémentation
d31b3d9b | 104 tours | 2026-10-08 09:11 | Où en est-on
71d57f53 |  55 tours | 2026-10-29 07:42 | Évaluation des techniques de lecture rapide pour Drave
22bcae27 |  54 tours | 2026-09-25 11:56 | Étude de Qtrinet-bootstrap.md
8156fdcb |  23 tours | 2026-10-29 08:40 | Réviser roadmap et backlog, établir priorités
0b0a6a0d |  20 tours | 2026-10-31 17:17 | Continue session work
bc3c0b97 |  15 tours | 2026-10-27 08:56 | Cohérence de la documentation et recommandations
4f3e8570 |  13 tours | 2026-10-12 15:30 | Configuration RAID0 NVMe pour modèles IA
cf0456ab |   8 tours | 2026-10-29 15:51 | Mécanisme de mise à jour pair douteux
00221850 |   6 tours | 2026-10-27 11:34 | Outillage de présentation de documentation
c3d0f0bd |   5 tours | 
… [188 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie les preuves de portes et la cohérence numérique de l'état.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== journaux de portes /tmp ==\" && ls -d /tmp/portes-* 2>/dev/null | tail -5; for d in $(ls -d /tmp/portes-* 2>/dev/null | tail -2); do echo \"--- $d\"; ls \"$d\" | wc -l; ls \"$d\" | head -3; cat \"$d/registre.txt\" 2>/dev/nu … [169 caractères tronqués]`

  ```
== journaux de portes /tmp ==

== mtimes journal 02/11 ==
-rw-------. 1 stephane stephane 19601  2 nov 14:38 journal/2026-11-02/README.md
-rw-r--r--. 1 stephane stephane  3222  2 nov 14:38 journal/2026-11-02/portes.md
-rw-r--r--. 1 stephane stephane  1853  2 nov 14:38 journal/2026-11-02/outils.md
-rw-r--r--. 1 stephane stephane  3190  2 nov 14:38 journal/2026-11-02/modele.md
-rw-r--r--. 1 stephane stephane 22102  2 nov 14:38 journal/2026-11-02/mesures.md
-rw-r--r--. 1 stephane stephane  4451  2 nov 14:38 journal/2026-11-02/memoire.md
-rw-r--r--. 1 stephane stephane  4579  2 nov 14:38 journal/2026-11-02/docs.md
-rw-r--r--. 1 stephane stephane  5208  2 nov 14:38 journal/2026-11-02/distribue.md
-rw-r--r--. 1 stephane stephane  3402  2 nov 14:38 journal/2026-11-02/attention.md
-rw-r--r--. 1 stephane stephane  3013  2 nov 14:38 journal/2026-11-02/apprentissage.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== chiffres B13 dans en-cours ==\" && grep -n -o '[0-9]\\+/[0-9]\\+ *portes\\|gold [0-9]\\+\\|coréférence [0-9]\\+/[0-9]\\+' docs/pilotage/en-cours.md && echo && echo \"== ligne la plus longue roadmap/chantiers ==\" && awk '{p … [445 caractères tronqués]`

  ```
== chiffres B13 dans en-cours ==
21:6/6 portes
45:gold 407
80:111/111 portes
121:gold 342
121:coréférence 27/30

== ligne la plus longue roadmap/chantiers ==
3163 183
2363 31
1845 164
1901 90
549 88
430 89

== commits par session (rapports) ==
e181ce02 | Commits | 195 |
fe3c05f0 | Commits | 99 |
0b0a6a0d | Commits | 88 |
71d57f53 | Commits | 98 |
8156fdcb | Commits | 40 |
c3d0f0bd | Commits | 32 |
  ```

### 🤖 Assistant

⏵ Je vérifie les livrables en attente (OCR, S) et la concentration des commits.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== total commits ==\" && git rev-list --count HEAD && echo \"== sous-modules ==\" && cat .gitmodules && git submodule status 2>&1 | head; echo && echo \"== OCR CEGEP (non committé) ==\" && sed -n '1,25p' reports/rapport-ocr-ce … [69 caractères tronqués]`

  ```
== total commits ==
2379
== sous-modules ==
[submodule "tools/docwatch"]
	path = tools/docwatch
	url = https://github.com/stephanedenis/docwatch.git
[submodule "tools/structures"]
	path = tools/structures
	url = /home/stephane/Data13TB/stephane/GitHub/drave-structures
+676e14429780560def8f38ac21da168dd4a02852 tools/docwatch (v0.4.1-2-g676e144)
 3b68143f3e805372c0fe2fcdbc2f574b95c7e9d3 tools/structures (heads/fusion)

== OCR CEGEP (non committé) ==
# Le corpus OCR du CEGEP — 10 notes scannées, 2 519 507 caractères

**Date** : 2026-11-02 (pilote de 05 h 52 à 11 h 25) · **Ligne** : Données · **Session** : fe3c05f0
**Statut** : **pilote clos** — 10 scans océrisés, manifeste `reports/ocr-pdf-cegep.json` ; le fonds CEGEP compte 2 681 PDF, la détection n'en a examiné que 41 avant la coupure `--max-doc 5`.

## 1. Ce que c'est

Le corpus OCR des **notes de cours du CEGEP** : les PDF sans couche texte du fonds `archives/CEGEP`, océrisés page à page par `tesseract`. C'est le complément CEGEP du corpus OCR des livres (`reports/rapport-ocr-pdf.md`).

## 2. Le chiffre

| grandeur | valeur |
|---|---:|
| scans océrisés | **10** |
| PDF examinés / scannés | 41 / 5 |
| pages | **1596** |
| caractèr
… [385 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== dernier rapport B13 committé ==\" && sed -n '1,15p' reports/rapport-pensee-absents.md && echo && echo \"== en-cours lignes 40-46 ==\" && sed -n '40,46p' docs/pilotage/en-cours.md && echo && echo \"== en-cours lignes 118-124 … [123 caractères tronqués]`

  ```
== dernier rapport B13 committé ==
# B13 — les absents : 0, les quatre étaient des faux

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-02 · **Verdict** : ✅
> **139/139 portes** : les **4 liens « absents »** du round précédent sont **0** après correction
> de la tokenisation : les mots étaient collés à la ponctuation (`dog;`, `letter;`), et le test
> les croyait hors du texte. Il n'y a **aucun antécédent absent** dans les 116 liens. La
> coréférence est **entièrement** résolue par la règle (51 intra + 65 inter).
>
> **Dispositif** : [`miroir.py`](../tools/tests/linguistique/miroir.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-absents.json`](pensee-absents.json).

## 1. Les classes corrigées

| classe | avant | **après** |
|---|---:|---:|

== en-cours lignes 40-46 ==
- **Prochaine action** : **L** — l'**annotation de l'absence** (T137 : 5 phrases sans antécédent, 0 lien ; `sans_antecedent`) ;
  **B13** — DRVM/native **bloqué**, la cascade mesurée reste la lecture.
- **Bloquants** : **neuronal réel bloqué** — `llama-cli` refuse/timeout, aucun tagger (`spacy`,
  `stanza`, `nltk`, `transformers`), aucun poids `drave-n0` ; le mock 
… [947 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je termine par les hooks, le mandat N2 clos et le récit du redémarrage.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== plan 0b0a6a0d (N2) ==\" && sed -n '1,40p' journal/sessions/0b0a6a0d-*/plan.md && echo && echo \"== hooks ==\" && ls -l .git/hooks/pre-commit .git/hooks/pre-commit.sample 2>/dev/null; head -20 .git/hooks/pre-commit 2>/dev/nu … [55 caractères tronqués]`

  ```
== plan 0b0a6a0d (N2) ==
# Plan de session — N2.h, le mètre propre

> **Mandat ouvert** le 2026-10-31 22 h 30 HAE depuis [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md)
> — mandat libre de 10 h (nuit du 31/10 au 1/11). Le heartbeat est celui de l'état.

- **Session** : `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2`
- **Rôle** : calcul : distillation ; corpus ; évaluation
- **Périmètre** : N2.h — corpus propre, porte honnête, généralité, verrou de longueur
- **Fichiers réservés** : `data/`, `tools/corpus*`, `tools/eval_n2_propre.py`,
  `tools/distiller_budget.py`, `reports/n2-*`, `work/n2h/`,
  `journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/`
- **Heartbeat** : 2026-11-01 08:35 EST
- **Objectif final** : un **mètre honnête** pour N2 — corpus dédupliqué (0 % de fenêtres de
  validation dans l'entraînement), chaîne refaite dessus, porte < 2,5 redéfinie — puis trancher
  ce que les chiffres contaminés ne pouvaient pas trancher : la **généralité hors dépôt** et le
  **verrou de longueur**.
- **Résultat** : corpus 4,63 → 3,61 Mo (−22,2 %), **0 / 2 814** fenêtres de validation dans
  l'entraînement (contre 32,8 %) ; chaîne propre **3,09** en domaine, **16,70** sur la litt
… [1488 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== GPU/reboot dans le journal du jour ==\" && grep -ril 'gpu\\|redémarr\\|reboot' journal/2026-11-02/ | head; echo \"(fin)\"; echo && echo \"== rapports non suivis vs index ==\" && for f in rapport-ocr-cegep rapport-pensee-par … [373 caractères tronqués]`

  ```
== GPU/reboot dans le journal du jour ==
(fin)

== rapports non suivis vs index ==
rapport-ocr-cegep                0
rapport-pensee-partielle         0
rapport-pensee-vrais-absents     1

== docwatch submodule ==
diff --git a/tools/docwatch b/tools/docwatch
index 95e94c47..676e1442 160000
--- a/tools/docwatch
+++ b/tools/docwatch
@@ -1 +1 @@
-Subproject commit 95e94c47007672e4a64e6a4952944e071f92ef94
+Subproject commit 676e14429780560def8f38ac21da168dd4a02852-dirty

== docs/pilotage/README ==
# Le dossier pilotage — carte et ordre de lecture

> **Ce que ce dossier est.** Le **pilotage** du projet : l'état courant, l'ordre des chantiers,
> le plan de travail multi-sessions, les relations entre chantiers, les contrats du backlog, les
> manques et les références de non-régression. **Ce n'est pas** la documentation de conception
> (celle-ci est dans `docs/theorie/`, `docs/implantation/`, `docs/methode/`) ni les résultats
> (`reports/`) ni le récit (`journal/`).
>
> **Machine** : une seule ; plusieurs sessions travaillent en parallèle sur le même arbre de
> travail. Les territoires et la surveillance sont dans [`plan-travail.md`](plan-travail.md).

## L'ordre de lecture

| ordre | docu
… [3352 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie si la revue documentaire voit les fiches non indexées.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== index reports ==\" && grep -n 'ocr-cegep\\|pensee-partielle\\|pensee-vrais-absents' reports/README.md; echo; echo \"== comptes HEAD vs disque ==\" && echo -n 'md HEAD: ' && git ls-tree -r HEAD --name-only reports | grep -c  … [383 caractères tronqués]`

  ```
== index reports ==
18:| [`rapport-pensee-vrais-absents.md`](rapport-pensee-vrais-absents.md) | **B13** — les vrais absents : 5 phrases, 0 lien, **140/140** |

== comptes HEAD vs disque ==
md HEAD: 717
md disque: 550
json HEAD: 627
json disque: 636

== règle classement ==
5:  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
11:  5. cohérence  : la synthèse (index.md) liste les huit chapitres, le chapitre 7 et B10–B12 ;
68:            if "archive" not in p.parts and p.name != "README.md" and not est_carte(p)]
82:            + [RACINE / "docs/README.md", RACINE / "README.md",
89:            + [RACINE / "README.md", RACINE / "REPRISE.md", RACINE / "AGENTS.md"])
97:               RACINE / "README.md", RACINE / "REPRISE.md", RACINE / "AGENTS.md"])
160:    # 1. classement : aucune donnée de résultat dans docs/
163:            if f.name == "index.json" and f.parent.name == "glossaire":
165:            alertes.append(f"classement : donnée de résultat dans docs/ → {f.relative_to(RACINE)}")
168:            alertes.append(f"classement : la fiche courante reports/{nom} manque")
169:    if not (RACINE / "reports/README.md").exists():
170:        alertes.ap
… [1108 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je date la pile de travail non committée, fichier par fichier.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== mtimes des 67 fichiers en mouvement (par minute) ==\" && git status --porcelain | awk '{print $2}' | while read f; do stat -c '%y' \"$f\" 2>/dev/null; done | cut -c12-16 | sort | uniq -c | sort -k2 && echo && echo \"== HEAD … [247 caractères tronqués]`

  ```
== mtimes des 67 fichiers en mouvement (par minute) ==
      2 04:04
      1 05:08
      1 05:09
      1 05:10
      1 05:15
      1 05:16
      1 09:54
      1 10:16
      1 11:26
      1 11:36
      1 12:07
     24 12:44
      9 12:53
      1 13:37
      2 14:39
      6 14:40
      4 15:17
      2 15:18
      1 19:09
      1 19:15
      1 19:52
      1 19:56
      1 20:10
      2 23:14

== HEAD 139a8b16 : fichiers ==
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 125 ++++++++++
 .../rapport.md                                     |  67 +++++-
 reports/README.md                                  |   2 +-
 reports/pensee-absents.json                        |  20 ++
 reports/rapport-pensee-absents.md                  |  57 +++++
 tools/pensee/autotest.py                           |  18 +-
 tools/tests/linguistique/miroir.py                 |  17 +-
 23 files changed, 607 insertions(+), 64 deletions(-)

== nb fichiers HEAD ==
23
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== rapports imbriqués ==\" && find reports -mindepth 2 -name '*.md' | wc -l && find reports -mindepth 1 -maxdepth 1 -type d | head && echo && echo \"== liens .md dans reports/README ==\" && grep -c '](.*\\.md)' reports/README. … [134 caractères tronqués]`

  ```
== rapports imbriqués ==
170
reports/archive
reports/toutes-langues
reports/campagne-benefices
reports/07

== liens .md dans reports/README ==
141
== lignes de tableau ==
137
  ```

### 🤖 Assistant

⏵ Je sépare les dates pour dater précisément la sédimentation.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== dates des fichiers modifiés (suivis) ==\" && git status --porcelain | awk '$1==\"M\"{print $2}' | while read f; do stat -c '%y' \"$f\"; done | cut -c1-16 | sort | uniq -c && echo && echo \"== dates des fichiers non suivis = … [200 caractères tronqués]`

  ```
== dates des fichiers modifiés (suivis) ==
      1 2026-10-30 09:54
      1 2026-11-01 19:56
      1 2026-11-01 20:10
      2 2026-11-02 04:04
      1 2026-11-02 05:10
      1 2026-11-02 05:15
      1 2026-11-02 05:16
      1 2026-11-02 11:36
      4 2026-11-02 12:44
      8 2026-11-02 12:53
      2 2026-11-02 14:39
      4 2026-11-02 14:40
      4 2026-11-02 15:17
      2 2026-11-02 15:18

== dates des fichiers non suivis ==
      1 2026-11-01 19:09
      1 2026-11-01 19:15
      1 2026-11-01 19:52
      2 2026-11-01 23:14
      1 2026-11-02 05:08
      1 2026-11-02 05:09
      1 2026-11-02 10:16
      1 2026-11-02 11:26
      1 2026-11-02 12:07
     20 2026-11-02 12:44
      1 2026-11-02 12:53
      1 2026-11-02 13:37
      2 2026-11-02 14:40
  ```

### 🤖 Assistant

⏵ J'identifie les fichiers les plus anciens de la pile non committée.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain | while read st f; do d=$(stat -c '%y' \"$f\" 2>/dev/null | cut -c1-16); case \"$d\" in 2026-10-30*|2026-11-01*) echo \"$d  $st  $f\";; esac; done | sort && echo && echo \"== répartition par dossier ==\" && git … [156 caractères tronqués]`

  ```
2026-10-30 09:54  M  tools/docwatch
2026-11-01 19:09  ??  reports/corpus-wiki-it-texte.json
2026-11-01 19:15  ??  reports/corpus-wiki-it-texte-contamination.json
2026-11-01 19:52  ??  tools/extrait_pdf.py
2026-11-01 19:56  M  docs/implantation/bloc-linguistique.md
2026-11-01 20:10  M  tools/distiller_budget.py
2026-11-01 23:14  ??  reports/pensee-partielle.json
2026-11-01 23:14  ??  reports/rapport-pensee-partielle.md

== répartition par dossier ==
     26 docs/theorie
      5 journal/sessions
      3 docs/methode
      3 docs/implantation
      2 tools/tests
      1 tools/pensee
      1 tools/ocr_pdf.py
      1 tools/liens_glossaire.py
      1 tools/glossaire_cartes.py
      1 tools/generer_natif.py
      1 tools/extrait_pdf.py
      1 tools/docwatch
      1 tools/distiller_budget.py
      1 reports/README.md
      1 reports/rapport-pensee-vrais-absents.md
      1 reports/rapport-pensee-partielle.md
      1 reports/rapport-ocr-pdf.md
      1 reports/rapport-ocr-cegep.md
      1 reports/rapport-genres.md
      1 reports/pensee-vrais-absents.json
      1 reports/pensee-partielle.json
      1 reports/ocr-pdf.json
      1 reports/ocr-pdf-contamination.json
      1 reports/ocr-pdf-cege
… [342 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je confirme la dernière trace des passes de portes avant synthèse.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== commits 'portes/passe' aujourd'hui ==\" && git log --since='2026-11-02 00:00' --oneline | grep -iE 'passe|portes' | head -10 && echo && echo \"== 2bf24422 touche references ? ==\" && git show --stat --oneline 2bf24422 | gre … [346 caractères tronqués]`

  ```
== commits 'portes/passe' aujourd'hui ==
20194fb1 B13 — LE GOLD GELÉ : 602 PHRASES, 21 PORTES PROTÉGÉES ; 133/133
4f7631aa DONNÉES — LE CEGEP PASSE À 10 NOTES (2,52 M CAR.) ; LE 11E PDF (ENCYCLOPEDIA) DÉPASSE LE TIMEOUT PDFTOPPM, L'OUTIL LE RATTRAPE
4d8c9905 B13 — LA CORÉFÉRENCE À 68 LIENS : LE RÔLE PASSE DEVANT (52/51), GOLD 372 ; 111/111
65708212 DONNÉES — LE CEGEP PASSE À 7 NOTES : 739 PAGES, 1,21 M CARACTÈRES (2 ALGORITHMS ILLUMINATED AJOUTÉS)
6c7bff9b ÉTAT — PASSE COMPLÈTE DES PORTES DU 02/11 06 h : 76 VERTES, 5 ROUGES (LES 4 CONNUES + GREFFE À LA BORNE)
166896b4 GENRES — L'OCR DES 20 LIVRES PASSE À 38,5 CAR/LIGNE (6,8 % DE DOUBLONS, 14,4 M)
07e87a6f DONNÉES — L'OCR PASSE 10 M CARACTÈRES : 11 LIVRES, 4 042 PAGES, 1 244 FENÊTRES 8 KO, ÉVAL 0/40
2bf24422 ÉTAT — PASSE COMPLÈTE DES PORTES DU 02/11 00 h 03 : 77 VERTES, 4 ROUGES (LES CONNUES)

== 2bf24422 touche references ? ==
0
[exit code: 1]
  ```

### 🤖 Assistant

⏵ Je récupère les deux dernières preuves de la chaîne de portes.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== 6c7bff9b touche references ? ==\"; git show --stat --oneline 6c7bff9b | grep 'references-non-regression' || echo \"NON\"; echo; echo \"== dernier commit references ==\"; git log -1 --format='%ci %h %s' -- docs/pilotage/refe … [175 caractères tronqués]`

  ```
== 6c7bff9b touche references ? ==
NON

== dernier commit references ==
2026-11-01 02:45:47 -0500 585d5a09 N2.h — LE CORPUS PROPRE : 3,09 EN DOMAINE (PAS 2,85), 16,70 HORS DÉPÔT, ET LE VERROU DE LONGUEUR TOMBE

== fichiers 6c7bff9b ==
 journal/sessions/MANIFEST.md                       |   6 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 148 +++++++++++++++++++++
 .../rapport.md                                     |  94 ++++++++++++-
 .../fe3c05f0-834b-44f2-8739-501865d652c1/digest.md |  12 ++
 .../rapport.md                                     |  12 +-
 19 files changed, 336 insertions(+), 50 deletions(-)
  ```

### 🤖 Assistant

⏵ Je vérifie la nature de l'index `reports/README` avant de conclure.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,24p' reports/README.md && echo \"...\" && grep -n 'Ce que cet index\\|toutes les fiches\\|sélection\\|550' reports/README.md | head", "description": "Read reports index intro to check exhaustiveness"}`

  ```
# Les rapports — données intermédiaires et références

> **Ce dossier porte les résultats et les données de nos travaux**, jamais la documentation de référence
> (elle est dans [`docs/`](../docs/)). Les fiches courantes sont citées depuis le tableau de bord
> [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md).

> **Navigation** : [la carte des sujets](../docs/theorie/carte.md) · [l'état du moment](../docs/pilotage/en-cours.md) ·
> [l'inventaire des docs](../docs/README.md) · [le journal](../journal/README.md).
>
> **Contexte** : la fiche [`07-mesures-couche-commune.md`](07-mesures-couche-commune.md) est un **hub** de
> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par
> partie**, jamais en entier ; l'index exhaustif des fiches est [`INDEX.md`](INDEX.md).

## Les fiches courantes

| fichier | ce qu'il porte |
|---|---|
| [`rapport-pensee-vrais-absents.md`](rapport-pensee-vrais-absents.md) | **B13** — les vrais absents : 5 phrases, 0 lien, **140/140** |
| [`rapport-pensee-pieges.md`](rapport-pensee-pieges.md) | **B13** — les questions pièges : 29/34, le si est une convention, **132/132** |
| [`rapport-pensee-miroir.md`](rap
… [667 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je contrôle l'index exhaustif des fiches avant de retenir ce point.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== INDEX.md : nouvelles fiches ==\" && grep -n 'ocr-cegep\\|pensee-partielle\\|pensee-vrais-absents' reports/INDEX.md; echo; echo \"== INDEX taille/date ==\" && wc -l reports/INDEX.md && git log -1 --format='%ci %h' -- reports … [143 caractères tronqués]`

  ```
== INDEX.md : nouvelles fiches ==

== INDEX taille/date ==
384 reports/INDEX.md
2026-11-01 08:32:01 -0500 51c988a6

== INDEX généré ? ==
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **376 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.

| fiche | titre |
|---|---|
  ```

### 🤖 Assistant

⏵ Je mesure la couverture réelle de l'index exhaustif.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo -n 'rapport-*.md disque: '; ls reports/rapport-*.md | wc -l; echo -n 'rapport-*.md HEAD: '; git ls-tree -r HEAD --name-only reports | grep -c '/rapport-[^/]*\\.md$'; echo -n 'toutes fiches INDEX (lignes tableau): '; grep -c '^|  … [125 caractères tronqués]`

  ```
rapport-*.md disque: 537
rapport-*.md HEAD: 536
toutes fiches INDEX (lignes tableau): 376

#!/usr/bin/env python3
"""index_reports.py — génère reports/INDEX.md à partir des en-têtes de fiches.

L'index est **exhaustif** et **déterministe** : une ligne par fiche, triée par nom,
avec son titre (premier `# `). Les fichiers d'infrastructure (`README.md`, `INDEX.md`
et `historique-*`) sont exclus du tableau ; les compteurs de `docs/en-cours.md`
comptent, eux, tous les `.md` de `reports/`.
"""
from __future__ import annotations
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent


def titre(p: pathlib.Path) -> str:
    for ligne in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if ligne.startswith("# "):
            return ligne[2:].strip().replace("|", "—")
    return p.stem.replace("-", " ")


def main() -> int:
    fiches = sorted(
        p for p in (RACINE / "reports").glob("*.md")
        if p.name not in ("README.md", "INDEX.md") and not p.name.startswith("historique-")
    )
    lignes = [
        "# Index des fiches de reports/",
        "",
        f"> **Généré** par `tools/index_reports.py` — **{len(fiches)} fiches**. Les fichiers",
  
… [464 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je date la dérive de l'index exhaustif.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo -n 'top-level md HEAD: '; git ls-tree -r HEAD --name-only reports | grep -c '^reports/[^/]*\\.md$'; echo -n 'top-level md au commit INDEX (51c988a6): '; git ls-tree -r 51c988a6 --name-only reports | grep -c '^reports/[^/]*\\.md$ … [256 caractères tronqués]`

  ```
top-level md HEAD: 547
top-level md au commit INDEX (51c988a6): 379
fiches INDEX listées: 376

== INDEX modifié dans le working tree ? ==
(rien = non)
  ```

### 🤖 Assistant

⏵ Je vérifie si l'index est régénéré par un contrôle automatique.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'index_reports' tools/*.sh tools/*.py 2>/dev/null | grep -v 'def \\|__main__\\|tools/index_reports.py:' | head; echo \"---\"; grep -n 'INDEX.md' tools/revue_documentation.py | head", "description": "Check whether INDEX is re … [20 caractères tronqués]`

  ```
---
  ```

### 🤖 Assistant

⏵ Synthèse de l'audit : sessions, état réel et écarts du pilotage.

# Audit — sessions et pilotage, 2 novembre 2026 (15 h 35)

**Périmètre.** 111 sessions archivées (110 DSH + `N2-GPU`), 2 mandats actifs, 4 traces actives aujourd'hui, 9 plans, 2 clôtures manuelles. J'ai lu le manifeste et les métadonnées des 110 archives, les rapports/digests des 18 sessions de travail, les fins des 4 traces du jour, puis confronté `en-cours`, `roadmap`, `chantiers`, `plan-travail`, le backlog, `references-non-regression` aux outils, à git et aux fichiers. Les 92 micro-sessions (≤ 1 tour) n'ont été lues qu'en métadonnées.

**Verdict.** Le dépôt produit beaucoup et vite — **149 commits aujourd'hui, 2 379 au total** — mais le pilotage a décroché : **deux mandats périmés passent la porte**, **deux écrivains non déclarés** ont produit les résultats du jour, et **67 fichiers, dont le 140/140 de B13, dorment non committés** depuis jusqu'à trois jours.

## 1. Le parc : 111 sessions, 18 seulement portent du travail

| classe | nombre | ce que c'est |
|---|---:|---|
| sessions archivées | **110** (+ `N2-GPU`) | **254,3 Mo** de traces, **39 978** messages, **37 327** appels d'outils |
| sessions de travail (> 1 tour) | **18** | 13 au-delà de 10 tours, 5 entre 2 et 10 |
| micro-sessions | **92** | 89 à 1 tour, 3 vides (0 message) |
| plans de mandat | **9** | 7 clos + 2 actifs |
| clôtures écrites | **2** | `c3d0f0bd`, `f0969e87` |

Les six sessions qui portent l'essentiel :

| session | tours | commits | rôle réel |
|---|---:|---:|---|
| `fe3c05f0` | **390** | 99 | D/R/A — corpus, OCR, docwatch, glossaire |
| `e181ce02` | **155** | **195** | L/B13 — pensée, coréférence, bloc linguistique |
| `d629d7d7` | 286 | — | « Continue the work » (19/10) |
| `0b0a6a0d` | 20 | **88** | N2 — distillation, N2.ac |
| `71d57f53` | 55 | 98 | coordination, roadmap, backlog |
| `8156fdcb` | 23 | 40 | R0 — lecteur |

Les 92 micro-sessions sont du bruit d'archive : elles ne portent ni mandat ni résultat. Le manifeste ne les distingue pas, ce qui rend l'archive trois fois plus grosse qu'elle ne l'est en réalité.

## 2. Qui écrit réellement aujourd'hui

| session | plan | dernière trace | heartbeat | travail réel | prochaine action |
|---|---|---|---:|---|---|
| `e181ce02` | **actif** | 14:40 | 02/11 07:50 → **7 h 45** | B13 : **140/140** dans l'arbre, gold **432** | l'état dit « T137 à faire » — **déjà fait, non committé** |
| `fe3c05f0` | **en cours** | 13:25 | 01/11 22:50 → **16 h 45** | OCR CEGEP 10 notes, glossaire, docwatch | OCR des ~127 scans, clôture |
| `0b0a6a0d` | **terminé** | 13:37 | 01/11 08:35 | **N2.ac : 1,02 Go, 3,49 en domaine, 6,03 en littérature** ; 88 commits | 200 000 pas sur le mélange — **sans mandat** |
| `b6a672ec` | **aucun plan** | 14:41 | — | diagnostic GPU : reset logiciel impossible | reboot 15:06 ; **incident non écrit** |
| `S` | **aucune session** | — | — | sous-module `tools/structures` (`heads/fusion`) | analyseur/export, hors dispositif |
| `N2-GPU` | terminé | pas de trace | — | N2.h clos | — |

Conclusion : **2 sessions déclarées, 4 traces, 1 chantier sans session**. Le journal du jour compte d'ailleurs **4 sessions** là où `en-cours` en déclare 2.

## 3. Ce qui tient

- Les sept contrôles passent : `verifie_en_cours` (1 622 mots), `verifie_backlog` (37 fiches, 43 arêtes, 4 à la frontière), `revue_documentation` (550 fiches, 636 JSON, 119 docs, 81 portes), `taille_documents` (T0 3 996/4 000), `verifie_journal` (111 sessions, 1 802 liens), `verifie_etat_a_jour` (HEAD = état), `sessions --status`.
- Le hook `pre-commit` est installé et fonctionne : aucun fait commité après le dernier état.
- Le graphe du backlog est cohérent, les compteurs `reports/` sont exacts, la revue documentaire est verte.
- Les résultats du jour sont réels : **B13 140/140**, **N2.ac modèle de production**, **OCR CEGEP 1 596 pages**, 149 commits.

## 4. Les écarts, par gravité

**P0 — la pile non committée.** 67 fichiers : 33 modifiés, 34 non suivis. **8 sont plus vieux qu'aujourd'hui** (le plus ancien : `tools/docwatch`, 30/10 09:54), dont 20 entrées de glossaire créées à 12:44, 9 fichiers à 12:53, le rapport B13 à 14:40, les digests à 15:17. `surveille_sessions` n'en attribue que **10 sur 67** à une session ; **54 sont orphelins (80 %)**. La conséquence est concrète : l'état dit « prochaine action : T137 », alors que le résultat T137 est dans l'arbre. Un redémarrage ou un nettoyage le perd.

**P0 — les mandats périmés passent la porte.** `sessions.py --check` sort en **0** (avertissements seulement) ; `--check --strict` sort en **1** sur les deux heartbeats. Or `porte-sessions.sh` appelle le mode non strict. Le document dit que `--check` « refuse » les heartbeats périmés : c'est faux en mode porte. La porte est verte par construction — exactement la famille de défaut que `references-non-regression` raconte pour `porte-tableaux`.

**P0 — les écrivains non déclarés.** `0b0a6a0d` a un plan « terminé » et a produit **N2.ac** aujourd'hui à 13:37 ; `b6a672ec` n'a **aucun plan** et a diagnostiqué la panne GPU jusqu'à 14:41 ; `S` n'a ni session ni plan. Le journal les voit, `sessions.py` et `surveille_sessions` ne les voient pas. Il y a donc deux sources de vérité pour « qui travaille » : les traces (4) et les plans (2), sans réconciliation.

**P1 — l'état se contredit.** `en-cours` donne B13 à **111/111** (l. 80) et **123/123** (l. 45), le gold à **342** (l. 121) et **407** (l. 45), et l'arbre à **140/140** et **432**. Il dit « N2.z le meilleur » et cite N2.ac dans la même puce. Il liste `fe3c05f0` dans les **sessions archivées** (l. 48-50) **et** comme session active (l. 52). Il est horodaté 15:20, son mtime est 14:40, le dernier commit 14:37. Il ne mentionne ni la panne GPU ni le redémarrage.

**P1 — roadmap, chantiers et plan-travail sont en retard.** La roadmap affiche « dernière mise à jour : 30/10 », B13 à 111/111, N2 à 3,53 comme meilleur, et « B10.2bis absent du backlog » alors que la fiche existe et est mesurée. Ses deux cellules N2 et B13 font **3 163** et **2 363 caractères** : ce sont des journaux de portes, pas des états. `chantiers` (01/11) dit **80 portes** au lieu de 81, **11 tests** pour S au lieu de 19, coréférence **27/30**. `plan-travail` décrit **quatre sessions** alors que deux ont un plan, et donne N2 à 3,53. Ces trois fichiers ont pourtant été touchés aujourd'hui à 11:27 et 13:33 : les dates internes sont fausses.

**P1 — le registre des rouges est en retard et les preuves ont disparu.** Les passes complètes du **02/11 00:03** (77 vertes, 4 rouges) et **06:00** (76 vertes, 5 rouges) ne sont pas dans `references-non-regression`, dont la dernière entrée est le **01/11 00:56** (80/4). La **5ᵉ rouge** (`greffe` à la borne 700 s, rejouée verte à 1200 s) n'est pas listée : par la règle 3, c'est une régression. Le §1 du même fichier dit encore **49 portes** (passe du 28/10). Et les journaux de portes vivaient dans `/tmp/portes-*`, **effacés par le reboot** : il ne reste que les messages de commit.

**P1 — les collisions de commits.** Deux effacements aujourd'hui (`edb54a29`, `26e4df27`) et deux restaurations (`b788ba04`, `26b8c442`) : N2 a vu ses fiches disparaître de HEAD parce qu'un commit B13 est reparti d'un index incomplet. Le `git add` explicite évite la contamination mais **ne vérifie pas la complétude** ; le hook contrôle l'état par commit, pas la propreté de l'arbre. D'où la sédimentation du P0.

**P2 — la navigation et les finitions.** `reports/INDEX.md`, présenté comme **exhaustif**, liste **376 fiches sur 548** (il n'a pas été régénéré depuis le 01/11 08:32 ; +168 fiches depuis). `reports/README` est à **2 793/2 800 mots** (7 mots de marge). Le sous-module `docwatch` est **dirty** (`676e1442-dirty`) et non épinglé. Trois sessions vides restent dans le manifeste. La panne GPU et le reboot ne sont ni dans l'état ni dans le journal.

## 5. Ce que je ferais, dans l'ordre

1. **Committer la pile par flux**, avec l'index alterné : B13 (140/140, gold 432), D/N2 (OCR, corpus IT, glossaire), hub (état, roadmap, index). Avant : remettre `en-cours` sur les vrais chiffres, retirer la ligne « archivée » de `fe3c05f0`, ajouter N2.ac. Committer les digests régénérés à part.
2. **Réconcilier les mandats** : rafraîchir ou clore `e181ce02` et `fe3c05f0` ; ouvrir un plan N2 (200 000 pas) ou acter sa clôture ; déclarer S ; écrire une `cloture.md` pour `b6a672ec` et consigner l'incident GPU + le reboot.
3. **Réparer l'instrument** : `--strict` dans `porte-sessions.sh` ; un contrôle « sessions du journal vs sessions de l'état » ; des journaux de portes durables (hors `/tmp`) ; `references` mis à jour à chaque passe ; retirer le `grep 71d57f53` (session close) comme contrôle positif.
4. **Dégraisser la roadmap** : sortir les journaux B13/N2 vers une fiche ou le journal, garder une ligne par chantier avec sa prochaine action, corriger les dates.
5. **Puis** lancer la passe complète (≈ 1 h 46), enregistrer le verdict (81 portes, rouges listées) et committer.

## 6. Limites de l'audit

- Les 92 micro-sessions n'ont été lues qu'en métadonnées ; les 18 sessions de travail par leur rapport/digest et la fin de leur trace.
- Aucune écriture, aucun commit : je n'ai pas modifié l'état ni la roadmap.
- Les GPU sont **sains maintenant** (1 Mio utilisés sur 16 384, 0 %) : la panne décrite par `b6a672ec` a été résolue par le reboot de 15:06.
- Les preuves de portes ne sont plus lisibles que dans les messages de commit, les journaux `/tmp` ayant été effacés.
- L'horodatage « 15:20 » de `en-cours` ne correspond ni au mtime (14:40) ni au dernier commit (14:37) ; je ne l'ai pas expliqué.

Je peux enchaîner sur les points 1 et 2 — commits par flux et réconciliation des mandats — si tu veux que je le fasse maintenant.


## Tour 2

### 👤 Utilisateur

vas-y et donne moi des instructions pour que je démarre ou récupère d'autre sessions dans d'autres terminaux

### 🤖 Assistant

⏵ J'exécute la reprise : d'abord l'identité de session, le hook et les flux en attente.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== DSH env ==\" && env | grep -i '^DSH_' | sort && echo && echo \"== hook complet ==\" && cat .git/hooks/pre-commit", "description": "Inspect DSH env vars and pre-commit hook"}`

  ```
== DSH env ==
DSH_HOME=/home/stephane/.dsh
DSH_PROFILE_DIR=/home/stephane/.dsh/profiles/dsh-tui
DSH_PROFILE=dsh-tui
DSH_SESSION_ID=536cd5d6-94ac-4057-8fe9-11709a4587c7
DSH_SHELL=1

== hook complet ==
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
python3 tools/archive_sessions.py --quiet >/dev/null || { echo "  ⛔ archivage des sessions en échec"; ex
… [434 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== dsh help ==\" && timeout 20 dsh --help 2>&1 | head -60; echo \"[exit $?]\"; echo; echo \"== dsh resume help ==\" && timeout 20 dsh resume --help 2>&1 | head -30", "description": "Check DSH CLI usage for starting and resumin … [12 caractères tronqués]`

  ```
== dsh help ==
Usage: dsh [--profile] <name> [options] [app-args...]
       dsh plugin --profile <name> <pnpm-args...>

dsh: boot a DeepSeek Harness profile — an ordered stack of plugin-bundle patch
layers under your own overrides.

Arguments:
  args                           arguments for the booted profile's app (see:
                                 dsh --profile <name> --help)

Options:
  -V, --version                  output the version number
  --profile <name>               the profile under $DSH_HOME/profiles to boot
  --from-default-profile <name>  initialize a new custom profile from a shipped
                                 profile template
  --patch <path>                 extra patch-list overlay applied after the
                                 profile layer (repeatable)
  --dump-config                  print the composed profile tree and exit
  --dump-config-schema           print JSON Schema for profile entries and
                                 patches without mounting
  --dump-default-config          print the profile tree without its user layer
                                 or --patch overlays and exit

Examples:
  dsh web                                   
… [1884 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je crée le plan du hub, puis je trie les 67 fichiers par flux avant de committer.

- **todo_write** `{"todos": [{"content": "Auditer sessions, état et pilotage", "status": "completed"}, {"content": "Créer le plan de la session hub 536cd5d6", "status": "in_progress"}, {"content": "Trier les 67 fichiers en flux B13 / D / N2 / hub", "status": "pending"}, {"content": "Réécrire en-cours avec les vrais c … [473 caractères tronqués]`

  ```
Updated todo list: 7 pending, 1 in progress, 1 completed.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat journal/sessions/_modele/plan.md && echo \"== plan session hub existe ? ==\" && ls -la journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/ 2>/dev/null || echo \"absent\"", "description": "Read plan template and check hub sessi … [8 caractères tronqués]`

  ```
# Plan de session — <id>

> **Mandat vivant.** Écris ce fichier **avant** `en-cours`, mets-le à jour à chaque cycle,
> et passe `État : terminé` quand la session se retire.

- **Session** : `<id>`
- **Rôle** : <chantier / programme>
- **Périmètre** : <A8.0, R13, ...>
- **Fichiers réservés** : `tools/...`, `reports/...`
- **Heartbeat** : <AAAA-MM-JJ HH:MM HAE>
- **Prochaine action** : <une action nommée>
- **État** : actif
== plan session hub existe ? ==
absent
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md", "content": "# Plan de session — le hub, la reprise après reboot\n\n> **Mandat vivant.** Ouvert le 2026-11-02 15 h 50 HNE depuis\n> [`docs/pilotage/en-cours.md`](../../../doc … [2138 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== numstat ==\" && git diff --numstat && echo && echo \"== docs/methode ==\" && git diff -- docs/methode/contexte.md docs/methode/portes.md docs/methode/resultats.md | head -120", "description": "Inspect method docs diffs"}`

  ```
== numstat ==
20	20	docs/README.md
1	1	docs/implantation/bloc-linguistique.md
25	25	docs/implantation/format-flux.md
3	2	docs/implantation/moteur-de-pensee.md
6	6	docs/methode/contexte.md
7	7	docs/methode/portes.md
13	13	docs/methode/resultats.md
3	3	docs/pilotage/en-cours.md
10	10	docs/theorie/carte.md
3	2	docs/theorie/glossaire.md
6	3	docs/theorie/glossaire/README.md
153	1	docs/theorie/glossaire/index.json
41	41	docs/theorie/lecture-rapide.md
20	20	docs/theorie/vision.md
2	2	journal/README.md
3	3	journal/sessions/MANIFEST.md
108	0	journal/sessions/b6a672ec-3349-4a4c-9e23-4478aa823170/digest.md
19	8	journal/sessions/b6a672ec-3349-4a4c-9e23-4478aa823170/rapport.md
116	0	journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
56	5	journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
1	1	reports/README.md
11	11	reports/corpus-genres.json
8	8	reports/native-generation.json
4	4	reports/rapport-genres.md
26	14	reports/rapport-ocr-pdf.md
20	9	tools/distiller_budget.py
1	1	tools/docwatch
8	1	tools/generer_natif.py
2	1	tools/glossaire_cartes.py
11	1	tools/ocr_pdf.py
12	1	tools/pensee/autotest.py
296	0	tools/tests/linguistique/gold_reel.json
15	0	tools/tests/linguistique
… [10155 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie les diffs non évidents pour attribuer chaque fichier sans erreur.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== bloc-linguistique ==\" && git diff -- docs/implantation/bloc-linguistique.md && echo \"== moteur-de-pensee ==\" && git diff -- docs/implantation/moteur-de-pensee.md && echo \"== format-flux (début) ==\" && git diff -- docs/ … [91 caractères tronqués]`

  ```
== bloc-linguistique ==
diff --git a/docs/implantation/bloc-linguistique.md b/docs/implantation/bloc-linguistique.md
index 823c801c..dcdf12e4 100644
--- a/docs/implantation/bloc-linguistique.md
+++ b/docs/implantation/bloc-linguistique.md
@@ -242,7 +242,7 @@ Les **contrôles négatifs** : profils permutés (0,0022), texte vide, ponctuati
 inconnue (`und`), indice faux (`und`), rejeu identique.
 
 **Le gold 180** (`gold.py` 20 réels + `gold_synthetique.py` 160 synthétiques) mesure les niveaux
-profonds : POS **0,751** (fermé **0,939**, ouvert **0,621**), syntagmes exacts **0,194**,
+profonds : POS **0,765** (fermé **0,939**, ouvert **0,621**), syntagmes exacts **0,194**,
 **par tête 0,560**, acte **1,0**, négation **1,0**, modalité **0,994**, double sens **0,889** ;
 la cascade (mock de contrat) préserve ces chiffres et couvre **67,1 %** en unités sémantiques.
 Le lexique synthétique est **disjoint** des listes de l'heuristique : les classes ouvertes
== moteur-de-pensee ==
diff --git a/docs/implantation/moteur-de-pensee.md b/docs/implantation/moteur-de-pensee.md
index 36e38658..d75b0e1f 100644
--- a/docs/implantation/moteur-de-pensee.md
+++ b/docs/implantation/moteur-de-pensee.md
@@ -3
… [6542 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== tools/ocr_pdf ==\" && git diff -- tools/ocr_pdf.py && echo \"== tools/generer_natif ==\" && git diff -- tools/generer_natif.py && echo \"== tools/distiller_budget (début) ==\" && git diff -- tools/distiller_budget.py | head … [64 caractères tronqués]`

  ```
== tools/ocr_pdf ==
diff --git a/tools/ocr_pdf.py b/tools/ocr_pdf.py
index aa03d8b9..c1d01419 100644
--- a/tools/ocr_pdf.py
+++ b/tools/ocr_pdf.py
@@ -64,7 +64,11 @@ def ocr(pdf: pathlib.Path, dpi: int, langues: str, max_pages: int) -> tuple[str,
         if max_pages:
             cmd += ["-f", "1", "-l", str(max_pages)]
         cmd += [str(pdf), str(tmp / "p")]
-        subprocess.run(cmd, capture_output=True, timeout=1800)
+        try:
+            subprocess.run(cmd, capture_output=True, timeout=1800)
+        except subprocess.TimeoutExpired:
+            print(f"  ! timeout pdftoppm : {pdf.name} (ignoré)", flush=True)
+            return "", 0
         textes = []
         for png in sorted(tmp.glob("p-*.png")):
             r = subprocess.run([str(TESS), str(png), "stdout", "-l", langues, "--psm", "3"],
@@ -96,6 +100,8 @@ def troncons(t: str, taille: int):
 def main() -> int:
     ap = argparse.ArgumentParser(description=__doc__)
     ap.add_argument("--max-doc", type=int, default=0)
+    ap.add_argument("--racine", default="", help="restreindre à une racine : Biblio_large, CEGEP")
+    ap.add_argument("--deja", type=int, default=0, help="sauter les N premiers PDF examinés
… [5340 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis le contrôle d'état et le sous-module docwatch avant de toucher aux commits.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_etat_a_jour.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_etat_a_jour.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """verifie_etat_a_jour.py — aucun fait commité sans sa ligne d'état.
3: 
4: POURQUOI CET OUTIL EXISTE. `en-cours` est la seule source de l'état, et le contrat
5: disait « seul le principal écrit ». Ce n'est pas une garantie : l'identité se déduit
6: d'une variable d'environnement absente — un « pair » est autodéclaré — et si la
7: principale s'arrête, l'état se fige. Surtout, rien ne comparait les commits : la
8: revue ne regardait que la DATE, donc deux commits du même jour passaient. Le 29/10,
9: A8.0 (15 h 51) a été commité après le dernier état (15 h 34) sans aucune alerte.
10: 
11: La garantie est au commit, pas dans la discipline d'un écrivain :
12:   --index  (hook pre-commit) : un commit qui prépare un fait (reports/, roadmap,
13:            backlog) sans toucher `en-cours` est REFUSÉ ;
14:   --head   : si un fait a été commité après le dernier commit d'`en-cours`, l'état
15:            est en retard — la session qui le voit le corrige, sans attendre.
16: 
17: Le journal est du récit dérivé (le hook l'archive) : il n'exige pas de
… [8311 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== docwatch status ==\" && git -C tools/docwatch status --short | head -20 && echo \"== docwatch log ==\" && git -C tools/docwatch log --oneline -5 && echo \"== docwatch remote ==\" && git -C tools/docwatch remote -v | head -4 … [125 caractères tronqués]`

  ```
== docwatch status ==
 M README.md
 M src/docwatch/server.py
 M src/docwatch/static/tree.js
 M src/docwatch/ui.py
 M tests/test_cli.py
 M tests/test_render.py
 M tests/test_server.py
 M tests/test_spa.py
== docwatch log ==
676e144 GLOSSAIRE — LE POINTILLÉ PASSE À 1,5 PX EN currentColor (TROP DISCRET EN 1 PX GRIS)
1759b10 GLOSSAIRE — LES TERMES DU MANIFESTE SONT ANNOTÉS AU RENDU (POINTILLÉ + FICHE EN SURVOL), SANS TOUCHER AU MARKDOWN
95e94c4 VERSION 0.4.1 — CORRECTIF DE REDIRECTION DES DOSSIERS
9f735c7 URLS — REDIRECTION DES DOSSIERS SANS SLASH (/second → /second/)
dbbb05a MULTI-RACINES ET DIAGRAMMES — CONFIG.TOML, URLS /<MONTAGE>/, PLANTUML/MERMAID → <SOURCE>.SVG ; 87 TESTS
== docwatch remote ==
origin	git@github.com:stephanedenis/docwatch.git (fetch)
origin	git@github.com:stephanedenis/docwatch.git (push)

== profils dsh ==
dsh-tui
headless
node_modules
web
  ```

### 🤖 Assistant

⏵ Je prépare l'état « en pause » et la porte stricte, puis je testerai.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/sessions.py", "offset": 190, "limit": 100}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/sessions.py</path>
<type>file</type>
<content>
190:     return erreurs, avertissements
191: 
192: 
193: def afficher(racine: Path) -> int:
194:     plans = decouvrir(racine)
195:     erreurs, avertissements = verifier(racine)
196:     print("sessions · plans de mandat")
197:     if not plans:
198:         print("  (aucun plan — chaque session active doit créer journal/sessions/<id>/plan.md)")
199:     for p in plans:
200:         age = "—" if p["age"] is None else f"{p['age']:.0f} min"
201:         marque = "⏰" if p["age"] is not None and p["age"] > PEREMPTION_MIN and p["etat"] in ACTIFS else " "
202:         per = ", ".join(p["perimetre"]) or "—"
203:         print(f"  {marque} {p['id'][:18]:18} · {p['etat'] or '?':8} · {age:>7} · {per}")
204:         if p["champs"].get("prochaine action"):
205:             print(f"      → {p['champs']['prochaine action']}")
206:     for a in avertissements:
207:         print(f"  ⚠ {a}")
208:     for e in erreurs:
209:         print(f"  ❌ {e}")
210:     return 1 if erreurs else 0
211: 
212: 
213: def autotest() -> int:
214:     with tempfile.TemporaryDirectory() as td:
215:         r = P
… [3354 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== dsh-tui help ==\" && timeout 25 dsh --profile dsh-tui --help 2>&1 | head -50; echo \"[exit $?]\"; echo; echo \"== docwatch diffstat ==\" && git -C tools/docwatch diff --stat && echo \"== docwatch tests ==\" && ls tools/docw … [135 caractères tronqués]`

  ```
== dsh-tui help ==
[exit 0]

== docwatch diffstat ==
 README.md                   |  25 ++++--
 src/docwatch/server.py      |  88 ++++++++++++++++++-
 src/docwatch/static/tree.js | 205 +++++++++++++++++++++++++++++++++++++++++++-
 src/docwatch/ui.py          |   6 ++
 tests/test_cli.py           |   3 +-
 tests/test_render.py        |  76 +++++++++++++++-
 tests/test_server.py        | 148 ++++++++++++++++++++++++++++++++
 tests/test_spa.py           | 129 ++++++++++++++++++++++++----
 8 files changed, 649 insertions(+), 31 deletions(-)
== docwatch tests ==
conftest.py
__pycache__
test_cli.py
test_config.py
test_diagrams.py
test_glossaire.py
test_paths.py
test_pins.py
test_render.py
test_server.py
test_spa.py
36:dev = ["pytest>=8", "ruff>=0.6", "build>=1.2", "twine>=5", "websocket-client>=1.7"]
53:[tool.pytest.ini_options]
54:testpaths = ["tests"]
60:src = ["src", "tests"]
67:"tests/*" = ["B011"]
  ```

### 🤖 Assistant

⏵ Je vérifie les contraintes de `verifie_en_cours` avant de réécrire l'état.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_en_cours.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_en_cours.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """verifie_en_cours.py — l'état doit rester court, structuré, reprenable et multi-session.
3: 
4: Le fichier `docs/pilotage/en-cours.md` est la seule source de l'état. Ce contrôle vérifie :
5:   1. un budget de **2 000 mots** ;
6:   2. les **sept sections** du template ;
7:   3. « Sessions en cours » : une sous-section `### Session ...` par session active, avec
8:      **Id**, **Rôle**, **Plan**, **Ambition**, **Stratégie**, **Objectif final**,
9:      **Ce qu'elle fait**, **Ce que font les autres**, **Prochaine action**, **Bloquants** et
10:      **Journal** ;
11:   4. **10 puces au plus** dans « Ce qui est en cours », sans doublon et sans puce de plus de 80 mots ;
12:   5. « Les chantiers et leurs bloquants » : une ligne **A**, **B**, **N**, **R** avec un bloquant
13:      **non vide** (le mot « aucun » est une information, une cellule vide est un oubli) ;
14:   6. **5 questions ouvertes au plus**, chacune avec ce qui la débloque (`→`) ;
15:   7. une **prochaine action nommée** dans « Ce qui reste » (A/B/C/N/R) ;
16:   8. aucune ligne de 
… [5638 caractères tronqués]
  ```

### 🤖 Assistant

⏵ J'ajoute l'état « en pause » au vérificateur et je rends la porte stricte.

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/sessions.py", "old_string": "Chaque session active expose son mandat dans `journal/sessions/<id>/plan.md` :\npérimètre, fichiers réservés, heartbeat, prochaine action, état. Les autres\nsessions consultent `--status` avant de claim … [887 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/sessions.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'ACTIFS = \\|A_CONFIRMER = \\|ETATS_CONNUS = \\|PEREMPTION_MIN' tools/sessions.py", "description": "Locate state constants for editing"}`

  ```
27:ACTIFS = {"actif", "active", "en cours", "bloqué", "bloquee", "bloqué(e)"}
28:A_CONFIRMER = {"à confirmer", "a confirmer"}
29:ETATS_CONNUS = ACTIFS | {"terminé", "termine", "libre", "libre."} | A_CONFIRMER
30:PEREMPTION_MIN = 45
170:        if a["age"] is not None and a["age"] > PEREMPTION_MIN:
203:        marque = "⏰" if p["age"] is not None and p["age"] > PEREMPTION_MIN and p["etat"] in ACTIFS else " "
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/sessions.py", "old_string": "ACTIFS = {\"actif\", \"active\", \"en cours\", \"bloqué\", \"bloquee\", \"bloqué(e)\"}\nA_CONFIRMER = {\"à confirmer\", \"a confirmer\"}\nETATS_CONNUS = ACTIFS | {\"terminé\", \"termine\", \"libre\", \" … [340 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/sessions.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/sessions.py", "old_string": "        e, _ = verifier(r)\n        assert any(\"manquant\" in x for x in e), e\n    print(\"autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé\")", "new_string": "        e, _  … [747 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/sessions.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/sessions.py'); t=p.read_text()\nt=t.replace('> et passe `État : terminé` quand la session se retire.','> et passe `État : en pause` (arrêt) ou `État : terminé` (retrait) quand e … [254 caractères tronqués]`

  ```
MODELE ok
        (d / "plan.md").write_text(
            "# Plan\n\n- **Session** : `a`\n- **Rôle** : test\n- **Périmètre** : A8.0\n"
            "- **Fichiers réservés** : `tools/a.py`\n- **Heartbeat** : 2026-10-30 11:00 HAE\n"
            "- **Prochaine action** : reprendre\n- **État** : en pause\n", encoding="utf-8")
        e, _ = verifier(r)
        assert not e, e
        e, _ = verifier(r, strict=True)
        assert not e, e
    print("autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé, "
          "pause sans heartbeat exigé")
    return 0


MODELE = """# Plan de session — <id>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > tools/porte-sessions.sh <<'SH'\n#!/bin/bash\n# porte-sessions.sh — les plans de session sont lisibles et le linter refuse un doublon.\nset -u\ncd \"$(dirname \"$0\")/..\"\npython3 tools/sessions.py --autotest || exit 1\npython3 … [286 caractères tronqués]`

  ```
autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé, pause sans heartbeat exigé
  ❌ mandat périmé (482 min) : e181ce02-cd50-488a-a6be-e84b79d40dcc — heartbeat à rafraîchir
  ❌ mandat périmé (1022 min) : fe3c05f0-834b-44f2-8739-501865d652c1 — heartbeat à rafraîchir
  ❌ plan actif non listé dans en-cours : 536cd5d6-94ac-4057-8fe9-11709a4587c7
[exit 1]
  ```

### 🤖 Assistant

⏵ Je passe les deux sessions arrêtées en pause avec leur point de reprise.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md')\nt=p.read_text()\nt=t.replace(\n\"- **Prochaine action** : le bloc linguistique v0 est livré (398 langues) et **AC-3/al … [2945 caractères tronqués]`

  ```
e181ce02 ok
fe3c05f0 ok
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md:19:- **Prochaine action** : le cycle **140/140** (T137, gold 432, 116 liens) est committé par le hub ;
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md:22:- **Arrêt** : 2026-11-02 15 h 06 (reboot) — dernière trace 14 h 40 ; **en pause** ; reprise par
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md:24:- **État** : en pause
journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md:18:- **État** : en pause
journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md:19:- **Prochaine action** : le **fonds CEGEP** (~127 scans) ; la **clôture** de la session ;
journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/plan.md:22:- **Arrêt** : 2026-11-02 15 h 06 (reboot) — dernière trace 13 h 25 ; **en pause** ; reprise par
  ```

### 🤖 Assistant

⏵ J'écris l'état cohérent : trois sessions, N2.ac, B13 140/140 et la reprise.

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "content": "# En ce moment\n\n**Mis à jour : 2026-11-02, 16 h 05 HNE (heure locale, EST).**\n\n> **État courant, pas histoire.** Une sous-section par **session active**, une ligne par **chantier**\n> avec son  … [16351 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
Updated file
</content>
  ```

### 🤖 Assistant

⏵ Je vérifie l'état et la porte stricte avant les commits.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py; echo \"[exit $?]\"; echo; python3 tools/sessions.py --check --strict; echo \"[exit $?]\"; echo; bash tools/porte-sessions.sh; echo \"[exit $?]\"", "description": "Validate state and strict session g … [5 caractères tronqués]`

  ```
en-cours · 2177 mots · 7 sections · 3 session(s) · 10 puces · 5 questions
  ❌ 4 anomalie(s) :
     · 2177 mots > budget 2 000
     · session « Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 » ne dit pas « **Ce qu'elle fait** »
     · question sans ce qui la débloque (`→`) : **N2** : les **200 k pas** sur le mélange 1 Go font-ils pass
     · question sans ce qui la débloque (`→`) : **Pensée** : l'**absence** est-elle annotable (5 phrases, 0 
[exit 1]

  ✅ plans cohérents
[exit 0]

autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé, pause sans heartbeat exigé
  ✅ plans cohérents
PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict
[exit 0]
  ```

### 🤖 Assistant

⏵ Je resserre l'état sous 2 000 mots et corrige les champs manquants.

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "content": "# En ce moment\n\n**Mis à jour : 2026-11-02, 16 h 10 HNE (heure locale, EST).**\n\n> **État courant, pas histoire.** Une sous-section par **session active**, une ligne par **chantier**\n> avec son  … [13877 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py; echo \"[exit $?]\"; echo; python3 tools/sessions.py --check --strict; echo \"[exit $?]\"", "description": "Recheck state length and session coherence"}`

  ```
en-cours · 1865 mots · 7 sections · 3 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
[exit 0]

  ✅ plans cohérents
[exit 0]
  ```

### 🤖 Assistant

⏵ Je mets à jour la roadmap, les chantiers et le plan de travail (chiffres et dates).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== roadmap occurrences ==\" && grep -n '111/111\\|T0–T108\\|2026-10-30\\|B10.2bis absent\\|3,0904\\|gold 342\\|plus de français unique' docs/pilotage/roadmap.md | cut -c1-220 && echo && echo \"== chantiers occurrences ==\" &&  … [206 caractères tronqués]`

  ```
== roadmap occurrences ==
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12
32:| **N — le natif** | DRVM, `drave-n0`, [distillation](../theorie/glossaire/entrees/distillation.md), usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; N2.h : corpus propre, **3,0904** en domaine, **16,70 → 3,85** h
42:L'ordre est **la valeur / le coût**, pas la date. La dernière mise à jour est le **2026-10-30**.
58:   (professeur 23,5 M, base 20 000 pas, distillation 20 000 pas × 3) ; **3,0904** en domaine — la porte
164:| **B13** | le **moteur de pensée** : RSN plurielle, arbre d'états, anytime | ✅ **state store v0** + moteur + **AC-3/alpha-bêta** + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes** + **nécessaire** 
183:| **N2** | la distillation : corpus, professeur, [curriculum](../theorie/glossaire/entrees/curriculum.md) | 🔬 | **N2.h** — corpus dédupliqué (**0 %** de fuite) : la chaîne propre vaut **3,0904**, pas 2,85 ; **la dive
323:- **non bloqué, à faire** : **N2** (plus de français unique, capacité) ; **N4**
… [1365 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== plan-travail occurrences ==\" && grep -n '2026-11-01\\|N2 — le natif\\|L — la langue\\|S — les structures\\|D/R/A\\|3,53\\|sessions.py --check' docs/pilotage/plan-travail.md | cut -c1-240 && echo && echo \"== gitignore work … [100 caractères tronqués]`

  ```
== plan-travail occurrences ==
9:> **Date** : 2026-11-01. **Machine** : une seule — 40 cœurs, 125 Go de RAM, 2 GPU de 16 Go,
38:| **N2 — le natif** | entraîner et évaluer le modèle natif sur les corpus D, mesurer longueur, capacité, diversité | N2, N4, le mètre honnête | **GPU** (1 des 2), 8–16 cœurs | la chaîne réelle est mesurée (N2.h → N2.z) : **le meilleur mo
39:| **L — la langue et la pensée** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**, 2–8 cœurs | le contrat/bloc (**398 langues**), le **gold 342 réels + 160 synt
40:| **S — les structures** | les structures d'interprétation candidates, la validation humaine/LLM, la banque | S, la pragmatique, l'export | **CPU**, 2–4 cœurs | l'analyseur plus riche (rôles, subordonnées), l'export vers le corpus |
41:| **D/R/A — les données, le lecteur, le moteur** | les corpus (texte intégral, PDF/OCR, licences, stubs), la préparation de R1.1/R1.2, A2.6/A8.3 | D, R1, A2.6/A8.3 | **CPU/IO**, 4–16 cœurs | le texte intégral des 10 corpus (**fait**), l'
56:dans le plan de chaque session et se vérifient par `tools/sessions.py --check`.
63:| **D/R/A** | `data/wikipedia/
… [657 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== roadmap 56-62 ==\" && sed -n '56,62p' docs/pilotage/roadmap.md && echo \"== roadmap 347-352 ==\" && sed -n '347,352p' docs/pilotage/roadmap.md && echo \"== top B tail ==\" && sed -n '31p' docs/pilotage/roadmap.md | grep -o  … [180 caractères tronqués]`

  ```
== roadmap 56-62 ==
   en ordre inverse) — les **scans réels de bout en bout** restent ouverts.
2. **N2 — la distillation** (en cours) : corpus dédupliqué (**0 %** de fuite), chaîne refaite
   (professeur 23,5 M, base 20 000 pas, distillation 20 000 pas × 3) ; **3,0904** en domaine — la porte
   < 2,5 est à **0,59** — et **16,70** sur de la littérature jamais vue. La **diversité
   française** ramène la littérature à **3,85** pour **+0,17** en domaine ; les **positions
   aléatoires** font passer 256 octets de **14,11** à **3,25**.
3. ~~N0.3b — la parité de [perplexité](../theorie/glossaire/entrees/perplexite.md) DRVM ↔ [GGUF](../theorie/glossaire/entrees/gguf.md)~~ **close** : conversion **68,1917 / 92,1875**, natif **4,6585 / 18,6394**.
== roadmap 347-352 ==
  puis **R1.2** (curriculum) tranchent ; la hiérarchie portée par N2 est écartée deux fois.
- **R2** : un **gist** explicite bat-il le **closed-book** sur une question dont l'indice est loin ?
- **N2** : le student peut-il descendre sous **2,5** de PPL — et **sur quel jeu** ? Sur le corpus
  propre il est à **3,0904** (0,59 de la porte) : le levier est la **quantité de texte français
  unique** (3,2 Mo), pas le budget.
- **B1
… [407 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\nlines=pathlib.Path('docs/pilotage/roadmap.md').read_text().splitlines()\nfor n in (31,32,164,183):\n    print(f'--- line {n} ({len(lines[n-1])} chars) tail:')\n    print(lines[n-1][-600:])\n    print … [63 caractères tronqués]`

  ```
--- line 31 (2363 chars) tail:
ourbe20** + **bord fin** + **gold 200** + **sous-ensembles** + **complexes** + **20 complexes** + **50 complexes** + **100 complexes** + **discours** + **anaphore** + **pièges anaphore** + **anaphore corrigée** + **pronoms objets** + **chaînes longues** + **rôles** + **hybride** + **sémantique** + **[plafond](../theorie/glossaire/entrees/plafond.md)** + **kappa** + **méta** + **pondéré** + **CV** + **CV graines** + **bilan anaphore**, **111/111 portes** | B10.3 attend un **encodeur qui porte** ; **B13** : **[DRVM](../theorie/glossaire/entrees/drvm.md)/native** (bloquée) ; **cascade mesurée** |

--- line 32 (305 chars) tail:
| **N — le natif** | DRVM, `drave-n0`, [distillation](../theorie/glossaire/entrees/distillation.md), usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; N2.h : corpus propre, **3,0904** en domaine, **16,70 → 3,85** hors dépôt ; N4 partiel | **N2** (plus de français unique, capacité), **N4** (consigne) |

--- line 164 (1845 chars) tail:
 **concurrentes** + **phase dans l'état** + **phase devinée** + **vote** + **cycle** + **courbe20** + **bord fin** + **gold 200** + **sous-ensembles** + **complexes** + **20 complexes** + **50 compl
… [1036 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\n\ndef sub(t, old, new, n=1):\n    c = t.count(old)\n    assert c == n, f\"attendu {n}, trouvé {c} pour {old[:60]!r}\"\n    return t.replace(old, new)\n\np = pathlib.Path('docs/pilotage/roadmap.md');  … [4143 caractères tronqués]`

  ```
roadmap ok 6380
chantiers ok 3952
  ```

### 🤖 Assistant

⏵ Je vérifie le nom de la racine OCR, puis j'ajoute le runbook au plan de travail.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'RACINES = \\|(\"' tools/ocr_pdf.py | head -8 && sed -n '1,20p' docs/pilotage/plan-travail.md | tail -8", "description": "Check OCR root names for runbook"}`

  ```
35:RACINES = [("Biblio_large", pathlib.Path("/home/stephane/Data13TB/stephane/Biblio_large"),
37:           ("CEGEP", pathlib.Path("/home/stephane/Data13TB/stephane/archives/CEGEP"),
45:            if ligne.startswith("Pages:"):
55:                              capture_output=True, timeout=60).stdout.decode("utf-8", "ignore")
73:        for png in sorted(tmp.glob("p-*.png")):
76:            textes.append(r.stdout.decode("utf-8", "ignore"))
83:    return hashlib.blake2b(t.encode("utf-8"), digest_size=taille).hexdigest()
91:            coupe = t.rfind(" ", debut + taille // 2, fin)
> **Chargement** : ce document avant d'ouvrir une session ; puis la fiche du chantier.

## 1. Où ce plan se situe

```
en-cours.md          ce qui se passe maintenant (état court, une section par session active)
plan-travail.md      qui fait quoi, où, à quelle cadence (ce document)
roadmap.md           l'ordre des chantiers et leur état
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\n\np = pathlib.Path('docs/pilotage/plan-travail.md')\nlines = p.read_text().splitlines()\n\ndef remplace_ligne(prefixe, nouvelle):\n    n = 0\n    for i, l in enumerate(lines):\n        if l.startswit … [7167 caractères tronqués]`

  ```
plan-travail ok 2414
  ```

### 🤖 Assistant

⏵ Je mets le registre des rouges à jour et je rends les journaux de portes durables.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '48,56p' docs/pilotage/references-non-regression.md && echo \"== portes.md ==\" && grep -n '49 portes\\|46 vertes\\|28/10' docs/methode/portes.md", "description": "Read exact gate reference rows"}`

  ```
## 1. Ce qui se vérifie en une commande

| quoi | commande | attendu |
|---|---|---|
| tests unitaires | `cargo test --release` (dans `drave-core/`) | **138 tests** (le compte est dans la sortie) |
| toutes les portes | `tools/toutes-les-portes.sh` | **49 portes** ; dernière passe : **46 vertes, 3 rouges** (28/10 00 h 12), **1 h 40**, aucune sautée — les deux rouges sont **structurelles** et connues (`porte-indice`, `porte-melange`) · ⚠ **ne jamais lire une porte à travers un `tail`** : sa dernière ligne suit l'échec, et le code de sortie est celui du tuyau |
| une porte | `tools/porte-<nom>.sh` | la dernière ligne dit ce qu'elle verrouille |

> ### ⚠️ DEUX DÉFAUTS DE MESURE, TROUVÉS LE 16/10 — ET ILS SONT DE LA MÊME FAMILLE
== portes.md ==
13:**1 h 30 – 2 h** sur Hauru (**49 portes** ; certaines entraînent de petits modèles, d'autres utilisent les [GPU](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md) ;
14:`porte-deepseek` est **hors réseau** et rapide). La dernière passe complète à **49 portes** (28/10 00 h 12) a donné
15:**46 vertes, 3 rouges** ; la liste et le diagnostic sont dans
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\n\ndef sub(t, old, new, n=1):\n    c = t.count(old); assert c == n, f\"attendu {n}, trouvé {c}: {old[:70]!r}\"\n    return t.replace(old, new)\n\np = pathlib.Path('docs/pilotage/references-non-regress … [2772 caractères tronqués]`

  ```
references ok
portes.md ok
toutes-les-portes ok
32:JOURNAUX=${JOURNAUX:-work/portes-$(date +%m%d-%Hh%M)}
  ```

### 🤖 Assistant

⏵ Je teste docwatch, régénère l'INDEX et vérifie les budgets.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch && timeout 240 python3 -m pytest -q 2>&1 | tail -15; echo \"[exit ${PIPESTATUS[0]}]\"", "description": "Run docwatch test suite", "timeoutMs": 260000}`

  ```
ImportError while loading conftest '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch/tests/conftest.py'.
tests/conftest.py:17: in <module>
    from docwatch.config import State, make_settings
E   ModuleNotFoundError: No module named 'docwatch'
[exit 4]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/index_reports.py && wc -l reports/INDEX.md && tail -3 reports/INDEX.md", "description": "Regenerate exhaustive report index"}`

  ```
547 fiches → reports/INDEX.md
555 reports/INDEX.md
| [rapport-vitesse-v41.md](rapport-vitesse-v41.md) | Rapport — La nuit des optimisations V4.1 : ×3,54 sur la passe, et pas un chiffre changé |
| [rapport-vram-transfert.md](rapport-vram-transfert.md) | La VRAM : ce qui coûte n'est pas le lien, c'est l'allocation |
| [toutes-langues.md](toutes-langues.md) | Extension à toutes les langues, puis aux grands corpus |
  ```

### 🤖 Assistant

⏵ Je relance les tests docwatch dans son environnement.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch && echo \"== system pytest ==\" && PYTHONPATH=src timeout 240 python3 -m pytest -q 2>&1 | tail -8; echo \"[exit ${PIPESTATUS[0]}]\"; echo \"== pipx python ==\" && PYTHONPATH=src timeout 240 ~/.local/share/pipx/venvs/docwa … [161 caractères tronqués]`

  ```
== system pytest ==
........................................................................ [ 65%]
......................................                                   [100%]
[exit 0]
== pipx python ==
/home/stephane/.local/share/pipx/venvs/docwatch/bin/python: No module named pytest
[exit 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 tools/taille_documents.py 2>&1 | tail -20; echo \"[exit ${PIPESTATUS[0]}]\"", "description": "Check document budgets after edits", "timeoutMs": 320000}`

  ```
2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2793    181   T1   2800  reports/README.md
    2567    185   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1865    179   T0   2000  docs/pilotage/en-cours.md
  T0 max : 4239 mots (budget 4 000)

  avertissements :
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ❌ 2 violation(s) :
     · docs/pilotage/references-non-regression.md : 2567 mots 
… [96 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je mesure les sections de l'état pour revenir sous le budget T0.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib\nt=pathlib.Path('docs/pilotage/en-cours.md').read_text()\ndef mots(s): return len(re.findall(r'\\S+',s))\nparts=re.split(r'(?m)^## ',t)\nprint('total',mots(t))\nfor p in parts[1:]:\n    titre=p.sp … [325 caractères tronqués]`

  ```
total 1865
  859  Sessions en cours
  277  Ce qui est en cours
  121  Les chiffres de l'état
  276  Les chantiers et leurs bloquants
   92  Ce qui reste
  109  Les questions ouvertes
   33  La carte
   190  Session `536cd5d6-94ac-4057-8fe9-11709a4587c7` — le hub, l'intégration
   361  Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurie
   222  Session `fe3c05f0-834b-44f2-8739-501865d652c1` — D/R/A : les données,
  ```

### 🤖 Assistant

⏵ Je compresse les trois sections de session pour repasser sous 4 000 mots T0.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); t=p.read_text()\n\nhub = \"\"\"### Session `536cd5d6-94ac-4057-8fe9-11709a4587c7` — le hub, l'intégration et la reprise\n\n- **Id** : `536cd5d6-94ac-4 … [5418 caractères tronqués]`

  ```
ok 1710
  en-cours · 1710 mots · 7 sections · 3 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
[exit 0]
  avertissements :
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ❌ 2 violation(s) :
     · docs/pilotage/references-non-regression.md : 2567 mots > budget 2500 (T1)
     · T0 : 4084 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

### 🤖 Assistant

⏵ Je retire de l'état les résultats clos et j'allège le registre des portes.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); t=p.read_text()\nfor prefix in (\"- **R13 — la tokenisation**\", \"- **B10.2bis — décodeur**\", \"- **A8** : **A8.0 : 19**\", \"- **B11.10** :\"):\n   … [2459 caractères tronqués]`

  ```
en-cours 1628
references 2499
  T0 max : 4002 mots (budget 4 000)

  avertissements :
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ❌ 1 violation(s) :
     · T0 : 4002 mots (AGENTS + en-cours + une tâche) > budget 4 000
[exit 1]
  ```

### 🤖 Assistant

⏵ Je gagne les deux mots manquants, puis j'écris la clôture GPU et la note du jour.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib, re\np=pathlib.Path('docs/pilotage/en-cours.md'); t=p.read_text()\nold=\"- **Ambition** : un état reprenable en deux minutes, des mandats qui disent la vérité.\"\nnew=\"- **Ambition** : un état repren … [361 caractères tronqués]`

  ```
1625
  T0 max : 3999 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
[exit 0]

- **Les dix corpus Wikipédia en texte intégral** : 20,53 M articles, 67,73 G caractères, 81,2 Go, 8 Ko 0 partout ; l'anglais clos à 99,2 % (l'écriture bloquée à 125/125 Go, le manifeste reconstruit depuis le journal et les SHA-256 ; la limite nommée : ~75 Go de résidence pour 6 M d'articles).
- **Le corpus PDF** : 2 785 PDF, 1 927 documents, 322 Mo, 8 Ko 0, licences nommées.
- **Le corpus Documents** : 7 459 PDF, 3 384 documents, 872 M caractères, 8 Ko 2,07 % (les 372 tronçons dupliqués).
- **Le corpus OCR** : 20 livres, 7 381 pages, 15,36 M caractères, 8 Ko 0 (val 115 fenêtres, éval 0/40) ; le pilote `--max-doc 20` est clos (le 20e, *Life Histories of Etnos Theory*, 450 p).
- **Le corpus OCR du CEGEP** : 10 notes scannées, 1 596 pages, 2 519 507 caractères, 8 Ko 0 (val 11 fenêtres) — le pilote `--racine CEGEP` ferme la boucle « livres, CEGEP, collections » (4 *Algorithms Illuminated* + *Data Structures in C* ajoutés). **Le lot de 40 s'est arrêté sur l'*Encyclopedia of Algorithms* (1 000+ pages) : `pdftoppm` a dépassé son timeout de 1 800 s et le run est tom
… [415 caractères tronqués]
  ```

### 🤖 Assistant

⏵ J'écris la clôture de la session GPU et la note de récit du reboot.

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/b6a672ec-3349-4a4c-9e23-4478aa823170/cloture.md", "content": "# Clôture — `b6a672ec` : le GPU bloqué, le reboot\n\n> **Session** : `b6a672ec-3349-4a4c-9e23-4478aa823170` · **Début** : 2026-11-01 13 h 28 ·\n> **Fin** : 20 … [1801 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/b6a672ec-3349-4a4c-9e23-4478aa823170/cloture.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('journal/2026-11-02/README.md'); t=p.read_text()\nnote = \"\"\"- **15 h 06 — reboot.** Les deux GPU étaient bloqués (`GPU requires reset`, `nvidia_drm refcnt -1`) ; le reset logiciel a … [511 caractères tronqués]`

  ```
note ok
## La suite

L'OCR complet (les 159 scans), la préparation R1.1/R1.2 (bloquée sur N2), et la clôture de la session à 8 h.
- **15 h 06 — reboot.** Les deux GPU étaient bloqués (`GPU requires reset`, `nvidia_drm refcnt -1`) ; le reset logiciel a échoué et le reboot a rendu les cartes (1 Mio, 0 %). Les deux sessions de travail (`e181ce02`, `fe3c05f0`) sont **en pause** ; leurs cycles sont committés par le hub. Détail : [`b6a672ec/cloture.md`](../sessions/b6a672ec-3349-4a4c-9e23-4478aa823170/cloture.md).
<!-- /notes -->
  ```

### 🤖 Assistant

⏵ Je passe la revue documentaire et les contrôles de clôture avant de committer.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for t in tools/revue_documentation.py tools/verifie_backlog.py tools/verifie_journal.py; do echo \"===== $t\"; timeout 300 python3 \"$t\" 2>&1 | tail -18; echo \"[exit ${PIPESTATUS[0]}]\"; done; echo \"===== porte-sessions\"; bash to … [206 caractères tronqués]`

  ```
===== tools/revue_documentation.py
  revue de documentation · 550 fiche(s) · 636 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
[exit 0]
===== tools/verifie_backlog.py
=== GRAPHE DU BACKLOG ===
  fiches 37 · lignes sans fiche 1 · arêtes dures 43 · plafonds 3
  profondeur 5 : R01 → R02 → R03 → R31 → R32 → R51
  frontière (4) : A2.6, N2, N3, N4

✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.
[exit 0]
===== tools/verifie_journal.py
  journal · 39 jour(s) · 111 session(s) · 1803 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
[exit 0]
===== porte-sessions
autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé, pause sans heartbeat exigé
  ✅ plans cohérents
PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict
[exit 0]
===== en-cours
  en-cours · 1625 mots · 7 sections · 3 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
[exit 0]
  ```

### 🤖 Assistant

⏵ Je commite d'abord docwatch (sous-module), puis le flux B13.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/docwatch && git add README.md src tests && git status --short && git commit -q -m \"GLOSSAIRE — LES TESTS DE L'ANNOTATION AU RENDU ; SERVEUR, SPA ET RENDU VERTS\" && git log --oneline -3; echo \"[exit $?]\"", "description": "Commi … [34 caractères tronqués]`

  ```
M  README.md
M  src/docwatch/server.py
M  src/docwatch/static/tree.js
M  src/docwatch/ui.py
M  tests/test_cli.py
M  tests/test_render.py
M  tests/test_server.py
M  tests/test_spa.py
d256888 GLOSSAIRE — LES TESTS DE L'ANNOTATION AU RENDU ; SERVEUR, SPA ET RENDU VERTS
676e144 GLOSSAIRE — LE POINTILLÉ PASSE À 1,5 PX EN currentColor (TROP DISCRET EN 1 PX GRIS)
1759b10 GLOSSAIRE — LES TERMES DU MANIFESTE SONT ANNOTÉS AU RENDU (POINTILLÉ + FICHE EN SURVOL), SANS TOUCHER AU MARKDOWN
[exit 0]
  ```

### 🤖 Assistant

⏵ Je commite le flux B13 avec son état et le cycle de clôture.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/implantation/bloc-linguistique.md docs/implantation/moteur-de-pensee.md tools/pensee/autotest.py tools/tests/linguistique/gold_reel.json tools/tests/linguistique/gold_reel.py reports/pensee-vrais-absents.json reports/rap … [1335 caractères tronqués]`

  ```
== staged ==
 docs/implantation/bloc-linguistique.md             |   2 +-
 docs/implantation/moteur-de-pensee.md              |   5 +-
 docs/pilotage/en-cours.md                          | 136 +++++-----
 journal/2026-11-02/README.md                       |   1 +
 .../536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md   |  30 +++
 .../cloture.md                                     |  39 +++
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md   |  19 +-
 .../fe3c05f0-834b-44f2-8739-501865d652c1/plan.md   |   9 +-
 reports/README.md                                  |   2 +-
 reports/pensee-partielle.json                      |  27 ++
 reports/pensee-vrais-absents.json                  |  14 +
 reports/rapport-pensee-partielle.md                |  59 ++++
 reports/rapport-pensee-vrais-absents.md            |  68 +++++
 tools/pensee/autotest.py                           |  13 +-
 tools/tests/linguistique/gold_reel.json            | 296 +++++++++++++++++++++
 tools/tests/linguistique/gold_reel.py              |  15 ++
 16 files changed, 652 insertions(+), 83 deletions(-)

[exit 0]
702b368c B13 — LES VRAIS ABSENTS : 5 PHRASES, 0 LIEN, GOLD 432 ; 140/140
[stderr]
  ✅ index : aucun fait stagé sans
… [5 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie le commit B13, puis je prépare le flux données (OCR + glossaire).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== HEAD ==\" && git show --stat --oneline HEAD | tail -6 && echo && echo \"== restant ==\" && git status --short | sed -n '1,80p'", "description": "Inspect B13 commit and remaining files"}`

  ```
== HEAD ==
 reports/rapport-pensee-partielle.md                |   59 +
 reports/rapport-pensee-vrais-absents.md            |   68 +
 tools/pensee/autotest.py                           |   13 +-
 tools/tests/linguistique/gold_reel.json            |  296 ++
 tools/tests/linguistique/gold_reel.py              |   15 +
 33 files changed, 4102 insertions(+), 114 deletions(-)

== restant ==
 M docs/README.md
 M docs/implantation/format-flux.md
 M docs/methode/contexte.md
 M docs/methode/portes.md
 M docs/methode/resultats.md
 M docs/pilotage/chantiers.md
 M docs/pilotage/plan-travail.md
 M docs/pilotage/references-non-regression.md
 M docs/pilotage/roadmap.md
 M docs/theorie/carte.md
 M docs/theorie/glossaire.md
 M docs/theorie/glossaire/README.md
 M docs/theorie/glossaire/index.json
 M docs/theorie/lecture-rapide.md
 M docs/theorie/vision.md
 M reports/INDEX.md
 M reports/corpus-genres.json
 M reports/native-generation.json
 M reports/rapport-genres.md
 M reports/rapport-ocr-pdf.md
 M tools/distiller_budget.py
 M tools/docwatch
 M tools/generer_natif.py
 M tools/glossaire_cartes.py
 M tools/ocr_pdf.py
 M tools/porte-sessions.sh
 M tools/sessions.py
 M tools/toutes-les-portes.sh
?? docs
… [1276 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je commite le flux données : OCR CEGEP, glossaire, docwatch et liens.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); t=p.read_text()\nold=\"**Mis à jour : 2026-11-02, 16 h 10 HNE (heure locale, EST).**\"\nnew=\"**Mis à jour : 2026-11-02, 16 h 25 HNE (heure locale, EST).* … [1650 caractères tronqués]`

  ```
horodatage ok
== staged ==
 reports/ocr-pdf-cegep.json                         |  49 ++++++
 reports/ocr-pdf-contamination.json                 |  57 +++++++
 reports/ocr-pdf.json                               |  55 ++++++
 reports/rapport-genres.md                          |   8 +-
 reports/rapport-ocr-cegep.md                       |  58 +++++++
 reports/rapport-ocr-pdf.md                         |  40 +++--
 tools/docwatch                                     |   2 +-
 tools/extrait_pdf.py                               | 187 +++++++++++++++++++++
 tools/glossaire_cartes.py                          |   3 +-
 tools/liens_glossaire.py                           | 155 +++++++++++++++++
 tools/ocr_pdf.py                                   |  12 +-
 45 files changed, 1259 insertions(+), 172 deletions(-)

[exit 0]
ca06ab0b D — L'OCR CEGEP, LE GLOSSAIRE AU RENDU ET LES LIENS DE LA FAMILLE 13
[stderr]
  ✅ index : aucun fait stagé sans état
  ```

### 🤖 Assistant

⏵ Je commite le flux N2 (mélange 1 Go, canal et pénalité).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); t=p.read_text()\nold=\"**Mis à jour : 2026-11-02, 16 h 25 HNE (heure locale, EST).**\"\nnew=\"**Mis à jour : 2026-11-02, 16 h 35 HNE (heure locale, EST).* … [1187 caractères tronqués]`

  ```
horodatage ok
== staged ==
 docs/pilotage/en-cours.md           |  2 +-
 reports/corpus-wiki-big-propre.json | 17 +++++++++++++++++
 reports/native-generation.json      | 16 ++++++++--------
 tools/distiller_budget.py           | 29 ++++++++++++++++++++---------
 tools/generer_natif.py              |  9 ++++++++-
 5 files changed, 54 insertions(+), 19 deletions(-)

[exit 0]
86cfb580 N2 — N2.ac EST LE MODÈLE DE PRODUCTION : LE MÉLANGE 1 Go, LE CANAL ET LA PÉNALITÉ
[stderr]
  ✅ index : aucun fait stagé sans état
  ```

### 🤖 Assistant

⏵ Je vérifie l'archive de la session hub, puis je commite le pilotage.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== session hub ==\" && ls -l journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/ && echo && echo \"== status ==\" && git status --short && echo && echo \"== checks ==\" && python3 tools/verifie_en_cours.py && python3 tools/ … [235 caractères tronqués]`

  ```
== session hub ==
total 1004
-rw-r--r--. 1 stephane stephane 159902  2 nov 16:01 digest.md
-rw-------. 1 stephane stephane   2320  2 nov 15:47 plan.md
-rw-r--r--. 1 stephane stephane  16864  2 nov 16:02 rapport.md
-rw-------. 1 stephane stephane 838973  2 nov 16:01 session.v4.jsonl.zstd

== status ==
 M docs/methode/portes.md
 M docs/pilotage/chantiers.md
 M docs/pilotage/plan-travail.md
 M docs/pilotage/references-non-regression.md
 M docs/pilotage/roadmap.md
 M docs/theorie/glossaire.md
 M reports/INDEX.md
 M tools/porte-sessions.sh
 M tools/sessions.py
 M tools/toutes-les-portes.sh

== checks ==
  en-cours · 1625 mots · 7 sections · 3 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  journal · 39 jour(s) · 112 session(s) · 1809 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  revue de documentation · 550 fiche(s) · 636 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

### 🤖 Assistant

⏵ Je vérifie le dernier écart du glossaire avant le commit de pilotage.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- docs/theorie/glossaire.md && echo \"== stat INDEX ==\" && git diff --stat -- reports/INDEX.md", "description": "Inspect remaining glossary and index diffs"}`

  ```
diff --git a/docs/theorie/glossaire.md b/docs/theorie/glossaire.md
index f74849d4..15f7d3da 100644
--- a/docs/theorie/glossaire.md
+++ b/docs/theorie/glossaire.md
@@ -103,7 +103,7 @@ check-list de reprise ; ils emploient le même vocabulaire que ce glossaire.
 ---
 
 
-## Les onze familles
+## Les treize familles
 
 Le glossaire fait **2 276 lignes** : il est découpé en **onze familles**, chacune atteignable
 directement. Les liens vers ce fichier continuent de fonctionner.
@@ -121,8 +121,9 @@ directement. Les liens vers ce fichier continuent de fonctionner.
 | **9.** Sources externes citées | [09-sources-externes-citees.md](glossaire/09-sources-externes-citees.md) | 79 |
 | **10.** Le pont linguistico-sémantique — le vocabulaire de l'émulation | [10-le-pont-linguistico-semantique-le-vocabu.md](glossaire/10-le-pont-linguistico-semantique-le-vocabu.md) | 514 |
 | **11.** Sources externes ajoutées par le §10 | [11-sources-externes-ajoutees-par-le-10.md](glossaire/11-sources-externes-ajoutees-par-le-10.md) | 50 |
+| **13.** Le corpus et la mesure documentaire | [13-le-corpus-et-la-mesure-documentaire.md](glossaire/13-le-corpus-et-la-mesure-documentaire.md) | 41 |
 
 > **Les fiches par 
… [623 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je commite le pilotage : état, roadmap, runbook, porte stricte et INDEX.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); t=p.read_text()\nold=\"**Mis à jour : 2026-11-02, 16 h 35 HNE (heure locale, EST).**\"\nnew=\"**Mis à jour : 2026-11-02, 16 h 45 HNE (heure locale, EST).* … [1716 caractères tronqués]`

  ```
horodatage ok
== staged ==
 docs/methode/portes.md                     |  18 +--
 docs/pilotage/chantiers.md                 |  16 ++-
 docs/pilotage/en-cours.md                  |   2 +-
 docs/pilotage/plan-travail.md              |  81 ++++++++++++--
 docs/pilotage/references-non-regression.md |  15 +--
 docs/pilotage/roadmap.md                   |  33 +++---
 docs/theorie/glossaire.md                  |   5 +-
 reports/INDEX.md                           | 173 ++++++++++++++++++++++++++++-
 tools/porte-sessions.sh                    |   6 +-
 tools/sessions.py                          |  29 +++--
 tools/toutes-les-portes.sh                 |   4 +-
 11 files changed, 318 insertions(+), 64 deletions(-)

[exit 0]
2dab14e4 PILOTAGE — L'ÉTAT REPREND : 140/140, N2.ac, DEUX SESSIONS EN PAUSE, PORTE STRICTE
86cfb580 N2 — N2.ac EST LE MODÈLE DE PRODUCTION : LE MÉLANGE 1 Go, LE CANAL ET LA PÉNALITÉ
ca06ab0b D — L'OCR CEGEP, LE GLOSSAIRE AU RENDU ET LES LIENS DE LA FAMILLE 13
702b368c B13 — LES VRAIS ABSENTS : 5 PHRASES, 0 LIEN, GOLD 432 ; 140/140
[stderr]
  ✅ index : aucun fait stagé sans état
  ```

### 🤖 Assistant

⏵ Je rafraîchis le heartbeat du hub, puis je vérifie la commande de reprise DSH.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md'); t=p.read_text()\nt=t.replace('- **Heartbeat** : 2026-11-02 15:50 EST','- **Heartbeat** : 2026-11-02 16:50 EST')\nt=t.r … [1367 caractères tronqués]`

  ```
hub heartbeat et état ok
[exit 0]
566ac478 HUB — LE RUNBOOK EST PUBLIÉ ; HEARTBEAT À JOUR, PROCHAINE ACTION LA PASSE DE PORTES
[stderr]
  ✅ index : aucun fait stagé sans état
  ```

- **bash** `{"command": "grep -rn -- \"'--resume'\\|\\\"--resume\\\"\\|--resume\" ~/.local/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/ 2>/dev/null | grep -v '\\.map' | head -8", "description": "Confirm DSH resume flag in installed app"}`

  ```
/home/stephane/.local/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/dsh-cmdline/lib/types/index.d.ts:22: * verbatim and in argv order. `dsh --profile tui --resume abc` yields
/home/stephane/.local/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/dsh-cmdline/lib/types/index.d.ts:23: * `['--resume', 'abc']`.
/home/stephane/.local/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/dsh-cmdline/README.md:34:- `ctx.cmdlineArgs` — the inner arguments of your invocation. Reading them returns an immutable snapshot and never consumes or changes them: `dsh --profile tui --resume abc` gives your app `['--resume', 'abc']`.
/home/stephane/.local/lib/node_modules/@deepseek-ai/dsh/node_modules/@deepseek-ai/dsh-cmdline/README.zh.md:34:- `ctx.cmdlineArgs`——本次调用的内层参数。读取它返回一份不可变快照，且绝不会消费或修改它们：`dsh --profile tui --resume abc` 给你的应用 `['--resume', 'abc']`。
  ```

### 🤖 Assistant

⏵ Je passe la vérification finale de l'arbre et des portes légères.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"== status ==\" && git status --short && echo \"(fin)\" && echo && echo \"== HEAD/état ==\" && python3 tools/verifie_etat_a_jour.py; echo \"[exit $?]\" && echo && echo \"== porte sessions ==\" && bash tools/porte-sessions.sh; e … [163 caractères tronqués]`

  ```
== status ==
(fin)

== HEAD/état ==
  état · dernier fait 2dab14e4 · dernier état 566ac478
  ✅ aucun fait commité après le dernier état
[exit 0]

== porte sessions ==
autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé, pause sans heartbeat exigé
  ✅ plans cohérents
PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict
[exit 0]

== en-cours ==
  en-cours · 1633 mots · 7 sections · 3 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
[exit 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for t in tools/revue_documentation.py tools/taille_documents.py tools/verifie_journal.py tools/verifie_backlog.py; do echo \"===== $t\"; timeout 300 python3 \"$t\" 2>&1 | tail -4; echo \"[exit ${PIPESTATUS[0]}]\"; done; echo \"=====  … [205 caractères tronqués]`

  ```
===== tools/revue_documentation.py
  revue de documentation · 550 fiche(s) · 636 JSON · 119 doc(s) · 81 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
[exit 0]
===== tools/taille_documents.py
     · 15 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ❌ 1 violation(s) :
     · T0 : 4007 mots (AGENTS + en-cours + une tâche) > budget 4 000
[exit 1]
===== tools/verifie_journal.py
  journal · 39 jour(s) · 112 session(s) · 1809 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
[exit 0]
===== tools/verifie_backlog.py
  profondeur 5 : R01 → R02 → R03 → R31 → R32 → R51
  frontière (4) : A2.6, N2, N3, N4

✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.
[exit 0]
===== schemas
  schémas · 458 document(s) · 66 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
[ex
… [5 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je repasse le T0 sous 4 000 et je commite l'ajustement.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); t=p.read_text()\nt=t.replace(\"- **Ce qu'elle fait** : audit des 111 sessions ; commits B13 **140/140**, D (OCR/glossaire), N2.ac ; sessions en pause ; po … [816 caractères tronqués]`
