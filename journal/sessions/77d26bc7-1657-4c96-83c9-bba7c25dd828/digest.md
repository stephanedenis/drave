# Session DSH — relecture

- identifiant : `77d26bc7-1657-4c96-83c9-bba7c25dd828`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-07 00:49:20
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **re-auditer le produit sur les textes libres** avec le code de la nuit (23 h 30 → 00 h 50), en lecture seule.

Contexte : `tools/drave.py` (CLI : `analyser`, `--fichier`, `--jsonl`, `--partition`), `tools/bloc_linguistique.py`. Les audits précédents : `reports/rapport-fiabilite-produit.md` (50 textes, 0 plantage, 34/50 anomalies, 107 chevauchements) et `reports/rapport-frontieres-phrase.md` (40 textes, 32/40 frontières fausses avant correctif). Depuis : frontières de phrase, partition étiquetée, GN du pronom/nom propre, POS 86,25 %, F1 0,7535, attachement 236/237.

À faire :
1. **Rejouer les 50 textes** de `reports/pensee-fiabilite-produit.json` (banc_50.resultats) avec la CLI actuelle : plantages, refus, spans hors texte, chevauchements (les deux vues), POS sans classe, temps. **Compare aux chiffres de l'audit** (mêmes définitions, en le disant si ce n'est pas possible).
2. **Rejouer les 40 textes** de `reports/pensee-frontieres-phrase.json` : frontières, phrases, actes — confirmes-tu 0/40 fausses ?
3. **Nouveaux cas limites** (20 textes) : HTML, markdown, code, tableaux, langues non latines, très long, NFD, URL avec paramètres — plantages et contrats.
4. **Contrat** : les 8 champs obligatoires tiennent-ils sur ces textes ? Un client peut-il parser sans casser ?
5. Écris **uniquement** deux fichiers neufs : `reports/rapport-re-audit-produit.md` et `reports/pensee-re-audit-produit.json`.
6. Ne commite rien ; ne modifie aucun existant ; pas de `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, natifs.

Rends un résumé : avant/après (où c'est comparable), les plantages, les 3 prochains P0 du produit.
Your parent agent id is "e181ce02-cd50-488a-a6be-e84b79d40dcc". Before you finish, send your result to that agent with send_message({ agent_id: "e181ce02-cd50-488a-a6be-e84b79d40dcc", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Cartographie du dépôt et des audits existants avant de rejouer les textes

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -20 && git branch --show-current && ls reports/ | head -50", "description": "Vérifier branche et état du dépôt"}`

  ```
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
D  journal/2026-11-06/distribue.md
D  journal/2026-11-06/docs.md
D  journal/2026-11-06/memoire.md
D  journal/2026-11-06/mesures.md
D  journal/2026-11-06/modele.md
D  journal/2026-11-06/moteur.md
D  journal/2026-11-06/outils.md
D  journal/2026-11-06/portes.md
D  journal/2026-11-07/README.md
D  journal/2026-11-07/docs.md
D  journal/2026-11-07/mesures.md
s/v7
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
a80-porte-topologie.j
… [499 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la tools/drave.py tools/bloc_linguistique.py reports/pensee-fiabilite-produit.json reports/pensee-frontieres-phrase.json 2>&1", "description": "Vérifier existence des fichiers clés"}`

  ```
-rw-r--r--. 1 stephane stephane 103706  6 nov 12:52 reports/pensee-fiabilite-produit.json
-rw-r--r--. 1 stephane stephane 142486  6 nov 20:18 reports/pensee-frontieres-phrase.json
-rw-r--r--. 1 stephane stephane 144700  7 nov 00:08 tools/bloc_linguistique.py
-rw-------. 1 stephane stephane  20037  7 nov 00:38 tools/drave.py
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """drave.py — le point d'entrée produit du bloc linguistique.
3: 
4: Une seule commande, trois gestes, hors ligne et déterministe :
5: 
6:     python3 tools/drave.py analyser "Le chat dort."
7:     python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
8:     python3 tools/drave.py evaluer
9:     python3 tools/drave.py evaluer --gold --json
10:     python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
11:     python3 tools/drave.py --version
12: 
13: Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
14: avec rôle et cible d'attachement, pragmatique, unités sémantiques — et sa mesure sur le gold.
15: Ce qu'elle n'expose pas encore : le neuronal (`llama-cli` ou endpoint local), la restitution
16: (annotation → texte), la traduction et la génération : ils demandent des poids, un service ou
17: un GPU, alors que ce prototype est hors ligne, CPU et sans réseau.
18: 
19: Codes de sortie : 0 succès · 2 usage · 1 erreur (ou refus d'analyse).
20: """
21: 
… [20973 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nfor f in ['reports/pensee-fiabilite-produit.json','reports/pensee-frontieres-phrase.json']:\n    d=json.load(open(f))\n    print('===',f)\n    print('top keys:', list(d.keys())[:20])\n    for k,v in d.item … [296 caractères tronqués]`

  ```
=== reports/pensee-fiabilite-produit.json
top keys: ['rapport', 'ligne', 'branche', 'commit_mesure', 'commit_module', 'date', 'objet', 'verdict', 'snapshot', 'dispositif', 'banc_50', 'robustesse', 'contrat', 'schema_propose', 'test_non_regression', 'correctifs', 'controle_negatif', 'limites', 'fichiers']
  rapport = 'fiabilite-produit'
  ligne = 'B13'
  branche = 's/v7'
  commit_mesure = '56eb43af'
  commit_module = '1962eb15'
  date = '2026-11-06'
  objet = 'Audit de fiabilité du produit hors gold : 50 phrases libres via la CLI, robustesse des entrées, contrat de sortie, sché
  verdict = '⚠️ surface fiable (0 plantage, 0 JSON invalide, 0 span hors texte, 50/50 déterminisme) ; contrat non versionné et struc
  snapshot dict keys: ['drave_py_sha256', 'bloc_linguistique_sha256', 'bloc_linguistique_git', 'module_change_pendant_audit', 'note']
  dispositif dict keys: ['banc_50', 'mesure', 'machine', 'harnais', 'controle_negatif']
  banc_50 dict keys: ['synthese', 'resultats']
  robustesse dict keys: ['synthese', 'cas']
  contrat dict keys: ['enveloppe_actuelle', 'etiquette_actuelle', 'invariants_tenus', 'peut_etre_vide', 'ce_qui_casse_un_client']
  schema_propose dict keys: ['schema', '
… [1977 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nb=d['banc_50']\nprint('SYNTHESE:', json.dumps(b['synthese'],ensure_ascii=False,indent=1))\nprint('N resultats', len(b['resultats']))\nprint('PREM … [201 caractères tronqués]`

  ```
SYNTHESE: {
 "n": 50,
 "succes": 46,
 "refus": 4,
 "plantages": 0,
 "json_invalide": 0,
 "sorties_vides_sur_succes": 0,
 "spans_hors_texte": 0,
 "spans_vides": 0,
 "valeurs_vides": 0,
 "cles_racine_ko": 0,
 "cles_etiquette_ko": 0,
 "types_inconnus": 0,
 "cibles_absentes_du_texte": 0,
 "stderr_succes_non_vide": 0,
 "determinisme": "46/46",
 "labels": 4501,
 "mots": 1068,
 "pos": 766,
 "syntagmes": 360,
 "attachements": 284,
 "sans_attachement": 76,
 "syntagmes_par_type": {
  "GN": {
   "total": 87,
   "attaches": 83,
   "sans": 4,
   "union": 11
  },
  "GV": {
   "total": 145,
   "attaches": 75,
   "sans": 70,
   "union": 35
  },
  "GP": {
   "total": 86,
   "attaches": 84,
   "sans": 2,
   "union": 28
  },
  "REL": {
   "total": 28,
   "attaches": 28,
   "sans": 0,
   "union": 10
  },
  "SUB": {
   "total": 14,
   "attaches": 14,
   "sans": 0,
   "union": 1
  }
 },
 "chevauchements": {
  "textes": 23,
  "textes_tous_niveaux": 28,
  "paires": 107,
  "union_labels": 85,
  "apres_filtre_union": 0,
  "tous_impliquent_union": true
 },
 "phrases_type": 76,
 "phrases_espaces_initiaux": 19,
 "phrase_chevauchement_type": 1,
 "documents": 49,
 "doc_tronquees": 17,
 "doc_titres_faux": 2,
 "la
… [3233 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,200p reports/rapport-fiabilite-produit.md", "description": "Lire le rapport de fiabilité existant"}`

  ```
# Fiabilité du produit hors gold — 0 plantage sur 50 phrases, 4 refus sans JSON, 23/46 textes à chevauchement de syntagmes

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
> **Commit mesuré** : `56eb43af` (module `c1a08588`, `tools/drave.py` `59a06f3e`) ·
> **Date** : 2026-11-06 · **Verdict** : ⚠️ **la surface est fiable ; le contrat ne l'est pas encore.**
> **Aucun fichier existant modifié ; aucun commit.** Sorties : ce rapport et
> [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json).
>
> **Dispositif** : [`tools/drave.py`](../tools/drave.py) (CLI : `analyser`, `evaluer`, `rejouer`,
> `--version`) et [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) ;
> **50 phrases libres** écrites pour l'audit (textes dans le JSON) ; harnais local non committé
> dans `/tmp` ; machine **Xeon E5-2687W v3**, Python **3.13.16**.
>
> **Snapshot.** HEAD a bougé pendant l'audit (`6ef2a3f5` → `56eb43af`). Le module a reçu à
> **11 h 34** le correctif « non-str / surrogate » (`c1a08588`) ; le banc a tourné à **11 h 40**,
> après ce correctif, et `drave.py` n'a pas changé. Les chiffres portent sur ce couple de hash ;
> un audit futur doit repa
… [11035 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 200,420p reports/rapport-fiabilite-produit.md", "description": "Suite du rapport fiabilité"}`

  ```
| cas | résultat |
|---|---|
| UTF-8 valide (`Élodie sourit.`) | 0, JSON UTF-8 non échappé |
| **NFD** (`e` + accent combinant) | 0, mais tokens `e` / `́` / `lodie` ; **0 syntagme** ; POS `NOUN` pour `e` et `lodie` |
| BOM (`\ufeffLe chat dort.`) | 0 ; le BOM devient un token de **ponctuation** `[0:1]` |
| **octet UTF-8 invalide seul** (`\xff`) | 1, refus **`vide`** (pas `encodage`), stdout 0 |
| **octet invalide dans un mot** (`a\xffb`) | 1, **`UnicodeEncodeError` interne** à l'écriture du JSON, stdout 0 |
| stdout **ASCII** (`PYTHONIOENCODING=ascii`) | 1, **`UnicodeEncodeError` interne** (le tiret `—` de l'en-tête) |
| `LC_ALL=C` | 0, UTF-8 sort quand même (mode UTF-8 de Python 3.13) |

Deux **échecs internes** subsistent : l'UTF-8 invalide mêlé à des lettres et le stdout ASCII.
Aucun n'émet de traceback, mais le message est `drave: erreur : UnicodeEncodeError` — pas un
refus d'encodage explicite.

### 3.3 Les 10 000 caractères

| texte | code | temps CLI | étiquettes | JSON | constat |
|---|---:|---:|---:|---:|---|
| 10 000 car., phrases répétées | 0 | **590–765 ms** | 10 362 | **2 763 666 o** | spans valides, déterminisme |
| 10 000 car., `a` × 10 000 | 0 | **172 ms** | 7 | 42 
… [10398 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --since='2026-11-06 20:00' --pretty='%h %ad %s' --date=format:'%d %H:%M' | head -40", "description": "Voir les commits de la nuit"}`

  ```
149ecc5d 07 00:45 FICHE — LES TROIS RÈGLES DE SEGMENTATION REJETÉES (ADVERBE FINAL, ROGNAGE S, ADJ/ADV) ; LE F1 RESTE À 0,7535
5b9c18ef 07 00:39 PRODUIT — --fichier ET --jsonl (TRAITEMENT DE CORPUS, UNE LIGNE JSON PAR PHRASE) ; 16 TESTS
662a3698 07 00:31 PRODUIT — evaluer PUBLIE LES DEUX VUES (FIDÈLE F1 75,33 / LINÉAIRE 81,04, COUVERTURE 93,31) ; 14 TESTS
1f61caaa 07 00:27 FICHES — DIX FICHES ANNOTÉES « INSTANTANÉ HISTORIQUE » (L'ÉTAT COURANT EST 86,25 / 0,7535 / 236-237)
e9088d45 07 00:21 PRODUIT — LE VALIDATEUR PORTE --gold (20 PHRASES DU CORPUS VALIDÉES CONTRE LE SCHÉMA V1) : LA PORTE L'UTILISE
26c7b7ab 07 00:16 ROADMAP ET JOURNAL — LA NUIT FINIT À F1 0,7535, POS 86,25 %, 236/237, COUVERTURE 0,9916 ; LA CONVENTION DU SUJET
efbae885 07 00:13 B13 — LE NOM PROPRE SUJET EST UN GN : F1 0,7438 → 0,7535, TÊTE 0,865, ATTACHEMENT 236/237 ; 183/183
295e0d7b 07 00:05 B13 — LES PRONOMS SUJETS ANGLAIS AUSSI : F1 0,7013 → 0,7438, TÊTE 0,8561, ATTACHEMENT PRÉSERVÉ ; 183/183
a46e550b 06 23:58 ÉTAT — HORODATAGE CORRIGÉ (23 H 58, LE 06/11)
c78a53bd 06 23:55 B13 — LE PRONOM SUJET EST UN GN : F1 0,6519 → 0,7013 (+4,9), TÊTE 0,7709 → 0,8141, ATTACHEMENT PRÉSERVÉ (236/237, 0,9916) ; 183/183
5a067ba5 
… [3641 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"class Annotation\\|def json\\|SCHEMA\\|schema\\|version\\|def _phrases\\|def couverture\\|NIVEAUX\\|def analyser\" tools/bloc_linguistique.py | head -60", "description": "Repérer contrat et frontières dans le module"}`

  ```
50:NIVEAUX = ("graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
63:    def json(self) -> dict:
81:    def json(self) -> dict:
91:SCHEMA_ANNOTATION = "drave.annotation"
96:class Annotation:
115:    def couverture(self) -> dict[str, float]:
120:    def json(self, avec_duree: bool = False) -> dict:
125:            # le **format** est versionné : un client peut vérifier ce qu'il reçoit
126:            "schema": SCHEMA_ANNOTATION, "version": VERSION_ANNOTATION,
139:    def analyser(self, texte: str, langue: str | None = None,
170:    de test. Un profil est une donnée, pas un prompt : il se versionne et se rejoue.
839:    def _phrases(texte: str) -> list[tuple[int, int, str, str]]:
1297:    def analyser(self, texte: str, langue: str | None = None,
1676:    def analyser(self, texte: str, langue: str | None = None,
1747:    def analyser(self, texte: str, langue: str | None = None,
1774:            if e.get("niveau") not in NIVEAUX:
1857:    def analyser(self, texte: str, langue: str | None = None,
1991:    def analyser(self, texte: str, langue: str | None = None,
2083:    def analyser(self, texte: str, langue: str | None = None,
2161:    def analyser(self, texte: str,
… [483 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nprint(json.dumps(d['contrat'],ensure_ascii=False,indent=1)[:4000])\nprint('---ROBUSTESSE---')\nprint(json.dumps(d['robustesse']['synthese'],ensur … [90 caractères tronqués]`

  ```
{
 "enveloppe_actuelle": [
  "texte",
  "langue",
  "script",
  "source",
  "refus",
  "etiquettes",
  "unites_semantiques",
  "fraction_semantique",
  "trace",
  "cout",
  "contexte"
 ],
 "etiquette_actuelle": [
  "niveau",
  "type",
  "valeur",
  "debut",
  "fin",
  "source",
  "confiance",
  "candidats",
  "langue",
  "script",
  "meta"
 ],
 "invariants_tenus": {
  "cles_racine": "46/46",
  "cles_etiquette": "4501/4501",
  "labels_tries": "46/46",
  "doublons_exacts": 0,
  "spans_dans_texte": "4501/4501",
  "spans_vides": 0,
  "confiance_0_1": "4501/4501",
  "source_dans_enum": "4501/4501",
  "niveau_dans_enum": "4501/4501",
  "texte_roundtrip": "46/46",
  "determinisme": "46/46",
  "stderr_vide": "46/46"
 },
 "peut_etre_vide": {
  "etiquettes": "seulement sur refus (0/46 succès)",
  "unites_semantiques": "f18 (chiffres) : 0 ; fraction 0,0",
  "fraction_semantique": "0,0 sur f18 ; max 0,8571 sur f03",
  "syntagmes": "4/46 succès : f13, f18, f27 (Élodie sourit.), f37",
  "pos": "1/46 : f18 (chiffres) ; sinon 3 à 200 POS",
  "candidats": "3470/4501 étiquettes : graphème, mot, phrase, document, POS fermées",
  "meta": "3375/4501 étiquettes : graphème, mot, phrase, pragmatique, disc
… [2051 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 40, "limit": 160}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
40: import subprocess
41: import sys
42: import threading
43: import time
44: import unicodedata
45: import urllib.request
46: from dataclasses import dataclass, field
47: from typing import Protocol, Sequence
48: 
49: RACINE = pathlib.Path(__file__).resolve().parent.parent
50: NIVEAUX = ("graphème", "morphème", "mot", "pos", "syntagme", "phrase", "discours",
51:            "pragmatique", "document")
52: SOURCES = ("heuristique", "neuronal", "humain")
53: SCRIPT_NEUTRE = "Zyyy"
54: 
55: # --------------------------------------------------------------------------- types
56: 
57: 
58: @dataclass(frozen=True)
59: class Span:
60:     debut: int
61:     fin: int
62: 
63:     def json(self) -> dict:
64:         return {"debut": self.debut, "fin": self.fin}
65: 
66: 
67: @dataclass
68: class Etiquette:
69:     niveau: str
70:     type: str
71:     valeur: str
72:     debut: int
73:     fin: int
74:     source: str = "heuristique"
75:     confiance: float = 0.5
76:     candidats: list[str] = field(default_factory=list)
77:     langue: str = "und"
78:     script: str = SCRIPT_
… [5472 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 780,980p tools/bloc_linguistique.py", "description": "Lire la logique de frontières de phrase"}`

  ```
j += 1
        if not _dans_zone(zones, i, j) and _est_frontiere(texte, i, j, zones):
            ajouter(_absorber_fermants(texte, j), _type_phrase(texte[i:j]))
        i = j
    ajouter(n, "déclarative")
    return sortie


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
        # Dans les deux filtres, le segment retiré reste dans `meta.alter
