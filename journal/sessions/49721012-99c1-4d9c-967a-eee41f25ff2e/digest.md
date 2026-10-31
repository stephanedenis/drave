# Session DSH — relecture

- identifiant : `49721012-99c1-4d9c-967a-eee41f25ff2e`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 12:11:36
- agent : standard


## Tour 1

### 👤 Utilisateur

Dépôt /home/stephane/GitHub/Qtrinet, sprint autonome 24 h. Sous-agent A11 : revisiter M7 après le négatif A2, sans toucher aux autres modules.

État A2 :
- `tools/cerveau/neuromodulation.py` : `MemoireLimitee` (capacité 16), politiques FIFO/LRU/LFU/gel/… ; 30 permutations appariées.
- 3,64 % = plafond 16/439 ; LFU +23,1 pts de répétés (30/30), +4,25 pts suffixe surface ; nouveauté −19,6, incertitude −38,7, récompense −53,3. Aucun signal neuromodulateur ne bat FIFO ; la fréquence, si.
- Tests : `PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools` → 86 OK (8 skip sans torch).

Objectif : construire un module **M7-bis** honnête, `MemoireFrequence`, qui :
1. utilise **LFU** (fréquence) comme politique de base, et **LFU + récence** (LFU avec départage par récence) ;
2. compare à FIFO/LRU sur 30 permutations, avec **rétention des répétés**, des nouveaux, suffixe code/surface ;
3. teste si un signal **contextuel** (jeu, longueur, type) bat LFU ; contrôle **clé permutée** ;
4. Écrire `/tmp/a11-m7-lfu.json` et `.md` ; si LFU + récence ne bat pas LFU, le dire.

Contraintes :
- Modifie uniquement `tools/cerveau/neuromodulation.py` et `tools/cerveau/tests/test_neuromodulation.py` ; ne touche pas aux autres modules, docs, reports, journal, `batterie.py`, git.
- Pas de `git add/commit/checkout`.
- CPU. Sois autonome, mesure, autocritique. Réponds avec un résumé et les chemins.
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

⏵ Cartographie du dépôt et lecture du module M7 existant

- **bash** `{"command": "ls /home/stephane/GitHub/Qtrinet && echo '---' && ls /home/stephane/GitHub/Qtrinet/tools/cerveau | head -50", "description": "List repo root and cerveau directory"}`

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
pipeline_semantique.py
predictif.py
__pycache__
sequences.py
sommeil.py
tests
voies.py
  ```

- **bash** `{"command": "wc -l /home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_neuromodulation.py 2>/dev/null; ls /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/ 2>/dev/null", "description": "Check sizes of key files"}`

  ```
