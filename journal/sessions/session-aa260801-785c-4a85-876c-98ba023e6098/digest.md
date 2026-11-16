# Session DSH — relecture

- identifiant : `session-aa260801-785c-4a85-876c-98ba023e6098`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-16 00:31:32
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche U2 (suite de T1) : **la roue** — `python3 -m build` (ou `pip wheel .`) produit `drave-0.1.0-py3-none-any.whl`, installée dans un venv **propre** depuis la roue (pas le dépôt) : `drave --version` et `drave analyser` depuis `/tmp` ; le **contrôle négatif** : la roue sans les gold doit-elle échouer (le CLI lit `tools/tests/linguistique/gold_*.json` — si les gold ne sont pas dans la roue, `evaluer` échoue : décide et documente, avec un `--gold` qui dit quoi faire) ; la doc § 8.10 mise à jour. Fiche `reports/rapport-roue.md` + JSON.

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

- **bash** `{"command": "pwd && ls -la && git log --oneline -15 && git status --short | head -50", "description": "Inspect repo root and git state"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
total 212
drwxr-xr-x. 1 stephane stephane   714 15 nov 22:25 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138 15 nov 22:25 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   220 16 nov 00:31 .git
-rw-r--r--. 1 stephane stephane   653 15 nov 22:25 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane  1012 16 nov 00:22 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-------. 1 stephane stephane   334 15 nov 21:38 pyproject.toml
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 79462 16 nov 00:27 reports
-r
… [3345 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' docs/pilotage/en-cours.md", "description": "Read current state doc"}`

  ```
# En ce moment

**Mis à jour : 2026-11-16, 00 h 30 HNE (U1 : les deux O(k²) bornés, α 1,08)**

> **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs.
- **Prochaine action** : **suivi docs**, puis la **passe**.
- **État** : **en pause** depuis le 05/11 ; la clôture J14.1 est portée par `e181ce02`.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `É
… [10949 caractères tronqués]
  ```

- **bash** `{"command": "cat pyproject.toml; echo '---'; ls src; echo '---'; find src -maxdepth 3 -type f | head -50", "description": "Read pyproject and src layout"}`

  ```
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "drave"
version = "0.1.0"
description = "Le point d'entrée produit du bloc linguistique de Drave."
requires-python = ">=3.10"
dependencies = []

[project.scripts]
drave = "tools.drave:main"

[tool.setuptools]
packages = ["tools"]
---
bpe_np.py
encoding.py
gguf_min.py
__pycache__
roofline.py
sparsity.py
ternary.py
tiny_model.py
transformer_np.py
---
src/roofline.py
src/__pycache__/roofline.cpython-313.pyc
src/__pycache__/ternary.cpython-313.pyc
src/__pycache__/sparsity.cpython-313.pyc
src/__pycache__/tiny_model.cpython-313.pyc
src/__pycache__/encoding.cpython-313.pyc
src/__pycache__/gguf_min.cpython-313.pyc
src/__pycache__/bpe_np.cpython-313.pyc
src/__pycache__/transformer_np.cpython-313.pyc
src/ternary.py
src/sparsity.py
src/tiny_model.py
src/encoding.py
src/gguf_min.py
src/bpe_np.py
src/transformer_np.py
  ```

- **bash** `{"command": "grep -rn \"8\\.10\\|la roue\\|T1\\|U2\" docs/pilotage docs/methode reports/*.md 2>/dev/null | head -80", "description": "Find task references"}`

  ```
docs/pilotage/chantiers.md:90:| **B13 — le moteur de pensée** | penser est-il une recherche tracée sur des états pluriels ? | ✅ state store v0 + AC-3/alpha-bêta + **DRVF `thought`** + **banc anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **porte** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **professeur** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + **votante** + **trois looks** + **bayésien** + **bayésien 2** + **vraisemblance** + **dérive** + **adaptative** + **glisse** + **rupture** + **alternance** + **chaotique** + **fréquent** + **rapide** + **limite** + **hasard 2** + **intra** + **asym** + **rare** + **très rare** + **ultra-rare** + **un look** + **look tardif** + **oubli** + **oubli fort** + **oubli total** + **seuil** + **seuil fin*
… [20393 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"8\\.10\" --include='*.md' . | head -40; echo '---'; ls docs/*; printf '\\n--- reports empaquetage ---\\n'; sed -n '1,220p' reports/rapport-empaquetage.md", "description": "Find section 8.10 and T1 report"}`

  ```
