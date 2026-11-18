# Session DSH — relecture

- identifiant : `6e7ba93b-7eb8-400a-8457-6f6a8fe67f54`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-18 11:47:54
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (Drave, en français). Machine dédiée. `data/` est en LECTURE SEULE.

CONTEXTE : `reports/rapport-dedup-blocs.md` vient d'établir que le dédoublonnage par blocs n'écarte rien (0 %) sur `data/corpus_wiki_fr_texte/train.txt` (7,50 Go) parce que la duplication est courte et diffuse : la mesure exacte donne **53,98 % des lignes répétées = 8,28 % des octets** (621 Mo, dont 23 Mo de lignes vides à préserver). La prochaine action recommandée est un dédoublonnage **par ligne, en flux**.

TÂCHE : écrire `tools/dedup_lignes.py` (dédup par ligne, en flux, à mémoire bornée) et le mesurer sur les 7,50 Go.

Exigences :
1. CLI : `python3 tools/dedup_lignes.py --entree F --sortie G [--memoire-mo 2048] [--normaliser] [--json R] [--autotest]`. Lecture en flux (pas de fichier entier en RAM), hachage 64 bits par ligne normalisée (au moins : espaces de fin retirés ; `--normaliser` ajoute minuscules + espaces compactés), on garde la première occurrence, on **préserve toutes les lignes vides** (séparateurs de paragraphes), on écrit la sortie telle quelle.
2. **Budget mémoire explicite** : `--memoire-mo` est un plafond (par exemple un filtre de Bloom à taille fixe, ou une table de hachages avec éviction) ; mesure `ru_maxrss` et prouve-le sur 200 Mo au moins ; budget impossible → erreur nommée (rc 3).
3. **Autotest obligatoire** (`--autotest`) : (a) ligne unique gardée, (b) copie exacte écartée, (c) copie avec espaces de fin différents écartée par défaut, (d) ligne différente gardée, (e) lignes vides préservées (compte), (f) deux passes → même sha256 (stabilité).
4. **Mesure** : passe sur `data/corpus_wiki_fr_texte/train.txt` (7,50 Go, lecture seule) → `work/dedup/train-lignes.txt` + `--json reports/dedup-lignes-7.5go.json` ; mesure temps, RSS max, lignes gardées/écartées, octets gardés/écartés, sha256 de la sortie.
5. Écris `reports/rapport-dedup-lignes.md` : dispositif, chiffres, contrôles, comparaison aux 53,98 %/8,28 % du rapport blocs, ce qui pourrait le rendre faux (collisions 64 bits, lignes quasi identiques non détectées, normalisation, ordre), et la suite (le corpus v2 : `work/dedup/train-lignes.txt`, sa taille, son épingle — sans toucher à `data/`).

CONTRAINTES : n'écris que `tools/dedup_lignes.py`, `reports/rapport-dedup-lignes.md`, `reports/dedup-lignes-7.5go.json`, `work/dedup/` ; ne touche pas à en-cours/roadmap/AGENTS ; ne committe pas ; pas d'appel API ; lecture seule sur `data/`.

