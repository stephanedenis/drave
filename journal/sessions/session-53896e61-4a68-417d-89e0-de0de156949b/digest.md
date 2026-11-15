# Session DSH — relecture

- identifiant : `session-53896e61-4a68-417d-89e0-de0de156949b`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 04:53:45
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche D2 : la restitution v2 — au-delà de la surface exacte (v0) et de la forme canonique (v1), restitue les **rôles** (agent, prédicat, lieu) dans une forme lisible et mesure la fidélité des rôles sur les 46 textes de la v0 ; fiche `reports/rapport-restitution-v2.md` + JSON, tests, commit. Si les rôles ne se restituent pas, écris le négatif.

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

- **bash** `{"command": "pwd && ls -la && git status --short | head -50 && git log --oneline -10", "description": "Inspect workspace root and git state"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138  6 nov 10:08 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   198 15 nov 04:53 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 01:33 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 77310 15 nov 04:44 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [3128 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/ 2>/dev/null | head -60; echo \"---\"; ls -la data/ 2>/dev/null | head -40", "description": "List reports and data directories"}`

  ```
total 27932
drwxr-xr-x. 1 stephane stephane   77310 15 nov 04:44 .
drwxr-xr-x. 1 stephane stephane     686  6 nov 09:52 ..
drwxr-xr-x. 1 stephane stephane     102 24 oct 15:52 07
-rw-r--r--. 1 stephane stephane    4447 28 oct 09:17 07-mesures-couche-commune.md
-rw-r--r--. 1 stephane stephane     907 29 oct 16:25 a26-bilan.json
-rw-r--r--. 1 stephane stephane    1163  1 nov 20:40 a26-lot-disque.json
-rw-r--r--. 1 stephane stephane    1121 30 oct 08:57 a80-audit-final.json
-rw-r--r--. 1 stephane stephane     560 30 oct 00:04 a80-indice-qualifie.json
-rw-r--r--. 1 stephane stephane     672 29 oct 23:42 a80-melange-qualifie.json
-rw-r--r--. 1 stephane stephane     430 30 oct 08:57 a80-pannes-ppl.json
-rw-r--r--. 1 stephane stephane     630 29 oct 17:07 a80-porte-adaptateur.json
-rw-r--r--. 1 stephane stephane     521 29 oct 16:40 a80-porte-budget.json
-rw-r--r--. 1 stephane stephane     625 29 oct 22:07 a80-porte-bus.json
-rw-r--r--. 1 stephane stephane     654 29 oct 22:19 a80-porte-bus-socket.json
-rw-r--r--. 1 stephane stephane     677 29 oct 21:05 a80-porte-c4-retard.json
-rw-r--r--. 1 stephane stephane     600 29 oct 20:06 a80-porte-consolidation.json
-rw-r--r--. 1 stephane stepha
… [6033 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"restitution\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md 2>/dev/null | head -60; echo \"===\"; ls reports | grep -i restitut | head -50", "description": "Find restitution references in state and reports"}`

  ```
docs/pilotage/en-cours.md:64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)) ; **D1** ([fiche](../../reports/rapport-exemples-tagger.md)).
docs/pilotage/en-cours.md:90:- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejeté** (g017 à trancher), schéma v2, restitution v1 (46/46, strict 0,1087), **J9.1** (19 fiches), **D1** ; [s065](../../reports/rapport-s065.md), [restitution v1](../../reports/rapport-restitution-v1.md), [J9.1](../../reports/rapport-passe-honnetete.md).
docs/pilotage/en-cours.md:121:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 + convention GV (0,7902), s065 (238/239), g017 rejeté, schéma v2,
… [7270 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"restitution\" tools/ reports/ docs/ 2>/dev/null | head -80", "description": "Locate all restitution-related files"}`

  ```
tools/__pycache__/udhr_commun.cpython-313.pyc
tools/__pycache__/restitution_udhr.cpython-313.pyc
tools/__pycache__/decoupage_familles.cpython-313.pyc
tools/__pycache__/carte_chantiers.cpython-313.pyc
tools/__pycache__/mesurer_restitution_v0.cpython-313.pyc
tools/__pycache__/mesurer_restitution_v1.cpython-313.pyc
tools/__pycache__/restitution.cpython-313.pyc
tools/__pycache__/drave.cpython-313.pyc
tools/udhr_commun.py
tools/restitution_udhr.py
tools/decoupage_familles.py
tools/jeux/lexique.py
tools/jeux/codecs/base.py
tools/jeux/codecs/__pycache__/base.cpython-313.pyc
tools/jeux/__pycache__/mesure.cpython-313.pyc
tools/jeux/__pycache__/lexique.cpython-313.pyc
tools/jeux/mesure.py
tools/jeux/tests/test_codecs.py
tools/jeux/tests/__pycache__/test_codecs.cpython-313.pyc
tools/semantique/__pycache__/restitution.cpython-313.pyc
tools/semantique/restitution.py
tools/cerveau/tests/__pycache__/test_restitution.cpython-313.pyc
tools/cerveau/tests/test_multilingue.py
tools/cerveau/tests/test_restitution.py
tools/cerveau/hub.py
tools/cerveau/__pycache__/restitution.cpython-313.pyc
tools/cerveau/__pycache__/hub.cpython-313.pyc
tools/cerveau/restitution.py
tools/tests/documents/bench-complet.jso
… [1791 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,240p' tools/mesurer_restitution_v0.py", "description": "Read v0 restitution measurement script"}`

  ```
#!/usr/bin/env python3
"""mesurer_restitution_v0.py — produit le JSON de la fiche J1.4.

Mesure la restitution v0 sur les **50 textes libres** de
`reports/pensee-fiabilite-produit.json` (le banc de l'audit A26) et écrit
`reports/pensee-restitution-v0.json`. La fiche `reports/rapport-restitution-v0.md`
cite ce JSON.

    python3 tools/mesurer_restitution_v0.py
"""
from __future__ import annotations

import datetime
import hashlib
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

import tools.restitution as restitution  # noqa: E402

BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
SORTIE = RACINE / "reports" / "pensee-restitution-v0.json"

LIMITES = [
    "4 refus sans annotation (f14 emoji, f15 vide, f16 espaces, f17 « ... ») : "
    "la surface n'est pas reconstructible, ils sont comptés à part.",
    "La fidélité binaire du miroir compare la sortie à la source exacte : la ponctuation "
    "séparée des mots fait tomber mots et POS à 5/46, alors que la fidélité de caractères "
    "reste à 0,9506. Les deux mesures disent des choses différentes.",
    "La sur
… [2327 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,280p' tools/mesurer_restitution_v1.py", "description": "Read v1 restitution measurement script"}`

  ```
#!/usr/bin/env python3
"""mesurer_restitution_v1.py — produit le JSON de la fiche J8.1.

Mesure la **forme canonique v1** sur les **50 textes libres** de
`reports/pensee-fiabilite-produit.json` (le banc de l'audit A26) et écrit
`reports/pensee-restitution-v1.json`. La fiche `reports/rapport-restitution-v1.md`
cite ce JSON.

La v1 ne remplace pas la v0 : elle ajoute une lecture **structurelle** (segments +
rôles + cibles) et un **miroir canonique** comparé à une source canonisée. Le miroir
strict (surface brute) reste mesuré, pour que la réponse à « doit-il monter ? » soit
vérifiable.

    python3 tools/mesurer_restitution_v1.py
"""
from __future__ import annotations

import datetime
import hashlib
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

import tools.restitution as restitution  # noqa: E402

BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
SORTIE = RACINE / "reports" / "pensee-restitution-v1.json"

LIMITES = [
    "Le miroir canonique vaut 1,0000 **par construction** : les jetons viennent des "
    "spans `mot`/`pos`, qui sont des sous-chaînes de la 
… [3239 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,320p' tools/restitution.py", "description": "Read restitution module part 1"}`

  ```
"""restitution.py — la restitution v0 (surface) et la v1 (forme canonique).

La **surface** est reconstruite depuis le niveau `graphème` — les spans typés qui portent
les caractères — **sans lire** `Annotation.texte`. Les niveaux `mot` et `pos` sont mesurés
comme des sorties plus pauvres : ils disent ce que la couche de surface ajoute.

Le **miroir** est la règle 6 du dépôt : `fidelite` est binaire (1.0 si la sortie égale la
source), et `miroir` est le minimum des trois fidélités (surface, mots, pos). C'est la
définition de `tools/tests/linguistique/miroir.mesurer`, réutilisée ici pour ne pas en
avoir deux. `fidelite_caractere` ajoute une distance de Levenshtein normalisée : elle
distingue « presque fidèle » de « fidèle » et documente la perte de la ponctuation.

La **forme canonique** (v1) est une lecture **structurelle** de l'annotation : les
syntagmes avec leur type, leur rôle et leur cible d'attachement, une linéarisation sans
chevauchement, et un plancher de jetons normalisés (casse repliée, ponctuation retirée).
Elle ne remplace pas la surface : elle la met entre parenthèses pour mesurer ce que la
structure ajoute, et son **miroir canonique** se compare à une source canonisée
… [11512 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '320,760p' tools/restitution.py", "description": "Read restitution module part 2"}`

  ```
[r["controle_negatif"]["melange"]["fidelite"] for r in annotes]),
            "melange_fidelite_caractere": _moyenne(
                [r["controle_negatif"]["melange"]["fidelite_caractere"] for r in annotes]),
            "tronque_exacts": sum(
                1 for r in annotes if r["controle_negatif"]["tronque"]["exact"]),
            "tronque_fidelite_caractere": _moyenne(
                [r["controle_negatif"]["tronque"]["fidelite_caractere"] for r in annotes]),
            "detectes": sum(1 for r in annotes if r["controle_negatif"]["detecte"]),
        },
    }


def mesurer_banc(items: list[dict], langue: str | None = None, graine: int = 0) -> dict:
    """Mesure la restitution sur une liste de textes (`id`, `texte`, `langue` optionnelle).

    `langue=None` laisse le bloc détecter, comme le CLI sans `--langue` — c'est la
    condition du banc des 50 textes libres.
    """
    h = bl.Heuristique()
    resultats: list[dict] = []
    for item in items:
        texte = item.get("texte", "")
        ident = item.get("id", f"t{len(resultats) + 1:02d}")
        a = h.analyser(texte, langue)
        if a.refus:
            resultats.append({
                "id": ident,
            
… [17253 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '760,1160p' tools/restitution.py", "description": "Read restitution module part 3"}`

  ```
"refus_ids": [r.get("id") for r in refuses],
        "strict": {
            "exacts": sum(1 for r in annotes if r["strict"]["exact"]),
            "fidelite": moyenne([r["strict"]["fidelite"] for r in annotes]),
        },
        "canonique": {
            "exacts": sum(1 for r in annotes if r["canonique"]["exact"]),
            "fidelite": moyenne([r["canonique"]["fidelite"] for r in annotes]),
            "fidelite_caractere": moyenne(
                [r["canonique"]["forme"]["fidelite_caractere"] for r in annotes]),
        },
        "strict_sur_canonique": {
            "exacts": sum(1 for r in annotes if r["strict_sur_canonique"]["exact"]),
            "fidelite": moyenne(
                [r["strict_sur_canonique"]["fidelite"] for r in annotes]),
            "fidelite_caractere": moyenne(
                [r["strict_sur_canonique"]["fidelite_caractere"] for r in annotes]),
        },
        "structure": structure,
        "stabilite": {
            "squelette_identique": sum(
                1 for r in annotes if r["stabilite"]["squelette_identique"]),
            "jetons_identiques": sum(
                1 for r in annotes if r["stabilite"]["jetons_identiques"]),
         
… [12525 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"D2\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md tools/chantier/plan.json 2>/dev/null | head -60", "description": "Find D2 task in planning docs"}`

  ```
docs/pilotage/roadmap.md:56:D1–D20, rejets R1–R30, échecs, reste — est dans
tools/chantier/plan.json:518:   "id": "D2",
tools/chantier/plan.json:521:   "mandat": "Tâche D2 : la restitution v2 — au-delà de la surface exacte (v0) et de la forme canonique (v1), restitue les **rôles** (agent, prédicat, lieu) dans une forme lisible et mesure la fidélité des rôles sur les 46 textes de la v0 ; fiche `reports/rapport-restitution-v2.md` + JSON, tests, commit. Si les rôles ne se restituent pas, écris le négatif.",
  ```

- **bash** `{"command": "sed -n '1,220p' reports/rapport-restitution-v1.md", "description": "Read v1 report"}`

  ```
# B13 — la restitution v1 : la forme canonique à 46/46, le miroir strict reste à 0,1087

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : J8.1 · **Date** : 2026-11-14 ·
> **Verdict** : ✅
>
> **La question.** Au-delà de la surface exacte (46/46), produire une **forme canonique**
> depuis l'annotation — **segments + rôles + cibles** — et la mesurer : le **miroir strict**
> (0,1087) doit-il monter ?
>
> **La réponse.** **Non — et il ne doit pas.** Le miroir strict compare une sortie à la
> **surface brute** ; la forme canonique replie la casse, retire la ponctuation et réduit
> les espaces. Contre la source canonisée, elle est exacte **46/46 = 1,0000** ; contre la
> source brute, elle tombe à **1/46 = 0,0217** (seul `f18`, `1234567890`, n'a ni casse ni
> ponctuation). Le **miroir strict reste 5/46 = 0,1087** : la v1 ne fabrique pas de
> surface, elle mesure autre chose. Le chiffre utile de la v1 est **1,0000 canonique**,
> pas 0,1087 strict.
>
> **Le chiffre.** 46 annotations, **46/46 formes canoniques exactes** contre la source
> canonisée ; **395 segments**, **395 rôles**, **315 cibles**, **315/315 cibles résolues**
> dans la source, **313/315** portées par un autre segment 
… [10168 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' reports/rapport-restitution-v0.md", "description": "Read v0 report"}`

  ```
# B13 — la restitution v0 : 46/46 surfaces exactes, le miroir strict à 0,1087

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : J1.4 · **Date** : 2026-11-07 ·
> **Verdict** : ✅
> **Ce que la commande fait** : `python3 tools/drave.py restituer TEXTE` analyse le texte,
> reconstruit la surface depuis le niveau **`graphème`** de l'annotation — **sans lire
> `Annotation.texte`** — et affiche la fidélité du **miroir** (surface, mots, POS), la fidélité
> de caractères et un **contrôle négatif**. `restituer --banc` rejoue le banc des 50 textes.
>
> **Le chiffre.** Sur les **50 textes libres** de l'audit A26 : **46 annotations** (4 refus),
> **46/46 surfaces exactes** (1,0000) ; le **miroir strict** — le minimum des fidélités
> surface/mots/POS — vaut **5/46 = 0,1087** ; le contrôle négatif casse **46/46**.
> Le miroir a trouvé un trou : `f50` perdait ses **10 sauts de ligne** (45/46, 0,9783) ;
> le correctif `C` les annote et la surface revient à 46/46.
>
> **Dispositif** : [`drave.py`](../tools/drave.py) (`restituer`, `--banc`, `--json`),
> [`restitution.py`](../tools/restitution.py) (reconstruction, Levenshtein, miroir, contrôle),
> [`bloc_linguistique.py`](../tools/bloc_linguis
… [8344 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nprint(type(p))\nif isinstance(p,dict): print(p.keys())\nPY\nsed -n '470,560p' tools/chantier/plan.json", "description": "Read D2 plan entry context"}`

  ```
<class 'dict'>
dict_keys(['nom', 'principe', 'taches'])
     "attendu": "FICHE-OK"
    }
   ]
  },
  {
   "id": "B2",
   "jour": 15,
   "titre": "Panini — les atomes et les niveaux, prédiction",
   "mandat": "Tâche B2 : les 14 atomes comme prédicteurs des 8 niveaux Drave — sur les 44 œuvres × 14 flottants (JSON plat, lecture seule chez Panini), mesure la prédiction d'un niveau (POS, syntagmes, attachement) par les atomes, avec le contrôle de permutation des colonnes et le contrôle de date ; fiche `reports/rapport-atomes-prediction.md` + JSON.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-atomes-prediction.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    }
   ]
  },
  {
   "id": "B3",
   "jour": 15,
   "titre": "Panini — le corpus d'or CIC étendu",
   "mandat": "Tâche B3 : le corpus d'or CIC (42 verdicts, 42/42 reproduits en J12.2) — étends le vérificateur : les 36 preuves altérées sont rejetées ; ajoute la vérification du **type de Bruijn** et le sha256 indépendant rejoué par une seconde implémentation ; fiche `reports/rapport-cic-v2.md` + JSON.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rappor
… [1995 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' docs/pilotage/en-cours.md", "description": "Read current state file"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 05 h 00 HNE (D1)**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs.
- **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
- **État** : **en pause** depuis le 05/11 (dernier heartbeat) ; la clôture J14.1 est portée par `e181ce02`.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état
… [11330 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn '\"role\"\\|role.*agent\\|agent.*predicat\\|predicat.*lieu' tools/*.py tools/**/*.py 2>/dev/null | head -100", "description": "Find role definitions in code"}`

  ```
tools/atomes_prediction.py:316:                roles[e["meta"].get("role", "?")] += 1
tools/bloc_linguistique.py:974:                        gn.update({"type": "GN", "role": "agent", "niveau": 0,
tools/bloc_linguistique.py:1345:                                     "role": "complément" if stype == "SUB" else "qualité",
tools/bloc_linguistique.py:1372:                segments.append({"type": "GN", "role": role, "niveau": 0,
tools/bloc_linguistique.py:1380:                    segments.append({"type": "REL", "role": "qualité", "niveau": 1,
tools/bloc_linguistique.py:1394:                segments.append({"type": "GN", "role": "agent", "niveau": 0,
tools/bloc_linguistique.py:1402:                segments.append({"type": "GN", "role": "agent", "niveau": 0,
tools/bloc_linguistique.py:1429:                segments.append({"type": "GV", "role": "prédicat", "niveau": 0,
tools/bloc_linguistique.py:1446:                segments.append({"type": "GP", "role": _role_gp(t), "niveau": 1,
tools/bloc_linguistique.py:1701:                    meta = {"role": s.get("role", ""), "niveau": s.get("niveau", 0)}
tools/bloc_linguistique.py:1724:                meta = {"role": s["role"], "niveau": s["niveau"]}

… [9114 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"agent\" data/ reports/ tools/tests/ 2>/dev/null | head -80", "description": "Find agent role references in data and tests"}`

  ```
data/wikitext2_test.txt
data/corpus_en_val.txt
data/corpus_en.txt
data/corpus_fr.txt
data/corpus_mixte.txt
data/corpus_fr_litterature.txt
data/corpus_mixte_litt.txt
data/corpus_mixte_litt2.txt
data/udhr/articles.jsonl
data/udhr/udhr_train.txt
data/udhr/articles_propres.jsonl
data/udhr/udhr_50_train.txt
data/udhr/familles/austronesian.jsonl
data/glottolog/values.csv
data/eurlex/xhtml/32025R1106-deu.xhtml
data/eurlex/xhtml/32025R1106-spa.xhtml
data/eurlex/xhtml/32025R2509-eng.xhtml
data/eurlex/xhtml/32025R2509-fra.xhtml
data/eurlex/xhtml/32025R2509-deu.xhtml
data/eurlex/xhtml/32025R2509-spa.xhtml
data/eurlex/xhtml/32025R1106-nld.xhtml
data/eurlex/xhtml/32025R1106-ces.xhtml
data/eurlex/xhtml/32025R1106-dan.xhtml
data/eurlex/xhtml/32025R1106-est.xhtml
data/eurlex/xhtml/32025R1106-lit.xhtml
data/eurlex/xhtml/32025R1106-slk.xhtml
data/eurlex/32025R1106.json
data/eurlex/32025R2509.json
data/eurlex/32025R1106-8.json
data/eurlex/32025R1106-24.json
data/alignement/verne_fr_en.json
data/presse/api/IP_26_1633-DE.json
data/presse/presse_2026.json
data/onu/pdf/A_RES_80_5-en.txt
data/onu/pdf/A_RES_80_5-fr.txt
data/onu/pdf/A_RES_80_5-es.txt
data/onu/onu_2026.json
data/jw/html/https_www_jw_org_en_l
… [1794 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,240p' tools/structures/mesure_analyseur.py", "description": "Read role measurement baseline"}`

  ```
#!/usr/bin/env python3
"""mesure_analyseur.py — le gold de l'analyseur : types, rôles, couverture, et trois contrôles.

Le gold (`donnees/gold-analyseur.json`) porte des structures **écrites à la main** : pour chaque
phrase, la suite de segments (texte, type, rôle) et son découpage `dev` / `test` / `holdout`.
La mesure compare la **structure de base** de `generateur.structure` (sans variantes) au gold :

- **types** : la séquence de types est-elle exacte ?
- **couverture** : les octets du gold sont-ils couverts par un segment généré **du même type** ?
- **rôles** : le rôle du segment généré qui recouvre le segment d'or est-il le bon ?

Trois contrôles, parce qu'un score de rôle sans contrôle ne dit rien :

1. **baseline** — un étiqueteur à rôle **constant par type** (GN=agent, GV=predicat, GP=lieu,
   SUB=contenu, REL=qualite) ; l'analyseur doit le battre ;
2. **règles coupées** — `structure(roles=False)` rend les rôles par défaut : la chute isole ce que
   les règles apportent, à segmentation égale ;
3. **rôles mélangés** — les rôles attendus des compléments sont permutés (200 tirages, graine
   fixe) : le score doit tomber au hasard, sinon la mesure ne lit pas les étiquettes.

  
… [9457 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/structures/ && sed -n '1,180p' tools/structures/construire_donnees.py", "description": "Inspect structures corpus sources"}`

  ```
total 160
drwxr-xr-x. 1 stephane stephane   438  3 nov 16:22 .
drwxr-xr-x. 1 stephane stephane 17876 15 nov 03:59 ..
-rw-r--r--. 1 stephane stephane  7469  3 nov 17:08 arbre_svg.py
-rw-------. 1 stephane stephane  4388  2 nov 20:04 candidats_corpus.py
-rw-r--r--. 1 stephane stephane  7035  2 nov 02:10 construire_donnees.py
drwxr-xr-x. 1 stephane stephane   414  3 nov 16:49 donnees
-rw-r--r--. 1 stephane stephane 11442  2 nov 16:27 exporter_corpus.py
-rw-r--r--. 1 stephane stephane 30580  4 nov 11:41 generateur.py
-rw-r--r--. 1 stephane stephane    44  1 nov 10:50 .git
-rw-r--r--. 1 stephane stephane    19  1 nov 10:50 .gitignore
-rw-r--r--. 1 stephane stephane  4963  2 nov 02:10 llm.py
-rw-------. 1 stephane stephane 11226  2 nov 16:24 mesure_analyseur.py
-rw-r--r--. 1 stephane stephane  3209  3 nov 16:23 mesure_arbre.py
-rw-------. 1 stephane stephane  8428  2 nov 19:59 mesure_corpus.py
drwxr-xr-x. 1 stephane stephane   564  4 nov 11:41 __pycache__
-rw-r--r--. 1 stephane stephane 21682  4 nov 11:42 README.md
-rw-r--r--. 1 stephane stephane 15208  3 nov 17:45 serveur.py
drwxr-xr-x. 1 stephane stephane   110  3 nov 16:35 static
drwxr-xr-x. 1 stephane stephane   240  3 nov 16:23 test
… [7007 caractères tronqués]
  ```

