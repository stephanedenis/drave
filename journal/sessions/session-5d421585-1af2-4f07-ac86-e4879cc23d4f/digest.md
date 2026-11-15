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
