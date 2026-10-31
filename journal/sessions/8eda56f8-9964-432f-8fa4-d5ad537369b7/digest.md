# Session DSH — relecture

- identifiant : `8eda56f8-9964-432f-8fa4-d5ad537369b7`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 15:11:33
- agent : standard


## Tour 1

### 👤 Utilisateur

Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A17 : compléter M9 par des **lésions croisées, sham et dose-réponse**, sans modifier les modules existants.

État :
- `tools/cerveau/lesion.py` : `batterie_lesions()` CPU ; M2 réel `voies.py` validé (action 98,63→12,33, de 91,78→2,05).
- M2 `voies.py`, M5 `predictif.py`, M6 `gating.py`, M8 `sommeil.py`.
- Tests : `PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools` → 127 OK.

Objectif :
1. Créer `tools/cerveau/lesion_complet.py` : lésions **une par module** et **doubles** (M2+M5, M2+M6, M5+M6), **sham** (même opération sans effet) et **dose-réponse** (capacité 0/4/8/12/16, contexte 0/25/50/75/100 %).
2. Mesurer `intacte − lésée`, double dissociation M2 ventrale/dorsale, M5 plateau/transitions, et **récupération** après restauration.
3. Écrire `/tmp/a17-m9-complet.json` et `.md` ; si une lésion n'a aucun effet, le dire.

