# Session DSH — relecture

- identifiant : `b80df26d-3dc3-49ea-98b8-fa5a7e0c4cdf`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 09:52:35
- agent : standard


## Tour 1

### 👤 Utilisateur

Nous sommes dans /home/stephane/GitHub/Qtrinet (dépôt Drave), sprint autonome de 24 h. Tu es un sous-agent chargé de stresser M3 (mémoire de travail) et M4 (mémoire épisodique), sans toucher aux modules déjà confiés à d'autres sous-agents.

État mesuré :
- M3 `tools/cerveau/memoire_travail.py` : span 12/12, exact 1,0 ; n-back contrôle 1,0 ; n-back brut très faible (test invalide).
- M4 `tools/cerveau/episodique.py` : rappel 1,0, complétion 97,9 %, séparation 1,0 ; plus proche voisin exact.
- Corpus : `tools/semantique/typed_corpus.items()` (528), `tools/cerveau/sequences.py`, `tools/cerveau/episodique.py`.
- Tests : `PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools`.

Objectif : produire des mesures plus dures, et améliorer ou documenter un négatif.
M3 :
- Construis une tâche d'**interférence** (codes similaires, distracteurs) et une tâche de **span avec bruit** ; mesure exactitude, seuil, et compare à un tampon sans interférence.
- Teste si le tampon sature (capacité 3/5/7/12) ; documente.
M4 :
- Teste la **généralisation** : stocke une partie des épisodes, teste la complétion sur des codes **non stockés** ; mesure champs/exact et compare à M8 (prototypes).
- Teste la **fausse mémoire** (code proche mais différent) et la séparation ; documente.
- Si M4 ne généralise pas, nomme le négatif.

