# Session DSH — relecture

- identifiant : `a117a3c1-8325-4a63-8e8f-14fea0bce484`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 10:30:52
- agent : standard


## Tour 1

### 👤 Utilisateur

Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A6 : tenter une dernière amélioration de M5/M6 après les négatifs A1, sans toucher aux autres modules.

État A1 :
- M5 `predictif.py` : `action` constante ; `source` +6,1 pts mais mécanique ; `cible` surprisal −0,04 ; code observé sans plateau.
- M6 `gating.py` : conjonction 94,3 % / base 75 %, commutation 0, 2 surfaces fr/en identiques.
- Corpus : `cerveau.sequences.corpus`, `semantique.typed_corpus.items`, `semantique.universaux.resume_contexte`.
- Tests : `PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools`.

Objectif : **donner le contexte/plateau** à M5 et mesurer si la prédiction de `cible`/`action` dépasse l'oracle partiel ; pour M6, construire une tâche de **gating de tâche** (pas seulement de langue) avec conflit et mesure de commutation, ou documenter le négatif.
- M5 : ajoute le contexte (`resume_contexte`) au prédicteur ; cible `cible` et `source` ; ordres 1/2 ; baseline majoritaire/tour ; 3 graines ; compare au sans-contexte. Si le plateau donne un gain réel (surprisal), garde-le ; sinon négatif net.
- M6 : tâche `go`/`traduction`/`langue`/`ni` déjà ; tente une **vraie porte de tâche** (deux tâches, conflit, switch) et mesure le coût. Si le canal lexical suffit, dis-le.
- Écris `/tmp/a6-m5-m6.json` et `.md` ; code seulement `predictif.py`, `gating.py`, tests associés.
- Ne touche pas à `batterie.py`, docs, reports, journal, git. Pas de commit.
- CPU uniquement. Sois autonome, timebox, autocritique. Réponds avec un résumé et les chemins.
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

⏵ Exploration du dépôt et des modules M5/M6

- **bash** `{"command": "ls /home/stephane/GitHub/Qtrinet && echo \"---\" && ls /home/stephane/GitHub/Qtrinet/tools/cerveau/ | head -50", "description": "List repo root and cerveau tools"}`

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

- **bash** `{"command": "find /home/stephane/GitHub/Qtrinet -name \"predictif.py\" -o -name \"gating.py\" 2>/dev/null | head -20", "description": "Find M5 and M6 module files"}`

  ```
/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py
/home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """M5 — codage prédictif : prédire une cible **variable**, mesurer l'erreur.
3: 
4: Leçon mesurée (sprint 24 h, corpus `sequences.corpus`) : l'ancienne cible
5: `action` est **structurellement constante** par jeu — `action()` dans
6: `universaux.py` classe le coup par la *forme* du code (présence de `de`/`vers`,
7: de `chemin`, de `case`…), pas par sa sémantique. Résultat : échecs = toujours
8: `deplacer`, dames = toujours `prendre`, morpion = toujours `jouer_case` ; seul go
9: varie (`poser` 92 %, `passer` 8 %). Prédire `action` ne peut donc pas battre la
10: classe majoritaire : le 98,9 % publié était le taux de cette constante.
11: 
12: Le module change de cible et mesure honnêtement :
13: 
14: - `action` — la cible historique, gardée comme témoin ;
15: - `source` — la case de départ (`de` aux échecs, `chemin_0` aux dames) ;
16: - `cible`  — la case d'arrivée (`vers`, dernier `chemin`, `point`, `case`).
17: 
18: Trois ordres de Markov (0 = marginale par jeu, 1 = pas précédent, 2 = deux pas),
19: avec **repli hiérarchique Dirichlet** pour que la surprisal
… [18357 caractères tronqués]
  ```


  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """M6 — porte exécutive : une vraie tâche de conflit langue/tâche sur B7.
3: 
4: L'ancienne porte ne mesurait qu'une chose : `MULTI.detecte_langue(surface)`
5: comparée à la langue cible. Son « exactitude » de 72,9 % était donc le taux du
6: classifieur lexical, pas une mesure d'inhibition ; son « coût de commutation »
7: négatif venait de la composition des blocs (les cibles alternaient sur des
8: items très majoritairement français), pas d'un coût cognitif.
9: 
10: La tâche construite ici est un **go/no-go de confluence** sur les surfaces B7
11: fr/en (11 codes, deux langues) :
12: 
13: - `go`          : la sonde est le coup cible **dans la langue cible** → accepter ;
14: - `traduction`  : même coup, **autre langue** → inhiber le sens, refuser ;
15: - `langue`      : autre coup, **langue cible** → inhiber la langue, refuser ;
16: - `ni`          : autre coup, autre langue → refuser.
17: 
18: Les quatre conditions sont équilibrées (22 essais chacune, 88 au total) : un
19: politique « toujours non » obtient 75 %, et chaque canal seul (langue ou sens)
20: obtie
… [21331 caractères tronqués]
  ```

- **bash** `{"command": "ls /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/ && echo \"---\" && ls /tmp/a*-m5-m6* 2>/dev/null; ls /tmp | grep -i a6 2>/dev/null; echo \"---\"; ls /home/stephane/GitHub/Qtrinet/tools/semantique/ | head -40", "description": "List tests and previous A1 artifacts"}`

  ```
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
---
/tmp/a1-m5-m6.json
/tmp/a1-m5-m6.md
nvA64
semantique-nvlink-A64
semantique-nvlink-A64.json
semantique-nvlink-A64.out
tmp4a6jtkb0
tmpa6n66hs_
tmplo1a6pcv
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

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,120p' tools/cerveau/sequences.py", "description": "Read sequences module head"}`

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

- **bash** `{"command": "cat /tmp/a1-m5-m6.md", "description": "Read previous A1 report"}`

  ```
# M5 (prédictif) et M6 (gating) — résultat mesuré

Corpus M5 : `cerveau.sequences.corpus(0, 200, 12)`, split par partie 80/20, graine 3. Corpus M6 : surfaces B7 fr/en. Temps : 20.7 s.

## M5 — la cible `action` était constante ; les cibles de case ne le sont pas

| cible | ordre | n | exact | majoritaire | gain exact | surprisal | surprisal maj. | gain surprisal |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| action | 0 | 1538 | 97.5 % | 97.5 % | +0.0 pt | 0.086 | 0.086 | +0.000 |
| action | 1 | 1538 | 97.5 % | 97.5 % | +0.0 pt | 0.087 | 0.086 | -0.000 |
| action | 2 | 1538 | 97.5 % | 97.5 % | +0.0 pt | 0.087 | 0.086 | -0.001 |
| source | 0 | 770 | 6.5 % | 6.5 % | +0.0 pt | 3.539 | 3.539 | +0.000 |
| source | 1 | 770 | 12.6 % | 6.5 % | +6.1 pt | 3.112 | 3.539 | +0.428 |
| source | 2 | 770 | 14.4 % | 6.5 % | +7.9 pt | 3.099 | 3.539 | +0.440 |
| cible | 0 | 1465 | 5.8 % | 5.8 % | +0.0 pt | 3.375 | 3.375 | +0.000 |
| cible | 1 | 1465 | 7.9 % | 5.8 % | +2.1 pt | 3.418 | 3.375 | -0.043 |
| cible | 2 | 1465 | 11.4 % | 5.8 % | +5.6 pt | 3.410 | 3.375 | -0.035 |

Lecture : l'ordre 0 est la baseline majoritaire par jeu. L'ancien M5 (`action`, ordre 1) donnait 98,9 % = la classe constante 
… [13034 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/cerveau/tests/test_predictif.py && echo \"=====GATING=====\" && sed -n '1,80p' tools/cerveau/tests/test_gating.py", "description": "Read M5 and M6 tests head"}`

  ```
from __future__ import annotations

import unittest

from cerveau.predictif import (Predictif, baseline_tour, controle_negatif,
                               permuter, valeur)
from cerveau.sequences import Pas, Sequence, corpus


def _pas(jeu: str, action: str = "deplacer", source=None, cible=None,
         champ_cible: str | None = None) -> Pas:
    code = {"jeu": jeu, "action": action}
    if source is not None:
        code["de" if jeu == "echecs" else "chemin_0"] = source
    if cible is not None:
        if champ_cible is None:
            champ_cible = {"echecs": "vers", "dames": "chemin_1",
                           "go": "point", "morpion": "case"}[jeu]
        code[champ_cible] = cible
    return Pas(jeu, code, "", "", None)


def _sequence(jeu: str, pas) -> Sequence:
    return Sequence(jeu, tuple(pas))


class TestCibles(unittest.TestCase):
    def test_source_et_cible(self):
        self.assertEqual(valeur(_pas("echecs", source=62, cible=45), "source"), 62)
        self.assertEqual(valeur(_pas("echecs", source=62, cible=45), "cible"), 45)
        dames = _pas("dames", source=8, cible=17, champ_cible="chemin_1")
        self.assertEqual(valeur(dames, "source"), 8)
    
… [5791 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"resume_contexte\" -r tools/semantique/universaux.py | head; echo ---; grep -n \"def resume_contexte\" -A 80 tools/semantique/universaux.py", "description": "Inspect resume_contexte implementation"}`

  ```
139:def resume_contexte(ctx) -> str:
---
139:def resume_contexte(ctx) -> str:
140-    """Le contexte RSN en une ligne courte : trait, taille, cases, plateau."""
141-    if ctx is None:
142-        return ""
143-    corps = dict(ctx.corps or {})
144-    parts = [str(ctx.jeu), str(ctx.nature)]
145-    for cle in ("trait", "taille", "passe", "roques", "ep", "demi", "plein"):
146-        if cle in corps and corps[cle] is not None:
147-            parts.append(f"{cle}={corps[cle]}")
148-    if "cases" in corps and isinstance(corps["cases"], list):
149-        parts.append("cases=" + ",".join("." if v is None else str(v) for v in corps["cases"]))
150-    if "plateau" in corps:
151-        parts.append("plateau=" + str(corps["plateau"]))
152-    return " ".join(parts)
153-
154-
155-def empreinte_code(code: dict) -> str:
156-    """L'empreinte du code typé : stable, indépendante de la langue."""
157-    return hashlib.sha256(json.dumps(code, sort_keys=True, ensure_ascii=False,
158-                                    separators=(",", ":")).encode()).hexdigest()
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"class ItemType\\|def items\\|resume_contexte\\|contexte\" tools/semantique/typed_corpus.py | head -40", "description": "Inspect typed_corpus context fields"}`

  ```
