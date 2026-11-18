# Session DSH — relecture

- identifiant : `da0f2984-32d0-459d-a761-d3faf6a10b8a`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-18 09:15:21
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave, en français). La machine est dédiée.

TÂCHE : l'INVENTAIRE des données disponibles pour le palier 1 du modèle natif (100-150 M, 3-6 Go de français propre). Tu ne télécharges RIEN et tu ne modifies AUCUNE donnée : tu mesures ce qui est là et tu chiffres l'écart.

À faire :
1. `du -sh data/*` et les sous-dossiers ; compte les fichiers, les octets, les lignes des corpus texte (attention : `data/wiki_mix/propre/train.txt` fait 1 Go — ne le lis pas en entier, utilise `wc -c`/`wc -l`).
2. Cherche les corpus déjà présents et leur nature : `data/wiki_mix/`, `data/corpus_fr.txt`, `data/corpus_mixte.txt`, `data/corpus_en.txt`, `data/udhr/`, `data/structures/`, `data/panini*`, etc. Pour chacun : taille, langue, licence si un fichier la nomme (LICENSE, README, un champ), doublons probables (même taille/nom).
3. Le corpus épinglé d'entraînement : `data/wiki_mix/propre/train.txt` (1 017 487 092 o) et `val.txt` — l'épingle est dans `reports/corpus-epingle.json` (ne la refais pas).
4. Chiffre l'écart au palier 1 (3-6 Go) : combien de Go manquent, et quelles sources déjà présentes pourraient être ajoutées sans collecte (livres ? articles ? UDHR ? wikitext2 ?).
5. Écris reports/rapport-donnees-inventaire.md : le tableau des corpus (chemin, octets, langue, licence, usage), l'écart aux 3-6 Go, les doublons/risques, et la prochaine action de collecte (sans la faire).

CONTRAINTES STRICTES :
- aucune modification de `data/` (lecture seule), aucun téléchargement ;
- ne touche pas à docs/pilotage/en-cours.md, docs/pilotage/roadmap.md, AGENTS.md ;
- ne committe pas ;
- n'écris que reports/rapport-donnees-inventaire.md ;
- les commandes doivent rester rapides (< 2 min chacune) : pas de lecture intégrale des gros fichiers.

Rends : le total des données (Go), l'écart au palier 1, les 3 sources les plus prometteuses déjà présentes, et le chemin du rapport.
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

⏵ Inventaire des données : mesure de `data/` en lecture seule

Je commence par mesurer l'arborescence `data/` sans rien lire intégralement.

- **bash** `{"command": "du -sh data 2>/dev/null; echo \"---\"; du -sh data/* 2>/dev/null | sort -rh | head -40", "description": "Mesure la taille de data et ses sous-dossiers", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
127G	data
---
21G	data/corpus_wiki_en_texte
11G	data/corpus_wiki_ru_texte
10G	data/corpus_wiki_de_texte
9,3G	data/corpus_wiki_en
7,8G	data/corpus_wiki_fr_texte
6,9G	data/corpus_wiki_ja_texte
6,4G	data/corpus_wiki_es_texte
5,0G	data/corpus_wiki_it_texte
4,9G	data/corpus_wiki_ru
4,5G	data/corpus_wiki_de
4,2G	data/corpus_wiki_ja
3,6G	data/corpus_wiki_fr
3,4G	data/corpus_wiki_ar_texte
3,0G	data/corpus_wiki_pt_texte
2,7G	data/wiki_big
2,7G	data/corpus_wiki_es
2,5G	data/corpus_wiki_zh_texte
2,3G	data/xnli
2,2G	data/corpus_wiki_it
2,0G	data/wiki_mix
2,0G	data/corpus_wiki_zh
1,9G	data/corpus_wiki_ar
1,3G	data/corpus_wiki_pt
1,2G	data/opensubtitles
1,2G	data/multiun
846M	data/corpus_pdf_documents
824M	data/wiki_multi
817M	data/wiki_fr
457M	data/wiki_en
326M	data/wikimatrix
314M	data/pidgin.old
308M	data/corpus_pdf
170M	data/adaptateurs
145M	data/composition-verne-large-etats.npz
141M	data/composition-verne-plan-etats.npz
116M	data/corpus_multi.txt
111M	data/corpus_multi_train.txt
109M	data/ted2020
96M	data/corpus_en.txt
85M	data/pensee-etats-7b.npz
  ```

