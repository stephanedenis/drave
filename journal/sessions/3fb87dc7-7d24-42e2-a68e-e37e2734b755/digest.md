# Session DSH — relecture

- identifiant : `3fb87dc7-7d24-42e2-a68e-e37e2734b755`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 23:24:20
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **re-mesurer dev/test sur l'état v10** (commit `710ec7f9`) et éprouver la robustesse du split.

Contexte : `tools/tests/linguistique/gold_split.py` (`dev`, `test`, `compter`), `evaluer_gold.py` (`charger`, `evaluer_bloc`), `bloc_linguistique.py`. Les valeurs publiées 152/152 (dev) et 67/67 (test) datent d'avant les deux dernières corrections (`-ée`, garde DET du GP).

À faire :
1. Re-mesure dev et test au commit courant : exact/labels, F1, tête, couverture, par langue (fr/en) et par type (REL/SUB/GP).
2. Vérifie l'**équilibre** du split (sources, langues, types) et signale les catégories absentes.
3. Éprouve la **stabilité** : trois découpages (`crc32(id)%3 == 0/1/2`) — donne les écarts.
4. Compare à la fiche `reports/rapport-dev-test-v7.md` (dev 133/134, test 62/62) et à l'audit `rapport-audit-r1r3.md` (dev 148/148, test 64/64).
5. Écris **uniquement** deux fichiers neufs : `reports/rapport-dev-test-v10.md` et `reports/pensee-dev-test-v10.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé : dev, test, les trois splits, l'écart.
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

⏵ Cartographie du dépôt et des outils de mesure gold

I'll start by orienting myself in the repo: current branch/commit, the tooling, and the reports to compare against.

- **bash** `{"command": "git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet rev-parse --abbrev-ref HEAD; git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet rev-parse HEAD; git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet status --porcelain | head -30", "description": "Show branch, HEAD and status" … [1 caractères tronqués]`

  ```
s/v7
710ec7f982ea3a85a3ca2cb8afc8e3390a129c9c
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
D  journ
… [463 caractères tronqués]
  ```

- **bash** `{"command": "ls /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/ 2>/dev/null; echo '---'; ls /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/ | head -60", "description": "List linguistique tools and reports"}`

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
---
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
a
… [445 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des outils gold (split, évaluation, bloc)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_split.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py"}`

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

⏵ Inspection du bloc linguistique et recherche des chiffres publiés

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -15 && echo '---' && git show --stat --oneline 710ec7f9 | head -40", "description": "Show recent commits and HEAD stat"}`

  ```
710ec7f9 B13 — LE FÉMININ -ÉE ET LA GARDE DÉTERMINANT DU GP : EXACT 220/220 (1,0000), COUVERTURE 0,9205, F1 0,5880, 19 SPANS ; 183/183
160d08ca B13 — LA GARDE PRON : EXACT 219/219 (1,0000), COUVERTURE 0,9163, F1 0,5822, DEV 152/152 ET TEST 67/67 ; AUDIT DE COHÉRENCE V8 INTÉGRÉ ; 183/183
d497324b B13 — TOP-K 211/239 (LE SITE D'APPEL prec = s), LA V8 RÉÉCRITE HONNÊTEMENT (+17 NET, 7 RÉGRESSIONS), AUDITS A17/A19 INTÉGRÉS ; 183/183
b551cf3b ÉTAT — LA LIGNE FAIT PASSE À L'ATTACHEMENT 212/212, COUVERTURE 0,887, 27 SPANS
7c43c75e JOURNAL — LE BILAN DE LA JOURNÉE : 137/145 → 212/212, COUVERTURE 0,6067 → 0,8870, F1 0,2862 → 0,5763
5c15ee91 JOURNAL — LES RÈGLES DE A17 : EXACT 212/212, COUVERTURE 0,887, 27 SPANS DONT 17 INATTEIGNABLES
f908d7b0 B13 — R1/R2/R3 : EXACT 212/212 (1,0000), COUVERTURE 0,887, F1 0,5763, FR 1,0 / EN 1,0 ; 27 SPANS DONT 17 INATTEIGNABLES ; 183/183
638ac8e8 PORTES — 13 DOCSTRINGS PÉRIMÉES MISES À JOUR (ATTACHEMENT 195/196, SPANS 43, TOP-K 166) ; 183/183
4ebeb683 B13 — L'AUDIT V7 INTÉGRÉ : DEUX RÉCITS CORRIGÉS (8 LABELS, +0,0118, EXEMPLE r204), VALEURS VÉRIFIÉES
9bf94feb FICHES — LA LISTE DE L'AUDIT APPLIQUÉE : PROSES V4/V5, SPLIT LEXICAL DE LA V2, F1 V6 SUR BASE CONSTAN
… [2034 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports | grep -iE 'dev.?test|audit.?r1r3|v10|v7' ; echo '---'; ls reports/*dev* 2>/dev/null", "description": "Find dev-test and audit reports"}`

  ```
pensee-audit-r1r3.json
pensee-audit-v7.json
pensee-coherence-fiches-v7.json
pensee-couverture-v7.json
pensee-dev-test-v7.json
pensee-spans-v7.json
pensee-v10.json
rapport-audit-r1r3.md
rapport-audit-v7.md
rapport-coherence-fiches-v7.md
rapport-dev-test-v7.md
rapport-pensee-couverture-v7.md
rapport-pensee-v10.md
rapport-spans-v7.md
---
reports/pensee-dev-test-v7.json
reports/pensee-phase-devine.json
reports/rapport-dev-test-v7.md
reports/rapport-pensee-phase-devine.md
  ```

### 🤖 Assistant

⏵ Lecture des fiches de référence (v7 et audit r1r3)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v7.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-audit-r1r3.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v7.md</path>
<type>file</type>
<content>
1: # B13 — dev/test en v7 : dev 133/134, test 62/62, le split tient sur trois découpages
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Commit mesuré** : `69bd865e` · **Verdict** : ✅
4: > Le gold 612 est re-coupé par `crc32(id) % 3 == 0` (test) : **dev 133/134 (0,9925)**, **test 62/62 (1,0)**
5: > — mais le test ne couvre que **62 des 76 cibles** (0,8158). En décalant le split (`%3==1`, `%3==2`),
6: > l'exact reste à **1 cas près** (étendue 0,0172), la couverture à **3 spans près** (14/13/16 des 43),
7: > la F1 à **2,4 points**. **Aucune catégorie demandée n'est absente** ; les écarts dev/test tiennent à
8: > **un échec unique (r102)** et à la **composition par type**, pas au split.
9: >
10: > **Dispositif** : [`gold_split.py`](../tools/tests/linguistique/gold_split.py) (`dev`, `test`, `compter`),
11: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`),
12: > [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (heuristique) ; JSON
13: > [`pensee-dev-test-v7.json`](pense
… [14651 caractères tronqués]
  ```


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
… [30110 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du JSON v7 et du diff des deux corrections

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -c 6000 reports/pensee-dev-test-v7.json", "description": "Inspect v7 JSON structure"}`

  ```
{
 "commit": "69bd865e",
 "valide_contre_evaluer_gold": true,
 "validation": {
  "exact": [
   195,
   195
  ],
  "labels": [
   196,
   196
  ],
  "cibles": [
   239,
   239
  ],
  "f1": [
   0.5555,
   0.5555
  ],
  "tete_f1": [
   0.7152,
   0.7152
  ],
  "pos": [
   0.7581,
   0.7581
  ],
  "couverture": [
   0.8201,
   0.8201
  ]
 },
 "analyses_secondes": 0.384,
 "equilibre_global": {
  "phrases": 612,
  "ids_uniques": 612,
  "sources": {
   "hand": 20,
   "reel": 432,
   "synthetique": 160
  },
  "langues": {
   "fr": 402,
   "en": 210
  },
  "types_tout": {
   "GN": 828,
   "GV": 712,
   "GP": 105,
   "SUB": 70,
   "REL": 74,
   "ADJ": 35,
   "ADV": 30,
   "PONCT": 9
  },
  "types_cibles": {
   "GP": 96,
   "SUB": 69,
   "REL": 74
  },
  "cibles_par_langue": {
   "fr": 151,
   "en": 88
  }
 },
 "splits": {
  "canonique": {
   "regle": "crc32(id)%3==0 -> test",
   "dev": {
    "phrases": 422,
    "tokens": 2185,
    "pos": {
     "exactitude": 0.7547,
     "ferme": 0.8952,
     "ouvert": 0.6201,
     "tokens": 2185
    },
    "syntagme": {
     "precision": 0.5953,
     "rappel": 0.5131,
     "f1": 0.5512,
     "tp": 665,
     "fp": 452,
     "fn": 631
    },
    "tete": {
  
… [4800 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 710ec7f9 -- tools/bloc_linguistique.py; echo '=== 160d08ca ==='; git show 160d08ca -- tools/bloc_linguistique.py", "description": "Show diffs of the two recent corrections"}`

  ```
commit 710ec7f982ea3a85a3ca2cb8afc8e3390a129c9c
Author: Stéphane <stephane@localhost>
Date:   Thu Nov 5 23:16:21 2026 -0500

    B13 — LE FÉMININ -ÉE ET LA GARDE DÉTERMINANT DU GP : EXACT 220/220 (1,0000), COUVERTURE 0,9205, F1 0,5880, 19 SPANS ; 183/183

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
=== 160d08ca ===
commit 160d08caf50135761fb997dc07d59a46c1d23fd7

… [4003 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du contenu exact du commit v10

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 710ec7f9 --stat --oneline | tail -25 && echo '=== cherche -ée dans le diff ===' && git show 710ec7f9 -G'ée|feminin|féminin' --oneline --stat", "description": "Locate the -ée correction in HEAD"}`

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
 
… [819 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"ée\\|feminin\\|f.minin\" tools/bloc_linguistique.py | head -20; echo '---'; sed -n '1,80p' reports/pensee-v10.json 2>/dev/null", "description": "Search -ée handling and v10 JSON"}`

  ```
10:  - `NeuronalLLM` : l'adaptateur réel, qui interroge un modèle local (`llama-cli`) et rend le
12:  - `NeuronalLLMPOS` : le **tagger** neuronal réel — un modèle local, une liste de tokens, des
13:    POS alignés par grammaire GBNF ; c'est l'implémentation qualifiée sur le gold ;
18:La sortie est une **annotation typée** — pas le corps de la RSN : chaque étiquette porte son
112:        """La confiance maximale par niveau — la couverture *déclarée*, pas une précision."""
164:    de test. Un profil est une donnée, pas un prompt : il se versionne et se rejoue.
413:bu cru sue pu voulu dû venue venu partie parti sorti mort née né ouvert offerte souffert couru
485:    for suf in ("er", "ir", "e", "es", "ent", "ait", "aient", "é", "ée", "és", "i", "u",
490:    # participes en -é/-és/-ée : `accroché` → `accrocher`
491:    for suf in ("ées", "ées", "ée", "és", "é"):
761:        """La tête nominale d'un span : le dernier mot, **élision séparée** (`L'homme` → `homme`)."""
816:        # mesurée (2026-11-05) et donne **le même** exact — elle n'est pas retenue.
1029:        # 2. mot + POS fermées / ouvertes
1231:        # 7. unités sémantiques : ouvertes + syntagmes ambiguës, dédupliquées
1315:
… [1191 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Première mesure canonique dev/test au commit courant

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0, 'tools')\nsys.path.insert(0, '.')\nfrom tools.tests.linguistique import evaluer_gold as eg\nfrom tools.tests.linguistique import gold_split as gs\nimport bloc_linguistique as bl … [647 caractères tronqués]`

  ```
phrases 612
dev 422 test 190
dev cibles 163 labels 152 exact 152 couv 0.9325 F1 0.5812 tete 0.733 POS 0.7547
   par_langue {'fr': {'cibles': 101, 'labels': 91, 'exact': 91, 'topk': 91, 'exact_taux_span': 1.0}, 'en': {'cibles': 62, 'labels': 61, 'exact': 61, 'topk': 61, 'exact_taux_span': 1.0}}
   tete_att {'cibles': 152, 'labels': 152, 'top1': 152, 'topk': 152, 'top1_taux': 1.0, 'topk_taux': 1.0, 'couverture': 1.0}
test cibles 76 labels 68 exact 68 couv 0.8947 F1 0.589 tete 0.7337 POS 0.7656
   par_langue {'fr': {'cibles': 50, 'labels': 43, 'exact': 43, 'topk': 42, 'exact_taux_span': 1.0}, 'en': {'cibles': 26, 'labels': 25, 'exact': 25, 'topk': 25, 'exact_taux_span': 1.0}}
   tete_att {'cibles': 68, 'labels': 68, 'top1': 68, 'topk': 67, 'top1_taux': 1.0, 'topk_taux': 0.9853, 'couverture': 1.0}
all cibles 239 labels 220 exact 220 couv 0.9205 F1 0.5836 tete 0.7332 POS 0.7581
   par_langue {'fr': {'cibles': 151, 'labels': 134, 'exact': 134, 'topk': 133, 'exact_taux_span': 1.0}, 'en': {'cibles': 88, 'labels': 86, 'exact': 86, 'topk': 86, 'exact_taux_span': 1.0}}
   tete_att {'cibles': 220, 'labels': 220, 'top1': 220, 'topk': 219, 'top1_taux': 1.0, 'topk_taux': 0.9955, 'couverture': 1.0
… [1 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du corpus, des types et des outils statistiques disponibles

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, collections\nsys.path.insert(0, 'tools'); sys.path.insert(0, '.')\nfrom tools.tests.linguistique import evaluer_gold as eg\nph = eg.charger(); ge = eg.charger_gele()\nprint('vivant', len(ph), 'gel … [739 caractères tronqués]`

  ```
vivant 612 gele 602
vivant {'hand': 20, 'reel': 432, 'synthetique': 160} {'fr': 402, 'en': 210} segments {'GN': 828, 'GV': 712, 'GP': 105, 'SUB': 70, 'REL': 74, 'ADJ': 35, 'ADV': 30, 'PONCT': 9} cibles {'GP': 96, 'SUB': 69, 'REL': 74} n_cibles 239
 ids uniques 612
gele {'hand': 20, 'reel': 422, 'synthetique': 160} {'fr': 394, 'en': 208} segments {'GN': 818, 'GV': 702, 'GP': 105, 'SUB': 69, 'REL': 74, 'ADJ': 35, 'ADV': 28} cibles {'GP': 96, 'SUB': 69, 'REL': 74} n_cibles 239
 ids uniques 602
scipy?
scipy 1.18.1
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -S'ées' -- tools/bloc_linguistique.py | head -5; echo '--- blame lignes 480-495 ---'; git blame -L 480,495 tools/bloc_linguistique.py", "description": "Trace origin of -ée handling"}`

  ```
a408a909 B13 — LE LEXIQUE ÉLARGI (PARTICIPES IRRÉGULIERS ET EN -É) : EXACT 0,8082 → 0,8483 ; 174/174
4a85604d B13 — LA PRAGMATIQUE NEURONALE EST SOUS L'HEURISTIQUE : TEST 0,6375 (MAJORITAIRE 0,7556), DEV 1,0 ; L'HEURISTIQUE GARDE
7ef0199c B13 — LE GOLD NEURONAL : TAGGER 7B LOCAL, CASCADE POS 0,944 ; PORTE BLOC VERTE, B13 134/140 (6 ROUGES S)
651bfc90 BLOC LINGUISTIQUE — NEUF NIVEAUX, HEURISTIQUE ET NEURONAL, 398 LANGUES À 0,9687
--- blame lignes 480-495 ---
dcf7bc91 (Stéphane 2026-11-05 15:18:56 -0500 480)     n = _normaliser(_sans_enclitique(mot))
d400e188 (Stéphane 2026-11-05 09:11:28 -0500 481)     if not n:
d400e188 (Stéphane 2026-11-05 09:11:28 -0500 482)         return False
d400e188 (Stéphane 2026-11-05 09:11:28 -0500 483)     if n in VERBES_CONNUS:
d400e188 (Stéphane 2026-11-05 09:11:28 -0500 484)         return True
d400e188 (Stéphane 2026-11-05 09:11:28 -0500 485)     for suf in ("er", "ir", "e", "es", "ent", "ait", "aient", "é", "ée", "és", "i", "u",
d400e188 (Stéphane 2026-11-05 09:11:28 -0500 486)                 "ez", "ons", "iez", "ais", "ra", "rai", "ras", "rons", "rez", "ront",
d400e188 (Stéphane 2026-11-05 09:11:28 -0500 487)                 "s", "ed", "ing", "en"
… [708 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la fiche v10 livrée avec le commit (pour cadrer l'écart)

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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 710ec7f9 -- tools/pensee/autotest.py | head -120", "description": "Inspect autotest changes in v10"}`

  ```
commit 710ec7f982ea3a85a3ca2cb8afc8e3390a129c9c
Author: Stéphane <stephane@localhost>
Date:   Thu Nov 5 23:16:21 2026 -0500

    B13 — LE FÉMININ -ÉE ET LA GARDE DÉTERMINANT DU GP : EXACT 220/220 (1,0000), COUVERTURE 0,9205, F1 0,5880, 19 SPANS ; 183/183

diff --git a/tools/pensee/autotest.py b/tools/pensee/autotest.py
index 94cc7d6c..94b9f354 100644
--- a/tools/pensee/autotest.py
+++ b/tools/pensee/autotest.py
@@ -1668,7 +1668,7 @@ def t109_anaphore_103() -> tuple[bool, str]:
 
 
 def t110_segmenteur() -> tuple[bool, str]:
-    """Le segmenteur : S F1 0,5006 (français seul), chunker 0,6178 ; tête 0,6675 / 0,7632 (gelé 602)."""
+    """Le segmenteur : S F1 0,5014 (français seul), chunker 0,6203 ; tête 0,6677 / 0,7639 (gelé 602)."""
     import tools.bloc_linguistique as bl
     from ..tests.linguistique.evaluer_gold import charger_gele as charger, evaluer_bloc
     ph = charger()
@@ -1681,7 +1681,7 @@ def t110_segmenteur() -> tuple[bool, str]:
     f2 = round(r2["syntagme"]["f1"], 4)
     t1 = round(r1["syntagme"]["tete"]["f1"], 4)
     t2 = round(r2["syntagme"]["tete"]["f1"], 4)
-    return (abs(f1 - 0.5006) < 0.001 and abs(f2 - 0.6178) < 0.001
+    return (abs(f1 - 0.5014) < 0.00
… [4923 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Construction du harnais de mesure (splits, langues, types) dans /tmp

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"class Annotation\\|class Etiquette\\|def analyser\" tools/bloc_linguistique.py | head -20; echo '---'; sed -n '60,130p' tools/bloc_linguistique.py", "description": "Inspect Annotation and analyser API"}`

  ```
68:class Etiquette:
92:class Annotation:
133:    def analyser(self, texte: str, langue: str | None = None,
999:    def analyser(self, texte: str, langue: str | None = None,
1272:    def analyser(self, texte: str, langue: str | None = None,
1341:    def analyser(self, texte: str, langue: str | None = None,
1451:    def analyser(self, texte: str, langue: str | None = None,
1585:    def analyser(self, texte: str, langue: str | None = None,
1677:    def analyser(self, texte: str, langue: str | None = None,
1755:    def analyser(self, texte: str, langue: str | None = None,
1938:    def analyser(self, texte: str, langue: str | None = None,
1966:    def analyser(self, texte: str, langue: str | None = None,
---
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
           
… [1926 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0, 'tools'); sys.path.insert(0, '.')\nfrom tools.tests.linguistique import evaluer_gold as eg\nimport bloc_linguistique as bl\nph = eg.charger()\nh = bl.Heuristique()\np = ph[0]\na … [485 caractères tronqués]`

  ```
<class 'bloc_linguistique.Annotation'> dict_keys(['texte', 'langue', 'script', 'etiquettes', 'refus', 'trace', 'cout', 'unites_semantiques', 'fraction_semantique', 'source', 'contexte'])
Etiquette(niveau='graphème', type='lettres', valeur='Le', debut=0, fin=2, source='heuristique', confiance=0.99, candidats=[], langue='fr', script='Latn', meta={})
Etiquette(niveau='mot', type='mot', valeur='Le', debut=0, fin=2, source='heuristique', confiance=0.98, candidats=[], langue='fr', script='Latn', meta={})
Etiquette(niveau='pos', type='DET', valeur='Le', debut=0, fin=2, source='heuristique', confiance=0.92, candidats=[], langue='fr', script='Latn', meta={'ouvert': False})
Etiquette(niveau='syntagme', type='GN', valeur='Le chat', debut=0, fin=7, source='heuristique', confiance=0.55, candidats=['structure la plus proche', 'dort'], langue='fr', script='Latn', meta={'role': 'agent', 'niveau': 1, 'attachement': {'segment': 'Le chat', 'cible': 'dort'}})
Etiquette(niveau='discours', type='paragraphe', valeur='suite', debut=0, fin=13, source='heuristique', confiance=0.5, candidats=['suite', 'contraste', 'cause', 'conséquence'], langue='fr', script='Latn', meta={})
Etiquette(niveau='document', type
… [872 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Repérage des 19 spans perdus actuels et des cibles par seau

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, zlib, collections, json\nsys.path.insert(0, 'tools'); sys.path.insert(0, '.')\nfrom tools.tests.linguistique import evaluer_gold as eg\nimport bloc_linguistique as bl\nph = eg.charger(); h = bl.Heuristi … [869 caractères tronqués]`

  ```
cibles par seau {0: 76, 1: 89, 2: 74} total 239
perdus 19 Counter({'REL': 9, 'SUB': 6, 'GP': 4})
('r035', 'en', 'REL', 'reel', 9, 24, 'she talks about', 'film', 2)
('r255', 'fr', 'REL', 'reel', 11, 27, "que j'ai achetée", 'voiture', 0)
('r264', 'fr', 'SUB', 'reel', 8, 26, "qu'il vient demain", 'sais', 0)
('r288', 'en', 'SUB', 'reel', 7, 29, 'that he comes tomorrow', 'know', 0)
('r303', 'fr', 'SUB', 'reel', 8, 23, 'car il est tard', 'pars', 2)
('s010', 'fr', 'REL', 'synthetique', 10, 18, 'qui nage', 'chemin', 1)
('s027', 'fr', 'GP', 'synthetique', 31, 33, 'il', 'marche', 1)
('s035', 'fr', 'REL', 'synthetique', 10, 19, 'qui ferme', 'papier', 0)
('s037', 'fr', 'REL', 'synthetique', 5, 15, 'qui marche', 'Paul', 1)
('s044', 'fr', 'SUB', 'synthetique', 17, 29, 'que ils crie', 'nage', 2)
('s061', 'fr', 'REL', 'synthetique', 9, 18, 'qui saute', 'nuage', 2)
('s065', 'fr', 'REL', 'synthetique', 5, 17, 'qui commence', 'elle', 2)
('s112', 'fr', 'SUB', 'synthetique', 24, 39, 'que Lucas ferme', 'nage', 0)
('s114', 'fr', 'SUB', 'synthetique', 22, 43, 'que les avocat compte', 'dessine', 2)
('s125', 'fr', 'REL', 'synthetique', 11, 21, 'qui compte', 'renard', 1)
('s141', 'fr', 'REL', 'synthetique', 
… [249 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Diagnostic des deux cas limites (r255, r303) et du rôle réel des corrections

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0, 'tools'); sys.path.insert(0, '.')\nfrom tools.tests.linguistique import evaluer_gold as eg\nimport bloc_linguistique as bl\nph = {p['id']: p for p in eg.charger()}\nh = bl.Heuristique … [806 caractères tronqués]`

  ```
======================================================================
r303 fr reel 'Je pars car il est tard.'
 gold: [('GN', 0, 2, 'Je', None), ('GV', 3, 7, 'pars', None), ('SUB', 8, 23, 'car il est tard', 'pars')]
 pred: [('GV', 0, 7, 'Je pars', None), ('GV', 3, 7, 'pars', None), ('SUB', 8, 18, 'car il est', 'pars'), ('GV', 12, 18, 'il est', 'pars'), ('GP', 19, 23, 'tard', 'pars')]
======================================================================
r255 fr reel "La voiture que j'ai achetée roule."
 gold: [('GN', 0, 10, 'La voiture', None), ('REL', 11, 27, "que j'ai achetée", 'voiture'), ('GV', 28, 33, 'roule', None)]
 pred: [('GN', 0, 10, 'La voiture', None), ('REL', 11, 33, "que j'ai achetée roule", 'voiture')]
======================================================================
s037 fr synthetique 'Paul qui marche marche'
 gold: [('GN', 0, 4, 'Paul', None), ('REL', 5, 15, 'qui marche', 'Paul'), ('GV', 16, 22, 'marche', None)]
 pred: [('GV', 0, 4, 'Paul', None), ('SUB', 5, 15, 'qui marche', 'Paul'), ('REL', 5, 22, 'qui marche marche', 'Paul'), ('GV', 16, 22, 'marche', None)]
======================================================================
g017 en hand 'She said that s
… [989 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des bases vivant/gelé et des valeurs publiées v10

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0, 'tools'); sys.path.insert(0, '.')\nfrom tools.tests.linguistique import evaluer_gold as eg\nimport bloc_linguistique as bl\nh = bl.Heuristique()\nfor nom, ps in [('vivant', eg.charger … [529 caractères tronqués]`

  ```
vivant phrases 612 F1 0.5836 tete 0.7332 POS 0.7581 labels 220 exact 220 topk 219 couv 0.9205
  precision/rappel 0.6275 0.5454
gele phrases 602 F1 0.588 tete 0.7388 POS 0.7603 labels 220 exact 220 topk 219 couv 0.9205
  precision/rappel 0.6302 0.5511
  ```

