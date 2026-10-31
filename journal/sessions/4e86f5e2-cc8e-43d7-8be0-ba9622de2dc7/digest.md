# Session DSH — relecture

- identifiant : `4e86f5e2-cc8e-43d7-8be0-ba9622de2dc7`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 14:55:19
- agent : standard


## Tour 1

### 👤 Utilisateur

Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A15 : compléter M9 par des **lésions croisées et des contrôles sham** sur les modules réels, sans modifier les modules existants.

État :
- `tools/cerveau/lesion.py` : `batterie_lesions()` CPU (M1 contexte, M2 proxy, M3, M4, M5, M6, M7, M8) ; M2 réel `voies.py` validé (action 98,63→12,33, de 91,78→2,05).
- M2 `voies.py`, M5 `predictif.py`, M6 `gating.py`, M8 `sommeil.py`, M9.
- Tests : `PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools` → 126 OK.

Objectif :
1. Créer `tools/cerveau/lesion_complet.py` : lésions **une par module** et **doubles lésions** (M2+M5, M2+M6, M5+M6), avec **sham** (même opération sans effet) et **dose-réponse** (capacité 0/4/8/12/16, contexte 0/25/50/75/100 %).
2. Mesurer les déficits `intacte − lésée`, la **double dissociation** M2 ventrale/dorsale et M5 plateau/transitions, et la **récupération** après restauration.
3. Écrire `/tmp/a15-m9-complet.json` et `.md` ; si une lésion n'a aucun effet, le dire.

Contraintes :
- Crée uniquement `tools/cerveau/lesion_complet.py` et `tools/cerveau/tests/test_lesion_complet.py` ; ne modifie pas les modules existants, docs, reports, journal, `batterie.py`, git.
- Pas de `git add/commit/checkout`.
- CPU/GPU si nécessaire (`CUDA_VISIBLE_DEVICES=0`). Sois autonome, timebox, autocritique. Réponds avec un résumé et les chemins.
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

