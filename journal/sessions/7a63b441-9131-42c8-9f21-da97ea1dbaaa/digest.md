# Session DSH — relecture

- identifiant : `7a63b441-9131-42c8-9f21-da97ea1dbaaa`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 12:03:43
- agent : standard


## Tour 1

### 👤 Utilisateur

Dépôt /home/stephane/GitHub/Qtrinet, sprint autonome 24 h. Sous-agent A9 : brancher **M2** (voies ventrales/dorsales) dans la chaîne B13 et mesurer le bout en bout, sans modifier les modules existants.

État :
- `tools/cerveau/pipeline_semantique.py` : B13 M1→M5→M6→M8, M1 528/528, M5 contexte 18,7 % vs 12,6 %, M6 94,3 %, M8 57,95 % (borne haute).
- `tools/cerveau/voies.py` : M2 `Voies` + `entrainer`/`evaluer`/`evaluer_champs`, augmentation `augmenter`, pools mean/last/mean+last, têtes `de`/`vers`/`point`/`chemin_0`.
- Base `/tmp/natif-600-512-8-align-s1`, GPU `CUDA_VISIBLE_DEVICES=0`, `/home/stephane/gpu-env/bin/python`.
- Corpus : `semantique.typed_corpus.items()`, `semantique.synth_corpus.items_synth()`, `cerveau.sequences.corpus`.
- Tests : `PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest discover -s tools/cerveau/tests -t tools` → 86 OK (8 skip sans torch).

Objectif :
1. Créer `tools/cerveau/pipeline_semantique_m2.py` : `percevoir` M1 → `coder_voies` M2 (`de`/`vers`) → `predire` M5 contexte → `selectionner` M6 ; M9 lésions M1/M2/M5.
2. Entraîner M2 (300 pas, 1–3 graines) et mesurer `de`/`vers` sur les 146 items réels : exact, vu/inédit ; comparer au M2 seul (A3/A5).
3. Mesurer la chaîne **bout en bout** : code M1 exact, champ M2 exact, prédiction M5 exacte/surprise, sélection M6 ; contrôle négatif (M2 sans contexte, M5 sans plateau, M1 sans contexte).
4. Écrire `/tmp/a9-pipeline-m2.json` et `.md` avec chiffres, commandes, limites. Si M2 n'ajoute rien à la chaîne, le dire.

Contraintes :
- Crée uniquement `tools/cerveau/pipeline_semantique_m2.py` et `tools/cerveau/tests/test_pipeline_semantique_m2.py` ; ne modifie pas les modules existants, docs, reports, journal, `batterie.py`, git.
- Pas de `git add/commit/checkout`.
- GPU `CUDA_VISIBLE_DEVICES=0`. Sois autonome, timebox, autocritique. Réponds avec un résumé et les chemins.
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

⏵ Lecture de l'état du dépôt et des modules B13/M2

- **bash** `{"command": "ls -la && echo \"---\" && ls tools/cerveau/ && echo \"---\" && ls tools/cerveau/tests/", "description": "List repo root and cerveau modules"}`

  ```
total 192
drwxr-xr-x. 1 stephane stephane   630 27 oct 09:29 .
drwxr-xr-x. 1 stephane stephane  2478 27 oct 11:39 ..
-rw-r--r--. 1 stephane stephane  8041 27 oct 11:52 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  1056 26 oct 11:22 data
drwxr-xr-x. 1 stephane stephane   928 27 oct 11:55 docs
drwxr-xr-x. 1 stephane stephane    82 28 sep 11:58 drave-core
drwxr-xr-x. 1 stephane stephane   164 27 oct 12:03 .git
-rw-r--r--. 1 stephane stephane   399 30 sep 10:01 .gitignore
drwxr-xr-x. 1 stephane stephane  6690 27 oct 11:54 journal
drwxr-xr-x. 1 stephane stephane   100 15 oct 09:02 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-------. 1 stephane stephane 19300 27 oct 11:51 README.md
drwxr-xr-x. 1 stephane stephane 20762 27 oct 11:58 reports
-rw-------. 1 stephane stephane 12170 27 oct 11:52 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane 10507 30 sep 08:44 run_clusters.py
-rw-------. 1 stephane stephane 12507 30 
… [1198 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && wc -l tools/cerveau/pipeline_semantique.py tools/cerveau/voies.py tools/cerveau/semantique.py tools/cerveau/sequences.py 2>/dev/null; git status --short | head -20", "description": "Check file sizes and git status"}`

  ```
125 tools/cerveau/pipeline_semantique.py
  737 tools/cerveau/voies.py
  114 tools/cerveau/sequences.py
  976 total
 M docs/README.md
  ```

### 🤖 Assistant

⏵ Localisation du module sémantique et lecture du pipeline B13

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && find tools -name \"semantique*\" -o -name \"*semantique*\" | head -20 && echo \"---\" && cat tools/cerveau/pipeline_semantique.py", "description": "Find semantique module and read pipeline"}`

  ```
tools/invariance_semantique.py
tools/premiere_couche_semantique.py
tools/semantique
tools/cerveau/tests/__pycache__/test_pipeline_semantique.cpython-313.pyc
tools/cerveau/tests/test_pipeline_semantique.py
tools/cerveau/__pycache__/pipeline_semantique.cpython-313.pyc
tools/cerveau/pipeline_semantique.py
---
#!/usr/bin/env python3
"""pipeline_semantique.py — B13 : la chaîne M1 → M5 → M6 → M8.

Ce n'est pas un nouveau module : c'est un **test d'intégration** des briques
corrigées, sur un seul flux. M1 lit le code, M5 prédit avec le plateau, M6
sélectionne la tâche, M8 consolide. M2 n'est pas inclus (il demande un
entraînement GPU séparé) ; M9 lèse M1/M5.

La chaîne ne prétend pas faire mieux que M1 seul : elle vérifie que les blocs
se parlent et que chaque mesure reste celle de son module.
"""
from __future__ import annotations

import collections
import json
import random
from pathlib import Path

from .bus import Bus
from .episodique import Episodique
from .gating import Porte
from .hub import Hub
from .predictif import Predictif
from .sequences import corpus
from .sommeil import Sommeil


class PipelineSemantique:
    nom = "B13-pipeline-semantique"

    def __init__(self) -> None:
… [3460 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat tools/cerveau/tests/test_pipeline_semantique.py && echo \"=== SEQUENCES ===\" && cat tools/cerveau/sequences.py", "description": "Read existing pipeline tests and sequences"}`

  ```
from __future__ import annotations
import unittest
from cerveau.pipeline_semantique import PipelineSemantique
from jeux.regles import echecs as E


class TestPipelineSemantique(unittest.TestCase):
    def test_m1_m5_m6_m8(self):
        p = PipelineSemantique()
        ctx = E.rsn_depuis_position(E.Position.depart())
        code = p.percevoir("Nf3", "echecs", ctx)
        self.assertEqual(code["de"], 62)
        r = p.selectionner()
        self.assertIn("exact", r)
        self.assertEqual(len(p.memoire.episodes), 1)
        p.consolider()
        self.assertTrue(p.sommeil.nom)


if __name__ == "__main__":
    unittest.main()
