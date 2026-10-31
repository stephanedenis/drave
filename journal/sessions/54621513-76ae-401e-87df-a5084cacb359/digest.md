# Session DSH — relecture

- identifiant : `54621513-76ae-401e-87df-a5084cacb359`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 09:41:21
- agent : standard


## Tour 1

### 👤 Utilisateur

Nous sommes dans /home/stephane/GitHub/Qtrinet (dépôt Drave). Sprint autonome 24 h. Tu es un sous-agent chargé de M5 (codage prédictif) et M6 (gating/contrôle exécutif) du prototype `tools/cerveau/`.

État actuel mesuré :
- M5 `tools/cerveau/predictif.py` : prédit l'action suivante ; exact 98,9 % = majoritaire 98,9 %, aucun gain ; l'ordre 2 n'a rien changé.
- M6 `tools/cerveau/gating.py` : exact 72,9 %, FP 1, FN 18, coût de commutation −0,11.
- Corpus : `tools/semantique/typed_corpus.items()` (528 surfaces B5/B7), `tools/cerveau/sequences.py` (parties générées par les règles, 4 jeux).
- Tests : `PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools`.

Objectif : améliorer réellement, ou produire un négatif net et documenté.
M5 :
- Change la cible : prédire `de`, `vers`, ou l'action/conditionnel, pas seulement l'action majoritaire.
- Teste ordre 2, par jeu, et une baseline majoritaire ; mesure exact, surprisal, n ; conserve un contrôle négatif.
- Si aucun gain, dis-le et nomme la cause (cible trop constante, séquences aléatoires, etc.).
M6 :
- Construis une vraie tâche de conflit langue/tâche (deux langues, cible, inhibition, commutation) sur les surfaces B7 ; mesure exactitude, faux positifs/négatifs, coût de commutation.
- Si le score reste faible, documente le négatif et pourquoi la détection de langue n'est pas du contrôle exécutif.

Contraintes :
- Modifie uniquement `tools/cerveau/predictif.py`, `tools/cerveau/gating.py` et, si nécessaire, `tools/cerveau/tests/test_predictif.py` / `test_gating.py`. Ne touche pas à `batterie.py`, docs, reports, journal, git.
- N'exécute pas de `git commit`, `git add` ou `git checkout`.
- Écris tes résultats structurés dans `/tmp/a1-m5-m6.json` et un court markdown dans `/tmp/a1-m5-m6.md` (chiffres, commandes, ce qui tient/ne tient pas).
- Utilise `PYTHONPATH=tools`, pas de GPU nécessaire (CPU).
- Sois autonome, teste, autocritique-toi. Réponds avec un résumé concis et les chemins des fichiers.
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

⏵ Exploring the cerveau prototype and its data sources.

- **bash** `{"command": "pwd && ls -la && ls -la tools/cerveau/ 2>/dev/null && echo \"---\" && ls -la tools/semantique/ 2>/dev/null | head -40", "description": "List repo and cerveau directory"}`

  ```
/home/stephane/GitHub/Qtrinet
total 192
drwxr-xr-x. 1 stephane stephane   630 27 oct 09:29 .
drwxr-xr-x. 1 stephane stephane  2464 22 oct 16:06 ..
-rw-r--r--. 1 stephane stephane  7544 27 oct 09:32 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  1056 26 oct 11:22 data
drwxr-xr-x. 1 stephane stephane   928 27 oct 09:36 docs
drwxr-xr-x. 1 stephane stephane    82 28 sep 11:58 drave-core
drwxr-xr-x. 1 stephane stephane   164 27 oct 09:41 .git
-rw-r--r--. 1 stephane stephane   399 30 sep 10:01 .gitignore
drwxr-xr-x. 1 stephane stephane  6494 27 oct 09:37 journal
drwxr-xr-x. 1 stephane stephane   100 15 oct 09:02 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-------. 1 stephane stephane 19008 27 oct 09:27 README.md
drwxr-xr-x. 1 stephane stephane 20414 27 oct 09:36 reports
-rw-------. 1 stephane stephane 12170 27 oct 09:32 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane 10507 30 sep 08:44 run_clusters.py
-rw-------.
… [2921 caractères tronqués]
  ```

- **bash** `{"command": "wc -l tools/cerveau/*.py tools/cerveau/tests/*.py 2>/dev/null", "description": "Count lines in cerveau files"}`

  ```
225 tools/cerveau/batterie.py
   51 tools/cerveau/bus.py
   69 tools/cerveau/episodique.py
   49 tools/cerveau/gating.py
   47 tools/cerveau/hub.py
    0 tools/cerveau/__init__.py
   57 tools/cerveau/memoire_travail.py
   55 tools/cerveau/neuromodulation.py
   66 tools/cerveau/predictif.py
  114 tools/cerveau/sequences.py
   40 tools/cerveau/sommeil.py
  103 tools/cerveau/voies.py
    0 tools/cerveau/tests/__init__.py
   29 tools/cerveau/tests/test_bus.py
   24 tools/cerveau/tests/test_modules.py
  929 total
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/sequences.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/semantique/typed_corpus.py"}`

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

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/batterie.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_modules.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/semantique/universaux.py"}`

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


  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_modules.py</path>
<type>file</type>
<content>
1: from __future__ import annotations
2: import unittest
3: from cerveau.memoire_travail import MemoireTravail
4: from cerveau.episodique import Episodique
5: from cerveau.sequences import partie
6: 
7: 
8: class TestModules(unittest.TestCase):
9:     def test_span(self):
10:         s = partie("echecs", 0, 5)
11:         m = MemoireTravail(5)
12:         self.assertGreaterEqual(m.span([s])["span"], 1)
13: 
14:     def test_episodique(self):
15:         e = Episodique()
16:         a = {"jeu": "echecs", "action": "deplacer", "de": 62, "vers": 45}
17:         b = {"jeu": "echecs", "action": "deplacer", "de": 52, "vers": 36}
18:         e.stocker("Nf3", a); e.stocker("e4", b)
19:         self.assertTrue(e.rappel(a)["exact"])
20:         self.assertTrue(e.separation(a, b)["distincts"])
21: 
22: 
23: if __name__ == "__main__":
24:     unittest.main()

(End of file - total 24 lines)
</content>
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

- **bash** `{"command": "ls tools/jeux/ && sed -n 1,200p tools/jeux/lexique_multilingue.py", "description": "Inspect multilingual lexicon module"}`

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

Ce module ne **devine** pas la langue d'un texte : il compte les libellés
reconnus et rend la
… [7536 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/cerveau/tests/; sed -n 1,80p tools/cerveau/tests/test_bus.py; echo ---; grep -rn \"detecte_langue\" tools/ | head -20", "description": "Inspect tests and detecte_langue usages"}`

  ```
__init__.py
__pycache__
test_bus.py
test_modules.py
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
        self.assertEqual(len(list(b.rejouer("sens"))), 1)
        self.assertEqual(b.compter("sens"), 1)

    def test_hub(self):
        h = Hub()
        ctx = E.rsn_depuis_position(E.Position.depart())
        code = h.percevoir("Nf3", "echecs", ctx)
        self.assertEqual(code["jeu"], "echecs")
        self.assertEqual(code["de"], 62)
        self.assertEqual(code["vers"], 45)
        surface = h.rendre(code, ctx)
        self.assertIn(surface, ("Nf3", "nf3", "g1f3", "g1-f3"))


if __name__ == "__main__":
    unittest.main()