- **bash** `{"command": "ls reports | grep -Ei 'role|structure|analyseur' | head -60; echo ===; grep -rln '144/144\\|roles' reports/rapport-s-analyseur-roles.md reports/*.json 2>/dev/null | head -40", "description": "Find role gold reports and JSON"}`

  ```
pensee-anaphore-roles.json
pensee-roles.json
plan-controle-3b.json
rapport-consolidation-structure-partagee.md
rapport-pensee-anaphore-roles.md
rapport-pensee-roles.md
rapport-r02-controleur.md
rapport-s-analyseur.md
rapport-s-analyseur-roles.md
s-banque-structures.json
===
reports/rapport-s-analyseur-roles.md
reports/a80-porte-pont.json
reports/a83b-regimes.json
reports/a83-defaut.json
reports/atomes-niveaux.json
reports/b10-decodeur-mots.json
reports/b10-mots-contraste.json
reports/b10-mots-jw.json
reports/b1110-cartes.json
reports/bloc-linguistique.json
reports/cerveau-mesures-corrigees.json
reports/cic-verificateur.json
reports/cic-verificateur-v2.json
reports/corpus-commun.json
reports/drvm-ppl.json
reports/evaluer-langue.json
reports/genealogie-deux-faces.json
reports/m7-frequence.json
reports/n2-200k.json
reports/n2-fenetre.json
reports/n2-porte-propre.json
reports/n2-production-fenetre.json
reports/n2-r11.json
reports/n2-r12-2048.json
reports/n3.6-service-briques.json
reports/passe-honnetete.json
reports/pensee-attachement-v3.json
reports/pensee-audit-v2.json
reports/pensee-audit-v7.json
reports/pensee-bilan-nuit.json
reports/pensee-coherence-fiches.json
reports/pensee-cohe
… [292 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,260p' reports/rapport-s-analyseur-roles.md", "description": "Read role analyzer report"}`

  ```
# S — Le contexte tranche les homographes : 54/55 types, 131/131 rôles, 55 structures au corpus

> **Ligne de roadmap** : S · **Date** : 2026-11-02 · **Verdict** : sur un gold de **55 phrases**
> (7 `dev`, 16 `test`, 32 `holdout` en quatre vagues), la structure de base retrouve la **séquence
> de types 54/55** (98,2 %), les **rôles 131/131** (100 %), les **compléments 47/47**, et couvre
> **1 466/1 475 octets** (99,4 % ; holdout **762/771**, 98,8 %). La **règle de contexte** corrige
> les homographes `h046` (« ferme ») et `h047` (« fait ») : un mot du lexique de verbes est un
> **nom** si le suivant est un auxiliaire ou un autre verbe. La **limite nommée** se déplace :
> `h050` (« fait » suivi d'un verbe **hors lexique**) et `h053` (« lit » après un adjectif, en
> fin de phrase). Le corpus de référence sort : **55 lignes**, SHA-256
> `76accf9dbd60a9fcc9fe58a56eecbdbb6aec0ffd5e8dbf0c69443e4a49dd1ac6`.

## Le dispositif

- **Gold** : [`tools/structures/donnees/gold-analyseur.json`](../tools/structures/donnees/gold-analyseur.json),
  **55 phrases** : **7 `dev`**, **16 `test`**, **32 `holdout`** en quatre vagues : `h024–h031`
  (première règle), `h032–h039` (copule), `h040–h047` (front
… [7001 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/structures/donnees/; echo ===; for f in tools/structures/donnees/*.json; do echo \"--- $f\"; python3 -c \"import json,sys; d=json.load(open('$f')); print(type(d), list(d)[:10] if isinstance(d,dict) else len(d))\"; done", "description": "Inspect structures gold data"}`

  ```
total 636
drwxr-xr-x. 1 stephane stephane    414  3 nov 16:49 .
drwxr-xr-x. 1 stephane stephane    438  3 nov 16:22 ..
-rw-------. 1 stephane stephane  16806  4 nov 11:42 gold-analyseur.json
-rw-r--r--. 1 stephane stephane    659  3 nov 12:36 llm.jsonl
-rw-r--r--. 1 stephane stephane  21646  4 nov 11:42 mesure-analyseur.json
-rw-r--r--. 1 stephane stephane    886  3 nov 16:23 mesure-arbre.json
-rw-r--r--. 1 stephane stephane   5099  3 nov 18:36 mesure-corpus.json
-rw-r--r--. 1 stephane stephane   7217  4 nov 09:44 paragraphes.json
-rw-r--r--. 1 stephane stephane   6047  4 nov 15:10 paragraphes-validations.jsonl
-rw-r--r--. 1 stephane stephane    366  2 nov 20:35 phrases-corpus-manifest.json
-rw-r--r--. 1 stephane stephane 527440  2 nov 20:35 phrases_generees.json
-rw-r--r--. 1 stephane stephane  12115  2 nov 02:10 phrases.json
-rw-r--r--. 1 stephane stephane  25828  3 nov 16:46 validations.jsonl
===
--- tools/structures/donnees/gold-analyseur.json
<class 'dict'> ['version', 'note', 'segments', 'phrases']
--- tools/structures/donnees/mesure-analyseur.json
<class 'dict'> ['gold', 'date', 'phrases', 'par_split', 'global', 'controles', 'lignes']
--- tools/structures/donnees/mesure-arbr
… [792 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='reports/pensee-fiabilite-produit.json'\nd=json.load(open(p))\nprint(type(d), d.keys() if isinstance(d,dict) else len(d))\nif isinstance(d,dict):\n    for k,v in d.items():\n        print(k, type(v), (list(v)[:10] if isinstance(v,dict) else len(v) if has … [77 caractères tronqués]`

  ```
<class 'dict'> dict_keys(['rapport', 'ligne', 'branche', 'commit_mesure', 'commit_module', 'date', 'objet', 'verdict', 'snapshot', 'dispositif', 'banc_50', 'robustesse', 'contrat', 'schema_propose', 'test_non_regression', 'correctifs', 'controle_negatif', 'limites', 'fichiers'])
rapport <class 'str'> 17
ligne <class 'str'> 3
branche <class 'str'> 4
commit_mesure <class 'str'> 8
commit_module <class 'str'> 8
date <class 'str'> 10
objet <class 'str'> 166
verdict <class 'str'> 226
snapshot <class 'dict'> ['drave_py_sha256', 'bloc_linguistique_sha256', 'bloc_linguistique_git', 'module_change_pendant_audit', 'note']
dispositif <class 'dict'> ['banc_50', 'mesure', 'machine', 'harnais', 'controle_negatif']
banc_50 <class 'dict'> ['synthese', 'resultats']
robustesse <class 'dict'> ['synthese', 'cas']
contrat <class 'dict'> ['enveloppe_actuelle', 'etiquette_actuelle', 'invariants_tenus', 'peut_etre_vide', 'ce_qui_casse_un_client']
schema_propose <class 'dict'> ['schema', 'version', 'champs_cles', 'champs_optionnels', 'json_schema', 'politique_de_version']
test_non_regression <class 'dict'> ['fichier_propose', 'statut', 'integration', 'code']
correctifs <class 'dict'> ['bloquants', 'importan
… [173 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nitems=d['banc_50']['resultats']\nprint(len(items))\nfor it in items:\n    print(it.get('id'), repr(it.get('texte')), it.get('langue'))\nPY", "description": "List the 50 v0 texts"}`

  ```
50
f01 'Le chat dort.' fr
f02 'Le chat de la voisine qui dort sur le toit se réveille.' fr
f03 "Bonjour ! Comment allez-vous aujourd'hui ?" fr
f04 "Ferme la porte, s'il te plaît." fr
f05 'Ne touche pas à ça !' fr
f06 "Je ne pense pas qu'il viendra demain, mais nous verrons bien." fr
f07 'The cat sleeps on the roof.' en
f08 'Where is the nearest train station, please?' en
f09 "Don't forget to bring your passport." en
f10 'Le prix est de 1 234,56 € pour 3 articles.' fr
f11 'Rendez-vous le 12/03/2026 à 14h30.' fr
f12 'Visitez https://example.com/docs?page=2 pour la documentation.' fr
f13 "J'ai trouvé ça génial 😍🔥" und
f14 '🚀' None
f15 '' None
f16 '   ' None
f17 '...' None
f18 '1234567890' und
f19 "COVID-19 : la situation s'améliore-t-elle vraiment ?" fr
f20 'M. Dupont, le Dr Martin et Mme Leroy sont arrivés vers 9 h.' fr
f21 '« Je ne sais pas », répondit-il en haussant les épaules.' fr
f22 "C'est l'été ; les oiseaux chantent, les enfants jouent." fr
f23 'Attention : ce produit peut contenir des traces de noisettes.' fr
f24 'Il était une fois une petite fille qui vivait au bord de la forêt...' fr
f25 'Pourquoi ? Parce que.' fr
f26 'Où sont les toilettes ? Je cherche depuis dix minutes.
… [3956 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '930,1030p' tools/bloc_linguistique.py; echo '---'; sed -n '1320,1470p' tools/bloc_linguistique.py; echo '---'; sed -n '1680,1770p' tools/bloc_linguistique.py", "description": "Read role generation in linguistic block"}`

  ```
for s in segs:
                if s.get("type") != "GV":
                    sortie.append(s)
                    continue
                d, f = s.get("debut", 0), s.get("fin", 0)
                mots = [(d + a, d + b, t, typ) for a, b, t, typ in self._mots(texte[d:f])]
                if len(mots) < 2:
                    sortie.append(s)
                    continue
                # un GN sujet précède immédiatement : le GV est déjà conforme
                if any(x.get("type") == "GN" and x.get("fin", 0) <= d
                       and not texte[x.get("fin", 0):d].strip() for x in segs):
                    sortie.append(s)
                    continue
                n0 = _normaliser(mots[0][2])
                n0e = _elisions.get(n0.split("'")[0], n0)
                # le prédicat peut commencer par un clitique élidé (« elle s'ouvre »,
                # « il l'aime ») : on saute le clitique pour trouver le verbe, mais le GV
                # commence au clitique (il en fait partie).
                k = 1
                while k < len(mots) and _normaliser(mots[k][2]) in _clitiques:
                    k += 1
                if k >= len(mots):
                    sortie.appen
… [19305 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln '\"f01\"\\|f01' reports tools data 2>/dev/null | head -60", "description": "Find role gold for bench ids"}`

  ```
reports/corpus-wiki-fr.json
reports/corpus-wiki-zh.json
reports/corpus-wiki-de-texte.json
reports/ocr-pdf-cegep-detection.json
reports/rapport-produit-bloc-l.md
reports/pensee-produit-bloc-l.json
reports/pensee-fiabilite-produit.json
reports/rapport-fiabilite-produit.md
reports/pensee-restitution-v0.json
reports/corpus-commun.json
reports/pensee-restitution-v1.json
reports/rapport-restitution-v1.md
reports/pensee-robustesse-semaine.json
tools/__pycache__/verificateur_cic.cpython-313.pyc
tools/docwatch/tests/__pycache__/test_diagrams.cpython-313-pytest-9.1.1.pyc
tools/docwatch/tests/__pycache__/test_diagrams.cpython-313.pyc
tools/docwatch/tests/test_diagrams.py
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/utils/glibc.py
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/_manylinux.py
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/unistring.py
tools/docwatch/.venv/lib/python3.13/site-packages/urllib3/connection.py
tools/docwatch/.venv/lib/python3.13/site-packages/ruff-0.17.3.dist-info/sboms/ruff.cyclonedx.json
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/unistring.py
tools/docwatch/.venv/lib/python3.13/site
… [1888 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn 'role.*agent\\|\"agent\"' reports/*.json 2>/dev/null | head -60", "description": "Search role agent in report JSONs"}`

  ```
reports/cerveau-mesures-corrigees.json:9266:   "agent": "A5",
reports/pensee-gold-anglais.json:920:    "agent": 12,
reports/pensee-inventaire-panini.json:345:      "role": "journal d'agents",
reports/pensee-inventaire-panini.json:452:        "role": "agent, experienceur",
reports/pensee-passifs-corriges.json:5: "role_gp": "agent (corrigé)",
reports/pensee-passifs.json:7: "roles_obtenus": "agent/moyen",
reports/pensee-passifs.json:8: "roles_attendus": "patient/agent",
reports/pensee-passifs-sans-par.json:7: "annotation": "agent",
reports/pensee-relation.json:7:  "agent": 260,
reports/pensee-restitution-v1.json:131:      "role": "agent",
reports/pensee-restitution-v1.json:180:     "agent": 1,
reports/pensee-restitution-v1.json:282:      "role": "agent",
reports/pensee-restitution-v1.json:386:     "agent": 1,
reports/pensee-restitution-v1.json:508:      "role": "agent",
reports/pensee-restitution-v1.json:577:     "agent": 1,
reports/pensee-restitution-v1.json:1024:      "role": "agent",
reports/pensee-restitution-v1.json:1099:      "role": "agent",
reports/pensee-restitution-v1.json:1160:     "agent": 2,
reports/pensee-restitution-v1.json:1713:      "role": "agent",
reports/pensee-res
… [2449 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' reports/rapport-pensee-roles.md; echo ===; python3 - <<'PY'\nimport json\nfor p in ['reports/pensee-roles.json','reports/pensee-anaphore-roles.json']:\n d=json.load(open(p)); print(p, type(d), list(d)[:20] if isinstance(d,dict) else len(d))\nPY", "description": "Read tho … [27 caractères tronqués]`

  ```
# B13 — les 322 GN sans rôle : 129 avant le GV, 172 après

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-04 · **Verdict** : ✅
> **160/160 portes** : les **322 GN sans rôle** sont **301 avec un GV** ; la **position** tranche :
> **129 avant** le GV (sujet probable → `agent`), **172 après** (objet probable → `patient`).
> La règle de position rend la relation GN → GV **calculable pour 301 GN** au lieu de 221
> (0,3469 → 0,4725).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-roles.json`](pensee-roles.json).

## 1. La position

| mesure | GN | part |
|---|---:|---:|
| GN sans rôle | **322** | 100 % |
| dont avec un GV | **301** | 93,5 % |
| **avant le GV** (sujet probable) | **129** | 40,0 % |
| **après le GV** (objet probable) | **172** | 53,4 % |

| relation | avant | **après la règle de position** |
|---|---:|---:|
| GN avec rôle et un GV | 221 (0,3469) | **301 + 221 = 522 (0,8195)** |

**Ce que ça dit** :