=== SEQUENCES ===
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
from semantique.universaux i
… [2899 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de `voies.py` (M2) et du corpus typé

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,260p tools/cerveau/voies.py", "description": "Read voies.py part 1"}`

  ```
#!/usr/bin/env python3
"""M2 — deux voies : ventrale (quoi) et dorsale (où/comment).

Un même encodeur de surface, **gelé**, alimente deux familles de têtes :

- la voie **ventrale** lit l'**action** ;
- la voie **dorsale** lit un ou plusieurs champs de lieu : `de`, `vers`,
  `point`, `chemin_0`…

Chaque tête est indépendante : on peut en léser une (logits aléatoires) sans
toucher les autres. C'est la double dissociation minimale, étendue à plusieurs
champs dorsaux.

L'entraînement est **synthétique** (`items_synth`) ; l'évaluation porte sur les
surfaces **réelles** (`items`). Le module expose aussi les ablations :

- `pool="mean"` : moyenne seule (ablation du dernier état) ;
- `pool="last"` : dernier état seul ;
- `contexte=True` : ajout du RSN de contexte, encodé par le même encodeur gelé.

Les surfaces et le contexte sont normalisés (`normaliser`) puis lus en octets,
comme dans le prototype d'origine. L'API `entrainer`/`evaluer` reste compatible
avec `batterie.py` quand aucun champ dorsal supplémentaire n'est demandé.

## Généralisation aux surfaces inédites (A5)

Deux leviers sont ajoutés, tous deux **désactivés par défaut** :

- `augmentation_*` (voir `augmenter`) : le corpus 
… [9389 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls tools/semantique/ && wc -l tools/semantique/*.py", "description": "List semantique modules"}`

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

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 260,520p tools/cerveau/voies.py", "description": "Read voies.py part 2"}`

  ```
prise = pos.plateau[coup.vers] != 0 or coup.drapeau == E.EP
    sortie = [
        (f"{c0}{c1}", "uci", "notation"),
        (f"{c0} {c1}", "uci-espace", "notation"),
        (f"{c0}-{c1}", "uci-tiret", "notation"),
        (f"{lettre} {c0} {c1}", "piece-espace", "notation"),
        (f"{lettre} {c0}-{c1}", "piece-tiret", "notation"),
    ]
    if prise:
        sortie += [(f"{c0}x{c1}", "prise", "notation"),
                   (f"{lettre}x{c1}", "prise-piece", "notation")]
    san = pos.san(coup)
    sortie.append((san, "san", "notation"))
    if san.endswith(("+", "#")):
        sortie.append((san[:-1], "san", "notation"))
    fr = _san_francais(san.rstrip("+#"))
    if fr != san:
        sortie.append((fr, "san-fr", "notation"))
    if coup.promotion:
        pl = "NBRQ"[coup.promotion - E.CAVALIER]
        sortie += [(f"{c0}{c1}{pl.lower()}", "promo-uci", "notation"),
                   (f"{c1}={pl}", "promo-eq", "notation"),
                   (f"{c0}-{c1}={pl}", "promo-long", "notation")]
    for langue in ("fr", "en"):
        formes = MULTI.formes(f"echecs.piece.{lettre}", langue)
        if not formes:
            continue
        p = formes[0]
        if langue == "fr":
 
… [9947 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat tools/semantique/typed_corpus.py && echo \"=== SYNTH ===\" && cat tools/semantique/synth_corpus.py", "description": "Read typed and synth corpora"}`

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
   
… [6625 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la suite de `voies.py` (entraînement/évaluation)

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 520,737p tools/cerveau/voies.py", "description": "Read voies.py part 3"}`

  ```
choix_total = choix_action + [i for nom in champs for i in choix_par[nom]]
            ctx = ([i.contexte for i in choix_total] if contexte else None)
            x, masque, c, cm = _entrees(choix_total, seq, seq_ctx, contexte, ctx, norm)
            va, vd = m.logits(
                x.to(device), masque.to(device),
                c.to(device) if c is not None else None,
                cm.to(device) if cm is not None else None,
            )
            # La voie ventrale voit tout le lot composite (tous les blocs ont
            # une action) : plus d'exemples par pas, sans toucher aux têtes
            # dorsales, qui ne reçoivent leur perte que sur leur bloc.
            perte = F.cross_entropy(
                va, _cibles(choix_total, "action", idx_action, device))
            debut = lot
            for nom in champs:
                fin = debut + lot
                perte = perte + F.cross_entropy(
                    vd[nom][debut:fin],
                    _cibles(choix_par[nom], nom, m._idx[nom], device))
                debut = fin
        opt.zero_grad()
        perte.backward()
        opt.step()
    return m, val


def _stats_classes(pred, cible, n_classes_tete: int)
… [8514 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat tools/cerveau/tests/test_voies.py && echo \"=== UNIVERSAUX ===\" && cat tools/semantique/universaux.py", "description": "Read voies tests and universaux"}`

  ```
from __future__ import annotations

import unittest
from types import SimpleNamespace

try:
    import torch
    import torch.nn as nn
    _TORCH = True
except ImportError:
    torch = None
    nn = None
    _TORCH = False

if _TORCH:
    from cerveau.voies import (
        Voies, augmenter, entrainer, evaluer, evaluer_champs,
        normaliser_coordonnees,
    )
from semantique.normalisation import normaliser
from semantique.typed_corpus import ItemType


if _TORCH:
    class _Base(nn.Module):
        """Encodeur minimal : assez pour tester les formes, pas pour apprendre."""

        def __init__(self, d: int = 16, vocab: int = 256):
            super().__init__()
            self.config = SimpleNamespace(hidden_size=d)
            self.emb = nn.Embedding(vocab, d)

        def forward(self, input_ids, attention_mask, output_hidden_states=True):
            h = self.emb(input_ids)
            return SimpleNamespace(hidden_states=[h, h])
else:
    _Base = object


def _items():
    base = {"jeu": "echecs", "action": "deplacer", "de": None, "vers": None,
            "point": None, "chemin_0": None}
    return [
        ItemType("e2e4", {**base, "de": 52, "vers": 36}, "echecs", "cou
… [12868 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des résultats M2 existants (A3/A5) et des interfaces M1/M5/M6/M9

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rl \"voies\\|M2\" reports/ journal/ 2>/dev/null | head -20 && echo \"---\" && ls reports/ | tail -40", "description": "Find M2 reports"}`

  ```
reports/rapport-minimal.md
reports/rapport-eparsite.md
reports/rapport-precision.md
reports/rapport-encodage.md
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
reports/cerveau-mesures.json
reports/README.md
reports/rapport-cerveau-corrections.md
reports/cerveau-mesures-corrigees.json
reports/rapport-pipeline-semantique.md
---
traduction-eurlex-7b-fraeng.json
traduction-eurlex-7b.json
traduction-jw-A.json
traduction-jw-B.json
traduction-langues-3b.json
traduction-langues-7b.json
traduction-legal-0.5b-6.json
traduction-legal-1.5b.json
traduction-legal-3b.json
traduction-legal-7b.json
traduction-legal.json
traduction-litteraire-3b.json
traduction-litteraire-7b.json
traduction-onu-3b.json
traduction-onu6-3b.json
traduction-onu6-7b.json
traduction-onu-7b.json
traduction-pidgin-14b.json
traduction-pidgin-7b.json
tr
… [451 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,140p tools/cerveau/hub.py && echo \"=== PREDICTIF ===\" && sed -n 1,120p tools/cerveau/predictif.py && echo \"=== GATING ===\" && sed -n 1,100p tools/cerveau/gating.py && echo \"=== LESION ===\" && sed -n 1,80p tools/cerveau/lesion.py", "desc … [40 caractères tronqués]`

  ```
#!/usr/bin/env python3
"""M1 — hub sémantique typé : surface → code RSN, et retour canonique.

Le hub est la **zone de convergence** du système : il ne produit pas un vecteur
libre, il produit le code fixe de `universaux.py` (15 champs, 502 classes) en
s'appuyant sur le codec classique. Chaque perception et chaque restitution est
publiée sur le bus.
"""
from __future__ import annotations

from jeux.codecs import codec
from semantique.universaux import code_rsn, rsn_depuis_code
from .bus import Bus

FORMATS = {"morpion": "cellule", "echecs": "san", "dames": "numerique",
           "go": "gtp", "cartes": "carte"}


class Hub:
    nom = "M1-hub"

    def __init__(self, bus: Bus | None = None) -> None:
        self.bus = bus or Bus()
        self.dernier = None

    def percevoir(self, texte: str, jeu: str, contexte=None):
        try:
            lec = codec(jeu).lit(texte, niveau=4, contexte=contexte)
        except Exception as e:
            self.bus.publier("echec", {"texte": texte, "erreur": type(e).__name__}, self.nom)
            return None
        if not (lec and lec.rsn):
            self.bus.publier("echec", {"texte": texte, "erreur": "pas de RSN"}, self.nom)
            re
… [13024 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection des résultats A3/A5 et de l'encodeur de base

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls /tmp/*.json /tmp/*.md 2>/dev/null | head -40 && echo \"---REPORTS M2---\" && ls reports/ | grep -i \"voies\\|m2\\|A3\\|A5\" && echo \"---\" && grep -rn \"voies\\|mean+last\" reports/rapport-pipeline-semantique.md | head", "description": "List tmp r … [23 caractères tronqués]`

  ```
/tmp/a1-m5-m6.json
/tmp/a1-m5-m6.md
/tmp/a2-m2-cpu.json
/tmp/a2-m7-m8-m9.json
/tmp/a2-m7-m8-m9.md
/tmp/a2-m7-m8-m9-part1.md
/tmp/a2-m7-m8-m9-part2.md
/tmp/a2-m7-m8-m9-part3.md
/tmp/a3-m2.json
/tmp/a3-m2.md
/tmp/a3-m2-partial.json
/tmp/a4-m3-m4.json
/tmp/a4-m3-m4.md
/tmp/a5-ablations.json
/tmp/a5-m2-generalisation.json
/tmp/a5-m2-generalisation.md
/tmp/a5-quick.json
/tmp/a6-m5-m6.json
/tmp/a6-m5-m6.md
/tmp/a7-m8-m9.json
/tmp/a7-m8-m9.md
/tmp/cerveau-mesures.json
/tmp/hybride.json
/tmp/jeux-mesures.json
/tmp/langues.json
/tmp/langues-mesures.json
/tmp/lexique_wikidata_raw.json
/tmp/maitres-mesures.json
/tmp/restitution.json
/tmp/semantique-100.json
/tmp/semantique-300.json
/tmp/semantique-diag-corr.json
/tmp/semantique-diag.json
/tmp/semantique-nvlink-10d.json
/tmp/semantique-nvlink-20b.json
/tmp/semantique-nvlink-A512.json
/tmp/semantique-nvlink-A64.json
/tmp/semantique-nvlink-A.json
/tmp/semantique-nvlink-B2.json
/tmp/semantique-nvlink-B.json
---REPORTS M2---
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls -la /tmp/natif-600-512-8-align-s1 2>/dev/null | head -20 && echo \"---\" && cat tools/semantique/modele.py", "description": "Inspect base model and modele.py"}`

  ```
total 123596
drwxr-xr-x.   2 stephane stephane       100 26 oct 16:04 .
drwxrwxrwt. 735 root     root         22100 27 oct 12:04 ..
-rw-r--r--.   1 stephane stephane       974 26 oct 16:04 config.json
-rw-r--r--.   1 stephane stephane       153 26 oct 16:04 generation_config.json
-rw-------.   1 stephane stephane 126553768 26 oct 16:04 model.safetensors
---
#!/usr/bin/env python3
"""modele.py — l'encodeur sémantique et le décodeur sens→texte du natif.

Le même `route` fait les deux :
- **encodeur** : il lit la surface (octets), et l'état caché du dernier octet est
  projeté en un vecteur `z` de dimension `d_sem`, normalisé ;
- **décodeur** : `z` devient `k` préfixes doux, plus un jeton de **langue cible**,
  et le même `route` génère la texte cible. La langue est dans le décodeur, pas
  dans `z` : c'est la condition pour que `z` soit un sens partagé.

Le protocole n'ajoute donc ni un second modèle ni un tokeniseur : il ajoute une
tête, un préfixe et une table de langues au modèle natif.
"""
from __future__ import annotations

import copy

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModelForCausalLM


class RetourInverse(torch.auto
… [6248 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des rapports A3/A5 pour les chiffres de référence

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat /tmp/a3-m2.md && echo \"=== A5 ===\" && cat /tmp/a5-m2-generalisation.md", "description": "Read A3 and A5 M2 reports"}`

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
… [35140 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat tools/semantique/entrainer_type.py | sed -n 1,160p", "description": "Read M2 training script"}`

  ```
#!/usr/bin/env python3
"""entrainer_type.py — le modèle natif sur une base fixe d'universaux.

La sortie n'est plus un vecteur libre : c'est un **code typé** de 15 champs fixes
(jeu, action, source, cible, promotion, roque, case, symbole, carte, taille,
point, passe, chemin 0..2). Chaque champ a un vocabulaire fixe ; l'embedding est
le one-hot concaténé, et la lecture est un `argmax` — donc **déterministe**.

Le décodeur n'est pas neuronal : c'est le **codec classique** du jeu, qui rend la
RSN en surface. C'est l'hybride demandé : un bloc neuronal pour lire la surface,
un bloc classique pour rendre le sens.
"""
from __future__ import annotations

import argparse
import collections
import dataclasses
import hashlib
import json
import pathlib
import random
import sys
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModelForCausalLM

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from jeux.codecs import codec  # noqa: E402
from semantique.entrainer import pad  # noqa: E402
from semantique.typed_corpus import decouper, items, lot, lot_par_paire  # noqa: E402
from semantique.normalisation import normaliser
… [5561 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du rapport B13, de M5 (plateau) et de M6 pour câbler la chaîne

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat reports/rapport-pipeline-semantique.md | head -120 && echo \"=== A6 ===\" && cat /tmp/a6-m5-m6.md | head -150", "description": "Read B13 report and A6 M5/M6 results"}`

  ```
# B13 — chaîne sémantique M1 → M5 → M6 → M8

> **Objet.** Vérifier que les briques corrigées se **parlent** sur un seul flux. Ce n'est pas un
> nouveau module et ce n'est pas une preuve sémantique : chaque score reste celui de son module.

## Mesures

| étage | mesure | résultat |
|---|---|---:|
| **M1** | code exact sur 528 surfaces réelles | **528/528** |
| **M5** contexte | `source`, ordre 1, split 80/20 par partie, 160 parties test | **18,70 %** (majoritaire 6,49 %) ; surprise **2,423** vs **3,539** |
| **M5** sans contexte | même split | **12,60 %** ; surprise **3,112** |
| **M6** | conjonction 88 essais | **94,32 %** (base 75 %) |
| **M6** | tâche sens/langue 792 essais | **94,95 %** (base 50 %), commutation 0 |
| **M8** | prototypes sur les 528 épisodes (non tenus à l'écart) | champs **96,14 %**, exact **57,95 %**, 7 prototypes |
| **M9** | M1 sans contexte | **70,83 %** |

## Lecture

- **M1** porte la chaîne : sans lui, rien.
- **M5** avec le plateau gagne **+6,1 pts** d'exact et **−1,12 nat** de surprise sur `source` ;
  c'est le gain de contexte déjà mesuré par A6, retrouvé dans le pipeline.
- **M6** est un **sélecteur** ; la commutation reste nulle.
- **M8** est mesuré 
… [13225 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 120,520p tools/cerveau/predictif.py", "description": "Read predictif.py rest"}`

  ```
occ = cases.split(",")
        return (occ if len(occ) == 32 else None), trait
    if jeu == "go":
        plat = _champ_contexte(contexte, "plateau")
        if not plat:
            return None, None
        try:
            occ = [int(x) for x in plat.strip("[]").replace(" ", "").split(",") if x]
        except ValueError:
            return None, None
        return (occ if len(occ) == 81 else None), trait
    if jeu == "morpion":
        cases = _champ_contexte(contexte, "cases")
        if not cases:
            return None, None
        occ = cases.split(",")
        return (occ if len(occ) == 9 else None), trait
    return None, None


def candidats_contexte(contexte: str, jeu: str, cible: str):
    """Les valeurs de `cible` compatibles avec le plateau, ou None.

    Le filtre est **purement observable** : pour `source`, les cases occupées
    par le trait (on ne peut déplacer que sa pièce) ; pour `cible`, les cases
    qui ne sont pas occupées par le trait (case vide, ou pièce adverse pour une
    prise). Aucune règle de déplacement n'est utilisée : la géométrie des coups
    reste inconnue, c'est ce que mesure l'écart à l'oracle.
    """
    occ, trait = plateau_contexte(
… [16376 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection des codecs (contexte) et de la porte M6

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,120p tools/jeux/codecs.py && echo \"=== grep lit ===\" && grep -n \"def lit\\|def rend\\|contexte\" tools/jeux/codecs.py | head -40", "description": "Read codecs API"}`

  ```
[stderr]
sed: can't read tools/jeux/codecs.py: No such file or directory
[exit code: 2]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"def executer\\|def executer_switch\\|return\" tools/cerveau/gating.py | tail -30 && sed -n 250,360p tools/cerveau/gating.py", "description": "Read Porte.executer"}`

  ```
143:    return max(0.0, centre - demi), min(1.0, centre + demi)
148:    return (tp * tn - fp * fn) / denom if denom else 0.0
176:            return self._cache_langue[texte]
183:        return resultat
187:        return MULTI.detecte_langue(texte)
196:            return None
198:        return min(votes, key=lambda langue: (-votes[langue], langue))
204:            return self._cache_lecture[cle]
211:        return code
243:            return []
247:            return sorted(groupes[cle][langue], key=lambda i: i["texte"])[0]
273:        return essais
312:            return []
315:            return sorted(groupes[cle][langue], key=lambda i: i["texte"])[0]
360:        return essais
400:        return decisions
441:            return x["corrects"] / x["n"] if x["n"] else 0.0
460:        return {
480:    def executer_switch(self, items=None, cibles=("fr", "en")) -> dict:
489:            return {"exact": 0.0, "n": 0, "effet_conflit": 0.0,
517:        return resultat
544:        return decisions
581:        return {
620:        return {"langue_n": len(paires), "langue_exact": langue_ok / len(paires) if paires else 0.0,
634:            return {"cout": 0.0, "n_commutations": 0, "n_repetit
… [6346 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls tools/jeux/ && grep -rn \"def lit\" tools/jeux/ | head", "description": "Find codec lit"}`

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
tools/jeux/codecs/base.py:111:    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
tools/jeux/codecs/base.py:193:def lit(texte: str, jeu: str | None = None, niveau: int = 4,
tools/jeux/codecs/morpion.py:221:    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
tools/jeux/codecs/echecs.py:256:    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
tools/jeux/codecs/dames.py:134:    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
tools/jeux/codecs/go.py:141:    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
tools/jeux/codecs/cartes.py:144:    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 660,712p tools/cerveau/gating.py && echo \"=== PORTE INIT ===\" && sed -n 160,250p tools/cerveau/gating.py", "description": "Read Porte executer and init"}`

  ```
precedente = langue_bloc
        def moyenne(classe):
            vals = [e for e, c in zip(erreurs, classes) if c == classe]
            return sum(vals) / len(vals) if vals else 0.0
        return {"cout": moyenne("commutation") - moyenne("repetition"),
                "n_commutations": classes.count("commutation"),
                "n_repetitions": classes.count("repetition"),
                "erreur_commutation": moyenne("commutation"),
                "erreur_repetition": moyenne("repetition")}

    # ------------------------------------------------------------------
    # Le point d'entrée (compatible avec `batterie.m6`).
    # ------------------------------------------------------------------
    def executer(self, items=None, cibles=("fr", "en")) -> dict:
        """Exécute la tâche de conflit et rend toutes les mesures.

        Les clés historiques (`exact`, `faux_positifs`, `faux_negatifs`, `n`,
        `cout_commutation`) sont conservées telles quelles pour la batterie.
        """
        essais = self.tache_conflit(items, cibles)
        if not essais:
            return {"exact": 0.0, "faux_positifs": 0, "faux_negatifs": 0,
                    "n": 0, "cout_commutatio
… [5456 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test rapide de M1 sur les items typés et reconstruction des contextes RSN

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import code_rsn\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multi … [822 caractères tronqués]`

  ```
n items 528
de 146 vers 146
formats {'algebrique': 2, 'carte': 8, 'cellule': 22, 'francais': 5, 'gtp': 10, 'multilingue': 449, 'numerique': 11, 'san': 12, 'sgf': 1, 'uci': 8}
ItemType(texte='A1', code={'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 0, 'symbole': 'X', 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}, jeu='morpion', nature='coup', langue='fr', paire='morpion-a1', format='cellule', contexte='morpion etat trait=X taille=3 cases=.,.,.,.,.,.,.,.,.')
ItemType(texte='a1', code={'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 0, 'symbole': 'X', 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}, jeu='morpion', nature='coup', langue='fr', paire='morpion-a1', format='cellule', contexte='morpion etat trait=X taille=3 cases=.,.,.,.,.,.,.,.,.')
ItemType(texte='(1,1)', code={'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 0, 'symbole': 'X', 'carte': None, 'taille': Non
… [1931 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import co … [2048 caractères tronqués]`

  ```
match keys 528 528 True
de 146 vers 146
M1 code exact de-subset: 146/146 = 1.0000; sans contexte 138/146 = 0.9452
M1 code exact vers-subset: 146/146 = 1.0000; sans contexte 138/146 = 0.9452
de field exact 146 146 1.0 sans ctx 0.9452054794520548
vers field exact 146 146 1.0 sans ctx 0.9452054794520548
M1 sequences sans contexte: 2400 8733 0.27481964960494676
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv && CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python -c \"import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))\"", "description": "Che … [21 caractères tronqués]`

  ```
name, memory.used [MiB], memory.total [MiB]
Quadro RTX 5000, 1 MiB, 16384 MiB
Quadro RTX 5000, 1 MiB, 16384 MiB
2.11.0+cu130 True Quadro RTX 5000
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat tools/semantique/normalisation.py && grep -n \"def pad\" -A 12 tools/semantique/entrainer.py", "description": "Read normalisation and pad"}`

  ```
#!/usr/bin/env python3
"""normalisation.py — la surface vers des concepts, avant le parseur natif.

Le lexique multilingue connaît les noms de jeux, les pièces, les rangs et les
enseignes dans 66 langues. On remplace ces formes par un **concept canonique**
(`[jeu.morpion]`, `[echecs.piece.N]`, `[cartes.rang.13]`) ; les coordonnées et les
nombres restent. Deux surfaces qui disent la même chose dans deux langues
deviennent alors **presque identiques** — c'est ce qui doit rendre le natif
cohérent entre langues.
"""
from __future__ import annotations

from jeux.lexique import normalise_forme
from jeux.lexique_multilingue import MULTI

DOMAINES = ("jeu.nom", "echecs.piece", "cartes.rang", "cartes.couleur",
            "go.passe", "commun.couleur")


def normaliser(texte: str) -> str:
    t = normalise_forme(texte)
    if not t:
        return t
    tokens = t.split()
    trouves = []
    for domaine in DOMAINES:
        trouves.extend(MULTI.cherche(domaine, texte))
    jeux = {m.concept for m in trouves if m.domaine == "jeu.nom"}
    # Une enseigne de carte tranche l'ambiguïté « roi » (pièce d'échecs vs rang).
    cartes = any(m.domaine == "cartes.couleur" for m in trouves) or "jeu.cart
… [1479 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Benchmark du coût d'entraînement M2 (300 pas, avec/sans contexte)

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat > /tmp/a9_bench.py <<'EOF'\nimport time, sys, torch\nfrom transformers import AutoModelForCausalLM\nsys.path.insert(0,\"tools\")\nfrom cerveau.voies import entrainer, evaluer_champs\nfrom semantique.typed_corpus import items\n\nbase = AutoModelFor … [943 caractères tronqués]`

  ```
loaded 512 params 31.630848
ctx False 20 pas 2.53 s -> 300 pas ~ 37.9 s
eval 0.78 s {'de': (0.4863, 146), 'vers': (0.9315, 146)}
ctx True 20 pas 3.8 s -> 300 pas ~ 57.0 s
eval 1.58 s {'de': (0.5, 146), 'vers': (0.4589, 146)}
[stderr]
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 973.54it/s]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nfrom cerveau.sequences import corpus\nseqs=corpus(0,200,12)\nfor s in seqs[:1]+[x for x in seqs if x.jeu==\"dames\"][:1]+[x for x in seqs if x.jeu==\"go\"][:1]+[x for x in seqs if x.jeu==\" … [205 caractères tronqués]`

  ```
echecs | g3 | echecs etat trait=w roques=KQkq demi=0 plein=1 plateau=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR | code {'jeu': 'echecs', 'action': 'deplacer', 'de': 54, 'vers': 46}
dames | 12-16 | dames etat trait=b demi=0 cases=b,b,b,b,b,b,b,b,b,b,b,b,.,.,.,.,.,.,.,.,w,w,w,w,w,w,w,w,w,w,w,w | code {'jeu': 'dames', 'action': 'prendre', 'chemin_0': 11, 'chemin_1': 15}
go | G3 | go etat trait=1 taille=9 passe=0 plateau=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, | code {'jeu': 'go', 'action': 'poser', 'taille': 9, 'point': 60}
morpion | C1 | morpion etat trait=X taille=3 cases=.,.,.,.,.,.,.,.,. | code {'jeu': 'morpion', 'action': 'jouer_case', 'case': 2, 'symbole': 'X'}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 250,330p tools/jeux/codecs/echecs.py && echo \"=== DAMES ===\" && sed -n 130,180p tools/jeux/codecs/dames.py", "description": "Read codec lit context use"}`

  ```
# Codec
# ---------------------------------------------------------------------------
class CodecEchecs(Codec):
    jeu = "echecs"
    formats = ("fen", "diagramme", "san", "uci", "francais", "pgn", "canonique")

    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
            langue: str | None = None) -> Lecture:
        lec = self.lecture(texte, niveau, langue)
        if not texte or not texte.strip():
            return self.echoue(lec, "surface vide")

        # 1. FEN = état
        if _est_fen(texte):
            try:
                pos = E.Position.depuis_fen(texte.strip(), valide=(niveau >= 4))
                if niveau >= 4:
                    pos = _canonise_position(pos)
            except Exception as e:
                return self.echoue(lec, f"FEN invalide : {e}")
            lec.format = "fen"
            lec.arbre = Arbre("etat_echecs", (("fen", pos.fen()),))
            return self.reussi(lec, E.rsn_depuis_position(pos), "fen", 1.0)

        # 2. diagramme = état
        if niveau >= 1 and _est_diagramme(texte):
            try:
                pos = _lit_diagramme(texte)
                if niveau >= 4:
                    pos = _canonise
… [4990 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"def rsn_depuis_position\\|def position_depuis_rsn\" -A 30 tools/jeux/regles/echecs.py | head -70 && echo \"=== DAMES ===\" && grep -n \"def rsn_depuis_position\\|def position_depuis_rsn\" -A 25 tools/jeux/regles/dames.py | head -60 && echo \ … [263 caractères tronqués]`

  ```
794:def rsn_depuis_position(pos: Position, annotation: Annotation | None = None) -> RSN:
795-    corps = {
796-        "plateau": pos.fen().split()[0],
797-        "trait": "w" if pos.trait == BLANC else "b",
798-        "roques": "".join(ch for bit, ch in ((1, "K"), (2, "Q"), (4, "k"), (8, "q"))
799-                          if pos.roques & bit) or "-",
800-        "ep": indice_vers_case(pos.ep) if pos.ep >= 0 else None,
801-        "demi": pos.demi,
802-        "plein": pos.plein,
803-    }
804-    return RSN("echecs", "etat", corps,
805-               annotation or Annotation(langue="notation", format="fen", surface=""))
806-
807-
808:def position_depuis_rsn(rsn: RSN, valide: bool = True) -> Position:
809-    c = rsn.corps
810-    roques = c.get("roques") or "-"
811-    ep = c.get("ep") or "-"
812-    fen = f"{c['plateau']} {c['trait']} {roques} {ep} {int(c.get('demi', 0))} {int(c.get('plein', 1))}"
813-    return Position.depuis_fen(fen, valide=valide)
814-
815-
816-def action_depuis_coup(coup: Coup, annotation: Annotation | None = None) -> RSN:
817-    corps = {
818-        "de": coup.de,
819-        "vers": coup.vers,
820-        "promotion": {CAVALIER: "n", FOU: "b", TOUR: "
… [3987 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport re\nfrom jeux.rsn import RSN\nfrom cerveau.sequences import corpus\nfrom cerveau.hub import Hub\n\ndef champs_resume(s):\n    out={}\n    for m in re.finditer(r\"(\\w+)=(\\[[^\\]]*\\ … [1654 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 37, in <module>
  File "<stdin>", line 16, in ctx_depuis_resume
ValueError: invalid literal for int() with base 10: 'e6'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport re\nfrom jeux.rsn import RSN\nfrom cerveau.sequences import corpus\nfrom cerveau.hub import Hub\n\ndef champs_resume(s):\n    out={}\n    for m in re.finditer(r\"(\\w+)=(\\[[^\\]]*\\ … [1662 caractères tronqués]`

  ```
Counter({'echecs': 2400, 'dames': 2400, 'go': 2400, 'morpion': 1533}) Counter({'echecs': 2400, 'dames': 2400, 'go': 2400, 'morpion': 0})
('morpion', 'C1', {'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 2, 'symbole': 'X', 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}, None)
('morpion', 'C2', {'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 5, 'symbole': 'O', 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}, None)
('morpion', 'A1', {'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 0, 'symbole': 'X', 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}, None)
('morpion', 'B2', {'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 4, 'symbole': 'O', 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_
… [4336 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 210,280p tools/jeux/codecs/morpion.py && grep -n \"def rsn\\|etat_initial\\|def avec\" -A 20 tools/jeux/regles/morpion.py | head -80", "description": "Inspect morpion codec and state"}`

  ```
return "O", None
    return None, f"comptes impossibles : {x} X contre {o} O"


class CodecMorpion(Codec):
    jeu = "morpion"
    formats = ("grille", "diagramme", "canonique", "cellule", "texte", "liste", "naturel")

    # ------------------------------------------------------------------
    # Lecture
    # ------------------------------------------------------------------
    def lit(self, texte: str, niveau: int = 4, contexte: RSN | None = None,
            langue: str | None = None) -> Lecture:
        lec = self.lecture(texte, niveau, langue, format="inconnu")
        if not texte or not texte.strip():
            return self.echoue(lec, "surface vide")
        texte = self.sans_nom_jeu(texte)

        # 1. une grille = un état
        cases, trait_exp, ambiguites = _cases_depuis_grille(texte, niveau)
        if cases is not None:
            lec.format = "grille"
            lec.ambiguites = tuple(ambiguites)
            if niveau < 4:
                # aux niveaux bas, on ne vérifie pas la cohérence des comptes
                trait = trait_exp or ("O" if cases.count("X") == cases.count("O") + 1 else "X")
            else:
                trait, err = _trait_derive(cases)

… [3117 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"def coup_valide\\|def trait\\|def applique\" -A 25 tools/jeux/regles/morpion.py", "description": "Inspect morpion coup_valide"}`

  ```
31:def trait(rsn: RSN) -> str:
32-    return str(rsn.corps.get("trait") or "X")
33-
34-
35-def gagnant(cases_: Iterable[str | None]) -> str | None:
36-    c = list(cases_)
37-    for a, b, d in LIGNES:
38-        if c[a] is not None and c[a] == c[b] == c[d]:
39-            return c[a]
40-    return None
41-
42-
43-def plein(cases_: Iterable[str | None]) -> bool:
44-    return all(x is not None for x in cases_)
45-
46-
47-def resultat(rsn: RSN) -> str | None:
48-    """« X », « O », « N » (nulle) ou None (en cours)."""
49-    c = cases(rsn)
50-    g = gagnant(c)
51-    if g:
52-        return g
53-    if plein(c):
54-        return "N"
55-    return None
56-
--
72:def coup_valide(rsn: RSN, coup: RSN) -> tuple[bool, str]:
73-    if coup.jeu != "morpion" or coup.nature != "coup":
74-        return False, "ce n'est pas un coup de morpion"
75-    i = coup.corps.get("case")
76-    if not isinstance(i, int) or not (0 <= i < 9):
77-        return False, f"case hors du plateau : {i!r}"
78-    if cases(rsn)[i] is not None:
79-        return False, f"la case {i} est déjà occupée"
80-    s = coup.corps.get("symbole")
81-    if s is not None and s != trait(rsn):
82-        return False, f"c'est
… [1400 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des masques vu/inédit et de l'alignement des 146 items

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import items_synth\nfrom semantique.normalisation import normaliser\n\nits=items(); syn=items_synth()\nprint(\"synth\ … [1001 caractères tronqués]`

  ```
synth 16662
subsets equal order: True
same keys True
de train 3660 classes 10 seen 126 unseen 20 unseen covered 13
  unseen codes Counter({52: 6, 62: 6, 60: 4, 8: 2, 28: 1, 57: 1})
vers train 3660 classes 16 seen 126 unseen 20 unseen covered 13
  unseen codes Counter({36: 6, 45: 6, 62: 2, 58: 2, 0: 2, 19: 1, 42: 1})
  ```

### 🤖 Assistant

⏵ Vérification des mesures de référence M1/M6 avant d'écrire le module

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux import code_rsn\nfrom cerveau.hub impor … [713 caractères tronqués]`

  ```
M1 528 avec 528 sans 374 1.0 0.7083333333333334
M6 executer keys {'exact': 0.9431818181818182, 'n': 88, 'vrais_positifs': 17, 'faux_positifs': 0, 'faux_negatifs': 5, 'vrais_negatifs': 66, 'sensibilite': 0.7727272727272727, 'specificite': 1.0, 'exactitude_equilibree': 0.8863636363636364, 'mcc': 0.8475316272298808, 'sensibilite_ic95': (0.5655964393704065, 0.8987710920517964), 'specificite_ic95': (0.9449955327483907, 1.0), 'taux_base_tout_non': 0.75, 'par_condition': {'go': {'n': 22, 'corrects': 17, 'acceptes': 17, 'exact': 0.7727272727272727}, 'traduction': {'n': 22, 'corrects': 22, 'acceptes': 0, 'exact': 1.0}, 'langue': {'n': 22, 'corrects': 22, 'acceptes': 0, 'exact': 1.0}, 'ni': {'n': 22, 'corrects': 22, 'acceptes': 0, 'exact': 1.0}}, 'par_langue': {'fr': {'n': 44, 'corrects': 42, 'tp': 9, 'fn': 2, 'exact': 0.9545454545454546, 'sensibilite': 0.8181818181818182}, 'en': {'n': 44, 'corrects': 41, 'tp': 8, 'fn': 3, 'exact': 0.9318181818181818, 'sensibilite': 0.7272727272727273}}, 'politique': 'conjonction', 'cibles': ['fr', 'en'], 'cout_commutation': 0.0, 'cout_commutation_details': {'cout': 0.0, 'n_commutations': 21, 'n_repetitions': 21, 'erreur_commutation': 0.05952380952380952, 'e
… [2020 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Écriture du module `pipeline_semantique_m2.py` (chaîne + mesures M9)

- **write** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "content": "#!/usr/bin/env python3\n\"\"\"pipeline_semantique_m2.py — B13 + M2 : la chaîne M1 → M2 → M5 → M6.\n\nCe module est un **test d'intégration**, pas un nouveau module de perception.\nIl branche les brique … [39659 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Correction du module (device, agrégation, flux M5) avant le test fumée

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "old_string": "from .predictif import Predictif, permuter_contextes, valeur\nfrom .sequences import Pas, Sequence, corpus", "new_string": "from .predictif import Predictif, permuter_contextes\nfrom .sequences impo … [21 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "old_string": "def _entrees_voies(m, textes, contextes, seq: int = 64, seq_ctx: int = 192):\n    x, masque = pad([octets(normaliser(t), seq) for t in textes])\n    if not m.contexte:\n        return x, masque, Non … [498 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "old_string": "        x, masque, c, cm = _entrees_voies(self.voies, [texte], [contexte],\n                                          seq=seq, seq_ctx=seq_ctx)\n        self.voies.eval()\n        with torch.no_grad … [733 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "old_string": "        if self.voies is None:\n            raise ValueError(\"aucun modèle M2 branché\")\n        return evaluer_champs(self.voies, items, champs=tuple(champs),\n                              devic … [389 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"plat.update\\|m1_sans_ok\\|code_m2 = p.coder\\|pred_m5\\|m2_consomme\" tools/cerveau/pipeline_semantique_m2.py", "description": "Locate sections to fix"}`

  ```
580:                plat.update({f"{champ}_{k}": v
614:            m1_sans_ok = [int(it.code[champ] is not None
620:            erreurs = [i for i, v in enumerate(m1_sans_ok) if not v]
625:                sum(int(a or b) for a, b in zip(m1_sans_ok, ok))
736:    code_m2 = p.coder_voies(exemple.texte, exemple.jeu, ctx) if False else None
739:    code_m2 = p.coder_voies(exemple.texte, exemple.jeu, ctx)
740:    pred_m5, prob_m5 = p.predictif.predire(
747:        "m5": {"cible": p.predictif.cible, "valeur": pred_m5,
750:        "m2_consomme_par_m5": False,
  ```

### 👤 Utilisateur

Agent f0969e87-af0c-43b1-93cf-f278d9c90846 sent a message: 
Timebox : donne un point et écris /tmp/a9-pipeline-m2.json/.md dès qu'une mesure existe, même partielle ; termine ensuite.

### 🤖 Assistant

⏵ Point d'étape au parent, puis correction et lancement des mesures

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "A9 — point d'étape (timebox). Références vérifiées : M1 528/528 avec contexte, 374/528 (70,8 %) sans ; sur les 146 items `de`/`vers`, M1 = 146/146 avec contexte, 138/146 (94,5 %) sans. M6 = 94,32 % (confluence) / 94,95 % (commutation). … [463 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "offset": 560, "limit": 80}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py</path>
<type>file</type>
<content>
560:     for graine in graines:
561:         for contexte in (True, False):
562:             m, info = _train_m2(base, pas, graine, contexte, device=device,
563:                                 cache_dir=cache_dir, reuse=reuse)
564:             modeles[(graine, contexte)] = m
565:             infos_train.append(info)
566: 
567:     # ---- M2 : évaluation par condition ------------------------------
568:     par_graine = {"contexte_reel": {}, "contexte_vide": {}, "sans_contexte": {}}
569:     predictions = {"contexte_reel": {}, "contexte_vide": {}}
570:     for graine in graines:
571:         m_ctx = modeles[(graine, True)]
572:         m_nc = modeles[(graine, False)]
573:         reel = _mesurer_m2(m_ctx, items_146, synth, "reel", lesions=True)
574:         vide = _mesurer_m2(m_ctx, items_146, synth, "vide", lesions=False)
575:         sans = _mesurer_m2(m_nc, items_146, synth, "reel", lesions=True)
576:         for nom, r in (("contexte_reel", reel), ("contexte_vide", vide),
577:                        ("sans_contexte", sans)):
578:             plat = {}
579:             
… [3597 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "new_string": "        for nom, r in ((\"contexte_reel\", reel), (\"contexte_vide\", vide),\n                       (\"sans_contexte\", sans)):\n            plat = {}\n            for champ in CHAMPS_DORSAUX:\n    … [1502 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "new_string": "    chaine = {\"sans_m2\": {\"de\": m1_avec[\"de\"][\"exact\"],\n                          \"vers\": m1_avec[\"vers\"][\"exact\"]},\n              \"m1_sans_contexte\": {\"de\": m1_sans[\"de\"][\"ex … [2751 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "limit": 60, "offset": 720}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py</path>
<type>file</type>
<content>
720: 
721:     # ---- Flux : la chaîne se parle-t-elle ? -------------------------
722:     exemple = items_146[0]
723:     ctx = None
724:     # retrouver un contexte RSN réel pour l'exemple
725:     for it in reels:
726:         if (it.texte, it.jeu) == (exemple.texte, exemple.jeu):
727:             ctx = it.contexte
728:             break
729:     code_m1 = hub.percevoir(exemple.texte, exemple.jeu, ctx)
730:     code_m2 = p.coder_voies(exemple.texte, exemple.jeu, ctx) if False else None
731:     # `p` n'a pas encore de modèle : on prend la graine 1, condition contexte.
732:     p.voies = modeles[(graines[0], True)]
733:     code_m2 = p.coder_voies(exemple.texte, exemple.jeu, ctx)
734:     pred_m5, prob_m5 = p.predictif.predire(
735:         code_m1, contexte=getattr(exemple, "contexte", None))
736:     flux = {
737:         "exemple": {"texte": exemple.texte, "jeu": exemple.jeu,
738:                     "code_attendu": exemple.code},
739:         "m1": code_m1,
740:         "m2": code_m2,
741:         "m5": {"cible": p.predictif.cible, "valeur": pred_m5,
742:           
… [1875 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "new_string": "    code_m1 = hub.percevoir(exemple.texte, exemple.jeu, ctx)\n    # `p` n'a pas encore de modèle : on prend la graine 1, condition contexte.\n    p.voies = modeles[(graines[0], True)]\n    code_m2 = … [763 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "limit": 55, "offset": 795}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py</path>
<type>file</type>
<content>
795:     """Les phrases que les chiffres autorisent, et celles qu'ils interdisent."""
796:     de = m2["contexte_reel"]["de_global_exact"]["moyenne"]
797:     vers = m2["contexte_reel"]["vers_global_exact"]["moyenne"]
798:     return {
799:         "M1_code_exact": m1["code_exact"],
800:         "M1_de_exact": m1["de"]["exact"],
801:         "M1_vers_exact": m1["vers"]["exact"],
802:         "M2_de_exact": de,
803:         "M2_vers_exact": vers,
804:         "M2_ecart_de": de - m1["de"]["exact"],
805:         "M2_ecart_vers": vers - m1["vers"]["exact"],
806:         "M2_sans_contexte_de": m2["sans_contexte"]["de_global_exact"]["moyenne"],
807:         "M2_sans_contexte_vers": m2["sans_contexte"]["vers_global_exact"]["moyenne"],
808:         "M5_source_avec_plateau": m5["source"]["chaine_m1"]["exact"],
809:         "M5_source_sans_plateau": m5["source"]["sans_plateau"]["exact"],
810:         "M5_source_surprise_avec": m5["source"]["chaine_m1"]["surprise"],
811:         "M5_source_surprise_sans": m5["source"]["sans_plateau"]["surprise"],
812:         "M6_confluence": m6["con
… [2190 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "new_string": "    de = m2[\"contexte_reel\"][\"de_global_exact\"][\"moyenne\"]\n    vers = m2[\"contexte_reel\"][\"vers_global_exact\"][\"moyenne\"]\n    ameliore = (de > m1[\"de\"][\"exact\"] or vers > m1[\"vers … [3915 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"m.base.device\\|self.device\\|contexte_vide\\|predictions\\[nom\\]\" tools/cerveau/pipeline_semantique_m2.py | head -20 && /home/stephane/gpu-env/bin/python -c \"import ast; ast.parse(open('tools/cerveau/pipeline_semantique_m2.py').read());  … [75 caractères tronqués]`

  ```
167:        self.device = device
473:    r = evaluer_champs(m, items_, champs=CHAMPS_DORSAUX, device=str(m.base.device),
568:    par_graine = {"contexte_reel": {}, "contexte_vide": {}, "sans_contexte": {}}
569:    predictions = {"contexte_reel": {}, "contexte_vide": {}}
576:        for nom, r in (("contexte_reel", reel), ("contexte_vide", vide),
584:                predictions[nom][graine] = {
syntax ok
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "new_string": "    r = evaluer_champs(m, items_, champs=CHAMPS_DORSAUX, device=_device_de(m),\n                       lesions=lesions, contexte_mode=contexte_mode,\n                       retour_pred=True)", "old_ … [207 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py has been updated successfully.
  ```

### 🤖 Assistant

⏵ Test fumée de bout en bout du module (2 pas, 1 graine)

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=0 PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m cerveau.pipeline_semantique_m2 --pas 2 --graines 1 --sequences-n 2 --sequences-pas 3 --cache /tmp/a9-smoke-cache --sortie /tmp/a9-smoke.json 2>&1 | tail -30", "description":  … [57 caractères tronqués]`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights:  90%|█████████ | 81/90 [00:00<00:00, 793.12it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 870.36it/s]
{
 "duree_s": 24.0,
 "M1": 1.0,
 "M2_de": 0.4589041095890411,
 "M2_vers": 0.0,
 "M2_sans_contexte_de": 0.0273972602739726,
 "M5_source": 0.0,
 "M5_source_sans_plateau": 0.0,
 "M6_confluence": 0.9431818181818182,
 "sortie": "/tmp/a9-smoke.json"
}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nr=json.load(open(\"/tmp/a9-smoke.json\"))\nprint(\"keys\", list(r))\nprint(\"M1 seq\", r[\"M5\"][\"m1_sur_sequences\"])\nprint(\"M2 conditions keys\", list(r[\"M2\"][\"contexte_reel\"])[:10])\n … [272 caractères tronqués]`

  ```
keys ['meta', 'corpus', 'M1', 'M2', 'chaine', 'M5', 'M6', 'M9', 'flux', 'verdict']
M1 seq {'avec_contexte': {'n': 6, 'code_exact': 1.0, 'n_none': 0}, 'sans_contexte': {'n': 6, 'code_exact': 0.5, 'n_none': 0}, 'avec_contexte_train': {'n': 18, 'code_exact': 1.0, 'n_none': 0}, 'sans_contexte_train': {'n': 18, 'code_exact': 0.16666666666666666, 'n_none': 6}}
M2 conditions keys ['de_action', 'de_global_exact', 'de_global_macro', 'de_inedit_couvert_exact', 'de_inedit_couvert_n', 'de_inedit_exact', 'de_inedit_n', 'de_lesion_dorsale_action', 'de_lesion_dorsale_champ', 'de_lesion_ventrale_action']
chaine {'sans_m2': {'de': 1.0, 'vers': 1.0}, 'm1_sans_contexte': {'de': 0.9452054794520548, 'vers': 0.9452054794520548}, 'avec_m2': {'de': {'moyenne': 0.4589041095890411, 'ecart_type': 0.0, 'valeurs': [0.4589041095890411]}, 'vers': {'moyenne': 0.0, 'ecart_type': 0.0, 'valeurs': [0.0]}}, 'de_oracle_secours': {'moyenne': 3.0, 'ecart_type': 0.0, 'valeurs': [3.0]}, 'de_erreurs_m1_sans_contexte': {'moyenne': 8.0, 'ecart_type': 0.0, 'valeurs': [8.0]}, 'de_oracle_exact': {'moyenne': 0.9657534246575342, 'ecart_type': 0.0, 'valeurs': [0.9657534246575342]}, 'vers_oracle_secours': {'moyenne': 0.0, 'ecart_typ
… [2078 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nr=json.load(open(\"/tmp/a9-smoke.json\"))\nfor c in (\"source\",\"cible\"):\n    print(\"---\",c)\n    for k,v in r[\"M5\"][c].items():\n        if k.startswith(\"par_jeu\"): print(k, v); conti … [170 caractères tronqués]`

  ```
--- source
reference_codes_vrais {'n': 2, 'exact': 0.0, 'surprise': 3.1780548303484455, 'surprise_majoritaire': 0.8754687373538999, 'hors_vocabulaire': 0}
chaine_m1 {'n': 2, 'exact': 0.0, 'surprise': 3.1780548303484455, 'surprise_majoritaire': 0.8754687373538999, 'hors_vocabulaire': 0}
sans_plateau {'n': 0, 'exact': 0.0, 'surprise': 0.0, 'surprise_majoritaire': 0.0, 'hors_vocabulaire': 2}
sans_transitions {'n': 2, 'exact': 0.0, 'surprise': 3.1780548303484455, 'surprise_majoritaire': 0.8754687373538999, 'hors_vocabulaire': 0}
m1_sans_contexte {'n': 2, 'exact': 0.0, 'surprise': 3.1780548303484455, 'surprise_majoritaire': 0.8754687373538999, 'hors_vocabulaire': 0}
plateau_permute {'n': 2, 'exact': 0.0, 'surprise': 3.1780548303484455, 'surprise_majoritaire': 0.8754687373538999, 'hors_vocabulaire': 0}
par_jeu_reference {'dames': {'n': 2, 'exact': 0.0, 'majoritaire': 0.0, 'surprise': 3.1780548303484455, 'surprise_majoritaire': 0.8754687373538999, 'gain_surprise': -2.3025860929945456}}
par_jeu_sans_plateau {}
--- cible
reference_codes_vrais {'n': 4, 'exact': 0.0, 'surprise': 3.920737573185589, 'surprise_majoritaire': 0.8754687373538999, 'hors_vocabulaire': 0}
chaine_m1 {'n': 4, 'exact': 0
… [991 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lancement des mesures complètes (300 pas × 3 graines) en arrière-plan

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=0 PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m cerveau.pipeline_semantique_m2 --pas 300 --graines 1,2,3 --cache /tmp/a9-m2-cache --sortie /tmp/a9-pipeline-m2.json > /tmp/a9-run.log 2>&1; echo \"EXIT $?\"", "description":  … [89 caractères tronqués]`

  ```
started background job bash-2212
  ```

### 🤖 Assistant

⏵ Ajout de `etape` (flux) au module, puis écriture des tests

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "new_string": "    # ---- M6 ---------------------------------------------------------\n    def selectionner(self, items=None):\n        return self.porte.executer(items)\n\n    # ---- flux ----------------------- … [698 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py has been updated successfully.
  ```

- **write** `{"content": "from __future__ import annotations\n\nimport unittest\nfrom types import SimpleNamespace\n\ntry:\n    import torch\n    import torch.nn as nn\n    _TORCH = True\nexcept ImportError:\n    torch = None\n    nn = None\n    _TORCH = False\n\nfrom jeux.regles import echecs as E\nfrom jeux.rs … [5921 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_pipeline_semantique_m2.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -i 's/from semantique.universaux import code_rsn/from semantique.universaux import CHAMPS, code_rsn/' tools/cerveau/tests/test_pipeline_semantique_m2.py && python3 - <<'EOF'\np='tools/cerveau/tests/test_pipeline_semantique_m2.py'\ns=open(p).read() … [548 caractères tronqués]`

  ```
test_code_vide (tools.cerveau.tests.test_pipeline_semantique_m2.TestPipelineSemantiqueM2.test_code_vide) ... ok
test_coder_voies_avec_contexte (tools.cerveau.tests.test_pipeline_semantique_m2.TestPipelineSemantiqueM2.test_coder_voies_avec_contexte) ... ok
test_coder_voies_faux_modele (tools.cerveau.tests.test_pipeline_semantique_m2.TestPipelineSemantiqueM2.test_coder_voies_faux_modele) ... ok
test_coder_voies_sans_modele (tools.cerveau.tests.test_pipeline_semantique_m2.TestPipelineSemantiqueM2.test_coder_voies_sans_modele) ... ok
test_contexte_depuis_resume_les_quatre_jeux (tools.cerveau.tests.test_pipeline_semantique_m2.TestPipelineSemantiqueM2.test_contexte_depuis_resume_les_quatre_jeux) ... ok
test_etape_rend_les_deux_lectures (tools.cerveau.tests.test_pipeline_semantique_m2.TestPipelineSemantiqueM2.test_etape_rend_les_deux_lectures) ... ok
test_lesionner_m1 (tools.cerveau.tests.test_pipeline_semantique_m2.TestPipelineSemantiqueM2.test_lesionner_m1) ... ok
test_lesionner_m2 (tools.cerveau.tests.test_pipeline_semantique_m2.TestPipelineSemantiqueM2.test_lesionner_m2) ... ok
test_lesionner_m5 (tools.cerveau.tests.test_pipeline_semantique_m2.TestPipelineSemantiqueM2.test_lesionner_m
… [360 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de l'avancement du run complet

- **job_output** `{"job_id": "bash-2212"}`

  ```
(no new output)
[status: running]
  ```

### 🤖 Assistant

⏵ Attente du run complet (mesures M2/M5/M6)

- **job_output** `{"job_id": "bash-2212", "wait": true, "timeout_ms": 300000}`

  ```
EXIT 0
[status: completed, exit code: 0]
  ```

### 🤖 Assistant

⏵ Lecture des résultats complets et contrôle des invariants

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && tail -30 /tmp/a9-run.log && echo \"---\" && ls -l /tmp/a9-pipeline-m2.json && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nr=json.load(open(\"/tmp/a9-pipeline-m2.json\"))\nprint(json.dumps(r[\"verdict\"], ensure_ascii=False, indent=1))\np … [389 caractères tronqués]`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1014.91it/s]
{
 "duree_s": 283.4,
 "M1": 1.0,
 "M2_de": 0.9337899543378995,
 "M2_vers": 0.9360730593607306,
 "M2_sans_contexte_de": 0.9360730593607306,
 "M5_source": 0.18701298701298702,
 "M5_source_sans_plateau": 0.12597402597402596,
 "M6_confluence": 0.9431818181818182,
 "sortie": "/tmp/a9-pipeline-m2.json"
}
---
-rw-r--r--. 1 stephane stephane 139871 27 oct 12:27 /tmp/a9-pipeline-m2.json
{
 "M1_code_exact": 1.0,
 "M1_de_exact": 1.0,
 "M1_vers_exact": 1.0,
 "M2_de_exact": 0.9337899543378995,
 "M2_vers_exact": 0.9360730593607306,
 "M2_ecart_de": -0.06621004566210054,
 "M2_ecart_vers": -0.0639269406392694,
 "M2_sans_contexte_de": 0.9360730593607306,
 "M2_sans_contexte_vers": 0.9360730593607306,
 "M2_egal_M1": false,
 "M2_avec_m2_de": 0.9337899543378995,
 "M2_avec_m2_vers": 0.9360730593607306,
 "M5_source_avec_plateau": 0.18701298701298702,
 "M5_source_sans_plateau": 0.12597402597402596,
 "M5_source_surprise_avec": 2.4233681002594083,
 "M5_source_surprise_sans": 3.1116004007138085,
 "M5_source_gain_surprise": -0.6882323004544002,
 "M5_source_m1_sans_contexte": 0.280303030303
… [1132 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nr=json.load(open(\"/tmp/a9-pipeline-m2.json\"))\nprint(\"== M2 contexte_reel ==\")\nfor k,v in sorted(r[\"M2\"][\"contexte_reel\"].items()):\n    if k.startswith((\"de_\",\"vers_\")): print(k,  … [1683 caractères tronqués]`

  ```
== M2 contexte_reel ==
de_action 0.9863 ± 0.0 [0.9863013698630136, 0.9863013698630136, 0.9863013698630136]
de_global_exact 0.9338 ± 0.004 [0.9383561643835616, 0.9315068493150684, 0.9315068493150684]
de_global_macro 0.3293 ± 0.0014 [0.33088235294117646, 0.3284313725490196, 0.3285014005602241]
de_inedit_couvert_exact 0.7949 ± 0.0444 [0.8461538461538461, 0.7692307692307693, 0.7692307692307693]
de_inedit_couvert_n 13.0 ± 0.0 [13.0, 13.0, 13.0]
de_inedit_exact 0.5167 ± 0.0289 [0.55, 0.5, 0.5]
de_inedit_n 20.0 ± 0.0 [20.0, 20.0, 20.0]
de_lesion_dorsale_action 0.9863 ± 0.0 [0.9863013698630136, 0.9863013698630136, 0.9863013698630136]
de_lesion_dorsale_champ 0.0205 ± 0.0 [0.02054794520547945, 0.02054794520547945, 0.02054794520547945]
de_lesion_ventrale_action 0.1301 ± 0.0 [0.13013698630136986, 0.13013698630136986, 0.13013698630136986]
de_lesion_ventrale_champ 0.9338 ± 0.004 [0.9383561643835616, 0.9315068493150684, 0.9315068493150684]
de_nouvelle_classe_exact 0.0 ± 0.0 [0.0, 0.0, 0.0]
de_nouvelle_classe_n 7.0 ± 0.0 [7.0, 7.0, 7.0]
de_vu_exact 1.0 ± 0.0 [1.0, 1.0, 1.0]
de_vu_n 126.0 ± 0.0 [126.0, 126.0, 126.0]
vers_action 0.9863 ± 0.0 [0.9863013698630136, 0.9863013698630136, 0.986301369863013
… [7481 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Ajout des mesures de couverture M5 (contrôle M1 lésé) avant relance avec cache

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cp /tmp/a9-pipeline-m2.json /tmp/a9-pipeline-m2-run1.json && grep -n \"def _m5_par_jeu\\|m5 = {\\|for cible in (\\\"source\\\", \\\"cible\\\")\\|m1_sans_contexte\" tools/cerveau/pipeline_semantique_m2.py | head -20", "description": "Backup JSON and lo … [15 caractères tronqués]`

  ```
417:def _m5_par_jeu(train, test, cible: str, contexte: bool, ordre: int) -> dict:
606:              "m1_sans_contexte": {"de": m1_sans["de"]["exact"],
628:            d[f"{champ}_erreurs_m1_sans_contexte"] = len(erreurs)
639:        chaine[f"{champ}_erreurs_m1_sans_contexte"] = _agg(
640:            [chaine["par_graine"][g][f"{champ}_erreurs_m1_sans_contexte"]
662:    m5 = {"sequences": {"n": len(sequences), "n_train": len(train),
670:    for cible in ("source", "cible"):
683:            "m1_sans_contexte": _m5_compact(lese),
716:    for cible in ("source", "cible"):
720:                         ("m1_sans_contexte", m5[cible]["m1_sans_contexte"])):
829:        "M5_source_m1_sans_contexte": m5["source"]["m1_sans_contexte"]["exact"],
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "limit": 55, "offset": 660}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py</path>
<type>file</type>
<content>
660:     test_nc = _sequences_codes(test, codes_test_nc)
661: 
662:     m5 = {"sequences": {"n": len(sequences), "n_train": len(train),
663:                         "n_test": len(test), "graine_split": m5_graine,
664:                         "fraction": m5_fraction},
665:           "m1_sur_sequences": {"avec_contexte": info_m1_test,
666:                                "sans_contexte": info_m1_test_nc,
667:                                "avec_contexte_train": info_m1_train,
668:                                "sans_contexte_train": info_m1_train_nc},
669:           "source": {}, "cible": {}}
670:     for cible in ("source", "cible"):
671:         ref = _eval_m5(train, test, cible, True, 1)
672:         m1 = _eval_m5(train_m1, test_m1, cible, True, 1)
673:         sans = _eval_m5(train_m1, test_m1, cible, False, 1)
674:         trans = _eval_m5(train_m1, test_m1, cible, True, 0)
675:         lese = _eval_m5(train_nc, test_nc, cible, True, 1)
676:         perm = _eval_m5(train_m1, permuter_contextes(test_m1, graine=0),
677:                         cible, True, 1)
678:       
… [1824 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "new_string": "def _m5_par_jeu(train, test, cible: str, contexte: bool, ordre: int) -> dict:\n    \"\"\"Décomposition par jeu, au même réglage que le résultat global.\"\"\"\n    m = Predictif(cible=cible, ordre=or … [1657 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "new_string": "    for cible in (\"source\", \"cible\"):\n        ref = _eval_m5(train, test, cible, True, 1)\n        m1 = _eval_m5(train_m1, test_m1, cible, True, 1)\n        sans = _eval_m5(train_m1, test_m1, c … [2456 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "limit": 35, "offset": 735}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py</path>
<type>file</type>
<content>
735:     for cible in ("source", "cible"):
736:         ref = m5[cible]["chaine_m1"]
737:         for nom, res in (("sans_plateau", m5[cible]["sans_plateau"]),
738:                          ("sans_transitions", m5[cible]["sans_transitions"]),
739:                          ("m1_sans_contexte", m5[cible]["m1_sans_contexte"])):
740:             m9["M5"][f"{cible}_{nom}"] = {
741:                 "reference_exact": ref["exact"],
742:                 "lessee_exact": res["exact"],
743:                 "deficit_exact": ref["exact"] - res["exact"],
744:                 "reference_surprise": ref["surprise"],
745:                 "lessee_surprise": res["surprise"],
746:                 "gain_surprise": ref["surprise"] - res["surprise"],
747:                 "n_reference": ref["n"],
748:                 "n_lessee": res["n"],
749:             }
750: 
751:     # ---- Flux : la chaîne se parle-t-elle ? -------------------------
752:     exemple = items_146[0]
753:     ctx = None
754:     # retrouver un contexte RSN réel pour l'exemple
755:     for it in reels:
756:         if (it.texte,
… [797 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "new_string": "                \"n_reference\": ref[\"n\"],\n                \"n_lessee\": res[\"n\"],\n                \"couverture\": res[\"n\"] / max(1, ref[\"n\"]),\n            }", "old_string": "             … [92 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py has been updated successfully.
  ```

### 🤖 Assistant

⏵ Relance avec cache (ajout couverture M5), puis rédaction du rapport

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls /tmp/a9-m2-cache/ && /home/stephane/gpu-env/bin/python -c \"import ast; ast.parse(open('tools/cerveau/pipeline_semantique_m2.py').read()); print('syntax ok')\"", "description": "Check cache and syntax"}`

  ```
m2-0369dd173eb5.pt
m2-661fe406e6c0.pt
m2-9f40f60c0ec5.pt
m2-a39530146036.pt
m2-a4b4e6d1086d.pt
m2-fd2abd86cc08.pt
syntax ok
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && CUDA_VISIBLE_DEVICES=0 PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m cerveau.pipeline_semantique_m2 --pas 300 --graines 1,2,3 --cache /tmp/a9-m2-cache --reuse --sortie /tmp/a9-pipeline-m2.json > /tmp/a9-run2.log 2>&1; echo \"EXIT $?\"; tail -5 … [100 caractères tronqués]`

  ```
EXIT 0
 "M5_source": 0.18701298701298702,
 "M5_source_sans_plateau": 0.12597402597402596,
 "M6_confluence": 0.9431818181818182,
 "sortie": "/tmp/a9-pipeline-m2.json"
}
  ```

### 🤖 Assistant

⏵ Extraction des chiffres définitifs pour le rapport

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nr=json.load(open(\"/tmp/a9-pipeline-m2.json\"))\nr1=json.load(open(\"/tmp/a9-pipeline-m2-run1.json\"))\nprint(\"duree run2\", r[\"meta\"][\"duree_s\"], \"run1\", r1[\"meta\"][\"duree_s\"])\npri … [2623 caractères tronqués]`

  ```
duree run2 88.43979573249817 run1 283.377587556839
train [(1, True, 57.4), (1, False, 11.2), (2, True, 55.1), (2, False, 11.3), (3, True, 55.2), (3, False, 11.7)]
corpus {'n_items_types': 528, 'n_items_reels': 528, 'n_de': 146, 'n_vers': 146, 'n_synth': 16662, 'vu': {'de': 126, 'vers': 126}}

== M2 ==

-- contexte_reel
de_global_exact: 0.9338 ± 0.0040  [0.9384, 0.9315, 0.9315]
de_global_macro: 0.3293 ± 0.0014  [0.3309, 0.3284, 0.3285]
de_vu_exact: 1.0000 ± 0.0000  [1.0, 1.0, 1.0]
de_inedit_exact: 0.5167 ± 0.0289  [0.55, 0.5, 0.5]
de_inedit_couvert_exact: 0.7949 ± 0.0444  [0.8462, 0.7692, 0.7692]
de_nouvelle_classe_exact: 0.0000 ± 0.0000  [0.0, 0.0, 0.0]
vers_global_exact: 0.9361 ± 0.0079  [0.9315, 0.9452, 0.9315]
vers_global_macro: 0.3726 ± 0.0021  [0.3714, 0.375, 0.3714]
vers_vu_exact: 1.0000 ± 0.0000  [1.0, 1.0, 1.0]
vers_inedit_exact: 0.5333 ± 0.0577  [0.5, 0.6, 0.5]
vers_inedit_couvert_exact: 0.8205 ± 0.0888  [0.7692, 0.9231, 0.7692]
vers_nouvelle_classe_exact: 0.0000 ± 0.0000  [0.0, 0.0, 0.0]
de_action: 0.9863 ± 0.0000  [0.9863, 0.9863, 0.9863]
vers_action: 0.9863 ± 0.0000  [0.9863, 0.9863, 0.9863]
de_lesion_ventrale_action: 0.1301 ± 0.0000  [0.1301, 0.1301, 0.1301]
de_lesion_
… [10353 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de la suite complète de tests (86 + 11 nouveaux)

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -8", "description": "Run full cerveau test suite", "timeoutMs": 600000}`

  ```
.....................Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 971.57it/s]
......................................................................................................
----------------------------------------------------------------------
Ran 123 tests in 29.474s

OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git status --short && echo \"---\" && ls tools/cerveau/tests/test_*.py | wc -l && ls tools/cerveau/tests/ | grep -i m2", "description": "Check git status and new files"}`

  ```
M docs/README.md
 M docs/carte.md
 M docs/en-cours.md
 M docs/references-non-regression.md
 M docs/roadmap.md
 M docs/utilisation.md
 M journal/2026-10-27_sprint-24h.md
 M reports/README.md
 M tools/cerveau/neuromodulation.py
 M tools/cerveau/pipeline_semantique_m2.py
 M tools/cerveau/tests/test_multilingue.py
 M tools/cerveau/tests/test_neuromodulation.py
?? reports/m7-frequence.json
?? reports/rapport-m7-frequence.md
---
14
test_pipeline_semantique_m2.py
  ```

### 🤖 Assistant

⏵ Contrôle critique : le fichier M2 était-il déjà suivi dans git ?

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git ls-files | grep -E \"pipeline_semantique_m2|test_pipeline_semantique_m2\" ; echo \"--- diff stat\"; git diff --stat tools/cerveau/pipeline_semantique_m2.py tools/cerveau/tests/test_pipeline_semantique_m2.py; echo \"--- HEAD file\"; git show HEAD:t … [257 caractères tronqués]`

  ```
tools/cerveau/pipeline_semantique_m2.py
tools/cerveau/tests/test_pipeline_semantique_m2.py
--- diff stat
 tools/cerveau/pipeline_semantique_m2.py | 30 +++++++++++++++++++++++++-----
 1 file changed, 25 insertions(+), 5 deletions(-)
--- HEAD file
#!/usr/bin/env python3
"""pipeline_semantique_m2.py — B13 + M2 : la chaîne M1 → M2 → M5 → M6.

Ce module est un **test d'intégration**, pas un nouveau module de perception.
Il branche les briques existantes sur un seul flux et mesure chaque étage sur
--- HEAD test
from __future__ import annotations

import unittest
from types import SimpleNamespace

--- log
26057c13 B15 — TEST MULTILINGUE : 528 SURFACES, 66 LANGUES, 30 PAIRES
25830d86 B14 — M2 DANS LA CHAÎNE : 100 % VS 93,4/93,6 %, AUCUN ÉTAGE NE LE CONSOMME ; RAMEAU
db2c2b93 B15 — M1 SUR 66 LANGUES : 528/528, INVARIANCE 26/26 ET 15/15, CONTRÔLE PERMUTÉ 0/90
  ```

### 🤖 Assistant

⏵ Découverte : le module M2 existe déjà dans HEAD (commit B14) — comparaison avec notre version

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls -l /tmp/a9-pipeline-m2.* 2>/dev/null; echo \"--- md head\"; head -40 /tmp/a9-pipeline-m2.md 2>/dev/null; echo \"--- reports\"; ls reports/ | grep -i \"m2\\|pipeline\" ; echo \"--- diff\"; git diff --stat tools/cerveau/pipeline_semantique_m2.py; git … [122 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 141502 27 oct 12:33 /tmp/a9-pipeline-m2.json
--- md head
--- reports
pipeline-m2.json
pipeline-semantique.json
rapport-pipeline-m2.md
rapport-pipeline-semantique.md
--- diff
 tools/cerveau/pipeline_semantique_m2.py | 30 +++++++++++++++++++++++++-----
 1 file changed, 25 insertions(+), 5 deletions(-)
diff --git a/tools/cerveau/pipeline_semantique_m2.py b/tools/cerveau/pipeline_semantique_m2.py
index 3a2bb1f2..02bd6954 100644
--- a/tools/cerveau/pipeline_semantique_m2.py
+++ b/tools/cerveau/pipeline_semantique_m2.py
@@ -418,13 +418,22 @@ def _m5_par_jeu(train, test, cible: str, contexte: bool, ordre: int) -> dict:
     """Décomposition par jeu, au même réglage que le résultat global."""
     m = Predictif(cible=cible, ordre=ordre, contexte=contexte, melange=0.5)
     m.entrainer(train)
+    return _par_jeu_modele(m, test)
+
+
+def _par_jeu_modele(modele: Predictif, test) -> dict:
+    """Évalue un modèle déjà entraîné, jeu par jeu.
+
+    Sert au contrôle M1 lésé : il montre quels jeux **survivent** à la
+    privation de contexte et lesquels sont perdus. Un exact plus haut sur un
+    sous-ensemble plus petit n'est pas un gain, c'est une sélection.
+ 
… [2672 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du rapport B14 déjà commité (même dispositif) pour aligner le nôtre

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,180p reports/rapport-pipeline-m2.md", "description": "Read committed A9/B14 report"}`

  ```
# B14 — M2 dans la chaîne : un rameau, pas un étage

> **Objet.** Brancher M2 (`voies.py`) dans la chaîne B13 et mesurer s'il **ajoute** quelque chose.
> Résultat : **non**. M1 lit **100 %** des 146 items `de`/`vers` ; M2 lit **93,4 / 93,6 %** ; et
> aucun étage ne consomme M2. C'est un **rameau neural parallèle**, pas un étage du pipeline.

## Mesures (3 graines, 300 pas)

| lecture | `de` | `vers` |
|---|---:|---:|
| M1 avec contexte | **100 %** | **100 %** |
| M1 sans contexte | 94,5 % | 94,5 % |
| M2 avec contexte | **93,4 %** | **93,6 %** |
| M2 sans contexte | 93,6 % | 93,6 % |
| M2 écart vs M1 | **−6,6 pts** | **−6,4 pts** |

- M2 **vu** : 126/126 ; **inédit couvert** : 79,5 % (`de`), 82,1 % (`vers`) ; **nouvelle classe** 0/7.
- **M2 ne bat pas M1** ; l'ajouter **dégrade** le champ dorsal.
- **Aucun étage ne consomme M2** : M5 consomme le code M1 ; M6 ne lit pas le champ dorsal.

## M5 et M6 dans la chaîne

| étage | mesure |
|---|---:|
| M5 `source` avec plateau | **18,70 %** (majoritaire 6,49 %) ; surprise **2,423** |
| M5 `source` sans plateau | **12,60 %** ; surprise **3,112** |
| M5 `source` sans transitions | 14,29 % |
| M5 `source` M1 sans contexte | 28,03 % (n=396) |
… [1057 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction de `/tmp/a9-pipeline-m2.md` avec la correction du contrôle M5

- **write** `{"content": "# A9 — M2 dans la chaîne B13 : un rameau, pas un étage\n\n_Sprint autonome 24 h — sous-agent A9. Encodeur `/tmp/natif-600-512-8-align-s1` gelé (Qwen3-MoE 512d, 8 couches), GPU Quadro RTX 5000, `CUDA_VISIBLE_DEVICES=0`, `PYTHONPATH=tools`, 3 graines, 300 pas. Mesure du 2026-10-27, durée  … [16444 caractères tronqués]`

  ```
<path>/tmp/a9-pipeline-m2.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Contrôle final de cohérence JSON/MD et des fichiers modifiés

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python - <<'EOF'\nimport json\nr=json.load(open(\"/tmp/a9-pipeline-m2.json\"))\nassert \"couverture_m1_sans_contexte\" in r[\"M5\"][\"source\"]\nassert \"par_jeu_m1_sans_contexte\" in r[\"M5\"][\"source\"]\nassert \"par_jeu_ … [718 caractères tronqués]`

  ```
JSON OK 88.43979573249817 False
source per_game lese ['dames']
cible per_game lese ['dames', 'go', 'morpion']
--- git diff files
docs/README.md
docs/agent/contexte.md
docs/glossaire.md
tools/cerveau/neuromodulation.py
tools/cerveau/pipeline_semantique_m2.py
tools/cerveau/tests/test_multilingue.py
tools/revue_documentation.py
tools/taille_documents.py
--- status
 M tools/cerveau/pipeline_semantique_m2.py
  ```

- **bash** `{"command": "ls -l /tmp/a9-pipeline-m2.json /tmp/a9-pipeline-m2.md && wc -l /tmp/a9-pipeline-m2.md && head -6 /tmp/a9-pipeline-m2.md && echo \"...\" && tail -8 /tmp/a9-pipeline-m2.md", "description": "Confirm deliverables exist"}`

  ```
-rw-r--r--. 1 stephane stephane 141502 27 oct 12:33 /tmp/a9-pipeline-m2.json
-rw-------. 1 stephane stephane  16853 27 oct 12:39 /tmp/a9-pipeline-m2.md
221 /tmp/a9-pipeline-m2.md
# A9 — M2 dans la chaîne B13 : un rameau, pas un étage

_Sprint autonome 24 h — sous-agent A9. Encodeur `/tmp/natif-600-512-8-align-s1` gelé (Qwen3-MoE 512d, 8 couches), GPU Quadro RTX 5000, `CUDA_VISIBLE_DEVICES=0`, `PYTHONPATH=tools`, 3 graines, 300 pas. Mesure du 2026-10-27, durée 283,4 s (rejeu avec cache : 88,4 s)._

> **Note de dépôt.** Le dépôt contient déjà un rapport B14 (même dispositif, commit `25830d86`) et les chiffres ci-dessous le reproduisent : M1 100 %, M2 93,4/93,6 %, M5 18,70/12,60 %, M6 94,32/94,95 %. La seule différence est le **contrôle M1 lésé → M5** : le chiffre brut de 28,03 % est un **artefact de sélection** (couverture 51,4 %), pas une amélioration. Le détail est au § 4.2. Le JSON de ce run contient les champs de couverture ajoutés pour le montrer.

...
  -s tools/cerveau/tests -t tools
```

- Tests : nos **11** tests OK ; suite complète `discover` **123 tests OK** (état du dépôt au moment du run, autres chantiers inclus ; sans torch, les tests qui en dépendent sont `skip`).
- JS
… [431 caractères tronqués]
  ```

### 👤 Utilisateur

<system-reminder>
Updated instructions from: AGENTS.md

This file changed after it was loaded. Use the following content instead of the previously loaded instructions from this file.

# Directives de l'agent — Drave

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs
> unifiés (**49 portes, 8 chapitres, 179 fichiers / 246 JSON, 53 documents**), chemins archivés
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

### 🤖 Assistant

⏵ Envoi du résultat final au parent

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "A9 terminé. Résumé autoportant.\n\nATTENTION DÉPÔT : HEAD contient déjà B14 (commit 25830d86, `tools/cerveau/pipeline_semantique_m2.py`, son test, `reports/rapport-pipeline-m2.md`) avec le même dispositif. Mes mesures reproduisent exac … [2539 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

### 🤖 Assistant

⏵ Résumé final et chemins

## Résultat

**M2 n'ajoute rien à la chaîne.** M1 lit **146/146** items réels `de`/`vers` ; M2 lit **93,4 / 93,6 %**. Le remplacer dans la chaîne **dégrade** le champ dorsal de **6,4–6,6 pts**, et aucun étage ne consomme M2 (M5 consomme M1, M6 appelle le codec directement).

| mesure | `de` | `vers` |
|---|---:|---:|
| M1 avec contexte | **100,00 %** | **100,00 %** |
| M1 sans contexte | 94,52 % | 94,52 % |
| M2 avec contexte (3 graines) | **93,38 % ± 0,40** | **93,61 % ± 0,79** |
| M2 vu / inédit / inédit couvert | 100 % / 10,3/20 / 10,3/13 | 100 % / 10,7/20 / 10,7/13 |
| Chaîne avec M2 | 93,38 % | 93,61 % |
| Chaîne sans M2 | **100 %** | **100 %** |

- **M2 seul** reproduit A3 (93,6/94,3) à 0,2–0,7 pt ; A5 à 1 000 pas avec augmentation plafonne à 95,2/95,4, toujours sous M1.
- **M5** : 18,70 % avec plateau vs 12,60 % sans (surprise 2,423 vs 3,112) ; plateau permuté 5,97 % / surprise 12,639. **M6** : 94,32 % (confluence), 94,95 % (commutation).
- **M9** : lésion dorsale M2 → 2,05/2,74 % ; lésion ventrale → action 13,01 %, champ intact ; M1 sans contexte → 70,83 % (code), 94,52 % (`de`/`vers`).
- **Correction importante** : le brut « M5 avec M1 lésé = 28,03 % » est un **artefact de sélection** (couverture 51,4 %, seuls les pas de dames survivent ; la référence y fait exactement 28,03 %, les 374 pas d'échecs à 8,82 % sont perdus). Le JSON contient la couverture et le détail par jeu.

## Chemins

- `/tmp/a9-pipeline-m2.json` — chiffres, prédictions par item, couverture M5, lésions, commandes.
- `/tmp/a9-pipeline-m2.md` — rapport complet, limites et autocritique.
- `tools/cerveau/pipeline_semantique_m2.py` — module (working tree : +25/−5 pour la couverture M5).
- `tools/cerveau/tests/test_pipeline_semantique_m2.py` — 11 tests.

**Tests** : 11/11 OK ; suite complète `discover` **123 tests OK**. Aucun `git add/commit/checkout` ; docs, reports, journal, batterie non touchés.

**Note dépôt** : HEAD contient déjà B14 (même dispositif, mêmes chiffres). Notre apport est la correction du contrôle M5 M1-lésé et les champs de couverture ; le rapport B14 devrait être amendé sur ce point.

