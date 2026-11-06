# Session DSH — relecture

- identifiant : `eedb7a58-2a33-4caa-8509-f46d9e328080`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-06 18:33:56
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **expliciter la partition des syntagmes** (P0-3 des audits : 23/46 textes libres à chevauchement, 132 paires), sans dédupliquer en silence.

Contexte : `tools/bloc_linguistique.py` (`Heuristique.analyser`, l'union S+chunker, `Etiquette.meta`), les audits `reports/rapport-fiabilite-produit.md` (107 paires, 85 `meta.union`) et `reports/rapport-produit-bloc-l.md` (132 paires ; la déduplication donne F1 0,5849→0,6141 mais **222→208** attachements exacts). `tools/drave.py` (CLI).

À faire :
1. **Cartographie** : sur les 50 textes des audits (relis-les dans les JSON d'audit) et sur des textes libres, classe les chevauchements : union S+chunker (le segment S contient le segment chunker), mêmes bornes multi-label, segments qui se croisent. Donne les effectifs par classe.
2. **Deux options mesurées** : (a) **explicite** — garder les deux segments mais marquer `meta.alternative` (le client choisit) ; (b) **filtrer** l'union (garder le chunker quand il est contenu dans un segment S plus large) — mesure le coût en attachement (attendu : 222→208 pour la déduplication, mais le filtre union est peut-être moins cher). Compare F1, attachement, POS, et la lisibilité de la sortie.
3. **Recommande** une option (ou une combinaison), avec le patch exact et le schéma de `meta.alternative`.
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-partition-syntagmes.md` et `reports/pensee-partition-syntagmes.json`.
5. Ne commite rien ; ne modifie aucun existant ; pas de `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, natifs. Simulation par sous-classe ou copie locale.

Rends un résumé : les classes de chevauchement, les deux options chiffrées, ta recommandation.
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

⏵ Exploring the repo structure and audit JSONs to understand the partition problem

I'll start by exploring the repository structure and the relevant files.

- **bash** `{"command": "pwd && git branch --show-current && git status --short | head -50 && ls", "description": "Check repo state and list top-level files"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
s/v7
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
MM journal/2026-11-06/README.md
D  journal/2026-11-06/distribue.md
D  journal/2026-11-06/docs.md
D  journal/2026-11-06/mesures.md
D  journal/2026-11-06/modele.md
D  journal/2026-11-06/outils.md
D  journal/2026-11-06/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
D  journal/sessions/082fe8ca-3e1e-4454-b91b-12586843e880/digest.md
D  journal/sessions/082fe8ca-3e1e-4454-b91b-12586843e880/rapport.md
D  journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/digest.md
D  journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/rapport.md
D  journal/sessions/1555bdd3-27e9-4779-b1e7-716e32399c11/digest.md
D  journal/sessions/1555bdd3-27e9-4779-b1e7-716e32399c11/rapport.md
D  journal/sessions/1b0cf09a-a77a-443d-82e2-6
… [1907 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | head -60 && echo '---' && ls reports/ | wc -l", "description": "List reports directory"}`

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
bilan-b11.md
bilan-multi-materiel.md
bloc-linguistique.json
bruit-entree.json
-
… [45 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -i -E 'bloc|fiabilite|produit' | head -50", "description": "Find audit JSON files"}`

  ```
bloc-linguistique.json
kv-cache-int8-bloc.json
pensee-fiabilite-produit.json
pensee-juge-bloc.json
pensee-produit-bloc-l.json
pensee-produit-v0.json
pensee-robustesse-produit.json
r41-bloc-tableaux.json
r42-bloc-code.json
r43-bloc-maths.json
rapport-bloc-linguistique.md
rapport-fiabilite-produit.md
rapport-hebbien-produits.md
rapport-kv-cache-int8-bloc.md
rapport-miroir-blocs.md
rapport-pensee-juge-bloc.md
rapport-produit-bloc-l.md
rapport-produit-v0.md
rapport-r41-bloc-tableaux.md
rapport-r42-bloc-code.md
rapport-r43-bloc-maths.md
rapport-robustesse-produit.md
  ```

- **bash** `{"command": "ls -la tools/bloc_linguistique.py tools/drave.py reports/rapport-fiabilite-produit.md reports/rapport-produit-bloc-l.md 2>&1", "description": "Check key files exist"}`

  ```
-rw-r--r--. 1 stephane stephane  39588  6 nov 12:56 reports/rapport-fiabilite-produit.md
-rw-------. 1 stephane stephane  34549  6 nov 11:31 reports/rapport-produit-bloc-l.md
-rw-------. 1 stephane stephane 120621  6 nov 18:07 tools/bloc_linguistique.py
-rw-------. 1 stephane stephane  17196  6 nov 18:07 tools/drave.py
  ```

- **bash** `{"command": "grep -n -i -E 'chevauche|union|alternative|dédupliqu|dedupliqu|partition|syntagme|overlap' reports/rapport-fiabilite-produit.md | head -60", "description": "Grep overlap mentions in first audit"}`

  ```
1:# Fiabilité du produit hors gold — 0 plantage sur 50 phrases, 4 refus sans JSON, 23/46 textes à chevauchement de syntagmes
21:mais **4 refus n'ont pas de JSON** (stdout vide, code 1), **23/46 succès** portent des syntagmes
22:qui se chevauchent, **4/46** n'ont **aucun syntagme**, **302/1068 tokens** n'ont **pas de POS**,
36:| chevauchements de syntagmes | **23/46** textes, **107** paires |
37:| textes sans aucun syntagme | **4/46** |
52:  **20 invariants** : clés, spans, `valeur` vs tranche, chevauchements, cibles, POS, unités,
57:  chevauchement, cible absente, confiance 1,7, clé manquante, fraction fausse, valeur hors span,
65:python3 tools/drave.py analyser "Élodie sourit."          # SYNTAGMES —
90:| syntagmes qui se chevauchent | **107 paires** dans **23/46** textes ; **85/360** étiquettes `meta.union` | f02 : `REL 22-42` et `REL 22-54` ; f50 : 50 paires |
91:| partition après filtre `meta.union` | **0 conflit** | le filtre marche, mais n'est pas dans le schéma |
92:| textes sans aucun syntagme | **4/46** | f13 (emoji), f18 (chiffres), f27 « Élodie sourit. », f37 (email/téléphone) |
97:| phrases qui se chevauchent | **1** paire | f20 : `[0:59]` et `[2:59]` sur `M. Dupont…` |
… [2988 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -i -E 'chevauche|union|alternative|dédupliqu|dedupliqu|partition|syntagme|overlap' reports/rapport-produit-bloc-l.md | head -60", "description": "Grep overlap mentions in second audit"}`

  ```
21:anomalie, dont **31/50** avec des **syntagmes qui se chevauchent** (188/362 étiquettes), les
24:document) est utilisable seule ; la structure (syntagmes, attachement, cascade) ne l'est pas encore.
32:| syntagme | ❌ | **132 paires** de chevauchement dans **31/50** textes, **188/362** étiquettes ; F1 gold **0,5849** |
37:| scripts non latins | ⚠️ | russe et chinois : graphème/mot/phrase/document, **0 syntagme**, **0 morphème** |
45:- **Analyses** : `Heuristique().analyser(texte)` (défaut : générateur S + union + chunker), plus
49:  cible d'attachement présente et token, segment d'attachement, chevauchements `pos`/`syntagme`/
68:| F1 syntagmes (vivant 612) | **0,5849** (P 0,6292 ; R 0,5464) |
129:  **50/50** textes ; **morphème manque 9 fois** (mots sans affixe productif) ; **syntagme manque
141:| **chevauchement de syntagmes** | **132 paires** | **31/50** | f02 : `GP 29-51` et `GP 29-60` ; `GV 80-96` et `GV 90-96` |
142:| **chevauchement de phrases** | 1 | f10 | `(0,104)` et `(2,104)` : l'extension d'abréviation (`M.`) ne fait pas avancer l'itérateur |
146:| **zéro** | 0 | — | span hors texte, span vide, cible absente, cible non-token, segment d'attachement, unité hors texte, unit
… [5734 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/pensee-fiabilite-produit.json reports/pensee-produit-bloc-l.json && python3 -c \"\nimport json\nfor p in ['reports/pensee-fiabilite-produit.json','reports/pensee-produit-bloc-l.json']:\n    d=json.load(open(p))\n    print(p, type(d), list(d)[:20] if isinstance(d,dict) els … [62 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 103706  6 nov 12:52 reports/pensee-fiabilite-produit.json
-rw-r--r--. 1 stephane stephane  82893  6 nov 11:33 reports/pensee-produit-bloc-l.json
reports/pensee-fiabilite-produit.json <class 'dict'> ['rapport', 'ligne', 'branche', 'commit_mesure', 'commit_module', 'date', 'objet', 'verdict', 'snapshot', 'dispositif', 'banc_50', 'robustesse', 'contrat', 'schema_propose', 'test_non_regression', 'correctifs', 'controle_negatif', 'limites', 'fichiers']
reports/pensee-produit-bloc-l.json <class 'dict'> ['rapport', 'ligne', 'branche', 'commit', 'date', 'objet', 'verdict', 'dispositif', 'gold', 'banc_50', 'cas_limites', 'performance', 'contrat', 'compositions', 'correctifs', 'controle_negatif', 'limites', 'fichiers']
  ```

- **bash** `{"command": "sed -n 330,420p reports/rapport-produit-bloc-l.md", "description": "Read dedup simulation table in audit 2"}`

  ```
| **P2-16** | Couvrir les caractères de contrôle dans graphème | x46 : **7 newlines** non couverts, 95,14 % ; 49/50 à 100 % | 1020-1031 | **15 min** |
| **P2-17** | Aligner la doc sur les plages réelles | fraction **0,3529–0,8750** (doc 0,51–0,76) ; `couverture()` = max, pas un taux | 111-114, 1237-1238 | **1 h** (doc) |
| **P2-18** | Nettoyages sans effet produit | `_verbe_dans` : boucle dupliquée 777-782 ; `trace` à schéma variable ; `priorite_syntagme="heuristique"` par défaut = mauvais choix pour le tagger réel | 777-782, 116-127, 1931, 1957 | **1 h** |

## 8. Contrôles négatifs

- **Les 6 mutations sont détectées (6/6)** : span hors texte, cible absente, chevauchement,
  confiance 1,7, valeur hors span, fraction incohérente. Le détecteur d'anomalies n'est pas
  complaisant ; noter que l'annotation de base porte déjà un chevauchement, donc le test de
  mutation ajoute une anomalie à un état déjà imparfait.
- **Le chunker seul ne chevauche pas** : 0 paire avec `segmenter_s=False, union=False`, contre 132
  avec le générateur S + union. Le défaut vient bien de la composition des segments, pas du
  détecteur.
- **La déduplication simulée** (`_supprimer_chevauchements`, politique a
… [5569 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nfor k in d:\n    v=d[k]\n    print(k, type(v).__name__, (len(v) if hasattr(v,'__len__') else ''))\nprint('---banc_50---')\nb=d['banc_50']\nprint(type(b), len(b))\nprint(json.dumps(b[0] if isinstan … [109 caractères tronqués]`

  ```
rapport str 17
ligne str 3
branche str 4
commit_mesure str 8
commit_module str 8
date str 10
objet str 166
verdict str 226
snapshot dict 5
dispositif dict 5
banc_50 dict 2
robustesse dict 2
contrat dict 5
schema_propose dict 6
test_non_regression dict 4
correctifs dict 3
controle_negatif dict 6
limites list 7
fichiers list 2
---banc_50---
<class 'dict'> 2
{"synthese": {"n": 50, "succes": 46, "refus": 4, "plantages": 0, "json_invalide": 0, "sorties_vides_sur_succes": 0, "spans_hors_texte": 0, "spans_vides": 0, "valeurs_vides": 0, "cles_racine_ko": 0, "cles_etiquette_ko": 0, "types_inconnus": 0, "cibles_absentes_du_texte": 0, "stderr_succes_non_vide": 0, "determinisme": "46/46", "labels": 4501, "mots": 1068, "pos": 766, "syntagmes": 360, "attachements": 284, "sans_attachement": 76, "syntagmes_par_type": {"GN": {"total": 87, "attaches": 83, "sans": 4, "union": 11}, "GV": {"total": 145, "attaches": 75, "sans": 70, "union": 35}, "GP": {"total": 86, "attaches": 84, "sans": 2, "union": 28}, "REL": {"total": 28, "attaches": 28, "sans": 0, "union": 10}, "SUB": {"total": 14, "attaches": 14, "sans": 0, "union": 1}}, "chevauchements": {"textes": 23, "t
  ```

- **bash** `{"command": "grep -n -E 'chunker|union|alternative|_supprimer_chevauchements|def analyser|class Etiquette|class Heuristique|meta' tools/bloc_linguistique.py | head -80", "description": "Locate key code sections"}`

  ```
68:class Etiquette:
79:    meta: dict = field(default_factory=dict)
87:            "script": self.script, "meta": dict(self.meta),
139:    def analyser(self, texte: str, langue: str | None = None,
531:class Heuristique:
538:                 union: bool = True):
543:        self.union = union
1009:    def analyser(self, texte: str, langue: str | None = None,
1053:                                            langue=lg, script=script, meta={"ouvert": ouvert}))
1073:                                          script=script, meta={"ouvert": True, "contexte": avant.type})
1087:                                           meta={"ouvert": True, "contexte": "pron_sujet"})
1107:                                       meta={"ouvert": False, "contexte": "det_sans_nom"})
1118:                                           meta={"ouvert": True, "contexte": "nom_sujet_3s"})
1143:        # 5. syntagmes : le générateur S (candidats) ou un chunker simple
1147:        # l'interroge que pour le français, sinon ses segments polluent l'union.
1151:        # **un seul chunking par analyse**, partagé par les trois chemins (S, union, chunker) :
1196:                    meta = {"role": s.get("role", ""), "niveau": s.
… [2086 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 60,135p tools/bloc_linguistique.py", "description": "Read Etiquette dataclass"}`

  ```
debut: int
    fin: int

    def json(self) -> dict:
        return {"debut": self.debut, "fin": self.fin}


@dataclass
class Etiquette:
    niveau: str
    type: str
    valeur: str
    debut: int
    fin: int
    source: str = "heuristique"
    confiance: float = 0.5
    candidats: list[str] = field(default_factory=list)
    langue: str = "und"
    script: str = SCRIPT_NEUTRE
    meta: dict = field(default_factory=dict)

    def json(self) -> dict:
        return {
            "niveau": self.niveau, "type": self.type, "valeur": self.valeur,
            "debut": self.debut, "fin": self.fin, "source": self.source,
            "confiance": round(float(self.confiance), 4),
            "candidats": list(self.candidats), "langue": self.langue,
            "script": self.script, "meta": dict(self.meta),
        }


SCHEMA_ANNOTATION = "drave.annotation"
VERSION_ANNOTATION = 1


@dataclass
class Annotation:
    texte: str
    langue: str = "und"
    script: str = SCRIPT_NEUTRE
    etiquettes: list[Etiquette] = field(default_factory=list)
    refus: str = ""
    trace: list[dict] = field(default_factory=list)
    cout: dict = field(default_factory=dict)
    unites_semantiques: list[Span] 
… [1393 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1130,1275p tools/bloc_linguistique.py", "description": "Read syntagm generation and union logic"}`

  ```
premier = next((m.group() for m in re.finditer(r"\w+", p)), "")
            acte = ("question" if typ == "interrogative" else
                    "exclamation" if typ == "exclamative" else
                    "ordre" if premier.casefold() in VERBES_IMPERATIFS else "assertion")
            etiquettes.append(Etiquette("pragmatique", "acte", acte, d, f, self.nom, 0.45,
                                        candidats=["assertion", "question", "ordre"],
                                        langue=lg, script=script))
            if (" ou " in p or "«" in p or "“" in p
                    or any(m in _normaliser(p) for m in MOTS_DOUBLE_SENS)):
                etiquettes.append(Etiquette("pragmatique", "double_sens", "candidat", d, f,
                                            self.nom, 0.25, candidats=["littéral", "figuré"],
                                            langue=lg, script=script))

        # 5. syntagmes : le générateur S (candidats) ou un chunker simple
        verbes = [(e.debut, e.fin, e.valeur) for e in etiquettes
                  if e.niveau == "pos" and e.type == "VERB"]
        # le générateur S est **français** : il ne segmente pas l'anglais (A14) — on ne
    
… [8526 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1860,1905p tools/bloc_linguistique.py && echo '=== appel ===' && sed -n 1940,1990p tools/bloc_linguistique.py", "description": "Read dedup function and fusion call"}`

  ```
trace=[{"etape": "neuronal-pragmatique", "erreur": str(e)[:160]}],
                                    cout={"octets": len(texte.encode("utf-8", "replace")),
                                          "duree_s": round(time.perf_counter() - t0, 6)})
        if self.cache:
            self._cache[cle] = annotation
        return annotation


# --------------------------------------------------------------------------- compositions


def _supprimer_chevauchements(etiquettes: list[Etiquette],
                              priorite_syntagme: str = "heuristique") -> list[Etiquette]:
    """Les alternatives se suppriment **par type** quand les types sont complémentaires.

    `pos` et `syntagme` sont des alternatives de **span** : on garde la plus confiante.
    Pour le **syntagme**, la politique par défaut (`heuristique`) garde la segmentation de
    l'heuristique ; `confiance` laisse la plus confiante gagner (le tagger neuronal à 0,6
    passe devant l'heuristique à 0,4). `phrase` (type/négation/modalité), `pragmatique` (acte/double_sens/contexte), `discours`
    (paragraphe/connecteur) et `document` (titre/paragraphe) portent des types **complémentaires**
    sur le même span : les supp
… [4217 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor p in ['reports/pensee-fiabilite-produit.json','reports/pensee-produit-bloc-l.json']:\n    d=json.load(open(p))\n    print('====',p)\n    for k,v in d.items():\n        print(' ',k, type(v).__name__, len(v) if hasattr(v,'__len__') else '')\n    b=d.get( … [330 caractères tronqués]`

  ```
==== reports/pensee-fiabilite-produit.json
  rapport str 17
  ligne str 3
  branche str 4
  commit_mesure str 8
  commit_module str 8
  date str 10
  objet str 166
  verdict str 226
  snapshot dict 5
  dispositif dict 5
  banc_50 dict 2
  robustesse dict 2
  contrat dict 5
  schema_propose dict 6
  test_non_regression dict 4
  correctifs dict 3
  controle_negatif dict 6
  limites list 7
  fichiers list 2
 banc keys: ['synthese', 'resultats']
    synthese dict 44
    resultats list 50
    sample: {"id": "f01", "categorie": "fr", "attendu": "fr", "texte": "Le chat dort.", "caracteres": 13, "octets_utf8": 13, "rc": 0, "temps_cli_ms": 150.79, "temps_api_ms": 0.796, "deterministe": true, "json_octets": 5561, "json_valide": true, "langue": "fr", "script": "Latn", "labels": 19, "mots": 4, "pos": 3, "syntagmes": 2, "attaches": 2, "sans_attachement": 0, "chevauchements_syntagme": 0, "chevauchements_phrase_type": 0, "syntagmes_union": 0, "conflits_apres_filtre_union": 0, "cibles_fermees": 0, "cib
==== reports/pensee-produit-bloc-l.json
  rapport str 14
  ligne str 3
  branche str 4
  commit str 40
  date str 10
  objet str 185
  verdict str 311
  dispositif dict 9
  gold dict 31
  banc_50 di
… [1390 caractères tronqués]
  ```

- **bash** `{"command": "git status --short tools/bloc_linguistique.py tools/drave.py reports/ docs/ && git log -1 --format='%H %cd %s' -- tools/bloc_linguistique.py && git diff --stat HEAD -- tools/bloc_linguistique.py", "description": "Check module modification state vs HEAD"}`

  ```
M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-spans-chunker.md
?? docs/produit/schema-v1.json
?? reports/rapport-s-paragraphes.md
037fe0412a8cb98a3d1947a0cdd6fcf9d6191a78 Fri Nov 6 18:14:19 2026 -0500 PRODUIT — LE CONTRAT V1 : schema/version, REFUS EN JSON (CODE 3), SURROGATE ET NON-STR TOLÉRÉS ; PORTE À 8 CONTRÔLES ; 183/183
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\na=json.load(open('reports/pensee-fiabilite-produit.json'))\nb=json.load(open('reports/pensee-produit-bloc-l.json'))\nta=[r['texte'] for r in a['banc_50']['resultats']]\ntb=[r['texte'] for r in b['banc_50']['detail']]\nprint(len(ta),len(tb))\nprint('communs … [240 caractères tronqués]`

  ```
50 50
communs 0
A only 50 B only 50
diff idx 0 'Le chat dort.' || 'Le chat dort sur le canapé.'
diff idx 1 'Le chat de la voisine qui dort sur le toit se réveille.' || 'La voisine arrose les fleurs du jardin chaque matin avant de partir au travail, puis elle rentre vers dix-huit heures et prépare le dîner pour ses deux enfants.'
diff idx 2 "Bonjour ! Comment allez-vous aujourd'hui ?" || "Le livre que tu m'as prêté hier soir était passionnant, même si la fin m'a un peu déçu."
diff idx 3 "Ferme la porte, s'il te plaît." || 'Quand la pluie tombe depuis trois jours, les rues du village se transforment en ruisseaux boueux et les enfants rentrent trempés.'
diff idx 4 'Ne touche pas à ça !' || '« Je ne sais pas », répondit-elle en haussant les épaules ; son frère, lui, prétendait le contraire.'
diff idx 5 "Je ne pense pas qu'il viendra demain, mais nous verrons bien." || 'Peut-être que nous devrions reporter la réunion à demain, non ?'
diff idx 6 'The cat sleeps on the roof.' || "Ferme la porte, s'il te plaît, et n'oublie pas d'éteindre la lumière !"
diff idx 7 'Where is the nearest train station, please?' || "Il n'a jamais vraiment compris pourquoi elle était partie sans laisser d'adress
… [9149 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/tests/linguistique/ && sed -n 1,80p tools/tests/linguistique/evaluer_gold.py", "description": "Inspect gold evaluation harness"}`

  ```
anaphore.py
classement_cible.py
evaluer_gold.py
gold_gele.json
gold.json
gold.py
gold_reel.json
gold_reel.py
gold_split.py
gold_synthetique.json
gold_synthetique.py
juge.py
miroir.py
__pycache__
qualifier_cascade.py
qualifier_frontiere_71.py
qualifier_lien_appris.py
qualifier_neuronal.py
qualifier_pragmatique.py
qualifier_quatre_modes.py
qualifier_syntagmes.py
replis_cible.py
test_bloc_linguistique.py
"""evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) + synthétique (160).

Trois niveaux : POS (token, exact), syntagmes (exact + **par tête**), pragmatique. Quatre
lectures : heuristique, mock neuronal, parallèle, cascade. Le vrai modèle est optionnel
(`--reel`) : s'il ne répond pas, il est refusé, pas simulé.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections import Counter, defaultdict

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl  # noqa: E402

GOLD = pathlib.Path(__file__).with_name("gold.json")
REEL = pathlib.Path(__file__).with_name("gold_reel.json")
SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")


def 
… [2249 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -E 'def (charger|evaluer_bloc|main)|argparse|gold' tools/tests/linguistique/evaluer_gold.py | head -40 && echo '---' && grep -rn 'attachement' tools/tests/linguistique/*.py | head -30", "description": "Find gold functions and attachment evaluation"}`

  ```
1:"""evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) + synthétique (160).
9:import argparse
19:GOLD = pathlib.Path(__file__).with_name("gold.json")
20:REEL = pathlib.Path(__file__).with_name("gold_reel.json")
21:SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")
24:def charger() -> list[dict]:
35:GELE = pathlib.Path(__file__).with_name("gold_gele.json")
38:def charger_gele() -> list[dict]:
39:    """Le gold **gelé** : une copie figée pour les portes à nombre absolu.
41:    Le gold vivant grandit (phrases, liens) ; les portes qui codent un chiffre exact
80:def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
109:        pred_seg, gold_seg = _seg(a), {(s["type"], s["debut"], s["fin"]) for s in phrase["segments"]}
110:        tp += len(pred_seg & gold_seg)
111:        fp += len(pred_seg - gold_seg)
112:        fn += len(gold_seg - pred_seg)
114:        gold_tete = {(s["type"], s["debut"]) for s in phrase["segments"]}
115:        ttp += len(pred_tete & gold_tete)
116:        tfp += len(pred_tete - gold_tete)
117:        tfn += len(gold_tete - pred_tete)
138:            # le gold admet parfois plusieurs cibles (43/96 GP) : mesure secondaire
1
… [4133 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 80,230p tools/tests/linguistique/evaluer_gold.py", "description": "Read full gold evaluation logic incl. attachment"}`

  ```
def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
    tp = fp = fn = ttp = tfp = tfn = 0
    pos_ok = pos_n = pos_ok_ferme = pos_n_ferme = pos_ok_ouvert = pos_n_ouvert = 0
    conf = defaultdict(Counter)
    acte_ok = neg_ok = mod_ok = ds_ok = 0
    fractions = []
    att_n = att_labels = att_top1 = att_topk = att_exact = 0
    att_topk_exact = 0
    att_exact_any = 0
    par_langue = {"fr": {"cibles": 0, "labels": 0, "exact": 0, "topk": 0},
                  "en": {"cibles": 0, "labels": 0, "exact": 0, "topk": 0}}
    att_v_n = att_v_ok = att_n_n = att_n_ok = 0
    att_t_n = att_t_labels = att_t_top1 = att_t_topk = 0
    for phrase in phrases:
        a = bloc.analyser(phrase["texte"], phrase["langue"])
        fractions.append(a.fraction_semantique)
        pos = _pos_map(a)
        for mot in phrase["mots"]:
            pred = pos.get((mot["debut"], mot["fin"]), "?")
            pos_n += 1
            pos_ok += int(pred == mot["pos"])
            ferme = mot["pos"] in {"DET", "PREP", "PRON", "CONJ", "AUX", "ADV", "NUM"}
            if ferme:
                pos_n_ferme += 1
                pos_ok_ferme += int(pred == mot["pos"])
            else:
                pos
… [7156 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 230,320p tools/tests/linguistique/evaluer_gold.py", "description": "Read main of gold harness"}`

  ```
phrases = charger()
    h, n = bl.Heuristique(), bl.MockNeuronal()
    cascade = bl.Cascade(h, n)
    blocs = {"heuristique": h, "mock_neuronal": n,
             "parallele": bl.Parallele([h, n]), "cascade": cascade}
    sources = {"all": phrases,
               "reel": [p for p in phrases if p["source"] in ("hand", "reel")],
               "hand": par_source(phrases, "hand"),
               "reel_new": par_source(phrases, "reel"),
               "synthetique": par_source(phrases, "synthetique")}
    resultats = {nom: {src: evaluer_bloc(nom, bloc, ps) for src, ps in sources.items()}
                 for nom, bloc in blocs.items()}
    resultats["cascade"]["appels_neuronal"] = cascade.appels_neuronal
    reel = {"statut": "non demandé"}
    if args.reel:
        try:
            from bloc_linguistique import NeuronalLLM
            m = NeuronalLLM(RACINE / "models/Qwen2.5-0.5B-Q4_0.gguf", timeout=10)
            a = m.analyser("Le chat dort.", "fr")
            reel = {"statut": "ok", "etiquettes": len(a.etiquettes)}
        except Exception as e:
            reel = {"statut": "refus", "detail": type(e).__name__ + ": " + str(e)[:160]}
    resultats["reel"] = reel
    # contrôle néga
… [3292 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. timeout 900 python3 tools/tests/linguistique/evaluer_gold.py 2>&1 | tail -60", "description": "Run gold evaluation baseline"}`

  ```
}
   },
   "pragmatique": {
    "acte": 0.9967,
    "negation": 0.9771,
    "modalite": 0.9886,
    "double_sens": 0.9444
   },
   "fraction_semantique": 0.5834,
   "attachement": {
    "cibles": 239,
    "labels": 208,
    "top1": 208,
    "topk": 207,
    "exact": 208,
    "top1_taux": 0.8703,
    "topk_taux": 0.8661,
    "exact_taux": 0.8703,
    "exact_any": 208,
    "exact_any_taux_span": 1.0,
    "top1_taux_span": 1.0,
    "topk_taux_span": 0.9952,
    "topk_exact": 207,
    "topk_exact_taux": 0.8661,
    "topk_exact_taux_span": 0.9952,
    "exact_taux_span": 1.0,
    "verbe": {
     "cibles": 138,
     "justes": 138,
     "taux": 1.0
    },
    "nom": {
     "cibles": 70,
     "justes": 70,
     "taux": 1.0
    },
    "couverture": 0.8703,
    "par_langue": {
     "fr": {
      "cibles": 151,
      "labels": 122,
      "exact": 122,
      "topk": 121,
      "exact_taux_span": 1.0
     },
     "en": {
      "cibles": 88,
      "labels": 86,
      "exact": 86,
      "topk": 86,
      "exact_taux_span": 1.0
     }
    }
   },
   "attachement_tete": {
    "cibles": 208,
    "labels": 208,
    "top1": 208,
    "topk"
heuristique all: {"pos": {"exactitude": 0.8383, "exactitude_fer
… [926 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Building a local harness to reproduce the audit overlaps and classify them

- **bash** `{"command": "mkdir -p /tmp/partition_syntagmes && cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 531,620p tools/bloc_linguistique.py", "description": "Read Heuristique init and analyser start"}`

  ```
class Heuristique:
    """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""

    nom = "heuristique"

    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
                 seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
                 union: bool = True):
        self.profils = profils
        self.segmenter_s = segmenter_s
        self.seuil_ouvert = seuil_ouvert
        self.seuil_langue = seuil_langue
        self.union = union

    # -- langues / script ---------------------------------------------------
    def _langue(self, texte: str, indice: str | None) -> tuple[str, float, str]:
        langue, conf, _ = detecter_langue(texte, self.profils, indice)
        script = detecter_script(texte)
        if conf < self.seuil_langue:
            return "und", conf, script
        return langue, conf, script

    # -- tokens -------------------------------------------------------------
    @staticmethod
    def _mots(texte: str) -> list[tuple[int, int, str, str]]:
        motif = re.compile(r"\b[ldmtsnLDMTNS]['’](?=\w)|\w+(?:['’\-]\w+)*|\d+(?:[.,]\d+)*|https?://\S+|[\U0001F300-\U0001FAFF]|[^\w\s]
… [2918 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1009,1060p tools/bloc_linguistique.py && sed -n 1,60p tools/bloc_linguistique.py", "description": "Read analyser signature and module header"}`

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
… [4311 caractères tronqués]
  ```

- **write** `{"file_path": "/tmp/partition_syntagmes/inventaire.py", "content": "\"\"\"Inventaire et classification des chevauchements de syntagmes.\n\nNe modifie rien dans le dépôt : importe le module tel quel, relit les 50 textes\ndes deux JSON d'audit, et rend les effectifs par classe.\n\"\"\"\nfrom __future_ … [5350 caractères tronqués]`

  ```
<path>/tmp/partition_syntagmes/inventaire.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. timeout 600 python3 /tmp/partition_syntagmes/inventaire.py 2>&1 | tail -40", "description": "Run overlap inventory on both audit bancs"}`

  ```
fiabilite {"textes": 46, "textes_avec_chevauchement": 24, "paires": 130, "syntagmes": 386, "union": 110, "attaches": 295, "classes": {"union_contenu": 83, "inclusion_s_dans_union": 33, "croisement": 11, "meme_span_union": 3}}
  ex inclusion_s_dans_union f02 'qui dort sur le toit' | 'qui dort sur le toit se réveille' {'type': 'REL', 'debut': 22, 'fin': 42, 'union': False, 'att': True} {'type': 'REL', 'debut': 22, 'fin': 54, 'union': True, 'att': True}
  ex croisement f06 'Je ne pense pas' | "ne pense pas qu'il viendra demain" {'type': 'GV', 'debut': 0, 'fin': 15, 'union': False, 'att': False} {'type': 'GV', 'debut': 3, 'fin': 36, 'union': True, 'att': False}
  ex union_contenu f06 'nous verrons bien' | 'verrons bien' {'type': 'GV', 'debut': 43, 'fin': 60, 'union': False, 'att': False} {'type': 'GV', 'debut': 48, 'fin': 60, 'union': True, 'att': False}
  ex meme_span_union f50 "où il passe l'après-midi" | "où il passe l'après-midi" {'type': 'REL', 'debut': 209, 'fin': 233, 'union': False, 'att': True} {'type': 'SUB', 'debut': 209, 'fin': 233, 'union': True, 'att': True}
bloc_l {"textes": 50, "textes_avec_chevauchement": 32, "paires": 139, "syntagmes": 374, "union": 107, "attaches": 2
… [1037 caractères tronqués]
  ```

