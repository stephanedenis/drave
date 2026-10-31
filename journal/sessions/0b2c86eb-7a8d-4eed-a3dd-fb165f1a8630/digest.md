# Session DSH — relecture

- identifiant : `0b2c86eb-7a8d-4eed-a3dd-fb165f1a8630`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 10:29:11
- agent : standard


## Tour 1

### 👤 Utilisateur

Dépôt /home/stephane/GitHub/Qtrinet, sprint autonome 24 h. Sous-agent A5 : améliorer la GÉNÉRALISATION de M2 aux surfaces inédites, sans toucher aux autres modules.

État mesuré (A3) :
- `tools/cerveau/voies.py` : encodeur `route` gelé, têtes ventrales (action) / dorsales (de, vers, point, chemin_0), pools mean/last/mean+last, contexte optionnel, lésions.
- Sur 146 items `de` : `de` moyen 93,6 % sur 3 graines, mais **126/126 vus** et **10,7/20 inédits (53,3 %)** ; `vers` 94,3 %, inédit 11,7/20 ; `point` 95,7 % < majorité 97,1 % ; `chemin_0` 84,3 % < 97,1 %.
- Le recouvrement de surfaces normalisées est de 86,3 % ; le gain du dernier état vs mean à 1000 pas est ~+2,7/+3,4 pts.
- Tests : `PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest discover -s tools/cerveau/tests -t tools`.

Objectif : améliorer le **split inédit**, pas le score global. Pistes :
1. **Augmentation synthétique** : générer plus de formes (templates, coordonnées, pièces, langues), sans jamais utiliser les surfaces réelles de test à l'entraînement.
2. **Contexte** : encoder le contexte RSN (position/trait) avec un encodeur séparé ou une paire surface+contexte ; mesurer l'ablation.
3. **Split par template/paire** : évaluer sur les 20 inédits et sur un split par code ; 3 graines.
4. **Pooling** : mean, last, mean+last ; comparer à pas égal (1000).
5. **Normalisation/translitération** : tester une normalisation plus agressive des coordonnées.
6. Si aucun gain, produire un négatif net avec courbes vu/inédit.

Contraintes :
- Modifie uniquement `tools/cerveau/voies.py` et `tools/cerveau/tests/test_voies.py` ; ne touche pas à `batterie.py`, docs, reports, journal, git.
- Pas de `git add/commit/checkout`.
- GPU `CUDA_VISIBLE_DEVICES=0`, python `/home/stephane/gpu-env/bin/python`.
- Écris `/tmp/a5-m2-generalisation.json` et `.md` (chiffres vus/inédits, 3 graines, commandes, verdict).
- Sois autonome, mesure, autocritique-toi. Réponds avec un résumé concis et les chemins.
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

⏵ Reading the current M2 encoder and its tests to ground the baseline

