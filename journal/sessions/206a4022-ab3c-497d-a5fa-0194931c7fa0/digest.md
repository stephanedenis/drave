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

### 🤖 Assistant

⏵ Inspection du script de contamination et de ses options

- **bash** `{"command": "python3 tools/verifie_contamination.py --help 2>&1; echo \"=== exit $?\"", "description": "Aide du script de contamination"}`

  ```
usage: verifie_contamination.py [-h] --train TRAIN [--val VAL] [--test TEST]
                                [--eval EVAL] [--fenetre FENETRE] [--pas PAS]
                                [--echantillon ECHANTILLON]
                                [--taille-troncon TAILLE_TRONCON]
                                [--sortie SORTIE]

verifie_contamination.py — les fuites entre splits et entre corpus, mesurées.
POURQUOI CE FICHIER. Un corpus d'entraînement sans contrôle de fuite est un
corpus qui mentira sur son évaluation. Ce script vérifie deux choses, avec des
chiffres : 1. **les doublons de tronçons entre splits** : chaque ligne des
fichiers (tronçon de 8 Ko écrit par `corpus_wikipedia.py`) est hachée ; un
tronçon qui apparaît dans deux splits est une fuite exacte (les quasi-doublons
ne sont pas détectés — c'est dit). Pour le **texte intégral**
(`corpus_wikipedia_texte.py`), l'unité est la **fenêtre** de 8 Ko coupée au
mot (`--taille-troncon 8192`), parce que les tronçons contiennent des retours
à la ligne ; 2. **le recouvrement avec les jeux d'évaluation** : des fenêtres
de `--fenetre` octets, échantillonnées dans chaque fichier d'évaluation, sont
cherchées dans l'entraînement par 
… [748 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' tools/verifie_contamination.py", "description": "Lecture du script de contamination"}`

  ```
#!/usr/bin/env python3
"""verifie_contamination.py — les fuites entre splits et entre corpus, mesurées.

POURQUOI CE FICHIER. Un corpus d'entraînement sans contrôle de fuite est un corpus qui mentira
sur son évaluation. Ce script vérifie deux choses, avec des chiffres :

1. **les doublons de tronçons entre splits** : chaque ligne des fichiers (tronçon de 8 Ko écrit
   par `corpus_wikipedia.py`) est hachée ; un tronçon qui apparaît dans deux splits est une fuite
   exacte (les quasi-doublons ne sont pas détectés — c'est dit). Pour le **texte intégral**
   (`corpus_wikipedia_texte.py`), l'unité est la **fenêtre** de 8 Ko coupée au mot
   (`--taille-troncon 8192`), parce que les tronçons contiennent des retours à la ligne ;
2. **le recouvrement avec les jeux d'évaluation** : des fenêtres de `--fenetre` octets,
   échantillonnées dans chaque fichier d'évaluation, sont cherchées dans l'entraînement par
   `mmap.find` — une fenêtre trouvée est une fuite.

Ce n'est pas un détecteur de paraphrase : deux textes reformulés passent. C'est un contrôle
d'**exactitude**, celui qui doit être à zéro avant d'entraîner.

Usage :
  python3 tools/verifie_contamination.py --train data/corpus_wiki_fr/tr
… [4851 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des traces de l'append et lancement de la contamination réelle

- **bash** `{"command": "ls -lat work/ | head -15; echo \"=== work/ocr récent\"; ls -lat work/ocr/ | head -15; echo \"=== git status court\"; git status --short | head -30; echo \"=== suivi data\"; git ls-files data/corpus_ocr_cegep/ ; echo \"=== gitignore\"; grep -n \"data\\|work\" .gitignore", "description":  … [30 caractères tronqués]`

  ```
total 220
drwxr-xr-x. 1 stephane stephane   596  4 nov 15:56 ocr
drwxr-xr-x. 1 stephane stephane  1422  4 nov 15:30 .
-rw-r--r--. 1 stephane stephane   393  4 nov 15:30 ressources.json
drwxr-xr-x. 1 stephane stephane 10116  4 nov 15:26 n2ac
drwxr-xr-x. 1 stephane stephane   768  4 nov 11:32 portes-n3-cloture
drwxr-xr-x. 1 stephane stephane    76  4 nov 08:44 pensee
drwxr-xr-x. 1 stephane stephane   244  4 nov 08:07 portes
-rw-r--r--. 1 stephane stephane   556  3 nov 18:43 msg-claims.txt
-rw-r--r--. 1 stephane stephane   801  3 nov 18:40 msg-nuit.txt
-rw-r--r--. 1 stephane stephane   454  3 nov 13:36 msg-cpt.txt
-rw-r--r--. 1 stephane stephane   640  3 nov 13:34 msg-backlog-n2.txt
-rw-r--r--. 1 stephane stephane   554  3 nov 13:31 msg-1335.txt
-rw-r--r--. 1 stephane stephane   696  3 nov 13:29 msg-n2-sous25.txt
-rw-r--r--. 1 stephane stephane   652  3 nov 13:18 msg-80-2.txt
=== work/ocr récent
total 1532
drwxr-xr-x. 1 stephane stephane     46  4 nov 15:56 cegep64
drwxr-xr-x. 1 stephane stephane    596  4 nov 15:56 .
drwxr-xr-x. 1 stephane stephane   1422  4 nov 15:30 ..
drwxr-xr-x. 1 stephane stephane     48  4 nov 15:24 restants
-rw-r--r--. 1 stephane stephane   1148  4 nov 15:24 r
… [1361 caractères tronqués]
  ```

- **bash** `{"command": "taskset -c 10-19,30-39 python3 tools/verifie_contamination.py --train data/corpus_ocr_cegep/train.txt --val data/corpus_ocr_cegep/val.txt --test data/corpus_ocr_cegep/test.txt --taille-troncon 8192 --sortie work/ocr/cegep64/contamination.json; echo \"=== exit $?\"", "description": "Cont … [47 caractères tronqués]`

  ```
{
 "train": "data/corpus_ocr_cegep/train.txt",
 "doublons_entre_splits": {
  "train_troncons": 14205,
  "par_split": {
   "val.txt": {
    "troncons": 207,
    "doublons": 131,
    "taux": 0.63285
   },
   "test.txt": {
    "troncons": 69,
    "doublons": 0,
    "taux": 0.0
   }
  }
 },
 "recouvrement_eval": [],
 "taille_troncon": 8192,
 "doublons_entre_splits_troncon": {
  "train_troncons": 546,
  "par_split": {
   "val.txt": {
    "troncons": 4,
    "doublons": 0,
    "taux": 0.0
   },
   "test.txt": {
    "troncons": 2,
    "doublons": 0,
    "taux": 0.0
   }
  }
 }
}
=== exit 0
  ```

### 👤 Utilisateur

Agent aeafe951-9c3d-4bb5-8af7-0246a4f3d51d sent a message: 
STOP — la prémisse « 4 nouveaux documents » est fausse, et je viens de le mesurer. Ne conclus pas « 64 documents ». Voici la preuve indépendante, à rejouer toi-même avant de l'écrire :

- `train[:4_430_959]` (l'ancien train, hash `6d53a023…` du manifeste) contient déjà une grande partie du texte ajouté : **25 fenêtres exactes de 500 octets sur 56** (pas de 1 000) du bloc ajouté s'y retrouvent ; un exemple à `new[30000:30500]` == `old[3999195:3999695]` (« Fiche de travail — Offres d'emploi ») ; « Choquette » apparaît **7 fois** dans l'ancien train ; sur 200 fenêtres aléatoires de 200 o, **101** sont dans l'ancien train.
- Interprétation : les 4 documents OCRisés depuis les `.PDF` majuscules sont, au moins en grande partie, des **doublons** de documents déjà présents dans les 60 (mêmes contenus sous des copies `.pdf` minuscules), que la déduplication par hash de document entier n'a pas vus parce que l'OCR diffère légèrement.

NOUVELLE MISSION (même périmètre de fichiers, mêmes interdits — `data/` en lecture seule, aucun commit, pas de docs/pilotage) :
1. Quantifie le doublon **par document** : ré-OCRise les 8 `.PDF` un par un (`tools/ocr_pdf.py` fonctions `ocr`/`pages`, ou `--liste` vers `work/ocr/cegep64/par-doc/`), puis pour chacun des 5 textes distincts, mesure la fraction de fenêtres de 500 o (pas 1 000) présentes dans `train[:4_430_959]` et dans val/test. Donne le tableau par document.
2. Prépare `work/ocr/cegep64/train_restaure.txt` = les **4 430 959 premiers octets** de `data/corpus_ocr_cegep/train.txt` ; vérifie que son SHA-256 vaut `6d53a023db1ab7aaa93608c0995bbe40fb37524a8f74f53f86951fa7ada77310` (le hash du manifeste). Ne touche pas à `data/`.
3. Fais quand même le contrôle 8 Ko **entre splits** (train complet vs val/test) + le contrôle négatif (fenêtre de val injectée dans une copie du train doit être trouvée). Mais le résultat principal est le **doublon intra-train** : le contrôle 8 Ko entre splits peut être à 0 et ne pas voir le problème.
4. Écris les deux livrables avec le verdict honnête : l'append est un **doublon** ; le corpus ne gagne pas 4 documents ; l'état « 64 documents » n'est pas soutenu ; la restauration (retirer les 55 857 octets ajoutés) est la décision à proposer au hub, avec le hash restauré. La fiche `reports/rapport-ocr-cegep-64.md` doit porter ce verdict, pas « intégration réussie ».
5. Si ton contrôle par document contredit le mien (par exemple duplication faible < 10 %), dis-le explicitement et donne les chiffres — c'est le désaccord qui compte, pas la confirmation.

Rapport final : mêmes 10 lignes, avec la **ligne d'état exacte** proposée au hub (elle doit dire « doublon, restauration proposée », pas « 64 documents »).

### 🤖 Assistant

⏵ Rejeu de la mesure du parent : fenêtres du bloc ajouté dans l'ancien train

- **bash** `{"command": "python3 - <<'EOF'\nimport mmap, random, hashlib\np='data/corpus_ocr_cegep/train.txt'\nd=open(p,'rb').read()\nold, new = d[:4430959], d[4430959:]\nprint('old',len(old),'new',len(new))\nprint('sha old',hashlib.sha256(old).hexdigest())\n# fenetres 500, pas 1000\npos=list(range(0,len(new)-5 … [914 caractères tronqués]`

  ```
old 4430959 new 33988
sha old 6d53a023db1ab7aaa93608c0995bbe40fb37524a8f74f53f86951fa7ada77310
fenetres 500/1000: 34
trouvees 24 / 34 0.706
exemples [(8000, 3999064), (9000, 4000064), (10000, 4001064)]
exemple 30000: False
Choquette old 7 new 1
200o trouvees 149 /200 = 0.745
  ```

- **bash** `{"command": "head -c 4430959 data/corpus_ocr_cegep/train.txt > work/ocr/cegep64/train_restaure.txt && sha256sum work/ocr/cegep64/train_restaure.txt && stat -c '%n %s' work/ocr/cegep64/train_restaure.txt; echo \"=== attendu 6d53a023db1ab7aaa93608c0995bbe40fb37524a8f74f53f86951fa7ada77310\"", "descrip … [67 caractères tronqués]`

  ```
6d53a023db1ab7aaa93608c0995bbe40fb37524a8f74f53f86951fa7ada77310  work/ocr/cegep64/train_restaure.txt
work/ocr/cegep64/train_restaure.txt 4430959
=== attendu 6d53a023db1ab7aaa93608c0995bbe40fb37524a8f74f53f86951fa7ada77310
  ```

### 🤖 Assistant

⏵ Alerte : la taille lue du train ne correspond plus — vérification immédiate

- **bash** `{"command": "date -Is; stat -c '%n %s %y' data/corpus_ocr_cegep/train.txt; sha256sum data/corpus_ocr_cegep/train.txt; echo \"=== tail sha\"; tail -c 55857 data/corpus_ocr_cegep/train.txt | sha256sum; echo \"=== python len\"; python3 -c \"d=open('data/corpus_ocr_cegep/train.txt','rb').read(); print(l … [184 caractères tronqués]`

  ```
2026-11-04T15:59:01-05:00
data/corpus_ocr_cegep/train.txt 4464947 2026-11-04 15:57:00.342307238 -0500
661e6386fb09ca333778e37dfdff8badd55135ea014d04975714ab8cc445458d  data/corpus_ocr_cegep/train.txt
=== tail sha
03c616b4d1ec5f35550a538e177c11ce82db0b108c6844808fbc5ddac9bd1a2e  -
=== python len
4464947
b'Choquette c. Chagnon\nCANADA\n\nPR'
=== git?
total 4412
drwxr-xr-x. 1 stephane stephane      48  2 nov 16:31 .
drwxr-xr-x. 1 stephane stephane    2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane   12711  4 nov 15:57 test.txt
-rw-r--r--. 1 stephane stephane 4464947  4 nov 15:57 train.txt
-rw-r--r--. 1 stephane stephane   32220  4 nov 15:57 val.txt
  ```

### 🤖 Assistant

⏵ `data/` a changé pendant la session (15:57) — j'identifie l'auteur et l'état

- **bash** `{"command": "date -Is; ps -eo pid,lstart,cmd | grep -E \"ocr_pdf|contamination|python3\" | grep -v grep | tail -20; echo \"=== ouverts\"; (command -v lsof >/dev/null && lsof data/corpus_ocr_cegep/train.txt 2>/dev/null) || echo \"lsof absent/rien\"; echo \"=== fichiers work recents <10min\"; find wor … [149 caractères tronqués]`

  ```
2026-11-04T15:59:31-05:00
   2062 mar nov  3 19:34:00 2026 /usr/bin/python3.13 /usr/sbin/firewalld --nofork --nopid
   2233 mar nov  3 19:34:01 2026 /usr/bin/python3.13 /usr/bin/fail2ban-server -xf start
   3002 mar nov  3 19:34:05 2026 /usr/bin/python3 /home/stephane/.local/share/pipewire-eq/eqdaemon.py
 268346 mer nov  4 09:45:22 2026 python3 serveur.py --port 8765
=== ouverts
lsof absent/rien
=== fichiers work recents <10min
1793825800.5041941730 work/ocr/cegep64/queue_55857.bin 55857
1793825906.6550946740 work/ocr/cegep64/contamination.json 578
1793825931.3719418120 work/ocr/cegep64/train_restaure.txt 4430959
1793825951.4950571470 work/n2ac/rope2048-10k.log 2413
  ```

- **bash** `{"command": "for f in data/corpus_ocr_cegep/*.txt; do echo \"$f $(stat -c %s $f) $(tail -c 120 $f | tr '\\n' '|')\"; done; echo \"=== tete val/test\"; head -c 150 data/corpus_ocr_cegep/val.txt; echo; echo \"---\"; head -c 150 data/corpus_ocr_cegep/test.txt", "description": "Que contiennent les nouve … [17 caractères tronqués]`

  ```
data/corpus_ocr_cegep/test.txt 12711 réal, ce 25 juin 2013||y Représentant autorisé|#|F a||a °||Courtiers d'assurances internationaux|www. BFLCANADA.ca||
data/corpus_ocr_cegep/train.txt 4464947 rôler votre travail||© 2013 Cisco et/ou ses filiales. Tous droits réservés. Ce document contient des informations pu
data/corpus_ocr_cegep/val.txt 32220 cteur de contrôler votre travail||© 2013 Cisco et/ou ses filiales. Tous droits réservés. Ce document contient des in
=== tete val/test
inscription AQPC
AQPC- Confirmation d'inscription

36e COLLOQUE ANNUEL DE L'AQPC

8, 9 et 10 juin 2016

Votre inscription est confirmée, sous réserv
---
2.8寸ILI9341 TFTLCD尺寸图（钢化玻璃TP）
Customer Approved LES HE W À De | HM
(AP ATES)
50.00(Outline)
49.60(TP) — 0.20 0
10S 46.00(TP V.A
  ```

### 🤖 Assistant

⏵ Alerte envoyée au parent, puis préparation de l'OCR par document

- **send_message** `{"agent_id": "aeafe951-9c3d-4bb5-8af7-0246a4f3d51d", "message": "ALERTE data/ modifié pendant la session (pas par moi, rien écrit dans data/). À 15:57:00, data/corpus_ocr_cegep/ n'est plus l'état 15:49 : train 4 486 816→4 464 947 o (SHA 661e6386…), val 12 536→32 220 o, test 10 524→12 711 o. Le préfi … [837 caractères tronqués]`

  ```
message delivered to agent aeafe951-9c3d-4bb5-8af7-0246a4f3d51d
  ```

- **bash** `{"command": "sed -n '1,99p' tools/ocr_pdf.py; echo \"=== liste\"; cat work/ocr/restants-pdf.liste", "description": "Lecture des constantes et fonctions OCR, liste des PDF"}`

  ```
#!/usr/bin/env python3
"""ocr_pdf.py — l'OCR des PDF **scannés** (R4.4 appliqué aux documents réels).

POURQUOI. `extrait_pdf.py` extrait le texte natif ; les PDF sans couche texte (les scans) sont
comptés et écartés. Ce script les **océrise** avec le tesseract installé sans root par
`installer_ocr.sh` (5.5.3, fra+eng) : `pdftoppm` rend les pages, `tesseract` les lit.

Ce qu'il ne fait pas (encore) : le prétraitement d'image de R4.4 (`nettoyer_scan.py` : rotation,
contraste, colonnes) — le pilote mesure l'OCR **brut** ; la WER réelle n'a pas de vérité terrain
(seule la parité R4.4 sur scans simulés la donne), donc la fiche donne le débit, les caractères et
un échantillon, pas une WER inventée.

Usage :
  python3 tools/ocr_pdf.py --max-doc 20          # pilote (les 20 premiers scannés)
  python3 tools/ocr_pdf.py                       # tous les scannés des racines
  python3 tools/ocr_pdf.py --liste scans.txt --ouvriers 8
      # liste explicite de scans déjà qualifiés (détection intégrale), pages en parallèle

DÉTECTION. Sans `--liste`, un PDF est « scanné » si ses **deux premières pages** portent moins de
50 caractères natifs par page. Mesure du 02/11 sur le fonds CEGEP : 807 candi
… [4239 caractères tronqués]
  ```

### 👤 Utilisateur

Agent aeafe951-9c3d-4bb5-8af7-0246a4f3d51d sent a message: 
CORRECTION IMPORTANTE — ignore mon message précédent sur le « doublon » : c'était un artefact de lecture pendant une réécriture. Le hub a réécrit le corpus à 15 h 57 (re-split 2/1/1) **pendant** que je mesurais ; j'ai comparé la queue du nouveau train avec son propre milieu, d'où les fenêtres qui se ressemblaient.

État stable à mesurer (ne lis que celui-là, vérifie taille + mtime avant/après chaque mesure) :
- `train.txt` 4 464 947 o, `val.txt` 32 220 o, `test.txt` 12 711 o (mtime 15:57:00) ;
- **les anciens splits sont préservés au préfixe, hashes du manifeste** : train[:4 430 959] = `6d53a023…`, val[:12 536] = `dd605833…`, test[:10 524] = `1c9ab734…` — je l'ai vérifié, refais-le ;
- répartition annoncée par le hub : **Choquette 7 575 + DOC1 25 470 → train ; DOC2 19 101 → val ; Assurance 2 021 → test**.

Mission corrigée :
1. Vérifie les trois préfixes (hashes ci-dessus) : c'est la preuve que le re-split n'a pas touché l'ancien corpus.
2. Vérifie la répartition : les suffixes ajoutés à chaque split doivent correspondre aux textes OCR des documents (ré-OCRise un par un dans `work/ocr/cegep64/par-doc/`, compare par fenêtres de 500 o ; les textes doivent se retrouver **dans le split annoncé**, pas dans un autre).
3. Contrôle 8 Ko **entre splits** sur les fichiers 15:57 (train vs val vs test), avec le contrôle négatif (fenêtre de val injectée dans une copie du train → doit être trouvée).
4. Contrôle de non-duplication croisée : pour chaque nouveau document, vérifie qu'il ne duplique pas le préfixe d'un **autre** split (fenêtres exactes de 500 o). Si un nouveau doc de val/test duplique l'ancien train, c'est une fuite — dis-le avec les offsets.
5. Écris les deux livrables avec le verdict vrai : re-split 2/1/1, anciens splits intacts, contamination 8 Ko = X (chiffre), contrôle négatif OK/KO. La fiche doit aussi noter que le manifeste `ocr-pdf-restants.json` disait « 4 en train » : le re-split du hub le remplace (2/1/1), c'est la version à retenir.
6. Ligne d'état proposée : corpus CEGEP 64 documents, re-split 2/1/1, anciens splits intacts, 8 Ko 0 (ou le chiffre vrai).

Timebox inchangée. Si tu as déjà écrit une fiche avec « doublon », corrige-la.