… [8514 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 640,790p tools/bloc_linguistique.py", "description": "Lire le découpage de phrases actuel"}`

  ```
if d >= fin:
            break
        if f > debut:
            return True
    return False


def _mot_avant(texte: str, i: int) -> str:
    j = i
    while j > 0 and (texte[j - 1].isalnum() or texte[j - 1] in "'’"):
        j -= 1
    return texte[j:i]


def _apres_ponctuation(texte: str, j: int) -> int:
    n = len(texte)
    while j < n and (texte[j].isspace() or texte[j] in _FERMANTS):
        j += 1
    return j


def _mot_suivant(texte: str, p: int) -> str:
    m = re.match(r"[^\W\d_][\w'’\-]*", texte[p:p + 80], re.UNICODE)
    return m.group() if m else ""


def _absorber_fermants(texte: str, j: int) -> int:
    """Absorbe « . » », « . ) » : le fermant appartient à la phrase qui se termine."""
    n = len(texte)
    while True:
        k = j
        while k < n and texte[k] in " \t":
            k += 1
        if k < n and texte[k] in _FERMANTS:
            j = k + 1
            continue
        return j


def _nouvelle_ligne_structurelle(texte: str, i: int, j: int) -> bool:
    """Un saut de ligne coupe la phrase s'il est vide ou s'il borde un titre / une liste."""
    if texte.count("\n", i, j) >= 2:
        return True
    avant = texte[texte.rfind("\n", 0, i) + 1:i]
  
… [4036 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nd=json.load(open('reports/pensee-frontieres-phrase.json'))\nprint(json.dumps(d['resume_40'],ensure_ascii=False,indent=1))\nprint('--- verdict')\nprint(json.dumps(d['verdict'],ensure_ascii=False,indent=1))\ … [371 caractères tronqués]`

  ```
{
 "avant": {
  "phrases": 102,
  "textes_exacts": 2,
  "textes_frontiere_fausse": 32,
  "textes_casses": 38,
  "extra": 47,
  "missing": 4,
  "overlaps": 9,
  "leading": 31,
  "vides": 0,
  "fausses_questions": 5,
  "types_faux": 63
 },
 "apres": {
  "phrases": 59,
  "textes_exacts": 40,
  "textes_frontiere_fausse": 0,
  "textes_casses": 0,
  "extra": 0,
  "missing": 0,
  "overlaps": 0,
  "leading": 0,
  "vides": 0,
  "fausses_questions": 0,
  "types_faux": 0
 }
}
--- verdict
{
 "frontieres": "40/40 textes exacts après patch (2/40 avant), 32/40 frontières fausses avant, 0 après",
 "dev_test": "delta 0 sur POS, F1 syntagmes, attachement et tokens ; 2 spans de phrase du gold corrigés ; 0 valeur d'acte changée",
 "tokénisation": "patch B : 477 → 362 tokens, 273 → 232 POS, 47 POS dans des fragments URL/courriel/chemin supprimés, 0 token du gold changé",
 "recommandation": "appliquer A (frontières) ; B est indépendant et additif, à appliquer si le contrat accepte les types courriel/chemin"
}
--- dispositif
{
 "banc": "40 textes libres écrits pour l'analyse (59 phrases attendues), catégories URL, courriel, chemin, décimaux, dates, versions/IP, abréviations, ellipses, guillemets, listes,
… [2786 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py analyser \"Le chat dort.\" --json | head -40 && echo \"---\" && python3 tools/drave.py analyser \"\" --json; echo \"rc=$?\"", "description": "Tester la CLI actuelle"}`

  ```
{
 "schema": "drave.annotation",
 "version": 1,
 "texte": "Le chat dort.",
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
---
{
 "schema": "drave.annotation",
 "version": 1,
 "texte": "",
 "langue": "und",
 "script": "Zyyy",
 "source": "heuristique",
 "refus": "vide",
 "etiquettes": [],
 "unites_semantiques": [],
 "fraction_semantique": 0.0,
 "trace": [
  {
   "etape": "refus",
   "raison": "vide"
  }
 ],
 "cout": {
  "octets": 0
 },
 "contexte": ""
}
rc=3
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nfor r in d['banc_50']['resultats']:\n    print(r['id'], r['categorie'], repr(r['texte'])[:90])\n\"", "description": "Lister les 50 textes du banc … [2 caractères tronqués]`

  ```
f01 fr 'Le chat dort.'
f02 fr 'Le chat de la voisine qui dort sur le toit se réveille.'
f03 fr "Bonjour ! Comment allez-vous aujourd'hui ?"
f04 fr "Ferme la porte, s'il te plaît."
f05 fr 'Ne touche pas à ça !'
f06 fr "Je ne pense pas qu'il viendra demain, mais nous verrons bien."
f07 en 'The cat sleeps on the roof.'
f08 en 'Where is the nearest train station, please?'
f09 en "Don't forget to bring your passport."
f10 fr 'Le prix est de 1 234,56 € pour 3 articles.'
f11 fr 'Rendez-vous le 12/03/2026 à 14h30.'
f12 fr 'Visitez https://example.com/docs?page=2 pour la documentation.'
f13 fr "J'ai trouvé ça génial 😍🔥"
f14 refus '🚀'
f15 refus ''
f16 refus '   '
f17 refus '...'
f18 fr '1234567890'
f19 fr "COVID-19 : la situation s'améliore-t-elle vraiment ?"
f20 fr 'M. Dupont, le Dr Martin et Mme Leroy sont arrivés vers 9 h.'
f21 fr '« Je ne sais pas », répondit-il en haussant les épaules.'
f22 fr "C'est l'été ; les oiseaux chantent, les enfants jouent."
f23 fr 'Attention : ce produit peut contenir des traces de noisettes.'
f24 fr 'Il était une fois une petite fille qui vivait au bord de la forêt...'
f25 fr 'Pourquoi ? Parce que.'
f26 fr 'Où sont les toilettes ? Je cherche depuis dix minute
… [1555 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nd=json.load(open('reports/pensee-frontieres-phrase.json'))\nc=d['corpus_40']\nprint('keys item', sorted(set(k for r in c for k in r)))\nfor r in c[:4]:\n    print(json.dumps(r,ensure_ascii=False,indent=1)[ … [239 caractères tronqués]`

  ```
keys item ['apres', 'attendu', 'avant', 'cat', 'effet', 'id', 'texte']
{
 "id": "n01",
 "cat": "négatif/2 phrases",
 "texte": "Il part. Elle reste.",
 "attendu": [
  {
   "debut": 0,
   "fin": 8,
   "texte": "Il part.",
   "type": "déclarative"
  },
  {
   "debut": 9,
   "fin": 20,
   "texte": "Elle reste.",
   "type": "déclarative"
  }
 ],
 "avant": {
  "phrases": 2,
  "exact": false,
  "frontiere_fausse": false,
  "casse": true,
  "extra": [],
  "missing": [],
  "overlaps": [],
  "leading": [
   8
  ],
  "vides": [],
  "fausses_questions": [],
  "spans": [
   {
    "debut": 0,
    "fin": 8,
    "texte": "Il part.",
    "type": "déclarative"
   },
   {
    "debut": 8,
    "fin": 20,
    "texte": " Elle reste.",
    "type": "déclarative"
   }
  ]
 },
 "apres": {
  "phrases": 2,
  "exact": true,
  "frontiere_fausse": false,
  "casse": false,
  "extra": [],
  "missing": [],
  "overlaps": [],
  "leading": [],
  "vides": [],
  "fausses_questions": [],
  "spans": [
   {
    "debut": 0,
    "fin": 8,
    "texte": "Il part.",
    "type": "déclarative"
   },
   {
    "debut": 9,
    "fin": 20,
    "texte": "Elle reste.",
    "type": "déclarative"
   }
  ]
 },
 "effet": {
  "pos_identique":
… [6503 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"acte\\|frontiere_fausse\\|textes_casses\\|exact\" reports/rapport-frontieres-phrase.md | head -40 && echo ---- && sed -n 1,80p reports/rapport-frontieres-phrase.md", "description": "Lire définitions du rapport frontières"}`

  ```
12:> les mesures et les patchs exacts).
21:textes sont exacts, **0** défaut, **0** chevauchement, **0** fausse question. Sur le **gold 612**, POS,
23:phrase** se décalent d'un espace (r308, r318), **0 valeur d'acte** change. **Le gain dev/test est donc
26:libre : **63 actes faux sur 102 phrases → 0 sur 59**.
67:| textes exacts (spans + types) | 2/40 | **40/40** | 40/40 |
76:| actes faux par phrase | 63/102 | **0/59** | 0 |
235:- **38/40** textes changent de libellés `phrase` et de spans d'acte ; **5/40** changent de connecteurs
236:  `discours` (fragments d'URL supprimés, spans corrigés). Les **actes faux** passent de **63/102** à
250:| règle | textes exacts (seule) | coupures retirées* | fusions réparées* | espaces retirés* | fausses questions retirées* | Δ dev POS / F1 / att | Δ test POS / F1 / att |
267:gain de textes exacts à lui seul, 13/40) ; (f) les titres et listes sans ponctuation finale. **Toutes**
272:| lecture | POS dev | F1 dev | att dev | acte dev | POS test | F1 test | att test | acte test |
285:F1 syntagmes, attachement et acte, sur dev comme sur test. Le seul déplacement est le **span** de
286:2 phrases du gold (r308, r318), dû à la règle (e) ; **la valeur d'acte n
… [5538 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '\"acte\"\\|acte=\\|def _pragmatique\\|assertion\\|exclamation' tools/bloc_linguistique.py | head -30 && sed -n '/def _pragmatique/,/return/p' tools/bloc_linguistique.py | head -80", "description": "Lire la logique d'actes pr … [12 caractères tronqués]`

  ```
1471:                    "exclamation" if typ == "exclamative" else
1472:                    "ordre" if premier.casefold() in VERBES_IMPERATIFS else "assertion")
1473:            etiquettes.append(Etiquette("pragmatique", "acte", acte, d, f, self.nom, 0.45,
1474:                                        candidats=["assertion", "question", "ordre"],
1703:                    "exclamation" if typ == "exclamative" else "assertion")
1704:            etiquettes.append(Etiquette("pragmatique", "acte", acte, d, f, self.nom, 0.8,
2103:ACTES = ("assertion", "question", "exclamation")
2119:    `grammaire_pragma` : l'acte (`assertion`, `question`, `exclamation`), puis trois
2144:                "UNIQUEMENT par un objet JSON {\"acte\":\"assertion|question|exclamation\","
2179:            acte = str(donnees.get("acte", "")).lower()
2186:            etiquettes = [Etiquette("pragmatique", "acte", acte, 0, n, self.nom,
2406:    ("pragmatique", "acte"): "neuronal",
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nfor t in [\"Il part. Elle reste.\",\"Le prix est 12.5 euros.\",\"Pourquoi ? Parce que.\",\"M. Dupont…\",\"Le 12.03.2024. Il part.\"]:\n   … [294 caractères tronqués]`

  ```
'Il part. Elle reste.' [(0, 8, 'déclarative', 'Il part.'), (9, 20, 'déclarative', 'Elle reste.')]
  prag: [('type', 'déclarative', 0, 8), ('acte', 'assertion', 0, 8), ('type', 'déclarative', 9, 20), ('acte', 'assertion', 9, 20)]
'Le prix est 12.5 euros.' [(0, 23, 'déclarative', 'Le prix est 12.5 euros.')]
  prag: [('type', 'déclarative', 0, 23), ('acte', 'assertion', 0, 23)]
'Pourquoi ? Parce que.' [(0, 10, 'interrogative', 'Pourquoi ?'), (11, 21, 'déclarative', 'Parce que.')]
  prag: [('type', 'interrogative', 0, 10), ('acte', 'question', 0, 10), ('type', 'déclarative', 11, 21), ('acte', 'assertion', 11, 21)]
'M. Dupont…' [(0, 10, 'déclarative', 'M. Dupont…')]
  prag: [('type', 'déclarative', 0, 10), ('acte', 'assertion', 0, 10)]
'Le 12.03.2024. Il part.' [(0, 14, 'déclarative', 'Le 12.03.2024.'), (15, 23, 'déclarative', 'Il part.')]
  prag: [('type', 'déclarative', 0, 14), ('acte', 'assertion', 0, 14), ('type', 'déclarative', 15, 23), ('acte', 'assertion', 15, 23)]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1297,1400p tools/bloc_linguistique.py", "description": "Lire le pipeline d'analyse"}`

  ```
def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        t0 = time.perf_counter()
        if not isinstance(texte, str):
            # une entrée non textuelle est **refusée** proprement (le produit ne plante pas)
            return Annotation(texte=str(texte)[:200], refus="non_texte", source=self.nom,
                              trace=[{"etape": "refus", "raison": "non_texte",
                                      "type": type(texte).__name__}],
                              cout={"octets": 0, "duree_s": round(time.perf_counter() - t0, 6)})
        texte = texte or ""
        trace: list[dict] = []
        if not texte.strip() or not any(ch.isalpha() or ch.isdigit() for ch in texte):
            return Annotation(texte=texte, refus="vide", source=self.nom,
                              trace=[{"etape": "refus", "raison": "vide"}],
                              cout={"octets": len(texte.encode("utf-8", "replace")), "duree_s": round(time.perf_counter() - t0, 6)})

        lg, conf_lg, script = self._langue(texte, langue)
        trace.append({"etape": "langue", "langue": lg, "script": script, "confiance": conf_l
… [5068 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-frontieres-phrase.json'))\nfor r in d['corpus_40']:\n    print(r['id'], r['cat'], '|', repr(r['texte'])[:100])\n    if r.get('effet',{}).get('acte_labels_differents'):\ … [105 caractères tronqués]`

  ```
n01 négatif/2 phrases | 'Il part. Elle reste.'
   effet acte diff: {'pos_identique': True, 'syntagme_identique': True, 'attachement_identique': True, 'phr_avant': 2, 'phr_apres': 2, 'phrase_labels_differents': True, 'acte_labels_differents': True, 'syntagmes_traversants_avant': 0, 'syntagmes_traversants_apres': 0, 'pos_labels': 4, 'syntagme_labels': 4}
n02 négatif/3 phrases | 'Il part. Elle reste. Nous attendons.'
   effet acte diff: {'pos_identique': True, 'syntagme_identique': True, 'attachement_identique': True, 'phr_avant': 3, 'phr_apres': 3, 'phrase_labels_differents': True, 'acte_labels_differents': True, 'syntagmes_traversants_avant': 0, 'syntagmes_traversants_apres': 0, 'pos_labels': 6, 'syntagme_labels': 6}
d01 décimal | 'Le prix est 12.5 euros.'
   effet acte diff: {'pos_identique': True, 'syntagme_identique': True, 'attachement_identique': True, 'phr_avant': 2, 'phr_apres': 1, 'phrase_labels_differents': True, 'acte_labels_differents': True, 'syntagmes_traversants_avant': 0, 'syntagmes_traversants_apres': 0, 'pos_labels': 4, 'syntagme_labels': 3}
d02 décimal+milliers | 'La remise est de 12,5 % sur 1.234,56 euros.'
   effet acte diff: {'pos_identique': True, 'syntagme_ide
… [13129 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 215,245p reports/rapport-frontieres-phrase.md && sed -n 300,345p reports/rapport-frontieres-phrase.md", "description": "Lire la définition des actes faux"}`

  ```
Après : **2** phrase(s) — `1. Ouvrir le fichier.` | `2. Lire la première ligne.`


**x01 — ellipse minuscule**
~~~text
Il hésite... puis il part.
~~~

Attendu : **1** phrase(s) — `Il hésite... puis il part.`

Avant : **2** phrase(s) — `Il hésite...` | ` puis il part.`

Après : **1** phrase(s) — `Il hésite... puis il part.`


### 2.4 Effet sur POS, syntagmes et attachement

- **Le patch de frontières ne change aucun POS, aucun syntagme, aucun attachement** : **0/40** textes
  modifiés sur ces trois niveaux, et **0/612** sur le gold. C'est structurel : `_pos` et `_syntagmes_*`
  ne lisent pas `_phrases` ; seuls `phrase`, `pragmatique` et `discourse` en dépendent.
- **38/40** textes changent de libellés `phrase` et de spans d'acte ; **5/40** changent de connecteurs
  `discours` (fragments d'URL supprimés, spans corrigés). Les **actes faux** passent de **63/102** à
  **0/59**.
- **Syntagmes traversant une frontière** : **0 → 2** (`t01`, `t02`). Ce n'est pas la frontière qui est
  fausse : le chunker S traite `de réunion\n\nLe budget` et `les coûts\n- Échéance` comme des syntagmes.
  La règle (f) révèle ce défaut du chunker (P0-3/P1-4), elle ne le crée pas.
- **Patch B (tokénisation)** 
… [3065 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"acte\" reports/rapport-frontieres-phrase.md | head -30", "description": "Chercher actes dans le rapport"}`

  ```
23:phrase** se décalent d'un espace (r308, r318), **0 valeur d'acte** change. **Le gain dev/test est donc
26:libre : **63 actes faux sur 102 phrases → 0 sur 59**.
76:| actes faux par phrase | 63/102 | **0/59** | 0 |
235:- **38/40** textes changent de libellés `phrase` et de spans d'acte ; **5/40** changent de connecteurs
236:  `discours` (fragments d'URL supprimés, spans corrigés). Les **actes faux** passent de **63/102** à
272:| lecture | POS dev | F1 dev | att dev | acte dev | POS test | F1 test | att test | acte test |
285:F1 syntagmes, attachement et acte, sur dev comme sur test. Le seul déplacement est le **span** de
286:2 phrases du gold (r308, r318), dû à la règle (e) ; **la valeur d'acte ne change pas**. C'est le
321:| valeurs d'acte | référence | identique | 0 texte différent |
329:métrique ne bouge (POS 0,8490 / 0,8511 ; F1 0,6439 / 0,6552 ; att 0,9816 / 0,9868 ; acte 1,0000 /
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"34\\|anomal\" reports/rapport-fiabilite-produit.md | head -30", "description": "Chercher le chiffre 34/50 dans le rapport"}`

  ```
15:> **11 h 34** le correctif « non-str / surrogate » (`c1a08588`) ; le banc a tourné à **11 h 40**,
88:| anomalie | mesure | où / exemple |
94:| `POS —` | **1/46** | f18, `1234567890` |
100:| faux titres de document | **2/49** | f18 (`1234567890`), f31 (`ÇA NE MARCHE PAS !!!`) |
126:une limite ou un texte sans structure. Même chose pour `1234567890` (`POS —`, `SYNTAGMES —`,
156:Le **démarrage** (`--version`, 10 passages) coûte **134–192 ms**, médiane **146 ms**. Pour une
186:| texte commençant par `--` (`--bonjour`) | 0 | **2** | 0 | **anomalie** : pris pour une option |
257:| `candidats` | **3470/4501** étiquettes : graphème, mot, phrase, document, POS fermées |
422:    "1234567890",
583:| **P1-7** | **Compacité et lot** : `--compact`, JSONL, `--fichier`/stdin | **2,76 Mo** pour 10 k ; **11,5 Mo** pour 50 k ; 1 texte par appel | `drave.py` 50-52, 329-341 | **0,5–1 j** | faible : option additive |
593:| **P2-3** | `contexte` : l'exposer ou le retirer | **46/46** vide ; aucune option CLI | `bloc_linguistique.py` 1237-1239 ; `drave.py` 329-341 | **1 h** |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nd=json.load(open('reports/pensee-frontieres-phrase.json'))\n# current spans for 40\nexact=0; ff=0; extra=0; missing=0; overlap=0; leading … [1307 caractères tronqués]`

  ```
phrases 59 exact 0 ff 0 extra 0 missing 0 overlaps 0 leading 20 fq 0 types_faux 59
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nd=json.load(open('reports/pensee-frontieres-phrase.json'))\nexact=0; ff=0; extra=0; missing=0; overlap=0; leading=0; fq=0; typf=0; phrase … [1541 caractères tronqués]`

  ```
phrases 59 exact 40 ff 0 extra 0 missing 0 overlaps 0 leading 20 fq 0 types_faux 0 actes_faux 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -V && uname -srm && nproc && python3 tools/drave.py analyser --json -- \"test\" >/dev/null; echo \"sep rc=$?\"; python3 tools/drave.py analyser --json -- \"-3 degrés\" >/dev/null; echo \"neg rc=$?\"", "description": "Vérifier … [33 caractères tronqués]`

  ```
Python 3.13.16
Linux 7.2.6-1-default x86_64
40
sep rc=0
neg rc=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nd=json.load(open('reports/pensee-frontieres-phrase.json'))\nlead=0\nfor r in d['corpus_40']:\n    for a,b,tx,ty in bl.decouper_phrases(r[ … [203 caractères tronqués]`

  ```
phrases commençant par espace: 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\ndef walk(o,p=''):\n    if isinstance(o,dict):\n        for k,v in o.items(): walk(v,p+'/'+str(k))\n    elif isinstance(o,list) and o and isin … [280 caractères tronqués]`

  ```
/robustesse/synthese/anomalies = 9
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"34/50\\|34 / 50\\|anomalies\" reports/rapport-fiabilite-produit.md reports/*.md | head -20", "description": "Chercher 34/50 dans les rapports"}`

  ```
reports/INDEX.md:622:| [rapport-produit-bloc-l.md](rapport-produit-bloc-l.md) | Audit produit du bloc linguistique — 0 plantage sur 50 phrases, 34/50 avec une anomalie de contrat |
reports/rapport-etat-a.md:139:- `rapport-produit-bloc-l.md` : **50 phrases**, **0 plantage**, **34/50** avec au moins une anomalie,
reports/rapport-gold-anglais.md:342:- [`pensee-gold-anglais.json`](pensee-gold-anglais.json) — chiffres, spans, cibles, anomalies, contrôles.
reports/rapport-produit-bloc-l.md:1:# Audit produit du bloc linguistique — 0 plantage sur 50 phrases, 34/50 avec une anomalie de contrat
reports/rapport-produit-bloc-l.md:20:jamais une sortie vide** et garde **tous les offsets** ; mais **34/50 textes** portent au moins une
reports/rapport-produit-bloc-l.md:124:| textes avec au moins une anomalie | **34/50** |
reports/rapport-produit-bloc-l.md:125:| anomalies détectées | **149** |
reports/rapport-produit-bloc-l.md:318:| **P1-9** | **Rendre le repli S visible** | sans générateur S : **34/50** sorties changent, **132 syntagmes** et **119 attachements** perdus, sans trace | 641-650, 652-667 | **2 h** | faible : trace `repli_s` + champ de mode, ou échec explicite |
reports/rapport-produit-b
… [104 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,160p reports/rapport-produit-bloc-l.md", "description": "Lire le rapport produit-bloc-l (34/50)"}`

  ```
# Audit produit du bloc linguistique — 0 plantage sur 50 phrases, 34/50 avec une anomalie de contrat

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **HEAD vérifié en fin d'audit** : `c6904284`
> (le HEAD a bougé pendant l'audit ; module `bloc_linguistique.py` inchangé ; `evaluer_gold.py`
> modifié en `7f73c17f`) ·
> **Date** : 2026-11-06 ·
> **Verdict** : ⚠️ **la surface est utilisable en autonomie ; la structure ne l'est pas encore.**
> **Aucun fichier existant modifié par cet audit ; aucun commit.** Sorties : ce rapport et
> [`pensee-produit-bloc-l.json`](pensee-produit-bloc-l.json).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ; **50 phrases libres** écrites pour
> l'audit (textes dans le JSON) ; harnais local non committé dans `/tmp/audit_produit_bl`.
> **Porte** : `bash tools/porte-bloc-linguistique.sh` → **verte** (16 tests, autotest UDHR
> **0,9687**, profils permutés **0,0022**).

**En une phrase.** Sur 50 phrases libres
… [9453 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short tools/ && git log -1 --format='%h %ad %s' --date=iso -- tools/drave.py && sha256sum tools/drave.py tools/bloc_linguistique.py && grep -rn \"8 champs\\|drave.annotation\\|schema.*version\\|version.*1.0\" docs/ READM … [86 caractères tronqués]`

  ```
m tools/structures
5b9c18ef 2026-11-07 00:39:21 -0500 PRODUIT — --fichier ET --jsonl (TRAITEMENT DE CORPUS, UNE LIGNE JSON PAR PHRASE) ; 16 TESTS
88ce03da9d9e11e48bc352083aaa94dd492b80798ef31268a1219689a78d463c  tools/drave.py
858197f736d758be2ca97e1ccd71a5045fd47d19d31c50afaf13fd669893b47f  tools/bloc_linguistique.py
docs/archive/cerveau-facultes.md:137:*(La première version mesurait la perplexité sur les **1 024 premiers jetons** — c'est-à-dire le
docs/schemas/decision.puml.svg:2:<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" data-diagram-type="ACTIVITY" style="width:462px;height:426px;background:#FFFFFF;" width="462px" height="426px" viewBox="0 0 462 426" zoomAndPan="magnify" preserveAspectRatio="none" contentStyleType="text/css"><title>Diagramme PlantUML</title><desc>Généré par PlantUML</desc><?plantuml 1.2026.9?><defs/><g font-family="sans-serif" lengthAdjust="spacing"><g class="title" data-source-line="1"><text x="126.595" y="34.966" fill="#000" font-size="14" textLength="206.849" font-weight="700">Choisir la source d'un schéma</text></g><ellipse cx="228.26" cy="65.068" rx="10" ry="10" fill="#222" style="stroke:#222;stroke-wid
… [7260 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/pensee-produit-bloc-l.json && python3 - <<'EOF'\nimport json\na=json.load(open('reports/pensee-fiabilite-produit.json'))['banc_50']['resultats']\nb=json.load(open('reports/pensee-produit-bloc-l.json'))['banc_50']['detail'] … [219 caractères tronqués]`

  ```
reports/pensee-produit-bloc-l.json
new 50 old 50 intersection 0
old keys ['anomalies', 'anomalies_n', 'attachements', 'attendu', 'cat', 'etiquettes', 'fraction', 'id', 'langue', 'mots', 'niveaux', 'niveaux_absents', 'script', 'texte']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 20,45p README.md && echo === && sed -n 350,380p docs/produit/README.md", "description": "Lire le contrat publié"}`

  ```
```bash
python3 tools/drave.py analyser "Le chat de la voisine qui dort sur le toit se réveille."
python3 tools/drave.py analyser "The cat that sleeps on the roof is black." --langue en --json
python3 tools/drave.py evaluer        # la mesure sur le gold (POS, F1, attachement)
python3 tools/drave.py rejouer "Le chat dort."   # vérifie le déterminisme (sha256)
```

Sortie : une **annotation** — langue, classes de mots, syntagmes avec rôle et **cible
d'attachement**, acte de parole — avec ses spans et sa confiance, de façon **déterministe**. Le
**format est versionné** (`schema: "drave.annotation"`, `version: 1`, schéma publié dans
[`tools/schemas/`](tools/schemas/), un refus est une réponse JSON avec le code 3). La notice
complète est [`docs/produit/README.md`](docs/produit/README.md), les exemples vérifiés
[`docs/produit/exemples.md`](docs/produit/exemples.md), et la porte produit
`bash tools/porte-produit.sh` (10 contrôles, ~2 min).

**Mesuré au 06/11** : POS **85,00 %**, syntagmes F1 **0,6482**, attachement **235/236**
(couverture **0,9874**), 183/183 portes. Les limites sont dites : 3 spans inatteignables, la
restitution et la traduction ne sont pas encore là.

## L'origine

Dra
… [2772 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"drave.annotation\" --include='*.py' --include='*.md' . | grep -v archive | head -20", "description": "Chercher les usages du schéma"}`

  ```
./reports/rapport-fiabilite-produit.md:295:Le schéma **`drave.annotation` v1.0** garde **8 champs obligatoires** et laisse les autres en
./reports/rapport-fiabilite-produit.md:300:| 1 | `schema` | `"drave.annotation"` | famille de format |
./reports/rapport-fiabilite-produit.md:317:  "title": "drave.annotation v1.0",
./reports/rapport-fiabilite-produit.md:322:    "schema": {"const": "drave.annotation"},
./reports/rapport-fiabilite-produit.md:383:- **cible v1** (`schema: "drave.annotation"`, `version: "1.0"`, 8 champs requis) : il est
./reports/rapport-fiabilite-produit.md:404:SCHEMA = "drave.annotation"
./reports/rapport-schema-v1.md:8:> **Ce qui change pour un client** : le JSON porte désormais **`schema`** (`"drave.annotation"`)
./reports/rapport-schema-v1.md:12:> **Le schéma est publié** : [`tools/schemas/drave-annotation-v1.json`](../tools/schemas/drave-annotation-v1.json)
./reports/rapport-schema-v1.md:33:| 1 | **format versionné** | 11 clés sans `schema`/`version` | **13 clés**, `schema="drave.annotation"`, `version=1` |
./reports/rapport-schema-v1.md:58:1. ~~Publier le schéma~~ — **fait** (`tools/schemas/drave-annotation-v1.json`, validé, 9e contrôle).
./tools/tests/test_pro
… [1086 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/schemas/drave-annotation-v1.json | head -120 && echo === && sed -n 1,80p reports/rapport-schema-v1.md", "description": "Lire le schéma v1 publié"}`

  ```
{
 "$schema": "https://json-schema.org/draft/2020-12/schema",
 "$id": "https://drave.local/schema/annotation-v1.json",
 "title": "drave.annotation v1",
 "description": "L'annotation du bloc linguistique heuristique : un texte, ses étiquettes par niveau, ses unités sémantiques et son refus éventuel.",
 "type": "object",
 "required": [
  "schema",
  "version",
  "texte",
  "langue",
  "script",
  "refus",
  "etiquettes",
  "unites_semantiques"
 ],
 "properties": {
  "schema": {
   "const": "drave.annotation"
  },
  "version": {
   "const": 1
  },
  "texte": {
   "type": "string"
  },
  "langue": {
   "type": "string",
   "pattern": "^[a-z]{2,3}$|^und$"
  },
  "script": {
   "type": "string"
  },
  "source": {
   "type": "string"
  },
  "refus": {
   "type": "string",
   "enum": [
    "",
    "vide",
    "non_texte",
    "trop_long",
    "neuronal"
   ]
  },
  "etiquettes": {
   "type": "array",
   "items": {
    "type": "object",
    "required": [
     "niveau",
     "type",
     "valeur",
     "debut",
     "fin",
     "source",
     "confiance"
    ],
    "properties": {
     "niveau": {
      "type": "string"
     },
     "type": {
      "type": "string"
     },
     "valeur": {
 
… [4627 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,80p tools/verifier_schema_produit.py && echo === && sed -n 1,80p tools/tests/test_schema_produit.py", "description": "Lire le vérificateur et le test du schéma"}`

  ```
#!/usr/bin/env python3
"""verifier_schema_produit.py — valide une annotation `drave.annotation` contre le schéma v1.

Le schéma publié est `tools/schemas/drave-annotation-v1.json` (Draft 2020-12). Ce vérificateur compile le
schéma une fois, puis valide les annotations de cas choisis : français, anglais, refus (texte
vide), entrée non textuelle, texte très long. Il ne dépend que de `fastjsonschema` (sinon il se
rabat sur une validation minimale des 8 champs obligatoires).

Usage :
    python3 tools/verifier_schema_produit.py              # 5 cas, sortie 0/1
    python3 tools/verifier_schema_produit.py --json       # le détail des cas
    python3 tools/verifier_schema_produit.py --aide
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parents[1]
SCHEMA = RACINE / "tools" / "schemas" / "drave-annotation-v1.json"
OBLIGATOIRES = ("schema", "version", "texte", "langue", "script", "refus",
                "etiquettes", "unites_semantiques")

CAS = [
    ("fr", "Le chat de la voisine qui dort sur le toit se réveille.", "fr"),
    ("en", "The cat that sleeps on the roof is black.", "en"),
    ("vide", "",
… [5453 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 python3 tools/drave.py evaluer --json > /tmp/reaudit_evaluer.json; echo rc=$?; python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/reaudit_evaluer.json'))\nm=d['heuristique']\nprint('POS',m['pos']['exactitude'],'ferme' … [453 caractères tronqués]`

  ```
rc=0
POS 0.8625 ferme 0.9373 ouvert 0.7918
F1 0.7533 tete 0.864
att {"cibles": 239, "labels": 237, "top1": 236, "topk": 235, "exact": 236, "top1_taux": 0.9874, "topk_taux": 0.9833, "exact_taux": 0.9874, "exact_any": 236, "exact_any_taux_span": 0.9958, "top1_taux_span": 0.9958, "topk_taux_span": 0.9916, "topk_exact": 235, "topk_exact_taux": 0.9833, "topk_exact_taux_span": 0.9916, "exact_taux_span": 0.9958, "verbe": {"cibles": 158, "justes": 158, "taux": 1.0}, "nom": {"cibles": 79, "justes": 78, "taux": 0.9873}, "couverture": 0.9916, "par_langue": {"fr": {"cibles": 151, "labels": 151, "exact": 150, "topk": 149, "exact_taux_span": 0.9934}, "en": {"cibles": 88, "labels": 86, "exact": 86, "topk": 86, "exact_taux_span": 1.0}}}
lineaire F1 0.8104 cov 0.9331
prag {"acte": 0.9967, "negation": 0.9771, "modalite": 0.9886, "double_sens": 0.9444}
gold {'nom': 'vivant (hand + reel + synthétique)', 'gele': False, 'phrases': 612, 'tokens': 3179, 'cibles_attachement': 239}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"import fastjsonschema; print('fastjsonschema',fastjsonschema.__version__)\" 2>&1; python3 -c \"import jsonschema; print('jsonschema',jsonschema.__version__)\" 2>&1 | head -2; python3 tools/verifier_schema_produit.py; ech … [87 caractères tronqués]`

  ```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import fastjsonschema; print('fastjsonschema',fastjsonschema.__version__)
                                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'fastjsonschema' has no attribute '__version__'
<string>:1: DeprecationWarning: Accessing jsonschema.__version__ is deprecated and will be removed in a future release. Use importlib.metadata directly to query for jsonschema's version.
jsonschema 4.26.0
  ✅ fr
  ✅ en
  ✅ vide
  ✅ ponctuation
  ✅ long
  ✅ validateur JSON Schema · 5 cas
verifier rc=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/reaudit_evaluer.json'))\nprint(json.dumps(d['heuristique']['syntagme'],ensure_ascii=False,indent=1))\nEOF\ngit show HEAD:tools/bloc_linguistique.py | sha256sum; sha256sum tools/b … [181 caractères tronqués]`

  ```
{
 "precision": 0.7239,
 "rappel": 0.7853,
 "f1": 0.7533,
 "tp": 1463,
 "fp": 558,
 "fn": 400,
 "tete": {
  "precision": 0.8519,
  "rappel": 0.8765,
  "f1": 0.864,
  "tp": 1633,
  "fp": 284,
  "fn": 230
 }
}
858197f736d758be2ca97e1ccd71a5045fd47d19d31c50afaf13fd669893b47f  -
858197f736d758be2ca97e1ccd71a5045fd47d19d31c50afaf13fd669893b47f  tools/bloc_linguistique.py
88ce03da9d9e11e48bc352083aaa94dd492b80798ef31268a1219689a78d463c  -
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n '\"document\"' tools/bloc_linguistique.py | head -10 && sed -n '/# 7\\. document/,/return Annotation/p' tools/bloc_linguistique.py | head -60 && grep -n \"60\" tools/bloc_linguistique.py | grep -i \"titre\\|document\\|trunc\\ … [74 caractères tronqués]`

  ```
51:           "pragmatique", "document")
1624:            etiquettes.append(Etiquette("document", "titre" if titre else "paragraphe",
2356:             "discours": "type", "document": "type"}
2399:    "pragmatique": "heuristique", "discours": "heuristique", "document": "heuristique",
1625:                                        p.strip()[:60], d, f, self.nom, 0.7,
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport subprocess,sys,json,time\ntexts=[\"\", \"   \", \"...\", \"🚀\", \"a\", \"-3 degrés\"]\nfor t in texts:\n    p=subprocess.run([sys.executable,'tools/drave.py','analyser','--json','--',t],capture_output=True,t … [192 caractères tronqués]`

  ```
'' rc 3 out 330 err  json? {
'   ' rc 3 out 333 err  json? {
'...' rc 3 out 333 err  json? {
'🚀' rc 3 out 331 err  json? {
'a' rc 0 out 2686 err  json? {
'-3 degrés' rc 0 out 4086 err  json? {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1580,1675p tools/bloc_linguistique.py", "description": "Lire la génération des documents et titres"}`

  ```
prec = None
            for s in simples:
                if (s["type"], s["debut"], s["fin"]) in deja:
                    prec = s
                    continue
                meta = {"role": s["role"], "niveau": s["niveau"], "union": True}
                cible = (self._cible_precedent(texte, s, prec, verbes)
                         or self._repli_cible_gp(texte, s, [x for x in simples if x["type"] == "GN"])
                         or self._cible_proche(texte, s, gvs_u, verbes, cache_gv))
                cible = self._cible_hors_span(texte, s, gvs_u, cible)
                cible = self._repli_verbe_propre(texte, s, cible)
                if cible:
                    meta["attachement"] = {"segment": s["texte"], "cible": cible}
                etiquettes.append(Etiquette("syntagme", s["type"], s["texte"], s["debut"],
                                            s["fin"], self.nom, 0.30,
                                            candidats=([s["type"]]
                                                       + self._candidats_precedent(texte, s, prec)
                                                       + self._verbes_proches(
                                                   
… [4019 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'Etiquette(\"phrase\"\\|Etiquette(\"pragmatique\"' tools/bloc_linguistique.py | head -20 && sed -n 1440,1490p tools/bloc_linguistique.py", "description": "Lire l'émission des phrases et actes"}`

  ```
1461:            etiquettes.append(Etiquette("phrase", "type", typ, d, f, self.nom, 0.85,
1464:                etiquettes.append(Etiquette("phrase", "négation", "oui", d, f, self.nom, 0.65,
1467:                etiquettes.append(Etiquette("phrase", "modalité", "oui", d, f, self.nom, 0.55,
1473:            etiquettes.append(Etiquette("pragmatique", "acte", acte, d, f, self.nom, 0.45,
1478:                etiquettes.append(Etiquette("pragmatique", "double_sens", "candidat", d, f,
1628:            etiquettes.append(Etiquette("pragmatique", "contexte", contexte[:200], 0, len(texte),
1700:            etiquettes.append(Etiquette("phrase", "type", typ, d, f, self.nom, 0.9,
1704:            etiquettes.append(Etiquette("pragmatique", "acte", acte, d, f, self.nom, 0.8,
2186:            etiquettes = [Etiquette("pragmatique", "acte", acte, 0, n, self.nom,
2189:                etiquettes.append(Etiquette("phrase", "négation", "", 0, n, self.nom,
2192:                etiquettes.append(Etiquette("phrase", "modalité", "", 0, n, self.nom,
2195:                etiquettes.append(Etiquette("pragmatique", "double_sens", "", 0, n, self.nom,
                if (_normaliser(_av.valeur) in _cop_fr
        
… [3428 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,120p tools/porte-produit.sh", "description": "Lire la porte produit pour les contrôles existants"}`

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
… [2116 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,240p tools/tests/test_produit_libre.py", "description": "Lire le test des 50 textes libres"}`

  ```
#!/usr/bin/env python3
"""test_produit_libre.py — non-régression sur les **50 textes libres** de l'audit A26.

Ce que le test fige :
- la vue **`filtrer`** ne produit **aucun** chevauchement de syntagmes (0/50) ;
- la vue **`alternative`** (défaut) documente les chevauchements dans `meta.alternative` ;
- les **5 textes non linguistiques** (emoji, vide, espaces, ponctuation, nombre nu) n'ont
  **aucun** syntagme ;
- l'analyse est **déterministe** (deux passes identiques).
"""
from __future__ import annotations

import json
import pathlib
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))

BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
NON_LINGUISTIQUES = {"f14", "f15", "f16", "f17", "f18"}


def _textes() -> list[tuple[str, str]]:
    donnees = json.loads(BANC.read_text(encoding="utf-8"))
    return [(item["id"], item["texte"]) for item in donnees["banc_50"]["resultats"]]


def _segments(annotation) -> list:
    return [e for e in annotation.etiquettes if e.niveau == "syntagme"]


def _chevauchements(segments: list) -> int:
    return sum(1 for i, a in enumerate(segments) for b in segments[i + 1:]
           
… [1439 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def _expliciter_partition\" tools/bloc_linguistique.py && sed -n '/def _expliciter_partition/,/^def /p' tools/bloc_linguistique.py | head -80", "description": "Lire la partition étiquetée"}`

  ```
2262:def _expliciter_partition(etiquettes: list[Etiquette], filtrer: str = "") -> None:
def _expliciter_partition(etiquettes: list[Etiquette], filtrer: str = "") -> None:
    """Documente (et, si `filtrer`, linéarise) les chevauchements de syntagmes.

    `meta.partition` porte le groupe, le rang et la vue ; `meta.alternative` porte les
    autres segments du groupe, leur relation vue du porteur et, en mode `filtrer`, le
    drapeau `retire`. Aucun segment n'est supprimé en mode `alternative`.

    `filtrer="union"` : on retire le S qui **contient** un segment chunker (le filtre
    union du P0-3) ; les autres chevauchements restent documentés. `filtrer="strict"` :
    le chunker est la partition — **tous** les segments `union` sont conservés, et tous
    les S qui les chevauchent sont retirés. Dans les deux cas, le retiré reste lisible
    dans `meta.alternative` du segment conservé, avec `retire: true`.
    """
    segs = [e for e in etiquettes if e.niveau == "syntagme"]
    groupes = _groupes_partition(segs)
    rangs: dict[int, tuple[int, int]] = {}
    for gid, groupe in enumerate(groupes):
        for i, e in enumerate(sorted(groupe, key=_cle_preferee)):
            rangs[id(
… [3019 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Construction du harnais de rejeu dans /tmp (lecture seule du dépôt)

- **write** `{"file_path": "/tmp/reaudit/explorer.py", "content": "#!/usr/bin/env python3\n\"\"\"Exploration rapide des 50 textes via l'API (pas la CLI).\"\"\"\nimport json, sys, time, collections\n\nRACINE = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, RACINE)\nsys.path.insert(0, RACI … [2353 caractères tronqués]`

  ```
<path>/tmp/reaudit/explorer.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/reaudit/explorer.py 2>&1 | head -110", "description": "Explorer les métriques des 50 textes"}`

  ```
== alternative
textes avec chevauchement 26 / 50
  alt: 226
  cibles: 321
  documents: 49
  labels: 4833
  non_surface: 245
  paires: 149
  phrases: 67
  sans_cible: 87
  syntagmes: 408
  tokens_mot: 766
  tokens_nombre: 45
  tokens_ponctuation: 257
  union: 129
  unites: 407
== filtrer
textes avec chevauchement 0 / 50
  alt: 128
  cibles: 236
  documents: 49
  labels: 4735
  non_surface: 245
  paires: 0
  phrases: 67
  sans_cible: 74
  syntagmes: 310
  tokens_mot: 766
  tokens_nombre: 45
  tokens_ponctuation: 257
  union: 129
  unites: 407

Détail alternative:
f02 2 [('GN', 0, 7, 'Le chat'), ('GP', 8, 21, 'de la voisine'), ('REL', 22, 42, 'qui dort sur le toit'), ('REL', 22, 54, 'qui dort sur le toit se réveil'), ('GV', 43, 54, 'se réveille')]
f03 3 [('GV', 0, 7, 'Bonjour'), ('GN', 10, 17, 'Comment'), ('GV', 10, 28, 'Comment allez-vous'), ('GV', 18, 40, "allez-vous aujourd'hui"), ('GP', 29, 40, "aujourd'hui")]
f05 1 [('GV', 0, 13, 'Ne touche pas'), ('GP', 14, 18, 'à ça'), ('GN', 16, 18, 'ça')]
f06 6 [('GN', 0, 2, 'Je'), ('GV', 0, 15, 'Je ne pense pas'), ('GV', 3, 15, 'ne pense pas'), ('SUB', 16, 29, "qu'il viendra"), ('SUB', 16, 36, "qu'il viendra demain"), ('GP', 30, 36, 'demain'
… [4828 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys,re\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nfor t in [\"Visitez https://example.com/docs?page=2 pour la documentation.\",\"Email: alice@example.org, phone: +33 6 12 34 56 78.\",\"Un f … [328 caractères tronqués]`

  ```
'Visitez https://example.com/docs?page=2 pour la documentation.'
 mots: [(0, 7, 'Visitez', 'mot'), (8, 13, 'https', 'mot'), (13, 14, ':', 'ponctuation'), (14, 15, '/', 'ponctuation'), (15, 16, '/', 'ponctuation'), (16, 23, 'example', 'mot'), (23, 24, '.', 'ponctuation'), (24, 27, 'com', 'mot'), (27, 28, '/', 'ponctuation'), (28, 32, 'docs', 'mot'), (32, 33, '?', 'ponctuation'), (33, 37, 'page', 'mot'), (37, 38, '=', 'ponctuation'), (38, 39, '2', 'nombre'), (40, 44, 'pour', 'mot'), (45, 47, 'la', 'mot'), (48, 61, 'documentation', 'mot'), (61, 62, '.', 'ponctuation')]
 zones: [(8, 39, "'https://example.com/docs?page=2'")]
'Email: alice@example.org, phone: +33 6 12 34 56 78.'
 mots: [(0, 5, 'Email', 'mot'), (5, 6, ':', 'ponctuation'), (7, 12, 'alice', 'mot'), (12, 13, '@', 'ponctuation'), (13, 20, 'example', 'mot'), (20, 21, '.', 'ponctuation'), (21, 24, 'org', 'mot'), (24, 25, ',', 'ponctuation'), (26, 31, 'phone', 'mot'), (31, 32, ':', 'ponctuation'), (33, 34, '+', 'ponctuation'), (34, 36, '33', 'nombre'), (37, 38, '6', 'nombre'), (39, 41, '12', 'nombre'), (42, 44, '34', 'nombre'), (45, 47, '56', 'nombre'), (48, 50, '78', 'nombre'), (50, 51, '.', 'ponctuation')]
 zones: [(7, 24, "'a
… [726 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys,collections\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nbanc=json.load(open('reports/pensee-fiabilite-produit.json'))['banc_50']['resultats']\nh=bl.Heuristique()\ntot=collections.Co … [593 caractères tronqués]`

  ```
POS total 1068 POS dans zone protégée 95 textes 6
('f11', 5, [('12', 'NUM', 15, 17), ('/', 'PONCT', 17, 18), ('03', 'NUM', 18, 20), ('/', 'PONCT', 20, 21), ('2026', 'NUM', 21, 25)])
('f12', 13, [('https', 'VERB', 8, 13), (':', 'PONCT', 13, 14), ('/', 'PONCT', 14, 15), ('/', 'PONCT', 15, 16), ('example', 'NOUN', 16, 23), ('.', 'PONCT', 23, 24), ('com', 'NOUN', 24, 27), ('/', 'PONCT', 27, 28), ('docs', 'NOUN', 28, 32), ('?', 'PONCT', 32, 33), ('page', 'NOUN', 33, 37), ('=', 'PONCT', 37, 38), ('2', 'NUM', 38, 39)])
('f37', 5, [('alice', 'NOUN', 7, 12), ('@', 'PONCT', 12, 13), ('example', 'NOUN', 13, 20), ('.', 'PONCT', 20, 21), ('org', 'NOUN', 21, 24)])
('f38', 22, [('https', 'NOUN', 14, 19), (':', 'PONCT', 19, 20), ('/', 'PONCT', 20, 21), ('/', 'PONCT', 21, 22), ('a', 'PREP', 22, 23), ('.', 'PONCT', 23, 24), ('b', 'NOUN', 24, 25), ('/', 'PONCT', 25, 26), ('c', 'DET', 26, 27), ('?', 'PONCT', 27, 28), ('d', 'PREP', 28, 29), ('=', 'PONCT', 29, 30), ('e', 'NOUN', 30, 31), ('#', 'PONCT', 31, 32), ('f', 'NOUN', 32, 33), ('http', 'NOUN', 37, 41), (':', 'PONCT', 41, 42), ('/', 'PONCT', 42, 43), ('/', 'PONCT', 43, 44), ('x', 'NOUN', 44, 45), ('.', 'PONCT', 45, 46), ('y', 'PRON', 46, 47)])
('f
… [1407 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nfor r in d['banc_50']['resultats']:\n    if r['id'] in ('f01','f12','f13','f18','f37','f38','f39','f50'):\n        print(r['id'], {k:r.get(k) … [232 caractères tronqués]`

  ```
f01 {'mots': 4, 'pos': 3, 'syntagmes': 2, 'labels': 19, 'trous_pos': {'mot': {'total': 3, 'sans_pos': 0}, 'ponctuation': {'total': 1, 'sans_pos': 1}}, 'chevauchements_syntagme': 0, 'syntagmes_union': 0, 'phrases': 1, 'documents': 1, 'doc_tronquees': 0, 'doc_titres': [], 'langue': 'fr', 'rc': 0}
f12 {'mots': 18, 'pos': 9, 'syntagmes': 5, 'labels': 63, 'trous_pos': {'mot': {'total': 9, 'sans_pos': 0}, 'ponctuation': {'total': 8, 'sans_pos': 8}, 'nombre': {'total': 1, 'sans_pos': 1}}, 'chevauchements_syntagme': 0, 'syntagmes_union': 0, 'phrases': 3, 'documents': 1, 'doc_tronquees': 1, 'doc_titres': [], 'langue': 'fr', 'rc': 0}
f13 {'mots': 6, 'pos': 4, 'syntagmes': 0, 'labels': 26, 'trous_pos': {'mot': {'total': 4, 'sans_pos': 0}, 'ponctuation': {'total': 2, 'sans_pos': 2}}, 'chevauchements_syntagme': 0, 'syntagmes_union': 0, 'phrases': 1, 'documents': 1, 'doc_tronquees': 0, 'doc_titres': [], 'langue': 'und', 'rc': 0}
f18 {'mots': 1, 'pos': 0, 'syntagmes': 0, 'labels': 6, 'trous_pos': {'nombre': {'total': 1, 'sans_pos': 1}}, 'chevauchements_syntagme': 0, 'syntagmes_union': 0, 'phrases': 1, 'documents': 1, 'doc_tronquees': 0, 'doc_titres': ['1234567890'], 'langue': 'und', 'rc': 0}
f37 
… [1545 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys,collections\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nbanc=json.load(open('reports/pensee-fiabilite-produit.json'))['banc_50']['resultats']\nh=bl.Heuristique()\nfor r in banc:\n   … [691 caractères tronqués]`

  ```
f01 rc-API  lang fr phr [(0, 13, 'déclarative')] synt 2 holes 0 espaces 0
f02 rc-API  lang fr phr [(0, 55, 'déclarative')] synt 5 holes 0 espaces 0
f03 rc-API  lang fr phr [(0, 9, 'exclamative'), (10, 42, 'interrogative')] synt 5 holes 0 espaces 0
f04 rc-API  lang fr phr [(0, 30, 'déclarative')] synt 3 holes 0 espaces 0
f05 rc-API  lang fr phr [(0, 20, 'exclamative')] synt 3 holes 0 espaces 0
f06 rc-API  lang fr phr [(0, 61, 'déclarative')] synt 9 holes 0 espaces 0
f07 rc-API  lang en phr [(0, 27, 'déclarative')] synt 3 holes 0 espaces 0
f08 rc-API  lang en phr [(0, 43, 'interrogative')] synt 1 holes 0 espaces 0
f09 rc-API  lang en phr [(0, 36, 'déclarative')] synt 1 holes 0 espaces 0
f10 rc-API  lang fr phr [(0, 42, 'déclarative')] synt 5 holes 0 espaces 0
f11 rc-API  lang fr phr [(0, 34, 'déclarative')] synt 4 holes 0 espaces 0
f12 rc-API  lang fr phr [(0, 62, 'déclarative')] synt 7 holes 0 espaces 0
f13 rc-API  lang und phr [(0, 24, 'déclarative')] synt 2 holes 0 espaces 0
f14 rc-API refus=vide lang und phr [] synt 0 holes 0 espaces 0
f15 rc-API refus=vide lang und phr [] synt 0 holes 0 espaces 0
f16 rc-API refus=vide lang und phr [] synt 0 holes 0 espaces 0
f17 rc-API refus=vid
… [3063 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for l in \"\" \"--langue fr\"; do echo \"== $l\"; python3 tools/drave.py analyser \"Élodie sourit.\" $l --json | python3 -c \"import json,sys; d=json.load(sys.stdin); print('langue',d['langue'],'synt',[(e['type'],e['valeur']) for e i … [119 caractères tronqués]`

  ```
== 
langue und synt []
== --langue fr
langue und synt [('GV', 'Élodie sourit')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py analyser \"J'ai trouvé ça génial 😍🔥\" --json | python3 -c \"import json,sys; d=json.load(sys.stdin); print([(e['niveau'],e['type'],e['valeur']) for e in d['etiquettes'] if e['niveau'] in ('pos','syntagme')])\"" … [58 caractères tronqués]`

  ```
[('pos', 'PRON', "J'ai"), ('syntagme', 'GN', "J'ai"), ('pos', 'NOUN', 'trouvé'), ('syntagme', 'GV', 'trouvé ça génial'), ('pos', 'PRON', 'ça'), ('pos', 'ADJ', 'génial'), ('pos', 'PONCT', '😍'), ('pos', 'PONCT', '🔥')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nprint(type(bl.POS_FERME), list(bl.POS_FERME)[:5])\nprint({k:type(v).__name__ for k,v in bl.POS_FERME['fr'].items()})\nprint('exemples', {k:lis … [233 caractères tronqués]`

  ```
<class 'dict'> ['fr', 'en']
{'DET': 'set', 'PREP': 'set', 'PRON': 'set', 'CONJ': 'set', 'AUX': 'set', 'ADV': 'set', 'NUM': 'set'}
exemples {'DET': ['ses', 'quelles', 'ton', 'quel', 'cette'], 'PREP': ['dans', 'au-dessous', 'par', 'aux', 'd'], 'PRON': ['dont', 'quoi', 'elle', 'que', 'il']}
VERBES_IMPERATIFS ['find', 'open', 'dis', 'trouve', 'va', 'look', 'fais', 'cherche', 'ouvre', 'go', 'give', 'écoute', 'ferme', 'viens', 'regarde', 'take', 'close', 'come', 'donne', 'prends']
MOTS_DOUBLE_SENS ['point', 'mousse', 'note', 'voler', 'duck', 'canard', 'avocat', 'temps', 'manche', 'glace']
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Fonctions communes du re-audit produit (lecture seule du depot).\n\nTout est mesure depuis /tmp : le harnais n'ecrit aucun fichier dans le depot.\n\"\"\"\nfrom __future__ import annotations\n\nimport collections\nimport hashlib\nimport json\nimport pathlib\ … [16937 caractères tronqués]`

  ```
<path>/tmp/reaudit/commun.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Rejeu des 50 textes du banc fiabilite-produit par la CLI actuelle.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport pathlib\nimport statistics\nimport sys\nimport time\n\nsys.path.insert(0, \"/tmp/reaudit\")\nimport commun as C\n\nSORTIE = p … [5586 caractères tronqués]`

  ```
<path>/tmp/reaudit/run50.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/reaudit/run50.py 5 2>&1 | tail -20", "description": "Tester le harnais sur 5 textes"}`

  ```
1/5 f01 rc=0 labels=20 t=149ms chev=0 filtrer=0 api=2.56ms
 2/5 f02 rc=0 labels=60 t=163ms chev=2 filtrer=0 api=1.35ms
 3/5 f03 rc=0 labels=41 t=151ms chev=3 filtrer=0 api=1.76ms
 4/5 f04 rc=0 labels=40 t=147ms chev=0 filtrer=0 api=2.16ms
 5/5 f05 rc=0 labels=31 t=154ms chev=1 filtrer=0 api=2.54ms
écrit /tmp/reaudit/banc50.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/reaudit/banc50.json'))\nfor r in d[:2]:\n    m=r['metriques']\n    print(r['id'],'schema',r['schema_valide'],r['contrat'])\n    print(' trous',m['trous_pos'],'pos_zone',m['pos_zo … [391 caractères tronqués]`

  ```
f01 schema True {'manquants': [], 'erreurs': [], 'schema': '', 'ok': True}
 trous {'mot': {'total': 3, 'sans_pos': 0}, 'ponctuation': {'total': 1, 'sans_pos': 0}} pos_zone {} url 0 emoji 0
 phrases [{'debut': 0, 'fin': 13, 'valeur': 'déclarative'}] unites 2 True True
 vues {'alternative': (0, 2, 0), 'brut': (0, 2, 0), 'filtrer_union': (0, 2, 0), 'filtrer': (0, 2, 0)}
 readable {'rc': 0, 'stdout_octets': 593, 'stderr': '', 'temps_ms': 144.89, 'traceback': False}
f02 schema True {'manquants': [], 'erreurs': [], 'schema': '', 'ok': True}
 trous {'mot': {'total': 12, 'sans_pos': 0}, 'ponctuation': {'total': 1, 'sans_pos': 0}} pos_zone {} url 0 emoji 0
 phrases [{'debut': 0, 'fin': 55, 'valeur': 'déclarative'}] unites 5 True True
 vues {'alternative': (0, 5, 2), 'brut': (0, 5, 2), 'filtrer_union': (0, 5, 2), 'filtrer': (0, 3, 0)}
 readable {'rc': 0, 'stdout_octets': 1013, 'stderr': '', 'temps_ms': 148.82, 'traceback': False}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 /tmp/reaudit/run50.py 2>&1 | tail -55", "description": "Rejouer les 50 textes par la CLI", "timeoutMs": 900000}`

  ```
1/50 f01 rc=0 labels=20 t=151ms chev=0 filtrer=0 api=1.58ms
 2/50 f02 rc=0 labels=60 t=163ms chev=2 filtrer=0 api=3.48ms
 3/50 f03 rc=0 labels=41 t=158ms chev=3 filtrer=0 api=3.56ms
 4/50 f04 rc=0 labels=40 t=157ms chev=0 filtrer=0 api=1.11ms
 5/50 f05 rc=0 labels=31 t=162ms chev=1 filtrer=0 api=1.28ms
 6/50 f06 rc=0 labels=67 t=158ms chev=6 filtrer=0 api=2.55ms
 7/50 f07 rc=0 labels=33 t=147ms chev=0 filtrer=0 api=1.61ms
 8/50 f08 rc=0 labels=39 t=166ms chev=0 filtrer=0 api=0.91ms
 9/50 f09 rc=0 labels=34 t=150ms chev=0 filtrer=0 api=0.81ms
10/50 f10 rc=0 labels=58 t=170ms chev=1 filtrer=0 api=4.62ms
11/50 f11 rc=0 labels=48 t=157ms chev=1 filtrer=0 api=1.65ms
12/50 f12 rc=0 labels=70 t=159ms chev=2 filtrer=0 api=2.38ms
13/50 f13 rc=0 labels=30 t=148ms chev=0 filtrer=0 api=1.07ms
14/50 f14 rc=3 labels=0 t=169ms chev=0 filtrer=0 api=0.03ms
15/50 f15 rc=3 labels=0 t=149ms chev=0 filtrer=0 api=0.01ms
16/50 f16 rc=3 labels=0 t=153ms chev=0 filtrer=0 api=0.02ms
17/50 f17 rc=3 labels=0 t=166ms chev=0 filtrer=0 api=0.02ms
18/50 f18 rc=0 labels=7 t=144ms chev=0 filtrer=0 api=0.42ms
19/50 f19 rc=0 labels=46 t=161ms chev=0 filtrer=0 api=2.17ms
20/50 f20 rc=0 labels=72 t=171ms chev=3 filtrer
… [1935 caractères tronqués]
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Rejeu des 40 textes du banc frontieres-phrase par la CLI actuelle.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport pathlib\nimport re\nimport statistics\nimport sys\nimport time\n\nsys.path.insert(0, \"/tmp/reaudit\")\nimport commun as C\n\ … [7074 caractères tronqués]`

  ```
<path>/tmp/reaudit/run40.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/reaudit && python3 - <<'EOF'\nimport re, pathlib\np=pathlib.Path('run40.py')\ns=p.read_text()\ns=s.replace('def evaluer(texte: str, pred: list[dict], attendu: list[dict], acts: dict) -> dict:',\n            'def evaluer(texte: str, pred: list[dict], attendu: list[dict], acts: di … [598 caractères tronqués]`

  ```
ok
 1/40 n01  phr= 2/ 2 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=2
 2/40 n02  phr= 3/ 3 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=3
 3/40 d01  phr= 1/ 1 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=1
 4/40 d02  phr= 1/ 1 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=1
 5/40 d03  phr= 1/ 1 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=1
 6/40 d04  phr= 1/ 1 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=1
 7/40 u01  phr= 1/ 1 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=1
 8/40 u02  phr= 2/ 2 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=2
 9/40 e01  phr= 1/ 1 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=1
10/40 e02  phr= 1/ 1 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=1
11/40 c01  phr= 1/ 1 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=1
12/40 c02  phr= 1/ 1 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=1
13/40 c03  phr= 1/ 1 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=1
14/40 c04  phr= 1/ 1 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=1
15/40 a01  phr= 1/ 1 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=1
16/40 a02  p
… [1999 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/reaudit && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('run40.py'); s=p.read_text()\ns=s.replace('cands[(e[\"debut\"], e[\"fin\"], \"candidats\")] = e.get(\"candidats\") or []',\n            'cands[(e[\"debut\"], e[\"fin\"])] = e.get(\"candidats\") or []')\np.write_text(s) … [200 caractères tronqués]`

  ```
ok
                     ~~~~^^
  File "/tmp/reaudit/run40.py", line 119, in main
    ev = evaluer(texte, pred, attendu, acts, cands) if d is not None else {
         ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/reaudit/run40.py", line 74, in evaluer
    cands = set((cands or {}).get((cle[0], cle[1]), []))
                ^^^^^^^^^^^^^^^^^
AttributeError: 'set' object has no attribute 'get'
  ```

- **bash** `{"command": "cd /tmp/reaudit && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('run40.py'); s=p.read_text()\ns=s.replace('        cands = set((cands or {}).get((cle[0], cle[1]), []))\\n        if act not in cands:\\n            actes_candidats_ko.append({\"debut\": a[\"debut\"], \"acte\": act, \" … [469 caractères tronqués]`

  ```
ok
34/40 en01 phr= 2/ 2 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=0
35/40 en02 phr= 1/ 1 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=0
36/40 en03 phr= 2/ 2 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=0
37/40 u03  phr= 1/ 1 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=0
38/40 s03  phr= 2/ 2 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=0
39/40 d05  phr= 2/ 2 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=0
40/40 u04  phr= 2/ 2 exact=True ff=False extra=0 miss=0 actes_faux=0 cand_ko=0
écrit /tmp/reaudit/frontieres40.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, collections\nd=json.load(open('/tmp/reaudit/frontieres40.json'))\nagg=collections.Counter()\nfor r in d:\n    for k in ('phrases','exact','frontiere_fausse','casse','actes_presents','actes_faux','actes … [814 caractères tronqués]`

  ```
{'phrases': 59, 'exact': 40, 'frontiere_fausse': 0, 'casse': 0, 'actes_presents': 59, 'actes_faux': 0, 'actes_faux_type': 0, 'actes_candidats_ko': 0, 'extra': 0, 'missing': 0, 'overlaps': 0, 'leading': 0, 'vides': 0, 'fausses_questions': 0, 'types_faux': 0}
temps 145.67 171.46
json bytes 7929 27781
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, unicodedata, json\nsys.path.insert(0,'tools'); import bloc_linguistique as bl\ncas = {\n 'ar': 'القطة تنام على السطح. هل ترى القمر؟',\n 'zh': '猫在屋顶上睡觉。你看见月亮了吗？',\n 'ru': 'Кошка спит на крыше. Ты видишь  … [549 caractères tronqués]`

  ```
ar phr [(0, 21, "'القطة تنام على السطح.'", 'القطة تنام على السطح.'), (22, 35, "'هل ترى القمر؟'", 'هل ترى القمر؟')]
  zones []
zh phr [(0, 16, "'猫在屋顶上睡觉。你看见月亮了吗？'", '猫在屋顶上睡觉。你看见月亮了吗？')]
  zones []
ru phr [(0, 20, "'Кошка спит на крыше.'", 'Кошка спит на крыше.'), (21, 36, "'Ты видишь луну?'", 'Ты видишь луну?')]
  zones []
he phr [(0, 17, "'החתול ישן על הגג.'", 'החתול ישן על הגג.'), (18, 35, "'אתה רואה את הירח?'", 'אתה רואה את הירח?')]
  zones []
json phr [(0, 18, '\'{"schema": "drave.\'', '{"schema": "drave.'), (18, 94, '\'annotation", "version": 1, "url": "https://example.com/a?b=2", "prix": 12.5}\'', 'annotation", "version": 1, "url": "https://example.com/a?b=2", "prix": 12.5}')]
  zones [(53, 78, "'https://example.com/a?b=2'")]
url phr [(0, 89, "'Voir https://example.com/docs?page=2&lang=fr#section-3, puis https://a.b/c?d=e%20f&g=h+i.'", 'Voir https://example.com/docs?page=2&lang=fr#section-3, puis https://a.b/c?d=e%20f&g=h+i.')]
  zones [(5, 54, "'https://example.com/docs?page=2&lang=fr#section-3'"), (61, 88, "'https://a.b/c?d=e%20f&g=h+i'")]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport subprocess,sys,json\nfor t in ['', '...', '🚀', 'Il part. Elle reste.']:\n    p=subprocess.run([sys.executable,'tools/drave.py','analyser','--jsonl','--',t],capture_output=True,text=True,cwd='.')\n    print(r … [295 caractères tronqués]`

  ```
'' rc 3 lines 0 err drave: refus d'analyse : vide
'...' rc 0 lines 1 err 
    '...' refus 'vide' schema drave.annotation
'🚀' rc 0 lines 1 err 
    '🚀' refus 'vide' schema drave.annotation
'Il part. Elle reste.' rc 0 lines 2 err 
    'Il part.' refus '' schema drave.annotation
    'Elle reste.' refus '' schema drave.annotation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, unicodedata, json\nsys.path.insert(0,'tools'); import bloc_linguistique as bl\nfor s in [\"Élodie sourit. Le café est prêt.\", \"Visitez https://exemple.fr/café?x=1 à Paris.\"]:\n    t=unicodedata.norma … [550 caractères tronqués]`

  ```
NFC? False NFD? True
lang fr phr [(0, 15, "'Élodie sourit.'", 'Élodie sourit.'), (16, 35, "'Le café est prêt.'", 'Le café est prêt.')]
tokens [(0, 1, "'E'", 'mot'), (1, 2, "'́'", 'ponctuation'), (2, 7, "'lodie'", 'mot'), (8, 14, "'sourit'", 'mot'), (14, 15, "'.'", 'ponctuation'), (16, 18, "'Le'", 'mot'), (19, 23, "'cafe'", 'mot'), (23, 24, "'́'", 'ponctuation'), (25, 28, "'est'", 'mot'), (29, 32, "'pre'", 'mot'), (32, 33, "'̂'", 'ponctuation'), (33, 34, "'t'", 'mot'), (34, 35, "'.'", 'ponctuation')]
pos [('E', 'NOUN', 0, 1), ('́', 'PONCT', 1, 2), ('lodie', 'NOUN', 2, 7), ('sourit', 'NOUN', 8, 14), ('.', 'PONCT', 14, 15), ('Le', 'DET', 16, 18), ('cafe', 'NOUN', 19, 23), ('́', 'PONCT', 23, 24), ('est', 'AUX', 25, 28), ('pre', 'NOUN', 29, 32), ('̂', 'PONCT', 32, 33), ('t', 'PRON', 33, 34), ('.', 'PONCT', 34, 35)]
zones []
NFC? False NFD? True
lang fr phr [(0, 46, "'Visitez https://exemple.fr/café?x=1 à Paris.'", 'Visitez https://exemple.fr/café?x=1 à Paris.')]
tokens [(0, 7, "'Visitez'", 'mot'), (8, 13, "'https'", 'mot'), (13, 14, "':'", 'ponctuation'), (14, 15, "'/'", 'ponctuation'), (15, 16, "'/'", 'ponctuation'), (16, 23, "'exemple'", 'mot'), (23, 24, "'.'", 'ponctuation'
… [871 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport subprocess,sys,tempfile,pathlib,json\nfor contenu in [b'a\\xffb', b'\\xef\\xbb\\xbfLe chat dort.', b'Il part.\\r\\nElle reste.\\r\\n']:\n    p=pathlib.Path('/tmp/reaudit/probe.txt'); p.write_bytes(contenu)\n … [484 caractères tronqués]`

  ```
b'a\xffb' rc 0 err 
  texte 'a�b' len 3 phr [(0, 3)]
b'\xef\xbb\xbfLe chat dort.' rc 0 err 
  texte '\ufeffLe chat dort.' len 14 phr [(0, 14)]
b'Il part.\r\nElle reste.\r\n' rc 0 err 
  texte 'Il part.\nElle reste.\n' len 21 phr [(0, 8), (9, 20)]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys,json\nsys.path.insert(0,'tools'); import bloc_linguistique as bl\ncas={\n'html1':'<p>Le chat <strong>dort</strong> sur le toit.</p>',\n'html2':'<html><head><style>body { color: red; }</style></head><body … [1464 caractères tronqués]`

  ```
html1 lang fr script Latn phr [(0, 45, "'<p>Le chat <strong>dort</strong> sur le toit.'", '<p>Le chat <strong>dort</strong> sur le toit.'), (45, 49, "'</p>'", '</p>')] synt 7
  labels 81 refus  zones []
html2 lang fr script Latn phr [(0, 146, '\'<html><head><style>body { color: red; }</style></head><body><h1>Titre</h1><p>Un texte &amp; une <a href="https://example.com?a=1&amp;b=2">URL</a>.\'', '<html><head><style>body { color: red; }</style></head><body><h1>Titre</h1><p>Un texte &amp; une <a href="https://example.com?a=1&amp;b=2">URL</a>.'), (146, 164, "'</p></body></html>'", '</p></body></html>')] synt 15
  labels 281 refus  zones [(105, 136, "'https://example.com?a=1&amp;b=2'")]
html3 lang fr script Latn phr [(0, 2, "'<!'", '<!'), (2, 65, '\'-- commentaire --><script>if (a < b && c > d) { console.log("x?\'', '-- commentaire --><script>if (a < b && c > d) { console.log("x?'), (65, 89, '\'y=1"); }</script><p>Fin.\'', 'y=1"); }</script><p>Fin.'), (89, 93, "'</p>'", '</p>')] synt 11
  labels 176 refus  zones [(50, 61, "'console.log'")]
md1 lang fr script Latn phr [(0, 7, "'# Notes'", '# Notes'), (9, 38, "'Le **chat** dort sur le toit.'", 'Le **chat** dort sur le toit.'), (40, 50, "'-
… [2371 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys,time,json\nsys.path.insert(0,'tools'); import bloc_linguistique as bl\nt16=(\"\\n\\n\".join([\"Le chat de la voisine qui dort sur le toit se réveille. \" * 20]*16)).strip()\nt17=\"a\"*10000\nfor k,t in [ … [481 caractères tronqués]`

  ```
x16 len 17949
  alternative ms 1228.8 labels 18911 phr 320 synt 1600
  filtrer ms 1267.0 labels 18271 phr 320 synt 960
x17 len 10000
  alternative ms 26.4 labels 7 phr 1 synt 0
  filtrer ms 16.1 labels 7 phr 1 synt 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport subprocess,sys,time,json\nt=\"a\"*10000\nt0=time.perf_counter(); p=subprocess.run([sys.executable,'tools/drave.py','analyser','--json','--',t],capture_output=True,cwd='.'); dt=time.perf_counter()-t0\nprint(' … [415 caractères tronqués]`

  ```
x17 json rc 0 ms 182.0 out 42528
x17 readable rc 0 ms 168.2 out 10457 maxligne 10010
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Les 20 nouveaux cas limites du re-audit produit (lecture seule).\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport pathlib\nimport statistics\nimport sys\nimport unicodedata\n\nsys.path.insert(0, \"/tmp/reaudit\")\nimport commun as C\n\nSORTI … [9987 caractères tronqués]`

  ```
<path>/tmp/reaudit/run20.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 /tmp/reaudit/run20.py 2>&1 | tail -25", "description": "Rejouer les 20 cas limites", "timeoutMs": 900000}`

  ```
1/20 x01 html               rc=0 phr=  2 labels=81 t=172ms json=23054 schema=True zone=0 q=False
 2/20 x02 html               rc=0 phr=  2 labels=281 t=169ms json=73464 schema=True zone=0 q=False
 3/20 x03 html               rc=0 phr=  4 labels=176 t=159ms json=45812 schema=True zone=0 q=True
 4/20 x04 markdown           rc=0 phr=  5 labels=151 t=165ms json=42458 schema=True zone=0 q=False
 5/20 x05 markdown-tableau   rc=0 phr=  4 labels=102 t=155ms json=25116 schema=True zone=0 q=False
 6/20 x06 markdown-code      rc=0 phr=  4 labels=103 t=157ms json=28504 schema=True zone=2 q=False
 7/20 x07 code-python        rc=0 phr=  2 labels=152 t=175ms json=39096 schema=True zone=0 q=False
 8/20 x08 code-json          rc=0 phr=  2 labels=141 t=152ms json=34656 schema=True zone=0 q=False
 9/20 x09 code-shell         rc=0 phr=  2 labels=99 t=156ms json=24703 schema=True zone=0 q=False
10/20 x10 tableau-tsv        rc=0 phr=  1 labels=67 t=148ms json=16844 schema=True zone=0 q=False
11/20 x11 tableau-ascii      rc=0 phr=  5 labels=173 t=159ms json=42016 schema=True zone=0 q=False
12/20 x12 arabe              rc=0 phr=  2 labels=39 t=162ms json=10477 schema=True zone=0 q=False
13/20 x13 chinois 
… [851 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/reaudit/cas20.json'))\nfor r in d:\n    if 'fichier' in r:\n        print(r['id'],'fichier', {k:r['fichier'].get(k) for k in ('rc','json_valide','texte_identique','sortie_identiq … [268 caractères tronqués]`

  ```
x03 fichier {'rc': 0, 'json_valide': True, 'texte_identique': True, 'sortie_identique_argv': True, 'octets': 93, 'labels': 176} args 45812
x04 jsonl {'rc': 0, 'lignes': 5, 'lignes_ok': 5, 'refus': 0, 'phrases_attendues': 5, 'octets': 33265}
x05 jsonl {'rc': 0, 'lignes': 4, 'lignes_ok': 4, 'refus': 1, 'phrases_attendues': 4, 'octets': 17905}
x06 jsonl {'rc': 0, 'lignes': 4, 'lignes_ok': 4, 'refus': 1, 'phrases_attendues': 4, 'octets': 22091}
x10 jsonl {'rc': 0, 'lignes': 1, 'lignes_ok': 1, 'refus': 0, 'phrases_attendues': 1, 'octets': 13791}
x11 jsonl {'rc': 0, 'lignes': 5, 'lignes_ok': 5, 'refus': 3, 'phrases_attendues': 5, 'octets': 12308}
x16 fichier {'rc': 0, 'json_valide': True, 'texte_identique': True, 'sortie_identique_argv': True, 'octets': 18269, 'labels': 18911} args 5803495
x16 jsonl {'rc': 0, 'lignes': 320, 'lignes_ok': 320, 'refus': 0, 'phrases_attendues': 320, 'octets': 4771840}
x17 fichier {'rc': 0, 'json_valide': True, 'texte_identique': True, 'sortie_identique_argv': True, 'octets': 10000, 'labels': 7} args 42528
x18 fichier {'rc': 0, 'json_valide': True, 'texte_identique': True, 'sortie_identique_argv': True, 'octets': 38, 'labels': 54} args 14954
x19 fichier {'rc'
… [222 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/reaudit/cas20.json'))\nfor r in d:\n    if r['id'] in ('x01','x02','x03','x06','x07','x08','x09','x11','x12','x13','x18','x19'):\n        print(r['id'], r['cat'])\n        for p  … [159 caractères tronqués]`

  ```
x01 html
    0 45 déclarative '<p>Le chat <strong>dort</strong> sur le toit.'
    45 49 déclarative '</p>'
x02 html
    0 146 déclarative '<html><head><style>body { color: red; }</style></head><body><h1>Titre<'
    146 164 déclarative '</p></body></html>'
x03 html
    0 2 exclamative '<!'
    2 65 interrogative '-- commentaire --><script>if (a < b && c > d) { console.log("x?'
    65 89 déclarative 'y=1"); }</script><p>Fin.'
    89 93 déclarative '</p>'
x06 markdown-code
    0 25 déclarative '> Citation : « Il part. »'
    27 36 déclarative '```python'
    37 63 déclarative 'def f(x):\n    return x + 1'
    64 67 déclarative '```'
x07 code-python
    0 64 déclarative 'def analyse(texte: str) -> dict:\n    """Analyse le texte (v1.2).'
    64 112 déclarative '"""\n    return {"texte": texte, "n": len(texte)}'
x08 code-json
    0 18 déclarative '{"schema": "drave.'
    18 94 déclarative 'annotation", "version": 1, "url": "https://example.com/a?b=2", "prix":'
x09 code-shell
    0 21 déclarative 'grep -n "TODO" src/*.'
    21 63 déclarative 'py | head -5 && echo "fini" > /tmp/out.txt'
x11 tableau-ascii
    0 17 déclarative '+-------+-------+'
    18 35 déclarative '| nom   | prix  |'
   
… [440 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/reaudit/cas20.json'))\nfor r in d:\n    if r['id'] in ('x12','x13','x14','x15','x18','x19'):\n        m=r['metriques']\n        print(r['id'],r['cat'],'langue',m['langue'],'scrip … [336 caractères tronqués]`

  ```
x12 arabe langue und script Arab refus '' labels 39
  niveaux {'graphème': 15, 'mot': 9, 'pos': 9, 'phrase': 2, 'pragmatique': 2, 'discours': 1, 'document': 1} trous {'mot': {'total': 7, 'sans_pos': 0}, 'ponctuation': {'total': 2, 'sans_pos': 0}} pos_zone {} sans_syntagme True
  phrases [(0, 21, 'déclarative'), (22, 35, 'déclarative')]
x13 chinois langue und script Hani refus '' labels 16
  niveaux {'graphème': 4, 'mot': 4, 'pos': 4, 'discours': 1, 'document': 1, 'phrase': 1, 'pragmatique': 1} trous {'mot': {'total': 2, 'sans_pos': 0}, 'ponctuation': {'total': 2, 'sans_pos': 0}} pos_zone {} sans_syntagme True
  phrases [(0, 16, 'déclarative')]
x14 russe langue und script Cyrl refus '' labels 39
  niveaux {'graphème': 15, 'mot': 9, 'pos': 9, 'phrase': 2, 'pragmatique': 2, 'discours': 1, 'document': 1} trous {'mot': {'total': 7, 'sans_pos': 0}, 'ponctuation': {'total': 2, 'sans_pos': 0}} pos_zone {} sans_syntagme True
  phrases [(0, 20, 'déclarative'), (21, 36, 'interrogative')]
x15 hébreu langue und script Hebr refus '' labels 43
  niveaux {'graphème': 17, 'mot': 10, 'pos': 10, 'phrase': 2, 'pragmatique': 2, 'discours': 1, 'document': 1} trous {'mot': {'total': 8, 'sans_pos': 0}, 'p
… [883 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys\nsys.path.insert(0,'tools'); import bloc_linguistique as bl\nd=json.load(open('/tmp/reaudit/cas20.json'))\nfor r in d:\n    if r['id'] in ('x18','x19'):\n        t=r['texte']\n        print(r['id'], … [463 caractères tronqués]`

  ```
x18 NFD? True texte_identique True
 tokens []
 mots [('E', 'mot', 0, 1), ('́', 'ponctuation', 1, 2), ('lodie', 'mot', 2, 7), ('sourit', 'mot', 8, 14), ('.', 'ponctuation', 14, 15), ('Le', 'mot', 16, 18), ('cafe', 'mot', 19, 23), ('́', 'ponctuation', 23, 24), ('est', 'mot', 25, 28), ('pre', 'mot', 29, 32), ('̂', 'ponctuation', 32, 33), ('t', 'mot', 33, 34), ('.', 'ponctuation', 34, 35)]
 pos [('E', 'NOUN'), ('́', 'PONCT'), ('lodie', 'NOUN'), ('sourit', 'NOUN'), ('.', 'PONCT'), ('Le', 'DET'), ('cafe', 'NOUN'), ('́', 'PONCT'), ('est', 'AUX'), ('pre', 'NOUN'), ('̂', 'PONCT'), ('t', 'PRON'), ('.', 'PONCT')]
x19 NFD? True texte_identique True
 tokens []
 mots [('Visitez', 'mot', 0, 7), ('https', 'mot', 8, 13), (':', 'ponctuation', 13, 14), ('/', 'ponctuation', 14, 15), ('/', 'ponctuation', 15, 16), ('exemple', 'mot', 16, 23), ('.', 'ponctuation', 23, 24), ('fr', 'mot', 24, 26), ('/', 'ponctuation', 26, 27), ('cafe', 'mot', 27, 31), ('́', 'ponctuation', 31, 32), ('?', 'ponctuation', 32, 33), ('x', 'mot', 33, 34), ('=', 'ponctuation', 34, 35), ('1', 'nombre', 35, 36), ('a', 'mot', 37, 38), ('̀', 'ponctuation', 38, 39), ('Paris', 'mot', 40, 45), ('.', 'ponctuation', 45, 46)]
 pos [('Visitez
… [308 caractères tronqués]
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Sondes CLI et contrat : codes, refus, --jsonl, --fichier, encodages, vues.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport os\nimport pathlib\nimport sys\n\nsys.path.insert(0, \"/tmp/reaudit\")\nimport commun as C\n\nSORTIE = pathlib.Path(\ … [10578 caractères tronqués]`

  ```
<path>/tmp/reaudit/run_probes.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 /tmp/reaudit/run_probes.py 2>&1 | tail -10", "description": "Lancer les sondes CLI et contrat", "timeoutMs": 600000}`

  ```
**kw).encode(obj)
          ~~~~~~^^^^^
  File "/usr/lib64/python3.13/json/encoder.py", line 202, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "/usr/lib64/python3.13/json/encoder.py", line 263, in iterencode
    return _iterencode(o, 0)
  File "/usr/lib64/python3.13/json/encoder.py", line 182, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
                    f'is not JSON serializable')
TypeError: Object of type bytes is not JSON serializable
[stderr]

real	0m12,469s
user	0m11,197s
sys	0m1,206s
  ```

- **bash** `{"command": "cd /tmp/reaudit && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('run_probes.py'); s=p.read_text()\ns=s.replace('n[\"fichier_brut\"] = chemin.read_bytes()[:40] if chemin.is_file() else None',\n            'n[\"fichier_brut_hex\"] = chemin.read_bytes()[:40].hex() if chemin.is_file()  … [246 caractères tronqués]`

  ```
ok
écrit /tmp/reaudit/probes.json
[stderr]

real	0m11,650s
user	0m10,487s
sys	0m1,174s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/reaudit/probes.json'))\nprint('== VERSION'); print(json.dumps(d['version'],ensure_ascii=False,indent=1)[:800])\nprint('== USAGE')\nfor k,v in d['usage'].items():\n    print(k,'rc … [577 caractères tronqués]`

  ```
== VERSION
{
 "--version": {
  "rc": 0,
  "stdout_octets": 12,
  "stderr": "",
  "json_valide": false,
  "erreur_json": "JSONDecodeError : Expecting value: line 1 column 1 (char 0)",
  "temps_ms": 184.55,
  "stdout": "drave 0.1.0"
 },
 "--aide": {
  "rc": 0,
  "stdout_octets": 875,
  "stderr": "",
  "json_valide": false,
  "erreur_json": "JSONDecodeError : Expecting value: line 1 column 1 (char 0)",
  "temps_ms": 159.97,
  "stdout": 875,
  "traceback": false
 },
 "-V": {
  "rc": 0,
  "stdout_octets": 12,
  "stderr": "",
  "json_valide": false,
  "erreur_json": "JSONDecodeError : Expecting value: line 1 column 1 (char 0)",
  "temps_ms": 155.86,
  "stdout": "drave 0.1.0"
 }
}
== USAGE
aucune_commande rc 2 out 0 json False refus None err usage: drave [-h] [-V] {analyser,evaluer,rejouer} ...
drave:
commande_inconnue rc 2 out 0 json False refus None err usage: drave [-h] [-V] {analyser,evaluer,rejouer} ...
drave:
option_inconnue rc 2 out 0 json False refus None err usage: drave [-h] [-V] {analyser,evaluer,rejouer} ...
drave:
langue_de rc 2 out 0 json False refus None err usage: drave analyser [-h] [--partition {brut,alternative,fi
partition_inconnue rc 2 out 0 json False refus None err 
… [1319 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/reaudit/probes.json'))\nprint('== FICHIER')\nfor k,v in d['fichier'].items():\n    print(k,'rc',v.get('rc'),'json',v.get('json_valide'),'texte',repr(v.get('texte'))[:60],'labels' … [642 caractères tronqués]`

  ```
== FICHIER
normal rc 0 json True texte 'Élodie sourit.' labels 14 octets 15 err 
vide rc 3 json True texte '' labels 0 octets 0 err 
inexistant rc 1 json False texte None labels None octets None err drave: erreur : FileNotFoundError : [Errno 2] No s
crlf rc 0 json True texte 'Il part.\nElle reste.\n' labels 33 octets 23 err 
bom rc 0 json True texte '\ufeffLe chat dort.' labels 22 octets 16 err 
invalide rc 0 json True texte 'a�b' labels 15 octets 3 err 
jsonl rc 0 json None texte None labels None octets None err 
== ENCODAGES
stdout_ascii_json {"rc": 0, "stdout_octets": 4186, "stderr": "", "json_valide": true, "erreur_json": "", "temps_ms": 162.36, "contrat": {"manquants": [], "erreurs": [], "schema": "", "ok": true}, "schema": "drave.annotation", "version": 1, "refus": "", "langue": "und", "script": "Latn", "texte": "Élodie sourit.", "la
stdout_ascii_lisible {"rc": 0, "stdout_octets": 481, "stderr": "", "traceback": false, "temps_ms": 153.49}
LC_ALL_C {"rc": 0, "stdout_octets": 4186, "stderr": "", "json_valide": true, "erreur_json": "", "temps_ms": 170.82, "contrat": {"manquants": [], "erreurs": [], "schema": "", "ok": true}, "schema": "drave.annotation", "version": 1, "refus": "
… [3195 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, collections\nd=json.load(open('/tmp/reaudit/banc50.json'))\nfor part in ('alternative','brut','filtrer_union','filtrer'):\n    pairs=sum(r['vues'][part]['metriques'].get('chevauchements_syntagme',0) fo … [1176 caractères tronqués]`

  ```
alternative pairs 149 textes 26 segs 408 union 129 alt 226
brut pairs 149 textes 26 segs 408 union 129 alt 0
filtrer_union pairs 41 textes 12 segs 350 union 129 alt 168
filtrer pairs 0 textes 0 segs 310 union 129 alt 128
temps_cli_ms min 142.63 med 158.805 mean 159.7 p95 172.29 max 248.44
temps_api_ms min 0.01 med 2.0765000000000002 mean 3.5 p95 4.619 max 55.487
json_octets min 330 med 15033.5 mean 29176.5 p95 29672 max 655792
OLD temps_cli_ms min 136.77 med 152.725 mean 157.3 p95 181.6 max 226.64
OLD temps_api_ms min 0.177 med 1.009 mean 2.2 p95 2.414 max 45.088
OLD json_octets min 0 med 12355.5 mean 24108.4 p95 27206 max 533611
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, collections\nd=json.load(open('/tmp/reaudit/cas20.json'))\nfor part in ('alternative','filtrer'):\n    pairs=sum(r['metriques' if part=='alternative' else 'filtrer']['metriques'].get('chevauchements_sy … [1028 caractères tronqués]`

  ```
alternative pairs 657 textes 8
filtrer pairs 0 textes 0
schema 20 / 20
deterministe 20 / 20
rc0 20 / 20
frontieres zone 2
phrases sans lettre 6
file parite [('x03', True, True), ('x16', True, True), ('x17', True, True), ('x18', True, True), ('x19', True, True)]
jsonl [('x04', 5, 5, 0, 5), ('x05', 4, 4, 1, 4), ('x06', 4, 4, 1, 4), ('x10', 1, 1, 0, 1), ('x11', 5, 5, 3, 5), ('x16', 320, 320, 0, 320), ('x20', 1, 1, 0, 1)]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, collections, statistics\nd=json.load(open('/tmp/reaudit/banc50.json'))\nagg=collections.Counter(); roles=collections.Counter(); non=collections.Counter(); zones=collections.Counter()\nlangues=collectio … [2505 caractères tronqués]`

  ```
AGG
{'labels': 4833, 'mots': 1068, 'pos': 1068, 'syntagmes': 408, 'attaches': 321, 'sans_attachement': 87, 'syntagmes_union': 129, 'syntagmes_alternative': 226, 'phrases': 67, 'phrases_espaces_initiaux': 0, 'phrases_vides': 0, 'documents': 49, 'doc_tronquees': 17, 'cibles': 321, 'cibles_absentes': 0, 'cibles_fermees': 18, 'cibles_ambigues': 60, 'cibles_un_caractere': 23, 'unites': 407, 'spans_hors_texte': 0, 'spans_vides': 0, 'valeurs_vides': 0, 'valeur_hors_surface': 0, 'doublons': 0, 'non_surface': 245, 'url_tokens': 0, 'emoji_tokens': 0, 'pos_emoji_ponct': 4, 'schema_ok': 50, 'texte_identique': 50, 'deterministe': 50, 'json_valide': 50, 'stderr_succes': 0, 'stdout_vide_succes': 0}
ROLES {'agent': 41, 'predicat': 106, 'possession': 10, 'qualite': 17, 'qualité': 12, 'prédicat': 53, 'temps': 11, 'patient': 60, 'hypothese': 4, 'destinataire': 15, 'contenu': 3, 'complément': 8, 'groupe nominal': 18, 'lieu': 12, 'but': 9, 'theme': 19, 'cause': 3, 'concession': 1, 'moyen': 5, 'maniere': 1}
NON_SURFACE {'discours': 67, 'phrase': 80, 'pragmatique': 77, 'morphème': 4, 'document': 17}
ZONES {'chemin': 35, 'url': 50, 'courriel': 10}
HOLES {'mot_total': 766, 'mot_sans': 0, 'ponctuation_total
… [1023 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, collections, sys\nsys.path.insert(0,'tools'); import bloc_linguistique as bl\nd=json.load(open('/tmp/reaudit/banc50.json'))\nun=[]; ferm=[]; amb=[]\nfor r in d:\n    t=r['texte']\n    for s in r.get('s … [613 caractères tronqués]`

  ```
UN CARACTERE 23
[('f20', 'M', 'GV', 'Dupont'), ('f38', 'c', 'GN', 'Les URL'), ('f38', 'c', 'GP', 'd=e#f'), ('f38', 'f', 'GV', 'http'), ('f38', 'f', 'GV', 'x'), ('f38', 'f', 'GV', 'y sont parfois coupées'), ('f39', 'C', 'GV', 'Windows\\System'), ('f41', 'ß', 'GN', 'Le texte contient'), ('f41', 'ß', 'GP', 'des accents é'), ('f41', 'ß', 'GP', 'des ligatures œ æ'), ('f50', 'h', 'GV', 'en notant chaque passage'), ('f50', 'h', 'GN', 'le'), ('f50', 'h', 'GV', 'trois chats sont entrés'), ('f50', 'ß', 'GP', 'à ç ù'), ('f50', 'ø', 'GN', 'les ligatures œ æ aussi'), ('f50', 'ø', 'GN', 'les emojis'), ('f50', 'ø', 'GV', 'restent lisibles'), ('f50', 'ø', 'GV', 'Ne supprimez pas'), ('f50', 'ø', 'GN', 'les lignes vides'), ('f50', 'ø', 'GV', 'elles séparent'), ('f50', 'ø', 'GN', 'les paragraphes'), ('f50', 'ø', 'GV', 'changent'), ('f50', 'ø', 'GN', 'la lecture')]
FERMEES 17
[('f05', 'pas', 'GP'), ('f05', 'pas', 'GN'), ('f10', 'est', 'GN'), ('f10', 'est', 'GP'), ('f10', 'est', 'GP'), ('f30', 'hier', 'GV'), ('f32', 'pas', 'GN'), ('f32', 'pas', 'GN'), ('f41', 'et', 'GP'), ('f43', 'ce', 'REL'), ('f43', 'ce', 'REL'), ('f50', 'Nous', 'GP'), ('f50', 'est', 'GP'), ('f50', 'ici', 'GN'), ('f50', 'Ce', 'REL'),
… [448 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys,collections\nsys.path.insert(0,'tools'); import bloc_linguistique as bl\ntextes=[]\nb=json.load(open('reports/pensee-fiabilite-produit.json'))['banc_50']['resultats']\ntextes += [('50',r['id'],r['te … [1537 caractères tronqués]`

  ```
labels 27788 meta_vide 19232 cand_vide 22010 actes 491
actes hors candidats 5
[('50', 'f03', 'exclamation', ['assertion', 'question', 'ordre']), ('50', 'f05', 'exclamation', ['assertion', 'question', 'ordre']), ('50', 'f31', 'exclamation', ['assertion', 'question', 'ordre']), ('50', 'f36', 'exclamation', ['assertion', 'question', 'ordre']), ('20', 'x03', 'exclamation', ['assertion', 'question', 'ordre'])]
doublons candidats 5
[('50', 'f06', 'syntagme', 'SUB', ['SUB', 'pense', 'pense', 'verrons']), ('50', 'f24', 'syntagme', 'REL', ['REL', 'fille', 'fille', 'au', 'était']), ('50', 'f43', 'syntagme', 'REL', ['REL', 'phrase', 'phrase', 'est', 'même']), ('50', 'f50', 'syntagme', 'SUB', ['SUB', 'dès', 'dès', 'descend', 'réveille']), ('50', 'f50', 'syntagme', 'SUB', ['SUB', 'sait', 'sait', 'tout'])]
meta schemas 11
  () 19232
  ('ouvert',) 6185
  ('attachement', 'niveau', 'role') 914
  ('alternative', 'attachement', 'niveau', 'partition', 'role') 761
  ('alternative', 'attachement', 'niveau', 'partition', 'role', 'union') 438
  ('alternative', 'niveau', 'partition', 'role', 'union') 86
  ('contexte', 'ouvert') 76
  ('niveau', 'role') 61
  ('alternative', 'niveau', 'partition', 'role') 26

… [78 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"P0-\\|P1-\\|P2-\" reports/rapport-fiabilite-produit.md | head -40 && sed -n 540,620p reports/rapport-fiabilite-produit.md", "description": "Lire la liste P0/P1 de l'audit précédent"}`

  ```
373:`TestSchemaV1` est sautée tant que `schema` n'existe pas. Elle deviendra stricte dès P0-1 livré.
450:                # peuvent s'ajouter sans casser ce test (transition P0-1).
513:    """Le schéma cible versionné — sauté tant que P0-1 n'est pas livré."""
568:| **P0-1** | **Versionner le format** : `schema` + `version` dans chaque annotation, `--version` les affiche | **0/46** annotations ; impossible d'épingler un rejeu | `drave.py` 50-52, 324 ; `bloc_linguistique.py` 116-127 | **2 h** | faible : champs additifs, test de schéma à ajouter |
569:| **P0-2** | **Refus en JSON + code 3** (le refus n'est plus une erreur) | **6 refus CLI** : stdout 0 octet, code 1 ; code 3 absent | `drave.py` 154-164, 265-272, 310-311 ; `bloc_linguistique.py` 1012-1017 | **2 h** | faible : JSON d'annotation sur stdout, code 3, docs/tests |
570:| **P0-3** | **Partition explicite des syntagmes** : `meta.alternative` + filtre `union` documenté (ou suppression mesurée) | **107 paires / 23 textes** ; 85 `union` ; 0 conflit après filtre | `bloc_linguistique.py` 1099-1156, 1179-1204, 1820-1849 | **0,5–1 j** | moyen : change F1/attachement ; préférer l'alternative étiquetée à la suppression |
571:| **P0-4** |
… [10991 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"P0\" docs/pilotage/en-cours.md | head -20", "description": "Voir les P0 courants dans l'état"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys,json\nsys.path.insert(0,'/tmp/reaudit'); import commun as C\nprint(json.dumps(C.snapshot(),ensure_ascii=False,indent=1))\nEOF", "description": "Prendre le snapshot du code et de la machine"}`

  ```
{
 "commit": "caeb730c7df6216c872348cb701b8188bb481c77",
 "commit_court": "caeb730c",
 "commit_date": "2026-11-07 01:24:53 -0500",
 "branche": "s/v7",
 "date_mesure": "2026-11-07T02:07:25-0500",
 "drave_sha256": "88ce03da9d9e11e48bc352083aaa94dd492b80798ef31268a1219689a78d463c",
 "bloc_sha256": "858197f736d758be2ca97e1ccd71a5045fd47d19d31c50afaf13fd669893b47f",
 "schema_sha256": "87d0bdb8527869cb1c92f0aa0318677c9beeade679682080ca222685c86cf04a",
 "python": "3.13.16",
 "machine": "Intel(R) Xeon(R) CPU E5-2687W v3 @ 3.10GHz",
 "nproc": "40",
 "os": "Linux-7.2.6-1-default-x86_64-with-glibc2.44",
 "statut_git": ""
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,sys,collections\nsys.path.insert(0,'tools'); import bloc_linguistique as bl\nd=json.load(open('reports/pensee-frontieres-phrase.json'))['corpus_40']\nident=0; schema=0; labels=0\nfor r in d:\n    a=bl.H … [404 caractères tronqués]`

  ```
texte identique 40 / 40 schema 40 labels 2107
  ```

