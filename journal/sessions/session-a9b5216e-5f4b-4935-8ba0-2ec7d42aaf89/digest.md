# Session DSH — relecture

- identifiant : `session-a9b5216e-5f4b-4935-8ba0-2ec7d42aaf89`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-07 14:46:07
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J2.1 : la table de correspondance entre les **14 atomes** de Panini (∃ ∆ ∼ ↗ ⊙ ⧖ ◇ № ⊕ ⊗ λ ⊞ ≍ ≡) et nos **niveaux** (graphème, mot, pos, syntagme, phrase, pragmatique, discours, document). Lis `../Panini/README.md`, `../Panini-Research/`, `docs/theorie/genealogie-des-langues.md`. Produis `reports/rapport-atomes-niveaux.md` + JSON : 14 lignes, ce que chaque atome capte, quel niveau le porte, la mesure possible. Aucune écriture dans Panini.

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

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/ | head -50; echo ---; ls -la /home/stephane/Data13TB/stephane/GitHub/Panini 2>/dev/null | head -40; echo ---; ls -la /home/stephane/Data13TB/stephane/GitHub/Panini-Research 2>/dev/null | head -40", "description": "List workspace and Panini … [14 caractères tronqués]`

  ```
total 28
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 .
drwxr-xr-x. 1 stephane stephane  2454 31 oct 16:57 ..
drwxr-xr-x. 1 stephane stephane    80 31 jui 13:15 915-SPO (1).com
drwxr-xr-x. 1 stephane stephane   228 22 fév  2026 915-SPO.com
drwxr-xr-x. 1 stephane stephane   260  7 jun  2024 915-SPO.com-2
drwxr-xr-x. 1 stephane stephane    62  6 jun  2024 Ai_Docs
drwxr-xr-x. 1 stephane stephane    80  6 jun  2024 arduino-i2c-scanner
drwxr-xr-x. 1 stephane stephane   994  6 jun  2024 Arduino-IRremote
drwxr-xr-x. 1 stephane stephane    74  6 jun  2024 ArduinoNunchuk
drwxr-xr-x. 1 stephane stephane   732 31 jui 13:16 Biblio
drwxr-xr-x. 1 stephane stephane   404  6 jun  2024 Biblio-2
drwxr-xr-x. 1 stephane stephane   262  6 jun  2024 blue-pill-quickstart
drwxr-xr-x. 1 stephane stephane   248 11 mar  2026 bohemian-lab
-rwx--x--x. 1 stephane stephane  2421 18 oct 17:06 consolider_panini_research.sh
drwxr-xr-x. 1 stephane stephane   186  1 nov 16:42 contcal
drwxr-xr-x. 1 stephane stephane  1200 27 jan  2026 copilotage
drwxr-xr-x. 1 stephane stephane   248 27 jan  2026 copilotage-shared
drwxr-xr-x. 1 stephane stephane   408 16 mar  2026 DeDRM_tools
drwxr-xr-x. 1 stephane stephane   438
… [4661 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -30; echo ---; ls reports | tail -30; echo ---; ls docs/theorie | head -40", "description": "Check Qtrinet repo status and reports"}`

  ```
M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/superviseur.py
 m tools/structures
?? reports/rapport-s-paragraphes.md
---
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
traduction-udhr-propre-3b-fraeng.json
traduction-udhr-propre-7b-fraeng.json
traduction-udhr-propre-7b.json
universaux-mesures.json
xnli-14b.json
xnli-14b-l18.json
xnli-14b-l24.json
xnli-14b-l30.json
xnli-14b-l36.json
xnli-1.5b.json
xnli-1.5b-l14.json
xnli-1.5b-l22.json
xnli-32b.json
xnli-32b-l32.json
xnli-3b.json
xnli-3b-l30.json
xnli-entrainement-3b.json
xnli-mlp-3b.json
xnli-train-complet-3b.json
---
architecture-native.md
carte.md
contrat-bloc-langue.md
genealogie-des-langues.md
glossaire
glossaire.md
histoire.md
jeux-symboliq
… [186 caractères tronqués]
  ```

- **todo_write** `{"todos": [{"content": "Lire Panini/README.md et inventorier Panini-Research/ (atomes 14)", "status": "in_progress"}, {"content": "Lire docs/theorie/genealogie-des-langues.md et le modèle des niveaux Drave", "status": "pending"}, {"content": "Établir la table 14 atomes × niveaux + mesures possibles" … [195 caractères tronqués]`

  ```
Updated todo list: 4 pending, 1 in progress, 0 completed.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini && wc -l README.md && head -100 README.md", "description": "Read head of Panini README"}`

  ```
199 README.md
# Panini — noyau formel et sémantique computationnelle

[![Python](https://img.shields.io/badge/Python-3.13-green)](pyproject.toml)
[![Noyau](https://img.shields.io/badge/Noyau-CIC--lite_·_ℝ_localisé-blue)](research/docs/noyau/J4_CATALOGUE.md)
[![Licence](https://img.shields.io/badge/Licence-Voir_LICENSE-lightgrey)](LICENSE)

> Ce README décrit l'état **réel** du projet. Les chiffres vivent dans les rapports
> (`research/docs/noyau/VALIDATIONS.md`, `docs/journal-de-bord/`) — pas ici : un
> README qui vieillit ment.

## 1. Ce qu'est Panini

Deux niveaux, une seule discipline : **ce qui est affirmé doit être prouvé ou mesuré**.

- **Le noyau** — un système formel (CIC-lite en Python) qui *infère* et ne décrit jamais :
  termes, types dépendants, tactiques, et les **fondations mathématiques** (ℝ localisé par
  coupures de Dedekind). Ses certitudes sont des **théorèmes clos, vérifiés par la machine**.
- **NIPADA** — la couche *descriptive* : le tissu computationnel (graphe, dhātus, DTP),
  l'encyclopédie, les corpus, les lexiques candidats, les hypothèses et leurs degrés.
  Elle **décrit** ce que le noyau ne peut pas inférer.

**NIPADA (produit) = noyau + couche descripti
… [5001 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini && sed -n '100,199p' README.md", "description": "Read rest of Panini README"}`

  ```
> Panini décompose le texte en 14 atomes sémantiques, NIPADA le fait tourner comme un tissu
> computationnel — **algébrique, là où Drave est statistique**. Ils tiennent le système
> linguistique et généralisent une généalogie des langues, dialectes et styles.

Concrètement :

| Panini / NIPADA apporte | Drave apporte en retour |
|---|---|
| la **théorie** : atomes, universaux, généalogie des langues | les **mesures** : retrieval inter-langues, alignement sur les familles Glottolog |
| les **corpus** multilingues (Gutenberg, UDHR) et leur découpage | la **face statistique** de la comparaison, chiffrée et reproductible |
| le **noyau formel** (ce qui est prouvé) | le **moteur d'exécution** (flots, AER, matériel hétérogène) |

Règle de fonctionnement côté Drave : **à chaque cycle**, lire ce que Panini/NIPADA ont
publié (docs, journaux, `git log`) et confronter — la théorie va dans leur
`docs/genealogie-des-langues.md`, **jamais les chiffres** (qui restent dans `reports/`).

## 7. Écosystème et dépôts

Panini est un **dépôt hôte** : le laboratoire vit dans le submodule `research`, et les
composants d'infrastructure sont des submodules (`modules/`).

| Submodule | Rôle |
|---|---|
| `re
… [3477 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && ls -la; echo ---; ls philosophy-theory 2>/dev/null | head -60", "description": "List research root and philosophy-theory"}`

  ```
total 1452
drwxr-xr-x. 1 stephane stephane    2112 21 oct 08:37 .
drwxr-xr-x. 1 stephane stephane     814 22 oct 22:15 ..
-rw-r--r--. 1 stephane stephane    2842 21 oct 16:48 AGENTS.md
drwxr-xr-x. 1 stephane stephane     310  7 sep 12:47 archives
drwxr-xr-x. 1 stephane stephane      20 23 mai 19:31 archives_scripts_v1
drwxr-xr-x. 1 stephane stephane      38 27 jan  2026 autonomous-agents
drwxr-xr-x. 1 stephane stephane     572 28 mai 10:34 colab_results
drwxr-xr-x. 1 stephane stephane      50 27 jan  2026 config
-rw-r--r--. 1 stephane stephane    1335 18 oct 10:03 conftest.py
drwxr-xr-x. 1 stephane stephane     210 27 jan  2026 copilotage
drwxr-xr-x. 1 stephane stephane    8154  5 aoû 14:37 data
drwxr-xr-x. 1 stephane stephane     752 30 jun 20:45 deployments
drwxr-xr-x. 1 stephane stephane      16 27 jan  2026 diagrams_dhatu_cycles
drwxr-xr-x. 1 stephane stephane    1242 21 oct 08:36 docs
-rw-r--r--. 1 stephane stephane    4676 27 jan  2026 E1_REPORT_20251224.md
-rw-r--r--. 1 stephane stephane   13655 27 jan  2026 FONDAMENTAL_RESEARCH_ROADMAP_Q1_2026.md
-rw-r--r--. 1 stephane stephane    1971  7 sep 13:33 GATES_G1_G3_REPORT_2026-09-07.md
-rw-r--r--. 1 stephane stephane      33 11 
… [4943 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && grep -rl \"⊞\" --include=*.md . 2>/dev/null | head -40", "description": "Find docs mentioning atom symbols"}`

  ```
./docs/journal-de-bord/2026-07-14.md
./docs/journal-de-bord/2026-08-02.md
./docs/journal-de-bord/2026-08-03.md
./docs/journal-de-bord/2026-08-05.md
./docs/journal-de-bord/2026-08-07.md
./docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md
./docs/MEMO_ARCHITECTURE_NIPADA_v1.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && grep -rln \"V14\\|14 atomes\\|atomes sémantiques\" --include=*.md . 2>/dev/null | head -50", "description": "Find V14 atom docs"}`

  ```
./.github/copilot-instructions.md
./archives/filesystem_archive/cleanup/backup_20250906_154458/OPERATIONS/DevOps/scripts/investor_pitch_deck_20250816_112702.md
./archives/filesystem_archive/cleanup/backup_20250906_154458/OPERATIONS/DevOps/scripts/press_release_20250816_112702.md
./archives/filesystem_archive/cleanup/backup_20250906_154458/OPERATIONS/DevOps/PUBLICATION_LEANPUB_FINAL.md
./archives/filesystem_archive/cleanup/backup_20250906_154458/OPERATIONS/DevOps/PUBLICATION_MEDIUM_FINAL.md
./archives/filesystem_archive/cleanup/backup_20250906_154458/OPERATIONS/DevOps/demo-prototypage-rapide.md
./archives/filesystem_archive/cleanup/backup_20250906_154458/OPERATIONS/DevOps/roadmap.md
./archives/filesystem_archive/cleanup/backup_20250906_154458/OPERATIONS/DevOps/session-bilan-vision-realite.md
./archives/2025_prototypes/semantic-primitives/docs/PANINI_VS_NSM_COMPARISON.md
./archives/2025_prototypes/semantic-primitives/README.md
./archives/2025_prototypes/README.md
./misc/docs/ANALYSE_ENRICHIE_COMPLETE.md
./misc/docs/CONTRAINTES_COMPATIBILITE_APPLICATIONS.md
./misc/docs/GITHUB_PROJECT_FINAL_REPORT.md
./misc/docs/GITHUB_PROJECT_ISSUES_STRATEGIQUES.md
./misc/docs/PHASE1_HUMAN_TASK_GUIDE.
… [2452 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && grep -n \"⊞\\|∃\\|∆\\|∼\\|↗\\|⊙\\|⧖\\|◇\\|№\\|⊕\\|⊗\\|λ\\|≍\\|≡\" docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md | head -80", "description": "Locate atom symbols in cadres doc"}`

  ```
33:- **V7** (25 avril, §102) : Ajout de MODALITÉ=17, opérateur ⊗ de contextualisation. Univers ω = 2·3·5·7·11·13·17 = 510 510
113:| **Col 1 — Dynamique** | ∃(2)→↗(7)→◇(17)→⊗(29)→≍(41) | être→viser→pouvoir→faire→équilibrer |
114:| **Col 2 — Discernabilité** | ∆(3)→⊙(11)→№(19)→λ(31)→≡(43) | distinguer→se situer→compter→mapper→identifier |
115:| **Col 3 — Configuration** | ∼(5)→⧖(13)→⊕(23)→⊞(37)→??(47) | relier→situer→étendre→organiser→[SYSTÈME?] |
124:- **Vectoriel** : ↗ et ⊕ (direction, topologie)
125:- **Relationnel** : ∼, λ, ⊞ (opèrent sur d'autres atomes)
133:- **Probablement composites** : ⊗, λ, ≍, ≡ (s'expriment comme motifs des autres)
134:- **Questionnables** : ↗, №, ⊕, ⊞
135:- **Probablement irréductibles** : ∃, ∆, ∼ (Spencer-Brown) + ⊙, ⧖, ◇
141:- **Plus informationnels** (H élevée) : ∃(1.59), ⊙(1.32), ⊕(1.25) bits
142:- **Quasi redondants** (H faible) : ≍(0.12), λ(0.12), ↗(0.12) bits — candidats ablation
143:- **Corrélations fortes** : ∃↔⊙(0.59), ∼↔⊙(0.53), ⧖↔◇(0.46)
149:- ⊙(SUJET) est le plus « attractif » (5 liens entrants)
150:- ◇(MODALITÉ) est émetteur pur (3 sortants, 0 entrants)
151:- ↗ et λ n'ont qu'1 lien chacun — candidats réduction
154:- Q001 : L'agent est-il tou
… [1722 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && sed -n '1,160p' philosophy-theory/GRILLE_ABLATION_V14_v0.1.md", "description": "Read V14 ablation grid"}`

  ```
# Grille d'Ablation V14 — prédictions a priori (v0.1)

**Date** : 2026-08-28 (préparé à distance, téléphone)
**Statut** : prédictions **a priori** à comparer au verdict A1 du portefeuille (ablation systématique 14×, exécution station de travail)
**Références** : `PORTEFEUILLE_CANDIDATS_NOYAU_v1.0.md` (A1) · `DOCUMENT_DE_CONTEXTE_v2.0.md` (critère de sortie, iso) · corpus §334 (114 textes, 655 paires, R²=0.909139)
> **Note de cohérence (2026-09-09)** — la vision de référence est désormais `DOCUMENT_DE_CONTEXTE_v3.0.md` : le noyau y est défini comme **système formel** (les atomes V14 et consorts sont des **candidats révisables**), et le critère de sortie est la **fidélité générative** (sans copie de tokens) complétée d'invariants structurels, et non la restitution identique par ré-émission. Les renvois à la v2.0 ci-dessous sont conservés comme contexte historique.


---

## 1. Objet et protocole

**Question** : lequel des 14 atomes de V14 est-il **non porteur** — retirable sans perte (ni pour la loi H₀, ni pour la restitution DTP) ?

**Protocole A1** (sur la station) : pour chacun des 14 atomes, retirer la composante et **renormaliser les 13 restantes à somme 1** (la renormalisation 
… [6596 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && sed -n '95,180p' docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md", "description": "Read atom definition table in cadres"}`

  ```
#### Conséquences Architecturales

1. **Le projecteur V14 doit rester vectoriel** : la projection texte→V14 est fondamentalement une opération de découverte, pas de preuve. Le flou est nécessaire.
2. **Le SAT-solver doit être algébrique** : la reconstruction est fondamentalement une opération de preuve. Le déterminisme trinaire est nécessaire.
3. **La cristallisation est le point critique** : si le seuillage est mauvais, le SAT-solver hérite d'erreurs de la phase découverte. La qualité de la bascule détermine la qualité globale.
4. **Ne pas hybrider les modes dans la même couche** : les 3 échecs embedding (§655-§658) venaient de tentatives d'injecter du vectoriel (GloVe, WordNet) dans la phase de reconstruction (qui doit être algébrique).
5. **Le graphe est le pont** : le graphe généalogique (15 881 nœuds) contient à la fois des poids flous (similarités cosinus) et des relations discrètes (arêtes DEP/COORD/OPP). Il est le lieu naturel de la cristallisation.

#### Implications pour la Pensée Robuste

Une intelligence qui ne fait QUE du vectoriel (LLM) a de l'intuition mais pas de garantie (hallucinations). Une intelligence qui ne fait QUE de l'algébrique (système expert) a des garan
… [3438 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l docs/theorie/genealogie-des-langues.md && sed -n '1,120p' docs/theorie/genealogie-des-langues.md", "description": "Read genealogie doc head"}`

  ```
74 docs/theorie/genealogie-des-langues.md
# La généalogie des langues, des dialectes et des styles

> **Ce que cette page est.** La **théorie** de la structure généalogique qui doit organiser l'**étage entrée-sortie** (nom historique : « couche commune »)
> entrée-sortie de Drave, et ce que les projets complémentaires **Panini** et **Nipada** ont établi sur elle. Les
> mesures de Drave sont dans [`reports/07-mesures-couche-commune.md`](../../reports/07-mesures-couche-commune.md).
> *À relire et à mettre à jour à chaque cycle : Panini et Nipada sont des sources vivantes.*

## 1. Pourquoi une généalogie

Une couche entrée-sortie ne peut pas être « riche en langues » au sens d'une **liste**. Les langues forment une
**structure** : des familles, des branches, des dialectes, des styles, et des **traductions** qui traversent tout
cela. Si la structure est réelle, elle doit se voir dans les états du modèle — et si elle ne s'y voit pas, c'est le
modèle qui est incomplet.

La hiérarchie à couvrir, du plus large au plus fin :

| niveau | exemple | ce qui varie |
|---|---|---|
| **famille** | indo-européen, nigéro-congolais, austronésien | le système, la morphologie |
| **branche** | roman, s
… [3675 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"syntagme\" --include=*.md --include=*.json docs reports journal 2>/dev/null | head -40", "description": "Find docs with syntagme"}`

  ```
docs/pilotage/chantiers.md
docs/pilotage/plan-travail.md
docs/pilotage/roadmap.md
docs/pilotage/semaine-autonome.md
docs/theorie/synthese/07-modeles-alternatifs-entree-sortie.md
docs/theorie/modele-natif.md
docs/theorie/pre-traitement-linguistique.md
docs/theorie/contrat-bloc-langue.md
docs/implantation/moteur-de-pensee.md
docs/implantation/bloc-linguistique.md
docs/produit/exemples.md
docs/produit/README.md
reports/bloc-linguistique.json
reports/rapport-bloc-linguistique.md
reports/pensee-gold-linguistique.json
reports/rapport-pensee-gold-linguistique.md
reports/rapport-pensee-gold-200.md
reports/pensee-gold-200.json
reports/rapport-pensee-gold-200-subsets.md
reports/pensee-gold-subsets.json
reports/rapport-pensee-gold-complexes.md
reports/pensee-gold-complexes.json
reports/rapport-pensee-gold-complexes20.md
reports/pensee-gold-complexes20.json
reports/rapport-pensee-gold-complexes50.md
reports/pensee-gold-complexes50.json
reports/rapport-pensee-gold-complexes100.md
reports/pensee-gold-complexes100.json
reports/rapport-pensee-gold-342.md
reports/pensee-gold-342.json
reports/rapport-pensee-anaphore-68.md
reports/rapport-pensee-anaphore-103.md
reports/rapport-pensee-segmenteur.md
re
… [280 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"graphème\\|graphème\" --include=*.md --include=*.json docs reports journal 2>/dev/null | head -40", "description": "Find docs with grapheme level"}`

  ```
docs/pilotage/roadmap.md
docs/theorie/contrat-bloc-langue.md
docs/implantation/bloc-linguistique.md
docs/produit/exemples.md
docs/produit/README.md
reports/bloc-linguistique.json
reports/rapport-bloc-linguistique.md
reports/rapport-pensee-miroir.md
reports/rapport-pensee-miroir-pos.md
reports/rapport-pensee-miroir-espaces.md
reports/rapport-pensee-miroir-resume.md
reports/rapport-pensee-miroir-reponse.md
reports/rapport-pensee-reponse-contenu.md
reports/rapport-pensee-frontiere-71.md
reports/rapport-pensee-fusion-reparee.md
reports/rapport-produit-bloc-l.md
reports/pensee-produit-bloc-l.json
reports/pensee-fiabilite-produit.json
reports/rapport-fiabilite-produit.md
reports/pensee-restitution-v0.json
reports/rapport-restitution-v0.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/rapport.md
journal/sessions/abb58991-fe0a-4d6e-b039-6552b09f8454/digest.md
journal/sessions/abb58991-fe0a-4d6e-b039-6552b09f8454/rapport.md
journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/digest.md
journal/sessions/f55ccb7b-481e-4ab6-b5b4-331dc6ff2238/rapport.md
journ
… [765 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,180p' docs/theorie/contrat-bloc-langue.md", "description": "Read contrat bloc langue"}`

  ```
# Le contrat du bloc langue — un seul contrat, quatre modes

> **Rôle.** Ce document est le **premier livrable de L** : le contrat d'entrée/sortie que doivent
> respecter l'**heuristique** et le **neuronal** pour être **substituables** ou **parallèles**.
> Il ne remplace pas une mesure : il fixe l'interface, les niveaux, les modes, la trace, le coût
> et la porte. Les chiffres cités viennent des fiches ; le contrat, lui, ne dépend pas d'eux.
>
> **Ce qu'il n'est pas.** Un plaidoyer « le CPU remplace le réseau » ; ni un contrat de
> **sémantique** (la couche sémantique est un autre bloc, `CoucheSemantique`), ni un contrat de
> **document** (R). Le contrat de L est celui de l'**annotation linguistique**, du graphème au
> pragmatique.

## 1. L'interface

```python
class BlocLinguistique(Protocol):
    nom: str

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation: ...
```

- **Entrée** : `texte` (chaîne), `langue` (code BCP-47 ou `None` → `und`), `contexte` (optionnel,
  pour la pragmatique et la coréférence).
- **Sortie** : une **`Annotation`** unique, quel que soit le mode. C'est elle qui rend la
  substitution pos
… [7026 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"graphème\\|mot\\|pos\\|syntagme\\|phrase\\|pragmatique\\|discours\\|document\" docs/theorie/contrat-bloc-langue.md | head -60", "description": "Locate levels in contrat"}`

  ```
3:> **Rôle.** Ce document est le **premier livrable de L** : le contrat d'entrée/sortie que doivent
10:> **document** (R). Le contrat de L est celui de l'**annotation linguistique**, du graphème au
11:> pragmatique.
24:  pour la pragmatique et la coréférence).
26:  substitution possible : le lecteur ne sait pas qui a étiqueté, il lit la même structure.
60:`NIVEAUX = ("graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
61:"pragmatique", "document")`.
63:- **graphème** : script, normalisation, direction, ponctuation.
65:- **mot** : frontières, nombres, dates, URLs.
66:- **pos** : les classes (`DET`, `NOUN`, `VERB`, `ADJ`, `ADV`, `PREP`, `PRON`, `AUX`, `CONJ`, …).
67:- **syntagme** : `GN`, `GV`, `GP`, `REL`, `SUB`, rôles, attachements.
68:- **phrase** : frontières, type, négation, modalité.
69:- **discours** : coréférence, chaînes, liens entre phrases.
70:- **pragmatique** : acte, négation, modalité, double sens.
71:- **document** : structure, régions, provenance (le contrat de R s'y branche).
81:| **neuronal** | `NeuronalLLMPOS`, `NeuronalLLMChunks`, `NeuronalLLMPragmatique`, `NeuronalLLMCompose` | tranche l'ambigu (POS, BIO, pragmatique) | un appel par phrase et 
… [641 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l docs/theorie/pre-traitement-linguistique.md && sed -n '1,220p' docs/theorie/pre-traitement-linguistique.md", "description": "Read pre-traitement linguistique"}`

  ```
350 docs/theorie/pre-traitement-linguistique.md
# La couche heuristique — ce que le CPU étiquette avant le réseau

> **Rôle.** Cette note analyse une **couche linguistique de prétraitement par heuristiques** : ce
> qu'elle peut étiqueter, du mot au document, en plusieurs langues, et ce qu'elle **retire au
> réseau de neurones**. Elle ne remplace pas une mesure : elle fixe les niveaux, la cascade, le
> coût et le protocole. Les chiffres cités viennent des fiches ; les **projections** sont dites
> comme telles.
>
> **Ce qu'elle n'est pas.** Un plaidoyer « le CPU remplace le réseau ». Le CPU étiquette la
> **surface** ; le réseau tranche l'**ambiguïté** et le **sens**. La cascade se juge sur sa
> **précision par unité de calcul**, pas sur son débit brut.

## 1. La thèse en trois idées

1. **Le réseau paie la surface.** Une part du travail d'un modèle de langue n'est pas du sens :
   c'est de la normalisation Unicode, de la détection de script et de langue, des frontières de
   mots et de phrases, des classes fermées, des régions de document. Ces opérations sont
   **locales, déterministes et bon marché** : un CPU les fait à des ordres de grandeur qui n'ont
   rien à voir avec un passa
… [13573 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,140p' reports/rapport-bloc-linguistique.md; echo ===; head -60 reports/bloc-linguistique.json", "description": "Read bloc linguistique report and JSON shape"}`

  ```
# Le bloc linguistique — 398 langues au niveau langue, un contrat pour l'heuristique et le neuronal

> **Ligne de roadmap** : **R0.7** (proposition — la couche linguistique de surface) · **Date** :
> 2026-11-01 · **Verdict** : ✅ **le contrat tient** : neuf niveaux, deux implémentations
> substituables, un parallèle et une cascade, une activation sémantique à **51–76 %** ; la
> **langue** est mesurée à **0,9687** sur **398 langues** (script **1,0000**, profils permutés
> **0,0022**). ⚠️ **les niveaux profonds n'ont pas de gold** et le **modèle neuronal réel n'est
> pas qualifié** (le `llama-cli` local a expiré) : la couverture est **déclarée**, pas prouvée.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`porte-bloc-linguistique.sh`](../tools/porte-bloc-linguistique.sh),
> [`test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_linguistique.py),
> JSON [`bloc-linguistique.json`](bloc-linguistique.json). Contrat :
> [`bloc-linguistique.md`](../docs/implantation/bloc-linguistique.md).

## 1. La question

Peut-on avoir **un seul bloc** qui étiquette du **graphème** à la **pragmatique**, avec une
version **heuristique CPU** et une version **n
… [7282 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"J2\" docs/pilotage reports journal --include=*.md 2>/dev/null | head -40", "description": "Find J2 references"}`

  ```
docs/pilotage/semaine-autonome.md:89:| **J2 · 08/11** | matin | **Panini I** : l'inventaire croisé, la **table atomes ↔ niveaux** | la table, 20 exemples mesurés |
reports/rapport-inventaire-panini.md:233:ne doivent pas entrer dans la table J2.
reports/rapport-inventaire-panini.md:408:   atomes ↔ niveaux Drave + 20 exemples mesurés (le J2 du plan de semaine).
reports/rapport-inventaire-panini.md:433:### 4.1 Le corpus UDHR et la généalogie — **la plus mûre, à faire en J2**
reports/rapport-inventaire-panini.md:490:4. **Trois vocabulaires** : 14/9 (Research) / 34/7 (Panini-FS) / 9 (docs hôte). La table J2 doit
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:4998:### J2 vraie suite : 400 octets de wikitext apres 600 octets de contexte
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:5006:### J2 vraie suite : 400 octets de wikitext apres 600 octets de contexte
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:5022:- **bash** `{"command": "sleep 270; cat /tmp/controles3_oss.out", "description": "Wait for J2/J3 results", "timeoutMs": 330000}`
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:5027:### J2 vraie suite : 400 octets de
… [5805 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"atome\" docs reports --include=*.md | head -40", "description": "Find atom references in Qtrinet"}`

  ```
docs/methode/panini-nipada.md
docs/pilotage/semaine-autonome.md
docs/theorie/genealogie-des-langues.md
docs/implantation/bloc-maths.md
reports/rapport-inventaire-panini.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' reports/rapport-inventaire-panini.md", "description": "Read inventaire Panini head"}`

  ```
# Inventaire Panini — état daté du 7 novembre 2026

> **Mission.** Inventaire complet et daté des 14 dépôts de l'écosystème Panini pour préparer le
> chantier autonome d'une semaine d'intégration avec Drave (`../Qtrinet/`, 7 → 14/11/2026).
> **Lecture seule** : aucun commit, aucun fichier de code, de doc ou de configuration modifié,
> `git status` lancé avec `--no-optional-locks`. Un seul effet de bord, documenté au §5.7 : un
> `sqlite3` de lecture a checkpointé le WAL d'une base de corpus. Les deux seuls fichiers écrits sont ce rapport et son JSON.
>
> **Méthode.** `git log` / `status` / `submodule status`, lecture des README, docs et journaux de
> bord, comptages (`find`, `du`, `wc`), lecture directe des artefacts JSON. **Aucune suite de tests
> n'a été exécutée** : les leurs coûtent de 45 min à 3 h 30. Les chiffres cités sont ceux que
> Panini **publie**, avec leur date et leur chemin — ils sont repris, pas re-mesurés.

---

## 0. Ce qu'il faut retenir

1. **Un seul dépôt est vivant au sens fort : `Panini/research`** (= `Panini-Research`, qui est un
   lien symbolique vers lui). 1 622 commits, dernier le **25/10/2026**, 182 194 lignes de Python,
   50 124 lignes de noyau formel.
… [7478 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '380,520p' reports/rapport-inventaire-panini.md", "description": "Read inventaire Panini conclusions"}`

  ```
données comparables, issues de la **même source** (`eric-muller/udhr`, fichiers `udhr_XXX.xml`).
- Le plus riche : **signatures §334** — `pairs334_axes_v1.json` donne, pour chaque paire,
  `d_topo`, `d_lex`, `d_H`, `cos`, `trad_*`, `lang_*` : une table prête pour un test de retrieval.
- Le plus « prêt à prouver » : **corpus d'or CIC** (`corpus_dor_cic_v1.json`, 46 Ko + TSV) : 3 defs,
  21 consts, **42 entrées** (36 `accepte`, 6 `rejette`), chacune avec preuve et type sérialisés en
  de Bruijn (hex) et une empreinte SHA-256. Sa doctrine : « toute implémentation doit reproduire
  exactement ces verdicts à partir de cet artefact seul ».

### 3.5 Interfaces et données partageables (ce que Drave peut consommer)

| Surface | Chemin | Format | Dépendances | Maturité |
|---|---|---|---|---|
| Signatures V14 par texte | `nipada/falsification/analytic_sigs_v1.json` | `{texte: {ATOME: float}}` | aucune | **haute** |
| Lexiques V14 | `data/v14_lexicon_enriched.json` (3,9 Mo) | `{lang: {ATOME: [mots]}}` | aucune | haute (qualité à vérifier) |
| Paires §334 | `nipada/falsification/pairs334_axes_v1.json` | 655 objets `{a,b,d_topo,d_lex,d_H,cos,trad,lang}` | aucune | **haute** |
| Corpus d'or CIC 
… [8102 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && grep -rn \"ÊTRE\\|DIFFÉRENCE\\|SYMÉTRIE\\|ÉQUATION\" --include=*.md docs philosophy-theory nipada/api 2>/dev/null | head -40", "description": "Find atom name table"}`

  ```
docs/journal-de-bord/2026-04-22.md:181:ÊTRE ←→ DIFFÉRENCE ←→ RAPPORT
docs/journal-de-bord/2026-04-22.md:195:ÊTRE         = 2  ┐
docs/journal-de-bord/2026-04-22.md:196:DIFFÉRENCE   = 3  ├── triangle irréductible (3 aspects du même acte)
docs/journal-de-bord/2026-04-22.md:212:| ÊTRE | "il y a…" | Présence d'une région | Existence d'un état |
docs/journal-de-bord/2026-04-22.md:213:| DIFFÉRENCE | négation, privatifs | Magic bytes | États quantiques distincts |
docs/journal-de-bord/2026-04-22.md:231:| ℝ réels | 1D | triangle (ÊTRE+DIFFÉRENCE+RAPPORT) | — |
docs/journal-de-bord/2026-04-22.md:267:$$\text{ÊTRE} \times \text{DIFFÉRENCE} \times \text{RAPPORT} = 2 \times 3 \times 5 = 30$$
docs/journal-de-bord/2026-04-22.md:272:- COMPOSITION = ÊTRE × RAPPORT = $2 \times 5 = 10$
docs/journal-de-bord/2026-04-22.md:273:- TRANSFORMATION = ÊTRE × DIFFÉRENCE × ORIENTATION = $2 \times 3 \times 7 = 42$
docs/journal-de-bord/2026-04-22.md:275:- CAUSALITÉ = ÊTRE × DIFFÉRENCE × RAPPORT × ORIENTATION = $2 \times 3 \times 5 \times 7 = 210$
docs/journal-de-bord/2026-04-22.md:277:Mais ORIENTATION est-elle irréductible ? Tentative de réduction : RAPPORT × DIFFÉRENCE = $5 \times 3 = 15$. Ça lit "un rapport qui 
… [4012 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '60,110p' docs/pilotage/semaine-autonome.md; echo ===; sed -n '1,120p' docs/methode/panini-nipada.md", "description": "Read J2 plan and panini-nipada method"}`

  ```
| # | intégration | livrable | contrôle négatif | risque |
|---|---|---|---|---|
| 1 | **UDHR + généalogie** (même source XML des deux côtés) | table iso3/famille/branche + échantillon 20 langues | familles différentes = retrieval faible ; sœurs = fort | codes ISO (007/008 vs iso3) |
| 2 | **atomes V14 ↔ niveaux** (44 œuvres × 14 flottants, JSON pur) | table + 20 exemples mesurés | permuter les colonnes doit tuer le prédictif | signature lexicale : contrôler la date |
| 3 | **corpus d'or CIC** (42 verdicts, preuve + sha256) | vérificateur indépendant, 42/42 | altérer un octet doit être rejeté | aucun (le plus vérifiable) |

**Trop immature pour la semaine** : le produit NIPADA, le noyau comme service, les 11 modules,
Panini-FS, l'API REST.

### 2.4 La surface d'intégration

| Panini / NIPADA apporte | Drave apporte | premier livrable commun |
|---|---|---|
| les **14 atomes**, les universaux | nos **niveaux** (POS, syntagmes, pragmatique) et leurs mesures | une **table de correspondance** atomes ↔ niveaux, sur un corpus commun |
| les **corpus** (Gutenberg, UDHR) et leur découpage | le **retrieval** inter-langues (mesures 49) | une mesure de retrieval **à époque contrôlée** |
| la 
… [4429 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && python3 -c \"\nimport json\np='nipada/falsification/analytic_sigs_v1.json'\nd=json.load(open(p))\nprint(type(d), len(d))\nks=list(d)[:5]\nfor k in ks: print(k, json.dumps(d[k], ensure_ascii=False)[:300])\n\"", "description":  … [37 caractères tronqués]`

  ```
<class 'dict'> 44
2_esdras {"ÊTRE": 0.07446500282604852, "DIFFÉRENCE": 0.013816044014481109, "RAPPORT": 0.10099345547363615, "ORIENTATION": 0.005331763602619648, "SUJET": 0.14124697298283334, "TEMPS": 0.05189835957545314, "MODALITÉ": 0.02705634807902917, "NOMBRE": 0.14932406971800052, "ESPACE": 0.04847053574653187, "OPÉRATION
aristotle_categories {"ÊTRE": 0.14598002759025833, "DIFFÉRENCE": 0.03854854561582201, "RAPPORT": 0.0765354958116522, "ORIENTATION": 0.005632418801409541, "SUJET": 0.17885306226299458, "TEMPS": 0.05455181280253287, "MODALITÉ": 0.0543486933929131, "NOMBRE": 0.0919066931460675, "ESPACE": 0.0584934401577834, "OPÉRATION": 0.
aristotle_de_caelo {"ÊTRE": 0.1403058077327118, "DIFFÉRENCE": 0.028694654081925678, "RAPPORT": 0.06535243912604145, "ORIENTATION": 0.00881809751666501, "SUJET": 0.14649945328756767, "TEMPS": 0.09177787259739713, "MODALITÉ": 0.04111184069593867, "NOMBRE": 0.07061017857516651, "ESPACE": 0.07959109637719919, "OPÉRATION":
aristotle_nicomachean_ethics {"ÊTRE": 0.12798570044607704, "DIFFÉRENCE": 0.036858669905749535, "RAPPORT": 0.06967430078078224, "ORIENTATION": 0.00675712334483951, "SUJET": 0.20593730200160879, "TEMPS": 0.07110840426297166, "MODALI
… [427 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && grep -rn \"STRUCTURE.*37\\|FONCTION.*31\\|ESPACE.*23\\|NOMBRE.*19\" --include=*.md docs philosophy-theory 2>/dev/null | head -30", "description": "Find full atom name/prime table"}`

  ```
docs/journal-de-bord/2026-04-25.md:942:| NOMBRE | 19 | objet quantitatif pur (entier, réel, complexe) |
docs/journal-de-bord/2026-04-25.md:943:| ESPACE | 23 | variété/structure topologique avec dimension |
docs/journal-de-bord/2026-04-25.md:945:| FONCTION | 31 | morphisme typé entre objets |
docs/journal-de-bord/2026-04-25.md:946:| STRUCTURE | 37 | ensemble + axiomes (groupe, anneau, champ) |
docs/journal-de-bord/2026-04-25.md:1140:- ✅ **§120 — Noyau primal T_O_math (V8) : 7 nouveaux atomes premiers (NOMBRE=19, ESPACE=23, OPÉRATION=29, FONCTION=31, STRUCTURE=37, SYMÉTRIE=41, ÉQUATION=43) prolongeant V7 → V14. ω_V14 = 13 082 547 408 856 533 030. 8 molécules-seed (AXIOME, THÉORÈME, PREUVE, GROUPE, VARIÉTÉ, TENSEUR, FONCTIONNELLE, AUTOMORPHISME) avec produits factoriels uniques. Justification orthogonalité sémantique : aucune des 7 catégories n'est dérivable des 6 autres ni des 7 V7. Bourbaki + catégories ne fusionnent jamais ces 7 sans perte.**
docs/journal-de-bord/2026-04-25.md:1141:- ✅ **§121 — Stratification numérique ℕ → 𝕆 (`number_strata_v121.json`) : signatures factorisées par ratios *exactement égaux aux primes* (ℕ=19, ℤ=38=19×2 +ÊTRE, ℚ=190=38×5 +RAPPORT, ℝ=2470=190×13 +TEMPS
… [4108 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && sed -n '180,240p' docs/journal-de-bord/2026-04-22.md; echo ===; sed -n '440,470p' docs/journal-de-bord/2026-04-22.md", "description": "Read atom definitions in journal April 22"}`

  ```
```
ÊTRE ←→ DIFFÉRENCE ←→ RAPPORT
```

Chacun des trois présuppose les deux autres. C'est le nœud d'interdépendance : on ne peut pas réduire davantage sans perdre la possibilité même de décrire quoi que ce soit.

### L'Ur-primitif = 1 (neutre multiplicatif)

En mathématiques, 1 n'est pas un nombre premier. Il est le fond neutre, la condition de possibilité de tout produit. Dans nipada : l'acte de distinction lui-même (Spencer-Brown's mark). Il n'entre jamais dans les produits parce qu'il est la condition de possibilité de tout produit.

### Architecture des primes révisée

```
Ur-primitif = 1              ← l'acte de distinction (Spencer-Brown)
──────────────────────────────────────────────────────
ÊTRE         = 2  ┐
DIFFÉRENCE   = 3  ├── triangle irréductible (3 aspects du même acte)
RAPPORT      = 5  ┘
──────────────────────────────────────────────────────
COMPOSITION    = 7  ┐
TRANSFORMATION = 11 ├── second ordre : opérations sur le triangle
RÉCURSION      = 13 ┘
──────────────────────────────────────────────────────
Tout le reste → produits de primes
```

### Convergence cross-domaine validée

La même structure traverse tous les domaines :

| Prime | Langage naturel | Format b
… [3445 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && sed -n '590,640p' docs/journal-de-bord/2026-08-03.md; echo ===; sed -n '930,960p' docs/journal-de-bord/2026-04-25.md", "description": "Read atom table August and April 25"}`

  ```
**Conséquence** : Le pipeline de reconstruction doit fonctionner SANS bigrammes.
Le graphe sémantique (nœuds V14 + arêtes) est la SEULE source d'information pour
le SAT-solver. Si ça ne marche pas sans bigrammes, c'est que V14 est incomplet —
pas qu'il faut ajouter des bigrammes.

### Décisions

1. **V14 = hypothèse falsifiable.** Le notebook la présente comme telle.
2. **Dhātus = patterns, pas atomes.** Retirés du statut atomique.
3. **Ablation = priorité.** Dès que la reconstruction marche, tester chaque atome.
4. **Le gap similarité vs sens est le problème théorique #1.** À adresser.

---

## Classification périodique V14 + NP-complétude sans dhātus

### Table périodique V14 (Mendeleev)

V14 organisé en 3 colonnes × 5 périodes :

| Période | Col 1 (Dynamique) | Col 2 (Discernabilité) | Col 3 (Configuration) |
|---------|-------------------|------------------------|----------------------|
| I | ∃ ÊTRE (2) | ∆ DIFFÉRENCE (3) | ∼ RAPPORT (5) |
| II | ↗ ORIENTATION (7) | ⊙ SUJET (11) | ⧖ TEMPS (13) |
| III | ◇ MODALITÉ (17) | № NOMBRE (19) | ⊕ ESPACE (23) |
| IV | ⊗ OPÉRATION (29) | λ FONCTION (31) | ⊞ STRUCTURE (37) |
| V | ≍ SYMÉTRIE (41) | ≡ ÉQUATION (43) | **? (47)** ← MANQUANT 
… [3788 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"niveau\\|atome\\|couche\\|étage\" docs/theorie/glossaire.md | head -60", "description": "Check glossary vocabulary"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' docs/theorie/glossaire.md", "description": "Read glossary head"}`

  ```
# Glossaire raisonné de Drave

Ce document explique **tout le vocabulaire** employé dans `docs/` et `reports/`, pour quelqu'un qui ne
connaît ni les grands modèles de langage, ni le matériel, ni le vocabulaire de la
mesure de performance. Il se lit seul : chaque notion est définie sur place, et
chaque définition renvoie au fichier du dépôt qui l'emploie.

---

## Mode d'emploi

**Ce que contient une entrée.** Chaque entrée suit le même patron :

> **Terme** *(forme développée française ; forme anglaise)* — définition en une à
> trois phrases, sans prérequis. La définition dit **où** le moteur s'en sert
> (fichier, outil ou drapeau du dépôt, avec un numéro de ligne quand il aide) et,
> quand une source externe stable existe, la référence **Réf.** (article,
> spécification, documentation officielle).

**Conventions de lecture.**

- `chemin:ligne` renvoie à un fichier **du dépôt**, à la ligne indiquée. Exemple :
  `docs/theorie/vision.md:34`.
- Les liens externes pointent vers des articles ou des spécifications ; quand je
  n'ai pas pu vérifier l'adresse, je cite l'article **par son titre et ses
  auteurs, sans lien** — c'est une règle du dépôt, on n'invente pas d'URL.
- Un terme qui 
… [3229 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"graphème\\|syntagme\\|pragmatique\" docs/theorie/glossaire.md | head -30", "description": "Search glossary for linguistic levels"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports | grep -i \"panini\\|atome\\|niveau\" | head -30; echo ===; ls reports | grep -i \"inventaire\"", "description": "List panini-related reports"}`

  ```
pensee-defaut-niveau.json
pensee-inventaire-panini.json
pensee-quatre-modes-niveau.json
rapport-inventaire-panini.md
rapport-pensee-defaut-niveau.md
===
inventaire-donnees-entrainement.json
inventaire-donnees-entrainement.md
n3-inventaire.json
pensee-inventaire-panini.json
rapport-inventaire-panini.md
rapport-n3-inventaire.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -80 reports/pensee-inventaire-panini.json; echo ===; python3 -c \"\nimport json\nd=json.load(open('reports/pensee-inventaire-panini.json'))\nprint(type(d))\nprint(list(d)[:20])\n\"", "description": "Inspect inventaire JSON shape … [2 caractères tronqués]`

  ```
{
  "fiche": "reports/rapport-inventaire-panini.md",
  "date": "2026-11-07",
  "heure": "10:35 HNE",
  "branche": "s/v7",
  "head": "a2ad039d",
  "head_date": "2026-11-07",
  "mission": "Inventaire complet et date des 14 depots Panini, en lecture seule, pour preparer le chantier autonome d'une semaine d'integration avec Drave (7-14/11/2026) : etat git, role, docs cles, chantiers ouverts, portes et chiffres publies, lien Drave, donnees partageables. Deux fichiers neufs, aucun commit, aucun fichier de code/doc/config modifie ; seul effet de bord, un checkpoint SQLite sur une base de corpus (documente).",
  "verdict": "Un seul depot est vivant au sens fort : Panini/research (= Panini-Research, symlink), 1622 commits, dernier le 2026-10-25, 182194 lignes de Python, noyau formel + NIPADA. L'hote Panini est un conteneur de sous-modules, actif jusqu'au 2026-10-22. Sept des treize autres depots sont des echafaudages (LICENSE + README de 1 a 4 lignes + templates GitHub) ; seuls Panini-FS (Rust, 581 fichiers, ligne divergente 7 dhatu / 34 atomes), OntoWave (TS, 81 fichiers, sous-module sans clone standalone) et ExecutionOrchestrator (CLI + 3 drivers) ont du code. Le lien avec Drave n'existe 
… [4766 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,60p' docs/methode/resultats.md; echo ===; sed -n '1,80p' docs/methode/rangement.md", "description": "Read result and filing methods"}`

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
… [7709 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' docs/pilotage/en-cours.md; echo ===; grep -n \"J2.1\\|atomes\\|Panini\" docs/pilotage/en-cours.md docs/pilotage/chantiers.md docs/pilotage/plan-travail.md docs/pilotage/roadmap.md | head -60", "description": "Check cur … [32 caractères tronqués]`

  ```
# En ce moment

**Mis à jour : 2026-11-07, 14 h 40 HNE (heure locale, EST).**

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
… [4830 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/chantier/superviseur.py etat 2>&1 | head -60", "description": "Check chantier supervisor state"}`

  ```
chantier : Semaine 07/11 → 14/11 — le produit et l'intégration Panini · depuis 2026-11-07 10:44:20
session : (aucune — dsh créera une session neuve)
budget consommé : 8823.199999999999 s · lancements : 6
STOP : absent

  [fait    ] J0     j0 — Le contrôle du superviseur
  [fait    ] J1.1   j1 — r035 : la relative zéro
  [echec   ] J1.2   j1 — La convention des GV
  [fait    ] J1.3   j1 — Le schéma v2
  [fait    ] J1.4   j1 — La restitution v0
  [a_faire ] J2.1   j2 — Panini I — la table atomes ↔ niveaux
  [a_faire ] J2.2   j2 — Panini I — le corpus commun
  [a_faire ] J3.1   j3 — Panini II — le retrieval à époque contrôlée
  [a_faire ] J3.2   j3 — Panini II — la généalogie à deux faces
  [a_faire ] J4.1   j4 — Coordination N2 — le mètre RoPE
  [a_faire ] J4.2   j4 — Coordination S — les 11 verdicts
  [a_faire ] J4.3   j4 — Coordination R — le tagger sur 612
  [a_faire ] J4.4   j4 — Coordination A — A6.2 et A8.3b2
  [a_faire ] J5.1   j5 — Le rapport de semaine
  [a_faire ] J5.2   j5 — La passe complète et le tag
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/chantier/superviseur.py --help 2>&1 | head -60; echo ===; grep -rn \"J2.1\\|atomes\" work/chantier 2>/dev/null | head -20; echo ===; ls work/chantier 2>/dev/null", "description": "Inspect supervisor usage and task files … [2 caractères tronqués]`

  ```
usage: superviseur.py [-h] {etat,prochaine,executer,boucle,stop,reprendre} ...

superviseur.py — le méta-harnais du chantier autonome : file de tâches,
exécution, vérification.

positional arguments:
  {etat,prochaine,executer,boucle,stop,reprendre}

options:
  -h, --help            show this help message and exit
===
work/chantier/journal.log:17:2026-11-07 14:46:05 · ▶ J2.1 — Panini I — la table atomes ↔ niveaux (timeout 5400 s)
===
boucle.log
etat.json
journal.log
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -8; echo ===; git status --short | head -20", "description": "Check recent commits and status"}`

  ```
8eb0cc49 B13 — RESTITUTION v0 : 46/46 SURFACES EXACTES, MIROIR STRICT 0,1087, LE MIROIR TROUVE LES SAUTS DE LIGNE
9a259953 B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC), v1 TOUJOURS LUE
92652984 B13 — LA CONVENTION DES GV : SUJET HORS DU GV + ADVERBE FINAL, F1 0,7549 → 0,7902, ATTACHEMENT 237/238 ; 183/183
25a6c0ff B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183
d7469b5c INDEX — RÉGÉNÉRÉ APRÈS L'INVENTAIRE PANINI (702 FICHES) ; ÉTAT HORODATÉ
34fdd4ef DOCS — README T1 TENU (DEUX LIGNES LONGUES RACCOURCIES)
fffbbe5d PANINI — L'INVENTAIRE INTÉGRÉ AU PLAN : 14 DÉPÔTS, 7 AXES, 14 ATOMES, 9 CORPUS, TROIS INTÉGRATIONS MÛRES (UDHR+GÉNÉALOGIE, ATOMES↔NIVEAUX, CORPUS CIC) AVEC LEURS CONTRÔLES NÉGATIFS
f93ddc60 DOCS — README T1 : DEUX LIGNES RACCOURCIES, BUDGET TENU
===
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/superviseur.py
 m tools/structures
?? reports/rapport-s-pa
… [12 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nd=json.load(open('work/chantier/etat.json'))\nprint(type(d), list(d)[:20])\nprint(json.dumps(d, ensure_ascii=False, indent=1)[:4000])\n\"", "description": "Inspect supervisor state JSON"}`

  ```
<class 'dict'> ['taches', 'depuis', 'budget_s', 'lancements']
{
 "taches": {
  "J1.1": {
   "titre": "r035 : la relative zéro",
   "statut": "fait",
   "debut": "2026-11-07 12:41:17",
   "duree_s": 1347.7,
   "code_agent": 0,
   "acceptation": [
    "✅ test -f reports/rapport-r035.md && echo FICHE-OK",
    "✅ python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?"
   ],
   "sortie_agent": "avant | après |\n|---|---:|---:|\n| exact / labels | 236/237 | **237/238** |\n| couverture | 0,9916 | **0,9958** |\n| POS | 0,8625 | **0,8625** |\n| F1 syntagmes | 0,7533 | **0,7549** |\n| dev exact / labels | 160/161 | **161/162** |\n| test exact / labels | 76/76 | **76/76** |\n\n`r035` est en dev ; le test ne bouge pas (il ne contient pas de relative zéro). Une seule phrase sur 612 change, **0 POS modifiée sur 3 179 tokens**.\n\n**Contrôles négatifs** : pas de REL devant `about the book`, `about it`, `about today`, sans pronom sujet, ni en français. Généralisation : « The book **he reads about** is good. » → REL [9:23], cible `book`. **183/183** portes, 17 tests unitaires, `porte-bloc-linguistique` et `porte-produit` vertes.\n\n**Intégration.** `tools/bloc_linguistique.py` (`relati
… [2862 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"J2.1\" tools work .github 2>/dev/null | head -20", "description": "Find J2.1 task definition"}`

  ```
tools/tokenizer_kimi/tiktoken.model:92663:J2F1dA== 92662
tools/tokenizer_kimi/tiktoken.model:128028:aXJ2 128027
tools/tokenizer_kimi/tiktoken.model:132887:IGJ2 132886
tools/tokenizer_kimi/tiktoken.model:160303:CXJ2 160302
tools/chantier/plan.json:87:   "id": "J2.1",
tools/chantier/plan.json:90:   "mandat": "Tâche J2.1 : la table de correspondance entre les **14 atomes** de Panini (∃ ∆ ∼ ↗ ⊙ ⧖ ◇ № ⊕ ⊗ λ ⊞ ≍ ≡) et nos **niveaux** (graphème, mot, pos, syntagme, phrase, pragmatique, discours, document). Lis `../Panini/README.md`, `../Panini-Research/`, `docs/theorie/genealogie-des-langues.md`. Produis `reports/rapport-atomes-niveaux.md` + JSON : 14 lignes, ce que chaque atome capte, quel niveau le porte, la mesure possible. Aucune écriture dans Panini.",
work/ocr/cegep64/controle/train.txt:115631:07 SIM 9M ‘s}ied Aueul Jo pasoduioo ale YOIyM SWI9JSAÂS J2917 9M UOIJ99S SIU} Ul
work/ocr/cegep64/controle/train_fuite.txt:115971:07 SIM 9M ‘s}ied Aueul Jo pasoduioo ale YOIyM SWI9JSAÂS J2917 9M UOIJ99S SIU} Ul
work/ocr/cegep64/train_restaure.txt:115631:07 SIM 9M ‘s}ied Aueul Jo pasoduioo ale YOIyM SWI9JSAÂS J2917 9M UOIJ99S SIU} Ul
work/ocr/cegep64/propre/train.txt:115631:07 SIM 9M ‘s}ied Aue
… [442 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,160p' tools/chantier/superviseur.py", "description": "Read supervisor head"}`

  ```
#!/usr/bin/env python3
"""superviseur.py — le méta-harnais du chantier autonome : file de tâches, exécution, vérification.

**Le problème.** DSH donne l'**agent** : des rounds, une session reprenable (`--session-id`), la
compaction du contexte, des sous-agents. Il **ne donne pas** la couche de contrôle d'un chantier de
plusieurs jours : file de tâches persistante, vérification d'acceptation **indépendante** de
l'agent, budget, reprise après crash, escalade, journal d'audit. Ce superviseur est cette couche.

**Les trois garanties.**
1. **Une tâche n'est finie que si son acceptation passe** — une commande, un attendu, exécutés par
   le superviseur, pas par l'agent.
2. **Rien n'est perdu** : l'état (`work/chantier/etat.json`) et le journal (`work/chantier/journal.log`)
   sont écrits après **chaque** étape ; une relance reprend la première tâche non finie.
3. **On s'arrête proprement** : le fichier `work/chantier/STOP` (ou le budget, ou le nombre de
   tâches) arrête la boucle ; l'agent n'est jamais tué au milieu d'un commit.

**Usage.**
    python3 tools/chantier/superviseur.py etat          # où en est-on ?
    python3 tools/chantier/superviseur.py prochaine     # la prochaine tâch
… [5489 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nfor t in d['taches']:\n    if t['id']=='J2.1': print(json.dumps(t, ensure_ascii=False, indent=1))\n\"", "description": "Read J2.1 full task spec"}`

  ```
{
 "id": "J2.1",
 "jour": 2,
 "titre": "Panini I — la table atomes ↔ niveaux",
 "mandat": "Tâche J2.1 : la table de correspondance entre les **14 atomes** de Panini (∃ ∆ ∼ ↗ ⊙ ⧖ ◇ № ⊕ ⊗ λ ⊞ ≍ ≡) et nos **niveaux** (graphème, mot, pos, syntagme, phrase, pragmatique, discours, document). Lis `../Panini/README.md`, `../Panini-Research/`, `docs/theorie/genealogie-des-langues.md`. Produis `reports/rapport-atomes-niveaux.md` + JSON : 14 lignes, ce que chaque atome capte, quel niveau le porte, la mesure possible. Aucune écriture dans Panini.",
 "budget_min": 90,
 "acceptation": [
  {
   "commande": "test -f reports/rapport-atomes-niveaux.md && echo FICHE-OK",
   "attendu": "FICHE-OK"
  },
  {
   "commande": "grep -c '∃' reports/rapport-atomes-niveaux.md",
   "attendu": ""
  }
 ]
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '160,280p' tools/chantier/superviseur.py", "description": "Read supervisor commit logic"}`

  ```
ok, details = verifier_acceptation(tache)
    # l'acceptation **prime** : un agent qui a fini son travail (fiche + portes) puis dépasse le
    # timeout a réussi ; le code 124 est noté, pas pénalisé.
    resultat = {"statut": "fait" if ok else "echec",
                "timeout": code == 124,
                "debut": _maintenant(), "duree_s": duree, "code_agent": code,
                "acceptation": details, "sortie_agent": sortie[-1500:]}
    _journal(f"{'✔' if resultat['statut'] == 'fait' else '✘'} {tache['id']} en {duree} s "
             f"(code {code}) — {'; '.join(details)}")
    return resultat


# ------------------------------------------------------------------ commandes

def cmd_etat(_: argparse.Namespace) -> int:
    plan, etat = charger_plan(), charger_etat()
    print(f"chantier : {plan.get('nom', '?')} · depuis {etat.get('depuis')}")
    print(f"session : {session_id() or '(aucune — dsh créera une session neuve)'}")
    print(f"budget consommé : {etat.get('budget_s', 0)} s · lancements : {etat.get('lancements', 0)}")
    print(f"STOP : {'présent — la boucle s’arrêtera' if STOP.exists() else 'absent'}\n")
    for t in plan["taches"]:
        s = etat["taches"].get(t["i
… [4259 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Panini\\|panini\\|atome\\|généalogie\\|J2\" docs/pilotage/roadmap.md | head -40; echo ===; sed -n '1,80p' docs/pilotage/roadmap.md", "description": "Find roadmap line for Panini integration"}`

  ```
===
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
- **Le carpe diem** : pas d'échéance. Un chantier est **[fait](../theorie/glossaire/ent
… [13854 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && python3 - <<'PY'\nimport json, statistics, math\np='nipada/falsification/analytic_sigs_v1.json'\nd=json.load(open(p))\nprint('n=',len(d))\natoms=list(next(iter(d.values())).keys())\nprint('atoms=',atoms)\n# sums\nsums=[sum(v. … [353 caractères tronqués]`

  ```
n= 44
atoms= ['ÊTRE', 'DIFFÉRENCE', 'RAPPORT', 'ORIENTATION', 'SUJET', 'TEMPS', 'MODALITÉ', 'NOMBRE', 'ESPACE', 'OPÉRATION', 'FONCTION', 'STRUCTURE', 'SYMÉTRIE', 'ÉQUATION']
sum min/max 0.9999999999999999 1.0
ÊTRE         mean=0.1074 sd=0.0326 min=0.0506 max=0.1657 cv=0.30
DIFFÉRENCE   mean=0.0232 sd=0.0106 min=0.0040 max=0.0435 cv=0.46
RAPPORT      mean=0.0882 sd=0.0347 min=0.0332 max=0.1751 cv=0.39
ORIENTATION  mean=0.0062 sd=0.0031 min=0.0009 max=0.0146 cv=0.50
SUJET        mean=0.1890 sd=0.0282 min=0.0873 max=0.2331 cv=0.15
TEMPS        mean=0.0801 sd=0.0233 min=0.0188 max=0.1273 cv=0.29
MODALITÉ     mean=0.0365 sd=0.0195 min=0.0025 max=0.0981 cv=0.53
NOMBRE       mean=0.0960 sd=0.0336 min=0.0569 max=0.2246 cv=0.35
ESPACE       mean=0.0482 sd=0.0192 min=0.0069 max=0.0903 cv=0.40
OPÉRATION    mean=0.0831 sd=0.0220 min=0.0173 max=0.1360 cv=0.27
FONCTION     mean=0.0962 sd=0.0237 min=0.0383 max=0.1400 cv=0.25
STRUCTURE    mean=0.1170 sd=0.0204 min=0.0873 max=0.1608 cv=0.17
SYMÉTRIE     mean=0.0029 sd=0.0016 min=0.0003 max=0.0090 cv=0.56
ÉQUATION     mean=0.0260 sd=0.0170 min=0.0044 max=0.1004 cv=0.66
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && python3 - <<'PY'\nimport json, statistics, math\np='nipada/falsification/analytic_sigs_v1.json'\nd=json.load(open(p))\natoms=list(next(iter(d.values())).keys())\ndef pearson(xs,ys):\n    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n\ … [610 caractères tronqués]`

  ```
top correlations |r|>=0.5
NOMBRE       ÉQUATION     r=+0.923
ÊTRE         DIFFÉRENCE   r=+0.857
ÊTRE         RAPPORT      r=-0.846
RAPPORT      ESPACE       r=-0.829
ÊTRE         ESPACE       r=+0.796
RAPPORT      MODALITÉ     r=-0.760
DIFFÉRENCE   RAPPORT      r=-0.758
RAPPORT      STRUCTURE    r=+0.732
ORIENTATION  ESPACE       r=+0.727
MODALITÉ     STRUCTURE    r=-0.723
SUJET        ÉQUATION     r=-0.714
RAPPORT      ORIENTATION  r=-0.707
MODALITÉ     OPÉRATION    r=+0.692
DIFFÉRENCE   MODALITÉ     r=+0.670
MODALITÉ     FONCTION     r=-0.664
SUJET        ESPACE       r=-0.659
FONCTION     STRUCTURE    r=+0.653
RAPPORT      FONCTION     r=+0.650
ÊTRE         FONCTION     r=-0.649
ÊTRE         STRUCTURE    r=-0.643
TEMPS        ÉQUATION     r=-0.640
DIFFÉRENCE   STRUCTURE    r=-0.637
ÊTRE         ORIENTATION  r=+0.611
SUJET        NOMBRE       r=-0.605
DIFFÉRENCE   ESPACE       r=+0.604
ÊTRE         MODALITÉ     r=+0.598
SUJET        TEMPS        r=+0.575
DIFFÉRENCE   FONCTION     r=-0.570
TEMPS        ESPACE       r=-0.559
ESPACE       FONCTION     r=-0.554
RAPPORT      OPÉRATION    r=-0.512
TEMPS        NOMBRE       r=-0.506
DIFFÉRENCE   ORIENTATION  r=+0.506
n pairs 33
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && grep -rln \"analytic_sigs_v1\" --include=*.py --include=*.md . 2>/dev/null | head -20", "description": "Find script producing analytic signatures"}`

  ```
./scripts/loi_analytique.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && python3 - <<'PY'\nimport json\nd=json.load(open('nipada/falsification/analytic_sigs_v1.json'))\nfor k in d: print(k)\nPY", "description": "List 44 works"}`

  ```
2_esdras
aristotle_categories
aristotle_de_caelo
aristotle_nicomachean_ethics
aristotle_parts_of_animals
aristotle_posterior_analytics
aristotle_prior_analytics
bengio_2003
book_of_enoch
curry_1930
daniel_book
dn1_brahmajala
ezekiel_book
hosea_book
isaiah_book
jeremiah_book
kleene_1936
lukasiewicz_1920
mengzi
mikolov_2013
miller_evidence_prophecy
mn2_sabbasava
mn35_culasaccaka
nostradamus_centuries
plato_charmides
plato_gorgias
plato_gorgias_jowett
plato_laws
plato_meno
plato_meno_jowett
plato_phaedo
plato_phaedrus_jowett
plato_philebus_jowett
plato_republic_jowett
plato_sophist
plato_symposium_jowett
plato_theaetetus_jowett
qiwulun
quillian_1968
russell_parousia_1878
schank_1972
sibylline_oracles
voluspa
zechariah_book
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && python3 - <<'PY'\nimport json, math, statistics\nd=json.load(open('nipada/falsification/analytic_sigs_v1.json'))\natoms=list(next(iter(d.values())).keys())\nrows=[[v[a] for a in atoms] for v in d.values()]\n# clr with zero re … [1285 caractères tronqués]`

  ```
CLR top |r|>=0.5, n= 44
RAPPORT      STRUCTURE    r=+0.925
SUJET        ESPACE       r=-0.886
RAPPORT      FONCTION     r=+0.877
MODALITÉ     STRUCTURE    r=-0.875
FONCTION     STRUCTURE    r=+0.862
RAPPORT      MODALITÉ     r=-0.815
SUJET        TEMPS        r=+0.809
SUJET        FONCTION     r=+0.806
RAPPORT      SUJET        r=+0.797
TEMPS        ESPACE       r=-0.795
MODALITÉ     FONCTION     r=-0.763
DIFFÉRENCE   RAPPORT      r=-0.752
RAPPORT      ESPACE       r=-0.751
ORIENTATION  ESPACE       r=+0.740
RAPPORT      ORIENTATION  r=-0.738
DIFFÉRENCE   STRUCTURE    r=-0.696
DIFFÉRENCE   FONCTION     r=-0.681
DIFFÉRENCE   SUJET        r=-0.661
TEMPS        ÉQUATION     r=-0.649
SUJET        STRUCTURE    r=+0.647
--- raw vs clr for key pairs
NOMBRE ÉQUATION raw 0.923 clr 0.577
ÊTRE DIFFÉRENCE raw 0.857 clr 0.581
ÊTRE RAPPORT raw -0.846 clr -0.42
RAPPORT ESPACE raw -0.829 clr -0.751
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && python3 - <<'PY'\ntry:\n    import numpy as np\nexcept Exception as e:\n    print('no numpy', e); raise SystemExit\nimport json, math\nd=json.load(open('nipada/falsification/analytic_sigs_v1.json'))\natoms=list(next(iter(d.va … [740 caractères tronqués]`

  ```
eigenvalues [np.float64(6.967), np.float64(2.845), np.float64(1.491), np.float64(1.26), np.float64(0.528), np.float64(0.381), np.float64(0.207), np.float64(0.14), np.float64(0.084), np.float64(0.047), np.float64(0.032), np.float64(0.013), np.float64(0.005), np.float64(-0.0)]
var explained first3 0.807
n components >1 4
var first3 [np.float64(0.498), np.float64(0.203), np.float64(0.107)] cum 0.807
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && python3 - <<'PY'\nimport numpy as np, json\nd=json.load(open('nipada/falsification/analytic_sigs_v1.json'))\natoms=list(next(iter(d.values())).keys())\nrows=np.array([[v[a] for a in atoms] for v in d.values()], dtype=float)\n … [425 caractères tronqués]`

  ```
PC 1
  ESPACE       +0.323
  DIFFÉRENCE   +0.312
  MODALITÉ     +0.296
  ORIENTATION  +0.288
  ÊTRE         +0.161
  ÉQUATION     +0.130
  SYMÉTRIE     +0.051
  OPÉRATION    -0.061
  NOMBRE       -0.176
  TEMPS        -0.280
  STRUCTURE    -0.330
  FONCTION     -0.336
  SUJET        -0.340
  RAPPORT      -0.363
PC 2
  OPÉRATION    +0.481
  TEMPS        +0.274
  MODALITÉ     +0.256
  SYMÉTRIE     +0.221
  SUJET        +0.169
  ORIENTATION  +0.082
  DIFFÉRENCE   +0.034
  FONCTION     -0.008
  ÊTRE         -0.080
  RAPPORT      -0.107
  STRUCTURE    -0.184
  ESPACE       -0.214
  ÉQUATION     -0.471
  NOMBRE       -0.472
PC 3
  ÊTRE         +0.694
  DIFFÉRENCE   +0.231
  SYMÉTRIE     +0.169
  SUJET        +0.152
  TEMPS        +0.139
  STRUCTURE    +0.072
  FONCTION     +0.067
  ESPACE       +0.063
  ORIENTATION  +0.034
  RAPPORT      -0.019
  NOMBRE       -0.129
  MODALITÉ     -0.309
  ÉQUATION     -0.356
  OPÉRATION    -0.375
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls .git/hooks | head; echo ===; sed -n '1,120p' .git/hooks/pre-commit 2>/dev/null", "description": "Inspect pre-commit hook"}`

  ```
applypatch-msg.sample
commit-msg.sample
fsmonitor-watchman.sample
post-update.sample
pre-applypatch.sample
pre-commit
pre-commit.sample
pre-merge-commit.sample
prepare-commit-msg.sample
pre-push.sample
===
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
python3 tools/archive_sessions.py --quiet >/dev/null || { echo "  ⛔ archivage des sessions en éche
… [440 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,180p' tools/verifie_etat_a_jour.py", "description": "Read state freshness checker"}`

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
… [6062 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline 92652984 | head -30; echo ===; git show 92652984 -- docs/pilotage/en-cours.md | head -60", "description": "Inspect prior task commit and state update"}`

  ```
92652984 B13 — LA CONVENTION DES GV : SUJET HORS DU GV + ADVERBE FINAL, F1 0,7549 → 0,7902, ATTACHEMENT 237/238 ; 183/183
 docs/pilotage/en-cours.md                          |   14 +-
 docs/pilotage/roadmap.md                           |    2 +-
 docs/pilotage/semaine-autonome.md                  |    2 +-
 journal/2026-11-07/README.md                       |   10 +-
 journal/2026-11-07/distribue.md                    |    2 +-
 journal/2026-11-07/docs.md                         |    6 +-
 journal/2026-11-07/memoire.md                      |    2 +-
 journal/2026-11-07/mesures.md                      |   18 +-
 journal/2026-11-07/modele.md                       |    2 +-
 journal/2026-11-07/portes.md                       |    2 +-
 journal/README.md                                  |    4 +-
 journal/sessions/MANIFEST.md                       |    6 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  286 ++
 .../rapport.md                                     |   70 +-
 .../digest.md                                      | 2764 ++++++++++++
 .../rapport.md                                     |  189 +
 .../digest.md                                      | 4497 ++++++++++++++++++
… [5801 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' reports/README.md; echo ===; grep -n \"rapport-.*\\.md\" reports/INDEX.md | tail -10", "description": "Check reports naming conventions"}`

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
… [9105 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub && git --no-optional-locks -C Panini/research log -1 --format='%h %ad %s' --date=short; stat -c '%y %s %n' Panini/research/nipada/falsification/analytic_sigs_v1.json; echo ---; git --no-optional-locks -C Panini/research status --porcelain -- ni … [103 caractères tronqués]`

  ```
e10d695e6 2026-10-25 docs(incident): la classe vue depuis les KITS — un False rapide est un kit incomplet, pas une preuve cassee ; diagnostic en une commande
2026-10-18 10:03:43.318995465 -0400 22381 Panini/research/nipada/falsification/analytic_sigs_v1.json
---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && grep -n \"14 atomes\\|V14\\|premier\" docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md | head -20", "description": "Locate key V14 passages"}`

  ```
10:Pāṇini (dhātu, IVᵉ s. BCE) → Leibniz (*Characteristica Universalis*, 1679) → Gödel (Gödel numbering, 1931) → Łukasiewicz (multi-valued logic, 1920) → Zadeh (fuzzy logic, 1965) → Wierzbicka (semantic primitives NSM, 1972) → Mel'čuk (Meaning-Text Theory / Lexical Functions, 1996) → Spencer-Brown (*Laws of Form*, 1969) → Jackendoff (conceptual semantics, 1972) → Pustejovsky (Generative Lexicon, 1995) → Fillmore (FrameNet, 1997) → Goldberg (Construction Grammar, 1995) → **NIPADA V14** (2026-04-22)
14:## 1. V14 — Atomes Sémantiques
26:**Encodage Leibniz-Gödel par nombres premiers** (§69-70) : Chaque primitive = un nombre premier. Concepts = produits de premiers. Appartenance = divisibilité (O(1)). Intersection = GCD. Union = LCM.
34:- **V14** (25 avril, §133-134) : 56 énoncés × 6 modes (texte, formule, diagramme, code, chimie, biologie). 12/14 atomes suffisants. Aucun nouveau premier nécessaire. Couverture cross-modale 100%.
44:| **Fondation** | Leibniz-Gödel (ℤ, premiers) | Zadeh ([0,1]¹⁴, flou) |
45:| **Représentation** | Entiers, produits de premiers | Vecteurs normalisés 14D |
57:Le théorème de Hurwitz (1898) : les seules algèbres de division normées sur ℝ sont ℝ (1D), ℂ (2D), ℍ 
… [1610 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && sed -n '14,50p' docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md", "description": "Read V14 atom table header"}`

  ```
## 1. V14 — Atomes Sémantiques

### 1.1 Origine : Spencer-Brown + Leibniz-Gödel

Deux intuitions convergentes le **2026-04-22** :

**Triangle irréductible de Spencer-Brown** (§69) : L'acte de tracer une distinction (le *mark*) contient simultanément trois aspects inséparables :

$$\text{ÊTRE} \longleftrightarrow \text{DIFFÉRENCE} \longleftrightarrow \text{RAPPORT}$$

Chacun présuppose les deux autres. C'est l'*Ur-primitive* — on ne peut réduire davantage sans perdre la capacité de décrire quoi que ce soit. L'Ur-primitive = 1 (le *mark* de Spencer-Brown lui-même — condition de possibilité de tous les produits, n'entre jamais dans les produits).

**Encodage Leibniz-Gödel par nombres premiers** (§69-70) : Chaque primitive = un nombre premier. Concepts = produits de premiers. Appartenance = divisibilité (O(1)). Intersection = GCD. Union = LCM.

$$\text{ÊTRE}=2, \text{DIFFÉRENCE}=3, \text{RAPPORT}=5, \text{ORIENTATION}=7, \text{SUJET}=11, \text{TEMPS}=13, \text{MODALITÉ}=17, \text{NOMBRE}=19, \text{ESPACE}=23, \text{OPÉRATION}=29, \text{FONCTION}=31, \text{STRUCTURE}=37, \text{SYMÉTRIE}=41, \text{ÉQUATION}=43$$

### 1.2 Évolution 6→14 (2026-04-22 → 2026-04-25)

- **V6** (22 avril) : 6 a
… [1384 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && find . -iname '*meno*' -o -iname '*aristotle*categor*' -o -iname '*plato*' 2>/dev/null | head -30", "description": "Search for source texts of 44 works"}`

  ```
./nipada/corpus/_cache/sources/plato_parmenides.txt
./nipada/corpus/_cache/sources/plato_charmides.txt
./nipada/corpus/_cache/sources/plato_crito.txt
./nipada/corpus/_cache/sources/plato_crito_jowett.txt
./nipada/corpus/_cache/sources/plato_gorgias.txt
./nipada/corpus/_cache/sources/plato_gorgias_jowett.txt
./nipada/corpus/_cache/sources/plato_meno.txt
./nipada/corpus/_cache/sources/plato_meno_jowett.txt
./nipada/corpus/_cache/sources/plato_phaedo.txt
./nipada/corpus/_cache/sources/plato_phaedrus_jowett.txt
./nipada/corpus/_cache/sources/plato_philebus_jowett.txt
./nipada/corpus/_cache/sources/plato_sophist.txt
./nipada/corpus/_cache/sources/plato_symposium_jowett.txt
./nipada/corpus/_cache/sources/aristotle_categories.txt
./nipada/corpus/_cache/sources/plato_laws.txt
./nipada/corpus/_cache/sources/plato_republic_jowett.txt
./nipada/corpus/_cache/sources/plato_euthyphro_jowett.txt
./nipada/corpus/_cache/sources/plato_theaetetus_jowett.txt
./nipada/corpus/_cache/wikipedia_dump/wiki_de_amenophis.txt
./nipada/corpus/_cache/wikipedia_dump/wiki_de_amenophis_sohn_des_hapu.txt
./nipada/corpus/_cache/wikipedia_dump/wiki_de_apologie_platon.txt
./nipada/corpus/_cache/wikipedia_dump/wiki_de_g
… [542 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && grep -n \"def \\|TEXTS\\|sources\\|data/\" scripts/loi_analytique.py | head -50", "description": "Inspect analytic signatures script sources"}`

  ```
16:SRC = ROOT / "nipada" / "corpus" / "_cache" / "sources"
24:def sign_one(nid):
36:def main():
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && sed -n '1,120p' scripts/loi_analytique.py", "description": "Read signature computation script"}`

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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"class Heuristique\\|def analyser\\|class Annotation\\|class Etiquette\\|NIVEAUX\\|def __init__\" tools/bloc_linguistique.py | head -40; echo ===; sed -n '1,80p' tools/bloc_linguistique.py", "description": "Inspect bloc ling … [14 caractères tronqués]`

  ```
50:NIVEAUX = ("graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
68:class Etiquette:
98:class Annotation:
141:    def analyser(self, texte: str, langue: str | None = None,
796:class Heuristique:
801:    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
1433:    def analyser(self, texte: str, langue: str | None = None,
1817:    def __init__(self, profils: dict[str, dict] | None = None):
1820:    def analyser(self, texte: str, langue: str | None = None,
1873:    def __init__(self, modele: str | pathlib.Path, llama_cli: str = "llama-cli",
1891:    def analyser(self, texte: str, langue: str | None = None,
1918:            if e.get("niveau") not in NIVEAUX:
1962:    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18081",
2001:    def analyser(self, texte: str, langue: str | None = None,
2091:    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18082",
2135:    def analyser(self, texte: str, langue: str | None = None,
2221:    def __init__(self, pos: BlocLinguistique, chunks: BlocLinguistique,
2227:    def analyser(self, texte: str, langue: str | None = None,
2271:    
… [3604 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '796,860p' tools/bloc_linguistique.py; echo ===; sed -n '1433,1500p' tools/bloc_linguistique.py", "description": "Read Heuristique init and analyser"}`

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
… [6018 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/bloc_linguistique.py --texte \"Le chat de la voisine qui dort sur le toit se réveille. Il n'est pas content. Il peut dormir pour récupérer. Trois chats dorment.\" --json 2>/dev/null | head -120", "description": "Sample  … [22 caractères tronqués]`

  ```
{
 "schema": "drave.annotation",
 "version": 2,
 "texte": "Le chat de la voisine qui dort sur le toit se réveille. Il n'est pas content. Il peut dormir pour récupérer. Trois chats dorment.",
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
    "« pour récupérer » → voisine",
    "« pour récupérer » → Le
… [1041 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'tools')\nfrom bloc_linguistique import Heuristique\nh=Heuristique()\na=h.analyser(\"Le chat de la voisine qui dort sur le toit se réveille. Il n'est pas content. Il peut dormir p … [391 caractères tronqués]`

  ```
fr Latn 
Counter({('graphème', 'espace', ' '): 23, ('phrase', 'type', 'déclarative'): 4, ('pragmatique', 'acte', 'assertion'): 4, ('graphème', 'ponctuation', '.'): 4, ('mot', 'ponctuation', '.'): 4, ('pos', 'PONCT', '.'): 4, ('morphème', 'préfixe', 'ré'): 2, ('graphème', 'lettres', 'Il'): 2, ('mot', 'mot', 'Il'): 2, ('pos', 'PRON', 'Il'): 2, ('syntagme', 'GN', 'Il'): 2, ('graphème', 'lettres', 'Le'): 1, ('mot', 'mot', 'Le'): 1, ('pos', 'DET', 'Le'): 1, ('syntagme', 'GN', 'Le chat'): 1, ('discours', 'paragraphe', 'suite'): 1, ('document', 'paragraphe', 'Le chat de la voisine qui dort sur le toit se réveille. Il n'): 1, ('graphème', 'lettres', 'chat'): 1, ('mot', 'mot', 'chat'): 1, ('pos', 'NOUN', 'chat'): 1, ('graphème', 'lettres', 'de'): 1, ('mot', 'mot', 'de'): 1, ('pos', 'PREP', 'de'): 1, ('syntagme', 'GP', 'de la voisine'): 1, ('graphème', 'lettres', 'la'): 1, ('mot', 'mot', 'la'): 1, ('pos', 'DET', 'la'): 1, ('graphème', 'lettres', 'voisine'): 1, ('mot', 'mot', 'voisine'): 1, ('pos', 'NOUN', 'voisine'): 1, ('graphème', 'lettres', 'qui'): 1, ('mot', 'mot', 'qui'): 1, ('pos', 'PRON', 'qui'): 1, ('syntagme', 'REL', 'qui dort sur le toit'): 1, ('syntagme', 'REL', 'qui dort sur le t
… [2638 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, time, json\nsys.path.insert(0,'tools')\nfrom bloc_linguistique import Heuristique\nfrom pathlib import Path\nsrc=Path('../Panini/research/nipada/corpus/_cache/sources')\nfor nid in ['plato_meno_jowett',' … [503 caractères tronqués]`

  ```
plato_meno_jowett 51985 und Latn 3.37 {'graphème': 22076, 'mot': 12031, 'pos': 12031, 'phrase': 1391, 'pragmatique': 1053, 'discours': 305, 'document': 1, 'morphème': 1265, 'syntagme': 2304}
aristotle_categories 57165 und Latn 3.27 {'graphème': 21736, 'mot': 11825, 'pos': 11825, 'discours': 348, 'phrase': 661, 'pragmatique': 413, 'document': 1, 'morphème': 2052, 'syntagme': 2168}
bengio_2003 63198 und Jpan 1.31 {'graphème': 42965, 'mot': 35688, 'pos': 35688, 'phrase': 432, 'pragmatique': 433, 'discours': 1, 'document': 1, 'morphème': 219, 'syntagme': 785}
mikolov_2013 3783 en Latn 0.07 {'morphème': 122, 'graphème': 1363, 'mot': 751, 'pos': 751, 'discours': 14, 'phrase': 35, 'pragmatique': 36, 'document': 1, 'syntagme': 149}
2_esdras 102937 und Latn 1.43 {'mot': 25869, 'pos': 25869, 'graphème': 37751, 'phrase': 404, 'pragmatique': 380, 'discours': 28, 'document': 1, 'morphème': 1476, 'syntagme': 1046}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Panini/research && python3 - <<'PY'\nimport json\nfrom pathlib import Path\nd=json.load(open('nipada/falsification/analytic_sigs_v1.json'))\nsrc=Path('nipada/corpus/_cache/sources')\nmissing=[k for k in d if not (src/f'{k}.txt').exists()]\nprin … [182 caractères tronqués]`

  ```
n 44 missing []
2_esdras 103170
aristotle_categories 100963
aristotle_de_caelo 75423
aristotle_nicomachean_ethics 656863
aristotle_parts_of_animals 43456
aristotle_posterior_analytics 6802
aristotle_prior_analytics 5110
bengio_2003 66060
book_of_enoch 5246
curry_1930 130182
daniel_book 1698
dn1_brahmajala 78743
ezekiel_book 4811
hosea_book 1210
isaiah_book 4989
jeremiah_book 5185
kleene_1936 6817
lukasiewicz_1920 3269
mengzi 1666
mikolov_2013 3784
miller_evidence_prophecy 213248
mn2_sabbasava 12283
mn35_culasaccaka 7595
nostradamus_centuries 64628
plato_charmides 56360
plato_gorgias 65707
plato_gorgias_jowett 65707
plato_laws 1338923
plato_meno 66718
plato_meno_jowett 66718
plato_phaedo 70996
plato_phaedrus_jowett 123765
plato_philebus_jowett 63754
plato_republic_jowett 1419392
plato_sophist 62810
plato_symposium_jowett 102134
plato_theaetetus_jowett 388414
qiwulun 4487
quillian_1968 71910
russell_parousia_1878 498777
schank_1972 80481
sibylline_oracles 7064
voluspa 46501
zechariah_book 1320
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-atomes-niveaux.md", "content": "# Table de correspondance — 14 atomes de Panini et 8 niveaux de Drave\n\n> **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J2.1 · **Date** : 2026-11-07\n> **Ve … [21675 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-atomes-niveaux.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"porte r\\|se renforcent\\|80,7\\|33 paires\\|4 composantes\" reports/rapport-atomes-niveaux.md", "description": "Locate typos and claims"}`

  ```
7:> 44 œuvres de Panini montre **33 paires d'atomes à |r| ≥ 0,5** (brut), **4 composantes > 1** et **80,7 %** de
34:| **direct** | un seul niveau suffit à porte r l'atome | № → mot ; ⊗ → pos |
183:Sur les 44 œuvres, **33 paires** d'atomes ont |r| ≥ 0,5 en brut. Les plus fortes :
196:№ ↔ ≡ passe de **+0,923** à **+0,577**, et ∃ ↔ ∼ de **−0,846** à **−0,420**. Certaines paires se renforcent
200:Une ACP sur les parts CLR donne **4 composantes de valeur propre > 1** ; les trois premières expliquent
201:**80,7 %** de la variance (6,967 · 2,845 · 1,491 · 1,260 · …). Autrement dit, dans ce corpus, les 14 atomes
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l reports/rapport-atomes-niveaux.md; sed -n '1,80p' reports/rapport-atomes-niveaux.md", "description": "Read report head"}`

  ```
314 reports/rapport-atomes-niveaux.md
# Table de correspondance — 14 atomes de Panini et 8 niveaux de Drave

> **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J2.1 · **Date** : 2026-11-07
> **Verdict** : ✅ **la table est complète** — 14 atomes, 8 niveaux, 14 lignes, un ancrage et un porteur par
> atome, une mesure possible et son contrôle négatif. ⚠️ **aucune correspondance atome ↔ niveau n'est mesurée à
> ce stade** : c'est une **hypothèse de lecture** et un **protocole**, pas une corrélation. La calibration des
> 44 œuvres de Panini montre **33 paires d'atomes à |r| ≥ 0,5** (brut), **4 composantes > 1** et **80,7 %** de
> la variance sur les trois premières (ACP sur CLR) : la colinéarité est le premier confondant, avant même
> l'époque.
> **Dispositif** : lecture seule de `../../Panini/research` (HEAD `e10d695`, 2026-10-25) ; signatures
> `../../Panini/research/nipada/falsification/analytic_sigs_v1.json` (44 œuvres, 2026-10-18) ; contrat des
> niveaux `../docs/theorie/contrat-bloc-langue.md` ; JSON [`atomes-niveaux.json`](atomes-niveaux.json).
> **Aucune écriture dans Panini** : les seuls fichiers produits sont cette fiche et son JSON.

## 1. La ques
… [3893 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '180,205p' reports/rapport-atomes-niveaux.md", "description": "Read calibration conclusion"}`

  ```
### 5.2 Les atomes ne sont pas indépendants

Sur les 44 œuvres, **33 paires** d'atomes ont |r| ≥ 0,5 en brut. Les plus fortes :

| paire | r brut | r CLR |
|---|---:|---:|
| № NOMBRE ↔ ≡ ÉQUATION | **+0,923** | +0,577 |
| ∃ ÊTRE ↔ ∆ DIFFÉRENCE | **+0,857** | +0,581 |
| ∃ ÊTRE ↔ ∼ RAPPORT | **−0,846** | −0,420 |
| ∼ RAPPORT ↔ ⊕ ESPACE | **−0,829** | −0,751 |
| ∃ ÊTRE ↔ ⊕ ESPACE | +0,796 | — |
| ∼ RAPPORT ↔ ◇ MODALITÉ | −0,760 | — |

Les parts sont des **données compositionnelles** (somme 1) : une corrélation brute est mécaniquement contrainte.
Le passage au **CLR** (log-ratio centré, remplacement des zéros par 1e−6) change la structure : par exemple
№ ↔ ≡ passe de **+0,923** à **+0,577**, et ∃ ↔ ∼ de **−0,846** à **−0,420**. Certaines paires se renforcent
(∼ ↔ ⊕ : −0,829 → **−0,751**), d'autres apparaissent (∼ ↔ ⊞ : **+0,925** en CLR). **Conclusion : toute
corrélation atome ↔ niveau doit être calculée sur les parts transformées, pas sur les parts brutes.**

Une ACP sur les parts CLR donne **4 composantes de valeur propre > 1** ; les trois premières expliquent
**80,7 %** de la variance (6,967 · 2,845 · 1,491 · 1,260 · …). Autrement dit, dans ce corpus, les 14 atomes
n'occupent que **
… [265 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-atomes-niveaux.md", "old_string": "| **direct** | un seul niveau suffit à porte r l'atome | № → mot ; ⊗ → pos |", "new_string": "| **direct** | un seul niveau suffit à porter l'atome | № → mot ; ⊗ → pos |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-atomes-niveaux.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-atomes-niveaux.md", "old_string": "№ ↔ ≡ passe de **+0,923** à **+0,577**, et ∃ ↔ ∼ de **−0,846** à **−0,420**. Certaines paires se renforcent\n(∼ ↔ ⊕ : −0,829 → **−0,751**), d'autres apparaissent (∼ ↔ ⊞ : **+0,925** en C … [250 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-atomes-niveaux.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, math, statistics\nfrom pathlib import Path\nimport numpy as np\n\nSRC = Path('../Panini/research/nipada/falsification/analytic_sigs_v1.json')\nd = json.loads(SRC.read_text(encoding='utf-8'))\natoms_sig  … [2918 caractères tronqués]`

  ```
{
 "stats": {
  "ÊTRE": {
   "moyenne": 0.107443,
   "ecart_type": 0.032566,
   "min": 0.050592,
   "max": 0.165658,
   "cv": 0.3031
  },
  "DIFFÉRENCE": {
   "moyenne": 0.023207,
   "ecart_type": 0.010585,
   "min": 0.004031,
   "max": 0.043502,
   "cv": 0.4561
  },
  "RAPPORT": {
   "moyenne": 0.088174,
   "ecart_type": 0.034694,
   "min": 0.033223,
   "max": 0.175124,
   "cv": 0.3935
  },
  "ORIENTATION": {
   "moyenne": 0.006197,
   "ecart_type": 0.00308,
   "min": 0.000913,
   "max": 0.014632,
   "cv": 0.4971
  },
  "SUJET": {
   "moyenne": 0.189031,
   "ecart_type": 0.028152,
   "min": 0.087297,
   "max": 0.233076,
   "cv": 0.1489
  },
  "TEMPS": {
   "moyenne": 0.080068,
   "ecart_type": 0.023334,
   "min": 0.018835,
   "max": 0.127257,
   "cv": 0.2914
  },
  "MODALITÉ": {
   "moyenne": 0.03647,
   "ecart_type": 0.019462,
   "min": 0.002513,
   "max": 0.098077,
   "cv": 0.5336
  },
  "NOMBRE": {
   "moyenne": 0.095984,
   "ecart_type": 0.033624,
   "min": 0.056852,
   "max": 0.224591,
   "cv": 0.3503
  },
  "ESPACE": {
   "moyenne": 0.048242,
   "ecart_type": 0.019247,
   "min": 0.0069,
   "max": 0.090297,
   "cv": 0.399
  },
  "OPÉRATION": {
   "moyenne": 0.083131,
   "ecar
… [2500 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, math, statistics\nfrom pathlib import Path\nimport numpy as np\n\nSRC = Path('../Panini/research/nipada/falsification/analytic_sigs_v1.json')\nd = json.loads(SRC.read_text(encoding='utf-8'))\natoms_sig  … [22040 caractères tronqués]`

  ```
written reports/atomes-niveaux.json 22066
atoms 14
levels 8
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/atomes-niveaux.json'))\nprint('keys:', list(d))\nprint('n atoms', len(d['atomes']), 'n levels', len(d['niveaux']))\nfor a in d['atomes']:\n    print(a['rang'], a['symbole'], a[ … [476 caractères tronqués]`

  ```
keys: ['fiche', 'version', 'date', 'titre', 'statut', 'sources', 'niveaux', 'niveaux_du_contrat', 'principe', 'atomes', 'calibration_44_oeuvres', 'protocole', 'limites', 'prochaine_etape', 'fichiers']
n atoms 14 n levels 8
1 ∃ ÊTRE 2 mot -> phrase distribué
2 ∆ DIFFÉRENCE 3 graphème -> phrase distribué
3 ∼ RAPPORT 5 pos -> syntagme distribué
4 ↗ ORIENTATION 7 syntagme -> discours distribué
5 ⊙ SUJET 11 pos -> syntagme distribué
6 ⧖ TEMPS 13 pos -> phrase distribué
7 ◇ MODALITÉ 17 pos -> pragmatique distribué
8 № NOMBRE 19 mot -> mot direct
9 ⊕ ESPACE 23 pos -> syntagme distribué
10 ⊗ OPÉRATION 29 mot -> pos direct
11 λ FONCTION 31 pos -> syntagme distribué
12 ⊞ STRUCTURE 37 syntagme -> document émergent
13 ≍ SYMÉTRIE 41 graphème -> discours émergent
14 ≡ ÉQUATION 43 syntagme -> phrase émergent
sum means 1.0
raw n 33
clr n 44
acp {'valeurs_propres': [6.9668, 2.8449, 1.4911, 1.2596, 0.5285, 0.3807], 'composantes_sup_1': 4, 'variance_3_premiers': 0.8073, 'variance_brute_3_premiers': [0.4976, 0.2032, 0.1065]}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -60 reports/atomes-niveaux.json", "description": "Inspect JSON head"}`

  ```
{
 "fiche": "reports/rapport-atomes-niveaux.md",
 "version": "1.0",
 "date": "2026-11-07",
 "titre": "Table de correspondance — 14 atomes V14 de Panini et 8 niveaux Drave",
 "statut": "hypothese_de_lecture_et_protocole_non_mesure",
 "sources": {
  "atomes": {
   "depot": "../../Panini/research",
   "head": "e10d695",
   "head_date": "2026-10-25",
   "fichiers": [
    "../../Panini/README.md",
    "../../Panini/research/docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md",
    "../../Panini/research/philosophy-theory/GRILLE_ABLATION_V14_v0.1.md",
    "../../Panini/research/nipada/falsification/analytic_sigs_v1.json"
   ],
   "note": "V14 de Research uniquement ; les 34 atomes de Panini-FS et les 9 dhatus de l'ancien docs/ de l'hote ne sont pas utilises."
  },
  "niveaux": {
   "fichiers": [
    "../docs/theorie/contrat-bloc-langue.md",
    "../docs/theorie/pre-traitement-linguistique.md",
    "rapport-bloc-linguistique.md"
   ],
   "note": "Le contrat compte 9 niveaux avec morphème ; le mandat J2.1 en liste 8. Le morphème reste un ancrage possible pour ∆ et λ, pas un porteur."
  }
 },
 "niveaux": [
  "graphème",
  "mot",
  "pos",
  "syntagme",
  "phrase",
  "pragmatique",
  "discours",
  
… [537 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -80", "description": "Run documentation review"}`

  ```
revue de documentation · 710 fiche(s) · 803 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 709 fichiers, le disque en a 710
     · compteurs : en-cours.md dit 802 JSON, le disque en a 803
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh 2>&1 | tail -40", "description": "Run table gate"}`

  ```
✅ 1766 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3813 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-07)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"709\\|802\\|Panini\\|J2\" docs/pilotage/en-cours.md | head -40; echo ===; tail -60 docs/pilotage/en-cours.md", "description": "Locate counters and Panini section in state"}`

  ```
26:### Session `536cd5d6-94ac-4057-8fe9-11709a4587c7` — le hub, l'intégration et la reprise *(en pause)*
28:- **Id** : `536cd5d6-94ac-4057-8fe9-11709a4587c7` — [`plan.md`](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/plan.md).
38:- **Journal** : [la session](../../journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/).
101:| fichiers / JSON de résultats | **709** / **802** | `reports/*.md` / `reports/*.json` |
===
- **Ce que font les autres** : **hub**, **S**, **Pensée**.
- **Prochaine action** : la **porte propre (0,29)** ; le **2 048** est fini.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).

## Ce qui est en cours

- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67, 8 verdicts de référents ; page **`/paragraphes`**.
- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** (2×10 000 pas ; drvm `c50beff6` + `91a3028…`) ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
- **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`porte-n3-i
… [4563 caractères tronqués]
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M %Z'", "description": "Get current date and time"}`

  ```
2026-11-07 14:55 EST
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-07, 14 h 40 HNE (heure locale, EST).**", "new_string": "**Mis à jour : 2026-11-07, 14 h 55 HNE (heure locale, EST).**"}`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **709** / **802** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **710** / **803** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.", "new_string": "- **L — le bloc langue** : contrat ;  … [466 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-07, 14 h 40 HNE (heure locale, EST).**
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
… [8992 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-07, 14 h 40 HNE (heure locale, EST).**", "new_string": "**Mis à jour : 2026-11-07, 14 h 55 HNE (heure locale, EST).**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **709** / **802** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **710** / **803** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.", "new_string": "- **L — le bloc langue** : contrat ;  … [466 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -40", "description": "Re-run documentation review"}`

  ```
revue de documentation · 710 fiche(s) · 803 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -30; echo ===; python3 tools/taille_documents.py 2>&1 | tail -30", "description": "Check state and document budgets"}`

  ```
en-cours · 1686 mots · 7 sections · 4 session(s) · 6 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
===
  budget de contexte · documents chargeables
    mots lignes  cat budget  document
    7123    383   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2783    190   T1   2800  reports/README.md
    2434    162   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942   
… [653 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Panini J2.1 — la table atomes ↔ niveaux** : **14 atomes × 8 niveaux**, un ancrage et un porteur par atome, une mesure possible et son contrôle négatif ; calibration des **44 œuvres** (33 pai … [306 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -8", "description": "Recheck document budget"}`

  ```
1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4013 mots (budget 4 000)

  avertissements :
     · 39 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4013 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Panini J2.1** : table **14 atomes × 8 niveaux** ; [fiche](../../reports/rapport-atomes-niveaux.md) ; suite **J2.2**.", "new_string": "- **Panini J2.1** : table **14 atomes × 8 niveaux** ; [f … [49 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| dernière passe | **03/11 11 h 30** (82, **80/2**, les 2 connues) ; **04/11 08 h 40 arrêtée** ; N3 **17/17** à 11 h 32 ; complète après les runs | `docs/pilotage/references-non-regression.md` | … [145 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -6; echo ===; python3 tools/revue_documentation.py 2>&1 | tail -10", "description": "Recheck budget and review"}`

  ```
T0 max : 3996 mots (budget 4 000)

  avertissements :
     · 39 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
===
  revue de documentation · 710 fiche(s) · 803 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\nimport json, re\ntxt=Path('reports/rapport-atomes-niveaux.md').read_text(encoding='utf-8')\nsyms=['∃','∆','∼','↗','⊙','⧖','◇','№','⊕','⊗','λ','⊞','≍','≡']\nprint('symbols present:', all(s i … [736 caractères tronqués]`

  ```
symbols present: True []
table rows ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
json atoms 14 symbols ['∃', '∆', '∼', '↗', '⊙', '⧖', '◇', '№', '⊕', '⊗', 'λ', '⊞', '≍', '≡']
levels ['graphème', 'mot', 'pos', 'syntagme', 'phrase', 'pragmatique', 'discours', 'document']
all fields ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -30", "description": "Check working tree status"}`

  ```
M docs/pilotage/en-cours.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/superviseur.py
 m tools/structures
?? reports/atomes-niveaux.json
?? reports/rapport-atomes-niveaux.md
?? reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add reports/rapport-atomes-niveaux.md reports/atomes-niveaux.json docs/pilotage/en-cours.md && python3 tools/verifie_etat_a_jour.py --index; echo \"state-check=$?\"; git diff --cached --stat", "description": "Stage deliverables a … [22 caractères tronqués]`

  ```
✅ index : aucun fait stagé sans état
state-check=0
 docs/pilotage/en-cours.md         |   7 +-
 reports/atomes-niveaux.json       | 740 ++++++++++++++++++++++++++++++++++++++
 reports/rapport-atomes-niveaux.md | 314 ++++++++++++++++
 3 files changed, 1058 insertions(+), 3 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -m \"PANINI J2.1 — TABLE 14 ATOMES × 8 NIVEAUX : 14/14 LIGNES, 33 PAIRES COLINÉAIRES, AUCUNE MESURE ENCORE\" -m \"Table de correspondance V14 (Research) × 8 niveaux Drave : pour chaque atome, ce qu'il capte, son ancrage, s … [615 caractères tronqués]`