Rends : les chiffres (temps, RSS, % lignes/octets écartés, taille de sortie), les 6 cas d'autotest, les chemins.
Your parent agent id is "d67a9bb1-090e-4f69-baf2-a831c00aa275". Before you finish, send your result to that agent with send_message({ agent_id: "d67a9bb1-090e-4f69-baf2-a831c00aa275", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

12. **La tarification de l'API a deux fenêtres** : **remisé** pendant **UTC 16:30 → 00:30**
    (la Chine 00:30 → 08:30), soit au Canada **11:30 → 19:30** ; **plein tarif** le reste.
    **L'API en remisée** (le tagger, la distillation), **le local en pleine** (l'entraînement, les
    tests, les docs) ; **deux files** par chantier. → [`plans-tarif.md`](docs/pilotage/plans-tarif.md)

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

⏵ Reading the existing dedup context and repo conventions

- **bash** `{"command": "pwd && ls -la && echo '---' && ls -la tools/ | head -60 && echo '---' && ls -la reports/ | head -40 && echo '---' && ls -la work/ 2>/dev/null | head -20", "description": "List workspace, tools, reports, work"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
total 212
drwxr-xr-x. 1 stephane stephane   774 16 nov 03:32 .
drwxr-xr-x. 1 stephane stephane  2574 16 nov 10:32 ..
-rw-r--r--. 1 stephane stephane 10375 18 nov 08:31 AGENTS.md
drwxr-xr-x. 1 stephane stephane   198 18 nov 10:07 bench
drwxr-xr-x. 1 stephane stephane    42 16 nov 02:01 build
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane    56 16 nov 00:38 dist
drwxr-xr-x. 1 stephane stephane   138 16 nov 04:02 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   136 16 nov 04:07 drave.egg-info
drwxr-xr-x. 1 stephane stephane   220 18 nov 11:47 .git
drwxr-xr-x. 1 stephane stephane    22 16 nov 03:51 .github
-rw-r--r--. 1 stephane stephane   653 15 nov 22:25 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane  1052 18 nov 08:36 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-------. 1 stephane stephane  1272 16 nov 01:44 pyproject.toml
drwxr-xr-x. 1 stephan
… [9621 caractères tronqués]
  ```

- **bash** `{"command": "ls -la data/ 2>/dev/null | head -20; echo '---'; ls -la data/corpus_wiki_fr_texte/ 2>/dev/null; echo '---'; df -h . data 2>/dev/null; echo '---'; nproc; free -m", "description": "Inspect data dir and machine resources"}`

  ```
total 961812
drwxr-xr-x. 1 stephane stephane      2664  2 nov 18:33 .
drwxr-xr-x. 1 stephane stephane       774 16 nov 03:32 ..
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
-rw-r--r--. 1 stephane stephane   2032162  8 oct 09:42 corpus_en_val.txt
-rw-r--r--. 1 stephane stephane  17031747 17 oct 18:26 corpus_fr_litterature.txt
-rw-r--r--. 1 stephane stephane   4402195 28 oct 12:45
… [984 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/ | grep -i dedup; echo '---'; ls -la work/dedup/; echo '---'; ls -la reports/ | grep -i dedup", "description": "Find dedup-related files"}`

  ```
-rw-------. 1 stephane stephane  38680 18 nov 11:18 dedup_blocs.py
---
total 7718892
drwxr-xr-x. 1 stephane stephane        556 18 nov 11:14 .
drwxr-xr-x. 1 stephane stephane       2868 18 nov 10:34 ..
drwxr-xr-x. 1 stephane stephane        568 18 nov 10:46 controle
-rw-r--r--. 1 stephane stephane        513 18 nov 11:00 diagnostic-ancrage.log
-rw-------. 1 stephane stephane       4574 18 nov 10:50 diagnostic_ancrage.py
-rw-r--r--. 1 stephane stephane       1330 18 nov 11:11 diagnostic-lignes-exact.log
-rw-------. 1 stephane stephane       3618 18 nov 11:08 diagnostic_lignes_exact.py
-rw-r--r--. 1 stephane stephane       1554 18 nov 11:04 diagnostic-lignes.log
-rw-------. 1 stephane stephane       3803 18 nov 11:01 diagnostic_lignes.py
drwxr-xr-x. 1 stephane stephane        106 18 nov 11:14 granularite
-rw-r--r--. 1 stephane stephane       7513 18 nov 11:11 prouve-200Mo.json
-rw-r--r--. 1 stephane stephane       2237 18 nov 11:11 prouve-200Mo.log
-rw-r--r--. 1 stephane stephane       1032 18 nov 11:11 prouve-200Mo.out
-rw-r--r--. 1 stephane stephane  200000000 18 nov 11:11 slice-200Mo-garde.txt
-rw-r--r--. 1 stephane stephane  200000000 18 nov 10:46 slice-200Mo.txt
-rw-r--r--. 1 st
… [347 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-blocs.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-blocs.md</path>
<type>file</type>
<content>
1: # N — dédoublonner 7,50 Go par blocs : 954 Mio de RSS, 0 bloc écarté, 5,2 % de shingles déjà vus
2: 
3: > **Ligne de roadmap** : N (le palier 1, « la donnée d'abord ») · **Date** : 2026-11-18 ·
4: > **Verdict** : [`tools/dedup_blocs.py`](../tools/dedup_blocs.py) passe les **7 504 078 589
5: > octets** de `data/corpus_wiki_fr_texte/train.txt` en **7 min 11 s**, avec **954,3 Mio de RSS
6: > max** pour un budget de **2 048 Mio** (marge 1 094 Mio), et écrit **7 504 078 589 octets** :
7: > **112 blocs sur 112 gardés, aucun écarté**. La duplication n'est pourtant pas nulle —
8: > **4,18 %** des shingles échantillonnés étaient déjà vus avant leur bloc, **5,17 %** en
9: > comptant les répétitions internes au bloc — mais elle est **courte et diffuse** : 54,0 % des
10: > lignes sont des répétitions exactes, pour **8,28 % des octets**, surtout des lignes vides et
11: > du boilerplate. Aucun bloc de 64 Mio n'atteint le seuil de 80 % (le plus chargé est à
12: > **48,9 %**). Le dédoublonnage **par blocs ne ferme donc pas l'écart du palier 1** : il le
13: > **chiffre**, et mo
… [21421 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading `dedup_blocs.py` conventions (CLI, errors, JSON)

- **bash** `{"command": "sed -n '1,220p' tools/dedup_blocs.py", "description": "Read dedup_blocs.py header and CLI"}`

  ```
#!/usr/bin/env python3
"""dedup_blocs.py — dédoublonner du texte par blocs, à mémoire bornée.

POURQUOI. `tools/corpus_propre.py` garde **tous** les shingles en mémoire (≈ 80 Go par Go
de texte, cf. `reports/rapport-n2-corpus-1go.md`) : dédupliquer les 7,50 Go de
`data/corpus_wiki_fr_texte/train.txt` demanderait ≈ 600 Go de RAM pour 125 Go installés.
Ici, la mémoire est **bornée par construction** : on lit le fichier en blocs, on décide
bloc par bloc, et le jeu des shingles « déjà vus » est **échantillonné** à un taux dérivé
du budget (`--memoire-mo`).

MÉTHODE.

1. **Découpe.** Blocs de `--bloc-mo` Mio, coupés au dernier saut de ligne (aucune ligne
   n'est coupée), plus une marge de contexte **après** le bloc (2 % du bloc, au plus
   1 Mio, ou `--recouvrement-mo`) : elle sert à terminer les fenêtres qui commencent dans
   les derniers octets du bloc. Le **cœur** est ce qui sera écrit.
2. **Normalisation.** Minuscules ASCII (`bytes.lower`) et espaces horizontaux réduits
   (`[ \\t\\r\\f\\v]+` → un espace). Les **sauts de ligne sont conservés** : c'est ce qui
   permet l'ancrage ci-dessous.
3. **Ancrage des shingles (le point clé).** Un shingle est une fenêtre de `--shingle`
   oct
… [9318 caractères tronqués]
  ```

- **bash** `{"command": "cat work/dedup/prouve-200Mo.json | head -80; echo '---'; cat work/dedup/prouve-200Mo.log; echo '---'; python3 --version; python3 -c 'import numpy; print(numpy.__version__)' 2>&1; which time; git status --porcelain | head -20; cat .gitignore", "description": "Inspect proof JSON, env, git … [8 caractères tronqués]`

  ```
{
 "outil": "tools/dedup_blocs.py",
 "date": "2026-11-18T11:11:31",
 "verdict": "ok",
 "entree": {
  "chemin": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/slice-200Mo.txt",
  "octets": 200000000,
  "mtime": "2026-11-18T10:46:48"
 },
 "sortie": {
  "chemin": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/slice-200Mo-garde.txt",
  "octets": 200000000,
  "sha256": "8bf0f29ec75f971fbd3b25cfe0e7df3b3d721a9d1461953d4081a91a587adf8c",
  "lignes": 1741348
 },
 "parametres": {
  "bloc_mo": 8.0,
  "memoire_mo": 256.0,
  "shingle_octets": 96,
  "pas": 48,
  "seuil": 0.8,
  "hash_bits": 64,
  "graine": 0,
  "recouvrement_mo": null
 },
 "memoire": {
  "budget_mio": 256.0,
  "plancher_mio": 112.6,
  "bloc_mio": 8.0,
  "recouvrement_octets": 167772,
  "recouvrement_origine": "2 % du bloc, plafonné à 1 Mio",
  "cout_entree": {
   "cout_entree_octets": 80.0,
   "source": "mesure 2026-11-18 : set de 10 M d'entiers 64 bits = 757 Mio de ru_maxrss, soit 79,4 o/entrée"
  },
  "ancres_attendues": 6250000,
  "capacite_entrees": 1879048,
  "taux_echantillonnage": "1/8",
  "p": 0.125,
  "plafond_test_mio": null,
  "rss_max_mio": 120.8,
  "marge_mio": 135.2
 },
 "shingles": {
  "
… [3982 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'def \\|ERREUR\\|autotest\\|argparse\\|add_argument' tools/dedup_blocs.py | head -80", "description": "Map functions and CLI in dedup_blocs.py"}`

  ```
48:   nommée** si le RSS dépasse le budget (`ERREUR memoire_depassee`, code 3) ; idem si le
63:  python3 tools/dedup_blocs.py --autotest          # contrôle négatif reproductible
65:                                                   # → ERREUR budget_memoire_impossible
72:import argparse
119:    def __init__(self, nom: str, message: str):
126:def normalise(bloc: bytes) -> bytes:
136:def melange(x: int) -> int:
144:def hacheur(bits: int, graine: int):
147:        def h(w: bytes) -> int:
150:        def h(w: bytes) -> int:
155:def cout_entree() -> dict:
170:def rss_max_octets() -> int:
176:def est_sous(chemin: pathlib.Path, racine: pathlib.Path) -> bool:
180:def ecrit_json(chemin: str | pathlib.Path, objet: dict) -> None:
186:def parametres_json(a) -> dict:
199:def valide(a) -> None:
215:def execute(a, rapport: dict) -> None:
327:    def remplir(jusqua: int) -> None:
335:    def classe(fraction: float) -> str:
501:def squelette(a) -> dict:
566:def genere_texte(graine: int, n_paragraphes: int, octets_par_paragraphe: int,
585:def disperse(texte: bytes, fraction: float, graine: int, vocabulaire: list[str]) -> bytes:
602:def lance_autotest(repertoire: pathlib.Path) -> tuple[bool, dict]:

… [2163 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '220,430p' tools/dedup_blocs.py", "description": "Read execute core of dedup_blocs.py"}`

  ```
if not entree.is_file():
        raise ErreurNommee("entree_invalide", f"{entree} n'est pas un fichier lisible")
    if entree == sortie:
        raise ErreurNommee("sortie_invalide", "l'entrée et la sortie sont le même fichier")
    if est_sous(sortie, RACINE / "data"):
        raise ErreurNommee("sortie_interdite", f"{sortie} est sous data/ (lecture seule)")
    if sortie.parent.exists() and not sortie.parent.is_dir():
        raise ErreurNommee("sortie_invalide", f"{sortie.parent} n'est pas un répertoire")
    sortie.parent.mkdir(parents=True, exist_ok=True)

    taille = entree.stat().st_size
    bloc_o = max(int(a.bloc_mo * MIB), a.shingle * LONGUEUR_MIN_BLOC, 4096)
    if a.recouvrement_mo is None:
        rec_o = max(a.shingle, min(MIB, int(0.02 * bloc_o)))
        rec_origine = "2 % du bloc, plafonné à 1 Mio"
    else:
        rec_o = max(a.shingle, int(a.recouvrement_mo * MIB))
        rec_origine = "--recouvrement-mo"

    budget_o = int(a.memoire_mo * MIB)
    cal = cout_entree()
    besoin_bloc = FACTEUR_BLOC * (bloc_o + rec_o) + DIVERS_BLOC_MO * MIB
    plancher = besoin_bloc + PLANCHER_MO * MIB
    attendus = max(1, math.ceil(1.5 * taille / a.pas))

    rapport["memoi
… [6718 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '490,620p' tools/dedup_blocs.py; echo '====='; sed -n '620,830p' tools/dedup_blocs.py", "description": "Read JSON skeleton, autotest and main"}`

  ```
})
    rapport["distribution"] = {"fraction_seuil": dist}
    rapport["journal_blocs"] = journal
    rapport["journal_tronque"] = blocs > len(journal)
    rapport["duree_s"] = round(duree, 1)
    rapport["debit_mio_s"] = round((taille / MIB) / duree, 1) if duree else None
    rapport["memoire"]["rss_max_mio"] = round(rss_max / MIB, 1)
    rapport["memoire"]["marge_mio"] = round((budget_o - rss_max) / MIB, 1)
    rapport["verdict"] = "ok"


def squelette(a) -> dict:
    return {
        "outil": "tools/dedup_blocs.py",
        "date": dt.datetime.now().isoformat(timespec="seconds"),
        "verdict": None,
        "entree": {"chemin": str(pathlib.Path(a.entree).resolve()) if a.entree else None,
                   "octets": None,
                   "mtime": None},
        "sortie": {"chemin": str(pathlib.Path(a.sortie).resolve()) if a.sortie else None,
                   "octets": 0, "sha256": None, "lignes": 0},
        "parametres": parametres_json(a),
        "memoire": {},
        "shingles": {},
        "blocs": {},
        "distribution": {},
        "duree_s": None,
        "journal_blocs": [],
        "comparaison_inventaire": {
            "source": "reports/rapport-donnees
… [16277 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/diagnostic_lignes_exact.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/diagnostic_lignes_exact.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """diagnostic_lignes_exact.py — la duplication ligne à ligne, exacte, sur tout le fichier.
3: 
4: `diagnostic_lignes.py` échantillonnait **par valeur de ligne** (un hachage tiré une fois
5: par valeur) : une ligne très répétée était retenue en entier ou pas du tout, d'où une
6: variance énorme (12,1 % d'octets dupliqués contre 3,7 à 5,1 % mesurés exactement sur des
7: tranches). Ici, pas d'échantillonnage : chaque ligne est hachée (40 bits de BLAKE2b, plus
8: sa longueur sur 24 bits, empaquetés dans un uint64), les 88,1 M de valeurs sont **triées**
9: (numpy, en place), et les doublons se lisent sur les voisins égaux.
10: 
11: Mémoire : un tableau de 8 octets par ligne, soit ≈ 0,7 Go pour les 7,50 Go — c'est un
12: diagnostic, pas l'outil (qui, lui, tient en 2 Go par échantillonnage).
13: 
14: Les collisions 40 bits (88,1 M² / 2⁴¹ ≈ 3 700) sont négligeables devant 88,1 M de lignes.
15: 
16: Usage :
17:   python3 work/dedup/diagnostic_lignes_exact.py
18: """
19: from __future__ import annotations
20: 
21: import argparse
22: impo
… [2896 caractères tronqués]
  ```

- **bash** `{"command": "cat work/dedup/diagnostic-lignes-exact.log; echo '---'; head -c 600 work/dedup/slice-200Mo.txt | od -c | head -20; echo '---'; sha256sum data/corpus_wiki_fr_texte/train.txt 2>/dev/null | head -1", "description": "Read exact-lines diagnostic log and input signature"}`

  ```
88114432 lignes, 7504078589 octets ; tableau 672 Mio
lignes déjà vues : 47563661 (53.98 %) ; octets : 621277675 (8.28 %)
catégorie        lignes        dupl.  % lignes         octets  octets dupl.  % octets
vides          23037969     23037968    100.0%       23037969      23037968    100.0%
1-19 o         20689727     16900629     81.7%      243994263     187886634     77.0%
20-79 o        23410695      6825264     29.2%      959609824     216037267     22.5%
80 o et +      20976041       799800      3.8%     6277436533     194315806      3.1%
	Command being timed: "python3 work/dedup/diagnostic_lignes_exact.py"
	User time (seconds): 140.25
	System time (seconds): 9.79
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 2:30.05
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 3535964
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 2361586
	Voluntary context switches: 1
	Involuntary context switches: 231
	Swaps: 0
	File system inputs: 0
	File system outputs:
… [1676 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Benchmarking the per-line hash + exact table on 200 MB

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -v python3 - <<'PY' 2>&1 | tail -30\nimport array, hashlib, struct, time, resource\ncap = 1 << 24\nt0 = time.perf_counter()\ntab = array.array('Q', [0]) * cap\nprint('alloc', round(time.perf_counter()-t0,2), 's', 'rss', … [924 caractères tronqués]`

  ```
alloc 0.04 s rss 144.24609375
n 1741349 uniq 1015997 dup 263917 dt 2.72 lines/s 639842 rss 148.12890625
	Command being timed: "python3 -"
	User time (seconds): 2.71
	System time (seconds): 0.08
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:02.79
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 151684
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 2010
	Voluntary context switches: 1
	Involuntary context switches: 4
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
  ```

### 🤖 Assistant

⏵ Checking 1 GiB table allocation and RSS peak

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -v python3 - <<'PY' 2>&1 | tail -22\nimport array, resource, time\nt0=time.perf_counter()\nt = array.array('Q', [0]) * (1 << 27)\nprint('alloc 1GiB', round(time.perf_counter()-t0,2), 's', 'rss MiB', resource.getrusage(r … [235 caractères tronqués]`

  ```
User time (seconds): 0.18
	System time (seconds): 0.18
	Percent of CPU this job got: 100%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.36
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 1059996
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 1610
	Voluntary context switches: 1
	Involuntary context switches: 1
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
               total        used        free      shared  buff/cache   available
Mem:          128795       42955       14553       18307       90983       85839
  ```

### 🤖 Assistant

⏵ Writing `tools/dedup_lignes.py` (streaming exact line dedup)

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "content": "#!/usr/bin/env python3\n\"\"\"dedup_lignes.py — dédoublonner un texte **ligne à ligne**, en flux, à mémoire bornée.\n\nPOURQUOI. `reports/rapport-dedup-blocs.md` a mesuré que le dédoublonnage **par blo … [34158 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m py_compile tools/dedup_lignes.py && echo COMPILE_OK", "description": "Compile the new tool"}`

  ```
COMPILE_OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'journal_tronque\\|saturations\\|e_lignes_vides\\|lance_controle\\|b_copie_exacte' tools/dedup_lignes.py", "description": "Locate lines to patch"}`

  ```
415:        "saturations": 0,
431:    rapport["journal_tronque"] = lignes_lues > (
491:        "journal_tronque": False,
540:    def lance_controle(nom: str, sortie: str, *extra: str) -> tuple[int, dict, bytes]:
547:    rc1, r1, sortie1 = lance_controle("defaut", "defaut.txt")
551:    verifie("b_copie_exacte_ecartee",
563:    verifie("e_lignes_vides_preservees",
573:    rc1b, r1b, sortie1b = lance_controle("defaut_bis", "defaut-bis.txt")
582:    rc2, r2, sortie2 = lance_controle("normalise", "normalise.txt", "--normaliser")
588:    rc2b, r2b, _ = lance_controle("normalise_bis", "normalise-bis.txt", "--normaliser")
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "old_string": "    rapport[\"table\"] = {\n        \"slots_utilises\": slots_utilises,\n        \"charge_finale\": round(slots_utilises / mem[\"capacite_slots\"], 4),\n        \"entrees_max\": entrees_max,\n       … [245 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "old_string": "    rapport[\"journal\"] = journal\n    rapport[\"journal_tronque\"] = lignes_lues > (\n        journal[-1][\"lignes_lues\"] if journal else 0)", "new_string": "    rapport[\"journal\"] = journal\n  … [312 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "offset": 525, "limit": 100}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py</path>
<type>file</type>
<content>
525: 
526:     controle = repertoire / "controle.txt"
527:     controle.write_bytes(b"".join(LIGNES_CONTROLE))
528:     attendu_defaut = b"".join(LIGNES_CONTROLE[i] for i in GARDES_DEFAUT)
529:     attendu_normalise = b"".join(LIGNES_CONTROLE[i] for i in GARDES_NORMALISE)
530:     n_vides = sum(1 for ligne in LIGNES_CONTROLE if not ligne.rstrip())
531: 
532:     def lance(nom: str, args: list[str]) -> tuple[int, dict, str]:
533:         json_path = repertoire / f"{nom}.json"
534:         cmd = [sys.executable, outil, *args, "--json", str(json_path)]
535:         p = subprocess.run(cmd, capture_output=True, text=True)
536:         manifeste = json.loads(json_path.read_text()) if json_path.exists() else {}
537:         return p.returncode, manifeste, (p.stderr or "") + (p.stdout or "")
538: 
539:     cas: list[dict] = []
540: 
541:     def verifie(nom: str, condition: bool, detail) -> None:
542:         cas.append({"nom": nom, "ok": bool(condition), "detail": detail})
543: 
544:     def lance_controle(nom: str, sortie: str, *extra: str) -> tuple[int, dict, bytes]:
545:      
… [5081 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "new_string": "    def lance(nom: str, args: list[str]) -> tuple[int, dict, str]:\n        json_path = repertoire / f\"{nom}.json\"\n        cmd = [sys.executable, outil, *args, \"--json\", str(json_path)]\n       … [677 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "new_string": "    verifie(\"b_copie_exacte_ecartee\",\n            r1.get(\"lignes\", {}).get(\"ecartees\") == 2,\n            {\"ecartees\": r1.get(\"lignes\", {}).get(\"ecartees\"), \"attendu\": 2})\n    # (b)  … [2234 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "new_string": "    verifie(\"e_lignes_vides_preservees\",\n            r1.get(\"lignes\", {}).get(\"vides_lues\") == n_vides\n            and sortie1.count(b\"\\n\") == len(GARDES_DEFAUT),\n            {\"vides_at … [591 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

### 🤖 Assistant

⏵ Running the six-case autotest suite

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m py_compile tools/dedup_lignes.py && /usr/bin/time -v python3 tools/dedup_lignes.py --autotest 2>work/dedup/autotest-lignes.log | tail -80; echo \"RC=${PIPESTATUS[0]}\"; echo '--- LOG ---'; tail -20 work/dedup/autotest-lign … [56 caractères tronqués]`

  ```
RC=1
--- LOG ---
	Percent of CPU this job got: 100%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:01.32
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 166376
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 48939
	Voluntary context switches: 41
	Involuntary context switches: 4
	Swaps: 0
	File system inputs: 0
	File system outputs: 36720
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nr=json.load(open('work/dedup/autotest-lignes/autotest.json'))\nprint('ok', r['ok'])\nfor c in r['cas']:\n    print(('OK ' if c['ok'] else 'FAIL'), c['nom'], c['detail'])\nPY", "description": "Show autot … [18 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
FileNotFoundError: [Errno 2] No such file or directory: 'work/dedup/autotest-lignes/autotest.json'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat work/dedup/autotest-lignes.log | head -60; ls -la work/dedup/autotest-lignes/ 2>/dev/null | head", "description": "Read full autotest stderr log"}`

  ```
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", line 766, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", line 717, in main
    ok, resume = lance_autotest(pathlib.Path(a.repertoire))
                 ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", line 675, in lance_autotest
    ecrit_json(repertoire / "autotest.json", resume)
    ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", line 125, in ecrit_json
    p.write_text(json.dumps(objet, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
                 ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.13/json/__init__.py", line 242, in dumps
    **kw).encode(obj)
          ~~~~~~^^^^^
  File "/usr/lib64/python3.13/json/encoder.py", line 202, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "/usr/lib64/python3.13/json/encoder.py", line 263, in iterencode
    return _it
… [1696 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/dedup_lignes.py')\ns=p.read_text()\ns=s.replace('{\"prefixe\": sortie1[:24]})', '{\"prefixe\": sortie1[:24].decode(\"utf-8\", \"replace\")})')\np.write_text(s)\nPY\npython3 -m … [98 caractères tronqués]`

  ```
OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/dedup_lignes.py --autotest > work/dedup/autotest-lignes.out 2> work/dedup/autotest-lignes.err; echo \"RC=$?\"; python3 - <<'PY'\nimport json\nr=json.load(open('work/dedup/autotest-lignes/autotest.json'))\nprint('ok', r[ … [331 caractères tronqués]`

  ```
RC=1
ok False | lignes controle 12 | vides 4
OK   a_ligne_unique_gardee | {"rc": 0, "non_vides_gardees": 6}
OK   b_copie_exacte_ecartee | {"ecartees": 2, "attendu": 2}
OK   b_copie_exacte_seule_ecartee | {"rc": 0, "ecartees": 1, "sortie_identique": true}
OK   c_espaces_de_fin_seuls_ecartes | {"rc": 0, "ecartees": 1, "sortie_identique": true}
OK   c_espaces_de_fin_ecartes_par_defaut | {"sortie_octets": 121, "attendu_octets": 121, "identique": true}
OK   c_premiere_occurrence_telle_quelle | {"prefixe": "ligne unique alpha   \nli"}
OK   d_ligne_differente_gardee | {"presente": true}
OK   e_lignes_vides_preservees | {"vides_attendues": 4, "vides_json": 4, "lignes_sortie": 10}
OK   e_ligne_espaces_preservee | {"presente": true}
OK   f_deux_passes_meme_sha256 | {"sha1": "3de1a6d949aa169ed891b1e1968c7e6fcc701e3982e2a1ecc33741858e6df89b", "sha2": "3de1a6d949aa169ed891b1e1968c7e6fcc701e3982e2a1ecc33741858e6df89b", "sortie
OK   normaliser_ecarte_minuscules_et_espaces | {"rc": 0, "ecartees": 4, "attendu": 4, "identique": true}
OK   normaliser_stable | {"sha1": "a8667c3cabf663a6278062c7a5fd154df434da4b9ff27a0a7828f1dd197f2cfe", "sha2": "a8667c3cabf663a6278062c7a5fd154df434da4b9ff27a0a7828f1dd1
… [629 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport resource, subprocess, sys, os\n# parent takes 180 MiB\nblob = bytearray(180 * (1<<20))\nfor i in range(0, len(blob), 4096): blob[i] = 1\nprint('parent ru_maxrss MiB', resource.getrusage(resource.RUSAGE_SELF). … [664 caractères tronqués]`

  ```
parent ru_maxrss MiB 193.01953125
child ru_maxrss MiB 193.01953125
parent VmRSS MiB 193.1
child VmRSS 10972
  ```

### 🤖 Assistant

⏵ Fixing RSS measurement (fork-inherited `ru_maxrss` quirk) and autotest footprint

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "new_string": "def rss_max_octets() -> int:\n    \"\"\"RSS maximal du processus (ru_maxrss est en Kio sous Linux, en octets sous macOS).\n\n    ATTENTION : sous Linux, `ru_maxrss` est **hérité** à travers fork/exe … [1155 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "limit": 40, "offset": 110}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py</path>
<type>file</type>
<content>
110: 
111: # --- briques -----------------------------------------------------------------
112: def rss_max_octets() -> int:
113:     """RSS maximal du processus (ru_maxrss est en Kio sous Linux, en octets sous macOS)."""
114:     brut = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
115:     return brut if sys.platform == "darwin" else brut * 1024
116: 
117: 
118: def est_sous(chemin: pathlib.Path, racine: pathlib.Path) -> bool:
119:     return chemin == racine or racine in chemin.parents
120: 
121: 
122: def ecrit_json(chemin: str | pathlib.Path, objet: dict) -> None:
123:     p = pathlib.Path(chemin)
124:     p.parent.mkdir(parents=True, exist_ok=True)
125:     p.write_text(json.dumps(objet, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
126: 
127: 
128: def modele_memoire(budget_o: int) -> dict:
129:     """Budget → capacité de table. Le plafond est le budget ; la table est le seul gros poste."""
130:     plancher_o = int(PLANCHER_MO * MIB)
131:     dispo = budget_o - plancher_o
132:     minimum = SLOTS_MIN * COUT_SLOT
133:     if dispo < minimum:
134:    
… [876 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "new_string": "# --- briques -----------------------------------------------------------------\ndef rss_max_octets() -> int:\n    \"\"\"RSS maximal du processus (ru_maxrss est en Kio sous Linux, en octets sous mac … [1317 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'rss_max\\|rss_max_octets' tools/dedup_lignes.py", "description": "Locate RSS usages"}`

  ```
112:def rss_max_octets() -> int:
134:    return rss_max_octets()
259:    rss_max = 0
275:    rss_max = rss_max_octets()
276:    if rss_max > plafond_o:
281:            f"RSS max {rss_max / MIB:.0f} Mio > plafond {plafond_o / MIB:.0f} Mio "
342:                rss_max = max(rss_max, rss_max_octets())
343:                if rss_max > plafond_o:
346:                        f"RSS max {rss_max / MIB:.0f} Mio > plafond "
355:                        "rss_mio": round(rss_max / MIB, 1),
376:    rss_max = max(rss_max, rss_max_octets())
377:    if rss_max > plafond_o:
380:            f"RSS max {rss_max / MIB:.0f} Mio > plafond {plafond_o / MIB:.0f} Mio "
436:        "rss_max_mio": round(rss_max / MIB, 1),
437:        "marge_mio": round((budget_o - rss_max) / MIB, 1),
778:        "rss_max_mio": rapport["memoire"].get("rss_max_mio"),
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "limit": 45, "offset": 252}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py</path>
<type>file</type>
<content>
252: 
253:     lignes_lues = lignes_gardees = lignes_ecartees = 0
254:     lignes_vides = 0
255:     octets_lus = octets_gardes = octets_ecartes = octets_vides = 0
256:     premiere_vide_octets = None
257:     plus_longue = 0
258:     slots_utilises = 0
259:     rss_max = 0
260:     journal: list[dict] = []
261:     prochain_check = CHECK_LIGNES
262:     prochain_journal = t0 + 10.0
263:     sha = hashlib.sha256()
264:     tampon = bytearray()
265: 
266:     f_in = open(entree, "rb", buffering=tampon_o)
267:     try:
268:         f_out = open(sortie, "wb", buffering=tampon_o)
269:     except OSError:
270:         f_in.close()
271:         raise
272: 
273:     # Le chien de garde vaut aussi pour l'allocation : un plafond de test de 1 Mio doit
274:     # échouer tout de suite, sans attendre la première ligne.
275:     rss_max = rss_max_octets()
276:     if rss_max > plafond_o:
277:         f_in.close()
278:         f_out.close()
279:         raise ErreurNommee(
280:             "memoire_depassee",
281:             f"RSS max {rss_max / MIB:.0f} Mio > plafond {plafond_o / MIB:
… [543 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "new_string": "    slots_utilises = 0\n    rss_max = 0\n    rss_ru = 0\n    journal: list[dict] = []", "old_string": "    slots_utilises = 0\n    rss_max = 0\n    journal: list[dict] = []"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "new_string": "    # Le chien de garde vaut aussi pour l'allocation : un plafond de test de 1 Mio doit\n    # échouer tout de suite, sans attendre la première ligne. On mesure le VmRSS courant,\n    # pas ru_maxrs … [904 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "new_string": "            if lignes_lues >= prochain_check:\n                prochain_check += CHECK_LIGNES\n                rss_max = max(rss_max, rss_courant_octets())\n                rss_ru = max(rss_ru, rss_ … [266 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "new_string": "    duree = time.perf_counter() - t0\n    rss_max = max(rss_max, rss_courant_octets())\n    rss_ru = max(rss_ru, rss_max_octets())\n    if rss_max > plafond_o:", "old_string": "    duree = time.perf … [92 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "new_string": "    rapport[\"memoire\"].update({\n        \"rss_max_mio\": round(rss_max / MIB, 1),\n        \"rss_max_source\": \"maximum de VmRSS (/proc/self/status), échantillonné après \"\n                     … [421 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "new_string": "    grosses = repertoire / \"grosses.txt\"\n    with open(grosses, \"wb\", buffering=int(TAMPON_IO_MO * MIB)) as f:\n        for debut in range(0, 850_000, 20_000):\n            f.write(b\"\".join(\ … [271 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rm -rf work/dedup/autotest-lignes && python3 -m py_compile tools/dedup_lignes.py && python3 tools/dedup_lignes.py --autotest > work/dedup/autotest-lignes.out 2> work/dedup/autotest-lignes.err; echo \"RC=$?\"; python3 - <<'PY'\nimport … [483 caractères tronqués]`

  ```
RC=0
ok True | lignes controle 12 | vides 4
OK   a_ligne_unique_gardee | {"rc": 0, "non_vides_gardees": 6}
OK   b_copie_exacte_ecartee | {"ecartees": 2, "attendu": 2}
OK   b_copie_exacte_seule_ecartee | {"rc": 0, "ecartees": 1, "sortie_identique": true}
OK   c_espaces_de_fin_seuls_ecartes | {"rc": 0, "ecartees": 1, "sortie_identique": true}
OK   c_espaces_de_fin_ecartes_par_defaut | {"sortie_octets": 121, "attendu_octets": 121, "identique": true}
OK   c_premiere_occurrence_telle_quelle | {"prefixe": "ligne unique alpha   \nli"}
OK   d_ligne_differente_gardee | {"presente": true}
OK   e_lignes_vides_preservees | {"vides_attendues": 4, "vides_json": 4, "lignes_sortie": 10}
OK   e_ligne_espaces_preservee | {"presente": true}
OK   f_deux_passes_meme_sha256 | {"sha1": "3de1a6d949aa169ed891b1e1968c7e6fcc701e3982e2a1ecc33741858e6df89b", "sha2": "3de1a6d949aa169ed891b1e1968c7e6fcc701e3982e2a1ecc33741858e6df89b", "sorties_identiques": true}
OK   normaliser_ecarte_minuscules_et_espaces | {"rc": 0, "ecartees": 4, "attendu": 4, "identique": true}
OK   normaliser_stable | {"sha1": "a8667c3cabf663a6278062c7a5fd154df434da4b9ff27a0a7828f1dd197f2cfe", "sha2": "a8667c3cabf663a6278062c7a5fd154df434da
… [1482 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Proving the 64 MiB ceiling on the 200 MB slice

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -v python3 tools/dedup_lignes.py --entree work/dedup/slice-200Mo.txt --sortie work/dedup/slice-200Mo-lignes.txt --memoire-mo 64 --json work/dedup/prouve-200Mo-lignes.json --verifier > work/dedup/prouve-200Mo-lignes.out  … [678 caractères tronqués]`

  ```
RC=0
{
 "entree_octets": 200000000,
 "sortie_octets": 192946503,
 "lignes_lues": 1741349,
 "lignes_gardees": 1477432,
 "lignes_ecartees": 263917,
 "pct_lignes_ecartees": 15.156,
 "pct_octets_ecartes": 3.527,
 "duree_s": 3.4,
 "rss_max_mio": 45.5,
 "sha256": "1ec785b6dab27396cfedbb802883a0777fa11e092b9d1f2e964fcfa4df320222"
}
--- time ---
	User time (seconds): 3.89
	System time (seconds): 0.22
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:04.11
	Maximum resident set size (kbytes): 50400
	Exit status: 0
--- json ---
entree {"chemin": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/slice-200Mo.txt", "octets": 200000000, "mtime": "2026-11-18T10:46:48"}
sortie {"chemin": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/slice-200Mo-lignes.txt", "octets": 192946503, "sha256": "1ec785b6dab27396cfedbb802883a0777fa11e092b9d1f2e964fcfa4df320222", "lignes": 1477432}
parametres {"memoire_mo": 64.0, "normaliser": false, "hachage": "BLAKE2b-64 (digest_size=8, non salé)", "lecture": "flux ligne à ligne, tampon 4 Mio", "verifier": true}
memoire {"budget_mio": 64.0, "plancher_mio": 48.0, "structure": "table de hachage exacte à adressage ouvert linéaire (array('Q'))", "octets
… [1692 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Running the 7.50 GB pass at 2048 MiB with output verification

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -v python3 tools/dedup_lignes.py --entree data/corpus_wiki_fr_texte/train.txt --sortie work/dedup/train-lignes.txt --memoire-mo 2048 --json reports/dedup-lignes-7.5go.json --verifier > work/dedup/train-lignes.out 2> wor … [140 caractères tronqués]`

  ```
RC=0
{
 "entree_octets": 7504078589,
 "sortie_octets": 6900585097,
 "lignes_lues": 88114432,
 "lignes_gardees": 63438199,
 "lignes_ecartees": 24676233,
 "pct_lignes_ecartees": 28.005,
 "pct_octets_ecartes": 8.042,
 "duree_s": 158.0,
 "rss_max_mio": 1053.7,
 "sha256": "e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552"
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -E 'Elapsed|Maximum resident|User time|System time|Exit status' work/dedup/train-lignes.log; echo '--- progress tail ---'; tail -6 work/dedup/train-lignes.log; echo '--- key JSON ---'; python3 - <<'PY'\nimport json\nr=json.load( … [411 caractères tronqués]`

  ```
User time (seconds): 170.35
	System time (seconds): 7.98
	Elapsed (wall clock) time (h:mm:ss or m:ss): 2:58.97
	Maximum resident set size (kbytes): 1078692
	Exit status: 0
--- progress tail ---
	File system outputs: 13477864
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
--- key JSON ---
verdict = "ok"
entree = {"chemin": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/corpus_wiki_fr_texte/train.txt", "octets": 7504078589, "mtime": "2026-11-01T17:25:40"}
sortie = {"chemin": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/train-lignes.txt", "octets": 6900585097, "sha256": "e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552", "lignes": 63438199}
parametres = {"memoire_mo": 2048.0, "normaliser": false, "hachage": "BLAKE2b-64 (digest_size=8, non salé)", "lecture": "flux ligne à ligne, tampon 4 Mio", "verifier": true}
memoire = {"budget_mio": 2048.0, "plancher_mio": 48.0, "structure": "table de hachage exacte à adressage ouvert linéaire (array('Q'))", "octets_par_slot": 8, "capacite_slots": 134217728, "octets_table": 1073741824, "charge_max": 0.8, "entrees_max": 107374182, "plafond_test
… [2010 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Splitting pass vs verification timings, then re-running cleanly

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'duree\\|debit_mio' tools/dedup_lignes.py | sed -n '1,40p'", "description": "Locate timing code"}`

  ```
379:    duree = time.perf_counter() - t0
454:    rapport["duree_s"] = round(duree, 1)
455:    rapport["debit_mio_s"] = round((taille / MIB) / duree, 1) if duree else None
519:        "duree_s": None,
520:        "debit_mio_s": None,
770:        rapport["duree_s"] = round(time.perf_counter() - t_debut, 1)
789:        "duree_s": rapport["duree_s"],
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "limit": 30, "offset": 374}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "limit": 18, "offset": 446}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py</path>
<type>file</type>
<content>
374:             tampon.clear()
375:     finally:
376:         f_in.close()
377:         f_out.close()
378: 
379:     duree = time.perf_counter() - t0
380:     rss_max = max(rss_max, rss_courant_octets())
381:     rss_ru = max(rss_ru, rss_max_octets())
382:     if rss_max > plafond_o:
383:         raise ErreurNommee(
384:             "memoire_depassee",
385:             f"RSS max {rss_max / MIB:.0f} Mio > plafond {plafond_o / MIB:.0f} Mio "
386:             f"en fin de passe",
387:         )
388: 
389:     sha_hex = sha.hexdigest()
390:     lignes_non_vides = lignes_lues - lignes_vides
391:     lignes_non_vides_gardees = lignes_gardees - lignes_vides
392:     # Ce que donnerait la même passe si les lignes vides étaient dédoublonnées comme dans
393:     # le diagnostic exact (toutes sauf la première) : directement comparable aux 53,98 %.
394:     vides_ecartees_equiv = max(0, lignes_vides - 1)
395:     octets_vides_ecartes_equiv = max(0, octets_vides - (premiere_vide_octets or 0))
396:     lignes_equiv = lignes_ecartees + vides_ecartees_equiv
397:     octets_equiv = octets_
… [271 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py</path>
<type>file</type>
<content>
446:         "plafond_atteint": False,
447:     })
448:     rapport["integrite"] = {
449:         "sha256_sortie": sha_hex,
450:         "octets": octets_gardes,
451:         "lignes": lignes_gardees,
452:         "verifie": False,
453:     }
454:     rapport["duree_s"] = round(duree, 1)
455:     rapport["debit_mio_s"] = round((taille / MIB) / duree, 1) if duree else None
456:     rapport["journal"] = journal
457:     rapport["journal_tronque"] = len(journal) >= JOURNAL_MAX
458:     # Contrôle interne : la somme des longueurs lues doit être la taille du fichier.
459:     rapport["integrite_lecture"] = {
460:         "octets_lus": octets_lus,
461:         "octets_stat": taille,
462:         "coherent": octets_lus == taille,
463:     }

(Showing lines 446-463 of 797. Use offset=464 to continue.)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "limit": 25, "offset": 463}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py</path>
<type>file</type>
<content>
463:     }
464: 
465:     if a.verifier:
466:         rapport["integrite"].update(
467:             verifie_sortie(sortie, octets_gardes, lignes_gardees, sha_hex))
468: 
469:     # Comparaison directe avec le diagnostic exact du rapport blocs (§ 4.3).
470:     rapport["comparaison_blocs"] = {
471:         "source": "reports/rapport-dedup-blocs.md § 4.3 (mesure exacte, 2026-11-18)",
472:         "lignes_dupliquees_pct_diagnostic": 53.98,
473:         "octets_dupliques_pct_diagnostic": 8.28,
474:         "lignes_vides_diagnostic": 23037969,
475:         "note": "le diagnostic supprimait toutes les lignes vides sauf une ; ici toutes "
476:                 "sont préservées, d'où deux taux : effectif (vides gardées) et équivalent "
477:                 "(vides dédoublonnées comme le diagnostic)",
478:         "mesure_equivalente": {
479:             "lignes_ecartees": lignes_equiv,
480:             "pct_lignes_ecartees": round(100 * lignes_equiv / lignes_lues, 3)
481:             if lignes_lues else 0.0,
482:             "octets_ecartes": octets_equiv,
483:             "pct_oct
… [230 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "new_string": "    duree_passe = time.perf_counter() - t0\n    rss_max = max(rss_max, rss_courant_octets())", "old_string": "    duree = time.perf_counter() - t0\n    rss_max = max(rss_max, rss_courant_octets())"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "new_string": "    rapport[\"duree_s\"] = None  # rempli après l'éventuelle vérification de sortie\n    rapport[\"debit_mio_s\"] = None\n    rapport[\"journal\"] = journal", "old_string": "    rapport[\"duree_s\"] … [140 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "new_string": "    if a.verifier:\n        rapport[\"integrite\"].update(\n            verifie_sortie(sortie, octets_gardes, lignes_gardees, sha_hex))\n\n    duree = time.perf_counter() - t0\n    rapport[\"duree_s … [512 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py", "new_string": "        \"duree_s\": None,\n        \"duree_passe_s\": None,\n        \"duree_verification_s\": None,\n        \"debit_mio_s\": None,\n        \"debit_total_mio_s\": None,", "old_string": "        \ … [51 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_lignes.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/dedup_lignes.py')\ns=p.read_text()\ns=s.replace('''        \"duree_s\": rapport[\"duree_s\"],\n        \"rss_max_mio\"''','''        \"duree_s\": rapport[\"duree_s\"],\n       … [792 caractères tronqués]`

  ```
AUTOTEST_RC=0
ok True | cas 16 / 16
duree defaut 0.0 passe 0.0 verif 0.0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -v python3 tools/dedup_lignes.py --entree work/dedup/slice-200Mo.txt --sortie work/dedup/slice-200Mo-lignes.txt --memoire-mo 64 --json work/dedup/prouve-200Mo-lignes.json --verifier > work/dedup/prouve-200Mo-lignes.out  … [855 caractères tronqués]`

  ```
RC=0
{
 "entree_octets": 200000000,
 "sortie_octets": 192946503,
 "lignes_lues": 1741349,
 "lignes_gardees": 1477432,
 "lignes_ecartees": 263917,
 "pct_lignes_ecartees": 15.156,
 "pct_octets_ecartes": 3.527,
 "duree_s": 4.1,
 "duree_passe_s": 3.5,
 "rss_max_mio": 45.7,
 "sha256": "1ec785b6dab27396cfedbb802883a0777fa11e092b9d1f2e964fcfa4df320222"
}
	User time (seconds): 3.70
	System time (seconds): 0.18
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:04.21
	Maximum resident set size (kbytes): 50496
duree 4.1 passe 3.5 verif 0.6 debits 53.7 46.1
memoire {'budget_mio': 64.0, 'rss_max_mio': 45.7, 'ru_maxrss_mio': 49.3, 'marge_mio': 18.3, 'octets_table': 16777216, 'capacite_slots': 2097152}
integrite True True
lignes {'lues': 1741349, 'gardees': 1477432, 'ecartees': 263917, 'vides_lues': 461435, 'vides_gardees': 461435, 'non_vides_lues': 1279914, 'non_vides_gardees': 1015997, 'non_vides_ecartees': 263917, 'plus_longue_ligne_octets': 5457}
taux {'pct_lignes_ecartees': 15.156, 'pct_lignes_ecartees_hors_vides': 20.62, 'pct_octets_ecartes': 3.527, 'pct_octets_vides': 0.231, 'pct_sortie': 96.473}
equivalent {'lignes_ecartees': 725351, 'pct_lignes_ecartees': 41.655, 'octets_ecartes': 7514931,
… [29 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Re-running the 7.50 GB pass with corrected timing split

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -v python3 tools/dedup_lignes.py --entree data/corpus_wiki_fr_texte/train.txt --sortie work/dedup/train-lignes.txt --memoire-mo 2048 --json reports/dedup-lignes-7.5go.json --verifier > work/dedup/train-lignes.out 2> wor … [243 caractères tronqués]`

  ```
RC=0
{
 "entree_octets": 7504078589,
 "sortie_octets": 6900585097,
 "lignes_lues": 88114432,
 "lignes_gardees": 63438199,
 "lignes_ecartees": 24676233,
 "pct_lignes_ecartees": 28.005,
 "pct_octets_ecartes": 8.042,
 "duree_s": 176.1,
 "duree_passe_s": 156.0,
 "rss_max_mio": 1053.8,
 "sha256": "e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552"
}
	User time (seconds): 166.07
	System time (seconds): 7.32
	Elapsed (wall clock) time (h:mm:ss or m:ss): 2:56.21
	Maximum resident set size (kbytes): 1078364
	Exit status: 0
  ```

### 🤖 Assistant

⏵ Proving idempotence: second pass on the output should remove nothing

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -v python3 tools/dedup_lignes.py --entree work/dedup/train-lignes.txt --sortie /dev/null --memoire-mo 2048 --json work/dedup/idempotence-train-lignes.json > work/dedup/idempotence-train-lignes.out 2> work/dedup/idempote … [749 caractères tronqués]`

  ```
RC=0
{
 "entree_octets": 6900585097,
 "sortie_octets": 6900585097,
 "lignes_lues": 63438199,
 "lignes_gardees": 63438199,
 "lignes_ecartees": 0,
 "pct_lignes_ecartees": 0.0,
 "pct_octets_ecartes": 0.0,
 "duree_s": 111.2,
 "duree_passe_s": 111.2,
 "rss_max_mio": 1053.8,
 "sha256": "e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552"
}
	User time (seconds): 107.40
	System time (seconds): 3.86
	Elapsed (wall clock) time (h:mm:ss or m:ss): 1:51.27
	Maximum resident set size (kbytes): 1078780
	Exit status: 0
ecartees 0 | sha e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552 | octets 6900585097 | lignes 63438199
sha identique passe 1 ? True
memoire {'rss_max_mio': 1053.8, 'ru_maxrss_mio': 1053.5, 'marge_mio': 994.2} | table {'slots_utilises': 40400230, 'charge_finale': 0.301, 'entrees_max': 107374182}
  ```

### 🤖 Assistant

⏵ External checks on the 6.90 GB output (sha, lines, size)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum work/dedup/train-lignes.txt && stat -c 'octets=%s mtime=%y' work/dedup/train-lignes.txt && wc -l work/dedup/train-lignes.txt && echo '--- input (lecture seule) ---' && stat -c 'octets=%s mtime=%y' data/corpus_wiki_fr_texte/ … [156 caractères tronqués]`

  ```
e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552  work/dedup/train-lignes.txt
octets=6900585097 mtime=2026-11-18 12:06:41.525651357 -0500
63438199 work/dedup/train-lignes.txt
--- input (lecture seule) ---
octets=7504078589 mtime=2026-11-01 17:25:40.769701171 -0500
[still running after 60000ms; moved to background job bash-762]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nI=7504078589; O=6900585097\nL=88114432; LK=63438199; LE=24676233; V=23037969; NV=65076463\nOE=603493492; OV=23037969\ndiag_l=47563661; diag_b=621277675; diag_ev=23037968\ndiag_nv=diag_l-diag_ev; diag_nvb=diag_b-2303 … [970 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 6, in <module>
TypeError: not enough arguments for format string
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nI=7504078589; O=6900585097\nL=88114432; LK=63438199; LE=24676233; V=23037969; NV=65076463\nOE=603493492; OV=23037969\ndiag_l=47563661; diag_b=621277675; diag_ev=23037968\ndiag_nv=diag_l-diag_ev; diag_nvb=diag_b-2303 … [978 caractères tronqués]`

  ```
sortie % du fichier : 91.958
octets ecartes % : 8.042
lignes ecartees % : 28.005
non vides ecartees % : 37.919
diag non vides : lignes 24525693 = 27.834 % du total, 37.688 % des non-vides
diag non vides octets 598239707 = 7.972 %
extra lignes 150540 = 0.171 point
extra octets 5253785 = 0.070 point
equiv lignes 47714201 = 54.150 %
equiv octets 626531460 = 8.349 %
vides octets % 0.307
output GiB 6.427, input GiB 6.989
debit passe MiB/s 45.87, total 40.64
charge table 0.3010
  ```

- **job_output** `{"job_id": "bash-762", "wait": true, "timeout_ms": 120000}`

  ```
27277e320d7781e0dc8957a449fff386a7d1fa712838bba42f8a1e728dd0924b  data/corpus_wiki_fr_texte/train.txt
--- df ---
/dev/mapper/system-root   11T  9,0T  1,9T  83% /home/stephane/Data13TB
[status: completed, exit code: 0]
  ```

### 🤖 Assistant

⏵ Measuring the `--normaliser` variant on the full corpus (output to `/dev/null`)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -v python3 tools/dedup_lignes.py --entree data/corpus_wiki_fr_texte/train.txt --sortie /dev/null --memoire-mo 2048 --normaliser --json work/dedup/normalise-train-lignes.json > work/dedup/normalise-train-lignes.out 2> wo … [1020 caractères tronqués]`

  ```
RC=0
{
 "entree_octets": 7504078589,
 "sortie_octets": 6894056525,
 "lignes_lues": 88114432,
 "lignes_gardees": 63273652,
 "lignes_ecartees": 24840780,
 "pct_lignes_ecartees": 28.191,
 "pct_octets_ecartes": 8.129,
 "duree_s": 260.8,
 "duree_passe_s": 260.8,
 "rss_max_mio": 1053.9,
 "sha256": "839385ecc589b6cba596707c3e2c16cc0ac665225f7dbf16f2a4d8d48def1cb7"
}
	User time (seconds): 254.83
	System time (seconds): 5.99
	Elapsed (wall clock) time (h:mm:ss or m:ss): 4:20.84
	Maximum resident set size (kbytes): 1079544
	Exit status: 0
normalise: ecartees 24840780 octets 610022064 sortie 6894056525 sha 839385ecc589b6cba596707c3e2c16cc0ac665225f7dbf16f2a4d8d48def1cb7
defaut   : ecartees 24676233 octets 603493492 sortie 6900585097
delta lignes 164547 delta octets 6528572
taux {'pct_lignes_ecartees': 28.191, 'pct_lignes_ecartees_hors_vides': 38.172, 'pct_octets_ecartes': 8.129, 'pct_octets_vides': 0.307, 'pct_sortie': 91.871} | equiv {'lignes_ecartees': 47878748, 'pct_lignes_ecartees': 54.337, 'octets_ecartes': 633060032, 'pct_octets_ecartes': 8.436}
rss 1053.9 1054.2 | duree 260.8
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nr=json.load(open('reports/dedup-lignes-7.5go.json'))\nm=r['memoire']\nprint({k:m[k] for k in ('budget_mio','plancher_mio','rss_max_mio','ru_maxrss_mio','marge_mio','capacite_slots','octets_table','entre … [309 caractères tronqués]`

  ```
{'budget_mio': 2048.0, 'plancher_mio': 48.0, 'rss_max_mio': 1053.8, 'ru_maxrss_mio': 1053.1, 'marge_mio': 994.2, 'capacite_slots': 134217728, 'octets_table': 1073741824, 'entrees_max': 107374182, 'charge_max': 0.8}
table {'slots_utilises': 40400230, 'charge_finale': 0.301, 'entrees_max': 107374182}
durees {'duree_s': 176.1, 'duree_passe_s': 156.0, 'duree_verification_s': 20.1, 'debit_mio_s': 45.9, 'debit_total_mio_s': 40.6}
integrite {'sha256_sortie': 'e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552', 'octets': 6900585097, 'lignes': 63438199, 'verifie': True, 'methode': 'relecture séquentielle par blocs de 4 Mio', 'octets_relus': 6900585097, 'lignes_relues': 63438199, 'sha256_relu': 'e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552'}
journal [{'lignes_lues': 5177344, 'pct_lignes_ecartees': 16.66, 'rss_mio': 1053.7, 's': 10.1}, {'lignes_lues': 11206656, 'pct_lignes_ecartees': 21.53, 'rss_mio': 1053.8, 's': 20.1}, {'lignes_lues': 17235968, 'pct_lignes_ecartees': 23.68, 'rss_mio': 1053.8, 's': 30.1}, {'lignes_lues': 22609920, 'pct_lignes_ecartees': 23.59, 'rss_mio': 1053.8, 's': 40.2}, {'lignes_lues': 28442624, 'pct_lignes_ecartees': 23.87, 'rss_mio': 
… [895 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/dedup_lignes.py --entree work/dedup/slice-200Mo.txt --sortie work/dedup/jamais-budget.txt --memoire-mo 8 --json work/dedup/budget-impossible-8.json > work/dedup/budget-impossible-8.out 2> work/dedup/budget-impossible-8. … [303 caractères tronqués]`

  ```
RC=3
ERREUR budget_memoire_impossible: budget 8 Mio < plancher 48 Mio + 8 Mio (table minimale de 1048576 cases à 8 o) — augmentez --memoire-mo
erreur {'nom': 'budget_memoire_impossible', 'message': 'budget 8 Mio < plancher 48 Mio + 8 Mio (table minimale de 1048576 cases à 8 o) — augmentez --memoire-mo'} 0.0
ls: cannot access 'work/dedup/jamais-budget.txt': No such file or directory
  ```

### 🤖 Assistant

⏵ Checking workspace hygiene and gathering final report facts

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && find tools -maxdepth 2 -name '*dedup_lignes*' -o -name '__pycache__' | head; echo '---'; git status --porcelain | head -30; echo '--- json date ---'; python3 -c \"import json;r=json.load(open('reports/dedup-lignes-7.5go.json'));print … [100 caractères tronqués]`

  ```
tools/__pycache__
tools/__pycache__/dedup_lignes.cpython-313.pyc
tools/jeux/__pycache__
tools/llm/__pycache__
tools/semantique/__pycache__
tools/cerveau/__pycache__
tools/tests/__pycache__
tools/pensee/__pycache__
tools/structures/__pycache__
tools/dedup_lignes.py
---
?? reports/banc-generation-r2.json
?? reports/banc-grammaticalite-r2.json
?? reports/dedup-lignes-7.5go.json
?? tools/dedup_lignes.py
--- json date ---
2026-11-18T12:04:06
{'chemin': '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/corpus_wiki_fr_texte/train.txt', 'octets': 7504078589, 'mtime': '2026-11-01T17:25:40'}
{'chemin': '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/train-lignes.txt', 'octets': 6900585097, 'sha256': 'e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552', 'lignes': 63438199}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rm -f tools/__pycache__/dedup_lignes.cpython-313.pyc && rmdir tools/__pycache__ 2>/dev/null || true; echo 'pycache cleaned'; python3 - <<'PY'\nimport json, os\np=json.load(open('work/dedup/prouve-200Mo-lignes.json'))\nprint('200Mo me … [1184 caractères tronqués]`

  ```
pycache cleaned
200Mo memoire {'budget_mio': 64.0, 'rss_max_mio': 45.7, 'ru_maxrss_mio': 49.3, 'marge_mio': 18.3, 'capacite_slots': 2097152, 'octets_table': 16777216, 'entrees_max': 1677721, 'plancher_mio': 48.0}
200Mo table {'slots_utilises': 1015997, 'charge_finale': 0.4845, 'entrees_max': 1677721} durees {'duree_s': 4.1, 'duree_passe_s': 3.5, 'duree_verification_s': 0.6, 'debit_mio_s': 53.7, 'debit_total_mio_s': 46.1}
200Mo lignes {'lues': 1741349, 'gardees': 1477432, 'ecartees': 263917, 'vides_lues': 461435, 'vides_gardees': 461435, 'non_vides_lues': 1279914, 'non_vides_gardees': 1015997, 'non_vides_ecartees': 263917, 'plus_longue_ligne_octets': 5457} taux {'pct_lignes_ecartees': 15.156, 'pct_lignes_ecartees_hors_vides': 20.62, 'pct_octets_ecartes': 3.527, 'pct_octets_vides': 0.231, 'pct_sortie': 96.473} integrite True
autotest controle {'chemin': '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/autotest-lignes/controle.txt', 'lignes': 12, 'octets': 162, 'vides': 4} attendu {'defaut_octets': 121, 'normalise_octets': 87} ok True cas 16
autotest shas 3de1a6d949aa169ed891b1e1968c7e6fcc701e3982e2a1ecc33741858e6df89b a8667c3cabf663a6278062c7a5fd154df434da4b9ff27a0a7828f1d
… [1084 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Adding conservative ru_maxrss margin fields, then regenerating artifacts

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('tools/dedup_lignes.py')\ns=p.read_text()\ns=s.replace('''        \"pct_sortie\": round(100 * octets_gardes / octets_lus, 3) if octets_lus else 0.0,\n    }''','''        \"pct_lignes … [808 caractères tronqués]`

  ```
OK
433:        "pct_lignes_gardees": round(100 * lignes_gardees / lignes_lues, 3)
435:        "pct_lignes_vides": round(100 * lignes_vides / lignes_lues, 3)
450:        "marge_ru_maxrss_mio": round((budget_o - rss_ru) / MIB, 1),
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rm -rf work/dedup/autotest-lignes && python3 tools/dedup_lignes.py --autotest > work/dedup/autotest-lignes.out 2> work/dedup/autotest-lignes.err; echo \"AUTOTEST_RC=$?\"; /usr/bin/time -v python3 tools/dedup_lignes.py --entree work/d … [925 caractères tronqués]`

  ```
AUTOTEST_RC=0
PROOF_RC=0
{
 "entree_octets": 200000000,
 "sortie_octets": 192946503,
 "lignes_lues": 1741349,
 "lignes_gardees": 1477432,
 "lignes_ecartees": 263917,
 "pct_lignes_ecartees": 15.156,
 "pct_octets_ecartes": 3.527,
 "duree_s": 5.0,
 "duree_passe_s": 4.1,
 "rss_max_mio": 45.6,
 "sha256": "1ec785b6dab27396cfedbb802883a0777fa11e092b9d1f2e964fcfa4df320222"
}
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:05.03
	Maximum resident set size (kbytes): 50688
autotest True 16 / 16
proof memoire {'rss_max_mio': 45.6, 'ru_maxrss_mio': 49.5, 'marge_mio': 18.4, 'marge_ru_maxrss_mio': 14.5, 'budget_mio': 64.0}
proof taux {'pct_lignes_ecartees': 15.156, 'pct_lignes_ecartees_hors_vides': 20.62, 'pct_octets_ecartes': 3.527, 'pct_octets_vides': 0.231, 'pct_lignes_gardees': 84.844, 'pct_lignes_vides': 26.499, 'pct_sortie': 96.473}
proof durees {'duree_s': 5.0, 'duree_passe_s': 4.1, 'duree_verification_s': 0.9, 'debit_mio_s': 46.9, 'debit_total_mio_s': 38.4}
  ```

### 🤖 Assistant

⏵ Regenerating the 7.50 GB manifest with the final tool

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -v python3 tools/dedup_lignes.py --entree data/corpus_wiki_fr_texte/train.txt --sortie work/dedup/train-lignes.txt --memoire-mo 2048 --json reports/dedup-lignes-7.5go.json --verifier > work/dedup/train-lignes.out 2> wor … [229 caractères tronqués]`

  ```
RC=0
{
 "entree_octets": 7504078589,
 "sortie_octets": 6900585097,
 "lignes_lues": 88114432,
 "lignes_gardees": 63438199,
 "lignes_ecartees": 24676233,
 "pct_lignes_ecartees": 28.005,
 "pct_octets_ecartes": 8.042,
 "duree_s": 182.4,
 "duree_passe_s": 161.1,
 "rss_max_mio": 1053.8,
 "sha256": "e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552"
}
	User time (seconds): 169.97
	System time (seconds): 8.51
	Elapsed (wall clock) time (h:mm:ss or m:ss): 3:02.49
	Maximum resident set size (kbytes): 1078684
	Exit status: 0
  ```

### 🤖 Assistant

⏵ Regenerating the idempotence proof on the final output

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -v python3 tools/dedup_lignes.py --entree work/dedup/train-lignes.txt --sortie /dev/null --memoire-mo 2048 --json work/dedup/idempotence-train-lignes.json > work/dedup/idempotence-train-lignes.out 2> work/dedup/idempote … [879 caractères tronqués]`

  ```
RC=0
{
 "entree_octets": 6900585097,
 "sortie_octets": 6900585097,
 "lignes_lues": 63438199,
 "lignes_gardees": 63438199,
 "lignes_ecartees": 0,
 "pct_lignes_ecartees": 0.0,
 "pct_octets_ecartes": 0.0,
 "duree_s": 118.5,
 "duree_passe_s": 118.5,
 "rss_max_mio": 1053.8,
 "sha256": "e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552"
}
	User time (seconds): 113.77
	System time (seconds): 4.79
	Elapsed (wall clock) time (h:mm:ss or m:ss): 1:58.58
	Maximum resident set size (kbytes): 1078652
	Exit status: 0
main memoire {'rss_max_mio': 1053.8, 'ru_maxrss_mio': 1053.4, 'marge_mio': 994.2, 'marge_ru_maxrss_mio': 994.6}
main durees {'duree_s': 182.4, 'duree_passe_s': 161.1, 'duree_verification_s': 21.3, 'debit_mio_s': 44.4, 'debit_total_mio_s': 39.2}
main taux {'pct_lignes_ecartees': 28.005, 'pct_lignes_ecartees_hors_vides': 37.919, 'pct_octets_ecartes': 8.042, 'pct_octets_vides': 0.307, 'pct_lignes_gardees': 71.995, 'pct_lignes_vides': 26.146, 'pct_sortie': 91.958}
idem 0 e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552 6900585097 63438199 1053.8 1053.4 118.5
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum work/dedup/train-lignes.txt && stat -c 'octets=%s mtime=%y' work/dedup/train-lignes.txt && wc -l work/dedup/train-lignes.txt && sha256sum data/corpus_wiki_fr_texte/train.txt && stat -c 'octets=%s mtime=%y' data/corpus_wiki_ … [222 caractères tronqués]`

  ```
e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552  work/dedup/train-lignes.txt
octets=6900585097 mtime=2026-11-18 12:20:47.051258247 -0500
63438199 work/dedup/train-lignes.txt
[still running after 60000ms; moved to background job bash-776]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

### 🤖 Assistant

⏵ Writing `reports/rapport-dedup-lignes.md` with figures, controls, and caveats

- **write** `{"content": "# N — dédoublonner 7,50 Go par ligne : 24,7 M lignes retirées, 603 Mo (8,04 %), 1 054 Mio de RSS\n\n> **Ligne de roadmap** : N (le palier 1, « la donnée d'abord ») · **Date** : 2026-11-18 ·\n> **Verdict** : [`tools/dedup_lignes.py`](../tools/dedup_lignes.py) passe les **7 504 078 589\n> … [24514 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 👤 Utilisateur

background job bash-776 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sha256sum work/dedup/train-lignes.txt && stat -c 'octets=%s mtime=%y' work/dedup/train-lignes.txt && wc -l work/dedup/train-lignes.txt && sha256sum data/corpus_wiki_fr_texte/train.txt && stat -c 'octets=%s mtime=%y' data/corpus_wiki_fr_texte/train.txt && echo '--- git ---' && git status --porcelain | head -20 && echo '--- pycache dedup ---' && find tools -maxdepth 2 -name '*dedup_lignes*' -print) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-776"}`

  ```
27277e320d7781e0dc8957a449fff386a7d1fa712838bba42f8a1e728dd0924b  data/corpus_wiki_fr_texte/train.txt
octets=7504078589 mtime=2026-11-01 17:25:40.769701171 -0500
--- git ---
 M journal/README.md
 M journal/sessions/6e7ba93b-7eb8-400a-8457-6f6a8fe67f54/digest.md
 M journal/sessions/6e7ba93b-7eb8-400a-8457-6f6a8fe67f54/rapport.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/digest.md
 M journal/sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/rapport.md
?? reports/banc-generation-r2.json
?? reports/banc-grammaticalite-r2.json
?? reports/dedup-lignes-7.5go.json
?? tools/dedup_lignes.py
--- pycache dedup ---
tools/__pycache__/dedup_lignes.cpython-313.pyc
tools/dedup_lignes.py
[status: completed, exit code: 0]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md", "new_string": "Les 8,042 % se lisent : **8,279 %** du diagnostic **− 0,307 point** de lignes vides\npréservées **+ 0,070 point** de variantes d'espaces de fin **= 8,042 %**. La sortie fait\n**6 900 585 0 … [405 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md", "new_string": "  distincte soit confondue avec une autre et écartée à tort. C'est négligeable, mais ce n'est\n  pas zéro ; une table à 128 bits doublerait la mémoire **à capacité égale** (2 GiB pour\n  2 … [418 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md", "new_string": "- **Budget et capacité.** La table est exacte **tant qu'elle n'est pas pleine** : à 2 048 Mio\n  elle peut accueillir 107 374 182 entrées (40,4 M utilisées, **62,4 %** de marge). Avec un\n … [392 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Validating report links and final artifact consistency

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib\np=pathlib.Path('reports/rapport-dedup-lignes.md')\ns=p.read_text()\nlinks=re.findall(r'\\[[^\\]]*\\]\\(([^)]+)\\)', s)\nprint('liens', len(links))\nfor l in links:\n    if l.startswith(('http://' … [649 caractères tronqués]`

  ```
liens 16
OK   ../tools/dedup_lignes.py
OK   rapport-dedup-blocs.md
OK   rapport-dedup-blocs.md
OK   ../work/dedup/autotest-lignes/autotest.json
OK   ../work/dedup/prouve-200Mo-lignes.json
OK   ../work/dedup/budget-impossible-8.json
OK   rapport-dedup-blocs.md
OK   ../tools/dedup_lignes.py
OK   dedup-lignes-7.5go.json
OK   ../work/dedup/train-lignes.txt
OK   ../work/dedup/prouve-200Mo-lignes.json
OK   ../work/dedup/autotest-lignes/autotest.json
OK   ../work/dedup/idempotence-train-lignes.json
OK   ../work/dedup/normalise-train-lignes.json
OK   ../work/dedup/budget-impossible-8.json
OK   ../work/dedup/diagnostic_lignes_exact.py
lignes 375 mots 3992
--- json validity + key figures ---
ok 6900585097 63438199 e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552
24676233 603493492 28.005 8.042
1053.4 994.6
  ```

### 🤖 Assistant

⏵ Final lint/CLI checks and workspace cleanup

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (command -v ruff >/dev/null && ruff check tools/dedup_lignes.py || echo 'ruff absent') ; python3 tools/dedup_lignes.py --help | head -25; rm -f tools/__pycache__/dedup_lignes.cpython-313.pyc; rmdir tools/__pycache__ 2>/dev/null || tr … [234 caractères tronqués]`

  ```
ruff absent
usage: dedup_lignes.py [-h] [--entree ENTREE] [--sortie SORTIE]
                       [--memoire-mo MEMOIRE_MO] [--normaliser] [--json JSON]
                       [--verifier] [--autotest] [--repertoire REPERTOIRE]

Dédoublonner un fichier texte ligne à ligne, en flux, à mémoire bornée.

options:
  -h, --help            show this help message and exit
  --entree ENTREE       fichier texte à dédupliquer (lecture seule)
  --sortie SORTIE       fichier de sortie (lignes gardées, telles quelles)
  --memoire-mo MEMOIRE_MO
                        plafond mémoire en Mio (défaut 2048)
  --normaliser          minuscules ASCII + espaces compactés (en plus du
                        retrait des espaces de fin)
  --json JSON           manifeste JSON de la passe
  --verifier            relire la sortie et vérifier octets, lignes et sha256
  --autotest            contrôle négatif reproductible
  --repertoire REPERTOIRE
                        répertoire de l'autotest
--- status ---
?? reports/dedup-lignes-7.5go.json
?? reports/rapport-dedup-lignes.md
?? tools/dedup_lignes.py
--- pycache ---
tools/dedup_lignes.py
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md", "new_string": "Le temps de la passe principale est **CPU** : 169,97 s d'utilisateur et 8,51 s de système\npour 182,49 s d'horloge (97,8 %) ; le hachage et le sondage dominent, pas les entrées-sorties.\nL … [844 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md", "new_string": "Le diagnostic exact du [rapport blocs](rapport-dedup-blocs.md) § 4.3 comptait **toutes** les\nlignes, y compris les vides, et ne retirait **pas** les espaces de fin. Il hachait sur\n**40 b … [477 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md</path>
<type>file</type>
<content>
1: # N — dédoublonner 7,50 Go par ligne : 24,7 M lignes retirées, 603 Mo (8,04 %), 1 054 Mio de RSS
2: 
3: > **Ligne de roadmap** : N (le palier 1, « la donnée d'abord ») · **Date** : 2026-11-18 ·
4: > **Verdict** : [`tools/dedup_lignes.py`](../tools/dedup_lignes.py) passe les **7 504 078 589
5: > octets** de `data/corpus_wiki_fr_texte/train.txt` en **161,1 s de passe** (+ **21,3 s** de
6: > relecture de vérification, soit **3 min 02 s** au total), avec **1 053,8 Mio de VmRSS** et
7: > **1 053,4 Mio de `ru_maxrss`** pour un budget de **2 048 Mio** (marge **994 Mio**), et écrit
8: > **6 900 585 097 octets** (6,43 Gio), sha256
9: > `e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552`. Il écarte
10: > **24 676 233 lignes** (**28,005 %**) et **603 493 492 octets** (**8,042 %**), en préservant
11: > **toutes** les **23 037 969 lignes vides**. La table est **exacte** (pas de filtre de Bloom,
12: > pas d'éviction) : la deuxième passe sur la sortie n'écarte **aucune** ligne et rend le
13: > **même sha256**. Comparé aux **53,98 % / 8,28 %** du [rapport blocs
… [7248 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md", "limit": 130, "offset": 121}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md</path>
<type>file</type>
<content>
121: le traitement par ligne ne crée donc aucun gros objet, et la mémoire est dominée par la table.
122: La relecture de vérification a relu **6 900 585 097 octets** et **63 438 199 lignes**, avec
123: le **même sha256** que l'écriture. `wc -l` et `stat` confirment ces deux valeurs de
124: l'extérieur, et `sha256sum` confirme le sha256.
125: 
126: Les 8,042 % se lisent : **8,279 %** du diagnostic **− 0,307 point** de lignes vides
127: préservées **+ 0,070 point** de variantes d'espaces de fin **= 8,042 %**. La sortie fait
128: **6 900 585 097 o = 91,958 %** de l'entrée ; les 23,04 M de lignes vides pèsent **0,307 %**
129: des octets.
130: 
131: **Preuve sur 200 Mo.** Budget **64 Mio** — plus serré que les 256 Mio du rapport blocs — pour
132: une entrée de 200 Mo : `ru_maxrss` **49,5 Mio**, soit **14,5 Mio sous le plafond**, avec une
133: table de 16 Mio et 1,016 M de lignes uniques. C'est la preuve demandée « sur 200 Mo au moins »,
134: et elle est plus contraignante que la passe principale (charge 48,45 % contre 30,10 %).
135: 
136: **Idempotence.** Une deuxième
… [7865 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md", "limit": 140, "offset": 251}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md</path>
<type>file</type>
<content>
251: - **Collisions 64 bits.** La table ne stocke que 64 bits par ligne. Avec 40 400 230 lignes
252:   uniques, on attend **4,4 × 10⁻⁵ collision**, soit **0,004 %** de chance qu'une ligne
253:   distincte soit confondue avec une autre et écartée à tort. C'est négligeable, mais ce n'est
254:   pas zéro ; une table à 128 bits doublerait la mémoire **à capacité égale** (2 GiB pour
255:   2^27 cases), donc diviserait par deux le nombre d'entrées à budget constant, et une
256:   collision n'est **pas détectable** avec cette structure.
257: - **Lignes quasi identiques non détectées.** Par défaut, seule la fin de ligne est
258:   normalisée. Une ligne qui change **un mot, une ponctuation, une casse, un accent ou un
259:   espace interne** est gardée. Les 150 540 variantes d'espaces de fin montrent que la
260:   normalisation compte : `--normaliser` en trouve 164 547 de plus, et il ne va toujours pas
261:   jusqu'aux accents (`É` ≠ `é`), aux variantes Unicode ni aux textes reflués. Une ligne
262:   répétée mais **coupée différemment** (phrase à cheval sur deux lignes) es
… [8412 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md", "new_string": "> **toutes** les **23 037 969 lignes vides**. La table est **exacte** (pas de filtre de Bloom,\n> pas d'éviction ; seules les collisions 64 bits du § 5 restent) : la deuxième passe sur la\ … [287 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md", "new_string": "Le corpus a **40 400 230** lignes non vides distinctes (mesuré). À 8 octets par case, une\ntable ouverte à charge 0,30 tient dans **1 GiB** : c'est le choix fait à 2 048 Mio. « Exacte »\nv … [1218 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-lignes.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Final end-to-end validation of artifacts after the last rerun

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/dedup_lignes.py --autotest > work/dedup/autotest-lignes.out 2> work/dedup/autotest-lignes.err; echo \"AUTOTEST_RC=$?\"; python3 -c \"import json;a=json.load(open('work/dedup/autotest-lignes/autotest.json'));print('autot … [723 caractères tronqués]`

  ```
AUTOTEST_RC=0
autotest ok True cas 16 / 16
e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552  work/dedup/train-lignes.txt
63438199 work/dedup/train-lignes.txt
6900585097
--- all json ---
reports/dedup-lignes-7.5go.json OK ok
work/dedup/prouve-200Mo-lignes.json OK ok
work/dedup/idempotence-train-lignes.json OK ok
work/dedup/normalise-train-lignes.json OK ok
work/dedup/budget-impossible-8.json OK erreur
work/dedup/autotest-lignes/autotest.json OK True
--- pycache ---
tools/dedup_lignes.py
  ```

- **send_message** `{"agent_id": "d67a9bb1-090e-4f69-baf2-a831c00aa275", "message": "Dédup par ligne terminé et mesuré sur les 7,50 Go. Aucun fichier de data/ touché, aucun commit, aucun appel API.\n\n## Chiffres (passe principale)\n- Entrée : data/corpus_wiki_fr_texte/train.txt, 7 504 078 589 o, sha256 27277e320d7781e … [3377 caractères tronqués]`

  ```
message delivered to agent d67a9bb1-090e-4f69-baf2-a831c00aa275
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('reports/rapport-dedup-lignes.md')\ns=p.read_text()\ns=s.replace('''Le diagnostic exact du [rapport blocs](rapport-dedup-blocs.md) § 4.3 comptait **toutes** les\nlignes, y compris le … [2132 caractères tronqués]`

  ```
edits ok
links 16 missing []
lignes 383 mots 4120
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '88,96p;198,208p;248,258p;278,290p' reports/rapport-dedup-lignes.md", "description": "Inspect edited passages"}`

  ```
le budget, ou `--test-plafond-mo` (hameçon masqué) pour prouver que le garde-fou sait
échouer. Un budget inférieur à **56 Mio** (plancher 48 + table minimale 8) est refusé au
départ : `ERREUR budget_memoire_impossible` (code 3).

`ru_maxrss` est reporté à part (`ru_maxrss_mio`) : sous Linux, il est **hérité** à travers
fork/exec, donc un enfant lancé depuis un parent gros (l'autotest) lit le pic du parent.
C'est pourquoi le chien de garde utilise le VmRSS ; pour les passes lancées depuis un shell,
les deux mesures coïncident à 0,4 Mio près (1 053,4 Mio ici, confirmé par
`/usr/bin/time -v`).
- **Chien de garde** : plafond de test de 1 Mio → `ERREUR memoire_depassee`, **code 3**
  (autotest). Un garde-fou qui ne sait pas échouer ne garde rien.

## 4. Comparaison aux 53,98 % / 8,28 % du rapport blocs

Le diagnostic exact du [rapport blocs](rapport-dedup-blocs.md) § 4.3 comptait **toutes** les
lignes, y compris les vides, et ne retirait **pas** les espaces de fin. Il hachait sur
**40 bits** (≈ 3 700 collisions attendues sur 88,1 M de lignes, négligeables devant
150 540) ; ici le hachage est sur 64 bits (≈ 4,4 × 10⁻⁵ collision attendue), donc l'écart
n'est **pas** un artefact de collisi
… [1976 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dédoublonnage par ligne terminé, mesuré et contrôlé

## Chiffres (passe principale)

- **Entrée** : `data/corpus_wiki_fr_texte/train.txt`, **7 504 078 589 o**, sha256 `27277e32…`
- **Sortie** : `work/dedup/train-lignes.txt`, **6 900 585 097 o** (6,43 Gio), **63 438 199 lignes**, sha256 **`e3112a842ed6d97a15b2da0dd20d5f3d6ea81477356d0741fce175d7f3858552`**
- **Écarté** : **24 676 233 lignes (28,005 %** ; 37,919 % des non-vides) et **603 493 492 o (8,042 %)**
- **Préservé** : **23 037 969 lignes vides** (26,146 % des lignes, 0,307 % des octets)
- **Temps** : **161,1 s de passe** (2 min 41 s) + 21,3 s de relecture `--verifier` = **182,4 s** ; **44,4 Mio/s** de passe ; CPU 169,97 s user + 8,51 s sys.
- **RSS** : `ru_maxrss` **1 053,4 Mio**, VmRSS 1 053,8, pour budget **2 048 Mio** (marge **994,6 Mio**). Table exacte de 1 GiB (2^27 cases, 40 400 230 entrées, charge 30,10 %).
- **Preuve 200 Mo** : budget **64 Mio**, `ru_maxrss` **49,5 Mio** (marge 14,5), table 16 Mio, 263 917 lignes / 7 053 497 o écartés (15,156 % / 3,527 %), sortie 192 946 503 o.
- **Idempotence** : 2ᵉ passe sur la sortie → **0 ligne écartée**, même sha256, mêmes 6 900 585 097 o ; 118,5 s, même RSS.

## Comparaison aux 53,98 % / 8,28 %

Réconciliation exacte avec le rapport blocs :
- `47 563 661 − 23 037 968 (vides préservées) + 150 540 (espaces de fin) = 24 676 233 lignes`
- `621 277 675 − 23 037 968 + 5 253 785 = 603 493 492 o`

Soit **54,150 % / 8,349 %** à politique de lignes vides égale, et **28,005 % / 8,042 %** en pratique (les vides expliquent −0,307 point ; le `rstrip` ajoute +0,070 point). La variante `--normaliser` retire 164 547 lignes / 6 528 572 o de plus, mais coûte 260,8 s.

## Autotest : 16/16

(a) ligne unique gardée (6 non-vides, sortie exacte) ;
(b) copie exacte écartée (1) ;
(c) copie avec espaces de fin écartée par défaut (1), première occurrence écrite **telle quelle** avec ses espaces ;
(d) ligne différente gardée ;
(e) 4 lignes vides préservées (3 `\n` + 1 `   \n`), `vides_lues = 4` ;
(f) deux passes → **même sha256** `3de1a6d9…`, sorties identiques.

Extras : `--normaliser` (4 écartées vs 2, sha stable), `budget_memoire_impossible` rc 3, `capacite_depassee` rc 3, `memoire_depassee` rc 3, `--verifier` OK.

## Chemins

- `tools/dedup_lignes.py`
- `reports/rapport-dedup-lignes.md`
- `reports/dedup-lignes-7.5go.json`
- `work/dedup/train-lignes.txt` (corpus v2)
- `work/dedup/prouve-200Mo-lignes.json`
- `work/dedup/autotest-lignes/autotest.json`
- `work/dedup/idempotence-train-lignes.json`

## Limites et suite

Collisions 64 bits : ≈ 4,4 × 10⁻⁵ attendue (0,0044 % de risque). Les lignes quasi identiques (un mot, une casse Unicode, un refluage) ne sont pas détectées ; l'ordre garde la première occurrence ; les vides sont tous préservés ; la table exacte s'arrête proprement à 107 374 182 entrées à 2 048 Mio. La prose de 80 o et + reste ≈ 2,6 % du fichier.

Le corpus v2 est prêt dans `work/` (pas dans `data/`) : taille, lignes et sha256 ci-dessus. Prochaine étape recommandée : compter les jetons v1/v2 et mesurer une petite perplexité/qualité avant de s'en servir. Aucun fichier de `data/` modifié, aucun commit, aucun appel API, `en-cours`/`roadmap`/`AGENTS` non touchés.

