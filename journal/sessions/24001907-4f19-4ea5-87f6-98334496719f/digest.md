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

### 🤖 Assistant

⏵ Lecture de l'évaluateur gold et du découpage dev/test

- **read** `{"file_path": "tools/tests/linguistique/evaluer_gold.py"}`
- **read** `{"file_path": "tools/tests/linguistique/gold_split.py"}`

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
… [15928 caractères tronqués]
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

⏵ Rejeu de l'évaluateur gold pour mesurer toutes les valeurs v7

- **bash** `{"command": "python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/audit_v7_eval.json > /tmp/audit_v7_eval.out 2>&1; echo \"exit=$?\"; tail -5 /tmp/audit_v7_eval.out", "description": "Run gold evaluator and save JSON"}`

  ```
exit=1
   },
   "attachement_tete": {
    "cibles": 181,
    "labels": 18
heuristique all: {"pos": {"exactitude": 0.7581, "exactitude_ferme": 0.9004, "exactitude_ouvert": 0.6234, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 50, "NOUN": 80, "VERB": 4}, "ADV": {"ADV": 117, "NOUN": 20, "PREP": 2, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 118, "?": 3, "NOUN": 3}, "CONJ": {"CONJ": 44, "PRON": 25, "DET": 12, "?": 13, "PREP": 2, "NOUN": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 657, "ADJ": 17, "VERB": 7, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"?": 25}, "PREP": {"PREP": 114}, "PRON": {"PRON": 411, "NOUN": 8, "?": 30, "DET": 25, "CONJ": 1}, "VERB": {"VERB": 311, "NOUN": 450, "ADJ": 5, "PREP": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.5959, "rappel": 0.5201, "f1": 0.5555, "tp": 969, "fp": 657, "fn": 894, "tete": {"precision": 0.7885, "rappel": 0.6543, "f1": 0.7152, "tp": 1219, "fp": 327, "fn": 644}}, "pragmatique": {"acte": 0.9967, "negation": 0.9771, "modalite": 0.9886, "double_sens": 0.9444}, "fraction_semantique": 0.5537}
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json\nsys.path.insert(0, '.')\nsys.path.insert(0, 'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger, charger_gele\nfrom tools.tests.linguistique.gold_split import dev, test, compter\nph = charger(); ge = charger_gele()\nprint('vivant', len … [488 caractères tronqués]`

  ```
vivant 612 {'phrases': 612, 'cibles': 239, 'sources': {'hand': 20, 'reel': 432, 'synthetique': 160}, 'langues': {'fr': 402, 'en': 210}}
gele 602 {'phrases': 602, 'cibles': 239, 'sources': {'hand': 20, 'reel': 422, 'synthetique': 160}, 'langues': {'fr': 394, 'en': 208}}
dev 422 test 190
all {'fr': 402, 'en': 210} {'hand': 20, 'reel': 432, 'synthetique': 160} cibles 239
dev {'fr': 277, 'en': 145} {'hand': 15, 'reel': 302, 'synthetique': 105} cibles 163
test {'fr': 125, 'en': 65} {'hand': 5, 'reel': 130, 'synthetique': 55} cibles 76
  ```

### 🤖 Assistant

⏵ Analyse du JSON rejoué et comparaison aux sources de gold

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/audit_v7_eval.json'))\nh=d['heuristique']\nfor src in h:\n    a=h[src]\n    att=a['attachement']; t=a['syntagme']\n    print(src, 'phr', a['phrases'], 'pos', a['pos']['exactitude'], 'F1', t['f1'], 'S?', 'tp',t['tp'],'fp',t['fp'],'fn' … [492 caractères tronqués]`

  ```
all phr 612 pos 0.7581 F1 0.5555 S? tp 969 fp 657 fn 894 tete 0.7152
   cibles 239 labels 196 exact 195 exact_span 0.9949 couv 0.8201 topk 166 topk_taux 0.6946 fr {'cibles': 151, 'labels': 135, 'exact': 135, 'topk': 121, 'exact_taux_span': 1.0} en {'cibles': 88, 'labels': 61, 'exact': 60, 'topk': 45, 'exact_taux_span': 0.9836}
reel phr 452 pos 0.7661 F1 0.5429 S? tp 740 fp 485 fn 761 tete 0.7006
   cibles 184 labels 154 exact 153 exact_span 0.9935 couv 0.837 topk 133 topk_taux 0.7228 fr {'cibles': 96, 'labels': 93, 'exact': 93, 'topk': 88, 'exact_taux_span': 1.0} en {'cibles': 88, 'labels': 61, 'exact': 60, 'topk': 45, 'exact_taux_span': 0.9836}
hand phr 20 pos 0.8857 F1 0.7107 S? tp 43 fp 22 fn 13 tete 0.8142
   cibles 13 labels 12 exact 12 exact_span 1.0 couv 0.9231 topk 10 topk_taux 0.7692 fr {'cibles': 10, 'labels': 10, 'exact': 10, 'topk': 8, 'exact_taux_span': 1.0} en {'cibles': 3, 'labels': 2, 'exact': 2, 'topk': 2, 'exact_taux_span': 1.0}
reel_new phr 432 pos 0.7608 F1 0.5351 S? tp 697 fp 463 fn 748 tete 0.6956
   cibles 171 labels 142 exact 141 exact_span 0.993 couv 0.8304 topk 123 topk_taux 0.7193 fr {'cibles': 86, 'labels': 83, 'exact': 83, 'topk': 80, 'exact_taux_span':
… [589 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger, charger_gele, evaluer_bloc\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nfor nom,ph in [('vivant',charger()),('gele',charger_gele())] … [432 caractères tronqués]`

  ```
vivant phr 612 pos 0.7581 F1 0.5555 tete 0.7152 cibles 239 labels 196 exact 195 0.9949 couv 0.8201 topk 166 fr {'cibles': 151, 'labels': 135, 'exact': 135, 'topk': 121, 'exact_taux_span': 1.0} en {'cibles': 88, 'labels': 61, 'exact': 60, 'topk': 45, 'exact_taux_span': 0.9836}
gele phr 602 pos 0.7603 F1 0.5595 tete 0.7205 cibles 239 labels 196 exact 195 0.9949 couv 0.8201 topk 166 fr {'cibles': 151, 'labels': 135, 'exact': 135, 'topk': 121, 'exact_taux_span': 1.0} en {'cibles': 88, 'labels': 61, 'exact': 60, 'topk': 45, 'exact_taux_span': 0.9836}
  ```

### 🤖 Assistant

⏵ Inspection des portes citées dans autotest.py

- **bash** `{"command": "grep -n \"T86\\|T87\\|T88\\|T89\\|T90\\|T107\\|T110\\|T111\\|T112\\|T113\\|T114\\|T115\\|T119\\|T138\\|T141\\|T153\\|T156\\|T157\\|T161\\|T162\\|T163\\|T164\\|T166\\|T167\\|T168\\|T169\\|T171\\|T172\\|T173\\|T177\\|T179\\|T180\" tools/pensee/autotest.py", "description": "Locate cited ga … [16 caractères tronqués]`

  ```
2731:              ("T86 sous-ensembles", t86_gold_subsets()),
2732:              ("T87 phrases complexes", t87_complexes()),
2733:              ("T88 20 complexes", t88_complexes20()),
2734:              ("T89 50 complexes", t89_complexes50()),
2735:              ("T90 100 complexes", t90_complexes100()),
2752:              ("T107 gold complet", t107_gold_complet()),
2755:              ("T110 segmenteur", t110_segmenteur()),
2756:              ("T111 hybride segmenteur", t111_hybride_seg()),
2757:              ("T112 union segmenteurs", t112_union()),
2758:              ("T113 union par défaut", t113_union_defaut()),
2759:              ("T114 cascade + union", t114_cascade_union()),
2760:              ("T115 tête cascade", t115_tete_cascade()),
2764:              ("T119 restitution sémantique", t119_miroir_resume()),
2783:              ("T138 défaut fusion", t138_defaut_niveau()),
2786:              ("T141 élision", t141_elision()),
2798:              ("T153 attachement", t153_attachement()),
2801:              ("T156 relation GN-GV", t156_relation()),
2802:              ("T157 rôles par position", t157_roles()),
2806:              ("T161 cible proximité", t161_cible_proximite()),
… [828 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"183\\|portes\\|def porte\\|registre\" tools/pensee/autotest.py | head -40; echo '---'; sed -n '1,80p' tools/pensee/autotest.py", "description": "Inspect autotest structure and gates count"}`

  ```
2:"""autotest.py — les portes du moteur de pensée : T0–T4, puis AC-3 et alpha-bêta.
1690:    """L'hybride frontières/têtes : tête F1 0,4183 (S 0,3552, chunker 0,4707)."""
1944:    """Le gold gelé : 602 phrases, les portes ne cassent plus."""
2647:    portes = [("T0 store canonique", t0_store()), ("T1 rejeu", t1_rejeu()),
2827:    for nom, (ok, msg) in portes:
2830:    print(f"  {len(portes) - échecs}/{len(portes)} portes tenues")
---
#!/usr/bin/env python3
"""autotest.py — les portes du moteur de pensée : T0–T4, puis AC-3 et alpha-bêta.

  T0  le store est canonique          aller-retour exact, empreinte stable, ordres différents
  T1  l'arbre se rejoue               mêmes empreintes, mêmes scores ; une graine changée diverge
  T1  le flux DRVF thought se relit   enveloppe, racine, rejeu ; un score corrompu est refusé
  T2  une stratégie est substituable  même arbre, deux stratégies ; une stratégie aveugle échoue
  T3  le moteur est anytime           best-so-far non décroissant ; un budget nul est refusé
  T4  la justification est valide     chemin racine → settled ; un chemin inventé est refusé
  T5  AC-3 se branche                 une chaîne propage, une contradiction se voit, la
… [3300 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"^def t8[6-9]\\|^def t9[0-9]\\|^def t10[0-9]\\|^def t11[0-9]\\|^def t13[0-9]\\|^def t14[0-9]\\|^def t15[0-9]\\|^def t16[0-9]\\|^def t17[0-9]\\|^def t18[0-9]\" tools/pensee/autotest.py", "description": "Find gate function definitions"}`

  ```
1349:def t86_gold_subsets() -> tuple[bool, str]:
1368:def t87_complexes() -> tuple[bool, str]:
1382:def t88_complexes20() -> tuple[bool, str]:
1396:def t89_complexes50() -> tuple[bool, str]:
1410:def t90_complexes100() -> tuple[bool, str]:
1424:def t91_discours() -> tuple[bool, str]:
1440:def t92_anaphore() -> tuple[bool, str]:
1451:def t93_anaphore_pieges() -> tuple[bool, str]:
1462:def t94_anaphore_corrigee() -> tuple[bool, str]:
1473:def t95_objets() -> tuple[bool, str]:
1484:def t96_chaines() -> tuple[bool, str]:
1495:def t97_roles() -> tuple[bool, str]:
1506:def t98_hybride() -> tuple[bool, str]:
1517:def t99_semantique() -> tuple[bool, str]:
1528:def t100_plafond() -> tuple[bool, str]:
1545:def t101_kappa() -> tuple[bool, str]:
1559:def t102_meta() -> tuple[bool, str]:
1570:def t103_pondere() -> tuple[bool, str]:
1582:def t104_cv() -> tuple[bool, str]:
1593:def t105_cv_graines() -> tuple[bool, str]:
1607:def t106_bilan_anaphore() -> tuple[bool, str]:
1631:def t107_gold_complet() -> tuple[bool, str]:
1644:def t108_anaphore_68() -> tuple[bool, str]:
1657:def t109_anaphore_103() -> tuple[bool, str]:
1670:def t110_segmenteur() -> tuple[bool, str]:
1689:def t111_hybride_seg() -> t
… [2945 caractères tronqués]
  ```

