# Session DSH — relecture

- identifiant : `b9ea3904-889c-4497-a781-694da7d4987c`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 14:47:27
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **auditer la qualité du gold anglais** (210 phrases sur 612), parce que beaucoup d'échecs d'attachement sont anglais.

Contexte : `tools/tests/linguistique/gold_reel.py` (432 phrases réelles, 20 fr / 20 en par bloc ; `gold_reel.json` généré), `tools/tests/linguistique/evaluer_gold.py` (`charger`), `tools/bloc_linguistique.py` (`Heuristique`). Les échecs d'attachement restants (`reports/rapport-pensee-attachement-v2.md`) et les spans perdus (`reports/rapport-pensee-spans.md`) sont majoritairement anglais.

À faire :
1. Sur les phrases anglaises du gold : vérifie la cohérence interne (POS des mots vs segments, spans des segments vs texte, rôles, cibles) ; liste les annotations suspectes (par ex. un verbe tagué NOUN, un GN qui avale un verbe, un span qui ne correspond pas au texte).
2. Mesure, pour les phrases anglaises seules et françaises seules : POS exactitude, F1 syntagmes, attachement exact/top-k, spans perdus — avec `Heuristique()`.
3. Vérifie si les cibles anglaises sont des têtes réduites (`saw`, `talks`) ou des textes complets, et si le POS gold anglais est fiable (compare `_est_verbe` au POS gold sur les cibles anglaises).
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-gold-anglais.md` (fiche : verdict, tableaux par langue, annotations suspectes, contrôles, limites, recommandation) et `reports/pensee-gold-anglais.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé : nombre d'annotations suspectes, écarts fr/en, recommandation.
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

⏵ Discovering the linguistic evaluation code and gold data files

