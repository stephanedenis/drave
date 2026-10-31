# Session DSH — relecture

- identifiant : `2fd56aa5-7b9b-40b0-9470-05c74b032d55`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-27 18:48:01
- agent : standard


## Tour 1

### 👤 Utilisateur

Dépôt /home/stephane/GitHub/Qtrinet, fenêtre jusqu'à 2026-10-28 08:00 HAE. Sous-agent A19 : améliorer le routeur M1→M2 (B23) par un **score de confiance**, sans modifier les modules existants.

Contexte :
- B23 `tools/cerveau/routeur_m1_m2.py` : original 100 %, casse 99,3 %, phrase 92,5 %, espaces 41,8 %, typo **56,2 %** < M2 **68,3 %** (collision de lexique).
- M1 `hub.py`, M2 `voies.py`/`m2_typo.py`, 146 items `de`.
- Tests : 132 OK.

Objectif :
1. Créer `tools/cerveau/routeur_confiance.py` : pour chaque surface, calculer un score (par ex. round-trip M1, marge de code, distance au lexique, longueur, espacement) et router M1/M2.
2. Mesurer : exactitude par mode (original, casse, espaces, typo, phrase), **oracle M1/M2** (borne haute), part M2, et si le score bat le routeur de B23 sur la typo.
3. Contrôle : score aléatoire, score constant, et **oracle**.
4. Écrire `/tmp/a19-routeur-confiance.json` et `.md` ; si aucun score ne bat B23, le dire.

