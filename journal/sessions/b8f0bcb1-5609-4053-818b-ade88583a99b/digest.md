# Session DSH — relecture

- identifiant : `b8f0bcb1-5609-4053-818b-ade88583a99b`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-07 00:49:20
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **les 2 spans restants et la convention des GV** — diagnostic et règles candidates mesurées, sans modifier le code du dépôt.

Contexte : `tools/bloc_linguistique.py` (`_syntagmes_simple`, `_cible_precedent`, `est_verbe`), `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bloc`), `tools/tests/linguistique/gold_split.py`. État : **POS 86,25 %**, **F1 0,7535**, **attachement 236/237 (0,9916)**, 2 spans perdus (`r035` « The film she talks about is out. » — relative zéro ; `g017` « She said that she would come yesterday. » — arbitrage d'adverbe). Fichier : les fiches `reports/rapport-gn-pronom-sujet.md`, `reports/rapport-r264-elision.md`.

À faire :
1. **`r035`** : reproduire, expliquer (pourquoi aucune REL n'est produite sur « she talks about »), proposer 2 règles générales mesurées (dev/test), avec le patch exact.
2. **`g017`** : reproduire, expliquer l'arbitrage d'adverbe (« yesterday » dans ou hors de la SUB), proposer une règle mesurée.
3. **La convention des GV** : 322 FP / 180 FN. Classe les erreurs (GV qui inclut le sujet, GV qui inclut l'adverbe, GV en double S×chunker, GV manquant), donne les effectifs, et mesure 2 à 3 règles candidates (chacune sur dev/test, avec l'effet sur F1 **et** sur l'attachement — il ne doit pas baisser).
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-segmentation-restante.md` et `reports/pensee-segmentation-restante.json` (patchs exacts inclus).
5. Ne commite rien ; ne modifie aucun existant ; pas de `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, natifs. Simulation par copie.

Rends un résumé : les causes, les gains dev/test par règle, les patchs, et ce qui est rejeté.
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

⏵ Exploration du dépôt et des outils de segmentation

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git branch --show-current && git status --short | head -50 && ls", "description": "Check branch and workspace state"}`

  ```
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
D  journal/2026-11-07/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
D  journal/sessions/082fe8ca-3e1e-4454-b91b-12586843e880/digest.md
D  journal/sessions/082fe8ca-3e1e-4454-b91b-12586843e880/rapport.md
D  journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/digest.md
D  journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/rapport.md
D  journal/sessions/1555bdd3-27e9-4779-b1e7-716e32399c11/digest.md
D
… [1681 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | head -60 && echo '---' && ls tools/tests/linguistique/ | head -40", "description": "List reports and linguistic test tools"}`

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
… [445 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des fiches existantes et des outils de segmentation

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/gold_split.py reports/rapport-gn-pronom-sujet.md reports/rapport-r264-elision.md", "description": "Count lines of key files"}`

  ```
2737 tools/bloc_linguistique.py
   307 tools/tests/linguistique/evaluer_gold.py
    50 tools/tests/linguistique/gold_split.py
    88 reports/rapport-gn-pronom-sujet.md
    60 reports/rapport-r264-elision.md
  3242 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -i -E 'pronon|elision|segment|syntagme|bloc'", "description": "Find related reports"}`

  ```
bloc-linguistique.json
kv-cache-int8-bloc.json
pensee-elision.json
pensee-gold-syntagmes.json
pensee-juge-bloc.json
pensee-partition-syntagmes.json
pensee-produit-bloc-l.json
pensee-r264-elision.json
pensee-segmentation-v4.json
pensee-segmenteur-defaut.json
pensee-segmenteur-hybride.json
pensee-segmenteur.json
pensee-segmenteur-union.json
r41-bloc-tableaux.json
r42-bloc-code.json
r43-bloc-maths.json
rapport-bloc-linguistique.md
rapport-kv-cache-int8-bloc.md
rapport-miroir-blocs.md
rapport-partition-syntagmes.md
rapport-pensee-elision.md
rapport-pensee-gold-syntagmes.md
rapport-pensee-juge-bloc.md
rapport-pensee-segmentation-v4.md
rapport-pensee-segmenteur-defaut.md
rapport-pensee-segmenteur-hybride.md
rapport-pensee-segmenteur.md
rapport-pensee-segmenteur-union.md
rapport-produit-bloc-l.md
rapport-r264-elision.md
rapport-r41-bloc-tableaux.md
rapport-r42-bloc-code.md
rapport-r43-bloc-maths.md
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gn-pronom-sujet.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r264-elision.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gn-pronom-sujet.md</path>
<type>file</type>
<content>
1: # B13 — le pronom sujet est un GN : F1 0,6519 → 0,7013, attachement préservé
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-07 · **Verdict** : ✅
4: > **La plus grosse erreur de segmentation** était la convention : le gold segmente le **pronom
5: > sujet** comme un **GN** (« Il | a couru »), le bloc le laissait dans le GV — **417 GN manquants**
6: > et **333 GV en trop**. La règle (un pronom sujet devant un verbe émet un GN, le GV commence
7: > après) fait passer la **F1 de 0,6519 à 0,7013** (+4,9), sans perdre un seul attachement :
8: > **236/237, couverture 0,9916**. **dev 0,6986 / test 0,7073** ; **183/183**.
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
11: > branche GV), [`autotest.py`](../tools/pensee/autotest.py) (7 assertions) ; JSON
12: > [`pensee-gn-pronom-sujet.json`](pensee-gn-pronom-sujet.json).
13: 
14: ## 1. La règle
15: 
16: ```python
17: # un pronom sujet devant le verbe est un GN (« Il | a couru ») — convention du gold
18: if (typ == "mot" and langu
… [3358 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-r264-elision.md</path>
<type>file</type>
<content>
1: # B13 — `r264` réglé : le GV s'arrête au marqueur élidé (`qu'il`), couverture 0,9916
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
4: > **Le 13e span est retrouvé** : dans « Je sais **qu'il vient demain** », le GV « sais » avalait
5: > le marqueur élidé, donc la SUB n'était jamais produite au bon span. La condition d'arrêt du GV
6: > testait `endswith("qu")` sur le **token entier** (`qu'il`) au lieu de son **radical** (`qu`).
7: > Corrigé : l'attachement passe de **235/236 à 236/237**, la **couverture de 0,9874 à 0,9916**,
8: > la **F1 de 0,6482 à 0,6519** ; **183/183** ; **2 spans restants** (`r035`, `g017`).
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (boucle GV),
11: > [`autotest.py`](../tools/pensee/autotest.py) (17 assertions) ; JSON
12: > [`pensee-r264-elision.json`](pensee-r264-elision.json).
13: 
14: ## 1. Le bug
15: 
16: ```python
17: # avant : la condition teste le token entier
18: and (_normaliser(mots[j][2]).split("'")[0] + "e"
19:      if _normaliser(mot
… [1779 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du dispositif d'évaluation et du gold

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_split.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py</path>
<type>file</type>
<content>
1: """evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) + synthétique (160).
2: 
3: Trois niveaux : POS (token, exact), syntagmes (exact + **par tête**), pragmatique. Quatre
4: lectures : heuristique, mock neuronal, parallèle, cascade. Le vrai modèle est optionnel
5: (`--reel`) : s'il ne répond pas, il est refusé, pas simulé.
6: """
7: from __future__ import annotations
8: 
9: import argparse
10: import json
11: import pathlib
12: import sys
13: from collections import Counter, defaultdict
14: 
15: RACINE = pathlib.Path(__file__).resolve().parents[3]
16: sys.path.insert(0, str(RACINE / "tools"))
17: import bloc_linguistique as bl  # noqa: E402
18: 
19: GOLD = pathlib.Path(__file__).with_name("gold.json")
20: REEL = pathlib.Path(__file__).with_name("gold_reel.json")
21: SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")
22: 
23: 
24: def charger() -> list[dict]:
25:     hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
26:     reel = json.loads(REEL.read_text(encoding="utf-8"))["phrases"]
27:     synth = json.
… [16119 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_split.py</path>
<type>file</type>
<content>
1: """gold_split.py — le gold 612 coupé en **dev** et **test**, de façon déterministe.
2: 
3: Le problème. Toutes les mesures de la session sont **in-sample** : les règles de segmentation et
4: d'attachement ont été dessinées en regardant les échecs du même gold qui les mesure. Pour juger
5: une règle, il faut un gold **tenu à l'écart** : on règle sur `dev`, on évalue sur `test`.
6: 
7: Protocole (fixé ici). Le split est un **hash stable de l'identifiant** (`crc32(id) % 3 == 0` →
8: test, sinon dev), donc reproductible, insensible à l'ordre et indépendant du contenu. Il est
9: **stratifié par source** (`hand`, `reel`, `synthetique`) et par langue : on vérifie l'équilibre
10: dans la fiche. Aucune phrase n'est dupliquée entre les deux ; l'union redonne les 612.
11: 
12: Usage :
13:     from tools.tests.linguistique.gold_split import dev, test, compter
14:     ph = charger(); d = dev(ph); t = test(ph)
15: """
16: from __future__ import annotations
17: 
18: import zlib
19: 
20: PART_TEST = 3  # une phrase sur trois va au test
21: 
22: 
23: def _est_test(phras
… [1070 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Localisation des fonctions clés dans le bloc linguistique

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def _syntagmes_simple\\|def _cible_precedent\\|def est_verbe\\|def _est_verbe\\|def _normaliser\\|SUJETS\\s*=\\|_syntagmes_simple(\" tools/bloc_linguistique.py", "description": "Locate key functions and SUJETS list"}`

  ```
150:def _normaliser(texte: str) -> str:
378:SUJETS = {"i", "you", "he", "she", "it", "we", "they", "there", "who", "that", "which",
501:def _est_verbe(mot: str) -> bool:
931:    def _cible_precedent(texte: str, segment: dict, precedent: dict | None, verbes) -> str | None:
1116:    def _syntagmes_simple(self, texte: str, langue: str,
1129:        def est_verbe(d: int, m: str) -> bool:
1493:        simples = self._syntagmes_simple(texte, lg, pos_verbes)
1706:        for s in h._syntagmes_simple(texte, lg):
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"r035\\|g017\" -r tools/tests/linguistique/ reports/*.json 2>/dev/null | head -20", "description": "Find r035 and g017 references"}`

  ```
tools/tests/linguistique/gold.py:71:    ("g017", "en", "She said that she would come yesterday.",
tools/tests/linguistique/gold.json:1080:   "id": "g017",
tools/tests/linguistique/gold_reel.py:143:    ("r035", "en", "The film she talks about is out.",
tools/tests/linguistique/gold_reel.json:2105:   "id": "r035",
tools/tests/linguistique/gold_gele.json:1096:"id": "g017",
tools/tests/linguistique/gold_gele.json:3449:"id": "r035",
reports/pensee-audit-r1r3.json:277:     "g017:SUB"
reports/pensee-audit-r1r3.json:279:    "lecture": "Le nouveau scan redige gagne 4 mais perd g017 : verbes_vus n'est pas incremente apres un AUX, donc la garde d'adverbe final ne s'applique pas et yesterday reste dans la SUB."
reports/pensee-audit-r1r3.json:545:   "g017",
reports/pensee-audit-r1r3.json:616:     "r035",
reports/pensee-audit-r1r3.json:662:     "g017",
reports/pensee-audit-r1r3.json:670:    "id": "r035",
reports/pensee-audit-r1r3.json:934:    "id": "g017",
reports/pensee-audit-r1r3.json:967:  "lecture": "Les 27 contiennent les 17 ids de A17 (meme ensemble, memes types) ; les 10 autres sont 7 régressions nouvelles (6 R1a + 1 R2) et 3 gains A17 non intégrés (g017, r153, r280)."
reports/pensee-audi
… [1095 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 330, "limit": 200}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 900, "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
330:               "arrivent pleut pleuvoir habite habites habitent parle parlons parlez parlent explique "
331:               "expliquons expliquez expliquent souffle soufflent chante chantent chantes peut peux "
332:               "pouvons pouvez peuvent doit devons devez doivent pourrait pourrais pourrions pourriez "
333:               "pourraient devrait devrais voudrais voudrait veux veut voulons voulez veulent prend "
334:               "prends prenons prenez prennent donne donnes donnons donnez donnent trouve trouves "
335:               "trouvons trouvez trouvent cherche cherches cherchons cherchez cherchent regarde "
336:               "regardes regardons regardez regardent écoute écoutes écoutons écoutez écoutent ouvre "
337:               "ouvres ouvrons ouvrez ouvrent ferme fermes fermons fermez ferment commence commences "
338:               "commençons commencez commencent essaie essaies essayons essayez essaient attrape "
339:               "attrapes attrapons attrapez attrapent".split()),
340:     "en": set("sleeps sleep slept saw see seen says said co
… [12898 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
900: 
901:     # -- syntagmes ----------------------------------------------------------
902:     def _syntagmes_s(self, texte: str) -> list[dict] | None:
903:         if not self.segmenter_s:
904:             return None
905:         try:
906:             if str(RACINE / "tools/structures") not in sys.path:
907:                 sys.path.insert(0, str(RACINE / "tools/structures"))
908:             import generateur  # le générateur S, importé en lecture seule
909:             return generateur.analyser(texte)
910:         except Exception:
911:             return None
912: 
913:     def _cibles_s(self, texte: str) -> dict:
914:         """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).
915: 
916:         Lecture seule de l'API interne du S : `_tokens`/`_segmente` rendent les `Segment` avec
917:         `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
918:         (GP, puis GN, puis GV), comme le premier candidat de `analyser`.
919:         """
920:         if not self.segmenter_s:
921:             return {
… [5583 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 320, "offset": 1100}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1100:         """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
1101:         if segment.get("type") == "GV" or not gvs:
1102:             return []
1103:         def ecart(g: dict) -> int:
1104:             if g["fin"] <= segment["debut"]:
1105:                 return segment["debut"] - g["fin"]
1106:             if g["debut"] >= segment["fin"]:
1107:                 return g["debut"] - segment["fin"]
1108:             return 0
1109:         proches: list[str] = []
1110:         for g in sorted(gvs, key=ecart)[:k]:
1111:             v = Heuristique._verbe_gv(texte, g, verbes, cache)
1112:             if v and v not in proches:
1113:                 proches.append(v)
1114:         return proches
1115: 
1116:     def _syntagmes_simple(self, texte: str, langue: str,
1117:                           pos_verbes: set[int] | None = None) -> list[dict]:
1118:         mots = self._mots(texte)
1119:         lex = POS_FERME.get(langue, POS_FERME["fr"])
1120:         pos_verbes = pos_verbes or set()
1121:         par_debut = {m[0]: k for k, m in enum
… [19913 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reproduction des deux cas perdus sur le gold

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib\ng = json.loads(pathlib.Path('tools/tests/linguistique/gold_reel.json').read_text())\nfor p in g['phrases']:\n    if p['id'] in ('r035',):\n        print(json.dumps(p, ensure_ascii=False, inden … [270 caractères tronqués]`

  ```
{
 "id": "r035",
 "langue": "en",
 "texte": "The film she talks about is out.",
 "mots": [
  {
   "texte": "The",
   "pos": "DET",
   "debut": 0,
   "fin": 3
  },
  {
   "texte": "film",
   "pos": "NOUN",
   "debut": 4,
   "fin": 8
  },
  {
   "texte": "she",
   "pos": "PRON",
   "debut": 9,
   "fin": 12
  },
  {
   "texte": "talks",
   "pos": "VERB",
   "debut": 13,
   "fin": 18
  },
  {
   "texte": "about",
   "pos": "PREP",
   "debut": 19,
   "fin": 24
  },
  {
   "texte": "is",
   "pos": "AUX",
   "debut": 25,
   "fin": 27
  },
  {
   "texte": "out",
   "pos": "ADV",
   "debut": 28,
   "fin": 31
  }
 ],
 "segments": [
  {
   "type": "GN",
   "texte": "The film",
   "role": "patient",
   "debut": 0,
   "fin": 8
  },
  {
   "type": "REL",
   "texte": "she talks about",
   "role": "qualité",
   "debut": 9,
   "fin": 24,
   "cibles": [
    "film"
   ],
   "cible": "film"
  },
  {
   "type": "GV",
   "texte": "is out",
   "role": "prédicat",
   "debut": 25,
   "fin": 31
  }
 ],
 "pragma": {
  "acte": "assertion"
 },
 "source": "reel"
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib\ng2 = json.loads(pathlib.Path('tools/tests/linguistique/gold_synthetique.json').read_text())\nprint(len(g2['phrases']))\nfor p in g2['phrases']:\n    if 'yesterday' in p['texte'] and 'would com … [138 caractères tronqués]`

  ```
160
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib\nfor fn in ('gold.json','gold_reel.json','gold_synthetique.json','gold_gele.json'):\n    g = json.loads(pathlib.Path('tools/tests/linguistique/'+fn).read_text())\n    hits=[p for p in g['phrase … [179 caractères tronqués]`

  ```
gold.json 20 1 ['g017']
gold_reel.json 432 0 []
gold_synthetique.json 160 0 []
gold_gele.json 602 1 ['g017']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib\ng = json.loads(pathlib.Path('tools/tests/linguistique/gold.json').read_text())\nfor p in g['phrases']:\n    if p['id']=='g017':\n        print(json.dumps(p, ensure_ascii=False, indent=1))\nEOF … [41 caractères tronqués]`

  ```
{
 "id": "g017",
 "langue": "en",
 "texte": "She said that she would come yesterday.",
 "mots": [
  {
   "texte": "She",
   "pos": "PRON",
   "debut": 0,
   "fin": 3
  },
  {
   "texte": "said",
   "pos": "VERB",
   "debut": 4,
   "fin": 8
  },
  {
   "texte": "that",
   "pos": "CONJ",
   "debut": 9,
   "fin": 13
  },
  {
   "texte": "she",
   "pos": "PRON",
   "debut": 14,
   "fin": 17
  },
  {
   "texte": "would",
   "pos": "AUX",
   "debut": 18,
   "fin": 23
  },
  {
   "texte": "come",
   "pos": "VERB",
   "debut": 24,
   "fin": 28
  },
  {
   "texte": "yesterday",
   "pos": "ADV",
   "debut": 29,
   "fin": 38
  }
 ],
 "segments": [
  {
   "type": "GN",
   "texte": "She",
   "role": "agent",
   "debut": 0,
   "fin": 3
  },
  {
   "type": "GV",
   "texte": "said",
   "role": "prédicat",
   "debut": 4,
   "fin": 8
  },
  {
   "type": "SUB",
   "texte": "that she would come",
   "role": "contenu",
   "debut": 9,
   "fin": 28,
   "cibles": [
    "said"
   ],
   "cible": "said"
  }
 ],
 "pragma": {
  "acte": "assertion",
  "modalite": true
 }
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/pensee-*.json | tail -30 && echo '---' && python3 -c \"\nimport json,pathlib\np=pathlib.Path('reports/pensee-gn-pronom-sujet.json')\nprint(p.exists())\nif p.exists():\n    d=json.loads(p.read_text())\n    print(json.dumps( … [93 caractères tronqués]`

  ```
reports/pensee-seuil-fin.json
reports/pensee-seuil-graines.json
reports/pensee-seuil.json
reports/pensee-seuil-parallele.json
reports/pensee-shaping.json
reports/pensee-si.json
reports/pensee-soustype-variance.json
reports/pensee-spans-chunker.json
reports/pensee-spans.json
reports/pensee-spans-v7.json
reports/pensee-stochastique.json
reports/pensee-tirages.json
reports/pensee-topk-diagnostic.json
reports/pensee-topk-strict.json
reports/pensee-topk-v8.json
reports/pensee-tres-rare.json
reports/pensee-troisieme-passe.json
reports/pensee-ultra-rare.json
reports/pensee-un-look.json
reports/pensee-v10.json
reports/pensee-v11.json
reports/pensee-v12.json
reports/pensee-v9.json
reports/pensee-variance.json
reports/pensee-verbe-gv.json
reports/pensee-verite.json
reports/pensee-votante3.json
reports/pensee-votante.json
reports/pensee-vote.json
reports/pensee-vrais-absents.json
---
True
{
 "date": "2026-11-07",
 "ligne": "B13",
 "regle": "pronom sujet (fr/en) et nom propre devant un verbe → GN",
 "cause": "convention du gold : 417 GN manquants, 333 GV en trop",
 "avant": {
  "f1": 0.6519,
  "f1_dev": 0.6482,
  "f1_test": 0.6601,
  "exact": "236/237",
  "couverture": 0.9916,
  "tete": 0.7709
… [432 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mesure de la ligne de base (F1 all/dev/test, attachement)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, pathlib, json\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nfrom evaler_gold import charger, evaluer_bloc\nfrom gold_split import dev, test, … [517 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
ModuleNotFoundError: No module named 'evaler_gold'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, pathlib, json\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaler_gold as eg\nfrom gold_split import dev, test\nph = eg.charger()\np … [529 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
ModuleNotFoundError: No module named 'evaler_gold'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\nfrom gold_split import dev, test\nph = eg.charger()\nprint('phrases' … [504 caractères tronqués]`

  ```
phrases 612 dev 422 test 190
all f1 0.7533 P 0.7239 R 0.7853 tp 1463 fp 558 fn 400 att 236 / 239 0.9916 exact 236 tete 0.864
dev f1 0.7476 P 0.7223 R 0.7747 tp 1004 fp 386 fn 292 att 160 / 163 0.9877 exact 160 tete 0.8603
test f1 0.7663 P 0.7274 R 0.8095 tp 459 fp 172 fn 108 att 76 / 76 1.0 exact 76 tete 0.8724
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nh = bl.Heuristique()\nfor txt in [\"The film she talks about is out.\", \"She said that she wou … [518 caractères tronqués]`

  ```
=== The film she talks about is out.
pos: [('The', 'DET'), ('film', 'NOUN'), ('she', 'PRON'), ('talks', 'VERB'), ('about', 'PREP'), ('is', 'AUX'), ('out', 'ADV'), ('.', 'PONCT')]
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 12, in <module>
AttributeError: 'Etiquette' object has no attribute 'role'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nh = bl.Heuristique()\nfor txt in [\"The film she talks about is out.\", \"She said that she wou … [497 caractères tronqués]`

  ```
=== The film she talks about is out.
pos: [('The', 'DET'), ('film', 'NOUN'), ('she', 'PRON'), ('talks', 'VERB'), ('about', 'PREP'), ('is', 'AUX'), ('out', 'ADV'), ('.', 'PONCT')]
  SEG GN 'The film she' 0 12 cible= 'talks' cands= ['GN', 'talks', 'out']
  SEG GV 'talks' 13 18 cible= None cands= ['GV']
  SEG GV 'about is out' 19 31 cible= None cands= ['GV']
  mots: [(0, 3, 'The', 'mot'), (4, 8, 'film', 'mot'), (9, 12, 'she', 'mot'), (13, 18, 'talks', 'mot'), (19, 24, 'about', 'mot'), (25, 27, 'is', 'mot'), (28, 31, 'out', 'mot'), (31, 32, '.', 'ponctuation')]
=== She said that she would come yesterday.
pos: [('She', 'PRON'), ('said', 'VERB'), ('that', 'CONJ'), ('she', 'PRON'), ('would', 'AUX'), ('come', 'VERB'), ('yesterday', 'ADV'), ('.', 'PONCT')]
  SEG GN 'She' 0 3 cible= 'said' cands= ['GN', 'said']
  SEG GV 'said' 4 8 cible= None cands= ['GV']
  SEG SUB 'that she would come yesterday' 9 38 cible= 'said' cands= ['SUB', 'said', 'said']
  mots: [(0, 3, 'She', 'mot'), (4, 8, 'said', 'mot'), (9, 13, 'that', 'mot'), (14, 17, 'she', 'mot'), (18, 23, 'would', 'mot'), (24, 28, 'come', 'mot'), (29, 38, 'yesterday', 'mot'), (38, 39, '.', 'ponctuation')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,pathlib\nd=json.loads(pathlib.Path('reports/pensee-audit-r1r3.json').read_text())\nprint(list(d.keys()))\nfor k,v in d.items():\n    if isinstance(v,(str,int,float,bool)):\n        print(k,'=',v)\nEOF", … [52 caractères tronqués]`

  ```
['rapport', 'ligne', 'branche', 'commit_audite', 'commit_parent', 'date', 'objet', 'methode', 'verdict', 'rejeu', 'ablations', 'decomposition', 'spans_27', 'controle_negatif', 'dev_test', 'portes_autotest', 'ecarts', 'limites', 'fichiers_ecrits', 'commit']
rapport = audit-r1r3
ligne = B13
branche = s/v7
commit_audite = f908d7b0613c8a5eb8fae7fab514bfdc5fa4668b
commit_parent = 69bd865ec1bae1958b6f617bde4bf685a15d7d67
date = 2026-11-05
objet = Audit du round R1/R2/R3 : rejeu des valeurs, ablations par règle, contrôles négatifs, dev/test, portes.
commit = False
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,pathlib\nd=json.loads(pathlib.Path('reports/pensee-audit-r1r3.json').read_text())\nprint(json.dumps({k:d[k] for k in ('methode','verdict','rejeu','ablations','dev_test','controle_negatif')},ensure_ascii … [81 caractères tronqués]`

  ```
{
 "methode": {
  "gold_vivant": {
   "source": "evaluer_gold.charger",
   "phrases": 612,
   "cibles": 239,
   "sources": {
    "hand": 20,
    "reel": 432,
    "synthetique": 160
   }
  },
  "gold_gele": {
   "source": "evaluer_gold.charger_gelé",
   "phrases": 602,
   "cibles": 239,
   "note": "les 10 phrases ajoutees apres le gel n'ont aucune cible"
  },
  "mesure": "evaluer_gold.evaluer_bloc pour les valeurs officielles ; harnais local pour les ensembles d'ids et les ablations",
  "ablations": "copie du module dans /tmp, une seule modification reintroduite par variante, puis import et mesure",
  "fidelite": "la variante tout-eteint ne differe du parent 69bd865e que par deux constantes inutilisees ; elle redonne 196/195, 0,5555 vivant / 0,5595 gelé, 43 spans, top-k 166",
  "portes": "PYTHONPATH=. python3 -m tools.pensee.autotest",
  "aucune_modification": true,
  "aucun_commit": true,
  "note_arbre_de_travail": {
   "mesures_prises": "2026-11-05 entre 21:27 et 21:44",
   "etat_mesure": "tools/bloc_linguistique.py identique a f908d7b0 (copie de base byte-identique)",
   "effet_arbre_courant": "labels 212, exact 212, couverture 0,887 inchangés ; top-k 211 au lieu de 177 ; portes 
… [4800 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,pathlib\nd=json.loads(pathlib.Path('reports/pensee-audit-r1r3.json').read_text())\nprint(json.dumps(d['ablations']['regles'].get('R1c'),ensure_ascii=False,indent=1))\nprint('---- spans_27 keys/lecture - … [273 caractères tronqués]`

  ```
{
 "ablation": "sans_r1c",
 "labels": 209,
 "exact": 209,
 "delta_labels": -3,
 "delta_exact": -3,
 "gains": {
  "dev": 2,
  "test": 2,
  "total": 4
 },
 "pertes": {
  "dev": 1,
  "test": 0,
  "total": 1
 },
 "effet_net": 3,
 "f1_vivant": 0.5685,
 "delta_f1": -0.0035,
 "gains_ids": [
  "r224:REL",
  "r291:REL",
  "r115:REL",
  "r239:REL"
 ],
 "pertes_ids": [
  "g017:SUB"
 ],
 "lecture": "Le nouveau scan redige gagne 4 mais perd g017 : verbes_vus n'est pas incremente apres un AUX, donc la garde d'adverbe final ne s'applique pas et yesterday reste dans la SUB."
}
---- spans_27 keys/lecture ----
{
 "counts": {
  "total": 27,
  "REL": 16,
  "SUB": 6,
  "GP": 5,
  "fr": 22,
  "en": 5,
  "synthetique": 19,
  "reel": 7,
  "hand": 1
 },
 "classes": [
  {
   "classe": "A17 non récupérable (13) + hors périmètre (4)",
   "n": 17,
   "types": {
    "REL": 8,
    "SUB": 5,
    "GP": 4
   },
   "ids": [
    "r035",
    "r255",
    "r264",
    "r288",
    "s010",
    "s027",
    "s035",
    "s044",
    "s061",
    "s065",
    "s112",
    "s114",
    "s125",
    "s141",
    "s146",
    "s148",
    "s160"
   ]
  },
  {
   "classe": "Régressions nouvelles",
   "n": 7,
   "types": {
    "REL": 7,
   
… [5688 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Ventilation des erreurs par type de syntagme

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\nfrom gold_split import dev, test\nph = eg.charger(); h  … [558 caractères tronqués]`

  ```
TP {'GN': 684, 'GV': 532, 'GP': 105, 'SUB': 69, 'REL': 73} 1463
FP {'GP': 25, 'GV': 322, 'SUB': 4, 'REL': 32, 'GN': 175} 558
FN {'GV': 180, 'SUB': 1, 'GN': 144, 'REL': 1, 'ADJ': 35, 'ADV': 30, 'PONCT': 9} 400
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 160, "offset": 1480}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1480:                                             langue=lg, script=script))
1481: 
1482:         # 5. syntagmes : le générateur S (candidats) ou un chunker simple
1483:         verbes = [(e.debut, e.fin, e.valeur) for e in etiquettes
1484:                   if e.niveau == "pos" and e.type == "VERB"]
1485:         # le générateur S est **français** : il ne segmente pas l'anglais (A14) — on ne
1486:         # l'interroge que pour le français, sinon ses segments polluent l'union.
1487:         cands = self._syntagmes_s(texte) if (langue or lg) == "fr" else []
1488:         cibles_s = self._cibles_s(texte) if cands else {}
1489:         cache_gv: dict = {}  # un GV n'est analysé qu'une fois par analyse
1490:         # **un seul chunking par analyse**, partagé par les trois chemins (S, union, chunker) :
1491:         # le O(n²) mesuré venait des re-chunkings (A6, A11) — sortie identique (T178).
1492:         pos_verbes = {e.debut for e in etiquettes if e.niveau == "pos" and e.type == "VERB"}
1493:         simples = self._syntagmes_simple(texte, lg, pos_verbes)
1494:      
… [10429 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"class Heuristique\" -A 40 tools/bloc_linguistique.py | head -60", "description": "Read Heuristique constructor defaults"}`

  ```
788:class Heuristique:
789-    """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""
790-
791-    nom = "heuristique"
792-
793-    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
794-                 seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
795-                 union: bool = True, partition: str = "alternative"):
796-        self.profils = profils
797-        self.segmenter_s = segmenter_s
798-        self.seuil_ouvert = seuil_ouvert
799-        self.seuil_langue = seuil_langue
800-        self.union = union
801-        # "brut" : la sortie d'avant (chevauchements non documentés) ; "alternative" :
802-        # les deux segments restent, `meta.alternative` dit lequel est préféré ;
803-        # "filtrer_union" : on retire le S qui **contient** un segment chunker (le filtre
804-        # union du P0-3) ; "filtrer" : partition stricte, le chunker est la partition.
805-        # Dans les deux filtres, le segment retiré reste dans `meta.alternative` (`retire`).
806-        if partition not in ("brut", "alternative", "filtrer_union", "filtrer"):
807-            raise ValueError("partition atten
… [1085 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection d'échantillons de GV faux positifs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\nph = eg.charger(); h = bl.Heuristique()\nn=0\nfor p in  … [871 caractères tronqués]`

  ```
g003  fr GV [9:21] "a vu l'homme" conf=[(0.4, None), (0.3, True), (0.4, None)]
     gold   : [('GN', 0, 8, 'La femme'), ('GV', 9, 13, 'a vu'), ('GN', 14, 21, "l'homme"), ('GP', 22, 34, 'dans le parc')]
     pred   : [('GN', 0, 8, 'La femme'), ('GV', 9, 13, 'a vu'), ('GV', 9, 21, "a vu l'homme"), ('GN', 14, 21, "l'homme"), ('GP', 22, 34, 'dans le parc')]
g004  fr GV [0:10] 'Il a couru' conf=[(0.3, True), (0.4, None), (0.3, True)]
     gold   : [('GN', 0, 2, 'Il'), ('GV', 3, 10, 'a couru'), ('GP', 11, 31, 'pour attraper le bus')]
     pred   : [('GN', 0, 2, 'Il'), ('GV', 0, 10, 'Il a couru'), ('GV', 3, 10, 'a couru'), ('GP', 11, 31, 'pour attraper le bus')]
g005  fr GV [0:10] 'Elle a dit' conf=[(0.3, True), (0.55, None), (0.3, True)]
     gold   : [('GN', 0, 4, 'Elle'), ('GV', 5, 10, 'a dit'), ('SUB', 11, 28, "qu'elle viendrait")]
     pred   : [('GN', 0, 4, 'Elle'), ('GV', 0, 10, 'Elle a dit'), ('GV', 5, 10, 'a dit'), ('SUB', 11, 28, "qu'elle viendrait"), ('SUB', 11, 33, "qu'elle viendrait hier"), ('GP', 29, 33, 'hier')]
g008  fr GV [0:9] 'Marie lit' conf=[(0.3, True), (0.55, None), (0.3, True)]
     gold   : [('GN', 0, 5, 'Marie'), ('GV', 6, 9, 'lit'), ('GN', 10, 18, 'un livre')]
 
… [11008 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Traçage des origines S/chunker des GV en double

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nh = bl.Heuristique()\nfor txt in [\"Il a couru.\", \"Elle a dit qu'elle viendrait.\", \"Marie l … [372 caractères tronqués]`

  ```
=== Il a couru.
 simples: [('GN', 0, 2, 'Il'), ('GV', 3, 10, 'a couru')]
 S      : [('GV', 0, 10, 'Il a couru')]
=== Elle a dit qu'elle viendrait.
 simples: [('GN', 0, 4, 'Elle'), ('GV', 5, 10, 'a dit'), ('SUB', 11, 28, "qu'elle viendrait")]
 S      : [('GV', 0, 10, 'Elle a dit'), ('SUB', 11, 28, "qu'elle viendrait")]
=== Marie lit un livre.
 simples: [('GN', 10, 18, 'un livre')]
 S      : [('GV', 0, 9, 'Marie lit'), ('GN', 10, 18, 'un livre')]
  ```

### 🤖 Assistant

⏵ Classification mesurée des 322 FP / 180 FN de GV

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, collections, json\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\nph = eg.charger(); h = bl.Heuristique()\n\ndef po … [2424 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 19, in <module>
TypeError: tuple indices must be integers or slices, not str
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\nph = eg.charger(); h = bl.Heuristique()\n\ndef pos_map( … [2142 caractères tronqués]`

  ```
FP GV total 322
par catégorie: {'droite_autre': 49, 'sujet': 148, 'adverbe': 16, 'tronque': 39, 'objet': 24, 'parasite': 17, 'gauche_autre': 2, 'deux_cotes': 27}
dont voisine TP (double): {'droite_autre': 1, 'sujet': 135, 'adverbe': 1, 'tronque': 11, 'objet': 3, 'parasite': 0, 'gauche_autre': 1, 'deux_cotes': 1}

## droite_autre 49
    g003 "a vu l'homme" | La femme a vu l'homme dans le parc. | double= True
    g014 "vu l'homme" | J'ai vu l'homme avec le télescope. | double= False
    r203 'est bon' | Le livre que j'ai lu est bon. | double= False
    r209 'est absent' | L'élève dont je parle est absent. | double= False
## sujet 148
    g004 'Il a couru' | Il a couru pour attraper le bus. | double= True
    g005 'Elle a dit' | Elle a dit qu'elle viendrait hier. | double= True
    g008 'Marie lit' | Marie lit un livre. | double= True
    g009 'Il ne dort pas' | Il ne dort pas. | double= True
## adverbe 16
    g010 'Viens ici' | Viens ici ! | double= True
    r010 'viens demain' | Tu viens demain ? | double= False
    r019 'souffle fort' | Le vent souffle fort. | double= False
    r030 'come tomorrow' | You come tomorrow? | double= False
## tronque 39
    g013 'venir' | Peux-tu venir 
… [1279 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/bloc_linguistique.py", "description": "Read module header and RACINE"}`

  ```
#!/usr/bin/env python3
"""bloc_linguistique.py — le bloc d'étiquetage linguistique, du graphème à la pragmatique.

Un seul contrat (`BlocLinguistique.analyser`) et **plusieurs implémentations** :

  - `Heuristique` : CPU, déterministe, ultra-rapide ; elle étiquette la surface et produit des
    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
  - `MockNeuronal` : une implémentation neuronale **de contrat**, déterministe, pour tester la
    substitution et le parallèle sans GPU ;
  - `NeuronalLLM` : l'adaptateur réel, qui interroge un modèle local (`llama-cli`) et rend le
    même type d'annotation ;
  - `NeuronalLLMPOS` : le **tagger** neuronal réel — un modèle local, une liste de tokens, des
    POS alignés par grammaire GBNF ; c'est l'implémentation qualifiée sur le gold ;
  - `Parallele` et `Cascade` : les deux modes de composition. Le parallèle fusionne les
    étiquettes par confiance ; la cascade n'envoie au neuronal que le **résidu** des niveaux
    que l'heuristique ne couvre pas.

La sortie est une **annotation typée** — pas le corps de la RSN : chaque étiquette porte son
`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script`
… [1731 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"RACINE\" tools/bloc_linguistique.py", "description": "List RACINE uses"}`

  ```
49:RACINE = pathlib.Path(__file__).resolve().parent.parent
906:            if str(RACINE / "tools/structures") not in sys.path:
907:                sys.path.insert(0, str(RACINE / "tools/structures"))
2708:    ap.add_argument("--modele", default=str(RACINE / "models/Qwen2.5-0.5B-Q4_0.gguf"))
2713:    ap.add_argument("--udhr", default=str(RACINE / "data/udhr/articles.jsonl"))
  ```

### 🤖 Assistant

⏵ Classification des 180 GV manquants

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\nph = eg.charger(); h = bl.Heuristique()\nstats=collecti … [1416 caractères tronqués]`

  ```
FN GV total 180
## chevauche 110
    g014 'vu' | J'ai vu l'homme avec le télescope. | (5, 7)
    r010 'viens' | Tu viens demain ? | (3, 8)
    r019 'souffle' | Le vent souffle fort. | (8, 15)
    r023 'love' | We love music. | (3, 7)
## avale_GN 51
    r004 'brille' | Le soleil brille. | (10, 16)
    r046 'boit' | Le chat boit du lait. | (8, 12)
    r047 'poussent' | Les fleurs poussent dans le jardin. | (11, 19)
    r081 'apporte' | Le facteur apporte une lettre. | (11, 18)
## tronque 19
    s026 'ne écoute pas' | le sombre voyage ne écoute pas | (17, 30)
    s027 'marche avec il' | mon sombre village marche avec il | (19, 33)
    s049 'ouvre le cheval' | une lente fenêtre ouvre le cheval | (18, 33)
    s051 'cherche ma lettre' | une douce montagne cherche ma lettre | (19, 36)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\nph = eg.charger(); h = bl.Heuristique()\nstats=collecti … [1307 caractères tronqués]`

  ```
FN GV total 180
## chev_droite 75
    [('r019', 'fr', 'souffle'), ('r023', 'en', 'love'), ('r030', 'en', 'come'), ('r039', 'en', 'blows'), ('r049', 'fr', 'dort'), ('r051', 'fr', 'roule')]
## avale_GN 51
    [('r004', 'fr', 'brille'), ('r046', 'fr', 'boit'), ('r047', 'fr', 'poussent'), ('r081', 'fr', 'apporte'), ('r088', 'fr', 'grimpe'), ('r089', 'fr', 'adoucit')]
## chev_deux 28
    [('g014', 'fr', 'vu'), ('r010', 'fr', 'viens'), ('r056', 'fr', 'arrivent'), ('r252', 'fr', 'lit'), ('r310', 'fr', 'dois partir'), ('r314', 'en', 'come')]
## tronque 19
    [('s026', 'fr', 'ne écoute pas'), ('s027', 'fr', 'marche avec il'), ('s049', 'fr', 'ouvre le cheval'), ('s051', 'fr', 'cherche ma lettre'), ('s063', 'fr', 'ne prépare pas'), ('s066', 'fr', 'ne trouve pas')]
## chev_gauche 7
    [('r035', 'en', 'is out'), ('r252', 'fr', 'écrit'), ('r277', 'en', 'writes'), ('s029', 'fr', 'ne commence pas'), ('s094', 'fr', 'ne prépare pas'), ('s095', 'fr', 'ne écoute pas')]
  ```

