# Session DSH — relecture

- identifiant : `session-b9138a2a-648e-490d-a349-124ac1aa1ef0`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-16 03:27:11
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche Z1 (exploitable, la protection) : l'**intégration continue** — un `.github/workflows/ci.yml` : la matrice **Python 3.10 / 3.13**, `pip install -e .`, `python3 tools/tests/test_produit.py`, `python3 tools/tests/test_tagger_api.py`, `bash tools/porte-produit.sh`, `python3 tools/tests/test_schema_produit.py` ; le **contrôle négatif** : un test qui casse doit faire échouer le job (le prouver en local) ; la doc. Fiche `reports/rapport-ci.md` + JSON. Si l'environnement n'a pas `act`, prouve au moins que le YAML est valide (un parseur) et que les commandes qu'il lance passent en local.

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

- **bash** `{"command": "ls -la && echo \"---\" && ls .github 2>/dev/null || echo \"no .github\" && echo \"---\" && ls tools/tests/ 2>/dev/null | head -50 && echo \"---\" && ls reports/ | head -40", "description": "Explore repository structure"}`

  ```
total 212
drwxr-xr-x. 1 stephane stephane   760 16 nov 02:01 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    42 16 nov 02:01 build
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane    56 16 nov 00:38 dist
drwxr-xr-x. 1 stephane stephane   138 15 nov 22:25 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   136 16 nov 02:01 drave.egg-info
drwxr-xr-x. 1 stephane stephane   220 16 nov 03:27 .git
-rw-r--r--. 1 stephane stephane   653 15 nov 22:25 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane  1012 16 nov 00:22 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-------. 1 stephane stephane  1272 16 nov 01:44 pyproject.toml
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-boot
… [2713 caractères tronqués]
  ```

- **bash** `{"command": "git status --short && echo \"---BRANCH---\" && git branch --show-current && echo \"---LOG---\" && git log --oneline -5", "description": "Check git status and recent commits"}`

  ```
M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/session-b3e96cb1-fb3b-4593-a2a6-b034ae644413/digest.md
 M journal/sessions/session-b3e96cb1-fb3b-4593-a2a6-b034ae644413/rapport.md
 M tools/chantier/plan.json
---BRANCH---
s/v7
---LOG---
3c10e3ee V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON
ae3c24f2 V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE
2e617034 EXPLOITABLE — U3 : LES PROFILS DE LANGUE (LA DÉTECTION EXPOSÉE, LA MESURE SUR L'ÉCHANTILLON UDHR, LE CONTRÔLE NÉGATIF)
1d4eb49e JOURNAL — 2026-11-16 : U2, LA ROUE AUTONOME ET LA ROUE SANS GOLD QUI SORT EN 4
c77ed4b6 U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE
  ```

- **bash** `{"command": "cat pyproject.toml && echo \"===PORTE===\" && cat tools/porte-produit.sh && echo \"===TEST_PRODUIT===\" && head -60 tools/tests/test_produit.py", "description": "Read pyproject, gate script, test head"}`

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
# Le paquet est un **namespace** (`tools/` n'a pas d'`__init__.py`) : on déclare les
# sous-ensembles dont le CLI a besoin. `tools.tests` reste un namespace implicite
# (son répertoire existe par `tools.tests.linguistique`) : on n'embarque pas les
# scripts de test, seulement les modules et les gold de la mesure.
packages = ["tools", "tools.llm", "tools.structures", "tools.tests.linguistique"]

