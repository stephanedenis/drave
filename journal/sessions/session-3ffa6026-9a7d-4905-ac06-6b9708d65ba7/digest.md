# Session DSH — relecture

- identifiant : `session-3ffa6026-9a7d-4905-ac06-6b9708d65ba7`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-07 17:59:23
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J3.2 : la généalogie à deux faces — confronter la théorie de Panini (14 atomes, 9 dhātus) à nos mesures d'alignement (Glottolog) sur le corpus commun. Fiche `reports/rapport-genealogie-deux-faces.md` + JSON : ce qui converge, ce qui diverge, ce qui reste à mesurer. La théorie va dans `docs/theorie/genealogie-des-langues.md` (mise à jour), les chiffres restent dans reports/.

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

- **bash** `{"command": "pwd && ls -la && git log --oneline -15", "description": "Inspect workspace root and recent history"}`

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
drwxr-xr-x. 1 stephane stephane   180  7 nov 17:59 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   932  7 nov 00:00 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 74288  7 nov 16:47 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [2423 caractères tronqués]
  ```

- **bash** `{"command": "ls -la docs/theorie/ docs/methode/ reports/ 2>/dev/null | head -100", "description": "List theory, method and reports directories"}`

  ```
docs/methode/:
total 108
drwxr-xr-x. 1 stephane stephane   450  7 nov 10:49 .
drwxr-xr-x. 1 stephane stephane   138  6 nov 10:08 ..
-rw-r--r--. 1 stephane stephane  5836  7 nov 10:49 chantier-autonome.md
-rw-r--r--. 1 stephane stephane  7161  2 nov 12:53 contexte.md
-rw-r--r--. 1 stephane stephane  7410 31 oct 22:46 continuite.md
-rw-r--r--. 1 stephane stephane  1979 28 oct 13:25 echantillonnage-vdc.md
-rw-r--r--. 1 stephane stephane  4287 30 oct 10:33 illustrations.md
-rw-r--r--. 1 stephane stephane  2817 28 oct 09:17 miroir.md
-rw-r--r--. 1 stephane stephane  4964 29 oct 08:14 mission.md
-rw-r--r--. 1 stephane stephane  7512 28 oct 09:17 modularisation.md
-rw-r--r--. 1 stephane stephane 10183 30 oct 13:34 organisation-du-depot.md
-rw-r--r--. 1 stephane stephane  1882 28 oct 09:17 panini-nipada.md
-rw-r--r--. 1 stephane stephane  5238  4 nov 12:29 portes.md
-rw-r--r--. 1 stephane stephane  5340 29 oct 14:21 rangement.md
-rw-r--r--. 1 stephane stephane  7125 28 oct 13:00 relations-humaines.md
-rw-r--r--. 1 stephane stephane  7141  3 nov 11:23 ressources.md
-rw-r--r--. 1 stephane stephane  3809  2 nov 12:53 resultats.md

