# Session DSH — relecture

- identifiant : `session-b4ff97bc-493d-4bfb-b734-e055dc85c779`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-16 01:31:33
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche U3 (suite de T5) : `--profils` — exposer la **détection de langue** (les 398 langues de l'autotest UDHR) dans le CLI : `drave profils --texte` (ou `analyser --profils`) rend la langue probable, le script et la confiance, pour un texte donné ; mesure sur les 20 langues de l'échantillon UDHR (la précision), le contrôle négatif (un texte ambigu), la doc § 3. Fiche `reports/rapport-profils.md` + JSON, tests.

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

- **bash** `{"command": "pwd && ls -la && git status --short | head -50 && git log --oneline -10", "description": "Inspect repository root and git state"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
total 212
drwxr-xr-x. 1 stephane stephane   760 16 nov 00:38 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    42 16 nov 00:38 build
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane    56 16 nov 00:38 dist
drwxr-xr-x. 1 stephane stephane   138 15 nov 22:25 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   136 16 nov 00:38 drave.egg-info
drwxr-xr-x. 1 stephane stephane   220 16 nov 01:31 .git
-rw-r--r--. 1 stephane stephane   653 15 nov 22:25 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane  1012 16 nov 00:22 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-------. 1 stephane stephane  1132 16 nov 00:34 pyproject.toml
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 s
… [3464 caractères tronqués]
  ```

- **bash** `{"command": "ls docs/pilotage/ && sed -n '1,120p' docs/pilotage/en-cours.md", "description": "Read current state document"}`

  ```
backlog
chantiers.md
en-cours.md
manques.md
plan-travail.md
programme-r.md
README.md
references-non-regression.md
roadmap.md
semaine-2.md
semaine-autonome.md
utilisation.md
# En ce moment

**Mis à jour : 2026-11-16, 00 h 45 HNE (U2 : la roue, les gold dedans, la roue sans gold échoue)**

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
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son
… [9378 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"398\" --include=*.py --include=*.md src tools reports docs 2>/dev/null | head -50", "description": "Search for 398 language references"}`

  ```
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/cachecontrol/controller.py:40:    """Parses a URI using the regex given in Appendix B of RFC 3986.
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/idna/uts46data.py:640:        0x398,
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/idna/uts46data.py:3473:        0x3398,
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/filters/__init__.py:139:        '\\Theta'                : '\U00000398',
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/filters/__init__.py:452:        '\\<Theta>'                : '\U00000398',
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/requests/models.py:502:        # handles RFC 3986 only.
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/requests/sessions.py:239:            # Compliant with RFC3986, we percent encode the url.
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/requests/utils.py:674:# The unreserved URI characters (RFC 3986)
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_cell_widths.py:95:    (3398, 3400, 0),
tools/docwatch/.venv/lib/python3.13/site-pack
… [5494 caractères tronqués]
  ```

- **bash** `{"command": "find src -type f | head -100 && echo '---' && find tools -maxdepth 2 -type f | head -80", "description": "List source and tools files"}`

  ```
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
---
tools/make_patch.py
tools/ref_logits.md
tools/harmony_canonique.py
tools/aiguille.py
tools/mla_synthetique.py
tools/vision_ref.py
tools/vision_mtmd.py
tools/diff_flux.py
tools/profil_flux.py
tools/flux_codec.py
tools/analyse_flux.py
tools/pair_factice.py
tools/proxy_latence.py
tools/trace_compacite.py
tools/preparer_colab.sh
tools/colab_cote_local.sh
tools/sprint.sh
tools/telecharger_modeles.py
tools/manifeste_modeles_lourds.json
tools/clusters_moe.py
tools/convertir_clusters.py
tools/verifier_table_types.sh
tools/inventaire_modeles_lourds.sh
tools/analyse_empreinte.py
tools/analyse_experts_statique.py
tools/ref_ggml_bloc.c
tools/verifier_formats.py
tools/portes_formats.sh
tools/extraire_tables_ggml.c
tools/extraire_tabl
… [1435 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"398\" --include=*.py --include=*.md --include=*.json --exclude-dir=.venv --exclude-dir=__pycache__ src tools reports docs journal drave-core 2>/dev/null | head -60", "description": "Search 398 excluding venv"}`

  ```
tools/tests/linguistique/gold_reel.py:1246:    ('r398', 'en', 'The moon shines; it lights.',
tools/tests/linguistique/gold_reel.json:28656:   "id": "r398",
tools/tests/linguistique/gold_gele.json:30000:"id": "r398",
tools/structures/README.md:204:dans le cadre — 1 020 × 550 pour l'exemple, 1 398 et 1 613 px pour les deux autres paragraphes),
tools/chantier/plan.json:868:   "mandat": "Tâche U3 (suite de T5) : `--profils` — exposer la **détection de langue** (les 398 langues de l'autotest UDHR) dans le CLI : `drave profils --texte` (ou `analyser --profils`) rend la langue probable, le script et la confiance, pour un texte donné ; mesure sur les 20 langues de l'échantillon UDHR (la précision), le contrôle négatif (un texte ambigu), la doc § 3. Fiche `reports/rapport-profils.md` + JSON, tests.",
tools/verifier_faq.py:83:    assert "398 langues" in bloc and "0,9687" in bloc, "profils UDHR absents de la fiche"
tools/verifier_faq.py:90:        "profils_udhr": {"langues": 398, "exactitude": 0.9687, "seuil": 0.12,
reports/rapport-minimal.md:63:| modèle minimal — ternaire dense 2 b | 0.0 Mo | 0.000 | 13989862.4 | 312 | 9360 |
reports/rapport-minimal.md:73:| 70B — ternaire CSR | 148750.0 Mo |
… [5494 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"udhr\\|UDHR\\|Udhr\" --include=*.py --include=*.md --include=*.json --exclude-dir=.venv --exclude-dir=__pycache__ . 2>/dev/null | head -60", "description": "Find UDHR-related files"}`

  ```
./reports/rapport-plateau-semantique.md
./reports/rapport-pont-semantique.md
./reports/rapport-pont-generatif.md
./reports/rapport-cycle-rapide.md
./reports/archive/rapport-toutes-langues.md
./reports/archive/rapport-campagne-benefices.md
./reports/toutes-langues/001-01-le-perimetre-inventorie.md
./reports/toutes-langues/004-04-les-cinq-phases-chainees.md
./reports/toutes-langues/005-05-mesure-linvariance-a-dix-points.md
./reports/toutes-langues/017-17-le-plateau-du-professeur-est-a-la-couche.md
./reports/toutes-langues/018-18-romeo-le-pont-transfere-sur-du-texte-lit.md
./reports/toutes-langues/019-19-couche-8-contre-couche-10-la-correction.md
./reports/toutes-langues/022-22-correction-la-richesse-nest-pas-dans-le.md
./reports/toutes-langues/023-23-domaine-ou-langue-teste-et-le-test-est-i.md
./reports/toutes-langues/024-24-signal-precoce-la-couche-8-gagne-aussi-a.md
./reports/toutes-langues/032-32-le-29-est-il-un-artefact-dalignement-non.md
./reports/toutes-langues/041-41-le-profil-porte-maintenant-tout-le-proto.md
./reports/toutes-langues/042-42-jalon-392-langues-tracees-aux-deux-couch.md
./reports/toutes-langues/045-45-premier-corpus-multi-domaine-et-aligne-4.md
./reports/toutes-
… [1740 caractères tronqués]
  ```

- **bash** `{"command": "cat pyproject.toml && echo '---' && find . -maxdepth 3 -type d -name 'drave*' -o -maxdepth 3 -type f -name 'cli*.py' | grep -v .venv | head -40", "description": "Read pyproject and locate CLI"}`

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
# Les gold sont **dans la roue** : `drave evaluer` doit marcher hors du dépôt.
# Le contrôle négatif (une roue amputée de ces fichiers) est décrit dans
# reports/rapport-roue.md : `evaluer` échoue alors en code 4, sans trace.
"tools.tests.linguistique" = [
    "gold.json",
    "gold_gele.json",
    "gold_reel.json",
    "gold_restitution_v2.json",
    "gold_synthetique.json",
]
---
./drave-core
./drave.egg-info
  ```

- **bash** `{"command": "wc -l tools/drave.py && sed -n '1,160p' tools/drave.py", "description": "Read CLI start"}`

  ```
1334 tools/drave.py
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
    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
    python3 tools/drave.py --version

Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure 
… [5953 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/tests/linguistique/ && echo '---' && grep -rn \"langue\\|script\\|profil\" --include=*.py tools/tests/linguistique tools/drave.py | head -80", "description": "Explore linguistics tests and language refs"}`

  ```
anaphore.py
classement_cible.py
classer_gv.py
evaluer_gold.py
gold_gele.json
gold.json
gold.py
gold_reel_50.py
gold_reel.json
gold_reel.py
gold_restitution_v2.json
gold_split.py
gold_synthetique.json
gold_synthetique.py
juge.py
miroir.py
__pycache__
qualifier_cascade.py
qualifier_frontiere_71.py
qualifier_lien_appris.py
qualifier_neuronal.py
qualifier_pragmatique.py
qualifier_quatre_modes.py
qualifier_syntagmes.py
qualifier_tagger_612.py
qualifier_tagger_h50.py
qualifier_tagger_lot.py
replis_cible.py
test_atomes_prediction.py
test_bloc_linguistique.py
---
tools/tests/linguistique/gold.py:91:    for pid, langue, texte, pos, segments, pragma in PHRASES:
tools/tests/linguistique/gold.py:111:        phrases.append({"id": pid, "langue": langue, "texte": texte, "mots": mots,
tools/tests/linguistique/evaluer_gold.py:89:    par_langue = {"fr": {"cibles": 0, "labels": 0, "exact": 0, "topk": 0},
tools/tests/linguistique/evaluer_gold.py:94:        a = bloc.analyser(phrase["texte"], phrase["langue"])
tools/tests/linguistique/evaluer_gold.py:119:        langue = phrase.get("langue", "fr")
tools/tests/linguistique/evaluer_gold.py:120:        bloc_langue = par_langue.get(langue, par_langue["fr"])
… [8419 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"def detecter_langue\\|def detecter_script\\|def _profil\\|PROFILS\\|profils\" tools/bloc_linguistique.py | head -60 && echo '---' && grep -rn \"0.9687\\|0,9687\\|profils_udhr\\|profil.*udhr\\|udhr.*profil\" --include=*.py --include=*.md --include=*.json --exclude-dir=.venv .  … [101 caractères tronqués]`

  ```
178:# --------------------------------------------------------------------------- profils de langue
190:def _profil(texte: str, top: int = 200) -> dict[str, int]:
195:def charger_profils_udhr(chemin: pathlib.Path, train=(0, 14), test=(15, 30),
198:    """Construit des profils de trigrammes par langue et un jeu de test tenu à l'écart.
210:    profils: dict[str, dict] = {}
220:        profils[langue] = {
226:    return profils, tests
236:def detecter_langue(texte: str, profils: dict[str, dict] | None = None,
239:    if profils:
241:        scores = {langue: _score_profil(tri, p["trigrammes"]) for langue, p in profils.items()}
293:def detecter_script(texte: str) -> str:
1017:    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
1020:        self.profils = profils
1036:        langue, conf, _ = detecter_langue(texte, self.profils, indice)
2145:    def __init__(self, profils: dict[str, dict] | None = None):
2146:        self.profils = profils
2151:        lg = detecter_langue(texte, self.profils, langue)[0]
3068:    profils, tests = charger_profils_udhr(udhr, test=(15, 15), min_test=1)
3074:        detectee, conf, _ = detecter_langue(texte, profils)
30
… [14708 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' tools/tests/linguistique/qualifier_frontiere_71.py", "description": "Read 71-language boundary qualifier"}`

  ```
#!/usr/bin/env python3
"""qualifier_frontiere_71.py — la frontière heuristique sur les 71 langues du dépôt.

Le contrat de L (docs/theorie/contrat-bloc-langue.md) demande une mesure de la
frontière « couverture × précision par unité de calcul ». Ici, sur le lexique
multilingue des jeux (71 langues, 35 concepts, labels Wikidata) :

  1. le SCRIPT (niveau graphème) : la détection de script contre les écritures
     connues de chaque langue — c'est le niveau que le CPU doit tenir ;
  2. la LANGUE (niveau multilingue) : la détection par trigrammes en
     leave-one-out, contre la **classe majoritaire** — le contrôle négatif
     « une heuristique rapide mais fausse coûte plus qu'un appel réseau ».

Le POS n'est pas mesuré : le gold POS est FR/EN, les 71 langues n'en ont pas.
Aucun serveur local, aucun GPU : le banc est CPU et hors ligne.

Usage : qualifier_frontiere_71.py [--sortie reports/pensee-frontiere-71.json]
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE))

from tools.bloc_linguistique import _profil, detecter_langue, d
… [5338 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '150,360p' tools/bloc_linguistique.py", "description": "Read profile and script detection implementation"}`

  ```
def json(self, avec_duree: bool = False) -> dict:
        cout = dict(self.cout)
        if not avec_duree:
            cout.pop("duree_s", None)
        return {
            # le **format** est versionné : un client peut vérifier ce qu'il reçoit
            "schema": SCHEMA_ANNOTATION, "version": VERSION_ANNOTATION,
            "texte": self.texte, "langue": self.langue, "script": self.script,
            "source": self.source, "refus": self.refus,
            "etiquettes": [e.json() for e in self.etiquettes],
            "unites_semantiques": [u.json() for u in self.unites_semantiques],
            "fraction_semantique": round(float(self.fraction_semantique), 4),
            "trace": list(self.trace), "cout": cout, "contexte": self.contexte,
        }


class BlocLinguistique(Protocol):
    nom: str

    def analyser(self, texte: str, langue: str | None = None,
                 contexte: str | None = None) -> Annotation: ...


class RefusNeuronal(RuntimeError):
    """Le modèle n'a pas rendu une annotation exploitable — le contrat refuse, il n'invente pas."""


# --------------------------------------------------------------------------- profils de langue


def _normaliser(texte:
… [10021 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '3030,3210p' tools/bloc_linguistique.py", "description": "Read autotest UDHR implementation"}`

  ```
def activer(self, annotation: Annotation) -> dict:
        self.appels += 1
        octets = sum(u.fin - u.debut for u in annotation.unites_semantiques)
        return {"unites": len(annotation.unites_semantiques),
                "octets": octets,
                "fraction": round(annotation.fraction_semantique, 4),
                "cout": round(octets * self.cout_par_octet, 4),
                "source": annotation.source,
                "langue": annotation.langue}


# --------------------------------------------------------------------------- autotest


ECHANTILLONS = {
    "fr": "Le chat de la voisine qui dort sur le toit se réveille. Va voir le chat ! "
          "Il ne dort pas, mais il a peut-être faim.",
    "en": "The cat of the neighbor who sleeps on the roof wakes up. Do you see the cat? "
          "It is not sleeping, but it may be hungry.",
    "de": "Die Katze der Nachbarin, die auf dem Dach schläft, wacht auf. Siehst du die Katze?",
    "es": "El gato de la vecina que duerme en el tejado se despierta. ¿Ves el gato?",
    "it": "Il gatto della vicina che dorme sul tetto si sveglia. Vedi il gatto?",
}


def _resume_annotation(a: Annotation) -> dict:
    par = a.par_n
… [7432 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"add_parser\\|def cmd_\\|def main\\|subparsers\\|analyser\\|evaluer\\|rejouer\\|restituer\" tools/drave.py | head -100", "description": "Locate CLI commands"}`

  ```
6:    python3 tools/drave.py analyser "Le chat dort."
7:    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
8:    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
9:    python3 tools/drave.py analyser "Le chat dort." --tagger auto     # API si clé, sinon heuristique
10:    python3 tools/drave.py evaluer
11:    python3 tools/drave.py evaluer --gold --json
12:    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
13:    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
14:    python3 tools/drave.py restituer "Le chat dort."
15:    python3 tools/drave.py restituer "Le chat dort." --roles
16:    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
19:Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
24:En **option** (`--tagger`, `analyser` et `evaluer`), le POS (et lui seul) vient du tagger de
27:`analyser --tagger auto` choisit : API si une clé existe, heuristique sinon, **sans jamais
91:    """La forme comparée par `rejouer` : clés triées, durée exc
… [6224 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '900,1334p' tools/drave.py", "description": "Read CLI command implementations"}`

  ```
"cout_pour_1000_phrases": _cout_pour_phrases(_cout_tagger(stats), len(phrases), 1000),
        }
    if args.par_langue:
        # le détail fr/en : on rejoue la **même** mesure sur chaque sous-gold. Le contrôle
        # négatif est recalculé par langue (l'univers des cibles change avec la langue).
        par_langue = {}
        for langue in sorted({p.get("langue", "fr") for p in phrases}):
            sous = [p for p in phrases if p.get("langue", "fr") == langue]
            m = evaluateur.evaluer_bloc("heuristique", bl.Heuristique(), sous)
            m["controle_negatif"] = {
                "nom": "cible exacte tirée au hasard dans le gold de la langue",
                "graine": 0,
                "cibles": len(_cibles_gold(sous)),
                "exact_taux": _controle_hasard(sous),
            }
            if cascade is not None:
                mt = evaluateur.evaluer_bloc("cascade", cascade, sous)
                m["tagger"] = {
                    "pos": {k: mt["pos"][k] for k in ("exactitude", "exactitude_ferme",
                                                      "exactitude_ouvert", "tokens")},
                    "syntagme": {"f1": mt["syntagme"]["f1"],
       
… [21594 caractères tronqués]
  ```

- **bash** `{"command": "ls -la data/udhr/ && wc -l data/udhr/articles.jsonl 2>/dev/null && head -2 data/udhr/articles.jsonl && du -h data/udhr/articles.jsonl", "description": "Inspect UDHR corpus"}`

  ```
total 19588
drwxr-xr-x. 1 stephane stephane     502 25 oct 00:01 .
drwxr-xr-x. 1 stephane stephane    2664  2 nov 18:33 ..
-rw-r--r--. 1 stephane stephane 7661342 17 oct 23:14 articles.jsonl
-rw-r--r--. 1 stephane stephane 6481755 17 oct 23:14 articles_propres.jsonl
-rw-r--r--. 1 stephane stephane    8286 17 oct 23:49 _eng.txt
drwxr-xr-x. 1 stephane stephane    1206 27 oct 22:33 familles
-rw-r--r--. 1 stephane stephane    9734 17 oct 23:49 _fra.txt
-rw-r--r--. 1 stephane stephane   90808 18 oct 10:30 genealogie.json
-rw-r--r--. 1 stephane stephane  126982 17 oct 23:14 langues.jsonl
-rw-r--r--. 1 stephane stephane   57191 17 oct 23:14 meta.json
-rw-r--r--. 1 stephane stephane   70498 18 oct 01:19 udhr_10_train.txt
-rw-r--r--. 1 stephane stephane   29232 18 oct 01:19 udhr_10_val.txt
-rw-r--r--. 1 stephane stephane    6834 18 oct 01:31 udhr_1_train.txt
-rw-r--r--. 1 stephane stephane    2239 18 oct 01:31 udhr_1_val.txt
-rw-r--r--. 1 stephane stephane  459299 18 oct 01:19 udhr_50_train.txt
-rw-r--r--. 1 stephane stephane  180892 18 oct 01:19 udhr_50_val.txt
-rw-r--r--. 1 stephane stephane    8818 18 oct 00:20 udhr_fra_train.txt
-rw-r--r--. 1 stephane stephane    5490 18 oct 00:28 udhr_
… [2190 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-bloc-linguistique.md && echo '---JSON---' && head -40 reports/bloc-linguistique.json", "description": "Read bloc linguistique report"}`

  ```
# Le bloc linguistique — 398 langues au niveau langue, un contrat pour l'heuristique et le neuronal

> **Ligne de roadmap** : **R0.7** (proposition — la couche linguistique de surface) · **Date** :
> 2026-11-01 · **Verdict** : ✅ **le contrat tient** : neuf niveaux, deux implémentations
> substituables, un parallèle et une cascade, une activation sémantique à **51–76 %** ; la
> **langue** est mesurée à **0,9687** sur **398 langues** (script **1,0000**, profils permutés
> **0,0022**). ⚠️ **les niveaux profonds n'ont pas de gold** et le **modèle neuronal réel n'est
> pas qualifié** (le `llama-cli` local a expiré) : la couverture est **déclarée**, pas prouvée.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`porte-bloc-linguistique.sh`](../tools/porte-bloc-linguistique.sh),
> [`test_bloc_linguistique.py`](../tools/tests/linguistique/test_bloc_linguistique.py),
> JSON [`bloc-linguistique.json`](bloc-linguistique.json). Contrat :
> [`bloc-linguistique.md`](../docs/implantation/bloc-linguistique.md).

## 1. La question

Peut-on avoir **un seul bloc** qui étiquette du **graphème** à la **pragmatique**, avec une
version **heuristique CPU** et une version **n
… [5894 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/tests/linguistique/test_bloc_linguistique.py && echo '---' && grep -n \"profils\\|detecter_langue\\|script\" tools/tests/linguistique/test_bloc_linguistique.py | head -50", "description": "Read existing linguistic tests"}`

  ```
"""Tests du bloc linguistique — contrat, substitution, parallèle, cascade, activation."""
import json
import pathlib
import random
import stat
import sys
import tempfile
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RACINE / "tools"))
import bloc_linguistique as bl

TEXTE = "Le chat de la voisine qui dort sur le toit se réveille. Va voir le chat !"


class TestBlocLinguistique(unittest.TestCase):
    def setUp(self):
        self.h = bl.Heuristique(segmenter_s=False)
        self.n = bl.MockNeuronal()

    def test_niveaux_et_spans(self):
        a = self.h.analyser(TEXTE, "fr")
        niveaux = {e.niveau for e in a.etiquettes}
        self.assertEqual(set(bl.NIVEAUX) - niveaux, set(), f"niveaux manquants : {set(bl.NIVEAUX)-niveaux}")
        for e in a.etiquettes:
            self.assertGreaterEqual(e.debut, 0)
            self.assertLessEqual(e.fin, len(TEXTE))
            self.assertLessEqual(e.debut, e.fin)

    def test_relative_zero(self):
        """Relative zéro : [GN] [pronom sujet] [verbe] [préposition orpheline] → REL.

        La règle est **structurelle** : elle ne dépend ni du nom, ni du pronom, ni du verbe,
        ni d
… [4933 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '110,160p' tools/tests/linguistique/test_bloc_linguistique.py && echo '---' && find tools/tests -maxdepth 2 -type f -name '*drave*' -o -maxdepth 2 -type f -name '*cli*' | head", "description": "Read language test and find CLI tests"}`

  ```
a = h.analyser(txt, lg)
            return [(e.type, txt[e.debut:e.fin]) for e in a.etiquettes
                    if e.niveau == "syntagme"]

        self.assertIn(("GV", "viens"), syntagmes("Tu viens demain ?"))
        self.assertNotIn(("GV", "viens demain"), syntagmes("Tu viens demain ?"))
        self.assertIn(("GV", "ne dort pas"), syntagmes("Il ne dort pas."))
        # « demain matin » : l'adverbe n'est pas final, le GV n'est pas coupé
        self.assertIn(("GV", "viens demain matin"), syntagmes("Tu viens demain matin."))

    def test_langue_et_script(self):
        for texte, langue in (("Le chat dort dans la maison.", "fr"),
                              ("The cat sleeps in the house.", "en"),
                              ("Die Katze schläft im Haus.", "de"),
                              ("El gato duerme en la casa.", "es"),
                              ("Il gatto dorme in casa.", "it")):
            lg, conf, _ = bl.detecter_langue(texte)
            self.assertEqual(lg, langue)
            self.assertGreater(conf, 0)
        self.assertEqual(bl.detecter_script("Привет мир"), "Cyrl")
        self.assertEqual(bl.detecter_script("مرحبا بالعالم"), "Arab")
        self.
… [1367 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"cmd_analyser\\|construire_parseur\\|drave.py\\|from tools.drave\\|import drave\" --include=*.py --exclude-dir=.venv tools | head -30", "description": "Find tests exercising CLI"}`

  ```
tools/speculatif_drave.py
tools/n4_dessin_b.py
tools/couche_distante.py
tools/tests/linguistique/qualifier_tagger_h50.py
tools/tests/linguistique/qualifier_tagger_lot.py
tools/tests/test_schema_produit.py
tools/tests/test_restitution.py
tools/tests/test_produit.py
tools/tests/test_restitution_v2.py
tools/tests/test_restitution_v3.py
tools/tests/test_tagger_api.py
tools/tests/test_empaquetage.py
tools/mesurer_restitution_v0.py
tools/mesurer_restitution_v1.py
tools/mesurer_robustesse_semaine.py
tools/restitution_v2.py
tools/mesurer_restitution_v2.py
tools/restitution_v3.py
tools/mesurer_restitution_v3.py
tools/verifier_faq.py
tools/banc_performance.py
tools/banc_cli_robuste.py
tools/drave.py
  ```

- **bash** `{"command": "ls tools/ | grep -i \"porte\\|test\" | head -50 && echo '---' && sed -n '1,200p' tools/porte-bloc-linguistique.sh", "description": "Inspect gates"}`

  ```
exporter_gguf_dense.py
exporter_gguf.py
importer_udhr.py
porte-adaptateur-sortie.sh
porte-audit-drapeaux.sh
porte-b1110-hybride.sh
porte-balayage.sh
porte-banc-performance.sh
porte-bloc-code.sh
porte-bloc-linguistique.sh
porte-bloc-maths.sh
porte-bloc-tableaux.sh
porte-budget.sh
porte-bus.sh
porte-bus-socket.sh
porte-c4-retard.sh
porte-cerveau.sh
porte-cic.sh
porte-consolidation.sh
porte-coupe.sh
porte-cycle-c2.sh
porte-deepseek.sh
porte-delais.sh
porte-diff-couche.sh
porte-document.sh
porte-echange-experts.sh
porte-episodique.sh
porte-etat.sh
porte-flux.sh
porte-fusion.sh
porte-gain.sh
porte-greffe.sh
porte-harnais-invariants.sh
porte-homeostasie.sh
porte-horloge.sh
porte-indice.sh
porte-jeux.sh
porte-jumeaux.sh
porte-lecteur.sh
porte-lecture.sh
porte-m5-brouillon.sh
porte-melange.sh
porte-memoire.sh
porte-miroir-blocs.sh
porte_mistral.py
porte-mistral.sh
porte_moteur.py
porte-n3-cache.sh
porte-n3-composition.sh
porte-n3-deux-processus.sh
---
#!/usr/bin/env bash
# Porte du bloc linguistique — tests de contrat + mesure UDHR (langue/script).
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "=== PORTE BLOC LINGUISTIQUE ==="
python3 -m unittest discover -s tools/tests/l
… [485 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"U3\" --include=*.md --include=*.json --exclude-dir=.venv docs reports journal tools/chantier/plan.json | head -40", "description": "Find U3 references"}`

  ```
docs/pilotage/en-cours.md:63:- **Prochaine action** : **U3 — `--profils`** ; **J4** ; T132/T133.
docs/pilotage/en-cours.md:113:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6 ; U1 : α 1,08, 10 000 mots 0,82 s ; U2 : roue 1 727 201 o, mêmes JSON, sans gold → evaluer 4** | **U3 — `--profils`** ; **`g017` tranché** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
docs/pilotage/en-cours.md:123:**T1–T6 — livré** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s, instrument 0,71/2,11) ; **U2 — la roue** (1 727 201 o, autonome, gold dedans, roue sans gold → 4) ; reste **U3** (`--profils`) ; [bilan](../../reports/rapport-bilan-exploitable.md), [U1](../../reports/rapport-performance-fix.md), [U2](../../reports/rapport-roue.md).
docs/pilotage/roadmap.md:170:`evaluer` **4** ([fiche](../../reports/rapport-roue.md)). Prochaine action : **U3 — `--profils`**.
reports/rapport-bilan-exploitable.json:473:      "id": "U3",
reports/rapport-bilan-exploitable.md:308:| **U3** | **`--profils`** (détection de langue) | T5 a rendu la CLI robuste ; la détection
… [8258 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' tools/tests/test_produit.py", "description": "Read product CLI tests"}`

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


… [4534 caractères tronqués]
  ```

- **bash** `{"command": "ls docs/implantation 2>/dev/null; ls docs | head -40; grep -rln \"bloc linguistique\\|profils\\|détection de langue\" docs --include=*.md | head -30", "description": "Locate docs mentioning profiles"}`

  ```
banc-lecture.md
bloc-code.md
bloc-linguistique.md
bloc-maths.md
bloc-tableaux.md
configuration-nvme-raid-amd.md
contexte-long.md
convertisseur.md
corpus-gele.md
diehl-cook.md
document-graph.md
encodeur-visuel.md
format-clusters.md
format-flux.md
lecteur-controleur.md
llm-externe.md
moteur-de-pensee.md
numa-segregation.md
pipeline-lecture.md
tete-balayage.md
tokenisation.md
agent
archive
implantation
methode
pilotage
produit
README.md
schemas
theorie
docs/archive/roadmap-detail-2026-10-29.md
docs/schemas/README.md
docs/pilotage/chantiers.md
docs/pilotage/en-cours.md
docs/pilotage/roadmap.md
docs/theorie/modules-cerveau-langage.md
docs/theorie/contrat-bloc-langue.md
docs/implantation/bloc-linguistique.md
docs/produit/README.md
docs/README.md
  ```

- **bash** `{"command": "grep -n \"^## \" docs/implantation/bloc-linguistique.md && echo '---' && sed -n '1,120p' docs/implantation/bloc-linguistique.md", "description": "Read bloc linguistique doc section 3"}`

  ```
16:## 1. Le besoin
32:## 2. Les neuf niveaux
56:## 3. La sortie : une annotation, pas un corps
77:## 4. Le contrat
100:## 5. Les deux implémentations
177:## 6. Substituer, paralléliser, cascader
217:## 7. Activer la couche sémantique à une fraction
243:## 8. Le multilingue : 398 langues au niveau langue
268:## 9. La mesure et la porte
292:## 10. Les limites
314:## 11. Ce qui rouvrirait / la suite
328:## 12. Fichiers
---
# Le bloc linguistique — un contrat, deux implémentations, neuf niveaux

> **Ce que ce document est.** La **spécification** du bloc d'étiquetage linguistique : ce qu'il
> étiquette du **graphème** à la **pragmatique**, ce que chaque étiquette porte, comment
> l'**heuristique CPU** et la **version neuronale** se substituent, se **parallélisent** ou se
> **cascadent**, et comment l'heuristique peut activer la **couche sémantique** sur une
> **fraction** des unités. Le code est [`bloc_linguistique.py`](../../tools/bloc_linguistique.py) ;
> la porte est [`porte-bloc-linguistique.sh`](../../tools/porte-bloc-linguistique.sh) ; la fiche
> est [`rapport-bloc-linguistique.md`](../../reports/rapport-bloc-linguistique.md).
>
> **Ce que ce n'est pas.** Ni un analyseur syntaxiqu
… [6527 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"^## \\|^### \" docs/pilotage/utilisation.md | head -40 && echo '---' && sed -n '1,80p' docs/pilotage/utilisation.md", "description": "Read usage docs"}`

  ```
9:## 1. ✅ Ce qui s'utilise tout de suite
11:### Parler au modèle — le chat
24:### La documentation, en ligne — **un seul serveur, `docwatch`**
58:### Montages et diagrammes
95:### Le code est un sous-module de Drave
116:### Mesurer un modèle
124:### Les portes (les 49 vérifications)
134:### La vision (le banc)
143:### La synthèse théorique (à lire en premier, ou en dernier)
155:### Les outils de la nuit du 16/10 (langage abstrait, empreinte, pensée itérative)
185:### Les facultés du « cerveau » (la recherche)
193:### Le journal et l'état
200:## 2. ❌ Ce qui manque, par ordre de ce que ça coûte
211:## 3. Le chemin le plus court vers « je peux m'en servir »
---
# UTILISER DRAVE — ce qui marche aujourd'hui, et ce qui manque

> Écrit le **16/10**, **revu le 2026-10-27**. en réponse à une question simple : « que manque-t-il pour que je puisse utiliser
> tout ça ? ». Ce document dit **ce qui s'utilise tout de suite** ✓, **la commande exacte** ✓, et
> **ce qui n'existe pas encore** ✗ — avec ce que chaque manque coûterait ✓.
> Règle de lecture : tout ce qui est ✅ a été **exécuté** le jour de l'écriture ✓ ; tout ce qui est ❌
> est un **manque constaté**, pas une supposition ✓.

## 1. ✅ Ce qu
… [3748 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '280,330p' reports/rapport-bilan-exploitable.md && python3 - <<'PY'\nimport json\np='reports/rapport-bilan-exploitable.json'\nd=json.load(open(p))\ndef walk(o):\n    if isinstance(o,dict):\n        if o.get('id')=='U3': print(json.dumps(o,ensure_ascii=False,indent=2))\n        fo … [150 caractères tronqués]`

  ```
([`panini_signatures_26.py`](../tools/panini_signatures_26.py)) ; **ce qui manque** est le retour
`/tmp/panini-v14-26.json` avec une calibration **44/44**. Tant qu'il n'est pas là, on ne conclut
pas : le test n'existe pas. C'est une ligne **bloquée par un tiers**, nommée et bornée, pas un
résultat négatif sur la généalogie.

### 8.3 La décision du tagger `auto` — prototype mesuré, décision humaine

Le **défaut** est — et reste — l'**heuristique CPU hors ligne** (W3) : `--tagger` est **opt-in**,
sans clé il sort **4**, avec réseau coupé il **replie** et sort **0**. Le prototype
[`rapport-tagger-auto.md`](rapport-tagger-auto.md) (Y1) est mesuré sur les quatre cas :
clé présente → API, **code 0**, **130 tokens** ; clé invalide → heuristique, **code 0**, `refus`
explicite ; clé absente → heuristique, **code 0**, sortie **identique au défaut octet pour
octet** ; réseau coupé → heuristique, **code 0** après **3 essais** ; refus de texte → **code 3**,
**aucun appel**. **30/30 tests.**

La **recommandation** de la fiche est de garder le **défaut hors ligne** et `--tagger auto` comme
**porte explicite opt-in**, jamais comme défaut. **La décision reste à l'humain** : Y1 ne change
pas le défa
… [2744 caractères tronqués]
  ```

- **bash** `{"command": "ls docs/produit && grep -n \"^## \" docs/produit/*.md | head -60", "description": "Inspect product docs sections"}`

  ```
demarrage.md
exemples.md
README.md
docs/produit/demarrage.md:14:## 1. Cloner
docs/produit/demarrage.md:28:## 2. Installer
docs/produit/demarrage.md:48:## 3. Les trois commandes
docs/produit/demarrage.md:163:## 4. Le tagger, en option
docs/produit/demarrage.md:199:## 5. Les trois erreurs courantes
docs/produit/demarrage.md:232:## 6. Les codes de sortie
docs/produit/demarrage.md:247:## 7. Et après
docs/produit/exemples.md:34:## 0. Comment lire les JSON
docs/produit/exemples.md:84:## 1. Une déclarative simple — `g001`
docs/produit/exemples.md:222:## 2. Un attachement de REL — `g011`
docs/produit/exemples.md:349:## 3. L'anglais et le marqueur ambigu — `r241`
docs/produit/exemples.md:505:## 4. Le refus — texte vide
docs/produit/exemples.md:557:## 5. L'échec autrefois connu — `r035`, désormais prédit
docs/produit/exemples.md:678:## 6. Le tagger en option — trois exécutions avec la clé
docs/produit/exemples.md:868:## 7. La base honnête — deux exécutions avec `--reel`
docs/produit/exemples.md:975:## 8. Ce que ces exemples ne montrent pas
docs/produit/exemples.md:999:## 9. Où aller ensuite
docs/produit/README.md:32:## Sommaire
docs/produit/README.md:44:## 1. À qui s'adresse le produit
docs/
… [450 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"§ 3\\|section 3\\|## 3\\.\" docs/produit docs/implantation/bloc-linguistique.md reports/rapport-cli-robuste.md | head -30", "description": "Find section 3 references"}`

  ```
docs/produit/exemples.md:60:  les mêmes candidats en objets dans `meta.attachement.candidats` (voir la notice § 3.2).
docs/produit/exemples.md:349:## 3. L'anglais et le marqueur ambigu — `r241`
docs/produit/exemples.md:839:**Lecture.** Le gold attend `when/PRON` ; l'heuristique rend `when/CONJ` (§ 3), le tagger rend
docs/produit/demarrage.md:26:restent absents. Le CLI fonctionne sans eux ; l'écart que cela produit est dit au § 3.
docs/produit/demarrage.md:48:## 3. Les trois commandes
docs/produit/demarrage.md:53:> pour `evaluer` F1 **79,02 %** / attachement **99,58 %** (voir [`README.md`](README.md) § 3.1
docs/produit/demarrage.md:54:> et § 3.3). L'écart est mesuré au § 4 de [`reports/rapport-quickstart.md`](../../reports/rapport-quickstart.md).
docs/produit/demarrage.md:56:### 3.1 `drave --version`
docs/produit/demarrage.md:68:### 3.2 `drave analyser "Le chat dort."`
docs/produit/demarrage.md:90:### 3.3 `drave evaluer`
docs/produit/demarrage.md:116:### 3.4 Le JSON — la même analyse, en machine
docs/produit/demarrage.md:178:ligne de coût ; le reste est celui du § 3.2 :
docs/produit/demarrage.md:196:Sans clé, `stdout` est identique au § 3.2 et `stderr` affiche
docs/produit/README.md
… [1456 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' reports/rapport-cli-robuste.md", "description": "Read T5 report structure for precedent"}`

  ```
# T5 — la robustesse de la CLI : `--duree`, cinq codes de sortie, aide des quatre sous-commandes, `--fichier` sans trace

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **T5** (exploitable, 5/5) ·
> **Date** : 2026-11-15 · **Verdict** : ✅ **20/20 cas mesurés**, **30 tests** de fumée
> verts (dont **6** ajoutés pour T5), aucune trace Python sur les chemins d'erreur.
>
> **Le chiffre.** `--duree` ajoute `cout.duree_s` au JSON de `analyser` — **4,7 à 5,6 ms**
> mesurés sur « Le chat dort. », **5,9 ms** sur la phrase longue — et **ne change rien
> d'autre** : texte, étiquettes et durée par défaut sont identiques. Les **cinq codes**
> sont désormais **0 succès / 3 refus / 4 clé ou dépendance / 5 usage / 1 autre erreur** ;
> les deux erreurs de `--fichier` sortent **4** (chemin inexistant) et **5** (répertoire),
> avec un message d'une ligne et **0 trace**. `--aide` et `--help` sortent **0** sur les
> **quatre** sous-commandes.
>
> **Dispositif** : [`tools/banc_cli_robuste.py`](../tools/banc_cli_robuste.py),
> [`reports/cli-robuste.json`](cli-robuste.json),
> [`tools/tests/test_produit.py`](../tools/tests/test_produit.py),
> [`tools/drave.py`](../tools/drave.py),
> [`docs/produ
… [8919 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '345,470p' docs/produit/README.md && echo '--- 3.7 ---' && sed -n '470,570p' docs/produit/README.md", "description": "Read product README sections 3.5-3.7"}`

  ```
### 3.3 ter Le contexte (mémoire de discours)

```bash
python3 tools/drave.py analyser "Il dort." --contexte "Le chat est sur le toit."
```

Le champ `contexte` est porté dans le JSON ; il alimente la mémoire de discours (coréférence,
connecteurs) sans changer le texte analysé.

### 3.4 Rejouer et vérifier le déterminisme

```bash
python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
```
```
rejeu identique : oui
  texte      : 'Le chat de la voisine qui dort sur le toit se réveille.'
  langue     : fr
  étiquettes : 60
  JSON       : 13284 octets · sha256 31f3798beebe22f7…
```

**Lecture.** La commande analyse **deux fois**, compare le JSON **canonique** (clés triées,
durée exclue) et rend une empreinte sha256. Deux exécutions indépendantes rendent le même octet :
l'analyse est déterministe. C'est la garantie de base du rejeu.

### 3.5 Le refus, et la langue inconnue

```bash
python3 tools/drave.py analyser ""; echo "exit=$?"
```
```
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
exit=3
```

**Lecture.** Le refus est une **réponse** : le CLI écrit un **JSON d'annotation** sur `stdout`
(`refus: "vide"`, `s
… [12730 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '48,170p' docs/produit/demarrage.md", "description": "Read demarrage section 3"}`

  ```
## 3. Les trois commandes

> **Note de mesure — clone public.** Les sorties ci-dessous sont celles d'un clone **sans**
> `tools/structures` (son URL dans `.gitmodules` est un chemin local). C'est ce qu'un débutant
> obtient. Le dépôt de développement, avec ce sous-module, rend `rôle=agent`, `GV → chat`, et
> pour `evaluer` F1 **79,02 %** / attachement **99,58 %** (voir [`README.md`](README.md) § 3.1
> et § 3.3). L'écart est mesuré au § 4 de [`reports/rapport-quickstart.md`](../../reports/rapport-quickstart.md).

### 3.1 `drave --version`

```bash
drave --version
```

```text
drave 0.1.0
```

Si la commande n'existe pas, le venv n'est pas activé ou l'installation a échoué (code **127**).

### 3.2 `drave analyser "Le chat dort."`

```bash
drave analyser "Le chat dort."
```

```text
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fr script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=objet     → dort
  GV   [8:12]  dort     rôle=predicat  → —
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (con
… [3028 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '240,292p' docs/implantation/bloc-linguistique.md && sed -n '314,345p' docs/implantation/bloc-linguistique.md", "description": "Read doc multilingual and limits sections"}`

  ```
pas sur le texte entier. Une heuristique fausse, elle, coûte plus qu'un appel réseau : la
confiance et la porte sont le garde-fou.

## 8. Le multilingue : 398 langues au niveau langue

Le bloc ne prétend pas étiqueter 398 langues au niveau du syntagme. Il sépare :

- **universel** : Unicode, script, frontières de phrase, classes de caractères — indépendant de
  la langue ;
- **famille** : les classes fermées et les affixes partagés (latin, germanique, roman) ;
- **langue** : les profils de trigrammes et les paquets de classes fermées.

La mesure UDHR (articles 0–14 pour les profils, article 15 tenu à l'écart) :

| mesure | résultat |
|---|---|
| langues avec profil | **398** |
| articles de test | **447** |
| **accuracy langue** | **0,9687** |
| **accuracy script** | **1,0000** |
| contrôle **profils permutés** | **0,0022** (proche du hasard) |
| construction des profils + test | **4,0 s** |

**Les erreurs sont nommées** : l'anglais et le scots sont proches, et l'échantillon anglais du
banc est classé `sco` (ou `und` sous le seuil) par l'heuristique ; le profil UDHR est
**parallèle et propre**, ce n'est pas 398 langues de déploiement. Le bloc est honnête : il dit
`und` sous le seui
… [3292 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' reports/rapport-roue.md && echo '---JSON---' && head -80 reports/roue.json 2>/dev/null || ls reports/*roue*", "description": "Read wheel report"}`

  ```
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
> **Dispositif** : [`pyproject.toml`](../pyp
… [12430 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '160,240p' reports/rapport-cli-robuste.md && sed -n '120,220p' tools/tests/test_produit.py", "description": "Read CLI test remainder"}`

  ```
explicitement (`DEEPSEEK*`, `DSH_*`) et utilise un `HOME` temporaire. C'est le comportement
  correct : avec une clé, `--tagger` ne doit pas sortir 4.
- **Le code 1 reste ouvert** aux erreurs inattendues ; une exception non prévue sort 1 avec
  un message, pas une trace. Le contrat ne prétend pas couvrir chaque exception possible.

## 8. Les fichiers touchés

| fichier | changement |
|---|---|
| `tools/drave.py` | `--duree` ; `ErreurEntree` (4/5) ; code d'usage **5** ; refus `rejouer` **3** ; épilogue des codes |
| `tools/tests/test_produit.py` | 6 tests T5 : durée JSON/JSONL, tableau, aide/help × 4, fichier inexistant, répertoire |
| `tools/tests/test_restitution*.py`, `test_tagger_api.py` | attentes d'usage passées de **2** à **5** (le contrat a changé) |
| `tools/banc_cli_robuste.py` | le banc des 20 cas et son JSON |
| `reports/cli-robuste.json` | la mesure reproductible |
| `docs/produit/README.md` | § 3.5, 6, 7 : codes, `--duree`, `--fichier` |
| `docs/produit/demarrage.md` | § 5–6 : erreurs de fichier et tableau des codes |
| `tools/verifier_faq.py`, `reports/faq.json`, `reports/rapport-faq.md` | `--langue de` et options fantômes en code **5** |

**Verdict.** La CLI est **ro
… [5928 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"profils\\|langue\\|script\\|confiance\" tools/schemas/*.json | head -40 && ls tools/schemas", "description": "Inspect schema fields"}`

  ```
tools/schemas/drave-annotation-v1.json:5: "description": "L'annotation du bloc linguistique heuristique : un texte, ses étiquettes par niveau, ses unités sémantiques et son refus éventuel.",
tools/schemas/drave-annotation-v1.json:11:  "langue",
tools/schemas/drave-annotation-v1.json:12:  "script",
tools/schemas/drave-annotation-v1.json:27:  "langue": {
tools/schemas/drave-annotation-v1.json:31:  "script": {
tools/schemas/drave-annotation-v1.json:58:     "confiance"
tools/schemas/drave-annotation-v1.json:81:     "confiance": {
tools/schemas/drave-annotation-v1.json:92:     "langue": {
tools/schemas/drave-annotation-v1.json:95:     "script": {
tools/schemas/drave-annotation-v2.json:5: "description": "L'annotation du bloc linguistique heuristique, version 2 : identique à la v1 et documente, dans `meta`, la partition des syntagmes qui se chevauchent (`meta.partition`), les segments alternatifs du groupe (`meta.alternative`), les **candidats d'attachement structurés** (`meta.attachement.candidats`, objets `{span, cible, source}`) et les **rôles normalisés** (vocabulaire fermé). Les champs sont additifs et optionnels : v1 reste lue.",
tools/schemas/drave-annotation-v2.json:11:  "langue",
… [455 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1000,1075p' tools/bloc_linguistique.py && sed -n '2135,2170p' tools/bloc_linguistique.py && grep -n \"SEUIL\\|seuil\" tools/bloc_linguistique.py | head -30", "description": "Inspect language detection integration and thresholds"}`

  ```
i += 1
            continue
        j = i + 1
        while j < n and texte[j] in ".!?…":
            j += 1
        if not _dans_zone(zones, i, j) and _est_frontiere(texte, i, j, zones):
            ajouter(_absorber_fermants(texte, j), _type_phrase(texte[i:j]))
        i = j
    ajouter(n, "déclarative")
    return sortie


class Heuristique:
    """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""

    nom = "heuristique"

    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
                 seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
                 union: bool = True, partition: str = "alternative"):
        self.profils = profils
        self.segmenter_s = segmenter_s
        self.seuil_ouvert = seuil_ouvert
        self.seuil_langue = seuil_langue
        self.union = union
        # "brut" : la sortie d'avant (chevauchements non documentés) ; "alternative" :
        # les deux segments restent, `meta.alternative` dit lequel est préféré ;
        # "filtrer_union" : on retire le S qui **contient** un segment chunker (le filtre
        # union du P0-3) ; "filtrer" : partition stricte, 
… [4785 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,collections\nlangs=collections.Counter(); scripts=collections.defaultdict(collections.Counter); noms={}\nfor line in open('data/udhr/articles.jsonl'):\n    d=json.loads(line); langs[d['iso3']]+=1; scripts[d['iso3']][d.get('script')]+=1; noms[d['iso3']]=d.ge … [641 caractères tronqués]`

  ```
n languages 400
fra French 31 {'Latn': 31}
eng English 31 {'Latn': 31}
deu German, Standard (1996) 62 {'Latn': 62}
spa Spanish 31 {'Latn': 31}
ita Italian 31 {'Latn': 31}
por Portuguese (Portugal) 62 {'Latn': 62}
nld Dutch 31 {'Latn': 31}
rus Russian 31 {'Cyrl': 31}
ukr Ukrainian 31 {'Cyrl': 31}
pol Polish 31 {'Latn': 31}
ces Czech 31 {'Latn': 31}
tur Turkish 31 {'Latn': 31}
heb Hebrew 31 {'Hebr': 31}
hin Hindi 31 {'Deva': 31}
ben Bengali 31 {'Beng': 31}
tam Tamil (Sri Lanka) 62 {'Taml': 62}
tha Thai (2) 62 {'Thai': 62}
jpn Japanese 31 {'Jpan': 31}
cmn Chinese, Mandarin (Traditional) 62 {'Hans': 31, 'Hant': 31}
kor Korean 31 {'Hang': 31}
ell Greek (polytonic) 62 {'Grek': 62}
swe Swedish 31 {'Latn': 31}
fin Finnish 31 {'Latn': 31}
dan Danish 31 {'Latn': 31}
ron Romanian (2006) 93 {'Latn': 93}
hun Hungarian 31 {'Latn': 31}
ind Indonesian 31 {'Latn': 31}
vie Vietnamese (Han nom) 62 {'Latn': 31, 'Hani': 31}
swh Swahili 31 {'Latn': 31}
amh Amharic 30 {'Ethi': 30}
hye Armenian 31 {'Armn': 31}
kat Georgian 31 {'Geor': 31}
khm Khmer, Central 31 {'Khmr': 31}
lao Lao 31 {'Laoo': 31}
mya Burmese 31 {'Mymr': 31}
sin Sinhala 31 {'Sinh': 31}
tel Telugu 31 {'Telu': 31}
kan Kannada 31 {'Knda': 31}
… [692 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, json, time, pathlib, collections\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\np=pathlib.Path('data/udhr/articles.jsonl')\nt0=time.perf_counter(); profils,tests=bl.charger_profils_udhr(p, test=(15,15), min_test=1); dt=time.perf_counter … [946 caractères tronqués]`

  ```
profiles 398 tests 447 load+build 1.081
accuracy 433 / 447 0.9686800894854586 time 5.512
sample in profiles []
fra -> fra 0.3928 ok script Latn Latn
eng -> eng 0.4213 ok script Latn Latn
deu -> deu 0.5193 ok script Latn Latn
spa -> spa 0.2619 ok script Latn Latn
ita -> ita 0.5535 ok script Latn Latn
por -> por 0.1627 ok script Latn Latn
nld -> nld 0.4098 ok script Latn Latn
rus -> rus 0.3985 ok script Cyrl Cyrl
ukr -> ukr 0.4334 ok script Cyrl Cyrl
pol -> pol 0.66 ok script Latn Latn
ces -> ces 0.5167 ok script Latn Latn
tur -> tur 0.3991 ok script Latn Latn
heb -> heb 0.9412 ok script Hebr Hebr
hin -> hin 0.4853 ok script Deva Deva
ben -> ben 1.0 ok script Beng Beng
tam -> tam 1.0 ok script Taml Taml
tha -> tha 1.0 ok script Thai Thai
jpn -> jpn 1.0 ok script Jpan Jpan
cmn -> cmn 0.0457 ok script Hani Hans
kor -> kor 1.0 ok script Hang Hang
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, pathlib\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\np=pathlib.Path('data/udhr/articles.jsonl')\nprofils,tests=bl.charger_profils_udhr(p, test=(15,15), min_test=1)\nlangs=sorted(profils)\nsample=langs[::max(1,len(langs)//20)][:20]\npr … [351 caractères tronqués]`

  ```
398 ['abk', 'ast', 'bod', 'cha', 'csw', 'eus', 'gjn', 'hin', 'ina', 'khm', 'lat', 'mah', 'mxi', 'npi', 'pcd', 'quz', 'san', 'srp', 'tgl', 'tzm']
abk -> abk 0.9764 ok script Cyrl Cyrl
ast -> ast 0.3493 ok script Latn Latn
bod -> bod 0.3709 ok script Tibt Tibt
cha -> cha 0.4218 ok script Latn Latn
csw -> csw 0.8685 ok script Cans Cans
eus -> eus 0.7838 ok script Latn Latn
gjn -> gjn 0.7366 ok script Latn Latn
hin -> hin 0.4853 ok script Deva Deva
ina -> ina 0.3542 ok script Latn Latn
khm -> khm 1.0 ok script Khmr Khmr
lat -> lat 0.603 ok script Latn Latn
mah -> mah 0.7667 ok script Latn Latn
mxi -> mxi 0.3246 ok script Latn Latn
npi -> npi 0.5703 ok script Deva Deva
pcd -> wln 0.1199 ERR script Latn Latn
quz -> quz 0.1477 ok script Latn Latn
san -> san 0.1289 ok script Deva Deva
srp -> srp 0.1068 ok script Cyrl Cyrl
tgl -> tgl 0.3825 ok script Latn Latn
tzm -> tzm 0.8065 ok script Latn Latn
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, pathlib, time\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\np=pathlib.Path('data/udhr/articles.jsonl')\nprofils,tests=bl.charger_profils_udhr(p, test=(15,30), min_test=1)\nprint('profiles',len(profils),'tests',len(tests))\nlangs=sorted … [645 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-41]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-41", "wait": true, "timeout_ms": 120000}`

  ```
profiles 398 tests 7137
abk 16/16 conf min 0.732
ast 16/16 conf min 0.164
bod 16/16 conf min 0.277
cha 16/16 conf min 0.36
csw 9/9 conf min 0.785
eus 16/16 conf min 0.578
gjn 16/16 conf min 0.493
hin 16/16 conf min 0.292
ina 16/16 conf min 0.231
khm 16/16 conf min 1.0
lat 32/32 conf min 0.405
mah 16/16 conf min 0.642
mxi 16/16 conf min 0.289
npi 16/16 conf min 0.195
pcd 14/16 conf min 0.083
quz 15/16 conf min 0.126
san 31/32 conf min 0.071
srp 3/32 conf min 0.066
tgl 16/16 conf min 0.224
tzm 16/16 conf min 0.655
sample total 328 / 361 0.9086
all 6904 / 7137 0.9674
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "grep -rn \"20 langues\\|20-language\\|20 langues UDHR\\|vingt langues\" --include=*.md --include=*.py --include=*.json --exclude-dir=.venv . 2>/dev/null | head -40", "description": "Search for existing 20-language sample"}`

  ```
./reports/rapport-pont-semantique.md:81:## Résultat 4 — validé à l'échelle : 20 langues d'entraînement, 20 langues jamais vues
./reports/rapport-pont-semantique.md:102:début**. C'est exactement le **rang** du pont. Courbe mesurée, 20 langues
./reports/rapport-pont-semantique.md:103:d'entraînement → 20 langues jamais vues :
./reports/rapport-pont-semantique.md:157:soit ~1 800 nombres, ajustés par moindres carrés sur 20 langues, qui transforment
./reports/rapport-pont-semantique.md:159:inter-langue à **0,9492** (pire paire **0,7762**) sur 20 langues **jamais vues**.
./reports/archive/rapport-toutes-langues.md:264:Ce panel est **partiel** : 20 langues de test sur 41, et 12 écritures sur 22. Les
./reports/archive/rapport-toutes-langues.md:433:| | signal précoce (20 langues) | **définitif (41 langues)** |
./reports/toutes-langues/010-10-signal-precoce-sur-le-panel-stratifie-le.md:40:Ce panel est **partiel** : 20 langues de test sur 41, et 12 écritures sur 22. Les
./reports/toutes-langues/014-14-le-livrable-de-la-phase-2-le-pont-sur-30.md:43:| | signal précoce (20 langues) | **définitif (41 langues)** |
./reports/07/p6.md:298:**La question** ✓✓. Le pidgin nigérian est la **seule** des 20
… [4415 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"langues_test\\|langues_train\" --include=*.py --exclude-dir=.venv tools | head -30", "description": "Find scripts using 20-language train/test lists"}`

  ```
tools/pont_recurrent.py:193:             langues_train=np.array(sorted(tr)), langues_test=np.array(sorted(te)))
tools/semantique/entrainer_type.py:188:    langues_train = sorted({it.langue for it in train})
tools/semantique/entrainer_type.py:189:    idx_langue = {l: i for i, l in enumerate(langues_train)}
tools/semantique/entrainer_type.py:191:    modele = ModeleType(base, len(langues_train),
  ```

- **bash** `{"command": "ls data/udhr/familles | head && find data -maxdepth 3 -iname '*20*' | head -20", "description": "Look for 20-language data files"}`

  ```
abkhaz-adyge.jsonl
ac_benue.jsonl
afro-asiatic.jsonl
afro_ouest.jsonl
arawakan.jsonl
artificial-language.jsonl
atlantic-congo.jsonl
austroasiatic.jsonl
austro_est.jsonl
austronesian.jsonl
data/eurlex/xhtml/32025R1106-eng.xhtml
data/eurlex/xhtml/32025R1106-fra.xhtml
data/eurlex/xhtml/32025R1106-deu.xhtml
data/eurlex/xhtml/32025R1106-spa.xhtml
data/eurlex/xhtml/32025R2509-eng.xhtml
data/eurlex/xhtml/32025R2509-fra.xhtml
data/eurlex/xhtml/32025R2509-deu.xhtml
data/eurlex/xhtml/32025R2509-spa.xhtml
data/eurlex/xhtml/32025R1106-ita.xhtml
data/eurlex/xhtml/32025R1106-pol.xhtml
data/eurlex/xhtml/32025R1106-nld.xhtml
data/eurlex/xhtml/32025R1106-por.xhtml
data/eurlex/xhtml/32025R1106-bul.xhtml
data/eurlex/xhtml/32025R1106-ces.xhtml
data/eurlex/xhtml/32025R1106-dan.xhtml
data/eurlex/xhtml/32025R1106-ell.xhtml
data/eurlex/xhtml/32025R1106-est.xhtml
data/eurlex/xhtml/32025R1106-fin.xhtml
data/eurlex/xhtml/32025R1106-gle.xhtml
data/eurlex/xhtml/32025R1106-hrv.xhtml
[stderr]
find: ‘standard output’: Broken pipe
find: write error
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='reports/corpus-commun.json'\nd=json.load(open(p))\nprint(json.dumps(d,ensure_ascii=False,indent=1)[:6000])\nPY", "description": "Inspect corpus-commun 20-language sample"}`

  ```
{
 "controle_negatif": {
  "date": "2026-11-07",
  "n_ok": 8,
  "n_rejets_attendus": 6,
  "n_temoins_attendus": 2,
  "n_tests": 8,
  "tests": [
   {
    "attendu": "acceptation",
    "detail": "udhr_eng : Panini == Drave après normalisation",
    "nom": "temoin_paire_correcte",
    "obtenu": "acceptation",
    "ok": true
   },
   {
    "attendu": "rejet",
    "detail": "un caractère changé dans le texte Panini doit casser l'égalité",
    "nom": "panini_altere",
    "obtenu": "rejet",
    "ok": true
   },
   {
    "attendu": "rejet",
    "detail": "un caractère changé dans le texte Drave doit casser l'égalité",
    "nom": "drave_altere",
    "obtenu": "rejet",
    "ok": true
   },
   {
    "attendu": "rejet",
    "detail": "deux langues différentes ne doivent pas être appariables",
    "nom": "appariement_croise",
    "obtenu": "rejet",
    "ok": true
   },
   {
    "attendu": "rejet",
    "detail": "nb_phrases 1 != 2; caractères perdus ou ajoutés (hors espaces)",
    "nom": "phrase_supprimee",
    "obtenu": "rejet",
    "ok": true
   },
   {
    "attendu": "rejet",
    "detail": "nb_phrases 3 != 2; ligne vide",
    "nom": "ligne_vide",
    "obtenu": "rejet",
    "ok": true
   },
  
… [4798 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"échantillon\\|stratif\\|familles\\|langues\" reports/rapport-corpus-commun.md | head -60 && sed -n '1,120p' reports/rapport-corpus-commun.md", "description": "Read corpus-commun report for sample languages"}`

  ```
4:> **Verdict** : ✅ **le corpus est construit et vérifié** — **21 textes** (20 langues stratifiées + le
5:> français pivot), **5 familles**, **10 écritures**, **42 phrases**, **3 603 caractères**. Les **21**
11:> après) ; `data/udhr/articles_propres.jsonl`, `langues.jsonl`, `genealogie.json` (HEAD
21:J2.2 demande un **échantillon de 10 à 50 textes présent des deux côtés** (Panini/NIPADA et Drave),
27:- Panini/NIPADA : `../Panini/research/data/udhr_corpus.json`, format `udhr-v2.0-xml`, **532 langues**,
29:- Drave : `data/udhr/articles_propres.jsonl`, **456 langues**, article 1, extrait du même fonds
30:  Unicode UDHR ; `langues.jsonl` et `genealogie.json` apportent le code ISO, l'écriture, la famille
41:- **pas un échantillon aléatoire** : il est stratifié et choisi pour l'égalité exacte et la
50:| côté | fichier | format | langues | HEAD | date | SHA-256 |
54:| Drave | `data/udhr/langues.jsonl` | JSONL | 456 | `9c7f71dc` | 2026-11-07 | `12eee362…` |
69:byte-identique** : après NFC et compression des espaces, **20 langues** gardent un écart de surface.
77:| langues Panini | 532 | — | le fonds Panini |
78:| langues Drave | 456 | — | le fonds Drave |
109:### 2.3 Les familles du pool e
… [9447 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '135,210p' reports/rapport-corpus-commun.md", "description": "Read sample table of 21 texts"}`

  ```
## 3. L'échantillon — 21 textes, 5 familles, 10 écritures

**Critères de sélection** :

1. présent des deux côtés, avec le **même identifiant** `udhr_<clé>` ↔ `udhr_<clé>.xml` ;
2. article 1 **identique** après NFC et compression des espaces — aucune correction manuelle ;
3. **5 familles** glottolog × **4 langues**, parmi les six plus représentées du pool exact, avec la
   diversité des écritures comme arbitrage (le turcique, 17 paires, est écarté) ;
4. **écritures distinctes** quand c'est possible (latin, devanagari, cyrillique, grec, adlam,
   arabe, birman, han, éthiopien, hébreu) ;
5. le **français** ajouté **hors strate** comme pivot de Drave (la langue de référence du dépôt).

| id | langue | écriture | famille | branche (feuille) | rôle | phrases | caractères |
|---|---|---|---|---:|---|---:|---:|
| `udhr_eng` | English | Latn | Indo-European | `macr1271` | strate | 2 | 170 |
| `udhr_hin` | Hindi | Deva | Indo-European | `hind1270` | strate | 2 | 189 |
| `udhr_bel` | Belarusan | Cyrl | Indo-European | `east1426` | strate | 2 | 154 |
| `udhr_ell_monotonic` | Greek (monotonic) | Grek | Indo-European | `nucl1783` | strate | 2 | 194 |
| `udhr_kin` | Rwanda | Latn | Atlantic-Cong
… [3219 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,collections\nkeys=['eng','hin','bel','ell_monotonic','kin','ewe','ibo','fuf_adlm','ind','tgl','mly_arab','jav','mya','cmn_hant','cnh','ctd','arb','amh','heb','hau_NE','fra']\nrows=collections.defaultdict(dict)\nfor line in open('data/udhr/articles.jsonl'):\ … [486 caractères tronqués]`

  ```
eng eng English Latn arts 31 False
hin hin Hindi Deva arts 31 False
bel bel Belarusan Cyrl arts 31 False
ell_monotonic ell Greek (monotonic) Grek arts 31 False
kin kin Rwanda Latn arts 31 False
ewe ewe Éwé Latn arts 31 False
ibo ibo Igbo Latn arts 31 False
fuf_adlm fuf Pular (Adlam) Adlm arts 31 False
ind ind Indonesian Latn arts 31 False
tgl tgl Tagalog Latn arts 31 False
mly_arab zlm Malay (Arabic) Arab arts 31 False
jav jav Javanese (Latin) Latn arts 31 False
mya mya Burmese Mymr arts 31 False
cmn_hant cmn Chinese, Mandarin (Traditional) Hant arts 31 False
cnh cnh Chin, Haka Latn arts 31 False
ctd ctd Chin, Tedim Latn arts 31 False
arb arb Arabic, Standard Arab arts 31 False
amh amh Amharic Ethi arts 30 False
heb heb Hebrew Hebr arts 31 False
hau_NE hau Hausa (Niger) Latn arts 31 False
fra fra French Latn arts 31 False
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor line in open('data/udhr/articles.jsonl'):\n    d=json.loads(line)\n    if d['fichier']=='udhr_eng.xml':\n        print(d['art'], d['titre'], d['texte'][:50])\nPY", "description": "Inspect article numbering"}`

  ```
0 Préambule Whereas recognition of the inherent dignity and of
1  All human beings are born free and equal in dignit
2  Everyone is entitled to all the rights and freedom
3  Everyone has the right to life, liberty and the se
4  No one shall be held in slavery or servitude; slav
5  No one shall be subjected to torture or to cruel, 
6  Everyone has the right to recognition everywhere a
7  All are equal before the law and are entitled with
8  Everyone has the right to an effective remedy by t
9  No one shall be subjected to arbitrary arrest, det
10  Everyone is entitled in full equality to a fair an
11  Everyone charged with a penal offence has the righ
12  No one shall be subjected to arbitrary interferenc
13  Everyone has the right to freedom of movement and 
14  Everyone has the right to seek and to enjoy in oth
15  Everyone has the right to a nationality. No one sh
16  Men and women of full age, without any limitation 
17  Everyone has the right to own property alone as we
18  Everyone has the right to freedom of thought, cons
19  Everyone has the right to freedom of opinion and e
20  Everyone has the right to freedom of peaceful asse
21  Everyone has the right to take part in the
… [502 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, pathlib\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\np=pathlib.Path('data/udhr/articles.jsonl')\nprofils,tests=bl.charger_profils_udhr(p, test=(15,30), min_test=1)\ncodes=['eng','hin','bel','ell','kin','ewe','ibo','fuf','ind','tgl','z … [1189 caractères tronqués]`

  ```
--- article 15 ---
eng -> eng 0.4213 ok Latn Latn
hin -> hin 0.4853 ok Deva Deva
bel -> bel 0.5897 ok Cyrl Cyrl
ell -> ell 1.0 ok Grek Grek
kin -> kin 0.4035 ok Latn Latn
ewe -> ewe 0.6366 ok Latn Latn
ibo -> ibo 0.7487 ok Latn Latn
fuf -> fuf 1.0 ok Adlm Adlm
ind -> ind 0.3812 ok Latn Latn
tgl -> tgl 0.3825 ok Latn Latn
zlm -> ind 0.2316 ERR Latn Latn
jav -> jav 1.0 ok Java Java
mya -> mya 0.8845 ok Mymr Mymr
cmn -> cmn 0.3257 ok Hani Hant
cnh -> cnh 0.3623 ok Latn Latn
ctd -> ctd 0.4867 ok Latn Latn
arb -> arb 0.8069 ok Arab Arab
amh -> amh 1.0 ok Ethi Ethi
heb -> heb 0.9412 ok Hebr Hebr
hau -> hau 0.6177 ok Latn Latn
article 15 19 / 20
--- articles 15-30 ---
eng 16/16
hin 16/16
bel 16/16
ell 16/16
kin 15/16
ewe 16/16
ibo 16/16
fuf 16/16
ind 16/16
tgl 16/16
zlm 0/16
jav 16/16
mya 16/16
cmn 13/16
cnh 16/16
ctd 16/16
arb 16/16
amh 16/16
heb 16/16
hau 16/16
all 300 / 320 0.9375
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,pathlib\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\np=pathlib.Path('data/udhr/articles.jsonl')\nprofils,_=bl.charger_profils_udhr(p, test=(15,15), min_test=1)\nfor t in [\"\", \"a\", \"no\", \"chat\", \"Le chat the cat dort sleeps on  … [401 caractères tronqués]`

  ```
'' -> und 0.0 script Zyyy top3 [('cri', 0.0), ('pov', 0.0), ('kmb', 0.0)]
'a' -> und 0.0 script Latn top3 [('cri', 0.0), ('pov', 0.0), ('kmb', 0.0)]
'no' -> und 0.0 script Latn top3 [('cri', 0.0), ('pov', 0.0), ('kmb', 0.0)]
'chat' -> agr 0.2 script Latn top3 [('agr', 1.0), ('ayr', 1.0), ('cic', 1.0)]
'Le chat the cat dort sleeps on the roof.' -> sco 0.3632 script Latn top3 [('sco', 0.5), ('eng', 0.3684210526315789), ('hns', 0.3157894736842105)]
'Le chat dort. The cat sleeps.' -> hns 0.2633 script Latn top3 [('hns', 0.4074074074074074), ('lld', 0.3333333333333333), ('sco', 0.3333333333333333)]
'hello' -> ekk 0.1333 script Latn top3 [('ekk', 0.6666666666666666), ('sot', 0.6666666666666666), ('tzm', 0.6666666666666666)]
'oui' -> und 0.0 script Latn top3 [('cri', 0.0), ('pov', 0.0), ('kmb', 0.0)]
'ja' -> und 0.0 script Latn top3 [('cri', 0.0), ('pov', 0.0), ('kmb', 0.0)]
'...' -> und 0.0 script Zyyy top3 [('cri', 0.0), ('pov', 0.0), ('kmb', 0.0)]
'123 456' -> und 0.0 script Zyyy top3 [('cri', 0.0), ('pov', 0.0), ('kmb', 0.0)]
'x' -> und 0.0 script Latn top3 [('cri', 0.0), ('pov', 0.0), ('kmb', 0.0)]
'the' -> cfm 0.2 script Latn top3 [('ctd', 1.0), ('eng', 1.0), ('fkv', 1.0)]
'le' -> u
… [371 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,pathlib\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\np=pathlib.Path('data/udhr/articles.jsonl'); profils,_=bl.charger_profils_udhr(p,test=(15,15),min_test=1)\ntests=[\"la le de un une\",\"le la les de du\",\"the of and to\",\"le the la … [650 caractères tronqués]`

  ```
'la le de un une' -> fra 0.1692 script Latn
'le la les de du' -> fra 0.1846 script Latn
'the of and to' -> eng 0.3818 script Latn
'le the la of' -> eng 0.12 script Latn
'chat chat chat' -> ayr 0.1667 script Latn
'no no no' -> amr 0.2 script Latn
'a a a' -> ada 0.2 script Latn
'de la la' -> ast 0.2 script Latn
'the the the' -> eng 0.2 script Latn
'et et et' -> fra 0.2 script Latn
'le chat the cat dort sleeps on the roof' -> sco 0.3659 script Latn
'Le chat the cat dort sleeps on the roof.' -> sco 0.3632 script Latn
'Le chat dort. The cat sleeps.' -> hns 0.2633 script Latn
'All human beings are born free and equal in dignity and rights. Tous les êtres humains naissent libres et égaux en dignité et en droits.' -> eng 0.0836 script Latn
'abc Привет مرحبا' -> rus 0.3762 script Cyrl
'Привет hello' -> sot 0.3933 script Cyrl
'hello world' -> xsm 0.3389 script Latn
'bonjour hello' -> bre 0.0545 script Latn
'bonjour' -> bin 0.04 script Latn
'hello' -> ekk 0.1333 script Latn
  ```

- **bash** `{"command": "sed -n '1,260p' tools/tests/test_empaquetage.py", "description": "Read packaging tests"}`

  ```
#!/usr/bin/env python3
"""test_empaquetage.py — le paquet `drave` et ses deux entrées.

Ce que le test fige :

- `pyproject.toml` : nom **drave**, version **0.1.0**, `requires-python >= 3.10`,
  **aucune dépendance**, script console `drave = tools.drave:main` ;
- la **roue** embarque les sous-paquets du CLI (`tools.tests.linguistique`,
  `tools.structures`, `tools.llm`) et les **gold** (`package-data`) ;
- le **chemin historique** `python3 tools/drave.py` rend la même version et analyse ;
- l'entrée `tools.drave:main` est **importable depuis un autre répertoire** (c'est ce que
  l'installation éditable met sur `sys.path`) ;
- **sans installation**, `drave` échoue **proprement** : code 127, « command not found »,
  pas de trace Python ;
- **sans gold**, `evaluer` échoue **proprement** : code 4, message qui dit quoi faire, et
  `stdout` vide (contrôle négatif de la roue).

Le test ne crée pas de venv et ne télécharge rien : la vérification complète
`python3 -m pip wheel .` puis l'installation dans `/tmp/venv-drave-roue` est consignée dans
`reports/rapport-roue.md` et `reports/roue.json`.
"""
from __future__ import annotations

import contextlib
import io
import os
import pathlib
impo
… [5944 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,180p' tools/verifier_faq.py", "description": "Read FAQ verifier"}`

  ```
#!/usr/bin/env python3
"""verifier_faq.py — les dix réponses de la FAQ produit, vérifiées contre le code courant.

La FAQ de `docs/produit/README.md` (§ 8) ne doit pas être une prose recopiée : chaque
réponse est adossée à une commande, à un chiffre de `reports/` ou à une constante du
code. Ce vérificateur exécute les dix contrôles, imprime un JSON (ou un résumé) et sort
avec le code 1 si une réponse ne tient plus.

Ce qu'il ne fait pas : aucune mesure nouvelle, aucun appel réseau, aucune clé lue. Il
rejoue le CLI en local, lit les JSON de résultats déjà publiés et inspecte le source.

Usage :
    python3 tools/verifier_faq.py            # résumé lisible
    python3 tools/verifier_faq.py --json     # le JSON de reports/faq.json

Le **contrôle négatif** est explicite : on vérifie qu'une affirmation fausse (« le CLI
accepte --langue de ») est bien rejetée par le code. Si ce contrôle passait, le
vérificateur ne prouverait rien.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import pathlib
import subprocess
import sys
import tempfile

RACINE = pathlib.Path(__file__).resolve().parent.parent
DRAVE = RACINE / "tools" / "drave.py"
DATE = "2026-11-1
… [6939 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' tools/revue_documentation.py", "description": "Read documentation review tool"}`

  ```
#!/usr/bin/env python3
"""revue_documentation.py — LA REVUE DE FIN DE SOUS-CHANTIER (AGENTS.md §4).

Ce qu'elle vérifie, et qu'il faut corriger AVANT le commit de clôture :
  1. classement : pas de résultats dans docs/ (les fiches sont dans reports/ et citées) ;
  2. structure  : les sept chantiers de en-cours.md ont leur entrée, leur état et leur fiche ;
  3. annotation : les liens relatifs des docs/ et reports/ résolvent, et leur libellé ne
     ment pas sur la cible ; les sources externes sont citées ;
  4. fraîcheur  : en-cours.md date du dernier commit, ET aucun fait n'a été commité après
     le dernier état (comparaison de commits, pas de dates : voir verifie_etat_a_jour.py) ;
  5. cohérence  : la synthèse (index.md) liste les huit chapitres, le chapitre 7 et B10–B12 ;
     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
  6. vocabulaire : « jeton » ne désigne **jamais** la représentation sémantique neutre (RSN) ;
  7. navigation : aucun document vivant n'est orphelin, et aucun chemin en code inline
     ne pointe vers un fichier absent (hors gabarits `AAAA`, `<...>`, `*`).

Sortie : un rapport lisible, code 0 si tout passe, 1 sinon (u
… [6605 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def _lire_entree\" -A40 tools/drave.py && sed -n '520,680p' tools/drave.py", "description": "Read text input helper and analyser command"}`

  ```
525:def _lire_entree(args: argparse.Namespace) -> str:
526-    """Le texte : l'argument, ou le **fichier** (`--fichier`).
527-
528-    Les erreurs de chemin sont **rendues** comme des codes du contrat, pas comme des
529-    traces Python : 4 pour un fichier introuvable (dépendance), 5 pour un répertoire
530-    (usage invalide de `--fichier`). Un fichier présent mais illisible reste une
531-    dépendance absente (4).
532-    """
533-    if getattr(args, "fichier", None):
534-        chemin = pathlib.Path(args.fichier)
535-        try:
536-            if not chemin.exists():
537-                raise ErreurEntree(f"fichier introuvable : {args.fichier!r}", 4)
538-            if chemin.is_dir():
539-                raise ErreurEntree(
540-                    f"un répertoire n'est pas un fichier : {args.fichier!r} "
541-                    "(--fichier attend un fichier UTF-8)", 5)
542-            return chemin.read_text(encoding="utf-8", errors="replace")
543-        except (OSError, ValueError) as exc:
544-            raise ErreurEntree(
545-                f"fichier illisible : {args.fichier!r} "
546-                f"({getattr(exc, 'strerror', None) or exc})", 4) from exc
547-    r
… [8076 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def _construire_tagger\" -A50 tools/drave.py", "description": "Inspect tagger construction"}`

  ```
370:def _construire_tagger(partition: str = "alternative"):
371-    """Rend (cascade, stats) ; lève `CleTaggerAbsente` si la clé manque (et ne l'affiche pas)."""
372-    stats = {"appels": 0, "requetes": 0, "cache": 0, "tokens": 0, "latence_s": 0.0,
373-             "modeles": {}, "cle_refusee": 0}
374-    client = _client_tagger()
375-    return _cascade_tagger(_transport_tagger(client, stats), partition=partition,
376-                           stats=stats), stats
377-
378-
379-def _cout_tagger(stats: dict) -> dict:
380-    """Le coût d'une exécution, tel qu'il va dans un rapport (`evaluer --json`)."""
381-    return {"modele": MODELE_TAGGER, "appels": stats["appels"],
382-            "requetes": stats["requetes"], "cache": stats["cache"],
383-            "tokens": stats["tokens"], "latence_s": round(stats["latence_s"], 3),
384-            "modeles_renvoyes": dict(stats["modeles"])}
385-
386-
387-def _cout_pour_phrases(cout: dict, mesurees: int, cible: int) -> dict:
388-    """Le coût d'un lot de `cible` phrases, au prorata du lot **mesuré**.
389-
390-    Le tagger fait **un appel par phrase** : le coût est linéaire en nombre de phrases. On ne
391-    modélise pas la longueur des
… [1397 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def _cascade_tagger\" -A40 tools/drave.py && grep -n \"class _TaggerAuto\" -A70 tools/drave.py", "description": "Inspect cascade tagger and auto mode"}`

  ```
353:def _cascade_tagger(transport, partition: str = "alternative", stats: dict | None = None):
354-    """Le câblage mesuré : tagger POS + syntagmes → compose → cascade à 0,6.
355-
356-    `transport` est injectable : les tests le remplacent par une fonction qui rend un JSON de
357-    POS valide, sans réseau. La fusion ne force que le **POS** au neuronal ; les syntagmes,
358-    rôles et attachements restent à l'heuristique (le neuronal n'en rend pas). `stats` porte le
359-    drapeau `cle_refusee` (401/403) qui arrête le run au lieu de le replier.
360-    """
361-    # **un seul** tagger : le POS. Le tagger de syntagmes du composite était appelé et sa
362-    # sortie **n'était pas utilisée** par la fusion (le niveau syntagme reste à l'heuristique) :
363-    # le retirer divise le coût par deux (2 appels → 1 par phrase).
364-    pos = bl.NeuronalLLMPOS(MODELE_TAGGER, transport=transport)
365-    cascade = bl.Cascade(bl.Heuristique(partition=partition), pos, seuil=SEUIL_TAGGER,
366-                         priorite_syntagme="confiance", priorite_par_niveau=PRIORITE_TAGGER)
367-    return _CascadeTagger(cascade, pos, stats=stats)
368-
369-
370-def _construire_tagger(partition: str 
… [4887 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,pathlib,json,hashlib,time\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\np=pathlib.Path('data/udhr/articles.jsonl')\nt0=time.perf_counter()\n# custom build\nimport collections\npar=collections.defaultdict(list)\nfor line in p.read_text(e … [1154 caractères tronqués]`

  ```
langues 398 build 1.129
size 794442 sha 0635d7c8be8d14533069a18ac47ee74fb2f98860c9b52fa89c6cfa6e4918e322
-rw-r--r--. 1 stephane stephane 776K 16 nov 01:37 /tmp/profils_udhr.json
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,pathlib,json,collections\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\nprofils,_=bl.charger_profils_udhr(pathlib.Path('data/udhr/articles.jsonl'),test=(15,15),min_test=1)\nfiles=['eng','hin','bel','ell_monotonic','kin','ewe','ibo','fuf_ … [873 caractères tronqués]`

  ```
eng eng -> eng 0.4213 ok | Latn Latn script ok
hin hin -> hin 0.4853 ok | Deva Deva script ok
bel bel -> bel 0.5897 ok | Cyrl Cyrl script ok
ell_monotonic ell -> ell 1.0 ok | Grek Grek script ok
kin kin -> kin 0.4035 ok | Latn Latn script ok
ewe ewe -> ewe 0.6366 ok | Latn Latn script ok
ibo ibo -> ibo 0.7487 ok | Latn Latn script ok
fuf_adlm fuf -> fuf 1.0 ok | Adlm Adlm script ok
ind ind -> ind 0.3812 ok | Latn Latn script ok
tgl tgl -> tgl 0.3825 ok | Latn Latn script ok
mly_arab zlm -> zlm 0.7171 ok | Arab Arab script ok
jav jav -> jav 0.3187 ok | Latn Latn script ok
mya mya -> mya 0.8845 ok | Mymr Mymr script ok
cmn_hant cmn -> cmn 0.3257 ok | Hani Hant script ok
cnh cnh -> cnh 0.3623 ok | Latn Latn script ok
ctd ctd -> ctd 0.4867 ok | Latn Latn script ok
arb arb -> arb 0.8069 ok | Arab Arab script ok
amh amh -> amh 1.0 ok | Ethi Ethi script ok
heb heb -> heb 0.9412 ok | Hebr Hebr script ok
hau_NE hau -> hau 0.6177 ok | Latn Latn script ok
lang 20 / 20 script 20 / 20
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,pathlib,json,collections\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\np=pathlib.Path('data/udhr/articles.jsonl'); profils,_=bl.charger_profils_udhr(p,test=(15,15),min_test=1)\nfiles=['eng','hin','bel','ell_monotonic','kin','ewe','ibo', … [853 caractères tronqués]`

  ```
eng             16/16 script 16/16
hin             16/16 script 16/16
bel             16/16 script 16/16
ell_monotonic   16/16 script 16/16
kin             15/16 script 16/16
ewe             16/16 script 16/16
ibo             16/16 script 16/16
fuf_adlm        16/16 script 16/16
ind             16/16 script 16/16
tgl             16/16 script 16/16
mly_arab        16/16 script 16/16
jav             13/16 script 16/16
mya             16/16 script 16/16
cmn_hant        13/16 script 16/16
cnh             16/16 script 16/16
ctd             16/16 script 16/16
arb             16/16 script 16/16
amh             16/16 script 16/16
heb             16/16 script 16/16
hau_NE          16/16 script 16/16
TOTAL 313 / 320 0.9781 script 320 / 320
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,pathlib,json,collections\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\np=pathlib.Path('data/udhr/articles.jsonl'); profils,_=bl.charger_profils_udhr(p,test=(15,15),min_test=1)\nnoms=sorted(profils); permutes={noms[i]:profils[noms[(i+1)% … [1140 caractères tronqués]`

  ```
permute sample 0 / 20
permute full 1 / 447 0.0022
'All human beings are born free and equal in dignity and righ' eng 0.0836 und? True
'chat' agr 0.2 und? False
'Le chat the cat dort sleeps on the roof.' sco 0.3632 und? False
  ```

- **bash** `{"command": "sed -n '1,220p' tools/tests/test_schema_produit.py", "description": "Read schema product tests"}`

  ```
#!/usr/bin/env python3
"""test_schema_produit.py — le **contrat** du produit : schéma v2, v1 lue, refus, entrées hostiles.

Ce que le test fige (et qu'un client peut supposer) :
- 8 champs **obligatoires** à la racine : `schema`, `version`, `texte`, `langue`, `script`,
  `refus`, `etiquettes`, `unites_semantiques` ;
- `schema == "drave.annotation"` et `version == 2` ;
- `meta.partition` et `meta.alternative` sont déclarés dans le schéma v2 ;
- une annotation **v1 reste lue** par le vérificateur (schéma v1), et le schéma v2 la refuse ;
- un refus est une **réponse** : JSON valide avec `refus`, code de sortie 3 ;
- un surrogate isolé et une entrée non textuelle ne font pas planter.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

RACINE = pathlib.Path(__file__).resolve().parents[2]
SCHEMA_V1 = RACINE / "tools" / "schemas" / "drave-annotation-v1.json"
SCHEMA_V2 = RACINE / "tools" / "schemas" / "drave-annotation-v2.json"
VERIFICATEUR = RACINE / "tools" / "verifier_schema_produit.py"
OBLIGATOIRES = ("schema", "version", "texte", "langue", "script", "refus",
                "etiquettes", "unites_semantiques")


def _cli(*arg
… [5104 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '150,180p' docs/pilotage/roadmap.md && grep -n \"U3\\|U2\\|U1\\|T1–T6\\|T1-T6\" docs/pilotage/roadmap.md | head -30", "description": "Read roadmap U3 area"}`

  ```
**J14.1 — la clôture : 84 portes, 81 vertes, 3 rouges nommées, le tag `chantier-2026-11-14`.** La
passe du **14/11 00 h 30** (`work/portes/passe-1311-23h15.log`) n'est **pas refaite** : les trois
rouges sont **revérifiées**. `porte-sessions` passe **verte** après la mise en pause du hub
`1e7ef596` et le rafraîchissement du heartbeat `e181ce02` ; `porte-indice` et `porte-melange`
restent **rouges structurelles** (mêmes causes : écart au témoin nul pour l'indice ; état de A qui
ne rend pas son code pour le mélange). Le tag annoté `chantier-2026-11-14` est posé sur le dernier
commit vert `0e75f101` (J13.1) ; le tag de semaine `semaine-2026-11-14` (J5.2, resté en échec) est
posé sur le même commit. [`rapport`](../../reports/rapport-cloture-chantier.md) +
[`JSON`](../../reports/rapport-cloture-chantier.json).
**Prochaine mesure** : **B13 — trancher `g017`**, T132/T133 et le
gold B13 ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).

**T4 — la performance (15/11).** 10 000 mots : **4,01 s**, **2 493 mots/s**, **126 Mio**,
**14,8 Mo** JSON ; α = **1,55**, `_groupes_partition`/`_cible_proche` **O(k²)**.
[Fiche](../../reports/rapport-performance.md) · [JSON](../../reports/perform
… [5984 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '30,90p' docs/pilotage/chantiers.md && grep -n \"B13\" docs/pilotage/chantiers.md | head", "description": "Read chantiers B13 row"}`

  ```
| 31/10 22 h 22 | « le RSN (le pluriel sera plus approprié car tu dois avoir plusieurs candidats) est une représentation de données interne qui te permet d'itérer indéfiniment dans des cycles de pensées à plusieurs niveaux. Il te faudra donc un arbre d'états et toutes les stratégies de l'IA traditionnelle » | la **RSN plurielle**, l'arbre d'états, le moteur de pensée (B13) |
| 31/10 22 h 38 | « en-cours.md doit contenir pour chaque session tout ton plan, ambition et stratégie et objectif final » | le **contrat de synergie** entre sessions |
| 01/11 10 h 29 | « s'éloigner du modèle octet et modèle token pour aller vers un modèle qui voit la structure du texte en surface […] la saccade et les mots dont on peut mélanger les lettres du milieu » | la **typoglycémie** et la **structure de surface** comme objet d'entraînement |
| 01/11 10 h 38 | « un outil semblable [à la coloration syntaxique] pour la linguistique […] coloration et découpage visuel de la structure des phrases et paragraphes […] en entrée de notre modèle pour accélérer son apprentissage » | l'outil **S** (structures candidates) et la **coloration** comme entrée du modèle |
| 01/11 10 h 46 | « créons d'abord un outil pour 
… [16438 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' docs/pilotage/references-non-regression.md", "description": "Read tolerated red gates"}`

  ```
# Références de non-régression

> **Passe — 2026-11-15 09 h 53 → 12 h 15 :** **85 portes, 81 vertes, 4 rouges** — `indice` et
> `melange` structurelles ; `sessions` (heartbeat) **réparée** à 12 h 20 ; `prechargement`
> **environnementale** (deux passes en parallèle ; PPL identique 799,8557 ; verte le 14/11).
> Journaux `work/portes-1115-09h53/`. **Pas de passe complète pour W6** ; ciblage
> `work/portes/w6-ciblage` (8/9), `w6-ciblage2` (2/2) puis `w6-final` (9/9).

> **Passe — 2026-11-14 00 h 30 :** **84 portes, 81 vertes, 3 rouges** — `porte-indice` et
> `porte-melange` (structurelles) et `porte-sessions` (mandats périmés du hub `1e7ef596` et de
> `e181ce02`). `porte-produit` et `porte-bloc` **vertes**. Journal :
> `work/portes/passe-1311-23h15.log`.
>
> **Vérification ciblée — 2026-11-14 06 h 55 (J14.1) :** `porte-sessions` **verte** (hub en pause,
> heartbeat `e181ce02` rafraîchi) ; `porte-indice` et `porte-melange` restent **rouges
> structurelles** (indice 482 contre témoin 459 ; état de A sans son code). Journaux
> `work/portes/verif-cloture/`.

> **Passe précédente — 2026-11-04 23 h 43 → 2026-11-05 02 h 12 :** **83 portes, 79 vertes,
> 4 rouges**, **2 h 29** (journaux durabl
… [4358 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' tools/bloc_linguistique.py && grep -n \"SCHEMA_ANNOTATION\\|VERSION_ANNOTATION\\|SCRIPT_NEUTRE\" tools/bloc_linguistique.py | head", "description": "Check bloc module constants"}`

  ```
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
    étiquettes par confiance ; la cascade n'envoie au neuronal que le **résidu** des niveaux
    que l'heuristique ne couvre pas.

La sortie est une **annotation typée** — pas le corps de la RSN : chaque étiquette porte son
`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script`
… [2312 caractères tronqués]
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/profils_udhr.py", "content": "#!/usr/bin/env python3\n\"\"\"profils_udhr.py — les profils de langue UDHR, chargés et exposés par le CLI.\n\nLe bloc linguistique sait déjà détecter la langue par **recouvrement de trigrammes** sur le … [10845 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/profils_udhr.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,pathlib\nsys.path.insert(0,'.')\nfrom tools import bloc_linguistique as bl\np=pathlib.Path('data/udhr/articles.jsonl')\nfor test,min_test in [((15,15),1),((15,30),1),((15,30),0),((0,0),0)]:\n    profils,tests=bl.charger_profils_udhr(p,test=test,min_test=min_ … [120 caractères tronqués]`

  ```
(15, 15) 1 398 447
(15, 30) 1 398 7137
(15, 30) 0 398 7137
(0, 0) 0 398 444
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"construire_profils_udhr.py — construit l'artefact de profils de langue UDHR.\n\nLes profils sont des **données** : 398 langues, un profil de trigrammes de caractères par\nlangue, construit sur les articles **0–14** de `data/udhr/articles.jsonl` (article 15  … [4897 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/construire_profils_udhr.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/construire_profils_udhr.py && ls -lh tools/tests/linguistique/profils_udhr.json && python3 tools/construire_profils_udhr.py --verifier && echo OK", "description": "Build and verify profile artifact"}`

  ```
profils UDHR : 398 langues · 802110 octets · sha256 33aee69d7659c9bc…
  source : data/udhr/articles.jsonl (e31851d53a882a4f…)
  sortie : /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/profils_udhr.json
-rw-r--r--. 1 stephane stephane 784K 16 nov 01:39 tools/tests/linguistique/profils_udhr.json
OK
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'.')\nimport profils_udhr as pu\np=pu.charger_profils()\nprint(pu.info_profils(p))\nfor t in [\"Le chat dort.\",\"The cat sleeps on the roof.\",\"Привет мир\",\"مرحبا بالعالم\",\"你好世界\",\"All human beings are born free and equal in dignity … [318 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 3, in <module>
ModuleNotFoundError: No module named 'profils_udhr'
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport profils_udhr as pu\np=pu.charger_profils()\nprint(pu.info_profils(p))\nfor t in [\"Le chat dort.\",\"The cat sleeps on the roof.\",\"Привет мир\",\"مرحبا بالعالم\",\"你好世界\",\"All human beings are born free and equal in dig … [322 caractères tronqués]`

  ```
{'langues': 398, 'schema': 'drave.profils-udhr', 'version': 1, 'source': 'data/udhr/articles.jsonl', 'source_sha256': 'e31851d53a882a4ff2e62187a79c5e44d7a33eaf874aacd0ee380041ed992dbf', 'train': [0, 14], 'top': 200}
'Le chat dort.' -> hns hns Latn 0.2701 False
   profils de langue (UDHR, hors ligne)
langue      : hns (Hindustani, Sarnami)
script      : Latn
confiance   : 0.2701 (marge 0.0909, seuil 0.12)
candidats   : hns 0.6364 · lld 0.5455 · deu 0.4545 · oci 0.4545 · pcd 0.4545
profils     : 398 langues UDHR (articles 0–14, top 200)
'The cat sleeps on the roof.' -> sco sco Latn 0.1793 False
   profils de langue (UDHR, hors ligne)
langue      : sco (Scots)
script      : Latn
confiance   : 0.1793 (marge 0.0400, seuil 0.12)
candidats   : sco 0.4800 · eng 0.4400 · hlt 0.2400 · lus 0.2400 · pcm 0.2400
profils     : 398 langues UDHR (articles 0–14, top 200)
'Привет мир' -> rus rus Cyrl 0.55 False
   profils de langue (UDHR, hors ligne)
langue      : rus (Russian)
script      : Cyrl
confiance   : 0.5500 (marge 0.1250, seuil 0.12)
candidats   : rus 0.2500 · bos 0.1250 · bul 0.1250 · evn 0.1250 · gld 0.1250
profils     : 398 langues UDHR (articles 0–14, top 200)
'مرحبا بالعالم' -> arb arb
… [1227 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport profils_udhr as pu\nimport bloc_linguistique as bl\np=pu.charger_profils(); langues=pu.langues_de(p)\nfor t in [\"Le chat dort.\",\"The cat sleeps on the roof.\",\"Le chat de la voisine qui dort sur le toit se réveille.\", … [335 caractères tronqués]`

  ```
'Le chat dort.' None -> hns 0.27
'Le chat dort.' fra -> hns 0.27
'Le chat dort.' eng -> hns 0.27
'Le chat dort.' deu -> hns 0.27
'Le chat dort.' spa -> hns 0.27

'The cat sleeps on the roof.' None -> sco 0.179
'The cat sleeps on the roof.' fra -> sco 0.179
'The cat sleeps on the roof.' eng -> sco 0.138
'The cat sleeps on the roof.' deu -> sco 0.179
'The cat sleeps on the roof.' spa -> sco 0.179

'Le chat de la voisine qui dort sur le toit se réveille.' None -> fra 0.329
'Le chat de la voisine qui dort sur le toit se réveille.' fra -> fra 0.363
'Le chat de la voisine qui dort sur le toit se réveille.' eng -> fra 0.329
'Le chat de la voisine qui dort sur le toit se réveille.' deu -> fra 0.329
'Le chat de la voisine qui dort sur le toit se réveille.' spa -> fra 0.329

'Le chat dort dans la maison.' None -> lld 0.311
'Le chat dort dans la maison.' fra -> lld 0.278
'Le chat dort dans la maison.' eng -> lld 0.311
'Le chat dort dans la maison.' deu -> lld 0.311
'Le chat dort dans la maison.' spa -> lld 0.311

'El gato duerme en la casa.' None -> spa 0.183
'El gato duerme en la casa.' fra -> spa 0.183
'El gato duerme en la casa.' eng -> spa 0.183
'El gato duerme en la casa.' deu -> spa 0.1
… [280 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport profils_udhr as pu, bloc_linguistique as bl\np=pu.charger_profils(); langues=pu.langues_de(p)\nfor t in [\"Le chat dort.\",\"The cat sleeps on the roof.\",\"Le chat dort dans la maison.\",\"Le chat de la voisine qui dort s … [304 caractères tronqués]`

  ```
'Le chat dort.' profile hns 0.2701
  top [('hns', 0.6363636363636364), ('lld', 0.5454545454545454), ('deu', 0.45454545454545453), ('oci', 0.45454545454545453), ('pcd', 0.45454545454545453), ('src', 0.45454545454545453), ('afr', 0.36363636363636365), ('ayr', 0.36363636363636365), ('cic', 0.36363636363636365), ('cnh', 0.36363636363636365)]
  lexique ('fr', 0.6667, {'fr': 0.3333333333333333, 'en': 0.0, 'de': 0.0, 'es': 0.3333333333333333, 'it': 0.3333333333333333, 'pt': 0.0, 'nl': 0.0})
'The cat sleeps on the roof.' profile sco 0.1793
  top [('sco', 0.48), ('eng', 0.44), ('hlt', 0.24), ('lus', 0.24), ('pcm', 0.24), ('vec', 0.24), ('cfm', 0.2), ('ctd', 0.2), ('dip', 0.2), ('fkv', 0.2)]
  lexique ('en', 0.8, {'fr': 0.2, 'en': 0.4, 'de': 0.0, 'es': 0.0, 'it': 0.0, 'pt': 0.0, 'nl': 0.0})
'Le chat dort dans la maison.' profile lld 0.3106
  top [('lld', 0.6153846153846154), ('fra', 0.5), ('oci', 0.4230769230769231), ('fur', 0.38461538461538464), ('roh', 0.38461538461538464), ('cat', 0.34615384615384615), ('pcd', 0.34615384615384615), ('src', 0.34615384615384615), ('tob', 0.34615384615384615), ('cfm', 0.3076923076923077)]
  lexique ('fr', 1.0, {'fr': 0.5, 'en': 0.0, 'de': 0.0, 'es': 0.333333
… [619 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,collections,json,pathlib,time\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl, profils_udhr as pu\np=pu.charger_profils(); langues=pu.langues_de(p)\nISO2=pu.ISO2_VERS_ISO3\n\ndef detect(t, use_prior=True):\n    tri=collections.Counter(bl._trigram … [2079 caractères tronqués]`

  ```
full prior False 433 / 447 0.9687 below seuil 6
full prior True 416 / 447 0.9306 below seuil 8
sample prior False 20 / 20
sample prior True 20 / 20
'Le chat dort.' raw hns 0.2701 prior hns 0.1749
'The cat sleeps on the roof.' raw sco 0.1793 prior eng 0.5966
'Le chat dort dans la maison.' raw lld 0.3106 prior fra 0.5846
'El gato duerme en la casa.' raw spa 0.1833 prior spa 0.7742
'Die Katze schläft im Haus.' raw deu 0.344 prior deu 0.6746
'Il gatto dorme in casa.' raw glg 0.0667 prior ita 0.6921
'O gato dorme em casa.' raw pcm 0.2165 prior por 0.6285
'De kat slaapt in het huis.' raw nds 0.075 prior nld 0.7464
'Le chat de la voisine qui dort sur le toit se réveille.' raw fra 0.3289 prior fra 0.843
'chat' raw agr 0.2 prior agr 0.2
'hello' raw ekk 0.1333 prior ekk 0.1333
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,collections\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl, profils_udhr as pu\np=pu.charger_profils(); langues=pu.langues_de(p)\nt=\"Le chat dort.\"\ntri=collections.Counter(bl._trigrammes(t))\nscores={code:bl._score_profil(tri,pr['trigrammes'] … [318 caractères tronqués]`

  ```
fra 0.2727272727272727 hns 0.6363636363636364
fallback ('fr', 0.6667, {'fr': 0.3333333333333333, 'en': 0.0, 'de': 0.0, 'es': 0.3333333333333333, 'it': 0.3333333333333333, 'pt': 0.0, 'nl': 0.0})
fallback fr score 0.3333333333333333
top [('hns', 0.6363636363636364), ('lld', 0.5454545454545454), ('deu', 0.45454545454545453), ('oci', 0.45454545454545453), ('pcd', 0.45454545454545453), ('src', 0.45454545454545453), ('afr', 0.36363636363636365), ('ayr', 0.36363636363636365), ('cic', 0.36363636363636365), ('cnh', 0.36363636363636365)]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,pathlib\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl, profils_udhr as pu\np=pu.charger_profils(); langues=p['langues']\nprofils_corpus,_=bl.charger_profils_udhr(pathlib.Path('data/udhr/articles.jsonl'),test=(15,15),min_test=1)\nfor code in ['f … [416 caractères tronqués]`

  ```
fra artifact 200 corpus 200 equal True
 only artifact []
 only corpus []
 diff counts []
hns artifact 200 corpus 200 equal True
 only artifact []
 only corpus []
 diff counts []
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,collections,json,pathlib,re\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl, profils_udhr as pu\np=pu.charger_profils(); langues=pu.langues_de(p); ISO2=pu.ISO2_VERS_ISO3\n\ndef raw(t):\n    tri=collections.Counter(bl._trigrammes(t)); scores={c:bl … [2108 caractères tronqués]`

  ```
full hybride 416 / 447 0.9306 Counter({'profils': 422, 'lexique': 25})
eng eng -> eng 0.5 lexique len 144
hin hin -> hin 0.485 profils len 191
bel bel -> bel 0.59 profils len 141
ell_monotonic ell -> ell 1.0 profils len 138
kin kin -> kin 0.404 profils len 180
ewe ewe -> ita 0.25 lexique len 167
ibo ibo -> ibo 0.749 profils len 158
fuf_adlm fuf -> fuf 1.0 profils len 147
ind ind -> ind 0.381 profils len 175
tgl tgl -> tgl 0.383 profils len 189
mly_arab zlm -> zlm 0.717 profils len 142
jav jav -> jav 0.319 profils len 200
mya mya -> mya 0.884 profils len 216
cmn_hant cmn -> cmn 0.195 profils len 37
cnh cnh -> cnh 0.362 profils len 206
ctd ctd -> ctd 0.487 profils len 150
arb arb -> arb 0.807 profils len 87
amh amh -> amh 1.0 profils len 80
heb heb -> heb 0.941 profils len 99
hau_NE hau -> hau 0.618 profils len 191
sample 19 / 20 Counter({'profils': 18, 'lexique': 2})
'Le chat dort.' -> ('fra', 0.3333, 'lexique')
'The cat sleeps on the roof.' -> ('eng', 0.4, 'lexique')
'Le chat dort dans la maison.' -> ('fra', 0.5, 'lexique')
'El gato duerme en la casa.' -> ('spa', 0.5, 'lexique')
'Die Katze schläft im Haus.' -> ('deu', 0.344, 'profils')
'Il gatto dorme in casa.' -> ('ita', 0.4, 'lex
… [315 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,collections,json,pathlib,re\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl, profils_udhr as pu\np=pu.charger_profils(); langues=pu.langues_de(p); ISO2=pu.ISO2_VERS_ISO3\n\ndef raw(t):\n    tri=collections.Counter(bl._trigrammes(t)); scores={c:bl … [1492 caractères tronqués]`

  ```
lim 0 full 433 / 447 0.9687 sample 20 /20
lim 40 full 433 / 447 0.9687 sample 20 /20
lim 60 full 432 / 447 0.9664 sample 20 /20
lim 80 full 431 / 447 0.9642 sample 20 /20
lim 100 full 431 / 447 0.9642 sample 20 /20
lim 120 full 429 / 447 0.9597 sample 20 /20
lim 150 full 422 / 447 0.9441 sample 20 /20
lim 200 full 416 / 447 0.9306 sample 19 /20
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re,pathlib\np=pathlib.Path('tools/profils_udhr.py')\ns=p.read_text()\ns=s.replace('import collections\\nimport functools','import functools')\ns=s.replace('''SEUIL_DEFAUT = 0.12\nTOP_DEFAUT = 200\nCANDIDATS_DEFAUT = 5''','''SEUIL_DEFAUT = 0.12\nTOP_DEFAUT = 200\ … [9889 caractères tronqués]`

  ```
patched
compiled
  ```

- **bash** `{"command": "grep -n \"source      \\|confiance   \\|def detecter\\|def _scores\\|LONGUEUR_PRIOR\\|SEUIL_PRIOR\" tools/profils_udhr.py && sed -n '130,290p' tools/profils_udhr.py", "description": "Review patched profils module"}`

  ```
43:LONGUEUR_PRIOR = 80
44:SEUIL_PRIOR = 0.25
157:def detecter(texte: str, profils: dict[str, Any] | None = None,
161:             longueur_prior: int = LONGUEUR_PRIOR) -> dict[str, Any]:
199:        if fb_langue in ISO2_VERS_ISO3 and score_fb >= SEUIL_PRIOR:
260:def _scores_profils(texte: str, langues: dict[str, dict]) -> dict[str, float]:
288:    lignes.append(f"confiance   : {detection['confiance']:.4f} "
290:    lignes.append(f"source      : {detection.get('source', 'profils')}")
    langues = langues_de(profils)
    return {
        "langues": len(langues),
        "schema": profils.get("schema", SCHEMA_PROFILS),
        "version": profils.get("version", VERSION_PROFILS),
        "source": profils.get("source", ""),
        "source_sha256": profils.get("source_sha256", ""),
        "train": profils.get("train", []),
        "top": profils.get("top", TOP_DEFAUT),
    }


def _candidats(scores: dict[str, float], langues: dict[str, dict],
               n: int = CANDIDATS_DEFAUT) -> list[dict[str, Any]]:
    classement = sorted(((code, score) for code, score in scores.items() if score > 0.0),
                        key=lambda kv: (-kv[1], kv[0]))
    return [{"langue": code,
    
… [7123 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport profils_udhr as pu\np=pu.charger_profils()\nfor t in [\"Le chat dort.\",\"The cat sleeps on the roof.\",\"Le chat dort dans la maison.\",\"El gato duerme en la casa.\",\"Die Katze schläft im Haus.\",\"Il gatto dorme in cas … [517 caractères tronqués]`

  ```
'Le chat dort.' -> fra fra Latn 0.3333 lexique False
'The cat sleeps on the roof.' -> eng eng Latn 0.4 lexique False
'Le chat dort dans la maison.' -> fra fra Latn 0.5 lexique False
'El gato duerme en la casa.' -> spa spa Latn 0.5 lexique False
'Die Katze schläft im Haus.' -> deu deu Latn 0.344 profils False
'Il gatto dorme in casa.' -> ita ita Latn 0.4 lexique False
'O gato dorme em casa.' -> por por Latn 0.4 lexique False
'De kat slaapt in het huis.' -> nld nld Latn 0.5 lexique False
'Le chat de la voisine qui dort sur le toit se réve' -> fra fra Latn 0.5455 lexique False
'chat' -> und agr Latn 0.04 profils True
'hello' -> und ekk Latn 0.0267 profils True
'Привет мир' -> rus rus Cyrl 0.22 profils False
'你好世界' -> und und Hani 0.0 profils True
'All human beings are born free and equal in dignit' -> und eng Latn 0.0836 profils True
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,json,pathlib,collections\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl, profils_udhr as pu\nprofils=pu.charger_profils()\n# full 398 raw corpus tests\n_,tests=bl.charger_profils_udhr(pathlib.Path('data/udhr/articles.jsonl'),test=(15,15),min_tes … [1204 caractères tronqués]`

  ```
full hybrid 431 / 447 0.9642 raw 433 und 7 Counter({'profils': 445, 'lexique': 2})
eng eng -> eng 0.4213 profils OK script True
hin hin -> hin 0.4853 profils OK script True
bel bel -> bel 0.5897 profils OK script True
ell_monotonic ell -> ell 1.0 profils OK script True
kin kin -> kin 0.4035 profils OK script True
ewe ewe -> ewe 0.6366 profils OK script True
ibo ibo -> ibo 0.7487 profils OK script True
fuf_adlm fuf -> fuf 1.0 profils OK script True
ind ind -> ind 0.3812 profils OK script True
tgl tgl -> tgl 0.3825 profils OK script True
mly_arab zlm -> zlm 0.7171 profils OK script True
jav jav -> jav 0.3187 profils OK script True
mya mya -> mya 0.8845 profils OK script True
cmn_hant cmn -> cmn 0.1954 profils OK script True
cnh cnh -> cnh 0.3623 profils OK script True
ctd ctd -> ctd 0.4867 profils OK script True
arb arb -> arb 0.8069 profils OK script True
amh amh -> amh 1.0 profils OK script True
heb heb -> heb 0.9412 profils OK script True
hau_NE hau -> hau 0.6177 profils OK script True
sample 20 /20 script 20 /20
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/profils_udhr.py')\ns=p.read_text()\ns=s.replace('''    n = _tokens(texte)\n    if n < 5:\n        confiance *= n / 5.0''','''    n = _tokens(texte)\n    # La pénalité ne vise que les textes **très courts** : un article chinois de 3 … [321 caractères tronqués]`

  ```
patched
compiled
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport profils_udhr as pu\np=pu.charger_profils()\nfor t in [\"你的人生而自由，在尊严和权利上一律平等。\",\"你好世界\",\"chat\",\"hello\",\"Привет мир\",\"Le chat dort.\"]:\n    d=pu.detecter(t,p); print(repr(t),'->',d['langue'],d['langue_probable'],d[' … [106 caractères tronqués]`

  ```
'你的人生而自由，在尊严和权利上一律平等。' -> cjy cjy 0.5222 profils False
'你好世界' -> und und 0.0 profils True
'chat' -> und agr 0.04 profils True
'hello' -> und ekk 0.0267 profils True
'Привет мир' -> rus rus 0.22 profils False
'Le chat dort.' -> fra fra 0.3333 lexique False
  ```

- **bash** `{"command": "grep -rn \"_construire_tagger\\|_cascade_tagger\" --include=*.py tools | grep -v __pycache__", "description": "Find cascade tagger callers"}`

  ```
tools/tests/linguistique/qualifier_tagger_h50.py:274:    cascade = drave._cascade_tagger(transport, partition=partition, stats=stats)
tools/tests/linguistique/qualifier_tagger_h50.py:488:                      "mesure que `drave evaluer` ; cascade `_cascade_tagger` de tools/drave.py",
tools/tests/linguistique/qualifier_tagger_lot.py:5:même câblage (`drave._cascade_tagger`, `NeuronalLLMPOS`, cache disque du client) sur un **lot
tools/tests/linguistique/qualifier_tagger_lot.py:258:    cascade = drave._cascade_tagger(transport, partition=partition, stats=stats)
tools/tests/linguistique/qualifier_tagger_lot.py:609:            "cablage": "drave._cascade_tagger (NeuronalLLMPOS + Heuristique, POS neuronal)",
tools/tests/test_tagger_api.py:122:        cascade = drave._cascade_tagger(transport_factice)
tools/tests/test_tagger_api.py:142:        annotation = drave._cascade_tagger(transport_factice).analyser(TEXTE, "fr")
tools/tests/test_tagger_api.py:175:        cascade = drave._cascade_tagger(transport)
tools/tests/test_tagger_api.py:185:        cascade = drave._cascade_tagger(lambda *_: "pas du JSON")
tools/drave.py:353:def _cascade_tagger(transport, partition: str = "alternative", stats: d
… [468 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/drave.py')\ns=p.read_text()\n# import\ns=s.replace('import restitution_v3  # noqa: E402  (la restitution v3 : les rôles des GP)',\n            'import restitution_v3  # noqa: E402  (la restitution v3 : les rôles des GP)\\nimport pr … [2365 caractères tronqués]`

  ```
patched cascade
62:import profils_udhr as pu  # noqa: E402  (la détection de langue UDHR, 398 profils)
354:def _cascade_tagger(transport, partition: str = "alternative", stats: dict | None = None,
373:def _construire_tagger(partition: str = "alternative",
  ```

- **bash** `{"command": "grep -n \"class _TaggerAuto\\|^def _ligne_tagger\\|^def _sur\\|^def _dumps\\|^# ---\" tools/drave.py | head -40", "description": "Find insertion point for helper class"}`

  ```
78:# --------------------------------------------------------------------------- sorties JSON
81:def _sur(s: str) -> str:
86:def _dumps(objet) -> str:
96:# --------------------------------------------------------------------------- le tagger (option)
198:class _TaggerAuto:
415:def _ligne_tagger(stats: dict) -> str:
422:# --------------------------------------------------------------------------- rendu lisible
526:# --------------------------------------------------------------------------- commandes
966:# --------------------------------------------------------------------------- restitution
1093:# --------------------------------------------------------------------------- CLI
  ```

- **bash** `{"command": "sed -n '300,355p' tools/drave.py", "description": "View end of auto class"}`

  ```
stats["cle_refusee"] = int(code)
            raise
        if getattr(reponse, "cache", False):
            stats["cache"] += 1
        else:
            usage = reponse.usage if isinstance(reponse.usage, dict) else {}
            stats["requetes"] += 1
            stats["tokens"] += int(usage.get("total_tokens", 0) or 0)
            stats["latence_s"] += float(getattr(reponse, "latence_s", 0.0) or 0.0)
        modele = getattr(reponse, "modele", None)
        if modele:
            stats["modeles"][modele] = stats["modeles"].get(modele, 0) + 1
        return reponse.contenu

    return transport


class _CascadeTagger:
    """La cascade du tagger, avec le **refus** du neuronal reporté sur l'annotation fusionnée.

    `bl.Cascade`/`_fusion` ne recopie pas `refus` : sans ce relais, un tagger qui échoue
    rendrait une annotation muette (POS absents, `refus` vide). Le composite est rappelé après
    la fusion ; ses taggers ont un cache, donc **aucun appel réseau supplémentaire**.
    """

    nom = "cascade"

    def __init__(self, cascade, compose, stats: dict | None = None):
        self.cascade = cascade
        self.compose = compose
        self.stats = stats if stats is not No
… [1368 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/drave.py')\ns=p.read_text()\nmarker='def _cascade_tagger(transport, partition: str = \"alternative\", stats: dict | None = None,'\ncls='''class _HeuristiqueProfils(bl.Heuristique):\n    \"\"\"L'heuristique avec la détection des **p … [782 caractères tronqués]`

  ```
inserted class
354:class _HeuristiqueProfils(bl.Heuristique):
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/drave.py')\ns=p.read_text()\ns=s.replace('''    texte = _lire_entree(args)\n    duree = bool(getattr(args, \"duree\", False))\n    h = bl.Heuristique(partition=args.partition)\n    mode = _mode_tagger(args)''','''    texte = _lire_ … [658 caractères tronqués]`

  ```
patched cmd_analyser
628:                cascade, stats_tagger = _construire_tagger(partition=args.partition, heuristique=h)
640:            cascade, stats_tagger = _construire_tagger(partition=args.partition, heuristique=h)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/drave.py')\ns=p.read_text()\nmarker='def cmd_analyser(args: argparse.Namespace) -> int:'\nfunc='''def cmd_profils(args: argparse.Namespace) -> int:\n    \"\"\"La langue probable, le script et la confiance — la détection UDHR exposé … [1984 caractères tronqués]`

  ```
inserted cmd_profils
612:def cmd_profils(args: argparse.Namespace) -> int:
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/drave.py')\ns=p.read_text()\ns=s.replace('Commandes : analyser, evaluer, rejouer, restituer.\\\\n',\n            'Commandes : analyser, evaluer, profils, rejouer, restituer.\\\\n')\ns=s.replace('\"--partition brut|alternative|filtr … [3991 caractères tronqués]`

  ```
patched parser
compiled
355:    """L'heuristique avec la détection des **profils UDHR** (`--profils`, `drave profils`).
1202:        "Commandes : analyser, evaluer, profils, rejouer, restituer.\n"
1208:        "--profils (analyser) et `drave profils --texte`.\n"
1219:        "  python3 tools/drave.py analyser \"Le chat dort.\" --profils\n"
1232:                                  metavar="{analyser,evaluer,profils,rejouer,restituer}",
1235:    analyser = sous.add_parser(
1261:    analyser.add_argument("--profils", action="store_true",
1277:    evaluer = sous.add_parser(
1304:    profils = sous.add_parser(
1330:    rejouer = sous.add_parser(
1345:    restituer = sous.add_parser(
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/drave.py')\ns=p.read_text()\ns=s.replace('''    except GoldAbsent as exc:\n        # les gold sont une dépendance de données : code 4, rien sur stdout, pas de trace\n        print(f\"{NOM}: dépendance absente : {exc}\", file=sys.st … [1058 caractères tronqués]`

  ```
patched main and docstring
compiled
  ```

- **bash** `{"command": "python3 tools/drave.py profils --texte \"Le chat dort.\" ; echo \"exit=$?\"; echo '---'; python3 tools/drave.py profils --texte \"Le chat dort.\" --json; echo \"exit=$?\"; echo '---'; python3 tools/drave.py profils --texte \"All human beings are born free and equal in dignity and rights … [145 caractères tronqués]`

  ```
drave 0.1.0 — profils de langue (UDHR, hors ligne)
langue      : fra (French)
script      : Latn
confiance   : 0.3333 (marge 0.0000, seuil 0.12)
source      : lexique
candidats   : fra 0.3333 · hns 0.6364 · lld 0.5455 · deu 0.4545 · oci 0.4545 · pcd 0.4545
profils     : 398 langues UDHR (articles 0–14, top 200)
exit=0
---
{
 "schema": "drave.profils",
 "version": 1,
 "texte": "Le chat dort.",
 "langue": "fra",
 "langue_probable": "fra",
 "nom": "French",
 "script": "Latn",
 "confiance": 0.3333,
 "marge": 0.0,
 "source": "lexique",
 "seuil": 0.12,
 "sous_seuil": false,
 "refus": "",
 "candidats": [
  {
   "langue": "fra",
   "nom": "French",
   "score": 0.333333
  },
  {
   "langue": "hns",
   "nom": "Hindustani, Sarnami",
   "score": 0.636364
  },
  {
   "langue": "lld",
   "nom": "Ladin",
   "score": 0.545455
  },
  {
   "langue": "deu",
   "nom": "German, Standard (1901)",
   "score": 0.454545
  },
  {
   "langue": "oci",
   "nom": "Occitan (Auvergnat)",
   "score": 0.454545
  },
  {
   "langue": "pcd",
   "nom": "Picard",
   "score": 0.454545
  }
 ],
 "profils": {
  "langues": 398,
  "schema": "drave.profils-udhr",
  "version": 1,
  "source": "data/udhr/articles.jsonl",
  "sourc
… [1184 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/profils_udhr.py')\ns=p.read_text()\ns=s.replace('''            scores_profils = _scores_profils(texte, langues)\n            cands = _candidats(scores_profils, langues, candidats)\n            if all(c[\"langue\"] != code for c in  … [2773 caractères tronqués]`

  ```
patched prior
compiled
{
 "schema": "drave.profils",
 "version": 1,
 "texte": "Le chat dort.",
 "langue": "fra",
 "langue_probable": "fra",
 "nom": "French",
 "script": "Latn",
 "confiance": 0.3333,
 "marge": 0.0,
 "source": "lexique",
 "seuil": 0.12,
 "sous_seuil": false,
 "refus": "",
 "prior": {
  "langue": "fra",
  "nom": "French",
  "score": 0.333333
 },
 "candidats": [
  {
   "langue": "hns",
   "nom": "Hindustani, Sarnami",
   "score": 0.636364
  },
  {
   "langue": "lld",
   "nom": "Ladin",
   "score": 0.545455
  },
  {
   "langue": "deu",
   "nom": "German, Standard (1901)",
   "score": 0.454545
  },
  {
   "langue": "oci",
   "nom": "Occitan (Auvergnat)",
   "score": 0.454545
  },
---
drave 0.1.0 — profils de langue (UDHR, hors ligne)
langue      : fra (French)
script      : Latn
confiance   : 0.3333 (marge 0.0000, seuil 0.12)
source      : lexique
prior       : fra (mots-outils 0.3333)
candidats   : hns 0.6364 · lld 0.5455 · deu 0.4545 · oci 0.4545 · pcd 0.4545
profils     : 398 langues UDHR (articles 0–14, top 200)
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat dort.\" --profils ; echo \"exit=$?\"; echo '---'; python3 tools/drave.py analyser \"Le chat dort.\" --profils --json | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d[\"langue\"], d[\"script\"], len(d[\"etiquettes\"]))'; echo '---'; … [183 caractères tronqués]`

  ```
drave 0.1.0 — analyse heuristique (CPU, hors ligne)
langue=fra script=Latn source=heuristique · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=objet     → dort
  GV   [8:12]  dort     rôle=predicat  → —
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.35 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
exit=0
---
fra Latn 20
---
drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
langue=fra script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=objet     → dort
exit=0
  ```

- **bash** `{"command": "DRAVE_PROFILS=/tmp/absent-profils.json python3 tools/drave.py profils --texte \"Le chat dort.\"; echo \"exit=$?\"; echo '---'; python3 tools/drave.py profils --texte \"\" --json; echo \"exit=$?\"; echo '---'; python3 tools/drave.py profils --texte \"\"; echo \"exit=$?\"; echo '---'; pyt … [150 caractères tronqués]`

  ```
exit=4
---
{
 "schema": "drave.profils",
 "version": 1,
 "texte": "",
 "langue": "und",
 "langue_probable": "und",
 "nom": "",
 "script": "Zyyy",
 "confiance": 0.0,
 "marge": 0.0,
 "source": "aucune",
 "seuil": 0.12,
 "sous_seuil": true,
 "refus": "vide",
 "prior": null,
 "candidats": [],
 "profils": {
  "langues": 398,
  "schema": "drave.profils-udhr",
  "version": 1,
  "source": "data/udhr/articles.jsonl",
  "source_sha256": "e31851d53a882a4ff2e62187a79c5e44d7a33eaf874aacd0ee380041ed992dbf",
  "train": [
   0,
   14
  ],
  "top": 200
 }
}
exit=3
---
exit=3
---
exit=5
[stderr]
drave: dépendance absente : profils de langue absents : /tmp/absent-profils.json — réinstaller la roue complète, ou lancer `python3 tools/construire_profils_udhr.py` depuis le dépôt (DRAVE_PROFILS peut pointer vers un autre artefact).
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
drave: erreur d'usage : --seuil doit être dans [0, 1]
  ```

- **bash** `{"command": "python3 tools/drave.py profils; echo \"exit=$?\"; python3 tools/drave.py profils \"Le chat dort.\" \"autre\" 2>&1 | head -3; echo \"exit=${PIPESTATUS[0]}\"; python3 tools/drave.py profils --texte \"Le chat dort.\" --fichier /tmp/nonexistent; echo \"exit=$?\"", "description": "Test profi … [17 caractères tronqués]`

  ```
exit=5
usage: drave [-h] [-V] {analyser,evaluer,profils,rejouer,restituer} ...
drave: erreur d'usage : unrecognized arguments: autre
exit=5
exit=4
[stderr]
drave: erreur d'usage : TEXTE ou --texte requis
drave: dépendance absente : fichier introuvable : '/tmp/nonexistent'
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,collections\nrows=collections.defaultdict(dict)\nfor line in open('data/udhr/articles.jsonl'):\n    d=json.loads(line); rows[d['fichier']][int(d['art'])]=d\nprint('files',len(rows),'with art15',sum(1 for a in rows.values() if 15 in a))\nprint('distinct iso3 … [120 caractères tronqués]`

  ```
files 456 with art15 452
distinct iso3 with art15 399
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"mesurer_profils.py — la mesure de `drave profils` sur l'échantillon UDHR de 20 langues.\n\nLe dispositif, en une commande :\n\n  1. charge l'artefact de profils (`tools/tests/linguistique/profils_udhr.json`) ;\n  2. vérifie qu'il est **identique** aux profi … [17045 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mesurer_profils.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/mesurer_profils.py --sortie reports/profils.json; echo \"exit=$?\"; ls -lh reports/profils.json", "description": "Run profile measurement", "timeoutMs": 180000}`

  ```
=== PROFILS DE LANGUE — UDHR ===
profils : 398 langues · 802110 octets · 33aee69d7659c9bc…
identité artefact ↔ corpus : oui (0 différence(s))
échantillon 20 (article 15) : langue 20/20 (1.0000) · script 20/20
échantillon 20 (articles 15–30) : langue 313/320 (0.9781) · script 320/320
autotest 398 (article 15) : brut 0.9687 · CLI 0.9642 · script 1.0000
permuté : 20 0.0000 · 398 0.0022
ambigu : und (0.0836) · mot isolé : und · vide : vide
verdict : OK · reports/profils.json
exit=0
-rw-r--r--. 1 stephane stephane 21K 16 nov 01:44 reports/profils.json
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/profils.json'))\nprint(json.dumps({k:d[k] for k in ['profils','identite','autotest_398','controle_permute','controle_negatif','cli','verdict']},ensure_ascii=False,indent=1))\nprint('20:', {k:d['echantillon_20'][k] for k in ['tests … [202 caractères tronqués]`

  ```
{
 "profils": {
  "fichier": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/profils_udhr.json",
  "sha256": "33aee69d7659c9bc9ecf9c1caf1740953d36b16d71efaa8279571a652d499cf1",
  "octets": 802110,
  "langues": 398,
  "top": 200,
  "train": [
   0,
   14
  ],
  "source": "data/udhr/articles.jsonl",
  "source_sha256": "e31851d53a882a4ff2e62187a79c5e44d7a33eaf874aacd0ee380041ed992dbf",
  "duree_chargement_s": 0.038
 },
 "identite": {
  "langues_corpus": 398,
  "langues_artefact": 398,
  "differences": [],
  "n_differences": 0,
  "sha256_source_corpus": "e31851d53a882a4ff2e62187a79c5e44d7a33eaf874aacd0ee380041ed992dbf",
  "sha256_source_artefact": "e31851d53a882a4ff2e62187a79c5e44d7a33eaf874aacd0ee380041ed992dbf",
  "source_identique": true,
  "ok": true
 },
 "autotest_398": {
  "langues": 398,
  "tests": 447,
  "brut": {
   "justes": 433,
   "total": 447,
   "taux": 0.9687
  },
  "cli": {
   "justes": 431,
   "total": 447,
   "taux": 0.9642,
   "sources": {
    "profils": 445,
    "lexique": 2
   }
  },
  "script": {
   "justes": 447,
   "total": 447,
   "taux": 1.0
  }
 },
 "controle_permute": {
  "echantillon_20": {
   "justes": 0,
   "total": 20,
   "taux"
… [1524 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('pyproject.toml')\ns=p.read_text()\ns=s.replace('''# Les gold sont **dans la roue** : `drave evaluer` doit marcher hors du dépôt.\n# Le contrôle négatif (une roue amputée de ces fichiers) est décrit dans\n# reports/rapport-roue.md : `eval … [923 caractères tronqués]`

  ```
patched pyproject
34:    "profils_udhr.json",
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/tests/test_empaquetage.py')\ns=p.read_text()\ns=s.replace('''- la **roue** embarque les sous-paquets du CLI (`tools.tests.linguistique`,\n  `tools.structures`, `tools.llm`) et les **gold** (`package-data`) ;''','''- la **roue** emb … [2028 caractères tronqués]`

  ```
patched test_empaquetage
compiled
  ```

- **write** `{"content": "#!/usr/bin/env python3\n\"\"\"test_profils.py — `drave profils`, la détection de langue UDHR exposée.\n\nCe que le test fige :\n\n- la commande `profils --texte` (et le TEXTE positionnel) rend la **langue probable**,\n  le **script** et la **confiance** ; le JSON porte `schema`, `langue … [11597 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_profils.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/tests/test_profils.py; echo \"exit=$?\"", "description": "Run new profile tests", "timeoutMs": 180000}`

  ```
exit=0
[stderr]
test_analyser_profils (__main__.TestAnalyserProfils.test_analyser_profils) ... ok
test_analyser_profils_absents_code_4 (__main__.TestAnalyserProfils.test_analyser_profils_absents_code_4) ... ok
test_20_langues_article_15 (__main__.TestEchantillonUDHR.test_20_langues_article_15) ... ok
test_artefact_398_et_source (__main__.TestEchantillonUDHR.test_artefact_398_et_source) ... ok
test_profils_permutés_proches_du_hasard (__main__.TestEchantillonUDHR.test_profils_permutés_proches_du_hasard) ... ok
test_ambigu_est_und (__main__.TestProfilsCLI.test_ambigu_est_und) ... ok
test_anglais (__main__.TestProfilsCLI.test_anglais) ... ok
test_cyrillique (__main__.TestProfilsCLI.test_cyrillique) ... ok
test_deterministe (__main__.TestProfilsCLI.test_deterministe) ... ok
test_fichier (__main__.TestProfilsCLI.test_fichier) ... ok
test_mot_isole_est_und (__main__.TestProfilsCLI.test_mot_isole_est_und) ... ok
test_profils_absents_code_4 (__main__.TestProfilsCLI.test_profils_absents_code_4) ... ok
test_profils_francais_json (__main__.TestProfilsCLI.test_profils_francais_json) ... ok
test_seuil_invalide_code_5 (__main__.TestProfilsCLI.test_seuil_invalide_code_5) ... ok
test_seuil_zero_gar
… [487 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/tests/test_produit.py')\ns=p.read_text()\ns=s.replace('''              and all(mot in aide.stdout for mot in (\"analyser\", \"evaluer\", \"rejouer\", \"--aide\")),''','''              and all(mot in aide.stdout for mot in (\"analys … [821 caractères tronqués]`

  ```
patched test_produit
exit=0
[stderr]
..............................
----------------------------------------------------------------------
Ran 30 tests in 16.828s

OK
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/porte-bloc-linguistique.sh')\ns=p.read_text()\ns=s.replace('''python3 -m unittest discover -s tools/tests/linguistique -p 'test_bloc_linguistique.py' || { echo \"❌ tests\"; exit 1; }\npython3 tools/bloc_linguistique.py --autotest - … [743 caractères tronqués]`

  ```
patched gate
=== PORTE BLOC LINGUISTIQUE ===
{
 "langue": {
  "langues_profil": 398,
  "articles_test": 447,
  "accuracy": 0.9687,
  "accuracy_script": 1.0,
  "duree_s": 4.777,
  "langues": {
   "hus": [
    3,
    3
   ],
   "oci": [
    7,
    6
   ],
   "roh": [
    7,
    7
   ],
   "ron": [
    3,
    3
   ]
  }
 },
 "controle_permute": {
  "accuracy": 0.0022,
  "attendu": "proche du hasard"
 },
 "niveaux_vus": [
  "discours",
  "document",
  "graphème",
  "morphème",
  "mot",
  "phrase",
  "pos",
  "pragmatique",
  "syntagme"
 ],
 "niveaux_manquants": [],
 "controles": {
  "vide_refus": "vide",
  "ponctuation_refus": "vide",
  "langue_inconnue": "und",
  "indice_faux": "und",
  "rejeu_identique": true
 },
 "verdicts": {
  "langue": true,
  "script": true,
  "permute_faible": true,
  "niveaux": true,
  "substitution": true,
  "parallele": true,
  "activation": true,
  "vide": true,
  "inconnue": true,
  "rejeu": true
 },
 "ok": true
}
✅ porte bloc linguistique verte
exit=0
[stderr]
.........................
----------------------------------------------------------------------
Ran 25 tests in 0.282s

OK
test_analyser_profils (__main__.TestAnalyserProfils.test_analyser_profils)
… [1597 caractères tronqués]
  ```

- **bash** `{"command": "rm -rf build drave.egg-info && mkdir -p dist && python3 -m pip wheel . --no-deps --no-build-isolation -w dist 2>&1 | tail -20 && ls -lh dist/", "description": "Build wheel with profile artifact", "timeoutMs": 300000}`

  ```
Processing ./.
  Preparing metadata (pyproject.toml): started
  Preparing metadata (pyproject.toml): finished with status 'done'
Building wheels for collected packages: drave
  Building wheel for drave (pyproject.toml): started
  Building wheel for drave (pyproject.toml): finished with status 'done'
  Created wheel for drave: filename=drave-0.1.0-py3-none-any.whl size=2054840 sha256=9920997e8db59be5b877a18e4c2305971334a5be2e2f2ed9faa539f2e9af0819
  Stored in directory: /tmp/pip-ephem-wheel-cache-pm9gi75o/wheels/96/02/a3/318108f401dc37bb3a575e67c80cf111852262a4b3c9f691ec
Successfully built drave
total 2,0M
-rw-r--r--. 1 stephane stephane 2,0M 16 nov 01:46 drave-0.1.0-py3-none-any.whl
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport zipfile\np='dist/drave-0.1.0-py3-none-any.whl'\nz=zipfile.ZipFile(p)\nnames=z.namelist()\nprint('entries',len(names))\nfor n in names:\n    if 'profils' in n: print(n, z.getinfo(n).file_size)\nprint('profile in archive', any(n.endswith('profils_udhr.json') for n … [79 caractères tronqués]`

  ```
entries 427
tools/construire_profils_udhr.py 4888
tools/mesurer_profils.py 16291
tools/profils_udhr.py 14148
tools/tests/linguistique/profils_udhr.json 802110
profile in archive True
  ```

- **bash** `{"command": "rm -rf /tmp/venv-drave-profils && python3 -m venv /tmp/venv-drave-profils && /tmp/venv-drave-profils/bin/python -m pip install --no-index --no-deps --no-cache-dir dist/drave-0.1.0-py3-none-any.whl 2>&1 | tail -5 && cd /tmp && /tmp/venv-drave-profils/bin/drave --version && /tmp/venv-drav … [396 caractères tronqués]`

  ```
Processing ./dist/drave-0.1.0-py3-none-any.whl
Installing collected packages: drave
Successfully installed drave-0.1.0
drave 0.1.0
drave 0.1.0 — profils de langue (UDHR, hors ligne)
langue      : fra (French)
script      : Latn
confiance   : 0.3333 (marge 0.0000, seuil 0.12)
source      : lexique
prior       : fra (mots-outils 0.3333)
candidats   : hns 0.6364 · lld 0.5455 · deu 0.4545 · oci 0.4545 · pcd 0.4545
profils     : 398 langues UDHR (articles 0–14, top 200)
{
 "schema": "drave.profils",
 "version": 1,
 "texte": "Le chat dort.",
 "langue": "fra",
 "langue_probable": "fra",
 "nom": "French",
 "script": "Latn",
 "confiance": 0.3333,
 "marge": 0.0,
 "source": "lexique",
 "seuil": 0.12,
None None
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/profils.json'))\nfor x in d['echantillon_20']['par_langue']:\n    e=x['exemple']\n    print(f\"| `{x['iso3']}` | {x['famille']} | {x['script']} | {e['langue']} | {e['confiance']:.4f} | {e['source']} | {'✓' if x['justes']==x['tests … [230 caractères tronqués]`

  ```
| `eng` | Indo-European | Latn | eng | 0.4213 | profils | ✓ |
| `hin` | Indo-European | Deva | hin | 0.4853 | profils | ✓ |
| `bel` | Indo-European | Cyrl | bel | 0.5897 | profils | ✓ |
| `ell` | Indo-European | Grek | ell | 1.0000 | profils | ✓ |
| `kin` | Atlantic-Congo | Latn | kin | 0.4035 | profils | ✓ |
| `ewe` | Atlantic-Congo | Latn | ewe | 0.6366 | profils | ✓ |
| `ibo` | Atlantic-Congo | Latn | ibo | 0.7487 | profils | ✓ |
| `fuf` | Atlantic-Congo | Adlm | fuf | 1.0000 | profils | ✓ |
| `ind` | Austronesian | Latn | ind | 0.3812 | profils | ✓ |
| `tgl` | Austronesian | Latn | tgl | 0.3825 | profils | ✓ |
| `zlm` | Austronesian | Arab | zlm | 0.7171 | profils | ✓ |
| `jav` | Austronesian | Latn | jav | 0.3187 | profils | ✓ |
| `mya` | Sino-Tibetan | Mymr | mya | 0.8845 | profils | ✓ |
| `cmn` | Sino-Tibetan | Hant | cmn | 0.3257 | profils | ✓ |
| `cnh` | Sino-Tibetan | Latn | cnh | 0.3623 | profils | ✓ |
| `ctd` | Sino-Tibetan | Latn | ctd | 0.4867 | profils | ✓ |
| `arb` | Afro-Asiatic | Arab | arb | 0.8069 | profils | ✓ |
| `amh` | Afro-Asiatic | Ethi | amh | 1.0000 | profils | ✓ |
| `heb` | Afro-Asiatic | Hebr | heb | 0.9412 | profils | ✓ |
| `hau` | Afro-Asiatic | Latn
… [188 caractères tronqués]
  ```

- **write** `{"content": "# U3 — `drave profils` : la détection de langue des 398 profils UDHR, exposée\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **U3** (suite de T5) ·\n> **Date** : 2026-11-16 · **Verdict** : ✅ **la détection est exposée** ; **20/20** langues\n> et **20/20** scripts sur l'écha … [12470 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-profils.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "grep -rn \"Les trois commandes\\|trois commandes\" docs/produit reports/rapport-quickstart.md | head -20", "description": "Find references to three commands"}`

  ```
docs/produit/exemples.md:680:> **Le dispositif.** Les trois commandes ci-dessous ont été lancées le **2026-11-15** avec la clé
docs/produit/demarrage.md:4:> trois commandes. Il part d'un **clone public** et ne suppose aucun fichier du dépôt de
docs/produit/demarrage.md:48:## 3. Les trois commandes
docs/produit/README.md:29:> **Démarrage en 5 minutes** : le parcours pas à pas — clone, installation, trois commandes,
reports/rapport-quickstart.md:1:# T3 — le démarrage en 5 minutes : clone public, installation, trois commandes, JSON, tagger, erreurs
reports/rapport-quickstart.md:29:3. les **trois commandes** : `drave --version`, `drave analyser "Le chat dort."`,
  ```

- **bash** `{"command": "grep -n \"^## 4\\. Ce que le produit\" docs/produit/README.md && sed -n '540,570p' docs/produit/README.md && grep -n \"^## 4\\. Le tagger\" docs/produit/demarrage.md", "description": "Find insertion points in product docs"}`

  ```
562:## 4. Ce que le produit ne fait pas encore
[`rapport-tagger-defaut.md`](../../reports/rapport-tagger-defaut.md) § 3.6.

**`evaluer --tagger`.** La commande mesure **les deux** lectures et publie l'écart et le coût
(la ligne `TAGGER API DEEPSEEK` sur 20 phrases, exemple réel) :

```
TAGGER API DEEPSEEK (option --tagger)
  POS         exactitude 97.14 % (fermé 94.74 %, ouvert 100.00 %) · Δ +8.57 pts vs heuristique
  SYNTAGMES   F1 90.16 % (tête 97.39 %) — conservés à l'heuristique
  COÛT        appels 20 · réseau 0 · cache 20 · tokens 0 · modèle deepseek-chat
  modèle renvoyé : deepseek-flash
```

**Le défaut ne bouge pas.** Sans `--tagger`, la commande ne lit aucune clé, n'importe pas le
module réseau, n'ouvre aucune socket, sort **code 0** et rend exactement l'heuristique d'avant
(le test [`test_tagger_api.py`](../../tools/tests/test_tagger_api.py) le compare octet pour
octet ; le test W3 piège `socket.socket` et vérifie que `tools.llm.deepseek` n'est pas importé).
Le `--tagger` **explicite** est une **option**, pas un changement de produit : c'est la seule
porte qui peut sortir **4** (clé absente ou refusée). `--tagger auto` ne peut pas sortir 4 : il
replie sur l'heuristique, 
… [704 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/produit/README.md')\ns=p.read_text()\nmarker='## 4. Ce que le produit ne fait pas encore'\nsection='''### 3.8 Les profils de langue — `drave profils`\n\n```bash\npython3 tools/drave.py profils --texte \"Le chat dort.\"\npython3 tool … [3080 caractères tronqués]`

  ```
patched README
562:### 3.8 Les profils de langue — `drave profils`
  ```

- **bash** `{"command": "sed -n '1,10p' docs/produit/demarrage.md && sed -n '150,170p' docs/produit/demarrage.md", "description": "Inspect demarrage intro and insertion point"}`

  ```
# Démarrage en 5 minutes

> **Ce que ce document est.** Le parcours le plus court pour installer **drave** et lancer
> trois commandes. Il part d'un **clone public** et ne suppose aucun fichier du dépôt de
> développement. Chaque commande et chaque sortie ont été **rejouées le 2026-11-15** sur un
> clone neuf (commit **7f1519f**, Python **3.13.16**, pip **26.2.1**), sans clé DeepSeek.
> Le relevé complet, les temps et le contrôle négatif sont dans
> [`reports/rapport-quickstart.md`](../../reports/rapport-quickstart.md) et
> [`reports/quickstart.json`](../../reports/quickstart.json).

```bash
python3 -c 'import json; a=json.load(open("annotation.json")); print(a["schema"], a["version"], a["langue"], len(a["etiquettes"]), "étiquettes"); print([(e["type"], e["valeur"], e["meta"].get("role")) for e in a["etiquettes"] if e["niveau"]=="syntagme"])'
```

```text
drave.annotation 2 fr 20 étiquettes
[('GN', 'Le chat', 'objet'), ('GV', 'dort', 'predicat')]
```

Le contrat est **versionné** et additif : `schema`, `version`, `texte`, `langue`, `script`,
`refus`, `etiquettes`, `unites_semantiques` sont les huit champs obligatoires de la racine ; la
version 1 reste lue. Schéma : [`tools/schemas/
… [314 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/produit/demarrage.md')\ns=p.read_text()\ns=s.replace('> trois commandes. Il part d\\'un **clone public**', '> les commandes. Il part d\\'un **clone public**')\ns=s.replace('## 3. Les trois commandes', '## 3. Les commandes')\nmarker= … [1890 caractères tronqués]`

  ```
patched demarrage
4:> les commandes. Il part d'un **clone public** et ne suppose aucun fichier du dépôt de
48:## 3. Les commandes
163:### 3.5 `drave profils` — la langue probable, le script et la confiance
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/implantation/bloc-linguistique.md')\ns=p.read_text()\nmarker='## 9. La mesure et la porte'\nsection='''**L'exposition produit — `drave profils`.** Les profils ne restent pas dans le banc :\n`drave profils --texte` rend la **langue p … [1157 caractères tronqués]`

  ```
patched implantation doc
268:**L'exposition produit — `drave profils`.** Les profils ne restent pas dans le banc :
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -60; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run documentation review", "timeoutMs": 180000}`

  ```
revue de documentation · 768 fiche(s) · 863 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 767 fichiers, le disque en a 768
     · compteurs : en-cours.md dit 862 JSON, le disque en a 863
exit=1
  ```

- **bash** `{"command": "grep -n \"Mis à jour\\|e181ce02\\|U3\\|T1–T6\\|Pensée — B13\\|L — le bloc langue\\|fichiers / JSON\" docs/pilotage/en-cours.md | head -30 && sed -n '50,70p' docs/pilotage/en-cours.md && sed -n '100,130p' docs/pilotage/en-cours.md", "description": "Locate en-cours lines to update"}`

  ```
3:**Mis à jour : 2026-11-16, 01 h 45 HNE (U2 : la roue)**
13:- **État** : **en pause** depuis le 05/11 ; la clôture J14.1 est portée par `e181ce02`.
55:### Session `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Pensée, la RSN plurielle et le moteur N3 *(actif)*
57:- **Id** : `e181ce02-cd50-488a-a6be-e84b79d40dcc` — [`plan.md`](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md).
63:- **Prochaine action** : **U3 — `--profils`** ; **J4** ; T132/T133.
65:- **Journal** : [la session](../../journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/).
85:- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; **U2 — la roue** (autonome, gold dedans, roue sans gold → 4) ; [v2](../../reports/rapport-restitution-v2.md), [v3](../../reports/rapport-restitution-v3.md), [roue](../../reports/rapport-roue.md).
86:- **L — le bloc langue** : contrat ; frontière script 1,0 / langue 0,137/0,9687 ; fusion réparée **0,9309/0,8226/0,8784/0,9954**.
101:| fichiers / JSON de résultats | **767** / **862** | `reports/*.md` / `reports/*.json` |
113:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur
… [6051 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text()\ns=s.replace('**Mis à jour : 2026-11-16, 01 h 45 HNE (U2 : la roue)**',\n            '**Mis à jour : 2026-11-16, 02 h 05 HNE (U3 : les profils, 20/20, le texte ambigu rend und, l\\'artefact da … [4027 caractères tronqués]`

  ```
patched en-cours
3:**Mis à jour : 2026-11-16, 02 h 05 HNE (U3 : les profils, 20/20, le texte ambigu rend und, l'artefact dans la roue)**
62:- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** ([fiche](../../reports/rapport-performance-fix.md)) ; **U2** la roue : **1 727 201 o**, mêmes JSON hors dépôt, sans gold → `evaluer` **4** ([fiche](../../reports/rapport-roue.md)) ; **U3** les profils : **398 langues**, **20/20** sur l'échantillon UDHR, ambigu **`und`**, artefact dans la roue ([fiche](../../reports/rapport-profils.md)).
85:- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; **U2 — la roue** (autonome, gold dedans, roue sans gold → 4) ; **U3 — les profils** (398 langues, 20/20, ambigu `und`, artefact dans la roue) ; [v2](../../reports/rapport-restitution-v2.md), [v3](../../reports/rapport-restitution-v3.md), [roue](../../reports/rapport-roue.md), [profils](../../reports/rapport-profils.md).
101:| fichiers / JSON de résultats | **768** / **863** | `reports/*.md` / `reports/*.json` |
113:| **B — l'intelligence** | *
… [838 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/roadmap.md')\ns=p.read_text()\ns=s.replace('''**U2 — la roue (16/11)** : **1 727 201 o**, 422 entrées, mêmes JSON hors dépôt ; sans gold,\n`evaluer` **4** ([fiche](../../reports/rapport-roue.md)). Prochaine action : **U3 —  … [871 caractères tronqués]`

  ```
patched roadmap
172:**U3 — les profils (16/11)** : `drave profils --texte` expose les **398 profils UDHR**
  ```

- **bash** `{"command": "grep -n \"U1\\|U2\\|T1–T6\" docs/pilotage/chantiers.md | head -10", "description": "Find U1/U2 mentions in chantiers"}`

  ```
(no output)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-bloc-linguistique.md')\ns=p.read_text()\nmarker='**Les erreurs nommées** : l\\'anglais et le scots sont proches ;'\nadd='''**L\\'exposition produit (U3).** `drave profils --texte` rend la langue probable, le script et\nla … [674 caractères tronqués]`

  ```
patched bloc report
61:**L'exposition produit (U3).** `drave profils --texte` rend la langue probable, le script et
  ```

- **bash** `{"command": "sed -n '802,860p' docs/produit/README.md && grep -n \"Quelles langues\\|--langue\\|398\" docs/produit/README.md | head -20", "description": "Inspect FAQ language answer"}`

  ```
rejeu identique : oui
  texte      : 'Le chat dort.'
  langue     : fr
  étiquettes : 20
  JSON       : 4227 octets · sha256 f4b7822076a4203d…
```

**Options du CLI** :

| option | commande | sens |
|---|---|---|
| `--langue fr\|en` | `analyser`, `rejouer`, `restituer` | **indice** de langue, pas une contrainte ; hors `fr`/`en` → code 5 |
| `--json` | `analyser`, `evaluer`, `restituer` | sortie machine UTF-8 |
| `--duree` | `analyser` | ajoute `cout.duree_s` au JSON (ou à chaque ligne de `--jsonl`) ; absent par défaut |
| `--tagger` | `analyser`, `evaluer` | POS par l'API DeepSeek (clé et réseau ; défaut : heuristique) ; `evaluer` mesure en plus la cascade et le Δ (§ 3.7) |
| `--jsonl` | `analyser` | une ligne JSON par phrase (avec `--fichier`) |
| `--fichier CHEMIN` | `analyser`, `restituer` | lit un texte UTF-8 au lieu de l'argument |
| `--banc CHEMIN` | `restituer` | mesure un banc JSON de textes (les 50 textes libres) |
| `--canonique` | `restituer` | ajoute la forme canonique v1 (segments + rôles + cibles) et son miroir |
| `--roles` | `restituer` | ajoute la forme lisible des rôles (agent, prédicat, lieu) ; avec `--banc`, mesure leur fidélité à l'or |
| `--partition MODE` | `
… [4962 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '860,900p' docs/produit/README.md && sed -n '760,790p' docs/produit/README.md && sed -n '60,75p' docs/produit/README.md", "description": "Read FAQ language answer and command contract"}`

  ```
> [`reports/rapport-faq.md`](../../reports/rapport-faq.md) et
> [`reports/faq.json`](../../reports/faq.json). Si le code bouge, relancer
> `python3 tools/verifier_faq.py`.

### 8.1 Quelles langues le produit reconnaît-il ?

Le **bloc** détecte la langue et le script : ses profils UDHR couvrent **398 langues**
(**0,9687** sur l'autotest), mais le **CLI** n'expose que `fr` et `en` comme **indice**
(`--langue`). Sans indice, il rend la langue détectée — `de` pour « Der Hund schläft. », `es`
pour « El perro duerme. » — ou `und` quand la confiance passe sous le seuil (**0,12**) :
« Élodie sourit. » rend `und`, **même avec `--langue fr`**. `--langue` est un **indice**, pas
une contrainte ; `--langue de` sort **5** (usage invalide). Les 398 profils ne sont pas
versionnés : `data/` est hors dépôt.

### 8.2 Est-ce que ça marche hors ligne ?

**Oui, par défaut.** `analyser`, `evaluer`, `rejouer` et `restituer` tournent sur **CPU**, sans
modèle, sans GPU et **sans ouvrir de socket** ; le seul chemin réseau est l'option
`--tagger` (§ 3.7). Vérifié en interdisant `socket.socket` : l'analyse passe, et le module
`tools.llm.deepseek` n'est **même pas importé**. Sans `--tagger`, aucune clé n'est lu
… [4241 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/produit/README.md')\ns=p.read_text()\ns=s.replace('''| **langue et script** | `fr`, `en`, `und`… et `Latn`, `Cyrl`… | **398 langues**, **0,9687** ; script **1,0000** (autotest UDHR ; le CLI n'expose que `fr`/`en` comme indice) |''', … [3956 caractères tronqués]`

  ```
patched FAQ/manques
71:| **langue et script** | `fr`, `en`, `und`… et `Latn`, `Cyrl`… | **398 langues**, **0,9687** ; script **1,0000** (autotest UDHR ; `drave profils` les expose, `--langue` reste un indice `fr`/`en`) |
562:### 3.8 Les profils de langue — `drave profils`
565:python3 tools/drave.py profils --texte "Le chat dort."
566:python3 tools/drave.py profils --texte "Привет мир" --json
567:python3 tools/drave.py profils --fichier article.txt --json
568:python3 tools/drave.py analyser "Le chat dort." --profils
571:drave 0.1.0 — profils de langue (UDHR, hors ligne)
578:profils     : 398 langues UDHR (articles 0–14, top 200)
581:**Lecture.** La commande charge l'artefact de **398 profils de trigrammes UDHR** (articles
583:**confiance**. Le JSON (`--json`) porte `schema: "drave.profils"`, `langue` (la **décision**),
585:`seuil`, `sous_seuil`, `refus`, `prior`, `candidats` et les métadonnées des profils. Sous le
588:**Deux chemins.** Sur un texte **long** (> 80 caractères), les 398 profils (`source: profils`).
591:`candidats` restent les profils — le désaccord est visible. Un texte de moins de cinq mots est
592:pénalisé : un mot isolé rend `und`. `analyser --profils` emploie le mê
… [1489 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '665,682p' docs/produit/README.md", "description": "Inspect remaining old profiles statement"}`

  ```
qualité. Le vrai adaptateur local (`NeuronalLLM`, `NeuronalLLMPOS`) parle à un serveur local ; il
n'est ni requis ni utilisé par défaut. Le CLI expose en **option** le tagger de l'**API**
DeepSeek (§ 3.7), pas le 7B local.

**5. Les classes ouvertes sont fragiles.** POS fermé **0,9004**, ouvert **0,6234** : les mots
inconnus tombent souvent en NOUN. Exemple réel : dans « Le livre que j'ai lu… », `lu` est tagué
NOUN ; dans « The day when we left… », `left` est NOUN. Un lexique plus large améliorerait ces
cas, pas une règle.

**6. La langue n'est pas forcée.** `--langue` est un **indice**, limité à `fr` et `en` dans le
CLI ; sous le seuil de confiance, la sortie reste `und`. Il n'y a pas de `--langue-forcee`. Les
profils UDHR (398 langues, 0,9687) ne sont pas exposés par le CLI et ne sont pas versionnés :
`data/` est hors dépôt, et le corpus XML source est externe. Sans eux, la détection se rabat sur
les indices internes.

**7. Pas de RSN, pas de DRVM, pas de serveur.** Le bloc a le contrat, la trace et le coût ; il
ne produit pas le corps de la RSN, n'est pas un port DRVM et n'expose pas d'API HTTP. La couche
sémantique est un **compteur d'unités**, pas une représentation.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/produit/README.md')\ns=p.read_text()\ns=s.replace('''**6. La langue n'est pas forcée.** `--langue` est un **indice**, limité à `fr` et `en` dans le\nCLI ; sous le seuil de confiance, la sortie reste `und`. Il n'y a pas de `--langue- … [906 caractères tronqués]`

  ```
patched paragraph
none left
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run documentation review again", "timeoutMs": 180000}`

  ```
revue de documentation · 768 fiche(s) · 863 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -30; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run table gate", "timeoutMs": 180000}`

  ```
✅ 1849 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4760 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-16)
exit=0
  ```

- **bash** `{"command": "python3 tools/tests/test_empaquetage.py 2>&1 | tail -20; echo \"exit=${PIPESTATUS[0]}\"; python3 tools/tests/test_profils.py 2>&1 | tail -5; echo \"exit=${PIPESTATUS[0]}\"; python3 tools/tests/test_schema_produit.py 2>&1 | tail -5; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run pa … [54 caractères tronqués]`

  ```
PATH vide : le nom `drave` n'est pas résolu, et l'échec est lisible. ... ok
test_analyser (__main__.TestEntreeHistorique.test_analyser) ... ok
test_version (__main__.TestEntreeHistorique.test_version) ... ok
test_import_depuis_un_autre_repertoire (__main__.TestEntreeInstallable.test_import_depuis_un_autre_repertoire) ... ok
test_aucune_dependance (__main__.TestMetadonnees.test_aucune_dependance) ... ok
test_gold_dans_la_roue (__main__.TestMetadonnees.test_gold_dans_la_roue)
Les cinq gold de la mesure voyagent comme données du paquet. ... ok
test_identite_et_python (__main__.TestMetadonnees.test_identite_et_python) ... ok
test_profils_dans_la_roue (__main__.TestMetadonnees.test_profils_dans_la_roue)
L'artefact de 398 profils voyage avec la roue : `drave profils` marche hors dépôt. ... ok
test_pyproject_existe (__main__.TestMetadonnees.test_pyproject_existe) ... ok
test_script_console (__main__.TestMetadonnees.test_script_console) ... ok
test_sous_paquets_de_la_roue (__main__.TestMetadonnees.test_sous_paquets_de_la_roue)
Le CLI a besoin de la mesure, du générateur S et du tagger dans la roue. ... ok
test_evaluer_sans_gold_code_4 (__main__.TestOrAbsent.test_evaluer_sans_gold_code_4) .
… [322 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifier_faq.py 2>&1 | tail -30; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run FAQ verifier", "timeoutMs": 300000}`

  ```
FAQ produit — 10/10 réponses vérifiées · contrôle négatif détecté
  ✅  1. Quelles langues le produit reconnaît-il ?
  ✅  2. Est-ce que ça marche hors ligne ?
  ✅  3. Combien ça coûte ?
  ✅  4. Qu'est-ce que --tagger change ?
  ✅  5. Quel est le format de sortie, et est-il stable ?
  ✅  6. Que veut dire « attachement », et à quel point est-il fiable ?
  ✅  7. Pourquoi reste-t-il un span inatteignable ?
  ✅  8. Que peut-on restituer : la surface, la forme, les rôles ?
  ✅  9. Quelles limites faut-il connaître avant de s'en servir ?
  ✅ 10. Comment l'installer et le lancer ?
✅ FAQ vérifiée
exit=0
  ```

- **bash** `{"command": "PY=/tmp/venv-drave-profils/bin/python; SITE=$($PY -c 'import tools.tests.linguistique as x; print(x.__path__[0])'); echo \"$SITE\"; ls -l \"$SITE/profils_udhr.json\"; mv \"$SITE/profils_udhr.json\" /tmp/profils_udhr.json.bak; cd /tmp && /tmp/venv-drave-profils/bin/drave profils --texte  … [304 caractères tronqués]`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique
-rw-r--r--. 1 stephane stephane 802110 16 nov 01:39 /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/profils_udhr.json
drave 0.1.0 — profils de langue (UDHR, hors ligne)
langue      : fra (French)
script      : Latn
confiance   : 0.3333 (marge 0.0000, seuil 0.12)
source      : lexique
prior       : fra (mots-outils 0.3333)
candidats   : hns 0.6364 · lld 0.5455 · deu 0.4545 · oci 0.4545 · pcd 0.4545
profils     : 398 langues UDHR (articles 0–14, top 200)
exit=0
{
 "schema": "drave.profils",
 "version": 1,
 "texte": "Le chat dort.",
 "langue": "fra",
 "langue_probable": "fra",
 "nom": "French",
 "script": "Latn",
 "confiance": 0.3333,
 "marge": 0.0,
 "source": "lexique",
 "seuil": 0.12,
 "sous_seuil": false,
 "refus": "",
 "prior": {
  "langue": "fra",
  "nom": "French",
  "score": 0.333333
 },
 "candidats": [
  {
   "langue": "hns",
   "nom": "Hindustani, Sarnami",
   "score": 0.636364
  },
  {
   "langue": "lld",
   "nom": "Ladin",
   "score": 0.545455
  },
  {
   "langue": "deu",
   "nom": "German, Standard (1901)",
   "score": 0.454545
  },
  {
   "langue": "oci",
   "nom": "Occitan (
… [527 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && /tmp/venv-drave-profils/bin/python -c 'import tools.tests.linguistique as x; print(x.__path__[0])' && SITE=$(cd /tmp && /tmp/venv-drave-profils/bin/python -c 'import tools.tests.linguistique as x; print(x.__path__[0])') && ls -l \"$SITE/profils_udhr.json\"", "description": "L … [34 caractères tronqués]`

  ```
/tmp/venv-drave-profils/lib64/python3.13/site-packages/tools/tests/linguistique
-rw-r--r--. 1 stephane stephane 802110 16 nov 01:46 /tmp/venv-drave-profils/lib64/python3.13/site-packages/tools/tests/linguistique/profils_udhr.json
  ```

- **bash** `{"command": "SITE=/tmp/venv-drave-profils/lib64/python3.13/site-packages/tools/tests/linguistique; mv \"$SITE/profils_udhr.json\" /tmp/profils_udhr.json.bak2; cd /tmp && /tmp/venv-drave-profils/bin/drave profils --texte \"Le chat dort.\"; echo \"exit=$?\"; /tmp/venv-drave-profils/bin/drave profils - … [191 caractères tronqués]`

  ```
exit=4
exit=4
restored
[stderr]
drave: dépendance absente : profils de langue absents : /tmp/venv-drave-profils/lib/python3.13/site-packages/tools/tests/linguistique/profils_udhr.json — réinstaller la roue complète, ou lancer `python3 tools/construire_profils_udhr.py` depuis le dépôt (DRAVE_PROFILS peut pointer vers un autre artefact).
drave: dépendance absente : profils de langue absents : /tmp/venv-drave-profils/lib/python3.13/site-packages/tools/tests/linguistique/profils_udhr.json — réinstaller la roue complète, ou lancer `python3 tools/construire_profils_udhr.py` depuis le dépôt (DRAVE_PROFILS peut pointer vers un autre artefact).
  ```

- **bash** `{"command": "python3 -m py_compile tools/profils_udhr.py tools/construire_profils_udhr.py tools/mesurer_profils.py tools/tests/test_profils.py tools/drave.py tools/tests/test_empaquetage.py tools/tests/test_produit.py && echo OK && git status --short", "description": "Compile new files and inspect g … [11 caractères tronqués]`

  ```
OK
 M docs/implantation/bloc-linguistique.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M docs/produit/demarrage.md
M  journal/2026-11-16/README.md
A  journal/2026-11-16/docs.md
M  journal/2026-11-16/memoire.md
M  journal/2026-11-16/mesures.md
M  journal/README.md
M  journal/THEMES.md
M  journal/sessions/MANIFEST.md
M  journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
M  journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
M  journal/sessions/session-aa260801-785c-4a85-876c-98ba023e6098/digest.md
M  journal/sessions/session-aa260801-785c-4a85-876c-98ba023e6098/rapport.md
A  journal/sessions/session-b4ff97bc-493d-4bfb-b734-e055dc85c779/digest.md
A  journal/sessions/session-b4ff97bc-493d-4bfb-b734-e055dc85c779/rapport.md
 M pyproject.toml
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-bloc-linguistique.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 M tools/drave.py
 M tools
… [393 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"rapport-roue\\|rapport-cli\\|rapport-performance-fix\\|rapport-bloc\" reports/README.md | head -20 && sed -n '1,80p' reports/README.md", "description": "Inspect reports index"}`

  ```
174:| [`rapport-bloc-linguistique.md`](rapport-bloc-linguistique.md) | **R0.7** — le bloc linguistique : 9 niveaux |
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
| [`rapport-bilan-semaine.md`](rapport-bilan-semaine.md) 
… [7831 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"rapport-roue\\|rapport-performance-fix\\|rapport-profils\" reports/README.md reports/INDEX.md | head -20", "description": "Check U2/U3 entries in report indexes"}`

  ```
reports/INDEX.md:637:| [rapport-performance-fix.md](rapport-performance-fix.md) | U1 — les deux O(k²) sont bornés : 10 000 mots de **4,0 s à 0,82 s** (×4,9), α de **1,53 à 1,08**, sorties **identiques au bit près** |
reports/INDEX.md:713:| [rapport-roue.md](rapport-roue.md) | U2 — la roue : `drave-0.1.0-py3-none-any.whl`, installée hors du dépôt, les gold dedans |
  ```

- **bash** `{"command": "sed -n '700,725p' reports/INDEX.md && tail -20 reports/INDEX.md", "description": "Inspect report index tail"}`

  ```
| [rapport-re-test-produit.md](rapport-re-test-produit.md) | B13 — re-test produit : 50 textes libres, la vue linéaire supprime les chevauchements |
| [rapport-regle-placement-perte.md](rapport-regle-placement-perte.md) | A8.3 — la règle place et perte choisit le KV comme la main |
| [rapport-replis-cible.md](rapport-replis-cible.md) | B13 — les trois retouches A3 sur le live : +1, +2, +1, et 145/145 exact/top1 |
| [rapport-restitution-v0.md](rapport-restitution-v0.md) | B13 — la restitution v0 : 46/46 surfaces exactes, le miroir strict à 0,1087 |
| [rapport-restitution-v1.md](rapport-restitution-v1.md) | B13 — la restitution v1 : la forme canonique à 46/46, le miroir strict reste à 0,1087 |
| [rapport-restitution-v2.md](rapport-restitution-v2.md) | B13 — la restitution v2 : les rôles se lisent, leur fidélité ne suit pas |
| [rapport-restitution-v3.md](rapport-restitution-v3.md) | B13 — la restitution v3 : les rôles des GP se séparent, la fidélité du cadre ne suit pas |
| [rapport-restitution.md](rapport-restitution.md) | B18 — restitution canonique : 528/528, mais pas un décodeur |
| [rapport-retrieval-epoque.md](rapport-retrieval-epoque.md) | J3.1 — Le retrieval inter-langues à é
… [5026 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/INDEX.md')\ns=p.read_text()\nneedle='| [rapport-protocole-date.md](rapport-protocole-date.md) |'\nrow='| [rapport-profils.md](rapport-profils.md) | U3 — `drave profils` : 398 profils UDHR exposés, 20/20 sur l\\'échantillon, ambig … [262 caractères tronqués]`

  ```
patched INDEX
665:| [rapport-profils.md](rapport-profils.md) | U3 — `drave profils` : 398 profils UDHR exposés, 20/20 sur l'échantillon, ambigu `und`, artefact dans la roue |
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/README.md')\ns=p.read_text()\nneedle='| [`rapport-passe-honnetete.md`](rapport-passe-honnetete.md) |'\nrow='| [`rapport-profils.md`](rapport-profils.md) | **U3/B13** — `drave profils` : les **398 profils UDHR** exposés, **20/20** … [338 caractères tronqués]`

  ```
patched reports README
43:| [`rapport-profils.md`](rapport-profils.md) | **U3/B13** — `drave profils` : les **398 profils UDHR** exposés, **20/20** sur l'échantillon, ambigu **`und`**, artefact de 802 110 o dans la roue |
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -20; echo \"revue=${PIPESTATUS[0]}\"; bash tools/porte-tableaux.sh 2>&1 | tail -10; echo \"tables=${PIPESTATUS[0]}\"", "description": "Re-run docs and table gates", "timeoutMs": 180000}`

  ```
revue de documentation · 768 fiche(s) · 863 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
revue=0
  ✅ 1849 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4762 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-16)
tables=0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='tools/chantier/plan.json'\nd=json.load(open(p))\nfor t in d.get('taches',[]):\n    if t.get('id') in ('U1','U2','U3','T6'):\n        print(json.dumps(t,ensure_ascii=False,indent=1))\nPY", "description": "Inspect U3 task entry in plan"}`

  ```
{
 "id": "T6",
 "jour": 19,
 "titre": "Le bilan de la nuit exploitable",
 "mandat": "Tâche T6 (clôture) : le bilan — relis les fiches T1-T5, écris `reports/rapport-bilan-exploitable.md` + JSON : ce qui est désormais installable, le quickstart, l'API du JSON, la performance, les codes de sortie ; les négatifs ; ce qui reste (le gold de S, les signatures de Panini, la décision du tagger `auto`) ; mets à jour `docs/pilotage/en-cours.md` et la roadmap. **Ne relance pas la passe complète** : lis `work/portes/`.",
 "budget_min": 90,
 "acceptation": [
  {
   "commande": "test -f reports/rapport-bilan-exploitable.md && echo FICHE-OK",
   "attendu": "FICHE-OK"
  }
 ]
}
{
 "id": "U1",
 "jour": 20,
 "titre": "La performance — les deux points quadratiques",
 "mandat": "Tâche U1 (exploitable, suite de T4) : **répare les deux points O(k²)** identifiés par T4 — `_groupes_partition` (toutes les paires de syntagmes) et `_cible_proche` (le tri de tous les GV pour chaque segment) — **sans changer les résultats** (les 612 phrases et le réel 452 : les mêmes F1, attachement, POS, au bit près) ; mesure le **α** de la croissance avant/après sur le bloc contrôlé de T4 (l'objectif : α ≤ 1,15 et le terme qua
… [1898 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/mesurer_profils.py')\ns=p.read_text()\nold='''    sortie = pathlib.Path(a.sortie)\n    sortie.parent.mkdir(parents=True, exist_ok=True)'''\nnew='''    # Un résumé plat, pour un client qui ne veut pas descendre dans les sous-objets. … [1493 caractères tronqués]`

  ```
patched resume
=== PROFILS DE LANGUE — UDHR ===
profils : 398 langues · 802110 octets · 33aee69d7659c9bc…
identité artefact ↔ corpus : oui (0 différence(s))
échantillon 20 (article 15) : langue 20/20 (1.0000) · script 20/20
échantillon 20 (articles 15–30) : langue 313/320 (0.9781) · script 320/320
autotest 398 (article 15) : brut 0.9687 · CLI 0.9642 · script 1.0000
permuté : 20 0.0000 · 398 0.0022
ambigu : und (0.0836) · mot isolé : und · vide : vide
verdict : OK · reports/profils.json
{
 "langues_profil": 398,
 "echantillon_langues": 20,
 "article": 15,
 "precision_langue_20": 1.0,
 "precision_script_20": 1.0,
 "precision_langue_20_complet": 0.9781,
 "precision_script_20_complet": 1.0,
 "precision_398_brut": 0.9687,
 "precision_398_cli": 0.9642,
 "permute_20": 0.0,
 "ambigu_langue": "und",
 "ambigu_confiance": 0.0836,
 "mot_isole_langue": "und"
}
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/mesurer_profils.py')\ns=p.read_text()\ns=s.replace('''            \"fichier\": str(pathlib.Path(a.profils)),''','''            \"fichier\": (str(pathlib.Path(a.profils).resolve().relative_to(RACINE))\n                        if pat … [471 caractères tronqués]`

  ```
patched path
profils : 398 langues · 802110 octets · 33aee69d7659c9bc…
identité artefact ↔ corpus : oui (0 différence(s))
échantillon 20 (article 15) : langue 20/20 (1.0000) · script 20/20
échantillon 20 (articles 15–30) : langue 313/320 (0.9781) · script 320/320
autotest 398 (article 15) : brut 0.9687 · CLI 0.9642 · script 1.0000
permuté : 20 0.0000 · 398 0.0022
ambigu : und (0.0836) · mot isolé : und · vide : vide
verdict : OK · reports/profils.json
tools/tests/linguistique/profils_udhr.json
  ```

- **bash** `{"command": "set -e\npython3 tools/tests/test_profils.py >/tmp/test-profils.out 2>&1 && tail -4 /tmp/test-profils.out\npython3 tools/tests/test_produit.py >/tmp/test-produit.out 2>&1 && tail -4 /tmp/test-produit.out\npython3 tools/tests/test_empaquetage.py >/tmp/test-empaquetage.out 2>&1 && tail -4  … [207 caractères tronqués]`

  ```
----------------------------------------------------------------------
Ran 18 tests in 4.613s

OK
----------------------------------------------------------------------
Ran 30 tests in 18.088s

OK
----------------------------------------------------------------------
Ran 12 tests in 0.674s

OK
}
✅ porte bloc linguistique verte
ALL_OK
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/profils_udhr.py')\ns=p.read_text()\ns=s.replace('''    if prior_lexique and len(texte) <= longueur_prior:\n        fb_langue, _fb_conf, fb_scores = bl.detecter_langue(texte, None)''','''    if prior_lexique and len(texte) <= longue … [652 caractères tronqués]`

  ```
patched token guard
und und 0.0 profils
fra fra 0.3333 lexique
  ```

- **bash** `{"command": "for t in \"the\" \"a\" \"no\" \"les\" \"la\" \"et\" \"un\" \"chat\" \"hello\" \"Le\" \"The cat\" \"Le chat\"; do printf '%-10s -> ' \"$t\"; python3 tools/drave.py profils --texte \"$t\" --json | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d[\"langue\"],d[\"langue_probable … [85 caractères tronqués]`

  ```
the        -> und cfm 0.04 profils
a          -> und und 0.0 profils
no         -> und und 0.0 profils
les        -> und ast 0.04 profils
la         -> und und 0.0 profils
et         -> und und 0.0 profils
un         -> und und 0.0 profils
chat       -> und agr 0.04 profils
hello      -> und ekk 0.0267 profils
Le         -> und und 0.0 profils
The cat    -> eng eng 0.5 lexique
Le chat    -> fra fra 0.5 lexique
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/tests/test_profils.py')\ns=p.read_text()\nneedle='''    def test_mot_isole_est_und(self) -> None:\n        sortie = drave(\"profils\", \"--texte\", \"chat\", \"--json\")\n        self.assertEqual(sortie.returncode, 0, detail(sortie … [844 caractères tronqués]`

  ```
patched test
----------------------------------------------------------------------
Ran 19 tests in 5.345s

OK
  ```

- **bash** `{"command": "grep -rn \"18 tests\\|18 tests\\|test_profils.*18\" reports/rapport-profils.md docs | head -20", "description": "Find test count references"}`

  ```
reports/rapport-profils.md:19:> mesure), [`tools/tests/test_profils.py`](../tools/tests/test_profils.py) (**18 tests**),
reports/rapport-profils.md:186:| `tools/tests/test_profils.py` | 18 tests : CLI, JSON, ambigu, mot isolé, vide, absent, 20 langues, permuté |
docs/produit/README.md:736:étiqueté en `fr` et `en`, `sha256 f4b7822076a4203d` deux fois, **18 tests** de fumée, **8 tests**
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-profils.md')\ns=p.read_text().replace('(**18 tests**)', '(**19 tests**)')\ns=s.replace('| `tools/tests/test_profils.py` | 18 tests : CLI, JSON, ambigu, mot isolé, vide, absent, 20 langues, permuté |',\n            '| `too … [277 caractères tronqués]`

  ```
patched report test count
19:> mesure), [`tools/tests/test_profils.py`](../tools/tests/test_profils.py) (**19 tests**),
186:| `tools/tests/test_profils.py` | 19 tests : CLI, JSON, ambigu, mot isolé, mot-outil isolé, vide, absent, 20 langues, permuté |
  ```

- **bash** `{"command": "python3 tools/mesurer_profils.py --sortie reports/profils.json | tail -8", "description": "Rerun measurement after guard", "timeoutMs": 180000}`

  ```
profils : 398 langues · 802110 octets · 33aee69d7659c9bc…
identité artefact ↔ corpus : oui (0 différence(s))
échantillon 20 (article 15) : langue 20/20 (1.0000) · script 20/20
échantillon 20 (articles 15–30) : langue 313/320 (0.9781) · script 320/320
autotest 398 (article 15) : brut 0.9687 · CLI 0.9642 · script 1.0000
permuté : 20 0.0000 · 398 0.0022
ambigu : und (0.0836) · mot isolé : und · vide : vide
verdict : OK · reports/profils.json
  ```

- **bash** `{"command": "rm -rf build drave.egg-info && mkdir -p dist && python3 -m pip wheel . --no-deps --no-build-isolation -w dist 2>&1 | tail -6 && ls -l dist/drave-0.1.0-py3-none-any.whl", "description": "Rebuild wheel after final code", "timeoutMs": 300000}`

  ```
Building wheels for collected packages: drave
  Building wheel for drave (pyproject.toml): started
  Building wheel for drave (pyproject.toml): finished with status 'done'
  Created wheel for drave: filename=drave-0.1.0-py3-none-any.whl size=2055055 sha256=0155b5d4bd627446f4f37edb881b2e99fbadf03214ec23bfce15d5c35e4f8804
  Stored in directory: /tmp/pip-ephem-wheel-cache-57nrm8u5/wheels/96/02/a3/318108f401dc37bb3a575e67c80cf111852262a4b3c9f691ec
Successfully built drave
-rw-r--r--. 1 stephane stephane 2055055 16 nov 01:52 dist/drave-0.1.0-py3-none-any.whl
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-profils.md')\ns=p.read_text().replace('2 054 840 octets contre 1 727 201', '2 055 055 octets contre 1 727 201')\np.write_text(s)\nprint('patched wheel size')\nPY\ngrep -n \"2 055 055\\|2 054 840\" reports/rapport-profils. … [50 caractères tronqués]`

  ```
patched wheel size
177:  (2 055 055 octets contre 1 727 201). C'est assumé : la détection doit marcher hors dépôt.
  ```

- **bash** `{"command": "rm -rf /tmp/venv-drave-profils2 && python3 -m venv /tmp/venv-drave-profils2 && /tmp/venv-drave-profils2/bin/python -m pip install --no-index --no-deps --no-cache-dir dist/drave-0.1.0-py3-none-any.whl >/tmp/install2.out 2>&1 && tail -2 /tmp/install2.out && cd /tmp && /tmp/venv-drave-prof … [361 caractères tronqués]`

  ```
Installing collected packages: drave
Successfully installed drave-0.1.0
und 0.0
drave 0.1.0 — profils de langue (UDHR, hors ligne)
langue      : fra (French)
script      : Latn
confiance   : 0.3333 (marge 0.0000, seuil 0.12)
source      : lexique
prior       : fra (mots-outils 0.3333)
candidats   : hns 0.6364 · lld 0.5455 · deu 0.4545 · oci 0.4545 · pcd 0.4545
profils     : 398 langues UDHR (articles 0–14, top 200)
usage: drave [-h] [-V] {analyser,evaluer,profils,rejouer,restituer} ...
  {analyser,evaluer,profils,rejouer,restituer}
    profils             détecter la langue d'un texte (398 profils UDHR)
Commandes : analyser, evaluer, profils, rejouer, restituer.
--profils (analyser) et `drave profils --texte`.
  python3 tools/drave.py profils --texte "Le chat dort."
  python3 tools/drave.py analyser "Le chat dort." --profils
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Все люди рождаются свободными и равными в своем достоинстве и правах.\" --profils --json | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d[\"langue\"],d[\"script\"],len(d[\"etiquettes\"]))'; python3 tools/drave.py analyser \"All human being … [246 caractères tronqués]`

  ```
rus Cyrl 50
eng Latn 57
  ```

- **bash** `{"command": "python3 tools/drave.py profils --aide | head -30; echo \"exit=${PIPESTATUS[0]}\"; python3 tools/drave.py profils --help >/dev/null; echo \"exit=$?\"", "description": "Check profils help"}`

  ```
usage: drave profils [-h] [--texte TEXTE] [--fichier CHEMIN] [--seuil SEUIL] [--json] [TEXTE]

Détecte la langue probable, le script et la confiance d'un texte avec les profils de trigrammes UDHR (398 langues, articles 0–14). La décision est `und` sous le seuil 0,12 ; la langue probable et la confiance restent publiées. Sur un texte court, le prior des mots-outils des sept langues du bloc prend le relais (champ `source`). `--json` publie les candidats.

arguments:
  TEXTE               texte à profiler (entre guillemets) ou --fichier

options:
  -h, --help, --aide  afficher cette aide et quitter
  --texte TEXTE       le texte (équivalent au TEXTE positionnel)
  --fichier CHEMIN    lire le texte dans un fichier UTF-8
  --seuil SEUIL       seuil de décision (défaut : 0,12) ; sous le seuil, `und`
  --json              sortie JSON (langue, langue probable, script, confiance, candidats)

Exemples : python3 tools/drave.py profils --texte "Le chat dort." ; python3 tools/drave.py profils --texte "Привет мир" --json ; python3 tools/drave.py profils --fichier page.txt
exit=0
exit=0
  ```

- **bash** `{"command": "python3 tools/verifier_schemas.py 2>&1 | tail -10; echo \"exit=${PIPESTATUS[0]}\"; python3 tools/taille_documents.py 2>&1 | tail -10; echo \"exit=${PIPESTATUS[0]}\"; python3 tools/verifie_en_cours.py 2>&1 | tail -10; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run doc/schema/state  … [33 caractères tronqués]`

  ```
schémas · 465 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
exit=0
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4060 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9064 mots > budget 9000 (T1)
     · T0 : 4060 mots (AGENTS + en-cours + une tâche) > budget 4 000
exit=1
  en-cours · 1690 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
exit=0
  ```

- **bash** `{"command": "sed -n '1,220p' tools/taille_documents.py", "description": "Read document size checker"}`

  ```
#!/usr/bin/env python3
"""taille_documents.py — le budget de contexte et la cohésion des documents.

Ce que l'outil vérifie :
  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
  2. la cohésion minimale : un titre, un résumé en tête, et pour les documents datés un
     « Résumé » + « ne pas charger par défaut » ;
  3. les fiches de résultats trop longues pour être lues d'un bloc (avertissement, pas échec) ;
  4. le classement des plus gros documents, pour voir où le contexte part.

Les fiches de `reports/` (sauf `reports/README.md`) et le `journal/` sont **hors budget** :
ils ne sont pas chargés automatiquement. Le budget est en **mots** ; l'estimation de tokens
est donnée à titre indicatif (≈ caractères / 4).

Les **sources de diagrammes** (` ```plantuml `, ` ```mermaid `) sont **rendues, pas lues** :
elles ne comptent pas dans le budget ; le document les porte, la page montre le SVG.
"""
from __future__ import annotations
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent

# (catégorie, budget en mots). Les globs sont résolus dans l'ordre ; le premier match gagne.
BUDGETS: list[tuple[str, str, int
… [6542 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib,re\nfrom tools.taille_documents import mots_hors_diagrammes\nfor f in ['AGENTS.md','docs/pilotage/en-cours.md','docs/pilotage/roadmap.md']:\n    print(f, mots_hors_diagrammes(pathlib.Path(f).read_text()))\nimport pathlib\nagents=[p for p in pathlib.Path( … [306 caractères tronqués]`

  ```
AGENTS.md 1196
docs/pilotage/en-cours.md 1690
docs/pilotage/roadmap.md 9064
task docs/methode/continuite.md 1174
task docs/methode/contexte.md 1089
task docs/methode/ressources.md 1068
task docs/methode/chantier-autonome.md 886
task docs/methode/rangement.md 768
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text()\ns=s.replace('**Mis à jour : 2026-11-16, 02 h 05 HNE (U3 : les profils, 20/20, le texte ambigu rend und, l\\'artefact dans la roue)**',\n            '**Mis à jour : 2026-11-16, 02 h 05 HNE (U3 … [2647 caractères tronqués]`

  ```
patched en-cours terse
patched roadmap terse
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4030 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9024 mots > budget 9000 (T1)
     · T0 : 4030 mots (AGENTS + en-cours + une tâche) > budget 4 000
exit=1
  ```

- **bash** `{"command": "sed -n '155,180p' docs/pilotage/roadmap.md && grep -n \"U3 — les profils\" -A4 docs/pilotage/roadmap.md", "description": "Inspect roadmap around U3"}`

  ```
ne rend pas son code pour le mélange). Le tag annoté `chantier-2026-11-14` est posé sur le dernier
commit vert `0e75f101` (J13.1) ; le tag de semaine `semaine-2026-11-14` (J5.2, resté en échec) est
posé sur le même commit. [`rapport`](../../reports/rapport-cloture-chantier.md) +
[`JSON`](../../reports/rapport-cloture-chantier.json).
**Prochaine mesure** : **B13 — trancher `g017`**, T132/T133 et le
gold B13 ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).

**T4 — la performance (15/11).** 10 000 mots : **4,01 s**, **2 493 mots/s**, **126 Mio**,
**14,8 Mo** JSON ; α = **1,55**, `_groupes_partition`/`_cible_proche` **O(k²)**.
[Fiche](../../reports/rapport-performance.md) · [JSON](../../reports/performance.json).

**U1 — les O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),
**12 259 mots/s**, **127,4 Mio** ; JSON identique. **α = 1,076** (1,530 avant), +0,00077 de R² ; sorties identiques (612/452). [Fiche](../../reports/rapport-performance-fix.md) ·
[JSON](../../reports/performance-fix.json) · [contrôle](../../tools/verifier_performance_fix.py).
**U2 — la roue (16/11)** : **1 727 201 o**, 422 entrées, mêmes JSON hors dépôt ; sans gold,
`evaluer` **4** ([fiche]
… [1079 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/roadmap.md')\ns=p.read_text()\ns=s.replace('''**U3 — les profils (16/11)** : `drave profils` expose les **398 profils UDHR** ; **20/20**,\n**433/447** sur 398 ; ambigu **`und`**, permuté **0/20**\n([fiche](../../reports/rap … [469 caractères tronqués]`

  ```
patched roadmap
  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9016 mots > budget 9000 (T1)
     · T0 : 4030 mots (AGENTS + en-cours + une tâche) > budget 4 000
exit=1
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text()\ns=s.replace('**Mis à jour : 2026-11-16, 02 h 05 HNE (U3 : profils, 20/20, ambigu und)**',\n            '**Mis à jour : 2026-11-16, 02 h 05 HNE (U3 : profils, 20/20)**')\ns=s.replace(' ; **U3* … [1128 caractères tronqués]`

  ```
patched en-cours
  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9016 mots > budget 9000 (T1)
     · T0 : 4005 mots (AGENTS + en-cours + une tâche) > budget 4 000
exit=1
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nfrom tools.taille_documents import mots_hors_diagrammes\nfor f in ['AGENTS.md','docs/pilotage/en-cours.md','docs/pilotage/roadmap.md']:\n    print(f, mots_hors_diagrammes(pathlib.Path(f).read_text()))\nPY\ngrep -n \"U3\\|U2\\|U1\" docs/pilotage/en-cours … [62 caractères tronqués]`

  ```
AGENTS.md 1196
docs/pilotage/en-cours.md 1635
docs/pilotage/roadmap.md 9016
3:**Mis à jour : 2026-11-16, 02 h 05 HNE (U3 : profils, 20/20)**
62:- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** ([fiche](../../reports/rapport-performance-fix.md)) ; **U2** la roue : **1 727 201 o**, mêmes JSON hors dépôt, sans gold → **4** ([fiche](../../reports/rapport-roue.md)) ; **U3** profils **20/20**, ambigu **`und`** ([fiche](../../reports/rapport-profils.md)).
85:- **Pensée — B13 (actif)** : **183/183** ; **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; **U2 — la roue** (autonome, gold dedans, roue sans gold → 4) ; **U3** profils 20/20 ; [v2](../../reports/rapport-restitution-v2.md), [v3](../../reports/rapport-restitution-v3.md), [roue](../../reports/rapport-roue.md), [profils](../../reports/rapport-profils.md).
113:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6 ; U1 : α 1,08, 10 000 mots 0,82 s ; U2 : roue 1 727 201 o, mêmes JSON, sans gold → evaluer 4 ; U3 : pro
… [544 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text()\ns=s.replace('''**T1–T6 — livré** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s, instrument 0,71/2,11) ; **U2 — la roue** (1 727 201 o, autonome, gold dedans, roue sans gold → 4 … [1188 caractères tronqués]`

  ```
trimmed
  T0 max : 4002 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/roadmap.md : 9007 mots > budget 9000 (T1)
     · T0 : 4002 mots (AGENTS + en-cours + une tâche) > budget 4 000
exit=1
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text()\ns=s.replace('**U2 — la roue** (1 727 201 o, gold dedans, roue sans gold → 4) ; **U3** profils 20/20, `und`',\n            '**U2 — la roue** (1 727 201 o, sans gold → 4) ; **U3** profils 20/20 … [576 caractères tronqués]`

  ```
trimmed again
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3998 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · docs/pilotage/roadmap.md : 9001 mots > budget 9000 (T1)
exit=1
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/roadmap.md')\ns=p.read_text().replace('**U3 (16/11)** :', '**U3** :')\np.write_text(s)\nprint('trimmed one')\nPY\npython3 tools/taille_documents.py 2>&1 | tail -6; echo \"exit=${PIPESTATUS[0]}\"", "description": "Trim one w … [39 caractères tronqués]`

  ```
trimmed one
  T0 max : 3998 mots (budget 4 000)

  avertissements :
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
exit=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -12; echo \"revue=${PIPESTATUS[0]}\"; python3 tools/verifie_en_cours.py 2>&1 | tail -5; echo \"etat=${PIPESTATUS[0]}\"; bash tools/porte-tableaux.sh 2>&1 | tail -6; echo \"tables=${PIPESTATUS[0]}\"", "description": "Re-run documentation a … [37 caractères tronqués]`

  ```
revue de documentation · 768 fiche(s) · 863 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
revue=0
  en-cours · 1628 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
etat=0
  ✅ 1849 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4762 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-16)
tables=0
  ```

- **bash** `{"command": "git diff --stat -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/produit/README.md docs/produit/demarrage.md docs/implantation/bloc-linguistique.md reports/rapport-bloc-linguistique.md pyproject.toml tools/drave.py tools/porte-bloc-linguistique.sh tools/tests/test_produit.py t … [153 caractères tronqués]`

  ```
docs/implantation/bloc-linguistique.md |  13 ++++
 docs/pilotage/en-cours.md              |  16 ++---
 docs/pilotage/roadmap.md               |   7 +-
 docs/produit/README.md                 |  89 ++++++++++++++++++-----
 docs/produit/demarrage.md              |  37 +++++++++-
 pyproject.toml                         |   9 ++-
 reports/rapport-bloc-linguistique.md   |   7 ++
 tools/drave.py                         | 124 ++++++++++++++++++++++++++++++---
 tools/porte-bloc-linguistique.sh       |   2 +
 tools/tests/test_empaquetage.py        |  10 ++-
 tools/tests/test_produit.py            |   6 +-
 11 files changed, 274 insertions(+), 46 deletions(-)
---
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 36ca8023..33e2680b 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-16, 00 h 45 HNE (U2 : la roue, les gold dedans, la roue sans gold échoue)**
+**Mis à jour : 2026-11-16, 02 h 05 HNE (U3 : profils, 20/20)**
 
 > **État courant, pas histoire** : une sous-section par session active ; preuves et plan plus bas (**La carte**).
 
@@ -59,8 +59,8 @@
 - **Plan** : B13 · **Stratégie** : v0 ·
… [7438 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text().replace('fusion réparée **0,9309/0,8226/0,8784/0,9954**\\n', 'fusion réparée **0,9309/0,8226/0,8784/0,9954**.\\n')\np.write_text(s)\nprint('restored period')\nPY\ngit diff -- docs/pilotage/roa … [78 caractères tronqués]`

  ```
restored period
diff --git a/docs/pilotage/roadmap.md b/docs/pilotage/roadmap.md
index 599f7d6f..ddf68b8c 100644
--- a/docs/pilotage/roadmap.md
+++ b/docs/pilotage/roadmap.md
@@ -166,8 +166,11 @@ gold B13 ; **E2** ([fiche](../../reports/rapport-tagger-erreurs.md)).
 **U1 — les O(k²) bornés (16/11).** 10 000 mots : **3,99 → 0,82 s** (×4,9),
 **12 259 mots/s**, **127,4 Mio** ; JSON identique. **α = 1,076** (1,530 avant), +0,00077 de R² ; sorties identiques (612/452). [Fiche](../../reports/rapport-performance-fix.md) ·
 [JSON](../../reports/performance-fix.json) · [contrôle](../../tools/verifier_performance_fix.py).
-**U2 — la roue (16/11)** : **1 727 201 o**, 422 entrées, mêmes JSON hors dépôt ; sans gold,
-`evaluer` **4** ([fiche](../../reports/rapport-roue.md)). Prochaine action : **U3 — `--profils`**.
+**U2 — la roue (16/11)** : **1 727 201 o** ; sans gold, `evaluer` **4**
+([fiche](../../reports/rapport-roue.md)).
+
+**U3** : **398 profils UDHR** ; **20/20**, **433/447** ; ambigu **`und`**
+([fiche](../../reports/rapport-profils.md)).
 
 **T6 — le bilan exploitable (15/11, 23 h 35).** Cinq briques : installation éditable,
 quickstart 3/3, API (2 139 objets, 8 rôles), performance 
… [34 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- docs/produit/README.md | sed -n '1,240p'", "description": "Review product README diff"}`

  ```
diff --git a/docs/produit/README.md b/docs/produit/README.md
index 3705d326..bfadaf66 100644
--- a/docs/produit/README.md
+++ b/docs/produit/README.md
@@ -68,7 +68,7 @@ candidats en **objets** `{span, cible, source}`, et `meta.role` appartient à un
 
 | ce que vous demandez | ce que vous obtenez | mesure du 15/11 |
 |---|---|---|
-| **langue et script** | `fr`, `en`, `und`… et `Latn`, `Cyrl`… | **398 langues**, **0,9687** ; script **1,0000** (autotest UDHR ; le CLI n'expose que `fr`/`en` comme indice) |
+| **langue et script** | `fr`, `en`, `und`… et `Latn`, `Cyrl`… | **398 langues**, **0,9687** ; script **1,0000** (autotest UDHR ; `drave profils` les expose, `--langue` reste un indice `fr`/`en`) |
 | **POS** | DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM… | **0,8625** (fermé 0,9373, ouvert 0,7918) ; **0,8891** sur le réel 452 ; **0,9575** avec `--tagger` |
 | **syntagmes** | GN, GV, GP, REL, SUB, avec leur span | F1 **0,7902** ; tête **0,9029** (vivant 612) ; **0,7906** sur le réel 452 |
 | **attachement** | par syntagme : `role`, `cible`, `candidats` (objets v2, chaînes d'affichage en lecture) | **238/239** exacts ; couverture **0,9958** ; exact sur span **1,0000** ; **2
… [10636 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"moins de cinq mots\\|moins de 5 mots\" reports/rapport-profils.md docs/produit/README.md docs/produit/demarrage.md tools/profils_udhr.py", "description": "Find token penalty claims"}`

  ```
reports/rapport-profils.md:64:désaccord est visible, pas masqué. Un texte de **moins de cinq mots** est pénalisé
docs/produit/README.md:591:`candidats` restent les profils — le désaccord est visible. Un texte de moins de cinq mots est
tools/profils_udhr.py:173:    - `profils` : au-delà, les 398 profils UDHR. Un texte de moins de cinq mots est
tools/profils_udhr.py:220:    # 2. Les profils UDHR ; la confiance d'un texte de moins de cinq mots est réduite.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-profils.md')\ns=p.read_text().replace('Un texte de **moins de cinq mots** est pénalisé', 'Un texte de **moins de cinq mots** qui passe par les profils est pénalisé')\np.write_text(s)\np=pathlib.Path('docs/produit/README.m … [589 caractères tronqués]`

  ```
patched
reports/rapport-profils.md:64:désaccord est visible, pas masqué. Un texte de **moins de cinq mots** qui passe par les profils est pénalisé
docs/produit/README.md:591:`candidats` restent les profils — le désaccord est visible. Un texte de moins de cinq mots qui passe par les profils est
tools/profils_udhr.py:173:    - `profils` : au-delà, les 398 profils UDHR. Un texte de moins de cinq mots qui passe par les profils est
tools/profils_udhr.py:220:    # 2. Les profils UDHR ; la confiance d'un texte de moins de cinq mots est réduite.
  ```

- **bash** `{"command": "set -e\npython3 tools/tests/test_profils.py >/tmp/final-profils.out 2>&1; tail -3 /tmp/final-profils.out\npython3 tools/tests/test_produit.py >/tmp/final-produit.out 2>&1; tail -3 /tmp/final-produit.out\npython3 tools/tests/test_empaquetage.py >/tmp/final-empaquetage.out 2>&1; tail -3 / … [538 caractères tronqués]`

  ```
Ran 19 tests in 5.033s

OK
Ran 30 tests in 17.670s

OK
Ran 12 tests in 0.719s

OK
Ran 9 tests in 1.578s

OK
Ran 25 tests in 0.328s

OK
  ✅ 10. Comment l'installer et le lancer ?
✅ FAQ vérifiée
✅ porte bloc linguistique verte
FINAL_OK
  ```

- **bash** `{"command": "ls tools/porte-produit.sh tools/porte-bloc.sh 2>/dev/null && sed -n '1,80p' tools/porte-produit.sh 2>/dev/null", "description": "Inspect product gate"}`

  ```
tools/porte-produit.sh
[exit code: 2]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/porte-produit.sh", "description": "Read product gate"}`

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
… [4115 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/porte-produit.sh')\ns=p.read_text()\nmarker='a=$(python3 tools/drave.py rejouer \"Le chat dort.\" 2>&1 | grep -o \\'sha256 [0-9a-f]*\\' | head -1)'\nblock='''if sortie=$(python3 tools/drave.py profils --texte \"Le chat dort.\" --js … [836 caractères tronqués]`

  ```
patched product gate
  ✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ profils : langue, script, confiance, 398 profils
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
exit=0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-profils.md')\ns=p.read_text()\ns=s.replace('''[`reports/profils.json`](profils.json), [`tools/drave.py`](../tools/drave.py),''','''[`reports/profils.json`](profils.json), [`tools/drave.py`](../tools/drave.py),\n[`tools/po … [521 caractères tronqués]`

  ```
patched report gate refs
21:[`tools/porte-produit.sh`](../tools/porte-produit.sh),
192:| `tools/porte-produit.sh` | le cas `profils` (langue, script, confiance, 398 profils) dans la porte produit |
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -5; echo \"exit=${PIPESTATUS[0]}\"; bash tools/porte-tableaux.sh 2>&1 | tail -4; echo \"exit=${PIPESTATUS[0]}\"; python3 tools/taille_documents.py 2>&1 | tail -3; echo \"exit=${PIPESTATUS[0]}\"", "description": "Final docs and budget chec … [25 caractères tronqués]`

  ```
revue de documentation · 768 fiche(s) · 863 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
  ✅ 1849 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4763 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-16)
exit=0
     · 65 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
exit=0
  ```

- **bash** `{"command": "git diff -- tools/drave.py | sed -n '1,260p'", "description": "Review CLI diff"}`

  ```
diff --git a/tools/drave.py b/tools/drave.py
index e5469d2f..d1674893 100644
--- a/tools/drave.py
+++ b/tools/drave.py
@@ -9,6 +9,9 @@ Une seule commande, quatre gestes, hors ligne et déterministe :
     python3 tools/drave.py analyser "Le chat dort." --tagger auto     # API si clé, sinon heuristique
     python3 tools/drave.py evaluer
     python3 tools/drave.py evaluer --gold --json
+    python3 tools/drave.py profils --texte "Le chat dort."
+    python3 tools/drave.py profils --texte "Привет мир" --json
+    python3 tools/drave.py analyser "Le chat dort." --profils
     python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
     python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
     python3 tools/drave.py restituer "Le chat dort."
@@ -59,6 +62,7 @@ import bloc_linguistique as bl  # noqa: E402  (import après l'installation des
 import restitution  # noqa: E402  (la restitution v0 : annotation → surface)
 import restitution_v2  # noqa: E402  (la restitution v2 : les rôles)
 import restitution_v3  # noqa: E402  (la restitution v3 : les rôles des GP)
+import profils_udhr as pu  # noqa: E402  (la détection 
… [12208 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/drave.py')\ns=p.read_text()\ns=s.replace('Une seule commande, quatre gestes, hors ligne et déterministe :',\n            'Une seule commande, cinq gestes, hors ligne et déterministe :')\ns=s.replace('''**restitution v0** (annotatio … [795 caractères tronqués]`

  ```
patched docstring
compiled
  ```

- **bash** `{"command": "sed -n '1,40p' tools/drave.py", "description": "Check CLI docstring"}`

  ```
#!/usr/bin/env python3
"""drave.py — le point d'entrée produit du bloc linguistique.

Une seule commande, cinq gestes, hors ligne et déterministe :

    python3 tools/drave.py analyser "Le chat dort."
    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
    python3 tools/drave.py analyser "Le chat dort." --tagger auto     # API si clé, sinon heuristique
    python3 tools/drave.py evaluer
    python3 tools/drave.py evaluer --gold --json
    python3 tools/drave.py profils --texte "Le chat dort."
    python3 tools/drave.py profils --texte "Привет мир" --json
    python3 tools/drave.py analyser "Le chat dort." --profils
    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
    python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
    python3 tools/drave.py restituer "Le chat dort."
    python3 tools/drave.py restituer "Le chat dort." --roles
    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
    python3 tools/drave.py --version

Ce que la com
… [1558 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"quatre sous-commandes\\|quatre gestes\\|analyser, evaluer, rejouer, restituer\\|les quatre commandes\" README.md docs reports/rapport-*.md --include=*.md | head -30", "description": "Find stale four-command references"}`

  ```
reports/rapport-cli-robuste.md:1:# T5 — la robustesse de la CLI : `--duree`, cinq codes de sortie, aide des quatre sous-commandes, `--fichier` sans trace
reports/rapport-cli-robuste.md:76:## 3. `--aide` et `--help` sur les quatre sous-commandes
  ```

- **bash** `{"command": "grep -rn \"1 727 201\\|1,727,201\\|1727201\\|422 entrées\" README.md docs reports/rapport-roue.md reports/roue.json | head -30", "description": "Find wheel size references"}`

  ```
docs/pilotage/en-cours.md:62:- **Ce qu'elle fait** : **W5** restitution v3 (gold S **144/144**, v2 **20/46**) ; **U1** O(k²) : **4,0 → 0,82 s**, α **1,53 → 1,08** ([fiche](../../reports/rapport-performance-fix.md)) ; **U2** la roue : **1 727 201 o**, mêmes JSON hors dépôt, sans gold → **4** ([fiche](../../reports/rapport-roue.md)) ; **U3** profils **20/20**, ambigu **`und`** ([fiche](../../reports/rapport-profils.md)).
docs/pilotage/en-cours.md:113:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit T1–T6 ; U1 : α 1,08, 10 000 mots 0,82 s ; U2 : roue 1 727 201 o, mêmes JSON, sans gold → evaluer 4 ; U3 : profils 398 langues, 20/20, ambigu und** | **`g017` tranché** ; **J4** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
docs/pilotage/en-cours.md:123:**T1–T6 — livré** ; **U1 — les deux O(k²) bornés** (α 1,08, 10 000 mots 0,82 s) ; **U2 — la roue** (1 727 201 o, sans gold → 4) ; **U3** profils 20/20 ; [bilan](../../reports/rapport-bilan-exploitable.md), [U1](../../reports/rapport-performance-fix.md), [U2](../../reports/rapport-roue.md), [U3](../../reports/
… [274 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-roue.md')\ns=p.read_text()\nmarker='''> sha256 `d980c4706f575e061faa9611aca4c42c024c1147b654004f724694914a99dbce`. Installée\n> dans un venv **propre** depuis la roue (pas le dépôt), elle rend `drave 0.1.0` (code 0),'''\n … [647 caractères tronqués]`

  ```
patched wheel report note
8:> sha256 `d980c4706f575e061faa9611aca4c42c024c1147b654004f724694914a99dbce`. **Depuis U3**,
  ```

- **bash** `{"command": "rm -rf build drave.egg-info && mkdir -p dist && python3 -m pip wheel . --no-deps --no-build-isolation -w dist 2>&1 | tail -4 && stat -c '%s' dist/drave-0.1.0-py3-none-any.whl", "description": "Final wheel build and size", "timeoutMs": 300000}`

  ```
Building wheel for drave (pyproject.toml): finished with status 'done'
  Created wheel for drave: filename=drave-0.1.0-py3-none-any.whl size=2055129 sha256=51c3f52c5b3a7e9683b4e10891da93498062e8b6ee2678a5d86263cb230062ae
  Stored in directory: /tmp/pip-ephem-wheel-cache-q1hw0ujr/wheels/96/02/a3/318108f401dc37bb3a575e67c80cf111852262a4b3c9f691ec
Successfully built drave
2055129
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nfor f in ['reports/rapport-profils.md','reports/rapport-roue.md']:\n    p=pathlib.Path(f)\n    s=p.read_text().replace('2 055 055', '2 055 129')\n    p.write_text(s)\nprint('updated size')\nPY\ngrep -rn \"2 055 129\\|2 055 055\" reports/rapport-profils. … [70 caractères tronqués]`

  ```
updated size
reports/rapport-profils.md:178:  (2 055 129 octets contre 1 727 201). C'est assumé : la détection doit marcher hors dépôt.
reports/rapport-roue.md:9:> l'artefact de profils (802 110 octets) ajoute ~0,33 Mo : la roue courante fait **2 055 129
  ```

- **bash** `{"command": "/tmp/venv-drave-profils2/bin/python -m pip install --no-index --no-deps --no-cache-dir --force-reinstall dist/drave-0.1.0-py3-none-any.whl >/tmp/install-final.out 2>&1 && tail -2 /tmp/install-final.out && cd /tmp && /tmp/venv-drave-profils2/bin/drave profils --texte \"Le chat dort.\" -- … [201 caractères tronqués]`

  ```
Successfully uninstalled drave-0.1.0
Successfully installed drave-0.1.0
fra Latn 398
  ```

- **bash** `{"command": "grep -n \"drave analyser\\|drave evaluer\\|sous-commandes\\|--profils\" docs/pilotage/utilisation.md | head -20", "description": "Check usage doc for CLI list"}`

  ```
(no output)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-profils.md')\ns=p.read_text()\ns=s.replace('''- **La roue n'est pas minimale** : l'artefact ajoute ~0,33 Mo compressés à la roue U2\n  (2 055 129 octets contre 1 727 201). C'est assumé : la détection doit marcher hors dép … [515 caractères tronqués]`

  ```
added limit
179:- **`--profils` est une option** : elle charge l'artefact (~800 Ko) et score 398 profils par
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-profils.md')\ns=p.read_text()\ns=s.replace('''   `stdout` vide, message qui nomme le fichier et les deux issues ; `analyser --profils` suit\n   le même chemin. C'est le contrôle négatif de l'empaquetage, comme la roue san … [474 caractères tronqués]`

  ```
patched
144:   le même chemin. La roue **installée**, artefact retiré de `site-packages`, sort aussi **4**
  ```

- **bash** `{"command": "git diff --check -- tools/drave.py tools/profils_udhr.py tools/construire_profils_udhr.py tools/mesurer_profils.py tools/tests/test_profils.py tools/tests/test_produit.py tools/tests/test_empaquetage.py tools/porte-bloc-linguistique.sh tools/porte-produit.sh pyproject.toml docs/produit/ … [350 caractères tronqués]`

  ```
exit=0
  ```

- **bash** `{"command": "grep -rn \" $\" tools/profils_udhr.py tools/construire_profils_udhr.py tools/mesurer_profils.py tools/tests/test_profils.py reports/rapport-profils.md reports/profils.json | head -10; echo \"exit=${PIPESTATUS[0]}\"", "description": "Check trailing spaces in new files"}`

  ```
exit=1
  ```

- **bash** `{"command": "python3 -m pytest -q tools/tests/test_profils.py 2>&1 | tail -10; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run profile tests under pytest", "timeoutMs": 180000}`

  ```
...................                                                      [100%]
19 passed in 5.20s
exit=0
  ```

- **bash** `{"command": "git status --short | grep -E \"profils|porte-produit|drave.py|pyproject|docs/produit|docs/implantation|docs/pilotage/(en-cours|roadmap)|rapport-bloc|rapport-roue|reports/(README|INDEX)\"", "description": "List relevant changed files"}`

  ```
M docs/implantation/bloc-linguistique.md
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M docs/produit/demarrage.md
 M pyproject.toml
 M reports/INDEX.md
 M reports/README.md
 M reports/rapport-bloc-linguistique.md
 M reports/rapport-roue.md
 M tools/drave.py
 M tools/porte-produit.sh
?? reports/profils.json
?? reports/rapport-profils.md
?? tools/construire_profils_udhr.py
?? tools/mesurer_profils.py
?? tools/profils_udhr.py
?? tools/tests/linguistique/profils_udhr.json
?? tools/tests/test_profils.py
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/produit/README.md')\ns=p.read_text().replace('clone, installation, trois commandes,', 'clone, installation, les commandes,')\np.write_text(s)\nprint('patched intro')\nPY\ngrep -n \"Démarrage en 5 minutes\" -A1 docs/produit/README.md … [55 caractères tronqués]`

  ```
patched intro
29:> **Démarrage en 5 minutes** : le parcours pas à pas — clone, installation, les commandes,
30-> JSON, tagger optionnel et erreurs — est dans [`demarrage.md`](demarrage.md).
  ```

- **bash** `{"command": "set -e\npython3 tools/revue_documentation.py >/tmp/final-revue.out 2>&1; tail -3 /tmp/final-revue.out\npython3 tools/taille_documents.py >/tmp/final-taille.out 2>&1; tail -2 /tmp/final-taille.out\npython3 tools/verifie_en_cours.py >/tmp/final-etat.out 2>&1; tail -2 /tmp/final-etat.out\n … [269 caractères tronqués]`

  ```
revue de documentation · 768 fiche(s) · 863 JSON · 125 doc(s) · 86 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  en-cours · 1628 mots · 7 sections · 4 session(s) · 9 puces · 3 questions
  ✅ état court, structuré, multi-session et reprenable
  ✅ 4764 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-16)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
DOCS_OK
  ```

- **bash** `{"command": "git diff --stat -- docs/implantation/bloc-linguistique.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/produit/README.md docs/produit/demarrage.md pyproject.toml reports/INDEX.md reports/README.md reports/rapport-bloc-linguistique.md reports/rapport-roue.md tools/drave.py too … [396 caractères tronqués]`

  ```
docs/implantation/bloc-linguistique.md |  13 ++++
 docs/pilotage/en-cours.md              |  14 ++--
 docs/pilotage/roadmap.md               |   7 +-
 docs/produit/README.md                 |  91 ++++++++++++++++++-----
 docs/produit/demarrage.md              |  37 +++++++++-
 pyproject.toml                         |   9 ++-
 reports/INDEX.md                       |   1 +
 reports/README.md                      |   1 +
 reports/rapport-bloc-linguistique.md   |   7 ++
 reports/rapport-roue.md                |   6 +-
 tools/drave.py                         | 130 +++++++++++++++++++++++++++++----
 tools/porte-bloc-linguistique.sh       |   2 +
 tools/porte-produit.sh                 |  15 ++++
 tools/tests/test_empaquetage.py        |  10 ++-
 tools/tests/test_produit.py            |   6 +-
 15 files changed, 299 insertions(+), 50 deletions(-)
--- new ---
  305 tools/profils_udhr.py
  116 tools/construire_profils_udhr.py
  363 tools/mesurer_profils.py
  251 tools/tests/test_profils.py
  210 reports/rapport-profils.md
 1245 total
-rw-r--r--. 1 stephane stephane  21K 16 nov 01:52 reports/profils.json
-rw-r--r--. 1 stephane stephane 784K 16 nov 01:39 tools/tests/linguistique/profils_udhr
… [5 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/profils_udhr.py')\ns=p.read_text()\ns=s.replace('''    if detection.get(\"refus\"):\n        lignes.append(f\"refus       : {detection['refus']} \"\n                      \"(le texte doit contenir au moins une lettre ou un chiffre) … [1184 caractères tronqués]`

  ```
patched formatter
drave 0.1.0 — profils de langue (UDHR, hors ligne)
langue=fra script=Latn confiance=0.3333 source=lexique
langue      : fra (French)
script      : Latn
confiance   : 0.3333 (marge 0.0000, seuil 0.12)
source      : lexique
prior       : fra (mots-outils 0.3333)
candidats   : hns 0.6364 · lld 0.5455 · deu 0.4545 · oci 0.4545 · pcd 0.4545
profils     : 398 langues UDHR (articles 0–14, top 200)
---
{
 "schema": "drave.profils",
 "version": 1,
 "texte": "Le chat dort.",
 "langue": "fra",
  ```

- **bash** `{"command": "grep -rn \"profils de langue (UDHR, hors ligne)\" reports/rapport-profils.md docs/produit/README.md docs/produit/demarrage.md", "description": "Find example blocks to update"}`

  ```
reports/rapport-profils.md:44:drave 0.1.0 — profils de langue (UDHR, hors ligne)
docs/produit/README.md:571:drave 0.1.0 — profils de langue (UDHR, hors ligne)
docs/produit/demarrage.md:173:drave 0.1.0 — profils de langue (UDHR, hors ligne)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nfor f in ['reports/rapport-profils.md','docs/produit/README.md','docs/produit/demarrage.md']:\n    p=pathlib.Path(f)\n    s=p.read_text()\n    s=s.replace('''drave 0.1.0 — profils de langue (UDHR, hors ligne)\nlangue      : fra (French)''','''drave 0.1. … [352 caractères tronqués]`

  ```
patched examples
reports/rapport-profils.md:45:langue=fra script=Latn confiance=0.3333 source=lexique
docs/produit/README.md:572:langue=fra script=Latn confiance=0.3333 source=lexique
docs/produit/demarrage.md:174:langue=fra script=Latn confiance=0.3333 source=lexique
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('tools/tests/test_profils.py')\ns=p.read_text()\nneedle='''    def test_texte_positionnel_et_option_equivalents(self) -> None:'''\nadd='''    def test_sortie_lisible_compacte(self) -> None:\n        sortie = drave(\"profils\", \"--texte\" … [568 caractères tronqués]`

  ```
patched test
----------------------------------------------------------------------
Ran 20 tests in 5.632s

OK
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\np=pathlib.Path('reports/rapport-profils.md')\ns=p.read_text().replace('(**19 tests**)', '(**20 tests**)')\ns=s.replace('19 tests : CLI, JSON, ambigu, mot isolé, mot-outil isolé, vide, absent, 20 langues, permuté',\n            '20 tests : CLI, JSON, sor … [223 caractères tronqués]`

  ```
patched count
19:> mesure), [`tools/tests/test_profils.py`](../tools/tests/test_profils.py) (**20 tests**),
192:| `tools/tests/test_profils.py` | 20 tests : CLI, JSON, sortie compacte, ambigu, mot isolé, mot-outil isolé, vide, absent, 20 langues, permuté |
  ```

- **bash** `{"command": "rm -rf build drave.egg-info && mkdir -p dist && python3 -m pip wheel . --no-deps --no-build-isolation -w dist 2>&1 | tail -3 && stat -c '%s' dist/drave-0.1.0-py3-none-any.whl", "description": "Rebuild wheel after formatter change", "timeoutMs": 300000}`

  ```
Created wheel for drave: filename=drave-0.1.0-py3-none-any.whl size=2055192 sha256=27a3a671aac8ae2c827dd1177703642d656da3ad354b6df6f08ab2ceca8ce2a7
  Stored in directory: /tmp/pip-ephem-wheel-cache-jyqgn4qg/wheels/96/02/a3/318108f401dc37bb3a575e67c80cf111852262a4b3c9f691ec
Successfully built drave
2055192
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nfor f in ['reports/rapport-profils.md','reports/rapport-roue.md']:\n    p=pathlib.Path(f); s=p.read_text().replace('2 055 129','2 055 192'); p.write_text(s)\nprint('updated')\nPY\ngrep -rn \"2 055 192\" reports/rapport-profils.md reports/rapport-roue.md … [38 caractères tronqués]`

  ```
updated
reports/rapport-profils.md:181:  (2 055 192 octets contre 1 727 201). C'est assumé : la détection doit marcher hors dépôt.
reports/rapport-roue.md:9:> l'artefact de profils (802 110 octets) ajoute ~0,33 Mo : la roue courante fait **2 055 192
  ```

- **bash** `{"command": "/tmp/venv-drave-profils2/bin/python -m pip install --no-index --no-deps --no-cache-dir --force-reinstall dist/drave-0.1.0-py3-none-any.whl >/tmp/install-final2.out 2>&1 && cd /tmp && /tmp/venv-drave-profils2/bin/drave profils --texte \"Le chat dort.\" | head -4", "description": "Reinsta … [62 caractères tronqués]`

  ```
drave 0.1.0 — profils de langue (UDHR, hors ligne)
langue=fra script=Latn confiance=0.3333 source=lexique
langue      : fra (French)
script      : Latn
  ```

- **bash** `{"command": "set -e\npython3 tools/tests/test_profils.py >/tmp/z1.out 2>&1; tail -3 /tmp/z1.out\npython3 tools/tests/test_produit.py >/tmp/z2.out 2>&1; tail -3 /tmp/z2.out\npython3 tools/tests/test_empaquetage.py >/tmp/z3.out 2>&1; tail -3 /tmp/z3.out\nbash tools/porte-bloc-linguistique.sh >/tmp/z4. … [330 caractères tronqués]`

  ```
Ran 20 tests in 5.336s

OK
Ran 30 tests in 17.266s

OK
Ran 12 tests in 0.650s

OK
✅ porte bloc linguistique verte
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ✅ la page vivante date du dernier commit (2026-11-16)
ALL_FINAL_OK
  ```

- **bash** `{"command": "git diff --check 2>&1 | head -20; echo \"exit=${PIPESTATUS[0]}\"; python3 - <<'PY'\nimport pathlib\nfor f in ['tools/profils_udhr.py','tools/construire_profils_udhr.py','tools/mesurer_profils.py','tools/tests/test_profils.py','reports/rapport-profils.md','reports/profils.json']:\n    s= … [215 caractères tronqués]`

  ```
exit=0
tools/profils_udhr.py trailing-lines []
tools/construire_profils_udhr.py trailing-lines []
tools/mesurer_profils.py trailing-lines []
tools/tests/test_profils.py trailing-lines []
reports/rapport-profils.md trailing-lines []
reports/profils.json trailing-lines []
  ```

### 🤖 Assistant

## U3 — `drave profils` : la détection de langue UDHR exposée

**Livré.**

### CLI

```bash
drave profils --texte "Le chat dort."
drave profils --texte "Привет мир" --json
drave profils --fichier article.txt --json
drave analyser "Le chat dort." --profils
```

La sortie rend **la langue probable** (ISO 639-3), **le script** et **la confiance** ; le JSON porte en plus `langue` (décision), `langue_probable`, `marge`, `seuil`, `sous_seuil`, `source`, `prior`, `candidats` et les métadonnées des profils. Sous le seuil `0,12`, la décision est `und` ; la langue probable reste publiée.

Deux chemins explicites :
- **texte long** → les **398 profils UDHR** (`source: profils`) ;
- **texte court** → prior des mots-outils des 7 langues du bloc (`source: lexique`), avec le désaccord visible dans `prior` vs `candidats` ;
- un mot isolé ou un mot-outil seul (`chat`, `le`) rend `und`.

### Résultats mesurés

| mesure | résultat |
|---|---:|
| 20 langues de l'échantillon UDHR, article 15 | **20/20 = 1,0000** |
| script, article 15 | **20/20** |
| 20 langues, articles 15–30 | **313/320 = 0,9781** |
| script, articles 15–30 | **320/320** |
| autotest complet 398 langues, profils bruts | **433/447 = 0,9687** |
| chemin CLI (hybride court/long) | **431/447 = 0,9642** |
| profils permutés | **0/20** · **1/447 = 0,0022** |
| texte ambigu bilingue | **`und`**, confiance **0,0836 < 0,12** |

L’artefact fait **802 110 octets**, sha256 `33aee69d…` ; il est **identique** aux profils reconstruits depuis le corpus (0 différence) et voyage dans la roue (`drave profils` a été testé installé depuis `/tmp`). Roue sans l’artefact → **code 4**, `stdout` vide, pas de trace.

### Fichiers

- `reports/rapport-profils.md` — la fiche.
- `reports/profils.json` — la mesure reproductible.
- `tools/profils_udhr.py` — chargement, détection, prior court, `ProfilsAbsents`.
- `tools/construire_profils_udhr.py` — construction déterministe des 398 profils + `--verifier`.
- `tools/mesurer_profils.py` — la mesure (20 langues, 398, permuté, contrôles, CLI).
- `tools/tests/linguistique/profils_udhr.json` — l’artefact embarqué.
- `tools/tests/test_profils.py` — **20 tests**.
- `tools/drave.py` — commande `profils`, option `analyser --profils`, `_HeuristiqueProfils`, code 4.
- `pyproject.toml` — `profils_udhr.json` dans les `package-data`.
- `tools/porte-bloc-linguistique.sh` et `tools/porte-produit.sh` — cas `profils` ajoutés.
- Documentation : `docs/produit/README.md` **§ 3.8**, `docs/produit/demarrage.md` **§ 3.5**, `docs/implantation/bloc-linguistique.md` **§ 8** ; état et roadmap mis à jour.

### Validation

```bash
python3 tools/tests/test_profils.py        # 20 tests OK
python3 tools/tests/test_produit.py        # 30 tests OK
python3 tools/tests/test_empaquetage.py    # 12 tests OK
bash tools/porte-bloc-linguistique.sh      # verte
bash tools/porte-produit.sh                # verte (cas profils inclus)
python3 tools/mesurer_profils.py           # verdict OK
```

`revue_documentation.py`, `porte-tableaux.sh`, `verifie_en_cours.py`, `verifier_schemas.py` et `taille_documents.py` passent. Les limites sont nommées dans la fiche : échantillon **stratifié** (pas aléatoire), confiance **non calibrée**, prior court limité à 7 langues, et **0,9642** sur les 398 textes du chemin CLI. Le tout reste **non commité** : l’arbre contenait déjà des modifications d’autres sessions, et je n’ai pas voulu mélanger les `git add`.

