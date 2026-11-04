# Session DSH — relecture

- identifiant : `206a4022-ab3c-497d-a5fa-0194931c7fa0`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-04 15:56:23
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt Drave, racine /home/stephane/Data13TB/stephane/GitHub/Qtrinet (lis AGENTS.md pour le contexte général, mais ton périmètre est strictement celui ci-dessous).

CONTEXTE. La session `aeafe951` a clos la limite de D : les 8 scans `.PDF` du fonds CEGEP (58 p) ont été OCRisés (rapport `reports/rapport-ocr-pdf-restants.md`, manifeste `reports/ocr-pdf-restants.json`, texte brut `work/ocr/restants/train.txt`, 55 857 octets, 4 documents retenus, 49 p, 54 167 car.). Le hub a ensuite **appended** ce texte au corpus CEGEP : `data/corpus_ocr_cegep/train.txt` est passé de 4 430 959 à 4 486 816 octets à 15 h 49. `val.txt` (12 536 o) et `test.txt` (10 524 o) n'ont pas bougé (hashes conformes au manifeste `reports/ocr-pdf-cegep.json`). Il manque : la preuve de l'append, les statistiques du corpus à 64 documents, le contrôle de contamination à 8 Ko, et la fiche.

MISSION. Vérifier et documenter l'intégration, sans la modifier. Tu ne dois **rien écrire dans `data/`**, rien committer, ne toucher ni `docs/pilotage/*`, ni `en-cours`, ni `roadmap`, ni `AGENTS.md`, ni les fichiers d'une autre session.

