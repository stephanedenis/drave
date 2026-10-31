# Session DSH — relecture

- identifiant : `6f65acfe-ea1e-4ed9-a560-c923bb47b81a`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 15:11:33
- agent : standard


## Tour 1

### 👤 Utilisateur

Dépôt /home/stephane/GitHub/Qtrinet, sprint 24 h. Sous-agent A16 : construire un **Stroop minimal** pour M6, après A6 (sélecteur 94,95 %, conflit 0, commutation 0), sans modifier les modules existants.

État :
- `tools/cerveau/gating.py` : `Porte` ; M6 sélecteur de tâche sens/langue 94,95 %, base 50 %.
- Corpus : `jeux.corpus_multilingue` (449), `semantique.typed_corpus.items`.
- Tests : `PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools` → 127 OK.

Objectif :
1. Créer `tools/cerveau/gating_conflit.py` : essais avec **deux dimensions** (langue du stimulus, sens du stimulus) et une **réponse binaire** (accepter/refuser) qui dépend d'une **règle de tâche** ; essais **congruents/incongrients**, blocs **switch/repeat**.
2. Mesurer exactitude, **effet de conflit** (incongruent − congruent), **coût de commutation**, contrôle positif de persévération ; 3 partitions.
3. Contrôles : réponse aléatoire, tout accepter, tout refuser, stimulus neutre.
4. Écrire `/tmp/a16-m6-conflit.json` et `.md` ; si l'effet de conflit reste 0, le dire.

Contraintes :
- Crée uniquement `tools/cerveau/gating_conflit.py` et `tools/cerveau/tests/test_gating_conflit.py` ; ne modifie pas les modules existants, docs, reports, journal, `batterie.py`, git.
- Pas de `git add/commit/checkout`.
- CPU. Sois autonome, timebox, autocritique. Réponds avec un résumé et les chemins.
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

⏵ Exploration du dépôt et des modules de gating existants.

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls && echo \"---\" && ls tools/cerveau | head -50 && echo \"---\" && ls tools/cerveau/tests", "description": "List repo and cerveau modules"}`

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
m2_secours.py
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
test_m2_secours.py
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

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && wc -l tools/cerveau/gating.py tools/cerveau/jeux.py tools/cerveau/semantique.py 2>/dev/null; echo \"---\"; PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -5", "description": "Check baseline tests and file siz … [4 caractères tronqués]`

  ```
707 tools/cerveau/gating.py
  707 total
---
..................................s.............................................sssssssssss............................ssssssss
----------------------------------------------------------------------
Ran 127 tests in 11.718s

OK (skipped=20)
  ```

### 🤖 Assistant

⏵ Lecture de `gating.py` et localisation des corpus.

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && find . -name \"jeux.py\" -o -name \"semantique.py\" | head; echo \"---\"; grep -rln \"corpus_multilingue\\|typed_corpus\" --include=*.py . | head -20", "description": "Locate corpus modules"}`

  ```