17:from semantique.universaux import code_item, resume_contexte
21:class ItemType:
29:    contexte: str = ""
32:def items() -> list[ItemType]:
44:                                it.langue, it.paire, it.format, resume_contexte(it.contexte)))
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/semantique/typed_corpus.py"}`

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

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,140p' tools/semantique/universaux.py", "description": "Read universaux head"}`

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
… [3539 caractères tronqués]
  ```

- **bash** `{"command": "ls -la /tmp/a1_m5_m6.py 2>/dev/null; python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/a1-m5-m6.json'))\ndef walk(o,p=''):\n    if isinstance(o,dict):\n        for k,v in o.items():\n            np = p+'.'+k if p else k\n            if isinstance(v,(dict,list)):\n                wa … [206 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 29310 27 oct 10:20 /tmp/a1_m5_m6.py
meta.titre = M5 codage prédictif / M6 gating exécutif — mesures du sprint
meta.corpus_m5 = cerveau.sequences.corpus(0, 200, 12)
meta.corpus_m6 = corpus_multilingue B7, fr/en
meta.graine_split = 3
meta.fraction = 0.8
meta.permutations = 20
meta.secondes = 20.7
m5.protocole.graine = 3
m5.protocole.fraction = 0.8
m5.protocole.n_sequences_train = 640
m5.protocole.n_sequences_test = 160
m5.protocole.cibles.action.ordre_0.exact = 0.974642
m5.protocole.cibles.action.ordre_0.majoritaire = 0.974642
m5.protocole.cibles.action.ordre_0.surprise = 0.086481
m5.protocole.cibles.action.ordre_0.surprise_majoritaire = 0.086481
m5.protocole.cibles.action.ordre_0.gain = 0.0
m5.protocole.cibles.action.ordre_0.gain_surprise = 0.0
m5.protocole.cibles.action.ordre_0.n = 1538
m5.protocole.cibles.action.ordre_0.hors_vocabulaire = 0
m5.protocole.cibles.action.ordre_0.cible = action
m5.protocole.cibles.action.ordre_0.ordre = 0
m5.protocole.cibles.action.ordre_0.par_jeu.dames.exact = 1.0
m5.protocole.cibles.action.ordre_0.par_jeu.dames.majoritaire = 1.0
m5.protocole.cibles.action.ordre_0.par_jeu.dames.surprise = 0.0
m5.protocole.cibles.action.
… [39920 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reconnaissance : format du contexte, oracle A1, interface batterie

- **todo_write** `{"todos": [{"content": "Reconnaissance corpus/contexte/oracle/interface batterie", "status": "in_progress"}, {"content": "M5 : ajouter le contexte plateau au prédicteur + protocole 3 graines vs sans contexte vs oracle", "status": "pending"}, {"content": "M6 : vraie porte de tâche (2 tâches, conflit, … [249 caractères tronqués]`

  ```
Updated todo list: 5 pending, 1 in progress, 0 completed.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"oracle\\|def h_oracle\\|H_oracle\" /tmp/a1_m5_m6.py | head -30", "description": "Locate oracle code in A1 script"}`

  ```
96:def oracle(jeu, graines, cible, n=12):
119:    return {"n": len(Hs), "H_oracle": sum(Hs) / len(Hs) if Hs else 0.0,
120:            "mode_oracle": sum(modes) / len(modes) if modes else 0.0}
123:def oracle_test(seqs_test, idx_test, cible):
129:    return {jeu: oracle(jeu, graines, cible) for jeu, graines in par_jeu.items()}
139:                "baseline_tour": {}, "controles": {}, "oracle": {},
153:        resultat["oracle"][cible] = oracle_test(test, idx_test, cible)
349:    a("### Plancher oracle (le plateau serait-il utile ?)\n")
350:    a("| cible | jeu | n oracle | H oracle | H modèle (ordre 1) | écart | mode oracle |")
353:        for jeu, x in m5["oracle"][cible].items():
359:            a(f"| {cible} | {jeu} | {x['n']} | {x['H_oracle']:.3f} | {h:.3f} | "
360:              f"{h - x['H_oracle']:+.3f} | {pct(x['mode_oracle'])} |")
361:    a("\nL'oracle est la loi de la cible **conditionnée par la position réelle** "
364:      "surprisal et H oracle est le prix de l'observation manquante (de 1,0 à "
365:      "1,6 nat selon le jeu et la cible). Le mode oracle n'est pas un plafond d'exactitude (il peut "
499:      "corpus plus grand pourrait révéler de petits gains, mais l'écar
… [18 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"m5\\|m6\\|M5\\|M6\" tools/cerveau/batterie.py | head -40", "description": "Inspect battery M5/M6 interface"}`

  ```
137:def m5(seqs):
146:def m6():
186:def m9(m1r, m2r, m3r, m4r, m5r, m6r, m7r):
197:        "M5_sans_transitions": 1.0 - m5r.get("majoritaire", 0.0),
198:        "M6_sans_porte": 1.0 - m6r.get("exact", 0.0),
212:    out["M5"] = m5(seqs)
213:    out["M6"] = m6()
216:    out["M9"] = m9(out["M1"], out["M2"], out["M3"], out["M4"], out["M5"], out["M6"], out["M7"])
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '80,170p' /tmp/a1_m5_m6.py", "description": "Read A1 oracle implementation"}`

  ```
for _ in range(min(n, 9)):
            coups = M.coups_legaux(etat)
            if not coups:
                break
            c = rng.choice(coups)
            codes = [code_rsn(x) for x in coups]
            etapes.append((code_rsn(c), codes))
            etat = M.applique(etat, c)
    # validation : le rejeu doit redonner exactement la séquence publique
    seq = partie(jeu, graine, n)
    assert len(seq.pas) == len(etapes), (jeu, graine)
    for (code, _), pas in zip(etapes, seq.pas):
        assert code == pas.code, (jeu, graine)
    return etapes


def oracle(jeu, graines, cible, n=12):
    Hs, modes = [], []
    for g in graines:
        etapes = rejoue(jeu, g, n)
        for i in range(1, len(etapes)):
            y = valeur(etapes[i][0], cible)
            prev = valeur(etapes[i - 1][0], cible)
            if y is None or prev is None:
                continue
            if cible == "action" and jeu == "go":
                p = {"passer": 0.1, "poser": 0.9}
            else:
                vals = [valeur(c, cible) for c in etapes[i][1]]
                vals = [v for v in vals if v is not None]
                if not vals:
                    continue
                cnt
… [2645 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom cerveau.sequences import corpus, partie\nseqs = corpus(0, 2, 6)\nfor s in seqs[:4]:\n    print('===', s.jeu, len(s.pas))\n    for p in s.pas[:2]:\n        print('CTX:', p.contexte[:300])\n        print('CODE:', … [100 caractères tronqués]`

  ```
=== echecs 6
CTX: echecs etat trait=w roques=KQkq demi=0 plein=1 plateau=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
CODE: {'jeu': 'echecs', 'action': 'deplacer', 'de': 54, 'vers': 46, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}
SURF: g3
CTX: echecs etat trait=b roques=KQkq demi=0 plein=1 plateau=rnbqkbnr/pppppppp/8/8/8/6P1/PPPPPP1P/RNBQKBNR
CODE: {'jeu': 'echecs', 'action': 'deplacer', 'de': 12, 'vers': 28, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}
SURF: e5
=== echecs 6
CTX: echecs etat trait=w roques=KQkq demi=0 plein=1 plateau=rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
CODE: {'jeu': 'echecs', 'action': 'deplacer', 'de': 50, 'vers': 42, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}
SURF: c3
CTX: echecs etat trait=b roques=KQkq demi=0 plein=1 plateau=rnbqkbnr/pppppppp/8/8/8/2P5/P
… [1733 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom cerveau.sequences import partie\nfor jeu in ('go','morpion'):\n    s = partie(jeu, 0, 4)\n    print('===', jeu)\n    for p in s.pas:\n        print('CTX:', p.contexte)\n        print('CODE:', {k:v for k,v in p. … [86 caractères tronqués]`

  ```
=== go
CTX: go etat trait=1 taille=9 passe=0 plateau=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
CODE: {'jeu': 'go', 'action': 'poser', 'taille': 9, 'point': 53}
CTX: go etat trait=2 taille=9 passe=0 plateau=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
CODE: {'jeu': 'go', 'action': 'passer', 'taille': 9, 'passe': True}
CTX: go etat trait=1 taille=9 passe=1 plateau=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
CODE: {'jeu': 'go', 'action': 'poser', 'taille': 9, 'point': 63}
CTX: go etat trait=2 taille=9 passe=0 plateau=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
… [781 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"def rsn_depuis_position\\|def position_depuis\\|plateau\\|def case\\|def index\" tools/jeux/regles/echecs.py | head -30; echo ---; grep -n \"def rsn_depuis_position\\|def vers_rsn\\|def plateau\\|cases\" tools/jeux/regles/dames.py tools/jeux … [107 caractères tronqués]`

  ```
16:  plateau à chaque nœud ;
72:def case_vers_indice(c: str) -> int:
184:    __slots__ = ("plateau", "trait", "roques", "ep", "demi", "plein", "rois", "hash")
186:    def __init__(self, plateau: list[int], trait: int = BLANC, roques: int = 0,
188:        if len(plateau) != 64:
189:            raise ErreurEchecs("le plateau doit avoir 64 cases")
190:        self.plateau = plateau
197:        for i, p in enumerate(plateau):
215:        plateau = [0] * 64
231:                    plateau[_idx(r, c)] = piece(coul, t)
244:        pos = cls(plateau, trait, roques, ep, demi, plein)
254:        return Position(list(self.plateau), self.trait, self.roques, self.ep,
263:                p = self.plateau[_idx(r, c)]
282:        for i, p in enumerate(self.plateau):
295:        p = self.plateau
333:        p = self.plateau
422:        p = self.plateau
436:        # plateau
512:        p = self.plateau
546:        pieces = [typ(p) for p in self.plateau if p]
567:        for i, p in enumerate(self.plateau):
621:            p = self.plateau[de]
623:            prise = self.plateau[vers] != 0 or drapeau == EP
631:                          if m != coup and typ(self.plateau[m.de]) == t and m.vers == ver
… [3814 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '60,100p' tools/jeux/regles/echecs.py && echo '--- RSN ---' && sed -n '790,840p' tools/jeux/regles/echecs.py && echo '--- idx ---' && grep -n \"def _idx\" -A 6 tools/jeux/regles/echecs.py", "description": "Read chess board index and RSN encodin … [3 caractères tronqués]`

  ```
def piece(couleur: int, typ: int) -> int:
    return (couleur << 3) | typ


def couleur(p: int) -> int:
    return p >> 3


def typ(p: int) -> int:
    return p & 7


def case_vers_indice(c: str) -> int:
    c = c.strip().lower()
    if len(c) != 2 or c[0] not in FICHIERS or c[1] not in "12345678":
        raise ValueError(f"case invalide : {c!r}")
    return (8 - int(c[1])) * 8 + FICHIERS.index(c[0])


def indice_vers_case(i: int) -> str:
    return FICHIERS[i % 8] + str(8 - i // 8)


def _coord(i: int) -> tuple[int, int]:
    return divmod(i, 8)


def _idx(r: int, c: int) -> int:
    return r * 8 + c


def _dans(r: int, c: int) -> bool:
    return 0 <= r < 8 and 0 <= c < 8


# Voisins d'un cavalier et d'un roi.
_SAUTS_C = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
_SAUTS_R = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
VOISINS_CAVALIER = [[] for _ in range(64)]
VOISINS_ROI = [[] for _ in range(64)]
for _i in range(64):
--- RSN ---
    pos = Position.depart()
    return rsn_depuis_position(pos, Annotation(langue="notation", format="fen", surface=""))


def rsn_depuis_position(pos: Position, annotation: Annotation | None = Non
… [2122 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,60p' tools/cerveau/batterie.py && sed -n '130,160p' tools/cerveau/batterie.py", "description": "Read battery M5/M6 functions"}`

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
… [1873 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Exploration du masque plateau : entropies et exactitude par jeu

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,80p' /tmp/a1_m5_m6.py", "description": "Read A1 replay helper header"}`

  ```
#!/usr/bin/env python3
"""Harnais de mesure M5/M6 — écrit /tmp/a1-m5-m6.json et .md."""
from __future__ import annotations

import collections
import json
import math
import os
import random
import subprocess
import sys
import time

RACINE = "/home/stephane/GitHub/Qtrinet"
sys.path.insert(0, os.path.join(RACINE, "tools"))
os.chdir(RACINE)

from cerveau.gating import Porte, CONDITIONS          # noqa: E402
from cerveau.predictif import (Predictif, baseline_tour, controle_negatif,  # noqa: E402
                               valeur)
from cerveau.sequences import corpus, partie         # noqa: E402
from jeux.regles import dames as D, echecs as E, go as G, morpion as M  # noqa: E402
from jeux.rsn import RSN                              # noqa: E402
from semantique.typed_corpus import items             # noqa: E402
from semantique.universaux import code_rsn            # noqa: E402

JEUX = ("echecs", "dames", "go", "morpion")
K = {j: i for i, j in enumerate(JEUX)}
GRAINE_SPLIT = 3
FRACTION = 0.8
N_PERMUTATIONS = 20
T0 = time.time()


def split(seqs):
    idx = list(range(len(seqs)))
    random.Random(GRAINE_SPLIT).shuffle(idx)
    n = int(len(idx) * FRACTION)
    return [seqs[i] for i in
… [1695 caractères tronqués]
  ```

- **write** `{"file_path": "/tmp/a6_explore.py", "content": "#!/usr/bin/env python3\n\"\"\"Exploration A6 : que donne le plateau (masque) sur M5 ?\"\"\"\nfrom __future__ import annotations\n\nimport collections\nimport math\nimport os\nimport random\nimport re\nimport sys\n\nRACINE = \"/home/stephane/GitHub/Qtri … [6002 caractères tronqués]`

  ```
<path>/tmp/a6_explore.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 /tmp/a6_explore.py", "description": "Run plateau mask exploration", "timeoutMs": 660000}`

  ```
train 640 test 160

### source
 ordre 0
  dames    n= 396 exact=0.086 H=3.270 | masque n= 396 exact=0.197 H=2.110 | unif exact=0.134 H=2.397 cand=11.0
  echecs   n= 374 exact=0.043 H=3.825 | masque n= 374 exact=0.086 H=2.785 | unif exact=0.037 H=2.770 cand=16.0
 ordre 1
  dames    n= 396 exact=0.174 H=2.612 | masque n= 396 exact=0.280 H=2.002 | unif exact=0.134 H=2.397 cand=11.0
  echecs   n= 374 exact=0.075 H=3.641 | masque n= 374 exact=0.088 H=3.171 | unif exact=0.037 H=2.770 cand=16.0
 ordre 2
  dames    n= 396 exact=0.212 H=2.524 | masque n= 396 exact=0.275 H=2.007 | unif exact=0.134 H=2.397 cand=11.0
  echecs   n= 374 exact=0.072 H=3.709 | masque n= 374 exact=0.083 H=3.272 | unif exact=0.037 H=2.770 cand=16.0

### cible
 ordre 0
  dames    n= 396 exact=0.093 H=2.908 | masque n= 396 exact=0.119 H=2.333 | unif exact=0.106 H=2.265 cand=9.8
  echecs   n= 373 exact=0.035 H=3.826 | masque n= 373 exact=0.040 H=3.693 | unif exact=0.038 H=3.872 cand=48.0
  go       n= 379 exact=0.016 H=4.403 | masque n=   0 exact=0.000 H=0.000 | unif exact=0.000 H=0.000 cand=0.0
  morpion  n= 317 exact=0.091 H=2.198 | masque n= 317 exact=0.246 H=1.523 | unif exact=0.249 H=1.521 cand=5.1
 ordre 1
  dame
… [884 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && cat > /tmp/a6_geom.py <<'PYEOF'\nfrom __future__ import annotations\nimport collections, math, os, random, re, sys\nRACINE = \"/home/stephane/GitHub/Qtrinet\"\nsys.path.insert(0, os.path.join(RACINE, \"tools\")); os.chdir(RACINE)\nfrom cerveau.predict … [5202 caractères tronqués]`

  ```
piece ('echecs', 'P') n 589 deltas 4 top [(-8, 314), (-16, 266), (-9, 6), (-7, 3)]
piece ('echecs', 'n') n 199 deltas 8 top [(17, 77), (15, 69), (10, 15), (6, 12), (-17, 10), (-15, 9)]
piece ('echecs', 'p') n 577 deltas 4 top [(8, 328), (16, 238), (7, 6), (9, 5)]
piece ('echecs', 'B') n 83 deltas 15 top [(-7, 16), (-14, 12), (-18, 11), (-9, 9), (-21, 7), (-27, 6)]
piece ('echecs', 'N') n 190 deltas 8 top [(-15, 70), (-17, 66), (-6, 16), (-10, 14), (6, 9), (15, 7)]
piece ('dames', 'b') n 983 deltas 8 top [(4, 381), (5, 179), (9, 147), (7, 147), (3, 113), (16, 13)]
piece ('dames', 'w') n 982 deltas 8 top [(-4, 351), (-5, 178), (-7, 168), (-9, 157), (-3, 93), (-16, 27)]
piece ('echecs', 'Q') n 72 deltas 19 top [(-7, 10), (-14, 8), (-9, 8), (-18, 6), (-27, 5), (-8, 5)]
piece ('echecs', 'q') n 67 deltas 19 top [(18, 9), (21, 7), (14, 7), (7, 6), (8, 6), (9, 5)]
piece ('echecs', 'k') n 22 deltas 5 top [(8, 7), (7, 7), (9, 4), (1, 3), (-1, 1)]
piece ('echecs', 'r') n 35 deltas 10 top [(8, 13), (1, 8), (-1, 7), (-8, 1), (16, 1), (-6, 1)]
piece ('echecs', 'R') n 38 deltas 8 top [(-8, 12), (1, 9), (-1, 7), (-16, 6), (16, 1), (-24, 1)]
piece ('echecs', 'b') n 96 deltas 16 top [(7, 17), (18, 1
… [651 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re\np='/tmp/a6_geom.py'\ns=open(p).read()\ns=s.replace('for mu in (0.0, 0.5):','for mu in (0.1, 0.3, 0.5, 0.7):')\nopen(p,'w').write(s)\nEOF\nPYTHONPATH=tools timeout 600 python3 /tmp/a6_geom.py 2>&1 | tail -20", "description … [65 caractères tronqués]`

  ```
dames n 396 exact 0.172 H 2.158
echecs n 374 exact 0.102 H 3.199
kappa 0.5 mix 0.5
dames n 396 exact 0.172 H 2.171
echecs n 374 exact 0.102 H 3.33
kappa 0.5 mix 0.7
dames n 396 exact 0.172 H 2.199
echecs n 374 exact 0.102 H 3.498
kappa 1.0 mix 0.1
dames n 396 exact 0.172 H 2.163
echecs n 374 exact 0.104 H 3.099
kappa 1.0 mix 0.3
dames n 396 exact 0.172 H 2.158
echecs n 374 exact 0.104 H 3.2
kappa 1.0 mix 0.5
dames n 396 exact 0.172 H 2.171
echecs n 374 exact 0.104 H 3.331
kappa 1.0 mix 0.7
dames n 396 exact 0.172 H 2.199
echecs n 374 exact 0.104 H 3.499
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/cerveau/memoire_travail.py", "description": "Read working memory module"}`

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
… [1757 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1,90p' tools/cerveau/lesion.py && echo '--- battery m9 ---' && sed -n '180,225p' tools/cerveau/batterie.py", "description": "Read lesion and battery M9"}`

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
… [4054 caractères tronqués]
  ```

### 👤 Utilisateur

Agent f0969e87-af0c-43b1-93cf-f278d9c90846 sent a message: 
Timebox : donne un point maintenant et écris /tmp/a6-m5-m6.json/.md dès que possible, même partiel. Termine ensuite ; un négatif net suffit.

### 🤖 Assistant

⏵ Point d'étape au parent, puis implémentation M5/M6

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "Point A6 (exploration, 1 graine, corpus A1) : le plateau donne un gain RÉEL de surprisal dès qu'on masque les candidats observables — source dames 3.27→2.11 nat (exact 8.6→19.7 %), source échecs 3.82→2.79 (uniforme sur mes pièces, mieu … [558 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

### 🤖 Assistant

⏵ Implémentation du masque de plateau dans M5

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py", "old_string": "import collections\nimport dataclasses\nimport math\nimport random\n\nfrom .sequences import Sequence", "new_string": "import collections\nimport dataclasses\nimport math\nimport random\nimport re\n\nfrom .seque … [22 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py", "old_string": "def champ_cible(code: dict, cible: str) -> str | None:\n    \"\"\"Le nom du champ à permuter pour le contrôle négatif.\"\"\"", "new_string": "# ------------------------------------------------------------------- … [3594 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py", "new_string": "    def __init__(self, cible: str = \"cible\", ordre: int = 1, kappa: float = 10.0,\n                 contexte: bool = False, melange: float = 0.5) -> None:\n        if cible not in CIBLES:\n            raise Va … [1585 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py", "new_string": "    def distribution(self, jeu: str, cur=None, precedent=None, contexte=None) -> dict:\n        \"\"\"La loi prédictive de la cible, lissée à chaque niveau.\n\n        Du plus spécifique au plus général : ordre  … [4262 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py", "new_string": "                jeu = b.jeu\n                precedent = valeur(pas[i - 2], self.cible) if i >= 2 else None\n                dist = self.distribution(jeu, cur, precedent,\n                                        … [223 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py", "new_string": "        for cible in cibles:\n            res_cible = {}\n            for ordre in ordres:\n                m = Predictif(cible, ordre, contexte=self.contexte,\n                              melange=self.melange … [228 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py", "new_string": "def permuter_contextes(sequences, graine: int = 0):\n    \"\"\"Permute les contextes entre pas d'un même jeu : le masque devient faux.\n\n    Contrôle négatif du gain de plateau. La distribution des contextes (d … [1110 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py", "new_string": "Le résultat attendu est un négatif net sur le *contenu* : les parties sont\ngénérées par un tirage **uniforme parmi les coups légaux**, et le code observé\nne porte pas le plateau. Le seul gain réel est mécaniqu … [1174 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -m unittest cerveau.tests.test_predictif -v 2>&1 | tail -20", "description": "Run existing M5 tests"}`

  ```
test_cible_dames_dernier_chemin (cerveau.tests.test_predictif.TestCibles.test_cible_dames_dernier_chemin) ... ok
test_cible_inconnue (cerveau.tests.test_predictif.TestCibles.test_cible_inconnue) ... ok
test_source_absente (cerveau.tests.test_predictif.TestCibles.test_source_absente) ... ok
test_source_et_cible (cerveau.tests.test_predictif.TestCibles.test_source_et_cible) ... ok
test_action_constante_aucun_gain (cerveau.tests.test_predictif.TestPredictif.test_action_constante_aucun_gain) ... ok
test_cles_historiques (cerveau.tests.test_predictif.TestPredictif.test_cles_historiques) ... ok
test_controle_negatif_tue_le_gain (cerveau.tests.test_predictif.TestPredictif.test_controle_negatif_tue_le_gain) ... ok
test_corpus_action_quasi_constante (cerveau.tests.test_predictif.TestPredictif.test_corpus_action_quasi_constante) ... ok
test_ordre_2_ne_change_rien_sur_constante (cerveau.tests.test_predictif.TestPredictif.test_ordre_2_ne_change_rien_sur_constante) ... ok
test_permutation_conserve_la_marginale (cerveau.tests.test_predictif.TestPredictif.test_permutation_conserve_la_marginale) ... ok
test_structure_alternee_gain (cerveau.tests.test_predictif.TestPredictif.test_structure_alternee
… [112 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Implémentation de la porte de tâche M6 (deux tâches, conflit, switch)

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py", "new_string": "from __future__ import annotations\n\nimport math\nimport random\nfrom collections import Counter, defaultdict\nfrom dataclasses import dataclass", "old_string": "from __future__ import annotations\n\nimport math\n … [81 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py", "new_string": "CONDITIONS = (\"go\", \"traduction\", \"langue\", \"ni\")\n# Tâches de la porte de tâche : juger le sens ou la langue de la sonde.\nTACHES = (\"sens\", \"langue\")\n# Domaines du lexique qui portent la langue d'une … [416 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py", "new_string": "    @property\n    def attendu(self) -> bool:\n        return self.condition == \"go\"\n\n\n@dataclass(frozen=True)\nclass EssaiTache:\n    \"\"\"Un essai de la tâche de commutation : sonde, cible, indice de tâche. … [815 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py", "new_string": "    tache: str\n    condition: str\n    transition: str\n    tache_precedente: str | None\n    reponse_sens: bool\n    reponse_langue: bool\n    contexte: object", "old_string": "    tache: str\n    condition: str\ … [94 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py", "new_string": "                        contexte=info[\"contexte\"]))\n        return essais\n\n    # ------------------------------------------------------------------\n    # Tâche de commutation : deux consignes, conflit, switch … [12946 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 300 python3 - <<'EOF'\nfrom cerveau.gating import Porte\np = Porte()\ne = p.tache_switch()\nprint(\"essais\", len(e))\nfrom collections import Counter\nprint(\"taches\", Counter(x.tache for x in e))\nprint(\"conditions\", Coun … [833 caractères tronqués]`

  ```
essais 792
taches Counter({'sens': 440, 'langue': 352})
conditions Counter({'congruent': 396, 'incongruent': 396})
transitions Counter({'commutation': 352, 'repetition': 352, 'initiale': 88})
croise Counter({('incongruent', 'commutation'): 176, ('congruent', 'commutation'): 176, ('incongruent', 'repetition'): 176, ('congruent', 'repetition'): 176, ('congruent', 'initiale'): 44, ('incongruent', 'initiale'): 44})
attendus Counter({True: 396, False: 396})
{
 "exact": 0.9494949494949495,
 "n": 792,
 "acceptes": 356,
 "taux_base_tout_non": 0.5505050505050505,
 "effet_conflit": 0.0,
 "effet_commutation": 0.0,
 "effet_commutation_congruent": 0.0,
 "effet_commutation_incongruent": 0.0,
 "interaction_conflit_commutation": 0.0,
 "effet_tache_langue": -0.11363636363636365,
 "politique": "tache",
 "cibles": [
  "fr",
  "en"
 ],
 "n_commutations": 352,
 "n_repetitions": 352,
 "controle_perseveration": -0.44318181818181823
}
par_tache {
 "sens": {
  "n": 440,
  "corrects": 440,
  "acceptes": 220,
  "exact": 1.0
 },
 "langue": {
  "n": 352,
  "corrects": 312,
  "acceptes": 136,
  "exact": 0.8863636363636364
 }
}
par_condition {
 "congruent": {
  "n": 396,
  "corrects": 376,
  "exact": 0.949494949
… [1213 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 300 python3 - <<'EOF'\nfrom cerveau.gating import Porte\np=Porte()\ne=p.tache_switch()\n# erreurs du canal langue sur les essais T_langue, par sonde unique\nuniq={}\nfor x in e:\n    if x.tache!=\"langue\": continue\n    uniq[ … [662 caractères tronqués]`

  ```
uniques 22 erreurs uniques 5
('english draughts b6 c5', 'dames', 'en') ('en', 'de')
('go D4', 'go', 'en') ('en', 'af')
('go D4', 'go', 'fr') ('fr', 'af')
('tic-tac-toe A1', 'morpion', 'en') ('en', 'de')
('tic-tac-toe A1', 'morpion', 'fr') ('fr', 'de')
confluence exact 0.9431818181818182 politique langue {'exact': 0.75, 'faux_positifs': 17, 'faux_negatifs': 5, 'sensibilite': 0.7727272727272727, 'specificite': 0.7424242424242424, 'exactitude_equilibree': 0.7575757575757576}
canal langue exact sur 88 68 / 88
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/cerveau/gating.py'\ns=open(p).read()\nold='''        par_croise = {(c, t): {\"n\": 0, \"corrects\": 0}\n                      for c in par_condition for t in par_transition}\n        n = ok = acceptes = 0\n        for d in  … [5379 caractères tronqués]`

  ```
patched
{
 "exact": 0.9494949494949495,
 "n": 792,
 "taux_base_tout_non": 0.5,
 "effet_conflit": 0.0,
 "effet_commutation": 0.0,
 "effet_tache_langue": -0.11363636363636365,
 "effet_tache_langue_macro": -0.07499999999999996,
 "controle_perseveration": -0.44318181818181823
}
{
 "sens": {
  "n_sondes": 80,
  "exact": 1.0
 },
 "langue": {
  "n_sondes": 80,
  "exact": 0.925
 }
}
{
 "perseveration_tache": {
  "exact": 0.7525252525252525,
  "effet_conflit": -0.3939393939393939,
  "effet_commutation": -0.44318181818181823,
  "effet_commutation_congruent": 0.0,
  "effet_commutation_incongruent": -0.8863636363636365,
  "interaction_conflit_commutation": -0.8863636363636365
 }
}
  ```

### 🤖 Assistant

⏵ Vérification rapide des bras M5 avec le code modifié

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 - <<'EOF'\nimport random\nfrom cerveau.sequences import corpus\nfrom cerveau.predictif import Predictif, baseline_tour, permuter_contextes\nseqs=corpus(0,200,12)\nidx=list(range(len(seqs))); random.Random(3).shuffl … [986 caractères tronqués]`

  ```
### source 1
  sans exact=0.126 maj=0.065 H=3.112 gainH=+0.428 n=770
  unif exact=0.087 maj=0.065 H=2.578 gainH=+0.961 n=770
  hist exact=0.187 maj=0.065 H=2.570 gainH=+0.970 n=770
  mix  exact=0.187 maj=0.065 H=2.423 gainH=+1.116 n=770
  perm exact=0.036 H=2.609 gainH=+0.927
### source 2
  sans exact=0.144 maj=0.065 H=3.099 gainH=+0.440 n=770
  unif exact=0.087 maj=0.065 H=2.578 gainH=+0.961 n=770
  hist exact=0.182 maj=0.065 H=2.621 gainH=+0.918 n=770
  mix  exact=0.182 maj=0.065 H=2.415 gainH=+1.125 n=770
  perm exact=0.036 H=2.609 gainH=+0.927
### cible 1
  sans exact=0.079 maj=0.058 H=3.418 gainH=-0.043 n=1465
  unif exact=0.096 maj=0.058 H=3.046 gainH=+0.333 n=1466
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 12, in <module>
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/predictif.py", line 329, in evaluer
    surprise.append(-math.log(dist[y]))
                     ~~~~~~~~^^^^^^^^^
ValueError: math domain error
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/cerveau/predictif.py'\ns=open(p).read()\nold='''                if y not in dist:\n                    # valeur de test jamais vue à l'entraînement : hors vocabulaire\n                    hors_vocab += 1\n                   … [504 caractères tronqués]`

  ```
patched
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/cerveau/predictif.py'\ns=open(p).read()\nold='''        if self.melange >= 1.0:\n            return hist\n        uniforme = 1.0 / len(cand)\n        return {x: self.melange * hist[x] + (1.0 - self.melange) * uniforme\n     … [2627 caractères tronqués]`

  ```
patched
### source 1
  sans exact=0.126 maj=0.065 H=3.112 gainH=+0.428 n=770 oov=0
  unif exact=0.187 maj=0.065 H=2.578 gainH=+0.961 n=770 oov=0
  hist exact=0.187 maj=0.065 H=2.570 gainH=+0.970 n=770 oov=0
  mix  exact=0.187 maj=0.065 H=2.423 gainH=+1.116 n=770 oov=0
  perm exact=0.060 H=12.250 gainH=-8.710
### source 2
  sans exact=0.144 maj=0.065 H=3.099 gainH=+0.440 n=770 oov=0
  unif exact=0.182 maj=0.065 H=2.578 gainH=+0.961 n=770 oov=0
  hist exact=0.182 maj=0.065 H=2.621 gainH=+0.918 n=770 oov=0
  mix  exact=0.182 maj=0.065 H=2.415 gainH=+1.125 n=770 oov=0
  perm exact=0.073 H=12.241 gainH=-8.701
### cible 1
  sans exact=0.079 maj=0.058 H=3.418 gainH=-0.043 n=1465 oov=1
  unif exact=0.120 maj=0.058 H=3.046 gainH=+0.333 n=1466 oov=0
  hist exact=0.120 maj=0.058 H=3.101 gainH=+0.274 n=1465 oov=1
  mix  exact=0.120 maj=0.058 H=2.959 gainH=+0.420 n=1466 oov=0
  perm exact=0.083 H=6.521 gainH=-3.142
### cible 2
  sans exact=0.114 maj=0.058 H=3.410 gainH=-0.035 n=1465 oov=1
  unif exact=0.149 maj=0.058 H=3.046 gainH=+0.333 n=1466 oov=0
  hist exact=0.149 maj=0.058 H=3.112 gainH=+0.263 n=1465 oov=1
  mix  exact=0.149 maj=0.058 H=2.940 gainH=+0.439 n=1466 oov=0
  perm exact=0.111 H
… [19 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"def _m5\\|Predictif(\" -A 40 tools/cerveau/lesion.py | sed -n '1,90p'", "description": "Inspect M5 lesion code"}`

  ```
315:def _m5(seqs) -> dict:
316-    rng = random.Random(3)
317-    seqs = list(seqs)
318-    rng.shuffle(seqs)
319-    n = int(len(seqs) * 0.8)
320-    tr, te = seqs[:n], seqs[n:]
321-    # cible par défaut du module actuel : la case d'arrivée (varie), pas l'action
322:    intact = Predictif(cible="cible", ordre=2)
323-    intact.entrainer(tr)
324-    mes_intact = intact.evaluer(te)
325:    sans = Predictif(cible="cible", ordre=2)
326-    sans.entrainer(tr)
327-    sans.transitions.clear()
328-    sans.transitions2.clear()
329-    mes_sans = sans.evaluer(te)
330:    ordre1 = Predictif(cible="cible", ordre=1)
331-    ordre1.entrainer(tr)
332-    mes_ordre1 = ordre1.evaluer(te)
333-    # contrôle positif : une chaîne de Markov où les transitions comptent
334-    rng2 = random.Random(5)
335-    actions = ("a", "b", "c", "d")
336-    synth = []
337-    for _ in range(200):
338-        pas = []
339-        etat = rng2.randrange(4)
340-        for _ in range(12):
341-            pas.append(_Pas(actions[etat]))
342-            etat = (etat + 1) % 4 if rng2.random() > 0.1 else rng2.randrange(4)
343-        synth.append(_Seq(pas))
344-    tr2, te2 = synth[:160], synth[160:]
345:    ps = Pred
… [2113 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '80,240p' tools/cerveau/tests/test_predictif.py", "description": "Read rest of M5 tests"}`

  ```
self.assertAlmostEqual(t["exact"], 1.0)

    def test_ordre_2_ne_change_rien_sur_constante(self):
        seqs = [_sequence("morpion", [_pas("morpion", action="jouer_case",
                                            cible=i % 9) for i in range(9)])
                for _ in range(3)]
        r1 = Predictif("action", 1); r1.entrainer(seqs); a = r1.evaluer(seqs)
        r2 = Predictif("action", 2); r2.entrainer(seqs); b = r2.evaluer(seqs)
        self.assertEqual(a["exact"], b["exact"])
        self.assertEqual(a["n"], b["n"])

    def test_cles_historiques(self):
        m = Predictif("action")
        m.entrainer([_sequence("echecs", [_pas("echecs") for _ in range(5)])])
        r = m.evaluer([_sequence("echecs", [_pas("echecs") for _ in range(5)])])
        for cle in ("exact", "majoritaire", "surprise", "n"):
            self.assertIn(cle, r)

    def test_permutation_conserve_la_marginale(self):
        seqs = [_sequence("echecs", [_pas("echecs", source=i, cible=i + 1)
                                     for i in range(6)]) for _ in range(3)]
        melange = permuter(seqs, "source", graine=1)
        avant = sorted(valeur(p, "source") for s in seqs for p in s.pas)
        apr
… [1012 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/cerveau/tests/test_predictif.py'\ns=open(p).read()\ns=s.replace('''from cerveau.predictif import (Predictif, baseline_tour, controle_negatif,\n                               permuter, valeur)''','''from cerveau.predictif im … [3944 caractères tronqués]`

  ```
patched
test_controle_negatif_tue_le_gain (cerveau.tests.test_predictif.TestPredictif.test_controle_negatif_tue_le_gain) ... ok
test_corpus_action_quasi_constante (cerveau.tests.test_predictif.TestPredictif.test_corpus_action_quasi_constante) ... ok
test_ordre_2_ne_change_rien_sur_constante (cerveau.tests.test_predictif.TestPredictif.test_ordre_2_ne_change_rien_sur_constante) ... ok
test_permutation_conserve_la_marginale (cerveau.tests.test_predictif.TestPredictif.test_permutation_conserve_la_marginale) ... ok
test_structure_alternee_gain (cerveau.tests.test_predictif.TestPredictif.test_structure_alternee_gain) ... ok

======================================================================
FAIL: test_contexte_ameliore_la_surprisal (cerveau.tests.test_predictif.TestContexte.test_contexte_ameliore_la_surprisal)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_predictif.py", line 111, in test_contexte_ameliore_la_surprisal
    self.assertLess(b["surprise"], a["surprise"])
    ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0.0 not less 
… [690 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/cerveau/tests/test_predictif.py'\ns=open(p).read()\ns=s.replace('''    def test_masque_uniforme(self):\n        ctx = \"morpion etat trait=X taille=3 cases=X,O,.,.,.,.,.,.,.\"\n        m = Predictif(\"cible\", 0, contexte=T … [2349 caractères tronqués]`

  ```
patched
test_structure_alternee_gain (cerveau.tests.test_predictif.TestPredictif.test_structure_alternee_gain) ... ok

======================================================================
FAIL: test_contexte_ameliore_la_surprisal (cerveau.tests.test_predictif.TestContexte.test_contexte_ameliore_la_surprisal)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_predictif.py", line 114, in test_contexte_ameliore_la_surprisal
    self.assertEqual(a["n"], b["n"])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
AssertionError: 114 != 161

----------------------------------------------------------------------
Ran 18 tests in 0.174s

FAILED (failures=1)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 300 python3 - <<'EOF'\nfrom cerveau.sequences import corpus\nfrom cerveau.predictif import Predictif\nseqs=corpus(0,12,8); train=seqs[::2]; test=seqs[1::2]\nfor kw in (dict(), dict(contexte=True,melange=0.5)):\n    m=Predictif … [257 caractères tronqués]`

  ```
{} {'n': 114, 'exact': 0.07894736842105263, 'surprise': 2.717095220317985, 'majoritaire': 0.10526315789473684, 'gain_surprise': -0.05370260799425086, 'hors_vocabulaire': 47}
{'contexte': True, 'melange': 0.5} {'n': 161, 'exact': 0.09316770186335403, 'surprise': 3.011707667309716, 'majoritaire': 0.07453416149068323, 'gain_surprise': 0.2855977083458656, 'hors_vocabulaire': 0}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/cerveau/tests/test_predictif.py'\ns=open(p).read()\ns=s.replace('''        a, b = sans.evaluer(test), ctx.evaluer(test)\n        self.assertGreater(a[\"n\"], 0)\n        self.assertEqual(a[\"n\"], b[\"n\"])\n        self.as … [768 caractères tronqués]`

  ```
..................
----------------------------------------------------------------------
Ran 18 tests in 0.177s

OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && tail -30 tools/cerveau/tests/test_gating.py", "description": "Read M6 test tail"}`

  ```
def test_executer(self):
        r = self.porte.executer()
        self.assertEqual(r["n"], 88)
        self.assertAlmostEqual(r["exact"], 83 / 88, places=6)
        self.assertEqual(r["faux_positifs"], 0)
        self.assertEqual(r["faux_negatifs"], 5)
        self.assertAlmostEqual(r["exactitude_equilibree"], (17 / 22 + 1.0) / 2, places=6)
        self.assertAlmostEqual(r["taux_base_tout_non"], 0.75)
        # aucune mémoire : coût de commutation apparié nul...
        self.assertAlmostEqual(r["cout_commutation"], 0.0)
        # ...mais l'instrument le détecte quand on simule une persévération
        self.assertGreater(r["controle_perseveration"], 0.3)

    def test_politiques_simples_au_taux_de_base(self):
        r = self.porte.executer()
        for nom in ("langue", "sens", "tout_non"):
            self.assertAlmostEqual(r["politiques"][nom]["exact"], 0.75, places=6)
        self.assertGreater(r["politiques"]["langue"]["faux_positifs"], 0)
        self.assertGreater(r["politiques"]["sens"]["faux_positifs"], 0)

    def test_compatibilite_typed_corpus(self):
        from semantique.typed_corpus import items
        its = [i for i in items() if i.langue in ("fr", "en")]
      
… [192 caractères tronqués]
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

### 🤖 Assistant

⏵ Tests de la tâche de commutation M6

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/cerveau/tests/test_gating.py'\ns=open(p).read()\ns=s.replace('''from cerveau.gating import CONDITIONS, Porte''','''from cerveau.gating import CONDITIONS, TACHES, Porte''')\ns=s.replace('''\n\nif __name__ == \"__main__\":\n  … [4678 caractères tronqués]`

  ```
patched
test_compatibilite_typed_corpus (cerveau.tests.test_gating.TestTacheConflit.test_compatibilite_typed_corpus) ... ok
test_conditions (cerveau.tests.test_gating.TestTacheConflit.test_conditions) ... ok
test_executer (cerveau.tests.test_gating.TestTacheConflit.test_executer) ... ok
test_langue_deterministe (cerveau.tests.test_gating.TestTacheConflit.test_langue_deterministe) ... ok
test_politiques_simples_au_taux_de_base (cerveau.tests.test_gating.TestTacheConflit.test_politiques_simples_au_taux_de_base) ... ok
test_surfaces_ambigues (cerveau.tests.test_gating.TestTacheConflit.test_surfaces_ambigues) ... ok
test_taille_et_equilibre (cerveau.tests.test_gating.TestTacheConflit.test_taille_et_equilibre) ... ok
test_compatibilite_typed_corpus (cerveau.tests.test_gating.TestTacheSwitch.test_compatibilite_typed_corpus) ... ok
test_conditions_et_consignes (cerveau.tests.test_gating.TestTacheSwitch.test_conditions_et_consignes) ... ok
test_controle_positif_de_perseveration (cerveau.tests.test_gating.TestTacheSwitch.test_controle_positif_de_perseveration) ... ok
test_politiques_temoins (cerveau.tests.test_gating.TestTacheSwitch.test_politiques_temoins) ... ok
test_porte_dure_sans_cout_
… [294 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -12; echo \"code=$?\"", "description": "Run full cerveau test discovery", "timeoutMs": 660000}`

  ```
.......................................................................ssssssss
----------------------------------------------------------------------
Ran 79 tests in 6.213s

OK (skipped=8)
code=0
  ```

### 🤖 Assistant

⏵ Écriture du harnais de mesure 3 graines et des sorties JSON/MD

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"Harnais A6 — M5 (contexte plateau) et M6 (porte de tâche).\n\nÉcrit /tmp/a6-m5-m6.json et /tmp/a6-m5-m6.md. Aucun autre fichier du dépôt\nn'est modifié (le code M5/M6 et ses tests sont dans tools/cerveau/).\n\"\"\"\nfrom __future__ import annotations\n\nimp … [27265 caractères tronqués]`

  ```
<path>/tmp/a6_m5_m6.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && timeout 900 python3 /tmp/a6_m5_m6.py 2>&1 | tail -40", "description": "Run A6 measurement harness", "timeoutMs": 960000}`

  ```
Traceback (most recent call last):
  File "/tmp/a6_m5_m6.py", line 530, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/tmp/a6_m5_m6.py", line 499, in main
    m5a = agreger_m5(m5)
  File "/tmp/a6_m5_m6.py", line 264, in agreger_m5
    m: stats([m5["graines"][str(g)]["cibles"][cle]
              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              ["controle_contextes_permutees"][arm][m]
              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^
KeyError: 'delta_surprise_vs_sans'
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='/tmp/a6_m5_m6.py'\ns=open(p).read()\nold='''                for arm in (\"masque_uniforme\", \"masque_melange\"):\n                    res[\"cibles\"][cle][\"controle_contextes_permutees\"][arm] = \\\\\n                        ev … [1120 caractères tronqués]`

  ```
patched
{
 "secondes": 39.36,
 "m5_cibles": [
  "action_ordre1",
  "action_ordre2",
  "source_ordre1",
  "source_ordre2",
  "cible_ordre1",
  "cible_ordre2"
 ],
 "m6_switch": {
  "n": 792,
  "exact": 0.9494949494949495,
  "effet_conflit": 0.0,
  "effet_commutation": 0.0,
  "controle_perseveration": -0.44318181818181823
 },
 "tests": {
  "m5_m6": {
   "commande": "python3 -m unittest cerveau.tests.test_predictif cerveau.tests.test_gating",
   "code": 0,
   "fin": "",
   "ok": true
  },
  "complet": {
   "commande": "python3 -m unittest discover -s tools/cerveau/tests -t tools",
   "code": 1,
   "fin": "",
   "ok": false
  }
 }
}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -25; echo \"PYCODE=${PIPESTATUS[0]}\"", "description": "Inspect full discovery failure", "timeoutMs": 660000}`

  ```
.............................F.........................................ssssssss
======================================================================
FAIL: test_m8_sommeil (cerveau.tests.test_lesion.TestLesion.test_m8_sommeil)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py", line 69, in test_m8_sommeil
    self.assertEqual(m8["deficit"]["exact_codes_nouveaux"], 0.0)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: [0.0, 0.0, 0.0] != 0.0

----------------------------------------------------------------------
Ran 79 tests in 6.952s

FAILED (failures=1, skipped=8)
PYCODE=1
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '55,80p' tools/cerveau/tests/test_lesion.py && grep -n \"def _m8\" -A 60 tools/cerveau/lesion.py | head -70 && echo '--- git status ---' && git status --porcelain | head -30", "description": "Inspect M8 lesion test and git status"}`

  ```
def test_m6_porte(self):
        m6 = self.r["modules"]["M6"]
        self.assertGreater(m6["deficit"]["canal_langue"], 0.15)
        self.assertGreater(m6["deficit"]["tout_accepter"], 0.6)

    def test_m7_modulation(self):
        m7 = self.r["modules"]["M7"]
        self.assertLess(m7["deficit"]["signal_sur_cle_code"], 0)
        self.assertGreater(m7["deficit"]["cle_code_sans_signal"], 0)
        self.assertLess(m7["deficit"]["surface_vs_fifo"]["rep_surface"], 0)

    def test_m8_sommeil(self):
        m8 = self.r["modules"]["M8"]
        self.assertGreater(m8["deficit"]["champs"], 0.15)
        self.assertEqual(m8["deficit"]["exact_codes_nouveaux"], 0.0)
        self.assertEqual(m8["intacte"]["hybride_exact_queue"], 1.0)

    def test_json(self):
        texte = json.dumps(self.r, ensure_ascii=False, default=str)
        self.assertIn("M8", texte)


if __name__ == "__main__":
    unittest.main()
558:def _m8() -> dict:
559-    """Le sommeil, lésé sur le protocole honnête : code tenu à l'écart.
560-
561-    La lésion est le retrait de tout prototype (repli sur la marginale globale),
562-    mesurée sur le **même** leave-one-code-out que l'intacte. La queue publiée
563-    (96,48
… [3406 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' /tmp/a6-m5-m6.md", "description": "Inspect generated MD part 1"}`

  ```
# M5 (contexte plateau) et M6 (porte de tâche) — A6

Corpus M5 : `cerveau.sequences.corpus(0, 200, 12)`, split par partie 80/20, graines 3, 11, 23. Corpus M6 : surfaces B7 fr/en. Temps : 39.4 s.

## M5 — le plateau est une observation, pas une règle

Le prédicteur reçoit `Pas.contexte` (sortie de `resume_contexte`) et restreint ses valeurs possibles à ce que le plateau autorise : `source` = mes pièces, `cible` = cases non occupées par moi. Le masque est mélangé 50/50 avec la loi temporelle masquée (`masque_melange`) ; `masque_uniforme` et `masque_hist` sont les composantes pures. Aucune règle de déplacement n'est importée.

### Global (moyenne de 3 graines)

| cible | ordre | bras | n | exact | majoritaire | surprisal | gain surv. | Δsurv. vs sans | Δexact vs sans |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| action | 1 | sans | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |
| action | 1 | masque_uniforme | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |
| action | 1 | masque_hist | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |
| action | 1 | masque_melange | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |
| action | 2 | sa
… [7641 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/a6-m5-m6.json'))\na=d['m5_agrege']['cibles']\nfor cle in ('source_ordre1','cible_ordre1'):\n    print('###',cle)\n    for arm in ('sans','masque_uniforme','masque_hist','masque_melange'):\n        … [612 caractères tronqués]`

  ```
### source_ordre1
sans H 3.224 exact 0.1065 n 843.3333333333334
  par jeu {'echecs': {'H': 3.686, 'Ho': 2.357, 'n': 454.6666666666667, 'part': 0.0}, 'dames': {'H': 2.69, 'Ho': 1.152, 'n': 388.6666666666667, 'part': 0.0}}
masque_uniforme H 2.598 exact 0.1655 n 843.3333333333334
  par jeu {'echecs': {'H': 2.768, 'Ho': 2.357, 'n': 454.6666666666667, 'part': 0.691}, 'dames': {'H': 2.401, 'Ho': 1.152, 'n': 388.6666666666667, 'part': 0.187}}
masque_hist H 2.686 exact 0.1655 n 843.3333333333334
  par jeu {'echecs': {'H': 3.205, 'Ho': 2.357, 'n': 454.6666666666667, 'part': 0.362}, 'dames': {'H': 2.086, 'Ho': 1.152, 'n': 388.6666666666667, 'part': 0.393}}
masque_melange H 2.48 exact 0.1655 n 843.3333333333334
  par jeu {'echecs': {'H': 2.796, 'Ho': 2.357, 'n': 454.6666666666667, 'part': 0.67}, 'dames': {'H': 2.116, 'Ho': 1.152, 'n': 388.6666666666667, 'part': 0.373}}
### cible_ordre1
sans H 3.52 exact 0.0865 n 1497.6666666666667
  par jeu {'echecs': {'H': 3.891, 'Ho': 2.786, 'n': 453.3333333333333, 'part': 0.0}, 'dames': {'H': 2.739, 'Ho': 1.118, 'n': 388.6666666666667, 'part': 0.0}, 'go': {'H': 4.976, 'Ho': 4.323, 'n': 368.3333333333333, 'part': 0.0}, 'morpion': {'H': 2.119, 'Ho': 1.497, '
… [2361 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='/tmp/a6_m5_m6.py'\ns=open(p).read()\n# 1) tests capture\nold='''        lignes = [x for x in p.stdout.strip().splitlines() if x.strip()]\n        return {\"commande\": cmd, \"code\": p.returncode,\n                \"fin\": lignes … [5265 caractères tronqués]`

  ```
patched
  "source_ordre2",
  "cible_ordre1",
  "cible_ordre2"
 ],
 "m6_switch": {
  "n": 792,
  "exact": 0.9494949494949495,
  "effet_conflit": 0.0,
  "effet_commutation": 0.0,
  "controle_perseveration": -0.44318181818181823
 },
 "tests": {
  "m5_m6": {
   "commande": "python3 -m unittest cerveau.tests.test_predictif cerveau.tests.test_gating",
   "code": 0,
   "fin": "OK",
   "echecs": [],
   "ok": true
  },
  "complet": {
   "commande": "python3 -m unittest discover -s tools/cerveau/tests -t tools",
   "code": 1,
   "fin": "FAILED (errors=1, skipped=8)",
   "echecs": [
    "ERROR: test_deficits_intacte_moins_lesee (cerveau.tests.test_lesion.TestLesion.test_deficits_intacte_moins_lesee)"
   ],
   "ok": false
  }
 }
}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 -m unittest cerveau.tests.test_lesion.TestLesion.test_deficits_intacte_moins_lesee 2>&1 | tail -30", "description": "Inspect failing lesion test detail", "timeoutMs": 660000}`

  ```
E
======================================================================
ERROR: test_deficits_intacte_moins_lesee (cerveau.tests.test_lesion.TestLesion.test_deficits_intacte_moins_lesee)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_lesion.py", line 117, in test_deficits_intacte_moins_lesee
    m["intacte"][i] - m["lessee"][i],
                      ~~~~~~~~~~~^^^
KeyError: 'exact'

----------------------------------------------------------------------
Ran 1 test in 5.048s

FAILED (errors=1)
  ```

- **bash** `{"command": "sed -n '1,80p' /tmp/a6-m5-m6.md; echo '...'; sed -n '80,170p' /tmp/a6-m5-m6.md", "description": "Inspect updated MD"}`

  ```
# M5 (contexte plateau) et M6 (porte de tâche) — A6

Corpus M5 : `cerveau.sequences.corpus(0, 200, 12)`, split par partie 80/20, graines 3, 11, 23. Corpus M6 : surfaces B7 fr/en. Temps : 39.1 s.

## M5 — le plateau est une observation, pas une règle

Le prédicteur reçoit `Pas.contexte` (sortie de `resume_contexte`) et restreint ses valeurs possibles à ce que le plateau autorise : `source` = mes pièces, `cible` = cases non occupées par moi. `masque_uniforme` restreint la loi à l'uniforme sur les candidats ; `masque_hist` restreint la loi temporelle ; `masque_melange` fait le mélange 50/50 des deux. Aucune règle de déplacement n'est importée.

### Global (moyenne de 3 graines)

| cible | ordre | bras | n | exact | majoritaire | surprisal | gain surv. | Δsurv. vs sans | Δexact vs sans |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| action | 1 | sans | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |
| action | 1 | masque_uniforme | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |
| action | 1 | masque_hist | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |
| action | 1 | masque_melange | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |
… [11760 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/cerveau/predictif.py'\ns=open(p).read()\nold='''    def predire(self, code: dict, precedent=None, contexte=None) -> tuple:\n        \"\"\"Rend (valeur prédite, probabilité). `precedent` est une valeur de cible.\"\"\"\n      … [1893 caractères tronqués]`

  ```
patched
----------------------------------------------------------------------
Ran 18 tests in 0.172s

OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && timeout 900 python3 /tmp/a6_m5_m6.py 2>&1 | tail -12 && echo '---' && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/a6-m5-m6.json'))\nfor cle in ('source_ordre1','cible_ordre1'):\n    print(cle, {a:{'exact':round(d['m5_agrege']['cibles'][cle] … [262 caractères tronqués]`

  ```
"echecs": [],
   "ok": true
  },
  "complet": {
   "commande": "python3 -m unittest discover -s tools/cerveau/tests -t tools",
   "code": 0,
   "fin": "OK (skipped=8)",
   "echecs": [],
   "ok": true
  }
 }
}
---
source_ordre1 {'sans': {'exact': 0.1065, 'H': 3.224}, 'masque_uniforme': {'exact': 0.1655, 'H': 2.598}, 'masque_hist': {'exact': 0.1655, 'H': 2.686}, 'masque_melange': {'exact': 0.1655, 'H': 2.48}}
cible_ordre1 {'sans': {'exact': 0.0865, 'H': 3.52}, 'masque_uniforme': {'exact': 0.1225, 'H': 3.109}, 'masque_hist': {'exact': 0.1226, 'H': 3.208}, 'masque_melange': {'exact': 0.1225, 'H': 3.031}}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='tools/cerveau/predictif.py'\ns=open(p).read()\nold='''        # Le masque est une croyance, pas une certitude : une petite fuite vers\n        # la loi non masquée garde une probabilité finie à une cible que le\n        # plateau … [1021 caractères tronqués]`

  ```
patched
----------------------------------------------------------------------
Ran 18 tests in 0.177s

OK
   "commande": "python3 -m unittest discover -s tools/cerveau/tests -t tools",
   "code": 0,
   "fin": "OK (skipped=8)",
   "echecs": [],
   "ok": true
  }
 }
}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/a6-m5-m6.json'))\nfor cle in ('source_ordre1','source_ordre2','cible_ordre1','cible_ordre2'):\n    print(cle, {a:{'exact':round(d['m5_agrege']['cibles'][cle]['bras'][a]['exact']['moyenne'],4),'H': … [679 caractères tronqués]`

  ```
source_ordre1 {'sans': {'exact': 0.1065, 'H': 3.224}, 'masque_uniforme': {'exact': 0.0797, 'H': 2.598}, 'masque_hist': {'exact': 0.1655, 'H': 2.686}, 'masque_melange': {'exact': 0.1655, 'H': 2.48}}
source_ordre2 {'sans': {'exact': 0.1382, 'H': 3.214}, 'masque_uniforme': {'exact': 0.0797, 'H': 2.598}, 'masque_hist': {'exact': 0.1739, 'H': 2.733}, 'masque_melange': {'exact': 0.1739, 'H': 2.468}}
cible_ordre1 {'sans': {'exact': 0.0865, 'H': 3.52}, 'masque_uniforme': {'exact': 0.0937, 'H': 3.109}, 'masque_hist': {'exact': 0.1226, 'H': 3.208}, 'masque_melange': {'exact': 0.1225, 'H': 3.031}}
cible_ordre2 {'sans': {'exact': 0.108, 'H': 3.521}, 'masque_uniforme': {'exact': 0.0937, 'H': 3.109}, 'masque_hist': {'exact': 0.146, 'H': 3.228}, 'masque_melange': {'exact': 0.1459, 'H': 3.016}}
perm cible1 {'masque_uniforme': {'exact': 0.0372, 'H': 6.68}, 'masque_melange': {'exact': 0.0844, 'H': 6.596}}
tests {'m5_m6': {'code': 0, 'fin': 'OK', 'echecs': []}, 'complet': {'code': 0, 'fin': 'OK (skipped=8)', 'echecs': []}}
runtime 46.7
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| action | 1 | sans | 1574 | 97.4 % | 97.4 % | 0.087 | -0.000 | +0.000 | +0.000 |
| action | 1 | masque_uniforme | 15
… [1634 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='/tmp/a6_m5_m6.py'\ns=open(p).read()\ns=s.replace('''a(\"\\\\n`action` est le témoin : le masque ne s'y applique pas (la cible est \"\n      \"un label de format), donc les quatre bras y sont identiques. \"\n      \"`masque_melang … [2130 caractères tronqués]`

  ```
patched
exit=0
  "action_ordre2",
  "source_ordre1",
  "source_ordre2",
  "cible_ordre1",
  "cible_ordre2"
 ],
 "m6_switch": {
  "n": 792,
  "exact": 0.9494949494949495,
  "effet_conflit": 0.0,
  "effet_commutation": 0.0,
  "controle_perseveration": -0.44318181818181823
 },
 "tests": {
  "m5_m6": {
   "commande": "python3 -m unittest cerveau.tests.test_predictif cerveau.tests.test_gating",
   "code": 0,
   "fin": "OK",
   "echecs": [],
   "ok": true
  },
  "complet": {
   "commande": "python3 -m unittest discover -s tools/cerveau/tests -t tools",
   "code": 0,
   "fin": "OK (skipped=8)",
   "echecs": [],
   "ok": true
  }
 }
}
  ```

### 🤖 Assistant

⏵ Dernières retouches de transparence (n des contrôles, équilibre des blocs) et relance

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\np='/tmp/a6_m5_m6.py'\ns=open(p).read()\n# control n aggregation\ns=s.replace('''                    for m in (\"exact\", \"surprise\", \"delta_surprise_vs_sans\",\n                              \"delta_exact_vs_sans\")}''','''       … [4020 caractères tronqués]`

  ```
patched
exit=0
   "commande": "python3 -m unittest discover -s tools/cerveau/tests -t tools",
   "code": 0,
   "fin": "OK (skipped=8)",
   "echecs": [],
   "ok": true
  }
 }
}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 -c \"import json; d=json.load(open('/tmp/a6-m5-m6.json')); print('json ok', len(json.dumps(d)), 'bytes'); print(d['meta']); print(d['tests'])\" && echo '--- MD sections ---' && grep -n \"Tâche :\\|macro par sonde\\|Intégration\\|## Tests\\|Éch … [110 caractères tronqués]`

  ```
json ok 253522 bytes
{'titre': 'A6 — M5 contexte plateau / M6 porte de tâche', 'date': '2026-10-27 11:09', 'secondes': 46.35, 'graines_m5': [3, 11, 23], 'fraction': 0.8, 'corpus_m5': 'cerveau.sequences.corpus(0, 200, 12)', 'corpus_m6': 'corpus_multilingue B7, fr/en', 'code_modifie': ['tools/cerveau/predictif.py', 'tools/cerveau/gating.py', 'tools/cerveau/tests/test_predictif.py', 'tools/cerveau/tests/test_gating.py']}
{'m5_m6': {'commande': 'python3 -m unittest cerveau.tests.test_predictif cerveau.tests.test_gating', 'code': 0, 'fin': 'OK', 'echecs': [], 'ok': True}, 'complet': {'commande': 'python3 -m unittest discover -s tools/cerveau/tests -t tools', 'code': 0, 'fin': 'OK (skipped=8)', 'echecs': [], 'ok': True}}
--- MD sections ---
1:# M5 (contexte plateau) et M6 (porte de tâche) — A6
88:## M6 — une vraie porte de tâche : deux consignes, conflit, commutation
90:Tâche : 792 essais, 352 commutations et 352 répétitions (blocs appariés, 4 sondes par bloc : go, traduction, langue, ni). Chaque groupe a 9 blocs, 5 `sens` et 4 `langue` : c'est ce qui équilibre exactement commutations et répétitions (une tâche de plus forcerait un déséquilibre de transition). Deux consignes : `sens` (le 
… [866 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 -m unittest cerveau.tests.test_predictif cerveau.tests.test_gating 2>&1 | tail -4 && PYTHONPATH=tools timeout 600 python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -3", "description": "Final  … [52 caractères tronqués]`

  ```
----------------------------------------------------------------------
Ran 31 tests in 0.505s

OK
Ran 85 tests in 8.157s

OK (skipped=8)
  ```

- **bash** `{"command": "sed -n '125,175p' /tmp/a6-m5-m6.md", "description": "Read final MD sections"}`

  ```
- **Commutation** : le coût apparié est nul, et le contrôle de persévération montre que l'instrument aurait vu un coût de 44,3 pt s'il y avait une inertie de tâche.

- **Tâche** : la seule asymétrie est perceptive (langue 88,6 % contre sens 100 %) ; elle vient du classifieur lexical, pas de la porte.

- **Canal lexical** : sur les 22 couples (surface, langue) uniques, il identifie 77.3 % (22 couples) ; les erreurs sont les surfaces identiques fr/en et une ambiguïté lexicale. La tâche `langue` est plus haute (88,6 %) parce qu'elle ne demande qu'un jugement binaire « est-ce la langue cible ? », pas l'identification.

## Tests

- `python3 -m unittest cerveau.tests.test_predictif cerveau.tests.test_gating` : code 0, OK.
- `python3 -m unittest discover -s tools/cerveau/tests -t tools` : code 0, OK (skipped=8).

## Intégration (opt-in, sans toucher aux autres modules)

- M5 : le mode contexte est **opt-in** (`Predictif(contexte=True, melange=0.5)`). Le défaut reste `contexte=False` pour ne pas changer `batterie.m5` ni la lésion M5 de `lesion.py`, qui ne sont pas touchés dans ce sprint ; activer le contexte dans la batterie est un changement d'une ligne, à faire dans une passe dédiée.

- 
… [2378 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git diff --stat -- tools/cerveau/predictif.py tools/cerveau/gating.py tools/cerveau/tests/test_predictif.py tools/cerveau/tests/test_gating.py && echo '--- status all ---' && git status --porcelain | head -20 && echo '--- py_compile ---' && PYTHONPATH … [222 caractères tronqués]`

  ```
tools/cerveau/predictif.py | 10 ++++++----
 1 file changed, 6 insertions(+), 4 deletions(-)
--- status all ---
M  docs/roadmap.md
M  reports/rapport-cerveau-corrections.md
M  tools/cerveau/lesion.py
 M tools/cerveau/predictif.py
M  tools/cerveau/sommeil.py
M  tools/cerveau/tests/test_lesion.py
M  tools/cerveau/tests/test_sommeil.py
 M tools/cerveau/tests/test_voies.py
 M tools/cerveau/voies.py
--- py_compile ---
OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git log --oneline -5 && echo '--- HEAD stat ---' && git show --stat --oneline HEAD | head -30 && echo '--- diff predictif ---' && git diff -- tools/cerveau/predictif.py | head -60", "description": "Inspect recent commits and predictif diff"}`

  ```
9a3f753d B12 — M5 CONTEXTE : SOURCE +0,626 NAT, CIBLE +0,411 ; M6 SÉLECTEUR 94,95 % MAIS CONFLIT 0
5e9ca5d6 B12 — M5 CONTEXTE : SOURCE DAMES 3,27→2,11 NAT ; CIBLE MORPION 2,20→1,52 (ORACLE)
ddbbea24 DOCS — FICHE DE COHÉRENCE (PASSAGE 3) ET COMPTEURS 174/242 ; REVUE, TABLEAUX ET REGISTRE VERTS
b271db7a B12 — M2 : LE SPLIT INÉDIT NE CONTIENT QUE 2–3 CLASSES ; 10,7/13 EST UN PRIORI, PAS UNE LECTURE
530b7043 B12 — STRESS SOUS-AGENTS : M1 SEUL SOLIDE ; M2 VU SEULEMENT ; M3–M8 NÉGATIFS ; M9 PROXY
--- HEAD stat ---
9a3f753d B12 — M5 CONTEXTE : SOURCE +0,626 NAT, CIBLE +0,411 ; M6 SÉLECTEUR 94,95 % MAIS CONFLIT 0
 docs/roadmap.md                        |   4 +-
 journal/2026-10-27.md                  |   5 +-
 journal/2026-10-27_memoire.md          |   3 +-
 reports/rapport-cerveau-corrections.md |   1 +
 tools/cerveau/gating.py                | 276 +++++++++++++++++++++++++++++++++
 tools/cerveau/predictif.py             | 193 +++++++++++++++++++++--
 tools/cerveau/tests/test_gating.py     |  81 +++++++++-
 tools/cerveau/tests/test_predictif.py  |  83 +++++++++-
 8 files changed, 628 insertions(+), 18 deletions(-)
--- diff predictif ---
diff --git a/tools/cerveau/predictif.py b/tools/cerv
… [1133 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/a6-m5-m6.json'))\na=d['m5_agrege']['cibles']\nfor cle in ('source_ordre1','source_ordre2','cible_ordre1','cible_ordre2'):\n    print('###',cle)\n    for arm in ('sans','masque_uniforme','masque_hi … [925 caractères tronqués]`

  ```
### source_ordre1
  sans             exact=0.1065 H=3.224 dH=+0.000 dExact=+0.0000
  masque_uniforme  exact=0.0797 H=2.598 dH=+0.626 dExact=-0.0267
  masque_hist      exact=0.1655 H=2.686 dH=+0.539 dExact=+0.0590
  masque_melange   exact=0.1655 H=2.480 dH=+0.744 dExact=+0.0590
  permute          exact=0.0499 H=12.395 dH=-9.170
### source_ordre2
  sans             exact=0.1382 H=3.214 dH=+0.000 dExact=+0.0000
  masque_uniforme  exact=0.0797 H=2.598 dH=+0.617 dExact=-0.0585
  masque_hist      exact=0.1739 H=2.733 dH=+0.481 dExact=+0.0357
  masque_melange   exact=0.1739 H=2.468 dH=+0.747 dExact=+0.0357
  permute          exact=0.0644 H=12.383 dH=-9.169
### cible_ordre1
  sans             exact=0.0865 H=3.520 dH=+0.000 dExact=+0.0000
  masque_uniforme  exact=0.0937 H=3.109 dH=+0.411 dExact=+0.0072
  masque_hist      exact=0.1226 H=3.208 dH=+0.312 dExact=+0.0361
  masque_melange   exact=0.1225 H=3.031 dH=+0.489 dExact=+0.0360
  permute          exact=0.0844 H=6.596 dH=-3.076
### cible_ordre2
  sans             exact=0.1080 H=3.521 dH=+0.000 dExact=+0.0000
  masque_uniforme  exact=0.0937 H=3.109 dH=+0.412 dExact=-0.0143
  masque_hist      exact=0.1460 H=3.228 dH=+0.292 dExact=+0.0380
  m
… [807 caractères tronqués]
  ```

- **bash** `{"command": "grep -A 16 \"Contrôle négatif\" /tmp/a6-m5-m6.md | head -20", "description": "Check final control table"}`

  ```
### Contrôle négatif : permutation des contextes

| cible | ordre | bras | n | exact | surprisal | Δsurv. vs sans |
|---|---:|---|---:|---:|---:|---:|
| action | 1 | masque_uniforme | 1574 | 97.4 % | 0.087 | +0.000 |
| action | 1 | masque_melange | 1574 | 97.4 % | 0.087 | +0.000 |
| action | 2 | masque_uniforme | 1574 | 97.4 % | 0.087 | +0.000 |
| action | 2 | masque_melange | 1574 | 97.4 % | 0.087 | +0.000 |
| source | 1 | masque_uniforme | 843 | 1.5 % | 12.439 | -9.215 |
| source | 1 | masque_melange | 843 | 5.0 % | 12.395 | -9.170 |
| source | 2 | masque_uniforme | 843 | 1.5 % | 12.439 | -9.225 |
| source | 2 | masque_melange | 843 | 6.4 % | 12.383 | -9.169 |
| cible | 1 | masque_uniforme | 1498 | 3.7 % | 6.680 | -3.160 |
| cible | 1 | masque_melange | 1498 | 8.4 % | 6.596 | -3.076 |
| cible | 2 | masque_uniforme | 1498 | 3.7 % | 6.680 | -3.159 |
| cible | 2 | masque_melange | 1498 | 9.3 % | 6.586 | -3.066 |
  ```

### 🤖 Assistant

⏵ Envoi du résultat final au parent

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "A6 terminé. Livrables : /tmp/a6-m5-m6.json, /tmp/a6-m5-m6.md ; harnais /tmp/a6_m5_m6.py ; code tools/cerveau/predictif.py, tools/cerveau/gating.py, tests/test_predictif.py, tests/test_gating.py.\n\nM5 (corpus 0/200/12, split 80/20 par  … [3052 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

### 🤖 Assistant

⏵ Résultat A6 : M5 gagne avec le plateau, M6 reste un sélecteur sans coût

**M5 — le plateau donne un gain réel de surprisal (3 graines, split 80/20 par partie)**

| cible / ordre | sans contexte | avec plateau (mélange 50/50) | gain |
|---|---:|---:|---:|
| source 1 | 3,224 nat / 10,6 % | 2,480 nat / 16,5 % | **+0,744 nat, +5,9 pt** |
| source 2 | 3,214 nat / 13,8 % | 2,468 nat / 17,4 % | **+0,747 nat, +3,6 pt** |
| cible 1 | 3,520 nat / 8,7 % | 3,031 nat / 12,3 % | **+0,489 nat, +3,6 pt** |
| cible 2 | 3,521 nat / 10,8 % | 3,016 nat / 14,6 % | **+0,504 nat, +3,8 pt** |

`action` est le témoin : les quatre bras y sont identiques (97,4 %, H = 0,087). Le masque ne s'applique pas à un label de format.

- **Oracle A1** : aucun bras ne le dépasse. Le masque uniforme seul l'atteint exactement à go (4,323 nat) et morpion (1,497 nat) ; le mélange comble 78 % (go), 98 % (morpion), 26–67 % (échecs/dames). L'écart restant est la géométrie des coups, pas le plateau.
- **Contrôle négatif** : contextes permutés (même distribution, mauvais pas) → source H ≈ 12,4 (Δ −9,2 nat), cible H ≈ 6,6 (Δ −3,1), exact 1,5–9,3 %. Le gain vient bien du **bon** plateau.
- **Baseline tour** : source 9,5 %, cible 7,7 % ; le contexte la dépasse, sauf `cible` aux échecs à l'exact (6,6 % contre 7,2 %), où la surprisal s'améliore quand même (3,89 → 3,60).
- **Intégration** : mode `Predictif(contexte=True, melange=0.5)` opt-in, défaut `contexte=False` pour ne pas modifier `batterie.m5` ni la lésion M5, qui n'ont pas été touchés.

**M6 — vraie porte de tâche (sens vs langue), conflit et commutation**

792 essais (352 switch / 352 repeat, 396 congruent / 396 incongruent), 9 blocs par groupe : 5 `sens`, 4 `langue`, ce qui équilibre exactement les transitions.

- Porte dure : **94,95 %**, conflit **0,000**, commutation **0,000** ; sens 100 %, langue 88,6 % (macro 92,5 %).
- Témoins : meilleur canal seul 77,8 %, indice aléatoire 73,5 %, inverse 50 %, tout-non 50 % → la consigne apporte +17,1 pt.
- Contrôle positif de persévération : coût de commutation **−44,3 pt**, congruent 0, incongrient −88,6 pt. L'instrument détecte un coût s'il y en a un ; la porte réelle n'en a pas.
- Canal lexical : 77,3 % d'identification sur 22 couples surface × langue ; la tâche langue monte à 88,6 % car c'est un jugement binaire. **Le canal lexical suffit à la tâche langue, pas au sens ; le contrôle exécutif se réduit à un sélecteur de canal**, sans inhibition ni commutation mesurables sur B7.

**Tests** : `PYTHONPATH=tools python3 -m unittest cerveau.tests.test_predictif cerveau.tests.test_gating` → 31 tests OK. Découverte complète → 85 tests OK (8 skipped).

**Fichiers** :
- `/tmp/a6-m5-m6.json`, `/tmp/a6-m5-m6.md` (résultats et fiches)
- `/tmp/a6_m5_m6.py` (harnais reproductible)
- `tools/cerveau/predictif.py`, `tools/cerveau/gating.py`
- `tools/cerveau/tests/test_predictif.py`, `tools/cerveau/tests/test_gating.py`

Aucun commit ; `batterie.py`, docs, reports et journal n'ont pas été touchés. Le commit `9a3f753d` déjà présent contient l'essentiel de A6 ; il reste un petit correctif non committé dans `predictif.py` (fuite uniforme du masque, pour que l'exact du masque uniforme ne soit plus un artefact de tie-break).