Contraintes :
- Crée uniquement `tools/cerveau/lesion_complet.py` et `tools/cerveau/tests/test_lesion_complet.py` ; ne modifie pas les modules existants, docs, reports, journal, `batterie.py`, git.
- Pas de `git add/commit/checkout`.
- CPU/GPU si nécessaire. Sois autonome, timebox, autocritique. Réponds avec un résumé et les chemins.
Your parent agent id is "f0969e87-af0c-43b1-93cf-f278d9c90846". Before you finish, send your result to that agent with send_message({ agent_id: "f0969e87-af0c-43b1-93cf-f278d9c90846", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

# Directives de l'agent — Drave

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs
> unifiés (**49 portes, 8 chapitres, 181 fichiers / 248 JSON, 54 documents**), chemins archivés
> corrigés (`docs/archive/`), B10–B12 réintégrés dans les cartes. **Les règles et le routage
> ci-dessous ne changent pas.** Source de vérité : `docs/en-cours.md` (état)
> et `docs/roadmap.md` (plan). Ne pas recopier ces chiffres dans un nouveau document.

> **Porte d'entrée.** Lis ce fichier en entier (2 min) : il porte la **vision**, les règles non négociables et le
> **routage** vers le document de chaque tâche. Le détail n'est pas ici : il est dans [`docs/agent/`](docs/agent/)
> (tableau § 3). L'**état courant** est dans [`docs/en-cours.md`](docs/en-cours.md) ; la **roadmap** dans
> [`docs/roadmap.md`](docs/roadmap.md) ; le récit daté dans [`journal/`](journal/).

## 1. La vision (l'essentiel)

**Drave est une vision de l'IA centrée sur les flots de données, pas sur le calcul brut.** Les activations d'un
réseau sont des **faits** regroupés en **listes valuées poussées** vers leurs lecteurs : le coût du calcul devient proportionnel à l'**activité**, et le modèle devient **décomposable**, **répartissable** et **observable**. Le projet a pour principe que la structure bat la taille. Construire le moteur et modèle optimisé qui rend cette structure observable, décomposable, répartissable et rejouable permet d'atteindre de nouveaux sommets. Bref, révolutionner l'IA avec une approche par bus d'événements où chaque bloc fonctionnel est optimisable, comparable et substituable par des alternatives ayant des architectures différentes. e.g. Blocs neuronaux là où l'intuition est un avantage, blocs computationnels classiques pour les opérations où l'informatique classique est plus fiable et performante.

Le projet est né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de
les **combiner**, de les **décomposer en couches et grappes de neurones** exécutables par du matériel divers, voire
**distribué en réseau**, de les **diagnostiquer et faire évoluer** en étudiant leurs **flux**, et de **rejouer à
volonté** des événements.


## 2. Les règles non négociables

1. **Rangement** : `docs/` = état, vision, concepts (ce qui reste vrai quand les chiffres changent) ; `reports/` =
   résultats mesurés, fiches, JSON ; `journal/` = récit daté ; `data/` = corpus. *Un résultat qui traîne dans
   `docs/` **déménage**.* → [`docs/agent/rangement.md`](docs/agent/rangement.md)
2. **Un résultat** porte le chiffre, la mesure, le dispositif, un **contrôle négatif**, et **ce qui pourrait le
   rendre faux** — puis un **commit**, la **fiche** dans `reports/`, le **récit** dans `journal/`, l'**état** dans
   `docs/en-cours.md`, et il **nomme sa ligne de roadmap** (A… / B…). *Sans contrôle négatif, ce n'est pas un
   résultat.* → [`docs/agent/resultats.md`](docs/agent/resultats.md)
3. **Les portes** : `bash tools/toutes-les-portes.sh` ; le registre est dans `$JOURNAUX/registre.txt` (affiché au
   lancement) et le verdict se lit par `awk '$2 != 0'` — **jamais** par les marqueurs ni à travers un tube. Rouges
   structurelles tolérées : **`porte-indice`** et **`porte-melange`** ; toute autre est une régression. →
   [`docs/agent/portes.md`](docs/agent/portes.md)
4. **La revue de documentation** avant chaque commit de clôture : `python3 tools/revue_documentation.py` (et
   `tools/porte-tableaux.sh`) ; **corriger** ce qu'elle signale. → [`docs/agent/rangement.md`](docs/agent/rangement.md)
5. **Panini et Nipada** à chaque cycle : lire ce qui a bougé chez eux, confronter ; la théorie va dans
   [`docs/genealogie-des-langues.md`](docs/genealogie-des-langues.md), **jamais** les chiffres. Leur avertissement :
   la surface capte **l'époque** (β +0,138) bien plus que la **filiation** (β +0,049) — contrôler la date dans tout
   test de style, la surface dans tout test de famille. → [`docs/agent/panini-nipada.md`](docs/agent/panini-nipada.md)
6. **Le miroir entrée/sortie** : toute mesure d'entrée se double d'une mesure de **sortie** (restitution, boucle) ;
   la **fluidité n'est pas la fidélité**. → [`docs/agent/miroir.md`](docs/agent/miroir.md)
7. **La roadmap** ([`docs/roadmap.md`](docs/roadmap.md)) : chaque chantier a une **prochaine action** ; l'ordre est
   celui de la **valeur** et des **dépendances**, jamais celui d'une date. Un chantier est **fini** quand il est
   mesuré, écrit et committé ; il est alors **marqué** dans la roadmap et le suivant est désigné.
8. **Ne jamais bloquer, ne jamais rester en attente** : une question humaine se **consolide** dans
   `docs/en-cours.md` et on **continue** ; si une ligne est bloquée (corpus, compte, matériel), on prend la suivante
   — la **file « jamais en attente »** de la roadmap. → [`docs/agent/ressources.md`](docs/agent/ressources.md)
9. **Les illustrations sont des SVG.** Aucun **ASCII art** : pas de `┌─┬─┐`, pas de flèches `──►`
   dans un bloc de code. Un schéma est un fichier **`.svg`** (directement, ou converti depuis
   Mermaid/PlantUML), avec `viewBox`, `<title>`, `<desc>`, liens relatifs ; il vit dans
   `docs/schemas/` ou `docs/synthese/schemas/`. Vérifier : `python3 tools/verifier_schemas.py`.
   → [`docs/agent/illustrations.md`](docs/agent/illustrations.md)

## 3. Routage : lire le document de sa tâche, pas les autres

| si la tâche est… | lire |
|---|---|
| comprendre la **vision** (les flots, les cinq axes, ce qu'elle n'est pas) | [`docs/vision.md`](docs/vision.md) |
| la **roadmap** (les deux programmes, l'ordre, la file « jamais en attente ») | [`docs/roadmap.md`](docs/roadmap.md) |
| comprendre la mission, les priorités, la philosophie | [`docs/agent/mission.md`](docs/agent/mission.md) |
| écrire un résultat (fiche, JSON, commit, journal) | [`docs/agent/resultats.md`](docs/agent/resultats.md) |
| ranger un fichier, revue de documentation, synthèse | [`docs/agent/rangement.md`](docs/agent/rangement.md) |
| **charger le contexte** (budget, protocole, ce qu'on ne charge pas) | [`docs/agent/contexte.md`](docs/agent/contexte.md) |
| **dessiner un schéma**, convertir un diagramme, améliorer une illustration | [`docs/agent/illustrations.md`](docs/agent/illustrations.md) |
| lancer ou lire les portes | [`docs/agent/portes.md`](docs/agent/portes.md) |
| étudier Panini/Nipada, la généalogie | [`docs/agent/panini-nipada.md`](docs/agent/panini-nipada.md) |
| concevoir un test d'entrée/sortie, corriger | [`docs/agent/miroir.md`](docs/agent/miroir.md) |
| planifier une campagne, le matériel, carpe diem | [`docs/agent/ressources.md`](docs/agent/ressources.md) |
| **les jeux symboliques** (surface → RSN-jeu → pensée, 71 langues, maîtres) | [`docs/jeux-symboliques.md`](docs/jeux-symboliques.md) |
| **le protocole sémantique** (rejouer, convergence, sens → texte, raisonnement gelé) | [`docs/protocole-semantique.md`](docs/protocole-semantique.md) |
| **l'état courant** (synthèse + chantiers + questions) | [`docs/en-cours.md`](docs/en-cours.md) |
| le **vocabulaire** (couche vs étage, termes du dépôt) | [`docs/glossaire.md`](docs/glossaire.md) |
| **trouver un sujet** (un concept, un chantier, une phase) | [`docs/carte.md`](docs/carte.md) |
| la carte de la documentation (l'inventaire) | [`docs/README.md`](docs/README.md) |

> **Chargement facultatif.** Les documents de cette table, `docs/en-cours.md`, `docs/roadmap.md`, `reports/` et
> `journal/` ne se lisent **que pour la tâche en cours** : le fichier de tâche suffit le plus souvent. Ne pas les
> charger « pour être complet » — c'est du contexte qui coûte et qui périme.

> **Le contexte est un budget.** Par défaut : `AGENTS.md` + `docs/en-cours.md` + **un** document de
> tâche. Le protocole, les budgets et les cas « ne pas charger » sont dans
> [`docs/agent/contexte.md`](docs/agent/contexte.md) ; la vérification est
> `python3 tools/taille_documents.py`.

## 4. Le minimum avant de conclure

- l'état est à jour dans [`docs/en-cours.md`](docs/en-cours.md) (synthèse, chantiers, questions en attente) ;
- la **roadmap** est à jour : le chantier fini y est marqué, le suivant est désigné ;
- la fiche est dans `reports/`, le récit dans `journal/`, le commit porte le chiffre ;
- les portes sont vertes, **hors les deux rouges structurelles connues** ;
- la revue de documentation passe, et les liens résolvent.
- le budget de contexte est vérifié : `python3 tools/taille_documents.py`.
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

⏵ Exploring the Qtrinet repo and existing cerveau modules

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls tools/cerveau/ && echo \"---TESTS---\" && ls tools/cerveau/tests/", "description": "List cerveau tools and tests"}`

  ```
batterie.py
bus.py
episodique.py
gating.py
hub.py
__init__.py
lesion.py
m2_secours.py
memoire_travail.py
multilingue.py
neuromodulation.py
pipeline_memoire.py
pipeline.py
pipeline_semantique_m2.py
pipeline_semantique.py
predictif.py
__pycache__
restitution.py
sequences.py
sommeil.py
tests
voies.py
---TESTS---
__init__.py
__pycache__
test_bus.py
test_episodique.py
test_gating.py
test_lesion.py
test_m2_secours.py
test_memoire_travail.py
test_modules.py
test_multilingue.py
test_neuromodulation.py
test_pipeline_memoire.py
test_pipeline.py
test_pipeline_semantique_m2.py
test_pipeline_semantique.py
test_predictif.py
test_restitution.py
test_sommeil.py
test_voies.py
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git status --short && echo \"---\" && git log --oneline -5", "description": "Show git status and recent log"}`

  ```
M docs/README.md
---
1b0d4162 B19 — M2 SECOURS : TYPOS 71,2/76,7 VS M1 36,6 ; PHRASES M1 86,6 VS M2 0 ; NICHE, PAS SECOURS GÉNÉRAL
0df610ec PORTES — PASSE FINALE : 49 PORTES, 47 VERTES, 2 ROUGES STRUCTURELLES ; AUCUNE RÉGRESSION
c7e5cdbe ILLUSTRATIONS — MÉTADONNÉES ACCENTUÉES DES SCHÉMAS (TITLES ET DESCRIPTIONS)
15effc93 ILLUSTRATIONS — ANNOTATION ÉTAT DANS LE PANNEAU (ANATOMIE)
95108777 DOCWATCH — v0.3.0 : NAVIGATION SPA, URL PROPRES, 69 TESTS
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """M9 — lésions par module : privations déclarées et déficits mesurés.
3: 
4: Une lésion n'est pas une approximation : c'est une **privation déclarée** du
5: module, mesurée sur le même test que la version intacte, avec un **sham** (la
6: même mesure répétée sans privation) qui doit donner un déficit nul. Le déficit
7: est ``intacte - lésée`` ; un déficit négatif veut dire que la lésion *améliore*
8: — c'est un résultat, pas une erreur.
9: 
10: Modules couverts :
11: 
12: - **M1** : retirer le contexte de perception ;
13: - **M2** : couper la voie ventrale (action) ou dorsale (``de``). Par défaut le
14:   **vrai ``voies.py``** est exécuté (encodeur natif gelé, entraînement des têtes
15:   sur GPU ou CPU) ; si la base ou torch manque, le substitut bayésien à deux
16:   têtes est déclaré dans ``statut`` (repli documenté, jamais silencieux) ;
17: - **M3** : capacité du tampon (0, 1, 2, 4, 8, 12), dose-réponse ;
18: - **M4** : stockage vide, puis lésion du champ d'adressage (le champ est mis à
19:   ``None`` dans la requête) ;
20: - **M5** : retirer les transition
… [35909 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && wc -l tools/cerveau/lesion.py tools/cerveau/voies.py tools/cerveau/predictif.py tools/cerveau/gating.py tools/cerveau/sommeil.py tools/cerveau/tests/test_lesion.py", "description": "Count lines of relevant modules"}`

  ```
726 tools/cerveau/lesion.py
   737 tools/cerveau/voies.py
   575 tools/cerveau/predictif.py
   707 tools/cerveau/gating.py
   972 tools/cerveau/sommeil.py
   127 tools/cerveau/tests/test_lesion.py
  3844 total
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """M2 — deux voies : ventrale (quoi) et dorsale (où/comment).
3: 
4: Un même encodeur de surface, **gelé**, alimente deux familles de têtes :
5: 
6: - la voie **ventrale** lit l'**action** ;
7: - la voie **dorsale** lit un ou plusieurs champs de lieu : `de`, `vers`,
8:   `point`, `chemin_0`…
9: 
10: Chaque tête est indépendante : on peut en léser une (logits aléatoires) sans
11: toucher les autres. C'est la double dissociation minimale, étendue à plusieurs
12: champs dorsaux.
13: 
14: L'entraînement est **synthétique** (`items_synth`) ; l'évaluation porte sur les
15: surfaces **réelles** (`items`). Le module expose aussi les ablations :
16: 
17: - `pool="mean"` : moyenne seule (ablation du dernier état) ;
18: - `pool="last"` : dernier état seul ;
19: - `contexte=True` : ajout du RSN de contexte, encodé par le même encodeur gelé.
20: 
21: Les surfaces et le contexte sont normalisés (`normaliser`) puis lus en octets,
22: comme dans le prototype d'origine. L'API `entrainer`/`evaluer` reste compatible
23: avec `batterie.py` quand aucun champ dorsal supplémentaire n
… [33832 caractères tronqués]
  ```


  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py</path>
<type>file</type>
<content>
1: from __future__ import annotations
2: 
3: import json
4: import unittest
5: 
6: from cerveau.lesion import batterie_lesions
7: 
8: 
9: class TestLesion(unittest.TestCase):
10:     @classmethod
11:     def setUpClass(cls):
12:         cls.r = batterie_lesions(rapide=True)
13: 
14:     def test_structure(self):
15:         for m in ("M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"):
16:             self.assertIn(m, self.r["modules"])
17:             for k in ("lesion", "intacte", "lessee", "deficit", "n", "statut"):
18:                 self.assertIn(k, self.r["modules"][m])
19: 
20:     def test_sham(self):
21:         for m, v in self.r["controles"]["sham"].items():
22:             self.assertAlmostEqual(v, 0.0, places=12)
23: 
24:     def test_m1_contexte(self):
25:         d = self.r["modules"]["M1"]["deficit"]["exact"]
26:         self.assertGreater(d, 0.25)
27:         self.assertLess(d, 0.35)
28: 
29:     def test_m2_double_dissociation(self):
30:         m2 = self.r["modules"]["M2"]
31:         self.assertTrue(m2["deficit"]["double_dissociation"])
32:         self.assertG
… [4890 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """M5 — codage prédictif : prédire une cible **variable**, mesurer l'erreur.
3: 
4: Leçon mesurée (sprint 24 h, corpus `sequences.corpus`) : l'ancienne cible
5: `action` est **structurellement constante** par jeu — `action()` dans
6: `universaux.py` classe le coup par la *forme* du code (présence de `de`/`vers`,
7: de `chemin`, de `case`…), pas par sa sémantique. Résultat : échecs = toujours
8: `deplacer`, dames = toujours `prendre`, morpion = toujours `jouer_case` ; seul go
9: varie (`poser` 92 %, `passer` 8 %). Prédire `action` ne peut donc pas battre la
10: classe majoritaire : le 98,9 % publié était le taux de cette constante.
11: 
12: Le module change de cible et mesure honnêtement :
13: 
14: - `action` — la cible historique, gardée comme témoin ;
15: - `source` — la case de départ (`de` aux échecs, `chemin_0` aux dames) ;
16: - `cible`  — la case d'arrivée (`vers`, dernier `chemin`, `point`, `case`).
17: 
18: Trois ordres de Markov (0 = marginale par jeu, 1 = pas précédent, 2 = deux pas),
19: avec **repli hiérarchique Dirichlet** pour que la surprisal
… [26979 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,120p' tools/cerveau/gating.py && echo \"=== SOMMEIL HEAD ===\" && sed -n '1,120p' tools/cerveau/sommeil.py", "description": "Read gating and sommeil top sections"}`

  ```
#!/usr/bin/env python3
"""M6 — porte exécutive : une vraie tâche de conflit langue/tâche sur B7.

L'ancienne porte ne mesurait qu'une chose : `MULTI.detecte_langue(surface)`
comparée à la langue cible. Son « exactitude » de 72,9 % était donc le taux du
classifieur lexical, pas une mesure d'inhibition ; son « coût de commutation »
négatif venait de la composition des blocs (les cibles alternaient sur des
items très majoritairement français), pas d'un coût cognitif.

La tâche construite ici est un **go/no-go de confluence** sur les surfaces B7
fr/en (11 codes, deux langues) :

- `go`          : la sonde est le coup cible **dans la langue cible** → accepter ;
- `traduction`  : même coup, **autre langue** → inhiber le sens, refuser ;
- `langue`      : autre coup, **langue cible** → inhiber la langue, refuser ;
- `ni`          : autre coup, autre langue → refuser.

Les quatre conditions sont équilibrées (22 essais chacune, 88 au total) : un
politique « toujours non » obtient 75 %, et chaque canal seul (langue ou sens)
obtient 75 % aussi, avec 25 % de faux positifs. La seule politique qui dépasse
le taux de base est la **conjonction** (sens ET langue) : exactitude 94,3 %,
exactitude équi
… [8577 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"^def \\|^class \\|    def \" tools/cerveau/gating.py | head -80", "description": "List gating API"}`

  ```
60:class Essai:
73:    def attendu(self) -> bool:
78:class EssaiTache:
102:    def attendu(self) -> bool:
106:def _contexte_depart(jeu: str):
124:def _normalise(it) -> dict:
135:def _wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
146:def _mcc(tp: int, fp: int, fn: int, tn: int) -> float:
151:class Porte:
157:    def __init__(self) -> None:
164:    def langue(self, texte: str) -> str | None:
185:    def langue_multi(self, texte: str) -> str | None:
190:    def _vote_lexical(texte: str) -> str | None:
200:    def lire(self, texte: str, jeu: str, contexte=None) -> dict | None:
216:    def tache_conflit(self, items=None, cibles=("fr", "en")) -> list[Essai]:
245:        def sonde(cle: str, langue: str) -> dict:
278:    def tache_switch(self, items=None, cibles=("fr", "en")) -> list[EssaiTache]:
314:        def sonde(cle: str, langue: str) -> dict:
362:    def _decisions_switch(self, essais, politique: str = "tache") -> list[dict]:
403:    def _metriques_switch(decisions) -> dict:
440:        def exact(x):
480:    def executer_switch(self, items=None, cibles=("fr", "en")) -> dict:
522:    def _decisions(self, essais, politique: str = "conjonction",
547:    def _metriques
… [260 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"^def \\|^class \\|    def \" tools/cerveau/sommeil.py | head -80 && echo \"=== SEQUENCES ===\" && grep -n \"^def \\|^class \" tools/cerveau/sequences.py", "description": "List sommeil and sequences API"}`

  ```
68:def _code(e) -> dict:
73:def _signature(code: dict) -> tuple:
77:def _cle(code: dict, cle) -> tuple:
95:def _mode_champs(codes) -> dict:
103:def _mode_joint(codes) -> dict:
108:class Sommeil:
112:    def consolider(self, episodes, mode: str = "champs", cle="groupe") -> dict:
131:    def evaluer(self, episodes, prototypes, cle="groupe", fallback=None) -> dict:
159:    def par_champ(self, episodes, prototypes, cle="groupe", fallback=None) -> dict:
182:    def baselines(self, train, test) -> dict:
243:    def index_episodes(self, episodes) -> dict:
250:    def evaluer_hybride(self, episodes, prototypes, index, cle="groupe",
290:    def dedupliquer(episodes, par: str = "code") -> list:
307:    def experience(self, items_=None, graines=(1, 2, 3)) -> dict:
416:    def _groupes(episodes, cle):
423:    def _prototypes(cls, episodes, cle, mode: str = "champs"):
433:    def prototypes_multi(self, episodes, cles=CLES, mode: str = "champs") -> dict:
438:    def _predire(code, protos_par_cle, ladder=LADDER, min_support: int = 1):
463:    def evaluer_profond(self, episodes, protos_par_cle, ladder=LADDER,
516:    def _metriques(episodes, predire) -> dict:
533:    def _prototypes_paires(episode
… [1249 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"Predictif\\|Porte\\|Voies\\|voies\\|predictif\\|gating\" tools/cerveau/pipeline*.py tools/cerveau/batterie.py | head -60", "description": "Find pipelines chaining modules"}`

  ```
tools/cerveau/pipeline_semantique_m2.py:10:- **M2** (`voies.py`) relit la surface et rend les champs dorsaux `de`/`vers`
tools/cerveau/pipeline_semantique_m2.py:15:- **M5** (`predictif.py`) prédit la source/la cible du pas suivant avec le
tools/cerveau/pipeline_semantique_m2.py:18:- **M6** (`gating.py`) sélectionne la tâche ; la mesure est la porte de
tools/cerveau/pipeline_semantique_m2.py:67:from .gating import Porte
tools/cerveau/pipeline_semantique_m2.py:69:from .predictif import Predictif, permuter_contextes
tools/cerveau/pipeline_semantique_m2.py:71:from .voies import VALEURS, Voies, entrainer, evaluer_champs
tools/cerveau/pipeline_semantique_m2.py:141:def _entrees_voies(m, textes, contextes, seq: int = 64, seq_ctx: int = 192):
tools/cerveau/pipeline_semantique_m2.py:156:    `voies` est un modèle `Voies` déjà entraîné (ou None : la chaîne reste
tools/cerveau/pipeline_semantique_m2.py:163:    def __init__(self, voies: Voies | None = None, device: str = "cuda") -> None:
tools/cerveau/pipeline_semantique_m2.py:166:        self.voies = voies
tools/cerveau/pipeline_semantique_m2.py:168:        self.predictif = Predictif(cible="source", ordre=1, contexte=True,
tools/cerveau/pipelin
… [4072 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport torch, transformers, sys\nprint(\"torch\", torch.__version__, \"cuda\", torch.cuda.is_available())\nprint(\"transformers\", transformers.__version__)\nimport pathlib\nfor p in [\"/tmp/natif-600-512-8-align-s1\", \"/tmp/natif- … [136 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'torch'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls -a | head -40 && echo \"---\" && find . -maxdepth 2 -name \"*venv*\" -o -maxdepth 2 -name \"pyproject.toml\" -o -maxdepth 2 -name \"requirements*.txt\" | head", "description": "Look for venv and dependency files"}`

  ```
.
..
AGENTS.md
bench
colab
data
docs
drave-core
.git
.gitignore
.gitmodules
journal
models
__pycache__
Qtrinet-bootstrap.md
README.md
reports
REPRISE.md
run_8bit_perfection.py
run_clusters.py
run_cpu.py
run_encoding.py
run_harness.py
run_list_mode.py
run_precision.py
run_quantify.py
run_real_clusters.py
run_sparsity.py
run_value_encoding.py
sprints
src
tools
---
  ```

- **bash** `{"command": "ls /home/stephane/Data13TB/stephane 2>/dev/null | head; which python3; ls /tmp | head -30; find /home/stephane -maxdepth 3 -type d -name \"*venv*\" 2>/dev/null | head", "description": "Search for Python environment"}`

  ```
adobe_account_backup_uuid_d79a3839-50e8-4906-bb1a-e8c3954711b2.zip
agent-kit
altera_pro
archives
Arduino
Biblio_large
corpus
data
Desktop
Documents
/usr/bin/python3
a10-multilingue.json
a10-multilingue.md
a10-run.log
a10-sans-controle.json
a10-sans-controle.md
a11-m7-lfu.json
a11-m7-lfu.md
a1-m5-m6.json
a1-m5-m6.md
a1_m5_m6.py
a1_old_m6.py
a1_oracle.py
a2-m2-cpu.json
a2-m2-cpu.out
a2-m7-m8-m9.json
a2-m7-m8-m9.md
a2-m7-m8-m9-part1.md
a2-m7-m8-m9-part2.md
a2-m7-m8-m9-part3.md
a3_baseline_items.py
a3_baseline_split.py
a3_long.py
a3_m2_driver.py
a3-m2.json
a3-m2.md
a3-m2-partial.json
a3_probe2.py
a3_probe.py
a3_quick2.py
a3_quick.py
/home/stephane/transcription/.venv
/home/stephane/IA/venv-drave
[stderr]
ls: write error: Broken pipe
  ```

- **bash** `{"command": "/home/stephane/IA/venv-drave/bin/python3 - <<'EOF'\nimport torch, transformers, sys\nprint(sys.executable)\nprint(\"torch\", torch.__version__, \"cuda\", torch.cuda.is_available())\nprint(\"transformers\", transformers.__version__)\nimport pathlib\nprint(\"base\", pathlib.Path(\"/tmp/na … [92 caractères tronqués]`

  ```
/home/stephane/IA/venv-drave/bin/python3
torch 2.14.1+cu130 cuda True
transformers 5.20.1
base True
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"M9\" docs/en-cours.md docs/roadmap.md | head -30", "description": "Find M9 roadmap context"}`

  ```
docs/roadmap.md:349:### B12 — les modules cerveau-langage M1–M9
docs/roadmap.md:361:| B12.9 | **M9 lésion** | ✅ **table** | contexte **29,2 %** ; M2 ventrale **24,7 %** ; M2 dorsale **2,1 %** ; M7 **13,7 %** ; M3 **0** ; M4 **0** ; M5 **1,1 %** ; M6 **30 %** ; M8 **0** |
docs/roadmap.md:369:| B13.1 | **Chaîne sémantique M1→M5→M6→M8** | ✅ **intégration** | M1 **528/528** ; M5 contexte **18,7 % vs 12,6 %** (surprise 2,423 vs 3,112) ; M6 **94,3 %** / switch **94,95 %** ; M8 **57,95 %** exact sur épisodes stockés (borne haute) ; M9 M1 **70,8 %** |
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"lesion_complet\\|lésions croisées\\|double.*lésion\\|dose-réponse\" docs reports journal tools 2>/dev/null | head -30", "description": "Search existing cross-lesion mentions"}`

  ```
docs/synthese/index.md:132:| **B12 — les modules cerveau-langage M1–M9** : bus réel, **M1 528/528**, **M2 98,6 / 93,2** (double dissociation), **M8 96,48 %** hors stock ; **M5/M6/M7** négatifs ou faibles ; **M9** table de lésions | [les modules](../modules-cerveau-langage.md) · [la fiche](../../reports/rapport-cerveau-modules.md) |
docs/modules-cerveau-langage.md:28:| **M2 voies** | ventrale (`action`) / dorsale (`de`) | `action` global **86,4 %** ; `de` **93,6 %** (3 graines) = **126/126 vus + 10,7/20 inédits** ; lésions croisées sur les vus | ⚠️ **vu seulement** |
docs/modules-cerveau-langage.md:61:   lésions croisées sont nettes. Le point qui a débloqué : **le dernier état caché** (coordonnée finale),
docs/carte.md:58:| **B12** les modules cerveau-langage | **premier passage** — M1 528/528 ; M2 **98,6 / 93,2** (double dissociation) ; M8 **96,48 %** hors stock ; M5/M6/M7 négatifs ; M9 lésions | [les modules](modules-cerveau-langage.md) · [la fiche](../reports/rapport-cerveau-modules.md) |
reports/rapport-cerveau-modules.md:54:- **M2** : lésions croisées des têtes ; ventrale 98,6 → 9,6 %, dorsale 93,2 → 0,7 %.
reports/rapport-cerveau-modules.md:77:- **M2** est **valide** : la doub
… [3351 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "offset": 380, "limit": 180}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py</path>
<type>file</type>
<content>
380:     """Fait passer les surfaces d'une séquence par M1 et rend les codes."""
381:     codes = []
382:     n = ok = n_none = 0
383:     for seq in sequences:
384:         cs = []
385:         for p in seq.pas:
386:             ctx = (contexte_depuis_resume(p.contexte, p.jeu)
387:                    if avec_contexte else None)
388:             c = hub.percevoir(p.surface, p.jeu, ctx)
389:             if c is None:
390:                 c = code_vide(p.jeu)
391:                 n_none += 1
392:             cs.append(c)
393:             n += 1
394:             ok += int(c == p.code)
395:         codes.append(cs)
396:     return codes, {"n": n, "code_exact": ok / max(1, n), "n_none": n_none}
397: 
398: 
399: def _sequences_codes(sequences, codes) -> list[Sequence]:
400:     return [_sequence_avec_codes(s, c) for s, c in zip(sequences, codes)]
401: 
402: 
403: def _eval_m5(train, test, cible: str = "source", contexte: bool = True,
404:              ordre: int = 1, melange: float = 0.5) -> dict:
405:     m = Predictif(cible=cible, ordre=ordre, contexte=contexte,
406:          
… [7613 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/cerveau/sequences.py && echo === && sed -n '120,180p' tools/cerveau/batterie.py", "description": "Read sequences and batterie M5/M6"}`

  ```
#!/usr/bin/env python3
"""sequences.py — des parties jouées par les règles, pour M3/M5/M8.

Chaque pas porte : le code typé, la surface canonique, le contexte (résumé) et
la RSN. Les parties sont déterministes pour une graine donnée.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

from jeux.codecs import codec
from jeux.regles import dames as D
from jeux.regles import echecs as E
from jeux.regles import go as G
from jeux.regles import morpion as M
from jeux.rsn import RSN
from semantique.universaux import code_rsn, resume_contexte


@dataclass(frozen=True)
class Pas:
    jeu: str
    code: dict
    surface: str
    contexte: str
    rsn: RSN


@dataclass(frozen=True)
class Sequence:
    jeu: str
    pas: tuple[Pas, ...]


def _surface(jeu: str, rsn: RSN, contexte, fmt: str) -> str:
    try:
        return codec(jeu).rend(rsn, format=fmt, contexte=contexte)
    except Exception:
        return ""


def _echecs(rng: random.Random, n: int) -> Sequence:
    pos = E.Position.depart()
    pas = []
    for _ in range(n):
        coups = pos.coups_legaux()
        if not coups:
            break
        c = rng.choice(coups)
        ctx = E.rsn_depu
… [3134 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/cerveau/pipeline_semantique_m2.py && sed -n '640,800p' tools/cerveau/pipeline_semantique_m2.py", "description": "Read M2 pipeline docs and main measure"}`

  ```
#!/usr/bin/env python3
"""pipeline_semantique_m2.py — B13 + M2 : la chaîne M1 → M2 → M5 → M6.

Ce module est un **test d'intégration**, pas un nouveau module de perception.
Il branche les briques existantes sur un seul flux et mesure chaque étage sur
son propre banc :

- **M1** (`hub.py`) lit la surface et rend le code typé ; la mesure est le code
  exact sur les 528 surfaces réelles, avec et sans contexte ;
- **M2** (`voies.py`) relit la surface et rend les champs dorsaux `de`/`vers`
  (encodeur natif gelé, têtes linéaires) ; la mesure est l'exactitude de champ
  sur les 146 items réels qui portent `de`/`vers`, découpée en surfaces **vues**
  (forme normalisée présente dans l'entraînement synthétique) et **inédites**,
  avec les lésions ventrale/dorsale ;
- **M5** (`predictif.py`) prédit la source/la cible du pas suivant avec le
  plateau ; la mesure est l'exactitude et la surprisal sur un split 80/20 par
  partie, avec le plateau et sans lui ;
- **M6** (`gating.py`) sélectionne la tâche ; la mesure est la porte de
  confluence et la tâche de commutation ;
- **M9** (`lesion.py` pour les principes) applique les privations : M1 sans
  contexte, M2 sans voie ventrale/dorsale, M5 sans
… [9840 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Checking the existing test suite runtime and module APIs

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /usr/bin/time -f 'ELAPSED %e s' env PYTHONPATH=tools /home/stephane/IA/venv-drave/bin/python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -6", "description": "Run existing cerveau tests with timing", "timeoutMs": 900000}`

  ```
..........................................................................................................
----------------------------------------------------------------------
Ran 127 tests in 28.545s

OK
ELAPSED 35.28 s
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"def experience_m7\" -A 40 tools/cerveau/neuromodulation.py | head -60 && echo === && sed -n '151,245p' tools/cerveau/gating.py", "description": "Inspect M7 and M6 APIs"}`

  ```
383:def experience_m7(episodes: list[EpisodeM7] | None = None,
384-                  permutations: int = 30, capacite: int = 16,
385-                  graine: int = 0, synthetique: bool = True) -> dict:
386-    """Compare les politiques de rétention sur le même flux, appariées.
387-
388-    Le suffixe est le dernier 20 % du flux ; la mémoire est gelée à la fin du
389-    préfixe. Les deltas sont ``politique - fifo`` par permutation (même ordre,
390-    même capacité), avec le taux de gains et un IC 95 % normal.
391-    """
392-    ep = episodes if episodes is not None else preparer_flux()
393-    n = len(ep)
394-    prefixe = int(n * 0.8)
395-    configs = _configurations()
396-    resultats: dict[str, dict[str, list[float]]] = {
397-        c["nom"]: collections.defaultdict(list) for c in configs}
398-    oracle = collections.defaultdict(list)
399-    for k in range(permutations):
400-        ordre = list(range(n))
401-        random.Random(graine + k).shuffle(ordre)
402-        for c in configs:
403-            m = _tourner(ep, ordre, prefixe, c["politique"], capacite,
404-                         c["cle"], graine + k, c["sans"])
405-            for nom in _METRIQUES:
406-       
… [5967 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '522,706p' tools/cerveau/gating.py", "description": "Read M6 decision policies and metrics"}`

  ```
def _decisions(self, essais, politique: str = "conjonction",
                   langues_forcees: list[str | None] | None = None) -> list[dict]:
        decisions = []
        for i, essai in enumerate(essais):
            code = self.lire(essai.texte, essai.jeu, essai.contexte)
            langue = self.langue(essai.texte)
            forcee = langues_forcees[i] if langues_forcees is not None else None
            if politique == "conjonction":
                accepte = code == essai.cible_code and langue == essai.cible_langue
            elif politique == "langue":
                accepte = langue == essai.cible_langue
            elif politique == "sens":
                accepte = code == essai.cible_code
            elif politique == "perseveration":
                reference = forcee if forcee is not None else essai.cible_langue
                accepte = code == essai.cible_code and langue == reference
            elif politique == "tout_non":
                accepte = False
            else:
                raise ValueError(f"politique inconnue : {politique!r}")
            decisions.append({"accepte": bool(accepte), "code": code,
                              "langue": langue
… [8403 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"class MemoireTravail\" -A 60 tools/cerveau/memoire_travail.py | head -80 && echo === && grep -n \"def span\\|def nback_scores\\|def charger\\|def nback\" tools/cerveau/memoire_travail.py", "description": "Inspect MemoireTravail API"}`

  ```
15:class MemoireTravail:
16-    nom = "M3-memoire-travail"
17-
18-    def __init__(self, capacite: int = 12) -> None:
19-        self.capacite = capacite
20-        self.tampon: deque = deque(maxlen=capacite)
21-
22-    def charger(self, codes) -> None:
23-        self.tampon.clear()
24-        for c in codes[-self.capacite:]:
25-            self.tampon.append(dict(c))
26-
27-    def pousser(self, code: dict) -> None:
28-        """Présente un code à la suite : le plus ancien sort si le tampon est plein.
29-
30-        C'est la présentation séquentielle (une liste poussée), par opposition à
31-        `charger` qui remplace tout le tampon d'un coup.
32-        """
33-        self.tampon.append(dict(code))
34-
35-    def lire(self, i: int):
36-        return self.tampon[i] if 0 <= i < len(self.tampon) else None
37-
38-    def distance(self, a: dict, b: dict) -> int:
39-        """Distance de Hamming sur les champs typés (0 = même code)."""
40-        return sum(1 for nom, _ in CHAMPS if a.get(nom) != b.get(nom))
41-
42-    def retrouver(self, code: dict):
43-        """Reconnaissance par contenu : le code du tampon le plus proche.
44-
45-        Le tampon d'origine ne lit que par po
… [1509 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"def _configurations\" -A 40 tools/cerveau/neuromodulation.py && grep -n \"def preparer_flux\" -A 20 tools/cerveau/neuromodulation.py | head -30", "description": "Inspect M7 configurations"}`

  ```
353:def _configurations() -> list[dict]:
354-    return [
355-        {"nom": "fifo", "politique": "fifo", "cle": "surface", "sans": ()},
356-        {"nom": "lru", "politique": "lru", "cle": "surface", "sans": ()},
357-        {"nom": "lfu", "politique": "lfu", "cle": "surface", "sans": ()},
358-        {"nom": "gel", "politique": "gel", "cle": "surface", "sans": ()},
359-        {"nom": "nouveaute", "politique": "nouveaute", "cle": "surface", "sans": ()},
360-        {"nom": "incertitude", "politique": "incertitude", "cle": "surface", "sans": ()},
361-        {"nom": "recompense", "politique": "recompense", "cle": "surface", "sans": ()},
362-        {"nom": "combine", "politique": "combine", "cle": "surface", "sans": ()},
363-        {"nom": "combine_sans_nouveaute", "politique": "combine", "cle": "surface",
364-         "sans": ("nouveaute",)},
365-        {"nom": "combine_sans_incertitude", "politique": "combine", "cle": "surface",
366-         "sans": ("incertitude",)},
367-        {"nom": "combine_sans_recompense", "politique": "combine", "cle": "surface",
368-         "sans": ("recompense",)},
369-        {"nom": "combine_sans_tout", "politique": "combine", "cle": "surface",
… [2291 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '962,980p' tools/cerveau/sommeil.py && grep -n \"def experience_contexte\" -A 40 tools/cerveau/sommeil.py | head -50", "description": "Inspect M8 public experience functions"}`

  ```
def experience_m8(items_=None) -> dict:
    return Sommeil().experience(items_)


def experience_contexte(items_=None, graines=(1, 2, 3)) -> dict:
    return Sommeil().experience_contexte(items_, graines)


if __name__ == "__main__":
    import json
    print(json.dumps(experience_m8()["verdict"], ensure_ascii=False, indent=1))
675:    def experience_contexte(self, items_=None, graines=(1, 2, 3)) -> dict:
676-        """M8 conditionné : jeu, action, type de coup, et code tenu à l'écart.
677-
678-        Trois protocoles, tous les prototypes construits **sans** le code testé :
679-
680-        1. ``leave-one-code-out`` : 29 plis, un code exclu par pli, évalué une
681-           fois (moyenne par code, non pondérée par la fréquence des surfaces) ;
682-        2. ``codes_tenus`` : 3 graines, 20 % des codes exclus par jeu, évaluation
683-           pondérée par les items et par code ;
684-        3. ``paires_tenues`` : le split historique ``decouper`` par paire, avec
685-           le contrôle de fuite ``codes_test_vus_dans_train``.
686-
687-        L'exact y est nul **par construction** (un prototype ne sort qu'un code
688-        vu, le code exclu n'est pas dans le train) : la mesure
… [1813 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Benchmarking the real M2 lesion path before designing the new battery

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && env PYTHONPATH=tools CUDA_VISIBLE_DEVICES=0 /home/stephane/IA/venv-drave/bin/python3 - <<'EOF'\nimport time, json\nt0=time.time()\nfrom cerveau.lesion import _m2_voies\nr=_m2_voies(pas=300, graines=(1,))\nprint(\"duree\", round(time.time()-t0,2), \"de … [276 caractères tronqués]`

  ```
Error: tool call aborted
  ```