⏵ Exploring the existing brain modules and lesion battery

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls && echo \"---\" && ls tools/cerveau && echo \"---\" && ls tools/cerveau/tests", "description": "List repo and cerveau directory"}`

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
---
__init__.py
__pycache__
test_bus.py
test_episodique.py
test_gating.py
test_lesion.py
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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/cerveau/*.py tools/cerveau/tests/*.py 2>/dev/null | tail -40", "description": "Count lines in cerveau modules"}`

  ```
225 tools/cerveau/batterie.py
    51 tools/cerveau/bus.py
    90 tools/cerveau/episodique.py
   707 tools/cerveau/gating.py
    47 tools/cerveau/hub.py
     0 tools/cerveau/__init__.py
   726 tools/cerveau/lesion.py
    84 tools/cerveau/memoire_travail.py
  1130 tools/cerveau/multilingue.py
  1138 tools/cerveau/neuromodulation.py
    69 tools/cerveau/pipeline_memoire.py
    46 tools/cerveau/pipeline.py
   903 tools/cerveau/pipeline_semantique_m2.py
   125 tools/cerveau/pipeline_semantique.py
   575 tools/cerveau/predictif.py
    59 tools/cerveau/restitution.py
   114 tools/cerveau/sequences.py
   972 tools/cerveau/sommeil.py
   737 tools/cerveau/voies.py
     0 tools/cerveau/tests/__init__.py
    29 tools/cerveau/tests/test_bus.py
    81 tools/cerveau/tests/test_episodique.py
   160 tools/cerveau/tests/test_gating.py
   127 tools/cerveau/tests/test_lesion.py
   119 tools/cerveau/tests/test_memoire_travail.py
    24 tools/cerveau/tests/test_modules.py
   229 tools/cerveau/tests/test_multilingue.py
   148 tools/cerveau/tests/test_neuromodulation.py
    24 tools/cerveau/tests/test_pipeline_memoire.py
    27 tools/cerveau/tests/test_pipeline.py
   151 tools/cerveau/tests/test_pipeline_
… [260 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/lesion.py</path>
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
20: - **M5** : reti
… [35927 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== voies.py ===\" && grep -n \"^class \\|^def \\|^    def \" tools/cerveau/voies.py && echo \"=== predictif.py ===\" && grep -n \"^class \\|^def \\|^    def \" tools/cerveau/predictif.py && echo \"=== gating.py ===\" && grep  … [219 caractères tronqués]`

  ```
=== voies.py ===
63:def _normaliser(texte: str) -> str:
68:def normaliser_coordonnees(texte: str) -> str:
95:def _san_francais(san: str) -> str:
103:class Voies(nn.Module):
108:    def __init__(self, base: nn.Module, champs_dorsaux=("de",),
138:    def dorsal(self) -> nn.Linear:
142:    def _pool(self, h: torch.Tensor, masque: torch.Tensor) -> torch.Tensor:
154:    def encode(self, ids, masque, ctx_ids=None, ctx_masque=None):
165:    def logits(self, ids, masque, ctx_ids=None, ctx_masque=None):
170:def _lot(items_, lot, seq, rng, normaliseur=None):
176:def _entrees(mor, seq, seq_ctx, contexte, contextes=None, normaliseur=None):
192:def _cibles(choix, nom, idx, device):
197:def _aleatoire_like(t: torch.Tensor, g: torch.Generator) -> torch.Tensor:
215:def _positions_echecs(n: int, graine: int):
236:def _positions_dames(n: int, graine: int):
252:def _textes_echecs(pos, coup):
298:def _textes_dames(coup):
324:def _textes_go(point: int):
342:def augmenter(champs=CHAMPS_DORSAUX, familles=("formes",), positions: int = 0,
362:    def ajoute(texte, r, code, famille, langue, contexte):
424:def entrainer(base, pas: int = 400, lot: int = 32, seq: int = 64, graine: int = 1,
546:def _stats_class
… [4778 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls /tmp/natif-600-512-8-align-s1 2>/dev/null | head; echo \"---\"; nvidia-smi --query-gpu=name,memory.free --format=csv,noheader 2>/dev/null; echo \"---\"; python3 -c \"import torch, transformers; print(torch.__version__, torch.cuda. … [120 caractères tronqués]`

  ```
config.json
generation_config.json
model.safetensors
---
Quadro RTX 5000, 15927 MiB
Quadro RTX 5000, 15927 MiB
---
    ^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'torch'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && which python3 && ls /home/stephane | head -30 && ls ~/.venvs 2>/dev/null; ls -d /home/stephane/*venv* /home/stephane/*conda* 2>/dev/null; echo \"---\"; cat /tmp/natif-600-512-8-align-s1/config.json | head -c 600", "description": "Loc … [32 caractères tronqués]`

  ```
/usr/bin/python3
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
intelFPGA_std
iverilog
lib64_shim
lvm-cache-backup-20251222-131716
Modèles
Mozilla-Recovery-Key_2026-08-13_stephane.denis.69@gmail.com.pdf
Music
Musique
nltk_data
package(1).zip
package(2).zip
---
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
  "num_local_exp
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for p in python python3.11 python3.12 /usr/bin/python3; do echo \"== $p\"; $p -c \"import torch; print(torch.__version__, torch.cuda.is_available())\" 2>&1 | tail -1; done; echo \"---\"; find /home/stephane -maxdepth 4 -name \"activa … [95 caractères tronqués]`

  ```
== python
bash: line 1: python: command not found
== python3.11
bash: line 1: python3.11: command not found
== python3.12
bash: line 1: python3.12: command not found
== /usr/bin/python3
ModuleNotFoundError: No module named 'torch'
---
/home/stephane/transcription/.venv/bin/activate
/home/stephane/IA/venv-drave/bin/activate
  ```

