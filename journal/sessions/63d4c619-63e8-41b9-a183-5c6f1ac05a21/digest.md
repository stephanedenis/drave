# Session DSH — relecture

- identifiant : `63d4c619-63e8-41b9-a183-5c6f1ac05a21`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 13:11:54
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, dépôt Python). Mission : **audit de reproductibilité** de la mesure d'attachement du bloc linguistique.

Contexte : `tools/tests/linguistique/evaluer_gold.py` expose `charger()` (gold de 612 phrases) et `evaluer_bloc(nom, bloc, phrases)` ; `tools/bloc_linguistique.py` expose `Heuristique`. Les valeurs publiées le 2026-11-05 sont : cibles 239, labels 145, top1 126, top-k (sous-chaîne) 134, exact 123, top-k strict 88, couverture 0,6067, cibles verbes 63 (60 justes), cibles noms 82 (63 justes), spans perdus 48 REL / 33 SUB / 13 GP.

À faire :
1. Depuis la racine du dépôt, recalcule ces valeurs en Python (`sys.path.insert(0,'.')`, `from tools.bloc_linguistique import Heuristique`, `from tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc`). Pour les spans et les types : itère sur `charger()`, analyse avec `Heuristique()`, et compare les `(type, debut, fin)` des segments gold à ceux des étiquettes de niveau `syntagme`.
2. Compare aux JSON existants : `reports/pensee-attachement-cible.json`, `reports/pensee-conventions.json`, `reports/pensee-topk-strict.json`, `reports/pensee-spans.json`, `reports/pensee-echecs-cible.json`.
3. Écris **uniquement** deux fichiers neufs : `reports/rapport-audit-attachement.md` (fiche : titre, verdict, tableau mesuré / publié / écart, contrôle négatif, limites, fichiers) et `reports/pensee-audit-attachement.json` (les mêmes chiffres).
4. Si une valeur ne reproduit pas, dis-le explicitement — ne l'arrondis pas, ne la « corrige » pas dans les fichiers existants.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé final avec les chiffres mesurés et les écarts constatés.
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

⏵ Exploring the repo and the evaluation scripts before auditing

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short && git branch --show-current && ls reports/ | head -50", "description": "Check git status, branch, and reports dir"}`

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
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rapport.md
MM journal/sessions/MANIFEST.md
MM journal/sessions/aeafe951-9c3d-4bb5-8af7-0246a4f3d51d/digest.md
MM journal/sessions/aeafe951-9c3d-4bb5-8af7-0246a4f3d51d/rapport.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
MM journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
D  journal/sessions/fbdbd6fb-1ebc-4348-a6cc-f10faf76520b/digest.md
D  journal/sessions/fbdbd6fb-1ebc-4348-a6cc-f10faf76520b/rapport.md
 M reports/pensee-quatre-modes.json
 m tools/structures
