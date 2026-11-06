# Session DSH — relecture

- identifiant : `ea169cb1-75d7-43fa-b69d-5e2a210f6c38`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 23:24:20
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer l'état v10** (commit `710ec7f9`) et vérifier que ses chiffres, ses règles et ses portes sont justes.

Contexte : `tools/bloc_linguistique.py` (`Heuristique`, `_syntagmes_simple`, `est_verbe` avec garde PRON, `est_sub`, boucle REL/SUB avec `predicat_vu`, `_est_verbe` avec `-ée`), `tools/tests/linguistique/evaluer_gold.py`, `gold_split.py` (dev/test), `tools/pensee/autotest.py` (183 portes). Fiches à auditer : `reports/rapport-pensee-v9.md` + `reports/pensee-v9.json`, `reports/rapport-pensee-v10.md` + `reports/pensee-v10.json`.

Revendications à rejouer (au commit `710ec7f9`) : labels 220, exact 220 (1,0000), couverture 0,9205, F1 union 0,5880 (S 0,5014, chunker 0,6203), tête 0,7388, fr 134/134, en 86/86, spans 19 (9 REL, 6 SUB, 4 GP), top-k 219.

À faire :
1. Rejoue chaque valeur (vivant 612 et gelé 602) et compare aux fiches/JSON ; note les écarts.
2. **Ablations** : mesure chaque correction séparément (garde PRON, `est_sub`, `predicat_vu`, `-ée`, garde DET du GP) sur le gold 612 et sur dev/test — gains/pertes, ids.
3. **Contrôles négatifs** : permutation globale des cibles (≥200 tirages), candidat aléatoire, et vérifie que les 19 spans restants sont bien ceux listés.
4. **dev/test** : re-mesure les deux moitiés (les valeurs publiées 152/152 et 67/67 datent d'avant les deux dernières corrections).
5. Écris **uniquement** deux fichiers neufs : `reports/rapport-audit-v10.md` et `reports/pensee-audit-v10.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé avec les écarts, les ablations et les valeurs dev/test.
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

⏵ Exploring repo state and audit targets

- **bash** `{"command": "git status --short && git branch --show-current && git log --oneline -5 && git rev-parse HEAD", "description": "Check git status, branch, recent commits", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

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
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
D  journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/digest.md
D  journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/rapport.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rapport.md
D  journal/sessions/24001907-4f19-4ea5-87f6-98334496719f/digest.md
D  journal/sessions/24001907-4f19-4ea5-87f6-98334496719f/rapport.md
D  journal/sessions/24529ced-6556-4491-9633-9401c2dffb0c/digest.md
D  journal/sessions/24529ced-6556-4491-9633-9401c2dffb0c/rapport.md
D  journal/sessions/2cc1ad4a-373e-4362-a341-3c4a630c2e0c/digest.md
D  journal/sessions/2cc1ad4a-373e-4362-a341-3c4a630c2e0c/rapport.md
D  journal/sessions/3144cf23-6004-46ef-bc3d-f05d81c0cf
… [4908 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -i pensee; echo '---'; ls tools/tests/linguistique/; echo '---'; ls tools/pensee/ | head -50", "description": "List relevant reports and test dirs", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
native-pensee.json
pas-de-pensee-14b.json
pas-de-pensee-7b.json
pas-de-pensee-contracte-3b.json
pas-de-pensee-contracte-7b.json
pas-de-pensee-corrige-14b.json
pas-de-pensee-corrige-3b.json
pas-de-pensee-corrige-7b.json
pas-de-pensee-corrige-large.json
pas-de-pensee.json
pas-de-pensee-mlp-18.json
pas-de-pensee-mlp-6.json
pas-de-pensee-non-lineaire-3b.json
pas-de-pensee-non-lineaire-large.json
pas-de-pensee-recurrent.json
pensee-absents.json
pensee-ac3-alphabeta.json
pensee-adaptive.json
pensee-aleatoire.json
pensee-alternance.json
pensee-anaphore-103.json
pensee-anaphore-68.json
pensee-anaphore-bilan.json
pensee-anaphore-chaines.json
pensee-anaphore-corrige.json
pensee-anaphore-cv-graines.json
pensee-anaphore-cv.json
pensee-anaphore-hybride.json
pensee-anaphore.json
pensee-anaphore-kappa.json
pensee-anaphore-limite.json
pensee-anaphore-meta.json
pensee-anaphore-objets.json
pensee-anaphore-pieges.json
pensee-anaphore-pondere.json
pensee-anaphore-roles.json
pensee-anaphore-semantique.json
pensee-annotation-independante.json
pensee-asym.json
pensee-attachement-cible.json
pensee-attachement.json
pensee-attachement-parfait.json
pensee-attachement-v2.json
pensee-attachement-v3.json
pensee
… [12241 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading v9/v10 fiches and JSON

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-v10.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-v10.md</path>
<type>file</type>
<content>
1: # B13 — 220/220 (1,0000), couverture 0,9205 : le féminin `-ée` et la garde déterminant du GP
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
4: > **État courant** · **Verdict** : ✅
5: > **183/183 portes** : deux corrections générales — le **féminin `-ée`** des participes
6: > (`achetée` → `acheter`) et la **garde déterminant** du GP (A17 R3b : un « verbe » précédé d'un
7: > déterminant est un nom, `for the bus`) — portent l'attachement à **220/220 (1,0000)** sur les
8: > **220 labels** prédits (sur 239), **couverture 0,9205**, **F1 0,5880** (union ; S 0,5014,
9: > chunker 0,6203), tête **0,7388** ; **fr 134/134**, **en 86/86** ; **19 spans** restants
10: > (9 REL, 6 SUB, 4 GP). **dev 152/152, test 67/67** (avant ces deux corrections).
11: >
12: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_est_verbe`, boucle GP),
13: > [`autotest.py`](../tools/pensee/autotest.py) (19 assertions) ;
14: > JSON [`pensee-v10.json`](pensee-v10.json).
15: 
16: ## 1. Les deux corrections
17: 
18: | # | correc
… [2615 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"\nimport json\nfor f in ['reports/pensee-v10.json','reports/pensee-v9.json']:\n    d=json.load(open(f))\n    print('===',f, type(d))\n    print(json.dumps(d, ensure_ascii=False, indent=1)[:6000])\n\"", "description": "Dump v10 and v9 JSON", "workdir": "/home/stephane/Data13 … [28 caractères tronqués]`

  ```
=== reports/pensee-v10.json <class 'dict'>
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "183/183",
 "avant": {
  "labels": 219,
  "exact": 219,
  "couverture": 0.9163,
  "f1": 0.5822,
  "spans": 20
 },
 "apres": {
  "labels": 220,
  "exact": 220,
  "exact_span": 1.0,
  "couverture": 0.9205,
  "f1": 0.588,
  "f1_s": 0.5014,
  "f1_chunker": 0.6203,
  "tete": 0.7388,
  "fr": "134/134",
  "en": "86/86",
  "topk": 219,
  "topk_taux": 0.9163,
  "spans": {
   "REL": 9,
   "SUB": 6,
   "GP": 4,
   "total": 19
  }
 },
 "corrections": [
  "féminin -ée des participes",
  "garde déterminant du GP (A17 R3b)"
 ],
 "limites": [
  "19 spans",
  "in-sample",
  "lexique"
 ]
}
=== reports/pensee-v9.json <class 'dict'>
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "183/183",
 "avant": {
  "labels": 212,
  "exact": 212,
  "couverture": 0.887,
  "f1": 0.5763,
  "spans": 27
 },
 "apres": {
  "labels": 219,
  "exact": 219,
  "exact_span": 1.0,
  "couverture": 0.9163,
  "f1": 0.5822,
  "f1_s": 0.5006,
  "f1_chunker": 0.6178,
  "tete": 0.7381,
  "fr": "134/134",
  "en": "85/85",
  "topk": 218,
  "topk_taux": 0.9121,
  "spans": {
   "REL": 9,
   "SUB": 6,
   "GP": 5,
   "total": 20
  },
  "dev
… [362 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Locating the scripts that produced v10 numbers

- **bash** `{"command": "grep -rn \"pensee-v10\\|v10\" --include=*.py --include=*.sh --include=*.md tools/ reports/rapport-pensee-v10.md docs/pilotage/en-cours.md 2>/dev/null | head -40", "description": "Find v10 generation references", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/rich/filesize.py:65:    or used by **Mac OS X** since v10.6 to report file sizes.
tools/docwatch/.venv/lib/python3.13/site-packages/markdown_it/common/utils.py:259:    # In node v10 'ẞ'.toLowerCase() === 'Ṿ', which is presumed to be a bug
tools/docwatch/.venv/lib/python3.13/site-packages/markdown_it/common/utils.py:263:    # (remove this when node v10 is no longer supported).
tools/docwatch/.venv/lib/python3.13/site-packages/rich/filesize.py:65:    or used by **Mac OS X** since v10.6 to report file sizes.
tools/r13_anglais.py:97:        v1024 = tokeniser(val, 1024, d, "val", tokenizer=d / "train-1024.json")
tools/r13_anglais.py:99:              f"val BPE 512 {v512['jetons']} · BPE 1024 {v1024['jetons']} jetons", flush=True)
tools/r13_anglais.py:115:                          (v512 if vocab == 512 else v1024)["octets"], vocab,
tools/r13_anglais.py:137:                    "bpe1024_val_jetons": v1024["jetons"]},
reports/rapport-pensee-v10.md:14:> JSON [`pensee-v10.json`](pensee-v10.json).
reports/rapport-pensee-v10.md:25:| mesure | v9 | **v10** |
reports/rapport-pensee-v10.md:74:- [`pensee-v10.json`](pensee-v10.json) — les c
… [8 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-v9.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-v9.md</path>
<type>file</type>
<content>
1: # B13 — la garde PRON : exact 219/219 (1,0000), couverture 0,9163, F1 0,5822
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
4: > **État courant** · **Verdict** : ✅
5: > **183/183 portes** : trois corrections issues de l'audit A19 réparent les **7 régressions** de la
6: > fiche [R1/R3](rapport-pensee-r1r3.md) et rouvrent trois spans : **la garde PRON** (A17 R1a
7: > fidèle : un pronom n'est jamais un verbe par position), **`est_sub`** (subordonnants par langue
8: > dans **toutes** les branches, pas seulement la branche REL/SUB) et **`predicat_vu`** pour
9: > l'adverbe final. Résultat : **219 labels** sur 239, **exact 219/219 = 1,0000** (fr **134/134**,
10: > en **85/85**), **couverture 0,9163**, **F1 0,5822** (union ; S 0,5006, chunker 0,6178), tête
11: > **0,7381** ; **20 spans** restants (9 REL, 6 SUB, 5 GP). **dev 152/152, test 67/67.**
12: >
13: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`est_verbe` garde PRON,
14: > `est_sub`, boucle REL/SUB), [`autotest.py`](../tools/pensee/autot
… [3762 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the linguistic bloc and evaluator

- **bash** `{"command": "wc -l tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/gold_split.py tools/pensee/autotest.py reports/rapport-audit-r1r3.md; echo '---'; grep -rn \"f1_chunker\\|topk\\|tete\\|union\" --include=*.py tools/ | grep -v site-packages | head -40", " … [120 caractères tronqués]`

  ```
2188 tools/bloc_linguistique.py
   305 tools/tests/linguistique/evaluer_gold.py
    50 tools/tests/linguistique/gold_split.py
  2836 tools/pensee/autotest.py
   460 reports/rapport-audit-r1r3.md
  5839 total
---
tools/aiguille.py:44:AIGUILLE = f" Pour memoire, le code de verification de la reunion est {CODE}. "
tools/aiguille.py:45:QUESTION = ("Quel est le code de verification de la reunion ? "
tools/aiguille.py:79:    if args.gpu_topk:
tools/aiguille.py:90:    if args.attn_topk > 0:
tools/aiguille.py:91:        cmd += ["--attn-topk", str(args.attn_topk)]
tools/aiguille.py:99:    # Le moteur DIT quand un drapeau ne s'applique pas (« --attn-topk ... est
tools/aiguille.py:140:    ap.add_argument("--attn-topk", type=int, default=0,
tools/aiguille.py:141:                    help="--attn-topk N (0 = attention complète)")
tools/aiguille.py:142:    ap.add_argument("--gpu-topk", action="store_true",
tools/aiguille.py:146:    # `--gpu-topk` sans `--attn-topk` affichait « top-k déporté » alors que le
tools/aiguille.py:149:    if args.gpu_topk and args.attn_topk <= 0:
tools/aiguille.py:150:        ap.error("--gpu-topk exige --attn-topk N (sinon le moteur ne déporte rien)")
tools/aiguille.py:1
… [2470 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py"}`

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

### 🤖 Assistant

⏵ Finding F1 union protocol and prior audit method

- **bash** `{"command": "grep -rn \"0[,.]5880\\|0[,.]588\\|union\" reports/rapport-audit-r1r3.md reports/rapport-pensee-v8.md 2>/dev/null | head -40; echo '---'; grep -rln \"0\\.5880\\|0,5880\" --include=*.py --include=*.md --include=*.json . 2>/dev/null | grep -v site-packages | head -20", "description": "Sear … [99 caractères tronqués]`

  ```
reports/rapport-audit-r1r3.md:59:| F1 union | 0,5763 | 0,5720 | **0,5763** | 0 sur la base gelée |
reports/rapport-audit-r1r3.md:84:| F1 union | 0,5595 | 0,5555 | **0,5595** | 0 sur la base gelée |
reports/rapport-audit-r1r3.md:98:`phrase:type`. F1 = union, vivant 612 (base 0,5720).
---
./reports/rapport-pensee-v10.md
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
./journal/sessions/3fb87dc7-7d24-42e2-a68e-e37e2734b755/digest.md
./journal/THEMES.md
./journal/2026-11-05/README.md
./journal/2026-11-05/mesures.md
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-r1r3.md", "limit": 200}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-r1r3.md</path>
<type>file</type>
<content>
1: # Audit R1/R2/R3 — les chiffres rejouent, l'attribution des règles ne rejoue pas
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
4: > **Commit audité** : `f908d7b0613c8a5eb8fae7fab514bfdc5fa4668b` (parent `69bd865ec1bae1958b6f617bde4bf685a15d7d67`) ·
5: > **HEAD observé en fin de rédaction** : `b551cf3b` (journal/état, sans `tools/`) — l'audit reste ancré sur `f908d7b0` ·
6: > **Date** : 2026-11-05 · **Verdict** : chiffres ✅, règles ❌.
7: > **Aucun fichier existant modifié ; aucun commit.** Sorties : ce rapport et
8: > [`pensee-audit-r1r3.json`](pensee-audit-r1r3.json).
9: 
10: **En une phrase.** Les **valeurs** de la fiche [`rapport-pensee-r1r3.md`](rapport-pensee-r1r3.md)
11: et de [`pensee-r1r3.json`](pensee-r1r3.json) rejouent **toutes** au chiffre près (212/212,
12: 0,8870, 0,5763, 27 spans, 177 top-k, 183/183 portes). Mais la **table des règles** ne rejoue
13: pas : elle annonce **+27 exacts** (donc 222), alors que le code livré en produit **+24 gains
14: bruts pour 7 pertes**, soit **+17** (212). R1a perd **6 s
… [12405 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the rest of the prior audit protocol

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-r1r3.md", "offset": 201, "limit": 260}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-r1r3.md</path>
<type>file</type>
<content>
201: 
202: ### 4.1 Arithmétique des ensembles
203: 
204: ```
205: exacts : 195 (v7) − 7 (régressions nouvelles) + 23 (des 26 gains A17) + 1 (r102 corrigé) = 212
206: labels : 196 (v7) − 7 (régressions nouvelles) + 23 (des 26 gains A17)                      = 212
207: ```
208: 
209: - **7 régressions nouvelles** (toutes françaises, toutes REL, toutes exactes en v7) :
210:   `r273 s032 s037 s069 s072 s115 s135` — 6 dues à R1a, 1 à R2 (`s037`).
211: - **26 gains A17** : 20 R1 + 4 R2 (dont `r245` avec R3c) + 1 R3a (`r280`) + 1 R3b (`r153`).
212:   **23 sont intégrés** ; les 3 manquants sont `g017` (R1c), `r153` (R3b absent), `r280`
213:   (R3a inerte).
214: - **`r102`** n'était pas un span manquant : il avait un label avec la mauvaise cible ; R3c le
215:   corrige (+1 exact, +0 label).
216: 
217: A17 attendait **222 exacts / 222 labels** (195+27 et 196+26) ; le code livré donne **212**.
218: L'écart de 10 = **7 régressions + 3 gains A17 non intégrés**.
219: 
220: ### 4.2 Les 27 spans, classés
221: 
222: | classe | n | types | identifiants |
223: |---|---:|---|---|
224:
… [16693 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Hunting the F1 union / S / chunker harness

- **bash** `{"command": "grep -rln \"0\\.4966\\|0,4966\\|0\\.5763\\|0,5763\" --include=*.py . 2>/dev/null | grep -v site-packages | head; echo '--- json files with f1_s ---'; grep -rln \"f1_s\" --include=*.json . 2>/dev/null | grep -v site-packages | head; echo '--- audits json ---'; python3 -c \"\nimport json\ … [230 caractères tronqués]`

  ```
--- json files with f1_s ---
./reports/pensee-coherence-fiches.json
./reports/pensee-segmentation-v4.json
./reports/pensee-couverture-v5.json
./reports/pensee-couverture-v7.json
./reports/pensee-audit-v7.json
./reports/pensee-audit-r1r3.json
./reports/pensee-coherence-fiches-v8.json
./reports/pensee-v9.json
./reports/pensee-v10.json
--- audits json ---
{
 "rapport": "audit-r1r3",
 "ligne": "B13",
 "branche": "s/v7",
 "commit_audite": "f908d7b0613c8a5eb8fae7fab514bfdc5fa4668b",
 "commit_parent": "69bd865ec1bae1958b6f617bde4bf685a15d7d67",
 "date": "2026-11-05",
 "objet": "Audit du round R1/R2/R3 : rejeu des valeurs, ablations par règle, contrôles négatifs, dev/test, portes.",
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
  "ablations": "copie du modu
… [3155 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"union\\|chunker\\|def f1\\|F1\" --include=*.py tools/tests/linguistique/ tools/bloc_linguistique.py | head -50", "description": "Search chunker and union in test tools", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
tools/tests/linguistique/qualifier_quatre_modes.py:12:Mêmes mesures que la cascade : POS, syntagmes F1, tête F1, acte, fraction, refus.
tools/tests/linguistique/gold_split.py:10:dans la fiche. Aucune phrase n'est dupliquée entre les deux ; l'union redonne les 612.
tools/bloc_linguistique.py:529:                 union: bool = True):
tools/bloc_linguistique.py:534:        self.union = union
tools/bloc_linguistique.py:1082:        # 5. syntagmes : le générateur S (candidats) ou un chunker simple
tools/bloc_linguistique.py:1086:        # l'interroge que pour le français, sinon ses segments polluent l'union.
tools/bloc_linguistique.py:1090:        # **un seul chunking par analyse**, partagé par les trois chemins (S, union, chunker) :
tools/bloc_linguistique.py:1174:        # 5 bis. union : les segments du chunker que le générateur S ne fournit pas
tools/bloc_linguistique.py:1175:        if cands and self.union:
tools/bloc_linguistique.py:1185:                meta = {"role": s["role"], "niveau": s["niveau"], "union": True}
  ```

### 🤖 Assistant

⏵ Mapping the bloc's classes and key functions

- **bash** `{"command": "grep -n \"^class \\|^    def \\|^def \\|PRON\\b\\|SUJETS\\|SUBORDONNANTS\\|RELATIFS\\|MODAUX\\|VERBES_CONNUS\\|_est_verbe\\|def est_verbe\\|def _syntagmes_simple\" tools/bloc_linguistique.py | head -120", "description": "Outline bloc_linguistique", "workdir": "/home/stephane/Data13TB/st … [23 caractères tronqués]`

  ```
59:class Span:
63:    def json(self) -> dict:
68:class Etiquette:
81:    def json(self) -> dict:
92:class Annotation:
105:    def par_niveau(self) -> dict[str, list[Etiquette]]:
111:    def couverture(self) -> dict[str, float]:
116:    def json(self, avec_duree: bool = False) -> dict:
130:class BlocLinguistique(Protocol):
133:    def analyser(self, texte: str, langue: str | None = None,
137:class RefusNeuronal(RuntimeError):
144:def _normaliser(texte: str) -> str:
148:def _trigrammes(texte: str) -> list[str]:
153:def _profil(texte: str, top: int = 200) -> dict[str, int]:
158:def charger_profils_udhr(chemin: pathlib.Path, train=(0, 14), test=(15, 30),
192:def _score_profil(tri: collections.Counter, profil: dict[str, int]) -> float:
199:def detecter_langue(texte: str, profils: dict[str, dict] | None = None,
230:def _script_char(ch: str) -> str:
256:def detecter_script(texte: str) -> str:
302:        "PRON": set("je j tu il elle on nous vous ils elles me te se lui leur moi toi soi y en ce cela ça qui que quoi dont où".split()),
311:        "PRON": set("i you he she it we they me him her us them who whom which that".split()),
367:RELATIFS = {"qui", "que", "qu", "dont", "où", "which", "
… [6264 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 280, "limit": 220}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
280:               "i you he she it we they me him her us them my your his its our their".split()),
281:     "de": set("der die das den dem des ein eine einer eines und oder aber denn sondern nicht "
282:               "kein keine ist sind war waren sein haben hat hatte ich du er sie es wir ihr "
283:               "mit von zu aus bei nach über unter für durch".split()),
284:     "es": set("el la los las un una unos unas de del a al y o pero sino que quien como donde "
285:               "yo tú él ella nosotros vosotros ellos me te se le les mi tu su nuestro vuestro "
286:               "es son era eran ser haber he has ha han no nunca muy en con por para".split()),
287:     "it": set("il lo la i gli le un uno una di del della a al alla e o ma però che chi cui "
288:               "dove io tu lui lei noi voi loro mi ti si ci vi mio tuo suo nostro vostro è sono "
289:               "era erano essere avere ho hai ha hanno non mai molto in con per su tra fra".split()),
290:     "pt": set("o a os as um uma uns umas de do da dos das a ao aos à às e ou mas porém que quem "

… [15375 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading segmentation rules and union logic

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 250, "offset": 840}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
840:             if g["fin"] <= segment["debut"]:
841:                 return segment["debut"] - g["fin"]
842:             if g["debut"] >= segment["fin"]:
843:                 return g["debut"] - segment["fin"]
844:             return 0
845:         proches: list[str] = []
846:         for g in sorted(gvs, key=ecart)[:k]:
847:             v = Heuristique._verbe_gv(texte, g, verbes, cache)
848:             if v and v not in proches:
849:                 proches.append(v)
850:         return proches
851: 
852:     def _syntagmes_simple(self, texte: str, langue: str,
853:                           pos_verbes: set[int] | None = None) -> list[dict]:
854:         mots = self._mots(texte)
855:         lex = POS_FERME.get(langue, POS_FERME["fr"])
856:         pos_verbes = pos_verbes or set()
857:         par_debut = {m[0]: k for k, m in enumerate(mots)}
858: 
859:         def est_sub(n: str) -> bool:
860:             """Le mot est-il un subordonnant **dans cette langue** ? (« car » est un nom anglais)"""
861:             if n in SUB_PAR_LANGUE.get(langue, set()):
862:       
… [14810 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 160, "offset": 1089}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1089:         cache_gv: dict = {}  # un GV n'est analysé qu'une fois par analyse
1090:         # **un seul chunking par analyse**, partagé par les trois chemins (S, union, chunker) :
1091:         # le O(n²) mesuré venait des re-chunkings (A6, A11) — sortie identique (T178).
1092:         pos_verbes = {e.debut for e in etiquettes if e.niveau == "pos" and e.type == "VERB"}
1093:         simples = self._syntagmes_simple(texte, lg, pos_verbes)
1094:         gvs_simple = [x for x in simples if x["type"] == "GV"]
1095:         if cands:
1096:             for c in cands[:1]:
1097:                 noms = [x.get("nom", "") for x in cands]
1098:                 gvs_s = [x for x in c.get("segments", []) if x.get("type") == "GV"]
1099:                 deja = {(x["debut"], x["fin"]) for x in gvs_s}
1100:                 gvs = gvs_s + [x for x in gvs_simple if (x["debut"], x["fin"]) not in deja]
1101:                 for s in c.get("segments", []):
1102:                     # la cible de S **convertie en son verbe** : « Les enfants jouent » →
1103:                     # `jouent` (
… [10470 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 120, "offset": 522}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
522: class Heuristique:
523:     """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""
524: 
525:     nom = "heuristique"
526: 
527:     def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
528:                  seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
529:                  union: bool = True):
530:         self.profils = profils
531:         self.segmenter_s = segmenter_s
532:         self.seuil_ouvert = seuil_ouvert
533:         self.seuil_langue = seuil_langue
534:         self.union = union
535: 
536:     # -- langues / script ---------------------------------------------------
537:     def _langue(self, texte: str, indice: str | None) -> tuple[str, float, str]:
538:         langue, conf, _ = detecter_langue(texte, self.profils, indice)
539:         script = detecter_script(texte)
540:         if conf < self.seuil_langue:
541:             return "und", conf, script
542:         return langue, conf, script
543: 
544:     # -- tokens ---------------------------------------------
… [5039 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 70, "offset": 638}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
638:     def _syntagmes_s(self, texte: str) -> list[dict] | None:
639:         if not self.segmenter_s:
640:             return None
641:         try:
642:             if str(RACINE / "tools/structures") not in sys.path:
643:                 sys.path.insert(0, str(RACINE / "tools/structures"))
644:             import generateur  # le générateur S, importé en lecture seule
645:             return generateur.analyser(texte)
646:         except Exception:
647:             return None
648: 
649:     def _cibles_s(self, texte: str) -> dict:
650:         """Toutes les cibles du générateur S (pas seulement le dernier segment ambigu).
651: 
652:         Lecture seule de l'API interne du S : `_tokens`/`_segmente` rendent les `Segment` avec
653:         `cible_nom`/`cible_gp`/`cible_verbe`. Le défaut retenu est la cible la plus proche
654:         (GP, puis GN, puis GV), comme le premier candidat de `analyser`.
655:         """
656:         if not self.segmenter_s:
657:             return {}
658:         try:
659:             import generateur
660:             base = generateur
… [2829 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /tmp/audit_r1r3/ 2>/dev/null && echo EXISTS || echo 'no /tmp/audit_r1r3'; ls /tmp | head -30", "description": "Check for previous audit harness"}`

  ```
total 376
drwxr-xr-x.   4 stephane stephane    380  5 nov 22:17 .
drwxrwxrwt. 192 root     root      18240  5 nov 23:27 ..
-rw-r--r--.   1 stephane stephane  14442  5 nov 21:32 autotest.log
-rw-r--r--.   1 stephane stephane 115791  5 nov 22:17 bl_f908.py
-rw-r--r--.   1 stephane stephane 114128  5 nov 21:28 bl_parent.py
-rw-r--r--.   1 stephane stephane  24641  5 nov 22:08 build_json.py
-rw-r--r--.   1 stephane stephane   7177  5 nov 21:43 compile.json
-rw-r--r--.   1 stephane stephane   3217  5 nov 21:43 compile.py
-rw-r--r--.   1 stephane stephane   2884  5 nov 21:33 complements.json
-rw-r--r--.   1 stephane stephane   3791  5 nov 21:33 complements.py
-rw-r--r--.   1 stephane stephane   3761  5 nov 21:40 details.json
-rw-r--r--.   1 stephane stephane   1186  5 nov 21:40 details.py
-rw-r--r--.   1 stephane stephane   8598  5 nov 21:27 harness.log
-rw-r--r--.   1 stephane stephane  19742  5 nov 21:27 harness.py
drwxr-xr-x.   3 stephane stephane    280  5 nov 21:33 mods
drwxr-xr-x.   2 stephane stephane     60  5 nov 21:31 __pycache__
-rw-r--r--.   1 stephane stephane  33271  5 nov 21:27 resultats.json
-rw-r--r--.   1 stephane stephane   2444  5 nov 21:35 verifs.json
-rw-r--r--.   1
… [571 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-audit-r1r3.json'))\nprint(list(d.keys()))\nprint(json.dumps({k:d[k] for k in d if k not in ('rejeu','ablations')}, ensure_ascii=False, indent=1)[:5000])\nEOF", "description": "Inspect audit JSON structure", "workdir": "/ho … [46 caractères tronqués]`

  ```
['rapport', 'ligne', 'branche', 'commit_audite', 'commit_parent', 'date', 'objet', 'methode', 'verdict', 'rejeu', 'ablations', 'decomposition', 'spans_27', 'controle_negatif', 'dev_test', 'portes_autotest', 'ecarts', 'limites', 'fichiers_ecrits', 'commit']
{
 "rapport": "audit-r1r3",
 "ligne": "B13",
 "branche": "s/v7",
 "commit_audite": "f908d7b0613c8a5eb8fae7fab514bfdc5fa4668b",
 "commit_parent": "69bd865ec1bae1958b6f617bde4bf685a15d7d67",
 "date": "2026-11-05",
 "objet": "Audit du round R1/R2/R3 : rejeu des valeurs, ablations par règle, contrôles négatifs, dev/test, portes.",
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
  "fidelit
… [4056 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reusing the prior harness code as a basis

- **read** `{"file_path": "/tmp/audit_r1r3/harness.py"}`

  ```
<path>/tmp/audit_r1r3/harness.py</path>
<type>file</type>
<content>
1: """Harnais d'audit R1/R2/R3 — mesures sur le gold vivant 612 et gelé 602.
2: 
3: Aucun fichier du dépôt n'est modifié : les variantes du bloc sont copiées dans /tmp et
4: importées comme modules distincts ; le module officiel n'est jamais patché sur disque.
5: """
6: from __future__ import annotations
7: 
8: import collections
9: import importlib.util
10: import json
11: import pathlib
12: import random
13: import statistics
14: import sys
15: 
16: RACINE = pathlib.Path("/home/stephane/Data13TB/stephane/GitHub/Qtrinet")
17: sys.path.insert(0, str(RACINE))
18: sys.path.insert(0, str(RACINE / "tools"))
19: 
20: import tools.tests.linguistique.evaluer_gold as eg  # noqa: E402
21: from tools.tests.linguistique.gold_split import dev as split_dev, test as split_test  # noqa: E402
22: 
23: SOURCE = (RACINE / "tools/bloc_linguistique.py").read_text(encoding="utf-8")
24: 
25: # ---- remplacements exacts des règles de f908d7b0 -------------------------
26: R1A_OLD = '''SUJETS = {"i", "you", "he", "she", "it", "we", "they", "who", "that", "which", "there",
27:           "je", "tu", "il", "elle", "on", "nous", "vous", "ils"
… [20565 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking the v10 diff and module identity

- **bash** `{"command": "git diff 160d08ca 710ec7f9 -- tools/bloc_linguistique.py tools/pensee/autotest.py tools/tests/linguistique/ | head -250; echo '---'; git status --short tools/bloc_linguistique.py tools/pensee/autotest.py tools/tests/linguistique/", "description": "Inspect v10 commit diff", "workdir": "/ … [48 caractères tronqués]`

  ```
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 074aa790..329298c4 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -980,7 +980,8 @@ class Heuristique:
                 # le GP s'arrête au verbe ou au relatif : « de la voisine | dort » et non
                 # « de la voisine dort » (mesuré : 25 spans « plus large » sur le gold).
                 while (j < len(mots) and mots[j][3] == "mot"
-                       and not est_verbe(mots[j][0], mots[j][2])
+                       and not (est_verbe(mots[j][0], mots[j][2])
+                                and not (j > i + 1 and _normaliser(mots[j - 1][2]) in lex.get("DET", set())))
                        and _normaliser(mots[j][2]) not in RELATIFS):
                     j += 1
                 # « à manger » : un GP réduit à sa préposition prend le verbe qui suit
diff --git a/tools/pensee/autotest.py b/tools/pensee/autotest.py
index 94cc7d6c..94b9f354 100644
--- a/tools/pensee/autotest.py
+++ b/tools/pensee/autotest.py
@@ -1668,7 +1668,7 @@ def t109_anaphore_103() -> tuple[bool, str]:
 
 
 def t110_segmenteur() -> tuple[bool, str]:
-    """Le segmenteur : S F1 0,5006 (français s
… [9753 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport hashlib, subprocess, pathlib\np = pathlib.Path('tools/bloc_linguistique.py')\ncur = p.read_bytes()\ncom = subprocess.run(['git','show','710ec7f9:tools/bloc_linguistique.py'],capture_output=True).stdout\nprint('current == commit710ec7f9:', cur==com)\nprint('sha  … [251 caractères tronqués]`

  ```
current == commit710ec7f9: True
sha current 308f6eeda95f69ea 116798
sha commit  308f6eeda95f69ea 116798
  ```

### 🤖 Assistant

⏵ Verifying which correction belongs to which commit

- **bash** `{"command": "git show --stat --oneline 710ec7f9; echo '--- parent -ée? ---'; git show 160d08ca:tools/bloc_linguistique.py | grep -n 'ées\\|ée\\|participes' | head; echo '--- 710ec7f9 -ée ---'; grep -n 'ées\\|ée\\|participes' tools/bloc_linguistique.py | head; echo '--- diff journal for v10 ---'; git … [150 caractères tronqués]`

  ```
710ec7f9 B13 — LE FÉMININ -ÉE ET LA GARDE DÉTERMINANT DU GP : EXACT 220/220 (1,0000), COUVERTURE 0,9205, F1 0,5880, 19 SPANS ; 183/183
 docs/pilotage/en-cours.md                          |   4 +-
 journal/2026-11-05/README.md                       |   7 +-
 journal/2026-11-05/attention.md                    |   2 +-
 journal/2026-11-05/distribue.md                    |   9 +-
 journal/2026-11-05/docs.md                         |   2 +-
 journal/2026-11-05/memoire.md                      |   2 +-
 journal/2026-11-05/mesures.md                      |   2 +-
 journal/2026-11-05/modele.md                       |   2 +-
 journal/2026-11-05/moteur.md                       |   2 +-
 journal/2026-11-05/portes.md                       |   2 +-
 journal/README.md                                  |   2 +-
 journal/THEMES.md                                  |   2 +-
 journal/sessions/MANIFEST.md                       |   2 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 113 +++++++++++++++++++++
 .../rapport.md                                     |  19 ++--
 reports/README.md                                  |   2 +-
 reports/pensee-v10.json                            |  41 ++++++++
 
… [3325 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -S'n[:-len(suf)] + \"er\"' -- tools/bloc_linguistique.py; echo '---'; git log --oneline -S'Une garde' -- tools/bloc_linguistique.py | head -3", "description": "Trace introduction of -ée rule", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
a408a909 B13 — LE LEXIQUE ÉLARGI (PARTICIPES IRRÉGULIERS ET EN -É) : EXACT 0,8082 → 0,8483 ; 174/174
---
  ```

### 🤖 Assistant

⏵ Isolating each rule's exact source delta

- **bash** `{"command": "git diff d497324b 160d08ca -- tools/bloc_linguistique.py", "description": "Diff v8 to v9 module", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 8daa099c..074aa790 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -369,8 +369,8 @@ RELATIFS = {"qui", "que", "qu", "dont", "où", "which", "that", "who", "whom", "
 # les subordonnants qui n'ont pas d'antécédent : toujours SUB
 AMBIGUES_PREP = {"since", "before", "after", "until", "as", "depuis", "avant", "après", "pendant", "durant"}
 
-SUJETS = {"i", "you", "he", "she", "it", "we", "they", "there",
-          "je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles"}
+SUJETS = {"i", "you", "he", "she", "it", "we", "they", "there", "who", "that", "which",
+          "je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles", "qui", "qu"}
 
 SUBORDONNANTS = {"because", "although", "though", "if", "while", "as", "since", "unless",
                  "whether", "car", "parce", "puisque", "comme", "quand", "si", "lorsque"}
@@ -856,11 +856,20 @@ class Heuristique:
         pos_verbes = pos_verbes or set()
         par_debut = {m[0]: k for k, m in enumerate(mots)}
 
+        def est_sub(n: str) -> bool:
+            """Le mot est-il un subordonnant **dans cette langue** ? (« ca
… [2577 caractères tronqués]
  ```

- **bash** `{"command": "git show a408a909 --stat --oneline | head -20; echo '--- -ée diff ---'; git show a408a909 -- tools/bloc_linguistique.py | head -80; echo '--- acheter in lexicon? ---'; grep -c 'acheter' tools/bloc_linguistique.py; grep -n 'achet' tools/bloc_linguistique.py data/* 2>/dev/null | head", "d … [110 caractères tronqués]`

  ```
a408a909 B13 — LE LEXIQUE ÉLARGI (PARTICIPES IRRÉGULIERS ET EN -É) : EXACT 0,8082 → 0,8483 ; 174/174
 docs/implantation/moteur-de-pensee.md              |  7 +-
 docs/pilotage/chantiers.md                         |  8 +-
 docs/pilotage/en-cours.md                          | 14 ++--
 docs/pilotage/roadmap.md                           |  6 +-
 journal/2026-11-05/README.md                       |  7 +-
 journal/2026-11-05/attention.md                    |  2 +-
 journal/2026-11-05/distribue.md                    |  2 +-
 journal/2026-11-05/docs.md                         |  5 +-
 journal/2026-11-05/memoire.md                      |  2 +-
 journal/2026-11-05/mesures.md                      |  2 +-
 journal/2026-11-05/modele.md                       |  2 +-
 journal/2026-11-05/moteur.md                       |  2 +-
 journal/2026-11-05/portes.md                       |  2 +-
 journal/README.md                                  |  6 +-
 .../0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md | 89 ++++++++++++++++++++++
 .../rapport.md                                     | 51 ++++++++++++-
 journal/sessions/MANIFEST.md                       |  4 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/dige
… [10862 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Building the v10 audit harness in /tmp

- **bash** `{"command": "mkdir -p /tmp/audit_v10/mods && cat > /tmp/audit_v10/mesure.py <<'PY'\nfrom __future__ import annotations\nimport collections, json, pathlib, sys, statistics, random, importlib.util\nRACINE = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nsys.path.insert(0, str(RACINE) … [2272 caractères tronqués]`

  ```
vivant 612 gele 602
dev 422 test 190
--- vivant 612
labels 220 exact 220 exact_span 1.0 couverture 0.9205
topk 219 0.9163 topk_span 0.9955
fr {'cibles': 151, 'labels': 134, 'exact': 134, 'topk': 133, 'exact_taux_span': 1.0} en {'cibles': 88, 'labels': 86, 'exact': 86, 'topk': 86, 'exact_taux_span': 1.0}
syntagme f1 0.5836 tete 0.7332
spans perdus 239
--- gele 602
labels 220 exact 220 exact_span 1.0 couverture 0.9205
topk 219 0.9163 topk_span 0.9955
fr {'cibles': 151, 'labels': 134, 'exact': 134, 'topk': 133, 'exact_taux_span': 1.0} en {'cibles': 88, 'labels': 86, 'exact': 86, 'topk': 86, 'exact_taux_span': 1.0}
syntagme f1 0.588 tete 0.7388
spans perdus 239
--- dev
labels 152 exact 152 exact_span 1.0 couverture 0.9325
topk 152 0.9325 topk_span 1.0
fr {'cibles': 101, 'labels': 91, 'exact': 91, 'topk': 91, 'exact_taux_span': 1.0} en {'cibles': 62, 'labels': 61, 'exact': 61, 'topk': 61, 'exact_taux_span': 1.0}
syntagme f1 0.5812 tete 0.733
spans perdus 239
--- test
labels 68 exact 68 exact_span 1.0 couverture 0.8947
topk 67 0.8816 topk_span 0.9853
fr {'cibles': 50, 'labels': 43, 'exact': 43, 'topk': 42, 'exact_taux_span': 1.0} en {'cibles': 26, 'labels': 25, 'exact': 25, 'topk': 25, '
… [2705 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Testing the -ée rule's actual reach

- **bash** `{"command": "python3 - <<'PY'\nimport sys; sys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfor w in ['achetée','acheté','aimée','entrée','portée','idée','année','journée','pensée','soirée','matinée','montée','visitée']:\n    print(w, bl._est_verbe(w), '| sans -ée hypothesis:', (w[:-2]+ … [404 caractères tronqués]`

  ```
achetée False | sans -ée hypothesis: False
acheté False | sans -ée hypothesis: -
aimée True | sans -ée hypothesis: True
entrée True | sans -ée hypothesis: True
portée True | sans -ée hypothesis: True
idée False | sans -ée hypothesis: False
année False | sans -ée hypothesis: False
journée False | sans -ée hypothesis: False
pensée False | sans -ée hypothesis: False
soirée False | sans -ée hypothesis: False
matinée False | sans -ée hypothesis: False
montée True | sans -ée hypothesis: True
visitée False | sans -ée hypothesis: False
acheter in VERBES_CONNUS: False
aimer: True entrer: True porter: True monter: True
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nph = eg.charger()\nfor p in ph:\n    if p['id'] in ('r303','s037','r153','r255','r264'):\n        print(p['id'], p['langue'], p.get('source'), repr(p['texte']))\n        for s … [257 caractères tronqués]`

  ```
r153 en reel 'We wait for the bus.'
    GN 0 2 'We' None
    GV 3 7 'wait' None
    GP 8 19 'for the bus' wait
r255 fr reel "La voiture que j'ai achetée roule."
    GN 0 10 'La voiture' None
    REL 11 27 "que j'ai achetée" voiture
    GV 28 33 'roule' None
r264 fr reel "Je sais qu'il vient demain."
    GN 0 2 'Je' None
    GV 3 7 'sais' None
    SUB 8 26 "qu'il vient demain" sais
r303 fr reel 'Je pars car il est tard.'
    GN 0 2 'Je' None
    GV 3 7 'pars' None
    SUB 8 23 'car il est tard' pars
s037 fr synthetique 'Paul qui marche marche'
    GN 0 4 'Paul' None
    REL 5 15 'qui marche' Paul
    GV 16 22 'marche' None
  ```

### 🤖 Assistant

⏵ Checking autotest entrypoint and measuring cost

- **bash** `{"command": "tail -80 tools/pensee/autotest.py; echo '---'; head -40 tools/pensee/autotest.py; echo '--- head of test list'; grep -n \"def t0\\|def t1\\|PORTES\\|__main__\" tools/pensee/autotest.py | tail -20", "description": "Inspect autotest runner", "workdir": "/home/stephane/Data13TB/stephane/Gi … [14 caractères tronqués]`

  ```
("T111 hybride segmenteur", t111_hybride_seg()),
              ("T112 union segmenteurs", t112_union()),
              ("T113 union par défaut", t113_union_defaut()),
              ("T114 cascade + union", t114_cascade_union()),
              ("T115 tête cascade", t115_tete_cascade()),
              ("T116 miroir", t116_miroir()),
              ("T117 sortie POS", t117_miroir_pos()),
              ("T118 restitution spans", t118_miroir_espaces()),
              ("T119 restitution sémantique", t119_miroir_resume()),
              ("T120 réponse", t120_miroir_reponse()),
              ("T121 réponse contenu", t121_reponse_contenu()),
              ("T122 extraction", t122_extraction()),
              ("T123 juge", t123_juge()),
              ("T124 réponses", t124_reponses()),
              ("T125 juge contre le bloc", t125_juge_bloc()),
              ("T126 réponse dirigée", t126_dirigee()),
              ("T127 négatives", t127_negatives()),
              ("T128 règle du si", t128_si()),
              ("T129 pièges", t129_pieges()),
              ("T130 gold gelé", t130_gold_gele()),
              ("T131 contexte", t131_contextuel()),
              ("T132 lien auto", t132_lien_auto
… [6741 caractères tronqués]
  ```

- **bash** `{"command": "time python3 - <<'PY'\nimport sys; sys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nimport tools.bloc_linguistique as bl\nph = eg.charger(); h=bl.Heuristique()\nfor p in ph[:50]:\n    h.analyser(p['texte'],p['langue'])\nprint('50 ok')\nPY", "description": "Ben … [82 caractères tronqués]`

  ```
50 ok
[stderr]

real	0m0,187s
user	0m0,168s
sys	0m0,019s
  ```

### 🤖 Assistant

⏵ Running the 183 gates in the background

- **bash** `{"command": "PYTHONPATH=. python3 -m tools.pensee.autotest > /tmp/audit_v10/autotest.log 2>&1; echo \"exit=$?\"", "description": "Run autotest gates", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet", "run_in_background": true}`

  ```
started background job bash-2416
  ```

- **bash** `{"command": "sed -n '260,380p' /tmp/audit_r1r3/harness.py >/dev/null; python3 - <<'PY'\nimport sys; sys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nph=eg.charger(); ge=eg.charger_gele()\n# check ids overlap and split semantics\nfrom tools.tests.linguistique.gold_split imp … [840 caractères tronqués]`

  ```
ids vivant uniques 612 gele uniques 602
gele subset ids True
test ids ['g002', 'g007', 'g013', 'g018', 'g020']
r303 split dev
s037 split dev
r153 split test
r255 split test
r264 split test
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_split.py"}`

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

- **bash** `{"command": "sed -n '1,60p' tools/tests/linguistique/gold_gele.json | head -5; python3 - <<'PY'\nimport json\nfor f in ['tools/tests/linguistique/gold.json','tools/tests/linguistique/gold_reel.json','tools/tests/linguistique/gold_synthetique.json','tools/tests/linguistique/gold_gele.json']:\n    d=j … [171 caractères tronqués]`

  ```
{
"gele": "2026-11-02",
"phrases": [
{
"id": "g001",
tools/tests/linguistique/gold.json 20
tools/tests/linguistique/gold_reel.json 432
tools/tests/linguistique/gold_synthetique.json 160
tools/tests/linguistique/gold_gele.json 602
  ```

- **bash** `{"command": "sed -n '1,60p' tools/bloc_linguistique.py", "description": "Check module RACINE definition", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

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
… [1316 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Writing the full measurement harness

- **bash** `{"command": "cat > /tmp/audit_v10/harness.py <<'PY'\n\"\"\"Harnais d'audit v10 — rejeu, ablations, contrôles négatifs, dev/test.\n\nAucun fichier du dépôt n'est modifié : chaque variante est une copie du module dans /tmp,\nimportée comme module distinct. Le module officiel n'est jamais patché.\n\"\" … [15964 caractères tronqués]`

  ```
exit=1
v10 labels 220 exact 220 f1g 0.7007 spans 19 0.7s
v9 labels 219 exact 219 f1g 0.6985 spans 20 0.7s
v8 labels 212 exact 212 f1g 0.6884 spans 27 0.8s
sans_pron labels 203 exact 203 f1g 0.6846 spans 36 0.8s
sans_est_sub labels 219 exact 219 f1g 0.6995 spans 20 0.9s
sans_predicat_vu labels 220 exact 220 f1g 0.7007 spans 19 0.8s
sans_ee labels 220 exact 220 f1g 0.7007 spans 19 0.9s
sans_gp_det labels 219 exact 219 f1g 0.6985 spans 20 0.7s
v9_attendu labels 219 exact 219 f1g 0.6985 spans 20 0.9s
Traceback (most recent call last):
  File "/tmp/audit_v10/harness.py", line 286, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/tmp/audit_v10/harness.py", line 260, in main
    dd=diff_sets(base,m,par_id)
  File "/tmp/audit_v10/harness.py", line 156, in diff_sets
    g=base['exact_set']-autre['exact_set']; p=autre['exact_set']-base['exact_set']
      ~~~~^^^^^^^^^^^^^
KeyError: 'exact_set'
[stderr]

real	0m10,637s
user	0m10,495s
sys	0m0,142s
  ```

### 🤖 Assistant

⏵ Fixing per-phrase F1 and set keys

- **bash** `{"command": "python3 - <<'PY'\np='/tmp/audit_v10/harness.py'\ns=open(p).read()\ns=s.replace('''def mesure_segmentation(ann, phrases):\n    pred=set(); pred_t=set(); gold=set(); gold_t=set()\n    for p in phrases:\n        a=ann[p['id']]\n        pred |= {(e.type,e.debut,e.fin) for e in a.etiquettes  … [1803 caractères tronqués]`

  ```
patched
exit=0
      "labels": 40,
      "exact": 40,
      "topk": 38
     },
     "en": {
      "cibles": 26,
      "labels": 24,
      "exact": 24,
      "topk": 19
     }
    }
   }
  }
 }
}
[stderr]

