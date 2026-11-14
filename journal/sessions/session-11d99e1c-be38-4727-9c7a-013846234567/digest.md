# Session DSH — relecture

- identifiant : `session-11d99e1c-be38-4727-9c7a-013846234567`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-13 22:41:42
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J4.4 : la coordination A — A6.2 est libre (le MoE local 18 Go existe ; le blocage est la résidence mono-GPU) et A8.3b2 est nommée. **Ne modifie rien dans A** (ni natifs, ni données). Fiche `reports/rapport-coordination-a.md` + JSON : l'état des deux lignes, les commandes, les décisions à prendre.

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

- **bash** `{"command": "pwd && ls -la && git log --oneline -15", "description": "List repo root and recent commits"}`

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
drwxr-xr-x. 1 stephane stephane   180 13 nov 22:41 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   952 13 nov 21:34 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 74750 13 nov 22:36 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [2826 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/ | head -60 && echo '---' && ls journal/ | tail -20", "description": "List reports and journal"}`

  ```
total 23356
drwxr-xr-x. 1 stephane stephane   74750 13 nov 22:36 .
drwxr-xr-x. 1 stephane stephane     686  6 nov 09:52 ..
drwxr-xr-x. 1 stephane stephane     102 24 oct 15:52 07
-rw-r--r--. 1 stephane stephane    4447 28 oct 09:17 07-mesures-couche-commune.md
-rw-r--r--. 1 stephane stephane     907 29 oct 16:25 a26-bilan.json
-rw-r--r--. 1 stephane stephane    1163  1 nov 20:40 a26-lot-disque.json
-rw-r--r--. 1 stephane stephane    1121 30 oct 08:57 a80-audit-final.json
-rw-r--r--. 1 stephane stephane     560 30 oct 00:04 a80-indice-qualifie.json
-rw-r--r--. 1 stephane stephane     672 29 oct 23:42 a80-melange-qualifie.json
-rw-r--r--. 1 stephane stephane     430 30 oct 08:57 a80-pannes-ppl.json
-rw-r--r--. 1 stephane stephane     630 29 oct 17:07 a80-porte-adaptateur.json
-rw-r--r--. 1 stephane stephane     521 29 oct 16:40 a80-porte-budget.json
-rw-r--r--. 1 stephane stephane     625 29 oct 22:07 a80-porte-bus.json
-rw-r--r--. 1 stephane stephane     654 29 oct 22:19 a80-porte-bus-socket.json
-rw-r--r--. 1 stephane stephane     677 29 oct 21:05 a80-porte-c4-retard.json
-rw-r--r--. 1 stephane stephane     600 29 oct 20:06 a80-porte-consolidation.json
-rw-r--r--. 1 stephane stepha
… [3342 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"A6\\.2\\|A8\\.3b2\\|J4\\.4\" --include='*.md' --include='*.json' --include='*.py' --include='*.sh' . 2>/dev/null | head -80", "description": "Search references to A6.2, A8.3b2, J4.4"}`

  ```
./reports/rapport-coherence-docs-3.md:96:  page (ordre du jour, file, décisions, A6.2) est à jour.
./reports/r03-banc-extractif.json:7345:    "reponse": "bloqué, nommé : B1.5 (corpus d'articles), A3.4 (compte Colab), A5.4 (FPGA), A6.2 (pas de MoE local), B10.3 (B10.2bis abs"
./reports/r03-banc-extractif.json:7352:    "reponse": "bloqué, nommé : B1.5 (corpus d'articles), A3.4 (compte Colab), A5.4 (FPGA), A6.2 (pas de MoE local), B10.3 (B10.2bis abs"
./reports/r03-banc-extractif.json:7359:    "reponse": "bloqué, nommé : B1.5 (corpus d'articles), A3.4 (compte Colab), A5.4 (FPGA), A6.2 (pas de MoE local), B10.3 (B10.2bis abs"
./reports/r03-banc-extractif.json:7366:    "reponse": "bloqué, nommé : B1.5 (corpus d'articles), A3.4 (compte Colab), A5.4 (FPGA), A6.2 (pas de MoE local), B10.3 (B10.2bis abs"
./reports/r03-banc-extractif.json:7380:    "reponse": "bloqué, nommé : B1.5 (corpus d'articles), A3.4 (compte Colab), A5.4 (FPGA), A6.2 (pas de MoE local), B10.3 (B10.2bis abs"
./reports/r03-banc-extractif.json:8579:   "or": "Ce qui n'y est pas, et pourquoi : A3.4, A5.4, A6.2, B1.5 sont bloqués ",
./reports/r03-banc-extractif.json:8585:    "reponse": "Ce qui n'y est pas, et pourquoi : A3.4,
… [10462 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"A6\\|A8\\|J4\\|coordination\" docs/pilotage/roadmap.md | head -80", "description": "Roadmap lines A6 A8 J4"}`

  ```
30:| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.6 partiel ; A3.2/A3.3 mesurées ; **A8.3c/d expliqués** ; **A2.6/A8.3 : le [lot](../theorie/glossaire/entrees/lot.md) ne divise pas les lectures denses (+27 % calcul, PPL −0,006 %)** | **A2.6** (experts : A6.2 bloqué) ; le lot ≥ 2 assumé |
84:8. **Les bloqués** : A3.4 ([Colab](../theorie/glossaire/entrees/colab-notebook-tunnel.md)), A5.4 ([FPGA](../theorie/glossaire/entrees/fpga.md)) ; A6.2 ([MoE](../theorie/glossaire/entrees/moe.md) local), B1.5 (corpus scientifique) — on prend la ligne
98:[A1–A8] lasts 1 day and is 100% complete and is colored in #2e7d32
99:[A8.0/A8.3a] lasts 1 day and is 100% complete and is colored in #2e7d32
100:[A8.3b/c] lasts 1 day and is 100% complete and is colored in #2e7d32
102:[A3.4/A5.4/A6.2] lasts 1 day and is colored in #b03a2e
117:[A8.0/A8.3a] starts at [A1–A8]'s end
118:[A8.3b/c] starts at [A8.0/A8.3a]'s end
119:[A2.6] starts at [A8.3b/c]'s end
120:[A3.4/A5.4/A6.2] starts at [A2.6]'s end
148:| **A2** | placer sur une machine : [KV](../theorie/glossai
… [1053 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-a.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-a.md</path>
<type>file</type>
<content>
1: # État du chantier A — le moteur : deux bloqués réels, un faux bloqué, une frontière à requalifier
2: 
3: > **Ligne de roadmap** : **A** (le moteur) · **Date** : 2026-11-06, 21 h 51 HNE · **Branche** : `s/v7` ·
4: > **HEAD** : `7a876f70` (le HEAD a bougé pendant l'audit : `d31aa9a2` → `7a876f70`) ·
5: > **Mission** : lecture seule, aucun code, aucun fichier existant modifié ; deux fichiers neufs.
6: >
7: > **Verdict** : ⚠️ **l'état A est sain, le récit A est en retard.** Les lignes fermées le sont
8: > réellement ; **A8.3a est fait pour 3 portes sur 19** (et non « fait » tout court) ; **A2.6 est
9: > partiel mais libre** — sa tête est **décidée** (refusée), ses experts ne sont **pas** bloqués par
10: > l'absence d'un MoE : un **Qwen3-30B-A3B Q4 de 18 Go est présent et tourne**. Les **deux seuls
11: > bloqués réels** de A sont **A3.4** (compte Colab) et **A5.4** (carte Stratix V). **A6.2 est
12: > mal classé** : aucune ressource ne manque (le MoE local existe) ; c'est une tâche de code/mesure,
13: > pas un bloqué. **A23 a raison sur l'effet** (A2.6 ne doit pas être l
… [20524 caractères tronqués]
  ```

- **bash** `{"command": "ls docs/pilotage/backlog/ | grep -i \"A6\\|A8\\|A2.6\" ; echo '---'; grep -rn \"J4\" docs/pilotage/ | head -40", "description": "Backlog A6/A8 files and J4 plan"}`

  ```
A2.6-ordonnanceur.md
A6.2-moe-local.md
A8.0-portes-ppl.md
A8.3-defaut.md
---
docs/pilotage/semaine-autonome.md:47:- **7 axes** ; le noyau J4 (ℝ, CIC-lite) est **actif** ; NIPADA (produit) est **bloqué** (DTP arrêté
docs/pilotage/semaine-autonome.md:93:| **J4 · 10/11** | matin | la **coordination** N2 (le mètre RoPE), S (les 11 verdicts), R (R1.1) | des fiches de coordination, 0 écriture S/D/N2 |
docs/pilotage/semaine-autonome.md:158:| J4.x coordination | ⏳ à faire | — | — |
docs/pilotage/semaine-autonome.md:161:**Reste** : J4 (coordination N2/S/R/A), J5 (rapport de semaine, passe, tag), et la relance de la
  ```

- **bash** `{"command": "sed -n '1,220p' docs/pilotage/semaine-autonome.md", "description": "Read autonomous week plan"}`

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

- **bash** `{"command": "ls docs/pilotage/ && echo '---' && grep -rln \"J4\\.\\|coordination A\\|A8.3b2\" docs/ journal/ reports/ tools/ 2>/dev/null | head -40", "description": "Find J4 coordination task files"}`

  ```
backlog
chantiers.md
en-cours.md
manques.md
plan-travail.md
programme-r.md
README.md
references-non-regression.md
roadmap.md
semaine-autonome.md
utilisation.md
---
docs/pilotage/semaine-autonome.md
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/session.jsonl.zstd
journal/sessions/8b315bb2-abba-4033-b3d4-177d04b4f194/session.jsonl.zstd
journal/sessions/31f26a6e-65f5-480d-be32-36b9f425b3dd/session.jsonl.zstd
journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/session.jsonl.zstd
journal/sessions/d629d7d7-e122-4596-8757-f4264a2b15cf/session.v4.jsonl.zstd
journal/sessions/fe3c05f0-834b-44f2-8739-501865d652c1/session.v4.jsonl.zstd
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/session.v4.jsonl.zstd
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
journal/sessions/1555bdd3-27e9-4779-b1e7-716e32399c11/session.v4.jsonl.zstd
journal/sessions/082fe8ca-3e1e-4454-b91b-12586843e880/session.v4.jsonl.zstd
journal/sessions/538288b3-117b-4daf-8d16-0cd8d6b0090d/digest.md
journal/sessions/session-a9b5216e-5f4b-4935-8ba0-2ec7d42aaf89/digest.md
journal/sessions/session-932afd57-1363-4133-b6f1-64f7d937f38d/ses
… [659 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nprint(json.dumps(p, ensure_ascii=False, indent=1)[:12000])\nPY", "description": "Read chantier plan JSON"}`

  ```
{
 "nom": "Semaine 07/11 → 14/11 — le produit et l'intégration Panini",
 "principe": "Une tâche n'est finie que si son acceptation passe ; l'agent commite, le superviseur vérifie.",
 "taches": [
  {
   "id": "J0",
   "jour": 0,
   "titre": "Le contrôle du superviseur",
   "mandat": "Réponds exactement le mot OK, sans autre texte. C'est un test de liaison du superviseur.",
   "budget_min": 2,
   "acceptation": [
    {
     "commande": "python3 -c \"print('LIAISON-OK')\"",
     "attendu": "LIAISON-OK"
    }
   ]
  },
  {
   "id": "J1.1",
   "jour": 1,
   "titre": "r035 : la relative zéro",
   "mandat": "Tâche J1.1 du chantier : la relative zéro (r035, « The film she talks about is out. »). Reproduis, explique, propose UNE règle générale mesurée sur dev/test ; si elle tient (attachement 236→237, POS/F1 stables), intègre-la et commite avec une fiche `reports/rapport-r035.md` + `reports/pensee-r035.json`. Sinon, écris la fiche du rejet (chiffres, raison) et commite-la. Règles : ne touche pas S/D/N2 ; 183/183 portes ; en-cours à jour.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-r035.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    },
   
… [10800 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' reports/rapport-coordination-s.md; echo '======'; sed -n '1,160p' reports/rapport-coordination-r.md", "description": "Read coordination S and R reports"}`

  ```
# S — les 11 verdicts de `/paragraphes` ne sont pas dans git

> **Ligne de roadmap** : S · **Date** : 2026-11-13 · **HEAD parent mesuré** : `ced21933`
> · **Sous-module `tools/structures`** : `523d8c1` · **Verdict** : les 11 verdicts a004–a009
> sont **11 lignes non committées** de `donnees/paragraphes-validations.jsonl` (lignes **9–19**)
> : **6 `resolu`, 1 `compatible`, 4 `exclu`**, soit **7 acceptés et 4 exclus**. Le working tree
> voit **19 verdicts / 11 acceptés / 0 candidat sans verdict** ; un clone à `523d8c1` voit
> **8 verdicts / 4 acceptés / 11 candidats sans verdict**. **Aucun fichier de `tools/structures/`
> n'est modifié par cette fiche** : l'unique modification du sous-module est celle des 11
> verdicts, antérieure à la fiche.

**En trois lignes.** (1) Les 11 verdicts sont des verdicts de **candidat**, pas de paragraphe :
six paragraphes (`a004`–`a009`), onze candidats, ajoutés le **2026-11-04** entre **15:03:43** et
**15:10:08**. (2) Le fichier est **append-only** et le diff est **+11 / −0** ; rien n'est committé.
(3) La session S doit committer le fichier **dans le sous-module**, puis avancer le **pointeur**
`tools/structures` dans le parent : sans les deux, un clon
… [18806 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' docs/pilotage/backlog/A6.2-moe-local.md", "description": "Read A6.2 backlog"}`

  ```
# A6.2 — Routage MoE appris (MoE local)

> **Statut** : bloquée · **Priorité** : P3 · **Programme** : A · **Dépend de** : A6 · **Bloqué par** : aucun MoE local dans 16 Go de VRAM
> **Ligne de roadmap** : A6.2 · **Fiche de résultat attendue** : rapport-a62-moe.md (à créer dans `reports/`)
> **Résumé** : Faire choisir les experts par les logs, avec une qualité égale et un coût de routage divisé.
> **Glossaire** : [MoE](../../theorie/glossaire/entrees/moe.md) · [expert](../../theorie/glossaire/entrees/expert.md) · [routeur](../../theorie/glossaire/entrees/routeur.md) · [k-WTA](../../theorie/glossaire/entrees/k-wta.md).

## Le besoin

Aucun MoE local ne tient dans 16 Go de VRAM ; le routage appris reste donc non mesuré.

## L'état

A6.1 et A6.3 ont rendu leurs négatifs ; A6.2 bloqué par le matériel.

## La porte

Qualité égale, coût de routage ÷10, sur un MoE qui tient.

## Contrôles négatifs

- routage aléatoire ; routage dense ; même budget

## Prochaine action

Dès qu'un MoE tient, mesurer le routage ; sinon, garder la ligne bloquée et prendre la suivante.

## Voir aussi

- [Programme A](../roadmap.md#programme-a--le-moteur-la-drave-les-flux)
- [Manques, M1](../../pilotage/manques.m
… [2 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' reports/rapport-a83b-decision.md; echo '====JSON===='; cat reports/a83b-decision.json", "description": "Read A8.3b decision report and JSON"}`

  ```
# A8.3b/c — décision : le défaut reste opt-in, la cause est le chemin lot

> **Ligne de roadmap** : A8.3b/c · **Date** : 2026-10-29 · **Verdict** : ⛔ **défaut refusé** —
> le signe du mélange 1 % bascule avec le **chemin lot binaire** (lot 1 contre lot ≥ 2), pas
> avec la taille du cache (ctx 64/256/512 identiques). A8.3 reste **opt-in**.
>
> **Dispositif** : synthèse des mesures A8.3a/b/c, aucun nouveau run ; données
> [`a83b-decision.json`](a83b-decision.json).

## Les chiffres qui décident

| régime | lot 1 | lot 2 | lot 4 |
|---|---:|---:|---:|
| f32 | **61,9920** | **60,8135** | **60,8135** |
| 1 % | **58,3200** | **62,7357** | **62,7357** |

- **Lot 1 = pas de lot** : les chiffres redonnent le mode 0.
- **Lot ≥ 2** : identiques ; la taille de lot ne porte pas l’effet.
- **Ctx 64/256/512** : 24 exécutions, aucune ligne ne bouge — le cache n’est pas la cause.
- Le signe **bascule avec le chemin** : f32 lotte mieux, 1 % lotte moins bien.

## Pourquoi le défaut est refusé

- **18 portes PPL épinglées**, mais seulement **3** ont un régime 1 % dual (flux, pont, coupe).
- Un défaut déplacerait les 15 autres ; ce serait une régression silencieuse.
- La cause est **le chemin `forward_
… [2295 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/rapport-coordination-* reports/pensee-coordination-* 2>/dev/null; echo '---'; ls -la \"$HOME/IA/modeles/\" 2>/dev/null | head; echo '---'; ls -la models/ 2>/dev/null", "description": "List coordination reports and model dirs"}`

  ```
reports/rapport-coordination-n2.json
reports/rapport-coordination-n2.md
reports/rapport-coordination-r.json
reports/rapport-coordination-r.md
reports/rapport-coordination-s.json
reports/rapport-coordination-s.md
---
total 18121784
drwxr-xr-x.  3 stephane stephane        4096 12 oct 15:50 .
drwxr-xr-x  14 stephane stephane        4096 21 oct 16:30 ..
drwxr-xr-x.  4 stephane stephane        4096 12 oct 16:04 ollama
-rw-r--r--.  1 stephane stephane 18556686752  3 oct 13:17 qwen3-30b-a3b-Q4_K_M.gguf
---
total 863324
drwxr-xr-x. 1 stephane stephane       100  3 nov 09:12 .
drwxr-xr-x. 1 stephane stephane       686  6 nov 09:52 ..
-rw-r--r--. 1 stephane stephane 352972352 25 sep 17:13 Qwen2.5-0.5B-Q4_0.gguf
-rw-r--r--. 1 stephane stephane 531068480 25 sep 16:52 Qwen2.5-0.5B-Q8_0.gguf
drwxr-xr-x. 1 stephane stephane       138 15 oct 09:02 vision
  ```

- **bash** `{"command": "cat reports/rapport-coordination-n2.json; echo '===='; sed -n '1,180p' reports/rapport-coordination-n2.md", "description": "Read N2 coordination report/JSON"}`

  ```
{
  "date": "2026-11-13",
  "head": "ced21933",
  "ligne": "N2",
  "objet": "coordination du mètre eval_n2_propre.py pour les checkpoints RoPE",
  "fiche": "reports/rapport-coordination-n2.md",
  "verdict": "eval_n2_propre.py lit les checkpoints RoPE comme des positions absolues et rend 8,0225 sur propre512-8k à 128 octets, contre 2,9726 à 128 et 2,7856 à 1024 au mètre RoPE. --rope est nécessaire mais non suffisant : le checkpoint de la porte a été entraîné avec le canal, et --rope seul rend 40,0658. Le correctif validé est --rope --canal-dir.",
  "aucune_modification_n2": [
    "tools/native_model.py",
    "tools/entrainer_native.py",
    "work/"
  ],
  "bug": {
    "fichier": "tools/eval_n2_propre.py",
    "symptome": "val 8,0225 au lieu de 2,9726 à 128 et 2,7856 à 1024 sur work/n2ac/propre512-8k.pt",
    "causes": [
      {
        "rang": 1,
        "nom": "architecture",
        "detail": "charge() construit NativeModel (table de positions apprise absolue) au lieu de NativeModelRoPE ; les checkpoints N2 depuis le 02/11 sont des NativeModelRoPE, avec les mêmes noms de tenseurs et self.pos inutilisé.",
        "silence": "load_state_dict(strict=False) : 127 clés, 0 manquante, 0 
… [19285 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' reports/rapport-c9-echange-experts.md 2>/dev/null; echo '===='; ls reports/ | grep -i \"echange\\|expert\\|chargement\\|a62\\|moe\"", "description": "Read C9 expert exchange report"}`

  ```
# C9 sur un modèle routé : échanger les choix d'experts ne transfère RIEN d'utilisable

> Campagne : **cerveau** · expérience : `--echange experts` (la « variante la plus plausible » du § 6.8)
> Question : la latéralité entre deux instances jumelles ne gagnait rien en échangeant des **états**
> (`rapport-c9-lateralite.md`). La suite nommée était d'échanger des **choix d'experts** sur un
> modèle **routé** : là, les deux instances voient des choses différentes, donc leurs routages
> pourraient porter une information que l'autre n'a pas.
> Verdict : **non — et la mesure a d'abord menti.** Le premier essai donnait **×0,81** (une
> amélioration de 19 % !) en imposant à A le routage de B à la dernière couche. Les contrôles l'ont
> démonté : **tout** routage différent y fait varier la perplexité de ±20 à 50 %, **le signe dépend
> du texte** (A : ×0,81 · A2 : ×1,46 · B en sens inverse : ×1,26), et l'ordre « le routage réel fait
> moins de mal que l'aléatoire » ne tient que **2 fois sur 3** (le sens inverse l'inverse : aléatoire
> ×0,94 contre réel ×1,26). Il n'y a **pas** de gain latéral.
> Date réelle : **2026-10-13, 12 h 57-13 h 20 HAE** (heure lue sur la machine)
> Protocole : Qwen3-30
… [5765 caractères tronqués]
  ```

- **bash** `{"command": "for f in reports/rapport-{cache-experts-vram,decoupage-moe,mla-experts,morcellement-experts,prefill-par-experts,reutilisation-experts,routage-experts,chargement-paresseux}.md; do echo \"===== $f\"; head -12 \"$f\"; done", "description": "Summaries of expert-related reports"}`

  ```
===== reports/rapport-cache-experts-vram.md
# Rapport — un cache d'experts en VRAM pour Kimi-K3 : mesuré, et pourquoi c'est non

**Question** (venue de Strata, `github.com/architectds/Strata`, via la vidéo
« Local AI Is Now 6x Faster on Your PC ») : garder les experts les plus appelés
dans la VRAM rend-il Kimi-K3 plus rapide ici ?

**Réponse courte : non.** ×1,09 prédit, pour un plafond absolu de ×1,41 — contre
un plafond de ×3,1 pour le chantier du dense, qui est déjà nommé.

## 1. Le plafond, avant toute mesure

Trafic disque d'un jeton de Kimi-K3, sur les postes **déjà mesurés**
===== reports/rapport-decoupage-moe.md
# Rapport — découpage des MoE en clusters, pour notre mode d'opération

**En une ligne** : sur Qwen3-30B-A3B (128 experts, 8 par jeton), regrouper les
experts par **fréquence d'usage** suffit à diviser par ~1,8 la ventilation d'un
jeton (3,08 nœuds au lieu de 5,32 au hasard, à 8 clusters) — et la co-activation,
qui devait faire mieux, donne **exactement la même partition** (accord 1,000). Le
découpage n'a donc pas besoin d'un algorithme de graphes : il a besoin d'un
**ordre**, et d'un format qui le respecte.

## Pourquoi cette question

Notre mode d'opération est év
… [4438 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"qwen3\\|gguf\\|MODEL\\|modele\" tools/porte-echange-experts.sh | head -30; echo '---'; ls -la modeles 2>/dev/null; find . -maxdepth 3 -iname '*qwen3*30b*' -o -maxdepth 3 -iname '*Qwen3-30B*' 2>/dev/null | head", "description": "Check MoE path and porte script"}`

  ```
23:M=${MODELE:-/home/stephane/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf}
24:IDS=${IDS:-$HOME/IA/scratch/prerequis/ids_qwen3_30b_wt2.txt}
28:[ -s "$M" ] || { echo "  ❌ modèle absent : $M (poser MODELE=…)"; exit 2; }
---
  ```

- **bash** `{"command": "grep -rn \"forward_lot\" drave-core/ tools/ --include='*.rs' --include='*.sh' --include='*.py' | head -40", "description": "Locate forward_lot implementations"}`

  ```
drave-core/src/model.rs:2995:    /// États imposés pour un LOT entier (`forward_lot`) : `t × hidden`, aplati.
drave-core/src/model.rs:3863:/// Un seul message pour `--attn-topk` ignoré en mode lot (voir `forward_lot`).
drave-core/src/model.rs:5967:    pub fn forward_lot(&mut self, toks: &[u32], pos0: usize) -> Vec<Vec<f32>> {
drave-core/src/model.rs:5973:        // (Vérifié le 02/10 : `grep -c hc` dans le corps de `forward_lot` = 0.)
drave-core/src/model.rs:6365:(`forward_lot` n'applique que les experts routés) — le lot calculerait un autre modèle. \
drave-core/src/model.rs:6570:    /// `forward_lot`, et non à chaque appel — `flux_lot` est appelé deux fois par
drave-core/src/model.rs:7734:        // perplexité répartie 798,3 au lieu de 18,2. `forward_lot` et
drave-core/src/model.rs:9384:        // Préremplissage par lots : `forward_lot` sur des tranches de `self.lot`
drave-core/src/model.rs:9385:        // jetons. `lot == 1` reprend exactement l'ancienne boucle (forward_lot
drave-core/src/model.rs:9394:                let hs = self.forward_lot(&ids[pos..pos + t], pos);
drave-core/src/main.rs:3907:            // `forward_lot` qui le consomme. L'appeler ici serait une erreur de
drave
… [804 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/porte-echange-experts.sh; echo '---FLUX---'; sed -n '1,100p' tools/porte-flux.sh", "description": "Read expert and flux gates"}`

  ```
#!/bin/bash
# porte-echange-experts.sh — le routage imposé fait-il EXACTEMENT ce qu'il annonce ?
#
# POURQUOI CETTE PORTE. `DRAVE_ROUTAGE_FORCER` (13/10) permet d'imposer à un modèle routé les
# experts qu'une autre instance a choisis — c'est l'expérience C9 « échange d'experts »
# (`reports/rapport-c9-echange-experts.md`). Toute la mesure repose sur **un** invariant :
# **imposer à une instance SON PROPRE routage doit rendre la perplexité de référence, au bit près.**
# S'il est faux, les effets mesurés (±20 %) baignent dans un artefact — et c'est arrivé : la
# première version donnait 37,2013 contre 37,1990, parce que la trace TRIE les experts et que
# l'accumulation flottante change avec l'ordre (`DRAVE_TRACE_EXPERTS_ORDRE=1` corrige ça).
#
# CE QU'ELLE VÉRIFIE (trois conditions, dans cet ordre) :
#   1. **inerte par défaut** : sans variable, la trace ne change RIEN à la perplexité ;
#   2. **exact sur son propre routage** : capturé puis imposé, même perplexité au chiffre près ;
#   3. **vivant sur un autre routage** : avec les experts d'une autre couche, la perplexité CHANGE
#      (sinon la porte ne mesure pas ce qu'elle croit — un mécanisme mort passerait les deux
#      premi
… [7439 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-prefill-par-experts.md; echo '===='; sed -n '1,120p' reports/rapport-decoupage-moe.md", "description": "Read prefill and clustering reports"}`

  ```
# Rapport — le préremplissage par experts : ce que le regroupement rapporte, mesuré

**Date** : bloc 31 · **Modèle** : Qwen3-30B-A3B-Instruct-2507-Q4_K_M (48 couches,
128 experts, 8 par jeton) · **Support** : NVMe (copie dédiée, le modèle d'origine
est sur le disque tournant) · 40 CPU, 16 fils · **Invite** : 192 jetons fixes,
identifiants produits une fois et réutilisés par toutes les configurations.

## Le mécanisme mesuré

`forward_lot` regroupe les jetons du lot par expert : la boucle est
`for e in 0..n_experts`, et chaque expert non vide reçoit **un** `gemm_dense_q4`
sur les `g` jetons qui l'ont choisi. Jeton par jeton, la même matrice est relue
autant de fois qu'elle a d'ayants droit.

## 1. Le temps

`tools/mesure-prefill-lot.sh`, 3 passes par point, médiane des 3 :

| lot | prompt_s | tok/s | CPU % | mur_s | gain |
|---|---|---|---|---|---|
| 1 | 33,23 | 5,77 | 995 | 60,5 | 1,00× |
| 2 | 24,51 | 7,83 | 889 | 51,1 | 1,36× |
| 4 | 23,29 | 8,27 | 864 | 50,3 | 1,43× |
| 8 | 23,17 | 8,27 | 854 | 50,6 | 1,43× |
| 16 | 22,45 | 8,53 | 851 | 49,3 | 1,48× |
| 32 | 21,91 | 8,77 | 839 | 48,9 | 1,52× |
| 64 | 21,27 | 9,03 | 831 | 48,2 | 1,56× |
| 192 | 21,00 | 9,20 | 827 | 47,8 | **1,58×
… [10401 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -i \"a83b\\|a833\\|lot\" | sort; echo '---'; grep -rn \"A8.3b2\\|b2\" reports/rapport-a83b*.md reports/*a83b*.json 2>/dev/null | head -40", "description": "Find A8.3b2 artifacts"}`

  ```
a26-lot-disque.json
a83b-decision.json
a83b-lot.json
a83b-regimes.json
a83c-lot.json
a83d-lot-threads.json
corpus-wiki-fr-texte-pilote-contamination.json
corpus-wiki-fr-texte-pilote.json
r03-pilote-modele.json
r44-ocr-pilote.json
rapport-a26-lot-disque.md
rapport-a83b-decision.md
rapport-a83b-lot.md
rapport-a83b-regimes.md
rapport-a83c-lot.md
rapport-a83d-lot-threads.md
rapport-mode4-lot-listes.md
rapport-prefill-par-lots.md
rapport-r44-ocr-pilote.md
---
reports/rapport-a83b-decision.md:52:Prochain : A8.3b2 (instrumentation `forward_lot`) ou B11.10.
reports/a83b-decision.json:42:  "A8.3b2 instrumentation forward_lot",
  ```

- **bash** `{"command": "sed -n '5940,6070p' drave-core/src/model.rs", "description": "Read forward_lot code"}`

  ```
for h in 0..n_head {
            let t = &mut v[h * head_dim..(h + 1) * head_dim];
            for i in 0..half {
                let freq = 1.0 / base.powf(2.0 * i as f32 / head_dim as f32);
                let (s, c) = (pos as f32 * freq).sin_cos();
                let a = t[i];
                let b = t[i + half];
                // rotation d'angle −θ : la matrice inverse de `rope`.
                t[i] = a * c + b * s;
                t[i + half] = b * c - a * s;
            }
        }
    }

    /// **Préremplissage par lots** : `t` jetons d'un coup, aux positions
    /// `pos0..pos0+t`.
    ///
    /// Toute la différence avec `forward` est dans les projections : elles
    /// passent d'un produit matrice-vecteur par jeton à un produit
    /// matrice-matrice pour le lot, donc chaque ligne de poids n'est lue qu'une
    /// fois au lieu de `t` fois (mesuré au noyau : ×2,4 à 16 jetons sur une
    /// matrice 4864 × 896).
    ///
    /// L'attention reste par jeton (elle est causale : le jeton i doit voir le
    /// cache écrit par les jetons < i), mais elle réutilise les Q, K, V calculés
    /// en lot. Les modèles à experts retombent sur le chemin jeton par jeton :
    /// l
… [5899 caractères tronqués]
  ```

- **bash** `{"command": "git status --porcelain | head -40; echo '---'; git rev-parse --short HEAD; echo '---'; nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv 2>&1 | head; echo '---'; free -g | head -3; echo '---'; stat -c '%n %s %y' \"$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf\" 2>&1", "desc … [51 caractères tronqués]`

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
… [886 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"gemm_dense_q4\\|quantif\\|xi\\[\\|sx\\[\\|MoE\\|experts\\|n_expert\" drave-core/src/model.rs | sed -n '1,120p'", "description": "Locate batch quantization and MoE code"}`

  ```
6://! moteur d'événements (`Pool`). Les activations sont quantifiées en int8 à la
26:/// Convention de routage des experts — quatre familles, et une seule
30:    /// `softmax` sur TOUS les logits, top-k, renormalisation. Qwen3-MoE, et le
109:    // (`res_mix`, `PetitesK3`), MoE latent (`MoeK3`), SiTU (`situ`), et la
115:    // K3 est un instrument de vérification qui déquantifie les experts en f32
116:    // (une couche MoE = 1 366 ms/jeton, et 93 couches en f32 demanderaient
124:déquantifie les experts en f32 — il sert à VÉRIFIER, pas encore à faire tourner le modèle");
243:(+0,009 / +0,372 / +0,611 puis +4,070 nat à la position 3 — voir reports/rapport-mla-experts.md §7).");
264:    // Modèle à experts dont les tenseurs d'experts sont absents : ce n'est pas
266:    // Sauf en mode CLUSTERS : les experts y sont préfixés (`cl0/blk.0.…`), donc
270:    if !clusters && cfg.n_expert > 0 && g.tensor("blk.0.ffn_gate_exps.weight").is_none()
274:            "le modèle déclare {} experts mais aucun tenseur d'experts n'est lisible \
276:incomplet", cfg.n_expert));
307:    pub n_expert: usize,
308:    pub n_expert_used: usize,
318:/// Lit la convention de routage des experts — **une seule foi
… [8562 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"LOT=\" tools/*.sh | head -40; echo '---'; grep -n \"lot\" drave-core/src/main.rs | grep -i \"arg\\|lot:\" | head -30", "description": "Find LOT commands and CLI option"}`

  ```
---
1396:    lot: usize,
3876:/// contrôle : jusqu'à ~15 To demandés au noyau. 256 Mo couvrent largement un lot
3909:            ChargeFlux::Lot(_) => panic!("un lot d'états n'est pas un vecteur dense"),
4739:                    let mut recu_lot = f.charge.plat().to_vec();
4741:                    // `largeur_etat`, pas la longueur du lot entier.
4743:                        for q in recu_lot.chunks_mut(largeur_etat) {
  ```

- **bash** `{"command": "sed -n '1,160p' reports/rapport-a83b-lot.md; echo '===='; cat reports/a83b-lot.json", "description": "Read A8.3b lot report/JSON"}`

  ```
# A8.3b.1 — le signe du mélange vient du **chemin lot**, pas de la taille de lot

> **Ligne de roadmap** : A8.3b · **Date** : 2026-10-29 · **Verdict** : ✅ **le basculement est
> binaire** — `--lot 1` (pas de lot) et `--lot ≥ 2` sont deux régimes ; à l’intérieur de `≥ 2`, la
> taille ne change rien à quatre décimales. Le signe du mélange 1 % bascule avec ce chemin.
>
> **Dispositif** : `drave --ppl-reparti`, Qwen2.5-0.5B Q8_0, 12 couches locales, 24 jetons,
> ctx 64 ; cinq tailles de lot × deux régimes ; données [`a83b-lot.json`](a83b-lot.json).

## Ce qui est mesuré

| lot | f32 | mélange 1 % |
|---:|---:|---:|
| **1** | **61,9920** | **58,3200** |
| 2 | **60,8135** | **62,7357** |
| 4 | **60,8135** | **62,7357** |
| 8 | **60,8135** | **62,7357** |
| 16 | **60,8135** | **62,7357** |

- **Lot 1 = pas de lot** : les valeurs sont exactement celles du mode 0 de `porte-flux`.
- **Lot ≥ 2** : identiques à quatre décimales dans chaque régime ; la taille de lot ne porte pas
  l’effet.
- En f32, lotter **améliore** (61,9920 → 60,8135, −1,9 %) ; sous la règle 1 %, lotter
  **dégrade** (58,3200 → 62,7357, +7,6 %). Le signe **bascule avec le chemin**, pas avec la taille.

## Le contrôle négati
… [2097 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"LOT\" tools/porte-*.sh | head -60; echo '---'; grep -rn '\"--lot\"\\|lot.*value\\|--lot' drave-core/src/main.rs | head -30", "description": "Find LOT env usage and CLI"}`

  ```
tools/porte-bus-socket.sh:183:echo "=== 6. le bus du PILOTE : neutre par socket, inerte AU BIT PRÈS ==="
tools/porte-bus-socket.sh:206:echo "=== 7. le bus du PILOTE branché : une ligne non neutre change le résultat ==="
tools/porte-flux.sh:90:    # `timeout` sur le PILOTE aussi : une régression du cadriciel qui bloque le
tools/porte-flux.sh:149:tester "mode 3 — lot dense f32"      "0"      "60.8135" --lot "${LOT:-4}"
tools/porte-flux.sh:150:tester "mode 4 — lot en listes"      "1e-2"   "60.8135" --lot "${LOT:-4}" --flux-blocs
tools/porte-gain.sh:218:#   · si le PILOTE n'appliquait pas la fenêtre (le défaut du round 28, où deux nombres égaux
tools/porte-topologie.sh:2:# porte-topologie.sh — la porte de la capacité C1 : la topologie PILOTE le découpage.
tools/porte-topologie.sh:22:# Ce qu'elle vérifie — « la topologie PILOTE le découpage, à chiffre ÉGAL » — ne dépend pas du
---
1088:    // `--lot N > 1` n'est PAS une simple affaire de vitesse : le chemin par lots
1597:            "--lot" => { o.lot = suivant(i).parse().unwrap(); 2 }
5286:    // `--lot T` : préremplissage par LOTS sur le fil. La référence locale est
5452:mode de lot, le 4) : le lot part en f32 dense. À --lot 1, le mod
… [180 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"DRAVE_PERTE_MAX\\|lot\" tools/porte-flux.sh | tail -40; echo '---'; grep -n \"DRAVE_PERTE_MAX\\|lot\" tools/porte-pont.sh | tail -30; echo '---'; grep -n \"DRAVE_PERTE_MAX\\|lot\" tools/porte-coupe.sh | tail -30", "description": "Check lot handling in gates"}`

  ```
15:# Les modes 0 (f32 dense), 1 et 3 (lot dense) sont EXACTS : écart attendu 0,00e0.
20:#   THREADS=N (défaut 8) : nombre de threads ; A8.3d a montré que l'écart de lot
21:#   survit à 1 thread — ce n'est pas le pool, c'est le noyau par lots.
74:tester() {   # nom, plafond d'écart, référence PPL, arguments du pilote
78:    if [ "${DRAVE_PERTE_MAX:-}" = "1" ]; then
122:    if [ "$nom" = "mode 4 — lot en listes" ] && [ -n "$ecart2" ]; then
144:# 60,8135 (le lot dense change la référence locale). La PPL à deux nœuds des modes
148:tester "mode 2 — listes par blocs"   "6e-2"   "61.9920" --flux-blocs --lot 1
149:tester "mode 3 — lot dense f32"      "0"      "60.8135" --lot "${LOT:-4}"
150:tester "mode 4 — lot en listes"      "1e-2"   "60.8135" --lot "${LOT:-4}" --flux-blocs
---
10:#   1. le pont n'était appliqué QUE du pilote vers le nœud ; le nœud renvoyait tout
37:# Le nœud prend le MÊME `--pont-k` que le pilote : c'est la seule façon d'avoir un
40:pilote() {
50:A=$(pilote --flux); REF=$(ppl "$A"); OD=$(aller "$A")
53:B=$(pilote --flux --pont-k 0); Z=$(ppl "$B")
56:C=$(pilote --flux --pont-k 4096); G=$(ppl "$C")
63:BL0=$(pilote --flux-blocs); REFB=$(ppl "$BL0")
66:BL1=$(pilote --flux-b
… [647 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"xi\\b\\|sx\\b\\|xi\\[\\|sx\\[\" drave-core/src/model.rs | sed -n '1,120p'", "description": "Find quantization variables in model"}`

  ```
5164:        let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
5187:            let y = pool.matvec_dense_q4(q, &xd, sx);
5215:            if let Some(y) = machine.proj(mg, &xd, sx) {
5231:            let y = pool.matvec_dense_i8(d, &xd, sx);
5273:                let mut y = acc[o] as f32 * (sx * m.scale[o]);
5296:        let Some((sv, sx)) = quant(hn, tk4, scratch) else { return false };
5299:        let Some(yg) = machine.proj_mxfp4(mg, &xd, sx) else { return false };
5304:        let Some(yu) = machine.proj_mxfp4(mu, &xd, sx) else { return false };
5348:            let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
5353:            for (&i, &v) in sv.idx.iter().zip(sv.val.iter()) { xd[i as usize] = v as f32 * sx; }
5372:        let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
5378:        let y = pool.matvec_dense_q4(m, &xd, sx);
6049:        let mut xi = vec![0i32; t * h];
6050:        let mut sx = vec![0f32; t];
6110:            quantifier(&hn, &mut xi, &mut sx, self.act_levels, self.act_thresh);
6112:                           0, l, t, &mut xi, &mut sx, h);

… [3299 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '6200,6400p' drave-core/src/model.rs", "description": "Read MoE portion of forward_lot"}`

  ```
Self::rope(qi, nh, hd, pos, self.cfg.rope_base, self.cfg.n_rot);
                        Self::rope(ki, nkv, hd, pos, self.cfg.rope_base, self.cfg.n_rot);
                    }
                }
                qgpu[i * nq..(i + 1) * nq].copy_from_slice(qi);
                {
                    let kvc = &mut self.kv[l];
                    for hh in 0..nkv {
                        kvc.ecrire(hh, pos, &ki[hh * hd..(hh + 1) * hd],
                                          &vi[hh * hd..(hh + 1) * hd]);
                    }
                }
                // Miroir VRAM, une position à la fois : l'attention du jeton `i`
                // a besoin des clés de TOUT le lot déjà écrit, donc la copie doit
                // suivre l'écriture. Quelques centaines d'octets par couche et par
                // jeton — le contraire (copier le lot à la fin) donnerait au noyau
                // un cache amputé de son propre lot.
                KvCache::miroir_gpu(self.kv_gpu.as_deref_mut(), l, &self.kv[l], pos, 1);
                let fen = if self.attn_window == 0 { 0 }
                          else if self.swa_pattern <= 1 { self.attn_window }
                          else if l % self
… [10814 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '6400,6540p' drave-core/src/model.rs", "description": "Read remaining MoE batch code"}`

  ```
let mut yq = vec![0f32; t * nff];
                let mut col = vec![0f32; nff];
                let mut colu = vec![0f32; nff];
                let mut ga = vec![0i16; t * nff];
                let mut s32a: Vec<Vec<i32>> = Vec::with_capacity(t);
                let mut sxa: Vec<f32> = Vec::with_capacity(t);
                // `yd` est hissé HORS de la boucle des experts : il était
                // alloué une fois par expert non vide (jusqu'à ~50 allocations
                // par couche et par lot). Le GEMM écrit toutes ses lignes et
                // toutes ses colonnes, donc la réutiliser ne change aucun
                // résultat — seule l'allocation disparaît.
                let mut yd = vec![0f32; t * nff.max(h)];
                // Les paires du chemin par LOTS : `gemm_dense_q4` ne tient pas
                // de compteur (le pool ne connaît pas le modèle), et le chemin
                // jeton, lui, passe par `matvec4_ou_iq` qui en tient un. Sans
                // cette ligne, « paires experts » tombait à ~1 % de sa valeur
                // dès `--lot 2` : le compteur ne voyait plus que les jetons de
                // génération, et un chiffre qui chute de 97 % san
… [6927 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"fn quantifier\\|fn quant_scratch\\|fn gemm_dense_q4\\|fn gemm_dense_i8\\|fn matvec4_ou_iq\\|fn router\" drave-core/src/model.rs drave-core/src/*.rs | head -20", "description": "Locate quantization and GEMM functions"}`

  ```
drave-core/src/model.rs:490:fn router(cfg: &Cfg, moe: &Moe, x: &[f32], tid: u32, k: usize, couche: usize, cle: u64)
drave-core/src/model.rs:5092:    fn quant_scratch(x: &[f32], levels: f32, thresh: f32, topk: usize, renorm: bool,
drave-core/src/model.rs:5339:    fn matvec4_ou_iq(pool: &mut Pool, vue: &Vue4, loc: usize, x: &[f32], out: &mut [f32],
drave-core/src/engine.rs:708:    pub fn gemm_dense_i8(&mut self, d: &DenseQ8, x: &[i32], t: usize, sx: &[f32], out: &mut [f32]) {
drave-core/src/engine.rs:726:    pub fn gemm_dense_q4(&mut self, d: &crate::list::DenseQ4, x16: &[i16], t: usize,
drave-core/src/model.rs:490:fn router(cfg: &Cfg, moe: &Moe, x: &[f32], tid: u32, k: usize, couche: usize, cle: u64)
drave-core/src/model.rs:5092:    fn quant_scratch(x: &[f32], levels: f32, thresh: f32, topk: usize, renorm: bool,
drave-core/src/model.rs:5339:    fn matvec4_ou_iq(pool: &mut Pool, vue: &Vue4, loc: usize, x: &[f32], out: &mut [f32],
  ```

- **bash** `{"command": "grep -n \"quantifier\\|quant_scratch\" drave-core/src/model.rs | head -30", "description": "Find quantifier definitions and calls"}`

  ```
1761:/// Occupation d'un tenseur **Q4_0** lu en place, **sans le déquantifier** : dans un bloc ggml de
2684:    /// tels quels (chemin exact, sans déquantifier-requantifier).
3648:    /// les quantifier » : c'est peut-être là que se joue son +0,8 % de
5092:    fn quant_scratch(x: &[f32], levels: f32, thresh: f32, topk: usize, renorm: bool,
5154:        // quantifier le reste fait dépendre l'ÉCHELLE d'activation de valeurs
5164:        let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
5294:            Self::quant_scratch(x, levels, thresh, topk, renorm, scratch)
5348:            let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
5372:        let Some((sv, sx)) = Self::quant_scratch(x, levels, thresh, topk, renorm, scratch) else {
6085:        // Quantification d'un lot : mêmes règles que `quant_scratch`.
6086:        let quantifier = |src: &[f32], dst: &mut [i32], ech: &mut [f32],
6110:            quantifier(&hn, &mut xi, &mut sx, self.act_levels, self.act_thresh);
6328:                quantifier(&att, &mut ai[..t * n_in_wo], &mut sa, self.act_levels, self.act_thresh);
6352:            quantifier(&hn, &mu
… [815 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '5080,5145p' drave-core/src/model.rs; echo '---BATCH---'; sed -n '6075,6115p' drave-core/src/model.rs; echo '---ENGINE---'; sed -n '690,780p' drave-core/src/engine.rs", "description": "Read quantization and GEMM code"}`

  ```
// Briques de calcul
    // ----------------------------------------------------------------------- //

    /// Quantifie un vecteur (une échelle pour tout le vecteur).
    #[inline]
    /// Parcimonie effective d'une projection : la valeur par projection prime,
    /// sinon on retombe sur le réglage global.
    #[inline]
    pub fn topk_de(&self, proj: usize) -> usize {
        if self.act_topk_proj[proj] > 0 { self.act_topk_proj[proj] } else { self.act_topk }
    }

    fn quant_scratch(x: &[f32], levels: f32, thresh: f32, topk: usize, renorm: bool,
                     scratch: &mut Vec<f32>) -> Option<(SparseVec, f32)> {
        let mut mx = 0f32;
        for &v in x { let a = v.abs(); if a > mx { mx = a; } }
        if mx == 0.0 { return None; }
        let s = mx / levels;
        let inv = 1.0 / s;
        // seuil absolu correspondant à la fraction demandée du maximum
        let seuil = (thresh * levels) as i32;
        let mut sv = SparseVec { idx: Vec::with_capacity(x.len()), val: Vec::with_capacity(x.len()) };
        if topk > 0 {
            // k-WTA : ne garder que les k plus grandes magnitudes (inhibition
            // latérale). `topk` est une FRACTION de la dime
… [8692 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '7820,7940p' drave-core/src/model.rs", "description": "Read token-path MoE code"}`

  ```
}
            }
            // Fenêtre EFFECTIVE de cette couche : le motif déclaré (gpt-oss :
            // une couche sur deux en attention complète) prime sur le réglage
            // global. Lue en champs directs : `self` est déjà déstructuré.
            let fen = if self.attn_window == 0 { 0 }
                      else if self.swa_pattern <= 1 { self.attn_window }
                      else if l % self.swa_pattern < self.swa_pattern - 1 { self.attn_window }
                      else { 0 };
            // ---- hyper-connexions : l'entrée de l'attention n'est pas l'état,
            // c'est le MÉLANGE de ses `hc` copies (`pre`), et la sortie sera
            // re-router par `comb` au lieu d'être additionnée.
            let hc_l = self.hc.as_ref().map(|v| &v[l]);
            let mut hc_attn: Option<HcSortie> = None;
            let mut xin = vec![0f32; h];
            match hc_l {
                Some((ha, _)) => {
                    let s = ha.sortie(&x);
                    // **Les 24 poids de connexion du raccord** (4 `pre` + 4 `post`
                    // + 16 `comb`) : c'est le flux de P1 — ils étaient calculés
                    // puis JETÉS, donc muets. La por
… [6442 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"act_levels\\|act_topk\\|act_thresh\\|act_renorm\" drave-core/src/model.rs | head -40; echo '---'; grep -rn \"act_levels\" drave-core/src/main.rs | head -20", "description": "Find activation quantization defaults"}`

  ```
2850:    pub act_levels: f32,
2852:    /// `act_thresh` écarte les activations sous cette fraction du maximum du
2853:    /// vecteur ; `act_topk` ne garde que les k plus grandes. Les deux imitent
2857:    pub act_thresh: f32,
2858:    pub act_topk: usize,
2862:    pub act_renorm: bool,
2864:    /// 5 = up, 6 = down. La valeur 0 signifie « utiliser act_topk ».
2865:    pub act_topk_proj: [usize; 7],
5018:            ctx, events: 0, paires: [0; 3], paires_flux: 0, act_levels: 127.0,
5019:            act_thresh: 0.0, act_topk: 0, act_renorm: false,
5020:            act_topk_proj: [0; 7], attn_topk: 0, attn_events: 0, qk_topk: 0,
5089:        if self.act_topk_proj[proj] > 0 { self.act_topk_proj[proj] } else { self.act_topk }
6110:            quantifier(&hn, &mut xi, &mut sx, self.act_levels, self.act_thresh);
6160:                                     &mut self.events, &mut self.paires[0], self.act_levels,
6161:                                     self.act_thresh, 0,
6162:                                     self.act_renorm, &mut scratch, self.seuil_push);
6328:                quantifier(&att, &mut ai[..t * n_in_wo], &mut sa, self.act_levels, self.act_thresh);
6352:            quantifi
… [2799 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"act_topk\\|act_thresh\\|act_levels\" drave-core/src/main.rs | head -40; echo '---'; grep -n \"struct Opt\\|act_\" drave-core/src/main.rs | head -50", "description": "Find CLI activation options"}`

  ```
1061:             mdl.act_levels, mdl.act_thresh, mdl.act_topk, mdl.act_renorm);
1063:             mdl.attn_topk, mdl.qk_topk, mdl.moe_topk, mdl.act_topk_proj);
1343:    act_thresh: f32, act_topk: usize, act_renorm: bool, topk_proj: [usize; 7],
1611:            "--act-thresh" => { o.act_thresh = suivant(i).parse().unwrap(); 2 }
1612:            "--act-topk" => { o.act_topk = suivant(i).parse().unwrap(); 2 }
1755:        act_thresh, act_topk, act_renorm, topk_proj, moe_topk, patch: patch_file,
1800:    mdl.act_thresh = act_thresh;
1801:    mdl.act_topk = act_topk;
1804:    mdl.act_topk_proj = topk_proj;
1846:    if act_topk > 0 || act_thresh > 0.0 {
1848:                 act_topk as f32 / 10.0,
1849:                 if act_thresh > 0.0 { format!(", seuil {:.1} %", act_thresh * 100.0) } else { String::new() });
3720:    mdl.act_levels = niveaux_activation(abits);
3726:    mdl.act_thresh = opt.act_thresh;
3727:    mdl.act_topk = opt.act_topk;
3732:    mdl.act_topk_proj = opt.topk_proj;
3829:        for (i, v) in m.act_topk_proj.iter().enumerate() { topk_proj[i] = *v as u32; }
3830:        Act { levels: m.act_levels, thresh: m.act_thresh, topk: m.act_topk as u32,
3838:        m.act_lev
… [3091 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"DRAVE_PERTE_MAX\\|perte_max\" drave-core/src/*.rs | head -40", "description": "Find 1% loss rule implementation"}`

  ```
drave-core/src/model.rs:4709:        // premières couches, +0,03 % sur les dernières (A5.3) — le budget `DRAVE_PERTE_MAX`
drave-core/src/model.rs:4711:        // La règle s'active **explicitement** (`DRAVE_PERTE_MAX`) : un changement de défaut
drave-core/src/model.rs:4715:            && std::env::var("DRAVE_PERTE_MAX").is_ok() {
drave-core/src/model.rs:4716:            let budget_pct: f64 = std::env::var("DRAVE_PERTE_MAX").ok()
drave-core/src/placement.rs:133:/// ici on répond à « où ça tient **sans payer plus que `perte_max`** ». Un 4 bits
drave-core/src/placement.rs:141:    perte_max: f64,
drave-core/src/placement.rs:145:        if p.perte_ppl > perte_max {
  ```

- **bash** `{"command": "sed -n '1,130p' tools/porte-coupe.sh; echo '---'; sed -n '1,100p' tools/porte-pont.sh", "description": "Read coupe and pont gates"}`

  ```
#!/bin/bash
# porte-coupe.sh — OÙ COUPER ? Le point de coupe est-il neutre, et à quel prix ?
#
# LA QUESTION PRATIQUE. Le découpage en régions (C1) et le pont (C9) avaient chacun
# été mesurés à UN endroit : 12 couches locales, 12 distantes. Rien ne disait que
# 12/12 soit le bon endroit. Cette porte répond à deux questions distinctes, et les
# sépare parce qu'elles n'ont pas la même réponse :
#
#   1. **le point de coupe change-t-il le RÉSULTAT ?** Avec un lien SANS PERTE (dense
#      f32), la réponse mesurée est NON : huit points de coupe (4, 6, 8, 10, 12, 15,
#      18, 20 couches locales sur 24) donnent tous 113,0068. C'est l'invariant de C1,
#      vérifié sur huit coupes et non sur une seule ;
#   2. **le point de coupe change-t-il ce que le lien COÛTE ?** Avec un lien encodé
#      (listes par blocs), la réponse est OUI, et fortement : les mêmes coupes donnent
#      de 108,87 à 118,53 de perplexité — soit 9 % d'écart — parce que l'erreur de
#      quantification dépend de l'état échangé, qui dépend de la profondeur. Et le coût
#      d'un pont de 448 fibres va de +0,52 % (coupe 18/6) à +17,09 % (coupe 15/9).
#
# Une porte qui ne saurait pas échouer ne vérifierait rien : le
… [10110 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '4680,4765p' drave-core/src/model.rs", "description": "Read DRAVE_PERTE_MAX rule"}`

  ```
if let Ok(spec) = std::env::var("DRAVE_KV_BITS_COUCHES") {
                for morceau in spec.split(',') {
                    let morceau = morceau.trim();
                    if morceau.is_empty() { continue; }
                    let (plage, bits) = match morceau.split_once(':') {
                        Some((p, b)) => (p.trim(), b.trim().parse::<u32>().ok()),
                        None => { println!("[config] KV par couche : « {morceau} » sans ':' — ignoré"); continue; }
                    };
                    let Some(bits) = bits else {
                        println!("[config] KV par couche : bits illisibles dans « {morceau} » — ignoré");
                        continue;
                    };
                    let (deb, fin) = match plage.split_once('-') {
                        Some((d, f)) => (d.trim().parse::<usize>().ok(), f.trim().parse::<usize>().ok()),
                        None => (plage.parse::<usize>().ok(), plage.parse::<usize>().ok()),
                    };
                    let (Some(deb), Some(fin)) = (deb, fin) else {
                        println!("[config] KV par couche : plage illisible dans « {morceau} » — ignoré");
                    
… [4263 caractères tronqués]
  ```

- **bash** `{"command": "ls -la drave-core/target/release/drave 2>/dev/null; ls -la /tmp/campagne24/ids_0.5B-Q8.txt 2>/dev/null; ls -la ~/IA/scratch/prerequis/ids_qwen3_30b_wt2.txt 2>/dev/null; ls data/wikitext2_test.txt 2>/dev/null", "description": "Check binary and token files"}`

  ```
-rwxr-xr-x. 2 stephane stephane 3187480 30 oct 08:39 drave-core/target/release/drave
-rw-r--r--. 1 stephane stephane 394684  4 nov 08:07 /tmp/campagne24/ids_0.5B-Q8.txt
-rw-r--r--. 1 stephane stephane 394684 12 oct 19:56 /home/stephane/IA/scratch/prerequis/ids_qwen3_30b_wt2.txt
data/wikitext2_test.txt
  ```

- **bash** `{"command": "./drave-core/target/release/drave --help 2>&1 | head -60", "description": "Check drave help/options"}`

  ```
thread 'main' (972473) panicked at src/main.rs:689:35:
ouverture du GGUF: Os { code: 2, kind: NotFound, message: "No such file or directory" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
  ```

- **bash** `{"command": "grep -n '\"--ppl\"\\|ppl:' drave-core/src/main.rs | head -20; echo '---'; sed -n '1570,1625p' drave-core/src/main.rs", "description": "Find PPL CLI options"}`

  ```
631:        (opt.ppl, "--ppl"), (opt.infer, "--infer"),
1162:    infer: bool, ppl: bool, plan: bool, tokenize: bool, gpu_banc: bool, k3_essai: bool,
1444:            "--ppl" => { o.ppl = true; o.ids_file = Some(suivant(i).clone()); 2 }
5695:    println!("  deux nœuds        : perplexité {ppl:.4}  ({:.1} s)", t1.elapsed().as_secs_f64());
---
            // RÉCURRENCE (C2) : la région consomme sa PROPRE sortie du pas précédent, avec un
            // poids déclaré : x0(t) += alpha · h(t−1). C'est la boucle que le plan décrit
            // (« une région peut consommer sa propre sortie du pas précédent ») et que le
            // validateur de topologie refuse encore dans un graphe (cycle) — ici elle est
            // explicite, bornée, et mesurable dans la région frontière.
            "--recurrence" => { o.recurrence = suivant(i).parse().unwrap(); 2 }
            // TAMPON explicite : les K derniers valeurs sont injectées sur les canaux suivants.
            // C'est la STRUCTURE dont la fiche `rapport-c8-peripherie.md` § 2 ter montre l'absence :
            // une récurrence qui fuit ne retient pas (R² 0,104), un tampon retient exactement.
            "--entree-memoire" => { o.ent
… [3557 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for lot in 1 4; do for reg in f32 perte1; do echo \"=== lot=$lot reg=$reg\"; if [ \"$reg\" = perte1 ]; then env DRAVE_PERTE_MAX=1 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/campagne24/ids_0.5B-Q8.txt - … [415 caractères tronqués]`

  ```
=== lot=1 reg=f32
[config] cache KV : 32 bits, 0.00 Go pour 64 jetons
      23 tokens notés — perplexité cumulée 48.580  (23.9 tok/s)
=== perplexité 48.5799 sur 23 tokens (0 événements, 1.0 s) ===
=== lot=1 reg=perte1
[config] KV par la règle place+perte : budget 1.0 % → 12 couche(s) en int8 (l'int8 coûte +2,28 % sur les premières, +0,03 % sur les dernières)
[config] cache KV : 32 bits, 0.00 Go pour 64 jetons
      23 tokens notés — perplexité cumulée 48.594  (22.5 tok/s)
=== perplexité 48.5937 sur 23 tokens (0 événements, 1.0 s) ===
=== lot=4 reg=f32
[config] cache KV : 32 bits, 0.00 Go pour 64 jetons
      23 tokens notés — perplexité cumulée 48.567  (28.5 tok/s)
=== perplexité 48.5666 sur 23 tokens (0 événements, 0.8 s) ===
=== lot=4 reg=perte1
[config] KV par la règle place+perte : budget 1.0 % → 12 couche(s) en int8 (l'int8 coûte +2,28 % sur les premières, +0,03 % sur les dernières)
[config] cache KV : 32 bits, 0.00 Go pour 64 jetons
      23 tokens notés — perplexité cumulée 48.670  (28.2 tok/s)
=== perplexité 48.6700 sur 23 tokens (0 événements, 0.8 s) ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for kv in 8 4; do for lot in 1 4; do echo \"=== KV=$kv lot=$lot\"; env DRAVE_KV_BITS=$kv ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/campagne24/ids_0.5B-Q8.txt --ctx 64 --limit 24 --threads 8 --lot $lot … [168 caractères tronqués]`

  ```
=== KV=8 lot=1
[config] cache KV : 8 bits, 0.00 Go pour 64 jetons
=== perplexité 33.1059 sur 23 tokens (0 événements, 1.0 s) ===
=== KV=8 lot=4
[config] cache KV : 8 bits, 0.00 Go pour 64 jetons
=== perplexité 33.2277 sur 23 tokens (0 événements, 0.8 s) ===
=== KV=4 lot=1
[config] cache KV : 4 bits, 0.00 Go pour 64 jetons
=== perplexité 70.1813 sur 23 tokens (172995 événements, 1.0 s) ===
=== KV=4 lot=4
[config] cache KV : 4 bits, 0.00 Go pour 64 jetons
=== perplexité 66.2076 sur 23 tokens (0 événements, 0.8 s) ===
  ```

- **bash** `{"command": "sed -n '1,100p' tools/mesure-prefill-lot.sh; echo '===='; sed -n '1,90p' tools/analyse_union_experts.py; echo '===='; sed -n '1,80p' tools/clusters_moe.py", "description": "Read expert measurement tools usage"}`

  ```
#!/usr/bin/env bash
# mesure-prefill-lot.sh — ce que le REGROUPEMENT PAR EXPERT fait gagner au
# préremplissage, mesuré, pas supposé.
#
# En préremplissage par lots (`--lot N`, `forward_lot`), les jetons du lot qui
# ont choisi le même expert partagent UNE lecture de sa matrice : un seul
# `gemm_dense_q4` par expert non vide. Jeton par jeton, la même matrice est
# relue autant de fois qu'elle a d'ayants droit.
#
# Le script donne, pour chaque taille de lot :
#   - prompt_s  : le temps de préremplissage rendu par le moteur lui-même ;
#   - tok/s     : le débit qui en découle ;
#   - CPU %     : le taux d'occupation RÉEL (un lot qui parallélise mal se voit
#                 ici avant de se voir dans le temps) ;
#   - mur s     : le temps total du processus, chargement compris — il dit si
#                 le chiffre mesure le calcul ou la lecture du fichier.
#
# Règle : rien d'autre ne tourne pendant la mesure. Deux pools de 16 fils sur
# 40 CPU se disputent les cœurs ET la bande mémoire, et le chiffre obtenu ne
# mesure plus la taille du lot (constaté : ×17 sur un lot 2 mesuré pendant
# qu'un autre `drave` tournait encore).
#
# Usage : tools/mesure-prefill-lot.sh <modele.gguf> <ids-
… [7587 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_backlog.py 2>&1 | tail -30; echo '---'; grep -n \"A6.2\\|A8.3b2\\|A2.6\" docs/pilotage/backlog/dependances.md | head -30", "description": "Run backlog verification and inspect dependencies"}`

  ```
=== GRAPHE DU BACKLOG ===
  fiches 37 · lignes sans fiche 1 · arêtes dures 43 · plafonds 3
  profondeur 5 : R01 → R02 → R03 → R31 → R32 → R51
  frontière (3) : A2.6, N2, N4

✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.
---
63:| **A2.6** | partiel | A2 (acquis) | — | — | [A2.6-ordonnanceur.md](A2.6-ordonnanceur.md) |
68:| **A6.2** | libre | A6 (acquis) | **pas** « aucun MoE local » : le MoE existe (Qwen3-30B-A3B Q4, 18 Go) ; le blocage est la **résidence mono-GPU 16 Go**, relevé le 06/11 | — | [A6.2-moe-local.md](A6.2-moe-local.md) |
162:| **A2.6** | partiel | `A2` mesuré ; `A6.2` est un plafond, pas une arête ; tête **refusée par décision**, `placement.rs` a **8 tests** | experts et placement dans la règle `choisir` |
167:**Ce qui n'y est pas, et pourquoi** : `A3.4`, `A5.4`, `A6.2`, `B1.5` sont bloqués par une
205:| **P2** | `N3`, `B11.10`, `B12.10`, `A2.6`, `A3.2`, `A8.0` | lignes autonomes, utiles, non bloquantes |
208:| **bloqués** | `A3.4`, `A5.4`, `B1.5` | ressource externe nommée : on prend la ligne suivante (`A6.2` est **libre** — voir l'état A du 06/11) |
  ```

- **bash** `{"command": "sed -n '55,80p' docs/pilotage/backlog/dependances.md; echo '---'; sed -n '200,215p' docs/pilotage/backlog/dependances.md; echo '---'; grep -n \"A6.2\\|A8.3b2\\|A8.3b\" docs/pilotage/backlog/index.md docs/pilotage/backlog/dependances.md docs/pilotage/en-cours.md docs/pilotage/chantiers.m … [113 caractères tronqués]`

  ```
table recopiée à la main diverge au premier ajout. « Acquis » = la ligne est mesurée ou close, elle
ne demande aucun travail ; « sans fiche » = une ligne ouverte de la roadmap qui n'a pas encore de
contrat, donc pas de porte ni de contrôle négatif.

### A — le moteur

| item | état | dépend de (dure) | plafond / contrainte | débloque | fiche |
|---|---|---|---|---|---|
| **A2.6** | partiel | A2 (acquis) | — | — | [A2.6-ordonnanceur.md](A2.6-ordonnanceur.md) |
| **A3.2** | mesurée | A3 (acquis) | — | A3.3 | [A3.2-granularite.md](A3.2-granularite.md) |
| **A3.3** | mesurée | A3.2 (dure) | — | — | [A3.3-seuil.md](A3.3-seuil.md) |
| **A3.4** | bloquée | A3 (acquis) | bloqué : le compte et le runtime Colab | — | [A3.4-colab.md](A3.4-colab.md) |
| **A5.4** | bloquée | A5 (acquis) | bloqué : la carte Stratix V | — | [A5.4-fpga.md](A5.4-fpga.md) |
| **A6.2** | libre | A6 (acquis) | **pas** « aucun MoE local » : le MoE existe (Qwen3-30B-A3B Q4, 18 Go) ; le blocage est la **résidence mono-GPU 16 Go**, relevé le 06/11 | — | [A6.2-moe-local.md](A6.2-moe-local.md) |
| **A8.0** | mesurée | A8 (acquis) | — | A8.3 | [A8.0-portes-ppl.md](A8.0-portes-ppl.md) |
| **A8.3** | mesurée | A8.0 (dure) | — 
… [3697 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"A8\\|A6\\|A2.6\\|coordination\" docs/pilotage/en-cours.md | head -50; echo '---'; wc -l docs/pilotage/en-cours.md", "description": "Current state A mentions"}`

  ```
113:| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; A6.2 MoE local | **A2.6** (experts et tête) |
---
140 docs/pilotage/en-cours.md
  ```

- **bash** `{"command": "grep -n \"31,9\\|réutilisation\\|cache\\|VRAM\\|Go\\|%\" reports/rapport-reutilisation-experts.md | head -40; echo '===='; sed -n '1,90p' reports/rapport-reutilisation-experts.md", "description": "Read expert reuse results"}`

  ```
1:# La réutilisation des experts, mesurée
4:> Kimi-K3 lit **24,7 Go d'experts routés** (16 sur 896). Aucun placement ne rend
6:> mesure qui décide si un cache peut servir à quelque chose, et elle manquait.
20:| **réutilisation immédiate** (t−1 → t) | 46,9 % | **47,9 %** | **48,8 %** |
21:| fenêtre de 2 jetons | 54,7 % | 57,1 % | 60,4 % |
22:| fenêtre de 4 | 63,9 % | 68,5 % | 72,9 % |
23:| fenêtre de 8 | 72,8 % | 78,1 % | 82,3 % |
24:| fenêtre de 16 | 78,8 % | 84,5 % | 88,2 % |
25:| sur tout l'historique | 82,7 % | 93,1 % | 93,9 % |
28:les trois textes (46,9 · 47,9 · 48,8 %), donc la dépendance au texte est faible
29:sur cette mesure. Le plafond de réutilisation (93 %) est atteint avec une fenêtre
33:## 2. Ce qu'un cache LRU rend, mesuré
35:| capacité du cache (experts par couche) | part des experts | taux de succès |
37:| 8 | 6 % | 33,7 % |
38:| 16 | 13 % | 58,5 % |
39:| **32** | **25 %** | **74,8 %** |
40:| 64 | 50 % | 82,3 % |
41:| 128 | 100 % | 82,7 % |
43:Le rendement est **très favorable au début** : un quart des experts en cache
44:(32 sur 128) sert **de 75 à 87 % des lectures** selon le texte, et la moitié en
45:sert 92 à 93 %. C'est exactement la forme qu'il
53:courbe de ré
… [5612 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"×1,09\\|plafond\\|VRAM\\|Go\\|verdict\\|Conclusion\\|conclusion\" reports/rapport-cache-experts-vram.md | head -40; echo '===='; sed -n '1,80p' reports/rapport-chargement-paresseux.md", "description": "Read cache VRAM and lazy load results"}`

  ```
1:# Rapport — un cache d'experts en VRAM pour Kimi-K3 : mesuré, et pourquoi c'est non
5:dans la VRAM rend-il Kimi-K3 plus rapide ici ?
7:**Réponse courte : non.** ×1,09 prédit, pour un plafond absolu de ×1,41 — contre
8:un plafond de ×3,1 pour le chantier du dense, qui est déjà nommé.
10:## 1. Le plafond, avant toute mesure
15:| poste | Go/jeton | part |
23:Un cache d'experts ne peut retirer **que** les 25,83 Go routés. Donc :
32:## 2. Ce que la VRAM peut tenir
34:2 × 16 Go = 32 Go. Une matrice d'expert K3 (3 × 3072 × 3584 à 4,25 bits) pèse
39:experts par couche et 34-50 Go de experts **tiennent tous en RAM** ; ici 896 par
40:couche et 1 508 Go au total.
58:## 4. Le verdict
60:Avec 32 Go de VRAM et 28,7 % de succès :
61:`88,09 / (88,09 − 0,287 × 25,83) = 88,09 / 80,68` = **×1,09**.
67:cache de pages garde les 59,6 Go résidents) a un plafond de **×3,1** : 61 Go des
68:88,09 Go d'un jeton.
78:- **Le plafond, lui, ne dépend d'aucune de ces réserves** : 29,3 % du trafic,
85:1. **cache d'experts en VRAM** — mesuré ici, ×1,09 : non ;
====
# Le chargement construisait 2,7 Go de « listes » que personne ne lisait

> Campagne : **machine et moteur** · expérience 01 — le coût du chargement
> 
… [4848 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 900 bash tools/porte-echange-experts.sh 2>&1 | tee /tmp/porte-echange-a.log | tail -30; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run expert exchange gate on local MoE", "timeoutMs": 900000}`

  ```
porte de l'échange d'experts — qwen3-30b-a3b-Q4_K_M.gguf, 16 jetons
  référence (aucune imposition) : 54.5202
  trace : 768 décisions (couche, jeton, experts)
  ✅ son propre routage imposé : 54.5202 — identique à la référence
  ✅ routage étranger (couche +3) : 36074.9497 — différent, donc le mécanisme agit
  PORTE TENUE
EXIT=0
  ```

- **bash** `{"command": "sed -n '1,80p' reports/rapport-a26-bilan.md; echo '===='; cat reports/a26-bilan.json", "description": "Read A2.6 assessment and JSON"}`

  ```
# A2.6 — l'ordonnanceur est partiel : le générique et le KV sont faits, la tête est refusée, les experts bloqués

> **Ligne de roadmap** : A2.6 · **Date** : 2026-10-29 · **Verdict** : ⚠️ **partielle** — la règle
> générique et le KV sont mesurés ; la tête 4 bits est refusée par la perte ; les experts attendent
> **A6.2** (pas de MoE local). A2.6 ne peut pas être « complétée » sans cette brique.
>
> **Dispositif** : bilan des mesures existantes (`placement.rs`, `rapport-placement-kv-8k.md`,
> `rapport-regle-placement-perte.md`, A8.3) ; **pas de nouvelle mesure** ; données
> [`a26-bilan.json`](a26-bilan.json).

## Le bilan

| partie | état | preuve |
|---|---|---|
| `choisir` générique | ✅ fait | `placement.rs`, 4 tests ; `kv_en_vram` appliqué dans `model.rs` |
| KV en VRAM | ✅ mesuré | ×1,93 au préremplissage 8 k, ×5,8 sur l’attention |
| tête 4 bits | ❌ refusée | +10 % de PPL ; `choisir_avec_perte` la refuse à 5 % |
| experts | 🧱 bloqué | **A6.2** — pas de MoE local à router |
| place + perte | 🔬 opt-in | A8.3 : le défaut déplace les portes ; **A8.3a** à venir |

## Le contrôle négatif

- `choisir_avec_perte` refuse la tête 4 bits à un budget de 5 % : la place ne suffit pas, la per
… [1885 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"A6.2\\|A8.3b2\\|A2.6\" docs/pilotage/roadmap.md | head -40; echo '---'; sed -n '140,160p' docs/pilotage/roadmap.md; echo '---'; sed -n '335,360p' docs/pilotage/roadmap.md", "description": "Read roadmap A sections"}`

  ```
30:| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.6 partiel ; A3.2/A3.3 mesurées ; **A8.3c/d expliqués** ; **A2.6/A8.3 : le [lot](../theorie/glossaire/entrees/lot.md) ne divise pas les lectures denses (+27 % calcul, PPL −0,006 %)** | **A2.6** (experts : A6.2 bloqué) ; le lot ≥ 2 assumé |
36:| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67,73 G car., 81,2 Go, **8 Ko 0**) ; **PDF** (1 927 doc., 322 Mo) ; **documents** (3 384 doc., 872 M car., 8 Ko 2,07 %) ; **OCR** (20 livres, 7 381 p, 15,36 M, 8 Ko 0 ; [CEGEP](../theorie/glossaire/entrees/cegep.md) **91 scans uniques**, 60 documents, 1 982 p, 4,41 M car., 8 Ko 0) ; **genres** mesurés | **l'OCR est clos** (limite : 8 scans `.PDF`, 58 p) ; la préparation **R1.1/R1.2** (N2) et **A2.6** (A) |
84:8. **Les bloqués** : A3.4 ([Colab](../theorie/glossaire/entrees/colab-notebook-tunnel.md)), A5.4 ([FPGA](../theorie/glossaire/entrees/fpga.md)) 
… [5559 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '155,175p' docs/pilotage/backlog/dependances.md; echo '---'; sed -n '75,95p' docs/pilotage/backlog/index.md", "description": "Read contradictions context"}`

  ```
**Quatre items** — c'est la file « jamais en attente » réelle. Une ligne **mesurée**, **bloquée**
ou dont une dépendance dure n'est pas levée n'y figure pas ; les lignes `bloquée` (B10.3 par le
négatif de B10.2bis, R44 par l'OCR) en sont exclues par leur statut.

| item | état | pourquoi c'est libre | la prochaine action |
|---|---|---|---|
| **A2.6** | partiel | `A2` mesuré ; `A6.2` est un plafond, pas une arête ; tête **refusée par décision**, `placement.rs` a **8 tests** | experts et placement dans la règle `choisir` |
| **N2** | en cours | `N1` acquis | la **hiérarchie** (état de section, 3 graines) ; porte **< 2,5** |
| **N3** | partiel | `N1` mesuré ; le service composé existe (N3.6) | ce qui reste des opérations natives, brique par brique |
| **N4** | partiel | aucune arête dure ; `N2` est un plafond | la **consigne courte**, tenue à l'écart |

**Ce qui n'y est pas, et pourquoi** : `A3.4`, `A5.4`, `A6.2`, `B1.5` sont bloqués par une
ressource externe nommée ; **R44** est bloqué par l'absence d'OCR ; `B10.3` attend un **encodeur
qui porte** ; `N5` attend `N2` et `N4` ; R1/R2/R3 attendent **N2** et le banc ; les lignes
mesurées (R0.4, R0.5, R13, B11.10, B12.10, N0.3b, R41–R43)
… [1820 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"A8.3b2\" docs/ reports/ tools/ 2>/dev/null; echo '---'; find docs/pilotage/backlog -maxdepth 1 -iname '*A8*' -o -iname '*A6*' | sort", "description": "Check A8.3b2 named anywhere"}`

  ```
docs/pilotage/semaine-autonome.md:37:| **A** | A6.2 **libre** (MoE local 18 Go), A8.3a 3/19 | A6.2 routage, A8.3b2 | A (lecture seule) |
reports/a83b-decision.json:42:  "A8.3b2 instrumentation forward_lot",
reports/rapport-a83b-decision.md:52:Prochain : A8.3b2 (instrumentation `forward_lot`) ou B11.10.
reports/rapport-etat-a.md:53:opt-in**, pas ouvert. Le seul travail A réellement neuf est **A8.3b2** (instrumenter le chemin lot),
reports/rapport-etat-a.md:72:| **A8.3b2** | **à faire — libre** | A8.3b | — | `LOT=1/4 bash tools/porte-flux.sh` + instrumentation | **nommé par la fiche A8.3b, absent du graphe** |
reports/rapport-etat-a.md:163:| **A8.3b2** | **oui** | instrumenter `forward_lot` ; aucune ressource externe | **action 3** |
reports/rapport-etat-a.md:174:**A a trois lignes libres (A2.6 P2, A6.2, A8.3b2), deux bloqués réels (A3.4, A5.4) et un faux
reports/rapport-etat-a.md:186:  A8.3b2 → ligne nommée ; `dependances.md` § 5 : **4 → 2/3** items ; roadmap A8 : **6 → 19** pins.
reports/rapport-etat-a.md:189:- **Cible** : **2 bloqués** (A3.4, A5.4), **3 libres** (A2.6 P2, A6.2, A8.3b2), **0 faux bloqué**.
reports/rapport-etat-a.md:205:### Action 3 — A8.3b2 : instrumenter le chemin
… [1725 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"CUDA_VISIBLE_DEVICES\\|cudaSetDevice\\|device_count\\|multi.*gpu\\|plusieurs GPU\\|deux GPU\" drave-core/src/*.rs tools/*.py tools/*.sh 2>/dev/null | head -40", "description": "Check multi-GPU support"}`

  ```
drave-core/src/gpu.rs:197:            // Piège courant : `CUDA_VISIBLE_DEVICES=` (vide) masque TOUS les
drave-core/src/gpu.rs:200:            if std::env::var("CUDA_VISIBLE_DEVICES").map(|v| v.trim().is_empty()).unwrap_or(false) {
drave-core/src/gpu.rs:201:                std::env::remove_var("CUDA_VISIBLE_DEVICES");
drave-core/src/gpu.rs:202:                eprintln!("[gpu] CUDA_VISIBLE_DEVICES vide : ignoré (les GPU redeviennent visibles)");
drave-core/src/main.rs:7020:        // pas confortablement, et NVLink quand deux GPU se partagent le modèle.
drave-core/src/model.rs:3498:/// depuis la RAM), 19 Go en int8, 9,7 Go en int4 (13 ms depuis les deux GPU).
tools/adaptateur_langue.py:18:  CUDA_VISIBLE_DEVICES=0 python tools/adaptateur_langue.py --hf /tmp/jouet-d256 \\
tools/aligneur_litteraire.py:26:    CUDA_VISIBLE_DEVICES="" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py
tools/aligneur_litteraire.py:27:    CUDA_VISIBLE_DEVICES="" ... --json /tmp/verne.json --rapport /tmp/verne.md --sans-controles
tools/aligneur_litteraire.py:1450:        "CUDA_VISIBLE_DEVICES=\"\" /home/stephane/IA/venv-drave/bin/python tools/aligneur_litteraire.py"
tools/banc_lecteur.py:16: 
… [3258 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"VMAP\\|vram\\|VRAM\\|gpu\" drave-core/src/main.rs | head -40", "description": "Check GPU options in main"}`

  ```
77:mod gpu;
626:        (opt.gpu_banc, "--gpu-banc"), (opt.materiel, "--materiel"), (opt.config, "--config"),
656:    if opt.gpu_banc { run_gpu_banc(opt); return; }
1132:            "inactif : DRAVE_GPU_KV n'est pas posé (pas de miroir VRAM à interroger)"
1162:    infer: bool, ppl: bool, plan: bool, tokenize: bool, gpu_banc: bool, k3_essai: bool,
1274:    /// Banc du KV déporté : nombre de clés à faire tenir en VRAM.
1511:            "--gpu-banc" => { o.gpu_banc = true; 1 }
1732:        // Le pool est publié À PART : c'est lui qui dit si la VRAM est bornée (avant lui, une
1734:        println!("[gpu] experts : {} demandes, {} manques (succès {:.1} %), {} évictions, \
3632:    println!("  cache experts    : {:.1} Go en VRAM", plan.cache_experts_go);
5763:/// du plan `docs/plan-gpu-topk.md`. Il compare les scores calculés en VRAM à la
5782:    // Un cache KV rempli de valeurs déterministes, puis son miroir VRAM.
5802:    let machine = match crate::gpu::machines().first() {
5808:        None => { println!("allocation VRAM impossible : banc terminé"); return; }
5812:            cache.vers_gpu(machine, &mut miroir, kvh, pos);
5841:    let t_gpu = t1.elapsed().as_secs_f64();
5850:    pri
… [1615 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"DRAVE_EXPERTS_VRAM\\|DRAVE_EXPERTS_RAM\\|cache experts\\|cache_experts\" drave-core/src/*.rs tools/*.sh docs/ reports/ --include='*.rs' --include='*.sh' --include='*.md' | head -60", "description": "Find expert VRAM/RAM cache options"}`

  ```
drave-core/src/main.rs:1731:    if let Some(c) = mdl.cache_experts.as_ref() {
drave-core/src/main.rs:3632:    println!("  cache experts    : {:.1} Go en VRAM", plan.cache_experts_go);
drave-core/src/materiel.rs:80:    pub cache_experts_go: f64,
drave-core/src/materiel.rs:354:        let cache_experts_go = (vram - reserve - commun_go).max(0.0);
drave-core/src/materiel.rs:359:                cache_experts_go, vram, reserve, commun_go));
drave-core/src/materiel.rs:395:        Plan { threads, epinglage, lecteurs, cache_experts_go, kv_bits, raisons }
drave-core/src/model.rs:1583:/// **Cache RAM des experts** (`DRAVE_EXPERTS_RAM` en Mo).
drave-core/src/model.rs:1669:    /// redevient le cache mesuré perdant (`DRAVE_EXPERTS_RAM`).
drave-core/src/model.rs:3110:    pub cache_experts: Option<CacheExperts>,
drave-core/src/model.rs:3111:    /// Cache RAM des experts (`DRAVE_EXPERTS_RAM`), voir `CacheExpertsRam`.
drave-core/src/model.rs:4956:        let cache_experts = if std::env::var("DRAVE_GPU_EXPERTS").is_ok()
drave-core/src/model.rs:5052:            cache_experts,
drave-core/src/model.rs:5061:                } else { match std::env::var("DRAVE_EXPERTS_RAM").ok()
drave-core/src/model.rs:848
… [1119 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1580,1745p' drave-core/src/model.rs", "description": "Read expert RAM cache implementation"}`

  ```
/// fichier, pour ne changer QU'UNE chose.
static SANS_COMPRESSION_EXERCICE: std::sync::OnceLock<bool> = std::sync::OnceLock::new();

/// **Cache RAM des experts** (`DRAVE_EXPERTS_RAM` en Mo).
///
/// Les octets d'un expert sont lus une fois depuis le NVMe et gardés en
/// mémoire. Le noyau en garde déjà une partie en `buff/cache`, mais il les
/// évince au rythme des ~330 Go lus par passe ; ici la résidence est explicite
/// et bornée.
///
/// **Ce que ça ne fait pas** : aucun octet n'est modifié, aucun ordre de
/// sommation ne change — un expert lu en RAM rend exactement ce que le mmap
/// rendait. Vérifié : 2 544 vides identiques au bit près, perplexité inchangée.
///
/// **MESURÉ PLUS LENT, et c'est le résultat qui compte.** La trace de routage
/// rendait l'idée plausible (63 jetons de wiki réel : 15 360 lectures, 3 817
/// experts distincts, 50 % des lectures dans 394 experts, 31,9 % de réutilisation
/// entre jetons consécutifs) — mais le noyau fait DÉJÀ ce travail : `buff/cache`
/// garde ~95 Go de pages du fichier, donc la copie ajoute un second exemplaire et
/// du trafic mémoire sans retirer les lectures NVMe. Mesuré, passe ctx 32
/// (31 jetons) : **145,1 s sans cache,
… [6629 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '4930,4975p' drave-core/src/model.rs; echo '---'; sed -n '330,400p' drave-core/src/materiel.rs; echo '---'; sed -n '8450,8520p' drave-core/src/model.rs", "description": "Read GPU expert cache and material plan"}`

  ```
let bits = caches_kv.first().map(|c| c.bits).unwrap_or(32);
                        if !(bits == 8 || bits == 32) {
                            println!("[gpu] top-k déporté REFUSÉ : valeurs KV {bits} bits (le noyau 3 n'en gère que 8 ou 32)");
                        } else {
                            println!("[gpu] top-k déporté demandé (DRAVE_GPU_TOPK) : actif si --attn-topk vaut 1 à 1024, sans fenêtre, et si nkv × rep = nh");
                        }
                    }
                    Some(v)
                } else {
                    println!("[gpu] KV déporté impossible sur {} périphérique(s) : contexte {} \
                              trop long pour la VRAM — cache KV gardé en RAM",
                             machines.len(), caches_kv.first().map(|c| c.ctx).unwrap_or(0));
                    None
                }
            }
        } else { None };
        // ---- MLA : reconnu à ses tenseurs, sans aucune clé de configuration
        // (les rangs se lisent dans les FORMES, ce qui évite d'ajouter cinq
        // champs à `Cfg` et de les tenir à jour).
        let mla_cache = match mla.as_ref() {
            Some(v) => v.iter().map(|m| (vec![0f32; ctx * m.
… [9558 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"enum Source\\|Mxfp4\\|Q4K\\|Q4_K\\|Source::\" drave-core/src/list.rs drave-core/src/model.rs | head -60", "description": "Check expert source formats"}`

  ```
drave-core/src/list.rs:342:pub enum Source8 {
drave-core/src/list.rs:644:pub enum Source {
drave-core/src/list.rs:645:    Propre, Q4_0, Mxfp4, Q4_K, Q6_K,
drave-core/src/list.rs:749:                  src: Source::Propre, base: std::ptr::null(), nb_ligne: 0 }
drave-core/src/list.rs:797:                  plan6: None, src: Source::Propre, base: std::ptr::null(), nb_ligne: 0 }
drave-core/src/list.rs:839:                  plan6: Some(plan6), src: Source::Propre,
drave-core/src/list.rs:892:    /// **Prête** des super-blocs Q4_K (144 octets pour 256 poids) lus dans le
drave-core/src/list.rs:893:    /// fichier. Format de toute la famille Qwen/Llama en `Q4_K_M`.
drave-core/src/list.rs:902:            src: Source::Q4_K, base, nb_ligne: nb_super,
drave-core/src/list.rs:915:            src: Source::Q6_K, base, nb_ligne: nb_super,
drave-core/src/list.rs:984:    /// Produit scalaire **Q4_K en place** (noyau AVX2).
drave-core/src/list.rs:986:    /// Q4_K est **asymétrique** : chaque sous-bloc de 32 poids a une échelle
drave-core/src/list.rs:999:            let p = self.base.add((o * self.nb_ligne + sup) * crate::gguf::TAILLE_Q4K);
drave-core/src/list.rs:1059:                  src: Source::Propre
… [4274 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"DRAVE_GPU_EXPERTS\" reports/ docs/ | head -20; echo '---'; grep -n \"MXFP4\\|mxfp4\" reports/rapport-vram-transfert.md | head -20", "description": "Check GPU expert cache reports"}`

  ```
reports/rapport-drapeaux-ignores.md:113:| `DRAVE_GPU_TETE` · `DRAVE_GPU_KV` · `DRAVE_GPU_EXPERTS` · `DRAVE_GPU_EXPERTS_GO` | `Model::load` : 1391, 1413, 1505, 1508 | Inutiles sans `DRAVE_GPU` ; sans objet en BK/GB (bancs dédiés) | — |
reports/rapport-gpu-tandem-nvlink.md:36:cache KV**, et un **cache d'experts en VRAM** (`DRAVE_GPU_EXPERTS`) mesuré à
reports/rapport-vram-transfert.md:82:Mesures — gpt-oss-120b MXFP4, 2 jetons, `DRAVE_GPU_EXPERTS_GO=8`, mêmes identifiants, données
reports/rapport-vram-transfert.md:102:Le premier essai comparait les deux binaires **sans `DRAVE_GPU_EXPERTS`** : le cache n'était donc
reports/rapport-passe-complete-13-octobre.md:63:* **rien du chemin VRAM** : aucune porte ne l'exerce (`DRAVE_GPU_EXPERTS` n'apparaît dans aucun
docs/theorie/histoire.md:56:| `QT_GPU_EXPERTS`, `QT_GPU_EXPERTS_GO` | `DRAVE_GPU_EXPERTS`, `DRAVE_GPU_EXPERTS_GO` |
docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md:208:| GPU | `DRAVE_GPU`, `DRAVE_GPU_TETE`, `DRAVE_GPU_KV`, `DRAVE_GPU_TOPK`, `DRAVE_GPU_EXPERTS`, `DRAVE_GPU_EXPERTS_GO` |
docs/theorie/glossaire/06-repartition-materiel-et-energie.md:101:`DRAVE_GPU_TETE`, `DRAVE_GPU_TOPK`, `DRAVE_GPU_EXPERTS`.
docs/i
… [1001 caractères tronqués]
  ```

- **bash** `{"command": "git log -1 --format='%h %ad %s' --date=iso -- drave-core/src/model.rs; echo '---'; git log -1 --format='%h %ad %s' --date=iso -- drave-core/src/main.rs; echo '---'; git log -1 --format='%h %ad %s' --date=iso -- drave-core/target/release/drave 2>/dev/null || true; echo '---'; git status  … [78 caractères tronqués]`

  ```
d199ce16 2026-10-28 12:34:34 -0400 N0.3b — PPL DRVM EN MÉMOIRE : 28,7355 SANS FICHIER GGUF TEMPORAIRE
---
720d7e7d 2026-10-30 08:41:04 -0400 N3.5f — POSITION VÉRIFIÉE PAS À PAS, DÉSYNC REFUSÉE (CODE 4) ; PORTE 76
---
a44414d2 2026-09-30 10:01:17 -0400 Hygiène : sortir les artefacts de compilation du dépôt, et committer la sentinelle
---
  ```

- **bash** `{"command": "grep -n \"porte-flux\" docs/pilotage/references-non-regression.md | head; echo '---'; grep -n \"61.9920\\|60.8135\\|62.7357\\|58.3200\" tools/porte-flux.sh reports/a83b-lot.json reports/rapport-a83b-lot.md | head -20", "description": "Check pinned refs"}`

  ```
85:| `porte-flux.sh` | 24 s | mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427) |
151:   d'exécution se paie d'un passage des portes (`porte-flux.sh` au minimum, cinq modes, ~2 min) ;
---
tools/porte-flux.sh:80:            "mode 0"*|"mode 1"*|"mode 2"*) ref_attendue="58.3200" ;;
tools/porte-flux.sh:81:            "mode 3"*|"mode 4"*) ref_attendue="62.7357" ;;
tools/porte-flux.sh:143:# Références PPL (A8.0) : les modes 0/1/2 partent de 61,9920 ; les modes 3/4 de
tools/porte-flux.sh:144:# 60,8135 (le lot dense change la référence locale). La PPL à deux nœuds des modes
tools/porte-flux.sh:146:tester "mode 0 — f32 dense"          "0"      "61.9920" --flux
tools/porte-flux.sh:147:tester "mode 1 — listes quantifiées" "0"      "61.9920" --flux-listes
tools/porte-flux.sh:148:tester "mode 2 — listes par blocs"   "6e-2"   "61.9920" --flux-blocs --lot 1
tools/porte-flux.sh:149:tester "mode 3 — lot dense f32"      "0"      "60.8135" --lot "${LOT:-4}"
tools/porte-flux.sh:150:tester "mode 4 — lot en listes"      "1e-2"   "60.8135" --lot "${LOT:-4}" --flux-blocs
reports/a83b-lot.json:12:   "2": 60.8135,
reports/a83b-lot.json:13:   "4": 60.8135,
reports/a83b-lot.json:
… [480 caractères tronqués]
  ```

- **bash** `{"command": "git rev-parse --abbrev-ref HEAD; git log -1 --format='%H%n%ad%n%s' --date=iso; date '+%Y-%m-%d %H:%M %Z'", "description": "Get branch, HEAD, date"}`

  ```
s/v7
dc78f22319e81b253ae094df873cafe74137b4bd
2026-11-13 22:40:57 -0500
ÉTAT — T0 DANS LE BUDGET (3 991 MOTS) : LA LIGNE R0.7 PORTE LE TAGGER 612 (0,9475, +8,49, INTÉGRER)
2026-11-13 22:45 EST
  ```

- **bash** `{"command": "sha256sum \"$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf\" 2>/dev/null | cut -c1-16; echo '---'; python3 - <<'PY'\nimport os\np=os.path.expanduser('~/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf')\nn=os.path.getsize(p)\nprint(n, n/1e9, n/2**30)\nPY", "description": "Hash prefix and exact size of  … [26 caractères tronqués]`

  ```
6c997b8af17debdf
---
18556686752 18.556686752 17.28226128220558
  ```

- **bash** `{"command": "sha256sum \"$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf\"", "description": "Full sha256 of MoE file", "timeoutMs": 180000}`

  ```
6c997b8af17debdfb01d890214400ccbab00db6acc0ba8da5de1cc906c4774d0  /home/stephane/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf
  ```

- **bash** `{"command": "sed -n '1,80p' reports/rapport-gpu-tandem-nvlink.md", "description": "Read GPU tandem report"}`

  ```
# Le tandem GPU (2 × Quadro RTX 5000, NVLink) : ce qu'il fait, ce qu'il pourrait faire

> Question posée le 03/10 : « fais-tu bon usage du tandem de GPU en NVLink pour
> distribuer la charge principale ? »
>
> Réponse courte : **non — pour V4-Flash et V4.1, la charge principale (le MoE) est
> entièrement sur le CPU, et les deux GPU sont au repos.** Ce n'est pas un oubli :
> c'est la condition même du chemin GPU du moteur qui l'exclut. Ce rapport chiffre
> l'écart et ce qu'il faudrait pour le combler.

## 1. Le matériel, mesuré

```
GPU 0: Quadro RTX 5000 (16 Go)   GPU 1: Quadro RTX 5000 (16 Go)
topologie : GPU0 NV1 GPU1         (NVLink, 1 lien)
nvidia-smi nvlink -s : 25,781 Go/s par lien et par sens
NUMA : les deux GPU sur le node 0 (CPU 0-9,20-29)
PCIe : maximum Gen3 x16 (l'état courant oscille Gen1/Gen2 au repos — abaissement
       de veille classique, à revérifier sous charge)
```

Turing, 16 Go de VRAM chacun : **32 Go au total**, et 25,78 Go/s entre les deux
(soit ~4× le PCIe mesuré du dépôt).

## 2. Ce que le moteur fait des GPU aujourd'hui

Le principe est écrit dans `drave-core/src/gpu.rs` :

> « **les poids restent sur le GPU**. Mesuré : PCIe x8 6,5 Go/s contre 380 Go/s e
… [2832 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' reports/rapport-vram-transfert.md", "description": "Read VRAM transfer report"}`

  ```
# La VRAM : ce qui coûte n'est pas le lien, c'est l'allocation

> Campagne : **machine et moteur** · expérience 02 — le transfert vers la VRAM, par expert
> Question : la direction du 12/10 demande, pour la VRAM, le même remède que pour le disque —
> « granularité fine, allocation intelligente au lieu de virtualiser une grande mémoire en
> lecture aléatoire ». Le cache d'experts VRAM actuel a été mesuré **perdant** (×1,09) ; avant de
> le refaire, il faut savoir **ce qui coûte** dans un transfert : le lien, ou autre chose ?
> Verdict : **l'allocation.** Monter un expert coûte **3,39 ms** (Q4_K, 0,88 Mo) et **11,72 ms**
> (MXFP4, 4,41 Mo) quand chaque montage alloue son tampon ; dans **un tampon réutilisé**, les
> mêmes octets montent en **0,27 ms** et **1,05 ms**. Autrement dit : **37 % du coût en Q4_K et
> 91 % en MXFP4 sont l'allocation**, pas le transfert. Le lien, lui, rend **5,2 Go/s** (Q4_K) et
> **4,2 Go/s** (MXFP4) en copies paginées.
> Date réelle : 2026-10-12, 22 h 50-23 h 00 HAE (heure lue sur la machine ; source : git, commit `334f8085`)
> Protocole : `drave --gpu-banc --matrix blk.0.ffn_gate_exps.weight` (`DRAVE_GPU=1`), 16 experts
> montés un par un, puis 15 dans un t
… [5847 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"struct CacheExperts\\|impl CacheExperts\\|fn obtenir\" drave-core/src/model.rs | head; echo '---'; sed -n '3150,3240p' drave-core/src/model.rs", "description": "Inspect CacheExperts implementation"}`

  ```
1603:pub struct CacheExpertsRam {
1610:impl CacheExpertsRam {
1991:pub struct CacheExperts {
2015:impl CacheExperts {
2046:    fn obtenir<'a>(&'a mut self, machine: &crate::gpu::Gpu, l: usize, e: usize,
---

/// Un neurone ajouté à une couche, sans réentraînement du reste du modèle.
///
/// Il suit la forme SwiGLU du réseau : `a = silu(u·x) · (v·x)`, contribution
/// `a · d` ajoutée au flux résiduel. Le point important : **le produit de deux
/// formes linéaires est quadratique**. Prendre `u` sur une ligne existante de
/// `gate` et `v` sur une AUTRE ligne de `up` fabrique une caractéristique que le
/// réseau n'a jamais calculée — les 4 864 neurones d'origine n'apparient que
/// `gate[i]` avec `up[i]`.
///
/// Format binaire du fichier (little-endian) :
///   magie "QPAT" | version u32 | couche u32 | n u32 | n f32 (u) | n f32 (v) | n f32 (d)
pub struct Patch {
    pub layer: usize,
    pub u: Vec<f32>,
    pub v: Vec<f32>,
    pub d: Vec<f32>,
}

impl Patch {
    pub fn load(path: &str) -> std::io::Result<Patch> {
        use std::io::Read;
        let mut buf = Vec::new();
        std::fs::File::open(path)?.read_to_end(&mut buf)?;
        if buf.len() < 16 || &buf[0..4] != b"QPAT
… [2789 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1991,2095p' drave-core/src/model.rs", "description": "Read CacheExperts obtenir"}`

  ```
pub struct CacheExperts {
    /// Une entrée par (couche, expert) : ses trois matrices (gate, up, down).
    cartes: std::collections::HashMap<(usize, usize), (crate::gpu::MatriceGpu,
                                                       crate::gpu::MatriceGpu,
                                                       crate::gpu::MatriceGpu, u64)>,
    pub octets: usize,
    pub budget: usize,
    pub demandes: u64,
    pub manques: u64,
    pub evictions: u64,
    pub octets_envoyes: u64,
    ticks: u64,
    /// **Tampons libérés, réutilisables.** Deux raisons, mesurées le 12/10 :
    ///   * `charger_mxfp4` ALLOUE à chaque montage, et l'allocation est **37 %** (Q4_K) à **91 %**
    ///     (MXFP4) du coût d'un montage — 11,72 ms contre 1,05 ms pour les mêmes 4,41 Mo
    ///     (`reports/rapport-vram-transfert.md`) ;
    ///   * `MatriceGpu` n'a **pas de `Drop`** : une éviction laissait la VRAM allouée pour de bon.
    ///     Le pool garde ces tampons et les réutilise, donc la VRAM d'un run est bornée par
    ///     `budget`, ce qui était l'intention du budget depuis le début.
    libres: Vec<crate::gpu::MatriceGpu>,
    /// Octets actuellement retenus par le pool (comptés dans l
… [4241 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && env DRAVE_TAMPONS=1 timeout 600 ./drave-core/target/release/drave \"$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf\" --ppl \"$HOME/IA/scratch/prerequis/ids_qwen3_30b_wt2.txt\" --ctx 512 --limit 32 --threads 8 2>&1 | tee /tmp/a62-ppl32.lo … [173 caractères tronqués]`

  ```
[modele] 48 couches chargées en 9.822170116s — listes 0.91 Go , 8 threads
      31 tokens notés — perplexité cumulée 37.201  (3.1 tok/s)
=== perplexité 37.2013 sur 31 tokens (0 événements, 9.9 s) ===
EXIT=0
  ```

- **bash** `{"command": "sed -n '1,70p' reports/rapport-a83c-lot.md; echo '===='; sed -n '1,70p' reports/rapport-a83d-lot-threads.md", "description": "Read A8.3c/d summaries"}`

  ```
# A8.3c — le lot n'est pas neutre : la « non-monotonie » du KV était un effet de chemin

> **Ligne de roadmap** : A8.3 (suite d'A8.3b) · **Date** : 2026-10-29 · **Verdict** : ✅
> **expliqué** — le régime du KV a un effet **cohérent sur chaque chemin** : **−5,9 %** sur le
> chemin jeton par jeton, **+3,2 %** sur le chemin par lots. La « non-monotonie » d'A8.3b
> n'était pas la règle : c'étaient **deux chemins différents**, et le lot déplace à lui seul la
> PPL de **1,90 %** (61,9920 à lot 1 contre 60,8135 à lot ≥ 2, en f32).
>
> **Dispositif** : `porte-flux`, mode 3 (`--lot`), deux régimes de KV (f32 ; mélange 1 % par
> `DRAVE_PERTE_MAX=1`), trois lots (1, 2, 4) ; Qwen2.5-0.5B-Q8_0, GPU ; JSON
> [`a83c-lot.json`](a83c-lot.json) ; suite d'[A8.3](rapport-a83-defaut.md) et
> [A8.3b](rapport-a83b-regimes.md).

## La question

A8.3b a montré que le mélange KV « améliore » le mode 0 (−5,9 %) et « dégrade » le mode 3
(+3,2 %) — un signe qui n'est pas celui d'une quantification. D'où vient-il : de la règle, du
nombre de couches, ou du **chemin de calcul** ?

## Ce qui est mesuré

| lot | f32 | mélange 1 % | effet du mélange |
|---|---:|---:|---:|
| **1** (jeton par jeton) | **61,9920** | **
… [5538 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/a83c-lot.json; echo '===='; cat reports/a83d-lot-threads.json", "description": "Read A8.3c/d JSON"}`

  ```
{
 "date": "2026-10-29",
 "ligne": "A8.3c",
 "dispositif": {
  "modele": "Qwen2.5-0.5B-Q8_0",
  "porte": "porte-flux (mode 3)",
  "regimes": [
   "f32",
   "melange_1"
  ],
  "lots": [
   1,
   2,
   4
  ]
 },
 "mesures": {
  "lot_1": {
   "f32": 61.992,
   "melange_1": 58.32
  },
  "lot_2": {
   "f32": 60.8135,
   "melange_1": 62.7357
  },
  "lot_4": {
   "f32": 60.8135,
   "melange_1": 62.7357
  }
 },
 "effets_pct": {
  "melange_lot_1": -5.9,
  "melange_lot_4": 3.2,
  "lot_sur_f32": -1.9
 },
 "explication": "le préremplissage par lots n'est pas bit à bit identique (main.rs l. 799-812) : sommes réordonnées, routeur à l'égalité",
 "verdict": "non-monotonie expliquée : effet par chemin, pas anomalie de la règle",
 "prochain": "réduire la non-équivalence du lot, ou l'assumer comme références distinctes"
}====
{
  "ligne": "A8.3d",
  "date": "2026-10-30",
  "dispositif": {
    "modele": "Qwen2.5-0.5B-Q8_0",
    "porte": "porte-flux mode 3 (--lot)",
    "lots": [1, 4],
    "threads": [1, 8],
    "ids": 24,
    "ctx": 64
  },
  "mesures": {
    "threads_8": {"lot_1": 61.9920, "lot_4": 60.8135},
    "threads_1": {"lot_1": 61.9920, "lot_4": 60.8135}
  },
  "ecart_pct": {"threads_8": -1.90
… [221 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '4710,4775p' drave-core/src/main.rs; echo '---'; sed -n '5380,5470p' drave-core/src/main.rs", "description": "Inspect distributed lot protocol"}`

  ```
// calculent pas la même chose.
                f.act.appliquer(&mut mdl);
                mdl.couche_debut = f.debut as usize;
                mdl.couche_fin = f.fin as usize;
                // Le nœud moteur rend TOUJOURS un flux résiduel brut : la norme
                // finale appartient au nœud qui a la tête de sortie, et à lui
                // seul. C'est ce qui manquait — 798,3 au lieu de 18,2.
                mdl.flux_brut = true;
                // Les DEUX modes de lot : 3 (dense f32) et 4 (listes). Oublier le
                // second faisait tomber un flux de listes dans le chemin « un seul
                // vecteur » et paniquait sur `en_dense` — attrapé au premier essai.
                if f.mode == MODE_LOT || f.mode == MODE_LOT_LISTES {
                    // Préremplissage réparti : N états d'un coup. Le nœud n'a pas
                    // les identifiants de jetons — il n'en a pas besoin, les
                    // états entrent directement dans SA première couche.
                    let t = f.n;
                    // Refus EXPLICITE plutôt qu'une boucle sans fin : au-delà de
                    // son contexte, `KvCache::assurer` ne peut pas agrandir et
  
… [7031 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for L in 1 4; do echo \"######## LOT=$L\"; LOT=$L timeout 600 bash tools/porte-flux.sh 2>&1 | tee /tmp/porte-flux-lot$L.log | tail -25; echo \"EXIT=${PIPESTATUS[0]}\"; done", "description": "Run porte-flux at lot 1 and 4", "timeoutMs … [10 caractères tronqués]`

  ```
######## LOT=1
  mode 0 — f32 dense               0.00e0  ✅  (réf 61.9920 / deux nœuds 61.9920)
  mode 1 — listes quantifiées     0.00e0  ✅  (réf 61.9920 / deux nœuds 61.9920)
  mode 2 — listes par blocs        3.65e-2  ✅  (réf 61.9920 / deux nœuds 64.2535)
  mode 3 — lot dense f32           0.00e0  ❌ référence PPL 61.9920 (attendu 60.8135)
  mode 4 — lot en listes           3.65e-2  ❌ référence PPL 61.9920 (attendu 60.8135)
EXIT=1
######## LOT=4
  mode 0 — f32 dense               0.00e0  ✅  (réf 61.9920 / deux nœuds 61.9920)
  mode 1 — listes quantifiées     0.00e0  ✅  (réf 61.9920 / deux nœuds 61.9920)
  mode 2 — listes par blocs        3.65e-2  ✅  (réf 61.9920 / deux nœuds 64.2535)
  mode 3 — lot dense f32           0.00e0  ✅  (réf 60.8135 / deux nœuds 60.8135)
  mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
EXIT=0
  ```

- **bash** `{"command": "echo '===== LOT=1'; cat /tmp/porte-flux-lot1.log; echo '===== LOT=4'; cat /tmp/porte-flux-lot4.log", "description": "Read full porte-flux logs"}`

  ```
===== LOT=1
  mode 0 — f32 dense               0.00e0  ✅  (réf 61.9920 / deux nœuds 61.9920)
  mode 1 — listes quantifiées     0.00e0  ✅  (réf 61.9920 / deux nœuds 61.9920)
  mode 2 — listes par blocs        3.65e-2  ✅  (réf 61.9920 / deux nœuds 64.2535)
  mode 3 — lot dense f32           0.00e0  ❌ référence PPL 61.9920 (attendu 60.8135)
  mode 4 — lot en listes           3.65e-2  ❌ référence PPL 61.9920 (attendu 60.8135)
===== LOT=4
  mode 0 — f32 dense               0.00e0  ✅  (réf 61.9920 / deux nœuds 61.9920)
  mode 1 — listes quantifiées     0.00e0  ✅  (réf 61.9920 / deux nœuds 61.9920)
  mode 2 — listes par blocs        3.65e-2  ✅  (réf 61.9920 / deux nœuds 64.2535)
  mode 3 — lot dense f32           0.00e0  ✅  (réf 60.8135 / deux nœuds 60.8135)
  mode 4 — lot en listes           4.45e-3  ✅  (réf 60.8135 / deux nœuds 60.5427)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo '######## 1% LOT=4'; DRAVE_PERTE_MAX=1 LOT=4 timeout 600 bash tools/porte-flux.sh 2>&1 | tee /tmp/porte-flux-perte1-lot4.log | tail -12; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run 1% gate at lot 4", "timeoutMs": 600000 … [1 caractères tronqués]`

  ```
######## 1% LOT=4
  mode 0 — f32 dense               0.00e0  ✅  (réf 58.3200 / deux nœuds 58.3200)
  mode 1 — listes quantifiées     0.00e0  ✅  (réf 58.3200 / deux nœuds 58.3200)
  mode 2 — listes par blocs        1.14e-1  ✅  (réf 58.3200 / deux nœuds 64.9975)
  mode 3 — lot dense f32           0.00e0  ✅  (réf 62.7357 / deux nœuds 62.7357)
  mode 4 — lot en listes           3.49e-2  ✅  (réf 62.7357 / deux nœuds 64.9228)
EXIT=0
  ```

- **bash** `{"command": "sed -n '100,160p' tools/porte-flux.sh; echo '---'; sed -n '5280,5385p' drave-core/src/main.rs", "description": "Inspect gate comparison and pilot reference"}`

  ```
local ppl_ref ppl_deux
    ppl_ref=$(printf '%s\n' "$sortie" | grep -oE "référence locale +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
    ppl_deux=$(printf '%s\n' "$sortie" | grep -oE "deux nœuds +: perplexité [0-9.]+" | grep -oE "[0-9.]+$")
    if [ -z "$ecart" ] || [ "$code" != "0" ]; then
        printf "  %-34s %s\n" "$nom" "❌ pas d'écart mesuré (code $code)"; echec=1
        printf '%s\n' "$sortie" | tail -3 | sed 's/^/      /'
        return
    fi
    # A8.0 — la PPL de référence est ÉPINGLÉE : la porte ne vérifie plus seulement
    # l'écart entre deux nœuds, elle vérifie l'absolu. Tolérance 5e-4 (0,05 %) :
    # les références sont stables à quatre décimales sur ce modèle.
    local ok_ref
    ok_ref=$(python3 -c "import sys; a=float('$ppl_ref'); b=float('$ref_attendue'); sys.exit(0 if abs(a-b) <= 5e-4*max(b,1.0) else 1)" 2>/dev/null && echo oui || echo non)
    if [ "$ok_ref" != "oui" ]; then
        printf "  %-34s %s  ❌ référence PPL %s (attendu %s)\n" "$nom" "$ecart" "$ppl_ref" "$ref_attendue"; echec=1
        return
    fi
    # Le mode 2 est le codec de référence (avec perte) : le mode 4 emploie le
    # MÊME codec par état, donc il ne doit pas être plus dégradé qu
… [8401 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --tokenize --fichier data/wikitext2_test.txt --sortie /tmp/ids_gate_flux.txt >/dev/null 2>&1 && for lot in 1 4; do echo \"=== lot=$lot\"; ./drave-core/target/release/dra … [510 caractères tronqués]`

  ```
=== lot=1
=== perplexité 48.5799 sur 23 tokens (0 événements, 1.0 s) ===
=== lot=4
=== perplexité 48.5666 sur 23 tokens (0 événements, 0.8 s) ===
--- perte1
=== 1% lot=1
=== perplexité 48.5937 sur 23 tokens (0 événements, 1.0 s) ===
=== 1% lot=4
=== perplexité 48.6700 sur 23 tokens (0 événements, 0.8 s) ===
  ```

- **bash** `{"command": "ls -l /tmp/ids_gate_flux.txt /tmp/campagne24/ids_0.5B-Q8.txt; echo '---'; head -c 200 /tmp/ids_gate_flux.txt; echo; echo '---'; tail -c 200 /tmp/ids_gate_flux.txt; echo; echo '---'; ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_gate_flux.txt --ctx 64 --l … [96 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 394684  4 nov 08:07 /tmp/campagne24/ids_0.5B-Q8.txt
-rw-r--r--. 1 stephane stephane 394684 13 nov 22:52 /tmp/ids_gate_flux.txt
---
198,284,8397,425,10965,465,284,14731,8397,425,10965,465,374,458,6364,4531,1154,12425,323,33496,12089,659,1260,1030,264,8640,569,12,31,39400,3476,389,279,12425,4013,576,8596,304,220,17,15,15,15,659,109
---
1368,284,284,284,14731,730,54990,672,374,264,30444,835,269,799,369,8438,991,96937,50086,905,1154,17426,64303,41595,320,55420,873,1154,9449,60585,320,15294,873,1154,67327,43825,1154,323,85081,659,14731
---
=== perplexité 48.5799 sur 23 tokens (0 événements, 1.0 s) ===
    23.9 tok/s effectifs (avant + tête)
    attention : 0.00 M paires (requête, clé) par token
    projections : 0.0 M événements par token
    paires (poids × activation) par token : attention 46.0 M · experts 0.0 M · partagé 463.6 M · scores 4 K · total 509.5 M
    occupation des poids : 99.2 % de non-nuls (489995762 sur 493961216) — attention 99.1 % · experts 0.0 %
    ⇒ si la représentation était CREUSE (non-nuls × activations vivantes, hypothèse) : 505.4 M paires par token au lieu de 509.5 M (÷1.01)
    dont en listes (une paire y est un événement) : 0.
… [423 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"couche_fin\\|couche_debut\" drave-core/src/main.rs | sed -n '1,80p'; echo '---'; grep -n \"fn ppl_reparti\\|fn run_ppl_reparti\\|ppl_reparti\" drave-core/src/main.rs | head", "description": "Find couche_fin assignments in repart"}`

  ```
1065:             mdl.couche_debut, mdl.couche_fin, mdl.flux_brut,
4712:                mdl.couche_debut = f.debut as usize;
4713:                mdl.couche_fin = f.fin as usize;
5204:    // LA FIN DE PLAGE EST EXCLUSIVE : le nœud fait `couche_fin = f.fin` et exécute
5436:    mdl.couche_fin = couches_locales;
---
623:        (opt.ppl_reparti.is_some(), "--ppl-reparti"),
651:    if let Some(pair) = opt.ppl_reparti.clone() { run_ppl_reparti(opt, &pair); return; }
1303:    ppl_reparti: Option<String>,
1530:            "--ppl-reparti" => { o.ppl_reparti = Some(suivant(i).clone()); 2 }
5115:fn run_ppl_reparti(opt: Options, pair: &str) {
  ```

- **bash** `{"command": "grep -n \"pub fn load\" drave-core/src/model.rs | head; sed -n '4500,4545p' drave-core/src/model.rs; echo '---'; sed -n '5115,5175p' drave-core/src/main.rs", "description": "Inspect Model::load args and repart start"}`

  ```
3170:    pub fn load(path: &str) -> std::io::Result<Patch> {
3882:    pub fn load(path: &str, ctx: usize, n_threads: usize, dense: bool, keep: f32,
3888:    pub fn load_partiel(path: &str, ctx: usize, n_threads: usize, dense: bool, keep: f32,
3896:    pub fn load_partiel_g(g: Gguf, ctx: usize, n_threads: usize, dense: bool, keep: f32,
        // Deux sources pour les trois hyper-paramètres, et il faut les deux :
        // V4-Flash les déclare en clés GGUF normalisées
        // (`deepseek4.hyper_connection.*`), V4.1 seulement dans le `config.json`
        // recopié sous `deepseek41.config` (`hc_mult`, `hc_sinkhorn_iters`,
        // `hc_eps`). Lire une seule des deux donne `hc = 0` — donc un modèle
        // silencieusement traité comme s'il n'avait pas d'hyper-connexions.
        // **V4.1 = mHC RETARDÉ.** L'architecture se lit dans
        // `general.architecture` (« deepseek41 » contre « deepseek4 » pour
        // V4-Flash) : c'est elle qui décide QUELLE chaîne de repliement
        // s'applique, et se tromper donne des nombres plausibles et faux — le
        // même genre d'erreur que la base RoPE des couches compressées.
        let hc_retarde = g.meta.get("general.archi
… [5370 caractères tronqués]
  ```

- **bash** `{"command": "grep -n '\"--dense\"\\|dense:' drave-core/src/main.rs | head -10; grep -n \"Model::load\" drave-core/src/main.rs | head -10", "description": "Check dense flag"}`

  ```
1055:fn options_actives(mdl: &model::Model, mode: &str, ctx_impose: bool, dense: bool, keep: f32,
1326:    ctx: usize, threads: usize, abits: u32, dense: bool, auto: bool,
1652:            "--dense" => { o.dense = true; 1 }
1768:    let mut mdl = model::Model::load_partiel(path, ctx, n_threads, dense, keep, auto, q4, b6,
2841:            let mut mdl = model::Model::load(&chemin, 512, 16, true, 1.0, false, 0, 0);
4571:    let mut mdl = model::Model::load(&chemin, ctx, fils(&opt), true, opt.keep, false, 0, 0);
5290:    let mut mdl = model::Model::load(&chemin,
6352:    let mut mdl = model::Model::load(path, 4096, fils(&opt), opt.dense, opt.keep, false, 0, 0);
7328:    let mut mdl = model::Model::load_partiel(&path, ctx, n_threads, false, 1.0, false, 0, 0, None);
7366:        let mut m = model::Model::load_partiel(&path, ctx, n_threads, false, 1.0, false, 0, 0,
7466:        let mut mdl = model::Model::load_partiel(&path, ctx, n_threads, false, 1.0, false, 0, 0,
7477:            let mut mdl = model::Model::load_partiel(&path, ctx, n_threads, false, 1.0, false,
8027:    let mut mdl = model::Model::load_partiel(chemin, ctx, fils(opt), true, opt.keep, false, 0, 0,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for lot in 1 4; do echo \"=== dense lot=$lot\"; ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_gate_flux.txt --ctx 64 --limit 24 --threads 8 --dense --lot $lot 2>&1 | grep -E \"perplexité .* sur\" | ta … [386 caractères tronqués]`

  ```
=== dense lot=1
=== perplexité 48.5799 sur 23 tokens (0 événements, 1.0 s) ===
=== dense lot=4
=== perplexité 48.5666 sur 23 tokens (0 événements, 0.8 s) ===
--- dense perte1
=== dense 1% lot=1
=== perplexité 48.5937 sur 23 tokens (0 événements, 1.0 s) ===
=== dense 1% lot=4
=== perplexité 48.6700 sur 23 tokens (0 événements, 0.9 s) ===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PORT=49321; ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur $PORT --ctx 64 --threads 8 >/tmp/srv.log 2>&1 & SRV=$!; for i in $(seq 1 40); do grep -q \"nœud moteur sur\" /tmp/srv.log 2>/dev/null && break … [432 caractères tronqués]`

  ```
[flux] pilote : 12 couches en local, 12 chez le pair, 24 jetons
  référence locale  : perplexité 61.9920  (1.0 s)
  deux nœuds        : perplexité 61.9920  (1.0 s)
--- srv
[flux] nœud moteur sur 127.0.0.1:49321 · 896 cachés · 24 couches · contexte 64
[flux] client connecté : 127.0.0.1:63600
[flux] arrêt : failed to fill whole buffer
[horloge] 23 pas servis
[flux] 23 flux servis
  ```

- **bash** `{"command": "grep -n \"fn run_ppl\" drave-core/src/main.rs; sed -n '6320,6395p' drave-core/src/main.rs", "description": "Inspect run_ppl id truncation"}`

  ```
5115:fn run_ppl_reparti(opt: Options, pair: &str) {
8158:fn run_ppl(opt: Options) {
8162:fn run_ppl_avec(opt: Options, g_drvm: Option<Gguf>) {
                set.sort_unstable();
                if set == att { ok_lignes += 1; }
            }
            // ⚠️ `t_k2` et `t2_k2` sont en SECONDES : les afficher avec l'unité « ms »
            // sans convertir a fait croire à un noyau 1 500× trop rapide — un
            // affichage mal étiqueté est un affichage qui ment.
            println!("    second passage k = {k2}, mêmes tampons : {ok_lignes}/{lignes} lignes · \
{:.2} ms ({:.2} ms de seuil) · cases non écrites {vides}", t_k2 * 1e3, t2_k2 * 1e3);
            if ok_lignes != lignes || vides != 0 {
                println!("    → ÉCART : la réutilisation des tampons avec un k plus grand est \
suspecte");
            }
        } else {
            println!("    second passage k = {k2} : REFUSÉ (la réutilisation des tampons est \
cassée)");
        }
    }
}

/// Banc **MLA** : passe avant du modèle synthétique, logits écrits en binaire
/// pour être comparés à `logits.npy` (référence numpy indépendante).
fn run_banc_mla(opt: Options, sortie: &str) {
    use std::io::Write;
    //
… [2867 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '8158,8245p' drave-core/src/main.rs", "description": "Read run_ppl_avec"}`

  ```
fn run_ppl(opt: Options) {
    run_ppl_avec(opt, None)
}

fn run_ppl_avec(opt: Options, g_drvm: Option<Gguf>) {
    // La restriction de la tête n'a pas de sens ici : le softmax normalise sur
    // tout le vocabulaire, et retirer des termes en retire aussi de la masse au
    // dénominateur. Mesuré, la perplexité BAISSE alors artificiellement (24,31
    // contre 25,37) — elle n'est plus comparable à rien.
    if let Some(f) = &opt.tete_restreinte {
        eprintln!("[tete] --tete-restreinte ignore en perplexite ({f}) : une perplexite \
calculee sur un vocabulaire restreint n'est comparable a rien. Utilisez --infer.");
    }
    let montre_options = opt.options_actives;
    // Capturés AVANT la déstructuration : `let Options { .. } = opt` déplace les
    // champs un à un, et `&opt` n'existe plus après (attrapé à la compilation).
    let (f_etat, f_alpha, f_pos, e_sortie, e_pos) =
        (opt.fusion_etat.clone(), opt.fusion_alpha, opt.fusion_pos,
         opt.etat_sortie.clone(), opt.etat_pos);
    let (tete_partielle_opt, adaptateur_opt) = (opt.tete_partielle, opt.adaptateur_sortie.clone());
    let Options {
        ids_file: idfile, texte_file, ppl_texte: _, limit, depuis,
  
… [3294 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nids=open('/tmp/ids_gate_flux.txt').read().strip().split(',')\nprint(len(ids))\nopen('/tmp/ids_last24.txt','w').write(','.join(ids[-24:]))\nPY\nfor lot in 1 4; do echo \"=== dense last24 lot=$lot\"; ./drave-core/targ … [550 caractères tronqués]`

  ```
85626
=== dense last24 lot=1
=== perplexité 214.1443 sur 23 tokens (0 événements, 1.0 s) ===
=== dense last24 lot=4
=== perplexité 214.1520 sur 23 tokens (0 événements, 0.9 s) ===
--- perte1
=== dense 1% last24 lot=1
=== perplexité 214.6174 sur 23 tokens (0 événements, 0.9 s) ===
=== dense 1% last24 lot=4
=== perplexité 213.9042 sur 23 tokens (0 événements, 0.8 s) ===
  ```

- **bash** `{"command": "sed -n '1,60p' tools/analyse_reutilisation_experts.py; echo '---'; grep -n \"DRAVE_EXPERTS_RAM\\|DRAVE_GPU_EXPERTS\" docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md | head", "description": "Read reuse tool usage"}`

  ```
#!/usr/bin/env python3
"""analyse_reutilisation_experts.py — la réutilisation des experts, mesurée.

Lit une trace de routage (`DRAVE_TRACE_EXPERTS=chemin` : une ligne par
(couche, jeton), `couche jeton e1 e2 …`) et répond à LA question qui décide si un
cache d'experts peut servir un modèle trop gros pour tenir en mémoire :

    les mêmes experts reviennent-ils d'un jeton à l'autre ?

Ce qu'il rend, par couche et globalement :

  - la **couverture** : combien d'experts DISTINCTS sont touchés sur N jetons ;
  - la **réutilisation immédiate** : part des experts du jeton t déjà vus au
    jeton t−1 (le chiffre qui compte pour un cache LRU sans réentraînement) ;
  - la **réutilisation à distance** : part des experts du jeton t déjà vus dans
    les k jetons précédents (k = 1, 4, 16, tout) ;
  - la **courbe d'un cache LRU** : pour une capacité donnée (en experts par
    couche), le taux de succès mesuré — donc les octets économisés par jeton.

Usage :
    analyse_reutilisation_experts.py <trace> [--experts-par-jeton N] [--couches-totales N]
"""
import sys
from collections import Counter, OrderedDict


def lire(chemin):
    """Rend {couche: {jeton: [experts]}}."""
    par_couche = {}
   
… [1009 caractères tronqués]
  ```

- **bash** `{"command": "cat docs/pilotage/backlog/A8.3-defaut.md", "description": "Read A8.3 backlog fiche"}`

  ```
# A8.3 — Passer la règle place+perte par défaut

> **Statut** : mesurée · **Priorité** : P3 · **Programme** : A · **Dépend de** : A8.0
> **Ligne de roadmap** : A8.3 · **Fiches de résultat** :
> [`a83-defaut`](../../../reports/rapport-a83-defaut.md) et
> [`a83b-regimes`](../../../reports/rapport-a83b-regimes.md).
> **Résumé** : décider si `DRAVE_PERTE_MAX` devient le défaut ; la mesure dit **non**, pas
> encore.

## Le besoin

La règle choisit la précision du KV par couche selon la perte mesurée. Elle payait (+0,03 %
sur les dernières couches) et rendait le choix de la main. La passer par défaut ferait
bénéficier tout le monde de l'int8 tardif — à condition de ne pas déplacer les chiffres.

## L'état

**Mesurée négative** — le défaut déplace les portes épinglées de **−5,9 % à +19,5 %** ; trois
régimes sont reproductibles (f32, mélange tardif 1 %, int8 partout), et le **mélange** est un
troisième point : il **améliore deux mesures sur trois** et dégrade le mode de lot. La cause du
signe (le lot) n'est pas isolée. **A8.3 reste opt-in.**

## Le contrat

| élément | contenu |
|---|---|
| **entrée** | un budget de perte en %, la profondeur du modèle |
| **sortie** | une précision de KV p
… [1181 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PORT=49322; ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur $PORT --ctx 64 --threads 8 >/tmp/srv2.log 2>&1 & SRV=$!; for i in $(seq 1 40); do grep -q \"nœud moteur sur\" /tmp/srv2.log 2>/dev/null && bre … [350 caractères tronqués]`

  ```
référence locale  : perplexité 60.8135  (0.9 s)
  deux nœuds        : perplexité 60.8135  (0.9 s)
  ```

- **bash** `{"command": "grep -n \"logits_bin\" drave-core/src/main.rs | head -20; sed -n '8460,8535p' drave-core/src/main.rs", "description": "Check logits-bin support with lot"}`

  ```
1345:    logits_bin: Option<String>, ppl_profil: bool,
1581:            "--logits-bin" => { o.logits_bin = Some(suivant(i).clone()); 2 }
8185:        ffn_gain, logits_bin, keep,
8390:    let mut journal = match &logits_bin {
8495:    if let (Some(w), Some(f)) = (journal, &logits_bin) {
                    let moy = nll / n.max(1) as f64;
                    let gain = if moy > 1e-9 { (moy - nll_tok) / moy } else { 0.0 };
                    hd.modulateur = (1.0 + 2.0 * gain as f32).clamp(0.25, 4.0);
                }
                let b = (pos + 1) / 256;
                if b < seaux.len() { seaux[b].0 += nll_tok; seaux[b].1 += 1; }
                perte.push(nll_tok as f32);
                t_note += marque.elapsed().as_secs_f64();
                if let Some(w) = journal.as_mut() {
                    use std::io::Write;
                    tampon.clear();
                    for &v in &lg { tampon.extend_from_slice(&v.to_le_bytes()); }
                    w.write_all(&tampon).unwrap();
                    n_logits += 1;
                }
            }
            }
            pos += t;
        }
        let ppl = (nll / n as f64).exp();
        // La perplexité PROPRE à la fe
… [2811 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '8380,8410p' drave-core/src/main.rs", "description": "Read logits-bin header format"}`

  ```
f.len(), ids.len());
            f
        }
    };
    let t0 = Instant::now();
    let mut nll = 0f64;
    let mut n = 0usize;
    let mut perte: Vec<f32> = Vec::new();
    // Journal de logits : écrit à la volée (une matrice de vocabulaire fait
    // 800 Mo sur gpt-oss, la garder en mémoire serait absurde).
    let mut journal = match &logits_bin {
        Some(f) => {
            use std::io::Write;
            let mut w = std::io::BufWriter::new(
                std::fs::File::create(f).expect("création du fichier de logits"));
            w.write_all(&(mdl.cfg.vocab as i32).to_le_bytes()).unwrap();
            w.write_all(&0i32.to_le_bytes()).unwrap();   // n_pos, réécrit à la fin
            Some(w)
        }
        None => None,
    };
    let mut n_logits = 0i32;
    let mut tampon: Vec<u8> = Vec::new();
    // Profil par profondeur : la perte moyenne par tranche de 256 positions.
    // Une perplexité qui MONTE avec la position ne dit pas du tout la même
    // chose qu'une perplexité uniformément mauvaise — et à 4 096 jetons, la
    // moyenne seule ne permet pas de trancher.
    let profil = ppl_profil;
    let mut seaux: Vec<(f64, usize)> = vec![(0.0, 0); ctx.div_cei
… [163 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nrun() {\n  local lot=$1 out=$2 port=$3\n  ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur $port --ctx 64 --threads 8 >/tmp/srv_lot$lot.log 2>&1 & local srv=$!\n  for i in $(seq 1 40); do grep -q \"nœud mo … [1200 caractères tronqués]`

  ```
référence locale  : perplexité 61.9920  (1.0 s)
  deux nœuds        : perplexité 61.9920  (1.0 s)
  référence locale  : perplexité 60.8135  (0.9 s)
  deux nœuds        : perplexité 60.8135  (0.9 s)
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 7, in <module>
  File "<stdin>", line 3, in lire
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/lot1.bin'
[exit code: 1]
  ```

- **bash** `{"command": "cmp -s /tmp/ids_gate_flux.txt /tmp/campagne24/ids_0.5B-Q8.txt && echo SAME || echo DIFF; echo '---'; ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_gate_flux.txt --ctx 64 --limit 24 --threads 8 --dense --lot 1 2>&1 | head -5; echo '---'; ./drave-core/targ … [243 caractères tronqués]`

  ```
SAME
---
/tmp/ids_gate_flux.txt : 24 tokens, fenêtres de 64
[config] cache KV : 32 bits, 0.00 Go pour 64 jetons
[modele] 24 couches chargées en 1.37060712s — listes 0.00 Go , 8 threads
[config] 24 couches, hidden 896 · 
[config] puits appris sur 0/24 couches · n_rot 64 · ffn 4864 · experts 0
---
       1 tokens notés — perplexité cumulée 1849.099  (0.5 tok/s)  [fenêtre 1 : 1 notés, PPL 1849.099]
      24 tokens notés — perplexité cumulée 234.270  (8.2 tok/s)  [fenêtre 2 : 23 notés, PPL 214.144]
=== perplexité 234.2702 sur 24 tokens (0 événements, 2.9 s) ===
  ```

- **bash** `{"command": "grep -n \"trace_flux\\|trace_couches\\|flux_forcer\\|trace\\.\" drave-core/src/main.rs | sed -n '1,80p'", "description": "Check trace flux support in repart"}`

  ```
1066:             mdl.trace.is_some(), mdl.flux_force.is_some());
1258:    /// C12 — vérification : rejouer et comparer à cette trace.
1282:    trace_flux: Option<String>,
1285:    flux_forcer: Option<String>,
1311:    trace_couches: Vec<usize>,
1523:            "--trace-flux" => { o.trace_flux = Some(suivant(i).clone()); 2 }
1524:            "--flux-forcer" => { o.flux_forcer = Some(suivant(i).clone()); 2 }
1539:            "--trace-couches" => { o.trace_couches = suivant(i).split(',')
1757:        trace_flux, trace_couches, flux_forcer, ..
1816:    if let Some(chemin) = trace_flux.as_deref() {
1817:        match model::TraceFlux::nouveau(chemin, trace_couches.clone(), mdl.cfg.hidden,
1824:    if let Some(chemin) = flux_forcer.as_deref() {
4747:                    trace.enregistrer_mode(&region_trace, f.pos as u32, "local->pair",
4762:                    trace.enregistrer_mode(&region_trace, f.pos as u32, "pair->local",
4784:                trace.enregistrer_mode(&region_trace, f.pos as u32, "local->pair",
4843:                trace.enregistrer_mode(&region_trace, f.pos as u32, "pair->local",
5580:        trace.enregistrer("local", pos as u32, "local->pair", &etat, 0.0);
5676:    
… [621 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"struct TraceFlux\\|impl TraceFlux\\|fn nouveau\\|fn ecrire\" drave-core/src/model.rs | grep -A2 -B2 Trace; echo '---'; sed -n '2670,2760p' drave-core/src/model.rs", "description": "Inspect TraceFlux format"}`

  ```
1611:    pub fn nouveau(budget: usize) -> Self {
2016:    pub fn nouveau(budget: usize) -> Self {
2542:pub struct TraceFlux {
2557:impl TraceFlux {
2558:    pub fn nouveau(chemin: &str, couches: Vec<usize>, hidden: usize, n_layer: usize)
2584:    pub fn ecrire(&mut self, couche: usize, pos: usize, actifs: &[i32], echelle: f32) {
---
        use std::io::Write;
        let _ = self.fichier.write_all(&0xFFFFu16.to_le_bytes());
        let _ = self.fichier.flush();
    }
}

/// Relit une trace de flux et rend, pour (couche, position), la liste
/// enregistrée. C'est le pendant du `TraceFlux` : ce qu'un nœud distant devrait
/// recevoir pour continuer le calcul, on sait déjà l'écrire — ici, on apprend à
/// le RELIRE et à repartir de là.
pub struct FluxRelecteur {
    /// (couche, position) -> (échelle, indices/valeurs)
    /// (couche, jeton global) → (échelle, paires) pour les versions 1 et 2 : les
    /// ENTIERS d'origine sont conservés, parce que le rejeu par LOTS les réinjecte
    /// tels quels (chemin exact, sans déquantifier-requantifier).
    pub listes: std::collections::HashMap<(u16, u32), (f32, Vec<(u32, i16)>)>,
    /// Version 3 : les valeurs sont des f32 (i8 × échelle f
… [3827 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"DRVF\\|TraceFlux\\|trace-flux\" tools/ reports/ | head -20", "description": "Find trace comparison tools"}`

  ```
tools/diff_flux.py
tools/profil_flux.py
tools/flux_codec.py
tools/analyse_flux.py
tools/trace_compacite.py
tools/portes.sh
tools/granularite_flux.py
tools/invariance_semantique.py
tools/approximabilite_bloc.py
tools/plateau_multilingue.py
tools/lecture_plateau.py
tools/cancellation_langue.py
tools/contrastif_hors_echantillon.py
tools/pont_recurrent.py
tools/applique_pont.py
tools/sonde_pont.py
tools/pont_fidele.py
tools/pont_reservoir.py
tools/cache_pont.py
tools/compare_professeurs.py
  ```

- **bash** `{"command": "sed -n '2542,2625p' drave-core/src/model.rs", "description": "Read TraceFlux writer format"}`

  ```
pub struct TraceFlux {
    /// Version écrite : 2 (indices par écarts, valeurs i16 — SANS PERTE) ou
    /// 3 (`DRAVE_TRACE_BLOCS=1` : valeurs i8 et une échelle f16 par bloc de 32
    /// canaux, ~22 % plus petit, avec perte).
    pub version: u16,
    /// Nombre de canaux par bloc d'échelle en v3.
    pub bloc: usize,
    pub fichier: std::io::BufWriter<std::fs::File>,
    /// Couches à tracer (toutes si vide).
    pub couches: Vec<usize>,
    pub octets: u64,
    pub enregistrements: u64,
    pub actifs: u64,
}

impl TraceFlux {
    pub fn nouveau(chemin: &str, couches: Vec<usize>, hidden: usize, n_layer: usize)
        -> std::io::Result<Self> {
        use std::io::Write;
        let mut f = std::io::BufWriter::new(std::fs::File::create(chemin)?);
        f.write_all(b"DRVF")?;
        // Version 2 par défaut : indices par ÉCARTS, valeurs i16 — sans perte.
        // Version 3 sur `DRAVE_TRACE_BLOCS=1` : en plus, valeurs i8 et une échelle
        // f16 par bloc de 32 canaux (l'étude de compacité annonce −22 % de plus,
        // au prix de la fidélité du rejeu).
        let version: u16 = if std::env::var("DRAVE_TRACE_BLOCS").is_ok() { 3 } else { 2 };
        f.write_all(&vers
… [2980 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/diff_flux.py", "description": "Read diff_flux usage"}`

  ```
#!/usr/bin/env python3
"""Diff de deux traces de **flux d'activation** (format DRVF).

C'est l'outil qui manquait à la vision : deux exécutions du même modèle, et on
veut savoir non pas « la perplexité a bougé » mais **où** le flux diverge, à
quelle couche, à quel jeton, et de combien.

Usage : diff_flux.py <traceA> <traceB> [--top 8]
"""
import struct
import sys


def lire(chemin):
    with open(chemin, "rb") as f:
        assert f.read(4) == b"DRVF", "ce n'est pas une trace DRVF"
        version, = struct.unpack("<H", f.read(2))
        n_layer, hidden = struct.unpack("<II", f.read(8))
        listes = {}
        while True:
            b = f.read(2)
            if len(b) < 2:
                break
            couche, = struct.unpack("<H", b)
            if couche == 0xFFFF:
                break
            pos, n, echelle = struct.unpack("<IIf", f.read(12))
            actifs = {}
            if version == 2:
                # v2 : écart u8 + valeur i16 ; l'écart de 255 annonce l'indice
                # ABSOLU sur les deux octets suivants (le petit-boutiste du u32),
                # et le premier écart se compte depuis 0. C'est le format par
                # défaut des trace
… [1945 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for lot in 1 4; do echo \"=== trace lot=$lot\"; ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_last24.txt --ctx 64 --limit 24 --threads 8 --dense --lot $lot --trace-flux /tmp/tr$lot.drvf 2>&1 | grep -E … [240 caractères tronqués]`

  ```
=== trace lot=1
[trace] flux enregistré dans /tmp/tr1.drvf
[trace] 1152 listes · 1031291 neurones actifs · 3 Mo
=== perplexité 214.1443 sur 23 tokens (0 événements, 1.0 s) ===
=== trace lot=4
[trace] flux enregistré dans /tmp/tr4.drvf
[trace] 1152 listes · 1031299 neurones actifs · 3 Mo
=== perplexité 214.1520 sur 23 tokens (0 événements, 0.8 s) ===
-rw-r--r--. 1 stephane stephane 3110017 13 nov 22:55 /tmp/tr1.drvf
-rw-r--r--. 1 stephane stephane 3110041 13 nov 22:55 /tmp/tr4.drvf
--- diff
trace A : 1152 listes · trace B : 1152 listes · version 2 · 24 couches · 896 cachés
première divergence : couche 1 · jeton 2 · 896 neurones · écart max 1.622e-04 (de la dynamique)
  couche  neurones changés   écart / dynamique  1er jeton
      23             20603           5.242e-04          2
  FFN 23             20607           4.713e-04          2
       5             20607           4.300e-04          2
       8             20604           3.688e-04          2
      14             20600           3.679e-04          2
      10             20603           3.650e-04          2
      21             20606           3.602e-04          2
      12             20608           3.568e-04          2
   
… [228 caractères tronqués]
  ```

- **bash** `{"command": "grep -n '\"--couches\"' drave-core/src/main.rs | head; grep -n \"fn poser_plage\" drave-core/src/main.rs; sed -n '3920,3975p' drave-core/src/main.rs", "description": "Check couches option"}`

  ```
1532:            "--couches" => {
1020:fn poser_plage(mdl: &mut model::Model, tete_partielle: bool, adaptateur: Option<&str>) {
                if hors > 0 {
                    eprintln!("[flux] {hors} indice(s) hors dimension ignorés (flux reçu \
de {hidden} canaux) — pair bogué ou hostile ?");
                }
                x
            }
            ChargeFlux::Blocs { idx, val, echelles } => {
                let mut x = vec![0f32; hidden];
                let mut hors = 0usize;
                for (&i, &v) in idx.iter().zip(val.iter()) {
                    let b = i as usize / 32;
                    if (i as usize) < hidden && b < echelles.len() {
                        x[i as usize] = v as f32 * echelles[b];
                    } else { hors += 1; }
                }
                if hors > 0 {
                    eprintln!("[flux] {hors} indice(s) hors dimension ignorés (flux reçu \
de {hidden} canaux, {} blocs d'échelles)", echelles.len());
                }
                x
            }
        }
    }
    fn actifs(&self) -> usize {
        match self {
            ChargeFlux::Dense(v) => v.len(),
            ChargeFlux::Liste { idx, .. } | ChargeFlux::Blocs {
… [1514 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for c in '0:11' '0:23'; do echo \"=== couches $c\"; ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_last24.txt --ctx 64 --limit 24 --threads 8 --dense --lot 1 --couches $c 2>&1 | grep -E \"perplexité .* … [107 caractères tronqués]`

  ```
=== couches 0:11
[modele] 24 couches chargées en 1.232881523s — listes 0.00 Go , 8 threads
[config] 24 couches, hidden 896 · 
[config] puits appris sur 0/24 couches · n_rot 64 · ffn 4864 · experts 0
=== perplexité 71077858.1883 sur 23 tokens (0 événements, 0.6 s) ===
=== couches 0:23
[modele] 24 couches chargées en 1.196304971s — listes 0.00 Go , 8 threads
[config] 24 couches, hidden 896 · 
[config] puits appris sur 0/24 couches · n_rot 64 · ffn 4864 · experts 0
=== perplexité 70039.0118 sur 23 tokens (0 événements, 0.9 s) ===
  ```

- **bash** `{"command": "grep -rln \"routage appris\\|routeur appris\\|apprendre.*rout\\|router.*appris\\|A6.2\" tools/ drave-core/src/ docs/ reports/ 2>/dev/null | head -20", "description": "Search learned routing work"}`

  ```
tools/tokenizer_kimi/tiktoken.model
tools/profondeur_routee_oracle.py
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/idna/idnadata.py
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/idna/uts46data.py
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/platformdirs/windows.py
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/platformdirs/__pycache__/windows.cpython-313.pyc
tools/docwatch/.venv/lib/python3.13/site-packages/idna/idnadata.py
tools/docwatch/.venv/lib/python3.13/site-packages/idna/uts46data.py
tools/docwatch/.venv/bin/ruff
tools/tests/documents/bench-complet.json
tools/tests/documents/corpus/tableau/dependances.md
tools/tests/documents/corpus/tableau/en-cours.md
tools/tests/documents/corpus/tableau/index.md
tools/tests/documents/corpus/tableau/roadmap.md
tools/chantier/plan.json
drave-core/src/model.rs
docs/archive/roadmap-detail-2026-10-29.md
docs/schemas/pipeline.mmd.svg
docs/schemas/backlog-dependances.svg
docs/schemas/chantiers-decision.svg
  ```

- **bash** `{"command": "grep -rn \"routage\" reports/rapport-routage-experts.md | head -20; echo '---'; grep -n \"appris\\|apprend\\|logs\" reports/rapport-routage-experts.md | head -20", "description": "Check routing report for learned aspect"}`

  ```
1:# Rapport — le routage des experts était faux pour quatre gros modèles sur cinq
43:Une seule fonction de routage (`router`, dans `drave-core/src/model.rs`),
55:puis `× expert_weights_scale`, et le routage par table quand
74:Au passage, une leçon de méthode : réunir les deux chemins de routage a d'abord
103:calcul, et surtout rien du routage — qui, lui, était faux.
---
  ```

- **bash** `{"command": "sed -n '1,80p' tools/profondeur_routee_oracle.py; echo '---'; grep -n \"A6.2\\|routee\\|oracle\" tools/profondeur_routee_oracle.py | head -20", "description": "Read routed depth oracle tool"}`

  ```
#!/usr/bin/env python3
"""profondeur_routee_oracle.py — dessin H : ce qu'un routeur PARFAIT pourrait éviter.

LA QUESTION (docs/modele-pour-drave.md, dessin H « routage par profondeur »). Un modèle peut-il
décider, **jeton par jeton**, de s'arrêter plus tôt ? Avant d'entraîner un routeur, il faut savoir
ce qu'il y a à gagner : si un oracle qui connaîtrait la réponse ne gagne presque rien, aucun
routeur appris ne le fera. C'est la **borne supérieure**, et elle se mesure avec ce qui existe.

DEUX CHEMINS, MÊMES JETONS.
  · chemin LONG  : l'état après 24 couches (le modèle entier), relu par la norme finale et la
    tête liée — c'est le modèle, au bit près (vérifié par `verifier_chaine_etat.py` : 0,013 %) ;
  · chemin COURT : l'état après 16 couches, relu par un **adaptateur entraîné** A (896×896) puis
    la même tête gelée. C'est le meilleur lecture bon marché qu'on sache construire à cette
    profondeur — celui de C8.

TROIS CHIFFRES, ET ILS NE DISENT PAS LA MÊME CHOSE.
  1. **l'accord** : part des jetons où le chemin court rend la MÊME réponse que le chemin long.
     C'est la borne de l'oracle : sur ces jetons, sortir tôt ne change pas la décision.
  2. **la cascade** : un route
… [3974 caractères tronqués]
  ```

- **bash** `{"command": "find tools -maxdepth 2 -iname '*rout*' -o -iname '*moe*' | sort; echo '---'; grep -rln \"routeur\" tools/*.py | head -20", "description": "Find routing tools"}`

  ```
tools/census_routage.py
tools/cerveau/routeur_confiance.py
tools/cerveau/routeur_m1_m2.py
tools/clusters_moe.py
tools/porte-n3-routes.sh
tools/porte-profondeur-routee.sh
tools/profondeur_routee_oracle.py
tools/__pycache__/routeur.cpython-313.pyc
tools/routeur.py
---
tools/analyse_empreinte.py
tools/census_routage.py
tools/convertir_clusters.py
tools/entrainer_moteur.py
tools/essai_blocs.py
tools/exporter_gguf_dense.py
tools/exporter_gguf.py
tools/profondeur_routee_oracle.py
tools/routeur.py
tools/v41_attention_reference.py
tools/v41_experts_reference.py
  ```

- **bash** `{"command": "sed -n '1,60p' tools/routeur.py; echo '---'; head -40 tools/census_routage.py", "description": "Read router tools"}`

  ```
#!/usr/bin/env python3
"""routeur.py — R0.5 : choisir le lecteur (extractif ou génératif) selon la question.

POURQUOI CE FICHIER. Deux régimes mesurés, pas supposés : sur 249 questions qui partagent les
mots du document, l'extractif donne 0,72–1,00 et le modèle 0,23 ; sur 19 paraphrases, le modèle
donne 0,717 et l'extractif 0,30. Un seul lecteur perd la moitié des cas. Le routeur doit
décider — et la seule question qui compte est : **le signal prédit-il quel lecteur va gagner ?**

Le signal candidat est le **meilleur score BM25** des passages du document pour la question.
S'il est haut, les mots de la question sont dans le document : l'extractif suffit. S'il est
bas, la question parle d'autre chose : il faut le modèle.

Ce que ce fichier mesure :
  - l'**AUC du signal** pour l'étiquette « l'extractif bat le modèle » (toutes les questions,
    les deux bancs mélangés) ;
  - l'**exactitude du routeur** au seuil, et le **transfert** : seuil réglé sur un banc, testé
    sur l'autre ;
  - le **regret** contre un oracle qui choisirait toujours le bon lecteur ;
  - les **contrôles** : signal aléatoire, longueur de la question, choix fixes.

Usage :
  python3 tools/routeur.py --json repor
… [3293 caractères tronqués]
  ```

- **bash** `{"command": "test -e reports/rapport-coordination-a.md && echo EXISTS || echo ABSENT; test -e reports/rapport-coordination-a.json && echo EXISTSJSON || echo ABSENTJSON", "description": "Confirm target files are absent"}`

  ```
ABSENT
ABSENTJSON
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "content": "# A — coordination : A6.2 est libre, A8.3b2 est nommée mais hors du graphe\n\n> **Ligne de roadmap** : A (le moteur) · **Tâche** : J4.4 · **Date** : 2026-11-13, 22 h 45 HNE\n> · **Branche** … [30800 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "{\n  \"date\": \"2026-11-13\",\n  \"tache\": \"J4.4\",\n  \"head\": \"dc78f223\",\n  \"branche\": \"s/v7\",\n  \"ligne\": \"A\",\n  \"objet\": \"coordination A — A6.2 et A8.3b2\",\n  \"fiche\": \"reports/rapport-coordination-a.md\",\n  \"verdict\": \"A6.2 n'est pas bloquée : le MoE loca … [18311 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-coordination-a.json >/dev/null && echo JSON-OK; wc -l reports/rapport-coordination-a.md reports/rapport-coordination-a.json", "description": "Validate JSON and count lines"}`

  ```
JSON-OK
  467 reports/rapport-coordination-a.md
  327 reports/rapport-coordination-a.json
  794 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib\np=pathlib.Path('reports/rapport-coordination-a.md')\ntext=p.read_text()\nlinks=re.findall(r'\\]\\(([^)]+)\\)', text)\nbad=[]\nfor l in links:\n    if l.startswith('http'): continue\n    target=(p … [202 caractères tronqués]`

  ```
links 17 bad 0
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "limit": 240}`

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
… [15568 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "offset": 241, "limit": 240}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md</path>
<type>file</type>
<content>
241: 
242: **Ce n'est pas une régression** : les modes 3/4 de `porte-flux.sh` (l. 149–150) portent les
243: références du **chemin lot ≥ 2** (60,8135 / 62,7357). `LOT=1` redonne exactement le mode 0
244: (61,9920 / 58,3200), donc la porte **échoue par construction**. La commande
245: `LOT=1/4 bash tools/porte-flux.sh` citée par `rapport-etat-a.md` § 6 est donc **invalide pour
246: LOT=1** : elle ne peut pas servir d'A/B.
247: 
248: **Le bon harnais** est un A/B direct, avec **deux nœuds** et **deux références par chemin** :
249: 
250: ```bash
251: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
252: M=models/Qwen2.5-0.5B-Q8_0.gguf
253: PORT=49322
254: 
255: # nœud (il sert UNE connexion puis s'arrête : relancer entre lot 1 et lot 4)
256: ./drave-core/target/release/drave "$M" --flux-serveur $PORT --ctx 64 --threads 8 &
257: SRV=$!
258: # attendre « nœud moteur sur » dans le log du nœud
259: 
260: # lot 1 : référence 61,9920 / deux nœuds 61,9920
261: ./drave-core/target/release/drave "$M" --ppl-reparti 127.0.0.1:$PORT \
262:   --couches-locales 12 --limit 24 
… [15091 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "**Lecture, et c'est la décision D2.** Le contrat « coût de routage ÷10 » est **atteint en\noctets lus** par le regroupement par expert **au lot ≥ 64** (÷7,08 à 64, ÷15,51 à 192), et **pa … [938 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "- **aucun** code d'entraînement de routeur appris n'existe dans `tools/` (les outils de routage\n  sont `clusters_moe.py`, `analyse_union_experts.py`, `analyse_reutilisation_experts.py`, … [344 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "**D2 — définir la métrique du « ÷10 ».** Écrire dans la fiche A6.2 : métrique **M1** = octets\nd'experts lus par jeton en préremplissage (lot ≥ 64), cible **÷10** ; métrique **M2** = qua … [1099 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "- **A8.3b2** doit expliquer le **1,90 % f32** (lot 1 vs lot 4) puis le **+7,57 %** du régime\n  1 %. Le second n'est pas une « non-monotonie » : c'est le **KV int8** (`DRAVE_PERTE_MAX`\n … [472 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "Rejeu : **lot 1 = 61,9920 / 61,9920**, **lot 4 = 60,8135 / 60,8135**, le découpage est\n**neutre** (écart 0,00e0). C'est la base de l'instrumentation.", "new_string": "Rejeu : **lot 1 =  … [196 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "3. **Isoler le KV** : rejouer avec `DRAVE_KV_BITS=32` (KV f32) contre `DRAVE_PERTE_MAX=1` (KV\n   int8 sur les 12 premières couches). Si l'écart de 1,90 % disparaît en f32, le seuil int8 … [415 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "5. **Cible** : soit un écart **PPL < 0,05 %** (la tolérance des pins est 5e-4 relative) et une\n   **seule** référence ; soit une **cause nommée** et **deux références par chemin**, ce q … [469 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "**D8 — le défaut reste opt-in.** A8.3 ne passe pas par défaut tant que : (a) les **18/19** pins\nn'ont pas un régime 1 % **dual** (3/19 aujourd'hui : flux, pont, coupe) ; (b) A8.3b2 n'a  … [390 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "| **D2** | métrique du ÷10 = **octets lus** en préremplissage lot ≥ 64 ; qualité ±0,1 ; tok/s secondaire | A | `rapport-a62-moe.md` publie M1/M2/M3 séparément | run qui ne reproduit pas  … [271 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "| **D8** | A8.3 reste **opt-in** jusqu'à 18/19 dual + cause + passe complète | session principale + A | `toutes-les-portes.sh` sous défaut, rouges nommées | défaut qui déplace une porte  … [250 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.json", "old_string": "      \"objet\": \"définir la métrique du ÷10\",\n      \"detail\": \"M1 = octets d'experts lus par jeton en préremplissage lot >= 64 ; M2 = |ΔPPL| <= 0,1 ; M3 = tok/s, secondaire\",\n … [600 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.json has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.json", "old_string": "    \"A6.2 n'est pas mesuré : la fiche ne fait que requalifier la ligne et rassembler les mesures existantes.\",", "new_string": "    \"Le routage appris d'A6.2 n'est pas mesuré : la f … [66 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.json has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/rapport-coordination-a.json >/dev/null && echo JSON-OK; grep -n \"lot ≥ 64\\|M1 est tenue\\|18/19\\|A6.2 n'est pas mesuré\\| tenu\" reports/rapport-coordination-a.md || true; echo '---'; grep -n \"lot 192 … [124 caractères tronqués]`

  ```
JSON-OK
173:**M1 est tenue à 192, pas à 64 ; M3 non**. **Acceptation** : la fiche `rapport-a62-moe.md`
228:  régime 1 % dual (`porte-flux`, `porte-pont`, `porte-coupe`). Le compte 18/19 est lui-même
345:correction qui déplace les 18/19 pins sans les re-épingler.
405:| **D8** | A8.3 reste **opt-in** jusqu'à 18/19 (compte à trancher) dual + cause + passe complète | session principale + A | `toutes-les-portes.sh` sous défaut, rouges nommées | défaut qui déplace une porte non nommée |
---
89:| regroupement par expert, **lot 192** | **74 496 → 4 804** lectures d'experts, **÷15,51** ; borne à l'infini **÷12,1** | `rapport-prefill-par-experts.md` § 2 |
90:| regroupement, **lot 64** | **÷7,08** | idem |
92:| temps de préremplissage, **lot 192** | **×1,58** (le calcul dense et l'ordonnancement deviennent le mur) | idem § 1 |
100:octets lus** par le regroupement par expert **au lot 192** (÷15,51), mais **pas au lot 64**
101:(÷7,08) ; le point de passage entre 64 et 192 (128 par exemple) reste à mesurer. Il n'est **pas
104:est faite » : « octets d'experts lus par jeton en préremplissage, lot 192 » est mesurable et
170:d'experts lus par jeton en préremplissage (cible **÷10**, mesurée à **lot 1
… [452 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nj=json.load(open('reports/rapport-coordination-a.json'))\nassert j['a62']['rejeux']['ppl_c9']['ppl']==37.2013\nassert j['a83b2']['rejeux']['lot_4']['exit']==0\nassert j['a83b2']['rejeux']['lot_1']['exit … [108 caractères tronqués]`

  ```
JSON keys ok 8 decisions
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "```bash\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nM=models/Qwen2.5-0.5B-Q8_0.gguf\nPORT=49322\n\n# nœud (il sert UNE connexion puis s'arrête : relancer entre lot 1 et lot 4)\n … [1554 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "le JSON contient les deux références ou la référence unique. **Ce qui l'invaliderait** : une\ncorrection qui déplace les 18/19 pins sans les re-épingler.", "new_string": "le JSON contien … [143 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '1,80p' tools/revue_documentation.py", "description": "Inspect documentation review script"}`

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
… [1781 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 tools/revue_documentation.py > /tmp/revue-doc-a.log 2>&1; echo \"EXIT=$?\"; grep -n \"coordination-a\\|rapport-coordination\" /tmp/revue-doc-a.log | head -30; echo '--- tail'; tail -30 /tmp/revue-doc-a.log", "desc … [80 caractères tronqués]`

  ```
EXIT=1
--- tail
  revue de documentation · 717 fiche(s) · 811 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 716 fichiers, le disque en a 717
     · compteurs : en-cours.md dit 810 JSON, le disque en a 811
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain | grep -E \"rapport-coordination-a|rapport-coordination-a.json\" ; echo '--- all new reports'; git status --porcelain reports/ | head -20; echo '--- A clean?'; git status --porcelain drave-core data work | head … [61 caractères tronqués]`

  ```
?? reports/rapport-coordination-a.json
?? reports/rapport-coordination-a.md
--- all new reports
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
?? reports/rapport-coordination-a.json
?? reports/rapport-coordination-a.md
?? reports/rapport-coordination-n2.json
?? reports/rapport-coordination-n2.md
?? reports/rapport-coordination-s.json
?? reports/rapport-coordination-s.md
?? reports/rapport-s-paragraphes.md
--- A clean?
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "- **Aucune modification de A** : `drave-core/`, `data/`, `work/` et `docs/pilotage/backlog/`\n  sont intacts. Les rejeux n'écrivent que dans `/tmp` (`/tmp/porte-echange-a.log`,\n  `/tmp/ … [324 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib, json\np=pathlib.Path('reports/rapport-coordination-a.md')\nt=p.read_text()\nprint('fences', t.count('```'), 'even', t.count('```')%2==0)\nprint('lines', len(t.splitlines()))\nbad=[l for l in t.sp … [215 caractères tronqués]`

  ```
fences 4 even True
lines 473
trailing spaces lines 0
json ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib\np=pathlib.Path('reports/rapport-coordination-a.md')\nt=p.read_text()\nlinks=re.findall(r'\\]\\(([^)]+)\\)', t)\nbad=[]\nfor l in links:\n    if l.startswith('http'): continue\n    target=(p.paren … [521 caractères tronqués]`

  ```
links 17 bad []
inline paths 29 missing ['reports/rapport-a62-moe.md', 'reports/rapport-a62-moe.md', 'docs/pilotage/backlog/A8.3b2-instrumentation-lot.md', 'reports/rapport-a83b2-lot.md', 'tools/porte-lot.sh', 'reports/rapport-a62-moe.md']
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "| `reports/rapport-etat-a.md` § 3 et action 3 | **oui** | « à faire — libre », « nommé par la fiche A8.3b, absent du graphe » |\n| `docs/pilotage/backlog/index.md` | **non** | aucune lig … [348 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "**Conclusion** : A8.3b2 est **nommée par une fiche de résultat**, pas par le **graphe**. Le\ngraphe ne peut donc pas la proposer comme frontière — c'est le défaut que `rapport-etat-a.md` … [434 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.json", "old_string": "    \"nommee_par\": [\n      \"reports/rapport-a83b-decision.md:52\",\n      \"reports/a83b-decision.json:42\",\n      \"reports/rapport-etat-a.md (section 3 et action 3)\"\n    ],", " … [245 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.json has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md", "old_string": "| régime | lot 1 | lot ≥ 2 | effet |\n|---|---:|---:|---:|", "new_string": "| régime | lot 1 | lot ≥ 2 | effet du lot |\n|---|---:|---:|---:|"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coordination-a.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && test -f reports/rapport-coordination-a.md && echo FICHE-OK && test -f reports/rapport-coordination-a.json && echo JSON-FILE-OK && python3 -m json.tool reports/rapport-coordination-a.json >/dev/null && echo JSON-VALID && wc -l reports … [109 caractères tronqués]`

  ```
FICHE-OK
JSON-FILE-OK
JSON-VALID
  474 reports/rapport-coordination-a.md
  328 reports/rapport-coordination-a.json
  802 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain drave-core data work docs/pilotage | head -10; echo '--- our files'; git status --porcelain reports/rapport-coordination-a.*", "description": "Confirm A untouched and our files untracked"}`

  ```
M docs/pilotage/references-non-regression.md
--- our files
?? reports/rapport-coordination-a.json
?? reports/rapport-coordination-a.md
  ```

### 🤖 Assistant

Tâche J4.4 terminée. Deux fichiers neufs, **aucune modification de A** (`drave-core/`, `data/`, `work/` intacts) :

- `reports/rapport-coordination-a.md` (474 lignes)
- `reports/rapport-coordination-a.json` (328 lignes, JSON valide)

## Ce que la fiche établit

**A6.2 est libre, pas bloquée.**
- MoE local : `$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf`, **18 556 686 752 o**, **17,28 GiB**, `sha256 6c997b8a…`.
- `bash tools/porte-echange-experts.sh` → **exit 0**, réf. **54,5202** à `N=16`, **768** décisions, routage propre identique, routage étranger **36 074,9497**.
- `--ppl --ctx 512 --limit 32` → **37,2013** reproduit.
- Le blocage est bien la **résidence mono-GPU 16 Go**. Précision ajoutée : le cache VRAM d'experts (`DRAVE_GPU_EXPERTS`) n'est câblé que pour **MXFP4** ; le Q4_K n'y entre pas, même avec 32 Go. Le noyau GPU Q4_K est mesuré (0,171 ms/expert) mais non branché en production.
- Les mesures existantes montrent que le « ÷10 » est tenu **en octets lus au lot 192** (÷15,51), pas au lot 64 (÷7,08), ni en temps (×1,58). Le routage **appris** reste à mesurer.

**A8.3b2 est nommée mais hors du graphe.**
- Nommée dans `rapport-a83b-decision.md`, `a83b-decision.json`, `rapport-etat-a.md` et `semaine-autonome.md` ; absente de `backlog/index.md`, `dependances.md`, `roadmap.md` et `en-cours.md`.
- `LOT=4 bash tools/porte-flux.sh` → **exit 0** (60,8135 / 60,5427) ; `DRAVE_PERTE_MAX=1 LOT=4` → **exit 0** (62,7357 / 64,9228).
- **Correction importante** : `LOT=1 bash tools/porte-flux.sh` → **exit 1**, et c'est normal : les pins des modes 3/4 sont ceux du lot ≥ 2. `LOT=1/4` n'est donc pas un A/B valide. L'A/B manuel `--ppl-reparti` donne bien **61,9920** (lot 1) et **60,8135** (lot 4), découpage neutre.
- Les points d'instrumentation sont listés à `model.rs:5967` (`forward_lot`), `:6085`, `:6110`, `:6328`, `:6352`, `:6523`, `engine.rs:708/726`, et la règle 1 % est une règle **KV** (`model.rs:4711`), pas d'activation.

## Décisions proposées

**D1** requalifier A6.2 dans les docs ; **D2** définir la métrique du ÷10 (octets lus, lot 192) ; **D3** mesurer en offload CPU maintenant, cache Q4_K plus tard ; **D4** écrire `rapport-a62-moe.md` ; **D5** nommer A8.3b2 dans le graphe ; **D6** réparer le harnais `LOT=1` ; **D7** trancher une référence vs deux par chemin ; **D8** laisser A8.3 opt-in.

## Vérifications

- `python3 tools/verifie_backlog.py` → **exit 0**, frontière `(3) : A2.6, N2, N4`.
- `python3 tools/revue_documentation.py` → **exit 1**, uniquement les **2 compteurs** : `en-cours.md` dit 716 fiches / 810 JSON, le disque en a 717 / 811 — l'écart vient des deux fichiers neufs ; à mettre à jour par la session principale.
- Aucun commit effectué ; les deux fichiers sont laissés en `??`, comme les coordinations N2/S/R.