- **bash** `{"command": "ls -la tools/cerveau/ && wc -l tools/cerveau/voies.py tools/cerveau/tests/test_voies.py", "description": "List cerveau dir and count lines"}`

  ```
total 168
drwxr-xr-x. 1 stephane stephane   340 27 oct 10:04 .
drwxr-xr-x. 1 stephane stephane 12792 27 oct 09:34 ..
-rw-r--r--. 1 stephane stephane  8161 27 oct 09:18 batterie.py
-rw-r--r--. 1 stephane stephane  1674 27 oct 08:41 bus.py
-rw-r--r--. 1 stephane stephane  3346 27 oct 10:01 episodique.py
-rw-r--r--. 1 stephane stephane 20489 27 oct 10:21 gating.py
-rw-r--r--. 1 stephane stephane  1784 27 oct 08:41 hub.py
-rw-r--r--. 1 stephane stephane     0 27 oct 08:41 __init__.py
-rw-------. 1 stephane stephane 22516 27 oct 10:08 lesion.py
-rw-r--r--. 1 stephane stephane  3166 27 oct 10:01 memoire_travail.py
-rw-r--r--. 1 stephane stephane 26300 27 oct 10:00 neuromodulation.py
-rw-r--r--. 1 stephane stephane  1598 27 oct 09:49 pipeline.py
-rw-r--r--. 1 stephane stephane 17656 27 oct 10:04 predictif.py
drwxr-xr-x. 1 stephane stephane   672 27 oct 10:22 __pycache__
-rw-r--r--. 1 stephane stephane  3455 27 oct 08:41 sequences.py
-rw-r--r--. 1 stephane stephane 17087 27 oct 10:15 sommeil.py
drwxr-xr-x. 1 stephane stephane   402 27 oct 10:11 tests
-rw-r--r--. 1 stephane stephane 18486 27 oct 09:58 voies.py
  426 tools/cerveau/voies.py
  130 tools/cerveau/tests/test_voies.py
  556 total
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git status --short | head -50 && git log --oneline -5", "description": "Check git status and recent log"}`

  ```
530b7043 B12 — STRESS SOUS-AGENTS : M1 SEUL SOLIDE ; M2 VU SEULEMENT ; M3–M8 NÉGATIFS ; M9 PROXY
515e6e62 B12 — CORRECTION MAJEURE : M1 SEUL SOLIDE ; M2 VU SEULEMENT ; M3–M8 STRUCTURELS/NÉGATIFS
d28ad551 B12 — PIPELINE M1→M4→M8 : 528/528, COMPLÉTION 96,3 %, 7 PROTOTYPES (DOCS)
b563a155 B12 — PIPELINE M1→M4→M8 : 528/528, COMPLÉTION 96,3 %, PROTOYPES 7
831ecdb1 JOURNAL — RÉGÉNÉRATION APRÈS LE COMMIT DE COHÉRENCE (9 COMMITS DU 27/10, PASSE 2 VISIBLE)
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py"}`

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

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls tools/semantique/ && wc -l tools/semantique/*.py", "description": "List semantique modules and line counts"}`

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
   73 tools/semantique/corpus.py
   94 tools/semantique/diagnostic.py
  282 tools/semantique/entrainer_nvlink.py
  257 tools/semantique/entrainer.py
  305 tools/semantique/entrainer_type.py
   76 tools/semantique/hybride.py
    0 tools/semantique/__init__.py
  154 tools/semantique/modele.py
   58 tools/semantique/normalisation.py
   56 tools/semantique/restitution.py
  104 tools/semantique/synth_corpus.py
   91 tools/semantique/typed_corpus.py
  158 tools/semantique/universaux.py
 1708 total
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/semantique/synth_corpus.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/semantique/typed_corpus.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/semantique/normalisation.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/semantique/synth_corpus.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """synth_corpus.py — des surfaces synthétiques multilingues, labels RSN exacts.
3: 
4: Le codec classique est le professeur : on génère des surfaces à partir des
5: règles (coups légaux, cartes, points) et des libellés multilingues, puis on
6: entraîne le natif à lire ces surfaces. Les surfaces **réelles** B5/B7 ne sont
7: jamais utilisées à l'entraînement : elles servent de test de transfert.
8: """
9: from __future__ import annotations
10: 
11: from dataclasses import dataclass
12: 
13: from jeux.lexique_multilingue import MULTI
14: from jeux.regles import cartes as C
15: from jeux.regles import dames as D
16: from jeux.regles import echecs as E
17: from jeux.regles import go as G
18: from jeux.regles import morpion as M
19: from jeux.rsn import RSN
20: from semantique.typed_corpus import ItemType
21: from semantique.universaux import code_rsn, resume_contexte
22: 
23: PIECES = ("P", "N", "B", "R", "Q", "K")
24: LETTRES_DAMES = "abcdefgh"
25: 
26: 
27: def _forme(concept: str, langue: str) -> str | None:
28:     f = MULTI.formes(concept, langue)
29:
… [4037 caractères tronqués]
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


  ```
<path>/home/stephane/GitHub/Qtrinet/tools/semantique/normalisation.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """normalisation.py — la surface vers des concepts, avant le parseur natif.
3: 
4: Le lexique multilingue connaît les noms de jeux, les pièces, les rangs et les
5: enseignes dans 66 langues. On remplace ces formes par un **concept canonique**
6: (`[jeu.morpion]`, `[echecs.piece.N]`, `[cartes.rang.13]`) ; les coordonnées et les
7: nombres restent. Deux surfaces qui disent la même chose dans deux langues
8: deviennent alors **presque identiques** — c'est ce qui doit rendre le natif
9: cohérent entre langues.
10: """
11: from __future__ import annotations
12: 
13: from jeux.lexique import normalise_forme
14: from jeux.lexique_multilingue import MULTI
15: 
16: DOMAINES = ("jeu.nom", "echecs.piece", "cartes.rang", "cartes.couleur",
17:             "go.passe", "commun.couleur")
18: 
19: 
20: def normaliser(texte: str) -> str:
21:     t = normalise_forme(texte)
22:     if not t:
23:         return t
24:     tokens = t.split()
25:     trouves = []
26:     for domaine in DOMAINES:
27:         trouves.extend(MULTI.cherche(domaine, texte))
28:     jeux = {m.con
… [1301 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/batterie.py"}`
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

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls /tmp/a3* /tmp/natif* 2>/dev/null; ls /tmp/*.json 2>/dev/null | head -40", "description": "Check tmp artifacts and base model"}`

  ```
/tmp/a3_baseline_items.py
/tmp/a3_baseline_split.py
/tmp/a3_long.py
/tmp/a3_m2_driver.py
/tmp/a3-m2.json
/tmp/a3-m2.md
/tmp/a3-m2-partial.json
/tmp/a3_probe2.py
/tmp/a3_probe.py
/tmp/a3_quick2.py
/tmp/a3_quick.py
/tmp/a3_timing.py
/tmp/natif-224-6-align-s1.log
/tmp/natif-224-6-align-s2.log
/tmp/natif-224-6-align-s3.log
/tmp/natif-224-6-controle-s1.log
/tmp/natif-224-6-controle-s2.log
/tmp/natif-224-6-controle-s3.log
/tmp/natif-232-6-align-s1.log
/tmp/natif-232-6-align-s2.log
/tmp/natif-232-6-align-s3.log
/tmp/natif-232-6-controle-s1.log
/tmp/natif-232-6-controle-s2.log
/tmp/natif-232-6-controle-s3.log
/tmp/natif-240-6-align-s1.log
/tmp/natif-240-6-align-s2.log
/tmp/natif-240-6-align-s3.log
/tmp/natif-240-6-controle-s1.log
/tmp/natif-240-6-controle-s2.log
/tmp/natif-240-6-controle-s3.log
/tmp/natif-256-6-align-s1.log
/tmp/natif-256-6-align-s2.log
/tmp/natif-256-6-align-s3.log
/tmp/natif-256-6-controle-s1.log
/tmp/natif-256-6-controle-s2.log
/tmp/natif-256-6-controle-s3.log
/tmp/natif-300-align-s1.log
/tmp/natif-300-align-s2.log
/tmp/natif-300-align-s3.log
/tmp/natif-300-controle-s1.log
/tmp/natif-300-controle-s2.log
/tmp/natif-300-controle-s3.log
/tmp/natif-320-7-align-s1.log
/tmp/n
… [11530 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rl \"voies\" reports/ 2>/dev/null | head -20; echo ---; grep -rln \"inédit\" reports/ 2>/dev/null | head -20", "description": "Find reports mentioning voies and inédits"}`

  ```
reports/rapport-minimal.md
reports/rapport-eparsite.md
reports/rapport-precision.md
reports/rapport-cpu-aer.md
reports/bilan-multi-materiel.md
reports/rapport-session-2026-09-30.md
reports/rapport-tete-restreinte.md
reports/rapport-optimisations-auto.md
reports/archive/rapport-campagne-benefices.md
reports/campagne-benefices/025-22-bis-ce-que-le-nouveau-materiel-change-dapres.md
reports/rapport-modele-drave.md
reports/traduction-onu-7b.json
reports/traduction-onu6-7b.json
reports/rapport-cerveau-modules.md
reports/README.md
reports/rapport-cerveau-corrections.md
reports/cerveau-mesures-corrigees.json
---
reports/archive/rapport-campagne-benefices.md
reports/campagne-benefices/026-23-ce-qui-reste-a-mesurer-etat-de-la-file-9.md
reports/rapport-cerveau-modules.md
reports/README.md
reports/rapport-cerveau-corrections.md
reports/cerveau-mesures-corrigees.json
  ```

- **bash** `{"command": "cat /tmp/a3-m2.md 2>/dev/null | head -100", "description": "Read A3 report md"}`

  ```
# A3 — M2 : champs dorsaux multiples, dernier état et contexte

_Sprint autonome 24 h — sous-agent A3. Résultats mesurés sur GPU RTX 5000, encodeur `/tmp/natif-600-512-8-align-s1` gelé, `PYTHONPATH=tools`, `CUDA_VISIBLE_DEVICES=0`._

## 1. Ce qui est mesuré

Le prototype M2 d'origine avait deux têtes linéaires sur un encodeur gelé : `action` (ventrale) et `de` (dorsale), entraînées sur les surfaces synthétiques (`items_synth`, 16662 items) et testées sur les 528 surfaces réelles (`items`). Ici, la voie dorsale est étendue à **quatre champs** : `de`, `vers`, `point`, `chemin_0`. Chaque tête est indépendante ; une lésion remplace ses logits par du bruit gaussien.

Quatre conditions sont comparées, à nombre de pas égal (300) sauf mention :

- **`mean+last`** : moyenne masquée + dernier état (référence, comme M2) ;
- **`mean`** : moyenne seule (ablation du dernier état), à 300 pas **et** à 1 000 pas ;
- **`last`** : dernier état seul ;
- **`+contexte`** : moyenne + dernier état de la surface **et** du RSN de contexte, avec les mêmes têtes ; contexte réel, permuté ou vide à l'évaluation.

Le découpage honnête du test réel est calculé après normalisation : une surface est **vue** si sa f
… [8154 caractères tronqués]
  ```

- **bash** `{"command": "cat /tmp/a3_m2_driver.py 2>/dev/null | head -200", "description": "Read A3 driver script"}`

  ```
#!/usr/bin/env python3
"""A3-M2 : champs dorsaux multiples, ablation du dernier état et du contexte."""
import collections
import hashlib
import json
import math
import platform
import statistics
import time

import torch
from transformers import AutoModelForCausalLM

from cerveau.voies import entrainer, evaluer_champs, VALEURS
from semantique.normalisation import normaliser
from semantique.synth_corpus import items_synth
from semantique.typed_corpus import items

BASE = "/tmp/natif-600-512-8-align-s1"
FIELDS = ("de", "vers", "point", "chemin_0")
SEEDS = [1, 2, 3]
PAS, LOT, SEQ, SEQ_CTX = 300, 32, 64, 192
CONDITIONS = [
    {"key": "mean+last", "pool": "mean+last", "pas": 300, "contexte": False,
     "seeds": [1, 2, 3]},
    {"key": "mean-300", "pool": "mean", "pas": 300, "contexte": False,
     "seeds": [1]},
    {"key": "last", "pool": "last", "pas": 300, "contexte": False,
     "seeds": [1, 2, 3]},
    {"key": "contexte", "pool": "mean+last", "pas": 300, "contexte": True,
     "seeds": [1, 2, 3]},
]
# Contrôle exploratoire à 1 000 pas, 1 graine (mesuré à part, même code) :
# la moyenne seule a besoin de plus de pas pour converger. Ce n'est pas la
# comparaison principale (3 grai
… [6977 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 200,400p /tmp/a3_m2_driver.py", "description": "Read rest of A3 driver"}`

  ```
"n": per[0]["n"],
        "chance": per[0]["chance"],
        "majorite": per[0]["majorite"],
        "exact_par_graine": {str(s): r["exact"] for s, r in zip(runs, per)},
        "exact_moyen": moyenne([r["exact"] for r in per]),
        "exact_ecart_type": ecart_type([r["exact"] for r in per]),
        "macro_moyen": moyenne([r["macro_rappel"] for r in per]),
        "par_classe_moyen": {},
        "lesions_moyennes": {
            lese: {"action": moyenne([r["lesions"][lese]["action"] for r in per])}
            for lese in ("ventrale", "dorsale")
        },
    }
    for c in sorted({c for r in per for c in r["par_classe"]}, key=str):
        rs = [r["par_classe"][c]["rappel"] for r in per if c in r["par_classe"]]
        agg["par_classe_moyen"][c] = {"rappel_moyen": moyenne(rs)}
    out["action_global"] = agg
    if cond["contexte"]:
        out["variantes"] = {}
        for mode in ("reel", "melange", "vide"):
            out["variantes"][mode] = {}
            for f in FIELDS:
                per = [runs[s][mode][f] for s in runs]
                out["variantes"][mode][f] = {
                    "exact_moyen": moyenne([r["exact"] for r in per]),
                    "macro_moy
… [10304 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat /tmp/a3-m2-partial.json | head -50; echo ---; ls -la /tmp/a3-m2.json /tmp/a3-m2-partial.json", "description": "Inspect A3 partial JSON"}`

  ```
, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48], "ok": [1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], "pred_action": ["poser", "poser", "poser", "jouer_carte", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser"], "cible_action": ["poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "poser", "po
… [48731 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv && ls -la /tmp/natif-600-512-8-align-s1/", "description": "Check GPU state and base model"}`

  ```
name, memory.used [MiB], memory.total [MiB], utilization.gpu [%]
Quadro RTX 5000, 4 MiB, 16384 MiB, 0 %
Quadro RTX 5000, 124 MiB, 16384 MiB, 0 %
total 123596
drwxr-xr-x.   2 stephane stephane       100 26 oct 16:04 .
drwxrwxrwt. 696 root     root         20400 27 oct 10:30 ..
-rw-r--r--.   1 stephane stephane       974 26 oct 16:04 config.json
-rw-r--r--.   1 stephane stephane       153 26 oct 16:04 generation_config.json
-rw-------.   1 stephane stephane 126553768 26 oct 16:04 model.safetensors
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import items_synth\nfrom semantique.normalisation import normaliser\nimport collections\n\nits, syn = items(), items_ … [765 caractères tronqués]`

  ```
reel 528 synth 16662

=== de: reel 146, synth 3660, inedits 20
'e2-e4' -> 'e2-e4' code 52 lang notation jeu echecs
'e2 e4' -> 'e2 e4' code 52 lang notation jeu echecs
'e4' -> 'e4' code 52 lang notation jeu echecs
'E4' -> 'e4' code 52 lang notation jeu echecs
'le pion de e2 vers e4' -> 'le [echecs.piece.P] de e2 vers e4' code 52 lang fr jeu echecs
'pawn from e2 to e4' -> '[echecs.piece.P] from e2 to e4' code 52 lang en jeu echecs
'Nf3' -> 'nf3' code 62 lang notation jeu echecs
'Cf3' -> 'cf3' code 62 lang fr jeu echecs
'cavalier de g1 vers f3' -> '[echecs.piece.N] de g1 vers f3' code 62 lang fr jeu echecs
'le cavalier g1 va en f3' -> 'le [echecs.piece.N] g1 va en f3' code 62 lang fr jeu echecs
'knight from g1 to f3' -> '[echecs.piece.N] from g1 to f3' code 62 lang en jeu echecs
'O-O' -> 'o-o' code 60 lang notation jeu echecs
'petit roque' -> 'petit roque' code 60 lang fr jeu echecs
'O-O-O' -> 'o-o-o' code 60 lang notation jeu echecs
'grand roque' -> 'grand roque' code 60 lang fr jeu echecs
'exd6' -> 'exd6' code 28 lang notation jeu echecs
'a8=Q' -> 'a8=q' code 8 lang notation jeu echecs
'a7a8q' -> 'a7a8q' code 8 lang notation jeu echecs
'Nf3' -> 'nf3' code 62 lang notation jeu echecs
… [3156 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat /tmp/natif-600-512-8-align-s1/config.json; echo; sed -n 1,120p tools/semantique/modele.py", "description": "Read base config and model module"}`

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
    "rope_type": "default"
  },
  "router_aux_loss_coef": 0.001,
  "sliding_window": null,
  "tie_word_embeddings": true,
  "transformers_version": "5.15.0",
  "use_cache": true,
  "use_sliding_window": false,
  "vocab_size": 256
}

#!/usr/bin/env python3
"""modele.py — l'encodeur sémantique et le décodeur sens→texte du natif.

Le même `route` fait les deux :
- **encodeur** : il lit la surface (octets), et l'état caché du dernier octet est
  projeté en u
… [5184 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,140p tools/semantique/entrainer.py", "description": "Read entrainer main script"}`

  ```
#!/usr/bin/env python3
"""entrainer.py — le protocole sémantique natif, première version.

Trois choses, dans cet ordre :
1. **rejouer** des entrées multilingues parallèles : le même article, dans plusieurs
   langues, doit donner le même `z` (alignement) et se reconstruire (même langue) ;
2. **sens → texte** : de `z` et de la langue cible, le décodeur produit le texte ;
   la traduction est mesurée contre la référence humaine, avec le plancher
   source→référence ;
3. **convergence** : on arrête quand le rappel parallèle ne progresse plus ; la
   sonde de langue et le rappel mélangé sont les contrôles négatifs.

Usage :
    python3 tools/semantique/entrainer.py --checkpoint /tmp/natif-600-512-8-align-s1 \
        --pas 600 --eval-tous 100 --sortie /tmp/semantique-poc
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import random
import sys
import time

import torch
import torch.nn.functional as F

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from llm.mesure import chrf  # noqa: E402
from semantique.corpus import LANGUES, charger, decouper, exemple, lot  # noqa: E402
from semantique.modele import Semantique  # no
… [4626 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nj=json.load(open('/tmp/a3-m2.json'))\nprint(j.keys())\nprint(json.dumps(j['meta'], ensure_ascii=False, indent=1)[:1500])\nfor key,c in j['conditions'].items():\n    print(key, c['pas'], c['seed … [238 caractères tronqués]`

  ```
dict_keys(['meta', 'donnees', 'conditions', 'controle_1000_1_graine', 'comparaisons', 'negatifs', 'autocritique'])
{
 "date": "2026-10-27 10:23:27",
 "base": "/tmp/natif-600-512-8-align-s1",
 "n_synth": 16662,
 "n_reel": 528,
 "seeds": [
  1,
  2,
  3
 ],
 "pas": 300,
 "lot": 32,
 "seq": 64,
 "seq_ctx": 192,
 "gpu": "Quadro RTX 5000",
 "torch": "2.11.0+cu130",
 "python": "3.13.15",
 "duree_s": 803.0,
 "fichier_voies_sha256": "a531546e340f7ca416bf5d00a3d41ae328e9d327ffbe339fb3390f5590327691",
 "reference_originale": {
  "action": 0.9863013698630136,
  "de": 0.9315068493150684,
  "n": 146,
  "split_3_graines": {
   "vu": "126/126 = 100 %",
   "inedit": "10, 11, 10 sur 20"
  }
 },
 "graines_par_condition": {
  "mean+last": [
   1,
   2,
   3
  ],
  "mean-300": [
   1
  ],
  "last": [
   1,
   2,
   3
  ],
  "contexte": [
   1,
   2,
   3
  ],
  "controle_1000": [
   1
  ]
 }
}
mean+last 300 [1, 2, 3] train_s ?
mean-300 300 [1] train_s ?
last 300 [1, 2, 3] train_s ?
contexte 300 [1, 2, 3] train_s ?
donnees {
 "de": {
  "n_reel": 146,
  "n_synth": 3660,
  "n_classes_reel": 6,
  "n_classes_synth": 10,
  "n_classes_tete": 65,
  "majorite": 0.4794520547945205,
  "chance": 0.015384615384615
… [1365 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import items_synth\nfrom semantique.normalisation import normaliser\nj=json.load(open('/tmp/a3-m2.json'))\nc=j['condition … [523 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ModuleNotFoundError: No module named 'semantique'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import items_synth\nfrom semantique.normalisation import normaliser\nj=json.load(open('/tmp/a3-m2.json') … [547 caractères tronqués]`

  ```
dict_keys(['pool', 'pas', 'contexte', 'seeds', 'fields', 'action_global'])
{'pool': 'str', 'pas': 'int', 'contexte': 'bool', 'seeds': 'list', 'fields': 'dict', 'action_global': 'dict'}
20
'e2-e4' |ctx: 'echecs etat trait=w roques=KQkq demi=0 plein=1 plateau=rnbqkbnr/ppppp | de 52 vers 36 roque None promo None
'e2 e4' |ctx: 'echecs etat trait=w roques=KQkq demi=0 plein=1 plateau=rnbqkbnr/ppppp | de 52 vers 36 roque None promo None
'e4' |ctx: 'echecs etat trait=w roques=KQkq demi=0 plein=1 plateau=rnbqkbnr/ppppp | de 52 vers 36 roque None promo None
'E4' |ctx: 'echecs etat trait=w roques=KQkq demi=0 plein=1 plateau=rnbqkbnr/ppppp | de 52 vers 36 roque None promo None
'le pion de e2 vers e4' |ctx: 'echecs etat trait=w roques=KQkq demi=0 plein=1 plateau=rnbqkbnr/ppppp | de 52 vers 36 roque None promo None
'pawn from e2 to e4' |ctx: 'echecs etat trait=w roques=KQkq demi=0 plein=1 plateau=rnbqkbnr/ppppp | de 52 vers 36 roque None promo None
'Nf3' |ctx: 'echecs etat trait=w roques=KQkq demi=0 plein=1 plateau=rnbqkbnr/ppppp | de 62 vers 45 roque None promo None
'Cf3' |ctx: 'echecs etat trait=w roques=KQkq demi=0 plein=1 plateau=rnbqkbnr/ppppp | de 62 vers 45 roque None promo None
'cavalier
… [1498 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,260p tools/jeux/regles/echecs.py", "description": "Read chess rules module part 1"}`

  ```
#!/usr/bin/env python3
"""regles.echecs — les règles complètes des échecs, sans dépendance.

Ce module est l'**étage 2** des échecs : il ne connaît que la position interne
(64 cases, trait, droits, en passant) et il rend les coups **légaux**, la
terminalité, une évaluation et le perft. Les notations (FEN, SAN, UCI, français)
sont dans `codecs/echecs.py` ; elles s'appuient sur ce module pour valider, pas
l'inverse.

Choix de représentation :
- indice 0 = a8, 7 = h8, 56 = a1, 63 = h1 (l'ordre de la FEN, lisible) ;
- pièce = (couleur << 3) | type, type 1..6 = pion, cavalier, fou, tour, dame, roi ;
- coups = (de, vers, promotion, drapeau), drapeau 0 normal, 1 double, 2 en
  passant, 3 petit roque, 4 grand roque ;
- `joue`/`annule` avec un undo : le perft et la recherche ne copient pas le
  plateau à chaque nœud ;
- hachage de Zobrist incrémental, pour la table de transposition de la recherche.

Le contrôle de correction est le **perft** : les nombres de feuilles aux
profondeurs 1-4 des six positions de référence sont connus et vérifiés dans
`tests/test_echecs.py`. Une règle oubliée (roque, en passant, promotion) change
le nombre immédiatement.
"""
from __future__ import annotations

im
… [8126 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"def \\|^class \\|^[A-Z_]* =\" tools/jeux/regles/echecs.py | head -80; echo ---DAMES---; grep -n \"def \\|^class \\|^[A-Z_]* =\" tools/jeux/regles/dames.py | head -60", "description": "List chess/dames APIs"}`

  ```
39:FICHIERS = "abcdefgh"
42:VALEURS = {PION: 100, CAVALIER: 320, FOU: 330, TOUR: 500, DAME: 900, ROI: 0}
44:_CENTRE = [
54:_AVANCE = [0] * 64
60:def piece(couleur: int, typ: int) -> int:
64:def couleur(p: int) -> int:
68:def typ(p: int) -> int:
72:def case_vers_indice(c: str) -> int:
79:def indice_vers_case(i: int) -> str:
83:def _coord(i: int) -> tuple[int, int]:
87:def _idx(r: int, c: int) -> int:
91:def _dans(r: int, c: int) -> bool:
96:_SAUTS_C = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
97:_SAUTS_R = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
98:VOISINS_CAVALIER = [[] for _ in range(64)]
99:VOISINS_ROI = [[] for _ in range(64)]
110:_DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
111:RAYONS = [[[] for _ in _DIRS] for _ in range(64)]
122:POUSSE = [[None] * 64 for _ in range(2)]
123:DOUBLE_POUSSEE = [[None] * 64 for _ in range(2)]
124:CAPTURES = [[[] for _ in range(64)] for _ in range(2)]
125:ATTAQUE_PION = [[[] for _ in range(64)] for _ in range(2)]
149:_DROIT_TOUR = {63: 1, 56: 2, 7: 4, 0: 8}  # h1, a1, h8, a8
153:Z_PIECE = [[_rng.getrandbits(64) for _ in range(64)] for _ in range(12)]
154
… [4312 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import items_synth\nfrom semantique.normalisation import normaliser\nj=json.load(open('/tmp/a3-m2.json') … [427 caractères tronqués]`

  ```
dict_keys(['conditions'])
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"voies import\\|from cerveau.voies\\|entrainer(\" --include=*.py tools | grep -v \"def entrainer\" | head -30; echo ---; sed -n 610,680p tools/jeux/regles/echecs.py; echo ---DAMESCOUP---; sed -n 88,110p tools/jeux/regles/dames.py", "descript … [55 caractères tronqués]`

  ```
tools/audit_drapeaux_harnais.py:128:        bon, msg = entrainer(racine, nom, drapeaux, a.pas, a.graine, [])
tools/n4_dessin_b.py:728:        r = entrainer(banc, bras, train, val, tests, a)
tools/sonder_udhr.py:141:        pred, top5, modele = entrainer(X[masque_train], y[masque_train], X[masque_test], len(classes))
tools/style_traducteur.py:93:    pred, top5, _ = entrainer(Xtr, ytr, Xte, 2)
tools/pas_de_pensee_non_lineaire.py:111:            m, perte = entrainer(Xtr, Ytr, a.cache, a.epochs, 1e-3, graine=1000 + g, lot=a.lot)
tools/pas_de_pensee_non_lineaire.py:122:            mn, _ = entrainer(Xtr, Ytr[mel], a.cache, a.epochs, 1e-3, graine=2000 + g, lot=a.lot)
tools/etat_de_plan.py:134:            m, perte = entrainer(Xtr, Ctr, a.cache, a.epochs, 1e-3, graine=1000 + g, lot=a.lot)
tools/etat_de_plan.py:139:            mn, _ = entrainer(Xtr, Cmel, a.cache, a.epochs, 1e-3, graine=2000 + g, lot=a.lot)
tools/plan_code.py:96:            m, perte = entrainer(Xn[tr], a.cache, a.code, a.epochs, 1e-3, graine=1000 + g)
tools/cerveau/tests/test_predictif.py:62:            m.entrainer(seqs)
tools/cerveau/tests/test_predictif.py:74:        m1.entrainer(seqs)
tools/cerveau/tests/test_predictif.py
… [5147 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"def \\|^class \\|^MULTI\" tools/jeux/lexique_multilingue.py | head -40; echo ---; grep -n \"def point_vers_gtp\\|def gtp_vers_point\\|def point_vers\" tools/jeux/regles/go.py; echo ---; grep -n \"def san\\|def action_depuis_coup\\|def rsn_de … [140 caractères tronqués]`

  ```
36:class CorrespondanceML:
45:def _domaine_valeur(concept: str) -> tuple[str, str]:
73:class Multilingue:
74:    def __init__(self, chemin: pathlib.Path | str = FICHIER) -> None:
80:    def depuis_donnees(cls, donnees: dict) -> "Multilingue":
87:    def _construire(self) -> None:
124:    def cherche(self, domaine: str, texte: str, max_ngram: int = 4) -> list[CorrespondanceML]:
133:        def ajoute(concept, valeur, langue, forme, pos):
156:    def detecte_langue(self, texte: str) -> str | None:
183:    def jeu(self, texte: str) -> tuple[str, float] | None:
194:    def formes(self, concept: str, langue: str) -> list[str]:
197:    def langues_du_concept(self, concept: str) -> list[str]:
200:    def concepts_de_langue(self, langue: str) -> list[str]:
203:    def permute(self, decalage: int = 1) -> "Multilingue":
222:    def couverture(self) -> dict:
253:MULTI = Multilingue()
---
273:def gtp_vers_point(s: str, n: int) -> int:
289:def point_vers_gtp(p: int, n: int) -> str:
306:def point_vers_sgf(p: int, n: int) -> str:
---
tools/jeux/regles/dames.py:330:def rsn_depuis_position(pos: Position, annotation: Annotation | None = None) -> RSN:
tools/jeux/regles/dames.py:355:def action_depuis_
… [179 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"SGF\\|sgf\\|\\[dd\\]\" -r tools/jeux | head -20", "description": "Search SGF handling in jeux"}`

  ```
tools/jeux/codecs/go.py:2:"""codecs.go — la surface du go : GTP, SGF, diagramme, français.
tools/jeux/codecs/go.py:4:Trois notations coexistent : **GTP** (`D4`, `pass`), **SGF** (`B[dd]`, `(;…;B[dd];W[pp])`)
tools/jeux/codecs/go.py:114:def _lit_sgf(texte: str, n_defaut: int = 19) -> tuple[list[int], int, int] | None:
tools/jeux/codecs/go.py:115:    """Lit un SGF simple : rend (coups, couleur_de_départ, komi) ou None."""
tools/jeux/codecs/go.py:130:        coups.append(G.sgf_vers_point(m.group(2), n))
tools/jeux/codecs/go.py:138:    formats = ("diagramme", "gtp", "sgf", "francais", "partie")
tools/jeux/codecs/go.py:149:        # 1. SGF (état de partie, action ou partie)
tools/jeux/codecs/go.py:152:            res = _lit_sgf(texte, n_ctx)
tools/jeux/codecs/go.py:155:                # une seule action SGF = un coup
tools/jeux/codecs/go.py:157:                    lec.format = "sgf"
tools/jeux/codecs/go.py:160:                                       "sgf", 0.95)
tools/jeux/codecs/go.py:172:                    lec.format = "sgf"
tools/jeux/codecs/go.py:175:                                       "sgf", 0.9)
tools/jeux/codecs/go.py:177:                    return self.echoue(lec, f"SGF illég
… [1050 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport collections, re\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import items_synth\nfrom semantique.normalisation import normaliser\nits, syn = items(), item … [1021 caractères tronqués]`

  ```
######## de : reel 146 synth 3660
SYNTH motifs: [('[C] a# a#', 1220), ('a#a#', 1220), ('[C] a#-a#', 1220)]
REEL motifs: [('[C] a# a#', 122), ('a#a#', 4), ('aa#', 4), ('a#', 2), ('[C] aaaa a# aa a#', 2), ('aaaaa aaaaa', 2), ('a#-a#', 1), ('a# a#', 1), ('aa [C] aa a# aaaa a#', 1), ('[C] aa a# aaaa a#', 1), ('aa [C] a# aa aa a#', 1), ('a-a', 1), ('a-a-a', 1), ('aaa#', 1), ('a#=a', 1), ('a#a#a', 1)]
REEL formats: [('multilingue', 122), ('san', 12), ('uci', 8), ('francais', 4)]
REEL langues: [('notation', 16), ('fr', 8), ('en', 4), ('ar', 2), ('bn', 2), ('ca', 2), ('cs', 2), ('da', 2), ('de', 2), ('el', 2)]
UNSEEN par format: Counter({'san': 11, 'uci': 5, 'francais': 4})

######## vers : reel 146 synth 3660
SYNTH motifs: [('[C] a# a#', 1220), ('a#a#', 1220), ('[C] a#-a#', 1220)]
REEL motifs: [('[C] a# a#', 122), ('a#a#', 4), ('aa#', 4), ('a#', 2), ('[C] aaaa a# aa a#', 2), ('aaaaa aaaaa', 2), ('a#-a#', 1), ('a# a#', 1), ('aa [C] aa a# aaaa a#', 1), ('[C] aa a# aaaa a#', 1), ('aa [C] a# aa aa a#', 1), ('a-a', 1), ('a-a-a', 1), ('aaa#', 1), ('a#=a', 1), ('a#a#a', 1)]
REEL formats: [('multilingue', 122), ('san', 12), ('uci', 8), ('francais', 4)]
REEL langues: [('notation', 16), ('fr', 8), 
… [1287 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 265,330p tools/jeux/regles/go.py; echo ---; sed -n 325,380p tools/jeux/regles/dames.py; echo ---; sed -n 789,860p tools/jeux/regles/echecs.py", "description": "Read go/dames/chess RSN helpers"}`

  ```
if d % 10 == 0:
        return str(d // 10)
    return f"{d // 10}.{d % 10}"


# ---------------------------------------------------------------------------
# Coordonnées : GTP, SGF, (ligne, colonne)
# ---------------------------------------------------------------------------
def gtp_vers_point(s: str, n: int) -> int:
    s = s.strip().upper()
    if len(s) < 2:
        raise ErreurGo(f"coordonnée GTP invalide : {s!r}")
    col = _LETTRES_GTP.find(s[0])
    if col < 0 or col >= n:
        raise ErreurGo(f"colonne GTP invalide : {s[0]!r}")
    try:
        rang = int(s[1:])
    except ValueError:
        raise ErreurGo(f"rangée GTP invalide : {s!r}")
    if not 1 <= rang <= n:
        raise ErreurGo(f"rangée GTP hors plateau : {rang}")
    return (n - rang) * n + col


def point_vers_gtp(p: int, n: int) -> str:
    row, col = _coord(p, n)
    return f"{_LETTRES_GTP[col]}{n - row}"


def sgf_vers_point(s: str, n: int) -> int:
    if s in ("", "tt"):
        return -1  # passe dans l'ancien SGF
    if len(s) != 2:
        raise ErreurGo(f"coordonnée SGF invalide : {s!r}")
    col = ord(s[0]) - 97
    row = ord(s[1]) - 97
    if not (0 <= col < n and 0 <= row < n):
        raise Erreu
… [5755 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 202,265p tools/jeux/regles/dames.py", "description": "Read dames applique"}`

  ```
def simples(self) -> list[Coup]:
        sortie = []
        for i, piece in enumerate(self.cases):
            if piece == VIDE or _couleur(piece) != self.trait:
                continue
            for d in self._directions(piece):
                j = VOISINS[i][d]
                if j is not None and self.cases[j] == VIDE:
                    sortie.append(Coup((i, j)))
        return sortie

    def coups_legaux(self) -> list[Coup]:
        caps = self.captures()
        if caps:
            return caps
        return self.simples()

    # ---- application ---------------------------------------------------
    def est_prise(self, coup: Coup) -> bool:
        """Une prise = un saut : le milieu du pas est occupé avant le coup."""
        for a, b in zip(coup.chemin, coup.chemin[1:]):
            over = MILEU.get((a, b))
            if over is not None and self.cases[over] != VIDE:
                return True
        return False

    def applique(self, coup: Coup) -> "Position":
        legal = self.coups_legaux()
        if coup not in legal:
            raise ErreurDames(f"coup illégal : {coup.numerique()}")
        return self._applique_direct(coup)

    def _applique_direct(
… [1307 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python - <<'EOF'\nimport time, torch\nfrom transformers import AutoModelForCausalLM\nfrom cerveau.voies import entrainer, evaluer_champs\nbase = AutoModelForCausalLM.from_pretrained(\" … [669 caractères tronqués]`

  ```
50 pas 9.6 s val 528
eval 1.5 s {'de': 0.486, 'vers': 0.514, 'point': 0.0, 'chemin_0': 0.843, 'action_global': 0.64}
[stderr]
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 947.82it/s]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"def normalise_forme\" -A30 tools/jeux/lexique.py", "description": "Read normalise_forme"}`

  ```
107:def normalise_forme(texte: str) -> str:
108-    """Forme de comparaison d'un libellé multilingue (même règle que le constructeur).
109-
110-    NFKC, casse pliée, diacritiques **optionnels** retirés (latin, grec,
111-    cyrillique, arabe, hébreu), diacritiques **constitutifs** gardés (indic,
112-    thaï), parenthèses de désambiguïsation retirées (« 馬 (國際象棋) » → « 馬 »),
113-    espaces normalisés, ponctuation de bord ôtée.
114-    """
115-    t = unicodedata.normalize("NFD", normalise(texte).casefold())
116-    t = sans_diacritiques(t)
117-    t = re.sub(r"\s*\([^)]*\)\s*$", "", t)
118-    t = t.replace("\u2019", "'").replace("`", "'")
119-    t = re.sub(r"\s+", " ", t).strip(" .,;:!?«»\"'")
120-    return unicodedata.normalize("NFC", t)
121-
122-
123-def unites(texte: str) -> list[str]:
124-    """Découpe une surface en unités : mots, nombres, symboles, ponctuation.
125-
126-    Le découpage est **manuel** et non une regex ASCII : il groupe les lettres
127-    Unicode, les chiffres et les **marques combinantes** (les voyelles
128-    dévanagaries, les signes thaïs) avec leur base, sépare les symboles de
129-    cartes, et laisse la ponctuation isolée. C'est ce qui permet `राज
… [366 caractères tronqués]
  ```

### 👤 Utilisateur

Agent f0969e87-af0c-43b1-93cf-f278d9c90846 sent a message: 
Timebox : donne un point maintenant et écris /tmp/a5-m2-generalisation.json/.md dès que tu as un résultat, même partiel. Termine ensuite ; un négatif net suffit.

### 🤖 Assistant

⏵ Sending an early finding to the parent, then implementing the augmentation

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "A5 — point d'étape + première autocritique (avant mesures) :\n\n1) Diagnostic des 20 items inédits `de`/`vers` : ils ne contiennent que 2 classes pour `de` (52=e2e4 ×6, 62=g1f3 ×6, 57=nc3 ×1) et 3 pour `vers` (36 ×6, 45 ×6, 42 ×1). Le  … [1477 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 25,72p tools/jeux/regles/dames.py; echo ---; PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nfrom jeux.regles import dames as D\npos=D.Position.depart()\nfor c in pos.coups_legaux()[:10]:\n    print(c.chemin, c.algebrique(), c.num … [117 caractères tronqués]`

  ```
VIDE = 0
NOIR_PION, BLANC_PION, NOIR_DAME, BLANC_DAME = 1, 2, 3, 4
NOIR, BLANC = 1, 2

_LETTRES = "abcdefgh"


def _coord(n: int) -> tuple[int, int]:
    """Numéro 1..32 → (rangée 0..7 depuis le haut, colonne 0..7)."""
    i = n - 1
    row, k = divmod(i, 4)
    offset = (row + 1) % 2
    return row, 2 * k + offset


def _num(row: int, col: int) -> int:
    offset = (row + 1) % 2
    if not (0 <= row < 8 and offset <= col < 8 and (col - offset) % 2 == 0):
        raise ValueError(f"case claire ou hors plateau : {row},{col}")
    k = (col - offset) // 2
    return row * 4 + k + 1


def indice_vers_case(i: int) -> str:
    row, col = _coord(i + 1)
    return _LETTRES[col] + str(8 - row)


def case_vers_indice(s: str) -> int:
    s = s.strip().lower()
    if len(s) != 2 or s[0] not in _LETTRES or s[1] not in "12345678":
        raise ValueError(f"case invalide : {s!r}")
    col = _LETTRES.index(s[0])
    row = 8 - int(s[1])
    return _num(row, col) - 1


def numero_vers_indice(n: int) -> int:
    if not 1 <= n <= 32:
        raise ValueError(f"numéro de case hors 1..32 : {n}")
    return n - 1


def indice_vers_numero(i: int) -> int:
    return i + 1


# Directions : 0 haut-gauche, 1
… [188 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Implementing rule-based template augmentation and the leakage guard in voies.py

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py", "old_string": "Les surfaces et le contexte sont normalisés (`normaliser`) puis lus en octets,\ncomme dans le prototype d'origine. L'API `entrainer`/`evaluer` reste compatible\navec `batterie.py` quand aucun champ dorsal supplément … [4085 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py", "old_string": "def _aleatoire_like(t: torch.Tensor, g: torch.Generator) -> torch.Tensor:\n    return torch.randn(t.shape, generator=g, device=t.device, dtype=t.dtype)", "new_string": "def _aleatoire_like(t: torch.Tensor, g: torch. … [9164 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py", "new_string": "_FENS_ECHECS = (", "old_string": "_FENS_ECHEcs = ("}`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py", "new_string": "    for fen in _FENS_ECHECS:", "old_string": "    for fen in _FENS_ECHEcs:"}`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py", "new_string": "def _lot(items_, lot, seq, rng, normaliseur=None):\n    norm = normaliseur or _normaliser\n    choix = [rng.choice(items_) for _ in range(lot)]\n    return pad([octets(norm(i.texte), seq) for i in choix]), choix\n\n … [1517 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py", "offset": 390, "limit": 130}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py</path>
<type>file</type>
<content>
390:             ctx = resume_contexte(E.rsn_depuis_position(pos))
391:             for coup in pos.coups_legaux():
392:                 r = E.action_depuis_coup(coup)
393:                 code = code_rsn(r)
394:                 for texte, famille, langue in _textes_echecs(pos, coup):
395:                     ajoute(texte, r, code, famille, langue, ctx)
396: 
397:     if "dames" in besoin:
398:         import jeux.regles.dames as D
399: 
400:         positions_d = ([D.Position.depart()] if "positions" not in familles
401:                        else _positions_dames(positions or 40, graine))
402:         for pos in positions_d:
403:             ctx = resume_contexte(D.rsn_depuis_position(pos))
404:             for coup in pos.coups_legaux():
405:                 r = D.action_depuis_coup(coup)
406:                 code = code_rsn(r)
407:                 for texte, famille, langue in _textes_dames(coup):
408:                     ajoute(texte, r, code, famille, langue, ctx)
409: 
410:     if "go" in besoin:
411:         import jeux.regles.go as G
412:         from jeux.rsn import RSN
413: 
41
… [5519 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py", "new_string": "def entrainer(base, pas: int = 400, lot: int = 32, seq: int = 64, graine: int = 1,\n              device: str = \"cuda\", synth: bool = False, champs=None,\n              pool: str = \"mean+last\", contexte: bool =  … [5172 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py", "new_string": "            (x, masque), choix = _lot(train_par_champ[nom], lot, seq, rng, norm)\n            ctx = ([i.contexte for i in choix] if contexte else None)\n            x, masque, c, cm = _entrees(choix, seq, seq_ctx, c … [261 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py", "new_string": "            choix_total = choix_action + [i for nom in champs for i in choix_par[nom]]\n            ctx = ([i.contexte for i in choix_total] if contexte else None)\n            x, masque, c, cm = _entrees(choix_tota … [303 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py", "limit": 160, "offset": 560}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py</path>
<type>file</type>
<content>
560:         "majorite": max(classes.values(), default=0) / max(1, n),
561:         "n_classes": len(classes),
562:         "n_classes_tete": n_classes_tete,
563:         "macro_rappel": macro,
564:         "par_classe": par_classe,
565:     }
566: 
567: 
568: def _stats(m, mor, nom, pa, pf, retour_pred: bool = False):
569:     pred = [VALEURS[nom][p] for p in pf]
570:     cible = [it.code[nom] for it in mor]
571:     pred_a = [VALEURS["action"][p] for p in pa]
572:     cible_a = [it.code["action"] for it in mor]
573:     res = _stats_classes(pred, cible, len(VALEURS[nom]))
574:     res_a = _stats_classes(pred_a, cible_a, len(VALEURS["action"]))
575:     res["action"] = res_a["exact"]
576:     res["action_macro_rappel"] = res_a["macro_rappel"]
577:     res["action_par_classe"] = res_a["par_classe"]
578:     if retour_pred:
579:         res["pred"] = pred
580:         res["cible"] = cible
581:         res["ok"] = [int(a == b) for a, b in zip(pred, cible)]
582:         res["pred_action"] = pred_a
583:         res["cible_action"] = cible_a
584:         res["ok_action"] = [int(a == b) for a, b
… [6892 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re, pathlib\np = pathlib.Path(\"tools/cerveau/voies.py\")\ns = p.read_text(encoding=\"utf-8\")\n# _passe signature + _entrees call\ns = s.replace(\n\"\"\"def _passe(m, mor, nom, device, lese=None, contextes=None, seq=64, seq_ … [4323 caractères tronqués]`

  ```
ok
38:- `normaliseur=` : permet d'évaluer et d'entraîner avec une normalisation plus
170:def _lot(items_, lot, seq, rng, normaliseur=None):
171:    norm = normaliseur or _normaliser
176:def _entrees(mor, seq, seq_ctx, contexte, contextes=None, normaliseur=None):
178:    norm = normaliseur or _normaliser
344:              normaliseur=None) -> list[ItemType]:
352:    La comparaison se fait après `normaliseur` (défaut : `normaliser`), donc
356:    norm = normaliseur or _normaliser
428:              exclure_surfaces=None, normaliseur=None):
445:    norm = normaliseur or _normaliser
479:                          normaliseur=norm)
589:           graine_lesion=0, lot=64, normaliseur=None):
601:                                    normaliseur)
622:            normaliseur=None):
629:    pa, pf = _passe(m, sous, champ, device, lese=lese, normaliseur=normaliseur)
641:                   normaliseur=None):
682:                        seq=seq, seq_ctx=seq_ctx, normaliseur=normaliseur)
688:                                normaliseur=normaliseur)
692:                                normaliseur=normaliseur)
711:                       seq=seq, seq_ctx=seq_ctx, normaliseur=normaliseur)
718:           
… [152 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport time, collections\nfrom cerveau.voies import augmenter, normaliser_coordonnees\nfrom semantique.typed_corpus import items\nfrom semantique.normalisation import normaliser\n\nt=time.t … [2399 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-1745]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-1745", "wait": true, "timeout_ms": 120000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ps aux | grep -E \"gpu-env/bin/python|a5\" | grep -v grep | head; echo ---; top -b -n1 | head -15", "description": "Check running python process CPU"}`

  ```
stephane 2649402  0.0  0.0   7828  4048 ?        Ss   10:44   0:00 bash -c cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF' import time, collections from cerveau.voies import augmenter, normaliser_coordonnees from semantique.typed_corpus import items from semantique.normalisation import normaliser  t=time.time() a = augmenter(("de","vers","point","chemin_0"), familles=("formes",), positions=0, graine=1,               exclure_surfaces=[i.texte for i in items()]) print("formes:", len(a), "en", round(time.time()-t,1), "s") print(collections.Counter(i.format for i in a).most_common(20)) t=time.time() b = augmenter(("de","vers","point","chemin_0"), familles=("formes","positions"), positions=40, graine=1,               exclure_surfaces=[i.texte for i in items()]) print("positions:", len(b), "en", round(time.time()-t,1), "s") print(collections.Counter(i.format for i in b).most_common(20)) from semantique.universaux import CHAMPS real=items() # classes covered for f in ("de","vers","point","chemin_0"):     cls_real={i.code[f] for i in real if i.code.get(f) is not None}     cls_aug={i.code[f] for i in b if i.code.get(f) is not None}     cls_sy
… [3308 caractères tronqués]
  ```

- **job_kill** `{"job_id": "bash-1745", "reason": "Trop lent, profilage nécessaire"}`

  ```
requested cancellation of job bash-1745
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && timeout 40 env PYTHONPATH=tools /home/stephane/gpu-env/bin/python -u - <<'EOF'\nimport faulthandler, time\nfaulthandler.dump_traceback_later(15, repeat=False)\nfrom cerveau.voies import _normaliser\nfrom semantique.normalisation import normaliser\npri … [545 caractères tronqués]`

  ```
import ok
6 norm 0.004
81 norm 0.055
items 528 0.0
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && timeout 60 env PYTHONPATH=tools /home/stephane/gpu-env/bin/python -u - <<'EOF'\nimport faulthandler, time\nfaulthandler.dump_traceback_later(12, repeat=True)\nfrom cerveau.voies import augmenter\nfrom semantique.typed_corpus import items\nprint(\"star … [322 caractères tronqués]`

  ```
start
formes: 803 0.9
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && timeout 120 env PYTHONPATH=tools /home/stephane/gpu-env/bin/python -u - <<'EOF'\nimport faulthandler, time\nfaulthandler.dump_traceback_later(15, repeat=True)\nfrom cerveau.voies import augmenter\nfrom semantique.typed_corpus import items\nprint(\"sta … [333 caractères tronqués]`

  ```
start
positions: 4069 3.8
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && timeout 120 env PYTHONPATH=tools /home/stephane/gpu-env/bin/python -u - <<'EOF'\nimport time, collections\nfrom cerveau.voies import augmenter, normaliser_coordonnees\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import item … [2336 caractères tronqués]`

  ```
items: formes 803 positions 4069 en 3.6 s
formats formes: [('go-fr', 320), ('sgf', 161), ('gtp', 76), ('nlp-fr', 70), ('nlp-en', 38), ('piece-espace', 20), ('piece-tiret', 20), ('uci-espace', 19), ('uci-tiret', 19), ('uci', 17), ('san', 16), ('alg-espace', 7), ('num-espace', 7), ('alg-sep', 6), ('num-sep', 4), ('san-fr', 3)]
formats pos: [('nlp-fr', 907), ('nlp-en', 512), ('go-fr', 320), ('piece-espace', 257), ('piece-tiret', 257), ('uci-espace', 252), ('uci-tiret', 251), ('uci', 250), ('san', 244), ('san-fr', 209), ('sgf', 161), ('gtp', 76), ('alg-espace', 70), ('num-espace', 70), ('alg-sep', 68), ('num-sep', 67), ('prise-piece', 44), ('prise', 43), ('promo-long', 4), ('alg-tiret', 4), ('promo-uci', 3)]

de: reel 146 | classes syn 10 aug 56 | inedits A3 18 | classes inedites couvertes 6/6 manquantes []
   inedits restant inedits sous augmentation: 18 -> Counter({62: 6, 52: 4, 60: 4, 8: 2, 28: 1, 57: 1})

vers: reel 146 | classes syn 16 aug 60 | inedits A3 18 | classes inedites couvertes 7/7 manquantes []
   inedits restant inedits sous augmentation: 18 -> Counter({45: 6, 36: 4, 62: 2, 58: 2, 0: 2, 19: 1, 42: 1})

point: reel 70 | classes syn 81 aug 81 | inedits A3 4 | classes ined
… [1938 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Adding tests for the augmentation, the leakage guard and the aggressive normalization

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_voies.py", "new_string": "if _TORCH:\n    from cerveau.voies import (\n        Voies, augmenter, entrainer, evaluer, evaluer_champs,\n        normaliser_coordonnees,\n    )\nfrom semantique.normalisation import normaliser\nfrom se … [186 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_voies.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_voies.py", "new_string": "    def test_entrainement_court(self):\n        base = _Base(8)\n        m, val = entrainer(base, pas=1, lot=2, seq=16, graine=1, device=\"cpu\",\n                           synth=True, champs=(\"de\", \" … [3566 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_voies.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"tools/cerveau/tests/test_voies.py\")\ns=p.read_text(encoding=\"utf-8\")\ns=s.replace('self.assertIn(\"B[aa]\", par_forme)\\n        self.assertEqual(par_forme[\"B[aa]\"][\"point\"], 0)',\n            … [735 caractères tronqués]`

  ```
ok
..........................................................F.......
======================================================================
FAIL: test_augmentation_familles_et_garde (cerveau.tests.test_voies.TestVoies.test_augmentation_familles_et_garde)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_voies.py", line 143, in test_augmentation_familles_et_garde
    self.assertIn("b[aa]", par_forme)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
AssertionError: 'b[aa]' not found in {'a2a3': {'jeu': 'echecs', 'action': 'deplacer', 'de': 48, 'vers': 40, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}, 'a2 a3': {'jeu': 'echecs', 'action': 'deplacer', 'de': 48, 'vers': 40, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}, 'a2-a3': {'jeu': 'echecs', 'action': 'deplacer', 'de': 48, 'vers': 40, 'promotio
… [48730 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"tools/cerveau/tests/test_voies.py\")\ns=p.read_text(encoding=\"utf-8\")\nstart=s.index(\"    def test_augmentation_familles_et_garde(self):\")\nend=s.index(\"    def test_entrainement_avec_augmentati … [2965 caractères tronqués]`

  ```
ok

----------------------------------------------------------------------
Ran 62 tests in 4.659s

FAILED (failures=3, errors=1)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest tools.cerveau.tests.test_voies -v 2>&1 | tail -60", "description": "Run voies tests verbosely"}`

  ```
test_augmentation_familles_et_garde (tools.cerveau.tests.test_voies.TestVoies.test_augmentation_familles_et_garde) ... FAIL
test_contexte_melange_et_vide (tools.cerveau.tests.test_voies.TestVoies.test_contexte_melange_et_vide) ... ok
test_entrainement_avec_augmentation_et_normalisation (tools.cerveau.tests.test_voies.TestVoies.test_entrainement_avec_augmentation_et_normalisation) ... ok
test_entrainement_court (tools.cerveau.tests.test_voies.TestVoies.test_entrainement_court) ... ok
test_evaluation_et_lesions (tools.cerveau.tests.test_voies.TestVoies.test_evaluation_et_lesions) ... ok
test_formes_des_tetes (tools.cerveau.tests.test_voies.TestVoies.test_formes_des_tetes) ... ok
test_le_contexte_change_le_code (tools.cerveau.tests.test_voies.TestVoies.test_le_contexte_change_le_code) ... ok
test_pools (tools.cerveau.tests.test_voies.TestVoies.test_pools) ... ok

======================================================================
FAIL: test_augmentation_familles_et_garde (tools.cerveau.tests.test_voies.TestVoies.test_augmentation_familles_et_garde)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephane/Data13
… [48731 caractères tronqués]
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

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -i 's/\\[echecs.piece.p\\] from a2 to a3/[echecs.piece.P] from a2 to a3/' tools/cerveau/tests/test_voies.py && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest tools.cerveau.tests.test_voies 2>&1 | tail -3", "description": "Fix expec … [40 caractères tronqués]`

  ```
Ran 8 tests in 3.041s

FAILED (failures=1)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest tools.cerveau.tests.test_voies 2>&1 | grep -E \"^(FAIL|ERROR|AssertionError|  File|    self)\" | head -20", "description": "Show concise test failure"}`

  ```
FAIL: test_augmentation_familles_et_garde (tools.cerveau.tests.test_voies.TestVoies.test_augmentation_familles_et_garde)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_voies.py", line 164, in test_augmentation_familles_et_garde
    self.assertNotIn("a2 a3", formes_garde)
AssertionError: 'a2 a3' unexpectedly found in {'p g2 g4', 'f2 f4', 'pierre blanche en b4', 'ligne 1 colonne 7', 'pierre noire en c6', 'b[gf]', 'b[cd]', 'jouer en a1', 'b[bi]', 'pierre blanche en h3', 'pierre noire en h2', 'j2', 'pierre blanche en j2', 'pierre blanche en h6', 'pierre noire en a1', 'jouer en g6', 'b[gi]', 'jouer en b6', 'pierre blanche en e9', 'h4', 'pierre blanche en j8', 'b[ha]', 'jouer en e4', 'f6', 'le [echecs.piece.N] de g1 vers f3', 'b[dc]', 'w[af]', 'pierre noire en e5', 'jouer en f2', '[echecs.piece.N] b1 to c3', 'jouer en j8', 'b[ba]', 'pierre blanche en j6', 'b[eb]', 'ligne 6 colonne 3', 'b[hd]', 'jouer en h6', 'pierre blanche en e2', 'p h2-h4', 'pierre noire en h1', 'w[dc]', 'ligne 2 colonne 2', 'b[gh]', 'a2 a4', 'pierre blanche en c5', 'd2', 'e6', 'c5', 'a4', 'ca3', 'a3', 'a2a4', 'jouer en c9', 'b3', 'f8', '[echecs.piece.P] a2 to a4', 'pierre blanche en e
… [12128 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -i 's/exclure_surfaces=(\"a2a3\", \"a2-a3\", \"B\\[aa\\]\")/exclure_surfaces=(\"a2a3\", \"a2 a3\", \"a2-a3\", \"B[aa]\")/' tools/cerveau/tests/test_voies.py && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest tools.cerveau.tests.test … [76 caractères tronqués]`

  ```
Ran 8 tests in 3.651s

OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -3", "description": "Run full cerveau test suite"}`

  ```
Ran 68 tests in 25.822s

FAILED (errors=1)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | grep -A12 \"^ERROR\"", "description": "Show test error detail"}`

  ```
ERROR: setUpClass (cerveau.tests.test_lesion.TestLesion)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py", line 12, in setUpClass
    cls.r = batterie_lesions(rapide=True)
            ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py", line 648, in batterie_lesions
    "M2_mode": m2r.get("mode"),
                       ^^^^^^^^
KeyError: 'preservation'

----------------------------------------------------------------------
Ran 68 tests in 25.095s
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"M2_mode\\|preservation\\|def m2\\|voies\" tools/cerveau/lesion.py | head -20; git stash list; git diff --stat", "description": "Check lesion M2 dependency and git diff stat"}`

  ```
14:  **vrai ``voies.py``** est exécuté (encodeur natif gelé, entraînement des têtes
99:# M2 — les deux voies (voies.py réel, proxy bayésien en repli)
202:         "preservation": {"action_sous_lesion_dorsale": a,
205:        n, statut="proxy CPU (bayes naïf, deux têtes) ; voies.py non exécuté",
214:def _m2_voies(pas: int = 300, graines=(1,), device: str | None = None,
216:    """Le vrai M2 : encodeur natif gelé + têtes ventrale/dorsale de ``voies.py``.
225:    from cerveau.voies import entrainer, evaluer
266:        "couper la voie ventrale (action) / dorsale (de) — voies.py réel",
276:         "preservation": {"action_sous_lesion_dorsale": a_d,
282:        statut=(f"voies.py réel : base {base}, {pas} pas, graines "
291:    r["mode"] = "voies"
302:    if mode not in ("auto", "voies", "proxy"):
303:        raise ValueError(f"m2 inconnu : {mode!r} (auto, voies, proxy)")
307:        return _m2_voies(graines=graines)
309:        if mode == "voies":
312:        r["statut"] = (f"proxy CPU (voies.py non exécuté : "
609:    """Batterie M1–M9. ``m2`` : auto (réel si possible), voies, proxy."""
635:        "protocole": {"rapide": rapide, "cpu": m2r.get("mode") != "voies",
648:            "M2
… [626 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 180,320p tools/cerveau/lesion.py", "description": "Read lesion M2 functions"}`

  ```
ok_d_rand += int(rd == it.code["de"])
            if it.code["de"] is not None:
                ok_d_rand_nn += int(rd == it.code["de"])
    a, d = ok_a / n, ok_d / n
    a_rand = ok_a_rand / (n * repetitions)
    d_rand = ok_d_rand / (n * repetitions)
    a_prio, d_prio = ok_a_prio / n, ok_d_prio / n
    d_nn = ok_d_nn / max(1, n_nn)
    d_rand_nn = ok_d_rand_nn / max(1, n_nn * repetitions)
    d_prio_nn = ok_d_prio_nn / max(1, n_nn)
    r = _entree(
        "couper la voie ventrale (action) / dorsale (de) — tête détruite",
        {"action": a, "de": d, "de_non_nul": d_nn, "n_de_non_nul": n_nn},
        {"action": a_rand, "de": d_rand,
         "avec_priori": {"action": a_prio, "de": d_prio},
         "ventrale": {"action": a_rand, "de": d, "de_non_nul": d_nn},
         "dorsale": {"action": a, "de": d_rand, "de_non_nul": d_rand_nn}},
        {"action": a - a_rand, "de": d - d_rand,
         "de_non_nul": d_nn - d_rand_nn,
         "avec_priori": {"action": a - a_prio, "de": d - d_prio,
                         "de_non_nul": d_nn - d_prio_nn},
         "majorite": {"action": a_prio, "de": d_prio},
         "preservation": {"action_sous_lesion_dorsale": a,
                        
… [5590 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest tools.cerveau.tests.test_lesion 2>&1 | tail -4; git diff --stat tools/cerveau/lesion.py", "description": "Rerun lesion test alone"}`

  ```
----------------------------------------------------------------------
Ran 11 tests in 29.224s

FAILED (failures=1)
 tools/cerveau/lesion.py | 252 ++++++++++++++++++++++++++++++++++++++++--------
 1 file changed, 214 insertions(+), 38 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest tools.cerveau.tests.test_lesion -v 2>&1 | grep -E \"^(test_|FAIL|ERROR|AssertionError|KeyError)\" | head -20; sed -n 625,660p tools/cerveau/lesion.py", "description": "Identify failing les … [28 caractères tronqués]`

  ```
test_json (tools.cerveau.tests.test_lesion.TestLesion.test_json) ... ok
test_m1_contexte (tools.cerveau.tests.test_lesion.TestLesion.test_m1_contexte) ... ok
test_m2_double_dissociation (tools.cerveau.tests.test_lesion.TestLesion.test_m2_double_dissociation) ... ok
test_m3_tampon (tools.cerveau.tests.test_lesion.TestLesion.test_m3_tampon) ... ok
test_m4_stockage (tools.cerveau.tests.test_lesion.TestLesion.test_m4_stockage) ... ok
test_m5_transitions (tools.cerveau.tests.test_lesion.TestLesion.test_m5_transitions) ... ok
test_m6_porte (tools.cerveau.tests.test_lesion.TestLesion.test_m6_porte) ... ok
test_m7_modulation (tools.cerveau.tests.test_lesion.TestLesion.test_m7_modulation) ... ok
test_m8_sommeil (tools.cerveau.tests.test_lesion.TestLesion.test_m8_sommeil) ... FAIL
test_sham (tools.cerveau.tests.test_lesion.TestLesion.test_sham) ... ok
test_structure (tools.cerveau.tests.test_lesion.TestLesion.test_structure) ... ok
FAIL: test_m8_sommeil (tools.cerveau.tests.test_lesion.TestLesion.test_m8_sommeil)
AssertionError: [0.0, 0.0, 0.0] != 0.0
FAILED (failures=1)
    deficits = {k: v["deficit"] for k, v in modules.items()}
    plats = []
    for k, v in modules.items():
        d = v
… [1695 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Writing the measurement driver, then running baseline vs augmented at 1000 steps

- **write** `{"file_path": "/tmp/a5_driver.py", "content": "#!/usr/bin/env python3\n\"\"\"A5 — généralisation de M2 aux surfaces inédites (augmentation par les règles).\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport collections\nimport hashlib\nimport json\nimport math\nimport pathlib\nimpo … [13220 caractères tronqués]`

  ```
<path>/tmp/a5_driver.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python /tmp/a5_driver.py --quick --conditions baseline-1000,aug-pos,aug-pos-norm --out /tmp/a5-quick.json 2>&1 | tail -20", "description": "Run quick end-to-end validation of driver", "timeoutMs": 3000 … [3 caractères tronqués]`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 922.34it/s]
[baseline-1000]
  baseline-1000 graine 1 : 4 s, n_aug=0
  -> /tmp/a5-quick.json (33 s)
[aug-pos]
  aug-pos graine 1 : 18 s, n_aug=4069
  -> /tmp/a5-quick.json (98 s)
[aug-pos-norm]
  aug-pos-norm graine 1 : 2 s, n_aug=3172
  -> /tmp/a5-quick.json (108 s)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=0 nohup /home/stephane/gpu-env/bin/python /tmp/a5_driver.py --conditions baseline-1000,aug-formes,aug-pos > /tmp/a5-main.log 2>&1 &\necho \"job pid $!\"", "description": "Launch main experiments in background", "run_in_background" … [7 caractères tronqués]`

  ```
started background job bash-1824
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Génère /tmp/a5-m2-generalisation.md à partir du JSON mesuré.\"\"\"\nfrom __future__ import annotations\n\nimport collections\nimport json\nimport pathlib\nimport sys\n\nJSON = pathlib.Path(\"/tmp/a5-m2-generalisation.json\")\nMD = pathlib.Path(\"/tmp/a5-m2- … [13156 caractères tronqués]`

  ```
<path>/tmp/a5_md.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 👤 Utilisateur

background job bash-1824 (bash: cd /home/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=0 nohup /home/stephane/gpu-env/bin/python /tmp/a5_driver.py --conditions baseline-1000,aug-formes,aug-pos > /tmp/a5-main.log 2>&1 &
echo "job pid $!") finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "tail -5 /tmp/a5-main.log; ls -l /tmp/a5-m2-generalisation.json 2>/dev/null; ps aux | grep a5_driver | grep -v grep | awk '{print $2, $10}'", "description": "Check main experiment progress"}`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1034.74it/s]
[baseline-1000]
2711384 0:00
2711385 1:22
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nj=json.load(open('/tmp/a5-quick.json'))\nfor k,c in j['conditions'].items():\n    print(k, 'aug', c['aug'], 'norm', c['norm'])\n    for f in ('de','vers','point','chemin_0'):\n        r=c['resu … [421 caractères tronqués]`

  ```
baseline-1000 aug None norm std
   de n 146 vu 126 ineditA3 20 covA3 13 new 0 | exact 0.075 inedit 0.35
   vers n 146 vu 126 ineditA3 20 covA3 13 new 0 | exact 0.466 inedit 0.25
   point n 70 vu 66 ineditA3 4 covA3 4 new 0 | exact 0.0 inedit 0.0
   chemin_0 n 70 vu 56 ineditA3 14 covA3 13 new 0 | exact 0.957 inedit 0.786
aug-pos aug ['formes', 'positions'] norm std
   de n 146 vu 126 ineditA3 20 covA3 13 new 7 | exact 0.055 inedit 0.25
   vers n 146 vu 126 ineditA3 20 covA3 13 new 7 | exact 0.007 inedit 0.0
   point n 70 vu 66 ineditA3 4 covA3 4 new 0 | exact 0.0 inedit 0.0
   chemin_0 n 70 vu 56 ineditA3 14 covA3 13 new 1 | exact 0.0 inedit 0.0
aug-pos-norm aug ['formes', 'positions'] norm agressif
   de n 146 vu 128 ineditA3 18 covA3 11 new 7 | exact 0.493 inedit 0.278
   vers n 146 vu 128 ineditA3 18 covA3 11 new 7 | exact 0.925 inedit 0.444
   point n 70 vu 66 ineditA3 4 covA3 4 new 0 | exact 0.0 inedit 0.0
   chemin_0 n 70 vu 56 ineditA3 14 covA3 13 new 1 | exact 0.0 inedit 0.0
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nfrom cerveau.voies import augmenter\nfrom semantique.typed_corpus import items\nfrom semantique.normalisation import normaliser\nreal=items()\na=augmenter((\"de\",\"vers\",\"point\",\"chemi … [599 caractères tronqués]`

  ```
chemin classes aug: 30 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
21 in True 9 in True 8 in True
'c3-d4' 21 norm c3-d4
'10-14' 9 norm 10-14
  ```

- **bash** `{"command": "tail -3 /tmp/a5-main.log; date '+%H:%M:%S'; ps -o pid,etime,time,%cpu -p 2711385 2>/dev/null", "description": "Check main run elapsed time"}`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1034.74it/s]
[baseline-1000]
11:03:21
    PID     ELAPSED     TIME %CPU
2711385       02:18 00:02:23  104
  ```

- **bash** `{"command": "sleep 150; tail -5 /tmp/a5-main.log; ls -l /tmp/a5-m2-generalisation.json 2>/dev/null; date '+%H:%M:%S'", "description": "Wait and check main run progress", "timeoutMs": 180000}`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1034.74it/s]
[baseline-1000]
  baseline-1000 graine 1 : 182 s, n_aug=0
11:06:23
  ```

- **bash** `{"command": "sleep 240; tail -4 /tmp/a5-main.log; ls -l /tmp/a5-m2-generalisation.json 2>/dev/null; date '+%H:%M:%S'", "description": "Wait and check baseline completion", "timeoutMs": 270000}`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1034.74it/s]
[baseline-1000]
  baseline-1000 graine 1 : 182 s, n_aug=0
  baseline-1000 graine 2 : 180 s, n_aug=0
11:10:52
  ```

- **bash** `{"command": "sleep 200; tail -6 /tmp/a5-main.log; ls -l /tmp/a5-m2-generalisation.json 2>/dev/null; date '+%H:%M:%S'", "description": "Check baseline results file", "timeoutMs": 230000}`

  ```
[baseline-1000]
  baseline-1000 graine 1 : 182 s, n_aug=0
  baseline-1000 graine 2 : 180 s, n_aug=0
  baseline-1000 graine 3 : 181 s, n_aug=0
  -> /tmp/a5-m2-generalisation.json (630 s)
[aug-formes]
-rw-r--r--. 1 stephane stephane 212905 27 oct 11:11 /tmp/a5-m2-generalisation.json
11:14:29
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python /tmp/a5_md.py && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nj=json.load(open('/tmp/a5-m2-generalisation.json'))\nc=j['conditions']['baseline-1000']['resultats']['fields']\nfor f in ('de','vers','point', … [545 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "/tmp/a5_md.py", line 246, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/tmp/a5_md.py", line 75, in main
    syn = {f: {}}  # lue depuis les masques
           ^
UnboundLocalError: cannot access local variable 'f' where it is not associated with a value
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport re, pathlib\np=pathlib.Path('/tmp/a5_md.py')\ns=p.read_text(encoding='utf-8')\ns=s.replace(\"    syn = {f: {}}  # lue depuis les masques\\n\", \"\")\ns=s.replace(\"def f(x, pct=True):\", \"def fmt(x, pct=True):\")\n# remplace les appels f(...) par fm … [312 caractères tronqués]`

  ```
14 appels fmt
écrit /tmp/a5-m2-generalisation.md
  ```

- **bash** `{"command": "cd /tmp && grep -n \"[^a-zA-Z_]f(\" a5_md.py | head; echo ---; head -60 /tmp/a5-m2-generalisation.md; echo ...; sed -n 60,140p /tmp/a5-m2-generalisation.md", "description": "Check remaining formatter calls and MD content"}`

  ```
---
# A5 — M2 : généraliser aux surfaces inédites par les règles

_Sprint autonome 24 h — sous-agent A5. Encodeur `/tmp/natif-600-512-8-align-s1` gelé, GPU Quadro RTX 5000, `PYTHONPATH=tools`, `CUDA_VISIBLE_DEVICES=0`, 3 graines, 1000 pas._

**Question.** A3 a mesuré M2 sur 20 surfaces réelles inédites par champ (`de`, `vers`) : 10,7/20 et 11,7/20. Peut-on améliorer ce split par une **augmentation synthétique par les règles**, sans jamais montrer une surface réelle à l'entraînement ?

## 1. Ce qui est mesuré

Deux leviers, dans `tools/cerveau/voies.py` seulement :

1. **`augmenter`** : génère des surfaces à partir des **règles** des jeux (coups légaux de positions variées) et de **familles de templates** absentes du corpus synthétique : UCI collé/espacé/tireté, SAN anglais et français, prises `x`, promotions, `de … vers …`, `from … to …`, dames numérique `9x18`/algébrique `b6xd4`, go SGF `B[dd]` et français `ligne 4 colonne 4`. **Garde anti-fuite** : toute surface générée dont la forme normalisée égale celle d'un des 528 items réels est jetée. Le split inédit de A3 reste donc inédit, et l'augmentation ne peut pas gagner par mémoire de surface.

2. **`normaliser_coordonnees`** : nor
… [5468 caractères tronqués]
  ```

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "A5 — premier résultat mesuré (fichiers déjà écrits, encore partiels) :\n\n`/tmp/a5-m2-generalisation.json` et `.md` existent. Baseline M2 à **1 000 pas, 3 graines** (même encodeur gelé, mean+last, 4 champs) :\n- `de` 92,7 % ± 1,0 ; `ve … [1186 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

- **bash** `{"command": "sleep 280; tail -6 /tmp/a5-main.log; date '+%H:%M:%S'", "description": "Wait for aug-formes progress", "timeoutMs": 300000}`

  ```
baseline-1000 graine 2 : 180 s, n_aug=0
  baseline-1000 graine 3 : 181 s, n_aug=0
  -> /tmp/a5-m2-generalisation.json (630 s)
[aug-formes]
  aug-formes graine 1 : 182 s, n_aug=803
  aug-formes graine 2 : 183 s, n_aug=803
11:21:13
  ```

- **bash** `{"command": "sleep 180; tail -5 /tmp/a5-main.log; date '+%H:%M:%S'", "description": "Wait for aug-formes completion", "timeoutMs": 200000}`

  ```
aug-formes graine 1 : 182 s, n_aug=803
  aug-formes graine 2 : 183 s, n_aug=803
  aug-formes graine 3 : 179 s, n_aug=803
  -> /tmp/a5-m2-generalisation.json (1267 s)
[aug-pos]
11:24:30
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python /tmp/a5_md.py >/dev/null && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nj=json.load(open('/tmp/a5-m2-generalisation.json'))\nfor k in j['conditions']:\n    c=j['conditions'][k]['resultats']['fields']\n   … [564 caractères tronqués]`

  ```
baseline-1000
  de exact 0.927 | vu 1.000 | inedit 0.467 | cov 0.718 | new — | action 0.916
  vers exact 0.943 | vu 1.000 | inedit 0.583 | cov 0.897 | new — | action 0.916
  point exact 0.957 | vu 1.000 | inedit 0.250 | cov 0.250 | new — | action 0.986
  chemin_0 exact 0.810 | vu 0.988 | inedit 0.095 | cov 0.103 | new — | action 0.814
aug-formes
  de exact 0.952 | vu 1.000 | inedit 0.650 | cov 1.000 | new — | action 0.929
  vers exact 0.938 | vu 1.000 | inedit 0.550 | cov 0.846 | new — | action 0.929
  point exact 0.967 | vu 1.000 | inedit 0.417 | cov 0.417 | new — | action 1.000
  chemin_0 exact 0.881 | vu 0.994 | inedit 0.429 | cov 0.462 | new — | action 0.843
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nj=json.load(open('/tmp/a5-m2-generalisation.json'))\nfor f in ('de','vers','point','chemin_0'):\n    print('===',f)\n    for k in j['conditions']:\n        items=j['conditions'][k]['resultats'] … [331 caractères tronqués]`

  ```
=== de
baseline-1000 {'Nf3': 1, 'Cf3': 0, 'le cavalier g1 va en f3': 2, 'O-O': 0, 'petit roque': 0, 'O-O-O': 0, 'grand roque': 0, 'exd6': 0, 'a8=Q': 0, 'a7a8q': 0, 'Nc3': 0} | total 27 / 60
aug-formes {'O-O': 0, 'petit roque': 0, 'O-O-O': 0, 'grand roque': 0, 'exd6': 0, 'a8=Q': 0, 'a7a8q': 0} | total 36 / 60
=== vers
baseline-1000 {'Cf3': 1, 'O-O': 0, 'petit roque': 0, 'O-O-O': 0, 'grand roque': 0, 'exd6': 0, 'a8=Q': 0, 'a7a8q': 0, 'Nc3': 1} | total 32 / 60
aug-formes {'Cf3': 0, 'O-O': 0, 'petit roque': 0, 'O-O-O': 0, 'grand roque': 0, 'exd6': 0, 'a8=Q': 0, 'a7a8q': 0, 'Nc3': 0} | total 30 / 60
=== point
baseline-1000 {'pierre noire en D4': 0, 'ligne 4 colonne 4': 0, 'B[dd]': 0} | total 3 / 12
aug-formes {'pierre noire en D4': 2, 'ligne 4 colonne 4': 0, 'B[dd]': 0} | total 5 / 12
=== chemin_0
baseline-1000 {'9x18': 0, 'b6xd4': 0, 'le pion b6 prend en d4': 0, 'b6 prend d4': 0, '9x18x27': 0, 'b6xd4xf2': 0, 'le pion b6 prend en d4 puis f2': 1, '9-13': 0, '9-14': 0, 'b6-c5': 1, 'le pion de b6 vers c5': 2, 'c3-d4': 0, '10-14': 0} | total 4 / 42
aug-formes {'9x18': 2, 'b6xd4': 2, 'le pion b6 prend en d4': 0, 'b6 prend d4': 0, '9x18x27': 0, 'b6xd4xf2': 0, 'le pion b6 prend en d4 puis f2':
… [54 caractères tronqués]
  ```

- **bash** `{"command": "sleep 240; tail -5 /tmp/a5-main.log; date '+%H:%M:%S'", "description": "Wait for aug-pos progress", "timeoutMs": 260000}`

  ```
aug-formes graine 2 : 183 s, n_aug=803
  aug-formes graine 3 : 179 s, n_aug=803
  -> /tmp/a5-m2-generalisation.json (1267 s)
[aug-pos]
  aug-pos graine 1 : 195 s, n_aug=4069
11:29:14
  ```

- **bash** `{"command": "sleep 250; tail -5 /tmp/a5-main.log; date '+%H:%M:%S'", "description": "Wait for aug-pos completion", "timeoutMs": 270000}`

  ```
aug-formes graine 3 : 179 s, n_aug=803
  -> /tmp/a5-m2-generalisation.json (1267 s)
[aug-pos]
  aug-pos graine 1 : 195 s, n_aug=4069
  aug-pos graine 2 : 189 s, n_aug=4077
11:33:42
  ```

- **bash** `{"command": "sleep 220; tail -4 /tmp/a5-main.log; date '+%H:%M:%S'", "description": "Wait for aug-pos seed 3", "timeoutMs": 240000}`

  ```
aug-pos graine 1 : 195 s, n_aug=4069
  aug-pos graine 2 : 189 s, n_aug=4077
  aug-pos graine 3 : 196 s, n_aug=3172
  -> /tmp/a5-m2-generalisation.json (1988 s)
11:37:25
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python /tmp/a5_md.py >/dev/null && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nj=json.load(open('/tmp/a5-m2-generalisation.json'))\nfor k in j['conditions']:\n    c=j['conditions'][k]['resultats']['fields']\n   … [602 caractères tronqués]`

  ```
baseline-1000
  de exact 0.927 | inedit 0.467 (9/20) | cov 0.718 | new — | action 0.916
  vers exact 0.943 | inedit 0.583 (12/20) | cov 0.897 | new — | action 0.916
  point exact 0.957 | inedit 0.250 (1/4) | cov 0.250 | new — | action 0.986
  chemin_0 exact 0.810 | inedit 0.095 (1/14) | cov 0.103 | new — | action 0.814
aug-formes
  de exact 0.952 | inedit 0.650 (13/20) | cov 1.000 | new — | action 0.929
  vers exact 0.938 | inedit 0.550 (11/20) | cov 0.846 | new — | action 0.929
  point exact 0.967 | inedit 0.417 (2/4) | cov 0.417 | new — | action 1.000
  chemin_0 exact 0.881 | inedit 0.429 (6/14) | cov 0.462 | new — | action 0.843
aug-pos
  de exact 0.922 | inedit 0.433 (9/20) | cov 0.462 | new 0.381 | action 0.959
  vers exact 0.954 | inedit 0.667 (13/20) | cov 0.846 | new 0.333 | action 0.959
  point exact 0.971 | inedit 0.500 (2/4) | cov 0.500 | new — | action 0.995
  chemin_0 exact 0.867 | inedit 0.429 (6/14) | cov 0.385 | new 1.000 | action 0.905
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=0 nohup /home/stephane/gpu-env/bin/python /tmp/a5_driver.py --seeds 1 --conditions aug-pos-mean,aug-pos-last,aug-pos-norm,aug-pos-ctx --out /tmp/a5-ablations.json > /tmp/a5-ablations.log 2>&1 &\necho \"ablations pid $!\"", "descri … [72 caractères tronqués]`

  ```
started background job bash-1968
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nj=json.load(open('/tmp/a5-m2-generalisation.json'))\nfor f in ('de','vers','chemin_0'):\n    print('===',f)\n    base={it['texte']:it for it in j['conditions']['baseline-1000']['resultats']['fi … [486 caractères tronqués]`

  ```
=== de
aug-formes
   'Nf3' code 62 1/3 -> 3/3
   'Cf3' code 62 0/3 -> 3/3
   'le cavalier g1 va en f3' code 62 2/3 -> 3/3
   'Nf3' code 62 1/3 -> 3/3
   'Nc3' code 57 0/3 -> 3/3
aug-pos
   'e4' code 52 3/3 -> 0/3
   'E4' code 52 3/3 -> 0/3
   'le pion de e2 vers e4' code 52 3/3 -> 1/3
   'pawn from e2 to e4' code 52 3/3 -> 2/3
   'Nf3' code 62 1/3 -> 0/3
   'le cavalier g1 va en f3' code 62 2/3 -> 3/3
   'exd6' code 28 0/3 -> 2/3
   'a8=Q' code 8 0/3 -> 3/3
   'a7a8q' code 8 0/3 -> 3/3
   'Nf3' code 62 1/3 -> 0/3
=== vers
aug-formes
   'Cf3' code 45 1/3 -> 0/3
   'Nc3' code 42 1/3 -> 0/3
aug-pos
   'e4' code 36 3/3 -> 2/3
   'E4' code 36 3/3 -> 2/3
   'exd6' code 19 0/3 -> 1/3
   'a8=Q' code 0 0/3 -> 3/3
   'a7a8q' code 0 0/3 -> 3/3
=== chemin_0
aug-formes
   '9x18' code 8 0/3 -> 2/3
   'b6xd4' code 8 0/3 -> 2/3
   'le pion b6 prend en d4 puis f2' code 8 1/3 -> 0/3
   '9-13' code 8 0/3 -> 3/3
   '9-14' code 8 0/3 -> 2/3
   'b6-c5' code 8 1/3 -> 3/3
   'le pion de b6 vers c5' code 8 2/3 -> 3/3
   '9-13' code 8 0/3 -> 3/3
aug-pos
   '9x18' code 8 0/3 -> 2/3
   'b6xd4' code 8 0/3 -> 2/3
   'le pion b6 prend en d4' code 8 0/3 -> 1/3
   'b6 prend d4' code 8 0/3 -> 1/3
   'le pion b6 pre
… [223 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-1968 (bash: cd /home/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=0 nohup /home/stephane/gpu-env/bin/python /tmp/a5_driver.py --seeds 1 --conditions aug-pos-mean,aug-pos-last,aug-pos-norm,aug-pos-ctx --out /tmp/a5-ablations.json > /tmp/a5-ablations.log 2>&1 &
echo "ablations pid $!") finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "tail -6 /tmp/a5-ablations.log; date '+%H:%M:%S'; ls -l /tmp/a5-ablations.json 2>/dev/null", "description": "Check ablation progress"}`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 981.01it/s]
[aug-pos-mean]
11:38:38
[exit code: 2]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a5_md.py')\ns=p.read_text(encoding='utf-8')\n# 1) add count helper after fmt\ns=s.replace('''def fmt(x, pct=True):\n    if x is None:\n        return \"—\"\n    return f\"{100*x:.1f} %\" if pct else f\"{x:.3f}\"\n''',''' … [4573 caractères tronqués]`

  ```
patch ok
écrit /tmp/a5-m2-generalisation.md
### `de`

| condition | exact | vu | inédit A3 | inédit couvert A3 | nouvelle classe | action |
|---|---:|---:|---:|---:|---:|---:|
| `baseline-1000` | 92.7 % ± 1.0 % | 100.0 % | 46.7 % (9.3/20) | 71.8 % (9.3/13) | — (—) | 91.6 % |
| `aug-formes` | 95.2 % ± 0.0 % | 100.0 % | 65.0 % (13.0/20) | 100.0 % (13.0/13) | — (—) | 92.9 % |
| `aug-pos` | 92.2 % ± 1.0 % | 100.0 % | 43.3 % (8.7/20) | 46.2 % (6.0/13) | 38.1 % (2.7/7) | 95.9 % |

_n inédits A3 = 20 ; n inédits couverts A3 = 13 ; n nouvelles classes = 0._

| condition | Δ inédit A3 vs baseline | b/c (McNemar) | Δ inédit couvert A3 | b/c |
|---|---:|---|---:|---|
| `aug-formes` | +18.3 pts | 11/0, p=0.00098 | +28.2 pts | 11/0, p=0.00098 |
| `aug-pos` | -3.3 pts | 9/11, p=0.82 | -25.6 pts | 1/11, p=0.0063 |

_McNemar apparié sur les (item × graine) ; les mêmes items reviennent 3 fois (pseudo-réplication), la p-value est indicative._

| famille (inédits A3) | n | `baseline-1000` | `aug-formes` | `aug-pos` |
|---|---:|---:|---:|---:|
| `francais` | 4 | 50.0 % | 50.0 % | 25.0 % |
| `san` | 11 | 30.3 % | 63.6 % | 42.4 % |
| `uci` | 5 | 80.0 % | 80.0 % | 60.0 % |

| item inédit | famille | code
… [856 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a5_md.py')\ns=p.read_text(encoding='utf-8')\ns=s.replace('ad(\"| champ | n | inédits A3 | dont classe couverte A3 | classes distinctes des inédits couverts | plafond |\")',\n            'ad(\"| champ | n | inédits A3 | d … [1778 caractères tronqués]`

  ```
ok
écrit /tmp/a5-m2-generalisation.md
| item inédit | famille | code | `baseline-1000` (k/3) | `aug-formes` (k/3) | `aug-pos` (k/3) |
|---|---|---:|---:|---:|---:|
| `e2-e4` | uci | 52 | 3/3 | 3/3 | 3/3 |
| `e2 e4` | uci | 52 | 3/3 | 3/3 | 3/3 |
| `e4` | uci | 52 | 3/3 | 3/3 | 0/3 |
| `E4` | uci | 52 | 3/3 | 3/3 | 0/3 |
| `le pion de e2 vers e4` | francais | 52 | 3/3 | 3/3 | 1/3 |
| `pawn from e2 to e4` | francais | 52 | 3/3 | 3/3 | 2/3 |
| `Nf3` | san | 62 | 1/3 | 3/3 | 0/3 |
| `Cf3` | san | 62 | 0/3 | 3/3 | 0/3 |
| `cavalier de g1 vers f3` | san | 62 | 3/3 | 3/3 | 3/3 |
| `le cavalier g1 va en f3` | san | 62 | 2/3 | 3/3 | 3/3 |
| `knight from g1 to f3` | san | 62 | 3/3 | 3/3 | 3/3 |
| `O-O` | san | 60 | 0/3 | 0/3 | 0/3 |
| `petit roque` | francais | 60 | 0/3 | 0/3 | 0/3 |
| `O-O-O` | san | 60 | 0/3 | 0/3 | 0/3 |
| `grand roque` | francais | 60 | 0/3 | 0/3 | 0/3 |
| `exd6` | san | 28 | 0/3 | 0/3 | 2/3 |
| `a8=Q` | san | 8 | 0/3 | 0/3 | 3/3 |
| `a7a8q` | uci | 8 | 0/3 | 0/3 | 3/3 |
| `Nf3` | san | 62 | 1/3 | 3/3 | 0/3 |
| `Nc3` | san | 57 | 0/3 | 3/3 | 0/3 |

| item inédit | famille | code | `baseline-1000` (k/3) | `aug-formes` (k/3) | `aug-pos` (k/3) |
|---|---|---:|---:|---:|---:
… [221 caractères tronqués]
  ```

- **bash** `{"command": "tail -8 /tmp/a5-ablations.log; date '+%H:%M:%S'", "description": "Check ablation progress"}`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 981.01it/s]
[aug-pos-mean]
11:39:35
  ```

- **bash** `{"command": "cd /tmp && grep -n \"## 5. Verdict\" -A80 /tmp/a5_md.py | head -100", "description": "View verdict section code"}`

  ```
221:    ad("## 5. Verdict\n")
222-    base_c = conds.get("baseline-1000")
223-    aug_c = conds.get("aug-pos")
224-    if base_c and aug_c:
225-        for f in FIELDS:
226-            b = base_c["resultats"]["fields"][f]
227-            a = aug_c["resultats"]["fields"][f]
228-            d = (a["masques"]["inedit_a3"]["exact_moyen"]
229-                 - b["masques"]["inedit_a3"]["exact_moyen"])
230-            g = (a["exact_moyen"] - b["exact_moyen"])
231-            ad(f"- `{f}` : inédit A3 {fmt(b['masques']['inedit_a3']['exact_moyen'])} → "
232-               f"{fmt(a['masques']['inedit_a3']['exact_moyen'])} ({100*d:+.1f} pts) ; "
233-               f"global {fmt(b['exact_moyen'])} → {fmt(a['exact_moyen'])} ({100*g:+.1f} pts).")
234-        ad("")
235-    ad("**Réponse courte.** ")
236-    if base_c and aug_c:
237-        gains = []
238-        for f in FIELDS:
239-            d = (aug_c["resultats"]["fields"][f]["masques"]["inedit_a3"]["exact_moyen"]
240-                 - base_c["resultats"]["fields"][f]["masques"]["inedit_a3"]["exact_moyen"])
241-            gains.append((f, d))
242-        pos = [f for f, d in gains if d > 0.02]
243-        neg = [f for f, d in gains if d 
… [3393 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a5_md.py')\ns=p.read_text(encoding='utf-8')\nstart=s.index('    ad(\"## 5. Verdict\\\\n\")')\nend=s.index('    ad(\"## 7. Commandes\\\\n\")')\nnew='''    ad(\"## 5. Verdict\\\\n\")\n    base_c = conds.get(\"baseline-1000 … [7160 caractères tronqués]`

  ```
verdict patch ok
## 5. Verdict

| champ | `baseline-1000` inédit A3 | `aug-formes` inédit A3 | `aug-pos` inédit A3 | Δ aug-formes | Δ aug-pos |
|---|---:|---:|---:|---:|---:|
| `de` | 46.7 % (9.3/20) | 65.0 % (13.0/20) | 43.3 % (8.7/20) | +18.3 pts | -3.3 pts |
| `vers` | 58.3 % (11.7/20) | 55.0 % (11.0/20) | 66.7 % (13.3/20) | -3.3 pts | +8.3 pts |
| `point` | 25.0 % (1.0/4) | 41.7 % (1.7/4) | 50.0 % (2.0/4) | +16.7 pts | +25.0 pts |
| `chemin_0` | 9.5 % (1.3/14) | 42.9 % (6.0/14) | 42.9 % (6.0/14) | +33.3 pts | +33.3 pts |

**Gain net sur trois champs, pas sur le quatrième.** `aug-formes` (templates seuls, **aucune position ni classe nouvelle**) améliore le split inédit de A3 sur `de` (9,3 → 13/20), `chemin_0` (1 → 6/14) et `point` (1 → 2/4) ; sur `vers`, il perd un item (12 → 11/20). Le gain n'est pas de la mémoire de surface : la garde anti-fuite a généré **0** surface réelle, et `vu` est identique dans toutes les conditions.

**`aug-pos` déplace le gain.** Avec les positions et les classes nouvelles, `vers` passe à 13/20 et les promotions `a8=Q`/`a7a8q` sont lues 3/3 sur `de` et `vers` (0/3 avant) ; `exd6` passe à 2/3 sur `de`. Mais `de` retombe à 9/20 : le modèle cesse d'expl
… [4337 caractères tronqués]
  ```

- **bash** `{"command": "tail -8 /tmp/a5-ablations.log; date '+%H:%M:%S'; ls -l /tmp/a5-ablations.json 2>/dev/null", "description": "Check ablation progress again"}`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 981.01it/s]
[aug-pos-mean]
11:40:59
[exit code: 2]
  ```

- **bash** `{"command": "sleep 180; tail -8 /tmp/a5-ablations.log; date '+%H:%M:%S'; ls -l /tmp/a5-ablations.json 2>/dev/null", "description": "Wait for first ablation result", "timeoutMs": 200000}`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 981.01it/s]
[aug-pos-mean]
  aug-pos-mean graine 1 : 193 s, n_aug=4069
  -> /tmp/a5-ablations.json (240 s)
[aug-pos-last]
11:44:07
-rw-r--r--. 1 stephane stephane 83831 27 oct 11:42 /tmp/a5-ablations.json
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nj=json.load(open('/tmp/a5-ablations.json'))\nfor k,c in j['conditions'].items():\n    print(k)\n    for f in ('de','vers','point','chemin_0'):\n        r=c['resultats']['fields'][f]; m=r['masqu … [336 caractères tronqués]`

  ```
aug-pos-mean
  de exact 0.918 | inedit 0.400 cov 0.385 new 0.429
  vers exact 0.500 | inedit 0.400 cov 0.462 new 0.286
  point exact 0.057 | inedit 0.000 cov 0.000 new —
  chemin_0 exact 0.900 | inedit 0.571 cov 0.615 new 0.000
  ```

- **bash** `{"command": "sleep 200; tail -6 /tmp/a5-ablations.log; date '+%H:%M:%S'", "description": "Wait for aug-pos-last result", "timeoutMs": 220000}`

  ```
aug-pos-mean graine 1 : 193 s, n_aug=4069
  -> /tmp/a5-ablations.json (240 s)
[aug-pos-last]
  aug-pos-last graine 1 : 194 s, n_aug=4069
  -> /tmp/a5-ablations.json (484 s)
[aug-pos-ctx]
11:48:08
  ```

- **bash** `{"command": "grep -E \"^\\[|graine 1|->\" /tmp/a5-ablations.log; echo ---; /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nj=json.load(open('/tmp/a5-ablations.json'))\nprint(list(j['conditions']))\nfor k,c in j['conditions'].items():\n    print(k, c['pas'], c['pool'], c['norm'], c['duree_s … [340 caractères tronqués]`

  ```
[aug-pos-mean]
  aug-pos-mean graine 1 : 193 s, n_aug=4069
  -> /tmp/a5-ablations.json (240 s)
[aug-pos-last]
  aug-pos-last graine 1 : 194 s, n_aug=4069
  -> /tmp/a5-ablations.json (484 s)
[aug-pos-ctx]
---
['aug-pos-mean', 'aug-pos-last']
aug-pos-mean 1000 mean std 240.1989505290985
   de exact 0.918 | inedit 0.400 cov 0.385
   vers exact 0.500 | inedit 0.400 cov 0.462
   point exact 0.057 | inedit 0.000 cov 0.000
   chemin_0 exact 0.900 | inedit 0.571 cov 0.615
aug-pos-last 1000 last std 243.36573100090027
   de exact 0.945 | inedit 0.600 cov 0.692
   vers exact 0.966 | inedit 0.750 cov 0.923
   point exact 0.971 | inedit 0.500 cov 0.500
   chemin_0 exact 0.857 | inedit 0.429 cov 0.462
  ```

- **bash** `{"command": "sleep 300; tail -8 /tmp/a5-ablations.log; date '+%H:%M:%S'", "description": "Wait for context and norm ablations", "timeoutMs": 320000}`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 981.01it/s]
[aug-pos-mean]
  aug-pos-mean graine 1 : 193 s, n_aug=4069
  -> /tmp/a5-ablations.json (240 s)
[aug-pos-last]
  aug-pos-last graine 1 : 194 s, n_aug=4069
  -> /tmp/a5-ablations.json (484 s)
[aug-pos-ctx]
11:53:54
  ```

### 👤 Utilisateur

<system-reminder>
Updated instructions from: AGENTS.md

This file changed after it was loaded. Use the following content instead of the previously loaded instructions from this file.

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

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a5_md.py')\ns=p.read_text(encoding='utf-8')\n# marquer les conditions à 1 graine dans le tableau principal\ns=s.replace('''                ad(f\"| `{k}` | {fmt(r['exact_moyen'])} ± {fmt(r['exact_ecart_type'])} | \"''',\n … [1533 caractères tronqués]`

  ```
ok
[aug-pos-last]
  aug-pos-last graine 1 : 194 s, n_aug=4069
  -> /tmp/a5-ablations.json (484 s)
[aug-pos-ctx]
11:54:10
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Fusionne mesures principales + ablations, ajoute verdict et autocritique au JSON.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport pathlib\n\nMAIN = pathlib.Path(\"/tmp/a5-m2-generalisation.json\")\nABL = pathlib.Path(\"/tmp/a5-ablations.jso … [9912 caractères tronqués]`

  ```
<path>/tmp/a5_finalize.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "tail -6 /tmp/a5-ablations.log; date '+%H:%M:%S'; /home/stephane/gpu-env/bin/python -c \"\nimport json; j=json.load(open('/tmp/a5-ablations.json')); print(list(j['conditions']))\"", "description": "Check ctx ablation status"}`

  ```
aug-pos-last graine 1 : 194 s, n_aug=4069
  -> /tmp/a5-ablations.json (484 s)
[aug-pos-ctx]
  aug-pos-ctx graine 1 : 438 s, n_aug=4069
  -> /tmp/a5-ablations.json (977 s)
[aug-pos-norm]
11:55:13
['aug-pos-mean', 'aug-pos-last', 'aug-pos-ctx']
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nj=json.load(open('/tmp/a5-ablations.json'))\nfor k,c in j['conditions'].items():\n    print(k, c['contexte'])\n    for f in ('de','vers','point','chemin_0'):\n        r=c['resultats']['fields'] … [412 caractères tronqués]`

  ```
aug-pos-mean False
  de exact 0.918 | inedit 0.400 cov 0.385 new 0.429 | action 0.952
  vers exact 0.500 | inedit 0.400 cov 0.462 new 0.286 | action 0.952
  point exact 0.057 | inedit 0.000 cov 0.000 new — | action 0.986
  chemin_0 exact 0.900 | inedit 0.571 cov 0.615 new 0.000 | action 0.886
aug-pos-last False
  de exact 0.945 | inedit 0.600 cov 0.692 new 0.429 | action 0.938
  vers exact 0.966 | inedit 0.750 cov 0.923 new 0.429 | action 0.938
  point exact 0.971 | inedit 0.500 cov 0.500 new — | action 0.971
  chemin_0 exact 0.857 | inedit 0.429 cov 0.462 new 0.000 | action 0.914
aug-pos-ctx True
  de exact 0.952 | inedit 0.650 cov 1.000 new 0.000 | action 0.986
  vers exact 0.945 | inedit 0.600 cov 0.846 new 0.143 | action 0.986
  point exact 0.957 | inedit 0.250 cov 0.250 new — | action 1.000
  chemin_0 exact 0.929 | inedit 0.643 cov 0.615 new 1.000 | action 0.900
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a5_finalize.py')\ns=p.read_text(encoding='utf-8')\nold='''    # les compteurs surfaces_syn / surfaces_train sont dans j[\"conditions\"][k][\"masques\"]\n    for k, c in j[\"conditions\"].items():\n        garde[k] = {}\n … [1985 caractères tronqués]`

  ```
ok
  aug-pos-ctx graine 1 : 438 s, n_aug=4069
  -> /tmp/a5-ablations.json (977 s)
[aug-pos-norm]
  aug-pos-norm graine 1 : 65 s, n_aug=3172
  -> /tmp/a5-ablations.json (1052 s)
11:55:47
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import items_synth\nfrom semantique.normalisation import normaliser\nfrom cerveau.voies import normaliser_coordonnees\nj= … [978 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ModuleNotFoundError: No module named 'semantique'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import items_synth\nfrom cerveau.voies import normaliser_coordonnees\nj=json.load(open('/tmp/a5-ablation … [921 caractères tronqués]`

  ```
norm agressif
de exact 0.918 | vu n 128 exact 1.000 | ineditA3 n 18 0.333 | cov 0.273 new 0.429
vers exact 0.952 | vu n 128 exact 1.000 | ineditA3 n 18 0.611 | cov 0.818 new 0.286
point exact 0.971 | vu n 66 exact 1.000 | ineditA3 n 4 0.500 | cov 0.500 new —
chemin_0 exact 0.843 | vu n 56 exact 1.000 | ineditA3 n 14 0.214 | cov 0.154 new 1.000
de recouvrement agressif 128 / 146
vers recouvrement agressif 128 / 146
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python /tmp/a5_finalize.py && /home/stephane/gpu-env/bin/python /tmp/a5_md.py && echo \"---\" && grep -n \"aug-pos-norm\\|aug-pos-ctx\\|aug-pos-mean\\|aug-pos-last\" /tmp/a5-m2-generalisation.md | head -20", "description": " … [47 caractères tronqués]`

  ```
écrit /tmp/a5-m2-generalisation.json (7 conditions)
écrit /tmp/a5-m2-generalisation.md
---
37:| `aug-pos-mean` | 91.8 % ± 0.0 % | 100.0 % | 40.0 % (8.0/20) | 38.5 % (5.0/13) | 42.9 % (3.0/7) | 95.2 % |
38:| `aug-pos-last` | 94.5 % ± 0.0 % | 100.0 % | 60.0 % (12.0/20) | 69.2 % (9.0/13) | 42.9 % (3.0/7) | 93.8 % |
39:| `aug-pos-ctx` | 95.2 % ± 0.0 % | 100.0 % | 65.0 % (13.0/20) | 100.0 % (13.0/13) | 0.0 % (0.0/7) | 98.6 % |
40:| `aug-pos-norm` | 91.8 % ± 0.0 % | 100.0 % | 33.3 % (6.0/18) | 27.3 % (3.0/11) | 42.9 % (3.0/7) | 94.5 % |
49:| `aug-pos-mean` | -6.7 pts | 4/5, p=1 | -33.3 pts | 1/5, p=0.22 |
50:| `aug-pos-last` | +13.3 pts | 5/2, p=0.45 | -2.6 pts | 2/2, p=1 |
51:| `aug-pos-ctx` | +18.3 pts | 4/0, p=0.12 | +28.2 pts | 4/0, p=0.12 |
52:| `aug-pos-norm` | -13.3 pts | 3/6, p=0.51 | -44.5 pts | 0/6, p=0.031 |
56:| famille (inédits A3) | n | `baseline-1000` | `aug-formes` | `aug-pos` | `aug-pos-mean` | `aug-pos-last` | `aug-pos-ctx` | `aug-pos-norm` |
92:| `aug-pos-mean` | 50.0 % ± 0.0 % | 51.6 % | 40.0 % (8.0/20) | 46.2 % (6.0/13) | 28.6 % (2.0/7) | 95.2 % |
93:| `aug-pos-last` | 96.6 % ± 0.0 % | 100.0 % | 75.0 % (15.0/20) | 92.3 % (12.0/13) | 42.9 % (3.0/7) | 93.8 % |
94:| `au
… [839 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a5_md.py')\ns=p.read_text(encoding='utf-8')\n# note en tête de la section 3\ns=s.replace('''    ad(\"## 3. Résultats principaux (1 000 pas, 3 graines, moyenne ± écart-type)\\\\n\")''',\n'''    ad(\"## 3. Résultats princi … [5002 caractères tronqués]`

  ```
ok
| `positions − formes` | `vers` | +11.7 pts | inédit A3, 3 graine(s) |
| `positions − formes` | `point` | +8.3 pts | inédit A3, 3 graine(s) |
| `positions − formes` | `chemin_0` | +0.0 pts | inédit A3, 3 graine(s) |
| `pool mean − mean+last` | `de` | -3.3 pts | inédit A3, 1 graine(s) |
| `pool mean − mean+last` | `vers` | -26.7 pts | inédit A3, 1 graine(s) |
| `pool mean − mean+last` | `point` | -50.0 pts | inédit A3, 1 graine(s) |
| `pool mean − mean+last` | `chemin_0` | +14.3 pts | inédit A3, 1 graine(s) |
| `pool last − mean+last` | `de` | +16.7 pts | inédit A3, 1 graine(s) |
| `pool last − mean+last` | `vers` | +8.3 pts | inédit A3, 1 graine(s) |
| `pool last − mean+last` | `point` | +0.0 pts | inédit A3, 1 graine(s) |
| `pool last − mean+last` | `chemin_0` | -0.0 pts | inédit A3, 1 graine(s) |
| `contexte − sans contexte` | `de` | +21.7 pts | inédit A3, 1 graine(s) |
| `contexte − sans contexte` | `vers` | -6.7 pts | inédit A3, 1 graine(s) |
| `contexte − sans contexte` | `point` | -25.0 pts | inédit A3, 1 graine(s) |
| `contexte − sans contexte` | `chemin_0` | +21.4 pts | inédit A3, 1 graine(s) |
| `normalisation agressive − standard` | `de` | -10.0 pts | inédit A3, 1 grai
… [1197 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a5_md.py')\ns=p.read_text(encoding='utf-8')\nold='''        for f in FIELDS:\n            da = conds[a][\"resultats\"][\"fields\"][f][\"masques\"][\"inedit_a3\"][\"exact_moyen\"]\n            db = conds[b][\"resultats\"] … [1712 caractères tronqués]`

  ```
ok
| comparaison | champ | delta (moyen, même split) | lecture |
|---|---:|---:|---|
| `formes seules − baseline` | `de` | +18.3 pts | inédit A3, 3 graine(s) |
| `formes seules − baseline` | `vers` | -3.3 pts | inédit A3, 3 graine(s) |
| `formes seules − baseline` | `point` | +16.7 pts | inédit A3, 3 graine(s) |
| `formes seules − baseline` | `chemin_0` | +33.3 pts | inédit A3, 3 graine(s) |
| `positions − formes` | `de` | -21.7 pts | inédit A3, 3 graine(s) |
| `positions − formes` | `vers` | +11.7 pts | inédit A3, 3 graine(s) |
| `positions − formes` | `point` | +8.3 pts | inédit A3, 3 graine(s) |
| `positions − formes` | `chemin_0` | +0.0 pts | inédit A3, 3 graine(s) |
| `pool mean − mean+last` | `de` | -10.0 pts | inédit A3, 1 graine(s) |
| `pool mean − mean+last` | `vers` | -25.0 pts | inédit A3, 1 graine(s) |
| `pool mean − mean+last` | `point` | -50.0 pts | inédit A3, 1 graine(s) |
| `pool mean − mean+last` | `chemin_0` | -7.1 pts | inédit A3, 1 graine(s) |
| `pool last − mean+last` | `de` | +10.0 pts | inédit A3, 1 graine(s) |
| `pool last − mean+last` | `vers` | +10.0 pts | inédit A3, 1 graine(s) |
| `pool last − mean+last` | `point` | +0.0 pts | inédit A3, 1 graine(s) |
| 
… [1090 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a5_md.py')\ns=p.read_text(encoding='utf-8')\ns=s.replace('ad(\"| comparaison | champ | delta (moyen, même split) | lecture |\")',\n            'ad(\"| comparaison | champ | delta (apparié sur la graine quand il le faut)  … [1777 caractères tronqués]`

  ```
ok
```
/home/stephane/gpu-env/bin/python /tmp/a5_md.py
```
```
PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest tools.cerveau.tests.test_voies
```

_Fichiers : `/tmp/a5-m2-generalisation.json` (chiffres, masques, prédictions par item), `/tmp/a5-m2-generalisation.md` (ce rapport), `/tmp/a5_driver.py` (dispositif), `/tmp/a5_md.py` (génération du rapport)._
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nj=json.load(open('/tmp/a5-m2-generalisation.json'))\nprint(json.dumps(j['verdict'], ensure_ascii=False, indent=1)[:3000])\nprint('--- garde')\nfor k,v in j['garde_anti_fuite'].items():\n    pri … [181 caractères tronqués]`

  ```
{
 "principe": "Comparaison à pas égal (1000), encodeur gelé, garde anti-fuite (0 surface réelle générée).",
 "champs": {
  "de": {
   "baseline": {
    "exact_inedit": 0.46666666666666673,
    "k_sur_n": [
     9.33,
     20
    ]
   },
   "conditions": {
    "aug-formes": {
     "exact_inedit": 0.65,
     "delta_pts": 18.33333333333333,
     "k_sur_n": [
      13.0,
      20
     ],
     "delta_global_pts": 2.511415525114158
    },
    "aug-pos": {
     "exact_inedit": 0.43333333333333335,
     "delta_pts": -3.3333333333333384,
     "k_sur_n": [
      8.67,
      20
     ],
     "delta_global_pts": -0.45662100456621557
    }
   }
  },
  "vers": {
   "baseline": {
    "exact_inedit": 0.5833333333333334,
    "k_sur_n": [
     11.67,
     20
    ]
   },
   "conditions": {
    "aug-formes": {
     "exact_inedit": 0.55,
     "delta_pts": -3.3333333333333326,
     "k_sur_n": [
      11.0,
      20
     ],
     "delta_global_pts": -0.45662100456621557
    },
    "aug-pos": {
     "exact_inedit": 0.6666666666666666,
     "delta_pts": 8.333333333333325,
     "k_sur_n": [
      13.33,
      20
     ],
     "delta_global_pts": 1.1415525114155223
    }
   }
  },
  "point": {
   "baseline": {
… [2531 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a5_finalize.py')\ns=p.read_text(encoding='utf-8')\n# meta\ns=s.replace('''    j[\"meta\"][\"fichiers\"] = {''','''    j[\"meta\"][\"conditions\"] = list(j[\"conditions\"])\n    j[\"meta\"][\"pas\"] = {k: c[\"pas\"] for k … [5228 caractères tronqués]`

  ```
ok
écrit /tmp/a5-m2-generalisation.json (7 conditions)
['baseline-1000', 'aug-formes', 'aug-pos', 'aug-pos-mean', 'aug-pos-last', 'aug-pos-ctx', 'aug-pos-norm']
Oui pour chemin_0 (+33,3 pts), point (+16,7 à +25 pts) et une partie de de (+18,3 pts avec les templates seuls) ; non pour vers avec les templates seuls (-3,3 pts). Pas de gain uniforme, et le split inédit de A3 sur de/vers est trompeur (3 classes, prior de surface).
Pas de gain uniforme : vers ne gagne pas avec les templates seuls (-3,3 pts) ; aug-pos perd 3,3 pts sur de par rapport à la baseline (8,7/20 contre 9,3/20) ; le roque reste 0/3 (surface unique exclue)
conditions json: ['baseline-1000', 'aug-formes', 'aug-pos', 'aug-pos-mean', 'aug-pos-last', 'aug-pos-ctx', 'aug-pos-norm']
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a5_md.py')\ns=p.read_text(encoding='utf-8')\ns=s.replace('''          \"/\".join(str(meta[\"pas\"].get(k)) for k in keys)))''',\n'''          \"/\".join(sorted({str(v) for v in meta[\"pas\"].values()}))))''')\np.write_te … [344 caractères tronqués]`

  ```
ok
écrit /tmp/a5-m2-generalisation.md
# A5 — M2 : généraliser aux surfaces inédites par les règles

_Sprint autonome 24 h — sous-agent A5. Encodeur `/tmp/natif-600-512-8-align-s1` gelé, GPU Quadro RTX 5000, `PYTHONPATH=tools`, `CUDA_VISIBLE_DEVICES=0`, 3 graines, 1000 pas._

**Question.** A3 a mesuré M2 sur 20 surfaces réelles inédites par champ (`de`, `vers`) : 10,7/20 et 11,7/20. Peut-on améliorer ce split par une **augmentation synthétique par les règles**, sans jamais montrer une surface réelle à l'entraînement ?

## 1. Ce qui est mesuré

...
```
```
/home/stephane/gpu-env/bin/python /tmp/a5_finalize.py
```
```
/home/stephane/gpu-env/bin/python /tmp/a5_md.py
```
```
PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest tools.cerveau.tests.test_voies
```

_Fichiers : `/tmp/a5-m2-generalisation.json` (chiffres, masques, prédictions par item), `/tmp/a5-m2-generalisation.md` (ce rapport), `/tmp/a5_driver.py` (dispositif), `/tmp/a5_md.py` (génération du rapport)._
-rw-r--r--. 1 stephane stephane 986258 27 oct 11:58 /tmp/a5-m2-generalisation.json
-rw-r--r--. 1 stephane stephane  23810 27 oct 11:58 /tmp/a5-m2-generalisation.md
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest tools.cerveau.tests.test_voies -v 2>&1 | tail -12 && /home/stephane/gpu-env/bin/python -m py_compile tools/cerveau/voies.py tools/cerveau/tests/test_voies.py && echo COMPILE_OK", "descript … [42 caractères tronqués]`

  ```
test_contexte_melange_et_vide (tools.cerveau.tests.test_voies.TestVoies.test_contexte_melange_et_vide) ... ok
test_entrainement_avec_augmentation_et_normalisation (tools.cerveau.tests.test_voies.TestVoies.test_entrainement_avec_augmentation_et_normalisation) ... ok
test_entrainement_court (tools.cerveau.tests.test_voies.TestVoies.test_entrainement_court) ... ok
test_evaluation_et_lesions (tools.cerveau.tests.test_voies.TestVoies.test_evaluation_et_lesions) ... ok
test_formes_des_tetes (tools.cerveau.tests.test_voies.TestVoies.test_formes_des_tetes) ... ok
test_le_contexte_change_le_code (tools.cerveau.tests.test_voies.TestVoies.test_le_contexte_change_le_code) ... ok
test_pools (tools.cerveau.tests.test_voies.TestVoies.test_pools) ... ok

----------------------------------------------------------------------
Ran 8 tests in 3.249s

OK
COMPILE_OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git diff --stat -- tools/cerveau/voies.py tools/cerveau/tests/test_voies.py && git status --short -- tools/cerveau/voies.py tools/cerveau/tests/test_voies.py", "description": "Verify only two target files changed by A5"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -c \"def augmenter\" tools/cerveau/voies.py; grep -c \"test_augmentation\" tools/cerveau/tests/test_voies.py; git status --short | head; git log --oneline -3", "description": "Check files and git state after no diff"}`

  ```
1
1
 M docs/README.md
M  docs/carte.md
M  docs/en-cours.md
M  docs/roadmap.md
MM journal/2026-10-27.md
MM journal/2026-10-27_portes.md
M  journal/2026-10-27_sprint-24h.md
MM journal/README.md
M  reports/README.md
A  reports/pipeline-semantique.json
ba3552b9 DOCS — MDSERVE : 64 TESTS
47fc2151 DOCS — CONTEXTE IA : BUDGETS ET MANIFESTE, CHAPITRE 5 SCINDÉ, INDEX RÉDUIT (175/242/53, T0 3 561 MOTS)
8541dfe7 DOCS — MDSERVE : 60 TESTS (ET NON 59)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sha256sum tools/cerveau/voies.py tools/cerveau/tests/test_voies.py; /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nj=json.load(open('/tmp/a5-m2-generalisation.json'))\nprint('sha meta:', j['meta']['sha256_voies'])\nprint('conditions:', list … [310 caractères tronqués]`

  ```
03eba1ed3aa1cd0269c1003b456f7a2366d2483b7ae78721c1ef1513a79490b7  tools/cerveau/voies.py
95394ac504ac84cc28c8d94837618eeb5fd92e5f0fdfc13262ae1670ab2cdaf1  tools/cerveau/tests/test_voies.py
sha meta: 03eba1ed3aa1cd0269c1003b456f7a2366d2483b7ae78721c1ef1513a79490b7
conditions: ['baseline-1000', 'aug-formes', 'aug-pos', 'aug-pos-mean', 'aug-pos-last', 'aug-pos-ctx', 'aug-pos-norm']
verdict keys: ['principe', 'champs', 'lecture', 'negatif', 'promotion_lue_par_la_regle', 'resume_court', 'controle_negatif', 'chiffres']
autocritique: 9 items
garde toutes vraies: True
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a5_md.py')\ns=p.read_text(encoding='utf-8')\ns=s.replace('ad(\"| condition | exact | vu | inédit A3 | inédit couvert A3 | nouvelle classe | action |\")',\n            'ad(\"| condition | exact | vu (n) | inédit A3 | inéd … [771 caractères tronqués]`

  ```
ok
### `de`

| condition | exact | vu (n) | inédit A3 | inédit couvert A3 | nouvelle classe | action |
|---|---:|---:|---:|---:|---:|---:|
| `baseline-1000` | 92.7 % ± 1.0 % | 100.0 % (126/146) | 46.7 % (9.3/20) | 71.8 % (9.3/13) | — (—) | 91.6 % |
| `aug-formes` | 95.2 % ± 0.0 % | 100.0 % (126/146) | 65.0 % (13.0/20) | 100.0 % (13.0/13) | — (—) | 92.9 % |
| `aug-pos` | 92.2 % ± 1.0 % | 100.0 % (126/146) | 43.3 % (8.7/20) | 46.2 % (6.0/13) | 38.1 % (2.7/7) | 95.9 % |
| `aug-pos-mean` | 91.8 % ± 0.0 % | 100.0 % (126/146) | 40.0 % (8.0/20) | 38.5 % (5.0/13) | 42.9 % (3.0/7) | 95.2 % |
| `aug-pos-last` | 94.5 % ± 0.0 % | 100.0 % (126/146) | 60.0 % (12.0/20) | 69.2 % (9.0/13) | 42.9 % (3.0/7) | 93.8 % |
| `aug-pos-ctx` | 95.2 % ± 0.0 % | 100.0 % (126/146) | 65.0 % (13.0/20) | 100.0 % (13.0/13) | 0.0 % (0.0/7) | 98.6 % |
| `aug-pos-norm` | 91.8 % ± 0.0 % | 100.0 % (128/146) | 33.3 % (6.0/18) | 27.3 % (3.0/11) | 42.9 % (3.0/7) | 94.5 % |
`*` : 1 graine (exploratoire).
| champ | n | inédits A3 | dont classe couverte A3 | codes des inédits A3 (occurrences) | plafond |
|---|---:|---:|---:|---|---:|
| `de` | 146 | 20 | 13 | {52: 6, 62: 6, 60: 4, 28: 1, 8: 2, 57: 1} | 65.0 % |
| `vers` | 146 
… [655 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && grep -n \"plafond\" a5_md.py | head; python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('/tmp/a5_md.py')\ns=p.read_text(encoding='utf-8')\ns=s.replace('| codes des inédits A3 (occurrences) | plafond |',\n            '| codes des inédits A3 (occurrences) | plafond de couverture … [1492 caractères tronqués]`

  ```
94:    ad("| champ | n | inédits A3 | dont classe couverte A3 | codes des inédits A3 (occurrences) | plafond |")
104:        plafond = n_cov / n if n else None
106:           f"{dict(classes)} | {fmt(plafond)} |")
299:       "`9x18x27`. Le prétendu « plafond 13/20 » de A3 n'est donc pas un plafond : "
ok
19:| champ | n | inédits A3 | dont classe couverte A3 | codes des inédits A3 (occurrences) | plafond de couverture A3 |
277:**Ce qui est réellement appris par les règles** : les promotions (`a8=Q`/`a7a8q`, 0/3 → 3/3 des deux côtés), les formes numériques de dames (`9x18`, `9-13`, `9-14`), l'algébrique `b6xd4`/`b6-c5`, `pierre noire en D4`, et partiellement la prise SAN `exd6`. Restent non lisibles sans contexte : le **roque** (4 items, surface `O-O` unique et exclue) et le début de `9x18x27`. Le prétendu « plafond 13/20 » de A3 n'est donc pas un plafond : la règle de promotion rend 2 items de plus lisibles, même surface exclue.
26:**Conséquence.** Sur `de`, les 13 inédits couverts ne portent que 3 classes (52=e2e4, 62=g1f3, 57=nc3) : deviner la classe majoritaire de la famille de surface suffit déjà à ~12/13. Le 10,7/20 de A3 n'est donc **pas** une mesure de lecture ; le gain maxim
… [301 caractères tronqués]
  ```

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "A5 — TERMINÉ. Fichiers écrits :\n- `/tmp/a5-m2-generalisation.json` (7 conditions, masques par graine, prédictions par item, verdict, autocritique, garde anti-fuite)\n- `/tmp/a5-m2-generalisation.md` (rapport)\n- dispositif : `/tmp/a5_ … [3048 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

- **bash** `{"command": "ps aux | grep -E \"a5_driver|a5_finalize\" | grep -v grep | wc -l; ls -l /tmp/a5-m2-generalisation.json /tmp/a5-m2-generalisation.md; cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest tools.cerveau.tests.test_voies 2>&1 | tail -2", "descr … [52 caractères tronqués]`

  ```
0
-rw-r--r--. 1 stephane stephane 986258 27 oct 11:58 /tmp/a5-m2-generalisation.json
-rw-r--r--. 1 stephane stephane  24107 27 oct 12:00 /tmp/a5-m2-generalisation.md

OK
  ```

### 🤖 Assistant

⏵ Clôture d'A5 : résultats, autocritique et fichiers livrés

**Livrables**
- `/tmp/a5-m2-generalisation.json` — 7 conditions, masques par graine, prédictions par item, verdict, autocritique, garde anti-fuite.
- `/tmp/a5-m2-generalisation.md` — rapport complet.
- Dispositif : `/tmp/a5_driver.py`, `/tmp/a5_finalize.py`, `/tmp/a5_md.py` ; logs `/tmp/a5-main.log`, `/tmp/a5-ablations.log`.

**Code (uniquement les 2 fichiers autorisés)**
`tools/cerveau/voies.py` et `tools/cerveau/tests/test_voies.py` : `augmenter()` (templates UCI/SAN français/NLP, dames numérique-algébrique, go SGF/français, positions variées), `normaliser_coordonnees()`, paramètres `augmentation/positions/exclure_surfaces/normaliseur`, mémoïsation de `normaliser`. Rétro-compatible ; tests `test_voies` **8/8 OK**, `py_compile` OK. Aucun git de ma part.

**Résultats (1 000 pas, 3 graines, split inédit A3 gelé)**

| champ | baseline | aug-formes | aug-pos |
|---|---:|---:|---:|
| `de` | 9,3/20 | **13/20 (+18,3 pts)** | 8,7/20 (−3,3) |
| `vers` | 11,7/20 | 11/20 (−3,3) | **13,3/20 (+8,3)** |
| `point` | 1/4 | 1,7/4 (+16,7) | **2/4 (+25,0)** |
| `chemin_0` | 1,3/14 | **6/14 (+33,3)** | 6/14 (+33,3) |

La garde anti-fuite tient : `surfaces_train == surfaces_syn` partout, **0 surface réelle générée**, `vu` identique dans toutes les conditions.

**Verdict autocritique**
- Gain réel sur `chemin_0`, `point` et une partie de `de` ; **pas de gain uniforme** (`vers` négatif avec les templates seuls).
- Le split `de`/`vers` de A3 est trompeur : 13 inédits couverts, 3 classes, un prior par famille suffit à ~12/13. `aug-pos` **désapprend** les raccourcis `e4→52`/`Nf3→62` et baisse, tout en lisant par la règle les promotions `a8=Q`/`a7a8q` (0/3 → 3/3 des deux côtés) et `exd6` (2/3 sur `de`).
- Ablations 1 graine : mean s'effondre (`vers` 40 %, `point` 0 %) ; last meilleur sur `vers` (75 %) ; contexte +15 pts sur `de` mais −25 sur `point` ; normalisation agressive = négatif net (split 18/20, résidu `de` 33,3 %, `chemin` 21,4 %).
- Limites : roque 0/3 (surface unique exclue), `9x18x27` 0, McNemar pseudo-répliqué, pas de label-shuffle. L'échec `test_m8_sommeil` de la suite complète vient d'un autre agent (`sommeil.py`/`lesion.py`), pas de M2.

