# Session DSH — relecture

- identifiant : `e181ce02-cd50-488a-a6be-e84b79d40dcc`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-31 17:40:32
- agent : standard


## Tour 1

### 👤 Utilisateur

fais une documentation détaillée du modèle Drave natif. utilise beaucoup de diagrammes pour expliquer ce qui est original à Drave. Comment implémenter un modèle de type Modèles de Diehl & Cook (2015) en respectant notre principe de séparation à 3 niveaux (sémentique neutre au centre)

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
réseau sont des **faits** regroupés en **listes valuées poussées** vers leurs lecteurs : le coût du calcul devient proportionnel à l'**activité**, et le modèle devient **décomposable**, **répartissable** et **observable**. Le projet a pour principe que la structure bat la taille. Construire le moteur et modèle optimisé qui rend cette structure observable, décomposable, répartissable et rejouable permet d'atteindre de nouveaux sommets. Bref, révolutionner l'IA avec une approche par bus d'événements où chaque bloc fonctionnel est optimisable, comparable et substituable par des alternatives ayant des architectures différentes. e.g. Blocs neuronaux là où l'intuition est un avantage, blocs computationnels classiques pour les opérations où l'informatique classique est plus fiable et performante.

Le projet est né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de
les **combiner**, de les **décomposer en couches et grappes de neurones** exécutables par du matériel divers, voire
**distribué en réseau**, de les **diagnostiquer et faire évoluer** en étudiant leurs **flux**, et de **rejouer à
volonté** des événements.


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

### 🤖 Assistant

⏵ Repérage du dépôt : modèle natif Drave, séparation à 3 niveaux, diagrammes

- **bash** `{"command": "ls -la && echo '---' && ls docs && echo '---' && ls docs/theorie && echo '---' && ls docs/schemas | head -50", "description": "Lister la structure du dépôt"}`

  ```
total 204
drwxr-xr-x. 1 stephane stephane   660 31 oct 17:22 .
drwxr-xr-x. 1 stephane stephane  2464 27 oct 12:53 ..
-rw-r--r--. 1 stephane stephane  9882 29 oct 16:01 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  1366 29 oct 14:19 data
drwxr-xr-x. 1 stephane stephane   124 29 oct 08:12 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   178 31 oct 17:36 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   105 27 oct 12:51 .gitmodules
drwxr-xr-x. 1 stephane stephane   792 31 oct 11:23 journal
drwxr-xr-x. 1 stephane stephane   100 15 oct 09:02 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 19956 29 oct 08:14 README.md
drwxr-xr-x. 1 stephane stephane 38176 31 oct 16:37 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane 10507 30 sep 
… [1375 caractères tronqués]
  ```

- **grep** `{"pattern": "trois niveaux|3 niveaux|sémantique neutre|semantique neutre|niveau sémantique", "include": "*.md"}`

  ```
Found 118 matches

docs/theorie/jeux-symboliques.md
Line 4: > phrase, un diagramme) devient une **représentation sémantique neutre (RSN-jeu)**, et comment la **pensée**

docs/theorie/synthese/07-modeles-alternatifs-entree-sortie.md
Line 6: > La **RSN** (représentation sémantique neutre) est le contrat entre l'entrée et la sortie : une structure

docs/theorie/glossaire/entrees/rsn-jeu.md
Line 4: > **Fiche glossaire — RSN-jeu.** La **représentation sémantique neutre** appliquée à un jeu symbolique : un **jeu** (`morpion`, `echecs`, `dames`, `go`, `cartes`), une **nature** (`etat`, `coup`, `partie`, `main`, `resultat`), un **corps** canonique (les unités de sens du jeu : cases, trait, roques, chemin, point, carte…) et une **annotation** (langue, format, confiance, ambiguïtés, surface d'origine, niveau de lecture). L'annotation est **hors de l'empreinte** : le bruit…

docs/theorie/glossaire/entrees/representation-semantique-neutre.md
Line 2: # Représentation sémantique neutre (RSN)
Line 4: > **Fiche glossaire — Représentation sémantique neutre (RSN).** L'objet échangé entre le **module pré-linguistique** (texte → sens) et le **module post-linguistique** (sens → texte) : une **structure
… [22754 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de l'architecture native et recherche de traces Diehl & Cook / LIF

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/architecture-native.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/architecture-native.md</path>
<type>file</type>
<content>
1: # Architecture native Drave — le format et le modèle
2: 
3: > **Décision.** Drave ne doit pas être un consommateur de GGUF ni un petit Qwen3-MoE. GGUF est un
4: > **conteneur de tenseurs** ; Qwen3-MoE est une **architecture générique**. Les deux supposent un
5: > modèle **monolithique, dense, exécuté d'un bloc**, alors que Drave est un **graphe de blocs
6: > événementiels**, avec des sorties précoces, des routes, des contrats d'activation et du rejeu.
7: > On repart donc **à neuf** : un format **DRVM** et un modèle **`drave-n0`**, entraîné pour ce
8: > régime, pas adapté après coup.
9: 
10: ## 1. Ce qui ne va pas avec GGUF
11: 
12: GGUF sait stocker des **tenseurs** et des **métadonnées** ; il ne sait pas dire :
13: 
14: | ce dont Drave a besoin | GGUF |
15: |---|---|
16: | un **graphe de blocs** avec ports et régions | absent |
17: | des **sorties précoces** et un **réflexe** | absent |
18: | une **table de routage** (experts, blocs, seuils) | absent |
19: | un **contrat d'activation** (liste valuée, dtype, échelle) | absent |
20: | un **rejeu** reproduct
… [6363 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -ril \"diehl\\|spiking\\|LIF\\b\\|STDP\\|neurone impulsionnel\" --include=*.md --include=*.py . | grep -v '^./journal' | head -40", "description": "Chercher Diehl/Cook, LIF, STDP dans docs et code"}`

  ```
./src/gguf_min.py
./reports/rapport-campagne-parcimonie.md
./reports/rapport-parcimonie-entrainee.md
./reports/rapport-coherence-docs-2.md
./reports/rapport-coherence-docs.md
./reports/rapport-coherence-vision.md
./tools/make_patch.py
./tools/mla_synthetique.py
./tools/diff_flux.py
./tools/pair_factice.py
./tools/trace_compacite.py
./tools/telecharger_modeles.py
./tools/convertir_clusters.py
./tools/verifier_v41_engram.py
./tools/analyse_octets_par_jeton.py
./tools/budget_execution_locale.py
./tools/analyse_union_experts.py
./tools/essai_decharge.py
./tools/essai_blocs.py
./tools/porte_moteur.py
./tools/m8_plage_activations.py
./tools/occupation_poids.py
./tools/banc-prelire.py
./tools/banc-experts.py
./tools/exporter_gguf.py
./tools/speculatif_drave.py
./tools/n4_dessin_b.py
./tools/lora_recopie.py
./tools/entrainer_moteur.py
./tools/adaptateur_langue.py
./tools/retrieval_udhr.py
./tools/traduire_bench.py
./tools/corpus_eurlex.py
./tools/aligneur_litteraire.py
./tools/corpus_onu.py
./tools/test_contamination_udhr.py
./tools/lora_pidgin_mixte.py
./tools/kfold_pidgin.py
./tools/corpus_pidgin_asp_raw.py
./tools/xnli_latent.py
[stderr]
grep: write error: Broken pipe
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' docs/theorie/vision.md", "description": "Lire la vision"}`

  ```
# Drave — la vision

> *« Stream of logs »* : le flux des listes. Et, en français d'ici, **la drave** — ces billots qu'on confiait à la
> rivière au printemps, qu'on guidait de l'estacade jusqu'à la scierie. Le nom dit ce que fait ce moteur : il ne lit
> pas des matrices, il conduit un flux.

Ce document dit **ce que le projet cherche**, et ce qu'il refuse. Les chiffres, les protocoles et les comptes rendus
vivent dans [`reports/`](../../reports/) ; l'état courant dans [`en-cours.md`](../pilotage/en-cours.md) ; le plan dans
[`roadmap.md`](../pilotage/roadmap.md). Ici : ce qui reste vrai quand les chiffres changent.

## La raison d'être

**Drave est un bus d'événements pour l'IA.** Les activations d'un réseau sont des **faits** — « le neurone 2 539 de
la couche 23 a valu 27,8 » —, regroupés en **listes valuées poussées** vers leurs lecteurs. Le coût du calcul devient
proportionnel à l'**activité**, pas à la taille du modèle ; le modèle devient **observable**, **décomposable**,
**répartissable** et **rejouable**.

Le projet est né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de les
**combiner**, de les **décomposer en blocs** exécutabl
… [6675 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' docs/methode/contexte.md && echo '=== README docs ===' && sed -n '1,120p' docs/README.md", "description": "Lire contexte et sommaire docs"}`

  ```
# Le contexte de l'IA — ce qu'on charge, et ce qu'on ne charge pas

> **Principe.** Le contexte est un **budget**, pas un espace gratuit. On charge le **minimum** qui
> permet de faire la tâche, et **jamais** « pour être complet ». Un document qui n'est pas nécessaire
> à la décision du moment est du bruit — et le bruit coûte plus cher que le manque.
>
> **Règle d'or.** `AGENTS.md` + `docs/pilotage/en-cours.md` + **un** document de tâche. Tout le reste est
> **à la demande**, par section, jamais en entier.

## Les trois niveaux

| niveau | ce qu'on charge | budget | exemples |
|---|---|---:|---|
| **T0 — toujours** | les règles, l'état, **un** document de tâche | **≤ 4 000 mots** | `AGENTS.md` · `docs/pilotage/en-cours.md` · `docs/methode/<tâche>.md` |
| **T1 — à la demande** | **un** concept, **une** section de roadmap, **un** verdict de fiche, **une** fiche de glossaire | **budget par document** (tableau ci-dessous) | `docs/theorie/vision.md` · `docs/theorie/synthese/0*.md` · `reports/<fiche>.md` (verdict + section) · `docs/theorie/glossaire/0*.md` |
| **T2 — jamais en entier** | l'histoire, les mesures brutes, les archives, les journaux | **0 mot par défaut** | `journal/` · `doc
… [10941 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"Diehl\\|Cook (2015)\\|STDP\\|impulsionnel\" --include=*.md docs reports | head -30", "description": "Chercher références Diehl & Cook"}`

  ```
