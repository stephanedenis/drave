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