- **bash** `{"command": "git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet status --short | head -30; git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet branch --show-current", "description": "Check git status and branch"}`

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
D  journal/sessions/3f8f2bb8-781b-44a6-9e14-58025004b6fc/digest.md
D  journal/sessions/3f8f2bb8-781b-44a6-9e14-58025004b6fc/rapport.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/digest.md
D  journal/sessions/53bc3288-f2c1-4a7d-b1db-88d794074f70/rapport.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/digest.md
D  journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/rapport.md
D  journal/sessions/65495a29-10c0-4571-96be-e7729f1efe
… [387 caractères tronqués]
  ```

- **bash** `{"command": "ls /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/ /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/ | head -60", "description": "List linguistic test and reports dirs"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/:
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
bilan-mu
… [76 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/tests/linguistique/ && echo --- && ls reports/ | grep -i -E \"pensee|gold|linguist\"", "description": "List linguistique dir and relevant reports"}`

  ```
anaphore.py
classement_cible.py
evaluer_gold.py
gold_gele.json
gold.json
gold.py
gold_reel.json
gold_reel.py
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
test_bloc_linguistique.py
---
bloc-linguistique.json
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
pensee-anaphore-kappa.
… [11259 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/tests/linguistique/gold_reel.py tools/tests/linguistique/evaluer_gold.py tools/bloc_linguistique.py reports/rapport-pensee-attachement-v2.md reports/rapport-pensee-spans.md 2>&1", "description": "Line counts of key files" … [1 caractères tronqués]`

  ```
1385 tools/tests/linguistique/gold_reel.py
   287 tools/tests/linguistique/evaluer_gold.py
  1949 tools/bloc_linguistique.py
    91 reports/rapport-pensee-attachement-v2.md
    78 reports/rapport-pensee-spans.md
  3790 total
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-v2.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-spans.md"}`

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
… [14748 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-v2.md</path>
<type>file</type>
<content>
1: # B13 — l'attachement v2 : exact 0,8483 → 0,9448, top-k strict 0,6069 → 0,9724
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **180/180 portes** : trois corrections **mesurées**, issues de trois sous-agents indépendants :
5: > (1) la règle du **segment précédent** (un SUB après un GV est une complétive → cible = le verbe ;
6: > après un GN, une relative → cible = l'antécédent), (2) les **têtes des candidats** de S
7: > (« « … » → Le livre » → `livre`), (3) le **lexique verbal anglais** complété. Sur les 145
8: > segments au bon span : **exact 123 → 137 (0,9448)**, top1 **126 → 140 (0,9655)**, top-k
9: > **134 → 142 (0,9793)**, **top-k strict 88 → 141 (0,9724)**.
10: >
11: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
12: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
13: > [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) (`CONVENTION_CIBLE`),
14: > [`autotest.py`](../tools/pensee/autotest.py) ; fiches des sous-agents :
15: >
… [4730 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-spans.md</path>
<type>file</type>
<content>
1: # B13 — les 94 spans : 48 REL, 33 SUB, 13 GP (état courant ; 93/12 après le correctif GP, avant le lexique élargi)
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **169/169 portes** : les échecs d'attachement par **span** (94 à l'état courant ; **93** après le correctif GP, avant le lexique élargi de `a408a909`) sont
5: > **48 REL**, **33 SUB** et **13 GP** — les subordonnées ne sont **pas produites** (65 cas) ou le
6: > sont avec un span plus large (24 à l'état courant ; 25 après le correctif GP). Le correctif testé — borner le GP au verbe et au relatif —
7: > gagne **un span** (couverture 0,6067 → 0,6109, F1 0,2864 → 0,2869) mais **perd une cible** :
8: > le total des échecs ne bouge pas (107).
9: >
10: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
11: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
12: > [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-spans.json`](pensee-spans.json).
13: 
14: ## 1. Les 94 spans
15: 
16: | type | é
… [3134 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel.py", "limit": 180}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_reel.py</path>
<type>file</type>
<content>
1: """gold_reel.py — 200 phrases réelles (20 françaises, 20 anglaises).
2: 
3: Elles ne sont pas des phrases du bloc ni du générateur : elles sont écrites après, avec leurs
4: POS, leurs segments GN/GV/GP/REL/SUB et leur pragmatique. Le fichier `gold_reel.json` est généré
5: par `construire()` ; le gold réel total devient **200 phrases** (20 de `gold.py` + 180).
6: """
7: from __future__ import annotations
8: 
9: import json
10: import pathlib
11: 
12: # La **convention des cibles** d'attachement. Le gold ne la documentait pas ; elle a été lue
13: # sur les données le 2026-11-05 (T169/T172) et la voici, explicitement :
14: #
15: #   - **REL** : la cible est l'**antécédent** — la tête nominale du GN à gauche
16: #     (« l'homme que j'ai vu » → `homme`) ;
17: #   - **SUB** : la cible est le **verbe gouverneur** (le POS gold donne 69/69 cibles VERB :
18: #     « cette étoile écoute que Lucas trouve » → `écoute`), pas un antécédent ;
19: #   - **GP** : la cible est le **verbe qui gouverne** le complément (« au ballon » → `joue`),
20: #     ou, pour un génitif,
… [13575 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nd=json.load(open('tools/tests/linguistique/gold_reel.json'))\nprint(type(d), list(d.keys()) if isinstance(d,dict) else len(d))\nps=d['phrases']\nprint('n',len(ps))\nprint('keys', ps[0].keys())\nimport coll … [180 caractères tronqués]`

  ```
<class 'dict'> ['version', 'source', 'note', 'phrases']
n 432
keys dict_keys(['id', 'langue', 'texte', 'mots', 'segments', 'pragma', 'source'])
Counter({'fr': 228, 'en': 204})
{
 "id": "r001",
 "langue": "fr",
 "texte": "Le chien mange une pomme.",
 "mots": [
  {
   "texte": "Le",
   "pos": "DET",
   "debut": 0,
   "fin": 2
  },
  {
   "texte": "chien",
   "pos": "NOUN",
   "debut": 3,
   "fin": 8
  },
  {
   "texte": "mange",
   "pos": "VERB",
   "debut": 9,
   "fin": 14
  },
  {
   "texte": "une",
   "pos": "DET",
   "debut": 15,
   "fin": 18
  },
  {
   "texte": "pomme",
   "pos": "NOUN",
   "debut": 19,
   "fin": 24
  }
 ],
 "segments": [
  {
   "type": "GN",
   "texte": "Le chien",
   "role": "agent",
   "debut": 0,
   "fin": 8
  },
  {
   "type": "GV",
   "texte": "mange",
   "role": "prédicat",
   "debut": 9,
   "fin": 14
  },
  {
   "type": "GN",
   "texte": "une pomme",
   "role": "patient",
   "debut": 15,
   "fin": 24
  }
 ],
 "pragma": {
  "acte": "assertion"
 },
 "source": "reel"
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport sys, collections\nsys.path.insert(0,'tools/tests/linguistique')\nimport evaluer_gold as eg\nps=eg.charger()\nprint('total',len(ps))\nprint(collections.Counter((p['source'],p['langue']) for p in ps))\nprint('lang … [108 caractères tronqués]`

  ```
total 612
Counter({('reel', 'fr'): 228, ('reel', 'en'): 204, ('synthetique', 'fr'): 160, ('hand', 'fr'): 14, ('hand', 'en'): 6})
langues Counter({'fr': 402, 'en': 210})
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -80 tools/tests/linguistique/gold_reel.py", "description": "Show tail of gold_reel.py"}`

  ```
('r423', 'fr', 'Tu viens demain.',
     [('Tu', 'PRON'), ('viens', 'VERB'), ('demain', 'ADV'), ('.', 'PONCT')],
     [('GN', 'Tu', 'agent'), ('GV', 'viens', 'prédicat'), ('ADV', 'demain', 'temps'), ('PONCT', '.', 'ponctuation')], {'acte': 'assertion'}),
    ('r424', 'fr', 'Il mange.',
     [('Il', 'PRON'), ('mange', 'VERB'), ('.', 'PONCT')],
     [('GN', 'Il', 'agent'), ('GV', 'mange', 'prédicat'), ('PONCT', '.', 'ponctuation')], {'acte': 'assertion'}),
    ('r425', 'fr', 'Elle dort.',
     [('Elle', 'PRON'), ('dort', 'VERB'), ('.', 'PONCT')],
     [('GN', 'Elle', 'agent'), ('GV', 'dort', 'prédicat'), ('PONCT', '.', 'ponctuation')], {'acte': 'assertion'}),
    ('r426', 'fr', 'Ils partent.',
     [('Ils', 'PRON'), ('partent', 'VERB'), ('.', 'PONCT')],
     [('GN', 'Ils', 'agent'), ('GV', 'partent', 'prédicat'), ('PONCT', '.', 'ponctuation')], {'acte': 'assertion'}),
    ('r427', 'en', 'You come tomorrow.',
     [('You', 'PRON'), ('come', 'VERB'), ('tomorrow', 'ADV'), ('.', 'PONCT')],
     [('GN', 'You', 'agent'), ('GV', 'come', 'prédicat'), ('ADV', 'tomorrow', 'temps'), ('PONCT', '.', 'ponctuation')], {'acte': 'assertion'}),
    ('r428', 'fr', 'Il pleut.',
     [('Il', 'PRON'), ('pl
… [4050 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"_est_verbe\\|^class Heuristique\\|def analyser\\|VERBES\\|LEXIQUE\" tools/bloc_linguistique.py | head -60", "description": "Locate Heuristique and verb lexicon"}`

  ```
133:    def analyser(self, texte: str, langue: str | None = None,
218:    scores = {l: len(mots & set(LEXIQUES[l])) / max(1, len(mots)) for l in LEXIQUES}
273:LEXIQUES = {
319:VERBES = {
369:VERBES_IMPERATIFS = set("va viens prends fais dis regarde écoute donne cherche trouve ouvre ferme "
374:VERBES_CONNUS = set("""
431:def _est_verbe(mot: str) -> bool:
436:    if n in VERBES_CONNUS:
441:        if n.endswith(suf) and n[:-len(suf)] in VERBES_CONNUS:
445:        if n.endswith(suf) and (n[:-len(suf)] + "er") in VERBES_CONNUS:
475:class Heuristique:
557:        if n in VERBES.get(langue, VERBES["fr"]):
630:            if _est_verbe(m) and _normaliser(m) not in AUXILIAIRES:
649:            if _est_verbe(m) and _normaliser(m) not in AUXILIAIRES:
652:            if _est_verbe(m):
766:                       and not _est_verbe(mots[j][2])
796:    def analyser(self, texte: str, langue: str | None = None,
856:                    "ordre" if premier.casefold() in VERBES_IMPERATIFS else "assertion")
1033:    def analyser(self, texte: str, langue: str | None = None,
1102:    def analyser(self, texte: str, langue: str | None = None,
1212:    def analyser(self, texte: str, langue: str | None = No
… [338 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nfor f in ['gold.json','gold_gele.json','gold_synthetique.json']:\n    d=json.load(open('tools/tests/linguistique/'+f))\n    print(f, list(d.keys()), len(d['phrases']))\n    p=d['phrases'][0]\n    print(' k … [175 caractères tronqués]`

  ```
gold.json ['version', 'phrases', 'note'] 20
 keys ['id', 'langue', 'texte', 'mots', 'segments', 'pragma']
 langues Counter({'fr': 14, 'en': 6})
gold_gele.json ['gele', 'phrases'] 602
 keys ['id', 'langue', 'texte', 'mots', 'segments', 'pragma', 'source']
 langues Counter({'fr': 394, 'en': 208})
gold_synthetique.json ['version', 'source', 'graine', 'note', 'phrases'] 160
 keys ['id', 'langue', 'texte', 'pragma', 'source', 'mots', 'segments']
 langues Counter({'fr': 160})
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '250,470p' tools/bloc_linguistique.py", "description": "Read lexicons and _est_verbe"}`

  ```
for prefixe, code in prefixes:
        if prefixe in nom:
            return code
    return ""


def detecter_script(texte: str) -> str:
    c = collections.Counter(_script_char(ch) for ch in texte if ch.isalpha())
    c.pop("", None)
    if not c:
        return SCRIPT_NEUTRE
    if c.get("Jpan", 0) or (c.get("Hani", 0) and (c.get("Jpan", 0) or c.get("Hang", 0))):
        return "Jpan"
    if c.get("Hang", 0):
        return "Hang"
    if c.get("Hani", 0):
        return "Hani"
    return c.most_common(1)[0][0]


# --------------------------------------------------------------------------- lexiques


LEXIQUES = {
    "fr": set("le la les l un une des de du d à au aux et ou mais donc or ni car que qui quoi "
              "dont où je tu il elle on nous vous ils elles me te se lui leur mon ma mes ton "
              "ta tes son sa ses ce cet cette ces est sont était étaient être avoir ai as a "
              "avons avez ont ne pas plus jamais rien très dans sur sous avec pour par en".split()),
    "en": set("the a an of to and or but nor for so yet in on at by with from as is are was "
              "were be been being have has had do does did not no never this that these those "
 
… [13337 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '470,960p' tools/bloc_linguistique.py", "description": "Read Heuristique implementation"}`

  ```
# --------------------------------------------------------------------------- heuristique


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
        motif = re.compile(r"\b[ldmtsnLDMT
… [24536 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections\nd=json.load(open('tools/tests/linguistique/gold_reel.json'))\nps=d['phrases']\nen=[p for p in ps if p['langue']=='en']\nprint('n en',len(en),'n fr',len(ps)-len(en) … [448 caractères tronqués]`

  ```
n en 204 n fr 228
ids dupliques: []
textes dupliques: [('Le vent souffle fort.', 2), ('La voiture roule vite.', 2), ('Paul sees Marie; he speaks to her.', 2)]
premiers/derniers ids: ['r001', 'r002', 'r003'] ['r420', 'r421', 'r422']
r021 | The dog eats an apple.
r022 | The girl reads the newspaper.
r023 | We love music.
r024 | The sun shines.
r025 | She talks to her brother.
r026 | The students listen to the teacher.
r027 | The cat sleeps on the chair.
r028 | It rains since yesterday.
r029 | I do not understand.
r030 | You come tomorrow?
r031 | The train leaves at noon.
r032 | The car is fast.
r033 | They bought a house.
r034 | The book that I read is exciting.
r035 | The film she talks about is out.
r036 | She is maybe tired.
r037 | We must work.
r038 | The mouse is ready to eat.
r039 | The wind blows hard.
r040 | The children play in the park.
r061 | The boy plays with the ball.
r062 | The mother prepares the meal.
r063 | We listen to the radio.
r064 | The teacher talks to the students.
r065 | She watches television.
r066 | The cat drinks milk.
r067 | The flowers grow in the garden.
r068 | He writes a letter to his sister.
r069 | The baby sleeps deeply.
r070 | We leave on vacation
… [6229 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, re\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nfor lang in ('en','fr'):\n    print('='*20, lang, '='*20)\n    for p in ps:\n         … [1852 caractères tronqués]`

  ```
==================== en ====================
==================== fr ====================
r413 'Ne parle-t-elle pas ?'
    ('GAP_NONTRIVIAL', "' -t-  '")
r415 'Ne chante-t-il pas ?'
    ('GAP_NONTRIVIAL', "' -t-  '")
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, re\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nROLES={'GN':{'agent','patient','destinataire','lieu','temps','theme','groupe nominal' … [3954 caractères tronqués]`

  ```
========================= en =========================
r063 'We listen to the radio.'
    ('ROLE_INATTENDU', 'GP', 'to the radio', 'cible')
r077 'The dog barks at the postman.'
    ('ROLE_INATTENDU', 'GP', 'at the postman', 'cible')
r153 'We wait for the bus.'
    ('ROLE_INATTENDU', 'GP', 'for the bus', 'cible')
r168 'She listens to music.'
    ('ROLE_INATTENDU', 'GP', 'to music', 'cible')
r204 'The man who speaks is my father.'
    ('ROLE_INATTENDU', 'REL', 'who speaks', 'sujet')
    ('ROLE_INATTENDU', 'GN', 'my father', 'attribut')
r214 'The book that I read is good.'
    ('ROLE_INATTENDU', 'REL', 'that I read', 'objet')
r215 'When it rains, I stay.'
    ('ROLE_INATTENDU', 'SUB', 'When it rains', 'temps')
r217 'The student whom I mention is absent.'
    ('ROLE_INATTENDU', 'REL', 'whom I mention', 'objet')
r218 'Although it is late, he works.'
    ('ROLE_INATTENDU', 'SUB', 'Although it is late', 'concession')
r220 'The cat that sleeps is black.'
    ('ROLE_INATTENDU', 'REL', 'that sleeps', 'sujet')
r236 'The village where I live is small.'
    ('ROLE_INATTENDU', 'REL', 'where I live', 'lieu')
r237 'If you come, we will leave.'
    ('ROLE_INATTENDU', 'SUB', 'If you come', 'conditio
… [8235 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nen=[p for p in ps if p['langue']=='en']\nfor p in en:\n    toks=' '.join(f\"{m['texte']}/{m['pos']}\"  … [95 caractères tronqués]`

  ```
r021 | The/DET dog/NOUN eats/VERB an/DET apple/NOUN
r022 | The/DET girl/NOUN reads/VERB the/DET newspaper/NOUN
r023 | We/PRON love/VERB music/NOUN
r024 | The/DET sun/NOUN shines/VERB
r025 | She/PRON talks/VERB to/PREP her/DET brother/NOUN
r026 | The/DET students/NOUN listen/VERB to/PREP the/DET teacher/NOUN
r027 | The/DET cat/NOUN sleeps/VERB on/PREP the/DET chair/NOUN
r028 | It/PRON rains/VERB since/PREP yesterday/ADV
r029 | I/PRON do/AUX not/ADV understand/VERB
r030 | You/PRON come/VERB tomorrow/ADV
r031 | The/DET train/NOUN leaves/VERB at/PREP noon/NOUN
r032 | The/DET car/NOUN is/AUX fast/ADJ
r033 | They/PRON bought/VERB a/DET house/NOUN
r034 | The/DET book/NOUN that/CONJ I/PRON read/VERB is/AUX exciting/ADJ
r035 | The/DET film/NOUN she/PRON talks/VERB about/PREP is/AUX out/ADV
r036 | She/PRON is/AUX maybe/ADV tired/ADJ
r037 | We/PRON must/AUX work/VERB
r038 | The/DET mouse/NOUN is/AUX ready/ADJ to/PREP eat/VERB
r039 | The/DET wind/NOUN blows/VERB hard/ADV
r040 | The/DET children/NOUN play/VERB in/PREP the/DET park/NOUN
r061 | The/DET boy/NOUN plays/VERB with/PREP the/DET ball/NOUN
r062 | The/DET mother/NOUN prepares/VERB the/DET meal/NOUN
r063 | We/PRON listen/VERB to/PREP the/
… [10989 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nen=[p for p in ps if p['langue']=='en']\nfor p in en:\n    segs=' | '.join(f\"{s['type']}[{s['texte']} … [181 caractères tronqués]`

  ```
r021 : GN[The dog]/agent | GV[eats]/prédicat | GN[an apple]/patient
r022 : GN[The girl]/agent | GV[reads]/prédicat | GN[the newspaper]/patient
r023 : GN[We]/agent | GV[love]/prédicat | GN[music]/patient
r024 : GN[The sun]/agent | GV[shines]/prédicat
r025 : GN[She]/agent | GV[talks]/prédicat | GP[to her brother]/destinataire→talks
r026 : GN[The students]/agent | GV[listen]/prédicat | GP[to the teacher]/destinataire→listen
r027 : GN[The cat]/agent | GV[sleeps]/prédicat | GP[on the chair]/lieu→sleeps
r028 : GN[It]/agent | GV[rains]/prédicat | GP[since yesterday]/temps→rains
r029 : GN[I]/agent | GV[do not understand]/prédicat
r030 : GN[You]/agent | GV[come]/prédicat
r031 : GN[The train]/agent | GV[leaves]/prédicat | GP[at noon]/temps→leaves
r032 : GN[The car]/agent | GV[is fast]/prédicat
r033 : GN[They]/agent | GV[bought]/prédicat | GN[a house]/patient
r034 : GN[The book]/patient | REL[that I read]/qualité→book | GV[is exciting]/prédicat
r035 : GN[The film]/patient | REL[she talks about]/qualité→film | GV[is out]/prédicat
r036 : GN[She]/agent | GV[is maybe tired]/prédicat
r037 : GN[We]/agent | GV[must work]/prédicat
r038 : GN[The mouse]/agent | GV[is ready]/prédicat | GP[to eat]/but→re
… [15193 caractères tronqués]
  ```