---
./tools/jeux/corpus_multilingue.py
./tools/jeux/mesure_langues.py
./tools/semantique/tests/test_typed_corpus.py
./tools/semantique/typed_corpus.py
./tools/semantique/entrainer_type.py
./tools/semantique/synth_corpus.py
./tools/semantique/hybride.py
./tools/semantique/restitution.py
./tools/cerveau/tests/test_gating.py
./tools/cerveau/tests/test_voies.py
./tools/cerveau/tests/test_pipeline_semantique_m2.py
./tools/cerveau/tests/test_multilingue.py
./tools/cerveau/tests/test_pipeline_memoire.py
./tools/cerveau/tests/test_restitution.py
./tools/cerveau/batterie.py
./tools/cerveau/voies.py
./tools/cerveau/gating.py
./tools/cerveau/lesion.py
./tools/cerveau/sommeil.py
./tools/cerveau/pipeline_semantique.py
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/gating.py"}`

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
… [36714 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des tests existants et des interfaces de corpus.

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_gating.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_gating.py</path>
<type>file</type>
<content>
1: from __future__ import annotations
2: 
3: import unittest
4: 
5: from cerveau.gating import CONDITIONS, TACHES, Porte
6: 
7: 
8: class TestTacheConflit(unittest.TestCase):
9:     @classmethod
10:     def setUpClass(cls):
11:         cls.porte = Porte()
12:         cls.essais = cls.porte.tache_conflit()
13: 
14:     def test_taille_et_equilibre(self):
15:         self.assertEqual(len(self.essais), 88)
16:         for condition in CONDITIONS:
17:             n = sum(1 for e in self.essais if e.condition == condition)
18:             self.assertEqual(n, 22)
19:         # les blocs de 4 essais partagent la même langue cible
20:         for i in range(0, len(self.essais), 4):
21:             bloc = self.essais[i:i + 4]
22:             self.assertEqual(len({e.cible_langue for e in bloc}), 1)
23: 
24:     def test_conditions(self):
25:         for e in self.essais:
26:             if e.condition == "go":
27:                 self.assertEqual(e.langue_vraie, e.cible_langue)
28:                 self.assertEqual(e.code_vrai, e.cible_code)
29:             elif e.condition == "traduction
… [7364 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,120p tools/jeux/corpus_multilingue.py; echo \"=== TYPED ===\"; sed -n 1,140p tools/semantique/typed_corpus.py", "description": "Read corpus interfaces"}`

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
… [6709 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des résultats A6 et de toute mention Stroop.

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rli \"stroop\" --include=*.py --include=*.md --include=*.json . | head -20; echo \"=== A6 ===\"; grep -rli \"94,95\\|94.95\\|94,9\" --include=*.md --include=*.json --include=*.py . | head -20", "description": "Search Stroop and A6 references"}`

  ```
./data/ted2020/ted_fr_en.json
=== A6 ===
./reports/restitution-udhr-flux.json
./reports/alignement-verne.md
./reports/traduction-onu-7b.json
./reports/traduction-onu6-7b.json
./reports/traduction-onu6-3b.json
./reports/kfold-pidgin-tw.json
./reports/kfold-pidgin-7.json
./reports/kfold-tout-0210.json
./reports/kfold-7b-amp-0210.json
./reports/kfold-asp-0210.json
./reports/rapport-cerveau-corrections.md
./reports/cerveau-mesures-corrigees.json
./reports/rapport-pipeline-semantique.md
./reports/rapport-pipeline-m2.md
./reports/m7-frequence.json
./data/alignement/verne_fr_en.json
./data/pidgin.old/wiki_local.json
./data/jrc/jrc_tech_fr_en.json
./tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_cell_widths.py
./tools/docwatch/.venv/lib/python3.13/site-packages/rich/_unicode_data/unicode10-0-0.py
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls reports | tail -40; echo \"---\"; ls /tmp/a1-m5-m6* /tmp/a6* /tmp/a16* 2>/dev/null; echo \"---\"; ls reports | grep -i \"m6\\|gating\\|conflit\" | head", "description": "List reports and temp artifacts"}`

  ```
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
traduction-presse-3b.json
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
---
/tmp/a1-m5-m6.json
/tmp/a1-m5-m6.md
/tmp/a6_explore.py
/tmp/a6_geom.py
/tmp/a6-m5-m6.json
/tmp/a6-m5-m6.md
/tmp/a6_m5_m6.py
/tmp/a6_run.out
---
  ```

### 🤖 Assistant

⏵ Lecture des artefacts A6 pour aligner le Stroop minimal.

- **bash** `{"command": "cd /tmp && head -120 a6-m5-m6.md; echo \"=== JSON KEYS ===\"; python3 -c \"\nimport json\nd=json.load(open('/tmp/a6-m5-m6.json'))\ndef walk(o,p=''):\n    if isinstance(o,dict):\n        for k,v in o.items():\n            print(p+k, type(v).__name__, (v if not isinstance(v,(dict,list)) e … [241 caractères tronqués]`

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
… [10921 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de `voies.py` et `batterie.py` (M6) pour les canaux bruités.

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,100p tools/cerveau/voies.py; echo \"=== batterie m6 ===\"; grep -n \"m6\\|gating\\|Porte\" tools/cerveau/batterie.py | head -30", "description": "Read voies and batterie M6 hooks"}`

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
… [3228 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 120,260p /tmp/a6-m5-m6.md", "description": "Read rest of A6 report"}`

  ```
La consigne vaut +17,1 pt sur le meilleur canal seul (`sens`, 77,8 %) et +21,4 pt sur un indice aléatoire (73.5 %) : la porte **route** bien, et c'est son seul apport. Le coût restant est le canal lexical : la tâche `langue` n'est qu'à 88,6 % (macro 92,5 %), alors que la tâche `sens` est à 100 %. Ce 88,6 % n'est pas le taux d'identification du canal (77,3 % sur les 22 couples surface × langue) : la tâche `langue` est un jugement binaire « est-ce la langue cible ? », dont la moitié des essais sont négatifs, et une détection dans une troisième langue est un négatif correct. Le canal lexical ne suffit donc pas à lui seul (il ne peut pas juger le sens), mais il suffit à la tâche `langue` ; le contrôle exécutif se réduit à un **sélecteur de canal**, sans inhibition ni commutation mesurables sur ce corpus.

### Pourquoi ce n'est pas un coût exécutif caché

- **Conflit** : la porte dure ignore le canal non pertinent ; les essais incongrients ont exactement la même exactitude que les congruents. Le seul « conflit » est dans le corpus (deux dimensions qui se contredisent), pas dans la porte.

- **Commutation** : le coût apparié est nul, et le contrôle de persévération montre que l'instrumen
… [3479 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche d'A16/Stroop dans docs et roadmap.

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -rn \"A16\\|Stroop\\|stroop\" docs journal reports sprints 2>/dev/null | head -30; echo \"=== roadmap M6 ===\"; grep -n \"M6\\|A6\\|A16\" docs/roadmap.md docs/en-cours.md 2>/dev/null | head -40", "description": "Search A16 and M6 in docs"}`

  ```
=== roadmap M6 ===
docs/roadmap.md:27:| **A — le moteur** | A1–A8 : les formats, le placement, le transport, le rejeu, les matériels | A3.4 (Colab), A5.4 (FPGA), A6.2 (MoE local) — **bloqués** |
docs/roadmap.md:101:### A6 — Apprendre des flux
docs/roadmap.md:107:| A6.1 | **Capteur hebbien** : apprendre des journaux d'activation | ✅ mesuré — **négatif** | le capteur coûte +3,0 % ; la création de nœuds par Hebb n'ajoute rien sur 69 % des poids ; et les **produits** n'ajoutent que **+0,0045** de R² sur la couche 6 (la trace linéaire explique déjà 92 %) — [`reports/rapport-hebbien-produits.md`](../reports/rapport-hebbien-produits.md) ; la piste restante : les couches creuses, et le classement par la trace |
docs/roadmap.md:108:| A6.2 | **Routage appris** (MoE) : les experts choisis par les logs | ⏳ | qualité égale, coût de routage ÷10 |
docs/roadmap.md:109:| A6.3 | **Élagage guidé par les logs** : retirer les neurones qui ne s'allument jamais | ✅ mesuré — le critère est **vide** | **0 neurone mort** sur 116 736 (255 jetons) ; **63 %** s'allument à moins de 0,1 % (les rares, pas les morts) ; le top 10 % porte **19 %** de la masse — l'élagage exige un corpus de calibration plus large et 
… [3797 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n 1,60p tools/jeux/corpus.py; echo \"=== codecs ===\"; grep -n \"def lit\\|def codec\" tools/jeux/codecs.py | head; echo \"=== langue_probable ===\"; grep -n \"def langue_probable\" -A 30 tools/jeux/lexique.py", "description": "Read corpus item a … [24 caractères tronqués]`

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
… [2332 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des lignes B12.10 et des rapports M6.

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"B12.10\" -B 3 -A 6 docs/roadmap.md docs/en-cours.md; echo \"=== rapport cerveau M6 ===\"; grep -n \"M6\" -A 8 reports/rapport-cerveau-corrections.md | head -60", "description": "Read B12.10 and M6 report context"}`

  ```
docs/roadmap.md-25-| programme | ce qui est mesuré | ce qui reste ouvert |
docs/roadmap.md-26-|---|---|---|
docs/roadmap.md-27-| **A — le moteur** | A1–A8 : les formats, le placement, le transport, le rejeu, les matériels | A3.4 (Colab), A5.4 (FPGA), A6.2 (MoE local) — **bloqués** |
docs/roadmap.md:28:| **B — l'intelligence** | B1–B12 : la langue, la pensée, les jeux, les maîtres, le banc externe, la sémantique | B1.5 (corpus), B10.3 (décodeur), B12.10 (modules) |
docs/roadmap.md-29-
docs/roadmap.md-30-**Charger ce bloc, puis la section A ou B** ; le document entier (450 lignes) est une référence, pas un
docs/roadmap.md-31-chargement par défaut. Le détail de chaque ligne est dans les tableaux ci-dessous.
docs/roadmap.md-32-
docs/roadmap.md-33-
docs/roadmap.md-34----
--
docs/roadmap.md-359-| B12.7 | **M7 neuromodulation** | ❌ **nul** | 3,64 % = plafond 16/439 ; LFU +23,1 pts sur les répétés, nouveauté −19,6, incertitude −38,7, récompense −53,3 ; aucun signal ne bat FIFO |
docs/roadmap.md-360-| B12.8 | **M8 sommeil** | ❌ **marginal** | 96,48 % de champs mais exact **65,1 %**, baseline par jeu **96,10 %** ; leave-one-code-out exact **0 % par construction**, non nuls 63,5 % ; coordonné
… [8031 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && find tools -name \"codecs*\" -o -name \"codec*\" | head; echo \"---\"; grep -rn \"def codec\" tools/jeux | head", "description": "Locate codec module"}`

  ```
tools/jeux/codecs
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/idna/codec.py
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/idna/__pycache__/codec.cpython-313.pyc
tools/docwatch/.venv/lib/python3.13/site-packages/idna/codec.py
tools/docwatch/.venv/lib/python3.13/site-packages/idna/__pycache__/codec.cpython-313.pyc
---
tools/jeux/codecs/base.py:180:def codec(jeu: str) -> Codec:
  ```

### 🤖 Assistant

⏵ Exploration des surfaces disponibles et de leur lisibilité par la porte.

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'EOF'\nfrom collections import defaultdict\nfrom jeux.corpus_multilingue import construire_corpus_multilingue\nfrom semantique.typed_corpus import items as titems\nfrom semantique.universaux import empreinte_code, code_ite … [866 caractères tronqués]`

  ```
codes: 11
026fcaf91bfafd5b70454a2ef8e062c5c7f3fcd2727e4726311fc7c3c2213760 {'en': ['jack clubs'], 'fr': ['valet trefle']}
18913d13d9183327005fea34ea23db9e6be8ff960b49f00e1a5185b20a0c14f3 {'en': ['queen diamond'], 'fr': ['dame carreau']}
2654475081e3243a8d3d1a7feeb5fbf286be8e931f47ba3da8e90a22ed5f24e0 {'en': ['10 heart'], 'fr': ['10 coeur']}
290e3e8c8ee0e48303c25739b4bb13b4e4a357f5d41d51e11bdf2bd82bbe6a48 {'en': ['pass'], 'fr': ['passe']}
5c1e91f4acf686297510d9da395a1a8397827a794ea163ccb609ab472fd8403a {'en': ['pawn e2 e4'], 'fr': ['pion e2 e4']}
5fa9f445c7566a368bd21e51e147d82ae80495521fef16e07aa80af33eaff3bd {'en': ['go D4'], 'fr': ['go D4']}
ab969ceab4a1d29ea984dd0da125ef02a495fd6a473d6051c60c576ae895c76a {'en': ['king spade'], 'fr': ['roi pique']}
bba31d555c8bfb0a6422f3238d9ae4490a1bc7514420144f26f2f5a0885a4f0f {'en': ['english draughts b6 c5'], 'fr': ['dames anglaises b6 c5']}
d0cfbddffbec8ff20bd8ebcabbb11b7b74512719c7f89fc3cf975a6434056cae {'en': ['ace heart'], 'fr': ['as coeur']}
d63510d3d94ceb8b70cfe7a9a94c36a33e6752c5fbf783236ce7ef2e7dcf0ace {'en': ['tic-tac-toe A1'], 'fr': ['tic-tac-toe A1']}
e086eb9b630c4afc3ca183bc30c5027a80d2a8f152c55b3dc2262673c6ccbea1 {'en': ['knight 
… [3405 caractères tronqués]
  ```

### 👤 Utilisateur

Agent f0969e87-af0c-43b1-93cf-f278d9c90846 sent a message: 
Timebox : donne un point et écris /tmp/a16-m6-conflit.json/.md dès qu'une mesure existe, même partielle ; termine ensuite.