1. **Audit de l'append** (lecture seule) :
   - `data/corpus_ocr_cegep/train.txt` : taille 4 486 816 ; les **derniers 55 857 octets** doivent être identiques à `work/ocr/restants/train.txt` (compare par `tail -c 55857 | sha256sum` et par `cmp` sur le fichier extrait) ;
   - jonction : l'octet à l'offset 4 430 959 doit être `C` (début de l'append) et l'octet précédent `\n` (aucun mot collé) — vérifie-le indépendamment ;
   - `val.txt` et `test.txt` : SHA-256 doivent valoir `dd605833f27eab63df46de3437b1e74b479c2c3abcd6ea683365647063ccd0e1` et `1c9ab73459c1e44ae7c1e23e46210091c54a5be360df698bdad150e9c1153b84` ;
   - nouveau SHA-256 de `train.txt` : `111f79a4ede133e9e50e5057a8b7314820f48c8f750101b8917340dc259dffeb` (à confirmer).
2. **Statistiques du corpus 64** : 53+4=57 documents train, 4 val, 3 test (total **64**) ; pages **2 031** (1 982+49) ; caractères **4 462 978** (4 408 811+54 167) ; tronçons **582** (573+9) ; octets {train 4 486 816, val 12 536, test 10 524}. Vérifie chaque somme, ne les recopie pas sans les recalculer.
3. **Contrôle de contamination à 8 Ko** :
   `python3 tools/verifie_contamination.py --train data/corpus_ocr_cegep/train.txt --val data/corpus_ocr_cegep/val.txt --test data/corpus_ocr_cegep/test.txt --taille-troncon 8192 --sortie work/ocr/cegep64/contamination.json`
   (regarde `--help` d'abord ; adapte les options si nécessaire, mais garde 8 192). Résultat attendu : **0 duplication entre splits**, fenêtres comptées train/val/test. Si le script refuse un fichier vide ou un argument, note-le.
   **Contrôle négatif obligatoire** : copie les trois fichiers dans `work/ocr/cegep64/controle/`, injecte dans le train une fenêtre de 8 Ko **prise dans val**, relance le script sur la copie : il **doit** trouver au moins une fuite. Sans ce contrôle, un « 0 » ne prouve rien.
4. **Livrables** (écris uniquement ces fichiers) :
   - `reports/ocr-cegep-64.json` : manifeste daté (corpus, split, pages, caractères, octets, SHA-256 des trois splits, tronçons, résultat de contamination réel + contrôle négatif, preuve de l'append : taille avant/après, hash de la queue, jonction) ;
   - `reports/rapport-ocr-cegep-64.md` : fiche courte (verdict, tableau, contrôles négatifs, ce qui pourrait la rendre faux, limites, ligne d'état proposée au hub). Style du dépôt : un chiffre, une mesure, un contrôle ; pas de récit.
   - `work/ocr/cegep64/` : tes fichiers intermédiaires (non versionnés).
5. **Interdits** : modifier `data/`, `reports/ocr-pdf-cegep.json` (il est historique), `docs/`, `AGENTS.md`, committer, lancer un job GPU, tuer un job, écrire dans `reports/` autre chose que les deux livrables, toucher aux fichiers d'autres sessions. La machine a un run N2 sur GPU (claim `n2-jour`) : tout job lourd se fait sur cpu1 (`taskset -c 10-19,30-39`).
6. **Arrêt** : si un hash, une taille ou la jonction ne correspond pas, **arrête-toi** et rapporte le désaccord sans « réparer ». Si le contrôle négatif ne trouve pas la fuite injectée, arrête-toi aussi. Timebox : 30 min, 3 essais max sur le script de contamination.

RAPPORT FINAL (10 lignes, en français) :
1. fait (le chiffre) ; 2. fichiers touchés ; 3. la commande de contamination et son résultat ; 4. le contrôle négatif (fuite injectée trouvée ?) ; 5. ce qui pourrait rendre le résultat faux ; 6. limites ; 7. prochaine action ; 8. **ligne d'état exacte à mettre dans `en-cours`** (une phrase) ; 9. commit (« aucun ») ; 10. blocage nommé ou « aucun ».
Your parent agent id is "aeafe951-9c3d-4bb5-8af7-0246a4f3d51d". Before you finish, send your result to that agent with send_message({ agent_id: "aeafe951-9c3d-4bb5-8af7-0246a4f3d51d", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Lecture du contexte AGENTS.md et inventaire des fichiers

- **bash** `{"command": "pwd && ls -la && echo \"---\" && ls -la data/corpus_ocr_cegep/ work/ocr/restants/ reports/ 2>&1 | head -60", "description": "Inspecte la racine et les répertoires cibles"}`

  ```
/home/stephane/GitHub/Qtrinet
total 204
drwxr-xr-x. 1 stephane stephane   660  1 nov 10:50 .
drwxr-xr-x. 1 stephane stephane  2508  4 nov 11:00 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   124 31 oct 18:00 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   198  4 nov 15:54 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   872  4 nov 08:51 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 19956 29 oct 08:14 README.md
drwxr-xr-x. 1 stephane stephane 65510  4 nov 15:30 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 s
… [4877 caractères tronqués]
  ```

- **bash** `{"command": "date -Is && echo \"---\" && ls -la tools/ | head -30", "description": "Date courante et liste des outils"}`

  ```
2026-11-04T15:56:27-05:00
---
total 4856
drwxr-xr-x. 1 stephane stephane  17190  4 nov 11:34 .
drwxr-xr-x. 1 stephane stephane    660  1 nov 10:50 ..
-rw-------. 1 stephane stephane   8428 24 oct 21:16 adaptateur_langue.py
-rwx--x--x. 1 stephane stephane  11640  1 oct 04:21 aiguille.py
-rw-r--r--. 1 stephane stephane  80950 19 oct 14:33 aligneur_litteraire.py
-rw-------. 1 stephane stephane   7797  6 oct 22:04 amplification.py
-rw-------. 1 stephane stephane   3848 21 oct 00:56 analyse_alignement.py
-rwx--x--x. 1 stephane stephane   8850  1 oct 17:40 analyse_empreinte.py
-rw-------. 1 stephane stephane   4614  2 oct 17:28 analyse_engram.py
-rwx--x--x. 1 stephane stephane  11086  1 oct 20:13 analyse_experts_statique.py
-rwxr-xr-x. 1 stephane stephane   5449  3 oct 04:19 analyse_flux.py
-rwx--x--x. 1 stephane stephane   6767  3 oct 09:42 analyse_hc.py
-rw-------. 1 stephane stephane   6681 20 oct 08:52 analyse_litteraire.py
-rwx--x--x. 1 stephane stephane   6364  3 oct 08:11 analyse_octets_par_jeton.py
-rwx--x--x. 1 stephane stephane   6029  3 oct 11:51 analyse_reutilisation_experts.py
-rw-------. 1 stephane stephane   5049  3 oct 13:04 analyse_union_experts.py
-rw-------. 1 stephane
… [941 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Audit de l'append : tailles, hashes, jonction

- **bash** `{"command": "readlink -f . ; echo \"---\"; stat -c '%n %s %y' data/corpus_ocr_cegep/*.txt work/ocr/restants/train.txt 2>&1; echo \"--- SHA256\"; sha256sum data/corpus_ocr_cegep/train.txt data/corpus_ocr_cegep/val.txt data/corpus_ocr_cegep/test.txt work/ocr/restants/train.txt 2>&1", "description": "T … [49 caractères tronqués]`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
---
data/corpus_ocr_cegep/test.txt 10524 2026-11-02 18:06:52.133846441 -0500
data/corpus_ocr_cegep/train.txt 4486816 2026-11-04 15:49:10.655630317 -0500
data/corpus_ocr_cegep/val.txt 12536 2026-11-02 17:27:21.614829746 -0500
work/ocr/restants/train.txt 55857 2026-11-04 15:26:24.638730815 -0500
--- SHA256
111f79a4ede133e9e50e5057a8b7314820f48c8f750101b8917340dc259dffeb  data/corpus_ocr_cegep/train.txt
dd605833f27eab63df46de3437b1e74b479c2c3abcd6ea683365647063ccd0e1  data/corpus_ocr_cegep/val.txt
1c9ab73459c1e44ae7c1e23e46210091c54a5be360df698bdad150e9c1153b84  data/corpus_ocr_cegep/test.txt
ba4099c52bf26a75aca13f1e9b8144ce449003224874ee1dd60b556aa8887805  work/ocr/restants/train.txt
  ```

- **bash** `{"command": "echo \"=== tail 55857 sha\"; tail -c 55857 data/corpus_ocr_cegep/train.txt | sha256sum; echo \"=== work file sha\"; sha256sum work/ocr/restants/train.txt; echo \"=== offset 4430959 area\"; python3 - <<'EOF'\np='data/corpus_ocr_cegep/train.txt'\nwith open(p,'rb') as f:\n    d=f.read()\np … [274 caractères tronqués]`

  ```
=== tail 55857 sha
ba4099c52bf26a75aca13f1e9b8144ce449003224874ee1dd60b556aa8887805  -
=== work file sha
ba4099c52bf26a75aca13f1e9b8144ce449003224874ee1dd60b556aa8887805  work/ocr/restants/train.txt
=== offset 4430959 area
len 4486816
byte[4430959] b'Choquette c. Chagnon'
byte[4430958] b'\n'
byte[4430957] b'\n'
tail len 55857
  ```

### 🤖 Assistant

⏵ Vérification `cmp` de la queue et lecture des manifestes sources

- **bash** `{"command": "mkdir -p work/ocr/cegep64/controle && tail -c 55857 data/corpus_ocr_cegep/train.txt > work/ocr/cegep64/queue_55857.bin && cmp work/ocr/cegep64/queue_55857.bin work/ocr/restants/train.txt && echo \"CMP_OK identiques\"; echo \"--- tailles\"; stat -c '%n %s' work/ocr/cegep64/queue_55857.bi … [209 caractères tronqués]`

  ```
CMP_OK identiques
--- tailles
work/ocr/cegep64/queue_55857.bin 55857
work/ocr/restants/train.txt 55857
--- arithmetique
4486816 2031 4462978 582 57 64
  ```

- **bash** `{"command": "echo \"=== rapport restants\"; sed -n '1,80p' reports/rapport-ocr-pdf-restants.md 2>&1; echo \"=== manifeste restants\"; cat reports/ocr-pdf-restants.json 2>&1 | head -80", "description": "Lit le rapport et manifeste OCR des PDF restants"}`

  ```
=== rapport restants
# D — les 8 `.PDF` restants : 4 documents, 49 pages, 3 doublons — la limite est mesurée

> **Ligne de roadmap** : D · **Date** : 2026-11-04 · **Verdict** : ✅ **la limite nommée de D
> est close** — les **8 scans `.PDF`** (58 p) que `rglob("*.pdf")` manquait sont **OCRisés** en
> **90,1 s** ; ils ne donnent que **4 documents retenus** (49 p, **54 167 car.**, 8 736 mots,
> 9 tronçons de 8 Ko) : **6 fichiers uniques**, **5 textes distincts**, **3 copies** et **1
> formulaire de 210 car.** écartés. ⛔ **l'intégration au corpus CEGEP reste au hub** :
> `data/` est réservé par N2 et le split à 4 documents est vide en val/test.
>
> **Dispositif** : fonds `/home/stephane/Data13TB/stephane/archives/CEGEP`, 30 `.PDF`
> majuscules ; qualification au **texte natif intégral** (`pdftotext`, seuil 50 car/page) ;
> OCR `tools/ocr_pdf.py --liste` (tesseract 5.5.3 sans root, 300 dpi, fra+eng, 8 ouvriers)
> sur **cpu1** (claim `aeafe951/ocr-pdf-restants`) ; manifeste
> [`ocr-pdf-restants.json`](ocr-pdf-restants.json) ; texte brut dans `work/ocr/restants/`.

## 1. La qualification : 8 scans sur 30, et 22 `.PDF` natifs exclus

Les 30 `.PDF` (majuscules) du fonds, texte natif par pag
… [5691 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recalcul des statistiques du corpus et lecture du manifeste historique

- **bash** `{"command": "cat reports/ocr-pdf-cegep.json 2>&1 | head -120", "description": "Lit le manifeste historique du corpus CEGEP"}`

  ```
{
 "date": "2026-11-02",
 "ligne": "Données (R4.4 appliqué)",
 "nature": "corpus OCR des PDF scannés",
 "dispositif": {
  "ocr": "tesseract 5.5.3 sans root (work/ocr/root)",
  "langues": "fra+eng",
  "dpi": 300,
  "psm": 3,
  "pretraitement": "aucun (le R4.4 le fera)",
  "detection": "liste explicite de scans qualifiés sur le texte intégral",
  "liste": "work/ocr/scans-uniques.txt",
  "ouvriers": 8,
  "split": "hash salé du chemin : 5% val, 5% test",
  "deduplication": "documents + tronçons",
  "reprise_micropython": {
   "raison": "timeout pdftoppm (1 800 s) sur 359 pages au run principal",
   "dpi": 150,
   "pages": 359,
   "documents": 1,
   "temps_s": 1369.5
  }
 },
 "pdfs": 91,
 "scannes": 91,
 "ocrises": 60,
 "pages_ocr": 1982,
 "caracteres": 4408811,
 "troncons": 573,
 "documents": {
  "train": 53,
  "val": 4,
  "test": 3
 },
 "octets": {
  "train": 4430959,
  "val": 12536,
  "test": 10524
 },
 "temps_s": 7070.5,
 "echantillon": "---\ninscription AQPC\nAQPC- Confirmation d'inscription\n\n36e COLLOQUE ANNUEL DE L'AQPC\n\n8, 9 et 10 juin 2016\n\nVotre inscription est confirmée, sous réserve de validation par l'administration.\n\nCoordonnées\n\nParticipant\nNuméro de contact\n\
… [1524 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport hashlib, os\nbase='data/corpus_ocr_cegep'\ntot_chars=0; tot_bytes=0\nfor s in ('train','val','test'):\n    p=f'{base}/{s}.txt'\n    b=open(p,'rb').read()\n    t=b.decode('utf-8')\n    print(s, 'octets',len(b), 'chars',len(t), 'lignes', t.count(chr(10)), 'mots', … [407 caractères tronqués]`

  ```
train octets 4486816 chars 4443138 lignes 153115 mots 737181
val octets 12536 chars 12159 lignes 450 mots 1889
test octets 10524 chars 10355 lignes 234 mots 1990
TOTAL chars 4465652 octets 4509876
append octets 55857 chars 54249
ancien calc chars 4388889
  ```

### 🤖 Assistant

⏵ Écart sur le compte de caractères : inspection du script d'OCR pour la définition

- **bash** `{"command": "grep -n \"caracteres\\|troncon\\|pages_ocr\\|def .*split\\|train.txt\\|len(\" tools/ocr_pdf.py | head -80", "description": "Cherche le calcul des stats dans ocr_pdf.py"}`

  ```
93:        if ouvriers > 1 and len(pngs) > 1:
94:            with ThreadPoolExecutor(max_workers=min(ouvriers, len(pngs))) as ex:
98:        return "\n".join(textes).strip(), len(textes)
107:def troncons(t: str, taille: int):
109:    while debut < len(t):
110:        fin = min(debut + taille, len(t))
111:        if fin < len(t):
150:    vus, vus_troncons = set(), set()
151:    stats = {"pdfs": 0, "scannes": 0, "ocrises": 0, "pages_ocr": 0, "caracteres": 0,
152:             "troncons": 0, "documents": {"train": 0, "val": 0, "test": 0},
166:        stats["racines"].append({"nom": lib, "chemin": racine.as_posix(), "pdfs": len(pdfs), "licence": lic})
178:                if len(t.strip()) / max(npages, 1) >= 50:
182:            if len(texte) < args.min_chars:
192:            for m in troncons(doc, args.chunk):
195:                    if mq in vus_troncons:
197:                    vus_troncons.add(mq)
204:            stats["pages_ocr"] += n
205:            stats["troncons"] += len(morceaux)
206:            stats["caracteres"] += len(texte)
209:            print(f"  {lib} · {pdf.name[:40]} · {n} p · {len(texte)} car", flush=True)
213:    stats["mots_estimes"] = int(stats["caracteres"] / 6
… [100 caractères tronqués]
  ```

- **bash** `{"command": "ls work/ocr/ 2>&1; echo \"---\"; ls work/ocr/restants/ 2>&1; echo \"--- scripts ocr\"; ls tools/ | grep -i ocr", "description": "Inventaire des artefacts OCR"}`

  ```
ajoute_micro.py
cegep64
census-cegep.json
census_cegep.py
detecte_cegep.py
detection-cegep.json
fait_fiche.py
fiche-cegep.md
micro-manifest.json
micro.txt
pages
restants
restants-pdf.liste
root
rpm
run-cegep-02.log
run-micro.log
scans-restants.txt
scans-uniques2.txt
scans-uniques.json
scans-uniques.txt
scans-upper.txt
---
test.txt
train.txt
val.txt
--- scripts ocr
graphe_document_ocr.py
installer_ocr.sh
mesurer_ocr.py
ocr_pdf.py
porte-ocr-scans.sh
porte-ocr.sh
  ```

- **bash** `{"command": "sed -n '100,260p' tools/ocr_pdf.py", "description": "Lit la logique de tronçons, split et écriture"}`

  ```
shutil.rmtree(tmp, ignore_errors=True)


def empreinte(t: str, taille: int = 16) -> str:
    return hashlib.blake2b(t.encode("utf-8"), digest_size=taille).hexdigest()


def troncons(t: str, taille: int):
    debut = 0
    while debut < len(t):
        fin = min(debut + taille, len(t))
        if fin < len(t):
            coupe = t.rfind(" ", debut + taille // 2, fin)
            if coupe > debut:
                fin = coupe
        m = t[debut:fin].strip()
        if m:
            yield m
        debut = fin


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-doc", type=int, default=0)
    ap.add_argument("--racine", default="", help="restreindre à une racine : Biblio_large, CEGEP")
    ap.add_argument("--deja", type=int, default=0, help="sauter les N premiers PDF examinés (reprise)")
    ap.add_argument("--liste", type=pathlib.Path, default=None,
                    help="fichier de chemins PDF : OCR sans détection (scans déjà qualifiés)")
    ap.add_argument("--ouvriers", type=int, default=1,
                    help="pages OCR en parallèle (tesseract forcé mono-thread)")
    ap.add_argument("--dpi", type=int, default=300)
    ap
… [5800 caractères tronqués]
  ```

