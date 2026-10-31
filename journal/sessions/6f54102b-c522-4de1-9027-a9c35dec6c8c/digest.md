# Session DSH — relecture

- identifiant : `6f54102b-c522-4de1-9027-a9c35dec6c8c`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 09:41:21
- agent : standard


## Tour 1

### 👤 Utilisateur

Nous sommes dans /home/stephane/GitHub/Qtrinet (dépôt Drave). Sprint autonome 24 h. Tu es un sous-agent chargé d'étendre M2 (voies ventrales/dorsales) du prototype `tools/cerveau/`.

État actuel mesuré :
- M2 `tools/cerveau/voies.py` : encodeur `route` gelé, moyenne + dernier état caché ; entraînement synthétique 300 pas ; test sur 146 surfaces réelles.
- Résultat : `action` 98,6 %, `de` 93,2 % ; lésion ventrale `action` 9,6 %, `de` 93,2 % ; lésion dorsale `action` 98,6 %, `de` 0,7 %.
- Corpus : `tools/semantique/typed_corpus.items()` (528), `tools/semantique/synth_corpus.items_synth()` (16 662), `tools/semantique/normalisation.normaliser`.
- GPU disponible : `CUDA_VISIBLE_DEVICES=0`, Python `/home/stephane/gpu-env/bin/python`.

Objectif : étendre M2 à d'autres champs dorsaux (`vers`, `chemin`, `point`) et tester une ablation du contexte / du dernier état, avec contrôles.
- Entraîne et évalue `vers` (65 classes) et au moins un autre champ dorsal (`chemin_0` ou `point`) sur les surfaces synthétiques, test sur surfaces réelles.
- Teste l'ablation du dernier état (moyenne seule) pour montrer le gain du dernier état.
- Teste si le contexte (RSN) améliore, ou non ; si tu ajoutes le contexte, garde une ablation.
- Mesure exact, n, lésions ventrale/dorsale ; produis `/tmp/a3-m2.json` et `/tmp/a3-m2.md`.
- Si un champ reste au hasard, documente le négatif.

Contraintes :
- Modifie uniquement `tools/cerveau/voies.py` et, si nécessaire, `tools/cerveau/tests/test_voies.py`. Ne touche pas à `batterie.py`, docs, reports, journal, git.
- N'exécute pas de `git commit`, `git add`, `git checkout`.
- Utilise `PYTHONPATH=tools` ; `CUDA_VISIBLE_DEVICES=0`.
- Sois autonome, mesure, autocritique-toi. Réponds avec un résumé concis et les chemins.
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

⏵ Exploration du prototype M2 et du corpus

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls && echo \"---\" && ls tools/cerveau/ && echo \"---\" && ls tools/semantique/ | head -50", "description": "List repo and cerveau directories"}`

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
memoire_travail.py
neuromodulation.py
predictif.py
__pycache__
sequences.py
sommeil.py
tests
voies.py
---
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
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && wc -l tools/cerveau/voies.py tools/cerveau/tests/test_voies.py 2>/dev/null; python3 -c \"print('ok')\"", "description": "Check file sizes"}`

  ```
103 tools/cerveau/voies.py
 103 total
ok
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py"}`

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

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls tools/cerveau/tests/ && echo \"---\" && cat tools/cerveau/__init__.py", "description": "List cerveau tests"}`

  ```
__init__.py
__pycache__
test_bus.py
test_modules.py
---
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"voies\\|M2\\|entrainer\\|evaluer\" tools/cerveau/batterie.py | head -60", "description": "Find M2 usage in batterie"}`

  ```
