# Session DSH — relecture

- identifiant : `235066f5-307a-4285-a882-14bc2d06cb7b`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 11:38:25
- agent : standard


## Tour 1

### 👤 Utilisateur

Dépôt /home/stephane/GitHub/Qtrinet, sprint autonome 24 h. Sous-agent A8 : construire et mesurer une **chaîne sémantique** B13 avec les modules corrigés, sans toucher aux modules existants.

État corrigé (à utiliser tel quel) :
- M1 `hub.py` : codec typé exact, 528/528 avec contexte, 70,8 % sans contexte.
- M2 `voies.py` : têtes `de`/`vers` ; vues 126/126 ; inédit 13/20 (aug-formes) ; `point`/`chemin` non concluants.
- M5 `predictif.py` : `Predictif(cible="source", contexte=True, melange=0.5)` donne +0,626 nat ; sans contexte négatif.
- M6 `gating.py` : sélecteur de tâche 94,95 % (base 50 %), conflit/commutation 0.
- M8 `sommeil.py` : marginal ; M9 `lesion.py` réel.
- Tests : `PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools` → 85 OK (8 skip).

Objectif : écrire `tools/cerveau/pipeline_semantique.py` et `tools/cerveau/tests/test_pipeline_semantique.py` :
- `percevoir(surface, jeu, contexte)` → code M1 ; `predire(sequence, cible)` → M5 contexte ; `selectionner(code, langue)` → M6 ; `consolider()` → M8 ; `leser(module)` → M9.
- Mesurer une chaîne **bout en bout** sur les 528 items : code exact, prédiction de `source`/`cible` avec contexte, sélection, complétion M8 ; produire `/tmp/a8-pipeline-semantique.json` et `.md`.
- Comparer à une chaîne **sans contexte** et à un **contrôle négatif** (contexte permuté).
- Si la chaîne ne fait pas mieux que M1 seul, le dire : c'est un test d'intégration, pas une preuve sémantique.