docs/theorie/:
total 232
drwxr-xr-x. 1 stephane stephane   598
… [5332 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/genealogie-des-langues.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/panini-nipada.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/genealogie-des-langues.md</path>
<type>file</type>
<content>
1: # La généalogie des langues, des dialectes et des styles
2: 
3: > **Ce que cette page est.** La **théorie** de la structure généalogique qui doit organiser l'**étage entrée-sortie** (nom historique : « couche commune »)
4: > entrée-sortie de Drave, et ce que les projets complémentaires **Panini** et **Nipada** ont établi sur elle. Les
5: > mesures de Drave sont dans [`reports/07-mesures-couche-commune.md`](../../reports/07-mesures-couche-commune.md).
6: > *À relire et à mettre à jour à chaque cycle : Panini et Nipada sont des sources vivantes.*
7: 
8: ## 1. Pourquoi une généalogie
9: 
10: Une couche entrée-sortie ne peut pas être « riche en langues » au sens d'une **liste**. Les langues forment une
11: **structure** : des familles, des branches, des dialectes, des styles, et des **traductions** qui traversent tout
12: cela. Si la structure est réelle, elle doit se voir dans les états du modèle — et si elle ne s'y voit pas, c'est le
13: modèle qui est incomplet.
14: 
15: La hiérarchie à couvrir, du plus large au plus fin :
16: 
17: | niveau | exemple | c
… [4091 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/panini-nipada.md</path>
<type>file</type>
<content>
1: # Étudier Panini et Nipada, régulièrement
2: 
3: > Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **à chaque cycle**, avant de conclure sur
4: > la généalogie, les styles ou les familles de langues.
5: 
6: ## Pourquoi
7: 
8: Les projets **`../Panini/`** et **`../Panini-Research/`** poursuivent le **même objectif par une approche
9: complémentaire** : Panini décompose le texte en **14 atomes sémantiques**, Nipada le fait tourner comme un tissu
10: computationnel — *algébrique, là où Drave est statistique*. Ils tiennent le **système linguistique** et généralisent
11: une **généalogie des langues, dialectes et styles**.
12: 
13: ## La règle
14: 
15: À chaque cycle, **lire ce qui a bougé chez eux** (docs, publications, journaux de bord, `git log`) et **confronter
16: leurs résultats aux nôtres**. Ce qui en sort va dans [`docs/theorie/genealogie-des-langues.md`](../theorie/genealogie-des-langues.md)
17: (la théorie) — **jamais les chiffres** (ils vont dans `reports/`).
18: 
19: ## Leur avertissement, à ne pas oublier ✗✓
20: 
21: Leur signatur
… [916 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-07, 17 h 05 HNE (heure locale, EST).**
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
… [11035 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -i -E 'panini|atome|corpus-commun|epoque|glottolog|genealog|J3|j3' ", "description": "Find Panini/genealogy related reports"}`

  ```
atomes-niveaux.json
corpus-commun.json
pensee-inventaire-panini.json
rapport-atomes-niveaux.md
rapport-corpus-commun.md
rapport-inventaire-panini.md
rapport-retrieval-epoque.md
retrieval-epoque.json
  ```

- **bash** `{"command": "grep -ril \"J3.2\\|deux faces\\|deux-faces\" docs reports journal tools 2>/dev/null | head -50", "description": "Search for J3.2 mentions"}`

  ```
docs/schemas/pipeline.mmd.svg
docs/pilotage/semaine-autonome.md
docs/pilotage/roadmap.md
docs/theorie/synthese/07-modeles-alternatifs-entree-sortie.md
docs/implantation/numa-segregation.md
reports/rapport-inventaire-panini.md
reports/pensee-inventaire-panini.json
reports/rapport-atomes-niveaux.md
reports/corpus-commun.json
reports/rapport-corpus-commun.md
reports/rapport-retrieval-epoque.md
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/session.jsonl.zstd
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/session.jsonl.zstd
journal/sessions/7c876089-605c-4836-930e-925a66028509/session.jsonl.zstd
journal/sessions/18c3f6d0-5bb1-45bb-9f94-ab0e7812218d/session.jsonl.zstd
journal/sessions/e14c26ae-6d52-41f9-a72f-6ebdcef172d5/session.jsonl.zstd
journal/sessions/00221850-90de-4287-90ee-324a35e504cd/session.v4.jsonl.zstd
journal/sessions/2fd56aa5-7b9b-40b0-9470-05c74b032d55/session.v4.jsonl.zstd
journal/sessions/c3d0f0bd-e344-4600-a023-0ed50d25b48b/session.v4.jsonl.zstd
journal/sessions/f0969e87-af0c-43b1-93cf-f278d9c90846/session.v4.jsonl.zstd
journal/sessions/fc167f70-be8b-4c63-be5e-3c0d3c0ba1c3/session.v4.jsonl.zstd
journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/session
… [1069 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -i -E 'corpus|langue|glotto|arbre|famille' | head -80", "description": "List language/corpus reports"}`

  ```
b102bis-corpus-jw.json
carte-24langues-3b.json
carte-24langues.json
corpus-commun.json
corpus-genres.json
corpus-litt-propre.json
corpus-multi-propre.json
corpus-pdf-contamination.json
corpus-pdf-documents-contamination.json
corpus-pdf-documents.json
corpus-pdf.json
corpus-propre.json
corpus-repo-propre.json
corpus-wiki-ar.json
corpus-wiki-ar-texte-contamination.json
corpus-wiki-ar-texte.json
corpus-wiki-big-propre.json
corpus-wiki-de.json
corpus-wiki-de-texte-contamination.json
corpus-wiki-de-texte.json
corpus-wiki-en.json
corpus-wiki-en-propre.json
corpus-wiki-en-texte-contamination.json
corpus-wiki-en-texte.json
corpus-wiki-es.json
corpus-wiki-es-texte-contamination.json
corpus-wiki-es-texte.json
corpus-wiki-fr.json
corpus-wiki-fr-texte-contamination.json
corpus-wiki-fr-texte.json
corpus-wiki-fr-texte-pilote-contamination.json
corpus-wiki-fr-texte-pilote.json
corpus-wiki-it.json
corpus-wiki-it-texte-contamination.json
corpus-wiki-it-texte.json
corpus-wiki-ja.json
corpus-wiki-ja-texte-contamination.json
corpus-wiki-ja-texte.json
corpus-wikipedia-contamination.json
corpus-wiki-propre.json
corpus-wiki-pt.json
corpus-wiki-pt-texte-contamination.json
corpus-wiki-pt-texte.json
corpus-
… [969 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-atomes-niveaux.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-retrieval-epoque.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-atomes-niveaux.md</path>
<type>file</type>
<content>
1: # Table de correspondance — 14 atomes de Panini et 8 niveaux de Drave
2: 
3: > **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J2.1 · **Date** : 2026-11-07
4: > **Verdict** : ✅ **la table est complète** — 14 atomes, 8 niveaux, 14 lignes, un ancrage et un porteur par
5: > atome, une mesure possible et son contrôle négatif. ⚠️ **aucune correspondance atome ↔ niveau n'est mesurée à
6: > ce stade** : c'est une **hypothèse de lecture** et un **protocole**, pas une corrélation. La calibration des
7: > 44 œuvres de Panini montre **33 paires d'atomes à |r| ≥ 0,5** (brut), **4 composantes > 1** et **80,7 %** de
8: > la variance sur les trois premières (ACP sur CLR) : la colinéarité est le premier confondant, avant même
9: > l'époque.
10: > **Dispositif** : lecture seule de `../../Panini/research` (HEAD `e10d695`, 2026-10-25) ; signatures
11: > `../../Panini/research/nipada/falsification/analytic_sigs_v1.json` (44 œuvres, 2026-10-18) ; contrat des
12: > niveaux `../docs/theorie/contrat-bloc-langue.md` ; JSON [`atomes-niveaux.json`](atomes
… [21951 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md</path>
<type>file</type>
<content>
1: # Corpus commun Panini/NIPADA ↔ Drave — UDHR, article 1
2: 
3: > **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J2.2 · **Date** : 2026-11-07
4: > **Verdict** : ✅ **le corpus est construit et vérifié** — **21 textes** (20 langues stratifiées + le
5: > français pivot), **5 familles**, **10 écritures**, **42 phrases**, **3 603 caractères**. Les **21**
6: > paires Panini ↔ Drave sont **identiques après normalisation** ; **418 paires exactes** sur **438**
7: > appariables (**95,4 %**). **20 écarts de surface** sont **exclus, pas corrigés**. Les **8 contrôles**
8: > (**6 rejets** attendus + **2 témoins** d'acceptation) sont **conformes** (8/8).
9: > **Dispositif** : lecture seule de `../Panini/research/data/udhr_corpus.json` (HEAD du dépôt
10: > `e10d695`, 2026-10-25 ; fichier **non suivi par git**, SHA-256 `531bc75c…`, vérifié avant et
11: > après) ; `data/udhr/articles_propres.jsonl`, `langues.jsonl`, `genealogie.json` (HEAD
12: > `9c7f71dc`, 2026-11-07) ; outil `../tools/corpus_commun.py` ;
13: > JSON [`corpus-commun.json`](corpus-
… [21383 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-retrieval-epoque.md</path>
<type>file</type>
<content>
1: # J3.1 — Le retrieval inter-langues à époque contrôlée
2: 
3: > **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J3.1 · **Date** : 2026-11-07
4: > **Verdict** : ✅ **la mesure est faite ; elle borne l'avertissement** —
5: > dans ce retrieval de **surface**, **l'écriture domine** (+0,609 ; IC 95 % [0,529 ; 0,702]), la **famille**
6: > compte ensuite (+0,181 [0,106 ; 0,253]), et **l'écart d'années ne pèse pas en moyenne** (−0,034 par siècle
7: > [−0,075 ; +0,009], p = 0,19 par permutation). À écriture contrôlée, les couples **contemporains** et
8: > **décalés** sont au **même niveau** : **0,710 vs 0,710**. Le renversement brut (0,238 vs 0,427) est un
9: > **effet de composition** : les couples décalés contiennent **60 %** de paires de même écriture, les
10: > contemporains **33 %**. **L'époque ne domine pas ici ; le confondant de composition, lui, n'est pas nul : sans
11: > contrôle, il fausse la comparaison.**
12: > **Dispositif** : trois corpus, un même retrieval de surface (n-grammes de caractères, TF-IDF, cosinus,
13: > top-1)
… [20682 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -A6 -B2 \"J3.2\" docs/pilotage/semaine-autonome.md docs/pilotage/roadmap.md tools/chantier/plan.json 2>/dev/null | head -120", "description": "Find J3.2 task definition"}`

  ```
docs/pilotage/roadmap.md-33-| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **le tagger n'est pas à 0,944 contre 0,85** (corpus différents : +7,34 pts sur 180, +6,35 sur 432) ; **R1.2-1024 mesuré** (2,6256 à 1 000 o) ; **R4.1–R4.4 mesurées** (R4.4 : 4/5 familles ≥ 90 % de parité) ; **R0.7 — bloc linguistique** (398 langues, 0,9687) | **R4.4 close** (limites nommées) ; **R1.1/R1.2 mesurées** (RoPE **3,2545** à 1 000 octets, fenêtre **−0,244**) ; la suite : **1 024 octets entraînés** ; **`rope2048`** **fini** (2×10 000 pas, deux drvm) ; R2/R3 attendent N5/N4 |
docs/pilotage/roadmap.md-34-| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; le fait divers tranché (la tête du GN arrête le verbe) ; [fiche](../../reports/rapport-s-fait-divers.md). **v6** : h050, h053 et « si fort que » **fermés**, gold **60** (vague 5) ; **60/60** types, **142/142** rôles, **50/50** compléments, couverture 1,00 ; corpus 65,5 %/9,1 %, 596/1 184 homographes
… [8058 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/ | grep -i -E 'panini|atome|glotto|genealog|corpus_commun|retrieval' ; echo '---'; ls data/udhr/ | head -30; echo '---'; python3 -c \"import json;d=json.load(open('data/udhr/genealogie.json'));print(type(d));print(list(d)[:3] if isinstance(d,dict) else d[:2])\"", "description": … [43 caractères tronqués]`

  ```
corpus_commun.py
genealogie_udhr.py
retrieval_epoque.py
retrieval_parallele.py
retrieval_udhr.py
---
articles.jsonl
articles_propres.jsonl
_eng.txt
familles
_fra.txt
genealogie.json
langues.jsonl
meta.json
udhr_10_train.txt
udhr_10_val.txt
udhr_1_train.txt
udhr_1_val.txt
udhr_50_train.txt
udhr_50_val.txt
udhr_fra_train.txt
udhr_fra_val.txt
udhr_train.txt
udhr_val.txt
---
<class 'dict'>
['udhr_007.xml', 'udhr_008.xml', 'udhr_009.xml']
  ```

- **bash** `{"command": "cat reports/corpus-commun.json | head -80; echo '...'; python3 -c \"\nimport json\nd=json.load(open('reports/corpus-commun.json'))\nprint(d.keys())\n\"", "description": "Inspect corpus-commun JSON structure"}`

  ```
{
  "controle_negatif": {
    "date": "2026-11-07",
    "n_ok": 8,
    "n_rejets_attendus": 6,
    "n_temoins_attendus": 2,
    "n_tests": 8,
    "tests": [
      {
        "attendu": "acceptation",
        "detail": "udhr_eng : Panini == Drave après normalisation",
        "nom": "temoin_paire_correcte",
        "obtenu": "acceptation",
        "ok": true
      },
      {
        "attendu": "rejet",
        "detail": "un caractère changé dans le texte Panini doit casser l'égalité",
        "nom": "panini_altere",
        "obtenu": "rejet",
        "ok": true
      },
      {
        "attendu": "rejet",
        "detail": "un caractère changé dans le texte Drave doit casser l'égalité",
        "nom": "drave_altere",
        "obtenu": "rejet",
        "ok": true
      },
      {
        "attendu": "rejet",
        "detail": "deux langues différentes ne doivent pas être appariables",
        "nom": "appariement_croise",
        "obtenu": "rejet",
        "ok": true
      },
      {
        "attendu": "rejet",
        "detail": "nb_phrases 1 != 2; caractères perdus ou ajoutés (hors espaces)",
        "nom": "phrase_supprimee",
        "obtenu": "rejet",
        "ok": true
      },
    
… [1088 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nfor t in d if isinstance(d,list) else d.get('taches',[]):\n    if t.get('id') in ('J3.1','J3.2','J3.3'):\n        print(json.dumps(t,ensure_ascii=False,indent=2))\n\" 2>/dev/null || sed -n '100,170p' tools/chanti … [64 caractères tronqués]`

  ```
{
  "id": "J3.1",
  "jour": 3,
  "titre": "Panini II — le retrieval à époque contrôlée",
  "mandat": "Tâche J3.1 : le retrieval inter-langues **à époque contrôlée** (l'avertissement de Panini : l'époque domine). Sur le lexique B7 (71 langues) et/ou le corpus commun, mesure le retrieval avec un contrôle de date (couples contemporains vs décalés) et la surface (écriture, famille). Fiche `reports/rapport-retrieval-epoque.md` + JSON, contrôle négatif.",
  "budget_min": 90,
  "acceptation": [
    {
      "commande": "test -f reports/rapport-retrieval-epoque.md && echo FICHE-OK",
      "attendu": "FICHE-OK"
    }
  ]
}
{
  "id": "J3.2",
  "jour": 3,
  "titre": "Panini II — la généalogie à deux faces",
  "mandat": "Tâche J3.2 : la généalogie à deux faces — confronter la théorie de Panini (14 atomes, 9 dhātus) à nos mesures d'alignement (Glottolog) sur le corpus commun. Fiche `reports/rapport-genealogie-deux-faces.md` + JSON : ce qui converge, ce qui diverge, ce qui reste à mesurer. La théorie va dans `docs/theorie/genealogie-des-langues.md` (mise à jour), les chiffres restent dans reports/.",
  "budget_min": 90,
  "acceptation": [
    {
      "commande": "test -f reports/rapport-genealogi
… [74 caractères tronqués]
  ```

- **bash** `{"command": "wc -l tools/genealogie_udhr.py && sed -n '1,120p' tools/genealogie_udhr.py", "description": "Inspect genealogy tool head"}`

  ```
84 tools/genealogie_udhr.py
#!/usr/bin/env python3
"""genealogie_udhr.py — LA GÉNÉALOGIE DES 448 LANGUES (famille, branche), depuis Glottolog.

POURQUOI. Une couche entrée-sortie n'est pas « riche en langues » parce qu'elle en compte beaucoup : elle l'est si
elle couvre la **structure** — familles, branches, dialectes (cf. `docs/genealogie-des-langues.md`). Et les tests
doivent être **organisés par niveau** : une paire de langues sœurs n'est pas une paire de familles différentes.

LA SOURCE. Glottolog (CLDF, `glottolog/glottolog-cldf` sur GitHub) ✓ : `languages.csv` (27 000 languoïdes, avec
`Family_ID`, `Level`, `ISO639P3code`) et `values.csv` (dont la **classification** complète, « Indo-European > Italic
> Romance > … »). On télécharge une fois, on cache dans `data/glottolog/`.

SORTIE : `data/udhr/genealogie.json` — pour chaque fichier UDHR : `{iso3, famille, branche, glottocode, niveau}`.
⚠️ Ce que ce n'est pas ✗ : Glottolog donne la classification **savante**, pas la distance mesurée ; et certaines
langues UDHR ont un code qui n'est pas dans Glottolog ✗✓ (on le compte et on le dit ✓).
"""
from __future__ import annotations
import argparse, csv, json, pathlib, urllib.request

BA
… [2692 caractères tronqués]
  ```

- **bash** `{"command": "ls ../Panini/ 2>/dev/null | head; echo '---'; ls ../Panini/research/ 2>/dev/null | head -40; echo '---'; git -C ../Panini log --oneline -5 2>/dev/null; git -C ../Panini/research log --oneline -5 2>/dev/null", "description": "Inspect Panini repository"}`

  ```
config
CONTEXTE-IA.md
copilotage
corpus
data
Dockerfile.template
docs
experiments
experiments.json
legacy
---
AGENTS.md
archives
archives_scripts_v1
autonomous-agents
colab_results
config
conftest.py
copilotage
data
deployments
diagrams_dhatu_cycles
docs
E1_REPORT_20251224.md
FONDAMENTAL_RESEARCH_ROADMAP_Q1_2026.md
GATES_G1_G3_REPORT_2026-09-07.md
INTEGRITE_REPO_2026-10-18.md
json
misc
nipada
NIPADA_BACKLOG.md
notebooks
orchestrate_workflows.py
panini
panini-fs
PANINIFS_ARCHITECTURE_REFERENCE.md
Panini-Research.code-workspace
philosophy-theory
PLAN_CORPUS_SCALING_478b_479.md
PLAN_REORGANISATION_RESEARCH.md
prepare_e1_corpus.py
projects
publications
__pycache__
pyproject.toml
qualite_framework
README.md
README_SESSION_476_478c.md
RECHERCHE_PISTES_INDEX_v1.0.md
references
reports
---
9b80c323 docs(readme): réécriture complète — état réel, 7 axes de recherche, lien avec Drave
c70bcff8 chore(submodule): bump research (contrôle d'intégrité round 117)
0b34cadc chore(submodule): bump research (journal — leçon de harnais)
de546a85 chore(submodule): bump research (hooks de bissection WIP)
04a70418 chore(submodule): bump research (WIP recherche localisée, base vérifiée)
e10d695e6 docs(incide
… [745 caractères tronqués]
  ```

- **bash** `{"command": "grep -rIl \"analytic_sigs\\|signature\" ../Panini/research --include=*.py 2>/dev/null | head -30", "description": "Find signature computation scripts in Panini"}`

  ```
../Panini/research/.github/scripts/weekly_optimizer.py
../Panini/research/archives/filesystem_archive/cleanup/backup_20250906_154458/OPERATIONS/DevOps/scripts/autonomous_analyzer.py
../Panini/research/archives/filesystem_archive/cleanup/backup_20250906_154458/OPERATIONS/DevOps/scripts/comprehensive_opensource_strategy.py
../Panini/research/archives/filesystem_archive/cleanup/backup_20250906_154458/OPERATIONS/DevOps/scripts/implementation_roadmap_generator.py
../Panini/research/archives/filesystem_archive/cleanup/backup_20250906_154458/OPERATIONS/DevOps/scripts/information_theory_collector.py
../Panini/research/archives/pre_v14_unification_20260521/panlang_dhatu_nsm/compression_semantique.py
../Panini/research/archives/scripts_v2/build_articles_v1.py
../Panini/research/archives/scripts_v2/build_corpus_v295.py
../Panini/research/archives/scripts_v2/build_encyclopedia_v2.py
../Panini/research/archives/scripts_v2/build_encyclopedia_v296.py
../Panini/research/archives/scripts_v2/build_graph_v297b.py
../Panini/research/archives/scripts_v2/build_molecules_v291.py
../Panini/research/archives/scripts_v2/build_nc_v277.py
../Panini/research/archives/scripts_v2/build_nc_v279.py
../Panini/resea
… [1078 caractères tronqués]
  ```

- **bash** `{"command": "grep -rIn \"dhātu\\|dhatu\\|dhātu\\|9 dh\" ../Panini/README.md ../Panini/research/README.md 2>/dev/null | head -40", "description": "Find dhātu documentation"}`

  ```
../Panini/README.md:18:- **NIPADA** — la couche *descriptive* : le tissu computationnel (graphe, dhātus, DTP),
../Panini/README.md:31:| **NIPADA** | moteur de sémantique computationnelle (graphe, dhātus, DTP) | `research/src/nipada/` | **actif** |
../Panini/README.md:68:les **dhātus** sont les instructions, le **SAT-solver** est le processeur. Le produit
../Panini/research/README.md:69:│   ├── core/             ← Noyau : hardware_mapping (V14/dhātus), v14_projector_v360
../Panini/research/README.md:70:│   ├── compute/          ← Tissu computationnel : trinary_machine (Ł3), semantic_synthesizer (SAT), dhatu_token_program (DTP)
  ```

- **bash** `{"command": "grep -rIln \"Glottolog\" reports/*.md | head -40", "description": "Find reports mentioning Glottolog"}`

  ```
reports/rapport-corpus-commun.md
reports/rapport-inventaire-panini.md
reports/rapport-miroir-blocs.md
reports/rapport-r41-bloc-tableaux.md
reports/rapport-retrieval-epoque.md
  ```

- **bash** `{"command": "sed -n '40,140p' ../Panini/README.md", "description": "Read Panini README theory sections"}`

  ```
C'est le chantier le plus lourd et le plus vérifiable : un **assistant de preuve** minimal
(Python, sans dépendance) et ses mathématiques.

**Ce qui est prouvé à ce jour** (chaque énoncé est re-vérifié par le noyau, souvent sur
plusieurs niveaux : kit léger, chaîne réelle, validation lourde de plusieurs heures) :

| Domaine | Acquis |
|---|---|
| **ℝ localisé** | `ℝ = Σ x:ℝ. located x` par coupures de Dedekind ; ordre total, `+`, `−`, `\|·\|`, `·`, `sup` |
| **Corps** | multiplication définie par encadrements rationnels (**sans cas de signe** : le signe n'est pas décidable) ; `x·0 ⊆ 0`, `x·1 ⊆ x` ; **inverse des positifs** et **`x·x⁻¹ ≃ 1`** |
| **Ordre** | trichotomie constructive, antisymétrie, compatibilités, monotonies |
| **Métrique** | distance `d`, inégalité triangulaire, axiome `d(x,y) ≃ 0 ⟺ x ≃ y`, **isométrie de translation**, `d ≥ 0` |
| **Localisation** | close par `+` et `−` (`add_cut_located`, `reel_loc_add_located`) |
| **Complétude** | sup, Archimédien, complétude des coupures |

**Infrastructure de vérification** (ce qui rend le rythme tenable) :

- **cache de noyau** — un noyau ℝ complet (1 h 25 de construction) se recharge en **0,23 s** ;
- **tactique ℚ** — les l
… [4611 caractères tronqués]
  ```

- **bash** `{"command": "grep -rIn \"dhātu\" ../Panini/README.md ../Panini/research/docs/*.md 2>/dev/null | head -50", "description": "Search dhatu mentions in docs"}`

  ```
../Panini/README.md:18:- **NIPADA** — la couche *descriptive* : le tissu computationnel (graphe, dhātus, DTP),
../Panini/README.md:31:| **NIPADA** | moteur de sémantique computationnelle (graphe, dhātus, DTP) | `research/src/nipada/` | **actif** |
../Panini/README.md:68:les **dhātus** sont les instructions, le **SAT-solver** est le processeur. Le produit
../Panini/research/docs/ARCHITECTURE_NOYAU_NIPADA_v1.0.md:18:| **Noyau (iso)** | Moteur rigide / mathématique (V14, dhātus, Ł3, TrinarySAT, DTP, graphe = tissu computationnel). Il **infère**, il est déterministe, il **ne décrit jamais** aucun corpus. |
../Panini/research/docs/ARCHITECTURE_NOYAU_NIPADA_v2.0.md:12:d'implémentation** (V14, dhātus, TrinarySAT, DTP, graphe). La v2.0 donne les définitions
../Panini/research/docs/ARCHITECTURE_NOYAU_NIPADA_v2.0.md:49:| **instanciation candidate** | un artefact d'implémentation révisable (atomes V14, dhātus, DTP, projections, graphes) | le noyau, une fondation |
../Panini/research/docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md:10:Pāṇini (dhātu, IVᵉ s. BCE) → Leibniz (*Characteristica Universalis*, 1679) → Gödel (Gödel numbering, 1931) → Łukasiewicz (multi-valued logic, 1920) → Zadeh (fuzzy l
… [5751 caractères tronqués]
  ```

- **bash** `{"command": "grep -rIn \"0[.,]138\\|0[.,]049\" ../Panini/research ../Panini/README.md 2>/dev/null | grep -v Binary | head -40", "description": "Find beta coefficients source"}`

  ```
_reconstructions': 0, 'perfect_reconstruction_rate': 0.0, 'processed_texts_details': [{'original_length': 49, 'compressed_length': 813, 'reconstructed_length': 49, 'compression_ratio': 0.06027060270602706, 'reconstruction_fidelity': 1.0, 'is_perfect': False, 'processing_time': 0.00014710426330566406, 'source_path': 'root[0].title'}, {'original_length': 690, 'compressed_length': 2922, 'reconstructed_length': 690, 'compression_ratio': 0.23613963039014374, 'reconstruction_fidelity': 1.0, 'is_perfect': False, 'processing_time': 0.00021648406982421875, 'source_path': 'root[0].abstract'}, {'original_length': 32, 'compressed_length': 667, 'reconstructed_length': 32, 'compression_ratio': 0.047976011994003, 'reconstruction_fidelity': 1.0, 'is_perfect': False, 'processing_time': 0.00015354156494140625, 'source_path': 'root[0].content_hash'}, {'original_length': 34, 'compressed_length': 681, 'reconstructed_length': 34, 'compression_ratio': 0.049926578560939794, 'reconstruction_fidelity': 1.0, 'is_perfect': False, 'processing_time': 0.00015234947204589844, 'source_path': 'root[0].url'}, {'original_length': 34, 'compressed_length': 737, 'reconstructed_length': 34, 'compression_ratio': 0.0461329
… [48731 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '150,230p' ../Panini/research/docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md; echo '---580'; sed -n '575,620p' ../Panini/research/docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md", "description": "Read V14 and dhatu sections"}`

  ```
- ◇(MODALITÉ) est émetteur pur (3 sortants, 0 entrants)
- ↗ et λ n'ont qu'1 lien chacun — candidats réduction

11 questions ouvertes (Q001–Q011) dont :
- Q001 : L'agent est-il toujours ⊙(SUJET) ? L'ergatif contredit.
- Q002 : ↗(ORIENTATION) est-il réductible à ∼+⊕ ?
- Q005 : La différence existe-t-elle sans observateur ?
- Q010 : Le changement est-il ∆∘⧖ ou un atome distinct ?

### 1.9 Sous-Atomes V14 — Primitives Spatiales/Temporelles (Jackendoff, Phase 38, 2026-08-07)

6 sous-atomes enrichissant ESPACE(⊕) et TEMPS(⧖) :

| Sous-atome | Parent V14 | Origine Jackendoff |
|------------|-----------|---------------------|
| PROXIMAL | ESPACE (⊕) | AT, HERE |
| DISTAL | ESPACE (⊕) | FAR, THERE |
| DUR_LONG | TEMPS (⧖) | PATH (étendu) |
| DUR_SHORT | TEMPS (⧖) | POINT |
| PUNCTUAL | TEMPS (⧖) | TOUCH, MOMENT |
| CONTINUOUS | TEMPS (⧖) | GO, STAY |

**Résultat** : couverture NSM de 89% (58/65) → **100% (65/65)**. Confiance de 0.780 → 0.891 (+0.111). Total : 14 + 6 = 20 primitives.

---

## 2. Dhātus — Opérateurs Cognitifs

### 2.1 Origine (Pāṇini, IVᵉ s. BCE)

9 opérateurs cognitifs universels dérivés du système de dhātus de Pāṇini :

| Dhātu | Sens |
|--------|------|
| BHŪ | existence/p
… [4140 caractères tronqués]
  ```

- **bash** `{"command": "grep -rIln \"généalogie\\|filiation\\|genealogy\" ../Panini/research/docs ../Panini/research/nipada 2>/dev/null | head -30", "description": "Find Panini genealogy docs"}`

  ```
../Panini/research/docs/journal-de-bord/2026-04-25.md
../Panini/research/docs/journal-de-bord/2026-04-26.md
../Panini/research/docs/journal-de-bord/2026-05-21.md
../Panini/research/docs/journal-de-bord/2026-05-22.md
../Panini/research/docs/journal-de-bord/2026-05-23.md
../Panini/research/docs/journal-de-bord/2026-05-24.md
../Panini/research/docs/journal-de-bord/2026-06-01.md
../Panini/research/docs/journal-de-bord/2026-06-03.md
../Panini/research/docs/journal-de-bord/2026-06-04.md
../Panini/research/docs/journal-de-bord/2026-06-28.md
../Panini/research/docs/journal-de-bord/2026-06-29.md
../Panini/research/docs/journal-de-bord/2026-06-30.md
../Panini/research/docs/journal-de-bord/2026-07-01.md
../Panini/research/docs/journal-de-bord/2026-07-02.md
../Panini/research/docs/journal-de-bord/2026-07-03.md
../Panini/research/docs/journal-de-bord/2026-07-07.md
../Panini/research/docs/journal-de-bord/2026-08-04.md
../Panini/research/docs/journal-de-bord/2026-08-05.md
../Panini/research/docs/journal-de-bord/2026-09-08.md
../Panini/research/docs/journal-de-bord/2026-09-09.md
../Panini/research/docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md
../Panini/research/docs/CRITIQUE_NIPADA_2026-07-14.md
.
… [491 caractères tronqués]
  ```

- **bash** `{"command": "ls -la ../Panini/research/nipada/falsification/ | head -40; python3 - <<'EOF'\nimport json,os\np='../Panini/research/nipada/falsification/analytic_sigs_v1.json'\nd=json.load(open(p))\nprint(type(d))\nif isinstance(d,dict): print(list(d.keys())[:10])\nEOF", "description": "Inspect analyt … [20 caractères tronqués]`

  ```
total 212144
drwxr-xr-x. 1 stephane stephane   21326 18 oct 10:03 .
drwxr-xr-x. 1 stephane stephane     650  4 jun 11:29 ..
-rw-r--r--. 1 stephane stephane   22381 18 oct 10:03 analytic_sigs_v1.json
-rw-r--r--. 1 stephane stephane    7048 18 oct 10:03 axeA_p1_subset_v1.json
-rw-r--r--. 1 stephane stephane    1644 18 oct 10:03 benchmark_generatif_analytique_v1.json
-rw-r--r--. 1 stephane stephane    4228 18 oct 10:03 benchmark_generatif_clean_v1.json
-rw-r--r--. 1 stephane stephane    9358  8 sep 15:34 benchmark_generatif_contenu_v1.json
-rw-r--r--. 1 stephane stephane    6059 18 oct 10:03 benchmark_generatif_corpus_v1.json
-rw-r--r--. 1 stephane stephane    2200 18 oct 10:03 benchmark_generatif_v1.json
-rw-r--r--. 1 stephane stephane   25410 30 avr  2026 circular_translation_test.json
-rw-r--r--. 1 stephane stephane    1738 18 oct 10:03 container_profiles_v1.json
-rw-r--r--. 1 stephane stephane    7948 28 jun 19:53 context_q1_embedding.json
-rw-r--r--. 1 stephane stephane    3849 28 jun 19:48 context_q1_normalized.json
-rw-r--r--. 1 stephane stephane   11481 28 jun 19:32 context_q1_translation_drift.json
-rw-r--r--. 1 stephane stephane     773 28 jun 19:32 context_q3_channel_stabil
… [2206 caractères tronqués]
  ```

- **bash** `{"command": "grep -rIln \"analytic_sigs_v1\" ../Panini/research --include=*.py --include=*.md 2>/dev/null | head -20", "description": "Find generator of analytic signatures"}`

  ```
../Panini/research/scripts/loi_analytique.py
  ```

- **bash** `{"command": "ls ../Panini/research/nipada/falsification/; echo '---'; find ../Panini/research/nipada -maxdepth 2 -type d | head -40", "description": "List falsification and nipada dirs"}`

  ```
analytic_sigs_v1.json
axeA_p1_subset_v1.json
benchmark_generatif_analytique_v1.json
benchmark_generatif_clean_v1.json
benchmark_generatif_contenu_v1.json
benchmark_generatif_corpus_v1.json
benchmark_generatif_v1.json
circular_translation_test.json
container_profiles_v1.json
context_q1_embedding.json
context_q1_normalized.json
context_q1_translation_drift.json
context_q3_channel_stability.json
corpus_dor_cic_v1.json
corpus_dor_cic_v1.tsv
exploit_corpus_v1.json
exploit_corpus_v2.json
frontiere_promotion_corpus.json
h0prime_56H_holdout_validation_v1.json
h0prime_analytic_oos_v2.json
H2_v3_phrases_definitionnelles.json
H3_v3_calibration_phrases.json
LISTE_ACQUISITION_272.md
loi_analytique_cv_v1.json
loi_analytique_full_cv_v1.json
loi_analytique_v1.json
m2_subset_results_v1.json
modern_corpus_sigs_v2.json
modern_law_test_v1.json
modern_sigs_v1.json
nipada_adaptive_test.json
nipada_bootstrap.json
nipada_decomposer_test.json
nipada_holdout_v1.json
nipada_holdout_v2.json
nipada_lacunes_report.json
nipada_lacunes_report_NOBONUS.json
nipada_multilang_test.json
nipada_panini_fs_test.json
nipada_speech_acts_test.json
nipada_subject_test.json
nipada_supervised_report.json
nipada_udhr_benchmark.
… [11337 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor p in ['nipada_v355_linguistic_distance.json','nipada_v354_linguistic_profiles.json','nipada_v361_multilingual.json']:\n    d=json.load(open('../Panini/research/nipada/falsification/'+p))\n    print('==',p,type(d))\n    if isinstance(d,dict):\n         … [142 caractères tronqués]`

  ```
== nipada_v355_linguistic_distance.json <class 'dict'>
  section : §355
  date : 2026-05-25T13:30:03.930227+00:00
  description : Corrélation d_profile(LP) ↔ d_topo(v35) — décomposition N1/N2/N3
  n_texts : 17
  n_pairs : 66
  scheme_results : {'default': {'weights': {'N1': 0.4, 'N2': 0.2, 'N3': 0.4}, 'pearson_r': 0.375537, 'r_squared': 0.141028, 'd_profile_min': 0.015083, 'd_profile_max': 0.192482, 'd_profile_mean': 0.08621}, 'N1_only': {'
  default_pearson_r : 0.375537
  default_r_squared : 0.141028
== nipada_v354_linguistic_profiles.json <class 'dict'>
  section : §354
  date : 2026-05-25T12:22:11.855951+00:00
  description : Profils Linguistiques N1-N5 — Corpus §334 (textes cachés)
  pipeline_version : encyclopaedic_v352
  decoder_version : v353
  n_analysed : 27
  n_cacheable : 27
  n_roundtrip_pass : 27
== nipada_v361_multilingual.json <class 'dict'>
  schema : nipada_multilingual_v361
  date : 2026-05-25
  bilingual_pairs : [{'pair': 'darwin_origin_en↔darwin_origin_de', 'label': 'Darwin Origin of Species'}, {'pair': 'manifest_en↔manifest_de', 'label': 'Marx-Engels Communist Manifesto'}]
  pair_n1s : [0.567178, 0.847026]
  mean_pair_n1 : 0.707102
  multilang_results : [{'labe
… [398 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' ../Panini/research/scripts/loi_analytique.py", "description": "Read signature generator script"}`

  ```
#!/usr/bin/env python3
"""Loi H₀′ avec la projection ANALYTIQUE (sign_analytic) — round 18.

Même protocole que la re-fondation (paires §334 officielles couvertes par les textes
ré-acquis, split hors hold-out v1), mais d_lex calculé sur les signatures analytiques
dynamiques (WordNet→supersense→E-V14→V14), au lieu du signeur lexical saturant.
Usage : PYTHONPATH=src python3 scripts/loi_analytique.py
"""
from __future__ import annotations
import json
from multiprocessing import Pool
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "nipada" / "corpus" / "_cache" / "sources"
OUT = ROOT / "nipada" / "falsification"
W = 10000
V14 = ["ÊTRE","DIFFÉRENCE","RAPPORT","ORIENTATION","SUJET","TEMPS","MODALITÉ",
       "NOMBRE","ESPACE","OPÉRATION","FONCTION","STRUCTURE","SYMÉTRIE","ÉQUATION"]
CACHE = OUT / "analytic_sigs_v1.json"


def sign_one(nid):
    p = SRC / f"{nid}.txt"
    if not p.exists(): return (nid, None)
    words = p.read_text(encoding="utf-8").split()
    if len(words) < 300: return (nid, None)
    try:
        from nipada.signing.analytical_projection import sign_analytic
        return (nid, sign_analytic(" ".join(words[:W])
… [1705 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,os\nbase='../Panini/research/nipada/falsification/'\nfor p in ['pairs334_axes_v1.json','corpus_dor_cic_v1.json','modern_corpus_sigs_v2.json','structured_sigs_v1.json','RESULTATS_FALSIFICATION_v0.3.json']:\n    try:\n        d=json.load(open(base+p))\n    e … [279 caractères tronqués]`

  ```
== pairs334_axes_v1.json <class 'dict'> ['version', 'created', 'method', 'n_pairs', 'r2_L2', 'alpha', 'vopt', 'pairs']
{"version": "v2", "created": "2026-09-08", "method": "méthode §334, signatures par entrée", "n_pairs": 655, "r2_L2": {"a": 0.8865868831832314, "b": 0.9013737063007868, "c": 0.3239867750290341, "all": 0.9091387033097759}, "alpha": 0.67, "vopt": {"direct": 0.01, "translation": 0.01, "indirect": 1.0, "other": 1.8}, "pairs": [{"section": "a", "a": "dn1_brahmajala", "b": "mn2_sabbasava", "d_topo": 3.6, "d_lex": 0.33870554623886845, "d_H": 0.6076717359284258, "cos": 0.7492899129132787, "trad_a": "BUDDHIST_AXIAL", "trad_b": "BUDDHIST_AXIAL", "lang_a": "eng", "lang_b": "eng", "same_comp": true}, {"section": "a", "a": "dn1_brahmajala", "b": "mn35_culasaccaka", "d_topo": 3.6, "d_lex": 0.25142955342124895, "d_H": 0.39816781717180877, "cos": 0.8085855379994222, "trad_a": "BUDDHIST_AXIAL", "trad_b": "BUDDHIST_AXIAL", "lang_a": "eng", "lang_b": "eng", "same_comp": true}, {"section": "a", "a": "dn1_bra

== corpus_dor_cic_v1.json <class 'dict'> ['doctrine', 'defs', 'consts', 'entrees']
{"doctrine": "corpus d'or CIC-lite : preuve + type sérialisés (de Bruijn) + empreinte + verdict 
… [4438 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -A30 -B5 \"mesure 49\\|même branche\\|30,7\\|22,0\\|15,2\" reports/07-mesures-couche-commune.md | head -100", "description": "Read measure 49 of common layer"}`

  ```
(no output)
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-familles-9.md; echo '===IE==='; sed -n '1,100p' reports/rapport-ie-sous-familles.md", "description": "Read family reports"}`

  ```
# C3.2c — les 9 familles : 7 sur 9 au-dessus de 30 %

> **Objet.** Étendre la mesure des modules par famille aux **9 familles** de 9 langues ou plus
> (C3.2c). Les 5 premières étaient mesurées ; les 4 nouvelles sont **afro-asiatic**, **quechuan**,
> **mayan** et **uralic**.

## Résultats (8 textes, contrôle 0 %)

| famille | langues | avant | après | contrôle |
|---|---:|---:|---:|---:|
| indo-européen | 98 | 0,0 % | **14,7 %** | 0,0 % |
| atlantic-congo | 74 | — | **94,0 %** | 0,0 % |
| **quechuan** | 11 | 33,3 % | **88,2 %** | 0,0 % |
| **mayan** | 9 | 8,9 % | **64,4 %** | 0,0 % |
| **afro-asiatic** | 12 | 0,0 % | **60,2 %** | 0,5 % |
| austronesian | 35 | — | **61,0 %** | 0,0 % |
| **uralic** | 9 | 31,0 % | **46,7 %** | 0,0 % |
| turkic | 14 | — | **96,1 %** | 0,0 % |
| sino-tibetan | 17 | 40,5 % | **100,0 %** | 0,0 % |

- **Moyenne des 9** : **69,5 %** ; **médiane** : **64,4 %**.
- **7 familles sur 9** dépassent **30 %** ; **1 seule** (indo-européen) est sous **30 %**.
- Le **contrôle** reste **≤ 0,5 %** partout.

## Lecture

- La **taille** n'explique pas tout : l'**indo-européen** (98 langues) est **dernier** à **14,7 %**,
  tandis que le **quechuan** (11 langues) est à **88,
… [3515 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,100p' reports/rapport-c8-inter-langue.md", "description": "Read inter-language report"}`

  ```
# C8 — transfert inter-langue : ce que le corpus multilingue dit vraiment (et le piège du corpus PARALLÈLE)

> Campagne : **cerveau** · expérience : tête entraînée sur le français, testée sur un corpus
> multilingue — puis tête entraînée dans ce corpus
> Question : après le transfert réussi à un autre corpus de français (`÷1 730`), la lecture
> apprise traverse-t-elle une **autre langue** ?
> Verdict : **deux résultats, et le second invalide la lecture naïve du premier.**
> (1) **Le transfert depuis le français échoue** : entraînée sur le corpus de campagne, la tête ne
> gagne **rien** sur un morceau multilingue (582 361,83 avant comme après — la meilleure époque
> est l'époque 0). (2) **Dans le corpus multilingue, la tête atteint 3,1005** contre 29,9154 pour
> le modèle complet… **et ce chiffre ne veut pas dire ce qu'il a l'air de dire** : le corpus est
> l'UDHR **parallèle** — le même texte traduit en une centaine de langues —, donc les morceaux
> d'entraînement et le morceau de test **portent le même contenu**. Un adaptateur linéaire ne peut
> pas battre un modèle de 24 couches sur du texte neuf ; il le « bat » ici parce que le contenu
> du test a déjà été vu, dans d'autres lang
… [4328 caractères tronqués]
  ```

- **bash** `{"command": "grep -rIn \"même branche\\|30,7\\|22,0\\|15,2\" reports/*.md | head -30", "description": "Find branch alignment numbers"}`

  ```
reports/rapport-a80-portes-ppl.md:37:la main (30,7286 des deux côtés). Pour la passer **par défaut**, il faut d'abord **épingler les
reports/rapport-b10-contraste.md:27:| 3 | 30,9 | **31,9** | 30,7 | 11,7 | 1,2 |
reports/rapport-cache-chunker.md:153:| 160 | 48 | 16 | 27,88 | 27,27 | 13,55 | 30,76 | ×1,02 | ×2,06 | ×0,91 |
reports/rapport-coherence-vision.md:41:`axes 2-3`, un **19ᵉ format lisible** (`Q4_1`, lu par la même branche que `Q4_0`)
reports/rapport-coherence-vision.md:43:clusters que **rien ne mesure** (la mesure documentée est `origine 15,2789 ·
reports/rapport-coherence-vision.md:44:clusters 15,2789`). Elle a aussi confirmé, en scannant les **28 en-têtes GGUF** du
reports/rapport-croisement-push-pull.md:107:   moteur gagne ×2,27 de bout en bout (13,6 → 30,7 tok/s, 510 jetons) à basculer
reports/rapport-cycle-entraine.md:72:| **point fixe** (somme + pénalité de convergence) | **19,42** | **22,05** | **32,02** | 52,35 | que la boucle se **pose** |
reports/rapport-cycle-entraine.md:79:  stabilise rien** — elle donne la meilleure amorce (pas 2 et 3 les plus bas : 22,05 et 32,02) et
reports/rapport-cycle-entraine.md:96:  (**43,55**), « point fixe » l'amorce (22,05 au pas 2), «
… [2814 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor p in ['reports/atomes-niveaux.json','reports/corpus-commun.json','reports/retrieval-epoque.json']:\n    d=json.load(open(p))\n    print('==',p, list(d.keys()) if isinstance(d,dict) else type(d))\nEOF", "description": "List JSON top-level keys"}`

  ```
== reports/atomes-niveaux.json ['fiche', 'version', 'date', 'titre', 'statut', 'sources', 'niveaux', 'niveaux_du_contrat', 'principe', 'atomes', 'calibration_44_oeuvres', 'protocole', 'limites', 'prochaine_etape', 'fichiers']
== reports/corpus-commun.json ['controle_negatif', 'controles', 'date', 'fiche', 'fichiers', 'intersection', 'ligne_roadmap', 'limites', 'normalisation', 'prochaine_etape', 'selection', 'sources', 'statistiques', 'statut', 'textes', 'titre', 'version']
== reports/retrieval-epoque.json ['tache', 'titre', 'date', 'methode', 'b7', 'udhr', 'bible']
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('data/udhr/genealogie.json'))\nfor k,v in list(d.items())[:5]: print(k,v)\nprint('...')\n# inspect corpus metadata\nmeta=json.load(open('data/udhr/meta.json'))\nfor k,v in list(meta.items())[:3]: print(k,v)\nEOF", "description": "Inspect  … [32 caractères tronqués]`

  ```
udhr_007.xml {'iso3': 'cri', 'nom': 'Sãotomense', 'script': 'Latn', 'famille': 'Indo-European', 'branche': 'indo1319/clas1257/ital1284/lati1262/lati1263/impe1234/roma1334/ital1285/west2813/shif1234/sout3183/west2838/gali1263/macr1272/lowe1440/bant1299/saot1242', 'niveau': 'language'}
udhr_008.xml {'iso3': 'pov', 'nom': 'Crioulo, Upper Guinea (008)', 'script': 'Latn', 'famille': 'Indo-European', 'branche': 'indo1319/clas1257/ital1284/lati1262/lati1263/impe1234/roma1334/ital1285/west2813/shif1234/sout3183/west2838/gali1263/macr1272/uppe1458', 'niveau': 'language'}
udhr_009.xml {'iso3': 'kmb', 'nom': 'Mbundu (009)', 'script': 'Latn', 'famille': 'Atlantic-Congo', 'branche': 'atla1278/volt1241/benu1247/bant1294/sout3152/narr1281/cent2260/njil1234/nort3257/mbun1247', 'niveau': 'language'}
udhr_010.xml {'iso3': 'tdt', 'nom': 'Tetun Dili', 'script': 'Latn', 'famille': 'Austronesian', 'branche': 'aust1307/mala1545/timo1265/east2894/cent2079/tetu1244', 'niveau': 'language'}
udhr_011.xml {'iso3': 'umb', 'nom': 'Umbundu (011)', 'script': 'Latn', 'famille': 'Atlantic-Congo', 'branche': 'atla1278/volt1241/benu1247/bant1294/sout3152/narr1281/cent2260/njil1234/sout3233/kune1234', 'niveau': 'langua
… [390 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '300,380p' reports/rapport-inventaire-panini.md", "description": "Read inventory section on language distance"}`

  ```
| 1 | **ÊTRE** | ∃ | 2 | existence, substrat | témoin : retrait **catastrophique** |
| 2 | **DIFFÉRENCE** | ∆ | 3 | gradient entre états | témoin : casse |
| 3 | **RAPPORT** | ∼ | 5 | relation | témoin : casse |
| 4 | **ORIENTATION** | ↗ | 7 | direction du flux | témoin : dégrade (lien H₀) |
| 5 | **SUJET** | ⊙ | 11 | agent, expérienceur | porteur modéré |
| 6 | **TEMPS** | ⧖ | 13 | durée, séquence | porteur modéré |
| 7 | **MODALITÉ** | ◇ | 17 | possible / nécessaire (Ł3) | spéculatif |
| 8 | **NOMBRE** | № | 19 | quantité, cardinalité | faible (candidat au retrait) |
| 9 | **ESPACE** | ⊕ | 23 | localisation, métaphore | porteur modéré |
| 10 | **OPÉRATION** | ⊗ | 29 | action, acte (les dhātus ACT) | témoin : casse |
| 11 | **FONCTION** | λ | 31 | finalité, usage | spéculatif |
| 12 | **STRUCTURE** | ⊞ | 37 | organisation, agencement | porteur modéré |
| 13 | **SYMÉTRIE** | ≍ | 41 | symétrie, équilibre | **meilleur candidat au retrait** |
| 14 | **ÉQUATION** | ≡ | 43 | égalité, équivalence | faible en philo, fort en technique |

**Sont-ils utilisables par Drave ? Oui, à trois conditions.**

1. **En lecture directe** : `analytic_sigs_v1.json` est un `{texte: {14 flottants}}` pur, s
… [5743 caractères tronqués]
  ```

- **bash** `{"command": "grep -rIn \"lang_distance\" tools data ../Panini/research --include=*.py 2>/dev/null | head -20", "description": "Locate lang_distance implementation"}`

  ```
../Panini/research/src/nipada/signing/language_genealogy.py:6:  - lang_distance(l1, l2): normalized distance [0,1]
../Panini/research/src/nipada/signing/language_genealogy.py:35:  lang_distance(l1, l2) scoring:
../Panini/research/src/nipada/signing/language_genealogy.py:254:def lang_distance(lang1: str, lang2: str) -> float:
../Panini/research/src/nipada/signing/language_genealogy.py:290:        (avail, lang_distance(lang, avail))
../Panini/research/tests/signing/test_language_genealogy.py:10:    lang_distance,
../Panini/research/tests/signing/test_language_genealogy.py:80:            assert lang_distance(lang, lang) == 0.0
../Panini/research/tests/signing/test_language_genealogy.py:84:        d = lang_distance("eng", "deu")
../Panini/research/tests/signing/test_language_genealogy.py:89:        d = lang_distance("fra", "deu")
../Panini/research/tests/signing/test_language_genealogy.py:94:        d = lang_distance("eng", "lzh")
../Panini/research/tests/signing/test_language_genealogy.py:98:        assert lang_distance("eng", "xyz") == 1.00
../Panini/research/tests/signing/test_language_genealogy.py:99:        assert lang_distance("xyz", "abc") == 1.00
../Panini/research/tests/signin
… [198 caractères tronqués]
  ```

- **bash** `{"command": "grep -rIn \"0,15\\|0.15\\|same_comp\\|d_topo\" reports/rapport-inventaire-panini.md | head -20", "description": "Find distance convention context"}`

  ```
337:| **Distance** | même fichier, `lang_distance(l1,l2)` | 0 même langue / 0,15 même branche / 0,40 même famille / 0,75 familles différentes / 1,00 inconnu | fonction |
382:  `d_topo`, `d_lex`, `d_H`, `cos`, `trad_*`, `lang_*` : une table prête pour un test de retrieval.
394:| Paires §334 | `nipada/falsification/pairs334_axes_v1.json` | 655 objets `{a,b,d_topo,d_lex,d_H,cos,trad,lang}` | aucune | **haute** |
  ```

- **bash** `{"command": "ls -la ../Panini/research/data/ | grep -i -E 'udhr|v14|decompos|converg' ; echo '---'; ls -la ../Panini/research/data/udhr* 2>/dev/null", "description": "Find Panini UDHR decomposition files"}`

  ```
-rw-r--r--. 1 stephane stephane     5604  2 jui 11:18 author_v14_profiles.json
-rw-r--r--. 1 stephane stephane   932627  3 aoû 16:46 udhr_article1_en.json
-rw-r--r--. 1 stephane stephane  1058726  3 aoû 16:46 udhr_article1_fr.json
-rw-r--r--. 1 stephane stephane     4705  5 aoû 14:04 udhr_convergence_graph.json
-rw-r--r--. 1 stephane stephane     6045  5 aoû 14:03 udhr_convergence_v14.json
-rw-r--r--. 1 stephane stephane   235085  4 aoû 10:26 udhr_corpus.json
-rw-r--r--. 1 stephane stephane     2409  5 aoû 14:03 udhr_decomposed_v14.json
-rw-r--r--. 1 stephane stephane    12632  3 aoû 14:52 udhr_demo.nipada
-rw-r--r--. 1 stephane stephane     1521  5 aoû 14:10 udhr_omw_coverage.json
-rw-r--r--. 1 stephane stephane      533  5 aoû 14:13 udhr_reconstruction_full.json
-rw-r--r--. 1 stephane stephane      368  5 aoû 14:09 udhr_reconstruction_report.json
-rw-r--r--. 1 stephane stephane    12508  5 aoû 14:05 udhr_universal_graph.json
-rw-r--r--. 1 stephane stephane  3869584  4 jui 13:04 v14_lexicon_enriched.json
-rwxr-xr-x. 1 stephane stephane        0  4 jui 12:52 v14_lexicon_enriched.json.lock
---
-rw-r--r--. 1 stephane stephane  932627  3 aoû 16:46 ../Panini/research/data/udhr_article1
… [1024 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,os\nfor p in ['../Panini/research/data/udhr_decomposed_v14.json','../Panini/research/data/udhr_convergence_v14.json']:\n    if not os.path.exists(p): print('MISSING',p); continue\n    print('==',p,os.path.getsize(p))\n    d=json.load(open(p))\n    print(ty … [168 caractères tronqués]`

  ```
== ../Panini/research/data/udhr_decomposed_v14.json 2409
<class 'dict'> ['total_languages_processed', 'results']
{"total_languages_processed": 11, "results": {"bul": {"name": "Bulgarian", "family": "Indo-European", "branch": "Slavic", "tradition": "western_modern", "tokens": 29, "found": 1, "coverage": 0.034482758620689655}, "cat": {"name": "Catalan", "family": "Indo-European", "branch": "Romance", "tradition": "western_modern", "tokens": 30, "found": 16, "coverage": 0.5333333333333333}, "dan": {"name": "Danish", "family": "Indo-European", "branch": "Germanic", "tradition": "western_modern", "tokens": 28, "found": 11, "coverage": 0.39285714285714285}, "eng": {"name": "English", "family": "Indo-European", "branch": "Germanic", "tradition": "western_modern", "tokens": 30, "found": 21, "coverage": 0.7}, "fra": {"name": "French", "family": "Indo-European", "branch": "Romance", "tradition": "western_modern", "tokens": 34, "found": 10, "coverage": 0.29411764705882354}, "ind": {"name": "Indonesian", "family": "Austronesian", "branch": "Malayo-Polynesian", "tradition": "southeast_asian", "tokens": 26, "found": 3, "coverage": 0.11538461538461539}, "ita": {"name": "Italian", "family": "Indo-
… [1416 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('../Panini/research/data/udhr_corpus.json'))\nprint(type(d), len(d))\nif isinstance(d,dict):\n    k=list(d)[:3]; print(k)\n    for kk in k: print(kk, json.dumps(d[kk],ensure_ascii=False)[:500])\nelse:\n    print(json.dumps(d[0],ensure_asc … [77 caractères tronqués]`

  ```
<class 'dict'> 6
['format', 'source', 'article']
format "udhr-v2.0-xml"
source "eric-muller/udhr (GitHub) — Unicode UDHR XML Project"
article "Article 1"
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('../Panini/research/data/udhr_corpus.json'))\nprint(d.keys())\nfor k,v in d.items():\n    print('--',k,type(v), len(v) if hasattr(v,'__len__') else '')\n    if isinstance(v,list): print(json.dumps(v[0],ensure_ascii=False)[:600])\n    elif … [189 caractères tronqués]`

  ```
dict_keys(['format', 'source', 'article', 'total_languages', 'families', 'languages'])
-- format <class 'str'> 13
udhr-v2.0-xml
-- source <class 'str'> 52
eric-muller/udhr (GitHub) — Unicode UDHR XML Project
-- article <class 'str'> 9
Article 1
-- total_languages <class 'int'> 
532
-- families <class 'dict'> 10
{"Other": {"count": 503, "branches": ["Unknown"]}, "Indo-European": {"count": 17, "branches": ["Germanic", "Indo-Iranian", "Italic", "Romance", "Slavic"]}, "Afro-Asiatic": {"count": 2, "branches": ["Semitic"]}}
-- languages <class 'dict'> 532
{"007": {"name": "Sãotomense", "iso": "007", "script": "Latn", "dir": "ltr", "text": "Tudu nguê di mundu ca nancê livli e igual ni dignidade e ni dirêtu. Punda nen ca pensá e nen tê cunxensa, selá nen fé tudu cuá cu tençón de lumón.", "family": "Other", "branch": "Unknown", "tradition": "other"}, "008": {"name": "Crioulo, Upper Guinea (008)", "iso": "008", "script": "Latn", "dir": "ltr", "text": "Tudu pecadur padidu livre, ninguin ca más ninguin, tudu djusta, tudu tem mesmu diritu. Tudu quin qui padidu, tem si roçon, cu si manera di pensa. Na metadi di utrus I díbidi fassi cussas cu ermondadi.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('../Panini/research/data/udhr_corpus.json'))['languages']\nmeta=json.load(open('data/udhr/meta.json'))\ng=json.load(open('data/udhr/genealogie.json'))\nsel=json.load(open('reports/corpus-commun.json'))['textes']\nprint('n selection',len(s … [214 caractères tronqués]`

  ```
n selection 21
{'branche': 'indo1319/clas1257/germ1287/nort3152/west2793/nort3175/angl1264/angl1265/late1254/merc1242/macr1271', 'branche_feuille': 'macr1271', 'branche_panini': 'Germanic', 'drave_fichier': 'udhr_eng.xml', 'epoque': 1948, 'epoque_label': '1948 — adoption de la DUDH', 'epoque_note': "date de l'œuvre ; date de la traduction non documentée", 'famille': 'Indo-European', 'famille_panini': 'Indo-European', 'genre': 'declaration', 'id': 'udhr_eng', 'iso3': 'eng', 'langue': 'English', 'nb_caracteres': 170, 'nb_mots_ws': 30, 'nb_phrases': 2, 'niveau_glottolog': 'language', 'panini_cle': 'eng', 'phrases': ['All human beings are born free and equal in dignity and rights.', 'They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.'], 'role': 'strate', 'script': 'Latn', 'sens': 'ltr', 'sha256_fichier': '95b7af97d4eca78cf41422a4366078d5ba4f981d24357e039f7d56bf9cb3c1c1', 'sha256_source_drave': 'a2ccb5fb55a20f5d5db80ecf01a1e24803441a328040261fd07466369b09a345', 'sha256_source_panini': 'a2ccb5fb55a20f5d5db80ecf01a1e24803441a328040261fd07466369b09a345', 'tradition_panini': 'western_modern'}
udhr_eng
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nsel=json.load(open('reports/corpus-commun.json'))['textes']\nfrom collections import Counter\nprint(f\"{'id':22s} {'script':5s} {'panini_fam':18s} {'panini_br':20s} {'glotto_fam':18s} leaf\")\nfor t in sel:\n    print(f\"{t['id']:22s} {t['script']:5s} {t[ … [331 caractères tronqués]`

  ```
id                     script panini_fam         panini_br            glotto_fam         leaf
udhr_eng               Latn  Indo-European      Germanic             Indo-European      macr1271
udhr_hin               Deva  Indo-European      Indo-Iranian         Indo-European      hind1270
udhr_bel               Cyrl  Indo-European      Slavic               Indo-European      east1426
udhr_ell_monotonic     Grek  Indo-European      Hellenic             Indo-European      nucl1783
udhr_kin               Latn  Niger-Congo        Bantu                Atlantic-Congo     rwan1241
udhr_ewe               Latn  Other              Unknown              Atlantic-Congo     ewei1234
udhr_ibo               Latn  Niger-Congo        Volta-Niger          Atlantic-Congo     cent2417
udhr_fuf_adlm          Adlm  Other              Unknown              Atlantic-Congo     fula1264
udhr_ind               Latn  Austronesian       Malayo-Polynesian    Austronesian       stan1327
udhr_tgl               Latn  Austronesian       Malayo-Polynesian    Austronesian       taga1269
udhr_mly_arab          Arab  Other              Unknown              Austronesian       sing1270
udhr_jav               Latn  Austronesi
… [1707 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-epoque.json'))['udhr']\nprint(d.keys())\nfor k,v in d.items():\n    print('--',k,type(v), len(v) if hasattr(v,'__len__') else '')\n    print(json.dumps(v,ensure_ascii=False)[:700])\nEOF", "description": "Inspect UDHR re … [24 caractères tronqués]`

  ```
dict_keys(['n_langues', 'n_articles', 'epoque', 'meta_langues', 'agregats', 'regression', 'controles', 'paires'])
-- n_langues <class 'int'> 
21
-- n_articles <class 'int'> 
30
-- epoque <class 'int'> 
1948
-- meta_langues <class 'dict'> 21
{"udhr_amh": {"iso3": "amh", "nom": "Amharic", "script": "Ethi", "sens": "ltr", "variante": "amh", "nb_articles": 30, "famille": "Afro-Asiatic", "branche": "afro1255/semi1276/west2786/ethi1244/sout3078/amha1244", "epoque": 1948}, "udhr_arb": {"iso3": "arb", "nom": "Arabic, Standard", "script": "Arab", "sens": "rtl", "variante": "arb", "nb_articles": 30, "famille": "Afro-Asiatic", "branche": "afro1255/semi1276/west2786/cent2236/arab1394/arab1395", "epoque": 1948}, "udhr_bel": {"iso3": "bel", "nom": "Belarusan", "script": "Cyrl", "sens": "ltr", "variante": "bel", "nb_articles": 30, "famille": "Indo-European", "branche": "indo1319/clas1257/balt1263/slav1255/east1426", "epoque": 1948}, "udhr_cmn
-- agregats <class 'dict'> 9
{"toutes": {"n_paires": 420, "top1_moyen": 0.049444444444444444, "top1_median": 0.03333333333333333, "ic_bas": 0.0, "ic_haut": 0.18416666666666592}, "script_meme": {"n_paires": 112, "top1_moyen": 0.09375, "top1_median": 0.05, "ic
… [1891 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor p in ['nipada_v150_validation.json','nipada_v174_loo_traditions.json','nipada_v222_falsification.json']:\n    d=json.load(open('../Panini/research/nipada/falsification/'+p))\n    print('==',p,type(d), list(d.keys())[:12] if isinstance(d,dict) else len … [139 caractères tronqués]`

  ```
== nipada_v150_validation.json <class 'dict'> ['version', 'step', 'H1_stratification', 'H2_loocv_tradition', 'H3_ols_regression', 'verdict']
{"version": "v150", "step": "§150 — validation prédictive Phase B révisée (composite)", "H1_stratification": {"median_d_graph": 0.6694, "n_strong_transmission": 17, "n_weak_transmission": 12, "mean_dsig_strong": 0.3403, "mean_dsig_weak": 0.3727, "expected": "mean_dsig_strong < mean_dsig_weak (signature plus proche si héritage fort)", "u_stat": 94.0, "p_value_two_tailed": 0.7232, "verdict": "KO"}, "H2_loocv_tradition": {"baseline_majority_acc": 0.3, "acc_full_signature": 0.4, "acc_reflexion_signature": 0.2, "delta_full_vs_baseline": 0.1, "delta_refl_vs_baseline": -0.1, "delta_refl_vs_full": -0.2, "verdict": "KO", "loocv_full": {"accuracy": 0.4, "n": 10, "n_correct": 4, "confusion": {"GRECO_LAT_MATERIAL": {"GRECO_LAT_MATERIAL": 2, "CHINESE_MATERIAL": 1}, "SCEPT": {"ISLAMIC_RATIONALIST": 1}, "INDIAN_MATERIAL": {"CHINESE_MATERIAL": 1}, "CHINESE_MATERIAL": {"INDIAN_MATERIAL": 1}, "ISLAMIC_RATIONALIST": {"SCEPT": 1}, "MODERN_WESTERN": {"INDIAN_MATERIAL": 1, "MODERN_WESTERN": 2}}, "detail": [{"work": "democritus_fragments", "true": "GRECO_LAT_MATERIA
… [2069 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('../Panini/research/nipada/falsification/pairs334_axes_v1.json'))\nps=d['pairs']\nprint(len(ps), ps[0].keys())\nimport collections\nprint('lang_a',collections.Counter(p.get('lang_a') for p in ps).most_common(10))\nprint('trad_a',collectio … [402 caractères tronqués]`

  ```
655 dict_keys(['section', 'a', 'b', 'd_topo', 'd_lex', 'd_H', 'cos', 'trad_a', 'trad_b', 'lang_a', 'lang_b', 'same_comp'])
lang_a [('eng', 408), ('', 245), ('fra', 2)]
trad_a [('', 199), ('BUDDHIST_AXIAL', 107), ('GRECO_PLATONIC', 56), ('FUZZY_LOGIC', 35), ('MANY_VALUED_LOGIC', 34), ('RECURSIVE_FUNCTIONS', 33), ('COMBINATORY_LOGIC', 32), ('SEMANTIC_NETWORKS', 31), ('CONCEPTUAL_DEPENDENCY', 30), ('INDIAN_AXIAL', 26)]
sections Counter({'a': 459, 'b': 180, 'c': 16})
d_topo vals [0.0, 0.01, 0.02, 0.03, 0.04, 1.0, 1.01, 1.02, 1.03, 1.04, 1.05, 1.8, 1.81, 2.0, 2.8, 2.8099999999999996, 2.8199999999999994, 2.829999999999999, 2.839999999999999, 3.6]
d_lex range 0.008792229443804334 0.6947086733314612
d_H range 0.017181860755894656 1.2832753957116763
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('../Panini/research/nipada/falsification/nipada_v150_validation.json'))\nprint(json.dumps(d['H3_ols_regression'],ensure_ascii=False,indent=2))\nprint(json.dumps(d['verdict'],ensure_ascii=False,indent=2))\nEOF", "description": "Print Panin … [17 caractères tronqués]`

  ```
{
  "features": [
    "intercept",
    "d_graph",
    "dyear_per_1000y",
    "same_tradition"
  ],
  "ols_dsig": {
    "beta": [
      0.1594,
      0.0489,
      0.1378,
      0.0022
    ],
    "r2": 0.3004
  },
  "ols_drefl": {
    "beta": [
      0.7014,
      -0.0279,
      -0.0365,
      -0.1114
    ],
    "r2": 0.0128
  },
  "interpretation_dsig": "d_sig ≈ +0.159 +0.049·d_graph +0.138·(Δyear/1000) +0.002·same_trad  (R²=0.300)",
  "verdict": "OK"
}
{
  "H1_strong_vs_weak_transmission": "KO",
  "H2_loocv_tradition": "KO",
  "H3_ols_regression": "OK",
  "go_no_go_phase_religieuse": "NO-GO",
  "rationale": "Phase religieuse §151+ SUSPENDUE — la signature V14 (binaire ou fréquentielle) ne reproduit pas suffisamment le graphe d'héritage. Cela ne réfute pas V14 en soi, mais exige soit (a) un extracteur sémantique au-delà du lexical (embeddings, parseurs philosophiques), soit (b) un corpus avec ≥ 20 fragments par auteur."
}
  ```

- **bash** `{"command": "sed -n '240,300p' ../Panini/research/src/nipada/signing/language_genealogy.py; echo '---TREE---'; grep -n \"LANG_TREE\" ../Panini/research/src/nipada/signing/language_genealogy.py | head", "description": "Read lang_distance and tree"}`

  ```
# ---------------------------------------------------------------------------
# Distance matrix
# ---------------------------------------------------------------------------

# Distance by (family, branch) relationship
_DISTANCE_SAME_LANG: float = 0.00
_DISTANCE_SAME_BRANCH: float = 0.15
_DISTANCE_SAME_FAMILY: float = 0.40
_DISTANCE_DIFF_FAMILY: float = 0.75
_DISTANCE_UNKNOWN: float = 1.00


def lang_distance(lang1: str, lang2: str) -> float:
    """Normalized linguistic distance between two language codes.

    Returns:
        0.00 — same language
        0.15 — same branch (e.g. French ↔ Italian)
        0.40 — same family (e.g. French ↔ German — both Indo-European)
        0.75 — different families (e.g. French ↔ Arabic)
        1.00 — one or both unknown
    """
    if lang1 == lang2:
        return _DISTANCE_SAME_LANG
    info1 = LANG_TREE.get(lang1)
    info2 = LANG_TREE.get(lang2)
    if info1 is None or info2 is None:
        return _DISTANCE_UNKNOWN
    if info1.family != info2.family:
        return _DISTANCE_DIFF_FAMILY
    if info1.branch == info2.branch:
        return _DISTANCE_SAME_BRANCH
    return _DISTANCE_SAME_FAMILY


def get_closest_known_langs(lang: str, avai
… [1232 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport numpy, scipy, sklearn\nprint('numpy',numpy.__version__,'scipy',scipy.__version__,'sklearn',sklearn.__version__)\nEOF", "description": "Check scientific Python stack"}`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'sklearn'
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport numpy, scipy\nprint('numpy',numpy.__version__,'scipy',scipy.__version__)\nEOF", "description": "Check numpy and scipy"}`

  ```
numpy 2.5.3 scipy 1.18.1
  ```

- **bash** `{"command": "mkdir -p work/j32 && cat > work/j32/explore.py <<'PY'\nimport json, itertools, math\nimport numpy as np\nfrom scipy import stats\n\nbase='.'\nsel=json.load(open('reports/corpus-commun.json'))['textes']\nret=json.load(open('reports/retrieval-epoque.json'))['udhr']\nids=[t['id'] for t in  … [2149 caractères tronqués]`

  ```
pairs 210 ordered 420
('udhr_amh', 'udhr_arb') [0.13316623769734637, 0.13316623769734637]
('udhr_amh', 'udhr_bel') [0.13316623769734637, 0.13316623769734637]

Panini family counts {'Austronesian': 3, 'Niger-Congo': 2, 'Afro-Asiatic': 3, 'Sino-Tibetan': 2, 'Indo-European': 5, 'Other': 6}
Panini branch counts {'Semitic': 2, 'Chadic': 1, 'Indo-Iranian': 1, 'Slavic': 1, 'Malayo-Polynesian': 3, 'Bantu': 1, 'Hellenic': 1, 'Unknown': 6, 'Tibeto-Burman': 1, 'Romance': 1, 'Volta-Niger': 1, 'Sinitic': 1, 'Germanic': 1}
labeled 15 ['udhr_eng', 'udhr_hin', 'udhr_bel', 'udhr_ell_monotonic', 'udhr_kin', 'udhr_ibo', 'udhr_ind', 'udhr_tgl', 'udhr_jav', 'udhr_mya', 'udhr_cmn_hant', 'udhr_amh', 'udhr_heb', 'udhr_hau_NE', 'udhr_fra']
udhr_eng           panini Indo-European  /Germanic             glotto Indo-European    indo1319/clas1257/germ1287/nort3152/west2793/nort3175/angl1264/angl1265/late1254/merc1242/macr1271
udhr_hin           panini Indo-European  /Indo-Iranian         glotto Indo-European    indo1319/clas1257/indo1320/indo1321/midd1375/cont1248/midl1245/shau1239/indo1322/west2812/hind1270
udhr_bel           panini Indo-European  /Slavic               glotto Indo-European    indo1319/clas125
… [1891 caractères tronqués]
  ```

- **bash** `{"command": "cat >> work/j32/explore.py <<'PY'\n\n# Distribution and group means\nprint('\\nMRR unique', len(set(np.round(mrr[np.triu_indices(21,1)],6))))\nfor name,M in [('MRR',mrr)]:\n    print(name,'min',M[np.triu_indices(21,1)].min(),'max',M[np.triu_indices(21,1)].max(),'mean',M[np.triu_indices( … [1954 caractères tronqués]`

  ```
MRR min 0.10482049827147305 max 0.9515476190476191 mean 0.1509748095221739

 Panini distance
  d=0.150 n=  4 MRR=0.3589 top1?
  d=0.400 n= 14 MRR=0.1915 top1?
  d=0.750 n= 87 MRR=0.1481 top1?
  d=1.000 n=105 MRR=0.1401 top1?

Glottolog distance
  d= 0.20 n=  1 MRR=0.1332
  d= 0.45 n=  1 MRR=0.1332
  d= 0.60 n=  2 MRR=0.2394
  d= 0.64 n=  1 MRR=0.1332
  d= 0.75 n=  1 MRR=0.1311
  d= 0.78 n=  3 MRR=0.4094
  d= 0.80 n=  3 MRR=0.1780
  d= 0.83 n=  1 MRR=0.1332
  d= 0.86 n=  2 MRR=0.1332
  d= 0.88 n=  1 MRR=0.1585
  d= 0.89 n=  3 MRR=0.1332
  d= 0.90 n=  1 MRR=0.1332
  d= 0.91 n=  1 MRR=0.1332
  d= 0.92 n=  2 MRR=0.5424
  d= 1.00 n= 11 MRR=0.1332
  d= 1.08 n=  1 MRR=0.1328
  d= 1.10 n= 14 MRR=0.1613
  d= 1.11 n=  4 MRR=0.1823
  d= 1.12 n= 14 MRR=0.1390
  d= 1.13 n= 23 MRR=0.1486
  d= 1.14 n=  6 MRR=0.1646
  d= 1.15 n= 12 MRR=0.1332
  d= 1.17 n=  3 MRR=0.1332
  d= 1.18 n= 16 MRR=0.1332
  d= 1.20 n= 42 MRR=0.1391
  d= 1.22 n= 27 MRR=0.1422
  d= 1.25 n= 11 MRR=0.1345
  d= 1.29 n=  3 MRR=0.1332
same script
   True 56 0.1999
   False 154 0.1332
same glotto family
   True 34 0.1925
   False 176 0.143
same panini family (labelled)
   True 18 0.2287
   False 192 0.1437

labeled pairs 105
panini
… [190 caractères tronqués]
  ```

- **bash** `{"command": "cat > work/j32/explore2.py <<'PY'\nimport json, itertools, math\nimport numpy as np\nfrom scipy import stats\n\nsel=json.load(open('reports/corpus-commun.json'))['textes']\nret=json.load(open('reports/retrieval-epoque.json'))['udhr']\nids=[t['id'] for t in sel]; idx={x:i for i,x in enum … [4072 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/j32/explore2.py", line 39, in <module>
    labeled=np.array([a['famille_panini']!='Other' and b['famille_panini']!='Other' for a,b in pairs])
                      ~^^^^^^^^^^^^^^^^^^
TypeError: 'int' object is not subscriptable
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re\np='work/j32/explore2.py'\ns=open(p).read()\ns=s.replace(\"labeled=np.array([a['famille_panini']!='Other' and b['famille_panini']!='Other' for a,b in pairs])\",\n            \"labeled=np.array([sel[a]['famille_panini']!='Other' and sel[b]['famille_panini']!=' … [281 caractères tronqués]`

  ```
n pairs 210 labeled 105
spearman pan-glotto all SignificanceResult(statistic=np.float64(0.3094056106668597), pvalue=np.float64(4.887015019515832e-06))
spearman pan-glotto labeled SignificanceResult(statistic=np.float64(0.6567319679304343), pvalue=np.float64(2.8079707377579747e-14))
pearson pan-glotto labeled PearsonRResult(statistic=np.float64(0.9181587261283043), pvalue=np.float64(3.29165402400434e-43))
spearman MRR pan all SignificanceResult(statistic=np.float64(-0.03307323534111793), pvalue=np.float64(0.6336851332282833))
spearman MRR glo all SignificanceResult(statistic=np.float64(-0.04936207062027425), pvalue=np.float64(0.47678148079955657))
spearman MRR pan labeled SignificanceResult(statistic=np.float64(-0.05939263991491333), pvalue=np.float64(0.5472806789219654))
spearman MRR glo labeled SignificanceResult(statistic=np.float64(-0.10043391620813341), pvalue=np.float64(0.3080120043866734))

== OLS all n 210
  script             R2=0.1228 AIC=-1062.5 b=[0.1332 0.0668] p=[0. 0.]
  script+pan         R2=0.1980 AIC=-1079.3 b=[ 0.2331  0.0652 -0.1184] p=[0. 0. 0.]
  script+glo         R2=0.1638 AIC=-1070.5 b=[ 0.2638  0.0651 -0.1161] p=[0.     0.     0.0017]
  script+pan+glo     R
… [2368 caractères tronqués]
  ```

- **bash** `{"command": "cat > work/j32/explore3.py <<'PY'\nimport json, numpy as np\nfrom scipy import stats\nV14=[\"ÊTRE\",\"DIFFÉRENCE\",\"RAPPORT\",\"ORIENTATION\",\"SUJET\",\"TEMPS\",\"MODALITÉ\",\"NOMBRE\",\"ESPACE\",\"OPÉRATION\",\"FONCTION\",\"STRUCTURE\",\"SYMÉTRIE\",\"ÉQUATION\"]\nsigs=json.load(open( … [2065 caractères tronqués]`

  ```
n (44, 14)
eigenvalues [1.499e+00 5.600e-01 3.150e-01 2.220e-01 9.800e-02 7.600e-02 2.900e-02
 1.900e-02 1.500e-02 8.000e-03 5.000e-03 2.000e-03 1.000e-03 0.000e+00]
var ratio [5.263e-01 1.967e-01 1.104e-01 7.790e-02 3.440e-02 2.670e-02 1.030e-02
 6.600e-03 5.100e-03 2.700e-03 1.900e-03 7.000e-04 2.000e-04 0.000e+00]
cum [0.5263 0.723  0.8334 0.9114 0.9458 0.9724 0.9828 0.9893 0.9945 0.9972
 0.9991 0.9998 1.     1.    ]
n >1 1
perm n>1 mean 0.0 pct [0. 0. 0.]
perm var3 mean 0.4822170638644803 pct [0.45193454 0.48229338 0.51548531] observed 0.8334365978869643
split-half cos PC1 mean 0.8758272085160932 pct [0.32377324 0.95699255 0.99451322]
split-half subspace3 overlap mean 0.6363029658615285 pct [0.48095233 0.64085969 0.74845716]
PC 1 var 0.526 [('MODALITÉ', np.float64(0.51)), ('RAPPORT', np.float64(-0.43)), ('FONCTION', np.float64(-0.3)), ('ORIENTATION', np.float64(0.29)), ('ESPACE', np.float64(0.28)), ('DIFFÉRENCE', np.float64(0.28))]
PC 2 var 0.197 [('ÉQUATION', np.float64(-0.59)), ('SYMÉTRIE', np.float64(0.44)), ('NOMBRE', np.float64(-0.33)), ('TEMPS', np.float64(0.32)), ('ESPACE', np.float64(-0.28)), ('MODALITÉ', np.float64(0.27))]
PC 3 var 0.11 [('SYMÉTRIE', np.float64(-0.75))
… [373 caractères tronqués]
  ```

- **bash** `{"command": "cat > work/j32/explore3b.py <<'PY'\nimport json, numpy as np\nV14=[\"ÊTRE\",\"DIFFÉRENCE\",\"RAPPORT\",\"ORIENTATION\",\"SUJET\",\"TEMPS\",\"MODALITÉ\",\"NOMBRE\",\"ESPACE\",\"OPÉRATION\",\"FONCTION\",\"STRUCTURE\",\"SYMÉTRIE\",\"ÉQUATION\"]\nsigs=json.load(open('../Panini/research/nipa … [770 caractères tronqués]`

  ```
raw eigen [6.147e+00 3.319e+00 1.400e+00 9.800e-01 7.240e-01 5.460e-01 4.280e-01
 1.750e-01 1.350e-01 1.140e-01 1.900e-02 9.000e-03 4.000e-03 0.000e+00] cum [0.439  0.6761 0.7761 0.8461 0.8978 0.9368 0.9674 0.9799 0.9895 0.9977
 0.999  0.9997 1.     1.    ] n>1 3
 PC 1 [('RAPPORT', np.float64(0.39)), ('ÊTRE', np.float64(-0.35)), ('ESPACE', np.float64(-0.34)), ('DIFFÉRENCE', np.float64(-0.33)), ('MODALITÉ', np.float64(-0.32))]
 PC 2 [('NOMBRE', np.float64(0.5)), ('ÉQUATION', np.float64(0.5)), ('SUJET', np.float64(-0.41)), ('TEMPS', np.float64(-0.33)), ('OPÉRATION', np.float64(-0.28))]
 PC 3 [('SYMÉTRIE', np.float64(-0.47)), ('ORIENTATION', np.float64(0.45)), ('STRUCTURE', np.float64(0.37)), ('FONCTION', np.float64(0.37)), ('ESPACE', np.float64(0.3))]
 PC 4 [('OPÉRATION', np.float64(0.69)), ('ÊTRE', np.float64(-0.4)), ('MODALITÉ', np.float64(0.39)), ('SYMÉTRIE', np.float64(-0.24)), ('DIFFÉRENCE', np.float64(-0.19))]
clr eigen [ 6.967e+00  2.845e+00  1.491e+00  1.260e+00  5.280e-01  3.810e-01
  2.070e-01  1.400e-01  8.400e-02  4.700e-02  3.200e-02  1.300e-02
  5.000e-03 -0.000e+00] cum [0.4976 0.7008 0.8073 0.8973 0.9351 0.9623 0.977  0.9871 0.9931 0.9964
 0.9987 0.9996 1.     1.    ]
… [676 caractères tronqués]
  ```

- **bash** `{"command": "cat > work/j32/explore3c.py <<'PY'\nimport json, numpy as np\nV14=[\"ÊTRE\",\"DIFFÉRENCE\",\"RAPPORT\",\"ORIENTATION\",\"SUJET\",\"TEMPS\",\"MODALITÉ\",\"NOMBRE\",\"ESPACE\",\"OPÉRATION\",\"FONCTION\",\"STRUCTURE\",\"SYMÉTRIE\",\"ÉQUATION\"]\nsigs=json.load(open('../Panini/research/nipa … [1882 caractères tronqués]`

  ```
eigen [ 6.9668e+00  2.8449e+00  1.4911e+00  1.2596e+00  5.2850e-01  3.8070e-01
  2.0680e-01  1.4040e-01  8.4000e-02  4.7000e-02  3.2100e-02  1.2700e-02
  5.4000e-03 -0.0000e+00]
cum [0.4976 0.7008 0.8073 0.8973 0.9351 0.9623 0.977  0.9871 0.9931 0.9964
 0.9987 0.9996 1.     1.    ]
n>1 4
components for 0.5 2
components for 0.8 3
components for 0.9 5
components for 0.95 6
split cos1 mean/pct 0.9253646489814714 [0.2079582  0.97665348 0.99299696]
split sub3 mean/pct 0.6131980592746533 [0.49411832 0.6178518  0.70675283]
split n>1 dist [  0   0  12 644 341   3]
perm n>1 mean 6.266 dist [  0   0   0   0   0  60 619 316   5]
perm var3 mean/pct 0.39175198503809283 [0.3589208  0.39153327 0.42450578] obs 0.80734335194426
PC 1 eig 6.967 [('RAPPORT', np.float64(0.36)), ('SUJET', np.float64(0.34)), ('FONCTION', np.float64(0.34)), ('STRUCTURE', np.float64(0.33)), ('ESPACE', np.float64(-0.32)), ('DIFFÉRENCE', np.float64(-0.31))]
PC 2 eig 2.845 [('OPÉRATION', np.float64(0.48)), ('NOMBRE', np.float64(-0.47)), ('ÉQUATION', np.float64(-0.47)), ('TEMPS', np.float64(0.27)), ('MODALITÉ', np.float64(0.26)), ('SYMÉTRIE', np.float64(0.22))]
PC 3 eig 1.491 [('ÊTRE', np.float64(0.69)), ('OPÉRATION', np.float
… [563 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,re\n# Panini UDHR labels\np=json.load(open('../Panini/research/data/udhr_corpus.json'))\nlangs=p['languages']\nfrom collections import Counter\nfam=Counter(v['family'] for v in langs.values())\nprint('UDHR 532 families',fam)\nknown=[k for k,v in langs.items … [1173 caractères tronqués]`

  ```
UDHR 532 families Counter({'Other': 421, 'Indo-European': 53, 'Sino-Tibetan': 11, 'Niger-Congo': 9, 'Afro-Asiatic': 8, 'Austronesian': 7, 'Dravidian': 6, 'Uralic': 3, 'Japonic': 3, 'Turkic': 3, 'Austroasiatic': 3, 'Tai-Kadai': 2, 'Isolate': 1, 'Kartvelian': 1, 'Koreanic': 1})
known family 111 unknown 421
branches Counter({'Romance': 15, 'Slavic': 11, 'Germanic': 9, 'Indo-Iranian': 9, 'Sinitic': 9, 'Malayo-Polynesian': 7, 'Southern': 6, 'Bantu': 6, 'Semitic': 4, 'Chadic': 3, 'Japanese': 3, 'Tibeto-Burman': 2, 'Celtic': 2, 'Hellenic': 2, 'Finnic': 2, 'Volta-Niger': 2, 'Kipchak': 2, 'Tai': 2, 'Italic': 2, 'Baltic': 2, 'Vietic': 2, 'Basque': 1, 'Ugric': 1, 'Armenian': 1, 'Georgian': 1, 'Khmer': 1, 'Korean': 1, 'Cushitic': 1, 'Oghuz': 1, 'Atlantic': 1})
known keys ['afr', 'amh', 'ast', 'bel', 'ben', 'bod', 'bul', 'cat', 'ces', 'cmn_hans', 'cmn_hans_beijing', 'cmn_hans_guiyang', 'cmn_hans_harbin', 'cmn_hans_nanjing', 'cmn_hans_tianjin', 'cmn_hant', 'cym', 'dan', 'deu_1901', 'deu_1996', 'ell_monotonic', 'ell_polytonic', 'eng', 'est', 'eus', 'fin', 'fra', 'gle', 'glg', 'guj', 'hau_3', 'hau_NE', 'hau_NG', 'heb', 'hin', 'hrv', 'hun', 'hye', 'ibo', 'ind', 'isl', 'ita', 'jav', 'jav_java', 'jpn
… [1532 caractères tronqués]
  ```

- **bash** `{"command": "cat > work/j32/explore4.py <<'PY'\nimport json, numpy as np\nfrom scipy import stats\nsel=json.load(open('reports/corpus-commun.json'))['textes']\nret=json.load(open('reports/retrieval-epoque.json'))['udhr']\nids=[t['id'] for t in sel]; idx={x:i for i,x in enumerate(ids)}\nP={}\nfor p i … [3772 caractères tronqués]`

  ```
entries 0 []

 P1 LANG_TREE values {np.float64(1.0): np.int64(210)}
   1.0 210 0.151 script 0.27

 P2 UDHR meta values {np.float64(0.15): np.int64(4), np.float64(0.4): np.int64(14), np.float64(0.75): np.int64(87), np.float64(1.0): np.int64(105)}
   0.15 4 0.3589 script 0.75
   0.4 14 0.1915 script 0.14
   0.75 87 0.1481 script 0.26
   1.0 105 0.1401 script 0.27

 G Glottolog values {np.float64(0.2): np.int64(1), np.float64(0.45454545454545453): np.int64(1), np.float64(0.6): np.int64(2), np.float64(0.6363636363636364): np.int64(1), np.float64(0.75): np.int64(1), np.float64(0.7777777777777778): np.int64(3), np.float64(0.8): np.int64(3), np.float64(0.8333333333333334): np.int64(1), np.float64(0.8571428571428571): np.int64(2), np.float64(0.875): np.int64(1), np.float64(0.8888888888888888): np.int64(2), np.float64(0.8947368421052632): np.int64(1), np.float64(0.9): np.int64(1), np.float64(0.9130434782608695): np.int64(1), np.float64(0.92): np.int64(2), np.float64(1.0): np.int64(11), np.float64(1.0769230769230769): np.int64(1), np.float64(1.0952380952380953): np.int64(4), np.float64(1.1): np.int64(10), np.float64(1.105263157894737): np.int64(3), np.float64(1.1111111111111112): np.int64(1)
… [2796 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '60,120p' ../Panini/research/src/nipada/signing/language_genealogy.py", "description": "Inspect LANG_TREE entry format"}`

  ```
script: str                     # primary script
    closest_kin: tuple[str, ...] = field(default_factory=tuple)  # ordered by proximity
    notes: str = ""


# ---------------------------------------------------------------------------
# LANG_TREE — master registry
# ---------------------------------------------------------------------------

LANG_TREE: dict[str, LangInfo] = {
    # ── Indo-European / Germanic ───────────────────────────────────────────
    "eng": LangInfo("eng", "indo_european", "germanic", "modern",
                    "analytic", "latin_roman",
                    ("deu",),
                    "English — analytic modern Germanic"),
    "deu": LangInfo("deu", "indo_european", "germanic", "modern",
                    "fusional", "latin_roman",
                    ("eng",),
                    "German — fusional modern Germanic"),
    "nld": LangInfo("nld", "indo_european", "germanic", "modern",
                    "fusional", "latin_roman",
                    ("eng", "deu"),
                    "Dutch"),
    "swe": LangInfo("swe", "indo_european", "germanic", "modern",
                    "analytic", "latin_roman",
                    ("nor", "dan", "eng"),
   
… [1706 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re\nsrc=open('../Panini/research/src/nipada/signing/language_genealogy.py').read()\nblock=src.split('LANG_TREE: dict[str, LangInfo] = {',1)[1].split('\\n}',1)[0]\nentries={}\nfor m in re.finditer(r'\"([a-z]{3})\":\\s*LangInfo\\(\\s*\"([a-z]{3})\",\\s*\"([^\"]+)\ … [255 caractères tronqués]`

  ```
29
eng {'family': 'indo_european', 'branch': 'germanic'}
fra {'family': 'indo_european', 'branch': 'romance'}
ell {'family': 'indo_european', 'branch': 'hellenic'}
hin {'family': 'indo_european', 'branch': 'indic'}
heb {'family': 'semitic', 'branch': 'hebrew'}
kin None
ind None
amh None
  ```

- **bash** `{"command": "python3 - <<'PY'\np='work/j32/explore4.py'\ns=open(p).read()\ns=s.replace(\"\"\"entries={}\nfor m in re.finditer(r\"^\\\\s{4}\\\\\"([a-z]{3})\\\\\": LangInfo\\\\((.*?)\\\\n\\\\s{4}\\\\)\",src,re.S|re.M):\n    code,body=m.group(1),m.group(2)\n    def get(field):\n        mm=re.search(rf\ … [619 caractères tronqués]`

  ```
entries 29 [('eng', {'family': 'indo_european', 'branch': 'germanic'}), ('deu', {'family': 'indo_european', 'branch': 'germanic'}), ('nld', {'family': 'indo_european', 'branch': 'germanic'})]

 P1 LANG_TREE values {np.float64(0.4): np.int64(6), np.float64(0.75): np.int64(4), np.float64(1.0): np.int64(200)}
   0.4 6 0.2696 script 0.17
   0.75 4 0.1332 script 0.0
   1.0 200 0.1478 script 0.28

 P2 UDHR meta values {np.float64(0.15): np.int64(4), np.float64(0.4): np.int64(14), np.float64(0.75): np.int64(87), np.float64(1.0): np.int64(105)}
   0.15 4 0.3589 script 0.75
   0.4 14 0.1915 script 0.14
   0.75 87 0.1481 script 0.26
   1.0 105 0.1401 script 0.27

 G Glottolog values {np.float64(0.2): np.int64(1), np.float64(0.45454545454545453): np.int64(1), np.float64(0.6): np.int64(2), np.float64(0.6363636363636364): np.int64(1), np.float64(0.75): np.int64(1), np.float64(0.7777777777777778): np.int64(3), np.float64(0.8): np.int64(3), np.float64(0.8333333333333334): np.int64(1), np.float64(0.8571428571428571): np.int64(2), np.float64(0.875): np.int64(1), np.float64(0.8888888888888888): np.int64(2), np.float64(0.8947368421052632): np.int64(1), np.float64(0.9): np.int64(1), np.float64(0.91304
… [2398 caractères tronqués]
  ```

- **bash** `{"command": "cat > work/j32/explore5.py <<'PY'\nimport json, re, numpy as np\nfrom scipy import stats\nsel=json.load(open('reports/corpus-commun.json'))['textes']\nret=json.load(open('reports/retrieval-epoque.json'))['udhr']\nids=[t['id'] for t in sel]; idx={x:i for i,x in enumerate(ids)}\nP={}\nfor … [6256 caractères tronqués]`

  ```
== Model B decomposition ==
P2 all + unknown indicator [ 0.2946  0.0638 -0.22   -0.1716] [0. 0. 0. 0.] R2 0.2253
P2 labelled only [ 0.279  0.102 -0.212] [0.     0.     0.0009] R2 0.2564
G all + unknown indicator [ 0.4132  0.0629 -0.2413 -0.2899] [0.     0.     0.0001 0.    ] R2 0.2021
G labelled only [ 0.3861  0.1005 -0.2259] [0.0001 0.     0.0065] R2 0.2297

== LOO labelled ==
P2 coef min/med/max -0.2958 -0.212 -0.1034 R2 min/med/max 0.1648 0.2564 0.3171
   worst language udhr_ind best udhr_tgl
G coef min/med/max -0.2944 -0.2259 -0.1004 R2 min/med/max 0.1539 0.2297 0.3007
   worst language udhr_ind best udhr_bel

== LOO all ==
P2 coef min/med/max -0.1371 -0.1289 -0.057 R2 min/med/max 0.141 0.2043 0.2328
   worst language udhr_ind best udhr_tgl
G coef min/med/max -0.1584 -0.1223 -0.0652 R2 min/med/max 0.138 0.1632 0.1944
   worst language udhr_jav best udhr_mly_arab

== label permutation ==
P2 obs {'all': np.float64(-0.1184), 'labeled': np.float64(-0.212)}
   all null mean 0.001 p 0.004 pct [-0.0726  0.0051  0.0479]
   labeled null mean 0.0022 p 0.002 pct [-0.1351  0.0081  0.0982]
G obs {'all': np.float64(-0.1161), 'labeled': np.float64(-0.2259)}
   all null mean -0.0003 p 0.014 pc
… [291 caractères tronqués]
  ```

- **bash** `{"command": "cat > work/j32/explore6.py <<'PY'\nimport json, numpy as np\nsel=json.load(open('reports/corpus-commun.json'))['textes']\nret=json.load(open('reports/retrieval-epoque.json'))['udhr']\nids=[t['id'] for t in sel]; idx={x:i for i,x in enumerate(ids)}\nP={}\nfor p in ret['paires']:\n    key … [2127 caractères tronqués]`

  ```
overall MRR 0.1509748095221739 top1 0.049444444444444444

P2 levels:
  0.15 n=  4 MRR=0.3589 top1=0.2667 script=0.75
  0.40 n= 14 MRR=0.1915 top1=0.0964 script=0.14
  0.75 n= 87 MRR=0.1481 top1=0.0458 script=0.26
  1.00 n=105 MRR=0.1401 top1=0.0379 script=0.27

P2 levels x script (MRR / n):
  d=0.15 script=1 n=  3 MRR=0.4342 top1=0.3444
  d=0.15 script=0 n=  1 MRR=0.1332 top1=0.0333
  d=0.40 script=1 n=  2 MRR=0.5413 top1=0.4750
  d=0.40 script=0 n= 12 MRR=0.1332 top1=0.0333
  d=0.75 script=1 n= 23 MRR=0.1896 top1=0.0804
  d=0.75 script=0 n= 64 MRR=0.1332 top1=0.0333
  d=1.00 script=1 n= 28 MRR=0.1590 top1=0.0506
  d=1.00 script=0 n= 77 MRR=0.1332 top1=0.0333

Glottolog family x script (MRR / n):
  fam=1 script=1 n=  8 MRR=0.3853 top1=0.2917
  fam=1 script=0 n= 26 MRR=0.1332 top1=0.0333
  fam=0 script=1 n= 48 MRR=0.1691 top1=0.0608
  fam=0 script=0 n=128 MRR=0.1332 top1=0.0333

Pairs in same-script x (same family or same branch):
  udhr_eng           udhr_fra           MRR=0.9515 top1=0.9333 panini=0.40 branch=Germanic/Romance
  udhr_kin           udhr_ewe           MRR=0.1585 top1=0.0500 panini=1.00 branch=Bantu/Unknown
  udhr_kin           udhr_ibo           MRR=0.1311 top1=0.016
… [592 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, numpy as np\nsel=json.load(open('reports/corpus-commun.json'))['textes']\nret=json.load(open('reports/retrieval-epoque.json'))['udhr']\nids=[t['id'] for t in sel]; idx={x:i for i,x in enumerate(ids)}\nP={}\nfor p in ret['paires']:\n    key=tuple(sorted((p[ … [766 caractères tronqués]`

  ```
cross n 154 min 0.13316623769734637 max 0.13316623769734637 unique 1
same n 56 min 0.10482049827147305 max 0.9515476190476191 mean 0.1999483820404497
cross top1 unique [np.float64(0.03333333333333333)]
H30/30 0.13316623769734637
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nfor t in (d if isinstance(d,list) else d.get('taches',[])):\n    if t.get('jour')==3:\n        print(t['id'],'—',t['titre'])\nPY", "description": "List day 3 tasks"}`

  ```
J3.1 — Panini II — le retrieval à époque contrôlée
J3.2 — Panini II — la généalogie à deux faces
  ```

- **bash** `{"command": "ls journal/ | tail -20; echo '---'; ls journal/2026-11-07 2>/dev/null | head; echo '---'; find journal -maxdepth 2 -type f -name '*.md' | tail -20", "description": "Inspect journal structure"}`

  ```
2026-10-22
2026-10-23
2026-10-24
2026-10-25
2026-10-26
2026-10-27
2026-10-28
2026-10-29
2026-10-30
2026-10-31
2026-11-01
2026-11-02
2026-11-03
2026-11-04
2026-11-05
2026-11-06
2026-11-07
README.md
sessions
THEMES.md
---
distribue.md
docs.md
memoire.md
mesures.md
modele.md
portes.md
README.md
---
journal/2026-11-05/moteur.md
journal/2026-11-05/mesures.md
journal/2026-11-05/modele.md
journal/2026-11-05/attention.md
journal/2026-11-06/README.md
journal/2026-11-06/distribue.md
journal/2026-11-06/mesures.md
journal/2026-11-06/portes.md
journal/2026-11-06/docs.md
journal/2026-11-06/modele.md
journal/2026-11-06/outils.md
journal/2026-11-06/memoire.md
journal/2026-11-06/moteur.md
journal/2026-11-07/docs.md
journal/2026-11-07/portes.md
journal/2026-11-07/distribue.md
journal/2026-11-07/modele.md
journal/2026-11-07/memoire.md
journal/2026-11-07/mesures.md
journal/2026-11-07/README.md
  ```

- **bash** `{"command": "cat journal/2026-11-07/README.md; echo '==='; tail -60 journal/2026-11-07/mesures.md", "description": "Read journal README and measures"}`

  ```
# 2026-11-07

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-07/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**28 commits** · **5 session(s)** · **6 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 3 | [distribue.md](distribue.md) |
| docs | 12 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 7 | [mesures.md](mesures.md) |
| modele | 1 | [modele.md](modele.md) |
| portes | 4 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `77d26bc7-1657-4c96-83c9-bba7c25dd828` | Tu travailles dans /home/stephane/Data13 | 2026-11-07 00:49 | 1.4 h | [rapport](../sessions/77d26bc7-1657-4c96-83c9-bba7c25dd828/rapport.md) · [digest](../sessions/77d26bc7-1657-4c96-83c9-bba7c25dd828/digest.md) |
| `7f247e9c-00ab-4bdf-bfba-2dc5c20d7cf0` | Tu travailles dans /home/stephane/Data13 | 2026-11-07 02:09 | 0.1 h | [rapport](../sessions/7f247e9c-00ab-4bdf-bfba-2dc5c20d7cf0/rap
… [12194 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' docs/pilotage/roadmap.md | head -60; echo '---'; grep -n \"R0.7\\|J3.2\\|généalogie\" docs/pilotage/roadmap.md | head -20", "description": "Read roadmap head and R0.7 mentions"}`

  ```
# La roadmap de [Drave](../theorie/glossaire/entrees/drave.md) — un seul plan, quatre chantiers

> **Un seul document de plan.** Le **moteur** (A), l'**intelligence** (B), le **natif** (N) et le **lecteur** (R).
> L'ordre se décide par la **valeur** et les **dépendances**, jamais par une date. Les chiffres, les séries et les
> contrôles vivent dans [`reports/`](../../reports/) ; ici : l'[état](../theorie/glossaire/entrees/etat.md), la prochaine action, et ce qui bloque.
>
> **Détail et histoire** : l'ancien plan [A/B](../theorie/glossaire/entrees/a-b.md) est archivé dans
> [`roadmap-detail-2026-10-29.md`](../archive/roadmap-detail-2026-10-29.md), le détail N dans
> [`roadmap-native-2026-10-29.md`](../archive/roadmap-native-2026-10-29.md). Les **fiches de fonctionnalité** sont
> dans [`backlog/index.md`](backlog/index.md) ; le **graphe des dépendances** est dans
> [`backlog/dependances.md`](backlog/dependances.md). La **page vivante** est [`en-cours.md`](en-cours.md).

## Comment lire cette roadmap

- **Les états** : ✅ mesuré et écrit · 🔬 en cours · ⏳ à faire · 🧱 bloqué par une infra absente.
- **Le carpe diem** : pas d'échéance. Un chantier est **[fait](../theorie/glossaire/entrees
… [14851 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, collections\nd=json.load(open('../Panini/research/nipada/falsification/pairs334_axes_v1.json'))\nps=d['pairs']\nc=collections.Counter()\nfor p in ps:\n    a=p.get('lang_a') or ''; b=p.get('lang_b') or ''\n    c[(a,b)]+=1\nprint('top lang pairs',c.most_comm … [512 caractères tronqués]`

  ```
top lang pairs [(('eng', ''), 234), (('eng', 'eng'), 173), (('', ''), 153), (('', 'eng'), 92), (('fra', 'eng'), 2), (('eng', 'fra'), 1)]
both nonempty 176
different nonempty 3
same nonempty 173
lang_a empty 245
lang_b empty 387
  ```

- **bash** `{"command": "cat > work/j32/explore7.py <<'PY'\nimport json, re, numpy as np\nsel=json.load(open('reports/corpus-commun.json'))['textes']\nret=json.load(open('reports/retrieval-epoque.json'))['udhr']\nids=[t['id'] for t in sel]; idx={x:i for i,x in enumerate(ids)}\nP={}\nfor p in ret['paires']:\n    … [2818 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/j32/explore7.py", line 11, in <module>
    Y=np.array([mrr[(ids[i],ids[j])] for i,j in pairs]); T=np.array([top[(ids[i],ids[j])] for i,j in pairs])
                ~~~^^^^^^^^^^^^^^^^^
KeyError: ('udhr_eng', 'udhr_bel')
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='work/j32/explore7.py'\ns=open(p).read()\ns=s.replace(\"Y=np.array([mrr[(ids[i],ids[j])] for i,j in pairs]); T=np.array([top[(ids[i],ids[j])] for i,j in pairs])\",\n\"Y=np.array([mrr[tuple(sorted((ids[i],ids[j])))] for i,j in pairs]); T=np.array([top[tuple(sorted((id … [145 caractères tronqués]`

  ```
P1
  0.40 n=  6 mean=0.2696 med=0.1332 min=0.1332 max=0.9515 script=0.17
  0.75 n=  4 mean=0.1332 med=0.1332 min=0.1332 max=0.1332 script=0.00
  1.00 n=200 mean=0.1478 med=0.1332 min=0.1048 max=0.9178 script=0.28

 P2
  0.15 n=  4 mean=0.3589 med=0.1924 min=0.1332 max=0.9178 script=0.75
  0.40 n= 14 mean=0.1915 med=0.1332 min=0.1311 max=0.9515 script=0.14
  0.75 n= 87 mean=0.1481 med=0.1332 min=0.1171 max=0.3501 script=0.26
  1.00 n=105 mean=0.1401 med=0.1332 min=0.1048 max=0.3456 script=0.27

G by LCA depth
  depth=0 n=176 mean=0.1430 med=0.1332 script=0.27
  depth=1 n= 11 mean=0.1332 med=0.1332 script=0.00
  depth=2 n= 17 mean=0.2395 med=0.1332 script=0.35
  depth=3 n=  4 mean=0.1857 med=0.1332 script=0.50
  depth=4 n=  1 mean=0.1332 med=0.1332 script=0.00
  depth=5 n=  1 mean=0.1332 med=0.1332 script=0.00

8 same-family same-script pairs
  udhr_eng           udhr_fra           MRR=0.9515 top1=0.9333 panini=0.40
  udhr_kin           udhr_ewe           MRR=0.1585 top1=0.0500 panini=1.00
  udhr_kin           udhr_ibo           MRR=0.1311 top1=0.0167 panini=0.40
  udhr_ewe           udhr_ibo           MRR=0.1932 top1=0.1000 panini=1.00
  udhr_ind           udhr_tgl           MRR=0.2
… [252 caractères tronqués]
  ```

- **bash** `{"command": "cat >> work/j32/explore7.py <<'PY'\nprint('\\nFraction above floor (MRR > 0.133166+1e-6):')\nfor name,D in [('P1',P1),('P2',P2)]:\n    print(' ',name)\n    for v in sorted(set(D)):\n        m=D==v; x=Y[m]; ab=x>0.1331663+1e-6\n        print(f'   {v:.2f} n={m.sum():3d} above={ab.sum():3d … [614 caractères tronqués]`

  ```
depth=3 n=  4 mean=0.1857 med=0.1332 script=0.50
  depth=4 n=  1 mean=0.1332 med=0.1332 script=0.00
  depth=5 n=  1 mean=0.1332 med=0.1332 script=0.00

8 same-family same-script pairs
  udhr_eng           udhr_fra           MRR=0.9515 top1=0.9333 panini=0.40
  udhr_kin           udhr_ewe           MRR=0.1585 top1=0.0500 panini=1.00
  udhr_kin           udhr_ibo           MRR=0.1311 top1=0.0167 panini=0.40
  udhr_ewe           udhr_ibo           MRR=0.1932 top1=0.1000 panini=1.00
  udhr_ind           udhr_tgl           MRR=0.2077 top1=0.1167 panini=0.15
  udhr_ind           udhr_jav           MRR=0.9178 top1=0.8667 panini=0.15
  udhr_tgl           udhr_jav           MRR=0.1771 top1=0.0500 panini=0.15
  udhr_cnh           udhr_ctd           MRR=0.3456 top1=0.2000 panini=1.00

Fraction above floor (MRR > 0.133166+1e-6):
  P1
   0.40 n=  6 above=  1 (17%) mean_above=0.9515
   0.75 n=  4 above=  0 (0%) mean_above=nan
   1.00 n=200 above= 43 (22%) mean_above=0.2037
  P2
   0.15 n=  4 above=  3 (75%) mean_above=0.4342
   0.40 n= 14 above=  1 (7%) mean_above=0.9515
   0.75 n= 87 above= 18 (21%) mean_above=0.2071
   1.00 n=105 above= 22 (21%) mean_above=0.1694

Same script x family:
  fam=T
… [266 caractères tronqués]
  ```

- **bash** `{"command": "mkdir -p tools && cat > tools/genealogie_deux_faces.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"genealogie_deux_faces.py — J3.2 : la généalogie à deux faces.\n\nPOURQUOI. Panini tient une **théorie** de la généalogie (14 atomes, 9 dhātus, une échelle de\ndistance à quatre niveaux) ; Drave  … [50188 caractères tronqués]`

  ```
[stderr]
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/genealogie_deux_faces.py:173: RuntimeWarning: invalid value encountered in divide
  t = b / se
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/genealogie_deux_faces.py", line 888, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/genealogie_deux_faces.py", line 759, in main
    "convergence": {"n": len(convergence), "langues": sorted(convergence),
                                                      ~~~~~~^^^^^^^^^^^^^
TypeError: '<' not supported between instances of 'dict' and 'dict'
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/genealogie_deux_faces.py'\ns=open(p).read()\ns=s.replace('    convergence = lire_json(panini / \"data\" / \"udhr_convergence_v14.json\")',\n            '    convergence_v14 = lire_json(panini / \"data\" / \"udhr_convergence_v14.json\")')\ns=s.replace('    conv … [1952 caractères tronqués]`

  ```
J3.2 — la généalogie à deux faces
  corpus commun : 21 langues, 5 familles, 10 écritures, 210 paires non ordonnées
  couverture : LANG_TREE 5/21 ; métadonnées UDHR 15/21 ; Glottolog 21/21
  V14 : décomposition 3/21 ; convergence 1/21
  accord familles (mappé) : 15/15 ; branches exactes : 14/15
  retrieval : MRR 0.1510 ; hors script 0.1332 (hasard 0.1332), même script 0.1999
  régression labelisées : R² Panini 0.2564 ; Glottolog 0.2297
  atomes : 4 valeurs propres > 1 (corrélation), 1 (covariance) ; 90 % à 5 composantes
  §150 : 3/655 paires inter-langues ; β filiation/époque = 0.355
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/genealogie-deux-faces.json
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/genealogie-deux-faces.json'))\nprint(d.keys())\nprint('\\ncorpus',d['corpus_commun']['n_textes'],d['corpus_commun']['n_paires_non_ordonnees'])\nprint('\\nconvergence n',len(d['convergence']))\nprint('\\ndivergence n',len(d['diverg … [825 caractères tronqués]`

  ```
dict_keys(['titre', 'version', 'date', 'ligne_roadmap', 'chantier', 'statut', 'question', 'sources', 'corpus_commun', 'theorie_panini', 'accord_genealogies', 'alignement', 'atomes', 'convergence', 'divergence', 'a_mesurer', 'limites', 'controles_negatifs', 'fichiers'])

corpus 21 210

convergence n 5

divergence n 7

a_mesurer n 7

script {'n_meme': 56, 'n_different': 154, 'mrr_meme': 0.1999483820404497, 'mrr_different': 0.13316623769734637, 'top1_meme': 0.09375, 'top1_different': 0.03333333333333333, 'hors_script_au_hasard': True, 'mrr_hors_script_unique': 0.13316624}

regressions:
  toutes
    {'nom': 'script', 'n': 210, 'coef_script': 0.06678214434310357, 'p_script': 1.8463667994517152e-07, 'r2': 0.12280053618310405, 'aic': -1062.4591309082941}
    {'nom': 'script+panini_lang_tree', 'n': 210, 'coef_script': 0.06977453435914231, 'p_script': 2.3016811123710568e-08, 'r2': 0.1820928947975473, 'aic': -1075.156114986561, 'coef_distance': -0.19609704785956372, 'p_distance': 0.00014375566925362016}
    {'nom': 'script+panini_udhr', 'n': 210, 'coef_script': 0.06518655524535885, 'p_script': 1.1530892329858489e-07, 'r2': 0.19801982096860682, 'aic': -1079.2857384625843, 'coef_distance': -0.
… [7084 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/genealogie-deux-faces.json'))\nprint('decomposition_inconnu:')\nfor x in d['alignement']['decomposition_inconnu']: print(x)\nprint('\\np1_p2:',d['accord_genealogies']['p1_p2'])\nprint('\\ngroupes P2:')\nfor k,v in d['alignement'][ … [339 caractères tronqués]`

  ```
decomposition_inconnu:
{'nom': 'panini_udhr', 'coef_script': 0.06381765451860782, 'coef_distance': -0.22001514842041292, 'coef_inconnu': -0.17156403133608442, 'p_distance': 3.433018574527935e-06, 'p_inconnu': 4.906223651790498e-07, 'r2': 0.22528903010001167, 'aic': -1084.5504522982185, 'n': 210}
{'nom': 'glottolog', 'coef_script': 0.06291331262688848, 'coef_distance': -0.2412828764615394, 'coef_inconnu': -0.289914178369434, 'p_distance': 8.228208760252542e-05, 'p_inconnu': 2.716266498548059e-05, 'r2': 0.20213223661374935, 'aic': -1078.3653525492516, 'n': 210}

p1_p2: {'n_paires': 10, 'valeurs_identiques': True, 'exemple': [{'p1': 0.4, 'p2': 0.4}, {'p1': 0.4, 'p2': 0.4}, {'p1': 0.75, 'p2': 0.75}, {'p1': 0.4, 'p2': 0.4}, {'p1': 0.4, 'p2': 0.4}]}

groupes P2:
0.15 {'n': 4, 'moyenne': 0.3589388754914747, 'mediane': 0.1923825950972392, 'min': 0.13316623769734637, 'max': 0.9178240740740741, 'au_dessus_du_hasard': 3, 'part_au_dessus_du_hasard': 0.75, 'moyenne_au_dessus': 0.4341964214228508, 'script_meme': 0.75, 'top1_moyen': 0.2666666666666667}
0.40 {'n': 14, 'moyenne': 0.19147118766024843, 'mediane': 0.13316623769734637, 'min': 0.1310541558277025, 'max': 0.9515476190476191, 'au_dessus_du
… [3185 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/genealogie_deux_faces.py'\ns=open(p).read()\nold='''    accord_famille_brut = 0\n    accord_famille_mappe = 0\n    desaccords_famille = []\n    accord_branche_exact = 0\n    accord_branche_proche = 0\n    desaccords_branche = []\n    for t in labelise_textes:\ … [4463 caractères tronqués]`

  ```
J3.2 — la généalogie à deux faces
  corpus commun : 21 langues, 5 familles, 10 écritures, 210 paires non ordonnées
  couverture : LANG_TREE 5/21 ; métadonnées UDHR 15/21 ; Glottolog 21/21
  V14 : décomposition 3/21 ; convergence 1/21
  accord familles (mappé) : 15/15 ; branches exactes : 14/15
  retrieval : MRR 0.1510 ; hors script 0.1332 (hasard 0.1332), même script 0.1999
  régression labelisées : R² Panini 0.2564 ; Glottolog 0.2297
  atomes : 4 valeurs propres > 1 (corrélation), 1 (covariance) ; 90 % à 5 composantes
  §150 : 3/655 paires inter-langues ; β filiation/époque = 0.355
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/genealogie-deux-faces.json
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/genealogie-deux-faces.json'))\na=d['accord_genealogies']\nfor k in ['famille_brute','famille_mappee','branche_exacte','branche_proche']:\n    print(k,a[k])\nPY", "description": "Verify agreement details"}`

  ```
famille_brute {'accord': 13, 'n': 15, 'taux': 0.8666666666666667, 'desaccords': [{'id': 'udhr_kin', 'panini': 'Niger-Congo', 'glottolog': 'Atlantic-Congo', 'note': 'nomenclature : Niger-Congo est la famille large, Atlantic-Congo le nœud Glottolog'}, {'id': 'udhr_ibo', 'panini': 'Niger-Congo', 'glottolog': 'Atlantic-Congo', 'note': 'nomenclature : Niger-Congo est la famille large, Atlantic-Congo le nœud Glottolog'}]}
famille_mappee {'accord': 15, 'n': 15, 'taux': 1.0, 'desaccords': []}
branche_exacte {'accord': 14, 'n': 15, 'taux': 0.9333333333333333, 'desaccords': [{'id': 'udhr_mya', 'panini': 'Tibeto-Burman', 'noeud': 'burm1265', 'note': "le nœud exact tibe1272 n'est pas dans le chemin Glottolog ; burm1265 est le descendant le plus proche"}]}
branche_proche {'accord': 15, 'n': 15, 'taux': 1.0}
  ```

- **bash** `{"command": "ls -lh reports/genealogie-deux-faces.json; python3 -c \"\nimport json;d=json.load(open('reports/genealogie-deux-faces.json'));print(len(json.dumps(d,ensure_ascii=False)))\"", "description": "Check JSON size"}`

  ```
-rw-r--r--. 1 stephane stephane 106K  7 nov 18:08 reports/genealogie-deux-faces.json
91201
  ```

- **bash** `{"command": "cat > reports/rapport-genealogie-deux-faces.md <<'MD'\n# J3.2 — La généalogie à deux faces : Panini et Glottolog sur le corpus commun\n\n> **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : semaine Panini, J3.2 · **Date** : 2026-11-07\n> **Verdict** : ✅ **la confrontation … [26893 caractères tronqués]`

  ```
389 reports/rapport-genealogie-deux-faces.md
  ```

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-genealogie-deux-faces.md'\ns=open(p).read()\ns=s.replace(\"**Stabilité split-half** (1 000 coupures 22/22) : le premier axe est stable (cos moyen **0,930**, IC\\n[0,298 ; 0,993]), mais le sous-espace à 3 dimensions ne l'est que partiellement (recouvr … [1187 caractères tronqués]`

  ```
230:**Stabilité split-half** (1 000 coupures 22/22) : le premier axe est stable **en moyenne** (cos **0,930**),
303:   Les 6 langues non labellisées par Panini sont **toutes non-IE** ; **3 des 4 paires de même branche** sont
  ```

- **bash** `{"command": "cat > docs/theorie/genealogie-des-langues.md <<'MD'\n# La généalogie des langues, des dialectes et des styles\n\n> **Ce que cette page est.** La **théorie** de la structure généalogique qui doit organiser l'**étage\n> entrée-sortie** (nom historique : « couche commune ») de Drave, et ce … [11115 caractères tronqués]`

  ```
157 docs/theorie/genealogie-des-langues.md
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/theorie/genealogie-des-langues.md'\ns=open(p).read()\ns=s.replace(\"et il y est porté par **quelques paires** (deux paires de même famille et de même écriture portent la\\nmoyenne ; les autres sont à peine au-dessus du hasard).\",\n\"et il y est porté par **que … [792 caractères tronqués]`

  ```
87:et il y est porté par **quelques paires** (quelques paires de même famille et de même écriture portent la
105:1. **Les 14 atomes ne sont pas 14 dimensions.** Sur les signatures de Panini, l'ACP donne **un petit nombre**
150:   le corpus actuel ne donne que quelques paires de même famille et de même écriture.
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/en-cours.md'\ns=open(p).read()\ns=s.replace(\"**Mis à jour : 2026-11-07, 17 h 05 HNE (heure locale, EST).**\",\n            \"**Mis à jour : 2026-11-07, 18 h 30 HNE (heure locale, EST).**\")\nold=\"- **Panini J2.1/J2.2/J3.1** : table **14 atomes** ; UD … [1832 caractères tronqués]`

  ```
3:**Mis à jour : 2026-11-07, 18 h 30 HNE (heure locale, EST).**
92:- **Panini J2.1/J2.2/J3.1/J3.2** : table **14 atomes** ; UDHR **418/438 exactes** ; **J3.1 : l'écriture domine, l'époque ne pèse pas à écriture contrôlée (−0,034/siècle, p=0,19), le brut est un effet de composition** ; **J3.2 : les deux faces ne mesurent pas le même objet** — la « filiation » de Panini est une distance de **tradition** (**3/655** paires inter-langues), sa fonction `lang_distance` couvre **5/21** langues (**200/210** paires « inconnues »), Glottolog **21/21** ; **154/154** paires hors script au hasard exact, le signal de famille vit dans **2-3 paires** ; la face atomes n'est pas disponible (**V14 : 3/21**) ; [fiches](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [époque](../../reports/rapport-retrieval-epoque.md), [deux faces](../../reports/rapport-genealogie-deux-faces.md).
124:**N2** — la **porte propre (0,29)** ; le 2 048 est fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035`, convention des GV, schéma v2 et restitution v0 faits**, reste `g017` ; **J3.2** — fait : [deux faces](../../reports/rapport-genealogie-deux-faces.md) ; la pr
… [641 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/roadmap.md'\ns=open(p).read()\nold=\" ; **J3.1 retrieval à époque contrôlée : l'écriture domine (+0,609), l'époque ne pèse pas à écriture contrôlée (−0,034/siècle, p=0,19), le brut est un effet de composition (0,238 vs 0,427)** ([fiche](../../reports/r … [2523 caractères tronqués]`

  ```
35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **fusion réparée par niveau : 0,9309/0,8226/0,8784/0,9954 (le max)** ([fiche](../../reports/rapport-pensee-fusion-reparee.md)) ; **corpus commun UDHR : 21 textes, 418/438 paires exactes (95,4 %), 20 écarts exclus** ([fiche](../../reports/rapport-corpus-commun.md)) ; **J3.1 retrieval à époque contrôlée : l'écriture domine (+0,609), l'époque ne pèse pas à écriture contrôlée (−0,034/siècle, p=0,19), le brut est un effet de composition (0,238 vs 0,427)** ([fiche](../../reports/rapport-retrieval-epoque.md)) ; **J3.2 généalogie à deux faces : Panini couvre 5/21 langues (200/210 paires « inconnues »), Glottolog 21/21 ; 154/154 paires hors script au hasard exact, le signal de famille vit dans 
… [1802 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='journal/2026-11-07/README.md'\ns=open(p).read()\nadd=\"\"\"\n**La fin d'après-midi du 07/11 (J3.2).** La **généalogie à deux faces** confronte la théorie de Panini\n(14 atomes, 9 dhātus, une échelle de distance) à nos mesures d'alignement (Glottolog + retrieval) sur … [3103 caractères tronqués]`

  ```
<!-- notes -->
**13 h 30 — la convention des GV.** Le classement des erreurs de GV (320 FP / 179 FN après
`r035`, 322/180 avant) donnait **144 FP de sujet (45 %)** et 73 d'objet. La règle **sujet hors du
GV** (le GV du générateur S commence au prédicat, le sujet est un GN) rend **F1 0,7549 → 0,7881** ;
l'**arrêt à l'adverbe final de temps** rend **+0,0026** ; les deux ensemble **0,7902** (dev
**0,7875**, test **0,7962**), **attachement 237/238 inchangé**, POS **0,8625**, **183/183**. Le
gold est **unanime** sur le sujet (**712/712 GV** commencent par VERB/AUX/ADV, aucun par un sujet)
mais **contradictoire** sur l'adverbe final (`r019`/`r186`, `r051`/`r189`). Fiche
[rapport-convention-gv.md](../../reports/rapport-convention-gv.md) · JSON
[pensee-convention-gv.json](../../reports/pensee-convention-gv.json).

**18 h 30 — J3.2, la généalogie à deux faces.** La confrontation de la théorie de Panini (14 atomes,
9 dhātus) et de nos mesures d'alignement (Glottolog + retrieval) sur les 21 langues du corpus commun
donne trois résultats. **Ce qui converge** : la surface passe avant la filiation des deux côtés, et le
rapport filiation/surface est du même ordre (β 0,049/0,138 = 0,355 chez Panin
… [1279 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/ | grep -i -E 'index|revue|rapport|documentation|tableau|schema|taille|journal|en_cours'", "description": "Find documentation/index tools"}`

  ```
bloc_tableaux.py
decouper-rapport.py
extraire_tableaux.py
index_reports.py
index_spans.py
index_wiki_en.py
journal_auto.py
porte-bloc-tableaux.sh
porte-tableaux.sh
rapport_du_pont.py
revue_documentation.py
schemas
taille_documents.py
verifie_en_cours.py
verifie_journal.py
verifier_schema_produit.py
verifier_schemas.py
  ```

- **bash** `{"command": "head -40 reports/README.md; echo '---'; head -30 reports/INDEX.md; echo '---'; grep -n \"rapport-genealogie\\|genealogie-deux-faces\" reports/README.md reports/INDEX.md 2>/dev/null | head", "description": "Inspect reports index files"}`

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
| [`rapport-convention-gv.md`](rapport-convention-gv.md) | GV : F1 **0,7902** |
| [`rapport-r035.md`](rapport-r035.md) | **B13** — relative zéro : **237/238** |
| [`rapport-gn-pronom-sujet.md`](rapport-gn-pronom-sujet.md) | **B13** — pronom sujet = GN : **0,7013** |
| [`rapport-r264-elision.md`](rapport-r264
… [5350 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/index_reports.py", "description": "Read reports index generator"}`

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
… [1392 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/index_reports.py && python3 tools/revue_documentation.py 2>&1 | tail -60", "description": "Regenerate reports index and run doc review"}`

  ```
710 fiches → reports/INDEX.md
  revue de documentation · 713 fiche(s) · 806 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 712 fichiers, le disque en a 713
     · compteurs : en-cours.md dit 805 JSON, le disque en a 806
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/en-cours.md'\ns=open(p).read()\ns=s.replace(\"| fichiers / JSON de résultats | **712** / **805** | `reports/*.md` / `reports/*.json` |\",\n            \"| fichiers / JSON de résultats | **713** / **806** | `reports/*.md` / `reports/*.json` |\")\nopen(p … [168 caractères tronqués]`

  ```
102:| fichiers / JSON de résultats | **713** / **806** | `reports/*.md` / `reports/*.json` |
174:| [rapport-genealogie-deux-faces.md](rapport-genealogie-deux-faces.md) | J3.2 — La généalogie à deux faces : Panini et Glottolog sur le corpus commun |
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo '---TABLEAUX---'; bash tools/porte-tableaux.sh 2>&1 | tail -30; echo '---SCHEMAS---'; python3 tools/verifier_schemas.py 2>&1 | tail -20", "description": "Run doc review, table and schema gates"}`

  ```
revue de documentation · 713 fiche(s) · 806 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
---TABLEAUX---
  ✅ 1769 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3839 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-07)
---SCHEMAS---
  schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -20; echo '---EN-COURS---'; python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo '---JOURNAL---'; python3 tools/verifie_journal.py 2>&1 | tail -20", "description": "Run size, state and journal checks"}`

  ```
3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2783    190   T1   2800  reports/README.md
    2404    162   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4087 mots (budget 4 000)

  avertissements :
     · 42 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-f
… [441 caractères tronqués]
  ```

- **bash** `{"command": "git status --short | head -50; echo '---'; git diff --stat | tail -20", "description": "Show working tree status"}`

  ```
MM docs/pilotage/en-cours.md
 M docs/pilotage/references-non-regression.md
MM docs/pilotage/roadmap.md
 M docs/theorie/genealogie-des-langues.md
MM journal/2026-11-07/README.md
 M journal/2026-11-07/mesures.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-a9b5216e-5f4b-4935-8ba0-2ec7d42aaf89/digest.md
 M journal/sessions/session-a9b5216e-5f4b-4935-8ba0-2ec7d42aaf89/rapport.md
MM reports/INDEX.md
A  reports/corpus-commun.json
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
A  reports/rapport-corpus-commun.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
A  reports/rapport-retrieval-epoque.md
 M reports/rapport-spans-chunker.md
A  reports/retrieval-epoque.json
 M tools/chantier/superviseur.py
A  tools/corpus_commun.py
A  tools/retrieval_epoque.py
 m tools/structures
?? journal/sessions/session-1a1b15e7-d5f5-4f11-aeb3-0e6e42628dbe/
?? journal/sessions/session
… [1426 caractères tronqués]
  ```

- **bash** `{"command": "git diff HEAD -- docs/pilotage/en-cours.md | head -120; echo '===ROADMAP==='; git diff HEAD -- docs/pilotage/roadmap.md | head -160", "description": "Inspect all changes in en-cours and roadmap"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index d923018f..a62c04ee 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-07, 14 h 55 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-07, 18 h 30 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -85,11 +85,11 @@
 ## Ce qui est en cours
 
 - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
-- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
+- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
 - **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-i
… [17411 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"commit\\|git add\\|accepter\\|accept\" tools/chantier/superviseur.py | head -60", "description": "Inspect supervisor commit behavior"}`

  ```
6:plusieurs jours : file de tâches persistante, vérification d'acceptation **indépendante** de
10:1. **Une tâche n'est finie que si son acceptation passe** — une commande, un attendu, exécutés par
15:   tâches) arrête la boucle ; l'agent n'est jamais tué au milieu d'un commit.
20:    python3 tools/chantier/superviseur.py executer      # exécute UNE tâche (agent + acceptation)
92:# ------------------------------------------------------------------ acceptation
94:def verifier_acceptation(tache: dict) -> tuple[bool, list[str]]:
95:    """Exécute les commandes d'acceptation de la tâche ; rend (ok, détails)."""
97:    for test in tache.get("acceptation", []):
124:    vérifier, après la tâche, qu'un commit a bien été produit.
136:    """Lance l'agent sur le mandat, puis vérifie l'acceptation. Rend le résultat."""
150:                "acceptation": ["clé DeepSeek absente"], "sortie_agent": "", "cle": False}
160:    ok, details = verifier_acceptation(tache)
161:    # l'acceptation **prime** : un agent qui a fini son travail (fiche + portes) puis dépasse le
166:                "acceptation": details, "sortie_agent": sortie[-1500:]}
194:    for a in t.get("acceptation", []):
195:        prin
… [154 caractères tronqués]
  ```

- **bash** `{"command": "git diff --cached --stat; echo '---'; git diff --cached --name-only", "description": "Show staged files"}`

  ```
docs/pilotage/en-cours.md           |    10 +-
 docs/pilotage/roadmap.md            |     4 +-
 journal/2026-11-07/README.md        |    19 +
 reports/INDEX.md                    |     5 +-
 reports/corpus-commun.json          |  1501 +
 reports/rapport-corpus-commun.md    |   330 +
 reports/rapport-retrieval-epoque.md |   304 +
 reports/retrieval-epoque.json       | 88655 ++++++++++++++++++++++++++++++++++
 tools/corpus_commun.py              |  1154 +
 tools/retrieval_epoque.py           |   818 +
 10 files changed, 92792 insertions(+), 8 deletions(-)
---
docs/pilotage/en-cours.md
docs/pilotage/roadmap.md
journal/2026-11-07/README.md
reports/INDEX.md
reports/corpus-commun.json
reports/rapport-corpus-commun.md
reports/rapport-retrieval-epoque.md
reports/retrieval-epoque.json
tools/corpus_commun.py
tools/retrieval_epoque.py
  ```

- **bash** `{"command": "git diff --cached -- docs/pilotage/en-cours.md | head -80; echo '===ROADMAP STAGED==='; git diff --cached -- docs/pilotage/roadmap.md | head -80", "description": "Inspect staged state edits"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index d923018f..5a197a0a 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-07, 14 h 55 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-07, 17 h 05 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -85,11 +85,11 @@
 ## Ce qui est en cours
 
 - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
-- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
+- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
 - **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-i
… [12030 caractères tronqués]
  ```

- **bash** `{"command": "cp reports/genealogie-deux-faces.json /tmp/j32-a.json && python3 tools/genealogie_deux_faces.py >/tmp/j32-run2.txt && cmp -s /tmp/j32-a.json reports/genealogie-deux-faces.json && echo \"DETERMINISTE-OK\" || echo \"DIFFERENT\"; tail -3 /tmp/j32-run2.txt", "description": "Verify JSON dete … [9 caractères tronqués]`

  ```
DETERMINISTE-OK
  atomes : 4 valeurs propres > 1 (corrélation), 1 (covariance) ; 90 % à 5 composantes
  §150 : 3/655 paires inter-langues ; β filiation/époque = 0.355
  → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/genealogie-deux-faces.json
  ```

- **bash** `{"command": "sed -n '1,160p' tools/taille_documents.py", "description": "Read document size checker"}`

  ```
#!/usr/bin/env python3
"""taille_documents.py — le budget de contexte et la cohésion des documents.

Ce que l'outil vérifie :
  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
  2. la cohésion minimale : un titre, un résumé en tête, et pour les documents datés un
     « Résumé » + « ne pas charger par défaut » ;
  3. les fiches de résultats trop longues pour être lues d'un bloc (avertissement, pas échec) ;
  4. le classement des plus gros documents, pour voir où le contexte part.

Les fiches de `reports/` (sauf `reports/README.md`) et le `journal/` sont **hors budget** :
ils ne sont pas chargés automatiquement. Le budget est en **mots** ; l'estimation de tokens
est donnée à titre indicatif (≈ caractères / 4).

Les **sources de diagrammes** (` ```plantuml `, ` ```mermaid `) sont **rendues, pas lues** :
elles ne comptent pas dans le budget ; le document les porte, la page montre le SVG.
"""
from __future__ import annotations
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent

# (catégorie, budget en mots). Les globs sont résolus dans l'ordre ; le premier match gagne.
BUDGETS: list[tuple[str, str, int
… [5985 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/en-cours.md'\ns=open(p).read()\nstart=\"- **Panini J2.1/J2.2/J3.1/J3.2** :\"\nend=\"\\n\"\ni=s.index(start); j=s.index(\"\\n\", i)\nnew=\"- **Panini J2.1/J2.2/J3.1/J3.2** : table **14 atomes** ; UDHR **418/438** ; **J3.1** : l'écriture domine, l'époque … [1452 caractères tronqués]`

  ```
en-cours · 1635 mots · 7 sections · 4 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
---TAILLE---
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4005 mots (budget 4 000)

  avertissements :
     · 42 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4005 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/en-cours.md'\ns=open(p).read()\ns=s.replace(\"**J3.2** : les deux faces ne mesurent pas le même objet — `lang_distance` couvre\",\n            \"**J3.2** : les deux faces diffèrent — `lang_distance` couvre\")\nopen(p,'w').write(s)\nPY\npython3 tools/ta … [133 caractères tronqués]`

  ```
T0 max : 4000 mots (budget 4 000)

  avertissements :
     · 42 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  en-cours · 1630 mots · 7 sections · 4 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -8; echo '---'; bash tools/porte-tableaux.sh 2>&1 | tail -8; echo '---'; python3 tools/verifie_journal.py 2>&1 | tail -5; echo '---'; python3 tools/verifier_schemas.py 2>&1 | tail -5", "description": "Run all lightweight documentation gat … [4 caractères tronqués]`

  ```
revue de documentation · 713 fiche(s) · 806 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
---
  ✅ 1769 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3839 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-07)
---
  journal · 44 jour(s) · 172 session(s) · 2372 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
---
  schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

- **bash** `{"command": "git commit -m \"PANINI — J2.2 ET J3.1 : LE CORPUS COMMUN (418/438 PAIRES EXACTES, 8/8 CONTRÔLES) ET LE RETRIEVAL À ÉPOQUE CONTRÔLÉE (SCRIPT +0,609, ÉPOQUE −0,034/SIÈCLE, p=0,19)\" 2>&1 | tail -30", "description": "Commit J2.2 and J3.1 staged deliverables"}`
