# Session DSH — relecture

- identifiant : `session-cbce9c66-4423-4a44-a112-b8c9f8b333dc`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 22:35:07
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche T4 (exploitable, 4/5) : la **performance** — mesure `analyser` sur un texte réel de **10 000 mots** (le corpus du dépôt ou un texte assemblé), le **temps** (s), le **débit** (mots/s), la **mémoire** (pic RSS), la **taille du JSON**, et le même sur 100 phrases courtes (le coût fixe par appel) ; compare avec `--tagger` (le coût réseau) ; le **contrôle négatif** : le temps doit croître linéairement avec la taille (pas quadratiquement). Fiche `reports/rapport-performance.md` + JSON, un banc reproductible (`tools/banc_performance.py` ?).

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

- **bash** `{"command": "pwd && ls -la && git status --short | head -50 && git log --oneline -5", "description": "Inspect repo root and git state"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
total 212
drwxr-xr-x. 1 stephane stephane   714 15 nov 22:25 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138 15 nov 22:25 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   220 15 nov 22:35 .git
-rw-r--r--. 1 stephane stephane   653 15 nov 22:25 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 12:34 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-------. 1 stephane stephane   334 15 nov 21:38 pyproject.toml
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 79000 15 nov 22:31 reports
-r
… [2002 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/ reports/ 2>/dev/null | head -100", "description": "List tools and reports directories"}`

  ```
reports/:
total 30044
drwxr-xr-x. 1 stephane stephane   79000 15 nov 22:31 .
drwxr-xr-x. 1 stephane stephane     714 15 nov 22:25 ..
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
-rw-r--r--. 1 steph
… [6124 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"analyser\" --include=*.py -l . | head -30; echo '---'; grep -rn \"tagger\" --include=*.py -l . | head -30", "description": "Find analyser and tagger implementations"}`

  ```
./tools/analyse_flux.py
./tools/trace_compacite.py
./tools/analyse_empreinte.py
./tools/aligneur_litteraire.py
./tools/docwatch/src/docwatch/diagrams.py
./tools/docwatch/src/docwatch/server.py
./tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/util.py
./tools/docwatch/.venv/lib/python3.13/site-packages/pygments/util.py
./tools/tests/linguistique/evaluer_gold.py
./tools/tests/linguistique/juge.py
./tools/tests/linguistique/qualifier_neuronal.py
./tools/tests/linguistique/qualifier_syntagmes.py
./tools/tests/linguistique/qualifier_cascade.py
./tools/tests/linguistique/qualifier_pragmatique.py
./tools/tests/linguistique/miroir.py
./tools/tests/linguistique/qualifier_lien_appris.py
./tools/tests/linguistique/qualifier_quatre_modes.py
./tools/tests/linguistique/classement_cible.py
./tools/tests/linguistique/replis_cible.py
./tools/tests/linguistique/classer_gv.py
./tools/tests/linguistique/qualifier_tagger_612.py
./tools/tests/linguistique/test_bloc_linguistique.py
./tools/tests/linguistique/gold_reel_50.py
./tools/tests/linguistique/qualifier_tagger_h50.py
./tools/tests/linguistique/qualifier_tagger_lot.py
./tools/tests/test_produit_libre.py
./tools/tests/test_sch
… [821 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"analyser\\|tagger\" tools/drave.py | head -80", "description": "Locate analyser and tagger in CLI"}`

  ```
6:    python3 tools/drave.py analyser "Le chat dort."
7:    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
8:    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
9:    python3 tools/drave.py analyser "Le chat dort." --tagger auto     # API si clé, sinon heuristique
12:    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
19:Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
24:En **option** (`--tagger`, `analyser` et `evaluer`), le POS (et lui seul) vient du tagger de
27:`analyser --tagger auto` choisit : API si une clé existe, heuristique sinon, **sans jamais
31:**Sans `--tagger`, le défaut ne change pas** : heuristique, CPU, hors ligne, déterministe.
35:Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger indisponible
67:# Le tagger est une **option** : sans `--tagger`, rien de ce bloc n'est importé ni exécuté.
70:# La fusion de l'option : le POS vient du tagger, tout le reste de l'heuristique. On ne force
95:# --------------------------------------------------------------------------- le tagger
… [4833 caractères tronqués]
  ```

- **bash** `{"command": "wc -l tools/drave.py tools/bloc_linguistique.py tools/tests/test_produit_libre.py tools/tests/linguistique/qualifier_tagger_lot.py 2>/dev/null; ls -la data | head -60", "description": "Check file sizes and data corpus"}`

  ```
1254 tools/drave.py
  3019 tools/bloc_linguistique.py
    75 tools/tests/test_produit_libre.py
   747 tools/tests/linguistique/qualifier_tagger_lot.py
  5095 total
total 961812
drwxr-xr-x. 1 stephane stephane      2664  2 nov 18:33 .
drwxr-xr-x. 1 stephane stephane       714 15 nov 22:25 ..
drwxr-xr-x. 1 stephane stephane       220 22 oct 22:05 adaptateurs
drwxr-xr-x. 1 stephane stephane        32 19 oct 14:30 alignement
-rw-r--r--. 1 stephane stephane  59784525 21 oct 01:02 composition-etats.npz
-rw-r--r--. 1 stephane stephane  30539912 21 oct 03:44 composition-verne-14b-etats.npz
-rw-r--r--. 1 stephane stephane  21144969 21 oct 01:38 composition-verne-7b-etats.npz
-rw-r--r--. 1 stephane stephane  12037642 21 oct 01:30 composition-verne-etats.npz
-rw-r--r--. 1 stephane stephane 151064111 21 oct 23:31 composition-verne-large-etats.npz
-rw-r--r--. 1 stephane stephane 147255554 21 oct 23:47 composition-verne-plan-etats.npz
-rw-r--r--. 1 stephane stephane     97900 29 oct 14:19 consignes_train.jsonl
-rw-r--r--. 1 stephane stephane      1931 29 oct 14:19 consignes_val.jsonl
-rw-r--r--. 1 stephane stephane 100276153  8 oct 09:42 corpus_en.txt
-rw-r--r--. 1 stephane stephane   2032162  8
… [3345 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -i \"perform\\|banc\\|bench\" ; echo '---'; ls bench; echo '---'; sed -n '1,120p' docs/pilotage/en-cours.md", "description": "Look for existing perf work and current state"}`

  ```
pensee-banc.json
r02-banc-lecture.json
r03-banc-durci-extractif.json
r03-banc-durci-modele.json
r03-banc-extractif.json
r03-banc-modele.json
rapport-pensee-banc.md
rapport-r03-banc-complet.md
rapport-r03-banc-durci.md
---
cpu_aer.c
cpu_merge.c
---
# En ce moment

**Mis à jour : 2026-11-15, 22 h 26 HNE (T3 : le démarrage)**

> **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs.
- **Prochaine action** : **suivi docs**, puis la **passe**.
- **État** : **en pause** depuis le 05/11 ; la clôture J14.1 est portée par `e181ce02`.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/
… [9912 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"T4\" docs/pilotage docs/methode journal/sessions 2>/dev/null | grep -i \"perform\\|T4\" | head -40", "description": "Find T4 task definition"}`

  ```
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:3201:- **T4** `/dev/nvme0n1p2  828G  243G  586G  30% /home`
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:3202:- **T4** `Creating uninstaller 25%`
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:3203:- **T4** `Creating uninstaller 50%`
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:3204:- **T4** `Creating uninstaller 75%`
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:3205:- **T4** `Creating uninstaller 100%`
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:3329:- **T4** : === options de quartus_sh liées aux devices ===  === test : quartus_sh --list_parts === Error (23024): Unknown long option --list_parts. Refer to --help for legal options  Usage: ------   === test : r
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:3330:- **T4** : === requête Tcl : parties Stratix V connues === Info: Command: quartus_sh -t "puts PARTLIST_BEGIN; foreach p [get_part_list -family Stratix" "V] { if {[string match 5SGSMD5* ]} { puts  } }; puts PARTL
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/rapport.md:3331:- **T4** : === s
… [7277 caractères tronqués]
  ```