?? journal/2026-11-05/attention.md
?? journal/sessions/fbdbd6fb-1ebc-4348-a6cc-f10faf76520b/
?? repor
… [1079 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/tests/linguistique/ && wc -l tools/tests/linguistique/evaluer_gold.py tools/bloc_linguistique.py", "description": "List linguistique tests and count lines"}`

  ```
anaphore.py
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
   283 tools/tests/linguistique/evaluer_gold.py
  1881 tools/bloc_linguistique.py
  2164 total
  ```

### 🤖 Assistant

⏵ Reading evaluation script and bloc_linguistique API

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
… [14340 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/pensee-*.json reports/pensee-*.md 2>/dev/null; echo ---; for f in reports/pensee-attachement-cible.json reports/pensee-conventions.json reports/pensee-topk-strict.json reports/pensee-spans.json reports/pensee-echecs-cible. … [93 caractères tronqués]`

  ```
reports/pensee-absents.json
reports/pensee-ac3-alphabeta.json
reports/pensee-adaptive.json
reports/pensee-aleatoire.json
reports/pensee-alternance.json
reports/pensee-anaphore-103.json
reports/pensee-anaphore-68.json
reports/pensee-anaphore-bilan.json
reports/pensee-anaphore-chaines.json
reports/pensee-anaphore-corrige.json
reports/pensee-anaphore-cv-graines.json
reports/pensee-anaphore-cv.json
reports/pensee-anaphore-hybride.json
reports/pensee-anaphore.json
reports/pensee-anaphore-kappa.json
reports/pensee-anaphore-limite.json
reports/pensee-anaphore-meta.json
reports/pensee-anaphore-objets.json
reports/pensee-anaphore-pieges.json
reports/pensee-anaphore-pondere.json
reports/pensee-anaphore-roles.json
reports/pensee-anaphore-semantique.json
reports/pensee-asym.json
reports/pensee-attachement-cible.json
reports/pensee-attachement.json
reports/pensee-audit.json
reports/pensee-banc.json
reports/pensee-bayes2.json
reports/pensee-bayes-appris.json
reports/pensee-bayes.json
reports/pensee-bonne-reponse-voisin.json
reports/pensee-bord-fin.json
reports/pensee-bouge-graines.json
reports/pensee-bouge.json
reports/pensee-bruitee.json
reports/pensee-bruit.json
reports/pensee-candidats-verbes
… [6032 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reading the five existing JSON reports to audit

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in reports/pensee-attachement-cible.json reports/pensee-conventions.json reports/pensee-topk-strict.json reports/pensee-spans.json reports/pensee-echecs-cible.json; do echo \"===== $f\"; cat \"$f\"; echo; done", "description":  … [32 caractères tronqués]`

  ```
===== reports/pensee-attachement-cible.json
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "173/173",
 "gold": 612,
 "cibles": 239,
 "labels": 146,
 "avant": {
  "exact": 94,
  "exact_span": 0.6438,
  "top1": 114,
  "top1_span": 0.7808,
  "verbe": 0.7255,
  "nom": 0.6
 },
 "apres": {
  "exact": 118,
  "exact_span": 0.8082,
  "top1": 122,
  "top1_span": 0.8356,
  "verbe": 0.9412,
  "nom": 0.7368
 },
 "rendement": {
  "top1": 0.5105,
  "topk": 0.5523,
  "exact": 0.4937
 },
 "regle": "REL/SUB → antécédent (tête du GN à gauche, élision séparée) ; GP → verbe du GV",
 "limites": [
  "28 échecs non qualifiés",
  "convention non documentée",
  "top-k lenient",
  "gold 612"
 ]
}

===== reports/pensee-conventions.json
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "172/172",
 "gold": 612,
 "labels": 146,
 "verbe": {
  "cibles": 51,
  "justes": 37,
  "taux": 0.7255
 },
 "nom": {
  "cibles": 95,
  "justes": 57,
  "taux": 0.6
 },
 "tout": {
  "justes": 94,
  "taux": 0.6438
 },
 "limites": [
  "convention du gold non documentée",
  "52 échecs non qualifiés",
  "top-k lenient",
  "gold 612"
 ]
}

===== reports/pensee-topk-strict.json
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes"
… [1507 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"class Heuristique\\|def analyser\\|_est_verbe\\|class Annotation\\|class Etiquette\\|candidats\\|attachement\" tools/bloc_linguistique.py | head -60", "description": "Locate key symbols in bloc_linguistique"}`

  ```
7:    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
19:`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script` et ses `candidats`.
68:class Etiquette:
76:    candidats: list[str] = field(default_factory=list)
86:            "candidats": list(self.candidats), "langue": self.langue,
92:class Annotation:
133:    def analyser(self, texte: str, langue: str | None = None,
428:def _est_verbe(mot: str) -> bool:
472:class Heuristique:
631:            if _est_verbe(m) and _normaliser(m) not in AUXILIAIRES:
634:            if _est_verbe(m):
672:        """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
708:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
716:                       and not _est_verbe(mots[j][2])
721:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
730:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
739:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
746:    def analyser(self, texte: str, langue: str | None = None,
783:                                      
… [2563 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspecting Heuristique, annotation and gold structures

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 60, "limit": 150}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 400, "limit": 100}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
60:     debut: int
61:     fin: int
62: 
63:     def json(self) -> dict:
64:         return {"debut": self.debut, "fin": self.fin}
65: 
66: 
67: @dataclass
68: class Etiquette:
69:     niveau: str
70:     type: str
71:     valeur: str
72:     debut: int
73:     fin: int
74:     source: str = "heuristique"
75:     confiance: float = 0.5
76:     candidats: list[str] = field(default_factory=list)
77:     langue: str = "und"
78:     script: str = SCRIPT_NEUTRE
79:     meta: dict = field(default_factory=dict)
80: 
81:     def json(self) -> dict:
82:         return {
83:             "niveau": self.niveau, "type": self.type, "valeur": self.valeur,
84:             "debut": self.debut, "fin": self.fin, "source": self.source,
85:             "confiance": round(float(self.confiance), 4),
86:             "candidats": list(self.candidats), "langue": self.langue,
87:             "script": self.script, "meta": dict(self.meta),
88:         }
89: 
90: 
91: @dataclass
92: class Annotation:
93:     texte: str
94:     langue: str = "und"
95:     script: str = SCRIPT_NEUTRE
96:     etique
… [5441 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
400: bu cru sue pu voulu dû venue venu partie parti sorti mort née né ouvert offerte souffert couru
401: reçu aperçu déçu attendu entendu répondu perdu rendu vendu descendu monté resté tombé arrivé
402: entré rentré retourné passé tenu obtenu devenu revenu
403: travailles travaillent travaillait regarder regarde regardes regardent regardait écouter écoute
404: écoutes écoutent écoutait aimer aime aimes aiment aimait finir finis finit finissent finissait
405: grandir grandis grandit grandissent ouvrir ouvre ouvres ouvrent ouvrait fermer ferme fermes
406: ferment fermait donner donne donnes donnent donnait chercher cherche cherches cherchent trouvait
407: talk talks talked talking play plays played playing leave leaves left leaving write writes wrote
408: written writing read reads reading listen listens listened listening sleep sleeps slept sleeping
409: grow grows grew grown growing bark barks barked barking run runs ran running walk walks walked
410: walking sing sings sang sung singing dance dances danced dancing work works worked working
411: watch watches watched 
… [4317 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Searching for the scripts that generated these reports

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"pensee-spans\\|pensee-topk-strict\\|pensee-attachement-cible\\|pensee-conventions\\|pensee-echecs-cible\" --include=*.py --include=*.sh --include=*.md . | head -40", "description": "Find generators/references of the repor … [4 caractères tronqués]`

  ```
./reports/README.md
./reports/rapport-pensee-spans.md
./reports/rapport-pensee-conventions.md
./reports/rapport-pensee-attachement-cible.md
./reports/rapport-pensee-echecs-cible.md
./reports/rapport-pensee-topk-strict.md
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
./journal/sessions/63d4c619-63e8-41b9-a183-5c6f1ac05a21/digest.md
./journal/sessions/ff7e786c-3ece-4eae-864e-19dddfead93c/digest.md
./journal/2026-11-05/docs.md
./journal/2026-11-05/mesures.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib\nfor n in [\"gold.json\",\"gold_reel.json\",\"gold_synthetique.json\",\"gold_gele.json\"]:\n    p=pathlib.Path(\"tools/tests/linguistique\")/n\n    d=json.loads(p.read_text(encoding=\"utf-8\"))\ … [100 caractères tronqués]`

  ```
gold.json phrases= 20
gold_reel.json phrases= 432
gold_synthetique.json phrases= 160
gold_gele.json phrases= 602
  ```

### 🤖 Assistant

⏵ Reading companion markdown sheets for measurement protocol

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in reports/rapport-pensee-attachement-cible.md reports/rapport-pensee-conventions.md reports/rapport-pensee-topk-strict.md reports/rapport-pensee-spans.md reports/rapport-pensee-echecs-cible.md; do echo \"===== $f\"; cat \"$f\" … [62 caractères tronqués]`

  ```
===== reports/rapport-pensee-attachement-cible.md
# B13 — l'attachement ciblé : l'exact passe de 0,6438 à 0,8082

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **173/173 portes** : la nature de la cible dépend du **type du segment**, et la règle le dit
> maintenant : pour un **REL/SUB**, l'attachement est l'**antécédent** (la tête du GN à gauche,
> élision séparée : `L'homme` → `homme`) ; pour un **GP**, c'est le **verbe du GV** le plus
> proche. Sur les 146 segments au bon span : **exact 94 → 118** (0,6438 → **0,8082**), top1
> 0,8356, top-k 0,9041. Par convention : **verbes 48/51 (0,9412)**, **noms 70/95 (0,7368)**.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_tete_nom`),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-attachement-cible.json`](pensee-attachement-cible.json).

## 1. Avant / après (146 segments au bon span)

| mesure | avant | **attachement ciblé** | écart |
|---|---:|---:|---:|
| top1 | 114 (0,7808) | **122 (0,8356)** | +8 |
| top-k | 132 (0,9041) | 132 (0,9041) | 0 |
| **exact** | **94 (0,6
… [14039 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Running the canonical evaluer_bloc measurement on the 612 phrases

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'.')\nfrom tools.bloc_linguistique import Heuristique\nfrom tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc\nphrases = charger()\nprint(\"phrases\", len(ph … [460 caractères tronqués]`

  ```
phrases 612
{
 "cibles": 239,
 "labels": 145,
 "top1": 126,
 "topk": 134,
 "exact": 123,
 "top1_taux": 0.5272,
 "topk_taux": 0.5607,
 "exact_taux": 0.5146,
 "top1_taux_span": 0.869,
 "topk_taux_span": 0.9241,
 "topk_exact": 88,
 "topk_exact_taux": 0.3682,
 "topk_exact_taux_span": 0.6069,
 "exact_taux_span": 0.8483,
 "verbe": {
  "cibles": 63,
  "justes": 60,
  "taux": 0.9524
 },
 "nom": {
  "cibles": 82,
  "justes": 63,
  "taux": 0.7683
 },
 "couverture": 0.6067
}
attachement_tete {"cibles": 145, "labels": 145, "top1": 126, "topk": 134, "top1_taux": 0.869, "topk_taux": 0.9241, "couverture": 1.0}
syntagme {"precision": 0.3154, "rappel": 0.2619, "f1": 0.2862, "tp": 488, "fp": 1059, "fn": 1375, "tete": {"precision": 0.5862, "rappel": 0.4342, "f1": 0.4989, "tp": 809, "fp": 571, "fn": 1054}}
pos 0.7455 tokens 3179
[stderr]

real	0m0,544s
user	0m0,518s
sys	0m0,025s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short tools/structures tools/bloc_linguistique.py tools/tests/linguistique/ && git -C tools/structures status --short 2>/dev/null | head -5; git log -1 --format='%H %ad %s' --date=iso", "description": "Check code state a … [21 caractères tronqués]`

  ```
m tools/structures
 M donnees/paragraphes-validations.jsonl
56d70431dbdeac1faa6bf06959ffea8dc4ba4e23 2026-11-05 13:09:13 -0500 ÉTAT — B13 177/177, TRIM T0 ; LA TRANCHE SOUS-AGENTS CONTINUE
  ```

### 🤖 Assistant

⏵ Computing lost spans by type against gold segments

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 - <<'PY'\nimport sys, json\nfrom collections import Counter\nsys.path.insert(0,'.')\nfrom tools.bloc_linguistique import Heuristique\nfrom tools.tests.linguistique.evaluer_gold import charger\nphrases = charger()\nh = He … [2137 caractères tronqués]`

  ```
segments total par type: {'GN': 828, 'GV': 712, 'GP': 105, 'SUB': 70, 'REL': 74, 'ADJ': 35, 'ADV': 30, 'PONCT': 9}
sans cible: {'GN': 828, 'GV': 712, 'ADJ': 35, 'ADV': 30, 'GP': 9, 'PONCT': 9, 'SUB': 1} avec cible: 239
perdus par type: {'GP': 13, 'SUB': 33, 'REL': 48} total: 94
categories: {'plus_large': 25, 'aucun': 65, 'plus_etroit': 4} total: 94

 ('GP', 'aucun') 5
    ('The duck is ready to eat.', {'type': 'GP', 'texte': 'to eat', 'role': 'but', 'debut': 18, 'fin': 24, 'cibles': ['ready', 'duck'], 'cible': 'ready'}, [])
    ('It rains since yesterday.', {'type': 'GP', 'texte': 'since yesterday', 'role': 'temps', 'debut': 9, 'fin': 24, 'cibles': ['rains'], 'cible': 'rains'}, [])

 ('GP', 'plus_etroit') 2
    ('Les oiseaux volent au-dessus du lac.', {'type': 'GP', 'texte': 'au-dessus du lac', 'role': 'lieu', 'debut': 19, 'fin': 35, 'cibles': ['volent'], 'cible': 'volent'}, [(29, 35)])
    ('We wait for the bus.', {'type': 'GP', 'texte': 'for the bus', 'role': 'cible', 'debut': 8, 'fin': 19, 'cibles': ['wait'], 'cible': 'wait'}, [(8, 15)])

 ('GP', 'plus_large') 6
    ('Le chien du voisin aboie la nuit.', {'type': 'GP', 'texte': 'du voisin', 'role': 'possession', 'debut': 9, 'fin'
… [1800 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Searching the autotest for the exact span-category protocol

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"plus_etroit\\|plus large\\|plus_large\\|coupe\\|perdus\\|spans\" tools/pensee/autotest.py | head -40; echo ---; grep -n \"RELATIFS\\|_tete_nom\\|_verbe_dans\" tools/bloc_linguistique.py | head", "description": "Find span c … [29 caractères tronqués]`

  ```
12:  T6  alpha-bêta décide               gagner en un coup, bloquer, couper ; le minimax exact
14:  T6  alpha-bêta décide               gagner en un coup, bloquer, couper ; le minimax exact
190:    """Gagner en un coup, bloquer, et couper : le minimax exact visite plus de nœuds."""
207:    coupe = ab.noeuds < mm.noeuds and ab.coupes > 0
208:    ok = gagne and win == 2 and bloque and rate and coupe
210:                f"alpha-bêta {ab.noeuds} nœuds/{ab.coupes} coupes vs minimax {mm.noeuds}")
1819:    return abs(fid - 1.0) < 1e-9, f"restitution POS + spans : {round(fid, 4)}"
2406:def t166_spans() -> tuple[bool, str]:
2407:    """Les spans perdus : 48 REL, 33 SUB, 12 GP."""
2415:        spans = {(e.type, e.debut, e.fin) for e in a.etiquettes if e.niveau == "syntagme"}
2420:            if (s["type"], s["debut"], s["fin"]) not in spans:
2423:        f"spans : {cats['REL']} REL, {cats['SUB']} SUB, {cats['GP']} GP")
2427:    """Le dénominateur : rendement global (÷ 239) et exactitude spans (÷ 146)."""
2435:        f"dénominateur : spans {a['top1_taux_span']} / {a['topk_taux_span']} / {a['exact_taux_span']}")
2664:              ("T118 restitution spans", t118_miroir_espaces()),
2712:      
… [758 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"plus_etroit\\|plus_large\" --include=*.py tools/ | head -20", "description": "Search scripts for span categories"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2360,2460p' tools/pensee/autotest.py", "description": "Read T165-T168 autotests"}`

  ```
"""Les échecs de l'attachement : 94 de span, 33 de cible."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger
    h = bl.Heuristique()
    span = cible = 0
    for p in charger():
        a = h.analyser(p["texte"], p["langue"])
        labels = {(e.type, e.debut, e.fin): e for e in a.etiquettes if e.niveau == "syntagme"}
        for s in p["segments"]:
            cibles = s.get("cibles") or ([s["cible"]] if s.get("cible") else [])
            if not cibles:
                continue
            e = labels.get((s["type"], s["debut"], s["fin"]))
            if e is None:
                span += 1
                continue
            if not any(any(c in nom for c in cibles) for nom in (e.candidats or [])):
                cible += 1
    return span == 94 and cible == 11, (
        f"échecs : {span} de span, {cible} de cible (33 avant les correctifs)")


def t164_verbe_gv() -> tuple[bool, str]:
    """Le verbe du GV-phrase : le POS VERB, pas le dernier mot."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    h = bl.Heuristique()
    a = h.analyser("The boy saw the cat i
… [3595 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '700,900p' tools/bloc_linguistique.py", "description": "Read syntagme generation and GP handling"}`

  ```
role = "groupe nominal"
                # le passif sans `par` : GN + AUX (être) + participe → le sujet est un patient
                if j < len(mots) and _normaliser(mots[j][2]) in {
                        "est", "sont", "était", "étaient", "été", "sera", "seront",
                        "suis", "es", "sommes", "êtes"}:
                    role = "patient"
                segments.append({"type": "GN", "role": role, "niveau": 0,
                                 "debut": d, "fin": mots[j - 1][1],
                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
                i = j
                continue
            if typ == "mot" and n in lex.get("PREP", set()) and i + 1 < len(mots):
                j = i + 1
                # le GP s'arrête au verbe ou au relatif : « de la voisine | dort » et non
                # « de la voisine dort » (mesuré : 25 spans « plus large » sur le gold).
                while (j < len(mots) and mots[j][3] == "mot"
                       and not _est_verbe(mots[j][2])
                       and _normaliser(mots[j][2]) not in RELATIFS):
                    j += 1
                segments.append({"type": "GP", "role": _role_gp(
… [11110 caractères tronqués]
  ```

