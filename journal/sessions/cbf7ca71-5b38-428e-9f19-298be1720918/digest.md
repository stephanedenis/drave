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