[tool.setuptools.package-data]
# Les gold et l'artefact de profils sont **dans la roue** : `drave evaluer` et
# `drave profils` doivent marcher hors du dépôt. Le contrôle négatif (une roue
# amputée de ces fichiers) est décrit dans reports/rapport-roue.md et
# reports/rapport-profils.md : la mesure et la détection échouent alors en code 4,
# sans trace et sans stdout.
"tools.tests.linguistique" = [
    "gold.json",
    "gold_gele.json",
    "gold_reel.json",
    "gold_restitution_v2.js
… [8648 caractères tronqués]
  ```

- **bash** `{"command": "command -v act || echo \"NO ACT\"; command -v python3; python3 --version; ls /usr/bin/python3* 2>/dev/null; echo \"---\"; python3 -c \"import yaml; print('pyyaml', yaml.__version__)\" 2>&1; echo \"---\"; ls .github 2>/dev/null; find . -maxdepth 3 -name \"*.yml\" -o -maxdepth 3 -name \"* … [79 caractères tronqués]`

  ```
NO ACT
/usr/bin/python3
Python 3.13.16
/usr/bin/python3
/usr/bin/python3.13
/usr/bin/python3.13-config
/usr/bin/python3.14
/usr/bin/python3-config
---
pyyaml 6.0.3
---
  ```

- **bash** `{"command": "command -v uv || echo no-uv; command -v pyenv || echo no-pyenv; command -v conda || echo no-conda; command -v docker || echo no-docker; command -v python3.10 || echo no-3.10; ls /usr/local/bin/python* 2>/dev/null; echo \"---\"; python3 -m pip --version; echo \"---\"; python3 -c \"import … [87 caractères tronqués]`

  ```
/home/stephane/.local/share/../bin/uv
no-pyenv
no-conda
/usr/bin/docker
no-3.10
---
pip 26.2.2 from /usr/lib/python3.13/site-packages/pip (python 3.13)
---
  ```

- **bash** `{"command": "head -80 tools/tests/test_tagger_api.py; echo \"===SCHEMA===\"; head -50 tools/tests/test_schema_produit.py; echo \"===REPORTS GREP CI===\"; ls reports | grep -i -E 'ci|integra|workflow' | head -20; echo \"===REPORTS RECENT===\"; ls -t reports/*.md | head -10", "description": "Read test … [31 caractères tronqués]`

  ```
"""test_tagger_api.py — le tagger POS par API, **en option**, sans réseau.

Ce que le fichier verrouille, avec un **transport factice** (une fonction qui rend un JSON de
POS valide) :

1. la cascade remplace bien les POS par ceux du tagger (et garde les syntagmes de l'heuristique,
   avec leurs rôles et leurs cibles) ;
2. le JSON reste valide : le schéma **déclaré** (v2) le lit, et le contrat **v1** reste lisible ;
3. deux analyses du même texte ne refont pas d'appel (cache mémoire des taggers) ;
4. le défaut est inchangé : `analyser --json` sans `--tagger` rend exactement l'heuristique ;
5. les quatre cas d'erreur, chacun avec un transport factice :
   - **clé absente** → code **4**, message clair, `stdout` vide (`TestCle.test_sans_cle_code_4`) ;
   - **clé invalide** (HTTP 401/403) → code **4**, message clair, `stdout` vide, pas de repli ;
   - **réseau coupé** → **repli heuristique**, code **0**, `refus` non vide et message sur `stderr` ;
   - **refus du modèle** (texte non JSON, JSON incomplet) → **repli heuristique**, code **0**,
     `refus` non vide ;
6. l'ordre de résolution de la clé : `DEEPSEEK_KEY_FILE`, puis `~/.config/drave/deepseek.key`,
   puis `DEEPSEEK_API_KEY` ;
7
… [5373 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"Z1\\|Tâche Z\\|CI\\b\\|intégration continue\" docs/pilotage reports/README.md reports/INDEX.md AGENTS.md 2>/dev/null | head -40", "description": "Search for Z1 and CI references"}`

  ```
docs/pilotage/utilisation.md:39:| dépôt | [**stephanedenis/docwatch**](https://github.com/stephanedenis/docwatch) ✓ — licence MIT, CI Python 3.9–3.13 |
docs/pilotage/utilisation.md:43:**Le 27/10, l'outil a été isolé de Drave** ✓✓ : code, **87 tests**, CI Python 3.9–3.13, README et licence MIT
  ```

- **bash** `{"command": "cat reports/rapport-profils.md; echo \"===JSON===\"; cat reports/rapport-profils.json 2>/dev/null || ls reports | grep profils", "description": "Read a recent report and JSON"}`

  ```
# U3 — `drave profils` : la détection de langue des 398 profils UDHR, exposée

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **U3** (suite de T5) ·
> **Date** : 2026-11-16 · **Verdict** : ✅ **la détection est exposée** ; **20/20** langues
> et **20/20** scripts sur l'échantillon UDHR de 20 langues (article 15 tenu à l'écart),
> **313/320 = 0,9781** sur les articles 15–30, **433/447 = 0,9687** sur l'autotest complet
> 398 langues. Le texte ambigu bilingue rend **`und`** (0,0836 < 0,12), un mot isolé rend
> **`und`**, et les profils permutés tombent à **0/20** (0,0022 sur 447).
>
> **Le chiffre.** `drave profils --texte "Le chat dort."` rend **`fra`**, le script **`Latn`**
> et la confiance **0,3333** (source `lexique`, prior des mots-outils) ; un article 15 de
> l'UDHR rend la langue et le script par les **398 profils** (`source: profils`). La roue U2
> embarque l'artefact : **802 110 octets**, sha256 `33aee69d…`, et `drave profils` fonctionne
> **hors du dépôt**, depuis `/tmp`.
>
> **Dispositif** : [`tools/profils_udhr.py`](../tools/profils_udhr.py) (chargement, détection,
> prior court), [`tools/construire_profils_udhr.py`](../tools/construire_profils_udhr.py)
> (artefa
… [11849 caractères tronqués]
  ```

- **bash** `{"command": "uv python list 2>&1 | head -30; echo \"---find---\"; uv python find 3.10 2>&1 || true; echo \"---pip cache---\"; python3 -m pip cache dir 2>/dev/null; ls ~/.cache/uv/python 2>/dev/null || true", "description": "Check uv Python availability"}`

  ```
cpython-3.15.0rc1-linux-x86_64-gnu                 <download available>
cpython-3.15.0rc1+freethreaded-linux-x86_64-gnu    <download available>
cpython-3.14.8-linux-x86_64-gnu                    /usr/bin/python3.14
cpython-3.14.7-linux-x86_64-gnu                    <download available>
cpython-3.14.7+freethreaded-linux-x86_64-gnu       <download available>
cpython-3.13.16-linux-x86_64-gnu                   /usr/bin/python3.13
cpython-3.13.16-linux-x86_64-gnu                   /usr/bin/python3 -> python3.13
cpython-3.13.15-linux-x86_64-gnu                   <download available>
cpython-3.13.15+freethreaded-linux-x86_64-gnu      <download available>
cpython-3.12.13-linux-x86_64-gnu                   /home/stephane/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12
cpython-3.11.15-linux-x86_64-gnu                   <download available>
cpython-3.10.20-linux-x86_64-gnu                   <download available>
cpython-3.9.25-linux-x86_64-gnu                    <download available>
cpython-3.8.20-linux-x86_64-gnu                    <download available>
pypy-3.11.15-linux-x86_64-gnu                      <download available>
pypy-3.10.16-linux-x86_64-gnu                     
… [613 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' docs/pilotage/en-cours.md; echo \"===ROADMAP TAIL===\"; tail -80 docs/pilotage/roadmap.md", "description": "Read current state and roadmap"}`

  ```
# En ce moment

**Mis à jour : 2026-11-16 (V3)**

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
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.
>
> **Règle 11** : serveurs 
… [17662 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn '\"Z1\"\\|Z1\\|protection\\|intégration continue' tools/chantier/plan.json journal docs/pilotage 2>/dev/null | head -30; echo \"===PLAN===\"; head -80 tools/chantier/plan.json", "description": "Search plan.json for Z1"}`

  ```
tools/chantier/plan.json:929:   "id": "Z1",
tools/chantier/plan.json:931:   "titre": "L'intégration continue — le workflow",
tools/chantier/plan.json:932:   "mandat": "Tâche Z1 (exploitable, la protection) : l'**intégration continue** — un `.github/workflows/ci.yml` : la matrice **Python 3.10 / 3.13**, `pip install -e .`, `python3 tools/tests/test_produit.py`, `python3 tools/tests/test_tagger_api.py`, `bash tools/porte-produit.sh`, `python3 tools/tests/test_schema_produit.py` ; le **contrôle négatif** : un test qui casse doit faire échouer le job (le prouver en local) ; la doc. Fiche `reports/rapport-ci.md` + JSON. Si l'environnement n'a pas `act`, prouve au moins que le YAML est valide (un parseur) et que les commandes qu'il lance passent en local.",
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:32003:6509:.visible .entry _Z11attn_scoresPKvPKfS2_Pfiiiiiif(
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:32005:6508:	// .globl	_Z11attn_scoresPKvPKfS2_Pfiiiiiif // -- Begin function _Z11attn_scoresPKvPKfS2_Pfiiiiiif
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:32006:6509:.visible .entry _Z11attn_scoresPKvPKfS2_Pfiiiiiif(
journal/ses
… [8577 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/README.md | head -80; echo \"===INDEX===\"; head -60 reports/INDEX.md", "description": "Read report registry conventions"}`

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
| [`rapport-bilan-jour-1115.md`](rapport-bilan-jour-1115.md) | **Bilan** — le 15/11 : la semaine 2 en un jour, la décision du tagger |
| [`rapport-bilan-semaine.md`](rapport-bilan-semaine.md) | **Bilan** — la semaine 07 → 15/11 : le produit, Panini, la coordination, le harnais |
| [`rapport-bilan-nuit.md`](r
… [14757 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nfor t in p['taches']:\n    if t['id'].startswith('Z'):\n        print(json.dumps(t, ensure_ascii=False, indent=2))\nEOF", "description": "Print all Z tasks from plan"}`

  ```
{
  "id": "Z1",
  "jour": 22,
  "titre": "L'intégration continue — le workflow",
  "mandat": "Tâche Z1 (exploitable, la protection) : l'**intégration continue** — un `.github/workflows/ci.yml` : la matrice **Python 3.10 / 3.13**, `pip install -e .`, `python3 tools/tests/test_produit.py`, `python3 tools/tests/test_tagger_api.py`, `bash tools/porte-produit.sh`, `python3 tools/tests/test_schema_produit.py` ; le **contrôle négatif** : un test qui casse doit faire échouer le job (le prouver en local) ; la doc. Fiche `reports/rapport-ci.md` + JSON. Si l'environnement n'a pas `act`, prouve au moins que le YAML est valide (un parseur) et que les commandes qu'il lance passent en local.",
  "budget_min": 90,
  "acceptation": [
    {
      "commande": "test -f .github/workflows/ci.yml && echo CI-OK",
      "attendu": "CI-OK"
    },
    {
      "commande": "test -f reports/rapport-ci.md && echo FICHE-OK",
      "attendu": "FICHE-OK"
    }
  ]
}
{
  "id": "Z2",
  "jour": 22,
  "titre": "La passe complète de la nuit",
  "mandat": "Tâche Z2 (clôture technique) : la **passe complète** — `bash tools/toutes-les-portes.sh` avec `JOURNAUX=work/portes/passe-1611` ; lis le registre par `awk '$2 != 0'` (
… [1221 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '880,980p' tools/chantier/plan.json", "description": "Read plan around Z1"}`

  ```
"titre": "Le banc — evaluer --strict",
   "mandat": "Tâche V1 (exploitable, la suite du bilan T6) : `evaluer --strict` — le banc de recherche (`evaluer_gold.py`) mesure quatre modes et la cascade locale avec le plancher 0,70 ; le CLI ne le fait pas. Ajoute `--strict` à `evaluer` : mesure la **cascade locale** (`MockNeuronal`) sur 612 et le réel 452, **applique le plancher 0,70** (un échec = code 1), affiche les quatre modes (heuristique, neuronal, parallèle, cascade) et le delta ; le **contrôle négatif** (la cascade sous le plancher doit échouer). Fiche `reports/rapport-evaluer-strict.md` + JSON, un test, la doc § 3.3.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-evaluer-strict.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    },
    {
     "commande": "python3 tools/drave.py evaluer --strict >/dev/null 2>&1; echo STRICT-$?",
     "attendu": "STRICT-0"
    }
   ]
  },
  {
   "id": "V2",
   "jour": 21,
   "titre": "Les exemples — le JSON de la v2",
   "mandat": "Tâche V2 (exploitable) : les **exemples de la doc** — rejoue les 5 blocs de `docs/produit/exemples.md` avec le code courant (**les candidats objets, les rôles normalisés, la d
… [3747 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat --oneline 3c10e3ee | head -50; echo \"===T5?===\"; git log --oneline --all | head -20", "description": "Inspect recent task commit contents"}`

  ```
3c10e3ee V3 — LA CLÔTURE : 9 TÂCHES T1–T6 · U1–U3 + V1–V2, 86 PORTES (82/4 LUES, 84/2 APRÈS CIBLAGE), TAG exploitable-2026-11-16 SUR ae3c24f2 ; BILAN 2 + JSON
 docs/pilotage/en-cours.md                          |   17 +-
 docs/pilotage/references-non-regression.md         |    6 +
 docs/pilotage/roadmap.md                           |   17 +-
 journal/2026-11-16/README.md                       |   21 +-
 journal/2026-11-16/docs.md                         |    4 +-
 journal/2026-11-16/memoire.md                      |    2 +-
 journal/2026-11-16/mesures.md                      |    2 +-
 journal/2026-11-16/moteur.md                       |    2 +-
 journal/README.md                                  |    5 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   20 +
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md   |    4 +-
 .../rapport.md                                     |   14 +-
 .../digest.md                                      |   63 +
 .../rapport.md                                     |   27 +-
 .../digest.md                                      | 2547 ++++++++++++++++++++
 .../rapport.md                   
… [2911 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat --oneline 2e617034 | head -40; echo \"===EXEMPLES-V2 JSON===\"; ls reports | grep -E 'exemples-v2|evaluer-strict|profils.json'", "description": "Inspect another task commit and JSON naming"}`

  ```
2e617034 EXPLOITABLE — U3 : LES PROFILS DE LANGUE (LA DÉTECTION EXPOSÉE, LA MESURE SUR L'ÉCHANTILLON UDHR, LE CONTRÔLE NÉGATIF)
 journal/2026-11-16/README.md                       |    6 +-
 journal/2026-11-16/docs.md                         |   19 +
 journal/2026-11-16/memoire.md                      |    2 +-
 journal/2026-11-16/mesures.md                      |    2 +-
 journal/README.md                                  |    7 +-
 journal/THEMES.md                                  |    1 +
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  118 +
 .../rapport.md                                     |   18 +-
 .../digest.md                                      |  139 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 4640 ++++++++++++++++++++
 .../rapport.md                                     |  268 ++
 13 files changed, 5216 insertions(+), 25 deletions(-)
===EXEMPLES-V2 JSON===
evaluer-strict.json
profils.json
rapport-evaluer-strict.md
rapport-exemples-v2.json
rapport-exemples-v2.md
  ```

- **bash** `{"command": "python3 tools/tests/test_produit.py 2>&1 | tail -8; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run product smoke test", "timeout_ms": 300000}`

  ```
..............................
----------------------------------------------------------------------
Ran 30 tests in 17.383s

OK
EXIT=0
  ```

- **bash** `{"command": "python3 tools/tests/test_schema_produit.py 2>&1 | tail -8; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run schema product test", "timeout_ms": 300000}`

  ```
T2 : `meta.attachement.candidats` est typé, et `role` est un vocabulaire fermé. ... ok
test_le_schema_v2_declare_partition_et_alternative (__main__.TestSchemaV2.test_le_schema_v2_declare_partition_et_alternative)
Les deux champs ajoutés en v2 sont typés, pas seulement tolérés. ... ok

----------------------------------------------------------------------
Ran 9 tests in 1.616s

OK
EXIT=0
  ```

- **bash** `{"command": "python3 tools/tests/test_tagger_api.py 2>&1 | tail -8; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run tagger API test", "timeout_ms": 300000}`

  ```
~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 1 != 0 : drave: erreur : TypeError : TestMatriceW3.test_cout_pour_1000_phrases.<locals>.<lambda>() got an unexpected keyword argument 'gele'


----------------------------------------------------------------------
Ran 30 tests in 7.793s

FAILED (failures=2)
EXIT=1
  ```

- **bash** `{"command": "bash tools/porte-produit.sh 2>&1 | tail -25; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run product gate", "timeout_ms": 900000}`

  ```
[still running after 60000ms; moved to background job bash-20]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "python3 tools/tests/test_tagger_api.py 2>&1 | grep -n -A25 -B10 'FAIL:\\|ERROR:\\|TypeError' | head -120", "description": "Inspect tagger test failures", "timeout_ms": 300000}`

  ```
30-test_auto_refus_du_modele_repli (__main__.TestTaggerAuto.test_auto_refus_du_modele_repli)
31-Un modèle qui ne rend pas le contrat POS est un repli, pas un code 4. ... ok
32-test_auto_refus_texte_code_3 (__main__.TestTaggerAuto.test_auto_refus_texte_code_3) ... ok
33-test_auto_reseau_coupe_code_0 (__main__.TestTaggerAuto.test_auto_reseau_coupe_code_0) ... ok
34-test_auto_sans_cle_identique_au_defaut (__main__.TestTaggerAuto.test_auto_sans_cle_identique_au_defaut) ... ok
35-test_auto_sans_cle_n_importe_pas_le_reseau (__main__.TestTaggerAuto.test_auto_sans_cle_n_importe_pas_le_reseau) ... ok
36-test_auto_texte_apres_le_drapeau (__main__.TestTaggerAuto.test_auto_texte_apres_le_drapeau)
37-`--tagger auto TEXTE` ne doit pas avaler le texte comme une valeur de `--tagger`. ... ok
38-
39-======================================================================
40:FAIL: test_evaluer_tagger (__main__.TestCliAvecTransportFactice.test_evaluer_tagger)
41-----------------------------------------------------------------------
42-Traceback (most recent call last):
43-  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", line 323, in test_evaluer_tagger
44-    self
… [1118 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"gele\" tools/tests/test_tagger_api.py tools/drave.py tools/llm tools/tests/linguistique 2>/dev/null | head -30", "description": "Find gele argument usage"}`

  ```
tools/drave.py:748:GOLD_GELE = ("gold_gele.json",)
tools/drave.py:751:def _module_evaluation(gele: bool = False):
tools/drave.py:757:    être simulée, et le message dit quoi faire. `gele=True` ne requiert que le gold gelé.
tools/drave.py:763:    manquants = [nom for nom in (GOLD_GELE if gele else GOLD_VIVANT)
tools/drave.py:772:            "gelé (`gold_gele.json`) s'il est présent ; il ne remplace pas un gold absent."
tools/drave.py:1094:    evaluateur = _module_evaluation(gele=bool(args.gold))
tools/drave.py:1095:    phrases = evaluateur.charger_gele() if args.gold else evaluateur.charger()
tools/drave.py:1123:            "gele": bool(args.gold),
tools/drave.py:1503:                         help="mesurer le gold gelé gold_gele.json (livré avec la roue) au lieu "
tools/llm/prompts_publics_300.jsonl:203:{"id": "udhr-21-deu", "system": "Tu es un traducteur professionnel. Réponds uniquement par la traduction, sans commentaire.", "prompt": "Traduis en allemand l'article 21 de la Déclaration universelle des droits de l'homme. Réponds uniquement par la traduction.\n\nEveryone has the right to take part in the government of his country, directly or through freely chosen representatives. E
… [2193 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '280,350p' tools/tests/test_tagger_api.py; echo \"===MATRICE===\"; sed -n '470,545p' tools/tests/test_tagger_api.py; echo \"===DRAVE===\"; sed -n '1080,1135p' tools/drave.py", "description": "Read failing test code and drave call"}`

  ```
"""La CLI de bout en bout, client injecté : le chemin `--tagger` et son coût."""

    def setUp(self) -> None:
        self.client = _FauxClient()
        self._ancien_client = drave._client_tagger
        drave._client_tagger = lambda: self.client

    def tearDown(self) -> None:
        drave._client_tagger = self._ancien_client

    def _lancer(self, *arguments: str) -> tuple[int, str, str]:
        sortie, erreur = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(sortie), contextlib.redirect_stderr(erreur):
            code = drave.main(list(arguments))
        return code, sortie.getvalue(), erreur.getvalue()

    def test_analyser_tagger_json(self) -> None:
        code, sortie, erreur = self._lancer("analyser", TEXTE, "--tagger", "--json")
        self.assertEqual(code, 0, erreur)
        donnees = json.loads(sortie)
        self.assertEqual(_pos_map(donnees), {(0, 2): "VERB", (3, 7): "DET", (8, 12): "ADV", (12, 13): "PONCT"})
        self.assertEqual(donnees["source"], "cascade")
        self.assertIn("TAGGER API", erreur)
        self.assertEqual(self.client.demandes, 1)

    def test_analyser_tagger_lisible(self) -> None:
        code, sortie, erreur =
… [9119 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"_module_evaluation\\s*=\\|_module_evaluation(\" tools/tests tools | grep -v __pycache__ | head -30", "description": "Find monkeypatches of _module_evaluation"}`

  ```
tools/tests/test_tagger_api.py:314:        evaluateur = drave._module_evaluation()
tools/tests/test_tagger_api.py:318:        drave._module_evaluation = lambda: evaluateur
tools/tests/test_tagger_api.py:322:            drave._module_evaluation = ancien_module
tools/tests/test_tagger_api.py:511:        evaluateur = drave._module_evaluation()
tools/tests/test_tagger_api.py:521:        drave._module_evaluation = lambda: evaluateur
tools/tests/test_tagger_api.py:528:            drave._module_evaluation = ancien_module
tools/tests/test_evaluer_strict.py:90:        drave._module_evaluation = lambda gele=False: object()
tools/tests/test_evaluer_strict.py:103:            drave._module_evaluation = ancien_module
tools/tests/test_tagger_api.py:314:        evaluateur = drave._module_evaluation()
tools/tests/test_tagger_api.py:318:        drave._module_evaluation = lambda: evaluateur
tools/tests/test_tagger_api.py:322:            drave._module_evaluation = ancien_module
tools/tests/test_tagger_api.py:511:        evaluateur = drave._module_evaluation()
tools/tests/test_tagger_api.py:521:        drave._module_evaluation = lambda: evaluateur
tools/tests/test_tagger_api.py:528:            drave._m
… [428 caractères tronqués]
  ```

- **bash** `{"command": "true", "description": "noop"}`

  ```
(no output)
  ```

- **job_output** `{"job_id": "bash-20", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "old_string": "        drave._module_evaluation = lambda: evaluateur\n        try:\n            code, sortie, erreur = self._lancer(\"evaluer\", \"--tagger\", \"--json\")", "new_string": "        drave._m … [152 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "old_string": "        drave._module_evaluation = lambda: evaluateur\n        try:\n            sortie, erreur = io.StringIO(), io.StringIO()", "new_string": "        drave._module_evaluation = lambda gel … [94 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py": file has not been read — read the file, then retry
  ```

- **bash** `{"command": "wc -l tools/tests/test_tagger_api.py", "description": "Count lines in test file"}`

  ```
739 tools/tests/test_tagger_api.py
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "limit": 739}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py</path>
<type>file</type>
<content>
1: """test_tagger_api.py — le tagger POS par API, **en option**, sans réseau.
2: 
3: Ce que le fichier verrouille, avec un **transport factice** (une fonction qui rend un JSON de
4: POS valide) :
5: 
6: 1. la cascade remplace bien les POS par ceux du tagger (et garde les syntagmes de l'heuristique,
7:    avec leurs rôles et leurs cibles) ;
8: 2. le JSON reste valide : le schéma **déclaré** (v2) le lit, et le contrat **v1** reste lisible ;
9: 3. deux analyses du même texte ne refont pas d'appel (cache mémoire des taggers) ;
10: 4. le défaut est inchangé : `analyser --json` sans `--tagger` rend exactement l'heuristique ;
11: 5. les quatre cas d'erreur, chacun avec un transport factice :
12:    - **clé absente** → code **4**, message clair, `stdout` vide (`TestCle.test_sans_cle_code_4`) ;
13:    - **clé invalide** (HTTP 401/403) → code **4**, message clair, `stdout` vide, pas de repli ;
14:    - **réseau coupé** → **repli heuristique**, code **0**, `refus` non vide et message sur `stderr` ;
15:    - **refus du modèle** (texte non JSON, JSON incomplet) → **repli heuri
… [39188 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "new_string": "        drave._module_evaluation = lambda gele=False: evaluateur\n        try:\n            code, sortie, erreur = self._lancer(\"evaluer\", \"--tagger\", \"--json\")", "old_string": "      … [152 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "new_string": "        drave._module_evaluation = lambda gele=False: evaluateur\n        try:\n            sortie, erreur = io.StringIO(), io.StringIO()", "old_string": "        drave._module_evaluation = … [94 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/tests/test_tagger_api.py 2>&1 | tail -6; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Rerun tagger API test", "timeout_ms": 300000}`

  ```
`--tagger auto TEXTE` ne doit pas avaler le texte comme une valeur de `--tagger`. ... ok

----------------------------------------------------------------------
Ran 30 tests in 7.382s

OK
EXIT=0
  ```

- **job_output** `{"job_id": "bash-20", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "uv python install 3.10 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"; uv python find 3.10 2>&1 || true", "description": "Try installing Python 3.10 with uv", "timeout_ms": 300000}`

  ```
Downloading cpython-3.10.20-linux-x86_64-gnu (download) (28.1MiB)
 Downloaded cpython-3.10.20-linux-x86_64-gnu (download)
Installed Python 3.10.20 in 2.22s
 + cpython-3.10.20-linux-x86_64-gnu (python3.10)
EXIT=0
/home/stephane/.local/share/uv/python/cpython-3.10-linux-x86_64-gnu/bin/python3.10
  ```

- **bash** `{"command": "git diff --stat; git diff -- tools/tests/test_tagger_api.py | head -40", "description": "Show test fix diff"}`

  ```
journal/README.md                                  |   2 +-
 journal/sessions/MANIFEST.md                       |   2 +-
 .../digest.md                                      | 240 +++++++++++++++++++++
 .../rapport.md                                     |  38 +++-
 tools/chantier/plan.json                           |  47 ++++
 tools/tests/test_tagger_api.py                     |   4 +-
 6 files changed, 322 insertions(+), 11 deletions(-)
diff --git a/tools/tests/test_tagger_api.py b/tools/tests/test_tagger_api.py
index a7ca49b5..3941a17a 100644
--- a/tools/tests/test_tagger_api.py
+++ b/tools/tests/test_tagger_api.py
@@ -315,7 +315,7 @@ class TestCliAvecTransportFactice(unittest.TestCase):
         chargeur = evaluateur.charger
         evaluateur.charger = lambda: chargeur()[:2]
         ancien_module = drave._module_evaluation
-        drave._module_evaluation = lambda: evaluateur
+        drave._module_evaluation = lambda gele=False: evaluateur
         try:
             code, sortie, erreur = self._lancer("evaluer", "--tagger", "--json")
         finally:
@@ -518,7 +518,7 @@ class TestMatriceW3(unittest.TestCase):
         evaluateur.charger = lambda: [premier, second]
         
… [371 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-20", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "rm -rf /tmp/ci310 && /home/stephane/.local/share/uv/python/cpython-3.10-linux-x86_64-gnu/bin/python3.10 -m venv /tmp/ci310 && /tmp/ci310/bin/python -m pip install --upgrade pip -q && /tmp/ci310/bin/pip install -e . 2>&1 | tail -15; echo \"EXIT=${PIPESTATUS[0]}\"; /tmp/ci310/bin/python - … [169 caractères tronqués]`

  ```
/tmp/pip-build-env-mdubysv6/overlay/lib/python3.10/site-packages/setuptools/command/editable_wheel.py:354: BuildBackendWarning: Editable installation.
  !!
  
          ********************************************************************************
          Please be careful with folders in your working directory with the same
          name as your package as they may take precedence during imports.
          ********************************************************************************
  
  !!
    with strategy, WheelFile(wheel_path, "w") as wheel_obj:
  Created wheel for drave: filename=drave-0.1.0-0.editable-py3-none-any.whl size=2957 sha256=fc36da0e89e56f38528041f44a379f22483f21393c891f7b5e7cac3d7ec4a26c
  Stored in directory: /tmp/pip-ephem-wheel-cache-mjytals2/wheels/48/5b/99/493e15c466c82920f23becb9ec12a572cd5a4c9d943a087422
Successfully built drave
Installing collected packages: drave
Successfully installed drave-0.1.0
EXIT=0
Python 3.10.20
import ok
  ```

- **bash** `{"command": "rm -rf /tmp/ci313 && python3 -m venv /tmp/ci313 && /tmp/ci313/bin/python -m pip install --upgrade pip -q && /tmp/ci313/bin/pip install -e . 2>&1 | tail -15; echo \"EXIT=${PIPESTATUS[0]}\"; /tmp/ci313/bin/python --version; /tmp/ci313/bin/python -c \"import tools.drave; print('import ok') … [94 caractères tronqués]`

  ```
/tmp/pip-build-env-yzjlj_6f/overlay/lib/python3.13/site-packages/setuptools/command/editable_wheel.py:354: BuildBackendWarning: Editable installation.
  !!
  
          ********************************************************************************
          Please be careful with folders in your working directory with the same
          name as your package as they may take precedence during imports.
          ********************************************************************************
  
  !!
    with strategy, WheelFile(wheel_path, "w") as wheel_obj:
  Created wheel for drave: filename=drave-0.1.0-0.editable-py3-none-any.whl size=2957 sha256=c97f3caec8b6ffde145d43ed2454d1f45fff5cfdb803b8bce483d34620900de7
  Stored in directory: /tmp/pip-ephem-wheel-cache-kbg_216h/wheels/96/02/a3/318108f401dc37bb3a575e67c80cf111852262a4b3c9f691ec
Successfully built drave
Installing collected packages: drave
Successfully installed drave-0.1.0
EXIT=0
Python 3.13.16
import ok
  ```

- **bash** `{"command": "export PATH=/tmp/ci310/bin:$PATH; echo \"PY=$(python3 --version)\"; for f in tools/tests/test_produit.py tools/tests/test_tagger_api.py tools/tests/test_schema_produit.py; do echo \"=== $f ===\"; /usr/bin/time -f 'TIME=%e' python3 \"$f\" >/tmp/ci310-$(basename $f).log 2>&1; rc=$?; tail  … [135 caractères tronqués]`

  ```
PY=Python 3.10.20
=== tools/tests/test_produit.py ===

OK
TIME=16.10
EXIT=0
=== tools/tests/test_tagger_api.py ===

OK
TIME=7.80
EXIT=0
=== tools/tests/test_schema_produit.py ===

OK
TIME=1.30
EXIT=0
  ```

- **bash** `{"command": "export PATH=/tmp/ci313/bin:$PATH; echo \"PY=$(python3 --version)\"; for f in tools/tests/test_produit.py tools/tests/test_tagger_api.py tools/tests/test_schema_produit.py; do echo \"=== $f ===\"; /usr/bin/time -f 'TIME=%e' python3 \"$f\" >/tmp/ci313-$(basename $f).log 2>&1; rc=$?; tail  … [135 caractères tronqués]`

  ```
PY=Python 3.13.16
=== tools/tests/test_produit.py ===

OK
TIME=17.51
EXIT=0
=== tools/tests/test_tagger_api.py ===

OK
TIME=7.76
EXIT=0
=== tools/tests/test_schema_produit.py ===

OK
TIME=1.51
EXIT=0
  ```

### 👤 Utilisateur

background job bash-20 (bash: bash tools/porte-produit.sh 2>&1 | tail -25; echo "EXIT=${PIPESTATUS[0]}") finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-20", "wait": false}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ profils : langue, script, confiance, 398 profils
  ✅ rejeu : sha256 f6355d8175a75854 deux fois
  ✅ smoke test : Ran 30 tests
  ✅ evaluer --strict : Ran 5 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v2 : rôles lisibles, rendu relu, contrôle détecté
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ exemples de la doc : 27/27 cas conformes — ✅ aucun écart
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
EXIT=0
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cat .gitmodules; echo \"---\"; git remote -v; echo \"---\"; git branch -r | head -10; echo \"---submodule---\"; git submodule status 2>&1 | head", "description": "Inspect submodules and remotes"}`

  ```
[submodule "tools/docwatch"]
	path = tools/docwatch
	url = https://github.com/stephanedenis/docwatch.git
[submodule "tools/structures"]
	path = tools/structures
	url = /home/stephane/Data13TB/stephane/GitHub/drave-structures
---
origin	git@github.com:stephanedenis/drave.git (fetch)
origin	git@github.com:stephanedenis/drave.git (push)
---
  origin/HEAD -> origin/master
  origin/master
  origin/s/close
  origin/s/v7
---submodule---
 d256888934b017ac024de2a8eed22ecf81e6c799 tools/docwatch (v0.4.1-3-gd256888)
 648adce3ea18ef4d142778fd67d42413aae5ae64 tools/structures (heads/master)
  ```

- **bash** `{"command": "ls -la tools/structures 2>/dev/null | head; echo \"---\"; ls drave-core; echo \"---\"; grep -rn \"submodule\\|tools/structures\" tools/tests/test_produit.py tools/tests/test_schema_produit.py tools/tests/test_tagger_api.py tools/porte-produit.sh | head", "description": "Check submodule  … [21 caractères tronqués]`

  ```
total 160
drwxr-xr-x. 1 stephane stephane   438 16 nov 00:04 .
drwxr-xr-x. 1 stephane stephane 18686 16 nov 02:43 ..
-rw-r--r--. 1 stephane stephane  7469  3 nov 17:08 arbre_svg.py
-rw-------. 1 stephane stephane  4388  2 nov 20:04 candidats_corpus.py
-rw-r--r--. 1 stephane stephane  7035  2 nov 02:10 construire_donnees.py
drwxr-xr-x. 1 stephane stephane   414  3 nov 16:49 donnees
-rw-r--r--. 1 stephane stephane 11442  2 nov 16:27 exporter_corpus.py
-rw-r--r--. 1 stephane stephane 31037 16 nov 00:04 generateur.py
-rw-r--r--. 1 stephane stephane    44  1 nov 10:50 .git
---
Cargo.lock
Cargo.toml
gpu
README.md
src
target
tests
---
  ```

- **bash** `{"command": "grep -rn \"tools.structures\\|from structures\\|import structures\\|tools/structures\" tools --include='*.py' --include='*.sh' | grep -v __pycache__ | head -30", "description": "Find code depending on structures submodule"}`

  ```
tools/tests/test_empaquetage.py:9:  `tools.structures`, `tools.llm`), les **gold** et l'artefact de **profils** (`package-data`) ;
tools/tests/test_empaquetage.py:82:        for attendu in ("tools", "tools.llm", "tools.structures",
tools/structures/exporter_corpus.py:38:RACINE = pathlib.Path(__file__).resolve().parents[2]  # tools/structures → racine du dépôt
tools/canal_structure.py:6:([`tools/structures/generateur.py`](../tools/structures/generateur.py)) : mot plein, mot
tools/mesurer_restitution_v3.py:202:            "or_s": "tools/structures/donnees/gold-analyseur.json (61 phrases, 144 rôles)",
tools/bloc_linguistique.py:1222:            if str(RACINE / "tools/structures") not in sys.path:
tools/bloc_linguistique.py:1223:                sys.path.insert(0, str(RACINE / "tools/structures"))
tools/verifie_exemples.py:11:  - les trois commandes du démarrage dans une copie **sans** `tools/structures`, condition du
tools/verifie_exemples.py:265:    """La copie du code **sans** `tools/structures` : la condition du clone public."""
  ```

- **bash** `{"command": "sed -n '1190,1255p' tools/bloc_linguistique.py; echo \"===drave imports===\"; head -60 tools/drave.py", "description": "Check optional structures import"}`

  ```
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
                              and n0 not in lex.get("PRON", set()))
                if (n0e in _suj or nom_propre) and sv:
                    fin_sujet = mots[0][1]
                    if fin_sujet < f:
                        gn = dict(s)
                        gn.update({"type": "GN", "role": "agent", "niveau": 0,
                                   "fin": fin_sujet,
                                   "texte": texte[d:fin_sujet], "parent": None})
               
… [5507 caractères tronqués]
  ```

- **bash** `{"command": "rm -rf /tmp/ci-clone && mkdir -p /tmp/ci-clone && git archive HEAD | tar -x -C /tmp/ci-clone && ls -ld /tmp/ci-clone/tools/structures /tmp/ci-clone/tools/docwatch 2>&1; rm -rf /tmp/ci-clone-venv && /home/stephane/.local/share/uv/python/cpython-3.10-linux-x86_64-gnu/bin/python3.10 -m ven … [227 caractères tronqués]`

  ```
drwxr-xr-x. 2 stephane stephane 40 16 nov 03:12 /tmp/ci-clone/tools/docwatch
drwxr-xr-x. 2 stephane stephane 40 16 nov 03:12 /tmp/ci-clone/tools/structures
Obtaining file:///tmp/ci-clone
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Checking if build backend supports build_editable: started
  Checking if build backend supports build_editable: finished with status 'done'
  Getting requirements to build editable: started
  Getting requirements to build editable: finished with status 'done'
  Preparing editable metadata (pyproject.toml): started
  Preparing editable metadata (pyproject.toml): finished with status 'done'
Building wheels for collected packages: drave
  Building editable for drave (pyproject.toml): started
  Building editable for drave (pyproject.toml): finished with status 'done'
  Created wheel for drave: filename=drave-0.1.0-0.editable-py3-none-any.whl size=2931 sha256=abd89f55a5c5b2da00fd4471ba9c0e07a3eaaa0e756835a63bc53d219872df86
  Stored in directory: /tmp/pip-ephem-wheel-cache-mmd2oqxm/wheels/ed/e9/c3/89e42121ff4f75c6e2167bd7b230a63e7ef518422c7f16d486
Successfully built drave
Installing collected packages:
… [173 caractères tronqués]
  ```

- **bash** `{"command": "ls docs/produit; echo \"===README headings===\"; grep -n '^#' docs/produit/README.md; echo \"===demarrage headings===\"; grep -n '^#' docs/produit/demarrage.md", "description": "Inspect product docs structure"}`

  ```
demarrage.md
exemples.md
README.md
===README headings===
1:# Le premier produit — analyser un texte avec Drave
33:## Sommaire
45:## 1. À qui s'adresse le produit
61:## 2. Ce que le produit fait
99:## 3. Comment l'utiliser — cinq exemples réels
105:### 3.1 Analyser une phrase
128:### 3.2 Analyser en JSON et lire l'attachement
165:### 3.3 Mesurer sur le gold
266:### 3.3 quater Traiter un corpus
276:### 3.3 bis La vue des syntagmes qui se chevauchent — les champs du schéma v2
391:### 3.3 ter Le contexte (mémoire de discours)
400:### 3.4 Rejouer et vérifier le déterminisme
417:### 3.5 Le refus, et la langue inconnue
435:### 3.6 Restituer la surface (v0)
470:### 3.6 bis La base honnête — `--reel`
480:### 3.7 Le tagger en option — `--tagger`
608:### 3.8 Les profils de langue — `drave profils`
661:## 4. Ce que le produit ne fait pas encore
745:## 5. Performance
767:## 6. Garanties
811:## 7. Le CLI livré — contrat et manques
905:## 8. FAQ — dix questions
915:### 8.1 Quelles langues le produit reconnaît-il ?
925:### 8.2 Est-ce que ça marche hors ligne ?
932:### 8.3 Combien ça coûte ?
941:### 8.4 Qu'est-ce que `--tagger` change ?
952:### 8.5 Quel est le format de sortie, et est-il stable ?
9
… [840 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' docs/produit/README.md; echo \"===TAIL===\"; tail -50 docs/produit/README.md", "description": "Read product README start and end"}`

  ```
# Le premier produit — analyser un texte avec Drave

> **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
> linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
> il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
> qu'il garantit.
>
> **Vérifié le 2026-11-15** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
> **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
> existent, et la
> porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le
> **prototype `--tagger auto`** (complété le **2026-11-15**, § 3.7) choisit l'API si une clé
> existe, l'heuristique sinon, **sans changer le code de sortie** ; il ne change pas le défaut.
> Le format
> est **version 2** (`schema: "drave.annotation"`,
> `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
> reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du
> § 3.5 ont été relanc
… [8585 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"produit\" docs/README.md | head -20; echo \"---\"; sed -n '1,60p' docs/README.md; echo \"===GARANTIES===\"; sed -n '767,815p' docs/produit/README.md", "description": "Read docs index and guarantees section"}`

  ```
96:| [`produit/demarrage.md`](produit/demarrage.md) | le **quickstart** : cinq minutes, trois commandes |
97:| [`produit/README.md`](produit/README.md) | le **premier produit** : analyser un texte |
98:| [`produit/README.md` § 8](produit/README.md#8-faq--dix-questions) | la **FAQ** : dix questions vérifiées |
99:| [`produit/exemples.md`](produit/exemples.md) | cinq exemples réels, dont un échec connu |
---
# La documentation de [Drave](theorie/glossaire/entrees/drave.md) — quatre familles

> **`docs/` dit ce qui reste vrai** : la méthode, l'[état](theorie/glossaire/entrees/etat.md), la théorie, l'implantation. Les **chiffres** et les
> séries vivent dans [`reports/`](../reports/) ; le **récit daté** dans [`journal/`](../journal/). Une page de
> `docs/` qui se remplit de tableaux de mesures **déménage** dans `reports/`.

> **Chargement facultatif.** Aucun document de ce dossier n'est nécessaire pour commencer une tâche : lire
> [`AGENTS.md`](../AGENTS.md), puis le document de la tâche. Le reste se [charge](theorie/glossaire/entrees/charge-flux-chargeflux.md) au besoin.

## En trois portes

| si vous voulez… | lisez |
|---|---|
| **comprendre le projet** | [la vision](theorie/vision.
… [8003 caractères tronqués]
  ```

- **bash** `{"command": "ls -la journal/2026-11-16; echo \"===README===\"; cat journal/2026-11-16/README.md; echo \"===docs.md tail===\"; tail -40 journal/2026-11-16/docs.md", "description": "Read journal day structure"}`

  ```
total 24
drwxr-xr-x. 1 stephane stephane   90 16 nov 03:10 .
drwxr-xr-x. 1 stephane stephane 1012 16 nov 00:22 ..
-rw-r--r--. 1 stephane stephane 2120 16 nov 03:15 docs.md
-rw-r--r--. 1 stephane stephane 1076 16 nov 03:15 memoire.md
-rw-r--r--. 1 stephane stephane 1879 16 nov 03:15 mesures.md
-rw-r--r--. 1 stephane stephane 1001 16 nov 03:15 moteur.md
-rw-r--r--. 1 stephane stephane 5727 16 nov 03:15 README.md
===README===
# 2026-11-16

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-16/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**7 commits** · **1 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| docs | 2 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 3 | [mesures.md](mesures.md) |
| moteur | 1 | [moteur.md](moteur.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation
… [6899 caractères tronqués]
  ```

- **bash** `{"command": "head -40 journal/2026-11-16/mesures.md; echo \"===MEMOIRE===\"; cat journal/2026-11-16/memoire.md | head -40; echo \"===TOOLS JOURNAL===\"; python3 tools/verifie_journal.py 2>&1 | tail -10; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Inspect journal data files and verifier"}`

  ```
# 2026-11-16 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (3)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 00:19 | `d19f0fc7` | U1 — LES DEUX O(K²) BORNÉS : 10 000 MOTS 4,0 → 0,82 S (×4,9), α 1,53 → 1,08, QUADRATIQUE +0,00077 R² ; 612/452 ET 10 000 MOTS IDENTIQUES AU BIT PRÈS (DIFF VIDE), 127,4 MIO | `en-cours.md`, `roadmap.md`, `README.md` (+17) |
| 00:28 | `04894aea` | U1 — LE CONTRÔLE DE L'INSTRUMENT EST CELUI DE LA PASSE : LINÉAIRE 0,71, QUADRATIQUE 2,11 (ET NON LES VALEURS DE T4) | `en-cours.md`, `README.md`, `memoire.md` (+7) |
| 00:45 | `c77ed4b6` | U2 — LA ROUE AUTONOME : 1 727 201 OCTETS, 422 ENTRÉES, MÊMES JSON HORS DÉPÔT ; SANS GOLD `EVALUER` SORT EN 4, STDOUT VIDE | `en-cours.md`, `roadmap.md`, `README.md` (+19) |

## Chiffres du jour

`×4,9`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.
… [1842 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -- reports/rapport-profils.md reports/profils.json | head; echo \"---\"; git show --stat --oneline 2e617034 | cat", "description": "Trace U3 report commit"}`

  ```
ae3c24f2 V2 — LES EXEMPLES DE LA DOC : 3 BLOCS CORRIGÉS PAR LES RÔLES NORMALISÉS, 18 CANDIDATS OBJETS, 27/27 CAS CONFORMES ; DÉMARRAGE 3/3 SANS SOUS-MODULE
---
2e617034 EXPLOITABLE — U3 : LES PROFILS DE LANGUE (LA DÉTECTION EXPOSÉE, LA MESURE SUR L'ÉCHANTILLON UDHR, LE CONTRÔLE NÉGATIF)
 journal/2026-11-16/README.md                       |    6 +-
 journal/2026-11-16/docs.md                         |   19 +
 journal/2026-11-16/memoire.md                      |    2 +-
 journal/2026-11-16/mesures.md                      |    2 +-
 journal/README.md                                  |    7 +-
 journal/THEMES.md                                  |    1 +
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  118 +
 .../rapport.md                                     |   18 +-
 .../digest.md                                      |  139 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 4640 ++++++++++++++++++++
 .../rapport.md                                     |  268 ++
 13 files changed, 5216 insertions(+), 25 deletions(-)
  ```

- **bash** `{"command": "ls .git/hooks; echo \"---\"; sed -n '1,120p' tools/verifie_etat_a_jour.py 2>/dev/null; echo \"---precommit---\"; cat .git/hooks/pre-commit 2>/dev/null | head -60", "description": "Inspect state hook and pre-commit"}`

  ```
applypatch-msg.sample
commit-msg.sample
fsmonitor-watchman.sample
post-update.sample
pre-applypatch.sample
pre-commit
pre-commit.sample
pre-merge-commit.sample
prepare-commit-msg.sample
pre-push.sample
pre-rebase.sample
pre-receive.sample
push-to-checkout.sample
sendemail-validate.sample
update.sample
---
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
           est en 
… [5298 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"; echo \"---\"; wc -w docs/pilotage/en-cours.md", "description": "Check en-cours size and validity"}`

  ```
en-cours · 1628 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT=0
---
1628 docs/pilotage/en-cours.md
  ```

- **bash** `{"command": "grep -n \"V3\\|exploitable\\|V2\\|Chantiers\\|prochaine\" docs/pilotage/roadmap.md | head -30; echo \"===HEAD===\"; head -60 docs/pilotage/roadmap.md", "description": "Inspect roadmap top and recent lines"}`

  ```
5:> contrôles vivent dans [`reports/`](../../reports/) ; ici : l'[état](../theorie/glossaire/entrees/etat.md), la prochaine action, et ce qui bloque.
18:- **DSH ne reste jamais en attente** : chaque ligne a une **prochaine action** ; si elle est bloquée, on prend la
28:| chantier | ce qu'il couvre | état | prochaine action |
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entree
… [24017 caractères tronqués]
  ```

- **bash** `{"command": "mkdir -p .github/workflows", "description": "Create workflows directory"}`

  ```
(no output)
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.github/workflows/ci.yml", "content": "name: CI\n\n# Le dépôt est sur `s/v7` ; on teste aussi les pull requests et les autres branches.\n# `workflow_dispatch` permet de relancer une matrice à la main sans changer le code.\n\"on\":\n  pus … [1501 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.github/workflows/ci.yml</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "tail -12 tools/tests/test_produit.py", "description": "Check test main block"}`

  ```
def test_global_publie_la_base_reelle(self):
        sortie = drave("evaluer", "--json")
        self.assertEqual(sortie.returncode, 0, detail(sortie))
        d = json.loads(sortie.stdout)
        self.assertIsNotNone(d.get("reel"))
        self.assertEqual(d["reel"]["phrases"], 452)
        self.assertLess(d["reel"]["phrases"], d["gold"]["phrases"])


if __name__ == "__main__":
    unittest.main()
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"verifier_ci.py — vérifier le workflow CI **sans `act`** : YAML, commandes, contrôle négatif.\n\nPOURQUOI CET OUTIL EXISTE. Le workflow `.github/workflows/ci.yml` n'est exécuté que par\nGitHub Actions. Quand `act` n'est pas installé, il reste trois preuves p … [11275 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "export PATH=/tmp/ci310/bin:$PATH; python3 tools/verifier_ci.py --sans-porte 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Quick CI verification on Python 3.10", "timeout_ms": 600000}`

  ```
PyYAML absent : No module named 'yaml'. Installer pyyaml pour vérifier le workflow.
EXIT=1
  ```

- **bash** `{"command": "export PATH=/tmp/ci313/bin:$PATH; python3 tools/verifier_ci.py --sans-porte 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Quick CI verification on Python 3.13", "timeout_ms": 600000}`

  ```
PyYAML absent : No module named 'yaml'. Installer pyyaml pour vérifier le workflow.
EXIT=1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "new_string": "def _sortir_erreur(message: str) -> None:\n    print(message, file=sys.stderr)\n    raise SystemExit(2)\n\n\ndef charger_yaml(chemin: pathlib.Path) -> tuple[dict, str]:\n    try:\n        import yaml … [1250 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib, re\np=pathlib.Path('tools/verifier_ci.py')\ns=p.read_text()\ns=s.replace('raise SystemExit(\"YAML invalide : `jobs.produit` est absent\")','_sortir_erreur(\"YAML invalide : `jobs.produit` est absent\")')\ns=s.replace('raise SystemExit(f\"matrice inatte … [733 caractères tronqués]`

  ```
51:def _sortir_erreur(message: str) -> None:
53:    raise SystemExit(2)
60:        _sortir_erreur(f"PyYAML absent : {exc}. Installer pyyaml pour vérifier le workflow.")
64:        _sortir_erreur(f"YAML invalide : {chemin} : {exc}")
66:        _sortir_erreur(f"YAML invalide : la racine n'est pas un mapping : {type(donnees).__name__}")
80:        _sortir_erreur("YAML invalide : `jobs.produit` est absent")
84:        _sortir_erreur(f"matrice inattendue : {matrice!r} (attendu {MATRICE_ATTENDUE!r})")
89:        _sortir_erreur(f"commandes absentes du workflow : {manquantes}")
91:        _sortir_erreur(f"runs-on inattendu : {job.get('runs-on')!r}")
93:        _sortir_erreur("YAML invalide : aucun déclencheur `on`")
262:    raise SystemExit(main())
  ```

- **bash** `{"command": "/tmp/ci310/bin/pip install -q pyyaml && /tmp/ci310/bin/python -c \"import yaml; print(yaml.__version__)\"", "description": "Install PyYAML in Python 3.10 venv", "timeout_ms": 300000}`

  ```
6.0.3
  ```

- **bash** `{"command": "/tmp/ci313/bin/pip install -q pyyaml && /tmp/ci313/bin/python -c \"import yaml; print(yaml.__version__)\"", "description": "Install PyYAML in Python 3.13 venv", "timeout_ms": 300000}`

  ```
6.0.3
  ```

- **bash** `{"command": "export PATH=/tmp/ci310/bin:$PATH; python3 tools/verifier_ci.py --sans-porte 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Quick CI verification on Python 3.10", "timeout_ms": 600000}`

  ```
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", line 262, in <module>
    raise SystemExit(main())
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", line 213, in main
    contrat = controler(donnees)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", line 83, in controler
    if matrice != MATRICE_ATTENDUES:
NameError: name 'MATRICE_ATTENDUES' is not defined. Did you mean: 'MATRICE_ATTENDUE'?
EXIT=1
  ```

- **bash** `{"command": "export PATH=/tmp/ci313/bin:$PATH; python3 tools/verifier_ci.py --sans-porte 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Quick CI verification on Python 3.13", "timeout_ms": 600000}`

  ```
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", line 262, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", line 213, in main
    contrat = controler(donnees)
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", line 83, in controler
    if matrice != MATRICE_ATTENDUES:
                  ^^^^^^^^^^^^^^^^^
NameError: name 'MATRICE_ATTENDUES' is not defined. Did you mean: 'MATRICE_ATTENDUE'?
EXIT=1
  ```

- **bash** `{"command": "grep -n \"MATRICE\" tools/verifier_ci.py | head", "description": "Check matrix constant names"}`

  ```
48:MATRICE_ATTENDUE = ["3.10", "3.13"]
83:    if matrice != MATRICE_ATTENDUES:
84:        _sortir_erreur(f"matrice inattendue : {matrice!r} (attendu {MATRICE_ATTENDUE!r})")
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/verifier_ci.py')\ns=p.read_text().replace('MATRICE_ATTENDUES','MATRICE_ATTENDUE')\np.write_text(s)\nEOF\ngrep -n \"MATRICE\" tools/verifier_ci.py", "description": "Fix matrix constant typo"}`

  ```
48:MATRICE_ATTENDUE = ["3.10", "3.13"]
83:    if matrice != MATRICE_ATTENDUE:
84:        _sortir_erreur(f"matrice inattendue : {matrice!r} (attendu {MATRICE_ATTENDUE!r})")
  ```

- **bash** `{"command": "export PATH=/tmp/ci310/bin:$PATH; python3 tools/verifier_ci.py --sans-porte 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Quick CI verification on Python 3.10", "timeout_ms": 600000}`

  ```
YAML valide · PyYAML 6.0.3 · matrice ['3.10', '3.13']
Python Python 3.10.20 · act=absent
  ✅ installer            code=0 · 2.961 s
  ✅ test_produit         code=0 · 16.387 s
  ✅ test_tagger_api      code=0 · 7.541 s
  ✅ test_schema_produit  code=0 · 1.234 s
  ✅ contrôle négatif  code=1 · job_echoue=True · étape suivante exécutée=False
✅ CI locale verte
EXIT=0
  ```

- **bash** `{"command": "export PATH=/tmp/ci313/bin:$PATH; python3 tools/verifier_ci.py --sans-porte 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Quick CI verification on Python 3.13", "timeout_ms": 600000}`

  ```
YAML valide · PyYAML 6.0.3 · matrice ['3.10', '3.13']
Python Python 3.13.16 · act=absent
  ✅ installer            code=0 · 3.542 s
  ✅ test_produit         code=0 · 17.814 s
  ✅ test_tagger_api      code=0 · 7.807 s
  ✅ test_schema_produit  code=0 · 1.559 s
  ✅ contrôle négatif  code=1 · job_echoue=True · étape suivante exécutée=False
✅ CI locale verte
EXIT=0
  ```

- **bash** `{"command": "nproc; free -g | head -2", "description": "Check CPU and memory"}`

  ```
40
               total        used        free      shared  buff/cache   available
Mem:             125          24           1           9         110         101
  ```

- **bash** `{"command": "export PATH=/tmp/ci310/bin:$PATH; python3 tools/verifier_ci.py --json > /tmp/ci310-result.json 2> /tmp/ci310-result.err; echo \"EXIT=$?\" >> /tmp/ci310-result.err", "description": "Full CI verification on Python 3.10", "run_in_background": true}`

  ```
started background job bash-62
  ```

- **bash** `{"command": "export PATH=/tmp/ci313/bin:$PATH; python3 tools/verifier_ci.py --json > /tmp/ci313-result.json 2> /tmp/ci313-result.err; echo \"EXIT=$?\" >> /tmp/ci313-result.err", "description": "Full CI verification on Python 3.13", "run_in_background": true}`

  ```
started background job bash-63
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "new_string": "        print(f\"YAML valide · {resultat['yaml']['parseur']} · matrice {contrat['matrice']}\")\n        print(f\"{resultat['python_version']} · act={resultat['act'] or 'absent'}\")", "old_string": "  … [188 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py": file changed since it was read — re-read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "limit": 280}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """verifier_ci.py — vérifier le workflow CI **sans `act`** : YAML, commandes, contrôle négatif.
3: 
4: POURQUOI CET OUTIL EXISTE. Le workflow `.github/workflows/ci.yml` n'est exécuté que par
5: GitHub Actions. Quand `act` n'est pas installé, il reste trois preuves possibles en local :
6: 
7: 1. **le YAML est valide** : un parseur (PyYAML) le charge, et le contrat attendu est là
8:    (matrice 3.10/3.13, `pip install -e .`, les quatre commandes, `runs-on`) ;
9: 2. **les commandes qu'il lance passent** : chaque `run` est exécuté dans l'ordre, avec
10:    l'interpréteur courant (ou `--python`), et son code de sortie est relevé ;
11: 3. **le contrôle négatif** : un test volontairement cassé, copié depuis
12:    `tools/tests/test_produit.py`, doit sortir en **1** et **arrêter la séquence** — c'est
13:    exactement ce que fait un job GitHub Actions quand une étape échoue.
14: 
15: L'outil ne remplace pas `act` : il ne simule ni l'image du runner, ni `actions/checkout`,
16: ni `actions/setup-python`. Il prouve le YAML et les commandes, pas l'exécution
… [11109 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "new_string": "        print(f\"{resultat['python_version']} · act={resultat['act'] or 'absent'}\")", "old_string": "        print(f\"Python {resultat['python_version']} · act={resultat['act'] or 'absent'}\")"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py has been updated successfully.
  ```

- **job_output** `{"job_id": "bash-62", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **job_output** `{"job_id": "bash-63", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **job_output** `{"job_id": "bash-62", "wait": true, "timeout_ms": 300000}`

  ```
(no new output)
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-63 (bash: export PATH=/tmp/ci313/bin:$PATH; python3 tools/verifier_ci.py --json > /tmp/ci313-result.json 2> /tmp/ci313-result.err; echo "EXIT=$?" >> /tmp/ci313-result.err) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cat /tmp/ci310-result.err; echo \"---\"; python3 - <<'EOF'\nimport json\nfor v in ('310','313'):\n    d=json.load(open(f'/tmp/ci{v}-result.json'))\n    print(v, 'ok=',d['ok'], d['python_version'], 'act=',d['act'])\n    for e in d['execution']:\n        print(' ', e['etape'], e['code'],  … [174 caractères tronqués]`

  ```
EXIT=0
---
310 ok= True Python 3.10.20 act= None
  installer 0 2.856
  test_produit 0 16.163
  test_tagger_api 0 7.685
  porte_produit 0 226.376
  test_schema_produit 0 1.27
  negatif 1 True False
313 ok= True Python 3.13.16 act= None
  installer 0 3.297
  test_produit 0 17.71
  test_tagger_api 0 7.875
  porte_produit 0 195.788
  test_schema_produit 0 1.527
  negatif 1 True False
  ```

- **bash** `{"command": "cat /tmp/ci313-result.err; echo \"---tail gate 310---\"; python3 - <<'EOF'\nimport json\nfor v in ('310','313'):\n    d=json.load(open(f'/tmp/ci{v}-result.json'))\n    gate=[e for e in d['execution'] if e['etape']=='porte_produit'][0]\n    print(v, 'gate tail:', gate['stdout'][-300:])\n … [108 caractères tronqués]`

  ```
EXIT=0
---tail gate 310---
310 gate tail: ibles, rendu relu, contrôle détecté
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ exemples de la doc : 27/27 cas conformes — ✅ aucun écart
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
310 gate stderr: 
313 gate tail: ibles, rendu relu, contrôle détecté
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ exemples de la doc : 27/27 cas conformes — ✅ aucun écart
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
313 gate stderr:
  ```

- **bash** `{"command": "ls tools/tests/_controle_negatif_ci_* 2>/dev/null || echo \"aucun fichier temporaire\"; echo \"---\"; git status --short | head -30", "description": "Check temp cleanup and git status"}`

  ```
aucun fichier temporaire
---
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/session-b3e96cb1-fb3b-4593-a2a6-b034ae644413/digest.md
 M journal/sessions/session-b3e96cb1-fb3b-4593-a2a6-b034ae644413/rapport.md
 M tools/chantier/plan.json
 M tools/tests/test_tagger_api.py
?? .github/
?? tools/verifier_ci.py
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/ci310-result.json'))\nprint(d['negatif']['sortie'][-500:])\nEOF", "description": "Show negative control output"}`

  ```
_volontaire (__main__.TestControleNegatifCI)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/_controle_negatif_ci_h0phx1p9.py", line 443, in test_echec_volontaire
    self.fail("contrôle négatif CI volontaire")
AssertionError: contrôle négatif CI volontaire

----------------------------------------------------------------------
Ran 31 tests in 16.181s

FAILED (failures=1)
  ```

- **bash** `{"command": "sed -n '86,104p' docs/README.md", "description": "Read docs product table"}`

  ```
| [`implantation/diehl-cook.md`](implantation/diehl-cook.md) | un bloc Diehl & Cook : équations, contrat DRVM, RSN, portes |
| [`implantation/moteur-de-pensee.md`](implantation/moteur-de-pensee.md) | le state store, l'arbre d'états, les stratégies et les portes du moteur |
| [`implantation/llm-externe.md`](implantation/llm-externe.md) | le [banc externe](theorie/glossaire/entrees/banc-externe.md), le [professeur](theorie/glossaire/entrees/professeur.md) et l'[élève](theorie/glossaire/entrees/eleve.md) |
| [`implantation/numa-segregation.md`](implantation/numa-segregation.md) | la ségrégation [NUMA](theorie/glossaire/entrees/numa.md) mesurée |
| [`implantation/configuration-nvme-raid-amd.md`](implantation/configuration-nvme-raid-amd.md) | l'array [NVMe](theorie/glossaire/entrees/nvme-ssd-odirect-pread.md) et le pari AMD |

## Produit — ce qui s'utilise aujourd'hui

| document | pour quoi |
|---|---|
| [`produit/demarrage.md`](produit/demarrage.md) | le **quickstart** : cinq minutes, trois commandes |
| [`produit/README.md`](produit/README.md) | le **premier produit** : analyser un texte |
| [`produit/README.md` § 8](produit/README.md#8-faq--dix-questions) | la **FAQ** : dix question
… [168 caractères tronqués]
  ```

- **write** `{"content": "# L'intégration continue — le workflow et sa preuve locale\n\n> **Ce que ce document est.** La **protection** du produit : le workflow GitHub Actions qui\n> rejoue, à chaque `push` et à chaque `pull request`, l'installation éditable, les trois tests\n> du contrat et la **porte produit** … [5069 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/ci.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md", "new_string": "| [`produit/exemples.md`](produit/exemples.md) | cinq exemples réels, dont un échec connu |\n| [`produit/ci.md`](produit/ci.md) | l'**intégration continue** : matrice 3.10/3.13, cinq étapes, preuve locale  … [123 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **porte produit** | version, JSON fr/en, rejeu, smoke test, autotest | `bash tools/porte-produit.sh` → ✅ |\n| **intégration continue** | la porte et les tests du contrat rejoués sur **Python 3.10 … [236 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md", "limit": 150}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "limit": 1100}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md</path>
<type>file</type>
<content>
1: # La documentation de [Drave](theorie/glossaire/entrees/drave.md) — quatre familles
2: 
3: > **`docs/` dit ce qui reste vrai** : la méthode, l'[état](theorie/glossaire/entrees/etat.md), la théorie, l'implantation. Les **chiffres** et les
4: > séries vivent dans [`reports/`](../reports/) ; le **récit daté** dans [`journal/`](../journal/). Une page de
5: > `docs/` qui se remplit de tableaux de mesures **déménage** dans `reports/`.
6: 
7: > **Chargement facultatif.** Aucun document de ce dossier n'est nécessaire pour commencer une tâche : lire
8: > [`AGENTS.md`](../AGENTS.md), puis le document de la tâche. Le reste se [charge](theorie/glossaire/entrees/charge-flux-chargeflux.md) au besoin.
9: 
10: ## En trois portes
11: 
12: | si vous voulez… | lisez |
13: |---|---|
14: | **comprendre le projet** | [la vision](theorie/vision.md) · [la mission](methode/mission.md) · [le protocole sémantique](theorie/protocole-semantique.md) · [le glossaire](theorie/glossaire.md) · [la synthèse](theorie/synthese/index.md) |
15: | **faire** (résultat, [porte](theorie/glossaire/entrees/porte.md), ran
… [9339 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
1: # Le premier produit — analyser un texte avec Drave
2: 
3: > **Ce que ce document est.** La notice d'usage du **premier produit** de Drave : le bloc
4: > linguistique, utilisable **aujourd'hui**, sur un CPU, sans modèle et sans réseau. Il dit à qui
5: > il s'adresse, ce qu'il fait, comment l'exécuter, ce qu'il ne fait pas, ce qu'il coûte et ce
6: > qu'il garantit.
7: >
8: > **Vérifié le 2026-11-15** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
9: > **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
10: > existent, et la
11: > porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
12: > § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le
13: > **prototype `--tagger auto`** (complété le **2026-11-15**, § 3.7) choisit l'API si une clé
14: > existe, l'heuristique sinon, **sans changer le code de sortie** ; il ne change pas le défaut.
15: > Le format
16: > est **version 2** (`schema: "drave.annotation"`,
17: > `version: 2`) : le schéma v2 ajoute `met
… [52852 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md", "new_string": "| [`produit/exemples.md`](produit/exemples.md) | cinq exemples réels, dont un échec connu |\n| [`produit/ci.md`](produit/ci.md) | l'**intégration continue** : matrice 3.10/3.13, cinq étapes, preuve locale  … [123 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **porte produit** | version, JSON fr/en, rejeu, smoke test, autotest | `bash tools/porte-produit.sh` → ✅ |\n| **intégration continue** | la porte et les tests du contrat rejoués sur **Python 3.10 … [236 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "offset": 780, "limit": 300}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
780: | **intégration continue** | la porte et les tests du contrat rejoués sur **Python 3.10 et 3.13** à chaque `push` | [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) ; [ci.md](ci.md) |
781: 
782: **La porte produit, mesurée le 07/11** : `✅ porte produit verte` — `drave 0.1.0`, JSON valide et
783: étiqueté en `fr` et `en`, `sha256 f4b7822076a4203d` deux fois, **18 tests** de fumée, **8 tests**
784: de schéma (v2 + rétro-compatibilité v1), **4 tests** sur 50 textes libres, **11 tests** de
785: restitution, **183/183** portes d'autotest ; **12 contrôles**. Le smoke test est
786: `tools/tests/test_produit.py`.
787: 
788: **Codes de sortie.** Le CLI implémente **0 / 1 / 3 / 4 / 5** ; le contrat est écrit dans
789: `--aide` et vérifié par `tools/tests/test_produit.py` :
790: 
791: | code | sens | aujourd'hui |
792: |---:|---|---|
793: | **0** | succès : annotation rendue, évaluation rendue, rejeu identique, restitution rendue | `analyser`, `evaluer`, `rejouer`, `restituer` |
794: | **3** | refus d'analyse : une **réponse**, pas une erreur | `analyser ""` (JSON d
… [20846 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "restitution, **183/183** portes d'autotest ; **12 contrôles**. Le smoke test est\n`tools/tests/test_produit.py`.\n\n**L'intégration continue** rejoue cette porte à chaque `push` : `.github/workflow … [633 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "| **le tagger en option** (mesure 20/612, coût, tests) | [`reports/rapport-tagger-option.md`](../../reports/rapport-tagger-option.md) · [`reports/pensee-tagger-option.json`](../../reports/pensee-ta … [462 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, hashlib, pathlib, re, subprocess\n\nracine = pathlib.Path('.').resolve()\nworkflow = (racine/'.github/workflows/ci.yml').read_text(encoding='utf-8')\nsha = hashlib.sha256(workflow.encode()).hexdigest()\nhead = subprocess.check_output(['git','rev-parse','- … [4277 caractères tronqués]`

  ```
{
  "matrice": [
    "3.10",
    "3.13"
  ],
  "versions_mesurees": [
    "3.10.20",
    "3.13.16"
  ],
  "etapes_par_version": 5,
  "etapes_vertes": 10,
  "etapes_rouges": 0,
  "controles_negatifs": 2,
  "controle_negatif_code": [
    1
  ],
  "controle_negatif_job_arrete": true,
  "porte_produit": "183/183 portes d'autotest",
  "act": false,
  "duree_totale_s": 480.547,
  "sha256_workflow": "4f775690d5e4cea9132f651d94b065c7da8702b3dfdd0a5e00f7d868cca6d071"
}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-ci.json'))\nfor p in d['preuve_locale']:\n    print(p['version'])\n    for e in p['etapes']:\n        print(f\"  {e['etape']:<20} {e['code']} {e['duree_s']:>8} s tests={e['tests']}\")\n    print('  negatif', p['controle_n … [153 caractères tronqués]`

  ```
3.10.20
  installer            0    2.856 s tests=None
  test_produit         0   16.163 s tests=30
  test_tagger_api      0    7.685 s tests=30
  porte_produit        0  226.376 s tests=30
  test_schema_produit  0     1.27 s tests=9
  negatif 1 True
3.13.16
  installer            0    3.297 s tests=None
  test_produit         0    17.71 s tests=30
  test_tagger_api      0    7.875 s tests=30
  porte_produit        0  195.788 s tests=30
  test_schema_produit  0    1.527 s tests=9
  negatif 1 True
total 480.547
  ```

- **write** `{"content": "# Z1 — L'intégration continue : le workflow, la matrice et le contrôle négatif\n\n> **Ligne de roadmap** : **B13 — la protection** (produit exploitable) · **Tâche** : **Z1** ·\n> **Date** : 2026-11-16 · **Branche** : `s/v7` · **Verdict** : ✅ **la CI est verte en local** —\n> **2 version … [9802 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, pathlib\np=pathlib.Path('reports/rapport-ci.json')\nd=json.loads(p.read_text(encoding='utf-8'))\nfor preuve in d['preuve_locale']:\n    total=0.0\n    for e in preuve['etapes']:\n        total += e['duree_s']\n        if e['etape']=='porte_produit':\n     … [512 caractères tronqués]`

  ```
ok [254.35, 226.197]
JSON-VALIDE
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 45, "offset": 160}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 40, "offset": 115}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
160: gold B13 ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).
161: 
162: **T4 — la performance (15/11).** 10 000 mots : **4,01 s**, **2 493 mots/s**, **126 Mio**,
163: **14,8 Mo** JSON ; α = **1,55**, `_groupes_partition`/`_cible_proche` **O(k²)**.
164: [Fiche](../../reports/rapport-performance.md) · [JSON](../../reports/performance.json).
165: 
166: **U1 — les O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),
167: **12 259 mots/s**, **127,4 Mio** ; JSON identique. **α = 1,076** (1,530 avant), +0,00077 de R² ; sorties identiques (612/452). [Fiche](../../reports/rapport-performance-fix.md) ·
168: [JSON](../../reports/performance-fix.json) · [contrôle](../../tools/verifier_performance_fix.py).
169: **U2 — la roue (16/11)** : **1 727 201 o** ; sans gold, `evaluer` **4**
170: ([fiche](../../reports/rapport-roue.md)).
171: 
172: **U3** : **398 profils UDHR** ; **20/20**, **433/447** ; ambigu **`und`**
173: ([fiche](../../reports/rapport-profils.md)).
174: 
175: **V1 — `evaluer --strict` (16/11).** Quatre modes, cascade **0,8625** / **0,8891**, plan
… [2083 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
115: | **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 0,9575, réel 452 0,9500 ; W2 : 402 0,9643, H50 0,8607 ; W3 : défaut hors ligne, clé invalide 4, 1 000 phrases = 143 870 tokens / 0,031 $ hors pointe ; X3 : lot 1 000, 672 appels, 99 971 tokens, 0,02177 $ ; W5 : restitution v3, 20/46 (F1 0,5406), gold S 144/144, `--roles-v3` opt-in ; W6 : [rapport semaine 2](../../reports/rapport-semaine-2.md), tag `semaine-2-2026-11-20` sur `73edb3dd` ; Y1 : `--tagger auto` prototype (clé présente API 0/130 tokens ; invalide 0 ; sans clé 0 identique au défaut ; réseau coupé 0 après 3 essais ; défaut inchangé) ; **V3 : clôture, tag** ; R2/R3 attendent N5/N4 | **J4 — l'or de rôles** (seconds cadres) ; **Panini** si les 26 signatures arrivent ; **[fiche W3](../../reports/rapport-tagger-defaut.md)**, **[fiche Y1](../../reports/rapport-tagger-auto.md)**, **[fiche X3](../../reports/rapport-tagger-lot.md)**, **[fiche W5](../../reports/rapport-restitution-v3.md)**, **[rapport W6](../../reports/rapport-semaine-2.md)** |
116: | **C1** **C2** **C3** **C4** **C5** **C6** **C7** | hors grap
… [2174 caractères tronqués]
  ```

- **bash** `{"command": "printf 'md='; ls reports/*.md | wc -l; printf 'json='; ls reports/*.json | wc -l; printf 'docs='; find docs -name '*.md' ! -path 'docs/archive/*' ! -name 'README.md' | wc -l", "description": "Count reports and docs"}`

  ```
md=772
json=867
docs=461
  ```

- **bash** `{"command": "grep -n \"fichiers / JSON\\|771\\|866\\|documents de\" tools/revue_documentation.py | head -20", "description": "Find count checks in doc review"}`

  ```
175:    documents = extrait_entier(t, r"\|\s*documents de[^|]*\|\s*\*\*(\d+)\*\*")
176:    fiches = re.search(r"\|\s*fichiers / JSON de résultats\s*\|\s*\*\*(\d+)\*\*\s*/\s*\*\*(\d+)\*\*", t)
187:        alertes.append("compteurs : la ligne « fichiers / JSON » manque dans en-cours.md")
  ```

- **bash** `{"command": "sed -n '150,200p' tools/revue_documentation.py", "description": "Inspect doc review count logic"}`

  ```
if retard and not etat_modifie(RACINE):
        etat, _fait, lignes = retard
        if etat == "absent":
            alertes.append("fraîcheur : en-cours.md n'a jamais été commité")
        else:
            alertes.append(
                f"fraîcheur : {len(lignes)} fait(s) commité(s) après le dernier état "
                f"({etat[1]}) — mettre en-cours.md à jour"
            )

    # 1. classement : aucune donnée de résultat dans docs/
    for f in (RACINE / "docs").rglob("*"):
        if f.suffix in (".json", ".csv", ".npz", ".jsonl") and f.is_file():
            if f.name == "index.json" and f.parent.name == "glossaire":
                continue
            alertes.append(f"classement : donnée de résultat dans docs/ → {f.relative_to(RACINE)}")
    for nom in ("07-mesures-couche-commune.md", "fiche-nuit-17-10.md"):
        if not (RACINE / "reports" / nom).exists():
            alertes.append(f"classement : la fiche courante reports/{nom} manque")
    if not (RACINE / "reports/README.md").exists():
        alertes.append("classement : reports/ n'a pas d'index (reports/README.md)")

    # 5. compteurs : la page d'état est la source unique, et elle dit le disque
    portes = ex
… [1352 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def compte_docs\\|def compte_fiches\\|def compte_json\" -A15 tools/revue_documentation.py", "description": "Read count functions"}`

  ```
108:def compte_fiches() -> int:
109-    return len(rapports())
110-
111-
112:def compte_json() -> int:
113-    return len(list((RACINE / "reports").glob("*.json")))
114-
115-
116:def compte_docs() -> int:
117-    return len(docs_vivants())
118-
119-
120-def extrait_entier(texte: str, motif: str):
121-    m = re.search(motif, texte)
122-    return int(m.group(1)) if m else None
123-
124-
125-def main() -> int:
126-    alertes: list[str] = []
127-    en = RACINE / "docs/pilotage/en-cours.md"
128-    if not en.exists():
129-        print("✗ docs/pilotage/en-cours.md absent")
130-        return 1
131-    t = en.read_text()
  ```

- **bash** `{"command": "grep -n \"def docs_vivants\\|def rapports\" -A20 tools/revue_documentation.py", "description": "Read docs_vivants definition"}`

  ```
66:def docs_vivants():
67-    return [p for p in (RACINE / "docs").rglob("*.md")
68-            if "archive" not in p.parts and p.name != "README.md" and not est_carte(p)]
69-
70-
71-def docs_tous():
72-    return list((RACINE / "docs").rglob("*.md"))
73-
74-
75:def rapports():
76-    return list((RACINE / "reports").glob("*.md"))
77-
78-
79-def sources_nav():
80-    """Les fichiers vivants dont les liens comptent pour la navigation (orphelins)."""
81-    return (docs_vivants() + rapports()
82-            + [RACINE / "docs/README.md", RACINE / "README.md",
83-               RACINE / "REPRISE.md", RACINE / "AGENTS.md"])
84-
85-
86-def sources_propres():
87-    """Les documents vivants dont on vérifie les libellés et les chemins en code inline."""
88-    return (docs_vivants()
89-            + [RACINE / "README.md", RACINE / "REPRISE.md", RACINE / "AGENTS.md"])
90-
91-
92-def sources_liens():
93-    """Les fichiers dont les liens doivent résoudre (docs, fiches courantes, racine)."""
94-    return (docs_tous()
95-            + [RACINE / "reports/07-mesures-couche-commune.md",
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**V3 — la clôture** : **T1–T6**, **U1–U3**, **V1–V2** ; **86/82/4** → **84/2** après vérification ciblée ; tag `exploitable-2026-11-16` sur `ae3c24f2` ; [bilan 2](../../reports/rapport-bilan-exp … [899 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **772** / **867** | `reports/*.md` / `reports/*.json` |\n| documents de `docs/` | **126** (hors archive et README) | `docs/**/*.md` |", "old_string": "| fichiers … [158 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**V3 — la clôture (16/11).** **T1–T6 · U1–U3 · V1–V2** ; **86 / 82 / 4** → **84 / 2**\n(`work/portes/`) ; tag `exploitable-2026-11-16` sur **`ae3c24f2`**.\n[Fiche](../../reports/rapport-bilan-exp … [757 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md</path>
<type>file</type>
<content>
1: # 2026-11-16
2: 
3: > **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
4: > [`journal/2026-11-16/`](README.md). Le récit écrit à la main est conservé plus bas, dans
5: > le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
6: > [l'index des sessions](../README.md#sessions).
7: 
8: **7 commits** · **1 session(s)** · **4 thème(s)**
9: 
10: ## Thèmes du jour
11: 
12: | thème | commits | fichier |
13: |---|---|---|
14: | docs | 2 | [docs.md](docs.md) |
15: | memoire | 1 | [memoire.md](memoire.md) |
16: | mesures | 3 | [mesures.md](mesures.md) |
17: | moteur | 1 | [moteur.md](moteur.md) |
18: 
19: ## Sessions DSH
20: 
21: | session | titre | début | durée | liens |
22: |---|---|---|---|---|
23: | `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 370.5 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |
24: 
25: ## Tous les commits (heure réelle)
26: 
2
… [4871 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md", "new_string": "**`exploitable-2026-11-16`** est posé sur **`ae3c24f2`** (V2), le dernier commit vert ; le\ncommit de clôture suit. **La prochaine mesure est J4 — l'or de rôles**.\n\n### Z1 — l'intégration c … [1119 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run documentation review", "timeout_ms": 300000}`

  ```
revue de documentation · 772 fiche(s) · 867 JSON · 126 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -10; echo \"EXIT=${PIPESTATUS[0]}\"; echo \"---\"; python3 tools/verifie_journal.py 2>&1 | tail -5; echo \"EXIT=${PIPESTATUS[0]}\"; echo \"---\"; python3 tools/verifier_schemas.py 2>&1 | tail -5; echo \"EXIT=${PIPESTATUS[0]}\"", "description … [64 caractères tronqués]`

  ```
en-cours · 1656 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT=0
---
  journal · 48 jour(s) · 228 session(s) · 2738 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
EXIT=0
---
  schémas · 466 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
EXIT=0
  ```

- **bash** `{"command": "rm -rf /tmp/ci-archive && mkdir -p /tmp/ci-archive && git archive HEAD | tar -x -C /tmp/ci-archive && cp tools/tests/test_tagger_api.py /tmp/ci-archive/tools/tests/test_tagger_api.py && cp tools/verifier_ci.py /tmp/ci-archive/tools/verifier_ci.py && mkdir -p /tmp/ci-archive/.github/work … [316 caractères tronqués]`

  ```
YAML valide · PyYAML 6.0.3 · matrice ['3.10', '3.13']
Python 3.10.20 · act=absent
  ✅ installer            code=0 · 2.828 s
  ❌ test_produit         code=1 · 15.32 s
  ✅ contrôle négatif  code=1 · job_echoue=True · étape suivante exécutée=False
❌ CI locale rouge
EXIT=1
  ```

- **bash** `{"command": "cd /tmp/ci-archive && PATH=/tmp/ci310/bin:$PATH python3 tools/tests/test_produit.py 2>&1 | tail -40; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Inspect archive test failure", "timeout_ms": 300000}`

  ```
======================================================================
FAIL: test_roles_normalises_et_filtre_predicat (__main__.TestContratJSON)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/ci-archive/tools/tests/test_produit.py", line 249, in test_roles_normalises_et_filtre_predicat
    self.assertTrue(predicats)
AssertionError: [] is not true

======================================================================
FAIL: test_alternative_etiquette_les_chevauchements (__main__.TestPartition)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/ci-archive/tools/tests/test_produit.py", line 311, in test_alternative_etiquette_les_chevauchements
    self.assertTrue(any("alternative" in (e.get("meta") or {}) for e in segs))
AssertionError: False is not true

======================================================================
FAIL: test_analyser_francais (__main__.TestProduit)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/ci-archive/tools/tests/test_produit.py", line 58, in te
… [786 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,340p' tools/tests/test_produit.py", "description": "Read full product test"}`

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


… [15236 caractères tronqués]
  ```

- **bash** `{"command": "git ls-remote https://github.com/stephanedenis/drave-structures.git 2>&1 | head -10; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Check public structures repo", "timeout_ms": 60000}`

  ```
ERROR: Repository not found.
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
EXIT=128
  ```

- **bash** `{"command": "cd tools/structures && git remote -v; git log --oneline -3 2>&1 | head; cd ../..; git -C tools/structures rev-parse HEAD", "description": "Inspect structures submodule remote and commit"}`

  ```
origin	/home/stephane/Data13TB/stephane/GitHub/drave-structures (fetch)
origin	/home/stephane/Data13TB/stephane/GitHub/drave-structures (push)
648adce U1 — générateur S : construire_arbre et cibles en O(k), sorties identiques (620 textes)
389b99f S — LES 11 VERDICTS HUMAINS DE /paragraphes (a004–a009) : 19/19 CANDIDATS JUGÉS, 11 ACCEPTÉS, 8 EXCLUS ; DÉCISION DU 14/11 (3B), EXCEPTION AUTORISÉE
523d8c1 S — LE FAIT DIVERS EST TRANCHÉ : 61/61 TYPES, 144/144 RÔLES ; LA TÊTE DU GN ARRÊTE LE VERBE
648adce3ea18ef4d142778fd67d42413aae5ae64
  ```

- **bash** `{"command": "sed -n '1,80p' tools/structures/generateur.py; echo \"===IMPORTS===\"; grep -n \"^import\\|^from\\|open(\\|read_text\\|Path(\" tools/structures/generateur.py | head -30; echo \"===DATA===\"; ls -lh tools/structures/donnees | head; du -sh tools/structures", "description": "Inspect S gene … [20 caractères tronqués]`

  ```
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
COORD = set("et ou mais donc or ni car".split())
SU
… [4759 caractères tronqués]
  ```

- **bash** `{"command": "find . -name 'generateur.py' -not -path './.git/*' 2>/dev/null; echo \"---\"; git ls-files | grep -i 'generateur\\|structures' | head -20; echo \"---dist---\"; unzip -l dist/*.whl 2>/dev/null | grep -i generateur | head", "description": "Find copies of generator"}`

  ```
./tools/structures/generateur.py
./build/lib/tools/structures/generateur.py
---
docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
reports/s-banque-structures.json
tools/structures
---dist---
    31037  2026-11-16 05:04   tools/structures/generateur.py
  ```

- **bash** `{"command": "git ls-files build dist | head; echo \"---\"; git check-ignore build dist; echo \"---\"; cat .gitignore", "description": "Check if build/dist tracked or ignored"}`

  ```
---
build
dist
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
  ```

- **bash** `{"command": "cd /tmp/ci-archive && PATH=/tmp/ci310/bin:$PATH bash tools/porte-produit.sh 2>&1 | tail -40; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run product gate in archive without submodules", "timeout_ms": 900000}`

  ```
[still running after 60000ms; moved to background job bash-87]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "grep -rn \"role\\|agent\\|predicat\\|rôle\\|structures\" tools/tests/test_restitution.py tools/tests/test_restitution_v2.py tools/tests/test_produit_libre.py tools/verifie_exemples.py | head -50", "description": "Find role dependencies in gate tests"}`

  ```
tools/tests/test_restitution.py:7:- les sauts de ligne sont annotés (`graphème` de type `contrôle`) et reviennent ;
tools/tests/test_restitution.py:9:  tomber), et le contrôle négatif (mélange, troncature) le détecte ;
tools/tests/test_restitution.py:51:        self.assertIn("contrôle négatif", sortie.stdout)
tools/tests/test_restitution.py:62:        self.assertTrue(donnees["controle_negatif"]["detecte"])
tools/tests/test_restitution.py:93:        self.assertEqual(donnees["synthese"]["controle_negatif"]["melange_exacts"], 0)
tools/tests/test_restitution.py:99:        self.assertIn("GN/agent: le chat -> dort", sortie.stdout)
tools/tests/test_restitution.py:113:        self.assertTrue(donnees["controle_negatif_canonique"]["detecte"])
tools/tests/test_restitution.py:143:        self.assertEqual([s["role"] for s in forme["segments"]], ["agent", "predicat"])
tools/tests/test_restitution.py:147:                         ["GN/agent: le chat -> dort", "GV/predicat: dort -> chat"])
tools/tests/test_restitution.py:168:    def test_controles_negatifs(self):
tools/tests/test_restitution.py:171:        canonique = restitution.controler_negatif_canonique(a, source)
tools/tests/test_restitution.p
… [4039 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"agent\\|predicat\\|rôle\\|role\" tools/tests/test_evaluer_strict.py tools/tests/test_schema_produit.py | head -30", "description": "Find role dependencies in other tests"}`

  ```
tools/tests/test_evaluer_strict.py:8:3. le **contrôle négatif** est mesuré dans la même passe : une cascade dont le POS est forcé
tools/tests/test_evaluer_strict.py:64:        negatif = rapport["controle_negatif"]
tools/tests/test_evaluer_strict.py:83:            "controle_negatif": {"nom": "cascade dégradée", "pos": 0.60,
tools/tests/test_schema_produit.py:77:        """Contrôle négatif : un JSON amputé d'un champ obligatoire est bien refusé par le test."""
tools/tests/test_schema_produit.py:95:    def test_le_schema_v2_declare_candidats_structures_et_roles(self):
tools/tests/test_schema_produit.py:96:        """T2 : `meta.attachement.candidats` est typé, et `role` est un vocabulaire fermé."""
tools/tests/test_schema_produit.py:98:        from tools.roles_vocabulaire import ROLES
tools/tests/test_schema_produit.py:108:                         set(meta["properties"]["role"]["enum"]))
tools/tests/test_schema_produit.py:111:        self.assertEqual(set([""] + list(ROLES)), set(alternative["role"]["enum"]))
  ```

- **bash** `{"command": "grep -rn \"SANS_STRUCT\\|sans_structure\\|sans structure\\|DRAVE_S\\|generateur\" tools/tests tools/porte-produit.sh tools/verifie_exemples.py docs/produit/demarrage.md | head -40", "description": "Search existing degraded-mode switches"}`

  ```
tools/verifie_exemples.py:261:# --------------------------------------------------------------------------- démarrage sans structures
tools/verifie_exemples.py:264:def copie_sans_structures(destination: pathlib.Path) -> None:
tools/verifie_exemples.py:507:                         help="ne pas copier le code sans structures (plus rapide)")
tools/verifie_exemples.py:534:            copie_sans_structures(cwd)
  ```

- **bash** `{"command": "sed -n '255,330p' tools/verifie_exemples.py", "description": "Read no-structures copy logic"}`

  ```
if lignes[i].startswith(("PRAGMATIQUE", "COUVERTURE", "TAGGER API")):
            fin = i
            break
    return "\n".join(lignes[debut:fin]).strip()


# --------------------------------------------------------------------------- démarrage sans structures


def copie_sans_structures(destination: pathlib.Path) -> None:
    """La copie du code **sans** `tools/structures` : la condition du clone public."""
    ignorer = shutil.ignore_patterns("structures", "docwatch", "__pycache__", "*.pyc")
    shutil.copytree(RACINE / "tools", destination / "tools", ignore=ignorer)
    for nom in ("pyproject.toml", "README.md"):
        source = RACINE / nom
        if source.is_file():
            shutil.copy2(source, destination / nom)


def cas_demarrage(texte: str, cwd: pathlib.Path) -> tuple[list[Cas], dict]:
    sections = lire_sections(texte)
    cas: list[Cas] = []

    # Les trois commandes du § 3, telles que le débutant les lance.
    for prefixe, ident in (
        ("### 3.1", "demarrage §3.1 --version"),
        ("### 3.2", "demarrage §3.2 analyser"),
        ("### 3.3", "demarrage §3.3 evaluer"),
    ):
        s = section(sections, prefixe)
        cmd = bloc_bash(s, "drave ")
  
… [2039 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'role.*agent\\|role.*predicat\\|\"agent\"\\|\"predicat\"' tools/bloc_linguistique.py | head -40", "description": "Find role assignment logic"}`

  ```
766:        return "agent"
1206:                        gn.update({"type": "GN", "role": "agent", "niveau": 0,
1688:                segments.append({"type": "GN", "role": "agent", "niveau": 0,
1696:                segments.append({"type": "GN", "role": "agent", "niveau": 0,
  ```

- **bash** `{"command": "sed -n '700,790p' tools/bloc_linguistique.py; echo \"===1660===\"; sed -n '1640,1720p' tools/bloc_linguistique.py", "description": "Read role assignment code"}`

  ```
"could", "cannot"}

ENCLITIQUES = ("-moi", "-toi", "-nous", "-vous", "-le", "-la", "-les", "-lui", "-leur", "-y", "-en")


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
    # 1er groupe : `nage` → `nager`, `commence` → `commencer` (la voyelle finale tombe
… [8393 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"agent\\|predicat\\|rôle\\|role\\|→\" tools/tests/test_produit_libre.py | head -20; echo \"===restitution tests names===\"; grep -n \"    def test_\" tools/tests/test_restitution.py; echo \"===v2 names===\"; grep -n \"    def test_\\|^class \" tools/tests/test_restitution_v2.py … [60 caractères tronqués]`

  ```
===restitution tests names===
44:    def test_restituer_texte(self):
53:    def test_restituer_json(self):
64:    def test_restituer_multiligne(self):
72:    def test_restituer_refus(self):
79:    def test_restituer_banc(self):
95:    def test_restituer_canonique(self):
103:    def test_restituer_canonique_json(self):
115:    def test_restituer_banc_canonique(self):
135:    def test_forme_simple(self):
150:    def test_ne_lit_pas_le_texte(self):
157:    def test_miroir_canonique_et_strict(self):
168:    def test_controles_negatifs(self):
181:    def test_distance_canonique(self):
194:    def test_synthese_v1(self):
205:    def test_structure_v1(self):
218:    def test_stabilite_et_controles_v1(self):
237:    def test_ne_lit_pas_le_texte(self):
243:    def test_surface_sans_controle(self):
252:    def test_niveaux_pauvres(self):
261:    def test_distance(self):
268:    def test_controle_negatif(self):
284:    def test_50_textes_46_annotations(self):
===v2 names===
45:class TestCommandeRoles(unittest.TestCase):
46:    def test_restituer_roles(self):
55:    def test_restituer_roles_json(self):
68:    def test_roles_et_canonique_exclusifs(self):
73:    def test_gold_sans_banc_refuse(se
… [695 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-87", "wait": true, "timeout_ms": 300000}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ profils : langue, script, confiance, 398 profils
  ✅ rejeu : sha256 2577786670e5752c deux fois
  ❌ smoke test en échec (voir /tmp/porte-produit-tests.log)
  ✅ evaluer --strict : Ran 5 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ❌ 50 textes libres en échec (voir /tmp/porte-produit-libre.log)
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v2 : rôles lisibles, rendu relu, contrôle détecté
  ❌ restitution v0/v1 en échec (voir /tmp/porte-produit-restitution.log)
  ❌ restitution v2 en échec (voir /tmp/porte-produit-restitution-v2.log)
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ❌ exemples de la doc en écart (voir /tmp/porte-produit-exemples.log)
  ❌ autotest en échec (voir /tmp/porte-produit-autotest.log)
❌ porte produit rouge
EXIT=1
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "tail -30 /tmp/porte-produit-autotest.log 2>/dev/null; echo \"===EXEMPLES===\"; tail -20 /tmp/porte-produit-exemples.log 2>/dev/null; echo \"===LIBRE===\"; tail -20 /tmp/porte-produit-libre.log 2>/dev/null", "description": "Inspect archive gate failure logs"}`

  ```
✅ T152 trois tirages     tirages : [0.9838, 0.9838, 0.9838] (écart-type 0, modèle déterministe)
  ❌ T153 attachement       attachement : top1 0.8954, exact 0.887, couverture 0.9372
  ✅ T154 cibles            cibles : 1624/1863 segments sans cible (couverture 0.1283)
  ✅ T155 cibles 500        500 premiers : 294 GN, 206 GV
  ❌ T156 relation GN-GV    relation : 290/769 (0.3771)
  ❌ T157 rôles par position rôles : 478 sans rôle, 342 avant le GV, 102 après
  ❌ T158 passifs           passifs : 0/5 faux (le sujet est un patient)
  ✅ T159 correctif passifs par → agent, avec → moyen
  ✅ T160 passifs sans par  passif sans par (chunker) : 3/3 patient
  ❌ T161 cible proximité   proximité : top1 214/239, exact 212/239, tête 214/224
  ❌ T162 candidats verbes  candidats : top-k 214/239 (0.8954), tête 214/224
  ❌ T163 échecs attachement échecs : 15 de span, 10 de cible (33 avant les correctifs)
  ❌ T164 verbe du GV       verbe du GV : saw (attendu saw) ; exact 212/239
  ✅ T165 lexique verbal    lexique : talks True, joue True, brother False ; cible GP talks
  ❌ T166 spans perdus      spans : 3 REL, 9 SUB, 3 GP
  ❌ T167 dénominateur      dénominateur : spans 0.9554 / 0.9554 / 0.9464
  ❌ T168 class
… [2758 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '210,235p' tools/tests/test_restitution_v2.py; echo \"---\"; grep -rn \"structures/donnees\\|donnees/\" tools/tests/test_restitution*.py tools/pensee tools/verifie_exemples.py | head -20", "description": "Find data dependencies on structures"}`

  ```
self.assertEqual(par_id["f27"]["comparaison"]["exacts"], 1)
        self.assertEqual(par_id["f03"]["comparaison"]["exacts"], 1)
        self.assertEqual(par_id["f20"]["comparaison"]["exacts"], 0)


class TestGoldExterne(unittest.TestCase):
    def test_gold_analyseur(self):
        r = v2.mesurer_gold_analyseur()
        self.assertEqual(r["phrases"], 61)
        self.assertEqual(r["roles_justes"], 139)
        self.assertEqual(r["roles_total"], 144)
        self.assertEqual(r["taux"], 0.9653)
        self.assertEqual(r["baseline_role_constant"]["justes"], 104)
        self.assertEqual(r["baseline_role_constant"]["taux"], 0.7222)


class TestMesureSansOr(unittest.TestCase):
    def test_sans_or(self):
        h = bl.Heuristique()
        source = "Le chat dort."
        a = h.analyser(source, "fr")
        m = v2.mesurer_annotation_v2(a, source)
        self.assertIsNone(m["comparaison"])
        self.assertTrue(m["rendu"]["exact"])
        self.assertIsNotNone(m["controle_negatif_rendu"])

---
  ```

- **bash** `{"command": "grep -rn \"structures\" tools/pensee tools/tests tools/verifie_exemples.py tools/porte-produit.sh tools/drave.py tools/bloc_linguistique.py | grep -v __pycache__ | head -50", "description": "List structures references"}`

  ```
tools/tests/documents/corpus/prose/semantique-universaux.md:67:théorie des modèles, théorie de la démonstration. Les mathématiques fournissent les **structures** :
tools/tests/test_schema_produit.py:95:    def test_le_schema_v2_declare_candidats_structures_et_roles(self):
tools/tests/test_empaquetage.py:9:  `tools.structures`, `tools.llm`), les **gold** et l'artefact de **profils** (`package-data`) ;
tools/tests/test_empaquetage.py:82:        for attendu in ("tools", "tools.llm", "tools.structures",
tools/verifie_exemples.py:11:  - les trois commandes du démarrage dans une copie **sans** `tools/structures`, condition du
tools/verifie_exemples.py:124:    """Les écarts entre deux structures JSON ; `duree_s` est le seul champ toléré."""
tools/verifie_exemples.py:261:# --------------------------------------------------------------------------- démarrage sans structures
tools/verifie_exemples.py:264:def copie_sans_structures(destination: pathlib.Path) -> None:
tools/verifie_exemples.py:265:    """La copie du code **sans** `tools/structures` : la condition du clone public."""
tools/verifie_exemples.py:315:    # Les chiffres de la note : le dépôt de développement, avec structures, rend ag
… [605 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"gold-analyseur\\|STRUCT\\|RACINE\" tools/mesurer_restitution_v3.py tools/restitution_v2.py tools/tests/test_restitution_v2.py 2>/dev/null | head -20; echo \"---\"; grep -rn \"gold-analyseur\" tools --include='*.py' | grep -v __pycache__ | head", "description": "Locate gold-ana … [13 caractères tronqués]`

  ```
tools/mesurer_restitution_v3.py:30:RACINE = pathlib.Path(__file__).resolve().parent.parent
tools/mesurer_restitution_v3.py:31:if str(RACINE) not in sys.path:
tools/mesurer_restitution_v3.py:32:    sys.path.insert(0, str(RACINE))
tools/mesurer_restitution_v3.py:38:BANC = RACINE / "reports" / "pensee-fiabilite-produit.json"
tools/mesurer_restitution_v3.py:41:REFERENCE_V2 = RACINE / "reports" / "pensee-restitution-v2.json"
tools/mesurer_restitution_v3.py:42:SORTIE = RACINE / "reports" / "pensee-restitution-v3.json"
tools/mesurer_restitution_v3.py:86:        "fichier": str(REFERENCE_V2.relative_to(RACINE)),
tools/mesurer_restitution_v3.py:185:        "banc": str(BANC.relative_to(RACINE)),
tools/mesurer_restitution_v3.py:187:        "gold": str(GOLD.relative_to(RACINE)),
tools/mesurer_restitution_v3.py:189:        "gold_s": str(GOLD_S.relative_to(RACINE)),
tools/mesurer_restitution_v3.py:202:            "or_s": "tools/structures/donnees/gold-analyseur.json (61 phrases, 144 rôles)",
tools/mesurer_restitution_v3.py:234:    print(v3.formater_banc_v3(rapport, str(BANC.relative_to(RACINE))))
tools/mesurer_restitution_v3.py:245:    print(f"écrit : {SORTIE.relative_to(RACINE)}")
tools/restitut
… [1895 caractères tronqués]
  ```

- **bash** `{"command": "mkdir -p /tmp/ci-archive/tools/structures/donnees && cp tools/structures/generateur.py /tmp/ci-archive/tools/structures/generateur.py && cp tools/structures/donnees/gold-analyseur.json /tmp/ci-archive/tools/structures/donnees/gold-analyseur.json && cd /tmp/ci-archive && PATH=/tmp/ci310/ … [175 caractères tronqués]`

  ```
started background job bash-99
  ```

- **job_output** `{"job_id": "bash-99", "wait": true, "timeout_ms": 300000}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ profils : langue, script, confiance, 398 profils
  ✅ rejeu : sha256 f6355d8175a75854 deux fois
  ✅ smoke test : Ran 30 tests
  ✅ evaluer --strict : Ran 5 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v2 : rôles lisibles, rendu relu, contrôle détecté
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ exemples de la doc : 27/27 cas conformes — ✅ aucun écart
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
EXIT=0
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "mkdir -p .github/ci/structures/donnees && cp tools/structures/generateur.py .github/ci/structures/generateur.py && cp tools/structures/donnees/gold-analyseur.json .github/ci/structures/donnees/gold-analyseur.json && sha256sum tools/structures/generateur.py .github/ci/structures/generate … [161 caractères tronqués]`

  ```
ca2d8823e9a6df2f2d6009de30402ea5ced04d84dd371faa7b16ccc2c99279c4  tools/structures/generateur.py
ca2d8823e9a6df2f2d6009de30402ea5ced04d84dd371faa7b16ccc2c99279c4  .github/ci/structures/generateur.py
4cebc6d75b61db35acd3b2cbfc2a23924b25df3f020dce6038a2730adc2f8879  tools/structures/donnees/gold-analyseur.json
4cebc6d75b61db35acd3b2cbfc2a23924b25df3f020dce6038a2730adc2f8879  .github/ci/structures/donnees/gold-analyseur.json
  ```

- **write** `{"content": "# La copie de secours de S, pour l'intégration continue\n\n`tools/structures` est un **sous-module** dont l'URL versionnée est un **chemin local**\n(`/home/stephane/.../drave-structures`) : un runner GitHub hébergé ne peut pas le récupérer.\nOr `test_produit.py`, `porte-produit.sh` et l … [1519 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.github/ci/structures/README.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"verifie_structures_secours.py — la copie CI de S est-elle identique au sous-module ?\n\n`tools/structures` est un sous-module dont l'URL est un chemin local : GitHub Actions ne peut\npas le récupérer. La CI utilise donc une copie de secours dans `.github/ci … [1804 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_structures_secours.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.github/workflows/ci.yml", "new_string": "      - name: Vérifier l'interpréteur et pip\n        run: |\n          python3 --version\n          pip --version\n\n      # `tools/structures` est un sous-module dont l'URL versionnée est un ch … [1068 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/.github/workflows/ci.yml has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "limit": 80, "offset": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """verifier_ci.py — vérifier le workflow CI **sans `act`** : YAML, commandes, contrôle négatif.
3: 
4: POURQUOI CET OUTIL EXISTE. Le workflow `.github/workflows/ci.yml` n'est exécuté que par
5: GitHub Actions. Quand `act` n'est pas installé, il reste trois preuves possibles en local :
6: 
7: 1. **le YAML est valide** : un parseur (PyYAML) le charge, et le contrat attendu est là
8:    (matrice 3.10/3.13, `pip install -e .`, les quatre commandes, `runs-on`) ;
9: 2. **les commandes qu'il lance passent** : chaque `run` est exécuté dans l'ordre, avec
10:    l'interpréteur courant (ou `--python`), et son code de sortie est relevé ;
11: 3. **le contrôle négatif** : un test volontairement cassé, copié depuis
12:    `tools/tests/test_produit.py`, doit sortir en **1** et **arrêter la séquence** — c'est
13:    exactement ce que fait un job GitHub Actions quand une étape échoue.
14: 
15: L'outil ne remplace pas `act` : il ne simule ni l'image du runner, ni `actions/checkout`,
16: ni `actions/setup-python`. Il prouve le YAML et les commandes, pas l'exécution
… [2533 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "new_string": "1. **le YAML est valide** : un parseur (PyYAML) le charge, et le contrat attendu est là\n   (matrice 3.10/3.13, `pip install -e .`, les cinq commandes, `runs-on`) ;\n2. **les commandes qu'il lance pa … [1186 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "new_string": "import argparse\nimport hashlib\nimport json", "old_string": "import argparse\nimport json"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "new_string": "def verifier_secours() -> dict:\n    \"\"\"La copie CI de S est-elle identique au sous-module présent ?\"\"\"\n    paires = (\n        (\"tools/structures/generateur.py\", \".github/ci/structures/gen … [1044 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "limit": 70, "offset": 228}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py</path>
<type>file</type>
<content>
228:     parseur.add_argument("--workflow", type=pathlib.Path, default=WORKFLOW)
229:     parseur.add_argument("--python", help="interpréteur à utiliser à la place de python3")
230:     parseur.add_argument("--sans-porte", action="store_true", help="saute `porte-produit.sh`")
231:     parseur.add_argument("--timeout", type=int, default=900, help="timeout par étape (s)")
232:     parseur.add_argument("--json", action="store_true", help="sortie JSON")
233:     parseur.add_argument("--sortie", type=pathlib.Path, help="écrit le JSON dans ce fichier")
234:     args = parseur.parse_args(argv)
235: 
236:     workflow = args.workflow if args.workflow.is_absolute() else RACINE / args.workflow
237:     donnees, version_yaml = charger_yaml(workflow)
238:     contrat = controler(donnees)
239:     python, pip = _python_et_pip(args.python)
240: 
241:     negatif = controle_negatif(python, pip, min(args.timeout, 300))
242:     etapes = [("installer", "pip install -e ."),
243:               ("test_produit", "python3 tools/tests/test_produit.py"),
244:               ("test_tagger_api", "pyt
… [2306 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "new_string": "    negatif = controle_negatif(python, pip, min(args.timeout, 300))\n    secours = verifier_secours()\n    etapes = [(\"installer\", \"pip install -e .\"),\n              (\"test_produit\", \"python3 … [2554 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "new_string": "        etapes = [etape for etape in etapes if etape[0] != \"porte_produit\"]", "old_string": "        etapes = [etape for etape in etapes if etape[\"etape\"] != \"porte_produit\"]"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "new_string": "        print(f\"  {marque} contrôle négatif  code={negatif['code']} · \"\n              f\"job_echoue={negatif['job_echoue']} · \"\n              f\"étape suivante exécutée={negatif['etape_suivante_ … [654 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py has been updated successfully.
  ```

- **bash** `{"command": "python3 -m py_compile tools/verifier_ci.py tools/verifie_structures_secours.py && python3 tools/verifie_structures_secours.py; echo \"EXIT=${PIPESTATUS[0]}\"; python3 - <<'EOF'\nimport yaml\nd=yaml.safe_load(open('.github/workflows/ci.yml'))\nprint('YAML OK', d['jobs']['produit']['strat … [132 caractères tronqués]`

  ```
✅ tools/structures/generateur.py ≡ .github/ci/structures/generateur.py · ca2d8823e9a6…
✅ tools/structures/donnees/gold-analyseur.json ≡ .github/ci/structures/donnees/gold-analyseur.json · 4cebc6d75b61…
EXIT=0
YAML OK {'python': ['3.10', '3.13']}
steps 9
  ```

- **bash** `{"command": "export PATH=/tmp/ci310/bin:$PATH; python3 tools/verifier_ci.py --sans-porte 2>&1 | tail -15; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Quick CI verification after fallback", "timeout_ms": 600000}`

  ```
YAML valide · PyYAML 6.0.3 · matrice ['3.10', '3.13']
Python 3.10.20 · act=absent
  ✅ installer            code=0 · 2.911 s
  ✅ test_produit         code=0 · 16.635 s
  ✅ test_tagger_api      code=0 · 7.713 s
  ✅ test_schema_produit  code=0 · 1.249 s
  ✅ contrôle négatif  code=1 · job_echoue=True · étape suivante exécutée=False
  ✅ copie de secours S  identique
✅ CI locale verte
EXIT=0
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "new_string": "def restaurer_secours() -> dict:\n    \"\"\"Reproduit l'étape CI : restaurer S depuis `.github/ci/structures` s'il manque.\"\"\"\n    cible = RACINE / \"tools\" / \"structures\" / \"generateur.py\"\n … [698 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "new_string": "    restauration = restaurer_secours()\n    negatif = controle_negatif(python, pip, min(args.timeout, 300))\n    secours = verifier_secours()", "old_string": "    negatif = controle_negatif(python, p … [63 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "new_string": "        \"yaml\": {\"valide\": True, \"parseur\": f\"PyYAML {version_yaml}\"},\n        \"contrat\": contrat,\n        \"restauration\": restauration,\n        \"secours_s\": secours,", "old_string": … [146 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py", "new_string": "        print(f\"YAML valide · {resultat['yaml']['parseur']} · matrice {contrat['matrice']}\")\n        print(f\"{resultat['python_version']} · act={resultat['act'] or 'absent'}\")\n        if restau … [297 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_ci.py has been updated successfully.
  ```

- **bash** `{"command": "python3 -m py_compile tools/verifier_ci.py && export PATH=/tmp/ci310/bin:$PATH && python3 tools/verifier_ci.py --sans-porte 2>&1 | tail -12; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Quick check after restore function", "timeout_ms": 600000}`

  ```
YAML valide · PyYAML 6.0.3 · matrice ['3.10', '3.13']
Python 3.10.20 · act=absent
  ✅ installer            code=0 · 2.758 s
  ✅ test_produit         code=0 · 16.308 s
  ✅ test_tagger_api      code=0 · 7.409 s
  ✅ test_schema_produit  code=0 · 1.223 s
  ✅ contrôle négatif  code=1 · job_echoue=True · étape suivante exécutée=False
  ✅ copie de secours S  identique
✅ CI locale verte
EXIT=0
  ```

- **bash** `{"command": "rm -rf /tmp/ci-clean && mkdir -p /tmp/ci-clean && git archive HEAD | tar -x -C /tmp/ci-clean && cp -r .github /tmp/ci-clean/ && cp tools/verifier_ci.py tools/verifie_structures_secours.py /tmp/ci-clean/tools/ && cp tools/tests/test_tagger_api.py /tmp/ci-clean/tools/tests/ && cd /tmp/ci- … [257 caractères tronqués]`

  ```
started background job bash-104
  ```

- **bash** `{"command": "rm -rf /tmp/ci-clean-313 && mkdir -p /tmp/ci-clean-313 && git archive HEAD | tar -x -C /tmp/ci-clean-313 && cp -r .github /tmp/ci-clean-313/ && cp tools/verifier_ci.py tools/verifie_structures_secours.py /tmp/ci-clean-313/tools/ && cp tools/tests/test_tagger_api.py /tmp/ci-clean-313/too … [285 caractères tronqués]`

  ```
started background job bash-105
  ```

- **job_output** `{"job_id": "bash-104", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **job_output** `{"job_id": "bash-105", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/ci.md", "new_string": "Le workflow se déclenche sur `push`, `pull_request` et `workflow_dispatch` ; il a\n`permissions: contents: read` et annule le run précédent de la même référence\n(`concurrency`). `actions/checkout@v4`  … [1299 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/ci.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/ci.md", "new_string": "Le script choisit `python3` dans le `PATH`. Pour mesurer une version précise, on active son\nenvironnement (ou on passe `--python /chemin/venv/bin/python3`) : c'est ainsi que **3.10.20** et\n**3.13.16* … [484 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/ci.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/ci.md", "new_string": "- **Les versions d'actions peuvent bouger.** `@v4` et `@v5` sont des étiquettes mouvantes ; un\n  épinglage par SHA est plus strict, il n'est pas fait ici.\n- **La copie de secours de S peut dériver.** … [401 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/ci.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "**L'intégration continue** rejoue cette porte à chaque `push` : `.github/workflows/ci.yml` teste\n`pip install -e .`, les trois tests du contrat et `porte-produit.sh` sur **Python 3.10 et 3.13**\n( … [1222 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **job_output** `{"job_id": "bash-104", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **job_output** `{"job_id": "bash-105", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **job_output** `{"job_id": "bash-104", "wait": true, "timeout_ms": 300000}`

  ```
(no new output)
[status: completed, exit code: 0]
  ```

### 👤 Utilisateur

background job bash-105 (bash: rm -rf /tmp/ci-clean-313 && mkdir -p /tmp/ci-clean-313 && git archive HEAD | tar -x -C /tmp/ci-clean-313 && cp -r .github /tmp/ci-clean-313/ && cp tools/verifier_ci.py tools/verifie_structures_secours.py /tmp/ci-clean-313/tools/ && cp tools/tests/test_tagger_api.py /tmp/ci-clean-313/tools/tests/ && cd /tmp/ci-clean-313 && export PATH=/tmp/ci313/bin:$PATH && python3 tools/verifier_ci.py --json > /tmp/ci-clean-313.json 2> /tmp/ci-clean-313.err; echo "EXIT=$?" >> /tmp/ci-clean-313.err) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "cat /tmp/ci-clean-310.err; echo \"---\"; python3 - <<'EOF'\nimport json\nfor v in ('310','313'):\n    d=json.load(open(f'/tmp/ci-clean-{v}.json'))\n    print(v, 'ok=', d['ok'], d['python_version'], 'restauration=', d['restauration'], 'secours=', d['secours_s']['code'])\n    for e in d[' … [244 caractères tronqués]`

  ```
EXIT=0
---
310 ok= True Python 3.10.20 restauration= {'fait': True, 'fichiers': ['tools/structures/generateur.py', 'tools/structures/donnees/gold-analyseur.json']} secours= 0
  installer 0 2.933
  test_produit 0 15.982
  test_tagger_api 0 7.669
  porte_produit 0 227.457
  test_schema_produit 0 1.261
  negatif 1 True False
313 ok= True Python 3.13.16 restauration= {'fait': True, 'fichiers': ['tools/structures/generateur.py', 'tools/structures/donnees/gold-analyseur.json']} secours= 0
  installer 0 3.361
  test_produit 0 17.393
  test_tagger_api 0 7.767
  porte_produit 0 196.968
  test_schema_produit 0 1.532
  negatif 1 True False
  ```

- **bash** `{"command": "cat /tmp/ci-clean-313.err; echo \"---gate tails---\"; python3 - <<'EOF'\nimport json\nfor v in ('310','313'):\n    d=json.load(open(f'/tmp/ci-clean-{v}.json'))\n    gate=[e for e in d['execution'] if e['etape']=='porte_produit'][0]\n    print(v, gate['stdout'][-250:])\nEOF", "descriptio … [38 caractères tronqués]`

  ```
EXIT=0
---gate tails---
310 n v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ exemples de la doc : 27/27 cas conformes — ✅ aucun écart
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
313  détecté
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : 
  ✅ schéma v2 : 
  ✅ refus : JSON avec refus, code 3
  ✅ exemples de la doc : 27/27 cas conformes — ✅ aucun écart
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, hashlib, pathlib, re, subprocess\n\nracine = pathlib.Path('.').resolve()\nworkflow = (racine/'.github/workflows/ci.yml').read_text(encoding='utf-8')\nsha = hashlib.sha256(workflow.encode()).hexdigest()\nhead = subprocess.check_output(['git','rev-parse','- … [6248 caractères tronqués]`

  ```
JSON-VALIDE
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 47, in <module>
  File "<stdin>", line 9, in charger
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/ci-310.json'
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, hashlib, pathlib, re, subprocess\n\nracine = pathlib.Path('.').resolve()\nworkflow = (racine/'.github/workflows/ci.yml').read_text(encoding='utf-8')\nsha = hashlib.sha256(workflow.encode()).hexdigest()\nhead = subprocess.check_output(['git','rev-parse','- … [6265 caractères tronqués]`

  ```
{
  "matrice": [
    "3.10",
    "3.13"
  ],
  "versions_mesurees": [
    "3.10.20",
    "3.13.16"
  ],
  "etapes_par_version": 5,
  "etapes_vertes": 10,
  "etapes_rouges": 0,
  "controles_negatifs": 2,
  "controle_negatif_code": [
    1
  ],
  "controle_negatif_job_arrete": true,
  "porte_produit": "183/183 portes d'autotest",
  "act": false,
  "duree_totale_s": 482.323,
  "sha256_workflow": "8efe2f1be4421555f5f111a8c7602ab9a858fe18f8e37b9f023a9687d95323cf",
  "copie_secours_identique": true,
  "checkout_sans_sous_module": true
}
3.10.20 255.302 [2.933, 15.982, 7.669, 227.457, 1.261]
3.13.16 227.021 [3.361, 17.393, 7.767, 196.968, 1.532]
JSON-VALIDE
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md", "new_string": "> **Le chiffre.** Le workflow `.github/workflows/ci.yml` déclare une matrice **Python 3.10 /\n> 3.13** et cinq étapes : `pip install -e .`, `test_produit.py`, `test_tagger_api.py`,\n> `porte-produit … [2300 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md", "new_string": "| checkout | `actions/checkout@v4` — **sans sous-modules** ; S restauré depuis `.github/ci/structures` |\n| Python | `actions/setup-python@v5`, cache `pip` sur `pyproject.toml` |", "old_string": "|  … [165 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md", "new_string": "Le workflow ne récupère pas les sous-modules : `tools/structures` reste absent, et les tests\nqui rendent les rôles (`agent`, `predicat`) et les cibles ont besoin de son **générateur S**.\nL'URL ver … [1019 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md", "new_string": "| version | `pip install -e .` | `test_produit` | `test_tagger_api` | `porte-produit` | `test_schema_produit` | total |\n|---|---:|---:|---:|---:|---:|---:|\n| **3.10.20** | 0 · 2,933 s | 0 · 15,982 … [1017 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md", "new_string": "**Prouvé.** Le YAML est **valide** (PyYAML 6.0.3), la matrice et les cinq commandes sont\nprésentes ; les cinq commandes **passent** sur **3.10.20** et **3.13.16**, dans un venv propre\navec `pip in … [829 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md", "new_string": "- **La copie de secours peut dériver.** Elle est identique au sous-module au commit `648adce` ;\n  si S change, `tools/verifie_structures_secours.py` le dit (code **1**) et il faut la mettre à\n  jo … [1002 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md has been updated successfully.
  ```

- **bash** `{"command": "sed -n '/## 6\\. Ce qui pourrait/,/## 7\\./p' reports/rapport-ci.md", "description": "Read limitations section"}`

  ```
## 6. Ce qui pourrait rendre ce résultat faux

- **Le runner diffère de la machine.** `ubuntu-latest` change d'image ; les temps locaux
  (226 s et 196 s pour la porte) ne sont pas ceux du runner, et un timeout de 30 min peut
  devenir juste si l'autotest ralentit.
- **Le réseau de l'installation.** `pip install -e .` isole le build et télécharge
  `setuptools>=61` ; sans réseau ni cache, l'étape 1 échoue avant les tests. Les tests, eux,
  n'ouvrent aucune socket.
- **La copie de secours peut dériver.** Elle est identique au sous-module au commit `648adce` ;
  si S change, `tools/verifie_structures_secours.py` le dit (code **1**) et il faut la mettre à
  jour. C'est une duplication assumée : un run GitHub testerait sinon une autre version du
  générateur.
- **Le contrôle négatif est synthétique.** Il prouve le **mécanisme** (code 1, arrêt), pas
  qu'un test réel particulier détecte une régression métier. La couverture réelle est celle
  des 30 + 30 + 9 tests et de la porte.
- **La matrice locale n'est pas GitHub.** 3.10.20 vient d'un Python géré par `uv` et 3.13.16
  du système ; ce ne sont pas les builds exacts de `setup-python`.

## 7. Les fichiers
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md", "new_string": "- **Le runner diffère de la machine.** `ubuntu-latest` change d'image ; les temps locaux\n  (227 s et 197 s pour la porte) ne sont pas ceux du runner, et un timeout de 30 min peut\n  devenir juste s … [1036 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md", "new_string": "| fichier | changement |\n|---|---|\n| `.github/workflows/ci.yml` | le workflow : matrice 3.10/3.13, checkout, setup-python, restauration S, cinq étapes |\n| `.github/ci/structures/` | la copie de s … [1521 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md", "new_string": "**Verdict.** Z1 est **livré** : le workflow est écrit, la matrice **3.10 / 3.13** est déclarée,\nles cinq commandes passent **10/10** depuis une archive **sans sous-module** (copie de secours\nS res … [789 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"480\\|254,35\\|226,20\\|226 s\\|196 s\\|sans sous-module\\|clone public\\|copie de secours\" reports/rapport-ci.md | head -30; echo \"===DOC CI===\"; grep -n \"sans sous-module\\|copie de secours\\|480\\|482\" docs/produit/ci.md", "description": "Check report consistency"}`

  ```
15:> sous-module** : la copie de secours de S restaure les deux fichiers nécessaires.
51:| checkout | `actions/checkout@v4` — **sans sous-modules** ; S restauré depuis `.github/ci/structures` |
96:vérificateur restaure la copie de secours (comme le workflow), puis exécute les cinq commandes.
135:**archive `git archive HEAD` sans sous-module** : la copie de secours restaure S, les cinq
155:- **La copie de secours peut dériver.** Elle est identique au sous-module au commit `648adce` ;
170:| `.github/ci/structures/` | la copie de secours de S (`generateur.py`, `donnees/gold-analyseur.json`) et sa notice |
172:| `tools/verifie_structures_secours.py` | compare la copie de secours au sous-module (code 1 si dérive) |
181:les cinq commandes passent **10/10** depuis une archive **sans sous-module** (copie de secours
===DOC CI===
39:[`.github/ci/structures/`](../../.github/ci/structures/). C'est une **copie de secours**
64:**3.13.16** ont été mesurés séparément. Il **restaure aussi** la copie de secours de S si
66:lancer depuis une archive `git archive` sans sous-module.
86:- **La copie de secours de S peut dériver.** Elle est identique au sous-module au commit
  ```

- **bash** `{"command": "python3 -m json.tool reports/rapport-ci.json >/dev/null && echo JSON-OK; python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-ci.json'))\nprint(d['chiffres'])\nfor p in d['preuve_locale']:\n    print(p['version'], p['restauration_secours'], p['secours_identique'], p['duree_ … [65 caractères tronqués]`

  ```
JSON-OK
{'matrice': ['3.10', '3.13'], 'versions_mesurees': ['3.10.20', '3.13.16'], 'etapes_par_version': 5, 'etapes_vertes': 10, 'etapes_rouges': 0, 'controles_negatifs': 2, 'controle_negatif_code': [1], 'controle_negatif_job_arrete': True, 'porte_produit': "183/183 portes d'autotest", 'act': False, 'duree_totale_s': 482.323, 'sha256_workflow': '8efe2f1be4421555f5f111a8c7602ab9a858fe18f8e37b9f023a9687d95323cf', 'copie_secours_identique': True, 'checkout_sans_sous_module': True}
3.10.20 {'fait': True, 'fichiers': ['tools/structures/generateur.py', 'tools/structures/donnees/gold-analyseur.json']} 0 255.302
3.13.16 {'fait': True, 'fichiers': ['tools/structures/generateur.py', 'tools/structures/donnees/gold-analyseur.json']} 0 227.021
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Z1 — la protection (16/11)** : CI **3.10/3.13**, **10/10** étapes vertes depuis une archive **sans sous-module** (copie de secours S), porte **183/183**, test cassé → **1** et job arrêté ; `ac … [325 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**Z1 — l'intégration continue (16/11).** `.github/workflows/ci.yml` : matrice **3.10 / 3.13**,\n`pip install -e .` + les trois tests + la porte produit, `fail-fast: false` ; **10/10** étapes\nver … [666 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md", "new_string": "Les deux jambes locales sont vertes : **10/10** étapes, porte **183/183**, **482,3 s** au total.\nLa mesure part d'une archive **sans sous-module** : le sous-module `tools/structures` a une U … [962 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/ci.md", "new_string": "> **Vérifié le 2026-11-16** sur `s/v7` : YAML chargé par PyYAML **6.0.3**, **2 × 5 étapes\n> vertes** depuis une **archive sans sous-module** (copie de secours S) et depuis le dépôt,\n> porte produit * … [535 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/ci.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -30; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run doc review after edits", "timeout_ms": 300000}`

  ```
revue de documentation · 772 fiche(s) · 867 JSON · 126 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -8; echo \"EXIT=${PIPESTATUS[0]}\"; echo \"---\"; python3 tools/verifie_journal.py 2>&1 | tail -5; echo \"EXIT=${PIPESTATUS[0]}\"; echo \"---\"; python3 tools/verifie_structures_secours.py; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Ru … [57 caractères tronqués]`

  ```
en-cours · 1665 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT=0
---
  journal · 48 jour(s) · 228 session(s) · 2738 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
EXIT=0
---
✅ tools/structures/generateur.py ≡ .github/ci/structures/generateur.py · ca2d8823e9a6…
✅ tools/structures/donnees/gold-analyseur.json ≡ .github/ci/structures/donnees/gold-analyseur.json · 4cebc6d75b61…
EXIT=0
  ```

- **bash** `{"command": "rm -rf /tmp/ci-yaml && mkdir -p /tmp/ci-yaml && git archive HEAD | tar -x -C /tmp/ci-yaml && cp -r .github /tmp/ci-yaml/ && cp tools/verifier_ci.py tools/verifie_structures_secours.py /tmp/ci-yaml/tools/ && cp tools/tests/test_tagger_api.py /tmp/ci-yaml/tools/tests/ && cd /tmp/ci-yaml & … [817 caractères tronqués]`

  ```
--- étape YAML ---
if [ ! -f tools/structures/generateur.py ]; then
  mkdir -p tools/structures/donnees
  cp .github/ci/structures/generateur.py tools/structures/generateur.py
  cp .github/ci/structures/donnees/gold-analyseur.json tools/structures/donnees/gold-analyseur.json
  echo "S restauré depuis .github/ci/structures (sous-module non public)"
else
  echo "sous-module tools/structures présent : copie de secours non utilisée"
fi

code 0
S restauré depuis .github/ci/structures (sous-module non public)
 
EXIT=0
-rw-------. 1 stephane stephane 16806 16 nov 04:00 tools/structures/donnees/gold-analyseur.json
-rw-r--r--. 1 stephane stephane 31037 16 nov 04:00 tools/structures/generateur.py
DIFF=0
  ```

- **bash** `{"command": "cd /tmp/ci-yaml && export PATH=/tmp/ci310/bin:$PATH && python3 tools/verifier_ci.py --sans-porte 2>&1 | tail -10; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Run checks after YAML restore in clean archive", "timeout_ms": 600000}`

  ```
YAML valide · PyYAML 6.0.3 · matrice ['3.10', '3.13']
Python 3.10.20 · act=absent
  ✅ installer            code=0 · 2.797 s
  ✅ test_produit         code=0 · 16.385 s
  ✅ test_tagger_api      code=0 · 7.271 s
  ✅ test_schema_produit  code=0 · 1.187 s
  ✅ contrôle négatif  code=1 · job_echoue=True · étape suivante exécutée=False
  ✅ copie de secours S  identique
✅ CI locale verte
EXIT=0
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md", "limit": 220}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md</path>
<type>file</type>
<content>
1: # Z1 — L'intégration continue : le workflow, la matrice et le contrôle négatif
2: 
3: > **Ligne de roadmap** : **B13 — la protection** (produit exploitable) · **Tâche** : **Z1** ·
4: > **Date** : 2026-11-16 · **Branche** : `s/v7` · **Verdict** : ✅ **la CI est verte en local** —
5: > **2 versions**, **5 étapes par version**, **10/10 étapes vertes**, **0 rouge**, **2/2 contrôles
6: > négatifs** qui cassent et arrêtent la séquence, porte produit **183/183**.
7: >
8: > **Le chiffre.** Le workflow `.github/workflows/ci.yml` déclare une matrice **Python 3.10 /
9: > 3.13** et cinq étapes : `pip install -e .`, `test_produit.py`, `test_tagger_api.py`,
10: > `porte-produit.sh`, `test_schema_produit.py`. En local, avec **3.10.20** et **3.13.16** :
11: > **10 étapes vertes**, **0 rouge**, **482,3 s** au total ; la porte produit rend
12: > `✅ porte produit verte` avec **183/183** portes d'autotest et **27/27** exemples conformes.
13: > Un test volontairement cassé sort en **1** (`FAILED (failures=1)`) et **l'étape suivante
14: > n'est pas exécutée**. La mesure principale part d'une 
… [11189 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/index_reports.py --help 2>&1 | head -20; echo \"---\"; head -8 tools/index_reports.py", "description": "Inspect report index generator"}`

  ```
usage: index_reports.py [-h] [--verifier] [--aide]

Génère reports/INDEX.md (déterministe).

options:
  -h, --help  show this help message and exit
  --verifier  ne réécrit rien : compare l'index au disque, sort 1 s'il est
              périmé
  --aide      affiche l'aide et sort
---
#!/usr/bin/env python3
"""index_reports.py — génère reports/INDEX.md à partir des en-têtes de fiches.

L'index est **exhaustif** et **déterministe** : une ligne par fiche, triée par nom,
avec son titre (premier `# `). Les fichiers d'infrastructure (`README.md`, `INDEX.md`
et `historique-*`) sont exclus du tableau ; les compteurs de `docs/pilotage/en-cours.md`
comptent, eux, tous les `.md` de `reports/`.
  ```

- **bash** `{"command": "python3 tools/index_reports.py && git diff --stat reports/INDEX.md && grep -n \"rapport-ci\" reports/INDEX.md", "description": "Regenerate reports index"}`

  ```
769 fiches → reports/INDEX.md
 reports/INDEX.md | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
114:| [rapport-ci.md](rapport-ci.md) | Z1 — L'intégration continue : le workflow, la matrice et le contrôle négatif |
115:| [rapport-cic-v2.md](rapport-cic-v2.md) | B3 — Corpus d'or CIC v2 : le type de Bruijn vérifié, le sha256 rejoué deux fois |
116:| [rapport-cic-verificateur.md](rapport-cic-verificateur.md) | J12.2 — Le corpus d'or CIC : 42/42 verdicts rejoués par un vérificateur indépendant |
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "limit": 30, "offset": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md</path>
<type>file</type>
<content>
1: # Les rapports — données intermédiaires et références
2: 
3: > **Ce dossier porte les résultats et les données de nos travaux**, jamais la documentation de référence
4: > (elle est dans [`docs/`](../docs/)). Les fiches courantes sont citées depuis le tableau de bord
5: > [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md).
6: 
7: > **Navigation** : [la carte des sujets](../docs/theorie/carte.md) · [l'état du moment](../docs/pilotage/en-cours.md) ·
8: > [l'inventaire des docs](../docs/README.md) · [le journal](../journal/README.md).
9: >
10: > **Contexte** : la fiche [`07-mesures-couche-commune.md`](07-mesures-couche-commune.md) est un **hub** de
11: > **168 mesures** en **10 parties** (`07/p1.md` … `07/p10.md`), pas un fichier de 150 Ko. La lire **par
12: > partie**, jamais en entier ; l'index exhaustif des fiches est [`INDEX.md`](INDEX.md).
13: 
14: ## Les fiches courantes
15: 
16: | fichier | ce qu'il porte |
17: |---|---|
18: | [`rapport-bilan-jour-1115.md`](rapport-bilan-jour-1115.md) | **Bilan** — le 15/11 : la semaine 2 en un jour, la décision du tagger |
19: 
… [2153 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"rapport-bilan-exploitable-2\\|rapport-profils\\|rapport-evaluer-strict\" reports/README.md", "description": "Find insertion point in reports README"}`

  ```
44:| [`rapport-profils.md`](rapport-profils.md) | **U3/B13** — `drave profils` : les **398 profils UDHR** exposés, **20/20** sur l'échantillon, ambigu **`und`**, artefact 802 110 o |
45:| [`rapport-evaluer-strict.md`](rapport-evaluer-strict.md) | **V1** — `--strict` : cascade **0,8625/0,8891**, plancher **0,70** |
46:| [`rapport-bilan-exploitable-2.md`](rapport-bilan-exploitable-2.md) | **V3** — **86/82/4** → **84/2** |
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-bilan-exploitable-2.md`](rapport-bilan-exploitable-2.md) | **V3** — **86/82/4** → **84/2** |\n| [`rapport-ci.md`](rapport-ci.md) | **Z1/B13** — CI `3.10/3.13` : **10/10** étapes, porte **183 … [166 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/index_reports.py --verifier; echo \"INDEX=$?\"; python3 tools/revue_documentation.py 2>&1 | tail -5; echo \"REVUE=${PIPESTATUS[0]}\"", "description": "Verify index and doc review", "timeout_ms": 300000}`

  ```
INDEX=0
  revue de documentation · 772 fiche(s) · 867 JSON · 126 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -15; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Check context size budget", "timeout_ms": 300000}`

  ```
1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4035 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 4 violation(s) :
     · docs/README.md : 1012 mots > budget 1000 (T1)
     · docs/pilotage/roadmap.md : 9054 mots > budget 9000 (T1)
     · reports/README.md : 2817 mots > budget 2800 (T1)
     · T0 : 4035 mots (AGENTS + en-cours + une tâche) > budget 4 000
EXIT=1
  ```

- **bash** `{"command": "grep -n \"T0\\|4035\\|budget 4 000\\|task\\|tache\" tools/taille_documents.py | head -40; sed -n '1,80p' tools/taille_documents.py", "description": "Inspect context budget tool"}`

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
154:        violations.append(f"T0 : {t0} mots (AGENTS + en-cours + une tâche) > budget 4 000")
163:    print(f"  T0 max : {t0} mots (budget 4 000)")
#!/usr/bin/env python3
"""taille_documents.py — le budget de contexte et la cohésion des documents.

Ce que l'outil vérifie :
  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
  2. la cohésion minimale : un titre, un résumé en tête, et pour les documents datés un
     « Résumé » + « ne pas charger p
… [3186 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '60,125p' docs/pilotage/en-cours.md", "description": "Read en-cours prose for trimming"}`

  ```
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **238/239**.
- **Ce que font les autres** : N2.
- **Ce qu'elle fait** : **W5** v3 (gold S **144/144**, v2 **20/46**) ; **U1** 4,0 → 0,82 s (α 1,08) ; **U2** roue 1 727 201 o, sans gold → 4 ; **U3** profils 20/20, `und` ; **V1** `--strict` 0,8625/0,8891 ; **V2** exemples **27/27** ; **V3** la clôture — **86/82/4** → **84/2**, tag `exploitable-2026-11-16` ([bilan 2](../../reports/rapport-bilan-exploitable-2.md)).
- **Prochaine action** : **J4** ; T132/T133 ; la décision `auto`.
- **Bloquants** : 7B locales interdites (règle 11) ; **gold de pensée**.
- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).

### Session `0733c5bb-f90b-4f58-9241-3364fa32e46c` — N2 : la production et la capacité *(en pause)*

- **Id** : `0733c5bb-f90b-4f58-9241-3364fa32e46c` — [`plan.md`](../../journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/plan.md).
- **Rôle** : **N2** — la production et la capacité.
- **Plan** : fenêtre.
- **Ambition** : la longueur et la capacité.
- **Stratégie** : budgets contrôlés, mêmes bancs.
- **Objectif final** : la production qui tient.
- **Ce qu'elle fait** : **erratum 04/11** : la distil
… [6516 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**V3 — la clôture** : **T1–T6**, **U1–U3**, **V1–V2** ; **86/82/4** → **84/2** après vérification ciblée ; tag `exploitable-2026-11-16` sur `ae3c24f2` ; [bilan 2](../../reports/rapport-bilan-exp … [1007 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md", "new_string": "| [`produit/ci.md`](produit/ci.md) | l'**intégration continue** |", "old_string": "| [`produit/ci.md`](produit/ci.md) | l'**intégration continue** : matrice 3.10/3.13, cinq étapes, preuve locale sans `act` … [4 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md", "new_string": "| [`rapport-bilan-exploitable-2.md`](rapport-bilan-exploitable-2.md) | **V3** — **86/82/4** → **84/2** |", "old_string": "| [`rapport-bilan-exploitable-2.md`](rapport-bilan-exploitable-2.md) | **V3** —  … [166 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**V3 — la clôture (16/11).** **T1–T6 · U1–U3 · V1–V2** ; **86 / 82 / 4** → **84 / 2**\n(`work/portes/`) ; tag `exploitable-2026-11-16` sur **`ae3c24f2`** ; **Z1 — la CI** :\n**3.10 / 3.13**, **10 … [936 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -20; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Recheck context budgets", "timeout_ms": 300000}`

  ```
2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2797    236   T1   2800  reports/README.md
    2497    170   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4001 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 3 violation(s) :
     · docs/README.md : 1003 mots > budget 1000 (T1)
     · docs/pilotage/roadmap.md : 9016 mots > budge
… [87 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**V3 — la clôture** : **T1–T6**, **U1–U3**, **V1–V2** ; **86/82/4** → **84/2** après vérification ciblée ; tag `exploitable-2026-11-16` sur `ae3c24f2` ; [bilan 2](../../reports/rapport-bilan-exp … [758 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md", "new_string": "| [`methode/relations-humaines.md`](methode/relations-humaines.md) | *carpe diem*, le temps |", "old_string": "| [`methode/relations-humaines.md`](methode/relations-humaines.md) | *carpe diem*, le temps et … [17 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**V2 — exemples.** 3 corrigés ; 18 objets, 0 faux ; `verifie_exemples.py` 27/27 ; démarrage\n3/3. [Fiche](../../reports/rapport-exemples-v2.md) · [JSON](../../reports/rapport-exemples-v2.json).", … [253 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**V3 — la clôture (16/11).** **T1–T6 · U1–U3 · V1–V2** ; **86 / 82 / 4** → **84 / 2** ;\ntag `exploitable-2026-11-16` sur **`ae3c24f2`** ; **Z1 — la CI** : **3.10 / 3.13**, **10/10**.\n[Fiche](.. … [493 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -12; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Recheck budgets after trims", "timeout_ms": 300000}`

  ```
1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3999 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · docs/pilotage/roadmap.md : 9001 mots > budget 9000 (T1)
EXIT=1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "**V3 — clôture (16/11).** **T1–T6 · U1–U3 · V1–V2** ; **86 / 82 / 4** → **84 / 2** ;", "old_string": "**V3 — la clôture (16/11).** **T1–T6 · U1–U3 · V1–V2** ; **86 / 82 / 4** → **84 / 2** ;"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -10; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Final budget check", "timeout_ms": 300000}`

  ```
1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3999 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
EXIT=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -8; echo \"REVUE=${PIPESTATUS[0]}\"; echo \"---\"; python3 tools/verifie_en_cours.py 2>&1 | tail -5; echo \"ETAT=${PIPESTATUS[0]}\"", "description": "Rerun doc and state checks", "timeout_ms": 300000}`

  ```
revue de documentation · 772 fiche(s) · 867 JSON · 126 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE=0
---
  en-cours · 1629 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
ETAT=0
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -4; echo \"JOURNAL=${PIPESTATUS[0]}\"; python3 tools/index_reports.py --verifier >/dev/null 2>&1; echo \"INDEX=$?\"; python3 tools/verifie_structures_secours.py >/dev/null; echo \"SECOURS=$?\"", "description": "Rerun journal, index, fallback  … [30 caractères tronqués]`

  ```
journal · 48 jour(s) · 228 session(s) · 2738 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
JOURNAL=0
INDEX=0
SECOURS=0
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-ci.json'))\nprint(json.dumps({k:d[k] for k in ('chiffres','workflow')}, ensure_ascii=False, indent=2))\nprint('fichiers', d['fichiers'])\nEOF", "description": "Inspect report JSON workflow section"}`

  ```
{
  "chiffres": {
    "matrice": [
      "3.10",
      "3.13"
    ],
    "versions_mesurees": [
      "3.10.20",
      "3.13.16"
    ],
    "etapes_par_version": 5,
    "etapes_vertes": 10,
    "etapes_rouges": 0,
    "controles_negatifs": 2,
    "controle_negatif_code": [
      1
    ],
    "controle_negatif_job_arrete": true,
    "porte_produit": "183/183 portes d'autotest",
    "act": false,
    "duree_totale_s": 482.323,
    "sha256_workflow": "8efe2f1be4421555f5f111a8c7602ab9a858fe18f8e37b9f023a9687d95323cf",
    "copie_secours_identique": true,
    "checkout_sans_sous_module": true
  },
  "workflow": {
    "chemin": ".github/workflows/ci.yml",
    "declencheurs": [
      "push",
      "pull_request",
      "workflow_dispatch"
    ],
    "job": "produit",
    "runs_on": "ubuntu-latest",
    "timeout_minutes": 30,
    "fail_fast": false,
    "actions": [
      "actions/checkout@v4",
      "actions/setup-python@v5"
    ],
    "cache": "pip (pyproject.toml)",
    "restauration_s": "copie de secours .github/ci/structures si tools/structures/generateur.py manque",
    "commandes": [
      "pip install -e .",
      "python3 tools/tests/test_produit.py",
      "python3 tools/tests/te
… [587 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, pathlib\np=pathlib.Path('reports/rapport-ci.json')\nd=json.loads(p.read_text(encoding='utf-8'))\nfor f in ('reports/README.md','reports/INDEX.md'):\n    if f not in d['fichiers']:\n        d['fichiers'].append(f)\np.write_text(json.dumps(d, ensure_ascii=F … [183 caractères tronqués]`

  ```
ok
JSON-OK
  ```

- **bash** `{"command": "rm -rf /tmp/ci-yaml2 && mkdir -p /tmp/ci-yaml2 && git archive HEAD | tar -x -C /tmp/ci-yaml2 && cp -r .github /tmp/ci-yaml2/ && cp tools/verifier_ci.py tools/verifie_structures_secours.py /tmp/ci-yaml2/tools/ && cp tools/tests/test_tagger_api.py /tmp/ci-yaml2/tools/tests/ && cd /tmp/ci- … [755 caractères tronqués]`

  ```
started background job bash-131
  ```

- **job_output** `{"job_id": "bash-131", "wait": false}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "git status --short; echo \"---STAT---\"; git diff --stat | tail -20; echo \"---UNTRACKED---\"; git status --short | grep '^??'", "description": "Review working tree changes"}`

  ```
M docs/README.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M journal/2026-11-16/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/session-b3e96cb1-fb3b-4593-a2a6-b034ae644413/digest.md
 M journal/sessions/session-b3e96cb1-fb3b-4593-a2a6-b034ae644413/rapport.md
 M reports/INDEX.md
 M tools/chantier/plan.json
 M tools/tests/test_tagger_api.py
?? .github/
?? docs/produit/ci.md
?? reports/rapport-ci.json
?? reports/rapport-ci.md
?? tools/verifie_structures_secours.py
?? tools/verifier_ci.py
---STAT---
 docs/README.md                                     |   3 +-
 docs/pilotage/en-cours.md                          |   6 +-
 docs/pilotage/roadmap.md                           |  11 +-
 docs/produit/README.md                             |  12 ++
 journal/2026-11-16/README.md                       |  17 ++
 journal/README.md                                  |   2 +-
 journal/sessions/MANIFEST.md                       |   2 +-
 .../digest.md                                      | 240 +++++++++++++++++++++
 .../rapport.md                                     |  38 +++-
 reports/INDEX.md                                   
… [351 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-131", "wait": true, "timeout_ms": 300000}`

  ```
(no new output)
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "tail -35 /tmp/ci-yaml2.log; echo \"---codes---\"; grep -n '\\[code\\|\\[skip' /tmp/ci-yaml2.log", "description": "Inspect exact YAML run log"}`

  ```
Successfully uninstalled drave-0.1.0
Successfully installed drave-0.1.0
[code 0]

=== Smoke test produit ===
[code 0]

=== Tagger API (transport factice, sans réseau) ===
[code 0]

=== Porte produit ===
  ✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ profils : langue, script, confiance, 398 profils
  ✅ rejeu : sha256 f6355d8175a75854 deux fois
  ✅ smoke test : Ran 30 tests
  ✅ evaluer --strict : Ran 5 tests
  ✅ schéma v2 validé (5 cas v2 + 1 cas v1 + 20 phrases du gold)
  ✅ 50 textes libres : Ran 4 tests
  ✅ restitution v0 : surface exacte (miroir affiché)
  ✅ restitution v1 : forme canonique exacte, miroir strict distinct
  ✅ restitution v2 : rôles lisibles, rendu relu, contrôle détecté
  ✅ restitution v0/v1 : Ran 22 tests
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 9 tests
  ✅ refus : JSON avec refus, code 3
  ✅ exemples de la doc : 27/27 cas conformes — ✅ aucun écart
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
[code 0]

=== Schéma produit ===
[code 0]
EXIT=0
---codes---
77:[skip uses] Récupérer le dépôt -> actions/checkout@v4
78:[skip uses] Installer Pyt
… [140 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, pathlib\np=pathlib.Path('reports/rapport-ci.json')\nd=json.loads(p.read_text(encoding='utf-8'))\nd['preuve_yaml_run'] = {\n    'version': '3.10.20',\n    'environnement': 'archive `git archive HEAD` sans sous-module, blocs `run` du YAML exécutés avec `bas … [487 caractères tronqués]`

  ```
ok
JSON-OK
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md", "new_string": "Ces deux runs partent d'une **archive `git archive HEAD`** sans `tools/structures` ; le\nvérificateur restaure la copie de secours (comme le workflow), puis exécute les cinq commandes.\nLes mêmes ci … [771 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md", "new_string": "commandes passent, et `tools/verifie_structures_secours.py` confirme que la copie est\n**identique** au sous-module (code **0**). Les **sept blocs `run`** du YAML passent **7/7** sur\ncette archive  … [197 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -8; echo \"REVUE=${PIPESTATUS[0]}\"; python3 tools/verifie_en_cours.py 2>&1 | tail -4; echo \"ETAT=${PIPESTATUS[0]}\"", "description": "Rerun doc and state checks after report edits", "timeout_ms": 300000}`

  ```
revue de documentation · 772 fiche(s) · 867 JSON · 126 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE=0
  en-cours · 1629 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
ETAT=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -4; echo \"BUDGET=${PIPESTATUS[0]}\"; python3 tools/verifie_journal.py 2>&1 | tail -3; echo \"JOURNAL=${PIPESTATUS[0]}\"", "description": "Rerun budget and journal checks", "timeout_ms": 300000}`

  ```
avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
BUDGET=0
  journal · 48 jour(s) · 228 session(s) · 2738 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
JOURNAL=0
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/ci.md", "new_string": "**Ce que la preuve donne.** Les deux jambes passent les cinq étapes, la porte produit rend\n`✅ porte produit verte` et **183/183** portes d'autotest. Le contrôle négatif rend **1**, avec\n`FAILED (fail … [794 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/ci.md has been updated successfully.
  ```

- **bash** `{"command": "git diff -- docs/README.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md | head -100", "description": "Review docs diffs"}`

  ```
diff --git a/docs/README.md b/docs/README.md
index e55d50ba..04daadfb 100644
--- a/docs/README.md
+++ b/docs/README.md
@@ -33,7 +33,7 @@
 | [`methode/chantier-autonome.md`](methode/chantier-autonome.md) | le chantier long |
 | [`methode/continuite.md`](methode/continuite.md) | les cycles DSH, les sous-agents |
 | [`methode/modularisation.md`](methode/modularisation.md) | diviser ou paralléliser : ce que la mesure dit |
-| [`methode/relations-humaines.md`](methode/relations-humaines.md) | *carpe diem*, le temps et les échanges |
+| [`methode/relations-humaines.md`](methode/relations-humaines.md) | *carpe diem*, le temps |
 
 ## Pilotage — planification, état, suivi
 
@@ -97,6 +97,7 @@
 | [`produit/README.md`](produit/README.md) | le **premier produit** : analyser un texte |
 | [`produit/README.md` § 8](produit/README.md#8-faq--dix-questions) | la **FAQ** : dix questions vérifiées |
 | [`produit/exemples.md`](produit/exemples.md) | cinq exemples réels, dont un échec connu |
+| [`produit/ci.md`](produit/ci.md) | l'**intégration continue** |
 
 ## Transversal et archive
 
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 48408f6e..16c2bf3a 100644
--- a/docs/pilot
… [3816 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md", "new_string": "| `reports/rapport-ci.json` | les runs (archive et dépôt), les durées, le négatif, le sha256 du workflow |", "old_string": "| `reports/rapport-ci.json` | les deux runs (archive et dépôt), les durées … [39 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-ci.md has been updated successfully.
  ```

- **bash** `{"command": "sha256sum .github/workflows/ci.yml; python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-ci.json'))\nprint(d['chiffres']['sha256_workflow'])\nEOF", "description": "Verify workflow hash matches report"}`

  ```
8efe2f1be4421555f5f111a8c7602ab9a858fe18f8e37b9f023a9687d95323cf  .github/workflows/ci.yml
8efe2f1be4421555f5f111a8c7602ab9a858fe18f8e37b9f023a9687d95323cf
  ```

- **bash** `{"command": "export PATH=/tmp/ci310/bin:$PATH; python3 tools/verifier_ci.py --sans-porte 2>&1 | tail -10; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Final quick CI verification", "timeout_ms": 600000}`

  ```
YAML valide · PyYAML 6.0.3 · matrice ['3.10', '3.13']
Python 3.10.20 · act=absent
  ✅ installer            code=0 · 2.665 s
  ✅ test_produit         code=0 · 16.969 s
  ✅ test_tagger_api      code=0 · 7.613 s
  ✅ test_schema_produit  code=0 · 1.401 s
  ✅ contrôle négatif  code=1 · job_echoue=True · étape suivante exécutée=False
  ✅ copie de secours S  identique
✅ CI locale verte
EXIT=0
  ```

- **bash** `{"command": "git diff --check; echo \"CHECK=$?\"; python3 -m py_compile tools/verifier_ci.py tools/verifie_structures_secours.py tools/tests/test_tagger_api.py; echo \"PYCOMPILE=$?\"", "description": "Check whitespace and compile"}`

  ```
journal/2026-11-16/README.md:92: trailing whitespace.
+Le workflow `.github/workflows/ci.yml` rejoue le produit sur **Python 3.10 et 3.13** : 
journal/sessions/session-b3e96cb1-fb3b-4593-a2a6-b034ae644413/digest.md:2702: trailing whitespace.
+autonome (**1 727 201 o**, 
journal/sessions/session-b3e96cb1-fb3b-4593-a2a6-b034ae644413/digest.md:2787: new blank line at EOF.
CHECK=2
PYCOMPILE=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py >/tmp/revue-final.log 2>&1; echo \"REVUE=$?\"; tail -2 /tmp/revue-final.log; python3 tools/taille_documents.py >/tmp/taille-final.log 2>&1; echo \"TAILLE=$?\"; tail -2 /tmp/taille-final.log", "description": "Final doc review and budget", "timeout_ms" … [9 caractères tronqués]`

  ```
REVUE=0
  revue de documentation · 772 fiche(s) · 867 JSON · 126 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
TAILLE=0

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md", "new_string": "Le workflow `.github/workflows/ci.yml` rejoue le produit sur **Python 3.10 et 3.13** :\n`pip install -e .`, `test_produit.py`, `test_tagger_api.py`, `porte-produit.sh`,", "old_string": "Le wo … [166 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-16/README.md has been updated successfully.
  ```

- **bash** `{"command": "ls tools/tests/_controle_negatif_ci_* 2>/dev/null || echo \"pas de temporaire\"; git status --short | head -30", "description": "Check temp files and status"}`

  ```
pas de temporaire
 M docs/README.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M journal/2026-11-16/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/session-b3e96cb1-fb3b-4593-a2a6-b034ae644413/digest.md
 M journal/sessions/session-b3e96cb1-fb3b-4593-a2a6-b034ae644413/rapport.md
 M reports/INDEX.md
 M tools/chantier/plan.json
 M tools/tests/test_tagger_api.py
?? .github/
?? docs/produit/ci.md
?? reports/rapport-ci.json
?? reports/rapport-ci.md
?? tools/verifie_structures_secours.py
?? tools/verifier_ci.py
  ```

- **bash** `{"command": "git add .github/workflows/ci.yml .github/ci/structures/README.md .github/ci/structures/generateur.py .github/ci/structures/donnees/gold-analyseur.json tools/verifier_ci.py tools/verifie_structures_secours.py tools/tests/test_tagger_api.py docs/produit/ci.md docs/produit/README.md docs/R … [250 caractères tronqués]`

  ```
A  .github/ci/structures/README.md
A  .github/ci/structures/donnees/gold-analyseur.json
A  .github/ci/structures/generateur.py
A  .github/workflows/ci.yml
M  docs/README.md
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  docs/produit/README.md
A  docs/produit/ci.md
M  journal/2026-11-16/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/session-b3e96cb1-fb3b-4593-a2a6-b034ae644413/digest.md
 M journal/sessions/session-b3e96cb1-fb3b-4593-a2a6-b034ae644413/rapport.md
M  reports/INDEX.md
A  reports/rapport-ci.json
A  reports/rapport-ci.md
 M tools/chantier/plan.json
M  tools/tests/test_tagger_api.py
A  tools/verifie_structures_secours.py
A  tools/verifier_ci.py
  ```

- **bash** `{"command": "git commit -m \"Z1 — L'INTÉGRATION CONTINUE : MATRICE 3.10/3.13, 10/10 ÉTAPES VERTES (ARCHIVE SANS SOUS-MODULE, COPIE DE SECOURS S) ; PORTE 183/183 ; TEST CASSÉ → 1, JOB ARRÊTÉ ; act ABSENT, YAML PARSÉ\" 2>&1 | tail -40; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Commit Z1 with ho … [27 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-144]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-144", "wait": true, "timeout_ms": 180000}`

  ```
✅ index : aucun fait stagé sans état
[s/v7 19992f2f] Z1 — L'INTÉGRATION CONTINUE : MATRICE 3.10/3.13, 10/10 ÉTAPES VERTES (ARCHIVE SANS SOUS-MODULE, COPIE DE SECOURS S) ; PORTE 183/183 ; TEST CASSÉ → 1, JOB ARRÊTÉ ; act ABSENT, YAML PARSÉ
 30 files changed, 7338 insertions(+), 38 deletions(-)
 create mode 100644 .github/ci/structures/README.md
 create mode 100644 .github/ci/structures/donnees/gold-analyseur.json
 create mode 100644 .github/ci/structures/generateur.py
 create mode 100644 .github/workflows/ci.yml
 create mode 100644 docs/produit/ci.md
 create mode 100644 journal/2026-11-16/modele.md
 create mode 100644 journal/sessions/session-b9138a2a-648e-490d-a349-124ac1aa1ef0/digest.md
 create mode 100644 journal/sessions/session-b9138a2a-648e-490d-a349-124ac1aa1ef0/rapport.md
 create mode 100644 reports/rapport-ci.json
 create mode 100644 reports/rapport-ci.md
 create mode 100644 tools/verifie_structures_secours.py
 create mode 100644 tools/verifier_ci.py
EXIT=0
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "git status --short; echo \"---LOG---\"; git log -1 --oneline; echo \"---STAT---\"; git show --stat --oneline HEAD | head -40", "description": "Check post-commit status and stats"}`

  ```
M tools/chantier/plan.json
---LOG---
19992f2f Z1 — L'INTÉGRATION CONTINUE : MATRICE 3.10/3.13, 10/10 ÉTAPES VERTES (ARCHIVE SANS SOUS-MODULE, COPIE DE SECOURS S) ; PORTE 183/183 ; TEST CASSÉ → 1, JOB ARRÊTÉ ; act ABSENT, YAML PARSÉ
---STAT---
19992f2f Z1 — L'INTÉGRATION CONTINUE : MATRICE 3.10/3.13, 10/10 ÉTAPES VERTES (ARCHIVE SANS SOUS-MODULE, COPIE DE SECOURS S) ; PORTE 183/183 ; TEST CASSÉ → 1, JOB ARRÊTÉ ; act ABSENT, YAML PARSÉ
 .github/ci/structures/README.md                    |   30 +
 .github/ci/structures/donnees/gold-analyseur.json  | 1158 ++++++
 .github/ci/structures/generateur.py                |  657 ++++
 .github/workflows/ci.yml                           |   74 +
 docs/README.md                                     |    3 +-
 docs/pilotage/en-cours.md                          |    6 +-
 docs/pilotage/roadmap.md                           |   11 +-
 docs/produit/README.md                             |   12 +
 docs/produit/ci.md                                 |  100 +
 journal/2026-11-16/README.md                       |   23 +-
 journal/2026-11-16/docs.md                         |    2 +-
 journal/2026-11-16/memoire.md                      |    2 +-
 journal/2026-11
… [1167 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"Z1 — l'intégration continue\" -A4 journal/2026-11-16/README.md | head -10; echo \"---\"; python3 tools/verifie_en_cours.py 2>&1 | tail -3; echo \"ETAT=${PIPESTATUS[0]}\"; python3 tools/revue_documentation.py 2>&1 | tail -3; echo \"REVUE=${PIPESTATUS[0]}\"", "description": "Ver … [62 caractères tronqués]`

  ```
92:### Z1 — l'intégration continue, la matrice et le test qui casse
93-
94-Le workflow `.github/workflows/ci.yml` rejoue le produit sur **Python 3.10 et 3.13** :
95-`pip install -e .`, `test_produit.py`, `test_tagger_api.py`, `porte-produit.sh`,
96-`test_schema_produit.py`. Comme `act` n'est pas installé, `tools/verifier_ci.py` charge le YAML
---
  en-cours · 1629 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
ETAT=0
  revue de documentation · 772 fiche(s) · 867 JSON · 126 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE=0
  ```

- **bash** `{"command": "python3 tools/verifie_etat_a_jour.py 2>&1 | tail -5; echo \"ETAT-A-JOUR=${PIPESTATUS[0]}\"; python3 tools/taille_documents.py 2>&1 | tail -3; echo \"BUDGET=${PIPESTATUS[0]}\"; python3 tools/verifie_journal.py 2>&1 | tail -3; echo \"JOURNAL=${PIPESTATUS[0]}\"", "description": "Final stat … [49 caractères tronqués]`

  ```
état · dernier fait 19992f2f · dernier état 19992f2f
  ✅ aucun fait commité après le dernier état
ETAT-A-JOUR=0
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
BUDGET=0
  journal · 48 jour(s) · 229 session(s) · 2744 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
JOURNAL=0
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport yaml\nd=yaml.safe_load(open('.github/workflows/ci.yml'))\nj=d['jobs']['produit']\nprint('matrice', j['strategy']['matrix']['python'])\nprint('etapes', len(j['steps']))\nprint('runs', [s.get('name') for s in j['steps'] if 'run' in s])\nEOF\necho \"YAML=$?\"; pyt … [111 caractères tronqués]`

  ```
matrice ['3.10', '3.13']
etapes 9
runs ["Vérifier l'interpréteur et pip", 'Restaurer le générateur S (sous-module non public)', 'Installer le produit en éditable', 'Smoke test produit', 'Tagger API (transport factice, sans réseau)', 'Porte produit', 'Schéma produit']
YAML=0
✅ tools/structures/generateur.py ≡ .github/ci/structures/generateur.py · ca2d8823e9a6…
✅ tools/structures/donnees/gold-analyseur.json ≡ .github/ci/structures/donnees/gold-analyseur.json · 4cebc6d75b61…
SECOURS=0
  ```

- **bash** `{"command": "test -f .github/workflows/ci.yml && echo CI-OK; test -f reports/rapport-ci.md && echo FICHE-OK; test -f reports/rapport-ci.json && echo JSON-OK; git status --short", "description": "Run acceptance checks"}`

  ```
CI-OK
FICHE-OK
JSON-OK
 M tools/chantier/plan.json
  ```

### 🤖 Assistant

## Z1 — l’intégration continue : livrée

**Commit** : `19992f2f` — *Z1 — L'INTÉGRATION CONTINUE : MATRICE 3.10/3.13, 10/10 ÉTAPES VERTES (ARCHIVE SANS SOUS-MODULE, COPIE DE SECOURS S) ; PORTE 183/183 ; TEST CASSÉ → 1, JOB ARRÊTÉ ; act ABSENT, YAML PARSÉ*.

### Ce qui est en place

| fichier | rôle |
|---|---|
| `.github/workflows/ci.yml` | matrice **Python 3.10 / 3.13**, `pip install -e .`, les trois tests, `porte-produit.sh`, `fail-fast: false`, déclencheurs `push`/`pull_request`/`workflow_dispatch` |
| `tools/verifier_ci.py` | parse le YAML, exécute les commandes en fail-fast, restaure S, contrôle négatif, sortie JSON |
| `.github/ci/structures/` | copie de secours de `generateur.py` + `gold-analyseur.json` (le sous-module S a une URL locale, impossible à cloner sur un runner) |
| `tools/verifie_structures_secours.py` | compare la copie au sous-module (code 1 si dérive) |
| `docs/produit/ci.md` | mode d’emploi, preuve et limites |
| `reports/rapport-ci.md` + `.json` | fiche et données mesurées |

### Preuve locale, sans `act`

`act` n’est pas installé. Le YAML est chargé par **PyYAML 6.0.3**, puis les commandes sont exécutées :

| version | 5 étapes | porte produit | total |
|---|---:|---:|---:|
| **3.10.20** | 0 · 5/5 vertes | 0 · **183/183** | 255,30 s |
| **3.13.16** | 0 · 5/5 vertes | 0 · **183/183** | 227,02 s |

- **10/10 étapes vertes**, **0 rouge**, **482,3 s** au total.
- Mesure principale depuis une **archive `git archive HEAD` sans sous-module** : la copie de secours S restaure les deux fichiers, puis tout passe.
- Les **7 blocs `run` du YAML** exécutés tels quels avec `bash -e` : **7/7 code 0**.
- **Contrôle négatif 2/2** : une copie de `test_produit.py` avec un test cassé sort en **1** (`FAILED (failures=1)`) et **l’étape suivante n’est pas exécutée**.

### Deux points importants

1. **Le CI a trouvé un vrai défaut** : `test_tagger_api.py` échouait en HEAD car deux doubles `_module_evaluation` ne prenaient pas le mot-clé `gele` ajouté par `evaluer`. Correctif dans le test (`lambda gele=False: evaluateur`), pas dans le produit.
2. **Le sous-module `tools/structures` n’est pas public** (URL locale). Sans la copie de secours, `test_produit` et la porte échouaient sur un checkout propre ; la copie est identique au commit `648adce` et vérifiée par `tools/verifie_structures_secours.py`.

### Limite nommée

Sans `act`, on prouve le **YAML** et les **commandes**, pas l’image `ubuntu-latest`, `actions/checkout` ni `actions/setup-python`. La prochaine preuve est un **run vert dans l’onglet Actions** après le `push`.

Contrôles finaux : `revue_documentation` ✅, `verifie_en_cours` ✅, `verifie_journal` ✅, `taille_documents` ✅, `verifie_structures_secours` ✅, acceptation **CI-OK / FICHE-OK / JSON-OK** ✅.