real	0m10,647s
user	0m10,498s
sys	0m0,148s
  ```

### 🤖 Assistant

⏵ Inspecting harness results

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/audit_v10/resultats.json'))\nprint(json.dumps(d['gold'],indent=1))\nfor nom in ('v10','v9','v8'):\n    v=d['variantes'][nom]\n    print('\\n===',nom)\n    for k in ('labels','exact','exact_any','couverture','topk','topk_taux','topk_e … [661 caractères tronqués]`

  ```
{
 "vivant": 612,
 "gele": 602,
 "dev": 422,
 "test": 190
}

=== v10
  labels 220
  exact 220
  exact_any 220
  couverture 0.9205
  topk 219
  topk_taux 0.9163
  topk_exact 219
  topk_taux_span 0.9955
  f1_vivant 0.5836
  tete_vivant 0.7332
  f1_gele 0.588
  tete_gele 0.7388
  spans {'GP': 4, 'REL': 9, 'SUB': 6}
  spans_total 19
  f1_s_vivant 0.4957
  f1_chunker_vivant 0.6163
  f1_s_gele 0.5014
  f1_chunker_gele 0.6203
  tete_s_gele 0.6677
  tete_chunker_gele 0.7639
  fr {'cibles': 151, 'labels': 134, 'exact': 134, 'topk': 133}
  en {'cibles': 88, 'labels': 86, 'exact': 86, 'topk': 86}
  dev {'cibles': 163, 'labels': 152, 'exact': 152, 'couverture': 0.9325, 'f1': 0.5812, 'tete': 0.733, 'par_langue': {'fr': {'cibles': 101, 'labels': 91, 'exact': 91, 'topk': 91}, 'en': {'cibles': 62, 'labels': 61, 'exact': 61, 'topk': 61}}}
  test {'cibles': 76, 'labels': 68, 'exact': 68, 'couverture': 0.8947, 'f1': 0.589, 'tete': 0.7337, 'par_langue': {'fr': {'cibles': 50, 'labels': 43, 'exact': 43, 'topk': 42}, 'en': {'cibles': 26, 'labels': 25, 'exact': 25, 'topk': 25}}}

=== v9
  labels 219
  exact 219
  exact_any 219
  couverture 0.9163
  topk 218
  topk_taux 0.9121
  topk_exact 218
  topk_taux_
… [5283 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Comparing negative-control protocols with the prior audit

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-r1r3.json'))\nprint(json.dumps(d['controle_negatif'],ensure_ascii=False,indent=1)[:6000])\nPY", "description": "Read prior negative control JSON", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
{
 "permutation_globale": {
  "n": 212,
  "observe": 212,
  "tirages": 2000,
  "graine": 0,
  "moyenne": 2.0425,
  "mediane": 2.0,
  "max": 9,
  "p95": 5,
  "p": 0.0,
  "lecture": "0,96 % en moyenne contre 100 % observe"
 },
 "candidat_aleatoire": {
  "n": 212,
  "avec_candidats": 212,
  "candidats": 516,
  "top1_moyen": 76.1,
  "top1_taux": 0.359,
  "observe_top1": 212,
  "p_top1": 0.0,
  "lecture": "35,9 % en moyenne contre 100 % observe"
 },
 "permutation_candidats_topk": {
  "n": 212,
  "moyenne": 1.81,
  "taux": 0.0085,
  "max": 7,
  "observe": 177,
  "p": 0.0,
  "lecture": "0,85 % en moyenne contre 83,49 % observe"
 },
 "hasard_officiel": {
  "n": 239,
  "observe": 1,
  "taux": 0.0042,
  "top1_observe": 212,
  "top1_taux": 0.887
 },
 "spans_27_verifies": true,
 "absent_de_la_fiche": true,
 "verdict": "L'attachement n'est pas un artefact du hasard ; mais la fiche et le JSON ne publient aucun controle negatif."
}
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/audit_v10/resultats.json'))\nfor nom in ('sans_pron','sans_est_sub','sans_predicat_vu','sans_ee','sans_gp_det','v9','v8','v9_attendu'):\n    a=d['ablations'][nom]\n    print('\\n===',nom)\n    for k in ('labels','exact','delta_labels … [459 caractères tronqués]`

  ```
=== sans_pron
  labels 203
  exact 203
  delta_labels -17
  delta_exact -17
  couverture 0.8494
  n_gains 17
  n_pertes 0
  n_labels_gagnes 17
  n_labels_perdus 0
  f1_gele 0.5718
  delta_f1_gele -0.0162
  f1_vivant 0.5676
  delta_f1_vivant -0.016
  tete_gele 0.7288
  topk 202
  spans_total 36
  spans {'GP': 4, 'REL': 18, 'SUB': 14}
  gains {'dev': ['g017:SUB', 'r034:REL', 'r074:REL', 'r114:REL', 'r205:SUB', 'r219:SUB', 'r240:SUB', 'r243:REL', 'r247:SUB', 'r278:REL', 'r280:REL', 'r285:REL', 'r296:SUB', 'r299:REL'], 'test': ['r214:REL', 'r216:SUB', 'r281:SUB']}
  pertes {}
  dev {'cibles': 163, 'labels': 138, 'exact': 138, 'couverture': 0.8466, 'f1': 0.5621, 'tete': 0.7215, 'par_langue': {'fr': {'cibles': 101, 'labels': 91, 'exact': 91, 'topk': 91}, 'en': {'cibles': 62, 'labels': 47, 'exact': 47, 'topk': 47}}}
  test {'cibles': 76, 'labels': 65, 'exact': 65, 'couverture': 0.8553, 'f1': 0.5799, 'tete': 0.7278, 'par_langue': {'fr': {'cibles': 50, 'labels': 43, 'exact': 43, 'topk': 42}, 'en': {'cibles': 26, 'labels': 22, 'exact': 22, 'topk': 22}}}

=== sans_est_sub
  labels 219
  exact 219
  delta_labels -1
  delta_exact -1
  couverture 0.9163
  n_gains 1
  n_pertes 0
  n_labels_gagnes
… [5930 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-2416 (bash: PYTHONPATH=. python3 -m tools.pensee.autotest > /tmp/audit_v10/autotest.log 2>&1; echo "exit=$?") finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Checking gate results and prior top-k control code

- **bash** `{"command": "grep -n \"permutation\\|topk\\|candidat\" /tmp/audit_r1r3/*.py | head -40; echo '---'; tail -12 /tmp/audit_v10/autotest.log; echo '--- gate count ---'; grep -c '✅' /tmp/audit_v10/autotest.log; grep -c '❌' /tmp/audit_v10/autotest.log; grep 'portes tenues' /tmp/audit_v10/autotest.log", "d … [112 caractères tronqués]`

  ```
/tmp/audit_r1r3/bl_f908.py:7:    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
/tmp/audit_r1r3/bl_f908.py:19:`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script` et ses `candidats`.
/tmp/audit_r1r3/bl_f908.py:76:    candidats: list[str] = field(default_factory=list)
/tmp/audit_r1r3/bl_f908.py:86:            "candidats": list(self.candidats), "langue": self.langue,
/tmp/audit_r1r3/bl_f908.py:654:        (GP, puis GN, puis GV), comme le premier candidat de `analyser`.
/tmp/audit_r1r3/bl_f908.py:680:    def _candidats_precedent(texte: str, segment: dict, precedent: dict | None) -> list[str]:
/tmp/audit_r1r3/bl_f908.py:681:        """Les candidats que le **précédent** impose : l'antécédent d'une REL, le verbe d'une SUB."""
/tmp/audit_r1r3/bl_f908.py:739:        """La tête d'un texte de candidat : le verbe plein s'il y en a un, sinon le dernier mot.
/tmp/audit_r1r3/bl_f908.py:829:        """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
/tmp/audit_r1r3/bl_f908.py:923:                                     "texte": texte[d:mots[j - 1][1]], "candidats": []})
/tmp/audit_r1r3/bl_f908.py:944:                    
… [4313 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/audit_v10/resultats.json'))\nfor nom in ('v8','v9','v10'):\n    v=d['variantes'][nom]\n    print('\\n===',nom,'spans',v['spans_total'],v['spans'])\n    print(' ids:',[x['id']+':'+x['type'] for x in v['spans_liste']])\nPY", "descripti … [97 caractères tronqués]`

  ```
=== v8 spans 27 {'GP': 5, 'REL': 16, 'SUB': 6}
 ids: ['r153:GP', 's160:GP', 's027:GP', 's146:GP', 's148:GP', 's037:REL', 's141:REL', 's065:REL', 's010:REL', 's061:REL', 's032:REL', 's035:REL', 'r280:REL', 's125:REL', 's135:REL', 'r273:REL', 's069:REL', 'r035:REL', 'r255:REL', 's115:REL', 's072:REL', 'r264:SUB', 'g017:SUB', 'r288:SUB', 's044:SUB', 's112:SUB', 's114:SUB']

=== v9 spans 20 {'GP': 5, 'REL': 9, 'SUB': 6}
 ids: ['r153:GP', 's160:GP', 's027:GP', 's146:GP', 's148:GP', 's037:REL', 's141:REL', 's065:REL', 's010:REL', 's061:REL', 's035:REL', 's125:REL', 'r035:REL', 'r255:REL', 'r303:SUB', 'r264:SUB', 'r288:SUB', 's044:SUB', 's112:SUB', 's114:SUB']

=== v10 spans 19 {'GP': 4, 'REL': 9, 'SUB': 6}
 ids: ['s160:GP', 's027:GP', 's146:GP', 's148:GP', 's037:REL', 's141:REL', 's065:REL', 's010:REL', 's061:REL', 's035:REL', 's125:REL', 'r035:REL', 'r255:REL', 'r303:SUB', 'r264:SUB', 'r288:SUB', 's044:SUB', 's112:SUB', 's114:SUB']
  ```

- **bash** `{"command": "grep -n \"permutation_candidats\\|permut\\|candidats_topk\\|topk\" /tmp/audit_r1r3/build_json.py /tmp/audit_r1r3/compile.py /tmp/audit_r1r3/verifs.py /tmp/audit_r1r3/details.py /tmp/audit_r1r3/complements.py 2>/dev/null | head -30", "description": "Find prior top-k permutation code"}`

  ```
/tmp/audit_r1r3/build_json.py:46:                  "topk": 177, "topk_taux": 0.7406, "topk_exact": 177,
/tmp/audit_r1r3/build_json.py:52:                "topk": 177, "topk_taux": 0.7406, "topk_exact": 177,
/tmp/audit_r1r3/build_json.py:61:                  "topk": 166, "topk_taux": 0.6946,
/tmp/audit_r1r3/build_json.py:65:                "topk": 166, "topk_taux": 0.6946,
/tmp/audit_r1r3/build_json.py:177:  "permutation_globale": {"n": 212, "observe": 212, "tirages": 2000, "graine": 0,
/tmp/audit_r1r3/build_json.py:183:  "permutation_candidats_topk": {"n": 212, "moyenne": 1.81, "taux": 0.0085, "max": 7,
/tmp/audit_r1r3/build_json.py:201:   "dev": {"phrases": 422, "cibles": 163, "labels": 148, "exact": 148, "couverture": 0.908, "f1": 0.5723, "tete": 0.727, "topk": 120},
/tmp/audit_r1r3/build_json.py:202:   "test": {"phrases": 190, "cibles": 76, "labels": 64, "exact": 64, "couverture": 0.8421, "f1": 0.5714, "tete": 0.7241, "topk": 57},
/tmp/audit_r1r3/build_json.py:203:   "tout": {"phrases": 612, "cibles": 239, "labels": 212, "exact": 212, "couverture": 0.887, "f1": 0.572, "tete": 0.7262, "topk": 177}
/tmp/audit_r1r3/build_json.py:255:  {"id": "controle_negatif_absent", "gravite": "mo
… [878 caractères tronqués]
  ```

- **read** `{"file_path": "/tmp/audit_r1r3/complements.py", "offset": 50, "limit": 35}`

  ```
<path>/tmp/audit_r1r3/complements.py</path>
<type>file</type>
<content>
50: b = att(base, phrases)
51: par_id = {p["id"]: {"split": "test" if p in H.split_test(phrases) else "dev"} for p in phrases}
52: res["r3a_fidele"] = {"labels": a["labels"], "exact": a["exact"], "couverture": a["couverture"],
53:                      "gains_ids": H.ids_courts(b["exact_set"] - a["exact_set"]),
54:                      "pertes_ids": H.ids_courts(a["exact_set"] - b["exact_set"]),
55:                      "labels_gagnes": H.ids_courts(b["label_set"] - a["label_set"]),
56:                      "labels_perdus": H.ids_courts(a["label_set"] - b["label_set"])}
57: # détail r280 avant/après
58: for nom, mod in (("baseline", base), ("r3a_fidele", m)):
59:     aa = att(mod, phrases)
60:     res[f"r280_{nom}"] = aa["details"].get(("r280","REL",8,21), {})
61: # contrôle top-k par permutation des listes de candidats
62: a0 = att(base, phrases)
63: cles = sorted(a0["label_set"], key=lambda x: (x[0],x[1],x[2],x[3]))
64: cands = [a0["details"][k]["candidats"] for k in cles]
65: cibles = [a0["details"][k]["cible_gold"] for k in cles]
66: rng = random.Random(0); vals = []
67: for _ in range(2000):
68:     perm = 
… [580 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Cross-checking official F1 bases for v9

- **bash** `{"command": "python3 - <<'PY'\nimport sys, importlib.util, pathlib\nsys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nph=eg.charger(); ge=eg.charger_gele()\nspec=importlib.util.spec_from_file_location('bl_v9','/tmp/audit_v10/mods/v9.py')\nm=importlib.util.module_from_spec(s … [666 caractères tronqués]`

  ```
vivant f1 0.5822 tete 0.7326 labels 219 exact 219
gele f1 0.5866 tete 0.7381 labels 219 exact 219
v10 vivant f1 0.5836 tete 0.7332
v10 gele f1 0.588 tete 0.7388
  ```

### 🤖 Assistant

⏵ Checking all -é(e) forms in the gold

- **bash** `{"command": "python3 - <<'PY'\nimport json,sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfor f in ['tools/tests/linguistique/gold.json','tools/tests/linguistique/gold_reel.json','tools/tests/linguistique/gold_synthetique.json']:\n    ph=json.load(open(f))['phrases']\n    for p i … [383 caractères tronqués]`

  ```
r016 'fatiguée' False
r052 'musée' False
r099 'musée' False
r228 'achetée' False
r234 'restés' True
r255 'achetée' False
r431 'arrivés' True
  ```

### 🤖 Assistant

⏵ Diagnosing the r303 regression

- **bash** `{"command": "python3 - <<'PY'\nimport sys, importlib.util, pathlib\nsys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nph={p['id']:p for p in eg.charger()}\np=ph['r303']; print(repr(p['texte']))\nfor nom in ('v8','v9','v10'):\n    spec=importlib.util.spec_from_file_location( … [527 caractères tronqués]`

  ```
'Je pars car il est tard.'

 v8
  GV 0 7 'Je pars' None
  GV 3 7 'pars' None
  SUB 8 23 'car il est tard' {'segment': 'car il est tard', 'cible': 'pars'}
  GV 12 18 'il est' {'segment': 'il est', 'cible': 'pars'}
  GP 19 23 'tard' {'segment': 'tard', 'cible': 'pars'}

 v9
  GV 0 7 'Je pars' None
  GV 3 7 'pars' None
  SUB 8 18 'car il est' {'segment': 'car il est', 'cible': 'pars'}
  GV 12 18 'il est' {'segment': 'il est', 'cible': 'pars'}
  GP 19 23 'tard' {'segment': 'tard', 'cible': 'pars'}

 v10
  GV 0 7 'Je pars' None
  GV 3 7 'pars' None
  SUB 8 18 'car il est' {'segment': 'car il est', 'cible': 'pars'}
  GV 12 18 'il est' {'segment': 'il est', 'cible': 'pars'}
  GP 19 23 'tard' {'segment': 'tard', 'cible': 'pars'}
  ```

### 🤖 Assistant

⏵ Verifying v9's S/chunker and testing the R1a bundle

- **bash** `{"command": "cat >> /tmp/audit_v10/check_v9_modes.py <<'PY'\nimport sys, importlib.util, pathlib, json\nsys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nph=eg.charger(); ge=eg.charger_gele()\ndef seg(mod, phrases, mode):\n    h=mod.Heuristique()\n    if mode=='s': h.union= … [1312 caractères tronqués]`

  ```
v9 vivant {'union': (0.5822, 0.7326), 's': (0.495, 0.6602), 'chunker': (0.6138, 0.7585)}
v9 gele {'union': (0.5866, 0.7381), 's': (0.5006, 0.6675), 'chunker': (0.6178, 0.7632)}
v10 vivant {'union': (0.5836, 0.7332), 's': (0.4957, 0.6604), 'chunker': (0.6163, 0.7592)}
v10 gele {'union': (0.588, 0.7388), 's': (0.5014, 0.6677), 'chunker': (0.6203, 0.7639)}
  ```

### 🤖 Assistant

⏵ Confirming -ée's introduction point precisely

- **bash** `{"command": "for c in f908d7b0 69bd865e 160d08ca a408a909; do echo -n \"$c: \"; git show $c:tools/bloc_linguistique.py 2>/dev/null | grep -c 'participes en -é'; done; echo '--- dates ---'; git log -1 --format='%h %ad %s' --date=iso a408a909; git log -1 --format='%h %ad %s' --date=iso f908d7b0; git l … [296 caractères tronqués]`

  ```
f908d7b0: 1
69bd865e: 1
160d08ca: 1
a408a909: 1
--- dates ---
a408a909 2026-11-05 10:39:22 -0500 B13 — LE LEXIQUE ÉLARGI (PARTICIPES IRRÉGULIERS ET EN -É) : EXACT 0,8082 → 0,8483 ; 174/174
f908d7b0 2026-11-05 21:08:09 -0500 B13 — R1/R2/R3 : EXACT 212/212 (1,0000), COUVERTURE 0,887, F1 0,5763, FR 1,0 / EN 1,0 ; 27 SPANS DONT 17 INATTEIGNABLES ; 183/183
160d08ca 2026-11-05 22:56:46 -0500 B13 — LA GARDE PRON : EXACT 219/219 (1,0000), COUVERTURE 0,9163, F1 0,5822, DEV 152/152 ET TEST 67/67 ; AUDIT DE COHÉRENCE V8 INTÉGRÉ ; 183/183
--- ancestry ---
a408 before v8
  ```

### 🤖 Assistant

⏵ Adding exact-equality top-k control

- **bash** `{"command": "python3 - <<'PY'\nimport json, random, statistics\nd=json.load(open('/tmp/audit_v10/resultats.json'))\nv=d['variantes']['v10']; # details removed? check\nprint('keys', list(v.keys())[:20])\nPY", "description": "Check if details saved"}`

  ```
keys ['labels', 'exact', 'exact_any', 'couverture', 'topk', 'topk_taux', 'topk_exact', 'topk_taux_span', 'fr', 'en', 'f1_vivant', 'tete_vivant', 'f1_gele', 'tete_gele', 'spans', 'spans_total', 'spans_liste', 'dev', 'test', 'duree_s']
  ```

### 🤖 Assistant

⏵ Measuring the R1a bundle and exact top-k null

- **bash** `{"command": "python3 - <<'PY'\np='/tmp/audit_v10/harness.py'\ns=open(p).read()\n# add SUJETS snippets\ns=s.replace(\"MODS = pathlib.Path('/tmp/audit_v10/mods'); MODS.mkdir(parents=True, exist_ok=True)\",\n\"\"\"MODS = pathlib.Path('/tmp/audit_v10/mods'); MODS.mkdir(parents=True, exist_ok=True)\n\nSU … [3389 caractères tronqués]`

  ```
patched
exit=0
v10 labels 220 exact 220 f1g 0.588 spans 19 0.8s
v9 labels 219 exact 219 f1g 0.5866 spans 20 0.7s
v8 labels 212 exact 212 f1g 0.5763 spans 27 0.9s
sans_pron labels 203 exact 203 f1g 0.5718 spans 36 0.8s
sans_est_sub labels 219 exact 219 f1g 0.5849 spans 20 0.8s
sans_predicat_vu labels 220 exact 220 f1g 0.588 spans 19 0.7s
sans_ee labels 220 exact 220 f1g 0.588 spans 19 0.9s
sans_gp_det labels 219 exact 219 f1g 0.5866 spans 20 0.8s
v9_attendu labels 219 exact 219 f1g 0.5866 spans 20 0.9s
sans_sujets labels 214 exact 214 f1g 0.5833 spans 25 0.8s
sans_pron_sujets labels 214 exact 214 f1g 0.5808 spans 25 0.8s
{
 "controles": {
  "permutation": {
   "n": 220,
   "observe": 220,
[stderr]

real	0m13,943s
user	0m13,568s
sys	0m0,375s
  ```

### 🤖 Assistant

⏵ Inspecting the R1a bundle effects

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/audit_v10/resultats.json'))\nfor nom in ('sans_sujets','sans_pron_sujets','sans_pron','sans_est_sub','sans_predicat_vu','sans_ee','sans_gp_det'):\n    a=d['ablations'][nom]\n    print('\\n===',nom)\n    for k in ('labels','exact','de … [459 caractères tronqués]`

  ```
=== sans_sujets
  labels 214
  exact 214
  delta_labels -6
  delta_exact -6
  n_gains 6
  n_pertes 0
  n_labels_gagnes 6
  n_labels_perdus 0
  f1_gele 0.5833
  delta_f1_gele -0.0047
  topk 213
  spans_total 25
  spans {'GP': 4, 'REL': 15, 'SUB': 6}
  gains {'dev': ['r273:REL', 's069:REL', 's135:REL'], 'test': ['s032:REL', 's072:REL', 's115:REL']}
  pertes {}

=== sans_pron_sujets
  labels 214
  exact 214
  delta_labels -6
  delta_exact -6
  n_gains 6
  n_pertes 0
  n_labels_gagnes 6
  n_labels_perdus 0
  f1_gele 0.5808
  delta_f1_gele -0.0072
  topk 213
  spans_total 25
  spans {'GP': 4, 'REL': 15, 'SUB': 6}
  gains {'dev': ['r273:REL', 's069:REL', 's135:REL'], 'test': ['s032:REL', 's072:REL', 's115:REL']}
  pertes {}

=== sans_pron
  labels 203
  exact 203
  delta_labels -17
  delta_exact -17
  n_gains 17
  n_pertes 0
  n_labels_gagnes 17
  n_labels_perdus 0
  f1_gele 0.5718
  delta_f1_gele -0.0162
  topk 202
  spans_total 36
  spans {'GP': 4, 'REL': 18, 'SUB': 14}
  gains {'dev': ['g017:SUB', 'r034:REL', 'r074:REL', 'r114:REL', 'r205:SUB', 'r219:SUB', 'r240:SUB', 'r243:REL', 'r247:SUB', 'r278:REL', 'r280:REL', 'r285:REL', 'r296:SUB', 'r299:REL'], 'test': ['r214:REL', 'r216:SUB', 
… [2073 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Fixing the top-k control bug and re-running

- **bash** `{"command": "python3 - <<'PY'\np='/tmp/audit_v10/harness.py'\ns=open(p).read()\ns=s.replace(\"\"\"        topk_perm.append(sum(1 for j,i in enumerate(idx)\n                             if any(any(c in nom for c in cibles[i]) for nom in cands[perm[j]])))\"\"\",\n\"\"\"        topk_perm.append(sum(1 f … [530 caractères tronqués]`

  ```
patched
exit=0
{
 "permutation": {
  "n": 220,
  "observe": 220,
  "tirages": 2000,
  "graine": 0,
  "moyenne": 1.997,
  "mediane": 2.0,
  "max": 10,
  "p95": 5,
  "p": 0.0,
  "lecture": "0.908 % moyen contre 100.0 % observé"
 },
 "candidat": {
  "labels": 220,
  "labels_avec_candidats": 220,
  "candidats_total": 585,
  "tirage": 2000,
  "graine": 0,
  "hasard_top1_moyen": 92.7,
  "hasard_top1_taux": 0.4214,
  "hasard_topk_perm_moyen": 2.53,
  "hasard_topk_perm_taux": 0.0115,
  "observe_top1": 220,
  "observe_topk": 219,
  "p_top1": 0.0,
  "p_topk": 0.0
 },
 "permutation_candidats_exact": {
  "n": 220,
  "tirages": 2000,
  "graine": 0,
  "observe": 219,
  "moyenne": 2.18,
  "taux": 0.0099,
  "max": 8,
  "p": 0.0
 },
 "permutation_candidats_souschaine": {
  "n": 220,
  "tirages": 2000,
  "graine": 0,
  "observe": 219,
  "moyenne": 2.58,
  "taux": 0.0117,
  "max": 9,
  "p": 0.0
 }
}
  ```

### 🤖 Assistant

⏵ Classifying all 19 remaining spans

- **bash** `{"command": "python3 - <<'PY'\nimport json, collections\nd=json.load(open('/tmp/audit_v10/resultats.json'))\nsp=d['spans_v10']\nprint('counts type', collections.Counter(x['type'] for x in sp))\nprint('langue', collections.Counter(x['langue'] for x in sp))\nprint('source', collections.Counter(x['sour … [799 caractères tronqués]`

  ```
counts type Counter({'REL': 9, 'SUB': 6, 'GP': 4})
langue Counter({'fr': 17, 'en': 2})
source Counter({'synthetique': 14, 'reel': 5})
cross Counter({('fr', 'synthetique', 'REL'): 7, ('fr', 'synthetique', 'GP'): 4, ('fr', 'synthetique', 'SUB'): 3, ('fr', 'reel', 'SUB'): 2, ('en', 'reel', 'REL'): 1, ('fr', 'reel', 'REL'): 1, ('en', 'reel', 'SUB'): 1})
A17 subset True extra ['r303', 's037'] missing A17 []
| `s027` | fr | synthetique | GP | 31:33 | il | `marche` | A17 résiduel |
| `s146` | fr | synthetique | GP | 25:35 | les jardin | `observe` | A17 résiduel |
| `s148` | fr | synthetique | GP | 20:39 | les ancienne lettre | `nage` | A17 résiduel |
| `s160` | fr | synthetique | GP | 20:29 | le renard | `nage` | A17 résiduel |
| `r035` | en | reel | REL | 9:24 | she talks about | `film` | A17 résiduel |
| `r255` | fr | reel | REL | 11:27 | que j'ai achetée | `voiture` | A17 résiduel |
| `s010` | fr | synthetique | REL | 10:18 | qui nage | `chemin` | A17 résiduel |
| `s035` | fr | synthetique | REL | 10:19 | qui ferme | `papier` | A17 résiduel |
| `s037` | fr | synthetique | REL | 5:15 | qui marche | `Paul` | s037 (R2 v8) |
| `s061` | fr | synthetique | REL | 9:18 | qui saute | `nuage` | 
… [776 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Assembling ablation and dev/test tables

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/audit_v10/resultats.json'))\nnoms=('v10','sans_pron','sans_sujets','sans_pron_sujets','sans_est_sub','sans_predicat_vu','sans_ee','sans_gp_det','v9','v8')\nprint(f\"{'variante':20s} {'lab':>4} {'exa':>4} {'dE':>4} {'F1g':>7} {'dF1':> … [728 caractères tronqués]`

  ```
variante              lab  exa   dE     F1g     dF1 topk  sp      dev      test
v10                   220  220    0  0.5880  0.0000  219  19  152/152     68/68
sans_pron             203  203  -17  0.5718 -0.0162  202  36  138/138     65/65
sans_sujets           214  214   -6  0.5833 -0.0047  213  25  149/149     65/65
sans_pron_sujets      214  214   -6  0.5808 -0.0072  213  25  149/149     65/65
sans_est_sub          219  219   -1  0.5849 -0.0031  218  20  151/151     68/68
sans_predicat_vu      220  220    0  0.5880  0.0000  219  19  152/152     68/68
sans_ee               220  220    0  0.5880  0.0000  219  19  152/152     68/68
sans_gp_det           219  219   -1  0.5866 -0.0014  218  20  152/152     67/67
v9                    219  219   -1  0.5866 -0.0014  218  20  152/152     67/67
v8                    212  212   -8  0.5763 -0.0117  177  27  148/148     64/64

v10 dev {'cibles': 163, 'labels': 152, 'exact': 152, 'couverture': 0.9325, 'f1': 0.5812, 'tete': 0.733} test {'cibles': 76, 'labels': 68, 'exact': 68, 'couverture': 0.8947, 'f1': 0.589, 'tete': 0.7337}
sans_pron dev {'cibles': 163, 'labels': 138, 'exact': 138, 'couverture': 0.8466, 'f1': 0.5621, 'tete': 0.7215} test {
… [1769 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Confirming target files are new and checking repo cleanliness

- **bash** `{"command": "ls -la reports/rapport-audit-v10.md reports/pensee-audit-v10.json 2>&1; echo '---'; git status --short reports/ | head -20; echo '--- forbidden paths untouched'; git status --short docs/pilotage AGENTS.md journal tools/structures data tools/entrainer_native.py tools/native_model.py 2>/d … [138 caractères tronqués]`

  ```
ls: cannot access 'reports/rapport-audit-v10.md': No such file or directory
ls: cannot access 'reports/pensee-audit-v10.json': No such file or directory
---
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-spans-chunker.md
?? reports/rapport-s-paragraphes.md
--- forbidden paths untouched
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
  ```

### 🤖 Assistant

⏵ Checking the documented autotest invocation

- **bash** `{"command": "python3 tools/pensee/autotest.py > /tmp/audit_v10/autotest_direct.log 2>&1; echo \"exit=$?\"; tail -3 /tmp/audit_v10/autotest_direct.log", "description": "Test direct autotest invocation", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
exit=1
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/pensee/autotest.py", line 32, in <module>
    from .coeur import Candidat, Etat
ImportError: attempted relative import with no known parent package
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/audit_v10/resultats.json'))\n# verify exact topk strict and any\nv=d['variantes']['v10']\nprint('v10 topk',v['topk'],'topk_exact',v['topk_exact'],'topk_taux_span',v['topk_taux_span'])\n# check v9 fiche values\nv9=d['variantes']['v9'] … [433 caractères tronqués]`

  ```
v10 topk 219 topk_exact 219 topk_taux_span 0.9955
v9 {'labels': 219, 'exact': 219, 'couverture': 0.9163, 'topk': 218, 'topk_taux': 0.9121, 'fr': {'cibles': 151, 'labels': 134, 'exact': 134, 'topk': 133}, 'en': {'cibles': 88, 'labels': 85, 'exact': 85, 'topk': 85}, 'f1_vivant': 0.5822, 'f1_gele': 0.5866, 'tete_vivant': 0.7326, 'tete_gele': 0.7381, 'spans_total': 20, 'spans': {'GP': 5, 'REL': 9, 'SUB': 6}}
v10 {'labels': 220, 'exact': 220, 'couverture': 0.9205, 'topk': 219, 'topk_taux': 0.9163, 'fr': {'cibles': 151, 'labels': 134, 'exact': 134, 'topk': 133}, 'en': {'cibles': 88, 'labels': 86, 'exact': 86, 'topk': 86}, 'f1_vivant': 0.5836, 'f1_gele': 0.588, 'tete_vivant': 0.7332, 'tete_gele': 0.7388, 'spans_total': 19, 'spans': {'GP': 4, 'REL': 9, 'SUB': 6}}
  ```

### 🤖 Assistant

⏵ Probing the two stated risks of the new rules

- **bash** `{"command": "python3 - <<'PY'\nimport sys; sys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nh=bl.Heuristique()\nfor t in ['Il parle de la voir.', 'Elle finit de la regarder.', 'Une idée arrive.', 'La entrée est libre.', 'La portée est grande.']:\n    a=h.analyser(t,'fr')\n    print(repr … [390 caractères tronqués]`

  ```
'Il parle de la voir.'
    GV 0 8 'Il parle'
    GV 3 8 'parle'
    GP 9 19 'de la voir'
'Elle finit de la regarder.'
    GV 0 10 'Elle finit'
    GV 5 10 'finit'
    GP 11 25 'de la regarder'
'Une idée arrive.'
    GN 0 8 'Une idée'
    GV 9 15 'arrive'
'La entrée est libre.'
    GN 0 9 'La entrée'
    GV 10 19 'est libre'
'La portée est grande.'
    GN 0 9 'La portée'
    GV 10 20 'est grande'
_est_verbe idée False entrée True portée True aimée True
  ```

### 🤖 Assistant

⏵ Checking whether -ée changes any annotation on the gold

- **bash** `{"command": "python3 - <<'PY'\nimport sys, importlib.util, pathlib\nsys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nph=eg.charger()\ndef load(n):\n    spec=importlib.util.spec_from_file_location('z_'+n,f'/tmp/audit_v10/mods/{n}.py')\n    m=importlib.util.module_from_spec( … [664 caractères tronqués]`

  ```
phrases avec difference: 0
  ```

### 🤖 Assistant

⏵ Measuring the full reach of the GP guard

- **bash** `{"command": "python3 - <<'PY'\nimport sys, importlib.util, pathlib, collections\nsys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nph=eg.charger()\ndef load(n):\n    spec=importlib.util.spec_from_file_location('q_'+n,f'/tmp/audit_v10/mods/{n}.py')\n    m=importlib.util.modu … [679 caractères tronqués]`

  ```
Error: spawn bash ENOENT
  ```

### 🤖 Assistant

⏵ Re-running the GP guard annotation diff

- **bash** `{"command": "python3 - <<'PY'\nimport sys, importlib.util, pathlib\nsys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nph=eg.charger()\ndef load(n):\n    spec=importlib.util.spec_from_file_location('q_'+n,f'/tmp/audit_v10/mods/{n}.py')\n    m=importlib.util.module_from_spec( … [660 caractères tronqués]`

  ```
phrases avec difference: 3
('g004', [], [('syntagme', 'GP', 11, 27), ('syntagme', 'GV', 28, 31)])
('r147', [], [('syntagme', 'GP', 22, 31), ('syntagme', 'GV', 32, 37)])
('r153', [('syntagme', 'GP', 8, 19)], [('syntagme', 'GP', 8, 15), ('syntagme', 'GV', 16, 19)])
  ```

### 🤖 Assistant

⏵ Inspecting the other two GP-guard changes

- **bash** `{"command": "python3 - <<'PY'\nimport sys; sys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nph={p['id']:p for p in eg.charger()}\nfor i in ('g004','r147','r153'):\n    p=ph[i]; print('\\n',i,repr(p['texte']))\n    print(' gold:',[(s['type'],s['debut'],s['fin'],p['texte'][s … [953 caractères tronqués]`

  ```
g004 'Il a couru pour attraper le bus.'
 gold: [('GN', 0, 2, 'Il', None), ('GV', 3, 10, 'a couru', None), ('GP', 11, 31, 'pour attraper le bus', 'couru')]

 r147 'Les clients attendent devant la porte.'
 gold: [('GN', 0, 11, 'Les clients', None), ('GV', 12, 21, 'attendent', None), ('GP', 22, 37, 'devant la porte', 'attendent')]

 r153 'We wait for the bus.'
 gold: [('GN', 0, 2, 'We', None), ('GV', 3, 7, 'wait', None), ('GP', 8, 19, 'for the bus', 'wait')]

### v10
g004 [('GV', 0, 2, 'Il', None), ('GV', 0, 10, 'Il a couru', None), ('GV', 3, 10, 'a couru', None), ('GP', 11, 31, 'pour attraper le bus', {'segment': 'pour attraper le bus', 'cible': 'couru'})]
r147 [('GN', 0, 11, 'Les clients', {'segment': 'Les clients', 'cible': 'attendent'}), ('GV', 12, 21, 'attendent', {'segment': 'attendent', 'cible': 'clients'}), ('GP', 22, 37, 'devant la porte', {'segment': 'devant la porte', 'cible': 'attendent'})]
r153 [('GV', 3, 7, 'wait', None), ('GP', 8, 19, 'for the bus', {'segment': 'for the bus', 'cible': 'wait'})]

### sans_gp_det
g004 [('GV', 0, 2, 'Il', None), ('GV', 0, 10, 'Il a couru', None), ('GV', 3, 10, 'a couru', None), ('GP', 11, 27, 'pour attraper le', {'segment': 'pour attraper 
… [636 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Collecting final official counters

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nimport tools.bloc_linguistique as bl\na=eg.evaluer_bloc('h',bl.Heuristique(),eg.charger())['attachement']\nprint(json.dumps({k:a[k] for k in ('cibles','labels','top1','topk',' … [439 caractères tronqués]`

  ```
{
 "cibles": 239,
 "labels": 220,
 "top1": 220,
 "topk": 219,
 "exact": 220,
 "exact_any": 220,
 "top1_taux": 0.9205,
 "topk_taux": 0.9163,
 "exact_taux": 0.9205,
 "exact_any_taux_span": 1.0,
 "top1_taux_span": 1.0,
 "topk_taux_span": 0.9955,
 "topk_exact": 219,
 "topk_exact_taux": 0.9163,
 "topk_exact_taux_span": 0.9955,
 "exact_taux_span": 1.0,
 "verbe": {
  "cibles": 149,
  "justes": 149,
  "taux": 1.0
 },
 "nom": {
  "cibles": 71,
  "justes": 71,
  "taux": 1.0
 },
 "couverture": 0.9205
}
par langue {
 "fr": {
  "cibles": 151,
  "labels": 134,
  "exact": 134,
  "topk": 133,
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
  ```

### 🤖 Assistant

⏵ Pulling remaining ablation metrics

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/audit_v10/resultats.json'))\nfor n in ('v10','sans_pron','sans_sujets','sans_pron_sujets','sans_est_sub','sans_predicat_vu','sans_ee','sans_gp_det','v9','v8'):\n    v=d['variantes'][n]\n    print(n, 'tete_gele',v['tete_gele'],'f1_viv … [274 caractères tronqués]`

  ```
Error: spawn bash ENOENT
  ```

### 🤖 Assistant

⏵ Re-pulling remaining ablation metrics

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/audit_v10/resultats.json'))\nfor n in ('v10','sans_pron','sans_sujets','sans_pron_sujets','sans_est_sub','sans_predicat_vu','sans_ee','sans_gp_det','v9','v8'):\n    v=d['variantes'][n]\n    print(n, 'tete_gele',v['tete_gele'],'f1_viv … [280 caractères tronqués]`

  ```
v10 tete_gele 0.7388 f1_vivant 0.5836 tete_vivant 0.7332 topk 219 topk_taux 0.9163 spans_total 19 spans {'GP': 4, 'REL': 9, 'SUB': 6}
sans_pron tete_gele 0.7288 f1_vivant 0.5676 tete_vivant 0.7234 topk 202 topk_taux 0.8452 spans_total 36 spans {'GP': 4, 'REL': 18, 'SUB': 14}
sans_sujets tete_gele 0.7369 f1_vivant 0.5789 tete_vivant 0.7313 topk 213 topk_taux 0.8912 spans_total 25 spans {'GP': 4, 'REL': 15, 'SUB': 6}
sans_pron_sujets tete_gele 0.7343 f1_vivant 0.5764 tete_vivant 0.7288 topk 213 topk_taux 0.8912 spans_total 25 spans {'GP': 4, 'REL': 15, 'SUB': 6}
sans_est_sub tete_gele 0.7367 f1_vivant 0.5805 tete_vivant 0.7312 topk 218 topk_taux 0.9121 spans_total 20 spans {'GP': 4, 'REL': 10, 'SUB': 6}
sans_predicat_vu tete_gele 0.7388 f1_vivant 0.5836 tete_vivant 0.7332 topk 219 topk_taux 0.9163 spans_total 19 spans {'GP': 4, 'REL': 9, 'SUB': 6}
sans_ee tete_gele 0.7388 f1_vivant 0.5836 tete_vivant 0.7332 topk 219 topk_taux 0.9163 spans_total 19 spans {'GP': 4, 'REL': 9, 'SUB': 6}
sans_gp_det tete_gele 0.7381 f1_vivant 0.5822 tete_vivant 0.7326 topk 218 topk_taux 0.9121 spans_total 20 spans {'GP': 5, 'REL': 9, 'SUB': 6}
v9 tete_gele 0.7381 f1_vivant 0.5822 tete_vivant 0.7326 topk 2
… [203 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Writing the audit JSON

- **bash** `{"command": "cat > /tmp/audit_v10/build_json.py <<'PY'\nimport json, pathlib\nR = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\n\ndef lang(cibles, labels, exact, topk):\n    return {'cibles': cibles, 'labels': labels, 'exact': exact,\n            'couverture': round(labels/cibles, … [16328 caractères tronqués]`

  ```
written /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-audit-v10.json 25984
  ```

### 🤖 Assistant

⏵ Validating the audit JSON

- **bash** `{"command": "python3 -m json.tool reports/pensee-audit-v10.json > /dev/null && echo 'JSON valide'; python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-v10.json'))\nprint('top keys:', list(d.keys()))\nprint('verdict:', d['verdict']['resume'][:200])\nprint('ablations:', list(d['ablat … [280 caractères tronqués]`

  ```
JSON valide
top keys: ['rapport', 'ligne', 'branche', 'commit_audite', 'commit_parent', 'date', 'objet', 'methode', 'verdict', 'rejeu', 'ablations', 'controle_negatif', 'spans_19', 'dev_test', 'portes_autotest', 'ecarts', 'limites', 'fichiers_ecrits', 'commit']
verdict: Les valeurs v10 rejouent (220/220, 0,9205, 0,5880, 0,7388, 134/134, 86/86, 19 spans, top-k 219). Deux valeurs sont fausses : le F1 « avant » (0,5822 vivant, 0,5866 gelé) et le test (68/68, pas 67/67).
ablations: ['garde_pron', 'expansion_sujets', 'garde_pron_et_sujets', 'est_sub', 'predicat_vu', 'ee', 'garde_det_gp', 'v9', 'v8']
spans: 19 {'REL': 9, 'SUB': 6, 'GP': 4} 19
controles: ['permutation_globale', 'candidat_aleatoire', 'permutation_candidats_topk_exact', 'permutation_candidats_topk_souschaine', 'spans_19_verifies']
  ```

### 🤖 Assistant

⏵ Writing the audit report

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v10.md", "content": "# Audit v10 — les chiffres rejouent, l'attribution des corrections ne rejoue pas\n\n> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·\n> **Commit audité** : ` … [22240 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v10.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Proofreading the report and checking repo state

- **bash** `{"command": "git status --short reports/rapport-audit-v10.md reports/pensee-audit-v10.json; echo '---'; wc -l reports/rapport-audit-v10.md; echo '---'; grep -n \"0,5822\\|67/67\\|68/68\\|r303\\|s037\\|acheter\\|a408a909\" reports/rapport-audit-v10.md | head -40", "description": "Check new files and  … [74 caractères tronqués]`

  ```
?? reports/pensee-audit-v10.json
?? reports/rapport-audit-v10.md
---
327 reports/rapport-audit-v10.md
---
13:la seconde, le **`-ée`**, est **antérieure à la v10** (commit `a408a909`, déjà dans v8 et v9)
15:car `acheter` n'est pas dans le lexique. Le **seul** gain v10 est la **garde DET du GP**
17:`r264` » : `r255`/`r264` sont déjà dans les 17 ; les deux extras réels sont **`s037`**
18:(7e régression v8, toujours ouverte) et **`r303`** (régression v9 par `predicat_vu`, non
19:listée). Enfin, le F1 « avant » **0,5822** est la valeur du **vivant 612** ; le **gelé 602**
21:est **68/68**, pas 67/67.
37:  module `v9` (`160d08ca`) : **219/219, F1 gelé 0,5866, 20 spans, dev 152/152, test 67/67**.
72:1. **F1 « avant » (v9)** : la fiche et le JSON donnent **0,5822** en le présentant comme
73:   « gelé 602 » (ligne F1). Or **0,5822 est la valeur du vivant 612** ; sur le gelé 602, la
74:   v9 vaut **0,5866**. Le tableau « avant / après » compare donc **0,5822 (vivant)** à
77:2. **dev / test** : la fiche dit « dev 152/152, test 67/67 (avant ces deux corrections) ».
78:   C'est exact pour la **v9** ; après la garde DET du GP, le **test v10 est 68/68**
89:| F1 union | 0,5822 (« gelé 602 ») | **0,
… [2639 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re, json\nmd=open('reports/rapport-audit-v10.md').read()\nj=json.load(open('reports/pensee-audit-v10.json'))\n# verify key values in text\nfor s in ['220/220','0,9205','0,5880','0,7388','134/134','86/86','top-k 219','19 spans','68/68','0,5866','r153','r303','s03 … [358 caractères tronqués]`

  ```
220/220 7
0,9205 5
0,5880 7
0,7388 3
134/134 8
86/86 5
top-k 219 2
19 spans 8
68/68 8
0,5866 12
r153 11
r303 18
s037 10
a408a909 3
json verdict 2 183/183
json spans 19 {'REL': 9, 'SUB': 6, 'GP': 4}
json devtest {'dev': {'phrases': 422, 'cibles': 163, 'labels': 152, 'exact': 152, 'couverture': 0.9325, 'f1': 0.5812, 'tete': 0.733}, 'test': {'phrases': 190, 'cibles': 76, 'labels': 68, 'exact': 68, 'couverture': 0.8947, 'f1': 0.589, 'tete': 0.7337}, 'par_langue': {'dev': {'fr': '91/91', 'en': '61/61'}, 'test': {'fr': '43/43', 'en': '25/25'}}}
  ```

### 🤖 Assistant

⏵ Verifying the -ée rule is inert down to metadata

- **bash** `{"command": "python3 - <<'PY'\nimport sys, importlib.util, pathlib, json\nsys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nph=eg.charger()\ndef load(n):\n    spec=importlib.util.spec_from_file_location('r_'+n,f'/tmp/audit_v10/mods/{n}.py')\n    m=importlib.util.module_from … [733 caractères tronqués]`

  ```
phrases avec difference JSON: 0 []
  ```

### 🤖 Assistant

⏵ Clarifying the v9 dev/test row

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v10.md", "old_string": "| top-k | 218 ; 0,9121 | **218 ; 0,9121** | **218 ; 0,9121** | 0 |\n| spans | 20 (9 REL, 6 SUB, 5 GP) | **20 (9/6/5)** | **20 (9/6/5)** | 0 (comptes) |\n| dev / test | 152/152, 67/67 | **152/ … [398 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v10.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Checking the claimed 19 autotest assertions

- **bash** `{"command": "git diff 160d08ca 710ec7f9 -- tools/pensee/autotest.py | grep -E '^[-+].*return|^[-+] *abs|^[-+] *a\\[' | wc -l; echo '--- functions changed ---'; git diff 160d08ca 710ec7f9 -- tools/pensee/autotest.py | grep -E '^@@' | wc -l; git diff 160d08ca 710ec7f9 -- tools/pensee/autotest.py | gre … [136 caractères tronqués]`

  ```
34
--- functions changed ---
19
@@ -1668,7 +1668,7 @@ def t109_anaphore_103() -> tuple[bool, str]:
@@ -1681,7 +1681,7 @@ def t110_segmenteur() -> tuple[bool, str]:
@@ -1728,7 +1728,7 @@ def t112_union() -> tuple[bool, str]:
@@ -1740,7 +1740,7 @@ def t113_union_defaut() -> tuple[bool, str]:
@@ -1754,7 +1754,7 @@ def t114_cascade_union() -> tuple[bool, str]:
@@ -2223,8 +2223,8 @@ def t153_attachement() -> tuple[bool, str]:
@@ -2341,7 +2341,7 @@ def t161_cible_proximite() -> tuple[bool, str]:
@@ -2352,7 +2352,7 @@ def t162_candidats_verbes() -> tuple[bool, str]:
@@ -2375,7 +2375,7 @@ def t163_echecs_attachement() -> tuple[bool, str]:
@@ -2388,7 +2388,7 @@ def t164_verbe_gv() -> tuple[bool, str]:
@@ -2419,7 +2419,7 @@ def t166_spans() -> tuple[bool, str]:
@@ -2428,9 +2428,9 @@ def t167_denominateur() -> tuple[bool, str]:
@@ -2457,7 +2457,7 @@ def t168_classement() -> tuple[bool, str]:
@@ -2467,7 +2467,7 @@ def t169_conventions() -> tuple[bool, str]:
@@ -2494,7 +2494,7 @@ def t171_lexique_elargi() -> tuple[bool, str]:
@@ -2529,10 +2529,10 @@ def t173_topk_strict() -> tuple[bool, str]:
@@ -2593,7 +2593,7 @@ def t177_candidats_tete() -> tuple[bool, str]:
@@ -2627,7 +2627,7 @@ def t179_mul
… [97 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Refining the dev/test wording to avoid overclaiming

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-audit-v10.md'\ns=open(p).read()\ns=s.replace(\"\"\"est **68/68**, pas 67/67.\n\n## 1. Dispositif\"\"\",\"\"\"n'est pas actualisé : **68/68**, pas 67/67 (le 67/67 est explicitement la v9).\n\n## 1. Dispositif\"\"\")\ns=s.replace(\"\"\"2. **dev / test* … [2001 caractères tronqués]`

  ```
ok
json ok
  ```

### 🤖 Assistant

⏵ Reading the report end-to-end

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v10.md", "limit": 140}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v10.md</path>
<type>file</type>
<content>
1: # Audit v10 — les chiffres rejouent, l'attribution des corrections ne rejoue pas
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
4: > **Commit audité** : `710ec7f9` (parent `160d08ca`) · **Date** : 2026-11-05 ·
5: > **Verdict** : chiffres ✅ (deux écarts), règles ❌, portes ✅.
6: > **Aucun fichier existant modifié ; aucun commit.** Sorties : ce rapport et
7: > [`pensee-audit-v10.json`](pensee-audit-v10.json).
8: 
9: **En une phrase.** Les valeurs de la fiche [`rapport-pensee-v10.md`](rapport-pensee-v10.md)
10: rejouent presque toutes : **220/220**, couverture **0,9205**, **F1 0,5880** (gelé 602),
11: **tête 0,7388**, **fr 134/134**, **en 86/86**, **19 spans** (9 REL, 6 SUB, 4 GP),
12: **top-k 219**, **183/183 portes**. Mais la fiche attribue le gain à **deux** corrections :
13: la seconde, le **`-ée`**, est **antérieure à la v10** (commit `a408a909`, déjà dans v8 et v9)
14: et **inerte sur ce gold** (0 différence d'annotation sur 612 phrases) ; `r255` reste absent
15: car `acheter` n'est pas dans le lexique. Le **seul** 
… [8670 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys; sys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nph=eg.charger(); ge=eg.charger_gele()\nprint('tokens vivant', sum(len(p['mots']) for p in ph), 'gele', sum(len(p['mots']) for p in ge))\nprint('sources', {s:sum(1 for p in ph if p.g … [210 caractères tronqués]`

  ```
tokens vivant 3179 gele 3141
sources {'hand': 20, 'reel': 432, 'synthetique': 160}
phrases 612 602
  ```

### 🤖 Assistant

⏵ Reading the rest of the report

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v10.md", "offset": 141, "limit": 200}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v10.md</path>
<type>file</type>
<content>
141: - **Garde PRON** — gains : `g017 r034 r074 r114 r205 r219 r240 r243 r247 r278 r280 r285
142:   r296 r299` (dev), `r214 r216 r281` (test) ; aucune perte.
143: - **Expansion SUJETS** — gains : `r273 s069 s135` (dev), `s032 s072 s115` (test) ; aucune
144:   perte. **PRON + SUJETS** : mêmes six gains, mêmes pertes nulles.
145: - **`est_sub`** — gain : `r280` (dev) ; aucune perte.
146: - **`predicat_vu`** — gain : `g017` (dev) ; **perte : `r303`** (dev).
147: - **`-ée`** — aucun gain, aucune perte.
148: - **Garde DET du GP** — gain : `r153` (test) ; aucune perte.
149: - **v8 → v10** — 9 gains (`g017 r273 r280 s069 s135` dev ; `r153 s032 s072 s115` test),
150:   1 perte (`r303` dev) : net **+8** (212 → 220).
151: 
152: ### 4.2 Ce que les ablations disent
153: 
154: - **Le `-ée` est totalement inerte sur ce gold.** Retirer la boucle ne change **aucune**
155:   étiquette (niveau, type, span) sur les **612** phrases : labels, exact, F1, top-k et spans
156:   sont identiques. `_est_verbe("achetée")` reste **False** car `acheter` n'est **pas** dans
157:   `VERBES_CONNUS` 
… [13162 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Tightening the arithmetic and test wording

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-audit-v10.md'\ns=open(p).read()\ns=s.replace(\"\"\"- **L'arithmétique ne somme pas** : 212 + (6 REL + `r280` + `g017`) = 220, mais la v9 donne\n  **219** ; la différence est **`r303`**, perdue. Mesure : **8 gains bruts, 1 perte, net +7**\n  (212 → 21 … [729 caractères tronqués]`

  ```
ok
  ```

### 🤖 Assistant

⏵ Checking JSON consistency with the report

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-v10.json'))\nprint(json.dumps(d['verdict'],ensure_ascii=False,indent=1))\nprint('--- ecarts ---')\nfor e in d['ecarts']:\n    print(e['gravite'],'|',e['grandeur'],'|',e['fiche'],'->',e['mesure'])\nprint('--- rejeu v9  … [275 caractères tronqués]`

  ```
{
 "chiffres_rejoues": true,
 "ecarts_chiffres": 2,
 "regles_justes": false,
 "portes": "183/183",
 "resume": "Les valeurs v10 rejouent (220/220, 0,9205, 0,5880, 0,7388, 134/134, 86/86, 19 spans, top-k 219). Deux écarts de valeur : le F1 « avant » (0,5822 vivant, 0,5866 gelé) et le test non actualisé (68/68, pas 67/67, valeur v9 explicite). Les règles ne rejouent pas : la seule correction v10 est la garde DET du GP (+1, r153) ; le -ée est antérieur et inerte (0 différence sur 612 phrases), r255 reste absent. Les 19 spans sont 17 résiduels + s037 + r303, pas 17 + r255 + r264 ; r303 est une perte cachée du predicat_vu v9 (net 0 avec g017)."
}
--- ecarts ---
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 6, in <module>
KeyError: 'mesure'
[exit code: 1]
  ```

### 🤖 Assistant

⏵ Inspecting discrepancy entries safely

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-v10.json'))\nfor e in d['ecarts']:\n    print('\\n',e['gravite'],'|',e['grandeur'])\n    for k,v in e.items():\n        if k not in ('gravite','grandeur'): print('  ',k,':',v)\nprint('\\n--- rejeu v9 f1 ---', d['rejeu … [249 caractères tronqués]`

  ```
majeure | F1 union (état v9, colonne « avant » de la v10)
   fiche : 0.5822
   mesure_gele_602 : 0.5866
   mesure_vivant_612 : 0.5822
   note : 0,5822 est la valeur du vivant 612 ; le gelé 602 vaut 0,5866. La v9 étiquette 0,5822 « gelé 602 » ; la v10 la reprend en « avant ». Le gain v9→v10 est +0,0014, pas +0,0058.

 moyenne | dev / test
   fiche : 152/152, 67/67 (daté « avant corrections »)
   mesure : 152/152, 68/68
   note : Le 67/67 est explicitement la v9 ; la valeur courante v10 est test 68/68 (+1 par r153), dev 152/152. Le JSON v10 ne publie pas dev/test.

 majeure | décomposition des 19 spans
   fiche : 17 inatteignables + r255 + r264
   mesure : 17 résiduels + s037 + r303
   note : r255 et r264 sont déjà dans les 17 ; les deux extras réels sont s037 et r303.

 majeure | attribution des corrections
   fiche : -ée + garde DET du GP
   mesure : garde DET du GP seule
   note : -ée est présent dès a408a909 (avant v8), sans effet mesurable sur ce gold ; le commit 710ec7f9 ne modifie que la boucle GP.

 majeure | 7 régressions v8 réparées
   fiche : 7
   mesure : 6
   note : s037 (la 7e) reste absente ; les 6 réparées sont r273 s032 s069 s072 s115 s135.

 majeure | table v9 (212 
… [532 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-v10.json'))\nprint(json.dumps(d['rejeu']['v10'],ensure_ascii=False,indent=1)[:3500])\nPY", "description": "Inspect v10 replay JSON", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
{
 "vivant_612": {
  "labels": 220,
  "exact": 220,
  "exact_span": 1.0,
  "exact_any": 220,
  "couverture": 0.9205,
  "topk": 219,
  "topk_taux": 0.9163,
  "topk_exact": 219,
  "topk_taux_span": 0.9955,
  "fr": {
   "cibles": 151,
   "labels": 134,
   "exact": 134,
   "couverture": 0.8874,
   "topk": 133
  },
  "en": {
   "cibles": 88,
   "labels": 86,
   "exact": 86,
   "couverture": 0.9773,
   "topk": 86
  },
  "f1": 0.5836,
  "f1_s": 0.4957,
  "f1_chunker": 0.6163,
  "tete": 0.7332,
  "spans": {
   "REL": 9,
   "SUB": 6,
   "GP": 4,
   "total": 19
  },
  "verbe": {
   "cibles": 149,
   "justes": 149,
   "taux": 1.0
  },
  "nom": {
   "cibles": 71,
   "justes": 71,
   "taux": 1.0
  }
 },
 "gele_602": {
  "labels": 220,
  "exact": 220,
  "exact_span": 1.0,
  "exact_any": 220,
  "couverture": 0.9205,
  "topk": 219,
  "topk_taux": 0.9163,
  "topk_exact": 219,
  "topk_taux_span": 0.9955,
  "fr": {
   "cibles": 151,
   "labels": 134,
   "exact": 134,
   "couverture": 0.8874,
   "topk": 133
  },
  "en": {
   "cibles": 88,
   "labels": 86,
   "exact": 86,
   "couverture": 0.9773,
   "topk": 86
  },
  "f1": 0.588,
  "f1_s": 0.5014,
  "f1_chunker": 0.6203,
  "tete": 0.7388,
  "spans": {

… [2299 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Fixing two JSON notes for accuracy

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='reports/pensee-audit-v10.json'\nd=json.load(open(p))\nd['rejeu']['v10']['note']=\"labels/exact/couverture/top-k identiques sur les deux golds ; F1/S/chunker/tête sont les valeurs du gelé 602 dans la fiche ; les valeurs vivant 612 sont mesurées ici, la f … [485 caractères tronqués]`

  ```
ok
  ```

### 🤖 Assistant

⏵ Validating final outputs and links

- **bash** `{"command": "python3 -m json.tool reports/pensee-audit-v10.json >/dev/null && echo 'JSON OK'; python3 - <<'PY'\nimport re, pathlib\np=pathlib.Path('reports/rapport-audit-v10.md')\ns=p.read_text()\nlinks=re.findall(r'\\]\\(([^)]+)\\)',s)\nfor l in sorted(set(links)):\n    if l.startswith('http'): con … [213 caractères tronqués]`

  ```
JSON OK
OK  ../tools/bloc_linguistique.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py
OK  pensee-audit-v10.json -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-audit-v10.json
OK  rapport-audit-r1r3.md -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-r1r3.md
OK  rapport-audit-v10.md -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-v10.md
OK  rapport-pensee-v10.md -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-v10.md
  ```

- **bash** `{"command": "git status --short | grep -E 'rapport-audit-v10|pensee-audit-v10'; echo '--- diff stat (new files only)'; git status --short | wc -l; echo '--- forbidden tools ---'; git status --short tools/bloc_linguistique.py tools/pensee/autotest.py tools/tests/linguistique/evaluer_gold.py tools/tes … [252 caractères tronqués]`

  ```
?? reports/pensee-audit-v10.json
?? reports/rapport-audit-v10.md
--- diff stat (new files only)
106
--- forbidden tools ---
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
  ```

### 🤖 Assistant

⏵ Cross-checking gate messages cited

- **bash** `{"command": "grep -E 'T153|T161|T162|T163|T166|T167|T173|T180' /tmp/audit_v10/autotest.log", "description": "Read cited gate messages", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
✅ T153 attachement       attachement : top1 0.9205, exact 0.9205, couverture 0.9205
  ✅ T161 cible proximité   proximité : top1 220/239, exact 220/239, tête 220/145
  ✅ T162 candidats verbes  candidats : top-k 219/239 (0.9163), tête 219/220
  ✅ T163 échecs attachement échecs : 19 de span, 1 de cible (33 avant les correctifs)
  ✅ T166 spans perdus      spans : 9 REL, 6 SUB, 4 GP
  ✅ T167 dénominateur      dénominateur : spans 1.0 / 0.9955 / 1.0
  ✅ T173 top-k strict      top-k : 219 sous-chaîne, 219 exacts (0.9955)
  ✅ T180 par langue        langues : fr 134/134, en 86/86 (86/88 labels)
  ```

### 🤖 Assistant

⏵ Inspecting the odd T161 denominator

- **bash** `{"command": "sed -n '2325,2360p' tools/pensee/autotest.py", "description": "Read T161 implementation", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
"""Les passifs sans par : le chunker 3/3 patient."""
    import tools.bloc_linguistique as bl
    h = bl.Heuristique(segmenter_s=False)
    ok = 0
    for txt in ("Le livre est lu.", "La porte est ouverte.", "Les enfants sont partis."):
        a = h.analyser(txt, "fr")
        roles = [(e.meta or {}).get("role") for e in a.etiquettes
                 if e.niveau == "syntagme" and e.type == "GN"]
        if roles and roles[0] == "patient":
            ok += 1
    return ok == 3, f"passif sans par (chunker) : {ok}/3 patient"


def t161_cible_proximite() -> tuple[bool, str]:
    """La cible par proximité : 212/212 avec la règle du précédent."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    r = evaluer_bloc("h", bl.Heuristique(), charger())
    a, th = r["attachement"], r["attachement_tete"]
    return (a["cibles"] == 239 and a["top1"] == 220 and a["exact"] == 220), (
        f"proximité : top1 {a['top1']}/239, exact {a['exact']}/239, "
        f"tête {th['top1']}/145")


def t162_candidats_verbes() -> tuple[bool, str]:
    """Les candidats verbes : le top-k atteint 211/239 (0,8828) après le correctif du précédent.
… [514 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Scanning gate docstrings for stale numbers

- **bash** `{"command": "python3 - <<'PY'\nimport ast\nsrc=open('tools/pensee/autotest.py').read()\nt=ast.parse(src)\nfor node in t.body:\n    if isinstance(node,ast.FunctionDef) and node.name.startswith('t1') and int(node.name[1:])>=153:\n        doc=ast.get_docstring(node) or ''\n        if doc: print(node.na … [126 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
ValueError: invalid literal for int() with base 10: '1_rejeu'
[exit code: 1]
  ```

### 🤖 Assistant

⏵ Listing T153+ docstrings safely

- **bash** `{"command": "python3 - <<'PY'\nimport ast,re\nsrc=open('tools/pensee/autotest.py').read()\nt=ast.parse(src)\nfor node in t.body:\n    if isinstance(node,ast.FunctionDef):\n        m=re.match(r't(\\d+)_',node.name)\n        if m and 153<=int(m.group(1))<=180:\n            doc=(ast.get_docstring(node) … [189 caractères tronqués]`

  ```
t153_attachement             L'attachement sur le gold 612 (239 cibles) : top1 0,887, exact 0,887, couverture 0,887.
t154_cibles                  Les cibles de l'attachement : 1624 segments sans cible sur 1863.
t155_cibles_500              Les 500 premiers segments : 294 GN, 206 GV.
t156_relation                La relation GN → GV : 257/546 (0,4707).
t157_roles                   Les GN sans rôle : 231, dont 151 avant le GV et 46 après.
t158_passifs                 Les passifs : 5/5 faux par la position seule.
t159_passifs_corriges        Le correctif des passifs : _role_gp rend agent, le generateur S court-circuite.
t160_passifs_sans_par        Les passifs sans par : le chunker 3/3 patient.
t161_cible_proximite         La cible par proximité : 212/212 avec la règle du précédent.
t162_candidats_verbes        Les candidats verbes : le top-k atteint 211/239 (0,8828) après le correctif du précédent.
t163_echecs_attachement      Les échecs de l'attachement : 27 de span, 1 de cible.
t164_verbe_gv                Le verbe du GV-phrase : le POS VERB, pas le dernier mot.
t165_lexique_verbal          Le lexique verbal arbitre le POS : « talks » est un verbe, « brother » n'en est pas un.
t166_
… [1551 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Auditing gate docstrings for stale values

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/audit_v10/resultats.json'))['variantes']['v10']\nprint('v10 exact',d['exact'],'labels',d['labels'],'topk',d['topk'],'topk_exact',d['topk_exact'],'spans',d['spans'])\nprint('fr',d['fr'],'en',d['en'])\nprint('att tete',d.get('tete_gele … [125 caractères tronqués]`

  ```
v10 exact 220 labels 220 topk 219 topk_exact 219 spans {'GP': 4, 'REL': 9, 'SUB': 6}
fr {'cibles': 151, 'labels': 134, 'exact': 134, 'topk': 133} en {'cibles': 88, 'labels': 86, 'exact': 86, 'topk': 86}
att tete 0.7388
  ```

### 🤖 Assistant

⏵ Adding the stale gate docstrings finding

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-audit-v10.md'\ns=open(p).read()\nold=\"\"\"mesurées : `T153` top-1/exact 0,9205, `T161` 220/239, `T162` top-k 219/239 et tête 219/220,\n`T163` 19 spans et 1 cible, `T166` 9 REL / 6 SUB / 4 GP, `T167` labels 220 et top-k span\n0,9955, `T173` 219 sous- … [3033 caractères tronqués]`

  ```
ok
  ```

### 🤖 Assistant

⏵ Adding stale docstrings to the JSON

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='reports/pensee-audit-v10.json'\nd=json.load(open(p))\ndocstrings=[\n {'porte':'T153','docstring':'top1/exact/couverture 0,887','mesure':'0,9205 / 0,9205 / 0,9205'},\n {'porte':'T161','docstring':'212/212','mesure':'220/220'},\n {'porte':'T162','docstrin … [1674 caractères tronqués]`

  ```
ok
JSON OK
  ```

### 🤖 Assistant

⏵ Reading the updated gates section

- **bash** `{"command": "sed -n '250,310p' reports/rapport-audit-v10.md", "description": "Read updated gates section", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
en dev. La fiche v10 publie encore le **test 67/67** en le datant d'avant les corrections ;
la valeur courante est **68/68**.

## 7. Portes

`PYTHONPATH=. python3 -m tools.pensee.autotest` → **183/183 portes tenues**, exit 0,
**0 échec**. Les assertions du périmètre attachement/segmentation portent bien les valeurs
mesurées : `T153` top-1/exact 0,9205, `T161` 220/239, `T162` top-k 219/239 et tête 219/220,
`T163` 19 spans et 1 cible, `T166` 9 REL / 6 SUB / 4 GP, `T167` labels 220 et top-k span
0,9955, `T173` 219 sous-chaîne et 219 exacts (0,9955), `T180` fr 134/134 et en 86/86. Les
portes **entérinent** les valeurs courantes ; elles ne testent pas l'attribution des règles
(le `-ée` inerte et `r303` passent sans être vus).

**Onze docstrings du périmètre attachement/segmentation sont périmées** : elles contredisent
leur propre assertion (qui, elle, passe). Le commit `710ec7f9` a mis à jour 19 assertions,
pas ces textes.

| porte | docstring | mesure affichée |
|---|---|---|
| T153 | top1/exact/couverture 0,887 | **0,9205 / 0,9205 / 0,9205** |
| T161 | 212/212 | **220/220** |
| T162 | 211/239 (0,8828) | **219/239 (0,9163)** |
| T163 | 27 de span | **19 de span** |
| T166 | 16 REL, 6 S
… [2500 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Verifying JSON gate fields

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-v10.json'))\nprint(json.dumps(d['portes_autotest'],ensure_ascii=False,indent=1)[:2500])\nprint('\\nlast ecarts:')\nfor e in d['ecarts'][-2:]: print(e)\nPY", "description": "Inspect JSON gates and last discrepancies",  … [61 caractères tronqués]`

  ```
{
 "commande": "PYTHONPATH=. python3 -m tools.pensee.autotest",
 "resultat": "183/183, exit 0",
 "echecs": 0,
 "note": "183/183, exit 0. L'invocation directe python3 tools/pensee/autotest.py échoue sur l'import relatif (ImportError) ; utiliser -m. Onze docstrings du périmètre attachement/segmentation contredisent leur assertion (elles annoncent encore 212/0,887/27/211).",
 "docstrings_perimees": [
  {
   "porte": "T153",
   "docstring": "top1/exact/couverture 0,887",
   "mesure": "0,9205 / 0,9205 / 0,9205"
  },
  {
   "porte": "T161",
   "docstring": "212/212",
   "mesure": "220/220"
  },
  {
   "porte": "T162",
   "docstring": "211/239 (0,8828)",
   "mesure": "219/239 (0,9163)"
  },
  {
   "porte": "T163",
   "docstring": "27 de span",
   "mesure": "19 de span"
  },
  {
   "porte": "T166",
   "docstring": "16 REL, 6 SUB, 5 GP (27)",
   "mesure": "9 REL, 6 SUB, 4 GP (19)"
  },
  {
   "porte": "T167",
   "docstring": "exactitude spans ÷ 212",
   "mesure": "÷ 220"
  },
  {
   "porte": "T172",
   "docstring": "exact 212/212",
   "mesure": "220/220"
  },
  {
   "porte": "T173",
   "docstring": "211/212 (0,9953) ; 211/239 (0,8828)",
   "mesure": "219/220 (0,9955) ; 219/239 (0,9163)"
  }
… [746 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking T161's tête denominator

- **bash** `{"command": "python3 - <<'PY'\nimport sys,json; sys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nimport tools.bloc_linguistique as bl\nr=eg.evaluer_bloc('h',bl.Heuristique(),eg.charger())\nprint(json.dumps(r['attachement_tete'],indent=1))\nPY", "description": "Check attach … [82 caractères tronqués]`

  ```
{
 "cibles": 221,
 "labels": 221,
 "top1": 221,
 "topk": 220,
 "top1_taux": 1.0,
 "topk_taux": 0.9955,
 "couverture": 1.0
}
  ```

### 🤖 Assistant

⏵ Reproducing T161's tête count

- **bash** `{"command": "PYTHONPATH=. python3 - <<'PY'\nfrom tools.pensee.autotest import t161_cible_proximite\nprint(t161_cible_proximite())\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\nr=evaluer_bloc('h',bl.Heuristique(),charger())\nprint(r['a … [122 caractères tronqués]`

  ```
(False, 'proximité : top1 221/239, exact 221/239, tête 221/145')
{'cibles': 221, 'labels': 221, 'top1': 221, 'topk': 220, 'top1_taux': 1.0, 'topk_taux': 0.9955, 'couverture': 1.0}
  ```

### 🤖 Assistant

⏵ Investigating a reproducibility discrepancy (220 vs 221)

- **bash** `{"command": "python3 - <<'PY'\nimport hashlib,subprocess,pathlib\np=pathlib.Path('tools/bloc_linguistique.py'); cur=p.read_bytes()\ncom=subprocess.run(['git','show','710ec7f9:tools/bloc_linguistique.py'],capture_output=True).stdout\nprint('bloc current==commit:',cur==com, hashlib.sha256(cur).hexdige … [516 caractères tronqués]`

  ```
bloc current==commit: False 04545a07d41e
--- structures status ---
 M donnees/paragraphes-validations.jsonl
--- structures head ---
523d8c1e8c6ca29ca415360a71bfab6c5b56102c
--- mtimes ---
2026-11-04 11:41:49.129836555 -0500 tools/structures/generateur.py
2026-11-06 00:15:37.544747590 -0500 tools/bloc_linguistique.py
--- generateur imports ---
12:from __future__ import annotations
14:import json
15:import re
16:import unicodedata
44:facile faciles difficile difficiles important importante importants importantes
638:    import sys
  ```

### 🤖 Assistant

⏵ The working tree changed under us; diffing the live module

- **bash** `{"command": "git diff -- tools/bloc_linguistique.py | head -80; echo '--- status ---'; git status --short tools/bloc_linguistique.py tools/pensee/autotest.py", "description": "Diff dirty working-tree module", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 329298c4..2b77673b 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -896,9 +896,9 @@ class Heuristique:
                     or est_verbe(suivant[0], suivant[2]))))
                 if marqueur:
                     precedent = segments[-1]["type"] if segments else None
-                    # R2 : sans segment précédent, un marqueur ouvre une **SUB** (« When it rains »)
-                    stype = "SUB" if (n in SUBORDONNANTS or precedent == "GV"
-                                      or precedent is None) else "REL"
+                    # R2 : un **subordonnant** ouvre une SUB (« When it rains ») ; une relative
+                    # en tête reste une REL (« Paul qui marche »)
+                    stype = "SUB" if (est_sub(n) or n in SUBORDONNANTS or precedent == "GV") else "REL"
                     j = i + 1
                     verbes_vus = 0
                     prec_aux = False      # le mot précédent est un auxiliaire (même groupe)
@@ -927,10 +927,7 @@ class Heuristique:
                             if prec_aux:
                                 predicat_vu = True   # « is r
… [610 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Pinning the harness to commit 710ec7f9

- **bash** `{"command": "python3 - <<'PY'\np='/tmp/audit_v10/harness.py'\ns=open(p).read()\ns=s.replace(\"SOURCE = (RACINE/'tools/bloc_linguistique.py').read_text(encoding='utf-8')\",\n\"\"\"_COMMIT = '710ec7f9'\nSOURCE = subprocess.run(['git','show',f'{_COMMIT}:tools/bloc_linguistique.py'],\n                   … [404 caractères tronqués]`

  ```
pinned
exit=0
v10 labels 220 exact 220 f1g 0.588 spans 19 0.8s
v9 labels 219 exact 219 f1g 0.5866 spans 20 0.8s
v8 labels 212 exact 212 f1g 0.5763 spans 27 0.9s
sans_pron labels 203 exact 203 f1g 0.5718 spans 36 0.7s
sans_est_sub labels 219 exact 219 f1g 0.5849 spans 20 0.9s
sans_predicat_vu labels 220 exact 220 f1g 0.588 spans 19 0.8s
sans_ee labels 220 exact 220 f1g 0.588 spans 19 0.8s
sans_gp_det labels 219 exact 219 f1g 0.5866 spans 20 0.7s
v9_attendu labels 219 exact 219 f1g 0.5866 spans 20 0.8s
sans_sujets labels 214 exact 214 f1g 0.5833 spans 25 0.8s
sans_pron_sujets labels 214 exact 214 f1g 0.5808 spans 25 0.9s
{
 "controles": {
  "permutation": {
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,json,importlib.util,pathlib\nsys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\n# dirty tree measure\nimport tools.bloc_linguistique as bl\nr=eg.evaluer_bloc('h',bl.Heuristique(),eg.charger())\na=r['attachement']\nprint('dirty top1', … [248 caractères tronqués]`

  ```
dirty top1 221 exact 221 labels 221 topk 220 f1 0.5843 tete 0.733
  ```

### 🤖 Assistant

⏵ Characterizing the uncommitted working-tree change

- **bash** `{"command": "python3 - <<'PY'\nimport sys,json,collections\nsys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nimport tools.bloc_linguistique as bl\nfrom tools.tests.linguistique.gold_split import dev,test\nph=eg.charger(); ge=eg.charger_gele()\nh=bl.Heuristique()\ndef att(p … [884 caractères tronqués]`

  ```
dirty vivant {'labels': 221, 'exact': 221, 'topk': 220, 'topk_taux': 0.9205}
dirty dev {'labels': 152, 'exact': 152} test {'labels': 69, 'exact': 69}
dirty spans 18 Counter({'REL': 9, 'SUB': 5, 'GP': 4})
('g017', 'SUB', 'that she would come')
('r035', 'REL', 'she talks about')
('r241', 'REL', 'when we left')
('r255', 'REL', "que j'ai achetée")
('r264', 'SUB', "qu'il vient demain")
('s010', 'REL', 'qui nage')
('s027', 'GP', 'il')
('s035', 'REL', 'qui ferme')
('s044', 'SUB', 'que ils crie')
('s061', 'REL', 'qui saute')
('s065', 'REL', 'qui commence')
('s112', 'SUB', 'que Lucas ferme')
('s114', 'SUB', 'que les avocat compte')
('s125', 'REL', 'qui compte')
('s141', 'REL', 'qui trouve')
('s146', 'GP', 'les jardin')
('s148', 'GP', 'les ancienne lettre')
('s160', 'GP', 'le renard')
  ```

- **bash** `{"command": "PYTHONPATH=. python3 -m tools.pensee.autotest > /tmp/audit_v10/autotest_dirty.log 2>&1; echo \"exit=$?\"", "description": "Run gates on dirty working tree", "run_in_background": true, "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
started background job bash-2525
  ```

### 🤖 Assistant

⏵ Re-validating official counters with the pinned module

- **bash** `{"command": "python3 - <<'PY'\nimport sys, importlib.util, pathlib, json\nsys.path.insert(0,'.')\nimport tools.tests.linguistique.evaluer_gold as eg\nfrom tools.tests.linguistique.gold_split import dev, test\nspec=importlib.util.spec_from_file_location('pinned_v10','/tmp/audit_v10/mods/v10.py')\nm=i … [785 caractères tronqués]`

  ```
vivant labels 220 exact 220 topk 219 f1 0.5836 tete 0.7332
gele labels 220 exact 220 topk 219 f1 0.588 tete 0.7388
dev labels 152 exact 152 couverture 0.9325
test labels 68 exact 68 couverture 0.8947
  ```

### 🤖 Assistant

⏵ Checking gates on the dirty tree

- **job_output** `{"job_id": "bash-2525", "wait": true, "timeout_ms": 120000}`

  ```
(no new output)
[status: running]
  ```

### 🤖 Assistant

⏵ Documenting the uncommitted working-tree change

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-audit-v10.md'\ns=open(p).read()\nanchor=\"\"\"## 2. Rejeu des valeurs v10 — 2 écarts\"\"\"\nnew=\"\"\"### 1 bis. Note d'arbre de travail (importante)\n\nAu début de l'audit, `tools/bloc_linguistique.py` était **byte-identique** à `710ec7f9`\n(sha256  … [2249 caractères tronqués]`

  ```
report updated
  ```

### 🤖 Assistant

⏵ Adding the working-tree note to JSON

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='reports/pensee-audit-v10.json'\nd=json.load(open(p))\nd['methode']['note_arbre_de_travail']={\n 'etat_initial':'tools/bloc_linguistique.py byte-identique à 710ec7f9 (sha256 308f6eeda95f69ea...) au début de l\\'audit',\n 'changement_observe':'modificatio … [1306 caractères tronqués]`

  ```
ok
JSON OK
  ```

### 🤖 Assistant

⏵ Checking the dirty-tree gate run

- **job_output** `{"job_id": "bash-2525", "timeout_ms": 60000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

### 🤖 Assistant

⏵ Checking whether the working tree changed again

- **bash** `{"command": "git status --short tools/bloc_linguistique.py tools/pensee/autotest.py; stat -c '%y %n' tools/bloc_linguistique.py; python3 - <<'PY'\nimport hashlib,subprocess,pathlib\ncur=pathlib.Path('tools/bloc_linguistique.py').read_bytes()\ncom=subprocess.run(['git','show','710ec7f9:tools/bloc_lin … [201 caractères tronqués]`

  ```
M tools/bloc_linguistique.py
 M tools/pensee/autotest.py
2026-11-06 00:15:37.544747590 -0500 tools/bloc_linguistique.py
byte-identique commit: False
  ```

### 👤 Utilisateur

background job bash-2525 (bash: PYTHONPATH=. python3 -m tools.pensee.autotest > /tmp/audit_v10/autotest_dirty.log 2>&1; echo "exit=$?") finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Reading the dirty-tree gate results

- **bash** `{"command": "tail -8 /tmp/audit_v10/autotest_dirty.log; echo '--- failures ---'; grep -c '❌' /tmp/audit_v10/autotest_dirty.log; grep -c '✅' /tmp/audit_v10/autotest_dirty.log; echo '--- T161/T162/T163/T166 ---'; grep -E 'T161|T162|T163|T166|T173|T180' /tmp/audit_v10/autotest_dirty.log", "description" … [93 caractères tronqués]`

  ```
✅ T174 convention documentée convention : ['GN', 'GP', 'GV', 'REL', 'SUB'] documentée
  ✅ T175 audit attachement audit : 14/14, écarts 0
  ✅ T176 segment précédent segment précédent : s052 ouvre, s012 écoute
  ✅ T177 candidats têtes   candidats têtes : 220/221 (0.9955)
  ✅ T178 cache chunker     cache : 1 chunking chunker, 1 défaut (1+2S avant)
  ✅ T179 multi-cibles      multi-cibles : exact 221/221, exact_any 221/221
  ✅ T180 par langue        langues : fr 136/136, en 85/85 (85/88 labels)
  183/183 portes tenues
--- failures ---
0
183
--- T161/T162/T163/T166 ---
  ✅ T161 cible proximité   proximité : top1 221/239, exact 221/239, tête 221/145
  ✅ T162 candidats verbes  candidats : top-k 220/239 (0.9205), tête 220/221
  ✅ T163 échecs attachement échecs : 18 de span, 1 de cible (33 avant les correctifs)
  ✅ T166 spans perdus      spans : 9 REL, 5 SUB, 4 GP
  ✅ T173 top-k strict      top-k : 220 sous-chaîne, 220 exacts (0.9955)
  ✅ T180 par langue        langues : fr 136/136, en 85/85 (85/88 labels)
  ```

- **bash** `{"command": "git diff --stat tools/pensee/autotest.py; git diff tools/pensee/autotest.py | head -60", "description": "Inspect dirty autotest changes", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
(no output)
  ```

### 🤖 Assistant

⏵ Checking staged vs unstaged state of the in-flight change

- **bash** `{"command": "git status --short tools/bloc_linguistique.py tools/pensee/autotest.py; echo '--- cached stat ---'; git diff --cached --stat tools/pensee/autotest.py tools/bloc_linguistique.py; echo '--- unstaged stat ---'; git diff --stat tools/pensee/autotest.py tools/bloc_linguistique.py", "descript … [115 caractères tronqués]`

  ```
M  tools/bloc_linguistique.py
M  tools/pensee/autotest.py
--- cached stat ---
 tools/bloc_linguistique.py | 11 ++++-------
 tools/pensee/autotest.py   | 34 +++++++++++++++++-----------------
 2 files changed, 21 insertions(+), 24 deletions(-)
--- unstaged stat ---
  ```

### 🤖 Assistant

⏵ Documenting that the in-flight variant is staged and self-consistent

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-audit-v10.md'\ns=open(p).read()\nold=\"\"\"`g017`, ajoute `r241`). Ce changement n'est **pas** de cet audit et n'est **pas** évalué ici ;\nson auteur doit le vérifier et le committer. Les **183/183 portes** ont été obtenues quand\nl'arbre était encor … [1191 caractères tronqués]`

  ```
md ok
json ok
  ```

### 🤖 Assistant

⏵ Clarifying that only the audit wrote nothing else

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-audit-v10.md'\ns=open(p).read()\ns=s.replace(\"**Aucun fichier existant n'a été modifié ; aucun commit n'a été fait.**\",\"**Aucun fichier existant n'a été modifié par cet audit ; aucun commit n'a été fait.**\")\nopen(p,'w').write(s)\nprint('ok')\nPY … [155 caractères tronqués]`

  ```
ok

- [`rapport-audit-v10.md`](rapport-audit-v10.md) — ce rapport.
- [`pensee-audit-v10.json`](pensee-audit-v10.json) — les chiffres, les ids et les contrôles.

**Aucun fichier existant n'a été modifié par cet audit ; aucun commit n'a été fait.** Les scripts de mesure
vivaient dans `/tmp/audit_v10/` et ne sont pas livrés.
  ```

### 🤖 Assistant

⏵ Confirming the final measurement file is commit-anchored

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/audit_v10/resultats.json'))\nv=d['variantes']['v10']\nprint('v10',v['labels'],v['exact'],v['f1_gele'],v['topk'],v['spans_total'],v['spans'],v['test'])\nprint('v9',d['variantes']['v9']['labels'],d['variantes']['v9']['f1_gele'],d['vari … [246 caractères tronqués]`

  ```
v10 220 220 0.588 219 19 {'GP': 4, 'REL': 9, 'SUB': 6} {'cibles': 76, 'labels': 68, 'exact': 68, 'couverture': 0.8947, 'f1': 0.589, 'tete': 0.7337, 'par_langue': {'fr': {'cibles': 50, 'labels': 43, 'exact': 43, 'topk': 42}, 'en': {'cibles': 26, 'labels': 25, 'exact': 25, 'topk': 25}}}
v9 219 0.5866 20
controles 220 1.997
  ```

### 🤖 Assistant

⏵ Verifying gate docstrings at the audited commit

- **bash** `{"command": "git show 710ec7f9:tools/pensee/autotest.py > /tmp/audit_v10/autotest_710.py; python3 - <<'PY'\nimport ast,re\nsrc=open('/tmp/audit_v10/autotest_710.py').read()\nt=ast.parse(src)\nfor node in t.body:\n    if isinstance(node,ast.FunctionDef):\n        m=re.match(r't(\\d+)_',node.name)\n   … [277 caractères tronqués]`

  ```
t153_attachement             L'attachement sur le gold 612 (239 cibles) : top1 0,887, exact 0,887, couverture 0,887.
t154_cibles                  Les cibles de l'attachement : 1624 segments sans cible sur 1863.
t155_cibles_500              Les 500 premiers segments : 294 GN, 206 GV.
t156_relation                La relation GN → GV : 257/546 (0,4707).
t157_roles                   Les GN sans rôle : 231, dont 151 avant le GV et 46 après.
t158_passifs                 Les passifs : 5/5 faux par la position seule.
t159_passifs_corriges        Le correctif des passifs : _role_gp rend agent, le generateur S court-circuite.
t160_passifs_sans_par        Les passifs sans par : le chunker 3/3 patient.
t161_cible_proximite         La cible par proximité : 212/212 avec la règle du précédent.
t162_candidats_verbes        Les candidats verbes : le top-k atteint 211/239 (0,8828) après le correctif du précédent.
t163_echecs_attachement      Les échecs de l'attachement : 27 de span, 1 de cible.
t164_verbe_gv                Le verbe du GV-phrase : le POS VERB, pas le dernier mot.
t165_lexique_verbal          Le lexique verbal arbitre le POS : « talks » est un verbe, « brother » n'en est pas un.
t166_
… [1551 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Final consistency scan of the outputs

- **bash** `{"command": "grep -n \"221\\|dirty\\|arbre courant\\|00:15\" reports/rapport-audit-v10.md; echo '--- json ---'; grep -n \"221\\|arbre_courant\\|00:15\" reports/pensee-audit-v10.json | head -20", "description": "Locate working-tree mentions", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrine … [3 caractères tronqués]`

  ```
49:`2026-11-06 00:15:37`) : deux changements dans `_syntagmes_simple` — la condition R2
55:0,5880, 19 spans, test 68/68** ; l'arbre courant, lui, donne **221/221, F1 0,5843, top-k 220,
368:  `2026-11-06 00:15:37`, deux changements R2/adverbe) : les mesures sont faites sur la copie
369:  du **commit** `710ec7f9`, pas sur l'arbre courant. La reproductibilité sur l'arbre courant
--- json ---
45:   "changement_observe": "modification non commitée pendant la rédaction (mtime 2026-11-06 00:15:37) : condition R2 (est_sub(n) or n in SUBORDONNANTS or precedent == \"GV\") et suppression de la garde d'adverbe final",
46:   "ancrage": "toutes les mesures utilisent git show 710ec7f9:tools/bloc_linguistique.py, copié dans /tmp/audit_v10/mods ; le fichier de travail (staged, 221/221) n'est pas utilisé",
47:   "arbre_courant": {
48:    "labels": 221,
49:    "exact": 221,
61:    "portes": "183/183 avec les assertions autotest ajustées pour 221/221 et 18 spans"
1232:  "Le fichier tools/bloc_linguistique.py a été modifié sans commit pendant l'audit (mtime 2026-11-06 00:15:37) : les mesures sont ancrées sur git show 710ec7f9, pas sur l'arbre courant ; la reproductibilité sur l'arbre courant n'est pas 
… [64 caractères tronqués]
  ```

- **bash** `{"command": "python3 -m json.tool reports/pensee-audit-v10.json >/dev/null && echo 'JSON OK'; python3 - <<'PY'\nimport re,pathlib\np=pathlib.Path('reports/rapport-audit-v10.md'); s=p.read_text()\nfor l in sorted(set(re.findall(r'\\]\\(([^)]+)\\)',s))):\n    if l.startswith('http'): continue\n    pri … [166 caractères tronqués]`

  ```
JSON OK
OK ../tools/bloc_linguistique.py
OK pensee-audit-v10.json
OK rapport-audit-r1r3.md
OK rapport-audit-v10.md
OK rapport-pensee-v10.md
  ```

### 🤖 Assistant

⏵ Checking gate log timing against the in-flight edit

- **bash** `{"command": "stat -c '%y %n' /tmp/audit_v10/autotest.log /tmp/audit_v10/autotest_dirty.log /tmp/audit_v10/harness_pinned.log; head -3 /tmp/audit_v10/autotest.log; tail -1 /tmp/audit_v10/autotest.log", "description": "Check gate log timing", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet … [2 caractères tronqués]`

  ```
2026-11-05 23:38:21.095722471 -0500 /tmp/audit_v10/autotest.log
2026-11-06 00:28:34.264845723 -0500 /tmp/audit_v10/autotest_dirty.log
2026-11-06 00:22:42.573938810 -0500 /tmp/audit_v10/harness_pinned.log
  ✅ T0 store canonique     aller-retour exact, empreinte stable sous permutation
  ✅ T1 rejeu               rejeu identique sur 94 événements ; deux exécutions égales
  ✅ T1 graine              deux graines divergent au premier pas différent
  183/183 portes tenues
  ```

### 🤖 Assistant

⏵ Qualifying the gate verdict with stale docstrings

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-audit-v10.md'\ns=open(p).read()\ns=s.replace(\"> **Verdict** : chiffres ✅ (deux écarts), règles ❌, portes ✅.\",\"> **Verdict** : chiffres ✅ (deux écarts), règles ❌, portes ✅ (183/183, 11 docstrings périmées).\")\nopen(p,'w').write(s)\nprint('md ok')\ … [359 caractères tronqués]`

  ```
md ok
json ok
  ```

### 🤖 Assistant

⏵ Final repo status check

- **bash** `{"command": "git status --short reports/ | grep -E 'audit-v10|rapport-audit-v10|pensee-audit-v10'; echo '--- all new reports files ---'; git status --short reports/ | grep '^??'; echo '--- our files ---'; ls -l reports/rapport-audit-v10.md reports/pensee-audit-v10.json", "description": "Confirm only … [85 caractères tronqués]`

  ```
MM reports/pensee-audit-v10.json
MM reports/rapport-audit-v10.md
--- all new reports files ---
?? reports/rapport-s-paragraphes.md
--- our files ---
-rw-r--r--. 1 stephane stephane 29330  6 nov 00:33 reports/pensee-audit-v10.json
-rw-------. 1 stephane stephane 25957  6 nov 00:33 reports/rapport-audit-v10.md
  ```

### 🤖 Assistant

⏵ Investigating why the new files are now staged

- **bash** `{"command": "git log --oneline -3; echo '--- status ours ---'; git status --short reports/rapport-audit-v10.md reports/pensee-audit-v10.json; echo '--- cached diff stat ours ---'; git diff --cached --stat reports/rapport-audit-v10.md reports/pensee-audit-v10.json; echo '--- index hash ---'; git ls-f … [298 caractères tronqués]`

  ```
653a7981 B13 — LES DEUX DERNIÈRES RÉGRESSIONS (s037, r303) : EXACT 221/221 (1,0000), COUVERTURE 0,9247, 18 SPANS ; AUDIT V10 INTÉGRÉ, V10 CORRIGÉE ; 183/183
68a8717b JOURNAL — LE 06/11 AU FORMAT DE L'INDEX (EN-TÊTE, LIENS, BLOC NOTES)
41cae3e5 JOURNAL — LE 06/11 S'OUVRE SUR LA NUIT DU DÉCOUPAGE : 220/220, COUVERTURE 0,9205, 19 SPANS
--- status ours ---
MM reports/pensee-audit-v10.json
MM reports/rapport-audit-v10.md
--- cached diff stat ours ---
 reports/pensee-audit-v10.json | 8 +++++---
 reports/rapport-audit-v10.md  | 8 +++++---
 2 files changed, 10 insertions(+), 6 deletions(-)
--- index hash ---
100644 5b802258acd586d692519689ceee2b5548849499 0	reports/pensee-audit-v10.json
100644 dd6b1e81df627d5c4f483620fa47ca703b1515e3 0	reports/rapport-audit-v10.md
--- worktree hash ---
68a575d43d961c5dc37e63fc5be39ea621ec065c
da316c7409bb4197c8b144a12bf994b4964b7af0
  ```

### 🤖 Assistant

⏵ A concurrent commit appeared; comparing committed vs latest audit files

- **bash** `{"command": "git log -1 --format='%h %an <%ae> %ad%n%s' --date=iso 653a7981; echo '--- files in commit ---'; git show --stat --oneline 653a7981 | head -30; echo '--- HEAD version vs worktree (stat) ---'; git diff --stat HEAD -- reports/rapport-audit-v10.md reports/pensee-audit-v10.json; echo '--- wo … [229 caractères tronqués]`

  ```
653a7981 Stéphane <stephane@localhost> 2026-11-06 00:28:42 -0500
B13 — LES DEUX DERNIÈRES RÉGRESSIONS (s037, r303) : EXACT 221/221 (1,0000), COUVERTURE 0,9247, 18 SPANS ; AUDIT V10 INTÉGRÉ, V10 CORRIGÉE ; 183/183
--- files in commit ---
653a7981 B13 — LES DEUX DERNIÈRES RÉGRESSIONS (s037, r303) : EXACT 221/221 (1,0000), COUVERTURE 0,9247, 18 SPANS ; AUDIT V10 INTÉGRÉ, V10 CORRIGÉE ; 183/183
 docs/pilotage/en-cours.md                          |    4 +-
 journal/2026-11-06/README.md                       |   11 +-
 journal/2026-11-06/distribue.md                    |    9 +-
 journal/README.md                                  |    8 +-
 .../3fb87dc7-7d24-42e2-a68e-e37e2734b755/digest.md |  297 +++++
 .../rapport.md                                     |   22 +-
 journal/sessions/MANIFEST.md                       |    8 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  112 ++
 .../rapport.md                                     |   19 +-
 .../ea169cb1-75d7-43fa-b69d-5e2a210f6c38/digest.md |  743 ++++++++++++
 .../rapport.md                                     |   20 +-
 reports/README.md                                  |    2 +-
 reports/pensee-audit-v10.json                   
… [797 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Comparing committed audit version with current worktree

- **bash** `{"command": "wc -l reports/rapport-audit-v10.md; echo 'HEAD:'; git show HEAD:reports/rapport-audit-v10.md | wc -l; echo '--- diff HEAD vs worktree (report) ---'; git diff HEAD -- reports/rapport-audit-v10.md | head -120", "description": "Diff committed vs worktree report", "workdir": "/home/stephane … [35 caractères tronqués]`

  ```
378 reports/rapport-audit-v10.md
HEAD:
376
--- diff HEAD vs worktree (report) ---
diff --git a/reports/rapport-audit-v10.md b/reports/rapport-audit-v10.md
index fe47566d..68a575d4 100644
--- a/reports/rapport-audit-v10.md
+++ b/reports/rapport-audit-v10.md
@@ -2,7 +2,7 @@
 
 > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
 > **Commit audité** : `710ec7f9` (parent `160d08ca`) · **Date** : 2026-11-05 ·
-> **Verdict** : chiffres ✅ (deux écarts), règles ❌, portes ✅.
+> **Verdict** : chiffres ✅ (deux écarts), règles ❌, portes ✅ (183/183, 11 docstrings périmées).
 > **Aucun fichier existant modifié ; aucun commit.** Sorties : ce rapport et
 > [`pensee-audit-v10.json`](pensee-audit-v10.json).
 
@@ -55,8 +55,10 @@ importé ; le fichier de travail n'est jamais utilisé. Les chiffres du commit s
 0,5880, 19 spans, test 68/68** ; l'arbre courant, lui, donne **221/221, F1 0,5843, top-k 220,
 18 spans (9 REL, 5 SUB, 4 GP), dev 152/152, test 69/69** (il répare `s037` et `r303`, perd
 `g017`, ajoute `r241`). Ce changement n'est **pas** de cet audit et n'est **pas** évalué ici ;
-son auteur doit le vérifier et le committer. Les **183/183 portes** ont été obtenue
… [833 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Updating the note: the concurrent change is now committed as v11

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-audit-v10.md'\ns=open(p).read()\nold=\"\"\"Au début de l'audit, `tools/bloc_linguistique.py` était **byte-identique** à `710ec7f9`\n(sha256 `308f6eed…`). Pendant la rédaction, le fichier a été **modifié sans commit** (mtime\n`2026-11-06 00:15:37`) :  … [3643 caractères tronqués]`

  ```
md ok
json ok
  ```

### 🤖 Assistant

⏵ Updating the limitation bullet for committed v11

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-audit-v10.md'\ns=open(p).read()\nold=\"\"\"- **Dépôt déjà modifié** : `journal/`, plusieurs `reports/` et le sous-module\n  `tools/structures` portaient des modifications non commitées antérieures à cet audit. Le\n  fichier `tools/bloc_linguistique.p … [1587 caractères tronqués]`

  ```
md ok
json ok
  ```

### 🤖 Assistant

⏵ Reviewing final note and limitation text

- **bash** `{"command": "sed -n '42,72p' reports/rapport-audit-v10.md; echo '...'; sed -n '360,385p' reports/rapport-audit-v10.md; echo '--- json note ---'; python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-v10.json'))\nprint(json.dumps(d['methode']['note_arbre_de_travail'],ensure_ascii=Fals … [156 caractères tronqués]`

  ```
L'invocation directe `python3 tools/pensee/autotest.py` échoue sur l'import relatif
  (`ImportError`) ; il faut `-m`.

### 1 bis. Note d'arbre de travail (importante)

Au début de l'audit, `tools/bloc_linguistique.py` était **byte-identique** à `710ec7f9`
(sha256 `308f6eed…`). Pendant la rédaction, le fichier a été **modifié sans commit** (mtime
`2026-11-06 00:15:37`) : deux changements dans `_syntagmes_simple` — la condition R2
(`stype = "SUB" if (est_sub(n) or n in SUBORDONNANTS or precedent == "GV")`, qui répare
`s037`) et la **suppression de la garde d'adverbe final** (qui répare `r303` mais perd
`g017`). Ce changement a ensuite été **committé** dans `653a7981` (2026-11-06 00:28:42,
« … AUDIT V10 INTÉGRÉ, V10 CORRIGÉE »), avec `reports/pensee-v11.json` et
`rapport-pensee-v11.md` ; c'est la **v11**, pas la v10. **Toutes les mesures de ce rapport
sont ancrées sur `710ec7f9`** : le module est lu par
`git show 710ec7f9:tools/bloc_linguistique.py`, copié dans `/tmp/audit_v10/mods` et importé ;
le fichier de travail n'est jamais utilisé. Les chiffres du commit sont **220/220, 0,5880,
19 spans, test 68/68** ; l'arbre courant (v11) donne **221/221, F1 0,5843, top-k 220, 18 spans
(9 REL
… [3903 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Scoping the no-commit statement to this audit

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-audit-v10.md'\ns=open(p).read()\ns=s.replace(\"**Aucun fichier existant n'a été modifié par cet audit ; aucun commit n'a été fait.**\",\"**Aucun fichier existant n'a été modifié par cet audit ; aucun commit n'a été fait par cet audit.**\")\nopen(p,'w … [709 caractères tronqués]`

  ```
ok
json ok
JSON OK
  ```

### 🤖 Assistant

⏵ Final check of method and closing line

- **bash** `{"command": "tail -5 reports/rapport-audit-v10.md; echo '---'; python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-v10.json'))\nprint(json.dumps(d['methode'],ensure_ascii=False,indent=1)[:2000])\nPY", "description": "Review final method block", "workdir": "/home/stephane/Data13TB/s … [24 caractères tronqués]`

  ```
- [`rapport-audit-v10.md`](rapport-audit-v10.md) — ce rapport.
- [`pensee-audit-v10.json`](pensee-audit-v10.json) — les chiffres, les ids et les contrôles.

**Aucun fichier existant n'a été modifié par cet audit ; aucun commit n'a été fait par cet audit.** Les scripts de mesure
vivaient dans `/tmp/audit_v10/` et ne sont pas livrés.
---
{
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
  "source": "evaluer_gold.charger_gele",
  "phrases": 602,
  "cibles": 239,
  "note": "les 10 phrases ajoutées après le gel n'ont aucune cible"
 },
 "dev_test": {
  "split": "crc32(id) % 3 == 0 -> test",
  "dev": {
   "phrases": 422,
   "cibles": 163
  },
  "test": {
   "phrases": 190,
   "cibles": 76
  }
 },
 "mesure": "evaluer_gold.evaluer_bloc pour les valeurs officielles ; harnais local pour les ensembles d'identifiants, les ablations et les contrôles.",
 "ablations": "copies du module dans /tmp/audit_v10/mods, une seule modification réintroduite par variante ; aucun patch du dépôt.",
 "fidelite": "v10 sans garde GP sans -ée = module v9 (219, 0,5866, 20 spans, 152/15
… [1138 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Wrapping the closing line

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-audit-v10.md'\ns=open(p).read()\ns=s.replace(\"**Aucun fichier existant n'a été modifié par cet audit ; aucun commit n'a été fait par cet audit.** Les scripts de mesure\\nvivaient dans `/tmp/audit_v10/` et ne sont pas livrés.\",\"**Aucun fichier exis … [338 caractères tronqués]`

  ```
ok
- [`pensee-audit-v10.json`](pensee-audit-v10.json) — les chiffres, les ids et les contrôles.

**Aucun fichier existant n'a été modifié par cet audit ; aucun commit n'a été fait par cet
audit.** Les scripts de mesure vivaient dans `/tmp/audit_v10/` et ne sont pas livrés.
  ```

### 🤖 Assistant

⏵ Checking the concurrent correction to the v10 fiche

- **bash** `{"command": "git show 653a7981 -- reports/rapport-pensee-v10.md; echo '--- current fiche head ---'; head -20 reports/rapport-pensee-v10.md", "description": "Inspect v10 fiche correction in concurrent commit", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
commit 653a79817f4bccb9bb354e3687e8bba06b454995
Author: Stéphane <stephane@localhost>
Date:   Fri Nov 6 00:28:42 2026 -0500

    B13 — LES DEUX DERNIÈRES RÉGRESSIONS (s037, r303) : EXACT 221/221 (1,0000), COUVERTURE 0,9247, 18 SPANS ; AUDIT V10 INTÉGRÉ, V10 CORRIGÉE ; 183/183

diff --git a/reports/rapport-pensee-v10.md b/reports/rapport-pensee-v10.md
index 1e7e4f4b..1b1f036a 100644
--- a/reports/rapport-pensee-v10.md
+++ b/reports/rapport-pensee-v10.md
@@ -1,13 +1,14 @@
 # B13 — 220/220 (1,0000), couverture 0,9205 : le féminin `-ée` et la garde déterminant du GP
 
 > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
-> **État courant** · **Verdict** : ✅
-> **183/183 portes** : deux corrections générales — le **féminin `-ée`** des participes
-> (`achetée` → `acheter`) et la **garde déterminant** du GP (A17 R3b : un « verbe » précédé d'un
-> déterminant est un nom, `for the bus`) — portent l'attachement à **220/220 (1,0000)** sur les
-> **220 labels** prédits (sur 239), **couverture 0,9205**, **F1 0,5880** (union ; S 0,5014,
-> chunker 0,6203), tête **0,7388** ; **fr 134/134**, **en 86/86** ; **19 spans** restants
-> (9 REL, 6 SUB, 4 GP). **dev 152/
… [2239 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Noting the v10 fiche was also corrected in the concurrent commit

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-audit-v10.md'\ns=open(p).read()\nold=\"\"\"v11 passe aussi **183/183** avec ses assertions ajustées. Les versions de ce rapport et du\nJSON présentes dans `653a7981` sont une **version antérieure** ; les versions courantes du\nworktree sont les versi … [1120 caractères tronqués]`

  ```
md ok
json ok
  ```

### 🤖 Assistant

⏵ Verifying the final note paragraphs

- **bash** `{"command": "python3 -m json.tool reports/pensee-audit-v10.json >/dev/null && echo 'JSON OK'; sed -n '48,75p' reports/rapport-audit-v10.md; echo '---'; python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-v10.json'))\nprint(d['methode']['note_arbre_de_travail']['fiche_v10'])\nPY", " … [115 caractères tronqués]`

  ```
JSON OK
(sha256 `308f6eed…`). Pendant la rédaction, le fichier a été **modifié sans commit** (mtime
`2026-11-06 00:15:37`) : deux changements dans `_syntagmes_simple` — la condition R2
(`stype = "SUB" if (est_sub(n) or n in SUBORDONNANTS or precedent == "GV")`, qui répare
`s037`) et la **suppression de la garde d'adverbe final** (qui répare `r303` mais perd
`g017`). Ce changement a ensuite été **committé** dans `653a7981` (2026-11-06 00:28:42,
« … AUDIT V10 INTÉGRÉ, V10 CORRIGÉE »), avec `reports/pensee-v11.json` et
`rapport-pensee-v11.md` ; c'est la **v11**, pas la v10. **Toutes les mesures de ce rapport
sont ancrées sur `710ec7f9`** : le module est lu par
`git show 710ec7f9:tools/bloc_linguistique.py`, copié dans `/tmp/audit_v10/mods` et importé ;
le fichier de travail n'est jamais utilisé. Les chiffres du commit sont **220/220, 0,5880,
19 spans, test 68/68** ; l'arbre courant (v11) donne **221/221, F1 0,5843, top-k 220, 18 spans
(9 REL, 5 SUB, 4 GP), dev 152/152, test 69/69** (il répare `s037` et `r303`, perd `g017`,
ajoute `r241`). Ce changement n'est **pas** de cet audit et n'est **pas** évalué ici. Les
**183/183 portes** de ce rapport ont été obtenues quand l'arbre était enco
… [872 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Sending the audit summary to the parent

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Audit v10 terminé — ancré sur le commit 710ec7f9. Fichiers livrés : reports/rapport-audit-v10.md et reports/pensee-audit-v10.json (versions finales dans le worktree ; je n'ai rien commité ni modifié d'existant).\n\nVALEURS (rejouées su … [2836 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

### 🤖 Assistant

⏵ Clôture de l'audit et résumé final

Audit terminé. Deux fichiers neufs écrits :

- [`reports/rapport-audit-v10.md`](reports/rapport-audit-v10.md)
- [`reports/pensee-audit-v10.json`](reports/pensee-audit-v10.json)

Aucun fichier existant modifié par moi, aucun commit de ma part.

## Valeurs rejouées (commit `710ec7f9`)

| grandeur | fiche | vivant 612 | gelé 602 |
|---|---:|---:|---:|
| labels / exact | 220 / 220 (1,0000) | **220 / 220** | **220 / 220** |
| couverture | 0,9205 | **0,9205** | **0,9205** |
| F1 union | 0,5880 | 0,5836 | **0,5880** |
| S / chunker | 0,5014 / 0,6203 | 0,4957 / 0,6163 | **0,5014 / 0,6203** |
| tête | 0,7388 | 0,7332 | **0,7388** |
| fr / en | 134/134, 86/86 | **idem** | **idem** |
| spans | 19 (9 REL, 6 SUB, 4 GP) | **19** | **19** |
| top-k | 219 (0,9163) | **219** | **219** |

**Écarts**
1. Le F1 « avant » **0,5822** est la valeur du **vivant 612**, pas du gelé ; le **gelé v9 vaut 0,5866**. Le gain v9→v10 est **+0,0014**, pas +0,0058.
2. Le **test courant v10 est 68/68** (0,8947), pas 67/67 (le 67/67 est la v9).

## Règles

Le commit `710ec7f9` ne modifie, dans le bloc, que la **garde DET du GP** : **+1 exact (`r153`, test)**, 0 perte. Le **`-ée` est antérieur** (`a408a909`, déjà dans v8/v9) et **totalement inerte** : 0 différence d'annotation sur 612 phrases ; `r255` reste absent car `acheter` n'est pas dans `VERBES_CONNUS`.

## Ablations (base 220 ; F1 gelé)

| ablation | exact | Δ | gains / pertes | F1 |
|---|---:|---:|---|---:|
| garde PRON retirée | 203 | **−17** | 17 gains, 0 perte | 0,5718 (−0,0162) |
| expansion SUJETS retirée | 214 | **−6** | 6 gains (r273 s032 s069 s072 s115 s135) | 0,5833 |
| PRON + SUJETS retirées | 214 | **−6** | mêmes 6 gains ; garde inerte sans expansion | 0,5808 |
| `est_sub` retiré | 219 | **−1** | r280 | 0,5849 |
| `predicat_vu` retiré | 220 | **0** | gagne g017, perd r303 | 0,5880 |
| `-ée` retiré | 220 | **0** | 0 / 0 | 0,5880 |
| garde DET GP retirée | 219 | **−1** | r153 | 0,5866 |

**Les 19 spans** = **17 résiduels A17 + `s037` + `r303`**. La fiche « 17 inatteignables + r255 + r264 » double compte r255/r264 et omet s037/r303. `r303` est la perte cachée de `predicat_vu` (net 0 avec g017) ; `s037` est la 7e régression v8, toujours ouverte.

## dev/test

| moitié | v8 | v9 | **v10** |
|---|---:|---:|---:|
| dev | 148/148 | 152/152 | **152/152** (0,9325) |
| test | 64/64 | 67/67 | **68/68** (0,8947) |

Le +1 test est `r153` ; le `-ée` n'ajoute rien.

## Contrôles et portes

- Permutation globale des cibles : **1,997/220 = 0,908 %** (2000 tirages, p=0).
- Candidat aléatoire top-1 : **42,14 %** (p=0).
- Permutation des listes de candidats top-k : **0,99 %** (égalité) / **1,17 %** (sous-chaîne), p=0.
- Les 19 spans ont été vérifiés un par un.
- **183/183 portes**, exit 0 — mais **11 docstrings périmées** (T153, T161, T162, T163, T166, T167, T172, T173, T177, T179, T180) contredisent leur assertion.

## Note de concurrence

Un commit **`653a7981` (v11)** est apparu pendant l'audit : il intègre une version antérieure de mon rapport, corrige la fiche v10 et passe à **221/221, 18 spans, test 69/69**. Mes mesures restent **ancrées sur `710ec7f9`** via `git show` ; le worktree contient mes versions finales, le commit une version antérieure. Je n'ai rien commité.

