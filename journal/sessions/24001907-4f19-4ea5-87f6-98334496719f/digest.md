# Session DSH — relecture

- identifiant : `24001907-4f19-4ea5-87f6-98334496719f`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 19:25:28
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer l'état v7 de l'attachement** (commit `69bd865e`) et vérifier que ses chiffres et ses portes sont justes.

Contexte : `tools/bloc_linguistique.py` (classe `Heuristique`, `_syntagmes_simple`, `_cible_precedent`, `_cible_hors_span`), `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bloc`), `tools/tests/linguistique/gold_split.py` (dev/test), `tools/pensee/autotest.py` (183 portes). Fiches à auditer : `reports/rapport-pensee-couverture-v7.md` + `reports/pensee-couverture-v7.json`, et les fiches amont v4/v5 (`reports/rapport-pensee-segmentation-v4.md`, `rapport-pensee-couverture-v5.md`).

Revendications à rejouer (au commit `69bd865e`) : labels 196, exact 195 (0,9949), F1 0,5595 (S 0,4741, chunker 0,5858), tête 0,7205, POS 0,7603, couverture 0,8201, top-k 166, fr 135/135, en 60/61, spans 43 (21 REL, 17 SUB, 5 GP), dev/test (à re-mesurer).

À faire :
1. Rejoue chaque valeur depuis la racine (`sys.path.insert(0,'.')`) et compare à la fiche et au JSON ; note tout écart, même d'arrondi.
2. Vérifie que les portes citées attendent bien ces valeurs (lis `tools/pensee/autotest.py` : T86-T90, T107, T110-T115, T119, T138, T141, T153, T156, T157, T161-T164, T166-T169, T171-T173, T177, T179, T180) et signale toute porte périmée ou tout chiffre non couvert.
3. **Contrôles négatifs** : permutation des cibles (1000 tirages), candidat aléatoire, et ablation : que donne la mesure si on retire la règle du segment précédent (copie locale) ? Si on retire le POS contextuel ?
4. **Re-mesure dev/test** (le split n'a pas été re-mesuré depuis la v6) : donne dev et test exact/labels, F1, couverture.
5. Écris **uniquement** deux fichiers neufs : `reports/rapport-audit-v7.md` et `reports/pensee-audit-v7.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé avec les écarts, les contrôles et les valeurs dev/test.
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

⏵ Repérage du dépôt et de l'état git au commit 69bd865e

- **bash** `{"command": "git rev-parse HEAD && git status --short | head -50 && git log --oneline -5", "description": "Inspect git HEAD and status"}`

  ```
69bd865ec1bae1958b6f617bde4bf685a15d7d67
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
D  journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/digest.md
D  journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/rapport.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rapport.md
D  journal/sessions/3144cf23-6004-46ef-bc3d-f05d81c0cff6/digest.md
D  journal/sessions/3144cf23-6004-46ef-bc3d-f05d81c0cff6/rapport.md
D  journal/sessions/3f8f2bb8-781b-44a6-9e14-58025004b6fc/digest.md
D  journal/sessions/3f8f2bb8-781b-44a6-9e14-58025004b6fc/rapport.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/digest.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/rapport.md
D  journal/se
… [2398 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | head -60; echo '---'; ls tools/tests/linguistique/; echo '---'; ls tools/pensee/ 2>/dev/null | head", "description": "List reports and relevant tool dirs"}`

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
… [546 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des fiches v7 et du JSON pour cadrer les valeurs revendiquées

- **read** `{"file_path": "reports/rapport-pensee-couverture-v7.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-couverture-v7.md</path>
<type>file</type>
<content>
1: # B13 — la couverture à 0,8201 : POS contextuel, GV avant GP, prépositions ambiguës
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **183/183 portes** : la **couverture** passe de **187 à 196 labels** (sur 239) et l'exactitude
5: > tient : **exact 195/196 = 0,9949** (fr **135/135 = 1,0**, en **60/61**) ; la **F1 syntagmes**
6: > monte à **0,5595** (union ; S 0,4741, chunker 0,5858), la tête à **0,7205** ; la **POS** passe de
7: > **0,7475 à 0,7603** ; les **spans perdus** tombent de **52 à 43** (21 REL, 17 SUB, 5 GP).
8: >
9: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (POS contextuel,
10: > ordre GV/GP, prépositions composées, sujets), [`autotest.py`](../tools/pensee/autotest.py)
11: > (32 assertions recalées) ; JSON [`pensee-couverture-v7.json`](pensee-couverture-v7.json).
12: 
13: ## 1. Les cinq corrections
14: 
15: | # | correction | effet |
16: |---|---|---|
17: | 1 | **POS contextuel** : un verbe de suffixe après DET/PRÉP/ADJ devient un nom (« brothe
… [2780 caractères tronqués]
  ```

- **bash** `{"command": "wc -l reports/pensee-couverture-v7.json reports/rapport-pensee-couverture-v5.md reports/rapport-pensee-segmentation-v4.md tools/pensee/autotest.py tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/gold_split.py", "description": "Count lines of  … [11 caractères tronqués]`

  ```
48 reports/pensee-couverture-v7.json
    79 reports/rapport-pensee-couverture-v5.md
    79 reports/rapport-pensee-segmentation-v4.md
  2835 tools/pensee/autotest.py
  2144 tools/bloc_linguistique.py
   305 tools/tests/linguistique/evaluer_gold.py
    50 tools/tests/linguistique/gold_split.py
  5540 total
  ```

- **read** `{"file_path": "reports/pensee-couverture-v7.json"}`
- **read** `{"file_path": "reports/rapport-pensee-couverture-v5.md"}`
- **read** `{"file_path": "reports/rapport-pensee-segmentation-v4.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-couverture-v7.json</path>
<type>file</type>
<content>
1: {
2:  "date": "2026-11-05",
3:  "ligne": "B13",
4:  "portes": "183/183",
5:  "avant": {
6:   "labels": 187,
7:   "exact": 187,
8:   "couverture": 0.7824,
9:   "f1": 0.513,
10:   "tete": 0.6826,
11:   "pos": 0.7475,
12:   "spans": 52
13:  },
14:  "apres": {
15:   "labels": 196,
16:   "exact": 195,
17:   "exact_span": 0.9949,
18:   "couverture": 0.8201,
19:   "f1": 0.5595,
20:   "f1_s": 0.4741,
21:   "f1_chunker": 0.5858,
22:   "tete": 0.7205,
23:   "pos": 0.7603,
24:   "fr": "135/135",
25:   "en": "60/61",
26:   "topk": 166,
27:   "topk_taux": 0.6946,
28:   "spans": {
29:    "REL": 21,
30:    "SUB": 17,
31:    "GP": 5,
32:    "total": 43
33:   }
34:  },
35:  "corrections": [
36:   "POS contextuel (DET/PRÉP/ADJ → nom)",
37:   "GV avant GP",
38:   "prépositions composées",
39:   "prépositions ambiguës (since/before/after/until/as)",
40:   "verbe après pronom sujet + adverbe final"
41:  ],
42:  "limites": [
43:   "43 spans",
44:   "top-k incomplet",
45:   "in-sample",
46:   "heuristiques"
47:  ]
48: }

(End of file - total 48 lines)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-couverture-v5.md</path>
<type>file</type>
<content>
1: # B13 — la couverture : 187 labels, exact 185/187 (0,9893), F1 0,5156
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **183/183 portes** : la **couverture** passe de **160 à 187 labels** (sur 239) et l'exactitude
5: > tient : **exact 186/187 = 0,9947** (fr **0,9921**, en **1,0000** — 60/60) ; la **F1 syntagmes**
6: > monte à **0,5156** (union ; S 0,4582, chunker 0,5351) et la tête à **0,6826** ; les **spans
7: > perdus** tombent de **79 à 52** (24 REL, 12 SUB, 16 GP). Sur le gold tenu à l'écart : **dev
8: > 126/126 (1,000)**, **test 60/61** — la progression n'est pas un surajustement visible.
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
11: > `_cible_precedent`), [`autotest.py`](../tools/pensee/autotest.py) (25 assertions recalées) ;
12: > [`gold_split.py`](../tools/tests/linguistique/gold_split.py) pour dev/test ; JSON
13: > [`pensee-couverture-v5.json`](pensee-couverture-v5.json).
14: 
15: ## 1. Les six corrections
16: 
17: 
… [3515 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-segmentation-v4.md</path>
<type>file</type>
<content>
1: # B13 — la segmentation d'abord : F1 0,2862 → 0,4194, exact 158/160 (0,9875), couverture 160/239
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **183/183 portes** : le diagnostic de A12/A14 était juste — le trou n'était pas l'attachement mais le
5: > **découpage**. Sept corrections générales font passer la **F1 syntagmes de 0,2862 à 0,4539**
6: > (union ; S 0,4285, chunker 0,4143), la **tête de 0,4989 à 0,6432**, et la **couverture de 145 à
7: > 160 labels** (sur 239) ; l'attachement suit : **exact 157/160 = 0,9812**, **top-k 156/239**,
8: > par langue **fr 0,9915** (117/118) et **en 0,9524** (40/42) — l'anglais passe de **28 à 42 labels**.
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
11: > `_verbe_dans`, `_cible_hors_span`), [`autotest.py`](../tools/pensee/autotest.py) (38 assertions
12: > recalées) ; fiches amont [spans](rapport-spans-chunker.md) (A12), [gold anglais](rapport-gold-anglais.md)
13: > (A14) ; JSON [`pensee-s
… [4017 caractères tronqués]
  ```