Contraintes :
- Crée uniquement `tools/cerveau/pipeline_semantique.py` et son test ; ne modifie pas les modules existants, docs, reports, journal, `batterie.py`, git.
- Pas de `git add/commit/checkout`.
- CPU uniquement. Sois autonome, mesure, autocritique. Réponds avec un résumé et les chemins.
Your parent agent id is "f0969e87-af0c-43b1-93cf-f278d9c90846". Before you finish, send your result to that agent with send_message({ agent_id: "f0969e87-af0c-43b1-93cf-f278d9c90846", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

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

⏵ Exploration du dépôt et lecture des modules M1/M2/M5/M6/M8/M9

- **bash** `{"command": "ls /home/stephane/GitHub/Qtrinet && echo '---' && ls /home/stephane/GitHub/Qtrinet/tools/cerveau | head -60", "description": "List repo root and cerveau tools"}`

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
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git status --short | head -20 && echo '---' && git log --oneline -5", "description": "Check git status and recent log"}`

  ```
M tools/cerveau/sommeil.py
---
74c1fd86 B12 — M2 AUG-POS : VERS 95,4 % INÉDIT 13,3/20 ; DE 92,2 % ; POINT = MAJORITÉ ; AUCUNE VARIANTE NE DOMINE
6e2ce420 DOCS — LA FICHE DE COHÉRENCE ENREGISTRE L'INTRODUCTION DE LA SYNTHÈSE
96d50d8d DOCS — SCHÉMA MÉTHODE : TEXTES DANS LES CADRES
6a4c10fb DOCS — SYNTHÈSE COMME INTRODUCTION : 9 FICHES CONCEPT, 14 SCHÉMAS, GLOSSAIRE ET LIENS RELATIFS
daf5ccaf B12 — M9 RÉSERVE : ACTION TRIVIALE, DE SEUL INFORMATIF ; M8 QUEUE 106/106 VUS
  ```

### 🤖 Assistant

⏵ Lecture des interfaces réelles des six modules

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet/tools/cerveau && wc -l hub.py voies.py predictif.py gating.py sommeil.py lesion.py pipeline.py batterie.py && echo '---' && ls tests", "description": "Count lines in cerveau modules and list tests"}`

  ```
47 hub.py
   737 voies.py
   575 predictif.py
   707 gating.py
   972 sommeil.py
   726 lesion.py
    46 pipeline.py
   225 batterie.py
  4035 total
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

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet/tools/cerveau && sed -n '1,120p' hub.py", "description": "Read start of hub.py"}`

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
… [575 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Repérage du corpus 528 items et des conventions de banc

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,225p' tools/cerveau/batterie.py", "description": "Read batterie.py"}`

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
… [6929 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"528\" --include=*.py --include=*.md -l | head -30", "description": "Find files mentioning 528"}`

  ```
reports/archive/rapport-toutes-langues.md
reports/archive/rapport-campagne-benefices.md
reports/rapport-fenetre-puits-attention.md
reports/toutes-langues/050-50-la-contrainte-dinvariance-deplace-la-cou.md
reports/campagne-benefices/050-47-attn-sinks-le-drapeau-vit-mais-seulement.md
reports/rapport-raid0-nvme.md
reports/rapport-universaux.md
reports/rapport-hybride.md
reports/rapport-cerveau-modules.md
reports/bilan-b11.md
reports/rapport-restitution.md
reports/README.md
reports/rapport-cerveau-corrections.md
tools/cerveau/neuromodulation.py
tools/cerveau/sommeil.py
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md
journal/sessions/e7dfe34f-d596-4f98-93c2-cad5a92d3b1e/digest.md
journal/sessions/aa5f9fc5-9450-4118-b65f-e8b99a28519d/digest.md
journal/sessions/aa5f9fc5-9450-4118-b65f-e8b99a28519d/rapport.md
journal/sessions/5ce3f080-2d3d-467a-8ee1-df697f3f3e68/digest.md
journal/sessions/5185ccb1-be24-4716-89df-62621e790444/digest.md
journal/sessions/564fbe3a-a859-4b3b-bd17-4da73a2f4e22/digest.md
journal/sessions/8e04c99a-8ba1-4675-9f80-fa3338449
… [335 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Extraction des signatures/API des modules M2, M5, M6, M8, M9

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet/tools/cerveau && grep -n '^class \\|^def \\|^    def ' voies.py", "description": "List voies.py API"}`

  ```
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
546:def _stats_classes(pred, cible, n
… [404 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet/tools/cerveau && grep -n '^class \\|^def \\|^    def ' predictif.py gating.py sommeil.py lesion.py", "description": "List APIs of predictif, gating, sommeil, lesion"}`

  ```
predictif.py:55:def valeur(pas, cible: str = "cible"):
predictif.py:90:def _champ_contexte(contexte: str, nom: str) -> str | None:
predictif.py:95:def plateau_contexte(contexte: str, jeu: str):
predictif.py:140:def candidats_contexte(contexte: str, jeu: str, cible: str):
predictif.py:174:def champ_cible(code: dict, cible: str) -> str | None:
predictif.py:193:class Predictif:
predictif.py:203:    def __init__(self, cible: str = "cible", ordre: int = 1, kappa: float = 10.0,
predictif.py:224:    def entrainer(self, sequences) -> None:
predictif.py:244:    def distribution(self, jeu: str, cur=None, precedent=None, contexte=None) -> dict:
predictif.py:298:    def _choix(self, dist, jeu: str, contexte=None):
predictif.py:311:    def predire(self, code: dict, precedent=None, contexte=None) -> tuple:
predictif.py:322:    def evaluer(self, sequences) -> dict:
predictif.py:374:    def mesurer(self, sequences, cibles=CIBLES, ordres=(0, 1, 2),
predictif.py:408:    def diagnostic(self, sequences, cibles=CIBLES) -> dict:
predictif.py:444:def baseline_tour(sequences_train, sequences_test, cible: str = "cible") -> dict:
predictif.py:479:def permuter(sequences, cible: str = "cible", graine: int = 0
… [5144 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet/tools/cerveau && sed -n '1,230p' predictif.py", "description": "Read predictif.py first part"}`

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
… [8306 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet/tools/cerveau && sed -n '230,575p' predictif.py", "description": "Read predictif.py second part"}`

  ```
y = valeur(b, self.cible)
                cur = valeur(a, self.cible)
                if y is None or cur is None:
                    continue
                jeu = b.jeu
                self.marginal[jeu][y] += 1
                self.valeurs[jeu].add(y)
                self.transitions[(jeu, cur)][y] += 1
                if i >= 1:
                    prev = valeur(pas[i - 1], self.cible)
                    if prev is not None:
                        self.transitions2[(jeu, prev, cur)][y] += 1

    # ------------------------------------------------------------------
    def distribution(self, jeu: str, cur=None, precedent=None, contexte=None) -> dict:
        """La loi prédictive de la cible, lissée à chaque niveau.

        Du plus spécifique au plus général : ordre 2 → ordre 1 → marginale du
        jeu. Chaque niveau est interpolé avec `kappa` pseudo-comptes du niveau
        inférieur, ce qui garantit une probabilité non nulle partout.

        Si `contexte` est fourni et que le mode contexte est actif, la loi est
        restreinte aux valeurs **observables** du plateau (`candidats_contexte`)
        puis mélangée à l'uniforme sur ces candidats (`melange`). Le masque est
 
… [14589 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet/tools/cerveau && sed -n '1,280p' gating.py", "description": "Read gating.py first part"}`

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
… [10655 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet/tools/cerveau && sed -n '470,707p' gating.py", "description": "Read gating.py executer section"}`

  ```
"effet_commutation_congruent": effet_commutation_congruent,
            "effet_commutation_incongruent": effet_commutation_incongruent,
            "interaction_conflit_commutation": (effet_commutation_incongruent
                                                - effet_commutation_congruent),
            "effet_tache_langue": (exact(par_tache["langue"])
                                   - exact(par_tache["sens"])),
            "effet_tache_langue_macro": (macro_sonde["langue"]["exact"]
                                         - macro_sonde["sens"]["exact"]),
        }

    def executer_switch(self, items=None, cibles=("fr", "en")) -> dict:
        """Exécute la tâche de commutation et rend les coûts mesurés.

        La porte dure `tache` est comparée à ses témoins et au contrôle positif
        `perseveration_tache`. Aucune clé n'est partagée avec `executer` : la
        batterie M6 continue de mesurer la tâche de confluence.
        """
        essais = self.tache_switch(items, cibles)
        if not essais:
            return {"exact": 0.0, "n": 0, "effet_conflit": 0.0,
                    "effet_commutation": 0.0, "politique": "tache"}
        resultat = self._metriques_switch
… [11242 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet/tools/cerveau && sed -n '278,470p' gating.py", "description": "Read gating switch task section"}`

  ```
def tache_switch(self, items=None, cibles=("fr", "en")) -> list[EssaiTache]:
        """Tâche à deux consignes (`sens` / `langue`) sur les mêmes sondes B7.

        Chaque groupe (code cible × langue cible) donne **9 blocs de 4 essais**
        (go, traduction, langue, ni), tous de même consigne dans un bloc. La
        suite des consignes est `sens, langue, langue, sens, sens, langue,
        langue, sens, sens` : 4 commutations et 4 répétitions par groupe, à
        sondes appariées (mêmes 4 essais, ordre tourné). La consigne est
        l'**indice** ; elle est parfaitement fiable.

        `condition` vaut `congruent` quand les deux canaux donnent la même
        réponse (go : oui/oui ; ni : non/non) et `incongruent` quand ils
        divergent (traduction : sens oui, langue non ; langue : sens non,
        langue oui). C'est le conflit de la tâche : sous la consigne `sens`, le
        canal langue est le distracteur, et réciproquement.
        """
        if len(cibles) != 2:
            raise ValueError("la tâche de commutation exige exactement deux langues")
        if items is None:
            brut = [it for it in construire_corpus_multilingue().items]
        else:
       
… [9065 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet/tools/cerveau && sed -n '1,240p' sommeil.py", "description": "Read sommeil.py first part"}`

  ```
#!/usr/bin/env python3
"""M8 — sommeil : consolider des épisodes en prototypes, et mesurer ce que cela vaut.

Le module d'origine groupait par ``(jeu, action)`` et prenait le mode **champ par
champ**. Le score publié, 96,48 % sur 106 épisodes de test, est réel mais il est
mal lu :

- les champs sont **dominés par ``None``** : 12 des 15 champs ont plus de 98 %
  d'exactitude agrégée parce que la bonne réponse y est presque toujours
  ``None``. Sur les valeurs non nulles, la précision tombe à ~84 % sur tout le
  corpus (~86 % sur la queue), et les trois champs porteurs (``de``, ``vers``,
  ``carte``) sont à ~50 %, ~50 % et ~22–28 % conditionnellement.
- le score **exact** n'est pas 0 % : il vaut 65,1 % sur la queue, 24,1 % sur les
  29 codes uniques. La « baseline 0,0 » du rapport était l'absence de mémoire,
  pas un prédicteur.
- groupé par ``(jeu)`` seul, le prototype fait déjà 96,10 % : le groupe
  ``(jeu, action)`` n'ajoute que +0,38 point. Le score vient du jeu, pas de
  l'action.
- sur des **codes jamais vus**, le prototype ne peut pas produire le bon code :
  l'exact est 0 % par construction. Un prototype est une marginale, pas une
  généralisation.

Le module ajoute donc : pr
… [9474 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"94,95\\|94.95\\|0.9495\" --include=*.py --include=*.md --include=*.json tools reports /tmp 2>/dev/null | head -20", "description": "Search for 94.95 metric"}`

  ```
reports/rapport-pont-generatif.md:216:| 375 | 12 | 0,6222 | 0,6465 | 0,5006 | 0,9495 | 0,8979 |
reports/restitution-udhr-flux.json:1351:  "fragments_exacts_vus": 4.594594594594595,
reports/traduction-onu-7b.json:2362:    "chrf": 94.95,
reports/traduction-onu6-7b.json:3051:    "chrf": 94.95,
reports/traduction-onu6-3b.json:1383:  "chrf": 48.52261294695548,
reports/kfold-pidgin-tw.json:222:   "chrf": 88.00937594295972,
reports/kfold-pidgin-7.json:287:   "chrf": 88.00937594295972,
reports/kfold-tout-0210.json:62:   "chrf": 58.96666194195108,
reports/kfold-7b-amp-0210.json:27:   "chrf": 88.00937594295972,
reports/kfold-asp-0210.json:27:   "chrf": 88.00937594295972,
reports/rapport-cerveau-corrections.md:102:- **Tâche de gate de tâche** (sens/langue, 792 essais) : **94,95 %**, base 50 % ; conflit **0,000**, commutation **0,000** ; la langue seule est à 88,6 %, le sens à 100 %. C'est un **sélecteur de tâche**, pas un contrôle exécutif.
reports/rapport-cerveau-corrections.md:157:- **M6** : **sélecteur de tâche** à 94,95 % (base 50 %), mais **conflit 0** et **commutation 0** ;
/tmp/a6-m5-m6.json:2543:          "gain_surprise": -1.809949511001982,
/tmp/a6-m5-m6.json:4304:        "surprise_m
… [448 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet/tools/cerveau && sed -n '580,726p' lesion.py", "description": "Read lesion.py m8 and battery"}`

  ```
# ---------------------------------------------------------------------------
# M8 — le sommeil
# ---------------------------------------------------------------------------
def _m8() -> dict:
    """Le sommeil, lésé sur le protocole honnête : code tenu à l'écart.

    La lésion est le retrait de tout prototype (repli sur la marginale globale),
    mesurée sur le **même** leave-one-code-out que l'intacte. La queue publiée
    (96,48 %) est rappelée pour mémoire : ses 106 codes sont tous dans le train,
    c'est une reconstruction intra-code, pas une généralisation.
    """
    rq = experience_m8()
    rc = experience_contexte()
    q = rq["queue"]
    lq = rc["loo_codes"]
    intact = lq["ladder"]
    lese = lq["global"]
    hyb = rc["codes_tenus_resume"]["hybride_surface"]
    exact_nouveaux = rc["verdict"]["exact_codes_tenus"]
    return _entree(
        "retirer le sommeil (aucun prototype, marginale globale) — code tenu à l'écart",
        {"champs": intact["champs"], "exact": intact["exact"],
         "champs_non_nuls": intact["champs_non_nuls"],
         "champs_nuls": intact["champs_nuls"],
         "exact_codes_nouveaux": exact_nouveaux,
         "exact_codes_uniques": rq["
… [6313 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet/tools/cerveau && sed -n '1,110p' lesion.py && echo '=== M1 ===' && sed -n '58,110p' lesion.py", "description": "Read lesion.py intro and M1 lesion"}`

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
- **M2** : couper la voie ventrale (action) ou dorsale (``de``). Par défaut le
  **vrai ``voies.py``** est exécuté (encodeur natif gelé, entraînement des têtes
  sur GPU ou CPU) ; si la base ou torch manque, le substitut bayésien à deux
  têtes est déclaré dans ``statut`` (repli documenté, jamais silencieux) ;
- **M3** : capacité du tampon (0, 1, 2, 4, 8, 12), dose-réponse ;
- **M4** : stockage vide, puis lésion du champ d'adressage (le champ est mis à
  ``None`` dans la requête) ;
- **M5** : retirer les transitions, l'ordre 2 ou le repli majoritaire ; contrôle
  positif sur une chaîne de Markov synthétique ;
- **M6** : retirer la porte (tout accepter), l'inverser, la rendre al
… [5337 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet/tools/cerveau && sed -n '440,560p' lesion.py", "description": "Read lesion M5 and M6"}`

  ```
{"rappel": sans, "completion": completion_vide, "n": len(echantillon)},
        {"rappel": intact - sans, "completion": completion - completion_vide,
         "par_champ": champs,
         "champ_le_plus_necessaire": plus_faible,
         "deficit_champ_max": deficit_max,
         "tautologie_recuperation": True},
        len(echantillon), sham=0.0, note=note)


# ---------------------------------------------------------------------------
# M5 — le prédictif
# ---------------------------------------------------------------------------
class _Pas:
    __slots__ = ("code", "jeu")

    def __init__(self, action: str):
        self.jeu = "synthetique"
        self.code = {"jeu": "synthetique", "action": action}


class _Seq:
    __slots__ = ("pas",)

    def __init__(self, pas):
        self.pas = pas


def _m5(seqs) -> dict:
    rng = random.Random(3)
    seqs = list(seqs)
    rng.shuffle(seqs)
    n = int(len(seqs) * 0.8)
    tr, te = seqs[:n], seqs[n:]
    # cible par défaut du module actuel : la case d'arrivée (varie), pas l'action
    intact = Predictif(cible="cible", ordre=2)
    intact.entrainer(tr)
    mes_intact = intact.evaluer(te)
    sans = Predictif(cible="cible", ordre=2)
… [3696 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection du corpus typé (528 items) et des champs de code

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls tools/semantique tools/jeux && echo '---' && sed -n '1,160p' tools/semantique/typed_corpus.py", "description": "List semantic/jeux modules and read typed_corpus"}`

  ```
tools/jeux:
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

tools/semantique:
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
from semantique.un
… [2445 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,140p' tools/jeux/corpus.py", "description": "Read corpus.py"}`

  ```
#!/usr/bin/env python3
"""corpus.py — le corpus de surfaces, avec leur sens attendu.

Un item est un triplet (surface, contexte, RSN attendue). Le corpus est
**construit par le code**, pas stocké dans `data/` : il est reproductible, et on
peut le régénérer après chaque correction. Il couvre les cinq jeux, deux
langues, plusieurs notations, et des paires d'expressions **équivalentes** (pour
l'invariance) et **non équivalentes** (pour le contrôle de collision).

Règle : l'attendu est calculé par les **règles**, jamais recopié à la main. Si
le codec et les règles se contredisent, le corpus le dit — c'est un test, pas
une illustration.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .regles import cartes as C
from .regles import dames as D
from .regles import echecs as E
from .regles import go as G
from .regles import morpion as M
from .rsn import RSN


@dataclass(frozen=True)
class Item:
    jeu: str
    texte: str
    nature: str
    attendu: RSN
    contexte: RSN | None = None
    format: str = ""
    langue: str = ""
    groupe: str = ""
    paire: str | None = None
    contre: str | None = None  # paire NÉGATIVE : même `contre`, sens différen
… [5404 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,120p' tools/semantique/universaux.py && grep -n \"def code_rsn\\|def rsn_depuis_code\\|def code_item\\|def empreinte_code\\|def resume_contexte\\|^CHAMPS\" tools/semantique/universaux.py", "description": "Read universaux API"}`

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
… [2980 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom semantique.typed_corpus import items\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux import code_rsn\nvrais=[]\nfor c in … [593 caractères tronqués]`

  ```
vrais nature coup: 528
typed items: 528
jeux: {'cartes': 161, 'echecs': 146, 'dames': 70, 'go': 87, 'morpion': 64}
langues: 67
format: {'sgf': 1, 'carte': 8, 'numerique': 11, 'algebrique': 2, 'san': 12, 'gtp': 10, 'uci': 8, 'cellule': 22, 'multilingue': 449, 'francais': 5}
ctx non vide: 375
ItemType(texte='A1', code={'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 0, 'symbole': 'X', 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}, jeu='morpion', nature='coup', langue='fr', paire='morpion-a1', format='cellule', contexte='morpion etat trait=X taille=3 cases=.,.,.,.,.,.,.,.,.')
  ```

### 🤖 Assistant

⏵ Consultation des mesures A6/A7 existantes pour réutiliser le protocole

- **bash** `{"command": "ls -la /tmp/a*-*.json /tmp/a*-*.md 2>/dev/null | tail -20", "description": "List existing A-series result files"}`

  ```
-rw-r--r--. 1 stephane stephane  28491 27 oct 10:21 /tmp/a1-m5-m6.json
-rw-r--r--. 1 stephane stephane  14491 27 oct 10:21 /tmp/a1-m5-m6.md
-rw-r--r--. 1 stephane stephane    313 27 oct 09:55 /tmp/a2-m2-cpu.json
-rw-r--r--. 1 stephane stephane 114449 27 oct 10:17 /tmp/a2-m7-m8-m9.json
-rw-r--r--. 1 stephane stephane  24726 27 oct 10:17 /tmp/a2-m7-m8-m9.md
-rw-r--r--. 1 stephane stephane   8176 27 oct 10:11 /tmp/a2-m7-m8-m9-part1.md
-rw-r--r--. 1 stephane stephane  10317 27 oct 10:16 /tmp/a2-m7-m8-m9-part2.md
-rw-r--r--. 1 stephane stephane   5524 27 oct 10:16 /tmp/a2-m7-m8-m9-part3.md
-rw-r--r--. 1 stephane stephane  52818 27 oct 10:28 /tmp/a3-m2.json
-rw-r--r--. 1 stephane stephane  12967 27 oct 10:28 /tmp/a3-m2.md
-rw-r--r--. 1 stephane stephane 311113 27 oct 10:23 /tmp/a3-m2-partial.json
-rw-r--r--. 1 stephane stephane  16098 27 oct 10:10 /tmp/a4-m3-m4.json
-rw-r--r--. 1 stephane stephane  15057 27 oct 10:10 /tmp/a4-m3-m4.md
-rw-r--r--. 1 stephane stephane 637687 27 oct 11:34 /tmp/a5-m2-generalisation.json
-rw-r--r--. 1 stephane stephane  14914 27 oct 11:39 /tmp/a5-m2-generalisation.md
-rw-r--r--. 1 stephane stephane 247677 27 oct 11:00 /tmp/a5-quick.json
-rw-r--r--. 1 stephane 
… [256 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,240p' reports/rapport-cerveau-corrections.md", "description": "Read brain corrections report"}`

  ```
# Corrections B12 — ce que le stress des sous-agents a changé

> **Objet.** Les premiers chiffres B12 (M2 93,2 %, M3 12/12, M4 1,0, M8 96,48 %) étaient
> **gonflés par la structure du corpus**. Trois sous-agents ont refait les mesures avec des
> splits par code, des leurres, du bruit et des permutations. Ce document corrige, il n'efface pas :
> les anciens chiffres restent dans la fiche, avec leur cause.

## 1. Ce qui reste solide : M1

| mesure | valeur |
|---|---:|
| surfaces lues avec contexte | **528 / 528** |
| sans contexte | **70,8 %** |
| canonique | **100 %** |
| invariance | **100 %** |
| événements de bus | **1 584** |

M1 est le **codec classique** avec un bus. C'est exact, ce n'est pas neuronal.

## 2. M2 — le 93,2 % était du recouvrement de surfaces

Le test B5/B7 contient **146 items `de`** ; **126 sont des surfaces normalisées déjà vues** à
l'entraînement synthétique, **20 sont inédites**.

| mesure | valeur |
|---|---:|
| `de` moyen 3 graines | **93,6 %** |
| `de` sur surfaces vues | **126 / 126** |
| `de` sur surfaces inédites | **10,7 / 20 = 53,3 %** |
| `vers` moyen 3 graines | **94,3 %** |
| `vers` inédit | **11,7 / 20 = 58,3 %** |
| `point` | 95,7 % **< majori
… [9578 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,180p' /tmp/a6-m5-m6.md", "description": "Read A6 M5-M6 report"}`

  ```
# M5 (contexte plateau) et M6 (porte de tâche) — A6

Corpus M5 : `cerveau.sequences.corpus(0, 200, 12)`, split par partie 80/20, graines 3, 11, 23. Corpus M6 : surfaces B7 fr/en. Temps : 46.4 s.

## M5 — le plateau est une observation, pas une règle

Le prédicteur reçoit `Pas.contexte` (sortie de `resume_contexte`) et restreint ses valeurs possibles à ce que le plateau autorise : `source` = mes pièces, `cible` = cases non occupées par moi. `masque_uniforme` restreint la loi à l'uniforme sur les candidats ; `masque_hist` restreint la loi temporelle ; `masque_melange` fait le mélange 50/50 des deux. Aucune règle de déplacement n'est importée.

### Global (moyenne de 3 graines)

| cible | ordre | bras | n | exact | majoritaire | surprisal | gain surv. | Δsurv. vs sans | Δexact vs sans |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| action | 1 | sans | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |
| action | 1 | masque_uniforme | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |
| action | 1 | masque_hist | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |
| action | 1 | masque_melange | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |
… [12631 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,240p' tools/cerveau/tests/test_gating.py", "description": "Read gating tests"}`

  ```
from __future__ import annotations

import unittest

from cerveau.gating import CONDITIONS, TACHES, Porte


class TestTacheConflit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.porte = Porte()
        cls.essais = cls.porte.tache_conflit()

    def test_taille_et_equilibre(self):
        self.assertEqual(len(self.essais), 88)
        for condition in CONDITIONS:
            n = sum(1 for e in self.essais if e.condition == condition)
            self.assertEqual(n, 22)
        # les blocs de 4 essais partagent la même langue cible
        for i in range(0, len(self.essais), 4):
            bloc = self.essais[i:i + 4]
            self.assertEqual(len({e.cible_langue for e in bloc}), 1)

    def test_conditions(self):
        for e in self.essais:
            if e.condition == "go":
                self.assertEqual(e.langue_vraie, e.cible_langue)
                self.assertEqual(e.code_vrai, e.cible_code)
            elif e.condition == "traduction":
                self.assertEqual(e.code_vrai, e.cible_code)
                self.assertNotEqual(e.langue_vraie, e.cible_langue)
            elif e.condition == "langue":
                self.assertEqual(e.langu
… [6522 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,120p' tools/cerveau/pipeline.py && echo '--- tests pipeline ---' && sed -n '1,160p' tools/cerveau/tests/test_pipeline.py", "description": "Read existing pipeline and tests"}`

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
… [1214 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"selectionner\\|sélectionner\\|selecteur\\|sélecteur\" --include=*.py tools | head -30", "description": "Search for selection API in tools"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,220p' tools/cerveau/sequences.py", "description": "Read sequences corpus generator"}`

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
… [2245 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Prototypage rapide des mesures M1/M5/M6/M8 sur le corpus

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport collections\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import empreinte_code, code_rsn\nits = items()\nprint('n', len(its))\nprint('langues', collections.Counter(i.langue for i in  … [564 caractères tronqués]`

  ```
n 528
langues [('fr', 55), ('notation', 31), ('en', 15), ('de', 11), ('es', 11), ('it', 11), ('ja', 11), ('nl', 11), ('pl', 11), ('pt', 11), ('ru', 11), ('zh', 11), ('cs', 10), ('da', 10), ('eo', 10), ('et', 10), ('fa', 10), ('fi', 10), ('hu', 10), ('nb', 10), ('sl', 10), ('sr', 10), ('sv', 10), ('uk', 10), ('vi', 10), ('sq', 9), ('ar', 8), ('bn', 8), ('ca', 8), ('eu', 8), ('af', 8), ('be', 8), ('lv', 7), ('tr', 7), ('el', 6), ('ko', 6), ('sk', 6), ('th', 6), ('gl', 5), ('he', 5), ('hr', 5), ('id', 5), ('lt', 5), ('ms', 5), ('ro', 5), ('hy', 5), ('hi', 4), ('is', 4), ('ka', 4), ('mk', 4), ('nn', 4), ('ta', 4), ('ur', 4), ('az', 4), ('bs', 4), ('cy', 4), ('mn', 4), ('uz', 4), ('sw', 3), ('ga', 3), ('kk', 2), ('ne', 2), ('am', 1), ('km', 1), ('pa', 1), ('so', 1), ('zu', 1)]
fr/en 70
codes uniques 29
paires 31 paires non vides 518
taille paire [(2, 4), (1, 4), (4, 3), (3, 3), (6, 2), (61, 2), (30, 2), (12, 1), (10, 1), (7, 1)]
ctx vide 153
jeu/langue [(('morpion', 'fr'), 21), (('echecs', 'notation'), 16), (('dames', 'fr'), 9), (('cartes', 'fr'), 9), (('echecs', 'fr'), 8), (('go', 'fr'), 8), (('cartes', 'en'), 7), (('dames', 'notation'), 6), (('go', 'notation'), 5), (('cartes', 'bn'), 
… [233 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport collections, time\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import code_rsn, empreinte_code\nfrom cerveau.hub import Hub\nfrom jeux.codecs import codec\nits = items()\nhub = Hub() … [548 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 11, in <module>
AttributeError: 'ItemType' object has no attribute 'attendu'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport collections\nfrom semantique.typed_corpus import items\nfrom semantique.universaux import code_rsn\nfrom cerveau.hub import Hub\nits = items()\nhub = Hub()\nok=0; fails=[]\nfor it in its:\n    c = hub.percevo … [449 caractères tronqués]`

  ```
M1 ctx exact 0 / 528
M1 sans ctx 374
fails [('A1', 'morpion', 'fr', 'cellule', None, {'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 0, 'symbole': 'X', 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}), ('a1', 'morpion', 'fr', 'cellule', None, {'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 0, 'symbole': 'X', 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}), ('(1,1)', 'morpion', 'fr', 'cellule', None, {'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 0, 'symbole': 'X', 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None})]
paires: [('ml-go-d4', 62), ('ml-echecs-nf3', 61), ('ml-echecs-e4', 61), ('ml-dames-b6c5', 56), ('ml-morpion-a1', 42), ('ml-cartes-10h', 36), ('ml-cartes-ah', 30), ('ml-cartes-jc', 30), ('ml-cartes-ks', 29), ('ml-cartes-qd', 28), ('ml-go-passe', 14), ('morpion-a1', 12), (None, 10), ('echec
… [390 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport collections\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux import code_rsn, resume_contexte\nfrom cerveau.hub import  … [781 caractères tronqués]`

  ```
n 528 ctx RSN 375
ctx 528 sans 374
langues fr/en 70
format Counter({'multilingue': 449, 'cellule': 22, 'san': 12, 'numerique': 11, 'gtp': 10, 'uci': 8, 'carte': 8, 'francais': 5, 'algebrique': 2, 'sgf': 1})
paire None 10
ctx resume sample morpion etat trait=X taille=3 cases=.,.,.,.,.,.,.,.,.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport time, random, collections, dataclasses\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux import code_rsn, resume_context … [1699 caractères tronqués]`

  ```
corpus jeux 160 t 0.5201795101165771
eval seqs 47 {'morpion': 6, 'echecs': 13, 'dames': 6, 'go': 8, 'cartes': 14}
source sans {'exact': 0.0, 'majoritaire': 0.0, 'surprise': 4.5469, 'surprise_majoritaire': 3.472, 'gain_surprise': -1.075, 'n': 197}
source avec {'exact': 0.0457, 'majoritaire': 0.0, 'surprise': 2.4049, 'surprise_majoritaire': 3.472, 'gain_surprise': 1.0671, 'n': 197}
source permute {'exact': 0.0254, 'majoritaire': 0.0, 'surprise': 3.4024, 'surprise_majoritaire': 3.472, 'gain_surprise': 0.0695, 'n': 197}
cible sans {'exact': 0.0, 'majoritaire': 0.1656, 'surprise': 3.656, 'surprise_majoritaire': 3.4121, 'gain_surprise': -0.2439, 'n': 302}
cible avec {'exact': 0.0, 'majoritaire': 0.1639, 'surprise': 3.2784, 'surprise_majoritaire': 3.4558, 'gain_surprise': 0.1773, 'n': 305}
cible permute {'exact': 0.0, 'majoritaire': 0.1639, 'surprise': 3.7695, 'surprise_majoritaire': 3.4558, 'gain_surprise': -0.3138, 'n': 305}
t 0.6887261867523193
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport collections, time\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom cerveau.gating import Porte\nvrais=[]\nfor c in (construire_corpus(), cons … [877 caractères tronqués]`

  ```
fr/en 70 langue exact 0.6571428571428571 Counter({('fr', 'fr'): 34, ('fr', None): 15, ('en', 'en'): 12, ('fr', 'en'): 4, ('en', 'de'): 2, ('en', 'af'): 1, ('fr', 'af'): 1, ('fr', 'de'): 1})
majoritaire fr 0.7857142857142857
detected Counter({'fr': 54, None: 46, 'af': 41, 'en': 19, 'cs': 18, 'be': 16, 'de': 15, 'da': 14, 'sv': 12, 'fa': 11, 'ja': 11, 'eo': 10, 'es': 10, 'et': 10, 'zh': 10, 'it': 9, 'ar': 8, 'bn': 8, 'fi': 8, 'hu': 8, 'sl': 8, 'sr': 8, 'pl': 8, 'ru': 8, 'sq': 8, 'uk': 8, 'vi': 8, 'eu': 7, 'pt': 7, 'el': 6, 'ko': 6, 'nl': 6, 'th': 6, 'ca': 5, 'he': 5, 'bs': 5, 'id': 5, 'lv': 5, 'hy': 5, 'hi': 4, 'ka': 4, 'lt': 4, 'ky': 4, 'ta': 4, 'az': 4, 'is': 3, 'nb': 3, 'ur': 3, 'cy': 3, 'mn': 3, 'uz': 3, 'gl': 2, 'ro': 2, 'sk': 2, 'sw': 2, 'tr': 2, 'ga': 2, 'ne': 2, 'hr': 1, 'kk': 1, 'mk': 1, 'ms': 1, 'nn': 1, 'am': 1, 'km': 1, 'pa': 1, 'so': 1, 'zu': 1}) t 0.33538317680358887
switch exact 0.9494949494949495 n 792 conflit 0.0 commut 0.0
  ```

### 🤖 Assistant

⏵ Prototype M8 (split par paire, LOO) et du protocole de complétion

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport collections, random, time\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux import code_rsn, empreinte_code, CHAMPS\nfro … [2196 caractères tronqués]`

  ```
n 528 codes 29
paires 30 val 6 train 377 test 151 test paires ['cartes-carte-b', 'echecs-nf3', 'echecs-petit-roque', 'ml-cartes-10h', 'ml-echecs-nf3', 'ml-morpion-a1']
codes test vus train 109 / 151
protos 7 t 0.0023603439331054688
train {'champs': 0.976657824933687, 'exact': 0.6843501326259946, 'champs_non_nuls': 0.9053084648493543, 'n': 377, 'n_inconnus': 0, 'n_champs_non_nuls': 1394, 'prototypes': 7}
test {'champs': 0.9205298013245033, 'exact': 0.2781456953642384, 'champs_non_nuls': 0.6819787985865724, 'n': 151, 'n_inconnus': 0, 'n_champs_non_nuls': 566, 'prototypes': 7}
global {'champs': 0.7854, 'exact': 0.0, 'champs_non_nuls': 0.1413, 'n': 151, 'n_inconnus': 0, 'n_champs_non_nuls': 566, 'prototypes': 1}
par_jeu {'champs': 0.9205, 'exact': 0.2781, 'champs_non_nuls': 0.682, 'n': 151, 'n_inconnus': 0, 'n_champs_non_nuls': 566, 'prototypes': 5}
par_groupe {'champs': 0.9205, 'exact': 0.2781, 'champs_non_nuls': 0.682, 'n': 151, 'n_inconnus': 0, 'n_champs_non_nuls': 566, 'prototypes': 7}
par_type {'champs': 0.9214, 'exact': 0.2781, 'champs_non_nuls': 0.6855, 'n': 151, 'n_inconnus': 0, 'n_champs_non_nuls': 566, 'prototypes': 9}
joint {'champs': 0.9205, 'exact': 0.2781, 'champs_non_nul
… [792 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport collections, random, time\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux import code_rsn, resume_contexte\nfrom cerve … [1063 caractères tronqués]`

  ```
perm ctx: exact 491 wrong 2 none 35 n 528
echecs 146 133
dames 70 55
go 87 87
morpion 64 60
cartes 161 156
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport collections\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.universaux import resume_contexte\nvrais=[]\nfor c in (construire_cor … [496 caractères tronqués]`

  ```
echecs 146 ctx distincts 4 top [('echecs etat trait=w roques=KQkq demi=0 p', 139), ('echecs etat trait=w roques=KQkq demi=0 p', 4), ('echecs etat trait=w roques=- demi=0 plei', 2)]
dames 70 ctx distincts 4 top [('dames etat trait=b demi=0 cases=b,b,b,b,', 62), ('dames etat trait=b demi=0 cases=.,.,.,.,', 4), ('dames etat trait=b demi=0 cases=.,.,.,.,', 3)]
go 87 ctx distincts 1 top [('go etat trait=1 taille=9 passe=0 plateau', 87)]
morpion 64 ctx distincts 2 top [('morpion etat trait=X taille=3 cases=.,.,', 62), ('morpion etat trait=O taille=3 cases=.,.,', 2)]
cartes 161 ctx distincts 2 top [(None, 153), ('cartes etat', 8)]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nimport collections, random\nfrom jeux.corpus import construire_corpus\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom cerveau.gating import Porte\nvrais=[]\nfor c in (construire_corpus(), co … [1298 caractères tronqués]`

  ```
all exact 368 0.696969696969697 none 46
majority ('fr', 55) 0.10416666666666667
balanced acc 0.8484848484848485 tpr 0.696969696969697 tnr 1.0
perm labels balanced 0.5009469696969697 tpr 0.013257575757575758 tnr 0.9886363636363636
  ```

### 👤 Utilisateur

Agent f0969e87-af0c-43b1-93cf-f278d9c90846 sent a message: 
Timebox : donne un point maintenant. Écris `pipeline_semantique.py` et `/tmp/a8-pipeline-semantique.json/.md` dès qu'une chaîne minimale tourne, même sans toutes les mesures ; termine ensuite. Un négatif net suffit.

### 🤖 Assistant

⏵ Écriture du module `pipeline_semantique.py` (chaîne M1→M5→M6→M8→M9)