76:    from cerveau.voies import entrainer, evaluer
78:    m, val = entrainer(base, 300, 32, 64, 1, "cuda" if torch.cuda.is_available() else "cpu", synth=True)
80:    return {"normal": evaluer(m, val, dev), "lese_ventrale": evaluer(m, val, dev, "ventral"),
81:            "lese_dorsale": evaluer(m, val, dev, "dorsal")}
142:    p = Predictif(); p.entrainer(train)
143:    return p.evaluer(test)
180:    sleep = s.evaluer(test, protos)
193:        "M2_lese_ventrale_action": m2r["lese_ventrale"]["action"],
194:        "M2_lese_dorsale_de": m2r["lese_dorsale"]["de"],
209:    out["M2"] = m2()
216:    out["M9"] = m9(out["M1"], out["M2"], out["M3"], out["M4"], out["M5"], out["M6"], out["M7"])
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,80p tools/semantique/universaux.py", "description": "Read universaux CHAMPS"}`

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
… [1507 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 60,100p tools/cerveau/batterie.py", "description": "Read M2 batterie function"}`

  ```
relu = codec(it.jeu).lit(surface, niveau=4, contexte=it.contexte)
                canon += int(relu and relu.rsn and relu.rsn.corps == it.attendu.corps)
            except Exception:
                pass
    inv = [len(v) == 1 for e, v in par_paire.items()
           if compte_paire[e] > 1]
    return {"items": len(vrais), "exact": exact / max(1, len(vrais)),
            "sans_contexte": sans_ctx / max(1, len(vrais)),
            "canonique": canon / max(1, len(vrais)),
            "invariance": sum(inv) / max(1, len(inv)),
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
    sp = m.span(seq
… [506 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,120p tools/semantique/synth_corpus.py", "description": "Read synth corpus head"}`

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
… [3477 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,140p tools/semantique/typed_corpus.py", "description": "Read typed corpus"}`

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

- **bash** `{"command": "ls -la /tmp/natif-600-512-8-align-s1 2>&1 | head; echo \"---\"; nvidia-smi -L; echo \"---\"; /home/stephane/gpu-env/bin/python -c \"import torch, transformers; print(torch.__version__, transformers.__version__, torch.cuda.is_available())\"", "description": "Check model dir and GPU env"}`

  ```
total 123596
drwxr-xr-x.   2 stephane stephane       100 26 oct 16:04 .
drwxrwxrwt. 692 root     root         19440 27 oct 09:41 ..
-rw-r--r--.   1 stephane stephane       974 26 oct 16:04 config.json
-rw-r--r--.   1 stephane stephane       153 26 oct 16:04 generation_config.json
-rw-------.   1 stephane stephane 126553768 26 oct 16:04 model.safetensors
---
GPU 0: Quadro RTX 5000 (UUID: GPU-ff8cc368-1bb8-ccef-8a76-4d17375e212e)
GPU 1: Quadro RTX 5000 (UUID: GPU-bd161106-3e3e-c50f-161a-2550ab688ce2)
---
2.11.0+cu130 5.15.0 True
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat /tmp/natif-600-512-8-align-s1/config.json; echo ---; sed -n 1,80p tools/semantique/normalisation.py; echo ---; sed -n 1,60p tools/cerveau/tests/test_modules.py", "description": "Read config, normalisation, tests"}`

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
---
#!/usr/bin/env python3
"""normalisation.py — la surface vers des concepts, avant le parseur natif.

Le lexique multilingue connaît les noms de jeux, les pièces, les rangs et les
enseignes dans 66 langues. On remplace ces f
… [2684 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport collections\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import items_synth\nits=items(); sy=items_synth()\nprint(\"real\",len(its),\"synth\",len(sy))\nfo … [661 caractères tronqués]`

  ```
real 528 synth 16662
action real_nn 528 nclasses_r 7 synth_nn 16662 nclasses_s 6
de real_nn 146 nclasses_r 6 synth_nn 3660 nclasses_s 10
vers real_nn 146 nclasses_r 8 synth_nn 3660 nclasses_s 16
point real_nn 70 nclasses_r 3 synth_nn 10044 nclasses_s 81
chemin_0 real_nn 70 nclasses_r 3 synth_nn 392 nclasses_s 4
chemin_1 real_nn 70 nclasses_r 3 synth_nn 392 nclasses_s 4
chemin_2 real_nn 3 nclasses_r 1 synth_nn 0 nclasses_s 0
jeu real_nn 528 nclasses_r 5 synth_nn 16662 nclasses_s 5
case real_nn 64 nclasses_r 4 synth_nn 2034 nclasses_s 9
carte real_nn 161 nclasses_r 7 synth_nn 470 nclasses_s 16
exemples vers:
A1 {'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 0, 'symbole': 'X', 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None} morpion morpion-a1
a1 {'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 0, 'symbole': 'X', 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None} morpion morpion-a1
(1,1) {'jeu': 'morpion', 'action': 'jouer_case', 'de
… [217 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport collections\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import items_synth\nits=items(); sy=items_synth()\nfor nom in (\"vers\",\"point\",\"chemin_0\",\" … [979 caractères tronqués]`

  ```
==================== vers
real 146 jeux Counter({'echecs': 146})
  classes [0, 19, 36, 42, 44, 45, 58, 62]
  langues 63 paires 9
  ex [('e2e4', 36, 'notation'), ('e2-e4', 36, 'notation'), ('e2 e4', 36, 'notation'), ('e4', 36, 'notation'), ('E4', 36, 'notation')]
synth 3660 jeux Counter({'echecs': 3660})
  classes [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]
  langues 62 paires 20
  ex [('بيدق a2 a3', 40, 'ar'), ('a2a3', 40, 'ar'), ('بيدق a2-a3', 40, 'ar'), ('বোড়ে a2 a3', 40, 'bn'), ('a2a3', 40, 'bn')]
==================== point
real 70 jeux Counter({'go': 70})
  classes [30, 39, 48]
  langues 63 paires 4
  ex [('D4', 48, 'notation'), ('d4', 48, 'notation'), ('pierre noire en D4', 48, 'fr'), ('ligne 4 colonne 4', 48, 'fr'), ('jouer en D4', 48, 'fr')]
synth 10044 jeux Counter({'go': 10044})
  classes [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80]
  langues 62 paires 81
  ex [('غو A9', 0, 'ar'), ('A9'
… [19717 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"voies\\|Voies\\|\\.dorsal\\|\\.ventral\" --include=*.py . | grep -v __pycache__ | grep -v \"tools/cerveau/voies.py\"", "description": "Find all references to voies module"}`

  ```
./src/roofline.py:46:    lanes_needed: int          # voies de MAC pour saturer la mémoire
./src/roofline.py:53:    """Nombre de voies de MAC nécessaires pour suivre le débit mémoire.
./src/roofline.py:88:        f"{p.lanes_needed:6d} voies  {p.alms_for_lanes:7d} ALM"
./run_quantify.py:245:    L.append("| Modèle / encodage | Taille | ms/token | tok/s | Voies MAC | ALM |")
./run_quantify.py:274:        "faut que ~312 voies de MAC (≈ 9 400 ALM, 5 % du FPGA) pour saturer les 9,66 Go/s. "
./run_sparsity.py:175:          "≈ 3 400 ALM pour 312 voies (**2 % du FPGA**) — c'est payable.",
./run_precision.py:9:**mémoire** (312 voies suffisent à saturer la DDR3 ; 95 % du FPGA dort). Ajouter
./run_precision.py:166:          "   passante. Le débit est fixé par la DDR3 (9,66 Go/s) ; 312 voies suffisent à la",
./run_precision.py:174:          "   (mux + add/sub). Pour 312 voies : ~11 000 ALM, soit **6 % du FPGA** au lieu",
./run_cpu.py:253:         "   4 cartes = 4 mémoires et 4 jeux de voies indépendants → 4× le débit, là où",
./run_list_mode.py:81:    print(f"{'mode':<34} {'ALM/voie':>10} {'voies pour saturer la DDR3':>28}")
./run_list_mode.py:91:    print("  (voies = débit mémoire / (bits par 
… [256 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,120p tools/semantique/entrainer.py", "description": "Read entrainer pad"}`

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
… [3576 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport collections\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import items_synth\nfrom semantique.normalisation import normaliser\nits=items(); sy=items_synth( … [837 caractères tronqués]`

  ```
=============== de n 146 classes 6
  distrib [(52, 70), (62, 68), (60, 4), (8, 2), (28, 1), (57, 1)]
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 12, in <module>
TypeError: object of type 'int' has no len()
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport collections\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import items_synth\nfrom semantique.normalisation import normaliser\nfrom semantique.universaux i … [1077 caractères tronqués]`

  ```
=============== de n 146 classes 6
  distrib [(52, 70), (62, 68), (60, 4), (8, 2), (28, 1), (57, 1)]
  majoritaire 0.479  uniforme 0.0154
=============== vers n 146 classes 8
  distrib [(36, 69), (45, 68), (62, 2), (58, 2), (0, 2), (19, 1), (44, 1), (42, 1)]
  majoritaire 0.473  uniforme 0.0154
=============== point n 70 classes 3
  distrib [(48, 68), (30, 1), (39, 1)]
  majoritaire 0.971  uniforme 0.0122
=============== chemin_0 n 70 classes 3
  distrib [(8, 68), (21, 1), (9, 1)]
  majoritaire 0.971  uniforme 0.0154
=============== chemin_1 n 70 classes 3
  distrib [(13, 60), (17, 8), (12, 2)]
  majoritaire 0.857  uniforme 0.0154
=============== vers real
36 'e2e4' -> 'e2e4' notation
36 'e2-e4' -> 'e2-e4' notation
36 'e2 e4' -> 'e2 e4' notation
36 'e4' -> 'e4' notation
36 'E4' -> 'e4' notation
36 'le pion de e2 vers e4' -> 'le [echecs.piece.P] de e2 vers e4' fr
36 'pawn from e2 to e4' -> '[echecs.piece.P] from e2 to e4' en
45 'Nf3' -> 'nf3' notation
45 'Cf3' -> 'cf3' fr
45 'g1f3' -> 'g1f3' notation
45 'cavalier de g1 vers f3' -> '[echecs.piece.N] de g1 vers f3' fr
45 'le cavalier g1 va en f3' -> 'le [echecs.piece.N] g1 va en f3' fr
45 'knight from g1 to f3' -> '[echecs.piece.N] fr
… [11786 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat > /tmp/a3_timing.py <<'EOF'\nimport time, torch\nfrom transformers import AutoModelForCausalLM\nfrom cerveau.voies import entrainer, evaluer\nbase = AutoModelForCausalLM.from_pretrained(\"/tmp/natif-600-512-8-align-s1\", dtype=torch.float32)\nt=ti … [505 caractères tronqués]`

  ```
train 17.644915342330933 val 146
{'action': 0.9863013698630136, 'de': 0.9315068493150684, 'n': 146} eval 0.23415040969848633
{'action': 0.14383561643835616, 'de': 0.9315068493150684, 'n': 146}
{'action': 0.9863013698630136, 'de': 0.00684931506849315, 'n': 146}
[stderr]
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 958.77it/s]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport collections, re\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import items_synth\nfrom semantique.normalisation import normaliser\nits=items(); sy=items_sy … [1276 caractères tronqués]`

  ```
de: n_test=146 surfaces_vues=126 (86.3%) paires_vues=126 (86.3%) classes 6 plafond_couverture=0.952 ctx_vides=0
vers: n_test=146 surfaces_vues=126 (86.3%) paires_vues=126 (86.3%) classes 8 plafond_couverture=0.952 ctx_vides=0
  inédits: [('e2-e4', 36), ('e2 e4', 36), ('e4', 36), ('E4', 36), ('le pion de e2 vers e4', 36), ('pawn from e2 to e4', 36), ('Nf3', 45), ('Cf3', 45), ('cavalier de g1 vers f3', 45), ('le cavalier g1 va en f3', 45), ('knight from g1 to f3', 45), ('O-O', 62), ('petit roque', 62), ('O-O-O', 58), ('grand roque', 58), ('exd6', 19), ('a8=Q', 0), ('a7a8q', 0), ('Nf3', 45), ('Nc3', 42)]
    classe 0: n=2 vu=0 couvert=False
    classe 19: n=1 vu=0 couvert=False
    classe 36: n=69 vu=63 couvert=True
    classe 42: n=1 vu=0 couvert=True
    classe 44: n=1 vu=1 couvert=True
    classe 45: n=68 vu=62 couvert=True
    classe 58: n=2 vu=0 couvert=False
    classe 62: n=2 vu=0 couvert=False
point: n_test=70 surfaces_vues=66 (94.3%) paires_vues=66 (94.3%) classes 3 plafond_couverture=1.000 ctx_vides=0
  inédits: [('pierre noire en D4', 48), ('ligne 4 colonne 4', 48), ('jouer en D4', 48), ('B[dd]', 30)]
    classe 30: n=1 vu=0 couvert=True
    classe 39: n=1 vu=1 couvert=True
… [655 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat > /tmp/a3_baseline_split.py <<'EOF'\nimport collections, torch\nfrom transformers import AutoModelForCausalLM\nfrom cerveau.voies import entrainer, Voies\nfrom semantique.entrainer import pad\nfrom semantique.normalisation import normaliser\nfrom  … [1362 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "/tmp/a3_baseline_split.py", line 6, in <module>
    from semantique.typed_corpus import items, synth_corpus, octets
ImportError: cannot import name 'synth_corpus' from 'semantique.typed_corpus' (/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/semantique/typed_corpus.py). Did you mean: 'typed_corpus'?
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -i 's/from semantique.typed_corpus import items, synth_corpus, octets/from semantique.typed_corpus import items, octets/' /tmp/a3_baseline_split.py && PYTHONPATH=tools CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python /tmp/a3_baseline_split … [75 caractères tronqués]`

  ```
graine 1: global 136/146=0.9315 vu 126/126=1.0000 inedit 10/20=0.5000
graine 2: global 137/146=0.9384 vu 126/126=1.0000 inedit 11/20=0.5500
graine 3: global 136/146=0.9315 vu 126/126=1.0000 inedit 10/20=0.5000
[stderr]
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 913.24it/s]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport collections\nfrom semantique.typed_corpus import items\nfrom semantique.synth_corpus import items_synth\nfrom semantique.normalisation import normaliser\nits=items(); sy=items_synth( … [1215 caractères tronqués]`

  ```
==================== de
  vu: n=126 dist={52: 64, 62: 62} majorite=0.508 classes=2
  inedit: n=20 dist={52: 6, 62: 6, 60: 4, 28: 1, 8: 2, 57: 1} majorite=0.300 classes=6
  inedit_couvert: n=13 dist={52: 6, 62: 6, 57: 1} majorite=0.462 classes=3
  inedit_noncouvert: n=7 dist={60: 4, 28: 1, 8: 2} majorite=0.571 classes=3
  train synth classes 10 majorite [(48, 366), (49, 366), (50, 366)] n 3660
==================== vers
  vu: n=126 dist={36: 63, 45: 62, 44: 1} majorite=0.500 classes=3
  inedit: n=20 dist={36: 6, 45: 6, 62: 2, 58: 2, 19: 1, 0: 2, 42: 1} majorite=0.300 classes=7
  inedit_couvert: n=13 dist={36: 6, 45: 6, 42: 1} majorite=0.462 classes=3
  inedit_noncouvert: n=7 dist={62: 2, 58: 2, 19: 1, 0: 2} majorite=0.286 classes=4
  train synth classes 16 majorite [(40, 366), (42, 366), (45, 366)] n 3660
==================== point
  vu: n=66 dist={48: 65, 39: 1} majorite=0.985 classes=2
  inedit: n=4 dist={48: 3, 30: 1} majorite=0.750 classes=2
  inedit_couvert: n=4 dist={48: 3, 30: 1} majorite=0.750 classes=2
  inedit_noncouvert: n=0
  train synth classes 81 majorite [(0, 124), (1, 124), (2, 124)] n 10044
==================== chemin_0
  vu: n=56 dist={8: 56} majorite=1.000 classes=
… [268 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat > /tmp/a3_baseline_items.py <<'EOF'\nimport torch\nfrom transformers import AutoModelForCausalLM\nfrom cerveau.voies import entrainer\nfrom semantique.entrainer import pad\nfrom semantique.normalisation import normaliser\nfrom semantique.typed_cor … [1097 caractères tronqués]`

  ```
OK  cible 52 pred 53 'e2-e4' -> 'e2-e4'
OK  cible 52 pred 53 'e2 e4' -> 'e2 e4'
OK  cible 52 pred 53 'e4' -> 'e4'
OK  cible 52 pred 53 'E4' -> 'e4'
OK  cible 52 pred 53 'le pion de e2 vers e4' -> 'le [echecs.piece.P] de e2 vers e4'
NON cible 52 pred 49 'pawn from e2 to e4' -> '[echecs.piece.P] from e2 to e4'
OK  cible 62 pred 63 'Nf3' -> 'nf3'
NON cible 62 pred 51 'Cf3' -> 'cf3'
OK  cible 62 pred 63 'cavalier de g1 vers f3' -> '[echecs.piece.N] de g1 vers f3'
OK  cible 62 pred 63 'le cavalier g1 va en f3' -> 'le [echecs.piece.N] g1 va en f3'
OK  cible 62 pred 63 'knight from g1 to f3' -> '[echecs.piece.N] from g1 to f3'
NON cible 60 pred 52 'O-O' -> 'o-o'
NON cible 60 pred 50 'petit roque' -> 'petit roque'
NON cible 60 pred 52 'O-O-O' -> 'o-o-o'
NON cible 60 pred 63 'grand roque' -> 'grand roque'
NON cible 28 pred 53 'exd6' -> 'exd6'
NON cible 8 pred 50 'a8=Q' -> 'a8=q'
NON cible 8 pred 49 'a7a8q' -> 'a7a8q'
OK  cible 62 pred 63 'Nf3' -> 'nf3'
NON cible 57 pred 56 'Nc3' -> 'nc3'
[stderr]
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 932.18it/s]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python - <<'EOF'\nimport time\nfrom semantique.typed_corpus import items\nt=time.time(); a=items(); print(\"items\", len(a), time.time()-t)\nfrom semantique.synth_corpus import items_synth\nt=time.time(); b= … [102 caractères tronqués]`

  ```
items 528 0.021274328231811523
synth 16662 0.23177146911621094
  ```

### 🤖 Assistant

⏵ Implémentation des têtes dorsales multiples, du contexte et des ablations

- **write** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py", "content": "#!/usr/bin/env python3\n\"\"\"M2 — deux voies : ventrale (quoi) et dorsale (où/comment).\n\nUn même encodeur de surface, **gelé**, alimente deux familles de têtes :\n\n- la voie **ventrale** lit l'**action** ;\n- la vo … [18707 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py</path>
<type>file</type>
<content>
Updated file
</content>
  ```

### 👤 Utilisateur

Agent f0969e87-af0c-43b1-93cf-f278d9c90846 sent a message: 
Timebox : donne un point de progression maintenant. Écris dès que possible /tmp/a3-m2.json et /tmp/a3-m2.md avec les chiffres obtenus, puis termine. Ne bloque pas sur une amélioration parfaite ; un négatif net suffit.

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "Point A3-M2 (en cours) : voies.py étendu (têtes de/vers/point/chemin_0, pools mean|last|mean+last, contexte RSN, lésions, splits vu/inédit). Constat déjà mesuré sur le M2 d'origine : les 93,2 % de `de` = 126/126 sur les surfaces normal … [309 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python /tmp/a3_timing.py", "description": "Validate default path after refactor", "timeoutMs": 900000}`

  ```
train 23.74737858772278 val 146
{'action': 0.9863013698630136, 'de': 0.9315068493150684, 'n': 146} eval 0.23407721519470215
{'action': 0.1232876712328767, 'de': 0.9315068493150684, 'n': 146}
{'action': 0.9863013698630136, 'de': 0.02054794520547945, 'n': 146}
[stderr]
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 971.00it/s]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat > /tmp/a3_quick.py <<'EOF'\nimport time, torch, json\nfrom transformers import AutoModelForCausalLM\nfrom cerveau.voies import entrainer, evaluer_champs\nfrom semantique.typed_corpus import items\n\nbase = AutoModelForCausalLM.from_pretrained(\"/t … [1161 caractères tronqués]`

  ```
train 50.38653206825256
eval 3.9327001571655273
de n 146 exact 0.9384 maj 0.4795 macro 0.3309 action 0.8973 lesions {'ventrale': {'action': 0.1781, 'de': 0.9384}, 'dorsale': {'action': 0.8973, 'de': 0.0137}}
vers n 146 exact 0.9452 maj 0.4726 macro 0.375 action 0.8973 lesions {'ventrale': {'action': 0.1781, 'vers': 0.9452}, 'dorsale': {'action': 0.8973, 'vers': 0.0342}}
point n 70 exact 0.9571 maj 0.9714 macro 0.6569 action 1.0 lesions {'ventrale': {'action': 0.0571, 'point': 0.9571}, 'dorsale': {'action': 1.0, 'point': 0.0571}}
chemin_0 n 70 exact 0.8429 maj 0.9714 macro 0.2892 action 0.7714 lesions {'ventrale': {'action': 0.0857, 'chemin_0': 0.8429}, 'dorsale': {'action': 0.7714, 'chemin_0': 0.0143}}
action_global 0.8636 lesions {'ventrale': 0.1307, 'dorsale': 0.8636}
de par classe {'52': (70, 1.0), '62': (68, 0.985), '60': (4, 0.0), '8': (2, 0.0), '28': (1, 0.0), '57': (1, 0.0)}
vers par classe {'36': (69, 1.0), '45': (68, 1.0), '0': (2, 0.0), '58': (2, 0.0), '62': (2, 0.0), '19': (1, 0.0), '42': (1, 0.0), '44': (1, 1.0)}
point par classe {'48': (68, 0.971), '30': (1, 0.0), '39': (1, 1.0)}
chemin_0 par classe {'8': (68, 0.868), '21': (1, 0.0), '9': (1, 0.0)}
[stderr]
Loading we
… [112 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py", "old_string": "            perte = F.cross_entropy(\n                va[:lot], _cibles(choix_action, \"action\", idx_action, device))", "new_string": "            # La voie ventrale voit tout le lot composite (tous les blocs ont\n … [262 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/voies.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat > /tmp/a3_quick2.py <<'EOF'\nimport time, torch\nfrom transformers import AutoModelForCausalLM\nfrom cerveau.voies import entrainer, evaluer_champs\nfrom semantique.typed_corpus import items\nbase = AutoModelForCausalLM.from_pretrained(\"/tmp/nati … [972 caractères tronqués]`

  ```
mean train 54.6 action 0.5 {'de': 0.4795, 'vers': 0.5, 'point': 0.0429, 'chemin_0': 0.8} macro {'de': 0.1667, 'vers': 0.2572, 'point': 0.0147, 'chemin_0': 0.6029}
last train 52.9 action 0.8106 {'de': 0.9452, 'vers': 0.9384, 'point': 0.9571, 'chemin_0': 0.9143} macro {'de': 0.3333, 'vers': 0.3732, 'point': 0.6569, 'chemin_0': 0.3137}
contexte train 122.4 action 0.9356 {'de': 0.9384, 'vers': 0.9384, 'point': 0.9571, 'chemin_0': 0.8286} macro {'de': 0.3309, 'vers': 0.3732, 'point': 0.6569, 'chemin_0': 0.2843}
[stderr]
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1054.79it/s]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat > /tmp/a3_probe.py <<'EOF'\nimport torch, torch.nn.functional as F, random\nfrom transformers import AutoModelForCausalLM\nfrom semantique.entrainer import pad\nfrom semantique.normalisation import normaliser\nfrom semantique.typed_corpus import i … [2191 caractères tronqués]`

  ```
mean norme moyenne 20.2 ecart-type entre exemples 0.193 moyenne norme 19.7
   linear probe std= False exact 0.8973
   linear probe std= True exact 0.8904
last norme moyenne 21.8 ecart-type entre exemples 0.296 moyenne norme 20.7
   linear probe std= False exact 0.9384
   linear probe std= True exact 0.9384
both norme moyenne 29.7 ecart-type entre exemples 0.244 moyenne norme 28.6
   linear probe std= False exact 0.9315
   linear probe std= True exact 0.911
[stderr]
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 944.09it/s]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat > /tmp/a3_probe2.py <<'EOF'\nimport torch, torch.nn.functional as F, random\nfrom transformers import AutoModelForCausalLM\nfrom semantique.entrainer import pad\nfrom semantique.normalisation import normaliser\nfrom semantique.typed_corpus import  … [1642 caractères tronqués]`

  ```
pas 300 exact 0.5068
pas 1000 exact 0.8904
pas 3000 exact 0.8904
[stderr]
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1098.12it/s]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat > /tmp/a3_long.py <<'EOF'\nimport sys, time, torch, json\nfrom transformers import AutoModelForCausalLM\nfrom cerveau.voies import entrainer, evaluer_champs\nfrom semantique.typed_corpus import items\nmode=sys.argv[1]; pas=int(sys.argv[2]); pool=s … [884 caractères tronqués]`

  ```
started background job bash-1497
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python /tmp/a3_long.py mean1000 1000 mean 0", "description": "Background mean-only 1000 steps", "run_in_background": true}`

  ```
started background job bash-1498
  ```

- **job_list** `{}`

  ```
bash-1497 [bash] running — cd /home/stephane/GitHub/Qtrinet && cat > /tmp/a3_long.py <<'EOF'
import sys, time, torch, json
from transformers import AutoModelForCausalLM
from cerveau.voies import entrainer, evaluer_champs
from semantique.typed_corpus import items
mode=sys.argv[1]; pas=int(sys.argv[2]); pool=sys.argv[3]; ctx=(sys.argv[4]=="1")
base = AutoModelForCausalLM.from_pretrained("/tmp/natif-600-512-8-align-s1", dtype=torch.float32)
F=("de","vers","point","chemin_0")
torch.manual_seed(1)
t=time.time()
m,val=entrainer(base,pas,32,64,1,"cuda",synth=True,champs=F,pool=pool,contexte=ctx)
r=evaluer_champs(m,items(),champs=F,device="cuda",lesions=True,retour_pred=False,graine=1)
print(json.dumps({"mode":mode,"pas":pas,"pool":pool,"contexte":ctx,"train_s":round(time.time()-t,1),
 "action":r["action_global"]["exact"],
 "fields":{n:{"exact":r[n]["exact"],"macro":r[n]["macro_rappel"],"n":r[n]["n"]} for n in F}}), flush=True)
EOF
PYTHONPATH=tools CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python /tmp/a3_long.py meanlast1000 1000 mean+last 0
bash-1498 [bash] running — cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python /tmp/
… [31 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-1497", "wait": false}`

  ```
[stderr]
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 939.82it/s]
[status: running]
  ```

- **job_output** `{"job_id": "bash-1498", "wait": false}`

  ```
[stderr]
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 1017.38it/s]
[status: running]
  ```

- **bash** `{"command": "cat > /tmp/a3_m2_driver.py <<'PYEOF'\n#!/usr/bin/env python3\n\"\"\"A3-M2 : champs dorsaux multiples, ablation du dernier état et du contexte.\"\"\"\nimport collections\nimport hashlib\nimport json\nimport math\nimport platform\nimport statistics\nimport time\n\nimport torch\nfrom trans … [28906 caractères tronqués]`

  ```
OK
  ```

### 👤 Utilisateur

background job bash-1497 (bash: cd /home/stephane/GitHub/Qtrinet && cat > /tmp/a3_long.py <<'EOF'
import sys, time, torch, json
from transformers import AutoModelForCausalLM
from cerveau.voies import entrainer, evaluer_champs
from semantique.typed_corpus import items
mode=sys.argv[1]; pas=int(sys.argv[2]); pool=sys.argv[3]; ctx=(sys.argv[4]=="1")
base = AutoModelForCausalLM.from_pretrained("/tmp/natif-600-512-8-align-s1", dtype=torch.float32)
F=("de","vers","point","chemin_0")
torch.manual_seed(1)
t=time.time()
m,val=entrainer(base,pas,32,64,1,"cuda",synth=True,champs=F,pool=pool,contexte=ctx)
r=evaluer_champs(m,items(),champs=F,device="cuda",lesions=True,retour_pred=False,graine=1)
print(json.dumps({"mode":mode,"pas":pas,"pool":pool,"contexte":ctx,"train_s":round(time.time()-t,1),
 "action":r["action_global"]["exact"],
 "fields":{n:{"exact":r[n]["exact"],"macro":r[n]["macro_rappel"],"n":r[n]["n"]} for n in F}}), flush=True)
EOF
PYTHONPATH=tools CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python /tmp/a3_long.py meanlast1000 1000 mean+last 0) finished [status: completed, exit code: 0]. Read its output with job_output.

### 👤 Utilisateur

background job bash-1498 (bash: cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python /tmp/a3_long.py mean1000 1000 mean 0) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-1497"}`

  ```
{"mode": "meanlast1000", "pas": 1000, "pool": "mean+last", "contexte": false, "train_s": 181.4, "action": 0.8731060606060606, "fields": {"de": {"exact": 0.9246575342465754, "macro": 0.32598039215686275, "n": 146}, "vers": {"exact": 0.9452054794520548, "macro": 0.375, "n": 146}, "point": {"exact": 0.9571428571428572, "macro": 0.6568627450980392, "n": 70}, "chemin_0": {"exact": 0.7857142857142857, "macro": 0.2696078431372549, "n": 70}}}
[status: completed, exit code: 0]
  ```

- **job_output** `{"job_id": "bash-1498"}`

  ```
{"mode": "mean1000", "pas": 1000, "pool": "mean", "contexte": false, "train_s": 183.9, "action": 0.7784090909090909, "fields": {"de": {"exact": 0.8972602739726028, "macro": 0.31624649859943976, "n": 146}, "vers": {"exact": 0.910958904109589, "macro": 0.36588874680306904, "n": 146}, "point": {"exact": 0.9428571428571428, "macro": 0.6519607843137255, "n": 70}, "chemin_0": {"exact": 0.8142857142857143, "macro": 0.6078431372549019, "n": 70}}}
[status: completed, exit code: 0]
  ```

- **send_message** `{"agent_id": "f0969e87-0f0c-43b1-93cf-f278d9c90846", "message": "A3-M2 — chiffres clés déjà obtenus (1 graine, mean+last, 300 pas) : `vers` 94,5 % (plafond 95,2 %), 126/126 surfaces vues, 12/13 inédites à classe couverte ; `de` 93,8 % (100 % vu, 12/13 inédit couvert) ; `point` 95,7 % < majorité 97,1 … [536 caractères tronqués]`

  ```
Error: subagent "f0969e87-0f0c-43b1-93cf-f278d9c90846" is unavailable
  ```

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "A3-M2 — chiffres clés déjà obtenus (1 graine, mean+last, 300 pas) : `vers` 94,5 % (plafond 95,2 %), 126/126 surfaces vues, 12/13 inédites à classe couverte ; `de` 93,8 % (100 % vu, 12/13 inédit couvert) ; `point` 95,7 % < majorité 97,1 … [536 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\nimport re\np='/tmp/a3_m2_driver.py'\ns=open(p).read()\ns=s.replace('''CONDITIONS = [\n    {\"key\": \"mean+last\", \"pool\": \"mean+last\", \"pas\": 300, \"contexte\": False},\n    {\"key\": \"mean-300\", \"pool\": \"mean\", \"pas\": 300, \"contexte\": Fals … [3250 caractères tronqués]`

  ```
patch ok
COMPILE_OK
  ```

- **bash** `{"command": "grep -n \"mean-1000\\|mean 1000\\|Ablations\\|Le piège\\|comparaisons.*mean\" /tmp/a3_m2_driver.py | head -40", "description": "Locate MD sections to patch"}`

  ```
333:    ad("## 5. Ablations du dernier état et du contexte\n")
336:    for key in ("mean+last", "mean-300", "mean-1000", "last"):
341:    ad("| champ | mean+last | mean 300 | mean 1000 | last 300 | Δ (mean 1000 − mean+last) |")
346:        m1 = cond["mean-1000"]["fields"][f]["exact_moyen"]
350:    ad("**Le piège d'optimisation.** À 300 pas, la moyenne seule paraît au hasard "
360:    cmp_last = j["comparaisons"]["mean-1000_vs_mean+last"]
361:    ad("| champ | Δ exact (mean 1000 − mean+last) | graines | McNemar groupé (b/c, p) |")
452:    ad("- Graines : %s ; pas : 300 (sauf `mean-1000`) ; lot 32 ; seq 64 ; seq contexte 192." % j["meta"]["seeds"])
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'EOF'\np='/tmp/a3_m2_driver.py'\ns=open(p).read()\nold='''    for key in (\"mean+last\", \"mean-300\", \"mean-1000\", \"last\"):\n        c = cond[key]\n        ad(f\"| `{key}` | {c['pas']} | {fmt(c['action_global']['exact_moyen'])} | \" +\n           \" | \".join … [3285 caractères tronqués]`

  ```
md patch ok
COMPILE_OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python /tmp/a3_m2_driver.py", "description": "Run 3-seed experiment driver", "run_in_background": true}`

  ```
started background job bash-1537
  ```

- **bash** `{"command": "cat > /tmp/a3-m2.json <<'EOF'\n{\n \"statut\": \"preliminaire — 1 graine, mean+last 300 pas ; passe 3 graines en cours, ce fichier sera écrasé\",\n \"meta\": {\n  \"base\": \"/tmp/natif-600-512-8-align-s1\",\n  \"gpu\": \"Quadro RTX 5000\",\n  \"encodeur\": \"gelé\",\n  \"n_synth\": 166 … [6122 caractères tronqués]`

  ```
JSON_OK
  ```

- **bash** `{"command": "cat > /tmp/a3-m2.md <<'EOF'\n# A3 — M2 : champs dorsaux multiples, dernier état et contexte\n\n_Préliminaire — 1 graine, `mean+last`, 300 pas. La passe 3 graines est en cours ;\nce fichier sera écrasé par la version finale._\n\n## 1. Protocole\n\n- Encodeur `route` **gelé** : `/tmp/nati … [7378 caractères tronqués]`

  ```
126 /tmp/a3-m2.md
# A3 — M2 : champs dorsaux multiples, dernier état et contexte

_Préliminaire — 1 graine, `mean+last`, 300 pas. La passe 3 graines est en cours ;
  ```

- **job_output** `{"job_id": "bash-1537", "wait": false}`

  ```
[10:10:31] mean+last graine 1 …
[stderr]
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 982.64it/s]
[status: running]
  ```

- **write** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_voies.py", "content": "from __future__ import annotations\n\nimport unittest\nfrom types import SimpleNamespace\n\nimport torch\nimport torch.nn as nn\n\nfrom cerveau.voies import Voies, entrainer, evaluer, evaluer_champs\nfrom se … [5096 caractères tronqués]`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_voies.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest cerveau.tests.test_voies -v 2>&1 | tail -40", "description": "Run new voies tests", "timeoutMs": 300000}`

  ```
test_contexte_melange_et_vide (cerveau.tests.test_voies.TestVoies.test_contexte_melange_et_vide) ... ok
test_entrainement_court (cerveau.tests.test_voies.TestVoies.test_entrainement_court) ... ok
test_evaluation_et_lesions (cerveau.tests.test_voies.TestVoies.test_evaluation_et_lesions) ... ok
test_formes_des_tetes (cerveau.tests.test_voies.TestVoies.test_formes_des_tetes) ... ok
test_le_contexte_change_le_code (cerveau.tests.test_voies.TestVoies.test_le_contexte_change_le_code) ... ok
test_pools (cerveau.tests.test_voies.TestVoies.test_pools) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.438s

OK
  ```

- **job_output** `{"job_id": "bash-1537", "wait": false}`

  ```
fait en 51.2s
[10:11:26] mean+last graine 2 …
    fait en 49.3s
[10:12:19] mean+last graine 3 …
[status: running]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nj=json.load(open('/tmp/a3-m2-partial.json'))\nprint(j.keys())\nfor k,v in j['conditions'].items():\n    print(k, list(v.keys()))\n    for s,r in v.items():\n        print(' ',s,'train_s',round(r['train_s'],1),'de',round(r['reel']['de']['exact'],4),'vers', … [201 caractères tronqués]`

  ```
dict_keys(['conditions'])
mean+last ['1', '2']
  1 train_s 51.2 de 0.9384 vers 0.9452 ok_len 146
   action_global 0.8731
  2 train_s 49.3 de 0.9315 vers 0.9452 ok_len 146
   action_global 0.875
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nj=json.load(open('/tmp/a3-m2-partial.json'))['conditions']['mean+last']\nfor s in sorted(j):\n    r=j[s]['reel']\n    print('seed',s)\n    for f in ('de','vers','point','chemin_0'):\n        x=r[f]\n        print(' ',f,'exact',round(x['exact'],4),'macro', … [347 caractères tronqués]`

  ```
seed 1
  de exact 0.9384 macro 0.3309 action 0.9178 lesions {'ventrale': {'action': 0.13, 'de': 0.938}, 'dorsale': {'action': 0.918, 'de': 0.014}}
  vers exact 0.9452 macro 0.375 action 0.9178 lesions {'ventrale': {'action': 0.13, 'vers': 0.945}, 'dorsale': {'action': 0.918, 'vers': 0.021}}
  point exact 0.9571 macro 0.6569 action 0.9857 lesions {'ventrale': {'action': 0.129, 'point': 0.957}, 'dorsale': {'action': 0.986, 'point': 0.0}}
  chemin_0 exact 0.8429 macro 0.2892 action 0.8143 lesions {'ventrale': {'action': 0.086, 'chemin_0': 0.843}, 'dorsale': {'action': 0.814, 'chemin_0': 0.029}}
 action_global 0.8731 {'ventrale': 0.1269, 'dorsale': 0.8731}
seed 2
  de exact 0.9315 macro 0.3285 action 0.9315 lesions {'ventrale': {'action': 0.137, 'de': 0.932}, 'dorsale': {'action': 0.932, 'de': 0.021}}
  vers exact 0.9452 macro 0.375 action 0.9315 lesions {'ventrale': {'action': 0.137, 'vers': 0.945}, 'dorsale': {'action': 0.932, 'vers': 0.0}}
  point exact 0.9571 macro 0.6569 action 0.9857 lesions {'ventrale': {'action': 0.171, 'point': 0.957}, 'dorsale': {'action': 0.986, 'point': 0.014}}
  chemin_0 exact 0.8286 macro 0.2843 action 0.8143 lesions {'ventrale': {'action': 0.1, 'chemin_0
… [119 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-1537", "wait": false}`

  ```
fait en 49.0s
[10:13:12] mean-300 graine 1 …
    fait en 49.6s
[10:14:05] last graine 1 …
[status: running]
  ```

- **job_output** `{"job_id": "bash-1537", "wait": true, "timeout_ms": 600000}`

  ```
fait en 49.4s
[10:14:58] last graine 2 …
    fait en 49.2s
[10:15:51] last graine 3 …
    fait en 49.7s
[10:16:45] contexte graine 1 …
    fait en 120.3s
[10:18:58] contexte graine 2 …
    fait en 121.6s
[10:21:13] contexte graine 3 …
    fait en 122.2s
écrit /tmp/a3-m2.json et /tmp/a3-m2.md en 803s
[status: completed, exit code: 0]
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

### 🤖 Assistant

⏵ Vérification des résultats 3 graines et du rapport final

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nj=json.load(open('/tmp/a3-m2.json'))\nprint(\"keys:\", list(j.keys()))\nprint(\"meta:\", {k:j['meta'][k] for k in ('date','seeds','pas','gpu','duree_s')})\nfor k,c in j['conditions'].items():\n    print(\"\\nCOND\",k,\"pool\",c['pool'],\"pas\",c['pas'],\" … [855 caractères tronqués]`

  ```
keys: ['meta', 'donnees', 'conditions', 'controle_1000_1_graine', 'comparaisons', 'negatifs', 'autocritique']
meta: {'date': '2026-10-27 10:23:27', 'seeds': [1, 2, 3], 'pas': 300, 'gpu': 'Quadro RTX 5000', 'duree_s': 803.0}

COND mean+last pool mean+last pas 300 ctx False seeds [1, 2, 3]
 action 0.8744 lesions {'ventrale': 0.1313, 'dorsale': 0.8744}
  de: exact 0.9361±0.0040 macro 0.3301 vu 1.000 inedit 0.533 inedit_couvert 0.821 n_in 20 n_inc 13 lesions {'ventrale': {'action': 0.1415525114155251, 'champ': 0.9360730593607306}, 'dorsale': {'action': 0.9269406392694064, 'champ': 0.02054794520547945}}
  vers: exact 0.9429±0.0040 macro 0.3744 vu 1.000 inedit 0.583 inedit_couvert 0.897 n_in 20 n_inc 13 lesions {'ventrale': {'action': 0.1415525114155251, 'champ': 0.9429223744292238}, 'dorsale': {'action': 0.9269406392694064, 'champ': 0.01141552511415525}}
  point: exact 0.9571±0.0000 macro 0.6569 vu 1.000 inedit 0.250 inedit_couvert 0.250 n_in 4 n_inc 4 lesions {'ventrale': {'action': 0.15714285714285714, 'champ': 0.9571428571428572}, 'dorsale': {'action': 0.9857142857142858, 'champ': 0.009523809523809523}}
  chemin_0: exact 0.8333±0.0082 macro 0.2859 vu 0.994 inedit 0.190 inedit_couvert
… [5491 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nj=json.load(open('/tmp/a3-m2.json'))\nc=j['conditions']['contexte']\nfor s,r in c.items() if False else []:\n    pass\n# per-seed data is not in final JSON (only aggregates), but partial has it\np=json.load(open('/tmp/a3-m2-partial.json'))['conditions'][' … [642 caractères tronqués]`

  ```
seed 1 train 120.3
  de: exact 0.9384 macro 0.3309 action 0.9863 par_classe {'52': {'n': 70, 'rappel': 1.0}, '62': {'n': 68, 'rappel': 0.9852941176470589}, '60': {'n': 4, 'rappel': 0.0}, '8': {'n': 2, 'rappel': 0.0}, '28': {'n': 1, 'rappel': 0.0}, '57': {'n': 1, 'rappel': 0.0}}
  vers: exact 0.9384 macro 0.3732 action 0.9863 par_classe {'36': {'n': 69, 'rappel': 0.9855072463768116}, '45': {'n': 68, 'rappel': 1.0}, '0': {'n': 2, 'rappel': 0.0}, '58': {'n': 2, 'rappel': 0.0}, '62': {'n': 2, 'rappel': 0.0}, '19': {'n': 1, 'rappel': 0.0}, '42': {'n': 1, 'rappel': 0.0}, '44': {'n': 1, 'rappel': 1.0}}
  point: exact 0.9571 macro 0.6569 action 1.0000 par_classe {'48': {'n': 68, 'rappel': 0.9705882352941176}, '30': {'n': 1, 'rappel': 0.0}, '39': {'n': 1, 'rappel': 1.0}}
  chemin_0: exact 0.8286 macro 0.2843 action 0.9000 par_classe {'8': {'n': 68, 'rappel': 0.8529411764705882}, '21': {'n': 1, 'rappel': 0.0}, '9': {'n': 1, 'rappel': 0.0}}
   melange {'de': 0.9384, 'vers': 0.9384, 'point': 0.9571, 'chemin_0': 0.8429} action 0.2519
   vide {'de': 0.9315, 'vers': 0.9452, 'point': 0.9571, 'chemin_0': 0.8429} action 0.4375
  action reel 0.9356
seed 2 train 121.6
  de: exact 0.9315 macro 0.3285 a
… [2256 caractères tronqués]
  ```

- **read** `{"file_path": "/tmp/a3-m2.md"}`

  ```
<path>/tmp/a3-m2.md</path>
<type>file</type>
<content>
1: # A3 — M2 : champs dorsaux multiples, dernier état et contexte
2: 
3: _Sprint autonome 24 h — sous-agent A3. Résultats mesurés sur GPU RTX 5000, encodeur `/tmp/natif-600-512-8-align-s1` gelé, `PYTHONPATH=tools`, `CUDA_VISIBLE_DEVICES=0`._
4: 
5: ## 1. Ce qui est mesuré
6: 
7: Le prototype M2 d'origine avait deux têtes linéaires sur un encodeur gelé : `action` (ventrale) et `de` (dorsale), entraînées sur les surfaces synthétiques (`items_synth`, 16662 items) et testées sur les 528 surfaces réelles (`items`). Ici, la voie dorsale est étendue à **quatre champs** : `de`, `vers`, `point`, `chemin_0`. Chaque tête est indépendante ; une lésion remplace ses logits par du bruit gaussien.
8: 
9: Trois ablations sont comparées, à nombre de pas égal (300) sauf mention :
10: 
11: - **`mean+last`** : moyenne masquée + dernier état (référence, comme M2) ;
12: - **`mean`** : moyenne seule (ablation du dernier état), à 300 pas **et** à 1 000 pas ;
13: - **`last`** : dernier état seul ;
14: - **`+contexte`** : moyenne + dernier état de la surface **et** du RSN de contexte, avec les mêmes têtes ; contexte réel, permuté ou vide à l'évaluation.

… [10997 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('/tmp/a3-m2-partial.json'))['conditions']['contexte']\nfor mode in ('reel','melange','vide'):\n    vals=[p[s][mode]['action_global']['exact'] for s in sorted(p)]\n    print(mode, vals, sum(vals)/len(vals))\nfor s in sorted(p):\n    print( … [200 caractères tronqués]`

  ```
reel [0.9356060606060606, 0.9356060606060606, 0.9356060606060606] 0.9356060606060606
melange [0.2518939393939394, 0.2935606060606061, 0.23674242424242425] 0.26073232323232326
vide [0.4375, 0.4356060606060606, 0.4356060606060606] 0.4362373737373737
seed 1 point reel 0.9571428571428572 point mel 0.9571428571428572 point vide 0.9571428571428572
seed 2 point reel 0.9428571428571428 point mel 0.9428571428571428 point vide 0.9428571428571428
seed 3 point reel 0.05714285714285714 point mel 0.2857142857142857 point vide 0.9428571428571428
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np='/tmp/a3-m2.json'\nj=json.load(open(p))\n# notes graines\nj['meta']['graines_par_condition']={\n  \"mean+last\":[1,2,3], \"mean-300\":[1], \"last\":[1,2,3],\n  \"contexte\":[1,2,3], \"controle_1000\":[1]}\nj['conditions']['mean-300']['note']=\"1 seule g … [3483 caractères tronqués]`

  ```
json patch ok
JSON_VALID
  ```

- **bash** `{"command": "python3 - <<'EOF'\np='/tmp/a3-m2.md'\ns=open(p).read()\nrepls = [\n(\"Trois ablations sont comparées, à nombre de pas égal (300) sauf mention :\",\n \"Quatre conditions sont comparées, à nombre de pas égal (300) sauf mention :\"),\n(\"*Lecture.* `vers` est **décodable** : 94,5 % global, … [7151 caractères tronqués]`

  ```
md patch ok
[exit code: 1]
  ```

- **bash** `{"command": "sed -n 29,40p /tmp/a3-m2.md; echo '---'; sed -n 53,95p /tmp/a3-m2.md; echo '---'; sed -n 96,125p /tmp/a3-m2.md", "description": "Verify patched MD"}`

  ```
## 3. Résultat principal (`mean+last`, 300 pas, 3 graines)

| champ | n | exact (moy ± é-t) | majorité | hasard | macro-rappel | vu | inédit | inédit couvert |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| `de` | 146 | 93.6 % ± 0.4 % | 47.9 % | 1.5 % | 33.0 % | 100.0 % (126) | 53.3 % (20) | 82.1 % (13) |
| `vers` | 146 | 94.3 % ± 0.4 % | 47.3 % | 1.5 % | 37.4 % | 100.0 % (126) | 58.3 % (20) | 89.7 % (13) |
| `point` | 70 | 95.7 % ± 0.0 % | 97.1 % | 1.2 % | 65.7 % | 100.0 % (66) | 25.0 % (4) | 25.0 % (4) |
| `chemin_0` | 70 | 83.3 % ± 0.8 % | 97.1 % | 1.5 % | 28.6 % | 99.4 % (56) | 19.0 % (14) | 20.5 % (13) |

*Lecture.* `vers` est **décodable** : 94,3 % global, 100 % sur les 126 surfaces vues, et 11,7/13 (89,7 %) sur les surfaces inédites dont la classe est couverte. Les 7 items de classes jamais vues (roque, `exd6`, promotion) sont nécessairement à 0 ; le plafond de couverture est 95,2 %. `de` reproduit le résultat d'origine (93,6 % contre 93,2 %). `point` est **non concluant** et `chemin_0` un **négatif net** (voir § 6).

## 4. Lésions ventrale / dorsale (`mean+last`, 3 graines)
---
## 5. Ablations du dernier état et du contexte

| condition | pas | action | de | vers | point | 
… [8244 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nj=json.load(open('/tmp/a3-m2.json'))\nprint(json.dumps(j['negatifs'],ensure_ascii=False,indent=1))\nprint(json.dumps(j['autocritique'],ensure_ascii=False,indent=1))\nprint(json.dumps(j['conditions']['contexte']['stabilite_point'],ensure_ascii=False,indent … [205 caractères tronqués]`

  ```
{
 "chemin_0": "83,3 % < majorité 97,1 % ; macro 0,286 < 1/3 ; inédit 19,0 % ; négatif net.",
 "point": "95,7 % < majorité 97,1 % ; macro 0,657 ; inédit 25 % ; non concluant (68/70 même classe).",
 "vers": "94,3 % ; plafond de couverture 95,2 % ; 7 items de classes inconnues à 0 ; inédit couvert 89,7 % (11,7/13).",
 "contexte": "Aucun gain dorsal ; le contexte aide l'action (93,6 % vs 87,4 %) comme identifiant de jeu, et le permuter fait tomber l'action à 26,1 %. La tête point du modèle contexte a divergé sur la graine 3 (5,7 %).",
 "de_global": "93,2 % d'origine = 126/126 sur surfaces vues + 10/20 sur inédites (3 graines) : chiffre global gonflé par le recouvrement de templates."
}
[
 "Le recouvrement de surfaces normalisées est de 86,3 % pour de/vers, 94,3 % pour point, 80 % pour chemin_0 : l'exactitude globale mesure surtout la mémoire de templates.",
 "À 300 pas, mean seul est sous-entraîné (variance inter-exemples faible) ; à 1 000 pas il atteint 89,7 % sur de. La comparaison à pas égal exagère le gain du dernier état ; à 1 000 pas le gain de mean+last sur mean est de 2,7 pts (de), 3,4 (vers), 1,4 (point), et -2,9 (chemin_0), sur 1 graine.",
 "La comparaison mean 1000 vs mean+
… [1657 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle final : chemin historique et tests unitaires

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools CUDA_VISIBLE_DEVICES=0 /home/stephane/gpu-env/bin/python /tmp/a3_timing.py 2>&1 | tail -8", "description": "Reconfirm legacy M2 path", "timeoutMs": 900000}`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights:  96%|█████████▌| 86/90 [00:00<00:00, 859.12it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 893.16it/s]
train 24.270405530929565 val 146
{'action': 0.9863013698630136, 'de': 0.9315068493150684, 'n': 146} eval 0.23089933395385742
{'action': 0.1232876712328767, 'de': 0.9315068493150684, 'n': 146}
{'action': 0.9863013698630136, 'de': 0.02054794520547945, 'n': 146}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools /home/stephane/gpu-env/bin/python -m unittest cerveau.tests.test_voies -v 2>&1 | tail -12", "description": "Rerun voies unit tests", "timeoutMs": 300000}`

  ```
test_contexte_melange_et_vide (cerveau.tests.test_voies.TestVoies.test_contexte_melange_et_vide) ... ok
test_entrainement_court (cerveau.tests.test_voies.TestVoies.test_entrainement_court) ... ok
test_evaluation_et_lesions (cerveau.tests.test_voies.TestVoies.test_evaluation_et_lesions) ... ok
test_formes_des_tetes (cerveau.tests.test_voies.TestVoies.test_formes_des_tetes) ... ok
test_le_contexte_change_le_code (cerveau.tests.test_voies.TestVoies.test_le_contexte_change_le_code) ... ok
test_pools (cerveau.tests.test_voies.TestVoies.test_pools) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.597s

OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sha256sum tools/cerveau/voies.py && python3 - <<'EOF'\nimport json, hashlib\nj=json.load(open('/tmp/a3-m2.json'))\nh=hashlib.sha256(open('tools/cerveau/voies.py','rb').read()).hexdigest()\nprint(\"json hash\", j['meta']['fichier_voies_sha256'])\nprint … [171 caractères tronqués]`

  ```
a531546e340f7ca416bf5d00a3d41ae328e9d327ffbe339fb3390f5590327691  tools/cerveau/voies.py
json hash a531546e340f7ca416bf5d00a3d41ae328e9d327ffbe339fb3390f5590327691
match True
-rw-r--r--. 1 stephane stephane  52807 27 oct 10:26 /tmp/a3-m2.json
-rw-r--r--. 1 stephane stephane  12927 27 oct 10:27 /tmp/a3-m2.md
-rw-r--r--. 1 stephane stephane 311113 27 oct 10:23 /tmp/a3-m2-partial.json
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np='/tmp/a3-m2.md'\ns=open(p).read()\nold=\"- **`chemin_0` reste au hasard, et même en dessous de la majorité** : 83,3 % global contre 97,1 % de majorité, macro-rappel 0,286 contre 1/3 au hasard.\"\nnew=\"- **`chemin_0` ne fait pas mieux qu'un prédicteur m … [628 caractères tronqués]`

  ```
patched
JSON_VALID
98:- **`chemin_0` ne fait pas mieux qu'un prédicteur majoritaire, et son macro-rappel est au niveau du hasard** : 83,3 % global contre 97,1 % de majorité, macro-rappel 0,286 contre 1/3 au hasard. Les surfaces réelles inédites (`9x18`, `b6xd4`, `b6-c5`, `10-14`…) ne sont pas lues. La classe 21 n'existe pas dans l'entraînement synthétique. C'est un négatif net, pas un manque de pas : à 1 000 pas la moyenne seule ne sauve pas le champ.
  ```

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "A3-M2 terminé.\n\nCODE : `tools/cerveau/voies.py` étendu (têtes dorsales multiples `de`/`vers`/`point`/`chemin_0`, pools `mean`/`last`/`mean+last`, contexte RSN, lésions, `evaluer_champs`) ; `tools/cerveau/tests/test_voies.py` ajouté ( … [2391 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

### 🤖 Assistant

⏵ Bilan M2 : vers décodable, point/chemin négatifs, rapport écrit

## Ce qui a été fait

- `tools/cerveau/voies.py` étendu : têtes dorsales multiples (`de`, `vers`, `point`, `chemin_0`), pools `mean` / `last` / `mean+last`, contexte RSN, lésions ventrale/dorsale, évaluation par champ et split vu/inédit.
- `tools/cerveau/tests/test_voies.py` ajouté : 6 tests, tous verts.
- Livrables : **`/tmp/a3-m2.json`**, **`/tmp/a3-m2.md`** (brut : `/tmp/a3-m2-partial.json`).
- Le chemin historique M2 reproduit exactement : `action` 98,63 %, `de` 93,15 %, n = 146.

## Chiffres principaux (`mean+last`, 300 pas, 3 graines)

| champ | n | exact | majorité | macro | surfaces vues | inédit couvert |
|---|---:|---:|---:|---:|---:|---:|
| `vers` | 146 | **94,3 %** ± 0,4 | 47,3 % | 37,4 % | 100 % (126) | 89,7 % (11,7/13) |
| `de` | 146 | **93,6 %** ± 0,4 | 47,9 % | 33,0 % | 100 % (126) | 82,1 % (10,7/13) |
| `point` | 70 | 95,7 % | **97,1 %** | 65,7 % | 100 % (66) | 25,0 % (1/4) |
| `chemin_0` | 70 | 83,3 % | **97,1 %** | **28,6 %** | 99,4 % (56) | 20,5 % (2,7/13) |

- `vers` est décodable ; son plafond de couverture est 95,2 % (7 items de classes jamais vues : roque, `exd6`, promotion).
- `point` est **non concluant** (sous la majorité, 68/70 items de la même classe).
- `chemin_0` est un **négatif net** : sous la majorité, macro-rappel au niveau du hasard.
- Lésions : ventrale → action 13-14 % (hasard 12,5 %), champs dorsaux intacts ; dorsale → champs 1-2 % (hasard 1,2-1,5 %), action intacte. Double dissociation nette, mais architecturale.

## Ablations

- `mean` seul à 300 pas s'effondre (de 47,9 %, vers 50,0 %, point 4,3 %) par **sous-entraînement**, pas par absence d'information. À 1 000 pas : 89,7 / 91,1 / 94,3 / 81,4 ; `mean+last` à 1 000 pas : 92,5 / 94,5 / 95,7 / 78,6 (1 graine). Gain honnête du dernier état : **~+2,7 / +3,4 / +1,4 / −2,9 pts**.
- `last` seul égale `mean+last` sur `de`/`vers`/`point` et le dépasse sur `chemin_0` : la moyenne n'ajoute rien, voire nuit.
- Contexte : **aucun gain dorsal** ; il aide l'action comme identifiant de jeu (93,6 % vs 87,4 %), avec chute à 26,1 % si le contexte est permuté. La tête `point` en contexte a divergé sur une graine (5,7 %), moyenne non interprétable.

## Autocritique majeure

Le 93,2 % d'origine sur `de` est **126/126 sur les surfaces déjà vues** et **10/20 sur les inédites** (3 graines : 10, 11, 10). Recouvrement des surfaces normalisées : 86,3 % (`de`/`vers`), 94,3 % (`point`), 80 % (`chemin_0`). Les chiffres globaux mesurent surtout la mémoire de templates ; la mesure utile est le split vu/inédit. Limites : n = 146/70, classes rares à n = 1, une seule graine pour le contrôle 1000, têtes indépendantes, contexte synthétique constant par jeu.

## Contraintes

Seuls `tools/cerveau/voies.py` et `tools/cerveau/tests/test_voies.py` ont été modifiés. Aucun `git`, aucune modification de `batterie.py`, docs, reports ou journal.