Contraintes :
- Modifie uniquement `tools/cerveau/memoire_travail.py`, `tools/cerveau/episodique.py` et, si nécessaire, `tools/cerveau/tests/test_memoire_travail.py` / `test_episodique.py`. Ne touche pas aux autres fichiers, docs, reports, journal, git.
- N'exécute pas de `git commit`, `git add`, `git checkout`.
- Écris `/tmp/a4-m3-m4.json` et `/tmp/a4-m3-m4.md` (chiffres, commandes, verdicts).
- CPU uniquement. Sois autonome, mesure, autocritique-toi. Réponds avec un résumé concis et les chemins.
Your parent agent id is "f0969e87-af0c-43b1-93cf-f278d9c90846". Before you finish, send your result to that agent with send_message({ agent_id: "f0969e87-af0c-43b1-93cf-f278d9c90846", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

# Directives de l'agent — Drave

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs
> unifiés (**49 portes, 8 chapitres, 172 fichiers / 241 JSON, 52 documents**), chemins archivés
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

⏵ Exploration du dépôt et lecture des modules M3/M4

- **bash** `{"command": "pwd && ls && echo \"---\" && ls tools/cerveau/ && echo \"---\" && ls tools/cerveau/tests/", "description": "List repo and cerveau directory"}`

  ```
/home/stephane/GitHub/Qtrinet
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
test_modules.py
test_pipeline.py
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/memoire_travail.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/memoire_travail.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """M3 — mémoire de travail : maintenir une suite de codes, la relire, la comparer.
3: 
4: Le module est volontairement **structurel** : un tampon borné, un pointeur, une
5: répétition. Il ne promet pas la mémoire du réseau (N5) ; il mesure ce qu'un
6: **bus** peut tenir sans gradient.
7: """
8: from __future__ import annotations
9: 
10: from collections import deque
11: 
12: 
13: class MemoireTravail:
14:     nom = "M3-memoire-travail"
15: 
16:     def __init__(self, capacite: int = 12) -> None:
17:         self.capacite = capacite
18:         self.tampon: deque = deque(maxlen=capacite)
19: 
20:     def charger(self, codes) -> None:
21:         self.tampon.clear()
22:         for c in codes[-self.capacite:]:
23:             self.tampon.append(dict(c))
24: 
25:     def lire(self, i: int):
26:         return self.tampon[i] if 0 <= i < len(self.tampon) else None
27: 
28:     def nback(self, n: int):
29:         if len(self.tampon) <= n:
30:             return None
31:         return self.tampon[-1] == self.tampon[-1 - n]
32: 
33:     def span(self, seque
… [1158 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sequences.py"}`

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
… [1653 caractères tronqués]
  ```


  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/sequences.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """sequences.py — des parties jouées par les règles, pour M3/M5/M8.
3: 
4: Chaque pas porte : le code typé, la surface canonique, le contexte (résumé) et
5: la RSN. Les parties sont déterministes pour une graine donnée.
6: """
7: from __future__ import annotations
8: 
9: import random
10: from dataclasses import dataclass
11: 
12: from jeux.codecs import codec
13: from jeux.regles import dames as D
14: from jeux.regles import echecs as E
15: from jeux.regles import go as G
16: from jeux.regles import morpion as M
17: from jeux.rsn import RSN
18: from semantique.universaux import code_rsn, resume_contexte
19: 
20: 
21: @dataclass(frozen=True)
22: class Pas:
23:     jeu: str
24:     code: dict
25:     surface: str
26:     contexte: str
27:     rsn: RSN
28: 
29: 
30: @dataclass(frozen=True)
31: class Sequence:
32:     jeu: str
33:     pas: tuple[Pas, ...]
34: 
35: 
36: def _surface(jeu: str, rsn: RSN, contexte, fmt: str) -> str:
37:     try:
38:         return codec(jeu).rend(rsn, format=fmt, contexte=contexte)
39:     except Exception:
40:         return ""
4
… [2849 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/semantique/ && echo \"---\" && sed -n 1,120p tools/semantique/typed_corpus.py 2>/dev/null || true", "description": "Inspect semantics package and typed_corpus"}`

  ```
corpus.py
diagnostic.py
entrainer_nvlink.py
entrainer.py
entrainer_type.py
hybride.py
__init__.py
lancer_nvlink.sh
modele.py
normalisation.py
__pycache__
restitution.py
synth_corpus.py
tests
typed_corpus.py
universaux.py
---
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
    for cor
… [2158 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,160p tools/semantique/universaux.py", "description": "Read universaux module"}`

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

- **bash** `{"command": "grep -n \"MemoireTravail\\|Episodique\\|memoire_travail\\|episodique\" -r tools/cerveau/tests/ tools/cerveau/*.py | head -80", "description": "Find M3/M4 usages and tests"}`

  ```
tools/cerveau/tests/test_modules.py:3:from cerveau.memoire_travail import MemoireTravail
tools/cerveau/tests/test_modules.py:4:from cerveau.episodique import Episodique
tools/cerveau/tests/test_modules.py:11:        m = MemoireTravail(5)
tools/cerveau/tests/test_modules.py:14:    def test_episodique(self):
tools/cerveau/tests/test_modules.py:15:        e = Episodique()
tools/cerveau/batterie.py:22:from cerveau.episodique import Episodique  # noqa: E402
tools/cerveau/batterie.py:25:from cerveau.memoire_travail import MemoireTravail  # noqa: E402
tools/cerveau/batterie.py:86:    m = MemoireTravail(12)
tools/cerveau/batterie.py:108:    e = Episodique()
tools/cerveau/batterie.py:129:            e2 = Episodique(); e2.stocker("a", a); e2.stocker("b", b)
tools/cerveau/batterie.py:174:    e = Episodique()
tools/cerveau/batterie.py:188:    seqs0 = MemoireTravail(0)
tools/cerveau/batterie.py:190:    vide = Episodique()
tools/cerveau/episodique.py:26:class Episodique:
tools/cerveau/episodique.py:27:    nom = "M4-episodique"
tools/cerveau/memoire_travail.py:13:class MemoireTravail:
tools/cerveau/pipeline.py:12:from .episodique import Episodique
tools/cerveau/pipeline.py:23:        self.memoire
… [112 caractères tronqués]
  ```

- **bash** `{"command": "wc -l tools/cerveau/tests/*.py && sed -n 1,80p tools/cerveau/tests/test_modules.py", "description": "Inspect existing cerveau tests"}`

  ```
0 tools/cerveau/tests/__init__.py
  29 tools/cerveau/tests/test_bus.py
  24 tools/cerveau/tests/test_modules.py
  27 tools/cerveau/tests/test_pipeline.py
  80 total
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

- **bash** `{"command": "sed -n 1,220p tools/cerveau/batterie.py", "description": "Read batterie harness for M3/M4 baselines"}`

  ```
#!/usr/bin/env python3
"""batterie.py — la batterie M1–M9, exécutée et publiée.

Chaque module renvoie ses mesures ; M9 relit les autres et chiffre ce qu'une
lésion enlève. Aucun score n'est interprété ici : le rapport le fait.
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from jeux.corpus import construire_corpus  # noqa: E402
from jeux.corpus_multilingue import construire_corpus_multilingue  # noqa: E402
from jeux.codecs import codec  # noqa: E402
from semantique.typed_corpus import items  # noqa: E402
from semantique.universaux import code_rsn  # noqa: E402
from cerveau.bus import Bus  # noqa: E402
from cerveau.episodique import Episodique  # noqa: E402
from cerveau.gating import Porte  # noqa: E402
from cerveau.hub import Hub  # noqa: E402
from cerveau.memoire_travail import MemoireTravail  # noqa: E402
from cerveau.neuromodulation import MemoireLimitee, Neuromodulation  # noqa: E402
from cerveau.predictif import Predictif  # noqa: E402
from cerveau.sequences import corpus  # noqa: E402
from cerveau.sommeil import Sommeil  # noqa: E402


def vrai_
… [6858 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,200p tools/cerveau/sommeil.py", "description": "Read M8 sommeil/prototypes module"}`

  ```
#!/usr/bin/env python3
"""M8 — sommeil : rejouer les épisodes, consolider des prototypes.

Le sommeil ne touche pas aux poids du réseau : il **compacte** les épisodes en
prototypes par (jeu, action) et mesure si la complétion d'un code partiel
s'améliore ou se dégrade.
"""
from __future__ import annotations

import collections

from semantique.universaux import CHAMPS


class Sommeil:
    nom = "M8-sommeil"

    def consolider(self, episodes) -> dict:
        groupes = collections.defaultdict(list)
        for e in episodes:
            groupes[(e.code.get("jeu"), e.code.get("action"))].append(e.code)
        prototypes = {}
        for cle, codes in groupes.items():
            proto = {}
            for nom, _ in CHAMPS:
                vals = [c.get(nom) for c in codes]
                proto[nom] = collections.Counter(vals).most_common(1)[0][0]
            prototypes[cle] = proto
        return prototypes

    def evaluer(self, episodes, prototypes) -> dict:
        ok = n = 0
        for e in episodes:
            proto = prototypes.get((e.code.get("jeu"), e.code.get("action")))
            if not proto:
                continue
            n += 1
            ok += sum(1 for no
… [163 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,120p tools/cerveau/pipeline.py && echo \"---\" && sed -n 1,80p tools/cerveau/tests/test_pipeline.py", "description": "Read pipeline usage of M3/M4"}`

  ```
#!/usr/bin/env python3
"""pipeline.py — la chaîne minimale M1 → M4 → M8, sur un seul bus.

Le pipeline ne prétend pas être un cerveau : il vérifie que les modules se
**chaînent** sans se contredire. La surface est perçue par M1, stockée par M4,
résumée par M8 ; la lecture d'un code partiel passe par M4 et, si M8 a consolidé,
par ses prototypes.
"""
from __future__ import annotations

from .bus import Bus
from .episodique import Episodique
from .hub import Hub
from .sommeil import Sommeil


class Pipeline:
    nom = "pipeline-M1-M4-M8"

    def __init__(self) -> None:
        self.bus = Bus()
        self.hub = Hub(self.bus)
        self.memoire = Episodique()
        self.sommeil = Sommeil()
        self.prototypes = {}

    def percevoir(self, texte: str, jeu: str, contexte=None, langue: str = "?"):
        code = self.hub.percevoir(texte, jeu, contexte)
        if code is not None:
            self.memoire.stocker(texte, code, langue)
        return code

    def consolider(self):
        self.prototypes = self.sommeil.consolider(self.memoire.episodes)
        self.bus.publier("prototypes", len(self.prototypes), self.nom)
        return self.prototypes

    def repondre(self, cue
… [1195 caractères tronqués]
  ```

- **bash** `{"command": "PYTHONPATH=tools timeout 300 python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -20", "description": "Run cerveau unit tests baseline"}`

  ```
......
----------------------------------------------------------------------
Ran 6 tests in 0.010s

OK
  ```

- **bash** `{"command": "PYTHONPATH=tools timeout 300 python3 - <<'EOF'\nfrom collections import Counter\nfrom semantique.typed_corpus import items\nits = items()\nprint(\"items\", len(its))\nprint(\"paires\", len({i.paire for i in its}))\ncodes = [tuple(sorted(i.code.items())) for i in its]\nprint(\"codes uniq … [422 caractères tronqués]`

  ```
items 528
paires 31
codes uniques 29
jeux Counter({'cartes': 161, 'echecs': 146, 'go': 87, 'dames': 70, 'morpion': 64})
langues 67
doublons exacts 499
items par paire top [('ml-go-d4', 62), ('ml-echecs-nf3', 61), ('ml-echecs-e4', 61), ('ml-dames-b6c5', 56), ('ml-morpion-a1', 42), ('ml-cartes-10h', 36), ('ml-cartes-ah', 30), ('ml-cartes-jc', 30)]
paires avec 1 item 4
  ```

- **bash** `{"command": "PYTHONPATH=tools timeout 300 python3 - <<'EOF'\nfrom collections import defaultdict\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import CHAMPS\nits = items()\npar_code = defaultdict(list)\nfor i in its:\n    par_code[tuple(sorted(i.code.items()))].append(i)\npr … [381 caractères tronqués]`

  ```
codes uniques 29
55 | morpion jouer_case de None vers None case 0 carte None point None taille None | morpion-a1 | A1
6 | morpion jouer_case de None vers None case 4 carte None point None taille None | morpion-centre | milieu
2 | morpion jouer_case de None vers None case 8 carte None point None taille None | morpion-o-bas-droite | O joue en bas à droite
1 | morpion jouer_case de None vers None case 1 carte None point None taille None | None | B1
69 | echecs deplacer de 52 vers 36 case None carte None point None taille None | echecs-e4 | e2e4
68 | echecs deplacer de 62 vers 45 case None carte None point None taille None | echecs-nf3 | Nf3
2 | echecs deplacer de 60 vers 62 case None carte None point None taille None | echecs-petit-roque | O-O
2 | echecs deplacer de 60 vers 58 case None carte None point None taille None | echecs-grand-roque | O-O-O
1 | echecs deplacer de 28 vers 19 case None carte None point None taille None | echecs-ep | exd6
2 | echecs promouvoir de 8 vers 0 case None carte None point None taille None | echecs-promotion | a8=Q
1 | echecs deplacer de 52 vers 44 case None carte None point None taille None | None | e2e3
1 | echecs deplacer de 57 vers 42 case None carte
… [1784 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | head -40 && grep -ril \"memoire de travail\\|M3\\|M4\\|episodique\" reports/ | head -30", "description": "Find existing M3/M4 reports"}`

  ```
07
07-mesures-couche-commune.md
aiguille-30b.md
aiguille-gpt-oss.md
alignement-3b.json
alignement-7b.json
alignement-verne.md
analyse-litteraire.json
archive
bilan-b11.md
bilan-multi-materiel.md
bruit-entree.json
campagne-benefices
campagne-benefices.md
carte-24langues-3b.json
carte-24langues.json
cca-256-3b.json
cca-raisonnement-3b.json
cerveau-mesures.json
code-partage-256-3b.json
code-partage-64-3b.json
composition-latente-14b.json
composition-latente-3b.json
composition-latente-7b.json
composition-multilingue.json
composition-penalite-3b.json
composition-penalite-7b.json
composition-verne-14b.json
composition-verne-7b.json
composition-verne.json
composition-verne-large.json
composition-verne-plan.json
contamination-0.5b.json
contamination-1.5b.json
contamination-3b.json
contamination-7b.json
contamination-7b-litteral.json
contamination-eurlex-3b.json
contamination-eurlex-7b.json
contamination-udhr-A.json
reports/rapport-engram-etat.md
reports/rapport-v41-mhc.md
reports/archive/rapport-campagne-benefices.md
reports/campagne-benefices/001-R-resume-les-cinq-resultats-qui-comptent-e.md
reports/campagne-benefices/003-00-bis-le-verdict-famille-par-famille.md
reports/campagne-benefice
… [1147 caractères tronqués]
  ```

- **bash** `{"command": "grep -ril \"M3\\|M4\\|mémoire de travail\\|épisodique\" docs/en-cours.md docs/roadmap.md reports/ 2>/dev/null | head -20", "description": "Locate M3/M4 documentation references"}`

  ```
docs/en-cours.md
docs/roadmap.md
reports/rapport-engram-etat.md
reports/rapport-v41-mhc.md
reports/archive/rapport-campagne-benefices.md
reports/campagne-benefices/001-R-resume-les-cinq-resultats-qui-comptent-e.md
reports/campagne-benefices/003-00-bis-le-verdict-famille-par-famille.md
reports/campagne-benefices/005-02-les-deux-familles-de-taches-que-drave-ne.md
reports/campagne-benefices/007-04-ce-que-le-depot-sait-deja-par-famille-de.md
reports/campagne-benefices/009-07-repartir-par-experts-ce-que-couterait-lu.md
reports/campagne-benefices/027-24-memoire-episodique-c6-ce-qui-marche-et-c.md
reports/campagne-benefices.md
reports/rapport-c8-generalisation.md
reports/rapport-raid0-nvme.md
reports/rapport-niah-fragilite.md
reports/rapport-c8-echelle.md
reports/rapport-n4-dessin-b.md
reports/rapport-n4-porte-execution.md
reports/rapport-consolidation-c7.md
reports/rapport-cycle-c2.md
  ```

- **bash** `{"command": "grep -n \"M3\\|M4\\|memoire de travail\\|épisodique\\|episodique\" docs/en-cours.md | head -40", "description": "Read M3/M4 state lines in en-cours"}`

  ```
56:  70,8 %), **M4 mémoire épisodique 1,0** (complétion 97,9 %, séparation 1,0), **M3** tampon 12/12 et n-back contrôle 1,0 ;
60:- **B12 pipeline** — **M1 → M4 → M8** : **528/528** surfaces, **7** prototypes, **96,33 %** de complétion
61:  sur 120 codes partiels ; test d'intégration, pas de généralisation M4.
111:raisonnement sur `z`), **B12.10** (M2 équilibré + contexte, M3 répétitions, M5 ordre 2, M6 conflit, M7 capacité,
  ```

- **bash** `{"command": "cat reports/cerveau-mesures.json 2>/dev/null | head -80", "description": "Read published cerveau measures"}`

  ```
{
 "M1": {
  "items": 528,
  "exact": 1.0,
  "sans_contexte": 0.7083333333333334,
  "canonique": 1.0,
  "invariance": 1.0,
  "evenements": 1584
 },
 "M2": {
  "normal": {
   "action": 0.9863013698630136,
   "de": 0.9315068493150684,
   "n": 146
  },
  "lese_ventrale": {
   "action": 0.0958904109589041,
   "de": 0.9315068493150684,
   "n": 146
  },
  "lese_dorsale": {
   "action": 0.9863013698630136,
   "de": 0.00684931506849315,
   "n": 146
  }
 },
 "M3": {
  "span": 12,
  "span_exact": 1.0,
  "nback1": 0.000630119722747322,
  "nback2": 0.004204625087596356,
  "nback_controle1": 1.0,
  "nback_controle2": 1.0,
  "essais": 1747
 },
 "M4": {
  "rappel": 1.0,
  "completion_champs": 0.9791666666666666,
  "separation": 1.0,
  "n": 528,
  "codes_uniques": 29
 },
 "M5": {
  "exact": 0.9893238434163701,
  "majoritaire": 0.9893238434163701,
  "surprise": 0.01064535311304908,
  "n": 281
 },
 "M6": {
  "exact": 0.7285714285714285,
  "faux_positifs": 1,
  "faux_negatifs": 18,
  "n": 70,
  "cout_commutation": -0.1119909502262443
 },
 "M7": {
  "nouveaux": 439,
  "retention_fixe": 0.03644646924829157,
  "retention_modulee": 0.03644646924829157,
  "capacite": 16,
  "n": 528
 },
 "M8": {
  "champs"
… [460 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Prototypage des mesures dures M3/M4 sur le corpus réel

- **bash** `{"command": "mkdir -p /tmp/a4 && cat > /tmp/a4/proto.py <<'EOF'\nimport json, math, random, statistics\nfrom collections import Counter, defaultdict\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import CHAMPS, vecteur\nfrom cerveau.memoire_travail import MemoireTravail\nfrom … [5726 caractères tronqués]`

  ```
items 528 codes 29
vers None 382 0.7234848484848485
completion_champs attente 0.9815656565656565
codes uniques list 29
train/test codes 24 5
test: [('echecs', 'deplacer', {'jeu': 'echecs', 'action': 'deplacer', 'de': 52, 'vers': 44}), ('echecs', 'deplacer', {'jeu': 'echecs', 'action': 'deplacer', 'de': 57, 'vers': 42}), ('dames', 'prendre', {'jeu': 'dames', 'action': 'prendre', 'chemin_0': 21, 'chemin_1': 17}), ('cartes', 'jouer_carte', {'jeu': 'cartes', 'action': 'jouer_carte', 'carte': 0}), ('cartes', 'jouer_carte', {'jeu': 'cartes', 'action': 'jouer_carte', 'carte': 50})]
episodes train 491
[stderr]
Traceback (most recent call last):
  File "/tmp/a4/proto.py", line 64, in <module>
    comp = e2.completion(cue)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py", line 56, in completion
    e = self.chercher(code_partiel, 1)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py", line 40, in chercher
    q = self._cle(code)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py", line 37, in _cle
    return vecteur(code)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/semantiq
… [156 caractères tronqués]
  ```

### 👤 Utilisateur

Agent f0969e87-af0c-43b1-93cf-f278d9c90846 sent a message: 
Timebox : donne un point de progression maintenant. Écris dès que possible /tmp/a4-m3-m4.json et /tmp/a4-m3-m4.md avec les chiffres obtenus, puis termine. Ne bloque pas sur une amélioration parfaite ; un négatif net suffit.

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "Point A4 M3/M4 (timebox respecté, livraison imminente).\n\nDéjà établi, vérifié sur le corpus : les scores M3/M4 du rapport sont gonflés/tautologiques.\n- M4 : 528 items mais seulement **29 codes uniques** (31 paires, ~18 surfaces par  … [1353 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

- **bash** `{"command": "cd /tmp/a4 && python3 - <<'EOF'\np='proto.py'\ns=open(p).read()\ns=s.replace('for k in active(c):\\n        cue = dict(c); cue[k]=None', 'for k in active(c):\\n        if k in (\"jeu\",\"action\"): continue\\n        cue = dict(c); cue[k]=None')\nopen(p,'w').write(s)\nEOF\nPYTHONPATH=/h … [137 caractères tronqués]`

  ```
items 528 codes 29
vers None 382 0.7234848484848485
completion_champs attente 0.9815656565656565
codes uniques list 29
train/test codes 24 5
test: [('echecs', 'deplacer', {'jeu': 'echecs', 'action': 'deplacer', 'de': 52, 'vers': 44}), ('echecs', 'deplacer', {'jeu': 'echecs', 'action': 'deplacer', 'de': 57, 'vers': 42}), ('dames', 'prendre', {'jeu': 'dames', 'action': 'prendre', 'chemin_0': 21, 'chemin_1': 17}), ('cartes', 'jouer_carte', {'jeu': 'cartes', 'action': 'jouer_carte', 'carte': 0}), ('cartes', 'jouer_carte', {'jeu': 'cartes', 'action': 'jouer_carte', 'carte': 50})]
episodes train 491
held-out partial n 8
exact 0.0
champs 0.9
actifs 0.6666666666666666
rappel held-out exact 0.0
near misses 80
rappel exact sur near-miss (doit etre 0) 0.1625
champs near-miss 0.9441666666666666 correction vers stocke 0.5
[stderr]
Traceback (most recent call last):
  File "/tmp/a4/proto.py", line 115, in <module>
    comp = e4.completion(cue)
  File "/home/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py", line 56, in completion
    e = self.chercher(code_partiel, 1)
  File "/home/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py", line 40, in chercher
    q = self._cle(code)
  File "/home
… [305 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Consolidation des mesures M4 et protocole M3 (interférence, bruit, saturation)

- **bash** `{"command": "cat > /tmp/a4/proto2.py <<'EOF'\nimport json, math, random, statistics\nfrom collections import Counter, defaultdict\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import CHAMPS, vecteur\nfrom cerveau.memoire_travail import MemoireTravail\nfrom cerveau.episodique … [7689 caractères tronqués]`

  ```
items 528 codes 29 paires 31
BASELINE rappel 1.0 completion80 0.9791666666666666 vers_none 0.7234848484848485
SPLIT train_codes 23 test_codes 6 episodes_train 485
  TEST {'jeu': 'cartes', 'action': 'jouer_carte', 'carte': 50}
  TEST {'jeu': 'dames', 'action': 'prendre', 'chemin_0': 21, 'chemin_1': 17}
  TEST {'jeu': 'echecs', 'action': 'deplacer', 'de': 57, 'vers': 42}
  TEST {'jeu': 'echecs', 'action': 'deplacer', 'de': 52, 'vers': 44}
  TEST {'jeu': 'cartes', 'action': 'jouer_carte', 'carte': 0}
  TEST {'jeu': 'morpion', 'action': 'jouer_case', 'case': 4, 'symbole': 'X'}
HELD full rappel exact 0.0 n 6
HELD partial n 10 m4 exact 0.0 m4 champs 0.9 m4 cible 0.3 m4 actifs 0.6833333333333333
HELD partial m8 cible 0.2 m8 champs 0.9066666666666667 m8 actifs 0.6333333333333333
   {'code': {'jeu': 'cartes', 'action': 'jouer_carte', 'carte': 50}, 'blank': 'carte', 'm4_exact': False, 'm4_champs': 0.9333333333333333, 'm4_cible': 0, 'm4_actifs': 0.6666666666666666, 'm4_top': 0.9333333333333332, 'm4_marge': 0.0, 'm8_cible': 0, 'm8_champs': 0.9333333333333333, 'm8_actifs': 0.6666666666666666, 'm8_code': {'jeu': 'cartes', 'action': 'jouer_carte', 'carte': 34}}
   {'code': {'jeu': 'dames', 'actio
… [3937 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/a4/m3.py <<'EOF'\nimport json, random, statistics\nfrom collections import Counter\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import CHAMPS\nfrom cerveau.memoire_travail import MemoireTravail\nfrom cerveau.sequences import corpus\n\nCH = dict(CHAMP … [5430 caractères tronqués]`

  ```
codes uniques 29
SPAN synth {'span': 12, 'essais': 480, 'exact': 1.0} real {'span': 12, 'essais': 1747, 'exact': 1.0}
NBACK brut {'n': 1, 'exact': 0.000630119722747322, 'essais': 1587} {'n': 2, 'exact': 0.004204625087596356, 'essais': 1427}
INTERF cap,L=5 : D -> retention similaires / dissemblables
 cap 3 {0: (0.6, 0.6), 2: (0.2, 0.2), 4: (0.01, 0.0), 6: (0.01, 0.0), 8: (0.0, 0.0), 10: (0.0, 0.0), 12: (0.0, 0.0)}
 cap 5 {0: (1.0, 1.0), 2: (0.6, 0.6), 4: (0.22, 0.2), 6: (0.02, 0.0), 8: (0.0, 0.0), 10: (0.01, 0.0), 12: (0.01, 0.0)}
 cap 7 {0: (1.0, 1.0), 2: (1.0, 1.0), 4: (0.61, 0.6), 6: (0.21, 0.2), 8: (0.01, 0.0), 10: (0.01, 0.0), 12: (0.01, 0.0)}
 cap 12 {0: (1.0, 1.0), 2: (1.0, 1.0), 4: (1.0, 1.0), 6: (1.0, 1.0), 8: (0.8, 0.8), 10: (0.4, 0.4), 12: (0.01, 0.0)}
EFFET SIMILARITE MAX 0.02
 cap 3 premier D avec perte 0 D+L 5
Traceback (most recent call last):
  File "/tmp/a4/m3.py", line 76, in <module>
    first = next((D for D in range(0,20) if rows[(cap,D)][0] < 1.0), None)
  File "/tmp/a4/m3.py", line 76, in <genexpr>
    first = next((D for D in range(0,20) if rows[(cap,D)][0] < 1.0), None)
                                            ~~~~^^^^^^^^^
KeyError: (5, 1)
  ```

- **bash** `{"command": "cd /tmp/a4 && python3 - <<'EOF'\np='m3.py'; s=open(p).read()\ns=s.replace('''        dis.append(d)\n    m = MemoireTravail(cap)''','''        if d in target or d in dis: continue\n        dis.append(d)\n    m = MemoireTravail(cap)''')\ns=s.replace('''    first = next((D for D in range(0 … [343 caractères tronqués]`

  ```
codes uniques 29
SPAN synth {'span': 12, 'essais': 480, 'exact': 1.0} real {'span': 12, 'essais': 1747, 'exact': 1.0}
NBACK brut {'n': 1, 'exact': 0.000630119722747322, 'essais': 1587} {'n': 2, 'exact': 0.004204625087596356, 'essais': 1427}
INTERF cap,L=5 : D -> retention similaires / dissemblables
 cap 3 {0: (0.6, 0.6), 2: (0.2, 0.21), 4: (0.0, 0.0), 6: (0.0, 0.0), 8: (0.0, 0.0), 10: (0.0, 0.0), 12: (0.0, 0.0)}
 cap 5 {0: (1.0, 1.0), 2: (0.6, 0.6), 4: (0.22, 0.25), 6: (0.0, 0.03), 8: (0.0, 0.0), 10: (0.0, 0.0), 12: (0.0, 0.0)}
 cap 7 {0: (1.0, 1.0), 2: (1.0, 1.0), 4: (0.62, 0.7), 6: (0.21, 0.35), 8: (0.01, 0.09), 10: (0.0, 0.03), 12: (0.0, 0.0)}
 cap 12 {0: (1.0, 1.0), 2: (1.0, 1.0), 4: (1.0, 1.0), 6: (1.0, 1.0), 8: (0.84, 0.95), 10: (0.43, 0.74), 12: (0.1, 0.52)}
EFFET SIMILARITE MAX 0.42000000000000004
 cap 3 premier D avec perte 0 D+L 5
 cap 5 premier D avec perte 2 D+L 7
 cap 7 premier D avec perte 4 D+L 9
 cap 12 premier D avec perte 8 D+L 13
BRUIT exact par n (p)
 p 0.0 {1: 1.0, 2: 1.0, 3: 1.0, 5: 1.0, 7: 1.0, 10: 1.0, 12: 1.0}
 p 0.005 {1: 1.0, 2: 0.994, 3: 0.981, 5: 0.95, 7: 0.941, 10: 0.917, 12: 0.9}
 p 0.01 {1: 0.994, 2: 0.969, 3: 0.956, 5: 0.925, 7: 0.908, 10: 0.883, 12
… [1788 caractères tronqués]
  ```

- **bash** `{"command": "PYTHONPATH=/home/stephane/GitHub/Qtrinet/tools timeout 120 python3 - <<'EOF'\nimport random\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import CHAMPS\nfrom cerveau.memoire_travail import MemoireTravail\nCH=dict(CHAMPS)\ncodes,seen=[],set()\nfor it in items():\ … [854 caractères tronqués]`

  ```
len dis 8 len target 5
tampon len 12
target in buf [False, True, True, True, True]
n target 0.8
target positions [0, 1, 2, 3, 4]
buf ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
  ```

### 🤖 Assistant

⏵ Ajout des lectures de reconnaissance M3 et des scores/marges M4, puis tests durs

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/memoire_travail.py", "old_string": "from __future__ import annotations\n\nfrom collections import deque\n\n\nclass MemoireTravail:", "new_string": "from __future__ import annotations\n\nfrom collections import deque\n\nfrom semantique.univer … [47 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/memoire_travail.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/memoire_travail.py", "old_string": "    def charger(self, codes) -> None:\n        self.tampon.clear()\n        for c in codes[-self.capacite:]:\n            self.tampon.append(dict(c))\n\n    def lire(self, i: int):\n        return self.tam … [1479 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/memoire_travail.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py", "new_string": "    def classer(self, code: dict, k: int = 1):\n        \"\"\"Classe les épisodes par similarité cosinus décroissante.\n\n        Renvoie des couples `(score, episode)`, le score restant dans [0, 1] pour\n      … [2926 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -8", "description": "Run cerveau tests after additive changes"}`

  ```
......
----------------------------------------------------------------------
Ran 6 tests in 0.010s

OK
  ```

- **bash** `{"command": "cat > /tmp/a4/final.py <<'EOF'\nimport json, math, random, statistics, time\nfrom collections import Counter\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import CHAMPS\nfrom cerveau.memoire_travail import MemoireTravail\nfrom cerveau.episodique import Episodiqu … [18622 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-1486]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-1486", "wait": true, "timeout_ms": 120000}`

  ```
écrit /tmp/a4-m3-m4.json 80.39 s
M3 span 12 synth 12 nback 0.000630119722747322 1.0
M3 interf cap12 {'0': (1.0, 1.0), '2': (1.0, 1.0), '4': (1.0, 1.0), '6': (1.0, 1.0), '8': (0.8, 0.8), '10': (0.4, 0.4), '12': (0.0, 0.0)}
M3 effet sim 0.0 premier perte {3: 0, 5: 2, 7: 4, 12: 8} proactif 1.0
M3 leurre {'n': 30, 'distance': {0: 4, 1: 15, 5: 2, 2: 8, 3: 1}, 'exact': 0.13333333333333333}
Traceback (most recent call last):
  File "/tmp/a4/final.py", line 384, in <module>
    print("M3 bruit p50", {k: (round(v['mesure'],4), round(v['analytique'],4)) for k,v in p50.items()})
                               ~~~~~^^^^^^^^^^^^^^^
TypeError: type NoneType doesn't define __round__ method
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "PYTHONPATH=/home/stephane/GitHub/Qtrinet/tools python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/a4-m3-m4.json'))\nM3=d['M3']; M4=d['M4']\nprint(\"M3 bruit p50\", M3['bruit']['p50'])\nprint(\"M3 bruit courbes\")\nfor p,c in M3['bruit']['courbes'].items(): print(\" p\",p,{k:round(v, … [1213 caractères tronqués]`

  ```
M3 bruit p50 {'1': {'mesure': None, 'analytique': 0.5}, '2': {'mesure': 0.2875, 'analytique': 0.2928932188134524}, '3': {'mesure': 0.2063380281690141, 'analytique': 0.2062994740159002}, '5': {'mesure': 0.1266666666666667, 'analytique': 0.12944943670387588}, '7': {'mesure': 0.08586387434554973, 'analytique': 0.09427633573609329}, '10': {'mesure': 0.06656050955414014, 'analytique': 0.06696700846319259}, '12': {'mesure': 0.05500000000000001, 'analytique': 0.05612568731830647}}
M3 bruit courbes
 p 0.0 {'1': 1.0, '2': 1.0, '3': 1.0, '5': 1.0, '7': 1.0, '10': 1.0, '12': 1.0}
 p 0.005 {'1': 0.994, '2': 0.99, '3': 0.979, '5': 0.964, '7': 0.956, '10': 0.94, '12': 0.928}
 p 0.01 {'1': 0.99, '2': 0.97, '3': 0.961, '5': 0.936, '7': 0.918, '10': 0.9, '12': 0.868}
 p 0.02 {'1': 0.986, '2': 0.966, '3': 0.945, '5': 0.897, '7': 0.845, '10': 0.792, '12': 0.747}
 p 0.03 {'1': 0.974, '2': 0.943, '3': 0.919, '5': 0.859, '7': 0.797, '10': 0.718, '12': 0.678}
 p 0.05 {'1': 0.945, '2': 0.891, '3': 0.839, '5': 0.745, '7': 0.678, '10': 0.587, '12': 0.525}
 p 0.1 {'1': 0.882, '2': 0.785, '3': 0.703, '5': 0.56, '7': 0.43, '10': 0.325, '12': 0.275}
 p 0.2 {'1': 0.782, '2': 0.64, '3': 0.511, '5': 0.335, '7': 0.
… [6059 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/a4/fix_lure.py <<'EOF'\nimport json, random\nfrom collections import Counter\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import CHAMPS\nfrom cerveau.memoire_travail import MemoireTravail\nCH=dict(CHAMPS)\ndef ck(c): return tuple(sorted(c.items()))\n … [2063 caractères tronqués]`

  ```
n 163 exact 0.0 distance {1: 113, 2: 38, 5: 7, 3: 3, 6: 2} d<=1 0.6932515337423313
updated
  ```

- **bash** `{"command": "cat > /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_memoire_travail.py <<'EOF'\nfrom __future__ import annotations\n\nimport random\nimport unittest\n\nfrom cerveau.memoire_travail import MemoireTravail\nfrom cerveau.sequences import partie\nfrom semantique.universaux import CH … [8645 caractères tronqués]`

  ```
AssertionError: 0.06666666666666665 not less than 1e-12

======================================================================
FAIL: test_marge_depend_de_l_ordre_d_insertion (cerveau.tests.test_episodique.TestEpisodique.test_marge_depend_de_l_ordre_d_insertion)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_episodique.py", line 60, in test_marge_depend_de_l_ordre_d_insertion
    self.assertNotEqual(e1.completion(cue)["code"], e2.completion(cue)["code"])
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: {'jeu': 'echecs', 'action': 'deplacer', 'de': 52, 'vers': 36, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None} == {'jeu': 'echecs', 'action': 'deplacer', 'de': 52, 'vers': 36, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}

-----------------
… [97 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/cerveau/tests/test_episodique.py'\ns=open(p).read()\ns=s.replace('B = code(jeu=\"echecs\", action=\"deplacer\", de=62, vers=45)   # Nf3',\n            'B = code(jeu=\"echecs\", action=\"deplacer\", de=52, vers=45)   # même  … [216 caractères tronqués]`

  ```
..................
----------------------------------------------------------------------
Ran 18 tests in 0.029s

OK
  ```

### 🤖 Assistant

⏵ Rédaction du rapport /tmp/a4-m3-m4.md avec chiffres, commandes et verdicts

- **bash** `{"command": "cat > /tmp/a4-m3-m4.md <<'EOF'\n# A4 — Stress M3 (mémoire de travail) et M4 (mémoire épisodique)\n\nSprint autonome 24 h, CPU seulement, dépôt `Drave` (`/home/stephane/GitHub/Qtrinet`).\nMesures du 2026-10-27. JSON brut : `/tmp/a4-m3-m4.json` ; scripts : `/tmp/a4/final.py`,\n`/tmp/a4/fi … [14613 caractères tronqués]`

  ```
258 /tmp/a4-m3-m4.md
OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\np='/tmp/a4-m3-m4.json'\nd=json.load(open(p))\nd['commandes']={\n 'tests':'PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools',\n 'mesures':'PYTHONPATH=tools python3 /tmp/a4/final.py',\n 'leurr … [2113 caractères tronqués]`

  ```
JSON keys: ['M3', 'M4', 'commandes', 'corpus', 'date', 'duree_s', 'fichiers_modifies', 'limites', 'negatif_nomme', 'tests', 'verdicts']
valid 12393
-rw-r--r--. 1 stephane stephane 16001 27 oct 10:09 /tmp/a4-m3-m4.json
-rw-r--r--. 1 stephane stephane 14921 27 oct 10:09 /tmp/a4-m3-m4.md
----------------------------------------------------------------------
Ran 36 tests in 0.133s

OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls -la tools/cerveau/tests/ && PYTHONPATH=tools timeout 300 python3 -m unittest discover -s tools/cerveau/tests -t tools -v 2>&1 | head -50", "description": "Inspect test discovery duplication"}`

  ```
total 36
drwxr-xr-x. 1 stephane stephane  272 27 oct 10:08 .
drwxr-xr-x. 1 stephane stephane  340 27 oct 10:04 ..
-rw-r--r--. 1 stephane stephane    0 27 oct 08:41 __init__.py
drwxr-xr-x. 1 stephane stephane  458 27 oct 10:09 __pycache__
-rw-r--r--. 1 stephane stephane  942 27 oct 08:56 test_bus.py
-rw-r--r--. 1 stephane stephane 3112 27 oct 10:06 test_episodique.py
-rw-------. 1 stephane stephane 3565 27 oct 10:08 test_gating.py
-rw-r--r--. 1 stephane stephane 5081 27 oct 10:06 test_memoire_travail.py
-rw-r--r--. 1 stephane stephane  772 27 oct 08:56 test_modules.py
-rw-r--r--. 1 stephane stephane  810 27 oct 09:49 test_pipeline.py
-rw-------. 1 stephane stephane 5615 27 oct 10:09 test_predictif.py
test_hub (cerveau.tests.test_bus.TestBus.test_hub) ... ok
test_publier_rejouer (cerveau.tests.test_bus.TestBus.test_publier_rejouer) ... ok
test_code_non_stocke_n_est_pas_generalise (cerveau.tests.test_episodique.TestEpisodique.test_code_non_stocke_n_est_pas_generalise) ... ok
test_cue_ambigu_marge_nulle (cerveau.tests.test_episodique.TestEpisodique.test_cue_ambigu_marge_nulle) ... ok
test_fausse_memoire_du_voisin (cerveau.tests.test_episodique.TestEpisodique.test_fausse_memoire_du_vois
… [3493 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"18 tests\\|7 tests\\|6 tests\\|test_memoire_travail\\|test_episodique\" /tmp/a4-m3-m4.md", "description": "Locate test count references in MD"}`

  ```
235:- Tests : `tools/cerveau/tests/test_memoire_travail.py` (7 tests) et
236:  `test_episodique.py` (6 tests) verrouillent les négatifs (span=capacité, effet similarité
238:  Suite complète : **18 tests OK**.
245:# 18 tests, OK
256:  `tools/cerveau/tests/test_memoire_travail.py` (nouveau),
257:  `tools/cerveau/tests/test_episodique.py` (nouveau).
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\np='/tmp/a4-m3-m4.md'\ns=open(p).read()\ns=s.replace('  Suite complète : **18 tests OK**.', '  Suite découverte : **36 tests OK** au moment de la mesure (13 tests A4 + tests des autres\\n  sous-agents) ; les 13 tests A4  … [691 caractères tronqués]`

  ```
ok
238:  Suite découverte : **36 tests OK** au moment de la mesure (13 tests A4 + tests des autres
239:  sous-agents) ; les 13 tests A4 passent isolément.
246:# 36 tests découverts, OK (dont 13 tests A4)
{'n': 36, 'statut': 'OK', 'tests_A4': 13, 'nouveaux': {'test_memoire_travail.py': 7, 'test_episodique.py': 6}, 'note': 'suite partagée avec les tests des autres sous-agents ; les 13 tests A4 passent'}
M4 ne generalise pas au-dela des codes stockes : table de hachage exacte ; les 97.9% de completion sont de l'identite de doublons (72.35% vers=None + 27.65% a 14/15).
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 300 python3 -m unittest cerveau.tests.test_memoire_travail cerveau.tests.test_episodique 2>&1 | tail -4 && echo \"---\" && PYTHONPATH=tools timeout 300 python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail - … [66 caractères tronqués]`

  ```
----------------------------------------------------------------------
Ran 12 tests in 0.019s

OK
---
Ran 58 tests in 5.063s

OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\np='/tmp/a4-m3-m4.md'; s=open(p).read()\ns=s.replace('`tools/cerveau/tests/test_memoire_travail.py` (7 tests) et\\n  `test_episodique.py` (6 tests)', '`tools/cerveau/tests/test_memoire_travail.py` (6 tests) et\\n  `test_ … [935 caractères tronqués]`

  ```
counts fixed
238:  Suite découverte : **58 tests OK** au dernier passage (12 tests A4 + tests des autres
239:  sous-agents) ; les 12 tests A4 passent isolément.
246:# 58 tests découverts, OK (dont 12 tests A4)
  ```

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "A4 M3/M4 terminé. Livrables : `/tmp/a4-m3-m4.json`, `/tmp/a4-m3-m4.md`. Tests : 12 tests A4 OK ; suite complète découverte 58 OK (les autres sous-agents ont ajouté des tests pendant la session). CPU seulement.\n\nVERDICTS CHIFFRÉS\nM3  … [2918 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

### 🤖 Assistant

⏵ Livraison du rapport M3/M4 et des fichiers de mesures

**Livrables**
- `/tmp/a4-m3-m4.json` — toutes les mesures, courbes, détails et verdicts.
- `/tmp/a4-m3-m4.md` — rapport (protocoles, tableaux, commandes, limites).

**M3 — le 12/12 est tautologique**
- `span=12`, exact 1,0 même avec 40 séquences de **codes aléatoires** : `charger()` copie exactement et `span` ne teste que `n ≤ capacité`. Le n-back « contrôle » à 1,0 vient des 5 premiers items du corpus, qui ont le même code.
- Interférence : 5 cibles + D distracteurs. Similaires (mutants 1 champ) vs dissemblables → **effet 0,0** ; rétention purement FIFO (C=12 : D=8 → 0,8 ; D=10 → 0,4 ; D=12 → 0,0). Proactif → 1,0.
- Bruit : p50(span 12) = **5,5 %** (analytique 5,6 %) ; à p=5 %, champs exacts 99,64 % mais 12 codes exacts 52,5 % → aucune correction d’erreur.
- Saturation : C=3/5/7/12 → span=3/5/7/12, mur net ; débordement = décalage silencieux (0/12 positions originales justes).

**M4 — négatif net : pas de généralisation**
- 528 items → **29 codes uniques**. Le rappel 1,0 est un lookup de doublons ; la complétion 97,9 % se décompose en 72,35 % `vers=None` (15/15) + 27,65 % à 14/15 = 0,9816 : de l’identité.
- Split par code (23 train / 6 test) : codes non stockés rappelés **0/6** ; complétion exacte **0/10** ; **0/7** valeurs de champ inédites. M8 prototypes : **0/7** aussi.
- Fausse mémoire : `exact` strict 0/2412, mais 98,96 % des leurres 1-champ reçoivent une valeur fausse sur le champ modifié. Cue ambigu : marge 0 à 100 %, choix dépendant de l’ordre (55/55). Aucun seuil ne sépare complétion partielle légitime (0,867–0,933) et leurre (0,933).

**Modifications** (additives, existant inchangé) : `memoire_travail.py` (+`pousser`, `distance`, `retrouver`), `episodique.py` (+`classer`, `_marge`, clés `similarite`/`marge`), et les deux nouveaux fichiers de tests (12 tests A4 ; suite complète 58 OK au dernier passage). Aucun git/docs/reports/journal touché.

