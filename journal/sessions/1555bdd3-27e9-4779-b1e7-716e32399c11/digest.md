# Session DSH — relecture

- identifiant : `1555bdd3-27e9-4779-b1e7-716e32399c11`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-06 09:31:04
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, dépôt Drave). Mission : écrire la **documentation d'usage du premier produit** — ce qu'un utilisateur peut faire aujourd'hui, en autonomie, avec le système.

Contexte : lis d'abord `README.md` (la vitrine), `docs/pilotage/en-cours.md` (l'état), `reports/rapport-pensee-v12.md` + `reports/pensee-v12.json` (l'attachement : 222/222, couverture 0,9289), `reports/rapport-audit-v10.md` (limites), `reports/rapport-cache-chunker-applique.md` (performance), `tools/bloc_linguistique.py` (l'API). Un prototype de CLI (`tools/drave.py`) est en cours d'écriture par un autre agent : décris les commandes **telles qu'elles devraient être** (`analyser`, `evaluer`, `rejouer`, `--version`) sans supposer qu'elles existent déjà ; signale ce qui manque.

À faire :
1. Écris **`docs/produit/README.md`** (fichier neuf, dossier neuf) : à qui s'adresse le produit, ce qu'il fait (analyse linguistique : POS, syntagmes, attachement, pragmatique ; rejeu déterministe ; mesure sur gold), comment l'utiliser (3–5 exemples concrets avec la sortie attendue), ce qu'il **ne** fait pas encore (restitution, traduction, génération ; les 17 spans inatteignables ; la rouge `cascade_pos`), les performances (cache ×139, corpus 612 en ~0,6 s) et les garanties (déterminisme, hors réseau, codes de sortie).
2. Ajoute **`docs/produit/exemples.md`** (fichier neuf) : 5 exemples d'entrée/sortie réels (texte → JSON commenté), dont un cas d'échec connu (un span non prédit) — explique ce que l'utilisateur doit en conclure.
3. Vérifie que tes liens relatifs résolvent (`python3 tools/revue_documentation.py` peut être lancé, mais il exige que `docs/pilotage/en-cours.md` référence tes fichiers — ne le touche pas : signale-le dans ton résumé).
4. **N'écris que ces deux fichiers neufs.** Ne modifie aucun existant ; pas de `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, fichiers natifs. Ne commite rien.

Rends un résumé : les sections, les exemples, et la liste des liens qui resteront à déclarer dans l'état.
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

⏵ Lecture du contexte (README, état, rapports, API) avant d'écrire la doc.

- **bash** `{"command": "ls -la && echo \"---\" && ls docs/ && echo \"---\" && ls tools/ | head -50", "description": "List repo root, docs and tools"}`

  ```
total 204
drwxr-xr-x. 1 stephane stephane   660  1 nov 10:50 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   124 31 oct 18:00 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   180  6 nov 09:31 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   912  6 nov 00:08 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 19956 29 oct 08:14 README.md
drwxr-xr-x. 1 stephane stephane 70748  6 nov 01:26 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane 10507 30 sep 
… [1940 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md</path>
<type>file</type>
<content>
1: # Drave
2: 
3: > **Ce que ce document est.** La vitrine publique de Drave : la vision, les cinq axes, les deux
4: > étages, six résultats et l'état du dépôt. Les chiffres sont cités comme état ; les fiches sont
5: > dans [`reports/`](reports/). **Chargement :** T1 — ce résumé, puis la section utile.
6: 
7: **Drave est une vision de l'IA centrée sur les flots de données, pas sur le calcul brut.** Un moteur qui traite les
8: activations d'un réseau de neurones comme des **faits** — « le neurone 2 539 de la couche 23 a valu 27,8 » — et non
9: comme des cases dans une matrice. Le coût du calcul devient proportionnel à l'**activité**, pas à la taille du
10: modèle ; le modèle devient **décomposable**, **répartissable** sur du matériel divers, et **observable** — on peut le
11: tracer, le rejouer, le comparer.
12: 
13: *« Stream of logs » : le flux des listes. Et « la drave » — ces billots qu'on confiait à la rivière au printemps,
14: qu'on guidait de l'estacade jusqu'à la scierie. Le nom dit ce que fait le moteur : il ne lit pas des matrices, il
15: conduit un flux.*
16: 
17: ## L'origi
… [19635 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de l'état et des rapports clés en parallèle.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-06, 04 h 05 HNE (heure locale, EST).**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: >
8: > **Reboot du 03/11 19 h 33** : la nuit a été coupée (`kd2` **8 250/30 000**, `rope2048`
9: > **3 350/20 000**, sans checkpoint) ; les quatre sessions ont été mises en pause. **Reprise du
10: > 04/11** : hub `1e7ef596` (08 h 50), N2 09 h 41, S 09 h 46, L/B13 10 h 14 ; **N3** clos en
11: > session courte (11 h 30–11 h 38). Runbook [`plan-travail.md`](plan-travail.md) § 9 et § 12.
12: 
13: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11
14: 
15: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
16: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
17: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
18: - **Prochaine action** : **suivi docs**, puis la **passe** ap
… [10710 caractères tronqués]
  ```