- **read** `{"file_path": "tools/pensee/autotest.py", "offset": 1349, "limit": 120}`
- **read** `{"file_path": "tools/pensee/autotest.py", "offset": 1631, "limit": 180}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
1349: def t86_gold_subsets() -> tuple[bool, str]:
1350:     """Les sous-ensembles : les 20 nouvelles (POS 0,8214) contre les 180 anciennes (0,7897)."""
1351:     import tools.bloc_linguistique as bl
1352:     from ..tests.linguistique.gold_reel import construire
1353:     from ..tests.linguistique.evaluer_gold import evaluer_bloc
1354:     g = construire()
1355:     h = bl.Heuristique()
1356: 
1357:     def sous(a: int, b: int):
1358:         return [p for p in g["phrases"] if a <= int(p["id"][1:]) <= b]
1359: 
1360:     r1 = evaluer_bloc("h", h, sous(1, 180))
1361:     r2 = evaluer_bloc("h", h, sous(181, 200))
1362:     p2 = round(r2["pos"]["exactitude"], 4)
1363:     p1 = round(r1["pos"]["exactitude"], 4)
1364:     return abs(p2 - 0.8452) < 0.001 and abs(p1 - 0.8221) < 0.001, (
1365:         f"r181-200 POS {p2} ; r001-180 POS {p1}")
1366: 
1367: 
1368: def t87_complexes() -> tuple[bool, str]:
1369:     """Les phrases complexes : POS 0,6471, syntagme 0,4828 sur r201-r205."""
1370:     import tools.bloc_linguistique as bl
1371:     from ..tests.linguistique.gold_reel im
… [4844 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
1631: def t107_gold_complet() -> tuple[bool, str]:
1632:     """Le gold complet : 522 phrases, POS 0,7586."""
1633:     import tools.bloc_linguistique as bl
1634:     from ..tests.linguistique.evaluer_gold import charger_gele as charger, evaluer_bloc
1635:     phrases = charger()
1636:     h = bl.Heuristique()
1637:     r = evaluer_bloc("h", h, phrases)
1638:     return (len(phrases) == 602
1639:             and abs(r["pos"]["exactitude"] - 0.7603) < 0.001), (
1640:         f"gold complet : {len(phrases)} phrases, POS {round(r['pos']['exactitude'], 4)}, "
1641:         f"tête {round(r['syntagme']['tete']['f1'], 4)}")
1642: 
1643: 
1644: def t108_anaphore_68() -> tuple[bool, str]:
1645:     """La coréférence à 68 liens : 52/68 par le rôle, 51/68 par le dernier nom."""
1646:     from ..tests.linguistique.anaphore import mesurer, mesurer_roles
1647:     from ..tests.linguistique.gold_reel import construire
1648:     g = construire()
1649:     ps = [p for p in g["phrases"] if 301 <= int(p["id"][1:]) <= 372]
1650:     dernier = mesurer(ps, ignorer_pp=True)
1651:     role = m
… [8240 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des portes T138 à T180

- **read** `{"file_path": "tools/pensee/autotest.py", "limit": 130, "offset": 2017}`
- **read** `{"file_path": "tools/pensee/autotest.py", "limit": 160, "offset": 2221}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
2017: def t138_defaut_niveau() -> tuple[bool, str]:
2018:     """Le défaut de la fusion : la confiance (0,7424) bat le niveau (0,3432)."""
2019:     import tools.bloc_linguistique as bl
2020:     from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
2021:     ph = charger()
2022:     h, n = bl.Heuristique(), bl.MockNeuronal()
2023:     r_conf = evaluer_bloc("c", bl.Parallele([h, n]), ph)["pos"]["exactitude"]
2024:     r_niv = evaluer_bloc("n", bl.Parallele([h, n], priorite_par_niveau=bl.PRIORITE_NIVEAU), ph)["pos"]["exactitude"]
2025:     return abs(r_conf - 0.7465) < 0.001 and abs(r_niv - 0.3454) < 0.001 and r_conf > r_niv, (
2026:         f"défaut : confiance {round(r_conf, 4)}, niveau {round(r_niv, 4)}")
2027: 
2028: 
2029: def t139_quatre_modes() -> tuple[bool, str]:
2030:     """Les quatre modes (API réelle) : le niveau gagne (0,9309) et garde l'acte (0,9954)."""
2031:     import json
2032:     import pathlib
2033:     racine = pathlib.Path(__file__).resolve().parents[2]
2034:     d = json.loads((racine / "reports/pensee-quatre-modes-432.json").read_t
… [5553 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
2221: def t153_attachement() -> tuple[bool, str]:
2222:     """L'attachement sur le gold 612 (239 cibles) : top1 0,5983, exact 0,5900."""
2223:     import tools.bloc_linguistique as bl
2224:     from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
2225:     r = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
2226:     return (r["cibles"] == 239 and abs(r["top1_taux"] - 0.8159) < 0.001
2227:             and abs(r["exact_taux"] - 0.8159) < 0.001), (
2228:         f"attachement : top1 {r['top1_taux']}, exact {r['exact_taux']}, "
2229:         f"couverture {r['couverture']}")
2230: 
2231: 
2232: def t154_cibles() -> tuple[bool, str]:
2233:     """Les cibles de l'attachement : 1624 segments sans cible sur 1863."""
2234:     from ..tests.linguistique.evaluer_gold import charger
2235:     ph = charger()
2236:     tot = sum(len(p["segments"]) for p in ph)
2237:     sans = sum(1 for p in ph for s in p["segments"] if not s.get("cible"))
2238:     return tot == 1863 and sans == 1624, (
2239:         f"cibles : {sans}/{tot} segments sans cible (couvertu
… [6854 caractères tronqués]
  ```

- **read** `{"file_path": "tools/pensee/autotest.py", "limit": 120, "offset": 2381}`
- **read** `{"file_path": "tools/pensee/autotest.py", "limit": 110, "offset": 2476}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
2381: 
2382: def t164_verbe_gv() -> tuple[bool, str]:
2383:     """Le verbe du GV-phrase : le POS VERB, pas le dernier mot."""
2384:     import tools.bloc_linguistique as bl
2385:     from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
2386:     h = bl.Heuristique()
2387:     a = h.analyser("The boy saw the cat in the park.", "en")
2388:     gp = [e for e in a.etiquettes if e.niveau == "syntagme" and e.type == "GP"]
2389:     cible = ((gp[0].meta or {}).get("attachement") or {}).get("cible") if gp else None
2390:     r = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
2391:     return cible == "saw" and r["exact"] == 195, (
2392:         f"verbe du GV : {cible} (attendu saw) ; exact {r['exact']}/239")
2393: 
2394: 
2395: def t165_lexique_verbal() -> tuple[bool, str]:
2396:     """Le lexique verbal arbitre le POS : « talks » est un verbe, « brother » n'en est pas un."""
2397:     import tools.bloc_linguistique as bl
2398:     retour = (bl._est_verbe("talks"), bl._est_verbe("joue"), bl._est_verbe("brother"))
2399:     a = bl.Heuristique().ana
… [5821 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
2476: def t170_attachement_cible() -> tuple[bool, str]:
2477:     """L'attachement ciblé : REL → antécédent (nom à gauche), GP → verbe du GV."""
2478:     import tools.bloc_linguistique as bl
2479:     h = bl.Heuristique()
2480:     a = h.analyser("L'homme que j'ai vu dort.", "fr")
2481:     rel = [e for e in a.etiquettes if e.niveau == "syntagme" and e.type == "REL"]
2482:     cible = ((rel[0].meta or {}).get("attachement") or {}).get("cible") if rel else None
2483:     b = h.analyser("Le garçon joue au ballon.", "fr")
2484:     gp = [e for e in b.etiquettes if e.niveau == "syntagme" and e.type == "GP"]
2485:     cible2 = ((gp[0].meta or {}).get("attachement") or {}).get("cible") if gp else None
2486:     return cible == "homme" and cible2 == "joue", (
2487:         f"ciblé : REL « homme » {cible}, GP « joue » {cible2}")
2488: 
2489: 
2490: def t171_lexique_elargi() -> tuple[bool, str]:
2491:     """Le lexique élargi : participes irréguliers et verbes courants (« vu » n'était pas un verbe)."""
2492:     import tools.bloc_linguistique as bl
2493:     from ..tests.lingui
… [5175 caractères tronqués]
  ```

- **read** `{"file_path": "tools/pensee/autotest.py", "limit": 60, "offset": 1822}`
- **read** `{"file_path": "tools/pensee/autotest.py", "limit": 120, "offset": 2586}`
- **read** `{"file_path": "tools/pensee/autotest.py", "limit": 45, "offset": 2640}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
1822: def t119_miroir_resume() -> tuple[bool, str]:
1823:     """La restitution sémantique : rappel 0,7834 (heur), 0,7472 (cascade)."""
1824:     import tools.bloc_linguistique as bl
1825:     from ..tests.linguistique.evaluer_gold import charger_gele as charger
1826:     from ..tests.linguistique.miroir import rappel_resume
1827:     ph = charger()
1828:     h = bl.Heuristique()
1829:     rap_h = sum(rappel_resume(h.analyser(p["texte"], p["langue"]), p["texte"])
1830:                 for p in ph) / max(1, len(ph))
1831:     cas = bl.Cascade(h, bl.MockNeuronal())
1832:     rap_c = sum(rappel_resume(cas.analyser(p["texte"], p["langue"]), p["texte"])
1833:                 for p in ph) / max(1, len(ph))
1834:     return (abs(rap_h - 0.7465) < 0.001 and abs(rap_c - 0.6914) < 0.001), (
1835:         f"résumé : heur {round(rap_h, 4)}, cascade {round(rap_c, 4)}")
1836: 
1837: 
1838: def t120_miroir_reponse() -> tuple[bool, str]:
1839:     """La réponse : 19/19 sur les questions du gold."""
1840:     import tools.bloc_linguistique as bl
1841:     from ..tests.linguistique.evalu
… [2133 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
2586:     return cibles.get("s052") == "ouvre" and cibles.get("s012") == "écoute", (
2587:         f"segment précédent : s052 {cibles.get('s052')}, s012 {cibles.get('s012')}")
2588: 
2589: 
2590: def t177_candidats_tete() -> tuple[bool, str]:
2591:     """Les têtes des candidats S : le top-k strict passe de 88 à 141."""
2592:     import tools.bloc_linguistique as bl
2593:     from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
2594:     a = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
2595:     return (a["topk_exact"] == 166 and abs(a["topk_exact_taux_span"] - 0.8469) < 0.001), (
2596:         f"candidats têtes : {a['topk_exact']}/145 ({a['topk_exact_taux_span']})")
2597: 
2598: 
2599: def t178_cache_chunker() -> tuple[bool, str]:
2600:     """Le cache du chunker : un seul `_syntagmes_simple` par analyse (1+2S → 1)."""
2601:     import tools.bloc_linguistique as bl
2602:     appels = {"n": 0}
2603:     orig = bl.Heuristique._syntagmes_simple
2604: 
2605:     def compte(self, *a, **k):
2606:         appels["n"] += 1
2607:         return o
… [5878 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py</path>
<type>file</type>
<content>
2640:     return (fr["cibles"] == 151 and fr["labels"] == 135 and fr["exact"] == 135
2641:             and en["cibles"] == 88 and en["labels"] == 61 and en["exact"] == 60), (
2642:         f"langues : fr {fr['exact']}/{fr['labels']}, en {en['exact']}/{en['labels']} "
2643:         f"({en['labels']}/{en['cibles']} labels)")
2644: 
2645: 
2646: def main() -> int:
2647:     portes = [("T0 store canonique", t0_store()), ("T1 rejeu", t1_rejeu()),
2648:               ("T1 graine", t1_graine()), ("T1 DRVF thought", t1_drvf()),
2649:               ("T2 stratégies", t2_strategies()),
2650:               ("T3 anytime", t3_anytime()), ("T4 justification", t4_justification()),
2651:               ("T5 AC-3", t5_ac3()), ("T6 alpha-bêta", t6_alphabeta()),
2652:               ("T7 banc anytime", t7_banc()),
2653:               ("T8 opérateurs hétérogènes", t8_operateurs()),
2654:               ("T9 neuronal nécessaire", t9_necessaire()),
2655:               ("T10 labyrinthe non linéaire", t10_labyrinthe()),
2656:               ("T11 porte neuronale", t11_porte()),
2657:               
… [1863 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lancement des 183 portes pour confronter attentes et mesures

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. timeout 1200 python3 tools/pensee/autotest.py > /tmp/audit_v7_portes.out 2>&1; echo \"exit=$?\"; tail -20 /tmp/audit_v7_portes.out", "description": "Run autotest gates", "run_in_background": true}`

  ```
started background job bash-1750
  ```

- **bash** `{"command": "sed -n '1,120p' tools/bloc_linguistique.py", "description": "Read bloc_linguistique header and classes"}`

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
… [3234 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-1750 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. timeout 1200 python3 tools/pensee/autotest.py > /tmp/audit_v7_portes.out 2>&1; echo "exit=$?"; tail -20 /tmp/audit_v7_portes.out) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Lecture du verdict des portes

- **job_output** `{"job_id": "bash-1750"}`

  ```
exit=1
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", line 32, in <module>
    from .coeur import Candidat, Etat
ImportError: attempted relative import with no known parent package
[status: completed, exit code: 0]
  ```

### 🤖 Assistant

⏵ Relance des portes en module (import relatif)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=. timeout 1800 python3 -m tools.pensee.autotest > /tmp/audit_v7_portes.out 2>&1; echo \"exit=$?\"; tail -30 /tmp/audit_v7_portes.out", "description": "Run autotest as module", "run_in_background": true}`

  ```
started background job bash-1752
  ```

- **bash** `{"command": "grep -n \"def _syntagmes_simple\\|def _cible_precedent\\|def _cible_hors_span\\|def _pos\\|contexte\\|suffixe\\|segment précédent\\|segment_precedent\\|def _attacher\\|attachement\" tools/bloc_linguistique.py | head -80", "description": "Locate key heuristic functions"}`

  ```
103:    contexte: str = ""
126:            "trace": list(self.trace), "cout": cout, "contexte": self.contexte,
134:                 contexte: str | None = None) -> Annotation: ...
589:    def _pos(self, langue: str, mot: str) -> tuple[str, bool, float]:
620:                sortie.append(("suffixe", len(mot) - len(suf), len(mot), suf))
658:    def _cible_precedent(texte: str, segment: dict, precedent: dict | None, verbes) -> str | None:
706:    def _cible_hors_span(texte: str, segment: dict, gvs: list[dict], cible: str | None):
820:        """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
836:    def _syntagmes_simple(self, texte: str, langue: str,
956:                 contexte: str | None = None) -> Annotation:
1002:        # 3 bis. le contexte tranche les suffixes ambigus : un mot après DET/PRÉP/ADJ est un
1013:                                          script=script, meta={"ouvert": True, "contexte": avant.type})
1066:                        # REL/SUB : c'est le **segment précédent** qui tranche — après un GV
1093:                        meta["attachement"] = {"segment": s.get("texte", ""), "cible": cible}
1122:                    meta["attachement"] 
… [2453 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class Heuristique\" tools/bloc_linguistique.py", "description": "Locate Heuristique class"}`

  ```
513:class Heuristique:
  ```

- **read** `{"file_path": "tools/bloc_linguistique.py", "limit": 180, "offset": 513}`
- **read** `{"file_path": "tools/bloc_linguistique.py", "limit": 180, "offset": 658}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
513: class Heuristique:
514:     """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""
515: 
516:     nom = "heuristique"
517: 
518:     def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
519:                  seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
520:                  union: bool = True):
521:         self.profils = profils
522:         self.segmenter_s = segmenter_s
523:         self.seuil_ouvert = seuil_ouvert
524:         self.seuil_langue = seuil_langue
525:         self.union = union
526: 
527:     # -- langues / script ---------------------------------------------------
528:     def _langue(self, texte: str, indice: str | None) -> tuple[str, float, str]:
529:         langue, conf, _ = detecter_langue(texte, self.profils, indice)
530:         script = detecter_script(texte)
531:         if conf < self.seuil_langue:
532:             return "und", conf, script
533:         return langue, conf, script
534: 
535:     # -- tokens ---------------------------------------------
… [8303 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
658:     def _cible_precedent(texte: str, segment: dict, precedent: dict | None, verbes) -> str | None:
659:         """REL → tête du GN précédent ; SUB après un GV → son verbe (le gouverneur)."""
660:         if not precedent:
661:             return None
662:         if segment.get("type") == "REL" and precedent.get("type") == "GN":
663:             return Heuristique._tete_nom(texte, precedent["debut"], precedent["fin"])
664:         if segment.get("type") == "SUB" and precedent.get("type") == "GV":
665:             if _est_adverbe_seul(precedent):
666:                 return None
667:             return Heuristique._verbe_dans(texte, precedent["debut"], precedent["fin"], verbes)
668:         return None
669: 
670:     @staticmethod
671:     def _candidats_precedent(texte: str, segment: dict, precedent: dict | None) -> list[str]:
672:         """Les candidats que le **précédent** impose : l'antécédent d'une REL, le verbe d'une SUB."""
673:         if not precedent:
674:             return []
675:         if segment.get("type") == "REL" and precedent.get("type") == 
… [8757 caractères tronqués]
  ```

- **read** `{"file_path": "tools/bloc_linguistique.py", "limit": 150, "offset": 940}`
- **read** `{"file_path": "tools/bloc_linguistique.py", "limit": 80, "offset": 1090}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
940:                        and not est_verbe(mots[j][0], mots[j][2])
941:                        and _normaliser(mots[j][2]) not in RELATIFS):
942:                     j += 1
943:                 # « à manger » : un GP réduit à sa préposition prend le verbe qui suit
944:                 if j == i + 1 and j < len(mots) and est_verbe(mots[j][0], mots[j][2]):
945:                     j += 1
946:                 segments.append({"type": "GP", "role": _role_gp(t), "niveau": 1,
947:                                  "debut": d, "fin": mots[j - 1][1],
948:                                  "texte": texte[d:mots[j - 1][1]], "candidats": []})
949:                 i = j
950:                 continue
951:             i += 1
952:         return segments
953: 
954:     # -- analyse ------------------------------------------------------------
955:     def analyser(self, texte: str, langue: str | None = None,
956:                  contexte: str | None = None) -> Annotation:
957:         t0 = time.perf_counter()
958:         texte = texte or ""
959:         trace: list[dict] = []
960:
… [9197 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1090:                     cible = self._repli_verbe_propre(texte, s, cible)
1091:                     meta = {"role": s.get("role", ""), "niveau": s.get("niveau", 0)}
1092:                     if cible:
1093:                         meta["attachement"] = {"segment": s.get("texte", ""), "cible": cible}
1094:                     candidats = list(noms) + self._verbes_proches(
1095:                         texte, s, gvs, verbes=verbes, cache=cache_gv)
1096:                     # la **tête** de chaque candidat S (« « … » → Le livre » → livre ; « … → Les
1097:                     # fleurs poussent » → poussent) : mesuré +45 segments au top-k strict.
1098:                     for nom in noms:
1099:                         if "→" in nom:
1100:                             tete = self._tete_texte(nom.split("→", 1)[1])
1101:                             if tete and tete not in candidats:
1102:                                 candidats.append(tete)
1103:                     etiquettes.append(Etiquette("syntagme", s.get("type", "GN"),
1104:                                          
… [4531 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-1752", "timeout_ms": 300000, "wait": true}`

  ```
exit=0
  ✅ T152 trois tirages     tirages : [0.9838, 0.9838, 0.9838] (écart-type 0, modèle déterministe)
  ✅ T153 attachement       attachement : top1 0.8159, exact 0.8159, couverture 0.8201
  ✅ T154 cibles            cibles : 1624/1863 segments sans cible (couverture 0.1283)
  ✅ T155 cibles 500        500 premiers : 294 GN, 206 GV
  ✅ T156 relation GN-GV    relation : 257/546 (0.4707)
  ✅ T157 rôles par position rôles : 231 sans rôle, 151 avant le GV, 46 après
  ✅ T158 passifs           passifs : 5/5 faux (le sujet est un patient)
  ✅ T159 correctif passifs par → agent, avec → moyen
  ✅ T160 passifs sans par  passif sans par (chunker) : 3/3 patient
  ✅ T161 cible proximité   proximité : top1 195/239, exact 195/239, tête 195/145
  ✅ T162 candidats verbes  candidats : top-k 166/239 (0.6946), tête 167/145
  ✅ T163 échecs attachement échecs : 43 de span, 30 de cible (33 avant les correctifs)
  ✅ T164 verbe du GV       verbe du GV : saw (attendu saw) ; exact 195/239
  ✅ T165 lexique verbal    lexique : talks True, joue True, brother False ; cible GP talks
  ✅ T166 spans perdus      spans : 21 REL, 17 SUB, 5 GP
  ✅ T167 dénominateur      dénominateur : spans 0.9949 / 0.8469 / 0.9949
  ✅
… [1034 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Relevé complet des portes et repérage des libellés périmés

- **bash** `{"command": "grep -n \"T8[6-9]\\|T90\\|T107\\|T110\\|T111\\|T112\\|T113\\|T114\\|T115\\|T119\\|T138\\|T141\\|T153\\|T156\\|T157\\|T161\\|T162\\|T163\\|T164\\|T166\\|T167\\|T168\\|T169\\|T171\\|T172\\|T173\\|T177\\|T179\\|T180\" /tmp/audit_v7_portes.out", "description": "Extract cited gate outputs"}`

  ```
89:  ✅ T86 sous-ensembles     r181-200 POS 0.8452 ; r001-180 POS 0.8221
90:  ✅ T87 phrases complexes  r201-205 : POS 0.7353, syntagme 0.7027
91:  ✅ T88 20 complexes       r201-220 : POS 0.7236, syntagme 0.5954
92:  ✅ T89 50 complexes       r201-250 : POS 0.7327, syntagme 0.5839
93:  ✅ T90 100 complexes      r201-300 : POS 0.719, syntagme 0.5477
110:  ✅ T107 gold complet      gold complet : 602 phrases, POS 0.7603, tête 0.7205
113:  ✅ T110 segmenteur        segmenteur : S F1 0.4741 tête 0.6518 ; chunker F1 0.5858 tête 0.7441
114:  ✅ T111 hybride segmenteur hybride : tête F1 0.7265 (S 0,3552, chunker 0,4707)
115:  ✅ T112 union segmenteurs union : segments F1 0.5595 (S 0,4741)
116:  ✅ T113 union par défaut  union par défaut : F1 0.5595, tête 0.7205
117:  ✅ T114 cascade + union   cascade : F1 0.5864, tête 0.7285, 602 appels
118:  ✅ T115 tête cascade      tête cascade corrigée : 0.6709 (cascade 0,441 ; union 0,466)
122:  ✅ T119 restitution sémantique résumé : heur 0.7465, cascade 0.6914
141:  ✅ T138 défaut fusion     défaut : confiance 0.7465, niveau 0.3454
144:  ✅ T141 élision           élision : POS 0.7581
156:  ✅ T153 attachement       attachement : top1 0.8159, exact 0.8159, couvert
… [1274 caractères tronqués]
  ```

- **bash** `{"command": "head -8 /tmp/audit_v7_portes.out; echo ...; grep -c \"✅\" /tmp/audit_v7_portes.out; grep -c \"❌\" /tmp/audit_v7_portes.out; tail -2 /tmp/audit_v7_portes.out", "description": "Check gate totals"}`

  ```
✅ T0 store canonique     aller-retour exact, empreinte stable sous permutation
  ✅ T1 rejeu               rejeu identique sur 94 événements ; deux exécutions égales
  ✅ T1 graine              deux graines divergent au premier pas différent
  ✅ T1 DRVF thought        DRVF 23853 octets, 94 événements rejoués ; score corrompu refusé ; diff 0
  ✅ T2 stratégies          BFS et A* atteignent le même but ; la stratégie aveugle échoue
  ✅ T3 anytime             best-so-far non décroissant sur 5 budgets : [0.2, 0.25, 0.33, 1.0, 1.0]
  ✅ T4 justification       justification valide sur 7 nœuds ; chemin inventé refusé
  ✅ T5 AC-3                chaîne {'A': ('r',), 'B': ('g',), 'C': ('r',)} ; carte 3-colorable non réduite ; contradiction domaine vide = True
...
183
0
  ✅ T180 par langue        langues : fr 135/135, en 60/61 (61/88 labels)
  183/183 portes tenues
  ```

### 🤖 Assistant

⏵ Recherche des fiches v6 et vérification de la cohérence amont

- **bash** `{"command": "ls reports/ | grep -i \"pensee-\\(couverture\\|segmentation\\|audit\\)\"; echo '---'; git log --oneline --all -- reports/rapport-pensee-couverture-v5.md reports/rapport-pensee-segmentation-v4.md | head", "description": "List coverage reports and history"}`

  ```
pensee-audit-attachement.json
pensee-audit.json
pensee-audit-v2.json
pensee-couverture-v5.json
pensee-couverture-v7.json
pensee-segmentation-v4.json
rapport-pensee-audit.md
rapport-pensee-couverture-v5.md
rapport-pensee-couverture-v7.md
rapport-pensee-segmentation-v4.md
---
b975011b B13 — LES CANDIDATS DU PRÉCÉDENT : EXACT 186/187 (0,9947), ANGLAIS 60/60, DEV 126/126 ; 183/183
7a9f0d6a B13 — LA COUVERTURE : 187 LABELS, EXACT 185/187 (0,9893), F1 0,5156, DEV 125/126 ET TEST 60/61 ; 183/183
392f03aa B13 — S NE SEGMENTE QUE LE FRANÇAIS : F1 0,4194 → 0,4539, TÊTE 0,6432 ; EXACT 157/160, FR 0,9915 / EN 0,9524 ; 183/183
cceacc1a B13 — LA SEGMENTATION D'ABORD : F1 0,2862 → 0,4194, EXACT 158/160 (0,9875), COUVERTURE 160/239, FR 0,9915 / EN 0,9762 ; 183/183
  ```

- **bash** `{"command": "git show --stat --oneline 69bd865e | head -30; echo '---'; git show --stat --oneline 0ec6c27d | head -30; echo '---'; git show --stat --oneline b975011b | head -20; echo '---'; git show --stat --oneline 7a9f0d6a | head -20", "description": "Inspect v7 and upstream commits"}`

  ```
69bd865e B13 — LA COUVERTURE À 0,8201 : POS CONTEXTUEL 0,7603, F1 0,5595, EXACT 195/196 (0,9949), 43 SPANS ; 183/183
 docs/pilotage/en-cours.md                          |   4 +-
 docs/pilotage/roadmap.md                           |   2 +-
 journal/2026-11-05/README.md                       |   7 +-
 journal/2026-11-05/attention.md                    |   2 +-
 journal/2026-11-05/distribue.md                    |   2 +-
 journal/2026-11-05/docs.md                         |   2 +-
 journal/2026-11-05/memoire.md                      |   2 +-
 journal/2026-11-05/mesures.md                      |   8 +-
 journal/2026-11-05/modele.md                       |   2 +-
 journal/2026-11-05/moteur.md                       |   2 +-
 journal/2026-11-05/portes.md                       |   2 +-
 journal/README.md                                  |   2 +-
 journal/THEMES.md                                  |   2 +-
 journal/sessions/MANIFEST.md                       |   4 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 360 +++++++++++++++++++++
 .../rapport.md                                     |  21 +-
 reports/README.md                                  |   2 +-
 reports/pensee-couverture-
… [4405 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' reports/rapport-pensee-attachement-parfait.md 2>/dev/null; echo '---JSON---'; cat reports/pensee-attachement-parfait.json 2>/dev/null", "description": "Read v6 sheet and JSON"}`

  ```
# B13 — l'attachement parfait sur les spans prédits : 187/187 (1,0000)

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **183/183 portes** : sur les **187 segments dont le span est prédit** (sur 239 cibles), la cible
> est **juste 187 fois** — **français 127/127 (1,0)**, **anglais 60/60 (1,0)**, **verbes 131/131**,
> **noms 56/56** ; **dev 126/126**, **test 61/61**. Le **rendement global** reste **187/239 =
> 0,7824** : les 52 spans non prédits sont la seule frontière qui reste.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_cible_precedent`,
> `_candidats_precedent`, `_repli_verbe_propre`, `_est_adverbe_seul`),
> [`autotest.py`](../tools/pensee/autotest.py) ; dev/test [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ;
> JSON [`pensee-attachement-parfait.json`](pensee-attachement-parfait.json).

## 1. Les deux corrections de ce round

| # | correction | effet |
|---|---|---|
| 1 | **les candidats du précédent** : l'antécédent d'une REL et le verbe d'une SUB entrent dans `candidats` | couverture des candidats 26 → 26, top-k 161 |
| 2 | **un adverbe seul n'est pas un gouverneur** (`P
… [3178 caractères tronqués]
  ```

- **bash** `{"command": "git show 7a9f0d6a:reports/rapport-pensee-couverture-v5.md | sed -n '1,12p'; echo '=== b975011b ==='; git show b975011b:reports/rapport-pensee-couverture-v5.md | sed -n '1,12p'; echo '=== current ==='; diff <(git show b975011b:reports/rapport-pensee-couverture-v5.md) reports/rapport-pens … [76 caractères tronqués]`

  ```
# B13 — la couverture : 187 labels, exact 185/187 (0,9893), F1 0,5156

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **183/183 portes** : la **couverture** passe de **160 à 187 labels** (sur 239) et l'exactitude
> tient : **exact 185/187 = 0,9893** (fr **0,9921**, en **0,9833**) ; la **F1 syntagmes** monte à
> **0,5156** (union ; S 0,4577, chunker 0,5341) et la tête à **0,6826** ; les **spans perdus**
> tombent de **79 à 52** (24 REL, 12 SUB, 16 GP). Sur le gold tenu à l'écart : **dev 125/126,
> test 60/61** — la progression n'est pas un surajustement visible.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
> `_cible_precedent`), [`autotest.py`](../tools/pensee/autotest.py) (25 assertions recalées) ;
> [`gold_split.py`](../tools/tests/linguistique/gold_split.py) pour dev/test ; JSON
=== b975011b ===
# B13 — la couverture : 187 labels, exact 185/187 (0,9893), F1 0,5156

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **183/183 portes** : la **couverture** passe de **160 à 187 labels** (sur 239) et l'exactitude
> tient 
… [660 caractères tronqués]
  ```

- **bash** `{"command": "for c in cceacc1a 392f03aa; do echo \"=== $c ===\"; git show $c:reports/rapport-pensee-segmentation-v4.md | sed -n '1,10p'; done; echo '=== diff current vs 392f03aa ==='; diff <(git show 392f03aa:reports/rapport-pensee-segmentation-v4.md) reports/rapport-pensee-segmentation-v4.md | head … [50 caractères tronqués]`

  ```
=== cceacc1a ===
# B13 — la segmentation d'abord : F1 0,2862 → 0,4194, exact 158/160 (0,9875), couverture 160/239

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **183/183 portes** : le diagnostic de A12/A14 était juste — le trou n'était pas l'attachement mais le
> **découpage**. Six corrections générales du chunker font passer la **F1 syntagmes de 0,2862 à
> 0,4194**, la **tête de 0,4989 à 0,5930**, et la **couverture de 145 à 160 labels** (sur 239) ;
> l'attachement suit : **exact 158/160 = 0,9875**, **top-k 158/239**, par langue **fr 0,9915**
> (117/118) et **en 0,9762** (41/42) — l'anglais passe de **28 à 42 labels**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
=== 392f03aa ===
# B13 — la segmentation d'abord : F1 0,2862 → 0,4194, exact 158/160 (0,9875), couverture 160/239

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **183/183 portes** : le diagnostic de A12/A14 était juste — le trou n'était pas l'attachement mais le
> **découpage**. Sept corrections générales font passer la **F1 syntagmes de 0,2862 à 0,453
… [431 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/pensee-couverture-v5.json; echo '---'; cat reports/pensee-segmentation-v4.json", "description": "Read upstream JSONs"}`

  ```
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "183/183",
 "avant": {
  "labels": 160,
  "exact": 157,
  "exact_span": 0.9812,
  "topk": 156,
  "couverture": 0.6695,
  "f1": 0.4539,
  "tete": 0.6432,
  "fr": 0.9915,
  "en": 0.9524,
  "spans": 79,
  "echecs_cible": 3
 },
 "apres": {
  "labels": 187,
  "exact": 186,
  "exact_span": 0.9947,
  "topk": 161,
  "couverture": 0.7824,
  "f1": 0.5156,
  "f1_s": 0.4582,
  "f1_chunker": 0.5351,
  "tete": 0.6826,
  "fr": 0.9921,
  "en": 1.0,
  "spans": {
   "REL": 24,
   "SUB": 12,
   "GP": 16,
   "total": 52
  },
  "echecs_cible": 1,
  "topk_taux": 0.6736,
  "candidats_manquants": 26
 },
 "dev": {
  "exact": 126,
  "labels": 126,
  "f1": 0.5091,
  "couverture": 0.773
 },
 "test": {
  "exact": 60,
  "labels": 61,
  "f1": 0.5217,
  "couverture": 0.8026
 },
 "corrections": [
  "REL/SUB avant le GN + « that » désambiguïsé",
  "frontière de clause (second verbe, AUX)",
  "POS VERB dans le chunker",
  "déterminants élidés",
  "prépositions anglaises + live",
  "segment précédent dans l'union et le chunker",
  "candidats du précédent (antécédent REL, verbe SUB)"
 ],
 "limites": [
  "52 spans",
  "27 échecs de cible",
  "test petit",
  "heuristi
… [1032 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mesure complète v7 sur gold vivant, gelé, dev et test

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json, random, statistics\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger, charger_gele, evaluer_bloc, _seg\nfrom tools.tests.linguistique.go … [1478 caractères tronqués]`

  ```
{
 "vivant": {
  "phrases": 612,
  "pos": 0.7581,
  "f1": 0.5555,
  "tete": 0.7152,
  "cibles": 239,
  "labels": 196,
  "exact": 195,
  "exact_taux_span": 0.9949,
  "couverture": 0.8201,
  "topk": 166,
  "topk_taux": 0.6946,
  "topk_taux_span": 0.8469,
  "topk_exact": 166,
  "exact_taux": 0.8159,
  "fr": {
   "cibles": 151,
   "labels": 135,
   "exact": 135,
   "topk": 121,
   "exact_taux_span": 1.0
  },
  "en": {
   "cibles": 88,
   "labels": 61,
   "exact": 60,
   "topk": 45,
   "exact_taux_span": 0.9836
  },
  "verbe": {
   "cibles": 137,
   "justes": 136,
   "taux": 0.9927
  },
  "nom": {
   "cibles": 59,
   "justes": 59,
   "taux": 1.0
  }
 },
 "gele": {
  "phrases": 602,
  "pos": 0.7603,
  "f1": 0.5595,
  "tete": 0.7205,
  "cibles": 239,
  "labels": 196,
  "exact": 195,
  "exact_taux_span": 0.9949,
  "couverture": 0.8201,
  "topk": 166,
  "topk_taux": 0.6946,
  "topk_taux_span": 0.8469,
  "topk_exact": 166,
  "exact_taux": 0.8159,
  "fr": {
   "cibles": 151,
   "labels": 135,
   "exact": 135,
   "topk": 121,
   "exact_taux_span": 1.0
  },
  "en": {
   "cibles": 88,
   "labels": 61,
   "exact": 60,
   "topk": 45,
   "exact_taux_span": 0.9836
  },
  "verbe": {
   "cibles": 137,
… [2777 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mesure des composantes S/chunker et préparation des copies d'ablation

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger, charger_gele, evaluer_bloc\nimport bloc_linguistique as bl\nfor nom,ph in [('vivant',charger … [445 caractères tronqués]`

  ```
vivant S 0.4688 0.6446 chunker 0.5822 0.7397 union 0.5555
gele S 0.4741 0.6518 chunker 0.5858 0.7441 union 0.5595
  ```

- **bash** `{"command": "mkdir -p /tmp/audit_v7 && cp tools/bloc_linguistique.py /tmp/audit_v7/bloc_ablation.py && python3 - <<'PY'\nfrom pathlib import Path\np=Path('/tmp/audit_v7/bloc_ablation.py')\ns=p.read_text()\n# marque la racine pour que generateur S reste accessible\ns=s.replace('RACINE = pathlib.Path( … [236 caractères tronqués]`

  ```
written /tmp/audit_v7/bloc_ablation.py 113433
  ```

### 🤖 Assistant

⏵ Ablations locales : règle du segment précédent et POS contextuel

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\nimport re\nbase = Path('/tmp/audit_v7/bloc_ablation.py').read_text()\n\n# --- ablation 1 : POS contextuel (bloc 3 bis) ---\ndebut = base.index('        # 3 bis. le contexte tranche')\nfin = … [4019 caractères tronqués]`

  ```
sans_pos : bloc retiré 807 caractères
sans_precedent : 3 sites retirés
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 15, in <module>
  File "<stdin>", line 10, in charger_module
  File "<frozen importlib._bootstrap_external>", line 1027, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/tmp/audit_v7/bloc_sans_pos.py", line 58, in <module>
    @dataclass(frozen=True)
     ~~~~~~~~~^^^^^^^^^^^^^
  File "/usr/lib64/python3.13/dataclasses.py", line 1344, in wrap
    return _process_class(cls, init, repr, eq, order, unsafe_hash,
                          frozen, match_args, kw_only, slots,
                          weakref_slot)
  File "/usr/lib64/python3.13/dataclasses.py", line 997, in _process_class
    and _is_type(type, cls, dataclasses, dataclasses.KW_ONLY,
        ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                 _is_kw_only))):
                 ^^^^^^^^^^^^
  File "/usr/lib64/python3.13/dataclasses.py", line 757, in _is_type
    ns = sys.modules.get(cls.__module__).__dict__
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute '__dict__'. 
… [39 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport importlib.util, sys, json\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger, charger_gele, evaluer_bloc\nfrom tools.tests.linguistique.gold_split i … [1726 caractères tronqués]`

  ```
{
 "temoin": {
  "vivant": {
   "phrases": 612,
   "pos": 0.7581,
   "f1": 0.5555,
   "tete": 0.7152,
   "labels": 196,
   "exact": 195,
   "exact_span": 0.9949,
   "couverture": 0.8201,
   "topk": 166,
   "topk_exact": 166,
   "fr": [
    135,
    135
   ],
   "en": [
    60,
    61
   ]
  },
  "gele": {
   "phrases": 602,
   "pos": 0.7603,
   "f1": 0.5595,
   "tete": 0.7205,
   "labels": 196,
   "exact": 195,
   "exact_span": 0.9949,
   "couverture": 0.8201,
   "topk": 166,
   "topk_exact": 166,
   "fr": [
    135,
    135
   ],
   "en": [
    60,
    61
   ]
  },
  "dev": {
   "phrases": 422,
   "pos": 0.7547,
   "f1": 0.5512,
   "tete": 0.7132,
   "labels": 134,
   "exact": 133,
   "exact_span": 0.9925,
   "couverture": 0.8221,
   "topk": 111,
   "topk_exact": 111,
   "fr": [
    92,
    92
   ],
   "en": [
    41,
    42
   ]
  },
  "test": {
   "phrases": 190,
   "pos": 0.7656,
   "f1": 0.5651,
   "tete": 0.7196,
   "labels": 62,
   "exact": 62,
   "exact_span": 1.0,
   "couverture": 0.8158,
   "topk": 55,
   "topk_exact": 55,
   "fr": [
    43,
    43
   ],
   "en": [
    19,
    19
   ]
  },
  "s_vivant": 0.4688,
  "chunker_vivant": 0.5822
 },
 "sans_pos": {
  "vivant": {
 
… [2309 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des portes dev/test et des portes couvrant les chiffres v7

- **bash** `{"command": "grep -n \"gold_split\\|dev(\\|test(\\|dev\\b\\|test\\b\" tools/pensee/autotest.py | head -40; echo '---'; grep -n \"0.8201\\|0.5595\\|0.7603\\|0.7205\\|0.4741\\|0.5858\\|195\\|196\\|0.9949\\|166\" tools/pensee/autotest.py", "description": "Find dev/test and v7 value gates"}`

  ```
2:"""autotest.py — les portes du moteur de pensée : T0–T4, puis AC-3 et alpha-bêta.
25:Usage : PYTHONPATH=. ~/gpu-env/bin/python tools/pensee/autotest.py
1571:    """Le vote pondéré : poids appris (1,0,0,0), test 7/10."""
1578:            and r["justes_test"] == 7), (
1579:        f"pondéré : poids {r['poids']}, test {r['justes_test']}/{r['test']}")
1589:    return r["test"] == 30 and r["justes"] == 25, (
1590:        f"CV 5 plis : {r['justes']}/{r['test']} liens justes")
1602:    ecart = round(statistics.pstdev(taux), 4)
2125:    man = {"format": "DRVM", "version": d.VERSION, "model": {"nom": "test"},
---
1639:            and abs(r["pos"]["exactitude"] - 0.7603) < 0.001), (
1684:    return (abs(f1 - 0.4741) < 0.001 and abs(f2 - 0.5858) < 0.001
1731:    return abs(f1 - 0.5595) < 0.001, f"union : segments F1 {f1} (S 0,4741)"
1743:    return abs(f1 - 0.5595) < 0.001 and abs(tete - 0.7205) < 0.001, (
1794:    return abs(r["fidelite"] - 0.196) < 0.001, (
1807:    return abs(fid - 0.196) < 0.001, f"sortie POS : fidélité {round(fid, 4)}"
2344:    return (a["cibles"] == 239 and a["top1"] == 195 and a["exact"] == 195), (
2355:    return (a["topk"] == 166 and th["topk"] == 167 and a["top1"]
… [791 caractères tronqués]
  ```

- **bash** `{"command": "git diff 69bd865e^ 69bd865e -- tools/bloc_linguistique.py | head -220", "description": "Inspect v7 code changes"}`

  ```
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 4db853e2..364b3545 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -298,7 +298,7 @@ LEXIQUES = {
 POS_FERME = {
     "fr": {
         "DET": set("le la les l un une ce cet cette ces mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs quel quelle quels quelles".split()),
-        "PREP": set("à a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis pendant durant contre malgré selon près loin devant derrière après avant".split()),
+        "PREP": set("à a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis pendant durant contre malgré selon près loin devant derrière après avant au-dessus au-dessous vis-à-vis en-dehors".split()),
         "PRON": set("je j tu il elle on nous vous ils elles me te se lui leur moi toi soi y en ce cela ça qui que quoi dont où".split()),
         "CONJ": set("et ou mais donc or ni car quand comme si parce puisque lorsque pendant qu".split()),
         "AUX": set("est sont était étaient été être ai as a avons avez ont avait avaient eu avoir suis es sommes êtes".split()),
@@ -367,6 +367,11 @@ 
… [9123 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du POS/F1 de la v6 pour dater les valeurs « avant »

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 0ec6c27d:tools/bloc_linguistique.py > /tmp/audit_v7/bloc_v6.py && python3 - <<'PY'\nimport importlib.util,sys,json\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charge … [968 caractères tronqués]`

  ```
vivant pos 0.7461 f1 0.5321 tete 0.6966 labels 156 exact 135 exact_span 0.8654 couv 0.6527 topk 94 fr 75 96 en 60 60
  S 0.5321 chunker 0.5321
gele pos 0.7482 f1 0.5351 tete 0.7006 labels 156 exact 135 exact_span 0.8654 couv 0.6527 topk 94 fr 75 96 en 60 60
  S 0.5351 chunker 0.5351
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\np=Path('/tmp/audit_v7/bloc_v6.py'); s=p.read_text()\nold='RACINE = pathlib.Path(__file__).resolve().parent.parent'\nassert old in s\np.write_text(s.replace(old, 'RACINE = pathlib.Path(\"/ho … [1170 caractères tronqués]`

  ```
vivant pos 0.7461 f1 0.513 tete 0.6785 labels 187 exact 187 exact_span 1.0 couv 0.7824 topk 161 fr 127 127 en 60 60
  S 0.453 chunker 0.5321
gele pos 0.7482 f1 0.5164 tete 0.6834 labels 187 exact 187 exact_span 1.0 couv 0.7824 topk 161 fr 127 127 en 60 60
  S 0.4582 chunker 0.5351
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -R \"0.7475\\|0,7475\\|0.6826\\|0,6826\" --include='*.py' --include='*.md' --include='*.json' . | head -30", "description": "Search where before-values appear"}`

  ```
./reports/pensee-multilingue.json:   "cosinus_pont": 0.7475,
./reports/kfold-pidgin.json:   "chrf": 27.980340474759586,
./reports/m2-typo.json:   "M2_vers": 0.682648401826484
./reports/routeur-m1-m2.json:   "M2": 0.682648401826484,
./reports/n2-budget.json:    "precision_main": 0.6826,
./reports/n2-budget.json:    0.6826,
./reports/rapport-pensee-couverture-v5.md:> monte à **0,5156** (union ; S 0,4582, chunker 0,5351) et la tête à **0,6826** ; les **spans
./reports/rapport-pensee-couverture-v5.md:| F1 tête | 0,6432 | **0,6826** |
./reports/pensee-couverture-v5.json:  "tete": 0.6826,
./reports/rapport-pensee-couverture-v7.md:> **0,7475 à 0,7603** ; les **spans perdus** tombent de **52 à 43** (21 REL, 17 SUB, 5 GP).
./reports/rapport-pensee-couverture-v7.md:| 1 | **POS contextuel** : un verbe de suffixe après DET/PRÉP/ADJ devient un nom (« brother », « chair ») | POS 0,7475 → 0,7603, +9 labels |
./reports/rapport-pensee-couverture-v7.md:| F1 tête | 0,6826 | **0,7205** |
./reports/rapport-pensee-couverture-v7.md:| POS | 0,7475 | **0,7603** |
./reports/pensee-couverture-v7.json:  "tete": 0.6826,
./reports/pensee-couverture-v7.json:  "pos": 0.7475,
./data/alignement/verne_fr_en.json:   
… [2652 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 0ec6c27d:reports/pensee-attachement-parfait.json | head -40; echo '---commit message---'; git log -1 --format='%B' 0ec6c27d", "description": "Check v6 JSON for POS/head"}`

  ```
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "183/183",
 "exact": {
  "labels": 187,
  "justes": 187,
  "taux": 1.0,
  "fr": "127/127",
  "en": "60/60",
  "verbe": "131/131",
  "nom": "56/56"
 },
 "dev": {
  "exact": 126,
  "labels": 126
 },
 "test": {
  "exact": 61,
  "labels": 61
 },
 "global": {
  "exact": 187,
  "cibles": 239,
  "taux": 0.7824,
  "spans_non_predits": {
   "REL": 24,
   "SUB": 12,
   "GP": 16,
   "total": 52
  }
 },
 "topk": {
  "justes": 161,
  "taux": 0.6736
 },
 "f1": 0.513,
 "corrections": [
  "candidats du précédent (antécédent REL, verbe SUB)",
  "adverbe seul non gouverneur + repli propre verbe (SUB/REL)"
---commit message---
B13 — L'ATTACHEMENT PARFAIT SUR LES SPANS PRÉDITS : 187/187 (1,0000), FR 1,0, EN 1,0, DEV 126/126, TEST 61/61 ; RENDEMENT 0,7824 ; 183/183
  ```

### 🤖 Assistant

⏵ Contrôles négatifs : permutation des cibles et candidat aléatoire

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json, random, statistics, collections\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\nimport bloc_linguistique as bl\n\nph =  … [4498 caractères tronqués]`

  ```
labels 196 exact 195 0.9948979591836735
cible vide 1 candidats vides 0
vocab cibles 135 vocab pred 135
top cibles [('livre', 5), ('dit', 4), ('film', 4), ('leave', 4), ('compte', 4), ('travaille', 3), ('works', 3), ('nage', 3)]
permutation exact   : mean 1.8070 median 2 min 0 max 7 p>=obs 0.000
permutation cibles[]: mean 1.9010 min 0 max 7 p>=obs 0.000
top-k observé 166/196 (0.8469) ; candidats permutés mean 2.46/196 (0.0126) min 0 max 8
candidat aléatoire (liste du label) : mean 70.24/196 (0.3584) max 92
candidat aléatoire (pool global)    : mean 0.76/196 (0.0039) max 4
{
 "labels": 196,
 "exact_observe": 195,
 "exact_observe_taux": 0.9949,
 "topk_observe": 166,
 "permutation_cibles": {
  "tirages": 1000,
  "moyenne": 1.807,
  "taux_moyen": 0.0092,
  "min": 0,
  "max": 7,
  "p_value": 0.0,
  "ecart_type": 1.327
 },
 "permutation_listes_cibles": {
  "tirages": 1000,
  "moyenne": 1.901,
  "taux_moyen": 0.0097,
  "min": 0,
  "max": 7,
  "p_value": 0.0
 },
 "candidat_aleatoire_cible": {
  "tirages": 1000,
  "moyenne": 70.24,
  "taux_moyen": 0.3584,
  "max": 92
 },
 "candidat_aleatoire_pool": {
  "tirages": 1000,
  "moyenne": 0.757,
  "taux_moyen": 0.0039,
  "max": 4
 },
 "topk_candida
… [106 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Audit des fiches amont v4/v5 : rejeu aux commits d'origine

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline 392f03aa..HEAD -- tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json tools/tests/linguistique/gold_synthetique.json tools/tests/linguistique/gold_gele.json tools/tests/linguistique/gold_split … [264 caractères tronqués]`

  ```
85e4082b B13 — LE GOLD DEV/TEST : TEST 0,9814, DEV 0,9811, LES GAINS GÉNÉRALISENT ; RÈGLE « RÉGLER SUR DEV, ACCEPTER SI TEST NE BAISSE PAS »
---stat v4/v5---
 reports/pensee-segmentation-v4.json                |  24 ++--
 reports/rapport-pensee-segmentation-v4.md          |  27 ++--
 tools/bloc_linguistique.py                         |   8 +-
 tools/pensee/autotest.py                           |  58 ++++-----
---
 reports/pensee-couverture-v5.json                  |  23 ++--
 reports/rapport-pensee-couverture-v5.md            |  17 +--
 tools/bloc_linguistique.py                         |  27 ++++-
 tools/pensee/autotest.py                           |  48 ++++----
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for c in 392f03aa b975011b; do git show $c:tools/bloc_linguistique.py > /tmp/audit_v7/bloc_$c.py; sed -i 's#RACINE = pathlib.Path(__file__).resolve().parent.parent#RACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrin … [122 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 107304  5 nov 19:45 /tmp/audit_v7/bloc_392f03aa.py
-rw-------. 1 stephane stephane 114145  5 nov 19:38 /tmp/audit_v7/bloc_ablation.py
-rw-r--r--. 1 stephane stephane 111844  5 nov 19:45 /tmp/audit_v7/bloc_b975011b.py
-rw-r--r--. 1 stephane stephane 113383  5 nov 19:39 /tmp/audit_v7/bloc_sans_pos.py
-rw-r--r--. 1 stephane stephane 114144  5 nov 19:39 /tmp/audit_v7/bloc_sans_precedent.py
-rw-r--r--. 1 stephane stephane 113208  5 nov 19:41 /tmp/audit_v7/bloc_v6.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline 85e4082b | head -40; echo '---'; git show --stat --oneline 85e4082b | grep -E \"gold\"", "description": "Inspect gold split commit changes"}`

  ```
85e4082b B13 — LE GOLD DEV/TEST : TEST 0,9814, DEV 0,9811, LES GAINS GÉNÉRALISENT ; RÈGLE « RÉGLER SUR DEV, ACCEPTER SI TEST NE BAISSE PAS »
 docs/pilotage/en-cours.md                          |  6 +--
 journal/2026-11-05/README.md                       |  5 +-
 journal/2026-11-05/mesures.md                      |  5 +-
 journal/README.md                                  |  2 +-
 journal/THEMES.md                                  |  2 +-
 journal/sessions/MANIFEST.md                       |  2 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 54 +++++++++++++++++++
 .../rapport.md                                     | 18 ++++---
 reports/README.md                                  |  2 +-
 reports/pensee-gold-split.json                     | 33 ++++++++++++
 reports/rapport-gold-split.md                      | 63 ++++++++++++++++++++++
 tools/tests/linguistique/gold_split.py             | 50 +++++++++++++++++
 12 files changed, 223 insertions(+), 19 deletions(-)
---
 reports/pensee-gold-split.json                     | 33 ++++++++++++
 reports/rapport-gold-split.md                      | 63 ++++++++++++++++++++++
 tools/tests/linguistique/gold_split.py             | 50 ++++++
… [11 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport importlib.util,sys\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger, charger_gele, evaluer_bloc\nfor tag,path in [('v4','/tmp/audit_v7/bloc_392f03 … [903 caractères tronqués]`

  ```
=== v4
vivant pos 0.7455 f1 0.4509 tete 0.6385 labels 160 exact 157 exact_span 0.9812 couv 0.6695 topk 156 fr 117 118 en 40 42
gele pos 0.7475 f1 0.4539 tete 0.6432 labels 160 exact 157 exact_span 0.9812 couv 0.6695 topk 156 fr 117 118 en 40 42
=== v5
vivant pos 0.7461 f1 0.513 tete 0.6785 labels 187 exact 186 exact_span 0.9947 couv 0.7824 topk 161 fr 126 127 en 60 60
gele pos 0.7482 f1 0.5164 tete 0.6834 labels 187 exact 186 exact_span 0.9947 couv 0.7824 topk 161 fr 126 127 en 60 60
=== v6
vivant pos 0.7461 f1 0.513 tete 0.6785 labels 187 exact 187 exact_span 1.0 couv 0.7824 topk 161 fr 127 127 en 60 60
gele pos 0.7482 f1 0.5164 tete 0.6834 labels 187 exact 187 exact_span 1.0 couv 0.7824 topk 161 fr 127 127 en 60 60
=== v7
vivant pos 0.7581 f1 0.5555 tete 0.7152 labels 196 exact 195 exact_span 0.9949 couv 0.8201 topk 166 fr 135 135 en 60 61
gele pos 0.7603 f1 0.5595 tete 0.7205 labels 196 exact 195 exact_span 0.9949 couv 0.8201 topk 166 fr 135 135 en 60 61
  ```

### 🤖 Assistant

⏵ Vérification des composantes S/chunker des fiches amont

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 7a9f0d6a:tools/bloc_linguistique.py > /tmp/audit_v7/bloc_7a9f0d6a.py && sed -i 's#RACINE = pathlib.Path(__file__).resolve().parent.parent#RACINE = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\")#' /tmp/audi … [1210 caractères tronqués]`

  ```
v4 vivant union 0.4509 tete 0.6385 | S 0.4237 0.605 | chunker 0.4125 0.6211 | pos 0.7455 exact 157 labels 160
v4 gele union 0.4539 tete 0.6432 | S 0.4285 0.6117 | chunker 0.4143 0.6245 | pos 0.7475 exact 157 labels 160
v5a vivant union 0.5121 tete 0.6777 | S 0.4525 0.6283 | chunker 0.5311 0.6957 | pos 0.7461 exact 185 labels 187
v5a gele union 0.5156 tete 0.6826 | S 0.4577 0.6353 | chunker 0.5341 0.6997 | pos 0.7482 exact 185 labels 187
v5b vivant union 0.513 tete 0.6785 | S 0.453 0.6288 | chunker 0.5321 0.6966 | pos 0.7461 exact 186 labels 187
v5b gele union 0.5164 tete 0.6834 | S 0.4582 0.6358 | chunker 0.5351 0.7006 | pos 0.7482 exact 186 labels 187
v6 vivant union 0.513 tete 0.6785 | S 0.453 0.6288 | chunker 0.5321 0.6966 | pos 0.7461 exact 187 labels 187
v6 gele union 0.5164 tete 0.6834 | S 0.4582 0.6358 | chunker 0.5351 0.7006 | pos 0.7482 exact 187 labels 187
  ```

### 🤖 Assistant

⏵ Identification des 10 phrases du gold vivant absentes du gelé

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys,json\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger,charger_gele\nv=charger(); g=charger_gele(); ids_g={p['id'] for p in g}\nextra=[p for p  … [431 caractères tronqués]`

  ```
extra 10
r423 reel fr segments 4 cibles 0 | Tu viens demain.
r424 reel fr segments 3 cibles 0 | Il mange.
r425 reel fr segments 3 cibles 0 | Elle dort.
r426 reel fr segments 3 cibles 0 | Ils partent.
r427 reel en segments 4 cibles 0 | You come tomorrow.
r428 reel fr segments 3 cibles 0 | Il pleut.
r429 reel fr segments 3 cibles 0 | On dit que c'est vrai.
r430 reel fr segments 3 cibles 0 | Elle est partie.
r431 reel fr segments 3 cibles 0 | Ils sont arrivés.
r432 reel en segments 3 cibles 0 | It rains.
ids living 612 gele 602
doublons 0
  ```

### 🤖 Assistant

⏵ Rejeu dev/test aux commits v5 et v6 pour situer les chiffres amont

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport importlib.util,sys\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger,charger_gele,evaluer_bloc\nfrom tools.tests.linguistique.gold_split import dev … [746 caractères tronqués]`

  ```
v5 dev phr 422 exact 126 / 126 taux 1.0 f1 0.5091 couv 0.773 topk 105 / 163 verbe {'cibles': 81, 'justes': 81, 'taux': 1.0} nom {'cibles': 45, 'justes': 45, 'taux': 1.0}
v5 test phr 190 exact 60 / 61 taux 0.9836 f1 0.5217 couv 0.8026 topk 56 / 76 verbe {'cibles': 50, 'justes': 49, 'taux': 0.98} nom {'cibles': 11, 'justes': 11, 'taux': 1.0}
v6 dev phr 422 exact 126 / 126 taux 1.0 f1 0.5091 couv 0.773 topk 105 / 163 verbe {'cibles': 81, 'justes': 81, 'taux': 1.0} nom {'cibles': 45, 'justes': 45, 'taux': 1.0}
v6 test phr 190 exact 61 / 61 taux 1.0 f1 0.5217 couv 0.8026 topk 56 / 76 verbe {'cibles': 50, 'justes': 50, 'taux': 1.0} nom {'cibles': 11, 'justes': 11, 'taux': 1.0}
v7 dev phr 422 exact 133 / 134 taux 0.9925 f1 0.5512 couv 0.8221 topk 111 / 163 verbe {'cibles': 88, 'justes': 87, 'taux': 0.9886} nom {'cibles': 46, 'justes': 46, 'taux': 1.0}
v7 test phr 190 exact 62 / 62 taux 1.0 f1 0.5651 couv 0.8158 topk 55 / 76 verbe {'cibles': 49, 'justes': 49, 'taux': 1.0} nom {'cibles': 13, 'justes': 13, 'taux': 1.0}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger\nfrom tools.tests.linguistique.gold_split import dev,test,compter\nph=charger(); d=dev(ph); t … [448 caractères tronqués]`

  ```
dev 422 test 190 union 612 inter 0
dev {'phrases': 422, 'cibles': 163, 'sources': {'hand': 15, 'reel': 302, 'synthetique': 105}, 'langues': {'fr': 277, 'en': 145}}
test {'phrases': 190, 'cibles': 76, 'sources': {'hand': 5, 'reel': 130, 'synthetique': 55}, 'langues': {'fr': 125, 'en': 65}}
cibles dev 163
cibles test 76
  ```

### 🤖 Assistant

⏵ Identification de l'unique échec d'attachement v7

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nfor p in charger():\n    a=h.analyser(p[ … [652 caractères tronqués]`

  ```
r102 en GP 'since this morning' gold ['falls'] pred None candidats ['GP'] | The rain falls since this morning.
  ```

### 🤖 Assistant

⏵ Vérification du détail des 43 spans perdus

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, collections, re\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger\nimport bloc_linguistique as bl\nh=bl.Heuristique(); cats=collections.Counte … [892 caractères tronqués]`

  ```
Counter({'REL': 21, 'SUB': 17, 'GP': 5}) total 43 REL qui 6
('REL', 'that') 10
('SUB', 'that') 9
('REL', 'qui') 6
('SUB', 'When') 4
('SUB', 'que') 3
('GP', 'les') 2
('REL', 'she') 1
('REL', 'where') 1
('GP', 'for') 1
('REL', 'dont') 1
('REL', 'whose') 1
('REL', 'que') 1
('SUB', "qu'il") 1
('GP', 'il') 1
('GP', 'le') 1
--- exemples ---
('g017', 'en', 'SUB', 'that she would come', ['said'])
('r034', 'en', 'REL', 'that I read', ['book'])
('r035', 'en', 'REL', 'she talks about', ['film'])
('r074', 'en', 'REL', 'that you read', ['book'])
('r114', 'en', 'REL', 'that we saw', ['film'])
('r115', 'en', 'REL', 'where I was born', ['house'])
('r153', 'en', 'GP', 'for the bus', ['wait'])
('r205', 'en', 'SUB', 'that you are right', ['think'])
('r214', 'en', 'REL', 'that I read', ['book'])
('r215', 'en', 'SUB', 'When it rains', ['stay'])
('r216', 'en', 'SUB', 'that he comes', ['says'])
('r219', 'en', 'SUB', 'that you come', ['know'])
('r224', 'fr', 'REL', 'dont la voiture est rouge', ['homme'])
('r239', 'en', 'REL', 'whose car is red', ['man'])
('r240', 'en', 'SUB', 'that he is right', ['believe'])
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger\nimport bloc_linguistique as bl\nh=bl.Heuristique(); stats=collections.Counter() … [802 caractères tronqués]`

  ```
Counter({('en', 'SUB'): 13, ('en', 'REL'): 13, ('fr', 'REL'): 8, ('fr', 'SUB'): 4, ('fr', 'GP'): 4, ('en', 'GP'): 1})
REL premiers mots Counter({('en', 'that'): 10, ('fr', 'qui'): 6, ('en', 'she'): 1, ('en', 'where'): 1, ('fr', 'dont'): 1, ('en', 'whose'): 1, ('fr', 'que'): 1})
REL avec qui Counter({'fr': 6})
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport importlib.util,sys,collections\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger\nspec=importlib.util.spec_from_file_location('v6c','/tmp/audit_v7/ … [591 caractères tronqués]`

  ```
v6 spans {'SUB': 12, 'GP': 16, 'REL': 24} 52
  ```

### 🤖 Assistant

⏵ Vérification du nombre d'assertions recalées annoncé dans la fiche

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff 69bd865e^ 69bd865e -- tools/pensee/autotest.py | grep -E '^[-+].*(abs\\(|==|return)' | wc -l; echo '---'; git diff 69bd865e^ 69bd865e -- tools/pensee/autotest.py | head -120", "description": "Inspect v7 autotest diff"}`

  ```
82
---
diff --git a/tools/pensee/autotest.py b/tools/pensee/autotest.py
index a3dd7b88..a5aa06e3 100644
--- a/tools/pensee/autotest.py
+++ b/tools/pensee/autotest.py
@@ -1361,7 +1361,7 @@ def t86_gold_subsets() -> tuple[bool, str]:
     r2 = evaluer_bloc("h", h, sous(181, 200))
     p2 = round(r2["pos"]["exactitude"], 4)
     p1 = round(r1["pos"]["exactitude"], 4)
-    return abs(p2 - 0.8214) < 0.001 and abs(p1 - 0.7919) < 0.001, (
+    return abs(p2 - 0.8452) < 0.001 and abs(p1 - 0.8221) < 0.001, (
         f"r181-200 POS {p2} ; r001-180 POS {p1}")
 
 
@@ -1374,7 +1374,7 @@ def t87_complexes() -> tuple[bool, str]:
     h = bl.Heuristique()
     ps = [p for p in g["phrases"] if 201 <= int(p["id"][1:]) <= 205]
     r = evaluer_bloc("h", h, ps)
-    return abs(r["pos"]["exactitude"] - 0.7059) < 0.001, (
+    return abs(r["pos"]["exactitude"] - 0.7353) < 0.001, (
         f"r201-205 : POS {round(r['pos']['exactitude'], 4)}, "
         f"syntagme {round(r['syntagme']['f1'], 4)}")
 
@@ -1388,7 +1388,7 @@ def t88_complexes20() -> tuple[bool, str]:
     h = bl.Heuristique()
     ps = [p for p in g["phrases"] if 201 <= int(p["id"][1:]) <= 220]
     r = evaluer_bloc("h", h, ps)
-    return 
… [4616 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff 69bd865e^ 69bd865e -- tools/pensee/autotest.py | grep -E '^[-+].*(abs\\(|== )' | sed 's/^[+-]//' | sort | uniq -c | sort -rn | head -20; echo '--- changed assertion lines count ---'; git diff 69bd865e^ 69bd865e -- tools/pens … [107 caractères tronqués]`

  ```
1     return (v["cibles"] == 137 and v["justes"] == 136 and abs(v["taux"] - 0.9927) < 0.001
      1     return (v["cibles"] == 131 and v["justes"] == 131 and abs(v["taux"] - 1.0) < 0.001
      1     return span == 52 and cible == 26, (
      1     return span == 43 and cible == 30, (
      1     return (r["exact"] == 195 and verbes == 137 and noms == 59), (
      1     return (r["exact"] == 187 and verbes == 131 and noms == 56), (
      1     return (r["cibles"] == 239 and abs(r["top1_taux"] - 0.8159) < 0.001
      1     return (r["cibles"] == 239 and abs(r["top1_taux"] - 0.7824) < 0.001
      1     return ok == (True, True, True, False) and r["exact"] == 195, (
      1     return ok == (True, True, True, False) and r["exact"] == 187, (
      1     return n == 546 and avec == 257, f"relation : {avec}/{n} ({round(avec/n, 4)})"
      1     return n == 544 and avec == 251, f"relation : {avec}/{n} ({round(avec/n, 4)})"
      1     return n == 231 and avant == 151 and apres == 46, (
      1     return n == 229 and avant == 137 and apres == 38, (
      1     return (hors == 1 and dans == 0), f"échecs de cible : {hors} hors candidats, {dans} mal classés"
      1     return (hors == 0 and 
… [407 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport subprocess,re\nd=subprocess.run(['git','diff','-U0','69bd865e^','69bd865e','--','tools/pensee/autotest.py'],capture_output=True,text=True).stdout\ncur=None; funcs=set(); changed=0\nfor line in d.splitlines(): … [878 caractères tronqués]`

  ```
fonctions touchées 32 ['t107_gold_complet', 't110_segmenteur', 't111_hybride_seg', 't112_union', 't113_union_defaut', 't114_cascade_union', 't115_tete_cascade', 't119_miroir_resume', 't138_defaut_niveau', 't141_elision', 't153_attachement', 't156_relation', 't157_roles', 't161_cible_proximite', 't162_candidats_verbes', 't163_echecs_attachement', 't164_verbe_gv', 't166_spans', 't167_denominateur', 't168_classement', 't169_conventions', 't171_lexique_elargi', 't172_echecs_cible', 't173_topk_strict', 't177_candidats_tete', 't179_multi_cibles', 't180_par_langue', 't86_gold_subsets', 't87_complexes', 't88_complexes20', 't89_complexes50', 't90_complexes100']
fonctions avec assertion changée 32 ['t107_gold_complet', 't110_segmenteur', 't111_hybride_seg', 't112_union', 't113_union_defaut', 't114_cascade_union', 't115_tete_cascade', 't119_miroir_resume', 't138_defaut_niveau', 't141_elision', 't153_attachement', 't156_relation', 't157_roles', 't161_cible_proximite', 't162_candidats_verbes', 't163_echecs_attachement', 't164_verbe_gv', 't166_spans', 't167_denominateur', 't168_classement', 't169_conventions', 't171_lexique_elargi', 't172_echecs_cible', 't173_topk_strict', 't177_candidats_tete',
… [135 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport ast\nsrc=open('tools/pensee/autotest.py').read()\ntree=ast.parse(src)\nfor node in ast.walk(tree):\n    if isinstance(node,ast.FunctionDef) and node.name=='main':\n        # count tuples in the portes list\n  … [245 caractères tronqués]`

  ```
portes list len 183
  ```

### 🤖 Assistant

⏵ Relevé des comptes tp/fp/fn et des têtes pour la fiche d'audit

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys,json\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger,charger_gele,evaluer_bloc\nimport bloc_linguistique as bl\nfor nom,ph in [('vivant',char … [591 caractères tronqués]`

  ```
vivant syntagme {'precision': 0.5959, 'rappel': 0.5201, 'f1': 0.5555, 'tp': 969, 'fp': 657, 'fn': 894, 'tete': {'precision': 0.7885, 'rappel': 0.6543, 'f1': 0.7152, 'tp': 1219, 'fp': 327, 'fn': 644}} tete {'precision': 0.7885, 'rappel': 0.6543, 'f1': 0.7152, 'tp': 1219, 'fp': 327, 'fn': 644}
  att {'cibles': 239, 'labels': 196, 'top1': 195, 'topk': 166, 'exact': 195, 'exact_any': 195, 'topk_exact': 166, 'couverture': 0.8201, 'top1_taux': 0.8159, 'topk_taux': 0.6946, 'exact_taux': 0.8159, 'top1_taux_span': 0.9949, 'topk_taux_span': 0.8469, 'exact_taux_span': 0.9949, 'topk_exact_taux_span': 0.8469}
  tete {'cibles': 196, 'labels': 196, 'top1': 195, 'topk': 167, 'top1_taux': 0.9949, 'topk_taux': 0.852, 'couverture': 1.0}
gele syntagme {'precision': 0.5983, 'rappel': 0.5254, 'f1': 0.5595, 'tp': 962, 'fp': 646, 'fn': 869, 'tete': {'precision': 0.7919, 'rappel': 0.6608, 'f1': 0.7205, 'tp': 1210, 'fp': 318, 'fn': 621}} tete {'precision': 0.7919, 'rappel': 0.6608, 'f1': 0.7205, 'tp': 1210, 'fp': 318, 'fn': 621}
  att {'cibles': 239, 'labels': 196, 'top1': 195, 'topk': 166, 'exact': 195, 'exact_any': 195, 'topk_exact': 166, 'couverture': 0.8201, 'top1_taux': 0.8159, 'topk_taux': 0.6946, 'ex
… [253 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle de la cible tirée uniformément (référence du hasard)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys,random,statistics,collections\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger\nimport bloc_linguistique as bl\nph=charger(); h=bl.Heuristique … [838 caractères tronqués]`

  ```
cible uniforme : mean 1.925 (0.0098), max 8, min 0
  ```

### 🤖 Assistant

⏵ Ablations fines : cible du précédent vs candidats du précédent

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nfrom pathlib import Path\nbase=Path('/tmp/audit_v7/bloc_ablation.py').read_text()\n# candidats seulement\nold='''    def _candidats_precedent(texte: str, segment: dict, precedent: dict | None) -> list[str]:\n        … [2550 caractères tronqués]`

  ```
ok
temoin vivant exact 195 / 196 topk 166 couv 0.8201 fr 135 / 135 en 60 / 61
temoin gele exact 195 / 196 topk 166 couv 0.8201 fr 135 / 135 en 60 / 61
temoin dev exact 133 / 134 topk 111 couv 0.8221 fr 92 / 92 en 41 / 42
temoin test exact 62 / 62 topk 55 couv 0.8158 fr 43 / 43 en 19 / 19
sans_cand_prec vivant exact 195 / 196 topk 166 couv 0.8201 fr 135 / 135 en 60 / 61
sans_cand_prec gele exact 195 / 196 topk 166 couv 0.8201 fr 135 / 135 en 60 / 61
sans_cand_prec dev exact 133 / 134 topk 111 couv 0.8221 fr 92 / 92 en 41 / 42
sans_cand_prec test exact 62 / 62 topk 55 couv 0.8158 fr 43 / 43 en 19 / 19
sans_cible_prec vivant exact 160 / 196 topk 166 couv 0.8201 fr 115 / 135 en 45 / 61
sans_cible_prec gele exact 160 / 196 topk 166 couv 0.8201 fr 115 / 135 en 45 / 61
sans_cible_prec dev exact 105 / 134 topk 111 couv 0.8221 fr 77 / 92 en 28 / 42
sans_cible_prec test exact 55 / 62 topk 55 couv 0.8158 fr 38 / 43 en 17 / 19
  ```

### 🤖 Assistant

⏵ Vérification qualitative des cinq corrections v7 sur des exemples

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\ncas=[(\"Il entre en gare.\",\"fr\"),(\"L'oiseau vole au-dessus du lac.\",\"fr\"),\n     (\"He has b … [542 caractères tronqués]`

  ```
--- Il entre en gare. fr
POS [('Il', 'PRON'), ('entre', 'PREP'), ('en', 'PREP'), ('gare', 'NOUN')]
  GN 'Il' span 0 2 cible entre
  GV 'entre' span 3 8 cible None
  GV 'en gare' span 9 16 cible Il
  GP 'en gare' span 9 16 cible entre
--- L'oiseau vole au-dessus du lac. fr
POS [("L'", 'DET'), ('oiseau', 'NOUN'), ('vole', 'NOUN'), ('au-dessus', 'PREP'), ('du', 'PREP'), ('lac', 'NOUN')]
  GN "L'oiseau" span 0 8 cible vole
  GN "L'oiseau vole au-dessus" span 0 23 cible vole
  GV 'vole' span 9 13 cible None
  GP 'au-dessus du lac' span 14 30 cible vole
  GP 'du lac' span 24 30 cible vole
--- He has been here since yesterday. en
POS [('He', 'PRON'), ('has', 'AUX'), ('been', 'AUX'), ('here', 'ADV'), ('since', 'PREP'), ('yesterday', 'ADV')]
  GV 'He has been here' span 0 16 cible None
  GP 'since yesterday' span 17 32 cible here
--- The man who speaks English is here. en
POS [('The', 'DET'), ('man', 'NOUN'), ('who', 'PRON'), ('speaks', 'NOUN'), ('English', 'NOUN'), ('is', 'AUX'), ('here', 'ADV')]
  GN 'The man' span 0 7 cible here
  REL 'who speaks English' span 8 26 cible man
  GV 'is here' span 27 34 cible None
--- She said that she would come yesterday. en
POS [('She', 'PRON'), ('said',
… [221 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle du lexique verbal ajouté en v7 (français vs anglais)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"VERBES = \\|speak speaks\\|voler vole\\|VERBES\\[\" tools/bloc_linguistique.py | head -20; echo '---'; python3 - <<'PY'\nimport sys\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nfor m  … [326 caractères tronqués]`

  ```
319:VERBES = {
432:speak speaks spoke spoken speaking voler vole voles volent volait
595:        if n in VERBES.get(langue, VERBES["fr"]):
---
vole ('NOUN', True, 0.3) ('NOUN', True, 0.3) True
voler ('VERB', True, 0.4) ('VERB', True, 0.4) True
parle ('VERB', True, 0.72) ('NOUN', True, 0.3) True
speaks ('NOUN', True, 0.3) ('NOUN', True, 0.3) True
brother ('VERB', True, 0.4) ('VERB', True, 0.4) False
entre ('PREP', False, 0.92) ('NOUN', True, 0.3) True
fr verbs contains vole False
en verbs contains speaks False
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '319,440p' tools/bloc_linguistique.py", "description": "Inspect verb lexicons"}`

  ```
VERBES = {
    "fr": set("dort dorment dormait mange mangeons mangent mangeait court courent courait vu voir vois "
              "voit voyons voyez voient dit disons dites disent viendrait viens vient venons venez "
              "viennent aboie aboient joue jouons jouent jouait lit lisons lisez lisent pars partons "
              "partez partent fini finis finit finissons finissez finissent arrive arrives arrivez "
              "arrivent pleut pleuvoir habite habites habitent parle parlons parlez parlent explique "
              "expliquons expliquez expliquent souffle soufflent chante chantent chantes peut peux "
              "pouvons pouvez peuvent doit devons devez doivent pourrait pourrais pourrions pourriez "
              "pourraient devrait devrais voudrais voudrait veux veut voulons voulez veulent prend "
              "prends prenons prenez prennent donne donnes donnons donnez donnent trouve trouves "
              "trouvons trouvez trouvent cherche cherches cherchons cherchez cherchent regarde "
              "regardes regardons regardez regardent écoute écoutes écoutons écoutez écoutent ouvre "
              "ouvres ouvrons ouvrez ouvrent ferme fermes fermons fermez 
… [8086 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"would come\\|who speaks\\|au-dessus du lac\\|en gare\\|since yesterday\" tools/tests/linguistique/gold*.json | head -20", "description": "Find fiche example sentences in gold"}`

  ```
tools/tests/linguistique/gold_gele.json:1098:"texte": "She said that she would come yesterday.",
tools/tests/linguistique/gold_gele.json:1160:"texte": "that she would come",
tools/tests/linguistique/gold_gele.json:3034:"texte": "It rains since yesterday.",
tools/tests/linguistique/gold_gele.json:3078:"texte": "since yesterday",
tools/tests/linguistique/gold_gele.json:5075:"texte": "Les oiseaux volent au-dessus du lac.",
tools/tests/linguistique/gold_gele.json:5131:"texte": "au-dessus du lac",
tools/tests/linguistique/gold_gele.json:6609:"texte": "Le train entre en gare.",
tools/tests/linguistique/gold_gele.json:6659:"texte": "en gare",
tools/tests/linguistique/gold_gele.json:14350:"texte": "The man who speaks is my father.",
tools/tests/linguistique/gold_gele.json:14405:"texte": "who speaks",
tools/tests/linguistique/gold.json:1082:   "texte": "She said that she would come yesterday.",
tools/tests/linguistique/gold.json:1144:     "texte": "that she would come",
tools/tests/linguistique/gold_reel.json:1690:   "texte": "It rains since yesterday.",
tools/tests/linguistique/gold_reel.json:1734:     "texte": "since yesterday",
tools/tests/linguistique/gold_reel.json:3731:   "texte": "Le
… [437 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Analyse des phrases du gold citées par la fiche v7

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys,json\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger\nimport bloc_linguistique as bl\nh=bl.Heuristique(); ph=charger()\nfor p in ph:\n    if  … [731 caractères tronqués]`

  ```
=== g017 She said that she would come yesterday. en
gold: [('GN', 'She', None), ('GV', 'said', None), ('SUB', 'that she would come', 'said')]
pred: [('GV', 'said', None), ('SUB', 'that she', 'said'), ('GV', 'would come yesterday', None)]
POS: [('She', 'PRON'), ('said', 'VERB'), ('that', 'DET'), ('she', 'PRON'), ('would', 'AUX'), ('come', 'VERB'), ('yesterday', 'ADV')]
=== r025 She talks to her brother. en
gold: [('GN', 'She', None), ('GV', 'talks', None), ('GP', 'to her brother', 'talks')]
pred: [('GV', 'talks', None), ('GP', 'to her brother', 'talks')]
POS: [('She', 'PRON'), ('talks', 'NOUN'), ('to', 'PREP'), ('her', 'DET'), ('brother', 'NOUN')]
=== r028 It rains since yesterday. en
gold: [('GN', 'It', None), ('GV', 'rains', None), ('GP', 'since yesterday', 'rains')]
pred: [('GV', 'rains', None), ('GP', 'since yesterday', 'rains')]
POS: [('It', 'PRON'), ('rains', 'VERB'), ('since', 'PREP'), ('yesterday', 'ADV')]
=== r060 Les oiseaux volent au-dessus du lac. fr
gold: [('GN', 'Les oiseaux', None), ('GV', 'volent', None), ('GP', 'au-dessus du lac', 'volent')]
pred: [('GN', 'Les oiseaux', 'volent'), ('GN', 'Les oiseaux volent au-dessus', 'volent'), ('GV', 'volent', None), ('GP', 'au-d
… [889 caractères tronqués]
  ```

- **read** `{"file_path": "tools/bloc_linguistique.py", "limit": 80, "offset": 862}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
862:                 suivant = mots[i + 1] if i + 1 < len(mots) else None
863:                 # « since/before/after/until/as » : SUB devant une clause, PRÉP devant un GN
864:                 prep_ambigue = (n in AMBIGUES_PREP and (suivant is None
865:                                 or not (_normaliser(suivant[2]) in lex.get("PRON", set())
866:                                         or est_verbe(suivant[0], suivant[2]))))
867:                 ambigu = n in lex.get("DET", set())
868:                 marqueur = (not prep_ambigue) and ((not ambigu) or (suivant is not None and (
869:                     _normaliser(suivant[2]) in lex.get("PRON", set())
870:                     or _normaliser(suivant[2]) in lex.get("AUX", set())
871:                     or est_verbe(suivant[0], suivant[2]))))
872:                 if marqueur:
873:                     precedent = segments[-1]["type"] if segments else None
874:                     stype = "SUB" if (n in SUBORDONNANTS or precedent == "GV") else "REL"
875:                     j = i + 1
876:                     verbes_vus = 
… [4562 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des exemples POS « brother » et « chair »

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nfor txt,lg in [(\"She talks to her brother.\",\"en\"),(\"He sat on the chair.\",\"en\"),(\"The chai … [218 caractères tronqués]`

  ```
She talks to her brother. [('She', 'PRON', 0.92, None), ('talks', 'NOUN', 0.3, None), ('to', 'PREP', 0.92, None), ('her', 'DET', 0.92, None), ('brother', 'NOUN', 0.4, 'DET')]
He sat on the chair. [('He', 'PRON', 0.92, None), ('sat', 'NOUN', 0.3, None), ('on', 'PREP', 0.92, None), ('the', 'DET', 0.92, None), ('chair', 'NOUN', 0.4, 'DET')]
The chair is red. [('The', 'DET', 0.92, None), ('chair', 'NOUN', 0.4, 'DET'), ('is', 'AUX', 0.92, None), ('red', 'ADJ', 0.68, None)]
  ```

### 🤖 Assistant

⏵ Statistiques des listes de candidats pour interpréter le contrôle aléatoire

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys,statistics,collections\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger\nimport bloc_linguistique as bl\nh=bl.Heuristique(); lens=[]; has=0; n … [759 caractères tronqués]`

  ```
n 196 longueur moyenne 2.47 médiane 2.0 max 5
distribution [(2, 134), (3, 32), (4, 26), (5, 3), (1, 1)]
cible dans candidats 166 0.8469387755102041
  ```

### 🤖 Assistant

⏵ Permutation stratifiée par type et par langue (contrôle plus strict)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys,random,statistics\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger\nimport bloc_linguistique as bl\nh=bl.Heuristique(); recs=[]\nfor p in char … [1170 caractères tronqués]`

  ```
type mean 5.163 (0.0263) min 0 max 13
langue mean 3.468 (0.0177) min 0 max 13
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys,random,statistics\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger\nimport bloc_linguistique as bl\nh=bl.Heuristique(); recs=[]\nfor p in char … [1050 caractères tronqués]`

  ```
type+langue mean 9.397 (0.0479) min 2 max 20
  ```

### 🤖 Assistant

⏵ Consolidation des sorties de portes citées

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re,json\ncitees=['T86','T87','T88','T89','T90','T107','T110','T111','T112','T113','T114','T115','T119','T138','T141','T153','T156','T157','T161','T162','T163','T164','T166','T167','T168','T169','T171','T172', … [521 caractères tronqués]`

  ```
T86 {'ok': True, 'nom': 'sous-ensembles', 'message': 'r181-200 POS 0.8452 ; r001-180 POS 0.8221'}
T87 {'ok': True, 'nom': 'phrases complexes', 'message': 'r201-205 : POS 0.7353, syntagme 0.7027'}
T88 {'ok': True, 'nom': '20 complexes', 'message': 'r201-220 : POS 0.7236, syntagme 0.5954'}
T89 {'ok': True, 'nom': '50 complexes', 'message': 'r201-250 : POS 0.7327, syntagme 0.5839'}
T90 {'ok': True, 'nom': '100 complexes', 'message': 'r201-300 : POS 0.719, syntagme 0.5477'}
T107 {'ok': True, 'nom': 'gold complet', 'message': 'gold complet : 602 phrases, POS 0.7603, tête 0.7205'}
T110 {'ok': True, 'nom': 'segmenteur', 'message': 'segmenteur : S F1 0.4741 tête 0.6518 ; chunker F1 0.5858 tête 0.7441'}
T111 None
T112 None
T113 {'ok': True, 'nom': 'union par défaut', 'message': 'union par défaut : F1 0.5595, tête 0.7205'}
T114 {'ok': True, 'nom': 'cascade + union', 'message': 'cascade : F1 0.5864, tête 0.7285, 602 appels'}
T115 {'ok': True, 'nom': 'tête cascade', 'message': 'tête cascade corrigée : 0.6709 (cascade 0,441 ; union 0,466)'}
T119 None
T138 {'ok': True, 'nom': 'défaut fusion', 'message': 'défaut : confiance 0.7465, niveau 0.3454'}
T141 {'ok': True, 'nom': 'élision', 'message': 'é
… [1645 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Décomposition par langue de l'effet POS contextuel

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport importlib.util,sys,collections\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger,charger_gele\nimport bloc_linguistique as bl\ndef load(path,name): … [828 caractères tronqués]`

  ```
v7 gele {'fr': (1515, 2000, 0.7575), 'en': (873, 1141, 0.7651)}
sans_pos gele {'fr': (1511, 2000, 0.7555), 'en': (840, 1141, 0.7362)}
  ```

### 🤖 Assistant

⏵ Vérification que les deux fichiers d'audit sont neufs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l reports/rapport-audit-v7.md reports/pensee-audit-v7.json 2>&1; git status --short reports/ | head", "description": "Check audit files do not exist"}`

  ```
ls: cannot access 'reports/rapport-audit-v7.md': No such file or directory
ls: cannot access 'reports/pensee-audit-v7.json': No such file or directory
 M reports/pensee-quatre-modes.json
 M reports/rapport-spans-chunker.md
?? reports/rapport-dev-test-v7.md
?? reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' reports/rapport-dev-test-v7.md 2>/dev/null; echo '---'; sed -n '1,40p' reports/rapport-s-paragraphes.md 2>/dev/null", "description": "Peek at sibling untracked reports"}`

  ```
# B13 — dev/test en v7 : dev 133/134, test 62/62, le split tient sur trois découpages

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Commit mesuré** : `69bd865e` · **Verdict** : ✅
> Le gold 612 est re-coupé par `crc32(id) % 3 == 0` (test) : **dev 133/134 (0,9925)**, **test 62/62 (1,0)**
> — mais le test ne couvre que **62 des 76 cibles** (0,8158). En décalant le split (`%3==1`, `%3==2`),
> l'exact reste à **1 cas près** (étendue 0,0172), la couverture à **3 spans près** (14/13/16 des 43),
> la F1 à **2,4 points**. **Aucune catégorie demandée n'est absente** ; les écarts dev/test tiennent à
> **un échec unique (r102)** et à la **composition par type**, pas au split.
>
> **Dispositif** : [`gold_split.py`](../tools/tests/linguistique/gold_split.py) (`dev`, `test`, `compter`),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`),
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (heuristique) ; JSON
> [`pensee-dev-test-v7.json`](pensee-dev-test-v7.json).

## 1. Ce qui est mesuré

- **Corpus** : `charger()` = **612 phrases** (20 `hand`, 432 `reel`, 160 `synthetique`), 402 fr / 210 en,
  **239 ci
… [6130 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '80,200p' reports/rapport-dev-test-v7.md 2>/dev/null", "description": "Read rest of sibling dev/test report"}`

  ```
| `synthetique` (phrases) | 105 | 55 | 160 |
| fr (phrases) | 277 | 125 | 402 |
| en (phrases) | 145 | 65 | 210 |
| REL (cibles) | 57 | **17** | 74 |
| SUB (cibles) | 45 | 24 | 69 |
| GP (cibles) | 61 | 35 | 96 |

**Aucune catégorie demandée n'est absente d'une moitié** : les trois sources, les deux langues et les
trois types de cibles sont présents des deux côtés. Le χ² d'homogénéité du test canonique contre
l'ensemble ne rejette rien : sources χ²=0,93 (p=0,63), langues χ²=0,0009 (p=0,98), types de cibles
χ²=2,66 (p=0,26), types×langues χ²=3,49 (p=0,63) ; les splits décalés donnent des p entre 0,42 et 0,97.
L'équilibre tient donc **en espérance**, pas par construction : le hash n'est **pas stratifié**, il est
vérifié a posteriori.

Trois réserves de lecture, même sans catégorie absente :

- **`hand` est mince** : 5 phrases au test (4 au décalé 2, 11 au décalé 1), et **3 cibles seulement**,
  **toutes GP**. `hand/REL` (1 cible) et `hand/SUB` (2 cibles) sont entièrement dans dev. Les taux
  `hand` du test ne disent donc rien des REL/SUB.
- **REL/en est la cellule la plus mince** : 5 cibles au test (2 labels), contre 23 en dev. Toute
  conclusion sur l'anglais REL au test est fragile
… [7172 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Relevé des dénominateurs (tokens, segments) pour le rapport

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger,charger_gele,evaluer_bloc\nimport bloc_linguistique as bl\nfor nom,ph in [('vivant',charger() … [458 caractères tronqués]`

  ```
vivant phrases 612 tokens pos 3179 tokens gold 3179 segments gold 1863 pos ferme 0.9004 pos ouvert 0.6234
  pos ferme/ouvert counts? {'exactitude': 0.7581, 'exactitude_ferme': 0.9004, 'exactitude_ouvert': 0.6234, 'tokens': 3179, 'confusions': {'ADJ': {'ADJ': 50, 'NOUN': 80, 'VERB': 4}, 'ADV': {'ADV': 117, 'NOUN': 20, 'PREP': 2, 'ADJ': 1, '?': 1}, 'AUX': {'PREP': 4, 'AUX': 118, '?': 3, 'NOUN': 3}, 'CONJ': {'CONJ': 44, 'PRON': 25, 'DET': 12, '?': 13, 'PREP': 2, 'NOUN': 2}, 'DET': {'DET': 586, '?': 2}, 'NOUN': {'NOUN': 657, 'ADJ': 17, 'VERB': 7, '?': 1}, 'NUM': {'NUM': 2}, 'PONCT': {'?': 25}, 'PREP': {'PREP': 114}, 'PRON': {'PRON': 411, 'NOUN': 8, '?': 30, 'DET': 25, 'CONJ': 1}, 'VERB': {'VERB': 311, 'NOUN': 450, 'ADJ': 5, 'PREP': 2, '?': 16, 'AUX': 7, 'ADV': 1}}}
gele phrases 602 tokens pos 3141 tokens gold 3141 segments gold 1831 pos ferme 0.9007 pos ouvert 0.6269
  pos ferme/ouvert counts? {'exactitude': 0.7603, 'exactitude_ferme': 0.9007, 'exactitude_ouvert': 0.6269, 'tokens': 3141, 'confusions': {'ADJ': {'ADJ': 50, 'NOUN': 79, 'VERB': 4}, 'ADV': {'ADV': 115, 'NOUN': 20, 'PREP': 2, 'ADJ': 1, '?': 1}, 'AUX': {'PREP': 4, 'AUX': 116, '?': 3, 'NOUN': 3}, 'CONJ': {'CONJ': 44, 'PRON': 2
… [341 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Écriture du JSON d'audit structuré

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nD={\n \"audit\":\"v7\",\n \"commit\":\"69bd865ec1bae1958b6f617bde4bf685a15d7d67\",\n \"branche\":\"s/v7\",\n \"date\":\"2026-11-05\",\n \"ligne\":\"B13\",\n \"verdict\":\"Les chiffres de la fiche sont r … [20367 caractères tronqués]`

  ```
written reports/pensee-audit-v7.json 18934
JSON valide
  ```

### 🤖 Assistant

⏵ Correction du compte de docstrings et d'une coquille dans le JSON

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\np='reports/pensee-audit-v7.json'\nd=json.load(open(p,encoding='utf-8'))\nd['verdict']=d['verdict'].replace('20 docstrings','26 docstrings')\nd['limites']=[x.replace('La rege du sujet-verbe (`SUJETS`) su … [457 caractères tronqués]`

  ```
Les chiffres de la fiche sont reproductibles, mais cinq valeurs de qualite (POS, F1 union, S, chunker, tete) sont mesure
La regle du sujet-verbe (`SUJETS`) sur-promeut les mots apres « that/qui » : l'exemple g017 « that she would come » est coupe en « that she » ; d'autres phrases avec « that + pronom » peuvent etre touchees.
docstrings 26 messages 6
JSON valide
  ```

### 🤖 Assistant

⏵ Rédaction de la fiche d'audit v7

- **write** `{"file_path": "reports/rapport-audit-v7.md", "content": "# Audit v7 — 195/196 sur les deux golds, mais cinq valeurs de qualité sont gelées\n\n> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·\n> **Commit audité** : `69bd865e` (branche `s/v7`) · **Verdict** : ✅ ch … [31593 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Relecture de la fiche pour vérifier chiffres et cohérence

- **read** `{"file_path": "reports/rapport-audit-v7.md", "limit": 140}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md</path>
<type>file</type>
<content>
1: # Audit v7 — 195/196 sur les deux golds, mais cinq valeurs de qualité sont gelées
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
4: > **Commit audité** : `69bd865e` (branche `s/v7`) · **Verdict** : ✅ chiffres reproduits ;
5: > ⚠️ cinq valeurs sont mesurées sur le **gold gelé 602**, la colonne « avant » n'est pas la v6,
6: > et deux récits de la fiche sont faux.
7: >
8: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`Heuristique`,
9: > `_syntagmes_simple`, `_cible_precedent`, `_cible_hors_span`),
10: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`),
11: > [`gold_split.py`](../tools/tests/linguistique/gold_split.py) (`dev`, `test`),
12: > [`autotest.py`](../tools/pensee/autotest.py) (183 portes) · **JSON** :
13: > [`pensee-audit-v7.json`](pensee-audit-v7.json).
14: 
15: ## 1. Le verdict en une page
16: 
17: | question | réponse |
18: |---|---|
19: | les chiffres de la fiche sont-ils rejouables ? | **oui**, au commit `69bd865e`, sans modifier le c
… [7718 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-audit-v7.md", "limit": 180, "offset": 141}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md</path>
<type>file</type>
<content>
141: F1 tête.
142: 
143: ## 5. L'« avant » n'est pas la v6
144: 
145: La colonne « avant » du tableau de la fiche (et le bloc `avant` du JSON) mélange trois états :
146: 
147: | valeur « avant » | fiche | v6 vivant | v6 gelé | provenance réelle |
148: |---|---:|---:|---:|---|
149: | POS | 0,7475 | 0,7461 | 0,7482 | **v4 gelé** (0,7475) |
150: | F1 union | 0,5130 | **0,5130** | 0,5164 | **v6 vivant** |
151: | F1 tête | 0,6826 | 0,6785 | 0,6834 | **v5a gelé** (0,6826) |
152: | labels | 187 | 187 | 187 | v6 |
153: | exact | 187 | 187 | 187 | v6 |
154: | couverture | 0,7824 | 0,7824 | 0,7824 | v6 |
155: | spans | 52 | 52 | 52 | v6 |
156: 
157: Le POS 0,7475 est l'ancienne valeur de T107, mesurée sur le **v4**. La tête 0,6826 est l'ancienne
158: valeur de T113, mesurée sur le **v5a** (`7a9f0d6a`). Seule la F1 0,5130 est bien la v6, et elle est
159: mesurée sur le **vivant**. La v6, elle, donne :
160: 
161: | mesure | v6 vivant | v6 gelé |
162: |---|---:|---:|
163: | POS | 0,7461 | 0,7482 |
164: | F1 union | 0,5130 | 0,5164 |
165: | F1 tête | 0,6785 | 0,6834 |
166: | S | 0
… [9805 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-audit-v7.md", "limit": 230, "offset": 321}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md</path>
<type>file</type>
<content>
321: 
322: ### 8.1 Retirer la règle du segment précédent
323: 
324: Variante : `_cible_precedent` rend `None`, `_candidats_precedent` rend `[]`, et la branche inline
325: de la voie S (`if s.get("type") in ("REL", "SUB")`) est désactivée. Mesure sur le gelé 602 :
326: 
327: | variante | labels | exact | exact/labels | couverture | top-k | fr | en | dev | test |
328: |---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
329: | témoin | 196 | 195 | 0,9949 | 0,8201 | 166 | 135/135 | 60/61 | 133/134 | 62/62 |
330: | sans segment précédent | 196 | **160** | **0,8163** | 0,8201 | 166 | 115/135 | 45/61 | 105/134 | 55/62 |
331: 
332: La règle vaut **35 attachements exacts** (195 − 160), **20 en français**, **15 en anglais**,
333: **28 en dev**, **7 en test**. Elle ne change ni les labels, ni la couverture, ni le top-k, ni la
334: POS/F1/tête : c'est une règle d'attachement pur.
335: 
336: **La moitié « candidats du précédent » est redondante** : en ne retirant que
337: `_candidats_precedent` (la cible reste), **tous les chiffres sont identiques au témoin** (195/196,
338: top-k 
… [13299 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des spans exacts de g017 et des valeurs citées

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger\np=next(p for p in charger() if p['id']=='g017')\nprint(repr(p['texte']))\nfor s in p['segmen … [306 caractères tronqués]`

  ```
'She said that she would come yesterday.'
GN 0 3 'She' None
GV 4 8 'said' None
SUB 9 28 'that she would come' said
len 39

0 'S' 1 'h' 2 'e' 3 ' ' 4 's' 5 'a' 6 'i' 7 'd' 8 ' ' 9 't' 
10 'h' 11 'a' 12 't' 13 ' ' 14 's' 15 'h' 16 'e' 17 ' ' 18 'w' 19 'o' 
20 'u' 21 'l' 22 'd' 23 ' ' 24 'c' 25 'o' 26 'm' 27 'e' 28 ' ' 29 'y' 
30 'e' 31 's' 32 't' 33 'e' 34 'r' 35 'd' 36 'a' 37 'y' 38 '.'
  ```

### 🤖 Assistant

⏵ Vérification des cellules dev/test citées (REL/en, hand)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys,collections\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger\nfrom tools.tests.linguistique.gold_split import test,dev\nph=charger(); t=test(p … [1782 caractères tronqués]`

  ```
test cibles Counter({('fr', 'GP'): 24, ('fr', 'SUB'): 14, ('fr', 'REL'): 12, ('en', 'GP'): 11, ('en', 'SUB'): 10, ('en', 'REL'): 5})
dev cibles Counter({('fr', 'GP'): 38, ('fr', 'REL'): 34, ('fr', 'SUB'): 29, ('en', 'GP'): 23, ('en', 'REL'): 23, ('en', 'SUB'): 16})
hand test phrases 5 cibles 3
test
  ('en', 'GP') cibles 11 labels 10 exact 10
  ('en', 'REL') cibles 5 labels 2 exact 2
  ('en', 'SUB') cibles 10 labels 7 exact 7
  ('fr', 'GP') cibles 24 labels 22 exact 22
  ('fr', 'REL') cibles 12 labels 9 exact 9
  ('fr', 'SUB') cibles 14 labels 12 exact 12
dev
  ('en', 'GP') cibles 23 labels 23 exact 22
  ('en', 'REL') cibles 23 labels 13 exact 13
  ('en', 'SUB') cibles 16 labels 6 exact 6
  ('fr', 'GP') cibles 38 labels 36 exact 36
  ('fr', 'REL') cibles 34 labels 29 exact 29
  ('fr', 'SUB') cibles 29 labels 27 exact 27
  ```

### 🤖 Assistant

⏵ Corrections de précision dans la fiche (working tree, spans, flux dev/test)

- **edit** `{"file_path": "reports/rapport-audit-v7.md", "old_string": "- **Commit** : `git rev-parse HEAD` = `69bd865ec1bae1958b6f617bde4bf685a15d7d67`. Le working tree\n  ne portait que des journaux modifiés par la session ; aucun fichier de code, de gold ou de\n  `reports/` n'a été touché.", "new_string": "- … [281 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md has been updated successfully.
  ```

- **edit** `{"file_path": "reports/rapport-audit-v7.md", "old_string": "| T86-T90 | `gold_reel` (sous-ensembles) | POS 0,8452 / 0,7353 / 0,7236 / 0,7327 / 0,719 | idem | ✅ |", "new_string": "| T86-T90 | `gold_reel` (sous-ensembles) | T86 0,8452 / 0,8221 ; T87 0,7353 ; T88 0,7236 ; T89 0,7327 ; T90 0,719 | idem  … [7 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md has been updated successfully.
  ```

- **edit** `{"file_path": "reports/rapport-audit-v7.md", "old_string": "**Aucune assertion n'est fausse.** Les portes qui portent les cinq valeurs « gelées »\n(T107, T110-T115, T119) utilisent `charger_gele()` ; celles qui portent l'attachement\n(T138, T141, T153, T156, T157, T161-T164, T166-T169, T171-T173, T1 … [659 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md has been updated successfully.
  ```

- **edit** `{"file_path": "reports/rapport-audit-v7.md", "old_string": "- **dev/test** : aucune porte ne mesure `gold_split.dev` / `test`. Les 133/134 et 62/62 de la\n  fiche v7 (et de la v6) reposent sur des scripts ad hoc, pas sur le registre.", "new_string": "- **dev/test** : aucune porte ne mesure `gold_spl … [153 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md has been updated successfully.
  ```

- **edit** `{"file_path": "reports/rapport-audit-v7.md", "old_string": "- **par langue** (gelé) : français 0,7575 → 0,7555 (**−0,0020**), anglais 0,7651 → 0,7362\n  (**+0,0289**) ; le gain est massivement anglais ;", "new_string": "- **par langue** (gelé) : français 0,7555 → 0,7575 (**+0,0020**), anglais 0,7362 … [64 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md has been updated successfully.
  ```

- **edit** `{"file_path": "reports/rapport-audit-v7.md", "old_string": "- gold : `SUB « that she would come »` (span 9–29), cible `said` ;", "new_string": "- gold : `SUB « that she would come »` (span 9–28), cible `said` ;"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md has been updated successfully.
  ```

- **edit** `{"file_path": "reports/rapport-audit-v7.md", "new_string": "Le test gagne **un label** et reste parfait ; le dev gagne **8 labels** et **une erreur**. Le\nsolde est **+9 labels, +8 exacts**, mais il cache des flux : les 8 labels du POS contextuel sont\ntous dans dev, et l'erreur r102 aussi. Le test  … [882 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md has been updated successfully.
  ```

- **edit** `{"file_path": "reports/rapport-audit-v7.md", "new_string": "- les titres de v4 et v5 sont **périmés d'un label** ; pour v4, le corps et le JSON sont corrects ;\n  pour v5, le corps et le JSON **mélangent deux commits** (F1/tête de `7a9f0d6a`, exact/S/chunker\n  de `b975011b`), c'est le même type de  … [214 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md has been updated successfully.
  ```

- **edit** `{"file_path": "reports/rapport-audit-v7.md", "new_string": "Le total baisse de 9, mais les SUB manquantes **augmentent de 5**. La fiche ne le dit pas ; c'est\ncohérent avec les prépositions ambiguës et l'ordre GV/GP, sans que cet audit isole la cause. Le\nrésultat reste positif (le total baisse), ma … [457 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Correction d'une valeur de docstring T86 (0,7897 et non 0,7919)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -R \"0,7919\\|0.7919\" reports/rapport-audit-v7.md reports/pensee-audit-v7.json", "description": "Locate wrong T86 docstring value"}`

  ```
reports/rapport-audit-v7.md:| T86-T90 | POS 0,8214/0,7919, 0,6471, 0,6829, 0,7013, 0,6984 | 0,8452/0,8221, 0,7353, 0,7236, 0,7327, 0,719 |
reports/pensee-audit-v7.json:    "docstring": "perimee (0.8214 / 0.7919)"
  ```

- **edit** `{"file_path": "reports/rapport-audit-v7.md", "new_string": "| T86-T90 | POS 0,8214/0,7897, 0,6471, 0,6829, 0,7013, 0,6984 | 0,8452/0,8221, 0,7353, 0,7236, 0,7327, 0,719 |", "old_string": "| T86-T90 | POS 0,8214/0,7919, 0,6471, 0,6829, 0,7013, 0,6984 | 0,8452/0,8221, 0,7353, 0,7236, 0,7327, 0,719 |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\np='reports/pensee-audit-v7.json'\nd=json.load(open(p,encoding='utf-8'))\nfor g in d['portes']['citees']:\n    if g['id']=='T86':\n        g['docstring']='perimee (0.8214 / 0.7897)'\nopen(p,'w',encoding= … [211 caractères tronqués]`

  ```
ok
JSON valide
  ```

### 🤖 Assistant

⏵ Contrôle final des fichiers écrits et de l'absence de modification existante

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | grep -E \"rapport-audit-v7|pensee-audit-v7\" ; echo '---'; git status --short reports/ | head -20; echo '---'; git diff --stat | tail -5", "description": "Check git status for new audit files"}`

  ```
?? reports/pensee-audit-v7.json
?? reports/rapport-audit-v7.md
---
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-spans-chunker.md
?? reports/pensee-audit-v7.json
?? reports/rapport-audit-v7.md
?? reports/rapport-s-paragraphes.md
---
 reports/pensee-quatre-modes.json                   |  734 +-
 reports/rapport-coherence-fiches-v7.md             |   17 +-
 reports/rapport-spans-chunker.md                   |   13 +-
 tools/structures                                   |    0
 24 files changed, 9763 insertions(+), 394 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l reports/rapport-audit-v7.md && python3 -m json.tool reports/pensee-audit-v7.json > /dev/null && echo 'JSON valide' && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-v7.json',encoding='utf-8'))\nprint('clé … [480 caractères tronqués]`

  ```
547 reports/rapport-audit-v7.md
JSON valide
clés ['audit', 'commit', 'branche', 'date', 'ligne', 'verdict', 'gold', 'revendications', 'avant', 'portes', 'controles_negatifs', 'ablations', 'dev_test', 'amont', 'limites']
verdict Les chiffres de la fiche sont reproductibles, mais cinq valeurs de qualite (POS, F1 union, S, chunke ...
portes 183 183 0
citees 32 docstrings 26 messages 6
dev/test 133 134 62 62
  ```

- **edit** `{"file_path": "reports/rapport-audit-v7.md", "new_string": "- **POS vivant 0,7581 et F1 vivant 0,5555** : T141 couvre la POS vivante, T112/T113 couvrent la\n  F1 gelée, mais aucune porte n'associe les deux valeurs vivantes dans un même snapshot. Celui qui\n  rejoue `evaluer_gold.py` obtient 0,5555/0 … [370 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md has been updated successfully.
  ```

- **edit** `{"file_path": "reports/rapport-audit-v7.md", "new_string": "tous dans dev, et l'erreur r102 aussi. Le test ne montre donc **aucun** des 8 labels du POS\ncontextuel ; l'ablation du précédent en retire 7 au test, ce qui valide cette règle-là mais pas le\ngain POS. C'est un point de lecture important : … [523 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Vérification des liens relatifs de la fiche d'audit

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re,pathlib\np=pathlib.Path('reports/rapport-audit-v7.md')\ntxt=p.read_text(encoding='utf-8')\nliens=re.findall(r'\\[[^\\]]+\\]\\(([^)]+)\\)',txt)\nfor l in liens:\n    if l.startswith('http') or l.startswith( … [203 caractères tronqués]`

  ```
OK  ../tools/bloc_linguistique.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py
OK  ../tools/tests/linguistique/evaluer_gold.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py
OK  ../tools/tests/linguistique/gold_split.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_split.py
OK  ../tools/pensee/autotest.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py
OK  pensee-audit-v7.json -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-audit-v7.json
OK  ../tools/bloc_linguistique.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py
OK  ../tools/tests/linguistique/evaluer_gold.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py
OK  ../tools/tests/linguistique/gold_split.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_split.py
OK  ../tools/pensee/autotest.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py
OK  rapport-pensee-couverture-v7.md -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-
… [501 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Ajout d'une note sur la différence T163 (30) vs T172 (1)

- **edit** `{"file_path": "reports/rapport-audit-v7.md", "new_string": "**Aucune assertion n'est fausse.** Deux portes qui semblent se contredire ne mesurent pas la même\nchose : **T163** compte les **30 labels** (justes ou faux) dont la cible n'est pas dans\n`candidats` ; **T172** ne compte que les **échecs d' … [264 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Contrôle de la liste des docstrings périmées et des messages faux dans le JSON

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-v7.json',encoding='utf-8'))\nprint('docstrings',len(d['portes']['docstrings_perimees']),d['portes']['docstrings_perimees'])\nprint('messages',len(d['portes']['mess … [150 caractères tronqués]`

  ```
docstrings 26 ['T86', 'T87', 'T88', 'T89', 'T90', 'T107', 'T110', 'T111', 'T112', 'T113', 'T114', 'T115', 'T119', 'T138', 'T141', 'T153', 'T156', 'T157', 'T162', 'T163', 'T166', 'T167', 'T172', 'T173', 'T177', 'T179']
messages 6 ['T161 (tete 195/145)', 'T162 (tete 167/145)', 'T168 (exact 195/145)', 'T171 (exact 195/145)', 'T177 (166/145)', 'T179 (195/145, exact_any 195/145)']
citees 32
  ```

### 🤖 Assistant

⏵ Ajout d'une note sur les portes d'instantané (T154/T155/T175)

- **edit** `{"file_path": "reports/rapport-audit-v7.md", "new_string": "- **T114/T115/T119/T138/T156/T157** : valeurs recalées par le commit, mais aucune n'apparaît dans\n  la fiche v7. Ce n'est pas une faute — la fiche ne prétend pas tout dire — mais le « 183/183 »\n  couvre plus que les 14 lignes du tableau.\ … [534 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v7.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-attachement.json',encoding='utf-8'))\nm=d['mesure']\nprint({k:m[k] for k in ('cibles','labels','top1','topk_sous_chaine','exact','topk_strict')})\nprint('verdict', … [65 caractères tronqués]`

  ```
{'cibles': 239, 'labels': 145, 'top1': 126, 'topk_sous_chaine': 134, 'exact': 123, 'topk_strict': 88}
verdict {'statut': 'reproduit', 'valeurs_publiees': 14, 'valeurs_reproduites': 14, 'ecarts': 0, 'reserve': "3 JSON sur 5 (conventions, attachement-cible, spans) sont des instantanés antérieurs, reproduits à leur commit mais pas à l'état courant ; dans sa version committée, pensee-spans.json publie 12 GP / 93 spans dans son bloc `spans`, pas 13 / 94. L'audit n'a modifié aucun fichier existant et n'a fait aucun commit."}
  ```

### 🤖 Assistant

⏵ Contrôle final de cohérence JSON ↔ mesures

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-v7.json',encoding='utf-8'))\nfor k,v in d['revendications'].items():\n    print(k, v.get('fiche'), v.get('vivant'), v.get('gele'), v.get('ecart_vivant'), v.get('st … [578 caractères tronqués]`

  ```
labels 196 196 196 0 ok
exact 195 195 195 0 ok
exact_taux_span 0.9949 0.9949 0.9949 0.0 ok
couverture 0.8201 0.8201 0.8201 0.0 ok
topk 166 166 166 0 ok
topk_taux 0.6946 0.6946 0.6946 0.0 ok
pos 0.7603 0.7581 0.7603 -0.0022 gele seulement
f1 0.5595 0.5555 0.5595 -0.004 gele seulement
f1_s 0.4741 0.4688 0.4741 -0.0053 gele seulement
f1_chunker 0.5858 0.5822 0.5858 -0.0036 gele seulement
tete 0.7205 0.7152 0.7205 -0.0053 gele seulement
fr 135/135 135/135 135/135 0 ok
en 60/61 60/61 60/61 0 ok
spans {'REL': 21, 'SUB': 17, 'GP': 5, 'total': 43} {'REL': 21, 'SUB': 17, 'GP': 5, 'total': 43} {'REL': 21, 'SUB': 17, 'GP': 5, 'total': 43} 0 ok
--- avant
{'pos': 0.7475, 'f1': 0.513, 'tete': 0.6826, 'labels': 187, 'exact': 187, 'couverture': 0.7824, 'spans': 52}
{'vivant': {'phrases': 612, 'pos': 0.7461, 'f1': 0.513, 'tete': 0.6785, 'labels': 187, 'exact': 187, 'couverture': 0.7824, 'spans': 52, 'topk': 161}, 'gele': {'phrases': 602, 'pos': 0.7482, 'f1': 0.5164, 'tete': 0.6834, 'labels': 187, 'exact': 187, 'couverture': 0.7824, 'spans': 52, 'topk': 161}}
--- portes
183 183 0
--- negatifs
permutation_cibles 1.807 0.0092 7
permutation_cibles_par_type 5.163 0.0263 13
permutation_cibles_par_langue 
… [454 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Enrichissement du JSON pour les deux ablations fines

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json,copy\np='reports/pensee-audit-v7.json'\nd=json.load(open(p,encoding='utf-8'))\na=d['ablations']\n# sans_cible_precedent = sans_segment_precedent (mêmes chiffres), on garde la note\ncible=copy.deepcopy(a[ … [1032 caractères tronqués]`

  ```
ok
JSON valide
sans_cible_precedent {'pos': 0.7603, 'f1': 0.5595, 'tete': 0.7205, 'labels': 196, 'exact': 160, 'exact_span': 0.8163, 'couverture': 0.8201, 'topk': 166, 'fr': [115, 135], 'en': [45, 61]} {'labels': 134, 'exact': 105, 'f1': 0.5512, 'couverture': 0.8221, 'topk': 111} {'labels': 62, 'exact': 55, 'f1': 0.5651, 'couverture': 0.8158, 'topk': 55}
sans_candidats_precedent {'pos': 0.7603, 'f1': 0.5595, 'tete': 0.7205, 'labels': 196, 'exact': 195, 'exact_span': 0.9949, 'couverture': 0.8201, 'topk': 166, 'fr': [135, 135], 'en': [60, 61]} {'labels': 134, 'exact': 133, 'f1': 0.5512, 'couverture': 0.8221, 'topk': 111} {'labels': 62, 'exact': 62, 'f1': 0.5651, 'couverture': 0.8158, 'topk': 55}
  ```

### 🤖 Assistant

⏵ Vérification : r102 est-il un label nouveau ou un label cassé par le POS contextuel ?

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport importlib.util,sys\nsys.path.insert(0,'.'); sys.path.insert(0,'tools')\nfrom tools.tests.linguistique.evaluer_gold import charger\nimport bloc_linguistique as bl\nspec=importlib.util.spec_from_file_location(' … [863 caractères tronqués]`

  ```
v7 label? True cible None candidats ['GP']
  segments [('GN', 'The rain falls'), ('GP', 'since this morning')]
  POS [('The', 'DET'), ('rain', 'VERB'), ('falls', 'NOUN'), ('since', 'PREP'), ('this', 'DET'), ('morning', 'NOUN')]
sans_pos label? False cible None candidats None
  segments [('GN', 'The rain falls'), ('GP', 'since this'), ('GV', 'morning')]
  POS [('The', 'DET'), ('rain', 'VERB'), ('falls', 'NOUN'), ('since', 'PREP'), ('this', 'DET'), ('morning', 'VERB')]
  ```