./reports/rapport-coordination-n2.md:377:(`"129": 8.1024`, `"192": 8.4072`, `"256": 8.9710`, `"384": 10.0906`, `"512": 11.3357`) — le
./reports/rapport-empaquetage.md:17:> [`docs/produit/README.md`](../docs/produit/README.md) § 8.10.
./reports/rapport-empaquetage.md:54:- **La doc** [`docs/produit/README.md`](../docs/produit/README.md) § 8.10 porte désormais les
./reports/rapport-empaquetage.md:181:- [`docs/produit/README.md`](../docs/produit/README.md) § 8.10 — l'install utilisateur.
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:9153:    postes (ms/token) : projets-attn 295.23 | rope 1.73 | attention 2.83 | proj+mlp 448.10 | somme 747.89 | reste (tête + échantillonnage) 15.62
./journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/digest.md:40030:bruit50    991828.1040
./journal/sessions/d58fb6be-cedc-4236-a298-aa953dfb21b7/digest.md:518:tokenspeed-triton                        3.8.10.post20260721
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:66183:| **3. Le démarrage** | pas de **quickstart** (le § 8.10 existe mais c'est une note, pas un parcours) | 30 min de lecture au lieu de 5 |
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapp
… [20349 caractères tronqués]
  ```

- **bash** `{"command": "find tools -maxdepth 2 -name 'drave.py' -o -maxdepth 2 -name '*.sh' | head; echo '---'; sed -n '1,160p' tools/drave.py", "description": "Read CLI entrypoint start"}`

  ```
tools/preparer_colab.sh
tools/colab_cote_local.sh
tools/sprint.sh
tools/verifier_table_types.sh
tools/inventaire_modeles_lourds.sh
tools/portes_formats.sh
tools/extraire_tables_ggml.sh
tools/portes.sh
tools/porte-tokenizer-kimi.sh
tools/apres-telechargement-k3.sh
---
#!/usr/bin/env python3
"""drave.py — le point d'entrée produit du bloc linguistique.

Une seule commande, quatre gestes, hors ligne et déterministe :

    python3 tools/drave.py analyser "Le chat dort."
    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
    python3 tools/drave.py analyser "Le chat dort." --tagger auto     # API si clé, sinon heuristique
    python3 tools/drave.py evaluer
    python3 tools/drave.py evaluer --gold --json
    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
    python3 tools/drave.py restituer "Le chat dort."
    python3 tools/drave.py restituer "Le chat dort." --roles
    python3 tools/drave.py restituer --banc reports/pe
… [6090 caractères tronqués]
  ```

- **bash** `{"command": "find tools -maxdepth 2 -type d | sort; echo '---files root tools---'; ls tools | head -80; echo '---tests linguistique---'; ls -la tools/tests/linguistique | head -40; echo '---gold json---'; find tools -name 'gold*.json' | head -40", "description": "Inspect tools tree and gold files"}`

  ```
tools
tools/cerveau
tools/cerveau/__pycache__
tools/cerveau/tests
tools/chantier
tools/docwatch
tools/docwatch/.github
tools/docwatch/.pytest_cache
tools/docwatch/.ruff_cache
tools/docwatch/src
tools/docwatch/tests
tools/docwatch/.venv
tools/hooks
tools/jeux
tools/jeux/codecs
tools/jeux/__pycache__
tools/jeux/regles
tools/jeux/tests
tools/llm
tools/llm/__pycache__
tools/llm/tests
tools/pensee
tools/pensee/__pycache__
tools/__pycache__
tools/schemas
tools/semantique
tools/semantique/__pycache__
tools/semantique/tests
tools/structures
tools/structures/donnees
tools/structures/__pycache__
tools/structures/static
tools/structures/tests
tools/tests
tools/tests/cic
tools/tests/code
tools/tests/documents
tools/tests/linguistique
tools/tests/maths
tools/tests/__pycache__
tools/tests/tableaux
tools/tokenizer_kimi
---files root tools---
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

… [3719 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"evaluer\\|--gold\\|GOLD\\|gold\\|RACINE\" tools/drave.py | head -100; echo '---'; sed -n '880,980p' docs/produit/README.md", "description": "Find evaluer and gold option handling"}`

  ```
10:    python3 tools/drave.py evaluer
11:    python3 tools/drave.py evaluer --gold --json
12:    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
20:avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et la
24:En **option** (`--tagger`, `analyser` et `evaluer`), le POS (et lui seul) vient du tagger de
54:RACINE = pathlib.Path(__file__).resolve().parent.parent
55:sys.path.insert(0, str(RACINE / "tools"))
56:sys.path.insert(0, str(RACINE))
369:    """Le coût d'une exécution, tel qu'il va dans un rapport (`evaluer --json`)."""
664:    """Charge `evaluer_gold.py` (le gold et sa mesure) sans dépendre du répertoire courant."""
665:    chemin = RACINE / "tools" / "tests" / "linguistique" / "evaluer_gold.py"
667:        raise FileNotFoundError(f"mesure du gold introuvable : {chemin}")
668:    spec = importlib.util.spec_from_file_location("_drave_evaluer_gold", chemin)
677:def _cibles_gold(phrases: list[dict]) -> list[str]:
682:    """Contrôle négatif : une cible **exacte** tirée au hasard parmi les cibles du gold.
686:    cibles = _cibles_gold(phrases)
705:    gold = rapport["gold"]
715:        f"{NOM} {VER
… [9460 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('tools/chantier/plan.json'))\ndef walk(x,path=''):\n    if isinstance(x,dict):\n        s=json.dumps(x,ensure_ascii=False)\n        if 'U2' in s or 'roue' in s:\n            if 'mandat' in x:\n                print('---',path,x.get('id'),x … [260 caractères tronqués]`

  ```
--- /taches[58] U2 L'empaquetage — la roue et le README
Tâche U2 (suite de T1) : **la roue** — `python3 -m build` (ou `pip wheel .`) produit `drave-0.1.0-py3-none-any.whl`, installée dans un venv **propre** depuis la roue (pas le dépôt) : `drave --version` et `drave analyser` depuis `/tmp` ; le **contrôle négatif** : la roue sans les gold doit-elle échouer (le CLI lit `tools/tests/linguistique/gold_*.json` — si les gold ne sont pas dans la roue, `evaluer` échoue : décide et documente, avec un `--gold` qui dit quoi faire) ; la doc § 8.10 mise à jour. Fiche `reports/rapport-roue.md` + JSON.
  ```

- **bash** `{"command": "sed -n '650,900p' tools/drave.py", "description": "Read evaluer implementation"}`

  ```
if args.json:
        sys.stdout.write(_dumps(annotation.json(avec_duree=duree)))
        if stats is not None:
            print(f"{NOM}: TAGGER API · {_ligne_tagger(stats)}", file=sys.stderr)
    else:
        titre = auto.titre() if auto is not None else None
        print(_sur(formater_annotation(annotation, tagger=stats is not None, stats=stats,
                                       titre=titre)))
    if auto is not None:
        print(f"{NOM}: tagger auto · {auto.message()}", file=sys.stderr)
    return 0


def _module_evaluation():
    """Charge `evaluer_gold.py` (le gold et sa mesure) sans dépendre du répertoire courant."""
    chemin = RACINE / "tools" / "tests" / "linguistique" / "evaluer_gold.py"
    if not chemin.is_file():
        raise FileNotFoundError(f"mesure du gold introuvable : {chemin}")
    spec = importlib.util.spec_from_file_location("_drave_evaluer_gold", chemin)
    if spec is None or spec.loader is None:
        raise ImportError(f"impossible de charger {chemin}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _cibles_gold(phrases: list[dict]) -> list[str]
… [11473 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '900,1120p' tools/drave.py; echo '--- main ---'; sed -n '1120,1340p' tools/drave.py", "description": "Read rest of evaluer and main"}`

  ```
print(_formater_evaluation(rapport))
    return 0


def cmd_rejouer(args: argparse.Namespace) -> int:
    premiere = bl.Heuristique(partition=args.partition).analyser(args.texte, args.langue)
    seconde = bl.Heuristique(partition=args.partition).analyser(args.texte, args.langue)
    if premiere.refus or seconde.refus:
        refus = premiere.refus or seconde.refus
        print(f"{NOM}: refus d'analyse : {refus} "
              "(le texte doit contenir au moins une lettre ou un chiffre)", file=sys.stderr)
        return 3
    canonique_1 = _canonique(premiere)
    canonique_2 = _canonique(seconde)
    identique = canonique_1 == canonique_2
    empreinte = hashlib.sha256(canonique_1.encode("utf-8")).hexdigest()[:16]
    print(f"rejeu identique : {'oui' if identique else 'non'}")
    print(f"  texte      : {args.texte!r}")
    print(f"  langue     : {premiere.langue}")
    print(f"  étiquettes : {len(premiere.etiquettes)}")
    print(f"  JSON       : {len(canonique_1.encode('utf-8'))} octets "
          f"· sha256 {empreinte}…")
    if not identique:
        print("  divergence : les deux analyses ne rendent pas le même JSON canonique",
              file=sys.stderr)
        return
… [19559 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/tests/linguistique/evaluer_gold.py; echo '---'; grep -n \"def charger\\|GOLD\\|RACINE\\|Path(__file__)\\|open(\" tools/tests/linguistique/evaluer_gold.py | head -60", "description": "Read evaluer_gold loading logic"}`

  ```
"""evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) + synthétique (160).

Trois niveaux : POS (token, exact), syntagmes (exact + **par tête**), pragmatique. Quatre
lectures : heuristique, mock neuronal, parallèle, cascade. Le vrai modèle est optionnel
(`--reel`) : s'il ne répond pas, il est refusé, pas simulé.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections import Counter, defaultdict

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl  # noqa: E402

GOLD = pathlib.Path(__file__).with_name("gold.json")
REEL = pathlib.Path(__file__).with_name("gold_reel.json")
SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")


def charger() -> list[dict]:
    hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
    reel = json.loads(REEL.read_text(encoding="utf-8"))["phrases"]
    synth = json.loads(SYNTH.read_text(encoding="utf-8"))["phrases"]
    for p in hand:
        p["source"] = "hand"
    for p in reel:
        p["source"] = "reel"
    return hand + reel + synth


GELE = pathlib.Path(__file__).with_name("gold_ge
… [4320 caractères tronqués]
  ```

- **bash** `{"command": "for d in tools tools/tests tools/tests/linguistique tools/llm tools/schemas; do echo \"== $d\"; ls \"$d\"/__init__.py 2>/dev/null || echo \"(pas d'__init__.py)\"; done; echo '--- imports in bloc_linguistique/restitution ---'; head -60 tools/bloc_linguistique.py; echo '---'; grep -n '^im … [179 caractères tronqués]`

  ```
== tools
(pas d'__init__.py)
== tools/tests
(pas d'__init__.py)
== tools/tests/linguistique
(pas d'__init__.py)
== tools/llm
tools/llm/__init__.py
== tools/schemas
(pas d'__init__.py)
--- imports in bloc_linguistique/restitution ---
#!/usr/bin/env python3
"""bloc_linguistique.py — le bloc d'étiquetage linguistique, du graphème à la pragmatique.

Un seul contrat (`BlocLinguistique.analyser`) et **plusieurs implémentations** :

  - `Heuristique` : CPU, déterministe, ultra-rapide ; elle étiquette la surface et produit des
    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
  - `MockNeuronal` : une implémentation neuronale **de contrat**, déterministe, pour tester la
    substitution et le parallèle sans GPU ;
  - `NeuronalLLM` : l'adaptateur réel, qui interroge un modèle local (`llama-cli`) et rend le
    même type d'annotation ;
  - `NeuronalLLMPOS` : le **tagger** neuronal réel — un modèle local, une liste de tokens, des
    POS alignés par grammaire GBNF ; c'est l'implémentation qualifiée sur le gold ;
  - `Parallele` et `Cascade` : les deux modes de composition. Le parallèle fusionne les
    étiquettes par confiance ; la cascade n'envoie au neuronal que 
… [4014 caractères tronqués]
  ```

- **bash** `{"command": "python3 -m pip --version; python3 --version; python3 -c 'import build; print(build.__version__)' 2>&1; python3 -c 'import setuptools; print(setuptools.__version__)' 2>&1; ls dist 2>/dev/null; grep -n \"dist\\|build\\|egg\" .gitignore", "description": "Check build tooling availability"}`

  ```
pip 26.2.2 from /usr/lib/python3.13/site-packages/pip (python 3.13)
Python 3.13.16
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import build; print(build.__version__)
    ^^^^^^^^^^^^
ModuleNotFoundError: No module named 'build'
84.0.0
4:*.egg-info/
5:/build/
6:/dist/
  ```

- **bash** `{"command": "grep -rn \"la roue\\|rapport-roue\\|U2\" work docs/pilotage/roadmap.md reports 2>/dev/null | head -30; echo '--- plan task U2 neighbors'; python3 - <<'PY'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nt=p['taches']\nfor i in range(55,63):\n    x=t[i]\n    print(i, x.get(' … [155 caractères tronqués]`

  ```
work/ocr/census-cegep.json:14452:   "chemin": "/home/stephane/Data13TB/stephane/archives/CEGEP/import-export-2026-06-20/Documents/Enseignement__02/Cours/SW Engineering/Les 100 schémas du management  La matrice BCG, les 5 forces de Porter, la roue de Deming, la carte des alliés... et 96 autres by David Autissier, Laurent Giraud, Kevin J. Johnson (z-lib.org).pdf",
work/ocr/detection-cegep.json:10499:   "chemin": "/home/stephane/Data13TB/stephane/archives/CEGEP/import-export-2026-06-20/Documents/Enseignement__02/Cours/SW Engineering/Les 100 schémas du management  La matrice BCG, les 5 forces de Porter, la roue de Deming, la carte des alliés... et 96 autres by David Autissier, Laurent Giraud, Kevin J. Johnson (z-lib.org).pdf",
work/ocr/cegep64/controle/train.txt:4596:q2M SJU2TTD sap
work/ocr/cegep64/controle/train.txt:113012:U9P2MS ‘W[OU203S poor
work/ocr/cegep64/controle/train.txt:113030:au} UT YoIeasal US POUL JO JUO1F210} ay] ye U22q sÂeMye Sey Salas STU} ‘sauINTOA paysrqn Apsnoraaid amp
work/ocr/cegep64/controle/train.txt:113047:UL'SUOrJ)e2I [ETUI pue SPA UT pouLIO} samnjons}s perds ayy pue ‘487 Jase] Jo SUOETFISO JU212409
work/ocr/cegep64/controle/train.txt:113112:JO UOTIVIID-J[9S
… [4040 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"packages\\|package-data\\|tool.setuptools\" -n pyproject.toml; echo '--- setup files'; ls setup.py setup.cfg MANIFEST.in 2>/dev/null; echo '--- sizes'; du -sh tools/tests/linguistique/gold*.json; echo '--- imports tools.tests.linguistique'; grep -rn \"tools.tests\\|from tools  … [224 caractères tronqués]`

  ```
15:[tool.setuptools]
16:packages = ["tools"]
--- setup files
--- sizes
444K	tools/tests/linguistique/gold_gele.json
20K	tools/tests/linguistique/gold.json
460K	tools/tests/linguistique/gold_reel.json
16K	tools/tests/linguistique/gold_restitution_v2.json
148K	tools/tests/linguistique/gold_synthetique.json
--- imports tools.tests.linguistique
tools/restitution.py:9:définition de `tools/tests/linguistique/miroir.mesurer`, réutilisée ici pour ne pas en
tools/restitution.py:39:import tools.bloc_linguistique as bl  # noqa: E402
tools/restitution.py:40:from tools.tests.linguistique import miroir as _miroir  # noqa: E402
tools/restitution_v2.py:9:annotables du banc v0 (`tools/tests/linguistique/gold_restitution_v2.json`). L'or ne porte
tools/restitution_v2.py:36:import tools.bloc_linguistique as bl  # noqa: E402
tools/restitution_v2.py:37:from tools import restitution as _r  # noqa: E402
tools/restitution_v3.py:36:import tools.bloc_linguistique as bl  # noqa: E402
tools/restitution_v3.py:37:import tools.restitution_v2 as v2  # noqa: E402
tools/restitution_v3.py:38:from tools import roles_gp  # noqa: E402
tools/tests/linguistique/miroir.py:16:import tools.bloc_linguistique as bl
tools/tests
… [201 caractères tronqués]
  ```

- **bash** `{"command": "grep -n '^import \\|^from ' tools/tests/linguistique/miroir.py tools/tests/linguistique/evaluer_gold.py tools/roles_gp.py tools/roles_vocabulaire.py tools/restitution.py tools/restitution_v2.py tools/restitution_v3.py | sed -n '1,160p'", "description": "List imports of modules needed"}`

  ```
tools/tests/linguistique/miroir.py:8:from __future__ import annotations
tools/tests/linguistique/miroir.py:10:import re
tools/tests/linguistique/miroir.py:12:import pathlib
tools/tests/linguistique/miroir.py:13:import sys
tools/tests/linguistique/miroir.py:16:import tools.bloc_linguistique as bl
tools/tests/linguistique/miroir.py:17:from tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc
tools/tests/linguistique/evaluer_gold.py:7:from __future__ import annotations
tools/tests/linguistique/evaluer_gold.py:9:import argparse
tools/tests/linguistique/evaluer_gold.py:10:import json
tools/tests/linguistique/evaluer_gold.py:11:import pathlib
tools/tests/linguistique/evaluer_gold.py:12:import sys
tools/tests/linguistique/evaluer_gold.py:13:from collections import Counter, defaultdict
tools/tests/linguistique/evaluer_gold.py:17:import bloc_linguistique as bl  # noqa: E402
tools/roles_gp.py:23:from __future__ import annotations
tools/roles_gp.py:25:import re
tools/roles_vocabulaire.py:23:from __future__ import annotations
tools/restitution.py:25:from __future__ import annotations
tools/restitution.py:27:import collections
tools/restitution.py:28:import hashlib
tools/restituti
… [1238 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/restitution.py; echo '--- miroir imports and module constants'; sed -n '1,60p' tools/tests/linguistique/miroir.py; echo '--- roles declarations?'; ls tools/roles_*.py", "description": "Inspect restitution and miroir headers"}`

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
… [4958 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"_construire_tagger\" -A40 tools/drave.py | head -60; echo '--- llm files'; ls tools/llm; echo '--- imports deepseek'; grep -n '^import \\|^from ' tools/llm/deepseek.py 2>/dev/null | head -30", "description": "Check tagger construction imports"}`

  ```
359:def _construire_tagger(partition: str = "alternative"):
360-    """Rend (cascade, stats) ; lève `CleTaggerAbsente` si la clé manque (et ne l'affiche pas)."""
361-    stats = {"appels": 0, "requetes": 0, "cache": 0, "tokens": 0, "latence_s": 0.0,
362-             "modeles": {}, "cle_refusee": 0}
363-    client = _client_tagger()
364-    return _cascade_tagger(_transport_tagger(client, stats), partition=partition,
365-                           stats=stats), stats
366-
367-
368-def _cout_tagger(stats: dict) -> dict:
369-    """Le coût d'une exécution, tel qu'il va dans un rapport (`evaluer --json`)."""
370-    return {"modele": MODELE_TAGGER, "appels": stats["appels"],
371-            "requetes": stats["requetes"], "cache": stats["cache"],
372-            "tokens": stats["tokens"], "latence_s": round(stats["latence_s"], 3),
373-            "modeles_renvoyes": dict(stats["modeles"])}
374-
375-
376-def _cout_pour_phrases(cout: dict, mesurees: int, cible: int) -> dict:
377-    """Le coût d'un lot de `cible` phrases, au prorata du lot **mesuré**.
378-
379-    Le tagger fait **un appel par phrase** : le coût est linéaire en nombre de phrases. On ne
380-    modélise pas la longueur des
… [2357 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"import \\|from \" tools/roles_gp.py tools/roles_vocabulaire.py tools/tests/linguistique/anaphore.py | head -30; echo '--- test empaquetage'; sed -n '1,220p' tools/tests/test_empaquetage.py", "description": "Check remaining imports and packaging test"}`

  ```
tools/roles_gp.py:10:Le module est **pur** (pas d'import du bloc linguistique) : il peut être testé seul, et
tools/roles_gp.py:15:    from tools.roles_gp import role_gp
tools/roles_gp.py:23:from __future__ import annotations
tools/roles_gp.py:25:import re
tools/roles_vocabulaire.py:9:Ce module est la **seule** table de passage. Il est pur (aucun import du bloc) pour que
tools/roles_vocabulaire.py:13:    from tools.roles_vocabulaire import ROLES, normaliser_role
tools/roles_vocabulaire.py:23:from __future__ import annotations
tools/tests/linguistique/anaphore.py:7:from __future__ import annotations
tools/tests/linguistique/anaphore.py:163:    import random as _r
--- test empaquetage
#!/usr/bin/env python3
"""test_empaquetage.py — le paquet `drave` et ses deux entrées.

Ce que le test fige :

- `pyproject.toml` : nom **drave**, version **0.1.0**, `requires-python >= 3.10`,
  **aucune dépendance**, script console `drave = tools.drave:main` ;
- le **chemin historique** `python3 tools/drave.py` rend la même version et analyse ;
- l'entrée `tools.drave:main` est **importable depuis un autre répertoire** (c'est ce que
  l'installation éditable met sur `sys.path`) ;
- **sans installation**
… [4207 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '160,360p' tools/drave.py", "description": "Read tagger import and transport"}`

  ```
def _client_tagger():
    """Le client de l'API. L'import est **local** : le défaut ne charge pas le module réseau."""
    from tools.llm.deepseek import DeepSeek
    return DeepSeek(cle=_cle_tagger())


def _cle_tagger_presente() -> bool:
    """Vrai si une clé est trouvée — sans importer le module réseau et sans l'afficher."""
    try:
        _cle_tagger()
    except CleTaggerAbsente:
        return False
    return True


def _sans_secret(message: str) -> str:
    """Retire la clé d'un message de diagnostic si elle y apparaissait par accident."""
    try:
        cle = _cle_tagger()
    except CleTaggerAbsente:
        return message
    if cle and cle in message:
        return message.replace(cle, "<clé>")
    return message


class _TaggerAuto:
    """Le mode `auto` du tagger : API si une clé existe, heuristique sinon.

    Ce qu'il garantit :

    - **aucun code 4** : une clé refusée (401/403) ou un réseau coupé n'arrête pas le run ;
      l'analyse est rendue par l'heuristique, code 0, avec la cause dans `refus` ;
    - **aucun appel réseau sans clé** : la cascade n'est même pas construite ;
    - **la même analyse que le défaut** quand aucune clé n'existe : l'annotation s
… [8019 caractères tronqués]
  ```

- **bash** `{"command": "du -sh tools/*.py tools/llm tools/tests tools/tests/linguistique | sort -h | tail -15; echo '--- llm init'; cat tools/llm/__init__.py; echo '--- number py'; find tools -maxdepth 1 -name '*.py' | wc -l; find tools/tests -name '*.py' | wc -l; find tools/tests/linguistique -name '*.py' | w … [51 caractères tronqués]`

  ```
48K	tools/protocole_date.py
48K	tools/restitution.py
52K	tools/banc_performance.py
52K	tools/protocole_or_roles.py
52K	tools/retrieval_familles.py
56K	tools/pont_generatif.py
64K	tools/drave.py
64K	tools/verificateur_cic.py
68K	tools/entrainer_moteur.py
72K	tools/panini_334.py
76K	tools/couche_distante.py
80K	tools/aligneur_litteraire.py
164K	tools/bloc_linguistique.py
552K	tools/llm
4,4M	tools/tests
--- llm init
"""Le banc externe de Drave : les modèles que l'on interroge sans voir leurs poids."""
--- number py
370
50
24
  ```

- **bash** `{"command": "grep -rn \"gold_gele\\|gold_reel\\|gold_synthetique\\|gold_restitution_v2\\|GOLD_DEFAUT\" tools/restitution*.py tools/drave.py tools/tests/linguistique/miroir.py | head -40; echo '--- GOLD_DEFAUT defs'; grep -rn \"GOLD_DEFAUT\" tools/restitution*.py", "description": "Locate gold file co … [9 caractères tronqués]`

  ```
tools/restitution_v2.py:9:annotables du banc v0 (`tools/tests/linguistique/gold_restitution_v2.json`). L'or ne porte
tools/restitution_v2.py:45:GOLD_DEFAUT = RACINE / "tools" / "tests" / "linguistique" / "gold_restitution_v2.json"
tools/restitution_v3.py:46:GOLD_DEFAUT = v2.GOLD_DEFAUT
tools/drave.py:971:            defaut = (restitution_v2.GOLD_DEFAUT if args.roles
tools/drave.py:972:                      else restitution_v3.GOLD_DEFAUT)
tools/drave.py:1248:                                "(défaut : tools/tests/linguistique/gold_restitution_v2.json)")
--- GOLD_DEFAUT defs
tools/restitution_v2.py:45:GOLD_DEFAUT = RACINE / "tools" / "tests" / "linguistique" / "gold_restitution_v2.json"
tools/restitution_v3.py:46:GOLD_DEFAUT = v2.GOLD_DEFAUT
  ```

- **bash** `{"command": "grep -rn -- \"--gold\" tools/tests tools/*.sh tools/*.py | head -60; echo '--- test CLI'; ls tools/tests/*cli* tools/tests/test*cli* 2>/dev/null; grep -rn \"evaluer\" tools/tests/test_cli*.py 2>/dev/null | head", "description": "Find uses of --gold"}`

  ```
tools/tests/linguistique/qualifier_cascade.py:77:    ap.add_argument("--gold-reel", action="store_true",
tools/tests/linguistique/qualifier_quatre_modes.py:42:    ap.add_argument("--gold-reel", action="store_true", default=True)
tools/tests/test_restitution_v2.py:75:                       "--gold", str(GOLD))
tools/tests/test_restitution_v3.py:340:        sortie = drave("restituer", "Le chat dort.", "--roles-v3", "--gold", str(GOLD))
tools/porte-produit.sh:44:if python3 tools/verifier_schema_produit.py --gold 20 >/tmp/porte-produit-valide.log 2>&1; then
tools/drave.py:11:    python3 tools/drave.py evaluer --gold --json
tools/drave.py:956:        print(f"{NOM}: erreur d'usage : --gold ne sert qu'avec --banc --roles ou "
tools/drave.py:1121:        "  python3 tools/drave.py evaluer --gold --json\n"
tools/drave.py:1182:        epilog="Exemples : python3 tools/drave.py evaluer --gold --json ; "
tools/drave.py:1187:    evaluer.add_argument("--gold", action="store_true",
tools/drave.py:1246:    restituer.add_argument("--gold", default=None, metavar="CHEMIN",
tools/mesurer_schema_v2_doc.py:7:- `tools/verifier_schema_produit.py --gold 20` : 26 cas, 0 échec attendu ;
tools/mesurer_schema_v2
… [916 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/tests | grep -i 'cli\\|drave\\|produit' ; grep -rn \"evaluer\" tools/tests/test_cli_robuste.py tools/tests/test_produit* 2>/dev/null | head -30; grep -rn \"returncode.*evaluer\\|evaluer.*returncode\" tools/tests/*.py | head -20", "description": "Check CLI tests for evaluer"}`

  ```
test_produit_libre.py
test_produit.py
test_schema_produit.py
tools/tests/test_produit.py:48:            and all(mot in aide.stdout for mot in ("analyser", "evaluer", "rejouer", "--aide")),
tools/tests/test_produit.py:156:        for commande in ("analyser", "evaluer", "rejouer", "restituer"):
tools/tests/test_produit.py:347:    """`evaluer` publie la vue fidèle **et** la vue linéaire (transparence)."""
tools/tests/test_produit.py:350:        sortie = drave("evaluer", "--json")
tools/tests/test_produit.py:388:    """`evaluer --par-langue` scinde la mesure fr/en sans la changer."""
tools/tests/test_produit.py:391:        global_ = drave("evaluer", "--json")
tools/tests/test_produit.py:392:        sortie = drave("evaluer", "--par-langue", "--json")
tools/tests/test_produit.py:411:        sortie = drave("evaluer", "--par-langue")
tools/tests/test_produit.py:424:        sortie = drave("evaluer", "--reel", "--json")
tools/tests/test_produit.py:431:        sortie = drave("evaluer", "--json")
  ```

- **bash** `{"command": "grep -rn \"pip wheel\\|python3 -m build\\|empaquetage\\|drave-0.1.0\" tools/*.sh tools/*.py tools/tests/*.py docs/pilotage/references-non-regression.md | head -40; echo '--- porte produit'; sed -n '1,120p' tools/porte-produit.sh", "description": "Find gates touching wheel/packaging"}`

  ```
tools/verifier_faq.py:353:        "empaquetage": {"livre": "pip install -e . + commande drave",
tools/verifier_faq.py:401:        "empaquetage": {
tools/tests/test_empaquetage.py:2:"""test_empaquetage.py — le paquet `drave` et ses deux entrées.
tools/tests/test_empaquetage.py:16:`reports/rapport-empaquetage.md` et `reports/empaquetage.json`.
--- porte produit
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
a
… [4477 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/tests/test_produit.py; sed -n '330,450p' tools/tests/test_produit.py", "description": "Read product test sections"}`

  ```
"""test_produit.py — le smoke test de bout en bout du point d'entrée `tools/drave.py`.

Huit assertions, deux phrases (fr/en), le déterminisme et les codes de sortie. Le test passe
aussi bien par `python3 tools/tests/test_produit.py` que par `pytest` : il n'importe rien du
dépôt directement, il lance la commande comme un utilisateur.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
CLI = RACINE / "tools" / "drave.py"


def drave(*arguments: str) -> subprocess.CompletedProcess[str]:
    """Lance la commande depuis la racine du dépôt, en UTF-8, sans réseau."""
    return subprocess.run(
        [sys.executable, str(CLI), *arguments],
        cwd=str(RACINE),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )


def detail(resultat: subprocess.CompletedProcess[str]) -> str:
    return (f"code={resultat.returncode}\n"
            f"stdout={resultat.stdout}\n"
            f"stderr={resultat.stderr}")


class TestProduit(unittest.TestCase):
    """Le contrat produit : version/aide, analyse, JSON, rejeu, usage."""


… [6874 caractères tronqués]
  ```

- **bash** `{"command": "git diff --stat; echo '--- plan diff'; git diff tools/chantier/plan.json | head -60; echo '--- reports diff summary'; git diff --numstat reports | head -20", "description": "Inspect uncommitted changes"}`

  ```
reports/pensee-coherence-fiches-v7.json |  19 +
 reports/pensee-dev-test-v10.json        |   2 +-
 reports/pensee-quatre-modes.json        | 734 ++++++++++++++++++--------------
 reports/rapport-audit-v7.md             |   6 +-
 reports/rapport-coherence-fiches-v7.md  |  17 +-
 reports/rapport-dev-test-v10.md         |   2 +-
 reports/rapport-pensee-v12.md           |   4 +-
 reports/rapport-spans-chunker.md        |  13 +-
 tools/chantier/plan.json                | 137 ++++++
 9 files changed, 597 insertions(+), 337 deletions(-)
--- plan diff
diff --git a/tools/chantier/plan.json b/tools/chantier/plan.json
index 53061fbd..e0a071a0 100644
--- a/tools/chantier/plan.json
+++ b/tools/chantier/plan.json
@@ -736,6 +736,143 @@
      "attendu": "OK"
     }
    ]
+  },
+  {
+   "id": "T1",
+   "jour": 19,
+   "titre": "L'empaquetage — pip install et la commande drave",
+   "mandat": "Tâche T1 (exploitable, 1/5) : **l'empaquetage** — écris un **`pyproject.toml`** minimal (le nom `drave`, la version 0.1.0, le `requires-python >= 3.10`, **aucune dépendance**, le `console_scripts` `drave = tools.drave:main` ou un module d'entrée propre), vérifie `python3 -m pip install -e .` dans un **venv tem
… [3069 caractères tronqués]
  ```

- **bash** `{"command": "git check-ignore -v dist build 2>/dev/null; echo '---'; cat .gitignore; echo '--- branch'; git branch --show-current; git log -1 --format='%H %ci %s'", "description": "Check ignore and branch"}`

  ```
---
__pycache__/
*.pyc
.venv/
*.egg-info/
/build/
/dist/
reports/*.tmp
models/
data/
qtrinet-core/target/

# Traces de session : la copie brute reste sur disque (volumineuse, binaire),
# le digest markdown est versionné.
journal/sessions/*/session*.jsonl.zstd
journal/sessions/archive.log

# Outil de référence : la source est versionnée, le binaire se recompile
# (commande exacte dans tools/ref_logits.md).
tools/ref_logits
target/

# docwatch — SVG générés depuis les sources .puml/.mmd (docwatch les produit)
docs/**/*.puml.svg
docs/**/*.mmd.svg

# Campagnes GPU : points de contrôle et journaux de run (hors dépôt, archivés à part)
work/
--- branch
s/v7
04894aeaf6507ce94f86b630ab961010a6891763 2026-11-16 00:28:00 -0500 U1 — LE CONTRÔLE DE L'INSTRUMENT EST CELUI DE LA PASSE : LINÉAIRE 0,71, QUADRATIQUE 2,11 (ET NON LES VALEURS DE T4)
  ```

- **bash** `{"command": "find tools/tests/linguistique -maxdepth 1 -name '*.json' -printf '%f %s\\n' | sort; echo '--- other json in tools/tests'; find tools/tests -name '*.json' -printf '%p %s\\n' | sort | head -30", "description": "List JSON data under tests"}`

  ```
gold_gele.json 450905
gold.json 20009
gold_reel.json 470149
gold_restitution_v2.json 14631
gold_synthetique.json 149211
--- other json in tools/tests
tools/tests/cic/corpus_dor_cic_v1.json 46714
tools/tests/cic/manifeste.json 1066
tools/tests/code/snippets.json 2086
tools/tests/documents/bench-complet.json 97746
tools/tests/documents/bench-durci.json 30352
tools/tests/documents/bench-pilote.json 4376
tools/tests/documents/calibration-lexical.json 285
tools/tests/documents/calibration-paraphrase.json 282
tools/tests/documents/corpus/manifeste.json 7623
tools/tests/linguistique/gold_gele.json 450905
tools/tests/linguistique/gold.json 20009
tools/tests/linguistique/gold_reel.json 470149
tools/tests/linguistique/gold_restitution_v2.json 14631
tools/tests/linguistique/gold_synthetique.json 149211
tools/tests/maths/formules.json 3936
  ```

- **bash** `{"command": "grep -rn \"test_empaquetage\\|empaquetage\" tools/portes.sh tools/porte-*.sh tools/*.py docs/pilotage/references-non-regression.md | head -30; echo '--- count gates'; ls tools/porte-*.sh | wc -l; tail -60 tools/portes.sh", "description": "Check if packaging test is gated"}`

  ```
tools/verifier_faq.py:353:        "empaquetage": {"livre": "pip install -e . + commande drave",
tools/verifier_faq.py:401:        "empaquetage": {
--- count gates
86
    DRAVE_DUMP_COUCHES=/tmp/porte_hc timeout 900 $D "$V41_HC" --ppl /tmp/ids_v41_8.txt \
        --ctx 16 --limit 3 --dense --threads 8 --lot 1 >/dev/null 2>&1
    if ls /tmp/porte_hc-hc_attn-*-*.bin >/dev/null 2>&1; then
        sortie_hc=$(python3 tools/analyse_hc.py /tmp/porte_hc --couches 0,1,2 \
            --positions 0,1,2 2>&1)
        code_hc=$?
        res=$(printf '%s' "$sortie_hc" | grep -oE "connexions significatives.*" | head -1)
        if [ "$code_hc" = "0" ] && [ -n "$res" ]; then
            printf "  %-42s %s  ✅\n" "poids de connexion hc écrits et relus" "$res"
        else
            printf "  %-42s %s  ❌\n" "poids de connexion hc écrits et relus" "échec"
            printf '%s\n' "$sortie_hc" | tail -3 | sed 's/^/      /'
            ECHEC=1
        fi
    else
        printf "  %-42s %s  ❌\n" "poids de connexion hc écrits et relus" "aucun vidage écrit"
        ECHEC=1
    fi
fi

# 8. Le DÉCOUPAGE : deux nœuds, cinq modes de flux, un petit modèle (~20 s).
#    Elle manquait, et c'est exactement po
… [1833 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"test_empaquetage\\|tests/test_produit.py\\|unittest discover\\|pytest\" tools/porte-*.sh | head -40", "description": "Find which gate runs tests"}`

  ```
tools/porte-bloc-linguistique.sh:7:python3 -m unittest discover -s tools/tests/linguistique -p 'test_bloc_linguistique.py' || { echo "❌ tests"; exit 1; }
tools/porte-deepseek.sh:21:python3 -m unittest discover -s tools/llm/tests -t tools || exit 1
tools/porte-jeux.sh:29:python3 -m unittest discover -s tools/jeux/tests -t tools || exit 1
tools/porte-produit.sh:38:if python3 tools/tests/test_produit.py >/tmp/porte-produit-tests.log 2>&1; then
  ```

- **bash** `{"command": "rm -rf /tmp/drave-dist && mkdir -p /tmp/drave-dist && python3 -m pip wheel . --no-deps --no-build-isolation -w /tmp/drave-dist 2>&1 | tail -30; ls -l /tmp/drave-dist", "description": "Build wheel with current config", "timeoutMs": 180000}`

  ```
Processing ./.
  Preparing metadata (pyproject.toml): started
  Preparing metadata (pyproject.toml): finished with status 'done'
Building wheels for collected packages: drave
  Building wheel for drave (pyproject.toml): started
  Building wheel for drave (pyproject.toml): finished with status 'done'
  Created wheel for drave: filename=drave-0.1.0-py3-none-any.whl size=1444207 sha256=e492c9fb3db54f5c778795d610a9259d6362d27e42866799422d47751ae8d438
  Stored in directory: /tmp/pip-ephem-wheel-cache-9ij7m3sc/wheels/96/02/a3/318108f401dc37bb3a575e67c80cf111852262a4b3c9f691ec
Successfully built drave
total 1412
-rw-r--r--. 1 stephane stephane 1444207 16 nov 00:32 drave-0.1.0-py3-none-any.whl
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport zipfile\np='/tmp/drave-dist/drave-0.1.0-py3-none-any.whl'\nz=zipfile.ZipFile(p)\nnames=z.namelist()\nprint(len(names))\nfor n in names[:40]: print(n)\nprint('...')\nfor n in names:\n    if 'gold' in n or 'tests' in n or 'llm' in n: print(n)\nPY", "description":  … [25 caractères tronqués]`

  ```
375
tools/adaptateur_langue.py
tools/aiguille.py
tools/aligneur_litteraire.py
tools/amplification.py
tools/analyse_alignement.py
tools/analyse_empreinte.py
tools/analyse_engram.py
tools/analyse_experts_statique.py
tools/analyse_flux.py
tools/analyse_hc.py
tools/analyse_litteraire.py
tools/analyse_octets_par_jeton.py
tools/analyse_reutilisation_experts.py
tools/analyse_union_experts.py
tools/ancre_professeur.py
tools/applique_pont.py
tools/approximabilite_bloc.py
tools/archive_sessions.py
tools/atomes_prediction.py
tools/audit_drapeaux_harnais.py
tools/banc-experts.py
tools/banc-prelire.py
tools/banc_cli_robuste.py
tools/banc_complet.py
tools/banc_durci.py
tools/banc_lecteur.py
tools/banc_lecture.py
tools/banc_performance.py
tools/blanchiment_entree.py
tools/bloc_code.py
tools/bloc_linguistique.py
tools/bloc_maths.py
tools/bloc_tableaux.py
tools/boucle_directe.py
tools/bruit_entree.py
tools/budget_execution_locale.py
tools/c8_entrainer_tete.py
tools/c8_sonde_lineaire.py
tools/cache_pont.py
tools/calibre_modes.py
...
  ```

- **bash** `{"command": "find tools/tests -maxdepth 1 -type f -printf '%f %s\\n' | sort | head -30; echo '---'; du -sh tools/tests/*.py | tail; echo '--- linguistique py size'; du -sh tools/tests/linguistique/*.py | tail -5", "description": "Inspect tools/tests contents"}`

  ```
qualifier_politique_drvm.py 7758
qualifier_porte_bouge_drvm.py 6567
qualifier_porte_drvm.py 5290
qualifier_porte_fenetre_drvm.py 5997
qualifier_porte_minute_drvm.py 5982
qualifier_porte_mobile_drvm.py 7580
qualifier_porte_sto_drvm.py 6445
qualifier_porte_sto_graines.py 6007
test_banc_performance.py 5932
test_empaquetage.py 4742
test_panini_334.py 3295
test_pensee_politique.py 3591
test_pensee_store.py 1717
test_produit_libre.py 2646
test_produit.py 21122
test_restitution.py 14379
test_restitution_v2.py 10569
test_restitution_v3.py 16202
test_schema_produit.py 6334
test_tagger_api.py 36799
test_verificateur_cic.py 10129
test_verificateur_cic_v2.py 7903
test_verifier_performance_fix.py 2121
---
4,0K	tools/tests/test_produit_libre.py
24K	tools/tests/test_produit.py
16K	tools/tests/test_restitution.py
12K	tools/tests/test_restitution_v2.py
16K	tools/tests/test_restitution_v3.py
8,0K	tools/tests/test_schema_produit.py
36K	tools/tests/test_tagger_api.py
12K	tools/tests/test_verificateur_cic.py
8,0K	tools/tests/test_verificateur_cic_v2.py
4,0K	tools/tests/test_verifier_performance_fix.py
--- linguistique py size
32K	tools/tests/linguistique/qualifier_tagger_h50.py
36K	tools/tests/linguist
… [184 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"prompts_publics\\|Path(__file__)\\|__file__\" tools/llm/*.py | head -30; echo '--- llm size'; du -sh tools/llm/*.jsonl", "description": "Check llm data dependencies"}`

  ```
tools/llm/deepseek.py:43:RACINE = pathlib.Path(__file__).resolve().parents[2]
tools/llm/enseignant.py:15:    python3 tools/llm/enseignant.py --prompts tools/llm/prompts_publics.jsonl \
tools/llm/enseignant.py:18:        --prompts tools/llm/prompts_publics.jsonl --sortie data/deepseek/enseignant.jsonl
tools/llm/enseignant.py:113:    ap.add_argument("--prompts", default=str(pathlib.Path(__file__).with_name("prompts_publics.jsonl")))
tools/llm/entrainer_masque.py:34:sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
tools/llm/prompts_publics.py:2:"""prompts_publics.py — les prompts du banc externe, sans donnée privée.
tools/llm/prompts_publics.py:11:Le fichier produit (`prompts_publics.jsonl`) ne contient **que les prompts** et les
tools/llm/prompts_publics.py:20:RACINE = pathlib.Path(__file__).resolve().parents[2]
tools/llm/prompts_publics.py:22:SORTIE = pathlib.Path(__file__).resolve().parent / "prompts_publics.jsonl"
--- llm size
320K	tools/llm/prompts_publics_300.jsonl
48K	tools/llm/prompts_publics.jsonl
  ```

- **bash** `{"command": "sed -n '30,80p' tools/llm/deepseek.py; grep -n \"RACINE\" tools/llm/deepseek.py", "description": "Inspect deepseek RACINE use"}`

  ```
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field

RACINE = pathlib.Path(__file__).resolve().parents[2]
CACHE_DEFAUT = RACINE / "data" / "deepseek" / "cache"
BASE_DEFAUT = "https://api.deepseek.com"
MODELE_DEFAUT = "deepseek-chat"


class ErreurDeepSeek(Exception):
    """Une erreur de l'API, avec la possibilité de réessayer."""

    def __init__(self, message: str, *, code: int | None = None,
                 reessayable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.reessayable = reessayable


@dataclass
class ReponseDeepSeek:
    contenu: str
    modele: str
    usage: dict = field(default_factory=dict)
    raisonnement: str | None = None
    latence_s: float = 0.0
    cache: bool = False
    brut: dict | None = None

    def __str__(self) -> str:
        return self.contenu


def _cle_env() -> str:
    """La clé, sans jamais l'écrire : variable d'environnement ou fichier 0600.

    `DEEPSEEK_API_KEY` / `DSH_API_KEY` d'abord ; sinon `DEEPSEEK_KEY_FILE` /
    `DSH_KEY_FILE` 
… [294 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/empaquetage.json | head -120; echo '---'; python3 - <<'PY'\nimport json\nd=json.load(open('reports/empaquetage.json'))\nprint(json.dumps(d,ensure_ascii=False,indent=1)[:3000])\nPY", "description": "Read T1 JSON structure"}`

  ```
{
 "schema": "drave.empaquetage.verification",
 "version": 1,
 "date": "2026-11-15",
 "tache": "T1 (exploitable, 1/5)",
 "produit": "0.1.0",
 "pyproject": {
  "fichier": "pyproject.toml",
  "nom": "drave",
  "version": "0.1.0",
  "requires_python": ">=3.10",
  "dependances": [],
  "script_console": "drave = tools.drave:main",
  "build_backend": "setuptools.build_meta",
  "build_requires": ["setuptools>=61"],
  "packages": ["tools"]
 },
 "environnement": {
  "venv": "/tmp/venv-drave",
  "python": "3.13.16",
  "pip": "26.2.1",
  "commande": "python3 -m pip install -e .",
  "cwd": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet",
  "code": 0,
  "resultat": "Successfully installed drave-0.1.0",
  "editable": true,
  "pip_show": {
   "name": "drave",
   "version": "0.1.0",
   "requires": [],
   "editable_project_location": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet"
  }
 },
 "sorties": {
  "drave_version": {
   "commande": "drave --version",
   "cwd": "/tmp",
   "code": 0,
   "stdout": "drave 0.1.0"
  },
  "drave_analyser": {
   "commande": "drave analyser \"Le chat dort.\"",
   "cwd": "/tmp",
   "code": 0,
   "stdout_extrait": [
    "drave 0.1.0 — analyse heuristique (CPU, hors 
… [5890 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"roue\\|U2\\|gold\" journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md 2>/dev/null | tail -40", "description": "Search session plan for U2"}`

  ```
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:65014:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git branch -f master s/v7 && timeout 280 git push origin s/v7 2>&1 | tail -1; timeout 280 git push origin master 2>&1 | tail -1; head -8 reports/rapport-gold-452.md | cut -c1-170", "description": "Pousser W1 et lire le split", "timeo … [14 caractères tronqués]`
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:65019:# W1 — le gold réel 452 : composition, split 402 / H50, sha256 et 10 candidats GP/SUB
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:65022:> **Date** : 2026-11-15 (J1 · 16/11) · **HEAD mesuré** : `6b2208ee` · **Verdict** : ✅ **le gold réel 452 est
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:65023:> nommé et composé ; le split 402/H50 est figé ; le gold est intact ; les 10 GP/SUB sont listés pour S.**
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:65025:**En trois lignes.** (1) Le gold réel fait **452** phrases = **20 hand** (`gold.json`) + **432 corpus**
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md:65026:(`gold_reel.json`) ; **242 fr + 21
… [9965 caractères tronqués]
  ```

- **bash** `{"command": "ls journal | head; echo '--- session e181'; ls -la journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc | head -30; echo '--- plan'; sed -n '1,120p' journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "description": "Inspect journal structure"}`

  ```
2026-09-25
2026-09-26
2026-09-27
2026-09-28
2026-09-29
2026-09-30
2026-10-01
2026-10-02
2026-10-03
2026-10-04
--- session e181
total 25516
drwxr-xr-x. 1 stephane stephane       94 16 nov 00:12 .
drwxr-xr-x. 1 stephane stephane    17048 16 nov 00:17 ..
-rw-r--r--. 1 stephane stephane  4223758 16 nov 00:28 digest.md
-rw-r--r--. 1 stephane stephane     7010 16 nov 00:12 plan.md
-rw-r--r--. 1 stephane stephane   774673 16 nov 00:30 rapport.md
-rw-------. 1 stephane stephane 21112659 16 nov 00:24 session.v4.jsonl.zstd
--- plan
# Plan de session — Pensée, la RSN plurielle et le moteur N3

> **Mandat vivant.** Ouvert le 2026-10-31 22 h 45 HAE depuis
> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md). Ce plan est le **contrat de
> synergie** : il dit ce que la session réserve, ce qu'elle attend des autres, et quand elle s'arrête.
> Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.

- **Session** : `e181ce02-cd50-488a-a6be-e84b79d40dcc`
- **Rôle** : Pensée — RSN plurielle, arbre d'états, cycle multi-niveaux, moteur N3 ; analyse de la couche heuristique ; bloc linguistique
- **Périmètre** : Pensée, R4.4-reste, Coloration, Bloc linguistique (R0.7)
- **Fichie
… [6176 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' docs/methode/resultats.md; echo '--- rangement quick'; sed -n '1,120p' docs/methode/rangement.md", "description": "Read result and filing method"}`

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
… [7725 caractères tronqués]
  ```

- **bash** `{"command": "ls -la journal/2026-11-16 2>/dev/null | head; echo '---'; find journal/2026-11-16 -maxdepth 1 -type f -printf '%f\\n' 2>/dev/null | head; echo '--- last journal dirs'; ls -d journal/2026-11-* | tail -5", "description": "Inspect latest journal day"}`

  ```
total 12
drwxr-xr-x. 1 stephane stephane   58 16 nov 00:30 .
drwxr-xr-x. 1 stephane stephane 1012 16 nov 00:22 ..
-rw-r--r--. 1 stephane stephane 1076 16 nov 00:30 memoire.md
-rw-r--r--. 1 stephane stephane 1352 16 nov 00:30 mesures.md
-rw-r--r--. 1 stephane stephane 1382 16 nov 00:30 README.md
---
README.md
mesures.md
memoire.md
--- last journal dirs
journal/2026-11-07
journal/2026-11-13
journal/2026-11-14
journal/2026-11-15
journal/2026-11-16
  ```

- **bash** `{"command": "sed -n '1,80p' journal/2026-11-15/*.md 2>/dev/null | head -120; echo '--- journal_auto usage'; python3 tools/journal_auto.py --help 2>&1 | head -40", "description": "Read journal format and tool help"}`

  ```
# 2026-11-15 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (9)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 02:27 | `f926b5bc` | C2 — LA PAGE / NE SERT PAS LA V7 : 369 CANDIDATS SANS PROFONDEUR, 41 VERDICTS À RE-JUGER ; PORT 8765 PRIS, PARE-FEU ACTIF ; LES 11 VERDICTS COMMITTÉS (389b99f) | `en-cours.md`, `roadmap.md`, `README.md` (+17) |
| 03:04 | `c37fed06` | B1 — LE PROTOCOLE À DATE CONTRÔLÉE GELÉ : 60 PAIRES (20/20/20), 59 TEXTES, 26 À SIGNER ; LE §334 N'EN FOURNIT QU'UNE DÉJÀ SIGNÉE | `en-cours.md`, `README.md`, `distribue.md` (+16) |
| 04:26 | `f1c6b506` | PHASE 3 (C PUIS B) — N2 (--rope --canal-dir), S (page / et 11 VERDICTS), R (GOLD RÉEL 452), PANINI (PROTOCOLE À DATE CONTRÔLÉE, LES ATOMES NE PRÉDISENT PAS LES NIVEAUX, CIC 42/42) ; 6 FICHES, SEPT. 9 DU PLAN | `en-cours.md`, `semaine-autonome.md`, `README.md` (+12) |
| 06:31 | `7d4e3bc5` | E1 — LA F
… [6188 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('pyproject.toml')\nprint(p.read_text())\nPY", "description": "Re-read pyproject before edit"}`

  ```
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "drave"
version = "0.1.0"
description = "Le point d'entrée produit du bloc linguistique de Drave."
requires-python = ">=3.10"
dependencies = []

[project.scripts]
drave = "tools.drave:main"

[tool.setuptools]
packages = ["tools"]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/pyproject.toml", "old_string": "[tool.setuptools]\npackages = [\"tools\"]", "new_string": "[tool.setuptools]\n# Le paquet est un **namespace** (`tools/` n'a pas d'`__init__.py`) : on déclare les\n# sous-ensembles dont le CLI a besoin. `t … [698 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/pyproject.toml": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/pyproject.toml"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/pyproject.toml</path>
<type>file</type>
<content>
1: [build-system]
2: requires = ["setuptools>=61"]
3: build-backend = "setuptools.build_meta"
4: 
5: [project]
6: name = "drave"
7: version = "0.1.0"
8: description = "Le point d'entrée produit du bloc linguistique de Drave."
9: requires-python = ">=3.10"
10: dependencies = []
11: 
12: [project.scripts]
13: drave = "tools.drave:main"
14: 
15: [tool.setuptools]
16: packages = ["tools"]

(End of file - total 16 lines)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/pyproject.toml", "old_string": "[tool.setuptools]\npackages = [\"tools\"]", "new_string": "[tool.setuptools]\n# Le paquet est un **namespace** (`tools/` n'a pas d'`__init__.py`) : on déclare les\n# sous-ensembles dont le CLI a besoin. `t … [698 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/pyproject.toml has been updated successfully.
  ```

- **bash** `{"command": "rm -rf /tmp/drave-dist && mkdir -p /tmp/drave-dist && python3 -m pip wheel . --no-deps --no-build-isolation -w /tmp/drave-dist 2>&1 | tail -20; echo '--- contents'; python3 - <<'PY'\nimport zipfile,glob\np=glob.glob('/tmp/drave-dist/*.whl')[0]\nz=zipfile.ZipFile(p)\nnames=z.namelist()\n … [241 caractères tronqués]`

  ```
Processing ./.
  Preparing metadata (pyproject.toml): started
  Preparing metadata (pyproject.toml): finished with status 'done'
Building wheels for collected packages: drave
  Building wheel for drave (pyproject.toml): started
  Building wheel for drave (pyproject.toml): finished with status 'done'
  Created wheel for drave: filename=drave-0.1.0-py3-none-any.whl size=1696902 sha256=189cff19a4dfd026d55daee12199a63bfcee07550472c57c5fa410099e153756
  Stored in directory: /tmp/pip-ephem-wheel-cache-q3y4rdsx/wheels/96/02/a3/318108f401dc37bb3a575e67c80cf111852262a4b3c9f691ec
Successfully built drave
--- contents
/tmp/drave-dist/drave-0.1.0-py3-none-any.whl 412
tools/llm/__init__.py
tools/llm/deepseek.py
tools/llm/distillation.py
tools/llm/enseignant.py
tools/llm/entrainer_masque.py
tools/llm/masque.py
tools/llm/mesure.py
tools/llm/prompts_publics.py
tools/tests/linguistique/anaphore.py
tools/tests/linguistique/classement_cible.py
tools/tests/linguistique/classer_gv.py
tools/tests/linguistique/evaluer_gold.py
tools/tests/linguistique/gold.json
tools/tests/linguistique/gold.py
tools/tests/linguistique/gold_gele.json
tools/tests/linguistique/gold_reel.json
tools/tests/linguistique/gold_ree
… [987 caractères tronqués]
  ```

- **bash** `{"command": "set -e\nrm -rf /tmp/venv-drave-roue /tmp/drave-sorties && mkdir -p /tmp/drave-sorties\npython3 -m venv /tmp/venv-drave-roue\n/tmp/venv-drave-roue/bin/python -m pip install --no-index --no-deps /tmp/drave-dist/drave-0.1.0-py3-none-any.whl >/tmp/drave-sorties/install.log 2>&1\ncat /tmp/dr … [778 caractères tronqués]`

  ```
Processing /tmp/drave-dist/drave-0.1.0-py3-none-any.whl
Installing collected packages: drave
Successfully installed drave-0.1.0
Name: drave
Version: 0.1.0
Summary: Le point d'entrée produit du bloc linguistique de Drave.
Home-page: 
Author: 
Author-email: 
License: 
Location: /tmp/venv-drave-roue/lib64/python3.13/site-packages
Requires: 
Required-by: 
version code=0
analyser code=0
evaluer code=0
3182 /tmp/drave-sorties/evaluer.json
drave 0.1.0
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=objet     → dort
  GV   [8:12]  dort     rôle=predicat  → —
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py analyser \"Le chat dort.\" | sed -n '1,12p'; echo '--- compare json roles'; python3 tools/drave.py analyser \"Le chat dort.\" --json > /tmp/drave-sorties/repo.json; python3 - <<'PY'\nimport json\nfor n in ('rep … [321 caractères tronqués]`

  ```
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
--- compare json roles
repo [('syntagme', 'GN', None, None), ('syntagme', 'GV', None, None)]
wheel [Errno 2] No such file or directory: '/tmp/drave-sorties/wheel.json'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"structures\\|donnees\\|static\\|lexique\\|role\" tools/bloc_linguistique.py | head -60; echo '--- structures content'; ls tools/structures; find tools/structures -maxdepth 2 -type f | head -20; git submodule status", "desc … [43 caractères tronqués]`

  ```
53:    from . import roles_gp as _roles_gp
54:    from .roles_vocabulaire import normaliser_role as _normaliser_role
56:    import roles_gp as _roles_gp
57:    from roles_vocabulaire import normaliser_role as _normaliser_role
99:def normaliser_role(role: str, strict: bool = True) -> str:
100:    """Le rôle canonique (voir `tools/roles_vocabulaire.py`)."""
101:    return _normaliser_role(role, strict=strict)
107:    Le rôle brut reste dans l'objet Python (`e.meta["role"]`) : les règles internes et
112:    if "role" in sortie:
113:        sortie["role"] = normaliser_role(sortie.get("role", ""))
115:        if isinstance(alternative, dict) and "role" in alternative:
116:            alternative["role"] = normaliser_role(alternative.get("role", ""))
307:# --------------------------------------------------------------------------- lexiques
425:# Un lexique verbal minimal, bilingue, pour arbitrer les classes ouvertes : le POS de surface
742:def _role_gp(prep: str, suivant: str = "", precedent: str = "",
753:        return _roles_gp.role_gp(prep, suivant=suivant, precedent=precedent,
1043:    @staticmethod
1062:    @staticmethod
1067:    @staticmethod
1072:    @staticmethod
1111:    @stati
… [3293 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1180,1245p' tools/bloc_linguistique.py; echo '--- grep import inside methods'; grep -n \"import \" tools/bloc_linguistique.py | sed -n '1,120p' | tail -30", "description": "Inspect structures import in heuristics"}`

  ```
# commence au clitique (il en fait partie).
                k = 1
                while k < len(mots) and _normaliser(mots[k][2]) in _clitiques:
                    k += 1
                if k >= len(mots):
                    sortie.append(s)
                    continue
                suivant = mots[k]
                ns = _normaliser(suivant[2])
                sv = (suivant[0] in pos_verbes or _est_verbe(suivant[2])
                      or ns in AUXILIAIRES
                      or self._pos(langue, suivant[2])[0] == "VERB"
                      or ns in {"ne", "n'", "n’"})
                # un nom propre sujet : un seul mot, majuscule, pas un mot fermé ; la
                # forme inversée « Peux-tu » est un verbe + enclitique, pas un sujet.
                nom_propre = ("-" not in mots[0][2] and mots[0][2][:1].isupper()
                              and not _est_verbe(mots[0][2])
                              and self._pos(langue, mots[0][2])[0] != "VERB"
                              and n0 not in lex.get("DET", set())
                              and n0 not in lex.get("PREP", set())
                              and n0 not in lex.get("CONJ", set())
                      
… [2717 caractères tronqués]
  ```

- **bash** `{"command": "grep -n '^import \\|^from \\|Path(__file__)\\|RACINE\\|donnees' tools/structures/generateur.py | head -50; echo '--- sizes'; du -sh tools/structures/*.py tools/structures/donnees; echo '--- git ls-tree tools/structures'; git ls-tree HEAD tools/structures; git ls-tree HEAD tools/structur … [127 caractères tronqués]`

  ```
12:from __future__ import annotations
14:import json
15:import re
16:import unicodedata
--- sizes
8,0K	tools/structures/arbre_svg.py
8,0K	tools/structures/candidats_corpus.py
8,0K	tools/structures/construire_donnees.py
12K	tools/structures/exporter_corpus.py
32K	tools/structures/generateur.py
8,0K	tools/structures/llm.py
12K	tools/structures/mesure_analyseur.py
4,0K	tools/structures/mesure_arbre.py
12K	tools/structures/mesure_corpus.py
16K	tools/structures/serveur.py
8,0K	tools/structures/verifier_corpus.py
636K	tools/structures/donnees
--- git ls-tree tools/structures
160000 commit 648adce3ea18ef4d142778fd67d42413aae5ae64	tools/structures
tools/structures
  ```

- **bash** `{"command": "ls tools/structures/__init__.py 2>/dev/null || echo no-init; sed -n '1,40p' tools/structures/generateur.py; grep -n \"segmente\\|analyser\" tools/structures/generateur.py | tail -20; echo '--- bloc heur init'; grep -n \"def __init__\" -A35 tools/bloc_linguistique.py | grep -A35 \"class  … [90 caractères tronqués]`

  ```
no-init
#!/usr/bin/env python3
"""generateur.py — une phrase brute → des structures candidates (v0 heuristique).

Ce n'est pas un analyseur syntaxique : c'est un **générateur de candidats** à faire valider par
un humain. Il segmente (GN, GV, GP, REL, SUB), devine des rôles par la préposition, puis produit
plusieurs candidats en variant l'**attachement** de chaque segment ambigu (GN le plus proche ou
GV le plus proche).

    python3 generateur.py "Le chat de la voisine qui dort sur le toit se réveille."
    python3 generateur.py --json "..."     # la structure complète
"""
from __future__ import annotations

import json
import re
import unicodedata

DET = set("le la les l un une ce cet cette ces mon ma mes ton ta tes son sa ses "
          "notre nos votre vos leur leurs quel quelle quels quelles".split())
PREP = set("a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis "
           "pendant durant contre malgre selon pres loin devant derriere apres avant".split())
RELATIFS = set("qui que qu dont ou quoi".split())
CONJ = set("et ou mais donc or ni car quand comme si parce puisque lorsque pendant quoique".split())
COORD = set("et ou mais donc or ni car".spl
… [1741 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class Heuristique\" -A60 tools/bloc_linguistique.py | head -70", "description": "Read Heuristique constructor"}`

  ```
1012:class Heuristique:
1013-    """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""
1014-
1015-    nom = "heuristique"
1016-
1017-    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
1018-                 seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
1019-                 union: bool = True, partition: str = "alternative"):
1020-        self.profils = profils
1021-        self.segmenter_s = segmenter_s
1022-        self.seuil_ouvert = seuil_ouvert
1023-        self.seuil_langue = seuil_langue
1024-        self.union = union
1025-        # "brut" : la sortie d'avant (chevauchements non documentés) ; "alternative" :
1026-        # les deux segments restent, `meta.alternative` dit lequel est préféré ;
1027-        # "filtrer_union" : on retire le S qui **contient** un segment chunker (le filtre
1028-        # union du P0-3) ; "filtrer" : partition stricte, le chunker est la partition.
1029-        # Dans les deux filtres, le segment retiré reste dans `meta.alternative` (`retire`).
1030-        if partition not in ("brut", "alternative", "filtrer_union", "filtrer"):
1031-            raise ValueEr
… [1912 caractères tronqués]
  ```

- **bash** `{"command": "grep -n '^import \\|^from ' tools/structures/generateur.py; grep -n '^import \\|^from ' tools/structures/*.py | grep -v \"generateur.py\" | head -40", "description": "Check structures imports"}`

  ```
12:from __future__ import annotations
14:import json
15:import re
16:import unicodedata
tools/structures/arbre_svg.py:13:from __future__ import annotations
tools/structures/arbre_svg.py:15:import html
tools/structures/arbre_svg.py:16:import pathlib
tools/structures/arbre_svg.py:17:import sys
tools/structures/arbre_svg.py:19:import generateur
tools/structures/candidats_corpus.py:12:from __future__ import annotations
tools/structures/candidats_corpus.py:14:import argparse
tools/structures/candidats_corpus.py:15:import hashlib
tools/structures/candidats_corpus.py:16:import json
tools/structures/candidats_corpus.py:17:import pathlib
tools/structures/candidats_corpus.py:18:import re
tools/structures/candidats_corpus.py:19:import sys
tools/structures/candidats_corpus.py:20:import time
tools/structures/candidats_corpus.py:22:import exporter_corpus
tools/structures/candidats_corpus.py:23:import generateur
tools/structures/candidats_corpus.py:24:import mesure_corpus
tools/structures/construire_donnees.py:7:import json, pathlib
tools/structures/exporter_corpus.py:29:from __future__ import annotations
tools/structures/exporter_corpus.py:31:import argparse
tools/structures/exporter_corpus.py:3
… [1100 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/pyproject.toml", "old_string": "packages = [\"tools\", \"tools.llm\", \"tools.tests.linguistique\"]", "new_string": "packages = [\"tools\", \"tools.llm\", \"tools.structures\", \"tools.tests.linguistique\"]"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/pyproject.toml has been updated successfully.
  ```

- **bash** `{"command": "set -e\nrm -rf /tmp/drave-dist && mkdir -p /tmp/drave-dist\npython3 -m pip wheel . --no-deps --no-build-isolation -w /tmp/drave-dist >/tmp/drave-sorties/build2.log 2>&1\ntail -4 /tmp/drave-sorties/build2.log\nrm -rf /tmp/venv-drave-roue\npython3 -m venv /tmp/venv-drave-roue\n/tmp/venv-d … [512 caractères tronqués]`

  ```
Building wheel for drave (pyproject.toml): finished with status 'done'
  Created wheel for drave: filename=drave-0.1.0-py3-none-any.whl size=1735157 sha256=29a9d4e84d59cc47781bb06842280f990fab4a2da902e12f6f9e539b433e3214
  Stored in directory: /tmp/pip-ephem-wheel-cache-zxg7o_md/wheels/96/02/a3/318108f401dc37bb3a575e67c80cf111852262a4b3c9f691ec
Successfully built drave
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·
--- wheel contents structures
tools/structures/arbre_svg.py
tools/structures/candidats_corpus.py
tools/structures/construire_donnees.py
tools/structures/exporter_corpus.py
tools/structures/generateur.py
tools/structures/llm.py
tools/structures/mesure_analyseur.py
tools/structures/mesure_arbre.py
tools/structures/mesure_corpus.py
tools/s
… [56 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "offset": 655, "limit": 40}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
655:         titre = auto.titre() if auto is not None else None
656:         print(_sur(formater_annotation(annotation, tagger=stats is not None, stats=stats,
657:                                        titre=titre)))
658:     if auto is not None:
659:         print(f"{NOM}: tagger auto · {auto.message()}", file=sys.stderr)
660:     return 0
661: 
662: 
663: def _module_evaluation():
664:     """Charge `evaluer_gold.py` (le gold et sa mesure) sans dépendre du répertoire courant."""
665:     chemin = RACINE / "tools" / "tests" / "linguistique" / "evaluer_gold.py"
666:     if not chemin.is_file():
667:         raise FileNotFoundError(f"mesure du gold introuvable : {chemin}")
668:     spec = importlib.util.spec_from_file_location("_drave_evaluer_gold", chemin)
669:     if spec is None or spec.loader is None:
670:         raise ImportError(f"impossible de charger {chemin}")
671:     module = importlib.util.module_from_spec(spec)
672:     sys.modules[spec.name] = module
673:     spec.loader.exec_module(module)
674:     return module
675: 
676: 
677: def _cibles_gold(phrases: list[dict
… [742 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 55, "offset": 95}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
95: # --------------------------------------------------------------------------- le tagger (option)
96: 
97: 
98: class CleTaggerAbsente(RuntimeError):
99:     """Aucune clé : le tagger est une option, jamais un prérequis du produit."""
100: 
101: 
102: class CleTaggerRefusee(RuntimeError):
103:     """L'API refuse la clé (HTTP 401/403) : ce n'est pas un refus de phrase, c'est un arrêt.
104: 
105:     Une clé absente et une clé refusée sont la même dépendance manquante du point de vue du
106:     produit : le code 4, un message qui nomme les trois sources de la clé, et rien sur `stdout`.
107:     """
108: 
109:     def __init__(self, code: int) -> None:
110:         self.code = int(code)
111:         super().__init__(
112:             f"clé DeepSeek refusée (HTTP {self.code}) : vérifiez DEEPSEEK_KEY_FILE, "
113:             f"~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. "
114:             f"Sans --tagger, le défaut reste l'heuristique hors ligne."
115:         )
116: 
117: 
118: class ErreurEntree(RuntimeError):
119:     """L'entrée `--fichier` n'est pas lisible : le code d
… [1296 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "class ErreurEntree(RuntimeError):\n    \"\"\"L'entrée `--fichier` n'est pas lisible : le code dit pourquoi (4 ou 5), sans trace.", "new_string": "class GoldAbsent(RuntimeError):\n    \"\"\"Une roue amputée … [580 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "GOLD_VIVANT = (\"gold.json\", \"gold_reel.json\", \"gold_synthetique.json\")\nGOLD_GELE = (\"gold_gele.json\",)\n\n\ndef _module_evaluation(gele: bool = False):\n    \"\"\"Charge `evaluer_gold.py` et vérif … [2258 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 15, "offset": 812}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
812:             ]
813:             t = m.get("tagger")
814:             if t:
815:                 lignes.append(
816:                     f"      TAGGER POS {_pct(t['pos']['exactitude'])} "
817:                     f"· Δ {_points(t['delta_pos'])} "
818:                     f"· SYNTAGMES F1 {_pct(t['syntagme']['f1'])} "
819:                     f"(tête {_pct(t['syntagme']['tete']['f1'])})")
820:     return "\n".join(lignes)
821: 
822: 
823: def cmd_evaluer(args: argparse.Namespace) -> int:
824:     if getattr(args, "tagger_auto", False):
825:         print(f"{NOM}: erreur d'usage : --tagger auto n'est disponible que pour analyser",
826:               file=sys.stderr)

(Showing lines 812-826 of 1328. Use offset=827 to continue.)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 10, "offset": 826}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
826:               file=sys.stderr)
827:         return 5
828:     evaluateur = _module_evaluation()
829:     phrases = evaluateur.charger_gele() if args.gold else evaluateur.charger()
830:     if getattr(args, "reel", False):
831:         # la **base honnête** : les phrases réelles (main + corpus), sans le synthétique
832:         phrases = [p for p in phrases if p.get("source") in ("hand", "reel")]
833:     cascade = None
834:     stats = None
835:     if getattr(args, "tagger", False):

(Showing lines 826-835 of 1328. Use offset=836 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "    evaluateur = _module_evaluation(gele=bool(args.gold))", "old_string": "    evaluateur = _module_evaluation()"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 45, "offset": 1290}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
1290:                                 "rôles avec --roles)")
1291:     restituer.set_defaults(fonction=cmd_restituer)
1292:     return parseur
1293: 
1294: 
1295: def main(argv: list[str] | None = None) -> int:
1296:     # un stdout non-UTF-8 ne doit pas faire planter l'en-tête (« — ») : on tolère les remplacements
1297:     try:
1298:         sys.stdout.reconfigure(encoding="utf-8", errors="replace")
1299:     except (AttributeError, ValueError):
1300:         pass
1301:     brut = list(sys.argv[1:] if argv is None else argv)
1302:     args = construire_parseur().parse_args(_normaliser_tagger(brut))
1303:     args.tagger_mode = ("auto" if getattr(args, "tagger_auto", False)
1304:                         else "api" if getattr(args, "tagger", False) else None)
1305:     try:
1306:         return args.fonction(args)
1307:     except BrokenPipeError:
1308:         # `drave analyser ... | head` : le lecteur a fermé la sortie, ce n'est pas une erreur.
1309:         return 0
1310:     except KeyboardInterrupt:
1311:         print(f"{NOM}: interrompu", file=sys.stderr)
1312:         ret
… [902 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "    except GoldAbsent as exc:\n        # les gold sont une dépendance de données : code 4, rien sur stdout, pas de trace\n        print(f\"{NOM}: dépendance absente : {exc}\", file=sys.stderr)\n        ret … [97 caractères tronqués]`

  ```
Error: old_string matched 2 times in "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py"; provide a more specific old_string or set replace_all to true
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "    except ErreurEntree as exc:\n        # --fichier : dépendance (4) ou usage (5), message clair, rien sur stdout, pas de trace\n        prefixe = \"erreur d'usage\" if exc.code == 5 else \"dépendance abs … [699 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 35, "offset": 1218}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
1218:         formatter_class=_Formateur,
1219:     )
1220:     evaluer.add_argument("--gold", action="store_true",
1221:                          help="mesurer le gold gelé (référence figée) au lieu du gold vivant")
1222:     evaluer.add_argument("--reel", action="store_true",
1223:                          help="mesurer la base honnête : les phrases réelles (hand + reel), sans synthétique")
1224:     evaluer.add_argument("--par-langue", action="store_true",
1225:                          help="scinder la mesure en français et en anglais")
1226:     evaluer.add_argument("--tagger", action="store_true",
1227:                          help="mesurer en plus la cascade POS de l'API DeepSeek (clé et réseau)")
1228:     evaluer.add_argument("--tagger-auto", action="store_true", help=argparse.SUPPRESS)
1229:     evaluer.add_argument("--json", action="store_true",
1230:                          help="sortie JSON des mesures complètes")
1231:     evaluer.set_defaults(fonction=cmd_evaluer)
1232: 
1233:     rejouer = sous.add_parser(
1234:         "rejouer",
1235:         help="analyser de
… [1274 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "new_string": "    evaluer.add_argument(\"--gold\", action=\"store_true\",\n                         help=\"mesurer le gold gelé gold_gele.json (livré avec la roue) au lieu \"\n                              \"du gold viv … [279 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py evaluer --json >/tmp/drave-sorties/repo-eval.json && echo \"eval code=$?\" && python3 tools/drave.py evaluer --gold --json >/tmp/drave-sorties/repo-eval-gele.json && echo \"gele code=$?\" && python3 tools/drave … [95 caractères tronqués]`

  ```
eval code=0
gele code=0
usage: drave evaluer [-h] [--gold] [--reel] [--par-langue] [--tagger] [--json]

Mesure POS, syntagmes (F1/tête) et attachement (exact/couverture) sur le gold, avec un contrôle négatif reproductible. Avec --par-langue, donne le même détail pour le français et l'anglais. Avec --tagger, mesure en plus la cascade POS de l'API DeepSeek et son écart.
--
  --gold              mesurer le gold gelé gold_gele.json (livré avec la roue) au lieu du gold
                      vivant ; si les gold manquent, evaluer sort en 4 et dit quoi faire
  --reel              mesurer la base honnête : les phrases réelles (hand + reel), sans synthétique
--
Exemples : python3 tools/drave.py evaluer --gold --json ; python3 tools/drave.py evaluer --par-langue ; python3 tools/drave.py evaluer --tagger
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py", "limit": 80, "offset": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """test_empaquetage.py — le paquet `drave` et ses deux entrées.
3: 
4: Ce que le test fige :
5: 
6: - `pyproject.toml` : nom **drave**, version **0.1.0**, `requires-python >= 3.10`,
7:   **aucune dépendance**, script console `drave = tools.drave:main` ;
8: - le **chemin historique** `python3 tools/drave.py` rend la même version et analyse ;
9: - l'entrée `tools.drave:main` est **importable depuis un autre répertoire** (c'est ce que
10:   l'installation éditable met sur `sys.path`) ;
11: - **sans installation**, `drave` échoue **proprement** : code 127, « command not found »,
12:   pas de trace Python.
13: 
14: Le test ne crée pas de venv et ne télécharge rien : la vérification complète
15: `python3 -m pip install -e .` dans `/tmp/venv-drave` est consignée dans
16: `reports/rapport-empaquetage.md` et `reports/empaquetage.json`.
17: """
18: from __future__ import annotations
19: 
20: import os
21: import pathlib
22: import shutil
23: import subprocess
24: import sys
25: import tempfile
26: import unittest
27: 
28: RACINE = pathlib.Path(
… [2330 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py", "limit": 60, "offset": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py</path>
<type>file</type>
<content>
80:     def test_analyser(self):
81:         r = _executer([sys.executable, "tools/drave.py", "analyser", "Le chat dort."],
82:                       RACINE)
83:         self.assertEqual(r.returncode, 0, r.stderr)
84:         self.assertIn("GN", r.stdout)
85:         self.assertIn("Le chat", r.stdout)
86: 
87: 
88: class TestEntreeInstallable(unittest.TestCase):
89:     def test_import_depuis_un_autre_repertoire(self):
90:         with tempfile.TemporaryDirectory() as tmp:
91:             env = dict(os.environ)
92:             env["PYTHONPATH"] = str(RACINE)
93:             env.pop("VIRTUAL_ENV", None)
94:             r = _executer(
95:                 [sys.executable, "-c",
96:                  "from tools.drave import main; main(['--version'])"],
97:                 pathlib.Path(tmp), env=env,
98:             )
99:             self.assertEqual(r.returncode, 0, r.stderr)
100:             self.assertEqual(r.stdout.strip(), VERSION)
101: 
102: 
103: class TestControleNegatif(unittest.TestCase):
104:     def test_sans_installation_echec_propre(self):
105:         "
… [859 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py", "new_string": "Ce que le test fige :\n\n- `pyproject.toml` : nom **drave**, version **0.1.0**, `requires-python >= 3.10`,\n  **aucune dépendance**, script console `drave = tools.drave:main` ;\n- la **rou … [1934 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py", "new_string": "    def test_script_console(self):\n        project = _lire_pyproject()[\"project\"]\n        self.assertEqual(project[\"scripts\"][\"drave\"], \"tools.drave:main\")\n\n    def test_sous_p … [1147 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py", "new_string": "class TestOrAbsent(unittest.TestCase):\n    \"\"\"Le contrôle négatif de la roue : sans gold, `evaluer` refuse de mesurer.\"\"\"\n\n    def test_evaluer_sans_gold_code_4(self):\n        if … [992 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_empaquetage.py 2>&1 | tail -30", "description": "Run packaging tests", "timeoutMs": 120000}`

  ```
test_sans_installation_echec_propre (__main__.TestControleNegatif.test_sans_installation_echec_propre)
PATH vide : le nom `drave` n'est pas résolu, et l'échec est lisible. ... ok
test_analyser (__main__.TestEntreeHistorique.test_analyser) ... ok
test_version (__main__.TestEntreeHistorique.test_version) ... ok
test_import_depuis_un_autre_repertoire (__main__.TestEntreeInstallable.test_import_depuis_un_autre_repertoire) ... ok
test_aucune_dependance (__main__.TestMetadonnees.test_aucune_dependance) ... ok
test_gold_dans_la_roue (__main__.TestMetadonnees.test_gold_dans_la_roue)
Les cinq gold de la mesure voyagent comme données du paquet. ... ok
test_identite_et_python (__main__.TestMetadonnees.test_identite_et_python) ... ok
test_pyproject_existe (__main__.TestMetadonnees.test_pyproject_existe) ... ok
test_script_console (__main__.TestMetadonnees.test_script_console) ... ok
test_sous_paquets_de_la_roue (__main__.TestMetadonnees.test_sous_paquets_de_la_roue)
Le CLI a besoin de la mesure, du générateur S et du tagger dans la roue. ... ok
test_evaluer_sans_gold_code_4 (__main__.TestOrAbsent.test_evaluer_sans_gold_code_4) ... FAIL

=========================================================
… [724 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py", "new_string": "        with tempfile.TemporaryDirectory() as tmp:\n            dossier = pathlib.Path(tmp) / \"tools\" / \"tests\" / \"linguistique\"\n            dossier.mkdir(parents=True)\n            … [231 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_empaquetage.py has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_empaquetage.py 2>&1 | tail -12", "description": "Re-run packaging tests", "timeoutMs": 120000}`

  ```
Les cinq gold de la mesure voyagent comme données du paquet. ... ok
test_identite_et_python (__main__.TestMetadonnees.test_identite_et_python) ... ok
test_pyproject_existe (__main__.TestMetadonnees.test_pyproject_existe) ... ok
test_script_console (__main__.TestMetadonnees.test_script_console) ... ok
test_sous_paquets_de_la_roue (__main__.TestMetadonnees.test_sous_paquets_de_la_roue)
Le CLI a besoin de la mesure, du générateur S et du tagger dans la roue. ... ok
test_evaluer_sans_gold_code_4 (__main__.TestOrAbsent.test_evaluer_sans_gold_code_4) ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.731s

OK
  ```

- **bash** `{"command": "set -u\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nrm -rf dist && mkdir -p dist\npython3 -m pip wheel . --no-deps --no-build-isolation -w dist > /tmp/drave-sorties/build-final.log 2>&1\ncode=$?; echo \"build code=$code\"; tail -6 /tmp/drave-sorties/build-final.log\nls -l dist\n … [606 caractères tronqués]`

  ```
build code=0
Building wheels for collected packages: drave
  Building wheel for drave (pyproject.toml): started
  Building wheel for drave (pyproject.toml): finished with status 'done'
  Created wheel for drave: filename=drave-0.1.0-py3-none-any.whl size=1735736 sha256=cb6922ce07f312fc5a5e3a9fe320d6bf52931babf18f22ba17818767abc51542
  Stored in directory: /tmp/pip-ephem-wheel-cache-7k9jkxmw/wheels/96/02/a3/318108f401dc37bb3a575e67c80cf111852262a4b3c9f691ec
Successfully built drave
total 1696
-rw-r--r--. 1 stephane stephane 1735736 16 nov 00:36 drave-0.1.0-py3-none-any.whl
cb6922ce07f312fc5a5e3a9fe320d6bf52931babf18f22ba17818767abc51542  dist/drave-0.1.0-py3-none-any.whl
entrees 423
gold ['tools/tests/linguistique/gold.json', 'tools/tests/linguistique/gold.py', 'tools/tests/linguistique/gold_gele.json', 'tools/tests/linguistique/gold_reel.json', 'tools/tests/linguistique/gold_reel.py', 'tools/tests/linguistique/gold_reel_50.py', 'tools/tests/linguistique/gold_restitution_v2.json', 'tools/tests/linguistique/gold_split.py', 'tools/tests/linguistique/gold_synthetique.json', 'tools/tests/linguistique/gold_synthetique.py']
miroir True
structures ['tools/structures/arbre_svg.py', 'tools/s
… [100 caractères tronqués]
  ```

- **bash** `{"command": "set -u\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nrm -rf /tmp/venv-drave-roue /tmp/drave-home /tmp/drave-sorties && mkdir -p /tmp/drave-home /tmp/drave-sorties\npython3 -m venv /tmp/venv-drave-roue\n/tmp/venv-drave-roue/bin/python -m pip install --no-index --no-deps --no-cache … [2094 caractères tronqués]`

  ```
install code=0
Processing ./dist/drave-0.1.0-py3-none-any.whl
Installing collected packages: drave
Successfully installed drave-0.1.0
Name: drave
Version: 0.1.0
Summary: Le point d'entrée produit du bloc linguistique de Drave.
Home-page: 
Author: 
Author-email: 
License: 
Location: /tmp/venv-drave-roue/lib64/python3.13/site-packages
Requires: 
Required-by: 
version code=0
analyser code=0
analyser-en code=0
analyser-json code=0
evaluer code=0
evaluer-gele code=0
restituer code=0
tagger code=4
--- version
drave 0.1.0
--- analyser
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·
--- tagger err
drave: dépendance absente : clé DeepSeek absente : exportez DEEPSEEK_KEY_FILE, déposez la clé dans ~/.config/drave/deepseek.key, ou exportez DEEPSEEK_API_KEY. Sa
… [211 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/drave.py analyser \"Le chat dort.\" --json > /tmp/drave-sorties/repo.json 2>/tmp/drave-sorties/repo.json.err; echo \"repo json code=$?\"; cmp -s /tmp/drave-sorties/repo.json /tmp/drave-sorties/wheel.json; echo \"cmp ana … [421 caractères tronqués]`

  ```
repo json code=0
cmp analyser JSON=0
equal True
cmp evaluer JSON=0
  ```

- **bash** `{"command": "set -u\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nrm -rf /tmp/drave-amputee && mkdir -p /tmp/drave-amputee\npython3 - <<'PY'\nimport zipfile, pathlib, shutil\nsrc = pathlib.Path('dist/drave-0.1.0-py3-none-any.whl')\ndst = pathlib.Path('/tmp/drave-amputee/drave-0.1.0-py3-none-a … [2558 caractères tronqués]`

  ```
stripped /tmp/drave-amputee/drave-0.1.0-py3-none-any.whl 1633914
gold restants []
evaluer_gold True
install amputee code=0
Processing /tmp/drave-amputee/drave-0.1.0-py3-none-any.whl
Installing collected packages: drave
Successfully installed drave-0.1.0
amputee version code=0
amputee analyser code=0
amputee evaluer code=4
amputee evaluer --gold code=4
--- evaluer stderr
drave: dépendance absente : gold absent de cette installation : gold.json, gold_reel.json, gold_synthetique.json (attendu dans /tmp/venv-drave-roue-amputee/lib/python3.13/site-packages/tools/tests/linguistique). La roue doit contenir les gold ; réinstallez la roue complète, ou mesurez depuis le dépôt avec `python3 tools/drave.py evaluer`. Le drapeau `--gold` sélectionne le gold gelé (`gold_gele.json`) s'il est présent ; il ne remplace pas un gold absent.
--- evaluer stdout bytes
0
--- evaluer --gold stderr
drave: dépendance absente : gold absent de cette installation : gold_gele.json (attendu dans /tmp/venv-drave-roue-amputee/lib/python3.13/site-packages/tools/tests/linguistique). La roue doit contenir les gold ; réinstallez la roue complète, ou mesurez depuis le dépôt avec `python3 tools/drave.py evaluer`. Le drape
… [432 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 40, "offset": 905}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
905: (`objet` et `qualite` sont larges) et le span d'un candidat est sa première occurrence dans
906: le texte. Le format est versionné ; la **qualité linguistique** ne l'est pas.
907: 
908: ### 8.10 Comment l'installer et le lancer ?
909: 
910: Deux chemins, le même CLI. **Depuis le dépôt, sans rien installer** : `python3 tools/drave.py …`
911: depuis la racine (Python **3.10+**, mesuré ici en 3.13), **aucune dépendance externe**, aucun GPU.
912: **Comme commande `drave`** : dans un venv, depuis la racine,
913: 
914: ```bash
915: python3 -m venv /tmp/venv-drave
916: . /tmp/venv-drave/bin/activate
917: python3 -m pip install -e .
918: drave --version            # drave 0.1.0
919: cd /tmp && drave analyser "Le chat dort."
920: ```
921: 
922: L'installation est **éditable** : le paquet `drave` (version **0.1.0**, `requires-python >= 3.10`,
923: **zéro dépendance**) pointe vers le dépôt ; le script console appelle `tools.drave:main`.
924: Elle fonctionne **depuis n'importe quel répertoire** (`cd /tmp`). Sans installation, `drave`
925: n'existe pas : la commande échoue avec `
… [1874 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "### 8.10 Comment l'installer et le lancer ?\n\nTrois chemins, le même CLI. **Depuis le dépôt, sans rien installer** : `python3 tools/drave.py …`\ndepuis la racine (Python **3.10+**, mesuré ici en 3 … [3495 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_produit.py 2>&1 | tail -8", "description": "Run product smoke tests", "timeoutMs": 300000}`

  ```
..............................
----------------------------------------------------------------------
Ran 30 tests in 17.042s

OK
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/tests/test_restitution.py 2>&1 | tail -5; python3 tools/tests/test_restitution_v2.py 2>&1 | tail -5; python3 tools/tests/test_restitution_v3.py 2>&1 | tail -5", "description": "Run restitution tests", "timeoutMs": 30000 … [2 caractères tronqués]`

  ```
----------------------------------------------------------------------
Ran 22 tests in 16.380s

OK

----------------------------------------------------------------------
Ran 17 tests in 1.395s

OK

----------------------------------------------------------------------
Ran 29 tests in 2.595s

OK
  ```

- **bash** `{"command": "set -e\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ntest -f tools/tests/linguistique/gold_reel_50.py && cp -p tools/tests/linguistique/gold_reel_50.py /tmp/gold_reel_50.py.sauve\nrm -f tools/tests/linguistique/gold_reel_50.py\nrm -rf dist && mkdir -p dist\npython3 -m pip wheel . … [913 caractères tronqués]`

  ```
build code=0
Building wheels for collected packages: drave
  Building wheel for drave (pyproject.toml): started
  Building wheel for drave (pyproject.toml): finished with status 'done'
  Created wheel for drave: filename=drave-0.1.0-py3-none-any.whl size=1735736 sha256=0d38bc2cddd47380992d59afeef2e6d8abdefb16a44942f78227195bea802cd0
  Stored in directory: /tmp/pip-ephem-wheel-cache-qj4duffe/wheels/96/02/a3/318108f401dc37bb3a575e67c80cf111852262a4b3c9f691ec
Successfully built drave
total 1696
-rw-r--r--. 1 stephane stephane 1735736 16 nov 00:38 drave-0.1.0-py3-none-any.whl
0d38bc2cddd47380992d59afeef2e6d8abdefb16a44942f78227195bea802cd0  dist/drave-0.1.0-py3-none-any.whl
entrees 423
gold json ['tools/tests/linguistique/gold.json', 'tools/tests/linguistique/gold_gele.json', 'tools/tests/linguistique/gold_reel.json', 'tools/tests/linguistique/gold_restitution_v2.json', 'tools/tests/linguistique/gold_synthetique.json']
gold_reel_50 True
structures generateur True
llm deepseek True
-rw-r--r--. 1 stephane stephane 29924 15 nov 02:45 tools/tests/linguistique/gold_reel_50.py
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -d build *.egg-info 2>/dev/null; find build -name 'gold_reel_50.py' 2>/dev/null | head; find . -maxdepth 2 -name '*.egg-info' -type d", "description": "Check build cache"}`

  ```
build
drave.egg-info
build/lib/tools/tests/linguistique/gold_reel_50.py
./drave.egg-info
  ```

- **bash** `{"command": "set -e\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nrm -rf build drave.egg-info dist\nmkdir -p dist\ncp -p tools/tests/linguistique/gold_reel_50.py /tmp/gold_reel_50.py.sauve\nrm -f tools/tests/linguistique/gold_reel_50.py\npython3 -m pip wheel . --no-deps --no-build-isolation - … [782 caractères tronqués]`

  ```
build code=0
Building wheels for collected packages: drave
  Building wheel for drave (pyproject.toml): started
  Building wheel for drave (pyproject.toml): finished with status 'done'
  Created wheel for drave: filename=drave-0.1.0-py3-none-any.whl size=1727201 sha256=d980c4706f575e061faa9611aca4c42c024c1147b654004f724694914a99dbce
  Stored in directory: /tmp/pip-ephem-wheel-cache-k672t_ag/wheels/96/02/a3/318108f401dc37bb3a575e67c80cf111852262a4b3c9f691ec
Successfully built drave
d980c4706f575e061faa9611aca4c42c024c1147b654004f724694914a99dbce  dist/drave-0.1.0-py3-none-any.whl
entrees 422
gold json ['tools/tests/linguistique/gold.json', 'tools/tests/linguistique/gold_gele.json', 'tools/tests/linguistique/gold_reel.json', 'tools/tests/linguistique/gold_restitution_v2.json', 'tools/tests/linguistique/gold_synthetique.json']
gold_reel_50 False
structures generateur True
llm deepseek True
  ```

- **bash** `{"command": "set -u\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nrm -rf /tmp/venv-drave-roue /tmp/drave-home /tmp/drave-sorties-final && mkdir -p /tmp/drave-home /tmp/drave-sorties-final\npython3 -m venv /tmp/venv-drave-roue\n/tmp/venv-drave-roue/bin/python -m pip install --no-index --no-dep … [1874 caractères tronqués]`

  ```
install=0
version=0
analyser=0
analyser_en=0
analyser_json=0
evaluer_json=0
evaluer_gele=0
evaluer_reel=0
restituer=0
tagger_sans_cle=4
--- version
drave 0.1.0
--- evaluer gold
0.1.0 612 3179 239
--- gele
{'nom': 'gelé (référence figée)', 'gele': True, 'phrases': 602, 'tokens': 3141, 'cibles_attachement': 239}
--- reel
{'nom': 'réel (hand + reel, sans synthétique)', 'gele': False, 'phrases': 452, 'tokens': 2480, 'cibles_attachement': 184}
--- tagger
drave: dépendance absente : clé DeepSeek absente : exportez DEEPSEEK_KEY_FILE, déposez la clé dans ~/.config/drave/deepseek.key, ou exportez DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.
--- restituer
fidélité    : exacte 1.0000 · caractères 1.0000 · couverture 100.00%
mots        : exacte 0.0000 · caractères 0.9286 · couverture 84.62%
pos         : exacte 0.0000 · caractères 0.9286 · couverture 84.62%
miroir      : 0.0000 (non exact) — minimum des fidélités binaires de la surface (graphème), des mots et des POS ; une sortie n'est fidèle que si elle reproduit exactement la source
contrôle négatif : mélange exacte 0.0000 (caractères 0.3077) · troncature exacte 0.0000 (caractères 0.9231)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 tools/drave.py analyser \"Le chat dort.\" --json > /tmp/drave-sorties-final/repo-analyser.json\npython3 tools/drave.py evaluer --json > /tmp/drave-sorties-final/repo-evaluer.json\npython3 tools/drave.py evaluer --gold --json >  … [434 caractères tronqués]`

  ```
analyser_json vs repo-analyser -> 0
evaluer_json vs repo-evaluer -> 0
evaluer_gele vs repo-evaluer-gele -> 0
586830dfcd3120a49c8481b1a6c8afe125f11e28b898ac2f76e7b72580c90c36  /tmp/drave-sorties-final/analyser_json.out
586830dfcd3120a49c8481b1a6c8afe125f11e28b898ac2f76e7b72580c90c36  /tmp/drave-sorties-final/repo-analyser.json
  ```

- **bash** `{"command": "set -u\ncd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nrm -rf /tmp/drave-amputee /tmp/venv-drave-roue-amputee\nmkdir -p /tmp/drave-amputee\npython3 - <<'PY'\nimport zipfile, pathlib\nsrc = pathlib.Path('dist/drave-0.1.0-py3-none-any.whl')\ndst = pathlib.Path('/tmp/drave-amputee/dra … [2080 caractères tronqués]`

  ```
1625372
install=0
amputee-version=0
amputee-analyser=0
amputee-evaluer=4
amputee-evaluer_gele=4
--- stderr evaluer
drave: dépendance absente : gold absent de cette installation : gold.json, gold_reel.json, gold_synthetique.json (attendu dans /tmp/venv-drave-roue-amputee/lib/python3.13/site-packages/tools/tests/linguistique). La roue doit contenir les gold ; réinstallez la roue complète, ou mesurez depuis le dépôt avec `python3 tools/drave.py evaluer`. Le drapeau `--gold` sélectionne le gold gelé (`gold_gele.json`) s'il est présent ; il ne remplace pas un gold absent.
--- stdout bytes
0
--- stderr gele
drave: dépendance absente : gold absent de cette installation : gold_gele.json (attendu dans /tmp/venv-drave-roue-amputee/lib/python3.13/site-packages/tools/tests/linguistique). La roue doit contenir les gold ; réinstallez la roue complète, ou mesurez depuis le dépôt avec `python3 tools/drave.py evaluer`. Le drapeau `--gold` sélectionne le gold gelé (`gold_gele.json`) s'il est présent ; il ne remplace pas un gold absent.
--- analyser compare to full wheel
cmp=0
969ccd335beb11cfcee99efd434486849007089bb79f4ba712e4ae2e8948f76a  /tmp/drave-amputee/drave-0.1.0-py3-none-any.whl
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\n/tmp/venv-drave-roue/bin/python --version; /tmp/venv-drave-roue/bin/python -m pip --version; python3 -c 'import setuptools,sys;print(\"setuptools\",setuptools.__version__)'\necho '--- pip show'; cat /tmp/drave-sorties-final/pip-show.tx … [534 caractères tronqués]`

  ```
Python 3.13.16
pip 26.2.1 from /tmp/venv-drave-roue/lib64/python3.13/site-packages/pip (python 3.13)
setuptools 84.0.0
--- pip show
Name: drave
Version: 0.1.0
Summary: Le point d'entrée produit du bloc linguistique de Drave.
Home-page: 
Author: 
Author-email: 
License: 
Location: /tmp/venv-drave-roue/lib64/python3.13/site-packages
Requires: 
Required-by: 
--- metadata
Metadata-Version: 2.4
Name: drave
Version: 0.1.0
Summary: Le point d'entrée produit du bloc linguistique de Drave.
Requires-Python: >=3.10
--- wheel size
1727201
--- stripped size
1625372
--- json hashes
586830dfcd3120a49c8481b1a6c8afe125f11e28b898ac2f76e7b72580c90c36  /tmp/drave-sorties-final/analyser_json.out
7e8ed1b902cd07cc9ffb28c4eb0776ec250d7537d73e4d80f0b8ebe693209ed6  /tmp/drave-sorties-final/evaluer_json.out
04e363b7a46f575f0faf59fb11ed827582f2a22d298033cd286abed13d01629d  /tmp/drave-sorties-final/evaluer_gele.out
9e582febe5bdbfd36fe8d079896f7a3be9242c1cf6c581d0841c822f680cc16a  /tmp/drave-sorties-final/evaluer_reel.out
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json\nfor n in ('evaluer_json','evaluer_gele','evaluer_reel'):\n    d=json.load(open(f'/tmp/drave-sorties-final/{n}.out'))\n    print(n, json.dumps({'version':d['version'],'gold':d['gold'],'pos':d['heuristique' … [600 caractères tronqués]`

  ```
evaluer_json {"version": "0.1.0", "gold": {"nom": "vivant (hand + reel + synthétique)", "gele": false, "phrases": 612, "tokens": 3179, "cibles_attachement": 239}, "pos": 0.8625, "f1": 0.7902, "att_exact": 0.9958, "controle": {"nom": "cible exacte tirée au hasard dans le gold", "graine": 0, "cibles": 239, "exact_taux": 0.0167}}
evaluer_gele {"version": "0.1.0", "gold": {"nom": "gelé (référence figée)", "gele": true, "phrases": 602, "tokens": 3141, "cibles_attachement": 239}, "pos": 0.8625, "f1": 0.7882, "att_exact": 0.9791, "controle": {"nom": "cible exacte tirée au hasard dans le gold", "graine": 0, "cibles": 239, "exact_taux": 0.0167}}
evaluer_reel {"version": "0.1.0", "gold": {"nom": "réel (hand + reel, sans synthétique)", "gele": false, "phrases": 452, "tokens": 2480, "cibles_attachement": 184}, "pos": 0.8891, "f1": 0.7906, "att_exact": 0.9946, "controle": {"nom": "cible exacte tirée au hasard dans le gold", "graine": 0, "cibles": 184, "exact_taux": 0.0}}
--- analyser output bytes
593 /tmp/drave-sorties-final/analyser.out
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DE
… [500 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md", "limit": 30, "offset": 45}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md</path>
<type>file</type>
<content>
45:   module que `python3 tools/drave.py`.
46: - **Aucune dépendance d'exécution** (`dependencies = []`). `setuptools>=61` est une dépendance
47:   de **construction**, installée par pip en isolation de build, pas au runtime.
48: - **Le code historique n'est pas modifié** : `tools/drave.py` continue de calculer sa racine
49:   depuis `__file__`, d'ajouter `tools/` à `sys.path` et de fonctionner lancé directement.
50: - **Les artefacts d'installation** sont ignorés (`*.egg-info/`, `/build/`, `/dist/` dans
51:   [`.gitignore`](../.gitignore)).
52: - **Le test** [`tools/tests/test_empaquetage.py`](../tools/tests/test_empaquetage.py) vérifie
53:   les métadonnées, les deux entrées et le contrôle négatif, sans créer de venv ni télécharger.
54: - **La doc** [`docs/produit/README.md`](../docs/produit/README.md) § 8.10 porte désormais les
55:   deux chemins d'installation (historique et `drave`).
56: 
57: **Ce qui n'est pas livré.** Aucune **wheel** n'est livrée ni publiée sur PyPI ; l'installation
58: est **éditable** et pointe vers le dépôt. Un wheel non éditable, const
… [651 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md", "new_string": "**Ce qui n'est pas livré.** Aucune **wheel** n'est livrée ni publiée sur PyPI ; l'installation\nest **éditable** et pointe vers le dépôt. Un wheel non éditable, construit à part pour vérifi … [1210 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empaquetage.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json, pathlib, hashlib\n\nwheel = pathlib.Path('dist/drave-0.1.0-py3-none-any.whl')\namputee = pathlib.Path('/tmp/drave-amputee/drave-0.1.0-py3-none-any.whl')\ndef sha(p): return hashlib.sha256(p.read_bytes()). … [10550 caractères tronqués]`

  ```
written reports/roue.json 9314
JSON-OK
{
 "schema": "drave.roue.verification",
 "version": 1,
 "date": "2026-11-16",
 "tache": "U2 (la roue)",
 "ligne_roadmap": "B13",
 "produit": "0.1.0",
 "head_mesure": "04894aea",
 "decision": {
  "gold_dans_la_roue": true,
  "roue_sans_gold_doit_echouer": true,
  "pourquoi": "Une roue installable doit pouvoir mesurer : les cinq gold sont donc des données du paquet. Une roue amputée ne peut pas inventer une référence : evaluer échoue en 4, sans stdout, avec un message qui nomme les fichiers manquants et les deux issues (réinstaller la roue complète, ou mesurer depuis le dépôt). --gold sélectionne le gold gelé, il ne remplace pas un gold absent.",
  "gold": [
   "gold.json",
   "gold_gele.json",
   "gold_reel.json",
   "gold_restitution_v2.json",
   "gold_synthetique.json"
  ],
  "code_si_gold_absent": 4,
  "option_gold": "--gold mesure gold_gele.json (602 phrases) ; son aide et le message d'erreur disent qu'il ne remplace pas un gold absent."
 },
 "pyproject": {
  "fichier": "pyproject.toml",
  "nom": "drave",
  "version": "0.1.0",
  "requires_python": ">=3.10",
  "dependances": [],
  "script_console": "drave = tools.drave:main",
  "build_backen
… [197 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ncat > reports/rapport-roue.md <<'MD'\n# U2 — la roue : `drave-0.1.0-py3-none-any.whl`, installée hors du dépôt, les gold dedans\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **U2** (suite de T1) ·\n> **Date** : 2026-11-16 … [11103 caractères tronqués]`

  ```
174 reports/rapport-roue.md
# U2 — la roue : `drave-0.1.0-py3-none-any.whl`, installée hors du dépôt, les gold dedans

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **U2** (suite de T1) ·
> **Date** : 2026-11-16 · **Verdict** : ✅ **la roue est autonome ; une roue sans gold échoue proprement**.
>
> **Le chiffre.** `python3 -m pip wheel . --no-deps --no-build-isolation -w dist` rend
> **`drave-0.1.0-py3-none-any.whl`** : **1 727 201 octets**, **422 entrées**,
> sha256 `d980c4706f575e061faa9611aca4c42c024c1147b654004f724694914a99dbce`. Installée
> dans un venv **propre** depuis la roue (pas le dépôt), elle rend `drave 0.1.0` (code 0),
> `drave analyser "Le chat dort."` (code 0, `rôle=agent`) et `drave evaluer --json` (code 0,
> gold **612** phrases, POS **0,8625**, F1 **0,7902**, attachement exact **0,9958**) depuis
> **`/tmp`**. Les JSON `analyser` et `evaluer` sont **identiques au bit près** à ceux du dépôt.
> **Contrôle négatif** : la même roue **amputée des cinq `gold*.json`** s'installe encore et
> analyse encore, mais `drave evaluer` sort en **4**, `stdout` vide, et nomme les fichiers
> manquants. La mesure ne ment pas : sans référence, elle refuse.
>
> **Dispositif**
… [253 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -60", "description": "Run documentation review", "timeoutMs": 180000}`

  ```
revue de documentation · 767 fiche(s) · 862 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 766 fichiers, le disque en a 767
     · compteurs : en-cours.md dit 861 JSON, le disque en a 862
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 10, "offset": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-16, 00 h 30 HNE (U1 : les deux O(k²) bornés, α 1,08)**
4: 
5: > **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).
6: 
7: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*
8: 
9: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
10: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.

(Showing lines 1-10 of 145. Use offset=11 to continue.)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 18, "offset": 57}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
57: - **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
58: - **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
59: - **Plan** : B13 · **Stratégie** : v0 · **Ambition** : tracé · **Objectif final** : moteur v0.
60: - **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.
61: - **Ce que font les autres** : N2.
62: - **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** (`d19f0fc7` ; [fiche](../../reports/rapport-performance-fix.md), [JSON](../../reports/performance-fix.json)).
63: - **Prochaine action** : **U2 — la roue** ; **U3 — `--profils`** ; **J4** ; T132/T133.
64: - **Bloquants** : 7B locales interdites (règle 11) ; **gold de pensée**.
65: - **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).
66: 
67: ### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2 : la production et la capacité *(en pause)*
68: 
69: - **Id** : `0733c5bb-f90b-
… [413 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-16, 00 h 45 HNE (U2 : la roue, les gold dedans, la roue sans gold échoue)**", "old_string": "**Mis à jour : 2026-11-16, 00 h 30 HNE (U1 : les deux O(k²) bornés, α 1,08)**" … [1 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** (`d19f0fc7` ; [fiche](../../reports/rapport-performance-fix. … [694 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 28, "offset": 92}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
92: 
93: ## Les chiffres de l'état
94: 
95: > Vérifié par `tools/revue_documentation.py`.
96: 
97: | invariant | valeur | contrôle |
98: |---|---|---|
99: | portes | **86** (dont `porte-banc-performance` le 15/11) | `tools/porte-*.sh` |
100: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
101: | fichiers / JSON de résultats | **766** / **861** | `reports/*.md` / `reports/*.json` |
102: | documents de `docs/` | **125** (hors archive et README) | `docs/**/*.md` |
103: | dernière passe | **15/11 09 h 53 → 12 h 15** (85, **81/4**) ; rouges `indice`, `melange` (structurelles), `sessions` (**réparée** à 12 h 20), `prechargement` (**environnementale**) ; ciblage W6 **9/9** ; **86e porte** verte | `work/portes-1115-09h53/registre.txt` ; `work/portes/w6-final/` |
104: 
105: ## Les chantiers et leurs bloquants
106: 
107: **Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
108: externes** et la **prochaine action**.
109: 
110: | chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
111: |---|---
… [2095 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 14, "offset": 79}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
79: - **Journal** : [la session](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/).
80: 
81: ## Ce qui est en cours
82: 
83: - **S — les structures** : 61/61 types, 144/144 rôles ; **19/19 verdicts `389b99f`** ; [v2](../../reports/rapport-coordination-s-v2.md).
84: - **N2 — en pause** : commande **`eval_longueurs.py --rope --val <dir>`** (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
85: - **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports/rapport-restitution-v2.md), [v3](../../reports/rapport-restitution-v3.md).
86: - **L — le bloc langue** : contrat ; frontière script 1,0 / langue 0,137/0,9687 ; fusion réparée **0,9309/0,8226/0,8784/0,9954**.
87: - **W2/W3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; défaut **code 0 / 0 socket** ; `--tagger` **code 4** sans clé ; réseau coupé **code 0** + repli ; [W2](../../reports
… [1083 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 12, "offset": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
120: 
121: ## Ce qui reste
122: 
123: **T1–T6 — livré** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s, instrument 0,71/2,11) ; reste **U2** (la roue), **U3** (`--profils`) ; [bilan](../../reports/rapport-bilan-exploitable.md), [U1](../../reports/rapport-performance-fix.md).
124: 
125: **Pensée** — `g017`, T132/T133, gold de pensée ; **J4 — l'or de rôles** (seconds cadres). **Le gold de S** (61 phrases/144 rôles) n'est pas un or humain indépendant ; **S** — page `/` : décision et recette (106/41), **12/28** référents faux.
126: 
127: **Panini** — **26 signatures V14** manquantes, calibration **42/44**, rejeu **27/60** : le test attend ; **R0.7** — `--tagger auto` prototype livré (**opt-in**, défaut hors ligne inchangé), **décision humaine** ; **N2** — porte (0,2856/0,3566) ; **A** — A6.2, A8.3b2.
128: 
129: ## Les questions ouvertes
130: 
131: - **R1** : **1 024 octets** ? → **R1.2** (3,0107 à octets constants).

(Showing lines 120-131 of 145. Use offset=132 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; **U2 — la roue** (autonome, gold dedans, roue sans gold → … [388 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **767** / **862** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **766** / **861** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6 ; U1 : α 1,08, 10 000 mots 0,82 s ; U2 : ro … [511 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**T1–T6 — livré** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s, instrument 0,71/2,11) ; **U2 — la roue** (1 727 201 o, autonome, gold dedans, roue sans gold → 4) ; reste **U3** ( … [423 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 14, "offset": 164}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
164: [Fiche](../../reports/rapport-performance.md) · [JSON](../../reports/performance.json).
165: 
166: **U1 — les deux O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),
167: **12 259 mots/s**, **127,4 Mio** ; JSON identique. **α = 1,076** (1,530 avant), le
168: quadratique n'ajoute que **+0,00077 de R²** ; sorties identiques (612/452, diff vide).
169: `_groupes_partition`, `_cible_proche`, `_sujet_hors_gv` et deux boucles du générateur S sont
170: corrigés. [Fiche](../../reports/rapport-performance-fix.md) · [JSON](../../reports/performance-fix.json) ·
171: [contrôle](../../tools/verifier_performance_fix.py). **Prochaine action : U2 — la roue, U3 — `--profils`.**
172: 
173: **T6 — le bilan exploitable (15/11, 23 h 35).** Cinq briques : installation éditable,
174: quickstart 3/3, API (2 139 objets, 8 rôles), performance (10 000 mots 4,01 s, 126 Mio), CLI
175: 20/20. Trois limites : clone public 88,70 % d'attachement au lieu de 99,58 %, O(k²) (α = 1,55),
176: gold de S non humain. [Fiche](../../reports/rapport-bilan-exploitable.md) ·
177: [JSON](../../repor
… [160 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"U1 — les deux\\|U1 : α\\|U2\" docs/pilotage/roadmap.md | head -20", "description": "Find U1/U2 mentions in roadmap"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [2261 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "[contrôle](../../tools/verifier_performance_fix.py). **U2 livré** ; prochaine action : **U3 — `--profils`**.\n\n**U2 — la roue (16/11).** `drave-0.1.0-py3-none-any.whl` : **1 727 201 octets**, ** … [715 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**U1 — les deux O(k²) bornés** (α **1,08**, 10 000 mots **0,82 s**, sorties identiques, [fiche](../../reports/rapport-performance-fix.md)) ; **U2 — la roue autonome** (**1 727 201 o**, 422 entrée … [256 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "limit": 25, "offset": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md</path>
<type>file</type>
<content>
1: # Plan de session — Pensée, la RSN plurielle et le moteur N3
2: 
3: > **Mandat vivant.** Ouvert le 2026-10-31 22 h 45 HAE depuis
4: > [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md). Ce plan est le **contrat de
5: > synergie** : il dit ce que la session réserve, ce qu'elle attend des autres, et quand elle s'arrête.
6: > Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.
7: 
8: - **Session** : `e181ce02-cd50-488a-a6be-e84b79d40dcc`
9: - **Rôle** : Pensée — RSN plurielle, arbre d'états, cycle multi-niveaux, moteur N3 ; analyse de la couche heuristique ; bloc linguistique
10: - **Périmètre** : Pensée, R4.4-reste, Coloration, Bloc linguistique (R0.7)
11: - **Fichiers réservés** : `docs/theorie/pensee-iterative.md`, `docs/schemas/pensee-*.svg`,
12:   `docs/implantation/moteur-de-pensee.md`, `tools/pensee/`, `reports/pensee-*`,
13:   `reports/r44-*`, `docs/theorie/pre-traitement-linguistique.md`,
14:   `docs/schemas/heuristique-*.svg`, `tools/bloc_linguistique.py`,
15:   `tools/porte-bloc-linguistique.
… [971 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "limit": 20, "offset": 25}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md</path>
<type>file</type>
<content>
25: - **Plan** : 1) ~~RSN plurielle, arbre d'états, cycle multi-niveaux~~ ; 2) ~~portefeuille de
26:   stratégies, contrat, anytime~~ ; 3) ~~state store v0 (6/6 portes T0–T4)~~ ; 4) ~~moteur v0
27:   (BFS, greedy, A*, MCTS-lite)~~ ; 5) ~~AC-3, alpha-bêta~~ (**8/8**) ; ~~DRVF~~ (**9/9**) ; 6) **banc anytime** (AUC,
28:   regret, justification, rejeu) et intégration DRVM/DRVF ; 9) ~~bloc linguistique~~ (R0.7, 398 langues) ; 10) ~~coréférence et absences~~ (140/140, gold 432) ; 11) ~~gold neuronal~~ (tagger 7B local, cascade POS 0,9440) ; 12) ~~syntagmes~~ (BIO 7B, exact 0,6173, tête 0,7606) ; 13) ~~cascade complète~~ (POS 0,9415, syntagmes 0,7539, acte 1,0) ; 14) ~~DRVM/native~~ (cadenas 3 nœuds avec règle, minimal 0 ; porte 27 nœuds avec règle) ; 15) ~~porte DRVM~~ (27 nœuds, 4 sonde) ; 16) ~~pragmatique neuronale~~ (négatif : dev 1,0, test 0,6375) ; 17) ~~porte B13~~ (134/140 : 6 S fixés + 2 test périmé ; le 140/140 ne se rejoue pas) ; 18) ~~porte minute~~ (26 nœuds, 4 sonde ; le labyrinthe échoue) ; 19) ~~porte mobile~~ (2/2 mais l'
… [1747 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "new_string": "- **Heartbeat** : 2026-11-16 00:45 EST\n- **Prochaine action** : **U3 — `--profils`** ; **U1** (α **1,08**, 10 000 mots **0,82 s**, sorties identiques ; [fich … [424 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "new_string": "20) ~~porte B13 138~~ (6 S fixés ; T132/T133 restent) ; 21) ~~U1~~ (les deux O(k²) bornés, α 1,08) ; 22) ~~U2~~ (la roue : `drave-0.1.0-py3-none-any.whl`, mêm … [124 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/index_reports.py >/tmp/index.log 2>&1; echo \"code=$?\"; tail -5 /tmp/index.log; git diff --stat reports/INDEX.md; git diff reports/INDEX.md | head -40", "description": "Regenerate reports index"}`

  ```
code=0
  764 fiches → reports/INDEX.md
 reports/INDEX.md | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
diff --git a/reports/INDEX.md b/reports/INDEX.md
index c76c747a..7035466f 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **763 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **764 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -710,6 +710,7 @@
 | [rapport-reutilisation-experts.md](rapport-reutilisation-experts.md) | La réutilisation des experts, mesurée |
 | [rapport-robustesse-produit.md](rapport-robustesse-produit.md) | B13 — la robustesse du produit : un surrogate ne plante plus, une entrée non-str est refusée |
 | [rapport-robustesse-semaine.md](rapport-robustesse-semaine.md) | J11.3 — les 50 textes libres : 0 plantage, 50/50 au schéma v2, 115 chevauchements en `alternative`, 0 en `filtrer` |
+| [rapport-roue.md](rapport-roue.md) | U2 — la roue : `drave-0.1.0-py3-none-any.whl`, installée hors du dépôt, les gold dedans |
… [398 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py 2>&1 | tail -30", "description": "Run doc review again", "timeoutMs": 180000}`

  ```
revue de documentation · 767 fiche(s) · 862 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -20", "description": "Check document budgets", "timeoutMs": 120000}`

  ```
2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2773    232   T1   2800  reports/README.md
    2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4068 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/
… [110 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo '--- journal'; python3 tools/verifie_journal.py 2>&1 | tail -20; echo '--- schemas'; python3 tools/verifier_schemas.py 2>&1 | tail -10", "description": "Run state, journal, sche … [32 caractères tronqués]`

  ```
en-cours · 1698 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
--- journal
  journal · 48 jour(s) · 223 session(s) · 2701 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
--- schemas
  schémas · 465 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport subprocess,re\nfor label,text in [('HEAD',subprocess.check_output(['git','show','HEAD:docs/pilotage/roadmap.md'],text=True)),('WORK',open('docs/pilotage/roadmap.md').read())]:\n    print(label, len(text.split … [61 caractères tronqués]`

  ```
HEAD 9326
WORK 9433
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 22, "offset": 164}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
164: [Fiche](../../reports/rapport-performance.md) · [JSON](../../reports/performance.json).
165: 
166: **U1 — les deux O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),
167: **12 259 mots/s**, **127,4 Mio** ; JSON identique. **α = 1,076** (1,530 avant), le
168: quadratique n'ajoute que **+0,00077 de R²** ; sorties identiques (612/452, diff vide).
169: `_groupes_partition`, `_cible_proche`, `_sujet_hors_gv` et deux boucles du générateur S sont
170: corrigés. [Fiche](../../reports/rapport-performance-fix.md) · [JSON](../../reports/performance-fix.json) ·
171: [contrôle](../../tools/verifier_performance_fix.py). **U2 livré** ; prochaine action : **U3 — `--profils`**.
172: 
173: **U2 — la roue (16/11).** `drave-0.1.0-py3-none-any.whl` : **1 727 201 octets**, **422 entrées**,
174: sha256 `d980c470…a99dbce` ; installée dans un venv propre **depuis la roue**, `drave --version` et
175: `drave analyser` depuis `/tmp`, JSON **identiques** au dépôt. La roue embarque les **cinq gold**
176: (`package-data`), `tools.structures/generateur.py` et `tools.llm`. **Contrôle 
… [868 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**U1 — les deux O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),\n**12 259 mots/s**, **127,4 Mio** ; JSON identique. **α = 1,076** (1,530 avant), +0,00077 de R²\nseulement ; sortie … [1625 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**U1 — les deux O(k²) bornés** (α **1,08**, 10 000 mots **0,82 s**, sorties identiques, [fiche](../../reports/rapport-performance-fix.md)) |", "old_string": "**U1 — les deux O(k²) bornés** (α **1 … [256 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -6; python3 - <<'PY'\nimport subprocess\nprint('raw HEAD',len(subprocess.check_output(['git','show','HEAD:docs/pilotage/roadmap.md'],text=True).split()))\nprint('raw WORK',len(open('docs/ … [106 caractères tronqués]`

  ```
avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9002 mots > budget 9000 (T1)
     · T0 : 4068 mots (AGENTS + en-cours + une tâche) > budget 4 000
raw HEAD 9326
raw WORK 9328
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"T0\\|4000\\|AGENTS\\|en-cours\\|tache\" tools/taille_documents.py | head -60", "description": "Inspect T0 budget logic"}`

  ```
5:  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
27:    ("T0", "AGENTS.md", 1200),
28:    ("T0", "docs/pilotage/en-cours.md", 2000),
32:    ("T0", "docs/methode/*.md", 1200),
112:            if cat in ("T0", "T1"):
140:    # T0 : la somme des trois lectures par défaut
145:    # Le T0 est « AGENTS + en-cours + UN document de tâche », et le document de tâche est un
146:    # T0 (≤ 1 200 mots) : les trois documents `specifiques` ci-dessus sont des T1, avec leur
147:    # propre budget. Les compter ici faisait payer 1 579 mots au T0 (organisation-du-depot.md)
148:    # au lieu des 1 134 du plus gros T0 — un budget faux de 445 mots, dans le sens qui bloque.
150:    t0 = poids("AGENTS.md") + poids("docs/pilotage/en-cours.md") + max(
153:    if t0 > 4000:
154:        violations.append(f"T0 : {t0} mots (AGENTS + en-cours + une tâche) > budget 4 000")
163:    print(f"  T0 max : {t0} mots (budget 4 000)")
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -w AGENTS.md docs/pilotage/en-cours.md; python3 - <<'PY'\nimport re, pathlib\nt=pathlib.Path('docs/pilotage/en-cours.md').read_text()\n# print blocks with word counts\nfor i,block in enumerate(t.split('\\n\\n')):\n    n=len(block. … [113 caractères tronqués]`

  ```
1196 AGENTS.md
 1698 docs/pilotage/en-cours.md
 2894 total
4 62 - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/se
6 66 > Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
8 84 - **Id** : `536cd5d6-94ac-4057-8fe9-11709a4587c7` — [`plan.md`](../../journal/se
10 118 - **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/se
12 139 - **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/se
14 118 - **Id** : `0733c5bb-f90b-4f58-9241-3364fa32e46c` — [`plan.md`](../../journal/se
16 208 - **S — les structures** : 61/61 types, 144/144 rôles ; **19/19 verdicts `389b99
19 97 | invariant | valeur | contrôle |
22 337 | chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
25 44 **T1–T6 — livré** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s, 
26 41 **Pensée** — `g017`, T132/T133, gold de pensée ; **J4 — l'or de rôles** (seconds
27 38 **Panini** — **26 signatures V14** manquantes, calibration **42/44**, rejeu **27
29 149 - **R1** : **1 024 octets** ? → **R1.2** (3,0107 à octets constants).
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '55,80p' docs/pilotage/en-cours.md; echo '--- questions'; sed -n '127,145p' docs/pilotage/en-cours.md", "description": "Read en-cours blocks to trim"}`

  ```
### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif)*

- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
- **Rôle** : **Pensée** — RSN, arbre d'états, N3 ; heuristique ; bloc linguistique.
- **Plan** : B13 · **Stratégie** : v0 · **Ambition** : tracé · **Objectif final** : moteur v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.
- **Ce que font les autres** : N2.
- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** (`d19f0fc7` ; [fiche](../../reports/rapport-performance-fix.md), [JSON](../../reports/performance-fix.json)) ; **U2** la roue : `drave-0.1.0-py3-none-any.whl` **1 727 201 o**, installée hors dépôt, **mêmes JSON** que le dépôt, roue sans gold → `evaluer` **4** ([fiche](../../reports/rapport-roue.md), [JSON](../../reports/roue.json)).
- **Prochaine action** : **U3 — `--profils`** ; **J4** ; T132/T133.
- **Bloquants** : 7B locales interdites (règle 11) ; **gold de pensée**.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-
… [2512 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** ([fiche](../../reports/rapport-performance-fix.md)) ; **U2** … [608 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **N2** : **< 2,5** ? → **oui par la fenêtre** : 2,4759 / 2,4373 au grand corpus (1 024, 30 k pas) ; la porte **propre** reste à 2,7856.\n- **Pensée** : l'**absence** est-elle annotable ? → le  … [527 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **W2/W3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; défaut **code 0 / 0 socket** ; `--tagger` **code 4** sans clé ; [W2](../../reports/rapport-tagger-h5 … [352 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Panini B1** : **60 paires** ; **27/60**, calibration **42/44** ; [W4](../../reports/rapport-panini-manifeste.md), [B1](../../reports/rapport-protocole-date.md).", "old_string": "- **Panini B … [186 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**U1 — les O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),\n**12 259 mots/s**, **127,4 Mio** ; JSON identique. **α = 1,076** (1,530 avant), +0,00077 de R² ; sorties identiques (61 … [349 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -8; python3 tools/revue_documentation.py 2>&1 | tail -8; python3 tools/verifie_en_cours.py 2>&1 | tail -3", "description": "Recheck budgets and review", "timeoutMs": 180000}`

  ```
1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3993 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  revue de documentation · 767 fiche(s) · 862 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  en-cours · 1623 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh 2>&1 | tail -20; echo \"code=$?\"", "description": "Run table gate", "timeoutMs": 180000}`

  ```
✅ 1847 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4749 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-16)
code=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-produit.sh 2>&1 | tail -30; echo \"code=$?\"", "description": "Run product gate", "timeoutMs": 600000}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f6355d8175a75854 deux fois
  ✅ smoke test : Ran 30 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v2 : rôles lisibles, rendu relu, contrôle détecté
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
code=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' docs/methode/portes.md; echo '--- toutes'; sed -n '1,80p' tools/toutes-les-portes.sh", "description": "Read gates method and runner"}`

  ```
# Les portes : lancer, lire le verdict, ne pas se tromper de rouge

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant de lancer ou de lire les portes**.

## La commande

```bash
bash tools/toutes-les-portes.sh
```

Elle lance **toutes** les `tools/porte-*.sh`, séquentiellement, **sans s'arrêter à la première rouge** (on veut le
[tableau](../theorie/glossaire/entrees/tableau.md), pas la première tuile), et borne **chaque** [porte](../theorie/glossaire/entrees/porte.md) à `DELAI=1800` s. Durée observée d'une passe complète :
**1 h 30 – 2 h** sur Hauru (**83 portes** ; certaines entraînent de petits modèles, d'autres utilisent les [GPU](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md) ;
`porte-deepseek` est **hors réseau** et rapide). La dernière passe complète à **82 portes** (03/11 11 h 30, **machine au repos**, **1 h 48**) a donné
**80 vertes, 2 rouges** (les 2 connues : `indice`, `melange`) ;
`porte-reparti-moteur` (ré-étalonnée à 8,7434) et `porte-homeostasie` (auto-générée) sont **vertes** ;
la liste et le diagnostic sont dans
[`references-non-regression.md`](../pilotage/references-non-regression.md). `porte-deepseek` est **
… [7943 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/porte-*.sh | sed 's#tools/porte-##;s#\\.sh##' | tr '\\n' ' '; echo; grep -n \"rouge\\|tolér\" docs/pilotage/references-non-regression.md | head -20", "description": "List gate names and tolerated reds"}`

  ```
adaptateur-sortie audit-drapeaux b1110-hybride balayage banc-performance bloc-code bloc-linguistique bloc-maths bloc-tableaux budget bus bus-socket c4-retard cerveau cic consolidation coupe cycle-c2 deepseek delais diff-couche document echange-experts episodique etat flux fusion gain greffe harnais-invariants homeostasie horloge indice jeux jumeaux lecteur lecture m5-brouillon melange memoire miroir-blocs mistral n3-cache n3-composition n3-deux-processus n3-deux-regions n3-generation n3-inventaire n3-placement n3-pont n3-positions n3-profondeur n3-refus n3-reseau n3-routes n3-service-briques n3-service n3-seuil n3-sparsite-compte n3-sparsite occupation-elagage occupation-moteur ocr-scans ocr pannes peripherie poids-creux pont prechargement produit profondeur-routee push-paresseux r13-bpe recurrence reflexe registre reparti-moteur ressources sauvegarde-modele sessions speculatif tableaux tokenizer-kimi topologie trace vision 
3:> **Passe — 2026-11-15 09 h 53 → 12 h 15 :** **85 portes, 81 vertes, 4 rouges** — `indice` et
9:> **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
15:> heartbeat `e181ce02` rafraîchi) ; `porte-indice` et `porte-melange` 
… [736 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && JOURNAUX=work/portes/roue-1116 bash tools/toutes-les-portes.sh", "description": "Run full gates pass in background", "run_in_background": true}`

  ```
started background job bash-90
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short && echo '--- diff stat' && git diff --stat", "description": "Review working tree changes"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
 M pyproject.toml
 M reports/INDEX.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-empaquetage.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 M tools/drave.py
 M tools/tests/test_empaquetage.py
?? reports/rapport-roue.md
?? reports/rapport-s-paragraphes.md
?? reports/roue.json
?? tools/tests/linguistique/gold_reel_50.py
--- diff stat
 docs/pilotage/en-cours.md                          |  20 +-
 docs/pilotage/roadmap.md                           |  11 +-
 docs/produit/README.md                             |  50 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md   |   6 +-
 pyproject.toml                                     |  18 +-
 reports/INDEX.md                                   |   3 +-
 reports/pensee-coherence-fiches-v7.json            |  19 +
 reports/pensee-dev-test-v10.json       
… [705 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat journal/2026-11-16/README.md; echo '--- mesures'; cat journal/2026-11-16/mesures.md; echo '--- memoire'; cat journal/2026-11-16/memoire.md", "description": "Read today's journal files"}`

  ```
# 2026-11-16

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-16/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**2 commits** · **1 session(s)** · **2 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 1 | [mesures.md](mesures.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 367.7 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO |
| 00:24 | `75a56c05` | U1 — LA FICHE POINTE SES COM
… [2527 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff pyproject.toml tools/drave.py tools/tests/test_empaquetage.py | sed -n '1,260p'", "description": "Review code diff"}`

  ```
diff --git a/pyproject.toml b/pyproject.toml
index 3aea0ff4..1931828f 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -13,4 +13,20 @@ dependencies = []
 drave = "tools.drave:main"
 
 [tool.setuptools]
-packages = ["tools"]
+# Le paquet est un **namespace** (`tools/` n'a pas d'`__init__.py`) : on déclare les
+# sous-ensembles dont le CLI a besoin. `tools.tests` reste un namespace implicite
+# (son répertoire existe par `tools.tests.linguistique`) : on n'embarque pas les
+# scripts de test, seulement les modules et les gold de la mesure.
+packages = ["tools", "tools.llm", "tools.structures", "tools.tests.linguistique"]
+
+[tool.setuptools.package-data]
+# Les gold sont **dans la roue** : `drave evaluer` doit marcher hors du dépôt.
+# Le contrôle négatif (une roue amputée de ces fichiers) est décrit dans
+# reports/rapport-roue.md : `evaluer` échoue alors en code 4, sans trace.
+"tools.tests.linguistique" = [
+    "gold.json",
+    "gold_gele.json",
+    "gold_reel.json",
+    "gold_restitution_v2.json",
+    "gold_synthetique.json",
+]
diff --git a/tools/drave.py b/tools/drave.py
index 395d84b6..e5469d2f 100644
--- a/tools/drave.py
+++ b/tools/drave.py
@@ -115,6 +115,17 @@ class 
… [8873 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --check -- pyproject.toml tools/drave.py tools/tests/test_empaquetage.py docs/produit/README.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/rapport-roue.md reports/roue.json reports/rapport-empaquetage.md repo … [143 caractères tronqués]`

  ```
check=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit add pyproject.toml tools/drave.py tools/tests/test_empaquetage.py docs/produit/README.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/rapport-roue.md reports/roue.json reports/rapport-empaquetage.md reports/INDEX.md j … [1776 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  docs/produit/README.md
M  journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
M  pyproject.toml
M  reports/INDEX.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
M  reports/rapport-empaquetage.md
 M reports/rapport-pensee-v12.md
A  reports/rapport-roue.md
 M reports/rapport-spans-chunker.md
A  reports/roue.json
 M tools/chantier/plan.json
M  tools/drave.py
M  tools/tests/test_empaquetage.py
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
[stderr]
  ✅ index : aucun fait stagé sans état
[still running after 120000ms; moved to background job bash-95]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "sleep 5; echo done", "description": "Brief wait"}`

  ```
done
  ```

- **job_output** `{"job_id": "bash-95", "timeout_ms": 120000, "wait": true}`

  ```
[s/v7 c77ed4b6] U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE
 22 files changed, 4189 insertions(+), 76 deletions(-)
 create mode 100644 journal/sessions/session-aa260801-785c-4a85-876c-98ba023e6098/digest.md
 create mode 100644 journal/sessions/session-aa260801-785c-4a85-876c-98ba023e6098/rapport.md
 create mode 100644 reports/rapport-roue.md
 create mode 100644 reports/roue.json
c77ed4b6 U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline HEAD | sed -n '1,40p'; echo '--- status'; git status --short | sed -n '1,40p'", "description": "Inspect commit contents and status"}`

  ```
c77ed4b6 U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE
 docs/pilotage/en-cours.md                          |   20 +-
 docs/pilotage/roadmap.md                           |   11 +-
 docs/produit/README.md                             |   50 +-
 journal/2026-11-16/README.md                       |    7 +-
 journal/2026-11-16/memoire.md                      |    2 +-
 journal/2026-11-16/mesures.md                      |    5 +-
 journal/README.md                                  |    7 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   37 +
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md   |    6 +-
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 3158 ++++++++++++++++++++
 .../rapport.md                                     |  148 +
 .../digest.md                                      |  138 +
 .../rapport.md                                     |   63 +-
 pyproject.toml                                     |   18 +-
 reports/INDEX.md                                   |    3 +-

… [774 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,60p' journal/sessions/session-aa260801-785c-4a85-876c-98ba023e6098/rapport.md; echo '--- digest head'; sed -n '1,20p' journal/sessions/session-aa260801-785c-4a85-876c-98ba023e6098/digest.md; echo '--- manifest diff'; git sh … [109 caractères tronqués]`

  ```
# Session session- — Vérification roue Python et gold CLI

> **Journaux :** [le jour](../../2026-11-16/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `session-aa260801-785c-4a85-876c-98ba023e6098` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-16 00:31 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 133 |
| Appels d'outils | 149 |
| Fichiers touchés | 8 |
| Commandes | 96 |
| Sous-agents | 0 |
| Commits | 1 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tâche U2 (suite de T1) : **la roue** — `python3 -m build` (ou `pip wheel .`) produit `drave-0.1.0-py3-none-any.whl`, installée dans un venv **propre** depuis la roue (pas le dépôt) : `drave --version` et `drave analyser` depuis `/tmp` ; le **contrôle négatif** : la roue sans les gold doit-elle échouer (le CLI lit `tools/tests/linguistique/gold_*.json` — si les gold ne sont pas dans la roue, `evalu … [139 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tâche U2 (suite de T1) : **la roue** — `python3 -m build` (ou `pip wheel .`) produit `drave-0.1.0-py3-none
… [6916 caractères tronqués]
  ```

- **job_list** `{}`

  ```
bash-90 [bash] running — cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && JOURNAUX=work/portes/roue-1116 bash tools/toutes-les-portes.sh
bash-95 [bash] completed — cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
git add pyproject.toml tools/drave.py tools/tests/test_empaquetage.py docs/produit/README.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/rapport-roue.md reports/roue.json reports/rapport-empaquetage.md reports/INDEX.md journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
git status --short | sed -n '1,40p'
git commit -F - <<'MSG'
U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE

La roue est construite par `python3 -m pip wheel . --no-deps --no-build-isolation -w dist`
(`drave-0.1.0-py3-none-any.whl`, sha256 d980c470…a99dbce) et installée dans un venv propre
depuis le fichier, pas depuis le dépôt. Depuis `/tmp` : `drave --version` → `drave 0.1.0` (0),
`drave analyser "Le chat dort."` → `rôle=agent` (0), `drave evaluer --json` → gold 612,
POS 0,8625, F1 0,7902, exact 0,9958 (0). Les JSON `analyser`, `evaluer` et `evaluer --gold`
sont identiques au bit près à ceux du dépôt 
… [947 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -20 journal/2026-11-16/README.md; echo '--- mesures tail'; tail -12 journal/2026-11-16/mesures.md", "description": "Inspect journal notes blocks"}`

  ```
## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 368.1 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO |
| 00:24 | `75a56c05` | U1 — LA FICHE POINTE SES COMMITS : AVANT 83ADAA2B, APRÈS D19F0FC7 (SOUS-MODULE 648ADCE) |
| 00:28 | `04894aea` | U1 — LE CONTRÔLE DE L'INSTRUMENT EST CELUI DE LA PASSE : LINÉAIRE 0,71, QUADRATIQUE 2,11 (ET NON LES VALEURS DE T4) |

## Le récit de la journée (écrit à la main)

<!-- notes -->

<!-- /notes -->
--- mesures tail
## Sessions actives ce jour

- `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Documentation Drave avec diagrammes et implémentation (début 2026-10-31 17:40, 368.1 h) → [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/r
… [273 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/journal_auto.py --jour 2026-11-16 2>&1 | tail -10; git status --short | sed -n '1,30p'", "description": "Regenerate journal after commit", "timeoutMs": 180000}`

  ```
2026-11-16 : 4 commits
  journal/2026-11-16/memoire.md
  journal/2026-11-16/mesures.md
  journal/2026-11-16/README.md
  journal/THEMES.md
4 fichiers écrits · 4 commits classés
 M journal/2026-11-16/README.md
 M journal/2026-11-16/mesures.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md", "limit": 12, "offset": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md</path>
<type>file</type>
<content>
30: | 00:45 | `c77ed4b6` | U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE |
31: 
32: ## Le récit de la journée (écrit à la main)
33: 
34: <!-- notes -->
35: 
36: <!-- /notes -->

(End of file - total 36 lines)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md", "new_string": "<!-- notes -->\n\n### U2 — la roue autonome, et la roue sans gold qui refuse de mesurer\n\n`python3 -m pip wheel . --no-deps --no-build-isolation -w dist` a rendu\n**`drave-0.1.0-py3-none-any … [1060 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat journal/2026-11-16 journal/THEMES.md; git diff journal/THEMES.md | head -30", "description": "Inspect journal diffs"}`

  ```
journal/2026-11-16/README.md  | 22 ++++++++++++++++++++--
 journal/2026-11-16/mesures.md |  5 ++++-
 2 files changed, 24 insertions(+), 3 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\ngit add journal/2026-11-16/README.md journal/2026-11-16/mesures.md\ngit commit -F - <<'MSG'\nJOURNAL — 2026-11-16 : U2, LA ROUE AUTONOME ET LA ROUE SANS GOLD QUI SORT EN 4\n\nLe récit de la journée ajoute U2 : la roue installée hors dé … [394 caractères tronqués]`
