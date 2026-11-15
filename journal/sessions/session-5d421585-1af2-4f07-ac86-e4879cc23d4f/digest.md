# Session DSH — relecture

- identifiant : `session-5d421585-1af2-4f07-ac86-e4879cc23d4f`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 10:44:55
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche W4 (J3 matin, la part du pilote) : le manifeste à envoyer à Panini — les **26 signatures manquantes** (la liste des œuvres du §334 sans signature V14), la commande exacte qu'ils doivent lancer, le format attendu ; et le **rejeu des 60 paires** du protocole (`rapport-protocole-date.md`) sur ce qui est disponible, avec le contrôle négatif. Fiche `reports/rapport-panini-manifeste.md` + JSON. **Ne modifie rien chez Panini.**

### 👤 Utilisateur

<system-reminder>
The following workspace instructions may be relevant to your work. Use them as guidance when applicable. More specific instructions take precedence over broader ones. They do not override system, developer, or direct user instructions.

Instructions from: AGENTS.md

# Directives de l'agent — Drave

> **Compteurs vivants.** Dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; ne pas les recopier ici.

> **Porte d'entrée.** Lis ce fichier en entier (2 min) : il porte la **vision**, les règles non négociables et le
> **routage** vers le document de chaque tâche. Le détail n'est pas ici : il est dans [`docs/methode/`](docs/methode/)
> (tableau § 3). L'**état courant** est dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; la **roadmap** dans
> [`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md) ; le récit daté dans [`journal/`](journal/).

## 1. La vision (l'essentiel)

**Drave est une vision de l'IA centrée sur les flots de données, pas sur le calcul brut.** Les activations d'un
réseau sont des **faits** regroupés en **listes valuées poussées** vers leurs lecteurs : le coût du calcul devient proportionnel à l'**activité**, et le modèle devient **décomposable**, **répartissable** et **observable**. Le principe : la structure bat la taille. Construire le moteur et modèle optimisé qui rend cette structure observable, décomposable, répartissable et rejouable permet d'atteindre de nouveaux sommets. L'approche par **bus d'événements** rend chaque bloc fonctionnel optimisable, comparable et substituable (neuronal là où l'intuition aide, computationnel là où la fiabilité prime).

Né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de les
**combiner**, de les **décomposer** en couches et grappes exécutables par du matériel divers, voire **distribué
en réseau**, de les **diagnostiquer** en étudiant leurs **flux**, et de **rejouer** des événements.


## 2. Les règles non négociables

1. **Rangement** : `docs/` = état, vision, concepts (ce qui reste vrai quand les chiffres changent) ; `reports/` =
   résultats mesurés, fiches, JSON ; `journal/` = récit daté ; `data/` = corpus. *Un résultat qui traîne dans
   `docs/` **déménage**.* → [`docs/methode/rangement.md`](docs/methode/rangement.md)
2. **Un résultat** porte le chiffre, la mesure, le dispositif, un **contrôle négatif**, et **ce qui pourrait le
   rendre faux** — puis un **commit**, la **fiche** dans `reports/`, le **récit** dans `journal/`, l'**état** dans
   `docs/pilotage/en-cours.md`, et il **nomme sa ligne de roadmap** (A… / B… / N… / R…). *Sans contrôle négatif, ce n'est pas un
   résultat.* → [`docs/methode/resultats.md`](docs/methode/resultats.md)
3. **Les portes** : `bash tools/toutes-les-portes.sh` ; le registre est dans `$JOURNAUX/registre.txt` (affiché au
   lancement) et le verdict se lit par `awk '$2 != 0'` — **jamais** par les marqueurs ni à travers un tube. Rouges
   tolérées : **celles listées dans [`docs/pilotage/references-non-regression.md`](docs/pilotage/references-non-regression.md)** ; toute autre est une régression. →
   [`docs/methode/portes.md`](docs/methode/portes.md)
4. **La revue de documentation** avant chaque commit de clôture : `python3 tools/revue_documentation.py` (et
   `tools/porte-tableaux.sh`) ; **corriger** ce qu'elle signale. → [`docs/methode/rangement.md`](docs/methode/rangement.md)
5. **Panini et Nipada** à chaque cycle : lire ce qui a bougé chez eux, confronter ; la théorie va dans
   [`docs/theorie/genealogie-des-langues.md`](docs/theorie/genealogie-des-langues.md), **jamais** les chiffres. Leur avertissement :
   la surface capte **l'époque** (β +0,138) bien plus que la **filiation** (β +0,049) — contrôler la date dans tout
   test de style, la surface dans tout test de famille. → [`docs/methode/panini-nipada.md`](docs/methode/panini-nipada.md)
6. **Le miroir entrée/sortie** : toute mesure d'entrée se double d'une mesure de **sortie** (restitution, boucle) ;
   la **fluidité n'est pas la fidélité**. → [`docs/methode/miroir.md`](docs/methode/miroir.md)
7. **La roadmap** ([`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md)) : chaque chantier a une **prochaine action** ; l'ordre est la **valeur** et les **dépendances**, jamais une date. Un chantier est **fini** quand il est
   mesuré, écrit et committé ; il est **marqué**, et le suivant désigné.
8. **Ne jamais bloquer, ne jamais rester en attente** : une question humaine se **consolide** dans `en-cours` et on **continue** ; si une ligne est bloquée (corpus, compte, matériel), on prend la suivante
   — la **file « jamais en attente »** de la roadmap. → [`docs/methode/ressources.md`](docs/methode/ressources.md)
9. **Les illustrations sont des SVG.** Aucun **ASCII art** dans un bloc de code. Un schéma est un
   **`.svg`** — direct, ou généré par **docwatch** depuis `.mmd`/`.puml` (l'image pointe vers
   `<source>.svg`) — avec `viewBox`, `<title>`, `<desc>`, liens relatifs ; il vit dans
   `docs/schemas/` ou `docs/theorie/synthese/schemas/`. Vérifier : `python3 tools/verifier_schemas.py`.
   → [`docs/methode/illustrations.md`](docs/methode/illustrations.md)
10. **Pilotage : cycles longs, sous-agents, état unique.** Un goal par programme (`max_goal_rounds`
    1 000) ; on s'arrête sur un résultat mesuré, écrit, committé, ou un blocage. Les tâches
    indépendantes : **sous-agents** (2–4), sans toucher `en-cours`/`roadmap`/`AGENTS` ; ils
    rendent un **diff**. **État** : une session écrit `en-cours` à la fois ; aucun fait
    sans sa ligne (hook `verifie_etat_a_jour.py`). Git : `git add` explicite. La clôture met `en-cours` à jour (≤ 2 000 mots).
    → [`docs/methode/continuite.md`](docs/methode/continuite.md)

11. **Les GPU sont exclusivement réservés à Drave** ; les **professeurs** passent par l'**API
    DeepSeek** (`tools/llm/enseignant.py`), jamais par un serveur local (`llama-server`,
    `ollama`). Garde-fous : `hauru-gpu-guard` (timer 30 s), `porte-ressources` (contrôle GPU).
    → [`docs/methode/ressources.md`](docs/methode/ressources.md)

## 3. Routage : lire le document de sa tâche, pas les autres

