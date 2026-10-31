# Session DSH — relecture

- identifiant : `f2f82297-793b-4538-952f-cb8da809229c`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 12:03:58
- agent : standard


## Tour 1

### 👤 Utilisateur

Dépôt /home/stephane/GitHub/Qtrinet, sprint autonome 24 h. Sous-agent A10 : mesurer M1 (codec typé) sur le corpus **multilingue** déjà présent, sans modifier les modules existants.

État :
- `tools/cerveau/hub.py` M1 : 528/528 sur les surfaces réelles avec contexte, 70,8 % sans contexte, canonique 100 %, invariance 100 %.
- Corpus : `jeux/corpus.py`, `jeux/corpus_multilingue.py`, `semantique/typed_corpus.py` ; B5/B7 contiennent les surfaces multilingues (71 langues dans les campagnes précédentes).
- Tests : `PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools` → 86 OK (8 skip sans torch).

Objectif :
1. Créer `tools/cerveau/multilingue.py` : charge les corpus multilingues, mesure par langue et par jeu (n, exact avec contexte, exact sans contexte, canonique, invariance), et une **baseline surface** (même code pour toutes les surfaces d'une paire) + contrôle **surface permutée**.
2. Mesurer si le code M1 est **le même** pour les variantes de langue d'une même paire (invariance inter-langues) ; produire `/tmp/a10-multilingue.json` et `.md`.
3. Si les langues sont absentes du corpus réel, le dire et mesurer ce qui existe ; ne pas inventer.

Contraintes :
- Crée uniquement `tools/cerveau/multilingue.py` et `tools/cerveau/tests/test_multilingue.py` ; ne modifie pas les modules existants, docs, reports, journal, `batterie.py`, git.
- Pas de `git add/commit/checkout`.
- CPU uniquement. Sois autonome, mesure, autocritique. Réponds avec un résumé et les chemins.
Your parent agent id is "f0969e87-af0c-43b1-93cf-f278d9c90846". Before you finish, send your result to that agent with send_message({ agent_id: "f0969e87-af0c-43b1-93cf-f278d9c90846", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

# Directives de l'agent — Drave

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs
> unifiés (**49 portes, 8 chapitres, 175 fichiers / 242 JSON, 53 documents**), chemins archivés
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

## 3. Routage : lire le document de sa tâche, pas les autres

| si la tâche est… | lire |
|---|---|
| comprendre la **vision** (les flots, les cinq axes, ce qu'elle n'est pas) | [`docs/vision.md`](docs/vision.md) |
| la **roadmap** (les deux programmes, l'ordre, la file « jamais en attente ») | [`docs/roadmap.md`](docs/roadmap.md) |
| comprendre la mission, les priorités, la philosophie | [`docs/agent/mission.md`](docs/agent/mission.md) |
| écrire un résultat (fiche, JSON, commit, journal) | [`docs/agent/resultats.md`](docs/agent/resultats.md) |
| ranger un fichier, revue de documentation, synthèse | [`docs/agent/rangement.md`](docs/agent/rangement.md) |
| **charger le contexte** (budget, protocole, ce qu'on ne charge pas) | [`docs/agent/contexte.md`](docs/agent/contexte.md) |
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

⏵ Exploring the repository to locate M1, multilingual corpora, and existing tests

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls && echo '---' && ls tools/cerveau/ && echo '---' && ls jeux/ 2>/dev/null | head -50 && echo '---' && ls semantique/ 2>/dev/null | head -50", "description": "List repo structure and key directories"}`

  ```
AGENTS.md
bench
colab
data
docs
drave-core
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
batterie.py
bus.py
episodique.py
gating.py
hub.py
__init__.py
lesion.py
memoire_travail.py
neuromodulation.py
pipeline.py
pipeline_semantique.py
predictif.py
__pycache__
sequences.py
sommeil.py
tests
voies.py
---
---
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git status --short | head -30 && echo '---' && git log --oneline -5", "description": "Show git status and recent commits"}`

  ```
M docs/README.md
---
088922e0 B12 — M2 A5 FINAL : AUCUN GAIN UNIFORME ; AUG-POS LIT LES PROMOTIONS 3/3 ; ROQUE 0/3
08a9cf18 B13 — CHAÎNE M1→M5→M6→M8 : 528/528, M5 CONTEXTE 18,7 % VS 12,6 %, M6 94,3 %, M8 57,95 (BORNE HAUTE)
ba3552b9 DOCS — MDSERVE : 64 TESTS
47fc2151 DOCS — CONTEXTE IA : BUDGETS ET MANIFESTE, CHAPITRE 5 SCINDÉ, INDEX RÉDUIT (175/242/53, T0 3 561 MOTS)
8541dfe7 DOCS — MDSERVE : 60 TESTS (ET NON 59)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && find . -name 'corpus*.py' -o -name 'typed_corpus.py' | head -20 && echo '---' && ls src/ | head -80", "description": "Find corpus modules and list src"}`

  ```
./tools/corpus_neuf.py
./tools/corpus_wikipedia.py
./tools/corpus_eurlex.py
./tools/corpus_presse.py
./tools/corpus_onu.py
./tools/corpus_jw.py
./tools/corpus_pidgin.py
./tools/corpus_pidgin_bbc.py
./tools/corpus_pidgin_bible.py
./tools/corpus_pidgin_wiki_local.py
./tools/corpus_pidgin_asp_raw.py
./tools/corpus_raisonnement.py
./tools/corpus_raisonnement_paires.py
./tools/corpus_wikimatrix.py
./tools/corpus_opensubtitles.py
./tools/corpus_jrc.py
./tools/corpus_diabla.py
./tools/jeux/corpus.py
./tools/jeux/corpus_multilingue.py
./tools/semantique/corpus.py
---
bpe_np.py
encoding.py
gguf_min.py
__pycache__
roofline.py
sparsity.py
ternary.py
tiny_model.py
transformer_np.py
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"corpus_multilingue\\|typed_corpus\" --include='*.py' -l | head -20", "description": "Find references to multilingual corpus modules"}`

  ```
tools/jeux/corpus_multilingue.py
tools/jeux/mesure_langues.py
tools/semantique/tests/test_typed_corpus.py
tools/semantique/typed_corpus.py
tools/semantique/entrainer_type.py
tools/semantique/synth_corpus.py
tools/semantique/hybride.py
tools/semantique/restitution.py
tools/cerveau/tests/test_gating.py
tools/cerveau/tests/test_voies.py
tools/cerveau/batterie.py
tools/cerveau/neuromodulation.py
tools/cerveau/voies.py
tools/cerveau/gating.py
tools/cerveau/lesion.py
tools/cerveau/sommeil.py
tools/cerveau/pipeline_semantique.py
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && wc -l tools/cerveau/hub.py tools/cerveau/batterie.py tools/jeux/corpus.py tools/jeux/corpus_multilingue.py tools/semantique/typed_corpus.py tools/jeux/mesure_langues.py && echo '---' && ls tools/cerveau/tests/", "description": "Show sizes of key modul … [14 caractères tronqués]`

  ```
47 tools/cerveau/hub.py
  225 tools/cerveau/batterie.py
  386 tools/jeux/corpus.py
  102 tools/jeux/corpus_multilingue.py
   91 tools/semantique/typed_corpus.py
  222 tools/jeux/mesure_langues.py
 1073 total
---
__init__.py
__pycache__
test_bus.py
test_episodique.py
test_gating.py
test_lesion.py
test_memoire_travail.py
test_modules.py
test_neuromodulation.py
test_pipeline.py
test_pipeline_semantique.py
test_predictif.py
test_sommeil.py
test_voies.py
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"M1\\|def \\|class \" tools/cerveau/hub.py | head -120", "description": "Outline hub.py"}`

  ```
2:"""M1 — hub sémantique typé : surface → code RSN, et retour canonique.
19:class Hub:
20:    nom = "M1-hub"
22:    def __init__(self, bus: Bus | None = None) -> None:
26:    def percevoir(self, texte: str, jeu: str, contexte=None):
41:    def rendre(self, code: dict, contexte=None):
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/hub.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/jeux/corpus_multilingue.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/hub.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """M1 — hub sémantique typé : surface → code RSN, et retour canonique.
3: 
4: Le hub est la **zone de convergence** du système : il ne produit pas un vecteur
5: libre, il produit le code fixe de `universaux.py` (15 champs, 502 classes) en
6: s'appuyant sur le codec classique. Chaque perception et chaque restitution est
7: publiée sur le bus.
8: """
9: from __future__ import annotations
10: 
11: from jeux.codecs import codec
12: from semantique.universaux import code_rsn, rsn_depuis_code
13: from .bus import Bus
14: 
15: FORMATS = {"morpion": "cellule", "echecs": "san", "dames": "numerique",
16:            "go": "gtp", "cartes": "carte"}
17: 
18: 
19: class Hub:
20:     nom = "M1-hub"
21: 
22:     def __init__(self, bus: Bus | None = None) -> None:
23:         self.bus = bus or Bus()
24:         self.dernier = None
25: 
26:     def percevoir(self, texte: str, jeu: str, contexte=None):
27:         try:
28:             lec = codec(jeu).lit(texte, niveau=4, contexte=contexte)
29:         except Exception as e:
30:             self.bus.publier("echec", {"texte": texte
… [889 caractères tronqués]
  ```


  ```
<path>/home/stephane/GitHub/Qtrinet/tools/jeux/corpus_multilingue.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """corpus_multilingue.py — les mêmes connaissances, dans 71 langues.
3: 
4: Le corpus multilingue est **dérivé** du lexique Wikidata : pour chaque langue,
5: on prend les libellés disponibles et on construit des surfaces **à mots-clés**
6: (pièce + cases, rang + enseigne, nom du jeu + coordonnée). Ce n'est pas de la
7: grammaire : c'est la couche lexicale, celle qui doit déjà porter le sens avant
8: qu'une phrase soit possible.
9: 
10: Ce qui est **fort** : les pièces des échecs et les cartes, parce que le libellé
11: y porte tout le sens (un cavalier n'est pas un roi). Ce qui est **mixte** : les
12: noms de jeux + une coordonnée (go, dames, morpion), parce que la coordonnée est
13: déjà neutre ; cela vérifie qu'un mot étranger ne bloque pas la lecture.
14: 
15: Chaque item porte une **paire** (le même sens dans toutes les langues) : c'est
16: la mesure d'invariance inter-langues.
17: """
18: from __future__ import annotations
19: 
20: from .corpus import Corpus
21: from .lexique_multilingue import MULTI
22: from .regles import cartes as C
23: from .r
… [4111 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/jeux/corpus.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/batterie.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/jeux/corpus.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """corpus.py — le corpus de surfaces, avec leur sens attendu.
3: 
4: Un item est un triplet (surface, contexte, RSN attendue). Le corpus est
5: **construit par le code**, pas stocké dans `data/` : il est reproductible, et on
6: peut le régénérer après chaque correction. Il couvre les cinq jeux, deux
7: langues, plusieurs notations, et des paires d'expressions **équivalentes** (pour
8: l'invariance) et **non équivalentes** (pour le contrôle de collision).
9: 
10: Règle : l'attendu est calculé par les **règles**, jamais recopié à la main. Si
11: le codec et les règles se contredisent, le corpus le dit — c'est un test, pas
12: une illustration.
13: """
14: from __future__ import annotations
15: 
16: from dataclasses import dataclass, field
17: 
18: from .regles import cartes as C
19: from .regles import dames as D
20: from .regles import echecs as E
21: from .regles import go as G
22: from .regles import morpion as M
23: from .rsn import RSN
24: 
25: 
26: @dataclass(frozen=True)
27: class Item:
28:     jeu: str
29:     texte: str
30:     nature: str
31:     attendu:
… [20645 caractères tronqués]
  ```


  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/batterie.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """batterie.py — la batterie M1–M9, exécutée et publiée.
3: 
4: Chaque module renvoie ses mesures ; M9 relit les autres et chiffre ce qu'une
5: lésion enlève. Aucun score n'est interprété ici : le rapport le fait.
6: """
7: from __future__ import annotations
8: 
9: import collections
10: import json
11: import pathlib
12: import sys
13: import time
14: 
15: sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
16: from jeux.corpus import construire_corpus  # noqa: E402
17: from jeux.corpus_multilingue import construire_corpus_multilingue  # noqa: E402
18: from jeux.codecs import codec  # noqa: E402
19: from semantique.typed_corpus import items  # noqa: E402
20: from semantique.universaux import code_rsn  # noqa: E402
21: from cerveau.bus import Bus  # noqa: E402
22: from cerveau.episodique import Episodique  # noqa: E402
23: from cerveau.gating import Porte  # noqa: E402
24: from cerveau.hub import Hub  # noqa: E402
25: from cerveau.memoire_travail import MemoireTravail  # noqa: E402
26: from cerveau.neuromodulation import MemoireLimitee, Neur
… [8087 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/semantique/typed_corpus.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/jeux/mesure_langues.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/semantique/typed_corpus.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """typed_corpus.py — les surfaces de jeux avec leur code typé fixe.
3: 
4: La source est le corpus B5/B6 (112 items, formats canoniques) et le corpus
5: multilingue B7 (449 surfaces, 66 langues). On ne garde que les **coups** : ce
6: sont les items dont le code typé est complet (source, cible, matériel).
7: Le découpage se fait **par paire** : les surfaces d'un même sens restent du même
8: côté ; aucune langue d'une paire de validation n'est vue à l'entraînement.
9: """
10: from __future__ import annotations
11: 
12: import random
13: from dataclasses import dataclass
14: 
15: from jeux.corpus import construire_corpus
16: from jeux.corpus_multilingue import construire_corpus_multilingue
17: from semantique.universaux import code_item, resume_contexte
18: 
19: 
20: @dataclass(frozen=True)
21: class ItemType:
22:     texte: str
23:     code: dict
24:     jeu: str
25:     nature: str
26:     langue: str
27:     paire: str
28:     format: str
29:     contexte: str = ""
30: 
31: 
32: def items() -> list[ItemType]:
33:     out = []
34:     vus = set()
35:  
… [2435 caractères tronqués]
  ```


  ```
<path>/home/stephane/GitHub/Qtrinet/tools/jeux/mesure_langues.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """mesure_langues.py — 71 langues, le même sens.
3: 
4: Trois mesures, trois contrôles :
5: 1. **couverture** : combien de concepts du lexique ont un libellé dans combien
6:    de langues (Wikidata, 35 concepts, 71 langues) ;
7: 2. **corpus** : les surfaces multilingues du corpus (pièces, cartes, noms de
8:    jeux + coordonnées), lues au niveau 4, comparées à la RSN attendue ;
9: 3. **invariance** : les variantes d'une même paire (le même coup dans toutes
10:    les langues) doivent donner la même empreinte.
11: 
12: Contrôles : **permutation** des libellés entre concepts (le sens doit
13: s'effondrer), **notation** (les 112 items de notation sont lus dans chacune des
14: 71 langues : la notation ne dépend pas de la langue), et **détection** des noms
15: de jeux.
16: """
17: from __future__ import annotations
18: 
19: import time
20: from collections import Counter, defaultdict
21: 
22: from .codecs import base as B
23: from .codecs import cartes as CC
24: from .codecs import dames as CD
25: from .codecs import echecs as CE
26: from .codecs import go as 
… [7986 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"B5\\|B7\" --include='*.py' tools/ | head -40", "description": "Search B5/B7 references in Python code"}`

  ```
tools/jeux/mesure.py:337:        ("p5", "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8",
tools/jeux/tests/test_regles.py:34:            ("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8",
tools/semantique/universaux.py:12:La base couvre les **coups** des cinq jeux (B5/B6) et les surfaces multilingues
tools/semantique/universaux.py:13:(B7). Les champs sont des **universaux du jeu** (agent/action/source/cible/
tools/semantique/typed_corpus.py:4:La source est le corpus B5/B6 (112 items, formats canoniques) et le corpus
tools/semantique/typed_corpus.py:5:multilingue B7 (449 surfaces, 66 langues). On ne garde que les **coups** : ce
tools/semantique/synth_corpus.py:6:entraîne le natif à lire ces surfaces. Les surfaces **réelles** B5/B7 ne sont
tools/semantique/hybride.py:4:Le codec classique lit les surfaces de jeux à 100 % sur B5/B7. On mesure ici
tools/semantique/restitution.py:26:    for nom, corpus in (("B5", construire_corpus()), ("B7", construire_corpus_multilingue())):
tools/cerveau/gating.py:2:"""M6 — porte exécutive : une vraie tâche de conflit langue/tâche sur B7.
tools/cerveau/gating.py:10:La tâche construite ici est un **go/no-go de confluence** sur les 
… [969 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls tools/jeux/ && echo '---' && wc -l tools/jeux/lexique_multilingue.py && head -80 tools/jeux/lexique_multilingue.py", "description": "List jeux modules and inspect multilingual lexicon"}`

  ```
codecs
construire_lexique_multilingue.py
corpus_multilingue.py
corpus.py
grammaire.py
__init__.py
lexique_multilingue.json
lexique_multilingue.py
lexique.py
maitres.py
mesure_langues.py
mesure_maitres.py
mesure.py
pensee.py
__pycache__
regles
rsn.py
tests
---
253 tools/jeux/lexique_multilingue.py
#!/usr/bin/env python3
"""lexique_multilingue.py — les libellés des jeux, en 53 langues.

Le fichier `lexique_multilingue.json` (construit par
`construire_lexique_multilingue.py`) porte les libellés **normalisés** de
35 concepts : noms des cinq jeux, pièces des échecs, rangs et enseignes des
cartes, couleurs, notions de maîtres. Ce module les charge et les rend
cherchables par **domaine** :

    MULTI.cherche("echecs.piece", "король g1 f3")
    MULTI.cherche("cartes.couleur", "ملك القلوب")

La recherche est **multi-formes** : n-grammes de 1 à 4 unités pour les langues à
espaces, et sous-chaîne pour les écritures qui n'en mettent pas (CJK, thaï). Le
libellé est comparé sous sa forme normalisée (`normalise_forme`), la même que
celle du constructeur : NFKC, casse pliée, diacritiques optionnels retirés,
parenthèses de désambiguïsation ôtées.

Ce module ne **devine** pas la langue d'un texte : 
… [1865 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,120p' tools/jeux/codecs/__init__.py 2>/dev/null || ls tools/jeux/codecs*", "description": "Inspect codecs package interface"}`

  ```
"""Les codecs de jeux : un fichier par jeu, un seul contrat (`base.Codec`)."""
from .base import Arbre, Codec, Lecture, codec, detecte_jeu, lit, rend, tous_les_codecs  # noqa: F401
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"def lit\\|def codec\\|class Lecture\\|class Codec\\|langue\" tools/jeux/codecs/base.py | head -80 && echo '---' && sed -n '1,100p' tools/jeux/codecs/base.py", "description": "Inspect codec base contract"}`

  ```
25:from ..lexique import langue_probable
66:class Lecture:
83:    langue: str = "inconnue"
94:            "format": self.format, "langue": self.langue,
104:class Codec:
111:    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
112:            langue: str | None = None) -> Lecture:
115:    def rend(self, rsn: RSN, format: str = "canonique", langue: str = "fr",
138:    def lecture(self, texte: str, niveau: int, langue: str | None = None,
140:        lang = langue or langue_probable(texte)[0]
142:            ml = MULTI.detecte_langue(texte)
146:                       format=format, langue=lang)
150:        return Annotation(langue=lecture.langue, format=lecture.format,
165:        rsn = rsn.avec_annotation(langue=lecture.langue, format=lecture.format,
180:def codec(jeu: str) -> Codec:
193:def lit(texte: str, jeu: str | None = None, niveau: int = 4,
194:        contexte: RSN | None = None, langue: str | None = None) -> Lecture:
202:        return codec(jeu).lit(texte, niveau=niveau, contexte=contexte, langue=langue)
209:            l = c.lit(texte, niveau=niveau, contexte=contexte, langue=langue)
216:    return codec(meilleur).lit(texte, niveau=niveau, contexte=co
… [3529 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '80,260p' tools/jeux/lexique_multilingue.py", "description": "Read rest of multilingual lexicon module"}`

  ```
def depuis_donnees(cls, donnees: dict) -> "Multilingue":
        obj = cls.__new__(cls)
        obj.chemin = None
        obj.donnees = donnees
        obj._construire()
        return obj

    def _construire(self) -> None:
        self.langues: list[str] = list(self.donnees["langues"])
        self.concepts: dict = self.donnees["concepts"]
        # domaine → {forme: [(concept, valeur, langue)]}
        self.index: dict[str, dict[str, list[tuple[str, str, str]]]] = defaultdict(dict)
        for concept, c in self.concepts.items():
            domaine, valeur = _domaine_valeur(concept)
            for langue, formes in c.get("labels", {}).items():
                for f in formes:
                    f = normalise_forme(f)
                    if not f:
                        continue
                    variantes = {f}
                    # l'article arabe (ال) et l'article hébreu (ה) sont des
                    # préfixes : le libellé Wikidata les porte souvent, la
                    # surface peut les omettre (ou l'inverse).
                    if langue == "ar":
                        variantes.add(f[2:] if f.startswith("ال") else "ال" + f)
                    if langue == "
… [6955 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom jeux.lexique_multilingue import MULTI\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom jeux.corpus import construire_corpus\nfrom semantique.typed_corpus import items\nfrom collections i … [625 caractères tronqués]`

  ```
MULTI.langues 71
concepts 35
corpus ML items 449
langues corpus ML 66
par jeu Counter({'cartes': 153, 'echecs': 122, 'go': 76, 'dames': 56, 'morpion': 42})
par paire 11
items typed 528
langues typed 67
B5 items 112
premieres langues ['ar', 'bn', 'ca', 'cs', 'da', 'de', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'gl', 'he', 'hi', 'hr', 'hu']
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat tools/cerveau/tests/__init__.py && echo '---' && sed -n '1,120p' tools/cerveau/tests/test_modules.py", "description": "Inspect test style and init"}`

  ```
---
from __future__ import annotations
import unittest
from cerveau.memoire_travail import MemoireTravail
from cerveau.episodique import Episodique
from cerveau.sequences import partie


class TestModules(unittest.TestCase):
    def test_span(self):
        s = partie("echecs", 0, 5)
        m = MemoireTravail(5)
        self.assertGreaterEqual(m.span([s])["span"], 1)

    def test_episodique(self):
        e = Episodique()
        a = {"jeu": "echecs", "action": "deplacer", "de": 62, "vers": 45}
        b = {"jeu": "echecs", "action": "deplacer", "de": 52, "vers": 36}
        e.stocker("Nf3", a); e.stocker("e4", b)
        self.assertTrue(e.rappel(a)["exact"])
        self.assertTrue(e.separation(a, b)["distincts"])


if __name__ == "__main__":
    unittest.main()
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools python3 -c \"\nfrom cerveau.batterie import m1\nimport json\nprint(json.dumps(m1(), ensure_ascii=False, indent=1))\n\"", "description": "Run existing M1 battery measurement"}`

  ```
{
 "items": 528,
 "exact": 1.0,
 "sans_contexte": 0.7083333333333334,
 "canonique": 1.0,
 "invariance": 1.0,
 "evenements": 1584
}
[stderr]

real	0m1,720s
user	0m1,700s
sys	0m0,020s
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,120p' tools/semantique/universaux.py && echo '...' && grep -n \"def code_rsn\\|def rsn_depuis_code\\|CHAMPS\\|def code_item\\|def resume_contexte\" tools/semantique/universaux.py", "description": "Inspect typed universals module"}`

  ```
#!/usr/bin/env python3
"""universaux.py — la base fixe des universaux sémantiques des jeux.

Le protocole libre apprenait un vecteur `z` : il retrouvait l'article, mais ne
disait pas **ce qu'il contenait**. Ici, la sortie n'est plus un vecteur libre :
c'est un **code typé**, un tuple de champs fixes, chacun avec un vocabulaire fixe.
Deux conséquences, et c'est le but :

- l'embedding est **typé** : `jeu=carte`, `action=prendre`, `de=12`, `vers=28` ;
- il est **déterministe** : le même code se lit par `argmax`, sans seuil appris.

La base couvre les **coups** des cinq jeux (B5/B6) et les surfaces multilingues
(B7). Les champs sont des **universaux du jeu** (agent/action/source/cible/
matériel), pas des tokens : un `de` est une case, pas un mot.
"""
from __future__ import annotations

import hashlib
import json

JEUX = ("morpion", "echecs", "dames", "go", "cartes")
ACTIONS = ("deplacer", "prendre", "promouvoir", "jouer_case", "jouer_carte", "poser", "passer", "autre")
PROMOTIONS = (None, "q", "r", "b", "n")
ROQUES = (None, "K", "Q")
TAILLES = (None, 5, 9, 13, 19)
SYMBOLES = (None, "X", "O")
PASSES = (None, True, False)

# L'ordre est le contrat : il ne change jamais sans une nouvelle
… [3251 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"baseline surface\\|baseline_surface\\|surface permutée\\|surface permutee\\|permut\" reports/ journal/ docs/ --include='*.md' --include='*.json' | head -40", "description": "Search prior baseline and permutation definitions"}`

  ```
reports/rapport-hc-permutation.md:35:## 2. La structure : 4 connexions dominantes, et c'est une permutation
reports/rapport-hc-permutation.md:43:| les 4 dominantes forment-elles une **permutation** ? | **43 / 43 couches** |
reports/rapport-hc-permutation.md:48:3,9-4,0), mais **neuf couches permutent** :
reports/rapport-hc-permutation.md:50:| couche | permutation (destination ← source) | masse diagonale |
reports/rapport-hc-permutation.md:70:| modèle | couches | permutations (pos 0 / 1 / 2 / 3) | identités | diagonale moyenne |
reports/rapport-hc-permutation.md:76:permutation. V4.1 est encore plus proche de l'identité que V4-Flash (2 couches
reports/rapport-hc-permutation.md:89:  négligeables, 99 % de la masse), et ils forment une **permutation** ; la
reports/rapport-hc-permutation.md:92:  **permutation apprise** (4 coefficients) au lieu de 16, ce qui simplifie le
reports/rapport-hc-permutation.md:95:  `comb` par sa permutation dominante (0/1) donne une erreur L2 relative de
reports/rapport-hc-permutation.md:100:  `comb` à sa permutation dominante ; la perte de perplexité se lit alors contre
reports/rapport-hc-permutation.md:104:  couches-position, toutes en permutation) ; la varian
… [5229 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls reports/ | tail -30 && echo '---' && grep -rln \"M1\" reports/ | head -20", "description": "List reports and M1 references"}`

  ```
traduction-legal.json
traduction-litteraire-3b.json
traduction-litteraire-7b.json
traduction-onu-3b.json
traduction-onu6-3b.json
traduction-onu6-7b.json
traduction-onu-7b.json
traduction-pidgin-14b.json
traduction-pidgin-7b.json
traduction-presse-3b.json
traduction-presse-7b.json
traduction-udhr-propre-3b-fraeng.json
traduction-udhr-propre-7b-fraeng.json
traduction-udhr-propre-7b.json
universaux-mesures.json
xnli-14b.json
xnli-14b-l18.json
xnli-14b-l24.json
xnli-14b-l30.json
xnli-14b-l36.json
xnli-1.5b.json
xnli-1.5b-l14.json
xnli-1.5b-l22.json
xnli-32b.json
xnli-32b-l32.json
xnli-3b.json
xnli-3b-l30.json
xnli-entrainement-3b.json
xnli-mlp-3b.json
xnli-train-complet-3b.json
---
reports/rapport-passage-a-l-echelle.md
reports/rapport-cerveau-modules.md
reports/cerveau-mesures.json
reports/INDEX.md
reports/README.md
reports/rapport-cerveau-corrections.md
reports/cerveau-mesures-corrigees.json
reports/rapport-pipeline-semantique.md
reports/pipeline-semantique.json
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n -i \"multiling\\|langue\\|invariance\\|M1\" reports/rapport-cerveau-modules.md | head -60", "description": "Search M1 multilingual findings in report"}`

  ```
1:# Rapport — modules cerveau-langage M1–M9
8:> [`rapport-cerveau-corrections.md`](rapport-cerveau-corrections.md) : M1 reste solide, M2 est vu/inédit,
14:- **M1** : codec + contexte, code RSN typé.
21:## 1 bis. La chaîne M1 → M4 → M8
24:M1 perçoit, M4 stocke, M8 consolide.
28:| surfaces perçues (M1) | **528 / 528** |
41:| **M1** | exact **1,000** ; sans contexte **0,708** ; canonique **1,000** ; invariance **1,000** ; 1 584 événements | ✅ |
53:- **M1** : avec/sans contexte (100 / 70,8).
63:1. **M1** est un **hub de lecture fiable** : 528/528 avec contexte, 100 % en canonique et en invariance.
76:- **M1 exact** ne veut pas dire **M1 neuronal** : c'est un bloc classique.
90:- **M5** : ordre 2, séquences stochastiques, comparaison à un modèle de langue.
91:- **M6** : conflit langue/tâche, coût en pas, inhibition.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\np='reports/jeux-mesures.json'\nd=json.load(open(p))\nprint(d.keys())\nfor k,v in d.items():\n    if isinstance(v,dict): print(k, list(v.keys())[:20])\nEOF", "description": "Inspect jeux-mesures JSON structure"}`

  ```
dict_keys(['date', 'rapide', 'couches', 'pensee', 'secondes', 'verdict'])
couches ['corpus', 'couverture', 'invariance', 'collisions', 'controle_lexique', 'controle_etiquettes', 'restitution', 'restitution_negative', 'compacite', 'vitesse', 'detection']
pensee ['morpion', 'echecs', 'dames', 'go', 'cartes', 'invariance_pensee', 'invariance_negative']
verdict ['ok', 'echecs']
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/jeux-mesures.json'))\nprint(json.dumps(d['couches']['corpus'], ensure_ascii=False)[:2000])\nprint('---invariance---')\nprint(json.dumps(d['couches']['invariance'], ensure_ascii=False)[:2000])\n … [161 caractères tronqués]`

  ```
{"items": 112, "par_jeu": {"morpion": 32, "echecs": 34, "dames": 16, "go": 14, "cartes": 16}}
---invariance---
{"0": {"niveau": 0, "bonnes": 9, "total": 33, "taux": 0.2727, "detail": {"cartes-carte-a": {"ok": false, "n": 4}, "cartes-carte-b": {"ok": false, "n": 4}, "cartes-donne-a": {"ok": true, "n": 1}, "cartes-donne-b": {"ok": true, "n": 1}, "cartes-main": {"ok": false, "n": 4}, "dames-blanc": {"ok": false, "n": 1}, "dames-depart": {"ok": false, "n": 2}, "dames-prise-multiple": {"ok": false, "n": 3}, "dames-prise-simple": {"ok": false, "n": 4}, "dames-simple": {"ok": true, "n": 1}, "dames-simple-c5": {"ok": false, "n": 3}, "echecs-depart": {"ok": false, "n": 3}, "echecs-droits-impossibles": {"ok": false, "n": 2}, "echecs-e4": {"ok": false, "n": 7}, "echecs-ep": {"ok": false, "n": 1}, "echecs-ep-inutile": {"ok": false, "n": 2}, "echecs-grand-roque": {"ok": false, "n": 2}, "echecs-nf3": {"ok": false, "n": 6}, "echecs-petit-roque": {"ok": false, "n": 2}, "echecs-pgn": {"ok": false, "n": 1}, "echecs-promotion": {"ok": false, "n": 2}, "go-5x5": {"ok": true, "n": 1}, "go-d4": {"ok": false, "n": 5}, "go-dd": {"ok": true, "n": 1}, "go-partie": {"ok": false, "n": 1}, "go-passe": {"ok": fa
… [1115 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('reports/universaux-mesures.json'))\ndef walk(o,p=''):\n    if isinstance(o,dict):\n        for k,v in o.items():\n            if isinstance(v,(dict,list)): walk(v,p+'/'+str(k))\n            else: print … [190 caractères tronqués]`

  ```
/corpus/B5_coups = 79
/corpus/B7_coups = 449
/corpus/items = 528
/corpus/train = 377
/corpus/val = 151
/corpus/paires_train = 25
/corpus/paires_val = 6
/schema/champs = 15
/schema/classes = 502
/schema/version = 1
/modele_natif/train_exact = 0.4827586206896552
/modele_natif/val_exact = 0.0
/modele_natif/gele_base_exact = 0.0
/modele_natif/majoritaire_exact = 0.0
/modele_natif/determinisme = 1.0
/modele_natif/invariance_paires = 0.0
/modele_natif/meilleur_pas = 100
/modele_natif/train_par_champ/jeu = 0.8063660477453581
/modele_natif/train_par_champ/action = 0.8143236074270557
/modele_natif/train_par_champ/de = 0.946949602122016
/modele_natif/train_par_champ/vers = 0.9496021220159151
/modele_natif/train_par_champ/promotion = 0.9946949602122016
/modele_natif/train_par_champ/roque = 0.9946949602122016
/modele_natif/train_par_champ/case = 0.9416445623342176
/modele_natif/train_par_champ/symbole = 0.9416445623342176
/modele_natif/train_par_champ/carte = 0.7824933687002652
/modele_natif/train_par_champ/taille = 0.9204244031830239
/modele_natif/train_par_champ/point = 0.9310344827586207
/modele_natif/train_par_champ/passe = 0.986737400530504
/modele_natif/train_par_champ/chemin_0 = 0.88328
… [3995 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Probing per-language M1 behavior to design the measurement module

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import Counter, defaultdict\nfrom cerveau.hub import Hub\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom jeux.codecs import c … [1294 caractères tronqués]`

  ```
items 528
par jeu without ctx {'morpion': 0.078, 'echecs': 0.945, 'dames': 1.0, 'go': 0.0, 'cartes': 1.0}
langues 67
fr 55 ctx 1.0 sans 0.545 det 0.618
notation 31 ctx 1.0 sans 0.548 det 0.871
en 15 ctx 1.0 sans 0.8 det 0.8
de 11 ctx 1.0 sans 0.727 det 0.727
es 11 ctx 1.0 sans 0.727 det 0.636
it 11 ctx 1.0 sans 0.727 det 0.909
ja 11 ctx 1.0 sans 0.727 det 1.0
nl 11 ctx 1.0 sans 0.727 det 0.636
pl 11 ctx 1.0 sans 0.727 det 0.545
pt 11 ctx 1.0 sans 0.727 det 0.909
ru 11 ctx 1.0 sans 0.727 det 0.727
zh 11 ctx 1.0 sans 0.727 det 0.909
cs 10 ctx 1.0 sans 0.8 det 0.6
da 10 ctx 1.0 sans 0.8 det 0.3
eo 10 ctx 1.0 sans 0.8 det 1.0
--- failures sans contexte (20) ---
('morpion', 'fr', 'morpion-a1', 'A1', True, False)
('morpion', 'fr', 'morpion-a1', 'a1', True, False)
('morpion', 'fr', 'morpion-a1', '(1,1)', True, False)
('morpion', 'fr', 'morpion-a1', '1 1', True, False)
('morpion', 'fr', 'morpion-a1', 'ligne 1 colonne 1', True, False)
('morpion', 'fr', 'morpion-a1', 'case 1', True, False)
('morpion', 'fr', 'morpion-a1', 'haut gauche', True, False)
('morpion', 'fr', 'morpion-a1', 'en haut à gauche', True, False)
('morpion', 'fr', 'morpion-a1', 'top left', True, False)
('morpion', 'fr', 'morp
… [667 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import Counter, defaultdict\nfrom cerveau.hub import Hub\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux imp … [658 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 15, in <module>
TypeError: '<' not supported between instances of 'NoneType' and 'str'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import defaultdict\nfrom cerveau.hub import Hub\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nitems=[]\nfor c in (construire_corpus() … [716 caractères tronqués]`

  ```
cartes   cartes-carte-a               n=  4 langues= 3 codes=1 inv=True
cartes   cartes-carte-b               n=  4 langues= 3 codes=1 inv=True
cartes   ml-cartes-10h                n= 36 langues=36 codes=1 inv=True
cartes   ml-cartes-ah                 n= 30 langues=30 codes=1 inv=True
cartes   ml-cartes-jc                 n= 30 langues=30 codes=1 inv=True
cartes   ml-cartes-ks                 n= 29 langues=29 codes=1 inv=True
cartes   ml-cartes-qd                 n= 28 langues=28 codes=1 inv=True
dames    None                         n=  2 langues= 1 codes=2 inv=False
dames    dames-blanc                  n=  1 langues= 1 codes=1 inv=True
dames    dames-prise-multiple         n=  3 langues= 1 codes=1 inv=True
dames    dames-prise-simple           n=  4 langues= 1 codes=1 inv=True
dames    dames-simple                 n=  1 langues= 1 codes=1 inv=True
dames    dames-simple-c5              n=  3 langues= 2 codes=1 inv=True
dames    ml-dames-b6c5                n= 56 langues=56 codes=1 inv=True
echecs   None                         n=  4 langues= 1 codes=4 inv=False
echecs   echecs-e4                    n=  7 langues= 3 codes=1 inv=True
echecs   echecs-ep                    n=  1 la
… [1276 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import Counter, defaultdict\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom jeux.lexique_multilingue import MULTI\nc=construire_corpus_multilingue()\ncnt=Counter(it.langue f … [511 caractères tronqués]`

  ```
langues corpus 66
absentes du corpus: ['ky', 'lo', 'mt', 'si', 'yo']
hors lexique: []
n min/max: 1 11
distribution n: Counter({10: 13, 4: 12, 11: 11, 5: 8, 8: 6, 1: 5, 6: 4, 2: 2, 7: 2, 3: 2, 9: 1})
af 8 {'echecs': 2, 'cartes': 5, 'go': 1}
am 1 {'go': 1}
ar 8 {'echecs': 2, 'cartes': 2, 'go': 2, 'dames': 1, 'morpion': 1}
az 4 {'echecs': 2, 'go': 1, 'dames': 1}
be 8 {'echecs': 2, 'cartes': 3, 'go': 1, 'dames': 1, 'morpion': 1}
bn 8 {'echecs': 2, 'cartes': 5, 'go': 1}
bs 4 {'echecs': 2, 'go': 1, 'dames': 1}
ca 8 {'echecs': 2, 'cartes': 3, 'go': 1, 'dames': 1, 'morpion': 1}
cs 10 {'echecs': 2, 'cartes': 5, 'go': 1, 'dames': 1, 'morpion': 1}
cy 4 {'echecs': 2, 'go': 1, 'dames': 1}
da 10 {'echecs': 2, 'cartes': 5, 'go': 1, 'dames': 1, 'morpion': 1}
de 11 {'echecs': 2, 'cartes': 5, 'go': 2, 'dames': 1, 'morpion': 1}
el 6 {'echecs': 2, 'cartes': 2, 'go': 1, 'dames': 1}
en 11 {'echecs': 2, 'cartes': 5, 'go': 2, 'dames': 1, 'morpion': 1}
eo 10 {'echecs': 2, 'cartes': 5, 'go': 1, 'dames': 1, 'morpion': 1}
es 11 {'echecs': 2, 'cartes': 5, 'go': 2, 'dames': 1, 'morpion': 1}
et 10 {'echecs': 2, 'cartes': 5, 'go': 1, 'dames': 1, 'morpion': 1}
eu 8 {'echecs': 2, 'cartes': 3, 'go': 1, 'dames': 1, '
… [2510 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import defaultdict, Counter\nfrom cerveau.hub import Hub\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux imp … [1824 caractères tronqués]`

  ```
=== contexte
paires 30 invariantes 30 1.0
=== sans contexte
  NON INV echecs echecs-e4 n 7 codes 2
  NON INV echecs echecs-ep n 1 codes 1
  NON INV echecs echecs-nf3 n 6 codes 2
  NON INV echecs echecs-promotion n 2 codes 2
  NON INV morpion morpion-a1 n 12 codes 2
  NON INV morpion morpion-centre n 6 codes 2
paires 30 invariantes 24 0.8
baseline ctx 514 514 1.0
baseline sans 369 514 0.7178988326848249
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import defaultdict\nfrom cerveau.hub import Hub\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux import code_ … [1133 caractères tronqués]`

  ```
ctx paires 30 multi 26 interlangues 15 codes identiques 15 dont valides 15 taux 1.0
sans paires 30 multi 26 interlangues 15 codes identiques 14 dont valides 14 taux 0.9333333333333333
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"A10\\|multilingue.py\" --include='*.md' --include='*.py' --include='*.json' . 2>/dev/null | head -30", "description": "Search for A10 or multilingue module references"}`

  ```
./reports/rapport-plateau-semantique.md:17:`tools/plateau_multilingue.py` : pour chaque couche, la similarité cosinus
./reports/07/p5.md:521:**Le dispositif** ✓✓ (`tools/pensee_multilingue.py` ✓) : le corpus **JW 2026** (mesure 76), 139 paragraphes, **les
./reports/07/p6.md:14:**Le test** ✓✓ (`tools/composition_multilingue.py` ✓) : on coupe chaque paragraphe en **préfixes proportionnels**
./reports/07/p8.md:178:**Le dispositif** ✓✓ (`tools/position_multilingue.py` ✓) : les **307 séries** de 8 phrases FR/EN (3 B), 214/93 ✓ ;
./reports/rapport-langues-maitres.md:211:  [`construire_lexique_multilingue.py`](../tools/jeux/construire_lexique_multilingue.py), chargé par
./reports/rapport-langues-maitres.md:212:  [`lexique_multilingue.py`](../tools/jeux/lexique_multilingue.py) ;
./reports/rapport-langues-maitres.md:213:- corpus : [`corpus_multilingue.py`](../tools/jeux/corpus_multilingue.py) ;
./data/ted2020/ted_fr_en.json:906179:"en": "We found activity in some cells called the A10 cells, cells that actually make dopamine, a natural stimulant, and spray it to many brain regions.",
./data/multiun/multiun_tech_fr_en.json:2539:"en": "A10.2.11.1 This section is used primarily by medical profe
… [3250 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls sprints/ | tail -20 && grep -rn -i \"invariance inter\\|baseline\" docs/ roadmap.md docs/roadmap.md 2>/dev/null | head -20", "description": "Inspect sprint docs for measurement conventions"}`

  ```
12-la-rotation-des-couches-compressees.md
13-les-deux-enigmes-du-decoupage-v41.md
14-p8-la-vivacit-de-l-engram-interrupteur-d.md
15-p9-le-poste-d-attention-v4-1-profiler-le.md
16-les-experts-sur-nvme-la-reutilisation.md
17-les-experts-io-ou-calcul.md
18-vectoriser-la-dequantification-des-experts.md
19-v41-a-1024-jetons.md
20-la-passe-longue-instrumentee.md
21-localiser-le-defaut-v41.md
22-la-composition-verifiee-et-les-deux-portes.md
23-la-porte-de-correction-outillee-et-longue.md
24-le-produit-scalaire-des-experts-vectorise.md
25-le-disque-dur-deguise-en-defaut-moteur.md
26-la-porte-a-512-et-la-granularite-qui-route.md
27-la-porte-p1-fermee-et-la-bascule-vers-kimi-k3.md
28-la-bascule-vers-kimi-k3-et-deux-defauts-de-tokenizer.md
29-87-go-par-jeton-et-la-recurrence-du-kda.md
30-la-reutilisation-des-experts-mesuree.md
31-le-regroupement-par-experts-mesure-et-k3-au-complet.md
docs/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md:257:> **Témoin constant** *(constant baseline)* — la réponse la plus bête possible :
docs/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md:265:> **Invariance inter-langue** *(cross-lingual invariance)* — à quel point deux langues
docs/glossaire
… [1680 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import Counter\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nitems=[]\nfor c in (construire_corpus(), construire_corpus_multilingue() … [297 caractères tronqués]`

  ```
sans paire 10 Counter({('morpion', 'morpion-a1-vs-b1'): 2, ('echecs', 'echecs-e4-vs-e3'): 2, ('echecs', 'echecs-nf3-vs-nc3'): 2, ('dames', 'dames-9-13-vs-10-14'): 2, ('go', 'go-d4-vs-d5'): 2})
avec paire 518
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport random\nfrom collections import Counter, defaultdict\nfrom cerveau.hub import Hub\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique … [1566 caractères tronqués]`

  ```
strict ctx n 369 exact_orig 0.0 exact_don 0.8997289972899729
strict sans n 369 exact_orig 0.0 exact_don 0.8482384823848238
 couverture {'cartes': 158, 'dames': 13, 'echecs': 140, 'go': 37, 'morpion': 21}
large ctx n 518 exact_orig 0.0 exact_don 0.8166023166023166
large sans n 518 exact_orig 0.0 exact_don 0.749034749034749
 couverture {'cartes': 161, 'dames': 68, 'echecs': 142, 'go': 85, 'morpion': 62}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport random\nfrom collections import Counter, defaultdict\nfrom cerveau.hub import Hub\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique … [1870 caractères tronqués]`

  ```
B5 69 orig 0.0 don 0.4927536231884058
B7 300 orig 0.0 don 0.9933333333333333
morpion 21 orig 0.0 don 0.7142857142857143
echecs 140 orig 0.0 don 0.9142857142857143
dames 13 orig 0.0 don 0.15384615384615385
go 37 orig 0.0 don 1.0
cartes 158 orig 0.0 don 0.9493670886075949
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import defaultdict\nfrom cerveau.hub import Hub\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux import code_rsn\nc=construire_corpus_multilingue()\nh=H … [514 caractères tronqués]`

  ```
=== ctx
ml-cartes-10h n 36 codes 1 none 0
ml-cartes-ah n 30 codes 1 none 0
ml-cartes-jc n 30 codes 1 none 0
ml-cartes-ks n 29 codes 1 none 0
ml-cartes-qd n 28 codes 1 none 0
ml-dames-b6c5 n 56 codes 1 none 0
ml-echecs-e4 n 61 codes 1 none 0
ml-echecs-nf3 n 61 codes 1 none 0
ml-go-d4 n 62 codes 1 none 0
ml-go-passe n 14 codes 1 none 0
ml-morpion-a1 n 42 codes 1 none 0
=== sans ctx
ml-cartes-10h n 36 codes 1 none 0
ml-cartes-ah n 30 codes 1 none 0
ml-cartes-jc n 30 codes 1 none 0
ml-cartes-ks n 29 codes 1 none 0
ml-cartes-qd n 28 codes 1 none 0
ml-dames-b6c5 n 56 codes 1 none 0
ml-echecs-e4 n 61 codes 1 none 0
ml-echecs-nf3 n 61 codes 1 none 0
ml-go-d4 n 62 codes 1 none 0
ml-go-passe n 14 codes 1 none 0
ml-morpion-a1 n 42 codes 1 none 0
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom cerveau.hub import Hub\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux import code_rsn\nc=construire_corpus_multilingue()\nh=Hub()\nfor it in c.items:\n    if it.p … [330 caractères tronqués]`

  ```
de 'go D4'
 ctx  {'jeu': 'go', 'action': 'poser', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': 9, 'point': 48, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}
 sans {'jeu': 'go', 'action': 'poser', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': 19, 'point': 288, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}
 att  {'jeu': 'go', 'action': 'poser', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': 9, 'point': 48, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}
fr 'go D4'
 ctx  {'jeu': 'go', 'action': 'poser', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': 9, 'point': 48, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}
 sans {'jeu': 'go', 'action': 'poser', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': 19, 'point': 288, 'passe': None, 'chemin_0': None, 'chemin_1'
… [998 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import Counter, defaultdict\nfrom cerveau.hub import Hub\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux imp … [872 caractères tronqués]`

  ```
morpion 62 2 0.03225806451612903
echecs 141 140 0.9929078014184397
dames 66 66 1.0
go 84 0 0.0
cartes 161 161 1.0
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import Counter\nfrom cerveau.hub import Hub\nfrom jeux.corpus import construire_corpus\nfrom semantique.universaux import code_rsn\nc=construire_corpus(); h=Hub()\nfor p in (\"echecs-e4\",\"echecs-n … [459 caractères tronqués]`

  ```
== echecs-e4
 notation  'e2e4'                         ctx=True sans=True code_sans={'jeu': 'echecs', 'action': 'deplacer', 'de': 52, 'vers': 36, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}
 notation  'e2-e4'                        ctx=True sans=True code_sans={'jeu': 'echecs', 'action': 'deplacer', 'de': 52, 'vers': 36, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}
 notation  'e2 e4'                        ctx=True sans=True code_sans={'jeu': 'echecs', 'action': 'deplacer', 'de': 52, 'vers': 36, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}
 notation  'e4'                           ctx=True sans=False code_sans=None
 notation  'E4'                           ctx=True sans=False code_sans=None
 fr        'le pion de e2 vers e4'        ctx=True sans=True code_sans={'jeu': 'echecs', 'acti
… [4523 caractères tronqués]
  ```

- **bash** `{"command": "date -u +%Y-%m-%dT%H:%M:%SZ && python3 -V && cd /home/stephane/GitHub/Qtrinet && ls tools/cerveau/tests/__pycache__ >/dev/null 2>&1; echo ok", "description": "Show current date and Python version"}`

  ```
2026-10-27T16:14:16Z
Python 3.13.15
ok
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import defaultdict\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux import code_rsn\nitems=[]\nfor c in (cons … [459 caractères tronqués]`

  ```
paires 30 incoherentes 0
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '104,235p' tools/jeux/codecs/base.py", "description": "Inspect codec factory and lit contract"}`

  ```
class Codec:
    """La base : un codec déclare son jeu, ses formats et ses motifs."""

    jeu: str = "?"
    formats: tuple[str, ...] = ("canonique",)

    # ---- à implémenter par chaque codec --------------------------------
    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
            langue: str | None = None) -> Lecture:
        raise NotImplementedError

    def rend(self, rsn: RSN, format: str = "canonique", langue: str = "fr",
             contexte: RSN | None = None) -> str:
        raise NotImplementedError

    def detecte(self, texte: str) -> float:
        return 0.0

    # ---- aides communes ------------------------------------------------
    def sans_nom_jeu(self, texte: str) -> str:
        """Retire un nom de jeu en tête (« шахматы конь g1 f3 » → « конь g1 f3 »).

        Les libellés viennent du lexique multilingue ; le retrait est fait sur la
        forme normalisée du libellé, avec des séparateurs souples (tiret, espace,
        apostrophe). On ne retire que si le reste n'est pas vide.
        """
        ms = MULTI.cherche("jeu.nom", texte)
        if not ms:
            return texte
        m = max(ms, key=lambda x: len(x.forme))

… [4720 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import defaultdict\nfrom cerveau.hub import Hub\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux import code_rsn\nc=construire_corpus_multilingue(); h=H … [453 caractères tronqués]`

  ```
echecs 122 122 122 1.0
cartes 153 153 153 1.0
go 76 76 0 0.0
dames 56 56 56 1.0
morpion 42 42 0 0.0
B7 total [449, 449, 331] 0.7371937639198218
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import Counter, defaultdict\nfrom cerveau.hub import Hub\nfrom jeux.corpus import construire_corpus\nfrom semantique.universaux import code_rsn\nc=construire_corpus(); h=Hub()\nitems=[it for it in c … [754 caractères tronqués]`

  ```
B5 baseline sans 38 65 0.5846153846153846
B5 exact sans 43 79
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import defaultdict\nfrom cerveau.hub import Hub\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux import code_ … [857 caractères tronqués]`

  ```
M1 sans on baseline-applicable 368 514 0.7159533073929961
M1 sans on excluded 6 14
morpion notation None 'A1' False
morpion notation None 'B1' False
echecs notation echecs-ep 'exd6' False
echecs notation None 'e2e4' True
echecs notation None 'e2e3' True
echecs notation None 'Nf3' False
echecs notation None 'Nc3' False
dames notation dames-simple '9-13' True
dames notation dames-blanc 'c3-d4' True
dames notation None '9-13' True
dames notation None '10-14' True
go notation go-dd 'B[dd]' False
go notation None 'D4' False
go notation None 'D5' False
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import Counter, defaultdict\nfrom cerveau.hub import Hub\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux imp … [971 caractères tronqués]`

  ```
morpion 62 M1 5 0.08064516129032258 base 2 0.03225806451612903 delta -0.04838709677419355
echecs 141 M1 136 0.9645390070921985 base 140 0.9929078014184397 delta 0.028368794326241134
dames 66 M1 66 1.0 base 66 1.0 delta 0.0
go 84 M1 0 0.0 base 0 0.0 delta 0.0
cartes 161 M1 161 1.0 base 161 1.0 delta 0.0
  ```

### 🤖 Assistant

⏵ Writing the multilingual M1 measurement module

- **write** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "content": "#!/usr/bin/env python3\n\"\"\"multilingue.py — M1 (hub typé) mesuré sur le corpus multilingue réel.\n\nLe module ne remplace aucun codec : il **appelle** `Hub.percevoir` et\n`Hub.rendre`, et agrège les résultats  … [49014 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 👤 Utilisateur

Agent f0969e87-af0c-43b1-93cf-f278d9c90846 sent a message: 
Timebox : donne un point et écris /tmp/a10-multilingue.json/.md dès qu'une mesure existe, même partielle ; termine ensuite.

### 🤖 Assistant

⏵ Running the new module to get first measurements and outputs

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools python3 tools/cerveau/multilingue.py", "description": "Run multilingual M1 measurement CLI"}`

  ```
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", line 1051, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", line 1038, in main
    chemin_md.write_text(rendre_markdown(resultat) + "\n", encoding="utf-8")
                         ~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", line 785, in rendre_markdown
    f"- **Invariance interlangues** : **{_frac(inv)}** des paires avec "
                                         ~~~~~^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", line 741, in _frac
    return f"{res['ok']} / {res['n']} ({_pct(res['taux'])})"
              ~~~^^^^^^
KeyError: 'ok'

real	0m3,578s
user	0m3,560s
sys	0m0,018s
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"_frac(\" tools/cerveau/multilingue.py", "description": "List _frac call sites"}`

  ```
738:def _frac(res: dict | None) -> str:
780:        f"- **Avec contexte** : M1 lit **{_frac(g['exact_contexte'])}** et le "
781:        f"canonique revient à **{_frac(g['canonique'])}**.",
782:        f"- **Sans contexte** : **{_frac(g['exact_sans_contexte'])}** ; c'est là "
785:        f"- **Invariance interlangues** : **{_frac(inv)}** des paires avec "
791:        f"- **Baseline surface** : {_frac(baseline['exact_sans_contexte'])} sans "
793:        f"{_frac(baseline['m1_sur_applicables']['exact_sans_contexte'])} pour M1 "
800:            f"**{_frac(strict['exact_attendu_contexte'])}**, exact donneur "
801:            f"**{_frac(strict['exact_donateur_contexte'])}** avec contexte "
802:            f"(B7 : **{_frac(b7['controle_strict']['exact_donateur_contexte'])}**). "
867:            ["exact avec contexte", _frac(g["exact_contexte"])],
868:            ["exact sans contexte", _frac(g["exact_sans_contexte"])],
869:            ["canonique", _frac(g["canonique"])],
871:             _frac({"ok": inv["invariantes_contexte"], "n": inv["n"],
874:             _frac({"ok": inv["invariantes_sans_contexte"], "n": inv["n"],
877:             _frac({"ok": inv_multi["invariantes_contexte"], "n
… [988 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "old_string": "        f\"- **Invariance interlangues** : **{_frac(inv)}** des paires avec \"\n        f\"contexte et **{inv['invariantes_sans_contexte']} / {inv['n']}** sans \"\n        \"contexte. Les variantes de langue d … [425 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools python3 tools/cerveau/multilingue.py && echo '---' && ls -la /tmp/a10-multilingue.* && head -80 /tmp/a10-multilingue.md", "description": "Rerun measurement and inspect reports"}`

  ```
A10 — M1 multilingue : 528 items, exact ctx 100,0 %, sans ctx 70,8 %, invariance interlangues 100,0 %
JSON : /tmp/a10-multilingue.json
MD   : /tmp/a10-multilingue.md
---
-rw-r--r--. 1 stephane stephane 486460 27 oct 12:23 /tmp/a10-multilingue.json
-rw-r--r--. 1 stephane stephane  10096 27 oct 12:23 /tmp/a10-multilingue.md
# A10 — M1 (hub typé) sur le corpus multilingue

**Date** : 2026-10-27T16:23:36+00:00  
**Périmètre** : coups (mêmes items que batterie.m1), 528 surfaces, 66 langues réelles.  
**Source de mesure** : `tools/cerveau/hub.py` (`Hub.percevoir`, `Hub.rendre`), sans modification des modules existants.

## Verdict

- **Avec contexte** : M1 lit **528 / 528 (100,0 %)** et le canonique revient à **528 / 528 (100,0 %)**.
- **Sans contexte** : **374 / 528 (70,8 %)** ; c'est là que se voient les dépendances au contexte (go, morpion, notations courtes).
- **Invariance interlangues** : **15 / 15 (100,0 %)** des paires avec contexte et **14 / 15** sans contexte. Les variantes de langue d'une même paire donnent bien le même code.
- **Mais invariance ≠ exactitude** : sans contexte, les paires go et morpion peuvent être invariantes avec un code faux (voir § 5).
- **Baseline surface*
… [4851 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/a10-multilingue.json'))\nfor nom,p in d['paires'].items():\n    if p['n_langues']>=2 and not p['invariante_interlangues_sans_contexte']:\n        print(nom, p['jeu'], 'langues',p['langues'])\n     … [326 caractères tronqués]`

  ```
echecs-nf3 echecs langues ['en', 'fr']
 codes sans [{'action': 'deplacer', 'carte': None, 'case': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None, 'de': 62, 'jeu': 'echecs', 'passe': None, 'point': None, 'promotion': None, 'roque': None, 'symbole': None, 'taille': None, 'vers': 45}, None]
 deviantes sans [{'langue': 'fr', 'texte': 'Cf3'}]
 codes ctx [{'action': 'deplacer', 'carte': None, 'case': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None, 'de': 62, 'jeu': 'echecs', 'passe': None, 'point': None, 'promotion': None, 'roque': None, 'symbole': None, 'taille': None, 'vers': 45}]
 deviantes ctx []
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/a10-multilingue.json'))\nfor s,v in d['par_source'].items():\n    print(s, 'n',v['n'],'langues',len(v['langues']),'exact',v['exact_contexte'],v['exact_sans_contexte'],'canon',v['canonique'])\n     … [439 caractères tronqués]`

  ```
B5 n 79 langues 2 exact {'ok': 79, 'n': 79, 'taux': 1.0} {'ok': 43, 'n': 79, 'taux': 0.544304} canon {'ok': 79, 'n': 79, 'taux': 1.0}
  inv inter {'n': 4, 'invariantes_contexte': 4, 'taux_contexte': 1.0, 'invariantes_sans_contexte': 3, 'taux_sans_contexte': 0.75}
  inv multi {'n': 15, 'invariantes_contexte': 15, 'taux_contexte': 1.0, 'invariantes_sans_contexte': 10, 'taux_sans_contexte': 0.666667}
  baseline 65 {'ok': 38, 'n': 65, 'taux': 0.584615} m1 {'ok': 37, 'n': 65, 'taux': 0.569231} delta 0.015385
  controle {'n_items': 79, 'n': 69, 'exact_attendu_contexte': {'ok': 0, 'n': 69, 'taux': 0.0}, 'exact_donateur_contexte': {'ok': 34, 'n': 69, 'taux': 0.492754}, 'exact_attendu_sans_contexte': {'ok': 0, 'n': 69, 'taux': 0.0}, 'exact_donateur_sans_contexte': {'ok': 42, 'n': 69, 'taux': 0.608696}}
B7 n 449 langues 66 exact {'ok': 449, 'n': 449, 'taux': 1.0} {'ok': 331, 'n': 449, 'taux': 0.737194} canon {'ok': 449, 'n': 449, 'taux': 1.0}
  inv inter {'n': 11, 'invariantes_contexte': 11, 'taux_contexte': 1.0, 'invariantes_sans_contexte': 11, 'taux_sans_contexte': 1.0}
  inv multi {'n': 11, 'invariantes_contexte': 11, 'taux_contexte': 1.0, 'invariantes_sans_contexte': 11, 'taux_sans_conte
… [422 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/a10-multilingue.json'))\nfor k,v in d.items():\n    print(k, len(json.dumps(v, ensure_ascii=False)))\nEOF", "description": "Measure JSON section sizes"}`

  ```
meta 2186
global 2082
par_jeu 9615
par_langue 109050
par_langue_jeu 159470
par_source 4411
paires 59409
controle_surface_permutee 4996
autocritique 1675
duree_s 5
  ```

- **bash** `{"command": "sed -n '80,220p' /tmp/a10-multilingue.md", "description": "Read rest of generated Markdown"}`

  ```
|---|---|---|---|---|---|---|---|---|---|
| cartes-carte-a | cartes | 4 | 2 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |
| cartes-carte-b | cartes | 4 | 2 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |
| echecs-e4 | echecs | 7 | 2 | 1 | 2 | oui | oui | 100,0 % | 71,4 % |
| echecs-nf3 | echecs | 6 | 2 | 1 | 2 | oui | non | 100,0 % | 66,7 % |
| ml-cartes-10h | cartes | 36 | 36 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |
| ml-cartes-ah | cartes | 30 | 30 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |
| ml-cartes-jc | cartes | 30 | 30 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |
| ml-cartes-ks | cartes | 29 | 29 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |
| ml-cartes-qd | cartes | 28 | 28 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |
| ml-dames-b6c5 | dames | 56 | 56 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |
| ml-echecs-e4 | echecs | 61 | 61 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |
| ml-echecs-nf3 | echecs | 61 | 61 | 1 | 1 | oui | oui | 100,0 % | 100,0 % |
| ml-go-d4 | go | 62 | 62 | 1 | 1 | oui | oui | 100,0 % | 0,0 % |
| ml-go-passe | go | 14 | 14 | 1 | 1 | oui | oui | 100,0 % | 0,0 % |
| ml-morpion-a1 | morpion | 42 | 42 | 1 | 1 | oui | oui | 100,0 % | 0,0 % |

Les paires B7 (`ml-…`) ont de 14 à 62 varia
… [3105 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"## 4. Par jeu\" -A 12 /tmp/a10-multilingue.md | head -20 && echo '---' && grep -n \"## 7\" /tmp/a10-multilingue.md", "description": "Locate per-game and autocritique sections"}`

  ```
65:## 4. Par jeu
66-
67-| jeu | n | langues | exact ctx | exact sans ctx | canonique | inv. interlangues ctx | inv. interlangues sans ctx | inv. toutes variantes sans ctx |
68-|---|---|---|---|---|---|---|---|---|
69-| morpion | 64 | 42 | 100,0 % | 7,8 % | 100,0 % | 1 / 1 (100,0 %) | 1 / 1 (100,0 %) | 2 / 4 (50,0 %) |
70-| echecs | 146 | 62 | 100,0 % | 94,5 % | 100,0 % | 4 / 4 (100,0 %) | 3 / 4 (75,0 %) | 4 / 7 (57,1 %) |
71-| dames | 70 | 56 | 100,0 % | 100,0 % | 100,0 % | 1 / 1 (100,0 %) | 1 / 1 (100,0 %) | 4 / 4 (100,0 %) |
72-| go | 87 | 62 | 100,0 % | 0,0 % | 100,0 % | 2 / 2 (100,0 %) | 2 / 2 (100,0 %) | 4 / 4 (100,0 %) |
73-| cartes | 161 | 36 | 100,0 % | 100,0 % | 100,0 % | 7 / 7 (100,0 %) | 7 / 7 (100,0 %) | 7 / 7 (100,0 %) |
74-
75-Le go et le morpion sont les deux jeux où le contexte porte le sens (taille du plateau, symbole au trait) : leur exact sans contexte est bas, mais leurs paires restent invariantes. C'est le point « invariance ≠ exactitude ».
76-
77-## 5. Invariance interlangues, paire par paire
---
113:## 7. Autocritique — ce qui pourrait rendre ce résultat faux
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"## [0-9]\" tools/cerveau/multilingue.py", "description": "Locate markdown section headers in source"}`

  ```
806:        "## 1. Ce qui existe réellement dans le corpus",
838:        "## 2. Définitions",
860:        "## 3. Résultats globaux",
917:        "## 4. Par jeu",
947:        "## 5. Invariance interlangues, paire par paire",
970:        "## 6. Baseline et contrôle permuté",
999:        "## 7. Autocritique — ce qui pourrait rendre ce résultat faux",
1005:        "## 8. Reproductibilité",
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "old_string": "        f\"- **Invariance interlangues** : **{_frac({'ok': inv['invariantes_contexte'], 'n': inv['n'], 'taux': inv['taux_contexte']})}** \"\n        f\"des paires avec contexte et **{inv['invariantes_sans_cont … [1314 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "old_string": "        f\"- **Sans contexte** : **{_frac(g['exact_sans_contexte'])}** ; c'est là \"\n        \"que se voient les dépendances au contexte (go, morpion, notations \"\n        \"courtes).\",", "new_string": "    … [238 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "offset": 912, "limit": 70}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py</path>
<type>file</type>
<content>
912:                  _frac(strict["exact_donateur_sans_contexte"])],
913:                 ["exact donneur B7 (ctx)",
914:                  _frac(b7["controle_strict"]["exact_donateur_contexte"])],
915:                 ["exact donneur, variante large (ctx)",
916:                  _frac(large["exact_donateur_contexte"])],
917:             ])
918: 
919:     lignes += [
920:         "",
921:         "## 4. Par jeu",
922:         "",
923:     ]
924:     lignes += _tableau(
925:         ["jeu", "n", "langues", "exact ctx", "exact sans ctx", "canonique",
926:          "inv. interlangues ctx", "inv. interlangues sans ctx",
927:          "inv. toutes variantes sans ctx"],
928:         [[jeu,
929:           str(v["n"]),
930:           str(len(v["langues"])),
931:           _pct(v["exact_contexte"]["taux"]),
932:           _pct(v["exact_sans_contexte"]["taux"]),
933:           _pct(v["canonique"]["taux"]),
934:           _frac({"ok": v["invariance_interlangues"]["invariantes_contexte"],
935:                  "n": v["invariance_interlangues"]["n"],
936:                  "taux": v["invariance_in
… [2525 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "old_string": "    lignes += [\n        \"\",\n        \"## 4. Par jeu\",\n        \"\",\n    ]\n    lignes += _tableau(\n        [\"jeu\", \"n\", \"langues\", \"exact ctx\", \"exact sans ctx\", \"canonique\",\n         \"in … [1761 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "old_string": "    lignes += [\n        \"\",\n        \"Le go et le morpion sont les deux jeux où le contexte porte le sens \"\n        \"(taille du plateau, symbole au trait) : leur exact sans contexte est \"\n        \"ba … [2635 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"## [0-9]\" tools/cerveau/multilingue.py", "description": "List markdown section headers after edits"}`

  ```
810:        "## 1. Ce qui existe réellement dans le corpus",
842:        "## 2. Définitions",
864:        "## 3. Résultats globaux",
921:        "## 4. Par source",
947:        "## 5. Par jeu",
977:        "## 6. Par langue",
1014:        "## 7. Invariance interlangues, paire par paire",
1035:        "## 6. Baseline et contrôle permuté",
1064:        "## 7. Autocritique — ce qui pourrait rendre ce résultat faux",
1070:        "## 8. Reproductibilité",
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re\np='tools/cerveau/multilingue.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('\"## 6. Baseline et contrôle permuté\"','\"## 8. Baseline et contrôle permuté\"')\ns=s.replace('\"## 7. Autocritique — ce qui pourrait rend … [305 caractères tronqués]`

  ```
810:        "## 1. Ce qui existe réellement dans le corpus",
842:        "## 2. Définitions",
864:        "## 3. Résultats globaux",
921:        "## 4. Par source",
947:        "## 5. Par jeu",
977:        "## 6. Par langue",
1014:        "## 7. Invariance interlangues, paire par paire",
1035:        "## 8. Baseline et contrôle permuté",
1064:        "## 9. Autocritique — ce qui pourrait rendre ce résultat faux",
1070:        "## 10. Reproductibilité",
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '670,735p' tools/cerveau/multilingue.py", "description": "Read autocritique function"}`

  ```
"coordonnée » ; la réussite mesure la reconnaissance lexicale, pas la "
         "compréhension d'une phrase libre ni la traduction."),
    ]
    absentes = r["meta"]["langues_absentes_du_corpus"]
    if absentes:
        lignes.append(
            f"{r['meta']['langues_corpus']} langues réelles sur "
            f"{r['meta']['langues_lexique']} du lexique ; absentes du corpus : "
            f"{', '.join(absentes)}. Elles ne sont pas complétées.")
    n1 = r["meta"].get("langues_n1", [])
    if n1:
        lignes.append(
            f"n par langue de 1 à "
            f"{max(x['n'] for x in r['par_langue'].values())} ; "
            f"{len(n1)} langue(s) à n=1 ({', '.join(n1)}) : un taux de 0 ou "
            f"100 % sur un seul item n'est pas une estimation.")
    lignes.append(
        "Invariance n'est pas exactitude : sans contexte, les paires go et "
        "morpion restent souvent invariantes (même code pour toutes les "
        f"langues) alors que le code est faux (go : {_pct(go['exact_sans_contexte']['taux'])}, "
        f"morpion : {_pct(morpion['exact_sans_contexte']['taux'])} d'exact).")
    if "controle_strict" in g:
        c = g["controle_strict"]
        lignes.ap
… [1917 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "old_string": "    meta[\"par_jeu\"] = {}\n    for jeu in JEUX:\n        par_jeu = [s for s in surfaces if s.jeu == jeu]\n        meta[\"par_jeu\"][jeu] = {\n            \"n\": len(par_jeu),\n            \"langues\": len({s. … [832 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "offset": 220, "limit": 45}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py</path>
<type>file</type>
<content>
220:     records = []
221:     for s in surfaces:
222:         attendu = code_rsn(s.attendu)
223:         code_ctx = hub.percevoir(s.texte, s.jeu, s.contexte)
224:         code_sans = hub.percevoir(s.texte, s.jeu, None)
225:         records.append({
226:             "texte": s.texte,
227:             "jeu": s.jeu,
228:             "langue": s.langue,
229:             "paire": s.paire,
230:             "source": s.source,
231:             "format": s.format,
232:             "contexte": s.contexte,
233:             "attendu": attendu,
234:             "code_contexte": code_ctx,
235:             "code_sans_contexte": code_sans,
236:             "exact_contexte": code_ctx == attendu,
237:             "exact_sans_contexte": code_sans == attendu,
238:             "canonique": _canonique(hub, s, code_ctx),
239:             "baseline_applicable": False,
240:             "baseline_exact_contexte": False,
241:             "baseline_exact_sans_contexte": False,
242:         })
243:     return records
244: 
245: 
246: # ---------------------------------------------------------------------------
… [726 caractères tronqués]
  ```

- **grep** `{"pattern": "meta\\[\"par_jeu\"\\]", "path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py"}`

  ```
Found 3 matches

/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py
Line 180:     meta["par_jeu"] = {}
Line 183:         meta["par_jeu"][jeu] = {
Line 621:     meta["langues_par_jeu"] = {j: v["langues"] for j, v in meta["par_jeu"].items()}
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "offset": 176, "limit": 18}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py</path>
<type>file</type>
<content>
176:                                     if s.langue == LANGUE_NOTATION}),
177:     }
178: 
179:     # Comptes par jeu, utiles pour lire les taux sans contexte.
180:     meta["par_jeu"] = {}
181:     for jeu in JEUX:
182:         par_jeu = [s for s in surfaces if s.jeu == jeu]
183:         meta["par_jeu"][jeu] = {
184:             "n": len(par_jeu),
185:             "langues": len({s.langue for s in par_jeu if s.langue != LANGUE_NOTATION}),
186:             "paires": len({s.paire for s in par_jeu if s.paire is not None}),
187:         }
188:     return surfaces, meta
189: 
190: 
191: # ---------------------------------------------------------------------------
192: # Mesure item par item
193: # ---------------------------------------------------------------------------

(Showing lines 176-193 of 1116. Use offset=194 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "old_string": "        meta[\"par_jeu\"][jeu] = {\n            \"n\": len(par_jeu),\n            \"langues\": len({s.langue for s in par_jeu if s.langue != LANGUE_NOTATION}),\n            \"paires\": len({s.paire for s in pa … [618 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "offset": 616, "limit": 14}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py</path>
<type>file</type>
<content>
616:                 "baseline_surface": _stats_baseline(rs),
617:             }
618: 
619:     meta["items_sans_paire"] = global_["items_sans_paire"]
620:     meta["paires"] = global_["n_paires"]
621:     meta["paires_multi"] = global_["n_paires_multi"]
622:     meta["paires_interlangues"] = global_["n_paires_interlangues"]
623:     meta["items_paires_multi"] = global_["baseline_surface"]["n_applicable"]
624:     meta["langues_n1"] = _langues_n1(records)
625:     meta["langues_par_jeu"] = {j: v["langues"] for j, v in meta["par_jeu"].items()}
626: 
627:     resultat = {
628:         "meta": meta,
629:         "global": global_,

(Showing lines 616-629 of 1120. Use offset=630 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "old_string": "    meta[\"langues_n1\"] = _langues_n1(records)\n    meta[\"langues_par_jeu\"] = {j: v[\"langues\"] for j, v in meta[\"par_jeu\"].items()}", "new_string": "    meta[\"langues_n1\"] = _langues_n1(records)\n     … [123 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "old_string": "    n1 = r[\"meta\"].get(\"langues_n1\", [])\n    if n1:\n        lignes.append(\n            f\"n par langue de 1 à \"\n            f\"{max(x['n'] for x in r['par_langue'].values())} ; \"\n            f\"{len … [589 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "old_string": "        \"Les paires B7 (`ml-…`) ont de 14 à 62 variantes de langue. Le détail \"\n        \"des codes uniques, des surfaces déviantes et des langues est dans le \"\n        \"JSON (`paires`).\",", "new_string … [516 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"La baseline ne gagne pas uniformément\" -A 6 tools/cerveau/multilingue.py", "description": "Locate baseline note"}`

  ```
1068:        "La baseline ne gagne pas uniformément : elle corrige des incohérences "
1069-        "de notation dans les échecs, mais elle **cache** les erreurs du "
1070-        "morpion en figeant un code faux. Le contrôle permuté, lui, vérifie "
1071-        "que le code suit la surface donneuse : la lecture n'est pas un simple "
1072-        "effet de l'étiquette de paire.",
1073-        "",
1074-        "## 9. Autocritique — ce qui pourrait rendre ce résultat faux",
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "old_string": "        \"La baseline ne gagne pas uniformément : elle corrige des incohérences \"\n        \"de notation dans les échecs, mais elle **cache** les erreurs du \"\n        \"morpion en figeant un code faux. Le c … [894 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools python3 tools/cerveau/multilingue.py && echo '---' && sed -n '1,140p' /tmp/a10-multilingue.md", "description": "Rerun measurement and inspect updated report"}`

  ```
A10 — M1 multilingue : 528 items, exact ctx 100,0 %, sans ctx 70,8 %, invariance interlangues 100,0 %
JSON : /tmp/a10-multilingue.json
MD   : /tmp/a10-multilingue.md
---
# A10 — M1 (hub typé) sur le corpus multilingue

**Date** : 2026-10-27T16:28:46+00:00  
**Périmètre** : coups (mêmes items que batterie.m1), 528 surfaces, 66 langues réelles.  
**Source de mesure** : `tools/cerveau/hub.py` (`Hub.percevoir`, `Hub.rendre`), sans modification des modules existants.

## Verdict

- **Avec contexte** : M1 lit **528 / 528 (100,0 %)** et le canonique revient à **528 / 528 (100,0 %)**.
- **Sans contexte** : **374 / 528 (70,8 %)** ; c'est là que se voient les dépendances au contexte (go, morpion, notations courtes). Sur B7 seul : 331 / 449 (73,7 %).
- **Invariance interlangues** : **15 / 15 (100,0 %)** des paires avec contexte et **14 / 15** sans contexte. **Sur B7 seul : 11 / 11 (100,0 %) avec contexte et 11 / 11 (100,0 %) sans contexte. L'unique échec sans contexte est B5 `echecs-nf3` (`Cf3`, notation française courte qui a besoin du contexte).
- **Mais invariance ≠ exactitude** : sans contexte, les paires go et morpion restent invariantes avec un code faux (voir § 7).
- **Baseline surface
… [10434 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '140,260p' /tmp/a10-multilingue.md", "description": "Read remainder of updated Markdown"}`

  ```
| cy | 4 | 1d 2e 1g | 100,0 % | 75,0 % | 100,0 % | 100,0 % / 100,0 % (4) | 3 / 4 (75,0 %) |
| hi | 4 | 1d 2e 1g | 100,0 % | 75,0 % | 100,0 % | 100,0 % / 100,0 % (4) | 3 / 4 (75,0 %) |
| is | 4 | 1d 2e 1g | 100,0 % | 75,0 % | 100,0 % | 100,0 % / 100,0 % (4) | 3 / 4 (75,0 %) |
| ka | 4 | 1d 2e 1g | 100,0 % | 75,0 % | 100,0 % | 100,0 % / 100,0 % (4) | 3 / 4 (75,0 %) |
| mk | 4 | 1d 2e 1g | 100,0 % | 75,0 % | 100,0 % | 100,0 % / 100,0 % (4) | 3 / 4 (75,0 %) |
| mn | 4 | 1d 2e 1g | 100,0 % | 75,0 % | 100,0 % | 100,0 % / 100,0 % (4) | 3 / 4 (75,0 %) |
| nn | 4 | 1d 2e 1g | 100,0 % | 75,0 % | 100,0 % | 100,0 % / 100,0 % (4) | 3 / 4 (75,0 %) |
| ta | 4 | 2e 1g 1m | 100,0 % | 50,0 % | 100,0 % | 100,0 % / 100,0 % (4) | 2 / 4 (50,0 %) |
| ur | 4 | 1d 2e 1g | 100,0 % | 75,0 % | 100,0 % | 100,0 % / 100,0 % (4) | 3 / 4 (75,0 %) |
| uz | 4 | 1d 2e 1g | 100,0 % | 75,0 % | 100,0 % | 100,0 % / 100,0 % (4) | 3 / 4 (75,0 %) |
| ga | 3 | 2e 1g | 100,0 % | 66,7 % | 100,0 % | 100,0 % / 100,0 % (3) | 2 / 3 (66,7 %) |
| sw | 3 | 2e 1g | 100,0 % | 66,7 % | 100,0 % | 100,0 % / 100,0 % (3) | 2 / 3 (66,7 %) |
| kk | 2 | 1d 1g | 100,0 % | 50,0 % | 100,0 % | 100,0 % / 100,0 % (2) | 1 / 2 (50,0 %) |
| ne | 2 | 2e
… [5832 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "offset": 786, "limit": 22}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py</path>
<type>file</type>
<content>
786:         f"- **Avec contexte** : M1 lit **{_frac(g['exact_contexte'])}** et le "
787:         f"canonique revient à **{_frac(g['canonique'])}**.",
788:         f"- **Sans contexte** : **{_frac(g['exact_sans_contexte'])}** ; c'est là "
789:         "que se voient les dépendances au contexte (go, morpion, notations "
790:         f"courtes). Sur B7 seul : {_frac(b7['exact_sans_contexte'])}.",
791:         f"- **Invariance interlangues** : **{_frac({'ok': inv['invariantes_contexte'], 'n': inv['n'], 'taux': inv['taux_contexte']})}** "
792:         f"des paires avec contexte et **{inv['invariantes_sans_contexte']} / "
793:         f"{inv['n']}** sans contexte. **Sur B7 seul : "
794:         f"{_frac({'ok': b7['invariance_interlangues']['invariantes_contexte'], 'n': b7['invariance_interlangues']['n'], 'taux': b7['invariance_interlangues']['taux_contexte']})} "
795:         "avec contexte et "
796:         f"{_frac({'ok': b7['invariance_interlangues']['invariantes_sans_contexte'], 'n': b7['invariance_interlangues']['n'], 'taux': b7['invariance_interlangues']['taux_sans_contexte']})} "
7
… [767 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py", "old_string": "        f\"{inv['n']}** sans contexte. **Sur B7 seul : \"\n        f\"{_frac({'ok': b7['invariance_interlangues']['invariantes_contexte'], 'n': b7['invariance_interlangues']['n'], 'taux': b7['invariance_interl … [1047 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 tools/cerveau/multilingue.py >/tmp/a10-run.log && python3 - <<'EOF'\nimport json\np='/tmp/a10-multilingue.json'\nd=json.load(open(p))\njson.dumps(d, ensure_ascii=False, allow_nan=False)\nprint(\"JSON OK\", len(open(p,'rb').rea … [607 caractères tronqués]`

  ```
JSON OK 486559 octets
global {'ok': 528, 'n': 528, 'taux': 1.0} {'ok': 374, 'n': 528, 'taux': 0.708333} {'ok': 528, 'n': 528, 'taux': 1.0}
inv {'n': 15, 'invariantes_contexte': 15, 'taux_contexte': 1.0, 'invariantes_sans_contexte': 14, 'taux_sans_contexte': 0.933333}
B7 {'ok': 449, 'n': 449, 'taux': 1.0} {'ok': 331, 'n': 449, 'taux': 0.737194} {'n': 11, 'invariantes_contexte': 11, 'taux_contexte': 1.0, 'invariantes_sans_contexte': 11, 'taux_sans_contexte': 1.0}
baseline {'definition': 'code majoritaire des autres surfaces de la paire (leave-one-out), même code pour toutes les surfaces', 'n_items': 528, 'n_applicable': 514, 'm1_sur_applicables': {'exact_contexte': {'ok': 514, 'n': 514, 'taux': 1.0}, 'exact_sans_contexte': {'ok': 368, 'n': 514, 'taux': 0.715953}}, 'exact_contexte': {'ok': 514, 'n': 514, 'taux': 1.0}, 'exact_sans_contexte': {'ok': 369, 'n': 514, 'taux': 0.717899}, 'delta_sans_contexte': 0.001946}
controle {'n_items': 528, 'n': 369, 'exact_attendu_contexte': {'ok': 0, 'n': 369, 'taux': 0.0}, 'exact_donateur_contexte': {'ok': 332, 'n': 369, 'taux': 0.899729}, 'exact_attendu_sans_contexte': {'ok': 0, 'n': 369, 'taux': 0.0}, 'exact_donateur_sans_contexte': {'ok': 313, 'n'
… [229 caractères tronqués]
  ```

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "A10 point d'étape — mesure disponible, fichiers écrits.\n\nCréé : tools/cerveau/multilingue.py (seul module touché pour l'instant).\nSorties : /tmp/a10-multilingue.json (487 Ko) et /tmp/a10-multilingue.md (≈16 Ko), déjà générés.\n\nChi … [1492 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

### 🤖 Assistant

⏵ Adding the test suite for the multilingual measurement

- **write** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_multilingue.py", "content": "from __future__ import annotations\n\nimport json\nimport unittest\n\nfrom cerveau import multilingue as ML\n\n\nclass TestMultilingue(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls):\n  … [12026 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_multilingue.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_multilingue.py", "old_string": "    def test_aucune_langue_inventee(self):\n        meta = self.r[\"meta\"]\n        lexique = set(meta[\"langues_lexique\"] if isinstance(meta[\"langues_lexique\"], list)\n                      els … [1131 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_multilingue.py": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_multilingue.py", "offset": 1, "limit": 55}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_multilingue.py</path>
<type>file</type>
<content>
1: from __future__ import annotations
2: import unittest
3: from cerveau.multilingue import charger_surfaces
4: 
5: 
6: class TestMultilingue(unittest.TestCase):
7:     def test_chargement(self):
8:         surfaces, meta = charger_surfaces()
9:         self.assertEqual(len(surfaces), 528)
10:         self.assertEqual(meta["items"], 528)
11:         self.assertGreaterEqual(meta["langues_corpus"], 60)
12:         self.assertEqual(meta["paires"], 30)
13: 
14:     def test_langues_absentes_declarees(self):
15:         _, meta = charger_surfaces()
16:         for langue in ("ky", "lo", "mt", "si", "yo"):
17:             self.assertIn(langue, meta["langues_absentes_du_corpus"])
18: 
19: 
20: if __name__ == "__main__":
21:     unittest.main()

(End of file - total 21 lines)
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls -la --time-style=full-iso tools/cerveau/multilingue.py tools/cerveau/tests/test_multilingue.py && echo '---' && git status --short | head -20 && echo '---' && wc -l tools/cerveau/multilingue.py tools/cerveau/tests/test_multilingue.py", "description … [42 caractères tronqués]`

  ```
-rw-------. 1 stephane stephane 51224 2026-10-27 12:29:51.367009982 -0400 tools/cerveau/multilingue.py
-rw-------. 1 stephane stephane   723 2026-10-27 12:31:39.119970771 -0400 tools/cerveau/tests/test_multilingue.py
---
 M docs/README.md
 M tools/cerveau/multilingue.py
 M tools/cerveau/neuromodulation.py
 M tools/cerveau/pipeline_semantique_m2.py
?? tools/cerveau/tests/test_multilingue.py
---
 1130 tools/cerveau/multilingue.py
   21 tools/cerveau/tests/test_multilingue.py
 1151 total
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git diff --cached --stat && echo '---' && git ls-files tools/cerveau/multilingue.py tools/cerveau/tests/test_multilingue.py && echo '---' && git diff --stat", "description": "Inspect git index state for new files"}`

  ```
tools/cerveau/multilingue.py            | 117 ++++++++++++++++++++++++++------
 tools/cerveau/tests/test_multilingue.py |  21 ++++++
 2 files changed, 119 insertions(+), 19 deletions(-)
---
tools/cerveau/multilingue.py
tools/cerveau/tests/test_multilingue.py
---
 docs/README.md                          |   2 +-
 tools/cerveau/neuromodulation.py        | 540 ++++++++++++++++++++++++++++++++
 tools/cerveau/pipeline_semantique_m2.py |  30 +-
 3 files changed, 566 insertions(+), 6 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && echo '=== HEAD version ===' && git show HEAD:tools/cerveau/multilingue.py 2>&1 | head -60 && echo '=== INDEX version ===' && git show :tools/cerveau/multilingue.py 2>&1 | head -60", "description": "Inspect HEAD and index versions of multilingue.py"}`

  ```
=== HEAD version ===
#!/usr/bin/env python3
"""multilingue.py — M1 (hub typé) mesuré sur le corpus multilingue réel.

Le module ne remplace aucun codec : il **appelle** `Hub.percevoir` et
`Hub.rendre`, et agrège les résultats par langue, par jeu et par paire. Il
charge les deux corpus réels (`jeux.corpus` = B5/B6, `jeux.corpus_multilingue`
= B7) et vérifie que `semantique.typed_corpus.items()` couvre exactement les
mêmes surfaces.

Ce qui est mesuré (périmètre : les **coups**, seuls items dont le code typé est
complet, comme dans `batterie.m1`) :

- `exact_contexte` : `Hub.percevoir(texte, jeu, contexte)` == `code_rsn(attendu)` ;
- `exact_sans_contexte` : la même lecture avec `contexte=None` ;
- `canonique` : `Hub.rendre(code, contexte)` puis relecture par le codec, le
  corps de la RSN relue doit être celui de l'attendu ;
- `invariance_interlangues` : dans une paire, toutes les variantes **de langue**
  (on exclut l'étiquette `notation`) produisent le même code non nul ;
- `invariance_toutes_variantes` : la même chose en incluant `notation`.

Deux contrôles, qui n'utilisent que le corpus fourni :

1. **Baseline surface** : pour chaque paire, on prédit le code majoritaire des
   *a
… [4466 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git log --oneline -3 && echo '---' && git show --stat --oneline HEAD | head -20 && echo '---' && git diff --cached tools/cerveau/multilingue.py | head -80", "description": "Check recent commits and staged diff"}`

  ```
25830d86 B14 — M2 DANS LA CHAÎNE : 100 % VS 93,4/93,6 %, AUCUN ÉTAGE NE LE CONSOMME ; RAMEAU
db2c2b93 B15 — M1 SUR 66 LANGUES : 528/528, INVARIANCE 26/26 ET 15/15, CONTRÔLE PERMUTÉ 0/90
597cd245 JOURNAL — PASSE COMPLÈTE 47 VERTES, 2 ROUGES STRUCTURELLES ; B13 INTÉGRÉ
---
25830d86 B14 — M2 DANS LA CHAÎNE : 100 % VS 93,4/93,6 %, AUCUN ÉTAGE NE LE CONSOMME ; RAMEAU
 docs/carte.md                                      |     1 +
 docs/en-cours.md                                   |     7 +-
 docs/roadmap.md                                    |     1 +
 journal/2026-10-27.md                              |     5 +-
 journal/2026-10-27_mesures.md                      |     4 +-
 journal/2026-10-27_sprint-24h.md                   |     2 +
 reports/README.md                                  |     1 +
 reports/pipeline-m2.json                           | 10594 +++++++++++++++++++
 reports/rapport-pipeline-m2.md                     |    55 +
 tools/cerveau/pipeline_semantique_m2.py            |   883 ++
 tools/cerveau/tests/test_pipeline_semantique_m2.py |   151 +
 11 files changed, 11698 insertions(+), 6 deletions(-)
---
diff --git a/tools/cerveau/multilingue.py b/tools/cerveau/multilingue.py
… [4365 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls reports/ | grep -i 'b15\\|multiling\\|a10' && echo '---' && grep -rn \"B15\\|A10\" journal/2026-10-27*.md reports/ docs/en-cours.md 2>/dev/null | head -30", "description": "Find B15/A10 report and journal artifacts"}`

  ```
composition-multilingue.json
multilingue.json
pensee-multilingue.json
position-multilingue.json
raisonnement-multilingue-3b.json
rapport-multilingue.md
---
journal/2026-10-27.md:59:| 12:25 | `db2c2b93` | B15 — M1 SUR 66 LANGUES : 528/528, INVARIANCE 26/26 ET 15/15, CONTRÔLE PERMUTÉ 0/90 |
journal/2026-10-27_mesures.md:27:| 12:25 | `db2c2b93` | B15 — M1 SUR 66 LANGUES : 528/528, INVARIANCE 26/26 ET 15/15, CONTRÔLE PERMUTÉ 0/90 | `carte.md`, `en-cours.md`, `roadmap.md` (+7) |
journal/2026-10-27_sprint-24h.md:40:- 12:23 — **B15** mesuré : M1 528/528, 66 langues, invariance 26/26 variantes et 15/15 interlangues avec contexte, 21/26 et 14/15 sans ; contrôle permuté attendu 0 %, donneur 90 % ; baseline surface 71,8 %. Limite : couche lexicale, 5 langues absentes, n=1 pour 5 langues.
reports/README.md:31:| [`rapport-multilingue.md`](rapport-multilingue.md) | **B15** — M1 sur 66 langues : 528/528, invariance 26/26 et 15/15, contrôle permuté 0/90 %, baseline surface 71,8 % |
reports/rapport-multilingue.md:1:# B15 — M1 sur 66 langues : invariance et exactitude
docs/en-cours.md:56:- **B15 multilingue** — M1 sur **66 langues** : **528/528** avec contexte, **70,8 %** sans ; **26/26** variantes 
… [194 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git show --stat --oneline db2c2b93 | head -30 && echo '---' && git show db2c2b93:tools/cerveau/tests/test_multilingue.py 2>&1 | head -40", "description": "Inspect B15 commit and test file"}`

  ```
db2c2b93 B15 — M1 SUR 66 LANGUES : 528/528, INVARIANCE 26/26 ET 15/15, CONTRÔLE PERMUTÉ 0/90
 docs/carte.md                    |     1 +
 docs/en-cours.md                 |     7 +-
 docs/roadmap.md                  |     1 +
 journal/2026-10-27.md            |     5 +-
 journal/2026-10-27_docs.md       |     3 +-
 journal/2026-10-27_sprint-24h.md |     2 +
 reports/README.md                |     1 +
 reports/multilingue.json         | 26630 +++++++++++++++++++++++++++++++++++++
 reports/rapport-multilingue.md   |    63 +
 tools/cerveau/multilingue.py     |  1051 ++
 10 files changed, 27758 insertions(+), 6 deletions(-)
---
fatal: path 'tools/cerveau/tests/test_multilingue.py' exists on disk, but not in 'db2c2b93'
  ```

### 🤖 Assistant

⏵ Replacing the placeholder test with full coverage checks

- **write** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_multilingue.py", "content": "from __future__ import annotations\n\nimport json\nimport unittest\n\nfrom cerveau import multilingue as ML\n\n\nclass TestMultilingue(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls):\n  … [11957 caractères tronqués]`

  ```
Error: cannot write "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_multilingue.py": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_multilingue.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_multilingue.py</path>
<type>file</type>
<content>
1: from __future__ import annotations
2: import unittest
3: from cerveau.multilingue import charger_surfaces
4: 
5: 
6: class TestMultilingue(unittest.TestCase):
7:     def test_chargement(self):
8:         surfaces, meta = charger_surfaces()
9:         self.assertEqual(len(surfaces), 528)
10:         self.assertEqual(meta["items"], 528)
11:         self.assertGreaterEqual(meta["langues_corpus"], 60)
12:         self.assertEqual(meta["sources"]["B5"]["paires"] + meta["sources"]["B7"]["paires"], 30)
13: 
14:     def test_langues_absentes_declarees(self):
15:         _, meta = charger_surfaces()
16:         for langue in ("ky", "lo", "mt", "si", "yo"):
17:             self.assertIn(langue, meta["langues_absentes_du_corpus"])
18: 
19: 
20: if __name__ == "__main__":
21:     unittest.main()

(End of file - total 21 lines)
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && stat -c '%y %s %n' tools/cerveau/tests/test_multilingue.py tools/cerveau/multilingue.py && date -u && ps -eo pid,etimes,cmd | grep -E 'multilingue|unittest|python3' | grep -v grep | head -20", "description": "Check test file mtime and running processe … [3 caractères tronqués]`

  ```
2026-10-27 12:31:39.119970771 -0400 723 tools/cerveau/tests/test_multilingue.py
2026-10-27 12:29:51.367009982 -0400 51224 tools/cerveau/multilingue.py
mar 27 oct 2026 16:33:30 UTC
   1630  141155 /usr/bin/python3.13 /usr/sbin/firewalld --nofork --nopid
   1799  141153 /usr/bin/python3.13 /usr/bin/fail2ban-server -xf start
   2685  141146 /usr/bin/python3 tools/serveur-doc.py --port 8787
3141160      13 bash -c cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 - <<'PY' import json, time from cerveau.neuromodulation import experience_m7_bis t = time.time() r = experience_m7_bis(permutations=30, synthetique=True) r["meta"]["duree_s"] = round(time.time() - t, 2) r["meta"]["commande"] = "PYTHONPATH=tools python3 -c 'experience_m7_bis(permutations=30, synthetique=True)'" with open("/tmp/a11-m7-lfu.json", "w", encoding="utf-8") as f:     json.dump(r, f, ensure_ascii=False, indent=1) print("ecrit /tmp/a11-m7-lfu.json", len(json.dumps(r, ensure_ascii=False)), "octets") print("duree", r["meta"]["duree_s"], "s") print("verdict recence surface", {m: (round(v["moyenne"],5), v["gains"], round(v["p_sign"],4)) for m,v in r["verdict"]["lfu_recence_bat_lfu"]["surface"].items()
… [288 caractères tronqués]
  ```

- **write** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_multilingue.py", "content": "from __future__ import annotations\n\nimport json\nimport unittest\n\nfrom cerveau import multilingue as ML\n\n\nclass TestMultilingue(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls):\n  … [11957 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_multilingue.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools python3 -m unittest tools.cerveau.tests.test_multilingue -v 2>&1 | tail -40", "description": "Run the new multilingual test module"}`

  ```
test_B7_est_le_corpus_multilingue (tools.cerveau.tests.test_multilingue.TestMultilingue.test_B7_est_le_corpus_multilingue) ... ok
test_aucune_langue_inventee (tools.cerveau.tests.test_multilingue.TestMultilingue.test_aucune_langue_inventee) ... ok
test_autocritique_presente (tools.cerveau.tests.test_multilingue.TestMultilingue.test_autocritique_presente) ... ok
test_baseline_exclut_les_paires_uniques_et_sans_paire (tools.cerveau.tests.test_multilingue.TestMultilingue.test_baseline_exclut_les_paires_uniques_et_sans_paire) ... ok
test_baseline_surface (tools.cerveau.tests.test_multilingue.TestMultilingue.test_baseline_surface) ... ok
test_controle_surface_permutee (tools.cerveau.tests.test_multilingue.TestMultilingue.test_controle_surface_permutee) ... ok
test_duree_cpu (tools.cerveau.tests.test_multilingue.TestMultilingue.test_duree_cpu) ... ok
test_invariance_interlangues (tools.cerveau.tests.test_multilingue.TestMultilingue.test_invariance_interlangues) ... ok
test_invariance_paire_par_paire (tools.cerveau.tests.test_multilingue.TestMultilingue.test_invariance_paire_par_paire) ... ok
test_invariance_toutes_variantes (tools.cerveau.tests.test_multilingue.TestMultilingue.test_invari
… [1265 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Running the full cerveau test discovery

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -30", "description": "Run all cerveau tests"}`

  ```
.............................................................................sssssssssss...........................ssssssss
----------------------------------------------------------------------
Ran 123 tests in 11.319s

OK (skipped=19)
[stderr]

real	0m11,493s
user	0m11,461s
sys	0m0,035s
  ```

- **bash** `{"command": "grep -n \"Sur B7 seul\" /tmp/a10-multilingue.md | head -3 && echo '---' && ls -la --time-style=full-iso /tmp/a10-multilingue.* && echo '---' && head -20 /tmp/a10-multilingue.md", "description": "Verify final reports include latest fixes"}`

  ```
10:- **Sans contexte** : **374 / 528 (70,8 %)** ; c'est là que se voient les dépendances au contexte (go, morpion, notations courtes). Sur B7 seul : 331 / 449 (73,7 %).
11:- **Invariance interlangues** : **15 / 15 (100,0 %)** des paires avec contexte et **14 / 15** sans contexte. **Sur B7 seul** : 11 / 11 (100,0 %) avec contexte et 11 / 11 (100,0 %) sans contexte. L'unique échec sans contexte est B5 `echecs-nf3` (`Cf3`, notation française courte qui a besoin du contexte).
---
-rw-r--r--. 1 stephane stephane 486559 2026-10-27 12:30:03.509058293 -0400 /tmp/a10-multilingue.json
-rw-r--r--. 1 stephane stephane  18526 2026-10-27 12:30:03.511141483 -0400 /tmp/a10-multilingue.md
---
# A10 — M1 (hub typé) sur le corpus multilingue

**Date** : 2026-10-27T16:30:00+00:00  
**Périmètre** : coups (mêmes items que batterie.m1), 528 surfaces, 66 langues réelles.  
**Source de mesure** : `tools/cerveau/hub.py` (`Hub.percevoir`, `Hub.rendre`), sans modification des modules existants.

## Verdict

- **Avec contexte** : M1 lit **528 / 528 (100,0 %)** et le canonique revient à **528 / 528 (100,0 %)**.
- **Sans contexte** : **374 / 528 (70,8 %)** ; c'est là que se voient les dépendances au contexte (go
… [1276 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 tools/cerveau/multilingue.py --sans-controle --json /tmp/a10-sans-controle.json --md /tmp/a10-sans-controle.md && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/a10-sans-controle.json'))\nprint('sans controle OK, cles  … [197 caractères tronqués]`

  ```
A10 — M1 multilingue : 528 items, exact ctx 100,0 %, sans ctx 70,8 %, invariance interlangues 100,0 %
JSON : /tmp/a10-sans-controle.json
MD   : /tmp/a10-sans-controle.md
sans controle OK, cles controle presentes ? False
n 528 exact 1.0
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && stat -c '%y %s %n' tools/cerveau/tests/test_multilingue.py tools/cerveau/multilingue.py && PYTHONPATH=tools python3 -m unittest tools.cerveau.tests.test_multilingue 2>&1 | tail -5", "description": "Confirm final test file and rerun it"}`

  ```
2026-10-27 12:34:09.960038883 -0400 11342 tools/cerveau/tests/test_multilingue.py
2026-10-27 12:29:51.367009982 -0400 51224 tools/cerveau/multilingue.py
....................
----------------------------------------------------------------------
Ran 20 tests in 3.288s

OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,120p' reports/rapport-multilingue.md", "description": "Read integrated B15 report for consistency"}`

  ```
# B15 — M1 sur 66 langues : invariance et exactitude

> **Objet.** Mesurer le codec M1 sur le corpus multilingue existant, par langue et par jeu, avec
> une baseline de surface et un contrôle de surface permutée. **Couche lexicale** : les surfaces
> B7 sont « libellé + coordonnée » ; la réussite mesure la reconnaissance lexicale, pas la
> compréhension d'une phrase libre.

## Corpus

| source | coups | langues | paires |
|---|---:|---:|---:|
| B5 | 79 | 2 (en, fr) + notation | 19 |
| B7 | 449 | 66 | 11 |
| total | **528** | **66** | **30** |

- **71 langues** au lexique, **66** présentes dans le corpus ; absentes : **ky, lo, mt, si, yo**.
- **26 paires multi-variantes**, **15 paires interlangues**.
- 5 langues à **n=1** (am, km, pa, so, zu) : un taux de 0 ou 100 % sur un seul item n'est pas une estimation.

## Résultats globaux

| mesure | valeur |
|---|---:|
| exact avec contexte | **528 / 528 = 100 %** |
| exact sans contexte | **374 / 528 = 70,8 %** |
| canonique | **528 / 528 = 100 %** |
| invariance toutes variantes (contexte) | **26 / 26 = 100 %** |
| invariance interlangues (contexte) | **15 / 15 = 100 %** |
| invariance toutes variantes (sans contexte) | **21 / 26 = 80,8 %*
… [1615 caractères tronqués]
  ```

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "A10 TERMINÉ — module + tests + rapports.\n\nFichiers créés (seuls fichiers que j'ai écrits) :\n- tools/cerveau/multilingue.py (1130 lignes) : charge B5/B7/typed_corpus, mesure M1 par langue, par jeu, par paire, baseline surface LOO, co … [2361 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

- **present** `{"files": [{"path": "/tmp/a10-multilingue.md", "description": "Rapport A10 — M1 sur le corpus multilingue : résultats par langue, par jeu et par paire, baseline surface et contrôle permuté."}, {"path": "/tmp/a10-multilingue.json", "description": "JSON complet A10 : métadonnées de sources, agrégats,  … [41 caractères tronqués]`

  ```
Presented /tmp/a10-multilingue.md
Presented /tmp/a10-multilingue.json
  ```

### 🤖 Assistant

⏵ Closing with the summary, results, and file paths

Travail terminé. J’ai créé uniquement les deux fichiers demandés, sans toucher aux modules, docs, reports, journal, `batterie.py` ni à git en écriture.

## Fichiers

- Code : [`tools/cerveau/multilingue.py`](/home/stephane/GitHub/Qtrinet/tools/cerveau/multilingue.py)
- Tests : [`tools/cerveau/tests/test_multilingue.py`](/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_multilingue.py)
- Rapport : [`/tmp/a10-multilingue.md`](/tmp/a10-multilingue.md)
- JSON : [`/tmp/a10-multilingue.json`](/tmp/a10-multilingue.json)

## Résumé mesuré

Périmètre : 528 coups B5+B7, 66 langues réelles, 30 paires.

| mesure | valeur |
|---|---|
| exact avec contexte | **528 / 528 (100 %)** |
| exact sans contexte | **374 / 528 (70,8 %)** |
| canonique | **528 / 528 (100 %)** |
| invariance interlangues, contexte | **15 / 15 (100 %)** |
| invariance interlangues, sans contexte | **14 / 15 (93,3 %)** |
| invariance toutes variantes, contexte | **26 / 26 (100 %)** |
| invariance toutes variantes, sans contexte | **21 / 26 (80,8 %)** |

**B7 seul** (449 surfaces, 66 langues, 11 paires) : 449/449 avec contexte, 331/449 sans (73,7 %), canonique 449/449, invariance interlangues **11/11 dans les deux conditions**. L’unique échec global sans contexte est B5 `echecs-nf3` (`Cf3`, SAN français court qui exige la position) — B7 reste donc à 100 %.

**Baseline surface** (code majoritaire des autres surfaces de la paire, leave-one-out) : 514/514 avec contexte, 369/514 (71,8 %) sans, contre M1 368/514 (71,6 %) sur le même périmètre : **+1 item seulement**, avec −4,8 pt sur le morpion et +2,8 pt sur les échecs.

**Contrôle surface permutée stricte** : 369 items appariés, exact attendu **0/369**, exact donneur **332/369 (90,0 %)** ; B7 **298/300 (99,3 %)** ; variante large 518 items, donneur 423/518 (81,7 %).

**Invariance ≠ exactitude** : sans contexte, les paires B7 go (62 langues) et morpion (42 langues) restent invariantes avec un code faux (exact 0 %).

## Langues

71 langues au lexique, **66 présentes** dans le corpus ; absentes déclarées : **ky, lo, mt, si, yo**. Cinq langues à n=1 : am, km, pa, so, zu.

## Tests

- `PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools` → **123 tests OK, 19 skip**.
- Mon module seul : **20 tests OK en 3,3 s**.

## Limites (dans le rapport)

Corpus construit par le code (attendus et contextes issus des mêmes règles que le codec), couche lexicale seulement, pas d’intervalle de confiance, étiquette de langue non détectée par M1, et `exact_attendu = 0` partiellement mécanique dans le contrôle strict — le signal utile y est le **99,3 % de récupération du donneur en B7**.

Note : un autre thread a déjà committé une version antérieure de ce module sous B15 ; la version courante ajoute la **table par langue**, la **table par source** et les corrections de notes. Le `.md` de `/tmp` est à jour.

