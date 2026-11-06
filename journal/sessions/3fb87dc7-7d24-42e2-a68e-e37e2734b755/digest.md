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

### 🤖 Assistant

⏵ Vérification des dépendances du module avant copie des versions antérieures

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,60p' tools/bloc_linguistique.py; echo '--- ressources ---'; grep -n \"__file__\\|open(\\|Path(\" tools/bloc_linguistique.py | head -20", "description": "Inspect module imports and resource loading"}`

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
… [1962 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat f908d7b0..HEAD -- tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json tools/tests/linguistique/gold_synthetique.json tools/tests/linguistique/gold_gele.json; echo '---'; git diff --stat f908d7b0 … [172 caractères tronqués]`

  ```
---
 tools/bloc_linguistique.py | 34 +++++++++++++++++++++++++---------
 1 file changed, 25 insertions(+), 9 deletions(-)
---
 tools/bloc_linguistique.py | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
  ```

### 🤖 Assistant

⏵ Calibrage des tests χ² sur le split canonique (méthode v7)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'.')\nfrom tools.tests.linguistique import evaluer_gold as eg, gold_split as gs\nfrom scipy.stats import chi2_contingency\nph = eg.charger(); d … [1324 caractères tronqués]`

  ```
source vs dev chi2=1.353 p=0.5083 dof=2 min_exp=6.21
source vs tout chi2=0.711 p=0.7009 dof=2 min_exp=5.92
langue vs dev chi2=0.001 p=0.9712 dof=1 min_exp=65.20
langue vs tout chi2=0.001 p=0.9791 dof=1 min_exp=65.15
type vs dev chi2=3.902 p=0.1421 dof=2 min_exp=21.94
type vs tout chi2=2.098 p=0.3503 dof=2 min_exp=21.96
type_langue vs dev chi2=5.115 p=0.4020 dof=5 min_exp=8.27
type_langue vs tout chi2=2.768 p=0.7357 dof=5 min_exp=7.96
  ```

### 🤖 Assistant

⏵ Écriture du harnais complet de re-mesure (split, langues, types, contrôles)

- **write** `{"file_path": "/tmp/v10/harnais.py", "content": "#!/usr/bin/env python3\n\"\"\"Harnais de re-mesure dev/test v10 — hors dépôt (/tmp).\n\nMesure le bloc heuristique sur le gold vivant 612, le gold gelé 602, les trois\ndécoupages crc32(id) % 3 == 0/1/2, par langue et par type, avec :\n  - validation c … [44962 caractères tronqués]`

  ```
<path>/tmp/v10/harnais.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Exécution du harnais (première passe, correction des erreurs)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 600 python3 /tmp/v10/harnais.py 2>&1 | tail -80", "description": "Run measurement harness", "timeoutMs": 620000}`

  ```
Traceback (most recent call last):
  File "/tmp/v10/harnais.py", line 881, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/tmp/v10/harnais.py", line 652, in main
    {k: sorted(v["pred_segs"]) for k, v in recs.items()}, sort_keys=True,
               ~^^^^^^^^^^^^^
KeyError: 'pred_segs'
  ```

### 🤖 Assistant

⏵ Correction du digest de déterminisme et relance

- **bash** `{"command": "cd /tmp/v10 && python3 - <<'EOF'\nimport re\np = '/tmp/v10/harnais.py'\ns = open(p, encoding='utf-8').read()\nold = '            \"n_pred\": len(pred_segs), \"n_gold\": len(gold_segs),'\nnew = '            \"pred_segs\": pred_segs,\\n            \"n_pred\": len(pred_segs), \"n_gold\": l … [301 caractères tronqués]`

  ```
ok
== validation ==
tout écart max 10.0 phrases 612
dev écart max 6.0 phrases 422
test écart max 5.0 phrases 190
gelé 602: {'phrases': 602, 'pos': 0.7603, 'f1': 0.588, 'tete': 0.7388, 'labels': 220, 'exact': 220, 'couverture': 0.9205, 'topk': 219}

== canonique ==
dev phrases 422 cibles 163 labels 152 exact 152 couv 0.9325 F1 0.5812 tête 0.733 POS 0.7547
   langue {'fr': (101, 91, 91, 0.901), 'en': (62, 61, 61, 0.9839)}
   type {'REL': (57, 51, 51, 0.8947, 0.7907, 0.9573), 'SUB': (45, 42, 42, 0.9333, 0.9247, 0.9462), 'GP': (61, 59, 59, 0.9672, 0.8553, 0.8609)}
test phrases 190 cibles 76 labels 68 exact 68 couv 0.8947 F1 0.589 tête 0.7337 POS 0.7656
   langue {'fr': (50, 43, 43, 0.86), 'en': (26, 25, 25, 0.9615)}
   type {'REL': (17, 14, 14, 0.8235, 0.7179, 0.9444), 'SUB': (24, 21, 21, 0.875, 0.8571, 0.9583), 'GP': (35, 33, 33, 0.9429, 0.8571, 0.8675)}
all phrases 612 cibles 239 labels 220 exact 220 couv 0.9205 F1 0.5836 tête 0.7332 POS 0.7581
   langue {'fr': (151, 134, 134, 0.8874), 'en': (88, 86, 86, 0.9773)}
   type {'REL': (74, 65, 65, 0.8784, 0.7738, 0.9542), 'SUB': (69, 63, 63, 0.913, 0.9014, 0.9504), 'GP': (96, 92, 92, 0.9583, 0.8559, 0.8632)}

== stabilité ==
exact_taux_spa
… [2677 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Localisation de l'écart harnais/evaluer_bloc avant de publier

- **bash** `{"command": "cd /tmp/v10 && python3 - <<'EOF'\nimport json\nd = json.load(open('mesures.json'))\nfor nom in ('tout','dev','test'):\n    v = d['validation'][nom]\n    print('='*20, nom, 'ecart', v['ecart_max'])\n    def walk(a, b, path=''):\n        if isinstance(a, dict) and isinstance(b, dict):\n   … [388 caractères tronqués]`

  ```
==================== tout ecart 10.0
  /attachement/verbe/cibles: ref=149 moi=159 ecart=+10.000000
  /attachement/verbe/taux: ref=1.0 moi=0.9371 ecart=-0.062900
  /attachement/nom/cibles: ref=71 moi=80 ecart=+9.000000
  /attachement/nom/taux: ref=1.0 moi=0.8875 ecart=-0.112500
  /attachement_tete/cibles: ref=220 moi=239 ecart=+19.000000
  /attachement_tete/labels: ref=220 moi=235 ecart=+15.000000
  /attachement_tete/top1: ref=220 moi=235 ecart=+15.000000
  /attachement_tete/topk: ref=219 moi=234 ecart=+15.000000
  /attachement_tete/top1_taux: ref=1.0 moi=0.9833 ecart=-0.016700
  /attachement_tete/topk_taux: ref=0.9955 moi=0.9791 ecart=-0.016400
  /attachement_tete/couverture: ref=1.0 moi=0.9833 ecart=-0.016700
==================== dev ecart 6.0
  /attachement/verbe/cibles: ref=97 moi=102 ecart=+5.000000
  /attachement/verbe/taux: ref=1.0 moi=0.951 ecart=-0.049000
  /attachement/nom/cibles: ref=55 moi=61 ecart=+6.000000
  /attachement/nom/taux: ref=1.0 moi=0.9016 ecart=-0.098400
  /attachement_tete/cibles: ref=152 moi=163 ecart=+11.000000
  /attachement_tete/labels: ref=152 moi=160 ecart=+8.000000
  /attachement_tete/top1: ref=152 moi=160 ecart=+8.000000
  /attachement_tete/topk: re
… [932 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Correction des dénominateurs (verbe/nom, tête) et des valeurs brutes

- **bash** `{"command": "cd /tmp/v10 && python3 - <<'EOF'\np = '/tmp/v10/harnais.py'\ns = open(p, encoding='utf-8').read()\n\n# 1) verbe/nom : dénominateur = labels (le code officiel saute les spans non trouvés)\nold = '''    verbe_n = sum(1 for x in tg if x[\"verbe\"])\n    verbe_ok = sum(x[\"exact\"] for x in … [10580 caractères tronqués]`

  ```
patched
== validation ==
tout écart max 0.0 phrases 612
dev écart max 0.0 phrases 422
test écart max 0.0 phrases 190
gelé 602: {'phrases': 602, 'pos': 0.7603, 'f1': 0.588, 'tete': 0.7388, 'labels': 220, 'exact': 220, 'couverture': 0.9205, 'topk': 219}

== canonique ==
dev phrases 422 cibles 163 labels 152 exact 152 couv 0.9325 F1 0.5812 tête 0.733 POS 0.7547
   langue {'fr': (101, 91, 91, 0.901), 'en': (62, 61, 61, 0.9839)}
   type {'REL': (57, 51, 51, 0.8947, 0.7907, 0.9573), 'SUB': (45, 42, 42, 0.9333, 0.9247, 0.9462), 'GP': (61, 59, 59, 0.9672, 0.8553, 0.8609)}
test phrases 190 cibles 76 labels 68 exact 68 couv 0.8947 F1 0.589 tête 0.7337 POS 0.7656
   langue {'fr': (50, 43, 43, 0.86), 'en': (26, 25, 25, 0.9615)}
   type {'REL': (17, 14, 14, 0.8235, 0.7179, 0.9444), 'SUB': (24, 21, 21, 0.875, 0.8571, 0.9583), 'GP': (35, 33, 33, 0.9429, 0.8571, 0.8675)}
all phrases 612 cibles 239 labels 220 exact 220 couv 0.9205 F1 0.5836 tête 0.7332 POS 0.7581
   langue {'fr': (151, 134, 134, 0.8874), 'en': (88, 86, 86, 0.9773)}
   type {'REL': (74, 65, 65, 0.8784, 0.7738, 0.9542), 'SUB': (69, 63, 63, 0.913, 0.9014, 0.9504), 'GP': (96, 92, 92, 0.9583, 0.8559, 0.8632)}

== stabilité ==
exact_taux
… [2609 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des versions f908d7b0 et 160d08ca sur r303/r153/r280/g017

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show f908d7b0:tools/bloc_linguistique.py > /tmp/v10/bloc_f908d7b0.py && git show 160d08ca:tools/bloc_linguistique.py > /tmp/v10/bloc_160d08ca.py && python3 - <<'EOF'\nimport sys, importlib.util\nsys.path.insert(0, '/home/stephane … [1370 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 13, in <module>
  File "<stdin>", line 9, in charger
  File "<frozen importlib._bootstrap_external>", line 1027, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/tmp/v10/bloc_f908d7b0.py", line 58, in <module>
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
AttributeError: 'NoneType' object has no attribute '__dict__'. Did you mean: '__dir__'?
[exit code: 1]
  ```

### 🤖 Assistant

⏵ Correction de l'import des modules historiques et nouvelle vérification

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util\nsys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nfrom tools.tests.linguistique import e … [1236 caractères tronqués]`

  ```
============================== f908d7b0
  acheter dans VERBES_CONNUS ? False | _est_verbe(achetée) False
   r303 exact []
   r255 perdus [('REL', 11, 27, 'voiture')]
   r153 perdus [('GP', 8, 19, 'wait')]
   r280 perdus [('REL', 8, 21, 'car')]
   g017 perdus [('SUB', 9, 28, 'said')]
   s037 perdus [('REL', 5, 15, 'Paul')]
============================== 160d08ca
  acheter dans VERBES_CONNUS ? False | _est_verbe(achetée) False
   r303 perdus [('SUB', 8, 23, 'pars')]
   r255 perdus [('REL', 11, 27, 'voiture')]
   r153 perdus [('GP', 8, 19, 'wait')]
   r280 exact []
   g017 exact []
   s037 perdus [('REL', 5, 15, 'Paul')]
  ```

### 🤖 Assistant

⏵ Extraction et contrôle des tableaux canoniques (langue, type, croisement)

- **bash** `{"command": "cd /tmp/v10 && python3 - <<'EOF'\nimport json\nd = json.load(open('mesures.json'))\ncan = d['splits']['canonique']\nfor h in ('dev','test'):\n    a = can[h]\n    print('='*25, h.upper())\n    at = a['attachement']\n    print('phrases', a['phrases'], 'tokens', a['tokens'], 'cibles', at[' … [1738 caractères tronqués]`

  ```
========================= DEV
phrases 422 tokens 2185 cibles 163 labels 152 exact 152 exact_any 152 topk 152 topk_exact 152
couverture 0.9325 exact_taux_span 1.0 top1_taux 0.9325 topk_taux 0.9325 exact_any_taux_span 1.0 verbe {'cibles': 97, 'justes': 97, 'taux': 1.0} nom {'cibles': 55, 'justes': 55, 'taux': 1.0}
F1 {'precision': 0.6289, 'rappel': 0.5401, 'f1': 0.5812, 'tp': 700, 'fp': 413, 'fn': 596} 
TETE {'precision': 0.8116, 'rappel': 0.6682, 'f1': 0.733, 'tp': 866, 'fp': 201, 'fn': 430}
POS {'exactitude': 0.7547, 'exactitude_ferme': 0.8952, 'exactitude_ouvert': 0.6201, 'justes': 1649, 'tokens': 2185}
PRAGMA {'acte': 1.0, 'negation': 0.9787, 'modalite': 0.9929, 'double_sens': 0.9336} fraction 0.5509
ATT_TETE {'cibles': 152, 'labels': 152, 'top1': 152, 'topk': 152, 'top1_taux': 1.0, 'topk_taux': 1.0, 'couverture': 1.0}
PERDUS {'total': 11, 'par_type': {'REL': 6, 'SUB': 3, 'GP': 2}, 'par_langue': {'en': 1, 'fr': 10}, 'par_source': {'reel': 2, 'synthetique': 9}}
LANGUE:
  fr {'phrases': 277, 'cibles': 101, 'labels': 91, 'exact': 91, 'couverture': 0.901, 'exact_taux_span': 1.0} F1 0.5517 tete 0.7041 POS 0.7558
  en {'phrases': 145, 'cibles': 62, 'labels': 61, 'exact': 61, 'couvertur
… [2743 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction des trois splits (langues, types) et des contrôles d'équilibre

- **bash** `{"command": "cd /tmp/v10 && python3 - <<'EOF'\nimport json\nd = json.load(open('mesures.json'))\nprint('GLOBAL compte:', {k:d['equilibre_global'][k] for k in ('phrases','tokens','sources','langues','types_tout','types_cibles','cibles','cibles_par_langue','cibles_par_source')})\nprint('buckets', d['t … [2394 caractères tronqués]`

  ```
GLOBAL compte: {'phrases': 612, 'tokens': 3179, 'sources': {'hand': 20, 'reel': 432, 'synthetique': 160}, 'langues': {'fr': 402, 'en': 210}, 'types_tout': {'GN': 828, 'GV': 712, 'GP': 105, 'SUB': 70, 'REL': 74, 'ADJ': 35, 'ADV': 30, 'PONCT': 9}, 'types_cibles': {'GP': 96, 'SUB': 69, 'REL': 74}, 'cibles': 239, 'cibles_par_langue': {'fr': 151, 'en': 88}, 'cibles_par_source': {'hand': 13, 'reel': 171, 'synthetique': 55}}
buckets {'0': 190, '1': 229, '2': 193}

==================== canonique crc32(id)%3==0 -> test
dev phr 422 cib 163 lab 152 ex 152 couv 0.9325 F1 0.5812 tete 0.733 POS 0.7547 perdus 11
   lang {'fr': (101, 91, 91, 0.901, 0.5517, 0.7041, 0.7558), 'en': (62, 61, 61, 0.9839, 0.637, 0.7861, 0.7528)}
   type {'REL': (57, 51, 51, 0.8947, 0.7907, 0.9573), 'SUB': (45, 42, 42, 0.9333, 0.9247, 0.9462), 'GP': (61, 59, 59, 0.9672, 0.8553, 0.8609)}
test phr 190 cib 76 lab 68 ex 68 couv 0.8947 F1 0.589 tete 0.7337 POS 0.7656 perdus 8
   lang {'fr': (50, 43, 43, 0.86, 0.5702, 0.7188, 0.7512), 'en': (26, 25, 25, 0.9615, 0.6271, 0.7627, 0.7925)}
   type {'REL': (17, 14, 14, 0.8235, 0.7179, 0.9444), 'SUB': (24, 21, 21, 0.875, 0.8571, 0.9583), 'GP': (35, 33, 33, 0.9429, 0.8571, 0.8675)}
 
… [9540 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Re-mesure des commits v7, audit et v9 avec le même évaluateur (comparaison homogène)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for sha in 69bd865e f908d7b0 160d08ca; do git show $sha:tools/bloc_linguistique.py > /tmp/v10/bloc_$sha.py; done && python3 - <<'EOF'\nimport sys, importlib.util\nsys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/to … [1235 caractères tronqués]`

  ```
============================== v7_69bd865e
  dev   phr 422 cib 163 lab 116 ex 106 couv 0.7117 F1 0.5776 tete 0.7359 POS 0.7547 topk 67
  test  phr 190 cib  76 lab  56 ex  50 couv 0.7368 F1 0.5927 tete 0.7482 POS 0.7656 topk 40
  tout  phr 612 cib 239 lab 172 ex 156 couv 0.7197 F1 0.5822 tete 0.7397 POS 0.7581 topk 107
  gele  phr 602 cib 239 lab 172 ex 156 couv 0.7197 F1 0.5858 tete 0.7441 POS 0.7603 topk 107
============================== audit_f908d7b0
  dev   phr 422 cib 163 lab 132 ex 123 couv 0.8098 F1 0.6019 tete 0.7503 POS 0.7547 topk 77
  test  phr 190 cib  76 lab  59 ex  53 couv 0.7763 F1 0.6017 tete 0.7531 POS 0.7656 topk 42
  tout  phr 612 cib 239 lab 191 ex 176 couv 0.7992 F1 0.6018 tete 0.7512 POS 0.7581 topk 119
  gele  phr 602 cib 239 lab 191 ex 176 couv 0.7992 F1 0.6057 tete 0.7558 POS 0.7603 topk 119
============================== v9_160d08ca
  dev   phr 422 cib 163 lab 136 ex 127 couv 0.8344 F1 0.6114 tete 0.7570 POS 0.7547 topk 127
  test  phr 190 cib  76 lab  62 ex  56 couv 0.8158 F1 0.6190 tete 0.7619 POS 0.7656 topk 57
  tout  phr 612 cib 239 lab 198 ex 183 couv 0.8285 F1 0.6138 tete 0.7585 POS 0.7581 topk 184
  gele  phr 602 cib 239 lab 198 ex 183 couv 0.8285
… [42 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Diagnostic de l'écart des rejeux historiques (RACINE/lexique)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"RACINE\" /tmp/v10/bloc_69bd865e.py | head -20; echo '---'; grep -n \"json.load\\|read_text\\|LEXIQUE\\|lexique\" /tmp/v10/bloc_69bd865e.py | head -30; echo '--- diff evaluer_gold ---'; git diff --stat 69bd865e..HEAD -- tool … [179 caractères tronqués]`

  ```
49:RACINE = pathlib.Path(__file__).resolve().parent.parent
633:            if str(RACINE / "tools/structures") not in sys.path:
634:                sys.path.insert(0, str(RACINE / "tools/structures"))
2115:    ap.add_argument("--modele", default=str(RACINE / "models/Qwen2.5-0.5B-Q4_0.gguf"))
2120:    ap.add_argument("--udhr", default=str(RACINE / "data/udhr/articles.jsonl"))
---
167:    for ligne in chemin.read_text(encoding="utf-8").splitlines():
170:        d = json.loads(ligne)
218:    scores = {l: len(mots & set(LEXIQUES[l])) / max(1, len(mots)) for l in LEXIQUES}
270:# --------------------------------------------------------------------------- lexiques
273:LEXIQUES = {
381:# Un lexique verbal minimal, bilingue, pour arbitrer les classes ouvertes : le POS de surface
754:        """Le **verbe** du span : le lexique d'abord, puis le POS `VERB`, sinon le dernier mot."""
844:            """Le verbe : le lexique, le POS, ou la **position** après un pronom sujet."""
1315:            d = json.loads(texte_sortie[debut:fin + 1])
1404:            sortie = json.loads(reponse.read().decode("utf-8"))
1430:            pos = json.loads(sortie[debut:fin + 1]).get("pos")
1538:            sortie
… [345 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des changements de gold entre v7, audit, v9 et HEAD

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -10 -- tools/tests/linguistique/gold.json tools/tests/linguistique/gold_reel.json tools/tests/linguistique/gold_synthetique.json tools/tests/linguistique/gold_gele.json; echo '--- stat 69bd865e..HEAD ---'; git diff  … [293 caractères tronqués]`

  ```
702b368c B13 — LES VRAIS ABSENTS : 5 PHRASES, 0 LIEN, GOLD 432 ; 140/140
651c1fc0 B13 — LE LIEN AUTOMATIQUE RÉPARÉ : 5/5 APRÈS RÉORDONNANCEMENT ET REPLI PRON/NOUN ; 136/136
297c4f17 B13 — LA RÉPONSE CONTEXTUELLE : 5/5, LA PHRASE PRÉCÉDENTE TRANCHE ; 134/134
20194fb1 B13 — LE GOLD GELÉ : 602 PHRASES, 21 PORTES PROTÉGÉES ; 133/133
26e4df27 B13 — LES QUESTIONS PIÈGES : 29/34, LE SI EST UNE CONVENTION ; 132/132
866fcaa7 B13 — LES QUESTIONS NÉGATIVES : 19/29, LA RÈGLE DE SURFACE NE S'INVERSE PAS ; 130/130
56b22212 B13 — LES 19 RÉPONSES DE RÉFÉRENCE : COUVERTURE 19/19, LE JUGE EST UTILISABLE ; 127/127
41c7d1f1 B13 — LA CORÉFÉRENCE À 103 LIENS : 86/103, CIBLE 100 ATTEINTE, GOLD 407 ; 112/112
4d8c9905 B13 — LA CORÉFÉRENCE À 68 LIENS : LE RÔLE PASSE DEVANT (52/51), GOLD 372 ; 111/111
8e9d0c1d B13 — LES CHAÎNES LONGUES : 7/10, LE RÔLE MANQUE, GOLD 342 ; 99/99
--- stat 69bd865e..HEAD ---
--- stat f908d7b0..HEAD ---
--- stat 160d08ca..HEAD ---
  ```

### 🤖 Assistant

⏵ Test direct des classes historiques (identité et annotation)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util\nsys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nsys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nimport bloc_linguistique as cur\n\ndef … [955 caractères tronqués]`

  ```
cur Heuristique module bloc_linguistique 94461644208240
old Heuristique module bloc_69bd865e 94461644621136
same? False
old sources: ['Heuristique']
cur [('GN', 0, 7, 'dort'), ('GV', 8, 12, 'chat')]
cur meta [('GN', 0, 7, {'role': 'agent', 'niveau': 1, 'attachement': {'segment': 'Le chat', 'cible': 'dort'}}), ('GV', 8, 12, {'role': 'predicat', 'niveau': 0, 'attachement': {'segment': 'dort', 'cible': 'chat'}})]
old [('GN', 0, 7, 'dort'), ('GV', 8, 12, 'chat')]
old meta [('GN', 0, 7, {'role': 'agent', 'niveau': 1, 'attachement': {'segment': 'Le chat', 'cible': 'dort'}}), ('GV', 8, 12, {'role': 'predicat', 'niveau': 0, 'attachement': {'segment': 'dort', 'cible': 'chat'}})]
  ```

### 🤖 Assistant

⏵ Inspection de l'import `tools/structures` et correction de RACINE

- **bash** `{"command": "sed -n '615,650p' /tmp/v10/bloc_69bd865e.py; echo '--- current ---'; sed -n '620,650p' /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "description": "Inspect tools/structures import in old module"}`

  ```
def _morphemes(mot: str) -> list[tuple[str, int, int, str]]:
        n = _normaliser(mot)
        sortie = []
        for suf in SUFFIXES:
            if len(n) > len(suf) + 2 and n.endswith(suf):
                sortie.append(("suffixe", len(mot) - len(suf), len(mot), suf))
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

        Lecture seule de l'API interne du S : `_tokens`/`_
… [1640 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rejeu des commits historiques avec RACINE corrigé

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util, pathlib\nRACINE = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nsys.path.insert(0, str(RACINE / 'tools'))\nsys.path.insert(0, str(RACINE))\nfrom tools.tests.linguistiq … [1098 caractères tronqués]`

  ```
============================== v7_69bd865e
  dev   phr 422 cib 163 lab 134 ex 133 couv 0.8221 F1 0.5512 tete 0.7132 POS 0.7547 topk 111
  test  phr 190 cib  76 lab  62 ex  62 couv 0.8158 F1 0.5651 tete 0.7196 POS 0.7656 topk 55
  tout  phr 612 cib 239 lab 196 ex 195 couv 0.8201 F1 0.5555 tete 0.7152 POS 0.7581 topk 166
  gele  phr 602 cib 239 lab 196 ex 195 couv 0.8201 F1 0.5595 tete 0.7205 POS 0.7603 topk 166
============================== audit_f908d7b0
  dev   phr 422 cib 163 lab 148 ex 148 couv 0.9080 F1 0.5723 tete 0.7270 POS 0.7547 topk 120
  test  phr 190 cib  76 lab  64 ex  64 couv 0.8421 F1 0.5714 tete 0.7241 POS 0.7656 topk 57
  tout  phr 612 cib 239 lab 212 ex 212 couv 0.8870 F1 0.5720 tete 0.7262 POS 0.7581 topk 177
  gele  phr 602 cib 239 lab 212 ex 212 couv 0.8870 F1 0.5763 tete 0.7316 POS 0.7603 topk 177
============================== v9_160d08ca
  dev   phr 422 cib 163 lab 152 ex 152 couv 0.9325 F1 0.5807 tete 0.7327 POS 0.7547 topk 152
  test  phr 190 cib  76 lab  67 ex  67 couv 0.8816 F1 0.5855 tete 0.7323 POS 0.7656 topk 66
  tout  phr 612 cib 239 lab 219 ex 219 couv 0.9163 F1 0.5822 tete 0.7326 POS 0.7581 topk 218
  gele  phr 602 cib 239 lab 219 ex 219 couv 0.91
… [44 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Calcul des contrôles (χ², Wilson, test de proportion, effets de bord de la garde GP)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util, pathlib, json, math, collections, zlib\nRACINE = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nsys.path.insert(0, str(RACINE/'tools')); sys.path.insert(0, str(RACINE)) … [2614 caractères tronqués]`

  ```
phrases changées v9->v10: 3 Counter({0: 2, 1: 1})
('g004', 1, [('GP', 11, 27), ('GV', 28, 31)], [])
('r147', 0, [('GP', 22, 31), ('GV', 32, 37)], [])
('r153', 0, [('GP', 8, 15), ('GV', 16, 19)], [('GP', 8, 19)])

chi2 tailles seaux Power_divergenceResult(statistic=np.float64(4.617647058823529), pvalue=np.float64(0.09937809822251098))
chi2 spans perdus x seaux Chi2ContingencyResult(statistic=np.float64(2.3720582349118873), pvalue=np.float64(0.3054316926180265), dof=2, expected_freq=array([[ 6.041841  , 69.958159  ],
       [ 7.07531381, 81.92468619],
       [ 5.88284519, 68.11715481]]))
wilson dev 152 163 0.9325 (0.8832, 0.9619)
wilson test 68 76 0.8947 (0.8058, 0.9457)
wilson tout 220 239 0.9205 (0.8792, 0.9485)
wilson REL dev 51 57 0.8947 (0.7888, 0.9509)
wilson REL test 14 17 0.8235 (0.5897, 0.9381)
wilson SUB dev 42 45 0.9333 (0.8214, 0.9771)
wilson SUB test 21 24 0.875 (0.69, 0.9566)
wilson GP dev 59 61 0.9672 (0.8881, 0.991)
wilson GP test 33 35 0.9429 (0.8139, 0.9842)
wilson fr dev 91 101 0.901 (0.8273, 0.9453)
wilson fr test 43 50 0.86 (0.7381, 0.9305)
wilson en dev 61 62 0.9839 (0.9141, 0.9971)
wilson en test 25 26 0.9615 (0.8111, 0.9932)
z dev-test couverture (1.0054, np.f
… [330 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection des deux phrases modifiées par la garde GP hors r153

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util, pathlib\nRACINE = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nsys.path.insert(0, str(RACINE/'tools')); sys.path.insert(0, str(RACINE))\nfrom tools.tests.linguistique … [1008 caractères tronqués]`

  ```
======================================================================
g004 fr hand 'Il a couru pour attraper le bus.'
gold [('GN', 0, 2, 'Il', None), ('GV', 3, 10, 'a couru', None), ('GP', 11, 31, 'pour attraper le bus', 'couru')]
v9 [('GV', 0, 2, 'Il', None), ('GV', 0, 10, 'Il a couru', None), ('GV', 3, 10, 'a couru', None), ('GP', 11, 27, 'pour attraper le', 'couru'), ('GP', 11, 31, 'pour attraper le bus', 'couru'), ('GV', 28, 31, 'bus', None)]
v10 [('GV', 0, 2, 'Il', None), ('GV', 0, 10, 'Il a couru', None), ('GV', 3, 10, 'a couru', None), ('GP', 11, 31, 'pour attraper le bus', 'couru')]
======================================================================
r147 fr reel 'Les clients attendent devant la porte.'
gold [('GN', 0, 11, 'Les clients', None), ('GV', 12, 21, 'attendent', None), ('GP', 22, 37, 'devant la porte', 'attendent')]
v9 [('GN', 0, 11, 'Les clients', 'attendent'), ('GV', 12, 21, 'attendent', 'clients'), ('GP', 22, 31, 'devant la', 'attendent'), ('GP', 22, 37, 'devant la porte', 'attendent'), ('GV', 32, 37, 'porte', None)]
v10 [('GN', 0, 11, 'Les clients', 'attendent'), ('GV', 12, 21, 'attendent', 'clients'), ('GP', 22, 37, 'devant la porte', 'attendent')]
=======
… [363 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction des agrégats globaux (langue, type, source, croisements)

- **bash** `{"command": "cd /tmp/v10 && python3 - <<'EOF'\nimport json\nd = json.load(open('mesures.json'))\ng = d['global']\nprint('GLOBAL', g['phrases'], g['tokens'], g['attachement']['cibles'], g['attachement']['labels'], g['attachement']['exact'])\nprint('F1', g['syntagme'], 'TETE', g['tete'], 'POS', g['pos … [1062 caractères tronqués]`

  ```
GLOBAL 612 3179 239 220 220
F1 {'precision': 0.6275, 'rappel': 0.5454, 'f1': 0.5836, 'tp': 1016, 'fp': 603, 'fn': 847} TETE {'precision': 0.8089, 'rappel': 0.6704, 'f1': 0.7332, 'tp': 1249, 'fp': 295, 'fn': 614} POS {'exactitude': 0.7581, 'exactitude_ferme': 0.9004, 'exactitude_ouvert': 0.6234, 'justes': 2410, 'tokens': 3179} PRAGMA {'acte': 0.9967, 'negation': 0.9771, 'modalite': 0.9886, 'double_sens': 0.9444}
LANG fr 151 134 134 0.8874 F1 0.5575 tete 0.7087 POS 0.7543
LANG en 88 86 86 0.9773 F1 0.6341 tete 0.7791 POS 0.7648
TYPE REL 74 65 65 0.8784 F1 0.7738 tete 0.9542 tp/fp/fn 65 29 9
TYPE SUB 69 63 63 0.913 F1 0.9014 tete 0.9504 tp/fp/fn 64 8 6
TYPE GP 96 92 92 0.9583 F1 0.8559 tete 0.8632 tp/fp/fn 101 30 4
TL REL/fr 46 38 38 0.8261
TL REL/en 28 27 27 0.9643
TL SUB/fr 43 38 38 0.8837
TL SUB/en 26 25 25 0.9615
TL GP/fr 62 58 58 0.9355
TL GP/en 34 34 34 1.0
SRC hand 13 13 13 1.0
SRC reel 171 166 166 0.9708
SRC synthetique 55 41 41 0.7455
ATT_TETE {'cibles': 220, 'labels': 220, 'top1': 220, 'topk': 219, 'top1_taux': 1.0, 'topk_taux': 0.9955, 'couverture': 1.0}
PERDUS {'total': 19, 'par_type': {'REL': 9, 'SUB': 6, 'GP': 4}, 'par_langue': {'en': 2, 'fr': 17}, 'par_source': {'reel':
… [238 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Calcul des F1 GN/GV et des valeurs par type/langue pour les trois splits

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util\nsys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools'); sys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nspec = importlib.util.spec_from_file_l … [1314 caractères tronqués]`

  ```
dev F1 par type:
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 12, in <module>
  File "/tmp/v10/harnais.py", line 227, in seg_agrege
    tp = sum(sum(r["seg_type"][t]["tp"] for t in types) for r in rs)
  File "/tmp/v10/harnais.py", line 227, in <genexpr>
    tp = sum(sum(r["seg_type"][t]["tp"] for t in types) for r in rs)
             ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/v10/harnais.py", line 227, in <genexpr>
    tp = sum(sum(r["seg_type"][t]["tp"] for t in types) for r in rs)
                 ~~~~~~~~~~~~~^^^
KeyError: 'GN'
[exit code: 1]
  ```

### 🤖 Assistant

⏵ Recalcul direct des F1 par type (y compris GN/GV) et table des splits

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util, json\nsys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools'); sys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nspec = importlib.util.spec_from_ … [1392 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 16, in <module>
  File "<stdin>", line 11, in f1_type
KeyError: 'gold_segs'
[exit code: 1]
  ```

### 🤖 Assistant

⏵ Recalcul des F1 par type avec le gold directement

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util, json\nsys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools'); sys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nspec = importlib.util.spec_from_ … [1485 caractères tronqués]`

  ```
dev {'GN': {'f1': 0.4932, 'precision': 0.63, 'rappel': 0.4052, 'tp': 235, 'fp': 138, 'fn': 345}, 'GV': {'f1': 0.5959, 'precision': 0.5709, 'rappel': 0.6232, 'tp': 306, 'fp': 230, 'fn': 185}, 'ADJ': {'f1': 0.0, 'precision': 0.0, 'rappel': 0.0, 'tp': 0, 'fp': 0, 'fn': 30}, 'ADV': {'f1': 0.0, 'precision': 0.0, 'rappel': 0.0, 'tp': 0, 'fp': 0, 'fn': 18}, 'PONCT': {'f1': 0.0, 'precision': 0.0, 'rappel': 0.0, 'tp': 0, 'fp': 0, 'fn': 7}, 'REL': {'f1': 0.7907, 'precision': 0.7083, 'rappel': 0.8947, 'tp': 51, 'fp': 21, 'fn': 6}, 'SUB': {'f1': 0.9247, 'precision': 0.9149, 'rappel': 0.9348, 'tp': 43, 'fp': 4, 'fn': 3}, 'GP': {'f1': 0.8553, 'precision': 0.7647, 'rappel': 0.9701, 'tp': 65, 'fp': 20, 'fn': 2}}
test {'GN': {'f1': 0.4798, 'precision': 0.5838, 'rappel': 0.4073, 'tp': 101, 'fp': 72, 'fn': 147}, 'GV': {'f1': 0.6247, 'precision': 0.6, 'rappel': 0.6516, 'tp': 144, 'fp': 96, 'fn': 77}, 'ADJ': {'f1': 0.0, 'precision': 0.0, 'rappel': 0.0, 'tp': 0, 'fp': 0, 'fn': 5}, 'ADV': {'f1': 0.0, 'precision': 0.0, 'rappel': 0.0, 'tp': 0, 'fp': 0, 'fn': 12}, 'PONCT': {'f1': 0.0, 'precision': 0.0, 'rappel': 0.0, 'tp': 0, 'fp': 0, 'fn': 2}, 'REL': {'f1': 0.7179, 'precision': 0.6364, 'rappel': 0.8235, 't
… [2285 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Décomposition réel/synthétique par langue (le confond source-langue)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util\nsys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools'); sys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nspec = importlib.util.spec_from_file_l … [1127 caractères tronqués]`

  ```
==================== reel (hand+reel) phr 452
  tout 184 179 179 0.9728 F1 0.5798 tete 0.7232 POS 0.7661
   fr 242 96 94 94 0.9792 F1 0.5392 tete 0.6804 POS 0.7673
   en 210 88 85 85 0.9659 F1 0.6324 tete 0.7774 POS 0.7648
==================== synthetique phr 160
  tout 55 42 42 0.7636 F1 0.6003 tete 0.7703 POS 0.7296
   fr 160 55 42 42 0.7636 F1 0.6003 tete 0.7703 POS 0.7296
   en 0 0 0 0 None F1 0.0 tete 0.0 POS 0.0
==================== source hand phr 20
  tout 13 12 12 0.9231 F1 0.7288 tete 0.8288 POS 0.8857
   fr 14 10 10 10 1.0 F1 0.7416 tete 0.8537 POS 0.8514
   en 6 3 2 2 0.6667 F1 0.6897 tete 0.7586 POS 0.9677
==================== source reel phr 432
  tout 171 167 167 0.9766 F1 0.5731 tete 0.7186 POS 0.7608
   fr 228 86 84 84 0.9767 F1 0.5267 tete 0.6704 POS 0.7623
   en 204 85 83 83 0.9765 F1 0.6309 tete 0.7779 POS 0.7592
==================== source synthetique phr 160
  tout 55 42 42 0.7636 F1 0.6003 tete 0.7703 POS 0.7296
   fr 160 55 42 42 0.7636 F1 0.6003 tete 0.7703 POS 0.7296
   en 0 0 0 0 None F1 0.0 tete 0.0 POS 0.0
  ```

### 🤖 Assistant

⏵ Debug de l'écart source×langue dans le harnais

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util, collections\nsys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools'); sys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nspec = importlib.util.spe … [1146 caractères tronqués]`

  ```
langues phrases Counter({'fr': 402, 'en': 210})
langues records Counter({'fr': 402, 'en': 210})
sources records Counter({'reel': 432, 'synthetique': 160, 'hand': 20})
hand recs 20 tg 13 trouve 12 lang Counter({('fr', True): 10, ('en', True): 2, ('en', False): 1}) srclang Counter({('fr', 'hand'): 14, ('en', 'hand'): 6})
   fr recs 14 tg 10 trouve 10
   en recs 6 tg 3 trouve 2
reel recs 432 tg 171 trouve 167 lang Counter({('fr', True): 84, ('en', True): 83, ('en', False): 2, ('fr', False): 2}) srclang Counter({('fr', 'reel'): 228, ('en', 'reel'): 204})
   fr recs 228 tg 86 trouve 84
   en recs 204 tg 85 trouve 83
synthetique recs 160 tg 55 trouve 42 lang Counter({('fr', True): 42, ('fr', False): 13}) srclang Counter({('fr', 'synthetique'): 160})
   fr recs 160 tg 55 trouve 42
   en recs 0 tg 0 trouve 0
  ```

### 🤖 Assistant

⏵ Investigation de l'incohérence hand 12/13 vs 13/13

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util, collections, json\nsys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools'); sys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nspec = importlib.ut … [1204 caractères tronqués]`

  ```
g002 fr GP 8 21 trouve True exact 1 cible chat pred chat
g003 fr GP 22 34 trouve True exact 1 cible vu pred vu
g004 fr GP 11 31 trouve True exact 1 cible couru pred couru
g005 fr SUB 11 28 trouve True exact 1 cible dit pred dit
g006 fr GP 9 18 trouve True exact 1 cible chien pred chien
g007 fr GP 19 33 trouve True exact 1 cible jouent pred jouent
g010 fr GP 6 9 trouve True exact 1 cible Viens pred Viens
g011 fr REL 9 20 trouve True exact 1 cible livre pred livre
g012 fr GP 19 27 trouve True exact 1 cible prêt pred prêt
g014 fr GP 16 33 trouve True exact 1 cible vu pred vu
g016 en GP 22 33 trouve True exact 1 cible saw pred saw
g017 en SUB 9 28 trouve False exact 0 cible said pred 
g020 en GP 18 24 trouve True exact 1 cible ready pred ready
perdus hand [('g017', [('SUB', 9, 28, 'said')])]
agg hand par_source {'hand': {'cibles': 13, 'labels': 12, 'exact': 12, 'exact_any': 12, 'top1': 12, 'topk': 12, 'topk_exact': 12, 'couverture': 0.9231, 'exact_taux_span': 1.0, 'exact_taux_cibles': 0.9231, 'exact_any_taux_span': 1.0, 'top1_taux': 0.9231, 'topk_taux': 0.9231, 'topk_taux_span': 1.0, 'topk_exact_taux': 0.9231, 'verbe': {'cibles': 7, 'justes': 7, 'taux': 1.0}, 'nom': {'cibles': 5, 'just
… [1223 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Alerte : g017 diffère entre deux exécutions — vérification de l'état de l'arbre

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git rev-parse HEAD && git status --porcelain tools/bloc_linguistique.py tools/tests/linguistique/ | head -20; echo '--- dirty code? ---'; git diff --stat -- tools/bloc_linguistique.py tools/tests/linguistique/; echo '--- mtime ---';  … [189 caractères tronqués]`

  ```
68a8717b057f21d389194679bf34f1cabc5c312d
 M tools/bloc_linguistique.py
--- dirty code? ---
 tools/bloc_linguistique.py | 11 ++++-------
 1 file changed, 4 insertions(+), 7 deletions(-)
--- mtime ---
2026-11-06 00:15:37.544747590 -0500 tools/bloc_linguistique.py
2026-11-05 16:37:50.944795187 -0500 tools/tests/linguistique/gold.json
2026-11-02 14:39:32.079131990 -0500 tools/tests/linguistique/gold_reel.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util\nsys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools'); sys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nspec = importlib.util.spec_from_file_l … [609 caractères tronqués]`

  ```
bl file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py
gold [('GN', 0, 3, None), ('GV', 4, 8, None), ('SUB', 9, 28, 'said')]
pred [('GV', 4, 8), ('SUB', 9, 38)]
collect target [{'type': 'SUB', 'langue': 'en', 'source': 'hand', 'debut': 9, 'fin': 28, 'cibles': ['said'], 'trouve': False, 'cible_pred': '', 'exact': 0, 'exact_any': 0, 'top1': 0, 'topk': 0, 'topk_exact': 0, 'verbe': True}]
  ```

### 🤖 Assistant

⏵ L'arbre a bougé pendant la mesure — inspection du nouveau HEAD et du diff sale

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -5; echo '=== 68a8717b stat ==='; git show --stat --oneline 68a8717b | head -30; echo '=== diff sale ==='; git diff -- tools/bloc_linguistique.py", "description": "Inspect new HEAD and dirty module diff"}`

  ```
68a8717b JOURNAL — LE 06/11 AU FORMAT DE L'INDEX (EN-TÊTE, LIENS, BLOC NOTES)
41cae3e5 JOURNAL — LE 06/11 S'OUVRE SUR LA NUIT DU DÉCOUPAGE : 220/220, COUVERTURE 0,9205, 19 SPANS
4d34c37a PILOTAGE — LES VAGUES 5 À 7 (AUDITS V7/V8, R1/R3, TOP-K, V10) DOCUMENTÉES AU PLAN-TRAVAIL
77ed0856 THÉORIE ET JOURNAL — LE DÉCOUPAGE D'ABORD : LA COUVERTURE EST UN PLAFOND, UN GOLD SE VÉRIFIE AVANT DE JUGER
710ec7f9 B13 — LE FÉMININ -ÉE ET LA GARDE DÉTERMINANT DU GP : EXACT 220/220 (1,0000), COUVERTURE 0,9205, F1 0,5880, 19 SPANS ; 183/183
=== 68a8717b stat ===
68a8717b JOURNAL — LE 06/11 AU FORMAT DE L'INDEX (EN-TÊTE, LIENS, BLOC NOTES)
 journal/2026-11-06/README.md                       |  13 ++-
 journal/2026-11-06/distribue.md                    |  27 ++++++
 journal/README.md                                  |   6 +-
 journal/THEMES.md                                  |   1 +
 .../3fb87dc7-7d24-42e2-a68e-e37e2734b755/digest.md |  54 +++++++++++
 .../rapport.md                                     |  17 ++--
 journal/sessions/MANIFEST.md                       |   8 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  35 +++++++
 .../rapport.md                                     |  15 +--
 
… [1979 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mesure de l'arbre sale (après 710ec7f9) pour documenter le ballant g017/r303

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, collections\nsys.path.insert(0, 'tools'); sys.path.insert(0, '.')\nfrom tools.tests.linguistique import evaluer_gold as eg, gold_split as gs\nimport bloc_linguistique as bl\nph = eg.charger(); d = gs.de … [1133 caractères tronqués]`

  ```
dev 163 152 152 0.9325 F1 0.5812 tete 0.7324 POS 0.7547
test 76 69 69 0.9079 F1 0.5914 tete 0.7344 POS 0.7656
tout 239 221 221 0.9247 F1 0.5843 tete 0.733 POS 0.7581
perdus 18 Counter({'REL': 9, 'SUB': 5, 'GP': 4})
ids ['g017', 'r035', 'r241', 'r255', 'r264', 's010', 's027', 's035', 's044', 's061', 's065', 's112', 's114', 's125', 's141', 's146', 's148', 's160']
g017 [('GV', 4, 8), ('SUB', 9, 38)]
s037 [('GV', 0, 4), ('REL', 5, 15), ('REL', 5, 22), ('GV', 16, 22)]
r303 [('GV', 0, 7), ('GV', 3, 7), ('SUB', 8, 23), ('GV', 12, 18), ('GP', 19, 23)]
r255 [('GN', 0, 10), ('REL', 11, 33)]
r153 [('GV', 3, 7), ('GP', 8, 19)]
r280 [('GN', 0, 7), ('REL', 8, 21), ('GV', 22, 26)]
  ```

### 🤖 Assistant

⏵ Épinglage du module 710ec7f9 et re-exécution de contrôle du harnais

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cp /tmp/v10/mesures.json /tmp/v10/mesures_avant_pin.json && git show 710ec7f9:tools/bloc_linguistique.py > /tmp/v10/bloc_710ec7f9.py && python3 - <<'EOF'\np = '/tmp/v10/harnais.py'\ns = open(p, encoding='utf-8').read()\nold = '''from … [1078 caractères tronqués]`

  ```
ok
== validation ==
tout écart max 0.0 phrases 612
dev écart max 0.0 phrases 422
test écart max 0.0 phrases 190
gelé 602: {'phrases': 602, 'pos': 0.7603, 'f1': 0.588, 'tete': 0.7388, 'labels': 220, 'exact': 220, 'couverture': 0.9205, 'topk': 219}

== canonique ==
dev phrases 422 cibles 163 labels 152 exact 152 couv 0.9325 F1 0.5812 tête 0.733 POS 0.7547
   langue {'fr': (101, 91, 91, 0.901), 'en': (62, 61, 61, 0.9839)}
   type {'REL': (57, 51, 51, 0.8947, 0.7907, 0.9573), 'SUB': (45, 42, 42, 0.9333, 0.9247, 0.9462), 'GP': (61, 59, 59, 0.9672, 0.8553, 0.8609)}
test phrases 190 cibles 76 labels 68 exact 68 couv 0.8947 F1 0.589 tête 0.7337 POS 0.7656
   langue {'fr': (50, 43, 43, 0.86), 'en': (26, 25, 25, 0.9615)}
   type {'REL': (17, 14, 14, 0.8235, 0.7179, 0.9444), 'SUB': (24, 21, 21, 0.875, 0.8571, 0.9583), 'GP': (35, 33, 33, 0.9429, 0.8571, 0.8675)}
all phrases 612 cibles 239 labels 220 exact 220 couv 0.9205 F1 0.5836 tête 0.7332 POS 0.7581
   langue {'fr': (151, 134, 134, 0.8874), 'en': (88, 86, 86, 0.9773)}
   type {'REL': (74, 65, 65, 0.8784, 0.7738, 0.9542), 'SUB': (69, 63, 63, 0.913, 0.9014, 0.9504), 'GP': (96, 92, 92, 0.9583, 0.8559, 0.8632)}

== stabilité ==
exact_taux_span
… [2608 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Comparaison JSON épinglé vs JSON initial (doit être identique)

- **bash** `{"command": "cd /tmp/v10 && python3 - <<'EOF'\nimport json\na=json.load(open('mesures_avant_pin.json')); b=json.load(open('mesures_pin.json'))\ndef diff(x,y,path=''):\n    if type(x)!=type(y): print('TYPE', path, type(x), type(y)); return\n    if isinstance(x,dict):\n        for k in set(x)|set(y):\ … [476 caractères tronqués]`

  ```
done
  ```

### 🤖 Assistant

⏵ Décomposition réel/synthétique sur le module épinglé 710ec7f9

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util\nsys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools'); sys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nspec = importlib.util.spec_from_file_l … [1499 caractères tronqués]`

  ```
==================== reel (hand+reel) phr 452
  tout 184 179 179 0.9728 F1 0.5798 tete 0.7239 POS 0.7661
   fr 242 96 93 93 0.9688 F1 0.5379 tete 0.6804 POS 0.7673
   en 210 88 86 86 0.9773 F1 0.6341 tete 0.7791 POS 0.7648
==================== synthetique phr 160
  tout 55 41 41 0.7455 F1 0.5969 tete 0.7682 POS 0.7296
   fr 160 55 41 41 0.7455 F1 0.5969 tete 0.7682 POS 0.7296
==================== source hand phr 20
  tout 13 13 13 1.0 F1 0.7458 tete 0.8288 POS 0.8857
   fr 14 10 10 10 1.0 F1 0.7416 tete 0.8537 POS 0.8514
   en 6 3 3 3 1.0 F1 0.7586 tete 0.7586 POS 0.9677
==================== source reel phr 432
  tout 171 166 166 0.9708 F1 0.5723 tete 0.7194 POS 0.7608
   fr 228 86 83 83 0.9651 F1 0.5253 tete 0.6704 POS 0.7623
   en 204 85 83 83 0.9765 F1 0.6309 tete 0.7796 POS 0.7592
==================== source synthetique phr 160
  tout 55 41 41 0.7455 F1 0.5969 tete 0.7682 POS 0.7296
   fr 160 55 41 41 0.7455 F1 0.5969 tete 0.7682 POS 0.7296
GLOBAL 239 220 220
par source {'hand': (13, 13), 'reel': (171, 166), 'synthetique': (55, 41)}
par langue {'fr': (151, 134), 'en': (88, 86)}
  ```

### 🤖 Assistant

⏵ Décomposition par source et par moitié (contrôle du confond synthétique/français)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, importlib.util\nsys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools'); sys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nspec = importlib.util.spec_from_file_l … [1280 caractères tronqués]`

  ```
dev reel           phr 317 cib 131 lab 129 couv 0.9847 F1 0.5788 tete 0.7275 POS 0.7609
dev synth          phr 105 cib  32 lab  23 couv 0.7188 F1 0.5904 tete 0.7560 POS 0.7300
dev synth-fr       phr 105 cib  32 lab  23 couv 0.7188 F1 0.5904 tete 0.7560 POS 0.7300
test reel          phr 135 cib  53 lab  50 couv 0.9434 F1 0.5823 tete 0.7152 POS 0.7787
test synth         phr  55 cib  23 lab  18 couv 0.7826 F1 0.6078 tete 0.7893 POS 0.7290
test synth-fr      phr  55 cib  23 lab  18 couv 0.7826 F1 0.6078 tete 0.7893 POS 0.7290

dev {'hand': 10, 'reel': 121, 'synthetique': 32} total 163
test {'hand': 3, 'reel': 50, 'synthetique': 23} total 76
  ```

### 🤖 Assistant

⏵ Inspection de r241 (effet de bord de l'essai R2 dans l'arbre sale)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0, 'tools'); sys.path.insert(0, '.')\nfrom tools.tests.linguistique import evaluer_gold as eg\nimport bloc_linguistique as bl\np = {x['id']:x for x in eg.charger()}['r241']\nprint(p['lan … [410 caractères tronqués]`

  ```
en reel 'The day when we left was beautiful.'
gold [('GN', 0, 7, 'The day', None), ('REL', 8, 20, 'when we left', 'day'), ('GV', 21, 24, 'was', None), ('ADJ', 25, 34, 'beautiful', None)]
pred [('GN', 0, 7, 'The day'), ('SUB', 8, 20, 'when we left'), ('GV', 21, 34, 'was beautiful')]
  ```

### 🤖 Assistant

⏵ Assemblage du JSON final (comparaisons rejouées, contrôles, notes d'arbre)

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Assemble reports/pensee-dev-test-v10.json à partir de la mesure épinglée 710ec7f9.\n\nNe touche à aucun fichier existant hors les deux sorties demandées.\n\"\"\"\nfrom __future__ import annotations\n\nimport importlib.util\nimport json\nimport math\nimport  … [21315 caractères tronqués]`

  ```
<path>/tmp/v10/construire_json.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Vérification des cibles neuves puis génération du JSON final

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l reports/rapport-dev-test-v10.md reports/pensee-dev-test-v10.json 2>&1; echo '---'; timeout 300 python3 /tmp/v10/construire_json.py 2>&1 | tail -20", "description": "Check targets and build final JSON", "timeoutMs": 320000}`

  ```
ls: cannot access 'reports/rapport-dev-test-v10.md': No such file or directory
ls: cannot access 'reports/pensee-dev-test-v10.json': No such file or directory
---
Traceback (most recent call last):
  File "/tmp/v10/construire_json.py", line 416, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/tmp/v10/construire_json.py", line 89, in main
    bloc[label] = resume(eg.evaluer_bloc("h", h, ps))
                  ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/v10/construire_json.py", line 56, in resume
    "exact_taux_cibles": a["exact_taux_cibles"],
                         ~^^^^^^^^^^^^^^^^^^^^^
KeyError: 'exact_taux_cibles'
  ```

### 🤖 Assistant

⏵ Correction du champ exact_taux (nommage variable selon la source) et relance

- **bash** `{"command": "cd /tmp/v10 && python3 - <<'EOF'\np='/tmp/v10/construire_json.py'\ns=open(p,encoding='utf-8').read()\nold='\"exact_taux_cibles\": a[\"exact_taux_cibles\"],'\nnew='\"exact_taux_cibles\": a.get(\"exact_taux_cibles\", a.get(\"exact_taux\")),'\nassert old in s\ns=s.replace(old,new,1)\nopen( … [244 caractères tronqués]`

  ```
ok
Traceback (most recent call last):
  File "/tmp/v10/construire_json.py", line 416, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/tmp/v10/construire_json.py", line 95, in main
    "dev": resume(can["dev"]), "test": resume(can["test"]),
           ~~~~~~^^^^^^^^^^^^
  File "/tmp/v10/construire_json.py", line 59, in resume
    "tete": r["syntagme"]["tete"]["f1"],
            ~~~~~~~~~~~~~^^^^^^^^
KeyError: 'tete'
  ```

### 🤖 Assistant

⏵ Gestion des deux formes de sortie (tête au niveau syntagme ou racine)

- **bash** `{"command": "cd /tmp/v10 && python3 - <<'EOF'\np='/tmp/v10/construire_json.py'\ns=open(p,encoding='utf-8').read()\nold='''def resume(r: dict) -> dict:\n    a = r[\"attachement\"]\n    return {\n        \"phrases\": r[\"phrases\"],\n        \"cibles\": a[\"cibles\"], \"labels\": a[\"labels\"], \"exac … [1787 caractères tronqués]`

  ```
ok
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-dev-test-v10.json 144763 octets
deltas v7 {"dev": {"labels": 18, "exact": 19, "couverture": 0.1104, "f1": 0.03, "tete": 0.0198, "pos": 0.0}, "test": {"labels": 6, "exact": 6, "couverture": 0.0789, "f1": 0.0239, "tete": 0.0141, "pos": 0.0}, "tout": {"labels": 24, "exact": 25, "couverture": 0.1004, "f1": 0.0281, "tete": 0.018, "pos": 0.0}, "gele": {"labels": 24, "exact": 25, "couverture": 0.1004, "f1": 0.0285, "tete": 0.0183, "pos": 0.0}}
deltas audit {"dev": {"labels": 4, "exact": 4, "couverture": 0.0245, "f1": 0.0089, "tete": 0.006, "pos": 0.0}, "test": {"labels": 4, "exact": 4, "couverture": 0.0526, "f1": 0.0176, "tete": 0.0096, "pos": 0.0}, "tout": {"labels": 8, "exact": 8, "couverture": 0.0335, "f1": 0.0116, "tete": 0.007, "pos": 0.0}, "gele": {"labels": 8, "exact": 8, "couverture": 0.0335, "f1": 0.0117, "tete": 0.0072, "pos": 0.0}}
deltas v9 {"dev": {"labels": 0, "exact": 0, "couverture": 0.0, "f1": 0.0005, "tete": 0.0003, "pos": 0.0}, "test": {"labels": 1, "exact": 1, "couverture": 0.0131, "f1": 0.0035, "tete": 0.0014, "pos": 0.0}, "tout": {"labels": 1, "exact": 1, "couverture": 0.0042, "f1": 0.0014, "tete
… [122 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du JSON final (comparaisons, synthèse, contrôles)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-dev-test-v10.json'))\nprint('meta', d['meta'])\nprint('synthese dev/test/tout', {k:d['synthese'][k] for k in ('dev','test','tout')})\nprint('gele', d['synthese']['gele_ … [1098 caractères tronqués]`

  ```
meta {'ligne': 'B13', 'commit': '710ec7f9', 'sha': '710ec7f982ea3a85a3ca2cb8afc8e3390a129c9c', 'branche': 's/v7', 'date': '2026-11-05', 'verdict': 'dev/test re-mesurés ; stabilité vérifiée ; 3 écarts de fiche', 'ancrage': 'commit 710ec7f9 ; HEAD ultérieur 68a8717b et module sale non mesurés', 'aucun_commit': True, 'aucun_fichier_existant_modifie': True, 'fichiers': ['reports/rapport-dev-test-v10.md', 'reports/pensee-dev-test-v10.json']}
synthese dev/test/tout {'dev': {'phrases': 422, 'cibles': 163, 'labels': 152, 'exact': 152, 'couverture': 0.9325, 'f1': 0.5812, 'tete': 0.733, 'pos': 0.7547}, 'test': {'phrases': 190, 'cibles': 76, 'labels': 68, 'exact': 68, 'couverture': 0.8947, 'f1': 0.589, 'tete': 0.7337, 'pos': 0.7656}, 'tout': {'phrases': 612, 'cibles': 239, 'labels': 220, 'exact': 220, 'couverture': 0.9205, 'f1': 0.5836, 'tete': 0.7332, 'pos': 0.7581}}
gele {'phrases': 602, 'pos': 0.7603, 'f1': 0.588, 'tete': 0.7388, 'labels': 220, 'exact': 220, 'couverture': 0.9205, 'topk': 219}
ecart {'exact_taux': 0.0, 'couverture': 0.0378, 'f1': -0.0078, 'tete': -0.0007, 'pos': -0.0109}
stabilite {'exact_taux_span': {'dev': 0.0, 'test': 0.0}, 'exact': {'dev': 18, 'test': 18}, 'labels': {'d
… [3103 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction de la fiche `reports/rapport-dev-test-v10.md`

- **write** `{"content": "# B13 — dev/test en v10 : dev 152/152, test 68/68, l'exact est saturé et le split ne bouge plus que par la couverture\n\n> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·\n> **Commit mesuré** : `710ec7f9` (branche `s/v7`) · **Verdict** : ✅ chiffres j … [33950 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Relecture ciblée de la fiche (typos, chiffres, liens)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"+?\\|??\\|TODO\\|None\\|XXX\" reports/rapport-dev-test-v10.md; echo '--- lignes ---'; wc -l reports/rapport-dev-test-v10.md reports/pensee-dev-test-v10.json; echo '--- liens ---'; python3 - <<'EOF'\nimport re, pathlib\np=pa … [383 caractères tronqués]`

  ```
170:- **1 R2 non intégrée** : `s037` (« Paul qui marche marche » ; la règle `precedent is None
314:  synthétique **+3,33** : la composition annule les deux. Par type, REL +? au test (0,9444
463:   (`qui`, `dont`, `where`…) au lieu de `precedent is None → SUB`. Vérifier `r241` : `when`
--- lignes ---
   490 reports/rapport-dev-test-v10.md
  7389 reports/pensee-dev-test-v10.json
  7879 total
--- liens ---
OK  ../tools/tests/linguistique/gold_split.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_split.py
OK  ../tools/tests/linguistique/evaluer_gold.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py
OK  ../tools/bloc_linguistique.py -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py
OK  pensee-dev-test-v10.json -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-dev-test-v10.json
OK  rapport-dev-test-v10.md -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md
OK  pensee-dev-test-v10.json -> /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-dev-test-v10.json
OK  ../tools/tests/linguistique/gold_split.py -> /home/stephane/Data
… [642 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Correction du typographe « REL +? » dans la fiche

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md", "offset": 306, "limit": 16}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md</path>
<type>file</type>
<content>
306: - **F1** : test **+0,78 point** (0,5836 contre 0,5890), mais c'est un **effet de
307:   composition**, pas une meilleure segmentation des cibles : le test est plus synthétique
308:   (30,3 % des cibles contre 19,6 %) et le synthétique a une F1 plus haute (0,6078 au test
309:   contre 0,5823 au réel) ; à source fixée, le réel gagne +0,35 point et le synthétique
310:   +1,74. Sur les types cibles, le test est **plus bas** : REL 0,7179 contre 0,7907 (−7,3),
311:   SUB 0,8571 contre 0,9247 (−6,8), GP 0,8571 contre 0,8553 (+0,2). La F1 globale ne mesure
312:   donc pas la généralisation de l'attachement ; elle mesure surtout GN/GV et la source.
313: - **Tête** : test **+0,07 point** (0,7337 contre 0,7330), masque un réel **−1,23** et un
314:   synthétique **+3,33** : la composition annule les deux. Par type, REL +? au test (0,9444
315:   contre 0,9573, −1,29), SUB +1,21, GP +0,66. Rien de significatif.
316: - **POS** : test **+1,09 point** (0,7656 contre 0,7547), exactement le motif de la v7 :
317:   l'anglais gagne (+3,97), le français recule (−0,46). La POS est
… [381 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md", "old_string": "  synthétique **+3,33** : la composition annule les deux. Par type, REL +? au test (0,9444\n  contre 0,9573, −1,29), SUB +1,21, GP +0,66. Rien de significatif.", "new_string": "  synthétiq … [150 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Validation locale des tableaux et de la structure de la fiche

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib, re\np = pathlib.Path('reports/rapport-dev-test-v10.md')\nlines = p.read_text(encoding='utf-8').splitlines()\nblocs=[]; cur=[]\nfor i,l in enumerate(lines,1):\n    if l.strip().startswith('|'):\n     … [594 caractères tronqués]`

  ```
tableaux 14
OK  ligne 57 lignes 5 pipes [11]
OK  ligne 69 lignes 4 pipes [16]
OK  ligne 80 lignes 5 pipes [14]
OK  ligne 95 lignes 8 pipes [8]
OK  ligne 110 lignes 5 pipes [8]
OK  ligne 116 lignes 7 pipes [9]
OK  ligne 141 lignes 21 pipes [9]
OK  ligne 180 lignes 14 pipes [5]
OK  ligne 232 lignes 6 pipes [19]
OK  ligne 244 lignes 5 pipes [7]
OK  ligne 269 lignes 11 pipes [12]
OK  ligne 332 lignes 6 pipes [17]
OK  ligne 339 lignes 6 pipes [5]
OK  ligne 386 lignes 5 pipes [6]
1 # B13 — dev/test en v10 : dev 152/152, test 68/68, l'exact est saturé et le split ne bouge plus que 
29 ## 1. Ce qui est mesuré
55 ## 2. Le split canonique
67 ### 2.1 Par langue
78 ### 2.2 Par type
93 ### 2.3 Le croisement fin
108 ### 2.4 Par source — et le confond synthétique/français
139 ### 2.5 Les 19 spans perdus
178 ## 3. L'équilibre du split
230 ## 4. La stabilité : trois découpages
295 ## 5. L'écart dev/test
326 ## 6. Comparaison v7 (`69bd865e`), audit v8 (`f908d7b0`), v9 (`160d08ca`)
355 ### 6.1 Trois énoncés de la fiche v10 à corriger
381 ### 6.2 La garde GP : un effet plus large que `r153`
396 ## 7. Contrôles négatifs
417 ## 8. Ce que ce banc ne dit pas — et ce qui pourrait le rendre faux
452 ## 9. L
… [27 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Trois corrections de forme (renvoi, libellé d'étendue, nom de l'audit)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='reports/rapport-dev-test-v10.md'\ns=open(p,encoding='utf-8').read()\n# 1) renvoi source au bon paragraphe\nold=\"mais c'est un **effet de source**,\\npas un effet de langue (voir § 2.5).\"\nnew=\"mais c'est un * … [648 caractères tronqués]`

  ```
ok
MM reports/pensee-audit-v10.json
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-quatre-modes.json
MM reports/rapport-audit-v10.md
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-spans-chunker.md
?? reports/pensee-dev-test-v10.json
?? reports/rapport-dev-test-v10.md
?? reports/rapport-s-paragraphes.md
  ```

### 🤖 Assistant

⏵ Vérification finale : porte tableaux (lecture seule ?) et cohérence JSON

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,40p' tools/porte-tableaux.sh", "description": "Inspect table door script"}`

  ```
#!/bin/bash
# porte-tableaux.sh — un tableau Markdown qui ne rend pas est un tableau qui n'existe PAS.
#
# POURQUOI CETTE PORTE EXISTE. Le 13/10, le premier tableau de `docs/etat-cerveau.md` s'affichait
# comme du TEXTE dans docwatch : une seule ligne (`| **C2 (cycle 2 régions)** | … |`) avait
# **4 cellules pour 5 colonnes** — un lien qui avait glissé d'une colonne. Le rendu (mistune,
# puis markdown_it, puis markdown) refuse alors le tableau ENTIER, sans rien dire : les 13 lignes
# disparaissent de la page et personne ne le voit, parce que le texte est toujours là, en gris.
#
# CE QU'ELLE VÉRIFIE (trois conditions, toutes nécessaires au rendu) :
#   1. l'en-tête et le séparateur d'un tableau ont le MÊME nombre de cellules ;
#   2. chaque ligne du corps a ce nombre de cellules ;
#   3. aucun `\|` ne subsiste : mistune ne le déséchappe NI dans un espace de code NI dans la
#      prose (il s'affiche alors littéralement). Pour une barre de valeur absolue dans du code,
#      on écrit `∣` (U+2223), qui rend partout et ne casse pas la lecture.
# Les tableaux DANS une citation (`> | … |`) sont valides et vérifiés aussi.
#
# CE QU'ELLE NE VÉRIFIE PAS : les tableaux « écrasés » sur une se
… [855 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Passage de la porte tableaux sur la seule fiche neuve

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CIBLES=\"reports/rapport-dev-test-v10.md\" bash tools/porte-tableaux.sh; echo \"exit=$?\"", "description": "Run table door on new report"}`

  ```
✅ 1 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3475 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-06)
exit=0
  ```

### 🤖 Assistant

⏵ Assertions finales sur le JSON (splits, 19 spans, comparaisons, validation)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-dev-test-v10.json'))\nassert d['meta']['commit']=='710ec7f9'\nassert d['meta']['sha'].startswith('710ec7f9')\nfor h in ('dev','test','tout'):\n    s=d['synthese'][h]\n  … [1624 caractères tronqués]`

  ```
dev {'phrases': 422, 'cibles': 163, 'labels': 152, 'exact': 152, 'couverture': 0.9325, 'f1': 0.5812, 'tete': 0.733, 'pos': 0.7547}
test {'phrases': 190, 'cibles': 76, 'labels': 68, 'exact': 68, 'couverture': 0.8947, 'f1': 0.589, 'tete': 0.7337, 'pos': 0.7656}
tout {'phrases': 612, 'cibles': 239, 'labels': 220, 'exact': 220, 'couverture': 0.9205, 'f1': 0.5836, 'tete': 0.7332, 'pos': 0.7581}
json.tool OK
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 16, in <module>
KeyError: 'par_source'
  ```

### 🤖 Assistant

⏵ Ajout de `spans.par_source` au JSON et reprise des assertions

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, collections, pathlib\np=pathlib.Path('reports/pensee-dev-test-v10.json')\nd=json.loads(p.read_text(encoding='utf-8'))\nd['spans']['par_source']=dict(collections.Counter(s['source'] for s in d['spans'][ … [1778 caractères tronqués]`

  ```
par_source {'reel': 5, 'synthetique': 14}
validation ecarts {'tout': 0.0, 'dev': 0.0, 'test': 0.0}
stabilite {'exact_taux_span': {'dev': 0.0, 'test': 0.0}, 'exact': {'dev': 18, 'test': 18}, 'labels': {'dev': 18, 'test': 18}, 'couverture': {'dev': 0.0325, 'test': 0.0603}, 'f1': {'dev': 0.0107, 'test': 0.0209}, 'tete': {'dev': 0.0069, 'test': 0.0131}, 'pos': {'dev': 0.0055, 'test': 0.0111}}
deltas v9 test {'labels': 1, 'exact': 1, 'couverture': 0.0131, 'f1': 0.0035, 'tete': 0.0014, 'pos': 0.0}
mc test couverture {'p05': 0.0143, 'mediane': 0.0494, 'p95': 0.1008} obs 0.0603 p 0.345
JSON OK 104535 octets
json.tool OK
  ```

### 🤖 Assistant

⏵ Dernier ajustement de prudence sur la formulation du rejeu (`generateur`)

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md", "new_string": "- **Rejeu des anciens commits** : les modules sont copiés dans `/tmp` avec `RACINE` du dépôt ;\n  le `generateur` S est celui du dépôt (**le même pour tous les rejeux**), et le gold n'a pa … [541 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md": file changed since it was read — re-read the file, then retry
  ```

### 🤖 Assistant

⏵ Relecture de la section concernée avant la dernière correction

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Rejeu des anciens commits\" reports/rapport-dev-test-v10.md", "description": "Locate replay sentence"}`

  ```
444:- **Rejeu des anciens commits** : les modules sont copiés dans `/tmp` avec `RACINE` du dépôt ;
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md", "limit": 8, "offset": 444}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md</path>
<type>file</type>
<content>
444: - **Rejeu des anciens commits** : les modules sont copiés dans `/tmp` avec `RACINE` du dépôt ;
445:   le `generateur` S est celui du dépôt (identique entre les commits), et le gold n'a pas
446:   changé entre `69bd865e` et `710ec7f9` (vérifié : aucun diff de `tools/tests/linguistique/`).
447:   Les valeurs publiées sont reproduites, ce qui valide la comparaison.
448: - **Les 17 inatteignables** sont la classification de l'audit R1/R3, pas un jugement nouveau :
449:   4 d'entre eux sont « hors périmètre » (récupérables en changeant le gold/le lexique), 13 sont
450:   non récupérables sans changer le gold. `s037` et `r303` ne sont pas dans ces 17.
451: 

(Showing lines 444-451 of 490. Use offset=452 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md", "new_string": "  le `generateur` S est celui du dépôt (**le même pour tous les rejeux**), et le gold n'a pas\n  changé entre `69bd865e` et `710ec7f9` (vérifié : aucun diff de `tools/tests/linguistique/`) … [205 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Contrôle des caractères de contrôle et repassage de la porte tableaux

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\nfor f in ('reports/rapport-dev-test-v10.md','reports/pensee-dev-test-v10.json'):\n    b=pathlib.Path(f).read_bytes()\n    ctrl=[(i,hex(x)) for i,x in enumerate(b) if x<32 and x not in (9,10,13)]\n   … [214 caractères tronqués]`

  ```
reports/rapport-dev-test-v10.md control chars [(31613, '0x8')] count 1
reports/pensee-dev-test-v10.json control chars [] count 0
  ✅ 1 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3475 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-06)
exit=0
  ```

### 🤖 Assistant

⏵ Suppression du caractère de contrôle `\x08` dans la fiche

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-dev-test-v10.md')\nb=p.read_bytes()\ni=b.find(b'\\x08')\nprint('context:', repr(b[i-80:i+80].decode('utf-8', errors='replace')))\nb=b.replace(b'\\x08', b'')\np.write_ … [342 caractères tronqués]`

  ```
context: "ignables** sont la classification de l'audit R1/R3, pas un jugement nouveau :\n  \x084 d'entre eux sont « hors périmètre » (récupérables en changeant le gold/"
remaining control chars: []
line: "  4 d'entre eux sont « hors périmètre » (récupérables en changeant le gold/le lexique), 13 sont"
  ```

### 🤖 Assistant

⏵ Derniers contrôles (porte tableaux, statut, tailles) avant remontée au parent

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && CIBLES=\"reports/rapport-dev-test-v10.md\" bash tools/porte-tableaux.sh >/tmp/v10/porte_tableaux.log 2>&1; echo \"porte tables exit=$?\"; tail -3 /tmp/v10/porte_tableaux.log; echo '---'; wc -l -w reports/rapport-dev-test-v10.md; ls - … [416 caractères tronqués]`

  ```
porte tables exit=0
  ✅ 1 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3475 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-06)
---
  490  6077 reports/rapport-dev-test-v10.md
-rw-r--r--. 1 stephane stephane 144821  6 nov 00:54 reports/pensee-dev-test-v10.json
-rw-------. 1 stephane stephane  34289  6 nov 00:56 reports/rapport-dev-test-v10.md
--- status (mes fichiers) ---
?? reports/pensee-dev-test-v10.json
?? reports/rapport-dev-test-v10.md
--- status code/gold ---
--- head ---
653a7981
  ```

### 🤖 Assistant

⏵ Le parent a commité l'essai (HEAD 653a7981) — vérification de l'état courant

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -5; echo '--- HEAD stat ---'; git show --stat --oneline HEAD | head -15; echo '--- module diff depuis 710ec7f9 ---'; git diff --stat 710ec7f9..HEAD -- tools/bloc_linguistique.py; echo '--- mesure HEAD ---'; python3  … [1013 caractères tronqués]`

  ```
653a7981 B13 — LES DEUX DERNIÈRES RÉGRESSIONS (s037, r303) : EXACT 221/221 (1,0000), COUVERTURE 0,9247, 18 SPANS ; AUDIT V10 INTÉGRÉ, V10 CORRIGÉE ; 183/183
68a8717b JOURNAL — LE 06/11 AU FORMAT DE L'INDEX (EN-TÊTE, LIENS, BLOC NOTES)
41cae3e5 JOURNAL — LE 06/11 S'OUVRE SUR LA NUIT DU DÉCOUPAGE : 220/220, COUVERTURE 0,9205, 19 SPANS
4d34c37a PILOTAGE — LES VAGUES 5 À 7 (AUDITS V7/V8, R1/R3, TOP-K, V10) DOCUMENTÉES AU PLAN-TRAVAIL
77ed0856 THÉORIE ET JOURNAL — LE DÉCOUPAGE D'ABORD : LA COUVERTURE EST UN PLAFOND, UN GOLD SE VÉRIFIE AVANT DE JUGER
--- HEAD stat ---
653a7981 B13 — LES DEUX DERNIÈRES RÉGRESSIONS (s037, r303) : EXACT 221/221 (1,0000), COUVERTURE 0,9247, 18 SPANS ; AUDIT V10 INTÉGRÉ, V10 CORRIGÉE ; 183/183
 docs/pilotage/en-cours.md                          |    4 +-
 journal/2026-11-06/README.md                       |   11 +-
 journal/2026-11-06/distribue.md                    |    9 +-
 journal/README.md                                  |    8 +-
 .../3fb87dc7-7d24-42e2-a68e-e37e2734b755/digest.md |  297 +++++
 .../rapport.md                                     |   22 +-
 journal/sessions/MANIFEST.md                       |    8 +-
 .../e181ce02-cd50-488a-a6be-e84b79d4
… [933 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mise à jour de la note d'arbre : l'essai est désormais commité en 653a7981

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md", "limit": 28, "offset": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md</path>
<type>file</type>
<content>
1: # B13 — dev/test en v10 : dev 152/152, test 68/68, l'exact est saturé et le split ne bouge plus que par la couverture
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
4: > **Commit mesuré** : `710ec7f9` (branche `s/v7`) · **Verdict** : ✅ chiffres justes,
5: > **3 énoncés de la fiche v10 à corriger**, et une **régression nouvelle** (`r303`).
6: > **dev 152/152 (1,0000)**, **test 68/68 (1,0000)**, tout **220/220** ; couverture
7: > **0,9325 / 0,8947 / 0,9205** ; F1 **0,5812 / 0,5890 / 0,5836** (vivant 612) ;
8: > tête **0,7330 / 0,7337 / 0,7332** ; POS **0,7547 / 0,7656 / 0,7581**. **19 spans**
9: > restants (9 REL, 6 SUB, 4 GP). Sur les trois découpages `%3==0/1/2`, l'exact/labels
10: > reste **1,0 partout** ; l'étendue est de **0** sur le taux exact, **3,25 pts (dev) /
11: > 6,03 pts (test)** sur la couverture, **1,07 / 2,09** sur la F1, **0,69 / 1,31** sur la
12: > tête, **0,55 / 1,11** sur la POS — toutes dans la bande Monte-Carlo (p 0,30–0,86).
13: > L'écart dev/test n'est plus un écart d'exactitude (**0**) ; la 
… [1140 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Arbre mouvant\\|Re-mesurer quand\" reports/rapport-dev-test-v10.md", "description": "Locate tree note bullets"}`

  ```
435:- **Arbre mouvant** : la mesure est épinglée sur `710ec7f9` ; `HEAD` est `68a8717b` et le
470:6. **Re-mesurer quand le module sera stabilisé** : l'arbre sale est une exploration
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md", "limit": 14, "offset": 435}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md", "limit": 6, "offset": 468}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md</path>
<type>file</type>
<content>
435: - **Arbre mouvant** : la mesure est épinglée sur `710ec7f9` ; `HEAD` est `68a8717b` et le
436:   module est sale. L'arbre sale essaie de corriger `s037` (R2) et `r303` (retrait de la garde
437:   d'adverbe), mais il **perd `g017` et `r241`** : `g017` (« would come yesterday ») veut
438:   l'adverbe **exclu**, `r288` (« comes tomorrow ») veut l'adverbe **inclus** ; `r241`
439:   (« The day when we left ») devient SUB alors que le gold attend REL, parce que `est_sub`
440:   ajoute `when` aux subordonnants. Le couple `g017`/`r288` est un **ballant** : une garde
441:   unique ne peut pas satisfaire les deux sans une distinction sémantique (adverbe de phrase
442:   vs complément du prédicat, ou lexique temporel). L'arbre sale donne **221/221, 18 spans**,
443:   mais ce n'est pas l'état mesuré ici.
444: - **Rejeu des anciens commits** : les modules sont copiés dans `/tmp` avec `RACINE` du dépôt ;
445:   le `generateur` S est celui du dépôt (**le même pour tous les rejeux**), et le gold n'a pas
446:   changé entre `69bd865e` et `710ec7f9` (vérifié : aucun diff de `
… [276 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md</path>
<type>file</type>
<content>
468:    la source** avant de conclure sur une langue. La couverture est la mesure primaire ; le
469:    taux exact est saturé.
470: 6. **Re-mesurer quand le module sera stabilisé** : l'arbre sale est une exploration
471:    (`g017`/`r241`), pas l'état de la fiche.
472: 
473: ## 10. Fichiers

(Showing lines 468-473 of 490. Use offset=474 to continue.)
</content>
  ```

### 🤖 Assistant

⏵ Mise à jour de l'ancrage d'arbre dans la fiche (HEAD 653a7981)

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md", "new_string": "> **Ancrage d'arbre.** La mesure est faite sur le **module épinglé de `710ec7f9`** (copie\n> `/tmp`, `RACINE` du dépôt), pas sur l'arbre courant : depuis, `HEAD` a avancé à `653a7981`\n> ( … [1300 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md", "limit": 14, "offset": 438}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md</path>
<type>file</type>
<content>
438:   type (y compris les non-cibles) et inclut GN/GV dans l'agrégat. Elle ne remplace pas
439:   l'exact/couverture. Les types ADJ/ADV/PONCT, jamais prédits, pèsent 74 fn.
440: - **Arbre mouvant** : la mesure est épinglée sur `710ec7f9` ; `HEAD` est `68a8717b` et le
441:   module est sale. L'arbre sale essaie de corriger `s037` (R2) et `r303` (retrait de la garde
442:   d'adverbe), mais il **perd `g017` et `r241`** : `g017` (« would come yesterday ») veut
443:   l'adverbe **exclu**, `r288` (« comes tomorrow ») veut l'adverbe **inclus** ; `r241`
444:   (« The day when we left ») devient SUB alors que le gold attend REL, parce que `est_sub`
445:   ajoute `when` aux subordonnants. Le couple `g017`/`r288` est un **ballant** : une garde
446:   unique ne peut pas satisfaire les deux sans une distinction sémantique (adverbe de phrase
447:   vs complément du prédicat, ou lexique temporel). L'arbre sale donne **221/221, 18 spans**,
448:   mais ce n'est pas l'état mesuré ici.
449: - **Rejeu des anciens commits** : les modules sont copiés dans `/tmp` avec `RACINE` du dépô
… [274 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md", "new_string": "- **Arbre mouvant** : la mesure est épinglée sur `710ec7f9` ; `HEAD` a avancé à `653a7981`,\n  qui committe l'essai R2 + retrait de la garde d'adverbe. Cet état corrige `s037` (R2) et\n  ` … [1490 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Re-mesurer quand\" reports/rapport-dev-test-v10.md", "description": "Locate final point"}`

  ```
476:6. **Re-mesurer quand le module sera stabilisé** : l'arbre sale est une exploration
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md", "limit": 4, "offset": 476}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md</path>
<type>file</type>
<content>
476: 6. **Re-mesurer quand le module sera stabilisé** : l'arbre sale est une exploration
477:    (`g017`/`r241`), pas l'état de la fiche.
478: 
479: ## 10. Fichiers

(Showing lines 476-479 of 496. Use offset=480 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md", "new_string": "6. **Re-mesurer quand le module sera stabilisé** : l'état `653a7981` est une exploration\n   (`g017`/`r241`), pas l'état de la fiche.", "old_string": "6. **Re-mesurer quand le module sera  … [93 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-dev-test-v10.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Mise à jour du JSON (ancrage 653a7981, réserve d'arbre)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib\np=pathlib.Path('reports/pensee-dev-test-v10.json')\nd=json.loads(p.read_text(encoding='utf-8'))\nd['meta']['ancrage']=\"commit 710ec7f9 ; HEAD ultérieur 653a7981 (essai R2 + retrait de la gard … [1255 caractères tronqués]`

  ```
ancrage: commit 710ec7f9 ; HEAD ultérieur 653a7981 (essai R2 + retrait de la garde d'adverbe, commité) non mesuré ici
reserve: l'arbre a bougé après la mesure : HEAD 653a7981 (68a8717b puis 653a7981) ; l'essai R2 + retrait de la garde d'adverbe y est commité. Cet état donne, mesuré, dev 152/152, test 69/69, tout 221/221, couverture 0,9247, F1 0,5843, tête 0,7330, POS 0,7581, 18 spans (g017, r035, r241, r255, r264, s010, s027, s035, s044, s061, s065, s112, s114, s125, s141, s146, s148, s160 ; s037, r303, r288 récupérés) — ce n'est pas l'état 710ec7f9 mesuré ici
octets 145289
json OK
  ```