- **bash** `{"command": "/home/stephane/IA/venv-drave/bin/python -c \"import torch, transformers; print(torch.__version__, torch.cuda.is_available(), transformers.__version__)\" 2>&1 | tail -2; echo \"---\"; /home/stephane/IA/venv-drave/bin/python -c \"import numpy; print(numpy.__version__)\" 2>&1 | tail -1", " … [42 caractères tronqués]`

  ```
2.14.1+cu130 True 5.20.1
---
2.5.4
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py</path>
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
32:   
… [4908 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/voies.py", "offset": 95, "limit": 120}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/voies.py", "offset": 424, "limit": 230}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/voies.py</path>
<type>file</type>
<content>
95: def _san_francais(san: str) -> str:
96:     """SAN anglais → SAN français (R roi, D dame, T tour, F fou, C cavalier)."""
97:     if not san or san.startswith(("O-O", "o-o", "0-0")):
98:         return san
99:     table = {"K": "R", "Q": "D", "R": "T", "B": "F", "N": "C"}
100:     return table.get(san[0], san[0]) + san[1:]
101: 
102: 
103: class Voies(nn.Module):
104:     """Encodeur gelé + têtes ventrales/dorsales indépendantes."""
105: 
106:     nom = "M2-voies"
107: 
108:     def __init__(self, base: nn.Module, champs_dorsaux=("de",),
109:                  pool: str = "mean+last", contexte: bool = False):
110:         super().__init__()
111:         if pool not in POOLS:
112:             raise ValueError(f"pool inconnu : {pool!r} (attendu : {POOLS})")
113:         champs = tuple(champs_dorsaux)
114:         if not champs:
115:             raise ValueError("il faut au moins un champ dorsal")
116:         for nom in champs:
117:             if nom not in VALEURS:
118:                 raise ValueError(f"champ dorsal inconnu : {nom!r}")
119:         self.base = base
120
… [4827 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/voies.py</path>
<type>file</type>
<content>
424: def entrainer(base, pas: int = 400, lot: int = 32, seq: int = 64, graine: int = 1,
425:               device: str = "cuda", synth: bool = False, champs=None,
426:               pool: str = "mean+last", contexte: bool = False, seq_ctx: int = 192,
427:               augmentation=False, familles=("formes",), positions: int = 0,
428:               exclure_surfaces=None, normaliseur=None):
429:     """Entraîne les têtes sur les surfaces synthétiques.
430: 
431:     `champs` est la liste des champs dorsaux à apprendre. Par défaut `("de",)`,
432:     ce qui reproduit le prototype d'origine (une seule tête dorsale).
433: 
434:     Pour plusieurs champs, chaque pas forme un lot composite : un bloc d'items
435:     par champ (et un bloc d'action), une seule passe avant, et une perte par
436:     tête calculée sur son bloc. L'encodeur étant gelé, c'est équivalent à des
437:     passes séparées ; c'est simplement plus rapide.
438: 
439:     `augmentation` : `False` (défaut, comportement A3), `True` (familles
440:     `familles`) ou un tuple de familles (`"formes"`, `"positions"`
… [10681 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py", "limit": 260, "offset": 55}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py", "limit": 180, "offset": 315}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py</path>
<type>file</type>
<content>
55: def valeur(pas, cible: str = "cible"):
56:     """La valeur de la cible pour un pas (ou un code typé).
57: 
58:     `pas` peut être un `Pas` (attribut `.code`) ou directement le dictionnaire
59:     du code. Rend `None` quand la cible n'a pas de sens pour ce jeu (un go n'a
60:     pas de case de départ).
61:     """
62:     code = getattr(pas, "code", pas)
63:     if not isinstance(code, dict):
64:         raise TypeError("valeur attend un Pas ou un code typé (dict)")
65:     jeu = code.get("jeu")
66:     if cible == "action":
67:         return code.get("action")
68:     if cible == "source":
69:         champ = CHAMPS_SOURCE.get(jeu)
70:         return code.get(champ) if champ else None
71:     if cible == "cible":
72:         if jeu == "echecs":
73:             return code.get("vers")
74:         if jeu == "dames":
75:             for champ in ("chemin_2", "chemin_1", "chemin_0"):
76:                 if code.get(champ) is not None:
77:                     return code[champ]
78:             return None
79:         if jeu == "go":
80:             return code.get(
… [11212 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py</path>
<type>file</type>
<content>
315:         dist = self.distribution(jeu, cur, precedent, contexte)
316:         if not dist:
317:             return None, 0.0
318:         choix = self._choix(dist, jeu, contexte)
319:         return choix, dist[choix]
320: 
321:     # ------------------------------------------------------------------
322:     def evaluer(self, sequences) -> dict:
323:         """Exactitude, baseline majoritaire, surprisal et n sur des séquences.
324: 
325:         Ne prédit que les pas 1..n-1 : le premier pas n'a pas de passé. Les pas
326:         dont la cible est absente (source d'un go) sont ignorés.
327:         """
328:         n = ok = base = hors_vocab = 0
329:         surprise: list[float] = []
330:         surprise_base: list[float] = []
331:         for seq in sequences:
332:             pas = seq.pas
333:             for i in range(1, len(pas)):
334:                 b = pas[i]
335:                 y = valeur(b, self.cible)
336:                 cur = valeur(pas[i - 1], self.cible)
337:                 if y is None or cur is None:
338:                     continue
339:   
… [7981 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/pipeline.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "limit": 180}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/pipeline.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """pipeline.py — la chaîne minimale M1 → M4 → M8, sur un seul bus.
3: 
4: Le pipeline ne prétend pas être un cerveau : il vérifie que les modules se
5: **chaînent** sans se contredire. La surface est perçue par M1, stockée par M4,
6: résumée par M8 ; la lecture d'un code partiel passe par M4 et, si M8 a consolidé,
7: par ses prototypes.
8: """
9: from __future__ import annotations
10: 
11: from .bus import Bus
12: from .episodique import Episodique
13: from .hub import Hub
14: from .sommeil import Sommeil
15: 
16: 
17: class Pipeline:
18:     nom = "pipeline-M1-M4-M8"
19: 
20:     def __init__(self) -> None:
21:         self.bus = Bus()
22:         self.hub = Hub(self.bus)
23:         self.memoire = Episodique()
24:         self.sommeil = Sommeil()
25:         self.prototypes = {}
26: 
27:     def percevoir(self, texte: str, jeu: str, contexte=None, langue: str = "?"):
28:         code = self.hub.percevoir(texte, jeu, contexte)
29:         if code is not None:
30:             self.memoire.stocker(texte, code, langue)
31:         return code
… [714 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """pipeline_semantique_m2.py — B13 + M2 : la chaîne M1 → M2 → M5 → M6.
3: 
4: Ce module est un **test d'intégration**, pas un nouveau module de perception.
5: Il branche les briques existantes sur un seul flux et mesure chaque étage sur
6: son propre banc :
7: 
8: - **M1** (`hub.py`) lit la surface et rend le code typé ; la mesure est le code
9:   exact sur les 528 surfaces réelles, avec et sans contexte ;
10: - **M2** (`voies.py`) relit la surface et rend les champs dorsaux `de`/`vers`
11:   (encodeur natif gelé, têtes linéaires) ; la mesure est l'exactitude de champ
12:   sur les 146 items réels qui portent `de`/`vers`, découpée en surfaces **vues**
13:   (forme normalisée présente dans l'entraînement synthétique) et **inédites**,
14:   avec les lésions ventrale/dorsale ;
15: - **M5** (`predictif.py`) prédit la source/la cible du pas suivant avec le
16:   plateau ; la mesure est l'exactitude et la surprisal sur un split 80/20 par
17:   partie, avec le plateau et sans lui ;
18: - **M6** (`gating.py`) sélectionne la tâche ; la
… [6918 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py", "limit": 260, "offset": 181}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/gating.py", "limit": 160, "offset": 151}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/pipeline_semantique_m2.py</path>
<type>file</type>
<content>
181:     # ---- M2 ---------------------------------------------------------
182:     def coder_voies(self, texte: str, jeu: str, contexte=None,
183:                     seq: int = 64, seq_ctx: int = 192) -> dict | None:
184:         """M2 : surface (+ contexte) → champs ventraux/dorsaux.
185: 
186:         Rend `None` si aucun modèle M2 n'est branché. Les clés sont celles de
187:         `VALEURS` : `action` et chaque champ dorsal du modèle. `contexte` peut
188:         être un RSN (il est résumé) ou directement le résumé textuel.
189:         """
190:         if self.voies is None:
191:             return None
192:         if isinstance(contexte, RSN):
193:             contexte = resume_contexte(contexte)
194:         elif contexte is None:
195:             contexte = ""
196:         device = _device_de(self.voies)
197:         x, masque, c, cm = _entrees_voies(self.voies, [texte], [contexte],
198:                                           seq=seq, seq_ctx=seq_ctx)
199:         self.voies.eval()
200:         with torch.no_grad():
201:             va, vd
… [10705 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/gating.py</path>
<type>file</type>
<content>
151: class Porte:
152:     """La porte : deux canaux (langue, sens) et une règle de conjonction."""
153: 
154:     nom = "M6-gating"
155:     LANGUES = ("fr", "en")
156: 
157:     def __init__(self) -> None:
158:         self._cache_lecture: dict[tuple[str, str], dict | None] = {}
159:         self._cache_langue: dict[str, str | None] = {}
160: 
161:     # ------------------------------------------------------------------
162:     # Les deux canaux perceptifs.
163:     # ------------------------------------------------------------------
164:     def langue(self, texte: str) -> str | None:
165:         """Canal langue, **déterministe**.
166: 
167:         On combine deux readouts : le lexique fr/en (`langue_probable`, qui
168:         tranche les formes fléchies) puis un vote sur le lexique multilingue des
169:         domaines de jeu, départagé par ordre alphabétique. Le canal MULTI global
170:         (`MULTI.detecte_langue`) n'est **pas** déterministe sur les surfaces
171:         ambiguës — il itère des ensembles dont l'ordre dépend de
172:         `PYTHONHASHSEED` ; 
… [7491 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/gating.py", "limit": 190, "offset": 518}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/gating.py", "limit": 60, "offset": 60}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/gating.py</path>
<type>file</type>
<content>
518: 
519:     # ------------------------------------------------------------------
520:     # Politiques et mesures.
521:     # ------------------------------------------------------------------
522:     def _decisions(self, essais, politique: str = "conjonction",
523:                    langues_forcees: list[str | None] | None = None) -> list[dict]:
524:         decisions = []
525:         for i, essai in enumerate(essais):
526:             code = self.lire(essai.texte, essai.jeu, essai.contexte)
527:             langue = self.langue(essai.texte)
528:             forcee = langues_forcees[i] if langues_forcees is not None else None
529:             if politique == "conjonction":
530:                 accepte = code == essai.cible_code and langue == essai.cible_langue
531:             elif politique == "langue":
532:                 accepte = langue == essai.cible_langue
533:             elif politique == "sens":
534:                 accepte = code == essai.cible_code
535:             elif politique == "perseveration":
536:                 reference = forcee if forcee is 
… [9713 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/gating.py</path>
<type>file</type>
<content>
60: class Essai:
61:     """Un essai de la tâche : la sonde, la cible et la bonne réponse."""
62: 
63:     texte: str
64:     jeu: str
65:     langue_vraie: str
66:     code_vrai: dict
67:     cible_code: dict
68:     cible_langue: str
69:     condition: str
70:     contexte: object
71: 
72:     @property
73:     def attendu(self) -> bool:
74:         return self.condition == "go"
75: 
76: 
77: @dataclass(frozen=True)
78: class EssaiTache:
79:     """Un essai de la tâche de commutation : sonde, cible, indice de tâche.
80: 
81:     `tache` est la **consigne** (ce que la porte doit juger) ; `condition` dit
82:     si les deux canaux sont d'accord (`congruent`) ou non (`incongruent`).
83:     `transition` vaut `initiale`, `repetition` ou `commutation` selon le bloc
84:     précédent. La bonne réponse dépend de la consigne, jamais de l'accord.
85:     """
86: 
87:     texte: str
88:     jeu: str
89:     langue_vraie: str
90:     code_vrai: dict
91:     cible_code: dict
92:     cible_langue: str
93:     tache: str
94:     condition: str
95:     transition: str
96:     tache_p
… [1018 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"double dissociation\\|double_dissociation\\|dissociation\" --include=\"*.py\" --include=\"*.md\" tools reports docs | head -40", "description": "Search for existing double dissociation work"}`

  ```
tools/cerveau/tests/test_lesion.py:29:    def test_m2_double_dissociation(self):
tools/cerveau/tests/test_lesion.py:31:        self.assertTrue(m2["deficit"]["double_dissociation"])
tools/cerveau/voies.py:11:toucher les autres. C'est la double dissociation minimale, étendue à plusieurs
tools/cerveau/lesion.py:144:    """Substitut CPU : deux têtes bayésiennes, même dissociation structurelle."""
tools/cerveau/lesion.py:204:         "double_dissociation": (a - a_rand) > 0.2 and (d_nn - d_rand_nn) > 0.2},
tools/cerveau/lesion.py:287:         "double_dissociation": ((a - a_v) > 0.2 and (d - d_d) > 0.2
tools/cerveau/lesion.py:324:                      "dissociation, il ne remplace pas le module M2")
tools/cerveau/lesion.py:676:            "M2_double_dissociation": m2r["deficit"]["double_dissociation"],
reports/rapport-cerveau-modules.md:42:| **M2** | `action` **0,9863** ; `de` **0,9315** (n=146) ; lésion ventrale `action` **0,0959**, `de` **0,9315** ; lésion dorsale `action` **0,9863**, `de` **0,0068** | ✅ double dissociation |
reports/rapport-cerveau-modules.md:77:- **M2** est **valide** : la double dissociation est nette (`de` 93,2 %, lésion dorsale 0,7 %, lésion
reports/README.md:38:| 
… [1945 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"lesion_complet\\|A15\\|a15\" --include=\"*.py\" --include=\"*.md\" . 2>/dev/null | grep -v \".git/\" | head -30", "description": "Search for A15 references"}`

  ```
./tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/idna/idnadata.py:1592:        0xFA130000FA15,
./tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/idna/idnadata.py:1650:        0x10A1500010A18,
./tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/idna/uts46data.py:4256:        0xFA15,
./tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/idna/uts46data.py:5638:        0x10A15,
./tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/idna/uts46data.py:8370:        0x2FA15,
./tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/unistring.py:28:Lo = '\xaa\xba\u01bb\u01c0-\u01c3\u0294\u05d0-\u05ea\u05ef-\u05f2\u0620-\u063f\u0641-\u064a\u066e-\u066f\u0671-\u06d3\u06d5\u06ee-\u06ef\u06fa-\u06fc\u06ff\u0710\u0712-\u072f\u074d-\u07a5\u07b1\u07ca-\u07ea\u0800-\u0815\u0840-\u0858\u0860-\u086a\u08a0-\u08b4\u08b6-\u08bd\u0904-\u0939\u093d\u0950\u0958-\u0961\u0972-\u0980\u0985-\u098c\u098f-\u0990\u0993-\u09a8\u09aa-\u09b0\u09b2\u09b6-\u09b9\u09bd\u09ce\u09dc-\u09dd\u09df-\u09e1\u09f0-\u09f1\u09fc\u0a05-\u0a0a\u0a0f-\u0a10\u0a13-\u0a28\u0a2a-\u0a30\u0a32-\u0a33\u0a35-\u0a36\u0a38-\u0a39\u0a59-\u0a5c\u0a5e\u0a72-\u0a74\u0a85
… [48730 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,110p' reports/rapport-cerveau-modules.md", "description": "Read brain modules report"}`

  ```
# Rapport — modules cerveau-langage M1–M9

> **Objet.** Mesurer les neuf modules du prototype Python, sur les corpus B5/B7 et des parties générées
> par les règles. Aucun résultat n'est extrapolé au moteur Rust ni à un cerveau biologique.
>
> **Correction importante (27/10).** Les chiffres M2–M8 de cette fiche sont les **premiers**, avant le stress
> des sous-agents. Ils sont **gonflés par les doublons, les constantes et les templates**. Lire
> [`rapport-cerveau-corrections.md`](rapport-cerveau-corrections.md) : M1 reste solide, M2 est vu/inédit,
> M3/M4/M5/M6/M7/M8 sont structurels ou négatifs.

## 1. Dispositif

- **Bus** : événements typés, journal, rejeu.
- **M1** : codec + contexte, code RSN typé.
- **M2** : encodeur `route` gelé, deux têtes (jeu / de), **300 pas sur les surfaces synthétiques**, test sur les 146 surfaces réelles.
- **M3–M8** : structures déterministes, sans gradient.
- **Séquences** : 160 parties (échecs, dames, go, morpion), 12 pas, générées par les règles.
- **Corpus** : 528 coups B5/B7.
- **M9** : privations déclarées.

## 1 bis. La chaîne M1 → M4 → M8

Le pipeline `tools/cerveau/pipeline.py` enchaîne les modules sur un seul bus :
M1 perçoit, M4 stocke, M8 
… [4250 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls sprints | tail -5; grep -rn \"A15\\|lésions croisées\\|sham\" sprints docs/roadmap.md 2>/dev/null | head -30", "description": "Find sprint A15 context"}`

  ```
27-la-porte-p1-fermee-et-la-bascule-vers-kimi-k3.md
28-la-bascule-vers-kimi-k3-et-deux-defauts-de-tokenizer.md
29-87-go-par-jeton-et-la-recurrence-du-kda.md
30-la-reutilisation-des-experts-mesuree.md
31-le-regroupement-par-experts-mesure-et-k3-au-complet.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '440,903p' tools/cerveau/pipeline_semantique_m2.py | grep -n \"^def \\|^class \\|    def \\|experience\\|M2\\|M5\\|M6\" | head -80", "description": "Scan rest of pipeline M2 module"}`

  ```
6:# M2 : entraînement (avec cache de têtes) et évaluation
8:def _cle_cache(config: dict) -> str:
13:def _train_m2(base, pas: int, graine: int, contexte: bool, lot: int = 32,
16:    """Entraîne M2 sur les surfaces synthétiques, ou recharge les têtes du cache."""
51:def _mesurer_m2(m, items_, synth, contexte_mode: str = "reel",
80:def mesurer(pas: int = 300, graines=(1, 2, 3), device: str = "cuda",
90:    `Porte`). Les seules fonctions locales sont le rebranchissement (M2 →
111:    p = PipelineSemantiqueM2(voies=None, device=device)
138:    # ---- M2 : entraînement des deux conditions ----------------------
148:    # ---- M2 : évaluation par condition ------------------------------
171:    # ---- Chaîne : M1 seul, M1 remplacé par M2, M1 sans contexte -----
172:    # Le seul point où M2 peut agir est le champ dorsal : on compare les trois
194:            # secours oracle : M2 corrige-t-il les erreurs de M1 sans contexte ?
216:    # ---- M5 ---------------------------------------------------------
270:    # ---- M6 ---------------------------------------------------------
282:        "M2": {},
283:        "M5": {},
289:        m9["M2"][champ] = {
301:            m9["M5"][f"{cible}_{nom
… [2220 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' tools/cerveau/sequences.py && echo \"---\" && sed -n '1,60p' tools/cerveau/sommeil.py", "description": "Read sequences and sommeil headers"}`

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
… [5534 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"plateau\\|M5\" reports/rapport-cerveau-corrections.md | head -50", "description": "Read M5 plateau findings in corrections report"}`

  ```