568 /home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py
   70 /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_neuromodulation.py
  638 total
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
test_pipeline_semantique.py
test_predictif.py
test_sommeil.py
test_voies.py
  ```

- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py"}`
- **read** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_neuromodulation.py"}`

  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """M7 — neuromodulation : nouveauté, incertitude, récompense, rétention bornée.
3: 
4: Le module ne change pas le code : il change le **poids d'écriture** dans une
5: mémoire épisodique bornée. La question mesurable n'est pas « le poids bouge-t-il ? »
6: (oui, par construction) mais « la politique de rétention qui en résulte retient-elle
7: mieux ce qui sera redemandé ? ».
8: 
9: Trois corrections de banc, mesurées ici :
10: 
11: 1. **Plafond de la métrique historique.** La batterie comptait la rétention des
12:    surfaces nouvelles : 16 places / 439 surfaces = **3,64 %**. C'est le plafond
13:    de *toute* mémoire à 16 places qui garde des surfaces distinctes. La métrique
14:    ne peut donc pas distinguer deux politiques : 3,64 % n'est pas un résultat,
15:    c'est la capacité divisée par le vocabulaire.
16: 2. **Le comparateur n'était pas FIFO.** `MemoireLimitee.stocker` triait par poids
17:    et tronquait ; à poids égaux le tri est stable, donc la mémoire gardait les
18:    16 **premiers** arrivés (« gel »), pas les 16 derniers. `politique="gel"
… [27793 caractères tronqués]
  ```


  ```
<path>/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_neuromodulation.py</path>
<type>file</type>
<content>
1: from __future__ import annotations
2: 
3: import unittest
4: 
5: from cerveau.neuromodulation import (MemoireLimitee, Neuromodulation,
6:                                      experience_m7, preparer_flux)
7: 
8: 
9: class TestNeuromodulation(unittest.TestCase):
10:     def test_fifo_evince_le_plus_ancien(self):
11:         m = MemoireLimitee(2, politique="fifo")
12:         for s in ("a", "b", "c"):
13:             m.stocker(s, {"surface": s})
14:         self.assertFalse(m.contient("a"))
15:         self.assertTrue(m.contient("b"))
16:         self.assertTrue(m.contient("c"))
17: 
18:     def test_gel_garde_les_premiers(self):
19:         m = MemoireLimitee(2, politique="gel")
20:         for s in ("a", "b", "c"):
21:             m.stocker(s, {"surface": s})
22:         self.assertTrue(m.contient("a"))
23:         self.assertTrue(m.contient("b"))
24:         self.assertFalse(m.contient("c"))
25: 
26:     def test_cle_code_dedouble(self):
27:         c1 = {"jeu": "echecs", "action": "deplacer", "de": 1, "vers": 2}
28:         c2 = {"jeu": "echecs", "action": "deplac
… [2044 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de la base : tests, corpus, champs disponibles

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -5", "description": "Run baseline cerveau tests"}`

  ```
..............................................................................ssssssss
----------------------------------------------------------------------
Ran 86 tests in 7.799s

OK (skipped=8)
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -c \"\nfrom semantique.typed_corpus import items\nits = items()\nprint('n items:', len(its))\nprint('jeux:', sorted({it.jeu for it in its}))\nprint('surfaces distinctes:', len({it.texte for it in its}))\nprint('codes distincts … [254 caractères tronqués]`

  ```
n items: 528
jeux: ['cartes', 'dames', 'echecs', 'go', 'morpion']
surfaces distinctes: 439
codes distincts: 29
champs: Counter({('action', 'carte', 'case', 'chemin_0', 'chemin_1', 'chemin_2', 'de', 'jeu', 'passe', 'point', 'promotion', 'roque', 'symbole', 'taille', 'vers'): 528})
exemple: ItemType(texte='A1', code={'jeu': 'morpion', 'action': 'jouer_case', 'de': None, 'vers': None, 'promotion': None, 'roque': None, 'case': 0, 'symbole': 'X', 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}, jeu='morpion', nature='coup', langue='fr', paire='morpion-a1', format='cellule', contexte='morpion etat trait=X taille=3 cases=.,.,.,.,.,.,.,.,.')
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && ls /tmp/a11* /tmp/*m7* 2>/dev/null; ls reports/ | grep -i -E 'm7|a2|neuromod' | head; ls reports/fiches 2>/dev/null | head -5", "description": "Look for prior A2 artifacts"}`

  ```
/tmp/a2-m7-m8-m9.json
/tmp/a2-m7-m8-m9.md
/tmp/a2-m7-m8-m9-part1.md
/tmp/a2-m7-m8-m9-part2.md
/tmp/a2-m7-m8-m9-part3.md
/tmp/battery-m7.out

/tmp/tmpm7bkko6r:
cd6968324caab816ac0186bd2615c9f48cff0c412ae43e6a9c08229485ce6d5d.json

/tmp/tmpm7q9_hov:
d6309360a6a572047bb5d850e48248fb828821fde16fe21c197f84ff3e901cf0.json
  ```

- **bash** `{"command": "cd /tmp && head -80 a2-m7-m8-m9.md && echo '=== part1 ===' && head -50 a2-m7-m8-m9-part1.md", "description": "Read prior A2 report summary"}`

  ```
# A2 — M7/M8/M9 : neuromodulation, sommeil, lésions

> Sous-agent M7/M8/M9, sprint 24 h, CPU uniquement. Date : 2026-10-27 10:10:16.
> JSON complet : `/tmp/a2-m7-m8-m9.json`. Code : `tools/cerveau/neuromodulation.py`, `sommeil.py`, `lesion.py`.

## 0. Résumé

| module | mesure | résultat | verdict |
|---|---|---|---|
| **M7** | rétention bornée, 30 permutations appariées | plafond surface **3,6446 %** = 16/439 ; aucun signal ne bat FIFO ; LFU = +23,1 pts de répétés ; nouveauté surface = −19,6 pts ; incertitude = −38,7 pts de suffixe code ; récompense = −53,3 pts | **négatif net** : la modulation ne paie pas ; la fréquence, si |
| **M8** | prototypes vs codes neufs | 96,48 % champs reproduit ; exact **65,09 %** (pas 0 %) ; non nuls **85,96 %** ; codes uniques **24,14 %** ; codes neufs exact **0 %** ; baseline per-game 96,10 % ; hybride 100 % sur la queue = mémorisation | **négatif net** : 96,48 % est le plafond de la marginale, pas une généralisation |
| **M9** | lésions par module | M1 0,292 ; M2 0,524/0,630 (double dissociation) ; M3 1,0 ; M4 1,0 ; M5 0,037 ; M6 0,193 ; M7 déficit négatif ; M8 0,184 (champs) / 0,651 (exact) ; sham 0 partout | **table mesurée** ; M5/M7/M8 sont les 
… [9269 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -c \"\nimport json\nd = json.load(open('/tmp/a2-m7-m8-m9.json'))\nprint(list(d.keys()))\nprint(json.dumps(d.get('m7', d.get('M7', {})), ensure_ascii=False, indent=1)[:3000])\n\" 2>&1 | head -100", "description": "Inspect A2 JS … [14 caractères tronqués]`

  ```
['meta', 'M7', 'M8', 'M9', 'M2_reference_neuronale', 'fichiers', 'tests', 'limites', 'M9_part', 'avertissements']
{
 "protocole": {
  "n": 528,
  "prefixe": 422,
  "suffixe": 106,
  "capacite": 16,
  "permutations": 30,
  "graine": 0,
  "metriques": {
   "ret_surface_prefixe": "surfaces retenues / surfaces distinctes vues au préfixe",
   "ret_surface_finale": "surfaces retenues / surfaces distinctes du flux (dénominateur historique, plafonné)",
   "ret_code": "codes retenus / codes distincts vus au préfixe",
   "rep_surface": "écritures répétées dont la surface était déjà en mémoire",
   "rep_code": "écritures répétées dont le code était déjà en mémoire",
   "suf_surface": "queries du suffixe dont la surface est en mémoire (mémoire gelée)",
   "suf_code": "queries du suffixe dont le code est en mémoire (mémoire gelée)"
  },
  "plafonds": {
   "surface_finale": 0.03644646924829157,
   "code": 0.5517241379310345,
   "surface_prefixe": 0.037914691943127965
  }
 },
 "politiques": {
  "fifo": {
   "ret_surface_prefixe": {
    "moyenne": 0.04486314188570239,
    "ecart_type": 0.0005925355985270714,
    "min": 0.043835616438356165,
    "max": 0.04610951008645533,
    "n": 30
   },
   "ret
… [1560 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -c \"\nfrom semantique.typed_corpus import items\nfrom collections import Counter\nits = items()\nprint('natures:', Counter(it.nature for it in its))\nprint('jeux:', Counter(it.jeu for it in its))\nprint('langues:', Counter(it … [765 caractères tronqués]`

  ```
natures: Counter({'coup': 528})
jeux: Counter({'cartes': 161, 'echecs': 146, 'go': 87, 'dames': 70, 'morpion': 64})
langues: Counter({'fr': 55, 'notation': 31, 'en': 15, 'de': 11, 'es': 11, 'it': 11, 'ja': 11, 'nl': 11, 'pl': 11, 'pt': 11, 'ru': 11, 'zh': 11, 'cs': 10, 'da': 10, 'eo': 10, 'et': 10, 'fa': 10, 'fi': 10, 'hu': 10, 'nb': 10, 'sl': 10, 'sr': 10, 'sv': 10, 'uk': 10, 'vi': 10, 'sq': 9, 'ar': 8, 'bn': 8, 'ca': 8, 'eu': 8, 'af': 8, 'be': 8, 'lv': 7, 'tr': 7, 'el': 6, 'ko': 6, 'sk': 6, 'th': 6, 'gl': 5, 'he': 5, 'hr': 5, 'id': 5, 'lt': 5, 'ms': 5, 'ro': 5, 'hy': 5, 'hi': 4, 'is': 4, 'ka': 4, 'mk': 4, 'nn': 4, 'ta': 4, 'ur': 4, 'az': 4, 'bs': 4, 'cy': 4, 'mn': 4, 'uz': 4, 'sw': 3, 'ga': 3, 'kk': 2, 'ne': 2, 'am': 1, 'km': 1, 'pa': 1, 'so': 1, 'zu': 1})
actions: Counter({'jouer_carte': 161, 'deplacer': 144, 'prendre': 70, 'poser': 70, 'jouer_case': 64, 'passer': 17, 'promouvoir': 2})
longueurs surface: Counter({5: 72, 11: 71, 10: 64, 12: 47, 9: 41, 8: 34, 13: 24, 7: 23, 14: 20, 6: 19, 4: 18, 2: 14, 15: 14, 3: 10, 22: 10, 18: 9, 17: 7, 16: 7, 23: 6, 21: 5, 20: 4, 19: 3, 30: 2, 26: 2, 25: 1, 24: 1})
tailles code: Counter({None: 441, 9: 87})
surfaces freq top: [('go D4', 35), ('г
… [1772 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -c \"\nfrom cerveau.neuromodulation import preparer_flux\nep = preparer_flux()\nfrom collections import Counter\nprint('ep', len(ep), 'incertitude moyenne', sum(e.incertitude for e in ep)/len(ep))\nprint('recompense', sum(e.re … [190 caractères tronqués]`

  ```
ep 528 incertitude moyenne 0.06571969696969698
recompense 72.0
jeux Counter({'cartes': 161, 'echecs': 146, 'go': 87, 'dames': 70, 'morpion': 64})
codes 29
  ```

### 🤖 Assistant

⏵ Mesure des repères A2 (oracle, tailles d'effet) avant conception

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 900 python3 -c \"\nimport json, time\nfrom cerveau.neuromodulation import experience_m7\nt=time.time()\nr = experience_m7(permutations=30, synthetique=False)\nprint('duree', round(time.time()-t,2))\nprint('oracle', {k: round(v … [519 caractères tronqués]`

  ```
duree 3.92
oracle {'suf_surface': 0.2428, 'suf_code': 0.9849}
fifo {'ret_surface_prefixe': 0.0449, 'ret_code': 0.3343, 'rep_surface': 0.2874, 'rep_code': 0.7611, 'suf_surface': 0.0503, 'suf_code': 0.717}
lru {'ret_surface_prefixe': 0.0449, 'ret_code': 0.3356, 'rep_surface': 0.337, 'rep_code': 0.7659, 'suf_surface': 0.0594, 'suf_code': 0.7189}
lfu {'ret_surface_prefixe': 0.0449, 'ret_code': 0.3296, 'rep_surface': 0.5187, 'rep_code': 0.7734, 'suf_surface': 0.0928, 'suf_code': 0.7469}
gel {'ret_surface_prefixe': 0.0449, 'ret_code': 0.3437, 'rep_surface': 0.4121, 'rep_code': 0.7858, 'suf_surface': 0.0667, 'suf_code': 0.7506}
delta lfu {'rep_surface': (0.2313, 30), 'suf_surface': (0.0425, 27), 'suf_code': (0.0299, 16)}
delta lru {'rep_surface': (0.0496, 30), 'suf_surface': (0.0091, 5), 'suf_code': (0.0019, 2)}
  ```

### 🤖 Assistant

⏵ Conception de M7-bis : LFU, LFU+récence, contextes et contrôle permuté

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git status --short 2>/dev/null | head -20; echo '---'; tail -20 tools/cerveau/tests/test_neuromodulation.py", "description": "Check working tree and test tail"}`

  ```
M docs/README.md
?? tools/cerveau/pipeline_semantique_m2.py
---
    def test_experience(self):
        ep = preparer_flux()
        r = experience_m7(ep, permutations=5, synthetique=False)
        plafond = r["protocole"]["plafonds"]
        self.assertAlmostEqual(plafond["surface_finale"], 16 / 439)
        self.assertAlmostEqual(plafond["code"], 16 / 29)
        self.assertTrue(r["verdict"]["plafond_surface_atteint_par_toutes"])
        self.assertTrue(r["verdict"]["gel_egal_fifo_sur_la_metrique_historique"])
        # la nouveauté par surface ne bat pas FIFO sur les répétés
        d = r["deltas_vs_fifo"]["nouveaute"]
        self.assertLess(d["rep_surface"]["moyenne"], 0)
        # la clé code, elle, améliore le suffixe
        self.assertGreater(r["deltas_vs_fifo"]["fifo_code"]["suf_code"]["moyenne"], 0)
        # contrôle nul : FIFO contre lui-même
        for m, v in r["controles"]["fifo_contre_lui_meme"].items():
            self.assertEqual(v["moyenne"], 0.0)


if __name__ == "__main__":
    unittest.main()
  ```

### 👤 Utilisateur

Agent f0969e87-af0c-43b1-93cf-f278d9c90846 sent a message: 
Timebox : donne un point et écris /tmp/a11-m7-lfu.json/.md dès qu'une mesure existe, même partielle ; termine ensuite.

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '555,568p' tools/cerveau/neuromodulation.py", "description": "Confirm insertion point at module end"}`

  ```
"politiques": moyennes,
        "deltas_vs_fifo": deltas,
        "verdict": {
            "lfu_bat_fifo": deltas["lfu_code"]["suf_code"]["moyenne"] > 0,
            "recompense_informative_bat_fifo": deltas["recompense_code"]["suf_code"]["moyenne"] > 0,
            "hasard_non_significatif": abs(deltas["hasard"]["suf_code"]["moyenne"]) < 0.10,
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(experience_m7(permutations=10), ensure_ascii=False,
                     indent=1))
  ```

### 🤖 Assistant

⏵ Implémentation de `MemoireFrequence` et du banc M7-bis dans le module

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", "old_string": "if __name__ == \"__main__\":\n    import json\n    print(json.dumps(experience_m7(permutations=10), ensure_ascii=False,\n                     indent=1))", "new_string": "# --------------------------------- … [26214 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -c \"\nimport time\nfrom cerveau.neuromodulation import experience_m7_bis\nt=time.time()\nr = experience_m7_bis(permutations=3, synthetique=False)\nprint('duree', round(time.time()-t,2))\nprint('n configs', len(r['configuratio … [653 caractères tronqués]`

  ```
duree 1.91
n configs 33
verdict beta0 {'jeu': True, 'longueur': True, 'type': True}
plafond 0.03644646924829157
lfu {'rep_surface': 0.5681, 'suf_surface': 0.0912, 'suf_code': 0.7201, 'ret_nouveaux_utiles': 0.2319}
lfu_recence {'rep_surface': 0.5681, 'suf_surface': 0.0912, 'suf_code': 0.7201, 'ret_nouveaux_utiles': 0.2319}
lfu_code {'rep_surface': 0.2784, 'suf_surface': 0.0566, 'suf_code': 0.9654, 'ret_nouveaux_utiles': 0.0698}
lfu_recence_code {'rep_surface': 0.2784, 'suf_surface': 0.0566, 'suf_code': 0.9654, 'ret_nouveaux_utiles': 0.0698}
contexte_jeu {'rep_surface': 0.0907, 'suf_surface': 0.022, 'suf_code': 0.4591, 'ret_nouveaux_utiles': 0.0502}
lfu_contexte_jeu {'rep_surface': 0.4471, 'suf_surface': 0.0692, 'suf_code': 0.6887, 'ret_nouveaux_utiles': 0.1421}
contexte_jeu_permute {'rep_surface': 0.2687, 'suf_surface': 0.0409, 'suf_code': 0.7107, 'ret_nouveaux_utiles': 0.0904}
delta rec {'ret_nouveaux_utiles': (0.0, 0), 'rep_surface': (0.0, 0), 'suf_surface': (0.0, 0)}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -c \"\nfrom cerveau.neuromodulation import MemoireFrequence\n# scénario capacité 2 : a,b,b,a,c -> lfu garde b ; lfu_recence garde a\nfor pol in ('lfu','lfu_recence'):\n    m=MemoireFrequence(2, politique=pol)\n    for s in ('a … [223 caractères tronqués]`

  ```
lfu [('b', 2, 2, 3), ('c', 1, 5, 5)]
lfu_recence [('a', 2, 1, 4), ('c', 1, 5, 5)]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 -c \"\nimport time\nfrom cerveau.neuromodulation import experience_m7_bis\nt=time.time()\nr = experience_m7_bis(permutations=30, synthetique=True)\nprint('duree', round(time.time()-t,2))\nfor nom in ('fifo','lru',' … [819 caractères tronqués]`

  ```
Traceback (most recent call last):
  File "<string>", line 11, in <module>
    d=r['deltas_vs_lfu'][nom]
      ~~~~~~~~~~~~~~~~~~^^^^^
KeyError: 'lfu_code'
duree 14.54
fifo {'ret_surface_prefixe': 0.0449, 'ret_nouveaux_utiles': 0.101, 'ret_code': 0.3343, 'rep_surface': 0.2874, 'rep_code': 0.7611, 'suf_surface': 0.0503, 'suf_code': 0.717}
lru {'ret_surface_prefixe': 0.0449, 'ret_nouveaux_utiles': 0.1072, 'ret_code': 0.3356, 'rep_surface': 0.337, 'rep_code': 0.7659, 'suf_surface': 0.0594, 'suf_code': 0.7189}
lfu {'ret_surface_prefixe': 0.0449, 'ret_nouveaux_utiles': 0.1883, 'ret_code': 0.3296, 'rep_surface': 0.5187, 'rep_code': 0.7734, 'suf_surface': 0.0928, 'suf_code': 0.7469}
lfu_recence {'ret_surface_prefixe': 0.0449, 'ret_nouveaux_utiles': 0.1883, 'ret_code': 0.3296, 'rep_surface': 0.5187, 'rep_code': 0.7734, 'suf_surface': 0.0928, 'suf_code': 0.7469}
lfu_code {'ret_surface_prefixe': 0.0449, 'ret_nouveaux_utiles': 0.0785, 'ret_code': 0.5853, 'rep_surface': 0.2622, 'rep_code': 0.9828, 'suf_surface': 0.044, 'suf_code': 0.95}
lfu_recence_code {'ret_surface_prefixe': 0.0449, 'ret_nouveaux_utiles': 0.0785, 'ret_code': 0.5853, 'rep_surface': 0.2622, 'rep_code': 0.9826, 'suf_surface': 0
… [574 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -c \"\nimport random, collections\nfrom cerveau.neuromodulation import preparer_flux\nep = preparer_flux(); n=len(ep); prefixe=int(n*0.8)\nfor k in range(5):\n    ordre=list(range(n)); random.Random(k).shuffle(ordre)\n    c=co … [685 caractères tronqués]`

  ```
perm 0 surfaces prefixe 357 freq>=2 24 freq>=3 7
perm 1 surfaces prefixe 358 freq>=2 23 freq>=3 6
perm 2 surfaces prefixe 354 freq>=2 28 freq>=3 7
perm 3 surfaces prefixe 359 freq>=2 23 freq>=3 9
perm 4 surfaces prefixe 362 freq>=2 20 freq>=3 8
perm 0 utiles 34 dont freq_prefixe>=2 24
perm 1 utiles 33 dont freq_prefixe>=2 23
perm 2 utiles 32 dont freq_prefixe>=2 28
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -c \"\nimport random\nfrom cerveau.neuromodulation import preparer_flux, MemoireFrequence\nep=preparer_flux(); n=len(ep); prefixe=int(n*0.8)\nfor k in range(3):\n    ordre=list(range(n)); random.Random(k).shuffle(ordre)\n    e … [591 caractères tronqués]`

  ```
perm 0 intersection 16 diff []
 lfu [(29, 'go D4'), (6, 'dama b6 c5'), (3, 'pion e2 e4'), (2, 'bonde e2 e4'), (2, '10 srdce'), (1, 'গো D4'), (1, 'گو D4'), (1, 'רגלי e2 e4'), (1, 'коњ g1 f3'), (1, 'tic-tac-toe A1'), (1, 'springer g1 f3'), (1, 'pestininkas e2 e4'), (1, 'peon e2 e4'), (1, 'peo e2 e4'), (1, 'pass'), (1, '10 срце')]
perm 1 intersection 16 diff []
 lfu [(28, 'go D4'), (4, 'tic-tac-toe A1'), (4, 'dama b6 c5'), (2, 'ratsu g1 f3'), (2, 'pion e2 e4'), (1, 'សេះ g1 f3'), (1, 'غو D4'), (1, 'английские шашки b6 c5'), (1, 'pedone e2 e4'), (1, 'marchog g1 f3'), (1, 'kuda g1 f3'), (1, 'huszar g1 f3'), (1, 'hiruko artzain-joko A1'), (1, 'fanti spathiu'), (1, 'e2e4'), (1, 'b6-c5')]
perm 2 intersection 16 diff []
 lfu [(28, 'go D4'), (6, 'pion e2 e4'), (5, 'dama b6 c5'), (2, 'пешка e2 e4'), (2, 'passen'), (2, 'dam b6 c5'), (2, 'A1'), (1, 'หมากฮอส b6 c5'), (1, 'пас'), (1, 'tammi b6 c5'), (1, 'kral piky'), (1, 'checkers b6 c5'), (1, 'cavallo g1 f3'), (1, 'angla damludo b6 c5'), (1, 'a co'), (1, '10 ercens')]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -c \"\nimport random\nfrom cerveau.neuromodulation import preparer_flux, MemoireFrequence\nep=preparer_flux(); n=len(ep); prefixe=int(n*0.8)\nordre=list(range(n)); random.Random(0).shuffle(ordre)\nm1=MemoireFrequence(16, polit … [585 caractères tronqués]`

  ```
aucune divergence sur tout le prefixe
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -c \"\nimport random\nfrom cerveau.neuromodulation import preparer_flux, MemoireFrequence\nep=preparer_flux(); n=len(ep); prefixe=int(n*0.8)\nclass Debug(MemoireFrequence):\n    def __init__(self,*a,**k):\n        super().__in … [823 caractères tronqués]`

  ```
0 evictions 369 sans freq1 0 desaccords 0
1 evictions 371 sans freq1 0 desaccords 0
2 evictions 366 sans freq1 0 desaccords 0
3 evictions 377 sans freq1 0 desaccords 0
4 evictions 370 sans freq1 0 desaccords 0
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 -c \"\nimport time, json\nfrom cerveau.neuromodulation import experience_m7_bis\nt=time.time(); r=experience_m7_bis(permutations=30, synthetique=True); print('duree',round(time.time()-t,2))\nprint('zipf', json.dump … [1735 caractères tronqués]`

  ```
Traceback (most recent call last):
  File "<string>", line 18, in <module>
    print(signal, [(b, round(r['resultats'][f'lfu_contexte_{signal}_b{b:g}']['suf_surface']['moyenne'],4), round(r['resultats'][f'lfu_contexte_{signal}_b{b:g}']['suf_surface']['moyenne']-r['resultats']['lfu']['suf_surface']['moyenne'],4)) for b in (0.0,0.5,1.0,2.0,4.0)])
                             ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KeyError: 'lfu_contexte_jeu_b1'
duree 15.18
zipf {"lfu_bat_fifo_suffixe_code": true, "lfu_recence_bat_lfu_suffixe_code": false, "hasard_non_significatif": true}
zipf lfu delta {'suf_surface': (0.0434, 11), 'suf_code': (0.1352, 14), 'rep_surface': (0.0634, 15)}
oracle {'suf_surface': 0.2428, 'suf_code': 0.9849}
--- contextes (surface, vs lfu) ---
contexte_jeu suf_s 0.0075 d -0.0852 0 p 0.0 | suf_c 0.3708 d -0.3761 1
contexte_longueur suf_s 0.0192 d -0.0736 0 p 0.0 | suf_c 0.7013 d -0.0456 12
contexte_type suf_s 0.0075 d -0.0852 0 p 0.0 | suf_c 0.3585 d -0.3884 0
lfu_contexte_jeu suf_s 0.0739 d -0.0189 0 p 0.0 | suf_c 0.5899 d -0.1569 3
lfu_contexte_longueur suf_s 0.0921 d -0.0006 14 p 0.5413 | suf_c 0.7522 d 0.0053 13
lfu_contexte_type suf_s 0.0733 d -0.0195 0 p 0.0 
… [784 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 -c \"\nimport time, json\nfrom cerveau.neuromodulation import experience_m7_bis\nr=experience_m7_bis(permutations=30, synthetique=True)\nprint('--- LFU+recence vs LFU ---')\nfor nom in ('lfu_recence','lfu_recence_c … [1548 caractères tronqués]`

  ```
--- LFU+recence vs LFU ---
lfu_recence suf_surface mean 0.0 gains 0 p 1.0 ic [0.0, 0.0]
lfu_recence suf_code mean 0.0 gains 0 p 1.0 ic [0.0, 0.0]
lfu_recence rep_surface mean 0.0 gains 0 p 1.0 ic [0.0, 0.0]
lfu_recence rep_code mean 0.0 gains 0 p 1.0 ic [0.0, 0.0]
lfu_recence ret_nouveaux_utiles mean 0.0 gains 0 p 1.0 ic [0.0, 0.0]
lfu_recence ret_code mean 0.0 gains 0 p 1.0 ic [0.0, 0.0]
lfu_recence_code suf_surface mean 0.0 gains 0 p 1.0 ic [0.0, 0.0]
lfu_recence_code suf_code mean -0.00063 gains 0 p 0.5 ic [-0.00149, 0.00023]
lfu_recence_code rep_surface mean 0.0 gains 0 p 1.0 ic [0.0, 0.0]
lfu_recence_code rep_code mean -0.00017 gains 1 p 1.0 ic [-0.00058, 0.00024]
lfu_recence_code ret_nouveaux_utiles mean 0.0 gains 1 p 1.0 ic [-0.00294, 0.00294]
lfu_recence_code ret_code mean 0.0 gains 0 p 1.0 ic [0.0, 0.0]
--- beta sweep (suffix surface, delta vs lfu) ---
jeu [(0.0, 0.0928, 0.0, 0, 1.0), (0.5, 0.0739, -0.0189, 0, 0.0), (1.0, 0.0739, -0.0189, 0, 0.0), (2.0, 0.0704, -0.0223, 0, 0.0), (4.0, 0.0403, -0.0525, 0, 0.0)]
longueur [(0.0, 0.0928, 0.0, 0, 1.0), (0.5, 0.0921, -0.0006, 14, 0.541), (1.0, 0.0921, -0.0006, 14, 0.541), (2.0, 0.0742, -0.0186, 9, 0.307), (4.0, 0.0406, -0.0522, 
… [1084 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Résultat net obtenu : LFU+récence = LFU, contextes perdants ; ajout des tests

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", "old_string": "import collections\nimport dataclasses\nimport math\nimport random\nimport statistics", "new_string": "import collections\nimport dataclasses\nimport datetime\nimport math\nimport random\nimport statistics … [2 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", "old_string": "        \"meta\": {\"module\": \"M7-bis\", \"classe\": \"MemoireFrequence\",\n                 \"date\": __import__(\"datetime\").datetime.now().isoformat(\n                     timespec=\"seconds\")},", " … [222 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_neuromodulation.py", "new_string": "from cerveau.neuromodulation import (EpisodeM7, MemoireFrequence,\n                                     MemoireLimitee, Neuromodulation,\n                                     experience_m7, expe … [640 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_neuromodulation.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_neuromodulation.py", "new_string": "    def test_experience(self):\n        ep = preparer_flux()\n        r = experience_m7(ep, permutations=5, synthetique=False)\n        plafond = r[\"protocole\"][\"plafonds\"]\n        self.ass … [4723 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_neuromodulation.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 -m unittest tools.cerveau.tests.test_neuromodulation -v 2>&1 | tail -30", "description": "Run neuromodulation tests"}`

  ```
test_beta_zero_egal_lfu_recence (tools.cerveau.tests.test_neuromodulation.TestMemoireFrequence.test_beta_zero_egal_lfu_recence) ... ok
test_contexte_alloue_au_contexte_frequent (tools.cerveau.tests.test_neuromodulation.TestMemoireFrequence.test_contexte_alloue_au_contexte_frequent) ... ok
test_contexte_requis (tools.cerveau.tests.test_neuromodulation.TestMemoireFrequence.test_contexte_requis) ... ok
test_experience_m7_bis (tools.cerveau.tests.test_neuromodulation.TestMemoireFrequence.test_experience_m7_bis) ... FAIL
test_lfu_evince_le_moins_frequent (tools.cerveau.tests.test_neuromodulation.TestMemoireFrequence.test_lfu_evince_le_moins_frequent) ... ok
test_lfu_recence_departage (tools.cerveau.tests.test_neuromodulation.TestMemoireFrequence.test_lfu_recence_departage) ... ok
test_capacite_zero (tools.cerveau.tests.test_neuromodulation.TestNeuromodulation.test_capacite_zero) ... ok
test_cle_code_dedouble (tools.cerveau.tests.test_neuromodulation.TestNeuromodulation.test_cle_code_dedouble) ... ok
test_experience (tools.cerveau.tests.test_neuromodulation.TestNeuromodulation.test_experience) ... ok
test_fifo_evince_le_plus_ancien (tools.cerveau.tests.test_neuromodulation.TestNeuromodul
… [1350 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_neuromodulation.py", "new_string": "        self.assertIn(\"contexte_jeu\", r[\"verdict\"][\"contexte_bat_lfu\"])\n        self.assertIn(\"suf_surface\",\n                      r[\"verdict\"][\"lfu_recence_bat_lfu\"][\"surface\"]) … [191 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_neuromodulation.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 900 python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -5", "description": "Run full cerveau test suite"}`

  ```
...........................................................sssssssssss...........................ssssssss
----------------------------------------------------------------------
Ran 105 tests in 8.269s

OK (skipped=19)
  ```

### 🤖 Assistant

⏵ Génération du JSON M7-bis puis rédaction de la fiche mesurée

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 - <<'PY'\nimport json, time\nfrom cerveau.neuromodulation import experience_m7_bis\nt = time.time()\nr = experience_m7_bis(permutations=30, synthetique=True)\nr[\"meta\"][\"duree_s\"] = round(time.time() - t, 2)\nr … [855 caractères tronqués]`

  ```
ecrit /tmp/a11-m7-lfu.json 183945 octets
duree 14.47 s
verdict recence surface {'suf_surface': (0.0, 0, 1.0), 'rep_surface': (0.0, 0, 1.0), 'ret_nouveaux_utiles': (0.0, 0, 1.0)}
verdict recence code {'suf_code': (-0.00063, 0, 0.5), 'rep_code': (-0.00017, 1, 1.0), 'ret_code': (0.0, 0, 1.0)}
zipf {'lfu_bat_fifo_suffixe_code': True, 'lfu_recence_bat_lfu_suffixe_code': False, 'hasard_non_significatif': True}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 - <<'PY'\nimport json\nfrom datetime import datetime\n\nr = json.load(open(\"/tmp/a11-m7-lfu.json\", encoding=\"utf-8\"))\nP = r[\"protocole\"]\nV = r[\"verdict\"]\nres = r[\"resultats\"]\ndl = r[\"deltas_vs_lfu\"]\ndf = r[\"d … [17668 caractères tronqués]`

  ```
ecrit /tmp/a11-m7-lfu.md 13587 octets
142 /tmp/a11-m7-lfu.md
# A11 — M7-bis : `MemoireFrequence` (LFU, LFU + récence, contextes)

> Sous-agent A11, sprint autonome 24 h, CPU uniquement. Date : 2026-10-27T16:33:30+00:00.
> JSON complet : `/tmp/a11-m7-lfu.json`. Code : `tools/cerveau/neuromodulation.py` ;
> tests : `tools/cerveau/tests/test_neuromodulation.py`. Aucun autre fichier modifié.
> Durée de la mesure : 14.47 s (33 configurations × 30 permutations).

## 0. Résumé

| question | mesure (30 permutations appariées) | verdict |
|---|---|---|
| **LFU contre FIFO/LRU** | suffixe surface **+4.25 pts** (27/30) ; répétés surface **+23.13 pts** (30/30) ; nouveaux utiles **+8.73 pts** (30/30) | le LFU gagne, mais reste à **9.28 %** contre un oracle de **24.28 %** |
| **LFU + récence contre LFU** | surface : **0.00 pt** (0/30, p=1) ; code : **−0.06 pt** de suffixe code (0/30, p=0.5) | **ne bat pas le LFU** — sur surface, les deux politiques sont identiques |
| **contexte (jeu, longueur, type) contre LFU** | meilleur cas : longueur **−0.06 pt** (14/30, p=0.54, IC à 95 % incluant 0) ; jeu **−1.89 pt** (0/30) ; type **−1.95 pt** (0/30) | **aucun contexte ne bat le LFU** |
| **contrôle clé p
… [2334 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Ajout de la métrique « nouveaux du suffixe » et du diagnostic d'évictions

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"evictions\\|_METRIQUES_BIS\\|ret_nouveaux_utiles\\|def _tourner_frequence\\|def _evincer\" tools/cerveau/neuromodulation.py | tail -25", "description": "Locate lines for metrics and eviction edits"}`

  ```
220:    def _evincer(self) -> None:
672:    def _evincer(self) -> None:
716:_METRIQUES_BIS = ("ret_surface_prefixe", "ret_surface_finale",
717:                  "ret_nouveaux_utiles", "ret_code", "rep_surface",
761:def _tourner_frequence(episodes: list[EpisodeM7], ordre: list[int],
798:        "ret_nouveaux_utiles": len(surfaces_memoire & utiles)
914:            for met in _METRIQUES_BIS:
930:                               for m in _METRIQUES_BIS}
934:                                for m in _METRIQUES_BIS}
942:                   default=0.0) for m in _METRIQUES_BIS}
954:                              "rep_code", "ret_nouveaux_utiles")},
958:                              "rep_code", "ret_nouveaux_utiles")},
962:                              "rep_code", "ret_nouveaux_utiles")},
978:                                  "ret_nouveaux_utiles")},
985:                                  "ret_nouveaux_utiles")},
992:                            "rep_code", "ret_nouveaux_utiles")}
997:                            "rep_code", "ret_nouveaux_utiles")}
1005:                for m in _METRIQUES_BIS)
1019:                "ret_nouveaux_utiles": "surfaces vues au préfixe qui reviennent dans le flux et sont
… [328 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '635,700p' tools/cerveau/neuromodulation.py && echo '---' && sed -n '710,735p' tools/cerveau/neuromodulation.py && echo '---' && sed -n '780,815p' tools/cerveau/neuromodulation.py", "description": "Read class init, eviction, and runner snippets … [2 caractères tronqués]`

  ```
def contient_code(self, code: dict) -> bool:
        return any(e["code"] == code for e in self._slots.values())

    def codes(self) -> list[dict]:
        return [dict(e["code"]) for e in self._slots.values()]

    def etat(self) -> list[dict]:
        return [{"surface": e["surface"], "code": dict(e["code"]),
                 "frequence": int(e["freq"]), "contexte": e["ctx"],
                 "t_arrivee": e["t_arrivee"], "t_dernier": e["t_dernier"]}
                for e in sorted(self._slots.values(),
                                key=lambda e: e["t_arrivee"])]

    # ---- score et éviction ----------------------------------------------
    def _cle(self, surface: str, code: dict) -> tuple:
        if self.cle == "code":
            return tuple(sorted(code.items()))
        return ("surface", surface)

    def _score(self, e: dict) -> float:
        if self.politique in ("lfu", "lfu_recence"):
            return float(e["freq"])
        if self.politique == "contexte":
            return float(self._ctx.get(e["ctx"], 0))
        if self.politique == "lfu_contexte":
            part = self._ctx.get(e["ctx"], 0) / max(1, self._n)
            return math.log1p(e["freq"]) + self
… [3957 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '598,625p' tools/cerveau/neuromodulation.py", "description": "Read MemoireFrequence init"}`

  ```
où ``part_du_contexte`` est la part des écritures du contexte dans le
      flux vu. ``beta=0`` redonne exactement ``lfu_recence`` (contrôle de
      cohérence) ;
    - ``hasard`` : priorité aléatoire fixée à la première écriture (contrôle
      négatif).

    Le contexte n'est utilisé que pour les politiques contextuelles ; il doit
    alors être fourni à chaque écriture. Aucune information du suffixe n'entre
    dans le score : le contexte est compté en ligne, au fil des écritures.
    """

    nom = "M7bis-memoire-frequence"

    def __init__(self, capacite: int = 64, politique: str = "lfu",
                 cle: str = "surface", graine: int = 0,
                 beta: float = 1.0) -> None:
        if politique not in POLITIQUES_FREQUENCE:
            raise ValueError(f"politique inconnue : {politique}")
        if cle not in CLEFS:
            raise ValueError(f"clé inconnue : {cle}")
        self.capacite = max(0, int(capacite))
        self.politique = politique
        self.cle = cle
        self.beta = float(beta)
        self._slots: dict[tuple, dict] = {}
        self._ctx: collections.Counter = collections.Counter()
        self._t = 0
        self._n = 0
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '900,930p' tools/cerveau/neuromodulation.py && echo '---controles---' && sed -n '1025,1055p' tools/cerveau/neuromodulation.py", "description": "Read experiment loop and controls section"}`

  ```
c["nom"]: collections.defaultdict(list) for c in configs}
    oracle = collections.defaultdict(list)
    for k in range(permutations):
        ordre = list(range(n))
        random.Random(graine + k).shuffle(ordre)
        permutes = _contextes_permutes(contextes, ordre, prefixe,
                                       graine + k)
        for c in configs:
            ctx = None
            if c["signal"]:
                source = permutes if c["permute"] else contextes
                ctx = source[c["signal"]]
            m = _tourner_frequence(ep, ordre, prefixe, c, capacite, ctx,
                                   graine + k)
            for met in _METRIQUES_BIS:
                resultats[c["nom"]][met].append(m[met])
        o = _oracle_frequence(ep, ordre, prefixe, capacite)
        oracle["suf_surface"].append(o["suf_surface"])
        oracle["suf_code"].append(o["suf_code"])
    moyennes = {nom: {m: _stats(v) for m, v in vals.items()}
                for nom, vals in resultats.items()}
    ref_lfu = {"surface": "lfu", "code": "lfu_code"}
    ref_fifo = {"surface": "fifo", "code": "fifo_code"}
    deltas_lfu = {}
    deltas_fifo = {}
    for c in configs:
        nom = c["nom
… [1900 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", "new_string": "        self._t = 0\n        self._n = 0\n        self.evictions = 0\n        self.evictions_sans_freq1 = 0", "old_string": "        self._t = 0\n        self._n = 0"}`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", "new_string": "    def _evincer(self) -> None:\n        if not self._slots:\n            return\n        self.evictions += 1\n        if min(e[\"freq\"] for e in self._slots.values()) >= 2:\n            self.evictions_sa … [193 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", "new_string": "_METRIQUES_BIS = (\"ret_surface_prefixe\", \"ret_surface_finale\",\n                  \"ret_nouveaux_utiles\", \"ret_nouveaux_suffixe\",\n                  \"ret_code\", \"rep_surface\", \"rep_code\", \"su … [308 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", "new_string": "    total_surfaces = collections.Counter(e.surface for e in episodes)\n    utiles = {s for s in surfaces_vues if total_surfaces[s] >= 2}\n    suffixe = ordre[prefixe:]\n    prefix_counts = collections.Coun … [2516 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", "new_string": "    oracle = collections.defaultdict(list)\n    diagnostics = collections.defaultdict(collections.Counter)\n    for k in range(permutations):\n        ordre = list(range(n))\n        random.Random(graine + … [1576 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '1035,1075p' tools/cerveau/neuromodulation.py", "description": "Read controls and protocol descriptions"}`

  ```
"capacite": capacite, "permutations": permutations,
            "graine": graine,
            "metriques": {
                "ret_surface_prefixe": "surfaces retenues / surfaces distinctes vues au préfixe (plafonnée par la capacité)",
                "ret_surface_finale": "surfaces retenues / surfaces distinctes du flux (plafond = capacité/vocabulaire)",
                "ret_nouveaux_utiles": "surfaces vues au préfixe qui reviennent dans le flux et sont retenues / ces surfaces",
                "ret_code": "codes retenus / codes distincts vus au préfixe",
                "rep_surface": "écritures répétées dont la surface était déjà en mémoire",
                "rep_code": "écritures répétées dont le code était déjà en mémoire",
                "suf_surface": "requêtes du suffixe dont la surface est en mémoire (mémoire gelée)",
                "suf_code": "requêtes du suffixe dont le code est en mémoire (mémoire gelée)",
            },
            "plafond_surface_finale": plafond,
        },
        "configurations": configs,
        "resultats": moyennes,
        "deltas_vs_lfu": deltas_lfu,
        "deltas_vs_fifo": deltas_fifo,
        "oracle_suffixe": {m: _stats(v) for m, v in
… [1364 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", "new_string": "                \"ret_nouveaux_utiles\": \"surfaces vues au préfixe qui reviennent dans le flux et sont retenues / ces surfaces\",\n                \"ret_nouveaux_suffixe\": \"surfaces vues une seule fois  … [405 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", "new_string": "        \"controles\": {\n            \"contexte_reel_vs_permute\": contexte_controle,\n            \"beta_zero_ecart_max\": ecart_beta_zero,\n            \"evictions\": {\n                nom: {\"eviction … [1982 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && sed -n '990,1040p' tools/cerveau/neuromodulation.py", "description": "Read verdict section"}`

  ```
def _bat(d: dict) -> bool:
        return d["moyenne"] > 0 and d["ic95"][0] > 0

    rec = "lfu_recence"
    rec_code = "lfu_recence_code"
    verdict = {
        "lfu_recence_bat_lfu": {
            "surface": {m: _resume_delta(deltas_lfu[rec][m])
                        for m in ("suf_surface", "rep_surface",
                                  "ret_nouveaux_utiles")},
            "code": {m: _resume_delta(deltas_lfu[rec_code][m])
                     for m in ("suf_code", "rep_code", "ret_code")},
        },
        "lfu_bat_fifo": {
            "surface": {m: _resume_delta(deltas_fifo["lfu"][m])
                        for m in ("suf_surface", "rep_surface",
                                  "ret_nouveaux_utiles")},
            "code": {m: _resume_delta(deltas_fifo["lfu_code"][m])
                     for m in ("suf_code", "rep_code", "ret_code")},
        },
        "contexte_bat_lfu": {
            nom: {m: _resume_delta(deltas_lfu[nom][m])
                  for m in ("suf_surface", "suf_code", "rep_surface",
                            "rep_code", "ret_nouveaux_utiles")}
            for nom in contexte_controle},
        "cle_permutee_egale_reelle": {
            nom: {m: _res
… [1444 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", "new_string": "            \"surface\": {m: _resume_delta(deltas_lfu[rec][m])\n                        for m in (\"suf_surface\", \"rep_surface\",\n                                  \"ret_nouveaux_utiles\",\n             … [262 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py", "new_string": "            \"surface\": {m: _resume_delta(deltas_fifo[\"lfu\"][m])\n                        for m in (\"suf_surface\", \"rep_surface\",\n                                  \"ret_nouveaux_utiles\",\n        … [272 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/neuromodulation.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 -m unittest tools.cerveau.tests.test_neuromodulation 2>&1 | tail -4", "description": "Run M7-bis tests after metric additions"}`

  ```
----------------------------------------------------------------------
Ran 12 tests in 1.699s

OK
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 -c \"\nimport time\nfrom cerveau.neuromodulation import experience_m7_bis\nt=time.time(); r=experience_m7_bis(permutations=30, synthetique=True); print('duree',round(time.time()-t,2))\nfor nom in ('fifo','lru','lfu … [616 caractères tronqués]`

  ```
duree 15.52
fifo {'ret_nouveaux_utiles': 0.101, 'ret_nouveaux_suffixe': 0.0262, 'rep_surface': 0.2874, 'suf_surface': 0.0503, 'suf_code': 0.717}
lru {'ret_nouveaux_utiles': 0.1072, 'ret_nouveaux_suffixe': 0.0262, 'rep_surface': 0.337, 'suf_surface': 0.0594, 'suf_code': 0.7189}
lfu {'ret_nouveaux_utiles': 0.1883, 'ret_nouveaux_suffixe': 0.0194, 'rep_surface': 0.5187, 'suf_surface': 0.0928, 'suf_code': 0.7469}
lfu_recence {'ret_nouveaux_utiles': 0.1883, 'ret_nouveaux_suffixe': 0.0194, 'rep_surface': 0.5187, 'suf_surface': 0.0928, 'suf_code': 0.7469}
lfu_code {'ret_nouveaux_utiles': 0.0785, 'ret_nouveaux_suffixe': 0.0348, 'rep_surface': 0.2622, 'suf_surface': 0.044, 'suf_code': 0.95}
lfu_recence_code {'ret_nouveaux_utiles': 0.0785, 'ret_nouveaux_suffixe': 0.0348, 'rep_surface': 0.2622, 'suf_surface': 0.044, 'suf_code': 0.9494}
evictions {'lfu': {'evictions': 11163, 'sans_freq1': 0, 'part_sans_freq1': 0.0}, 'lfu_recence': {'evictions': 11163, 'sans_freq1': 0, 'part_sans_freq1': 0.0}, 'lfu_code': {'evictions': 546, 'sans_freq1': 12, 'part_sans_freq1': 0.02197802197802198}, 'lfu_recence_code': {'evictions': 548, 'sans_freq1': 11, 'part_sans_freq1': 0.020072992700729927}}
recence surface 
… [281 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools python3 -c \"\nimport random, collections\nfrom cerveau.neuromodulation import preparer_flux, MemoireFrequence\nep=preparer_flux(); n=len(ep); prefixe=int(n*0.8)\nfor k in range(3):\n    ordre=list(range(n)); random.Random(k).shuffle( … [713 caractères tronqués]`

  ```
perm 0 nouveaux_suffixe 10 prefix distinct 357 suffix distinct 98
  fifo retenus nouveaux 1 / 10
  lfu retenus nouveaux 1 / 10
  lfu_code retenus nouveaux 0 / 10
perm 1 nouveaux_suffixe 10 prefix distinct 358 suffix distinct 98
  fifo retenus nouveaux 0 / 10
  lfu retenus nouveaux 0 / 10
  lfu_code retenus nouveaux 1 / 10
perm 2 nouveaux_suffixe 4 prefix distinct 354 suffix distinct 96
  fifo retenus nouveaux 0 / 4
  lfu retenus nouveaux 0 / 4
  lfu_code retenus nouveaux 0 / 4
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 600 python3 - <<'PY'\nimport json, time\nfrom cerveau.neuromodulation import experience_m7_bis\nt = time.time()\nr = experience_m7_bis(permutations=30, synthetique=True)\nr[\"meta\"][\"duree_s\"] = round(time.time() - t, 2)\nr … [838 caractères tronqués]`

  ```
ok 15.14 s 201837 octets
evictions {'lfu': {'evictions': 11163, 'sans_freq1': 0, 'part_sans_freq1': 0.0}, 'lfu_recence': {'evictions': 11163, 'sans_freq1': 0, 'part_sans_freq1': 0.0}, 'lfu_code': {'evictions': 546, 'sans_freq1': 12, 'part_sans_freq1': 0.02197802197802198}, 'lfu_recence_code': {'evictions': 548, 'sans_freq1': 11, 'part_sans_freq1': 0.020072992700729927}}
nouveaux suffixe lfu/fifo 0.019419191919191916 0.026153198653198654
delta lfu vs fifo nouveaux suffixe {'ret_nouveaux_utiles': (0.0873404706457363, 29, 3.725290298461914e-09, [0.07386935611188951, 0.1008115851795831]), 'ret_nouveaux_suffixe': (-0.006734006734006734, 0, 0.5, [-0.015953537940869553, 0.0024855244728560844])}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nr = json.load(open(\"/tmp/a11-m7-lfu.json\", encoding=\"utf-8\"))\nP, V, res, dl, df = r[\"protocole\"], r[\"verdict\"], r[\"resultats\"], r[\"deltas_vs_lfu\"], r[\"deltas_vs_fifo\"]\ncc = r[\"controles\"][\"contexte_ree … [19933 caractères tronqués]`

  ```
ecrit 15457 octets
150 /tmp/a11-m7-lfu.md
# A11 — M7-bis : `MemoireFrequence` (LFU, LFU + récence, contextes)

> Sous-agent A11, sprint autonome 24 h, CPU uniquement. Date : 2026-10-27T16:40:32+00:00.
> JSON complet : `/tmp/a11-m7-lfu.json`. Code : `tools/cerveau/neuromodulation.py` ;
> tests : `tools/cerveau/tests/test_neuromodulation.py`. A11 n'a modifié que ces deux fichiers.
> Durée de la mesure : 15.14 s (33 configurations × 30 permutations).

## 0. Résumé

| question | mesure (30 permutations appariées) | verdict |
|---|---|---|
| **LFU contre FIFO/LRU** | suffixe surface **+4.25 pts** (27/30) ; répétés surface **+23.13 pts** (30/30) ; nouveaux utiles **+8.73 pts** (29/30) ; nouveaux du suffixe **−0.67 pt** (0/30, p=0.5, non significatif) | le LFU gagne sur les répétés et le suffixe, mais **sacrifie les one-shot** ; reste à **9.28 %** contre un oracle de **24.28 %** |
| **LFU + récence contre LFU** | surface : **0.00 pt** (0/30, p=1) ; code : **−0.06 pt** de suffixe code (0/30, p=0.5) | **ne bat pas le LFU** — sur surface, les deux politiques sont identiques |
| **contexte (jeu, longueur, type) contre LFU** | meilleur cas : longueur **−0.06 pt** (14/30, p=0.54, IC incluant 0)
… [2889 caractères tronqués]
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

- **bash** `{"command": "sed -n '40,115p' /tmp/a11-m7-lfu.md", "description": "Review MD middle sections"}`

  ```
| **lfu** | 18.83 | 1.94 | 51.87 | 9.28 | 74.69 |
| **lfu + récence** | 18.83 | 1.94 | 51.87 | 9.28 | 74.69 |
| hasard | 10.07 | 3.72 | 32.25 | 5.75 | 70.13 |
| contexte jeu (pur) | 3.58 | 1.23 | 9.01 | 0.75 | 37.08 |
| contexte longueur (pur) | 10.40 | 4.55 | 13.04 | 1.92 | 70.13 |
| contexte type (pur) | 3.68 | 1.23 | 8.72 | 0.75 | 35.85 |
| LFU + contexte jeu | 12.37 | 0.67 | 41.53 | 7.39 | 58.99 |
| LFU + contexte longueur | 21.17 | 2.85 | 44.36 | 9.21 | 75.22 |
| LFU + contexte type | 12.26 | 0.37 | 39.61 | 7.33 | 58.08 |

Deltas appariés **contre le LFU** (même clé, même ordre) :

| politique | Δ nouv. utiles | Δ nouv. suffixe | Δ répétés surface | Δ suffixe surface |
|---|---:|---:|---:|---:|
| lru | -8.12 (0/30, p=<0.001) | +0.67 (2/30, p=0.500) | -18.17 (0/30, p=<0.001) | -3.33 (1/30, p=<0.001) |
| lfu + récence | +0.00 (0/30, p=1.000) | +0.00 (0/30, p=1.000) | +0.00 (0/30, p=1.000) | +0.00 (0/30, p=1.000) |
| contexte jeu (pur) | -15.25 (0/30, p=<0.001) | -0.71 (2/30, p=0.688) | -42.86 (0/30, p=<0.001) | -8.52 (0/30, p=<0.001) |
| contexte longueur (pur) | -8.43 (2/30, p=<0.001) | +2.60 (7/30, p=0.180) | -38.83 (0/30, p=<0.001) | -7.36 (0/30, p=<0.001) |
| contexte type (
… [5683 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"9 métriques\\|sacrifie\\|p=<\" /tmp/a11-m7-lfu.md", "description": "Find MD wording to fix"}`

  ```
12:| **LFU contre FIFO/LRU** | suffixe surface **+4.25 pts** (27/30) ; répétés surface **+23.13 pts** (30/30) ; nouveaux utiles **+8.73 pts** (29/30) ; nouveaux du suffixe **−0.67 pt** (0/30, p=0.5, non significatif) | le LFU gagne sur les répétés et le suffixe, mais **sacrifie les one-shot** ; reste à **9.28 %** contre un oracle de **24.28 %** |
54:| lru | -8.12 (0/30, p=<0.001) | +0.67 (2/30, p=0.500) | -18.17 (0/30, p=<0.001) | -3.33 (1/30, p=<0.001) |
56:| contexte jeu (pur) | -15.25 (0/30, p=<0.001) | -0.71 (2/30, p=0.688) | -42.86 (0/30, p=<0.001) | -8.52 (0/30, p=<0.001) |
57:| contexte longueur (pur) | -8.43 (2/30, p=<0.001) | +2.60 (7/30, p=0.180) | -38.83 (0/30, p=<0.001) | -7.36 (0/30, p=<0.001) |
58:| contexte type (pur) | -15.15 (0/30, p=<0.001) | -0.71 (2/30, p=0.688) | -43.15 (0/30, p=<0.001) | -8.52 (0/30, p=<0.001) |
59:| LFU + contexte jeu | -6.46 (3/30, p=<0.001) | -1.27 (1/30, p=0.375) | -10.34 (3/30, p=<0.001) | -1.89 (0/30, p=<0.001) |
61:| LFU + contexte type | -6.57 (2/30, p=<0.001) | -1.57 (1/30, p=0.219) | -12.26 (2/30, p=<0.001) | -1.95 (0/30, p=<0.001) |
83:Sur la clé surface, `lfu` et `lfu_recence` sont **identiques sur les 9 métriques et les 30 permuta
… [462 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np = \"/tmp/a11-m7-lfu.md\"\ns = open(p, encoding=\"utf-8\").read()\ns = s.replace(\"p=<0.001\", \"p<0.001\")\ns = s.replace(\"identiques sur les 9 métriques\", \"identiques sur les 10 métriques\")\ns = s.replace(\"mais **sacrifie les one-shot** ;\", \"mais * … [927 caractères tronqués]`

  ```
ok
101:- Seul effet nominal positif parmi les contextes combinés : `longueur` sur `ret_nouveaux_utiles` (**+2.34 pts**, 16/30, p=0.027), qui ne se transpose pas au suffixe (−0.06 pt, p=0.54). Avec 18 comparaisons de contexte et sans correction, ce n'est pas un résultat robuste.
  ```

- **edit** `{"file_path": "/home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_neuromodulation.py", "new_string": "        self.assertIn(\"contexte_jeu\", r[\"verdict\"][\"contexte_bat_lfu\"])\n        self.assertIn(\"suf_surface\",\n                      r[\"verdict\"][\"lfu_recence_bat_lfu\"][\"surface\"]) … [346 caractères tronqués]`

  ```
The file /home/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_neuromodulation.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && PYTHONPATH=tools timeout 900 python3 -m unittest discover -s tools/cerveau/tests -t tools 2>&1 | tail -4", "description": "Final full test suite"}`

  ```
----------------------------------------------------------------------
Ran 123 tests in 11.289s

OK (skipped=19)
  ```

- **bash** `{"command": "grep -n \"105\\|123\\|tests OK\" /tmp/a11-m7-lfu.md", "description": "Find test count in MD"}`

  ```
127:| **suite de tests** | `PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools` : **105 tests OK, 19 skip** (état du workspace au moment de la mesure) | OK ; les 12 tests M7-bis passent |
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np = \"/tmp/a11-m7-lfu.md\"\ns = open(p, encoding=\"utf-8\").read()\ns = s.replace(\"**105 tests OK, 19 skip** (état du workspace au moment de la mesure)\",\n              \"**123 tests OK, 19 skip** (dernier contrôle ; le workspace bouge en parallèle)\")\nop … [136 caractères tronqués]`

  ```
127:| **suite de tests** | `PYTHONPATH=tools python3 -m unittest discover -s tools/cerveau/tests -t tools` : **123 tests OK, 19 skip** (dernier contrôle ; le workspace bouge en parallèle) | OK ; les 12 tests M7-bis passent |
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\np = \"/tmp/a11-m7-lfu.md\"\ns = open(p, encoding=\"utf-8\").read()\ns = s.replace(\"| **LFU contre FIFO/LRU** |\", \"| **LFU contre FIFO** (LRU au §2) |\")\ns = s.replace(\"| **aucun contexte ne bat le LFU** |\", \"| **aucun contexte ne bat le LFU sur le suf … [351 caractères tronqués]`

  ```
ok
## 0. Résumé

| question | mesure (30 permutations appariées) | verdict |
|---|---|---|
| **LFU contre FIFO** (LRU au §2) | suffixe surface **+4.25 pts** (27/30) ; répétés surface **+23.13 pts** (30/30) ; nouveaux utiles **+8.73 pts** (29/30) ; nouveaux du suffixe **−0.67 pt** (0/30, p=0.5, non significatif) | le LFU gagne sur les répétés et le suffixe, mais **sous-sert les one-shot** (direction, non significatif) ; reste à **9.28 %** contre un oracle de **24.28 %** |
| **LFU + récence contre LFU** | surface : **0.00 pt** (0/30, p=1) ; code : **−0.06 pt** de suffixe code (0/30, p=0.5) | **ne bat pas le LFU** — sur surface, les deux politiques sont identiques |
| **contexte (jeu, longueur, type) contre LFU** | meilleur cas : longueur **−0.06 pt** (14/30, p=0.54, IC incluant 0) ; jeu **−1.89 pt** (0/30) ; type **−1.95 pt** (0/30) | **aucun contexte ne bat le LFU sur le suffixe** |
| **contrôle clé permutée** | réel − permuté : jeu **−2.26 pts** (2/30), longueur **−0.06 pt** (13/30), type **−1.95 pt** (1/30) | le contexte réel n'ajoute pas d'information ; pour `jeu`/`type`, associé, il **nuit** |
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nr = json.load(open('/tmp/a11-m7-lfu.json', encoding='utf-8'))\nassert r['protocole']['n'] == 528 and r['protocole']['capacite'] == 16\nassert len(r['configurations']) == 33\nassert len(r['deltas_vs_lfu']) == 32  # toutes … [1143 caractères tronqués]`

  ```
--- fichiers ---
-rw-r--r--. 1 stephane stephane 257584 27 oct 12:40 /tmp/a11-m7-lfu.json
-rw-r--r--. 1 stephane stephane  16223 27 oct 12:45 /tmp/a11-m7-lfu.md
--- git status (lecture seule) ---
M  docs/glossaire/README.md
 M journal/2026-10-27.md
 M journal/2026-10-27_mesures.md
 M journal/2026-10-27_portes.md
 M journal/THEMES.md
 M tools/cerveau/tests/test_neuromodulation.py
M  tools/glossaire_cartes.py
--- diff stat de nos deux fichiers ---
 tools/cerveau/tests/test_neuromodulation.py | 2 ++
 1 file changed, 2 insertions(+)
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
AssertionError
  ```

### 🤖 Assistant

⏵ Vérification que le code M7-bis est intact après les écritures concurrentes

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && grep -n \"class MemoireFrequence\\|def experience_m7_bis\\|ret_nouveaux_suffixe\\|evictions_sans_freq1\" tools/cerveau/neuromodulation.py | head -12; echo '---'; grep -n \"class TestMemoireFrequence\\|ret_nouveaux_suffixe\" tools/cerveau/tests/test_ne … [115 caractères tronqués]`

  ```
573:class MemoireFrequence:
627:        self.evictions_sans_freq1 = 0
679:            self.evictions_sans_freq1 += 1
722:                  "ret_nouveaux_utiles", "ret_nouveaux_suffixe",
811:        "ret_nouveaux_suffixe": len(surfaces_memoire & nouveaux_suffixe)
821:        "evictions_sans_freq1": memoire.evictions_sans_freq1,
893:def experience_m7_bis(episodes: list[EpisodeM7] | None = None,
936:                    "evictions_sans_freq1"]
1000:                                  "ret_nouveaux_suffixe")},
1008:                                  "ret_nouveaux_suffixe")},
1043:                "ret_nouveaux_suffixe": "surfaces vues une seule fois au préfixe et présentes dans le suffixe, retenues / ces surfaces (oracle d'évaluation)",
1072:            "Le plafond de rétention des nouveaux (capacité/vocabulaire) n'est pas un résultat ; ret_nouveaux_utiles et ret_nouveaux_suffixe sont les métriques discriminantes ajoutées.",
---
83:class TestMemoireFrequence(unittest.TestCase):
140:        self.assertIn("ret_nouveaux_suffixe", r["resultats"]["lfu"])
--- log ---
c122f430 B14 — CORRECTION M5 : LE 28,03 % EST UNE COUVERTURE DE 51,4 %, PAS UN GAIN ; M5 HONNÊTE 12,60 %
86259771 B14/B15/B16 — FIN
… [294 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nr = json.load(open('/tmp/a11-m7-lfu.json', encoding='utf-8'))\nprint('configs', len(r['configurations']), 'deltas', len(r['deltas_vs_lfu']))\nprint('lfu refs', 'lfu' in r['deltas_vs_lfu'], 'lfu_code' in r['deltas_vs_lfu' … [570 caractères tronqués]`

  ```
configs 33 deltas 31
lfu refs False False
recence {'suf_surface': (0.0, 0, False), 'rep_surface': (0.0, 0, False), 'ret_nouveaux_utiles': (0.0, 0, False), 'ret_nouveaux_suffixe': (0.0, 0, False)}
lfu vs fifo {'suf_surface': (0.0425, 27, True), 'rep_surface': (0.2313, 30, True), 'ret_nouveaux_utiles': (0.0873, 29, True), 'ret_nouveaux_suffixe': (-0.0067, 0, False)}
contextes bat_zero suf_surface {'contexte_jeu': False, 'lfu_contexte_jeu': False, 'contexte_longueur': False, 'lfu_contexte_longueur': False, 'contexte_type': False, 'lfu_contexte_type': False}
evictions {'lfu': {'evictions': 11163, 'sans_freq1': 0, 'part_sans_freq1': 0.0}, 'lfu_recence': {'evictions': 11163, 'sans_freq1': 0, 'part_sans_freq1': 0.0}, 'lfu_code': {'evictions': 546, 'sans_freq1': 12, 'part_sans_freq1': 0.02197802197802198}, 'lfu_recence_code': {'evictions': 548, 'sans_freq1': 11, 'part_sans_freq1': 0.020072992700729927}}
zipf {'lfu_bat_fifo_suffixe_code': True, 'lfu_recence_bat_lfu_suffixe_code': False, 'hasard_non_significatif': True}
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && git diff -- tools/cerveau/tests/test_neuromodulation.py | tail -20; echo '---'; git show --stat --oneline 59ad77f3 | head -15", "description": "Inspect uncommitted test diff and M7-bis commit"}`

  ```
diff --git a/tools/cerveau/tests/test_neuromodulation.py b/tools/cerveau/tests/test_neuromodulation.py
index 364827aa..cecef567 100644
--- a/tools/cerveau/tests/test_neuromodulation.py
+++ b/tools/cerveau/tests/test_neuromodulation.py
@@ -137,6 +137,8 @@ class TestMemoireFrequence(unittest.TestCase):
         self.assertIn("contexte_jeu", r["verdict"]["contexte_bat_lfu"])
         self.assertIn("suf_surface",
                       r["verdict"]["lfu_recence_bat_lfu"]["surface"])
+        self.assertIn("ret_nouveaux_suffixe", r["resultats"]["lfu"])
+        self.assertIn("evictions", r["controles"])
         # reproductibilité à graine égale
         r2 = experience_m7_bis(ep, permutations=3, synthetique=False)
         self.assertEqual(r["resultats"], r2["resultats"])
---
59ad77f3 B16 — M7-BIS LFU : +23,1 PTS RÉPÉTÉS, +4,25 SUFFIXE, LFU+RÉCENCE = LFU ; FRÉQUENCE, PAS NEUROMODULATION
 docs/carte.md                               |     1 +
 docs/roadmap.md                             |     1 +
 journal/2026-10-27.md                       |    10 +-
 journal/2026-10-27_distribue.md             |     3 +-
 journal/2026-10-27_docs.md                  |     5 +-
 journal/2026-10-27_sprint
… [385 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/GitHub/Qtrinet && for f in reports/m7-frequence.json reports/rapport-m7-frequence.md; do echo \"== $f\"; test -f \"$f\" && grep -c \"ret_nouveaux_suffixe\\|evictions_sans_freq1\" \"$f\" || echo absent; done; echo '---'; grep -n \"ret_nouveaux_suffixe\\|evictions\" repo … [118 caractères tronqués]`

  ```
== reports/m7-frequence.json
0
absent
== reports/rapport-m7-frequence.md
0
absent
---
  ```

- **send_message** `{"agent_id": "f0969e87-af0c-43b1-93cf-f278d9c90846", "message": "A11 — M7-bis terminé, mesuré, écrit. Résumé autoportant :\n\n**Livrables**\n- `/tmp/a11-m7-lfu.json` (33 configurations × 30 permutations, 15,1 s CPU)\n- `/tmp/a11-m7-lfu.md` (fiche complète, verdicts, limites)\n- Code : `tools/cerveau … [2795 caractères tronqués]`

  ```
message delivered to agent f0969e87-af0c-43b1-93cf-f278d9c90846
  ```

### 🤖 Assistant

⏵ M7-bis terminé : résultats et artefacts livrés

**M7-bis `MemoireFrequence` — verdict**

- **LFU vs FIFO** : +4,25 pts de suffixe surface (27/30), +23,13 pts de répétés surface (30/30), +8,73 pts de nouveaux utiles (29/30) ; mais −0,67 pt sur les nouveaux du suffixe (0/30, non significatif). LFU reste à 9,28 % de suffixe surface contre 24,28 % pour l’oracle.
- **LFU + récence ne bat pas LFU** : identique sur la clé surface (0,00 pt, 0/30) — 0 éviction sans item de fréquence 1 sur 11 163 évictions, donc le départage ne s’exerce jamais ; sur la clé code, −0,06 pt de suffixe code (0/30, p=0,5), très légèrement pire.
- **Aucun contexte ne bat LFU** : meilleur cas `LFU + longueur` −0,06 pt (14/30, p=0,54) ; `jeu` −1,89 pt (0/30) ; `type` −1,95 pt (0/30). Les contextes purs perdent 7,4 à 8,5 pts de suffixe surface.
- **Contrôle clé permutée** : le contexte réel est pire que sa permutation pour `jeu` (−2,26 pts, p<0,001) et `type` (−1,95 pt, p<0,001) ; `longueur` est à égalité. Le contexte est un prior de groupe qui dilue la fréquence d’item.
- **Contrôles** : Zipf synthétique LFU vs FIFO +13,52 pts de suffixe code (14/15) et +4,34 pts surface (11/15) ; plafond 16/439 = 3,6446 % atteint partout ; β=0 redonne exactement LFU+récence.
- **Tests** : suite cerveau **123 OK, 19 skip** au dernier contrôle ; les 12 tests du fichier M7 passent.

**Chemins**
- `/tmp/a11-m7-lfu.json` — JSON complet (33 configurations × 30 permutations)
- `/tmp/a11-m7-lfu.md` — fiche détaillée, contrôles, limites
- `tools/cerveau/neuromodulation.py` — `MemoireFrequence`, `experience_m7_bis`, `controle_zipf_frequence`
- `tools/cerveau/tests/test_neuromodulation.py` — `TestMemoireFrequence`

**Coordination** : un autre agent a commité pendant la session (`59ad77f3` puis `86259771`, `c122f430`) ; je n’ai fait aucune écriture git. Le `reports/m7-frequence.*` commité ne contient pas les deux ajouts finaux (`ret_nouveaux_suffixe`, diagnostic `evictions`) présents dans mon JSON `/tmp` ; les deux dernières assertions de test sont non commitées (2 lignes, tests verts).