- **bash** `{"command": "ls docs/pilotage/; echo '---'; find docs/pilotage -maxdepth 2 -type f -name \"*.md\" | head -40; echo '---'; grep -rn \"10 000 mots\\|10000 mots\\|banc_performance\\|performance\" docs/pilotage docs/methode 2>/dev/null | head -40", "description": "Search for performance bench spec"}`

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
semaine-2.md
semaine-autonome.md
utilisation.md
---
docs/pilotage/manques.md
docs/pilotage/utilisation.md
docs/pilotage/backlog/R03-banc-lecture-rapide.md
docs/pilotage/backlog/R41-bloc-tableaux.md
docs/pilotage/backlog/R42-bloc-code.md
docs/pilotage/backlog/R43-bloc-maths.md
docs/pilotage/backlog/R44-encodeur-visuel.md
docs/pilotage/backlog/B12.10-pipeline-m1-m4-m8.md
docs/pilotage/backlog/_modele.md
docs/pilotage/backlog/R02-controleur-lecture.md
docs/pilotage/backlog/R04-tete-survol.md
docs/pilotage/backlog/R05-tete-balayage.md
docs/pilotage/backlog/R06-tete-relecture.md
docs/pilotage/backlog/R12-curriculum-contexte.md
docs/pilotage/backlog/R21-memoire-travail-gist.md
docs/pilotage/backlog/R22-memoire-episodique.md
docs/pilotage/backlog/R32-citations-provenance.md
docs/pilotage/backlog/R51-lecture-croisee.md
docs/pilotage/backlog/R52-multilingue-decodeur.md
docs/pilotage/backlog/N0.3b-parite-ppl.md
docs/pilotage/backlog/B10.3-raisonnement-z.md
docs/pilotage/backlog/B11.10-cartes-ambiguites.md
docs/pilotage/backlog/A3.4-colab.md
docs/pilotage/backlog/A5.4-f
… [970 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' tools/drave.py", "description": "Read drave CLI header"}`

  ```
#!/usr/bin/env python3
"""drave.py — le point d'entrée produit du bloc linguistique.

Une seule commande, quatre gestes, hors ligne et déterministe :

    python3 tools/drave.py analyser "Le chat dort."
    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
    python3 tools/drave.py analyser "Le chat dort." --tagger auto     # API si clé, sinon heuristique
    python3 tools/drave.py evaluer
    python3 tools/drave.py evaluer --gold --json
    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
    python3 tools/drave.py restituer "Le chat dort."
    python3 tools/drave.py restituer "Le chat dort." --roles
    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
    python3 tools/drave.py --version

Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et la
**
… [6445 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"exploitable\" docs/pilotage journal/sessions/*/plan.md 2>/dev/null | head -40; echo '---'; grep -rln \"T1.*T2\\|T3.*T4\\|T4\" docs/pilotage/plan-travail.md docs/pilotage/semaine-2.md docs/pilotage/roadmap.md 2>/dev/null", "description": "Find exploitable task series"}`

  ```
---
[exit code: 1]
  ```

- **bash** `{"command": "sed -n '1,200p' docs/pilotage/plan-travail.md", "description": "Read work plan"}`

  ```
# Le plan de travail — plusieurs sessions sur une même machine

> **Ce que ce document est.** Le **pont** entre l'état ([`en-cours.md`](en-cours.md), ce qui se
> passe maintenant) et l'ordre ([`roadmap.md`](roadmap.md), ce qu'il faut faire et dans quel
> ordre) : **qui fait quoi, dans quel territoire, à quelle cadence, et comment on surveille les
> fichiers qui bougent**. Il ne remplace ni l'un ni l'autre : l'état reste la source du présent,
> la roadmap la source de l'ordre.
>
> **Date** : 2026-11-02. **Machine** : une seule — 40 cœurs, 125 Go de RAM, 2 GPU de 16 Go,
> 2,0 To libres sur `Data13TB`, 34 Go sur `IA`. **Capacité** : voir
> [`chantiers.md`](chantiers.md) § 8 (4 sessions, 4 à 6 chantiers, 2 à 4 sous-agents par session).
>
> **Chargement** : ce document avant d'ouvrir une session ; puis la fiche du chantier.

## 1. Où ce plan se situe

```
en-cours.md          ce qui se passe maintenant (état court, une section par session active)
plan-travail.md      qui fait quoi, où, à quelle cadence (ce document)
roadmap.md           l'ordre des chantiers et leur état
chantiers.md         les relations entre les chantiers, la vision, la capacité
backlog/             les contrats par 
… [16182 caractères tronqués]
  ```

- **bash** `{"command": "git log --all --oneline --grep='T4\\|performance\\|PERFORMANCE' | head -30", "description": "Search git history for T4"}`

  ```
a20de579 PENSÉE v0 — LE STATE STORE EXISTE ET TIENT SES SIX PORTES
481083ee PENSÉE v0 — LE STATE STORE EXISTE ET TIENT SES SIX PORTES
87a841ae C8 : une tete ENTRAINEE pour sa profondeur — 845,45 contre 456 586,60 (div 540) sur le meme texte
5e53c744 Bloc 0-9 : première borne d'approximabilité — 19 % de la variance après dix couches avec DEUX directions
b0c14b95 K3 : les quatre premières couches COMPOSÉES (0 dense, 1-2 MoE, 3 MLA) — la chaîne vérifiée, pas seulement les pièces
  ```

- **bash** `{"command": "sed -n '400,660p' tools/drave.py", "description": "Read analyser formatting and command"}`

  ```
if len(v) <= largeur:
        return v
    return v[: max(1, largeur - 1)].rstrip() + "…"


def _envelopper(prefixe: str, contenu: str, largeur: int = LARGEUR) -> list[str]:
    """Coupe une ligne trop longue en gardant l'alignement sous le préfixe."""
    lignes = textwrap.wrap(contenu, width=max(20, largeur - len(prefixe)),
                           break_long_words=False, break_on_hyphens=False) or [""]
    return [prefixe + lignes[0]] + [" " * len(prefixe) + ligne for ligne in lignes[1:]]


class _Formateur(argparse.RawDescriptionHelpFormatter):
    """Une aide de largeur fixe : la sortie ne dépend pas de la taille du terminal."""

    def __init__(self, prog: str, **kwargs):
        kwargs.setdefault("width", LARGEUR)
        super().__init__(prog, **kwargs)


def formater_annotation(a: bl.Annotation, tagger: bool = False,
                        stats: dict | None = None, titre: str | None = None) -> str:
    """La sortie lisible : POS compact, syntagmes (rôle + cible), pragmatique, couverture.

    Avec `--tagger`, l'en-tête le dit, le coût de l'API est affiché et un refus du tagger est
    nommé — le JSON d'annotation, lui, garde exactement le même contrat. `titre` permet 
… [10500 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '660,900p' tools/drave.py", "description": "Read analyser command implementation"}`

  ```
return round(justes / len(cibles), 4)


def _pct(valeur: float) -> str:
    return f"{100.0 * float(valeur):.2f} %"


def _points(delta: float) -> str:
    """Un écart de taux en **points** de pourcentage, avec son signe."""
    return f"{100.0 * float(delta):+.2f} pts"


def _formater_evaluation(rapport: dict) -> str:
    gold = rapport["gold"]
    mesure = rapport["heuristique"]
    pos = mesure["pos"]
    syn = mesure["syntagme"]
    tete = syn["tete"]
    att = mesure["attachement"]
    att_tete = mesure["attachement_tete"]
    prag = mesure["pragmatique"]
    controle = rapport["controle_negatif"]
    lignes = [
        f"{NOM} {VERSION} — évaluation de l'heuristique sur le gold",
        f"gold {gold['nom']} · {gold['phrases']} phrases · {gold['tokens']} tokens · "
        f"{gold['cibles_attachement']} cibles d'attachement",
        "",
        f"POS         exactitude {_pct(pos['exactitude'])}  "
        f"(fermé {_pct(pos['exactitude_ferme'])}, ouvert {_pct(pos['exactitude_ouvert'])})",
        f"SYNTAGMES   F1 {_pct(syn['f1'])}  "
        f"(P {_pct(syn['precision'])} / R {_pct(syn['rappel'])})",
        f"  tête      F1 {_pct(tete['f1'])}  "
        f"(P {_pct(tete['prec
… [11068 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' docs/methode/resultats.md", "description": "Read result method doc"}`

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

- **bash** `{"command": "sed -n '255,400p' tools/drave.py", "description": "Read tagger cost accounting"}`

  ```
return (f"{NOM} {VERSION} — analyse heuristique "
                    f"(tagger auto : repli après échec de l'API)")
        if (self.stats or {}).get("appels", 0):
            return f"{NOM} {VERSION} — analyse cascade POS (tagger auto : API DeepSeek, réseau)"
        return f"{NOM} {VERSION} — analyse heuristique (tagger auto : API disponible, non appelée)"


def _transport_tagger(client, stats: dict):
    """Le transport attendu par les taggers : invite → contenu, avec le coût mesuré."""

    def transport(invite: str, _grammaire: str, max_jetons: int) -> str:
        stats["appels"] += 1
        try:
            reponse = client.demande(invite, temperature=0.0,
                                     max_tokens=max(64, int(max_jetons or 256)))
        except Exception as exc:  # noqa: BLE001 — le code HTTP décide du destin de l'option
            # 401/403 : la clé est refusée, aucune phrase ne peut être taguée. On retient le
            # code pour que `_CascadeTagger` arrête le run au lieu de publier un repli muet.
            code = getattr(exc, "code", None)
            if code in (401, 403):
                stats["cle_refusee"] = int(code)
            raise
        if getattr
… [6043 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def _mots\\|def _phrases\\|def analyser\\|class Heuristique\\|def json\" tools/bloc_linguistique.py | head -40; echo '---'; sed -n '1,120p' tools/bloc_linguistique.py", "description": "Inspect heuristic API"}`

  ```
69:    def json(self) -> dict:
87:    def json(self) -> dict:
149:    def json(self, avec_duree: bool = False) -> dict:
168:    def analyser(self, texte: str, langue: str | None = None,
835:class Heuristique:
867:    def _mots(texte: str) -> list[tuple[int, int, str, str]]:
886:    def _phrases(texte: str) -> list[tuple[int, int, str, str]]:
1561:    def analyser(self, texte: str, langue: str | None = None,
1956:    def analyser(self, texte: str, langue: str | None = None,
2027:    def analyser(self, texte: str, langue: str | None = None,
2137:    def analyser(self, texte: str, langue: str | None = None,
2271:    def analyser(self, texte: str, langue: str | None = None,
2363:    def analyser(self, texte: str, langue: str | None = None,
2441:    def analyser(self, texte: str, langue: str | None = None,
2769:    def analyser(self, texte: str, langue: str | None = None,
2797:    def analyser(self, texte: str, langue: str | None = None,
---
#!/usr/bin/env python3
"""bloc_linguistique.py — le bloc d'étiquetage linguistique, du graphème à la pragmatique.

Un seul contrat (`BlocLinguistique.analyser`) et **plusieurs implémentations** :

  - `Heuristique` : CPU, déterministe, ultra-rapide 
… [4541 caractères tronqués]
  ```

- **bash** `{"command": "ls -la data/corpus_propre data/corpus_litt_propre data/corpus_repo_propre 2>/dev/null; echo '---'; find data -maxdepth 2 -iname '*verne*' -o -iname '*litt*' | head -30; echo '---'; head -c 600 data/corpus_fr_litterature.txt", "description": "Inspect corpus candidates"}`

  ```
data/corpus_litt_propre:
total 16624
drwxr-xr-x. 1 stephane stephane       48 31 oct 22:24 .
drwxr-xr-x. 1 stephane stephane     2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane   843776 31 oct 22:24 test.txt
-rw-r--r--. 1 stephane stephane 15332926 31 oct 22:24 train.txt
-rw-r--r--. 1 stephane stephane   843776 31 oct 22:24 val.txt

data/corpus_propre:
total 7364
drwxr-xr-x. 1 stephane stephane     122  3 nov 02:03 .
drwxr-xr-x. 1 stephane stephane    2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane  320314 31 oct 22:21 dev.txt
-rw-r--r--. 1 stephane stephane  180224  3 nov 02:03 test.canal
-rw-r--r--. 1 stephane stephane  180224 31 oct 22:20 test.txt
-rw-r--r--. 1 stephane stephane 3244858  2 nov 23:07 train.canal
-rw-r--r--. 1 stephane stephane 3244858 31 oct 22:20 train.txt
-rw-r--r--. 1 stephane stephane  180224  2 nov 23:07 val.canal
-rw-r--r--. 1 stephane stephane  180224 31 oct 22:20 val.txt

data/corpus_repo_propre:
total 5708
drwxr-xr-x. 1 stephane stephane      62  1 nov 07:11 .
drwxr-xr-x. 1 stephane stephane    2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane  483328  1 nov 07:11 dev.txt
-rw-r--r--. 1 stephane stephane  262144  1 nov 07:11 test.txt
-rw-r--r
… [1035 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '835,930p' tools/bloc_linguistique.py; echo '---'; sed -n '1561,1700p' tools/bloc_linguistique.py", "description": "Read heuristic analyser internals"}`

  ```
class Heuristique:
    """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""

    nom = "heuristique"

    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
                 seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
                 union: bool = True, partition: str = "alternative"):
        self.profils = profils
        self.segmenter_s = segmenter_s
        self.seuil_ouvert = seuil_ouvert
        self.seuil_langue = seuil_langue
        self.union = union
        # "brut" : la sortie d'avant (chevauchements non documentés) ; "alternative" :
        # les deux segments restent, `meta.alternative` dit lequel est préféré ;
        # "filtrer_union" : on retire le S qui **contient** un segment chunker (le filtre
        # union du P0-3) ; "filtrer" : partition stricte, le chunker est la partition.
        # Dans les deux filtres, le segment retiré reste dans `meta.alternative` (`retire`).
        if partition not in ("brut", "alternative", "filtrer_union", "filtrer"):
            raise ValueError("partition attend 'brut', 'alternative', 'filtrer_union' ou 'filtrer'")
        self.partition =
… [12335 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '120,200p' tools/bloc_linguistique.py", "description": "Read Annotation json contract"}`

  ```
# chevauchent). Le format reste additif ; le vérificateur lit encore les annotations v1.
VERSION_ANNOTATION = 2


@dataclass
class Annotation:
    texte: str
    langue: str = "und"
    script: str = SCRIPT_NEUTRE
    etiquettes: list[Etiquette] = field(default_factory=list)
    refus: str = ""
    trace: list[dict] = field(default_factory=list)
    cout: dict = field(default_factory=dict)
    unites_semantiques: list[Span] = field(default_factory=list)
    fraction_semantique: float = 0.0
    source: str = "heuristique"
    contexte: str = ""

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
            cout.pop("duree_s", No
… [1920 caractères tronqués]
  ```

- **bash** `{"command": "command -v /usr/bin/time && /usr/bin/time --version 2>&1 | head -2; echo '---'; python3 - <<'PY'\nimport os, pathlib\np=pathlib.Path.home()/'.config/drave/deepseek.key'\nprint('keyfile', p.exists(), p.stat().st_size if p.exists() else 0)\nprint('env DEEPSEEK_API_KEY', bool(os.environ.ge … [162 caractères tronqués]`

  ```
/usr/bin/time
time (GNU Time) 1.10
Copyright (C) 2026 Free Software Foundation, Inc.
---
keyfile True 36
env DEEPSEEK_API_KEY False
env DEEPSEEK_KEY_FILE False
  ```

- **bash** `{"command": "for f in data/corpus_litt_propre/test.txt data/corpus_propre/test.txt data/corpus_repo_propre/test.txt; do echo \"=== $f\"; wc -c \"$f\"; head -c 500 \"$f\"; echo; done", "description": "Inspect clean corpora heads"}`

  ```
=== data/corpus_litt_propre/test.txt
843776 data/corpus_litt_propre/test.txt
 eut
retrouvé et qu'on leur eut rendu leurs ardoises et leurs crayons,
ils se mirent fort diligemment à écrire l'histoire de l'accident, à
l'exception du Lézard, qui paraissait trop accablé pour faire autre
chose que demeurer la bouche ouverte, les yeux fixés sur le plafond de
la salle.

"Que savez-vous de cette affaire-là?" demanda le Roi à Alice.

"Rien," répondit-elle.

"Rien absolument?" insista le Roi.

"Rien absolument," dit Alice.

"Voilà qui est très-important," dit le Roi, s
=== data/corpus_propre/test.txt
180224 data/corpus_propre/test.txt
guistique ». Ce niveau existe, il est
mesurable, il tient en 157 canaux sur 896, et il est nettement plus invariant que
6.4 Ce que ça laisse ouvert
La hiérarchie trouvée ([41, 15, 8, 8, 8]) n'a pas encore été soumise à
Le seuil de restriction (50 %, 75 %…) n'a pas été optimisé : c'est un curseur,
Les 218 canaux propres à certaines langues n'ont pas été examinés pour
eux-mêmes : ils portent peut-être une information utile qu'on jette.
7. L'invariant : le pont apporte +0,020, que
=== data/corpus_repo_propre/test.txt
262144 data/corpus_repo_propre/test.txt
eux gra
… [476 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re\nfor p in ['data/corpus_litt_propre/test.txt','data/corpus_propre/test.txt','data/corpus_repo_propre/test.txt','data/corpus_fr_litterature.txt']:\n    s=open(p,encoding='utf-8',errors='replace').read()\n    mots=re.findall(r\"\\w+(?:['’\\-]\\w+)*\",s)\n    pr … [129 caractères tronqués]`

  ```
data/corpus_litt_propre/test.txt chars 817280 words approx 136387 lines 17370
data/corpus_propre/test.txt chars 172882 words approx 29296 lines 1973
data/corpus_repo_propre/test.txt chars 252898 words approx 38385 lines 4363
data/corpus_fr_litterature.txt chars 16502139 words approx 2751154 lines 350641
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\ns=open('data/corpus_litt_propre/test.txt',encoding='utf-8',errors='replace').read()\nph=bl.Heuristique._phrases(s)\nprint('sentences',len(ph))\nfor p in ph[:8]: print(p[2], repr(s[p[0]:p[1]][:90])) … [122 caractères tronqués]`

  ```
sentences 7720
eut
retrouvé et qu'on leur eut rendu leurs ardoises et leurs crayons,
ils se mirent fort diligemment à écrire l'histoire de l'accident, à
l'exception du Lézard, qui paraissait trop accablé pour faire autre
chose que demeurer la bouche ouverte, les yeux fixés sur le plafond de
la salle. "eut\nretrouvé et qu'on leur eut rendu leurs ardoises et leurs crayons,\nils se mirent fort d"
"Que savez-vous de cette affaire-là? '"Que savez-vous de cette affaire-là?'
" demanda le Roi à Alice. '" demanda le Roi à Alice.'
"Rien," répondit-elle. '"Rien," répondit-elle.'
"Rien absolument? '"Rien absolument?'
" insista le Roi. '" insista le Roi.'
"Rien absolument," dit Alice. '"Rien absolument," dit Alice.'
"Voilà qui est très-important," dit le Roi, se tournant vers les jurés. '"Voilà qui est très-important," dit le Roi, se tournant vers les jurés.'
last Si vous l'exigez, c'est par moi que passeront les
assurances de son profond respect et de son désespoir de vo "Si vous l'exigez, c'est par moi que passeront les\nassurances de son profond respect et de "
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, re\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\ns=open('data/corpus_litt_propre/test.txt',encoding='utf-8',errors='replace').read()\n# exact first 10000 word tokens\nmots=[m for m in bl.Heuristique._mots(s) if m[3] in ('mot','nombre')]\nprin … [669 caractères tronqués]`

  ```
total word-ish 141996
chars 56284 words 10000
sentences 485
short 3-12 167
total words short100 680
'"Que savez-vous de cette affaire-là?'
'" demanda le Roi à Alice.'
'" insista le Roi.'
'"Rien absolument," dit Alice.'
'"Voilà qui est très-important," dit le Roi, se tournant vers les jurés.'
  ```

- **bash** `{"command": "time python3 tools/drave.py analyser \"Le chat dort sur le toit.\" --tagger --json > /tmp/tagger_test.json 2> /tmp/tagger_test.err; echo \"rc=$?\"; cat /tmp/tagger_test.err; echo '--- bytes'; wc -c /tmp/tagger_test.json; head -c 500 /tmp/tagger_test.json", "description": "Test one tagge … [33 caractères tronqués]`

  ```
rc=0
drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=1 · tokens=0 · latence=0.0 s
--- bytes
10816 /tmp/tagger_test.json
{
 "schema": "drave.annotation",
 "version": 2,
 "texte": "Le chat dort sur le toit.",
 "langue": "fr",
 "script": "Latn",
 "source": "cascade",
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
   "sou
[stderr]

real	0m0,196s
user	0m0,169s
sys	0m0,024s
  ```

- **bash** `{"command": "grep -n \"cache\\|latence\" tools/llm/deepseek.py | head -60; echo '---'; sed -n '1,180p' tools/llm/deepseek.py", "description": "Inspect DeepSeek client cache behavior"}`

  ```
14:dans le dépôt, dans un cache ou dans un message d'erreur. Il ne dépend d'aucun
21:- cache : `data/deepseek/cache/<sha256>.json` (gitignoré), clé = modèle + messages
44:CACHE_DEFAUT = RACINE / "data" / "deepseek" / "cache"
65:    latence_s: float = 0.0
66:    cache: bool = False
96:def _cache_cle(modele: str, messages: list[dict], temperature: float,
128:                 modele: str | None = None, cache_dir: str | pathlib.Path | None = None,
137:        self.cache_dir = pathlib.Path(cache_dir or os.environ.get("DEEPSEEK_CACHE")
151:    def _lire_cache(self, cle: str) -> ReponseDeepSeek | None:
152:        chemin = self.cache_dir / f"{cle}.json"
163:                               latence_s=float(d.get("latence_s", 0.0)),
164:                               cache=True, brut=d.get("brut"))
166:    def _ecrire_cache(self, cle: str, r: ReponseDeepSeek) -> None:
168:            self.cache_dir.mkdir(parents=True, exist_ok=True)
169:            (self.cache_dir / f"{cle}.json").write_text(json.dumps({
171:                "raisonnement": r.raisonnement, "latence_s": r.latence_s,
176:            # un cache indisponible ne doit pas faire échouer une mesure
183:                cache: bool = Tr
… [8123 caractères tronqués]
  ```

- **bash** `{"command": "find . ~/.cache -maxdepth 4 -iname '*deepseek*' -o -iname '*tagger*cache*' 2>/dev/null | head -30", "description": "Find tagger cache files"}`

  ```
./reports/deepseek-mesures.json
./reports/deepseek-mesures-300.json
./reports/deepseek-natif-300.json
./reports/rapport-deepseek.md
./data/deepseek
./tools/llm/deepseek.py
./tools/llm/tests/test_deepseek.py
./tools/llm/__pycache__/deepseek.cpython-313.pyc
./tools/porte-deepseek.sh
./journal/2026-10-26/deepseek.md
./docs/archive/plan-deepseek-v4-flash.md
./docs/archive/plan-deepseek41-complet.md
./work/portes/passe-1102-19h32/porte-deepseek.log
./work/portes/passe-1102-19h32/deepseek-porte
./work/portes/passe-0303-04h10/porte-deepseek.log
./work/portes/passe-0303-04h10/deepseek-porte
./work/portes/passe-0303-11h30/porte-deepseek.log
./work/portes/passe-0303-11h30/deepseek-porte
./work/portes/passe-1104-08h00/porte-deepseek.log
./work/portes/passe-1104-08h00/deepseek-porte
./work/portes/passe-2404-23h45/porte-deepseek.log
./work/portes/passe-2404-23h45/deepseek-porte
./work/portes/passe-1311-23h15/porte-deepseek.log
./work/portes/passe-1311-23h15/deepseek-porte
./work/portes/passe-1402-02h00/porte-deepseek.log
./work/portes/passe-1402-02h00/deepseek-porte
./work/portes-1106-01h28/porte-deepseek.log
./work/portes-1107-01h43/porte-deepseek.log
./work/portes-1107-02h09/porte-deepseek.lo
… [49 caractères tronqués]
  ```

- **bash** `{"command": "rm -rf /tmp/ds_cache_test; time DEEPSEEK_CACHE=/tmp/ds_cache_test python3 tools/drave.py analyser \"Le chat dort sur le toit.\" --tagger --json > /tmp/tagger_test.json 2> /tmp/tagger_test.err; echo \"rc=$?\"; cat /tmp/tagger_test.err; ls -la /tmp/ds_cache_test 2>/dev/null | head", "desc … [75 caractères tronqués]`

  ```
rc=0
drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=149 · latence=1.2 s
total 4
drwxr-xr-x.   2 stephane stephane    60 15 nov 22:36 .
drwxrwxrwt. 561 root     root     30500 15 nov 22:36 ..
-rw-r--r--.   1 stephane stephane  1064 15 nov 22:36 9e5116c34e54111d65df585da2295dfacb709d0fd0db57412c4703183c8dd5e8.json
[stderr]

real	0m1,422s
user	0m0,324s
sys	0m0,034s
  ```

- **bash** `{"command": "grep -n \"T1\\|T2\\|T3\\|T4\\|quickstart\\|contrat-json\\|performance\" docs/pilotage/roadmap.md docs/pilotage/en-cours.md docs/pilotage/backlog/index.md 2>/dev/null | head -80", "description": "Find roadmap line for T tasks"}`

  ```
docs/pilotage/roadmap.md:31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observ
… [6726 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat 7d114559 | head -60; echo '---'; git show --stat 7f1519f7 | head -60", "description": "Inspect T3 and T2 commits"}`

  ```
commit 7d114559dad6fdb76d07c8c709c9e8fe469f4504
Author: Stéphane <stephane@localhost>
Date:   Sun Nov 15 22:31:59 2026 -0500

    T3 — LE DÉMARRAGE EN 5 MINUTES : 3/3 COMMANDES REJOUÉES, JSON V2 5 899 OCTETS, TAGGER 4/0, ERREURS 3/4/1 ; LE CLONE PUBLIC SANS tools/structures EST DÉGRADÉ, DOCUMENTÉ
    
    Clone public neuf (7f1519f, Python 3.13.16, pip 26.2.1, sans clé) : clone + venv + install = 13,64 s ; drave --version, analyser, evaluer sortent 0 ; JSON 5 899 octets, 20 étiquettes, schéma v2 ; --tagger sans clé 4, --tagger auto 0 ; texte vide 3, fichier absent 1, langue invalide 2. Contrôle négatif « débutant sans le dépôt » : les commandes passent, mais tools/structures (URL locale dans .gitmodules) manque au clone public ; analyser rend objet/— au lieu de agent/chat, evaluer 81,88/88,70 au lieu de 79,02/99,58. Le quickstart affiche la sortie réelle du clone et nomme l'écart ; la correction du sous-module reste à faire. Fiche reports/rapport-quickstart.md + reports/quickstart.json.

 .gitignore                                         |    1 +
 docs/README.md                                     |    7 +-
 docs/pilotage/en-cours.md                          |   17 +-
 docs/produi
… [4093 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' reports/rapport-quickstart.md; echo '--- JSON'; sed -n '1,120p' reports/quickstart.json", "description": "Read T3 report style"}`

  ```
# T3 — le démarrage en 5 minutes : clone public, installation, trois commandes, JSON, tagger, erreurs

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T3** (exploitable, 3/5) ·
> **Date** : 2026-11-15 · **Verdict** : ✅ **quickstart livré et rejoué** ; ⚠️ le **clone
> public** n'a pas le sous-module `tools/structures`, donc la sortie d'un débutant est
> **dégradée** par rapport au dépôt de développement. Le document le dit, mesure l'écart et
> donne les deux sorties.
>
> **Le chiffre.** Sur un clone public neuf (commit **7f1519f**, Python **3.13.16**, pip
> **26.2.1**, sans clé) : **3/3 commandes** sortent **0**, le JSON fait **5 899 octets** en
> schéma **v2**, `--tagger` sans clé sort **4**, `--tagger auto` sort **0**, et les **3
> erreurs** rejouées sortent **3 / 4 / 1**. Clone + venv + installation : **13,64 s** de
> machine. Le contrôle négatif « un débutant sans le dépôt » passe pour les commandes, mais
> découvre l'écart du sous-module : `analyser` rend `rôle=objet` / `GV → —` au lieu de
> `agent` / `chat`, et `evaluer` **81,88 %** / **88,70 %** au lieu de **79,02 %** / **99,58 %**.
>
> **Dispositif** : [`docs/produit/demarrage.md`](../docs/produit/demarrage.md),
>
… [12081 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"produit\\|T1\\|T2\\|T3\\|quickstart\" docs/pilotage/roadmap.md | head -40; echo '---'; sed -n '145,175p' docs/pilotage/roadmap.md; echo '---'; sed -n '250,310p' docs/pilotage/roadmap.md", "description": "Inspect roadmap product lines"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [29049 caractères tronqués]
  ```

- **bash** `{"command": "ls journal/2026-11-15/; echo '---'; sed -n '1,120p' journal/2026-11-15/README.md; echo '--- mesures'; sed -n '1,160p' journal/2026-11-15/mesures.md", "description": "Inspect journal day structure"}`

  ```
distribue.md
docs.md
memoire.md
mesures.md
modele.md
outils.md
portes.md
README.md
---
# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**48 commits** · **1 session(s)** · **7 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 8 | [distribue.md](distribue.md) |
| docs | 13 | [docs.md](docs.md) |
| memoire | 3 | [memoire.md](memoire.md) |
| mesures | 17 | [mesures.md](mesures.md) |
| modele | 3 | [modele.md](modele.md) |
| outils | 1 | [outils.md](outils.md) |
| portes | 3 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 365.8 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réel
… [21853 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' docs/pilotage/en-cours.md; echo '--- fin'; tail -80 docs/pilotage/en-cours.md", "description": "Read full current state file"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 22 h 26 HNE (T3 : le démarrage)**

> **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs.
- **Prochaine action** : **suivi docs**, puis la **passe**.
- **État** : **en pause** depuis le 05/11 ; la clôture J14.1 est portée par `e181ce02`.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.

… [19497 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo \"rc=$?\"", "description": "Run doc review baseline"}`

  ```
revue de documentation · 762 fiche(s) · 856 JSON · 125 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
rc=0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,time,json,resource,hashlib\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\ns=open('data/corpus_litt_propre/test.txt',encoding='utf-8',errors='replace').read()\nmots=[m for m in bl.Heuristique._mots(s) if m[3] in ('mot','nombre')]\nt=s[:mots[9999 … [568 caractères tronqués]`

  ```
duree 3.0978960070060566 mots/s 3227.9973173355297 rss_kb 149368
json bytes 13796340 labels 51156 unites 6245 phrases 485
sha 93d5755272051cb4
  ```

- **bash** `{"command": "python3 -V; nproc; free -h | head -3; lscpu | grep -E 'Model name|CPU\\(s\\)|Thread|Core|Socket' | head -8; uname -a", "description": "Collect machine info"}`

  ```
Python 3.13.16
40
               total        used        free      shared  buff/cache   available
Mem:           125Gi        24Gi        13Gi       9,1Gi        98Gi       101Gi
Swap:           62Gi       292Mi        62Gi
CPU(s):                                  40
On-line CPU(s) list:                     0-39
Model name:                              Intel(R) Xeon(R) CPU E5-2687W v3 @ 3.10GHz
Thread(s) per core:                      2
Core(s) per socket:                      10
Socket(s):                               2
CPU(s) scaling MHz:                      56%
NUMA node0 CPU(s):                       0-9,20-29
Linux Hauru 7.2.6-1-default #1 SMP PREEMPT_DYNAMIC Tue Sep 15 06:50:07 UTC 2026 (3d19f11) x86_64 x86_64 x86_64 GNU/Linux
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,time,json,resource,statistics\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\ns=open('data/corpus_litt_propre/test.txt',encoding='utf-8',errors='replace').read()\nmots=[m for m in bl.Heuristique._mots(s) if m[3] in ('mot','nombre')]\nt=s[:mots[9 … [969 caractères tronqués]`

  ```
n 100 mots 680
total 0.11204247700516135 median_ms 1.0281145223416388 mean_ms 1.1204247700516135 max_ms 4.737477982416749
json total 1439810 mean 14398.1 max 31296
rss_kb 62808
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,time,json,resource,math,statistics\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\ns=open('data/corpus_litt_propre/test.txt',encoding='utf-8',errors='replace').read()\nallm=[m for m in bl.Heuristique._mots(s) if m[3] in ('mot','nombre')]\nh=bl.H … [282 caractères tronqués]`

  ```
250 0.0538 4648.4 1485
500 0.1155 4327.6 3021
1000 0.327 3058.3 5946
2000 1.0334 1935.4 11825
4000 0.7648 5229.8 21971
8000 2.1083 3794.6 41693
10000 3.0138 3318.1 51156
  ```

- **bash** `{"command": "sed -n '2360,2520p' tools/bloc_linguistique.py; echo '---'; sed -n '2520,2680p' tools/bloc_linguistique.py", "description": "Inspect Cascade and neuronal tagger"}`

  ```
self.chunks = chunks
        self.pragma = pragma

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        a = self.pos.analyser(texte, langue, contexte)
        b = self.chunks.analyser(texte, langue, contexte)
        c = self.pragma.analyser(texte, langue, contexte) if self.pragma else None
        etiquettes = a.etiquettes + b.etiquettes + (c.etiquettes if c else [])
        refus = "; ".join(x for x in (a.refus, b.refus, c.refus if c else "") if x)
        lg = a.langue if a.langue != "und" else b.langue
        script = a.script if a.script != SCRIPT_NEUTRE else b.script
        return Annotation(
            texte=texte, langue=lg, script=script, etiquettes=etiquettes,
            source=self.nom, refus=refus,
            trace=a.trace + b.trace + (c.trace if c else []) + [
                {"etape": "compose",
                 "niveaux": sorted({e.niveau for e in etiquettes})}],
            cout={"octets": len(texte.encode("utf-8", "replace")), "etiquettes": len(etiquettes),
                  "duree_s": round(a.cout.get("duree_s", 0.0) + b.cout.get("duree_s", 0.0)
                                   + 
… [15618 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class Cascade\" tools/bloc_linguistique.py; sed -n '2820,3019p' tools/bloc_linguistique.py", "description": "Read Cascade class"}`

  ```
2777:class Cascade:
    """

    def __init__(self, cout_par_octet: float = 1.0):
        self.cout_par_octet = cout_par_octet
        self.appels = 0

    def activer(self, annotation: Annotation) -> dict:
        self.appels += 1
        octets = sum(u.fin - u.debut for u in annotation.unites_semantiques)
        return {"unites": len(annotation.unites_semantiques),
                "octets": octets,
                "fraction": round(annotation.fraction_semantique, 4),
                "cout": round(octets * self.cout_par_octet, 4),
                "source": annotation.source,
                "langue": annotation.langue}


# --------------------------------------------------------------------------- autotest


ECHANTILLONS = {
    "fr": "Le chat de la voisine qui dort sur le toit se réveille. Va voir le chat ! "
          "Il ne dort pas, mais il a peut-être faim.",
    "en": "The cat of the neighbor who sleeps on the roof wakes up. Do you see the cat? "
          "It is not sleeping, but it may be hungry.",
    "de": "Die Katze der Nachbarin, die auf dem Dach schläft, wacht auf. Siehst du die Katze?",
    "es": "El gato de la vecina que duerme en el tejado se despierta. ¿Ves el ga
… [8208 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '2770,2835p' tools/bloc_linguistique.py", "description": "Read Cascade class exactly"}`

  ```
contexte: str | None = None) -> Annotation:
        a = self.blocs[0].analyser(texte, langue, contexte)
        b = self.blocs[1].analyser(texte, langue, contexte)
        return _fusion(a, b, self.nom, self.priorite_syntagme, self.priorite_par_niveau,
                       self.priorite_par_type)


class Cascade:
    """L'heuristique d'abord ; le neuronal seulement si un niveau reste sous le seuil."""

    nom = "cascade"

    def __init__(self, heuristique: BlocLinguistique, neuronal: BlocLinguistique,
                 seuil: float = 0.6, niveaux=("morphème", "pos", "syntagme", "discours", "pragmatique"),
                 priorite_syntagme: str = "heuristique",
                 priorite_par_niveau: dict | None = None,
                 priorite_par_type: dict | None = None):
        self.h = heuristique
        self.n = neuronal
        self.seuil = seuil
        self.niveaux = niveaux
        self.priorite_syntagme = priorite_syntagme
        self.priorite_par_niveau = (priorite_par_niveau if priorite_par_niveau is not None
                                     else priorite_par_defaut())
        self.priorite_par_type = dict(priorite_par_type or {})
        self.appels_neuronal 
… [1729 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class NeuronalLLMPOS\" tools/bloc_linguistique.py; sed -n '2020,2160p' tools/bloc_linguistique.py", "description": "Inspect NeuronalLLMPOS analyser"}`

  ```
2079:class NeuronalLLMPOS:
            "\"etiquettes\":[{\"niveau\":\"phrase|pragmatique|syntagme|pos\","
            "\"type\":\"...\",\"valeur\":\"...\",\"debut\":0,\"fin\":0,\"confiance\":0.8}]}. "
            "Niveaux attendus : phrase.type, pragmatique.acte, syntagme (GN/GV/GP/REL/SUB). "
            f"Langue indiquée : {langue or 'inconnue'}. Contexte : {contexte or 'aucun'}.\n"
            f"Texte : {texte}"
        )

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        t0 = time.perf_counter()
        if not pathlib.Path(self.modele).exists():
            raise RefusNeuronal(f"modèle absent : {self.modele}")
        try:
            sortie = subprocess.run(
                [self.llama_cli, "-m", self.modele, "-p", self._prompt(texte, langue, contexte),
                 "-n", str(self.max_jetons), "--temp", "0", "--no-display-prompt"],
                capture_output=True, text=True, timeout=self.timeout)
        except (OSError, subprocess.TimeoutExpired) as e:
            raise RefusNeuronal(str(e)) from e
        texte_sortie = sortie.stdout.strip()
        debut = texte_sortie.find("{")
       
… [6211 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/helper_scale.py <<'PY'\nimport sys,time,json,resource,hashlib\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\np=sys.argv[1]; n=int(sys.argv[2])\ns=open(p,encoding='utf-8',errors='replace').read()\nm=[x for x in bl.Heuristique._mots(s) if x[3] in ('mot','nombre')] … [1386 caractères tronqués]`

  ```
250 median 0.0609 min 0.0533 max 0.0639 cv 0.064
500 median 0.1242 min 0.1188 max 0.1393 cv 0.057
1000 median 0.3379 min 0.3106 max 0.3606 cv 0.048
2000 median 1.0599 min 1.017 max 1.153 cv 0.047
4000 median 0.8408 min 0.8156 max 0.8843 cv 0.031
8000 median 2.2391 min 2.1399 max 2.3425 cv 0.033
10000 median 3.1622 min 3.0373 max 3.291 cv 0.028
alpha all 1.0299619339639117
alpha >=1000 0.8560858736492278
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\ns=open('data/corpus_litt_propre/test.txt',encoding='utf-8',errors='replace').read()\nm=[x for x in bl.Heuristique._mots(s) if x[3] in ('mot','nombre')]\nfor n in [2000,4000,8000,10000]:\n    t=s[:m … [411 caractères tronqués]`

  ```
n 2000 sentences 184 max words 61 top5 [61, 59, 56, 53, 51] last 2
  tail "ns la salle voisine.\nC'était une salle d'audience, et un public assez nombreux, composé\nd'Européens et d'indigènes, en occupait déjà le prétoire.\n\nMr. Fogg, Mrs"
n 4000 sentences 318 max words 76 top5 [76, 61, 59, 56, 55] last 31
  tail ' pas, sans\ndoute, toute la profondeur du sentiment que lui inspirait son sauveur,\net à ce sentiment elle ne donnait encore que le nom de reconnaissance,\nmais, à'
n 8000 sentences 443 max words 137 top5 [137, 125, 98, 96, 92] last 23
  tail ' bellacos —dijo el comisario.\n\n— Ya le he dicho, señor comisario —respondió Pasamonte—, que se vaya poco a\npoco, que aquellos señores no le dieron esa vara para'
n 10000 sentences 485 max words 137 top5 [137, 125, 110, 104, 98] last 3
  tail 'o a ser quien soy y contra las santas leyes de la\nverdadera amistad, ahora por tan poderoso enemigo como el amor por mí\nrompidas y violadas.\n\n»—Si eso confiesas'
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,re\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nfor p in ['data/corpus_fr_litterature.txt','data/corpus_litt_propre/test.txt']:\n    s=open(p,encoding='utf-8',errors='replace').read()\n    m=[x for x in bl.Heuristique._mots(s) if x[3] in ('mo … [442 caractères tronqués]`

  ```
=== data/corpus_fr_litterature.txt chars 57588
head "Au lecteur\n\n  Cette version électronique reproduit dans son intégralité\n  la version originale.\n\n  La ponctuation n'a pas été modifiée hormis quelques"
tail 'it la Chenille.\n\n"Pas tout à fait, je le crains bien," dit Alice timidement. "Tous les\nmots ne sont pas les mêmes."\n\n"C\'est tout de travers d\'un bout à l\'autre," dit la Chenille d\'un ton\ndécidé; et il'
0.0 fr 0.165
0.2 fr 0.167
0.4 fr 0.173
0.6 fr 0.176
0.8 fr 0.181
=== data/corpus_litt_propre/test.txt chars 56284
head " eut\nretrouvé et qu'on leur eut rendu leurs ardoises et leurs crayons,\nils se mirent fort diligemment à écrire l'histoire de l'accident, à\nl'exception"
tail 'uyas no había yo de ir\ncontra lo que debo a ser quien soy y contra las santas leyes de la\nverdadera amistad, ahora por tan poderoso enemigo como el amor por mí\nrompidas y violadas.\n\n»—Si eso confiesas'
0.0 fr 0.177
0.2 fr 0.16
0.4 und 0.104
0.6 es 0.125
0.8 und 0.113
  ```

- **bash** `{"command": "cat > /tmp/helper_scale2.py <<'PY'\nimport sys,time,json,resource,hashlib\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\np=sys.argv[1]; n=int(sys.argv[2])\ns=open(p,encoding='utf-8',errors='replace').read()\nm=[x for x in bl.Heuristique._mots(s) if x[3] in ('mot','nombre') … [1309 caractères tronqués]`

  ```
[still running after 180000ms; moved to background job bash-48]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "job_list 2>/dev/null || true", "description": "List background jobs"}`

  ```
(no output)
  ```

- **bash** `{"command": "ps aux | grep helper_scale2 | grep -v grep | head; echo '---'; wc -l /tmp/scale2.jsonl 2>/dev/null; tail -3 /tmp/scale2.jsonl 2>/dev/null", "description": "Check background scaling job progress"}`

  ```
stephane 1064616  0.0  0.0   7832  4196 ?        Ss   22:39   0:00 bash -c cat > /tmp/helper_scale2.py <<'PY' import sys,time,json,resource,hashlib sys.path.insert(0,'tools') import bloc_linguistique as bl p=sys.argv[1]; n=int(sys.argv[2]) s=open(p,encoding='utf-8',errors='replace').read() m=[x for x in bl.Heuristique._mots(s) if x[3] in ('mot','nombre')] t=s[:m[n-1][1]] h=bl.Heuristique() t0=time.perf_counter(); a=h.analyser(t); d=time.perf_counter()-t0 t1=time.perf_counter(); out=json.dumps(a.json(),ensure_ascii=False,indent=1)+'\n'; dj=time.perf_counter()-t1 print(json.dumps({'n':n,'duree':d,'json':dj,'rss':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'bytes':len(out.encode()),'etiquettes':len(a.etiquettes)})) PY for rep in 1 2 3 4 5; do for n in 250 500 1000 2000 4000 8000 10000; do python3 /tmp/helper_scale2.py data/corpus_fr_litterature.txt $n; done; done > /tmp/scale2.jsonl python3 - <<'PY' import json,statistics,math rows=[json.loads(l) for l in open('/tmp/scale2.jsonl')] by={} for r in rows: by.setdefault(r['n'],[]).append(r['duree']) for n in sorted(by):     v=by[n]; print(n, 'median',round(statistics.median(v),4),'min',round(min(v),4),'max',round(max(v),4), 'cv', r
… [903 caractères tronqués]
  ```

- **bash** `{"command": "sleep 5; tail -1 /tmp/scale2.jsonl; ps aux | grep helper_scale2 | grep -v grep | wc -l", "description": "Wait for scaling job to finish"}`

  ```
{"n": 10000, "duree": 4.459407411981374, "json": 0.7737565280403942, "rss": 798316, "bytes": 14795890, "etiquettes": 54522}
2
  ```

- **bash** `{"command": "sleep 12; wc -l /tmp/scale2.jsonl; python3 - <<'PY'\nimport json,statistics,math\nrows=[json.loads(l) for l in open('/tmp/scale2.jsonl')]\nby={}\nfor r in rows: by.setdefault(r['n'],[]).append(r['duree'])\nfor n in sorted(by):\n    v=by[n]; print(n, 'median',round(statistics.median(v),4 … [484 caractères tronqués]`

  ```
23 /tmp/scale2.jsonl
250 median 0.1752 min 0.1722 max 0.1842 cv 0.026
500 median 0.2535 min 0.2376 max 0.2773 cv 0.07
1000 median 0.5043 min 0.486 max 0.5918 cv 0.088
2000 median 1.1104 min 1.1073 max 1.1439 cv 0.015
4000 median 0.9701 min 0.9619 max 1.0423 cv 0.036
8000 median 3.041 min 3.0114 max 3.1918 cv 0.026
10000 median 4.4594 min 4.3289 max 4.5374 cv 0.019
alpha from 250 0.843
alpha from 500 0.881
alpha from 1000 0.871
alpha from 2000 0.914
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,time,statistics\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\ns=open('data/corpus_fr_litterature.txt',encoding='utf-8',errors='replace').read()\nm=[x for x in bl.Heuristique._mots(s) if x[3] in ('mot','nombre')]\nfor n in [2000,4000]:\n    t=s … [727 caractères tronqués]`

  ```
=== n 2000 sentences 164 sum per-sentence 0.422
0.0723 65 "[L'Auteur désire exprimer ici sa reconnaissance envers le Traducteur\nde ce qu'il"
0.0094 58 "Elle s'était mise à réfléchir, (tant bien que mal, car la chaleur du\njour l'endo"
0.0094 38 "ALICE, assise auprès de sa sœur sur le gazon, commençait à s'ennuyer\nde rester l"
0.0089 37 "Douce Alice, acceptez l'offrande\n  De ces gais récits enfantins,\n  Et tressez-en"
0.0088 45 'Cependant, quand le Lapin vint à tirer une montre de\nson gousset, la regarda, pu'
0.0086 44 "Notre barque glisse sur l'onde\n  Que dorent de brûlants rayons;\n  Sa marche lent"
0.0081 58 'Cependant, ayant\nfait un second tour, elle aperçut un rideau placé très-bas et q'
0.008 28 "Cherche, se sentant épuisé,\n  A briser le pouvoir magique\n  Du charme qu'il a co"
last 0.0001 0 'Au cou de'
=== n 4000 sentences 300 sum per-sentence 0.627
0.0135 104 '" Car elle avait lu\ndans de jolis petits contes, que des enfants avaient été brû'
0.0121 65 "[L'Auteur désire exprimer ici sa reconnaissance envers le Traducteur\nde ce qu'il"
0.0109 64 "(Alice avait été\nau bord de la mer une fois en sa vie, et se figurait que sur n'"
0.0101 51 'Cependant, comme cette bouteil
… [449 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,cProfile,pstats,io\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\ns=open('data/corpus_fr_litterature.txt',encoding='utf-8',errors='replace').read()\nm=[x for x in bl.Heuristique._mots(s) if x[3] in ('mot','nombre')]\nfor n in [2000,4000]:\n     … [325 caractères tronqués]`

  ```
=== 2000
         5766437 function calls (5679271 primitive calls) in 17.266 seconds

   Ordered by: cumulative time
   List reduced from 355 to 18 due to restriction <18>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.559    0.559   17.269   17.269 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:1561(analyser)
      563    0.391    0.001    4.602    0.008 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:1273(_cible_proche)
        1    0.035    0.035    4.362    4.362 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:2542(_expliciter_partition)
   230636    1.697    0.000    3.771    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:516(_est_adverbe_seul)
        1    1.462    1.462    2.887    2.887 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:2518(_groupes_partition)
        1    0.027    0.027    2.003    2.003 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:950(_sujet_hors_gv)
      799    0.367    0.000    1.812    0.002 {built-in method builtins.any}
  1164481    1.703   
… [3569 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,time,statistics\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\ns=open('data/corpus_fr_litterature.txt',encoding='utf-8',errors='replace').read()\nm=[x for x in bl.Heuristique._mots(s) if x[3] in ('mot','nombre')]\nfor n in [250,500,1000,2000,40 … [495 caractères tronqués]`

  ```
250 median 0.0476 syntagmes 126 pos 295 labels 1430
500 median 0.1162 syntagmes 262 pos 611 labels 2981
1000 median 0.2969 syntagmes 496 pos 1194 labels 5672
2000 median 1.01 syntagmes 1006 pos 2401 labels 11188
4000 median 0.8409 syntagmes 1075 pos 4885 labels 21485
8000 median 3.1175 syntagmes 2192 pos 9912 labels 43379
10000 median 4.5141 syntagmes 2726 pos 12467 labels 54522
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,time,statistics\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\ns=open('data/corpus_fr_litterature.txt',encoding='utf-8',errors='replace').read()\nm=[x for x in bl.Heuristique._mots(s) if x[3] in ('mot','nombre')]\nt10=s[:m[9999][1]]\n# build a  … [1023 caractères tronqués]`

  ```
block words 247 chars 1522
k 1 words 247 median 0.05 syntagmes 124 labels 1407
k 2 words 494 median 0.1166 syntagmes 248 labels 2815
k 4 words 988 median 0.294 syntagmes 496 labels 5631
k 8 words 1976 median 0.8115 syntagmes 992 labels 11263
k 16 words 3952 median 2.6465 syntagmes 1984 labels 22527
k 32 words 7904 median 10.0773 syntagmes 3968 labels 45055
k 40 words 9880 median 15.3943 syntagmes 4960 labels 56319
  ```

### 👤 Utilisateur

background job bash-48 (bash: cat > /tmp/helper_scale2.py <<'PY'
import sys,time,json,resource,hashlib
sys.path.insert(0,'tools')
import bloc_linguistique as bl
p=sys.argv[1]; n=int(sys.argv[2])
s=open(p,encoding='utf-8',errors='replace').read()
m=[x for x in bl.Heuristique._mots(s) if x[3] in ('mot','nombre')]
t=s[:m[n-1][1]]
h=bl.Heuristique()
t0=time.perf_counter(); a=h.analyser(t); d=time.perf_counter()-t0
t1=time.perf_counter(); out=json.dumps(a.json(),ensure_ascii=False,indent=1)+'\n'; dj=time.perf_counter()-t1
print(json.dumps({'n':n,'duree':d,'json':dj,'rss':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'bytes':len(out.encode()),'etiquettes':len(a.etiquettes)}))
PY
for rep in 1 2 3 4 5; do for n in 250 500 1000 2000 4000 8000 10000; do python3 /tmp/helper_scale2.py data/corpus_fr_litterature.txt $n; done; done > /tmp/scale2.jsonl
python3 - <<'PY'
import json,statistics,math
rows=[json.loads(l) for l in open('/tmp/scale2.jsonl')]
by={}
for r in rows: by.setdefault(r['n'],[]).append(r['duree'])
for n in sorted(by):
    v=by[n]; print(n, 'median',round(statistics.median(v),4),'min',round(min(v),4),'max',round(max(v),4), 'cv', round(statistics.pstdev(v)/statistics.mean(v),3))
xs=[math.log(n) for n in sorted(by)]; ys=[math.log(statistics.median(by[n])) for n in sorted(by)]
for start in [0,1,2,3]:
    xs2=xs[start:]; ys2=ys[start:]; mx=sum(xs2)/len(xs2); my=sum(ys2)/len(ys2)
    b=sum((x-mx)*(y-my) for x,y in zip(xs2,ys2))/sum((x-mx)**2 for x in xs2)
    print('alpha from',sorted(by)[start],b)
PY) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "python3 - <<'PY'\nimport sys,time\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\ns=open('data/corpus_fr_litterature.txt',encoding='utf-8',errors='replace').read()\nm=[x for x in bl.Heuristique._mots(s) if x[3] in ('mot','nombre')]\nfor n in [2000,4000,10000]:\n    t=s[:m[n … [432 caractères tronqués]`

  ```
2000 segments 1006 groupes 193 max [8, 8, 7, 6, 6] sum sizes 617 temps_groupes 0.108
4000 segments 1075 groupes 0 max [] sum sizes 0 temps_groupes 0.126
10000 segments 2726 groupes 0 max [] sum sizes 0 temps_groupes 0.783
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,cProfile,pstats,io,time\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\ns=open('data/corpus_fr_litterature.txt',encoding='utf-8',errors='replace').read()\nm=[x for x in bl.Heuristique._mots(s) if x[3] in ('mot','nombre')]\nt10=s[:m[9999][1]]\nph … [771 caractères tronqués]`

  ```
words 3952
         16976679 function calls (16792077 primitive calls) in 49.267 seconds

   Ordered by: cumulative time
   List reduced from 352 to 25 due to restriction <25>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    1.256    1.256   49.276   49.276 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:1561(analyser)
     1040    1.314    0.001   14.774    0.014 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:1273(_cible_proche)
        1    0.077    0.077   14.504   14.504 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:2542(_expliciter_partition)
   768048    5.340    0.000   11.850    0.000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:516(_est_adverbe_seul)
        1    5.866    5.866   11.371   11.371 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:2518(_groupes_partition)
        1    0.051    0.051    5.890    5.890 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py:950(_sujet_hors_gv)
     1553    1.155    0.001    5.544    0.004 {built-in method builtins.any}
  3422472    4.86
… [2004 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '930,1045p' tools/bloc_linguistique.py; echo '---'; sed -n '1200,1340p' tools/bloc_linguistique.py", "description": "Read quadratic-looking functions"}`

  ```
return "ADJ", True, 0.38
        return ("NOUN" if (n and n[0].islower()) else "MOT"), True, 0.3

    # -- morphèmes ----------------------------------------------------------
    @staticmethod
    def _morphemes(mot: str) -> list[tuple[str, int, int, str]]:
        n = _normaliser(mot)
        sortie = []
        for suf in SUFFIXES:
            if len(n) > len(suf) + 2 and n.endswith(suf):
                sortie.append(("suffixe", len(mot) - len(suf), len(mot), suf))
                break
        for pre in PREFIXES:
            if len(n) > len(pre) + 2 and n.startswith(pre):
                sortie.append(("préfixe", 0, len(pre), pre))
                break
        return sortie

    # -- syntagmes ----------------------------------------------------------

    def _sujet_hors_gv(self, texte: str, langue: str, cands: list[dict] | None,
                       pos_verbes: set[int] | None = None) -> list[dict] | None:
        """La convention du gold : le sujet est un **GN**, pas le début du GV.

        Le générateur S rend « Il a couru », « Il ne dort pas », « Marie lit » comme un
        seul GV : il inclut le sujet. Le gold sépare le GN agent du GV. On **déplace**
        le suj
… [11235 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,time,statistics\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\n\ndef fast_groupes(segs):\n    if not segs: return []\n    ordonnes = sorted(enumerate(segs), key=lambda ie: (ie[1].debut, ie[1].fin, ie[0]))\n    groupes=[]; courant=[]; fin_max=No … [1564 caractères tronqués]`

  ```
=== old
1 247 0.078 124
2 494 0.143 248
4 988 0.272 496
8 1976 0.873 992
16 3952 2.69 1984
32 7904 9.962 3968
40 9880 15.298 4960
=== fast
1 247 0.099 124
2 494 0.131 248
4 988 0.258 496
8 1976 0.807 992
16 3952 2.396 1984
32 7904 8.262 3968
40 9880 12.373 4960
  ```

- **bash** `{"command": "sed -n '1328,1560p' tools/bloc_linguistique.py", "description": "Read syntagmes simple loop"}`

  ```
def _syntagmes_simple(self, texte: str, langue: str,
                          pos_verbes: set[int] | None = None) -> list[dict]:
        mots = self._mots(texte)
        lex = POS_FERME.get(langue, POS_FERME["fr"])
        pos_verbes = pos_verbes or set()
        par_debut = {m[0]: k for k, m in enumerate(mots)}

        def est_sub(n: str) -> bool:
            """Le mot est-il un subordonnant **dans cette langue** ? (« car » est un nom anglais)"""
            if n in SUB_PAR_LANGUE.get(langue, set()):
                return True
            return n in SUBORDONNANTS and not (langue == "en" and n == "car")

        def est_verbe(d: int, m: str) -> bool:
            """Le verbe : le lexique, le POS, ou la **position** après un pronom sujet."""
            if _est_verbe(m) or d in pos_verbes:
                return True
            n2 = _normaliser(m)
            # A17 (R1a) : un pronom n'est jamais un verbe **par la position** (« that I read »)
            if n2 in lex.get("PRON", set()):
                return False
            if n2 in lex.get("DET", set()) or n2 in lex.get("PREP", set()) or n2 in lex.get("CONJ", set()):
                return False
            idx = par_debut.ge
… [12701 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"_cible_proche\\|_verbes_proches\" tools/bloc_linguistique.py", "description": "Find call sites of proximity functions"}`

  ```
1274:    def _cible_proche(texte: str, segment: dict, gvs: list[dict],
1309:    def _verbes_proches(texte: str, segment: dict, gvs: list[dict],
1794:                        cible = self._cible_proche(texte, s, gvs, verbes, cache_gv)
1804:                                 or self._cible_proche(texte, s, gvs, verbes, cache_gv))
1807:                    candidats = list(noms) + self._verbes_proches(
1834:                         or self._cible_proche(texte, s, gvs_s, verbes, cache_gv))
1839:                             + self._verbes_proches(
1866:                         or self._cible_proche(texte, s, gvs_u, verbes, cache_gv))
1871:                             + self._verbes_proches(
  ```

- **bash** `{"command": "sed -n '1730,1895p' tools/bloc_linguistique.py", "description": "Read target attachment loop"}`

  ```
if self._negation(p):
                etiquettes.append(Etiquette("phrase", "négation", "oui", d, f, self.nom, 0.65,
                                            langue=lg, script=script))
            if self._modalite(p):
                etiquettes.append(Etiquette("phrase", "modalité", "oui", d, f, self.nom, 0.55,
                                            langue=lg, script=script))
            premier = next((m.group() for m in re.finditer(r"\w+", p)), "")
            acte = ("question" if typ == "interrogative" else
                    "exclamation" if typ == "exclamative" else
                    "ordre" if premier.casefold() in VERBES_IMPERATIFS else "assertion")
            etiquettes.append(Etiquette("pragmatique", "acte", acte, d, f, self.nom, 0.45,
                                        candidats=["assertion", "question", "ordre"],
                                        langue=lg, script=script))
            if (" ou " in p or "«" in p or "“" in p
                    or any(m in _normaliser(p) for m in MOTS_DOUBLE_SENS)):
                etiquettes.append(Etiquette("pragmatique", "double_sens", "candidat", d, f,
                                            self.nom, 0.25
… [9578 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,time,statistics\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\ns=open('data/corpus_fr_litterature.txt',encoding='utf-8',errors='replace').read()\nm=[x for x in bl.Heuristique._mots(s) if x[3] in ('mot','nombre')]\nt10=s[:m[9999][1]]\nph=bl.Heur … [919 caractères tronqués]`

  ```
start 250 block words 250 syntagmes 137 ratio 0.548
start 1000 block words 250 syntagmes 122 ratio 0.488
start 2000 block words 237 syntagmes 101 ratio 0.426
start 3000 block words 249 syntagmes 124 ratio 0.498
start 4000 block words 232 syntagmes 114 ratio 0.491
start 5000 block words 246 syntagmes 143 ratio 0.581
start 6000 block words 249 syntagmes 147 ratio 0.59
start 7000 block words 213 syntagmes 115 ratio 0.54
start 8000 block words 245 syntagmes 138 ratio 0.563
  ```

- **bash** `{"command": "mkdir -p work/banc-performance && ls -la work/banc-performance", "description": "Create bench work directory"}`

  ```
total 0
drwxr-xr-x. 1 stephane stephane    0 15 nov 22:51 .
drwxr-xr-x. 1 stephane stephane 2378 15 nov 22:51 ..
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\ns=open('data/corpus_fr_litterature.txt',encoding='utf-8',errors='replace').read()\nm=[x for x in bl.Heuristique._mots(s) if x[3] in ('mot','nombre')]\nt=s[:m[9999][1]]\nph=bl.Heuristique._phrases(t … [393 caractères tronqués]`

  ```
3-12 317 single sentence 317
['Cette version électronique reproduit dans son intégralité la version originale.', "La ponctuation n'a pas été modifiée hormis quelques corrections mineures.", "L'orthographe a été conservée.", 'Seuls quelques mots ont été modifiés.', 'La liste des modifications se trouve à la fin du texte.', "AVENTURES D'ALICE", 'PAYS DES MERVEILLES.', "AVENTURES D'ALICE", '_AU PAYS DES MERVEILLES_.', "TRADUIT DE L'ANGLAIS PAR HENRI BUÉ."]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,statistics\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\ns=open('data/corpus_fr_litterature.txt',encoding='utf-8',errors='replace').read()\nm=[x for x in bl.Heuristique._mots(s) if x[3] in ('mot','nombre')]\nt=s[:m[9999][1]]\nph=bl.Heuristique … [451 caractères tronqués]`

  ```
100 661 6.0 3 12
10 'Cette version électronique reproduit dans son intégralité la version originale.'
11 "La ponctuation n'a pas été modifiée hormis quelques corrections mineures."
5 "L'orthographe a été conservée."
6 'Seuls quelques mots ont été modifiés.'
11 'La liste des modifications se trouve à la fin du texte.'
3 "AVENTURES D'ALICE"
3 'PAYS DES MERVEILLES.'
3 "AVENTURES D'ALICE"
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/banc_performance.py", "content": "#!/usr/bin/env python3\n\"\"\"banc_performance.py — le banc reproductible de `drave analyser`.\n\nCe que le banc mesure, et comment :\n\n1. **le texte réel de 10 000 mots** — un préfixe exact du co … [46546 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/banc_performance.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/banc_performance.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''        r = _run([sys.executable, str(pathlib.Path(__file__).resolve()),\n                  \"--interne\", \"--fichier\", str(texte_path), \"--sortie\", str(sortie)])''','''        r = _ru … [3089 caractères tronqués]`

  ```
patched
OK
  ```

- **bash** `{"command": "grep -n \"sortie-json\\|syntagmes\\|cache_froid\\|annotation = bl.Heuristique().analyser\" tools/banc_performance.py | head -30; sed -n '285,330p' tools/banc_performance.py; sed -n '840,930p' tools/banc_performance.py", "description": "Verify patch sections"}`

  ```
270:                  "--interne", "--fichier", str(texte_path), "--sortie-json", str(sortie)])
289:        "syntagmes": resultats[0]["syntagmes"],
439:        "syntagmes": sum(1 for e in annotation.etiquettes if e.niveau == "syntagme"),
523:            "cache_froid": True,
745:        "syntagmes, donc le temps.",
747:        "constante. Le texte réel de 10 000 mots a une densité de syntagmes plus faible ; "
791:    ap.add_argument("--sortie-json", default="", help=argparse.SUPPRESS)
884:            "syntagmes": r["syntagmes"],
895:        # le nombre de syntagmes est la variable explicative réelle
904:            "syntagmes": r["syntagmes"],
915:    # le modèle en nombre de syntagmes : t = a + b·k + c·k²
916:    synt = [float(m["syntagmes"]) for m in mesures_bloc if m.get("syntagmes")]
917:    temps = [float(m["duree_s"]) for m in mesures_bloc if m.get("syntagmes")]
937:        "prochaine_action": ("profiler et borner `_groupes_partition` (O(k²) sur les syntagmes) "
939:                             "k = syntagmes, pas seulement les mots."),
984:                            "ajustements_syntagmes": ajust_synt},
        "duree_totale_s": _resume([x["duree_totale_s"] for x in resultat
… [6520 caractères tronqués]
  ```

- **bash** `{"command": "time python3 tools/banc_performance.py --rapide --sortie /tmp/perf-rapide.json 2>&1 | tail -60", "description": "Run quick bench smoke test", "timeoutMs": 300000}`

  ```
banc : 10000 mots, 814 phrases, 100 phrases courtes, bloc 247 mots
banc : 10 000 mots (fonction + CLI)…
banc : 100 phrases courtes (fonction + CLI)…
banc : échelle (préfixes réels)…
banc : échelle (bloc répété)…
banc : contrôle de l'instrument…
banc : JSON → /tmp/perf-rapide.json
{
 "dix_mille_s": 4.030711715808138,
 "debit_mots_s": 2480.951431177967,
 "rss_mio": 125.48046875,
 "json_octets": 14795890,
 "cent_ms": 1.0886330856010318,
 "alpha_bloc": 1.544611934172769,
 "controle_lineaire": false,
 "tagger_disponible": false,
 "sortie": "/tmp/perf-rapide.json"
}
[stderr]

real	1m35,540s
user	1m30,971s
sys	0m4,620s
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nr=json.load(open('/tmp/perf-rapide.json'))\nprint(json.dumps({k:r[k] for k in ('corpus','verdict')},ensure_ascii=False,indent=1)[:3000])\nprint('--- mesures 10k')\nprint(json.dumps(r['mesures']['reel_10000']['fonction'],ensure_ascii=False,indent=1)[:1500]) … [449 caractères tronqués]`

  ```
{
 "corpus": {
  "source": "data/corpus_fr_litterature.txt",
  "source_sha256": "392f6c6274daaedfcb2957aa92b489cd28de6fcd7e92c7ae9eb4d8f14e9ed2df",
  "prefixe_sha256": "0069b20e28975ca7b504755456aacf014b864b16705d40e6b381c45ae5e08871",
  "mots": 10000,
  "caracteres": 57588,
  "phrases": 814,
  "bloc_controle": {
   "mots": 247,
   "debut": 0,
   "fin": 1572,
   "sha256": "618e219f2420daa76d7ad52dce15d81ef08dc9a8e1f35826785ce566b695ca41"
  },
  "phrases_courtes": {
   "n": 100,
   "mots": 661,
   "median_mots": 6.0,
   "exemples": [
    "Cette version électronique reproduit dans son intégralité la version originale.",
    "La ponctuation n'a pas été modifiée hormis quelques corrections mineures.",
    "L'orthographe a été conservée.",
    "Seuls quelques mots ont été modifiés.",
    "La liste des modifications se trouve à la fin du texte."
   ]
  }
 },
 "verdict": {
  "resume": "10 000 mots exploitables ; contrôle de linéarité **échoue**",
  "dix_mille_exploitable": true,
  "debit_mots_s": 2480.951431177967,
  "controle_lineaire": false,
  "alpha_bloc_repete": 1.544611934172769,
  "alpha_prefixes_reels": 1.1684775911623348,
  "raison": "α = 1.54 sur le bloc répété (1 = linéaire, 2 
… [5145 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/banc_performance.py --repetitions 3 --sortie reports/performance.json --rapport /tmp/rapport-performance-genere.md > /tmp/banc-perf-offline.log 2>&1; echo \"rc=$?\"", "description": "Run full offline performance bench", "run_in_background": true}`

  ```
started background job bash-72
  ```

- **bash** `{"command": "sleep 20; tail -20 /tmp/banc-perf-offline.log; echo '---'; ps aux | grep banc_performance | grep -v grep | head -3", "description": "Check offline bench progress"}`

  ```
banc : 10000 mots, 814 phrases, 100 phrases courtes, bloc 247 mots
banc : 10 000 mots (fonction + CLI)…
---
stephane 1062676  3.4  0.1 1823580 188604 ?      Sl   22:35   0:41 node26 /home/stephane/.local/share/../bin/dsh --profile headless Tâche T4 (exploitable, 4/5) : la **performance** — mesure `analyser` sur un texte réel de **10 000 mots** (le corpus du dépôt ou un texte assemblé), le **temps** (s), le **débit** (mots/s), la **mémoire** (pic RSS), la **taille du JSON**, et le même sur 100 phrases courtes (le coût fixe par appel) ; compare avec `--tagger` (le coût réseau) ; le **contrôle négatif** : le temps doit croître linéairement avec la taille (pas quadratiquement). Fiche `reports/rapport-performance.md` + JSON, un banc reproductible (`tools/banc_performance.py` ?).
stephane 1069788  0.4  0.0   7700  4148 ?        Ss   22:54   0:00 bash -c python3 tools/banc_performance.py --repetitions 3 --sortie reports/performance.json --rapport /tmp/rapport-performance-genere.md > /tmp/banc-perf-offline.log 2>&1; echo "rc=$?"
stephane 1069795 27.4  0.0  76876 69324 ?        S    22:54   0:07 python3 tools/banc_performance.py --repetitions 3 --sortie reports/performance.json --rapport /t
… [32 caractères tronqués]
  ```

- **bash** `{"command": "sleep 60; tail -20 /tmp/banc-perf-offline.log", "description": "Check bench progress"}`

  ```
[still running after 60000ms; moved to background job bash-74]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "tail -20 /tmp/banc-perf-offline.log; echo '---'; ps aux | grep banc_performance.py | grep -v grep | head -3", "description": "Check bench log and process"}`

  ```
banc : 10000 mots, 814 phrases, 100 phrases courtes, bloc 247 mots
banc : 10 000 mots (fonction + CLI)…
banc : 100 phrases courtes (fonction + CLI)…
banc : échelle (préfixes réels)…
banc : échelle (bloc répété)…
---
stephane 1062676  3.3  0.1 1820384 185244 ?      Sl   22:35   0:43 node26 /home/stephane/.local/share/../bin/dsh --profile headless Tâche T4 (exploitable, 4/5) : la **performance** — mesure `analyser` sur un texte réel de **10 000 mots** (le corpus du dépôt ou un texte assemblé), le **temps** (s), le **débit** (mots/s), la **mémoire** (pic RSS), la **taille du JSON**, et le même sur 100 phrases courtes (le coût fixe par appel) ; compare avec `--tagger` (le coût réseau) ; le **contrôle négatif** : le temps doit croître linéairement avec la taille (pas quadratiquement). Fiche `reports/rapport-performance.md` + JSON, un banc reproductible (`tools/banc_performance.py` ?).
stephane 1069788  0.1  0.0   7700  4148 ?        Ss   22:54   0:00 bash -c python3 tools/banc_performance.py --repetitions 3 --sortie reports/performance.json --rapport /tmp/rapport-performance-genere.md > /tmp/banc-perf-offline.log 2>&1; echo "rc=$?"
stephane 1069795  9.9  0.1 155192 131900 ?       S    2
… [140 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-74 (bash: sleep 60; tail -20 /tmp/banc-perf-offline.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "sleep 45; tail -30 /tmp/banc-perf-offline.log; echo '---'; ps aux | grep banc_performance.py | grep -v grep | wc -l", "description": "Wait and check bench completion", "timeoutMs": 70000}`

  ```
banc : 10000 mots, 814 phrases, 100 phrases courtes, bloc 247 mots
banc : 10 000 mots (fonction + CLI)…
banc : 100 phrases courtes (fonction + CLI)…
banc : échelle (préfixes réels)…
banc : échelle (bloc répété)…
---
5
  ```

- **bash** `{"command": "sleep 60; tail -30 /tmp/banc-perf-offline.log; echo '---'; ps aux | grep banc_performance.py | grep -v grep | wc -l", "description": "Wait for bench completion", "timeoutMs": 90000}`

  ```
banc : 10000 mots, 814 phrases, 100 phrases courtes, bloc 247 mots
banc : 10 000 mots (fonction + CLI)…
banc : 100 phrases courtes (fonction + CLI)…
banc : échelle (préfixes réels)…
banc : échelle (bloc répété)…
banc : contrôle de l'instrument…
---
3
  ```

- **bash** `{"command": "sleep 20; tail -50 /tmp/banc-perf-offline.log; echo '---'; ps aux | grep banc_performance.py | grep -v grep | wc -l", "description": "Collect bench final output", "timeoutMs": 50000}`

  ```
banc : 10000 mots, 814 phrases, 100 phrases courtes, bloc 247 mots
banc : 10 000 mots (fonction + CLI)…
banc : 100 phrases courtes (fonction + CLI)…
banc : échelle (préfixes réels)…
banc : échelle (bloc répété)…
banc : contrôle de l'instrument…
banc : JSON → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/performance.json
banc : rapport → /tmp/rapport-performance-genere.md
{
 "dix_mille_s": 4.011746713891625,
 "debit_mots_s": 2492.6798008888813,
 "rss_mio": 125.94921875,
 "json_octets": 14795890,
 "cent_ms": 1.0996684432029724,
 "alpha_bloc": 1.5522043797482215,
 "controle_lineaire": false,
 "tagger_disponible": false,
 "sortie": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/performance.json"
}
---
1
  ```

### 👤 Utilisateur

background job bash-72 (bash: python3 tools/banc_performance.py --repetitions 3 --sortie reports/performance.json --rapport /tmp/rapport-performance-genere.md > /tmp/banc-perf-offline.log 2>&1; echo "rc=$?") finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "python3 - <<'PY'\np='tools/banc_performance.py'\ns=open(p,encoding='utf-8').read()\n# add argument\ns=s.replace('''    ap.add_argument(\"--tagger-complet\", action=\"store_true\",\n                    help=\"mesure aussi les 10 000 mots avec --tagger (coûteux)\")''','''    ap.add_argume … [3374 caractères tronqués]`

  ```
patched
OK
  ```

- **bash** `{"command": "python3 tools/banc_performance.py --tagger-seulement --avec-tagger --tagger-complet --sortie reports/performance.json --rapport /tmp/rapport-performance-genere.md > /tmp/banc-perf-tagger.log 2>&1; echo \"rc=$?\"", "description": "Run tagger performance measurements", "run_in_background" … [7 caractères tronqués]`

  ```
started background job bash-80
  ```

- **bash** `{"command": "sed -n '1,220p' /tmp/rapport-performance-genere.md", "description": "Inspect generated report"}`

  ```
# T4 — la performance de `drave analyser`

> **Ligne de roadmap** : B13 (produit) · **Tâche** : T4 (exploitable, 4/5) · **Date** : 2026-11-15 · **Verdict** : 10 000 mots exploitables ; contrôle de linéarité **échoue**

## 1. Le dispositif

- **Corpus** : `data/corpus_fr_litterature.txt` — préfixe exact de **10000 mots** (57588 caractères, 814 phrases), sha256 `0069b20e28975ca7…`.
- **Machine** : Intel(R) Xeon(R) CPU E5-2687W v3 @ 3.10GHz · 40 processeurs · 128795 Go · Python 3.13.16.
- **Mesure** : /usr/bin/time -f %M pour le pic RSS ; 3 répétitions pour les mesures froides ; médiane et intervalle.

## 2. Les 10 000 mots

| mesure | valeur |
|---|---:|
| temps mural du CLI (`--json`) | **4.965 s** (4.958–5.043) |
| temps de la fonction seule | **4.012 s** |
| sérialisation JSON | **0.672 s** |
| débit (fonction) | **2493 mots/s** |
| débit (CLI) | **2014 mots/s** |
| pic RSS | **125.9 Mio** (CLI 167.6 Mio) |
| taille du JSON | **14,795,890 octets** (14.8 Mo) |
| étiquettes | **54,522** |

## 3. Les 100 phrases courtes

| mesure | valeur |
|---|---:|
| 100 appels CLI séparés | **186.7 ms/appel** (19.20 s pour 100) |
| 100 appels fonction | **1.10 ms/appel** (0.116 s) |
| coût fixe (
… [2143 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nr=json.load(open('reports/performance.json'))\nprint('keys',list(r))\nprint('10k fonction',r['mesures']['reel_10000']['fonction']['duree_analyse_s'])\nprint('10k cli',r['mesures']['reel_10000']['cli']['duree_s'])\nprint('10k jsonl',r['mesures']['reel_10000 … [778 caractères tronqués]`

  ```
keys ['schema', 'version', 'date', 'tache', 'commande', 'parametres', 'environnement', 'corpus', 'mesures', 'echelle', 'verdict']
10k fonction {'n': 3, 'mediane': 4.011746713891625, 'moyenne': 4.111267012311146, 'min': 3.926388635998592, 'max': 4.39566568704322, 'p95': 4.39566568704322}
10k cli {'n': 3, 'mediane': 4.964545171009377, 'moyenne': 4.988494123642643, 'min': 4.957839253824204, 'max': 5.043097946094349, 'p95': 5.043097946094349}
10k jsonl {'n': 1, 'mediane': 3.0859061619266868, 'moyenne': 3.0859061619266868, 'min': 3.0859061619266868, 'max': 3.0859061619266868, 'p95': 3.0859061619266868} 17693596
100 fonction {'n': 300, 'mediane': 0.0010996684432029724, 'moyenne': 0.001209484557621181, 'min': 0.0003581519704312086, 'max': 0.003527808003127575, 'p95': 0.002141786040738225}
100 cli {'n': 100, 'mediane': 0.18673887301702052, 'moyenne': 0.19198978785658255, 'min': 0.17331848409958184, 'max': 0.23021083185449243, 'p95': 0.2231472530402243}
100 lot {'n': 1, 'mediane': 0.3694192739203572, 'moyenne': 0.3694192739203572, 'min': 0.3694192739203572, 'max': 0.3694192739203572, 'p95': 0.3694192739203572}
bloc ajust {
 "lineaire": {
  "a": -1.2542452135223319,
  "b": 0.0013767233380165
… [2556 caractères tronqués]
  ```

- **bash** `{"command": "tail -20 /tmp/banc-perf-tagger.log; echo '---'; ps aux | grep banc_performance.py | grep -v grep | head -3; echo '--- cache'; ls -d /tmp/banc-deepseek-* 2>/dev/null | head; ls /tmp/banc-deepseek-*/ 2>/dev/null | wc -l", "description": "Check tagger bench progress"}`

  ```
banc : tagger sur 100 phrases courtes (réseau froid)…
---
stephane 1062676  3.2  0.1 1822168 187056 ?      Sl   22:35   0:46 node26 /home/stephane/.local/share/../bin/dsh --profile headless Tâche T4 (exploitable, 4/5) : la **performance** — mesure `analyser` sur un texte réel de **10 000 mots** (le corpus du dépôt ou un texte assemblé), le **temps** (s), le **débit** (mots/s), la **mémoire** (pic RSS), la **taille du JSON**, et le même sur 100 phrases courtes (le coût fixe par appel) ; compare avec `--tagger` (le coût réseau) ; le **contrôle négatif** : le temps doit croître linéairement avec la taille (pas quadratiquement). Fiche `reports/rapport-performance.md` + JSON, un banc reproductible (`tools/banc_performance.py` ?).
stephane 1071402  1.7  0.0   7700  4232 ?        Ss   22:58   0:00 bash -c python3 tools/banc_performance.py --tagger-seulement --avec-tagger --tagger-complet --sortie reports/performance.json --rapport /tmp/rapport-performance-genere.md > /tmp/banc-perf-tagger.log 2>&1; echo "rc=$?"
stephane 1071409  1.8  0.0  38320 31044 ?        S    22:58   0:00 python3 tools/banc_performance.py --tagger-seulement --avec-tagger --tagger-complet --sortie reports/performance.
… [89 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/banc_performance.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''f\"{env['ram_kb'] // 1024 if env['ram_kb'] else '?'} Go · Python {env['python']}.\",''','''f\"{env['ram_kb'] // (1024 * 1024) if env['ram_kb'] else '?'} Go · Python {env['python']}.\",''') … [4742 caractères tronqués]`

  ```
patched
OK
  ```

- **bash** `{"command": "tail -10 /tmp/banc-perf-tagger.log; echo '---'; ls /tmp/banc-deepseek-*/ 2>/dev/null | wc -l; ps aux | grep banc_performance.py | grep -v grep | wc -l", "description": "Check tagger progress"}`

  ```
banc : tagger sur 100 phrases courtes (réseau froid)…
---
19
3
  ```

- **bash** `{"command": "pkill -f \"banc_performance.py --tagger-seulement\" || true; sleep 1; ps aux | grep banc_performance.py | grep -v grep | wc -l; tail -5 /tmp/banc-perf-tagger.log", "description": "Stop long tagger job"}`

  ```
(no output)
[killed by signal: SIGTERM]
  ```

### 👤 Utilisateur

background job bash-80 (bash: python3 tools/banc_performance.py --tagger-seulement --avec-tagger --tagger-complet --sortie reports/performance.json --rapport /tmp/rapport-performance-genere.md > /tmp/banc-perf-tagger.log 2>&1; echo "rc=$?") finished [status: killed, signal: SIGTERM]. Read its output with job_output.

- **bash** `{"command": "rm -rf /tmp/ds_test2; time DEEPSEEK_CACHE=/tmp/ds_test2 python3 tools/drave.py analyser \"Le chat dort sur le toit.\" --tagger --json >/dev/null 2>/tmp/ds_test2.err; cat /tmp/ds_test2.err", "description": "Measure current tagger latency", "timeoutMs": 60000}`

  ```
drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=149 · latence=0.8 s
[stderr]

real	0m1,007s
user	0m0,278s
sys	0m0,038s
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/banc_performance.py'\ns=open(p,encoding='utf-8').read()\n# insert extrapolation helper before _run_tagger\ns=s.replace('''def _run_tagger(texte_path: pathlib.Path, timeout: float = 7200.0) -> dict:''','''def _extrapoler_10k(tagger: dict, corpus: dict) -> None: … [4301 caractères tronqués]`

  ```
patched
OK
  ```

- **bash** `{"command": "python3 tools/banc_performance.py --tagger-seulement --avec-tagger --sortie reports/performance.json --rapport /tmp/rapport-performance-genere.md > /tmp/banc-perf-tagger100.log 2>&1; echo \"rc=$?\"", "description": "Measure tagger on 100 short sentences", "run_in_background": true}`

  ```
started background job bash-89
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nr=json.load(open('reports/performance.json'))\nprint('RSS fonction',r['mesures']['reel_10000']['fonction']['rss_kb'])\nprint('RSS CLI',r['mesures']['reel_10000']['cli']['rss_kb'])\nprint('JSON ser',r['mesures']['reel_10000']['fonction']['duree_json_s'])\np … [580 caractères tronqués]`

  ```
RSS fonction {'n': 3, 'mediane': 128972, 'moyenne': 128760, 'min': 128012, 'max': 129296, 'p95': 129296}
RSS CLI {'n': 3, 'mediane': 171656, 'moyenne': 171484, 'min': 171052, 'max': 171744, 'p95': 171744}
JSON ser {'n': 3, 'mediane': 0.6723313489928842, 'moyenne': 0.6412987713702023, 'min': 0.5686040250584483, 'max': 0.6829609400592744, 'p95': 0.6829609400592744}
prefixes
{'mots': 250, 'duree_s': 0.04710945510305464, 'duree_min_s': 0.045476330909878016, 'duree_max_s': 0.05517275910824537, 'rss_kb': 37244, 'json_octets': 715655, 'etiquettes': 1430, 'syntagmes': 126}
{'mots': 500, 'duree_s': 0.12208266998641193, 'duree_min_s': 0.12133605498820543, 'duree_max_s': 0.1579815859440714, 'rss_kb': 42356, 'json_octets': 1396996, 'etiquettes': 2981, 'syntagmes': 262}
{'mots': 1000, 'duree_s': 0.3058943438809365, 'duree_min_s': 0.3021870399825275, 'duree_max_s': 0.3095130871515721, 'rss_kb': 51068, 'json_octets': 2757378, 'etiquettes': 5672, 'syntagmes': 496}
{'mots': 2000, 'duree_s': 0.9806973449885845, 'duree_min_s': 0.8956390300299972, 'duree_max_s': 1.0514534760732204, 'rss_kb': 68704, 'json_octets': 5547446, 'etiquettes': 11188, 'syntagmes': 1006}
{'mots': 4000, 'duree_s': 0.758092628093
… [2360 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"add_parser(\\\"analyser\\\"\\|add_argument(\\\"texte\\|--texte\\|add_argument(\\\"fichier\" tools/drave.py | head -30; python3 - <<'PY'\nimport json\nr=json.load(open('reports/performance.json'))\nprint(r['mesures']['cent_courtes']['appels_cli']['codes'])\nprint(r['mesures'][' … [113 caractères tronqués]`

  ```
1117:    analyser.add_argument("texte", metavar="TEXTE", nargs="?", default=None,
1172:    rejouer.add_argument("texte", metavar="TEXTE", help="texte à rejouer (entre guillemets)")
1197:    restituer.add_argument("texte", metavar="TEXTE", nargs="?", default=None,
[2]
[0.20384253887459636, 0.17804639390669763, 0.18550283717922866]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/banc_performance.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''        r = _run([sys.executable, str(RACINE / \"tools\" / \"drave.py\"), \"analyser\",\n                  \"--texte\", phrase, \"--json\"])''','''        r = _run([sys.executable, str(RAC … [1231 caractères tronqués]`

  ```
patched
OK
phrases 100
{
 "appels": 100,
 "codes": [
  0
 ],
 "duree_totale_s": 19.724825939629227,
 "duree_par_appel_s": {
  "n": 100,
  "mediane": 0.19651348935440183,
  "moyenne": 0.19724825939629226,
  "min": 0.17947383294813335,
  "max": 0.24409899092279375,
  "p95": 0.21588126989081502
 },
 "rss_kb": {
  "n": 100,
  "mediane": 31920.0,
  "moyenne": 31862.36,
  "min": 31156,
  "max": 32120,
  "p95": 32080
 },
 "octets_par_appel": {
  "n": 100,
  "mediane": 12613.0,
  "moyenne": 14244.01,
  "min": 4415,
  "max": 36701,
  "p95": 27340
 },
 "octets_total": 1424401,
 "mots": 661
}
merged
  ```

- **bash** `{"command": "tail -10 /tmp/banc-perf-tagger100.log; echo '---'; ls /tmp/banc-deepseek-*/ 2>/dev/null | wc -l; ps aux | grep banc_performance.py | grep -v grep | wc -l", "description": "Check tagger 100 progress"}`

  ```
banc : tagger sur 100 phrases courtes (réseau froid)…
---
63
3
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nlines=[p for p in open('work/banc-performance/phrases-courtes.txt',encoding='utf-8').read().splitlines() if p.strip()]\nprint('lines',len(lines))\nph=bl.Heuristique._phrases('\\n'.join(lines))\npri … [301 caractères tronqués]`

  ```
lines 100
phrases 94
bad []
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nlines=[p for p in open('work/banc-performance/phrases-courtes.txt',encoding='utf-8').read().splitlines() if p.strip()]\nfor sep in ['\\n','\\n\\n']:\n    print(repr(sep), len(bl.Heuristique._phrase … [71 caractères tronqués]`

  ```
'\n' 94
'\n\n' 100
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/banc_performance.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''    lot_path.write_text(\"\\\\n\".join(courtes) + \"\\\\n\", encoding=\"utf-8\")''','''    lot_path.write_text(\"\\\\n\\\\n\".join(courtes) + \"\\\\n\", encoding=\"utf-8\")''')\ns=s.replac … [786 caractères tronqués]`

  ```
patched
OK
lot phrases 100
  ```

- **bash** `{"command": "sleep 30; tail -20 /tmp/banc-perf-tagger100.log; echo '---'; ps aux | grep banc_performance.py | grep -v grep | wc -l; ls /tmp/banc-deepseek-*/ 2>/dev/null | wc -l", "description": "Check tagger completion", "timeoutMs": 50000}`

  ```
banc : tagger sur 100 phrases courtes (réseau froid)…
---
3
102
  ```

- **bash** `{"command": "sleep 20; tail -30 /tmp/banc-perf-tagger100.log; echo '---'; ps aux | grep banc_performance.py | grep -v grep | wc -l", "description": "Wait for tagger job end", "timeoutMs": 40000}`

  ```
banc : tagger sur 100 phrases courtes (réseau froid)…
banc : JSON intermédiaire → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/performance.json
banc : rapport → /tmp/rapport-performance-genere.md
{
 "tagger_disponible": true,
 "cent_courtes_s": 110.20434978115372,
 "cent_courtes_appels": 92,
 "sortie": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/performance.json"
}
---
1
  ```

### 👤 Utilisateur

background job bash-89 (bash: python3 tools/banc_performance.py --tagger-seulement --avec-tagger --sortie reports/performance.json --rapport /tmp/rapport-performance-genere.md > /tmp/banc-perf-tagger100.log 2>&1; echo "rc=$?") finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "python3 - <<'PY'\nimport json\nr=json.load(open('reports/performance.json'))\nprint('tagger',json.dumps(r['mesures']['tagger'],ensure_ascii=False,indent=1)[:4000])\nprint('100 cli codes',r['mesures']['cent_courtes']['appels_cli']['codes'],'octets_total',r['mesures']['cent_courtes']['app … [218 caractères tronqués]`

  ```
tagger {
 "disponible": true,
 "raison": "--avec-tagger absent",
 "cent_courtes": {
  "code": 0,
  "duree_s": 110.20434978115372,
  "rss_kb": 34308,
  "octets_jsonl": 1116929,
  "lignes": 94,
  "phrases": 94,
  "etiquettes": 4069,
  "refus": 0,
  "stats": {
   "modele": "deepseek-chat",
   "appels": 92,
   "reseau": 92,
   "cache": 0,
   "tokens": 14677,
   "latence_s": 109.1
  },
  "stderr": "drave: TAGGER API · modèle=deepseek-chat · appels=92 · réseau=92 · cache=0 · tokens=14677 · latence=109.1 s\n",
  "disponible": true,
  "cache_froid": true,
  "extrapolation_10k": {
   "mesure": false,
   "phrases": 814,
   "phrases_mesurees": 94,
   "appels_estimes": 797,
   "requetes_estimees": 797,
   "tokens_estimes": 236215,
   "duree_estimee_s": 954.3227736367992,
   "reseau_estime_s": 944.759574468085,
   "rapport_longueur": 1.8585495136175922
  }
 }
}
100 cli codes [2] octets_total 0
lot lignes 94 octets 1100026
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/banc_performance.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''        tagger[\"disponible\"] = bool(t100.get(\"disponible\"))\n        if not tagger[\"disponible\"]:\n            tagger[\"raison\"] = (t100.get(\"stderr\", \"\")[:300]\n                … [2124 caractères tronqués]`

  ```
patched
OK
merged 100 CLI 0.19159204547759145 [0] 1424401
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nr=json.load(open('reports/performance.json'))\nprint('tagger',json.dumps(r['mesures']['tagger'],ensure_ascii=False,indent=1))\nprint('100 cli',json.dumps({k:r['mesures']['cent_courtes']['appels_cli'][k] for k in ('codes','duree_totale_s','duree_par_appel_s … [162 caractères tronqués]`

  ```
tagger {
 "disponible": true,
 "raison": "mesuré (cache froid)",
 "cent_courtes": {
  "code": 0,
  "duree_s": 110.20434978115372,
  "rss_kb": 34308,
  "octets_jsonl": 1116929,
  "lignes": 94,
  "phrases": 94,
  "etiquettes": 4069,
  "refus": 0,
  "stats": {
   "modele": "deepseek-chat",
   "appels": 92,
   "reseau": 92,
   "cache": 0,
   "tokens": 14677,
   "latence_s": 109.1
  },
  "stderr": "drave: TAGGER API · modèle=deepseek-chat · appels=92 · réseau=92 · cache=0 · tokens=14677 · latence=109.1 s\n",
  "disponible": true,
  "cache_froid": true,
  "extrapolation_10k": {
   "mesure": false,
   "phrases": 814,
   "phrases_mesurees": 94,
   "appels_estimes": 797,
   "requetes_estimees": 797,
   "tokens_estimes": 236215,
   "duree_estimee_s": 954.3227736367992,
   "reseau_estime_s": 944.759574468085,
   "rapport_longueur": 1.8585495136175922
  }
 },
 "note": "100 phrases en entrée ; 94 phrases après segmentation ; 92 appels réseau"
}
100 cli {
 "codes": [
  0
 ],
 "duree_totale_s": 19.427704149624333,
 "duree_par_appel_s": {
  "n": 100,
  "mediane": 0.19159204547759145,
  "moyenne": 0.19427704149624334,
  "min": 0.17441060906276107,
  "max": 0.26990763703361154,
  "p95": 0.2198254789
… [857 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/banc_performance.py'\ns=open(p,encoding='utf-8').read()\n# add argument\ns=s.replace('''    ap.add_argument(\"--tagger-seulement\", action=\"store_true\",\n                    help=\"ne refait que la partie --tagger et met à jour le JSON existant\")''','''     … [3286 caractères tronqués]`

  ```
patched
OK
  ```

- **bash** `{"command": "python3 tools/banc_performance.py --profil work/banc-performance/bloc-x16.txt --sortie reports/performance-profil.json 2>&1 | tail -20", "description": "Profile 3952-word controlled block", "timeoutMs": 180000}`

  ```
48.588 s         1  bloc_linguistique.py:1561  analyser
  14.474 s      1040  bloc_linguistique.py:1273  _cible_proche
  14.330 s         1  bloc_linguistique.py:2542  _expliciter_partition
  11.606 s    768048  bloc_linguistique.py:516  _est_adverbe_seul
  11.162 s         1  bloc_linguistique.py:2518  _groupes_partition
   5.964 s         1  bloc_linguistique.py:950  _sujet_hors_gv
   5.592 s      1553  ~:0  <built-in method builtins.any>
   4.832 s   3422434  ~:0  <method 'get' of 'dict' objects>
   4.376 s    895968  bloc_linguistique.py:979  <genexpr>
   4.300 s      3955  ~:0  <built-in method builtins.sorted>
   3.170 s      1984  bloc_linguistique.py:1308  _verbes_proches
   3.019 s    171610  copy.py:119  deepcopy
profil → /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/performance-profil.json  (48.6 s, 3952 mots, 1984 syntagmes)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport importlib.util, json, pathlib, sys\nspec=importlib.util.spec_from_file_location('banc','tools/banc_performance.py')\nb=importlib.util.module_from_spec(spec); sys.modules['banc']=b; spec.loader.exec_module(b)\nr=json.loads(pathlib.Path('reports/performance.json') … [270 caractères tronqués]`

  ```
written 3754
# T4 — la performance de `drave analyser`

> **Ligne de roadmap** : B13 (produit) · **Tâche** : T4 (exploitable, 4/5) · **Date** : 2026-11-15 · **Verdict** : 10 000 mots exploitables ; contrôle de linéarité **échoue**

## 1. Le dispositif

- **Corpus** : `data/corpus_fr_litterature.txt` — préfixe exact de **10,000 mots** (57,588 caractères, 814 phrases), sha256 `0069b20e28975ca7…`.
- **Machine** : Intel(R) Xeon(R) CPU E5-2687W v3 @ 3.10GHz · 40 processeurs · 125 Go · Python 3.13.16.
- **Mesure** : /usr/bin/time -f %M pour le pic RSS ; 3 répétitions pour les mesures froides ; médiane et intervalle.

## 2. Les 10 000 mots

| mesure | valeur |
|---|---:|
| temps mural du CLI (`--json`) | **4.965 s** (4.958–5.043) |
| temps de la fonction seule | **4.012 s** |
| sérialisation JSON | **0.672 s** |
| débit (fonction) | **2493 mots/s** |
| débit (CLI) | **2014 mots/s** |
| pic RSS | **125.9 Mio** (CLI 167.6 Mio) |
| taille du JSON | **14,795,890 octets** (14.8 Mo) |
| étiquettes | **54,522** |
| syntagmes | **2,726** |
| JSONL compact (10 000 mots) | **17,693,596 octets** (3.09 s) |

## 3. Les 100 phrases courtes

| mesure | valeur |
|---|---:|
| 100 appels CLI séparés | **19
… [2566 caractères tronqués]
  ```

- **write** `{"content": "# T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSON ; le contrôle de linéarité **échoue** (α = 1,55)\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T4** (exploitable, 4/5) ·\n> **Date** : 2026-11-15 · **Verdict** : ✅ **les 10 000 mot … [15924 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance.md", "limit": 20}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance.md</path>
<type>file</type>
<content>
1: # T4 — la performance de `drave analyser`
2: 
3: > **Ligne de roadmap** : B13 (produit) · **Tâche** : T4 (exploitable, 4/5) · **Date** : 2026-11-15 · **Verdict** : 10 000 mots exploitables ; contrôle de linéarité **échoue**
4: 
5: ## 1. Le dispositif
6: 
7: - **Corpus** : `data/corpus_fr_litterature.txt` — préfixe exact de **10,000 mots** (57,588 caractères, 814 phrases), sha256 `0069b20e28975ca7…`.
8: - **Machine** : Intel(R) Xeon(R) CPU E5-2687W v3 @ 3.10GHz · 40 processeurs · 125 Go · Python 3.13.16.
9: - **Mesure** : /usr/bin/time -f %M pour le pic RSS ; 3 répétitions pour les mesures froides ; médiane et intervalle.
10: 
11: ## 2. Les 10 000 mots
12: 
13: | mesure | valeur |
14: |---|---:|
15: | temps mural du CLI (`--json`) | **4.965 s** (4.958–5.043) |
16: | temps de la fonction seule | **4.012 s** |
17: | sérialisation JSON | **0.672 s** |
18: | débit (fonction) | **2493 mots/s** |
19: | débit (CLI) | **2014 mots/s** |
20: | pic RSS | **125.9 Mio** (CLI 167.6 Mio) |

(Showing lines 1-20 of 85. Use offset=21 to continue.)
</content>
  ```

- **write** `{"content": "# T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSON ; le contrôle de linéarité **échoue** (α = 1,55)\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T4** (exploitable, 4/5) ·\n> **Date** : 2026-11-15 · **Verdict** : ✅ **les 10 000 mot … [15924 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance.md</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance.md", "old_string": "coupe au caractère. Le JSON mesuré est celui du CLI, **indenté** (`indent=1`) ; le JSONL du\ntagger est **compact**, donc plus petit à contenu égal.", "new_string": "coupe au caractère. Le  … [256 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '1,160p' tools/porte-produit.sh 2>/dev/null || ls tools/porte-*.sh | head -20; echo '---'; sed -n '1,120p' tools/toutes-les-portes.sh", "description": "Inspect gate conventions"}`

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
… [8542 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/tests | head -40; echo '---'; sed -n '1,120p' tools/tests/test_produit.py", "description": "Inspect test conventions"}`

  ```
cic
code
documents
linguistique
maths
__pycache__
qualifier_politique_drvm.py
qualifier_porte_bouge_drvm.py
qualifier_porte_drvm.py
qualifier_porte_fenetre_drvm.py
qualifier_porte_minute_drvm.py
qualifier_porte_mobile_drvm.py
qualifier_porte_sto_drvm.py
qualifier_porte_sto_graines.py
tableaux
test_empaquetage.py
test_panini_334.py
test_pensee_politique.py
test_pensee_store.py
test_produit_libre.py
test_produit.py
test_restitution.py
test_restitution_v2.py
test_restitution_v3.py
test_schema_produit.py
test_tagger_api.py
test_verificateur_cic.py
test_verificateur_cic_v2.py
---
"""test_produit.py — le smoke test de bout en bout du point d'entrée `tools/drave.py`.

Huit assertions, deux phrases (fr/en), le déterminisme et les codes de sortie. Le test passe
aussi bien par `python3 tools/tests/test_produit.py` que par `pytest` : il n'importe rien du
dépôt directement, il lance la commande comme un utilisateur.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
CLI = RACINE / "tools" / "drave.py"


def drave(*arguments: str) -> subprocess.CompletedProcess[str]:
    
… [3921 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/banc_performance.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''    ap.add_argument(\"--tailles\", default=\",\".join(str(x) for x in TAILLES))''','''    ap.add_argument(\"--tailles\", default=\",\".join(str(x) for x in TAILLES))\n    ap.add_argument(\ … [370 caractères tronqués]`

  ```
patched
OK
  ```

- **write** `{"content": "\"\"\"test_banc_performance.py — les fondations du banc : découpage, ajustements, tagger.\n\nLe banc est un outil de mesure : ses **calculs** doivent être justes avant que ses chiffres\nservent de résultat. Ces tests ne mesurent pas la performance de la machine ; ils vérifient\nque le p … [5866 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_banc_performance.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/tests/test_banc_performance.py -v 2>&1 | tail -40", "description": "Run bench unit tests", "timeoutMs": 60000}`

  ```
test_lineaire (__main__.TestAjustements.test_lineaire) ... ok
test_loglog_lineaire (__main__.TestAjustements.test_loglog_lineaire) ... ok
test_loglog_quadratique (__main__.TestAjustements.test_loglog_quadratique) ... ok
test_quadratique (__main__.TestAjustements.test_quadratique) ... ok
test_bloc_de_phrases_entieres (__main__.TestDecoupage.test_bloc_de_phrases_entieres) ... ok
test_phrases_courtes_3_a_12_mots (__main__.TestDecoupage.test_phrases_courtes_3_a_12_mots) ... ok
test_prefixe_exact (__main__.TestDecoupage.test_prefixe_exact) ... ok
test_prefixe_plus_long_que_le_texte (__main__.TestDecoupage.test_prefixe_plus_long_que_le_texte) ... FAIL
test_resume (__main__.TestResumes.test_resume) ... ok
test_extrapolation (__main__.TestTagger.test_extrapolation) ... ok
test_lecture_de_la_ligne (__main__.TestTagger.test_lecture_de_la_ligne) ... ok
test_ligne_absente (__main__.TestTagger.test_ligne_absente) ... ok

======================================================================
FAIL: test_prefixe_plus_long_que_le_texte (__main__.TestDecoupage.test_prefixe_plus_long_que_le_texte)
----------------------------------------------------------------------
Traceback (most recent call last)
… [437 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/tests/test_banc_performance.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''        prefixe, n = banc._prefixe_mots(texte, 100)\n        self.assertEqual(n, 3)\n        self.assertEqual(prefixe, texte)''','''        prefixe, n = banc._prefixe_mots(texte … [426 caractères tronqués]`

  ```
patched
............
----------------------------------------------------------------------
Ran 12 tests in 0.002s

OK
  ```

- **write** `{"content": "#!/usr/bin/env bash\n# porte-banc-performance — le banc de performance mesure, et son JSON est complet.\n#\n# Ce qu'elle vérifie : les 12 tests des fondations (préfixe exact, bloc de phrases entières,\n# ajustements linéaire/quadratique/log-log, lecture de la ligne TAGGER, extrapolation … [3148 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-banc-performance.sh</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/porte-banc-performance.sh'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''if timeout 120 python3 tools/banc_performance.py --profil \"$tmp/performance.json\" \\\\\n     --sortie \"$tmp/profil.json\" >/dev/null 2>&1; then\n  # le fichier de test n'est pas d … [839 caractères tronqués]`

  ```
patched
  ✅ tests : Ran 12 tests
  ✅ passage court : 7 étapes
JSON complet : 1000 mots, 20 phrases, 3 points d'échelle, contrôle calculé
  ✅ JSON : contrat et mesures présents
  ✅ mode profil : fonctions dominantes exportées
✅ porte banc-performance verte
  ```

- **bash** `{"command": "git status --short | head -50; echo '---'; ls -lh reports/performance*.json reports/rapport-performance.md tools/banc_performance.py tools/porte-banc-performance.sh tools/tests/test_banc_performance.py", "description": "Check new files and git status"}`

  ```
M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? reports/performance-profil.json
?? reports/performance.json
?? reports/rapport-performance.md
?? reports/rapport-s-paragraphes.md
?? tools/banc_performance.py
?? tools/porte-banc-performance.sh
?? tools/tests/linguistique/gold_reel_50.py
?? tools/tests/test_banc_performance.py
---
-rw-r--r--. 1 stephane stephane  33K 15 nov 23:02 reports/performance.json
-rw-r--r--. 1 stephane stephane 3,6K 15 nov 23:03 reports/performance-profil.json
-rw-r--r--. 1 stephane stephane  16K 15 nov 23:04 reports/rapport-performance.md
-rw-------. 1 stephane stephane  52K 15 nov 23:04 tools/banc_performance.py
-rwx--x--x. 1 stephane stephane 3,2K 15 nov 23:05 tools/porte-banc-performance.sh
-rw-------. 1 stephane stephane 5,8K 15 nov 23:05 tools/tests/test_banc_performance.py
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nr=json.load(open('reports/performance.json'))\nprint('schema',r['schema'],'version',r['version'])\nprint('corpus',r['corpus']['mots'],r['corpus']['phrases'],r['corpus']['prefixe_sha256'][:16])\nprint('10k',r['mesures']['reel_10000']['fonction']['duree_anal … [342 caractères tronqués]`

  ```
schema drave.performance version 1
corpus 10000 814 0069b20e28975ca7
10k 4.011746713891625
100 cli 0.19159204547759145
tagger True {'modele': 'deepseek-chat', 'appels': 92, 'reseau': 92, 'cache': 0, 'tokens': 14677, 'latence_s': 109.1}
verdict False 1.5522043797482215
  ```

- **bash** `{"command": "chmod 755 tools/banc_performance.py tools/porte-banc-performance.sh; chmod 644 tools/tests/test_banc_performance.py; ls -l tools/banc_performance.py tools/porte-banc-performance.sh tools/tests/test_banc_performance.py tools/drave.py", "description": "Fix file permissions"}`

  ```
-rwxr-xr-x. 1 stephane stephane 52770 15 nov 23:04 tools/banc_performance.py
-rw-------. 1 stephane stephane 61308 15 nov 21:55 tools/drave.py
-rwxr-xr-x. 1 stephane stephane  3214 15 nov 23:05 tools/porte-banc-performance.sh
-rw-r--r--. 1 stephane stephane  5932 15 nov 23:05 tools/tests/test_banc_performance.py
  ```

- **bash** `{"command": "sed -n '150,168p' docs/pilotage/roadmap.md; echo '---'; sed -n '28,34p' docs/pilotage/roadmap.md", "description": "Read roadmap insertion points"}`

  ```
**J14.1 — la clôture : 84 portes, 81 vertes, 3 rouges nommées, le tag `chantier-2026-11-14`.** La
passe du **14/11 00 h 30** (`work/portes/passe-1311-23h15.log`) n'est **pas refaite** : les trois
rouges sont **revérifiées**. `porte-sessions` passe **verte** après la mise en pause du hub
`1e7ef596` et le rafraîchissement du heartbeat `e181ce02` ; `porte-indice` et `porte-melange`
restent **rouges structurelles** (mêmes causes : écart au témoin nul pour l'indice ; état de A qui
ne rend pas son code pour le mélange). Le tag annoté `chantier-2026-11-14` est posé sur le dernier
commit vert `0e75f101` (J13.1) ; le tag de semaine `semaine-2026-11-14` (J5.2, resté en échec) est
posé sur le même commit. [`rapport`](../../reports/rapport-cloture-chantier.md) +
[`JSON`](../../reports/rapport-cloture-chantier.json).
**Prochaine mesure** : **B13 — trancher `g017`**, T132/T133 et le
gold B13 ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).

**La vue d'ensemble des chantiers** — huit chantiers (A, B, N, R, **S**, **L**, **D**, B13), leurs relations, leurs chemins critiques et les tensions à trancher — est dans [`chantiers.md`](chantiers.md) ; la carte est [`chantiers-vision.svg`](../s
… [6684 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,8p' docs/pilotage/en-cours.md; echo '---'; sed -n '58,70p' docs/pilotage/en-cours.md; echo '---'; sed -n '84,92p' docs/pilotage/en-cours.md; echo '---'; sed -n '98,112p' docs/pilotage/en-cours.md", "description": "Read en-cours exact lines"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 22 h 26 HNE (T3 : le démarrage)**

> **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*

---
- **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
- **Plan** : B13.
- **Stratégie** : v0.
- **Ambition** : runtime tracé.
- **Objectif final** : moteur de pensée v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/rapport-tagger-erreurs.md)) ; [s065](../../reports/rapport-s065.md).
- **Ce que font les autres** : **N2**, **S**, **hub**.
- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144** (cinq **18/18**), gold v2 **20/46**, permutation **0/18** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/rapport-semaine-2.md) + [JSON](../../reports/rapport-semaine-2.json) ; tag annoté `semaine-2-2026-11-20` sur `73edb3dd` ; **85** portes lues (**81** ve
… [3165 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/en-cours.md'\ns=open(p,encoding='utf-8').read()\ns=s.replace('**Mis à jour : 2026-11-15, 22 h 26 HNE (T3 : le démarrage)**',\n            '**Mis à jour : 2026-11-15, 23 h 06 HNE (T4 : la performance)**')\ns=s.replace('''- **Ce qu'elle fait** : **W5 — r … [4460 caractères tronqués]`

  ```
en-cours patched
3:**Mis à jour : 2026-11-15, 23 h 06 HNE (T4 : la performance)**
65:- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144** (cinq **18/18**), gold v2 **20/46**, permutation **0/18** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/rapport-semaine-2.md) + [JSON](../../reports/rapport-semaine-2.json) ; tag annoté `semaine-2-2026-11-20` sur `73edb3dd` ; **85** portes lues (**81** vertes, **4** rouges nommées). **T4 — la performance** : **10 000 mots en 4,01 s** (2 493 mots/s, **126 Mio**, **14,8 Mo** de JSON) ; **1,10 ms/appel** sur 100 phrases ; `--tagger` **1,17 s/phrase** (~16 min pour 10 000 mots) ; **le contrôle de linéarité échoue** (α **1,55**) ; [fiche](../../reports/rapport-performance.md), [JSON](../../reports/performance.json), [profil](../../reports/performance-profil.json).
66:- **Prochaine action** : **J4 — l'or de rôles** (seconds cadres, rôles hors cadre) ; T132/T133, gold de pensée ; **T4 : borner `_groupes_partition` et `_cible_proche`** (O(k²) sur les syntagmes).
88:- **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 
… [1394 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/roadmap.md'\ns=open(p,encoding='utf-8').read()\nold='''**Prochaine mesure** : **B13 — trancher `g017`**, T132/T133 et le\ngold B13 ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).\n'''\nnew='''**Prochaine mesure** : **B13 — trancher `g017`* … [1331 caractères tronqués]`

  ```
roadmap patched
162:**T4 — la performance mesurée (15/11).** Sur un préfixe exact de **10 000 mots** du corpus
  ```

- **bash** `{"command": "tail -30 journal/2026-11-15/mesures.md", "description": "Read journal notes end"}`

  ```
### W3 — la matrice du tagger : le défaut reste hors ligne, `--tagger` peut seul sortir 4

La **matrice** est mesurée en sous-processus : le **défaut sans clé** sort **0** (heuristique,
`source=heuristique`), **0 socket**, `tools.llm.deepseek` **non importé** ; avec clé, **0**,
**130 tokens** (116 entrée + 14 sortie), **1,156 s**, POS neuronal ; **clé invalide** (401),
**4**, `stdout` **vide**, pas de repli ; **réseau coupé** (connexion refusée réelle), **0** après
**3 essais**, POS heuristique et `refus` publié. Le **coût pour 1 000 phrases** est extrapolé de
W2 : **143 870 tokens**, **989 requêtes**, **981,9 s**, **0,031 $ hors pointe / 0,062 $ en
pointe** ; le cache chaud rejoue à **0 token** en **~0,14 s**. **Recommandation** : défaut hors
ligne, `--tagger` opt-in, **pas de `auto`** ; s'il vient, seulement avec une clé présente et
**sans changer le code de sortie**. **21/21 tests**. [`fiche`](../../reports/rapport-tagger-defaut.md) ·
[`JSON`](../../reports/rapport-tagger-defaut.json).

### W5 — la restitution v3 : les rôles des GP se séparent, le cadre ne suit pas

`_role_gp` quitte la préposition seule pour le **contexte** : `à` + lieu (`la maison`, `Paris`),
`à` + temps (`14 
… [1184 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='journal/2026-11-15/mesures.md'\ns=open(p,encoding='utf-8').read()\nold='''pèsent plus que la préposition. [`fiche`](../../reports/rapport-restitution-v3.md) ·\n[`JSON`](../../reports/pensee-restitution-v3.json).\n<!-- /notes -->'''\nnew='''pèsent plus que la préposi … [2105 caractères tronqués]`

  ```
journal patched
131:### T4 — la performance : 10 000 mots en 4,0 s, et le contrôle de linéarité qui échoue
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo \"rc=$?\"", "description": "Run documentation review", "timeoutMs": 120000}`

  ```
revue de documentation · 763 fiche(s) · 858 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
rc=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo \"rc=$?\"; python3 tools/taille_documents.py 2>&1 | tail -20; echo \"rc=$?\"", "description": "Check state and context budget", "timeoutMs": 120000}`

  ```
en-cours · 1730 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ❌ 1 anomalie(s) :
     · puce > 80 mots : **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** *
rc=0
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2733    231   T1   2800  reports/README.md
    2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4100 mots (budget 4 000)

  avertissements :
     · 64 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759
… [302 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -20; echo \"rc=$?\"; python3 tools/verifier_schemas.py 2>&1 | tail -20; echo \"rc=$?\"", "description": "Check journal and schemas", "timeoutMs": 120000}`

  ```
journal · 47 jour(s) · 219 session(s) · 2668 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
rc=0
  schémas · 465 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
rc=0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re\ns=open('docs/pilotage/en-cours.md',encoding='utf-8').read()\nfor i,line in enumerate(s.splitlines(),1):\n    if line.startswith('- '):\n        w=len(re.findall(r\"\\S+\",line))\n        if w>50: print(i,w,line[:100])\nPY", "description": "List longest state … [10 caractères tronqués]`

  ```
65 95 - **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144** (cinq **18/18**), gold v2 **20/
88 86 - **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (F1 **0,5270**), **W5 — v3**
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re\ns=open('docs/pilotage/en-cours.md',encoding='utf-8').read().splitlines()\nfor i in [64,65,87,88,125]:\n    line=s[i]\n    print(i+1,len(re.findall(r\"\\S+\",line)))\n    if 'T4' in line:\n        j=line.find('T4')\n        print('  T4 tail words',len(re.find … [74 caractères tronqués]`

  ```
65 95
  T4 tail words 48
66 30
  T4 tail words 10
88 86
  T4 tail words 35
89 19
126 75
  T4 tail words 55
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/en-cours.md'\ns=open(p,encoding='utf-8').read()\n# session line: compact, keep T4 short\nold65='''- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144** (cinq **18/18**), gold v2 **20/46**, permutation **0/18** ; [fiche](../../reports/rap … [2789 caractères tronqués]`

  ```
patched
  en-cours · 1618 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3988 mots (budget 4 000)

  avertissements :
     · 64 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · docs/pilotage/roadmap.md : 9149 mots > budget 9000 (T1)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re\ns=open('docs/pilotage/roadmap.md',encoding='utf-8').read().splitlines()\nfor i in range(155,176):\n    if i < len(s):\n        w=len(re.findall(r\"\\S+\",s[i]))\n        print(i+1,w,s[i][:110])\nPY", "description": "Inspect roadmap lines for trimming"}`

  ```
156 15 commit vert `0e75f101` (J13.1) ; le tag de semaine `semaine-2026-11-14` (J5.2, resté en échec) est
157 7 posé sur le même commit. [`rapport`](../../reports/rapport-cloture-chantier.md) +
158 1 [`JSON`](../../reports/rapport-cloture-chantier.json).
159 10 **Prochaine mesure** : **B13 — trancher `g017`**, T132/T133 et le
160 5 gold B13 ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).
161 0 
162 16 **T4 — la performance mesurée (15/11).** Sur un préfixe exact de **10 000 mots** du corpus
163 14 français : **4,01 s** pour `Heuristique.analyser` (**2 493 mots/s**), **4,97 s** pour le CLI
164 17 `--json`, **126 Mio** de pic RSS et **14,8 Mo** de JSON ; **1,10 ms/appel** sur **100 phrases
165 16 courtes**, **191,6 ms** pour un CLI par phrase, **0,369 s** pour les 100 en un `--jsonl`.
166 15 Le **contrôle de linéarité échoue** : sur un bloc contrôlé, **α = 1,55**, le quadratique
167 12 explique **R² 0,99995** contre **0,957** pour le linéaire ; `_groupes_partition` (toutes les
168 15 paires de syntagmes) et `_cible_proche` (tri de tous les GV par segment) sont **O(k²)** sur
169 18 les syntagmes. Le tagger coûte **1,17 s et 160 tokens par phrase** (~16 min pour 10 000 mot
… [461 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/roadmap.md'\ns=open(p,encoding='utf-8').read()\nold_t4='''**T4 — la performance mesurée (15/11).** Sur un préfixe exact de **10 000 mots** du corpus\nfrançais : **4,01 s** pour `Heuristique.analyser` (**2 493 mots/s**), **4,97 s** pour le CLI\n`--json` … [2259 caractères tronqués]`

  ```
patched
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3988 mots (budget 4 000)

  avertissements :
     · 64 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · docs/pilotage/roadmap.md : 9005 mots > budget 9000 (T1)
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/roadmap.md'\ns=open(p,encoding='utf-8').read()\ns=s.replace('**14,8 Mo** de JSON ; 100 phrases **1,10 ms** ; `--tagger` **1,17 s/phrase**.\\n**Contrôle de linéarité négatif** : **α = 1,55**, quadratique **R² 0,99995** ;\\n`_groupes_partition`/`_cible_p … [691 caractères tronqués]`

  ```
patched

  avertissements :
     · 64 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · docs/pilotage/roadmap.md : 9002 mots > budget 9000 (T1)
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/roadmap.md'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''**La vue d'ensemble** est dans [`chantiers.md`](chantiers.md) ; la carte,\n[`chantiers-vision.svg`](../schemas/chantiers-vision.svg) ; le plan multi-sessions,\n[`plan-travail.md`](plan-trav … [366 caractères tronqués]`

  ```
patched
  T0 max : 3988 mots (budget 4 000)

  avertissements :
     · 64 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -20; echo \"rc=$?\"", "description": "Re-run doc review", "timeoutMs": 120000}`

  ```
revue de documentation · 763 fiche(s) · 858 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
rc=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -10; echo \"rc=$?\"; python3 tools/verifie_journal.py 2>&1 | tail -10; echo \"rc=$?\"; python3 tools/verifier_schemas.py 2>&1 | tail -10; echo \"rc=$?\"", "description": "Re-check state, journal, schemas", "timeoutMs": 120000}`

  ```
en-cours · 1618 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
rc=0
  journal · 47 jour(s) · 219 session(s) · 2668 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
rc=0
  schémas · 465 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
rc=0
  ```

- **bash** `{"command": "bash tools/porte-banc-performance.sh 2>&1 | tail -12; echo \"rc=$?\"", "description": "Re-run performance gate", "timeoutMs": 300000}`

  ```
✅ tests : Ran 12 tests
  ✅ passage court : 7 étapes
JSON complet : 1000 mots, 20 phrases, 3 points d'échelle, contrôle calculé
  ✅ JSON : contrat et mesures présents
  ✅ mode profil : fonctions dominantes exportées
✅ porte banc-performance verte
rc=0
  ```

- **bash** `{"command": "python3 tools/verifie_etat_a_jour.py 2>&1 | tail -30; echo \"rc=$?\"", "description": "Check state freshness hook", "timeoutMs": 120000}`

  ```
état · dernier fait 7d114559 · dernier état 7d114559
  ✅ aucun fait commité après le dernier état
rc=0
  ```

- **bash** `{"command": "git diff --stat -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-15/mesures.md; echo '---'; git diff -- docs/pilotage/roadmap.md | head -80", "description": "Inspect doc diffs"}`

  ```
docs/pilotage/en-cours.md     | 12 ++++++------
 docs/pilotage/roadmap.md      | 10 +++++++++-
 journal/2026-11-15/mesures.md | 23 +++++++++++++++++++++++
 3 files changed, 38 insertions(+), 7 deletions(-)
---
diff --git a/docs/pilotage/roadmap.md b/docs/pilotage/roadmap.md
index e6c1fbe6..149ff357 100644
--- a/docs/pilotage/roadmap.md
+++ b/docs/pilotage/roadmap.md
@@ -159,7 +159,15 @@ posé sur le même commit. [`rapport`](../../reports/rapport-cloture-chantier.md
 **Prochaine mesure** : **B13 — trancher `g017`**, T132/T133 et le
 gold B13 ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).
 
-**La vue d'ensemble des chantiers** — huit chantiers (A, B, N, R, **S**, **L**, **D**, B13), leurs relations, leurs chemins critiques et les tensions à trancher — est dans [`chantiers.md`](chantiers.md) ; la carte est [`chantiers-vision.svg`](../schemas/chantiers-vision.svg) ; le **plan de travail multi-sessions** (qui fait quoi, où, à quelle cadence) est dans [`plan-travail.md`](plan-travail.md). Les demandes des 48 h y sont reliées à ce qu'elles ont déplacé.
+**T4 — la performance (15/11).** 10 000 mots : **4,01 s**, **2 493 mots/s**, **126 Mio**,
+**14,8 Mo** JSON ; 100 phrases **
… [510 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- docs/pilotage/en-cours.md | head -100", "description": "Inspect state diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 37806d80..ba2e3157 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 22 h 26 HNE (T3 : le démarrage)**
+**Mis à jour : 2026-11-15, 23 h 06 HNE (T4 : la performance)**
 
 > **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).
 
@@ -62,8 +62,8 @@
 - **Objectif final** : moteur de pensée v0.
 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**, **F1 0,7902** ; D1–E2 ([exemples](../../reports/rapport-exemples-tagger.md), [FAQ](../../reports/rapport-faq.md), [erreurs](../../reports/rapport-tagger-erreurs.md)) ; [s065](../../reports/rapport-s065.md).
 - **Ce que font les autres** : **N2**, **S**, **hub**.
-- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144** (cinq **18/18**), gold v2 **20/46**, permutation **0/18** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/rapport-semaine-2.md) + [JSON](../../reports/rapport-semaine-2.json) ; tag annoté `semaine-2-2026-11-20` sur `73edb3dd` ; **85** porte
… [3802 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nr=json.load(open('reports/performance.json'))\nprint('commande',r['commande'])\nprint('parametres',r['parametres'])\nprint('date',r['date'])\nPY", "description": "Check JSON provenance fields"}`

  ```
commande tools/banc_performance.py --repetitions 3 --sortie reports/performance.json --rapport /tmp/rapport-performance-genere.md
parametres {'source': 'data/corpus_fr_litterature.txt', 'mots': 10000, 'phrases_courtes': 100, 'repetitions': 3, 'tailles': [250, 500, 1000, 2000, 4000, 8000, 10000], 'avec_tagger': False, 'tagger_complet': False}
date 2026-11-15
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/banc_performance.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''        rapport[\"mesures\"][\"tagger\"] = tagger\n        rapport[\"date\"] = time.strftime(\"%Y-%m-%d\")''','''        rapport[\"mesures\"][\"tagger\"] = tagger\n        rapport[\"comman … [986 caractères tronqués]`

  ```
patched
OK
metadata updated
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/banc_performance.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''    # --- le mode profil : la cause, pas seulement le chiffre\n    if args.profil:\n        return _profil(pathlib.Path(args.profil), pathlib.Path(args.sortie))''','''    # --- le mode pro … [547 caractères tronqués]`

  ```
patched
OK
  ```

- **bash** `{"command": "python3 tools/tests/test_banc_performance.py 2>&1 | tail -5; echo '---'; bash tools/porte-banc-performance.sh 2>&1 | tail -8", "description": "Re-run tests and gate", "timeoutMs": 300000}`

  ```
............
----------------------------------------------------------------------
Ran 12 tests in 0.002s

OK
---
  ✅ tests : Ran 12 tests
  ✅ passage court : 7 étapes
JSON complet : 1000 mots, 20 phrases, 3 points d'échelle, contrôle calculé
  ✅ JSON : contrat et mesures présents
  ✅ mode profil : fonctions dominantes exportées
✅ porte banc-performance verte
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance.md</path>
<type>file</type>
<content>
1: # T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSON ; le contrôle de linéarité **échoue** (α = 1,55)
2: 
3: > **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T4** (exploitable, 4/5) ·
4: > **Date** : 2026-11-15 · **Verdict** : ✅ **les 10 000 mots sont exploitables** (4,0 s de
5: > fonction, 2 493 mots/s, 126 Mio de pic RSS, 14,8 Mo de JSON) ; ❌ **le contrôle négatif de
6: > linéarité échoue** — le temps croît en **α = 1,55** sur un bloc contrôlé, et le terme
7: > quadratique explique **R² 0,99995** contre **0,957** pour le linéaire. Le coupable est
8: > nommé : `_groupes_partition` (toutes les paires de syntagmes, O(k²)) et `_cible_proche`
9: > (tri de tous les GV pour chaque segment), pas la tokenisation.
10: >
11: > **Les chiffres.** Sur le préfixe exact de **10 000 mots** de
12: > [`data/corpus_fr_litterature.txt`](../data/corpus_fr_litterature.txt) (Alice, français,
13: > 57 588 caractères, 814 phrases) : **4,012 s** pour `Heuristique.analyser`, **4,965 s**
14: > pour le CLI `--json` (dont 0,672 s de sérialisa
… [6231 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance.md", "offset": 121, "limit": 190}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance.md</path>
<type>file</type>
<content>
121: | tokens estimés | **236 215** |
122: | durée estimée | **954 s ≈ 15,9 min** |
123: | réseau estimé | **945 s** |
124: | comparaison à la fonction heuristique (4,012 s) | **×238** |
125: 
126: C'est une **estimation**, pas une mesure : le champ `mesure: false` du JSON le dit. Elle
127: suppose la même distribution de phrases, corrigée du rapport de longueur ; un cache chaud
128: diviserait le temps et les tokens par presque le nombre d'appels. Au taux de W3
129: (0,031 $ pour 143 870 tokens), 236 215 tokens valent **~0,05 $** — le coût monétaire est
130: négligeable, le coût **temps** ne l'est pas.
131: 
132: ## 5. Le contrôle négatif de linéarité — et pourquoi il échoue
133: 
134: ### 5.1 Les préfixes réels sont confondus par le contenu
135: 
136: Les préfixes du même texte ne permettent **pas** de conclure : le nombre de syntagmes n'est
137: pas proportionnel aux mots, et le temps suit les syntagmes.
138: 
139: | mots | syntagmes | temps (s) | mots/s |
140: |---:|---:|---:|---:|
141: | 250 | 126 | 0,047 | 5 300 |
142: | 500 | 262 | 0,122 | 4 097 |
143: | 1 
… [9063 caractères tronqués]
  ```

- **bash** `{"command": "git ls-files data/corpus_fr_litterature.txt; git check-ignore -v data/corpus_fr_litterature.txt 2>/dev/null || true; git ls-files data | head -10; echo '---'; git status --short data/corpus_fr_litterature.txt", "description": "Check if corpus is tracked"}`

  ```
.gitignore:9:data/	data/corpus_fr_litterature.txt
---
  ```

- **bash** `{"command": "cp work/banc-performance/corpus-10000.txt reports/performance-corpus-10000.txt\npython3 - <<'PY'\nimport hashlib, json, pathlib\np=pathlib.Path('reports/performance-corpus-10000.txt')\nb=p.read_bytes()\nprint('bytes',len(b),'sha256',hashlib.sha256(b).hexdigest())\nr=json.load(open('repo … [254 caractères tronqués]`

  ```
bytes 58790 sha256 0069b20e28975ca7b504755456aacf014b864b16705d40e6b381c45ae5e08871
json prefixe 0069b20e28975ca7b504755456aacf014b864b16705d40e6b381c45ae5e08871
json source 392f6c6274daaedfcb2957aa92b489cd28de6fcd7e92c7ae9eb4d8f14e9ed2df
prefixe file ends 'est tout de travers d\'un bout à l\'autre," dit la Chenille d\'un ton\ndécidé; et il'
  ```

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-performance.md'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''> **Les chiffres.** Sur le préfixe exact de **10 000 mots** de\n> [`data/corpus_fr_litterature.txt`](../data/corpus_fr_litterature.txt) (Alice, français,\n> 57 588 caractères, 814 phr … [3349 caractères tronqués]`

  ```
patched
13:> [`reports/performance-corpus-10000.txt`](performance-corpus-10000.txt)
81:**94** (le découpage fusionne six lignes), et le tagger fait **92 appels** (deux phrases
283:# le passage publié ici : hors ligne, puis réseau sur 100 phrases
285:  --source reports/performance-corpus-10000.txt --mots 10000 \
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance.md", "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-performance.md</path>
<type>file</type>
<content>
1: # T4 — la performance de `drave analyser` : 10 000 mots en 4,0 s, 126 Mio, 14,8 Mo de JSON ; le contrôle de linéarité **échoue** (α = 1,55)
2: 
3: > **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T4** (exploitable, 4/5) ·
4: > **Date** : 2026-11-15 · **Verdict** : ✅ **les 10 000 mots sont exploitables** (4,0 s de
5: > fonction, 2 493 mots/s, 126 Mio de pic RSS, 14,8 Mo de JSON) ; ❌ **le contrôle négatif de
6: > linéarité échoue** — le temps croît en **α = 1,55** sur un bloc contrôlé, et le terme
7: > quadratique explique **R² 0,99995** contre **0,957** pour le linéaire. Le coupable est
8: > nommé : `_groupes_partition` (toutes les paires de syntagmes, O(k²)) et `_cible_proche`
9: > (tri de tous les GV pour chaque segment), pas la tokenisation.
10: >
11: > **Les chiffres.** Sur le préfixe exact de **10 000 mots** de
12: > `data/corpus_fr_litterature.txt` (Alice, français), versionné dans
13: > [`reports/performance-corpus-10000.txt`](performance-corpus-10000.txt)
14: > (sha256 `0069b20e28975ca7b504755456aacf014b864b16705d40e6b381c45ae5e08871`,
15: > 57
… [1322 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -30; echo \"rc=$?\"", "description": "Doc review after corpus artifact", "timeoutMs": 120000}`

  ```
revue de documentation · 763 fiche(s) · 858 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
rc=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -8; python3 tools/taille_documents.py 2>&1 | tail -4", "description": "Recheck state and budget", "timeoutMs": 120000}`

  ```
en-cours · 1618 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  avertissements :
     · 64 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -8; python3 tools/verifier_schemas.py 2>&1 | tail -6", "description": "Recheck journal and schemas", "timeoutMs": 120000}`

  ```
journal · 47 jour(s) · 219 session(s) · 2668 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  schémas · 465 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

- **bash** `{"command": "grep -n \"rapport-performance\\|performance.json\\|T4\" reports/INDEX.md reports/README.md 2>/dev/null | head -20; echo '---'; head -40 reports/INDEX.md", "description": "Check reports index conventions"}`

  ```
---
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **756 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.

| fiche | titre |
|---|---|
| [07-mesures-couche-commune.md](07-mesures-couche-commune.md) | 7. Les modèles alternatifs pour l'entrée et la sortie — vers une couche commune |
| [aiguille-30b.md](aiguille-30b.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf |
| [aiguille-gpt-oss.md](aiguille-gpt-oss.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf |
| [alignement-verne.md](alignement-verne.md) | Alignement phrase à phrase — *Le Tour du monde en quatre-vingts jours* (français → anglais) |
| [bilan-b11.md](bilan-b11.md) | Bilan B11 — ce qui tient, ce qui ne tient pas |
| [bilan-multi-materiel.md](bilan-multi-materiel.md) | Bilan multi-matériel — CPU, FPGA, GPU |
| [campagne-benefices.md](campagne-benefices.md) | Campagne 24 h — où Drave est à son meilleur, tâche par tâche |
| [fiche-nuit-17-10.md](fiche-nuit-17-10.md) | La nuit du 17 au
… [3294 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nr=json.load(open('reports/performance.json'))\nprint('100 cli codes',r['mesures']['cent_courtes']['appels_cli']['codes'])\nprint('100 cli median',r['mesures']['cent_courtes']['appels_cli']['duree_par_appel_s']['mediane'])\nprint('tagger',r['mesures']['tagg … [148 caractères tronqués]`

  ```
100 cli codes [0]
100 cli median 0.19159204547759145
tagger {'modele': 'deepseek-chat', 'appels': 92, 'reseau': 92, 'cache': 0, 'tokens': 14677, 'latence_s': 109.1}
commande tools/banc_performance.py --repetitions 3 --sortie reports/performance.json ; puis --tagger-seulement --avec-tagger --sortie reports/performance.json
param {'source': 'data/corpus_fr_litterature.txt', 'mots': 10000, 'phrases_courtes': 100, 'repetitions': 3, 'tailles': [250, 500, 1000, 2000, 4000, 8000, 10000], 'avec_tagger': True, 'tagger_complet': False, 'tagger_seulement': True}
  ```

- **bash** `{"command": "grep -n \"work\" .gitignore; git status --short work/banc-performance | head", "description": "Check work ignore"}`

  ```
27:work/
  ```

- **bash** `{"command": "python3 tools/banc_performance.py --help 2>&1 | head -50; echo '---'; python3 -m py_compile tools/banc_performance.py tools/tests/test_banc_performance.py && echo compile-ok", "description": "Check bench help and compile"}`

  ```
usage: banc_performance.py [-h] [--source SOURCE] [--mots MOTS]
                           [--phrases-courtes PHRASES_COURTES]
                           [--repetitions REPETITIONS] [--tailles TAILLES]
                           [--bloc-repetitions BLOC_REPETITIONS]
                           [--sortie SORTIE] [--rapport RAPPORT]
                           [--avec-tagger] [--tagger-complet]
                           [--tagger-seulement] [--profil PROFIL] [--rapide]

banc_performance.py — le banc reproductible de `drave analyser`.

Ce que le banc mesure, et comment :

1. **le texte réel de 10 000 mots** — un préfixe exact du corpus (10 000 tokens `mot` ou
   `nombre`, coupés au 10 000e token, pas au caractère), analysé par le CLI (`--json`) et
   par la fonction (`Heuristique.analyser`) dans un sous-processus neuf ;
2. **100 phrases courtes** — 100 phrases réelles de 3 à 12 mots, mesurées en 100 appels
   séparés (le coût fixe du CLI), en 100 appels dans un même processus (le coût fixe de la
   fonction), et en un seul appel `--jsonl` (le lot) ;
3. **`--tagger`** — le même lot de 100 phrases, puis éventuellement les 10 000 mots, avec
   un cache DeepSeek **froid** (`DEEPSEEK_CACHE`
… [1447 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\" --json >/tmp/check.json 2>/tmp/check.err; echo \"rc=$?\"; head -c 100 /tmp/check.json; echo; cat /tmp/check.err", "description": "Smoke test CLI still works"}`

  ```
rc=0
{
 "schema": "drave.annotation",
 "version": 2,
 "texte": "Le chat dort.",
 "langue": "fr",
 "script
  ```

- **bash** `{"command": "ls -l .git/hooks/pre-commit 2>/dev/null && sed -n '1,120p' .git/hooks/pre-commit 2>/dev/null | head -80", "description": "Inspect pre-commit hook"}`

  ```
-rwxr-xr-x. 1 stephane stephane 1470 31 oct 12:55 .git/hooks/pre-commit
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
python3 tools/archive_sessions.py --quiet >/dev/null || { echo "  ⛔ archivage des sessions en échec"; exit 1; }
python3 tools/session_report.py --quiet >/dev/null || { echo "  ⛔ rapport de session en échec"; exit 1; }
# Le journal d
… [306 caractères tronqués]
  ```

- **bash** `{"command": "git add tools/banc_performance.py tools/porte-banc-performance.sh tools/tests/test_banc_performance.py reports/performance.json reports/performance-profil.json reports/performance-corpus-10000.txt reports/rapport-performance.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/ … [82 caractères tronqués]`

  ```
docs/pilotage/en-cours.md            |   12 +-
 docs/pilotage/roadmap.md             |   10 +-
 journal/2026-11-15/mesures.md        |   23 +
 reports/performance-corpus-10000.txt | 1335 ++++++++++++++++++++++++++++++++++
 reports/performance-profil.json      |  172 +++++
 reports/performance.json             | 1307 +++++++++++++++++++++++++++++++++
 reports/rapport-performance.md       |  308 ++++++++
 tools/banc_performance.py            | 1193 ++++++++++++++++++++++++++++++
 tools/porte-banc-performance.sh      |   69 ++
 tools/tests/test_banc_performance.py |  148 ++++
 10 files changed, 4570 insertions(+), 7 deletions(-)
  ```

- **bash** `{"command": "python3 tools/verifie_etat_a_jour.py --index 2>&1 | tail -20; echo \"rc=$?\"", "description": "Check staged state hook", "timeoutMs": 120000}`

  ```
✅ index : aucun fait stagé sans état
rc=0
  ```

- **bash** `{"command": "git commit -F - <<'EOF'\nT4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))\n\nLe banc tools/banc_performance.py mesure Heuristique.analyser sur un préfixe exact de 10 000 mots d … [1273 caractères tronqués]`

  ```
[s/v7 7f0e8320] T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))
 25 files changed, 8142 insertions(+), 35 deletions(-)
 create mode 100644 journal/sessions/session-cbce9c66-4423-4a44-a112-b8c9f8b333dc/digest.md
 create mode 100644 journal/sessions/session-cbce9c66-4423-4a44-a112-b8c9f8b333dc/rapport.md
 create mode 100644 reports/performance-corpus-10000.txt
 create mode 100644 reports/performance-profil.json
 create mode 100644 reports/performance.json
 create mode 100644 reports/rapport-performance.md
 create mode 100755 tools/banc_performance.py
 create mode 100755 tools/porte-banc-performance.sh
 create mode 100644 tools/tests/test_banc_performance.py
rc=0
[stderr]
  ✅ index : aucun fait stagé sans état
  ```

- **bash** `{"command": "git show --stat --oneline HEAD | head -40; echo '---'; git status --short | head -40", "description": "Inspect commit and remaining changes"}`

  ```
7f0e8320 T4 — LA PERFORMANCE : 10 000 MOTS EN 4,01 S (2 493 MOTS/S, 126 MIO, 14,8 MO DE JSON), 100 PHRASES À 1,10 MS ; LE CONTRÔLE DE LINÉARITÉ ÉCHOUE (α = 1,55, O(k²))
 docs/pilotage/en-cours.md                          |   12 +-
 docs/pilotage/roadmap.md                           |   10 +-
 journal/2026-11-15/README.md                       |    7 +-
 journal/2026-11-15/distribue.md                    |    2 +-
 journal/2026-11-15/docs.md                         |    9 +-
 journal/2026-11-15/memoire.md                      |    2 +-
 journal/2026-11-15/mesures.md                      |   25 +-
 journal/2026-11-15/modele.md                       |    2 +-
 journal/2026-11-15/outils.md                       |    2 +-
 journal/2026-11-15/portes.md                       |    2 +-
 journal/README.md                                  |    5 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   63 +
 .../rapport.md                                     |   15 +-
 .../digest.md                                      |  125 +
 .../rapport.md                                     |   37 +-
 .../digest.md                           
… [1010 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"T4 — la performance\" journal/2026-11-15/mesures.md; tail -30 journal/2026-11-15/mesures.md", "description": "Verify journal note preserved"}`

  ```
131:### T4 — la performance : 10 000 mots en 4,0 s, et le contrôle de linéarité qui échoue
contre 0,40 ; `agent` et `prédicat` sont inchangés. Le **contrôle négatif** tue la mesure :
permutation des cinq rôles **0/18**, permutation de tous **0,4028** global, rôle constant `lieu`
**0,0208** (3/18, F1 0,037). `--roles-v3` est le mode ; `--roles` reste la v2. Verdict :
**positif sur la séparation, négatif sur le produit** — la segmentation et le choix du cadre
pèsent plus que la préposition. [`fiche`](../../reports/rapport-restitution-v3.md) ·
[`JSON`](../../reports/pensee-restitution-v3.json).

### T4 — la performance : 10 000 mots en 4,0 s, et le contrôle de linéarité qui échoue

Le banc [`tools/banc_performance.py`](../../tools/banc_performance.py) mesure `analyser` sur un
préfixe exact de **10 000 mots** du corpus français (Alice, 57 588 caractères, 814 phrases) :
**4,012 s** pour la fonction, **4,965 s** pour le CLI `--json` (0,672 s de sérialisation),
**2 493 mots/s**, **128 972 Ko** de pic RSS, **14 795 890 octets** de JSON,
**54 522 étiquettes**, **2 726 syntagmes**. Sur **100 phrases courtes** : **1,10 ms/appel**
pour la fonction, **1,18 ms** de coût fixe, **191,6 ms** pour u
… [1151 caractères tronqués]
  ```

- **bash** `{"command": "git show HEAD:docs/pilotage/en-cours.md | grep -n \"T4\\|portes | \\|fichiers / JSON\" | head -10; echo '---'; git show HEAD:docs/pilotage/roadmap.md | grep -n \"T4 — la performance\"", "description": "Verify committed state and roadmap"}`

  ```
3:**Mis à jour : 2026-11-15, 23 h 06 HNE (T4 : la performance)**
65:- **Ce qu'elle fait** : **W5 — restitution v3** : gold S **144/144**, gold v2 **20/46** ; [fiche](../../reports/rapport-restitution-v3.md). **W6 — la clôture** : [rapport semaine 2](../../reports/rapport-semaine-2.md) ; **T4** : 10 000 mots **4,01 s**, contrôle **α 1,55** ; [fiche](../../reports/rapport-performance.md), [JSON](../../reports/performance.json).
66:- **Prochaine action** : **J4 — l'or de rôles** (seconds cadres, rôles hors cadre) ; T132/T133, gold de pensée ; **T4 : borner `_groupes_partition` et `_cible_proche`** (O(k²) sur les syntagmes).
102:| portes | **86** (dont `porte-banc-performance` le 15/11) | `tools/porte-*.sh` |
104:| fichiers / JSON de résultats | **763** / **858** | `reports/*.md` / `reports/*.json` |
---
162:**T4 — la performance (15/11).** 10 000 mots : **4,01 s**, **2 493 mots/s**, **126 Mio**,
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -8; echo \"rc=$?\"; python3 tools/taille_documents.py 2>&1 | tail -4; echo \"rc=$?\"", "description": "Final doc review and budget", "timeoutMs": 120000}`

  ```
revue de documentation · 763 fiche(s) · 858 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
rc=0
  avertissements :
     · 64 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
rc=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -6; echo \"rc=$?\"; python3 tools/verifie_journal.py 2>&1 | tail -6; echo \"rc=$?\"", "description": "Final state and journal checks", "timeoutMs": 120000}`

  ```
en-cours · 1618 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
rc=0
  journal · 47 jour(s) · 220 session(s) · 2672 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
rc=0
  ```

- **bash** `{"command": "bash tools/porte-banc-performance.sh 2>&1 | tail -8; echo \"rc=$?\"", "description": "Final performance gate", "timeoutMs": 300000}`

  ```
✅ tests : Ran 12 tests
  ✅ passage court : 7 étapes
JSON complet : 1000 mots, 20 phrases, 3 points d'échelle, contrôle calculé
  ✅ JSON : contrat et mesures présents
  ✅ mode profil : fonctions dominantes exportées
✅ porte banc-performance verte
rc=0
  ```

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-performance.md'\ns=open(p,encoding='utf-8').read()\nold='''Le point **4 000 mots est plus rapide que le point 2 000** : il ne contient que **1 075**\nsyntagmes contre **1 006** — la segmentation globale du générateur S change avec le texte.\nLa pente … [1351 caractères tronqués]`

  ```
patched
  revue de documentation · 763 fiche(s) · 858 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
rc=0
  ```

- **bash** `{"command": "git add reports/rapport-performance.md && git commit --amend --no-edit 2>&1 | tail -20; echo \"rc=$?\"", "description": "Amend T4 commit with report fix", "timeoutMs": 300000}`

  ```
❌ commit refusé : 1 fait(s) stagé(s) sans docs/pilotage/en-cours.md
     · reports/rapport-performance.md
     → mettre l'état à jour, puis `git add docs/pilotage/en-cours.md`
  ⛔ commit refusé : un fait sans ligne d'état.
     mets docs/pilotage/en-cours.md à jour, puis :
     git add docs/pilotage/en-cours.md
rc=0
  ```

- **bash** `{"command": "git add docs/pilotage/en-cours.md && git commit --amend --no-edit 2>&1 | tail -20; echo \"rc=$?\"", "description": "Amend with state file staged", "timeoutMs": 300000}`

  ```
❌ commit refusé : 1 fait(s) stagé(s) sans docs/pilotage/en-cours.md
     · reports/rapport-performance.md
     → mettre l'état à jour, puis `git add docs/pilotage/en-cours.md`
  ⛔ commit refusé : un fait sans ligne d'état.
     mets docs/pilotage/en-cours.md à jour, puis :
     git add docs/pilotage/en-cours.md
rc=0
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/en-cours.md'\ns=open(p,encoding='utf-8').read()\ns=s.replace('**Mis à jour : 2026-11-15, 23 h 06 HNE (T4 : la performance)**',\n            '**Mis à jour : 2026-11-15, 23 h 12 HNE (T4 : la performance ; lecture des préfixes corrigée)**')\nopen(p,'w',en … [772 caractères tronqués]`
