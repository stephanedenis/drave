# Session DSH — relecture

- identifiant : `fd4b8df1-abc9-4dd6-94df-fcf484cc9017`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 09:41:21
- agent : standard


## Tour 1

### 👤 Utilisateur

Nous sommes dans /home/stephane/GitHub/Qtrinet (dépôt Drave). Sprint autonome 24 h. Tu es un sous-agent chargé de M7 (neuromodulation), M8 (sommeil/consolidation) et M9 (lésions/ablations) du prototype `tools/cerveau/`.

État actuel mesuré :
- M7 `tools/cerveau/neuromodulation.py` : mémoire bornée 16 places, rétention 3,64 % en FIFO = 3,64 % avec nouveauté ; aucun effet.
- M8 `tools/cerveau/sommeil.py` : prototypes par (jeu, action) ; 96,48 % sur 106 épisodes non stockés, baseline 0 %.
- M9 n'existe pas comme module séparé : la batterie `tools/cerveau/batterie.py` calcule une table de privations.
- Corpus : `tools/semantique/typed_corpus.items()`, `tools/cerveau/sequences.py`, `tools/cerveau/episodique.py`.
- Tests : `PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools`.

Objectif : améliorer ou produire des négatifs nets.
M7 :
- Teste une vraie politique de rétention (capacité, nouveauté, incertitude, récompense) sur une mémoire bornée, avec contrôle apparié ; mesure rétention des nouveaux, des répétés, et l'effet de chaque signal.
- Si aucun signal ne bat FIFO, documente le négatif.
M8 :
- Affine les prototypes (par jeu/action/type, ou prototypes + épisodes), teste sur des épisodes non stockés ; mesure champs, exact, baseline ; compare à 96,48 %.
M9 :
- Crée `tools/cerveau/lesion.py` : un module de lésions par module, avec une fonction `batterie_lesions()` qui produit des privations déclarées et des déficits mesurables (M1 contexte, M2 voies, M3 tampon, M4 épisodique, M5 prédictif, M6 porte, M7 modulation, M8 sommeil).
- Ajoute `tools/cerveau/tests/test_lesion.py` si utile.
- Ne modifie pas `batterie.py`, docs, reports, journal, git.

Contraintes :
- Modifie uniquement `tools/cerveau/neuromodulation.py`, `tools/cerveau/sommeil.py`, `tools/cerveau/lesion.py`, et les tests `test_neuromodulation.py` / `test_sommeil.py` / `test_lesion.py`. Ne touche pas aux autres fichiers.
- N'exécute pas de `git commit`, `git add`, `git checkout`.
- Écris `/tmp/a2-m7-m8-m9.json` et `/tmp/a2-m7-m8-m9.md` (chiffres, commandes, verdicts).
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

⏵ Lecture de l'état du prototype cerveau et des modules M7/M8/M9

