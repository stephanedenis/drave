# Session DSH — relecture

- identifiant : `cbf7ca71-5b38-428e-9f19-298be1720918`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-18 10:17:36
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (Drave, en français). Machine dédiée (40 threads, 125 Go RAM). NE TOUCHE PAS à `data/` (lecture seule).

CONTEXTE : l'inventaire `reports/rapport-donnees-inventaire.md` a montré que `data/corpus_wiki_fr_texte/train.txt` fait **7,50 Go** et pourrait fermer l'écart du palier 1, MAIS l'outil actuel `tools/corpus_propre.py` tient tous les shingles en mémoire (~80 Go par Go de texte) → ~600 Go pour 7,5 Go : impossible. Il faut une passe **par blocs** à budget RAM borné.

TÂCHE : écrire `tools/dedup_blocs.py` — un dédoublonnage de texte par blocs, à mémoire bornée, et le prouver.

Exigences :
1. CLI : `python3 tools/dedup_blocs.py --entree F --sortie G [--bloc-mo 64] [--memoire-mo 2048] [--shingle 96] [--seuil 0.8] [--json R]`. Découpe l'entrée en blocs (par exemple par paragraphes/lignes, avec recouvrement), normalise (minuscules, espaces), calcule des shingles hachés (32 ou 64 bits), et **dédoublonne** : un bloc dont ≥ seuil de ses shingles a déjà été vu est écarté.
2. **Budget mémoire explicite** : la mémoire ne doit pas dépasser `--memoire-mo` (mesure-la avec `resource.getrusage(RUSAGE_SELF).ru_maxrss` et prouve-le sur au moins 200 Mo de texte d'entrée ; si le budget est dépassé, sors en erreur nommée).
3. **Contrôle négatif obligatoire** : construis un petit fichier de test avec (a) un texte unique, (b) sa copie exacte, (c) sa copie à 10 % modifiée, (d) un texte différent ; prouve que (b) est écarté, (c) est écarté ou non selon le seuil (dis-le), (d) est gardé — et que le résultat est **stable** (deux passes identiques).
4. **Mesure** : passe-le sur `data/corpus_wiki_fr_texte/train.txt` (7,50 Go, lecture seule) avec `--bloc-mo 64 --memoire-mo 2048 --json reports/dedup-blocs-7.5go.json` ; mesure le temps, la mémoire max, le nombre de blocs gardés/écartés, les octets écrits (dans `work/dedup/`, pas dans `data/`).
5. Écris `reports/rapport-dedup-blocs.md` : le dispositif, les chiffres (temps, RSS max, gardés/écartés, octets), les contrôles, ce qui pourrait le rendre faux (shingles 32 bits = collisions, seuil, blocs qui coupent les doublons à cheval), et la comparaison avec les 2,0 % mesurés par l'inventaire.

CONTRAINTES : n'écris que `tools/dedup_blocs.py`, `reports/rapport-dedup-blocs.md`, `reports/dedup-blocs-7.5go.json` et `work/dedup/` ; ne touche pas à en-cours/roadmap/AGENTS ; ne committe pas ; pas d'appel API.

Rends : les chiffres (temps, RSS, % écarté), le résultat des 4 cas de contrôle, et les chemins.
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

⏵ Exploring the workspace and inventory report before writing the tool

I'll start by examining the workspace, the inventory report, and the existing tool to understand the conventions.

- **bash** `{"command": "pwd && ls -la && echo \"---\" && ls -la tools/ | head -40 && echo \"---\" && ls -la reports/ | head -20", "description": "List workspace structure"}`

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
drwxr-xr-x. 1 stephane stephane   220 18 nov 10:17 .git
drwxr-xr-x. 1 stephane stephane    22 16 nov 03:51 .github
-rw-r--r--. 1 stephane stephane   653 15 nov 22:25 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane  1052 18 nov 08:36 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-------. 1 stephane stephane  1272 16 nov 01:44 pyproject.toml
drwxr-xr-x. 1 stephan
… [5536 caractères tronqués]
  ```

- **bash** `{"command": "ls -la data/ 2>/dev/null | head -20; echo \"---\"; ls -la data/corpus_wiki_fr_texte/ 2>/dev/null; echo \"---\"; df -h . data/ 2>/dev/null", "description": "Inspect data corpus size and disk"}`

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
… [770 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the inventory report and the existing dedup tool

- **bash** `{"command": "ls -la reports/rapport-donnees-inventaire.md 2>/dev/null; echo \"---\"; wc -l reports/rapport-donnees-inventaire.md 2>/dev/null; echo \"---\"; ls -la tools/corpus_propre.py; echo \"---\"; wc -l tools/corpus_propre.py", "description": "Check inventory report and corpus tool"}`

  ```
-rw-------. 1 stephane stephane 21004 18 nov 09:36 reports/rapport-donnees-inventaire.md
---
296 reports/rapport-donnees-inventaire.md
---
-rw-------. 1 stephane stephane 8990 31 oct 22:53 tools/corpus_propre.py
---
221 tools/corpus_propre.py
  ```

- **bash** `{"command": "head -c 2000 data/corpus_wiki_fr_texte/train.txt | od -c | head -40; echo \"===\"; head -c 1500 data/corpus_wiki_fr_texte/train.txt", "description": "Inspect beginning of train corpus"}`

  ```
0000000   A   n   t   o   i   n   e       M   e   i   l   l   e   t  \n
0000020   A   n   t   o   i   n   e       M   e   i   l   l   e   t   ,
0000040       n 303 251       l   e     303 240       M   o   u   l   i
0000060   n   s       (   A   l   l   i   e   r   )       e   t       m
0000100   o   r   t       l   e     303 240       C   h 303 242   t   e
0000120   a   u   m   e   i   l   l   a   n   t       (   C   h   e   r
0000140   )   ,       e   s   t       u   n       p   h   i   l   o   l
0000160   o   g   u   e       f   r   a   n 303 247   a   i   s   ,    
0000200   l   e       p   r   i   n   c   i   p   a   l       l   i   n
0000220   g   u   i   s   t   e       f   r   a   n 303 247   a   i   s
0000240       d   e   s       p   r   e   m   i 303 250   r   e   s    
0000260   d 303 251   c   e   n   n   i   e   s       d   u       .  \n
0000300  \n   B   i   o   g   r   a   p   h   i   e  \n   E   n   f   a
0000320   n   c   e       e   t       f   o   r   m   a   t   i   o   n
0000340  \n   P   a   u   l       J   u   l   e   s       A   n   t   o
0000360   i   n   e       M   e   i   l   l   e   t       e   s   t    
0000400   d   '   o   r   i   g   i   n   e     
… [3167 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md</path>
<type>file</type>
<content>
1: # L'inventaire des données pour le palier 1 : 1,02 Go épinglés sur 3–6 Go demandés
2: 
3: > **Ligne de roadmap** : N (le palier 1, « la donnée d'abord ») · **Date** : 2026-11-18 ·
4: > **Verdict** : le dépôt porte **135,5 Go** de données apparentes (4 428 fichiers), dont **120,1 Go
5: > de Wikipédia en 10 langues**. Le français vraiment exploitable se réduit à **7,5 Go** — et le
6: > corpus épinglé (**1,017 Go**) en est un **sous-ensemble de contenu**. Il manque **1,98 Go** pour
7: > 3 Go et **4,98 Go** pour 6 Go, mais ces octets sont **déjà sur le disque**
8: > (`data/corpus_wiki_fr_texte/`, 7,50 Go) : l'écart de **volume** est fermable sans aucune collecte ;
9: > l'écart de **diversité** (≈ 0,1 Go de français hors Wikipédia) ne l'est pas.
10: 
11: Aucun fichier de `data/` n'a été modifié, aucun téléchargement n'a été fait. Les seules écritures
12: sont ce rapport et un fichier temporaire `/tmp/titres_wikibig.txt`.
13: 
14: ## 1. Ce qui est mesuré, et comment
15: 
16: Mesures du **2026-11-18**, en lecture seule : `du -sb` et `find -type f` pour les octe
… [20658 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading corpus_propre.py to reuse its naming and shingling conventions

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_propre.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_propre.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """corpus_propre.py — un corpus sans répétition, et un split qui ne fuit pas.
3: 
4: POURQUOI. N2.d a mesuré que **32,8 %** des fenêtres du protocole de validation
5: apparaissent **verbatim** dans l'entraînement : le corpus empile des passages qui se
6: recopient (127 blocs contigus, jusqu'à 1,8 Ko). Toute PPL mesurée sur ce jeu est donc
7: une PPL de mémoire, pas de généralisation — et 2,7078 comme 2,6998 sont mesurées dessus.
8: 
9: CE QUE FAIT L'OUTIL.
10: 
11: 1. **Déduplication par shingles.** On roule un hachage de Rabin-Karp sur des fenêtres de
12:    `--fenetre` octets (96 par défaut). La première occurrence d'un shingle est gardée ;
13:    toute position couverte par un shingle déjà vu est retirée. Conséquence : après
14:    nettoyage, **aucune fenêtre de 128 octets ne se répète** dans le texte — donc aucune
15:    fenêtre de validation ne peut apparaître dans l'entraînement.
16: 2. **Split par chunks contigus.** Le texte nettoyé est découpé en chunks de `--chunk`
17:    octets ; un chunk sur `--val` va en validation, le suivant en t
… [8860 caractères tronqués]
  ```

- **bash** `{"command": "python3 -VV; echo \"---\"; python3 -c \"import numpy, sys; print('numpy', numpy.__version__)\"; echo \"---\"; python3 -c \"import xxhash; print('xxhash', xxhash.VERSION)\" 2>&1 | tail -1; echo \"---\"; nproc; free -g | head -2; echo \"---\"; lsblk -d -o NAME,ROTA,SIZE 2>/dev/null; echo  … [153 caractères tronqués]`

  ```
Python 3.13.16 (main, Oct 16 2026, 19:23:15) [GCC]
---
numpy 2.5.3
---
ModuleNotFoundError: No module named 'xxhash'
---
40
               total        used        free      shared  buff/cache   available
Mem:             125          42          22          17          80          83
---
NAME    ROTA   SIZE
sda        1  10,9T
nvme1n1    0 238,5G
nvme3n1    0 238,5G
nvme2n1    0 238,5G
nvme4n1    0 238,5G
nvme0n1    0 931,5G
---
total 240
drwxr-xr-x. 1 stephane stephane  2858 18 nov 09:07 .
drwxr-xr-x. 1 stephane stephane   774 16 nov 03:32 ..
-rw-r--r--. 1 stephane stephane  1040 15 nov 03:23 atomes_cohortes.py
-rwxr-xr-x. 1 stephane stephane  2133  2 nov 16:46 attente_portes.sh
drwxr-xr-x. 1 stephane stephane   562 17 nov 20:47 banc-performance
drwxr-xr-x. 1 stephane stephane   362 16 nov 03:27 chantier
drwxr-xr-x. 1 stephane stephane   168  7 nov 15:06 corpus-commun
-rw-r--r--. 1 stephane stephane  6879  1 nov 12:49 corpus-wiki-langues.log
-rw-r--r--. 1 stephane stephane  1004  1 nov 11:14 corpus-wiki.log
-rw-r--r--. 1 stephane stephane  3985  1 nov 12:49 corpus-wiki-reste.log
drwxr-xr-x. 1 stephane stephane     8  1 nov 18:44 dr
-rw-r--r--. 1 stephane stephane   479  2 nov 20:
… [492 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -iE \"dedup|propre|corpus\" | head -20; echo \"---\"; sed -n 1,60p reports/rapport-corpus-epingle.md 2>/dev/null", "description": "List related reports and style sample"}`

  ```
b102bis-corpus-jw.json
corpus-commun.json
corpus-epingle.json
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
---
# N — le corpus d'entraînement est épinglé

> **Ligne de roadmap** : N (le palier 1, « la donnée d'abord ») · **Date** : 2026-11-18 ·
> **Verdict** : ✅ le corpus de `data/wiki_mix/propre` est **épinglé** — sha256 du train, du val et
> de leurs canaux, tailles, lignes, dates, empreinte du manifeste (`fae5bb73…`). Sans cette
> épingle, chaque perplexité est une rumeur : l'alerte du 16/11 a montré que le `ppl_val` 2,40
> annoncé **ne se reproduit pas** avec le `val.txt` actuel (17,3 à 22,6 selon le morceau lu).
>
> **Dispositif** : [`tools/epingle_corpus.py`](../tools/epingle_corpus.py) · le manifeste
> [`corpus-epingle.json`](corpus-epingle.json) · vérification `--verifie` (recalcule 
… [2236 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Benchmarking hash strategies to pick a fast, deterministic one

- **bash** `{"command": "mkdir -p /tmp/bench && cd /tmp/bench && head -c 200000000 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/corpus_wiki_fr_texte/train.txt > slice.bin 2>/dev/null; ls -l slice.bin; md5sum slice.bin", "description": "Create 200MB slice for benchmarks"}`

  ```
-rw-r--r--. 1 stephane stephane 200000000 18 nov 10:24 slice.bin
e88370532e63d1e0ed8bd07ef47edf5b  slice.bin
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys\ns = set()\nfor i in range(1, 300001):\n    s.add((i*0x9E3779B97F4A7C15) & ((1<<64)-1))\nn=len(s)\nprint(\"n\", n, \"set bytes/entry\", sys.getsizeof(s)/n, \"int bytes\", sys.getsizeof(next(iter(s))))\ns32=set()\nfor i in range(1,300001):\n    s32.add((i*0x … [191 caractères tronqués]`

  ```
n 300000 set bytes/entry 27.962746666666668 int bytes 36
32 set bytes/entry 27.962746666666668 int32 bytes 32
  ```

- **bash** `{"command": "cd /tmp/bench && python3 - <<'EOF'\nimport time, hashlib, zlib, os\ndata = open('slice.bin','rb').read()\nprint(len(data))\nw, pas = 96, 96\nN = (len(data)-w)//pas\n\ndef bench(name, fn):\n    t=time.perf_counter(); h=fn(); dt=time.perf_counter()-t\n    print(f\"{name}: {dt:.2f}s  {N/dt … [633 caractères tronqués]`

  ```
200000000
hash(): 0.71s  2.95 M win/s  h=2188157392698351360
blake2b8: 2.02s  1.03 M win/s  h=10482647051311516644
crc32: 0.88s  2.38 M win/s  h=961420647
  ```

### 🤖 Assistant

⏵ Checking git state, /usr/bin/time, and micro-benchmarking the inner loop

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain | head -20; echo \"--- ignorés ---\"; git check-ignore -v work/dedup/train.txt reports/dedup-blocs-7.5go.json tools/dedup_blocs.py 2>&1; echo \"--- time ---\"; ls -l /usr/bin/time 2>&1; /usr/bin/time -v true 2> … [75 caractères tronqués]`

  ```
M drave-core/src/placement.rs
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/digest.md
 M journal/sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/rapport.md
?? journal/sessions/9f4f7b6d-c5aa-4269-b785-a0f444424470/
?? journal/sessions/cbf7ca71-5b38-428e-9f19-298be1720918/
?? reports/rapport-a2.6-tete-q8.md
--- ignorés ---
.gitignore:27:work/	work/dedup/train.txt
--- time ---
-rwxr-xr-x. 1 root root 27320 16 avr  2026 /usr/bin/time
	Command being timed: "true"
	User time (seconds): 0.00
	System time (seconds): 0.00
  ```

- **bash** `{"command": "cd /tmp/bench && python3 - <<'EOF'\nimport time, hashlib, zlib, struct\ndata = open('slice.bin','rb').read()[:50_000_000]\nw, pas = 96, 48\npositions = list(range(0, len(data)-w, pas))\nprint(\"positions\", len(positions))\nb = hashlib.blake2b\ndef bench(name, fn):\n    t=time.perf_coun … [773 caractères tronqués]`

  ```
positions 1041665
bytes+int: 1.06s  0.98 M/s h=15847550082717994196
bytes+struct: 0.96s  1.08 M/s h=15847550082717994196
memoryview+int: 1.06s  0.98 M/s h=15847550082717994196
  ```

### 🤖 Assistant

Now I'll write the tool. Let me first check the report conventions for JSON manifests and a couple of house details.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -40 reports/corpus-wiki-fr-texte.json; echo \"===\"; grep -rn \"ERREUR \" tools/*.py | head -10; echo \"===\"; grep -rln \"ru_maxrss\" tools/ | head", "description": "Check JSON manifest style and named-error conventions"}`

  ```
{
 "date": "2026-11-01",
 "ligne": "Données",
 "langue": "fr",
 "nature": "corpus Wikipédia fr (texte intégral)",
 "source": {
  "dump": "/home/stephane/Data13TB/stephane/data/wikipedia/dumps/fr/frwiki-latest-pages-articles-multistream.xml.bz2",
  "octets": 7129511779
 },
 "methode": {
  "debaliseur": "regex : commentaires, refs, tableaux, modèles (30 itérations), fichiers/catégories, liens → libellé, titres de sections, listes",
  "filtre": "ns 0, sans redirection, texte >= 300 caractères",
  "deduplication": "articles (BLAKE2b) + tronçons (train), première occurrence gardée",
  "split": "hash salé (graine 1) de page_id : 5% val, 5% test"
 },
 "dump": "/home/stephane/Data13TB/stephane/data/wikipedia/dumps/fr/frwiki-latest-pages-articles-multistream.xml.bz2",
 "dump_octets": 7129511779,
 "articles_lus": 5968207,
 "articles_gardes": 2388219,
 "articles_rediriges": 1827807,
 "articles_hors_ns": 1385362,
 "articles_courts": 366649,
 "articles_doublons": 170,
 "caracteres_gardes": 8025059777,
 "troncons": 2755825,
 "troncons_doublons": 783,
 "octets": {
  "train": 7504078589,
  "val": 419555119,
  "test": 415302543
 },
 "articles": {
  "train": 2149330,
  "val": 119866,
  "test": 11902
… [815 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Writing tools/dedup_blocs.py (core, budget model, autotest)

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", "content": "#!/usr/bin/env python3\n\"\"\"dedup_blocs.py — dédoublonner du texte par blocs, à mémoire bornée.\n\nPOURQUOI. `tools/corpus_propre.py` garde **tous** les shingles en mémoire (≈ 80 Go par Go\nde texte,  … [36285 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", "old_string": "    def classe(fraction: float) -> str:\n        for borne, nom in ((0.0, \"0\"), (0.01, \"0-1\"), (0.05, \"1-5\"), (0.2, \"5-20\"),\n                           (0.5, \"20-50\"), (0.8, \"50-80\"), (0 … [472 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", "new_string": "            calc += ((len(norm) - w) // pas + 1) if len(norm) >= w else 0\n            liste: list[int] = []\n            ech_bloc = vus_bloc = 0\n            tot_c_bloc = vus_c_bloc = 0\n            … [2116 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", "new_string": "    rapport = squelette(a)\n    t_debut = time.perf_counter()\n    try:\n        valide(a)\n        entree = pathlib.Path(a.entree)\n        if entree.is_file():\n            st = entree.stat()\n     … [1464 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py has been updated successfully.
  ```

### 🤖 Assistant

⏵ Running the first smoke test and the autotest

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/dedup_blocs.py --help | head -30 && echo \"=== petit essai ===\" && mkdir -p work/dedup && head -c 3000000 data/corpus_wiki_fr_texte/train.txt > work/dedup/essai-3mo.txt && time python3 tools/dedup_blocs.py --entree wor … [184 caractères tronqués]`

  ```
usage: dedup_blocs.py [-h] [--entree ENTREE] [--sortie SORTIE]
                      [--bloc-mo BLOC_MO] [--memoire-mo MEMOIRE_MO]
                      [--shingle SHINGLE] [--seuil SEUIL] [--json JSON]
                      [--pas PAS] [--hash-bits {32,64}] [--graine GRAINE]
                      [--recouvrement-mo RECOUVREMENT_MO] [--autotest]
                      [--repertoire REPERTOIRE]

Dédoublonner un fichier texte par blocs, à mémoire bornée.

options:
  -h, --help            show this help message and exit
  --entree ENTREE       fichier texte à dédupliquer (lecture seule)
  --sortie SORTIE       fichier de sortie (les blocs gardés)
  --bloc-mo BLOC_MO     taille d'un bloc en Mio (défaut 64)
  --memoire-mo MEMOIRE_MO
                        budget mémoire en Mio (défaut 2048)
  --shingle SHINGLE     fenêtre en octets (défaut 96)
  --seuil SEUIL         fraction de shingles déjà vus au-delà de laquelle un
                        bloc est écarté
  --json JSON           manifeste JSON de la passe
  --pas PAS             pas entre deux shingles (défaut 48)
  --hash-bits {32,64}   largeur des hachages (défaut 64)
  --graine GRAINE       décale les hachages (échantillon)
  --re
… [808 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/dedup_blocs.py --autotest 2>&1 | tail -80", "description": "Run the autotest (negative control)"}`

  ```
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", line 787, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", line 743, in main
    ok, resume = lance_autotest(pathlib.Path(a.repertoire))
                 ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", line 598, in lance_autotest
    C2 = disperse(A, 0.10, 44, VOCABULAIRE)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", line 567, in disperse
    mots = list(MOT.finditer(texte))
                ~~~~~~~~~~~~^^^^^^^
TypeError: cannot use a string pattern on a bytes-like object
[stderr]

real	0m0,164s
user	0m0,152s
sys	0m0,014s
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", "new_string": "def disperse(texte: bytes, fraction: float, graine: int, vocabulaire: list[str]) -> bytes:\n    \"\"\"Remplace `fraction` des mots par d'autres, dispersés : la copie « 10 % modifiée ».\"\"\"\n    s = … [1113 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/dedup_blocs.py --autotest 2>&1 | tail -90", "description": "Re-run the autotest"}`

  ```
},
  {
   "nom": "c_fraction_entre_080_et_095",
   "ok": false,
   "detail": {
    "fractions": [
     0.54,
     0.2085,
     0.4162,
     0.0889
    ]
   }
  },
  {
   "nom": "sortie_095_egale_a_plus_c_plus_d",
   "ok": false,
   "detail": {
    "octets": 851968
   }
  },
  {
   "nom": "copie_10pct_disperse_gardee",
   "ok": true,
   "detail": {
    "blocs": [
     true,
     true,
     true,
     true
    ],
    "fractions": [
     0.0007,
     0.0051,
     0.0104,
     0.0052
    ]
   }
  },
  {
   "nom": "hash32_memes_decisions",
   "ok": true,
   "detail": {
    "hash32": [
     true,
     true,
     true,
     true,
     true,
     false,
     false,
     false,
     true,
     true,
     true,
     true,
     true,
     true,
     true,
     true
    ],
    "identique": true
   }
  },
  {
   "nom": "budget_impossible_nomme",
   "ok": true,
   "detail": {
    "rc": 3,
    "erreur": {
     "nom": "budget_memoire_impossible",
     "message": "budget 64 Mio < plancher 344 Mio (4 × (bloc 64.0 + 2 × recouvrement 1.00) + 32 + 48 Mio) + 32 Mio pour le jeu de shingles"
    },
    "stderr": [
     "ERREUR budget_memoire_impossible: budget 64 Mio < plancher 344 Mio (4 × (bloc 64.0 + 2
… [356 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/dedup_blocs.py --autotest 2>/dev/null | head -70", "description": "Inspect first autotest cases"}`

  ```
{
 "ok": false,
 "controle": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/controle/controle.txt",
 "textes": {
  "A": 262144,
  "B": 262144,
  "C": 262144,
  "C2": 262292,
  "D": 262144,
  "paragraphe_octets": 2048,
  "paragraphes": 128
 },
 "fractions": {
  "b": [
   0.0,
   0.9632,
   0.9626,
   0.9618
  ],
  "c": [
   0.54,
   0.2085,
   0.4162,
   0.0889
  ],
  "d": [
   0.0,
   0.0,
   0.0,
   0.0
  ],
  "c_disperse": [
   0.0007,
   0.0051,
   0.0104,
   0.0052
  ]
 },
 "cas": [
  {
   "nom": "a_texte_unique_garde",
   "ok": true,
   "detail": {
    "blocs": [
     true,
     true,
     true,
     true
    ],
    "rc": 0
   }
  },
  {
   "nom": "b_copie_exacte_ecartee",
   "ok": false,
   "detail": {
    "blocs": [
     true,
     false,
     false,
     false
    ],
    "fractions": [
     0.0,
     0.9632,
     0.9626,
     0.9618
    ]
   }
  },
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nr = json.load(open('work/dedup/controle/seuil080.json'))\nfor b in r['journal_blocs']:\n    print(b['bloc'], b['debut'], b['fin'], b['octets'], b['shingles'], b['echantillonnes'], b['fraction'], b['fra … [137 caractères tronqués]`

  ```
1 0 65536 65536 1361 1361 0.0 0.0 True
2 65536 131072 65536 1386 1386 0.0 0.0 True
3 131072 196608 65536 1389 1389 0.0 0.0 True
4 196608 262144 65536 1386 1386 0.0 0.0 True
5 262144 327680 65536 1387 1387 0.0 0.0 True
6 327680 393216 65536 1386 1386 0.9632 1.0 False
7 393216 458752 65536 1389 1389 0.9626 1.0 False
8 458752 524288 65536 1386 1386 0.9618 1.0 False
9 524288 589824 65536 1387 1387 0.54 0.5606 True
10 589824 655360 65536 1386 1386 0.2085 0.2166 True
11 655360 720896 65536 1391 1391 0.4162 0.4324 True
12 720896 786432 65536 1384 1384 0.0889 0.0924 True
13 786432 851968 65536 1375 1375 0.0 0.0 True
14 851968 917504 65536 1383 1383 0.0 0.0 True
15 917504 983040 65536 1381 1381 0.0 0.0 True
16 983040 1048576 65536 1344 1344 0.0 0.0 True
{'bloc_mo': 0.0625, 'memoire_mo': 512.0, 'shingle_octets': 96, 'pas': 48, 'seuil': 0.8, 'hash_bits': 64, 'graine': 0, 'recouvrement_mo': None}
{'budget_mio': 512.0, 'plancher_mio': 80.3, 'bloc_mio': 0.06, 'recouvrement_octets': 1310, 'recouvrement_origine': '2 % du bloc, plafonné à 1 Mio', 'cout_entree': {'table_octets_entree': 104.9, 'entier_octets': 36, 'cout_entree_octets': 193.3}, 'shingles_attendus': 21846, 'capacite_entrees': 2342018, 
… [107 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport hashlib, struct, re\nBLANC = re.compile(rb\"\\s+\")\ndef normalise(b): return BLANC.sub(b\" \", b.lower())\ndef h(w): return struct.unpack(\"<Q\", hashlib.blake2b(w, digest_size=8).digest())[0]\nd = open('wo … [530 caractères tronqués]`

  ```
taille 1048576
A==B True
norm egales True 64101
shingles 1334 1334 communs 1334
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"liste\\|vus.update\\|deb_n\\|fin_n\\|n_coeur\\|brut_coeur\" tools/dedup_blocs.py | sed -n 1,60p", "description": "Inspect the hashing/insertion code"}`

  ```
83:DIVERS_BLOC_MO = 32.0     # tableau de hachages + listes + tampons de lecture
348:            brut_coeur = bytes(tampon[p1:p2])
350:            n_coeur = normalise(brut_coeur)
352:            norm = n_prefixe + n_coeur + n_suffixe
353:            deb_n = len(n_prefixe)
354:            fin_n = deb_n + len(n_coeur)
357:            liste: list[int] = []
371:                    if deb_n <= pos < fin_n:
377:                        liste.append(hh)
378:            vus.update(liste)
381:            fraction_coeur = vus_c_bloc / tot_c_bloc if tot_c_bloc else 0.0
385:                f_sortie.write(brut_coeur)
386:                sha.update(brut_coeur)
387:                lignes_gardees += brut_coeur.count(b"\n")
388:                octets_gardes += len(brut_coeur)
391:                octets_ecartes += len(brut_coeur)
410:            dist_coeur[classe(fraction_coeur)] += 1
416:                    "octets": len(brut_coeur),
421:                    "fraction_coeur": round(fraction_coeur, 4),
530:    "variable nombre valeur ensemble graphe arbre liste table colonne ligne "
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", "offset": 300, "limit": 90}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py</path>
<type>file</type>
<content>
300:     ech_et = vus_et = tot_c = vus_c = 0
301:     calc = 0
302:     rss_max = 0
303:     sha = hashlib.sha256()
304:     f_entree = open(entree, "rb")
305:     f_sortie = open(sortie, "wb")
306: 
307:     tampon = bytearray()
308:     base = 0
309: 
310:     def remplir(jusqua: int) -> None:
311:         nonlocal tampon
312:         while base + len(tampon) < jusqua:
313:             morceau = f_entree.read(min(jusqua - (base + len(tampon)), 8 * MIB))
314:             if not morceau:
315:                 return
316:             tampon += morceau
317: 
318:     def classe(fraction: float) -> str:
319:         if fraction <= 0.0:
320:             return "0"
321:         for borne, nom in ((0.01, "0-1"), (0.05, "1-5"), (0.2, "5-20"),
322:                            (0.5, "20-50"), (0.8, "50-80"), (0.95, "80-95")):
323:             if fraction < borne:
324:                 return nom
325:         return "95-100"
326: 
327:     debut = 0
328:     dernier_affichage = 0.0
329:     try:
330:         while debut < taille:
331:             blocs += 1
332:             cible_fin = 
… [2654 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cp tools/dedup_blocs.py /tmp/dbg_dedup.py && python3 - <<'EOF'\nimport re\np = '/tmp/dbg_dedup.py'\ns = open(p).read()\ns = s.replace('''            vus.update(liste)\n\n            fraction = vus_bloc / ech_bloc if ech_bloc else 0.0 … [665 caractères tronqués]`

  ```
DBG bloc=1 debut=0 fin=65536 deb_n=0 fin_n=64101 len_norm=65411 tot_c=1336 liste=1336 vus=1336 norm_coeur_debut=b'beau mourir feu arriv\xc3\xa9e rouge chaque savoir voir bleu vent '
DBG bloc=2 debut=65536 fin=131072 deb_n=1212 fin_n=65293 len_norm=66603 tot_c=1335 liste=1335 vus=2671 norm_coeur_debut=b'enfant for\xc3\xaat recevoir enseigner m\xc3\xa8re vivre ces p\xc3\xa8re temps'
DBG bloc=3 debut=131072 fin=196608 deb_n=1260 fin_n=65430 len_norm=66740 tot_c=1337 liste=1337 vus=4008 norm_coeur_debut=b'\xc3\x89toile \xc3\xa9toile partout voir certain rue nouveau vous jour p'
DBG bloc=4 debut=196608 fin=262144 deb_n=1271 fin_n=65278 len_norm=66588 tot_c=1333 liste=1333 vus=5341 norm_coeur_debut=b'r\xc3\xa9cit de arriv\xc3\xa9e route devoir pays femme roi le \xc5\x93uvre ces'
DBG bloc=5 debut=262144 fin=327680 deb_n=1216 fin_n=65317 len_norm=66627 tot_c=1335 liste=1335 vus=6676 norm_coeur_debut=b'beau mourir feu arriv\xc3\xa9e rouge chaque savoir voir bleu vent '
DBG bloc=6 debut=327680 fin=393216 deb_n=1212 fin_n=65293 len_norm=66603 tot_c=1335 liste=1335 vus=6676 norm_coeur_debut=b'enfant for\xc3\xaat recevoir enseigner m\xc3\xa8re vivre ces p\xc3\xa8re temps'
  ```

### 🤖 Assistant

⏵ Investigating a subtle phase-alignment flaw in the fixed-stride grid

The control revealed a real flaw: a copy at an offset not aligned with the stride matches nothing. Let me quantify this on the real corpus before fixing the design.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport hashlib, struct, time, re\nd = open('/tmp/bench/slice.bin','rb').read()   # 200 MB du vrai train\nprint(\"octets\", len(d))\nBLANC = re.compile(rb\"[ \\t\\r\\f\\v]+\")\ndef h(w): return struct.unpack(\"<Q\", … [982 caractères tronqués]`

  ```
octets 200000000
grille pas=96 : 2083333 shingles, 27942 vus (1.34 %) en 2.7s
grille pas=48 : 4166665 shingles, 64493 vus (1.55 %) en 5.4s
lignes        : 1741348 shingles, 48527 vus (2.79 %) en 2.6s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport hashlib, struct, time, re\nd = open('/tmp/bench/slice.bin','rb').read()[:50_000_000]   # 50 MB\nprint(\"octets\", len(d))\nW = 96\ndef h(w): return struct.unpack(\"<Q\", hashlib.blake2b(w, digest_size=8).dig … [751 caractères tronqués]`

  ```
octets 50000000
ancrage mots  : 7596803 shingles, 23735 vus (0.31 %) en 12.5s
stride 1 (/8) : 6249988 shingles, 5080 vus (0.08 %) en 19.5s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport hashlib, struct, time, re\nd = open('/tmp/bench/slice.bin','rb').read()[:20_000_000]\nW = 96\ndef h(w): return struct.unpack(\"<Q\", hashlib.blake2b(w, digest_size=8).digest())[0]\n\ndef mesure(nom, gen, gar … [904 caractères tronqués]`

  ```
tous, hash 1/16: 1249191 éch., 3035 vus (0.24 %) en 21.8s
grille 96      : 208333 éch., 17 vus (0.01 %) en 0.3s
grille 48      : 416665 éch., 57 vus (0.01 %) en 0.5s
lignes         : 145317 éch., 462 vus (0.32 %) en 0.2s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport hashlib, struct, time, re\nd = open('/tmp/bench/slice.bin','rb').read()   # 200 MB\nW = 96\nHBLANC = re.compile(rb\"[ \\t\\r\\f\\v]+\")\ndef normalise(b): return HBLANC.sub(b\" \", b.lower())\ndef h(w): retu … [1090 caractères tronqués]`

  ```
octets 200000000 normalisés 200000000
lignes 1741349
débuts de ligne seuls: 1279914 ancres (0.006/octet), 34632 vus (2.71 %), 2.5s
lignes + pas 192: 1905640 ancres (0.010/octet), 49546 vus (2.60 %), 3.6s
lignes + pas 96: 2829425 ancres (0.014/octet), 70820 vus (2.50 %), 5.1s
lignes + pas 48: 4830662 ancres (0.024/octet), 116448 vus (2.41 %), 8.3s
  ```

### 🤖 Assistant

The fixed-stride grid is fundamentally biased (0.01 % vs 0.24 % at 20 MB). I'll switch to content-defined anchors (line starts + stride within a line), which is shift-invariant.

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"dedup_blocs.py — dédoublonner du texte par blocs, à mémoire bornée.\n\nPOURQUOI. `tools/corpus_propre.py` garde **tous** les shingles en mémoire (≈ 80 Go par Go\nde texte, cf. `reports/rapport-n2-corpus-1go.md`) : dédupliquer les 7,50 Go de\n`data/corpus_wi … [37900 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", "new_string": "                    \"lignes\": brut_coeur.count(b\"\\n\"),\n                    \"shingles\": tot_bloc,\n                    \"vus\": vus_bloc,", "old_string": "                    \"lignes\": brut_ … [195 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/dedup_blocs.py --autotest 2>&1 | python3 -c \"\nimport json,sys\nr = json.load(sys.stdin)\nprint('OK =', r['ok'])\nfor c in r['cas']:\n    print(('  ✅' if c['ok'] else '  ❌'), c['nom'], json.dumps(c['detail'], ensu … [160 caractères tronqués]`

  ```
OK = False
  ❌ a_texte_unique_garde {"blocs": [true, true, true, true], "rc": 1}
  ❌ b_copie_exacte_ecartee {"blocs": [true, false, false, false], "fractions": [0.0, 0.9632, 0.9626, 0.9618]}
  ❌ b_fraction_1 {"fractions": [0.0, 0.9632, 0.9626, 0.9618]}
  ❌ c_copie_10pct_ecartee_a_080 {"blocs": [true, true, true, true], "fractions": [0.54, 0.2085, 0.4162, 0.0889]}
  ✅ d_texte_different_garde {"blocs": [true, true, true, true], "fractions": [0.0, 0.0, 0.0, 0.0]}
  ❌ sortie_egale_a_plus_d {"octets": 0, "attendu": 524288}
  ✅ budget_respecte_controle {"rss_max_mio": 30.6, "budget_mio": 512.0}
  ✅ stable_sha256 {"sha1": "882942f7297ccd93e41747eb0792ed412b12735983969a3e873d12842cab5ebd", "sha2": "882942f7297ccd93e41747eb0792ed412b12735983969a3e873d12842cab5ebd
  ✅ stable_blocs {"identiques": true}
  ✅ stable_octets {"octets": 851968}
  ✅ c_garde_a_095 {"blocs": [true, true, true, true], "fractions": [0.54, 0.2085, 0.4162, 0.0889]}
  ❌ c_fraction_entre_080_et_095 {"fractions": [0.54, 0.2085, 0.4162, 0.0889]}
  ❌ sortie_095_egale_a_plus_c_plus_d {"octets": 0}
  ✅ copie_decalee_ecartee {"blocs": [], "fractions": []}
  ✅ copie_10pct_disperse_gardee {"blocs": [true, true, true, true], "fracti
… [742 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rm -rf work/dedup/controle && python3 tools/dedup_blocs.py --entree work/dedup/controle/controle.txt --sortie /tmp/x.txt --bloc-mo 0.0625 --seuil 0.8 --memoire-mo 512 2>&1 | tail -20", "description": "Run tool directly to see the tra … [8 caractères tronqués]`

  ```
ERREUR entree_invalide: /home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/controle/controle.txt n'est pas un fichier lisible
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/dedup_blocs.py --autotest >/dev/null 2>&1; ls -la work/dedup/controle/ | head; echo \"=== run direct ===\"; python3 tools/dedup_blocs.py --entree work/dedup/controle/controle.txt --sortie /tmp/x.txt --bloc-mo 0.0625 --s … [103 caractères tronqués]`

  ```
total 2320
drwxr-xr-x. 1 stephane stephane     374 18 nov 10:45 .
drwxr-xr-x. 1 stephane stephane     108 18 nov 10:45 ..
-rw-r--r--. 1 stephane stephane    2756 18 nov 10:45 autotest.json
-rw-r--r--. 1 stephane stephane    1570 18 nov 10:45 budget_impossible.json
-rw-r--r--. 1 stephane stephane  786453 18 nov 10:45 controle_decale.txt
-rw-r--r--. 1 stephane stephane  524587 18 nov 10:45 controle_disperse.txt
-rw-r--r--. 1 stephane stephane 1048576 18 nov 10:45 controle.txt
-rw-r--r--. 1 stephane stephane       0 18 nov 10:45 garde-080-bis.txt
-rw-r--r--. 1 stephane stephane       0 18 nov 10:45 garde-080.txt
=== run direct ===
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", line 802, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", line 773, in main
    execute(a, rapport)
    ~~~~~~~^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", line 344, in execute
    remplir(besoin)
    ~~~~~~~^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", line 322, in remplir
  
… [161 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", "new_string": "    def remplir(jusqua: int) -> None:\n        nonlocal tampon\n        while base + len(tampon) < jusqua:", "old_string": "    def remplir(jusqua: int) -> None:\n        while base + len(tampon) < j … [8 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rm -rf work/dedup/controle && time python3 tools/dedup_blocs.py --autotest 2>&1 | python3 -c \"\nimport json,sys\nr = json.load(sys.stdin)\nprint('OK =', r['ok'])\nfor c in r['cas']:\n    print(('  OK ' if c['ok'] else '  KO '), c['n … [190 caractères tronqués]`

  ```
OK = True
  OK  a_texte_unique_garde {"blocs": [true, true, true, true], "rc": 0}
  OK  b_copie_exacte_ecartee {"blocs": [false, false, false, false], "fractions": [1.0, 1.0, 1.0, 1.0]}
  OK  b_fraction_1 {"fractions": [1.0, 1.0, 1.0, 1.0]}
  OK  c_copie_10pct_ecartee_a_080 {"blocs": [false, false, false, false], "fractions": [0.9021, 0.9016, 0.9004, 0.9006]}
  OK  d_texte_different_garde {"blocs": [true, true, true, true], "fractions": [0.0, 0.0, 0.0, 0.0]}
  OK  sortie_egale_a_plus_d {"octets": 524288, "attendu": 524288}
  OK  budget_respecte_controle {"rss_max_mio": 30.9, "budget_mio": 512.0}
  OK  stable_sha256 {"sha1": "1a5c01ef8c713c541c0a2ad6f50e2aa4ff4d7ce858a9e4d51e65033f4a402244", "sha2": "1a5c01ef8c713c541c0a2ad6f50e2aa4ff4d7ce858a9e4d51e65033f4a402244"}
  OK  stable_blocs {"identiques": true}
  OK  stable_octets {"octets": 524288}
  OK  c_garde_a_095 {"blocs": [true, true, true, true], "fractions": [0.9021, 0.9016, 0.9004, 0.9006]}
  OK  c_fraction_entre_080_et_095 {"fractions": [0.9021, 0.9016, 0.9004, 0.9006]}
  OK  sortie_095_egale_a_plus_c_plus_d {"octets": 786432}
  OK  copie_decalee_ecartee {"blocs": [false, false, false, false], "fractions": [0.9992, 1.0, 1.0, 1.
… [858 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport sys, resource, time\nfor n in (10_000, 20_000, 100_000, 1_000_000, 10_000_000):\n    s = set()\n    for i in range(n):\n        s.add((i * 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF)\n    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024\ … [218 caractères tronqués]`

  ```
n=     10000 sizeof/n=  52.5  int=28  RSS=   11.6 Mio  RSS/n=1219.4
n=     20000 sizeof/n= 104.9  int=28  RSS=   14.4 Mio  RSS/n=757.1
n=    100000 sizeof/n=  41.9  int=28  RSS=   22.0 Mio  RSS/n=230.2
n=   1000000 sizeof/n=  33.6  int=28  RSS=   95.4 Mio  RSS/n=100.0
n=  10000000 sizeof/n=  26.8  int=28  RSS=  757.0 Mio  RSS/n= 79.4
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re\np = 'tools/dedup_blocs.py'\ns = open(p).read()\n\nold = '''def calibre(n: int = 20_000) -> dict:\n    \"\"\"Mesure le coût d'une entrée de `set` : table + entier, avec le pic de redimensionnement.\n\n    … [2188 caractères tronqués]`

  ```
97:COUT_ENTREE_OCTETS = 80.0  # octets par entrée de set (mesuré, voir cout_entree())
157:    return {"cout_entree_octets": COUT_ENTREE_OCTETS,
232:    cal = cout_entree()
235:    attendus = max(1, math.ceil(1.5 * taille / a.pas))
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rm -rf work/dedup/controle && python3 tools/dedup_blocs.py --autotest 2>&1 | python3 -c \"\nimport json,sys\nr = json.load(sys.stdin)\nprint('OK =', r['ok'])\nfor c in r['cas']:\n    print(('  OK ' if c['ok'] else '  KO '), c['nom'], … [185 caractères tronqués]`

  ```
OK = True
  OK  a_texte_unique_garde {"blocs": [true, true, true, true], "rc": 0}
  OK  b_copie_exacte_ecartee {"blocs": [false, false, false, false], "fractions": [1.0, 1.0, 1.0, 1.0]}
  OK  b_fraction_1 {"fractions": [1.0, 1.0, 1.0, 1.0]}
  OK  c_copie_10pct_ecartee_a_080 {"blocs": [false, false, false, false], "fractions": [0.9021, 0.9016, 0.9004, 0.9006]}
  OK  d_texte_different_garde {"blocs": [true, true, true, true], "fractions": [0.0, 0.0, 0.0, 0.0]}
  OK  sortie_egale_a_plus_d {"octets": 524288, "attendu": 524288}
  OK  budget_respecte_controle {"rss_max_mio": 30.9, "budget_mio": 512.0}
  OK  stable_sha256 {"sha1": "1a5c01ef8c713c541c0a2ad6f50e2aa4ff4d7ce858a9e4d51e65033f4a402244", "sha2": "1a5c01ef8c713c541c0a2ad6f50e2aa4ff
  OK  stable_blocs {"identiques": true}
  OK  stable_octets {"octets": 524288}
  OK  c_garde_a_095 {"blocs": [true, true, true, true], "fractions": [0.9021, 0.9016, 0.9004, 0.9006]}
  OK  c_fraction_entre_080_et_095 {"fractions": [0.9021, 0.9016, 0.9004, 0.9006]}
  OK  sortie_095_egale_a_plus_c_plus_d {"octets": 786432}
  OK  copie_decalee_ecartee {"blocs": [false, false, false, false], "fractions": [0.9992, 1.0, 1.0, 1.0]}
  OK  copie_10pct_disperse_g
… [720 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Proving the memory bound on 200 MB with a 256 MiB budget

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cp /tmp/bench/slice.bin work/dedup/slice-200Mo.txt && ls -l work/dedup/slice-200Mo.txt && /usr/bin/time -v python3 tools/dedup_blocs.py --entree work/dedup/slice-200Mo.txt --sortie work/dedup/slice-200Mo-garde.txt --bloc-mo 8 --memoi … [170 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 200000000 18 nov 10:46 work/dedup/slice-200Mo.txt
ERREUR memoire_depassee: RSS max 318 Mio > plafond 256 Mio au bloc 1
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:00.85
	Maximum resident set size (kbytes): 326064
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -c 1000000 work/dedup/slice-200Mo.txt > /tmp/petit.txt && for b in 0.25 1 8; do echo \"=== bloc $b ===\"; /usr/bin/time -v python3 tools/dedup_blocs.py --entree /tmp/petit.txt --sortie /tmp/petit-out.txt --bloc-mo $b --memoire-m … [108 caractères tronqués]`

  ```
=== bloc 0.25 ===
	Maximum resident set size (kbytes): 34088
=== bloc 1 ===
	Maximum resident set size (kbytes): 58236
=== bloc 8 ===
	Maximum resident set size (kbytes): 58244
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, tracemalloc, resource, types\nsys.path.insert(0, 'tools')\nimport dedup_blocs as D\n\na = types.SimpleNamespace(entree='/tmp/petit.txt', sortie='/tmp/petit-out2.txt', bloc_mo=1.0,\n                      … [676 caractères tronqués]`

  ```
tracemalloc pic 33.9743537902832 Mio
     0.0 Mio         1  /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py:281
     0.0 Mio         3  /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py:415
     0.0 Mio         2  /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py:304
     0.0 Mio         1  /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py:454
     0.0 Mio         1  /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py:287
     0.0 Mio         3  /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py:140
     0.0 Mio         3  <stdin>:13
     0.0 Mio         1  /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py:451
RSS 70.10546875 Mio
[stderr]
[bloc 1] 0/1 Mio, 0.0% vu, gardé, RSS 70 Mio, 7 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, time, types\nsys.path.insert(0, 'tools')\nimport dedup_blocs as D\n\n# mesure des briques\nd = open('/tmp/petit.txt','rb').read()\nprint(\"octets\", len(d), \"lignes\", d.count(b'\\n'))\nt=time.perf_cou … [948 caractères tronqués]`

  ```
octets 1000000 lignes 7506
normalise 0.061 s -> 1000000
hachage 20832 fenêtres en 0.031 s
ancres 23497 lignes 7507 en 0.005 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cp tools/dedup_blocs.py /tmp/dbg2.py && python3 - <<'EOF'\np='/tmp/dbg2.py'; s=open(p).read()\ns = s.replace(\"\"\"            brut_coeur = bytes(tampon[p1:p2])\"\"\",\"\"\"            print(f\"  RSS avant bloc: {rss_max_octets()/MIB … [841 caractères tronqués]`

  ```
RSS avant bloc: 23.7 Mio, tampon=0.95 Mio
  RSS après normalise: 57.8 Mio, norm=0.95 Mio
  RSS après hachage: 57.8 Mio, tot=23497, liste=23497
[bloc 1] 0/1 Mio, 0.0% vu, gardé, RSS 58 Mio, 0 s
{
 "entree_octets": 1000000,
 "duree_s": 0.1,
 "debit_mio_s": 9.1,
 "rss_max_mio": 57.8,
 "budget_mio": 256.0,
 "blocs": {
  "total": 1,
  "gardes": 1,
  "ecartes": 0,
  "octets_gardes": 1000000,
  "octets_ecartes": 0,
  "pct_octets_ecartes": 0.0
 },
 "shingles": {
  "shingle_octets": 96,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re, resource, time\ndef rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024\nd = open('/tmp/petit.txt','rb').read()\nprint(\"départ RSS\", round(rss(),1), \"Mio\")\nR1 = re.compile(rb\"[ \\ … [487 caractères tronqués]`

  ```
départ RSS 12.6 Mio
1+ (actuel): 60.8 ms, pic RSS 45.9 Mio (+33.3), len=1000000
2+ (proposé): 19.0 ms, pic RSS 45.9 Mio (+0.0), len=1000000
espaces simples: 146472 runs 2+: 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/dedup_blocs.py'; s=open(p).read()\ns = s.replace('HBLANC = re.compile(rb\"[ \\\\t\\\\r\\\\f\\\\v]+\")     # espaces horizontaux ; les \\\\n sont conservés',\n              'HBLANC = re.compile(rb\"[ \\\\t\ … [1621 caractères tronqués]`

  ```
86:HBLANC = re.compile(rb"[ \t\r\f\v]{2,}")   # suites de 2+ espaces ; les \n restent
132:    return HBLANC.sub(b" ", bloc.lower())
=== 1 Mo ===
 "rss_max_mio": 28.5,
	Maximum resident set size (kbytes): 29212
=== 200 Mo, budget 256 ===
[bloc 18] 136/191 Mio, 15.9% vu, gardé, RSS 121 Mio, 8 s
[bloc 19] 144/191 Mio, 7.6% vu, gardé, RSS 121 Mio, 9 s
[bloc 20] 152/191 Mio, 2.8% vu, gardé, RSS 121 Mio, 9 s
[bloc 21] 160/191 Mio, 3.7% vu, gardé, RSS 126 Mio, 10 s
[bloc 22] 168/191 Mio, 1.3% vu, gardé, RSS 127 Mio, 10 s
[bloc 23] 176/191 Mio, 0.3% vu, gardé, RSS 128 Mio, 10 s
[bloc 24] 184/191 Mio, 0.6% vu, gardé, RSS 128 Mio, 11 s
	Maximum resident set size (kbytes): 131308
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nr = json.load(open('work/dedup/prouve-200Mo.json'))\nprint(json.dumps({k: r[k] for k in ('memoire','shingles','blocs','distribution','duree_s','debit_mio_s')}, ensure_ascii=False, indent=1))\nprint(\"f … [117 caractères tronqués]`

  ```
{
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
  "rss_max_mio": 128.2,
  "marge_mio": 127.8
 },
 "shingles": {
  "shingle_octets": 96,
  "pas": 48,
  "hash_bits": 64,
  "graine": 0,
  "taux_echantillonnage": "1/8",
  "ancrage": "début de ligne + tous les --pas octets dans la ligne (positions définies par le contenu : insensibles au décalage)",
  "calcules": 4830660,
  "echantillonnes": 604152,
  "vus": 11853,
  "vus_pct": 1.962
 },
 "blocs": {
  "total": 24,
  "gardes": 24,
  "ecartes": 0,
  "octets_gardes": 200000000,
  "octets_ecartes": 0,
  "pct_octets_ecartes": 0.0
 },
 "distribution": {
  "fraction_seuil": {
   "0": 2,
   "0-1": 15,
   "1-5": 4,
   "5-20": 3,
   "20-50": 0,
   "50-80": 0,
   "80-95": 0,
   "95-100": 0
  }
 },
 "duree_s": 11.1,
 "debit_mio_s
… [212 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/dedup_blocs.py'; s=open(p).read()\n\nold = \"\"\"            fraction = vus_bloc / tot_bloc if tot_bloc else 0.0\n            garde = (tot_bloc == 0) or (fraction < seuil)\n            vus.update(liste)\"\ … [1976 caractères tronqués]`

  ```
{
 "entree_octets": 200000000,
 "duree_s": 11.0,
 "debit_mio_s": 17.3,
 "rss_max_mio": 121.0,
 "budget_mio": 256.0,
 "blocs": {
  "total": 24,
  "gardes": 24,
  "ecartes": 0,
  "octets_gardes": 200000000,
  "octets_ecartes": 0,
  "pct_octets_ecartes": 0.0
 },
 "shingles": {
  "shingle_octets": 96,
  "pas": 48,
  "hash_bits": 64,
  "graine": 0,
  "taux_echantillonnage": "1/8",
  "ancrage": "début de ligne + tous les --pas octets dans la ligne (positions définies par le contenu : insensibles au décalage)",
  "calcules": 4830660,
  "echantillonnes": 604152,
  "vus": 11853,
  "vus_pct": 1.962,
  "vus_incluant_bloc": 14206,
  "vus_incluant_bloc_pct": 2.351,
  "definition": "vus_pct = déjà présents avant le bloc (métrique de décision) ; vus_incluant_bloc_pct = y compris les répétitions internes au bloc (même définition qu'une passe unique, comparable à l'inventaire)"
 },
 "sortie": {
  ```

### 🤖 Assistant

⏵ Launching the full 7.5 GB pass in the background

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && df -h /home/stephane/Data13TB | tail -1 && /usr/bin/time -v python3 tools/dedup_blocs.py --entree data/corpus_wiki_fr_texte/train.txt --sortie work/dedup/train.txt --bloc-mo 64 --memoire-mo 2048 --json reports/dedup-blocs-7.5go.json  … [177 caractères tronqués]`

  ```
started background job bash-643
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 20 && tail -3 work/dedup/train-pass.log", "description": "Check main run progress"}`

  ```
[bloc 5] 256/7156 Mio, 3.3% vu, gardé, RSS 437 Mio, 18 s
[bloc 6] 320/7156 Mio, 1.5% vu, gardé, RSS 439 Mio, 22 s
[bloc 7] 384/7156 Mio, 1.9% vu, gardé, RSS 442 Mio, 26 s
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"diagnostic_ancrage.py — pourquoi une grille à pas fixe sous-estime la duplication.\n\nLe 2026-11-18, l'inventaire (`reports/rapport-donnees-inventaire.md` § 1) a mesuré\n2,93 % de shingles de 96 octets déjà vus sur les 7,50 Go du train, avec un pas de 96\no … [4530 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/diagnostic_ancrage.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -2 work/dedup/train-pass.log && ls -l work/dedup/train.txt 2>/dev/null", "description": "Check main run progress"}`

  ```
[bloc 14] 832/7156 Mio, 1.8% vu, gardé, RSS 504 Mio, 52 s
[bloc 15] 896/7156 Mio, 7.0% vu, gardé, RSS 506 Mio, 56 s
-rw-r--r--. 1 stephane stephane 1006630218 18 nov 10:50 work/dedup/train.txt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 60 && tail -2 work/dedup/train-pass.log", "description": "Check progress again"}`

  ```
[still running after 60000ms; moved to background job bash-646]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -2 work/dedup/train-pass.log && ls -l work/dedup/train.txt", "description": "Check main run progress"}`

  ```
[bloc 37] 2304/7156 Mio, 1.4% vu, gardé, RSS 587 Mio, 139 s
[bloc 38] 2368/7156 Mio, 2.0% vu, gardé, RSS 589 Mio, 143 s
-rw-r--r--. 1 stephane stephane 2550127754 18 nov 10:52 work/dedup/train.txt
  ```

### 👤 Utilisateur

background job bash-646 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 60 && tail -2 work/dedup/train-pass.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 90; tail -2 work/dedup/train-pass.log; ls -l work/dedup/train.txt", "description": "Wait and check progress", "timeoutMs": 120000}`

  ```
[bloc 64] 4032/7156 Mio, 2.0% vu, gardé, RSS 716 Mio, 243 s
[bloc 65] 4096/7156 Mio, 2.1% vu, gardé, RSS 718 Mio, 247 s
-rw-r--r--. 1 stephane stephane 4362060020 18 nov 10:54 work/dedup/train.txt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 120; tail -3 work/dedup/train-pass.log; ls -l work/dedup/train.txt", "description": "Wait for main run", "timeoutMs": 150000}`

  ```
[bloc 96] 6080/7156 Mio, 2.4% vu, gardé, RSS 792 Mio, 368 s
[bloc 97] 6144/7156 Mio, 2.1% vu, gardé, RSS 794 Mio, 372 s
[bloc 98] 6208/7156 Mio, 2.7% vu, gardé, RSS 796 Mio, 376 s
-rw-r--r--. 1 stephane stephane 6576645689 18 nov 10:56 work/dedup/train.txt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 100; tail -6 work/dedup/train-pass.log; echo \"---\"; ls -l work/dedup/train.txt reports/dedup-blocs-7.5go.json 2>&1", "description": "Wait for main run completion", "timeoutMs": 130000}`

  ```
Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
code=0
---
-rw-r--r--. 1 stephane stephane      26397 18 nov 10:57 reports/dedup-blocs-7.5go.json
-rw-r--r--. 1 stephane stephane 7504078589 18 nov 10:57 work/dedup/train.txt
  ```

### 👤 Utilisateur

background job bash-643 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && df -h /home/stephane/Data13TB | tail -1 && /usr/bin/time -v python3 tools/dedup_blocs.py --entree data/corpus_wiki_fr_texte/train.txt --sortie work/dedup/train.txt --bloc-mo 64 --memoire-mo 2048 --json reports/dedup-blocs-7.5go.json > work/dedup/train-pass.out 2> work/dedup/train-pass.log; echo "code=$?" >> work/dedup/train-pass.log) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

The 7.5 GB pass completed. Let me read the results.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -E \"Elapsed|Maximum resident|User time|System time|Percent of CPU\" work/dedup/train-pass.log; echo \"=== JSON ===\"; python3 - <<'EOF'\nimport json\nr = json.load(open('reports/dedup-blocs-7.5go.json'))\nfor k in ('verdict','e … [287 caractères tronqués]`

  ```
User time (seconds): 419.87
	System time (seconds): 10.91
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 7:11.33
	Maximum resident set size (kbytes): 977200
=== JSON ===
verdict = "ok"
entree = {
 "chemin": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/corpus_wiki_fr_texte/train.txt",
 "octets": 7504078589,
 "mtime": "2026-11-01T17:25:40"
}
sortie = {
 "chemin": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/train.txt",
 "octets": 7504078589,
 "sha256": "27277e320d7781e0dc8957a449fff386a7d1fa712838bba42f8a1e728dd0924b",
 "lignes": 88114432
}
parametres = {
 "bloc_mo": 64.0,
 "memoire_mo": 2048.0,
 "shingle_octets": 96,
 "pas": 48,
 "seuil": 0.8,
 "hash_bits": 64,
 "graine": 0,
 "recouvrement_mo": null
}
memoire = {
 "budget_mio": 2048.0,
 "plancher_mio": 340.0,
 "bloc_mio": 64.0,
 "recouvrement_octets": 1048576,
 "recouvrement_origine": "2 % du bloc, plafonné à 1 Mio",
 "cout_entree": {
  "cout_entree_octets": 80.0,
  "source": "mesure 2026-11-18 : set de 10 M d'entiers 64 bits = 757 Mio de ru_maxrss, soit 79,4 o/entrée"
 },
 "ancres_attendues": 234502456,
 "capacite_entrees": 22387097,
 "taux_echantillonnage": "1/32",
 "p": 0.0
… [1024 caractères tronqués]
  ```

### 🤖 Assistant

The full pass took 7:11, RSS 954 MiB under the 2048 budget, 112/112 blocks kept (0 discarded), 4.18 % of shingles seen (5.17 % including within-block). Now the comparison and granularity experiments.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 work/dedup/diagnostic_ancrage.py --octets 100000000 > work/dedup/diagnostic-ancrage.log 2>&1; echo \"code=$?\"; cat work/dedup/diagnostic-ancrage.log", "description": "Run anchoring diagnostic on 100 MB", "run_in_background": … [6 caractères tronqués]`

  ```
started background job bash-665
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && mkdir -p work/dedup/granularite && for b in 64 1 0.064 0.004; do echo \"=== bloc $b Mio ===\"; python3 tools/dedup_blocs.py --entree work/dedup/slice-200Mo.txt --sortie work/dedup/granularite/sortie-$b.txt --bloc-mo $b --memoire-mo 5 … [318 caractères tronqués]`

  ```
=== bloc 64 Mio ===
{"duree_s": 10.9, "rss_max_mio": 473.6, "blocs": {"total": 3, "gardes": 3, "ecartes": 0, "octets_gardes": 200000000, "octets_ecartes": 0, "pct_octets_ecartes": 0.0}, "shingles": {"shingle_octets": 96, "pas": 48, "hash_bits": 64, "graine": 0, "taux_echantillonnage": "1/8", "ancrage": "début de ligne + tous les --pas octets dans la ligne (positions définies par le contenu : insensibles au décalage)", "calcules": 4830660, "echantillonnes": 604152, "vus": 9584, "vus_pct": 1.586, "vus_incluant_bloc": 14206, "vus_incluant_bloc_pct": 2.351, "definition": "vus_pct = déjà présents avant le bloc (métriq
=== bloc 1 Mio ===
{"duree_s": 11.6, "rss_max_mio": 116.6, "blocs": {"total": 191, "gardes": 191, "ecartes": 0, "octets_gardes": 200000000, "octets_ecartes": 0, "pct_octets_ecartes": 0.0}, "shingles": {"shingle_octets": 96, "pas": 48, "hash_bits": 64, "graine": 0, "taux_echantillonnage": "1/4", "ancrage": "début de ligne + tous les --pas octets dans la ligne (positions définies par le contenu : insensibles au décalage)", "calcules": 4830660, "echantillonnes": 1209144, "vus": 27898, "vus_pct": 2.307, "vus_incluant_bloc": 29826, "vus_incluant_bloc_pct": 2.467, "definition": 
… [1288 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cmp -s data/corpus_wiki_fr_texte/train.txt work/dedup/train.txt && echo \"IDENTIQUE à l'octet\" || echo \"DIFFÉRENT\"; echo \"---\"; job_output_dummy=1; cat work/dedup/diagnostic-ancrage.log 2>/dev/null | tail -12", "description": "V … [44 caractères tronqués]`

  ```
IDENTIQUE à l'octet
---
fichier data/corpus_wiki_fr_texte/train.txt : 100000000 octets lus, 100000000 normalisés (1.8 s), 904348 lignes
grille 96 (inventaire)   pas= 96 shingles=   1041666 vus=     412 (0.04 %) en 1.5 s
grille 48                pas= 48 shingles=   2083332 vus=    1531 (0.07 %) en 2.9 s
ancres (outil)           pas= 48 shingles=   2436451 vus=   10971 (0.45 %) en 3.7 s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport hashlib, collections\nd = open('work/dedup/slice-200Mo.txt','rb').read()\nlignes = d.split(b'\\n')\nprint(\"lignes\", len(lignes))\nvus = set(); dup = 0; octets_dup = 0; octets = 0\nlongueurs = []\nfor l in  … [715 caractères tronqués]`

  ```
lignes 1741349
lignes déjà vues : 724258 (41.59 %)
octets dans ces lignes : 7488062 (3.74 %)
longueur médiane des lignes dupliquées 0.0 moyenne 9.3 max 2990
lignes < 20 o : 752244
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport hashlib\nd = open('work/dedup/slice-200Mo.txt','rb').read()\nlignes = d.split(b'\\n')\nvus = set()\nbuckets = [(0,1,\"vides\"), (1,20,\"1-19 o\"), (20,80,\"20-79 o\"), (80,10**9,\"80 o et +\")]\nstats = {nom … [1055 caractères tronqués]`

  ```
catégorie      lignes      dupl.  % lignes  octets dupl.  % octets
vides          461435     461434    100.0%        461434     0.23%
1-19 o         290809     201021     69.1%       1972881     0.99%
20-79 o        453824      51527     11.4%       1545074     0.77%
80 o et +      535281      10276      1.9%       3508673     1.75%
total octets 200000001

lignes dupliquées de 80 o et + : 10276 (1.9 % des lignes longues), 3508673 octets = 1.75 % du fichier
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat work/dedup/diagnostic-ancrage.log; echo \"--- job ---\"; ps aux | grep -c \"[d]iagnostic_ancrage\"", "description": "Check diagnostic results"}`

  ```
fichier data/corpus_wiki_fr_texte/train.txt : 100000000 octets lus, 100000000 normalisés (1.8 s), 904348 lignes
grille 96 (inventaire)   pas= 96 shingles=   1041666 vus=     412 (0.04 %) en 1.5 s
grille 48                pas= 48 shingles=   2083332 vus=    1531 (0.07 %) en 2.9 s
ancres (outil)           pas= 48 shingles=   2436451 vus=   10971 (0.45 %) en 3.7 s
--- job ---
2
  ```

- **job_output** `{"job_id": "bash-665", "wait": true, "timeout_ms": 180000}`

  ```
code=0
fichier data/corpus_wiki_fr_texte/train.txt : 100000000 octets lus, 100000000 normalisés (1.8 s), 904348 lignes
grille 96 (inventaire)   pas= 96 shingles=   1041666 vus=     412 (0.04 %) en 1.5 s
grille 48                pas= 48 shingles=   2083332 vus=    1531 (0.07 %) en 2.9 s
ancres (outil)           pas= 48 shingles=   2436451 vus=   10971 (0.45 %) en 3.7 s
toutes, hash 1/16        pas=  1 shingles=   6252573 vus=   38933 (0.62 %) en 120.9 s

facteur de sous-estimation de la grille fixe (pas 96) : 16×
[status: completed, exit code: 0]
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"diagnostic_lignes.py — où est la duplication : lignes courtes ou prose ?\n\nLe dédoublonnage par blocs de 64 Mio n'écarte **aucun** bloc des 7,50 Go, alors que\n4 à 5 % des shingles sont déjà vus. Pour comprendre, ce script mesure la duplication\n**ligne à  … [3731 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/diagnostic_lignes.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"diagnostic_lignes.py — où est la duplication : lignes courtes ou prose ?\n\nLe dédoublonnage par blocs de 64 Mio n'écarte **aucun** bloc des 7,50 Go, alors que\n4 à 5 % des shingles sont déjà vus. Pour comprendre, ce script mesure la duplication\n**ligne à  … [3725 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/diagnostic_lignes.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -v python3 work/dedup/diagnostic_lignes.py > work/dedup/diagnostic-lignes.log 2>&1; echo \"code=$?\"; grep -E \"Maximum resident|Elapsed\" work/dedup/diagnostic-lignes.log; cat work/dedup/diagnostic-lignes.log | head -1 … [92 caractères tronqués]`

  ```
started background job bash-671
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, glob\nprint(\"=== autotest ===\")\na = json.load(open('work/dedup/controle/autotest.json'))\nprint(\"ok\", a['ok'], \"cas\", len(a['cas']), \"ko\", sum(1 for c in a['cas'] if not c['ok']))\nprint(\"tex … [1914 caractères tronqués]`

  ```
=== autotest ===
ok True cas 18 ko 0
textes {'A': 262144, 'B': 262144, 'C': 262144, 'C2': 262443, 'D': 262144, 'paragraphe_octets': 2048, 'paragraphes': 128, 'decalage_octets': 21}
  b [1.0, 1.0, 1.0, 1.0]
  c [0.9021, 0.9016, 0.9004, 0.9006]
  d [0.0, 0.0, 0.0, 0.0]
  c_decale [0.9992, 1.0, 1.0, 1.0]
  c_disperse [0.0099, 0.0114, 0.0221, 0.0283]

=== granularité (200 Mo) ===
bloc   0.004 Mio :  50837 blocs,    74 écartés,     293157 o (0.147 %), RSS 108 Mio, 13.5 s, vus 2.45 % / 2.47 %
bloc   0.064 Mio :   2993 blocs,     0 écartés,          0 o (0.000 %), RSS 109 Mio, 12.1 s, vus 2.40 % / 2.47 %
bloc     1.0 Mio :    191 blocs,     0 écartés,          0 o (0.000 %), RSS 117 Mio, 11.6 s, vus 2.31 % / 2.47 %
bloc    64.0 Mio :      3 blocs,     0 écartés,          0 o (0.000 %), RSS 474 Mio, 10.9 s, vus 1.59 % / 2.35 %

=== 200 Mo / 256 Mio ===
rss 121.0 budget 256.0 marge 135.0
durée 11.0 débit 17.3 p 1/8
blocs {'total': 24, 'gardes': 24, 'ecartes': 0, 'octets_gardes': 200000000, 'octets_ecartes': 0, 'pct_octets_ecartes': 0.0} 
shingles {'calcules': 4830660, 'echantillonnes': 604152, 'vus': 11853, 'vus_pct': 1.962, 'vus_incluant_bloc_pct': 2.351}

=== 7.5 Go ===
rss 954.3 budget 2
… [717 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-671", "timeout_ms": 240000, "wait": true}`

  ```
code=0
	Elapsed (wall clock) time (h:mm:ss or m:ss): 2:01.50
	Maximum resident set size (kbytes): 592020
fichier data/corpus_wiki_fr_texte/train.txt : 88114432 lignes, 7504078589 octets ; échantillon 1/16 par hachage = 5584866 lignes, 489002789 octets
catégorie   lignes éch.      dupl.  % lignes  octets éch.  octets dupl.  % octets
vides                 0          0      0.0%            0             0      0.0%
1-19 o          1618911    1382770     85.4%     12133938       8633946     71.2%
20-79 o         2659312    1622661     61.0%     85881503      39409804     45.9%
80 o et +       1306643      45667      3.5%    390987348      11094099      2.8%

lignes déjà vues : 54.63 % ; octets dans ces lignes : 59137849 / 489002789 = 12.09 % (extrapolé au fichier : ≈ 90.75 Go sur 7.50 Go)
lignes de 80 o et + déjà vues : 45667 (3.5 % d'entre elles), 2.27 % des octets du fichier
	Command being timed: "python3 work/dedup/diagnostic_lignes.py"
	User time (seconds): 115.30
	System time (seconds): 6.16
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 2:01.50
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport hashlib\nf = open('data/corpus_wiki_fr_texte/train.txt','rb')\nf.seek(3_500_000_000)\nd = f.read(200_000_000)\n# aligner sur une frontière de ligne\nd = d[d.find(b'\\n')+1:]\nlignes = d.split(b'\\n')\nprint( … [954 caractères tronqués]`

  ```
lignes 2423974 octets 199999953
lignes dupliquées 1156196 (47.7 %), octets dupliqués 10155845 (5.08 %)
  vides      lignes=  619341 dupl=  619340 (100.0 %) octets=    619341 dup=   619340 (100.0 %)
  1-19 o     lignes=  569080 dupl=  398705 ( 70.1 %) octets=   6795543 dup=  4372268 ( 64.3 %)
  20-79 o    lignes=  663142 dupl=  131314 ( 19.8 %) octets=  27349272 dup=  4028645 ( 14.7 %)
  80 o et +  lignes=  572411 dupl=    6837 (  1.2 %) octets= 165235798 dup=  1135592 (  0.7 %)
  ```

### 🤖 Assistant

The sampled line diagnostic was biased (all-or-nothing by line value). Let me do an exact full-corpus line measurement with a packed sort.

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"diagnostic_lignes_exact.py — la duplication ligne à ligne, exacte, sur tout le fichier.\n\n`diagnostic_lignes.py` échantillonnait **par valeur de ligne** (un hachage tiré une fois\npar valeur) : une ligne très répétée était retenue en entier ou pas du tout, … [3475 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/work/dedup/diagnostic_lignes_exact.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -v python3 work/dedup/diagnostic_lignes_exact.py > work/dedup/diagnostic-lignes-exact.log 2>&1; echo \"code=$?\" >> work/dedup/diagnostic-lignes-exact.log", "description": "Exact full-corpus line duplication", "run_in_b … [17 caractères tronqués]`

  ```
started background job bash-674
  ```

- **job_output** `{"job_id": "bash-674", "timeout_ms": 300000, "wait": true}`

  ```
(no new output)
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat work/dedup/diagnostic-lignes-exact.log", "description": "Read exact line duplication results"}`

  ```
88114432 lignes, 7504078589 octets ; tableau 672 Mio
lignes déjà vues : 47563661 (53.98 %) ; octets : 621277675 (8.28 %)
catégorie        lignes        dupl.  % lignes         octets  octets dupl.  % octets
1-19 o         42878299     39484010     92.1%      250044292     201832862     80.7%
20-79 o        24089913      7261823     30.1%      962983444     223686767     23.2%
80 o et +      21146220       817828      3.9%     6291050853     195758046      3.1%
	Command being timed: "python3 work/dedup/diagnostic_lignes_exact.py"
	User time (seconds): 150.79
	System time (seconds): 9.59
	Percent of CPU this job got: 99%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 2:40.40
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 2963996
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 2
	Minor (reclaiming a frame) page faults: 2356664
	Voluntary context switches: 3
	Involuntary context switches: 281
	Swaps: 0
	File system inputs: 1560
	File system outputs: 8
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Pag
… [43 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='work/dedup/diagnostic_lignes_exact.py'; s=open(p).read()\ns = s.replace('    long_all = longueur\\n    for lo, hi, nom in BUCKETS:\\n        m = (long_all >= lo) & (long_all < hi)',\n              '    long_all  … [529 caractères tronqués]`

  ```
40:            bloc = f.read(a.bloc_octets)
74:    long_all = longueur.astype(np.int64) - 1   # longueur de la ligne, sans le \n
76:        m = (long_all >= lo) & (long_all < hi)
80:        od = int(longueur[m & dup].sum())
81:        oc = int(longueur[m].sum())
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -v python3 work/dedup/diagnostic_lignes_exact.py > work/dedup/diagnostic-lignes-exact.log 2>&1; echo \"code=$?\" >> work/dedup/diagnostic-lignes-exact.log", "description": "Re-run exact line diagnostic with fixed bucket … [30 caractères tronqués]`

  ```
started background job bash-679
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nr = json.load(open('reports/dedup-blocs-7.5go.json'))\nfr = [b['fraction'] for b in r['journal_blocs']]\nprint(\"blocs\", len(fr), \"max\", max(fr), \"min\", min(fr))\nfr2 = sorted(fr, reverse=True)[:6 … [293 caractères tronqués]`

  ```
blocs 112 max 0.4891 min 0.0
top fractions [0.4891, 0.243, 0.2345, 0.1904, 0.1769, 0.1581]
blocs > 20%: 3
journal tronqué False
premier bloc {'bloc': 1, 'debut': 0, 'fin': 67108652, 'octets': 67108652, 'lignes': 618130, 'shingles': 51127, 'vus': 0, 'fraction': 0.0, 'garde': True, 'rss_mio': 291.0}
dernier bloc {'bloc': 112, 'debut': 7449057452, 'fin': 7504078589, 'octets': 55021137, 'lignes': 621259, 'shingles': 43508, 'vus': 1014, 'fraction': 0.0233, 'garde': True, 'rss_mio': 954.3}
  ```

- **job_output** `{"job_id": "bash-679", "timeout_ms": 300000, "wait": true}`

  ```
(no new output)
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -12 work/dedup/diagnostic-lignes-exact.log && grep -E \"Maximum resident|Elapsed\" work/dedup/diagnostic-lignes-exact.log", "description": "Read final exact line duplication"}`

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
	Elapsed (wall clock) time (h:mm:ss or m:ss): 2:30.05
	Maximum resident set size (kbytes): 3535964
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /usr/bin/time -v python3 tools/dedup_blocs.py --entree work/dedup/slice-200Mo.txt --sortie work/dedup/slice-200Mo-garde.txt --bloc-mo 8 --memoire-mo 256 --json work/dedup/prouve-200Mo.json > work/dedup/prouve-200Mo.out 2> work/dedup/ … [582 caractères tronqués]`

  ```
code=0
	User time (seconds): 10.89
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:11.40
	Maximum resident set size (kbytes): 123676
rss 120.8 budget 256.0 marge 135.2
duree 11.3 p 1/8 blocs {'total': 24, 'gardes': 24, 'ecartes': 0, 'octets_gardes': 200000000, 'octets_ecartes': 0, 'pct_octets_ecartes': 0.0}
shingles {'calcules': 4830660, 'echantillonnes': 604152, 'vus_pct': 1.962, 'vus_incluant_bloc_pct': 2.351}
  ```

### 🤖 Assistant

All numbers are in. Now writing the report.

- **write** `{"content": "# N — dédoublonner 7,50 Go par blocs : 954 Mio de RSS, 0 bloc écarté, 5,2 % de shingles déjà vus\n\n> **Ligne de roadmap** : N (le palier 1, « la donnée d'abord ») · **Date** : 2026-11-18 ·\n> **Verdict** : [`tools/dedup_blocs.py`](../tools/dedup_blocs.py) passe les **7 504 078 589\n> o … [20524 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-blocs.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/rapport-n2-corpus-1go.md 2>&1; python3 - <<'EOF'\np='reports/rapport-dedup-blocs.md'; s=open(p).read()\ns = s.replace(\"| catégorie | lignes | déjà vues | % lignes | octets | octets dupliqués | % octets |\",\n              … [641 caractères tronqués]`

  ```
reports/rapport-n2-corpus-1go.md
100:| durée | 11,3 s | **430,7 s = 7 min 11 s** |
195:| catégorie | lignes | déjà vues | % lignes | octets | octets dupliqués | % du fichier |
297:  de cette fiche en donne le coût : 2 min 30 s et 3,4 Gio de RSS pour la version triée, ou
298:  ≈ 2 min et un `set` échantillonné pour la version en flux.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-blocs.md", "offset": 1, "limit": 120}`

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
… [6736 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-blocs.md", "limit": 110, "offset": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-blocs.md</path>
<type>file</type>
<content>
120: ### 3.1 Les quatre cas demandés — et deux de plus
121: 
122: `python3 tools/dedup_blocs.py --autotest` construit un fichier de 1 Mio (quatre textes de
123: 262 144 o, paragraphes de 2 048 o) et vérifie **18 assertions**, toutes vertes :
124: 
125: | cas | contenu | attendu | fraction vue | décision |
126: |---|---|---|---:|---|
127: | (a) | texte A, 4 blocs | gardé | 0,0 % | ✅ |
128: | (b) | B = A, copie **exacte** | écarté | **100,0 %** | ✅ |
129: | (c) | C = A à **9,4 % modifié** (paragraphes entiers remplacés) | écarté à 0,8 | **90,04–90,21 %** | ✅ |
130: | (d) | D, texte **différent** | gardé | 0,0 % | ✅ |
131: | (b′) | B précédé de 21 o : copie **décalée** | écarté | 99,92–100 % | ✅ |
132: | (c′) | A avec **10 % des mots** remplacés, dispersés | **gardé** | 0,99–2,83 % | ✅ |
133: 
134: - **(c) départage le seuil**, comme demandé : à `--seuil 0,95`, C repasse et la sortie devient
135:   A + C + D (786 432 o au lieu de 524 288 o). La fraction de C dit pourquoi : **90 %** de ses
136:   shingles sont intacts, donc 0,8 < 0,90 < 0,95.
137: - **(c′) est le cont
… [6332 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-blocs.md", "limit": 100, "offset": 229}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dedup-blocs.md</path>
<type>file</type>
<content>
229:   suivantes.
230: - **Un bloc qui coupe un doublon à cheval.** Les blocs sont coupés sur des `\n` : aucune ligne
231:   n'est coupée, et la marge de contexte (1 Mio) termine toutes les fenêtres. Mais la **décision**
232:   reste par bloc : un doublon réparti sur deux blocs ne pèse que sa part dans chacun. C'est le
233:   § 4, pas un bug.
234: - **La taille de bloc change le taux mesuré** : sur la même tranche de 200 Mo, 1,59 % de shingles
235:   vus à 64 Mio, 2,45 % à 4 Kio (les répétitions internes au bloc ne sont pas comptées comme
236:   « déjà vu » avant la décision). Comparer deux chiffres exige la même taille de bloc.
237: - **Normalisation.** Les minuscules ne sont qu'**ASCII** : `É` (UTF-8) n'est pas `é`, donc
238:   « Étoile » et « étoile » ne se rencontrent pas. Les espaces horizontaux sont réduits, les
239:   sauts de ligne conservés. Une normalisation Unicode complète augmenterait un peu le taux.
240: - **Le corpus n'est pas homogène.** La tranche de 200 Mo est le **début** du fichier (articles
241:   anciens, peu de boilerplate) : 3,74 % d'octets
… [5835 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='reports/rapport-dedup-blocs.md'; s=open(p).read()\ns = s.replace(\n\"La marge de 0,5 sur la capacité absorbe le pic de redimensionnement de CPython. À chaque bloc,\",\n\"La marge de 0,5 laisse le jeu à la moitié … [1398 caractères tronqués]`

  ```
83:La marge de 0,5 laisse le jeu à la moitié de ce que le budget permettrait : elle absorbe l'écart
214:occurrence. C'est la prochaine étape naturelle, et elle coûte **2 min 30 s** et 3,4 Gio de RSS
280:   hachage, avec normalisation. Les chiffres entre 2 et 5 % mesurent des choses voisines, pas
296:- **La duplication réelle est plus grande que 2 %, et plus courte.** 54 % des lignes, 8,28 % des
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la tools/__pycache__/ | grep -i dedup; echo \"--- git status ---\"; git status --porcelain | head -30; echo \"--- fichiers créés ---\"; ls -la reports/dedup-blocs-7.5go.json reports/rapport-dedup-blocs.md tools/dedup_blocs.py; du … [78 caractères tronqués]`

  ```
-rw-------. 1 stephane stephane  47875 18 nov 10:58 dedup_blocs.cpython-313.pyc
--- git status ---
?? reports/banc-generation-r2.json
?? reports/banc-grammaticalite-r2.json
?? reports/dedup-blocs-7.5go.json
?? reports/rapport-dedup-blocs.md
?? tools/dedup_blocs.py
--- fichiers créés ---
-rw-r--r--. 1 stephane stephane 26397 18 nov 10:57 reports/dedup-blocs-7.5go.json
-rw-------. 1 stephane stephane 21223 18 nov 11:14 reports/rapport-dedup-blocs.md
-rw-------. 1 stephane stephane 38230 18 nov 10:49 tools/dedup_blocs.py
5,7M	work/dedup/controle
4,0K	work/dedup/diagnostic-ancrage.log
8,0K	work/dedup/diagnostic_ancrage.py
4,0K	work/dedup/diagnostic-lignes-exact.log
4,0K	work/dedup/diagnostic_lignes_exact.py
4,0K	work/dedup/diagnostic-lignes.log
4,0K	work/dedup/diagnostic_lignes.py
2,9M	work/dedup/essai-3mo-garde.txt
4,0K	work/dedup/essai-3mo.json
2,9M	work/dedup/essai-3mo.txt
764M	work/dedup/granularite
8,0K	work/dedup/prouve-200Mo.json
4,0K	work/dedup/prouve-200Mo.log
4,0K	work/dedup/prouve-200Mo.out
191M	work/dedup/slice-200Mo-garde.txt
191M	work/dedup/slice-200Mo.txt
8,0K	work/dedup/train-pass.log
4,0K	work/dedup/train-pass.out
7,0G	work/dedup/train.txt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"à supprimer :\" && ls -l work/dedup/essai-3mo* work/dedup/granularite/sortie-*.txt tools/__pycache__/dedup_blocs.cpython-313.pyc 2>&1 | head -12", "description": "List files to clean up"}`

  ```
à supprimer :
-rw-------. 1 stephane stephane     47875 18 nov 10:58 tools/__pycache__/dedup_blocs.cpython-313.pyc
-rw-r--r--. 1 stephane stephane   3000000 18 nov 10:34 work/dedup/essai-3mo-garde.txt
-rw-r--r--. 1 stephane stephane      2879 18 nov 10:34 work/dedup/essai-3mo.json
-rw-r--r--. 1 stephane stephane   3000000 18 nov 10:34 work/dedup/essai-3mo.txt
-rw-r--r--. 1 stephane stephane 199706843 18 nov 10:59 work/dedup/granularite/sortie-0.004.txt
-rw-r--r--. 1 stephane stephane 200000000 18 nov 10:58 work/dedup/granularite/sortie-0.064.txt
-rw-r--r--. 1 stephane stephane 200000000 18 nov 10:58 work/dedup/granularite/sortie-1.txt
-rw-r--r--. 1 stephane stephane 200000000 18 nov 10:58 work/dedup/granularite/sortie-64.txt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && rm -f tools/__pycache__/dedup_blocs.cpython-313.pyc work/dedup/essai-3mo.txt work/dedup/essai-3mo-garde.txt work/dedup/essai-3mo.json work/dedup/granularite/sortie-0.004.txt work/dedup/granularite/sortie-0.064.txt work/dedup/granular … [490 caractères tronqués]`

  ```
supprimés
7,4G	work/dedup
0
--- autotest final ---
code=0
ok True cas 18 ko 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nr = json.load(open('reports/dedup-blocs-7.5go.json'))\nbloc = 67108864\nexacts = [b for b in r['journal_blocs'] if b['octets'] == bloc]\nprint(\"blocs de exactement 64 Mio (coupe au milieu d'une ligne) … [732 caractères tronqués]`

  ```
blocs de exactement 64 Mio (coupe au milieu d'une ligne) : 0
tailles min/max : 55021137 67108862
200 Mo, blocs de exactement 8 Mio : 0
  granularité 64.0 Mio : 0 bloc(s) coupé(s) au milieu sur 3
  granularité 1.0 Mio : 1 bloc(s) coupé(s) au milieu sur 191
  granularité 0.064 Mio : 16 bloc(s) coupé(s) au milieu sur 2000
  granularité 0.004 Mio : 15 bloc(s) coupé(s) au milieu sur 2000
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='reports/rapport-dedup-blocs.md'; s=open(p).read()\ns = s.replace(\n\"1. **Découpe.** Blocs de `--bloc-mo` Mio (64), coupés au dernier saut de ligne — aucune ligne\\n   n'est coupée — plus une marge de contexte * … [1290 caractères tronqués]`

  ```
1. **Découpe.** Blocs de `--bloc-mo` Mio (64), coupés au dernier saut de ligne — 0 coupe au
   milieu d'une ligne sur les 112 blocs de la passe (une ligne plus longue que la moitié du bloc
   forcerait une coupe) — plus une marge de contexte **après** le bloc (2 % du bloc, max 1 Mio)
   qui sert à terminer les fenêtres commencées dans les derniers octets du bloc. Le cœur est ce
   qui sera écrit.
2. **Normalisation.** Minuscules ASCII (`bytes.lower`) et suites d'espaces horizontaux réduites
...
230:- **Le décalage des copies est traité, le refluage ne l'est pas.** Une copie dont les retours à
231-  la ligne diffèrent (texte reflué, lignes fusionnées) n'a plus les mêmes ancres : elle est
232-  invisible. Une copie qui commence au milieu d'une ligne perd sa première ligne, pas les
233-  suivantes. Et un bloc coupé au milieu d'une ligne (impossible ici, possible à 4 Kio) décale
234-  les ancres de cette ligne.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re, pathlib\np = pathlib.Path('reports/rapport-dedup-blocs.md')\ns = p.read_text()\nliens = re.findall(r'\\]\\(([^)#]+)\\)', s)\nprint(\"liens:\", len(liens))\nfor l in sorted(set(liens)):\n    cible = (p.pa … [563 caractères tronqués]`

  ```
liens: 7
  OK   ../tools/dedup_blocs.py
  OK   ../work/dedup/diagnostic_ancrage.py
  OK   ../work/dedup/diagnostic_lignes_exact.py
  OK   dedup-blocs-7.5go.json
  OK   rapport-donnees-inventaire.md
  OK   rapport-n2-corpus-1go.md
mots: 3744
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m py_compile tools/dedup_blocs.py && echo \"compile OK\" && (python3 -m pyflakes tools/dedup_blocs.py 2>&1 | head -10 || echo \"pyflakes absent\") && echo \"--- prints ---\" && grep -n \"print(\" tools/dedup_blocs.py && echo … [133 caractères tronqués]`

  ```
compile OK
/usr/bin/python3: No module named pyflakes
--- prints ---
448:                print(
781:        print(json.dumps(resume, ensure_ascii=False, indent=1))
801:        print(f"ERREUR {e.nom}: {e.message}", file=sys.stderr)
804:        print("interrompu", file=sys.stderr)
809:    print(json.dumps({
--- autotest via CLI ---
  }
 ]
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && mkdir -p /tmp/edge && : > /tmp/edge/vide.txt && printf 'une seule ligne sans fin de ligne' > /tmp/edge/sansnl.txt && printf 'court' > /tmp/edge/court.txt && python3 - <<'EOF'\nimport subprocess, sys, json\ncas = [\n  (\"vide\", \"/tm … [801 caractères tronqués]`

  ```
vide            rc=2 sortie=/tmp/edge/vide.txt stderr=ERREUR sortie_invalide: l'entrée et la sortie sont le même fichier
sans nl         rc=0 sortie=/tmp/edge/sans_nl.txt stderr=[bloc 1] 0/0 Mio, 0.0% vu, gardé, RSS 22 Mio, 0 s
court           rc=2 sortie=/tmp/edge/court.txt stderr=ERREUR sortie_invalide: l'entrée et la sortie sont le même fichier
seuil 0         rc=0 sortie=/tmp/edge/seuil_0.txt stderr=[bloc 1] 0/0 Mio, 0.0% vu, gardé, RSS 22 Mio, 0 s
seuil 1         rc=0 sortie=/tmp/edge/seuil_1.txt stderr=[bloc 1] 0/0 Mio, 0.0% vu, gardé, RSS 22 Mio, 0 s
data interdit   rc=2 sortie=/tmp/edge/data_interdit.txt stderr=ERREUR sortie_interdite: /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/ici.txt est sous data/ (lecture seule)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport subprocess, sys\ncas = [(\"vide\", \"/tmp/edge/vide.txt\"), (\"court\", \"/tmp/edge/court.txt\"),\n       (\"sans nl\", \"/tmp/edge/sansnl.txt\"), (\"8 octets\", \"/tmp/edge/8.txt\")]\nopen(\"/tmp/edge/8.txt … [732 caractères tronqués]`

  ```
vide       rc=0 stderr=
   sortie: b'' | json blocs: {'total': 0, 'gardes': 0, 'ecartes': 0, 'octets_gardes': 0, 'octets_ecartes': 0, 'pct_octets_ecartes': 0.0}
court      rc=0 stderr=[bloc 1] 0/0 Mio, 0.0% vu, gardé, RSS 22 Mio, 0 s
   sortie: b'court' | json blocs: {'total': 1, 'gardes': 1, 'ecartes': 0, 'octets_gardes': 5, 'octets_ecartes': 0, 'pct_octets_ecartes': 0.0}
sans nl    rc=0 stderr=[bloc 1] 0/0 Mio, 0.0% vu, gardé, RSS 22 Mio, 0 s
   sortie: b'une seule ligne sans fin de ligne' | json blocs: {'total': 1, 'gardes': 1, 'ecartes': 0, 'octets_gardes': 33, 'octets_ecartes': 0, 'pct_octets_ecartes': 0.0}
8 octets   rc=0 stderr=[bloc 1] 0/0 Mio, 0.0% vu, gardé, RSS 22 Mio, 0 s
   sortie: b'abcdefgh' | json blocs: {'total': 1, 'gardes': 1, 'ecartes': 0, 'octets_gardes': 8, 'octets_ecartes': 0, 'pct_octets_ecartes': 0.0}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 46,66p tools/dedup_blocs.py", "description": "Check docstring budget formula"}`

  ```
chien de garde relit `resource.getrusage(RUSAGE_SELF).ru_maxrss` et **sort en erreur
   nommée** si le RSS dépasse le budget (`ERREUR memoire_depassee`, code 3) ; idem si le
   jeu dépasse la capacité (`capacite_depassee`). Un budget inférieur au plancher est
   refusé au départ (`budget_memoire_impossible`).

CE QUE L'OUTIL N'EST PAS. Ce n'est pas un dédoublonnage au sens de `corpus_propre.py` :
la décision est **par bloc**, donc un bloc n'est écarté que si *son* contenu est
majoritairement déjà vu. Une répétition dispersée (quelques pour cent répartis sur tout
le fichier) ne fait tomber aucun bloc de 64 Mio sous le seuil : elle est **mesurée**
(taux de shingles déjà vus) mais **pas retirée**. Le seuil et la taille de bloc décident
donc de ce qui est retiré, pas seulement le taux de duplication.

Usage :
  python3 tools/dedup_blocs.py --entree data/corpus_wiki_fr_texte/train.txt \\
      --sortie work/dedup/train.txt --bloc-mo 64 --memoire-mo 2048 \\
      --json reports/dedup-blocs-7.5go.json
  python3 tools/dedup_blocs.py --autotest          # contrôle négatif reproductible
  python3 tools/dedup_blocs.py --entree F --sortie G --memoire-mo 64 --bloc-mo 64
                        
… [152 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 36,46p tools/dedup_blocs.py", "description": "Read budget formula in docstring"}`

  ```
5. **Budget mémoire.** Le taux d'échantillonnage `p` et la capacité du jeu sont calculés
   **avant** la lecture, à partir du budget, de la taille du fichier et du coût mesuré
   d'une entrée de `set` :

       plancher  = 4 × (bloc + recouvrement) + 32 Mio + 48 Mio   (copies + interpréteur)
       capacité  = (budget − plancher) / coût_mesuré_d_une_entrée
       p         = plus grande puissance de 2 ≤ 0,5 × capacité / (octets / pas)

   Le facteur 0,5 est une marge : le `set` de CPython double sa table en grandissant
   (pic ≈ 1,5 × la table finale), et le coût mesuré inclut ce pic. À chaque bloc, le
   chien de garde relit `resource.getrusage(RUSAGE_SELF).ru_maxrss` et **sort en erreur
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", "old_string": "       plancher  = 4 × (bloc + recouvrement) + 32 Mio + 48 Mio   (copies + interpréteur)\n       capacité  = (budget − plancher) / coût_mesuré_d_une_entrée\n       p         = plus grande puissance d … [745 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", "limit": 20, "offset": 36}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py</path>
<type>file</type>
<content>
36: 5. **Budget mémoire.** Le taux d'échantillonnage `p` et la capacité du jeu sont calculés
37:    **avant** la lecture, à partir du budget, de la taille du fichier et du coût mesuré
38:    d'une entrée de `set` :
39: 
40:        plancher  = 4 × (bloc + recouvrement) + 32 Mio + 48 Mio   (copies + interpréteur)
41:        capacité  = (budget − plancher) / coût_mesuré_d_une_entrée
42:        p         = plus grande puissance de 2 ≤ 0,5 × capacité / (octets / pas)
43: 
44:    Le facteur 0,5 est une marge : le `set` de CPython double sa table en grandissant
45:    (pic ≈ 1,5 × la table finale), et le coût mesuré inclut ce pic. À chaque bloc, le
46:    chien de garde relit `resource.getrusage(RUSAGE_SELF).ru_maxrss` et **sort en erreur
47:    nommée** si le RSS dépasse le budget (`ERREUR memoire_depassee`, code 3) ; idem si le
48:    jeu dépasse la capacité (`capacite_depassee`). Un budget inférieur au plancher est
49:    refusé au départ (`budget_memoire_impossible`).
50: 
51: CE QUE L'OUTIL N'EST PAS. Ce n'est pas un dédoublonnage au sens de `corpus_propre.py` :
52: la décisi
… [414 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", "new_string": "       plancher  = 4 × (bloc + recouvrement) + 32 Mio + 48 Mio   (copies + interpréteur)\n       capacité  = (budget − plancher) / coût_mesuré_d_une_entrée\n       p         = plus grande puissance d … [923 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 36,50p tools/dedup_blocs.py && python3 -m py_compile tools/dedup_blocs.py && echo \"compile OK\" && rm -f tools/__pycache__/dedup_blocs.cpython-313.pyc && python3 tools/dedup_blocs.py --autotest 2>&1 | tail -2 && rm -f tools/_ … [139 caractères tronqués]`

  ```
5. **Budget mémoire.** Le taux d'échantillonnage `p` et la capacité du jeu sont calculés
   **avant** la lecture, à partir du budget, de la taille du fichier et du coût mesuré
   d'une entrée de `set` :

       plancher  = 4 × (bloc + recouvrement) + 32 Mio + 48 Mio   (copies + interpréteur)
       capacité  = (budget − plancher) / coût_mesuré_d_une_entrée
       p         = plus grande puissance de 2 ≤ 0,5 × capacité / (1,5 × octets / pas)

   Le 1,5 compte les ancres de début de ligne, qui s'ajoutent à celles du pas. Le facteur
   0,5 est une marge : le `set` de CPython double sa table en grandissant (pic ≈ 1,5 × la
   table finale), et le coût mesuré (80 o par entrée) inclut ce pic. À chaque bloc, le
   chien de garde relit `resource.getrusage(RUSAGE_SELF).ru_maxrss` et **sort en erreur
   nommée** si le RSS dépasse le budget (`ERREUR memoire_depassee`, code 3) ; idem si le
   jeu dépasse la capacité (`capacite_depassee`). Un budget inférieur au plancher est
   refusé au départ (`budget_memoire_impossible`).
compile OK
 ]
}
0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/dedup_blocs.py --autotest > /tmp/a.json 2>/dev/null; echo \"autotest rc=$?\"; python3 -c \"\nimport json; r=json.load(open('/tmp/a.json')); print('ok:', r['ok'], '| cas:', len(r['cas']), '| KO:', sum(1 for c in r['cas'] … [342 caractères tronqués]`

  ```
autotest rc=0
ok: True | cas: 18 | KO: 0
--- git ---
?? reports/dedup-blocs-7.5go.json
?? reports/rapport-dedup-blocs.md
?? tools/dedup_blocs.py
--- tailles ---
-rw-r--r--. 1 stephane stephane      26397 18 nov 10:57 reports/dedup-blocs-7.5go.json
-rw-------. 1 stephane stephane      21429 18 nov 11:15 reports/rapport-dedup-blocs.md
-rw-------. 1 stephane stephane      38337 18 nov 11:16 tools/dedup_blocs.py
-rw-r--r--. 1 stephane stephane 7504078589 18 nov 10:57 work/dedup/train.txt
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='reports/rapport-dedup-blocs.md'; s=open(p).read()\nold = (\"Conséquence directe : un dédoublonnage **par bloc** ne peut pas retirer cette masse (aucun bloc\\n\"\n       \"n'est majoritairement de la copie), alor … [1751 caractères tronqués]`

  ```
214:jusqu'à 621 Mo (8,28 %), dont 23 Mo de lignes vides à préserver comme séparateurs : **598 Mo
288:   **ligne**, on retirerait jusqu'à 621 Mo (8,28 %), dont 23 Mo de lignes vides (à garder) et
308:  octets (598 Mo hors lignes vides), dont 2,6 % de prose. La conclusion de l'inventaire — « le volume est là, il faut
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 304,314p reports/rapport-dedup-blocs.md", "description": "Check line wrapping"}`

  ```
de cette fiche en donne le coût : 2 min 30 s et 3,4 Gio de RSS pour la version triée, ou
  ≈ 2 min et un `set` échantillonné pour la version en flux.
- **Le chiffre de l'inventaire est à corriger** dans les documents de pilotage : 2,0 % est une
  sous-estimation (méthode à grille fixe) et la masse retirable par ligne est plutôt de 8 % des
  octets (598 Mo hors lignes vides), dont 2,6 % de prose. La conclusion de l'inventaire — « le volume est là, il faut
  l'outiller » — reste vraie ; c'est la nature du dédoublonnage qui change : par ligne, pas par
  bloc.
- **Ce qui n'est pas tranché** : retirer 8,28 % des octets en supprimant les lignes répétées
  enlève aussi des lignes de tableau et de catégorie qui ont un sens ; un filtre « lignes
  dupliquées + longueur ≥ N » est un choix éditorial, à mesurer sur une perte de qualité, pas
  seulement sur des octets.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='reports/rapport-dedup-blocs.md'; s=open(p).read()\ns = s.replace(\n\"  octets (598 Mo hors lignes vides), dont 2,6 % de prose. La conclusion de l'inventaire — « le volume est là, il faut\\n  l'outiller » — reste … [358 caractères tronqués]`

  ```
- **Le chiffre de l'inventaire est à corriger** dans les documents de pilotage : 2,0 % est une
  sous-estimation (méthode à grille fixe) et la masse retirable par ligne est plutôt de 8 % des
  octets (598 Mo hors lignes vides), dont 2,6 % de prose. La conclusion de l'inventaire — « le
  volume est là, il faut l'outiller » — reste vraie ; c'est la nature du dédoublonnage qui change : par ligne, pas par
  bloc.
99: 117
195: 119
204: 112
301: 138
309: 118
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk 'length > 100 && $0 !~ /^\\|/ {print NR\": \"length\": \"$0}' reports/rapport-dedup-blocs.md", "description": "Find long non-table lines"}`

  ```
195: 119: Mesure **exacte** sur les 7,50 Go ([`work/dedup/diagnostic_lignes_exact.py`](../work/dedup/diagnostic_lignes_exact.py),
301: 138:   octets ; pour les lignes de 80 o et +, 3,1 % de leurs octets (194 Mo, 2,59 % du fichier). La prochaine action est un dédoublonnage **par
309: 118:   volume est là, il faut l'outiller » — reste vraie ; c'est la nature du dédoublonnage qui change : par ligne, pas par
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='reports/rapport-dedup-blocs.md'; s=open(p).read()\ns = s.replace(\n\"Mesure **exacte** sur les 7,50 Go ([`work/dedup/diagnostic_lignes_exact.py`](../work/dedup/diagnostic_lignes_exact.py),\\nhachage de chaque li … [1001 caractères tronqués]`

  ```
303: 137
- **L'outil est le bon bâtiment, la mauvaise maille.** `tools/dedup_blocs.py` prouve qu'on peut
  traverser 7,50 Go en 2 Go de RAM, décider de façon déterministe et rendre des erreurs nommées.
  Mais la décision par bloc de 64 Mio est un **no-op** sur ce corpus : il ne faut pas construire
  le corpus v2 avec.
- **La duplication réelle est plus grande que 2 %, et plus courte.** 54 % des lignes, 8,28 % des
  octets ; pour les lignes de 80 o et +, 3,1 % de leurs octets (194 Mo, 2,59 % du fichier).
  La prochaine action est un dédoublonnage **par ligne** en flux, avec le même modèle de budget : hacher chaque ligne, garder la première
  occurrence (en préservant les séparateurs vides), et mesurer ce qui reste. Le diagnostic exact
  de cette fiche en donne le coût : 2 min 30 s et 3,4 Gio de RSS pour la version triée, ou
  ≈ 2 min et un `set` échantillonné pour la version en flux.
- **Le chiffre de l'inventaire est à corriger** dans les documents de pilotage : 2,0 % est une
  sous-estimation (méthode à grille fixe) et la masse retirable par ligne est plutôt de 8 % des
  octets (598 Mo hors lignes vides), dont 2,6 % de prose. La conclusion de l'inventaire — « le
  volume est là, i
… [201 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='reports/rapport-dedup-blocs.md'; s=open(p).read()\ns = s.replace(\n\"  La prochaine action est un dédoublonnage **par ligne** en flux, avec le même modèle de budget : hacher chaque ligne, garder la première\\n   … [391 caractères tronqués]`

  ```
304: 136
(vide = ok)
329 reports/rapport-dedup-blocs.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 300,308p reports/rapport-dedup-blocs.md", "description": "Inspect remaining long line"}`

  ```
le corpus v2 avec.
- **La duplication réelle est plus grande que 2 %, et plus courte.** 54 % des lignes, 8,28 % des
  octets ; pour les lignes de 80 o et +, 3,1 % de leurs octets (194 Mo, 2,59 % du fichier).
  La prochaine action est un dédoublonnage **par ligne** en flux, avec le même modèle de budget :
  hacher chaque ligne, garder la première occurrence (en préservant les séparateurs vides), et mesurer ce qui reste. Le diagnostic exact
  de cette fiche en donne le coût : 2 min 30 s et 3,4 Gio de RSS pour la version triée, ou
  ≈ 2 min et un `set` échantillonné pour la version en flux.
- **Le chiffre de l'inventaire est à corriger** dans les documents de pilotage : 2,0 % est une
  sous-estimation (méthode à grille fixe) et la masse retirable par ligne est plutôt de 8 % des
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='reports/rapport-dedup-blocs.md'; s=open(p).read()\ns = s.replace(\n\"  hacher chaque ligne, garder la première occurrence (en préservant les séparateurs vides), et mesurer ce qui reste. Le diagnostic exact\\n  d … [880 caractères tronqués]`

  ```
305: 132
Vérification finale des tableaux
tableaux incohérents: 0 | lignes: 329 | mots: 3774
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 303,307p reports/rapport-dedup-blocs.md", "description": "Inspect line 305"}`

  ```
La prochaine action est un dédoublonnage **par ligne** en flux, avec le même modèle de budget :
  hacher chaque ligne, garder la première occurrence (en préservant les séparateurs vides), et
  mesurer ce qui reste. Le diagnostic exact de cette fiche en donne le coût : 2 min 30 s et 3,4 Gio de RSS pour la version triée, ou
  ≈ 2 min et un `set` échantillonné pour la version en flux.
- **Le chiffre de l'inventaire est à corriger** dans les documents de pilotage : 2,0 % est une
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='reports/rapport-dedup-blocs.md'; s=open(p).read()\ns = s.replace(\n\"  mesurer ce qui reste. Le diagnostic exact de cette fiche en donne le coût : 2 min 30 s et 3,4 Gio de RSS pour la version triée, ou\\n  ≈ 2 m … [467 caractères tronqués]`

  ```
ok si vide

- **L'outil est le bon bâtiment, la mauvaise maille.** `tools/dedup_blocs.py` prouve qu'on peut
  traverser 7,50 Go en 2 Go de RAM, décider de façon déterministe et rendre des erreurs nommées.
  Mais la décision par bloc de 64 Mio est un **no-op** sur ce corpus : il ne faut pas construire
  le corpus v2 avec.
- **La duplication réelle est plus grande que 2 %, et plus courte.** 54 % des lignes, 8,28 % des
  octets ; pour les lignes de 80 o et +, 3,1 % de leurs octets (194 Mo, 2,59 % du fichier).
  La prochaine action est un dédoublonnage **par ligne** en flux, avec le même modèle de budget :
  hacher chaque ligne, garder la première occurrence (en préservant les séparateurs vides), et
  mesurer ce qui reste. Le diagnostic exact de cette fiche en donne le coût : 2 min 30 s et
  3,4 Gio de RSS pour la version triée, ou ≈ 2 min et un `set` échantillonné en flux.
- **Le chiffre de l'inventaire est à corriger** dans les documents de pilotage : 2,0 % est une
  sous-estimation (méthode à grille fixe) et la masse retirable par ligne est plutôt de 8 % des
  octets (598 Mo hors lignes vides), dont 2,6 % de prose. La conclusion de l'inventaire — « le
  volume est là, il faut l'outi
… [68 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib\ntxt = pathlib.Path('reports/rapport-dedup-blocs.md').read_text()\nr = json.load(open('reports/dedup-blocs-7.5go.json'))\np = json.load(open('work/dedup/prouve-200Mo.json'))\na = json.load(open … [1733 caractères tronqués]`

  ```
valeurs manquantes: 0
cohérence JSON ↔ rapport : OK
?? reports/dedup-blocs-7.5go.json
?? reports/rapport-dedup-blocs.md
?? tools/dedup_blocs.py
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py", "limit": 14, "offset": 641}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/dedup_blocs.py</path>
<type>file</type>
<content>
641:     cas: list[dict] = []
642: 
643:     def verifie(nom: str, condition: bool, detail) -> None:
644:         cas.append({"nom": nom, "ok": bool(condition), "detail": detail})
645: 
646:     commun = ["--entree", str(controle), "--bloc-mo", "0.0625"]
647:     rc1, r1, log1 = lance("seuil080", [*commun, "--sortie", str(repertoire / "garde-080.txt"),
648:                                       "--seuil", "0.8", "--memoire-mo", "512"])
649:     g1 = gardes(r1)
650:     f1 = fractions(r1)
651:     verifie("a_texte_unique_garde", all(g1[0:4]) and rc1 == 0, {"blocs": g1[0:4], "rc": rc1})
652:     verifie("b_copie_exacte_ecartee", not any(g1[4:8]), {"blocs": g1[4:8], "fractions": f1[4:8]})
653:     verifie("b_fraction_1", all(x == 1.0 for x in f1[4:8]), {"fractions": f1[4:8]})
654:     verifie("c_copie_10pct_ecartee_a_080", not any(g1[8:12]),

(Showing lines 641-654 of 824. Use offset=655 to continue.)
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def lance_autotest\" -A 3 tools/dedup_blocs.py && grep -n \"if a.autotest:\" -A 4 tools/dedup_blocs.py", "description": "Locate autotest entry points"}`

  ```
602:def lance_autotest(repertoire: pathlib.Path) -> tuple[bool, dict]:
603-    repertoire.mkdir(parents=True, exist_ok=True)
604-    outil = str(pathlib.Path(__file__).resolve())
605-    paragraphe = 2048
780:    if a.autotest:
781-        ok, resume = lance_autotest(pathlib.Path(a.repertoire))
782-        print(json.dumps(resume, ensure_ascii=False, indent=1))
783-        return 0 if ok else 1
784-
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/dedup_blocs.py'; s=open(p).read()\nold = '''def lance_autotest(repertoire: pathlib.Path) -> tuple[bool, dict]:\n    repertoire.mkdir(parents=True, exist_ok=True)'''\nnew = '''def lance_autotest(repertoire: … [1453 caractères tronqués]`

  ```
compile OK
rc=0
ok True cas 18
--- répertoire data/ refusé ---
rc=2
[stderr]
ERREUR sortie_interdite: /home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/controle est sous data/ (lecture seule)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain | grep -iE \"dedup|pycache\"; echo \"--- work/dedup ---\"; ls -la work/dedup | grep -vE \"^total\"; echo \"--- data intact ---\"; ls -la data/corpus_wiki_fr_texte/train.txt; ls data/controle 2>&1 | head -1; ech … [215 caractères tronqués]`

  ```
?? reports/dedup-blocs-7.5go.json
?? reports/rapport-dedup-blocs.md
?? tools/dedup_blocs.py
--- work/dedup ---
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
-rw-r--r--. 1 stephane stephane  200000000 18 nov 10:46 slice-
… [423 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la work/dedup/granularite work/dedup/controle | head -25; du -sh work/dedup", "description": "Check remaining artifacts"}`

  ```
work/dedup/controle:
total 5776
drwxr-xr-x. 1 stephane stephane     568 18 nov 10:46 .
drwxr-xr-x. 1 stephane stephane     556 18 nov 11:14 ..
-rw-r--r--. 1 stephane stephane    4117 18 nov 11:18 autotest.json
-rw-r--r--. 1 stephane stephane    1622 18 nov 11:18 budget_impossible.json
-rw-r--r--. 1 stephane stephane    1878 18 nov 11:18 chien_de_garde.json
-rw-r--r--. 1 stephane stephane  786453 18 nov 11:18 controle_decale.txt
-rw-r--r--. 1 stephane stephane  524587 18 nov 11:18 controle_disperse.txt
-rw-r--r--. 1 stephane stephane 1048576 18 nov 11:18 controle.txt
-rw-r--r--. 1 stephane stephane    5066 18 nov 11:18 decale.json
-rw-r--r--. 1 stephane stephane    4291 18 nov 11:18 disperse.json
-rw-r--r--. 1 stephane stephane  524288 18 nov 11:18 garde-080-bis.txt
-rw-r--r--. 1 stephane stephane  524288 18 nov 11:18 garde-080.txt
-rw-r--r--. 1 stephane stephane  786432 18 nov 11:18 garde-095.txt
-rw-r--r--. 1 stephane stephane  524288 18 nov 11:18 garde-32.txt
-rw-r--r--. 1 stephane stephane  526336 18 nov 11:18 garde-decale.txt
-rw-r--r--. 1 stephane stephane  524587 18 nov 11:18 garde-disperse.txt
-rw-r--r--. 1 stephane stephane    5652 18 nov 11:18 hash32.json
-rw-r--r--. 1 ste
… [293 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la work/dedup/granularite/", "description": "List granularity JSONs"}`

  ```
total 812
drwxr-xr-x. 1 stephane stephane    106 18 nov 11:14 .
drwxr-xr-x. 1 stephane stephane    556 18 nov 11:14 ..
-rw-r--r--. 1 stephane stephane 382926 18 nov 10:59 bloc-0.004.json
-rw-r--r--. 1 stephane stephane 396808 18 nov 10:58 bloc-0.064.json
-rw-r--r--. 1 stephane stephane  41491 18 nov 10:58 bloc-1.json
-rw-r--r--. 1 stephane stephane   3210 18 nov 10:58 bloc-64.json
  ```

- **send_message** `{"agent_id": "d67a9bb1-090e-4f69-baf2-a831c00aa275", "message": "TÂCHE TERMINÉE (sous-agent dédup par blocs). Aucun commit, aucune écriture dans data/, aucun appel API, en-cours/roadmap/AGENTS intacts.\n\n## Livrables\n- `tools/dedup_blocs.py` (CLI exacte demandée + `--pas/--hash-bits/--graine/--aut … [3136 caractères tronqués]`

  ```
message delivered to agent d67a9bb1-090e-4f69-baf2-a831c00aa275
  ```

### 🤖 Assistant

⏵ Bilan final : chiffres, contrôles, chemins

Travail terminé. Voici le bilan.

## Livrables

| fichier | quoi |
|---|---|
| `tools/dedup_blocs.py` | l'outil (CLI demandée + autotest intégré, erreurs nommées) |
| `reports/rapport-dedup-blocs.md` | le rapport (dispositif, chiffres, contrôles, failles, comparaison inventaire) |
| `reports/dedup-blocs-7.5go.json` | le manifeste JSON de la passe |
| `work/dedup/train.txt` | la sortie (7 504 078 589 o, sha256 `27277e32…`), + `prouve-200Mo.json`, `controle/`, `granularite/`, diagnostics |

`data/` n'a pas été modifié (`train.txt` intact, mtime inchangé), aucun commit, aucun appel API, `en-cours`/`roadmap`/`AGENTS` intacts.

## Chiffres — 7,50 Go, `--bloc-mo 64 --memoire-mo 2048`

- **Temps : 430,7 s = 7 min 11 s** (16,6 Mio/s ; CPU 99 %, 419,9 s user) — c'est le hachage qui domine, pas l'I/O.
- **RSS max : 954,3 Mio** pour un budget de 2 048 Mio (marge 1 094) ; confirmé de l'extérieur par `/usr/bin/time` (977 200 Kio).
- **112 blocs : 112 gardés, 0 écarté, 0 octet écarté → 0,000 %** ; sortie identique à l'entrée à l'octet près (`cmp`).
- 191 312 755 shingles calculés, 6 006 207 échantillonnés (1/32) : **4,177 % déjà vus avant leur bloc, 5,171 % avec les répétitions internes**. Le bloc le plus chargé est à **48,9 %** — loin du seuil de 80 %.
- Preuve de budget : **200 Mo avec 256 Mio → RSS 120,8 Mio** (marge 135) ; budget impossible → `ERREUR budget_memoire_impossible` (rc 3) ; chien de garde déclenché pour de vrai → `ERREUR memoire_depassee` (rc 3).

## Les 4 cas de contrôle (18/18 assertions vertes)

| cas | attendu | observé |
|---|---|---|
| (a) texte unique | gardé | **gardé**, 0,0 % |
| (b) copie exacte | écarté | **écarté**, 100,0 % |
| (c) copie à 9,4 % modifiée | écarté à 0,8, gardé à 0,95 | **écarté** (90,04–90,21 %), **gardé à 0,95** — le seuil tranche entre 0,90 et 0,95 |
| (d) texte différent | gardé | **gardé**, 0,0 % |

En plus : copie **décalée de 21 octets** écartée (99,9–100 %) — c'est précisément ce qu'une grille à pas fixe rate ; copie à **10 % de mots dispersés gardée** (1–3 % vus) ; **stabilité** : deux passes → même sha256 (`1a5c01ef…`), mêmes décisions, mêmes octets.

## Le résultat qui change la suite

Le dédoublonnage **par blocs ne ferme pas l'écart** : à 64 Mio, 0 % ; même à 4 Kio, 0,147 % seulement. La mesure exacte ligne à ligne montre pourquoi : **53,98 % des lignes sont des répétitions, mais 8,28 % des octets** (621 Mo, dont 23 Mo de lignes vides à préserver → 598 Mo de contenu ; 2,59 % pour les lignes de 80 o et +). La duplication est courte et diffuse, pas « en blocs ».

Et le chiffre de l'inventaire est biaisé : sa grille à pas fixe sous-estime de **16×** sur 100 Mo (0,04 % contre 0,62 % pour toutes les fenêtres), encore **1,8×** à 7,50 Go (2,93 % contre 5,17 %). La correction à retenir : ~5 % des shingles, 8,28 % des octets, et la prochaine action est un dédup **par ligne** en flux (≈ 2 min) — pas un dédup par blocs.

