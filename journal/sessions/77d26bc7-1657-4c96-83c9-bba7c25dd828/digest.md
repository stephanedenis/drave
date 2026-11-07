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