- **bash** `{"command": "ls -la tools/cerveau/ && echo \"---TESTS---\" && ls -la tools/cerveau/tests/", "description": "List cerveau prototype files"}`

  ```
total 48
drwxr-xr-x. 1 stephane stephane   300 27 oct 08:45 .
drwxr-xr-x. 1 stephane stephane 12792 27 oct 09:34 ..
-rw-r--r--. 1 stephane stephane  8161 27 oct 09:18 batterie.py
-rw-r--r--. 1 stephane stephane  1674 27 oct 08:41 bus.py
-rw-r--r--. 1 stephane stephane  2455 27 oct 08:44 episodique.py
-rw-r--r--. 1 stephane stephane  1766 27 oct 08:45 gating.py
-rw-r--r--. 1 stephane stephane  1784 27 oct 08:41 hub.py
-rw-r--r--. 1 stephane stephane     0 27 oct 08:41 __init__.py
-rw-r--r--. 1 stephane stephane  2002 27 oct 08:44 memoire_travail.py
-rw-r--r--. 1 stephane stephane  2096 27 oct 09:18 neuromodulation.py
-rw-r--r--. 1 stephane stephane  2641 27 oct 09:18 predictif.py
drwxr-xr-x. 1 stephane stephane   580 27 oct 09:18 __pycache__
-rw-r--r--. 1 stephane stephane  3455 27 oct 08:41 sequences.py
-rw-r--r--. 1 stephane stephane  1372 27 oct 08:45 sommeil.py
drwxr-xr-x. 1 stephane stephane    96 27 oct 08:56 tests
-rw-r--r--. 1 stephane stephane  4062 27 oct 09:15 voies.py
---TESTS---
total 8
drwxr-xr-x. 1 stephane stephane  96 27 oct 08:56 .
drwxr-xr-x. 1 stephane stephane 300 27 oct 08:45 ..
-rw-r--r--. 1 stephane stephane   0 27 oct 08:41 __init__.py
drwxr-xr-x. 1 stephane
… [164 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git status --short | head -50 && echo \"---\" && git log --oneline -5", "description": "Check git status and recent log"}`

  ```
M  docs/en-cours.md
---
d9e7bdaa JOURNAL — RÉGÉNÉRATION APRÈS LE COMMIT DE COHÉRENCE (9 COMMITS DU 27/10, PASSE 2 VISIBLE)
a81c5bd9 DOCS — PASSE 2/2 : COHÉRENCE APPLIQUÉE (49 PORTES, 8 CHAPITRES, 172/241, 52 DOCS) ; 39 CHEMINS, 4 ORPHELINS, B10–B12, REVUE ÉTENDUE
ca31ba8f DOCS — PASSE 1/2 : BANDEAUX DE RÉVISION SUR LES ENTRÉES (49 PORTES, 8 CHAPITRES, 170/241, 52 DOCS)
8cf29faf B12 — M5 ORDRE 2 SANS GAIN, M7 NOUVEAUTÉ PAR SURFACE SANS EFFET ; M6 72,9 %
091203d1 B12 — M2 ACTION 98,6 % / DE 93,2 % (LÉSIONS 19,2 / 3,4) ; M7 NUL À CAPACITÉ 16
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/batterie.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """M7 — neuromodulation : nouveauté, incertitude, récompense.
3: 
4: Les signaux ne changent pas le code ; ils changent le **poids d'écriture** de la
5: mémoire épisodique. On mesure si cela aide le rappel des épisodes nouveaux ou
6: ambigus, et on publie le négatif s'il y en a un.
7: """
8: from __future__ import annotations
9: 
10: from semantique.universaux import CHAMPS
11: 
12: 
13: class Neuromodulation:
14:     nom = "M7-neuromodulation"
15: 
16:     def __init__(self, alpha: float = 0.5, beta: float = 0.5) -> None:
17:         self.alpha = alpha
18:         self.beta = beta
19:         self.vus = set()
20:         self.vus_surface = set()
21: 
22:     def signal(self, code: dict, marge: float = 1.0, recompense: float = 0.0) -> dict:
23:         cle = tuple(code.get(n) for n, _ in CHAMPS)
24:         nouveau = cle not in self.vus
25:         self.vus.add(cle)
26:         nouveaute = 1.0 if nouveau else 0.0
27:         incertitude = max(0.0, 1.0 - marge)
28:         poids = 1.0 + self.alpha * nouveaute + self.beta * incertitude + 0.2 * recompens
… [1241 caractères tronqués]
  ```


  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """M8 — sommeil : rejouer les épisodes, consolider des prototypes.
3: 
4: Le sommeil ne touche pas aux poids du réseau : il **compacte** les épisodes en
5: prototypes par (jeu, action) et mesure si la complétion d'un code partiel
6: s'améliore ou se dégrade.
7: """
8: from __future__ import annotations
9: 
10: import collections
11: 
12: from semantique.universaux import CHAMPS
13: 
14: 
15: class Sommeil:
16:     nom = "M8-sommeil"
17: 
18:     def consolider(self, episodes) -> dict:
19:         groupes = collections.defaultdict(list)
20:         for e in episodes:
21:             groupes[(e.code.get("jeu"), e.code.get("action"))].append(e.code)
22:         prototypes = {}
23:         for cle, codes in groupes.items():
24:             proto = {}
25:             for nom, _ in CHAMPS:
26:                 vals = [c.get(nom) for c in codes]
27:                 proto[nom] = collections.Counter(vals).most_common(1)[0][0]
28:             prototypes[cle] = proto
29:         return prototypes
30: 
31:     def evaluer(self, episodes, prototypes) -> dict:
32:         o
… [453 caractères tronqués]
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

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sequences.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/semantique/universaux.py"}`

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


  ```
<path>/home/stephane/GitHub/Qtrinet/tools/semantique/universaux.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """universaux.py — la base fixe des universaux sémantiques des jeux.
3: 
4: Le protocole libre apprenait un vecteur `z` : il retrouvait l'article, mais ne
5: disait pas **ce qu'il contenait**. Ici, la sortie n'est plus un vecteur libre :
6: c'est un **code typé**, un tuple de champs fixes, chacun avec un vocabulaire fixe.
7: Deux conséquences, et c'est le but :
8: 
9: - l'embedding est **typé** : `jeu=carte`, `action=prendre`, `de=12`, `vers=28` ;
10: - il est **déterministe** : le même code se lit par `argmax`, sans seuil appris.
11: 
12: La base couvre les **coups** des cinq jeux (B5/B6) et les surfaces multilingues
13: (B7). Les champs sont des **universaux du jeu** (agent/action/source/cible/
14: matériel), pas des tokens : un `de` est une case, pas un mot.
15: """
16: from __future__ import annotations
17: 
18: import hashlib
19: import json
20: 
21: JEUX = ("morpion", "echecs", "dames", "go", "cartes")
22: ACTIONS = ("deplacer", "prendre", "promouvoir", "jouer_case", "jouer_carte", "poser", "passer", "autre")
23: PROMOTIONS = (None, "q", "r", "b",
… [5203 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/memoire_travail.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/hub.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/bus.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py"}`

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


  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """M5 — codage prédictif : prédire l'action suivante, mesurer l'erreur.
3: 
4: Un prédicteur de Markov, volontairement simple, sur les séquences de jeu. Il
5: fournit une **prédiction** et une **surprise** ; l'erreur est l'information que le
6: module suivant peut consommer.
7: """
8: from __future__ import annotations
9: 
10: import collections
11: import math
12: 
13: 
14: class Predictif:
15:     nom = "M5-predictif"
16: 
17:     def __init__(self) -> None:
18:         self.transitions = collections.defaultdict(collections.Counter)
19:         self.transitions2 = collections.defaultdict(collections.Counter)
20:         self.majoritaire = {}
21: 
22:     def entrainer(self, sequences) -> None:
23:         for seq in sequences:
24:             pas = [p.code for p in seq.pas]
25:             for i, b in enumerate(pas[1:]):
26:                 a = pas[i]
27:                 self.transitions[(a["jeu"], a["action"])][b["action"]] += 1
28:                 if i > 0:
29:                     self.transitions2[(a["jeu"], pas[i - 1]["action"], a["action"])][b["actio
… [1829 caractères tronqués]
  ```


  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """M6 — porte exécutive : choisir la langue, inhiber l'autre.
3: 
4: Deux langues, une cible, une surface. La porte doit dire si la surface est dans la
5: langue cible. On mesure l'exactitude, les fausses acceptations (inhibition) et le
6: coût de commutation entre cibles.
7: """
8: from __future__ import annotations
9: 
10: from jeux.lexique_multilingue import MULTI
11: 
12: 
13: class Porte:
14:     nom = "M6-gating"
15: 
16:     def langue(self, texte: str) -> str | None:
17:         return MULTI.detecte_langue(texte)
18: 
19:     def executer(self, items, cibles=("fr", "en")) -> dict:
20:         ok = fp = fn = 0
21:         switch_erreurs = 0
22:         switch_n = 0
23:         repeat_erreurs = 0
24:         repeat_n = 0
25:         precedent = None
26:         n = 0
27:         for i, it in enumerate(items):
28:             if it.langue not in cibles:
29:                 continue
30:             n += 1
31:             # cible alternée par paire : commutation explicite
32:             cible = cibles[(i // 4) % 2]
33:             detectee = self.langue(it
… [885 caractères tronqués]
  ```


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
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/bus.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """bus.py — le bus d'événements des modules cerveau-langage.
3: 
4: Un événement est un **fait** typé, horodaté, avec sa source. Le bus le journalise,
5: le pousse aux abonnés et sait le **rejouer**. C'est le contrat minimal qui permet
6: de composer M1–M9 sans les fondre dans un seul bloc.
7: """
8: from __future__ import annotations
9: 
10: from dataclasses import dataclass, field
11: from typing import Any, Callable, Iterator
12: 
13: 
14: @dataclass(frozen=True)
15: class Evenement:
16:     type: str
17:     valeur: Any
18:     source: str
19:     t: int = 0
20:     meta: tuple[tuple[str, Any], ...] = ()
21: 
22:     def vers_dict(self) -> dict:
23:         return {"type": self.type, "source": self.source, "t": self.t,
24:                 "valeur": self.valeur, "meta": dict(self.meta)}
25: 
26: 
27: class Bus:
28:     def __init__(self) -> None:
29:         self.journal: list[Evenement] = []
30:         self.abonnes: dict[str, list[Callable[[Evenement], None]]] = {}
31:         self._t = 0
32: 
33:     def abonner(self, type_: str, f: Callable[[Evenement], No
… [792 caractères tronqués]
  ```


  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """M2 — deux voies : ventrale (quoi) et dorsale (où/comment).
3: 
4: Un même encodeur de surface alimente deux têtes séparées : l'une lit l'**action**
5: (voie ventrale), l'autre la **source** `de` (voie dorsale). On peut léser une tête
6: sans toucher l'autre : c'est la double dissociation minimale.
7: """
8: from __future__ import annotations
9: 
10: import collections
11: import random
12: 
13: import torch
14: import torch.nn as nn
15: import torch.nn.functional as F
16: from transformers import AutoModelForCausalLM
17: 
18: from semantique.entrainer import pad
19: from semantique.normalisation import normaliser
20: from semantique.typed_corpus import decouper, items, octets
21: from semantique.universaux import CHAMPS
22: 
23: 
24: class Voies(nn.Module):
25:     nom = "M2-voies"
26: 
27:     def __init__(self, base: nn.Module):
28:         super().__init__()
29:         self.base = base
30:         self.d_model = int(base.config.hidden_size)
31:         self.ventral = nn.Linear(2 * self.d_model, 8)      # action
32:         self.dorsal = nn.Linear(2 * sel
… [3397 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,120p tools/semantique/typed_corpus.py", "description": "Read typed_corpus head"}`

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

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat tools/cerveau/tests/test_modules.py tools/cerveau/tests/test_bus.py && echo \"---\" && ls tools/cerveau/tests/", "description": "Read existing tests"}`

  ```
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
from __future__ import annotations
import unittest
from cerveau.bus import Bus
from cerveau.hub import Hub
from jeux.regles import echecs as E


class TestBus(unittest.TestCase):
    def test_publier_rejouer(self):
        b = Bus(); vus = []
        b.abonner("sens", lambda e: vus.append(e.valeur))
        b.publier("sens", {"jeu": "echecs"}, "test")
        self.assertEqual(vus, [{"jeu": "echecs"}])
        self.assertEqua
… [569 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -5; echo \"EXIT=$?\"; python3 -c \"import torch, transformers; print(torch.__version__, transformers.__version__)\" 2>&1 | tail -2; ls -d /tmp/natif-600-512-8-al … [72 caractères tronqués]`

  ```
....
----------------------------------------------------------------------
Ran 4 tests in 0.008s

OK
EXIT=0
    ^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'torch'
/tmp/natif-600-512-8-align-s1
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -c \"\nfrom semantique.typed_corpus import items\nits=items()\nprint('n items',len(its))\nimport collections\nprint('jeux',collections.Counter(i.jeu for i in its))\nprint('langues',collections.Counter(i.langue for i in its).mo … [271 caractères tronqués]`

  ```
n items 528
jeux Counter({'cartes': 161, 'echecs': 146, 'go': 87, 'dames': 70, 'morpion': 64})
langues [('fr', 55), ('notation', 31), ('en', 15), ('de', 11), ('es', 11), ('it', 11), ('ja', 11), ('nl', 11)]
paires 31
codes uniques 29
textes uniques 439
exemple ItemType(texte='A1', code={'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 0, 'symbole': 'X', 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}, jeu='morpion', nature='coup', langue='fr', paire='morpion-a1', format='cellule', contexte='morpion etat trait=X taille=3 cases=.,.,.,.,.,.,.,.,.')
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'PY'\nfrom semantique.typed_corpus import items\nfrom cerveau.sommeil import Sommeil\nfrom cerveau.episodique import Episodique\nfrom semantique.universaux import CHAMPS\nimport collections\n\nits = items()\nn = int(len(it … [1123 caractères tronqués]`

  ```
n 528 train 422 test 106 protos 7
{'champs': 0.9647798742138365, 'n': 106, 'prototypes': 7}
groupes train Counter({('cartes', 'jouer_carte'): 136, ('echecs', 'deplacer'): 106, ('morpion', 'jouer_case'): 56, ('dames', 'prendre'): 56, ('go', 'poser'): 51, ('go', 'passer'): 15, ('echecs', 'promouvoir'): 2})
groupes test  Counter({('echecs', 'deplacer'): 38, ('cartes', 'jouer_carte'): 25, ('go', 'poser'): 19, ('dames', 'prendre'): 14, ('morpion', 'jouer_case'): 8, ('go', 'passer'): 2})
codes train 29 test 11
test codes jamais vus 0 / 106
field 0.9647798742138365 exact 0.6509433962264151
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'PY'\nfrom semantique.typed_corpus import items\nfrom cerveau.neuromodulation import MemoireLimitee, Neuromodulation\nits=items()\nfixe=MemoireLimitee(16); mod=Neuromodulation(); module=MemoireLimitee(16)\nvus=set(); nouve … [824 caractères tronqués]`

  ```
nouveaux 439 n 528 fixe 0.03644646924829157 mod 0.03644646924829157
textes uniques 439 occurrences repeat 89
top repeats [('go D4', 35), ('го D4', 7), ('dama b6 c5', 6), ('tic-tac-toe A1', 6), ('pion e2 e4', 6), ('springer g1 f3', 3), ('bonde e2 e4', 3), ('dam b6 c5', 3), ('skakac g1 f3', 3), ('dama karo', 3)]
codes repeats [((('action', 'deplacer'), ('carte', None), ('case', None), ('chemin_0', None), ('chemin_1', None), ('chemin_2', None), ('de', 52), ('jeu', 'echecs'), ('passe', None), ('point', None), ('promotion', None), ('roque', None), ('symbole', None), ('taille', None), ('vers', 36)), 69), ((('action', 'deplacer'), ('carte', None), ('case', None), ('chemin_0', None), ('chemin_1', None), ('chemin_2', None), ('de', 62), ('jeu', 'echecs'), ('passe', None), ('point', None), ('promotion', None), ('roque', None), ('symbole', None), ('taille', None), ('vers', 45)), 68), ((('action', 'poser'), ('carte', None), ('case', None), ('chemin_0', None), ('chemin_1', None), ('chemin_2', None), ('de', None), ('jeu', 'go'), ('passe', None), ('point', 48), ('promotion', None), ('roque', None), ('symbole', None), ('taille', 9), ('vers', None)), 68), ((('action', 'prendre'), ('carte', None), ('
… [546 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls -d .venv venv env 2>/dev/null; which -a python3 python 2>/dev/null; for p in /usr/bin/python3 /usr/local/bin/python3; do echo \"== $p\"; $p -c \"import torch;print(torch.__version__)\" 2>&1 | tail -1; done; ls /tmp | head -30; find / -maxdepth 4 -n … [101 caractères tronqués]`

  ```
/usr/bin/python3
/bin/python3
== /usr/bin/python3
ModuleNotFoundError: No module named 'torch'
== /usr/local/bin/python3
bash: line 1: /usr/local/bin/python3: No such file or directory
ablation_z.py
archiver.txt
attn_step.py
battery-m7.out
battery-m8.out
battery-r13.out
battery-r14.out
campagne24
cerveau-mesures.json
code-c0442c01-a594-432e-b4fc-f3b9ab99002c
com.google.Chrome.pJLsNY
com.google.Chrome.scoped_dir.2yDBH6
commit-b10-abl.txt
commit-b10.txt
commit-b11.txt
commit-b7b8-pass.txt
commit-b7b8.txt
commit-b9-27m.txt
commit-b9-316-610.txt
commit-b9-31m.txt
commit-b9-610-1000.txt
commit-b9-610.txt
commit-b9-910.txt
commit-b9-capacite.txt
commit-b9-fenetre.txt
commit-b9-scale.txt
commit-b9-seuil.txt
commit-b9-transition.txt
commit-b9.txt
commit-contexte.txt
[stderr]
ls: write error: Broken pipe
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"lesion\\|lésion\" --include=*.py tools | head -20; echo \"---reports---\"; ls reports | tail -20; grep -rln \"96.48\\|96,48\" reports docs journal 2>/dev/null | head", "description": "Search existing lesion references and M8 report"}`

  ```
tools/cerveau/batterie.py:5:lésion enlève. Aucun score n'est interprété ici : le rapport le fait.
tools/cerveau/batterie.py:187:    # Les lésions sont des privations déclarées, pas des approximations.
---reports---
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
reports/rapport-programme-evolutif.md
reports/rapport-p0-flux.md
reports/restitution-udhr-flux.json
reports/traduction-udhr-propre-7b-fraeng.json
reports/kfold-pidgin-7b-8bit.json
reports/rapport-cerveau-modules.md
reports/README.md
docs/synthese/index.md
docs/modules-cerveau-langage.md
docs/carte.md
  ```

- **bash** `{"command": "cat /tmp/battery-m7.out 2>/dev/null | head -40; echo ====; cat /tmp/battery-m8.out 2>/dev/null | head -40; echo ====; head -60 /tmp/cerveau-mesures.json", "description": "Read prior battery outputs"}`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights:  89%|████████▉ | 80/90 [00:00<00:00, 791.37it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 833.88it/s]
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
   "jeu": 1.0,
   "de": 0.9315068493150684,
   "n": 146
  },
  "lese_ventrale": {
   "jeu": 0.2465753424657534,
   "de": 0.9315068493150684,
   "n": 146
  },
  "lese_dorsale": {
   "jeu": 1.0,
   "de": 0.02054794520547945,
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
====
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 945.61it/s]
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
   "jeu": 1.0,
   "de": 
… [1663 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"M8\\|sommeil\\|96.48\" reports/rapport-cerveau-modules.md | head -20; echo ====; ls /opt /home/stephane 2>/dev/null | head -20; find /home/stephane -maxdepth 4 -name \"activate\" -path \"*bin*\" 2>/dev/null | head", "description": "Check M8 report and envs"}`

  ```
11:- **M3–M8** : structures déterministes, sans gradient.
27:| **M8** | **0,9648** sur 106 épisodes non stockés ; baseline **0,0** (M4 n'a rien vu) | ✅ |
28:| **M9** | contexte **0,292** ; M2 ventrale **0,096** ; M2 dorsale **0,007** ; M3 **0** ; M4 **0** ; M5 **0,011** ; M6 **0,271** ; M7 **0,036** ; M8 **0** | ✅ table |
38:- **M8** : les 106 épisodes de test sont hors mémoire → 0 % ; les prototypes consolidés → 96,48 %.
48:   ne bat pas la majorité ; la porte est à 70 % ; la neuromodulation ne change rien ; le sommeil dégrade.
49:5. **M8** généralise aux épisodes non stockés : **96,48 %** contre **0 %** ; la consolidation résume, elle ne
61:- **M5–M7** sont des négatifs utiles : ils disent ce qu'un module **ne fait pas**. **M8** est positif sur
72:- **M8** : rejet + prototypes + épisodes, gain hors domaine.
78:  sommeil, batterie, séquences.
====
/home/stephane:
altera_pro
amdgpu-dc0.sh
Applications
Bureau
data
Data13TB
Desktop
Documents
Downloads
etat.sh
FastNVMe
flex
fpga-compat
GitHub
gpu-env
greeter.sh
IA
Images
intelFPGA
/home/stephane/transcription/.venv/bin/activate
/home/stephane/IA/venv-drave/bin/activate
  ```

- **bash** `{"command": "/home/stephane/IA/venv-drave/bin/python3 -c \"import torch, transformers; print(torch.__version__, transformers.__version__)\" 2>&1 | tail -2; ls /home/stephane/gpu-env 2>/dev/null | head", "description": "Check venv-drave for torch"}`

  ```
2.14.1+cu130 5.20.1
bin
external
include
lib
lib64
pyvenv.cfg
share
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,100p reports/rapport-cerveau-modules.md", "description": "Read brain modules report"}`

  ```
# Rapport — modules cerveau-langage M1–M9

> **Objet.** Mesurer les neuf modules du prototype Python, sur les corpus B5/B7 et des parties générées
> par les règles. Aucun résultat n'est extrapolé au moteur Rust ni à un cerveau biologique.

## 1. Dispositif

- **Bus** : événements typés, journal, rejeu.
- **M1** : codec + contexte, code RSN typé.
- **M2** : encodeur `route` gelé, deux têtes (jeu / de), **300 pas sur les surfaces synthétiques**, test sur les 146 surfaces réelles.
- **M3–M8** : structures déterministes, sans gradient.
- **Séquences** : 160 parties (échecs, dames, go, morpion), 12 pas, générées par les règles.
- **Corpus** : 528 coups B5/B7.
- **M9** : privations déclarées.

## 2. Résultats

| module | mesure | verdict |
|---|---|---:|
| **M1** | exact **1,000** ; sans contexte **0,708** ; canonique **1,000** ; invariance **1,000** ; 1 584 événements | ✅ |
| **M2** | `action` **0,9863** ; `de` **0,9315** (n=146) ; lésion ventrale `action` **0,0959**, `de` **0,9315** ; lésion dorsale `action` **0,9863**, `de` **0,0068** | ✅ double dissociation |
| **M3** | span **12/12** ; exact **1,000** ; n-back contrôle **1,000** ; n-back brut **0,0006 / 0,0042** (invalide) | ✅ tampo
… [3295 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls tools/jeux/ && grep -rn \"class .*Lecture\\|niveau\\|marge\\|confiance\" tools/jeux/codecs.py | head -40", "description": "Inspect codecs API for confidence"}`

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
[stderr]
grep: tools/jeux/codecs.py: No such file or directory
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,80p tools/jeux/codecs.py", "description": "Read codecs head"}`

  ```
[stderr]
sed: can't read tools/jeux/codecs.py: No such file or directory
[exit code: 2]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls tools/jeux/codecs/ && grep -rn \"niveau\\|marge\\|confiance\\|class Lecture\" tools/jeux/codecs/*.py | head -30", "description": "Inspect codecs package"}`

  ```
base.py
cartes.py
dames.py
echecs.py
go.py
__init__.py
morpion.py
__pycache__
tools/jeux/codecs/base.py:7:- `lit(surface, niveau)` : de la surface vers une `Lecture` (les quatre couches
tools/jeux/codecs/base.py:10:- `detecte(surface)` : la confiance que cette surface parle de ce jeu.
tools/jeux/codecs/base.py:12:Les niveaux sont **cumulatifs** : 0 ne lit que la forme canonique exacte, 1
tools/jeux/codecs/base.py:66:class Lecture:
tools/jeux/codecs/base.py:75:    niveau: int
tools/jeux/codecs/base.py:84:    confiance: float = 0.0
tools/jeux/codecs/base.py:93:            "jeu": self.jeu, "surface": self.surface, "niveau": self.niveau,
tools/jeux/codecs/base.py:95:            "confiance": round(self.confiance, 4),
tools/jeux/codecs/base.py:111:    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
tools/jeux/codecs/base.py:138:    def lecture(self, texte: str, niveau: int, langue: str | None = None,
tools/jeux/codecs/base.py:145:        return Lecture(self.jeu, texte, niveau, naturel(texte), jetons(texte),
tools/jeux/codecs/base.py:149:                   confiance: float | None = None, ambiguites: Iterable[str] = ()) -> Annotation:
tools/jeux/codecs/base.py:151: 
… [1797 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,60p tools/jeux/codecs/__init__.py", "description": "Read codecs init"}`

  ```
"""Les codecs de jeux : un fichier par jeu, un seul contrat (`base.Codec`)."""
from .base import Arbre, Codec, Lecture, codec, detecte_jeu, lit, rend, tous_les_codecs  # noqa: F401
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'PY'\nimport collections\nfrom semantique.typed_corpus import items\nfrom jeux.codecs import codec\nits=items()\nconf=[]; amb=[]; nuls=0\nfor it in its:\n    try:\n        lec=codec(it.jeu).lit(it.texte, niveau=4, contexte … [390 caractères tronqués]`

  ```
n 528 nuls 0 conf distinctes [(0.95, 252), (1.0, 134), (0.9, 127), (0.0, 8), (0.8, 7)]
ambiguites [(1, 443), (0, 85)]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 60,180p tools/jeux/codecs/base.py", "description": "Read Lecture dataclass"}`

  ```
def vers_dict(self) -> dict:
        return {"genre": self.genre, **{k: v for k, v in self.champs}}


@dataclass
class Lecture:
    """Le résultat d'une lecture : toutes les couches restent visibles.

    `rsn` est la seule chose que l'étage 2 consomme. Les autres champs servent à
    mesurer, annoter et diagnostiquer — jamais à décider d'un coup.
    """

    jeu: str
    surface: str
    niveau: int
    normalise: str
    unites: list[Jeton] = field(default_factory=list)
    arbre: Arbre | None = None
    rsn: RSN | None = None
    candidats: list[RSN] = field(default_factory=list)
    erreurs: list[str] = field(default_factory=list)
    format: str = "inconnu"
    langue: str = "inconnue"
    confiance: float = 0.0
    ambiguites: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return self.rsn is not None and not self.erreurs

    def vers_dict(self) -> dict:
        return {
            "jeu": self.jeu, "surface": self.surface, "niveau": self.niveau,
            "format": self.format, "langue": self.langue,
            "confiance": round(self.confiance, 4),
            "ambiguites": list(self.ambiguites),
            "arbre": self.arbre.vers_dict() if self
… [3700 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Prototypage rapide des politiques de rétention M7 pour calibrer les métriques

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'PY'\nimport collections, random\nfrom semantique.typed_corpus import items\nits=items()\n# ordre naturel\nstream=its\nn=int(len(stream)*0.8)\npre, suf = stream[:n], stream[n:]\nprint('prefix',len(pre),'suffix',len(suf))\n … [968 caractères tronqués]`

  ```
prefix 422 suffix 106
suffix surfaces uniques 95
suffix codes uniques 11
prefix codes uniques 29
top suffix codes [((('action', 'deplacer'), ('carte', None), ('case', None), ('chemin_0', None), ('chemin_1', None), ('chemin_2', None), ('de', 62), ('jeu', 'echecs'), ('passe', None), ('point', None), ('promotion', None), ('roque', None), ('symbole', None), ('taille', None), ('vers', 45)), 19), ((('action', 'deplacer'), ('carte', None), ('case', None), ('chemin_0', None), ('chemin_1', None), ('chemin_2', None), ('de', 52), ('jeu', 'echecs'), ('passe', None), ('point', None), ('promotion', None), ('roque', None), ('symbole', None), ('taille', None), ('vers', 36)), 19), ((('action', 'poser'), ('carte', None), ('case', None), ('chemin_0', None), ('chemin_1', None), ('chemin_2', None), ('de', None), ('jeu', 'go'), ('passe', None), ('point', 48), ('promotion', None), ('roque', None), ('symbole', None), ('taille', 9), ('vers', None)), 19), ((('action', 'prendre'), ('carte', None), ('case', None), ('chemin_0', 8), ('chemin_1', 13), ('chemin_2', None), ('de', None), ('jeu', 'dames'), ('passe', None), ('point', None), ('promotion', None), ('roque', None), ('symbole', None), ('taille', None), ('
… [468 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'PY'\nimport collections, random\nfrom semantique.typed_corpus import items\nfrom jeux.codecs import codec\n\ndef key_surface(it): return it.texte\ndef key_code(it): return tuple(sorted(it.code.items()))\n\ndef run(policy, … [4634 caractères tronqués]`

  ```
distinct surfaces 439 codes 29
fifo             ret_surf=0.0364 ret_code=0.3448 rep_hit=28/67=0.418 suffix_surf=0.094 suffix_code=0.981 distinct_codes=10
lru              ret_surf=0.0364 ret_code=0.3448 rep_hit=28/67=0.418 suffix_surf=0.094 suffix_code=0.981 distinct_codes=10
lfu              ret_surf=0.0364 ret_code=0.3793 rep_hit=34/67=0.507 suffix_surf=0.085 suffix_code=0.981 distinct_codes=11
nouveaute        ret_surf=0.0364 ret_code=0.2759 rep_hit=9/67=0.134 suffix_surf=0.009 suffix_code=0.623 distinct_codes=8
nouveaute_code   ret_surf=0.0364 ret_code=0.5517 rep_hit=23/67=0.343 suffix_surf=0.066 suffix_code=1.000 distinct_codes=16
incertitude      ret_surf=0.0364 ret_code=0.2414 rep_hit=3/67=0.045 suffix_surf=0.000 suffix_code=0.434 distinct_codes=7
recompense       ret_surf=0.0364 ret_code=0.0690 rep_hit=8/67=0.119 suffix_surf=0.019 suffix_code=0.208 distinct_codes=2
oracle surface top16 0.25471698113207547
oracle code top16 1.0
ceiling novel code 16/29 0.5517241379310345 ceiling surface 0.03644646924829157
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'PY'\nimport collections, random, statistics\nfrom semantique.typed_corpus import items\nfrom jeux.codecs import codec\n\nitems_ = items()\nKEY = lambda it: it.texte\nKCODE = lambda it: tuple(sorted(it.code.items()))\nCONF … [4683 caractères tronqués]`

  ```
fifo             ret_surf=0.036 ret_code=0.316 rep_s=0.337 rep_c=0.844 suf_s=0.059 suf_c=0.719
lru              ret_surf=0.036 ret_code=0.316 rep_s=0.337 rep_c=0.844 suf_s=0.059 suf_c=0.719
lfu              ret_surf=0.036 ret_code=0.310 rep_s=0.519 rep_c=0.902 suf_s=0.093 suf_c=0.747
nouveaute        ret_surf=0.036 ret_code=0.332 rep_s=0.100 rep_c=0.737 suf_s=0.008 suf_c=0.707
nouveaute_code   ret_surf=0.036 ret_code=0.552 rep_s=0.265 rep_c=0.988 suf_s=0.043 suf_c=0.905
incertitude      ret_surf=0.036 ret_code=0.215 rep_s=0.140 rep_c=0.355 suf_s=0.016 suf_c=0.330
recompense       ret_surf=0.036 ret_code=0.152 rep_s=0.168 rep_c=0.290 suf_s=0.020 suf_c=0.183
aleatoire        ret_surf=0.036 ret_code=0.298 rep_s=0.347 rep_c=0.861 suf_s=0.057 suf_c=0.716

lru              rep_s     delta=+0.0000 sd=0.0000 wins=0/30
lru              rep_c     delta=+0.0000 sd=0.0000 wins=0/30
lru              suf_s     delta=+0.0000 sd=0.0000 wins=0/30
lru              suf_c     delta=+0.0000 sd=0.0000 wins=0/30
lru              ret_code  delta=+0.0000 sd=0.0000 wins=0/30

lfu              rep_s     delta=+0.1817 sd=0.0408 wins=30/30
lfu              rep_c     delta=+0.0585 sd=0.0267 wins=30/30
lfu      
… [1713 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 -c \"import numpy; print(numpy.__version__)\" 2>&1 | tail -1; PYTHONPATH=tools python3 - <<'PY'\nimport time\nfrom semantique.typed_corpus import items\nfrom cerveau.hub import Hub\nfrom cerveau.episodique import Episodique\nfrom jeux.corpus i … [1022 caractères tronqués]`

  ```
2.5.3
items 528 t 0.019614696502685547
vrais 528
M1 with ctx 1.0 t 0.54
M1 without ctx t 0.47
M4 rappel 1.0 t 21.76
96 queries t 4.059
  ```

### 🤖 Assistant

⏵ Mesures préparatoires M4/M5/M6/M8 (baselines, splits honnêtes)

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'PY'\nimport collections, random, time\nfrom semantique.typed_corpus import items, decouper\nfrom semantique.universaux import CHAMPS\nfrom cerveau.episodique import Episodique\nfrom cerveau.gating import Porte\nfrom cerve … [4147 caractères tronqués]`

  ```
M6 intact {'exact': 0.7, 'faux_positifs': 1, 'faux_negatifs': 20, 'n': 70, 'cout_commutation': -0.1504524886877828}
M6 accepte 0.4714285714285714 P(attendu) 0.471
M6 rejette 0.5285714285714286 P(attendu) 0.471
M6 hasard 0.5285714285714286 P(attendu) 0.471
M6 inverse 0.0 P(attendu) 0.471
M5 intact {'exact': 0.9893238434163701, 'majoritaire': 0.9893238434163701, 'surprise': 0.01064535311304908, 'n': 281}
M5 sans transitions {'exact': 0.9893238434163701, 'majoritaire': 0.9893238434163701, 'surprise': 13.815510557964274, 'n': 281}
M5 sans ordre2 {'exact': 0.9893238434163701, 'majoritaire': 0.9893238434163701, 'surprise': 0.009582168565428317, 'n': 281}
M8 tail (jeu,action) {'n': 106, 'champs': 0.9647798742138365, 'exact': 0.6509433962264151, 'champs_global': 0.7805031446540881, 'exact_global': 0.0, 'champs_parjeu': 0.9610062893081761, 'exact_parjeu': 0.6320754716981132, 'protos': 7}
M8 tail (jeu,action,sig) {'n': 106, 'champs': 0.9647798742138365, 'exact': 0.6509433962264151, 'champs_global': 0.7805031446540881, 'exact_global': 0.0, 'champs_parjeu': 0.9610062893081761, 'exact_parjeu': 0.6320754716981132, 'protos': 9}
M8 tail (jeu) {'n': 106, 'champs': 0.9610062893081761, 'exact': 0.632
… [631 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'PY'\nimport collections, random\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import CHAMPS\n\nits=items(); n=int(len(its)*0.8); tr,te=its[:n],its[n:]\ndef modes(codes):\n    return {nom: collecti … [3105 caractères tronqués]`

  ```
joint prototype: champs 0.9647798742138365 exact 0.6509433962264151
hybride: champs 1.0 exact 1.0 vus 106 / 106
global: champs 0.7805031446540881 exact 0.0
sham groupes mélangés: champs 0.7490566037735849
  champ jeu        1.000
  champ action     1.000
  champ de         0.821
  champ vers       0.821
  champ promotion  1.000
  champ roque      1.000
  champ case       1.000
  champ symbole    1.000
  champ carte      0.830
  champ taille     1.000
  champ point      1.000
  champ passe      1.000
  champ chemin_0   1.000
  champ chemin_1   1.000
  champ chemin_2   1.000
paires seed1: hybride exact 0.722 champs 0.980 vus 109/151
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 68, in <module>
KeyError: ('go', 'passer')
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'PY'\nimport collections\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import CHAMPS\nits=items()\ng=collections.defaultdict(list)\nfor it in its: g[(it.jeu,it.code['action'])].append(it.code)\ndef … [1972 caractères tronqués]`

  ```
jeu        tous=1.000 non_nul=1.000 n_non_nul=528
action     tous=1.000 non_nul=1.000 n_non_nul=528
de         tous=0.860 non_nul=0.493 n_non_nul=146
vers       tous=0.858 non_nul=0.486 n_non_nul=146
promotion  tous=1.000 non_nul=1.000 n_non_nul=2
roque      tous=0.992 non_nul=0.000 n_non_nul=4
case       tous=0.983 non_nul=0.859 n_non_nul=64
symbole    tous=0.996 non_nul=0.969 n_non_nul=64
carte      tous=0.763 non_nul=0.224 n_non_nul=161
taille     tous=1.000 non_nul=1.000 n_non_nul=87
point      tous=0.996 non_nul=0.971 n_non_nul=70
passe      tous=1.000 non_nul=1.000 n_non_nul=17
chemin_0   tous=0.996 non_nul=0.971 n_non_nul=70
chemin_1   tous=0.981 non_nul=0.857 n_non_nul=70
chemin_2   tous=0.994 non_nul=0.000 n_non_nul=3
micro champs non nuls 0.8438775510204082 n 1960
codes uniques 29
dedup code: champs 0.9264367816091954 exact 0.2413793103448276
dedup paire: n 31 champs 0.9397849462365592 exact 0.41935483870967744
in-sample: champs 0.9613636363636363 exact 0.5795454545454546
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat /tmp/natif-600-512-8-align-s1/config.json 2>/dev/null | head -30; du -sh /tmp/natif-600-512-8-align-s1 2>/dev/null", "description": "Inspect base model config"}`

  ```
{
  "architectures": [
    "Qwen3MoeForCausalLM"
  ],
  "attention_bias": false,
  "attention_dropout": 0.0,
  "bos_token_id": null,
  "decoder_sparse_step": 1,
  "dtype": "float32",
  "eos_token_id": null,
  "head_dim": 64,
  "hidden_act": "silu",
  "hidden_size": 512,
  "initializer_range": 0.08,
  "intermediate_size": 512,
  "max_position_embeddings": 512,
  "mlp_only_layers": [],
  "model_type": "qwen3_moe",
  "moe_intermediate_size": 256,
  "norm_topk_prob": true,
  "num_attention_heads": 8,
  "num_experts_per_tok": 2,
  "num_hidden_layers": 8,
  "num_key_value_heads": 4,
  "num_local_experts": 8,
  "output_router_logits": false,
  "pad_token_id": null,
  "rms_norm_eps": 1e-06,
  "rope_parameters": {
    "rope_theta": 10000.0,
121M	/tmp/natif-600-512-8-align-s1
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/IA/venv-drave/bin/python3 - <<'PY'\nimport time\nt=time.time()\nimport torch\nfrom transformers import AutoModelForCausalLM\nprint('imports',round(time.time()-t,2))\nt=time.time()\nm=AutoModelForCausalLM.from_pretrained('/tmp/natif-600- … [172 caractères tronqués]`

  ```
imports 5.99
load 0.51 31.630848 M
[stderr]
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights:  90%|█████████ | 81/90 [00:00<00:00, 796.64it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 875.71it/s]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls tools/semantique/ | head -30 && grep -n \"def items_synth\" -A5 tools/semantique/synth_corpus.py | head -20", "description": "Check synthetic corpus for M2"}`

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
37:def items_synth() -> list[ItemType]:
38-    out: list[ItemType] = []
39-    langues = MULTI.langues
40-    # --- échecs : tous les coups légaux du départ, 3 formes ---
41-    ctx_e = resume_contexte(E.rsn_depuis_position(E.Position.depart()))
42-    pos = E.Position.depart()
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,40p tools/semantique/synth_corpus.py 2>/dev/null; wc -l tools/semantique/synth_corpus.py 2>/dev/null", "description": "Read synth corpus head"}`

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
… [231 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'PY'\nfrom cerveau.neuromodulation import MemoireLimitee\nm=MemoireLimitee(16)\nfor i in range(30): m.stocker(f\"s{i}\", {\"i\":i}, 1.0)\nprint([e[0] for e in m.episodes][:3], '...', [e[0] for e in m.episodes][-3:], 'n',le … [139 caractères tronqués]`

  ```
['s0', 's1', 's2'] ... ['s13', 's14', 's15'] n 16 contient s0 True contient s29 False
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && nohup env PYTHONPATH=tools /home/stephane/IA/venv-drave/bin/python3 - > /tmp/a2-m2-cpu.out 2>&1 <<'PY' &\nimport json, time, torch\nfrom transformers import AutoModelForCausalLM\nfrom cerveau.voies import entrainer, evaluer\nt0=time.time()\nbase=AutoM … [495 caractères tronqués]`

  ```
started 2510988
  ```

### 🤖 Assistant

⏵ Écriture du module M7 (mémoire bornée, politiques, expérience appariée)

- **write** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", "content": "#!/usr/bin/env python3\n\"\"\"M7 — neuromodulation : nouveauté, incertitude, récompense, rétention bornée.\n\nLe module ne change pas le code : il change le **poids d'écriture** dans une\nmémoire épisodique b … [26526 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

### 👤 Utilisateur

Agent f0969e87-af0c-43b1-93cf-f278d9c90846 sent a message: 
Timebox : donne un point de progression maintenant. Écris dès que possible /tmp/a2-m7-m8-m9.json et /tmp/a2-m7-m8-m9.md (même partiels), puis termine. Ne bloque pas sur une amélioration parfaite ; un négatif net suffit.

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "POINT M7/M8/M9 (en cours, fichiers partiels /tmp écrits dans ~15 min).\n\nAcquis mesurés sur le corpus réel (528 items, 29 codes, 439 surfaces) :\n- M7 : le banc historique est faux sur deux points. (1) `MemoireLimitee.stocker` trie pa … [1764 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 300 python3 - <<'PY'\nimport json, time\nfrom cerveau.neuromodulation import experience_m7, preparer_flux\nt=time.time(); ep=preparer_flux(); print('flux',len(ep),'t',round(time.time()-t,2))\nt=time.time(); r=experience_m7(ep, … [856 caractères tronqués]`

  ```
flux 528 t 0.59
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", line 454, in experience_m7
    resultat["controle_synthetique"] = controle_synthetique(
                                       ~~~~~~~~~~~~~~~~~~~~^
        ep, permutations=max(8, permutations // 2), graine=graine + 1000)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", line 526, in controle_synthetique
    flux, chauds = _flux_zipf(episodes, 528, capacite, graine + k)
                   ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", line 498, in _flux_zipf
    codes = sorted(par_code)
TypeError: '<' not supported between instances of 'int' and 'NoneType'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib\np=pathlib.Path('tools/cerveau/neuromodulation.py')\ns=p.read_text()\ns=s.replace(\"    codes = sorted(par_code)\\n\", \"    codes = sorted(par_code, key=repr)\\n\")\nold='''    # contrôle nul : le FIFO contre lui- … [2077 caractères tronqués]`

  ```
patched
exp t 2.14
{
 "meilleur_suffixe_code": "lfu_code",
 "meilleur_repetes": "lfu",
 "signaux_qui_battent_fifo_suffixe": [],
 "signaux_qui_battent_fifo_repetes": [],
 "plafond_surface_atteint_par_toutes": true,
 "gel_egal_fifo_sur_la_metrique_historique": true,
 "nouveaute_code_egale_fifo_code": false
}
fifo {'ret_surface_finale': 0.036, 'ret_code': 0.312, 'rep_surface': 0.294, 'rep_code': 0.761, 'suf_surface': 0.055, 'suf_code': 0.714}
gel {'ret_surface_finale': 0.036, 'ret_code': 0.352, 'rep_surface': 0.385, 'rep_code': 0.777, 'suf_surface': 0.051, 'suf_code': 0.742}
lru {'ret_surface_finale': 0.036, 'ret_code': 0.316, 'rep_surface': 0.339, 'rep_code': 0.767, 'suf_surface': 0.055, 'suf_code': 0.718}
lfu {'ret_surface_finale': 0.036, 'ret_code': 0.316, 'rep_surface': 0.538, 'rep_code': 0.78, 'suf_surface': 0.09, 'suf_code': 0.749}
nouveaute {'ret_surface_finale': 0.036, 'ret_code': 0.33, 'rep_surface': 0.109, 'rep_code': 0.747, 'suf_surface': 0.011, 'suf_code': 0.7}
nouveaute_code {'ret_surface_finale': 0.036, 'ret_code': 0.581, 'rep_surface': 0.15, 'rep_code': 0.587, 'suf_surface': 0.01, 'suf_code': 0.204}
fifo_code {'ret_surface_finale': 0.036, 'ret_code': 0.581, 'rep_surface
… [2299 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/cerveau/neuromodulation.py')\ns=p.read_text()\nold='''    configs = [c for c in _configurations()\n               if c[\"nom\"] in (\"fifo\", \"lfu\", \"nouveaute\", \"recompense\",\n             … [2457 caractères tronqués]`

  ```
patched
exp t 4.71
{
 "meilleur_suffixe_code": "lfu_code",
 "meilleur_repetes": "lfu",
 "signaux_qui_battent_fifo_suffixe": [],
 "signaux_qui_battent_fifo_repetes": [],
 "plafond_surface_atteint_par_toutes": true,
 "gel_egal_fifo_sur_la_metrique_historique": true,
 "nouveaute_code_egale_fifo_code": false
}
{
 "lfu_bat_fifo": true,
 "recompense_informative_bat_fifo": true,
 "hasard_non_significatif": true
}
  fifo {'suf_surface': 0.239, 'suf_code': 0.504, 'ret_code': 0.225}
  fifo_code {'suf_surface': 0.226, 'suf_code': 0.547, 'ret_code': 0.279}
  lfu_code {'suf_surface': 0.269, 'suf_code': 0.682, 'ret_code': 0.279}
  nouveaute_code {'suf_surface': 0.126, 'suf_code': 0.213, 'ret_code': 0.279}
  recompense_code {'suf_surface': 0.272, 'suf_code': 0.7, 'ret_code': 0.279}
  hasard {'suf_surface': 0.232, 'suf_code': 0.492, 'ret_code': 0.235}
oracle {'suf_surface': {'moyenne': 0.24276729559748428, 'ecart_type': 0.032105437161864384, 'min': 0.18867924528301888, 'max': 0.330188679245283, 'n': 30}, 'suf_code': {'moyenne': 0.9849056603773586, 'ecart_type': 0.015786038236491988, 'min': 0.9433962264150944, 'max': 1.0, 'n': 30}}
plafonds {'surface_finale': 0.03644646924829157, 'code': 0.55172413
… [50 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'PY'\nimport json, time\nfrom cerveau.neuromodulation import experience_m7, preparer_flux\nt=time.time(); ep=preparer_flux(); r=experience_m7(ep, permutations=30, synthetique=True)\nout={\"meta\":{\"date\":time.strftime('% … [3329 caractères tronqués]`

  ```
written 4.7 s
-rw-r--r--. 1 stephane stephane 77657 27 oct 10:01 /tmp/a2-m7-m8-m9.json
[stderr]
  File "<stdin>", line 19
    L.append(f"\n### Verdict M7\n\n- `{r['verdict']}`\n- La métrique historique 3,64 % est le plafond 16/439 : **toutes** les politiques l'atteignent (`plafond_surface_atteint_par_toutes`) ; elle ne peut pas départager deux politiques.\n- `gel` (ancien `MemoireLimitee`) et `fifo` donnent le même 3,64 % mais ne gardent pas les mêmes épisodes ; le comparateur historique n'était pas FIFO.\n- Aucun signal neuromodulateur ne bat FIFO sur le suffixe ni sur les répétés. Le meilleur suffixe code est `lfu_code` (fréquence + clé code), le meilleur répétés est `lfu` : c'est la **fréquence**, pas la modulation, qui porte le gain.\n- L'incertitude (1−confiance codec) et la récompense (proxy `prendre`/`promouvoir`) **dégradent** fortement (jusqu'à −52 pts de suffixe code).\n\n')
             ^
SyntaxError: unterminated f-string literal (detected at line 19)
head: cannot open '/tmp/a2-m7-m8-m9.md' for reading: No such file or directory
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nr=json.load(open('/tmp/a2-m7-m8-m9.json'))['M7']\nL=[]\nL.append(\"# A2 — M7/M8/M9 (partiel : M7 mesuré)\\n\\n\")\nL.append(\"> Sous-agent M7/M8/M9, CPU uniquement. JSON complet : `/tmp/a2-m7-m8-m9.json`.\\n\\n\")\nL.app … [3238 caractères tronqués]`

  ```
md written 4290
# A2 — M7/M8/M9 (partiel : M7 mesuré)

> Sous-agent M7/M8/M9, CPU uniquement. JSON complet : `/tmp/a2-m7-m8-m9.json`.

## M7 — rétention bornée et neuromodulation

### Protocole

- Flux : `semantique.typed_corpus.items()`, n=528, préfixe=422, suffixe=106, capacité=16, 30 permutations appariées (même ordre pour toutes les politiques).
- Mémoire gelée à la fin du préfixe ; le suffixe est interrogé sans réécriture.
- Plafonds : surface finale 3.6446% (16/439), code 55.17% (16/29).

### Moyennes (30 permutations)

| politique | ret. surface finale | ret. code | répétés surface | répétés code | suffixe surface | suffixe code |
|---|---:|---:|---:|---:|---:|---:|
| fifo | 0.0364 | 0.3343 | 0.2874 | 0.7611 | 0.0503 | 0.7170 |
| lru | 0.0364 | 0.3356 | 0.3370 | 0.7659 | 0.0594 | 0.7189 |
| lfu | 0.0364 | 0.3296 | 0.5187 | 0.7734 | 0.0928 | 0.7469 |
| gel | 0.0364 | 0.3437 | 0.4121 | 0.7858 | 0.0667 | 0.7506 |
| nouveaute | 0.0364 | 0.3515 | 0.0915 | 0.7472 | 0.0082 | 0.7060 |
| incertitude | 0.0364 | 0.2272 | 0.1336 | 0.3712 | 0.0164 | 0.3296 |
| recompense | 0.0364 | 0.1622 | 0.1530 | 0.3050 | 0.0170 | 0.1843 |
| combine | 0.0364 | 0.2893 | 0.2294 | 0.4536 | 0.0393 | 0.462
… [466 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Écriture du module M8 (prototypes, baselines, hybride, splits honnêtes)

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"M8 — sommeil : consolider des épisodes en prototypes, et mesurer ce que cela vaut.\n\nLe module d'origine groupait par ``(jeu, action)`` et prenait le mode **champ par\nchamp**. Le score publié, 96,48 % sur 106 épisodes de test, est réel mais il est\nmal lu … [15244 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/cerveau/sommeil.py')\ns=p.read_text()\nold='''        # plafond triché : prototype par paire (l'étiquette paire n'est pas\n        # disponible au test, c'est une borne supérieure, pas une baseli … [3822 caractères tronqués]`

  ```
patched
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", line 351, in experience_m8
    return Sommeil().experience(items_)
           ~~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/sommeil.py", line 281, in experience
    codes = sorted({tuple(sorted(_code(e).items())) for e in its})
TypeError: '<' not supported between instances of 'NoneType' and 'int'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/cerveau/sommeil.py')\ns=p.read_text().replace(\"codes = sorted({tuple(sorted(_code(e).items())) for e in its})\",\n                        \"codes = sorted({tuple(sorted(_code(e).items())) for e  … [1159 caractères tronqués]`

  ```
ok
t 0.25
{
 "champs_96_48_reproduit": true,
 "exact_queue": 0.6509433962264151,
 "exact_annonce_0_est_faux": true,
 "gain_sur_par_jeu_champs": 0.0037735849056603765,
 "gain_sur_par_jeu_exact": 0.018867924528301883,
 "champs_non_nuls": 0.8596491228070176,
 "exact_codes_uniques": 0.2413793103448276,
 "exact_codes_nouveaux": [
  0.0,
  0.0,
  0.0
 ],
 "hybride_exact_queue": 1.0,
 "hybride_couverture_queue": 1.0,
 "hybride_exact_codes_nouveaux": [
  0.0,
  0.0,
  0.0
 ],
 "baseline_globale_champs": 0.7805031446540881,
 "baseline_globale_exact": 0.0,
 "groupes_melanges_champs": 0.8283018867924529
}
module_champs {'champs': 0.9648, 'exact': 0.6509, 'champs_non_nuls': 0.8596, 'n': 106, 'n_inconnus': 0, 'n_champs_non_nuls': 399, 'prototypes': 7}
module_joint {'champs': 0.9648, 'exact': 0.6509, 'champs_non_nuls': 0.8596, 'n': 106, 'n_inconnus': 0, 'n_champs_non_nuls': 399, 'prototypes': 7}
module_type {'champs': 0.9648, 'exact': 0.6509, 'champs_non_nuls': 0.8596, 'n': 106, 'n_inconnus': 0, 'n_champs_non_nuls': 399, 'prototypes': 9}
dedup_code {'champs': 0.9636, 'exact': 0.5455, 'champs_non_nuls': 0.8462, 'n': 11, 'n_inconnus': 0, 'n_champs_non_nuls': 39, 'prototypes': 7}
dedup_paire {'cham
… [1295 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Écriture de M9 (`lesion.py`) : privations par module, sham, dose-réponse, contrôles

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"M9 — lésions par module : privations déclarées et déficits mesurés.\n\nUne lésion n'est pas une approximation : c'est une **privation déclarée** du\nmodule, mesurée sur le même test que la version intacte, avec un **sham** (la\nmême mesure répétée sans priv … [20848 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/cerveau/lesion.py')\ns=p.read_text()\nold='''    vide = Episodique()\n    intact = sum(plein.rappel(it.code)[\"exact\"] for it in echantillon) / len(echantillon)\n    sans = sum(vide.rappel(it.co … [2079 caractères tronqués]`

  ```
patched
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", line 443, in batterie_lesions
    m4 = _m4(24 if rapide else 64)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", line 242, in _m4
    ok += int(plein.rappel(cue)["exact"])
              ~~~~~~~~~~~~^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py", line 70, in rappel
    e = self.chercher(code, 1)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py", line 59, in chercher
    return [e for _, e in self.classer(code, k)]
                          ~~~~~~~~~~~~^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py", line 47, in classer
    q = self._cle(code)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/episodique.py", line 37, in _cle
    return vecteur(code)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/semantique/universaux.py", line 105, in vecteur
    out[base + INDEX[nom][code.get(nom)]] = 1
               ~~~~~~~~~~^^^^^^^^^^^
… [34 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git status --short && sed -n 1,120p tools/cerveau/episodique.py", "description": "Inspect concurrently modified episodique"}`

  ```
M journal/2026-10-27_sprint-24h.md
 M tools/cerveau/episodique.py
 M tools/cerveau/gating.py
 M tools/cerveau/memoire_travail.py
 M tools/cerveau/neuromodulation.py
 M tools/cerveau/predictif.py
 M tools/cerveau/sommeil.py
 M tools/cerveau/voies.py
?? tools/cerveau/lesion.py
#!/usr/bin/env python3
"""M4 — mémoire épisodique adressable par contenu.

Chaque épisode est (surface, code, langue, paire). La clé est le one-hot du code
typé ; la lecture est un plus proche voisin. On mesure le rappel exact, la
complétion sur un code partiel et la séparation de codes voisins.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from semantique.universaux import CHAMPS, vecteur


@dataclass
class Episode:
    surface: str
    code: dict
    langue: str = "?"
    paire: str = ""
    poids: float = 1.0
    meta: dict = field(default_factory=dict)


class Episodique:
    nom = "M4-episodique"

    def __init__(self) -> None:
        self.episodes: list[Episode] = []

    def stocker(self, surface: str, code: dict, langue: str = "?", paire: str = "",
                poids: float = 1.0) -> None:
        self.episodes.append(Episode(surface, dict(code), lang
… [2405 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git diff --stat && grep -n \"def vecteur\\|def index_code\\|INDEX\" tools/semantique/universaux.py | head", "description": "Check diffs and universaux"}`

  ```
journal/2026-10-27_sprint-24h.md |   2 +
 tools/cerveau/episodique.py      |  31 ++-
 tools/cerveau/gating.py          | 450 ++++++++++++++++++++++++++++---
 tools/cerveau/memoire_travail.py |  27 ++
 tools/cerveau/neuromodulation.py | 555 +++++++++++++++++++++++++++++++++++++--
 tools/cerveau/predictif.py       | 426 ++++++++++++++++++++++++++----
 tools/cerveau/sommeil.py         | 358 +++++++++++++++++++++++--
 tools/cerveau/voies.py           | 421 +++++++++++++++++++++++++----
 8 files changed, 2092 insertions(+), 178 deletions(-)
47:INDEX = {nom: {val: i for i, val in enumerate(vals)} for nom, vals in CHAMPS}
96:def index_code(code: dict) -> dict[str, int]:
97:    return {nom: INDEX[nom][code.get(nom)] for nom, _ in CHAMPS}
100:def vecteur(code: dict) -> list[int]:
105:        out[base + INDEX[nom][code.get(nom)]] = 1
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'PY'\nfrom semantique.universaux import CHAMPS, vecteur\nfor nom, vals in CHAMPS:\n    print(nom, None in vals, len(vals))\ncode={nom:None for nom,_ in CHAMPS}\ntry:\n    v=vecteur(code); print('ok',sum(v))\nexcept Excepti … [84 caractères tronqués]`

  ```
jeu False 5
action False 8
de True 65
vers True 65
promotion True 5
roque True 3
case True 10
symbole True 3
carte True 53
taille True 5
point True 82
passe True 3
chemin_0 True 65
chemin_1 True 65
chemin_2 True 65
ERR None
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"^    def \\|^def \\|^class \" tools/cerveau/memoire_travail.py tools/cerveau/predictif.py tools/cerveau/gating.py | head -60", "description": "Check current APIs of M3/M5/M6"}`

  ```
tools/cerveau/memoire_travail.py:15:class MemoireTravail:
tools/cerveau/memoire_travail.py:18:    def __init__(self, capacite: int = 12) -> None:
tools/cerveau/memoire_travail.py:22:    def charger(self, codes) -> None:
tools/cerveau/memoire_travail.py:27:    def pousser(self, code: dict) -> None:
tools/cerveau/memoire_travail.py:35:    def lire(self, i: int):
tools/cerveau/memoire_travail.py:38:    def distance(self, a: dict, b: dict) -> int:
tools/cerveau/memoire_travail.py:42:    def retrouver(self, code: dict):
tools/cerveau/memoire_travail.py:55:    def nback(self, n: int):
tools/cerveau/memoire_travail.py:60:    def span(self, sequences) -> dict:
tools/cerveau/memoire_travail.py:76:    def nback_scores(self, sequences, n: int = 1) -> dict:
tools/cerveau/predictif.py:45:def valeur(pas, cible: str = "cible"):
tools/cerveau/predictif.py:77:def champ_cible(code: dict, cible: str) -> str | None:
tools/cerveau/predictif.py:96:class Predictif:
tools/cerveau/predictif.py:106:    def __init__(self, cible: str = "cible", ordre: int = 1, kappa: float = 10.0) -> None:
tools/cerveau/predictif.py:120:    def entrainer(self, sequences) -> None:
tools/cerveau/predictif.py:140:    def distrib
… [2095 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,40p tools/cerveau/predictif.py && sed -n 1,30p tools/cerveau/gating.py", "description": "Read predictif/gating heads"}`

  ```
#!/usr/bin/env python3
"""M5 — codage prédictif : prédire une cible **variable**, mesurer l'erreur.

Leçon mesurée (sprint 24 h, corpus `sequences.corpus`) : l'ancienne cible
`action` est **structurellement constante** par jeu — `action()` dans
`universaux.py` classe le coup par la *forme* du code (présence de `de`/`vers`,
de `chemin`, de `case`…), pas par sa sémantique. Résultat : échecs = toujours
`deplacer`, dames = toujours `prendre`, morpion = toujours `jouer_case` ; seul go
varie (`poser` 92 %, `passer` 8 %). Prédire `action` ne peut donc pas battre la
classe majoritaire : le 98,9 % publié était le taux de cette constante.

Le module change de cible et mesure honnêtement :

- `action` — la cible historique, gardée comme témoin ;
- `source` — la case de départ (`de` aux échecs, `chemin_0` aux dames) ;
- `cible`  — la case d'arrivée (`vers`, dernier `chemin`, `point`, `case`).

Trois ordres de Markov (0 = marginale par jeu, 1 = pas précédent, 2 = deux pas),
avec **repli hiérarchique Dirichlet** pour que la surprisal reste calibrée même
quand un contexte est rare. On oppose au modèle la **baseline majoritaire** et
sa **surprisal marginale**, on décompose par jeu, et un **contrôl
… [2591 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 160,230p tools/cerveau/predictif.py && echo ==== && sed -n 260,320p tools/cerveau/gating.py && echo ==== && sed -n 397,440p tools/cerveau/gating.py", "description": "Inspect current evaluer/executer returns"}`

  ```
c = self.transitions2[(jeu, precedent, cur)]
            total = sum(c.values())
            dist = {x: (c[x] + self.kappa * dist[x]) / (total + self.kappa) for x in valeurs}
        return dist

    def predire(self, code: dict, precedent=None) -> tuple:
        """Rend (valeur prédite, probabilité). `precedent` est une valeur de cible."""
        jeu = code.get("jeu")
        cur = valeur(code, self.cible)
        dist = self.distribution(jeu, cur, precedent)
        if not dist:
            return None, 0.0
        choix = max(dist, key=dist.get)
        return choix, dist[choix]

    # ------------------------------------------------------------------
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
                y =
… [6629 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 40,140p tools/cerveau/predictif.py && echo ==== && sed -n 55,95p tools/cerveau/memoire_travail.py", "description": "Inspect valeur/entrainer/span"}`

  ```
# Champ du code qui porte la « source » du coup, quand il existe.
CHAMPS_SOURCE = {"echecs": "de", "dames": "chemin_0"}
CIBLES = ("action", "source", "cible")


def valeur(pas, cible: str = "cible"):
    """La valeur de la cible pour un pas (ou un code typé).

    `pas` peut être un `Pas` (attribut `.code`) ou directement le dictionnaire
    du code. Rend `None` quand la cible n'a pas de sens pour ce jeu (un go n'a
    pas de case de départ).
    """
    code = getattr(pas, "code", pas)
    if not isinstance(code, dict):
        raise TypeError("valeur attend un Pas ou un code typé (dict)")
    jeu = code.get("jeu")
    if cible == "action":
        return code.get("action")
    if cible == "source":
        champ = CHAMPS_SOURCE.get(jeu)
        return code.get(champ) if champ else None
    if cible == "cible":
        if jeu == "echecs":
            return code.get("vers")
        if jeu == "dames":
            for champ in ("chemin_2", "chemin_1", "chemin_0"):
                if code.get(champ) is not None:
                    return code[champ]
            return None
        if jeu == "go":
            return code.get("point")
        if jeu == "morpion":
            return co
… [3893 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/cerveau/lesion.py')\ns=p.read_text()\n# M4: skip jeu/action\ns=s.replace('''    for nom in NOMS:\n        presents = [it for it in echantillon if it.code.get(nom) is not None]''',\n'''    for nom … [5563 caractères tronqués]`

  ```
patched
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", line 460, in batterie_lesions
    "negatif_M6_hasard": m6["lessee"]["hasard"],
                         ~~~~~~~~~~~~^^^^^^^^^^
KeyError: 'hasard'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/cerveau/lesion.py')\ns=p.read_text().replace('''            \"negatif_M6_hasard\": m6[\"lessee\"][\"hasard\"],''',\n'''            \"M6_tout_non\": m6[\"lessee\"][\"tout_non\"],\n            \"M6 … [924 caractères tronqués]`

  ```
ok
t 3.56 secondes 3.56
{
 "deficits": {
  "M1": {
   "exact": 0.29166666666666663,
   "relatif": 0.29166666666666663
  },
  "M2": {
   "action": 0.55,
   "de": 0.8166666666666667,
   "double_dissociation": true
  },
  "M3": {
   "span": 1.0,
   "exact": 1.0
  },
  "M4": {
   "rappel": 1.0,
   "completion": 0.9866666666666667,
   "par_champ": {
    "de": {
     "n": 4,
     "rappel_lese": 0.0,
     "deficit": 1.0
    },
    "vers": {
     "n": 4,
     "rappel_lese": 0.0,
     "deficit": 1.0
    },
    "promotion": {
     "n": 1,
     "rappel_lese": 0.0,
     "deficit": 1.0
    },
    "case": {
     "n": 4,
     "rappel_lese": 0.0,
     "deficit": 1.0
    },
    "symbole": {
     "n": 4,
     "rappel_lese": 0.0,
     "deficit": 1.0
    },
    "carte": {
     "n": 4,
     "rappel_lese": 0.0,
     "deficit": 1.0
    },
    "taille": {
     "n": 4,
     "rappel_lese": 0.0,
     "deficit": 1.0
    },
    "point": {
     "n": 2,
     "rappel_lese": 0.0,
     "deficit": 1.0
    },
    "passe": {
     "n": 2,
     "rappel_lese": 0.0,
     "deficit": 1.0
    },
    "chemin_0": {
     "n": 4,
     "rappel_lese": 0.0,
     "deficit": 1.0
    },
    "chemin_1": {
     "n": 4,
     "rappel_lese
… [5273 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/cerveau/lesion.py')\ns=p.read_text()\n\n# ---- M2: all items, de incl. None, report non-null ----\nstart=s.index('def _m2() -> dict:')\nend=s.index('# -------------------------------------------- … [7695 caractères tronqués]`

  ```
patched
t 3.61 secondes 3.61
M1 | mesure
  intacte {'exact': 1.0}
  lessee  {'exact': 0.7083}
  deficit {'exact': 0.2917, 'relatif': 0.2917}
M2 | proxy CPU (bayes naïf, deux têtes) ; voi
  intacte {'action': 0.6623, 'de': 0.6358, 'de_non_nul': 0.7536, 'n_de_non_nul': 69}
  lessee  {'action': 0.1384, 'de': 0.1245, 'avec_priori': {'action': 0.26490066225165565, 'de': 0.543046357615894}, 'ventrale': {'action': 0.13841059602649006, 'de': 0.6357615894039735, 'de_non_nul': 0.7536231884057971}, 'dorsale': {'action': 0.6622516556291391, 'de': 0.12450331125827814, 'de_non_nul': 0.12318840579710146}}
  deficit {'action': 0.5238, 'de': 0.5113, 'de_non_nul': 0.6304, 'avec_priori': {'action': 0.3973509933774835, 'de': 0.0927152317880795, 'de_non_nul': 0.7536231884057971}, 'double_dissociation': True}
M3 | mesure
  intacte {'span': 12, 'exact': 1.0, 'nback1_brut': 0.0006, 'nback1_controle': 0.0, 'nback2_controle': 0.0}
  lessee  {'span': 0, 'exact': 0.0, 'nback1_brut': 0.0, 'nback1_controle': 0.0, 'nback2_controle': 0.0}
  deficit {'span': 1.0, 'exact': 1.0, 'nback1_controle': 0.0}
M4 | mesure
  intacte {'rappel': 1.0, 'completion': 0.9867, 'n': 35}
  lessee  {'rappel': 0.0, 'completion': 0.0, '
… [3836 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/cerveau/lesion.py')\ns=p.read_text()\nold='''    rng = random.Random(7)\n    base = [dict(rng.choice([p.code for p in s.pas])) for s in seqs[:5]]\n    suite = [dict(base[i % len(base)]) for i in  … [1025 caractères tronqués]`

  ```
ok
{'span': 12, 'exact': 1.0, 'nback1_brut': 0.000630119722747322, 'nback1_controle': 0.0, 'nback2_controle': 1.0}
{'span': 1.0, 'exact': 1.0, 'nback2_controle': 1.0}
{'de': {'n': 7, 'rappel_lese': 1.0, 'deficit': 0.0}, 'vers': {'n': 7, 'rappel_lese': 1.0, 'deficit': 0.0}, 'roque': {'n': 1, 'rappel_lese': 1.0, 'deficit': 0.0}, 'case': {'n': 7, 'rappel_lese': 1.0, 'deficit': 0.0}, 'symbole': {'n': 7, 'rappel_lese': 1.0, 'deficit': 0.0}, 'carte': {'n': 7, 'rappel_lese': 0.42857142857142855, 'deficit': 0.5714285714285714}, 'taille': {'n': 7, 'rappel_lese': 1.0, 'deficit': 0.0}, 'point': {'n': 6, 'rappel_lese': 1.0, 'deficit': 0.0}, 'passe': {'n': 1, 'rappel_lese': 1.0, 'deficit': 0.0}, 'chemin_0': {'n': 7, 'rappel_lese': 1.0, 'deficit': 0.0}, 'chemin_1': {'n': 7, 'rappel_lese': 1.0, 'deficit': 0.0}}
  ```

- **write** `{"content": "from __future__ import annotations\n\nimport unittest\n\nfrom cerveau.neuromodulation import (MemoireLimitee, Neuromodulation,\n                                     experience_m7, preparer_flux)\n\n\nclass TestNeuromodulation(unittest.TestCase):\n    def test_fifo_evince_le_plus_ancien( … [2825 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_neuromodulation.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "from __future__ import annotations\n\nimport unittest\nfrom types import SimpleNamespace\n\nfrom cerveau.sommeil import Sommeil, experience_m8\n\n\ndef _it(code, texte=\"x\", paire=\"p\", jeu=\"echecs\"):\n    return SimpleNamespace(code=code, texte=texte, paire=paire, jeu=jeu)\n\n\nCOD … [2466 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_sommeil.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "from __future__ import annotations\n\nimport json\nimport unittest\n\nfrom cerveau.lesion import batterie_lesions\n\n\nclass TestLesion(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls):\n        cls.r = batterie_lesions(rapide=True)\n\n    def test_structure(self):\n       … [2859 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 300 python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -40; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run cerveau test suite"}`

  ```
..........................................................
----------------------------------------------------------------------
Ran 58 tests in 4.850s

OK
EXIT=0
  ```

- **bash** `{"command": "ls -la /tmp/a2-m2-cpu.json /tmp/a2-m2-cpu.out 2>&1; tail -5 /tmp/a2-m2-cpu.out 2>/dev/null; ps aux | grep -c \"[v]oies\\|[t]ransformers\"", "description": "Check background M2 job"}`

  ```
-rw-r--r--. 1 stephane stephane 313 27 oct 09:55 /tmp/a2-m2-cpu.json
-rw-r--r--. 1 stephane stephane 456 27 oct 09:55 /tmp/a2-m2-cpu.out
  "de": 0.00684931506849315,
  "n": 146
 },
 "secondes": 38.28941226005554
}
0
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 - <<'PY'\nimport json, time\nfrom cerveau.neuromodulation import experience_m7\nfrom cerveau.sommeil import experience_m8\nfrom cerveau.lesion import batterie_lesions\nt=time.time(); m7=experience_m7(permutations=3 … [1248 caractères tronqués]`

  ```
M7 4.7
M8 0.2
M9 6.9 6.938775560993236
JSON written
M7 verdict {"meilleur_suffixe_code": "lfu_code", "meilleur_repetes": "lfu", "signaux_qui_battent_fifo_suffixe": [], "signaux_qui_battent_fifo_repetes": [], "plafond_surface_atteint_par_toutes": true, "gel_egal_fifo_sur_la_metrique_historique": true, "nouveaute_code_egale_fifo_code": false}
M8 verdict {"champs_96_48_reproduit": true, "exact_queue": 0.6509433962264151, "exact_annonce_0_est_faux": true, "gain_sur_par_jeu_champs": 0.0037735849056603765, "gain_sur_par_jeu_exact": 0.018867924528301883, "champs_non_nuls": 0.8596491228070176, "exact_codes_uniques": 0.2413793103448276, "exact_codes_nouveaux": [0.0, 0.0, 0.0], "hybride_exact_queue": 1.0, "hybride_couverture_queue": 1.0, "hybride_exact_codes_nouveaux": [0.0, 0.0, 0.0], "baseline_globale_champs": 0.7805031446540881, "baseline_globale_exact": 0.0, "groupes_melanges_champs": 0.8283018867924529}
M9 resume {"deficits": {"M1": {"exact": 0.29166666666666663, "relatif": 0.29166666666666663}, "M2": {"action": 0.523841059602649, "de": 0.5112582781456954, "de_non_nul": 0.6304347826086957, "avec_priori": {"action": 0.3973509933774835, "de": 0.0927152317880795, "de_non_nul": 0.7536231884
… [222 caractères tronqués]
  ```

- **bash** `{"command": "cat /tmp/a2-m2-cpu.json", "description": "Read real M2 CPU reference"}`

  ```
{
 "normal": {
  "action": 0.9863013698630136,
  "de": 0.9178082191780822,
  "n": 146
 },
 "lese_ventrale": {
  "action": 0.1095890410958904,
  "de": 0.9178082191780822,
  "n": 146
 },
 "lese_dorsale": {
  "action": 0.9863013698630136,
  "de": 0.00684931506849315,
  "n": 146
 },
 "secondes": 38.28941226005554
}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nr=json.load(open('/tmp/a2-m7-m8-m9.json'))\nprint('M9 M4',json.dumps(r['M9']['modules']['M4']['deficit'],ensure_ascii=False)[:1200])\nprint('M9 M7',json.dumps(r['M9']['modules']['M7']['deficit'],ensure_ascii=False))\npri … [201 caractères tronqués]`

  ```
M9 M4 {"rappel": 1.0, "completion": 0.9866666666666666, "par_champ": {"de": {"n": 14, "rappel_lese": 1.0, "deficit": 0.0}, "vers": {"n": 14, "rappel_lese": 1.0, "deficit": 0.0}, "roque": {"n": 1, "rappel_lese": 1.0, "deficit": 0.0}, "case": {"n": 14, "rappel_lese": 1.0, "deficit": 0.0}, "symbole": {"n": 14, "rappel_lese": 1.0, "deficit": 0.0}, "carte": {"n": 14, "rappel_lese": 0.21428571428571427, "deficit": 0.7857142857142857}, "taille": {"n": 14, "rappel_lese": 1.0, "deficit": 0.0}, "point": {"n": 9, "rappel_lese": 1.0, "deficit": 0.0}, "passe": {"n": 5, "rappel_lese": 1.0, "deficit": 0.0}, "chemin_0": {"n": 14, "rappel_lese": 1.0, "deficit": 0.0}, "chemin_1": {"n": 14, "rappel_lese": 0.21428571428571427, "deficit": 0.7857142857142857}, "chemin_2": {"n": 2, "rappel_lese": 0.0, "deficit": 1.0}}, "champ_le_plus_necessaire": "chemin_2", "deficit_champ_max": 1.0}
M9 M7 {"surface_vs_fifo": {"suf_code": 0.004245283018867935, "rep_surface": -0.18851525986540854}, "code_vs_fifo": {"suf_code": -0.5141509433962265, "rep_surface": -0.14436643422377354}, "signal_sur_cle_code": -0.6764150943396227, "cle_code_sans_signal": 0.16226415094339625, "plafond_code": 0.5517241379310345, "plafond_surfa
… [1358 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\np='/tmp/a2-m7-m8-m9.json'\nr=json.load(open(p))\nr['M2_reference_neuronale']=json.load(open('/tmp/a2-m2-cpu.json'))\nr['fichiers']=['tools/cerveau/neuromodulation.py','tools/cerveau/sommeil.py','tools/cerveau/lesion.py', … [1902 caractères tronqués]`

  ```
json ok 109.6 KB
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nR=json.load(open('/tmp/a2-m7-m8-m9.json'))\nM7,M8,M9=R['M7'],R['M8'],R['M9']\nL=[]\ndef w(s=''): L.append(s+'\\n')\nw(\"# A2 — M7/M8/M9 : neuromodulation, sommeil, lésions\")\nw()\nw(\"> Sous-agent M7/M8/M9, sprint 24 h, … [7305 caractères tronqués]`

  ```
part1 7993
# A2 — M7/M8/M9 : neuromodulation, sommeil, lésions

> Sous-agent M7/M8/M9, sprint 24 h, CPU uniquement. Date : 2026-10-27 10:10:16.
> JSON complet : `/tmp/a2-m7-m8-m9.json`. Code : `tools/cerveau/neuromodulation.py`, `sommeil.py`, `lesion.py`.

## 0. Résumé

| module | mesure | résultat | verdict |
|---|---|---|---|
| **M7** | rétention bornée, 30 permutations appariées | plafond surface **3,6446 %** = 16/439 ; aucun signal ne bat FIFO ; LFU = +24,4 pts de répétés ; nouveauté surface = −18,5 pts ; incertitude = −38,9 pts de suffixe code ; récompense = −51,7 pts | **négatif net** : la modulation ne paie pas ; la fréquence, si |
| **M8** | prototypes vs codes neufs | 96,48 % champs reproduit ; exact **65,09 %** (pas 0 %) ; non nuls **85,96 %** ; codes uniques **24,14 %** ; codes neufs exact **0 %** ; baseline per-game 96,10 % ; hybride 100 % sur la queue = mémorisation | **négatif net** : 96,48 % est le plafond de la marginale, pas une généralisation |
| **M9** | lésions par module | M1 0,292 ; M2 0,524/0,630 (double dissociation) ; M3 1,0 ; M4 1,0 ; M5 0,037 ; M6 0,193 ; M7 déficit négatif ; M8 0,184 (champs) / 0,651 (exact) ; sham 0 partout | **table mesurée** ; M5/M7/M
… [541 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nR=json.load(open('/tmp/a2-m7-m8-m9.json')); M8,M9=R['M8'],R['M9']\nL=[]\ndef w(s=''): L.append(s+'\\n')\nw(\"## 2. M8 — sommeil : prototypes, baselines, codes neufs\")\nw()\nw(\"### 2.1 Protocole\")\nw()\np=M8['protocole … [11205 caractères tronqués]`

  ```
part2 9306
## 2. M8 — sommeil : prototypes, baselines, codes neufs

### 2.1 Protocole

- Corpus : **528** items, **29** codes uniques ; queue 80/20 = **422** train / **106** test.
- Prototypes par `(jeu, action)` (mode par champ), joints (code complet), par type (signature des champs non nuls).
- Baselines explicites : globale, par jeu, par groupe, groupes mélangés, hasard (un code du train par groupe), plafond triché par paire.
- Tests honnêtes : déduplication par code et par paire ; split par **codes tenus à l'écart** (le test ne contient que des codes jamais vus) ; split par paires (celui de `typed_corpus.decouper`).
- **Hybride prototypes + épisodes** : si le code exact a été vu, on le récupère ; sinon on retombe sur le prototype. C'est le « rejet + prototypes + épisodes » de la suite du rapport.
- Champs constants : **0/15** (``) ; variables : `jeu, action, de, vers, promotion, roque, case, symbole, carte, taille, point, passe, chemin_0, chemin_1, chemin_2`.

### 2.2 Résultats sur la queue (106 épisodes)

| évaluation | champs | exact | n |
|---|---:|---:|---:|
| module_champs | 0.9648 | 0.6509 | 106 |
| module_joint | 0.9648 | 0.6509 | 106 |
| module_type | 0.9648 | 0.6509 | 
… [329 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/cerveau/sommeil.py')\ns=p.read_text()\ns=s.replace('''- 12 des 15 champs sont **constants** sur le corpus (souvent ``None``) ; ils\n  offrent 80 % du score sans rien prédire. Sur les champs non n … [3996 caractères tronqués]`

  ```
patched
quasi_none ['promotion', 'roque', 'passe', 'chemin_2']
taux_none {'jeu': 0.0, 'action': 0.0, 'de': 0.723, 'vers': 0.723, 'promotion': 0.996, 'roque': 0.992, 'case': 0.879, 'symbole': 0.879, 'carte': 0.695, 'taille': 0.835, 'point': 0.867, 'passe': 0.968, 'chemin_0': 0.867, 'chemin_1': 0.867, 'chemin_2': 0.994}
par_champ {'jeu': (106, 1.0), 'action': (106, 1.0), 'de': (38, 0.5), 'vers': (38, 0.5), 'promotion': (0, 0.0), 'roque': (0, 0.0), 'case': (8, 1.0), 'symbole': (8, 1.0), 'carte': (25, 0.28), 'taille': (21, 1.0), 'point': (19, 1.0), 'passe': (2, 1.0), 'chemin_0': (14, 1.0), 'chemin_1': (14, 1.0), 'chemin_2': (0, 0.0)}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/cerveau/sommeil.py')\ns=p.read_text().replace(\"8 des 15 champs ont plus de 98 %\", \"12 des 15 champs ont plus de 98 %\")\ns=s.replace(\"sont à 49 %, 49 % et 22 % conditionnellement.\", \"sont à … [449 caractères tronqués]`

  ```
ok
M8 updated {"champs_96_48_reproduit": true, "exact_queue": 0.6509433962264151, "exact_annonce_0_est_faux": true, "gain_sur_par_jeu_champs": 0.0037735849056603765, "gain_sur_par_jeu_exact": 0.018867924528301883,
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nR=json.load(open('/tmp/a2-m7-m8-m9.json')); M8,M9=R['M8'],R['M9']\nL=[]\ndef w(s=''): L.append(s+'\\n')\nw(\"## 2. M8 — sommeil : prototypes, baselines, codes neufs\")\nw()\nw(\"### 2.1 Protocole\")\nw()\np=M8['protocole … [11839 caractères tronqués]`

  ```
part2 10116
## 2. M8 — sommeil : prototypes, baselines, codes neufs

### 2.1 Protocole

- Corpus : **528** items, **29** codes uniques ; queue 80/20 = **422** train / **106** test.
- Prototypes par `(jeu, action)` (mode par champ), joints (code complet), par type (signature des champs non nuls).
- Baselines explicites : globale, par jeu, par groupe, groupes mélangés, hasard (un code du train par groupe), plafond triché par paire.
- Tests honnêtes : déduplication par code et par paire ; split par **codes tenus à l'écart** (le test ne contient que des codes jamais vus) ; split par paires (celui de `typed_corpus.decouper`).
- **Hybride prototypes + épisodes** : si le code exact a été vu, on le récupère ; sinon on retombe sur le prototype. C'est le « rejet + prototypes + épisodes » de la suite du rapport.
- Champs dominés par `None` : `de` 72,3 %, `vers` 72,3 %, `carte` 69,5 %, `case` 87,9 %, `symbole` 87,9 %, `point` 86,7 %, `chemin_0/1` 86,7 %, `taille` 83,5 %. 12/15 champs ont >98 % d'exactitude agrégée, mais c'est parce que la bonne réponse y est presque toujours `None` ou la constante du groupe.

### 2.2 Résultats sur la queue (106 épisodes)

| évaluation | champs | exact | n |
|-
… [673 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nR=json.load(open('/tmp/a2-m7-m8-m9.json'))\nL=[]\ndef w(s=''): L.append(s+'\\n')\nw(\"## 4. M2 — référence neuronale CPU vs proxy M9\")\nw()\nw(\"Le M9 par défaut utilise un **proxy CPU déterministe** (bayes naïf à deux  … [4545 caractères tronqués]`

  ```
md final 23503
286 /tmp/a2-m7-m8-m9.md
- **M8** : le split par codes tenus à l'écart a de petits tests (6 à 192 items) et les champs restent à ~93 % parce que la réponse est dominée par `None` ; l'exact 0 est le seul chiffre robuste.
- **M9** : M3, M5 et M6 ont été modifiés par d'autres sous-agents pendant la session ; les chiffres M9 sont ceux des API au moment du run. M2 est un proxy. M4 est un échantillon de 72 items (`chemin_2` n=2).
- **M9** : le sham est une répétition no-op, pas une lésion aléatoire ; les contrôles négatifs sont « tout accepter » (M6), « tête au hasard » (M2) et « hasard » (M7). Une lésion n'établit pas une nécessité causale.
- **Concurrence** : `batterie.py`, `docs/`, `reports/` et `journal/` n'ont pas été modifiés par moi, comme demandé. Les autres modifications visibles dans `git status` (`episodique.py`, `gating.py`, `memoire_travail.py`, `predictif.py`, `voies.py`, `journal/`) viennent d'autres sous-agents. `batterie.py` reste l'ancienne table M9 ; il ne faut pas la confondre avec `lesion.batterie_lesions()`.

## 6. Fichiers, commandes, tests

Fichiers modifiés (uniquement ceux autorisés) :

- `tools/cerveau/neuromodulation.py`
- `tools/cerveau/sommeil.
… [872 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 -m py_compile tools/cerveau/neuromodulation.py tools/cerveau/sommeil.py tools/cerveau/lesion.py tools/cerveau/tests/test_neuromodulation.py tools/cerveau/tests/test_sommeil.py tools/cerveau/tests/test_lesion.py && echo COMPILE_OK\nPYTHONPATH=t … [370 caractères tronqués]`

  ```
COMPILE_OK
batterie.m7 {'nouveaux': 439, 'retention_fixe': 0.03644646924829157, 'retention_modulee': 0.03644646924829157, 'capacite': 16, 'n': 528}
batterie.m8 {'champs': 0.9647798742138365, 'exact': 0.6509433962264151, 'champs_non_nuls': 0.8596491228070176, 'n': 106, 'n_inconnus': 0, 'n_champs_non_nuls': 399, 'prototypes': 7, 'baseline': 0.0, 'train': 422, 'test': 106}
JSON_OK

----------------------------------------------------------------------
Ran 59 tests in 5.143s

FAILED (errors=1)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 300 python3 -m unittest discover -s tools/cerveau/tests -t tools -v 2>&1 | grep -A 20 -E \"ERROR|FAIL\" | head -60", "description": "Show failing test details"}`

  ```
cerveau.tests.test_voies (unittest.loader._FailedTest.cerveau.tests.test_voies) ... ERROR

======================================================================
ERROR: cerveau.tests.test_voies (unittest.loader._FailedTest.cerveau.tests.test_voies)
----------------------------------------------------------------------
ImportError: Failed to import test module: cerveau.tests.test_voies
Traceback (most recent call last):
  File "/usr/lib64/python3.13/unittest/loader.py", line 403, in _find_test_path
    module = self._get_module_from_name(name)
  File "/usr/lib64/python3.13/unittest/loader.py", line 346, in _get_module_from_name
    __import__(name)
    ~~~~~~~~~~^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_voies.py", line 6, in <module>
    import torch
ModuleNotFoundError: No module named 'torch'


----------------------------------------------------------------------
Ran 59 tests in 5.076s

FAILED (errors=1)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 300 python3 -m unittest cerveau.tests.test_neuromodulation cerveau.tests.test_sommeil cerveau.tests.test_lesion -v 2>&1 | tail -20", "description": "Run only my three test files"}`

  ```
test_consolider_et_evaluer (cerveau.tests.test_sommeil.TestSommeil.test_consolider_et_evaluer) ... ok
test_dedup (cerveau.tests.test_sommeil.TestSommeil.test_dedup) ... ok
test_experience_reelle (cerveau.tests.test_sommeil.TestSommeil.test_experience_reelle) ... ok
test_hybride (cerveau.tests.test_sommeil.TestSommeil.test_hybride) ... ok
test_json (cerveau.tests.test_lesion.TestLesion.test_json) ... ok
test_m1_contexte (cerveau.tests.test_lesion.TestLesion.test_m1_contexte) ... ok
test_m2_double_dissociation (cerveau.tests.test_lesion.TestLesion.test_m2_double_dissociation) ... ok
test_m3_tampon (cerveau.tests.test_lesion.TestLesion.test_m3_tampon) ... ok
test_m4_stockage (cerveau.tests.test_lesion.TestLesion.test_m4_stockage) ... ok
test_m5_transitions (cerveau.tests.test_lesion.TestLesion.test_m5_transitions) ... ok
test_m6_porte (cerveau.tests.test_lesion.TestLesion.test_m6_porte) ... ok
test_m7_modulation (cerveau.tests.test_lesion.TestLesion.test_m7_modulation) ... ok
test_m8_sommeil (cerveau.tests.test_lesion.TestLesion.test_m8_sommeil) ... ok
test_sham (cerveau.tests.test_lesion.TestLesion.test_sham) ... ok
test_structure (cerveau.tests.test_lesion.TestLesion.test_structure)
… [106 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nR=json.load(open('/tmp/a2-m7-m8-m9.json'))\nfor k in ('lfu','nouveaute','incertitude','recompense','fifo_code','nouveaute_code','lfu_code','hasard'):\n    d=R['M7']['deltas_vs_fifo'][k]\n    print(k, {m:(round(d[m]['moye … [289 caractères tronqués]`

  ```
lfu {'rep_surface': (0.2313, 30), 'suf_surface': (0.0425, 27), 'suf_code': (0.0299, 16)}
nouveaute {'rep_surface': (-0.1959, 0), 'suf_surface': (-0.0421, 0), 'suf_code': (-0.011, 9)}
incertitude {'rep_surface': (-0.1538, 0), 'suf_surface': (-0.034, 7), 'suf_code': (-0.3874, 0)}
recompense {'rep_surface': (-0.1344, 0), 'suf_surface': (-0.0333, 5), 'suf_code': (-0.5327, 0)}
fifo_code {'rep_surface': (-0.0379, 1), 'suf_surface': (-0.0116, 6), 'suf_code': (0.1569, 26)}
nouveaute_code {'rep_surface': (-0.1486, 0), 'suf_surface': (-0.0418, 0), 'suf_code': (-0.5277, 0)}
lfu_code {'rep_surface': (-0.0252, 2), 'suf_surface': (-0.0063, 6), 'suf_code': (0.2324, 30)}
hasard {'rep_surface': (0.0259, 15), 'suf_surface': (0.0006, 12), 'suf_code': (0.0053, 15)}
code vs fifo {'moyenne': -0.6845911949685536, 'ecart_type': 0.10559655491049232, 'n': 30, 'gains': 0, 'ic95': [-0.7223784368465025, -0.6468039530906047]}
M9 M7 {'surface_vs_fifo': {'suf_code': 0.004245283018867935, 'rep_surface': -0.18851525986540854}, 'code_vs_fifo': {'suf_code': -0.5141509433962265, 'rep_surface': -0.14436643422377354}, 'signal_sur_cle_code': -0.6764150943396227, 'cle_code_sans_signal': 0.16226415094339625, 'plafond_code'
… [61 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json, pathlib\np=pathlib.Path('/tmp/a2-m7-m8-m9.md'); s=p.read_text()\nrep={\n\"LFU = +24,4 pts de répétés ; nouveauté surface = −18,5 pts ; incertitude = −38,9 pts de suffixe code ; récompense = −51,7 pts\":\n\"LFU = +23,1 pt … [5267 caractères tronqués]`

  ```
patched md/json
10:| **M7** | rétention bornée, 30 permutations appariées | plafond surface **3,6446 %** = 16/439 ; aucun signal ne bat FIFO ; LFU = +23,1 pts de répétés ; nouveauté surface = −19,6 pts ; incertitude = −38,7 pts de suffixe code ; récompense = −53,3 pts | **négatif net** : la modulation ne paie pas ; la fréquence, si |
68:- **LFU** est la seule politique qui améliore nettement les répétés (**+23,1 pts**, 30/30) et le suffixe surface (+4,25 pts, 27/30) ; le suffixe code ne bouge pas significativement (+3,0 pts, 16/30).
69:- **Nouveauté par surface** : répétés **−19,6 pts** (0/30), suffixe surface −4,2 pts (0/30), suffixe code −1,1 pt (9/30). Le signal binaire sature : les 16 premiers items nouveaux ont tous le poids maximal, aucun item suivant ne les évince par ce signal.
70:- **Nouveauté par code** : la couverture des codes monte au plafond (16/29) mais le suffixe code s'effondre (**−52,8 pts**) : elle gèle les 16 premiers codes, pas les codes chauds.
71:- **Incertitude** (1 − confiance du codec) : **−38,7 pts** de suffixe code, 0/30. Les lectures peu confiantes sont ambiguës ou rares, pas utiles.
72:- **Récompense** (proxy gain matériel `prendre`/`promouvoir`) : **−
… [1014 caractères tronqués]
  ```

### 👤 Utilisateur

<system-reminder>
Updated instructions from: AGENTS.md

This file changed after it was loaded. Use the following content instead of the previously loaded instructions from this file.

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

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nR=json.load(open('/tmp/a2-m7-m8-m9.json'))\nprint('keys',list(R.keys()))\nprint('M7 policies',len(R['M7']['politiques']),'M8 keys',list(R['M8'].keys()),'M9 modules',list(R['M9']['modules']))\nprint('M2 ref',R['M2_referen … [548 caractères tronqués]`

  ```
keys ['meta', 'M7', 'M8', 'M9', 'M2_reference_neuronale', 'fichiers', 'tests', 'limites', 'M9_part', 'avertissements']
M7 policies 16 M8 keys ['protocole', 'queue', 'dedup_tout', 'codes_nouveaux', 'paires', 'verdict'] M9 modules ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8']
M2 ref {'action': 0.9863013698630136, 'de': 0.9178082191780822, 'n': 146}
tests {'mes_tests': '22 tests OK (5,22 s) : test_neuromodulation, test_sommeil, test_lesion', 'suite_complete': "59 tests, 1 erreur : cerveau/tests/test_voies.py importe torch au niveau module (torch absent du python3). Fichier d'un autre sous-agent, non modifié.", 'commande': 'PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools'}
md bytes 24193
--- git status ---
 M AGENTS.md
 M docs/README.md
 M docs/en-cours.md
 M journal/2026-10-27_sprint-24h.md
 M tools/cerveau/episodique.py
 M tools/cerveau/gating.py
 M tools/cerveau/memoire_travail.py
 M tools/cerveau/neuromodulation.py
 M tools/cerveau/predictif.py
 M tools/cerveau/sommeil.py
 M tools/cerveau/voies.py
?? reports/rapport-cerveau-corrections.md
?? tools/cerveau/lesion.py
?? tools/cerveau/tests/test_episodique.py
?? tools/cerveau/tests/test_gating.py
?? to
… [845 caractères tronqués]
  ```

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "M7/M8/M9 TERMINÉ. Livrables : /tmp/a2-m7-m8-m9.json (109 Ko) et /tmp/a2-m7-m8-m9.md (24 Ko). Code : tools/cerveau/neuromodulation.py, sommeil.py, lesion.py, tests/test_neuromodulation.py, test_sommeil.py, test_lesion.py.\n\nM7 — négati … [2844 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

### 🤖 Assistant

⏵ Clôture M7/M8/M9 : vérification des livrables et résumé

Sprint M7/M8/M9 terminé. Livrables écrits et testés.

## Chemins

- `/tmp/a2-m7-m8-m9.json` — résultats complets (M7 30 permutations, M8, M9, référence M2 CPU, limites)
- `/tmp/a2-m7-m8-m9.md` — rapport chiffré, commandes, verdicts, autocritique
- Code : `tools/cerveau/neuromodulation.py`, `tools/cerveau/sommeil.py`, `tools/cerveau/lesion.py`
- Tests : `tools/cerveau/tests/test_neuromodulation.py`, `test_sommeil.py`, `test_lesion.py`

## Résultats

**M7 — négatif net.** Le banc historique était faux : `MemoireLimitee.stocker` gardait les 16 premiers arrivés (« gel »), pas FIFO. La métrique 3,64 % = 16/439 est le plafond mathématique : toutes les politiques l'atteignent, hasard compris. Sur 30 permutations appariées : LFU +23,1 pts de répétés ; nouveauté surface −19,6 pts ; incertitude −38,7 pts de suffixe code ; récompense (proxy `prendre`/`promouvoir`) −53,3 pts. Aucun signal neuromodulateur ne bat FIFO. La clé code (fifo_code) gagne +15,7 pts, mais ajouter la nouveauté à cette clé coûte −68,5 pts. Contrôle positif Zipf réussi (LFU +17,8, récompense informative +19,6, hasard −1,2).

**M8 — 96,48 % reproduit, mais ce n'est pas une généralisation.** Exact 65,09 % (pas 0 %), champs non nuls 85,96 %, dédup code 24,14 % d'exact. Baseline par jeu 96,10 % : le groupe action n'apporte que +0,38 pt. Un tirage aléatoire d'un code mémorisé par groupe fait 96,35 %. Sur codes tenus à l'écart, exact **0,0000** partout ; l'hybride prototypes+épisodes fait 100 % sur la queue uniquement parce que tous les codes y sont vus — c'est M4, pas le sommeil.

**M9 — `lesion.py`.** Batterie CPU en 6,9 s, sham nul partout, dose-réponse M3, contrôle positif M5, double dissociation M2. Déficits : M1 0,292 ; M2 0,524/0,630 ; M3 1,0 ; M4 1,0 ; M5 0,037 seulement (ordre 2 = 0) ; M6 0,193 ; M7 négatif (la modulation coûte) ; M8 0,184/0,651 sur codes vus, **0 sur codes neufs**. Référence `voies.py` CPU : action 98,63→10,96, de 91,78→0,68 ; le proxy M9 reproduit la structure, pas les magnitudes.

## Tests

Mes 22 tests passent (5,22 s). La découverte complète (59 tests) échoue sur `test_voies.py`, ajouté par un autre sous-agent : il importe `torch` au niveau module, absent du `python3` du dépôt. Je ne l'ai pas modifié. `batterie.py` est intact ; sa table M9 reste l'ancienne (`1 − lésé`), à ne pas confondre avec `batterie_lesions()` (`intacte − lésée` + sham).

Aucun `git add/commit/checkout`, aucun `docs/`, `reports/`, `journal/` ou `batterie.py` touché.

