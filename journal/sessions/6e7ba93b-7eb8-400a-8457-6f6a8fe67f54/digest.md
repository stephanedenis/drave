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

