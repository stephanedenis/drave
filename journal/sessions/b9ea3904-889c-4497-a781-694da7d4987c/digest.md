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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\ndef mots_de(t,segs,typ=None):\n    return [s for s in segs if typ is None or s['type']==t … [1609 caractères tronqués]`

  ```
==================== en ====================
cibles GP non gouvernées: 0
cibles GP non verbe/nom: 1 [('r038', 'to eat', 'ready', 'ADJ')]
==================== fr ====================
cibles GP non gouvernées: 0
cibles GP non verbe/nom: 1 [('r018', 'à manger', 'prête', 'ADJ')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, re\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nfor lang in ('en','fr'):\n    print('='*22,lang,'='*22)\n    ponct=[]; unco=[]; seg_i … [1182 caractères tronqués]`

  ```
====================== en ======================
phrases avec PONCT: 3 ['r427', 'r432', 'r422']
tokens hors segment: 23 phrases 20
   [('r030', 'tomorrow', 'ADV'), ('r039', 'hard', 'ADV'), ('r069', 'deeply', 'ADV'), ('r071', 'fast', 'ADV'), ('r076', 'tomorrow', 'ADV'), ('r076', 'morning', 'NOUN'), ('r106', 'loudly', 'ADV'), ('r277', 'and', 'CONJ'), ('r311', 'so', 'CONJ'), ('r312', 'but', 'CONJ'), ('r314', 'Do', 'AUX'), ('r333', 'it', 'PRON'), ('r334', 'it', 'PRON'), ('r335', 'them', 'PRON'), ('r341', 'it', 'PRON'), ('r341', 'it', 'PRON'), ('r341', 'down', 'ADV'), ('r360', 'it', 'PRON'), ('r361', 'it', 'PRON'), ('r363', 'it', 'PRON'), ('r369', 'it', 'PRON'), ('r371', 'it', 'PRON'), ('r422', 'do', 'VERB')]
segments avec caractères non tokenisés: 0 []
====================== fr ======================
phrases avec PONCT: 22 ['r408', 'r409', 'r410', 'r411', 'r412', 'r413', 'r414', 'r415', 'r416', 'r417', 'r423', 'r424', 'r425', 'r426', 'r428', 'r429', 'r430', 'r431', 'r418', 'r419', 'r420', 'r421']
tokens hors segment: 40 phrases 36
   [('r010', 'demain', 'ADV'), ('r019', 'fort', 'ADV'), ('r049', 'profondément', 'ADV'), ('r051', 'vite', 'ADV'), ('r056', 'demain', 'ADV'), ('r056', 'matin'
… [866 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, json, collections, types, pathlib, subprocess\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\nimport bloc_linguistique as  … [615 caractères tronqués]`

  ```
gold pragma distinct values:
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 7, in <module>
  File "/usr/lib64/python3.13/collections/__init__.py", line 614, in __init__
    self.update(iterable, **kwds)
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.13/collections/__init__.py", line 706, in update
    _count_elements(self, iterable)
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
TypeError: unhashable type: 'dict'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, json, collections\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\nimport bloc_linguistique as bl\nps=eg.charger(); h=bl.He … [617 caractères tronqués]`

  ```
gold pragma (en):
  151 {"acte": "assertion"}
  6 {"acte": "assertion", "modalite": true}
  3 {"acte": "assertion", "negation": true}
  2 {"acte": "assertion", "double_sens": true}
  2 {"acte": "question", "reponse": "yes"}
  1 {"acte": "ordre"}
  3 {"acte": "assertion", "coref": {"it": "cat"}}
  1 {"acte": "assertion", "coref": {"she": "marie"}}
  4 {"acte": "assertion", "coref": {"it": "dog"}}
  1 {"acte": "assertion", "coref": {"she": "sophie"}}
  3 {"acte": "assertion", "coref": {"it": "book"}}
  1 {"acte": "assertion", "coref": {"it": "mouse"}}
  1 {"acte": "assertion", "coref": {"them": "flowers"}}
  1 {"acte": "assertion", "coref": {"her": "marie"}}
  1 {"acte": "assertion", "coref": {"they": "mouse"}}
  2 {"acte": "assertion", "coref": {"it": "book", "she": "marie"}}
  1 {"acte": "assertion", "coref": {"her": "marie", "she": "marie"}}
  1 {"acte": "assertion", "coref": {"he": "paul", "her": "marie"}}
  1 {"acte": "assertion", "coref": {"it": "car"}}
  1 {"acte": "assertion", "coref": {"they": "children"}}
  1 {"acte": "assertion", "coref": {"it": "train"}}
  1 {"acte": "assertion", "coref": {"it": "rain"}}
  1 {"acte": "assertion", "coref": {"him": "teacher"}}
  1 {"acte": 
… [1941 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, re\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nprint('EN coref:')\nfor p in ps:\n    if p['langue']!='en' or 'coref' not in p['pragm … [812 caractères tronqués]`

  ```
EN coref:
r317 'The cat sleeps; it dreams.' coref= {'it': 'cat'} pronoms= {'it': 1} 
r318 'Marie reads. She loves books.' coref= {'she': 'marie'} pronoms= {'She': 1} 
r326 'The cat sees the dog; it sleeps.' coref= {'it': 'dog'} pronoms= {'it': 1} 
r327 'Marie calls Sophie; she answers.' coref= {'she': 'sophie'} pronoms= {'she': 1} 
r328 'The book is on the table; it is red.' coref= {'it': 'book'} pronoms= {'it': 1} 
r333 'The cat eats the mouse; it sees it.' coref= {'it': 'mouse'} pronoms= {'it': 2}  COLLISION
r334 'Marie reads the book; she reads it.' coref= {'it': 'book'} pronoms= {'she': 1, 'it': 1} 
r335 'The children love the flowers; they pick them.' coref= {'them': 'flowers'} pronoms= {'they': 1, 'them': 1} 
r336 'Paul sees Marie; he speaks to her.' coref= {'her': 'marie'} pronoms= {'he': 1, 'her': 1} 
r340 'The cat, the dog and the mouse sleep; they dream.' coref= {'they': 'mouse'} pronoms= {'they': 1} 
r341 'Marie reads a book; she closes it; she puts it down.' coref= {'she': 'marie', 'it': 'book'} pronoms= {'she': 2, 'it': 2}  COLLISION
r342 'Paul sees Marie; he speaks to her; she listens.' coref= {'her': 'marie', 'she': 'marie'} pronoms= {'he': 1, 'her': 1, 'she': 1} 
r3
… [7061 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, types, pathlib, subprocess, json\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\npath=pathlib.Path('tools/bloc_linguistiqu … [719 caractères tronqués]`

  ```
======== r328 'The book is on the table; it is red.'
======== r336 'Paul sees Marie; he speaks to her.'
  GP 'to her' 27 33 att= {'segment': 'to her', 'cible': 'her'} cand= ['GP', 'her', 'sees']
======== r342 'Paul sees Marie; he speaks to her; she listens.'
  GP 'to her' 27 33 att= {'segment': 'to her', 'cible': 'her'} cand= ['GP', 'her', 'listens', 'sees']
======== r358 'Paul sees Marie; he speaks to her.'
  GP 'to her' 27 33 att= {'segment': 'to her', 'cible': 'her'} cand= ['GP', 'her', 'sees']
======== r363 'The book is on the table; I read it.'
======== r367 'The teacher speaks; the students listen to him.'
  GP 'to him' 40 46 att= {'segment': 'to him', 'cible': 'listen'} cand= ['GP', 'listen', 'teacher']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, types, pathlib, subprocess, copy, collections\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\npath=pathlib.Path('tools/blo … [2943 caractères tronqués]`

  ```
en first: cibles 88 labels 28 exact 28 per {'GP': 28} | any: exact 28 per {'GP': 28}
fr first: cibles 151 labels 117 exact 113 per {'GP': 52, 'SUB': 35, 'REL': 26} | any: exact 115 per {'GP': 54, 'SUB': 35, 'REL': 26}
missing targets added: 4
EN +4 cibles: cibles 92 labels 32 cov 0.3478 exact 29 exact_taux 0.3152 exact_span 0.9062
EN +6 cibles (is): cibles 94 labels 32 exact 29 exact_taux 0.3085
EN drop 5: 205 pos 0.7384 f1 0.1209 cibles 86 labels 28 cov 0.3256 exact 28 exact_taux 0.3256
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, types, pathlib, subprocess, json, random, collections, copy\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\nimport bloc_li … [4322 caractères tronqués]`

  ```
{
 "fr_all": {
  "phrases": 402,
  "pos": {
   "exactitude": 0.7518,
   "exactitude_ferme": 0.8956,
   "exactitude_ouvert": 0.6235,
   "tokens": 2031,
   "confusions": {
    "ADJ": {
     "ADJ": 26,
     "NOUN": 68
    },
    "ADV": {
     "ADV": 100,
     "NOUN": 5,
     "PREP": 1,
     "ADJ": 1
    },
    "AUX": {
     "PREP": 4,
     "AUX": 58,
     "?": 3,
     "NOUN": 2
    },
    "CONJ": {
     "CONJ": 22,
     "PRON": 25,
     "?": 13,
     "PREP": 2
    },
    "DET": {
     "DET": 373,
     "?": 2
    },
    "NOUN": {
     "NOUN": 412,
     "ADJ": 12,
     "VERB": 9,
     "?": 1
    },
    "NUM": {
     "NUM": 1
    },
    "PONCT": {
     "?": 22
    },
    "PREP": {
     "PREP": 70,
     "NOUN": 1
    },
    "PRON": {
     "PRON": 234,
     "?": 30,
     "DET": 11
    },
    "VERB": {
     "VERB": 231,
     "NOUN": 271,
     "PREP": 2,
     "?": 15,
     "AUX": 3,
     "ADV": 1
    }
   }
  },
  "syntagme": {
   "precision": 0.4035,
   "rappel": 0.3566,
   "f1": 0.3786,
   "tp": 414,
   "fp": 612,
   "fn": 747,
   "tete": {
    "precision": 0.6845,
    "rappel": 0.5065,
    "f1": 0.5822,
    "tp": 588,
    "fp": 271,
    "fn": 573
   }
  },
  "pragmatique": {
   "acte": 0.
… [9028 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date; sha256sum tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/gold_reel.json; echo '---'; git status --short tools/ | head; echo '--- submodule'; git -C tools/structures status --short | … [240 caractères tronqués]`

  ```
jeu 05 nov 2026 15:26:34 EST
9da6dee7118cfa576d159ccdf5d1241232e974544cd3a6c5cebaddcbbaccd059  tools/bloc_linguistique.py
c4d2dbc07b4e4c0b1c81889b61fd517d5d5953b4a3efae2094834a398ac5d599  tools/tests/linguistique/evaluer_gold.py
05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11  tools/tests/linguistique/gold_reel.json
---
 M tools/bloc_linguistique.py
 M tools/pensee/autotest.py
 m tools/structures
?? tools/tests/linguistique/replis_cible.py
--- submodule
 M donnees/paragraphes-validations.jsonl
523d8c1 2026-11-04 S — LE FAIT DIVERS EST TRANCHÉ : 61/61 TYPES, 144/144 RÔLES ; LA TÊTE DU GN ARRÊTE LE VERBE
4012729 2026-11-04 S — LA BANQUE DE PARAGRAPHES PASSE À NEUF : SIX PAIRES D'ALICE, SOURCES ANGLAISES ET RÉFÉRENTS
2026-11-04 11:41:49.129836555 -0500 tools/structures/generateur.py
--- super
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
MM journal/sessions/0733c5bb-f90b-4f58-9241-33
… [560 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^import\\|^from\\|import bloc\\|bloc_linguistique\\|_est_verbe\" tools/structures/generateur.py | head -40", "description": "Check S generator imports"}`

  ```
12:from __future__ import annotations
14:import json
15:import re
16:import unicodedata
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show HEAD:tools/bloc_linguistique.py | sha256sum; git diff --stat HEAD -- tools/bloc_linguistique.py; git status --short tools/bloc_linguistique.py", "description": "Check current HEAD and worktree diff"}`

  ```
64b7c5204f21e4c230dcd131469187f0c9789e06469f4e19af5f8819f87ab5fa  -
 tools/bloc_linguistique.py | 14 ++++++--------
 1 file changed, 6 insertions(+), 8 deletions(-)
 M tools/bloc_linguistique.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date; git rev-parse HEAD; git log -5 --format='%h %ad %s' --date=iso; echo '--- current diff'; git diff -- tools/bloc_linguistique.py", "description": "Identify current HEAD and working diff"}`

  ```
jeu 05 nov 2026 15:27:33 EST
dcf7bc912caeebe940793888d88723f0bbb57f58
dcf7bc91 2026-11-05 15:18:56 -0500 B13 — L'ATTACHEMENT V3 : EXACT 0,9448 → 0,9724, NOMS 29/29 = 1,0 ; R2/R3/R4 DE A9 ; 181/181
15ee10d3 2026-11-05 14:55:27 -0500 PILOTAGE — LES LIGNES B13 DU ROADMAP ET DES CHANTIERS PASSENT À LA V2 (ATTACHEMENT 0,9448, 181/181)
1ec7286c 2026-11-05 14:48:04 -0500 PILOTAGE — LES QUATRE VAGUES DE SOUS-AGENTS DOCUMENTÉES (§ 9) ; VAGUES 3 ET 4 EN COURS
a914c1e7 2026-11-05 14:44:19 -0500 FICHES — LES 3 DIVERGENCES ET LEURS RÉSIDUS CORRIGÉS (SPANS, DÉNOMINATEUR, LEXIQUE ÉLARGI) ; COHÉRENCE A4 À JOUR
a2def5ee 2026-11-05 14:41:59 -0500 PILOTAGE — LE CACHE DU CHUNKER AU JOURNAL ; T0 DANS LE BUDGET ; 181/181
--- current diff
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index b171b5f2..8d0ca1f8 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -922,10 +922,11 @@ class Heuristique:
         cands = self._syntagmes_s(texte)
         cibles_s = self._cibles_s(texte) if cands else {}
         cache_gv: dict = {}  # un GV n'est analysé qu'une fois par analyse
+        # **un seul chunking par analyse**, partagé par les trois chemins (S, union, chu
… [1828 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -i -E \"attachement.*v3|v3.*attachement|echecs-v2\"; echo '---'; sed -n '1,80p' reports/rapport-pensee-attachement-v3.md 2>/dev/null || true", "description": "Look for v3 attachment report"}`

  ```
pensee-attachement-v3.json
pensee-echecs-v2.json
rapport-echecs-v2.md
rapport-pensee-attachement-v3.md
---
# B13 — l'attachement v3 : exact 0,9448 → 0,9724, les noms à 1,0

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **181/181 portes** : trois règles **générales** issues du diagnostic des 8 échecs (A9) sont
> intégrées — **R2** (un GP n'est pas gouverné par un mot de son span), **R3** (cible vide :
> génitif → tête du GN à gauche), **R4** (enclitique `appelle-moi` → `appelle`). Sur les 145
> segments au bon span : **exact 137 → 141 (0,9724)**, top1 **140 → 143 (0,9862)**, top-k 142
> (0,9793), **top-k strict 142 (0,9793)** ; les **cibles noms atteignent 29/29 = 1,0**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_cible_hors_span`,
> `_repli_cible_gp`, `_sans_enclitique`), [`autotest.py`](../tools/pensee/autotest.py) ;
> fiche A9 [échecs v2](rapport-echecs-v2.md) ; JSON [`pensee-attachement-v3.json`](pensee-attachement-v3.json).

## 1. Avant / après (145 segments au bon span)

| mesure | v2 | **v3** | écart |
|---|---:|---:|---:|
| top1 | 140 (0,9655) | **143 (0,9862)** | +3 |
| top-k | 14
… [3234 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, types, pathlib, subprocess, hashlib, json, time\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\npath=pathlib.Path('tools/b … [1009 caractères tronqués]`

  ```
HEAD dcf7bc912caeebe940793888d88723f0bbb57f58
sha HEAD 64b7c5204f21e4c2 sha WT 9da6dee7118cfa57 same False
## head
fr pos 0.7518 f1 0.3786 labels 117 cov 0.7748 top1 115 topk 114 exact 113 topk_exact 114
en pos 0.7343 f1 0.121 labels 28 cov 0.3182 top1 28 topk 28 exact 28 topk_exact 28
## wt
fr pos 0.7518 f1 0.3786 labels 117 cov 0.7748 top1 115 topk 114 exact 113 topk_exact 114
en pos 0.7343 f1 0.121 labels 28 cov 0.3182 top1 28 topk 28 exact 28 topk_exact 28
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, json, collections\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg, bloc_linguistique as bl\nps=eg.charger()\nfor scope,rows … [1632 caractères tronqués]`

  ```
=============== reel ===============
cibles 92 uniques 67 segments multi-cibles 7 segtypes {'GP': 39, 'REL': 28, 'SUB': 25}
typologie {'token_exact': 92} POS {'VERB': 56, 'NOUN': 35, 'ADJ': 1}
conf _est_verbe (gold_VERB,est): {(True, True): 41, (True, False): 15, (False, False): 35, (False, True): 1}
FN 15 [('r028', 'GP', 'rains'), ('r102', 'GP', 'falls'), ('r162', 'GP', 'hung'), ('r194', 'GP', 'eat'), ('r205', 'SUB', 'think'), ('r215', 'SUB', 'stay'), ('r240', 'SUB', 'believe'), ('r244', 'SUB', 'cries'), ('r245', 'SUB', 'call'), ('r247', 'SUB', 'think'), ('r249', 'SUB', 'stayed'), ('r279', 'SUB', 'stay'), ('r284', 'SUB', 'goes'), ('r290', 'SUB', 'cries'), ('r298', 'SUB', 'continue')]
FP 1 [('r297', 'REL', 'flower', 'NOUN')]
accuracy 0.8260869565217391
=============== full ===============
cibles 97 uniques 70 segments multi-cibles 9 segtypes {'GP': 43, 'SUB': 26, 'REL': 28}
typologie {'token_exact': 97} POS {'VERB': 58, 'NOUN': 37, 'ADJ': 2}
conf _est_verbe (gold_VERB,est): {(True, True): 43, (False, False): 38, (True, False): 15, (False, True): 1}
FN 15 [('r028', 'GP', 'rains'), ('r102', 'GP', 'falls'), ('r162', 'GP', 'hung'), ('r194', 'GP', 'eat'), ('r205', 'SUB', 'think'), ('r21
… [325 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg, bloc_linguistique as bl\nps=[p for p in eg.charger() if p['lan … [1247 caractères tronqués]`

  ```
========== gold VERB
  -> NOUN 176 formes: [('leave', 7), ('sings', 6), ('writes', 5), ('speaks', 5), ('sees', 5), ('leaves', 4), ('play', 4), ('runs', 4), ('arrives', 4), ('shines', 3), ('talks', 3), ('prepares', 3), ('barks', 3), ('falls', 3), ('works', 3), ('stay', 3), ('mention', 3), ('cries', 3)]
  -> ADJ 5 formes: [('live', 3), ('arrive', 2)]
  -> AUX 4 formes: [('is', 3), ('have', 1), ('do', 1)]
  -> ? 1 formes: []
========== gold NOUN
  -> VERB 38 formes: [('letter', 5), ('teacher', 4), ('mother', 3), ('sister', 3), ('morning', 3), ('rain', 3), ('river', 3), ('flower', 2), ('newspaper', 1), ('brother', 1), ('chair', 1), ('dinner', 1), ('baker', 1), ('gardener', 1), ('seller', 1), ('water', 1), ('painting', 1), ('painter', 1)]
  -> ADJ 5 formes: [('table', 4), ('meal', 1)]
========== gold ADJ
  -> NOUN 12 formes: [('right', 2), ('fast', 1), ('calm', 1), ('dark', 1), ('absent', 1), ('mean', 1), ('fresh', 1), ('quiet', 1), ('alone', 1), ('rare', 1), ('hungry', 1)]
  -> VERB 4 formes: [('tired', 2), ('exciting', 1), ('open', 1)]
========== gold ADV
  -> NOUN 16 formes: [('late', 4), ('out', 2), ('maybe', 2), ('fast', 2), ('hard', 1), ('outside', 1), ('far', 1), ('again', 1), ('
… [1557 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, types, pathlib, subprocess, collections\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\npath=pathlib.Path('tools/bloc_ling … [1385 caractères tronqués]`

  ```
============ en phrases 210 S None 0 S segments 277 types {'GV': 277}
  exact S spans 2 / 702 pertype {'GV': 2} whole-sentence 147
  ex whole: [('g015', 'GV', 'The cat sleeps'), ('g016', 'GV', 'The woman saw the man in the park'), ('g017', 'GV', 'She said that she would come yesterday'), ('g018', 'GV', 'He does not sleep'), ('g019', 'GV', 'It might rain'), ('g020', 'GV', 'The duck is ready to eat'), ('r021', 'GV', 'The dog eats an apple'), ('r022', 'GV', 'The girl reads the newspaper')]
============ fr phrases 402 S None 0 S segments 824 types {'GN': 315, 'GV': 342, 'GP': 78, 'SUB': 38, 'REL': 51}
  exact S spans 410 / 1161 pertype {'GN': 176, 'GV': 118, 'GP': 53, 'SUB': 37, 'REL': 26} whole-sentence 100
  ex whole: [('g009', 'GV', 'Il ne dort pas'), ('g013', 'GV', 'Peux-tu venir'), ('r004', 'GN', 'Le soleil brille'), ('r009', 'GV', 'Je ne comprends pas'), ('r016', 'GV', 'Elle est peut-être fatiguée'), ('r017', 'GV', 'Nous devons travailler'), ('r019', 'GN', 'Le vent souffle fort'), ('r042', 'GN', 'La mère prépare le repas')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, types, pathlib, subprocess, collections\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\npath=pathlib.Path('tools/bloc_ling … [1525 caractères tronqués]`

  ```
reel en categories {'label': 27, 'aucun': 57, 'plus_etroit': 1} losts {'GP': 5, 'REL': 28, 'SUB': 25} par_type {'GP': {'label': 27, 'aucun': 4, 'plus_etroit': 1}, 'REL': {'aucun': 28}, 'SUB': {'aucun': 25}}
reel fr categories {'label': 78, 'plus_etroit': 3, 'plus_large': 3, 'coupe': 1, 'aucun': 1} losts {'GP': 2, 'REL': 4, 'SUB': 2} par_type {'GP': {'label': 28, 'plus_etroit': 1, 'plus_large': 1}, 'REL': {'label': 25, 'plus_large': 2, 'coupe': 1, 'plus_etroit': 1}, 'SUB': {'label': 25, 'plus_etroit': 1, 'aucun': 1}}
full en categories {'label': 28, 'aucun': 59, 'plus_etroit': 1} losts {'SUB': 26, 'GP': 6, 'REL': 28} par_type {'GP': {'label': 28, 'aucun': 5, 'plus_etroit': 1}, 'SUB': {'aucun': 26}, 'REL': {'aucun': 28}}
full fr categories {'label': 117, 'plus_large': 24, 'plus_etroit': 3, 'coupe': 1, 'aucun': 6} losts {'GP': 7, 'REL': 20, 'SUB': 7} par_type {'GP': {'label': 55, 'plus_large': 6, 'plus_etroit': 1}, 'SUB': {'label': 36, 'plus_etroit': 1, 'aucun': 6}, 'REL': {'label': 26, 'plus_large': 18, 'coupe': 1, 'plus_etroit': 1}}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, types, pathlib, subprocess, collections\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\npath=pathlib.Path('tools/bloc_ling … [810 caractères tronqués]`

  ```
en {('VERB', 'VERB'): 17, ('NOUN', 'NOUN'): 34, ('ADJ', 'ADJ'): 2, ('VERB', 'NOUN'): 41, ('NOUN', 'VERB'): 2, ('NOUN', 'ADJ'): 1}
  ('ADJ', 'ADJ') 2
  ('NOUN', 'ADJ') 1
  ('NOUN', 'NOUN') 34
  ('NOUN', 'VERB') 2
  ('VERB', 'NOUN') 41
  ('VERB', 'VERB') 17
fr {('NOUN', 'NOUN'): 75, ('VERB', 'VERB'): 36, ('DET', 'DET'): 1, ('VERB', 'NOUN'): 64, ('ADJ', 'ADJ'): 2, ('VERB', 'PREP'): 1, ('NOUN', 'ADJ'): 1, ('PRON', 'PRON'): 2, ('NOUN', 'VERB'): 3}
  ('ADJ', 'ADJ') 2
  ('DET', 'DET') 1
  ('NOUN', 'ADJ') 1
  ('NOUN', 'NOUN') 75
  ('NOUN', 'VERB') 3
  ('PRON', 'PRON') 2
  ('VERB', 'NOUN') 64
  ('VERB', 'PREP') 1
  ('VERB', 'VERB') 36
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -l reports/rapport-gold-anglais.md reports/pensee-gold-anglais.json 2>&1; echo '---'; git status --short reports/ | grep -E \"gold-anglais\" || true", "description": "Check target files do not exist"}`

  ```
ls: cannot access 'reports/rapport-gold-anglais.md': No such file or directory
ls: cannot access 'reports/pensee-gold-anglais.json': No such file or directory
---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections, re, hashlib, pathlib\nraw=json.load(open('tools/tests/linguistique/gold_reel.json'))\nps=raw['phrases']\nprint('sha gold',hashlib.sha256(pathlib.Path('tools/tests/ … [3979 caractères tronqués]`

  ```
sha gold 05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11
==================== en ====================
phrases 204 tokens 1117 segments 686
doublons [('Paul sees Marie; he speaks to her.', ['r336', 'r358'])]
mots span faux 0 segments span faux 0 chevauchements 0 bornes non-token 0
cibles absentes 0 cibles non-token 0 cible dans son segment 0 []
segments à cible 85 chaînes cibles 92 multi-cibles 7
  multi [('r038', 'GP', 'to eat', ['ready', 'mouse']), ('r040', 'GP', 'in the park', ['play', 'children']), ('r067', 'GP', 'in the garden', ['grow', 'flowers']), ('r108', 'GP', 'on the roof', ['climbs', 'cat']), ('r156', 'GP', 'in the water', ['swims', 'fish']), ('r162', 'GP', 'on the wall', ['hung', 'painting']), ('r166', 'GP', 'on the train', ['get', 'travelers'])]
phrases avec PONCT 3 ['r427', 'r432', 'r422']
tokens hors segment 23 phrases 20 par POS {'ADV': 7, 'NOUN': 1, 'CONJ': 3, 'AUX': 1, 'PRON': 10, 'VERB': 1}
phrases avec ponctuation non tokenisée 201 ex [('r021', '.'), ('r022', '.'), ('r023', '.'), ('r024', '.'), ('r025', '.')]
REL cible != tête GN gauche (élision gérée) 0 []
==================== fr ====================
phrases 228 tokens 1258 segments 759
doublon
… [1169 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, types, pathlib, subprocess, collections\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\npath=pathlib.Path('tools/bloc_ling … [724 caractères tronqués]`

  ```
en prédits {'GV': 323, 'GN': 164, 'GP': 34} gold {'GN': 321, 'GV': 259, 'GP': 40, 'SUB': 26, 'REL': 28, 'ADJ': 18, 'ADV': 8, 'PONCT': 2}
fr prédits {'GN': 473, 'GV': 361, 'GP': 88, 'SUB': 38, 'REL': 66} gold {'GN': 507, 'GV': 453, 'GP': 65, 'SUB': 44, 'REL': 46, 'ADJ': 17, 'ADV': 22, 'PONCT': 7}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, types, pathlib, subprocess\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\npath=pathlib.Path('tools/bloc_linguistique.py') … [996 caractères tronqués]`

  ```
en base 0.7343 patch 0.8031 delta 0.0688 ouvert 0.5571 -> 0.6982
fr base 0.7518 patch 0.776 delta 0.0242 ouvert 0.6235 -> 0.6692
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, types, pathlib, subprocess\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\npath=pathlib.Path('tools/bloc_linguistique.py') … [971 caractères tronqués]`

  ```
en base pos 0.7343 f1 0.121 labels 28 cov 0.3182 exact 28 top1 28 topk 28
en patch pos 0.8031 f1 0.121 labels 28 cov 0.3182 exact 28 top1 28 topk 28
fr base pos 0.7518 f1 0.3786 labels 117 cov 0.7748 exact 113 top1 115 topk 114
fr patch pos 0.776 f1 0.3786 labels 117 cov 0.7748 exact 113 top1 115 topk 114
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'tools/tests/linguistique')\nimport evaluer_gold as eg\nps=eg.charger()\nfor lg in ('en','fr'):\n    rows=[p for p in ps if p['langue']==lg]\n     … [562 caractères tronqués]`

  ```
en phrases 210 tokens 1148 segments 702 target segs 88 target strings 97
 par source Counter({'reel': 204, 'hand': 6})
fr phrases 402 tokens 2031 segments 1161 target segs 151 target strings 185
 par source Counter({'reel': 228, 'synthetique': 160, 'hand': 14})
total 612 1863 3179
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, types, pathlib, subprocess\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\npath=pathlib.Path('tools/bloc_linguistique.py') … [711 caractères tronqués]`

  ```
r032 'The car is fast.' -> GV 'is fast' 8 15
r245 'When you arrive, call me.' -> GV 'call me' 17 24
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport math\ndef wilson(k,n,z=1.96):\n    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d\n    return round(100*(c-h),1),round(100*(c+h),1),round(100*p,1)\nfor k,n,label in [(28,88,'en co … [249 caractères tronqués]`

  ```
en couv 28 88 (23.0, 42.1, 31.8)
fr couv 117 151 (70.2, 83.4, 77.5)
en exact span 28 28 (87.9, 100.0, 100.0)
fr exact span 113 117 (91.5, 98.7, 96.6)
en POS 843 1148 (70.8, 75.9, 73.4)
fr POS 1527 2031 (73.3, 77.0, 75.2)
en reel couv 28 85 (23.9, 43.5, 32.9)
fr reel couv 78 86 (82.7, 95.2, 90.7)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport math\ndef wilson(k,n,z=1.96):\n    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d\n    return round(100*(c-h),1),round(100*(c+h),1),round(100*p,1)\nfor k,n,label in [(27,85,'en re … [169 caractères tronqués]`

  ```
en reel couv 27 85 (22.8, 42.3, 31.8)
fr reel couv 78 86 (82.7, 95.2, 90.7)
en reel perdus 58 85 (57.7, 77.2, 68.2)
fr reel perdus 8 86 (4.8, 17.3, 9.3)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nen=[p for p in ps if p['langue']=='en']\ncop={'is','are','was','were'}\nfused=[]; split=[ … [1485 caractères tronqués]`

  ```
copule GV fusionné 14 [('r032', 'is fast'), ('r034', 'is exciting'), ('r035', 'is out'), ('r036', 'is maybe tired'), ('r038', 'is ready'), ('r074', 'is long'), ('r075', 'is beautiful'), ('r078', 'is open'), ('r112', 'is calm'), ('r114', 'was long'), ('r115', 'is small'), ('r118', 'is delicious'), ('r162', 'is hung'), ('r174', 'is dark')]
copule GV + attribut séparé 24 [('r204', 'is', 'GN', 'my father'), ('r214', 'is', 'ADJ', 'good'), ('r217', 'is', 'ADJ', 'absent'), ('r220', 'is', 'ADJ', 'black'), ('r236', 'is', 'ADJ', 'small'), ('r241', 'was', 'ADJ', 'beautiful'), ('r243', 'is', 'ADJ', 'old'), ('r246', 'is', 'ADJ', 'mean'), ('r248', 'is', 'GN', 'my sister'), ('r250', 'is', 'ADV', 'far'), ('r278', 'is', 'ADJ', 'fresh'), ('r283', 'is', 'GN', 'my friend'), ('r285', 'is', 'ADJ', 'big'), ('r287', 'is', 'ADJ', 'blue'), ('r289', 'is', 'ADJ', 'quiet'), ('r291', 'is', 'GN', 'mine'), ('r293', 'is', 'ADV', 'here'), ('r297', 'is', 'ADJ', 'rare'), ('r299', 'is', 'ADJ', 'old'), ('r300', 'is', 'ADJ', 'small'), ('r328', 'is', 'ADJ', 'red'), ('r362', 'is', 'ADJ', 'red'), ('r370', 'is', 'ADJ', 'old'), ('r397', 'is', 'ADJ', 'hungry')]
adverbes dans GV 10 [('r035', 'is out', 'out'), ('r036', 'is mayb
… [703 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nfor lg in ('en','fr'):\n    print('='*12,lg)\n    bad=collections.Counter(); ex=collectio … [1057 caractères tronqués]`

  ```
============ en
segments incohérents {}
============ fr
segments incohérents {}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl, evaluer_gold as eg\nh=bl.Heuristique()\nfor w in ('talks','brother','t … [387 caractères tronqués]`

  ```
talks _pos= NOUN _est_verbe= True
brother _pos= VERB _est_verbe= False
teacher _pos= VERB _est_verbe= False
letter _pos= VERB _est_verbe= False
morning _pos= VERB _est_verbe= False
flower _pos= VERB _est_verbe= True
bus _pos= NOUN _est_verbe= True
leaves _pos= NOUN _est_verbe= True
open _pos= VERB _est_verbe= True
a _pos= DET _est_verbe= True
As _pos= NOUN _est_verbe= True
gold talks {'VERB'}
gold brother {'NOUN'}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, collections\nsys.path.insert(0,'tools/tests/linguistique')\nimport evaluer_gold as eg\nps=[p for p in eg.charger() if p['langue']=='en']\nby=collections.defaultdict(list)\nfor p … [364 caractères tronqués]`

  ```
VERB ['barks', 'believe', 'belongs', 'call', 'climbs', 'continue', 'cries', 'danced', 'eat', 'falls', 'flows', 'fly', 'get', 'goes', 'grow', 'hung', 'know', 'leave', 'leaves', 'listen', 'listens', 'opens', 'passes', 'play', 'plays', 'rains', 'reads', 'runs', 'said', 'saw', 'says', 'sings', 'sleeps', 'smiles', 'stay', 'stayed', 'swims', 'talks', 'think', 'wait', 'works', 'writes'] 58
NOUN ['bird', 'book', 'boy', 'bread', 'bridge', 'car', 'cat', 'children', 'city', 'day', 'dog', 'duck', 'film', 'fish', 'flower', 'flowers', 'girl', 'house', 'man', 'mouse', 'painting', 'person', 'place', 'student', 'table', 'travelers', 'village'] 37
ADJ ['ready'] 2
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 -c \"\nimport json\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nfor lg in ('en','fr'):\n    rows=[p for p in ps if p['langue']==lg]\n    print(lg,'coref phrases',sum(1 f … [98 caractères tronqués]`

  ```
en coref phrases 44 / 204
fr coref phrases 47 / 228
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\npos_hard={'r291','r328','r363','r422','r218','r313','r250'}\nthat={'r034','r074','r114'}\nmissing={'r328','r336','r342','r358','r363','r367'}\nmissing_verb={'r336','r342','r358','r367'}\nroles_clear={'r165','r239'}\ … [762 caractères tronqués]`

  ```
base16 16 ['r028', 'r102', 'r165', 'r218', 'r239', 'r247', 'r250', 'r291', 'r313', 'r328', 'r336', 'r342', 'r358', 'r363', 'r367', 'r422']
+that 19 ['r028', 'r034', 'r074', 'r102', 'r114', 'r165', 'r218', 'r239', 'r247', 'r250', 'r291', 'r313', 'r328', 'r336', 'r342', 'r358', 'r363', 'r367', 'r422']
+coref 24 ['r028', 'r034', 'r074', 'r102', 'r114', 'r165', 'r218', 'r239', 'r247', 'r250', 'r291', 'r313', 'r328', 'r333', 'r336', 'r340', 'r341', 'r342', 'r358', 'r361', 'r363', 'r367', 'r368', 'r422']
+deb 25 ['r028', 'r034', 'r074', 'r102', 'r114', 'r165', 'r180', 'r218', 'r239', 'r247', 'r250', 'r291', 'r313', 'r328', 'r333', 'r336', 'r340', 'r341', 'r342', 'r358', 'r361', 'r363', 'r367', 'r368', 'r422']
missing all 6
overlap missing/pos {'r328', 'r363'}
coref overlap {'r336', 'r358'}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' docs/methode/resultats.md", "description": "Read results method guide"}`

  ```
# Ce qu'un résultat doit porter

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant d'écrire une fiche**, un JSON de
> résultats, ou un message de commit.

## Les cinq pièces d'un résultat

1. **Le chiffre** — la valeur, avec son [unité](../theorie/glossaire/entrees/unite.md) et son arrondi utile (jamais plus de chiffres que l'instrument n'en
   [porte](../theorie/glossaire/entrees/porte.md)) ;
2. **La mesure qui le produit** — le calcul exact, la métrique ([chrF](../theorie/glossaire/entrees/chrf.md), précision, rappel, [AUC](../theorie/glossaire/entrees/auc.md)…), et ce qu'elle ne
   mesure pas ;
3. **Le dispositif** — quel [corpus](../theorie/glossaire/entrees/corpus.md) (et sa provenance), quel modèle (taille, [quantification](../theorie/glossaire/entrees/quantification.md), date de coupure),
   quelles **couches de neurones** sondées, quel découpage, **quelle unité de mesure** (unité de sens ou unité
   grammaticale ; si c'est un [jeton](../theorie/glossaire/entrees/jeton.md), le dire comme **technique**), quels réglages (prompt, gabarit, longueur de
   sortie, graine) ;
4. **Le [contrôle négatif](../theorie/glossaire/entrees/controle-negatif.md)
… [2500 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Writing the JSON audit artifact with metrics, spans and anomalies

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, pathlib\n\nd = {\n \"version\": 1,\n \"date\": \"2026-11-05\",\n \"ligne\": \"B13\",\n \"objet\": \"audit de la qualité du gold anglais (210 phrases sur 612)\",\n \"snapshot\": … [22058 caractères tronqués]`

  ```
écrit reports/pensee-gold-anglais.json 22777 octets
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/pensee-gold-anglais.json > /dev/null && echo 'JSON valide' && python3 -c \"\nimport json\nd=json.load(open('reports/pensee-gold-anglais.json'))\nprint(list(d))\nprint('verdict',json.dumps(d['verdict'],ens … [154 caractères tronqués]`

  ```
JSON valide
['version', 'date', 'ligne', 'objet', 'snapshot', 'gold', 'metriques', 'spans', 'cibles_en', 'analyseur', 'anomalies', 'controles', 'verdict', 'recommandation']
verdict {
 "gold_structurel": "sain : 0 span faux, 0 chevauchement, 0 cible absente/non-token, 0 GN avalant un verbe",
 "gold_anomalies": "25/210 phrases (11,9 %), dont 16 (7,6 %) sur les couches mesurées ; 10 tags POS divergents, 6 GP sans cible, 3 rôles",
 "anglais_echec": "60/94 spans perdus, 100 % des REL et SUB anglais ; la cause est la segmentation, pas le gold",
 "cibles": "97/97 tokens exacts, 0 multi-mots, 0 lemme ; POS gold 97/97 correct ; tête réduite de surface (saw, talks), pas texte complet",
 "est_verbe": "83,5 % d'accord avec le POS gold sur les cibles ; 15 FN, 1 FP (flower) ; garder le POS gold comme référence",
 "v2_v3": "v2 (137/145) → v3 (141/145) ; l'anglais est inchangé (28/28 labels, 60 spans)",
 "recommandation_principale": "segmenter l'anglais (S language-aware ou chunker anglais) avant de retoucher le gold"
}
anomalies compte {'total_en': 210, 'couches_mesurees': 16, 'avec_convention_that': 19, 'avec_coref': 24, 'avec_role_discutable': 25, 'taux_25': 0.119, 'liste_25': ['r028', 'r034', 
… [184 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport json, collections\nps=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nen=[p for p in ps if p['langue']=='en']\ncop={'is','are','was','were'}\nc=collections.Cou … [618 caractères tronqués]`

  ```
{'agent': 12, 'patient': 28}
agent 12 [('r032', 'The car', 'is fast'), ('r036', 'She', 'is maybe tired'), ('r038', 'The mouse', 'is ready'), ('r078', 'The door', 'is open'), ('r112', 'The sea', 'is calm'), ('r118', 'The cake', 'is delicious'), ('r174', 'The room', 'is dark'), ('r204', 'The man', 'is'), ('r328', 'it', 'is'), ('r362', 'The car', 'is'), ('r370', 'The house', 'is'), ('r397', 'it', 'is')]
patient 28 [('r034', 'The book', 'is exciting'), ('r035', 'The film', 'is out'), ('r074', 'The book', 'is long'), ('r075', 'The city', 'is beautiful'), ('r114', 'The film', 'was long'), ('r115', 'The house', 'is small'), ('r162', 'The painting', 'is hung'), ('r214', 'The book', 'is'), ('r217', 'The student', 'is'), ('r220', 'The cat', 'is'), ('r236', 'The village', 'is'), ('r241', 'The day', 'was'), ('r243', 'The house', 'is'), ('r246', 'The dog', 'is'), ('r248', 'The girl', 'is'), ('r250', 'The place', 'is'), ('r278', 'The bread', 'is'), ('r283', 'The boy', 'is'), ('r285', 'The table', 'is'), ('r287', 'The bird', 'is'), ('r289', 'The place', 'is'), ('r291', 'The book', 'is'), ('r293', 'The person', 'is'), ('r297', 'The flower', 'is'), ('r299', 'The bridge', 'is'), ('r300', 'The house'
… [64 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"sujet_copule\\|snapshot\\|generateur_commit\\|note.*HEAD\" reports/pensee-gold-anglais.json | head", "description": "Locate fields to adjust in JSON"}`

  ```
6: "snapshot": {
12:  "generateur_commit": "523d8c1",
13:  "note": "HEAD dcf7bc91 = v3 ; le worktree (cache chunker) donne des chiffres identiques, vérifié. La v2 (15ee10d3) donnait 137/145 à l'attachement ; la v3 en donne 141/145, anglais inchangé."
914:   "sujet_copule": {
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json", "offset": 6, "limit": 12}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json", "offset": 910, "limit": 14}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json</path>
<type>file</type>
<content>
6:  "snapshot": {
7:   "head": "dcf7bc912caeebe940793888d88723f0bbb57f58",
8:   "head_sujet": "B13 — L'ATTACHEMENT V3 : EXACT 0,9448 → 0,9724, NOMS 29/29 = 1,0 ; R2/R3/R4 DE A9 ; 181/181",
9:   "bloc_head_sha256": "64b7c5204f21e4c230dcd131469187f0c9789e06469f4e19af5f8819f87ab5fa",
10:   "bloc_worktree_sha256": "9da6dee7118cfa576d159ccdf5d1241232e974544cd3a6c5cebaddcbbaccd059",
11:   "gold_reel_sha256": "05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11",
12:   "generateur_commit": "523d8c1",
13:   "note": "HEAD dcf7bc91 = v3 ; le worktree (cache chunker) donne des chiffres identiques, vérifié. La v2 (15ee10d3) donnait 137/145 à l'attachement ; la v3 en donne 141/145, anglais inchangé."
14:  },
15:  "gold": {
16:   "phrases": 612,
17:   "fr": 402,

(Showing lines 6-17 of 1139. Use offset=18 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json</path>
<type>file</type>
<content>
910:     "avec": 3,
911:     "sans": 201,
912:     "note": "tokenisation PONCT seulement dans le dernier bloc"
913:    },
914:    "sujet_copule": {
915:     "agent_ancien": 6,
916:     "patient_recent": 19,
917:     "note": "r032/r036/r078/r112/r118/r174 agent ; r214+ patient ; r362/r370 agent : ce n'est pas une règle unique"
918:    }
919:   },
920:   "coref": {
921:    "phrases_avec_coref": 44,
922:    "suspectes": 6,
923:    "liste": [

(Showing lines 910-923 of 1139. Use offset=924 to continue.)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json", "limit": 28, "offset": 889}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json</path>
<type>file</type>
<content>
889:     "qualite": 6,
890:     "fonction": 22,
891:     "note": "qualité : r034, r035, r074, r075, r114, r115 ; fonction : r204+ (sujet 7, objet 10, lieu 4, temps 1)"
892:    },
893:    "copule": {
894:     "gv_fusionne": 14,
895:     "gv_plus_attribut": 24,
896:     "note": "fusionné : r032, r034, r035, r036, r038, r074, r075, r078, r112, r114, r115, r118, r162, r174 ; séparé : r204+"
897:    },
898:    "adverbes": {
899:     "dans_gv": 10,
900:     "adv_segment": 8,
901:     "hors_segment": 7,
902:     "note": "trois traitements ; ex. play outside (GV), tomorrow (ADV r314), deeply (hors segment r069)"
903:    },
904:    "negation": {
905:     "dans_gv": 2,
906:     "adv_separe": 1,
907:     "note": "r029/r316 dans le GV ; r422 n't en ADV"
908:    },
909:    "ponct": {
910:     "avec": 3,
911:     "sans": 201,
912:     "note": "tokenisation PONCT seulement dans le dernier bloc"
913:    },
914:    "sujet_copule": {
915:     "agent_ancien": 6,
916:     "patient_recent": 19,

(Showing lines 889-916 of 1139. Use offset=917 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json", "old_string": "  \"generateur_commit\": \"523d8c1\",\n  \"note\": \"HEAD dcf7bc91 = v3 ; le worktree (cache chunker) donne des chiffres identiques, vérifié. La v2 (15ee10d3) donnait 137/145 à l'attachem … [350 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json", "old_string": "   \"copule\": {\n    \"gv_fusionne\": 14,\n    \"gv_plus_attribut\": 24,\n    \"note\": \"fusionné : r032, r034, r035, r036, r038, r074, r075, r078, r112, r114, r115, r118, r162, r174 ;  … [273 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json", "old_string": "   \"sujet_copule\": {\n    \"agent_ancien\": 6,\n    \"patient_recent\": 19,\n    \"note\": \"r032/r036/r078/r112/r118/r174 agent ; r214+ patient ; r362/r370 agent : ce n'est pas une règ … [295 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/pensee-gold-anglais.json > /dev/null && echo 'JSON valide'; sha256sum tools/bloc_linguistique.py; git rev-parse HEAD; date", "description": "Validate JSON and check snapshot hashes"}`

  ```
JSON valide
9544f173f92e55ccb6eed7b9f096f4a6bf100449d3b1d7875440a23badbda7ff  tools/bloc_linguistique.py
8281d51e659332154597761b362441dcda164522
jeu 05 nov 2026 15:59:19 EST
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport sys, types, pathlib, subprocess, hashlib\nsys.path.insert(0,'tools/tests/linguistique'); sys.path.insert(0,'tools')\nimport evaluer_gold as eg\npath=pathlib.Path('tools/bloc_linguist … [778 caractères tronqués]`

  ```
HEAD 8281d51e659332154597761b362441dcda164522 sha 9544f173f92e55cc
fr pos 0.7518 f1 0.3786 labels 117 cov 0.7748 top1 115 topk 114 exact 113 topk_exact 114
en pos 0.7343 f1 0.121 labels 28 cov 0.3182 top1 28 topk 28 exact 28 topk_exact 28
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json", "limit": 12, "offset": 6}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json</path>
<type>file</type>
<content>
6:  "snapshot": {
7:   "head": "dcf7bc912caeebe940793888d88723f0bbb57f58",
8:   "head_sujet": "B13 — L'ATTACHEMENT V3 : EXACT 0,9448 → 0,9724, NOMS 29/29 = 1,0 ; R2/R3/R4 DE A9 ; 181/181",
9:   "bloc_head_sha256": "64b7c5204f21e4c230dcd131469187f0c9789e06469f4e19af5f8819f87ab5fa",
10:   "bloc_worktree_sha256": "9da6dee7118cfa576d159ccdf5d1241232e974544cd3a6c5cebaddcbbaccd059",
11:   "gold_reel_sha256": "05d4f6dfae67dc72b714dbef69e8764a811247bc72c31b103bad9603be11ff11",
12:   "generateur_commit": "523d8c1",
13:   "mesure_le": "2026-11-05 ~15:30 EST",
14:   "note": "HEAD dcf7bc91 = v3 ; le worktree (cache chunker) donne des chiffres identiques, vérifié. La v2 (15ee10d3) donnait 137/145 à l'attachement ; la v3 en donne 141/145, anglais inchangé."
15:  },
16:  "gold": {
17:   "phrases": 612,

(Showing lines 6-17 of 1141. Use offset=18 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json", "new_string": " \"snapshot\": {\n  \"head\": \"dcf7bc912caeebe940793888d88723f0bbb57f58\",\n  \"head_mesure\": \"dcf7bc912caeebe940793888d88723f0bbb57f58\",\n  \"head_reverifie\": \"8281d51e659332154597 … [1637 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-gold-anglais.json has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 -m json.tool reports/pensee-gold-anglais.json > /dev/null && echo 'JSON valide' && python3 -c \"\nimport json\nd=json.load(open('reports/pensee-gold-anglais.json'))\nprint(d['snapshot']['head_reverifie'])\nprint(d['anomalies' … [73 caractères tronqués]`

  ```
JSON valide
8281d51e659332154597761b362441dcda164522
{'agent': 12, 'patient': 28, 'note': 'pas de règle unique : r032/r036/r078/r112/r118/r174 agent, r034/r035/r074/r075/r114/r115 et r214+ patient ; r328 « The book » patient mais « it » agent, r362/r370 agent'}
  ```

### 🤖 Assistant

⏵ Writing the English-gold audit report with per-language tables and controls

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md", "content": "# B13 — audit du gold anglais : 25 phrases à corriger, 60/94 spans perdus, et la segmentation est la cause\n\n> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11 … [23019 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md</path>
<type>file</type>
<content>
1: # B13 — audit du gold anglais : 25 phrases à corriger, 60/94 spans perdus, et la segmentation est la cause
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ⚠️ gold
4: > utilisable ; l'échec anglais est la **segmentation**, pas le gold.
5: > **Snapshot** : HEAD `dcf7bc91` (v3) mesuré, revérifié à `8281d51e` ; `bloc_linguistique.py` SHA
6: > `64b7c520…` puis `9544f173…`, chiffres **identiques** ; `gold_reel.json` SHA `05d4f6df…`.
7: > **Dispositif** : [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) et
8: > [`gold_reel.json`](../tools/tests/linguistique/gold_reel.json) (432 phrases réelles : 228 fr, 204 en),
9: > [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`),
10: > [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`Heuristique()`), comparaison des cibles à
11: > `_est_verbe` et au POS gold.
12: > **JSON** : [`pensee-gold-anglais.json`](pensee-gold-anglais.json).
13: 
14: ## 1. Verdict
15: 
16: Le gold anglais **n'est pas la cause principale*
… [23450 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Refining the report: title, convention table, and a few scope labels

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md", "new_string": "# B13 — audit du gold anglais : 25 phrases portent une anomalie, 60/94 spans perdus, et la segmentation est la cause", "old_string": "# B13 — audit du gold anglais : 25 phrases à corriger, … [54 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md", "new_string": "- **La cause est côté analyseur** : le générateur S (`tools/structures/generateur.py`) rend 277 GV\n  anglais (dont 147 couvrent toute la phrase), **0 GN, 0 GP, 0 REL, 0 SUB**, et 2 spans  … [428 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md", "new_string": "| GP dont la cible n'est gouvernée par aucun GV/GN (hors cible ADJ) | 0 (1 ADJ, `r018`) | 0 (1 ADJ, `r038`) |\n| GN contenant un VERB/AUX | 0 | 0 |\n| tags POS en contradiction avec une au … [305 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md", "new_string": "En réel seul, le français ne perd que **8/86** spans (1 aucun, 3 plus larges, 3 plus étroits, 1 coupé),\nl'anglais **58/85** (57 aucun, 1 plus étroit). Les 26 spans français ajoutés par le … [462 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md", "new_string": "| convention | constat | exemples |\n|---|---|---|\n| relative `that` | CONJ (3) dans les blocs anciens, PRON (11) dans les récents | `r034`/`r074`/`r114` vs `r214`+ |\n| rôle REL | `quali … [1508 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md", "new_string": "Les cibles sont des **formes de surface réduites**, pas des textes complets : `saw` (pas `see`), `talks`\n(pas `talk`), `book` (pas `The book`), `ready` pour les deux cas adjectivaux (`r03 … [481 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md", "new_string": "- **Les jugements manuels** (`that`, `sick`, `out`, `front`, `r180`, les coref) peuvent être contestés :\n  un second annotateur pourrait contester la convention `that` (CONJ vs PRON) ou j … [310 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport re, pathlib\np=pathlib.Path('reports/rapport-gold-anglais.md')\ntxt=p.read_text()\nlinks=re.findall(r'\\]\\(([^)]+)\\)',txt)\nprint('liens',len(links))\nfor l in links:\n    if l.sta … [760 caractères tronqués]`

  ```
liens 12
OK  ../tools/tests/linguistique/gold_reel.py
OK  ../tools/tests/linguistique/gold_reel.json
OK  ../tools/tests/linguistique/evaluer_gold.py
OK  ../tools/bloc_linguistique.py
OK  pensee-gold-anglais.json
OK  pensee-gold-anglais.json
OK  ../tools/tests/linguistique/gold_reel.py
OK  ../tools/tests/linguistique/gold_reel.json
OK  ../tools/tests/linguistique/evaluer_gold.py
OK  ../tools/bloc_linguistique.py
OK  rapport-pensee-attachement-v3.md
OK  rapport-pensee-spans.md
tables avec pipes incohérents []
  ```

- **bash** `{"command": "ls -l /tmp/gold_metrics.json 2>/dev/null && rm -f /tmp/gold_metrics.json && echo 'scratch supprimé'; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short reports/ | grep -E \"gold-anglais\"", "description": "Remove scratch file and check new reports"}`

  ```
-rw-r--r--. 1 stephane stephane 14838  5 nov 15:00 /tmp/gold_metrics.json
scratch supprimé
 M reports/rapport-gold-anglais.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short reports/ | grep -i gold; echo '--- ls-files'; git ls-files reports/rapport-gold-anglais.md reports/pensee-gold-anglais.json; echo '--- log'; git log -3 --format='%h %ad %s' --date=iso -- reports/rapport-gold-anglai … [190 caractères tronqués]`

  ```
M reports/rapport-gold-anglais.md
--- ls-files
reports/pensee-gold-anglais.json
reports/rapport-gold-anglais.md
--- log
028c8281 2026-11-05 16:07:04 -0500 B13 — L'AUDIT DU GOLD ANGLAIS (A14) : LE GOLD EST SAIN, LA SEGMENTATION EST LA CAUSE (60/94 SPANS) ; 182/182
--- head content
# B13 — audit du gold anglais : 25 phrases à corriger, 60/94 spans perdus, et la segmentation est la cause

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ⚠️ gold
> utilisable ; l'échec anglais est la **segmentation**, pas le gold.
> **Snapshot** : HEAD `dcf7bc91` (v3) mesuré, revérifié à `8281d51e` ; `bloc_linguistique.py` SHA
> `64b7c520…` puis `9544f173…`, chiffres **identiques** ; `gold_reel.json` SHA `05d4f6df…`.
> **Dispositif** : [`gold_reel.py`](../tools/tests/linguistique/gold_reel.py) et
> [`gold_reel.json`](../tools/tests/linguistique/gold_reel.json) (432 phrases réelles : 228 fr, 204 en),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) (`charger`, `evaluer_bloc`),
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`Heuristique()`), comparaison des cibles à
> `_est_verbe` et au POS gold.
> **JSON** : [`pensee-gold-a
… [441 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat -- reports/rapport-gold-anglais.md reports/pensee-gold-anglais.json; echo '--- report diff'; git diff -- reports/rapport-gold-anglais.md | head -120; echo '--- json diff'; git diff -- reports/pensee-gold-anglais.json  … [72 caractères tronqués]`

  ```
reports/rapport-gold-anglais.md | 44 +++++++++++++++++++++--------------------
 1 file changed, 23 insertions(+), 21 deletions(-)
--- report diff
diff --git a/reports/rapport-gold-anglais.md b/reports/rapport-gold-anglais.md
index 70ad6967..55428ab8 100644
--- a/reports/rapport-gold-anglais.md
+++ b/reports/rapport-gold-anglais.md
@@ -1,4 +1,4 @@
-# B13 — audit du gold anglais : 25 phrases à corriger, 60/94 spans perdus, et la segmentation est la cause
+# B13 — audit du gold anglais : 25 phrases portent une anomalie, 60/94 spans perdus, et la segmentation est la cause
 
 > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ⚠️ gold
 > utilisable ; l'échec anglais est la **segmentation**, pas le gold.
@@ -26,9 +26,10 @@ Le gold anglais **n'est pas la cause principale** des échecs d'attachement angl
   cible (36,8 %). Mais ces 60 échecs sont **des spans**, pas des cibles : sur les 28 segments anglais
   trouvés au bon span (tous des GP), l'attachement exact est **28/28**. Les 54 cibles REL/SUB anglaises
   ne sont jamais évaluées parce que **S ne produit aucun REL/SUB en anglais**.
-- **La cause est côté analyseur** : S rend 277 GV angla
… [6264 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md", "new_string": "| F1 tête | 0,5822 | 0,3614 | 0,5344 | 0,3618 |\n| couverture attachement | 0,7748 | **0,3182** | 0,9070 | **0,3176** |\n| labels au bon span | 117/151 | 28/88 | 78/86 | 27/85 |\n| top1 gl … [699 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'\nimport re, pathlib\np=pathlib.Path('reports/rapport-gold-anglais.md'); txt=p.read_text(); lines=txt.splitlines()\nlinks=re.findall(r'\\]\\(([^)]+)\\)',txt)\nmissing=[l for l in links if not … [738 caractères tronqués]`

  ```
liens manquants []
tables pipes incohérents []
lignes 359
JSON valide
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date; git rev-parse --short HEAD; sha256sum tools/bloc_linguistique.py | cut -c1-16; git status --short reports/rapport-gold-anglais.md reports/pensee-gold-anglais.json; git log -2 --format='%h %ad %s' --date=iso -- reports/rapport-g … [67 caractères tronqués]`

  ```
jeu 05 nov 2026 16:13:25 EST
028c8281
9544f173f92e55cc
 M reports/rapport-gold-anglais.md
028c8281 2026-11-05 16:07:04 -0500 B13 — L'AUDIT DU GOLD ANGLAIS (A14) : LE GOLD EST SAIN, LA SEGMENTATION EST LA CAUSE (60/94 SPANS) ; 182/182
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md", "offset": 69, "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-anglais.md</path>
<type>file</type>
<content>
69: 
70: ## 3. Mesures par langue (`Heuristique()`, HEAD `dcf7bc91`)
71: 
72: | mesure | fr 402 | en 210 | fr réel 228 | en réel 204 |
73: |---|---:|---:|---:|---:|
74: | POS exacte | 0,7518 | 0,7343 | 0,7591 | 0,7278 |
75: | POS fermé | 0,8956 | 0,9031 | 0,8779 | 0,9018 |
76: | POS ouvert | 0,6235 | **0,5571** | 0,6334 | **0,5466** |
77: | F1 syntagmes | 0,3786 | **0,1210** | 0,3654 | **0,1206** |
78: | F1 tête | 0,5822 | 0,3614 | 0,5344 | 0,3618 |
79: | couverture attachement | 0,7748 | **0,3182** | 0,9070 | **0,3176** |
80: | labels au bon span | 117/151 | 28/88 | 78/86 | 27/85 |
81: | top1 global | 0,7616 | 0,3182 | 0,8953 | 0,3176 |
82: | top-k global | 0,7550 | 0,3182 | 0,8953 | 0,3176 |
83: | exact global | 0,7483 | 0,3182 | 0,8953 | 0,3176 |
84: | exact sur span | 0,9658 | **1,0000** | 0,9872 | **1,0000** |
85: | top-k sur span | 0,9744 | 1,0000 | 0,9872 | 1,0000 |
86: | spans perdus | 34/151 | **60/88** | 8/86 | **58/85** |
87: 
88: Lecture : l'écart fr/en est de **−45,7 points de couverture** (plein) et **−58,9 points** (réel seul),
89: alors que l'exac
… [620 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat -- reports/rapport-gold-anglais.md reports/pensee-gold-anglais.json; git status --short reports/rapport-gold-anglais.md reports/pensee-gold-anglais.json", "description": "Final deliverable diff status"}`

  ```
reports/rapport-gold-anglais.md | 47 +++++++++++++++++++++++------------------
 1 file changed, 26 insertions(+), 21 deletions(-)
 M reports/rapport-gold-anglais.md
  ```

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "Audit gold anglais terminé. Livrables : `reports/rapport-gold-anglais.md` + `reports/pensee-gold-anglais.json`.\n\n**Verdict : le gold anglais est structurellement sain ; l'échec anglais est la segmentation, pas le gold.**\n- 0 span fa … [2323 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

### 🤖 Assistant

⏵ Clôture de l'audit gold anglais et livraison du rapport

**Livrables**
- `reports/rapport-gold-anglais.md` — fiche complète (verdict, tableaux fr/en, annotations suspectes, contrôles, limites, recommandation).
- `reports/pensee-gold-anglais.json` — chiffres, spans, cibles, anomalies, contrôles (JSON valide).

**Annotations suspectes : 25 phrases anglaises sur 210 (11,9 %)** portent au moins une anomalie ; **16 (7,6 %)** sur les couches réellement mesurées :
- **10 tags POS divergents** : 7 erreurs probables (`is`×3, `do`, `late`×2, `far`) + 3 dus à la convention `that` (CONJ vs PRON) ;
- **6 GP sans cible** : 4 après un verbe (`r336`, `r342`, `r358`, `r367`), 2 après copule (`r328`, `r363`) ;
- **3 rôles** (2 faux : `r165`, `r239` ; 1 discutable : `r180`), **1 modalité** (`r247`), **3 phrases non grammaticales** (`r028`, `r102`, `r165`), **1 doublon** (`r336`/`r358`), **6 coref** suspectes (hors mesure).

**Écarts fr/en** (HEAD v3 `dcf7bc91`, code `9544f173`, revérifié à `8281d51e`) :

| mesure | fr | en |
|---|---:|---:|
| couverture attachement (plein) | 0,775 | **0,318** |
| couverture (réel seul) | 0,907 | **0,318** |
| exact global | 0,748 | 0,318 |
| exact sur span | 0,966 | **1,000** (28/28, tous GP) |
| spans perdus | 34/151 | **60/88** |

Les 60 spans anglais perdus sont **28/28 REL et 26/26 SUB** : l'anglais représente **60/94 spans perdus (63,8 %)** pour 36,8 % des cibles. Le gold est structurellement sain (0 span faux, 0 chevauchement, 0 cible absente/non-token, 0 GN avalant un verbe ; 97/97 cibles = tokens de surface). La cause est l'analyseur : S ne segmente pas l'anglais (277 GV, 0 GN/GP/REL/SUB, 2/702 exacts) et `_pos` tague 176 VERB gold en NOUN (`talks`→NOUN, `brother`→VERB). `_est_verbe` n'est d'accord que sur 81/97 cibles : garder le POS gold.

**Recommandation** : segmenter l'anglais d'abord (S language-aware ou chunker anglais), puis corriger `_pos` (+6,9 pts simulés, attachement inchangé), puis l'hygiène du gold ; mesurer fr/en séparément ; ne pas ajuster le lexique au gold. La v2 (137/145) est périmée : v3 = 141/145, anglais inchangé.

**Commit** : `028c8281` (A14) a intégré mes deux fichiers pendant l'audit. Mes corrections post-commit du rapport (titre, tableau des conventions, note ADJ, lignes top1/top-k) sont dans le worktree et **non commitées** ; je n'ai rien commité. Le JSON est déjà dans le commit.

