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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -8 -- tools/bloc_linguistique.py && echo '---' && git cat-file -t fa1b0c6e 2>&1 && git show fa1b0c6e:tools/bloc_linguistique.py > /tmp/partition_syntagmes/bloc_fa1b0c6e.py && wc -l /tmp/partition_syntagmes/bloc_fa1b … [79 caractères tronqués]`

  ```
037fe041 PRODUIT — LE CONTRAT V1 : schema/version, REFUS EN JSON (CODE 3), SURROGATE ET NON-STR TOLÉRÉS ; PORTE À 8 CONTRÔLES ; 183/183
2ba393b0 B13 — LA POS À 83,83 % (R2a/R3/R2b) : F1 0,5849 → 0,6181, ANGLAIS 0,6341 → 0,7273, ATTACHEMENT INCHANGÉ (222/222) ; 183/183
1962eb15 PRODUIT — LA ROBUSTESSE : SURROGATE ET NON-STR FERMÉS (refus non_texte), 8 TESTS ; L'AUDIT A24 (50 PHRASES, 132 CHEVAUCHEMENTS, 18 CORRECTIFS)
0911ae29 B13 — 222/222 (1,0000) : LE DERNIER MARQUEUR AMBIGU (when APRÈS UN GN), COUVERTURE 0,9289, 17 SPANS TOUS INATTEIGNABLES ; 183/183
653a7981 B13 — LES DEUX DERNIÈRES RÉGRESSIONS (s037, r303) : EXACT 221/221 (1,0000), COUVERTURE 0,9247, 18 SPANS ; AUDIT V10 INTÉGRÉ, V10 CORRIGÉE ; 183/183
710ec7f9 B13 — LE FÉMININ -ÉE ET LA GARDE DÉTERMINANT DU GP : EXACT 220/220 (1,0000), COUVERTURE 0,9205, F1 0,5880, 19 SPANS ; 183/183
160d08ca B13 — LA GARDE PRON : EXACT 219/219 (1,0000), COUVERTURE 0,9163, F1 0,5822, DEV 152/152 ET TEST 67/67 ; AUDIT DE COHÉRENCE V8 INTÉGRÉ ; 183/183
d497324b B13 — TOP-K 211/239 (LE SITE D'APPEL prec = s), LA V8 RÉÉCRITE HONNÊTEMENT (+17 NET, 7 RÉGRESSIONS), AUDITS A17/A19 INTÉGRÉS ; 183/183
---
commit
2192 /tmp/partition_syntagmes/bloc_fa1b0
… [6 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in gold gold_reel gold_synthetique gold_gele; do echo -n \"$f fa1b0c6e: \"; git show fa1b0c6e:tools/tests/linguistique/$f.json 2>/dev/null | python3 -c \"import json,sys; d=json.load(sys.stdin); print(len(d.get('phrases',[])))\ … [203 caractères tronqués]`

  ```
gold fa1b0c6e: 20
gold HEAD: 20
gold_reel fa1b0c6e: 432
gold_reel HEAD: 432
gold_synthetique fa1b0c6e: 160
gold_synthetique HEAD: 160
gold_gele fa1b0c6e: 602
gold_gele HEAD: 602
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show fa1b0c6e:tools/tests/linguistique/evaluer_gold.py | head -30 && echo '--- diff evaluer ---' && git diff fa1b0c6e HEAD --stat -- tools/tests/linguistique/evaluer_gold.py", "description": "Check old gold harness compatibility" … [1 caractères tronqués]`

  ```
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


def charger() -> list[dict]:
    hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
    reel = json.loads(REEL.read_text(encoding="utf-8"))["phrases"]
    synth = json.loads(SYNTH.read_text(encoding="utf-8"))["phrases"]
    for p in hand:
        p["source"] = "hand"
    for p in reel:
--- diff evaluer ---
 tools/tests/linguistique/evaluer_gold.py | 5 ++++-
 1 file changed, 4 insertions(+), 1 d
… [10 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. timeout 900 python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/partition_syntagmes/base_head.json >/dev/null 2>&1; python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/partition_syntagmes/base_head.json'))\nfo … [494 caractères tronqués]`

  ```
heuristique F1 0.6181 P 0.655 R 0.5851 tete 0.7511 POS 0.8383
   att cibles 239   att labels 222   att exact 222   att exact_taux 0.9289   att couverture 0.9289   att top1 222   att topk 221
cascade F1 0.6495 P 0.7557 R 0.5695 tete 0.7616 POS 0.7528
   att cibles 239   att labels 208   att exact 208   att exact_taux 0.8703   att couverture 0.8703   att top1 208   att topk 207
parallele F1 0.6495 P 0.7557 R 0.5695 tete 0.7616 POS 0.7528
   att cibles 239   att labels 208   att exact 208   att exact_taux 0.8703   att couverture 0.8703   att top1 208   att topk 207
gold {'phrases': 612, 'reel': 452, 'hand': 20, 'reel_new': 432, 'synthetique': 160, 'tokens': 3179}
ok True
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls data/ | head -40 && echo '---' && find data -maxdepth 2 -type f | head -40", "description": "Explore corpus data for free texts"}`

  ```
adaptateurs
alignement
composition-etats.npz
composition-verne-14b-etats.npz
composition-verne-7b-etats.npz
composition-verne-etats.npz
composition-verne-large-etats.npz
composition-verne-plan-etats.npz
consignes_train.jsonl
consignes_val.jsonl
corpus_en.txt
corpus_en_val.txt
corpus_fr_litterature.txt
corpus_fr_train.txt
corpus_fr.txt
corpus_fr_val.txt
corpus_litt_propre
corpus_mixte_dev.txt
corpus_mixte_litt2.txt
corpus_mixte_litt.txt
corpus_mixte_propre.txt
corpus_mixte.txt
corpus_multi_train.txt
corpus_multi.txt
corpus_multi_val.txt
corpus_nonambigu
corpus_ocr
corpus_ocr_cegep
corpus_ocr_cegep_avant_micro
corpus_ocr_cegep_micro
corpus_ocr_cegep_pilote-2pages
corpus_pdf
corpus_pdf_documents
corpus_propre
corpus_repo_propre
corpus_repo.txt
corpus_wiki_ar
corpus_wiki_ar_texte
corpus_wiki_de
corpus_wiki_de_texte
---
data/wikitext2_test.txt
data/wt2.json
data/wikitext2_test.txt.ids
data/corpus_en_val.txt
data/corpus_en.txt
data/corpus_fr.txt
data/corpus_mixte.txt
data/corpus_fr_litterature.txt
data/corpus_mixte_litt.txt
data/corpus_mixte_litt2.txt
data/udhr/langues.jsonl
data/udhr/articles.jsonl
data/udhr/udhr_train.txt
data/udhr/meta.json
data/udhr/articles_propres.jsonl
data/udhr/u
… [707 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn -i 'texte libre\\|textes libres' reports/rapport-fiabilite-produit.md reports/rapport-produit-bloc-l.md | head -20", "description": "Find mentions of free texts in audits"}`

  ```
reports/rapport-produit-bloc-l.md:54:- **Ce que ce banc ne mesure pas** : la justesse sémantique sur texte libre (pas de gold), la
reports/rapport-produit-bloc-l.md:372:  sur texte libre n'a pas de gold ; on cite le gold 0,7581 et des exemples, pas une exactitude
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,120p tools/drave.py", "description": "Read drave CLI top"}`

  ```
#!/usr/bin/env python3
"""drave.py — le point d'entrée produit du bloc linguistique.

Une seule commande, trois gestes, hors ligne et déterministe :

    python3 tools/drave.py analyser "Le chat dort."
    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
    python3 tools/drave.py evaluer
    python3 tools/drave.py evaluer --gold --json
    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
    python3 tools/drave.py --version

Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
avec rôle et cible d'attachement, pragmatique, unités sémantiques — et sa mesure sur le gold.
Ce qu'elle n'expose pas encore : le neuronal (`llama-cli` ou endpoint local), la restitution
(annotation → texte), la traduction et la génération : ils demandent des poids, un service ou
un GPU, alors que ce prototype est hors ligne, CPU et sans réseau.

Codes de sortie : 0 succès · 2 usage · 1 erreur (ou refus d'analyse).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import random
import sys
import textwrap

# Le dépôt d'abord — 
… [3762 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -E 'analyser|--mode|print|json' tools/drave.py | head -50 && echo '--- corpus ---' && wc -c data/corpus_fr_litterature.txt data/corpus_fr.txt && head -c 600 data/corpus_fr_litterature.txt", "description": "Inspect CLI output  … [17 caractères tronqués]`

  ```
6:    python3 tools/drave.py analyser "Le chat dort."
7:    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
9:    python3 tools/drave.py evaluer --gold --json
13:Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
26:import json
57:    return _sur(json.dumps(objet, ensure_ascii=False, indent=1)) + "\n"
62:    return _sur(json.dumps(a.json(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
159:def cmd_analyser(args: argparse.Namespace) -> int:
160:    annotation = bl.Heuristique().analyser(args.texte, args.langue)
163:        if args.json:
164:            sys.stdout.write(_dumps(annotation.json()))
166:            print(f"{NOM}: refus d'analyse : {annotation.refus} "
169:    if args.json:
170:        sys.stdout.write(_dumps(annotation.json()))
172:        print(_sur(formater_annotation(annotation)))
267:    if args.json:
270:        print(_formater_evaluation(rapport))
275:    premiere = bl.Heuristique().analyser(args.texte, args.langue)
276:    seconde = bl.Heuristique().analyser(args.texte, args.langue)
279:        print(f"{NOM}: refus d'analyse : {refus} "
286:    print(f"rejeu identique : {'
… [2191 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1275,1340p tools/bloc_linguistique.py", "description": "Read end of Heuristique.analyser"}`

  ```
if m.group().strip():
                paragraphes.append((m.start(), m.end(), m.group()))
        for d, f, p in paragraphes:
            etiquettes.append(Etiquette("discours", "paragraphe", "suite", d, f, self.nom, 0.5,
                                        candidats=["suite", "contraste", "cause", "conséquence"],
                                        langue=lg, script=script))
            titre = (p.lstrip().startswith("#") or
                     bool(re.match(r"^\s*(?:\d+[.)]|[IVXLC]+[.)])\s+", p)) or
                     (len(p.strip()) < 80 and p.strip().endswith((":", ".")) is False and
                      p.strip() == p.strip().upper()))
            etiquettes.append(Etiquette("document", "titre" if titre else "paragraphe",
                                        p.strip()[:60], d, f, self.nom, 0.7,
                                        langue=lg, script=script))
        if contexte:
            etiquettes.append(Etiquette("pragmatique", "contexte", contexte[:200], 0, len(texte),
                                        "humain", 1.0, langue=lg, script=script))

        # 7. unités sémantiques : ouvertes + syntagmes ambiguës, dédupliquées
        unites = _fusionner
… [2124 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'unites.append' tools/bloc_linguistique.py | head -20 && sed -n 1060,1130p tools/bloc_linguistique.py", "description": "Check semantic units construction"}`

  ```
1055:                    unites.append(Span(d, f))
1349:                    unites.append(Span(d, f))
                                                langue=lg, script=script))

        # 3 bis. le contexte tranche les suffixes ambigus : un mot après DET/PRÉP/ADJ est un
        # nom (« brother », « chair » ne sont pas des verbes) — A14 : 176 VERB gold en NOUN.
        pos_idx = [i for i, e in enumerate(etiquettes) if e.niveau == "pos"]
        for k, i in enumerate(pos_idx):
            e = etiquettes[i]
            if e.type != "VERB" or e.confiance > 0.45 or k == 0:
                continue
            avant = etiquettes[pos_idx[k - 1]]
            if avant.type in ("DET", "PREP", "ADJ"):
                etiquettes[i] = Etiquette("pos", "NOUN", e.valeur, e.debut, e.fin, self.nom,
                                          e.confiance, candidats=["noun"], langue=lg,
                                          script=script, meta={"ouvert": True, "contexte": avant.type})

        # 3 a. après un pronom sujet, un mot inconnu est un verbe (« she sings ») ; l'exception
        # est morphologique : une désinence nominale reste un nom (« happiness »).
        _nominales = ("tion", "sion"
… [3327 caractères tronqués]
  ```

- **write** `{"content": "\"\"\"Mesure des options de partition des syntagmes (aucune modification du dépôt).\n\nVariantes :\n  base              : Heuristique() telle quelle (S + union).\n  alternative       : base + meta.alternative / meta.partition (les deux segments restent).\n  filtrer_chunker   : option (b … [16542 caractères tronqués]`

  ```
<path>/tmp/partition_syntagmes/options.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/tmp/partition_syntagmes/options.py", "old_string": "    parent = list(range(len(segs)))\n\n    def trouver(i: int) -> int:\n        while parent[i] != i:\n            parent[i] = parent[parent[i]]\n            i = parent[i]\n        return i\n\n    for i, j in ((segs.index(x), segs.i … [374 caractères tronqués]`

  ```
The file /tmp/partition_syntagmes/options.py has been updated successfully.
  ```

- **edit** `{"file_path": "/tmp/partition_syntagmes/options.py", "old_string": "    stat = {p: {\"groupes\": 0, \"prefere_est_gold\": 0, \"un_gold_dans_groupe\": 0}\n            for p in (\"chunker\", \"s_long\", \"large\")}\n    for ph in phrases:\n        a = h.analyser(ph[\"texte\"], ph[\"langue\"])\n        … [1454 caractères tronqués]`

  ```
The file /tmp/partition_syntagmes/options.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. timeout 1800 python3 /tmp/partition_syntagmes/options.py 2>&1 | tail -30", "description": "Run measured options over gold, bancs, free texts"}`

  ```
base {"f1": 0.6176, "precision": 0.6539, "rappel": 0.5851, "att_exact": 222, "att_labels": 222, "att_couverture": 0.9289, "pos": 0.8383, "fraction": 0.5537} bancs 269 760 libres 67 267 retires 0
alternative {"f1": 0.6176, "precision": 0.6539, "rappel": 0.5851, "att_exact": 222, "att_labels": 222, "att_couverture": 0.9289, "pos": 0.8383, "fraction": 0.5537} bancs 269 760 libres 67 267 retires 0
alternative_chunker {"f1": 0.6176, "precision": 0.6539, "rappel": 0.5851, "att_exact": 222, "att_labels": 222, "att_couverture": 0.9289, "pos": 0.8383, "fraction": 0.5537} bancs 269 760 libres 67 267 retires 0
alternative_large {"f1": 0.6176, "precision": 0.6539, "rappel": 0.5851, "att_exact": 222, "att_labels": 222, "att_couverture": 0.9289, "pos": 0.8383, "fraction": 0.5537} bancs 269 760 libres 67 267 retires 0
filtrer_chunker {"f1": 0.6497, "precision": 0.7371, "rappel": 0.5808, "att_exact": 215, "att_labels": 215, "att_couverture": 0.8996, "pos": 0.8383, "fraction": 0.5537} bancs 91 657 libres 27 243 retires 199
filtrer_contenu {"f1": 0.5373, "precision": 0.6211, "rappel": 0.4734, "att_exact": 208, "att_labels": 208, "att_couverture": 0.8703, "pos": 0.8383, "fraction": 0.5537} bancs 114 
… [869 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\no=json.load(open('/tmp/partition_syntagmes/options.json'))\nfor k in ['base','alternative','filtrer_chunker','filtrer_contenu','dedup']:\n    g=o['gold'][k]\n    print(k,{x:g[x] for x in ('tp','fp','fn' … [293 caractères tronqués]`

  ```
base {'tp': 1090, 'fp': 577, 'fn': 773, 'f1': 0.6176, 'precision': 0.6539, 'rappel': 0.5851, 'att_exact': 222, 'att_labels': 222}
alternative {'tp': 1090, 'fp': 577, 'fn': 773, 'f1': 0.6176, 'precision': 0.6539, 'rappel': 0.5851, 'att_exact': 222, 'att_labels': 222}
filtrer_chunker {'tp': 1082, 'fp': 386, 'fn': 781, 'f1': 0.6497, 'precision': 0.7371, 'rappel': 0.5808, 'att_exact': 215, 'att_labels': 215}
filtrer_contenu {'tp': 882, 'fp': 538, 'fn': 981, 'f1': 0.5373, 'precision': 0.6211, 'rappel': 0.4734, 'att_exact': 208, 'att_labels': 208}
dedup {'tp': 1059, 'fp': 345, 'fn': 804, 'f1': 0.6483, 'precision': 0.7543, 'rappel': 0.5684, 'att_exact': 206, 'att_labels': 206}
baseline {'tp': 1090, 'fp': 574, 'fn': 773, 'f1': 0.6181, 'precision': 0.655, 'rappel': 0.5851}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl, evaluer_gold as eg\np=eg.charger()\nprint(len(p), sum(len(x['mots']) for x in p))\n … [300 caractères tronqués]`

  ```
612 3179
{'tp': 1090, 'fp': 577, 'fn': 773, 'f1': 0.6176, 'precision': 0.6539, 'rappel': 0.5851}
{'tp': 1090, 'fp': 577, 'fn': 773, 'f1': 0.6176}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1985,2075p tools/bloc_linguistique.py && echo '--- parallele init ---' && sed -n 1975,2010p tools/bloc_linguistique.py | head -40", "description": "Inspect Cascade/Parallele init for shared state"}`

  ```
"""Les deux implémentations en parallèle : le contrat est le même, la fusion est explicite."""

    nom = "parallele"

    def __init__(self, blocs: Sequence[BlocLinguistique],
                 priorite_syntagme: str = "heuristique",
                 priorite_par_niveau: dict | None = None,
                 priorite_par_type: dict | None = None):
        if len(blocs) != 2:
            raise ValueError("le parallèle attend exactement deux blocs")
        self.blocs = list(blocs)
        self.priorite_syntagme = priorite_syntagme
        self.priorite_par_niveau = (priorite_par_niveau if priorite_par_niveau is not None
                                     else priorite_par_defaut())
        self.priorite_par_type = dict(priorite_par_type or {})

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation:
        a = self.blocs[0].analyser(texte, langue, contexte)
        b = self.blocs[1].analyser(texte, langue, contexte)
        return _fusion(a, b, self.nom, self.priorite_syntagme, self.priorite_par_niveau,
                       self.priorite_par_type)


class Cascade:
    """L'heuristique d'abord ; le neuronal seulem
… [4688 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -E 'lru_cache|cache|global |subprocess|_S_' tools/bloc_linguistique.py | head -40", "description": "Look for global caches or subprocesses in module"}`

  ```
40:import subprocess
797:    def _verbe_gv(texte: str, g: dict, verbes, cache: dict | None = None):
800:        if cache is not None and cle in cache:
801:            return cache[cle]
803:        if cache is not None:
804:            cache[cle] = v
810:                      cache: dict | None = None) -> str | None:
836:            v = Heuristique._verbe_gv(texte, g, verbes, cache)
840:        return Heuristique._verbe_gv(texte, g, verbes, cache)
845:                        cache: dict | None = None) -> list[str]:
857:            v = Heuristique._verbe_gv(texte, g, verbes, cache)
1152:        cache_gv: dict = {}  # un GV n'est analysé qu'une fois par analyse
1185:                        cible = self._cible_proche(texte, s, gvs, verbes, cache_gv)
1195:                                 or self._cible_proche(texte, s, gvs, verbes, cache_gv))
1202:                        texte, s, gvs, verbes=verbes, cache=cache_gv)
1218:            cache_gv: dict = {}
1224:                         or self._cible_proche(texte, s, gvs_s, verbes, cache_gv))
1234:                                                           texte, s, gvs_s, verbes=verbes, cache=cache_gv)),
1251:                         or sel
… [1222 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'def _syntagmes_s\\|def _syntagmes_simple' tools/bloc_linguistique.py && sed -n 640,700p tools/bloc_linguistique.py", "description": "Read S generator entry points"}`

  ```
648:    def _syntagmes_s(self, texte: str) -> list[dict] | None:
862:    def _syntagmes_simple(self, texte: str, langue: str,
                break
        for pre in PREFIXES:
            if len(n) > len(pre) + 2 and n.startswith(pre):
                sortie.append(("préfixe", 0, len(pre), pre))
                break
        return sortie

    # -- syntagmes ----------------------------------------------------------
    def _syntagmes_s(self, texte: str) -> list[dict] | None:
        if not self.segmenter_s:
            return None
        try:
            if str(RACINE / "tools/structures") not in sys.path:
                sys.path.insert(0, str(RACINE / "tools/structures"))
            import generateur  # le générateur S, importé en lecture seule
            return generateur.analyser(texte)
        except Exception:
            return None

    def _cibles_s(self, texte: str) -> dict:
        """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).

        Lecture seule de l'API interne du S : `_tokens`/`_segmente` rendent les `Segment` avec
        `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
        (GP, puis GN, 
… [1791 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n -E 'cache|_CACHE|lru|global ' tools/structures/generateur.py | head -30 && grep -n 'def analyser' tools/structures/generateur.py", "description": "Check S generator for caches/global state"}`

  ```
516:def analyser(texte: str, max_candidats: int = 4) -> list[dict]:
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short tools/structures/ tools/bloc_linguistique.py tools/tests/linguistique/ && ls -la --time-style=full-iso tools/structures/generateur.py tools/bloc_linguistique.py tools/tests/linguistique/gold.json | cat && date", "d … [61 caractères tronqués]`

  ```
M  tools/bloc_linguistique.py
 m tools/structures
-rw-------. 1 stephane stephane 120781 2026-11-06 18:45:48.848740129 -0500 tools/bloc_linguistique.py
-rw-r--r--. 1 stephane stephane  30580 2026-11-04 11:41:49.129836555 -0500 tools/structures/generateur.py
-rw-r--r--. 1 stephane stephane  20009 2026-11-06 18:17:22.233772666 -0500 tools/tests/linguistique/gold.json
ven 06 nov 2026 18:53:25 EST
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff HEAD -- tools/bloc_linguistique.py | head -80 && echo '--- cached ---' && git diff --cached --stat -- tools/bloc_linguistique.py", "description": "Inspect concurrent staged changes to module"}`

  ```
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index b9598d42..fdde29b5 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -442,6 +442,7 @@ cry cries cried crying go goes went gone going come comes came coming
 leave leaves left leaving read reads reading sleep sleeps slept sleeping
 rain rains rained raining hang hangs hung hanging paint paints painted painting
 live lives lived living continue continues continued continuing
+acheter achète achètes achètent achetait acheté achetée achetés achetées
 fall falls fell fallen falling call calls called calling
 speak speaks spoke spoken speaking voler vole voles volent volait
 rêver rêve rêves rêvent rêvait sauter saute sautes sautent sautait
@@ -892,7 +893,8 @@ class Heuristique:
         while i < len(mots):
             d, f, t, typ = mots[i]
             n = _normaliser(t)
-            if typ == "mot" and (n in RELATIFS or est_sub(n)):
+            _n_elic = n.split("'")[0] if "'" in n else n
+            if typ == "mot" and (n in RELATIFS or _n_elic in RELATIFS or est_sub(n)):
                 suivant = mots[i + 1] if i + 1 < len(mots) else None
                 # « since/before/after/
… [226 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,40p tools/structures/generateur.py && echo '--- imports ---' && grep -n '^import\\|^from' tools/structures/generateur.py", "description": "Check S generator imports and paths"}`

  ```
#!/usr/bin/env python3
"""generateur.py — une phrase brute → des structures candidates (v0 heuristique).

Ce n'est pas un analyseur syntaxique : c'est un **générateur de candidats** à faire valider par
un humain. Il segmente (GN, GV, GP, REL, SUB), devine des rôles par la préposition, puis produit
plusieurs candidats en variant l'**attachement** de chaque segment ambigu (GN le plus proche ou
GV le plus proche).

    python3 generateur.py "Le chat de la voisine qui dort sur le toit se réveille."
    python3 generateur.py --json "..."     # la structure complète
"""
from __future__ import annotations

import json
import re
import unicodedata

DET = set("le la les l un une ce cet cette ces mon ma mes ton ta tes son sa ses "
          "notre nos votre vos leur leurs quel quelle quels quelles".split())
PREP = set("a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis "
           "pendant durant contre malgre selon pres loin devant derriere apres avant".split())
RELATIFS = set("qui que qu dont ou quoi".split())
CONJ = set("et ou mais donc or ni car quand comme si parce puisque lorsque pendant quoique".split())
COORD = set("et ou mais donc or ni car".split())
SU
… [1365 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git rev-parse HEAD && git show HEAD:tools/bloc_linguistique.py | sha256sum && sha256sum tools/bloc_linguistique.py tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json tools/tests/linguistique/gold_synthetique.j … [54 caractères tronqués]`

  ```
e6fad714b3339bb6c1a4e4592c4d07af14dff6fc
c4d8f09b6038fb26829517d62b9ea421dff43452bea2e20fc944a5dcff0544dd  -
c4d8f09b6038fb26829517d62b9ea421dff43452bea2e20fc944a5dcff0544dd  tools/bloc_linguistique.py
3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a  tools/tests/linguistique/gold.json
05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11  tools/tests/linguistique/gold_reel.json
e3e704ce9cb599db07ab31d1b0651f0aa12ea9ecad31ca8bf558efdeed84a654  tools/tests/linguistique/gold_synthetique.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git ls-tree HEAD tools/structures && git ls-tree fa1b0c6e tools/structures && git ls-files -s tools/structures/generateur.py | cat && git log --oneline -3 -- tools/structures && echo '--- audit commit files ---' && git ls-tree -r --n … [114 caractères tronqués]`

  ```
160000 commit 523d8c1e8c6ca29ca415360a71bfab6c5b56102c	tools/structures
160000 commit 523d8c1e8c6ca29ca415360a71bfab6c5b56102c	tools/structures
8189c4f3 S — LE FAIT DIVERS EST TRANCHÉ : 61/61 TYPES, 144/144 RÔLES ; LA TÊTE DU GN ARRÊTE LE VERBE
4449646d B13 — LE DÉFAUT DE LA FUSION : LA CONFIANCE (0,7424) BAT LE NIVEAU (0,3432) ; 141/141
047945c5 S — LA BANQUE DE PARAGRAPHES PASSE À NEUF : SIX PAIRES D'ALICE, SOURCES ANGLAISES ET RÉFÉRENTS
--- audit commit files ---
tools/tests/linguistique/anaphore.py
tools/tests/linguistique/classement_cible.py
tools/tests/linguistique/evaluer_gold.py
tools/tests/linguistique/gold.json
tools/tests/linguistique/gold.py
tools/tests/linguistique/gold_gele.json
tools/tests/linguistique/gold_reel.json
tools/tests/linguistique/gold_reel.py
tools/tests/linguistique/gold_split.py
tools/tests/linguistique/gold_synthetique.json
  ```

### 🤖 Assistant

⏵ Pinning the audit commit in /tmp because the shared repo is moving under concurrent agents

- **bash** `{"command": "set -e\nR=/home/stephane/Data13TB/stephane/GitHub/Qtrinet\nP=/tmp/pin_audit\nrm -rf \"$P\"; mkdir -p \"$P/tools/structures\" \"$P/tools/tests/linguistique\"\ncd \"$R\"\ngit show fa1b0c6e:tools/bloc_linguistique.py > \"$P/tools/bloc_linguistique.py\"\ngit show fa1b0c6e:tools/tests/lingui … [641 caractères tronqués]`

  ```
5954d0870bb957472662047ba40d027ea8f64e9434ecb24217faa9337437b08f  /tmp/pin_audit/tools/bloc_linguistique.py
291df65a43693aac4cdd3fb7fd25955b5eb7f103e24e57d8c505e31d765202d5  /tmp/pin_audit/tools/structures/generateur.py
f2632969fbe38f67320deae3dc0052b607ffd79fcbeec29cb55d08dbb34105f1  /tmp/pin_audit/tools/tests/linguistique/gold_gele.json
3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a  /tmp/pin_audit/tools/tests/linguistique/gold.json
05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11  /tmp/pin_audit/tools/tests/linguistique/gold_reel.json
e3e704ce9cb599db07ab31d1b0651f0aa12ea9ecad31ca8bf558efdeed84a654  /tmp/pin_audit/tools/tests/linguistique/gold_synthetique.json
  2192 /tmp/pin_audit/tools/bloc_linguistique.py
   648 /tmp/pin_audit/tools/structures/generateur.py
  2840 total
  ```

- **bash** `{"command": "cd /tmp/partition_syntagmes && python3 - <<'PY'\nimport re\np='inventaire.py'\ns=open(p).read()\ns=s.replace('RACINE = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\\nsys.path.insert(0, RACINE + \"/tools\")',\n            'import os\\nRACINE = os.environ.get(\"PIN\", \"/home/steph … [1751 caractères tronqués]`

  ```
ok
13:RACINE = os.environ.get("PIN", "/home/stephane/Data13TB/stephane/GitHub/Qtrinet")
14:DEPOT = "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"
15:sys.path.insert(0, RACINE + "/tools")
71:        ("fiabilite", DEPOT + "/reports/pensee-fiabilite-produit.json", "resultats",
73:        ("bloc_l", DEPOT + "/reports/pensee-produit-bloc-l.json", "detail",
20:RACINE = os.environ.get("PIN", "/home/stephane/Data13TB/stephane/GitHub/Qtrinet")
21:DEPOT = "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"
22:sys.path.insert(0, RACINE + "/tools")
23:sys.path.insert(0, RACINE + "/tools/tests/linguistique")
243:    a = json.load(open(DEPOT + "/reports/pensee-fiabilite-produit.json", encoding="utf-8"))
244:    b = json.load(open(DEPOT + "/reports/pensee-produit-bloc-l.json", encoding="utf-8"))
257:    brut = open(DEPOT + "/data/corpus_fr_litterature.txt", encoding="utf-8",
  ```

- **bash** `{"command": "cd /tmp/pin_audit && PIN=/tmp/pin_audit OUT=/tmp/partition_syntagmes/inventaire_audit.json timeout 900 python3 /tmp/partition_syntagmes/inventaire.py 2>&1 | tail -15", "description": "Run inventory on pinned audit commit"}`

  ```
fiabilite {"textes": 46, "textes_avec_chevauchement": 23, "paires": 107, "syntagmes": 360, "union": 85, "attaches": 284, "classes": {"union_contenu": 60, "inclusion_s_dans_union": 37, "croisement": 7, "meme_span_union": 3}}
  ex inclusion_s_dans_union f02 'qui dort sur le toit' | 'qui dort sur le toit se réveille' {'type': 'REL', 'debut': 22, 'fin': 42, 'union': False, 'att': True} {'type': 'REL', 'debut': 22, 'fin': 54, 'union': True, 'att': True}
  ex croisement f06 'Je ne pense pas' | "ne pense pas qu'il viendra demain" {'type': 'GV', 'debut': 0, 'fin': 15, 'union': False, 'att': False} {'type': 'GV', 'debut': 3, 'fin': 36, 'union': True, 'att': False}
  ex union_contenu f06 'nous verrons bien' | 'verrons bien' {'type': 'GV', 'debut': 43, 'fin': 60, 'union': False, 'att': False} {'type': 'GV', 'debut': 48, 'fin': 60, 'union': True, 'att': False}
  ex meme_span_union f50 "où il passe l'après-midi" | "où il passe l'après-midi" {'type': 'REL', 'debut': 209, 'fin': 233, 'union': False, 'att': True} {'type': 'SUB', 'debut': 209, 'fin': 233, 'union': True, 'att': True}
bloc_l {"textes": 50, "textes_avec_chevauchement": 31, "paires": 132, "syntagmes": 362, "union": 98, "attaches": 265,
… [1034 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/pin_audit && PIN=/tmp/pin_audit OUT=/tmp/partition_syntagmes/options_audit.json timeout 1800 python3 /tmp/partition_syntagmes/options.py 2>&1 | tail -30", "description": "Run options measured at pinned audit commit"}`

  ```
base {"f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "att_exact": 222, "att_labels": 222, "att_couverture": 0.9289, "pos": 0.7581, "fraction": 0.5537} bancs 239 722 libres 59 233 retires 0
alternative {"f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "att_exact": 222, "att_labels": 222, "att_couverture": 0.9289, "pos": 0.7581, "fraction": 0.5537} bancs 239 722 libres 59 233 retires 0
alternative_chunker {"f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "att_exact": 222, "att_labels": 222, "att_couverture": 0.9289, "pos": 0.7581, "fraction": 0.5537} bancs 239 722 libres 59 233 retires 0
alternative_large {"f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "att_exact": 222, "att_labels": 222, "att_couverture": 0.9289, "pos": 0.7581, "fraction": 0.5537} bancs 239 722 libres 59 233 retires 0
filtrer_chunker {"f1": 0.6163, "precision": 0.7122, "rappel": 0.5432, "att_exact": 217, "att_labels": 217, "att_couverture": 0.9079, "pos": 0.7581, "fraction": 0.5537} bancs 91 636 libres 29 214 retires 197
filtrer_contenu {"f1": 0.5006, "precision": 0.5899, "rappel": 0.4348, "att_exact": 208, "att_labels": 208, "att_couverture": 0.8703, "pos": 0.7581, "fraction": 0.5537} bancs 112 
… [870 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/partition_syntagmes && python3 - <<'PY'\nimport json\no=json.load(open('options_audit.json'))\nfor v in ['base','filtrer_chunker','filtrer_contenu','union_any','widest','dedup']:\n    b=o['bancs'][v]\n    print(f\"{v:18} paires={b['paires']:3} segments={b['segments']:3} union={b … [741 caractères tronqués]`

  ```
base               paires=239 segments=722 union=183 att=549 textes_chev=54 classes={'inclusion_s_dans_union': 127, 'union_contenu': 80, 'croisement': 26, 'meme_span_union': 6}
   par banc {'fiabilite': {'paires': 107, 'textes': 23, 'segments': 360}, 'bloc_l': {'paires': 132, 'textes': 31, 'segments': 362}}
filtrer_chunker    paires= 91 segments=636 union=183 att=481 textes_chev=33 classes={'union_contenu': 80, 'meme_span_union': 6, 'croisement': 5}
   par banc {'fiabilite': {'paires': 42, 'textes': 11, 'segments': 316}, 'bloc_l': {'paires': 49, 'textes': 22, 'segments': 320}}
filtrer_contenu    paires=112 segments=595 union= 56 att=484 textes_chev=35 classes={'union_contenu': 80, 'croisement': 26, 'meme_span_union': 6}
   par banc {'fiabilite': {'paires': 47, 'textes': 11, 'segments': 300}, 'bloc_l': {'paires': 65, 'textes': 24, 'segments': 295}}
union_any          paires=  3 segments=543 union=  4 att=447 textes_chev= 2 classes={'croisement': 3}
   par banc {'fiabilite': {'paires': 0, 'textes': 0, 'segments': 276}, 'bloc_l': {'paires': 3, 'textes': 2, 'segments': 267}}
widest             paires= 32 segments=515 union= 56 att=409 textes_chev=24 classes={'croisement': 26, 'meme_spa
… [2231 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/partition_syntagmes && python3 - <<'PY'\np='options.py'\ns=open(p).read()\n# corriger l'inversion petit/grand\ns=s.replace('petit, grand = (x, y) if rel == \"inclut\" else (y, x)',\n            'petit, grand = (y, x) if rel == \"inclut\" else (x, y)')\n# ajouter les variantes \" … [2117 caractères tronqués]`

  ```
patched
206:def garder_chunker(a: bl.Annotation, portee: tuple[str, ...]) -> int:
255:        elif self.mode.startswith("garder_chunker"):
256:            portee = {"garder_chunker_c1": ("inclus",),
257:                      "garder_chunker_c1c2": ("inclus", "inclut"),
258:                      "garder_chunker_c1c2c3": ("inclus", "inclut", "meme_span"),
259:                      "garder_chunker": ("inclus", "inclut", "meme_span", "croise")}[self.mode]
260:            self.stats["retires"] += garder_chunker(a, portee)
367:        ("garder_chunker_c1", "garder_chunker_c1", "s_long"),
368:        ("garder_chunker_c1c2", "garder_chunker_c1c2", "s_long"),
369:        ("garder_chunker_c1c2c3", "garder_chunker_c1c2c3", "s_long"),
  ```

- **bash** `{"command": "cd /tmp/pin_audit && PIN=/tmp/pin_audit OUT=/tmp/partition_syntagmes/options_audit2.json timeout 1800 python3 /tmp/partition_syntagmes/options.py 2>&1 | tail -20", "description": "Measure progressive chunker-preserving filters"}`

  ```
base {"f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "att_exact": 222, "att_labels": 222, "att_couverture": 0.9289, "pos": 0.7581, "fraction": 0.5537} bancs 239 722 libres 59 233 retires 0
alternative {"f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "att_exact": 222, "att_labels": 222, "att_couverture": 0.9289, "pos": 0.7581, "fraction": 0.5537} bancs 239 722 libres 59 233 retires 0
alternative_chunker {"f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "att_exact": 222, "att_labels": 222, "att_couverture": 0.9289, "pos": 0.7581, "fraction": 0.5537} bancs 239 722 libres 59 233 retires 0
alternative_large {"f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "att_exact": 222, "att_labels": 222, "att_couverture": 0.9289, "pos": 0.7581, "fraction": 0.5537} bancs 239 722 libres 59 233 retires 0
filtrer_chunker {"f1": 0.6163, "precision": 0.7122, "rappel": 0.5432, "att_exact": 217, "att_labels": 217, "att_couverture": 0.9079, "pos": 0.7581, "fraction": 0.5537} bancs 91 636 libres 29 214 retires 197
filtrer_contenu {"f1": 0.5006, "precision": 0.5899, "rappel": 0.4348, "att_exact": 208, "att_labels": 208, "att_couverture": 0.8703, "pos": 0.7581, "fraction": 0.5537} bancs 112 
… [1704 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/partition_syntagmes && python3 - <<'PY'\np='options.py'\ns=open(p).read()\ns=s.replace('''def dedup(a: bl.Annotation) -> int:''', '''def _classe_paire(union: bl.Etiquette, s: bl.Etiquette) -> str:\n    rel = _relation(union, s)\n    return {\"inclus\": \"C1_union_dans_s\", \"inc … [5502 caractères tronqués]`

  ```
patched
  ```

- **bash** `{"command": "cd /tmp/pin_audit && PIN=/tmp/pin_audit OUT=/tmp/partition_syntagmes/options_audit3.json timeout 2400 python3 /tmp/partition_syntagmes/options.py 2>&1 | tail -22", "description": "Measure per-class partition rules"}`

  ```
alternative {"f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "att_exact": 222, "att_labels": 222, "att_couverture": 0.9289, "pos": 0.7581, "fraction": 0.5537} bancs 239 722 libres 59 233 retires 0
alternative_chunker {"f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "att_exact": 222, "att_labels": 222, "att_couverture": 0.9289, "pos": 0.7581, "fraction": 0.5537} bancs 239 722 libres 59 233 retires 0
alternative_large {"f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "att_exact": 222, "att_labels": 222, "att_couverture": 0.9289, "pos": 0.7581, "fraction": 0.5537} bancs 239 722 libres 59 233 retires 0
filtrer_chunker {"f1": 0.6163, "precision": 0.7122, "rappel": 0.5432, "att_exact": 217, "att_labels": 217, "att_couverture": 0.9079, "pos": 0.7581, "fraction": 0.5537} bancs 91 636 libres 29 214 retires 197
filtrer_contenu {"f1": 0.5006, "precision": 0.5899, "rappel": 0.4348, "att_exact": 208, "att_labels": 208, "att_couverture": 0.8703, "pos": 0.7581, "fraction": 0.5537} bancs 112 595 libres 35 209 retires 245
union_any {"f1": 0.4959, "precision": 0.6003, "rappel": 0.4224, "att_exact": 199, "att_labels": 199, "att_couverture": 0.8326, "pos": 0.7581, "fraction": 0.5537} ban
… [3334 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/partition_syntagmes && python3 - <<'PY'\nimport json\no=json.load(open('options_audit3.json'))\nfor v in ['base','filtrer_chunker','garder_chunker_c1c2','garder_chunker_c1c2c3','garder_chunker','regle_mix_A','regle_mix_E','glouton_att_union','dedup']:\n    b=o['bancs'][v]\n    p … [646 caractères tronqués]`

  ```
base                   paires=239 seg=722 union=183 att=549 textes=54 classes={'union_contenu': 127, 'inclusion_s_dans_union': 80, 'croisement': 26, 'meme_span_union': 6}
                       libres paires=59 seg=233 textes=10 classes={'union_contenu': 24, 'inclusion_s_dans_union': 24, 'croisement': 8, 'meme_span_union': 3}
filtrer_chunker        paires= 91 seg=636 union=183 att=481 textes=33 classes={'inclusion_s_dans_union': 80, 'meme_span_union': 6, 'croisement': 5}
                       libres paires=29 seg=214 textes= 7 classes={'inclusion_s_dans_union': 24, 'meme_span_union': 3, 'croisement': 2}
garder_chunker_c1c2    paires= 11 seg=556 union=183 att=406 textes= 9 classes={'meme_span_union': 6, 'croisement': 5}
                       libres paires= 5 seg=190 textes= 3 classes={'meme_span_union': 3, 'croisement': 2}
garder_chunker_c1c2c3  paires=  5 seg=550 union=183 att=400 textes= 5 classes={'croisement': 5}
                       libres paires= 2 seg=187 textes= 2 classes={'croisement': 2}
garder_chunker         paires=  0 seg=545 union=183 att=397 textes= 0 classes={}
                       libres paires= 0 seg=185 textes= 0 classes={}
regle_mix_A            paires=  0 
… [2722 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Writing the proposed patch on a pinned copy and validating it end-to-end

- **write** `{"content": "\"\"\"Construit une copie patchée du module épinglé (aucune modification du dépôt).\"\"\"\nfrom __future__ import annotations\n\nimport pathlib\n\nSRC = pathlib.Path(\"/tmp/pin_audit/tools/bloc_linguistique.py\")\nDST = pathlib.Path(\"/tmp/pin_audit/tools/bloc_partition.py\")\ns = SRC.r … [6811 caractères tronqués]`

  ```
<path>/tmp/partition_syntagmes/construire_patch.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/pin_audit && python3 /tmp/partition_syntagmes/construire_patch.py && python3 -c \"\nimport sys; sys.path.insert(0,'/tmp/pin_audit/tools')\nimport bloc_partition as bp\nh=bp.Heuristique()\na=h.analyser('Le chat de la voisine qui dort sur le toit se réveille.', 'fr')\nprint(len(a. … [186 caractères tronqués]`

  ```
écrit /tmp/pin_audit/tools/bloc_partition.py 2298 lignes
59 
GN 0 7 'Le chat' {'role': 'agent', 'niveau': 1, 'attachement': {'segment': 'Le chat', 'cible': 'réveille'}}
GP 8 21 'de la voisine' {'role': 'possession', 'niveau': 2, 'attachement': {'segment': 'de la voisine', 'cible': 'réveille'}}
REL 22 42 'qui dort sur le toit' {'role': 'qualite', 'niveau': 2, 'attachement': {'segment': 'qui dort sur le toit', 'cible': 'voisine'}, 'partition': {'groupe': 0, 'rang': 3, 'membres': 3, 'vue': 'alternative'}, 'alternative': [{'type': 'REL', 'debut': 22, 'fin': 54, 'source': 'heuristique', 'union': True, 'relation': 'inclus', 'rang': 1, 'attachement': {'segment': 'qui dort sur le toit se réveille', 'cible': 'réveille'}, 'role': 'qualité'}, {'type': 'GV', 'debut': 43, 'fin': 54, 'source': 'heuristique', 'union': False, 'relation': 'croise', 'rang': 2, 'attachement': {'segment': 'se réveille', 'cible': 'voisine'}, 'role': 'predicat'}]}
REL 22 54 'qui dort sur le toit se réveille' {'role': 'qualité', 'niveau': 1, 'union': True, 'attachement': {'segment': 'qui dort sur le toit se réveille', 'cible': 'réveille'}, 'partition': {'groupe': 0, 'rang': 1, 'membres': 3, 'vue': 'alternative'}, 'altern
… [1048 caractères tronqués]
  ```

- **write** `{"content": "\"\"\"Évalue le patch proposé sur la copie épinglée (aucune modification du dépôt).\"\"\"\nfrom __future__ import annotations\n\nimport copy\nimport hashlib\nimport json\nimport random\nimport sys\nfrom collections import Counter, defaultdict\n\nRACINE = \"/tmp/pin_audit\"\nDEPOT = \"/h … [12218 caractères tronqués]`

  ```
<path>/tmp/partition_syntagmes/patch_eval.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/pin_audit && timeout 2400 python3 /tmp/partition_syntagmes/patch_eval.py 2>&1 | tail -80", "description": "Evaluate proposed patch, payload, controls"}`

  ```
brut {"f1": 0.5849, "att_exact": 222, "att_cibles": 239, "pos": 0.7581} bancs 239 libres 59 octets 1928458 vues 0
alternative {"f1": 0.5849, "att_exact": 222, "att_cibles": 239, "pos": 0.7581} bancs 239 libres 59 octets 2129150 vues 894
filtrer {"f1": 0.5953, "att_exact": 189, "att_cibles": 239, "pos": 0.7581} bancs 0 libres 0 octets 1894470 vues 239
preference {'groupes': 244, 'rang1_gold': 177, 'un_gold': 207, 'groupes_sans_gold': 37}
pos {'brut': 'cb4757217465da39', 'alternative': 'cb4757217465da39', 'filtrer': 'cb4757217465da39'} det True
EXEMPLE BRUT
  GN  [0:28] 'La voisine arrose les fleurs' -> partir
  GP  [29:51] 'du jardin chaque matin' -> partir
  GP  [29:60] 'du jardin chaque matin avant de' -> fleurs
  GP  [58:67] 'de partir' -> au
  GV  [61:67] 'partir' -> —
  GP  [68:78] 'au travail' -> partir
  GV  [68:78] 'au travail' -> —
  GV  [80:96] 'puis elle rentre' -> travail
  GV  [90:96] 'rentre' -> —
  GP  [97:117] 'vers dix-huit heures' -> rentre
  GP  [97:159] 'vers dix-huit heures et prépare le dîner pour ses deux enfants' -> rentre
  GV  [121:128] 'prépare' -> heures
  GN  [129:137] 'le dîner' -> heures
  GP  [138:159] 'pour ses deux enfants' -> prépare
EXEMPLE ALTERN
… [3986 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/pin_audit && python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'/tmp/pin_audit/tools')\nimport bloc_partition as bp\nt=json.load(open('/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-produit-bloc-l.json'))['banc_50']['detail'][1]['texte']\nprint(t)\na=bp.Heuri … [289 caractères tronqués]`

  ```
La voisine arrose les fleurs du jardin chaque matin avant de partir au travail, puis elle rentre vers dix-huit heures et prépare le dîner pour ses deux enfants.
GN 0 28 'La voisine arrose les fleurs' union= None att= True
GP 29 51 'du jardin chaque matin' union= None att= True
GP 29 60 'du jardin chaque matin avant de' union= True att= True
GP 58 67 'de partir' union= None att= True
GV 61 67 'partir' union= True att= False
GP 68 78 'au travail' union= None att= True
GV 68 78 'au travail' union= True att= False
GV 80 96 'puis elle rentre' union= None att= True
GV 90 96 'rentre' union= True att= False
GP 97 117 'vers dix-huit heures' union= None att= True
GP 97 159 'vers dix-huit heures et prépare le dîner pour ses deux enfants' union= True att= True
GV 121 128 'prépare' union= None att= True
GN 129 137 'le dîner' union= None att= True
GP 138 159 'pour ses deux enfants' union= None att= True
  ```

- **bash** `{"command": "cd /tmp/pin_audit && python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'/tmp/pin_audit/tools')\nimport bloc_partition as bp\nt=json.load(open('/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-produit-bloc-l.json'))['banc_50']['detail'][1]['texte']\na=bp.Heuristique(par … [914 caractères tronqués]`

  ```
base 9
rest 6 paires 0
  ```

- **bash** `{"command": "cd /tmp/partition_syntagmes && python3 - <<'PY'\np='construire_patch.py'\ns=open(p).read()\nold = '''    for gid, groupe in enumerate(groupes):\n        ordre = sorted(groupe, key=_cle_preferee)\n        rangs = {id(e): i + 1 for i, e in enumerate(ordre)}\n        pref = ordre[0]\n      … [2870 caractères tronqués]`

  ```
ok
  ```

- **write** `{"content": "\"\"\"Construit une copie patchée du module épinglé (aucune modification du dépôt).\"\"\"\nfrom __future__ import annotations\n\nimport pathlib\n\nSRC = pathlib.Path(\"/tmp/pin_audit/tools/bloc_linguistique.py\")\nDST = pathlib.Path(\"/tmp/pin_audit/tools/bloc_partition.py\")\ns = SRC.r … [7991 caractères tronqués]`

  ```
Error: cannot write "/tmp/partition_syntagmes/construire_patch.py": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/tmp/partition_syntagmes/construire_patch.py", "limit": 20}`

  ```
<path>/tmp/partition_syntagmes/construire_patch.py</path>
<type>file</type>
<content>
1: """Construit une copie patchée du module épinglé (aucune modification du dépôt)."""
2: from __future__ import annotations
3: 
4: import pathlib
5: 
6: SRC = pathlib.Path("/tmp/pin_audit/tools/bloc_linguistique.py")
7: DST = pathlib.Path("/tmp/pin_audit/tools/bloc_partition.py")
8: s = SRC.read_text(encoding="utf-8")
9: 
10: # 1. le paramètre de politique, dans __init__
11: old = '''    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
12:                  seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
13:                  union: bool = True):
14:         self.profils = profils
15:         self.segmenter_s = segmenter_s
16:         self.seuil_ouvert = seuil_ouvert
17:         self.seuil_langue = seuil_langue
18:         self.union = union
19: '''
20: new = '''    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,

(Showing lines 1-20 of 186. Use offset=21 to continue.)
</content>
  ```

- **write** `{"content": "\"\"\"Construit une copie patchée du module épinglé (aucune modification du dépôt).\"\"\"\nfrom __future__ import annotations\n\nimport pathlib\n\nSRC = pathlib.Path(\"/tmp/pin_audit/tools/bloc_linguistique.py\")\nDST = pathlib.Path(\"/tmp/pin_audit/tools/bloc_partition.py\")\ns = SRC.r … [7991 caractères tronqués]`

  ```
<path>/tmp/partition_syntagmes/construire_patch.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "cd /tmp/pin_audit && python3 /tmp/partition_syntagmes/construire_patch.py && timeout 2400 python3 /tmp/partition_syntagmes/patch_eval.py 2>&1 | tail -60", "description": "Rebuild patch and re-evaluate"}`

  ```
écrit /tmp/pin_audit/tools/bloc_partition.py 2317 lignes
brut {"f1": 0.5849, "att_exact": 222, "att_cibles": 239, "pos": 0.7581} bancs 239 libres 59 octets 1928458 vues 0
alternative {"f1": 0.5849, "att_exact": 222, "att_cibles": 239, "pos": 0.7581} bancs 239 libres 59 octets 2129150 vues 894
filtrer {"f1": 0.6172, "att_exact": 205, "att_cibles": 239, "pos": 0.7581} bancs 0 libres 0 octets 1967190 vues 466
preference {'groupes': 244, 'rang1_gold': 177, 'un_gold': 207, 'groupes_sans_gold': 37}
pos {'brut': 'cb4757217465da39', 'alternative': 'cb4757217465da39', 'filtrer': 'cb4757217465da39'} det True
EXEMPLE BRUT
  GN  [0:28] 'La voisine arrose les fleurs' -> partir
  GP  [29:51] 'du jardin chaque matin' -> partir
  GP  [29:60] 'du jardin chaque matin avant de' -> fleurs
  GP  [58:67] 'de partir' -> au
  GV  [61:67] 'partir' -> —
  GP  [68:78] 'au travail' -> partir
  GV  [68:78] 'au travail' -> —
  GV  [80:96] 'puis elle rentre' -> travail
  GV  [90:96] 'rentre' -> —
  GP  [97:117] 'vers dix-huit heures' -> rentre
  GP  [97:159] 'vers dix-huit heures et prépare le dîner pour ses deux enfants' -> rentre
  GV  [121:128] 'prépare' -> heures
  GN  [129:137] 'le dîner' -> heures
  GP  [1
… [4194 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/pin_audit && python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'/tmp/pin_audit/tools'); sys.path.insert(0,'/tmp/pin_audit/tools/tests/linguistique')\nimport bloc_partition as bp, evaluer_gold as eg\nfrom collections import Counter\nph=eg.charger()\nh=bp.Heuristique(partition … [2333 caractères tronqués]`

  ```
tailles Counter({2: 148, 3: 75, 4: 19, 5: 2}) multi_union 60
union_court {'n': 207, 'gold': 0, 'rang1': 177, 'au_moins_un_gold_dans_gardes': 181}
union_long {'n': 207, 'gold': 0, 'rang1': 179, 'au_moins_un_gold_dans_gardes': 181}
union_att {'n': 207, 'gold': 0, 'rang1': 178, 'au_moins_un_gold_dans_gardes': 181}
court {'n': 207, 'gold': 0, 'rang1': 169, 'au_moins_un_gold_dans_gardes': 181}
long {'n': 207, 'gold': 0, 'rang1': 19, 'au_moins_un_gold_dans_gardes': 181}
att_court {'n': 207, 'gold': 0, 'rang1': 137, 'au_moins_un_gold_dans_gardes': 181}
  ```

- **bash** `{"command": "cd /tmp/pin_audit/tools && diff -u --label a/tools/bloc_linguistique.py --label b/tools/bloc_linguistique.py bloc_linguistique.py bloc_partition.py > /tmp/partition_syntagmes/patch.diff; wc -l /tmp/partition_syntagmes/patch.diff; sed -n 1,220p /tmp/partition_syntagmes/patch.diff", "desc … [58 caractères tronqués]`

  ```
155 /tmp/partition_syntagmes/patch.diff
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -529,12 +529,18 @@
 
     def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
                  seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
-                 union: bool = True):
+                 union: bool = True, partition: str = "alternative"):
         self.profils = profils
         self.segmenter_s = segmenter_s
         self.seuil_ouvert = seuil_ouvert
         self.seuil_langue = seuil_langue
         self.union = union
+        # "brut" : la sortie d'avant (chevauchements non documentés) ; "alternative" :
+        # les deux segments restent, `meta.alternative` dit lequel est préféré ; "filtrer" :
+        # une seule vue par groupe, l'autre est conservée dans `meta.alternative` (`retire`).
+        if partition not in ("brut", "alternative", "filtrer"):
+            raise ValueError("partition attend 'brut', 'alternative' ou 'filtrer'")
+        self.partition = partition
 
     # -- langues / script ---------------------------------------------------
     def _langue(self, texte: str, indice: str | None) -> tuple[str,
… [6418 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/partition_syntagmes && python3 - <<'PY'\np='construire_patch.py'\ns=open(p).read()\ns=s.replace('''    \"\"\"La vue préférée : le segment du chunker (union), puis le plus court, puis le plus sûr.\n\n    Mesuré sur le gold 612 : le chunker est le span du gold dans 177/244 groupes … [999 caractères tronqués]`

  ```
ok
écrit /tmp/pin_audit/tools/bloc_partition.py 2318 lignes
brut {"f1": 0.5849, "att_exact": 222, "att_cibles": 239, "pos": 0.7581} bancs 239 libres 59 octets 1928458 vues 0
alternative {"f1": 0.5849, "att_exact": 222, "att_cibles": 239, "pos": 0.7581} bancs 239 libres 59 octets 2129150 vues 894
filtrer {"f1": 0.6172, "att_exact": 205, "att_cibles": 239, "pos": 0.7581} bancs 0 libres 0 octets 1967190 vues 466
preference {'groupes': 244, 'rang1_gold': 179, 'un_gold': 207, 'groupes_sans_gold': 37}
pos {'brut': 'cb4757217465da39', 'alternative': 'cb4757217465da39', 'filtrer': 'cb4757217465da39'} det True
EXEMPLE BRUT
  GN  [0:28] 'La voisine arrose les fleurs' -> partir
  GP  [29:51] 'du jardin chaque matin' -> partir
  GP  [29:60] 'du jardin chaque matin avant de' -> fleurs
  GP  [58:67] 'de partir' -> au
  GV  [61:67] 'partir' -> —
  GP  [68:78] 'au travail' -> partir
  GV  [68:78] 'au travail' -> —
  GV  [80:96] 'puis elle rentre' -> travail
  GV  [90:96] 'rentre' -> —
  GP  [97:117] 'vers dix-huit heures' -> rentre
  GP  [97:159] 'vers dix-huit heures et prépare le dîner pour ses deux enfants' -> rentre
  GV  [121:128] 'prépare' -> heures
  GN  [129:137] 'le dîner' -> heures
  GP 
… [45 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 88,160p tools/drave.py && sed -n 335,355p tools/drave.py", "description": "Read formatter and CLI argument block for patch"}`

  ```
super().__init__(prog, **kwargs)


def formater_annotation(a: bl.Annotation) -> str:
    """La sortie lisible : POS compact, syntagmes (rôle + cible), pragmatique, couverture."""
    lignes = [f"{NOM} {VERSION} — analyse heuristique (CPU, hors ligne)"]
    lignes.append(
        f"langue={a.langue} script={a.script} source={a.source} · {len(a.etiquettes)} étiquettes "
        f"· unités sémantiques={len(a.unites_semantiques)} ({a.fraction_semantique:.1%} du texte)"
    )

    pos = [e for e in a.etiquettes if e.niveau == "pos"]
    if pos:
        lignes.extend(_envelopper("POS  ", " ".join(f"{e.valeur}/{e.type}" for e in pos)))
    else:
        lignes.append("POS  —")

    syntagmes = [e for e in a.etiquettes if e.niveau == "syntagme"]
    if syntagmes:
        valeurs = [_valeur_affichee(e.valeur, 46) for e in syntagmes]
        roles = [str(e.meta.get("role") or "—") for e in syntagmes]
        cibles = [str((e.meta.get("attachement") or {}).get("cible") or "—") for e in syntagmes]
        spans = [f"[{e.debut}:{e.fin}]" for e in syntagmes]
        lt = max(3, max(len(e.type) for e in syntagmes))
        lsp = max(len(s) for s in spans)
        lv = max(len(v) for v in valeurs)
… [3098 caractères tronqués]
  ```

- **write** `{"content": "\"\"\"Statistiques de lisibilité et contrôles complémentaires (copie épinglée).\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom collections import Counter, defaultdict\n\nRACINE = \"/tmp/pin_audit\"\nDEPOT = \"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\ … [4703 caractères tronqués]`

  ```
<path>/tmp/partition_syntagmes/stats_finales.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/pin_audit && timeout 1200 python3 /tmp/partition_syntagmes/stats_finales.py 2>&1 | tail -20", "description": "Compute readability stats and controls"}`

  ```
Traceback (most recent call last):
  File "/tmp/partition_syntagmes/stats_finales.py", line 94, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/tmp/partition_syntagmes/stats_finales.py", line 41, in main
    "ligne_max": max(longues + [0]), "ligne_mediane": sorted(longues)[len(longues) // 2],
                                                      ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
IndexError: list index out of range
  ```

- **bash** `{"command": "cd /tmp/partition_syntagmes && python3 - <<'PY'\np='stats_finales.py'\ns=open(p).read()\ns=s.replace('            longues = [len(l) for l in txt.splitlines()]',\n            '            longues = [len(l) for l in txt.splitlines()] or [0]')\nopen(p,'w').write(s)\nPY\ncd /tmp/pin_audit & … [136 caractères tronqués]`

  ```
{"brut": {"max": 132, "mediane": 38, "p95": 67, "lignes_sup_100": 7}, "alternative": {"max": 251, "mediane": 60, "p95": 171, "lignes_sup_100": 288}, "filtrer": {"max": 237, "mediane": 42, "p95": 178, "lignes_sup_100": 152}}
{"brut": 6, "alternative": 6, "filtrer": 6}
{"brut": {"0": 121}, "alternative": {"0": 57, "1": 31, "2": 19, "3": 8, "4": 2, "6": 2, "32": 1, "8": 1}, "filtrer": {"0": 57, "1": 31, "2": 19, "3": 8, "4": 2, "6": 2, "32": 1, "8": 1}}
{"chunker_seul": {"paires": 0, "segments": 611}, "s_sans_union": {"paires": 0, "segments": 725}}
{"s_dans_union:GP/GP": 45, "union_contenu:GV/GV": 42, "union_contenu:GP/GP": 15, "union_contenu:GN/GN": 13, "s_dans_union:GV/GV": 10, "s_dans_union:REL/REL": 9, "union_contenu:REL/REL": 9, "union_contenu:REL/GP": 9, "s_dans_union:GV/GP": 8, "union_contenu:REL/GV": 8, "union_contenu:SUB/GV": 8, "union_contenu:GN/GV": 7, "union_contenu:GP/GV": 7, "s_dans_union:GN/GN": 7, "s_dans_union:GP/GN": 6, "croisement:GV/GV": 6, "meme_span:GP/GV": 6, "union_contenu:REL/GN": 5, "union_contenu:SUB/GP": 5, "union_contenu:GV/GN": 4, "croisement:GP/GP": 4, "union_contenu:GP/GN": 4, "s_dans_union:GP/GV": 4, "union_contenu:SUB/SUB": 4, "s_dans_union:REL/GV": 3
… [768 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/pin_audit && python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'/tmp/pin_audit/tools')\nimport bloc_partition as bp\nfrom collections import Counter\nDEPOT='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'\na=json.load(open(DEPOT+'/reports/pensee-fiabilite-produit.json'))\nb … [2007 caractères tronqués]`

  ```
fiabilite {'textes': 46, 'chev': 23, 'paires': 107, 'segs': 360, 'union': 85, 'att': 284, 'classes': {'s_dans_union': 37, 'croisement': 7, 'union_contenu': 60, 'meme_span': 3}, 'impliques': 162, 'memes_types': 70, 'types_diff': 37}
  part labels impliques 0.45
bloc_l {'textes': 50, 'chev': 31, 'paires': 132, 'segs': 362, 'union': 98, 'att': 265, 'classes': {'s_dans_union': 43, 'croisement': 19, 'union_contenu': 67, 'meme_span': 3}, 'impliques': 152, 'memes_types': 61, 'types_diff': 71}
  part labels impliques 0.42
  ```

- **bash** `{"command": "cd /tmp/pin_audit && python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'/tmp/pin_audit/tools')\nimport bloc_partition as bp\nDEPOT='/home/stephane/Data13TB/stephane/GitHub/Qtrinet'\nb=json.load(open(DEPOT+'/reports/pensee-produit-bloc-l.json'))\na=json.load(open(DEPOT+'/reports/pens … [945 caractères tronqués]`

  ```
fiab segs 360 involved 170 labels in overlapping texts 314 texts_chev 23
bloc segs 362 involved 188 labels in overlapping texts 287 texts_chev 31
  ```

- **bash** `{"command": "cd /tmp/pin_audit && python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'/tmp/pin_audit/tools'); sys.path.insert(0,'/tmp/pin_audit/tools/tests/linguistique'); sys.path.insert(0,'/tmp/partition_syntagmes')\nimport bloc_partition as bp, evaluer_gold as eg\nfrom patch_eval import textes … [2120 caractères tronqués]`

  ```
gold F1 0.6163 P 0.7122 R 0.5432 exact 217 couv 0.9079 pos 0.7581
bancs paires 91 textes 33 segments 636 att 481 octets 2064733 vues 714 classes {'inclusion_s_dans_union': 80, 'croisement': 5, 'meme_span_union': 6}
libres paires 29 textes 7 segments 214 att 161 octets 959342 vues 155 classes {'inclusion_s_dans_union': 24, 'meme_span_union': 3, 'croisement': 2}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git rev-parse HEAD && git log -1 --format='%H %cd %s' && git status --short tools/bloc_linguistique.py tools/tests/linguistique/gold.json | cat", "description": "Check current HEAD and module status"}`

  ```
c5b80dd83ee4364df348903796fcaf5fd1071f82
c5b80dd83ee4364df348903796fcaf5fd1071f82 Fri Nov 6 19:03:16 2026 -0500 B13 — LE GOLD CORRIGÉ (4 GP SANS PRÉPOSITION) : EXACT 226/226 (1,0000), COUVERTURE 0,9289 → 0,9456, 17 → 13 SPANS ; 183/183
M  tools/bloc_linguistique.py
  ```

- **bash** `{"command": "cd /tmp/partition_syntagmes && python3 - <<'PY'\nimport json\np=json.load(open('patch_eval.json'))\nfor k in ['brut','alternative','filtrer']:\n    for b in ['gold','bancs','libres']:\n        print(k,b,json.dumps(p[b][k],ensure_ascii=False)[:600])\n    print()\nprint('pref',p['preferen … [233 caractères tronqués]`

  ```
brut gold {"f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "tete_f1": 0.7336, "tp": 1018, "fp": 600, "fn": 845, "pos": 0.7581, "fraction": 0.5537, "att_cibles": 239, "att_labels": 222, "att_exact": 222, "att_exact_taux": 0.9289, "att_couverture": 0.9289, "att_topk": 221, "att_tete_topk": 0.9955}
brut bancs {"variante": "brut", "textes": 96, "paires": 239, "textes_avec_chevauchement": 54, "segments": 722, "union": 183, "attachements": 549, "classes": {"union_contenu": 127, "inclusion_s_dans_union": 80, "croisement": 26, "meme_span_union": 6}, "octets_json": 1928458, "vues_alternative": 0, "vues_par_segment_ambigu": 0.0}
brut libres {"variante": "brut", "textes": 25, "paires": 59, "textes_avec_chevauchement": 10, "segments": 233, "union": 47, "attachements": 179, "classes": {"union_contenu": 24, "inclusion_s_dans_union": 24, "croisement": 8, "meme_span_union": 3}, "octets_json": 928683, "vues_alternative": 0, "vues_par_segment_ambigu": 0.0}

alternative gold {"f1": 0.5849, "precision": 0.6292, "rappel": 0.5464, "tete_f1": 0.7336, "tp": 1018, "fp": 600, "fn": 845, "pos": 0.7581, "fraction": 0.5537, "att_cibles": 239, "att_labels": 222, "att_exact": 222, "att_exact_taux": 0.9289, 
… [1875 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/pin_audit && python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'/tmp/pin_audit/tools'); sys.path.insert(0,'/tmp/partition_syntagmes')\nimport bloc_partition as bp\nfrom patch_eval import textes_bancs, textes_libres, syntagmes\ntextes=textes_bancs()+textes_libres()\nfor nom,h … [1022 caractères tronqués]`

  ```
brut max 138 mediane 44 p95 74 >100 9
alternative max 157 mediane 55 p95 88 >100 19
filtrer max 143 mediane 48 p95 96 >100 28
  ```

- **bash** `{"command": "cd /tmp/pin_audit && grep -n 'def priorite_par_defaut' -A 12 tools/bloc_linguistique.py", "description": "Check default source priority for compositions"}`

  ```
1849:def priorite_par_defaut() -> dict | None:
1850-    """La fusion par niveau si un neuronal réel est joignable (clé DeepSeek), sinon la confiance.
1851-
1852-    Le mock a montré que le niveau perd (0,3432) ; le réel (deux passes) a montré qu'il gagne
1853-    (0,9389). Le défaut suit donc la **présence d'un réel**, pas une doctrine.
1854-    """
1855-    return PRIORITE_NIVEAU if os.environ.get("DEEPSEEK_KEY_FILE") else None
1856-
1857-
1858-PRIORITE_NIVEAU = {
1859-    "graphème": "heuristique", "morphème": "heuristique", "mot": "heuristique",
1860-    "pos": "neuronal", "syntagme": "neuronal", "phrase": "heuristique",
1861-    "pragmatique": "heuristique", "discours": "heuristique", "document": "heuristique",
  ```