- **bash** `{"command": "ls docs/produit 2>/dev/null || echo \"PAS DE DOSSIER docs/produit\"; echo \"---\"; ls reports/ | grep -Ei \"pensee|cache-chunker|audit-v10\" ; echo \"---\"; ls tools/ | grep -Ei \"drave|revue_doc|bloc_ling\"", "description": "Check product dir, reports and tools"}`

  ```
PAS DE DOSSIER docs/produit
---
native-pensee.json
pas-de-pensee-14b.json
pas-de-pensee-7b.json
pas-de-pensee-contracte-3b.json
pas-de-pensee-contracte-7b.json
pas-de-pensee-corrige-14b.json
pas-de-pensee-corrige-3b.json
pas-de-pensee-corrige-7b.json
pas-de-pensee-corrige-large.json
pas-de-pensee.json
pas-de-pensee-mlp-18.json
pas-de-pensee-mlp-6.json
pas-de-pensee-non-lineaire-3b.json
pas-de-pensee-non-lineaire-large.json
pas-de-pensee-recurrent.json
pensee-absents.json
pensee-ac3-alphabeta.json
pensee-adaptive.json
pensee-aleatoire.json
pensee-alternance.json
pensee-anaphore-103.json
pensee-anaphore-68.json
pensee-anaphore-bilan.json
pensee-anaphore-chaines.json
pensee-anaphore-corrige.json
pensee-anaphore-cv-graines.json
pensee-anaphore-cv.json
pensee-anaphore-hybride.json
pensee-anaphore.json
pensee-anaphore-kappa.json
pensee-anaphore-limite.json
pensee-anaphore-meta.json
pensee-anaphore-objets.json
pensee-anaphore-pieges.json
pensee-anaphore-pondere.json
pensee-anaphore-roles.json
pensee-anaphore-semantique.json
pensee-annotation-independante.json
pensee-asym.json
pensee-attachement-cible.json
pensee-attachement.json
pensee-attachement-parfait.json
pensee-attachement-v2.json
p
… [11970 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des rapports de référence et de l'API `bloc_linguistique.py`.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-v12.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v10.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cache-chunker-applique.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-v12.md</path>
<type>file</type>
<content>
1: # B13 — 222/222 (1,0000) : le dernier marqueur ambigu, et 17 spans inatteignables
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-06 ·
4: > **État courant** · **Verdict** : ✅ — **la cible de A17 est atteinte**.
5: > **183/183 portes** : le dernier écart était un **marqueur ambigu** — « when » après un GN est
6: > une **relative** (« The day when we left »), ailleurs une **subordonnée** (« When it rains »).
7: > Résultat : **222 labels** sur 239, **exact 222/222 = 1,0000** (fr **136/136**, en **86/86**),
8: > **couverture 0,9289**, **F1 0,5893** (union ; S 0,5014, chunker 0,6203), tête **0,7392** ;
9: > **17 spans** restants (8 REL, 5 SUB, 4 GP) — **tous inatteignables** sans corriger le gold ou
10: > le lexique (12 formes synthétiques, 4 GP du gold sans préposition, une tokenisation `qu'il`).
11: > **dev 153/153, test 69/69.**
12: >
13: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`AMBIGUES_REL`,
14: > branche REL/SUB), [`autotest.py`](../tools/pensee/autotest.py) (16 assertions) ;
15: > JSO
… [2916 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v10.md</path>
<type>file</type>
<content>
1: # Audit v10 — les chiffres rejouent, l'attribution des corrections ne rejoue pas
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
4: > **Commit audité** : `710ec7f9` (parent `160d08ca`) · **Date** : 2026-11-05 ·
5: > **Verdict** : chiffres ✅ (deux écarts), règles ❌, portes ✅ (183/183, 11 docstrings périmées).
6: > **Aucun fichier existant modifié ; aucun commit.** Sorties : ce rapport et
7: > [`pensee-audit-v10.json`](pensee-audit-v10.json).
8: 
9: **En une phrase.** Les valeurs de la fiche [`rapport-pensee-v10.md`](rapport-pensee-v10.md)
10: rejouent presque toutes : **220/220**, couverture **0,9205**, **F1 0,5880** (gelé 602),
11: **tête 0,7388**, **fr 134/134**, **en 86/86**, **19 spans** (9 REL, 6 SUB, 4 GP),
12: **top-k 219**, **183/183 portes**. Mais la fiche attribue le gain à **deux** corrections :
13: la seconde, le **`-ée`**, est **antérieure à la v10** (commit `a408a909`, déjà dans v8 et v9)
14: et **inerte sur ce gold** (0 différence d'annotation sur 612 phrases) ; `r255` reste absent
15: car `acheter` n'est
… [26659 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cache-chunker-applique.md</path>
<type>file</type>
<content>
1: # B13 — le cache du chunker appliqué : ×139 en chunker, ×1 en défaut (S domine)
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **181/181 portes** : le **O(n²)** du chunker est supprimé (1+2S → **1**, dans **les deux chemins** depuis le hoisting complet : T178) — `_syntagmes_simple` était appelé
5: > **1+2S fois** par analyse (3,21/phrase sur le corpus, 193 fois à 320 tokens), il l'est **une
6: > fois** ; les verbes de GV sont **mémoïsés par span** (`_verbe_gv`). Résultat mesuré : **×139 à
7: > 160 répétitions** sur le chemin chunker, sortie **identique** (0 différence sur 612 phrases).
8: > Sur le chemin par défaut, le gain est **×5,8 à 20 répétitions puis ×1,0** : le coût restant est
9: > chez **S** (`_segmente` appelé deux fois par phrase), pas dans le chunker.
10: >
11: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_verbe_gv`,
12: > `cache_gv`, branche chunker hoistée), [`autotest.py`](../tools/pensee/autotest.py) (T178),
13: > bancs hors dépôt ; fic
… [3497 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de l'API `bloc_linguistique.py` et du JSON v12.

- **bash** `{"command": "wc -l tools/bloc_linguistique.py reports/pensee-v12.json tools/speculatif_drave.py 2>/dev/null; echo \"---\"; python3 -c \"\nimport json\nd=json.load(open('reports/pensee-v12.json'))\ndef walk(o,p=''):\n    if isinstance(o,dict):\n        for k,v in o.items():\n            if isinstance … [276 caractères tronqués]`

  ```
2192 tools/bloc_linguistique.py
    51 reports/pensee-v12.json
   160 tools/speculatif_drave.py
  2403 total
---
/date = '2026-11-06'
/ligne = 'B13'
/portes = '183/183'
/avant/labels = 221
/avant/exact = 221
/avant/couverture = 0.9247
/avant/spans = 18
/apres/labels = 222
/apres/exact = 222
/apres/exact_span = 1.0
/apres/couverture = 0.9289
/apres/f1 = 0.5893
/apres/f1_s = 0.5014
/apres/f1_chunker = 0.6203
/apres/tete = 0.7392
/apres/fr = '136/136'
/apres/en = '86/86'
/apres/topk = 221
/apres/topk_taux = 0.9247
/apres/spans/REL = 8
/apres/spans/SUB = 5
/apres/spans/GP = 4
/apres/spans/total = 17
/apres/dev/exact = 153
/apres/dev/labels = 153
/apres/dev/couverture = 0.9387
/apres/test/exact = 69
/apres/test/labels = 69
/apres/test/couverture = 0.9079
/correction = 'AMBIGUES_REL : REL après un GN, SUB ailleurs'
/controle_negatif/permutation = '1,997/220 (0,908 %) p=0'
/controle_negatif/candidat_aleatoire = '42,14 % top-1'
/limites [list len 3 ] ['17 spans inatteignables', 'in-sample']
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/speculatif_drave.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/speculatif_drave.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """speculatif_drave.py — LE RÉFLEXE PROPOSE, LE CERVEAU VÉRIFIE — et on mesure le taux.
3: 
4: POURQUOI CE FICHIER EXISTE, ET CE QU'IL AJOUTE. `tools/speculatif.py` (8 oct) mesure le taux
5: d'acceptation entre **deux modèles HuggingFace** (un 0,5B pour un 1,5B) : c'est la mesure *avant*
6: d'écrire du moteur. Depuis la nuit du 14-15/10, il y a **autre chose à mesurer** : un **réflexe
7: entraîné dans ce dépôt** — le chemin court (8 couches sur 24) avec un lecteur appris ou un LoRA
8: distillé, exporté en GGUF, lu **par le moteur** — qui génère **deux fois plus vite** que le cerveau
9: entier mais ne produit **pas** le même texte (accord par position : 28 % à la perplexité, 51 %
10: distillé ; 0 à 5 jetons sur 96 en génération libre).
11: 
12: La question qui restait : **à quoi sert un réflexe qui se trompe ?** Réponse : à **proposer**. Le
13: réflexe propose K jetons, le cerveau en vérifie K **en une passe**, garde le préfixe ratifié et
14: corrige le premier jeton faux. C'est le décodage spéculatif — et la seule quantité qui décide de
15:
… [8221 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection de l'API publique de `bloc_linguistique.py`.

- **bash** `{"command": "sed -n 1,120p tools/bloc_linguistique.py", "description": "Read module docstring of bloc_linguistique"}`

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
… [3234 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"^def \\|^class \\|^__all__\\|^[A-Z_][A-Z_0-9]* *=\" tools/bloc_linguistique.py | head -120", "description": "List public functions and constants"}`

  ```
49:RACINE = pathlib.Path(__file__).resolve().parent.parent
50:NIVEAUX = ("graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
52:SOURCES = ("heuristique", "neuronal", "humain")
53:SCRIPT_NEUTRE = "Zyyy"
59:class Span:
68:class Etiquette:
92:class Annotation:
130:class BlocLinguistique(Protocol):
137:class RefusNeuronal(RuntimeError):
144:def _normaliser(texte: str) -> str:
148:def _trigrammes(texte: str) -> list[str]:
153:def _profil(texte: str, top: int = 200) -> dict[str, int]:
158:def charger_profils_udhr(chemin: pathlib.Path, train=(0, 14), test=(15, 30),
192:def _score_profil(tri: collections.Counter, profil: dict[str, int]) -> float:
199:def detecter_langue(texte: str, profils: dict[str, dict] | None = None,
230:def _script_char(ch: str) -> str:
256:def detecter_script(texte: str) -> str:
273:LEXIQUES = {
298:POS_FERME = {
319:VERBES = {
340:ADJECTIFS = {
350:MOTS_DOUBLE_SENS = set("canard avocat livre temps voler glace note carte point mousse manche mode "
353:SUFFIXES = ("ment", "tions", "tion", "ités", "ité", "eux", "euse", "ables", "able", "isme",
356:PREFIXES = ("re", "ré", "dé", "des", "pré", "pro", "anti", "auto", "co", "con", "in", "im",
359:CONNECT
… [2465 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la CLI actuelle du bloc et du contrat d'annotation.

- **bash** `{"command": "sed -n 2013,2192p tools/bloc_linguistique.py", "description": "Read autotest, CLI and summary functions"}`

  ```
ECHANTILLONS = {
    "fr": "Le chat de la voisine qui dort sur le toit se réveille. Va voir le chat ! "
          "Il ne dort pas, mais il a peut-être faim.",
    "en": "The cat of the neighbor who sleeps on the roof wakes up. Do you see the cat? "
          "It is not sleeping, but it may be hungry.",
    "de": "Die Katze der Nachbarin, die auf dem Dach schläft, wacht auf. Siehst du die Katze?",
    "es": "El gato de la vecina que duerme en el tejado se despierta. ¿Ves el gato?",
    "it": "Il gatto della vicina che dorme sul tetto si sveglia. Vedi il gatto?",
}


def _resume_annotation(a: Annotation) -> dict:
    par = a.par_niveau()
    return {"langue": a.langue, "script": a.script, "source": a.source, "refus": a.refus,
            "niveaux": {n: len(es) for n, es in sorted(par.items())},
            "couverture": a.couverture(),
            "fraction_semantique": round(a.fraction_semantique, 4),
            "etiquettes": len(a.etiquettes)}


def autotest(udhr: pathlib.Path, sortie: pathlib.Path | None = None) -> dict:
    """Mesure la langue, le script, la substitution, le parallèle, la cascade et l'activation."""
    rapport: dict = {"date": time.strftime("%Y-%m-%dT%H:%M:%S")
… [7488 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"cascade_pos\" --include=*.md --include=*.py --include=*.sh --include=*.txt . | head -30; echo \"---\"; grep -rn \"612\" reports/rapport-cout-chunker.md 2>/dev/null | head; echo \"---\"; grep -rn \"0,6 s\\|0.6 s\\|~0,6\" reports/*.md | head -10", "description": "Find cascade_p … [28 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-2679]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

### 🤖 Assistant

⏵ Recherche du contexte « rouge cascade_pos » dans les références de non-régression.

- **bash** `{"command": "grep -n \"cascade\" docs/pilotage/references-non-regression.md | head -20; echo \"=== fichier ===\"; sed -n 1,80p docs/pilotage/references-non-regression.md", "description": "Inspect tolerated red gates references"}`

  ```
67:| `porte-bloc-linguistique.sh` | 17 s | ❌ **rouge tolérée** (2026-11-06) : `cascade_pos` — la fusion avec le neuronal de contrat (0,7465) passe **sous** l'heuristique (0,7581) depuis que le POS contextuel a progressé ; la fusion est par confiance et le stub gagne. Correctif : calibrer `MockNeuronal` ou la priorité de niveau (prochaine session) |
=== fichier ===
# Références de non-régression

> **Passe — 2026-11-06 :** 83 portes, **79 vertes, 4 rouges** (voir la ligne `bloc-linguistique`).

> **Passe précédente — 2026-11-04 23 h 43 → 2026-11-05 02 h 12 :** **83 portes, 79 vertes,
> 4 rouges**, **2 h 29** (journaux durables `work/portes/passe-2404-23h45`), **machine au repos**
> (GPU libres, aucune réservation). Les **2 rouges structurelles connues** restent : `porte-indice`
> (1 207 s), `porte-melange` (148 s). Deux rouges nouvelles, **hors dépôt** : `porte-lecteur` (0 s)
> échouait sur une ancre du banc pilote (« < 2,5 ») que la réécriture de la roadmap du 04/11
> (« sous 2,5 ») avait rendue introuvable — **corrigée et rejouée verte** ; `porte-sessions` (0 s)
> signale les heartbeats périmés du hub et de `e181ce02` au moment de la passe — le hub l'a rafraîchi
> à 01 h 55, **`e1
… [4975 caractères tronqués]
  ```

- **bash** `{"command": "ls docs/implantation/; echo ---; grep -rn \"BlocLinguistique\\|bloc-linguistique\" docs/README.md docs/implantation/*.md 2>/dev/null | head -20", "description": "List implantation docs"}`

  ```
banc-lecture.md
bloc-code.md
bloc-linguistique.md
bloc-maths.md
bloc-tableaux.md
configuration-nvme-raid-amd.md
contexte-long.md
convertisseur.md
corpus-gele.md
diehl-cook.md
document-graph.md
encodeur-visuel.md
format-clusters.md
format-flux.md
lecteur-controleur.md
llm-externe.md
moteur-de-pensee.md
numa-segregation.md
pipeline-lecture.md
tete-balayage.md
tokenisation.md
---
docs/README.md:83:| [`implantation/bloc-linguistique.md`](implantation/bloc-linguistique.md) | le bloc linguistique : neuf niveaux, heuristique/neural, substitution, activation sémantique |
docs/implantation/bloc-linguistique.md:8:> la porte est [`porte-bloc-linguistique.sh`](../../tools/porte-bloc-linguistique.sh) ; la fiche
docs/implantation/bloc-linguistique.md:9:> est [`rapport-bloc-linguistique.md`](../../reports/rapport-bloc-linguistique.md).
docs/implantation/bloc-linguistique.md:34:![Les neuf niveaux du bloc](../schemas/bloc-linguistique-niveaux.svg)
docs/implantation/bloc-linguistique.md:80:class BlocLinguistique(Protocol):
docs/implantation/bloc-linguistique.md:179:![Substituer, paralléliser, activer](../schemas/bloc-linguistique-substitution.svg)
docs/implantation/bloc-linguistique.md:270:La porte 
… [883 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection du banc gold (`evaluer_gold.py`) pour définir les commandes.

- **bash** `{"command": "ls tools/evaluer_gold.py && wc -l tools/evaluer_gold.py && grep -n \"^def \\|^class \\|^if __name__\\|add_argument\" tools/evaluer_gold.py | head -80", "description": "Inspect evaluer_gold API and CLI"}`

  ```
[stderr]
ls: cannot access 'tools/evaluer_gold.py': No such file or directory
[exit code: 2]
  ```

- **bash** `{"command": "grep -rn \"0,6 s\\|0.6 s\\|0,6s\\|0.6s\" reports/*.md | head -20; echo \"---\"; grep -rn \"612\" reports/rapport-*.md | grep -i \"s\\b\\|seconde\\|durée\\|duree\\|temps\" | head -20", "description": "Search performance claim 0.6s for 612 corpus"}`

  ```
reports/rapport-cache-chunker.md:239:- **Cache complet (C2)** : ×1,026 sur le corpus, ×1,26-3,65 sur les longues ; **×2,06 à 160**,
reports/rapport-chargement-paresseux.md:80:(0,6 s) — d'où un `float("")` en pleine passe, à 02 h 18. C'est la passe complète qui l'a vue, pas
reports/rapport-cout-chunker.md:160:  `_syntagmes_simple` 0,023 s, `_verbe_dans` 0,006 s.
reports/rapport-cout-chunker.md:162:  0,492 s, `_est_verbe` 0,414 s (les deux se recouvrent), `_syntagmes_s` 0,036 s,
reports/rapport-cout-chunker.md:163:  `_tete_texte` 0,024 s. V2 : total **0,264 s**, `_cible_proche` 0,056 s, `_verbe_dans` 0,013 s.
reports/rapport-drvm-ppl.md:51:  notés**. Le fichier de 1 076 octets en pèse 1 077 : **1 076 sont notés**.
reports/rapport-e6-poids-lognormaux.md:62:   7,2241 · 41,6677) — mais l'avantage sur le témoin dense reste **modeste** : ×1,006 sans élagage,
reports/rapport-e9-homeostasie.md:227:* **ce que la porte ne vérifie pas** : que ×0,6 soit l'optimum **universel** ✗ — le balayage a été
reports/rapport-n2-distillation.md:59:   état contre 2,9953 sans (−0,0017), et il bat l'état **étranger** de 0,0016 sur le protocole
reports/rapport-pensee-derive.md:14:Même monde que T50, mais la fi
… [2451 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Localisation du module gold et de son API.

- **bash** `{"command": "find tools -name \"evaluer_gold*\" -o -name \"*gold*.py\" | head -20; echo ---; ls tools/pensee/ 2>/dev/null | head -40", "description": "Find evaluer_gold module"}`

  ```
tools/tests/linguistique/__pycache__/evaluer_gold.cpython-313.pyc
tools/tests/linguistique/gold.py
tools/tests/linguistique/evaluer_gold.py
tools/tests/linguistique/gold_reel.py
tools/tests/linguistique/gold_split.py
tools/tests/linguistique/gold_synthetique.py
---
audit.py
autotest.py
banc.py
coeur.py
courbe.py
cruches.py
csp.py
graines.py
__init__.py
jeux.py
moteur.py
operateurs.py
__pycache__
store.py
taquin.py
trace.py
  ```

- **bash** `{"command": "sed -n 1,80p reports/rapport-audit-attachement.md", "description": "Read attachment audit header and timing"}`

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
… [3917 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du banc gold : fonctions, structure de sortie, CLI.

- **bash** `{"command": "wc -l tools/tests/linguistique/evaluer_gold.py; grep -n \"^def \\|^class \\|^if __name__\\|add_argument\" tools/tests/linguistique/evaluer_gold.py", "description": "Inspect evaluer_gold structure"}`

  ```
305 tools/tests/linguistique/evaluer_gold.py
24:def charger() -> list[dict]:
38:def charger_gele() -> list[dict]:
47:def par_source(phrases: list[dict], source: str) -> list[dict]:
51:def _pos_map(a: bl.Annotation) -> dict[tuple[int, int], str]:
55:def _seg(a: bl.Annotation) -> set[tuple[str, int, int]]:
59:def _tete(a: bl.Annotation) -> set[tuple[str, int]]:
64:def _pragma(a: bl.Annotation) -> dict:
72:def _prf(tp: int, fp: int, fn: int) -> dict:
80:def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
225:def main() -> int:
227:    ap.add_argument("--json", default="")
228:    ap.add_argument("--reel", action="store_true")
304:if __name__ == "__main__":
  ```

- **bash** `{"command": "grep -rn \"analyser\\|evaluer_bloc\\|rejouer\" docs/implantation/bloc-linguistique.md | head -20; echo \"=== 240-340 ===\"; sed -n 240,340p docs/implantation/bloc-linguistique.md", "description": "Read bloc-linguistique contract sections"}`

  ```
82:    def analyser(self, texte: str, langue: str | None = None,
97:`analyser` et `Annotation` ; il ne sait pas si l'étiquette vient d'un CPU, d'un mock ou d'un
116:- **syntagme** : le **générateur de la coloration** (`generateur.analyser`) est importé en
186:annotation = bloc.analyser(texte, langue="fr")
=== 240-340 ===
pas sur le texte entier. Une heuristique fausse, elle, coûte plus qu'un appel réseau : la
confiance et la porte sont le garde-fou.

## 8. Le multilingue : 398 langues au niveau langue

Le bloc ne prétend pas étiqueter 398 langues au niveau du syntagme. Il sépare :

- **universel** : Unicode, script, frontières de phrase, classes de caractères — indépendant de
  la langue ;
- **famille** : les classes fermées et les affixes partagés (latin, germanique, roman) ;
- **langue** : les profils de trigrammes et les paquets de classes fermées.

La mesure UDHR (articles 0–14 pour les profils, article 15 tenu à l'écart) :

| mesure | résultat |
|---|---|
| langues avec profil | **398** |
| articles de test | **447** |
| **accuracy langue** | **0,9687** |
| **accuracy script** | **1,0000** |
| contrôle **profils permutés** | **0,0022** (proche du hasard) |
| construction des p
… [4970 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture complète du banc gold pour produire des exemples réels.

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
… [15928 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Exécution d'analyses réelles pour capturer les sorties exactes.

- **bash** `{"command": "sed -n 105,145p tools/bloc_linguistique.py", "description": "Read Annotation.json schema"}`

  ```
def par_niveau(self) -> dict[str, list[Etiquette]]:
        sortie: dict[str, list[Etiquette]] = collections.defaultdict(list)
        for e in self.etiquettes:
            sortie[e.niveau].append(e)
        return dict(sortie)

    def couverture(self) -> dict[str, float]:
        """La confiance maximale par niveau — la couverture *déclarée*, pas une précision."""
        return {n: round(max((e.confiance for e in es), default=0.0), 4)
                for n, es in self.par_niveau().items()}

    def json(self, avec_duree: bool = False) -> dict:
        cout = dict(self.cout)
        if not avec_duree:
            cout.pop("duree_s", None)
        return {
            "texte": self.texte, "langue": self.langue, "script": self.script,
            "source": self.source, "refus": self.refus,
            "etiquettes": [e.json() for e in self.etiquettes],
            "unites_semantiques": [u.json() for u in self.unites_semantiques],
            "fraction_semantique": round(float(self.fraction_semantique), 4),
            "trace": list(self.trace), "cout": cout, "contexte": self.contexte,
        }


class BlocLinguistique(Protocol):
    nom: str

    def analyser(self, texte: str, lang
… [418 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/bloc_linguistique.py --texte \"Le chat de la voisine qui dort sur le toit se réveille.\" --json 2>&1 | head -80", "description": "Run heuristic analysis on French sentence"}`

  ```
{
 "texte": "Le chat de la voisine qui dort sur le toit se réveille.",
 "langue": "fr",
 "script": "Latn",
 "source": "heuristique",
 "refus": "",
 "etiquettes": [
  {
   "niveau": "graphème",
   "type": "lettres",
   "valeur": "Le",
   "debut": 0,
   "fin": 2,
   "source": "heuristique",
   "confiance": 0.99,
   "candidats": [],
   "langue": "fr",
   "script": "Latn",
   "meta": {}
  },
  {
   "niveau": "mot",
   "type": "mot",
   "valeur": "Le",
   "debut": 0,
   "fin": 2,
   "source": "heuristique",
   "confiance": 0.98,
   "candidats": [],
   "langue": "fr",
   "script": "Latn",
   "meta": {}
  },
  {
   "niveau": "pos",
   "type": "DET",
   "valeur": "Le",
   "debut": 0,
   "fin": 2,
   "source": "heuristique",
   "confiance": 0.92,
   "candidats": [],
   "langue": "fr",
   "script": "Latn",
   "meta": {
    "ouvert": false
   }
  },
  {
   "niveau": "syntagme",
   "type": "GN",
   "valeur": "Le chat",
   "debut": 0,
   "fin": 7,
   "source": "heuristique",
   "confiance": 0.4,
   "candidats": [
    "« qui dort sur le toit » → voisine",
    "« qui dort sur le toit » → Le chat",
    "réveille",
    "voisine",
    "chat"
   ],
   "langue": "fr",
   "script": "Latn",
   "meta": {
… [232 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Capture de plusieurs sorties (POS, syntagmes, pragmatique, attachement).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && mkdir -p /tmp/doc_produit && for t in \"Le chat de la voisine qui dort sur le toit se réveille.\" \"Va voir le chat !\" \"Le chat dort-il ?\" \"The cat of the neighbor who sleeps on the roof wakes up.\" \"Il ne dort pas, mais il a pe … [249 caractères tronqués]`

  ```
=== Le chat de la voisine qui dort sur le toit se réveille.
=== Va voir le chat !
=== Le chat dort-il ?
=== The cat of the neighbor who sleeps on the roof wakes up.
=== Il ne dort pas, mais il a peut-être faim.
total 64
drwxr-xr-x.   2 stephane stephane   140  6 nov 09:35 .
drwxrwxrwt. 219 root     root     19700  6 nov 09:35 ..
-rw-r--r--.   1 stephane stephane 16098  6 nov 09:35 0e17c859.json
-rw-r--r--.   1 stephane stephane  6697  6 nov 09:35 46891ad7.json
-rw-r--r--.   1 stephane stephane 14516  6 nov 09:35 4e6be2c1.json
-rw-r--r--.   1 stephane stephane 13694  6 nov 09:35 74211b3e.json
-rw-r--r--.   1 stephane stephane  5806  6 nov 09:35 7963ee00.json
  ```

- **bash** `{"command": "cd /tmp/doc_produit && python3 - <<'PY'\nimport json,glob\nfor f in sorted(glob.glob('*.json')):\n    d=json.load(open(f))\n    print('='*80)\n    print(f, '|', d['texte'], '| langue', d['langue'], d['script'], '| refus', repr(d['refus']))\n    for e in d['etiquettes']:\n        print(f … [313 caractères tronqués]`

  ```
================================================================================
0e17c859.json | Le chat de la voisine qui dort sur le toit se réveille. | langue fr Latn | refus ''
  graphème     lettres        'Le'                                       [0:2] conf=0.99 cand=[] meta={}
  mot          mot            'Le'                                       [0:2] conf=0.98 cand=[] meta={}
  pos          DET            'Le'                                       [0:2] conf=0.92 cand=[] meta={'ouvert': False}
  syntagme     GN             'Le chat'                                  [0:7] conf=0.4 cand=['« qui dort sur le toit » → voisine', '« qui dort sur le toit » → Le chat', 'réveille', 'voisine', 'chat'] meta={'role': 'agent', 'niveau': 1, 'attachement': {'segment': 'Le chat', 'cible': 'réveille'}}
  discours     paragraphe     'suite'                                    [0:55] conf=0.5 cand=['suite', 'contraste', 'cause', 'conséquence'] meta={}
  document     paragraphe     'Le chat de la voisine qui dort sur le '   [0:55] conf=0.7 cand=[] meta={}
  phrase       type           'déclarative'                              [0:55] conf=0.85 cand=[] meta={}
  pragmatique  acte           'a
… [25960 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction des phrases d'échec connues (r303, s037) depuis le gold.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib\nfor f in [\"gold.json\",\"gold_reel.json\",\"gold_synthetique.json\"]:\n    d=json.load(open(\"tools/tests/linguistique/\"+f))\n    for p in d[\"phrases\"]:\n        if p.get(\"id\") in (\"r303 … [494 caractères tronqués]`

  ```
gold_reel.json r153 | We wait for the bus. | langue en
   seg GN 0 2 'We' cible= None cibles= None
   seg GV 3 7 'wait' cible= None cibles= None
   seg GP 8 19 'for the bus' cible= wait cibles= ['wait']
   mots [(0, 2, 'PRON'), (3, 7, 'VERB'), (8, 11, 'PREP'), (12, 15, 'DET'), (16, 19, 'NOUN')]
gold_reel.json r241 | The day when we left was beautiful. | langue en
   seg GN 0 7 'The day' cible= None cibles= None
   seg REL 8 20 'when we left' cible= day cibles= ['day']
   seg GV 21 24 'was' cible= None cibles= None
   seg ADJ 25 34 'beautiful' cible= None cibles= None
   mots [(0, 3, 'DET'), (4, 7, 'NOUN'), (8, 12, 'PRON'), (13, 15, 'PRON'), (16, 20, 'VERB'), (21, 24, 'AUX'), (25, 34, 'ADJ')]
gold_reel.json r303 | Je pars car il est tard. | langue fr
   seg GN 0 2 'Je' cible= None cibles= None
   seg GV 3 7 'pars' cible= None cibles= None
   seg SUB 8 23 'car il est tard' cible= pars cibles= ['pars']
   mots [(0, 2, 'PRON'), (3, 7, 'VERB'), (8, 11, 'CONJ'), (12, 14, 'PRON'), (15, 18, 'AUX'), (19, 23, 'ADV')]
gold_synthetique.json s037 | Paul qui marche marche | langue fr
   seg GN 0 4 'Paul' cible= None cibles= None
   seg REL 5 15 'qui marche' cible= Paul cibles= ['Paul']
   seg GV
… [116 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rejeu des cas d'échec et mesure du corpus 612 (durée, déterminisme).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for t in \"Je pars car il est tard.\" \"Paul qui marche marche\"; do echo \"### $t\"; python3 tools/bloc_linguistique.py --texte \"$t\" --json | python3 -c \"\nimport json,sys\nd=json.load(sys.stdin)\nprint('langue',d['langue'],'refu … [346 caractères tronqués]`

  ```
### Je pars car il est tard.
langue fr refus ''
pos          PRON       'Je'                                 [0:2] conf=0.92 cand=[] meta={'ouvert': False}
syntagme     GV         'Je pars'                            [0:7] conf=0.55 cand=['« tard » → il est', 'est'] meta={'role': 'predicat', 'niveau': 0}
phrase       type       'déclarative'                        [0:24] conf=0.85 cand=[] meta={}
pragmatique  acte       'assertion'                          [0:24] conf=0.45 cand=['assertion', 'question', 'ordre'] meta={}
pos          VERB       'pars'                               [3:7] conf=0.72 cand=['verb'] meta={'ouvert': True}
syntagme     GV         'pars'                               [3:7] conf=0.3 cand=['GV'] meta={'role': 'prédicat', 'niveau': 0, 'union': True}
pos          CONJ       'car'                                [8:11] conf=0.92 cand=[] meta={'ouvert': False}
syntagme     SUB        'car il est tard'                    [8:23] conf=0.3 cand=['SUB', 'pars', 'est', 'pars'] meta={'role': 'complément', 'niveau': 1, 'union': True, 'attachement': {'segment': 'car il est tard', 'cible': 'pars'}}
pos          PRON       'il'                                 [12:14] conf=0.9
… [2147 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys,time\nsys.path.insert(0,'.')\nfrom tools.bloc_linguistique import Heuristique\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\nphr=charger()\nh=Heuristique()\nt=time.perf_counter( … [896 caractères tronqués]`

  ```
phrases 612 duree totale 0.359 s
pos 0.7581 syntagme f1 0.5849 tete f1 0.7336
pragma {'acte': 0.9967, 'negation': 0.9771, 'modalite': 0.9886, 'double_sens': 0.9444}
attachement {'cibles': 239, 'labels': 222, 'top1': 222, 'topk': 221, 'exact': 222, 'couverture': 0.9289, 'exact_taux_span': 1.0, 'topk_taux': 0.9247, 'topk_exact': 221, 'exact_any': 222}
attachement_tete {'cibles': 222, 'labels': 222, 'top1': 222, 'topk': 221, 'top1_taux': 1.0, 'topk_taux': 0.9955, 'couverture': 1.0}
rejeu identique: True
sha256 1fb044e285c2081e
  ```

### 🤖 Assistant

⏵ Énumération des 17 spans non prédits à l'état courant.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'.')\nfrom tools.bloc_linguistique import Heuristique\nfrom tools.tests.linguistique.evaluer_gold import charger\nphr=charger(); h=Heuristique(); manquants=[]\nfor p in phr:\n    a=h.an … [647 caractères tronqués]`

  ```
17
Counter({'REL': 8, 'SUB': 5, 'GP': 4})
('g017', 'hand', 'en', 'SUB', 9, 28, 'that she would come', 'said', 'She said that she would come yesterday.')
('r035', 'reel', 'en', 'REL', 9, 24, 'she talks about', 'film', 'The film she talks about is out.')
('r255', 'reel', 'fr', 'REL', 11, 27, "que j'ai achetée", 'voiture', "La voiture que j'ai achetée roule.")
('r264', 'reel', 'fr', 'SUB', 8, 26, "qu'il vient demain", 'sais', "Je sais qu'il vient demain.")
('s010', 'synthetique', 'fr', 'REL', 10, 18, 'qui nage', 'chemin', 'un chemin qui nage prépare')
('s027', 'synthetique', 'fr', 'GP', 31, 33, 'il', 'marche', 'mon sombre village marche avec il')
('s035', 'synthetique', 'fr', 'REL', 10, 19, 'qui ferme', 'papier', 'un papier qui ferme observe')
('s044', 'synthetique', 'fr', 'SUB', 17, 29, 'que ils crie', 'nage', 'une fenêtre nage que ils crie')
('s061', 'synthetique', 'fr', 'REL', 9, 18, 'qui saute', 'nuage', 'ce nuage qui saute observe')
('s065', 'synthetique', 'fr', 'REL', 5, 17, 'qui commence', 'elle', 'elle qui commence nage')
('s112', 'synthetique', 'fr', 'SUB', 24, 39, 'que Lucas ferme', 'nage', 'la brillante forêt nage que Lucas ferme')
('s114', 'synthetique', 'fr', 'SUB', 22, 4
… [600 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du hors-réseau, des refus et du format de sortie.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"urllib\\|http\\|socket\\|requests\" tools/bloc_linguistique.py | head -20; echo \"=== refus ===\"; grep -n \"refus\" tools/bloc_linguistique.py | head -30", "description": "Check network usage and refusal cases"}`

  ```
45:import urllib.request
550:        motif = re.compile(r"\b[ldmtsnLDMTNS]['’](?=\w)|\w+(?:['’\-]\w+)*|\d+(?:[.,]\d+)*|https?://\S+|[\U0001F300-\U0001FAFF]|[^\w\s]")
554:            if t.startswith(("http://", "https://")):
1416:    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18081",
1447:        requete = urllib.request.Request(
1451:        with urllib.request.urlopen(requete, timeout=self.timeout) as reponse:
1545:    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18082",
1581:        requete = urllib.request.Request(
1585:        with urllib.request.urlopen(requete, timeout=self.timeout) as reponse:
1725:    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18082",
1751:        requete = urllib.request.Request(
1755:        with urllib.request.urlopen(requete, timeout=self.timeout) as reponse:
=== refus ===
97:    refus: str = ""
122:            "source": self.source, "refus": self.refus,
138:    """Le modèle n'a pas rendu une annotation exploitable — le contrat refuse, il n'invente pas."""
1009:            return Annotation(texte=texte, refus="vide", source=self.nom,
1010:    
… [1552 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"### vide\"; python3 tools/bloc_linguistique.py --texte \"\" --json | head -20; echo \"### ponctuation\"; python3 tools/bloc_linguistique.py --texte \"... !!! ???\" --json | head -20; echo \"### langue inconnue\"; python3 tools … [131 caractères tronqués]`

  ```
### vide
{
 "texte": "",
 "langue": "und",
 "script": "Zyyy",
 "source": "heuristique",
 "refus": "vide",
 "etiquettes": [],
 "unites_semantiques": [],
 "fraction_semantique": 0.0,
 "trace": [
  {
   "etape": "refus",
   "raison": "vide"
  }
 ],
 "cout": {
  "octets": 0
 },
 "contexte": ""
}
### ponctuation
{
 "texte": "... !!! ???",
 "langue": "und",
 "script": "Zyyy",
 "source": "heuristique",
 "refus": "vide",
 "etiquettes": [],
 "unites_semantiques": [],
 "fraction_semantique": 0.0,
 "trace": [
  {
   "etape": "refus",
   "raison": "vide"
  }
 ],
 "cout": {
  "octets": 11
 },
 "contexte": ""
}
### langue inconnue
{
 "texte": "qqqqq zzzzz wwwww",
 "langue": "und",
 "script": "Latn",
 "source": "heuristique",
 "refus": "",
 "etiquettes": [
  {
   "niveau": "graphème",
   "type": "lettres",
   "valeur": "qqqqq",
   "debut": 0,
  ```

### 🤖 Assistant

⏵ Inspection des règles de la revue de documentation.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,90p tools/revue_documentation.py; echo \"=== checks ===\"; grep -n \"def \\|en-cours\\|docs/produit\\|lien\\|LIEN\\|taille\" tools/revue_documentation.py | head -60", "description": "Read documentation review rules"}`

  ```
#!/usr/bin/env python3
"""revue_documentation.py — LA REVUE DE FIN DE SOUS-CHANTIER (AGENTS.md §4).

Ce qu'elle vérifie, et qu'il faut corriger AVANT le commit de clôture :
  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
  2. structure  : les sept chantiers de en-cours.md ont leur entrée, leur état et leur fiche ;
  3. annotation : les liens relatifs des docs/ et reports/ résolvent, et leur libellé ne
     ment pas sur la cible ; les sources externes sont citées ;
  4. fraîcheur  : en-cours.md date du dernier commit, ET aucun fait n'a été commité après
     le dernier état (comparaison de commits, pas de dates : voir verifie_etat_a_jour.py) ;
  5. cohérence  : la synthèse (index.md) liste les huit chapitres, le chapitre 7 et B10–B12 ;
     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
  6. vocabulaire : « jeton » ne désigne **jamais** la représentation sémantique neutre (RSN) ;
  7. navigation : aucun document vivant n'est orphelin, et aucun chemin en code inline
     ne pointe vers un fichier absent (hors gabarits `AAAA`, `<...>`, `*`).

Sortie : un rapport lisible, code 0 si tout passe, 1 sinon (u
… [4631 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 120,270p tools/revue_documentation.py", "description": "Read review main checks including links/orphans"}`

  ```
def extrait_entier(texte: str, motif: str):
    m = re.search(motif, texte)
    return int(m.group(1)) if m else None


def main() -> int:
    alertes: list[str] = []
    en = RACINE / "docs/pilotage/en-cours.md"
    if not en.exists():
        print("✗ docs/pilotage/en-cours.md absent")
        return 1
    t = en.read_text()

    # 2. les sept chantiers
    ids = sorted(set(re.findall(r"\*\*(C[1-7])\*\*", t)))
    if len(ids) < 7:
        alertes.append(f"structure : {len(ids)} chantiers sur 7 dans en-cours.md ({ids})")

    # 4. fraîcheur : la date de la page, ET aucun fait commité après le dernier état.
    #    La date seule ne suffit pas : deux commits du même jour passaient (A8.0, 29/10).
    m = re.search(r"Mis à jour : (\d{4}-\d\d-\d\d)", t)
    if not m:
        alertes.append("fraîcheur : en-cours.md n'a pas de date « Mis à jour : AAAA-MM-JJ »")
    else:
        page, dernier = m.group(1), date_dernier_commit()
        if dernier and page != dernier:
            alertes.append(
                f"fraîcheur : en-cours.md dit {page}, le dernier commit date du {dernier}"
            )
    retard = retards(RACINE)
    if retard and not etat_modifie(RACINE):
        etat, _fa
… [5521 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de la version, de l'état git et de l'arrivée éventuelle de `drave.py`.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git branch --show-current && git log -1 --format='%h %ad %s' --date=short && git status --porcelain | head -30; echo \"=== version ===\"; find . -maxdepth 2 -iname \"VERSION\" -o -maxdepth 2 -name \"pyproject.toml\" -o -maxdepth 2 -n … [210 caractères tronqués]`

  ```
s/v7
bdeca168 2026-11-06 ÉTAT — OBJECTIF 09 H 30 → 12 H : LE PREMIER PRODUIT (CLI, SMOKE TEST, DOC D'USAGE, PORTE, FILE DES TÂCHES EN SOUS-AGENTS)
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
D  journal/2026-11-06/mesures.md
D  journal/2026-11-06/modele.md
D  journal/2026-11-06/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
D  journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/digest.md
D  journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/rapport.md
D  journal/sessions/1555bdd3-27e9-4779-b1e7-716e32399c11/digest.md
D  journal/sessions/1555bdd3-27e9-4779-b1e7-716e32399c11/rapport.md
D  journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/digest.md
D  journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6c
… [411 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nfor f in ['reports/pensee-v12.json','reports/pensee-cache-chunker-applique.json','reports/pensee-audit-v10.json']:\n    d=json.load(open(f)); print(f, list(d)[:12])\n\"; echo \"=== 0.45/0.55 ===\"; grep -n … [126 caractères tronqués]`

  ```
reports/pensee-v12.json ['date', 'ligne', 'portes', 'avant', 'apres', 'correction', 'controle_negatif', 'limites']
reports/pensee-cache-chunker-applique.json ['date', 'ligne', 'portes', 'chunker', 'defaut', 'egalite', 'appels', 'limites']
reports/pensee-audit-v10.json ['rapport', 'ligne', 'branche', 'commit_audite', 'commit_parent', 'date', 'objet', 'methode', 'verdict', 'rejeu', 'ablations', 'controle_negatif']
=== 0.45/0.55 ===
15:> gold inchangé (612 phrases : 20 `hand` + 432 `reel` + 160 synthétiques). Durée : 0,45–0,55 s.
  ```

### 🤖 Assistant

⏵ Lecture du commit « premier produit » pour le contrat CLI attendu.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat bdeca168 | head -60", "description": "Inspect the first-product commit"}`

  ```
commit bdeca168b4503171ce80ca8f2c9de02d8c9fc2c1
Author: Stéphane <stephane@localhost>
Date:   Fri Nov 6 09:31:32 2026 -0500

    ÉTAT — OBJECTIF 09 H 30 → 12 H : LE PREMIER PRODUIT (CLI, SMOKE TEST, DOC D'USAGE, PORTE, FILE DES TÂCHES EN SOUS-AGENTS)

 docs/pilotage/en-cours.md                          |   2 +-
 journal/2026-11-06/README.md                       |  11 +-
 journal/2026-11-06/distribue.md                    |   9 +-
 journal/2026-11-06/docs.md                         |   6 +-
 journal/2026-11-06/mesures.md                      |   6 +-
 journal/2026-11-06/modele.md                       |   6 +-
 journal/2026-11-06/portes.md                       |   6 +-
 journal/README.md                                  |   6 +-
 .../14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/digest.md | 337 +++++++++++++++++++
 .../rapport.md                                     |  57 ++++
 .../1555bdd3-27e9-4779-b1e7-716e32399c11/digest.md | 304 +++++++++++++++++
 .../rapport.md                                     |  65 ++++
 journal/sessions/MANIFEST.md                       |   8 +-
 .../a0d33fb7-37a9-4834-8a94-0da119e3b18f/digest.md | 351 ++++++++++++++++++++
 .../rapport.md                         
… [359 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat journal/2026-11-06/README.md", "description": "Read today's journal for product plan"}`

  ```
# 2026-11-06

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-06/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**16 commits** · **7 session(s)** · **5 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 7 | [distribue.md](distribue.md) |
| docs | 2 | [docs.md](docs.md) |
| mesures | 3 | [mesures.md](mesures.md) |
| modele | 1 | [modele.md](modele.md) |
| portes | 3 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `14114f3d-ae0d-416e-ad8e-4d4eaa04c36c` | Tu travailles dans le dépôt | 2026-11-06 09:31 | 0.0 h | [rapport](../sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/rapport.md) · [digest](../sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/digest.md) |
| `1555bdd3-27e9-4779-b1e7-716e32399c11` | Tu travailles dans le dépôt | 2026-11-06 09:31 | 0.0 h | [rapport](../sessions/1555bdd3-27e9-4779-b1e7-716e32399c11/rapport.md) · [digest](../sessions/1555bdd3-27e9-4779-b1e7-716e32399c11/d
… [5403 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du déterminisme, de la cascade et du banc `evaluer_gold.py`.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for i in 1 2 3; do python3 tools/bloc_linguistique.py --texte \"Le chat de la voisine qui dort sur le toit se réveille.\" --json | sha256sum; done; echo \"--- avec duree ---\"; python3 tools/bloc_linguistique.py --texte \"Le chat de  … [203 caractères tronqués]`

  ```
b99dd497e034cc9bd3cd5b41f77930c70a6f81ae74a355cdd2e594b69720f52e  -
b99dd497e034cc9bd3cd5b41f77930c70a6f81ae74a355cdd2e594b69720f52e  -
b99dd497e034cc9bd3cd5b41f77930c70a6f81ae74a355cdd2e594b69720f52e  -
--- avec duree ---
{'octets': 56, 'caracteres': 55, 'etiquettes': 59, 'duree_s': 0.00642}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -f \"elapsed %e s\" python3 tools/tests/linguistique/evaluer_gold.py > /tmp/doc_produit/evaluer.txt 2>/tmp/doc_produit/evaluer.err; echo \"exit=$?\"; tail -5 /tmp/doc_produit/evaluer.err; head -40 /tmp/doc_produit/evalu … [54 caractères tronqués]`

  ```
exit=1
Command exited with non-zero status 1
elapsed 4.37 s
{
 "parallele": {
  "all": {
   "bloc": "parallele",
   "phrases": 612,
   "pos": {
    "exactitude": 0.7465,
    "exactitude_ferme": 0.9004,
    "exactitude_ouvert": 0.6007,
    "tokens": 3179,
    "confusions": {
     "ADJ": {
      "ADJ": 50,
      "NOUN": 80,
      "VERB": 4
     },
     "ADV": {
      "ADV": 117,
      "NOUN": 20,
      "PREP": 2,
      "ADJ": 1,
      "?": 1
     },
     "AUX": {
      "PREP": 4,
      "AUX": 118,
      "?": 3,
      "NOUN": 3
     },
     "CONJ": {
      "CONJ": 44,
      "PRON": 25,
      "DET": 12,
      "?": 13,
      "PREP": 2,
      "NOUN": 2
     },
     "DET": {
      "DET": 586,
      "?": 2
  ```

- **bash** `{"command": "cd /tmp/doc_produit && python3 - <<'PY'\nimport re,json\nt=open('evaluer.txt').read()\n# le fichier est tronqué par le print à 2500 chars ; regardons la fin\nprint(t[-1800:])\nPY", "description": "Inspect gold evaluation tail/verdicts"}`

  ```
aux": 0.8661,
    "exact_taux": 0.8703,
    "exact_any": 208,
    "exact_any_taux_span": 1.0,
    "top1_taux_span": 1.0,
    "topk_taux_span": 0.9952,
    "topk_exact": 207,
    "topk_exact_taux": 0.8661,
    "topk_exact_taux_span": 0.9952,
    "exact_taux_span": 1.0,
    "verbe": {
     "cibles": 138,
     "justes": 138,
     "taux": 1.0
    },
    "nom": {
     "cibles": 70,
     "justes": 70,
     "taux": 1.0
    },
    "couverture": 0.8703,
    "par_langue": {
     "fr": {
      "cibles": 151,
      "labels": 122,
      "exact": 122,
      "topk": 121,
      "exact_taux_span": 1.0
     },
     "en": {
      "cibles": 88,
      "labels": 86,
      "exact": 86,
      "topk": 86,
      "exact_taux_span": 1.0
     }
    }
   },
   "attachement_tete": {
    "cibles": 208,
    "labels": 208,
    "top1"
heuristique all: {"pos": {"exactitude": 0.7581, "exactitude_ferme": 0.9004, "exactitude_ouvert": 0.6234, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 50, "NOUN": 80, "VERB": 4}, "ADV": {"ADV": 117, "NOUN": 20, "PREP": 2, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 118, "?": 3, "NOUN": 3}, "CONJ": {"CONJ": 44, "PRON": 25, "DET": 12, "?": 13, "PREP": 2, "NOUN": 2}, "DET": {"DET": 586, 
… [599 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Calcul d'un rapport d'évaluation concis et du cas d'échec `r035`.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'.')\nfrom tools.bloc_linguistique import Heuristique, Cascade, MockNeuronal\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\nphr=charger(); h=Heuristique … [834 caractères tronqués]`

  ```
heuristique POS 0.7581 F1 0.5849 tete 0.7336 att 222 / 222 couv 0.9289 acte 0.9967 frac 0.5537
cascade POS 0.7465 F1 0.6141 tete 0.7432 att 208 / 208 couv 0.8703 acte 0.9967 frac 0.5834
cascade_pos False
cascade_syntagme True
topk 221 0.9247
fr {'cibles': 151, 'labels': 136, 'exact': 136, 'topk': 135, 'exact_taux_span': 1.0} en {'cibles': 88, 'labels': 86, 'exact': 86, 'topk': 86, 'exact_taux_span': 1.0}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/bloc_linguistique.py --texte \"The film she talks about is out.\" --json | python3 -c \"\nimport json,sys\nd=json.load(sys.stdin)\nprint('langue',d['langue'],'refus',repr(d['refus']))\nfor e in d['etiquettes']:\n    if  … [257 caractères tronqués]`

  ```
langue en refus ''
pos       DET    'The'                                  [0:3] conf=0.92 cand=[] meta={'ouvert': False}
syntagme  GN     'The film she'                         [0:12] conf=0.35 cand=['GN', 'talks', 'out'] meta={'role': 'groupe nominal', 'niveau': 0, 'attachement': {'segment': 'The film she', 'cible': 'talks'}}
pos       NOUN   'film'                                 [4:8] conf=0.3 cand=['noun'] meta={'ouvert': True}
pos       PRON   'she'                                  [9:12] conf=0.92 cand=[] meta={'ouvert': False}
pos       NOUN   'talks'                                [13:18] conf=0.3 cand=['noun'] meta={'ouvert': True}
syntagme  GV     'talks'                                [13:18] conf=0.35 cand=['GV'] meta={'role': 'prédicat', 'niveau': 0}
pos       PREP   'about'                                [19:24] conf=0.92 cand=[] meta={'ouvert': False}
syntagme  GV     'about is out'                         [19:31] conf=0.35 cand=['GV'] meta={'role': 'prédicat', 'niveau': 0}
pos       AUX    'is'                                   [25:27] conf=0.92 cand=[] meta={'ouvert': False}
pos       NOUN   'out'                                  [28:31] conf=0.3 cand=['noun'] met
… [18 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche de toute spécification existante du CLI `drave.py`.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"drave\\.py\" --include=*.md --include=*.sh --include=*.py --include=*.txt . 2>/dev/null | grep -v \"^./tools/docwatch\" | head -30; echo \"=== portes ===\"; ls tools/porte-*drave* tools/porte-*produit* 2>/dev/null || echo  … [74 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-2755]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show bdeca168 -- docs/pilotage/en-cours.md; echo \"=== journal rapport e181 ===\"; grep -n -i \"produit\\|CLI\\|drave\" journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md 2>/dev/null | head -20", "description": "Inspec … [32 caractères tronqués]`

  ```
commit bdeca168b4503171ce80ca8f2c9de02d8c9fc2c1
Author: Stéphane <stephane@localhost>
Date:   Fri Nov 6 09:31:32 2026 -0500

    ÉTAT — OBJECTIF 09 H 30 → 12 H : LE PREMIER PRODUIT (CLI, SMOKE TEST, DOC D'USAGE, PORTE, FILE DES TÂCHES EN SOUS-AGENTS)

diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 22294bf8..5a8f776e 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-06, 04 h 05 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-06, 09 h 35 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
=== journal rapport e181 ===
29:- **Ambition** : faire de Drave un **runtime cognitif** où penser est une **recherche tracée** sur
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/ && sed -n 1,120p journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md 2>/dev/null", "description": "Read parent session plan"}`

  ```
digest.md
plan.md
rapport.md
session.v4.jsonl.zstd
# Plan de session — Pensée, la RSN plurielle et le moteur N3

> **Mandat vivant.** Ouvert le 2026-10-31 22 h 45 HAE depuis
> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md). Ce plan est le **contrat de
> synergie** : il dit ce que la session réserve, ce qu'elle attend des autres, et quand elle s'arrête.
> Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.

- **Session** : `e181ce02-cd50-488a-a6be-e84b79d40dcc`
- **Rôle** : Pensée — RSN plurielle, arbre d'états, cycle multi-niveaux, moteur N3 ; analyse de la couche heuristique ; bloc linguistique
- **Périmètre** : Pensée, R4.4-reste, Coloration, Bloc linguistique (R0.7)
- **Fichiers réservés** : `docs/theorie/pensee-iterative.md`, `docs/schemas/pensee-*.svg`,
  `docs/implantation/moteur-de-pensee.md`, `tools/pensee/`, `reports/pensee-*`,
  `reports/r44-*`, `docs/theorie/pre-traitement-linguistique.md`,
  `docs/schemas/heuristique-*.svg`, `tools/bloc_linguistique.py`,
  `tools/porte-bloc-linguistique.sh`, `tools/tests/linguistique/`,
  `docs/implantation/bloc-linguistique.md`, `docs/schemas/bloc-linguistique-*.svg`,
  `reports/bloc-*`, `journal/sess
… [5576 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-2755", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **job_kill** `{"job_id": "bash-2755", "reason": "grep trop lent ; recherche ciblée avec l'outil dédié"}`

  ```
requested cancellation of job bash-2755
  ```

- **grep** `{"pattern": "tools/drave\\.py|drave\\.py", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs"}`

  ```
Found 2 matches

docs/archive/etat-cerveau.md
Line 204: `porte-cycle-c2.sh` · `porte-speculatif.sh` · `speculatif_drave.py` (le réflexe propose, le cerveau

docs/archive/cerveau-facultes.md
Line 38: | **langage / décodage** | le modèle + **le réflexe qui PROPOSE, le cerveau qui VÉRIFIE** (`tools/speculatif_drave.py`) | réflexe : **×2,0** de débit, TTFT **÷3,1** ; **taux d'acceptation 2,4 à 30 %** (K = 4) et **75 %** (K = 1) pour le distillé, **0 %** pour la tête non entraînée ; gain net **0,95** au mieux — **sous 1** | — | 🟡 (mécanisme exécutable, rentabilité non atteinte : il manque ~×1,5) |
  ```

### 🤖 Assistant

⏵ Lecture de l'index `docs/README.md` et du style des documents voisins.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md</path>
<type>file</type>
<content>
1: # La documentation de [Drave](theorie/glossaire/entrees/drave.md) — quatre familles
2: 
3: > **`docs/` dit ce qui reste vrai** : la méthode, l'[état](theorie/glossaire/entrees/etat.md), la théorie, l'implantation. Les **chiffres** et les
4: > séries vivent dans [`reports/`](../reports/) ; le **récit daté** dans [`journal/`](../journal/). Une page de
5: > `docs/` qui se remplit de tableaux de mesures **déménage** dans `reports/`.
6: 
7: > **Chargement facultatif.** Aucun document de ce dossier n'est nécessaire pour commencer une tâche : lire
8: > [`AGENTS.md`](../AGENTS.md), puis le document de la tâche. Le reste se [charge](theorie/glossaire/entrees/charge-flux-chargeflux.md) au besoin.
9: 
10: ## En trois portes
11: 
12: | si vous voulez… | lisez |
13: |---|---|
14: | **comprendre le projet** | [la vision](theorie/vision.md) · [la mission](methode/mission.md) · [le protocole sémantique](theorie/protocole-semantique.md) · [le glossaire](theorie/glossaire.md) · [la synthèse](theorie/synthese/index.md) |
15: | **faire** (résultat, [porte](theorie/glossaire/entrees/porte.md), ran
… [8929 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de `docs/pilotage/utilisation.md` pour aligner le ton et éviter les doublons.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l docs/pilotage/utilisation.md && sed -n 1,140p docs/pilotage/utilisation.md", "description": "Read existing usage document"}`

  ```
217 docs/pilotage/utilisation.md
# UTILISER DRAVE — ce qui marche aujourd'hui, et ce qui manque

> Écrit le **16/10**, **revu le 2026-10-27**. en réponse à une question simple : « que manque-t-il pour que je puisse utiliser
> tout ça ? ». Ce document dit **ce qui s'utilise tout de suite** ✓, **la commande exacte** ✓, et
> **ce qui n'existe pas encore** ✗ — avec ce que chaque manque coûterait ✓.
> Règle de lecture : tout ce qui est ✅ a été **exécuté** le jour de l'écriture ✓ ; tout ce qui est ❌
> est un **manque constaté**, pas une supposition ✓.

## 1. ✅ Ce qui s'utilise tout de suite

### Parler au modèle — le chat

```bash
python3 tools/chat.py                       # REPL : Qwen2.5-0.5B, contexte 2048, 256 jetons/réponse
python3 tools/chat.py --modele models/Qwen2.5-0.5B-Q4_0.gguf --temp 0.9 --n 512
```

Commandes dans le REPL : `/aide`, `/reset`, `/system TEXTE`, `/temp X`, `/n X`, `/ctx X`, `/brut`,
`/quitter` ✓. **Ce que ce script corrige, et qui manquait** ✗ : `--chat` **seul ne fait rien** ✗ (le
gabarit n'est appliqué qu'avec `--prompt` ✓ — sans lui, le moteur lance un **banc de mesure** ✗✓) ; et
il n'existe **aucun mode silencieux** ✗ (la télémétrie suit la réponse ✓) → le
… [5665 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 140,217p docs/pilotage/utilisation.md", "description": "Read remainder of usage doc"}`

  ```
Le chemin image est **vérifié** ✓ (embedding exact, 31 couches à 7,58e-06 en isolation, projecteur à
0,71 % ✓) — mais ce n'est **pas encore** une vision multimodale utilisable ✗ (§ 2).

### La synthèse théorique (à lire en premier, ou en dernier)

**`docs/theorie/synthese/`** ✓ — **huit chapitres** **vulgarisés** et **quatorze schémas SVG** : l'idée fondatrice, l'anatomie
interne (régions, liens, bus, horloges), les modes d'exécution et les portes, les douze facultés et les neuf
apports de biologie, la pensée sans verbaliser (le travail du 16/10), la méthode avec ses cinq pièges, les
modèles alternatifs de l'entrée-sortie, et les opérations (la négation, la composition, la grappe).
Entrée : **`docs/theorie/synthese/index.md`** ✓.

⚠️ **Où les schémas s'affichent** ✓ : sur **docwatch** (route `/asset` et réécriture des `src`) ; si une image
reste cassée, c'est un **cache** ✗ : rechargez avec `Ctrl+Maj+R` ✓ — ou ouvrez directement le fichier
`docs/theorie/synthese/schemas/vue-ensemble.svg` ✓ (les SVG sont autonomes ✓).

### Les outils de la nuit du 16/10 (langage abstrait, empreinte, pensée itérative)

Tous sont dans `tools/`, documentés dans la fiche `reports/rapport-modele-drave.md
… [5672 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de la règle de vocabulaire de la revue (« jeton »).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 270,360p tools/revue_documentation.py", "description": "Read vocabulary and remaining review checks"}`

  ```
if c.name not in txt:
                    alertes.append(f"glossaire : {c.name} n'est pas listé dans glossaire/README.md")

    # 7c. documents datés : une date de vérification, et pas trop vieille
    for f in docs_vivants():
        try:
            tete = f.read_text(encoding="utf-8", errors="ignore")[:900]
        except OSError:
            continue
        if "> **Document daté." not in tete:
            continue
        m = re.search(r"Dernière vérification : (\d{4}-\d\d-\d\d)", tete)
        if not m:
            alertes.append(
                f"dates : {f.relative_to(RACINE)} est daté sans « Dernière vérification : AAAA-MM-JJ »"
            )
            continue
        try:
            age = (date.today() - date.fromisoformat(m.group(1))).days
        except ValueError:
            alertes.append(f"dates : {f.relative_to(RACINE)} a une date invalide ({m.group(1)})")
            continue
        if age > 90:
            alertes.append(
                f"dates : {f.relative_to(RACINE)} vérifié il y a {age} jours (> 90) — archiver ou revoir"
            )

    # 6. vocabulaire : « jeton » ne désigne jamais la RSN
    for f in (RACINE / "docs").rglob("*.md"):
        if f.n
… [3181 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-2679 (bash: grep -rn "cascade_pos" --include=*.md --include=*.py --include=*.sh --include=*.txt . | head -30; echo "---"; grep -rn "612" reports/rapport-cout-chunker.md 2>/dev/null | head; echo "---"; grep -rn "0,6 s\|0.6 s\|~0,6" reports/*.md | head -10) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Récupération du grep de fond sur `cascade_pos` et les performances.

- **job_output** `{"job_id": "bash-2679"}`

  ```
./tools/tests/linguistique/evaluer_gold.py:280:        "cascade_pos": c_all["pos"]["exactitude"] >= h_all["pos"]["exactitude"],
./tools/tests/linguistique/qualifier_cascade.py:104:        mesures["cascade_pos"] = _sources(bl.Cascade(h, pos), phrases)
./tools/tests/linguistique/qualifier_cascade.py:115:        pos_seul = mesures["cascade_pos"]["all"]
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md:21:  `cascade_pos` (documentée, tolérée).
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:10574:  "cascade_pos": true,
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:10592:verdict {'pos': True, 'syntagme': True, 'acte': True, 'cascade_pos': True, 'cascade_syntagme': True, 'reel_non_requis': True} ok True
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:10835:{'pos_hand': True, 'pos_synthetique': True, 'syntagme_hand': True, 'syntagme_synthetique': True, 'tete': True, 'acte': True, 'cascade_pos': True, 'cascade_syntagme': True, 'reel_non_requis': True} True refus
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:11574:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - 
… [8964 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de `qualifier_cascade.py` pour distinguer mock et tagger réel.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,150p tools/tests/linguistique/qualifier_cascade.py", "description": "Read cascade qualification script"}`

  ```
#!/usr/bin/env python3
"""qualifier_cascade.py — la cascade **complète** avec le vrai modèle (POS + syntagmes).

Le bloc neuronal est `NeuronalLLMCompose` : `NeuronalLLMPOS` + `NeuronalLLMChunks`, appelés
une fois par phrase, réunis en une annotation. La cascade garde l'heuristique pour la
pragmatique (acte 1,0 sur le gold) et applique la politique `confiance` au syntagme.

On mesure six lectures : heuristique, neuronal composite, cascade POS seule, cascade
syntagmes seule, cascade complète (confiance), cascade complète (priorité heuristique). Les
quatre dernières sont les **ablations** : la complète doit valoir les parties, sans perte.

    python3 tools/tests/linguistique/qualifier_cascade.py --endpoint http://127.0.0.1:18082 \
        --workers 1 --sortie reports/pensee-gold-cascade.json

Le serveur est sur CPU (`-ngl 0`) : les GPU de N2 restent intacts.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import subprocess
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import bloc_linguistique as
… [6016 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Récupération des chiffres de la cascade réelle (POS 0,9440) et de leur statut.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"0,9440\\|0.9440\\|0,9415\\|0.9415\" reports/*.md | head -12; echo \"=== json ===\"; ls reports/pensee-gold-cascade.json 2>/dev/null && python3 -c \"\nimport json; d=json.load(open('reports/pensee-gold-cascade.json')); prin … [160 caractères tronqués]`

  ```
reports/INDEX.md:386:| [rapport-pensee-cascade-vrai-modele.md](rapport-pensee-cascade-vrai-modele.md) | B13 — la cascade complète avec le vrai modèle : POS 0,9415 / syntagmes 0,6130 / tête 0,7574 / acte 1,0 sur 180 phrases |
reports/INDEX.md:416:| [rapport-pensee-gold-cascade.md](rapport-pensee-gold-cascade.md) | B13 — la cascade complète : POS 0,9415, syntagmes 0,7539, acte 1,0 |
reports/rapport-pensee-cascade-vrai-modele.md:1:# B13 — la cascade complète avec le vrai modèle : POS 0,9415 / syntagmes 0,6130 / tête 0,7574 / acte 1,0 sur 180 phrases
reports/rapport-pensee-cascade-vrai-modele.md:6:> (latence médiane 6,6 s). POS **0,9415**, syntagmes F1 **0,6130** (précision 0,6066, rappel
reports/rapport-pensee-cascade-vrai-modele.md:36:| **cascade complète (all)** | **0,9415** | **0,6130** | **0,7574** | **1,0** |
reports/rapport-pensee-cascade-vrai-modele.md:40:- **POS** : 0,9415 (fermé 0,9392, ouvert 0,9432) — au-dessus de l'heuristique (0,7544) et du
reports/rapport-pensee-gold-cascade.md:1:# B13 — la cascade complète : POS 0,9415, syntagmes 0,7539, acte 1,0
reports/rapport-pensee-gold-cascade.md:4:> **Verdict** : ✅ **la cascade complète est mesurée** — POS **0,9415**, syntagmes ex
… [744 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche d'un rejeu existant dans les tests du bloc.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"rejeu\\|rejou\" tools/tests/linguistique/*.py | head -20; echo \"=== test file ===\"; ls tools/tests/linguistique/ | head -30", "description": "Find replay tests for the block"}`

  ```
tools/tests/linguistique/replis_cible.py:518:        "mêmes conditions dans `analyser` et rejouer les portes.",
tools/tests/linguistique/replis_cible.py:821:                 "note": "état de la fiche A3 / début de session, non rejoué ici"},
tools/tests/linguistique/test_bloc_linguistique.py:84:    def test_rejeu(self):
=== test file ===
anaphore.py
classement_cible.py
evaluer_gold.py
gold_gele.json
gold.json
gold.py
gold_reel.json
gold_reel.py
gold_split.py
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
qualifier_quatre_modes.py
qualifier_syntagmes.py
replis_cible.py
test_bloc_linguistique.py
  ```

### 🤖 Assistant

⏵ Capture des sorties exactes pour les 5 exemples (dont l'anglais et le refus).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for t in \"Le chat dort.\" \"The day when we left was beautiful.\" \"Élodie sourit.\"; do echo \"##### $t\"; python3 tools/bloc_linguistique.py --texte \"$t\" --json | python3 -c \"\nimport json,sys\nd=json.load(sys.stdin)\nprint('la … [425 caractères tronqués]`

  ```
##### Le chat dort.
langue fr script Latn refus '' frac 0.6154
pos         DET        'Le'                                   [0:2] conf=0.92 cand=[] meta={'ouvert': False}
syntagme    GN         'Le chat'                              [0:7] conf=0.55 cand=['structure la plus proche', 'dort'] meta={'role': 'agent', 'niveau': 1, 'attachement': {'segment': 'Le chat', 'cible': 'dort'}}
phrase      type       'déclarative'                          [0:13] conf=0.85 cand=[] meta={}
pragmatique acte       'assertion'                            [0:13] conf=0.45 cand=['assertion', 'question', 'ordre'] meta={}
pos         NOUN       'chat'                                 [3:7] conf=0.3 cand=['noun'] meta={'ouvert': True}
pos         VERB       'dort'                                 [8:12] conf=0.72 cand=['verb'] meta={'ouvert': True}
syntagme    GV         'dort'                                 [8:12] conf=0.55 cand=['structure la plus proche'] meta={'role': 'predicat', 'niveau': 0, 'attachement': {'segment': 'dort', 'cible': 'chat'}}
##### The day when we left was beautiful.
langue en script Latn refus '' frac 0.4571
pos         DET        'The'                                  [0:3] conf=0.9
… [1994 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && command -v jq && echo \"jq présent\" || echo \"jq absent\"; python3 - <<'PY'\nimport sys; sys.path.insert(0,'.')\nfrom tools.bloc_linguistique import Heuristique\nh=Heuristique()\nfor t in [\"Élodie sourit.\",\"Le chat 🐱 dort.\",\"Qu … [182 caractères tronqués]`

  ```
/usr/bin/jq
jq présent
Élodie sourit. [(0, 6, 'Élodie'), (7, 13, 'sourit'), (13, 14, '.')]
Le chat 🐱 dort. [(0, 2, 'Le'), (3, 7, 'chat'), (8, 9, '🐱'), (10, 14, 'dort'), (14, 15, '.')]
Qu'il vienne ! [(0, 5, "Qu'il"), (6, 12, 'vienne'), (13, 14, '!')]
  ```

### 🤖 Assistant

⏵ Calcul de l'impact des deux fichiers sur les compteurs de la revue.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 100,120p tools/revue_documentation.py; python3 -c \"\nimport sys; sys.path.insert(0,'tools')\nimport revue_documentation as r\nprint('docs vivants', len(r.docs_vivants()))\nprint('compte_docs', r.compte_docs())\nprint('fiches' … [156 caractères tronqués]`

  ```
def compte_portes() -> int:
    return len(list((RACINE / "tools").glob("porte-*.sh")))


def compte_chapitres() -> int:
    return len(list((RACINE / "docs/theorie/synthese").glob("0*.md")))


def compte_fiches() -> int:
    return len(rapports())


def compte_json() -> int:
    return len(list((RACINE / "reports").glob("*.json")))


def compte_docs() -> int:
    return len(docs_vivants())


def extrait_entier(texte: str, motif: str):
docs vivants 120
compte_docs 120
fiches 676 json 769 portes 83
Python 3.13.16
  ```

### 🤖 Assistant

⏵ Test des profils UDHR sur texte court et exécution hors racine.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/bloc_linguistique.py --texte \"Élodie sourit.\" --profils data/udhr/articles.jsonl --json | python3 -c \"import json,sys; d=json.load(sys.stdin); print('langue',d['langue'],'script',d['script'],'refus',repr(d['refus'])) … [233 caractères tronqués]`

  ```
langue und script Latn refus ''
=== hors racine ===
{
 "texte": "Le chat dort.",
 "langue": "fr",
 "script": "Latn",
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/bloc_linguistique.py --texte \"Élodie sourit.\" --langue fr --json | python3 -c \"\nimport json,sys; d=json.load(sys.stdin); print('langue',d['langue'],'refus',repr(d['refus']))\nprint([(e.valeur,e.type) for e in d['eti … [371 caractères tronqués]`

  ```
langue und refus ''
=== longue phrase sans profils ===
langue fr
[stderr]
Traceback (most recent call last):
  File "<string>", line 3, in <module>
    print([(e.valeur,e.type) for e in d['etiquettes'] if e.niveau=='pos'])
                                                         ^^^^^^^^
AttributeError: 'dict' object has no attribute 'niveau'
  ```

### 🤖 Assistant

⏵ Lecture de `Heuristique.analyser` : rôle exact de `--langue`.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 980,1060p tools/bloc_linguistique.py", "description": "Read Heuristique analyser language handling"}`

  ```
i = j
                continue
            if typ == "mot" and n in lex.get("PREP", set()) and i + 1 < len(mots):
                j = i + 1
                # le GP s'arrête au verbe ou au relatif : « de la voisine | dort » et non
                # « de la voisine dort » (mesuré : 25 spans « plus large » sur le gold).
                while (j < len(mots) and mots[j][3] == "mot"
                       and not (est_verbe(mots[j][0], mots[j][2])
                                and not (j > i + 1 and _normaliser(mots[j - 1][2]) in lex.get("DET", set())))
                       and _normaliser(mots[j][2]) not in RELATIFS):
                    j += 1
                # « à manger » : un GP réduit à sa préposition prend le verbe qui suit
                if j == i + 1 and j < len(mots) and est_verbe(mots[j][0], mots[j][2]):
                    j += 1
                segments.append({"type": "GP", "role": _role_gp(t), "niveau": 1,
                                 "debut": d, "fin": mots[j - 1][1],
                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
                i = j
                continue
            i += 1
        return segments

    # -- analyse -----
… [3271 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def _langue\" -A 30 tools/bloc_linguistique.py", "description": "Read _langue decision logic"}`

  ```
540:    def _langue(self, texte: str, indice: str | None) -> tuple[str, float, str]:
541-        langue, conf, _ = detecter_langue(texte, self.profils, indice)
542-        script = detecter_script(texte)
543-        if conf < self.seuil_langue:
544-            return "und", conf, script
545-        return langue, conf, script
546-
547-    # -- tokens -------------------------------------------------------------
548-    @staticmethod
549-    def _mots(texte: str) -> list[tuple[int, int, str, str]]:
550-        motif = re.compile(r"\b[ldmtsnLDMTNS]['’](?=\w)|\w+(?:['’\-]\w+)*|\d+(?:[.,]\d+)*|https?://\S+|[\U0001F300-\U0001FAFF]|[^\w\s]")
551-        sortie = []
552-        for m in motif.finditer(texte):
553-            t = m.group()
554-            if t.startswith(("http://", "https://")):
555-                typ = "url"
556-            elif t[0].isdigit():
557-                typ = "nombre"
558-            elif re.fullmatch(r"[^\w\s]", t):
559-                typ = "ponctuation"
560-            elif len(t) == 1 and ord(t) >= 0x1F300:
561-                typ = "emoji"
562-            else:
563-                typ = "mot"
564-            sortie.append((m.start(), m.end(), t, typ))
56
… [283 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys; sys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nh=bl.Heuristique()\nprint('seuil_langue',h.seuil_langue)\nfor t in [\"Élodie sourit.\",\"Le chat dort.\",\"Élodie sourit parce que le soleil  … [193 caractères tronqués]`

  ```
seuil_langue 0.12
Élodie sourit. ('fr', 0.04) ('und', 0.0)
Le chat dort. ('fr', 0.7067) ('fr', 0.6667)
Élodie sourit parce que le soleil se lève sur la ville. ('fr', 0.9491) ('fr', 0.9091)
  ```

### 🤖 Assistant

⏵ Test d'un texte multi-phrases pour décrire la granularité de la sortie.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/bloc_linguistique.py --texte \"Le chat dort. Va voir le chat ! Il ne dort pas, mais il a peut-être faim.\" --json | python3 -c \"\nimport json,sys; d=json.load(sys.stdin)\nfor e in d['etiquettes']:\n    if e['niveau'] i … [282 caractères tronqués]`

  ```
phrase type 'déclarative' [ 0 : 13 ] {}
pragmatique acte 'assertion' [ 0 : 13 ] {}
discours paragraphe 'suite' [ 0 : 73 ] {}
phrase type 'exclamative' [ 13 : 31 ] {}
pragmatique acte 'exclamation' [ 13 : 31 ] {}
discours connecteur 'mais' [ 31 : 73 ] {}
phrase type 'déclarative' [ 31 : 73 ] {}
phrase négation 'oui' [ 31 : 73 ] {}
phrase modalité 'oui' [ 31 : 73 ] {}
pragmatique acte 'assertion' [ 31 : 73 ] {}
unites 7 frac 0.3562
  ```

### 🤖 Assistant

⏵ Génération des extraits JSON réels (filtre `jq`) pour les cinq exemples.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && FILTRE='{langue, script, refus, fraction_semantique, pos: [.etiquettes[]|select(.niveau==\"pos\")|{valeur,type,debut,fin,confiance,ouvert:.meta.ouvert}], syntagmes: [.etiquettes[]|select(.niveau==\"syntagme\")|{valeur,type,debut,fin, … [533 caractères tronqués]`

  ```
##### Le chat dort.
{
  "langue": "fr",
  "script": "Latn",
  "refus": "",
  "fraction_semantique": 0.6154,
  "pos": [
    {
      "valeur": "Le",
      "type": "DET",
      "debut": 0,
      "fin": 2,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "chat",
      "type": "NOUN",
      "debut": 3,
      "fin": 7,
      "confiance": 0.3,
      "ouvert": true
    },
    {
      "valeur": "dort",
      "type": "VERB",
      "debut": 8,
      "fin": 12,
      "confiance": 0.72,
      "ouvert": true
    }
  ],
  "syntagmes": [
    {
      "valeur": "Le chat",
      "type": "GN",
      "debut": 0,
      "fin": 7,
      "confiance": 0.55,
      "role": "agent",
      "cible": "dort",
      "candidats": [
        "structure la plus proche",
        "dort"
      ]
    },
    {
      "valeur": "dort",
      "type": "GV",
      "debut": 8,
      "fin": 12,
      "confiance": 0.55,
      "role": "predicat",
      "cible": "chat",
      "candidats": [
        "structure la plus proche"
      ]
    }
  ],
  "phrase": [
    {
      "type": "type",
      "valeur": "déclarative",
      "debut": 0,
      "fin": 13
    }
  ],
  "pragmatique": [
    {
      "type": "acte",
 
… [6386 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction des exemples 4 (refus) et 5 (span non prédit).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && FILTRE='{langue, script, refus, fraction_semantique, pos: [.etiquettes[]|select(.niveau==\"pos\")|{valeur,type,debut,fin,confiance,ouvert:.meta.ouvert}], syntagmes: [.etiquettes[]|select(.niveau==\"syntagme\")|{valeur,type,debut,fin, … [695 caractères tronqués]`

  ```
##### VIDE
{
  "langue": "und",
  "script": "Zyyy",
  "refus": "vide",
  "fraction_semantique": 0.0,
  "pos": [],
  "syntagmes": [],
  "phrase": [],
  "pragmatique": [],
  "unites_semantiques": []
}
##### r035
{
  "langue": "en",
  "script": "Latn",
  "refus": "",
  "fraction_semantique": 0.375,
  "syntagmes": [
    {
      "valeur": "The film she",
      "type": "GN",
      "debut": 0,
      "fin": 12,
      "confiance": 0.35,
      "role": "groupe nominal",
      "cible": "talks",
      "union": null,
      "candidats": [
        "GN",
        "talks",
        "out"
      ]
    },
    {
      "valeur": "talks",
      "type": "GV",
      "debut": 13,
      "fin": 18,
      "confiance": 0.35,
      "role": "prédicat",
      "cible": null,
      "union": null,
      "candidats": [
        "GV"
      ]
    },
    {
      "valeur": "about is out",
      "type": "GV",
      "debut": 19,
      "fin": 31,
      "confiance": 0.35,
      "role": "prédicat",
      "cible": null,
      "union": null,
      "candidats": [
        "GV"
      ]
    }
  ],
  "phrase": [
    {
      "type": "type",
      "valeur": "déclarative"
    }
  ],
  "pragmatique": [
    {
      "type": "acte",
      "vale
… [559 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && FILTRE='{langue, script, refus, fraction_semantique, pos: [.etiquettes[]|select(.niveau==\"pos\")|{valeur,type,debut,fin,confiance,ouvert:.meta.ouvert}], syntagmes: [.etiquettes[]|select(.niveau==\"syntagme\")|{valeur,type,debut,fin, … [463 caractères tronqués]`

  ```
{
  "langue": "fr",
  "script": "Latn",
  "refus": "",
  "fraction_semantique": 0.4909,
  "syntagmes": [
    {
      "valeur": "Le chat",
      "type": "GN",
      "debut": 0,
      "fin": 7,
      "confiance": 0.4,
      "role": "agent",
      "cible": "réveille",
      "union": null,
      "candidats": [
        "« qui dort sur le toit » → voisine",
        "« qui dort sur le toit » → Le chat",
        "réveille",
        "voisine",
        "chat"
      ]
    },
    {
      "valeur": "de la voisine",
      "type": "GP",
      "debut": 8,
      "fin": 21,
      "confiance": 0.4,
      "role": "possession",
      "cible": "réveille",
      "union": null,
      "candidats": [
        "« qui dort sur le toit » → voisine",
        "« qui dort sur le toit » → Le chat",
        "réveille",
        "voisine",
        "chat"
      ]
    },
    {
      "valeur": "qui dort sur le toit",
      "type": "REL",
      "debut": 22,
      "fin": 42,
      "confiance": 0.4,
      "role": "qualite",
      "cible": "voisine",
      "union": null,
      "candidats": [
        "« qui dort sur le toit » → voisine",
        "« qui dort sur le toit » → Le chat",
        "réveille",
        "voisine",
    
… [833 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Production du résumé d'évaluation réel depuis le JSON du banc.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/doc_produit/gold.json >/dev/null 2>&1; echo \"exit=$?\"; jq '{phrases: .gold.phrases, cibles: .heuristique.all.attachement.cibles, exact: .heuristique.all.attachement.exact … [733 caractères tronqués]`

  ```
exit=1
{
  "phrases": 612,
  "cibles": 239,
  "exact": 222,
  "couverture": 0.9289,
  "topk": 221,
  "topk_taux": 0.9247,
  "pos": 0.7581,
  "pos_ferme": 0.9004,
  "pos_ouvert": 0.6234,
  "f1": 0.5849,
  "tete": 0.7336,
  "acte": 0.9967,
  "negation": 0.9771,
  "modalite": 0.9886,
  "double_sens": 0.9444,
  "cascade_pos": 0.7465,
  "hasard": 0.0042,
  "ok": false
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && jq '.verdict, (.verdict | to_entries | map(select(.value==false)))' /tmp/doc_produit/gold.json", "description": "Confirm failing verdicts"}`

  ```
{
  "pos_hand": true,
  "pos_reel": true,
  "pos_synthetique": true,
  "syntagme_hand": true,
  "syntagme_reel": true,
  "syntagme_synthetique": true,
  "tete": true,
  "acte": true,
  "cascade_pos": false,
  "cascade_syntagme": true,
  "attachement_topk": true,
  "attachement_hasard": true,
  "attachement_tete_couverture": true,
  "attachement_tete_topk": true,
  "attachement_tete_hasard": true,
  "reel_non_requis": true
}
[
  {
    "key": "cascade_pos",
    "value": false
  }
]
  ```

### 🤖 Assistant

⏵ Vérification des valeurs sur le gold gelé 602 (base du F1 publié).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys; sys.path.insert(0,'.')\nfrom tools.bloc_linguistique import Heuristique\nfrom tools.tests.linguistique.evaluer_gold import charger_gele, evaluer_bloc\nr=evaluer_bloc('h', Heuristique(), charger_gele())\n … [399 caractères tronqués]`

  ```
phrases 602 exact 222 labels 222 couv 0.9289
f1 0.5893 tete 0.7392 pos 0.7603
fr 136 en 86
  ```

### 🤖 Assistant

⏵ Vérification des quatre spans réels non attachés (g017, r255, r264, r035).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for t in \"She said that she would come yesterday.\" \"La voiture que j'ai achetée roule.\" \"Je sais qu'il vient demain.\"; do echo \"##### $t\"; python3 tools/bloc_linguistique.py --texte \"$t\" --json | jq '[.etiquettes[]|select(. … [169 caractères tronqués]`

  ```
##### She said that she would come yesterday.
[
  {
    "valeur": "said",
    "type": "GV",
    "debut": 4,
    "fin": 8,
    "role": "prédicat",
    "cible": null,
    "candidats": [
      "GV"
    ]
  },
  {
    "valeur": "that she would come yesterday",
    "type": "SUB",
    "debut": 9,
    "fin": 38,
    "role": "complément",
    "cible": "said",
    "candidats": [
      "SUB",
      "said",
      "said"
    ]
  }
]
##### La voiture que j'ai achetée roule.
[
  {
    "valeur": "La voiture",
    "type": "GN",
    "debut": 0,
    "fin": 10,
    "role": "agent",
    "cible": null,
    "candidats": [
      "« que j'ai achetée roule » → La voiture",
      "voiture"
    ]
  },
  {
    "valeur": "que j'ai achetée roule",
    "type": "REL",
    "debut": 11,
    "fin": 33,
    "role": "qualite",
    "cible": "voiture",
    "candidats": [
      "« que j'ai achetée roule » → La voiture",
      "voiture"
    ]
  }
]
##### Je sais qu'il vient demain.
[
  {
    "valeur": "Je sais",
    "type": "GV",
    "debut": 0,
    "fin": 7,
    "role": "predicat",
    "cible": null,
    "candidats": [
      "« demain » → Je sais",
      "sais"
    ]
  },
  {
    "valeur": "sais qu'il vient demain",
    
… [522 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test de l'API Python documentable (import et sortie).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom tools.bloc_linguistique import Heuristique\na = Heuristique().analyser(\"Le chat dort.\", \"fr\")\nprint(a.langue, a.script, len(a.etiquettes), round(a.fraction_semantique, 4))\nfor e in a.etiquettes:\n    if e … [180 caractères tronqués]`

  ```
fr Latn 19 0.6154
GN 'Le chat' 0 7 {'segment': 'Le chat', 'cible': 'dort'}
GV 'dort' 8 12 {'segment': 'dort', 'cible': 'chat'}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/bloc_linguistique.py --texte \"Le chat dort.\"; echo \"=== fichier ===\"; printf 'Le chat de la voisine qui dort sur le toit se réveille.\\n' > /tmp/doc_produit/page.txt && python3 tools/bloc_linguistique.py --fichier / … [87 caractères tronqués]`

  ```
langue=fr script=Latn source=heuristique refus=-
  discours     paragraphe     'suite' [0:13] conf=0.50 src=heuristique
  document     paragraphe     'Le chat dort.' [0:13] conf=0.70 src=heuristique
  graphème     lettres        'Le' [0:2] conf=0.99 src=heuristique
  graphème     espace         ' ' [2:3] conf=0.99 src=heuristique
  graphème     lettres        'chat' [3:7] conf=0.99 src=heuristique
  graphème     espace         ' ' [7:8] conf=0.99 src=heuristique
  mot          mot            'Le' [0:2] conf=0.98 src=heuristique
  mot          mot            'chat' [3:7] conf=0.98 src=heuristique
  mot          mot            'dort' [8:12] conf=0.98 src=heuristique
  mot          ponctuation    '.' [12:13] conf=0.98 src=heuristique
  phrase       type           'déclarative' [0:13] conf=0.85 src=heuristique
  pos          DET            'Le' [0:2] conf=0.92 src=heuristique
  pos          NOUN           'chat' [3:7] conf=0.30 src=heuristique
  pos          VERB           'dort' [8:12] conf=0.72 src=heuristique
  pragmatique  acte           'assertion' [0:13] conf=0.45 src=heuristique
  syntagme     GN             'Le chat' [0:7] conf=0.55 src=heuristique
  syntagme     GV            
… [1508 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Calcul de l'empreinte réelle pour l'exemple de rejeu.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/bloc_linguistique.py --texte \"Le chat dort.\" --json | tee /tmp/doc_produit/chat.json | sha256sum; jq '.etiquettes | length' /tmp/doc_produit/chat.json; wc -c /tmp/doc_produit/chat.json", "description": "Compute replay … [27 caractères tronqués]`

  ```
7edccb3202f0ecc0ad53f5a89a4e8f4767135c5679ab5c4fcc53beb74bd68934  -
19
5561 /tmp/doc_produit/chat.json
  ```

### 🤖 Assistant

⏵ Vérification du gold de la phrase d'exemple (attachement) pour ne pas surinterpréter.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nfor f in ['gold.json','gold_reel.json','gold_synthetique.json']:\n    d=json.load(open('tools/tests/linguistique/'+f))\n    for p in d['phrases']:\n        if p['texte'].startswith('Le chat de la voisin … [213 caractères tronqués]`

  ```
gold.json g002 Le chat de la voisine dort.
   {'type': 'GN', 'texte': 'Le chat', 'role': 'agent', 'debut': 0, 'fin': 7}
   {'type': 'GP', 'texte': 'de la voisine', 'role': 'possession', 'debut': 8, 'fin': 21, 'cibles': ['chat'], 'cible': 'chat'}
   {'type': 'GV', 'texte': 'dort', 'role': 'prédicat', 'debut': 22, 'fin': 26}
  pragma {'acte': 'assertion'}
  ```

### 🤖 Assistant

⏵ Recherche d'une phrase du gold avec REL correctement attachée pour l'exemple 2.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'.')\nfrom tools.bloc_linguistique import Heuristique\nfrom tools.tests.linguistique.evaluer_gold import charger\nh=Heuristique(); phr=charger()\nn=0\nfor p in phr:\n    if p.get( … [772 caractères tronqués]`

  ```
g002 'Le chat de la voisine dort.' | GP 'de la voisine' -> chat
g003 "La femme a vu l'homme dans le parc." | GP 'dans le parc' -> vu
g004 'Il a couru pour attraper le bus.' | GP 'pour attraper le bus' -> couru
g005 "Elle a dit qu'elle viendrait hier." | SUB "qu'elle viendrait" -> dit
g006 'Le chien du voisin aboie la nuit.' | GP 'du voisin' -> chien
g007 'Les enfants jouent dans le jardin.' | GP 'dans le jardin' -> jouent
g010 'Viens ici !' | GP 'ici' -> Viens
g011 "Le livre que j'ai lu est intéressant." | REL "que j'ai lu" -> livre
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/bloc_linguistique.py --texte \"Le livre que j'ai lu est intéressant.\" --json | jq '[.etiquettes[]|select(.niveau==\"syntagme\")|{valeur,type,debut,fin,confiance,role:.meta.role,cible:.meta.attachement.cible,union:.meta … [300 caractères tronqués]`

  ```
[
  {
    "valeur": "Le livre",
    "type": "GN",
    "debut": 0,
    "fin": 8,
    "confiance": 0.55,
    "role": "agent",
    "cible": "intéressant",
    "union": null,
    "candidats": [
      "« que j'ai lu » → Le livre",
      "intéressant",
      "livre"
    ]
  },
  {
    "valeur": "que j'ai lu",
    "type": "REL",
    "debut": 9,
    "fin": 20,
    "confiance": 0.55,
    "role": "qualite",
    "cible": "livre",
    "union": null,
    "candidats": [
      "« que j'ai lu » → Le livre",
      "intéressant",
      "livre"
    ]
  },
  {
    "valeur": "que j'ai lu est intéressant",
    "type": "REL",
    "debut": 9,
    "fin": 36,
    "confiance": 0.3,
    "role": "qualité",
    "cible": "livre",
    "union": true,
    "candidats": [
      "REL",
      "livre",
      "intéressant"
    ]
  },
  {
    "valeur": "est intéressant",
    "type": "GV",
    "debut": 21,
    "fin": 36,
    "confiance": 0.55,
    "role": "predicat",
    "cible": "livre",
    "union": null,
    "candidats": [
      "« que j'ai lu » → Le livre",
      "livre"
    ]
  }
]
[
  {
    "valeur": "Le",
    "type": "DET",
    "debut": 0,
    "fin": 2
  },
  {
    "valeur": "livre",
    "type": "NOUN",
    "debut":
… [1015 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && jq '.phrases[0:3]|map({id,texte,segments,pragma})' tools/tests/linguistique/gold.json", "description": "Check first hand gold entries"}`

  ```
[
  {
    "id": "g001",
    "texte": "Le chat dort.",
    "segments": [
      {
        "type": "GN",
        "texte": "Le chat",
        "role": "agent",
        "debut": 0,
        "fin": 7
      },
      {
        "type": "GV",
        "texte": "dort",
        "role": "prédicat",
        "debut": 8,
        "fin": 12
      }
    ],
    "pragma": {
      "acte": "assertion"
    }
  },
  {
    "id": "g002",
    "texte": "Le chat de la voisine dort.",
    "segments": [
      {
        "type": "GN",
        "texte": "Le chat",
        "role": "agent",
        "debut": 0,
        "fin": 7
      },
      {
        "type": "GP",
        "texte": "de la voisine",
        "role": "possession",
        "debut": 8,
        "fin": 21,
        "cibles": [
          "chat"
        ],
        "cible": "chat"
      },
      {
        "type": "GV",
        "texte": "dort",
        "role": "prédicat",
        "debut": 22,
        "fin": 26
      }
    ],
    "pragma": {
      "acte": "assertion"
    }
  },
  {
    "id": "g003",
    "texte": "La femme a vu l'homme dans le parc.",
    "segments": [
      {
        "type": "GN",
        "texte": "La femme",
        "role": "agent",
        "debut": 
… [576 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l data/udhr/articles.jsonl 2>/dev/null | head -2; ls tools/__init__.py 2>/dev/null || echo \"pas de tools/__init__.py (namespace package)\"; ls docs/produit 2>/dev/null || echo \"docs/produit absent\"", "description": "Check UDHR … [24 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 7661342 17 oct 23:14 data/udhr/articles.jsonl
pas de tools/__init__.py (namespace package)
docs/produit absent
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git ls-files --error-unmatch data/udhr/articles.jsonl >/dev/null 2>&1 && echo \"versionné\" || echo \"non versionné\"; git check-ignore -v data/udhr/articles.jsonl 2>/dev/null || true", "description": "Check if UDHR corpus is version … [4 caractères tronqués]`

  ```
non versionné
.gitignore:5:data/	data/udhr/articles.jsonl
  ```

### 🤖 Assistant

⏵ Vérification de la reproductibilité des profils UDHR hors corpus versionné.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"articles.jsonl\" tools/*.py tools/*.sh 2>/dev/null | head -10; ls tools/ | grep -i udhr", "description": "Find UDHR profile builder"}`

  ```
tools/bloc_linguistique.py:25:    python3 tools/bloc_linguistique.py --autotest --udhr data/udhr/articles.jsonl
tools/bloc_linguistique.py:2164:    ap.add_argument("--profils", default="", help="articles.jsonl UDHR pour les profils de langue")
tools/bloc_linguistique.py:2168:    ap.add_argument("--udhr", default=str(RACINE / "data/udhr/articles.jsonl"))
tools/extraire_evals_langues.py:24:UDHR = RACINE / "data/udhr/articles.jsonl"
tools/importer_udhr.py:20:  · `articles.jsonl` : une ligne par (fichier, article) — le **texte normalisé** ✓.
tools/importer_udhr.py:99:    (sortie / "articles.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in articles))
tools/importer_udhr.py:111:    print(f"  ✓ écrit dans {sortie}/langues.jsonl et {sortie}/articles.jsonl")
tools/preparer_udhr.py:33:    arts = [json.loads(l) for l in pathlib.Path("data/udhr/articles.jsonl").read_text().splitlines()]
tools/porte-bloc-linguistique.sh:8:python3 tools/bloc_linguistique.py --autotest --udhr data/udhr/articles.jsonl --sortie /tmp/bloc-linguistique-porte.json || { echo "❌ autotest"; exit 1; }
extrait_udhr.py
genealogie_udhr.py
importer_udhr.py
preparer_udhr.py
restitution_udhr.py
retri
… [69 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,45p tools/importer_udhr.py", "description": "Confirm UDHR importer source/network"}`

  ```
#!/usr/bin/env python3
"""importer_udhr.py — LE CORPUS PARALLÈLE UDHR : 400+ langues, 30 articles alignés.

POURQUOI CE CORPUS. Pour tester une **couche commune** qui abstrait la langue, il faut **le même contenu dans
beaucoup de langues** ✓✓ : c'est la seule façon de séparer « ce qui est dit » de « la langue qui le dit » ✓. La
**Déclaration universelle des droits de l'homme** est le texte le plus traduit du monde ✓ — et le corpus Unicode
UDHR (Office of the High Commissioner for Human Rights ✓) la donne en **459 fichiers XML**, avec le **même
découpage en 30 articles** ✓✓.

CE QU'IL Y A DANS LE CORPUS, ET C'EST TOUT L'INTÉRÊT ✓ :
  · **404 langues** avec leurs métadonnées (iso639-3, nom, **écriture**, sens d'écriture ✓) ;
  · **32 langues ont PLUSIEURS variantes** ✗✓ (l'occitan en a **7** ✓, le roumain 3, le hunde 3, l'allemand 2,
    le chinois 2, le grec 2…) — ce sont des **traductions différentes de la même langue**, exactement ce qu'il
    faut pour mesurer un **style de traducteur** ✓✓ ;
  · **30 articles alignés** (le même numéro = le même sens ✓✓) — c'est notre unité parallèle ✓ ;
  · et **7 écritures** dominantes (latin 324, cyrillique 29, arabe 8, devanagari 7, et le rest
… [1100 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json tools/tests/linguistique/gold_synthetique.json tools/tests/linguistique/gold_gele.json; do git ls-files --error-unmatch \"$f\" >/dev/null 2>&1 && ech … [101 caractères tronqués]`

  ```
tools/tests/linguistique/gold.json versionné
tools/tests/linguistique/gold_reel.json versionné
tools/tests/linguistique/gold_synthetique.json versionné
tools/tests/linguistique/gold_gele.json versionné
  ```

### 🤖 Assistant

⏵ Validation des one-liners réels qui iront dans la notice.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && printf \"Le livre que j'ai lu est intéressant.\\n\" > /tmp/doc_produit/page.txt\necho \"--- ex1\"; python3 tools/bloc_linguistique.py --texte \"Le chat dort.\" --json | jq -r '\"\\(.langue) \\(.script) · \" + ([.etiquettes[]|select(. … [893 caractères tronqués]`

  ```
--- ex1
fr Latn · GN Le chat [0:7] → dort · GV dort [8:12] → chat
--- ex2
fr Latn · 42 étiquettes · GN Le livre → intéressant · REL que j'ai lu → livre · REL que j'ai lu est intéressant → livre · GV est intéressant → livre
--- ex4
identique · c1f3c76a5a40fcbd…
  ```

### 🤖 Assistant

⏵ Rédaction de `docs/produit/README.md`.

- **bash** `{"command": "mkdir -p /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit && echo ok", "description": "Create product docs directory"}`

  ```
ok
  ```

### 🤖 Assistant

⏵ Capture finale des JSON exacts pour `exemples.md`.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && FILTRE='{langue, script, refus, fraction_semantique, pos: [.etiquettes[] | select(.niveau==\"pos\") | {valeur, type, debut, fin, confiance, ouvert:.meta.ouvert}], syntagmes: [.etiquettes[] | select(.niveau==\"syntagme\") | {valeur, t … [1130 caractères tronqués]`

  ```
83 /tmp/doc_produit/ex1.json
  83 /tmp/doc_produit/ex2.json
 120 /tmp/doc_produit/ex3.json
  11 /tmp/doc_produit/ex4.json
  61 /tmp/doc_produit/ex5.json
 358 total
=== ex2 ===
{
  "langue": "fr",
  "script": "Latn",
  "refus": "",
  "fraction_semantique": 0.4865,
  "syntagmes": [
    {
      "valeur": "Le livre",
      "type": "GN",
      "debut": 0,
      "fin": 8,
      "confiance": 0.55,
      "role": "agent",
      "cible": "intéressant",
      "union": null,
      "candidats": [
        "« que j'ai lu » → Le livre",
        "intéressant",
        "livre"
      ]
    },
    {
      "valeur": "que j'ai lu",
      "type": "REL",
      "debut": 9,
      "fin": 20,
      "confiance": 0.55,
      "role": "qualite",
      "cible": "livre",
      "union": null,
      "candidats": [
        "« que j'ai lu » → Le livre",
        "intéressant",
        "livre"
      ]
    },
    {
      "valeur": "que j'ai lu est intéressant",
      "type": "REL",
      "debut": 9,
      "fin": 36,
      "confiance": 0.3,
      "role": "qualité",
      "cible": "livre",
      "union": true,
      "candidats": [
        "REL",
        "livre",
        "intéressant"
      ]
    },
    {
      "valeur": "es
… [500 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/doc_produit && echo \"=== EX1 ===\"; cat ex1.json; echo \"=== EX5 ===\"; cat ex5.json", "description": "Inspect example 1 and 5 outputs"}`

  ```
=== EX1 ===
{
  "langue": "fr",
  "script": "Latn",
  "refus": "",
  "fraction_semantique": 0.6154,
  "pos": [
    {
      "valeur": "Le",
      "type": "DET",
      "debut": 0,
      "fin": 2,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "chat",
      "type": "NOUN",
      "debut": 3,
      "fin": 7,
      "confiance": 0.3,
      "ouvert": true
    },
    {
      "valeur": "dort",
      "type": "VERB",
      "debut": 8,
      "fin": 12,
      "confiance": 0.72,
      "ouvert": true
    }
  ],
  "syntagmes": [
    {
      "valeur": "Le chat",
      "type": "GN",
      "debut": 0,
      "fin": 7,
      "confiance": 0.55,
      "role": "agent",
      "cible": "dort",
      "union": null,
      "candidats": [
        "structure la plus proche",
        "dort"
      ]
    },
    {
      "valeur": "dort",
      "type": "GV",
      "debut": 8,
      "fin": 12,
      "confiance": 0.55,
      "role": "predicat",
      "cible": "chat",
      "union": null,
      "candidats": [
        "structure la plus proche"
      ]
    }
  ],
  "phrase": [
    {
      "type": "type",
      "valeur": "déclarative"
    }
  ],
  "pragmatique": [
    {
      "type": "acte",
  
… [1191 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/doc_produit && cat ex3.json", "description": "Inspect example 3 output"}`

  ```
{
  "langue": "en",
  "script": "Latn",
  "refus": "",
  "fraction_semantique": 0.4571,
  "pos": [
    {
      "valeur": "The",
      "type": "DET",
      "debut": 0,
      "fin": 3,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "day",
      "type": "NOUN",
      "debut": 4,
      "fin": 7,
      "confiance": 0.3,
      "ouvert": true
    },
    {
      "valeur": "when",
      "type": "CONJ",
      "debut": 8,
      "fin": 12,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "we",
      "type": "PRON",
      "debut": 13,
      "fin": 15,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "left",
      "type": "NOUN",
      "debut": 16,
      "fin": 20,
      "confiance": 0.3,
      "ouvert": true
    },
    {
      "valeur": "was",
      "type": "AUX",
      "debut": 21,
      "fin": 24,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "beautiful",
      "type": "ADJ",
      "debut": 25,
      "fin": 34,
      "confiance": 0.68,
      "ouvert": true
    }
  ],
  "syntagmes": [
    {
      "valeur": "The day",
      "type": "GN",
      "debut": 0,
      "fin": 7,
      "confi
… [847 caractères tronqués]
  ```

- **bash** `{"command": "cat /tmp/doc_produit/ex4.json", "description": "Inspect refusal JSON"}`

  ```
{
  "langue": "und",
  "script": "Zyyy",
  "refus": "vide",
  "fraction_semantique": 0.0,
  "pos": [],
  "syntagmes": [],
  "phrase": [],
  "pragmatique": [],
  "unites_semantiques": []
}
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "content": "# Le premier produit — analyser un texte avec Drave\n\n> **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc\n> linguistique, utilisable **aujourd'hui**, sur un CPU … [21693 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/bloc_linguistique.py --texte \"Le livre que j'ai lu est intéressant.\" --json | jq -r '[.etiquettes[] | select(.niveau==\"pos\") | \"\\(.valeur)/\\(.type)\"] | join(\" \")'", "description": "Get exact POS one-liner outp … [4 caractères tronqués]`

  ```
Le/DET livre/NOUN que/PRON j'ai/PRON lu/NOUN est/AUX intéressant/ADJ
  ```

- **write** `{"content": "# Cinq exemples d'analyse, commentés\n\n> **Ce que ce document est.** Cinq exécutions **réelles** du bloc linguistique, avec leur JSON\n> commenté. Il complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce\n> document dit *comment lire* ce qui sort. Les sorties ont … [17511 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md": file has not been read — read the file, then retry
  ```

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/; test -f /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md && echo EXISTE || echo ABSENT", "description": "Check whether exemples.md exists"}`

  ```
total 28
drwxr-xr-x. 1 stephane stephane    40  6 nov 10:21 .
drwxr-xr-x. 1 stephane stephane   138  6 nov 10:08 ..
-rw-r--r--. 1 stephane stephane  3765  6 nov 10:21 exemples.md
-rw-------. 1 stephane stephane 21932  6 nov 10:19 README.md
EXISTE
  ```

### 🤖 Assistant

⏵ Un `exemples.md` vient d'apparaître : inspection avant toute écriture.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md</path>
<type>file</type>
<content>
1: # Exemples — entrées et sorties réelles
2: 
3: > Tous les exemples ci-dessous ont été **lancés** avec `tools/drave.py` le 2026-11-06 sur `s/v7`.
4: > Les sorties sont recopiées telles quelles (espaces compactés).
5: 
6: ## 1. Une phrase simple, en français
7: 
8: ```bash
9: python3 tools/drave.py analyser "Le chat dort."
10: ```
11: 
12: ```text
13: POS  Le/DET chat/NOUN dort/VERB
14: SYNTAGMES
15:   GN   [0:7]   Le chat  rôle=agent     → dort
16:   GV   [8:12]  dort     rôle=predicat  → chat
17: PRAGMATIQUE
18:   phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
19: ```
20: 
21: **À lire** : le GN a le rôle `agent` et sa **cible** est le verbe `dort` ; le GV a pour cible le
22: sujet `chat`. L'attachement est la relation segment → gouverneur, pas le rôle.
23: 
24: ## 2. Une relative, en français
25: 
26: ```bash
27: python3 tools/drave.py analyser "Le chat de la voisine qui dort sur le toit se réveille."
28: ```
29: 
30: ```text
31: GN   [0:7]    Le chat                           rôle=agent       → réveille
32: GP   [8:21]   
… [3014 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de l'arrivée de `tools/drave.py` et de son contrat réel.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l tools/drave.py 2>/dev/null && head -60 tools/drave.py 2>/dev/null || echo \"toujours absent\"; echo \"=== git status ===\"; git status --porcelain docs/produit tools/drave.py 2>/dev/null", "description": "Check if drave.py now  … [8 caractères tronqués]`

  ```
-rw-------. 1 stephane stephane 16540  6 nov 09:55 tools/drave.py
#!/usr/bin/env python3
"""drave.py — le point d'entrée produit du bloc linguistique.

Une seule commande, trois gestes, hors ligne et déterministe :

    python3 tools/drave.py analyser "Le chat dort."
    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
    python3 tools/drave.py evaluer
    python3 tools/drave.py evaluer --gold --json
    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
    python3 tools/drave.py --version

Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
avec rôle et cible d'attachement, pragmatique, unités sémantiques — et sa mesure sur le gold.
Ce qu'elle n'expose pas encore : le neuronal (`llama-cli` ou endpoint local), la restitution
(annotation → texte), la traduction et la génération : ils demandent des poids, un service ou
un GPU, alors que ce prototype est hors ligne, CPU et sans réseau.

Codes de sortie : 0 succès · 2 usage · 1 erreur (ou refus d'analyse).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathl
… [1195 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Le prototype CLI est livré : lecture complète pour aligner la documentation sur le réel.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """drave.py — le point d'entrée produit du bloc linguistique.
3: 
4: Une seule commande, trois gestes, hors ligne et déterministe :
5: 
6:     python3 tools/drave.py analyser "Le chat dort."
7:     python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
8:     python3 tools/drave.py evaluer
9:     python3 tools/drave.py evaluer --gold --json
10:     python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
11:     python3 tools/drave.py --version
12: 
13: Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
14: avec rôle et cible d'attachement, pragmatique, unités sémantiques — et sa mesure sur le gold.
15: Ce qu'elle n'expose pas encore : le neuronal (`llama-cli` ou endpoint local), la restitution
16: (annotation → texte), la traduction et la génération : ils demandent des poids, un service ou
17: un GPU, alors que ce prototype est hors ligne, CPU et sans réseau.
18: 
19: Codes de sortie : 0 succès · 2 usage · 1 erreur (ou refus d'analyse).
20: """
21: 
… [17183 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Exécution du CLI réel : version, analyse, évaluation, rejeu, refus.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== VERSION ===\"; python3 tools/drave.py --version; echo \"exit=$?\"; echo \"=== ANALYSER ===\"; python3 tools/drave.py analyser \"Le chat dort.\"; echo \"exit=$?\"; echo \"=== ANALYSER EN ===\"; python3 tools/drave.py analys … [121 caractères tronqués]`

  ```
=== VERSION ===
drave 0.1.0
exit=0
=== ANALYSER ===
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 19 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.92 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
exit=0
=== ANALYSER EN ===
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=en script=Latn source=heuristique · 37 étiquettes · unités sémantiques=3 (45.7% du texte)
POS  The/DET day/NOUN when/CONJ we/PRON left/NOUN was/AUX beautiful/ADJ
SYNTAGMES
  GN   [0:7]    The day        rôle=groupe nominal  → beautiful
  REL  [8:20]   when we left   rôle=qualité         → day
  GV   [21:34]  was beautiful  rôle=prédicat        → —
PRAGMATIQUE
  phrase [0:35] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0
… [141 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== EVALUER ===\"; python3 tools/drave.py evaluer; echo \"exit=$?\"; echo \"=== EVALUER GOLD ===\"; python3 tools/drave.py evaluer --gold; echo \"exit=$?\"", "description": "Run CLI evaluation on both golds"}`

  ```
=== EVALUER ===
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement

POS         exactitude 75.81 %  (fermé 90.04 %, ouvert 62.34 %)
SYNTAGMES   F1 58.49 %  (P 62.92 % / R 54.64 %)
  tête      F1 73.36 %  (P 81.00 % / R 67.04 %)
ATTACHEMENT exact 92.89 % · couverture 92.89 % · exact sur span 100.00 % · top-k 92.47 %
  tête      couverture 100.00 % · top-k 99.55 %
PRAGMATIQUE acte 99.67 % · négation 97.71 % · modalité 98.86 % · double sens 94.44 %
FRACTION SÉMANTIQUE 55.37 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 1.67 % (graine 0, 239 cibles)
exit=0
=== EVALUER GOLD ===
drave 0.1.0 — évaluation de l'heuristique sur le gold
gold gelé (référence figée) · 602 phrases · 3141 tokens · 239 cibles d'attachement

POS         exactitude 76.03 %  (fermé 90.07 %, ouvert 62.69 %)
SYNTAGMES   F1 58.93 %  (P 63.19 % / R 55.22 %)
  tête      F1 73.92 %  (P 81.36 % / R 67.72 %)
ATTACHEMENT exact 92.89 % · couverture 92.89 % · exact sur span 100.00 % · top-k 92.47 %
  tête      couverture 100.00 % · top-k 99.55 %
PRAGMATIQUE acte 99.67 % · négation 97.67 % · modalité 98.84 % · double sens 94.35 %

… [110 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test du refus, du rejeu, du JSON et de l'aide du CLI réel.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== REFUS ===\"; python3 tools/drave.py analyser \"\"; echo \"exit=$?\"; echo \"=== REJOUER ===\"; python3 tools/drave.py rejouer \"Le chat de la voisine qui dort sur le toit se réveille.\"; echo \"exit=$?\"; echo \"=== REJOUE … [119 caractères tronqués]`

  ```
=== REFUS ===
exit=1
=== REJOUER ===
rejeu identique : oui
  texte      : 'Le chat de la voisine qui dort sur le toit se réveille.'
  langue     : fr
  étiquettes : 59
  JSON       : 11700 octets · sha256 b0a1709a97abe8d4…
exit=0
=== REJOUER VIDE ===
exit=1
[stderr]
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== JSON HEAD ===\"; python3 tools/drave.py analyser \"Le chat dort.\" --json | head -25; echo \"=== JSON KEYS ===\"; python3 tools/drave.py analyser \"Le chat dort.\" --json | jq 'keys'; echo \"=== AIDE ===\"; python3 tools/d … [74 caractères tronqués]`

  ```
=== JSON HEAD ===
{
 "texte": "Le chat dort.",
 "langue": "fr",
 "script": "Latn",
 "source": "heuristique",
 "refus": "",
 "etiquettes": [
  {
   "niveau": "graphème",
   "type": "lettres",
   "valeur": "Le",
   "debut": 0,
   "fin": 2,
   "source": "heuristique",
   "confiance": 0.99,
   "candidats": [],
   "langue": "fr",
   "script": "Latn",
   "meta": {}
  },
  {
   "niveau": "mot",
   "type": "mot",
   "valeur": "Le",
   "debut": 0,
=== JSON KEYS ===
[
  "contexte",
  "cout",
  "etiquettes",
  "fraction_semantique",
  "langue",
  "refus",
  "script",
  "source",
  "texte",
  "trace",
  "unites_semantiques"
]
=== AIDE ===
usage: drave [-h] [-V] {analyser,evaluer,rejouer} ...

Point d'entrée produit du bloc linguistique (analyse heuristique).

arguments:
  {analyser,evaluer,rejouer}
    analyser            étiqueter un texte (POS, syntagmes, pragmatique)
    evaluer             mesurer l'heuristique sur le gold
    rejouer             analyser deux fois et vérifier le déterminisme

options:
  -h, --help, --aide    afficher cette aide et quitter
  -V, --version         afficher la version et quitter

Codes de sortie : 0 succès · 2 usage · 1 erreur (ou refus d'analyse).
Limites :
… [196 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== LONGUE ===\"; python3 tools/drave.py analyser \"Le chat de la voisine qui dort sur le toit se réveille.\"; echo \"=== ANGLAIS THAT ===\"; python3 tools/drave.py analyser \"The cat that sleeps on the roof is black.\" --lang … [147 caractères tronqués]`

  ```
=== LONGUE ===
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 59 étiquettes · unités sémantiques=5 (49.1% du texte)
POS  Le/DET chat/NOUN de/PREP la/DET voisine/NOUN qui/PRON dort/VERB sur/PREP le/DET toit/NOUN
     se/PRON réveille/NOUN
SYNTAGMES
  GN   [0:7]    Le chat                           rôle=agent       → réveille
  GP   [8:21]   de la voisine                     rôle=possession  → réveille
  REL  [22:42]  qui dort sur le toit              rôle=qualite     → voisine
  REL  [22:54]  qui dort sur le toit se réveille  rôle=qualité     → réveille
  GV   [43:54]  se réveille                       rôle=predicat    → voisine
PRAGMATIQUE
  phrase [0:55] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · morphème=0.32 · mot=0.98 · pos=0.92 ·
            syntagme=0.40 · phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
=== ANGLAIS THAT ===
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=en script=Latn source=heuristique · 45 étiquettes · unités sémantiques=4 (43.9% du texte)
POS  The/DET cat/NOUN that/DET sleeps/VERB on/PREP the/D
… [1147 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Comparaison CLI/bloc et inspection du JSON d'évaluation produit.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== hash JSON CLI vs bloc ===\"; python3 tools/drave.py analyser \"Le chat de la voisine qui dort sur le toit se réveille.\" --json | sha256sum; python3 tools/bloc_linguistique.py --texte \"Le chat de la voisine qui dort sur l … [319 caractères tronqués]`

  ```
=== hash JSON CLI vs bloc ===
b99dd497e034cc9bd3cd5b41f77930c70a6f81ae74a355cdd2e594b69720f52e  -
b99dd497e034cc9bd3cd5b41f77930c70a6f81ae74a355cdd2e594b69720f52e  -
=== rejouer court ===
rejeu identique : oui
  texte      : 'Le chat dort.'
  langue     : fr
  étiquettes : 19
  JSON       : 4013 octets · sha256 6b6def477a493444…
=== evaluer json keys ===
[
  "controle_negatif",
  "gold",
  "heuristique",
  "version"
]
{
  "nom": "vivant (hand + reel + synthétique)",
  "gele": false,
  "phrases": 612,
  "tokens": 3179,
  "cibles_attachement": 239
}
[
  "attachement",
  "attachement_tete",
  "bloc",
  "fraction_semantique",
  "phrases",
  "pos",
  "pragmatique",
  "syntagme"
]
{
  "nom": "cible exacte tirée au hasard dans le gold",
  "graine": 0,
  "cibles": 239,
  "exact_taux": 0.0167
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== analyser help ===\"; python3 tools/drave.py analyser --help; echo \"=== evaluer help ===\"; python3 tools/drave.py evaluer --help; echo \"=== rejouer help ===\"; python3 tools/drave.py rejouer --help", "description": "Read … [19 caractères tronqués]`

  ```
=== analyser help ===
usage: drave analyser [-h] [--langue {fr,en}] [--json] TEXTE

Analyse un texte avec l'heuristique et rend la lecture compacte ou le JSON.

arguments:
  TEXTE               texte à analyser (entre guillemets)

options:
  -h, --help, --aide  afficher cette aide et quitter
  --langue {fr,en}    indice de langue (fr/en) ; sans lui, le bloc détecte
  --json              sortie JSON complète (annotation, sans durée)

Exemple : python3 tools/drave.py analyser "Le chat dort." --json
=== evaluer help ===
usage: drave evaluer [-h] [--gold] [--json]

Mesure POS, syntagmes (F1/tête) et attachement (exact/couverture) sur le gold, avec un contrôle négatif reproductible.

options:
  -h, --help, --aide  afficher cette aide et quitter
  --gold              mesurer le gold gelé (référence figée) au lieu du gold vivant
  --json              sortie JSON des mesures complètes

Exemple : python3 tools/drave.py evaluer --gold --json
=== rejouer help ===
usage: drave rejouer [-h] [--langue {fr,en}] TEXTE

Analyse le texte deux fois, compare le JSON canonique et rend une empreinte sha256. Sortie 1 si les deux analyses divergent.

arguments:
  TEXTE               texte à rejouer (entre
… [208 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du double message de refus dans `rejouer`.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py rejouer \"\" 2>/tmp/doc_produit/rejouer.err; echo \"exit=$?\"; echo \"--- stderr ---\"; cat -n /tmp/doc_produit/rejouer.err", "description": "Count refusal messages from rejouer"}`

  ```
exit=1
--- stderr ---
     1	drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
  ```

### 🤖 Assistant

⏵ Mesure des temps réels du CLI et recherche d'un smoke test/porte.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -f \"evaluer: %e s\" python3 tools/drave.py evaluer >/dev/null; /usr/bin/time -f \"analyser: %e s\" python3 tools/drave.py analyser \"Le chat dort.\" >/dev/null; /usr/bin/time -f \"rejouer: %e s\" python3 tools/drave.py … [117 caractères tronqués]`

  ```
[stderr]
evaluer: 0.55 s
analyser: 0.15 s
rejouer: 0.15 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/porte-*drave* tools/porte-*produit* tools/tests/*drave* 2>/dev/null || echo \"aucune porte/smoke test drave\"; grep -rn \"drave.py\" tools/tests/*.py tools/porte-*.sh 2>/dev/null | head -10", "description": "Find product gat … [17 caractères tronqués]`

  ```
tools/porte-produit.sh
aucune porte/smoke test drave
tools/tests/test_produit.py:1:"""test_produit.py — le smoke test de bout en bout du point d'entrée `tools/drave.py`.
tools/tests/test_produit.py:17:CLI = RACINE / "tools" / "drave.py"
tools/porte-produit.sh:11:ver=$(python3 tools/drave.py --version 2>&1)
tools/porte-produit.sh:19:  sortie=$(python3 tools/drave.py analyser "$texte" --langue "$langue" --json 2>&1)
tools/porte-produit.sh:34:a=$(python3 tools/drave.py rejouer "Le chat dort." 2>&1 | grep -o 'sha256 [0-9a-f]*' | head -1)
tools/porte-produit.sh:35:b=$(python3 tools/drave.py rejouer "Le chat dort." 2>&1 | grep -o 'sha256 [0-9a-f]*' | head -1)
tools/porte-speculatif.sh:40:$P tools/speculatif_drave.py --n "$N" --K 4 --invite "$INVITE" --json "$T/pilote.json" \
tools/porte-speculatif.sh:76:    $P tools/speculatif_drave.py --n 12 --K 4 --invite "$INVITE" --json "$T/distille.json" \
tools/porte-speculatif.sh:95:$P tools/speculatif_drave.py --n 4 --K 2 --invite "$INVITE" \
  ```

### 🤖 Assistant

⏵ Lecture et exécution de la porte produit et du smoke test livrés.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/porte-produit.sh; echo \"=== TEST ===\"; sed -n 1,80p tools/tests/test_produit.py", "description": "Read product gate and smoke test"}`

  ```
#!/usr/bin/env bash
# porte-produit — le premier produit : la CLI répond, le JSON est valide, le rejeu est identique.
#
# Ce qu'elle vérifie : `drave --version`, `analyser` (fr et en) rend un JSON parsable avec des
# étiquettes, `rejouer` rend le même sha256 deux fois, et le smoke test passe.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
ko=0
dit() { printf '  %s %s\n' "$1" "$2"; }

ver=$(python3 tools/drave.py --version 2>&1)
case "$ver" in drave*) dit ✅ "version : $ver" ;; *) dit ❌ "version : $ver"; ko=1 ;; esac

for langue in fr en; do
  case "$langue" in
    fr) texte="Le chat dort sur le toit." ;;
    en) texte="The cat sleeps on the roof." ;;
  esac
  sortie=$(python3 tools/drave.py analyser "$texte" --langue "$langue" --json 2>&1)
  if printf '%s' "$sortie" | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['langue'] == '$langue', d.get('langue')
assert len(d['etiquettes']) > 5, len(d['etiquettes'])
assert any(e['niveau'] == 'syntagme' for e in d['etiquettes'])
assert any(e['niveau'] == 'pos' for e in d['etiquettes'])
" 2>/dev/null; then
    dit ✅ "analyser $langue : JSON valide, étiquettes et syntagmes"
  else
    dit ❌ "analyser $langue : JSON invalide 
… [3903 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-produit.sh; echo \"exit=$?\"", "description": "Run product gate"}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 6b6def477a493444 deux fois
  ✅ smoke test : Ran 6 tests
[still running after 60000ms; moved to background job bash-2983]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

### 🤖 Assistant

⏵ Collecte de la porte produit (job de fond) et des sorties CLI finales.

- **job_output** `{"job_id": "bash-2983", "wait": true, "timeout_ms": 120000}`

  ```
✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
exit=0
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 80,200p tools/tests/test_produit.py", "description": "Read remainder of product smoke test"}`

  ```
and donnees["langue"] == "fr"
            and ("pos", "NOUN") in etiquettes
            and ("syntagme", "GN") in etiquettes
            and bool(donnees["unites_semantiques"])
            and "duree_s" not in donnees["cout"],
            detail(premier),
        )
        self.assertEqual(premier.stdout, second.stdout,
                         "deux appels à --json doivent rendre exactement la même sortie")

    def test_rejouer_deterministe(self) -> None:
        resultat = drave("rejouer", "Le chat de la voisine qui dort sur le toit se réveille.")
        self.assertTrue(
            resultat.returncode == 0
            and "rejeu identique : oui" in resultat.stdout
            and "sha256" in resultat.stdout,
            detail(resultat),
        )

    def test_codes_usage(self) -> None:
        sans_commande = drave()
        langue_inconnue = drave("analyser", "Le chat dort.", "--langue", "de")
        self.assertEqual(
            (2, 2),
            (sans_commande.returncode, langue_inconnue.returncode),
            detail(sans_commande) + detail(langue_inconnue),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py analyser \"Élodie sourit.\"; echo \"exit=$?\"; echo \"=== langue de ===\"; python3 tools/drave.py analyser \"Le chat dort.\" --langue de >/dev/null 2>/tmp/doc_produit/de.err; echo \"exit=$?\"; cat /tmp/doc_prod … [73 caractères tronqués]`

  ```
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=und script=Latn source=heuristique · 13 étiquettes · unités sémantiques=2 (85.7% du texte)
POS  Élodie/NOUN sourit/NOUN
SYNTAGMES —
PRAGMATIQUE
  phrase [0:14] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.55 · phrase=0.85 ·
            discours=0.50 · pragmatique=0.45 · document=0.70
exit=0
=== langue de ===
exit=2
usage: drave analyser [-h] [--langue {fr,en}] [--json] TEXTE
drave analyser: erreur d'usage : argument --langue: invalid choice: 'de' (choose from 'fr', 'en')
  ```

### 🤖 Assistant

⏵ Génération des JSON CLI définitifs pour les cinq exemples.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && \\\npython3 tools/drave.py analyser \"Le chat dort.\" --json | jq '{langue, script, refus, pos: [.etiquettes[]|select(.niveau==\"pos\")|{valeur,type,debut,fin,confiance,ouvert:.meta.ouvert}], syntagmes: [.etiquettes[]|select(.niveau= … [1749 caractères tronqués]`

  ```
72 /tmp/doc_produit/cli1.json
  82 /tmp/doc_produit/cli2.json
 107 /tmp/doc_produit/cli3.json
  60 /tmp/doc_produit/cli5.json
 321 total
{
  "langue": "fr",
  "script": "Latn",
  "refus": "",
  "pos": [
    {
      "valeur": "Le",
      "type": "DET",
      "debut": 0,
      "fin": 2,
      "confiance": 0.92,
      "ouvert": false
    },
    {
      "valeur": "chat",
      "type": "NOUN",
      "debut": 3,
      "fin": 7,
      "confiance": 0.3,
      "ouvert": true
    },
    {
      "valeur": "dort",
      "type": "VERB",
      "debut": 8,
      "fin": 12,
      "confiance": 0.72,
      "ouvert": true
    }
  ],
  "syntagmes": [
    {
      "valeur": "Le chat",
      "type": "GN",
      "debut": 0,
      "fin": 7,
      "confiance": 0.55,
      "role": "agent",
      "cible": "dort",
      "union": null,
      "candidats": [
        "structure la plus proche",
        "dort"
      ]
    },
    {
      "valeur": "dort",
      "type": "GV",
      "debut": 8,
      "fin": 12,
      "confiance": 0.55,
      "role": "predicat",
      "cible": "chat",
      "union": null,
      "candidats": [
        "structure la plus proche"
      ]
    }
  ],
  "phrase": [
    {
      "type": "type"
… [129 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Réécriture de la notice sur le CLI réellement livré (0.1.0, porte verte).

- **write** `{"content": "# Le premier produit — analyser un texte avec Drave\n\n> **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc\n> linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui\n> il s'adresse, ce qu'il fait, comment l'ex … [21745 caractères tronqués]`

  ```
Error: cannot write "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md": file changed since it was read — re-read the file, then retry
  ```

### 🤖 Assistant

⏵ `README.md` a changé sous mes pieds : relecture de la version concurrente.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l --time-style=full-iso docs/produit/; echo \"=== head ===\"; sed -n 1,40p docs/produit/README.md; echo \"=== sections ===\"; grep -n \"^#\\|^##\" docs/produit/README.md", "description": "Inspect concurrent README version"}`

  ```
total 28
-rw-r--r--. 1 stephane stephane  3765 2026-11-06 10:21:26.143348304 -0500 exemples.md
-rw-------. 1 stephane stephane 21932 2026-11-06 10:19:52.747486811 -0500 README.md
=== head ===
# Le premier produit — analyser un texte avec Drave

> **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
> linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
> il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
> qu'il garantit.
>
> **Vérifié le 2026-11-06** sur la branche `s/v7`. Le CLI unifié **`tools/drave.py`** est
> **livré** : `analyser`, `evaluer`, `rejouer`, `--version` ; la **porte produit**
> (`bash tools/porte-produit.sh`) le vérifie en **6 contrôles** et **1 min 56** ; le smoke test
> `tools/tests/test_produit.py` passe **6 tests en 1,2 s**. Les exemples du § 3 sont réels : ils
> ont été lancés pour ce document.
>
> **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,
> classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses
> candidats, de façon **déterministe**, et il sait **se mesure
… [1997 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 60,160p docs/produit/README.md; echo \"=== §7 ===\"; sed -n 256,300p docs/produit/README.md", "description": "Check current README body consistency"}`

  ```
banc vivant a **612** phrases (10 ajoutées après le gel, sans cible). Les deux bases donnent le
même attachement (222/222, couverture 0,9289) mais pas le même F1 : **0,5893** sur le gelé,
**0,5849** sur le vivant. Toujours lire la base avec le chiffre — c'est la leçon de l'audit v10.

## 3. Comment l'utiliser — cinq exemples réels

Tout se lance **depuis la racine du dépôt**. Les commandes ci-dessous sont celles d'aujourd'hui ;
elles n'utilisent ni modèle, ni GPU, ni réseau. Les JSON complets et commentés sont dans
[`exemples.md`](exemples.md).

### 3.1 Analyser une phrase

```bash
python3 tools/bloc_linguistique.py --texte "Le chat dort." --json \
  | jq -r '"\(.langue) \(.script) · " + ([.etiquettes[] | select(.niveau=="syntagme")
           | "\(.type) \(.valeur) [\(.debut):\(.fin)] → \(.meta.attachement.cible // "—")"]
           | join(" · "))'
```
```
fr Latn · GN Le chat [0:7] → dort · GV dort [8:12] → chat
```

**Lecture.** La phrase est reconnue comme française, deux syntagmes sont posés, chacun avec sa
cible : le GN « Le chat » est rattaché à « dort », le GV « dort » à « chat ». `jq` ne sert qu'à
l'affichage ; le produit n'en dépend pas. Le JSON complet contient aussi les
… [5198 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Alerte au parent : collision d'écriture et CLI livré pendant la rédaction.

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Point de situation (doc produit) — un autre agent écrit dans les mêmes fichiers pendant ma rédaction.\n\n1) Le CLI est arrivé : `tools/drave.py` (0.1.0, `analyser`/`evaluer`/`rejouer`/`--version`), plus `tools/porte-produit.sh` et `too … [1387 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

### 🤖 Assistant

⏵ Relecture complète de la notice concurrente avant remplacement.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
1: # Le premier produit — analyser un texte avec Drave
2: 
3: > **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
4: > linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
5: > il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
6: > qu'il garantit.
7: >
8: > **Vérifié le 2026-11-06** sur la branche `s/v7`. Le CLI unifié **`tools/drave.py`** est
9: > **livré** : `analyser`, `evaluer`, `rejouer`, `--version` ; la **porte produit**
10: > (`bash tools/porte-produit.sh`) le vérifie en **6 contrôles** et **1 min 56** ; le smoke test
11: > `tools/tests/test_produit.py` passe **6 tests en 1,2 s**. Les exemples du § 3 sont réels : ils
12: > ont été lancés pour ce document.
13: >
14: > **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,
15: > classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses
16: > candidats, de façon **déterministe**, et il sait **se mesurer** sur un gold de 612 ph
… [22029 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Remplacement de la notice par la version réconciliée avec le CLI réel.

- **write** `{"content": "# Le premier produit — analyser un texte avec Drave\n\n> **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc\n> linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui\n> il s'adresse, ce qu'il fait, comment l'ex … [21745 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
Updated file
</content>
  ```

### 👤 Utilisateur

Agent e181ce02-cd50-488a-a6be-e84b79d40dcc sent a message: 
Garde **ta** version de `docs/produit/README.md` et `exemples.md` : tu as raison sur les faits (le CLI livré n'a ni `--fichier` ni `--sortie` ni code 3 ; l'exemple « le chemin nage avec le renard » que j'ai écrit était faux — je l'ai inventé au lieu de le lancer). Je ne touche plus `docs/produit/` jusqu'à ta livraison.

Termine : (1) réécris les deux fichiers pour coller au CLI réel (`analyser`/`evaluer`/`rejouer`/`--version`, texte en argument, codes 0/1/2) ; (2) n'utilise que des sorties **que tu as lançées**, avec la commande exacte au-dessus ; (3) garde le § limites (restitution/traduction/neuronal absents, 17 spans, doublon REL de l'union) ; (4) vérifie que `docs/produit/exemples.md` a un lien entrant depuis `docs/produit/README.md` (sinon la revue le signale). Ne touche pas à `en-cours`, `roadmap`, `tools/`, `reports/` ; ne commit rien. Rends la liste des liens à déclarer et le diff de tes deux fichiers.

### 🤖 Assistant

⏵ Réécriture de `exemples.md` avec les sorties CLI exactes, commande au-dessus.

- **bash** `{"command": "cd /tmp/doc_produit && echo \"=== CLI2 ===\"; cat cli2.json; echo \"=== CLI3 ===\"; cat cli3.json; echo \"=== CLI5 ===\"; cat cli5.json", "description": "Read exact CLI JSON excerpts"}`

  ```
=== CLI2 ===
{
  "langue": "fr",
  "script": "Latn",
  "refus": "",
  "syntagmes": [
    {
      "valeur": "Le livre",
      "type": "GN",
      "debut": 0,
      "fin": 8,
      "confiance": 0.55,
      "role": "agent",
      "cible": "intéressant",
      "union": null,
      "candidats": [
        "« que j'ai lu » → Le livre",
        "intéressant",
        "livre"
      ]
    },
    {
      "valeur": "que j'ai lu",
      "type": "REL",
      "debut": 9,
      "fin": 20,
      "confiance": 0.55,
      "role": "qualite",
      "cible": "livre",
      "union": null,
      "candidats": [
        "« que j'ai lu » → Le livre",
        "intéressant",
        "livre"
      ]
    },
    {
      "valeur": "que j'ai lu est intéressant",
      "type": "REL",
      "debut": 9,
      "fin": 36,
      "confiance": 0.3,
      "role": "qualité",
      "cible": "livre",
      "union": true,
      "candidats": [
        "REL",
        "livre",
        "intéressant"
      ]
    },
    {
      "valeur": "est intéressant",
      "type": "GV",
      "debut": 21,
      "fin": 36,
      "confiance": 0.55,
      "role": "predicat",
      "cible": "livre",
      "union": null,
      "candidats": [
       
… [3163 caractères tronqués]
  ```

- **write** `{"content": "# Cinq exemples d'analyse, commentés\n\n> **Ce que ce document est.** Cinq exécutions **réelles** du produit, avec leur JSON commenté. Il\n> complète la notice [`README.md`](README.md) : la notice dit *quoi* faire, ce document dit\n> *comment lire* ce qui sort. Les sorties ont été produ … [20148 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/exemples.md</path>
<type>file</type>
<content>
Updated file
</content>
  ```

### 🤖 Assistant

⏵ Vérification des liens, de la revue et des compteurs après rédaction.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib, re\nR=pathlib.Path('.')\nfor f in [R/'docs/produit/README.md', R/'docs/produit/exemples.md']:\n    t=f.read_text()\n    print('==',f)\n    for c in re.findall(r'\\]\\(([^)#]+?)\\)', t):\n        if c … [201 caractères tronqués]`

  ```
== docs/produit/README.md
OK  exemples.md
OK  ../../README.md
OK  exemples.md
OK  ../implantation/bloc-linguistique.md
OK  ../../reports/rapport-pensee-v12.md
OK  ../../reports/pensee-v12.json
OK  ../../reports/rapport-audit-v10.md
OK  ../../reports/rapport-cache-chunker-applique.md
OK  ../../reports/rapport-pensee-gold-cascade.md
OK  ../pilotage/references-non-regression.md
OK  ../pilotage/utilisation.md
OK  ../theorie/pre-traitement-linguistique.md
== docs/produit/exemples.md
OK  README.md
OK  README.md
OK  ../implantation/bloc-linguistique.md
OK  ../../reports/rapport-pensee-v12.md
OK  ../../reports/rapport-audit-v10.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -40; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run documentation review"}`

  ```
revue de documentation · 679 fiche(s) · 772 JSON · 121 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
  ```

### 🤖 Assistant

⏵ Vérification de l'état courant : liens produit et compteurs mis à jour par une autre session.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"produit\\|121\\|84\\|679\\|772\" docs/pilotage/en-cours.md | head -40", "description": "Check en-cours product links and counters"}`

  ```
63:### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif ; heartbeat à rafraîchir)*
65:- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
71:- **Fait** : B13 **183/183** ; **attachement 222/222 (1,0000)** (fr 136/136, en 86/86), **couverture 0,9289** ; dev 153/153, test 69/69 ; **17 spans** inatteignables ; **`drave` v0**, porte produit et doc d'usage ; file des 29 tâches intégrée.
77:- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).
95:- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
99:- **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.
107:| portes | **84** (dont `porte-produit` le 06/11) | `tools/porte-*.sh` |
109:| fichiers / JSON de résultats | **679** / **772** | `reports/*.md` / `reports/*.json` |
110:| documents de `docs/` | **121** (hors archive et README) | `docs/**/*.md` |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"docs/produit\" docs/ README.md 2>/dev/null | head -20; echo \"=== compteurs ===\"; python3 -c \"\nimport sys; sys.path.insert(0,'tools')\nimport revue_documentation as r\nprint('docs',r.compte_docs(),'portes',r.compte_port … [120 caractères tronqués]`

  ```
docs/pilotage/roadmap.md:38:**État au 06/11 10 h 45.** B13 est à **183/183** ; **attachement 222/222 (1,0000)** (fr 136/136, en 86/86), **couverture 0,9289**, F1 0,5849 ; dev 153/153, test 69/69 ; **le premier produit est debout** : `python3 tools/drave.py analyser|evaluer|rejouer`, la **porte produit** (`porte-produit.sh`, 6 contrôles, ~2 min) et la **doc d'usage** (`docs/produit/`) ; **autotest parallèle** (×2,4) ; **84 portes** (3 rouges : `indice`, `melange`, `sessions` du hub) ; **17 spans** inatteignables ; `master` et `s/v7` poussés au même commit ;
=== compteurs ===
docs 121 portes 84 fiches 679 json 772
  ```

### 🤖 Assistant

⏵ Recherche du lien entrant réel vers `exemples.md`.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"produit/\\|exemples\\.md\" docs/*.md docs/pilotage/*.md docs/produit/*.md | head -30", "description": "Find incoming link to exemples.md"}`

  ```
docs/README.md:94:| [`produit/README.md`](produit/README.md) | le **premier produit** : analyser un texte avec Drave — à qui, quoi, comment, limites |
docs/README.md:95:| [`produit/exemples.md`](produit/exemples.md) | cinq exemples réels (entrée → sortie), dont un cas d'échec connu |
docs/pilotage/roadmap.md:38:**État au 06/11 10 h 45.** B13 est à **183/183** ; **attachement 222/222 (1,0000)** (fr 136/136, en 86/86), **couverture 0,9289**, F1 0,5849 ; dev 153/153, test 69/69 ; **le premier produit est debout** : `python3 tools/drave.py analyser|evaluer|rejouer`, la **porte produit** (`porte-produit.sh`, 6 contrôles, ~2 min) et la **doc d'usage** (`docs/produit/`) ; **autotest parallèle** (×2,4) ; **84 portes** (3 rouges : `indice`, `melange`, `sessions` du hub) ; **17 spans** inatteignables ; `master` et `s/v7` poussés au même commit ;
docs/produit/README.md:70:[`exemples.md`](exemples.md).
docs/produit/README.md:165:`stdout`**, code **1**. Le bloc, lui, rend un JSON avec `refus: "vide"` (voir `exemples.md` § 4) :
docs/produit/README.md:352:| **voir cinq JSON commentés** | [`exemples.md`](exemples.md) |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, pathlib\nsys.path.insert(0,'tools')\nimport revue_documentation as r\nR=pathlib.Path('.')\nentrants=set()\nfor f in r.sources_nav():\n    for c in r.liens(f.read_text(encoding='utf-8',errors='ignore')):\ … [580 caractères tronqués]`

  ```
exemples dans entrants ? True
source: /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/miroir.md
    1. **Valider l'entrée par la sortie** ✓✓ : ce que l'entrée a compris doit pouvoir être **reproduit** par la sortie
source: /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/resultats.md
    2. **La mesure qui le produit** — le calcul exact, la métrique ([chrF](../theorie/glossaire/entrees/chrf.md), précision, rappel, [AUC](../theorie/glossaire/entr
source: /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/illustrations.md
    Le **SVG généré n'a pas besoin d'être committé** : docwatch le produit à la demande. S'il est
source: /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/manques.md
    | **M8** | ~~**défaut du variant log-normal** — le fichier sauvé ne reproduit pas le modèle entraîné~~ **CAUSE TROUVÉE ET CORRIGÉE le 2026-10-10 22 h 50** | la 
source: /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/utilisation.md
    | 6 | **un seul cerveau, pas de « produit »** ✗ | un usage « clé en main » des facultés ✗ | les facultés sont des **outils et des portes** ✓, pas un service ✓ —
source: /home/stephane/Data13TB/stephane/GitH
… [48730 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle de la version finale de la notice et du point « doublon REL de l'union ».

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,16p docs/produit/README.md; echo \"...\"; sed -n 104,120p docs/produit/README.md; echo \"=== §4 début ===\"; sed -n 158,182p docs/produit/README.md; echo \"=== mtime ===\"; ls -l --time-style=full-iso docs/produit/", "descri … [57 caractères tronqués]`

  ```
# Le premier produit — analyser un texte avec Drave

> **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
> linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
> il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
> qu'il garantit.
>
> **Vérifié le 2026-11-06** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer` et `--version` existent, et la
> porte produit est verte. Les exemples du § 3 sont réels : ils ont été lancés pour ce document.
> Ce qui manque encore au contrat est nommé au § 7, sans être présenté comme acquis.
>
> **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,
> classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses
> candidats, de façon **déterministe**, et il sait **se mesurer** sur un gold de 612 phrases.

...
```

**Lecture.** Un appel = **une annotation** ; les phrases sont des étiquettes de niveau `phrase`,
pas des objets séparés. La REL « que j'ai lu » est bien rattachée à « livre » (cas `
… [2140 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Ajout du doublon REL de l'union dans les limites de la notice.

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "gold). Le JSON publie aussi une **seconde lecture d'union** (`meta.union: true`, span plus\nlarge) : c'est une lecture concurrente, pas un doublon. La sortie lisible du § 3.1 ne montre pas\n`union` … [284 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**2. Dix-sept spans restent inatteignables.** Sur **239 cibles**, **222** sont attachées\n(couverture **0,9289**) ; **17** ne le sont pas : **8 REL, 5 SUB, 4 GP**. Elles sont\n**inatteignables sans … [1249 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Vérification automatique : chaque commande JSON du document reproduit-elle son bloc ?

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, json, subprocess, pathlib, sys\nt = pathlib.Path('docs/produit/exemples.md').read_text()\nblocs = re.findall(r'```(\\w*)\\n(.*?)```', t, re.S)\nprint('blocs:', [(lang, len(c.splitlines())) for lang, c in  … [63 caractères tronqués]`

  ```
blocs: [('bash', 9), ('bash', 1), ('', 10), ('bash', 9), ('json', 72), ('bash', 7), ('json', 82), ('bash', 7), ('json', 107), ('bash', 1), ('', 2), ('bash', 2), ('json', 6), ('json', 7), ('bash', 7), ('json', 60)]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^## \\|when we left\\|r241\" docs/produit/exemples.md | head -20; wc -l docs/produit/exemples.md", "description": "Check whether example 3 exists"}`

  ```
12:## 0. Comment lire les JSON
42:## 1. Une déclarative simple — `g001`
172:## 2. Un attachement de REL — `g011`
295:## 3. L'anglais et le marqueur ambigu — `r241`
297:**Entrée.** `The day when we left was beautiful.` (phrase `reel` du gold, `r241`).
302:python3 tools/drave.py analyser "The day when we left was beautiful." --langue en --json \
392:      "valeur": "when we left",
425:- `when` est tagué **CONJ** par le POS, mais il déclenche une **REL** `[8:20] « when we left »`
441:## 4. Le refus — texte vide
493:## 5. L'échec connu — un span non prédit (`r035`)
605:## 6. Ce que ces exemples ne montrent pas
621:## 7. Où aller ensuite
629 docs/produit/exemples.md
  ```

### 🤖 Assistant

⏵ Exécution des commandes du document et comparaison aux blocs JSON.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, json, subprocess, pathlib\nt = pathlib.Path('docs/produit/exemples.md').read_text()\nblocs = re.findall(r'```(\\w*)\\n(.*?)```', t, re.S)\nok = True\nfor i, (lang, contenu) in enumerate(blocs):\n    if la … [955 caractères tronqués]`

  ```
✅ bloc 3 → JSON identique ( 815 octets )
✅ bloc 5 → JSON identique ( 1108 octets )
✅ bloc 7 → JSON identique ( 1249 octets )
✅ bloc 11 → JSON identique ( 69 octets )
✅ bloc 14 → JSON identique ( 675 octets )
TOUT OK
  ```

### 🤖 Assistant

⏵ Contrôle final : revue, tableaux, liens et permissions des deux fichiers.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && chmod 644 docs/produit/README.md docs/produit/exemples.md && ls -l docs/produit/ && wc -l docs/produit/README.md docs/produit/exemples.md && git status --porcelain docs/produit/", "description": "Fix permissions and count lines"}`

  ```
total 44
-rw-r--r--. 1 stephane stephane 19249  6 nov 10:45 exemples.md
-rw-r--r--. 1 stephane stephane 22442  6 nov 10:49 README.md
  370 docs/produit/README.md
  629 docs/produit/exemples.md
  999 total
 M docs/produit/README.md
 M docs/produit/exemples.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -6; echo \"revue_exit=${PIPESTATUS[0]}\"; echo \"=== tableaux ===\"; bash tools/porte-tableaux.sh 2>&1 | tail -10; echo \"tableaux_exit=${PIPESTATUS[0]}\"", "description": "Run review  … [17 caractères tronqués]`

  ```
revue de documentation · 679 fiche(s) · 773 JSON · 121 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 1 anomalie(s) :
     · compteurs : en-cours.md dit 772 JSON, le disque en a 773
revue_exit=1
=== tableaux ===
  ✅ 1723 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3499 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-06)
tableaux_exit=0
  ```

### 🤖 Assistant

⏵ Les deux fichiers sont désormais suivis : lecture du diff par rapport au commit.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -3 -- docs/produit/ && echo \"=== stat ===\" && git diff --stat -- docs/produit/ && echo \"=== noms ===\" && git diff --name-status -- docs/produit/", "description": "Inspect commit and diff stat for product docs"}`

  ```
9952a330 PRODUIT — LA DOC D'USAGE ET LES EXEMPLES ; cascade_pos DEVIENT UN PLANCHER (0,70) ET LA PORTE BLOC REPASSE VERTE ; 84 PORTES
=== stat ===
 docs/produit/README.md   | 297 +++++++++++-----------
 docs/produit/exemples.md | 631 +++++++++++++++++++++++++++++++++++++++++++----
 2 files changed, 733 insertions(+), 195 deletions(-)
=== noms ===
M	docs/produit/README.md
M	docs/produit/exemples.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --numstat -- docs/produit/; echo \"=== titres version HEAD ===\"; git show HEAD:docs/produit/README.md 2>/dev/null | grep -n \"^## \" | head -20; echo \"=== exemples HEAD ===\"; git show HEAD:docs/produit/exemples.md 2>/dev/ … [93 caractères tronqués]`

  ```
154	143	docs/produit/README.md
579	52	docs/produit/exemples.md
=== titres version HEAD ===
18:## 1. À qui s'adresse le produit
33:## 2. Ce que le produit fait
64:## 3. Comment l'utiliser — cinq exemples réels
157:## 4. Ce que le produit ne fait pas encore
209:## 5. Performance
230:## 6. Garanties
256:## 7. Le CLI en préparation — contrat et manques
342:## 8. Où aller ensuite
=== exemples HEAD ===
6:## 1. Une phrase simple, en français
24:## 2. Une relative, en français
43:## 3. Une phrase anglaise
57:## 4. Le JSON, pour un client
72:## 5. La mesure sur le gold
90:## 6. Un cas d'échec connu
  ```

### 🤖 Assistant

⏵ Le commit du hub a changé `cascade_pos` : vérification de l'état réel avant d'ajuster la notice.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"cascade_pos\" tools/tests/linguistique/evaluer_gold.py docs/pilotage/references-non-regression.md | head -20; echo \"=== commit ===\"; git show --stat 9952a330 | head -30", "description": "Check cascade_pos threshold and co … [12 caractères tronqués]`

  ```
tools/tests/linguistique/evaluer_gold.py:283:        "cascade_pos": c_all["pos"]["exactitude"] >= 0.70,
docs/pilotage/references-non-regression.md:67:| `porte-bloc-linguistique.sh` | 17 s | ✅ porte bloc linguistique verte (`cascade_pos` : plancher 0,70, la fusion rend 0,7465) |
=== commit ===
commit 9952a3303f6657c8ef9e6d387d135514f6a39fb4
Author: Stéphane <stephane@localhost>
Date:   Fri Nov 6 10:23:41 2026 -0500

    PRODUIT — LA DOC D'USAGE ET LES EXEMPLES ; cascade_pos DEVIENT UN PLANCHER (0,70) ET LA PORTE BLOC REPASSE VERTE ; 84 PORTES

 docs/README.md                                     |   7 +
 docs/pilotage/en-cours.md                          |   2 +-
 docs/produit/README.md                             | 359 +++++++++++++++++++
 docs/produit/exemples.md                           | 102 ++++++
 journal/2026-11-06/README.md                       |  13 +-
 journal/2026-11-06/distribue.md                    |   8 +-
 journal/2026-11-06/docs.md                         |   8 +-
 journal/2026-11-06/mesures.md                      |  12 +-
 journal/2026-11-06/modele.md                       |   8 +-
 journal/2026-11-06/portes.md                       |   8 +-
 journal/README.md   
… [806 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,120p reports/rapport-produit-v0.md", "description": "Read product v0 report"}`

  ```
# B13 — le premier produit : `drave` v0, une CLI qui analyse, mesure et rejoue

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Ce que c'est** : un **point d'entrée unique** — `python3 tools/drave.py` — qui expose le bloc
> linguistique en autonomie, **hors ligne**, **CPU**, **déterministe** : `analyser` (POS, syntagmes
> avec rôle et **cible d'attachement**, pragmatique), `evaluer` (la mesure sur le gold), `rejouer`
> (le déterminisme par sha256), `--version`. Une **porte** le vérifie (`porte-produit.sh` : 5
> contrôles + le smoke test + l'autotest parallèle), et un **smoke test** de 6 cas tourne en 1,2 s.
>
> **Dispositif** : [`drave.py`](../tools/drave.py), [`test_produit.py`](../tools/tests/test_produit.py),
> [`porte-produit.sh`](../tools/porte-produit.sh) ; JSON [`pensee-produit-v0.json`](pensee-produit-v0.json).

## 1. Ce que la commande fait

| commande | sortie | mesure |
|---|---|---|
| `drave.py analyser "Le chat dort sur le toit."` | POS, syntagmes (GN/GV/GP, rôle, cible), pragmatique, couverture | 32 étiquettes, 3 segments |
| `drave.py analyser … --langue en --json` | le même en JSON complet | 8 704 o (fr court 5 561 o
… [2135 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mise à jour de la notice : `cascade_pos` est un plancher (0,70), la porte est verte.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"rouge\\|cascade_pos\\|strict\" docs/produit/README.md", "description": "Locate cascade/red mentions in README"}`

  ```
190:**3. La rouge `cascade_pos`.** Elle appartient au **banc de recherche** (`evaluer_gold.py`,
193:la fusion par confiance laisse gagner le stub. C'est une **rouge tolérée**, listée dans les
345:| **`--strict`** | `evaluer` ne mesure pas la cascade et ne peut pas échouer sur une rouge tolérée ; c'est le banc de recherche qui le fait |
363:| **la rouge tolérée** et les repères des passes | [`docs/pilotage/references-non-regression.md`](../pilotage/references-non-regression.md) |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 188,206p docs/produit/README.md", "description": "Read cascade paragraph"}`

  ```
une lecture unique (garder `union: null`, ou le segment qui en contient un autre).

**3. La rouge `cascade_pos`.** Elle appartient au **banc de recherche** (`evaluer_gold.py`,
porte `porte-bloc-linguistique.sh`), pas à `drave evaluer`, qui ne mesure que l'heuristique. La
cascade (heuristique + `MockNeuronal`) donne **0,7465** en POS, sous l'heuristique **0,7581** :
la fusion par confiance laisse gagner le stub. C'est une **rouge tolérée**, listée dans les
références de non-régression. Elle améliore pourtant les syntagmes (F1 **0,6141** contre
**0,5849**, tête **0,7432** contre **0,7336**) : c'est un **échange**, pas un gain. Le produit
par défaut reste l'heuristique. La cascade avec le vrai tagger 7B a été mesurée à **0,9415** en
POS sur 180 phrases, mais elle exige un serveur local 7B, que la règle 11 interdit aujourd'hui :
ce n'est pas un chemin livré.

**4. Pas de neuronal.** `MockNeuronal` est un **contrat** déterministe, pas un tagger de qualité.
Le vrai adaptateur (`NeuronalLLM`, `NeuronalLLMPOS`) parle à un serveur local ; il n'est ni requis
ni utilisé par défaut, et le CLI ne l'expose pas.

**5. Les classes ouvertes sont fragiles.** POS fermé **0,9004**, ouvert **0,6234** :
… [200 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**3. `cascade_pos` : le plancher, pas le gain.** La « rouge » historique est devenue un\n**plancher** : le banc exige **0,70** et la cascade rend **0,7465**, donc la porte\n`porte-bloc-linguistique … [1400 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md": file changed since it was read — re-read the file, then retry
  ```

### 🤖 Assistant

⏵ Le fichier a encore changé : relecture avant la dernière correction.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l --time-style=full-iso docs/produit/README.md; grep -n \"cascade_pos\\|rouge\\|plancher\" docs/produit/README.md | head -20; echo \"=== §3.2 ===\"; sed -n 104,114p docs/produit/README.md", "description": "Inspect latest README c … [8 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 22442 2026-11-06 10:49:06.890149034 -0500 docs/produit/README.md
55:**Les contre-épreuves.** Le CLI imprime son propre plancher : **cible exacte tirée au hasard
190:**3. La rouge `cascade_pos`.** Elle appartient au **banc de recherche** (`evaluer_gold.py`,
193:la fusion par confiance laisse gagner le stub. C'est une **rouge tolérée**, listée dans les
345:| **`--strict`** | `evaluer` ne mesure pas la cascade et ne peut pas échouer sur une rouge tolérée ; c'est le banc de recherche qui le fait |
363:| **la rouge tolérée** et les repères des passes | [`docs/pilotage/references-non-regression.md`](../pilotage/references-non-regression.md) |
=== §3.2 ===
```

**Lecture.** Un appel = **une annotation** ; les phrases sont des étiquettes de niveau `phrase`,
pas des objets séparés. La REL « que j'ai lu » est bien rattachée à « livre » (cas `g011` du
gold). Le JSON publie aussi une **seconde lecture d'union** (`meta.union: true`, span plus
large) : dans la sortie lisible, elle apparaît comme un **doublon REL** ; le JSON la marque
`union: true`, à filtrer pour une lecture unique.

### 3.3 Mesurer sur le gold

```bash
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
1: # Le premier produit — analyser un texte avec Drave
2: 
3: > **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
4: > linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
5: > il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
6: > qu'il garantit.
7: >
8: > **Vérifié le 2026-11-06** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
9: > **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer` et `--version` existent, et la
10: > porte produit est verte. Les exemples du § 3 sont réels : ils ont été lancés pour ce document.
11: > Ce qui manque encore au contrat est nommé au § 7, sans être présenté comme acquis.
12: >
13: > **Le produit en une phrase.** Vous donnez un texte ; il rend une **annotation** — langue,
14: > classes de mots, syntagmes, attachements, acte de parole — avec ses spans, sa confiance et ses
15: > candidats, de façon **déterministe**, et il sait **se mesurer** sur un gold de 612 phrases.
16: 
17: ## 1. À qui s'adres
… [22598 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**3. `cascade_pos` : le plancher, pas le gain.** La « rouge » historique est devenue un\n**plancher** : le banc exige **0,70** et la cascade rend **0,7465**, donc la porte\n`porte-bloc-linguistique … [1400 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **`--strict`** | `evaluer` ne mesure pas la cascade et n'applique pas son plancher (0,70) ; c'est le banc de recherche (`evaluer_gold.py`) qui le fait |", "old_string": "| **`--strict`** | `evalu … [118 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