- **La position est un signal fort** : 129 GN avant le GV (sujet), 172 après (obje
… [1919 caractères tronqués]
  ```

- **job_list** `{}`

  ```
bash-25 [bash] running — grep -rln '"f01"\|f01' reports tools data 2>/dev/null | head -60
  ```

- **job_kill** `{"job_id": "bash-25", "reason": "grep trop large terminé, résultats déjà obtenus"}`

  ```
requested cancellation of job bash-25
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, collections\nd=json.load(open('reports/pensee-restitution-v1.json'))\nfor r in d['resultats']:\n    if r.get('refus'):\n        print(r['id'], 'REFUS', r['refus']); continue\n    f=r.get('forme') or {}\n    segs=f.get('segments') or []\n    roles=collectio … [313 caractères tronqués]`

  ```
f01   13 segs= 2 roles={'agent': 1, 'predicat': 1}
    GN /agent        'Le chat' -> 'dort' lin=True
    GV /predicat     'dort' -> 'chat' lin=True
f02   55 segs= 5 roles={'agent': 1, 'possession': 1, 'qualite': 1, 'qualité': 1, 'predicat': 1}
    GN /agent        'Le chat' -> 'réveille' lin=True
    GP /possession   'de la voisine' -> 'réveille' lin=True
    REL/qualite      'qui dort sur le toit' -> 'voisine' lin=False
    REL/qualité      'qui dort sur le toit se réveille' -> 'réveille' lin=True
    GV /predicat     'se réveille' -> 'voisine' lin=False
f03   42 segs= 4 roles={'predicat': 2, 'agent': 1, 'temps': 1}
    GV /predicat     'Bonjour' -> '' lin=True
    GN /agent        'Comment' -> 'allez' lin=True
    GV /predicat     'allez-vous' -> '' lin=True
    GP /temps        "aujourd'hui" -> 'allez' lin=True
f04   30 segs= 3 roles={'predicat': 1, 'patient': 1, 'hypothese': 1}
    GV /predicat     'Ferme' -> '' lin=True
    GN /patient      'la porte' -> 'Ferme' lin=True
    SUB/hypothese    "s'il te plaît" -> 'porte' lin=True
f05   20 segs= 3 roles={'predicat': 1, 'destinataire': 1, 'patient': 1}
    GV /predicat     'Ne touche pas' -> '' lin=True
    GP /destinataire 'à ça' 
… [24585 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/tests/linguistique/; echo ===; find tools/tests/linguistique -maxdepth 1 -type f -printf '%f\\n' | sort", "description": "List linguistic tests and gold files"}`

  ```
total 1524
drwxr-xr-x. 1 stephane stephane    916 15 nov 03:46 .
drwxr-xr-x. 1 stephane stephane    974 15 nov 03:58 ..
-rw-r--r--. 1 stephane stephane  16090  2 nov 09:26 anaphore.py
-rw-r--r--. 1 stephane stephane  35148  5 nov 14:25 classement_cible.py
-rw-r--r--. 1 stephane stephane   6231  7 nov 13:02 classer_gv.py
-rw-r--r--. 1 stephane stephane  15762  6 nov 19:50 evaluer_gold.py
-rw-r--r--. 1 stephane stephane 450905  2 nov 13:27 gold_gele.json
-rw-r--r--. 1 stephane stephane  20009 15 nov 03:54 gold.json
-rw-r--r--. 1 stephane stephane   7813  2 nov 12:03 gold.py
-rw-r--r--. 1 stephane stephane  29924 15 nov 02:45 gold_reel_50.py
-rw-r--r--. 1 stephane stephane 470149  2 nov 14:39 gold_reel.json
-rw-r--r--. 1 stephane stephane 132934  5 nov 14:04 gold_reel.py
-rw-r--r--. 1 stephane stephane   1939  5 nov 17:52 gold_split.py
-rw-r--r--. 1 stephane stephane 149211  6 nov 18:56 gold_synthetique.json
-rw-r--r--. 1 stephane stephane  10222  6 nov 18:55 gold_synthetique.py
-rw-r--r--. 1 stephane stephane   2953  2 nov 12:17 juge.py
-rw-r--r--. 1 stephane stephane  22366  3 nov 14:05 miroir.py
drwxr-xr-x. 1 stephane stephane   1040 15 nov 03:46 __pycache__
-rw-------. 1 stephane 
… [1285 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn 'role\\|agent\\|lieu' tools/tests/linguistique/*.py tools/tests/linguistique/*.json 2>/dev/null | head -100", "description": "Search role gold in linguistic tests"}`

  ```
tools/tests/linguistique/anaphore.py:42:ROLES_SUJET = ("agent",)
tools/tests/linguistique/anaphore.py:51:def resoudre_roles(mots: list[dict], segments: list[dict]) -> dict[str, str]:
tools/tests/linguistique/anaphore.py:52:    """Résout les pronoms par le **rôle du segment** : sujet → agent, objet → patient."""
tools/tests/linguistique/anaphore.py:53:    agent = patient = None
tools/tests/linguistique/anaphore.py:58:        if seg.get("role") in ROLES_SUJET:
tools/tests/linguistique/anaphore.py:59:            agent = nom
tools/tests/linguistique/anaphore.py:60:        elif seg.get("role") in ROLES_OBJET:
tools/tests/linguistique/anaphore.py:69:        elif texte in SUJETS and agent is not None and texte not in vus:
tools/tests/linguistique/anaphore.py:70:            liens[texte] = agent
tools/tests/linguistique/anaphore.py:91:    agent = patient = None
tools/tests/linguistique/anaphore.py:96:        if seg.get("role") in ROLES_SUJET:
tools/tests/linguistique/anaphore.py:97:            agent = nom
tools/tests/linguistique/anaphore.py:98:        elif seg.get("role") in ROLES_OBJET:
tools/tests/linguistique/anaphore.py:112:            elif agent is not None:
tools/tests/linguistique/a
… [11836 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,260p' docs/methode/miroir.md", "description": "Read mirror method"}`

  ```
# Le miroir de sortie renforce le modèle d'entrée

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant de concevoir un test d'entrée**,
> une correction, ou une interface post-linguistique.

## Le principe

Notre **sens → texte** (la sortie) sera toujours **plus léger et plus fiable** que notre **texte → sens** (l'entrée)
✓✓ — parce que l'entrée doit gérer les **imperfections** du réel (bruit, orthographes multiples, langues mêlées,
coquilles), alors que la sortie part d'un sens **propre** ✓. On s'en sert donc comme d'un **miroir**.

## Les quatre règles

1. **Valider l'entrée par la sortie** ✓✓ : ce que l'entrée a compris doit pouvoir être **reproduit** par la sortie
   (restitution à l'identique, ou **boucle** entrée → sortie → entrée). *Si la sortie ne peut pas le redire, l'entrée
   a inventé ou perdu quelque chose* ✗✓.
2. **Découpler le signal du bruit** ✓✓ : la sortie, plus fiable, sert de **référence** pour juger l'entrée — on
   mesure l'écart entre ce que l'entrée a extrait et ce que la sortie sait reconstruire.
3. **Garder des marqueurs de bruit dans l'interface post-linguistique** ✓✓ : le sens extrait porte **où** et
   **combien** l'entrée 
… [1497 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,260p' docs/methode/resultats.md", "description": "Read results method"}`

  ```
# Ce qu'un résultat doit porter

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant d'écrire une fiche**, un JSON de
> résultats, ou un message de commit.

## Les cinq pièces d'un résultat

1. **Le chiffre** — la valeur, avec son [unité](../theorie/glossaire/entrees/unite.md) et son arrondi utile (jamais plus de chiffres que l'instrument n'en
   [porte](../theorie/glossaire/entrees/porte.md)) ;
2. **La mesure qui le produit** — le calcul exact, la métrique ([chrF](../theorie/glossaire/entrees/chrf.md), précision, rappel, [AUC](../theorie/glossaire/entrees/auc.md)…), et ce qu'elle ne
   mesure pas ;
3. **Le dispositif** — quel [corpus](../theorie/glossaire/entrees/corpus.md) (et sa provenance), quel modèle (taille, [quantification](../theorie/glossaire/entrees/quantification.md), date de coupure),
   quelles **couches de neurones** sondées, quel découpage, **quelle unité de mesure** (unité de sens ou unité
   grammaticale ; si c'est un [jeton](../theorie/glossaire/entrees/jeton.md), le dire comme **technique**), quels réglages (prompt, gabarit, longueur de
   sortie, graine) ;
4. **Le [contrôle négatif](../theorie/glossaire/entrees/controle-negatif.md)
… [2500 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nbench=json.load(open('reports/pensee-fiabilite-produit.json'))['banc_50']['resultats']\nfor gp in ['tools/tests/linguistique/gold.json','tools/tests/linguistique/gold_gele.json','tools/tests/linguistique/gold_reel.json','tools/tests/linguistique/gold_synth … [494 caractères tronqués]`

  ```
tools/tests/linguistique/gold.json 20
  MATCH f01 'Le chat dort.'
tools/tests/linguistique/gold_gele.json 602
  MATCH f01 'Le chat dort.'
tools/tests/linguistique/gold_reel.json 432
tools/tests/linguistique/gold_synthetique.json 160
tools/structures/donnees/gold-analyseur.json 61
  MATCH f02 'Le chat de la voisine qui dort sur le toit se réveille.'
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/structures/donnees/gold-analyseur.json'))\nfor p in d['phrases']:\n if p['texte'] in ['Le chat dort.','Le chat de la voisine qui dort sur le toit se réveille.']:\n  print(json.dumps(p,ensure_ascii=False,indent=2))\nPY", "description … [51 caractères tronqués]`

  ```
{
  "id": "p001",
  "split": "dev",
  "texte": "Le chat de la voisine qui dort sur le toit se réveille.",
  "attendus": [
    [
      "Le chat",
      "GN",
      "agent"
    ],
    [
      "de la voisine",
      "GP",
      "possession"
    ],
    [
      "qui dort sur le toit",
      "REL",
      "qualite"
    ],
    [
      "se réveille",
      "GV",
      "predicat"
    ]
  ]
}
  ```

- **bash** `{"command": "grep -n \"class Heuristique\\|def __init__\\|segmenter_s\\|union\" tools/bloc_linguistique.py | head -60", "description": "Inspect heuristic init options"}`

  ```
796:class Heuristique:
801:    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
803:                 union: bool = True, partition: str = "alternative"):
805:        self.segmenter_s = segmenter_s
808:        self.union = union
811:        # "filtrer_union" : on retire le S qui **contient** un segment chunker (le filtre
812:        # union du P0-3) ; "filtrer" : partition stricte, le chunker est la partition.
814:        if partition not in ("brut", "alternative", "filtrer_union", "filtrer"):
815:            raise ValueError("partition attend 'brut', 'alternative', 'filtrer_union' ou 'filtrer'")
987:        if not self.segmenter_s:
1004:        if not self.segmenter_s:
1033:        chemin courant (union S/chunker) et exige un GV à droite **et** un GN à gauche.
1590:        # participes : « Il est médecin », « la réunion est reportée »).
1647:        # l'interroge que pour le français, sinon ses segments polluent l'union.
1657:        # **un seul chunking par analyse**, partagé par les trois chemins (S, union, chunker) :
1740:        # 5 bis. union : les segments du chunker que le générateur S ne fournit pas
1741:        if cands and self.union:
1
… [2261 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '2380,2530p' tools/bloc_linguistique.py", "description": "Read annotation construction and views"}`

  ```
# --------------------------------------------------------------------------- compositions


def _relation_partition(x: Etiquette, y: Etiquette) -> str:
    """La relation de `y` vue **depuis** `x` : `inclut` = x contient y."""
    if x.debut == y.debut and x.fin == y.fin:
        return "meme_span"
    if x.debut <= y.debut and x.fin >= y.fin:
        return "inclut"
    if y.debut <= x.debut and y.fin >= x.fin:
        return "inclus"
    return "croise"


def _cle_preferee(e: Etiquette) -> tuple:
    """La vue préférée : le segment du chunker (union), le plus large, puis le plus sûr.

    Mesuré sur le gold 612 : dans 179/207 groupes ambigus qui portent un span du gold, le
    chunker le plus large **est** ce span (86,5 %) ; le S le plus large ne l'est que 25 fois sur 244.
    La préférence ne supprime rien par défaut : elle **classe**.
    """
    return (0 if (e.meta or {}).get("union") else 1, -(e.fin - e.debut), -e.confiance,
            e.debut, e.fin, e.type)


def _groupes_partition(segs: list[Etiquette]) -> list[list[Etiquette]]:
    """Les composantes connexes du graphe de chevauchement, ordonnées par position."""
    parent = list(range(len(segs)))

    def trouver(i: 
… [6196 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,280p' tools/tests/test_restitution.py", "description": "Read restitution tests"}`

  ```
#!/usr/bin/env python3
"""test_restitution.py — la restitution v0 (J1.4) : annotation → surface, et le miroir.

Ce que le test fige :
- la commande `drave restituer TEXTE` sort 0 et affiche la fidélité de surface ;
- la surface est reconstruite **sans lire** `Annotation.texte` ;
- les sauts de ligne sont annotés (`graphème` de type `contrôle`) et reviennent ;
- le miroir strict est le minimum de surface/mots/POS (la ponctuation séparée le fait
  tomber), et le contrôle négatif (mélange, troncature) le détecte ;
- sur les **50 textes libres**, 46 annotations et **46/46 surfaces exactes** ; sans le
  correctif `C`, `f50` perd ses sauts de ligne (45/46) — le trou que le miroir a trouvé.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE))

import tools.bloc_linguistique as bl  # noqa: E402
import tools.restitution as restitution  # noqa: E402

CLI = RACINE / "tools" / "drave.py"
BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"


def drave(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.ru
… [12102 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"restituer\\|canonique\\|restitution\" tools/drave.py | head -80; echo ===; sed -n '220,330p' tools/drave.py", "description": "Inspect CLI restituter"}`

  ```
13:    python3 tools/drave.py restituer "Le chat dort."
14:    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
19:**restitution v0** (annotation → surface, avec la fidélité du miroir). La restitution est un
51:import restitution  # noqa: E402  (la restitution v0 : annotation → surface)
80:def _canonique(a: bl.Annotation) -> str:
646:    canonique_1 = _canonique(premiere)
647:    canonique_2 = _canonique(seconde)
648:    identique = canonique_1 == canonique_2
649:    empreinte = hashlib.sha256(canonique_1.encode("utf-8")).hexdigest()[:16]
654:    print(f"  JSON       : {len(canonique_1.encode('utf-8'))} octets "
657:        print("  divergence : les deux analyses ne rendent pas le même JSON canonique",
663:# --------------------------------------------------------------------------- restitution
666:def cmd_restituer(args: argparse.Namespace) -> int:
671:    laisse le bloc détecter la langue, comme le CLI sans `--langue`. `--canonique`
672:    ajoute la **forme canonique v1** (segments + rôles + cibles) et son miroir ; la
682:            items = restitution.items_banc(donnees)
686:        if args.canonique:
687:            rapport = restitution.me
… [7624 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '660,735p' tools/drave.py; sed -n '280,380p' tools/tests/test_restitution.py", "description": "Read CLI restitution and rest of tests"}`

  ```
return 0


# --------------------------------------------------------------------------- restitution


def cmd_restituer(args: argparse.Namespace) -> int:
    """Reconstruit la surface depuis l'annotation et rend la fidélité du miroir.

    Deux modes : un **texte** (ou un fichier), ou un **banc** JSON de textes
    (`--banc`, le format de `reports/pensee-fiabilite-produit.json`). Le mode banc
    laisse le bloc détecter la langue, comme le CLI sans `--langue`. `--canonique`
    ajoute la **forme canonique v1** (segments + rôles + cibles) et son miroir ; la
    sortie de la v0 reste celle par défaut.
    """
    if args.banc:
        if args.texte is not None or args.fichier:
            print(f"{NOM}: erreur d'usage : --banc est exclusif de TEXTE et --fichier",
                  file=sys.stderr)
            return 2
        try:
            donnees = json.loads(pathlib.Path(args.banc).read_text(encoding="utf-8"))
            items = restitution.items_banc(donnees)
        except (OSError, ValueError) as exc:
            print(f"{NOM}: erreur : banc illisible : {exc}", file=sys.stderr)
            return 1
        if args.canonique:
            rapport = restitution.mesurer_banc_v1
… [2940 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nimport tools.restitution as r\nfrom tools.tests.linguistique import miroir\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nitems=r.items_banc(d)\nh=bl.Heuristique()\nfor it in i … [631 caractères tronqués]`

  ```
f01 ag='Le chat' pr='dort' li='—'
f02 ag='Le chat' pr='se réveille' li='—'
f03 ag='Comment' pr='Bonjour' li='—'
f04 ag='—' pr='Ferme' li='—'
f05 ag='—' pr='Ne touche pas' li='—'
f06 ag='Je' pr='ne pense pas' li='—'
f07 ag='—' pr='sleeps' li='on the roof'
f08 ag='—' pr='—' li='—'
f09 ag='—' pr='—' li='—'
f10 ag='Le prix' pr='est' li='—'
f11 ag='—' pr='Rendez-vous' li='—'
f12 ag='Visitez' pr='https' li='—'
f13 ag="J'ai" pr='trouvé ça génial' li='—'
f14 REFUS
f15 REFUS
f16 REFUS
f17 REFUS
f18 ag='—' pr='—' li='—'
f19 ag='—' pr='COVID-' li='—'
f20 ag='Leroy' pr='M' li='vers'
f21 ag='Je' pr='ne sais pas' li='—'
f22 ag='—' pr="C'est" li='—'
f23 ag='—' pr='Attention' li='—'
f24 ag='Il' pr='était' li='—'
f25 ag='—' pr='Pourquoi' li='—'
f26 ag='Je' pr='cherche' li='—'
f27 ag='—' pr='—' li='—'
f28 ag='Le café coûte' pr='est gratuite' li='—'
f29 ag='Il' pr='a dit' li='—'
f30 ag='Nous' pr='avons lu' li='—'
f31 ag='NE' pr='ÇA NE MARCHE PAS' li='—'
f32 ag="J'aime les pommes" pr='pas' li='—'
f33 ag='—' pr='—' li='—'
f34 ag='il' pr='continue' li='—'
f35 ag='—' pr='jumps' li='—'
f36 ag='I' pr="can't believe it's already" li='—'
f37 ag='—' pr='—' li='—'
f38 ag='Les URL' pr='a' li='—'
f39 ag='Un fich
… [500 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nimport tools.restitution as r\ngold=json.load(open('tools/structures/donnees/gold-analyseur.json'))['phrases']\nh=bl.Heuristique()\njustes=total=0\nfor p in gold:\n    a=h.analyser(p['texte' … [1030 caractères tronqués]`

  ```
p002 GP instrument got attribut ''
p005 GP theme got destinataire ''
g019 GP destinataire got theme ''
h029 GV predicat got prédicat ''
h031 GV predicat got prédicat ''
h046 GV predicat got prédicat ''
h047 GV predicat got prédicat ''
h048 GV predicat got prédicat ''
h049 GV predicat got prédicat ''
h050 GV predicat got prédicat ''
h051 GV predicat got prédicat ''
h056 SUB consequence got complément ''
h058 GV predicat got prédicat ''
h060 GP theme got possession ''
h061 GV predicat got prédicat ''
roles 129 144 0.8958
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))\nr=d['banc_50']['resultats'][0]\nprint(json.dumps(r,ensure_ascii=False,indent=2)[:3000])\nPY", "description": "Inspect v0 bench result fields"}`

  ```
{
  "id": "f01",
  "categorie": "fr",
  "attendu": "fr",
  "texte": "Le chat dort.",
  "caracteres": 13,
  "octets_utf8": 13,
  "rc": 0,
  "temps_cli_ms": 150.79,
  "temps_api_ms": 0.796,
  "deterministe": true,
  "json_octets": 5561,
  "json_valide": true,
  "langue": "fr",
  "script": "Latn",
  "labels": 19,
  "mots": 4,
  "pos": 3,
  "syntagmes": 2,
  "attaches": 2,
  "sans_attachement": 0,
  "chevauchements_syntagme": 0,
  "chevauchements_phrase_type": 0,
  "syntagmes_union": 0,
  "conflits_apres_filtre_union": 0,
  "cibles_fermees": 0,
  "cibles_absentes": 0,
  "phrases": 1,
  "phrases_espaces_initiaux": 0,
  "documents": 1,
  "doc_tronquees": 0,
  "doc_titres": [],
  "unites_semantiques": 2,
  "fraction_semantique": 0.6154,
  "trous_pos": {
    "mot": {
      "total": 3,
      "sans_pos": 0
    },
    "ponctuation": {
      "total": 1,
      "sans_pos": 1
    }
  },
  "sans_syntagme": false,
  "sans_pos": false
}
  ```

- **bash** `{"command": "cd tools/structures && python3 - <<'PY'\nimport json,sys\nsys.path.insert(0,'.')\nimport generateur\nbench=json.load(open('../../reports/pensee-fiabilite-produit.json'))['banc_50']['resultats']\nfor it in bench:\n    if it['id'] in ('f14','f15','f16','f17'): continue\n    try: segs=gene … [224 caractères tronqués]`

  ```
f01 [('GN', 'agent', 'Le chat'), ('GV', 'predicat', 'dort')]
f02 [('GN', 'agent', 'Le chat'), ('GP', 'possession', 'de la voisine'), ('REL', 'qualite', 'qui dort sur le toit'), ('GV', 'predicat', 'se réveille')]
f03 [('GV', 'predicat', 'Bonjour'), ('GV', 'predicat', 'Comment allez-vous'), ('GP', 'temps', "aujourd'hui")]
f04 [('GV', 'predicat', 'Ferme'), ('GN', 'patient', 'la porte'), ('SUB', 'hypothese', "s'il te plaît")]
f05 [('GV', 'predicat', 'Ne touche pas'), ('GN', 'patient', 'ça')]
f06 [('GV', 'predicat', 'Je ne pense pas'), ('SUB', 'contenu', "qu'il viendra"), ('GP', 'temps', 'demain'), ('GV', 'predicat', 'nous verrons bien')]
f07 [('GV', 'predicat', 'The cat sleeps on the roof')]
f08 [('GV', 'predicat', 'Where is the nearest train station'), ('GV', 'predicat', 'please')]
f09 [('GV', 'predicat', "Don't forget to bring your passport")]
f10 [('GN', 'agent', 'Le prix'), ('GV', 'predicat', 'est'), ('GP', 'but', 'pour 3 articles')]
f11 [('GV', 'predicat', 'Rendez-vous'), ('GN', 'patient', 'le'), ('GP', 'destinataire', 'à 14h')]
f12 [('GV', 'predicat', 'Visitez https'), ('GV', 'predicat', 'example'), ('GV', 'predicat', 'com/docs'), ('GV', 'predicat', 'page'), ('GP', 'but', 'pour l
… [9480 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nh=bl.Heuristique()\nfor t in ['Bonjour','Comment allez-vous','Le chat dort.','M. Dupont','Question rhétorique','Notes de terrain','Lorem ipsum dolor sit amet']:\n a=h.analyser(t,'fr')\n print(t,  … [126 caractères tronqués]`

  ```
Bonjour [('Bonjour', 'NOUN')]
Comment allez-vous [('Comment', 'NOUN'), ('allez-vous', 'ADJ')]
Le chat dort. [('Le', 'DET'), ('chat', 'NOUN'), ('dort', 'VERB'), ('.', 'PONCT')]
M. Dupont [('M', 'PRON'), ('.', 'PONCT'), ('Dupont', 'NOUN')]
Question rhétorique [('Question', 'NOUN'), ('rhétorique', 'NOUN')]
Notes de terrain [('Notes', 'NOUN'), ('de', 'PREP'), ('terrain', 'NOUN')]
Lorem ipsum dolor sit amet [('Lorem', 'NOUN'), ('ipsum', 'NOUN'), ('dolor', 'NOUN'), ('sit', 'NOUN'), ('amet', 'NOUN')]
  ```

- **bash** `{"command": "grep -n '^def _est_verbe\\|^def est_verbe\\|^def _normaliser\\|^AUXILIAIRES\\|^VERBES' tools/bloc_linguistique.py | head -20; grep -n 'def _tokens' tools/bloc_linguistique.py | head", "description": "Find verb helper functions"}`

  ```
152:def _normaliser(texte: str) -> str:
327:VERBES = {
393:VERBES_IMPERATIFS = set("va viens prends fais dis regarde écoute donne cherche trouve ouvre ferme "
398:VERBES_CONNUS = set("""
468:AUXILIAIRES = set("""
509:def _est_verbe(mot: str) -> bool:
2002:    def _tokens(texte: str) -> list[tuple[int, int, str]]:
2131:    def _tokens(texte: str) -> list[tuple[int, int, str]]:
  ```

- **bash** `{"command": "sed -n '500,530p' tools/bloc_linguistique.py; sed -n '327,410p' tools/bloc_linguistique.py | head -40", "description": "Read verb detection helper"}`

  ```
def _sans_enclitique(mot: str) -> str:
    """`appelle-moi` → `appelle` (les enclitiques ne font pas partie de la tête)."""
    for suf in ENCLITIQUES:
        if mot.endswith(suf) and len(mot) > len(suf):
            return mot[: -len(suf)]
    return mot


def _est_verbe(mot: str) -> bool:
    """Le mot est-il un verbe ? Lexique + désinences courantes (fr/en)."""
    n = _normaliser(_sans_enclitique(mot))
    if not n:
        return False
    if n in VERBES_CONNUS:
        return True
    for suf in ("er", "ir", "e", "es", "ent", "ait", "aient", "é", "ée", "és", "i", "u",
                "ez", "ons", "iez", "ais", "ra", "rai", "ras", "rons", "rez", "ront",
                "s", "ed", "ing", "en"):
        if n.endswith(suf) and n[:-len(suf)] in VERBES_CONNUS:
            return True
    # participes en -é/-és/-ée : `accroché` → `accrocher`
    for suf in ("ées", "ée", "és", "é"):
        if n.endswith(suf) and (n[:-len(suf)] + "er") in VERBES_CONNUS:
            return True
    # 1er groupe : `nage` → `nager`, `commence` → `commencer` (la voyelle finale tombe)
    for suf in ("es", "ent", "e", "ait", "aient", "ais", "ons", "ez"):
        if n.endswith(suf):
            radical = 
… [3413 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys; sys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfor w in ['dort','allez','allez-vous','jumps','sleeps','is','est','a','sont','peut','contient','aime','est reportée','se réveille','n\\'y','Notes','Bonjour','M','Dupont','Question','adipiscing',' … [282 caractères tronqués]`

  ```
dort True dort False
allez True allez False
allez-vous True allez-vous False
jumps False jumps False
sleeps True sleeps False
is False is True
est True est True
a True a True
sont True sont True
peut True peut False
contient False contient False
aime True aime False
est reportée False est reportée False
se réveille False se réveille False
n'y False n'y False
Notes False notes False
Bonjour False bonjour False
M False m False
Dupont False dupont False
Question False question False
adipiscing False adipiscing False
s'améliore False s'améliore False
cherche True cherche False
continue True continue False
vit False vit False
sourit False sourit False
chantent True chantent False
jouent True jouent False
arrivés True arrivés False
trouvé True trouvé False
can't False can't False
believe False believe False
flies True flies False
oublie False oublie False
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys; sys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfor w in ['réveille','réveillent','contient','sourit','vit','oublie','jumps','can','believe','est','reportée','arrivés']:\n print(w, bl._est_verbe(w))\nPY", "description": "Test more verb forms"}`

  ```
réveille False
réveillent False
contient False
sourit False
vit False
oublie False
jumps False
can False
believe False
est True
reportée False
arrivés True
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys; sys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nh=bl.Heuristique()\nfor t in ['Élodie sourit.','Le texte contient des accents.','Il était une fois une petite fille','Le chat de la voisine qui dort sur le toit se réveille.','M. Dupont, le Dr Ma … [350 caractères tronqués]`

  ```
Élodie sourit.
[('Élodie', 'NOUN'), ('sourit', 'NOUN'), ('.', 'PONCT')]
[('Élodie sourit', 'predicat')]
Le texte contient des accents.
[('Le', 'DET'), ('texte', 'NOUN'), ('contient', 'NOUN'), ('des', 'PREP'), ('accents', 'NOUN'), ('.', 'PONCT')]
[('Le texte contient', 'agent'), ('des accents', 'possession')]
Il était une fois une petite fille
[('Il', 'PRON'), ('était', 'AUX'), ('une', 'DET'), ('fois', 'NOUN'), ('une', 'DET'), ('petite', 'ADJ'), ('fille', 'NOUN')]
[('Il', 'agent'), ('était', 'prédicat'), ('était une fois une petite fille', 'predicat'), ('une fois une petite fille', 'groupe nominal')]
Le chat de la voisine qui dort sur le toit se réveille.
[('Le', 'DET'), ('chat', 'NOUN'), ('de', 'PREP'), ('la', 'DET'), ('voisine', 'NOUN'), ('qui', 'PRON'), ('dort', 'VERB'), ('sur', 'PREP'), ('le', 'DET'), ('toit', 'NOUN'), ('se', 'PRON'), ('réveille', 'NOUN'), ('.', 'PONCT')]
[('Le chat', 'agent'), ('de la voisine', 'possession'), ('qui dort sur le toit', 'qualite'), ('qui dort sur le toit se réveille', 'qualité'), ('se réveille', 'predicat')]
M. Dupont, le Dr Martin et Mme Leroy sont arrivés vers 9 h.
[('M', 'PRON'), ('.', 'PONCT'), ('Dupont', 'NOUN'), (',', 'PONCT'), ('le', 'DET')
… [779 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys; sys.path.insert(0,'.')\nimport tools.bloc_linguistique as bl\nfor w in ['sourit','contient','réveille','vit','oublie','jumps','can','believe','adipiscing','reportée']:\n print(w, w in bl.VERBES['fr'] or w in bl.VERBES['en'], w in bl.VERBES_CONNUS)\nPY", "de … [30 caractères tronqués]`

  ```
sourit False False
contient False False
réveille False False
vit False False
oublie False False
jumps False False
can False False
believe False False
adipiscing False False
reportée False False
  ```

- **bash** `{"command": "date -Iseconds; git config user.name; git config user.email", "description": "Get current date and git identity"}`

  ```
2026-11-15T04:59:00-05:00
Stéphane
stephane@localhost
  ```

- **bash** `{"command": "sed -n '1,70p' tools/drave.py; sed -n '760,890p' tools/drave.py", "description": "Inspect drave imports and parser"}`

  ```
#!/usr/bin/env python3
"""drave.py — le point d'entrée produit du bloc linguistique.

Une seule commande, quatre gestes, hors ligne et déterministe :

    python3 tools/drave.py analyser "Le chat dort."
    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
    python3 tools/drave.py evaluer
    python3 tools/drave.py evaluer --gold --json
    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
    python3 tools/drave.py restituer "Le chat dort."
    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
    python3 tools/drave.py --version

Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et la
**restitution v0** (annotation → surface, avec la fidélité du miroir). La restitution est un
**codec de surface** : elle reconstruit depuis le niveau `graphème`, pas
… [10005 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'def _dumps' -A10 tools/drave.py", "description": "Inspect JSON dump helper"}`

  ```
75:def _dumps(objet) -> str:
76-    """JSON stable (pas d'horodatage, pas de durée) et lisible."""
77-    return _sur(json.dumps(objet, ensure_ascii=False, indent=1)) + "\n"
78-
79-
80-def _canonique(a: bl.Annotation) -> str:
81-    """La forme comparée par `rejouer` : clés triées, durée exclue, sans espaces inutiles."""
82-    return _sur(json.dumps(a.json(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
83-
84-
85-# --------------------------------------------------------------------------- le tagger (option)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib\nRACINE=pathlib.Path('.').resolve()\nbank=json.loads((RACINE/'reports/pensee-fiabilite-produit.json').read_text(encoding='utf-8'))\nitems=bank['banc_50']['resultats']\nby_id={it['id']:it for it in items}\n\nF={\n'f01':[{'agent':'Le chat','predicat' … [5511 caractères tronqués]`

  ```
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold_restitution_v2.json 46
46 f01 f50
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py", "content": "\"\"\"restitution_v2.py — la restitution v2 : les rôles (agent, prédicat, lieu).\n\nLa v0 restitue la **surface** (graphème → texte) ; la v1 restitue la **forme canonique**\n(segments + rôles + cible … [31253 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py", "old_string": "    eligible = bool(principal[\"agent\"] or principal[\"predicat\"] or principal[\"lieu\"])", "new_string": "    eligible = bool(principal[\"predicat\"])"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py", "old_string": "        f\"  rôles exacts            {roles['exacts']:>6}/{roles['total']:<6} \"\n        f\"{roles['taux']:>8.4f}\",\n        f\"  justes / attendus       {roles['justes']:>6}/{roles['attendus']: … [645 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,sys,pathlib,time\nsys.path.insert(0,'.')\nimport tools.restitution_v2 as v2\nbank=json.loads(pathlib.Path('reports/pensee-fiabilite-produit.json').read_text(encoding='utf-8'))\ngold=json.loads(pathlib.Path('tools/tests/linguistique/gold_restitution_v2.json' … [645 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 8, in <module>
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py", line 569, in mesurer_banc_v2
    m = mesurer_annotation_v2(a, texte, attendu)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py", line 430, in mesurer_annotation_v2
    "controle_negatif_rendu": controler_negatif_rendu(rendu),
                              ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py", line 361, in controler_negatif_rendu
    texte_sans, relu_sans = altère(True)
                            ^^^^^^
NameError: name 'altère' is not defined. Did you mean: 'altere'?
[exit code: 1]
  ```

- **bash** `{"command": "grep -n 'altère\\|altere' tools/restitution_v2.py", "description": "Locate typo"}`

  ```
342:    def altere(sans: bool) -> tuple[str, dict]:
361:    texte_sans, relu_sans = altère(True)
362:    texte_permute, relu_permute = altère(False)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/restitution_v2.py')\ns=p.read_text(encoding='utf-8')\ns=s.replace('altère(True)','altere(True)').replace('altère(False)','altere(False)')\np.write_text(s,encoding='utf-8')\nPY\npython3 - <<'PY'\nimport json,sys,pathlib,time\nsys.pa … [847 caractères tronqués]`

  ```
durée 0.15
restitution v2 — les rôles — banc reports/pensee-fiabilite-produit.json
textes 50 · annotés 46 · refus 4 (f14, f15, f16, f17)

cadre principal (agent, prédicat, lieu)
  cadres exacts                20/46       0.4348
  cadres partiels              42/46       0.9130
  exacts stricts (1re var.)    17/46       0.3696
  rôles exacts                93/138      0.6739
  justes / attendus           41/77    
  précision / rappel / F1 0.1916 / 0.5325 / 0.2818
  faux positifs / négatifs 32 / 36

par rôle                  exacts    attendus   prédits   justes   préc.   rappel
  agent                     30/46         32        30       19  0.6333   0.5938
  prédicat                  23/46         39        39       20  0.5128   0.5128
  lieu                      40/46          6         4        2  0.5000   0.3333

segments de rôle 198 · agents 43 · prédicats 143 · lieux 12 · cadres 139
textes avec au moins un rôle : 40/46 (0.8696)
spans de rôle dans la source : 198/198 (1.0000)

contrôle vide            : 61/138 rôles exacts
contrôle constant (type) : 68/138 rôles exacts
contrôle rôles mélangés  : 27/138 rôles exacts
restitution du rendu     : 46/46 (1.0000)
contrôle négatif ren
… [2249 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,sys,pathlib\nsys.path.insert(0,'.')\nimport tools.restitution_v2 as v2\nbank=json.loads(pathlib.Path('reports/pensee-fiabilite-produit.json').read_text(encoding='utf-8'))\ngold=json.loads(pathlib.Path('tools/tests/linguistique/gold_restitution_v2.json').rea … [161 caractères tronqués]`

  ```
{'exacts': 93, 'total': 138, 'taux': 0.6739, 'justes': 41, 'attendus': 77, 'predits': 214, 'faux_positifs': 32, 'faux_negatifs': 36, 'vrais_negatifs': 52, 'par_role': {'agent': {'exacts': 30, 'attendus': 32, 'predits': 30, 'justes': 19, 'faux_positifs': 11, 'faux_negatifs': 13, 'vrais_negatifs': 11, 'taux_exact': 0.6522, 'precision': 0.6333, 'rappel': 0.5938, 'f1': 0.6129}, 'predicat': {'exacts': 23, 'attendus': 39, 'predits': 39, 'justes': 20, 'faux_positifs': 19, 'faux_negatifs': 19, 'vrais_negatifs': 3, 'taux_exact': 0.5, 'precision': 0.5128, 'rappel': 0.5128, 'f1': 0.5128}, 'lieu': {'exacts': 40, 'attendus': 6, 'predits': 4, 'justes': 2, 'faux_positifs': 2, 'faux_negatifs': 4, 'vrais_negatifs': 38, 'taux_exact': 0.8696, 'precision': 0.5, 'rappel': 0.3333, 'f1': 0.4}}}
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,sys,pathlib\nsys.path.insert(0,'.')\nimport tools.restitution_v2 as v2\nbank=json.loads(pathlib.Path('reports/pensee-fiabilite-produit.json').read_text(encoding='utf-8'))\ngold=json.loads(pathlib.Path('tools/tests/linguistique/gold_restitution_v2.json').rea … [306 caractères tronqués]`

  ```
f01 6 {'variante': 0, 'exacts': 3, 'justes': 2, 'attendus': 2, 'predits': 6, 'faux_positifs': 0, 'faux_negatifs': 0, 'vrais_negatifs': 1, 'par_role': {'agent': {'predit': 'Le chat', 'attendu': 'Le chat', 'egal': True, 'juste': True, 'faux_positif': False, 'faux_negatif': False, 'vrai_negatif': False}, 'predicat': {'predit': 'dort', 'attendu': 'dort', 'egal': True, 'juste': True, 'faux_positif': False, 'faux_negatif': False, 'vrai_negatif': False}, 'lieu': {'predit': '', 'attendu': '', 'egal': True, 'juste': False, 'faux_positif': False, 'faux_negatif': False, 'vrai_negatif': True}}}
f02 6 {'variante': 1, 'exacts': 3, 'justes': 2, 'attendus': 2, 'predits': 6, 'faux_positifs': 0, 'faux_negatifs': 0, 'vrais_negatifs': 1, 'par_role': {'agent': {'predit': 'Le chat', 'attendu': 'Le chat', 'egal': True, 'juste': True, 'faux_positif': False, 'faux_negatif': False, 'vrai_negatif': False}, 'predicat': {'predit': 'se réveille', 'attendu': 'se réveille', 'egal': True, 'juste': True, 'faux_positif': False, 'faux_negatif': False, 'vrai_negatif': False}, 'lieu': {'predit': '', 'attendu': '', 'egal': True, 'juste': False, 'faux_positif': False, 'faux_negatif': False, 'vrai_negatif': True}}}
f03 6 
… [588 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py", "new_string": "            \"predits\": sum(1 for role in ROLES if predit.get(role)),", "old_string": "            \"predits\": sum(1 for p in predit.values() if p),"}`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py": file changed since it was read — re-read the file, then retry
  ```

- **bash** `{"command": "grep -n 'predits' tools/restitution_v2.py | head -20", "description": "Locate predits line"}`

  ```
298:            "predits": sum(1 for p in predit.values() if p),
445:        role: {"exacts": 0, "attendus": 0, "predits": 0,
456:            p["predits"] += int(bool(x["predit"]))
463:        p["precision"] = _taux(p["justes"], p["predits"])
474:        "predits": sum(c["predits"] for c in comparaisons),
660:    precision = _taux(roles["justes"], roles["predits"])
674:            f"{p['predits']:>9} {p['justes']:>8} {p['precision']:>7.4f} {p['rappel']:>8.4f}")
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py", "offset": 288, "limit": 22}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py</path>
<type>file</type>
<content>
288:         exacts = sum(1 for x in par_role.values() if x["egal"])
289:         justes = sum(1 for x in par_role.values() if x["juste"])
290:         fp = sum(1 for x in par_role.values() if x["faux_positif"])
291:         fn = sum(1 for x in par_role.values() if x["faux_negatif"])
292:         score = (exacts, justes, -fp, -fn, -rang)
293:         fiche = {
294:             "variante": rang,
295:             "exacts": exacts,
296:             "justes": justes,
297:             "attendus": sum(1 for v in variante.values() if v),
298:             "predits": sum(1 for p in predit.values() if p),
299:             "faux_positifs": fp,
300:             "faux_negatifs": fn,
301:             "vrais_negatifs": sum(1 for x in par_role.values() if x["vrai_negatif"]),
302:             "par_role": par_role,
303:         }
304:         if meilleur is None or score > meilleur[0]:
305:             meilleur = (score, fiche)
306:     return meilleur[1]
307: 
308: 
309: def _cadre_constant_par_type(a: bl.Annotation) -> dict:

(Showing lines 288-309 of 691. Use offset=310 to continue.)
<
… [9 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py", "new_string": "            \"predits\": sum(1 for role in ROLES if predit.get(role)),", "old_string": "            \"predits\": sum(1 for p in predit.values() if p),"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,sys,pathlib\nsys.path.insert(0,'.')\nimport tools.restitution_v2 as v2\nbank=json.loads(pathlib.Path('reports/pensee-fiabilite-produit.json').read_text(encoding='utf-8'))\ngold=json.loads(pathlib.Path('tools/tests/linguistique/gold_restitution_v2.json').rea … [209 caractères tronqués]`

  ```
restitution v2 — les rôles — banc reports/pensee-fiabilite-produit.json
textes 50 · annotés 46 · refus 4 (f14, f15, f16, f17)

cadre principal (agent, prédicat, lieu)
  cadres exacts                20/46       0.4348
  cadres partiels              42/46       0.9130
  exacts stricts (1re var.)    17/46       0.3696
  rôles exacts                93/138      0.6739
  justes / attendus           41/77    
  précision / rappel / F1 0.5616 / 0.5325 / 0.5467
  faux positifs / négatifs 32 / 36

par rôle                  exacts    attendus   prédits   justes   préc.   rappel
  agent                     30/46         32        30       19  0.6333   0.5938
  prédicat                  23/46         39        39       20  0.5128   0.5128
  lieu                      40/46          6         4        2  0.5000   0.3333

segments de rôle 198 · agents 43 · prédicats 143 · lieux 12 · cadres 139
textes avec au moins un rôle : 40/46 (0.8696)
spans de rôle dans la source : 198/198 (1.0000)

contrôle vide            : 61/138 rôles exacts
contrôle constant (type) : 68/138 rôles exacts
contrôle rôles mélangés  : 27/138 rôles exacts
restitution du rendu     : 46/46 (1.0000)
contrôle négatif rendu   : 39/3
… [20 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py", "limit": 70, "offset": 468}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py</path>
<type>file</type>
<content>
468:     return {
469:         "exacts": sum(c["exacts"] for c in comparaisons),
470:         "total": 3 * len(comparaisons),
471:         "taux": _taux(sum(c["exacts"] for c in comparaisons), 3 * len(comparaisons)),
472:         "justes": sum(c["justes"] for c in comparaisons),
473:         "attendus": sum(c["attendus"] for c in comparaisons),
474:         "predits": sum(c["predits"] for c in comparaisons),
475:         "faux_positifs": sum(c["faux_positifs"] for c in comparaisons),
476:         "faux_negatifs": sum(c["faux_negatifs"] for c in comparaisons),
477:         "vrais_negatifs": sum(c["vrais_negatifs"] for c in comparaisons),
478:         "par_role": par_role,
479:     }
480: 
481: 
482: def _agreger_resultats(resultats: list[dict]) -> dict:
483:     annotes = [r for r in resultats if not r.get("refus")]
484:     refuses = [r for r in resultats if r.get("refus")]
485:     n = len(annotes)
486:     comparaisons = [r["comparaison"] for r in annotes]
487:     strictes = [r["comparaison_stricte"] for r in annotes]
488:     constant = [r["constant_par_type"] for r 
… [2775 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py", "new_string": "    return {\n        \"exacts\": sum(c[\"exacts\"] for c in comparaisons),\n        \"total\": 3 * len(comparaisons),\n        \"taux\": _taux(sum(c[\"exacts\"] for c in comparaisons), 3 * len(co … [1464 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py", "new_string": "        \"cadre\": {\n            \"exacts\": sum(1 for c in comparaisons if c[\"exacts\"] == 3),\n            \"taux\": _taux(sum(1 for c in comparaisons if c[\"exacts\"] == 3), n),\n             … [1808 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/restitution_v2.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/restitution_v2.py')\ns=p.read_text(encoding='utf-8')\nold='''        \"cadre\": {\n            \"exacts\": sum(1 for c in comparaisons if c[\"exacts\"] == 3),\n            \"taux\": _taux(sum(1 for c in comparaisons if c[\"exacts\" … [2025 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/restitution_v2.py')\ns=p.read_text(encoding='utf-8')\nold='''        f\"  cadres exacts            {cadre['exacts']:>6}/{n:<6} {cadre['taux']:>8.4f}\",\n        f\"  cadres partiels          {cadre['partiels']:>6}/{n:<6} \"\n       … [1861 caractères tronqués]`

  ```
ok
restitution v2 — les rôles — banc reports/pensee-fiabilite-produit.json
textes 50 · annotés 46 · refus 4 (f14, f15, f16, f17)

cadre principal (agent, prédicat, lieu)
  cadres exacts                20/46       0.4348
  dont non vides               17/46     (0.3696) · vides 3
  cadres partiels              42/46       0.9130
  exacts stricts (1re var.)    17/46       0.3696
  rôles exacts                93/138      0.6739
  justes / attendus           41/77    
  précision / rappel / F1 0.5616 / 0.5325 / 0.5467
  faux positifs / négatifs 32 / 36

par rôle                  exacts    attendus   prédits   justes   préc.   rappel
  agent                     30/46         32        30       19  0.6333   0.5938
  prédicat                  23/46         39        39       20  0.5128   0.5128
  lieu                      40/46          6         4        2  0.5000   0.3333

segments de rôle 198 · agents 43 · prédicats 143 · lieux 12 · cadres 139
textes avec au moins un rôle : 40/46 (0.8696)
spans de rôle dans la source : 198/198 (1.0000)

contrôle vide            : 61/138 rôles exacts · cadres exacts 7/46
contrôle constant (type) : 68/138 rôles exacts · cadres exacts 6/46
contrôle rôles 
… [146 caractères tronqués]
  ```

- **bash** `{"command": "cat >> tools/restitution_v2.py <<'PY'\n\n\n# --------------------------------------------------------------------------- gold externe\n\n\nROLE_CONSTANT = {\"GN\": \"agent\", \"GV\": \"predicat\", \"GP\": \"lieu\",\n                 \"SUB\": \"contenu\", \"REL\": \"qualite\"}\nGOLD_ANAL … [3182 caractères tronqués]`

  ```
{'or': 'tools/structures/donnees/gold-analyseur.json', 'phrases': 61, 'roles_justes': 139, 'roles_total': 144, 'taux': 0.9653, 'baseline_role_constant': {'justes': 104, 'total': 144, 'taux': 0.7222}, 'par_type': {'GN': 36, 'GP': 23, 'GV': 58, 'REL': 7, 'SUB': 20}, 'definition': 'appariement par recouvrement maximal à type égal, puis comparaison du rôle normalisé (prédicat/predicat)'}
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"mesurer_restitution_v2.py — produit le JSON de la fiche D2.\n\nMesure la **restitution v2** — les rôles (agent, prédicat, lieu) — sur les **46 textes\nannotables** du banc v0 (`reports/pensee-fiabilite-produit.json`) et compare le cadre\nprincipal à l'**or  … [5428 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_restitution_v2.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/mesurer_restitution_v2.py", "description": "Generate v2 JSON and summary"}`

  ```
restitution v2 — les rôles — banc reports/pensee-fiabilite-produit.json
textes 50 · annotés 46 · refus 4 (f14, f15, f16, f17)

cadre principal (agent, prédicat, lieu)
  cadres exacts                20/46       0.4348
  dont non vides               17/46     (0.3696) · vides 3
  cadres partiels              42/46       0.9130
  exacts stricts (1re var.)    17/46       0.3696
  rôles exacts                93/138      0.6739
  justes / attendus           41/77    
  précision / rappel / F1 0.5616 / 0.5325 / 0.5467
  faux positifs / négatifs 32 / 36

par rôle                  exacts    attendus   prédits   justes   préc.   rappel
  agent                     30/46         32        30       19  0.6333   0.5938
  prédicat                  23/46         39        39       20  0.5128   0.5128
  lieu                      40/46          6         4        2  0.5000   0.3333

segments de rôle 198 · agents 43 · prédicats 143 · lieux 12 · cadres 139
textes avec au moins un rôle : 40/46 (0.8696)
spans de rôle dans la source : 198/198 (1.0000)

contrôle vide            : 61/138 rôles exacts · cadres exacts 7/46
contrôle constant (type) : 68/138 rôles exacts · cadres exacts 6/46
contrôle rôles mél
… [261 caractères tronqués]
  ```

- **bash** `{"command": "ls -lh reports/pensee-restitution-v2.json; python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-restitution-v2.json'))\nprint(d['schema'], d['version'], d['date'], d['tache'])\nprint(d['synthese']['cadre'])\nprint(d['synthese']['roles']['exacts'], d['synthese']['roles']['tota … [317 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 546K 15 nov 05:02 reports/pensee-restitution-v2.json
drave.restitution.v2.banc 1 2026-11-15 D2
{'exacts': 20, 'taux': 0.4348, 'exacts_non_vides': 17, 'exacts_vides': 3, 'partiels': 42, 'partiels_taux': 0.913, 'exacts_stricts': 17, 'taux_strict': 0.3696, 'roles_exacts_moyens': 2.0217}
93 138
externe 0.9653
f01 {'agent': 'Le chat', 'predicat': 'dort', 'lieu': '', 'agent_role': 'agent', 'agent_origine': 'agent_avant', 'lieu_role': '', 'lieu_origine': '', 'agent_span': [0, 7], 'predicat_span': [8, 12], 'lieu_span': None} 3 True
f02 {'agent': 'Le chat', 'predicat': 'se réveille', 'lieu': '', 'agent_role': 'agent', 'agent_origine': 'agent_avant', 'lieu_role': '', 'lieu_origine': '', 'agent_span': [0, 7], 'predicat_span': [43, 54], 'lieu_span': None} 3 True
f03 {'agent': 'Comment', 'predicat': 'Bonjour', 'lieu': '', 'agent_role': 'agent', 'agent_origine': 'agent_apres', 'lieu_role': '', 'lieu_origine': '', 'agent_span': [10, 17], 'predicat_span': [0, 7], 'lieu_span': None} 1 True
refus ['f14', 'f15', 'f16', 'f17']
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/drave.py')\ns=p.read_text(encoding='utf-8')\nold='''import bloc_linguistique as bl  # noqa: E402  (import après l'installation des chemins)\nimport restitution  # noqa: E402  (la restitution v0 : annotation → surface)\n'''\nnew=''' … [8783 caractères tronqués]`

  ```
ok
restitution v2 (rôles)
source          : 'Le chat dort.'
cadre principal :
  agent         : Le chat
  prédicat      : dort
  lieu          : —
segments de rôle: 2 (1 agents, 1 prédicats, 0 lieux)

rôles (agent, prédicat, lieu)
  agent     : Le chat
  prédicat  : dort
  lieu      : —
segments de rôle : 2
   1. GN/agent [0:7] « Le chat » → dort
   2. GV/predicat [8:12] « dort » → chat

restitution du rendu : exacte (relire_roles(rendre_roles(a)))
fidélité à l'or       : 1/3 rôles exacts, 0/0 justes, 2 faux positifs, 0 faux négatifs (variante 0)
contrôle négatif      : retrait détecté · permutation détectée · détecté True
---- JSON
{
 "schema": "drave.restitution.v2",
 "version": 1,
 "langue": "fr",
 "refus": "",
 "source_caracteres": 13,
 "roles": {
  "definition": "cadre principal (agent, prédicat, lieu) lu depuis les syntagmes et leur meta.role ; cadres par prédicat ; segments de rôle",
  "principal": {
   "agent": "Le chat",
   "predicat": "dort",
   "lieu": "",
   "agent_role": "agent",
   "agent_origine": "agent_avant",
   "lieu_role": "",
   "lieu_origine": "",
   "agent_span": [
    0,
    7
   ],
   "predicat_span": [
    8,
    12
   ],
   "lieu_span": null
  },
  "cadre
… [1507 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/restitution_v2.py')\ns=p.read_text(encoding='utf-8')\nold='''    rendu = rendre_roles(a)\n    principal = rendu[\"principal\"]\n    variantes = (gold or {}).get(\"variantes\") or []\n    comparaison = comparer_cadre(principal, vari … [1573 caractères tronqués]`

  ```
ok
  prédicat  : dort
  lieu      : —
segments de rôle : 2
   1. GN/agent [0:7] « Le chat » → dort
   2. GV/predicat [8:12] « dort » → chat

restitution du rendu : exacte (relire_roles(rendre_roles(a)))
contrôle négatif      : retrait détecté · permutation détectée · détecté True
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,sys,pathlib\nsys.path.insert(0,'.')\nimport tools.restitution_v2 as v2\nbank=json.loads(pathlib.Path('reports/pensee-fiabilite-produit.json').read_text(encoding='utf-8'))\ngold=json.loads(pathlib.Path('tools/tests/linguistique/gold_restitution_v2.json').rea … [248 caractères tronqués]`

  ```
{
 "cadre": {
  "exacts": 20,
  "taux": 0.4348,
  "exacts_non_vides": 17,
  "exacts_vides": 3,
  "partiels": 42,
  "partiels_taux": 0.913,
  "exacts_stricts": 17,
  "taux_strict": 0.3696,
  "roles_exacts_moyens": 2.0217
 },
 "roles": {
  "exacts": 93,
  "total": 138,
  "taux": 0.6739,
  "cadres_exacts": 20,
  "cadres_exacts_taux": 0.4348,
  "cadres_partiels": 42,
  "justes": 41,
  "attendus": 77,
  "predits": 73,
  "faux_positifs": 32,
  "faux_negatifs": 36,
  "vrais_negatifs": 52,
  "par_role": {
   "agent": {
    "exacts": 30,
    "attendus": 32,
    "predits": 30,
    "justes": 19,
    "faux_positifs": 11,
    "faux_negatifs": 13,
    "vrais_negatifs": 11,
    "taux_exact": 0.6522,
    "precision": 0.6333,
    "rappel": 0.5938,
    "f1": 0.6129
   },
   "predicat": {
    "exacts": 23,
    "attendus": 39,
    "predits": 39,
    "justes": 20,
    "faux_positifs": 19,
    "faux_negatifs": 19,
    "vrais_negatifs": 3,
    "taux_exact": 0.5,
    "precision": 0.5128,
    "rappel": 0.5128,
    "f1": 0.5128
   },
   "lieu": {
    "exacts": 40,
    "attendus": 6,
    "predits": 4,
    "justes": 2,
    "faux_positifs": 2,
    "faux_negatifs": 4,
    "vrais_negatifs": 38,
    "taux_exact":
… [3633 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/restitution_v2.py')\ns=p.read_text(encoding='utf-8')\nold='''    comparaisons = [r[\"comparaison\"] for r in annotes]\n    strictes = [r[\"comparaison_stricte\"] for r in annotes]\n    constant = [r[\"constant_par_type\"] for r in  … [3971 caractères tronqués]`

  ```
ok
restitution v2 — les rôles — banc x
textes 50 · annotés 46 · refus 4 (f14, f15, f16, f17)

cadre principal (agent, prédicat, lieu)
  cadres exacts                20/46       0.4348
  dont non vides               17/46     (0.3696) · vides 3
  cadres partiels              42/46       0.9130
  exacts stricts (1re var.)    17/46       0.3696
  rôles exacts                93/138      0.6739
  justes / attendus           41/77    
  précision / rappel / F1 0.5616 / 0.5325 / 0.5467
  faux positifs / négatifs 32 / 36

par rôle                  exacts    attendus   prédits   justes   préc.   rappel
  
ERR <class 'TypeError'> 'NoneType' object is not subscriptable
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/restitution_v2.py')\ns=p.read_text(encoding='utf-8')\nold='''            \"exacts_non_vides\": sum(\n                1 for r in annotes\n                if r[\"comparaison\"][\"exacts\"] == 3\n                and any(_variante_de(r … [817 caractères tronqués]`

  ```
ok
partiel 0 {'exacts': 0, 'taux': 0.0, 'exacts_non_vides': 0, 'exacts_vides': 0, 'partiels': 0, 'partiels_taux': 0.0, 'exacts_stricts': 0, 'taux_strict': 0.0, 'roles_exacts_moyens': 0.0}
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/restitution_v2.py')\ns=p.read_text(encoding='utf-8')\nold='''    s = rapport[\"synthese\"]\n    n = s[\"annotations\"]\n    cadre = s[\"cadre\"]\n'''\nnew='''    s = rapport[\"synthese\"]\n    n = s[\"annotations\"]\n    n_or = s.g … [2564 caractères tronqués]`

  ```
ok
restitution v2 — les rôles — banc reports/pensee-fiabilite-produit.json
textes 50 · annotés 46 · refus 4 (f14, f15, f16, f17)

cadre principal (agent, prédicat, lieu)
  cadres exacts                20/46       0.4348
  dont non vides               17/46     (0.3696) · vides 3
  cadres partiels              42/46       0.9130
  exacts stricts (1re var.)    17/46       0.3696
  rôles exacts                93/138      0.6739
  justes / attendus           41/77    
  précision / rappel / F1 0.5616 / 0.5325 / 0.5467
  faux positifs / négatifs 32 / 36

par rôle                  exacts    attendus   prédits   justes   préc.   rappel
  agent                     30/46         32        30       19  0.6333   0.5938
  prédicat                  23/46         39        39       20  0.5128   0.5128
  lieu                      40/46          6         4        2  0.5000   0.3333

segments de rôle 198 · agents 43 · prédicats 143 · lieux 12 · cadres 139
textes avec au moins un rôle : 40/46 (0.8696)
spans de rôle dans la source : 198/198 (1.0000)

contrôle vide            : 61/138 rôles exacts · cadres exacts 7/46
contrôle constant (type) : 68/138 rôles exacts · cadres exacts 6/46
contrôle rôles 
… [52 caractères tronqués]
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"test_restitution_v2.py — la restitution v2 (D2) : les rôles agent / prédicat / lieu.\n\nCe que le test fige :\n- `drave restituer TEXTE --roles` rend un cadre principal lisible et un JSON v2 ;\n- `relire_roles(rendre_roles(a))` redonne le cadre principal (c … [10248 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_restitution_v2.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 -m unittest tools.tests.test_restitution_v2 -v 2>&1 | tail -60", "description": "Run v2 tests"}`

  ```
test_gold_sans_banc_refuse (tools.tests.test_restitution_v2.TestCommandeRoles.test_gold_sans_banc_refuse) ... ok
test_restituer_roles (tools.tests.test_restitution_v2.TestCommandeRoles.test_restituer_roles) ... ok
test_restituer_roles_json (tools.tests.test_restitution_v2.TestCommandeRoles.test_restituer_roles_json) ... ok
test_roles_et_canonique_exclusifs (tools.tests.test_restitution_v2.TestCommandeRoles.test_roles_et_canonique_exclusifs) ... ok
test_gold_analyseur (tools.tests.test_restitution_v2.TestGoldExterne.test_gold_analyseur) ... ok
test_sans_or (tools.tests.test_restitution_v2.TestMesureSansOr.test_sans_or) ... ok
test_cas_connus (tools.tests.test_restitution_v2.TestOrEtBanc.test_cas_connus) ... ok
test_controles_v2 (tools.tests.test_restitution_v2.TestOrEtBanc.test_controles_v2) ... ok
test_or_46_textes (tools.tests.test_restitution_v2.TestOrEtBanc.test_or_46_textes) ... ok
test_roles_par_role (tools.tests.test_restitution_v2.TestOrEtBanc.test_roles_par_role) ... ok
test_synthese_v2 (tools.tests.test_restitution_v2.TestOrEtBanc.test_synthese_v2) ... ok
test_controle_negatif_rendu (tools.tests.test_restitution_v2.TestRenduRoles.test_controle_negatif_rendu) ... ok
test_co
… [505 caractères tronqués]
  ```

- **bash** `{"command": "python3 -m unittest tools.tests.test_restitution -v 2>&1 | tail -40", "description": "Run existing restitution tests"}`

  ```
test_50_textes_46_annotations (tools.tests.test_restitution.TestCinquanteTextes.test_50_textes_46_annotations) ... ok
test_stabilite_et_controles_v1 (tools.tests.test_restitution.TestCinquanteTextesV1.test_stabilite_et_controles_v1) ... ok
test_structure_v1 (tools.tests.test_restitution.TestCinquanteTextesV1.test_structure_v1) ... ok
test_synthese_v1 (tools.tests.test_restitution.TestCinquanteTextesV1.test_synthese_v1) ... ok
test_restituer_banc (tools.tests.test_restitution.TestCommande.test_restituer_banc) ... ok
test_restituer_banc_canonique (tools.tests.test_restitution.TestCommande.test_restituer_banc_canonique) ... ok
test_restituer_canonique (tools.tests.test_restitution.TestCommande.test_restituer_canonique) ... ok
test_restituer_canonique_json (tools.tests.test_restitution.TestCommande.test_restituer_canonique_json) ... ok
test_restituer_json (tools.tests.test_restitution.TestCommande.test_restituer_json) ... ok
test_restituer_multiligne (tools.tests.test_restitution.TestCommande.test_restituer_multiligne) ... ok
test_restituer_refus (tools.tests.test_restitution.TestCommande.test_restituer_refus) ... ok
test_restituer_texte (tools.tests.test_restitution.TestCommande.test_
… [1157 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py restituer --help | sed -n '1,80p'; echo ===; python3 tools/drave.py --version", "description": "Check CLI help and version"}`

  ```
usage: drave restituer [-h] [--banc CHEMIN] [--canonique] [--roles] [--gold CHEMIN]
                       [--fichier CHEMIN] [--langue {fr,en}] [--contexte CONTEXTE] [--json]
                       [TEXTE]

Analyse un texte, reconstruit la surface depuis le niveau `graphème` (sans lire le champ `texte` de l'annotation) et compare à la source. Affiche la fidélité binaire du miroir, la fidélité de caractères et un contrôle négatif. Avec --canonique, produit en plus la forme canonique v1 (segments + rôles + cibles) et son miroir canonique ; avec --roles, produit la forme lisible des rôles (agent, prédicat, lieu) et, sur un banc, leur fidélité à un or écrit à la main.

arguments:
  TEXTE                texte à restituer (entre guillemets) ou --fichier

options:
  -h, --help, --aide   afficher cette aide et quitter
  --banc CHEMIN        mesurer un banc JSON de textes (ex. les 50 textes libres)
  --canonique          ajouter la forme canonique v1 (segments + rôles + cibles) et son miroir
                       canonique
  --roles              ajouter la forme lisible des rôles (agent, prédicat, lieu) ; avec --banc,
                       mesurer leur fidélité à l'or
  --gold CHEMIN    
… [706 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln 'Verdict.*❌\\|Verdict.*négatif\\|Verdict.*⚠' reports/*.md | head -20; echo ===; grep -rn 'Verdict' reports/rapport-atomes-niveaux.md reports/rapport-*.md 2>/dev/null | grep -v '✅' | head -20", "description": "Find negative verdict style"}`

  ```
reports/rapport-a26-bilan.md
reports/rapport-a80-portes-ppl.md
reports/rapport-a83-defaut.md
reports/rapport-atomes-prediction.md
reports/rapport-audit-attachement.md
reports/rapport-audit-r1r3.md
reports/rapport-audit-v10.md
reports/rapport-b13-porte-134.md
reports/rapport-c9-lateralite.md
reports/rapport-classement-appris.md
reports/rapport-coherence-fiches.md
reports/rapport-coherence-fiches-v7.md
reports/rapport-coherence-fiches-v8.md
reports/rapport-etat-a.md
reports/rapport-etat-r.md
reports/rapport-fiabilite-produit.md
reports/rapport-frontieres-phrase.md
reports/rapport-g017.md
reports/rapport-gold-anglais.md
reports/rapport-n2-distillation.md
===
reports/rapport-8bits.md:38:## Verdict
reports/rapport-a26-bilan.md:3:> **Ligne de roadmap** : A2.6 · **Date** : 2026-10-29 · **Verdict** : ⚠️ **partielle** — la règle
reports/rapport-a26-lot-disque.md:3:> **Verdict.** Sur un modèle **dense** de 0,5 Go (Qwen2.5-0.5B-Q8), avec l'**éviction du cache**
reports/rapport-a80-indice-qualifie.md:3:> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **Verdict** : ⛔ **rouge confirmée** —
reports/rapport-a80-melange-qualifie.md:3:> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-29 · **
… [1744 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-restitution-v2.json'))\ns=d['synthese']\nprint('exacts:', [r['id'] for r in d['resultats'] if r.get('comparaison') and r['comparaison']['exacts']==3])\nprint('non vides:', [r['id'] for r in d['resultats'] if r.get('comparai … [640 caractères tronqués]`

  ```
exacts: ['f01', 'f02', 'f04', 'f05', 'f06', 'f07', 'f10', 'f11', 'f18', 'f21', 'f23', 'f26', 'f28', 'f29', 'f30', 'f34', 'f37', 'f40', 'f45', 'f46']
non vides: ['f01', 'f02', 'f04', 'f05', 'f06', 'f07', 'f10', 'f11', 'f21', 'f23', 'f26', 'f28', 'f29', 'f30', 'f34', 'f45', 'f46']
zeros: ['f08', 'f20', 'f24', 'f50']
f03 pred ('Comment', 'Bonjour', '') or ('vous', 'allez', '') exacts 1
f20 pred ('Leroy', 'M', 'vers 9 h') or ('M. Dupont, le Dr Martin et Mme Leroy', 'sont arrivés', '') exacts 0
f27 pred ('', '', '') or ('Élodie', 'sourit', '') exacts 1
f35 pred ('The quick brown fox', 'jumps', '') or ('The quick brown fox', 'jumps', 'over the lazy dog') exacts 2
f41 pred ('Le texte contient', 'ß ñ ø å et', '') or ('Le texte', 'contient', '') exacts 1
f49 pred ('La réunion', 'est reportée', '') or ('La réunion', 'est reportée', 'salle B12') exacts 2
f50 pred ('il', 'Notes', 'dans la cour') or ('Le chat de la voisine', 'se réveille', '') exacts 0
  ```

- **write** `{"content": "# B13 — la restitution v2 : les rôles se lisent, leur fidélité ne suit pas\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : D2 · **Date** : 2026-11-15 ·\n> **Verdict** : ❌ **négatif sur la fidélité** — la forme est fidèle (46/46), la sémantique\n> ne l'est pas : **20/46 cadre … [17123 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-restitution-v2.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\ng=json.load(open('tools/tests/linguistique/gold_restitution_v2.json'))\nprint(len(g['textes']), sum(len(t['variantes']) for t in g['textes']))\nprint(sum(1 for t in g['textes'] if len(t['variantes'])>1))\nPY", "description": "Count gold variants"}`

  ```
46 65
18
  ```

- **bash** `{"command": "grep -rn '74' reports/rapport-restitution-v2.md tools/restitution_v2.py tools/mesurer_restitution_v2.py | head -20", "description": "Find stale 74 references"}`

  ```
reports/rapport-restitution-v2.md:105:**46 cadres**, **74 variantes**, un cadre principal par texte, écrit depuis le texte et non
reports/rapport-restitution-v2.md:321:  cadres, 74 variantes.
tools/mesurer_restitution_v2.py:33:    "74 variantes. Il ne note ni les subordonnées, ni les seconds cadres, ni les rôles "
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-restitution-v2.json'))\nprint([r['id'] for r in d['resultats'] if not r.get('refus') and not r['controle_negatif_rendu']['eligible']])\nprint([r['id'] for r in d['resultats'] if not r.get('refus') and not r['roles']['princi … [68 caractères tronqués]`

  ```
['f08', 'f09', 'f18', 'f27', 'f33', 'f37', 'f40']
['f08', 'f09', 'f18', 'f27', 'f33', 'f37', 'f40']
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nfor p in ['reports/rapport-restitution-v2.md','tools/mesurer_restitution_v2.py']:\n f=pathlib.Path(p); s=f.read_text(encoding='utf-8'); s=s.replace('74 variantes','65 variantes'); f.write_text(s,encoding='utf-8')\nprint('ok')\nPY\ngrep -rn '65 variantes … [115 caractères tronqués]`

  ```
ok
reports/rapport-restitution-v2.md:105:**46 cadres**, **65 variantes**, un cadre principal par texte, écrit depuis le texte et non
reports/rapport-restitution-v2.md:321:  cadres, 65 variantes.
tools/mesurer_restitution_v2.py:33:    "65 variantes. Il ne note ni les subordonnées, ni les seconds cadres, ni les rôles "
  ```

- **bash** `{"command": "python3 -m py_compile tools/restitution_v2.py tools/mesurer_restitution_v2.py tools/drave.py tools/tests/test_restitution_v2.py && echo OK", "description": "Compile new and changed Python files"}`

  ```
OK
  ```

- **bash** `{"command": "python3 tools/mesurer_restitution_v2.py >/tmp/v2.out && tail -8 /tmp/v2.out && python3 -c \"import json; d=json.load(open('reports/pensee-restitution-v2.json')); print(len(d['limites']), d['limites'][0][:80])\"", "description": "Regenerate JSON and check limits"}`

  ```
contrôle constant (type) : 68/138 rôles exacts · cadres exacts 6/46
contrôle rôles mélangés  : 27/138 rôles exacts · cadres exacts 3/46
restitution du rendu     : 46/46 (1.0000)
contrôle négatif rendu   : 39/39 éligibles détectés

contrôle externe (gold S) : 139/144 (0.9653) · baseline 104/144 (0.7222)

écrit : reports/pensee-restitution-v2.json
8 L'or ne note que le **cadre principal** (agent, prédicat, lieu) : 46 textes, 46
  ```

- **bash** `{"command": "sed -n '1,240p' tools/porte-produit.sh", "description": "Inspect product gate"}`

  ```
#!/usr/bin/env bash
# porte-produit — le premier produit : la CLI répond, le JSON est valide, le rejeu est identique.
#
# Ce qu'elle vérifie : `drave --version`, `analyser` (fr et en) rend un JSON parsable avec des
# étiquettes, `rejouer` rend le même sha256 deux fois, et le smoke test passe.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
ko=0
dit() { printf '  %s %s\n' "$1" "$2"; }

ver=$(python3 tools/drave.py --version 2>&1)
case "$ver" in drave*) dit ✅ "version : $ver" ;; *) dit ❌ "version : $ver"; ko=1 ;; esac

for langue in fr en; do
  case "$langue" in
    fr) texte="Le chat dort sur le toit." ;;
    en) texte="The cat sleeps on the roof." ;;
  esac
  sortie=$(python3 tools/drave.py analyser "$texte" --langue "$langue" --json 2>&1)
  if printf '%s' "$sortie" | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['langue'] == '$langue', d.get('langue')
assert len(d['etiquettes']) > 5, len(d['etiquettes'])
assert any(e['niveau'] == 'syntagme' for e in d['etiquettes'])
assert any(e['niveau'] == 'pos' for e in d['etiquettes'])
" 2>/dev/null; then
    dit ✅ "analyser $langue : JSON valide, étiquettes et syntagmes"
  else
    dit ❌ "analyser $langue : JSON invalide 
… [3266 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/porte-produit.sh')\ns=p.read_text(encoding='utf-8')\nold='''if python3 tools/tests/test_restitution.py >/tmp/porte-produit-restitution.log 2>&1; then\n  dit ✅ \"restitution v0/v1 : $(grep -oE 'Ran [0-9]+ tests' /tmp/porte-produit-r … [1618 caractères tronqués]`

  ```
ok

if sortie=$(python3 tools/drave.py restituer "Le chat dort." 2>&1) \
   && printf '%s' "$sortie" | grep -q "exacte 1.0000"; then
  dit ✅ "restitution v0 : surface exacte (miroir affiché)"
else
  dit ❌ "restitution v0 : sortie inattendue : $sortie"; ko=1
fi

if sortie=$(python3 tools/drave.py restituer "Le chat dort." --canonique --json 2>&1) \
   && printf '%s' "$sortie" | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['schema'] == 'drave.restitution.canonique', d.get('schema')
assert d['forme']['surface_canonique'] == 'le chat dort', d['forme']['surface_canonique']
assert d['canonique']['exact'], d['canonique']
assert not d['strict']['exact'], d['strict']
" 2>/dev/null; then
  dit ✅ "restitution v1 : forme canonique exacte, miroir strict distinct"
else
  dit ❌ "restitution v1 : sortie inattendue : $sortie"; ko=1
fi

if sortie=$(python3 tools/drave.py restituer "Le chat dort." --roles --json 2>&1) \
   && printf '%s' "$sortie" | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['schema'] == 'drave.restitution.v2', d.get('schema')
assert d['roles']['principal']['agent'] == 'Le chat', d['roles']['principal']
assert d['roles']['principal']['predicat'
… [1232 caractères tronqués]
  ```

- **bash** `{"command": "bash tools/porte-produit.sh 2>&1 | tail -30", "description": "Run product gate", "timeoutMs": 180000}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f4b7822076a4203d deux fois
  ✅ smoke test : Ran 20 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v2 : rôles lisibles, rendu relu, contrôle détecté
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 16 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
  ```

- **bash** `{"command": "sed -n '30,75p' docs/pilotage/roadmap.md; echo ===; sed -n '370,420p' docs/pilotage/roadmap.md", "description": "Inspect roadmap B13 and R3 sections"}`

  ```
| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.6 partiel ; A3.2/A3.3 mesurées ; **A8.3c/d expliqués** ; **A2.6/A8.3 : le [lot](../theorie/glossaire/entrees/lot.md) ne divise pas les lectures denses (+27 % calcul, PPL −0,006 %)** | **A2.6** (experts : A6.2 bloqué) ; le lot ≥ 2 assumé |
| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seu
… [17939 caractères tronqués]
  ```

- **bash** `{"command": "ls -lt journal | head -20; echo ===; find journal -maxdepth 2 -type f -name '*.md' | sort | tail -20", "description": "Inspect journal structure"}`

  ```
total 88
-rw-r--r--. 1 stephane stephane 33075 15 nov 04:51 THEMES.md
-rw-r--r--. 1 stephane stephane 50728 15 nov 04:51 README.md
drwxr-xr-x. 1 stephane stephane 15112 15 nov 04:46 sessions
drwxr-xr-x. 1 stephane stephane    94 15 nov 04:46 2026-11-15
drwxr-xr-x. 1 stephane stephane   132 14 nov 06:59 2026-11-14
drwxr-xr-x. 1 stephane stephane    76 13 nov 23:10 2026-11-13
drwxr-xr-x. 1 stephane stephane   132  7 nov 15:13 2026-11-07
drwxr-xr-x. 1 stephane stephane   168  6 nov 22:24 2026-11-06
drwxr-xr-x. 1 stephane stephane   174  5 nov 10:24 2026-11-05
drwxr-xr-x. 1 stephane stephane   180  4 nov 23:37 2026-11-04
drwxr-xr-x. 1 stephane stephane   224  3 nov 16:48 2026-11-03
drwxr-xr-x. 1 stephane stephane   224  2 nov 20:13 2026-11-02
drwxr-xr-x. 1 stephane stephane   244  1 nov 22:30 2026-11-01
drwxr-xr-x. 1 stephane stephane   182 31 oct 23:28 2026-10-31
drwxr-xr-x. 1 stephane stephane   150 31 oct 11:22 2026-10-30
drwxr-xr-x. 1 stephane stephane   208 29 oct 17:08 2026-10-29
drwxr-xr-x. 1 stephane stephane   150 28 oct 14:12 2026-10-12
drwxr-xr-x. 1 stephane stephane   192 28 oct 14:12 2026-10-11
drwxr-xr-x. 1 stephane stephane   288 28 oct 14:12 2026-10-10
===
journal/2026-
… [549 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' journal/2026-11-15/README.md; echo ===; sed -n '1,160p' journal/2026-11-15/mesures.md; echo ===; sed -n '1,120p' journal/2026-11-15/docs.md", "description": "Read today's journal entries"}`

  ```
# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**14 commits** · **1 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 3 | [distribue.md](distribue.md) |
| docs | 3 | [docs.md](docs.md) |
| mesures | 7 | [mesures.md](mesures.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 348.1 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTI
… [10366 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('**Mis à jour : 2026-11-15, 05 h 00 HNE (D1)**','**Mis à jour : 2026-11-15, 05 h 30 HNE (D2)**')\n# session fait\nold='''- **Fait** : B13 **183/183** ; **POS 86,25 … [3709 caractères tronqués]`

  ```
ok
3:**Mis à jour : 2026-11-15, 05 h 30 HNE (D2)**
64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **restitution v2** (rôles lisibles 46/46, fidélité **17/46** non vides, F1 **0,5467** ; [fiche](../../reports/rapport-restitution-v2.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)) ; **D1** ([fiche](../../reports/rapport-exemples-tagger.md)).
90:- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejeté** (g017 à trancher), schéma v2, restitution v1 (46/46, strict 0,1087), **restitution v2** (rôles lisibles 46/46, fidélité 17/46, F1 0,5467), **J9.1** (19 fiches), **D1** ; [s065](../../reports/rapport-s065.md), [restitution v1](../../reports/rapport-restitution-v1.md), [restitution v2](../../reports/rapport-restitu
… [460 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nr=pathlib.Path('reports')\nprint('md',len(list(r.glob('*.md'))),'json',len(list(r.glob('*.json'))))\ndocs=[p for p in pathlib.Path('docs').rglob('*.md') if 'archive' not in p.parts and p.name!='README.md']\nprint('docs',len(docs))\nPY", "description": " … [24 caractères tronqués]`

  ```
md 744 json 838
docs 458
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('**743** / **837**','**744** / **838**')\np.write_text(s,encoding='utf-8')\np=pathlib.Path('docs/pilotage/roadmap.md')\ns=p.read_text(encoding='utf-8')\nold='''**S … [1900 caractères tronqués]`

  ```
ok
46:**D2 — la restitution v2 (15/11 05 h 30).** Les **rôles** (agent, prédicat, lieu) se **lisent** :
docs/pilotage/en-cours.md:109:| fichiers / JSON de résultats | **744** / **838** | `reports/*.md` / `reports/*.json` |
docs/pilotage/roadmap.md:44:CEGEP **91 scans uniques**, 1 982 p). **Passe** : 84 portes, **81/3**, 1 h 30 (00 h 30) ; les rouges tolérées sont `indice` et `melange` (structurelles), `sessions` est revérifiée verte ; compteurs **744 fiches / 838 JSON**.
  ```

- **bash** `{"command": "sed -n '36,62p' docs/pilotage/roadmap.md", "description": "Verify roadmap insertion context"}`

  ```
| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67,73 G car., 81,2 Go, **8 Ko 0**) ; **PDF** (1 927 doc., 322 Mo) ; **documents** (3 384 doc., 872 M car., 8 Ko 2,07 %) ; **OCR** (20 livres, 7 381 p, 15,36 M, 8 Ko 0 ; [CEGEP](../theorie/glossaire/entrees/cegep.md) **91 scans uniques**, 60 documents, 1 982 p, 4,41 M car., 8 Ko 0) ; **genres** mesurés | **l'OCR est clos** (limite : 8 scans `.PDF`, 58 p) ; la préparation **R1.1/R1.2** (N2) et **A2.6** (A) |

**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du GV : 238/238, 0 span, 0 POS ; [fiche](../../reports/rapport-s065.md)) ; **183/183** ; **`r035`** (relative zéro) réglé ; **convention des GV** réglée (sujet hors du GV + adverbe final : GV F1 0,7549 → 0,7902, 0 perte d'attachement) ; **contrat v2 publié et validé** (`meta.partition`/`meta.alternative`, version 2, **v1 lue** : 26 cas, 0 échec) ; **restitution v1** (`restituer --canonique`
… [4191 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('journal/2026-11-15/mesures.md')\ns=p.read_text(encoding='utf-8')\nnote='''\n### D2 — la restitution v2 : les rôles se lisent, leur fidélité ne suit pas\n\nLa v2 devait passer de la surface (v0) et de la forme canonique (v1) aux **rôles** … [1332 caractères tronqués]`

  ```
ok
<!-- notes -->

### D2 — la restitution v2 : les rôles se lisent, leur fidélité ne suit pas

La v2 devait passer de la surface (v0) et de la forme canonique (v1) aux **rôles**. Elle le fait
comme **forme** : `restituer --roles` rend un cadre `agent / prédicat / lieu`, 198 segments de rôle,
**198/198** spans dans la source, et `relire_roles(rendre_roles(a))` redonne le cadre **46/46**.
Mais la **fidélité** ne suit pas. Sur un or écrit à la main (46 cadres, 65 variantes), **20/46**
cadres sont exacts — **17/46** non vides —, **93/138** cellules exactes, mais **F1 0,5467**
(précision 0,5616, rappel 0,5325, **32 faux positifs / 36 faux négatifs**) ; **agent 0,6129**,
**prédicat 0,5128**, **lieu 0,4000**. Les planchers : vide **7/46**, constant par type **6/46**,
rôles mélangés **3/46**. Le contrôle externe (gold S, 61 phrases) vaut **139/144 = 0,9653** :
l'instrument n'est pas cassé ; c'est la lecture des rôles de l'annotation qui ne tient pas.
`f03` lit `Comment / Bonjour`, `f20` lit `Leroy / M / vers 9 h`, `f27` (« Élodie sourit. ») n'a
aucun syntagme. La v2 est une **vue fidèle de rôles faux ou absents**, pas un analyseur.
[`fiche`](../../reports/rapport-restitution-v2.md) · [`JS
… [64 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/roadmap.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('porte produit **13 contrôles** (16 + 8 + 4 + 22 tests)','porte produit **15 contrôles** (dont 16 tests v2)')\np.write_text(s,encoding='utf-8')\nprint('ok')\nPY\ngr … [110 caractères tronqués]`

  ```
ok
38:**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du GV : 238/238, 0 span, 0 POS ; [fiche](../../reports/rapport-s065.md)) ; **183/183** ; **`r035`** (relative zéro) réglé ; **convention des GV** réglée (sujet hors du GV + adverbe final : GV F1 0,7549 → 0,7902, 0 perte d'attachement) ; **contrat v2 publié et validé** (`meta.partition`/`meta.alternative`, version 2, **v1 lue** : 26 cas, 0 échec) ; **restitution v1** (`restituer --canonique` : **46/46 formes canoniques exactes** contre la source canonisée, **miroir strict 0,1087 inchangé**, **395 segments / 395 rôles / 315 cibles dont 315 résolues**, stabilité **18/46** ; le strict ne monte pas, la v1 n'est pas la surface ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J9.1 passe d'honnêteté** (**19** fiches « instantané historique » : 10 encarts réécrits, 9 ajoutés ; **0 fiche de résultats** ne publie les quatre marqueurs sans mention, hors 2 faux positifs ; [fiche](../../reports/rapport-passe-honnetete.md)), porte produit **15 contrôles** (dont 16 tests v2) ; frontières de
… [329 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -80", "description": "Run documentation review", "timeoutMs": 180000}`

  ```
revue de documentation · 744 fiche(s) · 838 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -40", "description": "Run table gate", "timeoutMs": 120000}`

  ```
✅ 1816 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4410 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --roles --json | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['schema'], d['synthese']['annotations'], d['synthese']['cadre']['exacts_non_vides'], d['synthese']['roles']['exacts'])\"", "descri … [36 caractères tronqués]`

  ```
drave.restitution.v2.banc 46 17 93
  ```

- **bash** `{"command": "python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --roles --gold tools/tests/linguistique/gold_restitution_v2.json >/dev/null && echo OK", "description": "Check explicit gold option"}`

  ```
OK
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -30; echo ===; python3 tools/verifie_journal.py 2>&1 | tail -30", "description": "Check state and journal consistency"}`

  ```
en-cours · 1686 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
===
  journal · 47 jour(s) · 201 session(s) · 2573 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -30; echo ===; python3 tools/verifier_schemas.py 2>&1 | tail -20", "description": "Check document size and schemas"}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    9136    504   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2463    221   T1   2800  reports/README.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [750 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib,re\ns=pathlib.Path('docs/pilotage/roadmap.md').read_text(encoding='utf-8')\ni=s.index('**D2 — la restitution v2')\nj=s.index('**J3.2**',i)\npar=s[i:j]\nprint('mots D2',len(par.split()))\nprint(par)\nPY", "description": "Count D2 roadmap paragraph words"}`

  ```
mots D2 144
**D2 — la restitution v2 (15/11 05 h 30).** Les **rôles** (agent, prédicat, lieu) se **lisent** :
`restituer --roles` rend un cadre principal, 198 segments de rôle et un rendu relu **46/46** ; les
**198/198** spans sont dans la source. Leur **fidélité** ne suit pas : sur un or écrit à la main
(46 cadres, 65 variantes), **20/46** cadres exacts — **17/46** non vides —, **93/138** cellules
exactes mais **F1 0,5467** (précision 0,5616, rappel 0,5325, **32 faux positifs / 36 faux
négatifs**) ; **agent 0,6129**, **prédicat 0,5128**, **lieu 0,4000**. Contrôles : vide **7/46**,
constant par type **6/46**, rôles mélangés **3/46** ; contrôle externe gold S **139/144 = 0,9653**.
Le négatif est nommé : la v2 est une **vue fidèle de rôles faux ou absents**, pas un analyseur ;
la prochaine action est la **qualité des rôles** de l'analyseur, pas le format. [Fiche](../../reports/rapport-restitution-v2.md)
· [JSON](../../reports/pensee-restitution-v2.json).
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\n# roadmap: remove separate D2 paragraph and add a short sentence in the B13 state paragraph\np=pathlib.Path('docs/pilotage/roadmap.md')\ns=p.read_text(encoding='utf-8')\nstart=s.index('\\n**D2 — la restitution v2')\nend=s.index('\\n**J3.2**',start)\npar … [1469 caractères tronqués]`

  ```
ok
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4017 mots (budget 4 000)

  avertissements :
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4017 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "grep -n 'restitution v2\\|qualité des rôles' docs/pilotage/en-cours.md", "description": "Locate v2 mentions in state"}`

  ```
90:- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejeté** (g017 à trancher), schéma v2, restitution v1 (46/46, strict 0,1087), **restitution v2** (17/46, F1 0,5467), **J9.1** (19 fiches), **D1** ; [s065](../../reports/rapport-s065.md), [restitution v1](../../reports/rapport-restitution-v1.md), [restitution v2](../../reports/rapport-restitution-v2.md), [J9.1](../../reports/rapport-passe-honnetete.md).
131:**N2** — porte (0,2856/0,3566) ; **Pensée** — `g017`, T132/T133, gold 200+, **qualité des rôles** (restitution v2 : 17/46, F1 0,5467) ; **J3.2** — V14 des 21 langues ; **J7.1** — réplication neuronale ; **S** — migration `/` v7 (106/41) ; référents ; **R0.7** — split réel ; **A** — A6.2, A8.3b2.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('schéma v2, restitution v1 (46/46, strict 0,1087), **restitution v2** (17/46, F1 0,5467), **J9.1**', 'schéma v2, **restitution v2** (17/46, F1 0,5467), **J9.1**')\ … [456 caractères tronqués]`

  ```
ok
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4004 mots (budget 4 000)

  avertissements :
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4004 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('**restitution v2** (17/46, F1 0,5467), **J9.1**', '**restitution v2** ([fiche](../../reports/rapport-restitution-v2.md)), **J9.1**')\n# remove the duplicate link  … [353 caractères tronqués]`

  ```
ok

  avertissements :
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4002 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "sed -n '90p' docs/pilotage/en-cours.md", "description": "Inspect state line"}`

  ```
- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejeté** (g017 à trancher), schéma v2, **restitution v2** ([fiche](../../reports/rapport-restitution-v2.md)), **J9.1** (19 fiches), **D1** ; [s065](../../reports/rapport-s065.md), [restitution v2](../../reports/rapport-restitution-v2.md), [J9.1](../../reports/rapport-passe-honnetete.md).
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('[s065](../../reports/rapport-s065.md), [restitution v2](../../reports/rapport-restitution-v2.md), [J9.1]', '[s065](../../reports/rapport-s065.md), [J9.1]')\np.wri … [134 caractères tronqués]`

  ```
T0 max : 4000 mots (budget 4 000)

  avertissements :
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -20", "description": "Re-run documentation review", "timeoutMs": 180000}`

  ```
revue de documentation · 744 fiche(s) · 838 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -10; echo ===; python3 tools/verifie_en_cours.py 2>&1 | tail -5; echo ===; python3 tools/verifie_journal.py 2>&1 | tail -5", "description": "Re-run tables, state, journal checks", "timeoutMs": 120000}`

  ```
✅ 1816 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4410 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
===
  en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
===
  journal · 47 jour(s) · 201 session(s) · 2573 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "bash tools/toutes-les-portes.sh 2>&1 | tail -120", "description": "Run all repository gates", "timeoutMs": 900000}`

  ```
[still running after 600000ms; moved to background job bash-111]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "git status --short | sed -n '1,120p'; echo ===; git diff --stat -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md tools/drave.py tools/porte-produit.sh journal/2026-11-15/mesures.md", "description": "Inspect working tree and diff stats"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M journal/2026-11-15/mesures.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-e73a3601-e2c6-417c-a009-88ffadca4e61/digest.md
 M journal/sessions/session-e73a3601-e2c6-417c-a009-88ffadca4e61/rapport.md
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
 M tools/porte-produit.sh
?? journal/sessions/session-53896e61-4a68-417d-89e0-de0de156949b/
?? reports/pensee-restitution-v2.json
?? reports/rapport-gold-reel-50.json
?? reports/rapport-gold-reel-50.md
?? reports/rapport-restitution-v2.md
?? reports/rapport-s-paragraphes.md
?? tools/mesurer_restitution_v2.py
?? tools/restitution_v2.py
?? tools/tests/linguistique/gold_reel_50.py
?? tools/tests/linguistique/gold_restitution_v2.json

… [362 caractères tronqués]
  ```

- **bash** `{"command": "git diff --stat -- journal/README.md journal/sessions/MANIFEST.md journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md journal/sessions/session-e73a3601-e2c6-417c-a009-88ffadca4e61/digest.md journal/sessions/ses … [153 caractères tronqués]`

  ```
journal/README.md                                  |  5 +-
 journal/sessions/MANIFEST.md                       |  7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 27 ++++++
 .../rapport.md                                     | 14 ++--
 .../digest.md                                      | 98 ++++++++++++++++++++++
 .../rapport.md                                     | 54 ++++++++++--
 6 files changed, 186 insertions(+), 19 deletions(-)
===
diff --git a/journal/README.md b/journal/README.md
index a6905ad3..9e051278 100644
--- a/journal/README.md
+++ b/journal/README.md
@@ -213,7 +213,7 @@ de la session ; le `digest.md` voisin en donne le verbatim complet.
 | `ddf8d740` | Tâche autonome de mesure, dans | 2026-10-22 08:28 | 0.1 h | 1 | 14 | 0 | 0 | [rapport](sessions/ddf8d740-9433-4f97-a5d8-38bd92bd45f6/rapport.md) |
 | `df1b1098` | Tu es relecteur visuel de | 2026-10-31 17:52 | 0.0 h | 1 | 0 | 0 | 0 | [rapport](sessions/df1b1098-d54e-4763-bfc2-2a8cc1498cec/rapport.md) |
 | `e14c26ae` | Tu es relecteur ADVERSARIAL, en | 2026-10-02 21:15 | 0.2 h | 1 | 76 | 1 | 0 | [rapport](sessions/e14c26ae-6d52-41f9-a72f-6ebdcef172d5/rapport.md) |
-| `e181ce02` | Documentation Drave avec diag
… [3703 caractères tronqués]
  ```

- **bash** `{"command": "find journal/sessions/session-53896e61-4a68-417d-89e0-de0de156949b -maxdepth 1 -type f -printf '%f\\n'; echo ===; sed -n '1,120p' journal/sessions/session-53896e61-4a68-417d-89e0-de0de156949b/rapport.md; echo ===; sed -n '1,80p' journal/sessions/session-53896e61-4a68-417d-89e0-de0de1569 … [66 caractères tronqués]`

  ```
session.v4.jsonl.zstd
digest.md
rapport.md
===
# Session session- — Restitution v2 : rôles et fidélité

> **Journaux :** [le jour](../../2026-11-15/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-53896e61-4a68-417d-89e0-de0de156949b` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-15 04:53 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 105 |
| Appels d'outils | 125 |
| Fichiers touchés | 4 |
| Commandes | 111 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche D2 : la restitution v2 — au-delà de la surface exacte (v0) et de la forme canonique (v1), restitue les **rôles** (agent, prédicat, lieu) dans une forme lisible et mesure la fidélité des rôles sur les 46 textes de la v0 ; fiche `reports/rapport-restitution-v2.md` + JSON, tests, commit. Si les rôles ne se restituent pas, écris le négatif.

## 2. Déroulé, étape par étape

### Tour 1 — Tâche D2 : la restitution v2 — au-delà de la surface exacte (v0) et de la forme canonique (v1), restitue les **rôles** ( … [224 caractères tronq
… [11414 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/journal_auto.py; grep -n 'def main\\|argparse\\|--' tools/journal_auto.py | tail -20", "description": "Inspect journal auto tool"}`

  ```
#!/usr/bin/env python3
"""journal_auto.py — le journal quotidien, ÉCRIT PAR JOUR (UN DOSSIER) ET PAR THÈME, à partir de git et des sessions.

POURQUOI. Le journal doit consigner les **événements datés** (voir
`docs/organisation-du-depot.md`), et une journée de ce dépôt est trop riche pour un seul
fichier : un jour touche le moteur, les protocoles, les mesures, les portes et la
documentation. D'où le découpage **`<AAAA-MM-JJ>_<thème>.md`** : on lit la journée d'un thème,
et on suit un thème **d'un jour à l'autre** (le nom commence par la date, le thème suit —
`ls journal/2026-10-1*/attention.md`).

SOURCES, et rien d'autre :
  1. **git** — les commits du jour (heure d'auteur, en heure locale de la machine) et les
     fichiers touchés ; c'est la chronologie **fiable** (les horodatages écrits à la main
     s'étaient retrouvés dans le futur) ;
  2. **journal/sessions/** — les rapports de session dont la fenêtre de temps couvre le jour
     (début et durée lus dans l'index `journal/README.md`, régénéré par
     `tools/session_report.py`) : on en extrait les **titres de tour** classés par thème, avec
     le lien vers le rapport complet.

CE QUI EST PRÉSERVÉ. Tout ce que l'humain (ou l
… [4529 caractères tronqués]
  ```

- **job_list** `{}`

  ```
bash-25 [bash] killed — grep -rln '"f01"\|f01' reports tools data 2>/dev/null | head -60
bash-111 [bash] running — bash tools/toutes-les-portes.sh 2>&1 | tail -120
  ```

- **bash** `{"command": "git check-ignore -v tools/tests/linguistique/gold_restitution_v2.json || true; git ls-files tools/tests/linguistique/gold.py; ls -la tools/tests/linguistique/.git 2>/dev/null || echo 'pas de .git'; cat .gitmodules", "description": "Check gold path tracking"}`

  ```
tools/tests/linguistique/gold.py
pas de .git
[submodule "tools/docwatch"]
	path = tools/docwatch
	url = https://github.com/stephanedenis/docwatch.git
[submodule "tools/structures"]
	path = tools/structures
	url = /home/stephane/Data13TB/stephane/GitHub/drave-structures
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/restitution_v2.py')\ns=p.read_text(encoding='utf-8')\nold='''    return {\n        \"exacts\": sum(c[\"exacts\"] for c in comparaisons),\n        \"total\": 3 * len(comparaisons),\n        \"taux\": _taux(sum(c[\"exacts\"] for c in … [2929 caractères tronqués]`

  ```
ok
[stderr]
----------------------------------------------------------------------
Ran 16 tests in 0.898s

OK
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/restitution_v2.py')\ns=p.read_text(encoding='utf-8')\nold='''def mesurer_banc_v2(items: list[dict], gold: dict) -> dict:\n    \"\"\"Mesure la v2 sur les textes d'un banc et l'or de rôles (`gold[\"textes\"]`).\"\"\"\n    par_id = {g … [1704 caractères tronqués]`

  ```
ok
restitution v2 — les rôles — banc x
textes 50 · annotés 46 · refus 4 (f14, f15, f16, f17)

cadre principal (agent, prédicat, lieu)
  cadres exacts                20/46       0.4348
  dont non vides               17/46     (0.3696) · vides 3
  cadres partiels              42/46       0.9130
  exacts stricts (1re var.)    17/46       0.3696
  rôles exacts                93/138      0.6739
  justes / attendus           41/77    
  précision / rappel / F1 0.5616 / 0.5325 / 0.5467
  faux positifs / négatifs 32 / 36

par rôle                  exacts    attendus   prédits   justes   préc.   rappel
  agent                     30/46         32        30       19  0.6333   0.5938
  prédicat                  23/46         39        39       20  0.5128   0.5128
  lieu                      40/46          6         4        2  0.5000   0.3333

segments de rôle 198 · agents 43 · prédicats 143 · lieux 12 · cadres 139
textes avec au moins un rôle : 40/46 (0.8696)
spans de rôle dans la source : 198/198 (1.0000)

contrôle vide            : 61/138 rôles exacts · cadres exacts 7/46
contrôle constant (type) : 68/138 rôles exacts · cadres exacts 6/46
contrôle rôles mélangés  : 27/138 rôles exacts · ca
… [110 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/drave.py')\ns=p.read_text(encoding='utf-8')\ns=s.replace('''            rapport = restitution_v2.mesurer_banc_v2(items, gold)''','''            rapport = restitution_v2.mesurer_banc_v2(items, gold, args.langue)''')\np.write_text(s, … [200 caractères tronqués]`

  ```
ok
OK
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json, pathlib\nsys.path.insert(0,'.')\nimport tools.restitution_v2 as v2\n# monkey test both languages by adapting function? Just compare a copy quickly\nimport tools.bloc_linguistique as bl\nd=json.load(open('tools/structures/donnees/gold-analyseur.json')) … [795 caractères tronqués]`

  ```
fr 139 144 104
None 139 144 104
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/restitution_v2.py')\ns=p.read_text(encoding='utf-8')\ns=s.replace('''        a = h.analyser(phrase[\"texte\"], \"fr\")''','''        a = h.analyser(phrase[\"texte\"])''')\np.write_text(s,encoding='utf-8')\nprint('ok')\nPY\npython3  … [104 caractères tronqués]`

  ```
ok
[stderr]
----------------------------------------------------------------------
Ran 16 tests in 0.867s

OK
  ```

- **bash** `{"command": "python3 tools/mesurer_restitution_v2.py >/tmp/v2.out && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-restitution-v2.json'))\nprint(d['synthese']['roles']['precision'], d['synthese']['roles']['rappel'], d['synthese']['roles']['f1'])\nprint(d['synthese']['or'])\nprint(l … [98 caractères tronqués]`

  ```
0.5616 0.5325 0.5467
{'textes': 46, 'variantes': 65, 'roles_attendus': 77}
8 limites
restitution du rendu     : 46/46 (1.0000)
contrôle négatif rendu   : 39/39 éligibles détectés

contrôle externe (gold S) : 139/144 (0.9653) · baseline 104/144 (0.7222)

écrit : reports/pensee-restitution-v2.json
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/drave.py')\ns=p.read_text(encoding='utf-8')\ns=s.replace('''**restitution v0** (annotation → surface, avec la fidélité du miroir). La restitution est un\n**codec de surface** : elle reconstruit depuis le niveau `graphème`, pas un d … [807 caractères tronqués]`

  ```
ok
OK
  ```

- **job_output** `{"job_id": "bash-111", "wait": true, "timeout_ms": 600000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ps -o pid,etime,pcpu,pmem,cmd -C bash -C python3 -C python | grep -v grep | head -30", "description": "Inspect running gate processes"}`

  ```
PID     ELAPSED %CPU %MEM CMD
   3002 11-09:55:33  0.1  0.0 /usr/bin/python3 /home/stephane/.local/share/pipewire-eq/eqdaemon.py
  64459 10-22:05:43  0.0  0.0 bash /home/stephane/.local/bin/monitor-hotplug.sh
  64700 10-22:05:43  0.0  0.0 /bin/bash
  64814 10-22:05:43  0.0  0.0 /bin/bash
 264795 10-19:50:29  0.0  0.0 /bin/bash
 264836 10-19:50:26  0.0  0.0 /bin/bash
 735575 10-12:31:47  0.0  0.0 /bin/bash
2035895  9-19:00:30  0.0  0.0 /bin/bash
2725526    13:16:04  0.0  0.0 bash -c sleep 2; cd /home/stephane/Data13TB/stephane/GitHub/financemeteo && python3 src/app.py --no-browser
2725542    13:16:01  0.0  0.0 python3 src/app.py --no-browser
2997720       53:46  0.1  0.0 python3 tools/chantier/superviseur.py boucle --budget 14400 --timeout 3600
3013484       20:58  0.0  0.0 bash -c bash tools/toutes-les-portes.sh 2>&1 | tail -120
3013491       20:58  0.0  0.0 bash tools/toutes-les-portes.sh
3104196       05:56  0.0  0.0 bash -c cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sleep 1500; date; tail -2 work/chantier/journal.log; git rev-list --count origin/master..s/v7
3140014       00:41  0.0  0.0 bash tools/porte-gain.sh
3146578       00:00  0.0  0.0 bash tools/porte-gain.sh
  ```

- **bash** `{"command": "echo \"JOURNAUX=${JOURNAUX:-}\"; ls -l \"${JOURNAUX:-/tmp}/registre.txt\" 2>/dev/null || true; find . -maxdepth 3 -name 'registre.txt' -printf '%p\\n' 2>/dev/null | head", "description": "Locate gate registry"}`

  ```
JOURNAUX=
./work/portes-n3-cloture/registre.txt
./work/portes-1106-01h03/registre.txt
./work/portes-1106-01h28/registre.txt
./work/portes-1107-01h43/registre.txt
./work/portes-1107-02h09/registre.txt
./work/portes-j12-1107-12h58/registre.txt
./work/portes-1107-15h11/registre.txt
./work/portes-1107-16h48/registre.txt
./work/portes-1107-18h17/registre.txt
./work/portes-1107-18h22/registre.txt
  ```

- **bash** `{"command": "ls -lt work/*/registre.txt 2>/dev/null | head -5; echo ===; ls -lt work/portes-* 2>/dev/null | head -5", "description": "Find current gate registry"}`

  ```
-rw-r--r--. 1 stephane stephane  544 15 nov 05:28 work/portes-1115-05h08/registre.txt
-rw-r--r--. 1 stephane stephane   42 15 nov 04:03 work/portes-1115-04h03/registre.txt
-rw-r--r--. 1 stephane stephane  561 14 nov 06:16 work/portes-1114-05h52/registre.txt
-rw-r--r--. 1 stephane stephane   47 14 nov 05:42 work/portes-1114-05h40/registre.txt
-rw-r--r--. 1 stephane stephane  161 14 nov 05:37 work/portes-1114-05h36/registre.txt
===
work/portes-1115-05h08:
total 116
-rw-r--r--. 1 stephane stephane  369 15 nov 05:29 porte-gain.log
-rw-r--r--. 1 stephane stephane  544 15 nov 05:28 registre.txt
-rw-r--r--. 1 stephane stephane 1844 15 nov 05:28 porte-fusion.log
  ```

- **bash** `{"command": "cat work/portes-1115-05h08/registre.txt; echo ===; tail -20 work/portes-1115-05h08/porte-gain.log", "description": "Read current gate registry and gain log"}`

  ```
porte-adaptateur-sortie 0 80
porte-audit-drapeaux 0 185
porte-b1110-hybride 0 0
porte-balayage 0 0
porte-bloc-code 0 14
porte-bloc-linguistique 0 13
porte-bloc-maths 0 1
porte-bloc-tableaux 0 2
porte-budget 0 44
porte-bus 0 78
porte-bus-socket 0 94
porte-c4-retard 0 31
porte-cerveau 0 9
porte-cic 0 11
porte-consolidation 0 99
porte-coupe 0 132
porte-cycle-c2 0 124
porte-deepseek 0 0
porte-delais 0 21
porte-diff-couche 0 18
porte-document 0 6
porte-echange-experts 0 52
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
===
=== 1. invariant : --ffn-gain L:1.0 EST l'absence de réglage ===
  sans réglage : 14.6496
  ✅ PPL référence épinglée : 14.6496
  couche 0   gain 1.0 : 14.6496
  couche 6   gain 1.0 : 14.6496
  couche 18  gain 1.0 : 14.6496
  ✅ l'identité est exacte sur trois couches
=== 2. inhibition MONOTONE (couche 12) ===
  gain 0.0    : 15.6908
  gain -0.25  : 16.3034
  gain -0.5   : 17.1200
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-restitution-v2.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('''**46 cadres**, **65 variantes**, un cadre principal par texte, écrit depuis le texte et non\ndepuis les sorties.''','''**46 cadres**, **65 variantes**,  … [1748 caractères tronqués]`

  ```
ok
reports/rapport-restitution-v2.md:106:texte — mais **après avoir vu les sorties** : c'est un biais nommé, pas un or aveugle.
reports/rapport-restitution-v2.md:283:- **L'or** : 46 cadres écrits à la main, de la même main que la fiche, **après avoir vu les
tools/mesurer_restitution_v2.py:36:    "L'or est écrit à la main en lisant le texte, mais **après avoir vu les sorties** : c'est "
  ```

- **bash** `{"command": "python3 tools/mesurer_restitution_v2.py >/dev/null && python3 -c \"import json; d=json.load(open('reports/pensee-restitution-v2.json')); print(d['limites'][1][:120]); print(d['synthese']['roles']['f1'])\"", "description": "Regenerate JSON with bias note"}`

  ```
L'or est écrit à la main en lisant le texte, mais **après avoir vu les sorties** : c'est un biais nommé, pas un or aveug
0.5467
  ```

- **bash** `{"command": "cat work/portes-1115-05h08/registre.txt | tail -10; echo ===; ps -o pid,etime,cmd -p 3013491,3140014,3146578 2>/dev/null", "description": "Check gate progress"}`

  ```
porte-cycle-c2 0 124
porte-deepseek 0 0
porte-delais 0 21
porte-diff-couche 0 18
porte-document 0 6
porte-echange-experts 0 52
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
===
    PID     ELAPSED CMD
3013491       21:19 bash tools/toutes-les-portes.sh
3140014       01:01 bash tools/porte-gain.sh
  ```

- **bash** `{"command": "sed -n '1,120p' tools/porte-gain.sh", "description": "Inspect gain gate runtime"}`

  ```
#!/bin/bash
# porte-gain.sh — E4 : le GAIN de la FFN par couche, et l'équilibre excitation/inhibition.
#
# L'HYPOTHÈSE BIOLOGIQUE (docs/biologie-pour-drave.md, E4) : un réseau cortical équilibré
# vit près d'un point où excitation et inhibition se compensent, et un déséquilibre dans un
# sens ou dans l'autre coûte. Transposée au moteur, la question mesurable est : **existe-t-il
# un gain de la FFN, par couche, qui AMÉLIORE la perplexité — et est-il intérieur** (ni 0,
# ni 1, ni l'infini) ?
#
# CE QUE LA MESURE A DONNÉ, et les deux moitiés ne disent pas la même chose :
#   · du côté INHIBITION (gain < 1), la courbe est MONOTONE : toute inhibition dégrade, et
#     l'hypothèse d'un optimum intérieur y est RÉFUTÉE ;
#   · du côté AMPLIFICATION, l'optimum est INTÉRIEUR et net sur les premières couches :
#     couche 0 à 0,75 → **12,9635** contre **14,6496** sans réglage (**−11,5 %**), et couche
#     1 à 0,5 → 13,7907 (−5,9 %) ; la couche 2 n'a plus d'optimum utile.
#   · en dessous de l'optimum, une FALAISE : couche 0 à 0,25 → **996,04** (le gain trop
#     faible à la première couche casse le modèle, il ne le dégrade pas un peu).
#
# Ce que la porte verrouille :
#   1. `--ffn-gain L:
… [4564 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'restitution-v2\\|restitution v2' reports/INDEX.md reports/README.md 2>/dev/null | head -20", "description": "Check report index for new fiche"}`

  ```
(no output)
  ```

- **bash** `{"command": "grep -n 'restitution' reports/INDEX.md reports/README.md 2>/dev/null | head -20; ls reports/INDEX.md reports/README.md 2>/dev/null", "description": "Check report index contents"}`

  ```
reports/INDEX.md:263:| [rapport-modules-famille.md](rapport-modules-famille.md) | C3.2b — un module de restitution par famille : l'indo-européen recopie à 100 % |
reports/INDEX.md:529:| [rapport-pensee-miroir-espaces.md](rapport-pensee-miroir-espaces.md) | B13 — la restitution avec les intervalles : 1,0, la perte était le rendu |
reports/INDEX.md:530:| [rapport-pensee-miroir-pos.md](rapport-pensee-miroir-pos.md) | B13 — la sortie POS : 0,201, la restitution sémantique ne restitue pas |
reports/INDEX.md:532:| [rapport-pensee-miroir-resume.md](rapport-pensee-miroir-resume.md) | B13 — la restitution sémantique : le résumé rappelle 78 % |
reports/INDEX.md:688:| [rapport-restitution-v0.md](rapport-restitution-v0.md) | B13 — la restitution v0 : 46/46 surfaces exactes, le miroir strict à 0,1087 |
reports/INDEX.md:689:| [rapport-restitution-v1.md](rapport-restitution-v1.md) | B13 — la restitution v1 : la forme canonique à 46/46, le miroir strict reste à 0,1087 |
reports/INDEX.md:690:| [rapport-restitution.md](rapport-restitution.md) | B18 — restitution canonique : 528/528, mais pas un décodeur |
reports/README.md:58:| [`rapport-restitution-v0.md`](rapport-restitution-v0.md) | **B13** — res
… [344 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln 'reports/INDEX.md' tools/*.py tools/**/*.py 2>/dev/null | head -20; grep -rn 'INDEX.md' tools/*.py | head -20", "description": "Find report index generator"}`

  ```
tools/index_reports.py
tools/surveille_sessions.py
tools/index_reports.py:2:"""index_reports.py — génère reports/INDEX.md à partir des en-têtes de fiches.
tools/index_reports.py:5:avec son titre (premier `# `). Les fichiers d'infrastructure (`README.md`, `INDEX.md`
tools/index_reports.py:10:    python3 tools/index_reports.py              # réécrit reports/INDEX.md
tools/index_reports.py:32:        if p.name not in ("README.md", "INDEX.md") and not p.name.startswith("historique-")
tools/index_reports.py:42:        "> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;",
tools/index_reports.py:53:    ap = argparse.ArgumentParser(description="Génère reports/INDEX.md (déterministe).")
tools/index_reports.py:61:    sortie = RACINE / "reports/INDEX.md"
tools/index_reports.py:67:    print(f"  {len(fiches())} fiches → reports/INDEX.md")
tools/surveille_sessions.py:33:            "docs/pilotage/README.md", "AGENTS.md", "reports/INDEX.md",
tools/taille_documents.py:128:        if p.name in ("README.md", "INDEX.md") or p.name.startswith("historique-"):
  ```

- **bash** `{"command": "grep -n 'gold-reel-50\\|s-paragraphes\\|gold_reel_50' reports/INDEX.md reports/README.md 2>/dev/null | head; python3 tools/index_reports.py --dry-run 2>/dev/null | head -20 || true", "description": "Check index for untracked reports"}`

  ```
reports/INDEX.md:198:| [rapport-gold-reel-50.md](rapport-gold-reel-50.md) | R0.7 / B13 — le gold réel étendu : 50 phrases que l'heuristique rate, et ce qu'elles disent |
reports/INDEX.md:706:| [rapport-s-paragraphes.md](rapport-s-paragraphes.md) | S — La banque de paragraphes passe à neuf : six paires d'Alice, sources anglaises et référents |
reports/README.md:19:| [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md) | **R0.7** — le gold réel : 452 phrases, 50 ratées, le « 200+ » obsolète |
  ```

- **bash** `{"command": "python3 tools/index_reports.py 2>&1 | tail -5; grep -n 'restitution-v2' reports/INDEX.md | head", "description": "Regenerate reports index"}`

  ```
741 fiches → reports/INDEX.md
690:| [rapport-restitution-v2.md](rapport-restitution-v2.md) | B13 — la restitution v2 : les rôles se lisent, leur fidélité ne suit pas |
  ```

- **bash** `{"command": "git status --short reports/INDEX.md reports/README.md; git diff --stat reports/INDEX.md", "description": "Check index modifications"}`

  ```
M reports/INDEX.md
 reports/INDEX.md | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
  ```

- **bash** `{"command": "git diff -- reports/INDEX.md", "description": "Inspect INDEX diff"}`

  ```
diff --git a/reports/INDEX.md b/reports/INDEX.md
index 666d75bb..64253d6d 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **740 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **741 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -687,6 +687,7 @@
 | [rapport-replis-cible.md](rapport-replis-cible.md) | B13 — les trois retouches A3 sur le live : +1, +2, +1, et 145/145 exact/top1 |
 | [rapport-restitution-v0.md](rapport-restitution-v0.md) | B13 — la restitution v0 : 46/46 surfaces exactes, le miroir strict à 0,1087 |
 | [rapport-restitution-v1.md](rapport-restitution-v1.md) | B13 — la restitution v1 : la forme canonique à 46/46, le miroir strict reste à 0,1087 |
+| [rapport-restitution-v2.md](rapport-restitution-v2.md) | B13 — la restitution v2 : les rôles se lisent, leur fidélité ne suit pas |
 | [rapport-restitution.md](rapport-restitution.md) | B18 — restitution canonique : 528/528, mais pas un décodeur |
 | [rapport-retrieval-epoque.md]
… [209 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '50,65p' reports/README.md", "description": "Inspect reports README restitution rows"}`

  ```
| [`rapport-gn-pronom-sujet.md`](rapport-gn-pronom-sujet.md) | **B13** — pronom sujet = GN : **0,7013** |
| [`rapport-r264-elision.md`](rapport-r264-elision.md) | **B13** — `r264` : 236/237, couverture **0,9916** |
| [`rapport-pos-ponctuation.md`](rapport-pos-ponctuation.md) | **B13** — PONCT : POS **85,75 %**, miroir |
| [`rapport-etat-s.md`](rapport-etat-s.md) | **B13** — l'état de S : /paragraphes 19/19 |
| [`rapport-etat-r.md`](rapport-etat-r.md) | **B13** — l'état de R : tagger 0,8483/0,9440 |
| [`rapport-etat-n2.md`](rapport-etat-n2.md) | **B13** — l'état de N2 (porte propre, `porte-n2.sh`) |
| [`rapport-etat-a.md`](rapport-etat-a.md) | **B13** — l'état de A (frontière) |
| [`rapport-re-test-produit.md`](rapport-re-test-produit.md) | **B13** — re-test des 50 textes |
| [`rapport-restitution-v0.md`](rapport-restitution-v0.md) | **B13** — restitution v0 : **46/46** surfaces, miroir |
| [`rapport-restitution-v1.md`](rapport-restitution-v1.md) | **B13** — restitution v1 : forme canonique **46/46** |
| [`rapport-pos-nombres.md`](rapport-pos-nombres.md) | **B13** — les nombres ont une POS (NUM) |
| [`rapport-partition-integree.md`](rapport-partition-integree.md) | **B13** — partiti
… [444 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/README.md')\ns=p.read_text(encoding='utf-8')\nold='| [`rapport-restitution-v1.md`](rapport-restitution-v1.md) | **B13** — restitution v1 : forme canonique **46/46** |\\n'\nnew=old+'| [`rapport-restitution-v2.md`](rapport-restitut … [279 caractères tronqués]`

  ```
ok
  ✅ 1816 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4412 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "tail -5 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; tail -3 work/portes-1115-05h08/porte-gain.log", "description": "Check gate progress"}`

  ```
porte-echange-experts 0 52
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
    PID     ELAPSED CMD
3013491       21:52 bash tools/toutes-les-portes.sh
  ✅ PPL falaise 0.25 épinglée : 996.039
  ✅ la falaise est réelle : 996.039 contre 14.6496 (68× pire)
=== 5. le bénéfice est LOCALISÉ aux deux premières couches ===
  ```

- **bash** `{"command": "sed -n '1,160p' docs/pilotage/references-non-regression.md", "description": "Read tolerated red gates"}`

  ```
# Références de non-régression

> **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
> `porte-melange` (structurelles) et `porte-sessions` (mandats périmés du hub `1e7ef596` et de
> `e181ce02`). `porte-produit` et `porte-bloc` **vertes**. Journal :
> `work/portes/passe-1311-23h15.log`.
>
> **Vérification ciblée — 2026-11-14 06 h 55 (J14.1) :** `porte-sessions` **verte** (hub en pause,
> heartbeat `e181ce02` rafraîchi) ; `porte-indice` et `porte-melange` restent **rouges
> structurelles** (indice 482 contre témoin 459 ; état de A sans son code). Journaux
> `work/portes/verif-cloture/`.
> **Passe — 2026-11-06 :** 83 portes, **79 vertes, 4 rouges** (voir la ligne `bloc-linguistique`).

> **Passe précédente — 2026-11-04 23 h 43 → 2026-11-05 02 h 12 :** **83 portes, 79 vertes,
> 4 rouges**, **2 h 29** (journaux durables `work/portes/passe-2404-23h45`), **machine au repos**
> (GPU libres, aucune réservation). Les **2 rouges structurelles connues** restent : `porte-indice`
> (1 207 s), `porte-melange` (148 s). Deux rouges nouvelles, **hors dépôt** : `porte-lecteur` (0 s)
> échouait sur une ancre du banc pilote (« < 2,5 ») que la réécriture de la roadma
… [12333 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/tests/test_restitution_v2.py')\ns=p.read_text(encoding='utf-8')\nold='''        ids = {t[\"id\"] for t in textes}\n        refus = {\"f14\", \"f15\", \"f16\", \"f17\"}\n        self.assertEqual(ids | refus, {it[\"id\"] for it in se … [926 caractères tronqués]`

  ```
ok
[stderr]
----------------------------------------------------------------------
Ran 16 tests in 0.897s

OK
  ```

- **bash** `{"command": "tail -5 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; tail -2 work/portes-1115-05h08/porte-gain.log", "description": "Check gate progress again"}`

  ```
porte-echange-experts 0 52
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
    PID     ELAPSED CMD
3013491       22:03 bash tools/toutes-les-portes.sh
  ✅ le bénéfice est à l'ENTRÉE : couches 0 et 1 à 12.9635 et 13.9844 (mieux que 14.6496), couche 5 à 14.7526 (pas mieux)
=== 6. un PROFIL ne compose PAS : il défait le meilleur réglage seul ===
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/tests/test_restitution_v2.py')\ns=p.read_text(encoding='utf-8')\nold='''    def test_gold_sans_banc_refuse(self):\n        sortie = drave(\"restituer\", \"Le chat dort.\", \"--roles\",\n                       \"--gold\", str(GOLD)) … [1300 caractères tronqués]`

  ```
ok
[stderr]
----------------------------------------------------------------------
Ran 17 tests in 1.221s

OK
  ```

- **bash** `{"command": "grep -rn '16 tests\\|16 test' reports/rapport-restitution-v2.md tools/tests/test_restitution_v2.py docs/pilotage/roadmap.md docs/pilotage/en-cours.md | head -20", "description": "Find 16-test references"}`

  ```
reports/rapport-restitution-v2.md:320:- [`test_restitution_v2.py`](../tools/tests/test_restitution_v2.py) — 16 tests.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-restitution-v2.md')\ns=p.read_text(encoding='utf-8').replace('— 16 tests.','— 17 tests.')\np.write_text(s,encoding='utf-8')\nprint('ok')\nPY", "description": "Update test count in report"}`

  ```
ok
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/roadmap.md')\ns=p.read_text(encoding='utf-8').replace('dont 16 tests v2','dont 17 tests v2')\np.write_text(s,encoding='utf-8')\nprint('ok')\nPY", "description": "Update roadmap test count"}`

  ```
ok
  ```

- **bash** `{"command": "tail -5 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; tail -2 work/portes-1115-05h08/porte-gain.log", "description": "Check gate progress"}`

  ```
porte-echange-experts 0 52
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
    PID     ELAPSED CMD
3013491       22:19 bash tools/toutes-les-portes.sh
  ✅ la composition DÉGRADE (12.9635 → 13.7679), et un gain 1,0 y est exactement neutre (13.7679 = 13.7679)
=== 7. l'effet DIMINUE avec la fenêtre d'évaluation (et il tient) ===
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -8; echo ===; python3 tools/taille_documents.py 2>&1 | tail -3; echo ===; python3 tools/verifie_en_cours.py 2>&1 | tail -3", "description": "Re-run doc review and budget after edits", "timeoutMs": 180000}`

  ```
revue de documentation · 744 fiche(s) · 838 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
===
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
===
  en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -6; echo ===; python3 tools/verifie_journal.py 2>&1 | tail -3", "description": "Re-run tables and journal checks", "timeoutMs": 120000}`

  ```
✅ 1816 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4412 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
===
  journal · 47 jour(s) · 202 session(s) · 2577 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "ls -la .git/hooks | head -30; cat .git/hooks/pre-commit 2>/dev/null | head -80", "description": "Inspect git hooks"}`

  ```
total 68
drwxr-xr-x. 1 stephane stephane  576 31 oct 12:55 .
drwxr-xr-x. 1 stephane stephane  198 15 nov 05:30 ..
-rw-r--r--. 1 stephane stephane  478 25 sep 13:48 applypatch-msg.sample
-rw-r--r--. 1 stephane stephane 1972 25 sep 13:48 commit-msg.sample
-rw-r--r--. 1 stephane stephane 4611 25 sep 13:48 fsmonitor-watchman.sample
-rw-r--r--. 1 stephane stephane  189 25 sep 13:48 post-update.sample
-rw-r--r--. 1 stephane stephane  424 25 sep 13:48 pre-applypatch.sample
-rwxr-xr-x. 1 stephane stephane 1470 31 oct 12:55 pre-commit
-rw-r--r--. 1 stephane stephane 1649 25 sep 13:48 pre-commit.sample
-rw-r--r--. 1 stephane stephane  416 25 sep 13:48 pre-merge-commit.sample
-rw-r--r--. 1 stephane stephane 1492 25 sep 13:48 prepare-commit-msg.sample
-rw-r--r--. 1 stephane stephane 1374 25 sep 13:48 pre-push.sample
-rw-r--r--. 1 stephane stephane 4898 25 sep 13:48 pre-rebase.sample
-rw-r--r--. 1 stephane stephane  544 25 sep 13:48 pre-receive.sample
-rw-r--r--. 1 stephane stephane 2783 25 sep 13:48 push-to-checkout.sample
-rw-r--r--. 1 stephane stephane 2308 25 sep 13:48 sendemail-validate.sample
-rw-r--r--. 1 stephane stephane 3650 25 sep 13:48 update.sample
#!/bin/sh
# pre-commit — l'état a
… [1401 caractères tronqués]
  ```

- **bash** `{"command": "tail -8 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; tail -2 work/portes-1115-05h08/porte-gain.log", "description": "Check gate progress"}`

  ```
porte-delais 0 21
porte-diff-couche 0 18
porte-document 0 6
porte-echange-experts 0 52
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
    PID     ELAPSED CMD
3013491       22:32 bash tools/toutes-les-portes.sh
  ✅ la composition DÉGRADE (12.9635 → 13.7679), et un gain 1,0 y est exactement neutre (13.7679 = 13.7679)
=== 7. l'effet DIMINUE avec la fenêtre d'évaluation (et il tient) ===
  ```

- **bash** `{"command": "sed -n '1,200p' tools/toutes-les-portes.sh", "description": "Inspect all-gates runner"}`

  ```
#!/bin/bash
# toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait.
#
# POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS
# (`--attn-window` en réparti) que le v7 avait **délibérément retiré** en faisant voyager les
# trois réglages dans la trame (`main.rs:4432`). La porte ne pouvait donc plus passer — et
# personne ne l'a vu, parce que les portes étaient lancées **une par une**, à la main, quand
# on touchait la fonctionnalité du jour. Une porte qu'on croit verte et qui n'a pas tourné est
# exactement le défaut que ce dépôt traque (un drapeau inerte, une mesure qui ne mesure rien) :
# ici, appliqué aux instruments eux-mêmes.
#
# Ce que fait ce script, et ce qu'aucun autre ne faisait :
#   1. il lance **TOUTES** les `tools/porte-*.sh`, séquentiellement ;
#   2. il ne s'arrête PAS à la première rouge — il veut le tableau, pas la première tuile ;
#   3. il borne chaque porte dans le temps (`DELAI`, 1800 s par défaut) : une porte qui pend
#      est une porte ROUGE, pas une porte qu'on attend ;
#   4. il garde le journal de chacune (`JOURNAUX`) et n'affiche qu'une ligne par porte ;
#   5. il sort en 1 s'il y a la moindre rouge, en
… [3112 caractères tronqués]
  ```

- **bash** `{"command": "tail -3 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; tail -2 work/portes-1115-05h08/porte-gain.log", "description": "Check gate progress"}`

  ```
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
    PID     ELAPSED CMD
3013491       22:40 bash tools/toutes-les-portes.sh
  ✅ la composition DÉGRADE (12.9635 → 13.7679), et un gain 1,0 y est exactement neutre (13.7679 = 13.7679)
=== 7. l'effet DIMINUE avec la fenêtre d'évaluation (et il tient) ===
  ```

- **bash** `{"command": "tail -20 work/portes-1115-05h08/porte-gain.log; ps -eo pid,etime,pcpu,cmd | grep -E 'drave|porte-gain' | grep -v grep | head", "description": "Inspect gain gate subprocess"}`

  ```
gain -0.5   : 17.1200
  gain -1.0   : 19.4791
  ✅ toute inhibition dégrade, et de plus en plus : l'optimum intérieur est réfuté de ce côté
=== 3. optimum INTÉRIEUR (couche 0) : 0,75 doit battre 0,5 ET 1,5 ===
  gain 0,5 : 14.1057 · 0,75 : 12.9635 · 1,5 : 15.4298
  ✅ PPL gain 0.5 épinglée : 14.1057
  ✅ PPL gain 0.75 épinglée : 12.9635
  ✅ PPL gain 1.5 épinglée : 15.4298
  ✅ optimum intérieur : 12.9635 contre 14.1057, 15.4298 et 14.6496 sans réglage (11.5 % de mieux)
=== 4. la FALAISE : 0,25 à la couche 0 casse le modèle ===
  gain 0,25 : 996.0390
  ✅ PPL falaise 0.25 épinglée : 996.039
  ✅ la falaise est réelle : 996.039 contre 14.6496 (68× pire)
=== 5. le bénéfice est LOCALISÉ aux deux premières couches ===
  couche 0 : 12.9635 · couche 1 : 13.9844 · couche 5 : 14.7526 (référence 14.6496)
  ✅ le bénéfice est à l'ENTRÉE : couches 0 et 1 à 12.9635 et 13.9844 (mieux que 14.6496), couche 5 à 14.7526 (pas mieux)
=== 6. un PROFIL ne compose PAS : il défait le meilleur réglage seul ===
  0:0.75 seul : 12.9635 · +1:0.5 : 13.7679 · +1:0.5+2:1.0 : 13.7679
  ✅ la composition DÉGRADE (12.9635 → 13.7679), et un gain 1,0 y est exactement neutre (13.7679 = 13.7679)
=== 7. l'effet DIMINUE avec la 
… [362 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' tools/restitution_v2.py", "description": "Review restitution_v2 code part 1"}`

  ```
"""restitution_v2.py — la restitution v2 : les rôles (agent, prédicat, lieu).

La v0 restitue la **surface** (graphème → texte) ; la v1 restitue la **forme canonique**
(segments + rôles + cibles). La v2 ajoute une lecture **lisible des rôles** : un cadre
principal `agent / prédicat / lieu`, les cadres de chaque prédicat, et les segments de rôle.

La fidélité des rôles ne se mesure pas contre l'annotation qui les produit (ce serait une
tautologie) : elle se mesure contre un **or de rôles écrit à la main** sur les 46 textes
annotables du banc v0 (`tools/tests/linguistique/gold_restitution_v2.json`). L'or ne porte
que le **cadre principal** et quelques variantes d'ambiguïté ; il ne prétend pas annoter
toutes les propositions.

Deux mesures sont séparées :

- la **restitution** du rôle (le rôle est-il lisible et relu à l'identique ?) — un codec ;
- la **fidélité** du rôle (le rôle est-il celui de l'or ?) — une exactitude sémantique.

Le contrôle négatif retire ou permute les rôles du rendu : le lecteur doit le voir. Le
contrôle « cadre vide » et le contrôle « rôle constant par type » donnent les planchers.

    python3 tools/mesurer_restitution_v2.py
    python3 tools/drave.py restitue
… [7613 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/restitution_v2.py')\ns=p.read_text(encoding='utf-8')\nold='''    groupes = [e for e in segments if e[\"type\"] == \"GN\" and e[\"role_normalise\"] not in ROLES]'''\nnew='''    groupes = [e for e in segments if e[\"type\"] == \"GN\" … [698 caractères tronqués]`

  ```
ok
{'exacts': 19, 'taux': 0.413, 'exacts_non_vides': 16, 'exacts_vides': 3, 'partiels': 42, 'partiels_taux': 0.913, 'exacts_stricts': 16, 'taux_strict': 0.3478, 'roles_exacts_moyens': 1.9783}
91 39 71
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,sys,pathlib\nsys.path.insert(0,'.')\nimport tools.restitution_v2 as v2\nbank=json.loads(pathlib.Path('reports/pensee-fiabilite-produit.json').read_text(encoding='utf-8'))\ngold=json.loads(pathlib.Path('tools/tests/linguistique/gold_restitution_v2.json').rea … [1239 caractères tronqués]`

  ```
restitution v2 — les rôles — banc x
textes 50 · annotés 46 · refus 4 (f14, f15, f16, f17)

cadre principal (agent, prédicat, lieu)
  cadres exacts                19/46       0.4130
  dont non vides               16/46     (0.3478) · vides 3
  cadres partiels              42/46       0.9130
  exacts stricts (1re var.)    16/46       0.3478
  rôles exacts                91/138      0.6594
  justes / attendus           39/77    
  précision / rappel / F1 0.5493 / 0.5065 / 0.5270
  faux positifs / négatifs 32 / 38

par rôle                  exacts    attendus   prédits   justes   préc.   rappel
  agent                     29/46         32        28       18  0.6429   0.5625
  prédicat                  22/46         39        39       19  0.4872   0.4872
  lieu                      40/46          6         4        2  0.5000   0.3333

segments de rôle 198 · agents 43 · prédicats 143 · lieux 12 · cadres 139
textes avec au moins un rôle : 40/46 (0.8696)
spans de rôle dans la source : 198/198 (1.0000)

contrôle vide            : 61/138 rôles exacts · cadres exacts 7/46
contrôle constant (type) : 68/138 rôles exacts · cadres exacts 6/46
contrôle rôles mélangés  : 29/138 rôles exacts · cadre
… [1473 caractères tronqués]
  ```

- **bash** `{"command": "grep -nE '20/46|17/46|93/138|41|73|0,5616|0,5325|0,5467|32 faux|36 faux|0,6129|0,5128|30/46|23/46|0,6333|0,5938|0,5625|0,4872|27/138|16/46|19/46|91/138|39/77|0,5493|0,5065|0,5270|0,4130|0,3478' reports/rapport-restitution-v2.md | head -100", "description": "Locate stale metrics in repor … [3 caractères tronqués]`

  ```
5:> ne l'est pas : **20/46 cadres exacts** (dont **17 non vides**), **F1 0,5467**, **32 faux
6:> positifs** et **36 faux négatifs**.
15:> **20/46 cadres exacts** (0,4348), **17/46 non vides** (0,3696), **93/138 cellules de rôle
16:> exactes** (0,6739) — mais seulement **41 justes sur 77 attendus** et **73 prédits**, soit
17:> **précision 0,5616 · rappel 0,5325 · F1 0,5467**. Le contrôle « rôle constant par type »
23:> **Le chiffre.** **17/46 cadres principaux non vides exacts** (0,3696) ; **F1 0,5467** ;
24:> **agent 0,6129**, **prédicat 0,5128**, **lieu 0,4000** ; **32 faux positifs / 36 faux
96:- **fidélité** : `principal == or` — une exactitude sémantique, **17/46** cadres non vides.
124:la variante stricte (la première) est publiée à part (`exacts_stricts = 17/46`).
133:| cadres exacts (toutes variantes) | **20/46 = 0,4348** |
134:| dont **non vides** | **17/46 = 0,3696** |
137:| cadres exacts stricts (1re variante) | **17/46 = 0,3696** |
138:| rôles exacts (cellules) | **93/138 = 0,6739** |
140:Le **0,6739** est trompeur si on le lit seul : une cellule vide correctement vide compte
145:| rôles justes (les deux non vides et égaux) | **41** |
147:| rôles prédits (sortie non vide
… [704 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-restitution-v2.md')\ns=p.read_text(encoding='utf-8')\nrepl={\n'**20/46 cadres exacts** (dont **17 non vides**)':'**19/46 cadres exacts** (dont **16 non vides**)',\n'**F1 0,5467**':'**F1 0,5270**',\n'**32 faux\\n> positifs … [3278 caractères tronqués]`

  ```
MISSING: **Le chiffre.** **17/46 cadres principaux non vides exacts** (0,3696) ; **F1 0,5
done
23:> **Le chiffre.** **17/46 cadres principaux non vides exacts** (0,3696) ; **F1 0,5270** ;
24:> **agent 0,6129**, **prédicat 0,5128**, **lieu 0,4000** ; **32 faux positifs / 36 faux
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-restitution-v2.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('''> **Le chiffre.** **17/46 cadres principaux non vides exacts** (0,3696) ; **F1 0,5270** ;\n> **agent 0,6129**, **prédicat 0,5128**, **lieu 0,4000** ; ** … [492 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "grep -nE '19/46|16/46|91/138|0,4130|0,3478|0,6594|0,5493|0,5065|0,5270|0,6000|0,4872|29/138|38 faux|71 prédits|39 justes' reports/rapport-restitution-v2.md | head -50", "description": "Verify updated report metrics"}`

  ```
5:> ne l'est pas : **19/46 cadres exacts** (dont **16 non vides**), **F1 0,5270**, **32 faux
6:> positifs** et **38 faux négatifs**.
15:> **19/46 cadres exacts** (0,4130), **16/46 non vides** (0,3478), **91/138 cellules de rôle
16:> exactes** (0,6594) — mais seulement **39 justes sur 77 attendus** et **71 prédits**, soit
17:> **précision 0,5493 · rappel 0,5065 · F1 0,5270**. Le contrôle « rôle constant par type »
23:> **Le chiffre.** **16/46 cadres principaux non vides exacts** (0,3478) ; **F1 0,5270** ;
24:> **agent 0,6000**, **prédicat 0,4872**, **lieu 0,4000** ; **32 faux positifs / 38 faux
96:- **fidélité** : `principal == or` — une exactitude sémantique, **16/46** cadres non vides.
124:la variante stricte (la première) est publiée à part (`exacts_stricts = 16/46`).
133:| cadres exacts (toutes variantes) | **19/46 = 0,4130** |
134:| dont **non vides** | **16/46 = 0,3478** |
137:| cadres exacts stricts (1re variante) | **16/46 = 0,3478** |
138:| rôles exacts (cellules) | **91/138 = 0,6594** |
140:Le **0,6594** est trompeur si on le lit seul : une cellule vide correctement vide compte
148:| précision | **0,5493** |
149:| rappel | **0,5065** |
150:| **F1** | **0,5270** |
157:| **a
… [471 caractères tronqués]
  ```

- **bash** `{"command": "grep -n '17/46\\|0,5467\\|0,5616\\|0,5325\\|0,6129\\|0,5128\\|36 faux\\|41 justes\\|73 prédits\\|93/138\\|20/46' reports/rapport-restitution-v2.md || echo 'aucune'", "description": "Check for remaining stale values"}`

  ```
aucune
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/tests/test_restitution_v2.py')\ns=p.read_text(encoding='utf-8')\nrepl={\n'self.assertEqual(donnees[\"synthese\"][\"cadre\"][\"exacts_non_vides\"], 17)':'self.assertEqual(donnees[\"synthese\"][\"cadre\"][\"exacts_non_vides\"], 16)', … [1796 caractères tronqués]`

  ```
ok
[stderr]
----------------------------------------------------------------------
Ran 17 tests in 1.303s

OK
  ```

- **bash** `{"command": "grep -rn '0,5467\\|0.5467\\|17/46 cadres\\|20/46 cadres\\|93/138\\|0,5616\\|0,5325\\|0,4348\\|0,3696\\|0,6739\\|0,6129\\|0,5128' reports/rapport-restitution-v2.md tools/mesurer_restitution_v2.py docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-15/mesures.md tools/tests … [97 caractères tronqués]`

  ```
docs/pilotage/roadmap.md:38:**État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **attachement exact 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (REL suivie d'un GV → le sujet du GV : 238/238, 0 span, 0 POS ; [fiche](../../reports/rapport-s065.md)) ; **183/183** ; **`r035`** (relative zéro) réglé ; **convention des GV** réglée (sujet hors du GV + adverbe final : GV F1 0,7549 → 0,7902, 0 perte d'attachement) ; **contrat v2 publié et validé** (`meta.partition`/`meta.alternative`, version 2, **v1 lue** : 26 cas, 0 échec) ; **restitution v1** (`restituer --canonique` : **46/46 formes canoniques exactes** contre la source canonisée, **miroir strict 0,1087 inchangé**, **395 segments / 395 rôles / 315 cibles dont 315 résolues**, stabilité **18/46** ; le strict ne monte pas, la v1 n'est pas la surface ; [fiche](../../reports/rapport-restitution-v1.md)) ; **restitution v2** : **17/46** cadres non vides exacts, F1 **0,5467** ; [fiche](../../reports/rapport-restitution-v2.md). **J9.1 passe d'honnêteté** (**19** fiches « instantané historique » : 10 encarts réécrits, 9 ajoutés ; **0 fiche de résultats** ne publie les quatre marqueurs sans menti
… [961 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\n# roadmap\np=pathlib.Path('docs/pilotage/roadmap.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('**restitution v2** : **17/46** cadres non vides exacts, F1 **0,5467** ;','**restitution v2** : **16/46** cadres non vides exacts, F1 **0,5270** ;')\np.w … [1507 caractères tronqués]`

  ```
ok
aucune
  ```

- **bash** `{"command": "python3 tools/mesurer_restitution_v2.py >/tmp/v2.out && tail -8 /tmp/v2.out && python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-restitution-v2.json'))\ns=d['synthese']\nprint(s['cadre'])\nprint(s['roles']['exacts'], s['roles']['justes'], s['roles']['f1'])\nprint(s['contro … [100 caractères tronqués]`

  ```
contrôle constant (type) : 68/138 rôles exacts · cadres exacts 6/46
contrôle rôles mélangés  : 29/138 rôles exacts · cadres exacts 3/46
restitution du rendu     : 46/46 (1.0000)
contrôle négatif rendu   : 39/39 éligibles détectés

contrôle externe (gold S) : 139/144 (0.9653) · baseline 104/144 (0.7222)

écrit : reports/pensee-restitution-v2.json
{'exacts': 19, 'taux': 0.413, 'exacts_non_vides': 16, 'exacts_vides': 3, 'partiels': 42, 'partiels_taux': 0.913, 'exacts_stricts': 16, 'taux_strict': 0.3478, 'roles_exacts_moyens': 1.9783}
91 39 0.527
3
  ```

- **bash** `{"command": "grep -rn '0,5467\\|0.5467\\|17/46\\|0,5616\\|0,5325\\|93/138\\|0,4348\\|0,6129\\|0,5128' reports/README.md reports/INDEX.md docs/ journal/2026-11-15/ tools/ tests/ 2>/dev/null | head -40", "description": "Search all stale v2 metrics"}`

  ```
reports/README.md:60:| [`rapport-restitution-v2.md`](rapport-restitution-v2.md) | **B13** — restitution v2 : rôles **17/46**, F1 **0,5467** |
tools/docwatch/.venv/lib/python3.13/site-packages/ruff-0.17.3.dist-info/sboms/ruff.cyclonedx.json:1217:          "content": "52ce7f38b242319f7cabaa6813055467063ecdc9d355bbb4ce0c68908cd8130e"
tools/tests/test_restitution_v2.py:8:- sur les **46 textes** de la v0, le cadre principal est exact **20/46** et **17/46**
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/README.md')\ns=p.read_text(encoding='utf-8').replace('rôles **17/46**, F1 **0,5467**','rôles **16/46**, F1 **0,5270**')\np.write_text(s,encoding='utf-8')\np=pathlib.Path('tools/tests/test_restitution_v2.py')\ns=p.read_text(encodi … [527 caractères tronqués]`

  ```
ok
journal/2026-11-15/mesures.md:47:Mais la **fidélité** ne suit pas. Sur un or écrit à la main (46 cadres, 65 variantes), **20/46**
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('journal/2026-11-15/mesures.md')\ns=p.read_text(encoding='utf-8').replace('(46 cadres, 65 variantes), **20/46**','(46 cadres, 65 variantes), **19/46**')\np.write_text(s,encoding='utf-8')\nprint('ok')\nPY\ngrep -rn '20/46\\|17/46\\|0,5467\ … [318 caractères tronqués]`

  ```
ok
aucune
  ```

- **bash** `{"command": "python3 -m unittest tools.tests.test_restitution_v2 -q && python3 tools/mesurer_restitution_v2.py >/dev/null && echo 'json ok'", "description": "Run v2 tests and regenerate JSON"}`

  ```
json ok
[stderr]
----------------------------------------------------------------------
Ran 17 tests in 1.153s

OK
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -5; echo ===; python3 tools/taille_documents.py 2>&1 | tail -3", "description": "Re-run doc review and budget", "timeoutMs": 180000}`

  ```
revue de documentation · 744 fiche(s) · 838 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
===
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "tail -5 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; tail -2 work/portes-1115-05h08/porte-gain.log", "description": "Check gate progress"}`

  ```
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
porte-gain 0 214
    PID     ELAPSED CMD
3013491       23:56 bash tools/toutes-les-portes.sh
  tableau de bord : puits d'attention 4 (défaut) · puits d'attention 0 (imposé)
  ✅ drapeau VIVANT mais conditionnel : 0 casse (29.0206 → 1297.5437), 24 améliore (27.4439), sans fenêtre il se tait
  ```

- **bash** `{"command": "git diff -- tools/drave.py | sed -n '1,220p'", "description": "Review CLI diff"}`

  ```
diff --git a/tools/drave.py b/tools/drave.py
index 8e037dc4..f07b2901 100644
--- a/tools/drave.py
+++ b/tools/drave.py
@@ -11,13 +11,15 @@ Une seule commande, quatre gestes, hors ligne et déterministe :
     python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
     python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
     python3 tools/drave.py restituer "Le chat dort."
+    python3 tools/drave.py restituer "Le chat dort." --roles
     python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
     python3 tools/drave.py --version
 
 Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
 avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et la
-**restitution v0** (annotation → surface, avec la fidélité du miroir). La restitution est un
-**codec de surface** : elle reconstruit depuis le niveau `graphème`, pas un décodeur neuronal.
+**restitution v0** (annotation → surface, avec la fidélité du miroir) et la **v2** (rôles
+agent/prédicat/lieu lisibles). La restitution est un **codec de surface** : elle 
… [6810 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/drave.py')\ns=p.read_text(encoding='utf-8')\ns=s.replace('''    (`--banc`, le format de `reports/pensee-fiabilite-produit.json`). Le mode banc\n    laisse le bloc détecter la langue, comme le CLI sans `--langue`. `--canonique`\n    … [685 caractères tronqués]`

  ```
ok
OK
  ```

- **bash** `{"command": "tail -5 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; ls -lt work/portes-1115-05h08 | head -5", "description": "Check gate progress"}`

  ```
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
porte-gain 0 214
    PID     ELAPSED CMD
3013491       24:05 bash tools/toutes-les-portes.sh
total 124
-rw-r--r--. 1 stephane stephane   86 15 nov 05:32 porte-greffe.log
-rw-r--r--. 1 stephane stephane  561 15 nov 05:32 registre.txt
-rw-r--r--. 1 stephane stephane 4655 15 nov 05:32 porte-gain.log
-rw-r--r--. 1 stephane stephane 1844 15 nov 05:28 porte-fusion.log
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nfor p in ['reports/rapport-restitution-v2.md','docs/pilotage/roadmap.md','journal/2026-11-15/mesures.md']:\n f=pathlib.Path(p); s=f.read_text(encoding='utf-8')\n s=s.replace('vue fidèle de rôles faux ou absents','vue fidèle de rôles **souvent** faux ou  … [323 caractères tronqués]`

  ```
ok
journal/2026-11-15/mesures.md:54:aucun syntagme. La v2 est une **vue fidèle de rôles **souvent** faux ou absents**, pas un analyseur.
  ```

- **bash** `{"command": "grep -rn 'souvent faux' reports/rapport-restitution-v2.md docs/pilotage/roadmap.md journal/2026-11-15/mesures.md", "description": "Check bold nesting"}`

  ```
(no output)
[exit code: 1]
  ```

- **bash** `{"command": "grep -rn 'faux ou absents' reports/rapport-restitution-v2.md docs/pilotage/roadmap.md journal/2026-11-15/mesures.md", "description": "Find phrase"}`

  ```
journal/2026-11-15/mesures.md:54:aucun syntagme. La v2 est une **vue fidèle de rôles **souvent** faux ou absents**, pas un analyseur.
  ```

- **bash** `{"command": "grep -rn 'fidèle de rôles' reports/rapport-restitution-v2.md docs/pilotage/roadmap.md", "description": "Find report phrase"}`

  ```
(no output)
[exit code: 1]
  ```

- **bash** `{"command": "grep -rn 'faux ou' reports/rapport-restitution-v2.md docs/pilotage/roadmap.md | head", "description": "Search phrase variant"}`

  ```
(no output)
  ```

- **bash** `{"command": "grep -n 'vue' reports/rapport-restitution-v2.md docs/pilotage/roadmap.md | tail -10", "description": "Find vue phrase"}`

  ```
reports/rapport-restitution-v2.md:78:La v2 est une **vue** sur l'annotation, pas un second analyseur. Elle lit les syntagmes et
reports/rapport-restitution-v2.md:174:Les 198 spans sont des sous-chaînes exactes de la source : la vue ne fabrique pas de texte.
reports/rapport-restitution-v2.md:302:1. **Ne pas maquiller la v2 en analyseur** : elle restera une vue tant que les rôles de
docs/pilotage/roadmap.md:81:schéma v2 et passent la validation ; les **4 refus** sont des réponses JSON (code 3). En vue
docs/pilotage/roadmap.md:82:**`alternative`**, **395 segments** et **115 chevauchements** dans **21/46** textes ; en vue
docs/pilotage/roadmap.md:162:**La vue d'ensemble des chantiers** — huit chantiers (A, B, N, R, **S**, **L**, **D**, B13), leurs relations, leurs chemins critiques et les tensions à trancher — est dans [`chantiers.md`](chantiers.md) ; la carte est [`chantiers-vision.svg`](../schemas/chantiers-vision.svg) ; le **plan de travail multi-sessions** (qui fait quoi, où, à quelle cadence) est dans [`plan-travail.md`](plan-travail.md). Les demandes des 48 h y sont reliées à ce qu'elles ont déplacé.
docs/pilotage/roadmap.md:428:- **Ce n'est pas « lire à 1 000 mots/minute »** : l
… [225 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn 'absents' reports/rapport-restitution-v2.md docs/pilotage/roadmap.md journal/2026-11-15/mesures.md", "description": "Search absents phrase"}`

  ```
reports/rapport-restitution-v2.md:163:lieu sont souvent absents ou étiquetés `complément` / `destinataire` / `possession`.
journal/2026-11-15/mesures.md:54:aucun syntagme. La v2 est une **vue fidèle de rôles **souvent** faux ou absents**, pas un analyseur.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('journal/2026-11-15/mesures.md')\ns=p.read_text(encoding='utf-8').replace('**vue fidèle de rôles **souvent** faux ou absents**','**vue fidèle de rôles souvent faux ou absents**')\np.write_text(s,encoding='utf-8')\nprint('ok')\nPY\ngrep -n … [90 caractères tronqués]`

  ```
ok
54:aucun syntagme. La v2 est une **vue fidèle de rôles souvent faux ou absents**, pas un analyseur.
  ```

- **bash** `{"command": "grep -rn '0,5270\\|0.5270\\|0,4130\\|0.4130\\|0,5493\\|0.5493\\|0,5065\\|0.5065\\|19/46\\|16/46' reports/rapport-restitution-v2.md reports/README.md docs/pilotage/roadmap.md journal/2026-11-15/mesures.md tools/tests/test_restitution_v2.py | head -30", "description": "Verify final metric … [15 caractères tronqués]`

  ```
reports/rapport-restitution-v2.md:5:> ne l'est pas : **19/46 cadres exacts** (dont **16 non vides**), **F1 0,5270**, **32 faux
reports/rapport-restitution-v2.md:15:> **19/46 cadres exacts** (0,4130), **16/46 non vides** (0,3478), **91/138 cellules de rôle
reports/rapport-restitution-v2.md:17:> **précision 0,5493 · rappel 0,5065 · F1 0,5270**. Le contrôle « rôle constant par type »
reports/rapport-restitution-v2.md:23:> **Le chiffre.** **16/46 cadres principaux non vides exacts** (0,3478) ; **F1 0,5270** ;
reports/rapport-restitution-v2.md:96:- **fidélité** : `principal == or` — une exactitude sémantique, **16/46** cadres non vides.
reports/rapport-restitution-v2.md:124:la variante stricte (la première) est publiée à part (`exacts_stricts = 16/46`).
reports/rapport-restitution-v2.md:133:| cadres exacts (toutes variantes) | **19/46 = 0,4130** |
reports/rapport-restitution-v2.md:134:| dont **non vides** | **16/46 = 0,3478** |
reports/rapport-restitution-v2.md:137:| cadres exacts stricts (1re variante) | **16/46 = 0,3478** |
reports/rapport-restitution-v2.md:148:| précision | **0,5493** |
reports/rapport-restitution-v2.md:149:| rappel | **0,5065** |
reports/rapport-restitution-v2.md:15
… [2865 caractères tronqués]
  ```

- **bash** `{"command": "tail -6 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; tail -2 work/portes-1115-05h08/porte-greffe.log", "description": "Check gate progress"}`

  ```
porte-echange-experts 0 52
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
porte-gain 0 214
    PID     ELAPSED CMD
3013491       24:34 bash tools/toutes-les-portes.sh
=== 0. construire A (avec aiguille) et B (sans), et vérifier qu'elles diffèrent ===
  ```

- **bash** `{"command": "sed -n '88,94p' docs/pilotage/en-cours.md; echo ===; grep -n 'restitution v2' docs/pilotage/en-cours.md", "description": "Check state v2 line"}`

  ```
- **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67 ; **19/19 verdicts `389b99f`** ; `/paragraphes` v7, `/` ancien arbre ; [v2](../../reports/rapport-coordination-s-v2.md).
- **N2 — en pause** : **commande validée** `eval_longueurs.py --rope --val <dir>` (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejeté** (g017 à trancher), schéma v2, **restitution v2** ([fiche](../../reports/rapport-restitution-v2.md)), **J9.1** (19 fiches), **D1** ; [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).
- **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.
- **Panini J2.1–J3.2 + B2** : **14 atomes** ; UDHR **418/438** ; J3.2 : **5/21** langues (Glottolog **21/21**), **154/154** paires hors script au hasard, **V14 3/21** ; **B2 : atomes → niveaux négatif** (POS −0,092, syntagmes −0,160, attachement −0,092 ; style absorbé par la date) ; [atom
… [944 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text(encoding='utf-8')\ns=s.replace('**restitution v2** ([fiche](../../reports/rapport-restitution-v2.md)), **J9.1** (19 fiches)', '**restitution v2** **16/46** ([fiche](../../reports/rapport-restitu … [232 caractères tronqués]`

  ```
ok
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  en-cours · 1629 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | grep -E 'T0 max|violation|budget' | tail -5", "description": "Check T0 budget"}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
  T0 max : 3999 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "tail -6 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; tail -2 work/portes-1115-05h08/porte-greffe.log", "description": "Check gate progress"}`

  ```
porte-echange-experts 0 52
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
porte-gain 0 214
    PID     ELAPSED CMD
3013491       24:46 bash tools/toutes-les-portes.sh
=== 0. construire A (avec aiguille) et B (sans), et vérifier qu'elles diffèrent ===
  ```

- **bash** `{"command": "tail -20 work/portes-1115-05h08/porte-greffe.log", "description": "Inspect greffe gate log"}`

  ```
=== 0. construire A (avec aiguille) et B (sans), et vérifier qu'elles diffèrent ===
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | grep 'docs/pilotage/roadmap.md'", "description": "Check roadmap word count"}`

  ```
9000    493   T1   9000  docs/pilotage/roadmap.md
  ```

- **bash** `{"command": "sleep 60; tail -6 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; tail -3 work/portes-1115-05h08/porte-greffe.log", "description": "Wait and check gate progress", "timeoutMs": 90000}`

  ```
porte-echange-experts 0 52
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
porte-gain 0 214
    PID     ELAPSED CMD
3013491       25:56 bash tools/toutes-les-portes.sh
  A (avec aiguille) : [1863, 48, 12, 19, 19, 22, 16, 15843]
  B (sans aiguille) : [220, 16, 17, 18, 19, 20, 21, 22]
=== 1. prélever l'état de la dernière position DE L'INFÉRENCE (--etat-fin) ===
  ```

- **bash** `{"command": "bash tools/porte-document.sh 2>&1 | tail -5; echo ===; bash tools/porte-etat.sh 2>&1 | tail -5", "description": "Run quick doc and state gates", "timeoutMs": 120000}`

  ```
… et 24 autres

✅ les 50 pages sont découpées, les partitions exactes, le rejeu identique,
   la fidélité ≥ 0,99 et les trois contrôles négatifs se comportent comme prévu.
✅ porte document verte
===
  ✅ état court, structuré, multi-session et reprenable
  état · dernier fait d23780d7 · dernier état d23780d7
  ✅ aucun fait commité après le dernier état
  ✅ autotest : 6 cas, dont 3 refus attendus et 3 passes
✅ porte état verte : aucun fait commité après le dernier état
  ```

- **bash** `{"command": "bash tools/porte-produit.sh 2>&1 | tail -6", "description": "Re-run product gate after metric changes", "timeoutMs": 180000}`

  ```
✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
  ```

- **bash** `{"command": "git diff --check -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-15/mesures.md tools/drave.py tools/porte-produit.sh reports/INDEX.md reports/README.md; echo \"exit=$?\"", "description": "Check whitespace in modified files"}`

  ```
exit=0
  ```

- **bash** `{"command": "python3 -m json.tool tools/tests/linguistique/gold_restitution_v2.json >/dev/null && echo gold-ok; python3 -m json.tool reports/pensee-restitution-v2.json >/dev/null && echo json-ok; wc -l reports/rapport-restitution-v2.md tools/restitution_v2.py tools/tests/test_restitution_v2.py", "de … [43 caractères tronqués]`

  ```
gold-ok
json-ok
  329 reports/rapport-restitution-v2.md
  806 tools/restitution_v2.py
  238 tools/tests/test_restitution_v2.py
 1373 total
  ```

- **bash** `{"command": "tail -8 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; tail -2 work/portes-1115-05h08/porte-greffe.log", "description": "Check gate progress"}`

  ```
porte-diff-couche 0 18
porte-document 0 6
porte-echange-experts 0 52
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
porte-gain 0 214
    PID     ELAPSED CMD
3013491       28:45 bash tools/toutes-les-portes.sh
  ✅ l'état injecté porte bien la direction du contenu de A
=== 4. CORRIGÉ : l'état de A dans C (sans aucun code) DONNE le code ===
  ```

- **bash** `{"command": "grep -n '^echo \"===' tools/porte-greffe.sh | tail -10", "description": "List greffe steps"}`

  ```
70:echo "=== 0. construire A (avec aiguille) et B (sans), et vérifier qu'elles diffèrent ==="
91:echo "=== 1. prélever l'état de la dernière position DE L'INFÉRENCE (--etat-fin) ==="
97:echo "=== 2. témoin de non-effet : poids 0 ⇒ aucune différence ==="
102:echo "=== 3. le mécanisme fonctionne : A + son propre état reste sur le code ==="
110:echo "=== 4. CORRIGÉ : l'état de A dans C (sans aucun code) DONNE le code ==="
126:echo "=== 5. la greffe porte TOUT le contenu, pas seulement le premier jeton ==="
  ```

- **bash** `{"command": "sleep 90; tail -8 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; tail -2 work/portes-1115-05h08/porte-greffe.log", "description": "Wait and check gate progress", "timeoutMs": 120000}`

  ```
porte-diff-couche 0 18
porte-document 0 6
porte-echange-experts 0 52
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
porte-gain 0 214
    PID     ELAPSED CMD
3013491       30:19 bash tools/toutes-les-portes.sh
=== 4. CORRIGÉ : l'état de A dans C (sans aucun code) DONNE le code ===
  poids 1    : [220, 16, 17, 18, 19, 20, 21, 22]
  ```

- **bash** `{"command": "ps -eo pid,etime,pcpu,cmd | grep -E 'drave|porte-greffe' | grep -v grep | head", "description": "Check greffe subprocess"}`

  ```
3172990       06:31  0.0 timeout 1800 bash tools/porte-greffe.sh
3172991       06:31  0.0 bash tools/porte-greffe.sh
3175863       00:39  0.0 bash tools/porte-greffe.sh
3175864       00:39  877 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --infer --prompt  Division . On August 1 , the 23rd Regiment was in a new sector of which it had only a limited knowledge . It took over a 16 @,@ 000 yards ( 15 @,@ 000 m ) Naktong River front without its 3rd Battalion which had been attached to the US 1st Cavalry Division to the north . Colonel Paul L. Freeman , the regimental commander , deployed the 1st Battalion on the high ground along the river with the three companies abreast . The 1st Battalion , under US Lieutenant Colonel Claire E. Hutchin , Jr . , outposted the hills with platoons and squads . He placed the 2nd Battalion in a reserve position 8 miles ( 13 km ) behind the 1st Battalion and in a position where it commanded the road net in the regimental sector . On August 31h the 2nd Division moved E Company south to a reserve position in the 9th Infantry sector .    Two roads ran through the regimental sector from the Naktong River to Changnyong . The main road bent so
… [5272 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-111", "timeout_ms": 300000, "wait": true}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "tail -8 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; tail -2 work/portes-1115-05h08/porte-greffe.log", "description": "Check gate progress after wait"}`

  ```
porte-document 0 6
porte-echange-experts 0 52
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
porte-gain 0 214
porte-greffe 0 647
    PID     ELAPSED CMD
3013491       35:30 bash tools/toutes-les-portes.sh
     sur laquelle le moteur n'a aujourd'hui aucune prise — un manque, écrit.
  Fichiers conservés dans /tmp/tmp.JdekoJ4ki3
  ```

- **bash** `{"command": "ps -eo pid,etime,pcpu,cmd | grep -E 'porte-|drave' | grep -v grep | head -10; ls -lt work/portes-1115-05h08 | head -5", "description": "Identify current gate"}`

  ```
3177833       00:54  0.0 timeout 1800 bash tools/porte-harnais-invariants.sh
3177834       00:54  0.0 bash tools/porte-harnais-invariants.sh
3178335       00:19  0.0 timeout 1200 /home/stephane/gpu-env/bin/python -u tools/entrainer_moteur.py --famille route --dim 192 --couches 4 --tetes 4 --cache 768 --experts 8 --k 2 --seq 128 --lot 32 --lr 3e-4 --graine 1 --signes-figes --pas 200 --eval-tous 200 --elagage-tous 100 --elagage 0.25 --sortie /tmp/porte-harnais-invariants/sigfiges
3178336       00:19  128 /home/stephane/gpu-env/bin/python -u tools/entrainer_moteur.py --famille route --dim 192 --couches 4 --tetes 4 --cache 768 --experts 8 --k 2 --seq 128 --lot 32 --lr 3e-4 --graine 1 --signes-figes --pas 200 --eval-tous 200 --elagage-tous 100 --elagage 0.25 --sortie /tmp/porte-harnais-invariants/sigfiges
total 128
-rw-r--r--. 1 stephane stephane  825 15 nov 05:43 porte-harnais-invariants.log
-rw-r--r--. 1 stephane stephane  580 15 nov 05:43 registre.txt
-rw-r--r--. 1 stephane stephane 2073 15 nov 05:43 porte-greffe.log
-rw-r--r--. 1 stephane stephane 4655 15 nov 05:32 porte-gain.log
  ```

- **bash** `{"command": "grep -n '[[:blank:]]$' tools/restitution_v2.py tools/mesurer_restitution_v2.py tools/tests/test_restitution_v2.py reports/rapport-restitution-v2.md | head -20 || echo 'pas de fin de ligne blanche'", "description": "Check trailing whitespace in new files"}`

  ```
(no output)
  ```

- **bash** `{"command": "grep -rn 'restituer' docs/produit docs/README.md README.md | head -30", "description": "Find product docs for CLI restituter"}`

  ```
docs/produit/README.md:9:> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
docs/produit/README.md:330:python3 tools/drave.py restituer "Le chat dort."
docs/produit/README.md:440:**1. Il ne génère pas de texte.** `restituer` reconstruit la **surface** depuis l'annotation
docs/produit/README.md:442:paraphrase. Le produit rend des **étiquettes** et, avec `restituer`, la surface qu'elles
docs/produit/README.md:550:| **0** | succès : annotation rendue, évaluation rendue, rejeu identique, restitution rendue | `analyser`, `evaluer`, `rejouer`, `restituer` |
docs/produit/README.md:553:| **3** | refus **distinct** de l'erreur, avec l'annotation de refus sur `stdout` | `analyser ""`, `restituer "..."` |
docs/produit/README.md:574:python3 tools/drave.py restituer "TEXTE" [--langue fr|en] [--json] [--fichier CHEMIN]
docs/produit/README.md:575:python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json [--json]
docs/produit/README.md:609:| `--langue fr\|en` | `analyser`, `rejouer`, `restituer` | **indice** de langue, pas une contrainte ; hors `fr`/`en` → code 2 |
docs/produit/README.md:610:| `--json` | `analyser`, `evaluer`, `restit
… [688 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '560,625p' docs/produit/README.md; echo ===; sed -n '430,450p' docs/produit/README.md", "description": "Read product CLI docs section"}`

  ```
une ancienne réponse.

## 7. Le CLI livré — contrat et manques

Le point d'entrée existe : `tools/drave.py`, version **0.1.0**, sans dépendance externe.

```bash
python3 tools/drave.py --version
python3 tools/drave.py --aide
python3 tools/drave.py analyser "Le chat dort." [--langue fr|en] [--json] [--tagger] \
    [--partition brut|alternative|filtrer_union|filtrer] [--contexte TEXTE]
python3 tools/drave.py analyser --fichier corpus.txt [--jsonl|--json] [--tagger]
python3 tools/drave.py evaluer [--gold] [--json] [--par-langue] [--tagger]
python3 tools/drave.py rejouer "TEXTE" [--langue fr|en]
python3 tools/drave.py restituer "TEXTE" [--langue fr|en] [--json] [--fichier CHEMIN]
python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json [--json]
```

`--tagger` est la **seule** option qui sort du hors ligne : elle appelle l'API DeepSeek (clé et
réseau, § 3.7). Toutes les autres lignes ci-dessus restent CPU, déterministes et sans socket.

**Sorties réelles des commandes** (07/11 pour le format ; les valeurs d'`evaluer` sont celles
mesurées le 14/11) :

```
$ python3 tools/drave.py --version
drave 0.1.0

$ python3 tools/drave.py evaluer --gold
drave 0.1.0 — évaluatio
… [3120 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | grep 'docs/produit/README.md' || true", "description": "Check product doc budget"}`

  ```
(no output)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/produit/README.md')\ns=p.read_text(encoding='utf-8')\nold='''python3 tools/drave.py restituer \"TEXTE\" [--langue fr|en] [--json] [--fichier CHEMIN]\npython3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json [--j … [2381 caractères tronqués]`

  ```
ok
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ✅ 1816 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4412 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "tail -8 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; ls -lt work/portes-1115-05h08 | head -4", "description": "Check gate progress"}`

  ```
porte-document 0 6
porte-echange-experts 0 52
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
porte-gain 0 214
porte-greffe 0 647
    PID     ELAPSED CMD
3013491       35:56 bash tools/toutes-les-portes.sh
total 128
-rw-r--r--. 1 stephane stephane  948 15 nov 05:44 porte-harnais-invariants.log
-rw-r--r--. 1 stephane stephane  580 15 nov 05:43 registre.txt
-rw-r--r--. 1 stephane stephane 2073 15 nov 05:43 porte-greffe.log
  ```

- **bash** `{"command": "sleep 120; tail -10 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null", "description": "Wait and check gate progress", "timeoutMs": 150000}`

  ```
porte-diff-couche 0 18
porte-document 0 6
porte-echange-experts 0 52
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
porte-gain 0 214
porte-greffe 0 647
porte-harnais-invariants 0 115
    PID     ELAPSED CMD
3013491       38:01 bash tools/toutes-les-portes.sh
  ```

- **bash** `{"command": "grep -n 'tests' reports/rapport-restitution-v2.md | tail -5; grep -n 'tests v2' docs/pilotage/roadmap.md", "description": "Check test count references"}`

  ```
32:> [`gold_restitution_v2.json`](../tools/tests/linguistique/gold_restitution_v2.json) ;
33:> tests [`test_restitution_v2.py`](../tools/tests/test_restitution_v2.py) ;
104:[`gold_restitution_v2.json`](../tools/tests/linguistique/gold_restitution_v2.json) :
320:- [`test_restitution_v2.py`](../tools/tests/test_restitution_v2.py) — 17 tests.
321:- [`gold_restitution_v2.json`](../tools/tests/linguistique/gold_restitution_v2.json) — 46
[exit code: 1]
  ```

- **bash** `{"command": "sleep 300; tail -12 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; ls -lt work/portes-1115-05h08 | head -3", "description": "Wait 5 minutes and check gate progress", "timeoutMs": 330000}`

  ```
porte-deepseek 0 0
porte-delais 0 21
porte-diff-couche 0 18
porte-document 0 6
porte-echange-experts 0 52
porte-episodique 0 171
porte-etat 0 0
porte-flux 0 25
porte-fusion 0 7
porte-gain 0 214
porte-greffe 0 647
porte-harnais-invariants 0 115
    PID     ELAPSED CMD
3013491       43:09 bash tools/toutes-les-portes.sh
total 132
-rw-r--r--. 1 stephane stephane  437 15 nov 05:49 porte-homeostasie.log
-rw-r--r--. 1 stephane stephane  611 15 nov 05:45 registre.txt
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-restitution-v2.md')\ns=p.read_text(encoding='utf-8')\nold='''Le lecteur bat les planchers, mais **19/46** reste loin de 1. Le mélange tombe à **3/46** :\nles rôles comptent, la mesure ne lit pas un rôle constant déguisé.\ … [503 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "sleep 300; tail -12 work/portes-1115-05h08/registre.txt; ps -o pid,etime,cmd -p 3013491 2>/dev/null; ls -lt work/portes-1115-05h08 | head -4", "description": "Wait 5 minutes and check gate progress", "timeoutMs": 330000}`