88:## 5. M5 — l'action est une constante de format
99:baseline tour**. L'oracle avec plateau (H 1,1–2,8 nats) reste inatteignable : le code observé ne
100:contient pas le plateau, et le tirage est uniforme parmi les coups légaux.
143:**12,4 %** sur le proxy, M3 **0**, M4 **0**, M5 **?**, M6 **?**, M7 **?**, M8 **0**. M2 est un
159:- **M5** : **sans contexte négatif** (action constante) ; **avec le plateau**, gain réel de
170:un module solide (M1), un gain de contexte (M5), une table de lésions réelle (M9), et des
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"sans_plateau\\|M5_source\\|plateau\" reports/*.md | head -40", "description": "Search reports for M5 plateau"}`

  ```
reports/INDEX.md:143:| [rapport-plateau-semantique.md](rapport-plateau-semantique.md) | Rapport — le plateau sémantique, mesuré sur un corpus multilingue réel |
reports/rapport-architecture-memoire.md:144:**Le plateau est atteint dès 16 fils.** La charge est limitée par la bande
reports/rapport-c4-retard.md:33:   d'utile — le plateau est donc une information sur la *borne haute* du désastre, pas une
reports/rapport-cerveau-corrections.md:99:baseline tour**. L'oracle avec plateau (H 1,1–2,8 nats) reste inatteignable : le code observé ne
reports/rapport-cerveau-corrections.md:100:contient pas le plateau, et le tirage est uniforme parmi les coups légaux.
reports/rapport-cerveau-corrections.md:159:- **M5** : **sans contexte négatif** (action constante) ; **avec le plateau**, gain réel de
reports/rapport-cycle-rapide.md:165:Pic à la **couche 10** (+0,0374), plateau de 10 à 15 (+0,0269 à +0,0354),
reports/rapport-cycle-rapide.md:170:| | pic | plateau | bombement précoce |
reports/rapport-cycle-rapide.md:180:**Et cela corrobore une mesure indépendante.** `rapport-plateau-semantique.md`
reports/rapport-cycle-rapide.md:241:Et les couches **10 à 15** forment un plateau, pas un pic isolé.
rep
… [3377 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' reports/rapport-pipeline-m2.md", "description": "Read pipeline M2 report"}`

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
| M5 `source` M1 sans contexte | 28,03 % (n=396) —
… [1629 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '80,110p' reports/rapport-cerveau-corrections.md", "description": "Read M5 correction details"}`

  ```
- La complétion 97,9 % s'explique par **72,35 % `vers=None`** (15/15) et **27,65 % à 14/15** :
  0,7235 + 0,2765 × 14/15 = **0,9816** ; c'est de l'identité, pas de la complétion.
- Split par code (23 train / 6 test) : codes non stockés rappelés **0/6** ; complétion exacte
  **0/10** ; **0/7** valeurs de champ inédites.
- **Fausse mémoire** : 98,96 % des leurres à 1 champ reçoivent une valeur fausse ; 65,4 % renvoient
  exactement le code source. Aucun seuil ne sépare un cue partiel légitime d'un leurre.
- **M4 ne généralise pas** ; c'est une table de hachage exacte.

## 5. M5 — l'action est une constante de format

`action()` classe le coup par la **forme** du code (présence de `de`/`vers`, `chemin`, `case`), pas
par sa sémantique : échecs = toujours `deplacer`, dames = toujours `prendre`, morpion = une valeur.
Prédire `action` ne peut pas battre la majorité : **97,46 % = 97,46 %** sur 1 538 transitions,
ordre 2 compris.

Sur des cibles qui varient, il y a un gain **mécanique**, pas sémantique :
`source` ordre 1 **12,60 % vs 6,49 %** (+6,10 pts), ordre 2 **14,42 %** ; `cible` ordre 1
**7,92 % vs 5,80 %** (+2,12 pts) mais **surprisal −0,04 nat** (gain de mode). Les dames portent
l'e
… [1093 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"CHAMPS_SOURCE\\|^VALEURS\\|VALEURS =\\|MORPION\\|morpion\" tools/semantique/universaux.py | head -20; sed -n '1,80p' tools/semantique/universaux.py", "description": "Inspect universal field values"}`

  ```
21:JEUX = ("morpion", "echecs", "dames", "go", "cartes")
136:    return RSN(str(code.get("jeu", "morpion")), nature, corps)
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
TAILLES = (None, 5, 9, 13, 19
… [1631 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"CHAMPS_SOURCE\\|CIBLES\" -A25 tools/cerveau/predictif.py | head -50", "description": "Inspect predictif constants"}`

  ```
51:CHAMPS_SOURCE = {"echecs": "de", "dames": "chemin_0"}
52:CIBLES = ("action", "source", "cible")
53-
54-
55-def valeur(pas, cible: str = "cible"):
56-    """La valeur de la cible pour un pas (ou un code typé).
57-
58-    `pas` peut être un `Pas` (attribut `.code`) ou directement le dictionnaire
59-    du code. Rend `None` quand la cible n'a pas de sens pour ce jeu (un go n'a
60-    pas de case de départ).
61-    """
62-    code = getattr(pas, "code", pas)
63-    if not isinstance(code, dict):
64-        raise TypeError("valeur attend un Pas ou un code typé (dict)")
65-    jeu = code.get("jeu")
66-    if cible == "action":
67-        return code.get("action")
68-    if cible == "source":
69:        champ = CHAMPS_SOURCE.get(jeu)
70-        return code.get(champ) if champ else None
71-    if cible == "cible":
72-        if jeu == "echecs":
73-            return code.get("vers")
74-        if jeu == "dames":
75-            for champ in ("chemin_2", "chemin_1", "chemin_0"):
76-                if code.get(champ) is not None:
77-                    return code[champ]
78-            return None
79-        if jeu == "go":
80-            return code.get("point")
81-        if jeu == "morp
… [936 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def experience_m7\" -A80 tools/cerveau/neuromodulation.py | head -110", "description": "Inspect experience_m7"}`

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
… [4628 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def experience_m8\\|def experience_contexte\" -A60 tools/cerveau/sommeil.py | head -130", "description": "Inspect M8 experience functions"}`

  ```
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
688-        vu, le code exclu n'est pas dans le train) : la mesure utile est la
689-        décomposition champs / non nuls / nuls et le backoff par champ.
690-        """
691-        from semantique.typed_corpus import decouper, items as corpus_items
692-        its = list(items_) if items_ is not None else corpus_items()
693-        n = len(its)
694-        codes = sorted({tuple(sorted(_code
… [2763 caractères tronqués]
  ```

### 👤 Utilisateur

Agent f0969e87-af0c-43b1-93cf-f278d9c90846 sent a message: 
Timebox : donne un point et écris /tmp/a15-m9-complet.json/.md dès qu'une mesure existe, même partielle ; termine ensuite.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,84p' tools/cerveau/memoire_travail.py", "description": "Read memory module API"}`

  ```
#!/usr/bin/env python3
"""M3 — mémoire de travail : maintenir une suite de codes, la relire, la comparer.

Le module est volontairement **structurel** : un tampon borné, un pointeur, une
répétition. Il ne promet pas la mémoire du réseau (N5) ; il mesure ce qu'un
**bus** peut tenir sans gradient.
"""
from __future__ import annotations

from collections import deque

from semantique.universaux import CHAMPS


class MemoireTravail:
    nom = "M3-memoire-travail"

    def __init__(self, capacite: int = 12) -> None:
        self.capacite = capacite
        self.tampon: deque = deque(maxlen=capacite)

    def charger(self, codes) -> None:
        self.tampon.clear()
        for c in codes[-self.capacite:]:
            self.tampon.append(dict(c))

    def pousser(self, code: dict) -> None:
        """Présente un code à la suite : le plus ancien sort si le tampon est plein.

        C'est la présentation séquentielle (une liste poussée), par opposition à
        `charger` qui remplace tout le tampon d'un coup.
        """
        self.tampon.append(dict(code))

    def lire(self, i: int):
        return self.tampon[i] if 0 <= i < len(self.tampon) else None

    def distance(self, a: dict, 
… [1947 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def span\\|def nback\\|def charger\" -A25 tools/cerveau/memoire_travail.py", "description": "Read span/nback details"}`

  ```
22:    def charger(self, codes) -> None:
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
45-        Le tampon d'origine ne lit que par position ; cette lecture par contenu
46-        sert à mesurer la reconnaissance et les faux souvenirs. Elle ne modifie
47-        ni l'ordre ni le contenu du tampon.
--
55:    def nback(self, n: int):
56-        if
… [1230 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,90p' tools/cerveau/episodique.py", "description": "Read episodic memory API"}`

  ```
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
        self.episodes.append(Episode(surface, dict(code), langue, paire, poids))

    def _cle(self, code: dict):
        return vecteur(code)

    def classer(self, code: dict, k: int = 1):
        """Classe les épisodes par similarité cosinus décroissante.

        Renvoie des couples `(score, episode)`, le score restant dans [0, 1] p
… [2129 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def preparer_flux\\|def _tourner\\|def _configurations\" -A30 tools/cerveau/neuromodulation.py | head -80", "description": "Check M7 flux preparation"}`

  ```
248:def preparer_flux(items_=None) -> list[EpisodeM7]:
249-    """Les épisodes du corpus, avec les signaux disponibles *au moment de l'écriture*.
250-
251-    - incertitude : ``1 - confiance`` de la lecture du codec (pas d'étiquette) ;
252-    - récompense : proxy déclaré de gain matériel (``prendre``/``promouvoir``),
253-      le corpus n'ayant pas de récompense externe.
254-    """
255-    from jeux.codecs import codec
256-    from semantique.typed_corpus import items as corpus_items
257-
258-    its = list(items_) if items_ is not None else corpus_items()
259-    out = []
260-    for it in its:
261-        try:
262-            lec = codec(it.jeu).lit(it.texte, niveau=4)
263-            confiance = float(lec.confiance) if lec is not None else 0.0
264-        except Exception:
265-            confiance = 0.0
266-        out.append(EpisodeM7(it.texte, dict(it.code), it.jeu,
267-                             max(0.0, min(1.0, 1.0 - confiance)),
268-                             1.0 if it.code.get("action") in ("prendre", "promouvoir") else 0.0))
269-    return out
270-
271-
272-def _poids_politique(ep: EpisodeM7, politique: str) -> float:
273-    if politique == "incertitude":
274-   
… [2909 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Writing `tools/cerveau/lesion_complet.py` (benches, sham, dose-response, doubles)