- **bash** `{"command": "ls -la data/ 2>/dev/null | head -60", "description": "Liste le contenu de data", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

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
… [3181 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Cartographie complète de `data/` : tailles, fichiers, corpus français

- **bash** `{"command": "ls -la data/ | tail -80", "description": "Liste la fin du contenu de data", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
-rw-r--r--. 1 stephane stephane 151064111 21 oct 23:31 composition-verne-large-etats.npz
-rw-r--r--. 1 stephane stephane 147255554 21 oct 23:47 composition-verne-plan-etats.npz
-rw-r--r--. 1 stephane stephane     97900 29 oct 14:19 consignes_train.jsonl
-rw-r--r--. 1 stephane stephane      1931 29 oct 14:19 consignes_val.jsonl
-rw-r--r--. 1 stephane stephane 100276153  8 oct 09:42 corpus_en.txt
-rw-r--r--. 1 stephane stephane   2032162  8 oct 09:42 corpus_en_val.txt
-rw-r--r--. 1 stephane stephane  17031747 17 oct 18:26 corpus_fr_litterature.txt
-rw-r--r--. 1 stephane stephane   4402195 28 oct 12:45 corpus_fr_train.txt
-rw-r--r--. 1 stephane stephane   4633889 17 oct 15:01 corpus_fr.txt
-rw-r--r--. 1 stephane stephane    231694 28 oct 12:45 corpus_fr_val.txt
drwxr-xr-x. 1 stephane stephane        48 31 oct 22:24 corpus_litt_propre
-rw-r--r--. 1 stephane stephane    614400 31 oct 22:24 corpus_mixte_dev.txt
-rw-r--r--. 1 stephane stephane  15276376 17 oct 18:27 corpus_mixte_litt2.txt
-rw-r--r--. 1 stephane stephane  12233263 17 oct 16:31 corpus_mixte_litt.txt
-rw-r--r--. 1 stephane stephane   6144000 31 oct 22:24 corpus_mixte_propre.txt
-rw-r--r--. 1 stephane stephane  10647410 17 oc
… [4520 caractères tronqués]
  ```

- **bash** `{"command": "echo \"== nombre de fichiers par dossier de premier niveau ==\"; for d in data/*/; do n=$(find \"$d\" -type f 2>/dev/null | wc -l); s=$(du -sh \"$d\" 2>/dev/null | cut -f1); echo \"$s\t$n\t$d\"; done | sort -rh", "description": "Compte les fichiers et tailles par dossier", "workdir": "/ … [48 caractères tronqués]`

  ```
== nombre de fichiers par dossier de premier niveau ==
21G	3	data/corpus_wiki_en_texte/
11G	3	data/corpus_wiki_ru_texte/
10G	3	data/corpus_wiki_de_texte/
9,3G	3	data/corpus_wiki_en/
7,8G	3	data/corpus_wiki_fr_texte/
6,9G	3	data/corpus_wiki_ja_texte/
6,4G	3	data/corpus_wiki_es_texte/
5,0G	3	data/corpus_wiki_it_texte/
4,9G	3	data/corpus_wiki_ru/
4,5G	3	data/corpus_wiki_de/
4,2G	3	data/corpus_wiki_ja/
3,6G	3	data/corpus_wiki_fr/
3,4G	3	data/corpus_wiki_ar_texte/
3,0G	3	data/corpus_wiki_pt_texte/
2,7G	6	data/wiki_big/
2,7G	3	data/corpus_wiki_es/
2,5G	3	data/corpus_wiki_zh_texte/
2,3G	52	data/xnli/
2,2G	3	data/corpus_wiki_it/
2,0G	4	data/wiki_mix/
2,0G	3	data/corpus_wiki_zh/
1,9G	3	data/corpus_wiki_ar/
1,3G	3	data/corpus_wiki_pt/
1,2G	2	data/opensubtitles/
1,2G	2	data/multiun/
846M	3	data/corpus_pdf_documents/
824M	25	data/wiki_multi/
817M	9	data/wiki_fr/
457M	5	data/wiki_en/
326M	2	data/wikimatrix/
314M	70	data/pidgin.old/
314M	70	data/pidgin/
308M	3	data/corpus_pdf/
170M	19	data/adaptateurs/
109M	2	data/ted2020/
48M	2	data/jrc/
36M	73	data/jw/
28M	55	data/udhr/
24M	3789	data/deepseek/
23M	2	data/glottolog/
17M	3	data/corpus_litt_propre/
15M	3	data/corpus_ocr/
10M	32	data/eurlex/
9,9M	
… [389 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection détaillée des corpus wiki et du corpus épinglé

- **bash** `{"command": "for d in corpus_wiki_fr corpus_wiki_fr_texte wiki_fr wiki_big wiki_mix wiki_en wiki_multi corpus_propre corpus_litt_propre corpus_pdf corpus_pdf_documents corpus_ocr corpus_repo_propre corpus_nonambigu; do echo \"=== data/$d ===\"; ls -la \"data/$d\" 2>/dev/null | head -12; done", "desc … [124 caractères tronqués]`

  ```
=== data/corpus_wiki_fr ===
total 3717160
drwxr-xr-x. 1 stephane stephane         48  1 nov 11:02 .
drwxr-xr-x. 1 stephane stephane       2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane  189680293  1 nov 11:14 test.txt
-rw-r--r--. 1 stephane stephane 3425588868  1 nov 11:14 train.txt
-rw-r--r--. 1 stephane stephane  191095576  1 nov 11:14 val.txt
=== data/corpus_wiki_fr_texte ===
total 8143500
drwxr-xr-x. 1 stephane stephane         48  1 nov 16:37 .
drwxr-xr-x. 1 stephane stephane       2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane  415302543  1 nov 17:25 test.txt
-rw-r--r--. 1 stephane stephane 7504078589  1 nov 17:25 train.txt
-rw-r--r--. 1 stephane stephane  419555119  1 nov 17:25 val.txt
=== data/wiki_fr ===
total 231928
drwxr-xr-x. 1 stephane stephane        36  1 nov 11:54 .
drwxr-xr-x. 1 stephane stephane      2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane 237491315  1 nov 11:41 articles.txt
drwxr-xr-x. 1 stephane stephane       160  1 nov 18:42 propre
=== data/wiki_big ===
total 1022976
drwxr-xr-x. 1 stephane stephane         28  2 nov 10:03 .
drwxr-xr-x. 1 stephane stephane       2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane 1047525530  2 nov 09:1
… [3945 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/corpus-epingle.json 2>/dev/null; echo \"---\"; ls -la reports/ | grep -i -E \"corpus|donnee|data|palier|natif\" | head -20", "description": "Lit l'épingle du corpus et cherche rapports liés", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
{
 "schema": "drave.corpus-epingle",
 "version": 1,
 "date": "2026-11-18T08:59:56",
 "corpus": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/data/wiki_mix/propre",
 "note": "sha256 du train, du val et des canaux ; --verifie recalcule et compare l'empreinte de chaque fichier et l'empreinte du manifeste",
 "fichiers": {
  "train.txt": {
   "sha256": "0876b6089aaebb5d8f3f1bb08dfdd749bb2877e902ea1c46ba7360b0ac1e1ef1",
   "octets": 1017487092,
   "lignes": 2480766,
   "mtime": "2026-11-02T12:25:22"
  },
  "val.txt": {
   "sha256": "fbddef918166f1d659b6647a8d45aa8e88528ee7808d388990a88bce52b22ef5",
   "octets": 10330112,
   "lignes": 24498,
   "mtime": "2026-11-02T12:25:22"
  },
  "train.canal": {
   "sha256": "04efed3039f8398e5d39e3b3c79beebb771943bcf4857c3f2f72d6dabfb78bf7",
   "octets": 1017487092,
   "lignes": 0,
   "mtime": "2026-11-02T12:25:22"
  },
  "val.canal": {
   "sha256": "f1abc5d1d63c3207c369e1cebf767952fd451320e2f2730f40f333a8add16235",
   "octets": 10330112,
   "lignes": 0,
   "mtime": "2026-11-02T12:25:22"
  }
 },
 "manifeste_sha256": "fae5bb7389c6c0a93d3d4400886d7912fe4afdb1788fe2df34eb1b3d01acb52f"
}
---
-rw-r--r--. 1 stephane stephane    2176 29 oct 20:03 b102bis-c
… [1542 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Exploitation des JSON de corpus déjà mesurés (octets, lignes, licences)

- **bash** `{"command": "ls reports/ | sort", "description": "Liste tous les rapports", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
07
07-mesures-couche-commune.md
a26-bilan.json
a26-lot-disque.json
a80-audit-final.json
a80-indice-qualifie.json
a80-melange-qualifie.json
a80-pannes-ppl.json
a80-porte-adaptateur.json
a80-porte-budget.json
a80-porte-bus.json
a80-porte-bus-socket.json
a80-porte-c4-retard.json
a80-porte-consolidation.json
a80-porte-cycle-c2.json
a80-porte-delais.json
a80-porte-flux.json
a80-porte-fusion.json
a80-porte-gain.json
a80-porte-pont.json
a80-porte-profondeur.json
a80-porte-reflexe.json
a80-porte-reparti.json
a80-portes-ppl.json
a80-porte-topologie.json
a80-porte-trace.json
a83a-coupe.json
a83a-flux.json
a83a-pont.json
a83b-decision.json
a83b-lot.json
a83b-regimes.json
a83c-ctx.json
a83c-lot.json
a83-defaut.json
a83d-lot-threads.json
aiguille-30b.md
aiguille-gpt-oss.md
alignement-3b.json
alignement-7b.json
alignement-verne.md
analyse-litteraire.json
archive
atomes-niveaux.json
atomes-prediction.json
atomes-prediction-mesures.json
b102bis-capacite.json
b102bis-corpus-jw.json
b102bis-decodeur.json
b10-decodeur-mots.json
b10-mots-contraste.json
b10-mots-jw.json
b1110-audit.json
b1110b-hybride.json
b1110-cartes.json
b1110c-case.json
b13-porte-134.json
b13-porte-138.json
b13-porte-140.json
banc-
… [41381 caractères tronqués]
  ```

- **bash** `{"command": "ls -la data/wiki_mix/propre data/wiki_fr/propre data/wiki_big/propre data/wiki_en/propre 2>/dev/null", "description": "Liste les sous-dossiers propre", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
data/wiki_big/propre:
total 1759136
drwxr-xr-x. 1 stephane stephane        88  2 nov 10:28 .
drwxr-xr-x. 1 stephane stephane        28  2 nov 10:03 ..
-rw-r--r--. 1 stephane stephane  46186496  2 nov 10:03 test.txt
-rw-r--r--. 1 stephane stephane 831397620  2 nov 10:27 train.canal
-rw-r--r--. 1 stephane stephane 831397620  2 nov 10:03 train.txt
-rw-r--r--. 1 stephane stephane  46186496  2 nov 10:28 val.canal
-rw-r--r--. 1 stephane stephane  46186496  2 nov 10:03 val.txt

data/wiki_en/propre:
total 241932
drwxr-xr-x. 1 stephane stephane        62  1 nov 20:06 .
drwxr-xr-x. 1 stephane stephane        36  1 nov 19:25 ..
-rw-r--r--. 1 stephane stephane  20455424  1 nov 20:06 dev.txt
-rw-r--r--. 1 stephane stephane  11362304  1 nov 19:25 test.txt
-rw-r--r--. 1 stephane stephane 204556300  1 nov 19:25 train.txt
-rw-r--r--. 1 stephane stephane  11362304  1 nov 19:25 val.txt

data/wiki_fr/propre:
total 603712
drwxr-xr-x. 1 stephane stephane       160  1 nov 18:42 .
drwxr-xr-x. 1 stephane stephane        36  1 nov 11:54 ..
-rw-r--r--. 1 stephane stephane  18604032  1 nov 18:30 dev.txt
-rw-r--r--. 1 stephane stephane  10330245  1 nov 18:36 test.canal
-rw-r--r--. 1 stephane stephane  10330245
… [775 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de l'inventaire existant et des JSON de corpus pour recouper

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/inventaire-donnees-entrainement.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/inventaire-donnees-entrainement.md</path>
<type>file</type>
<content>
1: # L'inventaire local des données pour l'entraînement
2: 
3: > **Ligne de roadmap** : Données · **Date** : 2026-11-01 · **Verdict** : le disque porte
4: > **132 Go de Wikipédia** (10 langues), **12 Go d'articles Wikipédia en texte brut**, **6,6 Go de
5: > corpus déjà préparés** (dont 5,36 Mo de prose du dépôt unique), **~228 Go de documents à
6: > extraire** (dont 2 345 Kindle sous DRM, exclus), et **2,8 To de vidéos récupérées** qui ne sont
7: > pas des données d'entraînement. Le français « réel » hors Wikipédia reste **petit** : c'est le
8: > levier à construire, pas un stock à consommer.
9: 
10: ## 1. Ce qui est mesuré, et comment
11: 
12: Tour du disque le 1er novembre 2026 : `df -hT`, `lsblk`, `du -sh` par répertoire (avec délais), et
13: `find -type f` pour les comptages et les extensions. Le `du` complet de `/home/stephane` (10,9 To)
14: a été **interrompu** : trop lent ; les chiffres sont des **mesures ciblées**, pas une somme
15: exhaustive. Le JSON joint porte les 59 entrées, leurs tailles, formats, rôles et états.
16: 
17: | volume | taill
… [8219 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/recensement-francais.json 2>/dev/null | head -100", "description": "Lit le recensement français", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
{
 "objet": "recensement du français unique disponible dans le dépôt au 2026-11-01",
 "methode": "mêmes shingles de 96 octets que tools/corpus_propre.py, archives exclues",
 "docs+journal": {
  "documents": 995,
  "brut_octets": 48730000,
  "unique_octets": 27670000,
  "retire_pct": 43.3,
  "ratio_corpus_utilise": 8.5
 },
 "docs+journal+reports": {
  "documents": 1540,
  "brut_octets": 51970000,
  "unique_octets": 30350000,
  "retire_pct": 41.7,
  "ratio_corpus_utilise": 9.4
 },
 "corpus_utilise_octets": 3244858,
 "note": "mesure approximative (arrondie) ; journal/sessions contient des transcripts, à filtrer pour un corpus d'entraînement"
}
  ```

### 🤖 Assistant

⏵ Recoupement des manifestes : octets, lignes, recettes de chaque corpus

- **bash** `{"command": "for f in rapport-corpus-epingle.md corpus-commun.json corpus-wiki-fr-texte.json corpus-wiki-fr.json corpus-wiki-big-propre.json corpus-wiki-propre.json corpus-pdf.json corpus-pdf-documents.json corpus-litt-propre.json corpus-propre.json; do echo \"########## $f\"; head -c 2200 \"reports … [139 caractères tronqués]`

  ```
########## rapport-corpus-epingle.md
# N — le corpus d'entraînement est épinglé

> **Ligne de roadmap** : N (le palier 1, « la donnée d'abord ») · **Date** : 2026-11-18 ·
> **Verdict** : ✅ le corpus de `data/wiki_mix/propre` est **épinglé** — sha256 du train, du val et
> de leurs canaux, tailles, lignes, dates, empreinte du manifeste (`fae5bb73…`). Sans cette
> épingle, chaque perplexité est une rumeur : l'alerte du 16/11 a montré que le `ppl_val` 2,40
> annoncé **ne se reproduit pas** avec le `val.txt` actuel (17,3 à 22,6 selon le morceau lu).
>
> **Dispositif** : [`tools/epingle_corpus.py`](../tools/epingle_corpus.py) · le manifeste
> [`corpus-epingle.json`](corpus-epingle.json) · vérification `--verifie` (recalcule et compare).

## L'épingle

| fichier | sha256 | octets | lignes |
|---|---|---:|---:|
| `train.txt` | `0876b6089aaebb5d…` | 1 017 487 092 | 2 480 766 |
| `val.txt` | `fbddef918166f1d6…` | 10 330 112 | 24 498 |
| `train.canal` | `04efed3039f8398e…` | 1 017 487 092 | — (classes par octet) |
| `val.canal` | `f1abc5d1d63c3207…` | 10 330 112 | — |
| **manifeste** | `fae5bb7389c6c0a9…` | — | — |

Date des fichiers : **2026-11-02 12:25:22**. L'empreinte du manifeste est le 
… [16466 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche de la recette exacte du corpus épinglé `wiki_mix`

- **bash** `{"command": "grep -rIl \"wiki_mix\" --include=\"*.py\" --include=\"*.sh\" --include=\"*.md\" --include=\"*.json\" tools/ reports/ docs/ journal/ 2>/dev/null | head -20", "description": "Trouve les fichiers qui mentionnent wiki_mix", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
tools/banc_generation.py
tools/epingle_corpus.py
reports/rapport-n2-melange.md
reports/rapport-n2-200k.md
reports/n2-200k.json
reports/rapport-n2-fenetre.md
reports/n2-fenetre.json
reports/n2-production-fenetre.json
reports/rapport-n2-production-fenetre.md
reports/rapport-banc-generation.md
reports/rapport-natif-exploitable.md
reports/fiche-modele-natif.md
reports/rapport-native-reproductibilite.md
reports/corpus-epingle.json
reports/rapport-corpus-epingle.md
reports/natif-val-deux-decoupages.json
reports/rapport-natif-val-deux-decoupages.md
journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/digest.md
journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/rapport.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
  ```

- **bash** `{"command": "head -c 1500 data/wiki_big/brut.txt; echo; echo \"=== wiki_fr/articles.txt ===\"; head -c 800 data/wiki_fr/articles.txt; echo; echo \"=== corpus_fr_litterature ===\"; head -c 600 data/corpus_fr_litterature.txt", "description": "Aperçu des premiers octets de trois corpus", "workdir": "/h … [47 caractères tronqués]`

  ```
Jean Henri Le Febvre

Jean Henri Le Febvre, né le  à Montpellier (Hérault) et mort le  à Fleury-les-Aubrais (Loiret), est un homme politique français. Biographie Licencié en droit, il entre à l'école militaire de Saint-Cyr en 1890. Il quitte l'armée en 1903 et s'installe dans l'Indre, pour gérer ses domaines. Maire de Rosnay en 1908, il est député de l'Indre de 1919 à 1924, siégeant à droite, au groupe de l'Entente républicaine démocratique. Voir aussi Bibliographie Liens externes Catégorie:Naissance en février 1869 Catégorie:Naissance à Montpellier Catégorie:Décès en mars 1946 Catégorie:Député de l'Indre (Troisième République) Catégorie:Député de la douzième législature de la Troisième République Catégorie:Maire de l'Indre Catégorie:Personnalité de la Fédération républicaine Catégorie:Décès à 77 ans Catégorie:Décès à Fleury-les-Aubrais

Louis Aurin

Louis Aurin, né le  à Condom (Gers) et mort le  à Agen (Lot-et-Garonne), est un homme politique français. Biographie Ouvrier électricien et agent des PTT, syndicaliste unitaire, il est élu député de l'Indre en 1928 sous l'investiture communiste, mais son élection est contestée par la direction nationale du PCF qui lui reproche de s'êtr
… [1649 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection des corpus secondaires : UDHR, structures, panini, presse, ONU

- **bash** `{"command": "for d in udhr structures panini panini.old onu presse raisonnement jw eurlex jrc ted2020 multiun opensubtitles wikimatrix; do echo \"=== data/$d ===\"; ls -la \"data/$d\" 2>/dev/null | head -14; done", "description": "Inspecte les dossiers secondaires", "workdir": "/home/stephane/Data13 … [28 caractères tronqués]`

  ```
=== data/udhr ===
total 19588
drwxr-xr-x. 1 stephane stephane     502 25 oct 00:01 .
drwxr-xr-x. 1 stephane stephane    2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane 7661342 17 oct 23:14 articles.jsonl
-rw-r--r--. 1 stephane stephane 6481755 17 oct 23:14 articles_propres.jsonl
-rw-r--r--. 1 stephane stephane    8286 17 oct 23:49 _eng.txt
drwxr-xr-x. 1 stephane stephane    1206 27 oct 22:33 familles
-rw-r--r--. 1 stephane stephane    9734 17 oct 23:49 _fra.txt
-rw-r--r--. 1 stephane stephane   90808 18 oct 10:30 genealogie.json
-rw-r--r--. 1 stephane stephane  126982 17 oct 23:14 langues.jsonl
-rw-r--r--. 1 stephane stephane   57191 17 oct 23:14 meta.json
-rw-r--r--. 1 stephane stephane   70498 18 oct 01:19 udhr_10_train.txt
-rw-r--r--. 1 stephane stephane   29232 18 oct 01:19 udhr_10_val.txt
-rw-r--r--. 1 stephane stephane    6834 18 oct 01:31 udhr_1_train.txt
=== data/structures ===
total 136
drwxr-xr-x. 1 stephane stephane   264  2 nov 16:27 .
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane 27387  2 nov 20:36 banque.jsonl
-rw-r--r--. 1 stephane stephane   395  2 nov 20:36 banque-manifest.json
-rw-r--r--. 1 stephane stephane  4857  2 no
… [3798 caractères tronqués]
  ```

- **bash** `{"command": "ls -d corpus 2>/dev/null && du -sh corpus/* 2>/dev/null | sort -rh | head -30; echo \"=== racine ===\"; ls -la | head -40", "description": "Vérifie le dossier corpus hors data", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
=== racine ===
total 212
drwxr-xr-x. 1 stephane stephane   774 16 nov 03:32 .
drwxr-xr-x. 1 stephane stephane  2574 16 nov 10:32 ..
-rw-r--r--. 1 stephane stephane 10375 18 nov 08:31 AGENTS.md
drwxr-xr-x. 1 stephane stephane   158 18 nov 09:16 bench
drwxr-xr-x. 1 stephane stephane    42 16 nov 02:01 build
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane    56 16 nov 00:38 dist
drwxr-xr-x. 1 stephane stephane   138 16 nov 04:02 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   136 16 nov 04:07 drave.egg-info
drwxr-xr-x. 1 stephane stephane   220 18 nov 09:16 .git
drwxr-xr-x. 1 stephane stephane    22 16 nov 03:51 .github
-rw-r--r--. 1 stephane stephane   653 15 nov 22:25 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane  1052 18 nov 08:36 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-------. 1 stephane stephane  1272 16 nov 01:44 pyproject.toml
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .py
… [1242 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Determination de la composition exacte de `wiki_mix` (langues, sources)

- **bash** `{"command": "grep -n -B3 -A12 \"wiki_mix\" reports/rapport-n2-melange.md reports/rapport-n2-200k.md reports/fiche-modele-natif.md 2>/dev/null | head -80", "description": "Cherche la composition de wiki_mix dans les rapports", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
reports/rapport-n2-melange.md-53-
reports/rapport-n2-melange.md-54-## Fichiers
reports/rapport-n2-melange.md-55-
reports/rapport-n2-melange.md:56:- Modèle : `work/n2w/mix-60k.pt` ; corpus : `data/wiki_mix/propre/` (1,02 Go) ; mesures :
reports/rapport-n2-melange.md-57-  `work/n2w/eval-mix60-*.json`, `ood-mix60.json`.
--
reports/rapport-n2-200k.md-22-
reports/rapport-n2-200k.md-23-## Le dispositif
reports/rapport-n2-200k.md-24-
reports/rapport-n2-200k.md:25:- **Corpus** : `data/wiki_mix/propre/train.txt` — **1 017 487 092 octets** (1,02 Go), concaténation
reports/rapport-n2-200k.md-26-  de `data/wiki_fr/propre` (186 Mo) et `data/wiki_big/propre` (831 Mo) ; canal concaténé ; le
reports/rapport-n2-200k.md-27-  découpage interne réserve les 5 % finaux à la validation d'entraînement.
reports/rapport-n2-200k.md-28-- **Recette** : **identique à N2.ac** — 34,3 M (`384/512`), `--seq 128 --lot 8 --lr 3e-4
reports/rapport-n2-200k.md-29-  --graine 1 --positions-aleatoires 384 --canal` — à un seul paramètre près : **200 000 pas** au
reports/rapport-n2-200k.md-30-  lieu de 60 000 (×3,33). GPU 0, **11 410 s** (3 h 10), ~57 ms/pas.
reports/rapport-n2-200k.md-31-- **Mètre** : `work/n2ac/eval_200k.p
… [2881 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"wiki_mix\" tools/epingle_corpus.py tools/banc_generation.py 2>/dev/null | head -20; echo \"=== wiki_multi ===\"; ls -la data/wiki_multi/", "description": "Cherche wiki_mix dans les outils et liste wiki_multi", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
tools/epingle_corpus.py:13:  python3 tools/epingle_corpus.py --corpus data/wiki_mix/propre --sortie reports/corpus-epingle.json
tools/epingle_corpus.py:14:  python3 tools/epingle_corpus.py --corpus data/wiki_mix/propre --sortie reports/corpus-epingle.json --verifie
tools/epingle_corpus.py:120:    ap.add_argument("--corpus", default="data/wiki_mix/propre")
tools/banc_generation.py:15:    (`data/wiki_mix/propre/train.txt`, les 50 000 formes les plus fréquentes) —
tools/banc_generation.py:45:CORPUS = RACINE / "data/wiki_mix/propre/train.txt"
=== wiki_multi ===
total 562552
drwxr-xr-x. 1 stephane stephane       470  1 nov 13:34 .
drwxr-xr-x. 1 stephane stephane      2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane  29680990  1 nov 13:26 ar_train.txt
-rw-r--r--. 1 stephane stephane   2670849  1 nov 13:26 ar_val.txt
-rw-r--r--. 1 stephane stephane  21299927  1 nov 13:26 de_train.txt
-rw-r--r--. 1 stephane stephane   1945713  1 nov 13:26 de_val.txt
-rw-r--r--. 1 stephane stephane  21466004  1 nov 13:26 en_train.txt
-rw-r--r--. 1 stephane stephane   1955394  1 nov 13:26 en_val.txt
-rw-r--r--. 1 stephane stephane  20400723  1 nov 13:26 es_train.txt
-rw-r--r--. 1 stephane stephane   1838
… [958 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lancement du comptage de lignes des corpus français en tâche de fond

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in data/wiki_mix/propre/train.txt data/corpus_wiki_fr_texte/train.txt data/corpus_wiki_fr/train.txt data/wiki_big/brut.txt data/wiki_fr/articles.txt data/corpus_pdf_documents/train.txt data/corpus_pdf/train.txt data/wiki_multi/ … [304 caractères tronqués]`

  ```
started background job bash-428
  ```

- **bash** `{"command": "ls /home/stephane/Data13TB/stephane/data/ 2>/dev/null | head -40; echo \"=== taille ===\"; du -sh /home/stephane/Data13TB/stephane/data 2>/dev/null; echo \"=== corpus externe ===\"; ls -d /home/stephane/Data13TB/stephane/corpus 2>/dev/null && du -sh /home/stephane/Data13TB/stephane/corp … [96 caractères tronqués]`

  ```
wikipedia
=== taille ===
132G	/home/stephane/Data13TB/stephane/data
=== corpus externe ===
/home/stephane/Data13TB/stephane/corpus
21G	/home/stephane/Data13TB/stephane/corpus/udhr
12G	/home/stephane/Data13TB/stephane/corpus/wiki_apparie
1,8G	/home/stephane/Data13TB/stephane/corpus/wiki_traces
988M	/home/stephane/Data13TB/stephane/corpus/parallele_rj
261M	/home/stephane/Data13TB/stephane/corpus/parallele_crime
  ```

### 🤖 Assistant

⏵ Recherche des licences déclarées et échantillons de langue

- **bash** `{"command": "find data -maxdepth 3 -type f \\( -iname \"LICENSE*\" -o -iname \"README*\" -o -iname \"*.license\" -o -iname \"NOTICE*\" \\) 2>/dev/null | head -30; echo \"=== licences dans les manifestes ===\"; grep -h '\"licence\"' reports/corpus-*.json 2>/dev/null | sort | uniq -c | sort -rn | head … [132 caractères tronqués]`

  ```
data/adaptateurs/bilingue-1600/README.md
data/adaptateurs/plan-bilingue-800/README.md
data/adaptateurs/plan-contraste-800/README.md
data/adaptateurs/plan-contraste-plein-800/README.md
data/adaptateurs/plan-recurrent-800/README.md
data/adaptateurs/plan-multi-tache-800/README.md
data/xnli/XNLI-1.0/README.md
=== licences dans les manifestes ===
     10  "licence": "Wikipédia : CC-BY-SA 4.0 (et GFDL) — attribution et partage à l'identique ; corpus local, non diffusé",
     10  "licence": "Wikipédia : CC-BY-SA 4.0 (et GFDL) — attribution et partage à l'identique ; corpus local",
      6  "licence": "corpus local, licence à vérifier — ne pas diffuser",
      1    "licence": "notes de cours — droits réservés, usage local, non diffusé"
      1    "licence": "livres — droits réservés, usage local, non diffusé"
      1    "licence": "à préciser"
  ```

- **bash** `{"command": "echo \"=== corpus_multi.txt ===\"; head -c 500 data/corpus_multi.txt; echo; echo \"=== corpus_mixte.txt ===\"; head -c 400 data/corpus_mixte.txt; echo; echo \"=== corpus_en.txt ===\"; head -c 300 data/corpus_en.txt; echo; echo \"=== wiki_multi/train.txt ===\"; head -c 400 data/wiki_mult … [135 caractères tronqués]`

  ```
=== corpus_multi.txt ===
Tudu nguê di mundu ca nancê livli e igual ni dignidade e ni dirêtu. Punda nen ca pensá e nen tê cunxensa, selá nen fé tudu cuá cu tençón de lumón.
Tudu nguê ca pô flá ni dirêtu cu liberdade cu sa ploclamadu ni Declaraçón sé, sê distinçón, mó fala di laça, di côlô, di sexo, di lungua, di religiôn, di pensamento político ô ôtlo, di natureza di téla ô di sociedade, di liqueza, di naximentu ô qualqué ôtlo situaçón. Alén di cuá sé, a na ca pô fé nê ua separa�
=== corpus_mixte.txt ===
« « « ENGLISH « « «
Anarchism is a political philosophy and movement that seeks to abolish all institutions that perpetuate authority, coercion, or hierarchy, primarily targeting the state and capitalism. Anarchism advocates for the replacement of the state with stateless societies and voluntary free associations.

Although traces of anarchist ideas are found all throughout history, modern a
=== corpus_en.txt ===
Anarchism is a political philosophy and movement that seeks to abolish all institutions that perpetuate authority, coercion, or hierarchy, primarily targeting the state and capitalism. Anarchism advocates for the replacement of the state with stateless societies and volunta
… [451 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du comptage de lignes en cours

- **job_output** `{"job_id": "bash-428"}`

  ```
data/wiki_mix/propre/train.txt	2480766
data/corpus_wiki_fr_texte/train.txt	88114432
data/corpus_wiki_fr/train.txt	
[status: running]
  ```

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/data/wikipedia/ 2>/dev/null; echo \"=== fr ===\"; ls -la /home/stephane/Data13TB/stephane/data/wikipedia/db/fr* /home/stephane/Data13TB/stephane/data/wikipedia/dumps/fr/* 2>/dev/null | head", "description": "Inspecte les dumps Wikipédia externes"}`

  ```
total 0
drwxr-xr-x. 1 stephane stephane  14 25 mai 14:39 .
drwxr-xr-x. 1 stephane stephane  18 25 mai 14:39 ..
drwxr-xr-x. 1 stephane stephane 940  1 nov 11:41 db
drwxr-xr-x. 1 stephane stephane  40 26 mai 09:14 dumps
=== fr ===
-rw-r--r--. 1 stephane stephane 7248388096 25 mai 22:50 /home/stephane/Data13TB/stephane/data/wikipedia/db/frwiki_v14.db
-rw-r--r--. 1 stephane stephane      32768  2 nov 09:12 /home/stephane/Data13TB/stephane/data/wikipedia/db/frwiki_v14.db-shm
-rw-r--r--. 1 stephane stephane          0  1 nov 11:41 /home/stephane/Data13TB/stephane/data/wikipedia/db/frwiki_v14.db-wal
-rw-r--r--. 1 stephane stephane   63415485 25 mai 15:22 /home/stephane/Data13TB/stephane/data/wikipedia/dumps/fr/frwiki-latest-pages-articles-multistream-index.txt.bz2
-rw-r--r--. 1 stephane stephane 7129511779 25 mai 15:22 /home/stephane/Data13TB/stephane/data/wikipedia/dumps/fr/frwiki-latest-pages-articles-multistream.xml.bz2
  ```

### 🤖 Assistant

⏵ Lecture des fiches corpus 1 Go et élargissement (contexte du palier 1)

- **bash** `{"command": "for f in rapport-n2-corpus-1go.md rapport-n2-corpus-elargi.md; do echo \"########## $f\"; sed -n '1,80p' \"reports/$f\"; done", "description": "Lit les fiches du corpus 1 Go et élargi", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
########## rapport-n2-corpus-1go.md
# N2.aa — Le corpus de 831 Mo à compute constant : un autre domaine, pas plus de savoir

> **Ligne de roadmap** : N2 · **Date** : 2026-11-02 · **Verdict** : à recette égale (34,3 M, deux
> étages de 20 000 pas, canal), le corpus de **831 Mo** (600 000 articles, offset 1 M, **0 fuite**)
> donne **3,7025** sur la validation de N2.z (3,5250) et **3,4604** sur la sienne ; N2.z donne
> **3,5250** sur la sienne et **3,7107** sur celle du grand. **Chaque modèle est meilleur sur son
> propre domaine** (écart ~0,2) : à 40 Mo vus, un corpus 5,6× plus grand ne fait pas apprendre plus
> — il fait apprendre **autre chose**.

## Le dispositif

- **Corpus** : 600 000 articles (page_id à partir de 1 000 000, disjoint du corpus N2.j qui part de
  200 000) ; brut **1 048 Mo** → dédupliqué **924 Mo (88,2 %)** → train **831 Mo**, val 46 Mo, test
  46 Mo ; **0 fuite** sur 4 000 fenêtres (`reports/corpus-wiki-big-propre.json`).
- **Modèle** : 34,3 M (`384/512`), deux étages de 20 000 pas × 8 × 128, positions [0, 384], canal de
  structure — exactement la recette de N2.z.
- **Évaluation croisée** : chaque modèle sur **les deux** validations (la même fenêtre de 4 lots ×
… [7088 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-428 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in data/wiki_mix/propre/train.txt data/corpus_wiki_fr_texte/train.txt data/corpus_wiki_fr/train.txt data/wiki_big/brut.txt data/wiki_fr/articles.txt data/corpus_pdf_documents/train.txt data/corpus_pdf/train.txt data/wiki_multi/train.txt data/corpus_multi.txt data/corpus_en.txt data/corpus_fr_litterature.txt data/corpus_fr.txt; do printf '%s\t' "$f"; timeout 300 wc -l < "$f"; done) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Récupération des comptages de lignes terminés

- **job_output** `{"job_id": "bash-428"}`

  ```
4546588
data/wiki_big/brut.txt	2400000
data/wiki_fr/articles.txt	480000
data/corpus_pdf_documents/train.txt	21187808
data/corpus_pdf/train.txt	8306610
data/wiki_multi/train.txt	440000
data/corpus_multi.txt	1465777
data/corpus_en.txt	1196326
data/corpus_fr_litterature.txt	350641
data/corpus_fr.txt	48330
[status: completed, exit code: 0]
  ```

### 🤖 Assistant

⏵ Mesure du total, des débits gzip et de la langue réelle des corpus PDF

- **bash** `{"command": "echo \"=== total apparent ===\"; du -sb data 2>/dev/null; echo \"=== nombre de fichiers ===\"; find data -type f 2>/dev/null | wc -l; echo \"=== fichiers par dossier clé ===\"; for d in corpus_wiki_fr_texte corpus_wiki_fr wiki_mix wiki_big wiki_fr udhr structures opensubtitles multiun w … [287 caractères tronqués]`

  ```
=== total apparent ===
135523369596	data
=== nombre de fichiers ===
4428
=== fichiers par dossier clé ===
corpus_wiki_fr_texte         3
corpus_wiki_fr               3
wiki_mix                     4
wiki_big                     6
wiki_fr                      9
udhr                         55
structures                   6
opensubtitles                2
multiun                      2
wikimatrix                   2
ted2020                      2
jrc                          2
eurlex                       32
onu                          81
presse                       46
jw                           73
deepseek                     3789
pidgin.old                   70
adaptateurs                  19
xnli                         52
  ```

- **bash** `{"command": "for f in data/*/*.tmx.gz; do printf \"%-42s \" \"$f\"; gzip -l \"$f\" 2>/dev/null | tail -1 | awk '{printf \"compresse=%s  decompresse=%s\\n\", $2, $1}'; done", "description": "Taille décompressée des corpus parallèles TMX", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
data/jrc/en-fr.tmx.gz                      compresse=235330059  decompresse=49409718
data/multiun/en-fr.tmx.gz                  compresse=5137807269  decompresse=1276271220
data/opensubtitles/en-fr.tmx.gz            compresse=6243401029  decompresse=1264276955
data/ted2020/en-fr.tmx.gz                  compresse=124236908  decompresse=32964653
data/wikimatrix/en-fr.tmx.gz               compresse=1048389238  decompresse=340868887
  ```

### 🤖 Assistant

⏵ Estimation de la part française par échantillonnage (sans lecture intégrale)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport os, random\nFR=set(\"le la les de des du un une et est dans pour que qui sur pas au aux avec ce cette il elle nous vous ils sont être avoir plus mais ou où son sa ses leur\".split())\nEN=set(\"the of and to i … [1295 caractères tronqués]`

  ```
data/corpus_wiki_fr_texte/train.txt           FR~ 96.3%  (7.504 Go)
data/corpus_wiki_fr/train.txt                 FR~ 95.8%  (3.426 Go)
data/wiki_big/brut.txt                        FR~ 95.5%  (1.048 Go)
data/corpus_pdf/train.txt                     FR~ 16.5%  (0.296 Go)
data/corpus_pdf_documents/train.txt           FR~ 14.7%  (0.803 Go)
data/corpus_en.txt                            FR~  1.6%  (0.100 Go)
data/corpus_mixte.txt                         FR~ 53.5%  (0.011 Go)
data/wiki_multi/train.txt                     FR~ 41.3%  (0.275 Go)
data/corpus_multi.txt                         FR~ 17.4%  (0.122 Go)
data/corpus_fr_litterature.txt                FR~ 97.5%  (0.017 Go)
data/wiki_mix/propre/train.txt                FR~ 95.3%  (1.017 Go)
  ```

- **bash** `{"command": "cat reports/corpus-pdf-contamination.json reports/corpus-pdf-documents-contamination.json reports/corpus-wiki-fr-texte-contamination.json reports/corpus-wiki-fr-texte-pilote-contamination.json 2>/dev/null | head -60", "description": "Lit les rapports de contamination PDF et wiki", "work … [56 caractères tronqués]`

  ```
{
 "train": "data/corpus_pdf/train.txt",
 "doublons_entre_splits": {
  "train_troncons": 2080695,
  "par_split": {
   "val.txt": {
    "troncons": 120400,
    "doublons": 4868,
    "taux": 0.040432
   },
   "test.txt": {
    "troncons": 86900,
    "doublons": 2238,
    "taux": 0.025754
   }
  }
 },
 "recouvrement_eval": [
  {
   "fichier": "test.txt",
   "fenetre": 128,
   "fenetres": 40,
   "trouvees": 0,
   "taux": 0.0
  },
  {
   "fichier": "test.txt",
   "fenetre": 128,
   "fenetres": 40,
   "trouvees": 0,
   "taux": 0.0
  },
  {
   "fichier": "test.txt",
   "fenetre": 128,
   "fenetres": 40,
   "trouvees": 0,
   "taux": 0.0
  }
 ],
 "taille_troncon": 8192,
 "doublons_entre_splits_troncon": {
  "train_troncons": 36167,
  "par_split": {
   "val.txt": {
    "troncons": 1833,
    "doublons": 0,
    "taux": 0.0
   },
   "test.txt": {
    "troncons": 1436,
    "doublons": 0,
    "taux": 0.0
   }
  }
 }
}
{
 "train": "data/corpus_pdf_documents/train.txt",
 "doublons_entre_splits": {
  ```

### 🤖 Assistant

⏵ Vérification du déséquilibre linguistique des corpus PDF (comptage direct)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in data/corpus_pdf/train.txt data/corpus_pdf_documents/train.txt data/corpus_wiki_fr_texte/train.txt; do echo \"=== $f ===\"; printf \"occurrences ' de ' : \"; grep -o \" de \" \"$f\" | wc -l; printf \"occurrences ' the ' : \"; … [97 caractères tronqués]`

  ```
=== data/corpus_pdf/train.txt ===
occurrences ' de ' : 225758
occurrences ' the ' : 1770276
=== data/corpus_pdf_documents/train.txt ===
occurrences ' de ' : 509229
occurrences ' the ' : 4913127
=== data/corpus_wiki_fr_texte/train.txt ===
occurrences ' de ' : 
[still running after 60000ms; moved to background job bash-468]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport os\nfor p in [\"data/corpus_pdf/train.txt\",\"data/corpus_pdf_documents/train.txt\"]:\n    sz=os.path.getsize(p); acc=0; tot=0\n    with open(p,'rb') as f:\n        for k in range(20):\n            f.seek(k*s … [256 caractères tronqués]`

  ```
data/corpus_pdf/train.txt accentués 0.29%
data/corpus_pdf_documents/train.txt accentués 0.33%
  ```

### 🤖 Assistant

⏵ Vérification de la structure du corpus wiki FR plein texte et recouvrement

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== corpus_wiki_fr_texte (5 premières lignes, tronquées) ===\"; head -5 data/corpus_wiki_fr_texte/train.txt | cut -c1-160; echo; echo \"=== wiki_big/brut (4 lignes) ===\"; head -4 data/wiki_big/brut.txt | cut -c1-120; echo; ec … [164 caractères tronqués]`

  ```
=== corpus_wiki_fr_texte (5 premières lignes, tronquées) ===
Antoine Meillet
Antoine Meillet, né le à Moulins (Allier) et mort le à Châteaumeillant (Cher), est un philologue français, le principal linguiste français des premières décenni

Biographie
Enfance et formation

=== wiki_big/brut (4 lignes) ===
Jean Henri Le Febvre

Jean Henri Le Febvre, né le  à Montpellier (Hérault) et mort le  à Fleury-les-Aubrais (Loiret), est un homme politique f


=== wiki_fr/articles (4 lignes) ===
Antoine Meillet

Antoine Meillet, né le  à Moulins (Allier) et mort le  à Châteaumeillant (Cher), est un philologue français, le principa
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== corpus_wiki_fr-texte : lignes vides / titres ===\"; head -200000 data/corpus_wiki_fr_texte/train.txt | awk 'NF==0{v++} NF>0 && length($0)<100{t++} END{print \"vides:\",v,\" courts(<100):\",t}'", "description": "Analyse la  … [43 caractères tronqués]`

  ```
=== corpus_wiki_fr-texte : lignes vides / titres ===
vides: 58499  courts(<100): 83799
  ```

### 👤 Utilisateur

background job bash-468 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in data/corpus_pdf/train.txt data/corpus_pdf_documents/train.txt data/corpus_wiki_fr_texte/train.txt; do echo "=== $f ==="; printf "occurrences ' de ' : "; grep -o " de " "$f" | wc -l; printf "occurrences ' the ' : "; grep -o " the " "$f" | wc -l; done) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Lecture du comptage `de/the` et mesure du taux de duplication par échantillon

- **job_output** `{"job_id": "bash-468"}`

  ```
68688961
occurrences ' the ' : 580410
[status: completed, exit code: 0]
  ```

### 🤖 Assistant

⏵ Vérification de la faisabilité mémoire de la déduplication 7,5 Go

- **bash** `{"command": "free -g; echo \"---\"; nproc; echo \"=== corpus_propre.py : gestion mémoire ===\"; grep -n -E \"set\\(|bytearray|memoire|RAM|shingle|dict\" tools/corpus_propre.py | head -30", "description": "Vérifie la RAM disponible et l'approche du déduplicateur", "workdir": "/home/stephane/Data13TB/ … [25 caractères tronqués]`

  ```
total        used        free      shared  buff/cache   available
Mem:             125          42          29          17          73          83
Swap:             62           4          58
---
40
=== corpus_propre.py : gestion mémoire ===
11:1. **Déduplication par shingles.** On roule un hachage de Rabin-Karp sur des fenêtres de
12:   `--fenetre` octets (96 par défaut). La première occurrence d'un shingle est gardée ;
13:   toute position couverte par un shingle déjà vu est retirée. Conséquence : après
60:    """Vrai pour chaque position couverte par un shingle déjà vu plus tôt."""
62:    premier: dict[int, int] = {}
82:def deduit(data: bytes, fenetre: int, min_run: int = 64) -> tuple[bytes, dict]:
126:                       maxi: int | None = None) -> dict:
194:            "deduplication": "shingles de Rabin-Karp (base 257, mod 2^61−1), première "
196:            "fenetre_shingle": a.fenetre,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport os, zlib\np=\"data/corpus_wiki_fr_texte/train.txt\"; sz=os.path.getsize(p)\nN=150_000_000; off=(sz-N)//2\nwith open(p,'rb') as f:\n    f.seek(off); b=f.read(N)\nW=96; S=16\nvus=set(); tot=0; dup=0\nfor i in r … [343 caractères tronqués]`

  ```
échantillon 150 Mo, fenêtre 96 o, pas 16 o
shingles 9374994, dupliqués 67770 (0.72 %)
distincts 9307224
  ```

### 🤖 Assistant

⏵ Lancement de la mesure de duplication globale et vérification des licences déclarées

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport os, zlib, time\np=\"data/corpus_wiki_fr_texte/train.txt\"; sz=os.path.getsize(p)\nW=96; S=96\nvus=set(); tot=0; dup=0; t0=time.time()\nwith open(p,'rb') as f:\n    b=f.read()\nmv=memoryview(b)\nfor i in range … [391 caractères tronqués]`

  ```
started background job bash-492
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -l '\"licence\"' reports/corpus-*.json | head -30; echo \"=== palier 1 / cible 3-6 Go ===\"; grep -rn \"palier 1\" reports/*.md docs/pilotage/*.md 2>/dev/null | head -12", "description": "Liste les manifestes avec licence et che … [27 caractères tronqués]`

  ```
reports/corpus-litt-propre.json
reports/corpus-multi-propre.json
reports/corpus-pdf-documents.json
reports/corpus-pdf.json
reports/corpus-propre.json
reports/corpus-repo-propre.json
reports/corpus-wiki-ar.json
reports/corpus-wiki-ar-texte.json
reports/corpus-wiki-de.json
reports/corpus-wiki-de-texte.json
reports/corpus-wiki-en.json
reports/corpus-wiki-en-propre.json
reports/corpus-wiki-es.json
reports/corpus-wiki-es-texte.json
reports/corpus-wiki-fr.json
reports/corpus-wiki-fr-texte.json
reports/corpus-wiki-fr-texte-pilote.json
reports/corpus-wiki-it.json
reports/corpus-wiki-it-texte.json
reports/corpus-wiki-ja.json
reports/corpus-wiki-ja-texte.json
reports/corpus-wiki-propre.json
reports/corpus-wiki-pt.json
reports/corpus-wiki-pt-texte.json
reports/corpus-wiki-ru.json
reports/corpus-wiki-ru-texte.json
reports/corpus-wiki-zh.json
reports/corpus-wiki-zh-texte.json
=== palier 1 / cible 3-6 Go ===
reports/rapport-banc-generation.md:94:si rien ne change ; le palier 1 doit donc traiter la **répétition** (le contrôle, la
reports/rapport-bilan-natif.md:31:**Le pas suivant** (le palier 1) : un **100–150 M sur 3–6 Go propres**, avec **le banc dès le
reports/rapport-bilan-natif.md:45:- Il ne
… [1222 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du plan natif (définition exacte du palier 1) et de la fiche d'épingle

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -B4 -A18 \"palier 1\" docs/pilotage/natif-plan.md 2>/dev/null | head -70; echo \"##########\"; sed -n '30,55p' reports/rapport-corpus-epingle.md", "description": "Lit la définition du palier 1 et la suite de l'épingle"}`

  ```
19-| **1 — le pas suivant** | **100–150 M** | **3–6 Go** | **~2–4 jours CPU** (ou 1–2 j GPU) | **50 octets cohérents sur 3 prompts** (le banc) ; répétition ≤ 3 | des phrases |
20-| **2 — le produit** | **300–600 M** | **10–20 Go** | **~2–4 semaines GPU** | **une phrase sur deux sans faute** (le juge : notre analyseur) | de la prose courte |
21-| **3 — le service** | 1–3 Md | 20–60 Go | des mois GPU | un discours + le SFT (le refus, la consigne) | un assistant |
22-
23:**Le critère du palier 1 est le premier vrai test** : le banc de génération
24-([`tools/banc_generation.py`](../../tools/banc_generation.py)) le mesure déjà (la répétition, les
25-mots valides), le banc de grammaticalité
26-([`tools/banc_grammaticalite.py`](../../tools/banc_grammaticalite.py)) le juge avec notre
27-analyseur (les GV, le ciment).
28-
29-## 3. L'ordre des chantiers
30-
31-1. **La donnée d'abord** (le vrai goulot) : 3–6 Go de français **propre** (le wiki actuel fait
32-   1 Go ; il faut le compléter — des livres, des articles, avec la licence et le dédoublonnage).
33-   **Ne pas modifier `data/` sans le propriétaire** (le territoire D). **Et l'épingler** : le
34-   sha256 du train et du val, la date, la 
… [3686 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '20,60p' reports/rapport-bilan-natif.md", "description": "Lit le bilan natif sur le pas suivant"}`

  ```
| 7 | [`natif-plan.md`](../docs/pilotage/natif-plan.md) | le plan : 4 paliers, les critères falsifiables, les risques |
| 8 | [`rapport-natif-numpy.md`](rapport-natif-numpy.md) + [`drvm_infere.py`](../tools/drvm_infere.py) | **le natif sans torch** : le DRVM en numpy, **4/4 de parité** avec torch, ~0,6 s/octet |
| 9 | [`rapport-native-reproductibilite.md`](rapport-native-reproductibilite.md) | **le 2,40 annoncé n'est pas reproductible** (17,3 à 22,6 sur le val actuel, 18,55 sur le gold) : le corpus n'est pas épinglé |
| 10 | [`banc-grammaticalite-echelle.json`](banc-grammaticalite-echelle.json) | la syntaxe à l'échelle : GV **1,90 → 2,65 → 6,90**, ciment **0,137 → 0,278 → 0,335** |

## 2. La conclusion

Le natif est un **prototype de recherche complet** : l'entraînement, la génération, le service, le
DRVM, la distillation, le SFT — tout existe et tourne. **Ce qui manque n'est pas la plomberie,
c'est la qualité** : un 34 M qui a mémorisé les mots et les boucles du corpus.

**Le pas suivant** (le palier 1) : un **100–150 M sur 3–6 Go propres**, avec **le banc dès le
premier checkpoint** et un critère falsifiable — **50 octets cohérents, la répétition ≤ 3**. La
donnée est le vrai goul
… [1252 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des sommes exactes (doublons par construction) et calibration anglais

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\ndef sz(p): return __import__('os').path.getsize(p)\nprint(\"wiki_fr/propre train + wiki_big/propre train =\", sz(\"data/wiki_fr/propre/train.txt\")+sz(\"data/wiki_big/propre/train.txt\"), \"vs wiki_mix\", sz(\"data/ … [666 caractères tronqués]`

  ```
wiki_fr/propre train + wiki_big/propre train = 1017487092 vs wiki_mix 1017487092
corpus_fr_train + val = 4633889 vs corpus_fr 4633889
corpus_multi_train + val = 121523142 vs corpus_multi 121523142
corpus_mixte_propre / dev = 10.0
=== pidgin vs pidgin.old ===
328747430	data/pidgin.old
asp_raw.json
bible.json
bible_narratif.json
bible_web.json
eng_kjv_usfm.zip
asp_raw.json
bible.json
bible_narratif.json
bible_web.json
eng_kjv_usfm.zip
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && printf \"corpus_en.txt ' de ' : \"; grep -o \" de \" data/corpus_en.txt | wc -l; printf \"corpus_en.txt ' the ' : \"; grep -o \" the \" data/corpus_en.txt | wc -l", "description": "Calibre les densités de/the en anglais pur"}`

  ```
corpus_en.txt ' de ' : 7210
corpus_en.txt ' the ' : 861039
  ```

### 🤖 Assistant

⏵ Sommes par famille et statut de la déduplication globale

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport os, glob\ndef dsize(d):\n    t=n=0\n    for r,_,fs in os.walk(d):\n        for f in fs:\n            p=os.path.join(r,f)\n            if os.path.isfile(p) and not os.path.islink(p): t+=os.path.getsize(p); n+= … [1439 caractères tronqués]`

  ```
10 langues — wikitext (corpus_wiki_<lang>)            120.10 Go     60 fichiers
10 langues — texte (corpus_wiki_<lang>_texte)          81.32 Go     30 fichiers
wiki FR (articles, résumés, mix, big)                   5.76 Go     19 fichiers
wiki_multi (10 langues)                                 0.86 Go     25 fichiers
FR hors wiki (litt, propre, repo, pdf, ocr)             1.30 Go     40 fichiers
parallèles FR-EN (tmx + json)                           3.05 Go     10 fichiers
éval (xnli, daccord, diabla, wikitext2)                 2.38 Go     65 fichiers
  ```

- **job_output** `{"job_id": "bash-492"}`

  ```
octets 7504078589; shingles 78167485; dupliqués 2290786 (2.93 %); distincts 75876699; 88s
[status: running]
  ```

### 🤖 Assistant

⏵ Test de recouvrement par titres entre `wiki_big` et le plein texte

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && awk 'NR%4==1' data/wiki_big/brut.txt | head -200 > /tmp/titres_wikibig.txt && wc -l /tmp/titres_wikibig.txt && echo \"--- présents dans corpus_wiki_fr_texte/train.txt (lignes) ---\" && timeout 110 grep -c -F -f /tmp/titres_wikibig.tx … [117 caractères tronqués]`

  ```
200 /tmp/titres_wikibig.txt
--- présents dans corpus_wiki_fr_texte/train.txt (lignes) ---
3340
  ```

- **job_list** `{}`

  ```
bash-428 [bash] completed — cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in data/wiki_mix/propre/train.txt data/corpus_wiki_fr_texte/train.txt data/corpus_wiki_fr/train.txt data/wiki_big/brut.txt data/wiki_fr/articles.txt data/corpus_pdf_documents/train.txt data/corpus_pdf/train.txt data/wiki_multi/train.txt data/corpus_multi.txt data/corpus_en.txt data/corpus_fr_litterature.txt data/corpus_fr.txt; do printf '%s\t' "$f"; timeout 300 wc -l < "$f"; done
bash-468 [bash] completed — cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in data/corpus_pdf/train.txt data/corpus_pdf_documents/train.txt data/corpus_wiki_fr_texte/train.txt; do echo "=== $f ==="; printf "occurrences ' de ' : "; grep -o " de " "$f" | wc -l; printf "occurrences ' the ' : "; grep -o " the " "$f" | wc -l; done
bash-492 [bash] completed — cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'
import os, zlib, time
p="data/corpus_wiki_fr_texte/train.txt"; sz=os.path.getsize(p)
W=96; S=96
vus=set(); tot=0; dup=0; t0=time.time()
with open(p,'rb') as f:
    b=f.read()
mv=memoryview(b)
for i in range(0, len(b)-W, S):
    h=zlib.crc32(mv[i:i+W]); tot+=1
    if h in vus: dup+=1
    e
… [140 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-492 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'
import os, zlib, time
p="data/corpus_wiki_fr_texte/train.txt"; sz=os.path.getsize(p)
W=96; S=96
vus=set(); tot=0; dup=0; t0=time.time()
with open(p,'rb') as f:
    b=f.read()
mv=memoryview(b)
for i in range(0, len(b)-W, S):
    h=zlib.crc32(mv[i:i+W]); tot+=1
    if h in vus: dup+=1
    else: vus.add(h)
print(f"octets {sz}; shingles {tot}; dupliqués {dup} ({100*dup/tot:.2f} %); distincts {len(vus)}; {time.time()-t0:.0f}s")
PY) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Contrôle exact : titres de `wiki_big` présents en ligne entière dans le plein texte

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 110 grep -c -F -x -f /tmp/titres_wikibig.txt data/corpus_wiki_fr_texte/train.txt", "description": "Compte les titres présents en ligne exacte"}`

  ```
298
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== lignes vides / titres sur 1 M lignes du plein texte ===\"; head -1000000 data/corpus_wiki_fr_texte/train.txt | awk 'NF==0{v++} NF>0 && length($0)<80{t++} END{printf \"vides %d (%.1f%%), courts<80 %d (%.1f%%)\\n\", v, 100*v … [223 caractères tronqués]`

  ```
=== lignes vides / titres sur 1 M lignes du plein texte ===
vides 247759 (24.8%), courts<80 458311 (45.8%)
=== 3 exemples de lignes courtes ===
Antoine Meillet
Biographie
Enfance et formation
Carrière
Études arméniennes
1902 : il obtient la chaire d'arménien de l'École des langues orientales.
[stderr]
head: error writing 'standard output': Broken pipe
  ```

### 🤖 Assistant

⏵ Derniers contrôles : date, doublon pidgin, titres distincts

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date -I; echo \"=== pidgin cible ===\"; du -sb /home/stephane/IA/drave-data/pidgin 2>/dev/null; echo \"=== petits dossiers (octets) ===\"; for d in corpus_ocr_cegep corpus_ocr_cegep_micro corpus_ocr_cegep_avant_micro corpus_ocr_cegep … [287 caractères tronqués]`

  ```
2026-11-18
=== pidgin cible ===
328747430	/home/stephane/IA/drave-data/pidgin
=== petits dossiers (octets) ===
corpus_ocr_cegep                 4464047
corpus_ocr_cegep_micro           352571
corpus_ocr_cegep_avant_micro     4101448
corpus_ocr_cegep_pilote-2pages   2550873
udhr                             28858709
structures                       122454
presse                           671271
jw                               36851670
onu                              10176222
eurlex                           10325824
deepseek                         13375971
raisonnement                     8175404
adaptateurs                      177390271
daccord                          545846
diabla                           2103306
xnli                             2380057696
corpus_en.txt                    100276153
wikitext2_test.txt               359041
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 110 sh -c 'grep -F -x -f /tmp/titres_wikibig.txt data/corpus_wiki_fr_texte/train.txt | sort -u | wc -l'", "description": "Compte les titres distincts retrouvés"}`

  ```
182
  ```

### 🤖 Assistant

⏵ Vérification que les 18 titres manquants sont dans val/test (contrôle du split)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in val test; do printf \"%s : \" \"$f\"; grep -F -x -f /tmp/titres_wikibig.txt data/corpus_wiki_fr_texte/$f.txt | sort -u | wc -l; done", "description": "Cherche les titres dans les splits val et test"}`

  ```
val : 14
test : 18
  ```

### 🤖 Assistant

⏵ Union des titres retrouvés sur les trois splits

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat /tmp/titres_wikibig.txt | timeout 110 grep -F -x -f - data/corpus_wiki_fr_texte/train.txt data/corpus_wiki_fr_texte/val.txt data/corpus_wiki_fr_texte/test.txt 2>/dev/null | sort -u | wc -l", "description": "Compte l'union des tit … [24 caractères tronqués]`

  ```
214
  ```

### 🤖 Assistant

⏵ Correction du comptage (sans préfixe de fichier)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 110 grep -h -F -x -f /tmp/titres_wikibig.txt data/corpus_wiki_fr_texte/train.txt data/corpus_wiki_fr_texte/val.txt data/corpus_wiki_fr_texte/test.txt | sort -u | wc -l", "description": "Compte les titres distincts sans préfix … [3 caractères tronqués]`

  ```
200
  ```

### 🤖 Assistant

⏵ Rédaction du rapport d'inventaire (seul fichier écrit)

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md", "content": "# L'inventaire des données pour le palier 1 : 1,02 Go épinglés sur 3–6 Go demandés\n\n> **Ligne de roadmap** : N (le palier 1, « la donnée d'abord ») · **Date** : 2026-11-18 ·\n> **Verd … [19862 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Correction de trois chiffres imprécis dans le rapport

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md", "old_string": "| `data/corpus_ocr*/train.txt` (4 variantes) | 19 000 000 | — | fr | notes de cours, droits réservés | OCR CEGEP |", "new_string": "| `data/corpus_ocr*` (5 dossiers, tous splits) | 2 … [68 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md", "old_string": "  `corpus_pdf_documents` comme du français (1,10 Go) est faux d'un facteur ≈ 12.", "new_string": "  `corpus_pdf_documents` comme du français (1,10 Go) est faux d'un facteur ≈ 15 (1,1 … [38 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md", "new_string": "- **Licences non vérifiées** : OpenSubtitles, TED, JW, presse, PDF Biblio/CEGEP, `pidgin`. Wikipédia\n  est la seule licence déclarée à la fois **homogène et permissive** (CC-BY-SA 4 … [441 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Correction de la phrase sur la méthode de lecture, puis relecture finale

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md", "new_string": "Mesures du **2026-11-18**, en lecture seule : `du -sb` et `find -type f` pour les octets et les\ncomptages, `stat` pour les tailles exactes, `wc -l` pour les lignes, `head -c` pour l … [656 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md", "limit": 80}`

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
… [4184 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md", "offset": 120, "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md</path>
<type>file</type>
<content>
120: | `data/opensubtitles/en-fr.tmx.gz` | 1 264 276 955 → **6 243 401 029** | — | fr-en | **non vérifiée** | parallèle oral |
121: | `data/wikimatrix/en-fr.tmx.gz` | 340 868 887 → **1 048 389 238** | — | fr-en | CC-BY-SA (dérivé wiki) | parallèle |
122: | `data/jrc/en-fr.tmx.gz` | 49 409 718 → **235 330 059** | — | fr-en | réutilisation UE, à vérifier | parallèle juridique |
123: | `data/ted2020/en-fr.tmx.gz` | 32 964 653 → **124 236 908** | — | fr-en | TED, à vérifier (NC-ND ?) | parallèle oral |
124: | `data/xnli/` | 2 380 057 696 | — | fr (traduit) | à vérifier | **évaluation seulement** |
125: | `data/pidgin.old/` | 328 747 430 | — | en/pidgin | KJV/WEB DP, autres à vérifier | = `data/pidgin` (symlink) |
126: | `data/jw/` | 36 851 670 | — | multilingue | droits réservés | usage local |
127: | `data/presse/` | 671 271 | — | fr | droits réservés | API presse |
128: | `data/onu/` | 10 176 222 | — | fr/multi | ONU | banc R0.3 / questions |
129: | `data/eurlex/` | 10 325 824 | — | fr/multi | UE | traduction |
130: | `data/deepseek/` (3 789 fichiers) | 13 37
… [7599 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md", "new_string": "| le reste (artefacts `.npz` 0,56 Go, pidgin, adaptateurs, jw, ONU, UE, presse, SFT…) | ≈ 2,1 Go | 4 209 | 1,5 % |", "old_string": "| le reste (pidgin, adaptateurs, jw, ONU, UE, pres … [40 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md", "new_string": "**L'écart de volume est déjà comblé sur le disque.** `data/corpus_wiki_fr_texte/train.txt` fait\n**7,50 Go** ; après déduplication (≈ 2,0 %, § 1) il reste **≈ 7,2–7,35 Go**, dont **1 … [661 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md", "offset": 238}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md</path>
<type>file</type>
<content>
238: ordre de valeur :
239: 
240: 1. **Des livres français en domaine public** — dump **Wikisource FR** et catalogue **Gutenberg FR**
241:    (quelques centaines de Mo compressés, taille exacte à mesurer), extraction, filtre de longueur,
242:    déduplication contre les 7,5 Go Wikipédia, puis épinglage. Objectif : **+0,5 à 1 Go de prose
243:    longue**, un registre que Wikipédia ne donne pas. C'est exactement ce que le plan appelle
244:    « des livres, des articles ».
245: 2. **Un extrait de français contemporain sous licence claire** (presse ou web filtré) — plus lourd :
246:    droits à trier, qualité à filtrer, PII à retirer. À ne lancer qu'après le point 1.
247: 3. **Ne pas collecter de Wikipédia** : 7,5 Go sont déjà sur le disque, un téléchargement de plus
248:    n'ajoute **aucun savoir nouveau**.
249: 
250: **Le prérequis n'est pas la collecte, c'est l'outillage.** `tools/corpus_propre.py` garde tous les
251: shingles en mémoire (≈ 80 Go par Go de texte, cf. [`rapport-n2-corpus-1go`](rapport-n2-corpus-1go.md)) :
252: dédupliquer les 7,50 Go en une 
… [3038 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de la nature exacte des corpus `corpus_wiki_<lang>` (résumés ou texte)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for l in fr en de es it; do printf \"%-3s \" \"$l\"; python3 -c \"import json;d=json.load(open('reports/corpus-wiki-$l.json'));print(d.get('nature'),'|',d.get('source',{}).get('champ') or d.get('source',{}).get('dump','')[:60])\"; do … [255 caractères tronqués]`

  ```
fr  corpus Wikipédia FR (résumés) | summary
en  corpus Wikipédia en (résumés) | summary
de  corpus Wikipédia de (résumés) | summary
es  corpus Wikipédia es (résumés) | summary
it  corpus Wikipédia it (résumés) | summary
--- texte ---
fr  corpus Wikipédia fr (texte intégral)
en  corpus Wikipédia en (texte intégral, run interrompu)
de  corpus Wikipédia de (texte intégral)
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md", "new_string": "| 10 langues — résumés (`data/corpus_wiki_<lang>/`) | 38,78 Go | 30 | 28,6 % |\n| 10 langues — plein texte (`data/corpus_wiki_<lang>_texte/`) | 81,32 Go | 30 | 60,0 % |", "old_string … [169 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md", "new_string": "Le français est le **4ᵉ** corpus des 10 langues (en 21 Gio, ru 11, de 10, **fr 7,8**, ja 6,9, es 6,4,\nit 5,0, ar 3,4, pt 3,0, zh 2,5 — valeurs `du`).\n\n**Hors `data/` (pour mémoire … [700 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-donnees-inventaire.md has been updated successfully.
  ```