Contraintes :
- Crée uniquement `tools/cerveau/routeur_confiance.py` et `tools/cerveau/tests/test_routeur_confiance.py` ; ne modifie pas les modules existants, docs, reports, journal, `batterie.py`, git.
- Pas de `git add/commit/checkout`.
- CPU/GPU. Sois autonome, timebox, autocritique. Réponds avec un résumé et les chemins.
Your parent agent id is "f0969e87-af0c-43b1-93cf-f278d9c90846". Before you finish, send your result to that agent with send_message({ agent_id: "f0969e87-af0c-43b1-93cf-f278d9c90846", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

# Directives de l'agent — Drave

> **Révision documentaire — 2026-10-27 (passe 2/2, appliquée).** Compteurs
> unifiés (**49 portes, 8 chapitres, 185 fichiers / 252 JSON, 54 documents**), chemins archivés
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
9. **Les illustrations sont des SVG.** Aucun **ASCII art** dans un bloc de code. Un schéma est un
   **`.svg`** — direct, ou généré par **docwatch** depuis `.mmd`/`.puml` (l'image pointe vers
   `<source>.svg`) — avec `viewBox`, `<title>`, `<desc>`, liens relatifs ; il vit dans
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

⏵ Exploration du dépôt et des modules M1/M2 existants
Je commence par lire l'état du dépôt et les modules concernés.

- **bash** `{"command": "ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet | head -40; echo ---; ls tools/cerveau/ | head -50", "description": "List repo root and cerveau tools", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
total 200
drwxr-xr-x. 1 stephane stephane   652 27 oct 12:52 .
drwxr-xr-x. 1 stephane stephane  2464 27 oct 12:53 ..
-rw-r--r--. 1 stephane stephane  8729 27 oct 16:20 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  1056 26 oct 11:22 data
drwxr-xr-x. 1 stephane stephane   942 27 oct 16:21 docs
drwxr-xr-x. 1 stephane stephane    82 28 sep 11:58 drave-core
drwxr-xr-x. 1 stephane stephane   178 27 oct 18:47 .git
-rw-r--r--. 1 stephane stephane   520 27 oct 16:20 .gitignore
-rw-r--r--. 1 stephane stephane   105 27 oct 12:51 .gitmodules
drwxr-xr-x. 1 stephane stephane  6730 27 oct 14:33 journal
drwxr-xr-x. 1 stephane stephane   100 15 oct 09:02 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-------. 1 stephane stephane 19705 27 oct 12:52 README.md
drwxr-xr-x. 1 stephane stephane 21524 27 oct 16:39 reports
-rw-------. 1 stephane stephane 12170 27 oct 16:20 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane 10507 30 sep 
… [1151 caractères tronqués]
  ```

- **bash** `{"command": "git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet status --porcelain | head -30; echo ---; git -C /home/stephane/Data13TB/stephane/GitHub/Qtrinet log --oneline -5", "description": "Check git status and recent log"}`

  ```
M docs/README.md
---
d6fd9c85 A7.5 — GRAPPE SUR RÉSEAU : 4,44× MOINS D'OCTETS, FIDÉLITÉ 1 792/1 792, 0,125 MS LOOPBACK
075b132a DOCWATCH — v0.4.1 : REDIRECTION DES URLS DE DOSSIER
3d03b2cb DOCWATCH — v0.4.0 : MULTI-RACINES ET DIAGRAMMES PLANTUML/MERMAID
98bf85a3 DOCS — DOCWATCH MULTI-RACINES, 87 TESTS, SVG GÉNÉRÉS ; ÉTAT C6 À JOUR
e49463d1 DOCS — ÉTAT ET RÉFÉRENCES À JOUR (B22/B23, PASSE 27/10, 185/252/54) ; SVG DOCWATCH IGNORÉS
  ```

### 🤖 Assistant

⏵ Lecture du routeur B23 et des modules M1/M2
J'inspecte les interfaces existantes.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/routeur_m1_m2.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/routeur_m1_m2.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """routeur_m1_m2.py — B23 : routeur lexique + forme entre M1 et M2.
3: 
4: Le routeur ne devine pas : il choisit un canal selon la surface.
5: - surface déjà connue (ou sa casse normalisée) -> M1 ;
6: - surface longue avec espaces (phrase) -> M1 ;
7: - sinon (typo, espacement anormal) -> M2.
8: 
9: Les prédictions M1 et M2 sont calculées **une seule fois**, puis comparées.
10: """
11: from __future__ import annotations
12: 
13: import json
14: import random
15: 
16: from .hub import Hub
17: from .m2_typo import _reels, _typo
18: from .voies import entrainer, evaluer_champs
19: from semantique.typed_corpus import ItemType
20: from semantique.universaux import code_rsn
21: from semantique.normalisation import normaliser
22: 
23: 
24: def _lexique(reels):
25:     return {normaliser(it.texte) for it in reels}
26: 
27: 
28: def router(surface: str, lexique: set[str]) -> str:
29:     if surface != surface.strip():
30:         return "M2"
31:     if normaliser(surface) in lexique:
32:         return "M1"
33:     if " " in surface and len(surf
… [2644 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/cerveau/tests/; echo ---; sed -n 1,80p tools/cerveau/hub.py", "description": "List tests and read hub head", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
total 132
drwxr-xr-x. 1 stephane stephane   834 27 oct 16:37 .
drwxr-xr-x. 1 stephane stephane   640 27 oct 16:13 ..
-rw-r--r--. 1 stephane stephane     0 27 oct 08:41 __init__.py
drwxr-xr-x. 1 stephane stephane  1384 27 oct 16:37 __pycache__
-rw-r--r--. 1 stephane stephane   942 27 oct 08:56 test_bus.py
-rw-r--r--. 1 stephane stephane  3112 27 oct 10:06 test_episodique.py
-rw-------. 1 stephane stephane  7736 27 oct 10:53 test_gating.py
-rw-r--r--. 1 stephane stephane   813 27 oct 16:37 test_grappe_reseau.py
-rw-r--r--. 1 stephane stephane   466 27 oct 15:24 test_lesion_complet.py
-rw-------. 1 stephane stephane  5414 27 oct 11:03 test_lesion.py
-rw-r--r--. 1 stephane stephane   624 27 oct 15:09 test_m2_secours.py
-rw-r--r--. 1 stephane stephane   583 27 oct 15:29 test_m2_typo.py
-rw-r--r--. 1 stephane stephane  5081 27 oct 10:06 test_memoire_travail.py
-rw-r--r--. 1 stephane stephane   772 27 oct 08:56 test_modules.py
-rw-------. 1 stephane stephane 11342 27 oct 12:34 test_multilingue.py
-rw-------. 1 stephane stephane  6241 27 oct 12:44 test_neuromodulation.py
-rw-r--r--. 1 stephane stephane   799 27 oct 12:58 test_pipeline_memoire.py
-rw-r--r--. 1 stephane stephane   810 27 oct
… [2309 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_routeur_m1_m2.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/m2_typo.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/tests/test_routeur_m1_m2.py</path>
<type>file</type>
<content>
1: from __future__ import annotations
2: import unittest
3: try:
4:     from cerveau.routeur_m1_m2 import router, _lexique, _reels
5:     _TORCH = True
6: except ImportError:
7:     _TORCH = False
8: 
9: 
10: @unittest.skipUnless(_TORCH, "torch absent")
11: class TestRouteur(unittest.TestCase):
12:     def test_router(self):
13:         lex = _lexique(_reels())
14:         self.assertEqual(router("e2e4", lex), "M1")
15:         self.assertEqual(router("  e2e4  ", lex), "M2")
16:         self.assertEqual(router("le coup e2e4 est joue", lex), "M1")
17: 
18: 
19: if __name__ == "__main__":
20:     unittest.main()

(End of file - total 20 lines)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/m2_typo.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """m2_typo.py — B22 : quelles typos M2 sauve-t-il ?
3: 
4: B19 a montré que M2 sauve les suppressions de caractère (71,9/75,1 %) mieux que
5: M1 (36,8 %). Ici on distingue suppression, substitution, insertion et
6: transposition, à code constant.
7: """
8: from __future__ import annotations
9: 
10: import json
11: import random
12: 
13: from .hub import Hub
14: from .voies import entrainer, evaluer_champs
15: from semantique.typed_corpus import ItemType
16: from semantique.universaux import code_rsn
17: from jeux.corpus import construire_corpus
18: from jeux.corpus_multilingue import construire_corpus_multilingue
19: 
20: 
21: def _reels():
22:     return [it for c in (construire_corpus(), construire_corpus_multilingue())
23:             for it in c.items if it.attendu.nature == "coup"]
24: 
25: 
26: def _typo(texte: str, mode: str, rng: random.Random) -> str:
27:     if len(texte) < 3:
28:         return texte
29:     i = rng.randrange(1, len(texte) - 1)
30:     if mode == "suppression":
31:         return texte[:i] + texte[i + 1:]
32:     
… [2150 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,160p tools/cerveau/voies.py", "description": "Read voies head", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

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
… [5601 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des artefacts B23 et du checkpoint M2
Je cherche les rapports B23, les JSON de mesure et les checkpoints disponibles.

- **bash** `{"command": "grep -ril \"B23\" reports journal docs --include='*.md' --include='*.json' | head -30", "description": "Find B23 references", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
reports/INDEX.md
reports/README.md
reports/rapport-routeur-m1-m2.md
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md
journal/sessions/4e786d3f-0b66-4b23-8dc4-b452bc383bea/digest.md
journal/sessions/4e786d3f-0b66-4b23-8dc4-b452bc383bea/rapport.md
journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/digest.md
journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/rapport.md
journal/sessions/482522d1-31f1-43eb-ae9c-a681336404f7/digest.md
journal/sessions/a4277668-3825-4797-bf0b-d7addcbb569d/digest.md
journal/README.md
journal/2026-10-15.md
journal/2026-10-15_modele.md
journal/2026-10-16.md
journal/2026-10-16_apprentissage.md
journal/2026-10-16_docs.md
journal/2026-10-27.md
journal/2026-10-27_memoire.md
journal/2026-10-27_docs.md
journal/2026-10-27_sprint-24h.md
docs/carte.md
docs/roadmap.md
docs/en-cours.md
  ```

- **bash** `{"command": "ls -d /tmp/natif* /tmp/*routeur* /tmp/a19* 2>/dev/null; echo ---; ls /tmp | head -40; echo ---; nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv 2>/dev/null || echo no-gpu", "description": "Check tmp checkpoints and GPU"}`

  ```
/tmp/natif-224-6-align-s1
/tmp/natif-224-6-align-s1.log
/tmp/natif-224-6-align-s2
/tmp/natif-224-6-align-s2.log
/tmp/natif-224-6-align-s3
/tmp/natif-224-6-align-s3.log
/tmp/natif-224-6-controle-s1
/tmp/natif-224-6-controle-s1.log
/tmp/natif-224-6-controle-s2
/tmp/natif-224-6-controle-s2.log
/tmp/natif-224-6-controle-s3
/tmp/natif-224-6-controle-s3.log
/tmp/natif-232-6-align-s1
/tmp/natif-232-6-align-s1.log
/tmp/natif-232-6-align-s2
/tmp/natif-232-6-align-s2.log
/tmp/natif-232-6-align-s3
/tmp/natif-232-6-align-s3.log
/tmp/natif-232-6-controle-s1
/tmp/natif-232-6-controle-s1.log
/tmp/natif-232-6-controle-s2
/tmp/natif-232-6-controle-s2.log
/tmp/natif-232-6-controle-s3
/tmp/natif-232-6-controle-s3.log
/tmp/natif-240-6-align-s1
/tmp/natif-240-6-align-s1.log
/tmp/natif-240-6-align-s2
/tmp/natif-240-6-align-s2.log
/tmp/natif-240-6-align-s3
/tmp/natif-240-6-align-s3.log
/tmp/natif-240-6-controle-s1
/tmp/natif-240-6-controle-s1.log
/tmp/natif-240-6-controle-s2
/tmp/natif-240-6-controle-s2.log
/tmp/natif-240-6-controle-s3
/tmp/natif-240-6-controle-s3.log
/tmp/natif-256-6-align-s1
/tmp/natif-256-6-align-s1.log
/tmp/natif-256-6-align-s2
/tmp/natif-256-6-align-s2.log
/tmp/natif-256-6-align-s3

… [5626 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du rapport B23 et des mesures existantes
Je récupère les chiffres exacts et le protocole de B23.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-routeur-m1-m2.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-routeur-m1-m2.md</path>
<type>file</type>
<content>
1: # B23 — routeur M1→M2 : gagne sur les espaces, perd sur les typos
2: 
3: > **Objet.** M1 est exact sur les surfaces connues, M2 sauve les typos. Un routeur simple choisit
4: > M1 si la surface est connue (ou une phrase longue), M2 sinon. Mesure sur les **146 items `de`**,
5: > **3 graines**, 300 pas.
6: 
7: ## Résultats (moyennes 3 graines)
8: 
9: | mode | M1 | M2 | **routeur** | part M2 |
10: |---|---:|---:|---:|---:|
11: | original | **100 %** | 93,15 % | **100 %** | 0 % |
12: | casse | **99,32 %** | 93,15 % | **99,32 %** | 0 % |
13: | espaces | 11,64 % | **41,78 %** | **41,78 %** | 100 % |
14: | typo | 47,72 % | **68,27 %** | **56,16 %** | 60 % |
15: | phrase | **92,47 %** | 0 % | **92,47 %** | 0 % |
16: 
17: ## Lecture
18: 
19: - Le routeur **préserve** M1 sur original, casse et phrase.
20: - Il **bascule** sur M2 pour les espaces et gagne **+30,1 pts** (11,6 → 41,8).
21: - Sur les typos, il ne fait que **56,2 %** contre **68,3 %** pour M2 : **40 %** des typos
22:   normalisées tombent sur une **autre surface valide** du lexique, donc le routeur choisit M
… [1067 caractères tronqués]
  ```

- **bash** `{"command": "grep -rl \"routeur\" /tmp/*.json 2>/dev/null | head; echo ---; grep -n -A3 -B3 \"B23\" docs/roadmap.md | head -60", "description": "Find router JSON and roadmap B23", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
/tmp/b23-seeds.json
---
361-| B12.8 | **M8 sommeil** | ❌ **marginal** | 96,48 % de champs mais exact **65,1 %**, baseline par jeu **96,10 %** ; leave-one-code-out exact **0 % par construction**, non nuls 63,5 % ; coordonnées 0 % |
362-| B12.9 | **M9 lésion** | ✅ **table** | contexte **29,2 %** ; M2 ventrale **24,7 %** ; M2 dorsale **2,1 %** ; M7 **13,7 %** ; M3 **0** ; M4 **0** ; M5 **1,1 %** ; M6 **30 %** ; M8 **0** |
363-| B12.10 | **Pipeline M1 → M4 → M8** | ⚠️ **intégration** | **528/528**, 7 prototypes, 96,33 % de complétion — tautologique : M4 ne généralise pas, M8 est la marginale |
364:| B23.1 | **Routeur M1→M2** | ⚠️ **partiel** | original **100 %**, casse **99,3 %**, phrase **92,5 %** = M1 ; espaces **41,8 %** vs M1 **11,6 %** ; typo **56,2 %** < M2 **68,3 %** (collision de lexique) ; pas un oracle |
365-| B22.1 | **M2 et les typos** | ⚠️ **niche robuste** | M1 suppression **32,8 %**, substitution **27,1 %**, insertion **44,5 %**, transposition **24,1 %** ; M2 `de` **72,6 / 62,3 / 66,4 / 70,5 %**, `vers` **80,1 / 65,8 / 70,6 / 73,3 %** ; avantage +21,9 à +46,5 pts |
366-| B21.1 | **M9 par dose** | ✅ **dose** | M3 span **0/4/8/12/12** (linéaire, tautologique) ; M5 ordre 0/
… [939 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np='/tmp/b23-seeds.json'\nd=json.load(open(p))\nprint(json.dumps(d, ensure_ascii=False, indent=1)[:5000])\nEOF", "description": "Inspect B23 seeds JSON"}`

  ```
{
 "1": {
  "n": 146,
  "modes": {
   "original": {
    "M1": 1.0,
    "M2": 0.9315068493150684,
    "routeur": 1.0,
    "part_M2": 0.0
   },
   "casse": {
    "M1": 0.9931506849315068,
    "M2": 0.9315068493150684,
    "routeur": 0.9931506849315068,
    "part_M2": 0.0
   },
   "espaces": {
    "M1": 0.11643835616438356,
    "M2": 0.3561643835616438,
    "routeur": 0.3561643835616438,
    "part_M2": 1.0
   },
   "typo": {
    "M1": 0.4452054794520548,
    "M2": 0.678082191780822,
    "routeur": 0.5821917808219178,
    "part_M2": 0.5958904109589042
   },
   "phrase": {
    "M1": 0.9246575342465754,
    "M2": 0.0,
    "routeur": 0.9246575342465754,
    "part_M2": 0.0
   }
  }
 },
 "2": {
  "n": 146,
  "modes": {
   "original": {
    "M1": 1.0,
    "M2": 0.9315068493150684,
    "routeur": 1.0,
    "part_M2": 0.0
   },
   "casse": {
    "M1": 0.9931506849315068,
    "M2": 0.9315068493150684,
    "routeur": 0.9931506849315068,
    "part_M2": 0.0
   },
   "espaces": {
    "M1": 0.11643835616438356,
    "M2": 0.4246575342465753,
    "routeur": 0.4246575342465753,
    "part_M2": 1.0
   },
   "typo": {
    "M1": 0.4863013698630137,
    "M2": 0.6506849315068494,
    "routeur": 0.513698630136
… [843 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/routeur-m1-m2.json 2>/dev/null && python3 -c \"import json;print(json.dumps(json.load(open('reports/routeur-m1-m2.json')),ensure_ascii=False,indent=1))\" | head -80", "description": "Inspect B23 report JSON", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
reports/routeur-m1-m2.json
{
 "n": 146,
 "seeds": [
  1,
  2,
  3
 ],
 "modes": {
  "original": {
   "M1": 1.0,
   "M2": 0.9315068493150683,
   "routeur": 1.0,
   "part_M2": 0.0
  },
  "casse": {
   "M1": 0.9931506849315067,
   "M2": 0.9315068493150683,
   "routeur": 0.9931506849315067,
   "part_M2": 0.0
  },
  "espaces": {
   "M1": 0.11643835616438354,
   "M2": 0.41780821917808214,
   "routeur": 0.41780821917808214,
   "part_M2": 1.0
  },
  "typo": {
   "M1": 0.4771689497716895,
   "M2": 0.682648401826484,
   "routeur": 0.5616438356164384,
   "part_M2": 0.6004566210045662
  },
  "phrase": {
   "M1": 0.9246575342465754,
   "M2": 0.0,
   "routeur": 0.9246575342465754,
   "part_M2": 0.0
  }
 },
 "par_graine": {
  "1": {
   "n": 146,
   "modes": {
    "original": {
     "M1": 1.0,
     "M2": 0.9315068493150684,
     "routeur": 1.0,
     "part_M2": 0.0
    },
    "casse": {
     "M1": 0.9931506849315068,
     "M2": 0.9315068493150684,
     "routeur": 0.9931506849315068,
     "part_M2": 0.0
    },
    "espaces": {
     "M1": 0.11643835616438356,
     "M2": 0.3561643835616438,
     "routeur": 0.3561643835616438,
     "part_M2": 1.0
    },
    "typo": {
     "M1": 0.4452054794520548,
    
… [308 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection du modèle, du corpus et du coût de B23
Je vérifie la taille du checkpoint, les surfaces réelles et les temps de B23.

- **bash** `{"command": "python3 - <<'EOF'\nimport json,os\np='/tmp/natif-600-512-8-align-s1'\nprint(os.listdir(p))\ncfg=json.load(open(os.path.join(p,'config.json')))\nfor k in ('model_type','hidden_size','num_hidden_layers','num_attention_heads','vocab_size','n_positions','max_position_embeddings'):\n    prin … [224 caractères tronqués]`

  ```
['model.safetensors', 'generation_config.json', 'config.json']
model_type qwen3_moe
hidden_size 512
num_hidden_layers 8
num_attention_heads 8
vocab_size 256
n_positions None
max_position_embeddings 512
params-ish bytes 126.553768 MB
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nfrom cerveau.m2_typo import _reels\nfrom semantique.normalisation import normaliser\nfrom semantique.universaux import code_rsn\nr=_reels()\nprint('n',len(r))\nfor it in r[:12]:\n    print(repr(it.texte), '|', repr(normaliser(it … [272 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/m2_typo.py", line 14, in <module>
    from .voies import entrainer, evaluer_champs
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/cerveau/voies.py", line 48, in <module>
    import torch
ModuleNotFoundError: No module named 'torch'
[exit code: 1]
  ```

### 🤖 Assistant

⏵ Recherche de l'environnement Python avec torch
Je localise l'interpréteur et le venv utilisés par les tests.

- **bash** `{"command": "which -a python3 python; echo ---; ls -d .venv venv env 2>/dev/null; echo ---; find /home/stephane/Data13TB/stephane/GitHub/Qtrinet -maxdepth 2 -name 'pyvenv.cfg' 2>/dev/null; echo ---; conda env list 2>/dev/null; echo ---; ls /home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore;  … [133 caractères tronqués]`

  ```
/usr/bin/python3
/bin/python3
---
---
---
---
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore
__pycache__/
*.pyc
reports/*.tmp
models/
data/
qtrinet-core/target/

# Traces de session : la copie brute reste sur disque (volumineuse, binaire),
# le digest markdown est versionné.
journal/sessions/*/session.jsonl.zstd
journal/sessions/archive.log

# Outil de référence : la source est versionnée, le binaire se recompile
# (commande exacte dans tools/ref_logits.md).
tools/ref_logits
target/

# docwatch — SVG générés depuis les sources .puml/.mmd (docwatch les produit)
docs/**/*.puml.svg
docs/**/*.mmd.svg
[stderr]
which: no python in (/home/stephane/IA/outils:/usr/local/cuda-13/bin:/home/stephane/.lmstudio/bin:/home/stephane/IA/outils:/home/stephane/.local/share/../bin:/home/stephane/.cargo/bin:/usr/local/cuda-13/bin:/home/stephane/.lmstudio/bin:/home/stephane/.local/bin:/usr/local/bin:/usr/bin:/bin:/home/stephane/.dotnet/tools:/home/stephane/.lmstudio/bin:/home/stephane/.lmstudio/bin:/home/stephane/.lmstudio/bin)
  ```

- **bash** `{"command": "ls ~/.pyenv/versions 2>/dev/null; ls /opt 2>/dev/null; grep -rn \"python\" AGENTS.md | head; grep -rn \"venv\\|activate\\|python3\" REPRISE.md | head -20", "description": "Look for environment hints", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
containerd
google
microsoft
38:4. **La revue de documentation** avant chaque commit de clôture : `python3 tools/revue_documentation.py` (et
55:   `docs/schemas/` ou `docs/synthese/schemas/`. Vérifier : `python3 tools/verifier_schemas.py`.
87:> `python3 tools/taille_documents.py`.
96:- le budget de contexte est vérifié : `python3 tools/taille_documents.py`.
97:- les schémas sont des SVG valides et référencés : `python3 tools/verifier_schemas.py`.
  ```

### 🤖 Assistant

⏵ Localisation de l'installation torch dans le système
Je cherche les interpréteurs et packages disponibles.

- **bash** `{"command": "ls /home/stephane/IA 2>/dev/null; echo ---; find /home/stephane -maxdepth 4 -type d -name 'torch' 2>/dev/null | head; echo ---; find / -maxdepth 4 -type d -name 'site-packages' 2>/dev/null | head -20", "description": "Search for torch and site-packages"}`

  ```
artefacts
cache
docs
drave-data
k3-nvme
lost+found
migration-logs
migration-logs-phase1.out
modeles
modeles-lourds
outils
README.md
scratch
venv-drave
---
---
/usr/lib/python3.13/site-packages
/usr/lib/python3.14/site-packages
/usr/lib64/python3.13/site-packages
/usr/lib64/python3.14/site-packages
  ```

- **bash** `{"command": "python3 -c \"import sys; print(sys.version); print(sys.path)\"; echo ---; ls /usr/lib/python3/dist-packages | head; echo ---; pip3 list 2>/dev/null | head -30", "description": "Inspect system python packages"}`

  ```
3.13.15 (main, Sep 16 2026, 12:10:42) [GCC]
['', '/usr/lib64/python313.zip', '/usr/lib64/python3.13', '/usr/lib64/python3.13/lib-dynload', '/home/stephane/.local/lib/python3.13/site-packages', '/usr/lib64/python3.13/site-packages', '/usr/lib64/python3.13/site-packages/PIL', '/usr/lib64/python3.13/_import_failed', '/usr/lib/python3.13/site-packages']
---
---
Package                                    Version
------------------------------------------ -----------
aiodns                                     4.0.4
aiohappyeyeballs                           2.7.1
aiohttp                                    3.14.3
aioquic                                    1.3.0
aiosignal                                  1.4.0
antlr4-python3-runtime                     4.13.2
anyio                                      4.14.2
appdirs                                    1.4.4
applicationinsights                        0.11.10
argcomplete                                3.6.3
argon2-cffi                                25.1.0
argon2-cffi-bindings                       25.1.0
arrow                                      1.4.0
asttokens                                  3.0.2
async-lru                                
… [740 caractères tronqués]
  ```

- **bash** `{"command": "ls /home/stephane/IA/venv-drave/bin | head; /home/stephane/IA/venv-drave/bin/python -c \"import torch,transformers;print(torch.__version__, transformers.__version__, torch.cuda.is_available())\"", "description": "Check drave venv torch"}`

  ```
accelerate
accelerate-config
accelerate-estimate-memory
accelerate-launch
accelerate-merge-weights
activate
activate.bat
activate.csh
activate.fish
activate.nu
2.14.1+cu130 5.20.1 True
  ```

### 🤖 Assistant

⏵ Vérification des imports et des surfaces réelles
J'utilise le venv Drave et je mesure le comportement M1.

- **bash** `{"command": "ls tools | head -40; echo ---; PYTHONPATH=tools /home/stephane/IA/venv-drave/bin/python - <<'EOF'\nfrom cerveau.m2_typo import _reels\nfrom semantique.normalisation import normaliser\nprint('n',len(_reels()))\nfor it in _reels()[:10]:\n    print(repr(it.texte), '->', repr(normaliser(it. … [134 caractères tronqués]`

  ```
adaptateur_langue.py
aiguille.py
aligneur_litteraire.py
amplification.py
analyse_alignement.py
analyse_empreinte.py
analyse_engram.py
analyse_experts_statique.py
analyse_flux.py
analyse_hc.py
analyse_litteraire.py
analyse_octets_par_jeton.py
analyse_reutilisation_experts.py
analyse_union_experts.py
ancre_professeur.py
applique_pont.py
approximabilite_bloc.py
apres-telechargement-k3.sh
archive_sessions.py
audit_drapeaux_harnais.py
banc-experts.py
banc_lecteur.py
banc-prelire.py
blanchiment_entree.py
boucle-cerveau.sh
boucle_directe.py
bruit_entree.py
budget_execution_locale.py
c4_retard.sh
c8_carte_profondeur.sh
c8_corpus.sh
c8_entrainer_tete.py
c8_sonde_lineaire.py
cache_pont.py
calibre_modes.py
campagne-benefices.sh
campagne_synthese.py
cancellation_langue.py
carte_coupe.sh
carte-facultes.sh
---
n 528
'A1' -> 'a1' morpion
'a1' -> 'a1' morpion
'(1,1)' -> '' morpion
'1 1' -> '1 1' morpion
'ligne 1 colonne 1' -> 'ligne 1 colonne 1' morpion
'case 1' -> 'case 1' morpion
'haut gauche' -> 'haut gauche' morpion
'en haut à gauche' -> 'en haut [cartes.rang.14] gauche' morpion
'top left' -> '[echecs.piece.R] left' morpion
'coin haut gauche' -> 'coin haut gauche' morpion
  ```

- **bash** `{"command": "sed -n 1,120p semantique/normalisation.py 2>/dev/null || find tools -name normalisation.py", "description": "Read normalization module", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
tools/semantique/normalisation.py
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/semantique/normalisation.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/semantique/normalisation.py</path>
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
28:
… [1319 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def evaluer_champs\\|def entrainer\\|def _lots\\|def encoder\" tools/cerveau/voies.py; sed -n 260,430p tools/cerveau/voies.py", "description": "Read evaluer_champs implementation", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
424:def entrainer(base, pas: int = 400, lot: int = 32, seq: int = 64, graine: int = 1,
638:def evaluer_champs(m, val, champs=None, device: str = "cuda", lesions: bool = True,
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
    for lan
… [5767 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 424,560p tools/cerveau/voies.py; echo ====; sed -n 620,760p tools/cerveau/voies.py", "description": "Read training/eval functions", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
def entrainer(base, pas: int = 400, lot: int = 32, seq: int = 64, graine: int = 1,
              device: str = "cuda", synth: bool = False, champs=None,
              pool: str = "mean+last", contexte: bool = False, seq_ctx: int = 192,
              augmentation=False, familles=("formes",), positions: int = 0,
              exclure_surfaces=None, normaliseur=None):
    """Entraîne les têtes sur les surfaces synthétiques.

    `champs` est la liste des champs dorsaux à apprendre. Par défaut `("de",)`,
    ce qui reproduit le prototype d'origine (une seule tête dorsale).

    Pour plusieurs champs, chaque pas forme un lot composite : un bloc d'items
    par champ (et un bloc d'action), une seule passe avant, et une perte par
    tête calculée sur son bloc. L'encodeur étant gelé, c'est équivalent à des
    passes séparées ; c'est simplement plus rapide.

    `augmentation` : `False` (défaut, comportement A3), `True` (familles
    `familles`) ou un tuple de familles (`"formes"`, `"positions"`). Voir
    `augmenter` ; `exclure_surfaces` est la garde anti-fuite (par défaut, les
    surfaces réelles de `items()`, jamais utilisées à l'entraînement).
    """
    rng = random.Random(graine)

… [10918 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Analyse des collisions de lexique dans les typos
Je mesure quelles typos tombent dans le lexique, et si elles viennent d'un autre jeu.

- **bash** `{"command": "cat > /tmp/a19_analyse.py <<'EOF'\nimport sys, random, collections\nsys.path.insert(0,'tools')\nfrom cerveau.m2_typo import _reels, _typo\nfrom cerveau.routeur_m1_m2 import _perturber, _lexique, router\nfrom cerveau.hub import Hub\nfrom semantique.normalisation import normaliser\nfrom s … [1899 caractères tronqués]`

  ```
de items 146 lex 82
M1 typo 0.0 collisions 3 M1 ok on coll 0.0
M1 ok on noncoll 0.0
collisions same game 3 / 3
'e4' -> 'e4' jeu echecs norm 'e4' same True ok 0
'E4' -> 'E4' jeu echecs norm 'e4' same True ok 0
'peon e2 e4' -> 'peono e2 e4' jeu echecs norm '[echecs.piece.P] e2 e4' same True ok 0
  ```

### 🤖 Assistant

⏵ Débogage de la reproduction des typos B23
Je vérifie la séquence exacte et la distribution des décisions.

- **bash** `{"command": "cat > /tmp/a19_analyse2.py <<'EOF'\nimport sys, random, collections\nsys.path.insert(0,'tools')\nfrom cerveau.m2_typo import _reels, _typo\nfrom cerveau.routeur_m1_m2 import _perturber, _lexique, router\nfrom semantique.normalisation import normaliser\nfrom semantique.universaux import  … [949 caractères tronqués]`

  ```
de items 146 lex 82
original Counter({'M1': 146})
casse Counter({'M1': 146})
espaces Counter({'M2': 146})
typo Counter({'M2': 87, 'M1': 59})
coll 3
('e4', 'e4', 'e4')
('E4', 'E4', 'e4')
('peono e2 e4', 'peon e2 e4', '[echecs.piece.P] e2 e4')
samples [('e2e4', 'ee4'), ('e2-e4', 'e2-4'), ('e2 e4', 'e e4'), ('e4', 'e4'), ('E4', 'E4'), ('le pion de e2 vers e4', 'le pion d e2 vers e4'), ('pawn from e2 to e4', 'pawnfrom e2 to e4'), ('Nf3', 'N3'), ('Cf3', 'C3'), ('g1f3', 'g13')]
lens [2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23] max 26
phrase Counter({'M1': 146})
  ```

### 🤖 Assistant

⏵ Cartographie des 146 items et du round-trip M1
Je caractérise les surfaces et le rendu M1 avant de fixer le score.

- **bash** `{"command": "cat > /tmp/a19_surfaces.py <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools')\nfrom cerveau.m2_typo import _reels\nfrom cerveau.hub import Hub\nfrom semantique.normalisation import normaliser\nfrom semantique.universaux import code_rsn\nfrom jeux.codecs import codec\n\nreels=[ … [1078 caractères tronqués]`

  ```
n 146
Counter({'echecs': 146})
Counter({'ml-echecs-nf3': 61, 'ml-echecs-e4': 61, 'echecs-e4': 7, 'echecs-nf3': 6, None: 4, 'echecs-petit-roque': 2, 'echecs-grand-roque': 2, 'echecs-promotion': 2, 'echecs-ep': 1})
'e2e4' | echecs | echecs-e4 | e2e4 | {'jeu': 'echecs', 'action': 'deplacer', 'de': 52, 'vers': 36, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}
'e2-e4' | echecs | echecs-e4 | e2-e4 | {'jeu': 'echecs', 'action': 'deplacer', 'de': 52, 'vers': 36, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}
'e2 e4' | echecs | echecs-e4 | e2 e4 | {'jeu': 'echecs', 'action': 'deplacer', 'de': 52, 'vers': 36, 'promotion': None, 'roque': None, 'case': None, 'symbole': None, 'carte': None, 'taille': None, 'point': None, 'passe': None, 'chemin_0': None, 'chemin_1': None, 'chemin_2': None}
'e4' | echecs | echecs-e4 | e4 | {'jeu': 'echecs', 'action': 'deplacer', 'de': 52, 'vers': 36, 'promotion': None, 'roque': None, 'case': None, 'sy
… [11411 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Compréhension de ItemType et du rendu contextuel
Je lis la structure des items pour comparer codes et surfaces correctement.

- **bash** `{"command": "grep -n \"class ItemType\" -A80 tools/semantique/typed_corpus.py | head -100; echo ====; grep -n \"def rend\\|def lit\" tools/jeux/codecs/echecs.py | head", "description": "Read ItemType and chess codec API", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
21:class ItemType:
22-    texte: str
23-    code: dict
24-    jeu: str
25-    nature: str
26-    langue: str
27-    paire: str
28-    format: str
29-    contexte: str = ""
30-
31-
32-def items() -> list[ItemType]:
33-    out = []
34-    vus = set()
35-    for corpus in (construire_corpus(), construire_corpus_multilingue()):
36-        for it in corpus.items:
37-            if it.attendu.nature != "coup":
38-                continue
39-            cle = (it.texte, it.jeu, it.paire, it.langue)
40-            if cle in vus:
41-                continue
42-            vus.add(cle)
43-            out.append(ItemType(it.texte, code_item(it), it.jeu, it.attendu.nature,
44-                                it.langue, it.paire, it.format, resume_contexte(it.contexte)))
45-    return out
46-
47-
48-def decouper(items_: list[ItemType], graine: int = 1, fraction: float = 0.2):
49-    paires = sorted({i.paire for i in items_ if i.paire})
50-    rng = random.Random(graine)
51-    rng.shuffle(paires)
52-    n_val = max(1, int(len(paires) * fraction))
53-    val_paires = set(paires[:n_val])
54-    train = [i for i in items_ if i.paire not in val_paires]
55-    val = [i for i in items_ if i.paire in v
… [1554 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 400,470p tools/jeux/codecs/echecs.py; echo ====; grep -n \"def lire_contexte\\|def _contexte\\|contexte\" tools/jeux/codecs/echecs.py | head -30", "description": "Read chess render signature and context handling", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
if c is None:
                raise E.ErreurEchecs(f"coup PGN illisible : {j!r} ({a})")
            pos.joue(c)
            coups.append(c)
        if not coups:
            raise E.ErreurEchecs("PGN sans coup")
        return E.rsn_partie(depart, coups), amb

    # ------------------------------------------------------------------
    def rend(self, rsn: RSN, format: str = "canonique", langue: str = "fr",
             contexte: RSN | None = None) -> str:
        if rsn.jeu != "echecs":
            raise ValueError("ce n'est pas une RSN d'échecs")
        if rsn.nature == "etat":
            pos = E.position_depuis_rsn(rsn)
            if format in ("fen", "canonique"):
                return pos.fen()
            if format == "diagramme":
                lignes = []
                for r in range(8):
                    ligne = []
                    for c in range(8):
                        p = pos.plateau[r * 8 + c]
                        if not p:
                            ligne.append(".")
                        else:
                            ch = "pnbrqk"[E.typ(p) - 1]
                            ligne.append(ch.upper() if E.couleur(p) == E.BLANC else ch)
            
… [2766 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Calcul des features M1 sur toutes les perturbations
Je mesure round-trip, distances et marges, puis leur lien avec l'exactitude M1.

- **bash** `{"command": "cat > /tmp/a19_features.py <<'EOF'\nimport sys, random, collections\nsys.path.insert(0,'tools')\nfrom cerveau.m2_typo import _reels\nfrom cerveau.routeur_m1_m2 import _perturber, _lexique\nfrom cerveau.hub import Hub\nfrom semantique.normalisation import normaliser\nfrom semantique.univ … [3038 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "/tmp/a19_features.py", line 42, in <module>
    code_ok=int(p==it.code)
                   ^^^^^^^
AttributeError: 'Item' object has no attribute 'code'
[exit code: 1]
  ```

- **bash** `{"command": "sed -i 's/code_ok=int(p==it.code)/code=code_rsn(it.attendu); code_ok=int(p==code)/' /tmp/a19_features.py\nPYTHONPATH=tools /home/stephane/IA/venv-drave/bin/python /tmp/a19_features.py", "description": "Rerun feature analysis with correct codes", "workdir": "/home/stephane/Data13TB/steph … [20 caractères tronqués]`

  ```
== original M1 1.0
  connu 146 present 146 rt_eq 8 rt_in 76
  connu=1 n=146 M1=1.000
  rt_eq=0 n=138 M1=1.000
  rt_eq=1 n=8 M1=1.000
  rt_in=0 n=70 M1=1.000
  rt_in=1 n=76 M1=1.000
  sp=0 n=16 M1=1.000
  sp=1 n=130 M1=1.000
  lead=0 n=146 M1=1.000
  dl 0-0 n=146 M1=1.000
  dlj 0-0 n=146 M1=1.000
== casse M1 0.9931506849315068
  connu 146 present 145 rt_eq 8 rt_in 76
  connu=1 n=146 M1=0.993
  rt_eq=0 n=138 M1=0.993
  rt_eq=1 n=8 M1=1.000
  rt_in=0 n=70 M1=0.986
  rt_in=1 n=76 M1=1.000
  sp=0 n=16 M1=0.938
  sp=1 n=130 M1=1.000
  lead=0 n=146 M1=0.993
  dl 0-0 n=146 M1=0.993
  dlj 0-0 n=146 M1=0.993
== espaces M1 0.11643835616438356
  connu 17 present 17 rt_eq 8 rt_in 13
  connu=0 n=129 M1=0.000
  connu=1 n=17 M1=1.000
  rt_eq=0 n=138 M1=0.065
  rt_eq=1 n=8 M1=1.000
  rt_in=0 n=133 M1=0.030
  rt_in=1 n=13 M1=1.000
  sp=0 n=146 M1=0.116
  lead=1 n=146 M1=0.116
  dl 0-0 n=17 M1=1.000
  dl 1-1 n=5 M1=0.000
  dl 2-2 n=4 M1=0.000
  dl 3-4 n=18 M1=0.000
  dl 5-99 n=102 M1=0.000
  dlj 0-0 n=17 M1=1.000
  dlj 1-1 n=5 M1=0.000
  dlj 2-2 n=4 M1=0.000
  dlj 3-4 n=18 M1=0.000
  dlj 5-99 n=102 M1=0.000
== typo M1 0.4452054794520548
  connu 3 present 67 rt_eq 3 rt_in 49
  connu=0 n=143 M1=0.434
 
… [3761 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du sous-ensemble M1 de B23 sur la typo
Je calcule l'exactitude M1 par décision B23 pour comprendre l'écart.

- **bash** `{"command": "cat > /tmp/a19_b23sub.py <<'EOF'\nimport sys, random, collections\nsys.path.insert(0,'tools')\nfrom cerveau.m2_typo import _reels\nfrom cerveau.routeur_m1_m2 import _perturber, _lexique, router\nfrom cerveau.hub import Hub\nfrom semantique.normalisation import normaliser\nfrom semantiqu … [1167 caractères tronqués]`

  ```
M1 59 M1acc 0.423728813559322
M2 87 M1acc 0.45977011494252873
overall M1 0.4452054794520548
M1 wrong: 'le cavalier g1 va en f3' -> 'le cavaier g1 va en f3' len 22 sp True
M1 wrong: 'knight from g1 to f3' -> 'knigt from g1 to f3' len 19 sp True
M1 wrong: 'jezdec g1 f3' -> 'jezdc g1 f3' len 11 sp True
M1 wrong: 'springer g1 f3' -> 'springer g1 3' len 13 sp True
M1 wrong: 'knight g1 f3' -> 'knight g1f3' len 11 sp True
M1 wrong: 'cevalo g1 f3' -> 'cevalog1 f3' len 11 sp True
M1 wrong: 'caballo g1 f3' -> 'caballo g1 3' len 12 sp True
M1 wrong: 'zalduna g1 f3' -> 'zlduna g1 f3' len 12 sp True
M1 wrong: 'cavalier g1 f3' -> 'cavalier g1f3' len 13 sp True
M1 wrong: 'cabalo g1 f3' -> 'caalo g1 f3' len 11 sp True
M1 wrong: 'skakac g1 f3' -> 'skaka g1 f3' len 11 sp True
M1 wrong: 'huszar g1 f3' -> 'huszar g1 3' len 11 sp True
M1 wrong: 'cavallo g1 f3' -> 'cavallog1 f3' len 12 sp True
M1 wrong: 'მხედარი g1 f3' -> 'მხედარ g1 f3' len 12 sp True
M1 wrong: 'zirgas g1 f3' -> 'zigas g1 f3' len 11 sp True
M1 wrong: 'zirdzins g1 f3' -> 'zirdzins g1f3' len 13 sp True
M1 wrong: 'springer g1 f3' -> 'springerg1 f3' len 13 sp True
M1 wrong: 'sjakkbrikka springar g1 f3' -> 'sjakkbrikk springar g1 f3' len 25 
… [951 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test de reproduction d'une graine B23 et chronométrage
Je lance l'entraînement M2 seed 1 et compare aux chiffres publiés.

- **bash** `{"command": "cat > /tmp/a19_time.py <<'EOF'\nimport sys, random, time, json\nsys.path.insert(0,'tools')\nfrom cerveau.m2_typo import _reels, _typo\nfrom cerveau.routeur_m1_m2 import _perturber, _lexique\nfrom cerveau.hub import Hub\nfrom cerveau.voies import entrainer, evaluer_champs\nfrom semantiqu … [1327 caractères tronqués]`

  ```
Loading weights:   0%|          | 0/90 [00:00<?, ?it/s]Loading weights: 100%|██████████| 90/90 [00:00<00:00, 947.50it/s]
load 0.4382326602935791
train 16.754518270492554
original 0.9178082191780822 eval 0.34098148345947266
casse 0.9178082191780822 eval 0.39234328269958496
espaces 0.3082191780821918 eval 0.4077639579772949
typo 0.6712328767123288 eval 0.4239959716796875
phrase 0.0 eval 0.42465877532958984
total 19.193156480789185
  ```

### 👤 Utilisateur

Agent f0969e87-af0c-43b1-93cf-f278d9c90846 sent a message: 
Timebox : donne un point et écris /tmp/a19-routeur-confiance.json/.md dès qu'une mesure existe, même partielle ; termine ensuite.

### 🤖 Assistant

⏵ Vérification du contexte de rendu M1
Je contrôle comment le hub accepte le contexte, puis je code le module.

- **bash** `{"command": "sed -n 250,315p tools/jeux/codecs/echecs.py; echo ====; grep -n \"def resume_contexte\" -A20 tools/semantique/universaux.py; echo ====; grep -n \"def position_depuis_rsn\" -A25 tools/jeux/regles/echecs.py | head -40", "description": "Check context type handling", "workdir": "/home/steph … [38 caractères tronqués]`

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
… [4027 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Conception finalisée du score et du protocole
Je vérifie le bus (mémoire) puis j'écris le module.

- **bash** `{"command": "sed -n 1,80p tools/cerveau/bus.py", "description": "Read Bus implementation", "workdir": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"}`

  ```
#!/usr/bin/env python3
"""bus.py — le bus d'événements des modules cerveau-langage.

Un événement est un **fait** typé, horodaté, avec sa source. Le bus le journalise,
le pousse aux abonnés et sait le **rejouer**. C'est le contrat minimal qui permet
de composer M1–M9 sans les fondre dans un seul bloc.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterator


@dataclass(frozen=True)
class Evenement:
    type: str
    valeur: Any
    source: str
    t: int = 0
    meta: tuple[tuple[str, Any], ...] = ()

    def vers_dict(self) -> dict:
        return {"type": self.type, "source": self.source, "t": self.t,
                "valeur": self.valeur, "meta": dict(self.meta)}


class Bus:
    def __init__(self) -> None:
        self.journal: list[Evenement] = []
        self.abonnes: dict[str, list[Callable[[Evenement], None]]] = {}
        self._t = 0

    def abonner(self, type_: str, f: Callable[[Evenement], None]) -> None:
        self.abonnes.setdefault(type_, []).append(f)

    def publier(self, type_: str, valeur: Any, source: str,
                meta: dict | None = None) -> Evenement:
        self._t += 1
        e 
… [462 caractères tronqués]
  ```

- **bash** `{"command": "PYTHONPATH=tools python3 - <<'EOF'\ntry:\n    from cerveau.hub import Hub\n    from semantique.normalisation import normaliser\n    from semantique.universaux import code_rsn\n    h=Hub()\n    print('system python import ok', h.percevoir('e4','echecs',None))\nexcept Exception as e:\n    … [163 caractères tronqués]`

  ```
system python import ok None
  ```

