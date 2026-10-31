# Session DSH — relecture

- identifiant : `56f3ba0f-66b3-4728-a4cd-201951538ed1`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 10:30:52
- agent : standard


## Tour 1

### 👤 Utilisateur

Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A7 : améliorer M8 (sommeil/consolidation) et M9 (lésions), après les négatifs A2.

État A2 :
- M8 `sommeil.py` : 96,48 % de champs, exact 65,1 %, baseline par jeu 96,10 %, 0 % exact sur codes jamais vus ; prototypes par (jeu, action).
- M9 `lesion.py` : `batterie_lesions()` CPU, sham nul, M2 proxy bayésien.
- Corpus : `semantique.typed_corpus.items`, `cerveau.episodique.py`, `cerveau/sequences.py`.
- Tests : `PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest discover -s tools/cerveau/tests -t tools`.

Objectif :
M8 : tester des prototypes **conditionnés par le contexte** (jeu, action, type de coup) et/ou **prototype + épisode** ; split par code tenu à l'écart ; mesure exact/champs/non nuls, baseline par jeu et par paire ; 3 graines. Si le gain n'est que la marginale, documente le négatif.
M9 : utiliser le **vrai `voies.py`** (pas le proxy bayésien) pour les lésions M2, si le GPU/CPU le permet ; sinon documenter pourquoi le proxy suffit. Vérifie que `lesion.batterie_lesions()` reste cohérent avec `batterie.py` et que les déficits sont bien `intacte - lésée` (pas `1 - lésée`).
- Écris `/tmp/a7-m8-m9.json` et `.md` ; code seulement `sommeil.py`, `lesion.py`, tests associés.
- Ne touche pas à `batterie.py`, docs, reports, journal, git. Pas de commit.
- GPU `CUDA_VISIBLE_DEVICES=0` si nécessaire, sinon CPU. Sois autonome, timebox, autocritique. Réponds avec un résumé et les chemins.
Your parent agent id is "f0969e87-af0c-43b1-93cf-f278d9c90846". Before you finish, send your result to that agent with send_message({ agent_id: "f0969e87-af0c-43b1-93cf-f278d9c90846", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

# Directives de l'agent — Drave

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs
> unifiés (**49 portes, 8 chapitres, 173 fichiers / 242 JSON, 52 documents**), chemins archivés
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

## 4. Le minimum avant de conclure

- l'état est à jour dans [`docs/en-cours.md`](docs/en-cours.md) (synthèse, chantiers, questions en attente) ;
- la **roadmap** est à jour : le chantier fini y est marqué, le suivant est désigné ;
- la fiche est dans `reports/`, le récit dans `journal/`, le commit porte le chiffre ;
- les portes sont vertes, **hors les deux rouges structurelles connues** ;
- la revue de documentation passe, et les liens résolvent.

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

⏵ Cartographie du dépôt et lecture des fichiers M8/M9 existants

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls && echo \"---\" && ls tools/cerveau/ && echo \"---\" && ls tools/cerveau/tests | head -50", "description": "List repo and cerveau structure"}`

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
predictif.py
__pycache__
sequences.py
sommeil.py
tests
voies.py
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
test_predictif.py
test_sommeil.py
test_voies.py
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && wc -l tools/cerveau/sommeil.py tools/cerveau/lesion.py tools/cerveau/voies.py tools/cerveau/batterie.py tools/cerveau/episodique.py tools/cerveau/sequences.py 2>&1", "description": "Line counts of key files"}`

  ```
388 tools/cerveau/sommeil.py
  523 tools/cerveau/lesion.py
  426 tools/cerveau/voies.py
  225 tools/cerveau/batterie.py
   90 tools/cerveau/episodique.py
  114 tools/cerveau/sequences.py
 1766 total
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """M8 — sommeil : consolider des épisodes en prototypes, et mesurer ce que cela vaut.
3: 
4: Le module d'origine groupait par ``(jeu, action)`` et prenait le mode **champ par
5: champ**. Le score publié, 96,48 % sur 106 épisodes de test, est réel mais il est
6: mal lu :
7: 
8: - les champs sont **dominés par ``None``** : 12 des 15 champs ont plus de 98 %
9:   d'exactitude agrégée parce que la bonne réponse y est presque toujours
10:   ``None``. Sur les valeurs non nulles, la précision tombe à ~84 % sur tout le
11:   corpus (~86 % sur la queue), et les trois champs porteurs (``de``, ``vers``,
12:   ``carte``) sont à ~50 %, ~50 % et ~22–28 % conditionnellement.
13: - le score **exact** n'est pas 0 % : il vaut 65,1 % sur la queue, 24,1 % sur les
14:   29 codes uniques. La « baseline 0,0 » du rapport était l'absence de mémoire,
15:   pas un prédicteur.
16: - groupé par ``(jeu)`` seul, le prototype fait déjà 96,10 % : le groupe
17:   ``(jeu, action)`` n'ajoute que +0,38 point. Le score vient du jeu, pas de
18:   l'action.
19: - sur des **codes jamais vus**, le pro
… [17793 caractères tronqués]
  ```


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
13: - **M2** : couper la voie ventrale (action) ou dorsale (``de``) ; sur CPU, un
14:   substitut déterministe à deux têtes (bayes naïf sur n-grammes) est déclaré,
15:   avec la même double dissociation structurelle que ``voies.py`` ;
16: - **M3** : capacité du tampon (0, 1, 2, 4, 8, 12), dose-réponse ;
17: - **M4** : stockage vide, puis lésion du champ d'adressage (le champ est mis à
18:   ``None`` dans la requête) ;
19: - **M5** : retirer les transitions, l'ordre 2 ou le repli majoritaire ; contrôle
20:   positif sur une chaîne de Markov synthé
… [23833 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/batterie.py"}`

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
… [19365 caractères tronqués]
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

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls /tmp/natif-600-512-8-align-s1 2>&1 | head; echo \"---\"; nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv 2>&1 | head; echo \"---\"; /home/stephane/gpu-env/bin/python -c \"import torch;print(torch.__version__, torch.cuda.is_availab … [70 caractères tronqués]`

  ```
config.json
generation_config.json
model.safetensors
---
name, memory.total [MiB], memory.used [MiB]
Quadro RTX 5000, 16384 MiB, 832 MiB
Quadro RTX 5000, 16384 MiB, 4 MiB
---
2.11.0+cu130 True
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """M4 — mémoire épisodique adressable par contenu.
3: 
4: Chaque épisode est (surface, code, langue, paire). La clé est le one-hot du code
5: typé ; la lecture est un plus proche voisin. On mesure le rappel exact, la
6: complétion sur un code partiel et la séparation de codes voisins.
7: """
8: from __future__ import annotations
9: 
10: import math
11: from dataclasses import dataclass, field
12: 
13: from semantique.universaux import CHAMPS, vecteur
14: 
15: 
16: @dataclass
17: class Episode:
18:     surface: str
19:     code: dict
20:     langue: str = "?"
21:     paire: str = ""
22:     poids: float = 1.0
23:     meta: dict = field(default_factory=dict)
24: 
25: 
26: class Episodique:
27:     nom = "M4-episodique"
28: 
29:     def __init__(self) -> None:
30:         self.episodes: list[Episode] = []
31: 
32:     def stocker(self, surface: str, code: dict, langue: str = "?", paire: str = "",
33:                 poids: float = 1.0) -> None:
34:         self.episodes.append(Episode(surface, dict(code), langue, paire, poids))
35: 
36:     def _cle(self, cod
… [2622 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,200p tools/semantique/typed_corpus.py", "description": "Read typed_corpus head"}`

  ```
#!/usr/bin/env python3
"""typed_corpus.py — les surfaces de jeux avec leur code typé fixe.

La source est le corpus B5/B6 (112 items, formats canoniques) et le corpus
multilingue B7 (449 surfaces, 66 langues). On ne garde que les **coups** : ce
sont les items dont le code typé est complet (source, cible, matériel).
Le découpage se fait **par paire** : les surfaces d'un même sens restent du même
côté ; aucune langue d'une paire de validation n'est vue à l'entraînement.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

from jeux.corpus import construire_corpus
from jeux.corpus_multilingue import construire_corpus_multilingue
from semantique.universaux import code_item, resume_contexte


@dataclass(frozen=True)
class ItemType:
    texte: str
    code: dict
    jeu: str
    nature: str
    langue: str
    paire: str
    format: str
    contexte: str = ""


def items() -> list[ItemType]:
    out = []
    vus = set()
    for corpus in (construire_corpus(), construire_corpus_multilingue()):
        for it in corpus.items:
            if it.attendu.nature != "coup":
                continue
            cle = (it.texte, it.jeu, it.paire, it.langue)
   
… [1933 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,160p tools/semantique/universaux.py", "description": "Read universaux"}`

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
… [4375 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat tools/cerveau/tests/test_sommeil.py && echo \"=====\" && cat tools/cerveau/tests/test_lesion.py", "description": "Read tests for sommeil and lesion"}`

  ```
from __future__ import annotations

import unittest
from types import SimpleNamespace

from cerveau.sommeil import Sommeil, experience_m8


def _it(code, texte="x", paire="p", jeu="echecs"):
    return SimpleNamespace(code=code, texte=texte, paire=paire, jeu=jeu)


CODE_A = {"jeu": "echecs", "action": "deplacer", "de": 62, "vers": 45}
CODE_B = {"jeu": "echecs", "action": "deplacer", "de": 52, "vers": 36}
CODE_C = {"jeu": "dames", "action": "prendre", "chemin_0": 8, "chemin_1": 13}


class TestSommeil(unittest.TestCase):
    def test_consolider_et_evaluer(self):
        train = [_it(CODE_A, "Nf3"), _it(CODE_A, "g1f3"), _it(CODE_B, "e3")]
        s = Sommeil()
        protos = s.consolider(train)
        self.assertEqual(len(protos), 1)
        self.assertEqual(protos[("echecs", "deplacer")]["de"], 62)
        r = s.evaluer([_it(CODE_A), _it(CODE_B)], protos)
        self.assertEqual(r["n"], 2)
        self.assertGreater(r["champs"], 0.5)
        self.assertTrue(0.0 <= r["exact"] <= 1.0)

    def test_baselines(self):
        train = [_it(CODE_A, "a"), _it(CODE_A, "b"), _it(CODE_B, "c")]
        test = [_it(CODE_A, "d")]
        b = Sommeil().baselines(train, test)
        self.asser
… [4101 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nfrom semantique.typed_corpus import items\nimport collections\nits=items()\nprint('n',len(its))\nprint(collections.Counter(i.jeu for i in its))\nprint('paires',len({i.paire for i in its}))\npri … [202 caractères tronqués]`

  ```
n 528
Counter({'cartes': 161, 'echecs': 146, 'go': 87, 'dames': 70, 'morpion': 64})
paires 31
codes uniques 29
n contextes 0.7102272727272727
ItemType(texte='A1', code={'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 0, 'symbole': 'X', 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}, jeu='morpion', nature='coup', langue='fr', paire='morpion-a1', format='cellule', contexte='morpion etat trait=X taille=3 cases=.,.,.,.,.,.,.,.,.')
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"natif-600-512-8-align\" --include=*.py --include=*.sh --include=*.md . | head -20", "description": "Find base model provenance"}`

  ```
./tools/semantique/entrainer.py:14:    python3 tools/semantique/entrainer.py --checkpoint /tmp/natif-600-512-8-align-s1 \
./tools/semantique/entrainer.py:156:    ap.add_argument("--checkpoint", default="/tmp/natif-600-512-8-align-s1")
./tools/semantique/entrainer_nvlink.py:83:    ap.add_argument("--checkpoint", default="/tmp/natif-600-512-8-align-s1")
./tools/semantique/diagnostic.py:28:    ap.add_argument("--checkpoint", default="/tmp/natif-600-512-8-align-s1")
./tools/semantique/entrainer_type.py:132:    ap.add_argument("--checkpoint", default="/tmp/natif-600-512-8-align-s1")
./tools/cerveau/batterie.py:77:    base = AutoModelForCausalLM.from_pretrained("/tmp/natif-600-512-8-align-s1", dtype=torch.float32)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,120p tools/semantique/synth_corpus.py 2>/dev/null; echo \"===\"; ls tools/semantique/", "description": "Inspect synth corpus module"}`

  ```
#!/usr/bin/env python3
"""synth_corpus.py — des surfaces synthétiques multilingues, labels RSN exacts.

Le codec classique est le professeur : on génère des surfaces à partir des
règles (coups légaux, cartes, points) et des libellés multilingues, puis on
entraîne le natif à lire ces surfaces. Les surfaces **réelles** B5/B7 ne sont
jamais utilisées à l'entraînement : elles servent de test de transfert.
"""
from __future__ import annotations

from dataclasses import dataclass

from jeux.lexique_multilingue import MULTI
from jeux.regles import cartes as C
from jeux.regles import dames as D
from jeux.regles import echecs as E
from jeux.regles import go as G
from jeux.regles import morpion as M
from jeux.rsn import RSN
from semantique.typed_corpus import ItemType
from semantique.universaux import code_rsn, resume_contexte

PIECES = ("P", "N", "B", "R", "Q", "K")
LETTRES_DAMES = "abcdefgh"


def _forme(concept: str, langue: str) -> str | None:
    f = MULTI.formes(concept, langue)
    return f[0] if f else None


def _item(texte: str, r: RSN, langue: str, paire: str, fmt: str = "synthetique",
          contexte: str = "") -> ItemType:
    return ItemType(texte, code_rsn(r), r.jeu, r.natu
… [3702 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls tools/semantique/tests && grep -rn \"Voies\\|voies\" tools/semantique/tests tools/cerveau/tests | head -20", "description": "Look for voies tests"}`

  ```
__init__.py
__pycache__
test_corpus.py
test_normalisation.py
test_typed_corpus.py
test_universaux.py
tools/cerveau/tests/test_voies.py:16:    from cerveau.voies import Voies, entrainer, evaluer, evaluer_champs
tools/cerveau/tests/test_voies.py:52:class TestVoies(unittest.TestCase):
tools/cerveau/tests/test_voies.py:54:        m = Voies(_Base(16), champs_dorsaux=("de", "vers", "point"),
tools/cerveau/tests/test_voies.py:69:        m = Voies(_Base(16), champs_dorsaux=("de",), pool="mean")
tools/cerveau/tests/test_voies.py:71:        m = Voies(_Base(16), champs_dorsaux=("de",), pool="last")
tools/cerveau/tests/test_voies.py:73:        m = Voies(_Base(16), champs_dorsaux=("de",), pool="mean+last",
tools/cerveau/tests/test_voies.py:78:        m = Voies(_Base(16), champs_dorsaux=("de",), pool="mean+last",
tools/cerveau/tests/test_voies.py:89:        m = Voies(_Base(16), champs_dorsaux=("de", "vers", "point", "chemin_0"),
tools/cerveau/tests/test_voies.py:109:        m = Voies(_Base(16), champs_dorsaux=("de",), pool="mean+last",
[stderr]
grep: tools/cerveau/tests/__pycache__/test_voies.cpython-313.pyc: binary file matches
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import items_synth\nits=items(); syn=items_synth()\nfor champ in ('de','vers','point','chemin_0','carte','case'):\n    pr … [233 caractères tronqués]`

  ```
de 146
vers 146
point 70
chemin_0 70
carte 161
case 64
syn 16662
Counter({'go': 10106, 'echecs': 3660, 'morpion': 2034, 'cartes': 470, 'dames': 392})
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_voies.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_voies.py</path>
<type>file</type>
<content>
1: from __future__ import annotations
2: 
3: import unittest
4: from types import SimpleNamespace
5: 
6: try:
7:     import torch
8:     import torch.nn as nn
9:     _TORCH = True
10: except ImportError:
11:     torch = None
12:     nn = None
13:     _TORCH = False
14: 
15: if _TORCH:
16:     from cerveau.voies import Voies, entrainer, evaluer, evaluer_champs
17: from semantique.typed_corpus import ItemType
18: 
19: 
20: if _TORCH:
21:     class _Base(nn.Module):
22:         """Encodeur minimal : assez pour tester les formes, pas pour apprendre."""
23: 
24:         def __init__(self, d: int = 16, vocab: int = 256):
25:             super().__init__()
26:             self.config = SimpleNamespace(hidden_size=d)
27:             self.emb = nn.Embedding(vocab, d)
28: 
29:         def forward(self, input_ids, attention_mask, output_hidden_states=True):
30:             h = self.emb(input_ids)
31:             return SimpleNamespace(hidden_states=[h, h])
32: else:
33:     _Base = object
34: 
35: 
36: def _items():
37:     base = {"jeu": "echecs", "action": "deplacer", "de": None, "vers":
… [4699 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nimport time, torch\nt0=time.time()\nfrom transformers import AutoModelForCausalLM\nbase=AutoModelForCausalLM.from_pretrained('/tmp/natif-600-512-8-align-s1', dtype=torch.float32)\nprint('load', … [480 caractères tronqués]`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1114.50it/s]
load 5.261458158493042 31.630848
train 25.00459575653076 146
{'action': 0.9863013698630136, 'de': 0.9315068493150684, 'n': 146}
{'action': 0.1232876712328767, 'de': 0.9315068493150684, 'n': 146}
{'action': 0.9863013698630136, 'de': 0.02054794520547945, 'n': 146}
eval 0.6966683864593506
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nfrom semantique.typed_corpus import items\nimport collections\nits=items()\npar_code=collections.defaultdict(list); par_paire=collections.defaultdict(list)\nfor i in its:\n    k=tuple(sorted(i. … [429 caractères tronqués]`

  ```
codes 29 paires 31
55 3 ['morpion'] jouer_case ['case', 'symbole'] {None, 'morpion-a1', 'ml-morpion-a1'}
6 1 ['morpion'] jouer_case ['case', 'symbole'] {'morpion-centre'}
2 1 ['morpion'] jouer_case ['case', 'symbole'] {'morpion-o-bas-droite'}
1 1 ['morpion'] jouer_case ['case', 'symbole'] {None}
69 3 ['echecs'] deplacer ['de', 'vers'] {'echecs-e4', None, 'ml-echecs-e4'}
68 3 ['echecs'] deplacer ['de', 'vers'] {None, 'echecs-nf3', 'ml-echecs-nf3'}
2 1 ['echecs'] deplacer ['de', 'roque', 'vers'] {'echecs-petit-roque'}
2 1 ['echecs'] deplacer ['de', 'roque', 'vers'] {'echecs-grand-roque'}
1 1 ['echecs'] deplacer ['de', 'vers'] {'echecs-ep'}
2 1 ['echecs'] promouvoir ['de', 'promotion', 'vers'] {'echecs-promotion'}
1 1 ['echecs'] deplacer ['de', 'vers'] {None}
1 1 ['echecs'] deplacer ['de', 'vers'] {None}
4 1 ['dames'] prendre ['chemin_0', 'chemin_1'] {'dames-prise-simple'}
3 1 ['dames'] prendre ['chemin_0', 'chemin_1', 'chemin_2'] {'dames-prise-multiple'}
2 2 ['dames'] prendre ['chemin_0', 'chemin_1'] {None, 'dames-simple'}
59 2 ['dames'] prendre ['chemin_0', 'chemin_1'] {'dames-simple-c5', 'ml-dames-b6c5'}
1 1 ['dames'] prendre ['chemin_0', 'chemin_1'] {'dames-blanc'}
1 1 ['dames'] p
… [650 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de l'état de base (tests, temps, cohérence des déficits)

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -15", "description": "Run baseline cerveau test suite", "run_in_background": true}`

  ```
started background job bash-1711
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nfrom cerveau.predictif import Predictif\nimport inspect\nprint(inspect.getsource(Predictif.evaluer))\n\" 2>&1 | head -60", "description": "Read Predictif.evaluer"}`

  ```
def evaluer(self, sequences) -> dict:
        """Exactitude, baseline majoritaire, surprisal et n sur des séquences.

        Ne prédit que les pas 1..n-1 : le premier pas n'a pas de passé. Les pas
        dont la cible est absente (source d'un go) sont ignorés.
        """
        n = ok = base = hors_vocab = 0
        surprise: list[float] = []
        surprise_base: list[float] = []
        for seq in sequences:
            pas = seq.pas
            for i in range(1, len(pas)):
                b = pas[i]
                y = valeur(b, self.cible)
                cur = valeur(pas[i - 1], self.cible)
                if y is None or cur is None:
                    continue
                jeu = b.jeu
                precedent = valeur(pas[i - 2], self.cible) if i >= 2 else None
                dist = self.distribution(jeu, cur, precedent)
                if not dist:
                    continue
                if y not in dist:
                    # valeur de test jamais vue à l'entraînement : hors vocabulaire
                    hors_vocab += 1
                    continue
                n += 1
                ok += int(max(dist, key=dist.get) == y)
                surprise.appe
… [1090 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nimport json\nfrom cerveau.lesion import _m1, _m6\nfrom semantique.typed_corpus import items\nr1=_m1(); print('M1', json.dumps(r1, default=str)[:400])\nr6=_m6(items()); print('M6', json.dum … [91 caractères tronqués]`

  ```
M1 {"lesion": "retirer le contexte (percevoir sans contexte)", "intacte": {"exact": 1.0}, "lessee": {"exact": 0.7083333333333334}, "deficit": {"exact": 0.29166666666666663, "relatif": 0.29166666666666663}, "n": 528, "statut": "mesure", "controle_sham": 0.0, "note": "le codec lit la surface ; le contexte l\u00e8ve l'ambigu\u00eft\u00e9"}
M6 {"lesion": "retirer la conjonction (un seul canal), tout accepter, tout refuser", "intacte": {"exact": 0.9431818181818182, "n": 88, "faux_positifs": 0, "faux_negatifs": 5, "taux_base_tout_non": 0.75}, "lessee": {"canal_langue": 0.75, "canal_sens": 0.75, "tout_non": 0.75, "tout_accepter": 0.25}, "deficit": {"canal_langue": 0.19318181818181823, "canal_sens": 0.19318181818181823, "tout_non": 0.19318181818181823, "tout_accepter": 0.6931818181818182}, "n": 88, "statut": "mesure", "controle_sham": 0.0
[stderr]

real	0m1,355s
user	0m1,334s
sys	0m0,022s
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"def experience_m7\" -A 80 tools/cerveau/neuromodulation.py | head -100", "description": "Inspect M7 deltas convention"}`

  ```
382:def experience_m7(episodes: list[EpisodeM7] | None = None,
383-                  permutations: int = 30, capacite: int = 16,
384-                  graine: int = 0, synthetique: bool = True) -> dict:
385-    """Compare les politiques de rétention sur le même flux, appariées.
386-
387-    Le suffixe est le dernier 20 % du flux ; la mémoire est gelée à la fin du
388-    préfixe. Les deltas sont ``politique - fifo`` par permutation (même ordre,
389-    même capacité), avec le taux de gains et un IC 95 % normal.
390-    """
391-    ep = episodes if episodes is not None else preparer_flux()
392-    n = len(ep)
393-    prefixe = int(n * 0.8)
394-    configs = _configurations()
395-    resultats: dict[str, dict[str, list[float]]] = {
396-        c["nom"]: collections.defaultdict(list) for c in configs}
397-    oracle = collections.defaultdict(list)
398-    for k in range(permutations):
399-        ordre = list(range(n))
400-        random.Random(graine + k).shuffle(ordre)
401-        for c in configs:
402-            m = _tourner(ep, ordre, prefixe, c["politique"], capacite,
403-                         c["cle"], graine + k, c["sans"])
404-            for nom in _METRIQUES:
405-       
… [3122 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"1\\.0 *-\\|1 *-\" tools/cerveau/lesion.py", "description": "Grep for 1-minus patterns in lesion.py"}`

  ```
282:                       "deficit": 1.0 - ok / len(presents)}
  ```

- **job_output** `{"job_id": "bash-1711"}`

  ```
................................................................
----------------------------------------------------------------------
Ran 64 tests in 5.516s

OK
[stderr]

real	0m14,502s
user	0m15,563s
sys	0m1,110s
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-1711 (bash: cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -15) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport collections, random\nfrom semantique.typed_corpus import items\nfrom cerveau.sommeil import Sommeil, _code, _signature\nits=items(); s=Sommeil()\n# surface duplicates\npar_txt=collec … [1303 caractères tronqués]`

  ```
surfaces totales 439 surfaces multi-codes 0
textes uniques 439
modal mass global 0.0
modal mass jeu 0.0
modal mass groupe 0.0
modal mass type 0.0
  ```

- **bash** `{"command": "cat > /tmp/a7_explore.py <<'EOF'\nimport collections, random, statistics, sys\nsys.path.insert(0,'tools')\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import CHAMPS\nfrom cerveau.sommeil import Sommeil, _code, _cle, _signature, _mode_champs\nNOMS=tuple(n for n, … [3864 caractères tronqués]`

  ```
LOO codes=29
global       champs=0.7494  non_nuls=0.0460
jeu          champs=0.8920  non_nuls=0.6126
groupe       champs=0.8920  non_nuls=0.5971
type         champs=0.8897  non_nuls=0.5902
jeu_type     champs=0.8897  non_nuls=0.5902
action_type  champs=0.8897  non_nuls=0.5902
type_seul    champs=0.8897  non_nuls=0.5902
ladder sup3  champs=0.8920  non_nuls=0.6126
exemple fields {'jeu': 1, 'action': 1, 'de': 1, 'vers': 1}
champs non nuls par code Counter({4: 18, 3: 7, 5: 4})
  ```

### 👤 Utilisateur

Agent f0969e87-af0c-43b1-93cf-f278d9c90846 sent a message: 
Timebox : donne un point maintenant et écris /tmp/a7-m8-m9.json/.md dès que possible, même partiel. Termine ensuite ; un négatif net suffit.

### 🤖 Assistant

⏵ Point d'étape au parent + premiers fichiers partiels

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat > /tmp/a7_fields.py <<'EOF'\nimport collections, sys, json\nsys.path.insert(0,'tools')\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import CHAMPS\nfrom cerveau.sommeil import Sommeil, _code, _signature, _mode_champs\nNOMS … [1240 caractères tronqués]`

  ```
{
 "jeu": {
  "jeu": {
   "n": 29,
   "acc": 1.0
  },
  "action": {
   "n": 29,
   "acc": 0.896551724137931
  },
  "de": {
   "n": 8,
   "acc": 0.125
  },
  "vers": {
   "n": 8,
   "acc": 0.0
  },
  "roque": {
   "n": 2,
   "acc": 0.0
  },
  "carte": {
   "n": 7,
   "acc": 0.0
  },
  "case": {
   "n": 4,
   "acc": 0.0
  },
  "symbole": {
   "n": 4,
   "acc": 0.75
  },
  "taille": {
   "n": 4,
   "acc": 1.0
  },
  "passe": {
   "n": 1,
   "acc": 0.0
  },
  "point": {
   "n": 3,
   "acc": 0.0
  },
  "chemin_0": {
   "n": 6,
   "acc": 0.6666666666666666
  },
  "chemin_1": {
   "n": 6,
   "acc": 0.16666666666666666
  },
  "chemin_2": {
   "n": 1,
   "acc": 0.0
  },
  "promotion": {
   "n": 1,
   "acc": 0.0
  }
 },
 "groupe": {
  "jeu": {
   "n": 29,
   "acc": 0.9310344827586207
  },
  "action": {
   "n": 29,
   "acc": 0.9310344827586207
  },
  "de": {
   "n": 8,
   "acc": 0.125
  },
  "vers": {
   "n": 8,
   "acc": 0.0
  },
  "roque": {
   "n": 2,
   "acc": 0.0
  },
  "carte": {
   "n": 7,
   "acc": 0.0
  },
  "case": {
   "n": 4,
   "acc": 0.0
  },
  "symbole": {
   "n": 4,
   "acc": 0.75
  },
  "taille": {
   "n": 4,
   "acc": 0.75
  },
  "passe": {
   "n": 1,
   "acc": 0.0
  },
  "p
… [977 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat > /tmp/a7_ladder.py <<'EOF'\nimport collections, sys, json, statistics\nsys.path.insert(0,'tools')\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import CHAMPS\nfrom cerveau.sommeil import Sommeil, _code, _signature, _mode_ … [2487 caractères tronqués]`

  ```
ladder1 {"champs": 0.9011494252873563, "exact": 0.0, "champs_nuls": 0.9968944099378882, "n": 29}
  coords {'de': {'n': 8, 'acc': 0.375}, 'vers': {'n': 8, 'acc': 0.0}, 'carte': {'n': 7, 'acc': 0.0}, 'case': {'n': 4, 'acc': 0.0}, 'symbole': {'n': 4, 'acc': 0.75}, 'taille': {'n': 4, 'acc': 1.0}, 'point': {'n': 3, 'acc': 0.0}, 'chemin_0': {'n': 6, 'acc': 0.6666666666666666}}
ladder3 {"champs": 0.8919540229885058, "exact": 0.0, "champs_nuls": 0.9937888198757764, "n": 29}
  coords {'de': {'n': 8, 'acc': 0.125}, 'vers': {'n': 8, 'acc': 0.0}, 'carte': {'n': 7, 'acc': 0.0}, 'case': {'n': 4, 'acc': 0.0}, 'symbole': {'n': 4, 'acc': 0.75}, 'taille': {'n': 4, 'acc': 1.0}, 'point': {'n': 3, 'acc': 0.0}, 'chemin_0': {'n': 6, 'acc': 0.6666666666666666}}
type_seul1 {"champs": 0.8896551724137931, "exact": 0.0, "champs_nuls": 1.0, "n": 29}
  coords {'de': {'n': 8, 'acc': 0.375}, 'vers': {'n': 8, 'acc': 0.0}, 'carte': {'n': 7, 'acc': 0.0}, 'case': {'n': 4, 'acc': 0.0}, 'symbole': {'n': 4, 'acc': 0.75}, 'taille': {'n': 4, 'acc': 0.75}, 'point': {'n': 3, 'acc': 0.0}, 'chemin_0': {'n': 6, 'acc': 0.5}}
  ```

### 🤖 Assistant

⏵ Premiers fichiers pour le parent, puis implémentation M8/M9

- **bash** `{"command": "cat > /tmp/a7-m8-m9.json <<'EOF'\n{\n \"a7\": \"M8/M9 — état partiel (exploration terminée, code en cours)\",\n \"partiel\": true,\n \"M8\": {\n  \"protocole\": \"leave-one-code-out, 29 codes, prototype par champ, clé = (jeu[,action[,type]])\",\n  \"exact\": 0.0,\n  \"preuve_exact_nul\" … [4417 caractères tronqués]`

  ```
ok
  ```

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "Point A7 (partiel déjà écrit : /tmp/a7-m8-m9.json + .md) :\n\nM8 — négatif net, mesuré. Leave-one-code-out sur les 29 codes (528 items) : exact = 0 % PAR CONSTRUCTION (un prototype ne sort qu'un code vu ; le code exclu n'est pas dans l … [1186 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

- **todo_write** `{"todos": [{"content": "Explorer les corpus et chiffrer le négatif M8 (fait)", "status": "completed"}, {"content": "Implémenter M8 conditionné + tenue à l'écart + hybrides honnêtes dans sommeil.py", "status": "in_progress"}, {"content": "Implémenter M2 réel voies.py et corriger les déficits dans les … [300 caractères tronqués]`

  ```
Updated todo list: 4 pending, 1 in progress, 1 completed.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "old_string": "- sur des **codes jamais vus**, le prototype ne peut pas produire le bon code :\n  l'exact est 0 % par construction. Un prototype est une marginale, pas une\n  généralisation.\n\nLe module ajoute donc : prototypes … [2725 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "def _cle(code: dict, cle) -> tuple:\n    if callable(cle):\n        return cle(code)\n    if cle == \"type\":\n        return (code.get(\"jeu\"), code.get(\"action\"), _signature(code))\n    if cle == \"jeu_type\" … [759 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "NOMS = tuple(nom for nom, _ in CHAMPS)\nCLES = (\"global\", \"jeu\", \"groupe\", \"type\", \"jeu_type\", \"action_type\", \"type_seul\")\nLADDER = (\"type\", \"groupe\", \"jeu\", \"global\")", "old_string": "NOMS  … [35 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "old_string": "        }\n        return res\n\n\ndef experience_m8(items_=None) -> dict:\n    return Sommeil().experience(items_)", "new_string": "        }\n        return res\n\n    # ---- A7 : prototypes conditionnés, tenue  … [25598 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "            pred, _ = self._predire(code, protos_par_cle, ladder, min_support)\n            bon = sum(1 for nom in NOMS if pred.get(nom) == code.get(nom))\n            ok += bon\n            ok_nc += bon\n         … [447 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "            for g in graines:\n                rng = random.Random(g)\n                exclus = set()", "old_string": "            for g in graines:\n                rng = random.Random(1000 + g)\n                 … [16 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nimport json\nfrom cerveau.sommeil import experience_contexte\nr=experience_contexte()\nprint(json.dumps(r['verdict'], ensure_ascii=False, indent=1))\nprint('LOO', json.dumps(r['loo_codes'] … [382 caractères tronqués]`

  ```
Traceback (most recent call last):
  File "<string>", line 3, in <module>
    from cerveau.sommeil import experience_contexte
ImportError: cannot import name 'experience_contexte' from 'cerveau.sommeil' (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py)
[stderr]

real	0m0,076s
user	0m0,061s
sys	0m0,015s
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "def experience_m8(items_=None) -> dict:\n    return Sommeil().experience(items_)\n\n\ndef experience_contexte(items_=None, graines=(1, 2, 3)) -> dict:\n    return Sommeil().experience_contexte(items_, graines)", " … [96 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nimport json\nfrom cerveau.sommeil import experience_contexte\nr=experience_contexte()\nprint(json.dumps(r['verdict'], ensure_ascii=False, indent=1))\nprint('LOO', json.dumps(r['loo_codes'] … [382 caractères tronqués]`

  ```
Traceback (most recent call last):
  File "<string>", line 4, in <module>
    r=experience_contexte()
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", line 921, in experience_contexte
    return Sommeil().experience_contexte(items_, graines)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", line 727, in experience_contexte
    par_champ_loo[nom]["ok_nul"] += d["ok_nul"]
                                    ~^^^^^^^^^^
KeyError: 'ok_nul'
[stderr]

real	0m0,211s
user	0m0,190s
sys	0m0,021s
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "                \"n_nul\": d[\"n_nul\"],\n                \"exact_nul\": d[\"ok_nul\"] / max(1, d[\"n_nul\"]),\n                \"ok_nul\": d[\"ok_nul\"],", "old_string": "                \"n_nul\": d[\"n_nul\"],\ … [71 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nimport json\nfrom cerveau.sommeil import experience_contexte\nr=experience_contexte()\nprint(json.dumps(r['verdict'], ensure_ascii=False, indent=1))\nprint('LOO', json.dumps(r['loo_codes'] … [382 caractères tronqués]`

  ```
"n": 29
 },
 "action_type": {
  "champs": 0.8896551724137931,
  "exact": 0.0,
  "champs_non_nuls": 0.5902298850574713,
  "champs_nuls": 1.0,
  "n": 29
 },
 "type_seul": {
  "champs": 0.8896551724137931,
  "exact": 0.0,
  "champs_non_nuls": 0.5902298850574713,
  "champs_nuls": 1.0,
  "n": 29
 },
 "ladder": {
  "champs": 0.9011494252873563,
  "exact": 0.0,
  "champs_non_nuls": 0.6350574712643678,
  "champs_nuls": 0.9968652037617555,
  "n": 29,
  "niveaux_utilises": {
   "type": 390,
   "jeu": 30,
   "groupe": 15
  },
  "par_champ": {
   "jeu": {
    "n": 29,
    "exact_non_nul": 1.0,
    "n_nul": 0,
    "exact_nul": 0.0
   },
   "action": {
    "n": 29,
    "exact_non_nul": 0.9310344827586207,
    "n_nul": 0,
    "exact_nul": 0.0
   },
   "de": {
    "n": 8,
    "exact_non_nul": 0.375,
    "n_nul": 21,
    "exact_nul": 1.0
   },
   "vers": {
    "n": 8,
    "exact_non_nul": 0.0,
    "n_nul": 21,
    "exact_nul": 1.0
   },
   "promotion": {
    "n": 1,
    "exact_non_nul": 0.0,
    "n_nul": 28,
    "exact_nul": 1.0
   },
   "roque": {
    "n": 2,
    "exact_non_nul": 0.0,
    "n_nul": 27,
    "exact_nul": 1.0
   },
   "case": {
    "n": 4,
    "exact_non_nul": 0.0,
    "n_nul": 25,
  
… [2530 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "        codes_tenus_resume = {\n            \"par_cle\": self._resume_par_cle(\n                {r[\"graine\"]: r[\"cles\"] for r in codes_tenus}),\n            \"ladder_champs\": sum(r[\"ladder\"][\"champs\"] for … [756 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "            controles[cle] = {\n                \"champs\": sum(r[\"champs\"] for r in rows) / max(1, len(rows)),\n                \"exact\": sum(r[\"exact\"] for r in rows) / max(1, len(rows)),\n                \ … [736 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "        # ---- 4 bis. la queue publiée : ses codes sont-ils dans le train ?\n        nq = int(len(its) * 0.8)\n        trq, teq = its[:nq], its[nq:]\n        ppq = self.prototypes_multi(trq)\n        vusq = {tuple … [698 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "            \"hybride_oracle_tautologique\": True,\n            \"controle_cle_permutee\": controles,\n            \"queue_publiee\": {\n                \"champs\": queue[\"prototype\"][\"champs\"],\n              … [1051 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "            \"plaafond_contextuel\": plafond,\n            \"loo_codes\": loo_resume,\n            \"codes_tenus\": codes_tenus,\n            \"codes_tenus_resume\": codes_tenus_resume,\n            \"paires_tenue … [465 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "            \"plafond_contextuel\": plafond,", "old_string": "            \"plaafond_contextuel\": plafond,"}`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nimport json\nfrom cerveau.sommeil import experience_contexte\nr=experience_contexte()\nprint(json.dumps(r['verdict'], ensure_ascii=False, indent=1))\nprint('LOO champs', {k: round(v['champ … [758 caractères tronqués]`

  ```
{
 "exact_loo": 0.0,
 "exact_loo_preuve": "nul par construction : le prototype ne peut rendre qu'un code vu, le code exclu n'est pas dans le train",
 "exact_codes_tenus": [
  0.0,
  0.0,
  0.0
 ],
 "champs_loo": {
  "global": 0.7494252873563219,
  "jeu": 0.8919540229885058,
  "groupe": 0.8919540229885058,
  "type": 0.8896551724137931,
  "jeu_type": 0.8896551724137931,
  "action_type": 0.8896551724137931,
  "type_seul": 0.8896551724137931,
  "ladder": 0.9011494252873563
 },
 "non_nuls_loo": {
  "global": 0.04597701149425287,
  "jeu": 0.6126436781609195,
  "groupe": 0.5971264367816091,
  "type": 0.5902298850574713,
  "jeu_type": 0.5902298850574713,
  "action_type": 0.5902298850574713,
  "type_seul": 0.5902298850574713,
  "ladder": 0.6350574712643678
 },
 "gain_jeu_sur_global_champs": 0.14252873563218393,
 "gain_groupe_sur_jeu_champs": 0.0,
 "gain_type_sur_jeu_champs": -0.0022988505747126853,
 "gain_backoff_sur_jeu_champs": 0.009195402298850519,
 "gain_backoff_sur_jeu_non_nuls": 0.022413793103448376,
 "plafond_groupe": 0.5795454545454546,
 "irreductible_groupe": 0.4204545454545454,
 "coordonnees_non_nulles_ladder": {
  "de": 0.375,
  "vers": 0.0,
  "point": 0.0,
  "carte": 0.0,
  "cas
… [3740 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,35p tools/cerveau/lesion.py", "description": "Re-read lesion header"}`

  ```
#!/usr/bin/env python3
"""M9 — lésions par module : privations déclarées et déficits mesurés.

Une lésion n'est pas une approximation : c'est une **privation déclarée** du
module, mesurée sur le même test que la version intacte, avec un **sham** (la
même mesure répétée sans privation) qui doit donner un déficit nul. Le déficit
est ``intacte - lésée`` ; un déficit négatif veut dire que la lésion *améliore*
— c'est un résultat, pas une erreur.

Modules couverts :

- **M1** : retirer le contexte de perception ;
- **M2** : couper la voie ventrale (action) ou dorsale (``de``) ; sur CPU, un
  substitut déterministe à deux têtes (bayes naïf sur n-grammes) est déclaré,
  avec la même double dissociation structurelle que ``voies.py`` ;
- **M3** : capacité du tampon (0, 1, 2, 4, 8, 12), dose-réponse ;
- **M4** : stockage vide, puis lésion du champ d'adressage (le champ est mis à
  ``None`` dans la requête) ;
- **M5** : retirer les transitions, l'ordre 2 ou le repli majoritaire ; contrôle
  positif sur une chaîne de Markov synthétique ;
- **M6** : retirer la porte (tout accepter), l'inverser, la rendre aléatoire ;
- **M7** : retirer la modulation (FIFO) ; décomposition clé surface/code et
  s
… [369 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "Modules couverts :\n\n- **M1** : retirer le contexte de perception ;\n- **M2** : couper la voie ventrale (action) ou dorsale (``de``). Par défaut le\n  **vrai ``voies.py``** est exécuté (encodeur natif gelé, entraî … [2240 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "import collections\nimport math\nimport os\nimport pathlib\nimport random\nimport time", "old_string": "import collections\nimport math\nimport random\nimport time"}`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "# ---------------------------------------------------------------------------\n# M2 — les deux voies (voies.py réel, proxy bayésien en repli)\n# --------------------------------------------------------------------- … [336 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "def _m2_proxy() -> dict:\n    \"\"\"Substitut CPU : deux têtes bayésiennes, même dissociation structurelle.\"\"\"\n    its = corpus_items()", "old_string": "def _m2() -> dict:\n    its = corpus_items()"}`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "    r = _entree(\n        \"couper la voie ventrale (action) / dorsale (de) — tête détruite\",\n        {\"action\": a, \"de\": d, \"de_non_nul\": d_nn, \"n_de_non_nul\": n_nn},\n        {\"action\": a_rand, \"de\" … [2207 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "    r[\"mode\"] = \"proxy\"\n    return r\n\n\ndef _m2_voies(pas: int = 300, graines=(1,), device: str | None = None,\n              base: str | None = None) -> dict:\n    \"\"\"Le vrai M2 : encodeur natif gelé + t … [5409 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

### 👤 Utilisateur

<system-reminder>
Updated instructions from: AGENTS.md

This file changed after it was loaded. Use the following content instead of the previously loaded instructions from this file.

# Directives de l'agent — Drave

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs
> unifiés (**49 portes, 8 chapitres, 174 fichiers / 242 JSON, 52 documents**), chemins archivés
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

## 4. Le minimum avant de conclure

- l'état est à jour dans [`docs/en-cours.md`](docs/en-cours.md) (synthèse, chantiers, questions en attente) ;
- la **roadmap** est à jour : le chantier fini y est marqué, le suivant est désigné ;
- la fiche est dans `reports/`, le récit dans `journal/`, le commit porte le chiffre ;
- les portes sont vertes, **hors les deux rouges structurelles connues** ;
- la revue de documentation passe, et les liens résolvent.

</system-reminder>

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 395,470p tools/cerveau/lesion.py", "description": "View M4 current code"}`

  ```
champs[nom] = {"n": len(presents),
                       "rappel_lese": ok / len(presents),
                       "deficit": 1.0 - ok / len(presents)}
    plus_faible = max(champs, key=lambda k: champs[k]["deficit"]) if champs else None
    return _entree(
        "stockage vide (M4 sans épisodes) ; puis lésion du champ d'adressage",
        {"rappel": intact, "completion": completion,
         "n": len(echantillon)},
        {"rappel": sans, "completion": completion_vide, "n": len(echantillon)},
        {"rappel": intact - sans, "completion": completion - completion_vide,
         "par_champ": champs,
         "champ_le_plus_necessaire": plus_faible,
         "deficit_champ_max": champs[plus_faible]["deficit"] if plus_faible else 0.0},
        len(echantillon), sham=0.0,
        note="échantillon stratifié par jeu ; le champ lésé est mis à None dans la requête")


# ---------------------------------------------------------------------------
# M5 — le prédictif
# ---------------------------------------------------------------------------
class _Pas:
    __slots__ = ("code", "jeu")

    def __init__(self, action: str):
        self.jeu = "synthetique"
        self.code = {"jeu": "
… [1657 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"^def _m8\\|^def batterie_lesions\\|^def _m4\\|^def _m5\" tools/cerveau/lesion.py", "description": "Locate M4/M8/battery line numbers"}`

  ```
362:def _m4(taille: int = 32) -> dict:
430:def _m5(seqs) -> dict:
546:def _m8() -> dict:
575:def batterie_lesions(rapide: bool = True) -> dict:
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "offset": 362, "limit": 45}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py</path>
<type>file</type>
<content>
362: def _m4(taille: int = 32) -> dict:
363:     its = corpus_items()
364:     par_jeu = collections.defaultdict(list)
365:     for it in its:
366:         par_jeu[it.jeu].append(it)
367:     rng = random.Random(7)
368:     echantillon = []
369:     for jeu, v in par_jeu.items():
370:         k = max(1, taille // len(par_jeu))
371:         echantillon.extend(rng.sample(v, min(k, len(v))))
372:     plein = Episodique()
373:     for it in echantillon:
374:         plein.stocker(it.texte, it.code, it.langue, it.paire)
375:     vide = Episodique()
376:     intact = sum(plein.rappel(it.code)["exact"] for it in echantillon) / len(echantillon)
377:     sans = sum(vide.rappel(it.code)["exact"] for it in echantillon) / len(echantillon)
378:     completion = sum(plein.completion({**it.code, "vers": None})["champs"]
379:                      for it in echantillon) / len(echantillon)
380:     completion_vide = sum(vide.completion({**it.code, "vers": None})["champs"]
381:                           for it in echantillon) / len(echantillon)
382:     champs = {}
383:     for nom in NOMS:
384:         if 
… [1277 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "    champs = {}\n    for nom in NOMS:\n        if nom in (\"jeu\", \"action\"):\n            continue  # None n'est pas dans le vocabulaire de ces deux champs\n        presents = [it for it in echantillon if it.cod … [1641 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "limit": 35, "offset": 548}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py</path>
<type>file</type>
<content>
548:         note="déficit négatif = la modulation dégrade ; la clé code est un effet de clé, pas de signal")
549: 
550: 
551: # ---------------------------------------------------------------------------
552: # M8 — le sommeil
553: # ---------------------------------------------------------------------------
554: def _m8() -> dict:
555:     r = experience_m8()
556:     q = r["queue"]
557:     intact = q["module_champs"]
558:     lese = q["baselines"]["global"]
559:     code_nouveaux = r["codes_nouveaux"]
560:     return _entree(
561:         "retirer le sommeil (aucun prototype, repli sur la marginale globale)",
562:         {"champs": intact["champs"], "exact": intact["exact"],
563:          "champs_non_nuls": intact["champs_non_nuls"],
564:          "exact_codes_uniques": r["dedup_tout"]["module"]["exact"],
565:          "exact_codes_nouveaux": [c["module"]["exact"] for c in code_nouveaux],
566:          "hybride_exact_queue": q["hybride"]["exact"],
567:          "hybride_couverture_queue": q["hybride"]["couverture"]},
568:         {"champs": lese["champs"], "exact": lese["exact"],
569
… [834 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "def _m8() -> dict:\n    \"\"\"Le sommeil, lésé sur le protocole honnête : code tenu à l'écart.\n\n    La lésion est le retrait de tout prototype (repli sur la marginale globale),\n    mesurée sur le **même** leave- … [4022 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "from cerveau.sommeil import Sommeil, experience_contexte, experience_m8", "old_string": "from cerveau.sommeil import Sommeil, experience_m8"}`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "limit": 80, "offset": 594}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py</path>
<type>file</type>
<content>
594:          "type_seul_sur_jeu_champs": rc["verdict"]["gain_type_sur_jeu_champs"]},
595:         29, sham=0.0,
596:         note=("le sommeil porte la structure des champs (motif de None, +15,2 pts "
597:               "de champs et +58,9 pts de non nuls contre la marginale globale) ; "
598:               "il ne produit aucun code jamais vu (exact nul par construction). "
599:               "L'hybride 100 % de la queue est tautologique (clé = code cible) ; "
600:               "clé par surface, sa couverture sur codes tenus est 0 %."))
601: 
602: 
603: # ---------------------------------------------------------------------------
604: # La batterie
605: # ---------------------------------------------------------------------------
606: def batterie_lesions(rapide: bool = True) -> dict:
607:     t0 = time.monotonic()
608:     seqs = corpus(0, 40, 12)
609:     its = corpus_items()
610:     m1 = _m1()
611:     m2 = _m2()
612:     m3 = _m3(seqs)
613:     m4 = _m4(36 if rapide else 72)
614:     m5 = _m5(seqs)
615:     m6 = _m6(its)
616:     m7 = _m7(6 if rapide else 20)
617:     m8 = _m8()
618
… [2666 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "def batterie_lesions(rapide: bool = True, m2: str = \"auto\") -> dict:\n    \"\"\"Batterie M1–M9. ``m2`` : auto (réel si possible), voies, proxy.\"\"\"\n    t0 = time.monotonic()\n    seqs = corpus(0, 40, 12)\n     … [7014 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nimport json\nfrom cerveau.lesion import batterie_lesions\nr=batterie_lesions(rapide=True, m2='proxy')\nprint('protocole', json.dumps(r['protocole'], ensure_ascii=False, indent=1))\nfor k,v … [402 caractères tronqués]`

  ```
Traceback (most recent call last):
  File "<string>", line 4, in <module>
    r=batterie_lesions(rapide=True, m2='proxy')
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", line 648, in batterie_lesions
    "M2_preservation": m2r["deficit"]["preservation"],
                       ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
KeyError: 'preservation'
[stderr]

real	0m5,647s
user	0m5,621s
sys	0m0,027s
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "        {\"action\": a - a_rand, \"de\": d - d_rand,\n         \"de_non_nul\": d_nn - d_rand_nn,\n         \"avec_priori\": {\"action\": a - a_prio, \"de\": d - d_prio,\n                         \"de_non_nul\": d_n … [682 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nimport json\nfrom cerveau.lesion import batterie_lesions\nr=batterie_lesions(rapide=True, m2='proxy')\nprint('protocole', json.dumps(r['protocole'], ensure_ascii=False, indent=1))\nfor k,v … [409 caractères tronqués]`

  ```
protocole {
 "rapide": true,
 "cpu": true,
 "m2_mode": "proxy",
 "m2_statut": "proxy CPU (bayes naïf, deux têtes) ; voies.py non exécuté",
 "m4_echantillon": 36,
 "m7_permutations": 6,
 "n_items": 528,
 "n_sequences": 160
}
M1 | mesure | deficit= {"exact": 0.29166666666666663, "relatif": 0.29166666666666663}
M2 | proxy CPU (bayes naïf, deux têtes) ; voies.py non exécuté | deficit= {"action": 0.523841059602649, "de": 0.5112582781456954, "de_non_nul": 0.6304347826086957, "avec_priori": {"action": 0.3973509933774835, "de": 0.0927152317880795, "de_non_nul": 0.7536231884057971}, "majorite": {"action": 0.26490066225165565,
M3 | mesure | deficit= {"span": 1.0, "exact": 1.0, "nback2_controle": 1.0}
M4 | mesure | deficit= {"rappel": 1.0, "completion": 0.9866666666666666, "par_champ": {"de": {"n": 7, "intacte": 1.0, "rappel_lese": 1.0, "deficit": 0.0}, "vers": {"n": 7, "intacte": 1.0, "rappel_lese": 1.0, "deficit": 0.0}, "roque": {"n": 1, "intacte": 1.0, "rap
M5 | mesure | deficit= {"exact": 0.036630036630036625, "surprise": 0.007608411732380915, "sans_ordre2": 0.0, "controle_positif_deficit": 0.6818181818181818}
M6 | mesure | deficit= {"canal_langue": 0.19318181818181823, "canal_sens": 0.19
… [961 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time CUDA_VISIBLE_DEVICES=0 PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nimport json\nfrom cerveau.lesion import _m2\nr=_m2('voies', graines=(1,))\nprint(json.dumps({k:v for k,v in r.items() if k!='par_graine'}, ensure_ascii=False, indent … [108 caractères tronqués]`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights:  90%|█████████ | 81/90 [00:00<00:00, 800.31it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 878.15it/s]
Traceback (most recent call last):
  File "<string>", line 4, in <module>
    r=_m2('voies', graines=(1,))
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", line 307, in _m2
    return _m2_voies(graines=graines)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", line 263, in _m2_voies
    maj_a, maj_d = moy("majorite_action", ""), moy("majorite_de", "")
                   ~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", line 258, in moy
    return sum(g[famille][nom] for g in par_graine) / len(par_graine)
           ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", line 258, in <genexpr>
    return sum(g[famille][nom] for g in par_graine) / len(par_graine)
               ~~~~~~~~~~^^^^^
TypeError: 'float' object is not subscriptable
[stderr]

real	0m27,256s
user	0m31,146s
sys	0m2,006s
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "    def moy(famille: str, nom: str = \"\") -> float:\n        if nom:\n            return sum(g[famille][nom] for g in par_graine) / len(par_graine)\n        return sum(g[famille] for g in par_graine) / len(par_gra … [716 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time CUDA_VISIBLE_DEVICES=0 PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nimport json\nfrom cerveau.lesion import _m2\nr=_m2('voies', graines=(1,))\nprint(json.dumps({k:v for k,v in r.items() if k!='par_graine'}, ensure_ascii=False, indent … [108 caractères tronqués]`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights:  78%|███████▊  | 70/90 [00:00<00:00, 697.86it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 830.81it/s]
{
 "lesion": "couper la voie ventrale (action) / dorsale (de) — voies.py réel",
 "intacte": {
  "action": 0.9863013698630136,
  "de": 0.9315068493150684,
  "de_non_nul": 0.9315068493150684,
  "n": 146
 },
 "lessee": {
  "action": 0.1232876712328767,
  "de": 0.02054794520547945,
  "de_non_nul": 0.02054794520547945,
  "ventrale": {
   "action": 0.1232876712328767,
   "de": 0.9315068493150684,
   "de_non_nul": 0.9315068493150684
  },
  "dorsale": {
   "action": 0.9863013698630136,
   "de": 0.02054794520547945,
   "de_non_nul": 0.02054794520547945
  },
  "avec_priori": {
   "action": 0.9863013698630136,
   "de": 0.4794520547945205
  }
 },
 "deficit": {
  "action": 0.8630136986301369,
  "de": 0.910958904109589,
  "de_non_nul": 0.910958904109589,
  "avec_priori": {
   "action": 0.0,
   "de": 0.4520547945205479,
   "de_non_nul": 0.4520547945205479
  },
  "majorite": {
   "action": 0.9863013698630136,
   "de": 0.4794520547945205
  },
  "preservation": {
   "action_sous_lesion_dorsale": 0.9863013698630136,
… [662 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "        par_champ_loo = collections.defaultdict(\n            lambda: {\"n_non_nul\": 0, \"ok_non_nul\": 0, \"n_nul\": 0, \"ok_nul\": 0})\n        par_champ_jeu = collections.defaultdict(\n            lambda: {\"n … [281 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "                for k in (\"champs\", \"exact\", \"champs_non_nuls\", \"champs_nuls\"):\n                    loo[cle][k].append(r[k])\n                loo[cle][\"n\"] += r[\"n\"]\n                if cle == \"jeu\" … [420 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "        coords = {nom: g[\"ladder\"][\"par_champ\"].get(nom, {}).get(\"exact_non_nul\", 0.0)\n                  for nom in (\"de\", \"vers\", \"point\", \"carte\", \"case\",\n                              \"chemin … [880 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "            \"gain_backoff_sur_jeu_champs\": gain_ladder,\n            \"gain_backoff_sur_jeu_non_nuls\": gain_ladder_nn,\n            \"gain_backoff_sur_jeu_coordonnees\": gain_coordonnees,", "old_string": "      … [118 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "            \"conditionner_aide_exact\": False,\n            \"conditionner_aide_structure\": True,\n            \"conditionner_aide_valeurs\": gain_coordonnees > 0.05,\n            \"conclusion\": (\"le condition … [506 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nimport json\nfrom cerveau.sommeil import experience_contexte\nr=experience_contexte()\nv=r['verdict']\nfor k in ('exact_loo','gain_groupe_sur_jeu_champs','gain_type_sur_jeu_champs','gain_backof … [468 caractères tronqués]`

  ```
exact_loo 0.0
gain_groupe_sur_jeu_champs 0.0
gain_type_sur_jeu_champs -0.0022988505747126853
gain_backoff_sur_jeu_champs 0.009195402298850519
gain_backoff_sur_jeu_non_nuls 0.022413793103448376
gain_backoff_sur_jeu_coordonnees 0.04255319148936171
plafond_groupe 0.5795454545454546
conditionner_aide_structure True
conditionner_aide_valeurs False
conclusion le conditionnement ne gagne que le motif de None ; les coordonnées justes sont des coïncidences de marginale (case de départ, sous-type roque) ; exact nul
queue {'champs': 0.9647798742138365, 'exact': 0.6509433962264151, 'n_test': 106, 'codes_test_vus_dans_train': 106, 'paire_oracle_exact': 1.0, 'plafond_corpus_groupe': 0.5795454545454546}
controles {'groupe': (0.8469, 0.4643, 3.6666666666666665), 'type': (0.8481, 0.5367, 2.3333333333333335)}
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py", "new_string": "from cerveau.sommeil import (Sommeil, _cle, experience_contexte,\n                             experience_m8)", "old_string": "from cerveau.sommeil import Sommeil, experience_m8"}`

  ```
Error: cannot modify "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py", "new_string": "    def test_experience_reelle(self):\n        r = experience_m8()\n        v = r[\"verdict\"]\n        self.assertTrue(v[\"champs_96_48_reproduit\"])\n        self.assertTrue(v[\"exact_annonce_0_est_fa … [4061 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py</path>
<type>file</type>
<content>
1: from __future__ import annotations
2: 
3: import unittest
4: from types import SimpleNamespace
5: 
6: from cerveau.sommeil import Sommeil, experience_m8
7: 
8: 
9: def _it(code, texte="x", paire="p", jeu="echecs"):
10:     return SimpleNamespace(code=code, texte=texte, paire=paire, jeu=jeu)
11: 
12: 
13: CODE_A = {"jeu": "echecs", "action": "deplacer", "de": 62, "vers": 45}
14: CODE_B = {"jeu": "echecs", "action": "deplacer", "de": 52, "vers": 36}
15: CODE_C = {"jeu": "dames", "action": "prendre", "chemin_0": 8, "chemin_1": 13}
16: 
17: 
18: class TestSommeil(unittest.TestCase):
19:     def test_consolider_et_evaluer(self):
20:         train = [_it(CODE_A, "Nf3"), _it(CODE_A, "g1f3"), _it(CODE_B, "e3")]
21:         s = Sommeil()
22:         protos = s.consolider(train)
23:         self.assertEqual(len(protos), 1)
24:         self.assertEqual(protos[("echecs", "deplacer")]["de"], 62)
25:         r = s.evaluer([_it(CODE_A), _it(CODE_B)], protos)
26:         self.assertEqual(r["n"], 2)
27:         self.assertGreater(r["champs"], 0.5)
28:         self.assertTrue(0.0 <= r["exact
… [1681 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py", "new_string": "from cerveau.sommeil import (Sommeil, _cle, experience_contexte,\n                             experience_m8)", "old_string": "from cerveau.sommeil import Sommeil, experience_m8"}`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py", "new_string": "    def test_experience_reelle(self):\n        r = experience_m8()\n        v = r[\"verdict\"]\n        self.assertTrue(v[\"champs_96_48_reproduit\"])\n        self.assertTrue(v[\"exact_annonce_0_est_fa … [3977 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py", "offset": 50, "limit": 100}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py</path>
<type>file</type>
<content>
50: 
51:     def test_dedup(self):
52:         its = [_it(CODE_A, "a"), _it(CODE_A, "b"), _it(CODE_B, "c")]
53:         self.assertEqual(len(Sommeil.dedupliquer(its, "code")), 2)
54: 
55:     def test_experience_reelle(self):
56:         r = experience_m8()
57:         v = r["verdict"]
58:         self.assertTrue(v["champs_96_48_reproduit"])
59:         self.assertTrue(v["exact_annonce_0_est_faux"])
60:         self.assertGreater(v["exact_queue"], 0.6)
61:         self.assertTrue(all(x == 0.0 for x in v["exact_codes_nouveaux"]))
62:         self.assertEqual(r["queue"]["hybride"]["exact"], 1.0)
63:         self.assertGreater(v["champs_non_nuls"], 0.8)
64: 
65:     # ---- A7 : clés étendues, backoff, hybride honnête, code tenu à l'écart
66:     def test_cles_etendues(self):
67:         self.assertEqual(_cle(CODE_A, "type_seul"),
68:                          (("action", "de", "jeu", "vers"),))
69:         self.assertEqual(_cle(CODE_A, "jeu_type"),
70:                          ("echecs", ("action", "de", "jeu", "vers")))
71:         self.assertEqual(_cle(CODE_A, "action_type"),
72
… [2975 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py"}`

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
22:             self.assertEqual(v, 0.0)
23: 
24:     def test_m1_contexte(self):
25:         d = self.r["modules"]["M1"]["deficit"]["exact"]
26:         self.assertGreater(d, 0.25)
27:         self.assertLess(d, 0.35)
28: 
29:     def test_m2_double_dissociation(self):
30:         m2 = self.r["modules"]["M2"]
31:         self.assertTrue(m2["deficit"]["double_dissociation"])
32:         self.assertGreater(m2["defici
… [2070 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py", "new_string": "    def test_sham(self):\n        for m, v in self.r[\"controles\"][\"sham\"].items():\n            self.assertAlmostEqual(v, 0.0, places=12)", "old_string": "    def test_sham(self):\n        for m, v i … [82 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py", "new_string": "    def test_m2_double_dissociation(self):\n        m2 = self.r[\"modules\"][\"M2\"]\n        self.assertTrue(m2[\"deficit\"][\"double_dissociation\"])\n        self.assertGreater(m2[\"deficit\"][\"actio … [1123 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py", "new_string": "    def test_m4_stockage(self):\n        m4 = self.r[\"modules\"][\"M4\"]\n        self.assertEqual(m4[\"intacte\"][\"rappel\"], 1.0)\n        self.assertEqual(m4[\"lessee\"][\"rappel\"], 0.0)\n        s … [703 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py", "new_string": "    def test_m8_sommeil(self):\n        m8 = self.r[\"modules\"][\"M8\"]\n        self.assertEqual(m8[\"intacte\"][\"exact\"], 0.0)\n        self.assertGreater(m8[\"deficit\"][\"champs\"], 0.10)\n        … [1999 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py", "new_string": "        self.assertAlmostEqual(v[\"gain_groupe_sur_jeu_champs\"], 0.0, places=12)", "old_string": "        self.assertEqual(v[\"gain_groupe_sur_jeu_champs\"], 0.0)"}`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest cerveau.tests.test_sommeil -v 2>&1 | tail -30", "description": "Run sommeil tests", "timeoutMs": 300000}`

  ```
test_backoff_champ_par_champ (cerveau.tests.test_sommeil.TestSommeil.test_backoff_champ_par_champ) ... ok
test_baselines (cerveau.tests.test_sommeil.TestSommeil.test_baselines) ... ok
test_cles_etendues (cerveau.tests.test_sommeil.TestSommeil.test_cles_etendues) ... ok
test_consolider_et_evaluer (cerveau.tests.test_sommeil.TestSommeil.test_consolider_et_evaluer) ... ok
test_dedup (cerveau.tests.test_sommeil.TestSommeil.test_dedup) ... ok
test_experience_contexte_negative (cerveau.tests.test_sommeil.TestSommeil.test_experience_contexte_negative) ... ok
test_experience_reelle (cerveau.tests.test_sommeil.TestSommeil.test_experience_reelle) ... ok
test_hybride (cerveau.tests.test_sommeil.TestSommeil.test_hybride) ... ok
test_hybride_surface_honnete (cerveau.tests.test_sommeil.TestSommeil.test_hybride_surface_honnete) ... ok

----------------------------------------------------------------------
Ran 9 tests in 1.295s

OK
[stderr]

real	0m1,399s
user	0m1,382s
sys	0m0,019s
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nimport unittest\nfrom cerveau.lesion import batterie_lesions\nfrom cerveau.tests import test_lesion\ntest_lesion.TestLesion.setUpClass = classmethod(lambda cls: setattr(cls, 'r', batterie_ … [257 caractères tronqués]`

  ```
test_deficits_intacte_moins_lesee (cerveau.tests.test_lesion.TestLesion.test_deficits_intacte_moins_lesee) ... ERROR
test_json (cerveau.tests.test_lesion.TestLesion.test_json) ... ok
test_m1_contexte (cerveau.tests.test_lesion.TestLesion.test_m1_contexte) ... ok
test_m2_double_dissociation (cerveau.tests.test_lesion.TestLesion.test_m2_double_dissociation) ... ok
test_m2_mode_et_preservation (cerveau.tests.test_lesion.TestLesion.test_m2_mode_et_preservation) ... ok
test_m3_tampon (cerveau.tests.test_lesion.TestLesion.test_m3_tampon) ... ok
test_m4_stockage (cerveau.tests.test_lesion.TestLesion.test_m4_stockage) ... ok
test_m5_transitions (cerveau.tests.test_lesion.TestLesion.test_m5_transitions) ... ok
test_m6_porte (cerveau.tests.test_lesion.TestLesion.test_m6_porte) ... ok
test_m7_modulation (cerveau.tests.test_lesion.TestLesion.test_m7_modulation) ... ok
test_m8_sommeil (cerveau.tests.test_lesion.TestLesion.test_m8_sommeil) ... ok
test_sham (cerveau.tests.test_lesion.TestLesion.test_sham) ... ok
test_structure (cerveau.tests.test_lesion.TestLesion.test_structure) ... ok

======================================================================
ERROR: test_deficits_intacte_moins_lese
… [583 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "        {\"action\": a_rand, \"de\": d_rand, \"de_non_nul\": d_rand_nn,\n         \"avec_priori\": {\"action\": a_prio, \"de\": d_prio},", "old_string": "        {\"action\": a_rand, \"de\": d_rand,\n         \"ave … [51 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nimport unittest\nfrom cerveau.lesion import batterie_lesions\nfrom cerveau.tests import test_lesion\ntest_lesion.TestLesion.setUpClass = classmethod(lambda cls: setattr(cls, 'r', batterie_ … [259 caractères tronqués]`

  ```
m["intacte"][i] - m["lessee"][i],
    ~~~~~~~~~~~~^^^
KeyError: 'canal_langue'

----------------------------------------------------------------------
Ran 13 tests in 5.141s

FAILED (errors=1)
[stderr]

real	0m5,306s
user	0m5,277s
sys	0m0,029s
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py", "new_string": "            \"M6\": [(\"canal_langue\", \"exact\"),\n                   (\"tout_accepter\", \"exact\")],", "old_string": "            \"M6\": [(\"canal_langue\", \"canal_langue\"),\n                   (\ … [40 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nimport unittest\nfrom cerveau.lesion import batterie_lesions\nfrom cerveau.tests import test_lesion\ntest_lesion.TestLesion.setUpClass = classmethod(lambda cls: setattr(cls, 'r', batterie_ … [259 caractères tronqués]`

  ```
m["intacte"][i] - m["lessee"][i],
                      ~~~~~~~~~~~^^^
KeyError: 'exact'

----------------------------------------------------------------------
Ran 13 tests in 5.015s

FAILED (errors=1)
[stderr]

real	0m5,178s
user	0m5,130s
sys	0m0,049s
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nfrom cerveau.lesion import batterie_lesions\nr=batterie_lesions(rapide=True, m2='proxy')\ncouples = {'M1':[('exact','exact')],'M2':[('action','action'),('de','de'),('de_non_nul','de_non_nul')], … [596 caractères tronqués]`

  ```
KO M6 canal_langue exact manque 'exact' lessee keys ['canal_langue', 'canal_sens', 'tout_non', 'tout_accepter']
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py", "new_string": "    def test_deficits_intacte_moins_lesee(self):\n        couples = {\n            \"M1\": [(\"exact\", \"exact\", \"exact\")],\n            \"M2\": [(\"action\", \"action\", \"action\"), (\"de\", \"de\" … [2111 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nimport unittest\nfrom cerveau.lesion import batterie_lesions\nfrom cerveau.tests import test_lesion\ntest_lesion.TestLesion.setUpClass = classmethod(lambda cls: setattr(cls, 'r', batterie_ … [259 caractères tronqués]`

  ```
.............
----------------------------------------------------------------------
Ran 13 tests in 4.833s

OK
[stderr]

real	0m4,990s
user	0m4,964s
sys	0m0,027s
  ```

### 🤖 Assistant

⏵ Tests complets avec le M2 réel, puis mesures finales

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time CUDA_VISIBLE_DEVICES=0 PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest discover -s tools/cerveau/tests -t tools -v 2>&1 | tail -40", "description": "Full cerveau test suite with real M2", "run_in_background": true, "timeoutMs": 900 … [4 caractères tronqués]`

  ```
started background job bash-1849
  ```

- **write** `{"file_path": "/tmp/a7_mesure.py", "content": "#!/usr/bin/env python3\n\"\"\"A7 — mesure finale M8/M9, sortie /tmp/a7-m8-m9.json.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport platform\nimport sys\nimport time\n\nsys.path.insert(0, \"tools\")\n\nimport torch  # noqa: E402\nfrom ce … [7916 caractères tronqués]`

  ```
<path>/tmp/a7_mesure.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 👤 Utilisateur

background job bash-1849 (bash: cd /home/stephane/GitHub/Qtrinet && time CUDA_VISIBLE_DEVICES=0 PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest discover -s tools/cerveau/tests -t tools -v 2>&1 | tail -40) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-1849"}`

  ```
test_cible_dames_dernier_chemin (cerveau.tests.test_predictif.TestCibles.test_cible_dames_dernier_chemin) ... ok
test_cible_inconnue (cerveau.tests.test_predictif.TestCibles.test_cible_inconnue) ... ok
test_source_absente (cerveau.tests.test_predictif.TestCibles.test_source_absente) ... ok
test_source_et_cible (cerveau.tests.test_predictif.TestCibles.test_source_et_cible) ... ok
test_contexte_absent_ne_masque_pas (cerveau.tests.test_predictif.TestContexte.test_contexte_absent_ne_masque_pas) ... ok
test_contexte_ameliore_la_surprisal (cerveau.tests.test_predictif.TestContexte.test_contexte_ameliore_la_surprisal) ... ok
test_la_vraie_valeur_est_dans_le_masque (cerveau.tests.test_predictif.TestContexte.test_la_vraie_valeur_est_dans_le_masque) ... ok
test_masque_uniforme (cerveau.tests.test_predictif.TestContexte.test_masque_uniforme) ... ok
test_melange_invalide (cerveau.tests.test_predictif.TestContexte.test_melange_invalide) ... ok
test_permutation_des_contextes (cerveau.tests.test_predictif.TestContexte.test_permutation_des_contextes) ... ok
test_plateau_par_jeu (cerveau.tests.test_predictif.TestContexte.test_plateau_par_jeu) ... ok
test_action_constante_aucun_gain (cerveau.tests.t
… [2623 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time CUDA_VISIBLE_DEVICES=0 PYTHONPATH=tools /home/stephane/gpu-env/bin/python /tmp/a7_mesure.py 2>&1 | tail -15", "description": "Run final A7 measurement and write JSON", "timeoutMs": 900000}`

  ```
batterie_lesions ...
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 922.68it/s]
  27.4 s, M2=voies
expériences M8 ...
référence batterie.py ...
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1053.82it/s]
écrit /tmp/a7-m8-m9.json (98.3 s)
[stderr]

real	1m41,383s
user	1m44,774s
sys	0m3,870s
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git status --short | head -30 && echo \"---\" && git diff --stat -- tools/cerveau/sommeil.py tools/cerveau/lesion.py tools/cerveau/tests/test_sommeil.py tools/cerveau/tests/test_lesion.py", "description": "Check git status and my diff stat"}`

  ```
M tools/cerveau/lesion.py
 M tools/cerveau/predictif.py
 M tools/cerveau/sommeil.py
 M tools/cerveau/tests/test_lesion.py
 M tools/cerveau/tests/test_sommeil.py
 M tools/cerveau/tests/test_voies.py
 M tools/cerveau/voies.py
---
 tools/cerveau/lesion.py             | 256 +++++++++++++---
 tools/cerveau/sommeil.py            | 584 ++++++++++++++++++++++++++++++++++++
 tools/cerveau/tests/test_lesion.py  |  55 +++-
 tools/cerveau/tests/test_sommeil.py |  61 +++-
 4 files changed, 913 insertions(+), 43 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git diff --stat -- tools/cerveau/voies.py tools/cerveau/predictif.py && git diff -- tools/cerveau/voies.py | head -80", "description": "Inspect concurrent changes to voies.py"}`

  ```
tools/cerveau/predictif.py |  10 +-
 tools/cerveau/voies.py     | 353 ++++++++++++++++++++++++++++++++++++++++++---
 2 files changed, 338 insertions(+), 25 deletions(-)
diff --git a/tools/cerveau/voies.py b/tools/cerveau/voies.py
index 957efb21..27055b18 100644
--- a/tools/cerveau/voies.py
+++ b/tools/cerveau/voies.py
@@ -21,11 +21,29 @@ surfaces **réelles** (`items`). Le module expose aussi les ablations :
 Les surfaces et le contexte sont normalisés (`normaliser`) puis lus en octets,
 comme dans le prototype d'origine. L'API `entrainer`/`evaluer` reste compatible
 avec `batterie.py` quand aucun champ dorsal supplémentaire n'est demandé.
+
+## Généralisation aux surfaces inédites (A5)
+
+Deux leviers sont ajoutés, tous deux **désactivés par défaut** :
+
+- `augmentation_*` (voir `augmenter`) : le corpus d'entraînement est étendu par
+  les **règles** des jeux (positions variées, coups légaux) et par des
+  **familles de surfaces** absentes du corpus synthétique : UCI collé / espacé /
+  tireté, SAN anglais et français, prises `x`, promotions, NLG `de … vers …`,
+  `from … to …`, dames numérique `9x18` et algébrique `b6xd4`, go SGF `B[dd]`
+  et français `ligne 4 colonne 4`. Aucune
… [2461 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nr=json.load(open('/tmp/a7-m8-m9.json'))\nprint('size', len(open('/tmp/a7-m8-m9.json').read()))\nm2=r['M9']['M2']\nprint('M2 mode', m2['mode'], 'statut', m2['statut'])\nprint('intacte', {k:round(v,4) for k,v in m2['inta … [978 caractères tronqués]`

  ```
size 77892
M2 mode voies statut voies.py réel : base /tmp/natif-600-512-8-align-s1, 300 pas, graines [1], cuda
intacte {'action': 0.9863, 'de': 0.9178, 'de_non_nul': 0.9178}
lessee {'action': 0.1233, 'de': 0.0205, 'de_non_nul': 0.0205, 'ventrale': {'action': 0.1233, 'de': 0.9178, 'de_non_nul': 0.9178}, 'dorsale': {'action': 0.9863, 'de': 0.0205, 'de_non_nul': 0.0205}, 'avec_priori': {'action': 0.9863, 'de': 0.4795}}
deficit {'action': 0.863, 'de': 0.8973, 'de_non_nul': 0.8973, 'majorite': {'action': 0.9863013698630136, 'de': 0.4794520547945205}, 'double_dissociation': True}
coherence keys ['erreur_reference']
coh M2 null
coh M9 map null
coh others {'M1': None, 'M3': None, 'M4': None, 'M5': None, 'M6': None, 'M8': None}
M8 verdict {
 "exact_loo": 0.0,
 "exact_loo_preuve": "nul par construction : le prototype ne peut rendre qu'un code vu, le code exclu n'est pas dans le train",
 "exact_codes_tenus": [
  0.0,
  0.0,
  0.0
 ],
 "champs_loo": {
  "global": 0.7494252873563219,
  "jeu": 0.8919540229885058,
  "groupe": 0.8919540229885058,
  "type": 0.8896551724137931,
  "jeu_type": 0.8896551724137931,
  "action_type": 0.8896551724137931,
  "type_seul": 0.8896551724137931,
  "ladder": 0.901
… [2023 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && /home/stephane/gpu-env/bin/python -c \"\nimport json\nr=json.load(open('/tmp/a7-m8-m9.json'))\nprint(r['M9']['coherence_batterie_py'])\nprint('par_graine' in r['M9'], r['M9'].get('M2_par_graine'))\n\"", "description": "Show reference coherence error"}`

  ```
{'erreur_reference': "KeyError: 'M2_lese_dorsale_de'"}
False [{'graine': 1, 'intacte': {'action': 0.9863013698630136, 'de': 0.9178082191780822, 'n': 146}, 'ventrale': {'action': 0.1232876712328767, 'de': 0.9178082191780822, 'n': 146}, 'dorsale': {'action': 0.9863013698630136, 'de': 0.02054794520547945, 'n': 146}, 'sham_action': 0.0, 'sham_de': 0.0, 'majorite_action': 0.9863013698630136, 'majorite_de': 0.4794520547945205}]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"M2_lese_dorsale_de\" tools | head -10", "description": "Locate the KeyError source"}`

  ```
tools/cerveau/batterie.py:194:        "M2_lese_dorsale_de": m2r["lese_dorsale"]["de"],
[stderr]
grep: tools/cerveau/__pycache__/batterie.cpython-313.pyc: binary file matches
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 70,90p tools/cerveau/batterie.py && echo \"--- m9\" && sed -n 186,205p tools/cerveau/batterie.py && echo \"--- test\" && CUDA_VISIBLE_DEVICES=0 PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nfrom cerveau import batterie as ref\nr2=re … [196 caractères tronqués]`

  ```
"evenements": len(bus.journal)}


def m2():
    import torch
    from transformers import AutoModelForCausalLM
    from cerveau.voies import entrainer, evaluer
    base = AutoModelForCausalLM.from_pretrained("/tmp/natif-600-512-8-align-s1", dtype=torch.float32)
    m, val = entrainer(base, 300, 32, 64, 1, "cuda" if torch.cuda.is_available() else "cpu", synth=True)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    return {"normal": evaluer(m, val, dev), "lese_ventrale": evaluer(m, val, dev, "ventral"),
            "lese_dorsale": evaluer(m, val, dev, "dorsal")}


def m3(seqs):
    import random
    m = MemoireTravail(12)
    sp = m.span(seqs)
    n1 = m.nback_scores(seqs, 1)
    n2 = m.nback_scores(seqs, 2)
    # contrôle n-back : une suite de 5 codes répétés, donc des répétitions réelles
--- m9
def m9(m1r, m2r, m3r, m4r, m5r, m6r, m7r):
    # Les lésions sont des privations déclarées, pas des approximations.
    seqs0 = MemoireTravail(0)
    span0 = seqs0.span(corpus(0, 10, 8))["span"]
    vide = Episodique()
    return {
        "M1_sans_contexte": 1.0 - m1r["sans_contexte"],
        "M2_lese_ventrale_action": m2r["lese_ventrale"]["action"],
        "M2_lese_dorsale_de"
… [694 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=0 PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF' 2>&1 | tail -25\nimport traceback\nfrom cerveau import batterie as ref\ntry:\n    seqs3 = ref.corpus(0, 40, 12)\n    r1 = ref.m1(); print('m1 ok')\n    r2 = ref.m2();  … [483 caractères tronqués]`

  ```
m1 ok
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1137.30it/s]
m2 ok {'normal': ['action', 'de', 'n'], 'lese_ventrale': ['action', 'de', 'n'], 'lese_dorsale': ['action', 'de', 'n']}
m3 ok
m4 ok
m5 ok
m6 ok
m7 ok
m8 ok
m9 ok {'M1_sans_contexte': 0.29166666666666663, 'M2_lese_ventrale_action': 0.1232876712328767, 'M2_lese_dorsale_de': 0.02054794520547945, 'M3_capacite_zero': 0, 'M4_sans_stockage': 0.0, 'M5_sans_transitions': 0.9120879120879121, 'M6_sans_porte': 0.05681818181818177, 'M7_sans_modulation': 0.03644646924829157, 'M8_sans_sommeil': 0.0}
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Complète /tmp/a7-m8-m9.json avec la référence batterie.py (non modifié).\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport subprocess\nimport sys\nimport time\n\nsys.path.insert(0, \"tools\")\n\n\ndef main() -> int:\n    from cerveau import b … [6054 caractères tronqués]`

  ```
<path>/tmp/a7_patch.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time CUDA_VISIBLE_DEVICES=0 PYTHONPATH=tools /home/stephane/gpu-env/bin/python /tmp/a7_patch.py 2>&1 | tail -40", "description": "Patch JSON with batterie.py coherence", "timeoutMs": 600000}`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1033.57it/s]
patché 81536 octets
{
 "batterie_normal": {
  "action": 0.9863013698630136,
  "de": 0.9315068493150684,
  "n": 146
 },
 "lesion_intacte": {
  "action": 0.9863013698630136,
  "de": 0.9178082191780822,
  "de_non_nul": 0.9178082191780822,
  "n": 146
 },
 "batterie_lese_ventrale": {
  "action": 0.1232876712328767,
  "de": 0.9315068493150684,
  "n": 146
 },
 "lesion_ventrale": {
  "action": 0.1232876712328767,
  "de": 0.9178082191780822,
  "de_non_nul": 0.9178082191780822
 },
 "batterie_lese_dorsale": {
  "action": 0.9863013698630136,
  "de": 0.02054794520547945,
  "n": 146
 },
 "lesion_dorsale": {
  "action": 0.9863013698630136,
  "de": 0.02054794520547945,
  "de_non_nul": 0.02054794520547945
 },
 "ecart_de": {
  "batterie": 0.9315068493150684,
  "lesion": 0.9178082191780822
 }
}
[stderr]

real	1m19,879s
user	1m23,135s
sys	0m2,810s
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "    par_graine = []\n    val = []\n    for graine in graines:\n        # Les têtes sont initialisées par le RNG torch global : sans graine,\n        # deux exécutions du même protocole diffèrent de 1–2 items. On fi … [523 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=0 PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF' 2>&1 | tail -8\nfrom cerveau.lesion import _m2\nfor i in range(2):\n    r=_m2('voies', graines=(1,))\n    print(i, r['intacte'], {k:round(v,4) for k,v in r['deficit']. … [143 caractères tronqués]`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1142.02it/s]
0 {'action': 0.9863013698630136, 'de': 0.9315068493150684, 'de_non_nul': 0.9315068493150684, 'n': 146} {'action': 0.863, 'de': 0.911, 'de_non_nul': 0.911} True
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1125.47it/s]
1 {'action': 0.9863013698630136, 'de': 0.9315068493150684, 'de_non_nul': 0.9315068493150684, 'n': 146} {'action': 0.863, 'de': 0.911, 'de_non_nul': 0.911} True
  ```

- **edit** `{"file_path": "/tmp/a7_mesure.py", "new_string": "            \"M8\": {\"batterie_champs\": r8[\"champs\"],\n                   \"batterie_exact\": r8[\"exact\"],\n                   \"lesion_queue_champs\": mod[\"M8\"][\"intacte\"][\"queue_champs\"],\n                   \"lesion_queue_exact\": mod[ … [2413 caractères tronqués]`

  ```
The file /tmp/a7_mesure.py has been updated successfully.
  ```

- **bash** `{"command": "cd /tmp && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport re\np='/tmp/a7_mesure.py'\ns=open(p).read()\ns=s.replace('import platform\\nimport sys', 'import platform\\nimport subprocess\\nimport sys')\ns=s.replace('''            \"audit_deficits\": {''', '''            \"note_voies\" … [884 caractères tronqués]`

  ```
patched script
batterie_lesions ...
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 991.49it/s]
  26.9 s, M2=voies
expériences M8 ...
référence batterie.py ...
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1071.76it/s]
écrit /tmp/a7-m8-m9.json (96.7 s)
[stderr]

real	1m39,715s
user	1m42,546s
sys	0m4,041s
  ```

- **bash** `{"command": "cd /tmp && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nr=json.load(open('/tmp/a7-m8-m9.json'))\nm2=r['M9']['M2']\nprint('M2 mode', m2['mode'], '| intacte', {k:round(v,4) for k,v in m2['intacte'].items() if isinstance(v,float)})\nprint('lessee', {k:(round(v,4) if isinstance … [911 caractères tronqués]`

  ```
M2 mode voies | intacte {'action': 0.9863, 'de': 0.9315, 'de_non_nul': 0.9315}
lessee {'action': 0.1233, 'de': 0.0205, 'de_non_nul': 0.0205, 'ventrale': {'action': 0.1233, 'de': 0.9315, 'de_non_nul': 0.9315}, 'dorsale': {'action': 0.9863, 'de': 0.0205, 'de_non_nul': 0.0205}, 'avec_priori': {'action': 0.9863, 'de': 0.4795}}
deficit {'action': 0.863, 'de': 0.911, 'de_non_nul': 0.911, 'majorite': {'action': 0.9863013698630136, 'de': 0.4794520547945205}, 'double_dissociation': True}
par_graine [{'graine': 1, 'intacte': {'action': 0.9863013698630136, 'de': 0.9315068493150684, 'n': 146}, 'ventrale': {'action': 0.1232876712328767, 'de': 0.9315068493150684, 'n': 146}, 'dorsale': {'action': 0.9863013698630136, 'de': 0.02054794520547945, 'n': 146}, 'sham_action': 0.0, 'sham_de': 0.0, 'majorite_action': 0.9863013698630136, 'majorite_de': 0.4794520547945205}]
coh M2 null
coh map null
coh lecture None
coh M8 None
note voies voies.py a été modifié dans l'arbre de travail par un autre sous-agent pendant la session (augmentation/normalisation, défauts inchangés) ; lesion.py et la référence batterie.py utilisent le même fich
erreur KeyError: 'M2_lese_dorsale_de'
seconds 96.66746258735657
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time CUDA_VISIBLE_DEVICES=0 PYTHONPATH=tools /home/stephane/gpu-env/bin/python /tmp/a7_patch.py 2>&1 | tail -45", "description": "Re-patch JSON with reference coherence", "timeoutMs": 900000}`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 964.59it/s]
patché 81530 octets
{
 "batterie_normal": {
  "action": 0.9863013698630136,
  "de": 0.9315068493150684,
  "n": 146
 },
 "lesion_intacte": {
  "action": 0.9863013698630136,
  "de": 0.9315068493150684,
  "de_non_nul": 0.9315068493150684,
  "n": 146
 },
 "batterie_lese_ventrale": {
  "action": 0.1232876712328767,
  "de": 0.9315068493150684,
  "n": 146
 },
 "lesion_ventrale": {
  "action": 0.1232876712328767,
  "de": 0.9315068493150684,
  "de_non_nul": 0.9315068493150684
 },
 "batterie_lese_dorsale": {
  "action": 0.9863013698630136,
  "de": 0.02054794520547945,
  "n": 146
 },
 "lesion_dorsale": {
  "action": 0.9863013698630136,
  "de": 0.02054794520547945,
  "de_non_nul": 0.02054794520547945
 },
 "ecart_de": {
  "batterie": 0.9315068493150684,
  "lesion": 0.9315068493150684
 }
}
[stderr]

real	1m21,710s
user	1m24,212s
sys	0m2,968s
  ```

- **bash** `{"command": "cd /tmp && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nr=json.load(open('/tmp/a7-m8-m9.json'))\nc=r['M9']['coherence_batterie_py']\nprint('M1', c['M1'])\nprint('M3', c['M3']); print('M4', c['M4']); print('M5', c['M5']); print('M6', c['M6'])\nprint('M8', c['M8'])\nprint('ma … [1036 caractères tronqués]`

  ```
M1 {'batterie_exact': 1.0, 'lesion_intacte_exact': 1.0, 'batterie_sans_contexte': 0.7083333333333334, 'lesion_lessee_exact': 0.7083333333333334}
M3 {'batterie_span': 12, 'lesion_span': 12}
M4 {'batterie_rappel': 1.0, 'lesion_intacte_rappel': 1.0}
M5 {'batterie_exact': 0.12454212454212454, 'batterie_majoritaire': 0.08791208791208792, 'lesion_intacte_exact': 0.12454212454212454, 'lesion_lessee_exact': 0.08791208791208792}
M6 {'batterie_exact': 0.9431818181818182, 'lesion_intacte_exact': 0.9431818181818182}
M8 {'batterie_champs': 0.9647798742138365, 'batterie_exact': 0.6509433962264151, 'lesion_queue_champs': 0.9647798742138365, 'lesion_queue_exact': 0.6509433962264151}
map {
 "M1_sans_contexte": {
  "batterie": 0.29166666666666663,
  "lesion_deficit": 0.29166666666666663
 },
 "M2_lese_ventrale_action": {
  "batterie": 0.1232876712328767,
  "lesion_deficit": 0.8630136986301369
 },
 "M2_lese_dorsale_de": {
  "batterie": 0.02054794520547945,
  "lesion_deficit": 0.910958904109589
 },
 "M3_capacite_zero": {
  "batterie": 0,
  "lesion_deficit": 1.0
 },
 "M4_sans_stockage": {
  "batterie": 0.0,
  "lesion_deficit": 1.0
 },
 "M5_sans_transitions": {
  "batterie": 0.9120879120879121,
  "lesion
… [7712 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nr=json.load(open('/tmp/a7-m8-m9.json'))\nc=r['M8']['experience_contexte']\ns=c['codes_tenus_resume']\nprint('ladder_champs', s['ladder_champs'], 'ladder_non_nuls', s['ladder_non_nuls'], 'ladder_exact', s['ladder_exact' … [805 caractères tronqués]`

  ```
ladder_champs 0.8918614718614718 ladder_non_nuls 0.5746591613303037 ladder_exact 0.0
hybride_surface {'couverture': 0.0, 'exact': 0.0, 'exact_sur_couverts': 0.0}
hybride_oracle {'couverture': 0.0, 'exact': 0.0}
paire_oracle_champs 0.7988455988455989
par_cle non-nuls {'global': 0.1518, 'jeu': 0.5499, 'groupe': 0.5108, 'type': 0.513, 'jeu_type': 0.513, 'action_type': 0.513, 'type_seul': 0.513}
par_cle champs {'global': 0.7889, 'jeu': 0.8834, 'groupe': 0.8783, 'type': 0.8788, 'jeu_type': 0.8788, 'action_type': 0.8788, 'type_seul': 0.8788}
per-seed ladder [(1, 0.8903030303030303, 0.5606796116504854, 1.0, {'type': 1650}), (2, 0.8761904761904762, 0.5382978723404256, 0.9880281690140845, {'type': 1605, 'jeu': 285}), (3, 0.9090909090909091, 0.625, 1.0, {'type': 165})]
controles {'groupe': {'champs': 0.8468943402276735, 'exact': 0.0, 'champs_non_nuls': 0.46425669627487437, 'prototypes_fixes': 3.6666666666666665, 'note': 'clé→prototype permutée en cycle dans chaque jeu'}, 'type': {'champs': 0.8480840147506813, 'exact': 0.0, 'champs_non_nuls': 0.5367486056599876, 'prototypes_fixes': 2.3333333333333335, 'note': 'clé→prototype permutée en cycle dans chaque jeu'}}
queue verdict {'champs': 0.96477
… [742 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "    plus_faible = max(champs, key=lambda k: champs[k][\"deficit\"]) if champs else None\n    if plus_faible is not None and champs[plus_faible][\"deficit\"] <= 0.0:\n        # La requête partielle retrouve l'épisod … [1894 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nfrom cerveau.lesion import batterie_lesions\nr=json.load(open('/tmp/a7-m8-m9.json', encoding='utf-8'))\nb=batterie_lesions(rapide=True, m2='proxy')\nr['batterie_lesions']['modu … [905 caractères tronqués]`

  ```
{
 "rappel": 1.0,
 "completion": 0.9866666666666666,
 "par_champ": {
  "de": {
   "n": 7,
   "intacte": 1.0,
   "rappel_lese": 1.0,
   "deficit": 0.0
  },
  "vers": {
   "n": 7,
   "intacte": 1.0,
   "rappel_lese": 1.0,
   "deficit": 0.0
  },
  "roque": {
   "n": 1,
   "intacte": 1.0,
   "rappel_lese": 1.0,
   "deficit": 0.0
  },
  "case": {
   "n": 7,
   "intacte": 1.0,
   "rappel_lese": 1.0,
   "deficit": 0.0
  },
  "symbole": {
   "n": 7,
   "intacte": 1.0,
   "rappel_lese": 1.0,
   "deficit": 0.0
  },
  "carte": {
   "n": 7,
   "intacte": 1.0,
   "rappel_lese": 0.42857142857142855,
   "def
note: échantillon stratifié par jeu ; le champ lésé est mis à None dans la requête. L'intacte par champ vaut 1,0 par construction (le code complet est dans le magasin) et la requête partielle retrouve le même épisode : le déficit par champ est plat, non interprétable.
=== tests lesion proxy ===
----------------------------------------------------------------------
Ran 13 tests in 4.909s

OK
[stderr]

real	0m5,064s
user	0m5,041s
sys	0m0,026s
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "        note=(\"échantillon stratifié par jeu ; le champ lésé est mis à None dans \"\n              \"la requête. L'intacte par champ vaut 1,0 par construction (le code \"\n              \"complet est dans le magas … [709 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nfrom cerveau.lesion import _m4\nr=json.load(open('/tmp/a7-m8-m9.json', encoding='utf-8'))\nm4=_m4(36)  # même échantillon que la batterie rapide\nr['batterie_lesions']['modules … [290 caractères tronqués]`

  ```
{
 "rappel": 1.0,
 "completion": 0.9866666666666666,
 "champ_le_plus_necessaire": "carte",
 "deficit_champ_max": 0.5714285714285714,
 "tautologie_recuperation": true
}
échantillon stratifié par jeu ; le champ lésé est mis à None dans la requête. L'intacte par champ vaut 1,0 par construction (le code complet est dans le magasin). Les champs dont le retrait ne change pas le voisin (de, vers, case, symbole) ont un déficit nul : propriété du magasin (codes uniques), pas une lésion manquée. `carte` est détectable (0,4286) : plusieurs cartes partagent les autres champs, le voisin bascule.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", "new_string": "    plus_faible = max(champs, key=lambda k: champs[k][\"deficit\"]) if champs else None\n    if plus_faible is not None and champs[plus_faible][\"deficit\"] <= 0.0:\n        # La requête partielle retrouve l'épisod … [3257 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && for i in 1 2; do PYTHONPATH=tools /home/stephane/gpu-env/bin/python -c \"\nfrom cerveau.lesion import _m4\nr=_m4(36); d=r['deficit']; print(d['champ_le_plus_necessaire'], round(d['deficit_champ_max'],4), d['completion'], d['rappel'])\n\"; done", "desc … [54 caractères tronqués]`

  ```
carte 0.5714 0.9866666666666666 1.0
carte 0.5714 0.9866666666666666 1.0
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nfrom cerveau.lesion import _m4\nr=json.load(open('/tmp/a7-m8-m9.json', encoding='utf-8'))\nr['batterie_lesions']['modules']['M4']=_m4(36)\njson.dump(r, open('/tmp/a7-m8-m9.json … [255 caractères tronqués]`

  ```
échantillon stratifié par jeu ; le champ lésé est mis à None dans la requête. L'intacte par champ vaut 1,0 par construction (le code complet est dans le magasin). Les champs dont le retrait ne change pas le voisin (de, vers, case, symbole) ont un déficit nul : propriété du magasin (codes uniques), pas une lésion manquée. `carte` est détectable (0.5714) : plusieurs valeurs partagent les autres champs, le voisin bascule.
{'rappel': 1.0, 'completion': 0.9866666666666666, 'champ_le_plus_necessaire': 'carte', 'deficit_champ_max': 0.5714285714285714, 'tautologie_recuperation': True}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nfrom semantique.typed_corpus import items\nfrom cerveau.sommeil import Sommeil\nits=items(); nq=int(len(its)*0.8); trq, teq = its[:nq], its[nq:]\ns=Sommeil(); pp=s.prototypes_m … [684 caractères tronqués]`

  ```
{'champs': 0.9673, 'exact': 0.6698, 'couverture': 0.1981, 'n': 106, 'n_couverts': 21, 'n_non_couverts': 85, 'exact_sur_couverts': 1.0, 'exact_sur_non_couverts': 0.5882, 'champs_sur_non_couverts': 0.9592}
oracle queue {'champs': 1.0, 'exact': 1.0, 'couverture': 1.0, 'n': 106, 'couverts': 106, 'exact_sur_couverts': 1.0, 'champs_sur_couverts': 1.0, 'exact_sur_non_couverts': 0.0, 'champs_sur_non_couverts': 0.0, 'n_non_couverts': 0}
json patched
  ```

- **write** `{"content": "# A7 — M8 (sommeil/consolidation) et M9 (lésions), après les négatifs A2\n\n> Sortie machine : `/tmp/a7-m8-m9.json`. Code modifié : `tools/cerveau/sommeil.py`,\n> `tools/cerveau/lesion.py`, `tools/cerveau/tests/test_sommeil.py`,\n> `tools/cerveau/tests/test_lesion.py`. Aucun commit, auc … [15641 caractères tronqués]`

  ```
Error: cannot modify "/tmp/a7-m8-m9.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/tmp/a7-m8-m9.md", "limit": 5}`

  ```
<path>/tmp/a7-m8-m9.md</path>
<type>file</type>
<content>
1: # A7 — M8/M9, état partiel
2: 
3: > Partiel : exploration terminée, intégration dans `sommeil.py`/`lesion.py` en cours.
4: 
5: ## M8 — le sommeil sur un code tenu à l'écart

(Showing lines 1-5 of 53. Use offset=6 to continue.)
</content>
  ```

- **write** `{"content": "# A7 — M8 (sommeil/consolidation) et M9 (lésions), après les négatifs A2\n\n> Sortie machine : `/tmp/a7-m8-m9.json`. Code modifié : `tools/cerveau/sommeil.py`,\n> `tools/cerveau/lesion.py`, `tools/cerveau/tests/test_sommeil.py`,\n> `tools/cerveau/tests/test_lesion.py`. Aucun commit, auc … [15648 caractères tronqués]`

  ```
<path>/tmp/a7-m8-m9.md</path>
<type>file</type>
<content>
Updated file
</content>
  ```

### 🤖 Assistant

⏵ Validation finale : tests complets, JSON, diff et envoi au parent

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && time CUDA_VISIBLE_DEVICES=0 PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -6", "description": "Final full test suite", "run_in_background": true, "timeoutMs": 900000}`

  ```
started background job bash-1922
  ```

- **bash** `{"command": "cd /tmp && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nr=json.load(open('/tmp/a7-m8-m9.json', encoding='utf-8'))\nprint('sections', list(r))\nprint('M8 sections', list(r['M8']))\nprint('M9 sections', list(r['M9']))\nprint('battery modules', list(r['batterie_lesions']['modu … [409 caractères tronqués]`

  ```
sections ['a7', 'date', 'dispositif', 'M8', 'M9', 'batterie_lesions', 'secondes_mesure', 'date_maj']
M8 sections ['question', 'experience_contexte', 'experience_queue']
M9 sections ['M2', 'M2_par_graine', 'note_voies', 'audit_deficits', 'coherence_batterie_py']
battery modules ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']
coherence ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'batterie_py_M9_vs_deficits', 'lecture']
mode M2 voies
tests? False
size 82553
json ok
=== md ===
312 /tmp/a7-m8-m9.md
# A7 — M8 (sommeil/consolidation) et M9 (lésions), après les négatifs A2

> Sortie machine : `/tmp/a7-m8-m9.json`. Code modifié : `tools/cerveau/sommeil.py`,
> `tools/cerveau/lesion.py`, `tools/cerveau/tests/test_sommeil.py`,
> `tools/cerveau/tests/test_lesion.py`. Aucun commit, aucun autre fichier touché.

**Verdict court.**

- **M8 : négatif net, et cette fois *prouvé*.** Sur un code tenu à l'écart,
  l'exact d'un prototype est **nul par construction** : un prototype ne peut
  rendre qu'un code déjà vu, et le code testé n'est pas dans le train. Le
  96,48 % publié est une **reconstruction intra-code** : ses 106 items de test
  ont tous leur code dans le train (106/106). Le conditionne
… [511 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", "new_string": "- la seule partie gagnée sur un code neuf est le **motif de ``None``** : la clé\n  ``jeu`` porte les champs à 89,20 %, le backoff ``type→groupe→jeu→global`` à\n  90,11 %, mais les champs non nuls ne passent que de … [710 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git diff -- tools/cerveau/lesion.py | head -60 && echo \"...\" && grep -n \"expérience A7\\|A7\" tools/cerveau/sommeil.py | head", "description": "Spot-check lesion diff and sommeil docstring"}`

  ```
diff --git a/tools/cerveau/lesion.py b/tools/cerveau/lesion.py
index a1fcbbcf..e284a48a 100644
--- a/tools/cerveau/lesion.py
+++ b/tools/cerveau/lesion.py
@@ -233,6 +233,13 @@ def _m2_voies(pas: int = 300, graines=(1,), device: str | None = None,
     par_graine = []
     val = []
     for graine in graines:
+        # Les têtes sont initialisées par le RNG torch global : sans graine,
+        # deux exécutions du même protocole diffèrent de 1–2 items. On fixe la
+        # graine pour que la lésion soit reproductible (l'échantillonnage des
+        # données est déjà seedé par `entrainer`).
+        torch.manual_seed(int(graine))
+        if torch.cuda.is_available():
+            torch.cuda.manual_seed_all(int(graine))
         modele_base = AutoModelForCausalLM.from_pretrained(base, dtype=torch.float32)
         m, val = entrainer(modele_base, pas, 32, 64, graine, device, synth=True)
         intact = evaluer(m, val, device)
@@ -408,6 +415,24 @@ def _m4(taille: int = 32) -> dict:
                        "rappel_lese": rappel_lese,
                        "deficit": intacte_champ - rappel_lese}
     plus_faible = max(champs, key=lambda k: champs[k]["deficit"]) if champs else None
… [2184 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-1922", "wait": true, "timeout_ms": 300000}`

  ```
.....................Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 995.81it/s]
................................................................
----------------------------------------------------------------------
Ran 85 tests in 28.162s

OK
[stderr]

real	0m35,484s
user	0m40,378s
sys	0m2,964s
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-1922 (bash: cd /home/stephane/GitHub/Qtrinet && time CUDA_VISIBLE_DEVICES=0 PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -6) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git diff --check -- tools/cerveau/sommeil.py tools/cerveau/lesion.py tools/cerveau/tests/test_sommeil.py tools/cerveau/tests/test_lesion.py; echo \"check=$?\"; python3 - <<'EOF'\nimport re\np='/tmp/a7-m8-m9.md'\ns=open(p).read()\ns=s.replace('**85 tes … [445 caractères tronqués]`

  ```
check=0
md updated
  ```

- **bash** `{"command": "grep -n \"28,2\\|26,7\\|85 tests\" /tmp/a7-m8-m9.md", "description": "Verify MD test time update"}`

  ```
39:| tests | `PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest discover -s tools/cerveau/tests -t tools` → **85 tests OK en 28,2 s** (dont 8 ajoutés ici) |
250:| suite de tests `cerveau` complète | **28,2 s** (85 tests, dont 8 ajoutés ici) |
298:# 85 tests, OK, 28,2 s (M2 réel sur GPU)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git status --short | head -20 && echo \"---\" && git log -1 --oneline && echo \"---\" && ls -l /tmp/a7-m8-m9.json /tmp/a7-m8-m9.md", "description": "Final git status and artifact sizes"}`

  ```
M  docs/en-cours.md
M  docs/roadmap.md
M  reports/rapport-cerveau-corrections.md
 M tools/cerveau/lesion.py
 M tools/cerveau/predictif.py
 M tools/cerveau/sommeil.py
 M tools/cerveau/tests/test_voies.py
 M tools/cerveau/voies.py
---
0632e24f B12 — VERDICT FINAL : M1 SOLIDE ; M5 CONTEXTE POSITIF ; M9 RÉEL ; M3/M4/M6/M7/M8 STRUCTURELS/NÉGATIFS
---
-rw-r--r--. 1 stephane stephane 82695 27 oct 11:21 /tmp/a7-m8-m9.json
-rw-r--r--. 1 stephane stephane 16014 27 oct 11:24 /tmp/a7-m8-m9.md
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git show --stat --oneline HEAD | head -25 && echo \"=== diff HEAD ===\" && git diff --stat HEAD -- tools/cerveau/sommeil.py tools/cerveau/lesion.py tools/cerveau/tests/test_sommeil.py tools/cerveau/tests/test_lesion.py", "description": "Inspect concur … [22 caractères tronqués]`

  ```
0632e24f B12 — VERDICT FINAL : M1 SOLIDE ; M5 CONTEXTE POSITIF ; M9 RÉEL ; M3/M4/M6/M7/M8 STRUCTURELS/NÉGATIFS
 docs/modules-cerveau-langage.md        |  4 ++++
 journal/2026-10-27.md                  |  4 +++-
 journal/2026-10-27_modele.md           | 19 +++++++++++++++++++
 journal/README.md                      |  2 +-
 journal/THEMES.md                      |  1 +
 reports/rapport-cerveau-corrections.md | 25 ++++++++++++++++++-------
 6 files changed, 46 insertions(+), 9 deletions(-)
=== diff HEAD ===
 tools/cerveau/lesion.py  | 31 ++++++++++++++++++++++++++++---
 tools/cerveau/sommeil.py |  2 +-
 2 files changed, 29 insertions(+), 4 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git log --oneline -5 && echo \"---\" && git log --oneline -3 -- tools/cerveau/tests/test_sommeil.py tools/cerveau/tests/test_lesion.py && echo \"---\" && git show HEAD:tools/cerveau/tests/test_sommeil.py | grep -c \"experience_contexte\\|test_backoff\ … [143 caractères tronqués]`

  ```
0632e24f B12 — VERDICT FINAL : M1 SOLIDE ; M5 CONTEXTE POSITIF ; M9 RÉEL ; M3/M4/M6/M7/M8 STRUCTURELS/NÉGATIFS
076a9c8a B12 — M2 : PLUS D'ENTRAÎNEMENT DÉGRADE L'INÉDIT (10,7→9,3/20 À 1 000 PAS)
843fef8c B12 — M9 RÉEL : ACTION 98,6→12,3, DE 91,8→2,05 ; M8 LEAVE-ONE-CODE-OUT EXACT 0
9a3f753d B12 — M5 CONTEXTE : SOURCE +0,626 NAT, CIBLE +0,411 ; M6 SÉLECTEUR 94,95 % MAIS CONFLIT 0
5e9ca5d6 B12 — M5 CONTEXTE : SOURCE DAMES 3,27→2,11 NAT ; CIBLE MORPION 2,20→1,52 (ORACLE)
---
843fef8c B12 — M9 RÉEL : ACTION 98,6→12,3, DE 91,8→2,05 ; M8 LEAVE-ONE-CODE-OUT EXACT 0
530b7043 B12 — STRESS SOUS-AGENTS : M1 SEUL SOLIDE ; M2 VU SEULEMENT ; M3–M8 NÉGATIFS ; M9 PROXY
---
4
1
  ```

- **bash** `{"command": "cd /tmp && /home/stephane/gpu-env/bin/python - <<'EOF'\np='/tmp/a7-m8-m9.md'\ns=open(p).read()\nnote = \"\"\"\n\n---\n\n## État git (constat, pas action)\n\nA7 n'a fait **aucun commit**. Pendant la session, un autre sous-agent a committé\nune partie de l'arbre (par ex. `843fef8c`, qui c … [732 caractères tronqués]`

  ```
note git ajoutée 16306
  identité M4 `par_champ`, mode M2 déclaré (`voies`/`proxy`), préservation
  croisée M2, M8 sur code tenu à l'écart (exact 0, couverture oracle 0,
  couverture surface 0, 106/106 codes vus dans la queue).

Fichiers de sortie : `/tmp/a7-m8-m9.json` (mesures complètes, JSON) et
`/tmp/a7-m8-m9.md` (ce document). Aucun commit.

---

## État git (constat, pas action)

A7 n'a fait **aucun commit**. Pendant la session, un autre sous-agent a committé
une partie de l'arbre (par ex. `843fef8c`, qui contient déjà une version de ces
fichiers) et le parent a mis en index `docs/` et `reports/`. Au moment de la
remise, `git diff HEAD` pour le périmètre A7 :

- `tools/cerveau/lesion.py` : +31/−4 non committés (graine torch du M2 réel,
  note M4 pilotée par la mesure, audit) ;
- `tools/cerveau/sommeil.py` : +2/−1 non committé (docstring A7) ;
- les deux fichiers de tests sont dans `HEAD` ;
- `tools/cerveau/voies.py` et `tools/cerveau/predictif.py` sont modifiés par
  d'autres sous-agents, **pas par A7**.
  ```

- **todo_write** `{"todos": [{"content": "Explorer les corpus et chiffrer le négatif M8 (fait)", "status": "completed"}, {"content": "Implémenter M8 conditionné + tenue à l'écart + hybrides honnêtes dans sommeil.py", "status": "completed"}, {"content": "Implémenter M2 réel voies.py et corriger les déficits dans lesio … [306 caractères tronqués]`

  ```
Updated todo list: 0 pending, 0 in progress, 6 completed.
  ```

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "A7 TERMINÉ. Livrables : /tmp/a7-m8-m9.json (82 Ko, mesures complètes) et /tmp/a7-m8-m9.md (16 Ko, fiche). Code : tools/cerveau/sommeil.py, tools/cerveau/lesion.py, tests/test_sommeil.py, tests/test_lesion.py uniquement. Aucun commit de … [3501 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

### 🤖 Assistant

⏵ Clôture A7 : résumé, chiffres et chemins

## Résumé A7

**M8 — négatif net, et cette fois prouvé.** En leave-one-code-out sur les 29 codes du corpus (528 items), l'exact d'un prototype conditionné est **0,000 à chaque pli, par construction** : il ne peut rendre qu'un code déjà vu, et le code testé n'est pas dans le train. Les 3 graines à codes tenus à l'écart confirment (exact 0, zéro code test vu dans le train).

- Champs : global 74,94 %, `jeu` 89,20 %, `(jeu,action)` 89,20 %, `(jeu,action,type)` 88,97 %, backoff `type→groupe→jeu→global` 90,11 %.
- Non nuls : 4,60 / 61,26 / 59,71 / 59,02 / 63,51 %. Le conditionnement fin **perd** 0,23 pt de champs et 2,24 pts de non nuls ; le backoff ne regagne que le motif de `None` (+0,91 pt de champs, +2,24 pts de non nuls, +4,26 pts de coordonnées).
- Les non nuls justes sont `jeu` 100 %, `action` 93,1 %, `taille` 100 %, `symbole` 75 %, `chemin_0` 66,7 %, `de` 37,5 % (sous-type roque) ; `vers`, `point`, `carte`, `case`, `roque`, `promotion`, `passe` = **0 %**.
- Le 96,48 % / 65,1 % publié est **intra-code** : 106/106 codes de test sont dans le train, l'oracle par paire fait 100 %, et le plafond contextuel corpus vaut 57,95 % — sous le 65,1 %, donc la queue est un sous-ensemble favorable. Le split par paire fuit (61 à 109 items de test sur 108–151 ont un code vu).
- L'hybride historique est **tautologique** (clé = code cible entier) ; clé par surface, couverture 19,81 % sur la queue et **0 %** sur codes tenus.
- Contrôle clé permutée : la clé ne vaut que ~3 pts (87,83 → 84,69 %).

**M9 — le vrai `voies.py` tourne** (GPU Quadro RTX 5000, ~15 s train+éval, 300 pas, graine 1, torch seedé) : intacte action 98,63 / `de` 93,15 ; lésée ventrale 12,33 / 93,15 ; lésée dorsale 98,63 / 2,05 ; déficits `intacte−lésée` **+86,30** et **+91,10** ; double dissociation vraie. Réserve honnête : l'action est constante sur ce sous-ensemble, la majorité vaut 98,63 = le score intact, donc seule la tête `de` est informative.

Cohérence avec `batterie.py` (non modifié) : M1/M2/M3/M4/M5/M6/M8 concordent exactement. Audit : le seul `1−lésée` de `lesion.py` (M4 `par_champ`) est corrigé ; le M9 de `batterie.py` publie des scores bruts, pas des déficits (incohérence chiffrée, non corrigée car hors périmètre).

**Tests** : 85 tests OK en 28,2 s (dont 8 ajoutés), M2 réel inclus. Batterie M1–M8 complète en 26,85 s.

## Chemins

- `/tmp/a7-m8-m9.json` — mesures complètes (M8 LOO/graines/contrôles/queue, M9 M2 réel, cohérence `batterie.py`, audit).
- `/tmp/a7-m8-m9.md` — fiche détaillée, autocritique et ce qui pourrait rendre le résultat faux.

Code modifié : `tools/cerveau/sommeil.py`, `tools/cerveau/lesion.py`, `tools/cerveau/tests/test_sommeil.py`, `tools/cerveau/tests/test_lesion.py`. **Aucun commit de ma part** ; un autre agent a commité pendant la session (`843fef8c`, `0632e24f`), il reste +31/−4 non committés dans `lesion.py` et +2/−1 dans `sommeil.py`. `voies.py` et `predictif.py` ont été modifiés par d'autres sous-agents, pas par A7.

