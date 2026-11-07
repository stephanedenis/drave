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

### 🤖 Assistant

⏵ Comparaison S/chunker sur le cas français jumeau (g005)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nfor txt in [\"Elle a dit qu'elle viendrait hier.\", \"She said that she wou … [745 caractères tronqués]`

  ```
=== Elle a dit qu'elle viendrait hier.
mots [(0, 4, 'Elle', 'mot'), (5, 6, 'a', 'mot'), (7, 10, 'dit', 'mot'), (11, 18, "qu'elle", 'mot'), (19, 28, 'viendrait', 'mot'), (29, 33, 'hier', 'mot'), (33, 34, '.', 'ponctuation')]
POS [('Elle', 'PRON'), ('a', 'PREP'), ('dit', 'VERB'), ("qu'elle", 'PRON'), ('viendrait', 'VERB'), ('hier', 'ADV'), ('.', 'PONCT')]
simples [('GN', 0, 4, 'Elle'), ('GV', 5, 10, 'a dit'), ('SUB', 11, 33, "qu'elle viendrait hier")]
S [('GV', 0, 10, 'Elle a dit'), ('SUB', 11, 28, "qu'elle viendrait"), ('GP', 29, 33, 'hier')]
out [('GN', 0, 4, 'Elle', 0.3, True), ('GV', 0, 10, 'Elle a dit', 0.55, None), ('GV', 5, 10, 'a dit', 0.3, True), ('SUB', 11, 28, "qu'elle viendrait", 0.55, None), ('SUB', 11, 33, "qu'elle viendrait hier", 0.3, True), ('GP', 29, 33, 'hier', 0.55, None)]
=== She said that she would come yesterday.
mots [(0, 3, 'She', 'mot'), (4, 8, 'said', 'mot'), (9, 13, 'that', 'mot'), (14, 17, 'she', 'mot'), (18, 23, 'would', 'mot'), (24, 28, 'come', 'mot'), (29, 38, 'yesterday', 'mot'), (38, 39, '.', 'ponctuation')]
POS [('She', 'PRON'), ('said', 'VERB'), ('that', 'CONJ'), ('she', 'PRON'), ('would', 'AUX'), ('come', 'VERB'), ('yesterday', 'ADV'), ('.', 'PONC
… [298 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Analyse de la convention du gold sur les frontières GV/SUB

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\nph=eg.charger(); h=bl.Heuristique()\nlastpos=collection … [984 caractères tronqués]`

  ```
--- dernier POS du segment gold ---
('GV', 'ADJ') 27
('GV', 'ADV') 39
('GV', 'AUX') 47
('GV', 'NOUN') 8
('GV', 'PRON') 4
('GV', 'VERB') 587
('REL', 'ADJ') 2
('REL', 'ADV') 2
('REL', 'NOUN') 2
('REL', 'PREP') 1
('REL', 'VERB') 67
('SUB', 'ADJ') 11
('SUB', 'ADV') 6
('SUB', 'NOUN') 2
('SUB', 'VERB') 51
--- premier POS après le segment ---
('GV', 'ADJ') 35
('GV', 'ADV') 26
('GV', 'CONJ') 49
('GV', 'DET') 112
('GV', 'NOUN') 21
('GV', 'PONCT') 7
('GV', 'PREP') 98
('GV', 'PRON') 77
('REL', 'AUX') 53
('REL', 'VERB') 21
('SUB', 'ADV') 2
('SUB', 'PONCT') 1
('SUB', 'PRON') 24
('SUB', 'VERB') 2
--- segments gold contenant un ADV --- {'GV': 45, 'SUB': 8, 'REL': 2}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport evaluer_gold as eg\nph=eg.charger()\nprint('=== GV suivis d un ADV (26) ===')\nfor p in ph:\n    toks=p['mo … [947 caractères tronqués]`

  ```
=== GV suivis d un ADV (26) ===
 g010  GV='Viens' | après='ici' | Viens ici !
 r010  GV='viens' | après='demain' | Tu viens demain ?
 r019  GV='souffle' | après='fort' | Le vent souffle fort.
 r030  GV='come' | après='tomorrow' | You come tomorrow?
 r039  GV='blows' | après='hard' | The wind blows hard.
 r049  GV='dort' | après='profondément' | Le bébé dort profondément.
 r051  GV='roule' | après='vite' | La voiture roule vite.
 r056  GV='arrivent' | après='demain' | Ils arrivent demain matin.
 r069  GV='sleeps' | après='deeply' | The baby sleeps deeply.
 r071  GV='drives' | après='fast' | The car drives fast.
 r076  GV='arrive' | après='tomorrow' | They arrive tomorrow morning.
 r106  GV='laugh' | après='loudly' | The children laugh loudly.
 r235  GV='est' | après='loin' | L'endroit où nous allons est loin.
 r250  GV='is' | après='far' | The place where we go is far.
 r269  GV='est' | après='là' | La personne dont je parle est là.
 r293  GV='is' | après='here' | The person whom I mention is here.
 r310  GV='dois partir' | après='maintenant' | Je dois partir maintenant.
 r314  GV='come' | après='tomorrow' | Do you come tomorrow?
 r320  GV='must leave' | après='now' | I must leave n
… [1346 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mise en place du banc de simulation (copie /tmp, patchs textuels)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport zlib\nfor i in ('r035','g017','g005','r264','r288','r010','r030','r049','r069','r071','r076','r019','r023','r039','r065','r066','r106'):\n    print(i, 'test' if zlib.crc32(i.encode())%3==0 else 'dev')\nEOF", … [55 caractères tronqués]`

  ```
r035 dev
g017 dev
g005 dev
r264 test
r288 test
r010 dev
r030 test
r049 dev
r069 dev
r071 test
r076 dev
r019 dev
r023 test
r039 dev
r065 dev
r066 dev
r106 dev
  ```

### 🤖 Assistant

⏵ Vérification du cas « GN avale le verbe » (r004)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\nh=bl.Heuristique()\nfor p in eg.charger():\n    if p['id'] in ('r004 … [565 caractères tronqués]`

  ```
=== r004 Le soleil brille.
 POS [('Le', 'DET'), ('soleil', 'NOUN'), ('brille', 'NOUN'), ('.', 'PONCT')]
 simples [('GN', 0, 16, 'Le soleil brille')]
 gold [('GN', 'Le soleil'), ('GV', 'brille')]
 out [('GN', 'Le soleil brille')]
=== r046 Le chat boit du lait.
 POS [('Le', 'DET'), ('chat', 'NOUN'), ('boit', 'NOUN'), ('du', 'PREP'), ('lait', 'NOUN'), ('.', 'PONCT')]
 simples [('GN', 0, 12, 'Le chat boit'), ('GP', 13, 20, 'du lait')]
 gold [('GN', 'Le chat'), ('GV', 'boit'), ('GN', 'du lait')]
 out [('GN', 'Le chat boit'), ('GP', 'du lait')]
=== r047 Les fleurs poussent dans le jardin.
 POS [('Les', 'DET'), ('fleurs', 'NOUN'), ('poussent', 'NOUN'), ('dans', 'PREP'), ('le', 'DET'), ('jardin', 'NOUN'), ('.', 'PONCT')]
 simples [('GN', 0, 19, 'Les fleurs poussent'), ('GP', 20, 34, 'dans le jardin')]
 gold [('GN', 'Les fleurs'), ('GV', 'poussent'), ('GP', 'dans le jardin')]
 out [('GN', 'Les fleurs poussent'), ('GP', 'dans le jardin')]
=== r081 Le facteur apporte une lettre.
 POS [('Le', 'DET'), ('facteur', 'NOUN'), ('apporte', 'NOUN'), ('une', 'DET'), ('lettre', 'NOUN'), ('.', 'PONCT')]
 simples [('GN', 0, 29, 'Le facteur apporte une lettre')]
 gold [('GN', 'Le facteur'), ('GV', 'apporte
… [72 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Banc de mesure : variantes patchées en /tmp et métriques dev/test

- **write** `{"file_path": "/tmp/seg/measure.py", "content": "\"\"\"Mesure une variante de bloc_linguistique (copie patchée en /tmp/seg/variants/<nom>).\"\"\"\nimport json\nimport pathlib\nimport sys\n\nREPO = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nVAR = pathlib.Path(sys.argv[1])\nsys … [1443 caractères tronqués]`

  ```
<path>/tmp/seg/measure.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "\"\"\"Construit les variantes patchées de bloc_linguistique.py et mesure chacune.\n\nChaque variante = copie du fichier du dépôt + patchs textuels exacts (old→new), appliqués\nune seule fois chacun. Le module de la variante est importé dans un sous-processus (pas de\ncache de module), e … [12267 caractères tronqués]`

  ```
<path>/tmp/seg/variantes.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def _pos\\b\" -A 30 tools/bloc_linguistique.py", "description": "Read _pos method"}`

  ```
855:    def _pos(self, langue: str, mot: str) -> tuple[str, bool, float]:
856-        lex = POS_FERME.get(langue, POS_FERME["fr"])
857-        n = _normaliser(mot).split("'")[0].split("’")[0]
858-        # élision : « j' » → « je », « l' » → « le », « qu' » → « que » (10 tokens sans POS)
859-        _ELISIONS = {"j": "je", "l": "le", "d": "de", "qu": "que", "n": "ne",
860-                     "s": "se", "c": "ce", "m": "me", "t": "te"}
861-        n = _ELISIONS.get(n, n)
862-        # les **nombres** ont une classe (l'audit produit : 45 nombres sans POS)
863-        if re.fullmatch(r"\d+(?:[.,]\d+)*", n):
864-            return "NUM", False, 0.9
865-        for classe, mots in lex.items():
866-            if n in mots:
867-                return classe, False, 0.92
868-        if n in VERBES.get(langue, VERBES["fr"]):
869-            return "VERB", True, 0.72
870-        if n in ADJECTIFS.get(langue, ADJECTIFS["fr"]):
871-            return "ADJ", True, 0.68
872-        if re.fullmatch(r"\d+(?:[.,]\d+)*", mot):
873-            return "NUM", False, 0.95
874-        if mot[:1].isupper() and mot[1:].islower() and mot not in {"Le", "La", "Les", "Un", "Une", "The"}:
875-            retu
… [591 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('measure.py'); t=p.read_text()\nt=t.replace('h = bl.Heuristique()','part = sys.argv[2] if len(sys.argv) > 2 else \"alternative\"\\nh = bl.Heuristique(partition=part)')\nt=t.replace('sortie = {\"variante\": VAR.name,','sort … [151 caractères tronqués]`

  ```
"""Mesure une variante de bloc_linguistique (copie patchée en /tmp/seg/variants/<nom>)."""
import json
import pathlib
import sys

REPO = pathlib.Path("/home/stephane/Data13TB/stephane/GitHub/Qtrinet")
VAR = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(VAR / "tools"))
sys.path.insert(0, str(REPO / "tools/tests/linguistique"))

import bloc_linguistique as bl  # noqa: E402
import evaluer_gold as eg  # noqa: E402
from gold_split import dev, test  # noqa: E402

assert str(bl.__file__).startswith(str(VAR)), bl.__file__

phrases = eg.charger()
part = sys.argv[2] if len(sys.argv) > 2 else "alternative"
h = bl.Heuristique(partition=part)
sortie = {"variante": VAR.name, "partition": part, "module": str(bl.__file__), "mesures": {}, "phrases": {}}
for nom, ps in [("all", phrases), ("dev", dev(phrases)), ("test", test(phrases))]:
    r = eg.evaluer_bloc(nom, h, ps)
    s, a, t = r["syntagme"], r[
  ```

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('variantes.py'); t=p.read_text()\n# 1) retirer la variante cassee\nt=t.replace('    \"g017_G1_sans_const\": [(G1_OLD, G1_NEW)],\\n','')\n# 2) G-A : _pos_mot + garde AUX\nt=t.replace('''                       # le GV ne pre … [2312 caractères tronqués]`

  ```
ok
base                     all 0.7533 (P 0.7239 R 0.7853 tp 1463 fp 558 fn 400) dev 0.7476 test 0.7663 att 236/237
r035_P1                  all 0.7537 (P 0.7240 R 0.7858 tp 1464 fp 558 fn 399) dev 0.7480 test 0.7663 att 236/237
r035_P1P2                all 0.7549 (P 0.7254 R 0.7869 tp 1466 fp 555 fn 397) dev 0.7498 test 0.7663 att 237/238
r035_P2                  all 0.7533 (P 0.7239 R 0.7853 tp 1463 fp 558 fn 400) dev 0.7476 test 0.7663 att 236/237
g017_G1                  all 0.7541 (P 0.7248 R 0.7858 tp 1464 fp 556 fn 399) dev 0.7486 test 0.7663 att 237/238
gv_A_objet               all 0.7531 (P 0.7202 R 0.7890 tp 1470 fp 571 fn 393) dev 0.7450 test 0.7711 att 236/237
gv_B_adverbe             all 0.7559 (P 0.7264 R 0.7880 tp 1468 fp 553 fn 395) dev 0.7498 test 0.7696 att 236/237
gv_C_prep                all 0.7533 (P 0.7239 R 0.7853 tp 1463 fp 558 fn 400) dev 0.7476 test 0.7663 att 236/237
gv_E_pos                 all 0.7832 (P 0.7369 R 0.8357 tp 1557 fp 556 fn 306) dev 0.7802 test 0.7899 att 236/237
  ```

### 🤖 Assistant

⏵ Analyse des différences phrase à phrase pour chaque règle

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport json, pathlib, sys, collections\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique')\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nimport evaluer_gold as eg\nph={p['id']:p f … [1060 caractères tronqués]`

  ```
==================== r035_P1 0.7537 dev 0.748 test 0.7663
 gains nets {'GN': 1}  pertes nettes {'GN': 1}
   + r035 ('GN', 0, 8) | The film she talks about is out.
   - r035 ('GN', 9, 12) | The film she talks about is out.
==================== r035_P1P2 0.7549 dev 0.7498 test 0.7663
 gains nets {'GV': 1, 'GN': 1, 'REL': 1}  pertes nettes {}
   + r035 ('GV', 25, 31) | The film she talks about is out.
   + r035 ('GN', 0, 8) | The film she talks about is out.
   + r035 ('REL', 9, 24) | The film she talks about is out.
==================== g017_G1 0.7541 dev 0.7486 test 0.7663
 gains nets {'SUB': 1}  pertes nettes {}
   + g017 ('SUB', 9, 28) | She said that she would come yesterday.
==================== gv_A_objet 0.7531 dev 0.745 test 0.7711
 gains nets {'GV': 24}  pertes nettes {'GV': 42}
   + r023 ('GV', 3, 7) | We love music.
   + r051 ('GV', 11, 16) | La voiture roule vite.
   + r065 ('GV', 4, 11) | She watches television.
   + r066 ('GV', 8, 14) | The cat drinks milk.
   + r071 ('GV', 8, 14) | The car drives fast.
   + r105 ('GV', 10, 15) | The baker sells bread.
   + r109 ('GV', 6, 13) | Music softens manners.
   + r151 ('GV', 13, 19) | The gardener plants flowers.
   - g014 ('GV
… [1793 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport evaluer_gold as eg\nfor p in eg.charger():\n    if p['id'] in ('r190','r314','r418','r422','r010','r030','r310','r320',' … [262 caractères tronqués]`

  ```
r010 Tu viens demain ?
   gold [('GN', 'Tu'), ('GV', 'viens')]
   mots [('Tu', 'PRON'), ('viens', 'VERB'), ('demain', 'ADV')]
r030 You come tomorrow?
   gold [('GN', 'You'), ('GV', 'come')]
   mots [('You', 'PRON'), ('come', 'VERB'), ('tomorrow', 'ADV')]
r190 Ils arrivent demain.
   gold [('GN', 'Ils'), ('GV', 'arrivent demain')]
   mots [('Ils', 'PRON'), ('arrivent', 'VERB'), ('demain', 'ADV')]
r310 Je dois partir maintenant.
   gold [('GN', 'Je'), ('GV', 'dois partir'), ('ADV', 'maintenant')]
   mots [('Je', 'PRON'), ('dois', 'VERB'), ('partir', 'VERB'), ('maintenant', 'ADV')]
r314 Do you come tomorrow?
   gold [('GN', 'you'), ('GV', 'come'), ('ADV', 'tomorrow')]
   mots [('Do', 'AUX'), ('you', 'PRON'), ('come', 'VERB'), ('tomorrow', 'ADV')]
r320 I must leave now.
   gold [('GN', 'I'), ('GV', 'must leave'), ('ADV', 'now')]
   mots [('I', 'PRON'), ('must', 'AUX'), ('leave', 'VERB'), ('now', 'ADV')]
r423 Tu viens demain.
   gold [('GN', 'Tu'), ('GV', 'viens'), ('ADV', 'demain'), ('PONCT', '.')]
   mots [('Tu', 'PRON'), ('viens', 'VERB'), ('demain', 'ADV'), ('.', 'PONCT')]
r427 You come tomorrow.
   gold [('GN', 'You'), ('GV', 'come'), ('ADV', 'tomorrow'), ('PONCT', '.')]
   mots [(
… [505 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('variantes.py'); t=p.read_text()\nadd = '''\n# G-E2 : comme G-E mais le NOUN candidat doit suivre immédiatement le premier NOM\n# du GN (prevprev DET/ADJ/NUM) — évite « La cloche sonne | midi » (r135)\nGE2_OLD = GE_OLD\nGE … [2290 caractères tronqués]`

  ```
ok
gv_E_pos2                all 0.7836 (P 0.7376 R 0.8357 tp 1557 fp 554 fn 306) dev 0.7802 test 0.7912 att 236/237
gv_E_pos3                all 0.7663 (P 0.7296 R 0.8068 tp 1503 fp 557 fn 360) dev 0.7608 test 0.7785 att 236/237
comb_g017_E2             all 0.7843 (P 0.7384 R 0.8363 tp 1558 fp 552 fn 305) dev 0.7812 test 0.7912 att 237/238
comb_g017_GB_E2          all 0.7868 (P 0.7408 R 0.8390 tp 1563 fp 547 fn 300) dev 0.7834 test 0.7944 att 237/238
comb_r035_g017           all 0.7556 (P 0.7262 R 0.7874 tp 1467 fp 553 fn 396) dev 0.7508 test 0.7663 att 238/239
comb_tout                all 0.7883 (P 0.7422 R 0.8406 tp 1566 fp 544 fn 297) dev 0.7856 test 0.7944 att 238/239
  ```

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('measure.py'); t=p.read_text()\nt=t.replace('''        \"att_exact_any\": a[\"exact_any\"],''','''        \"att_exact_any\": a[\"exact_any\"],\n        \"pos\": r[\"pos\"][\"exactitude\"], \"pos_ferme\": r[\"pos\"][\"exact … [1236 caractères tronqués]`

  ```
ok
base                     all 0.7533 (P 0.7239 R 0.7853 tp 1463 fp 558 fn 400) dev 0.7476 test 0.7663 att 236/237
gv_E_pos                 all 0.7832 (P 0.7369 R 0.8357 tp 1557 fp 556 fn 306) dev 0.7802 test 0.7899 att 236/237
gv_E_pos2                all 0.7836 (P 0.7376 R 0.8357 tp 1557 fp 554 fn 306) dev 0.7802 test 0.7912 att 236/237
comb_tout                all 0.7883 (P 0.7422 R 0.8406 tp 1566 fp 544 fn 297) dev 0.7856 test 0.7944 att 238/239
  ```

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport json,pathlib\nR=json.loads(pathlib.Path('resultats.json').read_text())\nfor k in ('base','gv_E_pos2','comb_tout'):\n    m=R[k]['mesures']\n    print(k)\n    for s in ('all','dev','test','hand','reel','synthetique','fr','en'):\n        d=m[s]\n    … [170 caractères tronqués]`

  ```
base
  all          f1 0.7533 tp 1463 fp 558 fn 400 pos 0.8625
  dev          f1 0.7476 tp 1004 fp 386 fn 292 pos 0.8618
  test         f1 0.7663 tp 459 fp 172 fn 108 pos 0.8642
  hand         f1 0.8571 tp 54 fp 16 fn 2 pos None
  reel         f1 0.7483 tp 1088 fp 375 fn 357 pos None
  synthetique  f1 0.7553 tp 321 fp 167 fn 41 pos None
  fr           f1 0.698 tp 883 fp 486 fn 278 pos None
  en           f1 0.8567 tp 580 fp 72 fn 122 pos None
gv_E_pos2
  all          f1 0.7836 tp 1557 fp 554 fn 306 pos 0.8871
  dev          f1 0.7802 tp 1074 fp 383 fn 222 pos 0.887
  test         f1 0.7912 tp 483 fp 171 fn 84 pos 0.8873
  hand         f1 0.8571 tp 54 fp 16 fn 2 pos None
  reel         f1 0.7885 tp 1182 fp 371 fn 263 pos None
  synthetique  f1 0.7553 tp 321 fp 167 fn 41 pos None
  fr           f1 0.7424 tp 971 fp 484 fn 190 pos None
  en           f1 0.863 tp 586 fp 70 fn 116 pos None
comb_tout
  all          f1 0.7883 tp 1566 fp 544 fn 297 pos 0.8871
  dev          f1 0.7856 tp 1081 fp 375 fn 215 pos 0.887
  test         f1 0.7944 tp 485 fp 169 fn 82 pos 0.8873
  hand         f1 0.88 tp 55 fp 14 fn 1 pos None
  reel         f1 0.7939 tp 1190 fp 363 fn 255 pos None
  synthetique  f1
… [145 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport json, pathlib, sys, collections\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique')\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nimport evaluer_gold as eg\nph={p['id']:p f … [1029 caractères tronqués]`

  ```
E2 gains {'GN': 56, 'GV': 38} pertes {}
exemples de gains (10):
   r004 ('GN', 0, 9) | Le soleil brille. | gold: [('GN', 'Le soleil'), ('GV', 'brille')]
   r004 ('GV', 10, 16) | Le soleil brille. | gold: [('GN', 'Le soleil'), ('GV', 'brille')]
   r046 ('GV', 8, 12) | Le chat boit du lait. | gold: [('GN', 'Le chat'), ('GV', 'boit'), ('GN', 'du lait')]
   r046 ('GN', 0, 7) | Le chat boit du lait. | gold: [('GN', 'Le chat'), ('GV', 'boit'), ('GN', 'du lait')]
   r047 ('GN', 0, 10) | Les fleurs poussent dans le jardin. | gold: [('GN', 'Les fleurs'), ('GV', 'poussent'), ('GP', 'dans le jardin')]
   r047 ('GV', 11, 19) | Les fleurs poussent dans le jardin. | gold: [('GN', 'Les fleurs'), ('GV', 'poussent'), ('GP', 'dans le jardin')]
   r081 ('GN', 0, 10) | Le facteur apporte une lettre. | gold: [('GN', 'Le facteur'), ('GV', 'apporte'), ('GN', 'une lettre')]
   r081 ('GV', 11, 18) | Le facteur apporte une lettre. | gold: [('GN', 'Le facteur'), ('GV', 'apporte'), ('GN', 'une lettre')]
   r081 ('GN', 19, 29) | Le facteur apporte une lettre. | gold: [('GN', 'Le facteur'), ('GV', 'apporte'), ('GN', 'une lettre')]
   r088 ('GV', 8, 14) | Le chat grimpe sur le toit. | gold: [('GN', 'Le chat'), (
… [385 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle négatif (condition inversée) et modes de partition

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('variantes.py'); t=p.read_text()\nadd='''\n# placebo : le **même** déclencheur, mais une frontière qui n'en est pas une\nGPL_OLD = GE2_OLD\nGPL_NEW = GE2_NEW.replace('_su.type in (\"PONCT\", \"PREP\", \"DET\")', '_su.type  … [890 caractères tronqués]`

  ```
gv_E_pos2                all 0.7836 (P 0.7376 R 0.8357 tp 1557 fp 554 fn 306) dev 0.7802 test 0.7912 att 236/237
placebo_E2               all 0.7389 (P 0.7032 R 0.7783 tp 1450 fp 612 fn 413) dev 0.7359 test 0.7455 att 231/232
base                     all 0.7533 (P 0.7239 R 0.7853 tp 1463 fp 558 fn 400) dev 0.7476 test 0.7663 att 236/237
--- partition filtrer_union
all 0.8044 tp 1456 fp 301 fn 407 att 230 / 231 couv 0.9665
dev 0.7982 tp 999 fp 208 fn 297 att 155 / 156 couv 0.9571
test 0.8183 tp 457 fp 93 fn 110 att 75 / 75 couv 0.9868
--- partition filtrer
all 0.8104 tp 1440 fp 251 fn 423 att 222 / 223 couv 0.9331
dev 0.8003 tp 984 fp 179 fn 312 att 148 / 149 couv 0.9141
test 0.8329 tp 456 fp 72 fn 111 att 74 / 74 couv 0.9737
--- partition brut
all 0.7533 tp 1463 fp 558 fn 400 att 236 / 237 couv 0.9916
dev 0.7476 tp 1004 fp 386 fn 292 att 160 / 161 couv 0.9877
test 0.7663 tp 459 fp 172 fn 108 att 76 / 76 couv 1.0
  ```

### 🤖 Assistant

⏵ Re-mesure complète de toutes les variantes avec POS/sources

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('variantes.py'); t=p.read_text()\nt=t.replace('''    \"comb_r035_g017\": [''','''    \"comb_r035_g017_E2\": [(P1_OLD, P1_NEW), (P2_OLD, P2_NEW), (CONST_OLD, CONST_NEW), (G1_OLD, G1_NEW), (GE2_OLD, GE2_NEW)],\n    \"comb_r0 … [306 caractères tronqués]`

  ```
base                     all 0.7533 (P 0.7239 R 0.7853 tp 1463 fp 558 fn 400) dev 0.7476 test 0.7663 att 236/237
r035_P1                  all 0.7537 (P 0.7240 R 0.7858 tp 1464 fp 558 fn 399) dev 0.7480 test 0.7663 att 236/237
r035_P1P2                all 0.7549 (P 0.7254 R 0.7869 tp 1466 fp 555 fn 397) dev 0.7498 test 0.7663 att 237/238
r035_P2                  all 0.7533 (P 0.7239 R 0.7853 tp 1463 fp 558 fn 400) dev 0.7476 test 0.7663 att 236/237
r035_P1_P3               all 0.7537 (P 0.7240 R 0.7858 tp 1464 fp 558 fn 399) dev 0.7480 test 0.7663 att 236/237
g017_G1                  all 0.7541 (P 0.7248 R 0.7858 tp 1464 fp 556 fn 399) dev 0.7486 test 0.7663 att 237/238
gv_A_objet               all 0.7531 (P 0.7202 R 0.7890 tp 1470 fp 571 fn 393) dev 0.7450 test 0.7711 att 236/237
gv_B_adverbe             all 0.7559 (P 0.7264 R 0.7880 tp 1468 fp 553 fn 395) dev 0.7498 test 0.7696 att 236/237
gv_A_B                   all 0.7551 (P 0.7222 R 0.7912 tp 1474 fp 567 fn 389) dev 0.7472 test 0.7728 att 236/237
gv_C_prep                all 0.7533 (P 0.7239 R 0.7853 tp 1463 fp 558 fn 400) dev 0.7476 test 0.7663 att 236/237
gv_E_pos                 all 0.7832 (P 0.7369 R 0.8357 tp 1557 fp 556 
… [1059 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Tableau final : erreurs GV par règle et par classe

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport json, pathlib, sys, collections\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique')\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nimport evaluer_gold as eg\nph={p['id']:p f … [1064 caractères tronqués]`

  ```
variante                    F1     dev    test     POS  GVfp  GVfn      att    couv
base                    0.7533  0.7476  0.7663  0.8625   322   180 236/237    0.9916
r035_P1                 0.7537  0.7480  0.7663  0.8625   322   180 236/237    0.9916
r035_P1P2               0.7549  0.7498  0.7663  0.8625   320   179 237/238    0.9958
g017_G1                 0.7541  0.7486  0.7663  0.8625   322   180 237/238    0.9958
gv_B_adverbe            0.7559  0.7498  0.7696  0.8625   317   175 236/237    0.9916
gv_E_pos2               0.7836  0.7802  0.7912  0.8871   322   142 236/237    0.9916
gv_E_pos3               0.7663  0.7608  0.7785  0.8795   322   160 236/237    0.9916
placebo_E2              0.7389  0.7359  0.7455  0.8566   347   184 231/232    0.9707
gv_A_objet              0.7531  0.7450  0.7711  0.8625   335   173 236/237    0.9916
gv_A_B                  0.7551  0.7472  0.7728  0.8625   331   169 236/237    0.9916
gv_C_prep               0.7533  0.7476  0.7663  0.8625   321   180 236/237    0.9916
gv_E_pos                0.7832  0.7802  0.7899  0.8915   323   142 236/237    0.9916
comb_r035_g017          0.7556  0.7508  0.7663  0.8625   320   179 238/239    1.0000
comb_E2_GB 
… [328 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Génération des diffs exacts par règle et du diff combiné

- **bash** `{"command": "cd /tmp/seg && for v in r035_P1 r035_P1P2 g017_G1 gv_B_adverbe gv_E_pos2 gv_A_objet gv_C_prep placebo_E2 comb_tout; do\n  echo \"########## $v\"\n  diff -u /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py variants/$v/tools/bloc_linguistique.py | sed -e '1s|.*|- … [206 caractères tronqués]`

  ```
377 diffs.txt
9
  ```

- **bash** `{"command": "cd /tmp/seg && sed -n '1,120p' diffs.txt", "description": "Inspect first diffs"}`

  ```
########## r035_P1
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -1217,7 +1217,16 @@
                        and _normaliser(mots[j][2]) not in lex.get("PREP", set()) | lex.get("CONJ", set()) | lex.get("AUX", set())
                        and _normaliser(mots[j][2]) not in RELATIFS
                        and not est_sub(_normaliser(mots[j][2]))
-                       and (j == i + 1 or not est_verbe(mots[j][0], mots[j][2]))):
+                       and (j == i + 1 or not est_verbe(mots[j][0], mots[j][2]))
+                       # le GN ne traverse pas un **pronom sujet** devant un verbe :
+                       # « The film | she talks about » (relative zéro, r035)
+                       and not (j > i + 1
+                                and _normaliser(mots[j][2]) in (
+                                    SUJETS if langue == "fr"
+                                    else {"i", "you", "he", "she", "it", "we", "they"})
+                                and j + 1 < len(mots)
+                                and (est_verbe(mots[j + 1][0], mots[j + 1][2])
+                                     or _normaliser(mots[j + 1][2]) in lex.get("AUX", set())))):
    
… [6110 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Correction de robustesse du patch g017 (segments vide) et re-mesure

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('variantes.py'); t=p.read_text()\nt=t.replace('''def _derniere_tete(segment: dict, texte: str) -> str:\n    \"\"\"Le dernier mot du segment précédent (le gouverneur probable d'une SUB).\"\"\"\n    mots = re.findall(r\"[\\\ … [884 caractères tronqués]`

  ```
True True
base                     all 0.7533 (P 0.7239 R 0.7853 tp 1463 fp 558 fn 400) dev 0.7476 test 0.7663 att 236/237
r035_P1                  all 0.7537 (P 0.7240 R 0.7858 tp 1464 fp 558 fn 399) dev 0.7480 test 0.7663 att 236/237
r035_P1P2                all 0.7549 (P 0.7254 R 0.7869 tp 1466 fp 555 fn 397) dev 0.7498 test 0.7663 att 237/238
r035_P2                  all 0.7533 (P 0.7239 R 0.7853 tp 1463 fp 558 fn 400) dev 0.7476 test 0.7663 att 236/237
r035_P1_P3               all 0.7537 (P 0.7240 R 0.7858 tp 1464 fp 558 fn 399) dev 0.7480 test 0.7663 att 236/237
g017_G1                  all 0.7541 (P 0.7248 R 0.7858 tp 1464 fp 556 fn 399) dev 0.7486 test 0.7663 att 237/238
gv_A_objet               all 0.7531 (P 0.7202 R 0.7890 tp 1470 fp 571 fn 393) dev 0.7450 test 0.7711 att 236/237
gv_B_adverbe             all 0.7559 (P 0.7264 R 0.7880 tp 1468 fp 553 fn 395) dev 0.7498 test 0.7696 att 236/237
gv_A_B                   all 0.7551 (P 0.7222 R 0.7912 tp 1474 fp 567 fn 389) dev 0.7472 test 0.7728 att 236/237
gv_C_prep                all 0.7533 (P 0.7239 R 0.7853 tp 1463 fp 558 fn 400) dev 0.7476 test 0.7663 att 236/237
gv_E_pos                 all 0.7832 (P 0.7369 R 0.8357 tp 15
… [1069 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Classification finale et effectifs pour la fiche

- **bash** `{"command": "cd /tmp/seg && cat > classer.py <<'EOF'\n\"\"\"Classe les erreurs GV (FP/FN) du gold 612, sur une variante donnée.\"\"\"\nimport collections\nimport json\nimport pathlib\nimport sys\n\nREPO = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nVAR = pathlib.Path(sys.argv[ … [4277 caractères tronqués]`

  ```
== base FP 322 {'objet': 73, 'gauche_autre': 150, 'adverbe': 16, 'tronque': 39, 'parasite': 17, 'deux_cotes': 27} | FN 180 {'chev_deux': 28, 'avale_GN': 51, 'chev_droite': 75, 'chev_gauche': 7, 'tronque': 19}
   double 153 {'objet': 4, 'gauche_autre': 136, 'adverbe': 1, 'tronque': 11, 'deux_cotes': 1} | origine {'chunker': 98, 'S': 224}
== comb_tout FP 315 {'objet': 73, 'gauche_autre': 151, 'adverbe': 10, 'tronque': 40, 'parasite': 16, 'deux_cotes': 25} | FN 136 {'chev_deux': 23, 'chev_droite': 72, 'avale_GN': 13, 'chev_gauche': 9, 'tronque': 19}
   double 155 {'objet': 4, 'gauche_autre': 138, 'adverbe': 1, 'tronque': 11, 'deux_cotes': 1} | origine {'chunker': 91, 'S': 224}
  ```

- **bash** `{"command": "cd /tmp/seg && sed -i 's/dans_gn = any(g\\[0\\] <= d and g\\[1\\] >= gd for g in gn_gold)/dans_gn = any(g[0] >= d and g[1] <= gd and g[1] > g[0] for g in gn_gold)/' classer.py && python3 classer.py /tmp/seg/variants/base > class_base.json && python3 classer.py /tmp/seg/variants/comb_tou … [375 caractères tronqués]`

  ```
== base FP 322 {'objet': 73, 'sujet': 144, 'adverbe': 16, 'tronque': 39, 'parasite': 17, 'gauche_autre': 6, 'deux_cotes': 27} | FN 180 {'chev_deux': 28, 'avale_GN': 51, 'chev_droite': 75, 'chev_gauche': 7, 'tronque': 19}
   double 153 {'objet': 4, 'sujet': 133, 'adverbe': 1, 'tronque': 11, 'deux_cotes': 1, 'gauche_autre': 3} | origine {'chunker': 98, 'S': 224}
== comb_tout FP 315 {'objet': 73, 'sujet': 145, 'adverbe': 10, 'tronque': 40, 'parasite': 16, 'deux_cotes': 25, 'gauche_autre': 6} | FN 136 {'chev_deux': 23, 'chev_droite': 72, 'avale_GN': 13, 'chev_gauche': 9, 'tronque': 19}
   double 155 {'objet': 4, 'sujet': 135, 'adverbe': 1, 'tronque': 11, 'deux_cotes': 1, 'gauche_autre': 3} | origine {'chunker': 91, 'S': 224}
  ```

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport json\nd=json.load(open('class_base.json'))\nfor cat, items in d['exemples'].items():\n    print('##',cat)\n    for e in items: print('   ',e)\nEOF", "description": "Show examples per GV error class"}`

  ```
## objet
    {'id': 'g003', 'span': "a vu l'homme", 'sens': 'fp', 'origine': 'chunker', 'phrase': "La femme a vu l'homme dans le parc."}
    {'id': 'g014', 'span': "vu l'homme", 'sens': 'fp', 'origine': 'chunker', 'phrase': "J'ai vu l'homme avec le télescope."}
    {'id': 'r023', 'span': 'love music', 'sens': 'fp', 'origine': 'chunker', 'phrase': 'We love music.'}
    {'id': 'r056', 'span': 'arrivent demain matin', 'sens': 'fp', 'origine': 'chunker', 'phrase': 'Ils arrivent demain matin.'}
    {'id': 'r065', 'span': 'watches television', 'sens': 'fp', 'origine': 'chunker', 'phrase': 'She watches television.'}
## sujet
    {'id': 'g004', 'span': 'Il a couru', 'sens': 'fp', 'origine': 'S', 'phrase': 'Il a couru pour attraper le bus.'}
    {'id': 'g005', 'span': 'Elle a dit', 'sens': 'fp', 'origine': 'S', 'phrase': "Elle a dit qu'elle viendrait hier."}
    {'id': 'g008', 'span': 'Marie lit', 'sens': 'fp', 'origine': 'S', 'phrase': 'Marie lit un livre.'}
    {'id': 'g009', 'span': 'Il ne dort pas', 'sens': 'fp', 'origine': 'S', 'phrase': 'Il ne dort pas.'}
    {'id': 'g014', 'span': "J'ai vu", 'sens': 'fp', 'origine': 'S', 'phrase': "J'ai vu l'homme avec le télescope."}
## adverbe
    
… [4790 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/seg && cat > croisements.py <<'EOF'\nimport collections, json, pathlib, sys\nREPO = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")\nVAR = pathlib.Path(sys.argv[1])\nsys.path.insert(0, str(VAR / \"tools\")); sys.path.insert(0, str(REPO / \"tools/tests/linguisti … [2716 caractères tronqués]`

  ```
[stderr]
  File "/tmp/seg/croisements.py", line 19
    return [pm.get((m["debut"],m["fin"]),"?"") if False else pm.get((m["debut"],m["fin"]),"?") for m in p["mots"] if d<=m["debut"] and m["fin"]<=f]
                                                                                                                                             ^
SyntaxError: unterminated string literal (detected at line 19)
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('croisements.py'); t=p.read_text()\nimport re\nt=re.sub(r'    def extras\\(d,f\\):\\n.*\\n', '    def extras(d,f):\\n        return [pm.get((m[\"debut\"],m[\"fin\"]),\"?\") for m in p[\"mots\"] if d<=m[\"debut\"] and m[\"f … [144 caractères tronqués]`

  ```
FP par classe×origine: {'adverbe|S': 2, 'adverbe|chunker': 14, 'deux_cotes|S': 21, 'deux_cotes|chunker': 6, 'gauche_autre|S': 3, 'gauche_autre|chunker': 3, 'objet|S': 20, 'objet|chunker': 53, 'parasite|S': 11, 'parasite|chunker': 6, 'sujet|S': 142, 'sujet|chunker': 2, 'tronque|S': 25, 'tronque|chunker': 14}
doublons par classe×origine: {'adverbe|chunker': 1, 'deux_cotes|S': 1, 'gauche_autre|S': 3, 'objet|S': 3, 'objet|chunker': 1, 'sujet|S': 133, 'tronque|S': 10, 'tronque|chunker': 1}
FN: {'chev_deux': 28, 'avale_GN': 51, 'chev_droite': 75, 'chev_gauche': 7, 'tronque': 19}
  ```

### 🤖 Assistant

⏵ Vérification du style des fiches/JSON existants et de la date

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date -I && ls -t reports/*.json | head -5 && echo '---' && python3 -c \"\nimport json,pathlib\np=pathlib.Path('reports/pensee-r264-elision.json'); print(p.read_text()[:1500])\n\"", "description": "Check date and JSON style"}`

  ```
2026-11-07
reports/pensee-gn-pronom-sujet.json
reports/pensee-r264-elision.json
reports/pensee-pos-ponctuation.json
reports/pensee-etat-r.json
reports/pensee-etat-s.json
---
{
 "date": "2026-11-06",
 "ligne": "B13",
 "bug": "GV : endswith(qu) sur le token entier au lieu du radical",
 "avant": {
  "exact": 235,
  "labels": 236,
  "couverture": 0.9874,
  "spans": 3,
  "f1": 0.6482
 },
 "apres": {
  "exact": 236,
  "labels": 237,
  "couverture": 0.9916,
  "spans": 2,
  "f1": 0.6519,
  "pos": 0.8625,
  "dev": "160/161",
  "test": "76/76"
 },
 "spans_restants": [
  "r035 relative zéro",
  "g017 arbitrage d'adverbe"
 ],
 "controles": {
  "autotest": "183/183",
  "assertions": 17
 }
}

[stderr]
ls: write error: Broken pipe
  ```

### 🤖 Assistant

⏵ Extraction du tableau final complet et des diff exacts

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport json,pathlib\nR=json.loads(pathlib.Path('resultats.json').read_text())\nV=('base','r035_P1','r035_P1P2','g017_G1','gv_B_adverbe','gv_E_pos2','gv_E_pos3','gv_A_objet','gv_A_B','gv_C_prep','placebo_E2','comb_r035_g017','comb_E2_GB','comb_g017_E2',' … [778 caractères tronqués]`

  ```
variante                   F1      P      R   tp   fp   fn    POS    dev   test   tete      att   couv
base                   0.7533 0.7239 0.7853 1463  558  400 0.8625 0.7476 0.7663 0.8640 236/237   0.9916
r035_P1                0.7537 0.7240 0.7858 1464  558  399 0.8625 0.7480 0.7663 0.8638 236/237   0.9916
r035_P1P2              0.7549 0.7254 0.7869 1466  555  397 0.8625 0.7498 0.7663 0.8651 237/238   0.9958
g017_G1                0.7541 0.7248 0.7858 1464  556  399 0.8625 0.7486 0.7663 0.8640 237/238   0.9958
gv_B_adverbe           0.7559 0.7264 0.7880 1468  553  395 0.8625 0.7498 0.7696 0.8640 236/237   0.9916
gv_E_pos2              0.7836 0.7376 0.8357 1557  554  306 0.8871 0.7802 0.7912 0.8806 236/237   0.9916
gv_E_pos3              0.7663 0.7296 0.8068 1503  557  360 0.8795 0.7608 0.7785 0.8700 236/237   0.9916
gv_A_objet             0.7531 0.7202 0.7890 1470  571  393 0.8625 0.7450 0.7711 0.8620 236/237   0.9916
gv_A_B                 0.7551 0.7222 0.7912 1474  567  389 0.8625 0.7472 0.7728 0.8620 236/237   0.9916
gv_C_prep              0.7533 0.7239 0.7853 1463  558  400 0.8625 0.7476 0.7663 0.8640 236/237   0.9916
placebo_E2             0.7389 0.7032 0.7783 1450  612  41
… [1033 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"0\\.7535\\|0,7535\\|0\\.7533\\|0,7533\" tools/ reports/pensee-gn-pronom-sujet.json docs/pilotage/en-cours.md 2>/dev/null | head -20", "description": "Search for the headline F1 value in code/tests"}`

  ```
tools/pensee/autotest.py:1732:    return abs(f1 - 0.7535) < 0.001, f"union : segments F1 {f1} (S 0,5988)"
tools/pensee/autotest.py:1744:    return abs(f1 - 0.7535) < 0.001 and abs(tete - 0.865) < 0.001, (
tools/pensee/autotest.py:1758:    return (abs(f1 - 0.7535) < 0.001 and abs(tete - 0.865) < 0.001
reports/pensee-gn-pronom-sujet.json:15:  "f1": 0.7535,
reports/pensee-gn-pronom-sujet.json:34: "gain_total": "0,6519 → 0,7535 (+10,2 pts)"
docs/pilotage/en-cours.md:71:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 236/237 (0,9916)**, **F1 0,7535** (linéaire 0,8104), **2 spans** ; **contrat v1** validé ; frontières, partition, GN du sujet ; **`drave` v0**.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1700,1775p' tools/pensee/autotest.py", "description": "Read autotest assertions around F1 0.7535"}`

  ```
a1 = h1.analyser(phrase["texte"], phrase["langue"])
        a2 = h2.analyser(phrase["texte"], phrase["langue"])
        gold = {(s["type"], s["debut"]) for s in phrase["segments"]}
        seg_s = [(e.type, e.debut, e.fin) for e in a1.etiquettes if e.niveau == "syntagme"]
        seg_c = [(e.type, e.debut, e.fin) for e in a2.etiquettes if e.niveau == "syntagme"]
        pred = set()
        for (t, d, f) in seg_s:
            cand = [cd for (ct, cd, cf) in seg_c if ct == t and d <= cd < f]
            pred.add((t, cand[0] if cand else d))
        tp += len(pred & gold); fp += len(pred - gold); fn += len(gold - pred)
    p = tp / max(1, tp + fp); r = tp / max(1, tp + fn); f1 = round(2 * p * r / max(1e-9, p + r), 4)
    return abs(f1 - 0.823) < 0.001, (
        f"hybride : tête F1 {f1} (S 0,3552, chunker 0,4707)")


def t112_union() -> tuple[bool, str]:
    """L'union des segmenteurs : segments F1 0,5595 (S 0,4741)."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger_gele as charger, _seg, _tete
    ph = charger()
    h1 = bl.Heuristique(union=False)
    h2 = bl.Heuristique(union=False)
    h2.segmenter_s = False
    tp = fp = fn = 0

… [2394 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mesure aussi sur le gold gelé 602 (référence officielle des portes)

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('measure.py'); t=p.read_text()\nt=t.replace('''for nom, ps in [(\"all\", phrases), (\"dev\", dev(phrases)), (\"test\", test(phrases))]:''',\n'''gele = eg.charger_gele()\nfor nom, ps in [(\"all\", phrases), (\"gele\", gele) … [192 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-4572]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-4572", "wait": true, "timeout_ms": 120000}`

  ```
base                     all 0.7533 (P 0.7239 R 0.7853 tp 1463 fp 558 fn 400) dev 0.7476 test 0.7663 att 236/237
r035_P1                  all 0.7537 (P 0.7240 R 0.7858 tp 1464 fp 558 fn 399) dev 0.7480 test 0.7663 att 236/237
r035_P1P2                all 0.7549 (P 0.7254 R 0.7869 tp 1466 fp 555 fn 397) dev 0.7498 test 0.7663 att 237/238
r035_P2                  all 0.7533 (P 0.7239 R 0.7853 tp 1463 fp 558 fn 400) dev 0.7476 test 0.7663 att 236/237
r035_P1_P3               all 0.7537 (P 0.7240 R 0.7858 tp 1464 fp 558 fn 399) dev 0.7480 test 0.7663 att 236/237
g017_G1                  all 0.7541 (P 0.7248 R 0.7858 tp 1464 fp 556 fn 399) dev 0.7486 test 0.7663 att 237/238
gv_A_objet               all 0.7531 (P 0.7202 R 0.7890 tp 1470 fp 571 fn 393) dev 0.7450 test 0.7711 att 236/237
gv_B_adverbe             all 0.7559 (P 0.7264 R 0.7880 tp 1468 fp 553 fn 395) dev 0.7498 test 0.7696 att 236/237
gv_A_B                   all 0.7551 (P 0.7222 R 0.7912 tp 1474 fp 567 fn 389) dev 0.7472 test 0.7728 att 236/237
gv_C_prep                all 0.7533 (P 0.7239 R 0.7853 tp 1463 fp 558 fn 400) dev 0.7476 test 0.7663 att 236/237
gv_E_pos                 all 0.7832 (P 0.7369 R 0.8357 tp 1557 fp 556 
… [1093 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-4572 (bash: cd /tmp/seg && python3 - <<'EOF'
import pathlib
p=pathlib.Path('measure.py'); t=p.read_text()
t=t.replace('''for nom, ps in [("all", phrases), ("dev", dev(phrases)), ("test", test(phrases))]:''',
'''gele = eg.charger_gele()
for nom, ps in [("all", phrases), ("gele", gele), ("dev", dev(phrases)), ("test", test(phrases))]:''')
p.write_text(t)
EOF
cd /tmp/seg && python3 variantes.py 2>&1 | tail -25) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Extraction des valeurs gelées (référence officielle) par règle

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport json,pathlib\nR=json.loads(pathlib.Path('resultats.json').read_text())\nV=('base','r035_P1','r035_P1P2','g017_G1','gv_B_adverbe','gv_E_pos2','gv_E_pos3','gv_A_objet','gv_A_B','gv_C_prep','placebo_E2','comb_r035_g017','comb_E2_GB','comb_g017_E2',' … [579 caractères tronqués]`

  ```
variante                gelé F1   tp   fp   fn   tete    POS |  viv F1     dev    test      att   couv
base                     0.7535 1440  551  391 0.8650 0.8625 |  0.7533  0.7476  0.7663 232/233   0.9749
r035_P1                  0.7539 1441  551  390 0.8647 0.8625 |  0.7537  0.7480  0.7663 232/233   0.9749
r035_P1P2                0.7551 1443  548  388 0.8661 0.8625 |  0.7549  0.7498  0.7663 233/234   0.9791
g017_G1                  0.7543 1441  549  390 0.8650 0.8625 |  0.7541  0.7486  0.7663 233/234   0.9791
gv_B_adverbe             0.7551 1443  548  388 0.8650 0.8625 |  0.7559  0.7498  0.7696 232/233   0.9749
gv_E_pos2                0.7843 1534  547  297 0.8818 0.8873 |  0.7836  0.7802  0.7912 232/233   0.9749
gv_E_pos3                0.7666 1480  550  351 0.8711 0.8797 |  0.7663  0.7608  0.7785 232/233   0.9749
gv_A_objet               0.7533 1447  564  384 0.8629 0.8625 |  0.7531  0.7450  0.7711 232/233   0.9749
gv_A_B                   0.7543 1449  562  382 0.8629 0.8625 |  0.7551  0.7472  0.7728 232/233   0.9749
gv_C_prep                0.7535 1440  551  391 0.8650 0.8625 |  0.7533  0.7476  0.7663 232/233   0.9749
placebo_E2               0.7388 1427  605  404 0.8571 0.8
… [670 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Règle chirurgicale pour les GV du S qui incluent le sujet (suffixe chunker)

- **bash** `{"command": "cd /tmp/seg && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('variantes.py'); t=p.read_text()\nadd = '''\n# G-D : un GV de S qui **inclut le sujet** est remplacé par le GV du chunker (même fin,\n# début plus tardif) — la forme chirurgicale du filtre union, limitée aux GV\nGD_OLD = \ … [1462 caractères tronqués]`

  ```
Traceback (most recent call last):
  File "/tmp/seg/variantes.py", line 246, in <module>
    d = ecrire(nom, VARIANTS[nom])
                    ~~~~~~~~^^^^^
KeyError: 'gv_D_suffixe'
[stderr]
  File "<stdin>", line 8
    GD_OLD = \'\'\'                for s in c.get("segments", []):
              ^
SyntaxError: unexpected character after line continuation character
  ```

- **read** `{"file_path": "/tmp/seg/variantes.py", "offset": 150, "limit": 100}`

  ```
<path>/tmp/seg/variantes.py</path>
<type>file</type>
<content>
150: 
151:         # 3 a bis. une forme en -s/-es après un NOM sujet est un verbe (« the cat sleeps »).'''
152: 
153: 
154: # G-E2 : comme G-E mais le NOUN candidat doit suivre immédiatement le premier NOM
155: # du GN (prevprev DET/ADJ/NUM) — évite « La cloche sonne | midi » (r135)
156: GE2_OLD = GE_OLD
157: GE2_NEW = '''        # 3 a quater. un mot inconnu (NOUN, confiance ≤ 0,45) **juste après le
158:         # premier NOM d'un GN** et devant une frontière de clause (PONCT, PREP, DET) est
159:         # le verbe de la proposition : « Le soleil brille. », « Le chat boit du lait ».
160:         for _k, _i in enumerate(pos_idx):
161:             _e = etiquettes[_i]
162:             if _k < 2 or _e.type != "NOUN" or _e.confiance > 0.45:
163:                 continue
164:             _av = etiquettes[pos_idx[_k - 1]]
165:             _av2 = etiquettes[pos_idx[_k - 2]]
166:             _su = etiquettes[pos_idx[_k + 1]] if _k + 1 < len(pos_idx) else None
167:             if (_av.type == "NOUN" and _av2.type in ("DET", "ADJ", "NUM")
168:                     and _su is not None and _su.type in ("PONCT", "PREP", "DET")):
169: 
… [4409 caractères tronqués]
  ```

