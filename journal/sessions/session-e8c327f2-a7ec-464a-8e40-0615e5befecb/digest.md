# Session DSH — relecture

- identifiant : `session-e8c327f2-a7ec-464a-8e40-0615e5befecb`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-13 22:59:51
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J5.1 : le rapport de semaine — relis les fiches des jours 1 à 4, écris `reports/rapport-semaine.md` + JSON : les chiffres avant/après (POS, F1, attachement, le produit, l'intégration), les décisions, les rejets, ce qui reste. Mets à jour `docs/pilotage/semaine-autonome.md` (l'état de chaque jour).

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

- **bash** `{"command": "pwd; ls -la; echo \"---\"; ls reports/ | tail -50; echo \"---\"; ls docs/pilotage/", "description": "Explore workspace root and reports"}`

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
drwxr-xr-x. 1 stephane stephane   180 13 nov 22:59 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   952 13 nov 21:34 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 74854 13 nov 22:59 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [2372 caractères tronqués]
  ```

- **bash** `{"command": "cat docs/pilotage/semaine-autonome.md 2>/dev/null | head -200", "description": "Read semaine-autonome state file"}`

  ```
# Le chantier autonome — une semaine (7 → 14 novembre 2026)

> **Ce que ce document est.** Le **plan du chantier d'une semaine** : tous les travaux ouverts du
> dépôt et l'**intégration avec l'écosystème Panini**. Il dit **quoi**, **dans quel ordre**, **avec
> quels sous-agents**, **comment on mesure**, et **ce qui peut faire échouer**. L'état courant est
> dans [`en-cours.md`](en-cours.md) ; la théorie de la généalogie dans
> [`../theorie/genealogie-des-langues.md`](../theorie/genealogie-des-langues.md) ; la méthode
> Panini/Nipada dans [`../methode/panini-nipada.md`](../methode/panini-nipada.md).
> *À relire chaque matin du chantier.*

## 1. L'objet

**Une semaine, un système utilisable, une intégration mesurée.** Le produit `drave` (CLI, contrat,
porte) est la **priorité** ; l'intégration avec Panini/Nipada est le **second axe** ; les chantiers
N2/S/R/A sont **coordonnés** (jamais écrits par cette session). Chaque vague produit un
**résultat mesuré**, une **fiche** et son **JSON**, la mise à jour de l'**état** et un **commit
vérifié** — jamais une intention.

## 2. L'inventaire — ce qui est ouvert

### 2.1 Drave — le produit (priorité)

| reste | mesure | où |
|---|---|---|
| 1 
… [9736 caractères tronqués]
  ```

- **bash** `{"command": "ls -lat reports/*.md | head -40", "description": "List recent report markdown files"}`

  ```
-rw-------. 1 stephane stephane 31979 13 nov 22:59 reports/rapport-coordination-a.md
-rw-r--r--. 1 stephane stephane 22988 13 nov 22:36 reports/rapport-coordination-r.md
-rw-------. 1 stephane stephane 17471 13 nov 21:58 reports/rapport-coordination-s.md
-rw-r--r--. 1 stephane stephane 20149 13 nov 21:52 reports/rapport-coordination-n2.md
-rw-r--r--. 1 stephane stephane 22511 13 nov 21:30 reports/README.md
-rw-r--r--. 1 stephane stephane 27574  7 nov 18:19 reports/rapport-genealogie-deux-faces.md
-rw-r--r--. 1 stephane stephane 98343  7 nov 18:11 reports/INDEX.md
-rw-r--r--. 1 stephane stephane 20872  7 nov 17:40 reports/rapport-retrieval-epoque.md
-rw-------. 1 stephane stephane 21491  7 nov 15:16 reports/rapport-corpus-commun.md
-rw-------. 1 stephane stephane 22407  7 nov 14:53 reports/rapport-atomes-niveaux.md
-rw-------. 1 stephane stephane  9777  7 nov 14:41 reports/rapport-restitution-v0.md
-rw-------. 1 stephane stephane  6197  7 nov 14:18 reports/rapport-schema-v2.md
-rw-------. 1 stephane stephane 15180  7 nov 13:03 reports/rapport-convention-gv.md
-rw-------. 1 stephane stephane  7195  7 nov 12:34 reports/rapport-r035.md
-rw-------. 1 stephane stephane 38331  7 nov 11:05
… [2181 caractères tronqués]
  ```

- **bash** `{"command": "ls -lat reports/ | head -60", "description": "List most recent reports directory entries"}`

  ```