| si la tâche est… | lire |
|---|---|
| comprendre la **vision** (les flots, les cinq axes, ce qu'elle n'est pas) | [`docs/theorie/vision.md`](docs/theorie/vision.md) |
| la **roadmap** (A/B/N/R, l'ordre, la file « jamais en attente ») | [`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md) |
| **la lecture rapide** et son backlog (techniques, couches, fiches) | [`docs/theorie/lecture-rapide.md`](docs/theorie/lecture-rapide.md) · [`docs/pilotage/backlog/index.md`](docs/pilotage/backlog/index.md) |
| comprendre la mission et les priorités | [`docs/methode/mission.md`](docs/methode/mission.md) |
| écrire un résultat (fiche, JSON, commit, journal) | [`docs/methode/resultats.md`](docs/methode/resultats.md) |
| ranger un fichier, revue de documentation, synthèse | [`docs/methode/rangement.md`](docs/methode/rangement.md) |
| **charger le contexte** (budget, protocole, ce qu'on ne charge pas) | [`docs/methode/contexte.md`](docs/methode/contexte.md) |
| **cycles DSH, sous-agents, reprise** | [`docs/methode/continuite.md`](docs/methode/continuite.md) |
| **rapporter à l'humain, un round** | [`docs/methode/relations-humaines.md`](docs/methode/relations-humaines.md) |
| **dessiner un schéma**, convertir un diagramme, améliorer une illustration | [`docs/methode/illustrations.md`](docs/methode/illustrations.md) |
| lancer ou lire les portes | [`docs/methode/portes.md`](docs/methode/portes.md) |
| étudier Panini/Nipada, la généalogie | [`docs/methode/panini-nipada.md`](docs/methode/panini-nipada.md) |
| concevoir un test d'entrée/sortie, corriger | [`docs/methode/miroir.md`](docs/methode/miroir.md) |
| planifier une campagne, le matériel, carpe diem | [`docs/methode/ressources.md`](docs/methode/ressources.md) |
| **les jeux symboliques** (surface → RSN-jeu → pensée, 71 langues, maîtres) | [`docs/theorie/jeux-symboliques.md`](docs/theorie/jeux-symboliques.md) |
| **le protocole sémantique** (rejouer, convergence, sens → texte, raisonnement gelé) | [`docs/theorie/protocole-semantique.md`](docs/theorie/protocole-semantique.md) |
| **l'état courant** (synthèse + chantiers + questions) | [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) |
| le **vocabulaire** (couche vs étage, termes du dépôt) | [`docs/theorie/glossaire.md`](docs/theorie/glossaire.md) |
| **trouver un sujet** (un concept, un chantier, une phase) | [`docs/theorie/carte.md`](docs/theorie/carte.md) |
| la carte de la documentation | [`docs/README.md`](docs/README.md) |

> **Chargement facultatif.** Les documents de cette table, `docs/pilotage/en-cours.md`, `docs/pilotage/roadmap.md`, `reports/` et
> `journal/` ne se lisent **que pour la tâche en cours** : le fichier de tâche suffit. Ne pas les
> charger « pour être complet » : c'est du contexte qui coûte et périme.

> **Le contexte est un budget.** Par défaut : `AGENTS.md` + `docs/pilotage/en-cours.md` + **un** document de
> tâche. Le protocole, les budgets et les cas « ne pas charger » sont dans
> [`docs/methode/contexte.md`](docs/methode/contexte.md) ; la vérification est
> `python3 tools/taille_documents.py`.

## 4. Le minimum avant de conclure

- l'état est à jour dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) (synthèse, chantiers, questions en attente) ;
- la **roadmap** est à jour : le chantier fini y est marqué, le suivant est désigné ;
- la fiche est dans `reports/`, le récit dans `journal/`, le commit porte le chiffre ;
- les portes sont vertes, **hors les rouges tolérées listées dans `docs/pilotage/references-non-regression.md`** ;
- la revue de documentation passe, et les liens résolvent.
- le budget de contexte est vérifié : `python3 tools/taille_documents.py`.
- l'état est court et reprenable : `python3 tools/verifie_en_cours.py`.
- journal : dossiers/jour, sessions liées → `tools/verifie_journal.py`.
- les schémas sont des SVG valides et référencés : `python3 tools/verifier_schemas.py`.

</system-reminder>

### 👤 Utilisateur

Current runtime context. This snapshot supersedes earlier runtime-context snapshots.

Current DSH file policy: danger-full-access. The DSH file sandbox does not restrict file modifications by available operations.

Approval prompts are disabled in this session: actions that require approval are rejected automatically — do not request sandbox escalation (do not set `sandbox_permissions`).

### 👤 Utilisateur

<system-reminder>
A skill is a reusable set of task-specific instructions. The following skills are available in this session:

<available_skills>
- `microsoft-foundry`: Deploy, evaluate, fine-tune, and manage Foundry agents end-to-end with azd: hosted agent scaffold/run/deploy, prompt agent create, batch eval, continuous eval, prompt optimizer, Agent Optimizer scaffold, agent.yaml, dataset curation from traces, model fine-tuning (SFT/DPO/RFT). USE FOR: azd ai agent, azd provision/deploy, deploy agent, hosted agent, create agent, add tool to agent, invoke agent, evaluate agent, continuous eval, continuous monitoring, agent CI/CD, optimize prompt, improve prom...
</available_skills>

If the user names a skill, or the task clearly matches a skill's description, call the `skill` tool with the exact skill name before taking task actions. Load all applicable skills, then follow their full instructions. This catalog contains summaries only; do not infer or follow a skill's instructions until it has been loaded.
A user may also invoke a skill directly; its <skill_content> block then appears in this conversation. Follow it, and do not call the `skill` tool again for that skill.
</system-reminder>

- **bash** `{"command": "ls -la && git status --short && git log --oneline -5", "description": "List root and git state"}`

  ```
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138 15 nov 06:29 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   198 15 nov 10:44 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 01:33 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 77956 15 nov 09:50 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run
… [2749 caractères tronqués]
  ```

- **grep** `{"pattern": "§\\s*334|\\b334\\b", "include": "*.md"}`

  ```
Found 250 of 589 matches

reports/rapport-parcimonie-imposee.md
Line 33: | 0,2 % | 334,9 M (−5,1 %) | 19,6502 | 1,02× |

docs/archive/note-corpus-panini.md
Line 28: | wikipedia_fr | 15 636 | 1 334 668 | 8,3 Mo |

reports/README.md
Line 27: | [`note-panini-334.md`](note-panini-334.md) | **Panini** — la note à envoyer : H0 reproduite, β époque non, la collinéarité |
Line 28: | [`rapport-panini-334.md`](rapport-panini-334.md) | **Panini** — le §334 : H0 0,909/0,906, la |

reports/rapport-bilan-semaine.md
Line 46: | **le §334** | leur loi H0 **reproduite** (R² 0,909) ; leur β époque **+0,138 non reproduit** (−0,006) ; le plan est **colinéaire** |
Line 49: | **le protocole à date contrôlée** | 60 paires en 3 strates ; le §334 ne fournit **qu'une** paire contemporaine |
Line 76: | **4A** | la note Panini | ✅ écrite (`note-panini-334.md`), **à envoyer** |
Line 90: 4. **Le corpus à date contrôlée** : de nouvelles données (le §334 ne suffit pas).

reports/rapport-bilan-nuit.md
Line 27: | **le protocole à date contrôlée** | 60 paires en 3 strates ; le §334 ne fournit **qu'une** paire contemporaine mesurée | [`rapport-protocole-date.md`](rapport-protocole-date.md) |
Line 35: - **Le protocole 
… [41101 caractères tronqués]
  ```

- **grep** `{"pattern": "V14"}`

  ```
Found 250 of 434 matches

tools/atomes_prediction.py
Line 6: 44 œuvres du §334 de Panini ont une signature V14 (14 parts, somme 1) calculée

tools/protocole_date.py
Line 8: si Panini fournit les signatures V14 des 26 textes qui n'en ont pas encore.
Line 179:     "extracteur V14, sans mélanger avec les v14_signature du graphe v35 (instrument différent : "
Line 586:             "signatures V14 ? C'est l'avertissement de Panini (β époque +0,138), "
Line 593:             "La signature V14 est une signature de filiation/surface, pas d'époque."
Line 632:             "l'extracteur V14 au cosinus ≥ 0,99 (ou L2 ≤ 0,01) avant tout test.",
Line 906:         resume["message"] = "Aucune paire complète : fournir les signatures V14 des 26 textes à signer."
Line 996:     ap.add_argument("--rejouer", action="store_true", help="rejoue le test avec des signatures V14")

tools/panini_334.py
Line 7: paires finies, 102 sources acquises) et les signatures V14 de 44 œuvres (14 parts
Line 1286:             "formule": "d_sig(L2 V14) ~ 1 + d_topo + Δannée/1000 + même_tradition",

tools/genealogie_deux_faces.py
Line 38: V14 = ["ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET", "TEMPS", "MODALITÉ",
Line 
… [44728 caractères tronqués]
  ```

- **glob** `{"pattern": "**/rapport-protocole-date*"}`

  ```
reports/rapport-protocole-date.md
  ```

- **read** `{"file_path": "reports/rapport-protocole-date.md"}`
- **read** `{"file_path": "docs/methode/panini-nipada.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-protocole-date.md</path>
<type>file</type>
<content>
1: # B1 — le protocole Panini à date contrôlée : 60 paires, trois strates, et les 26 signatures qui manquent
2: 
3: > **Ligne de roadmap** : **R0.7** (le bloc linguistique) / **L** · **Tâche** : **B1**, suite de la
4: > note 4A · **Date** : 2026-11-15 · **HEAD mesuré** : `f926b5bc` · **Verdict** : ✅ **le protocole est
5: > gelé et rejouable ; le §334 seul ne peut pas fournir les 60 paires signées** — 60 paires
6: > (20 contemporaines / 20 même tradition / 20 même langue), **59 textes**, **27 paires déjà signées**
7: > (1 G1, 14 G2, 12 G3), **26 textes à signer** par Panini avec le même extracteur V14. Le test n'est
8: > **pas exécuté** : il attend ces signatures. Le manifeste est
9: > [`protocole-date.json`](protocole-date.json) ; le dispositif est
10: > [`../tools/protocole_date.py`](../tools/protocole_date.py).
11: 
12: **En trois lignes.** (1) La suite de 4A n'est pas « 20 paires contemporaines de traditions
13: différentes » à prendre dans les 44 signatures : le §334 n'en fournit **qu'une** dont les deux
14: signatures soient déjà mesurées (`book_of_enoch` 
… [30297 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/panini-nipada.md</path>
<type>file</type>
<content>
1: # Étudier Panini et Nipada, régulièrement
2: 
3: > Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **à chaque cycle**, avant de conclure sur
4: > la généalogie, les styles ou les familles de langues.
5: 
6: ## Pourquoi
7: 
8: Les projets **`../Panini/`** et **`../Panini-Research/`** poursuivent le **même objectif par une approche
9: complémentaire** : Panini décompose le texte en **14 atomes sémantiques**, Nipada le fait tourner comme un tissu
10: computationnel — *algébrique, là où Drave est statistique*. Ils tiennent le **système linguistique** et généralisent
11: une **généalogie des langues, dialectes et styles**.
12: 
13: ## La règle
14: 
15: À chaque cycle, **lire ce qui a bougé chez eux** (docs, publications, journaux de bord, `git log`) et **confronter
16: leurs résultats aux nôtres**. Ce qui en sort va dans [`docs/theorie/genealogie-des-langues.md`](../theorie/genealogie-des-langues.md)
17: (la théorie) — **jamais les chiffres** (ils vont dans `reports/`).
18: 
19: ## Leur avertissement, à ne pas oublier ✗✓
20: 
21: Leur signatur
… [916 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='reports/protocole-date.json'\nd=json.load(open(p))\nprint(type(d), list(d)[:40])\nfor k,v in d.items():\n    print('KEY',k,type(v), len(v) if hasattr(v,'__len__') else '')\nPY", "description": "Inspect protocole JSON structure"}`

  ```
<class 'dict'> ['tache', 'version', 'titre', 'date', 'commit_drave', 'commit_panini', 'sources', 'protocole', 'pre_enregistrement', 'faisabilite', 'composition', 'paires', 'textes', 'a_signer', 'commande', 'limites']
KEY tache <class 'str'> 2
KEY version <class 'str'> 3
KEY titre <class 'str'> 62
KEY date <class 'str'> 10
KEY commit_drave <class 'str'> 40
KEY commit_panini <class 'dict'> 4
KEY sources <class 'dict'> 7
KEY protocole <class 'dict'> 10
KEY pre_enregistrement <class 'dict'> 9
KEY faisabilite <class 'dict'> 3
KEY composition <class 'dict'> 7
KEY paires <class 'list'> 60
KEY textes <class 'list'> 59
KEY a_signer <class 'list'> 26
KEY commande <class 'str'> 123
KEY limites <class 'list'> 8
  ```

- **bash** `{"command": "sed -n '1,220p' tools/protocole_date.py", "description": "Read protocol tool head"}`

  ```
#!/usr/bin/env python3
"""protocole_date.py — B1 : le protocole Panini à date contrôlée (suite de la note 4A).

Ce script ne modifie jamais Panini. Il lit les artefacts §334 en lecture seule,
vérifie leurs SHA-256, construit le manifeste des **60 paires** en trois groupes
(20 contemporaines de traditions différentes à ±10 ans, 20 de même tradition à
±200 ans, 20 de même langue source à dates décalées), puis peut rejouer le test
si Panini fournit les signatures V14 des 26 textes qui n'en ont pas encore.

Usage :
  python3 tools/protocole_date.py --verifier
  python3 tools/protocole_date.py --construire --sortie reports/protocole-date.json
  python3 tools/protocole_date.py --rejouer --signatures /tmp/v14.json
  python3 tools/protocole_date.py --rejouer --rapide --sortie /tmp/resultats.json

Le manifeste est **gelé** : la sélection ne regarde que les métadonnées (année,
tradition, langue, auteur, titre), jamais les 14 atomes ni les distances
lexicales. Le test se rejoue sur le fichier gelé, jamais en re-sélectionnant.
"""
from __future__ import annotations

import argparse
import collections
import datetime as _dt
import hashlib
import heapq
import itertools
import json
import math
im
… [8707 caractères tronqués]
  ```

- **bash** `{"command": "grep -n '^def \\|^class \\|--rapide\\|controle\\|negative\\|negatif\\|permut\\|rejouer\\|incomplet\\|a_signer' tools/protocole_date.py | head -120", "description": "Outline protocol tool"}`

  ```
7:±200 ans, 20 de même langue source à dates décalées), puis peut rejouer le test
13:  python3 tools/protocole_date.py --rejouer --signatures /tmp/v14.json
14:  python3 tools/protocole_date.py --rejouer --rapide --sortie /tmp/resultats.json
176:    "regroupe par texte (permutation et bootstrap par texte).",
201:def sha256(chemin: pathlib.Path) -> str:
209:def lire_json(chemin: pathlib.Path):
213:def commit_git(chemin: pathlib.Path):
222:def normaliser(texte) -> str:
232:def auteur(v) -> str:
237:def titre(v) -> str:
241:def famille(v):
246:def arrondi(x, n=6):
258:class Corpus:
292:def meme_travail(a, b) -> bool:
300:def auteurs_differents(a, b) -> bool:
304:def candidats(corpus: Corpus, groupe: str):
323:def construire_adjacence(corpus: Corpus):
333:def bfs(adj, source, cibles):
348:def distances_topo(corpus: Corpus, ids):
360:def construire(corpus: Corpus) -> dict:
468:    a_signer = [
557:        "a_signer": a_signer,
559:            "python3 tools/protocole_date.py --rejouer "
568:def _stats(valeurs):
581:def _protocole():
609:            "controle_positif_G1": (
611:                "leur d_sig moyenne à un nul où les étiquettes de famille sont permutées "
620:        "controle
… [3107 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/protocole-date.json'))\nfor k in ['tache','version','titre','date','commit_drave','commit_panini','sources','pre_enregistrement','faisabilite','composition','commande']:\n    print('###',k)\n    print(json.dumps(d[k],ensure_ascii= … [184 caractères tronqués]`

  ```
### tache
"B1"
### version
"1.0"
### titre
"Protocole Panini à date contrôlée — 60 paires en trois groupes"
### date
"2026-11-15"
### commit_drave
"f926b5bc6d8da64ffb1c59a6dbc8a6fcfd1c9888"
### commit_panini
{
 "attendu_4a": "e10d695e65f52031222819cb1bdbb290d08f8e57",
 "lu": "9b80c323629be60c68696f5c5a21f37ad9420073",
 "identique": false,
 "note": "Le HEAD de Panini peut avancer ; les SHA-256 des artefacts §334 sont la référence."
}
### sources
{
 "paires334": {
  "chemin": "Panini/research/nipada/falsification/pairs334_axes_v1.json",
  "sha256": "8de7a6797d5316293bd29c3e5ac070d2ef5582acdeb96b286397237540528777"
 },
 "graphe334": {
  "chemin": "Panini/research/nipada/falsification/nipada_v334_graph_v35.json",
  "sha256": "9ddf050aa1699a3c345c6b9e8ad973b8096d6003219b069dd6a6f51489793cfe"
 },
 "signatures44": {
  "chemin": "Panini/research/nipada/falsification/analytic_sigs_v1.json",
  "sha256": "8aa9c1d50d89e4dc13a8b9bdbf0ae77d4e5a6da4bed00ecd126284f0f7a5519e"
 },
 "revalidation334": {
  "chemin": "Panini/research/nipada/falsification/nipada_v334_revalidation_v35.json",
  "sha256": "b2be71436a017b7881fee7f93d26bedd948a7c342166236c8314d1f278abb546"
 },
 "couverture": {
  "chemin": "P
… [11173 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,collections\nd=json.load(open('reports/protocole-date.json'))\nprint('PAIRE sample:',json.dumps(d['paires'][0],ensure_ascii=False,indent=1))\nprint('TEXTE sample:',json.dumps(d['textes'][0],ensure_ascii=False,indent=1))\n# distribution signatures\nc=collect … [180 caractères tronqués]`

  ```
PAIRE sample: {
 "id": "G1-01",
 "groupe": "G1",
 "a": "baudhayana_dharmasutra",
 "b": "plato_crito",
 "annee_a": -400,
 "annee_b": -399,
 "delta_annee": 1,
 "famille_a": "INDIAN",
 "famille_b": "GRECO",
 "meme_famille": false,
 "langue_a": "san",
 "langue_b": "grc",
 "meme_langue": false,
 "tradition_a": "INDIAN_AXIAL",
 "tradition_b": "GRECO_LATIN_AXIAL",
 "titre_a": "baudhayana dharma sutra",
 "titre_b": "crito",
 "auteur_a": "anonymous",
 "auteur_b": "plato",
 "source_a": "https://www.sacred-texts.com/hin/sbe14/",
 "source_b": "",
 "d_topo": null,
 "signatures_44": 0,
 "etat_signatures": "aucune"
}
TEXTE sample: {
 "id": "2_esdras",
 "annee": 100,
 "langue": "eng",
 "tradition_label": "JUDEAN_APOCALYPTIC_LATE",
 "famille": "ABRAHAMIC",
 "auteur": "anonymous",
 "titre": "2 esdras 4 ezra",
 "source": "https://www.sacred-texts.com/bib/poly/es2.htm",
 "source_ok": true,
 "signature_44": true,
 "signature_graphe": false,
 "usage": 2
}
sig counts Counter({'?': 60})
{'id': 'G1-01', 'groupe': 'G1', 'a': 'baudhayana_dharmasutra', 'b': 'plato_crito', 'annee_a': -400, 'annee_b': -399, 'delta_annee': 1, 'famille_a': 'INDIAN', 'famille_b': 'GRECO', 'meme_famille': False, 'langue_a': 'san', 
… [1506 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nprint(type(d), list(d)[:20] if isinstance(d,dict) else len(d))\nPY\ngrep -n 'W4\\|W3\\|W5\\|panini-manifeste\\|J3 matin' tools/chantier/plan.json | head -40", "description": "Locate W4 in plan"}`

  ```
<class 'dict'> ['nom', 'principe', 'taches']
621:   "id": "W3",
624:   "mandat": "Tâche W3 (J2 après-midi) : la matrice du tagger — **défaut** (sans clé, hors ligne, code 0), **avec clé**, **clé invalide**, **réseau coupé**, le coût pour 1 000 phrases, le repli ; la recommandation (défaut hors ligne, `--tagger` opt-in, un mode `auto` seulement si la clé existe et sans changer le code de sortie). Fiche `reports/rapport-tagger-defaut.md` + JSON, avec un test par cas dans `tools/tests/test_tagger_api.py`.",
638:   "id": "W4",
641:   "mandat": "Tâche W4 (J3 matin, la part du pilote) : le manifeste à envoyer à Panini — les **26 signatures manquantes** (la liste des œuvres du §334 sans signature V14), la commande exacte qu'ils doivent lancer, le format attendu ; et le **rejeu des 60 paires** du protocole (`rapport-protocole-date.md`) sur ce qui est disponible, avec le contrôle négatif. Fiche `reports/rapport-panini-manifeste.md` + JSON. **Ne modifie rien chez Panini.**",
645:     "commande": "test -f reports/rapport-panini-manifeste.md && echo FICHE-OK",
651:   "id": "W5",
654:   "mandat": "Tâche W5 (J3 après-midi) : la restitution v3 — `_role_gp` distingue **lieu / temps / destinataire 
… [834 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' docs/pilotage/semaine-2.md", "description": "Read week 2 plan"}`

  ```
# La semaine 2 — cinq jours, deux vagues, quatre chantiers et une décision

> **Ce que ce document est.** Le plan du **16 au 22 novembre 2026** : ce qui se fait, dans quel
> ordre, avec quelles dépendances, quels contrôles et quels livrables. Il **succède** à
> [`semaine-autonome.md`](semaine-autonome.md), qui reste l'**archive** de la semaine 1 et n'est
> **pas modifié**. L'état courant est dans [`en-cours.md`](en-cours.md) ; les chiffres sont dans
> les fiches citées, jamais recopiés ici.
>
> **Sources.** Le [bilan de la semaine](../../reports/rapport-bilan-semaine.md) et les fiches des
> tâches C/B/D/E : [C1](../../reports/rapport-coordination-n2-v2.md), [C2](../../reports/rapport-coordination-s-v2.md),
> [C3](../../reports/rapport-gold-reel-50.md), [B1](../../reports/rapport-protocole-date.md),
> [B2](../../reports/rapport-atomes-prediction.md), [B3](../../reports/rapport-cic-v2.md),
> [D1](../../reports/rapport-exemples-tagger.md), [D2](../../reports/rapport-restitution-v2.md),
> [D3](../../reports/rapport-faq.md), [E1](../../reports/rapport-faq-sommaire.md),
> [E2](../../reports/rapport-tagger-erreurs.md). Le plan ne promet aucun chiffre : il nomme la
> mesure, son **contrôle
… [10691 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '740,1000p' tools/protocole_date.py", "description": "Read replay implementation"}`

  ```
erreurs.append(f"{p['id']} : paire dupliquée {cle}")
        vus.add(cle)
        textes.add(a); textes.add(b)
    if len(textes) != manifeste["composition"]["textes_distincts"]:
        erreurs.append("textes_distincts incohérent")
    if manifeste["composition"]["paires_distinctes"] != len(vus):
        erreurs.append("paires_distinctes incohérent")
    if not silencieux:
        if erreurs:
            print("ÉCHEC : " + str(len(erreurs)) + " erreur(s)")
            for e in erreurs:
                print(" -", e)
        else:
            print(f"OK : 60 paires uniques, 20/20/20, {len(textes)} textes, sources acquises.")
    return erreurs


def verifier_hashes(manifeste: dict):
    """Refuse de rejouer sur des artefacts qui ne sont plus ceux du manifeste gelé."""
    carte = {
        "paires334": PAIRES_334, "graphe334": GRAPHE, "signatures44": SIGNATURES_44,
        "revalidation334": REVALIDATION, "couverture": COUVERTURE,
        "manifeste_sources": MANIFESTE_SOURCES, "v150": V150,
    }
    erreurs = []
    for nom, info in manifeste.get("sources", {}).items():
        chemin = carte.get(nom) or (RACINE.parent / info["chemin"])
        if not chemin.exists():
           
… [9780 caractères tronqués]
  ```

- **bash** `{"command": "ls reports | grep -i 'panini\\|manifeste\\|protocole'; echo ---; ls tools | grep -i 'panini\\|manifeste\\|protocole'; echo ---; git log --oneline --all -- reports/rapport-panini-manifeste.md | head; echo ---; grep -rn 'rapport-panini-manifeste' --include='*.md' --include='*.json' --incl … [76 caractères tronqués]`

  ```
note-panini-334.md
panini-334.json
pensee-inventaire-panini.json
protocole-date.json
rapport-inventaire-panini.md
rapport-panini-334.md
rapport-protocole-date.md
---
manifeste_modeles_lourds.json
panini_334.py
protocole_date.py
---
---
./tools/chantier/plan.json:641:   "mandat": "Tâche W4 (J3 matin, la part du pilote) : le manifeste à envoyer à Panini — les **26 signatures manquantes** (la liste des œuvres du §334 sans signature V14), la commande exacte qu'ils doivent lancer, le format attendu ; et le **rejeu des 60 paires** du protocole (`rapport-protocole-date.md`) sur ce qui est disponible, avec le contrôle négatif. Fiche `reports/rapport-panini-manifeste.md` + JSON. **Ne modifie rien chez Panini.**",
./tools/chantier/plan.json:645:     "commande": "test -f reports/rapport-panini-manifeste.md && echo FICHE-OK",
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,collections\ns=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))\nprint(type(s), len(s)); print(list(s)[:10])\nk=list(s)[0]; print(k, type(s[k]), s[k] if not isinstance(s[k],dict) else list(s[k])[:20])\nPY\nls -la ../Panini/re … [188 caractères tronqués]`

  ```
<class 'dict'> 44
['2_esdras', 'aristotle_categories', 'aristotle_de_caelo', 'aristotle_nicomachean_ethics', 'aristotle_parts_of_animals', 'aristotle_posterior_analytics', 'aristotle_prior_analytics', 'bengio_2003', 'book_of_enoch', 'curry_1930']
2_esdras <class 'dict'> ['ÊTRE', 'DIFFÉRENCE', 'RAPPORT', 'ORIENTATION', 'SUJET', 'TEMPS', 'MODALITÉ', 'NOMBRE', 'ESPACE', 'OPÉRATION', 'FONCTION', 'STRUCTURE', 'SYMÉTRIE', 'ÉQUATION']
total 212144
drwxr-xr-x. 1 stephane stephane   21326 18 oct 10:03 .
drwxr-xr-x. 1 stephane stephane     650  4 jun 11:29 ..
-rw-r--r--. 1 stephane stephane   22381 18 oct 10:03 analytic_sigs_v1.json
-rw-r--r--. 1 stephane stephane    7048 18 oct 10:03 axeA_p1_subset_v1.json
-rw-r--r--. 1 stephane stephane    1644 18 oct 10:03 benchmark_generatif_analytique_v1.json
-rw-r--r--. 1 stephane stephane    4228 18 oct 10:03 benchmark_generatif_clean_v1.json
-rw-r--r--. 1 stephane stephane    9358  8 sep 15:34 benchmark_generatif_contenu_v1.json
-rw-r--r--. 1 stephane stephane    6059 18 oct 10:03 benchmark_generatif_corpus_v1.json
-rw-r--r--. 1 stephane stephane    2200 18 oct 10:03 benchmark_generatif_v1.json
-rw-r--r--. 1 stephane stephane   25410 30 avr  2026 cir
… [1884 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/protocole-date.json'))\nfor p in d['paires']:\n    print(p['id'],p['groupe'],p['a'],p['b'],'sig',p['signatures_44'],p['etat_signatures'],'dt',p['d_topo'])\nPY", "description": "List pairs and signature status"}`

  ```
G1-01 G1 baudhayana_dharmasutra plato_crito sig 0 aucune dt None
G1-02 G1 vasistha_dharmasutra plato_euthyphro_jowett sig 0 aucune dt None
G1-03 G1 hiranyakesi_grhya_sutra plato_charmides sig 1 une dt None
G1-04 G1 paraskara_grhya_sutra plato_crito sig 0 aucune dt None
G1-05 G1 apastamba_grhya_sutra plato_euthyphro_jowett sig 0 aucune dt None
G1-06 G1 sankhayana_grhya_sutra plato_charmides sig 1 une dt None
G1-07 G1 daodejing plato_laws sig 1 une dt None
G1-08 G1 daodejing plato_sophist sig 1 une dt None
G1-09 G1 qiwulun epicurus_letters sig 1 une dt None
G1-10 G1 mengzi epicurus_letters sig 1 une dt None
G1-11 G1 mandukya_upanishad qiwulun sig 1 une dt None
G1-12 G1 mandukya_upanishad mengzi sig 1 une dt None
G1-13 G1 mandukya_upanishad xiaojing sig 0 aucune dt None
G1-14 G1 burnet_early_greek_philosophy curry_1930 sig 1 une dt None
G1-15 G1 miller_1956 zadeh_1965 sig 0 aucune dt None
G1-16 G1 ingersoll_works russell_parousia_1878 sig 1 une dt None
G1-17 G1 chandogya_upanishad isaiah_book sig 1 une dt None
G1-18 G1 brihadaranyaka_upanishad isaiah_book sig 1 une dt None
G1-19 G1 book_of_enoch yueji sig 1 une dt None
G1-20 G1 book_of_enoch sibylline_oracles sig 2 deux dt 1
G2-01 G2 
… [2371 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && grep -rln 'analytic_sigs_v1\\|analytic_sigs\\|V14_ATOMS\\|compute_signature\\|signature' --include='*.py' research/src research/tools research/scripts 2>/dev/null | head -50", "description": "Find V14 extractor scripts"}`

  ```
research/src/cloud/integration_manager.py
research/src/analyzers/gutenberg_dhatu_analyzer.py
research/src/dashboards/tripartite_ultimate_dashboard.py
research/src/documentation/complete_tripartite_guide.py
research/src/reports/tripartite_final_accomplishments.py
research/src/visualization/dhatu_cycle_diagrams.py
research/src/fpga/interface.py
research/src/nipada/ai/__init__.py
research/src/nipada/ai/agent_tools.py
research/src/nipada/ai/llm_plugin.py
research/src/nipada/ai/rag.py
research/src/nipada/api/api.py
research/src/nipada/api/cli.py
research/src/nipada/api/nipada_cli.py
research/src/nipada/api/server.py
research/src/nipada/compiler/__init__.py
research/src/nipada/compiler/benchmark.py
research/src/nipada/compute/ambiguity_backlog.py
research/src/nipada/compute/api.py
research/src/nipada/compute/author_metadata_ingestion.py
research/src/nipada/compute/calibration_cross_lingual.py
research/src/nipada/compute/cross_lingual_projector.py
research/src/nipada/compute/dhatu_token_program.py
research/src/nipada/compute/dialect_cognitive_profiler.py
research/src/nipada/compute/dpl3_solver.py
research/src/nipada/compute/dtp_sat_bridge.py
research/src/nipada/compute/dynamic_ingestion.p
… [1163 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && find research -iname '*signat*' -o -iname '*v14*' | head -60; echo ---; find research -iname '*extract*' | head -40", "description": "Find V14-related files"}`

  ```
research/archives/filesystem_archive/cleanup/backup_20250906_143516/publications/leanpub/manuscript_fr/ch12-meme-signature-baby-sign-iteration-output-sequence.md
research/archives/filesystem_archive/cleanup/backup_20250906_143516/publications/leanpub/manuscript_fr/ch22-meme-signature-semantique.md
research/archives/filesystem_archive/cleanup/backup_20250906_154458/OPERATIONS/DevOps/PaniniFS.Net/packages/DokanNet.1.3.0/.signature.p7s
research/archives/filesystem_archive/cleanup/backup_20250906_154458/OPERATIONS/DevOps/PaniniFS.Net/packages/SQLite.3.13.0/.signature.p7s
research/archives/filesystem_archive/cleanup/backup_20250906_154458/OPERATIONS/DevOps/PaniniFS.Net/packages/log4net.2.0.8/.signature.p7s
research/archives/pre_v14_unification_20260521
research/archives/scripts_v2/nipada_add_v14_atoms_v385a.py
research/archives/scripts_v2/nipada_s423_v14_signatures.py
research/archives/scripts_v2/nipada_s462_morpho_v14_delta.py
research/archives/scripts_v2/nipada_s483_parallel_concept_v14.py
research/archives/scripts_v2/nipada_v14_semantic_analyzer.py
research/data/parallel_pipeline/v14-0.pid
research/data/parallel_pipeline/v14-1.pid
research/data/parallel_pipeline/v14-2.pid
research/da
… [5425 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && grep -rln 'analytic_sigs_v1' . 2>/dev/null | head -30", "description": "Find references to signature artifact"}`

  ```
[still running after 60000ms; moved to background job bash-15]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_kill** `{"job_id": "bash-15", "reason": "Grep too broad; targeted search instead"}`

  ```
requested cancellation of job bash-15
  ```

- **bash** `{"command": "cd ../Panini && ls research/archives/scripts_v2 | grep -i 'v14\\|signature\\|analytic' && echo --- && sed -n '1,120p' research/archives/scripts_v2/nipada_s423_v14_signatures.py && echo ===ANALYZER=== && sed -n '1,160p' research/archives/scripts_v2/nipada_v14_semantic_analyzer.py", "desc … [42 caractères tronqués]`

  ```
nipada_add_v14_atoms_v385a.py
nipada_s423_v14_signatures.py
nipada_s462_morpho_v14_delta.py
nipada_s483_parallel_concept_v14.py
nipada_v14_semantic_analyzer.py
---
#!/usr/bin/env python3
"""§423 — Signatures V14 pour les 20 concepts §422B (African/Sufi/Kabbalah/Confucian).

Pattern identique aux scripts wave : vecteurs V14 construits par analyse sémantique
de chaque concept selon les 14 atomes universels.
"""
import json
import sys
from pathlib import Path

GRAPH_PATH = Path("nipada/encyclopedia/v2/ontowave_graph.json")
VALID_V14 = {
    "ÊTRE", "DIFFÉRENCE", "RAPPORT", "ORIENTATION", "SUJET",
    "TEMPS", "MODALITÉ", "NOMBRE", "ESPACE", "OPÉRATION",
    "FONCTION", "STRUCTURE", "SYMÉTRIE", "ÉQUATION",
}

# ── Vecteurs V14 pour les 20 concepts §422B ──────────────────────────────────
# Chaque vecteur est normalisé (somme ≤ 1.0), les atomes absents = 0.0
# Justification ci-dessous pour chaque concept.

V14_VECTORS = {

    # ── TRADITION AFRICAN_AXIAL ─────────────────────────────────────────────

    "UBUNTU": {
        # "Je suis parce que nous sommes" — ontologie relationnelle communautaire
        # ÊTRE (identité ontologique), RAPPORT (relation Je-Nous), SUJET (personne),
     
… [10570 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && grep -rln 'analytic_sigs_v1' research --include='*.py' --include='*.md' --include='*.json' 2>/dev/null | head -30", "description": "Targeted search for signature artifact"}`

  ```
[still running after 60000ms; moved to background job bash-17]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "cd ../Panini && ls research/nipada | head -40; echo ---; ls research/src/nipada | head -40; echo ---; find research/src/nipada -maxdepth 2 -iname '*analytic*' -o -iname '*signature*' | head -30", "description": "List Nipada modules"}`

  ```
api
closure
corpus
encyclopedia
falsification
fpga
modal
molecules
NAC_ROADMAP_v1.0.md
NIPADA_SEMANTIC_PIPELINE.md
ONTOWAVE_DESIGN_v1.0.md
originals_cache
publication
PUBLICATION_PLAN_v1.0.md
RAPPORT_FALSIFICATION_NIPADA_v1.0.md
schema
scripts
semantic
src
SYNTHESE_v0.2.0.md
SYNTHESE_v0.3.0.md
SYNTHESE_v0.4.0-alpha.md
taxonomies
v7
validation_repo
---
ai
api
benchmark.py
client.py
compiler
compute
container
core
daemon
data
encyclopedia
formalkernel
fpga_pcie_driver.py
fpga_worker.py
ingestion
__init__.py
kernel.py
molecule_factory.py
native
profiles
__pycache__
reconstruction
search
sense_encoder.py
signing
---
research/src/nipada/signing/analytical_projection.py
  ```

- **job_kill** `{"job_id": "bash-17", "reason": "Targeted search instead"}`

  ```
requested cancellation of job bash-17
  ```

- **bash** `{"command": "cd ../Panini && git log --oneline --follow -- research/nipada/falsification/analytic_sigs_v1.json | head -10; echo ---; git log --all --oneline --grep='analytic_sigs' | head -20; echo ---; git log --all --oneline --grep='V14' | head -30", "description": "Trace signature artifact history … [2 caractères tronqués]`

  ```
---
---
95ffa228 docs(vision): propager la définition théorique du noyau (15 fichiers) — fin des copies teintées d'implémentation
afb93f3b docs: journaux de bord §260-§271 + prologue pré-NIPADa
b9c50623 §269: add multilingual phraseme/MWE layer to freq_signature
81aa17c0 §266 scripts : patch v16p→v18p (3 filières) + revalidation
42dd3fba §265 scripts + backlog §237-§244 (scripts accumulés non commités)
437c6606 §212-prop: V14 propagation 2-hop (254 propagés / 1473 inatteignables) + journal 2026-05-01
0db393f4 NIPADA v0.4.0-α §207-§209: pipeline ingestion + signed batch + V_OPT v2 revalidation
900d9942 nipada §182 — limite NW×NW est STRUCTURELLE, pas statistique
bf34cf62 nipada §181 — V14 révélé comme filtre, pas bottleneck
d0ebfa3b nipada §180 — synthèse v0.2.0 (clôture sprint)
16d4d43a nipada §179 — densification intra-orientale (échec diagnostique)
be8365c4 nipāda §163-§165 — Phase E démarrée : scaffold + 2 œuvres acquises
cbc61cd8 feat(nipada): §151-§155 Phase C+D — embeddings denses + bigrammes atomiques
1417d557 feat(nipada): scripts §147-§150 + journal Phase B² composite
a5f10564 feat(nipada): scripts §144-§146 + journal Phase B (falsification V14 binaire)
47c0b483 feat(nipad
… [146 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && sed -n '1,200p' research/src/nipada/signing/analytical_projection.py; echo ---; ls -la research/src/nipada/signing", "description": "Inspect analytical projection module"}`

  ```
#!/usr/bin/env python3
"""Projection analytique dynamique (doctrine 2026-09-08).

La signature 14-dim issue du chemin lexical actuel sature (phrases distinctes →
signatures identiques) faute de couverture. Cette projection est ANALYTIQUE et
DÉTERMINISTE : chaque token de contenu est projeté via la chaîne
  WordNet → supersense → sous-atomes E-V14 (§826) → atomes V14 (collapse_to_atoms),
c'est-à-dire par la structure sémantique du mot (modèle), PAS par co-occurrence,
PAS de statistique, PAS de lexique du texte. La somme est normalisée (moyenne).

Usage : sign_analytic(text) -> dict V14 (somme 1).
"""
from __future__ import annotations
import numpy as np

V14 = ["ÊTRE","DIFFÉRENCE","RAPPORT","ORIENTATION","SUJET","TEMPS","MODALITÉ",
       "NOMBRE","ESPACE","OPÉRATION","FONCTION","STRUCTURE","SYMÉTRIE","ÉQUATION"]
# POS Penn Treebank → POS WordNet (n/v/a/r)
_WN = {"NN": "n", "NNS": "n", "NNP": "n", "NNPS": "n", "VB": "v", "VBD": "v",
       "VBG": "v", "VBN": "v", "VBP": "v", "VBZ": "v", "JJ": "a", "JJR": "a",
       "JJS": "a", "RB": "r", "RBR": "r", "RBS": "r"}

_pipe_cache = {}


def _pipeline():
    if "p" not in _pipe_cache:
        from .pipeline import SigningPipeline
        
… [7561 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && find research/nipada/corpus/_cache -maxdepth 2 -type d | head -20; echo ---; ls research/nipada/corpus/_cache | head -30; echo ---; python3 - <<'PY'\nimport json,os\nfor p in ['research/nipada/corpus/_cache/sources_manifest.json','research/nipada/corpus/_cache/sources_co … [170 caractères tronqués]`

  ```
research/nipada/corpus/_cache
research/nipada/corpus/_cache/sci
research/nipada/corpus/_cache/sources
research/nipada/corpus/_cache/gutenberg_curated
research/nipada/corpus/_cache/public_domain_auto
research/nipada/corpus/_cache/public_domain_auto/gutendex
research/nipada/corpus/_cache/references_v272
research/nipada/corpus/_cache/sacred_texts
research/nipada/corpus/_cache/suttacentral
research/nipada/corpus/_cache/suttacentral/leaves
research/nipada/corpus/_cache/wikipedia_dump
research/nipada/corpus/_cache/wikipedia_feed
---
dhammapada_muller_en_pg2017.txt
feuerbach_essence_en_pg69432.txt
gutenberg_curated
hobbes_leviathan_en_pg3207.txt
holbach_system_nature_en_pg8909.txt
hume_dialogues_en_pg4583.txt
manifest_de_wikisource.txt
manifest_en_pg61.txt
missing48.json
mit_aristotle_categories_idx.txt
mit_aristotle_categories_s001.txt
mit_aristotle_categories_s002.txt
mit_aristotle_categories_s003.txt
mit_aristotle_de_anima_idx.txt
mit_aristotle_de_anima_s001.txt
mit_aristotle_de_anima_s002.txt
mit_aristotle_de_anima_s003.txt
mit_aristotle_de_caelo_idx.txt
mit_aristotle_de_caelo_s001.txt
mit_aristotle_de_caelo_s002.txt
mit_aristotle_de_caelo_s003.txt
mit_aristotle_de_caelo_s004.txt
mit_
… [651 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && git ls-files --error-unmatch research/nipada/falsification/analytic_sigs_v1.json 2>&1 | head; git status --short -- research/nipada/falsification/analytic_sigs_v1.json; echo ---; ls research/nipada/scripts | head -60; echo ---; find research/nipada/falsification -maxdept … [92 caractères tronqués]`

  ```
error: pathspec 'research/nipada/falsification/analytic_sigs_v1.json' did not match any file(s) known to git
Did you forget to 'git add'?
---
nipada_autonomous_optimizer.py
nipada_s482b_corpus_encyclopedia_linking.py
nipada_s482c_corpus_primary_sources.py
nipada_s482_corpus_encyclopedia_integration.py
nipada_s484_lexical_ingestion.py
nipada_s485_merge_lexicon_graph.py
nipada_s486_web_interface.py
nipada_s487_lemmatization.py
nipada_s488_etymology.py
__pycache__
wiki_autopilot_ctl_v368.sh
---
analytic_sigs_v1.json
axeA_p1_subset_v1.json
benchmark_generatif_analytique_v1.json
benchmark_generatif_clean_v1.json
benchmark_generatif_contenu_v1.json
benchmark_generatif_corpus_v1.json
benchmark_generatif_v1.json
circular_translation_test.json
container_profiles_v1.json
context_q1_embedding.json
context_q1_normalized.json
context_q1_translation_drift.json
context_q3_channel_stability.json
corpus_dor_cic_v1.json
corpus_dor_cic_v1.tsv
exploit_corpus_v1.json
exploit_corpus_v2.json
frontiere_promotion_corpus.json
h0prime_56H_holdout_validation_v1.json
h0prime_analytic_oos_v2.json
H2_v3_phrases_definitionnelles.json
H3_v3_calibration_phrases.json
LISTE_ACQUISITION_272.md
loi_analytique_cv_v1.jso
… [1657 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && grep -rn 'analytic_sigs' research --include='*.py' --include='*.md' --include='*.sh' --include='*.json' 2>/dev/null | head -20", "description": "Search analytics artifact references"}`

  ```
research/scripts/loi_analytique.py:21:CACHE = OUT / "analytic_sigs_v1.json"
  ```

- **bash** `{"command": "cd ../Panini && grep -rn 'sign_analytic\\|analytical_projection' research --include='*.py' 2>/dev/null | head -20", "description": "Find sign_analytic usage"}`

  ```
research/scripts/benchmark_generatif.py:26:    from nipada.signing.analytical_projection import sign_analytic, cosine, enrich_decoder_analytic
research/scripts/benchmark_generatif.py:32:        target = sign_analytic(t)
research/scripts/benchmark_generatif.py:36:        cos = cosine(target, sign_analytic(str(o1))) if str(o1) not in ("", "(empty)") else 0.0
research/scripts/loi_analytique.py:2:"""Loi H₀′ avec la projection ANALYTIQUE (sign_analytic) — round 18.
research/scripts/loi_analytique.py:30:        from nipada.signing.analytical_projection import sign_analytic
research/scripts/loi_analytique.py:31:        return (nid, sign_analytic(" ".join(words[:W])))
research/src/nipada/signing/analytical_projection.py:11:Usage : sign_analytic(text) -> dict V14 (somme 1).
research/src/nipada/signing/analytical_projection.py:33:def sign_analytic(text: str, lang: str = "eng") -> dict[str, float]:
research/src/nipada/formalkernel/exploit_grammar.py:78:    from nipada.signing.analytical_projection import sign_analytic
research/src/nipada/formalkernel/exploit_grammar.py:79:    sig = sign_analytic(text)
research/tests/signing/test_analytical_projection.py:8:from nipada.signing.analytical_projec
… [273 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && sed -n '1,220p' research/scripts/loi_analytique.py", "description": "Read signature generator script"}`

  ```
#!/usr/bin/env python3
"""Loi H₀′ avec la projection ANALYTIQUE (sign_analytic) — round 18.

Même protocole que la re-fondation (paires §334 officielles couvertes par les textes
ré-acquis, split hors hold-out v1), mais d_lex calculé sur les signatures analytiques
dynamiques (WordNet→supersense→E-V14→V14), au lieu du signeur lexical saturant.
Usage : PYTHONPATH=src python3 scripts/loi_analytique.py
"""
from __future__ import annotations
import json
from multiprocessing import Pool
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "nipada" / "corpus" / "_cache" / "sources"
OUT = ROOT / "nipada" / "falsification"
W = 10000
V14 = ["ÊTRE","DIFFÉRENCE","RAPPORT","ORIENTATION","SUJET","TEMPS","MODALITÉ",
       "NOMBRE","ESPACE","OPÉRATION","FONCTION","STRUCTURE","SYMÉTRIE","ÉQUATION"]
CACHE = OUT / "analytic_sigs_v1.json"


def sign_one(nid):
    p = SRC / f"{nid}.txt"
    if not p.exists(): return (nid, None)
    words = p.read_text(encoding="utf-8").split()
    if len(words) < 300: return (nid, None)
    try:
        from nipada.signing.analytical_projection import sign_analytic
        return (nid, sign_analytic(" ".join(words[:W])
… [1705 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini && ls research/scripts | head -60; echo ---; grep -rln 'upanishad\\|dharmasutra\\|sacred-texts\\|sources_manifest' research/scripts research/nipada/scripts 2>/dev/null | head -30", "description": "Find corpus-to-signature pipeline"}`

  ```
apply_s467ui_patch.py
archive_org_enhanced_extractor.py
archive_org_extractor_v3.py
arreter_tout.py
automation_engine.py
bench_56dim_fixed.py
bench_56dim_reconstruct.py
bench_enriched_final.py
bench_hybrid_fast.py
bench_hybrid_reconstruct.py
bench_hybrid_v2.py
bench_jit_reconstruct.py
benchmark_generatif.py
bench_wordgraph_reconstruct.py
build_explained_page.py
build_multilingual_lexicons.py
build_mwe_pipeline.py
build_wordgraph_matrix.py
build_wordgraphs.py
cic_checker.cpp
colab_manager.py
collector_loop.sh
configure_project_columns.sh
constrained_reconstructor.py
construction_goldberg.py
create_dhatu_projects.sh
create_github_projects.py
create_project_issues.sh
create_projects_api.sh
create_projects_gh.sh
deep_crawl_worker.py
demo_communication.py
demo_udhr.py
demo_workflow_colab_pro.py
dhatu_projects_summary.sh
diagnostic_noyau
download_gutenberg_massive.py
enrich_anticircular_bilingual.py
enrich_bilingual_dicts.py
enrich_cognates.py
enrich_multilingual.py
enrich_pipeline_6layers.py
expand_udhr_lexicon.py
exploit_corpus.py
fast_corpus_collector.py
fetch_arxiv_technique.py
fetch_missing_334.py
fetch_sources_334.py
fetch_stage3.py
fix_git_credentials.py
framenet_integration.py
fr
… [1645 caractères tronqués]
  ```

- **read** `{"file_path": "docs/methode/resultats.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/resultats.md</path>
<type>file</type>
<content>
1: # Ce qu'un résultat doit porter
2: 
3: > Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant d'écrire une fiche**, un JSON de
4: > résultats, ou un message de commit.
5: 
6: ## Les cinq pièces d'un résultat
7: 
8: 1. **Le chiffre** — la valeur, avec son [unité](../theorie/glossaire/entrees/unite.md) et son arrondi utile (jamais plus de chiffres que l'instrument n'en
9:    [porte](../theorie/glossaire/entrees/porte.md)) ;
10: 2. **La mesure qui le produit** — le calcul exact, la métrique ([chrF](../theorie/glossaire/entrees/chrf.md), précision, rappel, [AUC](../theorie/glossaire/entrees/auc.md)…), et ce qu'elle ne
11:    mesure pas ;
12: 3. **Le dispositif** — quel [corpus](../theorie/glossaire/entrees/corpus.md) (et sa provenance), quel modèle (taille, [quantification](../theorie/glossaire/entrees/quantification.md), date de coupure),
13:    quelles **couches de neurones** sondées, quel découpage, **quelle unité de mesure** (unité de sens ou unité
14:    grammaticale ; si c'est un [jeton](../theorie/glossaire/entrees/jeton.md), le dire co
… [2865 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/README.md; echo ===; sed -n '1,60p' reports/INDEX.md; echo ===; grep -n 'rapport-protocole-date\\|rapport-panini-334\\|panini' reports/README.md reports/INDEX.md | head -30", "description": "Read reports index conventions"}`

  ```
# Les rapports — données intermédiaires et références

> **Ce dossier porte les résultats et les données de nos travaux**, jamais la documentation de référence
> (elle est dans [`docs/`](../docs/)). Les fiches courantes sont citées depuis le tableau de bord
> [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md).

> **Navigation** : [la carte des sujets](../docs/theorie/carte.md) · [l'état du moment](../docs/pilotage/en-cours.md) ·
> [l'inventaire des docs](../docs/README.md) · [le journal](../journal/README.md).
>
> **Contexte** : la fiche [`07-mesures-couche-commune.md`](07-mesures-couche-commune.md) est un **hub** de
> **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par
> partie**, jamais en entier ; l'index exhaustif des fiches est [`INDEX.md`](INDEX.md).

## Les fiches courantes

| fichier | ce qu'il porte |
|---|---|
| [`rapport-bilan-semaine.md`](rapport-bilan-semaine.md) | **Bilan** — la semaine 07 → 15/11 : le produit, Panini, la coordination, le harnais |
| [`rapport-bilan-nuit.md`](rapport-bilan-nuit.md) | **Bilan** — la nuit du 14 au 15/11 : le tagger, la base honnête, la phase C/B |
| [`rapport-gold-reel-50.md`](r
… [19518 caractères tronqués]
  ```

- **bash** `{"command": "ls tools | grep -i 'revue\\|journal\\|schema\\|taille\\|verifie'; echo ---; sed -n '1,160p' tools/revue_documentation.py", "description": "Inspect documentation review"}`

  ```
journal_auto.py
mesurer_schema_v2_doc.py
revue_documentation.py
schemas
taille_documents.py
verifie_backlog.py
verifie_contamination.py
verifie_en_cours.py
verifie_etat_a_jour.py
verifie_journal.py
verifier_bilan.py
verifier_chaine_etat.py
verifier_faq.py
verifier_formats.py
verifier_liens_faq.py
verifier_liens.py
verifier_parite_native.py
verifier_schema_produit.py
verifier_schemas.py
verifier_table_types.sh
verifier_v41_engram.py
verifier_v41_mhc.py
---
#!/usr/bin/env python3
"""revue_documentation.py — LA REVUE DE FIN DE SOUS-CHANTIER (AGENTS.md §4).

Ce qu'elle vérifie, et qu'il faut corriger AVANT le commit de clôture :
  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
  2. structure  : les sept chantiers de en-cours.md ont leur entrée, leur état et leur fiche ;
  3. annotation : les liens relatifs des docs/ et reports/ résolvent, et leur libellé ne
     ment pas sur la cible ; les sources externes sont citées ;
  4. fraîcheur  : en-cours.md date du dernier commit, ET aucun fait n'a été commité après
     le dernier état (comparaison de commits, pas de dates : voir verifie_etat_a_jour.py) ;
  5. cohérence  : la synthèse (index.md) liste 
… [4957 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nfor t in d['taches']:\n    if t.get('id') in ('W3','W4','W5'):\n        print(json.dumps(t,ensure_ascii=False,indent=1))\nPY", "description": "Read W4 plan entry"}`

  ```
{
 "id": "W3",
 "jour": 17,
 "titre": "J2 — la décision du tagger par défaut",
 "mandat": "Tâche W3 (J2 après-midi) : la matrice du tagger — **défaut** (sans clé, hors ligne, code 0), **avec clé**, **clé invalide**, **réseau coupé**, le coût pour 1 000 phrases, le repli ; la recommandation (défaut hors ligne, `--tagger` opt-in, un mode `auto` seulement si la clé existe et sans changer le code de sortie). Fiche `reports/rapport-tagger-defaut.md` + JSON, avec un test par cas dans `tools/tests/test_tagger_api.py`.",
 "budget_min": 90,
 "acceptation": [
  {
   "commande": "test -f reports/rapport-tagger-defaut.md && echo FICHE-OK",
   "attendu": "FICHE-OK"
  },
  {
   "commande": "python3 tools/tests/test_tagger_api.py 2>&1 | tail -1",
   "attendu": "OK"
  }
 ]
}
{
 "id": "W4",
 "jour": 17,
 "titre": "J3 — Panini : le manifeste et le rejeu",
 "mandat": "Tâche W4 (J3 matin, la part du pilote) : le manifeste à envoyer à Panini — les **26 signatures manquantes** (la liste des œuvres du §334 sans signature V14), la commande exacte qu'ils doivent lancer, le format attendu ; et le **rejeu des 60 paires** du protocole (`rapport-protocole-date.md`) sur ce qui est disponible, avec le contrôle n
… [992 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib, hashlib, collections\nm=json.load(open('reports/protocole-date.json'))\nsigs=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))\ng=json.load(open('../Panini/research/nipada/falsification/nipada_v334_graph_v35.json'))\ … [753 caractères tronqués]`

  ```
graph keys ['version', 'section', 'iso_from_v34', 'nodes', 'edges']
key nodes len 1753 sample ['epicurus_letters', 'lucretius_drn', 'sextus_pyrrho']
---
version <class 'str'> 3
section <class 'str'> 4
iso_from_v34 <class 'list'> 2
nodes <class 'dict'> 1753
edges <class 'list'> 19967
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib, collections\nm=json.load(open('reports/protocole-date.json'))\nsigs=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))\nd={t['id']:t for t in m['textes']}\npairs=m['paires']\ncomplete=[]; missing=[]\nfor p in pairs:\n … [565 caractères tronqués]`

  ```
complete 27 Counter({'G2': 14, 'G3': 12, 'G1': 1})
missing 33 Counter({'G1': 19, 'G3': 8, 'G2': 6})
missing ids ['G1-01', 'G1-02', 'G1-03', 'G1-04', 'G1-05', 'G1-06', 'G1-07', 'G1-08', 'G1-09', 'G1-10', 'G1-11', 'G1-12', 'G1-13', 'G1-14', 'G1-15', 'G1-16', 'G1-17', 'G1-18', 'G1-19', 'G2-15', 'G2-16', 'G2-17', 'G2-18', 'G2-19', 'G2-20', 'G3-06', 'G3-07', 'G3-13', 'G3-14', 'G3-15', 'G3-18', 'G3-19', 'G3-20']
a_signer 26
a_signer all in sources?
apastamba_grhya_sutra -400 san INDIAN usage 1 src True
baudhayana_dharmasutra -400 san INDIAN usage 3 src True
brihadaranyaka_upanishad -700 san INDIAN usage 3 src True
burnet_early_greek_philosophy 1930 en GRECO usage 1 src True
chandogya_upanishad -700 san INDIAN usage 3 src True
daodejing -350 lzh CHINESE usage 4 src True
epicurus_letters -300 grc GRECO usage 2 src True
hiranyakesi_grhya_sutra -400 san INDIAN usage 1 src True
holbach_systeme_en 1770 eng EUROPE_MODERN usage 1 src True
hume_dialogues_nhr 1779 eng EUROPE_MODERN usage 1 src True
ingersoll_works 1879 eng EUROPE_MODERN usage 1 src True
isa_upanishad -500 san INDIAN usage 3 src True
liji -300 lzh CHINESE usage 1 src True
lucretius_drn -55 eng GRECO usage 1 src True
mandukya_upanis
… [580 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib, hashlib, collections, os\nm=json.load(open('reports/protocole-date.json'))\nSRC=pathlib.Path('../Panini/research/nipada/corpus/_cache/sources')\nfor x in m['a_signer'][:5]:\n    p=SRC/(x['id']+'.txt')\n    print(x['id'], p.exists(), p.stat().st_si … [260 caractères tronqués]`

  ```
apastamba_grhya_sutra True 4307
baudhayana_dharmasutra True 3716
brihadaranyaka_upanishad True 3596
burnet_early_greek_philosophy True 495941
chandogya_upanishad True 5774
all 26 exist? True
missing sources []
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,pathlib,hashlib,re\nm=json.load(open('reports/protocole-date.json'))\nSRC=pathlib.Path('../Panini/research/nipada/corpus/_cache/sources')\nrows=[]\nfor x in m['a_signer']:\n    p=SRC/(x['id']+'.txt')\n    txt=p.read_text(encoding='utf-8',errors='replace')\n … [354 caractères tronqués]`

  ```
('sextus_pyrrho', 42, 552, 'cc20b37774b0655e')
('epicurus_letters', 84, 995, '2cfe388584a9a7e2')
('zadeh_1965', 278, 1778, 'cd9baea89c32f3bf')
('brihadaranyaka_upanishad', 596, 3596, '189b4a8f4085090f')
('baudhayana_dharmasutra', 626, 3716, '62a07681bbbc311e')
('vasistha_dharmasutra', 626, 3716, '62a07681bbbc311e')
('liji', 680, 3992, 'cc52fa05fd4af0f2')
('apastamba_grhya_sutra', 770, 4307, 'f7443b99845c0bd7')
('hiranyakesi_grhya_sutra', 770, 4307, 'f7443b99845c0bd7')
('daodejing', 788, 4487, '0d877881c8a644a3')
('zhuangzi', 788, 4487, '0d877881c8a644a3')
('paraskara_grhya_sutra', 848, 4769, 'e0bcd4dd8d3e8276')
('sankhayana_grhya_sutra', 848, 4769, 'e0bcd4dd8d3e8276')
('chandogya_upanishad', 890, 5774, '18f4886716914654')
('isa_upanishad', 890, 5774, '18f4886716914654')
('xiaojing', 908, 4994, '5ca04958d68f0555')
('yueji', 1166, 6443, '581a7e47811fc049')
('mandukya_upanishad', 1343, 26047, 'dd3f225708ec04dc')
('lucretius_drn', 1555, 27359, 'c13421704ad63ec7')
('plato_crito', 5398, 28160, '426278acead88b30')
('miller_1956', 8883, 52136, '55d7fcf2e9dbad07')
('plato_euthyphro_jowett', 12242, 69186, '4bee16ab376a2de9')
('hume_dialogues_nhr', 39012, 232242, '8de70402b8e299ba')
('burnet_
… [358 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nsigs=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))\nA=[\"ÊTRE\",\"DIFFÉRENCE\",\"RAPPORT\",\"ORIENTATION\",\"SUJET\",\"TEMPS\",\"MODALITÉ\",\"NOMBRE\",\"ESPACE\",\"OPÉRATION\",\"FONCTION\",\"STRUCTURE\",\"SYMÉTRIE\",\"ÉQU … [374 caractères tronqués]`

  ```
n 44 bad []
sums min/max 0.9999999999999999 1.0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,collections\ng=json.load(open('../Panini/research/nipada/falsification/nipada_v334_graph_v35.json'))\nnodes=g['nodes']\nprint('node sample keys',list(next(iter(nodes.values())).keys())[:30])\n# signature nodes\nvs={k:v for k,v in nodes.items() if isinstance … [350 caractères tronqués]`

  ```
node sample keys ['kind', 'author', 'year', 'language_original', 'tradition_label', 'v14_signature', 'ingestion_status', 'signed_n_chars']
nodes with v14_signature 57
a_signer with graph sig 9
['epicurus_letters', 'holbach_systeme_en', 'hume_dialogues_nhr', 'ingersoll_works', 'lucretius_drn', 'miller_1956', 'plato_euthyphro_jowett', 'sextus_pyrrho', 'zadeh_1965']
a_signer without graph sig 17
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,pathlib,hashlib,collections\nSRC=pathlib.Path('../Panini/research/nipada/corpus/_cache/sources')\nsigs=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))\nbyhash=collections.defaultdict(list)\nrows=[]\nfor k in sigs:\n    p=SRC … [660 caractères tronqués]`

  ```
44 sources absent []
44 word min/max 304 255752
<300 among 44 []
duplicate groups among 44:
['plato_gorgias', 'plato_gorgias_jowett'] words [12462, 12462]
['plato_meno', 'plato_meno_jowett'] words [12772, 12772]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,pathlib,hashlib,collections\nm=json.load(open('reports/protocole-date.json'))\nSRC=pathlib.Path('../Panini/research/nipada/corpus/_cache/sources')\nbyhash=collections.defaultdict(list)\nfor x in m['a_signer']:\n    p=SRC/(x['id']+'.txt'); h=hashlib.sha256(p … [349 caractères tronqués]`

  ```
duplicates among 26:
['apastamba_grhya_sutra', 'hiranyakesi_grhya_sutra']
['baudhayana_dharmasutra', 'vasistha_dharmasutra']
['chandogya_upanishad', 'isa_upanishad']
['daodejing', 'zhuangzi']
['paraskara_grhya_sutra', 'sankhayana_grhya_sutra']
exact 26 source hashes:
apastamba_grhya_sutra f7443b99845c0bd7643d648fcc3323f51deed449166e869f2b627f3defdc4f8e
baudhayana_dharmasutra 62a07681bbbc311e807d2e488883557601bd7f48210fd9d1b6b092ddf65a4fcd
brihadaranyaka_upanishad 189b4a8f4085090fc8178c37c102564ef8c88348d5acaa9061f501f702c6be7a
burnet_early_greek_philosophy 83de9c2359fc7b3b886e237935ad67ae6e5483f403258d7b5cce4c74e257bd7a
chandogya_upanishad 18f4886716914654f550e11cbd892504abdc993055aac8e4206bba5583109d72
daodejing 0d877881c8a644a3fb1ae4e635ffb508c79830281963652a9af07f005a110407
epicurus_letters 2cfe388584a9a7e286b4c04b8dbb2bb66b63afa67b943ffa9837585333f5542d
hiranyakesi_grhya_sutra f7443b99845c0bd7643d648fcc3323f51deed449166e869f2b627f3defdc4f8e
holbach_systeme_en d556f3b3a81d31e7ac0bd8760c7c580bf95f42788ce358eab0d4b6ac330b3d8a
hume_dialogues_nhr 8de70402b8e299baf5674c2d2c77d3a447959e63cc3e480d621edb1f401394b3
ingersoll_works 87da679106d6cb20401d9c55ca36fd592964b8356a07fc1d079b42283
… [1196 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '222,360p' tools/protocole_date.py; echo ===; sed -n '360,570p' tools/protocole_date.py", "description": "Read corpus selection logic"}`

  ```
def normaliser(texte) -> str:
    if not texte:
        return ""
    s = str(texte).lower()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"\b(trans|translation|transl\.?|trad\.?)\b.*$", "", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def auteur(v) -> str:
    a = normaliser(v.get("author"))
    return ALIASES_AUTEUR.get(a, a)


def titre(v) -> str:
    return normaliser(v.get("title_en") or v.get("title_original") or "")


def famille(v):
    t = v.get("tradition_label")
    return FAMILLES.get(t, t)


def arrondi(x, n=6):
    if x is None:
        return None
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return None
    return round(float(x), n)


# ---------------------------------------------------------------------------
# Chargement et métadonnées
# ---------------------------------------------------------------------------

class Corpus:
    def __init__(self):
        self.manifeste = lire_json(MANIFESTE_SOURCES)
        self.couverture = {x["id"]: x for x in lire_json(COUVERTURE)}
        self.graphe = lire_json(GRAPHE)
        self.noeuds = self.graphe["nodes"]
        self.aretes = self.graphe["edges"]
       
… [12330 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src timeout 120 python3 - <<'PY'\nimport json,pathlib\nfrom nipada.signing.analytical_projection import sign_analytic\np=pathlib.Path('nipada/corpus/_cache/sources/2_esdras.txt')\ntxt=' '.join(p.read_text(encoding='utf-8').sp … [135 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
  File "/home/stephane/Data13TB/stephane/GitHub/Panini/research/src/nipada/signing/analytical_projection.py", line 35, in sign_analytic
    from nltk import pos_tag
ModuleNotFoundError: No module named 'nltk'
[exit code: 1]
  ```

- **bash** `{"command": "cd ../Panini && ls -d .venv venv research/.venv 2>/dev/null; find . -maxdepth 3 -name 'python' -path '*/bin/*' 2>/dev/null | head; python3 -c 'import sys; print(sys.executable)'; pip list 2>/dev/null | grep -i nltk", "description": "Check for Panini venv"}`

  ```
research/.venv
.venv
./.venv/bin/python
/usr/bin/python3
[exit code: 1]
  ```

- **bash** `{"command": "cd ../Panini/research && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src timeout 180 .venv/bin/python - <<'PY'\nimport json,pathlib\nfrom nipada.signing.analytical_projection import sign_analytic\np=pathlib.Path('nipada/corpus/_cache/sources/2_esdras.txt')\ntxt=' '.join(p.read_text(encoding='u … [140 caractères tronqués]`

  ```
{"ÊTRE": 0.06667362152296491, "DIFFÉRENCE": 0.013816044014481136, "RAPPORT": 0.10099345547363635, "ORIENTATION": 0.005331763602619658, "SUJET": 0.14124697298283362, "TEMPS": 0.05189835957545324, "MODALITÉ": 0.02705634807902922, "NOMBRE": 0.17345233434667684, "ESPACE": 0.023588150398423387, "OPÉRATION": 0.0677678455988853, "FONCTION": 0.12163933372805305, "STRUCTURE": 0.15521307380581215, "SYMÉTRIE": 0.0006717195879862302, "ÉQUATION": 0.05065097728314488}
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\ns=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))['2_esdras']\nprint(json.dumps(s,ensure_ascii=False))\nPY", "description": "Show stored 2_esdras signature"}`

  ```
{"ÊTRE": 0.07446500282604852, "DIFFÉRENCE": 0.013816044014481109, "RAPPORT": 0.10099345547363615, "ORIENTATION": 0.005331763602619648, "SUJET": 0.14124697298283334, "TEMPS": 0.05189835957545314, "MODALITÉ": 0.02705634807902917, "NOMBRE": 0.14932406971800052, "ESPACE": 0.04847053574653187, "OPÉRATION": 0.06701372487945408, "FONCTION": 0.12163933372805281, "STRUCTURE": 0.14742169250272855, "SYMÉTRIE": 0.0006717195879862289, "ÉQUATION": 0.050650977283144785}
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,math\nstored=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))['2_esdras']\nnew={\"ÊTRE\": 0.06667362152296491, \"DIFFÉRENCE\": 0.013816044014481136, \"RAPPORT\": 0.10099345547363635, \"ORIENTATION\": 0.005331763602619658, \"S … [664 caractères tronqués]`

  ```
cos 0.9945962301506155 l2 0.0363770009467899 sum 0.9999999999999999 1.0
  ```

- **bash** `{"command": "cd ../Panini/research && cat > /tmp/calibrer_44.py <<'PY'\nimport json, pathlib, math, sys, time\nfrom nipada.signing.analytical_projection import sign_analytic\nROOT=pathlib.Path('.').resolve()\nSRC=ROOT/'nipada/corpus/_cache/sources'\nstored=json.load(open(ROOT/'nipada/falsification/a … [1066 caractères tronqués]`

  ```
started background job bash-44
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, math, collections, random\nimport numpy as np\nm=json.load(open('reports/protocole-date.json'))\nsigs=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))\nA=[\"ÊTRE\",\"DIFFÉRENCE\",\"RAPPORT\",\"ORIENTATION\",\"SUJET\",\"TEMPS … [1183 caractères tronqués]`

  ```
n 27
G1 1 mean d 0.08538973692164166 mean delta 0.0
  G1-20 book_of_enoch x sibylline_oracles 0 0.08539 1
G2 14 mean d 0.06616717697312198 mean delta 69.64285714285714
  G2-01 plato_gorgias x aristotle_posterior_analytics 45 0.145038 1
  G2-02 plato_meno x aristotle_de_caelo 55 0.086905 None
  G2-03 plato_republic_jowett x aristotle_parts_of_animals 50 0.067101 2
  G2-04 plato_symposium_jowett x aristotle_categories 45 0.056162 2
  G2-05 plato_republic_jowett x aristotle_nicomachean_ethics 40 0.035736 2
  G2-06 plato_laws x aristotle_parts_of_animals 20 0.067962 1
  G2-07 plato_gorgias x aristotle_prior_analytics 45 0.096208 None
  G2-08 plato_phaedo x aristotle_de_caelo 50 0.064818 None
  G2-09 isaiah_book x zechariah_book 180 0.043537 1
  G2-10 jeremiah_book x hosea_book 150 0.03538 1
  G2-11 ezekiel_book x zechariah_book 70 0.032685 1
  G2-12 daniel_book x book_of_enoch 35 0.14067 1
  G2-13 isaiah_book x ezekiel_book 110 0.015914 1
  G2-14 jeremiah_book x zechariah_book 80 0.038224 1
G3 12 mean d 0.11342042717549179 mean delta 1521.25
  G3-01 2_esdras x miller_evidence_prophecy 1736 0.120261 1
  G3-02 daniel_book x kleene_1936 2101 0.109724 None
  G3-03 book_of_enoch x curry_193
… [720 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, math, collections\nimport numpy as np\nm=json.load(open('reports/protocole-date.json'))\nsigs=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))\nA=[\"ÊTRE\",\"DIFFÉRENCE\",\"RAPPORT\",\"ORIENTATION\",\"SUJET\",\"TEMPS\",\"MOD … [3412 caractères tronqués]`

  ```
G2 dates within family
{
 "n": 14,
 "beta_obs": -0.42569896235341725,
 "r2_obs": 0.2509098851571937,
 "p_perm": 0.12593703148425786,
 "null_moy": -0.19462100170005225,
 "null_sd": 0.1959670819884059,
 "null_q025": -0.5207582440356038,
 "null_q975": 0.1489223828822089,
 "groupes": {
  "GRECO": 8,
  "ABRAHAMIC": 6
 }
}
G3 dates within language
{
 "n": 12,
 "beta_obs": -0.01133621286321172,
 "r2_obs": 0.04756377731318806,
 "p_perm": 0.7981009495252374,
 "null_moy": 0.016269730549299106,
 "null_sd": 0.00970867531274733,
 "null_q025": -0.008545693197277758,
 "null_q975": 0.029501405175733224,
 "groupes": {
  "eng": 10,
  "grc": 2
 }
}
texts 27
sigperm G2 obs 0.06616717697312198 null mean 0.12086162803489758 sd 0.01400498824377105 p 0.0004997501249375312
sigperm G3 obs 0.11342042717549179 null mean 0.1211487159649591 sd 0.016626680425761285 p 0.6331834082958521
sigperm ALL obs 0.08788056817226855 null mean 0.1207237796377034 sd 0.009240346442821673 p 0.0004997501249375312
sigperm slope G2 obs -0.42569896235341725 null mean 0.0031499859122401867 sd 0.3674467454494227 p 0.25037481259370314
sigperm slope G3 obs -0.01133621286321172 null mean -0.0005087891115289321 sd 0.020772968916446116 p 
… [18 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,pathlib,hashlib,collections\nm=json.load(open('reports/protocole-date.json'))\nSRC=pathlib.Path('../Panini/research/nipada/corpus/_cache/sources')\nallids=[t['id'] for t in m['textes']]\nbyhash=collections.defaultdict(list)\nfor i in allids:\n    p=SRC/(i+' … [1110 caractères tronqués]`

  ```
duplicates among 59 texts:
['apastamba_grhya_sutra', 'hiranyakesi_grhya_sutra']
['baudhayana_dharmasutra', 'vasistha_dharmasutra']
['chandogya_upanishad', 'isa_upanishad']
['daodejing', 'qiwulun', 'zhuangzi']
['paraskara_grhya_sutra', 'sankhayana_grhya_sutra']
['plato_gorgias', 'plato_gorgias_jowett']
n texts with twin 13
complete pairs involving twin:
G2-01 plato_gorgias twin aristotle_posterior_analytics 
G2-07 plato_gorgias twin aristotle_prior_analytics 
G3-16 plato_gorgias twin aristotle_parts_of_animals 
['plato_gorgias', 'plato_gorgias_jowett'] same sig? True max diff 0.0
['plato_meno', 'plato_meno_jowett'] same sig? True max diff 0.0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,pathlib,hashlib,collections\nm=json.load(open('reports/protocole-date.json'))\nSRC=pathlib.Path('../Panini/research/nipada/corpus/_cache/sources')\ns=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))\na={x['id'] for x in m['a_ … [483 caractères tronqués]`

  ```
a_signer with identical source to a signed 44 text:
['qiwulun', 'zhuangzi', 'daodejing'] signed: ['qiwulun'] to sign: ['zhuangzi', 'daodejing']
  ```

- **job_output** `{"job_id": "bash-44"}`

  ```
1 2_esdras 0.994596 0.036377 3733
2 aristotle_categories 0.995625 0.030335 17525
3 aristotle_de_caelo 0.991951 0.040372 13559
4 aristotle_nicomachean_ethics 0.998294 0.019312 116372
5 aristotle_parts_of_animals 0.996259 0.027796 7548
6 aristotle_posterior_analytics 0.998157 0.021973 941
7 aristotle_prior_analytics 0.997292 0.024428 422
8 bengio_2003 0.967836 0.105334 6607
9 book_of_enoch 0.999797 0.007244 827
10 curry_1930 0.992348 0.040637 18585
11 daniel_book 0.999989 0.001694 483
12 dn1_brahmajala 0.99762 0.022696 12773
13 ezekiel_book 0.999998 0.000859 1506
14 hosea_book 0.99999 0.001648 328
15 isaiah_book 0.999998 0.000685 1579
16 jeremiah_book 0.999998 0.000813 1609
17 kleene_1936 0.996225 0.028776 1129
18 lukasiewicz_1920 0.999539 0.010488 451
19 mengzi 0.989115 0.049993 304
20 mikolov_2013 0.999192 0.013434 600
21 miller_evidence_prophecy 0.99764 0.022839 35989
22 mn2_sabbasava 0.991115 0.042778 2055
23 mn35_culasaccaka 0.998134 0.020954 555
24 nostradamus_centuries 0.998802 0.016051 11008
25 plato_charmides 0.994491 0.034169 10668
26 plato_gorgias 0.996253 0.029379 12462
27 plato_gorgias_jowett 0.996253 0.029379 12462
28 plato_laws 0.998057 0.020972 241637
29 plato_meno 0.
… [716 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nc=json.load(open('/tmp/calibration_44.json'))\nfails=[(k,v) for k,v in c.items() if not v['ok']]\nprint('n',len(c),'fails',len(fails))\nfor k,v in sorted(fails,key=lambda kv: kv[1]['cos']): print(k,v)\nprint('min cos',min(v['cos'] for v in c.values()),'max … [440 caractères tronqués]`

  ```
n 44 fails 2
bengio_2003 {'cos': 0.9678357922916859, 'l2': 0.10533380815991583, 'words': 6607, 'ok': False}
mengzi {'cos': 0.9891145832750529, 'l2': 0.049993389740848944, 'words': 304, 'ok': False}
min cos 0.9678357922916859 max l2 0.10533380815991583
n cos>=0.99 42
n l2<=0.01 8
-rw-r--r--. 1 stephane stephane 66060 2026-09-08 13:08 ../Panini/research/nipada/corpus/_cache/sources/bengio_2003.txt
-rw-r--r--. 1 stephane stephane  1666 2026-09-08 15:08 ../Panini/research/nipada/corpus/_cache/sources/mengzi.txt
-rw-r--r--. 1 stephane stephane 22381 2026-10-18 10:03 ../Panini/research/nipada/falsification/analytic_sigs_v1.json
  ```

### 👤 Utilisateur

background job bash-44 (bash: cd ../Panini/research && cat > /tmp/calibrer_44.py <<'PY'
import json, pathlib, math, sys, time
from nipada.signing.analytical_projection import sign_analytic
ROOT=pathlib.Path('.').resolve()
SRC=ROOT/'nipada/corpus/_cache/sources'
stored=json.load(open(ROOT/'nipada/falsification/analytic_sigs_v1.json',encoding='utf-8'))
A=list(next(iter(stored.values())).keys())
out={}
t0=time.time()
for i,(k,ref) in enumerate(sorted(stored.items()),1):
    p=SRC/f'{k}.txt'
    words=p.read_text(encoding='utf-8',errors='replace').split()
    sig=sign_analytic(' '.join(words[:10000]))
    a=[float(ref[x]) for x in A]; b=[float(sig[x]) for x in A]
    na=math.sqrt(sum(x*x for x in a)); nb=math.sqrt(sum(x*x for x in b))
    cos=sum(x*y for x,y in zip(a,b))/(na*nb) if na and nb else None
    l2=math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
    out[k]={'cos':cos,'l2':l2,'words':len(words),'ok': bool(cos is not None and (cos>=0.99 or l2<=0.01))}
    print(i,k,round(cos,6) if cos else None,round(l2,6),len(words),flush=True)
json.dump(out,open('/tmp/calibration_44.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('done',time.time()-t0,'s')
PY
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src timeout 900 .venv/bin/python /tmp/calibrer_44.py) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cd ../Panini && git status --short -- research/nipada/corpus/_cache/sources/bengio_2003.txt research/nipada/corpus/_cache/sources/mengzi.txt research/src/nipada/signing/analytical_projection.py research/nipada/falsification/analytic_sigs_v1.json; echo ---; git log --oneline -3 -- resear … [232 caractères tronqués]`

  ```
---
---
-rw-r--r--. 1 stephane stephane  4040 2026-10-18 10:03 research/src/nipada/signing/analytical_projection.py
-rw-r--r--. 1 stephane stephane 34813 2026-09-07 12:47 research/src/nipada/signing/v14_enrichment.py
  ```

- **bash** `{"command": "cd ../Panini/research && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src timeout 300 .venv/bin/python - <<'PY'\nimport json,pathlib,math\nfrom nipada.signing.analytical_projection import sign_analytic\nSRC=pathlib.Path('nipada/corpus/_cache/sources')\nref=json.load(open('nipada/falsification/a … [583 caractères tronqués]`

  ```
bengio_2003 W None words 6607 cos 0.9678357922916859 l2 0.10533380815991583
bengio_2003 W 10000 words 6607 cos 0.9678357922916859 l2 0.10533380815991583
mengzi W None words 304 cos 0.9891145832750529 l2 0.049993389740848944
mengzi W 10000 words 304 cos 0.9891145832750529 l2 0.049993389740848944
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nm=json.load(open('reports/protocole-date.json'))\np334=json.load(open('../Panini/research/nipada/falsification/pairs334_axes_v1.json'))['pairs']\nt334={x for p in p334 for x in (p['a'],p['b'])}\nt59={t['id'] for t in m['textes']}\na26={x['id'] for x in m[' … [388 caractères tronqués]`

  ```
t334 48 t59 59 inter 34
26 in t334 1 ['zadeh_1965']
26 not in t334 25
t334 unsigned 4 ['an7_64_kodhana', 'aristotle_de_anima', 'brahma_sutra_badarayana', 'zadeh_1965']
59 unsigned 26
  ```

- **bash** `{"command": "date -Iseconds; git rev-parse --short HEAD; git -C ../Panini rev-parse --short HEAD; git status --short | head -30", "description": "Check date and HEADs"}`

  ```
2026-11-15T10:52:48-05:00
be3f41ad
9b80c323
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 M tools/drave.py
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
  ```

- **bash** `{"command": "git log --oneline -5; git status --short | wc -l; git status --short", "description": "Check recent commits and status"}`

  ```
be3f41ad SEMAINE 2 — W3 : LA MATRICE DU TAGGER (DÉFAUT HORS LIGNE CODE 0, CLÉ INVALIDE 4, RÉSEAU COUPÉ 0 APRÈS 3 ESSAIS, 1 000 PHRASES = 143 870 TOKENS) ; 4 TESTS DE PLUS
3439cb0c ÉTAT — W2 : heartbeat e181ce02 rafraîchi (2026-11-15 09:30), porte-sessions verte
1683c2b4 W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3
4dbeff45 SEMAINE 2 — W1 : LE GOLD RÉEL 452 (20 HAND + 432 CORPUS, 242 FR / 210 EN), LE SPLIT 402/H50 FIGÉ, LE SHA256, LES 10 GP/SUB LISTÉS POUR S
6b2208ee PLAN — LA SEMAINE 2 (16 → 22/11) : GOLD 452, PAGE / DE S, PANINI À DATE, RESTITUTION v3, LE TAGGER PAR DÉFAUT ? ; LA FILE DU CHANTIER À 41 TÂCHES
14
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 M tools/drave.py
?? reports/rapport-s-par
… [55 caractères tronqués]
  ```

- **bash** `{"command": "cat > tools/panini_signatures_26.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"panini_signatures_26.py — W4 : le signeur V14 à lancer côté Panini/NIPADA.\n\nCe script est **côté Panini** : il lit les sources du §334, re-extrait les 44\nsignatures de référence pour la calibration, puis signe  … [8038 caractères tronqués]`

  ```
OK
  ```

- **bash** `{"command": "cat > tools/panini_manifeste.py <<'PY'\n#!/usr/bin/env python3\n\"\"\"panini_manifeste.py — W4 : le manifeste des 26 signatures V14 et le rejeu disponible.\n\nCe script construit `reports/panini-manifeste.json`. Il ne modifie jamais Panini :\nil lit le manifeste gelé B1, les 44 signatur … [26106 caractères tronqués]`

  ```
OK
  ```

- **bash** `{"command": "python3 tools/panini_manifeste.py --construire", "description": "Build manifest JSON"}`

  ```
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_manifeste.py", line 559, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_manifeste.py", line 544, in main
    doc = construire()
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_manifeste.py", line 322, in construire
    n2 = perm_dates(rows, "G2", "famille")
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_manifeste.py", line 130, in perm_dates
    groupes[r[cle]].append(i)
            ~^^^^^
KeyError: 'famille'
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/panini_manifeste.py'\ns=open(p).read()\ns=s.replace('''                \"meme_famille\": p[\"meme_famille\"], \"meme_langue\": p[\"meme_langue\"],\n                \"d_topo\": p[\"d_topo\"],''','''                \"meme_famille\": p[\"meme_famille\"], \"meme_l … [925 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_manifeste.py", line 561, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_manifeste.py", line 546, in main
    doc = construire()
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_manifeste.py", line 359, in construire
    "mots": v["mots"], "ok": bool(v["ok"])} for k, v in sorted(c.items())},
            ~^^^^^^^^
KeyError: 'mots'
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/panini_manifeste.py'\ns=open(p).read()\ns=s.replace('''            \"par_oeuvre\": {k: {\"cos\": arr(v[\"cos\"]), \"l2\": arr(v[\"l2\"]),\n                               \"mots\": v[\"mots\"], \"ok\": bool(v[\"ok\"])} for k, v in sorted(c.items())},''','''     … [425 caractères tronqués]`

  ```
écrit : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/panini-manifeste.json
W4 — manifeste Panini
  à signer           : 26 textes (3 sources < 300 mots)
  doublons de sources: 6 groupes
  rejeu              : 27/60 paires
  par groupe         : G1 1/20, G2 14/20, G3 12/20
  calibration        : 42/44 ; échecs ['bengio_2003', 'mengzi']
  p-value H0         : None
  verdict            : incomplet : 27/60 paires calculées, 33 manquantes ; aucune p-value de H0 ; la calibration 42/44 échoue sur bengio_2003 et mengzi ; 3 sources < 300 mots.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/panini-manifeste.json'))\nm=d['manifeste']; r=d['rejeu']\nprint(json.dumps({k:m[k] for k in ['n_textes','n_deja_signes','n_a_signer','n_paires','sources_courtes','reduction_effective']},ensure_ascii=False,indent=1))\nprint('doublo … [451 caractères tronqués]`

  ```
{
 "n_textes": 59,
 "n_deja_signes": 33,
 "n_a_signer": 26,
 "n_paires": 60,
 "sources_courtes": [
  "epicurus_letters",
  "sextus_pyrrho",
  "zadeh_1965"
 ],
 "reduction_effective": {
  "textes_distincts_a_signer": 26,
  "vecteurs_distincts": 21,
  "vecteurs_deja_disponibles": [
   "qiwulun"
  ],
  "vecteurs_nouveaux_distincts": 20
 }
}
doublons:
{'sha256': 'f7443b99845c0bd7643d648fcc3323f51deed449166e869f2b627f3defdc4f8e', 'ids': ['apastamba_grhya_sutra', 'hiranyakesi_grhya_sutra'], 'signes': [], 'a_signer': ['apastamba_grhya_sutra', 'hiranyakesi_grhya_sutra'], 'mots': 770}
{'sha256': '62a07681bbbc311e807d2e488883557601bd7f48210fd9d1b6b092ddf65a4fcd', 'ids': ['baudhayana_dharmasutra', 'vasistha_dharmasutra'], 'signes': [], 'a_signer': ['baudhayana_dharmasutra', 'vasistha_dharmasutra'], 'mots': 626}
{'sha256': '18f4886716914654f550e11cbd892504abdc993055aac8e4206bba5583109d72', 'ids': ['chandogya_upanishad', 'isa_upanishad'], 'signes': [], 'a_signer': ['chandogya_upanishad', 'isa_upanishad'], 'mots': 890}
{'sha256': '0d877881c8a644a3fb1ae4e635ffb508c79830281963652a9af07f005a110407', 'ids': ['daodejing', 'qiwulun', 'zhuangzi'], 'signes': ['qiwulun'], 'a_signer': ['daodejing', 'zhuan
… [4458 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, numpy as np, collections\nd=json.load(open('reports/panini-manifeste.json'))\nrows=[]\nfor p in d['rejeu']['paires_calculees']:\n    rows.append({'id':p['id'],'g':p['groupe'],'delta':p['delta_annee'],'d':p['d_sig'],'lang':p.get('langue'),'fam':p.get('famil … [1241 caractères tronqués]`

  ```
G3 all (-0.011336335074664854, 0.04756468190124241, np.float64(0.0009995002498750624), array([-0.00877966,  0.02923891]))
G3 sans G3-08 (0.012011408839761838, 0.11863360092156605, np.float64(0.010994502748625687), array([0.01274292, 0.02107905]))
G3 sans G3-17 (-0.02485177843075135, 0.17530963152763135, np.float64(0.0009995002498750624), array([-0.02146234,  0.0310653 ]))
G3 sans G3-01 (-0.011595217185109254, 0.04957634310254688, np.float64(0.0009995002498750624), array([-0.00949695,  0.02941852]))
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/panini-manifeste.json'))\nprint(d['panini_lecture_seule'])\nprint(d['commit_drave'], d['commit_panini'])\nprint('calibration reference size',len(d['calibration']['reference']))\nprint('json size',len(open('reports/panini-manifeste … [71 caractères tronqués]`

  ```
{'statut_sha256_avant': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'statut_sha256_apres': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'identique': True, 'note': 'git status --porcelain limité à falsification/ et sources/ ; aucune écriture W4 dans Panini.'}
be3f41adc89b7f7bda103a54262ecf0c358c4339 9b80c323629be60c68696f5c5a21f37ad9420073
calibration reference size 44
json size 75189
  ```

- **bash** `{"command": "python3 tools/protocole_date.py --verifier; echo exit=$?", "description": "Verify B1 manifest hashes"}`

  ```
OK : 60 paires uniques, 20/20/20, 59 textes, sources acquises.
commit Drave : f926b5bc6d8da64ffb1c59a6dbc8a6fcfd1c9888
commit Panini lu : 9b80c323629be60c68696f5c5a21f37ad9420073
paires : 60 ; textes : 59 ; à signer : 26
exit=0
  ```

- **bash** `{"command": "cd ../Panini/research && PYTHONDONTWRITEBYTECODE=1 timeout 900 .venv/bin/python /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_signatures_26.py --manifeste /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/panini-manifeste.json --sortie /tmp/panini-v14-26.json --forc … [93 caractères tronqués]`

  ```
started background job bash-64
  ```

- **job_output** `{"job_id": "bash-64"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/panini_signatures_26.py'\ns=open(p).read()\nold='''    sortie.parent.mkdir(parents=True, exist_ok=True)\n    sortie.write_text(json.dumps({\n        \"instrument\": \"V14 — sign_analytic (nipada.signing.analytical_projection), 10 000 premiers mots\",\n         … [1639 caractères tronqués]`

  ```
OK
  ```

- **job_output** `{"job_id": "bash-64"}`

  ```
(no new output)
[status: running]
  ```

- **job_output** `{"job_id": "bash-64", "wait": true, "timeout_ms": 180000}`

  ```
exit=1
[stderr]
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_signatures_26.py", line 192, in <module>
    print(" -", e)
                 ^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_signatures_26.py", line 150, in main
    for t in manifeste["a_signer"]:
             ~~~~~~~~~^^^^^^^^^^^^
KeyError: 'a_signer'
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/panini_signatures_26.py'\ns=open(p).read()\nold='''    # 2. les 26 signatures demandées\n    signatures, sources_out, erreurs = {}, {}, []\n    for t in manifeste[\"a_signer\"]:'''\nnew='''    # 2. les 26 signatures demandées\n    a_signer = manifeste.get(\"a_ … [827 caractères tronqués]`

  ```
149:    a_signer = manifeste.get("a_signer") or manifeste.get("manifeste", {}).get("a_signer")
150:    if not a_signer:
151:        raise SystemExit("le manifeste ne porte pas a_signer (26 textes)")
153:    for t in a_signer:
193:    print(f"signatures   : {len(signatures)}/{len(a_signer)} ; sortie : {sortie}")
198:    if len(signatures) != len(a_signer):
  ```

- **bash** `{"command": "cd ../Panini/research && PYTHONDONTWRITEBYTECODE=1 timeout 900 .venv/bin/python /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_signatures_26.py --manifeste /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/panini-manifeste.json --sortie /tmp/panini-v14-26.json --forc … [94 caractères tronqués]`

  ```
started background job bash-67
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/panini-manifeste.json'))\nfor i,t in enumerate(d['manifeste']['a_signer'],1):\n    note=[]\n    if not t['seuil_300']: note.append(f\"**{t['mots']} mots**\")\n    if t['signature_deja_disponible_via']: note.append('sig. via `'+t[' … [473 caractères tronqués]`

  ```
| 01 | `apastamba_grhya_sutra` | -400 | san | INDIAN | 770 | 1 | `G1-05` | doublon de `hiranyakesi_grhya_sutra` |
| 02 | `baudhayana_dharmasutra` | -400 | san | INDIAN | 626 | 3 | `G1-01`, `G3-18`, `G3-19` | doublon de `vasistha_dharmasutra` |
| 03 | `brihadaranyaka_upanishad` | -700 | san | INDIAN | 596 | 3 | `G1-18`, `G2-16`, `G3-19` |  |
| 04 | `burnet_early_greek_philosophy` | 1930 | en | GRECO | 79972 | 1 | `G1-14` |  |
| 05 | `chandogya_upanishad` | -700 | san | INDIAN | 890 | 3 | `G1-17`, `G2-15`, `G3-18` | doublon de `isa_upanishad` |
| 06 | `daodejing` | -350 | lzh | CHINESE | 788 | 4 | `G1-07`, `G1-08`, `G2-20`, `G3-20` | sig. via `qiwulun` |
| 07 | `epicurus_letters` | -300 | grc | GRECO | 84 | 2 | `G1-09`, `G1-10` | **84 mots** ; graphe v35 |
| 08 | `hiranyakesi_grhya_sutra` | -400 | san | INDIAN | 770 | 1 | `G1-03` | doublon de `apastamba_grhya_sutra` |
| 09 | `holbach_systeme_en` | 1770 | eng | EUROPE_MODERN | 123805 | 1 | `G3-06` | graphe v35 |
| 10 | `hume_dialogues_nhr` | 1779 | eng | EUROPE_MODERN | 39012 | 1 | `G3-07` | graphe v35 |
| 11 | `ingersoll_works` | 1879 | eng | EUROPE_MODERN | 98782 | 1 | `G1-16` | graphe v35 |
| 12 | `isa_upanishad` | -500 | san | IND
… [1398 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/panini-manifeste.json'))\nshort=set(d['manifeste']['sources_courtes'])\nm=d['rejeu']['paires_manquantes']\nprint('missing pairs involving short:',[p['id'] for p in m if set(p['textes_sans_signature'])&short])\nprint('n',len([p for … [161 caractères tronqués]`

  ```
missing pairs involving short: ['G1-09', 'G1-10', 'G1-15', 'G3-13', 'G3-14', 'G3-15']
n 6
missing pairs: ['G1-01', 'G1-02', 'G1-03', 'G1-04', 'G1-05', 'G1-06', 'G1-07', 'G1-08', 'G1-09', 'G1-10', 'G1-11', 'G1-12', 'G1-13', 'G1-14', 'G1-15', 'G1-16', 'G1-17', 'G1-18', 'G1-19', 'G2-15', 'G2-16', 'G2-17', 'G2-18', 'G2-19', 'G2-20', 'G3-06', 'G3-07', 'G3-13', 'G3-14', 'G3-15', 'G3-18', 'G3-19', 'G3-20']
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/panini_signatures_26.py'\ns=open(p).read()\nold='''    # Le rejeu de `protocole_date.py` lit UN seul fichier : on y met les 59\n    # signatures (44 de référence + 26 nouvelles), pas seulement les 26.\n    signatures_completes = {k: {a: float(v[a]) for a in V1 … [2729 caractères tronqués]`

  ```
OK
  ```

- **job_output** `{"job_id": "bash-67", "wait": true, "timeout_ms": 180000}`

  ```
calibration : 42/44 ; échecs : ['bengio_2003', 'mengzi']
signatures   : 26/26 ; sortie : /tmp/panini-v14-26.json
 - epicurus_letters : 84 mots < 300 (hors support de calibration)
 - sextus_pyrrho : 42 mots < 300 (hors support de calibration)
 - zadeh_1965 : 278 mots < 300 (hors support de calibration)
exit=2
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd ../Panini/research && PYTHONDONTWRITEBYTECODE=1 timeout 900 .venv/bin/python /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_signatures_26.py --manifeste /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/panini-manifeste.json --sortie /tmp/panini-v14-26.json --forc … [101 caractères tronqués]`

  ```
started background job bash-71
  ```

- **bash** `{"command": "python3 tools/protocole_date.py --rejouer --rapide --signatures /tmp/panini-v14-26.json --sortie /tmp/protocole-complet-provisoire.json; echo exit=$?; python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/protocole-complet-provisoire.json'))\nprint(json.dumps(d,ensure_ascii=False,indent … [79 caractères tronqués]`

  ```
résultats écrits : /tmp/protocole-complet-provisoire.json
exit=0
{
 "statut": "complet",
 "n_paires": 60,
 "n_manquantes": 0,
 "paires_manquantes": [],
 "n_permutations": 300,
 "tests": {
  "G1_controle_positif": {
   "n": 20,
   "d_sig_moyenne": 0.12899443160638074,
   "p_permutation": 0.1893687707641196,
   "note": "nul : signatures permutées entre les textes du groupe G1."
  },
  "P1_G2": {
   "n": 20,
   "beta_brut": -0.1356103746002489,
   "r2": 0.046043450131664776,
   "p_permutation": 0.3588039867109635,
   "beta_standardise": -0.21457737562861742
  },
  "P2_G3": {
   "n": 20,
   "beta_brut": -0.010404057942400225,
   "r2": 0.033359796383119256,
   "p_permutation": 0.40863787375415284,
   "beta_standardise": -0.18264664350356732
  },
  "pooled": {
   "n": 60,
   "beta": [
    0.13943670719844176,
    -0.008038170489128506,
    -0.04759916264131492,
    0.014920319788583018
   ],
   "r2": 0.2035223720707322
  }
 },
 "verdict": "H0 non rejetée : aucun effet d'époque détectable sur ce plan",
 "date": "2026-11-15T10:55:40",
 "descriptif": {
  "G1": {
   "n": 20,
   "d_sig_moyenne": 0.12899443160638074,
   "delta_annee_moyen": 2.2
  },
  "G2": {
   "n": 20,
   "d_sig_moyenne": 0.
… [157 caractères tronqués]
  ```

- **bash** `{"command": "cp /tmp/panini-v14-26.json /tmp/panini-v14-26-provisoire-59.json 2>/dev/null && echo saved; ls -l /tmp/panini-v14-26*.json", "description": "Save provisional 59 signature file"}`

  ```
saved
-rw-r--r--. 1 stephane stephane 66656 15 nov 10:55 /tmp/panini-v14-26.json
-rw-r--r--. 1 stephane stephane 66656 15 nov 10:55 /tmp/panini-v14-26-provisoire-59.json
  ```

- **job_output** `{"job_id": "bash-71", "wait": true, "timeout_ms": 180000}`

  ```
calibration : 42/44 ; échecs : ['bengio_2003', 'mengzi']
signatures   : 26/26 ; sortie : /tmp/panini-v14-26.json
 - epicurus_letters : 84 mots < 300 (hors support de calibration)
 - sextus_pyrrho : 42 mots < 300 (hors support de calibration)
 - zadeh_1965 : 278 mots < 300 (hors support de calibration)
exit=2
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/panini-v14-26.json'))\nprint('keys',list(d))\nprint('calibration_ok',d['calibration_ok'],'n sig',len(d['signatures']),'n nouvelles',d['n_nouvelles'],'n total livrees',d['n_total_livrees'])\nprint('warnings',d['avertissements'][:2])\n … [105 caractères tronqués]`

  ```
keys ['instrument', 'commit', 'date', 'manifeste', 'calibration', 'calibration_ok', 'signatures', 'n_reference', 'n_nouvelles', 'n_total_livrees', 'nouvelles', 'sources', 'avertissements', 'regle']
calibration_ok False n sig 44 n nouvelles 26 n total livrees 44
warnings ['epicurus_letters : 84 mots < 300 (hors support de calibration)', 'sextus_pyrrho : 42 mots < 300 (hors support de calibration)']
source sample [('apastamba_grhya_sutra', {'fichier': 'nipada/corpus/_cache/sources/apastamba_grhya_sutra.txt', 'sha256': 'f7443b99845c0bd7643d648fcc3323f51deed449166e869f2b627f3defdc4f8e', 'mots': 770, 'seuil_300': True})]
  ```

- **bash** `{"command": "python3 tools/protocole_date.py --rejouer --rapide --signatures /tmp/panini-v14-26.json --sortie /tmp/protocole-gated.json; python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/protocole-gated.json'))\nprint({k:d[k] for k in ['statut','n_paires','n_manquantes','verdict']})\nPY", "descr … [55 caractères tronqués]`

  ```
résultats écrits : /tmp/protocole-gated.json
{'statut': 'incomplet', 'n_paires': 27, 'n_manquantes': 33, 'verdict': 'incomplet : le noyau est décrit, pas testé (pas de p-value sur un sous-ensemble)'}
  ```

- **bash** `{"command": "cat > reports/rapport-panini-manifeste.md <<'MD'\n# W4 — Panini : le manifeste des 26 signatures V14 et le rejeu disponible\n\n> **Ligne de roadmap** : **R0.7** (le bloc linguistique) / **L** · **Tâche** : **W4** (J3 matin,\n> la part du pilote) · **Date** : 2026-11-15 · **HEAD mesuré** … [20096 caractères tronqués]`

  ```
283 reports/rapport-panini-manifeste.md
  ```

- **read** `{"file_path": "reports/rapport-panini-manifeste.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-panini-manifeste.md</path>
<type>file</type>
<content>
1: # W4 — Panini : le manifeste des 26 signatures V14 et le rejeu disponible
2: 
3: > **Ligne de roadmap** : **R0.7** (le bloc linguistique) / **L** · **Tâche** : **W4** (J3 matin,
4: > la part du pilote) · **Date** : 2026-11-15 · **HEAD mesuré** : `be3f41ad` · **Verdict** :
5: > ✅ **le manifeste est prêt et envoyable** ; ❌ **le rejeu n'est pas un test** — **27/60** paires
6: > calculées, **33** manquantes, calibration **42/44**, **3** sources sous 300 mots, **5** groupes de
7: > doublons parmi les 26. **Aucune p-value de H0 n'est écrite.**
8: >
9: > **JSON** : [`panini-manifeste.json`](panini-manifeste.json) · **Commande Panini** :
10: > [`../tools/panini_signatures_26.py`](../tools/panini_signatures_26.py) · **Rejeu** :
11: > [`../tools/protocole_date.py`](../tools/protocole_date.py) · **Manifeste B1** :
12: > [`protocole-date.json`](protocole-date.json).
13: 
14: **En trois lignes.** (1) Les **26** textes du protocole B1 qui n'ont pas de signature
15: `analytic_sigs_v1` sont listés, avec leur fichier source, leur SHA-256, leurs mots et les paires
16: qu'il
… [8001 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/panini-manifeste.json'))\ns=d['calibration']['reference']['2_esdras']\nfor k,v in s.items(): print(f'\"{k}\": {v},')\nprint('sum',sum(s.values()))\nPY", "description": "Get real example signature"}`

  ```
"ÊTRE": 0.07446500282604852,
"DIFFÉRENCE": 0.013816044014481109,
"RAPPORT": 0.10099345547363615,
"ORIENTATION": 0.005331763602619648,
"SUJET": 0.14124697298283334,
"TEMPS": 0.05189835957545314,
"MODALITÉ": 0.02705634807902917,
"NOMBRE": 0.14932406971800052,
"ESPACE": 0.04847053574653187,
"OPÉRATION": 0.06701372487945408,
"FONCTION": 0.12163933372805281,
"STRUCTURE": 0.14742169250272855,
"SYMÉTRIE": 0.0006717195879862289,
"ÉQUATION": 0.050650977283144785,
sum 0.9999999999999999
  ```

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-panini-manifeste.md'\ns=open(p).read()\nold='''  \"signatures\": {\n    \"baudhayana_dharmasutra\": {\n      \"ÊTRE\": 0.12, \"DIFFÉRENCE\": 0.03, \"RAPPORT\": 0.0, \"ORIENTATION\": 0.0,\n      \"SUJET\": 0.0, \"TEMPS\": 0.0, \"MODALITÉ\": 0.0, \"NOM … [1305 caractères tronqués]`

  ```
136:Exemple réel, avec une œuvre **déjà signée** (`2_esdras`, somme 1) ; les 26 doivent
146:    "2_esdras": {
  ```

- **read** `{"file_path": "reports/rapport-panini-manifeste.md", "offset": 120, "limit": 180}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-panini-manifeste.md</path>
<type>file</type>
<content>
120: - Le **venv de Panini** (`research/.venv`) est celui qui porte `nltk` et WordNet ; sans lui,
121:   l'extracteur ne démarre pas.
122: - La commande écrit `/tmp/panini-v14-26.json`. **C'est ce fichier que Panini renvoie** (ou dépose
123:   dans un dossier partagé) : il contient la calibration, les 26 signatures et les sources.
124: - Codes de sortie : **0** = calibration 44/44 et 26 signatures ; **2** = calibration incomplète
125:   (le test ne doit pas être lancé) ; **3** = source absente ou signature invalide.
126: - **Garde-fou de calibration.** Si la calibration n'est pas 44/44, le script met les 26 signatures
127:   dans `nouvelles` mais **ne les livre pas** dans `signatures` : le fichier ne contient alors que
128:   les 44 références, et le rejeu B1 reste `incomplet` (27/60) au lieu de tester sur un instrument
129:   non calibré. C'est volontaire.
130: 
131: ### 2.2 Le format
132: 
133: Le fichier est un JSON UTF-8. Le rejeu B1 lit la clé `signatures` ; les autres clés sont le
134: diagnostic.
135: 
136: Exemple réel, avec une œuvre **déjà signée** 
… [11615 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-panini-manifeste.md'\ns=open(p).read()\ns=s.replace('''`mots` = mots du fichier source ; `usage` = nombre de paires du protocole qui utilisent le texte ;\n`sig.` = état particulier. Les 26 sources existent toutes, et sont toutes `ok = true` dans le\n … [2287 caractères tronqués]`

  ```
62:| 05 | `chandogya_upanishad` | -700 | san | INDIAN | 890 | 3 | `G1-17`, `G2-15`, `G3-18` | doublon de `isa_upanishad` |
69:| 12 | `isa_upanishad` | -500 | san | INDIAN | 890 | 3 | `G2-15`, `G2-16`, `G2-17` | doublon de `chandogya_upanishad` |
189:- **G2** : `G2-15` à `G2-20` (6 paires).
228:grande distance et le plus petit écart de date des **10 paires anglaises** du sous-ensemble. C'est
230:Sans elle, la pente devient positive (+0,012) et le `p_perm` reste 0,011 (n = 11) : le signal ne
258:   `qiwulun` : 21 vecteurs distincts au mieux, 20 nouveaux. La paire `G2-15` (`chandogya` ×
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nm=json.load(open('reports/protocole-date.json'))\ncov={x['id']:x for x in json.load(open('../Panini/research/nipada/corpus/_cache/sources_coverage.json'))}\nbad=[x['id'] for x in m['a_signer'] if not cov.get(x['id'],{}).get('ok')]\nprint('not ok',bad)\nPY" … [46 caractères tronqués]`

  ```
not ok []
  ```

- **bash** `{"command": "grep -n 'rapport-tagger-defaut\\|rapport-panini-manifeste' reports/INDEX.md reports/README.md; echo ---; sed -n '1,80p' tools/index_reports.py", "description": "Check index and generator"}`

  ```
reports/INDEX.md:733:| [rapport-tagger-defaut.md](rapport-tagger-defaut.md) | W3 — la matrice du tagger : le défaut reste hors ligne (code 0), `--tagger` est la seule porte qui peut sortir 4 |
reports/README.md:23:| [`rapport-tagger-defaut.md`](rapport-tagger-defaut.md) | **W3/R0.7** — la matrice du tagger : défaut hors ligne **code 0** / `--tagger` **code 4** sans clé ; réseau coupé = repli **code 0** ; coût **1 000 phrases** = 143 870 tokens, ~0,031 $ hors pointe ; recommandation : défaut hors ligne, opt-in, pas de `auto` |
---
#!/usr/bin/env python3
"""index_reports.py — génère reports/INDEX.md à partir des en-têtes de fiches.

L'index est **exhaustif** et **déterministe** : une ligne par fiche, triée par nom,
avec son titre (premier `# `). Les fichiers d'infrastructure (`README.md`, `INDEX.md`
et `historique-*`) sont exclus du tableau ; les compteurs de `docs/pilotage/en-cours.md`
comptent, eux, tous les `.md` de `reports/`.

Usage :
    python3 tools/index_reports.py              # réécrit reports/INDEX.md
    python3 tools/index_reports.py --verifier   # ne réécrit rien, sort 1 si périmé
    python3 tools/index_reports.py --aide       # affiche l'aide (ne touche à rien)
"""
f
… [1928 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='reports/README.md'\ns=open(p).read()\nold='''| [`rapport-protocole-date.md`](rapport-protocole-date.md) | **Panini** — le protocole à date contrôlée : 60 paires, trois strates |\n'''\nnew='''| [`rapport-protocole-date.md`](rapport-protocole-date.md) | **Panini** — l … [424 caractères tronqués]`

  ```
ok
25:| [`rapport-panini-manifeste.md`](rapport-panini-manifeste.md) | **W4/Panini** — le manifeste des 26 signatures V14 : 27/60 paires, calibration 42/44, 3 sources courtes, contrôle N5 vide |
  ```

- **bash** `{"command": "python3 tools/panini_manifeste.py --verifier; echo exit=$?; python3 -m json.tool reports/panini-manifeste.json >/dev/null && echo JSON-OK; python3 -m py_compile tools/panini_manifeste.py tools/panini_signatures_26.py && echo PY-OK", "description": "Verify manifest JSON and scripts"}`

  ```
OK
exit=0
JSON-OK
PY-OK
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py > /tmp/revue.out 2>&1; echo exit=$?; grep -n 'panini-manifeste\\|panini_signatures\\|panini_manifeste' /tmp/revue.out | head -30; tail -20 /tmp/revue.out", "description": "Run documentation review"}`

  ```
exit=1
  revue de documentation · 752 fiche(s) · 845 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 751 fichiers, le disque en a 752
     · compteurs : en-cours.md dit 844 JSON, le disque en a 845
  ```

- **bash** `{"command": "grep -n '751\\|844\\|fiches\\|JSON' docs/pilotage/en-cours.md | head -20; grep -n 'Mis à jour' docs/pilotage/en-cours.md", "description": "Locate counters in state"}`

  ```
49:- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **19/19 verdicts `389b99f`** ; **56 tests** ; fiches [analyseur](../../reports/rapport-s-analyseur-roles.md), [arbre](../../reports/rapport-s-arbre-referents.md), [limites](../../reports/rapport-s-limites-v6.md), [fait divers](../../reports/rapport-s-fait-divers.md).
79:- **Ce qu'elle fait** : **erratum 04/11** : la distillation native ne gagne rien à parité stricte (−0,03/−0,01/−0,004 ; +0,14–0,18 = repondération) ; `kd2` et `rope2048` **arrêtés** ; **paire propre** : **3,1500** → **3,1119** (−0,06 ; −0,19 anglais) ; **repondération : −0,05** ; **2 048** ne bat pas 1 024 ; fiches [fenêtre](../../reports/rapport-n2-fenetre.md), [production](../../reports/rapport-n2-production-fenetre.md), [erratum](../../reports/rapport-n2-distillation-native.md), [porte](../../reports/rapport-n2-porte-propre.md).
93:- **Panini B1 — protocole à date contrôlée** : **60 paires** (20 G1, 20 G2, 20 G3), **59 textes**, **26 à signer** ; [fiche](../../reports/rapport-protocole-date.md), [JSON](../../reports/protocole-date.json).
105:| fic
… [272 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '86,135p' docs/pilotage/en-cours.md", "description": "Read state around Panini line"}`

  ```
- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests ; **19/19 verdicts `389b99f`** ; `/paragraphes` v7, `/` ancien arbre ; [v2](../../reports/rapport-coordination-s-v2.md).
- **N2 — en pause** : commande **`eval_longueurs.py --rope --val <dir>`** (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
- **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (**16** non vides, F1 **0,5270**) ([fiche](../../reports/rapport-restitution-v2.md)), **D1–D3** ([FAQ](../../reports/rapport-faq.md)), **E1** ([sommaire](../../reports/rapport-faq-sommaire.md)) ; [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).
- **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.
- **W2/W3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; défaut sans clé **code 0**, **0 socket** ; `--tagger` sans clé ou clé refusée **code 4** ; réseau coupé **code 0** + repli ; **1 000 phrases = 143 870 tokens / 0,031 $ hors pointe** ; **défaut hors lig
… [4842 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/en-cours.md'\ns=open(p).read()\nold='''- **Panini B1 — protocole à date contrôlée** : **60 paires** (20 G1, 20 G2, 20 G3), **59 textes**, **26 à signer** ; [fiche](../../reports/rapport-protocole-date.md), [JSON](../../reports/protocole-date.json).'''\ … [1574 caractères tronqués]`

  ```
ok
3:**Mis à jour : 2026-11-15, 11 h 05 HNE (W4 : le manifeste Panini et le rejeu disponible)**
93:- **Panini B1 — protocole à date contrôlée** : **60 paires** (20 G1, 20 G2, 20 G3), **59 textes**, **26 à signer** ; **W4** : manifeste prêt, rejeu **27/60**, calibration **42/44**, **3** sources <300 mots, aucune p-value de H0 ; [W4](../../reports/rapport-panini-manifeste.md), [JSON W4](../../reports/panini-manifeste.json), [B1](../../reports/rapport-protocole-date.md), [JSON B1](../../reports/protocole-date.json).
105:| fichiers / JSON de résultats | **752** / **845** | `reports/*.md` / `reports/*.json` |
119:| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9575 (+9,5) ; réel 452 : 0,9500 (+6,1) ; W2 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/att 402 inchangés, fermé −1,55 ; W3 : défaut hors ligne code 0, `--tagger` code 4 sans clé, 1 000 phrases = 143 870 tokens / 0,031 $ hors pointe** ; R2/R3 attendent N5/N4 | **J3 — restitution v3** (rôles) ; **Panini** : W4 manifeste prêt, calibration **42/44** ; **[fiche W3](../../reports/rapport-tagger-defaut.md)** |
127:**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold de pensée, **qualité des rôles** ; **J3.2*
… [219 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py > /tmp/revue2.out 2>&1; echo exit=$?; cat /tmp/revue2.out | tail -30", "description": "Re-run documentation review"}`

  ```
exit=0
  revue de documentation · 752 fiche(s) · 845 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo exit=${PIPESTATUS[0]}", "description": "Check en-cours length/format"}`

  ```
en-cours · 1650 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
exit=0
  ```

- **bash** `{"command": "sed -n '96,120p' docs/pilotage/roadmap.md; echo ===; grep -n 'B1\\|protocole à date\\|26 signatures\\|Panini' docs/pilotage/roadmap.md | head -30", "description": "Read roadmap Panini section"}`

  ```
**26 cas / 0 échec** ; les **612 phrases du gold** passent le schéma v2 (**612/612**) et les
**612 annotations dérivées v1** passent le schéma v1 (**612/612**) ; les contrôles négatifs
refusent la version adverse (612/612) et la mutation d'un champ obligatoire. Les **146 groupes /
437 porteurs / 930 alternatives** reproduisent le compte de B13 (contrôle de cohérence).
[`fiche`](../../reports/rapport-schema-v2-doc.md) + [`JSON`](../../reports/schema-v2-doc.json).
J11.4 **ferme la suite produit** ; la prochaine action B13 est **trancher `g017`**.

**J12.1 — le §334 et les 44 signatures.** La deuxième vague Panini est **mesurée et auditée** :
les **655 lignes** de paires ne contiennent que **495 paires uniques** (**160 doublons**, **7
auto-paires**) et **48 textes** distincts, dont **44** ont une signature V14 ; les **102/107**
sources acquises ne sont pas 102 URL (71 URL uniques). La loi H0 se reproduit (**R² = 0,909139** sur
655 lignes, **0,906307** sur 488 paires uniques non auto) ; la date seule explique **0,258**, mais
n'ajoute que **0,0089** après la topologie (p=0,86). Le plan est **colinéaire** : 180 paires de même
tradition à **28,7 ans** d'écart (max 230), 308 paires inter-t
… [12364 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/panini_manifeste.py'\ns=open(p).read()\nold='''    # calibration : lue depuis /tmp (résultat de `panini_signatures_26.py`)\n    calibration = None\n    if CALIBRATION.exists():\n        c = lire(CALIBRATION)\n        fails = sorted(k for k, v in c.items() if n … [2193 caractères tronqués]`

  ```
W4 — manifeste Panini
  à signer           : 26 textes (3 sources < 300 mots)
  doublons de sources: 6 groupes
  rejeu              : 27/60 paires
  par groupe         : G1 1/20, G2 14/20, G3 12/20
  calibration        : 42/44 ; échecs ['bengio_2003', 'mengzi']
  p-value H0         : None
  verdict            : incomplet : 27/60 paires calculées, 33 manquantes ; aucune p-value de H0 ; la calibration 42/44 échoue sur bengio_2003 et mengzi ; 3 sources < 300 mots.
  ```

- **bash** `{"command": "python3 tools/panini_manifeste.py --verifier; echo exit=$?; python3 - <<'PY'\nimport json\nd=json.load(open('reports/panini-manifeste.json'))\nprint(d['commit_drave'],d['commit_panini'],d['panini_lecture_seule']['identique'])\nprint(d['calibration']['mesure']['ok'],d['calibration']['mes … [124 caractères tronqués]`

  ```
OK
exit=0
be3f41adc89b7f7bda103a54262ecf0c358c4339 9b80c323629be60c68696f5c5a21f37ad9420073 True
42 ['bengio_2003', 'mengzi']
27 33
  ```

- **bash** `{"command": "python3 - <<'PY'\np='tools/panini_manifeste.py'\ns=open(p).read()\nold='''        \"sources\": {\n            \"manifeste_b1\": {\"chemin\": \"reports/protocole-date.json\", \"sha256\": sha256(MANIFESTE_B1)},\n            \"signatures44\": {\"chemin\": \"Panini/research/nipada/falsifica … [939 caractères tronqués]`

  ```
W4 — manifeste Panini
  à signer           : 26 textes (3 sources < 300 mots)
  doublons de sources: 6 groupes
  rejeu              : 27/60 paires
  par groupe         : G1 1/20, G2 14/20, G3 12/20
  calibration        : 42/44 ; échecs ['bengio_2003', 'mengzi']
  p-value H0         : None
  verdict            : incomplet : 27/60 paires calculées, 33 manquantes ; aucune p-value de H0 ; la calibration 42/44 échoue sur bengio_2003 et mengzi ; 3 sources < 300 mots.
OK
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/panini-manifeste.json'))\nfor k,v in d['sources'].items(): print(k, v['chemin'], v['sha256'][:12])\nPY", "description": "Inspect source hashes in JSON"}`

  ```
manifeste_b1 reports/protocole-date.json 4f4ce0dcb11a
paires334 Panini/research/nipada/falsification/pairs334_axes_v1.json 8de7a6797d53
graphe334 Panini/research/nipada/falsification/nipada_v334_graph_v35.json 9ddf050aa169
signatures44 Panini/research/nipada/falsification/analytic_sigs_v1.json 8aa9c1d50d89
revalidation334 Panini/research/nipada/falsification/nipada_v334_revalidation_v35.json b2be71436a01
couverture Panini/research/nipada/corpus/_cache/sources_coverage.json 5d06443de6ae
manifeste_sources Panini/research/nipada/corpus/_cache/sources_manifest.json 5eda052cadf3
v150 Panini/research/nipada/falsification/nipada_v150_validation.json 353168c2fd38
  ```

- **bash** `{"command": "test -f reports/rapport-panini-manifeste.md && echo FICHE-OK; test -f reports/panini-manifeste.json && echo JSON-OK; python3 tools/protocole_date.py --verifier >/tmp/proto.out 2>&1; echo proto=$?; tail -2 /tmp/proto.out", "description": "Run acceptance checks"}`

  ```
FICHE-OK
JSON-OK
proto=0
commit Panini lu : 9b80c323629be60c68696f5c5a21f37ad9420073
paires : 60 ; textes : 59 ; à signer : 26
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -20; echo exit=${PIPESTATUS[0]}", "description": "Check context budget"}`

  ```
3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2624    227   T1   2800  reports/README.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4020 mots (budget 4 000)

  avertissements :
     · 59 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-f
… [118 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/en-cours.md'\ns=open(p).read()\ns=s.replace('''- **Panini B1 — protocole à date contrôlée** : **60 paires** (20 G1, 20 G2, 20 G3), **59 textes**, **26 à signer** ; **W4** : manifeste prêt, rejeu **27/60**, calibration **42/44**, **3** sources <300 mots … [1252 caractères tronqués]`

  ```
avertissements :
     · 59 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4008 mots (AGENTS + en-cours + une tâche) > budget 4 000
exit=1
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/en-cours.md'\ns=open(p).read()\ns=s.replace('''- **Panini B1 — protocole à date contrôlée** : **60 paires** (20 G1, 20 G2, 20 G3), **59 textes**, **26 à signer** ; **W4** : manifeste prêt, rejeu **27/60**, calibration **42/44** ; [W4](../../reports/rap … [581 caractères tronqués]`

  ```
avertissements :
     · 59 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
exit=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -5; echo exit=${PIPESTATUS[0]}; python3 tools/verifie_en_cours.py 2>&1 | tail -3; echo exit=${PIPESTATUS[0]}", "description": "Re-run doc review and state check"}`

  ```
revue de documentation · 752 fiche(s) · 845 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
  en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
exit=0
  ```

- **bash** `{"command": "python3 tools/panini_manifeste.py --verifier; echo exit=$?; python3 -m json.tool reports/panini-manifeste.json >/dev/null && echo JSON-OK", "description": "Final manifest verification"}`

  ```
OK
exit=0
JSON-OK
  ```

- **bash** `{"command": "git status --short; echo ---; git diff --stat -- docs/pilotage/en-cours.md reports/README.md; echo ---; ls -l reports/rapport-panini-manifeste.md reports/panini-manifeste.json tools/panini_manifeste.py tools/panini_signatures_26.py", "description": "Review working tree changes"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M reports/README.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 M tools/drave.py
?? reports/panini-manifeste.json
?? reports/rapport-panini-manifeste.md
?? reports/rapport-s-paragraphes.md
?? tools/panini_manifeste.py
?? tools/panini_signatures_26.py
?? tools/tests/linguistique/gold_reel_50.py
---
 docs/pilotage/en-cours.md | 6 +++---
 reports/README.md         | 1 +
 2 files changed, 4 insertions(+), 3 deletions(-)
---
-rw-r--r--. 1 stephane stephane 76435 15 nov 10:58 reports/panini-manifeste.json
-rw-r--r--. 1 stephane stephane 20716 15 nov 10:57 reports/rapport-panini-manifeste.md
-rwxr-xr-x. 1 stephane stephane 25236 15 nov 10:58 tools/panini_manifeste.py
-rwxr-xr-x. 1 stephane stephane  8936 15 nov 10:55 tools/panini_signatures_26.py
  ```

- **bash** `{"command": "git diff -- docs/pilotage/en-cours.md reports/README.md", "description": "Inspect our diffs"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 136d63e6..d2a5b8e3 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 10 h 50 HNE (W3 : la matrice du tagger)**
+**Mis à jour : 2026-11-15, 11 h 05 HNE (W4 : le manifeste Panini et le rejeu disponible)**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -90,7 +90,7 @@
 - **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.
 - **W2/W3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; défaut sans clé **code 0**, **0 socket** ; `--tagger` sans clé ou clé refusée **code 4** ; réseau coupé **code 0** + repli ; **1 000 phrases = 143 870 tokens / 0,031 $ hors pointe** ; **défaut hors ligne, opt-in, pas de `auto`** ; [W2](../../reports/rapport-tagger-h50.md), [W3](../../reports/rapport-tagger-defaut.md).
 - **Panini** : **14 atomes** ; UDHR **418/438** ; J3.2 **5/21** langues (Glottolog **21/21**), **154/154** hors script au hasard, **V
… [3618 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' tools/verifie_etat_a_jour.py", "description": "Inspect state freshness check"}`

  ```
#!/usr/bin/env python3
"""verifie_etat_a_jour.py — aucun fait commité sans sa ligne d'état.

POURQUOI CET OUTIL EXISTE. `en-cours` est la seule source de l'état, et le contrat
disait « seul le principal écrit ». Ce n'est pas une garantie : l'identité se déduit
d'une variable d'environnement absente — un « pair » est autodéclaré — et si la
principale s'arrête, l'état se fige. Surtout, rien ne comparait les commits : la
revue ne regardait que la DATE, donc deux commits du même jour passaient. Le 29/10,
A8.0 (15 h 51) a été commité après le dernier état (15 h 34) sans aucune alerte.

La garantie est au commit, pas dans la discipline d'un écrivain :
  --index  (hook pre-commit) : un commit qui prépare un fait (reports/, roadmap,
           backlog) sans toucher `en-cours` est REFUSÉ ;
  --head   : si un fait a été commité après le dernier commit d'`en-cours`, l'état
           est en retard — la session qui le voit le corrige, sans attendre.

Le journal est du récit dérivé (le hook l'archive) : il n'exige pas de ligne d'état.

Usage :
  python3 tools/verifie_etat_a_jour.py             # --head
  python3 tools/verifie_etat_a_jour.py --index     # pour le hook
  python3 tools/verifie_eta
… [6867 caractères tronqués]
  ```

- **bash** `{"command": "git add reports/rapport-panini-manifeste.md reports/panini-manifeste.json tools/panini_manifeste.py tools/panini_signatures_26.py reports/README.md docs/pilotage/en-cours.md\npython3 tools/verifie_etat_a_jour.py --index; echo index=$?\ngit diff --cached --stat", "description": "Stage W4 … [29 caractères tronqués]`

  ```
✅ index : aucun fait stagé sans état
index=0
 docs/pilotage/en-cours.md           |    6 +-
 reports/README.md                   |    1 +
 reports/panini-manifeste.json       | 2947 +++++++++++++++++++++++++++++++++++
 reports/rapport-panini-manifeste.md |  291 ++++
 tools/panini_manifeste.py           |  572 +++++++
 tools/panini_signatures_26.py       |  211 +++
 6 files changed, 4025 insertions(+), 3 deletions(-)
  ```

- **bash** `{"command": "git commit -m \"SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE\" -m \"Le manifeste reports/panini-manifeste.json liste les 26 textes du protocole B1 sans signature analytic_sigs_v1 (dont 1 seul … [767 caractères tronqués]`

  ```
[stderr]
  ✅ index : aucun fait stagé sans état
[still running after 60000ms; moved to background job bash-105]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-105", "wait": true, "timeout_ms": 120000}`

  ```
create mode 100644 journal/2026-11-15/memoire.md
 create mode 100644 reports/panini-manifeste.json
 create mode 100644 reports/rapport-panini-manifeste.md
 create mode 100755 tools/panini_manifeste.py
 create mode 100755 tools/panini_signatures_26.py
  état · dernier fait e283d09a · dernier état e283d09a
  ✅ aucun fait commité après le dernier état
head=0
e283d09a SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE
be3f41ad SEMAINE 2 — W3 : LA MATRICE DU TAGGER (DÉFAUT HORS LIGNE CODE 0, CLÉ INVALIDE 4, RÉSEAU COUPÉ 0 APRÈS 3 ESSAIS, 1 000 PHRASES = 143 870 TOKENS) ; 4 TESTS DE PLUS
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "git show --stat --oneline HEAD | head -30; echo ---; git status --short | head -30", "description": "Inspect W4 commit contents"}`

  ```
e283d09a SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE
 docs/pilotage/en-cours.md                          |    6 +-
 journal/2026-11-15/README.md                       |    6 +-
 journal/2026-11-15/distribue.md                    |    2 +-
 journal/2026-11-15/docs.md                         |    2 +-
 journal/2026-11-15/memoire.md                      |   25 +
 journal/2026-11-15/mesures.md                      |    2 +-
 journal/2026-11-15/modele.md                       |    2 +-
 journal/2026-11-15/outils.md                       |    2 +-
 journal/2026-11-15/portes.md                       |    2 +-
 journal/README.md                                  |    4 +-
 journal/THEMES.md                                  |    1 +
 journal/sessions/MANIFEST.md                       |    6 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   14 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 1472 ++++++++++
 .../rapport.md                                     |   42 +-
 reports/README.md                                  |
… [806 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -4; echo exit=${PIPESTATUS[0]}", "description": "Doc review after commit"}`

  ```
revue de documentation · 752 fiche(s) · 845 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
  ```

- **bash** `{"command": "python3 tools/panini_manifeste.py --verifier; echo exit=$?; python3 tools/protocole_date.py --verifier >/tmp/v.out 2>&1; echo proto=$?; tail -1 /tmp/v.out", "description": "Post-commit verification"}`

  ```
OK
exit=0
proto=0
paires : 60 ; textes : 59 ; à signer : 26
  ```

- **bash** `{"command": "cd ../Panini && git status --short -- research/src/nipada/signing research/nipada/falsification research/nipada/corpus/_cache/sources | head -20; echo '---'; find research/src/nipada/signing -name '__pycache__' -newermt '2026-11-15 10:50' 2>/dev/null | head", "description": "Check no Pa … [21 caractères tronqués]`

  ```
---
  ```

- **bash** `{"command": "python3 - <<'PY'\np='reports/rapport-panini-manifeste.md'\ns=open(p).read()\ns=s.replace('''\"sources\": {\"…\": {\"fichier\": \"nipada/corpus/_cache/sources/….txt\", \"sha256\": \"…\", \"mots\": 0, \"seuil_300\": true}},''','''\"sources\": {\"…\": {\"fichier\": \"nipada/corpus/_cache/s … [206 caractères tronqués]`

  ```
157:  "sources": {"…": {"fichier": "nipada/corpus/_cache/sources/….txt", "sha256": "…", "mots": 770, "seuil_300": true}},
  ```

- **bash** `{"command": "git add reports/rapport-panini-manifeste.md && git commit --amend --no-edit | tail -5; echo exit=${PIPESTATUS[0]}; git log --oneline -1", "description": "Amend W4 commit with fiche fix"}`

  ```
exit=1
e283d09a SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE
[stderr]
  ❌ commit refusé : 1 fait(s) stagé(s) sans docs/pilotage/en-cours.md
     · reports/rapport-panini-manifeste.md
     → mettre l'état à jour, puis `git add docs/pilotage/en-cours.md`
  ⛔ commit refusé : un fait sans ligne d'état.
     mets docs/pilotage/en-cours.md à jour, puis :
     git add docs/pilotage/en-cours.md
  ```

- **bash** `{"command": "python3 - <<'PY'\np='docs/pilotage/en-cours.md'\ns=open(p).read()\ns=s.replace('**Mis à jour : 2026-11-15, 11 h 05 HNE (W4 : le manifeste Panini et le rejeu disponible)**','**Mis à jour : 2026-11-15, 11 h 10 HNE (W4 : le manifeste Panini et le rejeu disponible)**')\nopen(p,'w').write(s) … [278 caractères tronqués]`