---
tools/jeux/codecs/base.py:142:            ml = MULTI.detecte_langue(texte)
tools/jeux/lexique_multilingue.py:20:reconnus et rend la langue la plus probable (`detecte_langue`). C'est une
tools/jeux/lexiq
… [396 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reproducing baseline measurements and profiling label distributions.

- **bash** `{"command": "cat > /tmp/diag_m5m6.py <<'EOF'\nimport sys, collections, math\nsys.path.insert(0, 'tools')\nfrom cerveau.sequences import corpus, partie\nfrom cerveau.predictif import Predictif\nfrom semantique.typed_corpus import items\n\nseqs = corpus(0, 40, 12)\nrng = __import__('random').Random(3) … [1582 caractères tronqués]`

  ```
M5 actuel: {'exact': 0.9893238434163701, 'majoritaire': 0.9893238434163701, 'surprise': 0.01064535311304908, 'n': 281}
go 480 [('poser', 442), ('passer', 38)] majoritaire=0.9208
echecs 480 [('deplacer', 480)] majoritaire=1.0000
dames 480 [('prendre', 480)] majoritaire=1.0000
morpion 307 [('jouer_case', 307)] majoritaire=1.0000
--- echecs
  action     n= 480 distincts=  1 maj=1.000
  de         n= 480 distincts= 60 maj=0.042
  vers       n= 480 distincts= 53 maj=0.048
--- dames
  action     n= 480 distincts=  1 maj=1.000
--- go
  action     n= 480 distincts=  2 maj=0.921
  point      n= 442 distincts= 79 maj=0.025
  passe      n=  38 distincts=  1 maj=1.000
--- morpion
  action     n= 307 distincts=  1 maj=1.000
  case       n= 307 distincts=  9 maj=0.124
items total: 528 langues: [('fr', 55), ('notation', 31), ('en', 15), ('de', 11), ('es', 11), ('it', 11), ('ja', 11), ('nl', 11), ('pl', 11), ('pt', 11), ('ru', 11), ('zh', 11), ('cs', 10), ('da', 10), ('eo', 10), ('et', 10), ('fa', 10), ('fi', 10), ('hu', 10), ('nb', 10), ('sl', 10), ('sr', 10), ('sv', 10), ('uk', 10), ('vi', 10), ('sq', 9), ('ar', 8), ('bn', 8), ('ca', 8), ('eu', 8), ('af', 8), ('be', 8), ('lv', 7), ('tr', 7), ('e
… [497 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/diag_items.py <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools')\nfrom semantique.typed_corpus import items\nfrom jeux.lexique_multilingue import MULTI\nits = items()\nby = collections.defaultdict(list)\nfor i in its: by[(i.jeu,i.langue)].append(i)\nfor k in sorted( … [357 caractères tronqués]`

  ```
('cartes', 'af') 5
('cartes', 'ar') 2
('cartes', 'be') 3
('cartes', 'bn') 5
('cartes', 'ca') 3
('cartes', 'cs') 5
('cartes', 'da') 5
('cartes', 'de') 5
('cartes', 'el') 2
('cartes', 'en') 7
('cartes', 'eo') 5
('cartes', 'es') 5
('cartes', 'et') 5
('cartes', 'eu') 3
('cartes', 'fa') 5
('cartes', 'fi') 5
('cartes', 'fr') 9
('cartes', 'hu') 5
('cartes', 'it') 5
('cartes', 'ja') 5
('cartes', 'lv') 2
('cartes', 'nb') 5
('cartes', 'nl') 5
('cartes', 'notation') 2
('cartes', 'pl') 5
('cartes', 'pt') 5
('cartes', 'ru') 5
('cartes', 'sk') 1
('cartes', 'sl') 5
('cartes', 'sq') 5
('cartes', 'sr') 5
('cartes', 'sv') 5
('cartes', 'th') 1
('cartes', 'tr') 1
('cartes', 'uk') 5
('cartes', 'vi') 5
('cartes', 'zh') 5
('dames', 'ar') 1
('dames', 'az') 1
('dames', 'be') 1
('dames', 'bs') 1
('dames', 'ca') 1
('dames', 'cs') 1
('dames', 'cy') 1
('dames', 'da') 1
('dames', 'de') 1
('dames', 'el') 1
('dames', 'en') 1
('dames', 'eo') 1
('dames', 'es') 1
('dames', 'et') 1
('dames', 'eu') 1
('dames', 'fa') 1
('dames', 'fi') 1
('dames', 'fr') 9
('dames', 'gl') 1
('dames', 'he') 1
('dames', 'hi') 1
('dames', 'hr') 1
('dames', 'hu') 1
('dames', 'hy') 1
('dames', 'id') 1
('dames', 'is') 1
('dames', 'it') 1
('dam
… [11406 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,220p tools/jeux/corpus_multilingue.py", "description": "Inspect multilingual corpus construction"}`

  ```
#!/usr/bin/env python3
"""corpus_multilingue.py — les mêmes connaissances, dans 71 langues.

Le corpus multilingue est **dérivé** du lexique Wikidata : pour chaque langue,
on prend les libellés disponibles et on construit des surfaces **à mots-clés**
(pièce + cases, rang + enseigne, nom du jeu + coordonnée). Ce n'est pas de la
grammaire : c'est la couche lexicale, celle qui doit déjà porter le sens avant
qu'une phrase soit possible.

Ce qui est **fort** : les pièces des échecs et les cartes, parce que le libellé
y porte tout le sens (un cavalier n'est pas un roi). Ce qui est **mixte** : les
noms de jeux + une coordonnée (go, dames, morpion), parce que la coordonnée est
déjà neutre ; cela vérifie qu'un mot étranger ne bloque pas la lecture.

Chaque item porte une **paire** (le même sens dans toutes les langues) : c'est
la mesure d'invariance inter-langues.
"""
from __future__ import annotations

from .corpus import Corpus
from .lexique_multilingue import MULTI
from .regles import cartes as C
from .regles import dames as D
from .regles import echecs as E
from .regles import go as G
from .regles import morpion as M
from .rsn import RSN


def _premier(concept: str, langue: str) -> str 
… [3561 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,210p tools/jeux/codecs/base.py; echo ---HUB---; sed -n 1,60p tools/cerveau/hub.py", "description": "Inspect codec base API and hub"}`

  ```
#!/usr/bin/env python3
"""base.py — le contrat d'un codec de jeu : surface ⇄ RSN.

Un codec est la **couche linguistique** d'un jeu. Il expose deux opérations et
une mesure :

- `lit(surface, niveau)` : de la surface vers une `Lecture` (les quatre couches
  + la RSN + les candidats) ;
- `rend(rsn, format)` : de la RSN vers une surface (la restitution) ;
- `detecte(surface)` : la confiance que cette surface parle de ce jeu.

Les niveaux sont **cumulatifs** : 0 ne lit que la forme canonique exacte, 1
ajoute la normalisation, 2 le lexique, 3 la grammaire des phrases, 4 la
sémantique (légalité, désambiguïsation, canonicalisation). L'ablation de
`mesure.py` vérifie que la couverture ne baisse pas quand on monte.
"""
from __future__ import annotations

import re

from dataclasses import dataclass, field
from typing import Any, Iterable

from ..grammaire import Jeton, jetons, naturel
from ..lexique import langue_probable
from ..lexique_multilingue import MULTI
from ..rsn import Annotation, RSN

NIVEAUX = {
    0: "surface (forme canonique exacte)",
    1: "normalisation (casse, espaces, ponctuation)",
    2: "lexique (synonymes, FR/EN)",
    3: "grammaire (phrases, ordre libre)",
    4: "
… [8777 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/diag_b7.py <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools')\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom jeux.codecs import codec\nfrom jeux.lexique_multilingue import MULTI\nfrom semantique.universaux import code_rsn\nc = construire_co … [403 caractères tronqués]`

  ```
B7 items: 449
[('de', 11), ('en', 11), ('es', 11), ('fr', 11), ('it', 11), ('ja', 11), ('nl', 11), ('pl', 11), ('pt', 11), ('ru', 11), ('zh', 11), ('cs', 10)]
en  echecs   'knight g1 f3'                   attendu={'jeu': 'echecs', 'action': 'deplacer', 'de': 62, 'vers': 45}
en  echecs   'pawn e2 e4'                     attendu={'jeu': 'echecs', 'action': 'deplacer', 'de': 52, 'vers': 36}
en  cartes   'ace heart'                      attendu={'jeu': 'cartes', 'action': 'jouer_carte', 'carte': 50}
en  cartes   'king spade'                     attendu={'jeu': 'cartes', 'action': 'jouer_carte', 'carte': 47}
en  cartes   'queen diamond'                  attendu={'jeu': 'cartes', 'action': 'jouer_carte', 'carte': 41}
en  cartes   'jack clubs'                     attendu={'jeu': 'cartes', 'action': 'jouer_carte', 'carte': 36}
en  cartes   '10 heart'                       attendu={'jeu': 'cartes', 'action': 'jouer_carte', 'carte': 34}
en  go       'go D4'                          attendu={'jeu': 'go', 'action': 'poser', 'taille': 9, 'point': 48}
en  go       'pass'                           attendu={'jeu': 'go', 'action': 'passer', 'taille': 9, 'passe': True}
en  dames    'english draughts
… [1474 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/diag_b7b.py <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools')\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom jeux.codecs import codec\nfrom jeux.lexique_multilingue import MULTI\nfrom jeux.lexique import langue_probable\nfrom semantique.un … [1060 caractères tronqués]`

  ```
n= 22
en echecs   'knight g1 f3'                 det=en   lp=('en', 1.0)    lit_ok=True  same=True fmt=francais lang=en
en echecs   'pawn e2 e4'                   det=en   lp=('en', 1.0)    lit_ok=True  same=True fmt=francais lang=en
en cartes   'ace heart'                    det=en   lp=('en', 1.0)    lit_ok=True  same=True fmt=carte lang=en
en cartes   'king spade'                   det=en   lp=('en', 1.0)    lit_ok=True  same=True fmt=carte lang=en
en cartes   'queen diamond'                det=en   lp=('en', 1.0)    lit_ok=True  same=True fmt=carte lang=en
en cartes   'jack clubs'                   det=en   lp=('en', 1.0)    lit_ok=True  same=True fmt=carte lang=en
en cartes   '10 heart'                     det=en   lp=('en', 1.0)    lit_ok=True  same=True fmt=carte lang=en
en go       'go D4'                        det=tr   lp=('inconnue', 0.0) lit_ok=True  same=True fmt=gtp lang=tr
en go       'pass'                         det=en   lp=('en', 1.0)    lit_ok=True  same=True fmt=gtp lang=en
en dames    'english draughts b6 c5'       det=de   lp=('inconnue', 0.0) lit_ok=True  same=True fmt=algebrique lang=de
en morpion  'tic-tac-toe A1'               det=vi   lp=('inconnue', 0.0
… [1340 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def action_depuis_coup\\|def rsn_depuis_position\\|class Coup\\|def __init__\\|chemin\" tools/jeux/regles/dames.py | head -40; echo ---; sed -n 1,120p tools/jeux/regles/dames.py", "description": "Inspect dames rules code"}`

  ```
7:mesurable : une notation `c3xe5xg7` n'est pas une chaîne, c'est un **chemin**
91:class Coup(NamedTuple):
92:    chemin: tuple[int, ...]
96:        return len(self.chemin) > 2
100:        return sep.join(str(i + 1) for i in self.chemin)
104:        return sep.join(indice_vers_case(i) for i in self.chemin)
127:    def __init__(self, cases: list[int], trait: int = NOIR, demi: int = 0) -> None:
153:                        chemin: list[int], prises: list[int], sortie: list[Coup]) -> None:
164:            # déjà été visitée par une dame (le chemin reste fini).
174:            nouvelle_chemin = chemin + [landing]
178:                sortie.append(Coup(tuple(nouvelle_chemin)))
180:            self._captures_piece(nouveau, landing, piece, nouvelle_chemin,
184:        if not prolonge and len(chemin) > 1:
185:            sortie.append(Coup(tuple(chemin)))
193:        # déduplique (deux ordres de prises peuvent produire le même chemin)
197:            if c.chemin not in vus:
198:                vus.add(c.chemin)
222:        for a, b in zip(coup.chemin, coup.chemin[1:]):
236:        piece = cases[coup.chemin[0]]
240:        for a, b in zip(coup.chemin, coup.chemin[1:]):
245:        cases[coup
… [4129 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def action_depuis_coup\" -A 20 tools/jeux/regles/echecs.py", "description": "Inspect echecs action derivation"}`

  ```
816:def action_depuis_coup(coup: Coup, annotation: Annotation | None = None) -> RSN:
817-    corps = {
818-        "de": coup.de,
819-        "vers": coup.vers,
820-        "promotion": {CAVALIER: "n", FOU: "b", TOUR: "r", DAME: "q"}.get(coup.promotion),
821-        "roque": {ROQUE_K: "K", ROQUE_Q: "Q"}.get(coup.drapeau),
822-    }
823-    return RSN("echecs", "coup", corps,
824-               annotation or Annotation(langue="notation", format="uci", surface=""))
825-
826-
827-def coup_depuis_action(rsn: RSN, pos: Position | None = None) -> Coup:
828-    c = rsn.corps
829-    de, vers = int(c["de"]), int(c["vers"])
830-    promo = {"n": CAVALIER, "b": FOU, "r": TOUR, "q": DAME}.get(c.get("promotion") or "")
831-    roque = c.get("roque")
832-    if pos is not None:
833-        for m in pos.coups_legaux():
834-            if roque and m.drapeau == (ROQUE_K if roque == "K" else ROQUE_Q):
835-                return m
836-            if m.de == de and m.vers == vers and (promo is None or m.promotion == promo):
  ```

- **bash** `{"command": "cat > /tmp/proto_m5.py <<'EOF'\nimport sys, collections, math, random, time\nsys.path.insert(0,'tools')\nfrom cerveau.sequences import corpus\n\nt0=time.time()\nseqs = corpus(0, 200, 12)\nprint(\"n seqs\", len(seqs), \"temps\", time.time()-t0)\n\ndef cible(pas, quoi):\n    c = pas.code; … [4099 caractères tronqués]`

  ```
n seqs 800 temps 2.4781277179718018
train/test seqs 640 160
action  n=1698 exact=0.9741 base=0.9741 gain=+0.0000 surprisal=0.088 base=0.087 dsur=-0.001
   echecs   n= 408 exact=1.0000 base=1.0000 gain=+0.0000 dsur=+0.000
   dames    n= 432 exact=1.0000 base=1.0000 gain=+0.0000 dsur=+0.000
   go       n= 492 exact=0.9106 base=0.9106 gain=+0.0000 dsur=-0.002
   morpion  n= 366 exact=1.0000 base=1.0000 gain=+0.0000 dsur=+0.000
source  n= 840 exact=0.1524 base=0.0583 gain=+0.0940 surprisal=3.711 base=3.506 dsur=-0.205
   echecs   n= 408 exact=0.0809 base=0.0490 gain=+0.0319 dsur=-0.765
   dames    n= 432 exact=0.2199 base=0.0671 gain=+0.1528 dsur=+0.324
[stderr]
Traceback (most recent call last):
  File "/tmp/proto_m5.py", line 97, in <module>
    rr=m.eval([s for s in test if s.jeu==jeu])
  File "/tmp/proto_m5.py", line 88, in eval
    return dict(n=tot, exact=ok/tot, exact_base=ok_base/tot, gain=ok/tot-ok_base/tot,
                             ~~^~~~
ZeroDivisionError: division by zero
[exit code: 1]
  ```

- **bash** `{"command": "cat > /tmp/proto_m5b.py <<'EOF'\nimport sys, collections, math, random\nsys.path.insert(0,'tools')\nfrom cerveau.sequences import corpus\n\nseqs = corpus(0, 200, 12)\nrng = random.Random(3)\nidx=list(range(len(seqs))); rng.shuffle(idx)\nn=int(len(seqs)*0.8); train=[seqs[i] for i in idx[ … [4698 caractères tronqués]`

  ```
action  ordre=0 n=1698 exact=0.9741 base=0.9741 gain=+0.0000 sur=0.087 surb=0.087 dsur=-0.000
action  ordre=1 n=1698 exact=0.9741 base=0.9741 gain=+0.0000 sur=0.088 surb=0.087 dsur=-0.000
action  ordre=2 n=1698 exact=0.9741 base=0.9741 gain=+0.0000 sur=0.088 surb=0.087 dsur=-0.001
   tour: {'n': 1698, 'exact': 0.9740871613663133}
   echecs   n= 408 exact=1.0000 base=1.0000 gain=+0.0000 tour=1.0000 residual=+0.0000 dsur=+0.000
   dames    n= 432 exact=1.0000 base=1.0000 gain=+0.0000 tour=1.0000 residual=+0.0000 dsur=+0.000
   go       n= 492 exact=0.9106 base=0.9106 gain=+0.0000 tour=0.9106 residual=+0.0000 dsur=-0.002
   morpion  n= 366 exact=1.0000 base=1.0000 gain=+0.0000 tour=1.0000 residual=+0.0000 dsur=+0.000
source  ordre=0 n= 840 exact=0.0583 base=0.0583 gain=+0.0000 sur=3.507 surb=3.506 dsur=-0.000
source  ordre=1 n= 840 exact=0.1357 base=0.0583 gain=+0.0774 sur=3.314 surb=3.506 dsur=+0.192
source  ordre=2 n= 840 exact=0.1524 base=0.0583 gain=+0.0940 sur=3.711 surb=3.506 dsur=-0.205
   tour: {'n': 840, 'exact': 0.11785714285714285}
   echecs   n= 408 exact=0.0809 base=0.0490 gain=+0.0319 tour=0.0882 residual=-0.0074 dsur=-0.201
   dames    n= 432 exact=0.1875 base=0.0671 ga
… [380 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/oracle.py <<'EOF'\nimport sys, collections, math\nsys.path.insert(0,'tools')\nfrom cerveau.sequences import partie\nfrom semantique.universaux import code_rsn\nfrom jeux.regles import echecs as E, dames as D, go as G, morpion as M\n\ndef val(rsn, quoi, jeu):\n    c=code_rsn(r … [3306 caractères tronqués]`

  ```
echecs action {'n': 480, 'oracle_exact': 1.0, 'oracle_entropie': 0.0, 'coups_moyens': 24.2167}
echecs source {'n': 480, 'oracle_exact': 0.1809, 'oracle_entropie': 2.3342, 'coups_moyens': 24.2167}
echecs cible {'n': 480, 'oracle_exact': 0.1156, 'oracle_entropie': 2.7835, 'coups_moyens': 24.2167}
dames action {'n': 480, 'oracle_exact': 1.0, 'oracle_entropie': 0.0, 'coups_moyens': 5.4667}
dames source {'n': 480, 'oracle_exact': 0.4671, 'oracle_entropie': 1.1288, 'coups_moyens': 5.4667}
dames cible {'n': 480, 'oracle_exact': 0.4656, 'oracle_entropie': 1.1047, 'coups_moyens': 5.4667}
go action {'n': 480, 'oracle_exact': 1.0, 'oracle_entropie': 0.0, 'coups_moyens': 1.0}
[stderr]
Traceback (most recent call last):
  File "/tmp/oracle.py", line 76, in <module>
    r=oracle(jeu,quoi)
  File "/tmp/oracle.py", line 71, in oracle
    return dict(n=len(accs), oracle_exact=sum(accs)/len(accs), oracle_entropie=sum(ents)/len(ents),
                                          ~~~~~~~~~^~~~~~~~~~
ZeroDivisionError: division by zero
[exit code: 1]
  ```

- **bash** `{"command": "cat > /tmp/diag_decode.py <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools')\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom jeux.codecs import codec\nfrom semantique.universaux import code_rsn\nc=construire_corpus_multilingue()\nitems=[i for i in c.it … [695 caractères tronqués]`

  ```
niveau 2 sans exact 12 / 22
   fail ('knight g1 f3', ['position requise pour un SAN'], None)
   fail ('pawn e2 e4', ['position requise pour un SAN'], None)
   fail ('go D4', [], {'jeu': 'go', 'action': 'poser', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': 19, 'point': 288, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None})
   fail ('pass', [], {'jeu': 'go', 'action': 'passer', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': 19, 'point': None, 'passe': True, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None})
   fail ('tic-tac-toe A1', [], {'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 0, 'symbole': None, 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None})
   fail ('cavalier g1 f3', ['position requise pour un SAN'], None)
niveau 2 avec exact 18 / 22
   fail ('knight g1 f3', ["SAN illisible : 'knight g1 f3'"], None)
   fail ('pawn e2 e4', ["SAN illisible : 'pawn e2 e4'"], None)
   fail ('cavalier g1 
… [3413 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/diag_matches.py <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nfrom jeux.lexique_multilingue import MULTI\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nc=construire_corpus_multilingue()\nfor i in c.items:\n    if i.langue not in ('fr','en'): continue\n … [571 caractères tronqués]`

  ```
en  echecs   'knight g1 f3'                 det=en   langs=['en']
       ('echecs.piece', 'N', 'en', 'knight')
en  echecs   'pawn e2 e4'                   det=en   langs=['en']
       ('echecs.piece', 'P', 'en', 'pawn')
en  cartes   'ace heart'                    det=en   langs=['en']
       ('cartes.rang', '14', 'en', 'ace')
       ('cartes.couleur', 'H', 'en', 'heart')
en  cartes   'king spade'                   det=en   langs=['en']
       ('echecs.piece', 'K', 'en', 'king')
       ('cartes.rang', '13', 'en', 'king')
       ('cartes.couleur', 'S', 'en', 'spade')
en  cartes   'queen diamond'                det=en   langs=['en']
       ('echecs.piece', 'Q', 'en', 'queen')
       ('cartes.rang', '12', 'en', 'queen')
       ('cartes.couleur', 'D', 'en', 'diamond')
en  cartes   'jack clubs'                   det=en   langs=['en']
       ('cartes.rang', '11', 'en', 'jack')
       ('cartes.couleur', 'C', 'en', 'clubs')
en  cartes   '10 heart'                     det=en   langs=['en']
       ('cartes.couleur', 'H', 'en', 'heart')
en  go       'go D4'                        det=is   langs=['af', 'bs', 'ca', 'cs', 'cy', 'da', 'de', 'en', 'es', 'et', 'eu', 'fi', 'fr', 'ga', 'gl', 'hr', 'hu
… [4798 caractères tronqués]
  ```

- **bash** `{"command": "for seed in 0 1 2 3 4 5; do PYTHONHASHSEED=$seed PYTHONPATH=tools python3 -c \"\nimport sys; sys.path.insert(0,'tools')\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom jeux.lexique_multilingue import MULTI\nc=construire_corpus_multilingue()\nprint('seed=$seed',  … [214 caractères tronqués]`

  ```
seed=0 [('go D4', 'ms'), ('pass', 'en'), ('english draughts b6 c5', 'de'), ('tic-tac-toe A1', 'ms'), ('go D4', 'ms'), ('passe', 'fr'), ('dames anglaises b6 c5', 'fr'), ('tic-tac-toe A1', 'ms')]
seed=1 [('go D4', 'gl'), ('pass', 'en'), ('english draughts b6 c5', 'en'), ('tic-tac-toe A1', 'ms'), ('go D4', 'gl'), ('passe', 'fr'), ('dames anglaises b6 c5', 'fr'), ('tic-tac-toe A1', 'ms')]
seed=2 [('go D4', 'hr'), ('pass', 'en'), ('english draughts b6 c5', 'de'), ('tic-tac-toe A1', 'en'), ('go D4', 'hr'), ('passe', 'fr'), ('dames anglaises b6 c5', 'fr'), ('tic-tac-toe A1', 'en')]
seed=3 [('go D4', 'af'), ('pass', 'en'), ('english draughts b6 c5', 'en'), ('tic-tac-toe A1', 'ms'), ('go D4', 'af'), ('passe', 'fr'), ('dames anglaises b6 c5', 'fr'), ('tic-tac-toe A1', 'ms')]
seed=4 [('go D4', 'cs'), ('pass', 'en'), ('english draughts b6 c5', 'en'), ('tic-tac-toe A1', 'en'), ('go D4', 'cs'), ('passe', 'fr'), ('dames anglaises b6 c5', 'fr'), ('tic-tac-toe A1', 'en')]
seed=5 [('go D4', 'pt'), ('pass', 'en'), ('english draughts b6 c5', 'en'), ('tic-tac-toe A1', 'de'), ('go D4', 'pt'), ('passe', 'fr'), ('dames anglaises b6 c5', 'fr'), ('tic-tac-toe A1', 'de')]
  ```

- **bash** `{"command": "grep -n \"def langue_probable\" -A 40 tools/jeux/lexique.py; echo ---; grep -n \"def normalise_forme\" -A 30 tools/jeux/lexique.py", "description": "Inspect langue_probable implementation"}`

  ```
548:def langue_probable(texte: str) -> tuple[str, float]:
549-    """« fr », « en », « notation » ou « inconnue », avec une confiance grossière."""
550-    ws = set(mots(texte))
551-    fr = len(ws & _MOTS_FR)
552-    en = len(ws & _MOTS_EN)
553-    if fr == 0 and en == 0:
554-        # Une notation formelle : beaucoup de chiffres/symboles, peu de lettres.
555-        lettres = sum(c.isalpha() for c in texte)
556-        chiffres = sum(c.isdigit() for c in texte)
557-        signes = sum(not c.isalnum() and not c.isspace() for c in texte)
558-        if chiffres + signes > 0 and lettres <= max(2, (chiffres + signes)):
559-            return "notation", 0.8
560-        return "inconnue", 0.0
561-    total = fr + en
562-    if fr == en:
563-        return "fr", 0.5  # égalité : on privilégie la langue du dépôt
564-    return ("fr" if fr > en else "en"), max(fr, en) / total
565-
566-
567-# ---------------------------------------------------------------------------
568-# Petites aides de lecture, partagées par les codecs.
569-# ---------------------------------------------------------------------------
570-def est_article(forme: str) -> bool:
571-    return bool(LEX.cherche("commun.art
… [2022 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/diag_chan.py <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools')\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom jeux.lexique_multilingue import MULTI\nfrom jeux.lexique import langue_probable, normalise_forme\nfrom jeux.rsn import RSN\nc=con … [1385 caractères tronqués]`

  ```
lp 16 / 22
     ('en', 'go D4', None)
     ('en', 'english draughts b6 c5', None)
     ('en', 'tic-tac-toe A1', None)
     ('fr', 'go D4', None)
     ('fr', 'dames anglaises b6 c5', None)
     ('fr', 'tic-tac-toe A1', None)
vote 15 / 22
     ('en', 'go D4', 'af')
     ('en', 'english draughts b6 c5', 'de')
     ('en', 'tic-tac-toe A1', 'de')
     ('fr', 'pion e2 e4', 'af')
     ('fr', 'dame carreau', 'de')
     ('fr', 'go D4', 'af')
     ('fr', 'tic-tac-toe A1', 'de')
combine 17 / 22
     ('en', 'go D4', 'af')
     ('en', 'english draughts b6 c5', 'de')
     ('en', 'tic-tac-toe A1', 'de')
     ('fr', 'go D4', 'af')
     ('fr', 'tic-tac-toe A1', 'de')
multi 16 / 22
     ('en', 'go D4', 'it')
     ('en', 'english draughts b6 c5', 'de')
     ('en', 'tic-tac-toe A1', 'tr')
     ('fr', 'pion e2 e4', 'af')
     ('fr', 'go D4', 'it')
     ('fr', 'tic-tac-toe A1', 'tr')

en 'knight g1 f3'               lp=('en', 1.0) vote=('en', 1) combi=en multi=en
en 'pawn e2 e4'                 lp=('en', 1.0) vote=('en', 1) combi=en multi=en
en 'ace heart'                  lp=('en', 1.0) vote=('en', 2) combi=en multi=en
en 'king spade'                 lp=('en', 1.0) vote=('en', 3) combi=en multi=en
en '
… [1471 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Designing the final M5 protocol (multi-target, order 0/1/2, controls).

- **bash** `{"command": "cat > /tmp/proto_m5c.py <<'EOF'\nimport sys, collections, math, random\nsys.path.insert(0,'tools')\nfrom cerveau.sequences import corpus\n\nCHAMPS_SOURCE={\"echecs\":\"de\",\"dames\":\"chemin_0\"}\ndef valeur(pas, quoi):\n    c=pas.code; j=c[\"jeu\"]\n    if quoi==\"action\": return c[\ … [3746 caractères tronqués]`

  ```
train 640 test 160
action o=0 n=1538 exact=0.9746 base=0.9746 gain=+0.0000 sur=0.086 base=0.086 dsur=-0.000
action o=1 n=1538 exact=0.9746 base=0.9746 gain=+0.0000 sur=0.087 base=0.086 dsur=-0.001
action o=2 n=1538 exact=0.9746 base=0.9746 gain=+0.0000 sur=0.087 base=0.086 dsur=-0.001
    echecs   n= 374 exact=1.0000 base=1.0000 gain=+0.0000 dsur=+0.000
    dames    n= 396 exact=1.0000 base=1.0000 gain=+0.0000 dsur=+0.000
    go       n= 451 exact=0.9135 base=0.9135 gain=+0.0000 dsur=-0.002
    morpion  n= 317 exact=1.0000 base=1.0000 gain=+0.0000 dsur=+0.000
source o=0 n= 770 exact=0.0649 base=0.0649 gain=+0.0000 sur=3.539 base=3.539 dsur=-0.001
source o=1 n= 770 exact=0.1260 base=0.0649 gain=+0.0610 sur=3.334 base=3.539 dsur=+0.205
source o=2 n= 770 exact=0.1442 base=0.0649 gain=+0.0792 sur=3.768 base=3.539 dsur=-0.229
    echecs   n= 374 exact=0.0749 base=0.0428 gain=+0.0321 dsur=-0.214
    dames    n= 396 exact=0.1742 base=0.0859 gain=+0.0884 dsur=+0.599
[stderr]
Traceback (most recent call last):
  File "/tmp/proto_m5c.py", line 78, in <module>
    r=m.eval(ss)
  File "/tmp/proto_m5c.py", line 64, in eval
    return dict(n=n,exact=ok/n,base=base/n,gain=ok/n-base/n,
           
… [70 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/proto_m5d.py <<'EOF'\nimport sys, collections, math, random\nsys.path.insert(0,'tools')\nfrom cerveau.sequences import corpus\n\nCHAMPS_SOURCE={\"echecs\":\"de\",\"dames\":\"chemin_0\"}\ndef valeur(pas, quoi):\n    c=pas.code; j=c[\"jeu\"]\n    if quoi==\"action\": return c[\ … [4514 caractères tronqués]`

  ```
source o=1 n= 770 exact=0.1260 base=0.0649 gain=+0.0610 sur=3.334 dsur=+0.205
source o=2 n= 770 exact=0.1442 base=0.0649 gain=+0.0792 sur=3.768 dsur=-0.229
  tour global {'n': 840, 'exact': 0.11785714285714285}
    echecs   n= 374 exact=0.0749 base=0.0428 gain=+0.0321 tour=0.0882 resid=-0.0134 dsur=-0.214
    dames    n= 396 exact=0.1742 base=0.0859 gain=+0.0884 tour=0.1458 resid=+0.0284 dsur=+0.599
[stderr]
Traceback (most recent call last):
  File "/tmp/proto_m5d.py", line 98, in <module>
    r=m.eval(ss); tt=t.eval(ss)
  File "/tmp/proto_m5d.py", line 64, in eval
    return dict(n=n,exact=ok/n,base=base/n,gain=ok/n-base/n,
                          ~~^~
ZeroDivisionError: division by zero
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport re\nsrc=open('/tmp/proto_m5d.py').read()\nsrc=src.replace('        r=m.eval(ss); tt=t.eval(ss)\\n        print(\"    %-8s', '        r=m.eval(ss); tt=t.eval(ss)\\n        if not r[\"n\"] or not tt[\"n\"]: continue\\n        print(\"    %-8s')\nopen(' … [132 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "/tmp/proto_m5d.py", line 3, in <module>
    from cerveau.sequences import corpus
ModuleNotFoundError: No module named 'cerveau'
[exit code: 1]
  ```

### 👤 Utilisateur

Agent f0969e87-af0c-43b1-93cf-f278d9c90846 sent a message: 
Timebox : donne un point de progression maintenant. Si un résultat est mesuré, écris immédiatement /tmp/a1-m5-m6.json et /tmp/a1-m5-m6.md avec les chiffres et termine ; ne bloque pas sur une amélioration parfaite. Un négatif net suffit.

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "Point M5/M6 (mesuré, code en cours de finalisation).\n\nM5 — cause du 98,9 % identifiée : le champ `action` est structurellement constant par jeu (échecs=toujours \"deplacer\", dames=toujours \"prendre\" — `action()` classe par forme d … [2275 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

### 🤖 Assistant

⏵ Implementing the new `predictif.py` (multi-target, orders, permutation control).

- **write** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py", "content": "#!/usr/bin/env python3\n\"\"\"M5 — codage prédictif : prédire une cible **variable**, mesurer l'erreur.\n\nLeçon mesurée (sprint 24 h, corpus `sequences.corpus`) : l'ancienne cible\n`action` est **structurellement  … [17600 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

### 🤖 Assistant

⏵ Implementing the new `gating.py` conflict task and controls.

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"M6 — porte exécutive : une vraie tâche de conflit langue/tâche sur B7.\n\nL'ancienne porte ne mesurait qu'une chose : `MULTI.detecte_langue(surface)`\ncomparée à la langue cible. Son « exactitude » de 72,9 % était donc le taux du\nclassifieur lexical, pas u … [20854 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

### 🤖 Assistant

⏵ Smoke-testing both modules and measuring the new task.

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport sys, json, time\nsys.path.insert(0,'tools')\nfrom cerveau.gating import Porte\nt0=time.time()\np=Porte()\nr=p.executer()\nprint(json.dumps({k:v for k,v in r.items() if k not in (\"par_condition\",)}, ensure_a … [181 caractères tronqués]`

  ```
{
 "exact": 0.9431818181818182,
 "n": 88,
 "vrais_positifs": 17,
 "faux_positifs": 0,
 "faux_negatifs": 5,
 "vrais_negatifs": 66,
 "sensibilite": 0.7727272727272727,
 "specificite": 1.0,
 "exactitude_equilibree": 0.8863636363636364,
 "mcc": 0.8475316272298808,
 "sensibilite_ic95": [
  0.5655964393704065,
  0.8987710920517964
 ],
 "specificite_ic95": [
  0.9449955327483907,
  1.0
 ],
 "taux_base_tout_non": 0.8068181818181818,
 "par_langue": {
  "fr": {
   "n": 44,
   "corrects": 42,
   "tp": 9,
   "fn": 2,
   "exact": 0.9545454545454546,
   "sensibilite": 0.8181818181818182
  },
  "en": {
   "n": 44,
   "corrects": 41,
   "tp": 8,
   "fn": 3,
   "exact": 0.9318181818181818,
   "sensibilite": 0.7272727272727273
  }
 },
 "politique": "conjonction",
 "cibles": [
  "fr",
  "en"
 ],
 "cout_commutation": 0.002705627705627704,
 "cout_commutation_details": {
  "cout": 0.002705627705627704,
  "n_commutations": 21,
  "n_repetitions": 22,
  "erreur_commutation": 0.05952380952380952,
  "erreur_repetition": 0.056818181818181816
 },
 "controle_perseveration": 0.38365800865800864,
 "politiques": {
  "langue": {
   "exact": 0.75,
   "faux_positifs": 17,
   "faux_negatifs": 5,
   "sensibilite": 0.77
… [957 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nfrom cerveau.gating import Porte, CONDITIONS\np=Porte(); essais=p.tache_conflit()\nblocs=[essais[i:i+4] for i in range(0,len(essais),4)]\nrejoues=[]\nfor b in blocs: rejoues + … [697 caractères tronqués]`

  ```
=== conjonction
0 L=fr prec=None none err=0 go=['valet trefle'] det=['fr']
1 L=fr prec=fr rep err=0 go=['valet trefle'] det=['fr']
2 L=en prec=fr SW err=0 go=['jack clubs'] det=['en']
3 L=en prec=en rep err=0 go=['jack clubs'] det=['en']
4 L=fr prec=en SW err=0 go=['dame carreau'] det=['fr']
5 L=fr prec=fr rep err=0 go=['dame carreau'] det=['fr']
6 L=en prec=fr SW err=0 go=['queen diamond'] det=['en']
7 L=en prec=en rep err=0 go=['queen diamond'] det=['en']
8 L=fr prec=en SW err=0 go=['10 coeur'] det=['fr']
9 L=fr prec=fr rep err=0 go=['10 coeur'] det=['fr']
10 L=en prec=fr SW err=0 go=['10 heart'] det=['en']
11 L=en prec=en rep err=0 go=['10 heart'] det=['en']
12 L=fr prec=en SW err=0 go=['passe'] det=['fr']
13 L=fr prec=fr rep err=0 go=['passe'] det=['fr']
14 L=en prec=fr SW err=0 go=['pass'] det=['en']
15 L=en prec=en rep err=0 go=['pass'] det=['en']
16 L=fr prec=en SW err=0 go=['pion e2 e4'] det=['fr']
17 L=fr prec=fr rep err=0 go=['pion e2 e4'] det=['fr']
18 L=en prec=fr SW err=0 go=['pawn e2 e4'] det=['en']
19 L=en prec=en rep err=0 go=['pawn e2 e4'] det=['en']
20 L=fr prec=en SW err=1 go=['go D4'] det=['af']
21 L=fr prec=fr rep err=1 go=['go D4'] det=['af']
22 L=en prec=fr S
… [3677 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nfrom cerveau.gating import Porte\np=Porte(); essais=p.tache_conflit()\nprint(\"conj\", p._cout_commutation(essais,\"conjonction\"))\nprint(\"pers\", p._cout_commutation(essais … [851 caractères tronqués]`

  ```
conj {'cout': 0.002705627705627704, 'n_commutations': 21, 'n_repetitions': 22, 'erreur_commutation': 0.05952380952380952, 'erreur_repetition': 0.056818181818181816}
pers {'cout': 0.38365800865800864, 'n_commutations': 21, 'n_repetitions': 22, 'erreur_commutation': 0.44047619047619047, 'erreur_repetition': 0.056818181818181816}
conjonction SW 21 0.05952380952380952 rep 22 0.056818181818181816 cost 0.002705627705627704
perseveration SW 21 0.44047619047619047 rep 22 0.056818181818181816 cost 0.38365800865800864
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nfrom cerveau.gating import Porte\np=Porte(); essais=p.tache_conflit()\nblocs=[essais[i:i+4] for i in range(0,len(essais),4)]\nrejoues=[]\nfor b in blocs: rejoues += [b,b]\npre … [596 caractères tronqués]`

  ```
0 none prec None L fr err 0 [('go', 'valet trefle', 'fr', 'fr', True, True), ('traduction', 'jack clubs', 'fr', 'en', False, False), ('langue', 'dame carreau', 'fr', 'fr', False, False), ('ni', 'queen diamond', 'fr', 'en', False, False)]
1 rep prec fr L fr err 0 [('go', 'valet trefle', 'fr', 'fr', True, True), ('traduction', 'jack clubs', 'fr', 'en', False, False), ('langue', 'dame carreau', 'fr', 'fr', False, False), ('ni', 'queen diamond', 'fr', 'en', False, False)]
2 SW prec fr L en err 2 [('traduction', 'valet trefle', 'en', 'fr', True, False), ('langue', '10 heart', 'en', 'en', False, False), ('ni', '10 coeur', 'en', 'fr', False, False), ('go', 'jack clubs', 'en', 'en', False, True)]
3 rep prec en L en err 0 [('traduction', 'valet trefle', 'en', 'fr', False, False), ('langue', '10 heart', 'en', 'en', False, False), ('ni', '10 coeur', 'en', 'fr', False, False), ('go', 'jack clubs', 'en', 'en', True, True)]
4 SW prec en L fr err 2 [('traduction', 'queen diamond', 'fr', 'en', True, False), ('langue', '10 coeur', 'fr', 'fr', False, False), ('ni', '10 heart', 'fr', 'en', False, False), ('go', 'dame carreau', 'fr', 'fr', False, True)]
5 rep prec fr L fr err 0 [('traduction', 'queen 
… [835 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nfrom cerveau.gating import Porte\np=Porte(); essais=p.tache_conflit()\nblocs=[essais[i:i+4] for i in range(0,len(essais),4)]\nrejoues=[]\nfor b in blocs: rejoues += [b,b]\npre … [570 caractères tronqués]`

  ```
[('none', 0.0), ('rep', 0.0), ('SW', 0.5), ('rep', 0.0), ('SW', 0.5), ('rep', 0.0), ('SW', 0.5), ('rep', 0.0), ('SW', 0.5), ('rep', 0.0), ('SW', 0.5), ('rep', 0.0), ('SW', 0.5), ('rep', 0.0), ('SW', 0.5), ('rep', 0.0), ('SW', 0.5), ('rep', 0.0), ('SW', 0.5), ('rep', 0.0), ('SW', 0.25), ('rep', 0.25), ('SW', 0.25), ('rep', 0.25), ('SW', 0.5), ('rep', 0.0), ('SW', 0.5), ('rep', 0.0), ('SW', 0.25), ('rep', 0.0), ('SW', 0.5), ('rep', 0.25), ('SW', 0.5), ('rep', 0.0), ('SW', 0.5), ('rep', 0.0), ('SW', 0.25), ('rep', 0.25), ('SW', 0.25), ('rep', 0.25), ('SW', 0.5), ('rep', 0.0), ('SW', 0.5), ('rep', 0.0)]
SW [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.25, 0.25, 0.5, 0.5, 0.25, 0.5, 0.5, 0.5, 0.25, 0.25, 0.5, 0.5] 0.44047619047619047
RP [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.25, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.25, 0.25, 0.0, 0.0] 0.056818181818181816
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/cerveau/gating.py')\ns=p.read_text()\ns=s.replace('\"taux_base_tout_non\": (tn + fn) / n if n else 0.0,',\n            '\"taux_base_tout_non\": (tn + fp) / n if n else 0.0,')\ns=s.replace('''    … [2008 caractères tronqués]`

  ```
{'exact': 0.9431818181818182, 'n': 88, 'vrais_positifs': 17, 'faux_positifs': 0, 'faux_negatifs': 5, 'vrais_negatifs': 66, 'sensibilite': 0.7727272727272727, 'specificite': 1.0, 'exactitude_equilibree': 0.8863636363636364, 'mcc': 0.8475316272298808, 'taux_base_tout_non': 0.75, 'cout_commutation': 0.0, 'controle_perseveration': 0.38095238095238093, 'canaux': {'langue_n': 22, 'langue_exact': 0.7727272727272727, 'lecture_n': 20, 'lecture_exact': 1.0, 'surfaces_ambigues': ['go D4', 'tic-tac-toe A1']}}
{'cout': 0.0, 'n_commutations': 21, 'n_repetitions': 21, 'erreur_commutation': 0.05952380952380952, 'erreur_repetition': 0.05952380952380952}
{'langue': {'exact': 0.75, 'faux_positifs': 17, 'faux_negatifs': 5, 'sensibilite': 0.7727272727272727, 'specificite': 0.7424242424242424, 'exactitude_equilibree': 0.7575757575757576}, 'sens': {'exact': 0.75, 'faux_positifs': 22, 'faux_negatifs': 0, 'sensibilite': 1.0, 'specificite': 0.6666666666666666, 'exactitude_equilibree': 0.8333333333333333}, 'tout_non': {'exact': 0.75, 'faux_positifs': 0, 'faux_negatifs': 22, 'sensibilite': 0.0, 'specificite': 1.0, 'exactitude_equilibree': 0.5}}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport sys, json, time\nsys.path.insert(0,'tools')\nfrom cerveau.sequences import corpus\nfrom cerveau.predictif import Predictif, baseline_tour, controle_negatif, valeur\nt0=time.time()\nseqs=corpus(0,200,12)\nprin … [1160 caractères tronqués]`

  ```
diag
action {'dames': {'n': 2400, 'distincts': 1, 'majoritaire': 1.0, 'entropie': -0.0}, 'echecs': {'n': 2400, 'distincts': 1, 'majoritaire': 1.0, 'entropie': -0.0}, 'go': {'n': 2400, 'distincts': 2, 'majoritaire': 0.9071, 'entropie': 0.3092}, 'morpion': {'n': 1533, 'distincts': 1, 'majoritaire': 1.0, 'entropie': -0.0}}
source {'dames': {'n': 2400, 'distincts': 32, 'majoritaire': 0.0754, 'entropie': 3.2393}, 'echecs': {'n': 2400, 'distincts': 64, 'majoritaire': 0.0429, 'entropie': 3.7974}}
cible {'dames': {'n': 2400, 'distincts': 27, 'majoritaire': 0.1021, 'entropie': 2.8767}, 'echecs': {'n': 2400, 'distincts': 64, 'majoritaire': 0.0425, 'entropie': 3.8006}, 'go': {'n': 2177, 'distincts': 81, 'majoritaire': 0.0184, 'entropie': 4.3785}, 'morpion': {'n': 1533, 'distincts': 9, 'majoritaire': 0.1194, 'entropie': 2.1965}}
action o=0 n=1538 exact=0.9746 maj=0.9746 gain=+0.0000 sur=0.086 surb=0.086 dsur=+0.000
action o=1 n=1538 exact=0.9746 maj=0.9746 gain=+0.0000 sur=0.087 surb=0.086 dsur=-0.000
action o=2 n=1538 exact=0.9746 maj=0.9746 gain=+0.0000 sur=0.087 surb=0.086 dsur=-0.001
   tour n=1698 exact=0.9741
source o=0 n= 770 exact=0.0649 maj=0.0649 gain=+0.0000 sur=3.539 surb=3.539 dsu
… [505 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/cerveau/predictif.py')\ns=p.read_text()\ns=s.replace('''                dist = self.distribution(jeu, cur, precedent)\n                if not dist:\n                    continue\n                … [3880 caractères tronqués]`

  ```
action o=0 n=1538 hv=0 exact=0.9746 maj=0.9746 gain=+0.0000 sur=0.086 surb=0.086 dsur=+0.000
action o=1 n=1538 hv=0 exact=0.9746 maj=0.9746 gain=+0.0000 sur=0.087 surb=0.086 dsur=-0.000
action o=2 n=1538 hv=0 exact=0.9746 maj=0.9746 gain=+0.0000 sur=0.087 surb=0.086 dsur=-0.001
   tour n=1538 exact=0.9746
     echecs   n= 374 exact=1.0000 maj=1.0000 gain=+0.0000 tour=1.0000 resid=+0.0000 dsur=+0.000
     dames    n= 396 exact=1.0000 maj=1.0000 gain=+0.0000 tour=1.0000 resid=+0.0000 dsur=+0.000
     go       n= 451 exact=0.9135 maj=0.9135 gain=+0.0000 tour=0.9135 resid=+0.0000 dsur=-0.002
     morpion  n= 317 exact=1.0000 maj=1.0000 gain=+0.0000 tour=1.0000 resid=+0.0000 dsur=+0.000
source o=0 n= 770 hv=0 exact=0.0649 maj=0.0649 gain=+0.0000 sur=3.539 surb=3.539 dsur=+0.000
source o=1 n= 770 hv=0 exact=0.1260 maj=0.0649 gain=+0.0610 sur=3.334 surb=3.539 dsur=+0.205
source o=2 n= 770 hv=0 exact=0.1442 maj=0.0649 gain=+0.0792 sur=3.768 surb=3.539 dsur=-0.228
   tour n=770 exact=0.1065
     echecs   n= 374 exact=0.0749 maj=0.0428 gain=+0.0321 tour=0.0829 resid=-0.0080 dsur=-0.213
     dames    n= 396 exact=0.1742 maj=0.0859 gain=+0.0884 tour=0.1288 resid=+0.0455 dsur=+0.600
cible  o=0 
… [1216 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport sys, random\nsys.path.insert(0,'tools')\nfrom cerveau.sequences import corpus\nfrom cerveau.predictif import Predictif\nseqs=corpus(0,200,12)\nidx=list(range(len(seqs))); random.Random(3).shuffle(idx); n=int( … [544 caractères tronqués]`

  ```
source o=1 k= 1 n= 770 exact=0.1260 maj=0.0649 gain=+0.0610 sur=3.334 dsur=+0.205
source o=1 k= 3 n= 770 exact=0.1260 maj=0.0649 gain=+0.0610 sur=3.204 dsur=+0.335
source o=1 k= 5 n= 770 exact=0.1260 maj=0.0649 gain=+0.0610 sur=3.156 dsur=+0.383
source o=1 k=10 n= 770 exact=0.1260 maj=0.0649 gain=+0.0610 sur=3.112 dsur=+0.428
source o=1 k=20 n= 770 exact=0.1260 maj=0.0649 gain=+0.0610 sur=3.098 dsur=+0.441
source o=1 k=50 n= 770 exact=0.1260 maj=0.0649 gain=+0.0610 sur=3.139 dsur=+0.401

source o=2 k= 1 n= 770 exact=0.1442 maj=0.0649 gain=+0.0792 sur=3.768 dsur=-0.228
source o=2 k= 3 n= 770 exact=0.1442 maj=0.0649 gain=+0.0792 sur=3.352 dsur=+0.187
source o=2 k= 5 n= 770 exact=0.1429 maj=0.0649 gain=+0.0779 sur=3.218 dsur=+0.322
source o=2 k=10 n= 770 exact=0.1442 maj=0.0649 gain=+0.0792 sur=3.099 dsur=+0.440
source o=2 k=20 n= 770 exact=0.1416 maj=0.0649 gain=+0.0766 sur=3.052 dsur=+0.487
source o=2 k=50 n= 770 exact=0.1377 maj=0.0649 gain=+0.0727 sur=3.086 dsur=+0.454

cible  o=1 k= 1 n=1465 exact=0.0792 maj=0.0703 gain=+0.0089 sur=3.917 dsur=-0.542
cible  o=1 k= 3 n=1465 exact=0.0792 maj=0.0703 gain=+0.0089 sur=3.649 dsur=-0.274
cible  o=1 k= 5 n=1465 exact=0.0792 maj=0.0703 gai
… [770 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/cerveau/predictif.py')\ns=p.read_text()\n# default kappa\ns=s.replace('def __init__(self, cible: str = \"cible\", ordre: int = 1, kappa: float = 1.0) -> None:',\n            'def __init__(self,  … [3548 caractères tronqués]`

  ```
action o=0 n=1538 hv=0 exact=0.9746 maj=0.9746 gain=+0.0000 sur=0.086 surb=0.086 dsur=+0.000
action o=1 n=1538 hv=0 exact=0.9746 maj=0.9746 gain=+0.0000 sur=0.087 surb=0.086 dsur=-0.000
action o=2 n=1538 hv=0 exact=0.9746 maj=0.9746 gain=+0.0000 sur=0.087 surb=0.086 dsur=-0.001
   tour n=1538 exact=0.9746
     echecs   n= 374 exact=1.0000 maj=1.0000 gain=+0.0000 tour=1.0000 resid=+0.0000 dsur=+0.000
     dames    n= 396 exact=1.0000 maj=1.0000 gain=+0.0000 tour=1.0000 resid=+0.0000 dsur=+0.000
     go       n= 451 exact=0.9135 maj=0.9135 gain=+0.0000 tour=0.9135 resid=+0.0000 dsur=-0.001
     morpion  n= 317 exact=1.0000 maj=1.0000 gain=+0.0000 tour=1.0000 resid=+0.0000 dsur=+0.000
source o=0 n= 770 hv=0 exact=0.0649 maj=0.0649 gain=+0.0000 sur=3.539 surb=3.539 dsur=+0.000
source o=1 n= 770 hv=0 exact=0.1260 maj=0.0649 gain=+0.0610 sur=3.112 surb=3.539 dsur=+0.428
source o=2 n= 770 hv=0 exact=0.1442 maj=0.0649 gain=+0.0792 sur=3.099 surb=3.539 dsur=+0.440
   tour n=770 exact=0.1065
     echecs   n= 374 exact=0.0749 maj=0.0428 gain=+0.0321 tour=0.0829 resid=-0.0080 dsur=+0.184
     dames    n= 396 exact=0.1742 maj=0.0859 gain=+0.0884 tour=0.1288 resid=+0.0455 dsur=+0.658
cible  o=0 
… [679 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport sys, random, collections\nsys.path.insert(0,'tools')\nfrom cerveau.sequences import corpus\nfrom cerveau.predictif import Predictif, baseline_tour, controle_negatif, valeur\nseqs=corpus(0,200,12)\nidx=list(ra … [1789 caractères tronqués]`

  ```
o2 source echecs n=374 exact=0.0722 maj=0.0428 gain=+0.0294 dsur=+0.116
o2 source dames n=396 exact=0.2121 maj=0.0859 gain=+0.1263 dsur=+0.746
o2 cible echecs n=373 exact=0.0751 maj=0.0349 gain=+0.0402 dsur=-0.036
o2 cible dames n=396 exact=0.2222 maj=0.0934 gain=+0.1288 dsur=+0.364
o2 cible go n=379 exact=0.0158 maj=0.0158 gain=+0.0000 dsur=-0.521
o2 cible morpion n=317 exact=0.1420 maj=0.0915 gain=+0.0505 dsur=+0.046

tour_excl echecs (374, 0.08288770053475936)
tour_excl dames (396, 0.12878787878787878)

controle {'cible': 'source', 'ordre': 2, 'permutations': 20, 'gain_observe': 0.0792, 'gain_surprise_observe': 0.4401, 'gain_null_moyen': -0.0118, 'gain_null_ecart': 0.0111, 'gain_surprise_null_moyen': -0.3998, 'p_value_gain': 0.0, 'p_value_gain_surprise': 0.0}
controle {'cible': 'cible', 'ordre': 2, 'permutations': 20, 'gain_observe': 0.056, 'gain_surprise_observe': -0.0355, 'gain_null_moyen': -0.0039, 'gain_null_ecart': 0.0062, 'gain_surprise_null_moyen': -0.3571, 'p_value_gain': 0.0, 'p_value_gain_surprise': 0.0}
controle {'cible': 'cible', 'ordre': 1, 'permutations': 20, 'gain_observe': 0.0212, 'gain_surprise_observe': -0.0431, 'gain_null_moyen': -0.0043, 'gain_null_ecart': 0.
… [93 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0,'tools')\nfrom cerveau.gating import Porte\nfrom semantique.typed_corpus import items\nits=[i for i in items() if i.langue in (\"fr\",\"en\")]\nr=Porte().executer(its,(\"fr\",\"en … [680 caractères tronqués]`

  ```
typed compat n 88 exact 0.9432 fp 0 fn 5 cout 0.0 persev 0.381
tache 88 88
mesurer ok 94 0.0319
{"graine": 3, "fraction": 0.8, "n_sequences_train": 64, "n_sequences_test": 16, "cibles": {"action": {"ordre_0": {"exact": 0.9904761904761905, "majoritaire": 0.9904761904761905, "surprise": 0.03510321
  ```

### 🤖 Assistant

⏵ Writing the unit tests for both modules.

- **write** `{"content": "from __future__ import annotations\n\nimport unittest\n\nfrom cerveau.predictif import (Predictif, baseline_tour, controle_negatif,\n                               permuter, valeur)\nfrom cerveau.sequences import Pas, Sequence, corpus\n\n\ndef _pas(jeu: str, action: str = \"deplacer\",  … [5753 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_predictif.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "from __future__ import annotations\n\nimport unittest\n\nfrom cerveau.gating import CONDITIONS, Porte\n\n\nclass TestTacheConflit(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls):\n        cls.porte = Porte()\n        cls.essais = cls.porte.tache_conflit()\n\n    def test_ … [3518 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_gating.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 -m unittest discover -s tools/cerveau/tests -t tools -v 2>&1 | tail -40", "description": "Run cerveau test suite"}`

  ```
test_executer (cerveau.tests.test_gating.TestTacheConflit.test_executer) ... ok
test_langue_deterministe (cerveau.tests.test_gating.TestTacheConflit.test_langue_deterministe) ... ok
test_politiques_simples_au_taux_de_base (cerveau.tests.test_gating.TestTacheConflit.test_politiques_simples_au_taux_de_base) ... ok
test_surfaces_ambigues (cerveau.tests.test_gating.TestTacheConflit.test_surfaces_ambigues) ... ok
test_taille_et_equilibre (cerveau.tests.test_gating.TestTacheConflit.test_taille_et_equilibre) ... ok
test_bruit_detruit_l_exactitude (cerveau.tests.test_memoire_travail.TestMemoireTravail.test_bruit_detruit_l_exactitude) ... ok
test_interference_positionnelle (cerveau.tests.test_memoire_travail.TestMemoireTravail.test_interference_positionnelle) ... ok
test_leurre_proche_distance_un (cerveau.tests.test_memoire_travail.TestMemoireTravail.test_leurre_proche_distance_un) ... ok
test_saturation_capacite (cerveau.tests.test_memoire_travail.TestMemoireTravail.test_saturation_capacite) ... ok
test_span_est_la_capacite (cerveau.tests.test_memoire_travail.TestMemoireTravail.test_span_est_la_capacite) ... ok
test_span_reel_ne_depend_pas_du_contenu (cerveau.tests.test_memoire_travail.Tes
… [2313 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/cerveau/tests/test_predictif.py')\ns=p.read_text().replace('self.assertAlmostEqual(r1[\"majoritaire\"], 0.5)',\n                        'self.assertAlmostEqual(r1[\"majoritaire\"], 6 / 11)')\np. … [178 caractères tronqués]`

  ```
....................................
----------------------------------------------------------------------
Ran 36 tests in 0.133s

OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0,'tools')\nfrom cerveau import batterie\nfrom cerveau.sequences import corpus\nseqs=corpus(0,40,12)\nprint(\"M5 batterie:\", json.dumps(batterie.m5(list(seqs)), ensure_ascii=False) … [127 caractères tronqués]`

  ```
M5 batterie: {"exact": 0.12454212454212454, "majoritaire": 0.08791208791208792, "surprise": 2.958466977800121, "surprise_majoritaire": 2.962032214789608, "gain": 0.036630036630036625, "gain_surprise": 0.003565236989487186, "n": 273, "hors_vocabulaire": 2, "cible": "cible", "ordre": 1}
M6 batterie: {"exact": 0.9431818181818182, "n": 88, "vrais_positifs": 17, "faux_positifs": 0, "faux_negatifs": 5, "vrais_negatifs": 66, "sensibilite": 0.7727272727272727, "specificite": 1.0, "exactitude_equilibree": 0.8863636363636364, "mcc": 0.8475316272298808, "sensibilite_ic95": [0.5655964393704065, 0.8987710920517964], "specificite_ic95": [0.9449955327483907, 1.0], "taux_base_tout_non": 0.75, "par_condition": {"go": {"n": 22, "corrects": 17, "acceptes": 17, "exact": 0.7727272727272727}, "traduction": {"n": 22, "corrects": 22, "acceptes": 0, "exact": 1.0}, "langue": {"n": 22, "corrects": 22, "acceptes": 0, "exact": 1.0}, "ni": {"n": 22, "corrects": 22, "acceptes": 0, "exact": 1.0}}, "par_langue": {"fr": {"n": 44, "corrects": 42, "tp": 9, "fn": 2, "exact": 0.9545454545454546, "sensibilite": 0.8181818181818182}, "en": {"n": 44, "corrects": 41, "tp": 8, "fn": 3, "exact": 0.9318181818181818, "sensibili
… [979 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Building the final measurement harness (M5 oracle, M6 old-design artifact and seeds).

- **bash** `{"command": "cat > /tmp/a1_old_m6.py <<'EOF'\n\"\"\"Reproduction de l'ANCIENNE mesure M6, pour montrer l'artefact.\"\"\"\nimport json, sys\nsys.path.insert(0, \"tools\")\nfrom jeux.lexique_multilingue import MULTI\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.ty … [2318 caractères tronqués]`

  ```
seed 0: {"ancien": {"exact": 0.7, "faux_positifs": 1, "faux_negatifs": 20, "n": 70, "cout_commutation": -0.1504524886877828, "switch_n": 17, "repeat_n": 52, "erreurs_cible_fr": 19, "n_cible_fr": 36, "erreurs_cible_en": 2, "n_cible_en": 34}, "b7_detection_exacte": 0.7272727272727273, "b7_detection_n": 16, "ambigu_surfaces": {"go D4": "ms", "tic-tac-toe A1": "ms"}}
seed 1: {"ancien": {"exact": 0.7, "faux_positifs": 1, "faux_negatifs": 20, "n": 70, "cout_commutation": -0.1504524886877828, "switch_n": 17, "repeat_n": 52, "erreurs_cible_fr": 19, "n_cible_fr": 36, "erreurs_cible_en": 2, "n_cible_en": 34}, "b7_detection_exacte": 0.7727272727272727, "b7_detection_n": 17, "ambigu_surfaces": {"go D4": "gl", "tic-tac-toe A1": "ms"}}
seed 2: {"ancien": {"exact": 0.6857142857142857, "faux_positifs": 2, "faux_negatifs": 20, "n": 70, "cout_commutation": -0.16968325791855202, "switch_n": 17, "repeat_n": 52, "erreurs_cible_fr": 19, "n_cible_fr": 36, "erreurs_cible_en": 3, "n_cible_en": 34}, "b7_detection_exacte": 0.7727272727272727, "b7_detection_n": 17, "ambigu_surfaces": {"go D4": "hr", "tic-tac-toe A1": "en"}}
seed 3: {"ancien": {"exact": 0.7, "faux_positifs": 1, "faux_negatifs": 20, "n": 70, "c
… [2507 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONHASHSEED=0 PYTHONPATH=tools python3 - <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools')\nfrom jeux.lexique_multilingue import MULTI\nfrom semantique.typed_corpus import items\nits=[i for i in items() if i.langue in (\"fr\",\"en\")]\np … [567 caractères tronqués]`

  ```
n 70 Counter({'fr': 55, 'en': 15})
fr 55 erreurs 39 [('A1', 'cellule', None), ('a1', 'cellule', None), ('(1,1)', 'cellule', None), ('1 1', 'cellule', None), ('ligne 1 colonne 1', 'cellule', None), ('case 1', 'cellule', None), ('haut gauche', 'cellule', None), ('en haut à gauche', 'cellule', 'vi'), ('top left', 'cellule', 'bs'), ('coin haut gauche', 'cellule', None), ('X joue en haut à gauche', 'cellule', 'vi'), ('X plays top left', 'cellule', 'bs'), ('milieu', 'cellule', None), ('centre', 'cellule', None), ('center', 'cellule', None), ('case 5', 'cellule', None), ('(2,2)', 'cellule', None), ('la croix au centre', 'cellule', None), ('O joue en bas à droite', 'cellule', 'vi'), ('le rond joue au coin bas droit', 'cellule', None), ('le pion de e2 vers e4', 'francais', 'nl'), ('Cf3', 'san', None), ('petit roque', 'francais', None), ('grand roque', 'francais', None), ('9x18', 'numerique', None), ('b6xd4', 'numerique', None), ('le pion b6 prend en d4', 'numerique', 'nl'), ('b6 prend d4', 'numerique', None), ('9x18x27', 'numerique', None), ('b6xd4xf2', 'numerique', None)]
en 15 erreurs 4 [('two of diamonds', 'carte', None), ('go D4', 'multilingue', 'ms'), ('english draughts b6 c5', 'multil
… [1671 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/a1_oracle.py <<'EOF'\nimport sys, math, collections, random\nsys.path.insert(0,'tools')\nfrom cerveau.sequences import partie\nfrom cerveau.predictif import valeur\nfrom semantique.universaux import code_rsn, rsn_depuis_code\nfrom jeux.regles import echecs as E, dames as D, g … [3469 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "/tmp/a1_oracle.py", line 78, in <module>
    r=oracle_steps(jeu,[K[jeu]*1000+i for i in range(5)],cible)
  File "/tmp/a1_oracle.py", line 47, in oracle_steps
    etapes=rejoue(jeu,g,n)
  File "/tmp/a1_oracle.py", line 20, in rejoue
    coups=pos.coups_legaux()
          ^^^^^^^^^^^^^^^^
AttributeError: 'tuple' object has no attribute 'coups_legaux'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"def applique\" -A 25 tools/jeux/regles/dames.py", "description": "Inspect dames applique return"}`

  ```
228:    def applique(self, coup: Coup) -> "Position":
229-        legal = self.coups_legaux()
230-        if coup not in legal:
231-            raise ErreurDames(f"coup illégal : {coup.numerique()}")
232-        return self._applique_direct(coup)
233-
234-    def _applique_direct(self, coup: Coup) -> "Position":
235-        cases = list(self.cases)
236-        piece = cases[coup.chemin[0]]
237-        if piece == VIDE or _couleur(piece) != self.trait:
238-            raise ErreurDames("pas de pièce au trait sur la case de départ")
239-        # retire les pièces sautées
240-        for a, b in zip(coup.chemin, coup.chemin[1:]):
241-            over = MILEU.get((a, b))
242-            if over is not None:
243-                cases[over] = VIDE
244-        # déplace
245-        cases[coup.chemin[0]] = VIDE
246-        arrivee = coup.chemin[-1]
247-        cases[arrivee] = piece
248-        # promotion
249-        if _est_pion(piece) and arrivee // 4 == _promotion_row(_couleur(piece)):
250-            cases[arrivee] = NOIR_DAME if _couleur(piece) == NOIR else BLANC_DAME
251-        # compteur de nulle : 80 demi-coups sans prise ni promotion
252-        promotion = (_est_pion(piece)
25
… [75 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"def joue\" -A 8 tools/jeux/regles/echecs.py; PYTHONPATH=tools python3 - <<'EOF'\nimport sys; sys.path.insert(0,'tools')\nfrom jeux.regles import echecs as E, dames as D\np=E.Position.depart(); c=p.coups_legaux()[0]\ntry:\n    q=p.joue(c); pr … [244 caractères tronqués]`

  ```
420:    def joue(self, coup: Coup) -> tuple:
421-        de, vers, promo, drapeau = coup
422-        p = self.plateau
423-        q = p[de]
424-        if not q or couleur(q) != self.trait:
425-            raise ErreurEchecs(f"coup illégal : pas de pièce au trait en {indice_vers_case(de)}")
426-        coul = couleur(q)
427-        t = typ(q)
428-        capture = p[vers]
echecs joue -> <class 'tuple'>
dames applique -> <class 'jeux.regles.dames.Position'>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 400,500p tools/jeux/regles/echecs.py", "description": "Inspect echecs joue implementation"}`

  ```
if (self.roques & 8 and p[3] == 0 and p[2] == 0 and p[1] == 0
                                and p[0] == piece(NOIR, TOUR)
                                and not self.est_attaque(4, BLANC)
                                and not self.est_attaque(3, BLANC)
                                and not self.est_attaque(2, BLANC)):
                            coups.append(Coup(4, 2, None, ROQUE_Q))
        return coups

    def coups_legaux(self) -> list[Coup]:
        coul = self.trait
        adv = 1 - coul
        legal = []
        for c in self.pseudo_coups():
            u = self.joue(c)
            if not self.est_attaque(self.rois[coul], adv):
                legal.append(c)
            self.annule(u)
        return legal

    # ---- jouer / annuler ----------------------------------------------
    def joue(self, coup: Coup) -> tuple:
        de, vers, promo, drapeau = coup
        p = self.plateau
        q = p[de]
        if not q or couleur(q) != self.trait:
            raise ErreurEchecs(f"coup illégal : pas de pièce au trait en {indice_vers_case(de)}")
        coul = couleur(q)
        t = typ(q)
        capture = p[vers]
        capture_sq = vers
        if drapeau == EP:
 
… [2347 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a1_oracle.py')\ns=p.read_text().replace('pos=pos.joue(c) if jeu==\"echecs\" else pos.applique(c)',\n                        'pos.joue(c) if jeu==\"echecs\" else None\\n            if jeu==\"dames … [146 caractères tronqués]`

  ```
echecs action {'n': 55, 'H_oracle': 0.0, 'mode_oracle': 1.0}
echecs source {'n': 55, 'H_oracle': 2.3577, 'mode_oracle': 0.1759}
echecs cible {'n': 55, 'H_oracle': 2.7639, 'mode_oracle': 0.1217}
dames action {'n': 55, 'H_oracle': 0.0, 'mode_oracle': 1.0}
dames source {'n': 55, 'H_oracle': 1.1954, 'mode_oracle': 0.4531}
dames cible {'n': 55, 'H_oracle': 1.1435, 'mode_oracle': 0.4671}
go action {'n': 55, 'H_oracle': 0.3251, 'mode_oracle': 0.9}
go cible {'n': 46, 'H_oracle': 4.3239, 'mode_oracle': 0.0133}
morpion action {'n': 31, 'H_oracle': 0.0, 'mode_oracle': 1.0}
morpion cible {'n': 31, 'H_oracle': 1.5501, 'mode_oracle': 0.2475}
  ```

### 🤖 Assistant

⏵ Writing the final harness that produces the JSON and markdown results.

- **bash** `{"command": "cat > /tmp/a1_m5_m6.py <<'PYEOF'\n#!/usr/bin/env python3\n\"\"\"Harnais de mesure M5/M6 — écrit /tmp/a1-m5-m6.json et .md.\"\"\"\nfrom __future__ import annotations\n\nimport collections\nimport json\nimport math\nimport os\nimport random\nimport subprocess\nimport sys\nimport time\n\nR … [27035 caractères tronqués]`

  ```
{"json": "/tmp/a1-m5-m6.json", "md": "/tmp/a1-m5-m6.md", "tests": {"commande": "PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools", "code": 1, "fin": "FAILED (errors=1)", "ok": false}, "secondes": 22.0}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONHASHSEED=0 PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -30", "description": "Run tests under hash seed 0"}`

  ```
..........................................................E
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
Ran 59 tests in 5.194s

FAILED (errors=1)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONHASHSEED=0 PYTHONPATH=tools python3 -m unittest cerveau.tests.test_predictif cerveau.tests.test_gating 2>&1 | tail -5", "description": "Run only M5/M6 tests under seed 0"}`

  ```
..................
----------------------------------------------------------------------
Ran 18 tests in 0.110s

OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a1_m5_m6.py')\ns=p.read_text()\ns=s.replace('''def tests():\n    env = dict(os.environ, PYTHONPATH=\"tools\")\n    out = subprocess.run([sys.executable, \"-m\", \"unittest\", \"discover\",\n      … [2107 caractères tronqués]`

  ```
{"json": "/tmp/a1-m5-m6.json", "md": "/tmp/a1-m5-m6.md", "tests": {"commande": "PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools", "complet": {"code": 1, "fin": "FAILED (errors=1)", "ok": false}, "m5_m6": {"code": 0, "fin": "OK", "ok": true}, "commande_m5_m6": "PYTHONPATH=tools python3 -m unittest cerveau.tests.test_predictif cerveau.tests.test_gating"}, "secondes": 22.0}
--- MD ---
# M5 (prédictif) et M6 (gating) — résultat mesuré

Corpus M5 : `cerveau.sequences.corpus(0, 200, 12)`, split par partie 80/19, graine 3. Corpus M6 : surfaces B7 fr/en. Temps : 22.0 s.

## M5 — la cible `action` était constante ; les cibles de case ne le sont pas

| cible | ordre | n | exact | majoritaire | gain exact | surprisal | surprisal maj. | gain surprisal |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| action | 0 | 1538 | 97.5 % | 97.5 % | +0.0 pt | 0.086 | 0.086 | +0.000 |
| action | 1 | 1538 | 97.5 % | 97.5 % | +0.0 pt | 0.087 | 0.086 | -0.000 |
| action | 2 | 1538 | 97.5 % | 97.5 % | +0.0 pt | 0.087 | 0.086 | -0.001 |
| source | 0 | 770 | 6.5 % | 6.5 % | +0.0 pt | 3.539 | 3.539 | +0.000 |
| source | 1 | 770 | 12.6 % | 6.5 % | +6.1 pt | 3.112 | 3.539 | +0.428 |
| 
… [2440 caractères tronqués]
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

- **bash** `{"command": "sed -n 40,200p /tmp/a1-m5-m6.md", "description": "Read the rest of the markdown report"}`

  ```
### Plancher oracle (le plateau serait-il utile ?)

| cible | jeu | n | H oracle (nat) | mode oracle |
|---|---|---:|---:|---:|
| action | morpion | 317 | 0.000 | 100.0 % |
| action | echecs | 374 | 0.000 | 100.0 % |
| action | go | 451 | 0.325 | 90.0 % |
| action | dames | 396 | 0.000 | 100.0 % |
| source | morpion | 0 | 0.000 | 0.0 % |
| source | echecs | 374 | 2.375 | 17.1 % |
| source | go | 0 | 0.000 | 0.0 % |
| source | dames | 396 | 1.118 | 48.0 % |
| cible | morpion | 317 | 1.521 | 26.1 % |
| cible | echecs | 374 | 2.793 | 11.5 % |
| cible | go | 379 | 4.323 | 1.3 % |
| cible | dames | 396 | 1.083 | 48.2 % |

L'oracle est la loi de la cible **conditionnée par la position réelle** (tirage uniforme parmi les coups légaux). C'est le plancher de surprisal d'un modèle qui verrait le plateau. Le modèle M5 ne le voit pas : l'écart entre sa surprisal et H oracle est le prix de l'observation manquante (0,7 nat aux échecs, ~1,9 nat aux dames). Le mode oracle n'est pas un plafond d'exactitude (il peut être sous la majorité quand la cible est quasi uniforme) : c'est la surprisal qui fait foi.

### Contrôles négatifs (permutation des cibles, 20 tirages)

| contrôle | gain observé | gain
… [7901 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a1_m5_m6.py')\ns=p.read_text()\n# 1. intro 80/20\ns=s.replace('f\"{int(100 * FRACTION)}/{int(100 * (1 - FRACTION))}, graine {GRAINE_SPLIT}. \"',\n            'f\"{int(100 * FRACTION)}/{100 - int( … [6669 caractères tronqués]`

  ```
{"json": "/tmp/a1-m5-m6.json", "md": "/tmp/a1-m5-m6.md", "tests": {"commande": "PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools", "complet": {"code": 1, "fin": "FAILED (errors=1)", "ok": false}, "m5_m6": {"code": 0, "fin": "OK", "ok": true}, "commande_m5_m6": "PYTHONPATH=tools python3 -m unittest cerveau.tests.test_predictif cerveau.tests.test_gating"}, "secondes": 21.2}
  ```

- **bash** `{"command": "sed -n 1,6p /tmp/a1-m5-m6.md; echo ...; sed -n 40,62p /tmp/a1-m5-m6.md; echo ...; grep -n \"Plafond\\|plafond\\|72,9\\|Effet sur la batterie\\|Ce qui pourrait\" /tmp/a1-m5-m6.md; echo ...; sed -n 100,140p /tmp/a1-m5-m6.md", "description": "Verify corrected markdown sections"}`

  ```
# M5 (prédictif) et M6 (gating) — résultat mesuré

Corpus M5 : `cerveau.sequences.corpus(0, 200, 12)`, split par partie 80/20, graine 3. Corpus M6 : surfaces B7 fr/en. Temps : 21.2 s.

## M5 — la cible `action` était constante ; les cibles de case ne le sont pas

...
### Plancher oracle (le plateau serait-il utile ?)

| cible | jeu | n oracle | H oracle | H modèle (ordre 1) | écart | mode oracle |
|---|---|---:|---:|---:|---:|---:|
| action | morpion | 317 | 0.000 | 0.000 | +0.000 | 100.0 % |
| action | echecs | 374 | 0.000 | 0.000 | +0.000 | 100.0 % |
| action | go | 451 | 0.325 | 0.296 | -0.029 | 90.0 % |
| action | dames | 396 | 0.000 | 0.000 | +0.000 | 100.0 % |
| source | echecs | 374 | 2.375 | 3.641 | +1.266 | 17.1 % |
| source | dames | 396 | 1.118 | 2.612 | +1.494 | 48.0 % |
| cible | morpion | 317 | 1.521 | 2.131 | +0.610 | 26.1 % |
| cible | echecs | 374 | 2.793 | 3.813 | +1.020 | 11.5 % |
| cible | go | 379 | 4.323 | 4.912 | +0.589 | 1.3 % |
| cible | dames | 396 | 1.083 | 2.646 | +1.563 | 48.2 % |

L'oracle est la loi de la cible **conditionnée par la position réelle** (tirage uniforme parmi les coups légaux). C'est le plancher de surprisal d'un modèle qui verrait le pl
… [7479 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"0,7 nat\\|l'ordre 2 n'aide\\|sur des surfaces non identifiables\\|16/22 avec\\|ou des variantes anglaises\\|## Commandes\" /tmp/a1_m5_m6.py", "description": "Locate stale strings in harness"}`

  ```
241:                "notations ou des variantes anglaises mal étiquetées) et B7 ; "
364:      "surprisal et H oracle est le prix de l'observation manquante (0,7 nat aux échecs, "
422:      "canal langue sur des surfaces non identifiables.\n")
457:      "lexical (16/22 avec `MULTI`, 17/22 avec le canal déterministe combiné), "
470:      f"(`A1`, `9x18`, `Cf3`) ou des variantes anglaises mal étiquetées `fr` : "
493:    a("## Commandes\n")
  ```

- **bash** `{"command": "sed -n 358,370p /tmp/a1_m5_m6.py; echo ---; sed -n 418,424p /tmp/a1_m5_m6.py; echo ---; sed -n 452,472p /tmp/a1_m5_m6.py; echo ---; grep -n \"L'ordre 2\" /tmp/a1_m5_m6.py", "description": "View exact harness lines to patch"}`

  ```
continue
            a(f"| {cible} | {jeu} | {x['n']} | {x['H_oracle']:.3f} | {h:.3f} | "
              f"{h - x['H_oracle']:+.3f} | {pct(x['mode_oracle'])} |")
    a("\nL'oracle est la loi de la cible **conditionnée par la position réelle** "
      "(tirage uniforme parmi les coups légaux). C'est le plancher de surprisal d'un "
      "modèle qui verrait le plateau. Le modèle M5 ne le voit pas : l'écart entre sa "
      "surprisal et H oracle est le prix de l'observation manquante (0,7 nat aux échecs, "
      "~1,9 nat aux dames). Le mode oracle n'est pas un plafond d'exactitude (il peut "
      "être sous la majorité quand la cible est quasi uniforme) : c'est la surprisal "
      "qui fait foi.\n")
    a("### Contrôles négatifs (permutation des cibles, 20 tirages)\n")
    a("| contrôle | gain observé | gain nul moyen | écart-type | p(gain) | gain surprisal observé | p(surprisal) |")
    a("|---|---:|---:|---:|---:|---:|---:|")
---
      "Les trois politiques simples sont **toutes au taux de base** : la langue seule "
      "accepte les leurres de langue (25 % de FP), le sens seul accepte les traductions "
      "(25 % de FP). Seule la conjonction fait mieux. Son exactitude est de 
… [1908 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a1_m5_m6.py')\ns=p.read_text()\ns=s.replace('\"surprisal et H oracle est le prix de l\\'observation manquante (0,7 nat aux échecs, \"\\n      \"~1,9 nat aux dames). Le mode oracle',\n             … [1522 caractères tronqués]`

  ```
ok
364:      "surprisal et H oracle est le prix de l'observation manquante (de 1,0 à "
397:      "de la structure (dames, un peu morpion) ; partout ailleurs il ne fait que du "
424:      "lexicale (`english draughts`).\n")
450:      "(le seul évitable est `english draughts`, ambigu en de/en).\n")
459:      "lexical (16 à 19/22 avec `MULTI` selon `PYTHONHASHSEED`, 17/22 avec le "
473:      f"(`A1`, `9x18`, `Cf3`) et quelques variantes anglaises mal étiquetées `fr` : "
497:    a("## Commandes\n")
  ```

- **bash** `{"command": "sed -n 492,500p /tmp/a1_m5_m6.py; cd /home/stephane/GitHub/Qtrinet && PYTHONHASHSEED=0 PYTHONPATH=tools timeout 900 python3 /tmp/a1_m5_m6.py && sed -n 50,58p /tmp/a1-m5-m6.md && grep -n \"les 5 FN\\|16 à 19\\|quelques variantes\\|dames, un peu\\|## Commandes\" /tmp/a1-m5-m6.md", "descri … [41 caractères tronqués]`

  ```
"ne tiendrait que pour une porte sans état.")
    a("- Le split M5 est par partie et les contrôles portent sur 20 permutations ; un "
      "corpus plus grand pourrait révéler de petits gains, mais l'écart à H oracle les "
      "borne.")
    a("")
    a("## Commandes\n")
    a("```bash")
    a("PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools")
    a("PYTHONPATH=tools python3 /tmp/a1_m5_m6.py")
{"json": "/tmp/a1-m5-m6.json", "md": "/tmp/a1-m5-m6.md", "tests": {"commande": "PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools", "complet": {"code": 1, "fin": "FAILED (errors=1)", "ok": false}, "m5_m6": {"code": 0, "fin": "OK", "ok": true}, "commande_m5_m6": "PYTHONPATH=tools python3 -m unittest cerveau.tests.test_predictif cerveau.tests.test_gating"}, "secondes": 21.1}
| cible | morpion | 317 | 1.521 | 2.131 | +0.610 | 26.1 % |
| cible | echecs | 374 | 2.793 | 3.813 | +1.020 | 11.5 % |
| cible | go | 379 | 4.323 | 4.912 | +0.589 | 1.3 % |
| cible | dames | 396 | 1.083 | 2.646 | +1.563 | 48.2 % |

L'oracle est la loi de la cible **conditionnée par la position réelle** (tirage uniforme parmi les coups légaux). C'est le plancher de s
… [2704 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, math, os\nj=json.load(open('/tmp/a1-m5-m6.json'))\nprint(\"taille\", os.path.getsize('/tmp/a1-m5-m6.json'), \"octets\")\nprint(\"cles\", list(j))\nprint(\"m5 split\", j['m5']['protocole']['n_sequences_train'], j['m5'][' … [1463 caractères tronqués]`

  ```
taille 28491 octets
cles ['meta', 'm5', 'm6', 'tests']
m5 split 640 160
m5 action o1 {'n': 1538, 'exact': 0.974642, 'majoritaire': 0.974642, 'gain': 0.0, 'surprise': 0.086836, 'gain_surprise': -0.000355}
m5 cible o2 {'n': 1465, 'exact': 0.113993, 'majoritaire': 0.05802, 'gain': 0.055973, 'surprise': 3.410394, 'gain_surprise': -0.035494}
m5 oracle dames source {'n': 396, 'H_oracle': 1.117683, 'mode_oracle': 0.480001}
m5 controles {'action_ordre1': (0.0, 1.0, -0.000355), 'source_ordre1': (0.061039, 0.0, 0.427779), 'source_ordre2': (0.079221, 0.0, 0.44012), 'cible_ordre1': (0.02116, 0.0, -0.043098), 'cible_ordre2': (0.055973, 0.0, -0.035494)}
m6 exact 0.943182 n 88
m6 cout 0.0 persev 0.380952
m6 ident {'plafond_exact': 0.954545, 'plafond_sensibilite': 0.818182, 'plafond_exactitude_equilibree': 0.909091}
m6 ancienne {'n': 70, 'fr': 55, 'en': 15, 'exact_min': 0.685714, 'exact_max': 0.7, 'cout_min': -0.169683, 'cout_max': -0.150452, 'erreurs_fr': 39}
tests {'code': 0, 'fin': 'OK', 'ok': True}
JSON OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a1_m5_m6.py')\ns=p.read_text()\ns=s.replace('''      \"Le 72,9 % publié (51/70) est une autre graine de hachage : la valeur n'est pas \"\n      \"reproductible. \"''',\n            '''      \"Le  … [1137 caractères tronqués]`

  ```
{"json": "/tmp/a1-m5-m6.json", "md": "/tmp/a1-m5-m6.md", "tests": {"commande": "PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools", "complet": {"code": 1, "fin": "FAILED (errors=1)", "ok": false}, "m5_m6": {"code": 0, "fin": "OK", "ok": true}, "commande_m5_m6": "PYTHONPATH=tools python3 -m unittest cerveau.tests.test_predictif cerveau.tests.test_gating"}, "secondes": 20.7}
126:Sur les 70 items fr/en de `typed_corpus` (55 fr, 15 en), l'ancienne porte donne 68.6 % à 70.0 % (moyenne 69.6 %) selon `PYTHONHASHSEED`, et un coût de commutation de -0.170 à -0.150. Le 72,9 % publié (51/70) n'est pas reproduit sur ces 10 graines (68,6–70,0 %) : il correspond à un autre tirage de hachage — la valeur n'est pas stable. Or 39/55 items « fr » sont des notations (`A1`, `9x18`, `Cf3`) et quelques variantes anglaises mal étiquetées `fr` : la langue y est indéfinie. L'« exactitude » mesure la couverture du détecteur sur des surfaces non linguistiques ; le « coût de commutation » compare des blocs dont la composition en langue n'est pas contrebalancée (19/36 erreurs sur cible fr contre 2/34 sur cible en, graine 0). Ce n'est ni de la langue ni du contrôle.
130:`Predictif()` 
… [641 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Final validation: tests, repo scope, and deliverables.

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -m unittest cerveau.tests.test_predictif cerveau.tests.test_gating 2>&1 | tail -3 && python3 -m py_compile tools/cerveau/predictif.py tools/cerveau/gating.py && echo \"compile OK\" && ls -l /tmp/a1-m5-m6.json /tmp/a1-m5-m6.md" … [48 caractères tronqués]`

  ```
Ran 18 tests in 0.107s

OK
compile OK
-rw-r--r--. 1 stephane stephane 28491 27 oct 10:21 /tmp/a1-m5-m6.json
-rw-r--r--. 1 stephane stephane 14491 27 oct 10:21 /tmp/a1-m5-m6.md
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git status --short -- tools/cerveau tools/semantique tools/jeux batterie.py 2>/dev/null | head -30; echo \"--- diff stat (cerveau) ---\"; git diff --stat -- tools/cerveau 2>/dev/null", "description": "Check scope of modified files"}`

  ```
M tools/cerveau/episodique.py
 M tools/cerveau/gating.py
 M tools/cerveau/memoire_travail.py
 M tools/cerveau/neuromodulation.py
 M tools/cerveau/predictif.py
 M tools/cerveau/sommeil.py
 M tools/cerveau/voies.py
?? tools/cerveau/lesion.py
?? tools/cerveau/tests/test_episodique.py
?? tools/cerveau/tests/test_gating.py
?? tools/cerveau/tests/test_lesion.py
?? tools/cerveau/tests/test_memoire_travail.py
?? tools/cerveau/tests/test_neuromodulation.py
?? tools/cerveau/tests/test_predictif.py
?? tools/cerveau/tests/test_sommeil.py
?? tools/cerveau/tests/test_voies.py
--- diff stat (cerveau) ---
 tools/cerveau/episodique.py      |  31 ++-
 tools/cerveau/gating.py          | 450 ++++++++++++++++++++++++++++---
 tools/cerveau/memoire_travail.py |  27 ++
 tools/cerveau/neuromodulation.py | 555 +++++++++++++++++++++++++++++++++++++--
 tools/cerveau/predictif.py       | 430 ++++++++++++++++++++++++++----
 tools/cerveau/sommeil.py         | 390 +++++++++++++++++++++++++--
 tools/cerveau/voies.py           | 421 +++++++++++++++++++++++++----
 7 files changed, 2126 insertions(+), 178 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/cerveau/gating.py')\ns=p.read_text().replace(\"le coût de commutation apparié est 0,000, alors qu'un contrôle positif de\\npersévération donne 1,000.\",\n                        \"le coût de com … [352 caractères tronqués]`

  ```
21:le taux de base est la **conjonction** (sens ET langue) : exactitude 94,3 %,
22:exactitude équilibrée 88,6 %, 0 faux positif, 5 faux négatifs. Les 5 FN sont
28:persévération donne 1,000. Conclusion : **la détection de langue n'est pas du
Ran 18 tests in 0.106s

OK
  ```

- **bash** `{"command": "sed -n 24,30p /home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py", "description": "View gating docstring lines"}`

  ```
codes ont la même surface en fr et en en : « go D4 », « tic-tac-toe A1 ») ou
d'ambiguïté lexicale (« english draughts »). Aucun effet d'inhibition ni de
commutation n'apparaît : la porte est une règle déterministe sans mémoire ; le
coût de commutation apparié est 0,000, alors qu'un contrôle positif de
persévération donne 1,000. Conclusion : **la détection de langue n'est pas du
contrôle exécutif**, c'est un classifieur lexical bruité ; le contrôle est la
règle de conjonction, et le corpus B7 ne permet pas de mesurer l'inhibition.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/cerveau/gating.py')\ns=p.read_text().replace(\"persévération donne 1,000.\", \"persévération donne 0,381.\")\np.write_text(s)\nEOF\ngrep -n \"persévération donne\" tools/cerveau/gating.py", "des … [51 caractères tronqués]`

  ```
28:persévération donne 0,381. Conclusion : **la détection de langue n'est pas du
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git diff --check -- tools/cerveau/predictif.py tools/cerveau/gating.py; echo \"diff-check code $?\"; wc -l tools/cerveau/predictif.py tools/cerveau/gating.py tools/cerveau/tests/test_predictif.py tools/cerveau/tests/test_gating.py; PYTHONPATH=tools py … [387 caractères tronqués]`

  ```
diff-check code 0
  400 tools/cerveau/predictif.py
  431 tools/cerveau/gating.py
  124 tools/cerveau/tests/test_predictif.py
   81 tools/cerveau/tests/test_gating.py
 1036 total
defaut M5: cible 1 10.0
M6 langue go D4: af | tic-tac-toe: de
  ```

### 🤖 Assistant

⏵ Sending the final self-contained result to the parent agent.

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "M5/M6 terminés, mesurés, testés. Livrables : /tmp/a1-m5-m6.json (28,5 Ko) et /tmp/a1-m5-m6.md (14,5 Ko). Code : tools/cerveau/predictif.py, tools/cerveau/gating.py, tests/test_predictif.py, tests/test_gating.py. Aucun commit, aucune mo … [3641 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -m unittest cerveau.tests.test_predictif cerveau.tests.test_gating 2>&1 | tail -3; ls -l /tmp/a1-m5-m6.json /tmp/a1-m5-m6.md; git status --short -- tools/cerveau/predictif.py tools/cerveau/gating.py tools/cerveau/tests/test_pr … [110 caractères tronqués]`

  ```
Ran 18 tests in 0.105s

OK
-rw-r--r--. 1 stephane stephane 28491 27 oct 10:21 /tmp/a1-m5-m6.json
-rw-r--r--. 1 stephane stephane 14491 27 oct 10:21 /tmp/a1-m5-m6.md
 M tools/cerveau/gating.py
 M tools/cerveau/predictif.py
?? tools/cerveau/tests/test_gating.py
?? tools/cerveau/tests/test_predictif.py
  ```

### 🤖 Assistant

## Résultat — M5/M6 mesurés, testés, documentés

**Fichiers modifiés** (aucun commit, aucun autre fichier touché) :
- `tools/cerveau/predictif.py` — cibles `action`/`source`/`cible`, ordres 0/1/2, repli Dirichlet, baselines majoritaire et « tour », oracle documenté, contrôle négatif par permutation, diagnostic de dispersion.
- `tools/cerveau/gating.py` — vraie tâche de conflit B7 fr/en (88 essais : go/traduction/langue/ni), politiques comparées, exactitude équilibrée/Wilson/MCC, commutation appariée, contrôle positif de persévération, canal langue déterministe.
- `tools/cerveau/tests/test_predictif.py`, `tools/cerveau/tests/test_gating.py` — 18 tests, tous OK.

**Livrables** : `/tmp/a1-m5-m6.json` (28,5 Ko) et `/tmp/a1-m5-m6.md` (14,5 Ko).

### M5 — le 98,9 % était la classe constante
`action` est un indicateur de **format** : échecs=toujours `deplacer`, dames=toujours `prendre`, morpion=toujours `jouer_case` ; seul go varie (92 % poser). Sur `corpus(0,200,12)` :
- `action` : 97,46 % = majoritaire, gain 0 ; ordre 2 sans effet.
- `source` : 12,60 % vs 6,49 % (ordre 1, +6,1 pt, +0,43 nat), mais le gain est **mécanique** : dames +8,8 pt (au-dessus de la baseline tour), échecs +3,2 pt **sous** la baseline tour.
- `cible` : +2,1 pt (ordre 1) mais surprisal **négative** (−0,04 nat) ; ordre 2 +5,6 pt, surprisal −0,04. Seules les dames gagnent réellement (+6 à +13 pt, +0,26 à +0,36 nat).
- Oracle avec plateau : H 1,1–2,8 nats selon jeu/cible, contre 2,6–4,9 pour le modèle → **le code observé ne contient pas le plateau** ; le tirage uniforme parmi les coups légaux borne le prédictible.
- Contrôles permutation : l'exact dépasse le null, mais le gain de surprisal reste négatif pour `cible` → gain de mode, pas d'information.

### M6 — la détection de langue n'est pas du contrôle exécutif
- Conjonction sens+langue : **94,32 %** exact, **88,64 %** équilibrée, VP 17, **FP 0, FN 5**, sensibilité 77,27 %, spécificité 100 %, MCC 0,848 (base « toujours non » 75 %).
- Langue-seule, sens-seul et tout-non : **toutes à 75 %** — seule la conjonction gagne.
- **Coût de commutation apparié = 0,000** (21 blocs switch / 21 repeat, mêmes stimuli) ; contrôle positif de persévération = 0,381 → l'instrument est sensible, la porte n'a pas de mémoire.
- 2 codes ont la même surface fr/en (`go D4`, `tic-tac-toe A1`) : plafond exact 95,45 %, sensibilité 81,82 %. La porte est à **1 essai du plafond** ; les 5 FN sont perceptifs, pas inhibiteurs.
- L'ancien 72,9 % : 70 items (55 fr/15 en), exact 68,6–70,0 % selon `PYTHONHASHSEED`, coût −0,150 à −0,170 ; 39/55 items « fr » sont des notations/variantes mal étiquetées, et l'asymétrie 19/36 erreurs sur cible fr vs 2/34 sur cible en prouve que l'ancien « coût de commutation » était un artefact de composition.

### À répercuter
`batterie.m5` publie désormais ~12,5 % (au lieu de 98,9 %) et M9 `M5_sans_transitions` ~0,91 ; `batterie.m6` publie 94,3 % (autre tâche). Si l'ancienne sémantique M5 est voulue : `Predictif("action")`.
La découverte complète des tests échoue sur `test_voies.py` (torch absent, fichier d'un autre agent) ; les 18 tests M5/M6 passent.