total 23408
drwxr-xr-x. 1 stephane stephane   74854 13 nov 22:59 .
-rw-------. 1 stephane stephane   31979 13 nov 22:59 rapport-coordination-a.md
-rw-------. 1 stephane stephane   17340 13 nov 22:59 rapport-coordination-a.json
-rw-r--r--. 1 stephane stephane   22988 13 nov 22:36 rapport-coordination-r.md
-rw-r--r--. 1 stephane stephane   13019 13 nov 22:35 rapport-coordination-r.json
-rw-r--r--. 1 stephane stephane   47402 13 nov 22:34 tagger-612.json
-rw-------. 1 stephane stephane   18503 13 nov 21:58 rapport-coordination-s.json
-rw-------. 1 stephane stephane   17471 13 nov 21:58 rapport-coordination-s.md
-rw-r--r--. 1 stephane stephane   20149 13 nov 21:52 rapport-coordination-n2.md
-rw-r--r--. 1 stephane stephane   11915 13 nov 21:52 rapport-coordination-n2.json
-rw-r--r--. 1 stephane stephane   22511 13 nov 21:30 README.md
-rw-r--r--. 1 stephane stephane  108429  7 nov 18:19 genealogie-deux-faces.json
-rw-r--r--. 1 stephane stephane   27574  7 nov 18:19 rapport-genealogie-deux-faces.md
-rw-r--r--. 1 stephane stephane   98343  7 nov 18:11 INDEX.md
-rw-r--r--. 1 stephane stephane   20872  7 nov 17:40 rapport-retrieval-epoque.md
-rw-r--r--. 1 stephane stephane 2131415  7 nov 17:
… [3381 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r035.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-convention-gv.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r035.md</path>
<type>file</type>
<content>
1: # B13 — la relative zéro (r035) : exact 236 → 237, POS inchangée
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.1 · **Date** : 2026-11-07 ·
4: > **Verdict** : ✅
5: > **`r035` est réglé** : « The film **she talks about** is out. » n'a aucun marqueur de relative.
6: > La règle **structurelle** `[GN antécédent] [pronom sujet] [verbe] [préposition orpheline] → REL`
7: > retrouve le span **[9:24]**, cible **`film`**. L'attachement exact passe de **236 à 237**,
8: > les labels de **237 à 238**, la couverture de **0,9916 à 0,9958** ; **POS inchangée**
9: > (0,8625), **F1 0,7533 → 0,7549**. **183/183 portes**.
10: >
11: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
12: > `relative_zero`), [`test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_linguistique.py)
13: > (test unitaire), [`autotest.py`](../tools/pensee/autotest.py) (183 portes, valeurs recalées) ;
14: > JSON [`pensee-r035.json`](pensee-r035.json).
15: 
16: ## 1. Le cas, reproduit
17: 
18: Gold de `r035` (`tools/tests/lingui
… [6486 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-convention-gv.md</path>
<type>file</type>
<content>
1: # B13 — la convention des GV : le sujet hors du GV, F1 0,7549 → 0,7902
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.2 · **Date** : 2026-11-07 ·
4: > **Verdict** : ✅
5: > Les **322 FP / 180 FN** du plan sont les erreurs **de GV** du gold d'avant `r035` (F1 0,7533) ;
6: > après `r035` (J1.1), la base courante est **320 FP / 179 FN** (F1 0,7549). Le classement ne
7: > change pas : **144 FP de sujet (45 %)** dominent, puis 73 d'objet, 39 de troncature. Deux règles
8: > candidates sont mesurées : **le sujet hors du GV** (F1 **+0,0332**, 0 perte d'attachement) et
9: > **l'arrêt à l'adverbe final de temps** (F1 **+0,0026**). Les deux sont **gardées** et combinées :
10: > **F1 0,7549 → 0,7902** (dev **0,7875**, test **0,7962**), **POS 0,8625 inchangée**, **attachement
11: > 237/238 inchangé** (0 cible perdue), **183/183 portes**. S/D/N2 intouchés.
12: >
13: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_sujet_hors_gv`,
14: > `ADVERBES_TEMPS`, la condition d'adverbe du GV), [`autotest.py`](../tools/pensee/a
… [14817 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v2.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v0.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-schema-v2.md</path>
<type>file</type>
<content>
1: # B13 — le schéma v2 : `meta.partition` et `meta.alternative` typés, version 2, v1 toujours lue
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.3 · **Date** : 2026-11-07 ·
4: > **Verdict** : ✅
5: > **Ce qui change pour un client** : l'annotation porte `schema: "drave.annotation"` et
6: > `version: 2`. Le schéma v2 publie les deux champs qui documentent les syntagmes qui se
7: > chevauchent : `meta.partition` (`{groupe, rang, membres, vue}`) et `meta.alternative` (la liste
8: > des autres segments du groupe, avec `relation`, `union`, `rang`, `retire`, `role`,
9: > `attachement`). Les champs sont **additifs** : un client qui ne lit pas `meta` continue de lire
10: > l'annotation. **La version 1 reste lue** : `verifier_schema_produit.py` choisit le schéma
11: > d'après `version`, et un **contrôle négatif** vérifie que le schéma v2 refuse bien une
12: > annotation v1.
13: >
14: > **Dispositif** : [`drave-annotation-v2.json`](../tools/schemas/drave-annotation-v2.json),
15: > [`drave-annotation-v1.json`](../tools/schemas/drave-annotation-v1.j
… [5497 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v0.md</path>
<type>file</type>
<content>
1: # B13 — la restitution v0 : 46/46 surfaces exactes, le miroir strict à 0,1087
2: 
3: > **Ligne de roadmap** : **B13** (produit) · **Tâche** : J1.4 · **Date** : 2026-11-07 ·
4: > **Verdict** : ✅
5: > **Ce que la commande fait** : `python3 tools/drave.py restituer TEXTE` analyse le texte,
6: > reconstruit la surface depuis le niveau **`graphème`** de l'annotation — **sans lire
7: > `Annotation.texte`** — et affiche la fidélité du **miroir** (surface, mots, POS), la fidélité
8: > de caractères et un **contrôle négatif**. `restituer --banc` rejoue le banc des 50 textes.
9: >
10: > **Le chiffre.** Sur les **50 textes libres** de l'audit A26 : **46 annotations** (4 refus),
11: > **46/46 surfaces exactes** (1,0000) ; le **miroir strict** — le minimum des fidélités
12: > surface/mots/POS — vaut **5/46 = 0,1087** ; le contrôle négatif casse **46/46**.
13: > Le miroir a trouvé un trou : `f50` perdait ses **10 sauts de ligne** (45/46, 0,9783) ;
14: > le correctif `C` les annote et la surface revient à 46/46.
15: >
16: > **Dispositif** : [`drave.py`](../tools/drave.py) 
… [9243 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-atomes-niveaux.md"}`

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

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-corpus-commun.md"}`

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

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-retrieval-epoque.md"}`

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

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-genealogie-deux-faces.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-genealogie-deux-faces.md</path>
<type>file</type>
<content>
1: # J3.2 — La généalogie à deux faces : Panini et Glottolog sur le corpus commun
2: 
3: > **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : semaine Panini, J3.2 · **Date** : 2026-11-07
4: > **Verdict** : ✅ **la confrontation est faite, et elle déplace la question.** Les deux faces ne mesurent
5: > **pas le même objet** : la « filiation » de Panini est une distance de **tradition** (3 paires seulement,
6: > sur 655, ont deux langues connues différentes), tandis que la nôtre est une distance de **famille de
7: > langues** (5 familles, 210 paires). Ce qui converge est réel mais **conditionnel** : la surface passe
8: > avant la filiation des deux côtés, et le rapport filiation/surface est du même ordre (≈ un tiers). Ce qui
9: > diverge est décisif : **la théorie couvre 5/21 langues** avec sa fonction `lang_distance` (200/210 paires
10: > codées « inconnu »), **15/21** avec ses métadonnées UDHR, **21/21** avec Glottolog ; et sur nos 21 langues,
11: > **les 154 paires hors script sont exactement au hasard** (MRR 0,1332 = H₃₀/30 ; top-1 0,0333 
… [27651 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-n2.md</path>
<type>file</type>
<content>
1: # N2 — la coordination du mètre : `--rope` ne suffit pas, il faut le canal
2: 
3: > **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-13 · **HEAD mesuré** :
4: > `ced21933` · **Verdict** : `tools/eval_n2_propre.py` lit les checkpoints RoPE comme des positions
5: > absolues et rend **8,0225** sur `propre512-8k` à 128 octets, là où le mètre RoPE rend **2,9726**
6: > à 128 et **2,7856** à 1 024. Le correctif `--rope` est **nécessaire mais non suffisant** : le
7: > checkpoint de la porte a été entraîné **avec le canal**, et `--rope` seul rend **40,0658** à 128.
8: > Le correctif validé est **`--rope --canal-dir`** ; la commande qui donne 2,79 aujourd'hui est le
9: > mètre existant `work/n2ac/eval_longueurs.py --rope`. **Aucun fichier de N2 modifié**
10: > (`native_model.py`, `entrainer_native.py`, `work/` intacts).
11: 
12: **En trois lignes.** (1) `charge()` construit `NativeModel` absolu et `ppl_protocole()` oublie le
13: canal : **deux** causes, pas une. (2) `--rope` seul rend **40,07** ; `--rope --canal-dir` rend
14: **2,9726** à 128 e
… [20830 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-s.md</path>
<type>file</type>
<content>
1: # S — les 11 verdicts de `/paragraphes` ne sont pas dans git
2: 
3: > **Ligne de roadmap** : S · **Date** : 2026-11-13 · **HEAD parent mesuré** : `ced21933`
4: > · **Sous-module `tools/structures`** : `523d8c1` · **Verdict** : les 11 verdicts a004–a009
5: > sont **11 lignes non committées** de `donnees/paragraphes-validations.jsonl` (lignes **9–19**)
6: > : **6 `resolu`, 1 `compatible`, 4 `exclu`**, soit **7 acceptés et 4 exclus**. Le working tree
7: > voit **19 verdicts / 11 acceptés / 0 candidat sans verdict** ; un clone à `523d8c1` voit
8: > **8 verdicts / 4 acceptés / 11 candidats sans verdict**. **Aucun fichier de `tools/structures/`
9: > n'est modifié par cette fiche** : l'unique modification du sous-module est celle des 11
10: > verdicts, antérieure à la fiche.
11: 
12: **En trois lignes.** (1) Les 11 verdicts sont des verdicts de **candidat**, pas de paragraphe :
13: six paragraphes (`a004`–`a009`), onze candidats, ajoutés le **2026-11-04** entre **15:03:43** et
14: **15:10:08**. (2) Le fichier est **append-only** et le diff est **+11 / −0** ; rien n
… [17498 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-r.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-r.md</path>
<type>file</type>
<content>
1: # R — le tagger POS sur le gold 612 : **+8,49 pts**, la règle dit **intégrer**
2: 
3: > **Ligne de roadmap** : **R0.7** (le bloc linguistique) · **Date** : 2026-11-13 · **HEAD mesuré** :
4: > `ced21933` · **Verdict** : le tagger POS par **API DeepSeek** mesure **0,9475** (**3012/3179**)
5: > sur le gold **612**, contre **0,8625** (**2742/3179**) pour l'heuristique du HEAD : **+8,49 pts**,
6: > IC95 bootstrap par phrase **[+7,23 ; +9,74]**, McNemar **344/74**, **p = 1,1 × 10⁻⁴²**. La règle
7: > de décision (**≥ +5 pts → intégrer**) donne : **intégrer via l'API**, jamais le 7B local
8: > (règle 11). La prémisse « clé absente » est **fausse** : la clé est dans
9: > `~/.config/drave/deepseek.key` (0600) et l'API répond **200** ; c'est `DEEPSEEK_API_KEY` qui
10: > manque. Coût mesuré : **1 218 appels, 358 962 tokens, 21 min**, **~0,04 $** hors pointe.
11: 
12: **En trois lignes.** (1) La mesure est **réelle**, faite le 2026-11-13 avec un **cache neuf** :
13: `deepseek-chat` est servi par `deepseek-flash` (DeepSeek-V4.1-Flash-1017), 1 218 appels,
14: 358 962 token
… [23367 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md</path>
<type>file</type>
<content>
1: # A — coordination : A6.2 est libre, A8.3b2 est nommée mais hors du graphe
2: 
3: > **Ligne de roadmap** : A (le moteur) · **Tâche** : J4.4 · **Date** : 2026-11-13, 22 h 45 HNE
4: > · **Branche** : `s/v7` · **HEAD** : `dc78f223`
5: >
6: > **Verdict** : **A6.2 n'est pas bloquée.** Le MoE local de 18 Go existe et tourne — la porte
7: > de l'échange d'experts est **tenue** au HEAD, et `--ppl` redonne **37,2013**. Le seul blocage
8: > est la **résidence mono-GPU 16 Go** (17,28 GiB > 16 GiB), avec une précision : le cache VRAM
9: > d'experts n'est câblé que pour **MXFP4**, pas pour le **Q4_K** du modèle local. **A8.3b2 est
10: > nommée** par A8.3b (« instrumenter `forward_lot` »), mais elle est **absente du backlog, de la
11: > roadmap et du graphe** ; elle est libre. **Aucun fichier de A modifié** (ni `drave-core/`, ni
12: > `data/`, ni `work/`) : deux fichiers neufs, celui-ci et son JSON.
13: 
14: **En trois lignes.** (1) Le MoE `qwen3-30b-a3b-Q4_K_M` (18 556 686 752 o, 17,28 GiB,
15: `sha256 6c997b8a…`) est présent, chargé en **9,82 s**, et rend **37,2013** de
… [32465 caractères tronqués]
  ```

- **bash** `{"command": "grep -rl \"rapport-semaine\\|rapport de semaine\\|rapport-semaine.json\" --include=\"*.md\" --include=\"*.json\" . 2>/dev/null | head -20", "description": "Search for existing weekly report references"}`

  ```
./tools/chantier/plan.json
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
./journal/sessions/session-a9b5216e-5f4b-4935-8ba0-2ec7d42aaf89/digest.md
./journal/sessions/session-5e097832-2ce1-407d-bf99-228cef7efa82/digest.md
./docs/pilotage/semaine-autonome.md
  ```

- **bash** `{"command": "sed -n '1,120p' reports/README.md; echo \"=== INDEX HEAD ===\"; sed -n '1,60p' reports/INDEX.md", "description": "Inspect reports README and INDEX head"}`

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
| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 niveaux |
| [`rapport-corpus-commun.md`](rapport-corpus-commun.md) | **Panini** — le corpus commun UDHR |
| [`rapport-retrieval-epoque.md`](rapport-retrieval-epoque.md) | **Panini** — le retrieval contrôlé |
| [`
… [20138 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' docs/methode/resultats.md", "description": "Read results method doc"}`

  ```
# Ce qu'un résultat doit porter

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant d'écrire une fiche**, un JSON de
> résultats, ou un message de commit.

## Les cinq pièces d'un résultat

1. **Le chiffre** — la valeur, avec son [unité](../theorie/glossaire/entrees/unite.md) et son arrondi utile (jamais plus de chiffres que l'instrument n'en
   [porte](../theorie/glossaire/entrees/porte.md)) ;
2. **La mesure qui le produit** — le calcul exact, la métrique ([chrF](../theorie/glossaire/entrees/chrf.md), précision, rappel, [AUC](../theorie/glossaire/entrees/auc.md)…), et ce qu'elle ne
   mesure pas ;
3. **Le dispositif** — quel [corpus](../theorie/glossaire/entrees/corpus.md) (et sa provenance), quel modèle (taille, [quantification](../theorie/glossaire/entrees/quantification.md), date de coupure),
   quelles **couches de neurones** sondées, quel découpage, **quelle unité de mesure** (unité de sens ou unité
   grammaticale ; si c'est un [jeton](../theorie/glossaire/entrees/jeton.md), le dire comme **technique**), quels réglages (prompt, gabarit, longueur de
   sortie, graine) ;
4. **Le [contrôle négatif](../theorie/glossaire/entrees/controle-negatif.md)
… [2500 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' docs/methode/rangement.md", "description": "Read filing method doc"}`

  ```
# Le rangement, et la revue de documentation

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). La règle la plus souvent violée du dépôt : à lire
> **avant de classer un fichier** ou de clore un sous-chantier.

## Les quatre dossiers (règle stricte)

| dossier | ce qu'il contient | ce qu'il ne contient **jamais** |
|---|---|---|
| **`docs/`** | quatre familles : **méthode**, **pilotage**, **théorie**, **implantation** — ce qui reste vrai quand les chiffres changent | des **résultats** de mesure, des tableaux de chiffres, des comptes rendus de round |
| **`reports/`** | les **résultats mesurés** : fiches, séries de mesures, tableaux, erratums, récits de round, JSON de résultats | la documentation de référence |
| **`journal/`** | le **récit daté** : ce qui a été fait, quand, et ce qu'on en a appris | les chiffres seuls (ils vont dans `reports/`) |
| **`data/`** | les corpus et leur généalogie (`data/udhr/`, `data/corpus_*.txt`, `data/eurlex/`) | du code |

Dans `docs/`, les quatre familles sont **séparées** : `methode/` (comment on travaille), `pilotage/` (où l'on en
est), `theorie/` (ce qui reste vrai), `implantation/` (comment c'est construit). Une page de `docs/`
… [4004 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"\nimport json\nfor f in ['reports/pensee-r035.json','reports/pensee-convention-gv.json','reports/pensee-schema-v2.json','reports/pensee-restitution-v0.json']:\n    d=json.load(open(f))\n    print('===',f)\n    print(type(d), list(d)[:30] if isinstance(d,dict) else len(d))\n … [50 caractères tronqués]`

  ```
=== reports/pensee-r035.json
<class 'dict'> ['date', 'ligne', 'tache', 'cas', 'phrase', 'regle', 'avant', 'apres', 'delta', 'gold', 'controles_negatifs', 'generalisation', 'portes', 'reste', 'limites']
=== reports/pensee-convention-gv.json
<class 'dict'> ['date', 'ligne', 'tache', 'objet', 'baseline_commit', 'dispositif', 'gold', 'convention_du_gold', 'avant_plan', 'avant_courant', 'regles', 'controles_negatifs', 'partition_lineaire', 'portes', 'limites']
=== reports/pensee-schema-v2.json
<class 'dict'> ['date', 'ligne', 'tache', 'objet', 'schema', 'version', 'schemas', 'champs_ajoutes', 'retrocompatibilite', 'validation', 'validation_complementaire', 'gold_alternative', 'limites']
=== reports/pensee-restitution-v0.json
<class 'dict'> ['schema', 'version', 'date', 'ligne', 'tache', 'titre', 'banc', 'banc_sha256', 'commande', 'dispositif', 'synthese', 'resultats', 'limites']
  ```

- **bash** `{"command": "python3 -c \"\nimport json\nfor f in ['reports/atomes-niveaux.json','reports/corpus-commun.json','reports/retrieval-epoque.json','reports/genealogie-deux-faces.json','reports/rapport-coordination-n2.json']:\n    d=json.load(open(f))\n    print('===',f)\n    print(type(d), list(d)[:40] i … [97 caractères tronqués]`

  ```
=== reports/atomes-niveaux.json
<class 'dict'> ['fiche', 'version', 'date', 'titre', 'statut', 'sources', 'niveaux', 'niveaux_du_contrat', 'principe', 'atomes', 'calibration_44_oeuvres', 'protocole', 'limites', 'prochaine_etape', 'fichiers']
=== reports/corpus-commun.json
<class 'dict'> ['controle_negatif', 'controles', 'date', 'fiche', 'fichiers', 'intersection', 'ligne_roadmap', 'limites', 'normalisation', 'prochaine_etape', 'selection', 'sources', 'statistiques', 'statut', 'textes', 'titre', 'version']
=== reports/retrieval-epoque.json
<class 'dict'> ['tache', 'titre', 'date', 'methode', 'b7', 'udhr', 'bible']
=== reports/genealogie-deux-faces.json
<class 'dict'> ['titre', 'version', 'date', 'ligne_roadmap', 'chantier', 'statut', 'question', 'sources', 'corpus_commun', 'theorie_panini', 'accord_genealogies', 'alignement', 'atomes', 'convergence', 'divergence', 'a_mesurer', 'limites', 'controles_negatifs', 'fichiers']
=== reports/rapport-coordination-n2.json
<class 'dict'> ['date', 'head', 'ligne', 'objet', 'fiche', 'verdict', 'aucune_modification_n2', 'bug', 'checkpoints', 'chiffres', 'correctif', 'commande_n2', 'limites', 'fichiers_lus_non_modifies', 'references']
  ```

- **bash** `{"command": "git status --short | head -40; echo \"---BRANCH---\"; git branch --show-current; echo \"---HEAD---\"; git log -1 --oneline", "description": "Check git status and HEAD"}`

  ```
M docs/pilotage/references-non-regression.md
D  journal/2026-11-13/README.md
D  journal/2026-11-13/docs.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
MM journal/sessions/session-3ffa6026-9a7d-4905-ac06-6b9708d65ba7/digest.md
MM journal/sessions/session-3ffa6026-9a7d-4905-ac06-6b9708d65ba7/rapport.md
D  journal/sessions/session-4a28c290-9701-4d27-8aad-a9cf004c9af9/digest.md
D  journal/sessions/session-4a28c290-9701-4d27-8aad-a9cf004c9af9/rapport.md
D  journal/sessions/session-5e097832-2ce1-407d-bf99-228cef7efa82/digest.md
D  journal/sessions/session-5e097832-2ce1-407d-bf99-228cef7efa82/rapport.md
D  journal/sessions/session-9f876d8f-5661-44f0-b052-0770211328ec/digest.md
D  journal/sessions/session-9f876d8f-5661-44f0-b052-0770211328ec/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans
… [656 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"fiches\\|JSON\\|49 portes\\|rapport-semaine\\|semaine\" docs/pilotage/en-cours.md | head -40", "description": "Find counters and week mentions in en-cours"}`

  ```
48:- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 tests** ; fiches [analyseur](../../reports/rapport-s-analyseur-roles.md), [arbre](../../reports/rapport-s-arbre-referents.md), [limites](../../reports/rapport-s-limites-v6.md), [fait divers](../../reports/rapport-s-fait-divers.md).
79:- **Ce qu'elle fait** : **erratum 04/11** : la distillation native ne gagne rien à parité stricte (−0,03/−0,01/−0,004 ; +0,14–0,18 = repondération) ; `kd2` et `rope2048` **arrêtés** ; **paire propre de production** : **3,1500** → **3,1119** (−0,06 ; −0,19 anglais) ; **repondération : −0,05** ; **2 048 mesuré** : ne bat pas 1 024 ; fiches [fenêtre](../../reports/rapport-n2-fenetre.md), [production](../../reports/rapport-n2-production-fenetre.md), [erratum](../../reports/rapport-n2-distillation-native.md), [porte](../../reports/rapport-n2-porte-propre.md).
102:| fichiers / JSON de résultats | **716** / **810** | `reports/*.md` / `reports/*.json` |
118:| **Backlog — graphe** | **37 fiches, 43 arêtes, 3 à la frontière** | 1 ligne sans fiche | `verifie_backlo
… [7 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' docs/pilotage/en-cours.md", "description": "Read en-cours top sections"}`

  ```
# En ce moment

**Mis à jour : 2026-11-13, 22 h 37 HNE (heure locale, EST).**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
- **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.
>
> **Règle 11** : serveurs loca
… [10376 caractères tronqués]
  ```

- **bash** `{"command": "echo \"md: $(ls reports/*.md | wc -l)\"; echo \"json: $(ls reports/*.json | wc -l)\"; echo \"---\"; ls reports/*.md | wc -l; ls reports/*.json | wc -l", "description": "Count reports md and json files"}`

  ```
md: 717
json: 811
---
717
811
  ```

- **bash** `{"command": "git show HEAD:docs/pilotage/en-cours.md | grep -n \"fichiers / JSON\" ; git ls-tree -r --name-only HEAD reports | grep -c '\\.md$'; git ls-tree -r --name-only HEAD reports | grep -c '\\.json$'", "description": "Compare committed counters and committed file counts"}`

  ```
102:| fichiers / JSON de résultats | **716** / **810** | `reports/*.md` / `reports/*.json` |
883
808
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -60", "description": "Run documentation review tool", "timeoutMs": 180000}`

  ```
revue de documentation · 717 fiche(s) · 811 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 716 fichiers, le disque en a 717
     · compteurs : en-cours.md dit 810 JSON, le disque en a 811
  ```

- **bash** `{"command": "git ls-tree --name-only HEAD reports | grep -c '\\.md$'; git ls-tree --name-only HEAD reports | grep -c '\\.json$'; echo \"--- untracked md/json:\"; git status --porcelain reports | grep '^??' | head -20", "description": "Count committed top-level report files"}`

  ```
0
0
--- untracked md/json:
?? reports/rapport-coordination-a.json
?? reports/rapport-coordination-a.md
?? reports/rapport-coordination-n2.json
?? reports/rapport-coordination-n2.md
?? reports/rapport-coordination-s.json
?? reports/rapport-coordination-s.md
?? reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "git ls-tree --name-only HEAD:reports | grep -c '\\.md$'; git ls-tree --name-only HEAD:reports | grep -c '\\.json$'; echo \"---\"; git ls-tree --name-only HEAD:reports | grep '\\.md$' | tail -5", "description": "Count committed reports directory entries"}`

  ```
713
808
---
rapport-vie-quatre-jours.md
rapport-vision-qwen2vl.md
rapport-vitesse-v41.md
rapport-vram-transfert.md
toutes-langues.md
  ```

- **bash** `{"command": "git log --since=2026-11-06 --until=2026-11-14 --pretty='%h %ad %s' --date=short | head -80", "description": "List commits during the week"}`

  ```
dc78f223 2026-11-13 ÉTAT — T0 DANS LE BUDGET (3 991 MOTS) : LA LIGNE R0.7 PORTE LE TAGGER 612 (0,9475, +8,49, INTÉGRER)
a934d779 2026-11-13 R0.7 — LE TAGGER POS SUR LE GOLD 612 : 0,9475 (3012/3179), +8,49 PTS, LA RÈGLE DIT INTÉGRER ; LA CLÉ ÉTAIT PRÉSENTE ET 0,8500 ÉTAIT DATÉ (0,8625)
ced21933 2026-11-13 CHANTIER — PHASE 2 (12 H) : LE VERDICT ACCEPTATION D'ABORD (TIMEOUT APRÈS COMMIT = FAIT), 12 TÂCHES AJOUTÉES (J4 COORDINATION, J6 SPANS, J7-J10 PANINI/BILAN), ÉTAT CORRIGÉ
c7f26b35 2026-11-13 DOCS — LA PASSE APRÈS LE CHANTIER : 8 FICHES INDEXÉES, L'ÉTAT PAR JOUR DU PLAN, LE JOURNAL DU CHANTIER, CHANTIERS À JOUR (F1 0,7902, 237/238)
c2e629b3 2026-11-07 J3.2 — DEUX FACES : 154/154 PAIRES HORS SCRIPT AU HASARD, PANINI 3/655 PAIRES INTER-LANGUES ET 5/21 LANGUES, LA FAMILLE VIT DANS 2-3 PAIRES
c3467170 2026-11-07 PANINI — J2.2 ET J3.1 : LE CORPUS COMMUN (418/438 PAIRES EXACTES, 8/8 CONTRÔLES) ET LE RETRIEVAL À ÉPOQUE CONTRÔLÉE (SCRIPT +0,609, ÉPOQUE −0,034/SIÈCLE, p=0,19)
9c7f71dc 2026-11-07 PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE
8eb0cc49 2026-11-07 B13 — RESTITUTION v0 : 46/46 SURFACES EXACTES, MIROIR STRICT 0,1087, LE MIRO
… [4384 caractères tronqués]
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M:%S %Z'; date -u '+%Y-%m-%d %H:%M:%S UTC'", "description": "Show current date and time"}`

  ```
2026-11-13 23:01:14 EST
2026-11-14 04:01:14 UTC
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-r035.json'))\nprint('r035 avant:',json.dumps(d['avant'],ensure_ascii=False)[:800])\nprint('r035 apres:',json.dumps(d['apres'],ensure_ascii=False)[:800])\nprint('r035 delta:',json.dumps(d['delta'],ensure_ascii=False)[:500]) … [51 caractères tronqués]`

  ```
r035 avant: {"all": {"phrases": 612, "pos": 0.8625, "f1": 0.7533, "precision": 0.7239, "rappel": 0.7853, "tete": 0.864, "exact": 236, "labels": 237, "cibles": 239, "couverture": 0.9916}, "dev": {"phrases": 422, "pos": 0.8618, "f1": 0.7476, "precision": 0.7223, "rappel": 0.7747, "tete": 0.8603, "exact": 160, "labels": 161, "cibles": 163, "couverture": 0.9877}, "test": {"phrases": 190, "pos": 0.8642, "f1": 0.7663, "precision": 0.7274, "rappel": 0.8095, "tete": 0.8724, "exact": 76, "labels": 76, "cibles": 76, "couverture": 1.0}}
r035 apres: {"all": {"phrases": 612, "pos": 0.8625, "f1": 0.7549, "precision": 0.7254, "rappel": 0.7869, "tete": 0.8651, "exact": 237, "labels": 238, "cibles": 239, "couverture": 0.9958}, "dev": {"phrases": 422, "pos": 0.8618, "f1": 0.7498, "precision": 0.7245, "rappel": 0.777, "tete": 0.8618, "exact": 161, "labels": 162, "cibles": 163, "couverture": 0.9939}, "test": {"phrases": 190, "pos": 0.8642, "f1": 0.7663, "precision": 0.7274, "rappel": 0.8095, "tete": 0.8724, "exact": 76, "labels": 76, "cibles": 76, "couverture": 1.0}}
r035 delta: {"exact": "236 → 237", "labels": "237 → 238", "couverture": "0,9916 → 0,9958", "pos": "0,8625 → 0,8625", "f1": "0,7533 → 0,7
… [70 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-convention-gv.json'))\nfor k in ['avant_plan','avant_courant','regles','controles_negatifs','partition_lineaire','portes','limites']:\n    v=d[k]\n    print('===',k, type(v))\n    print(json.dumps(v,ensure_ascii=False)[:12 … [64 caractères tronqués]`

  ```
=== avant_plan <class 'dict'>
{"all": {"phrases": 612, "f1": 0.7533, "precision": 0.7239, "rappel": 0.7853, "tp": 1463, "fp": 558, "fn": 400, "tete_f1": 0.864, "pos": 0.8625, "att_exact": 236, "att_labels": 237, "att_cibles": 239, "att_couverture": 0.9916}, "dev": {"phrases": 422, "f1": 0.7476, "precision": 0.7223, "rappel": 0.7747, "tp": 1004, "fp": 386, "fn": 292, "tete_f1": 0.8603, "pos": 0.8618, "att_exact": 160, "att_labels": 161, "att_cibles": 163, "att_couverture": 0.9877}, "test": {"phrases": 190, "f1": 0.7663, "precision": 0.7274, "rappel": 0.8095, "tp": 459, "fp": 172, "fn": 108, "tete_f1": 0.8724, "pos": 0.8642, "att_exact": 76, "att_labels": 76, "att_cibles": 76, "att_couverture": 1.0}, "classement": {"fp_total": 322, "fp": {"objet": 73, "sujet": 144, "adverbe": 16, "tronque": 39, "parasite": 17, "gauche_autre": 6, "deux_cotes": 27}, "fn_total": 180, "fn": {"chev_deux": 28, "avale_GN": 51, "chev_droite": 75, "chev_gauche": 7, "tronque": 19}, "doublons_total": 153, "doublons": {"objet": 4, "sujet": 133, "adverbe": 1, "tronque": 11, "deux_cotes": 1, "gauche_autre": 3}, "origine": {"chunker": 98, "S": 224}}}
=== avant_courant <class 'dict'>
{"all": {"phrases": 612, "f1": 0
… [5015 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-schema-v2.json'))\nprint(json.dumps(d.get('validation'),ensure_ascii=False)[:1500])\nprint('---complement---')\nprint(json.dumps(d.get('validation_complementaire'),ensure_ascii=False)[:1200])\nEOF", "description": "Extract … [31 caractères tronqués]`

  ```
{"commande": "python3 tools/verifier_schema_produit.py --gold 20", "cas": 26, "echecs": 0, "detail": {"base_v2": 5, "retro_v1": 1, "gold_v2": 20}, "validateur": "fastjsonschema", "repli_minimal": "champs obligatoires + version si fastjsonschema absent"}
---complement---
{"phrases_gold": 612, "vues": ["alternative", "filtrer_union", "filtrer"], "annotations": 1836, "echecs": 0}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-restitution-v0.json'))\nprint(json.dumps(d.get('synthese'),ensure_ascii=False)[:1800])\nEOF", "description": "Extract restitution v0 synthesis"}`

  ```
{"n": 50, "annotations": 46, "refus": 4, "refus_ids": ["f14", "f15", "f16", "f17"], "surface": {"exacts": 46, "fidelite": 1.0, "fidelite_caractere": 1.0}, "surface_sans_controle": {"exacts": 45, "fidelite": 0.9783, "fidelite_caractere": 0.9999}, "mots": {"exacts": 5, "fidelite": 0.1087, "fidelite_caractere": 0.9506}, "pos": {"exacts": 5, "fidelite": 0.1087, "fidelite_caractere": 0.9506}, "miroir": {"exacts": 5, "fidelite": 0.1087}, "controle_negatif": {"melange_exacts": 0, "melange_fidelite": 0.0, "melange_fidelite_caractere": 0.263, "tronque_exacts": 0, "tronque_fidelite_caractere": 0.9506, "detectes": 46}}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/atomes-niveaux.json'))\nprint('statut:',json.dumps(d.get('statut'),ensure_ascii=False)[:1200])\nprint('--- calibration keys:', list(d.get('calibration_44_oeuvres',{})))\nprint(json.dumps(d.get('calibration_44_oeuvres',{}),ensure_ … [88 caractères tronqués]`

  ```
statut: "hypothese_de_lecture_et_protocole_non_mesure"
--- calibration keys: ['source', 'n_oeuvres', 'parts_somme_1', 'statistiques', 'correlations_brutes', 'correlations_clr', 'comparaison_brut_clr', 'acp_clr', 'lecture']
{"source": "../../Panini/research/nipada/falsification/analytic_sigs_v1.json", "n_oeuvres": 44, "parts_somme_1": true, "statistiques": {"ÊTRE": {"moyenne": 0.107443, "ecart_type": 0.032566, "min": 0.050592, "max": 0.165658, "cv": 0.3031}, "DIFFÉRENCE": {"moyenne": 0.023207, "ecart_type": 0.010585, "min": 0.004031, "max": 0.043502, "cv": 0.4561}, "RAPPORT": {"moyenne": 0.088174, "ecart_type": 0.034694, "min": 0.033223, "max": 0.175124, "cv": 0.3935}, "ORIENTATION": {"moyenne": 0.006197, "ecart_type": 0.00308, "min": 0.000913, "max": 0.014632, "cv": 0.4971}, "SUJET": {"moyenne": 0.189031, "ecart_type": 0.028152, "min": 0.087297, "max": 0.233076, "cv": 0.1489}, "TEMPS": {"moyenne": 0.080068, "ecart_type": 0.023334, "min": 0.018835, "max": 0.127257, "cv": 0.2914}, "MODALITÉ": {"moyenne": 0.03647, "ecart_type": 0.019462, "min": 0.002513, "max": 0.098077, "cv": 0.5336}, "NOMBRE": {"moyenne": 0.095984, "ecart_type": 0.033624, "min": 0.056852, "max": 0.224591, "cv": 0.35
… [823 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/corpus-commun.json'))\nprint('statistiques:',json.dumps(d.get('statistiques'),ensure_ascii=False)[:1600])\nprint('--- statut:',json.dumps(d.get('statut'),ensure_ascii=False)[:800])\nEOF", "description": "Extract common corpus sta … [9 caractères tronqués]`

  ```
statistiques: {"familles": {"Afro-Asiatic": 4, "Atlantic-Congo": 4, "Austronesian": 4, "Indo-European": 5, "Sino-Tibetan": 4}, "langues_par_famille": {"Afro-Asiatic": ["udhr_amh", "udhr_arb", "udhr_hau_NE", "udhr_heb"], "Atlantic-Congo": ["udhr_ewe", "udhr_fuf_adlm", "udhr_ibo", "udhr_kin"], "Austronesian": ["udhr_ind", "udhr_jav", "udhr_mly_arab", "udhr_tgl"], "Indo-European": ["udhr_bel", "udhr_ell_monotonic", "udhr_eng", "udhr_fra", "udhr_hin"], "Sino-Tibetan": ["udhr_cmn_hant", "udhr_cnh", "udhr_ctd", "udhr_mya"]}, "n_caracteres": 3603, "n_familles": 5, "n_mots_ws": 566, "n_phrases": 42, "n_pivots": 1, "n_scripts": 10, "n_strates": 20, "n_textes": 21, "scripts": {"Adlm": 1, "Arab": 2, "Cyrl": 1, "Deva": 1, "Ethi": 1, "Grek": 1, "Hant": 1, "Hebr": 1, "Latn": 11, "Mymr": 1}}
--- statut: "corpus_construit_verifie"
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-epoque.json'))\nprint('keys', list(d))\nfor k in ['b7','udhr','bible']:\n    v=d[k]\n    print('===',k, type(v), list(v)[:20])\n    for kk in list(v)[:8]:\n        print(' ',kk,':',json.dumps(v[kk],ensure_ascii=False)[: … [65 caractères tronqués]`

  ```
keys ['tache', 'titre', 'date', 'methode', 'b7', 'udhr', 'bible']
=== b7 <class 'dict'> ['n_langues', 'n_concepts', 'n_langues_avec_libelle', 'n_langues_dans_paires', 'langues_hors_paires', 'meta_langues', 'agregats', 'regression', 'controles', 'paires']
  n_langues : 71
  n_concepts : 35
  n_langues_avec_libelle : 71
  n_langues_dans_paires : 64
  langues_hors_paires : ["am", "km", "ky", "lo", "mt", "si", "yo"]
  meta_langues : {"ar": {"famille": "Afro-Asiatic", "script": "Arab", "n_concepts": 28}, "bn": {"famille": "Indo-European", "script": "Beng", "n_concepts": 20}, "ca": {"famille": "Indo-European", "script": "Latn", "n_concepts": 31}, "cs": {"famille": "Indo-European", "script": "Latn", "n_concepts": 31}, "da": {"famille": "Indo-European", "script": "Latn", "n_concepts": 27}, "de": {"famille": "Indo-European", "script": "Latn", "n_concepts": 34}, "el": {"famille": "Indo-European", "script": "Grek", "n_concepts": 22}, "en": {"famille": "Indo-European", "script": "Latn", "n_concepts": 35}, "eo": {"famille": "Constructed", "script": "Latn", "n_concepts": 32}, "es": {"famille": "Indo-European", "script": "Latn", "
  agregats : {"toutes": {"n_paires": 4004, "top1_moyen": 0.1381102
… [7300 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/genealogie-deux-faces.json'))\nfor k in ['statut','convergence','divergence','a_mesurer','limites']:\n    v=d.get(k)\n    print('===',k,':',json.dumps(v,ensure_ascii=False)[:1400])\nEOF", "description": "Extract genealogy JSON ve … [16 caractères tronqués]`

  ```
=== statut : "mesuré, écrit, contrôlé"
=== convergence : [{"constat": "La surface passe avant la filiation, des deux côtés.", "preuve": "Panini §150 : β époque 0,1378 > β filiation 0,0489 (R² 0,30). Drave : le script est une porte (154/154 paires hors script au hasard exact), la famille ne vit que dans 56 paires de même script.", "ou": "reports/rapport-genealogie-deux-faces.md § 3.1"}, {"constat": "Le rapport filiation/surface est du même ordre : environ un tiers.", "preuve": "Panini : 0,0489/0,1378 = 0,355. J3.1 Bible : famille 0,181 / script 0,609 = 0,297.", "ou": "reports/rapport-retrieval-epoque.md § 4.3 et § 5"}, {"constat": "Les deux généalogies sont le même arbre sur les langues couvertes.", "preuve": "15/15 familles après appariement Niger-Congo→Atlantic-Congo ; 14/15 branches au nœud exact (15/15 si l'on accepte le descendant le plus proche pour Tibeto-Burman) ; Spearman 0,657 et Pearson 0,918 entre les distances P2 et Glottolog sur les 105 paires.", "ou": "reports/rapport-genealogie-deux-faces.md § 2.2"}, {"constat": "Les deux généalogies prédisent le retrieval de façon comparable.", "preuve": "Sur les 105 paires couvertes : R² 0,256 (Panini UDHR) contre 0,230 (Glottolog)
… [4507 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor f in ['reports/rapport-coordination-n2.json','reports/rapport-coordination-s.json','reports/rapport-coordination-r.json','reports/rapport-coordination-a.json']:\n    d=json.load(open(f))\n    print('===',f)\n    print('keys:', list(d))\n    for k in [ … [216 caractères tronqués]`

  ```
=== reports/rapport-coordination-n2.json
keys: ['date', 'head', 'ligne', 'objet', 'fiche', 'verdict', 'aucune_modification_n2', 'bug', 'checkpoints', 'chiffres', 'correctif', 'commande_n2', 'limites', 'fichiers_lus_non_modifies', 'references']
verdict : "eval_n2_propre.py lit les checkpoints RoPE comme des positions absolues et rend 8,0225 sur propre512-8k à 128 octets, contre 2,9726 à 128 et 2,7856 à 1024 au mètre RoPE. --rope est nécessaire mais non suffisant : le checkpoint de la porte a été entraîné avec le canal, et --rope seul rend 40,0658. Le correctif validé est --rope --canal-dir."
chiffres : {"propre512_8k": {"protocole": "validation data/corpus_propre/val.txt, fenêtres Van der Corput dans les chunks de 8192, 8 lots × 16 fenêtres", "courbes": {"absolu_sans_canal": {"128": 8.0225, "256": 8.971, "512": 11.3357, "1024": 38.5288, "source": "eval_n2_propre actuel, liste de longueurs étendue, sans --rope et sans canal"}, "rope_sans_canal": {"128": 40.0658, "256": 49.5308, "512": 59.8126, "1024": 65.7898, "source": "eval_n2_propre --rope seul, protocole sans canal"}, "rope_avec_canal": {"128": 2.9726, "256": 2.8988, "512": 2.8443, "1024": 2.7856, "source": "eval_n2_propre --rope
… [4146 caractères tronqués]
  ```

- **bash** `{"command": "wc -l docs/pilotage/semaine-autonome.md; grep -n '^#' docs/pilotage/semaine-autonome.md", "description": "Show semaine-autonome structure"}`

  ```
162 docs/pilotage/semaine-autonome.md
1:# Le chantier autonome — une semaine (7 → 14 novembre 2026)
11:## 1. L'objet
19:## 2. L'inventaire — ce qui est ouvert
21:### 2.1 Drave — le produit (priorité)
30:### 2.2 Drave — les chantiers voisins (coordination)
40:### 2.3 Panini — l'écosystème (intégration)
70:### 2.4 La surface d'intégration
79:## 3. La semaine — cinq jours, deux vagues par jour
100:## 4. Les règles du chantier
118:## 5. Les risques, nommés
128:## 6. La file (rappel)
134:## 7. Ce que la semaine doit avoir produit
142:## 3 bis. L'état du chantier (12 h 18, 07/11 → 18 h 22)
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-vie-quatre-jours.md", "description": "Read an existing multi-day report for style"}`

  ```
# Quatre jours de suite — deux refusés par le protocole, un qui dégrade

> Campagne : **cerveau** · expérience : la consolidation **séquentielle** sur un corpus
> **hétérogène** (`corpus_en`, dispersion ×2,9 — `rapport-consolidation-structure-partagee.md`) —
> le cas d'une **vie** : quatre journées, chacune rejouant cinq morceaux nouveaux, chacune
> reprenant le modèle de la veille (`--lora-depart`).
> Verdict : **le protocole refuse la moitié des journées, et celle qu'il accepte dégrade le texte
> tenu à l'écart.** Jour 1 : m30 **−0,92 %** ✓. Jours **2 et 3** : **aucune époque n'améliore la
> validation**, donc le protocole **rend le modèle inchangé** (0,00 %, au chiffre près) — un
> entraînement qui ne vaut rien **ne se publie pas**. Jour 4 : accepté, et la mesure tenue à
> l'écart **monte** (m30 **+0,36 %**, m0 **+0,61 %**).
> Date réelle : **2026-10-15 03 h 35-03 h 55 HAE** (heure lue sur la machine)
> Protocole : `tools/n4_dessin_b.py --objectif plein --ids /tmp/n4/ids-en.txt` · jour *j* = rejeu des
> morceaux 5j..5j+4 (5 morceaux, 8 époques, graine 0), en **reprise** du jour précédent
> (`--lora-depart`) · validation **m24** (jamais rejouée, choisie une fois pour toutes) · te
… [3528 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' tools/verifie_etat_a_jour.py 2>/dev/null; echo \"---HOOK---\"; ls -la .git/hooks | head -20; sed -n '1,120p' .git/hooks/pre-commit 2>/dev/null", "description": "Inspect state freshness checker and pre-commit hook"}`

  ```
#!/usr/bin/env python3
"""verifie_etat_a_jour.py — aucun fait commité sans sa ligne d'état.

POURQUOI CET OUTIL EXISTE. `en-cours` est la seule source de l'état, et le contrat
disait « seul le principal écrit ». Ce n'est pas une garantie : l'identité se déduit
d'une variable d'environnement absente — un « pair » est autodéclaré — et si la
principale s'arrête, l'état se fige. Surtout, rien ne comparait les commits : la
revue ne regardait que la DATE, donc deux commits du même jour passaient. Le 29/10,
A8.0 (15 h 51) a été commité après le dernier état (15 h 34) sans aucune alerte.

La garantie est au commit, pas dans la discipline d'un écrivain :
  --index  (hook pre-commit) : un commit qui prépare un fait (reports/, roadmap,
           backlog) sans toucher `en-cours` est REFUSÉ ;
  --head   : si un fait a été commité après le dernier commit d'`en-cours`, l'état
           est en retard — la session qui le voit le corrige, sans attendre.

Le journal est du récit dérivé (le hook l'archive) : il n'exige pas de ligne d'état.

Usage :
  python3 tools/verifie_etat_a_jour.py             # --head
  python3 tools/verifie_etat_a_jour.py --index     # pour le hook
  python3 tools/verifie_eta
… [9795 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' tools/porte-tableaux.sh", "description": "Inspect table gate rules"}`

  ```
#!/bin/bash
# porte-tableaux.sh — un tableau Markdown qui ne rend pas est un tableau qui n'existe PAS.
#
# POURQUOI CETTE PORTE EXISTE. Le 13/10, le premier tableau de `docs/etat-cerveau.md` s'affichait
# comme du TEXTE dans docwatch : une seule ligne (`| **C2 (cycle 2 régions)** | … |`) avait
# **4 cellules pour 5 colonnes** — un lien qui avait glissé d'une colonne. Le rendu (mistune,
# puis markdown_it, puis markdown) refuse alors le tableau ENTIER, sans rien dire : les 13 lignes
# disparaissent de la page et personne ne le voit, parce que le texte est toujours là, en gris.
#
# CE QU'ELLE VÉRIFIE (trois conditions, toutes nécessaires au rendu) :
#   1. l'en-tête et le séparateur d'un tableau ont le MÊME nombre de cellules ;
#   2. chaque ligne du corps a ce nombre de cellules ;
#   3. aucun `\|` ne subsiste : mistune ne le déséchappe NI dans un espace de code NI dans la
#      prose (il s'affiche alors littéralement). Pour une barre de valeur absolue dans du code,
#      on écrit `∣` (U+2223), qui rend partout et ne casse pas la lecture.
# Les tableaux DANS une citation (`> | … |`) sont valides et vérifiés aussi.
#
# CE QU'ELLE NE VÉRIFIE PAS : les tableaux « écrasés » sur une se
… [6759 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' tools/index_reports.py", "description": "Inspect report index generator"}`

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

- **bash** `{"command": "grep -n \"coordination\\|rapport-semaine\" reports/README.md | head -20; echo \"---\"; sed -n '1,60p' reports/README.md", "description": "Check README for coordination entries"}`

  ```
---
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
| [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 niveaux |
| [`rapport-corpus-commun.md`](rapport-corpus-commun.md) | **Panini** — le corpus commun UDHR |
| [`rapport-retrieval-epoque.md`](rapport-retrieval-epoque.md) | **Panini** — le retrieval contrôlé |

… [4582 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "offset": 128}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md</path>
<type>file</type>
<content>
128: ## 6. La file (rappel)
129: 
130: Les **29 tâches** de [`rapport-file-taches.md`](../../reports/rapport-file-taches.md) : **8
131: autonomes** (faites ou en cours), **11 en coordination**, **10 bloquées**. Les tâches autonomes
132: restantes sont dans le tableau du § 2.1 ; les autres sont des fiches de coordination.
133: 
134: ## 7. Ce que la semaine doit avoir produit
135: 
136: - le **produit** : 2 spans tranchés (ou déclarés), le schéma v2, la restitution v0, la porte verte ;
137: - **l'intégration** : une table atomes ↔ niveaux, un corpus commun, une mesure de retrieval à
138:   époque contrôlée, une fiche de généalogie à deux faces ;
139: - **la coordination** : un état daté de N2/S/R/A, les décisions prises et nommées ;
140: - **la consolidation** : la passe complète, un tag, le rapport de semaine, la roadmap à jour.
141: 
142: ## 3 bis. L'état du chantier (12 h 18, 07/11 → 18 h 22)
143: 
144: Le superviseur a lancé **10 tâches** (budget 21 600 s consommé). **Six sont « faites »**, trois ont
145: un **commit livré** mais un verdict « échec » (timeout
… [1103 caractères tronqués]
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine.md", "content": "# J5.1 — le rapport de semaine : le produit gagne 3,69 points de F1, l'intégration est bornée\n\n> **Ligne de roadmap** : **B13** (le moteur de pensée), **R0.7** (le bloc langue), **N2**, **S**,\n … [28525 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "{\n  \"titre\": \"J5.1 — le rapport de semaine : le produit gagne 3,69 points de F1, l'intégration est bornée\",\n  \"version\": 1,\n  \"date\": \"2026-11-13\",\n  \"tache\": \"J5.1\",\n  \"lignes_roadmap\": [\"B13\", \"R0.7\", \"N2\", \"S\", \"R\", \"A\", \"Panini\"],\n  \"statut\": \" … [25890 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-semaine.json > /dev/null && echo \"JSON OK\"; python3 -c \"import json;d=json.load(open('reports/rapport-semaine.json'));print('keys',list(d));print('decisions',len(d['decisions']),'rejets',len(d['rejets']),'reste',len(d['reste']))\"", "description": … [31 caractères tronqués]`

  ```
JSON OK
keys ['titre', 'version', 'date', 'tache', 'lignes_roadmap', 'statut', 'base', 'chiffres', 'decisions', 'rejets', 'reste', 'chronologie', 'limites', 'fichiers']
decisions 13 rejets 21 reste 12
  ```

- **bash** `{"command": "CIBLES=\"reports\" bash tools/porte-tableaux.sh 2>&1 | tail -20", "description": "Run table gate on reports", "timeoutMs": 120000}`

  ```
✅ 886 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3916 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-13)
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "old_string": "## 3 bis. L'état du chantier (12 h 18, 07/11 → 18 h 22)\n\nLe superviseur a lancé **10 tâches** (budget 21 600 s consommé). **Six sont « faites »**, trois ont\nun **commit livré** mais u … [2543 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md", "new_string": "**Reste** : J5.2 (passe complète, revue de documentation, tag annoté, release), les commits de\nS (11 verdicts + pointeur), le rapport A6.2, et la relance de la boucle.\n\n## 8. L'état d … [3906 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"2000\\|4000\\|budget\\|MOTS\" tools/verifie_en_cours.py | head -20; python3 tools/verifie_en_cours.py 2>&1 | tail -10", "description": "Check en-cours word budget and current state"}`

  ```
5:  1. un budget de **2 000 mots** ;
86:    if n > 2000:
87:        alertes.append(f"{n} mots > budget 2 000")
  en-cours · 1621 mots · 7 sections · 4 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-13, 23 h 10 HNE (heure locale, EST).**", "old_string": "**Mis à jour : 2026-11-13, 22 h 37 HNE (heure locale, EST).**"}`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 10}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-13, 22 h 37 HNE (heure locale, EST).**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11
9: 
10: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).

(Showing lines 1-10 of 140. Use offset=11 to continue.)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 90, "limit": 50}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
90: - **Pensée — B13 (actif)** : **183/183**, gold 432, DRVM 114/114 + 5/5, sto 5/5 ; pragmatique 130/432 ; **`r035` réglé** (237/238, 0,9958) ; **convention des GV réglée** (F1 **0,7902**, 0 perte d'attachement) ; **schéma v2** publié (26 cas, 0 échec ; `meta.partition`/`meta.alternative`, v1 lue) ; **restitution v0** : **46/46 surfaces**, miroir **0,1087** ; [fiche](../../reports/rapport-restitution-v0.md).
91: - **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.
92: - **Panini J2.1/J2.2/J3.1/J3.2** : table **14 atomes** ; UDHR **418/438** ; **J3.1** : l'écriture domine, l'époque ne pèse pas à écriture contrôlée ; **J3.2** : les deux faces diffèrent — `lang_distance` couvre **5/21** langues (Glottolog **21/21**), **154/154** paires hors script au hasard, la famille vit dans **2-3 paires**, **V14 : 3/21** ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [époque](../../reports/rapport-retrieval-epoque.md), [deux faces](../../repor
… [3858 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-13, 23 h 10 HNE (heure locale, EST).**", "old_string": "**Mis à jour : 2026-11-13, 22 h 37 HNE (heure locale, EST).**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Panini J2.1/J2.2/J3.1/J3.2** : table **14 atomes** ; UDHR **418/438** ; **J3.1** : l'écriture domine, l'époque ne pèse pas à écriture contrôlée ; **J3.2** : les deux faces diffèrent — `lang_ … [1819 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **718** / **812** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **716** / **810** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013, porte 54,5202 ; résidence mono-GPU 16 GiB ; cache Q4_K non câblé) | **A2.6** (experts et tête … [1701 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**N2** — **porte propre** (manque 0,2856 val / 0,3566 test) ; 2 048 fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035`, convention GV, schéma v2, restitution v0 faits**, res … [1338 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
1: # Les rapports — données intermédiaires et références
2: 
3: > **Ce dossier porte les résultats et les données de nos travaux**, jamais la documentation de référence
4: > (elle est dans [`docs/`](../docs/)). Les fiches courantes sont citées depuis le tableau de bord
5: > [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md).
6: 
7: > **Navigation** : [la carte des sujets](../docs/theorie/carte.md) · [l'état du moment](../docs/pilotage/en-cours.md) ·
8: > [l'inventaire des docs](../docs/README.md) · [le journal](../journal/README.md).
9: >
10: > **Contexte** : la fiche [`07-mesures-couche-commune.md`](07-mesures-couche-commune.md) est un **hub** de
11: > **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par
12: > partie**, jamais en entier ; l'index exhaustif des fiches est [`INDEX.md`](INDEX.md).
13: 
14: ## Les fiches courantes
15: 
16: | fichier | ce qu'il porte |
17: |---|---|
18: | [`rapport-atomes-niveaux.md`](rapport-atomes-niveaux.md) | **Panini** — la table 14 atomes × 8 niveaux |
19: | [`rapport-corpus-commun.md
… [1326 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| fichier | ce qu'il porte |\n|---|---|\n| [`rapport-semaine.md`](rapport-semaine.md) | **J5.1** — le rapport de semaine : produit, intégration, décisions, rejets, reste |\n| [`rapport-coordination-n2.m … [743 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-etat-s.md`](rapport-etat-s.md) | **B13** — l'état de S : /paragraphes 19/19 dans le working tree, banque 150/207, rétro-traduction absente ; un clone à `523d8c1` voit 8/4/11 |", "old_string" … [143 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "git log --oneline -3 -- reports/rapport-coordination-r.md reports/rapport-coordination-r.json; echo \"---\"; git status --porcelain reports/rapport-coordination-* reports/rapport-semaine.*", "description": "Check which coordination files are tracked"}`

  ```
a934d779 R0.7 — LE TAGGER POS SUR LE GOLD 612 : 0,9475 (3012/3179), +8,49 PTS, LA RÈGLE DIT INTÉGRER ; LA CLÉ ÉTAIT PRÉSENTE ET 0,8500 ÉTAIT DATÉ (0,8625)
---
?? reports/rapport-coordination-a.json
?? reports/rapport-coordination-a.md
?? reports/rapport-coordination-n2.json
?? reports/rapport-coordination-n2.md
?? reports/rapport-coordination-s.json
?? reports/rapport-coordination-s.md
?? reports/rapport-semaine.json
?? reports/rapport-semaine.md
  ```

- **bash** `{"command": "python3 tools/index_reports.py; python3 tools/index_reports.py --verifier && echo \"INDEX A JOUR\"", "description": "Regenerate and verify reports index"}`

  ```
715 fiches → reports/INDEX.md
INDEX A JOUR
  ```

- **bash** `{"command": "ls reports/*.md | wc -l; ls reports/*.md | grep -v -E '/(README|INDEX|historique-)' | wc -l; ls reports/*.md | grep -E '/(README|INDEX|historique-)'", "description": "Recount report fiches"}`

  ```
718
715
reports/historique-passes-portes.md
reports/INDEX.md
reports/README.md
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40", "description": "Run documentation review after edits", "timeoutMs": 180000}`

  ```
revue de documentation · 718 fiche(s) · 812 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -8", "description": "Check en-cours structure and word budget"}`

  ```
en-cours · 1790 mots · 7 sections · 4 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "CIBLES=\"docs reports\" bash tools/porte-tableaux.sh 2>&1 | tail -8", "description": "Run table and link gate on docs and reports", "timeoutMs": 180000}`

  ```
✅ 1349 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3926 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-13)
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -30", "description": "Check document budgets", "timeoutMs": 120000}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    7351    385   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2661    199   T1   2800  reports/README.md
    2404    162   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [519 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **J5.1** : rapport de semaine (F1 **0,7533 → 0,7902**, attachement **236 → 237**, tagger **0,9475**, intégration bornée, **13 décisions**, **21 rejets**) ; [rapport](../../reports/rapport-sema … [1280 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"^\\*\\*N2\\*\\* —\" docs/pilotage/en-cours.md", "description": "Locate remaining line"}`

  ```
126:**N2** — **porte propre** (manque 0,2856 val / 0,3566 test) ; 2 048 fini ; **R1** — R1.2-1024 ; **Pensée** — T132/T133, gold 200+, **`r035`, convention GV, schéma v2, restitution v0 faits**, reste `g017` ; **J3.2** — fait : [deux faces](../../reports/rapport-genealogie-deux-faces.md) ; prochaine mesure : **signature V14 multilingue des 21 langues** ; **S** — 11 verdicts à committer + pointeur ; **N4** — consigne ; **B10.3** — `z` ; **B13** — 183/183 ; **R0.7** — tagger 612 : **0,9475 (+8,49)**, **intégrer**, split réel à tenir ; **A** — rapport A6.2, A8.3b2 ; **D** — CEGEP **62 documents** (`data/corpus_ocr_cegep`), **passe finie** (79 vertes, 4 rouges : `indice`, `melange` tolérées ; `sessions` → heartbeat) ; **J5.2** — la passe complète, la revue de documentation, le tag et la release ; [fiche](../../reports/rapport-ocr-cegep-64.md).
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**N2** — porte propre (0,2856 val / 0,3566 test) ; **R1** — R1.2-1024 ; **Pensée** — `g017`, T132/T133, gold 200+ ; **J3.2** — prochaine mesure : **V14 des 21 langues** ; **S** — 11 verdicts + p … [1014 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -8", "description": "Recheck document budgets", "timeoutMs": 120000}`

  ```
1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4048 mots (budget 4 000)

  avertissements :
     · 47 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4048 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -5", "description": "Recheck en-cours structure"}`

  ```
en-cours · 1678 mots · 7 sections · 4 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 86, "limit": 45}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
86: 
87: - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
88: - **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
89: - **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-inventaire`, autotest 5/5) ; deux conditions nommées (placement = métadonnée, saut de calcul conditionnel) ; [fiche](../../reports/rapport-n3-inventaire.md).
90: - **Pensée — B13 (actif)** : **183/183**, gold 432, DRVM 114/114 + 5/5, sto 5/5 ; pragmatique 130/432 ; **`r035` réglé** (237/238, 0,9958) ; **convention des GV réglée** (F1 **0,7902**, 0 perte d'attachement) ; **schéma v2** publié (26 cas, 0 échec ; `meta.partition`/`meta.alternative`, v1 lue) ; **restitution v0** : **46/46 surfaces**, miroir **0,1087** ; [fiche](../../reports/rapport-restitution-v0.md).
91: - **L — le bloc langue** : contrat ; frontière scrip
… [4067 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183**, gold 432 ; pragmatique 130/432 ; **`r035` réglé** (237/238, 0,9958) ; **convention des GV réglée** (F1 **0,7902**, 0 perte d'attachement) ; **schéma v2* … [613 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Panini J2.1/J2.2/J3.1/J3.2** : table **14 atomes** ; UDHR **418/438** ; **J3.1** : script domine, date non significative ; **J3.2** : les deux faces diffèrent — `lang_distance` couvre **5/21 … [925 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **J5.1** : rapport de semaine (F1 **0,7533 → 0,7902**, tagger **0,9475**, **13 décisions**, **21 rejets**) ; [rapport](../../reports/rapport-semaine.md) + JSON.\n- **Coordination J4** : N2 **2 … [911 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |", "old_string": … [229 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9475 (+8,49), intégrer** ; R2/R3 attendent N5/N4 | **route API derrière drapeau** ; **split réel tenu à l'écart** |", "old_string": "| * … [198 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**N2** — porte propre (0,2856 val / 0,3566 test) ; **Pensée** — `g017`, T132/T133, gold 200+ ; **J3.2** — prochaine mesure : **V14 des 21 langues** ; **S** — 11 verdicts + pointeur ; **R0.7** —  … [465 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation|budget\" | head -5; python3 tools/verifie_en_cours.py 2>&1 | tail -3", "description": "Recheck budgets and en-cours", "timeoutMs": 120000}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
  T0 max : 4005 mots (budget 4 000)
  ❌ 1 violation(s) :
     · T0 : 4005 mots (AGENTS + en-cours + une tâche) > budget 4 000
  en-cours · 1635 mots · 7 sections · 4 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**N2** — porte (0,2856 val / 0,3566 test) ; **Pensée** — `g017`, T132/T133, gold 200+ ; **J3.2** — **V14 des 21 langues** ; **S** — 11 verdicts + pointeur ; **R0.7** — **0,9475**, intégrer, spli … [379 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation\" | head -3", "description": "Recheck T0 budget", "timeoutMs": 120000}`

  ```
T0 max : 3999 mots (budget 4 000)
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -6", "description": "Run doc review again", "timeoutMs": 180000}`

  ```
revue de documentation · 718 fiche(s) · 812 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "CIBLES=\"docs reports\" bash tools/porte-tableaux.sh 2>&1 | tail -5", "description": "Run table/link gate again", "timeoutMs": 180000}`

  ```
✅ 1349 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3926 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-13)
  ```

- **bash** `{"command": "grep -n \"r035.*tranché\\|Non modifiés\\|Mis à jour.*semaine-autonome\\|reports/README\" reports/rapport-semaine.md", "description": "Locate report lines to fix"}`

  ```
26:| **produit** | 2 spans tranchés (ou déclarés), schéma v2, restitution v0, porte verte | `r035` tranché (1 span) ; `g017` et `s065` déclarés ; schéma v2 (26 cas / 0 échec) ; restitution v0 (46/46, miroir 0,1087) ; autotest 183/183 | **1 span sur 2** ; la porte complète est J5.2 |
308:- **Mis à jour** : [`docs/pilotage/semaine-autonome.md`](../docs/pilotage/semaine-autonome.md)
311:- **Non modifiés** : les fiches et JSON ci-dessus (sauf ce rapport et son JSON), `docs/`,
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine.md", "new_string": "| **produit** | 2 spans tranchés (ou déclarés), schéma v2, restitution v0, porte verte | `r035` tranché (1 span), `g017` déclaré, `s065` cible fausse déclarée ; schéma v2 (26 cas / 0 échec) ; r … [405 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine.md", "limit": 14, "offset": 300}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine.md</path>
<type>file</type>
<content>
300:   `corpus-commun.json` ; [`rapport-retrieval-epoque.md`](rapport-retrieval-epoque.md) +
301:   `retrieval-epoque.json` ; [`rapport-genealogie-deux-faces.md`](rapport-genealogie-deux-faces.md)
302:   + `genealogie-deux-faces.json`.
303: - **Relus, J4** : [`rapport-coordination-n2.md`](rapport-coordination-n2.md) +
304:   `rapport-coordination-n2.json` ; [`rapport-coordination-s.md`](rapport-coordination-s.md) +
305:   `rapport-coordination-s.json` ; [`rapport-coordination-r.md`](rapport-coordination-r.md) +
306:   `rapport-coordination-r.json` ; [`rapport-coordination-a.md`](rapport-coordination-a.md) +
307:   `rapport-coordination-a.json`.
308: - **Mis à jour** : [`docs/pilotage/semaine-autonome.md`](../docs/pilotage/semaine-autonome.md)
309:   (l'état de chaque jour) ; [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md)
310:   (compteurs et ligne J5.1) ; [`reports/INDEX.md`](INDEX.md) (régénéré).
311: - **Non modifiés** : les fiches et JSON ci-dessus (sauf ce rapport et son JSON), `docs/`,
312:   `tools/`, `journal/` (le hook les archive), `drave-core/`,
… [96 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine.md", "new_string": "- **Mis à jour** : [`docs/pilotage/semaine-autonome.md`](../docs/pilotage/semaine-autonome.md)\n  (l'état de chaque jour) ; [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md)\n  (compt … [759 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine.json", "new_string": "    \"mis_a_jour\": [\"docs/pilotage/semaine-autonome.md\", \"docs/pilotage/en-cours.md\", \"reports/README.md\", \"reports/INDEX.md\"],\n    \"non_modifies\": [\"les fiches et JSON ci-dessus … [307 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-semaine.json has been updated successfully.
  ```

- **bash** `{"command": "git status --short | grep -E 'rapport-semaine|rapport-coordination|semaine-autonome|en-cours|reports/README|reports/INDEX'", "description": "Check status of intended commit files"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/semaine-autonome.md
 M reports/INDEX.md
 M reports/README.md
?? reports/rapport-coordination-a.json
?? reports/rapport-coordination-a.md
?? reports/rapport-coordination-n2.json
?? reports/rapport-coordination-n2.md
?? reports/rapport-coordination-s.json
?? reports/rapport-coordination-s.md
?? reports/rapport-semaine.json
?? reports/rapport-semaine.md
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-semaine.json > /dev/null && echo \"JSON OK\"; python3 tools/index_reports.py --verifier && echo \"INDEX OK\"", "description": "Validate JSON and index"}`

  ```
JSON OK
INDEX OK
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -4; echo \"---\"; python3 tools/verifie_en_cours.py 2>&1 | tail -2; echo \"---\"; python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation\" | head -3", "description": "Run review, state, and budget checks", "timeoutMs": 180000 … [1 caractères tronqués]`

  ```
revue de documentation · 718 fiche(s) · 812 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
---
  en-cours · 1629 mots · 7 sections · 4 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
---
  T0 max : 3999 mots (budget 4 000)
  ```

- **bash** `{"command": "CIBLES=\"docs reports\" bash tools/porte-tableaux.sh 2>&1 | tail -4", "description": "Final table and link gate", "timeoutMs": 180000}`

  ```
✅ 1349 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3927 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-13)
  ```

- **bash** `{"command": "git diff -- docs/pilotage/en-cours.md | head -120", "description": "Review en-cours diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index c5dd305e..77bcf830 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-13, 22 h 37 HNE (heure locale, EST).**
+**Mis à jour : 2026-11-13, 23 h 10 HNE (heure locale, EST).**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -87,9 +87,11 @@
 - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
 - **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
 - **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-inventaire`, autotest 5/5) ; deux conditions nommées (placement = métadonnée, saut de calcul conditionnel) ; [fiche](../../reports/rapport-n3-inventaire.md).
-- **Pensée — B13 (actif)** : **183/183**, gold 432, DRVM 114/114 + 5/5, sto 5/5 ; pragmatique 130/432 ; **`r035` réglé** (
… [5902 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- docs/pilotage/semaine-autonome.md | head -160", "description": "Review semaine-autonome diff"}`

  ```
diff --git a/docs/pilotage/semaine-autonome.md b/docs/pilotage/semaine-autonome.md
index ae7afa96..42d4e081 100644
--- a/docs/pilotage/semaine-autonome.md
+++ b/docs/pilotage/semaine-autonome.md
@@ -139,11 +139,12 @@ restantes sont dans le tableau du § 2.1 ; les autres sont des fiches de coordin
 - **la coordination** : un état daté de N2/S/R/A, les décisions prises et nommées ;
 - **la consolidation** : la passe complète, un tag, le rapport de semaine, la roadmap à jour.
 
-## 3 bis. L'état du chantier (12 h 18, 07/11 → 18 h 22)
+## 3 bis. L'état du chantier (12 h 18, 07/11 → 23 h 00, 13/11)
 
 Le superviseur a lancé **10 tâches** (budget 21 600 s consommé). **Six sont « faites »**, trois ont
 un **commit livré** mais un verdict « échec » (timeout de l'agent après le commit — l'acceptation
-prime désormais, correctif à committer), une est bloquée.
+prime désormais), une était bloquée. La reprise du **13/11** a ajouté **quatre coordinations**
+(N2, S, R, A) et la consolidation J5.
 
 | tâche | verdict | livrable | commit |
 |---|---|---|---|
@@ -155,8 +156,43 @@ prime désormais, correctif à committer), une est bloquée.
 | J2.1 atomes ↔ niveaux | ✅ fait | 14/14 lignes | `9c7f71dc` |
… [4540 caractères tronqués]
  ```

- **bash** `{"command": "git add docs/pilotage/en-cours.md docs/pilotage/semaine-autonome.md reports/README.md reports/INDEX.md reports/rapport-semaine.md reports/rapport-semaine.json reports/rapport-coordination-n2.md reports/rapport-coordination-n2.json reports/rapport-coordination-s.md reports/rapport-coordi … [175 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/semaine-autonome.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
MM journal/sessions/session-3ffa6026-9a7d-4905-ac06-6b9708d65ba7/digest.md
MM journal/sessions/session-3ffa6026-9a7d-4905-ac06-6b9708d65ba7/rapport.md
M  reports/INDEX.md
M  reports/README.md
A  reports/rapport-coordination-a.json
A  reports/rapport-coordination-a.md
A  reports/rapport-coordination-n2.json
A  reports/rapport-coordination-n2.md
A  reports/rapport-coordination-s.json
A  reports/rapport-coordination-s.md
A  reports/rapport-semaine.json
A  reports/rapport-semaine.md
  ```

- **bash** `{"command": "git commit -m \"J5.1 — LE RAPPORT DE SEMAINE : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 237, TAGGER 0,9475 (+8,49, INTÉGRER), INTÉGRATION BORNÉE (TABLE 14/14, CORPUS 418/438), 13 DÉCISIONS, 21 REJETS\" -m \"J1–J3 (07/11) : r035 237/238 ; convention GV F1 0,7902 ; schéma v2 26/0 ; restituti … [745 caractères tronqués]`
