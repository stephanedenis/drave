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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, re\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nfor lang in ('en','fr'):\n    print('='*20,lang,'='*20)\n    miss=collections.Counter … [1011 caractères tronqués]`

  ```
==================== en ====================
segments sans cible: {'GP': 6}
tokens hors segment: 23 types: {('PRON', 'it'): 9, ('ADV', 'tomorrow'): 2, ('ADV', 'hard'): 1, ('ADV', 'deeply'): 1, ('ADV', 'fast'): 1, ('NOUN', 'morning'): 1, ('ADV', 'loudly'): 1, ('CONJ', 'and'): 1, ('CONJ', 'so'): 1, ('CONJ', 'but'): 1, ('AUX', 'Do'): 1, ('PRON', 'them'): 1, ('ADV', 'down'): 1, ('VERB', 'do'): 1}
   ('r328', 'SANS_CIBLE', 'GP', 'on the table')
   ('r336', 'SANS_CIBLE', 'GP', 'to her')
   ('r342', 'SANS_CIBLE', 'GP', 'to her')
   ('r358', 'SANS_CIBLE', 'GP', 'to her')
   ('r363', 'SANS_CIBLE', 'GP', 'on the table')
   ('r367', 'SANS_CIBLE', 'GP', 'to him')
==================== fr ====================
segments sans cible: {'GP': 3, 'SUB': 1}
tokens hors segment: 40 types: {('ADV', 'Ne'): 10, ('PRON', 'le'): 6, ('PRON', 'lui'): 5, ('ADV', 'ne'): 4, ('PRON', "l'"): 3, ('ADV', 'demain'): 2, ('ADV', 'fort'): 1, ('ADV', 'profondément'): 1, ('ADV', 'vite'): 1, ('NOUN', 'matin'): 1, ('CONJ', 'et'): 1, ('CONJ', 'donc'): 1, ('CONJ', 'mais'): 1, ('PRON', 'la'): 1, ('PRON', 'les'): 1, ('PRON', 't'): 1}
   ('r267', 'SANS_CIBLE', 'GP', 'à moi')
   ('r324', 'SANS_CIBLE', 'GP', 'sur la table')
   ('r34
… [90 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, re\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nfor lang in ('en','fr'):\n    print('='*25,lang,'='*25)\n    typ=collections.Counter( … [1410 caractères tronqués]`

  ```
========================= en =========================
cibles: 92 uniques: 67
typologie: {'token_exact': 92}
POS gold de la cible: {'VERB': 56, 'NOUN': 35, 'ADJ': 1}
exemples de cibles uniques: ['barks', 'believe', 'belongs', 'bird', 'book', 'boy', 'bread', 'bridge', 'call', 'car', 'cat', 'children', 'city', 'climbs', 'continue', 'cries', 'danced', 'day', 'dog', 'eat', 'falls', 'film', 'fish', 'flower', 'flowers', 'flows', 'fly', 'get', 'girl', 'goes', 'grow', 'house', 'hung', 'know', 'leave', 'leaves', 'listen', 'listens', 'man', 'mouse']
========================= fr =========================
cibles: 93 uniques: 72
typologie: {'token_exact': 93}
POS gold de la cible: {'VERB': 56, 'NOUN': 36, 'ADJ': 1}
exemples de cibles uniques: ['aboie', 'accroché', 'appartient', 'appelle', 'attendent', 'chante', 'chat', 'chien', 'continue', 'coule', 'crois', 'dansait', 'dit', 'dort', 'endroit', 'enfants', 'entre', 'faut', 'fille', 'film', 'fleur', 'fleurs', 'garçon', 'grimpe', 'homme', 'joue', 'jouent', 'jour', 'lieu', 'lit', 'livre', 'maison', 'mangeons', 'montent', 'nage', 'oiseau', 'ouvre', 'pain', 'parle', 'pars']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nfor lang in ('en','fr'): … [933 caractères tronqués]`

  ```
==================== en ====================
n 92
  ('VERB', True) 41
  ('NOUN', False) 34
  ('VERB', False) 15
  ('ADJ', False) 1
  ('NOUN', True) 1
FN (gold VERB, _est_verbe faux): 15
   [('r028', 'GP', 'rains', 'VERB'), ('r102', 'GP', 'falls', 'VERB'), ('r162', 'GP', 'hung', 'VERB'), ('r194', 'GP', 'eat', 'VERB'), ('r205', 'SUB', 'think', 'VERB'), ('r215', 'SUB', 'stay', 'VERB'), ('r240', 'SUB', 'believe', 'VERB'), ('r244', 'SUB', 'cries', 'VERB'), ('r245', 'SUB', 'call', 'VERB'), ('r247', 'SUB', 'think', 'VERB'), ('r249', 'SUB', 'stayed', 'VERB'), ('r279', 'SUB', 'stay', 'VERB'), ('r284', 'SUB', 'goes', 'VERB'), ('r290', 'SUB', 'cries', 'VERB'), ('r298', 'SUB', 'continue', 'VERB')]
FP (gold non-VERB, _est_verbe vrai): 1
   [('r297', 'REL', 'flower', 'NOUN')]
==================== fr ====================
n 93
  ('NOUN', False) 36
  ('VERB', True) 34
  ('VERB', False) 22
  ('ADJ', False) 1
FN (gold VERB, _est_verbe faux): 22
   [('r008', 'GP', 'pleut', 'VERB'), ('r047', 'GP', 'poussent', 'VERB'), ('r057', 'GP', 'aboie', 'VERB'), ('r060', 'GP', 'volent', 'VERB'), ('r086', 'GP', 'rient', 'VERB'), ('r088', 'GP', 'grimpe', 'VERB'), ('r097', 'GP', 'téléphone', 'VERB'), ('r100', 'GP', '
… [547 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nfor lang in ('en','fr'): … [783 caractères tronqués]`

  ```
==================== en ====================
tokens 1114 conf (gold_VERB,_est_verbe): {(False, False): 833, (True, False): 121, (True, True): 141, (False, True): 19}
gold VERB / _est_verbe faux: 121 [(('answers', 'VERB'), 1), (('believe', 'VERB'), 1), (('blows', 'VERB'), 2), (('born', 'VERB'), 1), (('bought', 'VERB'), 3), (('brings', 'VERB'), 1), (('call', 'VERB'), 1), (('calls', 'VERB'), 2), (('catches', 'VERB'), 1), (('chases', 'VERB'), 1), (('continue', 'VERB'), 1), (('corrects', 'VERB'), 1), (('covers', 'VERB'), 2), (('crackles', 'VERB'), 1), (('creaks', 'VERB'), 1), (('cries', 'VERB'), 3), (('cross', 'VERB'), 1), (('crosses', 'VERB'), 1), (('delivers', 'VERB'), 1), (('do', 'VERB'), 1), (('dream', 'VERB'), 1), (('dreams', 'VERB'), 1), (('drinks', 'VERB'), 1), (('drives', 'VERB'), 1), (('eat', 'VERB'), 3), (('eats', 'VERB'), 3), (('enters', 'VERB'), 1), (('falls', 'VERB'), 3), (('follows', 'VERB'), 1), (('freezes', 'VERB'), 1), (('go', 'VERB'), 1), (('goes', 'VERB'), 1), (('have', 'VERB'), 1), (('hung', 'VERB'), 1), (('is', 'VERB'), 3), (('laugh', 'VERB'), 2), (('lights', 'VERB'), 2), (('live', 'VERB'), 3), (('lives', 'VERB'), 1), (('mention', 'VERB'), 3), (('mixes', 'VERB'), 1)
… [3983 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nfor txt,lg in [(\"The dog eats an apple.\",\"en\"),(\"She listens to music.\",\"en\"),(\"The book … [433 caractères tronqués]`

  ```
========== The dog eats an apple.
S: [{'nom': 'structure la plus proche', 'lecture': 'chaque segment se rattache à la cible la plus proche.', 'attachement': None, 'segments': [{'debut': 0, 'fin': 21, 'texte': 'The dog eats an apple', 'type': 'GV', 'role': 'predicat', 'niveau': 0, 'parent': None, 'profondeur': 0}]}]
  pos DET 'The' 0 3 cand= [] meta= {'ouvert': False}
  syntagme GV 'The dog eats an apple' 0 21 cand= ['structure la plus proche'] meta= {'role': 'predicat', 'niveau': 0}
  syntagme GN 'The dog eats an apple' 0 21 cand= ['GN', 'eats'] meta= {'role': 'groupe nominal', 'niveau': 0, 'union': True, 'attachement': {'segment': 'The dog eats an apple', 'cible': 'eats'}}
  pos NOUN 'dog' 4 7 cand= ['noun'] meta= {'ouvert': True}
  pos VERB 'eats' 8 12 cand= ['verb'] meta= {'ouvert': True}
  pos DET 'an' 13 15 cand= [] meta= {'ouvert': False}
  pos NOUN 'apple' 16 21 cand= ['noun'] meta= {'ouvert': True}
========== She listens to music.
S: [{'nom': 'structure la plus proche', 'lecture': 'chaque segment se rattache à la cible la plus proche.', 'attachement': None, 'segments': [{'debut': 0, 'fin': 20, 'texte': 'She listens to music', 'type': 'GV', 'role': 'predicat', 'niveau': 0, '
… [2348 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 time python3 - <<'PY'\nimport sys, json, collections\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg, bloc_linguistique as bl\nps=eg.charger()\nh=bl.Heur … [1467 caractères tronqués]`

  ```
all n= 612
  pos 0.7455 ferme 0.8984 ouvert 0.6007 tokens 3179
  seg f1 0.2862 P/R 0.3154 0.2619 tete f1 0.4989
  att {'cibles': 239, 'labels': 145, 'couverture': 0.6067, 'top1_taux': 0.5858, 'topk_taux': 0.5941, 'exact_taux': 0.5732, 'top1_taux_span': 0.9655, 'topk_taux_span': 0.9793, 'exact_taux_span': 0.9448, 'topk_exact_taux': 0.59, 'topk_exact_taux_span': 0.9724}
  att v/n {'cibles': 116, 'justes': 111, 'taux': 0.9569} {'cibles': 29, 'justes': 26, 'taux': 0.8966}
  att tete {'cibles': 145, 'labels': 145, 'top1': 140, 'topk': 142, 'top1_taux': 0.9655, 'topk_taux': 0.9793, 'couverture': 1.0}
  prag {'acte': 0.9967, 'negation': 0.9771, 'modalite': 0.9886, 'double_sens': 0.9444} frac 0.5551
fr_all n= 402
  pos 0.7518 ferme 0.8956 ouvert 0.6235 tokens 2031
  seg f1 0.3786 P/R 0.4035 0.3566 tete f1 0.5822
  att {'cibles': 151, 'labels': 117, 'couverture': 0.7748, 'top1_taux': 0.7417, 'topk_taux': 0.755, 'exact_taux': 0.7219, 'top1_taux_span': 0.9573, 'topk_taux_span': 0.9744, 'exact_taux_span': 0.9316, 'topk_exact_taux': 0.7483, 'topk_exact_taux_span': 0.9658}
  att v/n {'cibles': 88, 'justes': 83, 'taux': 0.9432} {'cibles': 29, 'justes': 26, 'taux': 0.8966}
  att tete {'cibles': 11
… [4361 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg, bloc_linguistique as bl\nps=eg.charger()\nsubs={'fr_all':[p for p in  … [753 caractères tronqués]`

  ```
### segmenter_s= False
fr_all pos 0.7518 ouvert 0.6235 seg F1 0.1292 tete 0.4573 cov 0.3245 exact_span 0.0 topk_span 0.0
en_all pos 0.7343 ouvert 0.5571 seg F1 0.1519 tete 0.4537 cov 0.3182 exact_span 0.0 topk_span 0.0
fr_reel pos 0.7591 ouvert 0.6334 seg F1 0.1345 tete 0.4095 cov 0.2907 exact_span 0.0 topk_span 0.0
en_reel pos 0.7278 ouvert 0.5466 seg F1 0.1517 tete 0.4551 cov 0.3176 exact_span 0.0 topk_span 0.0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, json, collections\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg, bloc_linguistique as bl\nps=eg.charger()\nh=bl.Heuristiq … [797 caractères tronqués]`

  ```
==================== en ====================
cibles par type: {'GP': 34, 'SUB': 26, 'REL': 28}
labels par type: {'GP': 28}
exemples labels: [('g016', 'GP', 'in the park', 'saw'), ('r025', 'GP', 'to her brother', 'talks'), ('r026', 'GP', 'to the teacher', 'listen'), ('r027', 'GP', 'on the chair', 'sleeps'), ('r031', 'GP', 'at noon', 'leaves'), ('r040', 'GP', 'in the park', 'play'), ('r061', 'GP', 'with the ball', 'plays'), ('r063', 'GP', 'to the radio', 'listen'), ('r064', 'GP', 'to the students', 'talks'), ('r067', 'GP', 'in the garden', 'grow'), ('r068', 'GP', 'to his sister', 'writes'), ('r070', 'GP', 'on vacation', 'leave'), ('r072', 'GP', 'at ten', 'opens'), ('r077', 'GP', 'at the postman', 'barks'), ('r080', 'GP', 'over the lake', 'fly'), ('r107', 'GP', 'to her friend', 'writes'), ('r108', 'GP', 'on the roof', 'climbs'), ('r110', 'GP', 'in an office', 'works'), ('r120', 'GP', 'to the sea', 'flows'), ('r156', 'GP', 'in the water', 'swims'), ('r160', 'GP', 'in the morning', 'passes'), ('r166', 'GP', 'on the train', 'get'), ('r168', 'GP', 'to music', 'listens'), ('r169', 'GP', 'at his mother', 'smiles'), ('r177', 'GP', 'in front of the door', 'wait'), ('r180', 'GP', 'to the libra
… [1907 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nd=json.load(open('reports/pensee-spans.json'))\nprint(json.dumps(d,ensure_ascii=False,indent=1)[:6000])\n\"", "description": "Read span report JSON"}`

  ```
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "169/169",
 "gold": 612,
 "cibles": 239,
 "spans": {
  "REL": 48,
  "SUB": 33,
  "GP": 12,
  "total": 93
 },
 "categories": {
  "aucun": 65,
  "plus_large": 25,
  "plus_etroit": 3,
  "coupe": 1
 },
 "avant": {
  "labels": 145,
  "couverture": 0.6067,
  "f1": 0.2864,
  "span": 94,
  "cible": 13
 },
 "apres": {
  "labels": 146,
  "couverture": 0.6109,
  "f1": 0.2869,
  "span": 93,
  "cible": 14
 },
 "limites": [
  "81 REL/SUB chez S",
  "dénominateur de l'attachement à corriger",
  "gold 612"
 ],
 "courant": {
  "date": "2026-11-05",
  "source": "audit A1 (pensee-audit-attachement.json)",
  "labels": 145,
  "couverture": 0.6067,
  "f1": 0.2862,
  "span": 94,
  "types": {
   "REL": 48,
   "SUB": 33,
   "GP": 13
  },
  "categories": {
   "aucun": 65,
   "plus_large": 24,
   "plus_etroit": 4,
   "coupe": 1
  },
  "note": "état courant après le lexique élargi (a408a909) ; les blocs avant/apres restent l'historique"
 }
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg, bloc_linguistique as bl\nps=eg.charger(); h=bl.Heuristique()\n … [1037 caractères tronqués]`

  ```
en {'label': 28, 'aucun': 59, 'plus_etroit': 1} losts {'SUB': 26, 'GP': 6, 'REL': 28} total 88
fr {'label': 117, 'plus_large': 25, 'plus_etroit': 3, 'aucun': 6} losts {'GP': 7, 'REL': 20, 'SUB': 7} total 151
None {'label': 145, 'plus_large': 25, 'aucun': 65, 'plus_etroit': 4} losts {'GP': 13, 'SUB': 33, 'REL': 48} total 239
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg, bloc_linguistique as bl\nps=eg.charger(); h=bl.Heuristique()\nfor lang in ( … [1045 caractères tronqués]`

  ```
========================= en =========================
g017 SUB 'that she would come' cible said -> aucun
g020 GP 'to eat' cible ready -> aucun
r028 GP 'since yesterday' cible rains -> aucun
r034 REL 'that I read' cible book -> aucun
r035 REL 'she talks about' cible film -> aucun
r038 GP 'to eat' cible ready -> aucun
r074 REL 'that you read' cible book -> aucun
r075 REL 'where we live' cible city -> aucun
r102 GP 'since this morning' cible falls -> aucun
r114 REL 'that we saw' cible film -> aucun
r115 REL 'where I was born' cible house -> aucun
r153 GP 'for the bus' cible wait -> plus_etroit
      pred GP 'for the' 8 15
r162 GP 'on the wall' cible hung -> aucun
r204 REL 'who speaks' cible man -> aucun
r205 SUB 'that you are right' cible think -> aucun
r214 REL 'that I read' cible book -> aucun
r215 SUB 'When it rains' cible stay -> aucun
r216 SUB 'that he comes' cible says -> aucun
r217 REL 'whom I mention' cible student -> aucun
r218 SUB 'Although it is late' cible works -> aucun
r219 SUB 'that you come' cible know -> aucun
r220 REL 'that sleeps' cible cat -> aucun
r236 REL 'where I live' cible village -> aucun
r237 SUB 'If you come' cible leave -> aucun
r238 SUB 'because she is h
… [4590 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nfor txt in [\"It rains since yesterday.\",\"The rain falls since this morning.\",\"The painting i … [495 caractères tronqués]`

  ```
============ It rains since yesterday.
simple: []
pred: [('GV', 'It rains since yesterday', 0, 24)]
============ The rain falls since this morning.
simple: [('GN', 'The rain falls since this morning')]
pred: [('GV', 'The rain falls since this morning', 0, 33), ('GN', 'The rain falls since this morning', 0, 33)]
============ The painting is hung on the wall.
simple: [('GN', 'The painting'), ('GV', 'is hung on the wall')]
pred: [('GN', 'The painting', 0, 12), ('GV', 'The painting is hung on the wall', 0, 32), ('GV', 'is hung on the wall', 13, 32)]
============ We wait for the bus.
simple: [('GP', 'for the')]
pred: [('GV', 'We wait for the bus', 0, 19), ('GP', 'for the', 8, 15)]
============ The mouse is ready to eat.
simple: [('GN', 'The mouse'), ('GV', 'is ready to eat')]
pred: [('GN', 'The mouse', 0, 9), ('GV', 'The mouse is ready to eat', 0, 25), ('GV', 'is ready to eat', 10, 25)]
est_verbe: {'yesterday': False, 'morning': False, 'bus': True, 'eat': False, 'hung': False, 'wall': False, 'a': True, 'this': False, 'the': False}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -c \"\nimport json\nps=json.load(open('tools/tests/linguistique/gold.json'))['phrases']\nfor p in ps:\n    if p['langue']!='en': continue\n    print('='*10,p['id'],p['texte'])\n    print(' mots:',[(m['texte'],m['pos']) for m  … [116 caractères tronqués]`

  ```
========== g015 The cat sleeps.
 mots: [('The', 'DET'), ('cat', 'NOUN'), ('sleeps', 'VERB')]
   {'type': 'GN', 'texte': 'The cat', 'role': 'agent', 'debut': 0, 'fin': 7}
   {'type': 'GV', 'texte': 'sleeps', 'role': 'prédicat', 'debut': 8, 'fin': 14}
========== g016 The woman saw the man in the park.
 mots: [('The', 'DET'), ('woman', 'NOUN'), ('saw', 'VERB'), ('the', 'DET'), ('man', 'NOUN'), ('in', 'PREP'), ('the', 'DET'), ('park', 'NOUN')]
   {'type': 'GN', 'texte': 'The woman', 'role': 'agent', 'debut': 0, 'fin': 9}
   {'type': 'GV', 'texte': 'saw', 'role': 'prédicat', 'debut': 10, 'fin': 13}
   {'type': 'GN', 'texte': 'the man', 'role': 'patient', 'debut': 14, 'fin': 21}
   {'type': 'GP', 'texte': 'in the park', 'role': 'lieu', 'debut': 22, 'fin': 33, 'cibles': ['saw', 'man'], 'cible': 'saw'}
========== g017 She said that she would come yesterday.
 mots: [('She', 'PRON'), ('said', 'VERB'), ('that', 'CONJ'), ('she', 'PRON'), ('would', 'AUX'), ('come', 'VERB'), ('yesterday', 'ADV')]
   {'type': 'GN', 'texte': 'She', 'role': 'agent', 'debut': 0, 'fin': 3}
   {'type': 'GV', 'texte': 'said', 'role': 'prédicat', 'debut': 4, 'fin': 8}
   {'type': 'SUB', 'texte': 'that she would come', '
… [1028 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, sys\nsys.path.insert(0,'tools/tests/linguistique')\nimport evaluer_gold as eg\nps=eg.charger()\nfor lang in ('en','fr'):\n    print('='*15,lang,'='*15)\n    n=coll … [468 caractères tronqués]`

  ```
=============== en ===============
nb de cibles par segment: {0: 614, 2: 9, 1: 79} total cibles 97
multi: [('g016', 'GP', 'in the park', ['saw', 'man']), ('g020', 'GP', 'to eat', ['ready', 'duck']), ('r038', 'GP', 'to eat', ['ready', 'mouse']), ('r040', 'GP', 'in the park', ['play', 'children']), ('r067', 'GP', 'in the garden', ['grow', 'flowers']), ('r108', 'GP', 'on the roof', ['climbs', 'cat']), ('r156', 'GP', 'in the water', ['swims', 'fish']), ('r162', 'GP', 'on the wall', ['hung', 'painting']), ('r166', 'GP', 'on the train', ['get', 'travelers'])]
=============== fr ===============
nb de cibles par segment: {0: 1010, 1: 117, 2: 34} total cibles 185
multi: [('g003', 'GP', 'dans le parc', ['vu', "l'homme"]), ('g007', 'GP', 'dans le jardin', ['jouent', 'enfants']), ('g012', 'GP', 'à manger', ['prêt', 'canard']), ('r018', 'GP', 'à manger', ['prête', 'souris']), ('r020', 'GP', 'dans le parc', ['jouent', 'enfants']), ('r047', 'GP', 'dans le jardin', ['poussent', 'fleurs']), ('r088', 'GP', 'sur le toit', ['grimpe', 'chat']), ('r126', 'GP', "dans l'eau", ['nage', 'poisson']), ('r132', 'GP', 'au mur', ['accroché', 'tableau']), ('r136', 'GP', 'dans le train', ['montent', 'voyageurs']),
… [1323 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nfor lang in ('en','fr'):\n    print('='*20,lang,'='*20)\n    d=collections.defaultdict(co … [586 caractères tronqués]`

  ```
==================== en ====================
formes multi-POS: 7 / 347
  is           {'AUX': 43, 'VERB': 3} ex: {'AUX': ['r032', 'r034', 'r035'], 'VERB': ['r291', 'r328', 'r363']}
  that         {'CONJ': 11, 'PRON': 11} ex: {'CONJ': ['r034', 'r074', 'r114'], 'PRON': ['r214', 'r220', 'r243']}
  her          {'DET': 4, 'PRON': 3} ex: {'DET': ['r025', 'r107', 'r117'], 'PRON': ['r336', 'r342', 'r358']}
  leaves       {'VERB': 4, 'NOUN': 1} ex: {'VERB': ['r031', 'r296', 'r312'], 'NOUN': ['r173']}
  when         {'CONJ': 4, 'PRON': 1} ex: {'CONJ': ['r215', 'r245', 'r279'], 'PRON': ['r241']}
  do           {'AUX': 2, 'VERB': 1} ex: {'AUX': ['r029', 'r314'], 'VERB': ['r422']}
  fast         {'ADJ': 1, 'ADV': 2} ex: {'ADJ': ['r032'], 'ADV': ['r071', 'r362']}
==================== fr ====================
formes multi-POS: 11 / 392
  le           {'DET': 97, 'PRON': 6} ex: {'DET': ['r001', 'r002', 'r004'], 'PRON': ['r330', 'r339', 'r339']}
  la           {'DET': 63, 'PRON': 1} ex: {'DET': ['r002', 'r003', 'r007'], 'PRON': ['r329']}
  est          {'AUX': 42, 'VERB': 4} ex: {'AUX': ['r012', 'r014', 'r015'], 'VERB': ['r267', 'r324', 'r349']}
  les          {'DET': 24, 'PRON': 1} ex: {'DET': ['r
… [674 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nfor lang,forms in (('en',{'that','is','do','late','far'}),('fr',{'que','est'})):\n    print('='*15,lan … [301 caractères tronqués]`

  ```
=============== en ===============
r029 'I do not understand.' [('do', 'AUX', 2)]
r032 'The car is fast.' [('is', 'AUX', 8)]
r034 'The book that I read is exciting.' [('that', 'CONJ', 9), ('is', 'AUX', 21)]
r035 'The film she talks about is out.' [('is', 'AUX', 25)]
r036 'She is maybe tired.' [('is', 'AUX', 4)]
r038 'The mouse is ready to eat.' [('is', 'AUX', 10)]
r074 'The book that you read is long.' [('that', 'CONJ', 9), ('is', 'AUX', 23)]
r075 'The city where we live is beautiful.' [('is', 'AUX', 23)]
r078 'The door is open.' [('is', 'AUX', 9)]
r112 'The sea is calm.' [('is', 'AUX', 8)]
r114 'The film that we saw was long.' [('that', 'CONJ', 9)]
r115 'The house where I was born is small.' [('is', 'AUX', 27)]
r118 'The cake is delicious.' [('is', 'AUX', 9)]
r162 'The painting is hung on the wall.' [('is', 'AUX', 13)]
r174 'The room is dark.' [('is', 'AUX', 9)]
r199 'The train arrives late.' [('late', 'ADV', 18)]
r204 'The man who speaks is my father.' [('is', 'AUX', 19)]
r205 'I think that you are right.' [('that', 'CONJ', 8)]
r214 'The book that I read is good.' [('that', 'PRON', 9), ('is', 'AUX', 21)]
r216 'She says that he comes.' [('that', 'CONJ', 9)]
r217 'The student whom 
… [5912 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, json, copy, collections\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg, bloc_linguistique as bl\nps=eg.charger(); h=bl.Heu … [1254 caractères tronqués]`

  ```
en corrections 10
  POS brut 0.7343 corrigé 0.7369 delta 0.0026
  ouvert brut 0.5571 corrigé 0.5581
fr corrections 7
  POS brut 0.7518 corrigé 0.7548 delta 0.003
  ouvert brut 0.6235 corrigé 0.6258
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg, bloc_linguistique as bl\nps=eg.charger(); h=bl.Heuristique()\n … [1693 caractères tronqués]`

  ```
#################### full ####################
en
  GP {'cibles': 34, 'labels': 28, 'exact': 28, 'top1': 28, 'topk': 28, 'topk_exact': 28} cov=0.824 exact_span=1.000 topk_span=1.000
  REL {'cibles': 28} cov=0.000 exact_span=0.000 topk_span=0.000
  SUB {'cibles': 26} cov=0.000 exact_span=0.000 topk_span=0.000
  échecs de cible sur labels: 0
fr
  GP {'cibles': 62, 'labels': 55, 'exact': 52, 'top1': 54, 'topk': 53, 'topk_exact': 53} cov=0.887 exact_span=0.945 topk_span=0.964
  REL {'cibles': 46, 'labels': 26, 'exact': 26, 'top1': 26, 'topk': 26, 'topk_exact': 26} cov=0.565 exact_span=1.000 topk_span=1.000
  SUB {'cibles': 43, 'labels': 36, 'exact': 35, 'top1': 35, 'topk': 35, 'topk_exact': 35} cov=0.837 exact_span=0.972 topk_span=0.972
  échecs de cible sur labels: 3
    ('r309', 'SUB', "qu'il viendra", ['viendra'], 'Peut-être')
    ('s108', 'GP', 'sous le nuage', ['rêve', 'papier'], 'papier')
    ('s122', 'GP', 'vers les montagne', ['saute', 'papier'], 'papier')
#################### reel ####################
en
  GP {'cibles': 32, 'labels': 27, 'exact': 27, 'top1': 27, 'topk': 27, 'topk_exact': 27} cov=0.844 exact_span=1.000 topk_span=1.000
  REL {'cibles': 28} cov=0.000 exact_span=0
… [612 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg, bloc_linguistique as bl\nps=eg.charger(); h=bl.Heuristique()\n … [1136 caractères tronqués]`

  ```
fr official labels 117 exact 113
  replicate cibles 151 labels 117 exact 113 per {'GP': 55, 'SUB': 36, 'REL': 26}
  ex ids [('g002', 'GP', 'de la voisine', ['chat'], 'chat'), ('g003', 'GP', 'dans le parc', ['vu', "l'homme"], 'vu'), ('g004', 'GP', 'pour attraper le bus', ['couru'], 'couru'), ('g005', 'SUB', "qu'elle viendrait", ['dit'], 'dit'), ('g007', 'GP', 'dans le jardin', ['jouent', 'enfants'], 'jouent'), ('g010', 'GP', 'ici', ['Viens'], 'Viens'), ('g011', 'REL', "que j'ai lu", ['livre'], 'livre'), ('g012', 'GP', 'à manger', ['prêt', 'canard'], 'prêt'), ('g014', 'GP', 'avec le télescope', ['vu'], 'vu'), ('r005', 'GP', 'à son frère', ['parle'], 'parle'), ('r007', 'GP', 'sur la chaise', ['dort'], 'dort'), ('r008', 'GP', 'depuis hier', ['pleut'], 'pleut'), ('r011', 'GP', 'à midi', ['part'], 'part'), ('r014', 'REL', "que j'ai lu", ['livre'], 'livre'), ('r015', 'REL', 'dont elle parle', ['film'], 'film'), ('r018', 'GP', 'à manger', ['prête', 'souris'], 'prête'), ('r020', 'GP', 'dans le parc', ['jouent', 'enfants'], 'jouent'), ('r041', 'GP', 'au ballon', ['joue'], 'joue'), ('r044', 'GP', 'aux étudiants', ['parle'], 'parle'), ('r047', 'GP', 'dans le jardin', ['poussent', 'fleurs'], 'p
… [1206 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg, bloc_linguistique as bl\nps=eg.charger(); h=bl.Heuristique()\nfor lg  … [212 caractères tronqués]`

  ```
fr
{
 "cibles": 151,
 "labels": 117,
 "top1": 115,
 "topk": 114,
 "exact": 113,
 "top1_taux": 0.7616,
 "topk_taux": 0.755,
 "exact_taux": 0.7483,
 "top1_taux_span": 0.9829,
 "topk_taux_span": 0.9744,
 "topk_exact": 114,
 "topk_exact_taux": 0.755,
 "topk_exact_taux_span": 0.9744,
 "exact_taux_span": 0.9658,
 "verbe": {
  "cibles": 88,
  "justes": 84,
  "taux": 0.9545
 },
 "nom": {
  "cibles": 29,
  "justes": 29,
  "taux": 1.0
 },
 "couverture": 0.7748
}
en
{
 "cibles": 88,
 "labels": 28,
 "top1": 28,
 "topk": 28,
 "exact": 28,
 "top1_taux": 0.3182,
 "topk_taux": 0.3182,
 "exact_taux": 0.3182,
 "top1_taux_span": 1.0,
 "topk_taux_span": 1.0,
 "topk_exact": 28,
 "topk_exact_taux": 0.3182,
 "topk_exact_taux_span": 1.0,
 "exact_taux_span": 1.0,
 "verbe": {
  "cibles": 28,
  "justes": 28,
  "taux": 1.0
 },
 "nom": {
  "cibles": 0,
  "justes": 0,
  "taux": 0.0
 },
 "couverture": 0.3182
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for seed in 0 1 2 42; do echo \"seed=$seed\"; PYTHONHASHSEED=$seed PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg, bloc_lin … [340 caractères tronqués]`

  ```
seed=0
fr labels 117 exact 113 top1 115 topk 114 cov 0.7748
en labels 28 exact 28 top1 28 topk 28 cov 0.3182
seed=1
fr labels 117 exact 113 top1 115 topk 114 cov 0.7748
en labels 28 exact 28 top1 28 topk 28 cov 0.3182
seed=2
fr labels 117 exact 113 top1 115 topk 114 cov 0.7748
en labels 28 exact 28 top1 28 topk 28 cov 0.3182
seed=42
fr labels 117 exact 113 top1 115 topk 114 cov 0.7748
en labels 28 exact 28 top1 28 topk 28 cov 0.3182
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg, bloc_linguistique as bl\nps=eg.charger()\nfr=[p for p in ps if p['langue']= … [474 caractères tronqués]`

  ```
fr #1 labels 117 top1 115 exact 113 topk 114 topk_exact 114
fr #2 labels 117 top1 115 exact 113 topk 114 topk_exact 114
fr fresh labels 117 top1 115 exact 113 topk 114 topk_exact 114
all labels 145 top1 143 exact 141 topk 142 topk_exact 142
fr after all labels 117 top1 115 exact 113 topk 114 topk_exact 114
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short tools/ reports/ docs/ AGENTS.md data/ | head -30; echo '---'; git log -3 --format='%h %ad %s' --date=short -- tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py; echo '---'; stat -c '%y %n' tools/b … [175 caractères tronqués]`

  ```
M docs/pilotage/en-cours.md
 M reports/pensee-quatre-modes.json
 M tools/bloc_linguistique.py
 M tools/pensee/autotest.py
 m tools/structures
?? reports/pensee-audit-v2.json
?? reports/pensee-cache-chunker.json
?? reports/pensee-echecs-v2.json
?? reports/pensee-replis-cible.json
?? reports/rapport-cache-chunker.md
?? reports/rapport-echecs-v2.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/replis_cible.py
---
e0592c59 2026-11-05 B13 — LE CACHE DU CHUNKER APPLIQUÉ : ×139 À 160 RÉPÉTITIONS, SORTIE IDENTIQUE (0/612) ; ×1 EN DÉFAUT, S DOMINE ; 181/181
9d5337ce 2026-11-05 B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180
e223a98d 2026-11-05 B13 — LE TOP-K STRICT : 0,6069 EN ÉGALITÉ EXACTE, PAS 0,9241 (SOUS-CHAÎNES) ; 176/176
---
2026-11-05 15:04:59.190598153 -0500 tools/bloc_linguistique.py
2026-11-05 13:51:45.675060894 -0500 tools/tests/linguistique/evaluer_gold.py
2026-11-02 14:39:32.079131990 -0500 tools/tests/linguistique/gold_reel.json
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git rev-parse HEAD && git diff --stat HEAD -- tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/gold_reel.py toolstests 2>/dev/null", "description": "Check git HEAD and diffs"}`

  ```
15ee10d3cd54dcdf3419144d23445765c8910ba2
 tools/bloc_linguistique.py | 66 +++++++++++++++++++++++++++++++++++++++++++---
 1 file changed, 62 insertions(+), 4 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date; echo '---'; git diff -- tools/bloc_linguistique.py | head -160", "description": "Inspect uncommitted bloc changes"}`

  ```
jeu 05 nov 2026 15:15:08 EST
---
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 07a41ec9..b171b5f2 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -428,9 +428,20 @@ am is are was were be been being have has had having do does did done
 """.split())
 
 
+ENCLITIQUES = ("-moi", "-toi", "-nous", "-vous", "-le", "-la", "-les", "-lui", "-leur", "-y", "-en")
+
+
+def _sans_enclitique(mot: str) -> str:
+    """`appelle-moi` → `appelle` (les enclitiques ne font pas partie de la tête)."""
+    for suf in ENCLITIQUES:
+        if mot.endswith(suf) and len(mot) > len(suf):
+            return mot[: -len(suf)]
+    return mot
+
+
 def _est_verbe(mot: str) -> bool:
     """Le mot est-il un verbe ? Lexique + désinences courantes (fr/en)."""
-    n = _normaliser(mot)
+    n = _normaliser(_sans_enclitique(mot))
     if not n:
         return False
     if n in VERBES_CONNUS:
@@ -616,6 +627,41 @@ class Heuristique:
         except Exception:
             return {}
 
+    @staticmethod
+    def _repli_cible_gp(texte: str, segment: dict, gns: list[dict]) -> str | None:
+        """Cible vide d'un GP : génitif → tête du GN à gauche (sinon None, l
… [5095 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,140p' tools/bloc_linguistique.py", "description": "Read module header and RACINE"}`

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
… [3993 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, types, pathlib, hashlib, subprocess, json\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\nimport bloc_linguistique as bl\n … [942 caractères tronqués]`

  ```
sha HEAD 5640809e8e6bfbd6 sha WT 64b7c5204f21e4c2 same False
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 10, in <module>
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", line 58, in <module>
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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, types, pathlib, hashlib, subprocess\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\nimport bloc_linguistique as bl\npath=p … [948 caractères tronqués]`

  ```
sha HEAD 5640809e8e6bfbd6 sha WT 64b7c5204f21e4c2
### head
fr pos 0.7518 f1 0.3786 labels 117 cov 0.7748 top1 112 topk 114 exact 109 topk_exact 113
en pos 0.7343 f1 0.121 labels 28 cov 0.3182 top1 28 topk 28 exact 28 topk_exact 28
### wt
fr pos 0.7518 f1 0.3786 labels 117 cov 0.7748 top1 115 topk 114 exact 113 topk_exact 114
en pos 0.7343 f1 0.121 labels 28 cov 0.3182 top1 28 topk 28 exact 28 topk_exact 28
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nfor lang in ('en','fr'):\n    print('='*22,lang,'='*22)\n    roles=collections.defaultdic … [1968 caractères tronqués]`

  ```
====================== en ======================
types: {'GN': 314, 'GV': 253, 'GP': 38, 'REL': 28, 'SUB': 25, 'ADJ': 18, 'ADV': 8, 'PONCT': 2}
  roles GN {'agent': 221, 'patient': 89, 'attribut': 4}
  roles GV {'prédicat': 253}
  roles GP {'destinataire': 11, 'lieu': 15, 'temps': 6, 'but': 1, 'moyen': 1, 'cible': 4}
  roles REL {'qualité': 6, 'sujet': 7, 'objet': 10, 'lieu': 4, 'temps': 1}
  roles SUB {'complément': 8, 'temps': 6, 'concession': 3, 'condition': 2, 'cause': 6}
  roles ADJ {'attribut': 18}
  roles ADV {'attribut': 2, 'temps': 4, 'modalité': 1, 'négation': 1}
  roles PONCT {'ponctuation': 2}
cible dans son segment: 0 []
REL cible != tête du GN gauche: 0
GP/SUB cible POS inattendue: 0
====================== fr ======================
types: {'GN': 344, 'GV': 279, 'GP': 33, 'REL': 29, 'SUB': 28, 'ADJ': 17, 'ADV': 22, 'PONCT': 7}
  roles GN {'agent': 246, 'patient': 94, 'temps': 1, 'attribut': 3}
  roles GV {'prédicat': 279}
  roles GP {'destinataire': 7, 'lieu': 16, 'temps': 5, 'but': 1, 'moyen': 1, 'cible': 1, 'manière': 1, 'attribut': 1}
  roles REL {'qualité': 6, 'sujet': 6, 'objet': 13, 'lieu': 3, 'temps': 1}
  roles SUB {'complément': 11, 'temps': 6, 'concession': 3
… [697 caractères tronqués]
  ```