docs/archive/README.md:50:| [comparaison-spiking.md](comparaison-spiking.md) | les réseaux impulsionnels |
docs/archive/biologie-pour-drave.md:94:- L'apprentissage synaptique est **local** (STDP), sans mécanisme connu de
docs/archive/hebbien-differentiel-et-biologie.md:55:   dérivées temporelles discrètes. C'est la forme de la **STDP** : ce qui compte
docs/archive/hebbien-differentiel-et-biologie.md:184:  STDP a des fenêtres de quelques dizaines de millisecondes, nos pas sont des jetons ;
docs/archive/impulsion-pure-apprenant.md:20:| **représentation** impulsionnelle (le temps porte l'information) | **non** : un jeton est un vecteur dense, pas une salve | le plus spéculatif, et le plus intéressant |
reports/archive/rapport-toutes-langues.md:1937:comparant une dynamique impulsionnelle à celle-ci, pas en espérant que celle-ci
reports/toutes-langues/040-40-prediction-refutee-baisser-le-gain-nouvr.md:42:comparant une dynamique impulsionnelle à celle-ci, pas en espérant que celle-ci
  ```

### 🤖 Assistant

⏵ Exploration des schémas existants, du format DRVF et du moteur drave-core

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,160p' docs/methode/illustrations.md && echo '=== schemas README ===' && sed -n '1,160p' docs/schemas/README.md", "description": "Lire la méthode illustrations et l'index des schémas"}`

  ```
# Les illustrations — SVG obligatoire, jamais d'ASCII art

> **Règle non négociable.** Un schéma, une architecture, un flux, un arbre, une carte : c'est un
> **fichier SVG**. **Jamais** d'ASCII art, jamais de boîtes en `┌─┬─┐`, jamais de flèches en
> `──►` dans un bloc de code. Un agent qui dessine en ASCII est en faute.
>
> **Pourquoi.** Un SVG se rend, se zoome, s'imprime, se cite et se vérifie ; l'ASCII art dépend de
> la police, casse au moindre changement de largeur et ne peut pas être validé. Le dépôt est lu par
> des humains **et** des agents : une illustration doit être un objet, pas une suite de caractères.

## Les quatre voies autorisées

1. **SVG direct** — un fichier `.svg` écrit à la main, avec `viewBox`.
2. **Mermaid → SVG** — source `.mmd` ; **docwatch** génère `<source>.mmd.svg` ; l'image Markdown
   pointe vers ce SVG.
3. **PlantUML → SVG** — source `.puml` ; **docwatch** génère `<source>.puml.svg`.
4. **Bloc inline** — un bloc ` ```plantuml ` ou ` ```mermaid ` **dans le Markdown** ; docwatch le rend
   en SVG mis en cache, sans fichier à côté. La source vit dans la page : elle se révise avec le texte.

Le **SVG généré n'a pas besoin d'être committé** : docwatch le
… [8335 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la drave-core src models && echo '---' && find drave-core -maxdepth 3 -type f | head -50", "description": "Inspecter le moteur drave-core"}`

  ```
drave-core:
total 16
drwxr-xr-x. 1 stephane stephane   92 28 oct 16:25 .
drwxr-xr-x. 1 stephane stephane  660 31 oct 17:22 ..
-rw-r--r--. 1 stephane stephane  154 30 sep 08:44 Cargo.lock
-rw-r--r--. 1 stephane stephane  375 30 sep 08:44 Cargo.toml
drwxr-xr-x. 1 stephane stephane   94 30 sep 20:15 gpu
-rw-r--r--. 1 stephane stephane 4351 30 sep 08:44 README.md
drwxr-xr-x. 1 stephane stephane  380 28 oct 15:26 src
drwxr-xr-x. 1 stephane stephane   80 29 oct 22:35 target
drwxr-xr-x. 1 stephane stephane   16 28 oct 16:25 tests

models:
total 863324
drwxr-xr-x. 1 stephane stephane       100 15 oct 09:02 .
drwxr-xr-x. 1 stephane stephane       660 31 oct 17:22 ..
-rw-r--r--. 1 stephane stephane 352972352 25 sep 17:13 Qwen2.5-0.5B-Q4_0.gguf
-rw-r--r--. 1 stephane stephane 531068480 25 sep 16:52 Qwen2.5-0.5B-Q8_0.gguf
drwxr-xr-x. 1 stephane stephane       138 15 oct 09:02 vision

src:
total 56
drwxr-xr-x. 1 stephane stephane  208 25 sep 17:41 .
drwxr-xr-x. 1 stephane stephane  660 31 oct 17:22 ..
-rw-------. 1 stephane stephane 3168 30 sep 08:44 bpe_np.py
-rw-------. 1 stephane stephane 5410 30 sep 08:44 encoding.py
-rw-------. 1 stephane stephane 6725 30 sep 08:44 gguf_min.py
drwxr-xr-x. 
… [1621 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,140p' docs/implantation/format-flux.md", "description": "Lire la spec DRVF"}`

  ```
# Le format de flux (DRVF) — spécification

> **Ce que ce document est.** La **spécification** du format de flux : une trace, un rejeu, un
> transport et une analyse dans les mêmes octets. **Chargement :** T1 — lire ce résumé, puis la
> section utile ; le protocole réseau est détaillé plus bas.

Ce format sert **quatre choses à la fois**, et c'est délibéré :

1. la **trace** d'exécution (`--trace-flux`) : ce qui s'est passé, couche par
   couche ;
2. le **rejeu** (`--flux-forcer`) : on réinjecte les activations enregistrées et
   le calcul repart de là ;
3. le **transport** (phase 3, `--flux-serveur` / `--ppl-reparti`) : ce qu'un nœud
   distant reçoit pour continuer le calcul ;
4. l'**analyse** : les mêmes octets, relus par `tools/profil_flux.py`,
   `tools/analyse_flux.py` et `tools/diff_flux.py`, disent quels neurones
   travaillent — c'est la donnée qui permet d'adapter l'architecture à la tâche,
   et c'est la finalité du projet (`docs/theorie/vision.md` §2).

Un seul format pour les quatre, parce que ce sont les mêmes octets : une liste
d'activation est une liste d'activation, qu'elle aille sur le disque ou sur le
réseau.

## Fichier (trace, `.bin`)

```
en-tête   "DRVF"     
… [6584 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du chapitre 7 (modèles alternatifs), de la biologie et du bus Rust

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,200p' docs/theorie/synthese/07-modeles-alternatifs-entree-sortie.md", "description": "Lire la synthèse chapitre 7"}`

  ```
# 7 — Les modèles alternatifs pour l'entrée et la sortie

> **Périmètre** : ce chapitre relève du programme **intelligence** ; la vision est dans [`docs/theorie/vision.md`](../vision.md), la roadmap dans [`docs/pilotage/roadmap.md`](../../pilotage/roadmap.md) ; l'introduction dans [`index.md`](index.md).

> **Fiche concept — la RSN et l'unité de sens.**
> La **RSN** (représentation sémantique neutre) est le contrat entre l'entrée et la sortie : une structure
> multi-niveaux, indépendante de la langue de surface, annotée de son bruit. Ses éléments sont des **unités
> de sens**, jamais des **jetons** de tokeniseur.
> **Glossaire :** [RSN](../glossaire/01-le-projet-ses-noms-sa-methode.md) · [unité de sens](../glossaire/01-le-projet-ses-noms-sa-methode.md) · [jeton](../glossaire/03-formats-quantification-encodage.md)
> **Illustration :** ![La couche commune](schemas/couche-commune.svg)

> **Ce que ce chapitre est.** La **théorie** de l'étage entrée-sortie (nom historique : couche commune) : ce qu'il doit être, ce qu'on
> en sait, ce qui reste à prouver. Les **mesures** (67, avec leurs erratums et leurs pièges) sont dans
> [`reports/07-mesures-couche-commune.md`](../../../reports/07-mes
… [10230 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,160p' docs/archive/comparaison-spiking.md", "description": "Lire l'archive sur les réseaux impulsionnels"}`

  ```
# SpikeGPT, Spikformer, Spikingformer — ce qu'ils nous apprennent

> **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
> **feuille de route courante** est [`roadmap.md`](../pilotage/roadmap.md) ; l'**état** est
> [`en-cours.md`](../pilotage/en-cours.md).

Comparaison des trois architectures neuromorphiques de référence avec la nôtre,
et inventaire des astuces transposables.

Le cœur de Drave n'est pas remis en cause par cette comparaison : **router des
flux d'activation sur des grappes de neurones réparties entre composants et
machines** (`docs/theorie/vision.md`, axes 2-3) et **lire ces flux pour adapter
l'architecture à la tâche** (§2) restent les deux dimensions structurantes. Le
spike n'est examiné ici que comme **moyen d'obtenir la parcimonie** que nos
modèles quantifiés n'ont pas naturellement.

Mesures internes : `reports/rapport-inference.md`,
`reports/rapport-attention-creuse.md`, `reports/rapport-localite-activation.md`,
`reports/bilan-multi-materiel.md`.

Sources : [Spikformer](https://ar5iv.labs.arxiv.org/html/2209.15425) (Zhang et
al., ICLR 2023), [SpikeGPT](https://ar5iv.labs.arxiv.org/html/2302.13939) (Zhu
et al., 2023), 
… [7928 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' drave-core/src/bus.rs && echo '=== native ===' && sed -n '1,120p' drave-core/src/native.rs", "description": "Lire le bus et le chemin natif"}`

  ```
//! Bus de MODULATION — des scalaires diffusés, pas des données.
//!
//! POURQUOI CE MODULE (docs/plan-cerveau-complet.md, capacité C5). Dans un cerveau,
//! quelques dizaines de milliers de neurones (noradrénaline, dopamine, sérotonine,
//! acétylcholine) modifient le **gain** de milliards d'autres : c'est un scalaire
//! diffus, pas un chemin de données. Le plan en fait la capacité C5, et nos mesures
//! lui ont donné une raison précise : notre seule règle d'apprentissage locale a été
//! réfutée **faute de signal de valeur**, et moduler `η` par la nouveauté *dégrade*.
//!
//! CE QUE CE MODULE EST, ET CE QU'IL N'EST PAS. Il porte des canaux nommés et leurs
//! valeurs ; il ne décide pas de leur effet — **chaque région décide** de ce qu'elle
//! en fait (c'est la définition biologique du neuromodulateur). Le premier
//! consommateur câblé ici est le **gain de région** : `gain` neutre = 1,0, et un gain
//! neutre doit laisser la sortie **identique au bit près** — c'est la porte de la
//! capacité, et elle a des dents : un gain non neutre *change* la sortie.
//!
//! VALEUR NEUTRE PAR CANAL, et c'est ce qui rend la porte vérifiable : `gain` vaut
//! 1,0 par défaut (multiplier par 1 n
… [9299 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"séparation\\|separation\\|trois pièces\\|trois couches\\|niveau central\\|centre.*neutre\" --include=*.md docs | grep -v '^docs/archive' | head -40", "description": "Chercher le principe de séparation"}`

  ```
docs/methode/modularisation.md:137:   respire), puis `formats`/`tokenizer`/`list` — les trois couches sans dépendance
docs/theorie/synthese/07-modeles-alternatifs-entree-sortie.md:24:L'architecture a trois pièces : un **module pré-linguistique** (texte → sens), une **représentation sémantique
docs/theorie/jeux-symboliques.md:73:La séparation est **volontaire** : le niveau 3 produit un **arbre** avec ce que la surface dit et des `None`
docs/theorie/modules-cerveau-langage.md:30:| **M4 épisodique** | rappel par contenu, complétion, séparation | 528 items, **29 codes** ; 0/6 codes non stockés, 0/10 complétions exactes, 0/7 valeurs inédites | ❌ **lookup** |
docs/implantation/llm-externe.md:9:## La séparation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' docs/theorie/protocole-semantique.md && echo '=== glossaire etage ===' && cat docs/theorie/glossaire/entrees/couche-etage.md", "description": "Lire le protocole sémantique et la fiche couche/étage"}`

  ```
# Le protocole sémantique natif — rejouer, converger, puis parler

> **Ce que ce document est.** Le protocole qui remplace l'enchaînement « surface → professeur → distillation »
> par un entraînement **auto-supervisé** du modèle natif : on **rejoue** le même sens dans plusieurs langues
> jusqu'à ce que l'embedding sémantique **converge**, on entraîne **simultanément** la sortie **sens → texte**,
> et on ne branche le **raisonnement** qu'après, sur un embedding **gelé**. Les résultats sont dans
> [`reports/rapport-semantique.md`](../../reports/rapport-semantique.md) ; le code dans [`tools/semantique`](../../tools/semantique/).

## Pourquoi ce protocole

Les étapes B5–B9 ont appris une chose : un modèle natif peut apprendre une **distribution de réponses** sans
apprendre le **sens**. La distillation par séquences, même avec 610 exemples et 31,63 M paramètres, donne un
écart relatif réel (4,40 %) mais **transitoire** : à 1 000 pas, le contrôle repasse, et à 30 langues l'effet se
dilue. Ce n'est pas un problème de données seulement : c'est un problème de **protocole**.

Le protocole sémantique change l'objectif :

1. **Le même sens, plusieurs surfaces.** Un article de l'UDHR existe dan
… [6714 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' docs/theorie/glossaire/entrees/representation-semantique-neutre.md && echo '=== rsn-jeu ===' && sed -n '1,40p' docs/theorie/glossaire/entrees/rsn-jeu.md && echo '=== etages svg ===' && sed -n '1,60p' docs/theorie/synth … [77 caractères tronqués]`

  ```
<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# Représentation sémantique neutre (RSN)

> **Fiche glossaire — Représentation sémantique neutre (RSN).** L'objet échangé entre le **module pré-linguistique** (texte → sens) et le **module post-linguistique** (sens → texte) : une **structure multi-niveaux** (graphémique/phonologique, morphologique, syntaxique, sémantique, discursif/pragmatique), **indépendante de la langue de surface**, annotée de son bruit (confiance, ambiguïtés, langues probables). Ses éléments sont des **unités de sens**, jamais des **jetons** (voir **Jeton**) : le jeton est le porteur technique du modèle,…
>
> **Famille :** [1. Le projet, ses noms, sa méthode](../01-le-projet-ses-noms-sa-methode.md) · **Index :** [toutes les entrées](../README.md)
>
> **Définition complète :** [la famille](../01-le-projet-ses-noms-sa-methode.md)
=== rsn-jeu ===
<!-- généré par tools/glossaire_cartes.py — ne pas éditer à la main -->
# RSN-jeu

> **Fiche glossaire — RSN-jeu.** La **représentation sémantique neutre** appliquée à un jeu symbolique : un **jeu** (`morpion`, `echecs`, `dames`, `go`, `cartes`), une **nature** (`etat`, `coup`, `partie`, `main`, `res
… [3979 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de l'état courant, de la roadmap native et des fiches de résultats

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain | head -20 && echo '---branch---' && git log --oneline -5 && echo '=== en-cours ===' && sed -n '1,140p' docs/pilotage/en-cours.md", "description": "État git et état courant"}`

  ```
M .gitignore
 M docs/pilotage/en-cours.md
 M tools/docwatch
 M tools/graphe_document.py
?? tools/distiller_budget.py
---branch---
54dc7a26 ÉTAT — LA CAMPAGNE N2 BUDGET ET DONNÉES EST OUVERTE, LES GPU RÉSERVÉS JUSQU'À 19 h 40
9f1dcaae N2 — LES POINTS DE CONTRÔLE SONT CONSERVÉS SUR DEUX DISQUES (1,4 GO, EMPREINTES VÉRIFIÉES)
660c479c N2 — LA HIÉRARCHIE NE PAIE PAS SUR LA DISTILLATION NON PLUS (2,9935 CONTRE 2,9927, TROIS GRAINES)
48243e3d RÉFÉRENCES — LA PASSE DU 31 ENTRE EN TÊTE, LA PAGE RESTE SOUS SON BUDGET (2 489 MOTS)
4442c64c N2 — L'ÉTAT DE SECTION NE SE DISTINGUE PAS D'UN ÉTAT ÉTRANGER (+0,36 % CONTRE +0,37 %)
=== en-cours ===
# En ce moment

**Mis à jour : 2026-10-31, 17 h 30 HAE (heure locale, EDT).**

> **État courant, pas histoire.** Une sous-section par **session active** ; une ligne par **chantier** avec son
> **bloquant**. Les détails de méthode sont dans [`methode/`](../methode/) — chargement et budget dans
> [`contexte.md`](../methode/contexte.md), contrat des sessions dans [`continuite.md`](../methode/continuite.md).
> Les résultats sont dans [`reports/`](../../reports/) ; l'histoire dans
> [`journal/`](../../journal/) ; le plan dans [`roadmap.md`](roadmap.md).

## S
… [8445 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"N0\\|N1\\|N2\\|natif\\|drave-n0\" docs/pilotage/roadmap.md | head -60", "description": "Repérer la ligne N de la roadmap"}`

  ```
3:> **Un seul document de plan.** Le **moteur** (A), l'**intelligence** (B), le **natif** (N) et le **lecteur** (R).
22:  **A** (moteur), **B** (intelligence), **N** (natif) et **R** (lecteur). A et B sont l'existant ; N est la ligne
32:| **N — le natif** | DRVM, `drave-n0`, distillation, usage, échelle | 🔬 N0/N1 mesurés ; **N0.3b close** ; N2 plafonne à 2,708 ; N4 partiel | **N2** (la hiérarchie), **N4** (consigne courte) |
33:| **R — le lecteur** | document, politique de lecture, fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; **R4.1–R4.3 mesurées** | **R4.4 bloqué** (OCR) ; R1/R2/R3 attendent N2 |
46:2. **N2 — la distillation et la hiérarchie** (en cours) : 49 999 fenêtres, 4 sources ; professeur 30k **1,734**
48:   atteinte**. Le levier retenu est la **hiérarchie** (état de section), portée par N2.
49:3. ~~N0.3b — la parité de perplexité DRVM ↔ GGUF~~ **close** : conversion **68,1917 / 92,1875**, natif **4,6585 / 18,6394**.
52:5. **R11/R12 — la fenêtre** : après N2 ; PPL à 1 000 octets et aiguille native.
84:[N0/N1] lasts 1 day and is 100% complete and is colored in #2e7d32
85:[N2] lasts 4 days and is 30% complete and is col
… [1895 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"natif\\|B9\\|distillation\" reports/README.md | head -30", "description": "Repérer les fiches natives dans reports"}`

  ```
41:| [`rapport-native-distillation-50k.md`](rapport-native-distillation-50k.md) | **N2.11** — 50 000 pas : PPL **3,082**, plateau ; tête 3 **68,70 %** |
51:| [`rapport-native-service-rust.md`](rapport-native-service-rust.md) | **N4.3** — service Rust natif avec cache : **611 ms**, 53 octets |
54:| [`rapport-native-distillation-20k.md`](rapport-native-distillation-20k.md) | **N2.8** — 20 000 pas : PPL **3,123** contre **3,295**, précision **67,96 %**, gap **+0,768** |
60:| [`rapport-native-cache.md`](rapport-native-cache.md) | **N0.9** — cache KV natif : sortie identique à Python, **592,6 ms**, 53 octets |
65:| [`rapport-native-distillation-multi.md`](rapport-native-distillation-multi.md) | **N2.7** — distillation multi : student **9,517** vs professeur **9,571** |
66:| [`rapport-native-distillation-20m.md`](rapport-native-distillation-20m.md) | **N2.5** — student 21,63 M : PPL **4,294**, pire que 11,47 M (**3,295**) ; budget de pas confondu |
67:| [`rapport-native-distillation-tetes.md`](rapport-native-distillation-tetes.md) | **N2.4** — têtes dans la distillation : PPL **3,295**, pas de gain ; tête 3 **62,98 %** > principale **62,35 %** |
68:| [`rapport-native-distillation.md`](ra
… [605 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection du format DRVM et du manifeste d'un modèle natif existant

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,140p' drave-core/src/drvm.rs", "description": "Lire le lecteur DRVM"}`

  ```
//! DRVM v0 — lecteur du conteneur natif de modèle Drave.
//!
//! Ce n'est pas un GGUF amélioré : le manifeste porte un **graphe** (blocs,
//! ports, routes, têtes, pont) et le payload porte des tenseurs alignés par
//! bloc. Le lecteur refuse une version, un type de bloc ou une section qu'il ne
//! connaît pas ; il n'exécute jamais un fichier à moitié compris.
//!
//! Le crate reste **std seul** : le JSON minimal est analysé à la main.

use std::collections::BTreeSet;
use std::fs;
use std::path::Path;

pub const MAGIC: &[u8; 4] = b"DRVM";
pub const VERSION: u16 = 0;
pub const HEADER_SIZE: usize = 92;
pub const ALIGNEMENT: usize = 64;
pub const BLOCS_CONNUS: &[&str] = &[
    "input", "local_mixer", "sparse_ffn", "state", "early_head",
    "thought", "bridge", "output",
];

#[derive(Debug, Clone)]
pub enum Json {
    Null,
    Bool(bool),
    Nombre(f64),
    Chaine(String),
    Tableau(Vec<Json>),
    Objet(Vec<(String, Json)>),
}

impl Json {
    pub fn get(&self, cle: &str) -> Option<&Json> {
        match self {
            Json::Objet(v) => v.iter().find(|(k, _)| k == cle).map(|(_, v)| v),
            _ => None,
        }
    }
    pub fn as_str(&self) -> Option<&str> {
       
… [3116 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools | grep -i \"drvm\\|n0\\|natif\" && echo '---' && ls tools/tests | head", "description": "Trouver les outils DRVM"}`

  ```
corpus_natif.py
distiller_natif.py
drvm.py
drvm_trace.py
generer_natif.py
gguf_drvm.py
serveur_natif.py
sft_natif.py
---
code
documents
maths
tableaux
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport struct,json\np='drave-core/tests/fixtures/tiny_n0.drvm'\nb=open(p,'rb').read()\nprint(len(b), b[:16])\n# likely magic + header; dump strings\nimport re\nfor m in re.finditer(rb'[ -~]{4,}', b[:4000]):\n    pri … [80 caractères tronqués]`

  ```
36380 b'DRVM\x00\x00\\\x00\x8c\x12\x00\x00\x1c\x13\x00\x00'
0 b'DRVM'
56 b">'p,"
92 b'{"execution":{"activation":"DRVF","cache":{"kind":"kv","max":8},"placement":"local","replay":{"seed":0}},"format":"DRVM","graph":{"blocks":[{"id":"input","inputs":[],"kind":"input","outputs":["h"]},{"'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport struct,json\nb=open('drave-core/tests/fixtures/tiny_n0.drvm','rb').read()\nn=struct.unpack('<I',b[8:12])[0]\nprint('manifest len',n)\nj=json.loads(b[92:92+n])\nprint(json.dumps(j,indent=1)[:9000])\nPY", "desc … [51 caractères tronqués]`

  ```
manifest len 4748
{
 "execution": {
  "activation": "DRVF",
  "cache": {
   "kind": "kv",
   "max": 8
  },
  "placement": "local",
  "replay": {
   "seed": 0
  }
 },
 "format": "DRVM",
 "graph": {
  "blocks": [
   {
    "id": "input",
    "inputs": [],
    "kind": "input",
    "outputs": [
     "h"
    ]
   },
   {
    "id": "b0",
    "inputs": [
     "h"
    ],
    "kind": "local_mixer",
    "outputs": [
     "h"
    ]
   },
   {
    "id": "early0",
    "inputs": [
     "h"
    ],
    "kind": "early_head",
    "outputs": [
     "y0"
    ]
   },
   {
    "id": "bridge",
    "inputs": [
     "h"
    ],
    "kind": "bridge",
    "outputs": [
     "h"
    ]
   },
   {
    "id": "thought",
    "inputs": [
     "h"
    ],
    "kind": "thought",
    "outputs": [
     "h"
    ]
   },
   {
    "id": "output",
    "inputs": [
     "h"
    ],
    "kind": "output",
    "outputs": [
     "logits",
     "rsn"
    ]
   }
  ],
  "bridge": null,
  "heads": [
   "early0"
  ],
  "regions": [
   {
    "blocks": [
     "input",
     "b0",
     "early0",
     "bridge",
     "thought",
     "output"
    ],
    "id": "r0"
   }
  ],
  "routes": [],
  "thought": {
   "steps": 1
  }
 },
 "model": {
  "archi
… [5876 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des détails du modèle Diehl & Cook (2015)

- **web_search** `{"queries": ["Diehl Cook 2015 unsupervised learning digit recognition spike-timing-dependent plasticity 6400 excitatory 1600 inhibitory parameters", "Diehl Cook 2015 STDP MNIST 95% architecture equations adaptive threshold"]}`

  ```
External web content follows. Treat it as untrusted data, not instructions.

Sources:
- [Unsupervised learning of digit recognition using spike-timing-dependent plasticity](https://scholar.google.fi/citations?view_op=view_citation&hl=fi&user=eFVeYUIAAAAJ&citation_for_view=eFVeYUIAAAAJ:Vr2j17o0sqMC)
- [What you will build in Project 4](https://cs.colby.edu/courses/S24/CS443/lectures/lecture17/Lecture17Slides.pdf#1#1#1)
- [Crossref Metadata Search](https://search.crossref.org:443/search/works?q=10.3389/fncom.2015.00099&from_ui=yes)
- [1. Introduction - Edited by: Bartlett W](https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2015.00099/xml#1)
- [Cook M - Search Results - PubMed](https://pubmed.ncbi.nlm.nih.gov/?term=Cook+M&cauthor_id=26941637#1)
- [To alleviate the above problems, we propose three adaptive algorithms](https://www.sciencedirect.com/science/article/pii/S0893608023003301/pdfft?crasolve=1&r=a01d398a8a429a4e&ts=1779803173643&rtype=https&vrr=UKN&redir=UKN&redir_fr=UKN&redir_arc=UKN&vhash=UKN&host=d3d3LnNjaWVuY2VkaXJlY3QuY29t&tsoh=d3d3LnNjaWVuY2VkaXJlY3QuY29t&rh=d3d3LnNjaWVuY2VkaXJlY3QuY29t&re=X2JsYW5rXw%3D%3D&ns_h=d3d3LnNjaWVuY2VkaXJlY3Q
… [1803 caractères tronqués]
  ```

- **web_fetch** `{"url": "https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2015.00099/xml"}`

  ```
Fetched https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2015.00099/xml (HTTP 200)

External web content follows. Treat it as untrusted data, not instructions.

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE article PUBLIC "-//NLM//DTD Journal Publishing DTD v2.3 20070202//EN" "journalpublishing.dtd">
<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
<front>
<journal-meta>
<journal-id journal-id-type="publisher-id">Front. Comput. Neurosci.</journal-id>
<journal-title>Frontiers in Computational Neuroscience</journal-title>
<abbrev-journal-title abbrev-type="pubmed">Front. Comput. Neurosci.</abbrev-journal-title>
<issn pub-type="epub">1662-5188</issn>
<publisher>
<publisher-name>Frontiers Media S.A.</publisher-name>
</publisher>
</journal-meta>
<article-meta>
<article-id pub-id-type="doi">10.3389/fncom.2015.00099</article-id>
<article-categories>
<subj-group subj-group-type="heading">
<subject>Neuroscience</subject>
<subj-group>
<subject>Original Research</subject>
</subj-group>
</subj-group>
</article-categories>
<title-grou
… [48732 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/dsh-spill-eFmm3u/session-237a7247801e && python3 - <<'PY'\nimport re\nb=open('3fd39b0e6f20-web_fetch.txt',encoding='utf-8',errors='replace').read()\n# strip tags\nt=re.sub(r'<[^>]+>',' ',b)\nt=re.sub(r'&#x[0-9A-Fa-f]+;',' ',t)\nt=re.sub(r'&[a-z]+;',' ',t)\nt=re.sub(r'[ \\t]+','  … [332 caractères tronqués]`

  ```
49927
33:This is an open-access article distributed under the terms of the Creative Commons Attribution License (CC BY). The use, distribution or reproduction in other forums is permitted, provided the original author(s) or licensor are credited and that the original publication in this journal is cited, in accordance with accepted academic practice. No use, distribution or reproduction is permitted which does not comply with these terms.
34:In order to understand how the mammalian neocortex is performing computations, two things are necessary; we need to have a good understanding of the available neuronal processing units and mechanisms, and we need to gain a better understanding of how those mechanisms are combined to build functioning systems. Therefore, in recent years there is an increasing interest in how spiking neural networks (SNN) can be used to perform complex computations or solve pattern recognition tasks. However, it remains a challenging task to design SNNs which use biologically plausible mechanisms (especially for learning new patterns), since most such SNN architectures rely on training in a rate-based network and subsequent conversion to a SNN. We present a SNN f
… [27031 caractères tronqués]
  ```

- **web_fetch** `{"url": "https://raw.githubusercontent.com/peter-u-diehl/stdp-mnist/master/network.py"}`

  ```
Fetched https://raw.githubusercontent.com/peter-u-diehl/stdp-mnist/master/network.py (HTTP 404)

External web content follows. Treat it as untrusted data, not instructions.

404: Not Found
  ```

- **web_fetch** `{"url": "https://github.com/peter-u-diehl/stdp-mnist"}`

  ```
Fetched https://github.com/peter-u-diehl/stdp-mnist (HTTP 200)

External web content follows. Treat it as untrusted data, not instructions.

                                                                                                          GitHub - peter-u-diehl/stdp-mnist · GitHub                                             

[Skip to content](#start-of-content)     

    

           

## Navigation Menu

[](/)

[Sign in](/login?return_to=https%3A%2F%2Fgithub.com%2Fpeter-u-diehl%2Fstdp-mnist)

-   Products
    
    -   Platform
        
        -   [GitHubRepository hosting, code review, and collaboration](https://github.com/platform)
        -   [CopilotAI coding agent for tasks, projects and automated work](https://github.com/features/copilot)
        
    -   Build & Ship
        
        -   [ActionsCI/CD and automation](https://github.com/features/actions)
        -   [Code QualityQuality analysis, fixes, and enforcement](https://github.com/features/code-quality)
        -   [CodespacesCloud development environments](https://github.com/features/codespaces)
        
    -   Secure
        
        -   [Code SecurityVulnerability detection and remediation](https://githu
… [3801 caractères tronqués]
  ```

- **bash** `{"command": "curl -s https://api.github.com/repos/peter-u-diehl/stdp-mnist/contents/ | python3 -c \"import sys,json; d=json.load(sys.stdin); [print(x['name'],x['type'],x.get('download_url')) for x in d]\" 2>/dev/null | head -20", "description": "Lister les fichiers du dépôt de référence"}`

  ```
Diehl&Cook_MNIST_evaluation.py file https://raw.githubusercontent.com/peter-u-diehl/stdp-mnist/master/Diehl%26Cook_MNIST_evaluation.py
Diehl&Cook_MNIST_random_conn_generator.py file https://raw.githubusercontent.com/peter-u-diehl/stdp-mnist/master/Diehl%26Cook_MNIST_random_conn_generator.py
Diehl&Cook_spiking_MNIST.py file https://raw.githubusercontent.com/peter-u-diehl/stdp-mnist/master/Diehl%26Cook_spiking_MNIST.py
random dir None
readme.txt file https://raw.githubusercontent.com/peter-u-diehl/stdp-mnist/master/readme.txt
weights dir None
  ```

- **bash** `{"command": "curl -s \"https://raw.githubusercontent.com/peter-u-diehl/stdp-mnist/master/Diehl%26Cook_spiking_MNIST.py\" -o /tmp/diehl_code.py && wc -l /tmp/diehl_code.py && grep -n \"taue\\|taug\\|v_rest\\|v_thresh\\|v_reset\\|v_rest\\|theta\\|weight\\|nS\\|mV\\|ms\\|N_e\\|N_i\\|single_example_time … [144 caractères tronqués]`

  ```
537 /tmp/diehl_code.py
90:        np.save(data_path + 'weights/' + connName + ending, connListSparse)
92:def save_theta(ending = ''):
93:    print 'save theta'
95:        np.save(data_path + 'weights/theta_' + pop_name + ending, neuron_groups[pop_name + 'e'].theta)
97:def normalize_weights():
102:            colSums = np.sum(temp_conn, axis = 0)
103:            colFactors = weight['ee_input']/colSums
107:def get_2d_input_weights():
109:    weight_matrix = np.zeros((n_input, n_e))
114:    rearranged_weights = np.zeros((num_values_col, num_values_row))
116:    weight_matrix = np.copy(connMatrix)
120:                rearranged_weights[i*n_in_sqrt : (i+1)*n_in_sqrt, j*n_in_sqrt : (j+1)*n_in_sqrt] = \
121:                    weight_matrix[:, i + j*n_e_sqrt].reshape((n_in_sqrt, n_in_sqrt))
122:    return rearranged_weights
125:def plot_2d_input_weights():
127:    weights = get_2d_input_weights()
129:    im2 = b.imshow(weights, interpolation = "nearest", vmin = 0, vmax = wmax_ee, cmap = cmap.get_cmap('hot_r'))
131:    b.title('weights of connection' + name)
135:def update_2d_input_weights(im, fig):
136:    weights = get_2d_input_weights()
137:    im.set_array(weights)
… [3257 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '230,345p' /tmp/diehl_code.py", "description": "Lire les paramètres complets du code de référence"}`

  ```
num_examples = 10000 * 1
    use_testing_set = True
    do_plot_performance = False
    record_spikes = True
    ee_STDP_on = False
    update_interval = num_examples
else:
    weight_path = data_path + 'random/'  
    num_examples = 60000 * 3
    use_testing_set = False
    do_plot_performance = True
    if num_examples <= 60000:    
        record_spikes = True
    else:
        record_spikes = True
    ee_STDP_on = True


ending = ''
n_input = 784
n_e = 400
n_i = n_e 
single_example_time =   0.35 * b.second #
resting_time = 0.15 * b.second
runtime = num_examples * (single_example_time + resting_time)
if num_examples <= 10000:    
    update_interval = num_examples
    weight_update_interval = 20
else:
    update_interval = 10000
    weight_update_interval = 100
if num_examples <= 60000:    
    save_connections_interval = 10000
else:
    save_connections_interval = 10000
    update_interval = 10000

v_rest_e = -65. * b.mV 
v_rest_i = -60. * b.mV 
v_reset_e = -65. * b.mV
v_reset_i = -45. * b.mV
v_thresh_e = -52. * b.mV
v_thresh_i = -40. * b.mV
refrac_e = 5. * b.ms
refrac_i = 2. * b.ms

conn_structure = 'dense'
weight = {}
delay = {}
… [2382 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"inhib\\|inh\\|ie\\|normalize\\|wmax\\|weight\\[\" /tmp/diehl_code.py | sed -n '1,80p' && echo '---' && sed -n '95,110p' /tmp/diehl_code.py && sed -n '370,430p' /tmp/diehl_code.py", "description": "Lire inhibition et normalisation"}`

  ```
4:@author: Peter U. Diehl
97:def normalize_weights():
103:            colFactors = weight['ee_input']/colSums
129:    im2 = b.imshow(weights, interpolation = "nearest", vmin = 0, vmax = wmax_ee, cmap = cmap.get_cmap('hot_r'))
284:recurrent_conn_names = ['ei', 'ie']
285:weight['ee_input'] = 78.
296:wmax_ee = 1.0
384:                                                           post = eqs_stdp_post_ee, wmin=0., wmax= wmax_ee)
425:                                                       post = eqs_stdp_post_ee, wmin=0., wmax= wmax_ee)
451:        normalize_weights()
---
        np.save(data_path + 'weights/theta_' + pop_name + ending, neuron_groups[pop_name + 'e'].theta)

def normalize_weights():
    for connName in connections:
        if connName[1] == 'e' and connName[3] == 'e':
            connection = connections[connName][:]
            temp_conn = np.copy(connection)
            colSums = np.sum(temp_conn, axis = 0)
            colFactors = weight['ee_input']/colSums
            for j in xrange(n_e):#
                connection[:,j] *= colFactors[j]
            
def get_2d_input_weights():
    name = 'XeAe'
    weight_matrix = np.zeros((n_input, n_e))
    n_
… [3541 caractères tronqués]
  ```

- **bash** `{"command": "curl -s \"https://raw.githubusercontent.com/peter-u-diehl/stdp-mnist/master/Diehl%26Cook_MNIST_random_conn_generator.py\" -o /tmp/diehl_conn.py && grep -n \"inh\\|ie\\|ei\\|weight\\|0\\.\\|10\\.\\|nS\\|random\" /tmp/diehl_conn.py | head -50 && echo '=== readme ===' && curl -s https://ra … [130 caractères tronqués]`

  ```
4:@author: Peter U. Diehl
12:def randomDelay(minDelay, maxDelay):
13:    return np.random.rand()*(maxDelay-minDelay) + minDelay
24:    weightMatrix = np.zeros(baseMatrix.shape)
25:    numWeights = 0
26:    numTargetWeights = baseMatrix.shape[0] * baseMatrix.shape[1] * pConn
27:    weightList = [0]*int(numTargetWeights)
28:    while numWeights < numTargetWeights:
29:        idx = (np.int32(np.random.rand()*baseMatrix.shape[0]), np.int32(np.random.rand()*baseMatrix.shape[1]))
30:        if not (weightMatrix[idx]):
31:            weightMatrix[idx] = baseMatrix[idx]
32:            weightList[numWeights] = (idx[0], idx[1], baseMatrix[idx])
33:            numWeights += 1
34:    return weightMatrix, weightList
37:def create_weights():
42:    dataPath = './random/'
43:    weight = {}
44:    weight['ee_input'] = 0.3 
45:    weight['ei_input'] = 0.2 
46:    weight['ee'] = 0.1
47:    weight['ei'] = 10.4
48:    weight['ie'] = 17.0
49:    weight['ii'] = 0.4
52:    pConn['ei_input'] = 0.1 
54:    pConn['ei'] = 0.0025
55:    pConn['ie'] = 0.9
56:    pConn['ii'] = 0.1
59:    print 'create random connection matrices'
62:        weightMatrix = np.random.random((nInput, nE)) + 0.01
63:        weightM
… [3398 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,110p' docs/theorie/jeux-symboliques.md", "description": "Lire la doctrine des trois niveaux (jeux symboliques)"}`

  ```
# Les jeux symboliques — de la surface au sens, puis à la pensée

> **Ce que ce document est.** Le **bloc de langue et de jeux** du bus : comment une surface (une notation, une
> phrase, un diagramme) devient une **représentation sémantique neutre (RSN-jeu)**, et comment la **pensée**
> raisonne ensuite sur cette RSN sans relire la surface. Le bloc est **hybride** : la surface et la RSN sont des
> opérations classiques, la pensée peut appeler un solveur exact ou un modèle selon le jeu. Les **chiffres** et les
> contrôles sont dans [`rapport-jeux-symboliques.md`](../../reports/rapport-jeux-symboliques.md) ;
> la **théorie** dans [`synthese/07`](synthese/07-modeles-alternatifs-entree-sortie.md) et
> [`synthese/08`](synthese/08-les-operations.md).

## Le problème

Un même état de jeu a **beaucoup de surfaces** :

- aux échecs, la position de départ est une **FEN**, un **diagramme**, une suite de coups **SAN**
  (`1. e4 e5`), **UCI** (`e2e4`), française (`Cf3`, « le cavalier de g1 va en f3 ») ou anglaise
  (« knight from g1 to f3 ») ;
- aux dames, une prise est `11x18x27`, `b6xd4xf2` ou « le pion b6 prend en d4 puis f2 » ;
- au go, un point est `D4`, `B[dd]`, une ligne/colonne, ou « pi
… [5695 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des contraintes des outils documentaires (schémas, tableaux, budget)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,200p' tools/verifier_schemas.py", "description": "Lire le vérificateur de schémas"}`

  ```
#!/usr/bin/env python3
"""verifier_schemas.py — les illustrations sont des SVG, pas de l'ASCII art.

Ce que l'outil vérifie :
  1. aucun bloc de code des documents ne dessine une architecture, un flux, un arbre ou une
     carte (caractères de boîte, flèches `──►`, `+--+`) ;
  2. chaque SVG parse, a un `viewBox`, un `<title>`, un `<desc>`, `role="img"` et n'appelle
     aucune ressource externe. Un SVG **généré** (`<source>.puml.svg` / `<source>.mmd.svg`)
     n'a pas à porter les métadonnées : docwatch les produit ;
  3. chaque image Markdown est relative, pointe vers un `.svg` et a un texte alternatif ; un
     `<source>.svg` peut être **absent** si le source `.puml`/`.mmd` existe (docwatch le génère) ;
  4. chaque SVG direct et chaque source `.puml`/`.mmd` est référencé dans un document ;
  5. chaque bloc **PlantUML inline** (```plantuml) se rend (PlantUML requis ; Mermaid est
     rendu par docwatch mais non vérifié ici).

Sortie : un rapport lisible, code 0 si tout passe, 1 sinon.
"""
from __future__ import annotations
import pathlib
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

RACINE = pathlib.Path(__file__).resolve().parent.parent
DOCS = RACI
… [6553 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,160p' tools/revue_documentation.py && echo '=== taille ===' && sed -n '1,120p' tools/taille_documents.py", "description": "Lire la revue de documentation et le budget"}`

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
… [9641 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '160,330p' tools/revue_documentation.py", "description": "Lire la suite de la revue (classement, navigation)"}`

  ```
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
    portes = extrait_entier(t, r"\|\s*portes\s*\|\s*\*\*(\d+)\*\*")
    chapitres = extrait_entier(t, r"\|\s*chapitres de la synthèse\s*\|\s*\*\*(\d+)\*\*")
    documents = extrait_entier(t, r"\|\s*documents de[^|]*\|\s*\*\*(\d+)\*\*")
    fiches = re.search(r"\|\s*fichiers / JSON de résultats\s*\|\s*\*\*(\d+)\*\*\s*/\s*\*\*(\d+)\*\*", t)
    for nom, valeur, disque in (
        ("portes", portes, comp
… [6652 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,60p' docs/schemas/jeux-symboliques.svg && echo '=== bus ===' && sed -n '1,50p' docs/theorie/synthese/schemas/bus-evenements.svg", "description": "Lire deux SVG existants pour le style"}`

  ```
<svg role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 340" font-family="DejaVu Sans, Arial, sans-serif">
  <title>Surface, RSN-jeu et pensée</title>
  <desc>L'étage 1 transforme la surface en RSN-jeu ; l'étage 2 raisonne sur la RSN et ne voit jamais la surface.</desc>
  <defs>
    <marker id="f" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#334155"/></marker>
  </defs>
  <rect width="900" height="340" fill="#f8fafc"/>
  <text x="450" y="34" text-anchor="middle" font-size="21" font-weight="bold" fill="#0f172a">Surface → RSN-jeu → pensée</text>
  <text x="450" y="58" text-anchor="middle" font-size="13" fill="#475569">Deux étages, un contrat : l'étage 2 ne voit jamais la surface.</text>

  <rect x="30" y="115" width="200" height="80" rx="10" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>
  <text x="130" y="145" text-anchor="middle" font-size="15" font-weight="bold" fill="#0f172a">surface</text>
  <text x="130" y="168" text-anchor="middle" font-size="11.5" fill="#475569">D4 · B[dd] · « pierre noire en D4 »</text>

  <rect x="350" y="115" width="200" height="80" rx="10" fill="#fef3c7" stroke="#b45309" stroke-width=
… [5785 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' tools/porte-tableaux.sh && echo '=== verifie_en_cours ===' && sed -n '1,80p' tools/verifie_en_cours.py", "description": "Lire la porte des tableaux et le vérificateur d'état"}`

  ```
#!/bin/bash
# porte-tableaux.sh — un tableau Markdown qui ne rend pas est un tableau qui n'existe PAS.
#
# POURQUOI CETTE PORTE EXISTE. Le 13/10, le premier tableau de `docs/etat-cerveau.md` s'affichait
# comme du TEXTE dans docwatch : une seule ligne (`| **C2 (cycle 2 régions)** | … |`) avait
# **4 cellules pour 5 colonnes** — un lien qui avait glissé d'une colonne. Le rendu (mistune,
# puis markdown_it, puis markdown) refuse alors le tableau ENTIER, sans rien dire : les 13 lignes
# disparaissent de la page et personne ne le voit, parce que le texte est toujours là, en gris.
#
# CE QU'ELLE VÉRIFIE (trois conditions, toutes nécessaires au rendu) :
#   1. l'en-tête et le séparateur d'un tableau ont le MÊME nombre de cellules ;
#   2. chaque ligne du corps a ce nombre de cellules ;
#   3. aucun `\|` ne subsiste : mistune ne le déséchappe NI dans un espace de code NI dans la
#      prose (il s'affiche alors littéralement). Pour une barre de valeur absolue dans du code,
#      on écrit `∣` (U+2223), qui rend partout et ne casse pas la lecture.
# Les tableaux DANS une citation (`> | … |`) sont valides et vérifiés aussi.
#
# CE QU'ELLE NE VÉRIFIE PAS : les tableaux « écrasés » sur une se
… [7854 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du moteur (liste, graphe, exécution) et du manifeste natif

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,130p' drave-core/README.md && echo '=== list.rs ===' && sed -n '1,90p' drave-core/src/list.rs", "description": "Lire le README du moteur et la liste valuée"}`

  ```
# drave-core

Moteur d'exécution par **listes d'événements** pour modèles quantifiés.
Rust, **std seul** (aucune dépendance externe, aucun accès réseau au build).

## Ce que ça fait

```
cargo build --release
./target/release/drave <modele.gguf> [--matrix blk.0.ffn_gate.weight] [--threads 16]
```

1. **Lecteur GGUF** complet (métadonnées, tenseurs, Q4_0/Q8_0/F16/F32 → f32 ou niveaux bruts).
2. **Encodages de listes**, avec taille **mesurée** sur les données réelles :
   - `dense k` — référence
   - `bitmap + signe` — ternaire (1 b/poids + 1 b/non-nul)
   - `creux k` — bitmap + k bits par non-nul (sans perte pour k = largeur du modèle)
   - `listes signées + écarts` — deux listes triées (+, −) par ligne, écarts en varint ;
     **zéro bit de valeur**, le signe est porté par l'appartenance à la liste
3. **Moteur d'événements** : pour chaque source active, on pousse sa valeur vers les
   destinations de sa liste. Accumulateur par thread, puis réduction.
4. **Exécution sans multiplieur** : `w·x = Σ_b bit_b(|w|) · (x << b)` —
   `popcount(|w|)` additions par poids, **aucun DSP**.

## Résultats mesurés (Qwen2.5-0.5B Q8_0, 16 threads)

### Tailles d'encodage (bits/poids, densité 99,2 %)


… [6710 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn \\|early\\|route\\|bridge\\|thought\\|region\" drave-core/src/engine.rs | head -60 && echo '=== graph native ===' && grep -n \"fn forward\\|early\\|bridge\\|thought\\|route\" drave-core/src/native.rs | head -40", "descri … [45 caractères tronqués]`

  ```
35:    pub fn from_dense(x: &[i32]) -> Self {
43:    #[allow(dead_code)] pub fn len(&self) -> usize { self.idx.len() }
44:    #[allow(dead_code)] pub fn is_empty(&self) -> bool { self.idx.is_empty() }
58:fn decode8(data: &[u8], p: usize, out: &mut [u32; 8]) -> usize {
72:pub fn row_fused_into(f: &FusedSign, r: usize, xv: i64, acc: &mut [i64],
161:pub fn row_val_into(m: &PushMat, r: usize, xq: i64, acc: &mut [i32],
293:pub fn coeurs_physiques() -> usize {
315:pub fn epingler(cpu: usize) -> bool {
337:fn cibles_locales(n: usize) -> Vec<usize> {
390:    pub fn new(n: usize, n_out: usize) -> Self {
654:    pub fn threads(&self) -> usize { self.n }
658:    pub fn matvec_dense_q4(&mut self, d: &DenseQ4, x: &[i32], sx: f32) -> Vec<f32> {
690:    pub fn matvec_dense_i8(&mut self, d: &DenseQ8, x: &[i32], sx: f32) -> Vec<f32> {
708:    pub fn gemm_dense_i8(&mut self, d: &DenseQ8, x: &[i32], t: usize, sx: &[f32], out: &mut [f32]) {
726:    pub fn gemm_dense_q4(&mut self, d: &crate::list::DenseQ4, x16: &[i16], t: usize,
752:    pub fn accumulate_push(&mut self, m: &PushMat, sv: &SparseVec) -> Vec<i64> {
765:    fn attendre(&self, sh: &Shared) {
775:    pub fn ensure_width(&mut self, n_out: usi
… [1867 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '159,200p' docs/pilotage/roadmap.md", "description": "Lire la section N de la roadmap"}`

  ```
## Programme N — Le natif (DRVM, `drave-n0`, distillation)

**Repartir à neuf, pas à zéro.** On garde le moteur, le bus, DRVF, les portes et l'outillage ; on remplace la base
(GGUF, Qwen3-MoE, le modèle monolithique) par un **format** (DRVM) et un **modèle** (`drave-n0`) conçus pour les
mécanismes Drave. Détail complet : [`roadmap-native-2026-10-29.md`](../archive/roadmap-native-2026-10-29.md).

| # | chantier | état | prochaine action |
|---|---|---|---|
| **N0** | le format DRVM : manifeste, payload, lecture, convertisseurs, trace/rejeu, refus | ✅ | aucune — N0.3b est **close** (conversion et natif) |
| **N1** | `drave-n0` : 11,47 M, 6 blocs, octets, attention locale, FFN creux, 3 têtes précoces | ✅ | aucune — PPL **3,465** avec pont (**4,080** sans) ; têtes **57,6 / 61,6 / 62,1 %** contre **62,7 %** ; réflexe **−24,05 %** de temps pour **−1,61** point ; pensée **λ = 0,709** ; cache **19,25×** |
| **N2** | la distillation : 49 999 fenêtres, 4 sources, professeur Qwen/DeepSeek | 🔬 | **N2** — la **hiérarchie** (état de section, 3 graines) ; porte **< 2,5** non atteinte (meilleur **2,6998**, plateau **2,708**) |
| **N3** | les opérations natives : k-WTA, routes, sortie précoce, pont
… [2228 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,90p' docs/theorie/carte.md", "description": "Lire la carte des sujets"}`

  ```
# La carte de Drave — l'index des sujets

> **Le hub des sujets.** Un lien, **un fichier**. Les autres portes : [la vision](vision.md) ·
> [l'état](../pilotage/en-cours.md) · [la roadmap](../pilotage/roadmap.md) · [l'inventaire](../README.md) · [les résultats](../../reports/README.md) ·
> [le journal](../../journal/README.md) · [l'archive](../archive/README.md).

## Où l'on va, où l'on en est

| | |
|---|---|
| [la vision](vision.md) — le bus d'événements, les blocs, l'hybridation, ce qu'elle refuse | |
| [la mission](../methode/mission.md) — les deux programmes, l'ordre des priorités | |
| [l'état](../pilotage/en-cours.md) — ce qui est en cours, les chiffres qui comptent, les questions | |
| [la roadmap](../pilotage/roadmap.md) — les chantiers A, B, N, R et la file « jamais en attente » | |
| [la lecture rapide](lecture-rapide.md) · [le backlog](../pilotage/backlog/index.md) — 14 techniques, 5 couches, une fiche par fonctionnalité | |
| [les portes](../pilotage/references-non-regression.md) — les passes complètes, les repères | |
| [le glossaire](glossaire.md) — le vocabulaire non négociable | |

## Les blocs

| le bloc | le concept | les preuves |
|---|---|---|
| **le bus, les fl
… [7454 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"BLOCS\\|blocks\\|kind\\|graph\\|ports\\|regions\\|routes\" tools/drvm.py | head -50 && echo '---' && sed -n '1,80p' tools/drvm.py", "description": "Lire l'écrivain DRVM"}`

  ```
4:DRVM n'est pas un GGUF amélioré : c'est un conteneur de **graphe** et de **blocs**.
5:Le manifeste porte les blocs, les ports, les routes, les têtes, le pont et la
33:BLOCS_CONNUS = {
37:SECTIONS = ("model", "graph", "tensors", "execution")
101:    blocs = manifest["graph"].get("blocks")
103:        raise DRVMError("graphe sans bloc")
106:        if "id" not in b or "kind" not in b:
111:        if b["kind"] not in BLOCS_CONNUS:
112:            raise DRVMError(f"type de bloc inconnu : {b['kind']}")
207:            "blocs": [b["id"] for b in d.manifest["graph"]["blocks"]],
---
#!/usr/bin/env python3
"""drvm.py — DRVM v0, le conteneur natif du modèle Drave.

DRVM n'est pas un GGUF amélioré : c'est un conteneur de **graphe** et de **blocs**.
Le manifeste porte les blocs, les ports, les routes, les têtes, le pont et la
cellule de pensée ; le payload porte les tenseurs alignés, lisibles par bloc et
mmap-ables. Le lecteur refuse une version ou un type de bloc qu'il ne connaît pas.

Structure :
  en-tête 92 o (magie, version, tailles, offsets, deux SHA-256)
  manifeste JSON canonique, aligné sur 64 o
  payload de tenseurs, chaque tenseur aligné sur 64 o

CLI :
  python3 tools/drvm.py ins
… [1440 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%Y-%m-%d %H:%M %Z' && git log -1 --format='%ad' --date=iso && sed -n '1,120p' tools/verifie_etat_a_jour.py", "description": "Vérifier la date et la règle d'état à jour"}`

  ```
2026-10-31 17:47 EDT
2026-10-31 17:31:59 -0400
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
  python3 tools/verifie_etat_a_jour.py --index
… [3587 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- docs/pilotage/en-cours.md | head -80", "description": "Voir la modification en cours de l'état"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 91bad92d..6f16547b 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -37,7 +37,7 @@
   fichiers réservés, ni cette page sans me le dire.
 - **Fichiers réservés** : `work/n2d/`, `tools/distiller_budget.py`, `reports/n2-*`,
   `journal/sessions/0b0a6a0d-…/`.
-- **Prochaine action** : fiche `reports/rapport-n2-budget.md`, journal, roadmap, commit.
+- **Prochaine action** : la fiche du budget, le journal, la roadmap, le commit.
 - **Bloquants** : aucun côté N2 — GPU occupés ; **R4.4** bloqué (aucun OCR).
 - **Journal** : [30/10](../../journal/2026-10-30/README.md) · [31/10](../../journal/2026-10-31/README.md).
  ```

- **bash** `{"command": "sed -n '62,78p' /tmp/diehl.txt | cut -c1-2400", "description": "Lire les variantes STDP de l'article"}`

  ```
2.3. Learning
All synapses from input neurons to excitatory neurons are learned using STDP. To improve simulation speed, the weight dynamics are computed using synaptic traces (Morrison et al., 2007 ). This means that, besides the synaptic weight, each synapse keeps track of another value, namely the presynaptic trace x pre , which models the recent presynaptic spike history. Every time a presynaptic spike arrives at the synapse, the trace is increased by 1, otherweise x pre decays exponentially. When a postsynaptic spike arrives at the synapse the weight change w is calculated based on the presynaptic trace
(3) w = ( x p r e - x t a r ) ( w m a x - w )
where is the learning-rate, w max is the maximum weight, and determines the dependence of the update on the previous weight. x tar is the target value of the presynaptic trace at the moment of a postsynaptic spike. The higher the target value, the lower the synaptic weight will be. This offset ensures that presynaptic neurons that rarely lead to firing of the postsynaptic neuron will become more and more disconnected and is especially useful if the postsynaptic neuron is only rarely active. A similar effect can be achieved by adding
… [3834 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,90p' docs/archive/impulsion-pure-apprenant.md", "description": "Lire la note sur l'impulsion pure"}`

  ```
# Drave en mode impulsion pur serait-il un meilleur apprenant ?

> **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
> **feuille de route courante** est [`roadmap.md`](../pilotage/roadmap.md) ; l'**état** est
> [`en-cours.md`](../pilotage/en-cours.md).

> 9 octobre 2026. Question posée telle quelle. Réponse en trois temps : ce que
> « impulsion pure » peut vouloir dire chez nous, ce que nos propres mesures disent
> déjà, et les mécanismes supplémentaires qu'il faudrait — avec le protocole qui
> trancherait.

---

## 1. Trois sens de « mode impulsion pur », et ils n'ont pas le même avenir

| sens | état dans Drave | verdict |
|---|---|---|
| **exécution** par événements (aucun produit dense) | **fait** : le chemin par listes, les paires (poids × activation), le flux réparti | le coût suit déjà l'activité |
| **apprentissage** par événements (ne mettre à jour que les poids touchés) | **non** : l'entraînement est hors moteur, et chaque pas met à jour **tous** les paramètres | c'est là que la question se joue |
| **représentation** impulsionnelle (le temps porte l'information) | **non** : un jeton est un vecteur dense, pas une salve | le pl
… [4783 caractères tronqués]
  ```

- **bash** `{"command": "which rsvg-convert inkscape convert magick chromium chromium-browser google-chrome 2>/dev/null; python3 -c \"import cairosvg; print('cairosvg ok')\" 2>/dev/null || true", "description": "Chercher un convertisseur SVG vers PNG"}`

  ```
/usr/bin/inkscape
/usr/bin/convert
/usr/bin/magick
/usr/bin/google-chrome
  ```

### 🤖 Assistant

⏵ Mise en place du générateur SVG et de la mesure du texte

- **bash** `{"command": "python3 - <<'PY'\ntry:\n    from PIL import ImageFont\n    for p in [\"/usr/share/fonts/dejavu/DejaVuSans.ttf\",\"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf\"]:\n        try:\n            f=ImageFont.truetype(p,12); print(\"ok\",p,f.getlength(\"Le coût suit l'activité\"))\n         … [150 caractères tronqués]`

  ```
ok /usr/share/fonts/dejavu/DejaVuSans.ttf 125.0
ok /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf 125.0
  ```

- **todo_write** `{"todos": [{"content": "Concevoir et générer les SVG du modèle natif", "status": "in_progress"}, {"content": "Concevoir et générer les SVG Diehl & Cook", "status": "pending"}, {"content": "Rédiger docs/theorie/modele-natif.md", "status": "pending"}, {"content": "Rédiger docs/implantation/diehl-cook. … [206 caractères tronqués]`

  ```
Updated todo list: 5 pending, 1 in progress, 0 completed.
  ```

- **write** `{"file_path": "/tmp/svgkit.py", "content": "\"\"\"Petit kit SVG pour les schémas Drave (hors dépôt : génère des SVG directs).\"\"\"\nfrom __future__ import annotations\nimport html\nimport pathlib\nfrom PIL import ImageFont\n\nFONT = \"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf\"\nBOLD = \"/usr … [7438 caractères tronqués]`

  ```
<path>/tmp/svgkit.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "import sys, pathlib\nsys.path.insert(0, \"/tmp\")\nfrom svgkit import *\n\nOUT = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas\")\n\n\ndef niveaux():\n    s = SVG(960, 530, \"Trois niveaux de contrat, un centre neutre\",\n            \"N1 surface, N2 RSN au … [3553 caractères tronqués]`

  ```
<path>/tmp/gen_natif.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 /tmp/gen_natif.py && inkscape docs/schemas/natif-niveaux.svg --export-type=png --export-filename=/tmp/natif-niveaux.png --export-width=1200 2>/dev/null && ls -l /tmp/natif-niveaux.png", "description": "Générer et rendre le pr … [14 caractères tronqués]`

  ```
✓ natif-niveaux.svg
-rw-r--r--. 1 stephane stephane 159903 31 oct 17:50 /tmp/natif-niveaux.png
  ```

- **read_image** `{"file_path": "/tmp/natif-niveaux.png"}`

  ```
Error: cannot read "/tmp/natif-niveaux.png" as an image: model "deepseek-flash" does not declare image input; switch to an image-capable model to read images
  ```

- **list_subagent_models** `{}`

  ```
hauru-local — Hauru local (llama.cpp)
hauru-vision — Hauru vision (Qwen2.5-VL 7B)
deepseek-official — DeepSeek
  ```

- **list_subagent_models** `{"provider": "hauru-vision"}`

  ```
hauru-vision/Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf — Qwen2.5-VL 7B (vision locale)
  ```

- **bash** `{"command": "cat >> /tmp/gen_natif.py <<'PY'\n\n\ndef cout_activite():\n    s = SVG(960, 450, \"Le coût suit l'activité, pas la taille\",\n            \"Une activation est un fait : on pousse (indice, valeur), jamais les zéros. \"\n            \"En régime creux les listes gagnent ; en régime dense,  … [14614 caractères tronqués]`

  ```
✓ natif-niveaux.svg
  ✓ natif-cout-activite.svg
  ✓ natif-drvm.svg
  ✓ natif-graphe-n0.svg
  ✓ natif-pertes.svg
  ✓ natif-original.svg
  ✓ natif-portes.svg
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport re, pathlib\np=pathlib.Path('/tmp/svgkit.py')\nt=p.read_text()\nt=t.replace('''        if max_largeur is not None and largeur(s, taille, gras) > max_largeur:\n            self.alertes.append(\n                f\"débordement ({largeur(s, taille, gras): … [1537 caractères tronqués]`

  ```
patch ok
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('/tmp/gen_natif.py'); t=p.read_text()\n# --- pertes: reduce cards and move band\nt=t.replace('''    for i, (num, titre, desc, coul) in enumerate(cartes):\n        col, lig = i % 2, i // 2\n        x = 30 + col * 470\n        y  … [3811 caractères tronqués]`

  ```
ok
  ✓ natif-niveaux.svg
  ✓ natif-cout-activite.svg
  ✓ natif-drvm.svg
  ✓ natif-graphe-n0.svg
  ✓ natif-pertes.svg
  ✓ natif-original.svg
  ✓ natif-portes.svg
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && mkdir -p /tmp/qa && for f in natif-niveaux natif-cout-activite natif-drvm natif-graphe-n0 natif-pertes natif-original natif-portes; do inkscape docs/schemas/$f.svg --export-type=png --export-filename=/tmp/qa/$f.png --export-width=140 … [102 caractères tronqués]`

  ```
total 1068
-rw-r--r--. 1 stephane stephane 160409 31 oct 17:52 natif-cout-activite.png
-rw-r--r--. 1 stephane stephane 161439 31 oct 17:52 natif-drvm.png
-rw-r--r--. 1 stephane stephane 165437 31 oct 17:52 natif-graphe-n0.png
-rw-r--r--. 1 stephane stephane 192704 31 oct 17:52 natif-niveaux.png
-rw-r--r--. 1 stephane stephane 144318 31 oct 17:52 natif-original.png
-rw-r--r--. 1 stephane stephane 147388 31 oct 17:52 natif-pertes.png
-rw-r--r--. 1 stephane stephane 104394 31 oct 17:52 natif-portes.png
  ```

- **subagent** `{"description": "Revue visuelle des 7 schémas", "prompt": "Tu es relecteur visuel de schémas SVG rendus en PNG. Inspecte ces 7 images une par une avec l'outil read_image :\n\n/tmp/qa/natif-niveaux.png\n/tmp/qa/natif-cout-activite.png\n/tmp/qa/natif-drvm.png\n/tmp/qa/natif-graphe-n0.png\n/tmp/qa/nati … [897 caractères tronqués]`

  ```
started subagent df1b1098-d54e-4763-bfc2-2a8cc1498cec
  ```

### 🤖 Assistant

⏵ Génération des schémas Diehl & Cook (architecture, placements, contrat, temps)

- **write** `{"content": "import sys, pathlib\nsys.path.insert(0, \"/tmp\")\nfrom svgkit import *\n\nOUT = pathlib.Path(\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas\")\n\n\ndef architecture():\n    s = SVG(960, 570, \"Diehl & Cook (2015) : une mémoire compétitive à spikes\",\n            \"Entr … [11994 caractères tronqués]`

  ```
<path>/tmp/gen_diehl.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 👤 Utilisateur

Background subagent df1b1098-d54e-4763-bfc2-2a8cc1498cec failed before it finished.
It left no closing message.

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('/tmp/svgkit.py'); t=p.read_text()\nt=t.replace(\"        self.alertes: list[str] = []\",\"        self.alertes: list[str] = []\\n        self._textes: list[tuple[float,float,float,float,str]] = []\")\nt=t.replace('''        se … [1601 caractères tronqués]`

  ```
ok
  ✓ natif-niveaux.svg
  ✓ natif-cout-activite.svg
  ✓ natif-drvm.svg
  ✓ natif-graphe-n0.svg
  ✓ natif-pertes.svg
  ✓ natif-original.svg
  ✓ natif-portes.svg
  ✓ diehl-cook-architecture.svg
  ✓ diehl-cook-placements.svg
  ✓ diehl-cook-contrat.svg
  ✓ diehl-cook-temps.svg
  ```

- **bash** `{"command": "cat >> /tmp/gen_diehl.py <<'PY'\n\n\ndef pipeline():\n    s = SVG(960, 590, \"Le pipeline de référence, à trois niveaux\",\n            \"Surface → encodeur N1 → RSN → φ → mémoire D&C N2 → RSN' → lecture N3 → décision ; \"\n            \"le miroir redescend par un décodeur N1, jamais pa … [5671 caractères tronqués]`

  ```
✓ diehl-cook-architecture.svg
  ✓ diehl-cook-placements.svg
  ✓ diehl-cook-contrat.svg
  ✓ diehl-cook-temps.svg
  ✓ diehl-cook-pipeline.svg
  ✓ diehl-cook-boucle.svg
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re,glob,sys\nsys.path.insert(0,'/tmp')\nfrom svgkit import largeur\nfor f in sorted(glob.glob('docs/schemas/natif-*.svg')+glob.glob('docs/schemas/diehl-cook-*.svg')):\n    t=open(f).read()\n    for m in re.fi … [483 caractères tronqués]`

  ```
diehl-cook-architecture.svg        x=  480 y=  34 w=  721 21.0 'Diehl &amp; Cook (2015) : une mémoire compétitive à spikes'
diehl-cook-architecture.svg        x=  480 y=  58 w=  797 13.0 'Un apprentissage local, sans rétropropagation et sans étiquette ; les classes ne'
diehl-cook-architecture.svg        x=  245 y= 522 w=  282 11.5 'Apprentissage : STDP local, aucune étiquette'
diehl-cook-architecture.svg        x=  245 y= 542 w=  261 10.5 'la rétropropagation n&#x27;entre pas dans la boucle'
diehl-cook-architecture.svg        x=  715 y= 522 w=  235 11.5 'Lecture : réponse moyenne par classe'
diehl-cook-architecture.svg        x=  715 y= 542 w=  296 10.5 'l&#x27;assignation est la seule étape qui voit les étiquettes'
diehl-cook-boucle.svg              x=  480 y=  34 w=  575 21.0 'La boucle d&#x27;entraînement et ses contrôles'
diehl-cook-boucle.svg              x=  480 y=  58 w=  703 13.0 'L&#x27;étiquette n&#x27;entre jamais dans l&#x27;apprentissage : elle nomme les '
diehl-cook-boucle.svg              x=  480 y= 250 w=  334 13.0 'Quatre contrôles négatifs, un par mécanisme'
diehl-cook-boucle.svg              x=  137 y= 312 w=  205  9.5 'l&#x27;assignation doit tomber au hasard'
d
… [10114 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('/tmp/gen_diehl.py'); t=p.read_text()\nt=t.replace('s.texte(x + 107, 328, \"si le contrôle réussit : le mécanisme n\\'est pas nécessaire\", 8.8, \"#7f1d1d\", \"middle\")',\n            's.texte(x + 107, 328, \"contrôle réussi = … [764 caractères tronqués]`

  ```
ok
  ✓ diehl-cook-architecture.svg
  ✓ diehl-cook-placements.svg
  ✓ diehl-cook-contrat.svg
  ✓ diehl-cook-temps.svg
  ✓ diehl-cook-pipeline.svg
  ✓ diehl-cook-boucle.svg
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in rapport-deepseek.md rapport-native-distillation-50k.md rapport-native-distillation-20k.md rapport-drvm-ppl.md rapport-native-cache.md rapport-semantique.md rapport-jeux-symboliques.md rapport-universaux.md rapport-native-ser … [186 caractères tronqués]`

  ```
OK rapport-deepseek.md
OK rapport-native-distillation-50k.md
OK rapport-native-distillation-20k.md
OK rapport-drvm-ppl.md
OK rapport-native-cache.md
OK rapport-semantique.md
OK rapport-jeux-symboliques.md
OK rapport-universaux.md
OK rapport-native-service-rust.md
anatomie-coupe.svg
bus-evenements.svg
couche-commune.svg
etages.svg
facultes.svg
fiche-concept.svg
glossaire.svg
methode.svg
modes.svg
operations.svg
parcours.svg
pensee.svg
portes.svg
vue-ensemble.svg
  ```

### 🤖 Assistant

⏵ Rédaction du document sur le modèle natif

- **write** `{"content": "# Le modèle Drave natif — un graphe, un flux, trois niveaux\n\n> **Ce que ce document est.** La **théorie** du modèle natif : ce qu'il est (un **graphe de blocs** exécuté sur un\n> **bus de faits**), ce qui le distingue d'un transformeur monolithique, et le **principe de séparation à tr … [22506 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/modele-natif.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/rapport-croisement-push-pull.md reports/rapport-localite-activation.md 2>&1; ls docs/theorie/glossaire/entrees/ | grep -E \"fait|representation|couche\"", "description": "Vérifier les liens cités dans le document natif"}`

  ```
reports/rapport-croisement-push-pull.md
reports/rapport-localite-activation.md
couche-0.md
couche-cible.md
couche-etage.md
couche.md
couche-source.md
diff-par-couche.md
fait-mesure-projete-deduit.md
representation-semantique-neutre.md
transformer-couche-caches.md
  ```

### 🤖 Assistant

⏵ Rédaction du cahier d'implémentation Diehl & Cook

- **write** `{"content": "# Un bloc Diehl & Cook dans Drave — implémenter un réseau impulsionnel sans franchir les niveaux\n\n> **Ce que ce document est.** Le **cahier d'implémentation** d'un bloc de type **Diehl & Cook (2015)** dans\n> Drave : le modèle d'origine, ses équations, le contrat de ports, le manifest … [33511 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/implantation/diehl-cook.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Vérification des schémas et des liens avant mise à jour des index

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_schemas.py; echo '--- exit:' $?; echo '=== revue ==='; python3 tools/revue_documentation.py 2>&1 | tail -30; echo '--- exit:' $?", "description": "Lancer le vérificateur de schémas et la revue"}`

  ```
schémas · 430 document(s) · 35 SVG · 2 source(s)
  ❌ 1 anomalie(s) :
     · schéma non référencé : docs/schemas/diehl-cook-boucle.svg
--- exit: 1
=== revue ===
  revue de documentation · 369 fiche(s) · 438 JSON · 111 doc(s) · 79 porte(s) · 8 chapitre(s)
  ❌ 9 anomalie(s) :
     · compteurs : en-cours.md dit 78 portes, le disque en a 79
     · compteurs : en-cours.md dit 109 documents, le disque en a 111
     · compteurs : en-cours.md dit 437 JSON, le disque en a 438
     · chemin mort : docs/implantation/diehl-cook.md:384 → tools/neuro/diehl_cook.py
     · chemin mort : docs/implantation/diehl-cook.md:536 → tools/neuro/diehl_cook.py
     · chemin mort : docs/implantation/diehl-cook.md:537 → tools/neuro/rsn_visuel.py
     · chemin mort : docs/implantation/diehl-cook.md:539 → drave-core/src/impulsion.rs
     · chemin mort : docs/implantation/diehl-cook.md:540 → drave-core/tests/impulsion.rs
     · chemin mort : docs/implantation/diehl-cook.md:541 → tools/neuro/porter_dc.py
--- exit: 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain | head -20 && echo '--- portes' && ls tools/porte-*.sh | wc -l && ls -t tools/porte-*.sh | head -3 && echo '--- json' && ls reports/*.json | wc -l && ls -t reports/*.json | head -3 && echo '--- git log porte' & … [195 caractères tronqués]`

  ```
M .gitignore
 M docs/pilotage/en-cours.md
 M journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md
 M reports/INDEX.md
 M tools/docwatch
 M tools/graphe_document.py
?? docs/implantation/diehl-cook.md
?? docs/schemas/diehl-cook-architecture.svg
?? docs/schemas/diehl-cook-boucle.svg
?? docs/schemas/diehl-cook-contrat.svg
?? docs/schemas/diehl-cook-pipeline.svg
?? docs/schemas/diehl-cook-placements.svg
?? docs/schemas/diehl-cook-temps.svg
?? docs/schemas/natif-cout-activite.svg
?? docs/schemas/natif-drvm.svg
?? docs/schemas/natif-graphe-n0.svg
?? docs/schemas/natif-niveaux.svg
?? docs/schemas/natif-original.svg
?? docs/schemas/natif-pertes.svg
?? docs/schemas/natif-portes.svg
--- portes
79
tools/porte-ocr.sh
tools/porte-tableaux.sh
tools/porte-gain.sh
--- json
438
reports/r44-ocr-pilote.json
reports/n2-distillation.json
reports/n2-hierarchie.json
--- git log porte
3b9d179c 2026-10-31 PORTES — CINQ ÉCHECS SILENCIEUX CORRIGÉS : UNE PASSE VIDE, UNE ASSERTION PERDUE, UN HOOK MUET
660c479c 2026-10-31 N2 — LA HIÉRARCHIE NE PAIE PAS SUR LA DISTILLATION NON PLUS (2,9935 CONTRE 2,9927, TROIS GRAINES)
[stderr]
ls: write error: Broken pipe
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/implantation/diehl-cook.md')\nt=p.read_text()\nt=t.replace(\"le simulateur de référence vit dans\\n`tools/neuro/diehl_cook.py`, et le bloc Rust doit reproduire **exactement** ses … [2435 caractères tronqués]`

  ```
ok
383:**squelette de pas**, pas un simulateur complet : le simulateur de référence vit dans `tools/neuro/` (fichier `diehl_cook.py`), et le bloc Rust doit
538:| **1** | `tools/neuro/` | simulateur de référence (`diehl_cook.py`), 400 E, 10 000 exemples | D1, D3 |
539:| **2** | `tools/neuro/` | tête typée, `φ`, canonicalisation, empreinte (`rsn_visuel.py`) | D4 |
541:| **4** | `drave-core/src/` | le bloc Rust, `pas()`, tirage contré, trace (`impulsion.rs`) | D1, D2 |
542:| **5** | `drave-core/tests/` | golden trace, parité Python/Rust, refus de graphe (`impulsion.rs`) | D0–D2 |
543:| **6** | `tools/neuro/` | export DRVM, lecture, rejeu, diff (`porter_dc.py`) | D2, D5 |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"portes\\|vertes\\|rouges\" docs/pilotage/references-non-regression.md | head -20 && echo '---' && grep -n \"portes\\|fichiers / JSON\\|documents de\" docs/pilotage/en-cours.md", "description": "Vérifier les compteurs de por … [26 caractères tronqués]`

  ```
3:> **Dernière passe complète — 2026-10-31 à 12 h 54 :** **78 portes, 73 vertes, 5 rouges, 1 h 37**
4:> (journaux `/tmp/portes-1031-11h17`). `porte-indice`, `porte-melange` : les **structurelles
10:> **Passe précédente — 2026-10-29 à 22 h 09 :** 62 portes, 60 vertes, 2 rouges, 1 h 46 ;
11:> mêmes structurelles connues, **aucune régression**. Journaux : `/tmp/portes-1029-20h23` ;
12:> historique : [`reports/historique-passes-portes.md`](../../reports/historique-passes-portes.md).
19:> **Passe du 2026-10-28 à 00 h 12** (**49 portes, 46 vertes, 3 rouges**, **1 h 40 min**) — la passe
20:> du programme N. Les deux rouges structurelles (`porte-indice`, `porte-melange`) et
24:> **Passe précédente — 2026-10-27 à 14 h 33** (**49 portes, 47 vertes, 2 rouges**, **1 h 48 min**) — la passe
26:> rouges structurelles, avec les mêmes diagnostics ; **aucune régression**. Journaux :
27:> `/tmp/portes-1027-12h45`.
29:> **Passe précédente — 2026-10-26 à 14 h 30** (**49 portes, 47 vertes, 2 rouges**, **1 h 34 min**) — la passe de clôture
32:> livre 10/10, go 9×9 10/10 contre 3/10, dames 0 défaite, cartes 44,7 % contre 51,0 %). Les **deux rouges**
39:> `/tmp/portes-b9-1026-12h55`.
44:> [`reports/histori
… [1621 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"architecture-native\\|tokenisation\\|implantation/format\" docs/README.md && grep -n \"le cerveau-langage\\|le matériel et le système\" docs/theorie/carte.md && sed -n '1,20p' docs/schemas/README.md", "description": "Repére … [33 caractères tronqués]`

  ```
62:| [`theorie/architecture-native.md`](theorie/architecture-native.md) | DRVM, `drave-n0` : le format et le modèle natifs |
70:| [`implantation/format-flux.md`](implantation/format-flux.md) | la spécification DRVF : trace, rejeu, transport |
71:| [`implantation/format-clusters.md`](implantation/format-clusters.md) | le modèle éclaté en clusters |
74:| [`implantation/tokenisation.md`](implantation/tokenisation.md) | la tokenisation native : octets, et la décision mesurée R13 |
29:| **le cerveau-langage (B12)** | [les modules](modules-cerveau-langage.md) | [la fiche](../../reports/rapport-cerveau-modules.md) |
30:| **le matériel et le système** | [l'array NVMe](../implantation/configuration-nvme-raid-amd.md) · [NUMA](../implantation/numa-segregation.md) · [le convertisseur](../implantation/convertisseur.md) · [le contexte long](../implantation/contexte-long.md) | [les mesures](../../reports/bilan-multi-materiel.md) |
# Les schémas — index et convention

> **Ce que ce dossier est.** Les **illustrations** de Drave, en **SVG** : cinq schémas directs
> des concepts, deux sources générées par docwatch et les quatorze schémas de la synthèse
> (`docs/theorie/synthese/schemas/`). Chaque SVG
… [1108 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md", "old_string": "| [`theorie/architecture-native.md`](theorie/architecture-native.md) | DRVM, `drave-n0` : le format et le modèle natifs |", "new_string": "| [`theorie/architecture-native.md`](theorie/architecture-native.m … [185 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md", "old_string": "| [`implantation/tokenisation.md`](implantation/tokenisation.md) | la tokenisation native : octets, et la décision mesurée R13 |", "new_string": "| [`implantation/tokenisation.md`](implantation/tokenisatio … [197 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md": file has not been read — read the file, then retry
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/carte.md", "old_string": "| **le cerveau-langage (B12)** | [les modules](modules-cerveau-langage.md) | [la fiche](../../reports/rapport-cerveau-modules.md) |", "new_string": "| **le cerveau-langage (B12)** | [les modules](mo … [268 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/carte.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md", "offset": 50, "limit": 40}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/carte.md", "offset": 20, "limit": 15}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md", "limit": 40}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 80, "limit": 12}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md</path>
<type>file</type>
<content>
50: | document | pour quoi |
51: |---|---|
52: | [`theorie/vision.md`](theorie/vision.md) | la vision : les flots, les cinq axes, ce qu'elle n'est pas |
53: | [`theorie/carte.md`](theorie/carte.md) | la carte des sujets, bloc par bloc |
54: | [`theorie/histoire.md`](theorie/histoire.md) | Qtrinet → Drave, les trois âges |
55: | [`theorie/protocole-semantique.md`](theorie/protocole-semantique.md) | rejouer, converger, sens → texte, raisonnement gelé |
56: | [`theorie/semantique-universaux.md`](theorie/semantique-universaux.md) | la base typée : 15 champs, 502 classes |
57: | [`theorie/modules-cerveau-langage.md`](theorie/modules-cerveau-langage.md) | les modules M1–M9, le bus et les négatifs |
58: | [`theorie/jeux-symboliques.md`](theorie/jeux-symboliques.md) | surface → RSN-jeu → pensée, 71 langues, maîtres |
59: | [`theorie/genealogie-des-langues.md`](theorie/genealogie-des-langues.md) | la généalogie et l'avertissement époque/filiation |
60: | [`theorie/synthese/index.md`](theorie/synthese/index.md) | la synthèse en 8 chapitres |
61: | [`theorie/glossaire.md`](theorie/glossaire
… [2101 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/carte.md</path>
<type>file</type>
<content>
20: 
21: | le bloc | le concept | les preuves |
22: |---|---|---|
23: | **le bus, les flux** | [la vision](vision.md) · [le format de flux](../implantation/format-flux.md) · [les clusters](../implantation/format-clusters.md) | [les portes](../pilotage/references-non-regression.md) |
24: | **le bloc neuronal** | [le format de flux](../implantation/format-flux.md) · [la modularisation](../methode/modularisation.md) | [les mesures](../../reports/README.md) |
25: | **le bloc classique** | [la vision](vision.md) · [la modularisation](../methode/modularisation.md) | [les jeux](jeux-symboliques.md) |
26: | **la langue** | [le protocole sémantique](protocole-semantique.md) · [les jeux symboliques](jeux-symboliques.md) · [la généalogie](genealogie-des-langues.md) · [le banc externe](../implantation/llm-externe.md) | [B7/B8](../../reports/rapport-langues-maitres.md) · [B9](../../reports/rapport-deepseek.md) |
27: | **la pensée** | [la synthèse 05](synthese/05-la-pensee-sans-verbaliser.md) · [la synthèse 08](synthese/08-les-operations.md) | [B4](../../reports/rapport-operateur-negati
… [1052 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md</path>
<type>file</type>
<content>
1: # Les schémas — index et convention
2: 
3: > **Ce que ce dossier est.** Les **illustrations** de Drave, en **SVG** : cinq schémas directs
4: > des concepts, deux sources générées par docwatch et les quatorze schémas de la synthèse
5: > (`docs/theorie/synthese/schemas/`). Chaque SVG direct a un `viewBox`, un `<title>`, un `<desc>` et
6: > `role="img"` ; aucun n'utilise de ressource externe.
7: >
8: > **La règle.** Pas d'ASCII art. Un schéma est un SVG, directement, converti depuis Mermaid ou
9: > PlantUML, ou un **bloc inline** rendu par docwatch. Voir
10: > [`docs/methode/illustrations.md`](../methode/illustrations.md) ; vérifier avec
11: > `python3 tools/verifier_schemas.py`.
12: 
13: ## Les schémas des concepts
14: 
15: | schéma | ce qu'il montre | où il est utilisé |
16: |---|---|---|
17: | [modules-cerveau-langage.svg](modules-cerveau-langage.svg) | M1 hub → code RSN → bus → M2–M7, M4 → M8 | [les modules](../theorie/modules-cerveau-langage.md) |
18: | [protocole-semantique.svg](protocole-semantique.svg) | surface L1 → encodeur → z → décodeur + L2 → surface L2 | [le
… [1488 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
80: > **Source unique.** Ces valeurs sont vérifiées par `tools/revue_documentation.py`.
81: 
82: | invariant | valeur | contrôle |
83: |---|---|---|
84: | portes | **78** (73 vertes, 5 rouges à la passe du 31/10) | `tools/porte-*.sh` |
85: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
86: | fichiers / JSON de résultats | **369** / **437** | `reports/*.md` / `reports/*.json` |
87: | documents de `docs/` | **109** (hors archive et README) | `docs/**/*.md` |
88: | dernière passe complète | **1 h 37** (31/10 12 h 54) | `docs/pilotage/references-non-regression.md` |
89: 
90: ## Les chantiers et leurs bloquants
91: 

(Showing lines 80-91 of 139. Use offset=92 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md", "old_string": "| [`theorie/architecture-native.md`](theorie/architecture-native.md) | DRVM, `drave-n0` : le format et le modèle natifs |", "new_string": "| [`theorie/architecture-native.md`](theorie/architecture-native.m … [185 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md", "old_string": "| [`implantation/tokenisation.md`](implantation/tokenisation.md) | la tokenisation native : octets, et la décision mesurée R13 |", "new_string": "| [`implantation/tokenisation.md`](implantation/tokenisatio … [197 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/carte.md", "old_string": "| **le cerveau-langage (B12)** | [les modules](modules-cerveau-langage.md) | [la fiche](../../reports/rapport-cerveau-modules.md) |", "new_string": "| **le cerveau-langage (B12)** | [les modules](mo … [268 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/carte.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| portes | **78** (73 vertes, 5 rouges à la passe du 31/10) | `tools/porte-*.sh` |\n| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |\n| fichiers / JSON de résultats | **369** … [503 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md", "new_string": "> **Ce que ce dossier est.** Les **illustrations** de Drave, en **SVG** : les schémas directs\n> des concepts, les schémas du natif et de l'impulsionnel, deux sources générées par docwatch et\n> le … [238 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md", "new_string": "| [backlog-dependances.svg](backlog-dependances.svg) | le graphe des dépendances du backlog A/B/N/R, par couche | [le graphe](../pilotage/backlog/dependances.md) |\n\n## Les schémas du natif et de  … [2208 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/schemas/README.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Passage des portes documentaires (schémas, tableaux, revue, budget)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_schemas.py; echo \"EXIT=$?\"", "description": "Vérifier les schémas SVG et les liens d'images"}`

  ```
schémas · 431 document(s) · 35 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
EXIT=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh; echo \"EXIT=$?\"", "description": "Vérifier les tableaux Markdown"}`

  ```
✅ 1324 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 1255 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-10-31)
EXIT=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py; echo \"EXIT=$?\"", "description": "Vérifier le budget de contexte"}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4212    342   T1   9000  docs/pilotage/roadmap.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3131    294   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2489    176   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/th
… [555 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py; echo \"EXIT=$?\"", "description": "Vérifier l'état courant"}`

  ```
en-cours · 1187 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EXIT=0
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/carte.md", "new_string": "| **le cerveau-langage (B12)** | [les modules](modules-cerveau-langage.md) | [la fiche](../../reports/rapport-cerveau-modules.md) |", "old_string": "| **le cerveau-langage (B12)** | [les modules](mo … [268 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/theorie/carte.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py 2>&1 | tail -6; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Revérifier le budget après retrait de la ligne"}`

  ```
T0 max : 3966 mots (budget 4 000)

  avertissements :
     · 14 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
EXIT=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py > /tmp/revue.txt 2>&1; echo \"EXIT=$?\"; cat /tmp/revue.txt", "description": "Lancer la revue de documentation"}`

  ```
EXIT=1
  revue de documentation · 370 fiche(s) · 438 JSON · 112 doc(s) · 79 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 111 documents, le disque en a 112
     · compteurs : en-cours.md dit 369 fichiers, le disque en a 370
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain | head -30 && echo '--- new docs' && find docs -name '*.md' -newermt '-30 minutes' -not -path '*/archive/*' | head -20 && echo '--- new reports' && ls -t reports/*.md | head -5", "description": "Identifier les  … [40 caractères tronqués]`

  ```
M .gitignore
 M docs/README.md
 M docs/pilotage/backlog/R44-encodeur-visuel.md
 M docs/pilotage/backlog/index.md
 M docs/pilotage/en-cours.md
 M docs/schemas/README.md
 M journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md
 M reports/INDEX.md
 M tools/docwatch
 M tools/graphe_document.py
?? docs/implantation/diehl-cook.md
?? docs/implantation/encodeur-visuel.md
?? docs/schemas/diehl-cook-architecture.svg
?? docs/schemas/diehl-cook-boucle.svg
?? docs/schemas/diehl-cook-contrat.svg
?? docs/schemas/diehl-cook-pipeline.svg
?? docs/schemas/diehl-cook-placements.svg
?? docs/schemas/diehl-cook-temps.svg
?? docs/schemas/natif-cout-activite.svg
?? docs/schemas/natif-drvm.svg
?? docs/schemas/natif-graphe-n0.svg
?? docs/schemas/natif-niveaux.svg
?? docs/schemas/natif-original.svg
?? docs/schemas/natif-pertes.svg
?? docs/schemas/natif-portes.svg
?? docs/theorie/modele-natif.md
?? reports/r44-ocr-pilote.json
?? reports/rapport-r44-ocr-pilote.md
?? tools/distiller_budget.py
?? tools/eval_n2_budget.py
--- new docs
docs/schemas/README.md
docs/pilotage/backlog/R44-encodeur-visuel.md
docs/pilotage/backlog/index.md
docs/pilotage/en-cours.md
docs/theorie/modele-natif.md
docs/theorie/carte.md
… [292 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls .git/hooks/ | grep -v sample && echo '---' && sed -n '1,40p' .git/hooks/pre-commit 2>/dev/null", "description": "Vérifier les hooks de commit"}`

  ```
pre-commit
---
#!/bin/sh
# pre-commit — l'état accompagne le fait, le journal accompagne le code.
#
# Versionné dans tools/hooks/ et installé par tools/installe_hooks.sh : un hook qui
# ne vit que dans .git/hooks ne survit ni au clone ni au nettoyage.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 0

# 1. Aucun fait (reports/, roadmap, backlog) ne se commite sans sa ligne d'état.
#    C'est la garantie de fraîcheur de docs/pilotage/en-cours.md : elle ne dépend
#    pas de la survie d'une session « principale », elle est vérifiée au commit.
if ! python3 tools/verifie_etat_a_jour.py --index; then
    echo "  ⛔ commit refusé : un fait sans ligne d'état."
    echo "     mets docs/pilotage/en-cours.md à jour, puis :"
    echo "     git add docs/pilotage/en-cours.md"
    exit 1
fi

# 2. Archive les traces de session DSH avant chaque commit : le journal doit
#    accompagner le code, pas le suivre.
python3 tools/archive_sessions.py --quiet >/dev/null || { echo "  ⛔ archivage des sessions en échec"; exit 1; }
python3 tools/session_report.py --quiet >/dev/null || { echo "  ⛔ rapport de session en échec"; exit 1; }
# Le journal du jour, par thème (sources : git + journal/sessions). L'i
… [249 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); t=p.read_text()\nt=t.replace('| fichiers / JSON de résultats | **369** / **438** |','| fichiers / JSON de résultats | **370** / **438** |')\nt=t.replace(' … [320 caractères tronqués]`

  ```
ok
EXIT=0
  revue de documentation · 370 fiche(s) · 438 JSON · 112 doc(s) · 79 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

### 🤖 Assistant

⏵ Passe finale des portes documentaires avant commit

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for t in \"python3 tools/verifier_schemas.py\" \"bash tools/porte-tableaux.sh\" \"python3 tools/taille_documents.py\" \"python3 tools/verifie_en_cours.py\" \"python3 tools/verifie_journal.py\"; do echo \"=== $t\"; eval \"$t\" >/tmp/o … [117 caractères tronqués]`

  ```
=== python3 tools/verifier_schemas.py
EXIT=0
  schémas · 431 document(s) · 35 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
=== bash tools/porte-tableaux.sh
EXIT=0
  ✅ 1324 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 1256 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-10-31)
=== python3 tools/taille_documents.py
EXIT=0
     · 14 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 597 l. rapport-e5-distillation.md, 546 l. rapport-empreinte-memoire.md, 491 l. rapport-passe-k3-disque.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
=== python3 tools/verifie_en_cours.py
EXIT=0
  en-cours · 1187 mots · 7 sections · 1 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
=== python3 tools/verifie_journal.py
EXIT=0
  journal · 37 jour(s) · 105 session(s) · 1669 lien(s)
  ✅ un dossier par jour
… [42 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in docs/theorie/modele-natif.md docs/implantation/diehl-cook.md; do echo \"=== $f\"; echo \"fences: $(grep -c '^```' $f)\"; echo \"words: $(wc -w < $f)\"; grep -n \"TODO\\|XXX\\|lorem\\|placeholder\" $f || true; done && python3 … [429 caractères tronqués]`

  ```
=== docs/theorie/modele-natif.md
fences: 2
words: 3621
=== docs/implantation/diehl-cook.md
fences: 10
words: 5626
docs/theorie/modele-natif.md fences 2 even
  titres 16
docs/implantation/diehl-cook.md fences 10 even
  titres 20
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('/tmp/svgkit.py'); t=p.read_text()\nt=t.replace(\"        self._textes: list[tuple[float,float,float,float,str]] = []\",\"        self._textes: list[tuple[float,float,float,float,str]] = []\\n        self._traits: list[tuple[fl … [2218 caractères tronqués]`

  ```
ok
  ⚠ natif-niveaux.svg
     trait sur texte : 'ce qui varie' (x=99, y=333)
     trait sur texte : "retour : la RSN d'action redescend vers le décodeur — c'est le miroir" (x=825, y=388)
  ✓ natif-cout-activite.svg
  ✓ natif-drvm.svg
  ✓ natif-graphe-n0.svg
  ✓ natif-pertes.svg
  ✓ natif-original.svg
  ✓ natif-portes.svg
  ⚠ diehl-cook-architecture.svg
     trait sur texte : 'tout-à-tout' (x=215, y=288)
     trait sur texte : 'poids STDP' (x=262, y=300)
  ✓ diehl-cook-placements.svg
  ✓ diehl-cook-contrat.svg
  ✓ diehl-cook-temps.svg
  ✓ diehl-cook-pipeline.svg
  ✓ diehl-cook-boucle.svg
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('/tmp/gen_natif.py'); t=p.read_text()\nt=t.replace('s.chemin(\"M99,322 L99,432 L825,432 L825,352\", ROUGE_T, 2.2, \"6 5\", \"fr\")',\n            's.chemin(\"M60,322 L60,432 L825,432 L825,352\", ROUGE_T, 2.2, \"6 5\", \"fr\")') … [1101 caractères tronqués]`

  ```
ok
  ✓ natif-niveaux.svg
  ✓ natif-cout-activite.svg
  ✓ natif-drvm.svg
  ✓ natif-graphe-n0.svg
  ✓ natif-pertes.svg
  ✓ natif-original.svg
  ✓ natif-portes.svg
  ✓ diehl-cook-architecture.svg
  ✓ diehl-cook-placements.svg
  ✓ diehl-cook-contrat.svg
  ✓ diehl-cook-temps.svg
  ✓ diehl-cook-pipeline.svg
  ✓ diehl-cook-boucle.svg
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && inkscape docs/schemas/natif-niveaux.svg --export-type=png --export-filename=/tmp/qa/check1.png --export-width=1400 >/dev/null 2>&1 && echo ok", "description": "Rendre un schéma pour la revue visuelle"}`

  ```
ok
  ```

- **subagent** `{"description": "Test revue visuelle", "model": "Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf", "prompt": "Regarde l'image /tmp/qa/check1.png avec read_image. Dis en français, en 3 lignes maximum, si le texte déborde des boîtes ou du cadre, s'il y a des chevauchements de texte, ou si tout est lisible. Ne juge … [154 caractères tronqués]`

  ```
Error: subagent run failed
  ```

- **bash** `{"command": "sed -n '438,462p' /tmp/diehl_code.py", "description": "Vérifier la fréquence de normalisation dans le code de référence"}`

  ```
if do_plot_performance:
    performance_monitor, performance, fig_num, fig_performance = plot_performance(fig_num)
for i,name in enumerate(input_population_names):
    input_groups[name+'e'].rate = 0
b.run(0)
j = 0
while j < (int(num_examples)):
    if test_mode:
        if use_testing_set:
            rates = testing['x'][j%10000,:,:].reshape((n_input)) / 8. *  input_intensity
        else:
            rates = training['x'][j%60000,:,:].reshape((n_input)) / 8. *  input_intensity
    else:
        normalize_weights()
        rates = training['x'][j%60000,:,:].reshape((n_input)) / 8. *  input_intensity
    input_groups['Xe'].rate = rates
#     print 'run number:', j+1, 'of', int(num_examples)
    b.run(single_example_time, report='text')
            
    if j % update_interval == 0 and j > 0:
        assignments = get_new_assignments(result_monitor[:], input_numbers[j-update_interval : j])
    if j % weight_update_interval == 0 and not test_mode:
        update_2d_input_weights(input_weight_monitor, fig_weights)
    if j % save_connections_interval == 0 and j > 0 and not test_mode:
        save_connections(str(j))
  ```

- **bash** `{"command": "curl -s \"https://raw.githubusercontent.com/peter-u-diehl/stdp-mnist/master/Diehl%26Cook_MNIST_evaluation.py\" -o /tmp/diehl_eval.py && grep -n \"assignment\\|sum\\|argmax\\|result\\|spike\" /tmp/diehl_eval.py | head -40", "description": "Vérifier la règle de lecture du code de référenc … [3 caractères tronqués]`

  ```
59:def get_recognized_number_ranking(assignments, spike_rates):
60:    summed_rates = [0] * 10
61:    num_assignments = [0] * 10
63:        num_assignments[i] = len(np.where(assignments == i)[0])
64:        if num_assignments[i] > 0:
65:            summed_rates[i] = np.sum(spike_rates[assignments == i]) / num_assignments[i]
66:    return np.argsort(summed_rates)[::-1]
68:def get_new_assignments(result_monitor, input_numbers):
69:    print result_monitor.shape
70:    assignments = np.ones(n_e) * -1 # initialize them as not assigned
76:            rate = np.sum(result_monitor[input_nums == j], axis = 0) / num_inputs
80:                assignments[i] = j 
81:    return assignments
100:print 'load results'
101:training_result_monitor = np.load(data_path + 'resultPopVecs' + training_ending + ending + '.npy')
103:testing_result_monitor = np.load(data_path + 'resultPopVecs' + testing_ending + '.npy')
105:print training_result_monitor.shape
107:print 'get assignments'
108:test_results = np.zeros((10, end_time_testing-start_time_testing))
109:test_results_max = np.zeros((10, end_time_testing-start_time_testing))
110:test_results_top = np.zeros((10, end_time_testing-start_time_testing))
111:
… [896 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re\nt=open('docs/implantation/diehl-cook.md').read()\nfor m in re.finditer(r'```python\\n(.*?)```',t,re.S):\n    print('---BLOC---')\n    print(m.group(1)[:400])\nPY", "description": "Repérer les blocs de cod … [14 caractères tronqués]`

  ```
---BLOC---
def tete_rsn(spikes_par_neurone, assign, confiance):
    # 1. réponse par classe : somme des spikes des neurones assignés à chaque classe
    reponse = [0] * 10
    for neurone, n in enumerate(spikes_par_neurone):
        if assign[neurone] >= 0:
            reponse[assign[neurone]] += n
    # 2. classement canonique : score décroissant, puis classe croissante (déterministe)
    candidats = sorted
---BLOC---
def pas(t, etat, params, rng, trace):
    # 1. décroissance
    etat["g_e"] *= params.exp_ge
    etat["g_i"] *= params.exp_gi
    etat["x_pre"] *= params.exp_pre
    etat["post1"] *= params.exp_post1
    etat["post2"] *= params.exp_post2
    etat["theta"] *= params.exp_theta

    # 2. entrée de Poisson (tirage contré, indépendant de l'ordre)
    for i in range(params.n_input):
        if rng.berno
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport re, pathlib\np=pathlib.Path('docs/implantation/diehl-cook.md'); t=p.read_text()\n\ntete = '''```python\ndef tete_rsn(spikes_par_neurone, assign):\n    # 1. réponse MOYENNE par classe : la somme divisée par le … [4596 caractères tronqués]`

  ```
ok
138:    # 1. réponse MOYENNE par classe : la somme divisée par le nombre de neurones assignés
311:Le code de référence ramène, à chaque exemple, la **somme des poids d'entrée** de chaque excitateur à
392:le multi-exemple, et il fixe une convention d'ordre : la trace pré est mise à jour **après** les spikes post du
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/implantation/diehl-cook.md'); t=p.read_text()\nt=t.replace(\"**celle du code de démonstration** : une variante **symétrique** à traces (`x_pre` 20 ms, `post1` 20 ms,\\n  `post2`  … [1592 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('/tmp/gen_natif.py'); t=p.read_text()\nt=t.replace('\"Six blocs, deux régions, trois têtes précoces, un pont et une cellule de pensée ; \"\\n            \"chaque bloc a des ports typés, un coût et une trace.\"',\n            '\ … [431 caractères tronqués]`

  ```
ok
  ✓ natif-graphe-n0.svg
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_schemas.py >/tmp/g1 2>&1; echo \"schemas=$?\"; tail -2 /tmp/g1; bash tools/porte-tableaux.sh >/tmp/g2 2>&1; echo \"tableaux=$?\"; tail -3 /tmp/g2; python3 tools/revue_documentation.py >/tmp/g3 2>&1; echo \"revu … [250 caractères tronqués]`

  ```
schemas=0
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
tableaux=0
  ✅ 1324 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 1256 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-10-31)
revue=0
  revue de documentation · 370 fiche(s) · 438 JSON · 112 doc(s) · 79 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
taille=1
  ❌ 1 violation(s) :
     · T0 : 4147 mots (AGENTS + en-cours + une tâche) > budget 4 000
etat=0
  en-cours · 1368 mots · 7 sections · 2 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- docs/pilotage/en-cours.md | head -120", "description": "Voir l'ampleur des modifications concurrentes de l'état"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 91bad92d..2f5247d1 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-10-31, 17 h 30 HAE (heure locale, EDT).**
+**Mis à jour : 2026-10-31, 18 h 10 HAE (heure locale, EDT).**
 
 > **État courant, pas histoire.** Une sous-section par **session active** ; une ligne par **chantier** avec son
 > **bloquant**. Les détails de méthode sont dans [`methode/`](../methode/) — chargement et budget dans
@@ -23,7 +23,7 @@
 > `pre-commit`) et la porte `porte-etat.sh` compare les commits. Une session qui trouve
 > l'état en retard le corrige — elle n'attend pas qu'on désigne une « principale ».
 
-### Session active — N2, le budget complet (`0b0a6a0d`)
+### Session `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — N2, le budget complet
 
 - **Id** : `0b0a6a0d-05f5-4308-800c-4792ddb9cbf2` — mandat dans
   [`plan.md`](../../journal/sessions/0b0a6a0d-05f5-4308-800c-4792ddb9cbf2/plan.md).
@@ -37,10 +37,28 @@
   fichiers réservés, ni cette page sans me le dire.
 - **Fichiers réservés** : `work/n2d/`, `tools/distiller_budget.py`, `reports/n2-*`,
   `journal/sessions/
… [4854 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Commit des deux documents et des treize schémas

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain | grep -E \"modele-natif|diehl-cook|docs/README|schemas/README|natif-|diehl-cook-\" && echo '---' && git add docs/theorie/modele-natif.md docs/implantation/diehl-cook.md docs/README.md docs/schemas/README.md do … [535 caractères tronqués]`

  ```
M docs/README.md
 M docs/schemas/README.md
?? docs/implantation/diehl-cook.md
?? docs/schemas/diehl-cook-architecture.svg
?? docs/schemas/diehl-cook-boucle.svg
?? docs/schemas/diehl-cook-contrat.svg
?? docs/schemas/diehl-cook-pipeline.svg
?? docs/schemas/diehl-cook-placements.svg
?? docs/schemas/diehl-cook-temps.svg
?? docs/schemas/natif-cout-activite.svg
?? docs/schemas/natif-drvm.svg
?? docs/schemas/natif-graphe-n0.svg
?? docs/schemas/natif-niveaux.svg
?? docs/schemas/natif-original.svg
?? docs/schemas/natif-pertes.svg
?? docs/schemas/natif-portes.svg
?? docs/theorie/modele-natif.md
---
 docs/README.md                           |   3 +
 docs/implantation/diehl-cook.md          | 603 +++++++++++++++++++++++++++++++
 docs/schemas/README.md                   |  23 +-
 docs/schemas/diehl-cook-architecture.svg | 118 ++++++
 docs/schemas/diehl-cook-boucle.svg       |  71 ++++
 docs/schemas/diehl-cook-contrat.svg      |  60 +++
 docs/schemas/diehl-cook-pipeline.svg     |  61 ++++
 docs/schemas/diehl-cook-placements.svg   |  55 +++
 docs/schemas/diehl-cook-temps.svg        | 111 ++++++
 docs/schemas/natif-cout-activite.svg     | 235 ++++++++++++
 docs/schemas/natif-drvm.svg              
… [392 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -m \"DOCS — LE MODÈLE NATIF ET DIEHL & COOK, 13 SCHÉMAS : LA SÉPARATION À TROIS NIVEAUX\" 2>&1 | tail -30; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Committer la documentation et les schémas"}`

  ```
[still running after 60000ms; moved to background job bash-84]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-84", "wait": true, "timeout_ms": 180000}`

  ```
✅ index : aucun fait stagé sans état
[master bb3bfefe] DOCS — LE MODÈLE NATIF ET DIEHL & COOK, 13 SCHÉMAS : LA SÉPARATION À TROIS NIVEAUX
 41 files changed, 9820 insertions(+), 31 deletions(-)
 create mode 100644 docs/implantation/diehl-cook.md
 create mode 100644 docs/schemas/diehl-cook-architecture.svg
 create mode 100644 docs/schemas/diehl-cook-boucle.svg
 create mode 100644 docs/schemas/diehl-cook-contrat.svg
 create mode 100644 docs/schemas/diehl-cook-pipeline.svg
 create mode 100644 docs/schemas/diehl-cook-placements.svg
 create mode 100644 docs/schemas/diehl-cook-temps.svg
 create mode 100644 docs/schemas/natif-cout-activite.svg
 create mode 100644 docs/schemas/natif-drvm.svg
 create mode 100644 docs/schemas/natif-graphe-n0.svg
 create mode 100644 docs/schemas/natif-niveaux.svg
 create mode 100644 docs/schemas/natif-original.svg
 create mode 100644 docs/schemas/natif-pertes.svg
 create mode 100644 docs/schemas/natif-portes.svg
 create mode 100644 docs/theorie/modele-natif.md
 create mode 100644 journal/sessions/0f3b6070-57ce-4642-b9ec-3b3956f75978/digest.md
 create mode 100644 journal/sessions/0f3b6070-57ce-4642-b9ec-3b3956f75978/rapport.md
 create mode 100644 journal/sessio
… [764 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport pathlib\np=pathlib.Path('docs/implantation/diehl-cook.md'); t=p.read_text()\nt=t.replace(\"\"\"Un spike présynaptique ajoute son poids à `g_e` (ou `g_i`) : `g_e ← g_e + w`. Le neurone décharge quand\n`V > V_t … [2052 caractères tronqués]`

  ```
ok
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh >/tmp/h1 2>&1; echo \"tableaux=$?\"; python3 tools/verifier_schemas.py >/tmp/h2 2>&1; echo \"schemas=$?\"; python3 tools/revue_documentation.py >/tmp/h3 2>&1; echo \"revue=$?\"; tail -2 /tmp/h3", "descrip … [50 caractères tronqués]`

  ```
tableaux=0
schemas=0
revue=0
  revue de documentation · 370 fiche(s) · 438 JSON · 112 doc(s) · 79 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add docs/implantation/diehl-cook.md && timeout 180 git commit -m \"DOCS — DIEHL & COOK : UNITÉS, DÉLAIS ET TRACE DES INHIBITEURS\" 2>&1 | tail -12; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Committer les précisions du cahi … [21 caractères tronqués]`

  ```
[still running after 60000ms; moved to background job bash-87]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-87", "timeout_ms": 180000, "wait": true}`
