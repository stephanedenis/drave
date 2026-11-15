# Session DSH — relecture

- identifiant : `session-ed9b8942-25a3-48ee-9f86-f6821e56df9d`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 14:13:52
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche Y1 (J5, la décision du tagger) : le **prototype** du mode `auto` — `analyser --tagger auto` : si la clé existe (le fichier ou l'environnement), utiliser l'API ; sinon l'heuristique ; **sans changer le code de sortie** (0 dans les deux cas, 3 pour un refus) ; un message sur stderr qui dit lequel a servi (sans la clé, sans le secret) ; le coût affiché dans la ligne TAGGER API. Mesure : les quatre cas (clé présente/invalide/absente/clé + réseau coupé), les codes de sortie, le comportement identique au défaut sans clé ; fiche `reports/rapport-tagger-auto.md` + JSON, un test dans `tools/tests/test_tagger_api.py`, doc `docs/produit/README.md` § 3.7. **La décision reste à l'humain** : la fiche dit la recommandation, ne change pas le défaut.

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

### 🤖 Assistant

Je vais d'abord explorer le dépôt pour comprendre l'existant : le tagger API, la commande `analyser`, les tests et la doc.

- **bash** `{"command": "ls -la && echo '---' && ls tools/ 2>/dev/null && echo '---' && ls tools/tests/ 2>/dev/null && echo '---' && ls docs/produit/ 2>/dev/null && echo '---' && ls reports/ 2>/dev/null | head -50", "description": "Lister la structure du dépôt"}`

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
drwxr-xr-x. 1 stephane stephane   220 15 nov 14:13 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 12:34 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 78680 15 nov 14:10 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run
… [12181 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -15 && echo '---STATUS---' && git status --short | head -40", "description": "Voir l'historique git et le statut"}`

  ```
f63ad709 BILAN DU 15/11 — LA SEMAINE 2 EN UN JOUR : LE TAGGER DÉCIDÉ (DÉFAUT HORS LIGNE), LE GOLD 452 NOMMÉ, LES RÔLES SÉPARÉS, PANINI BLOQUÉ SUR SES 26 SIGNATURES
158dee4d ÉTAT — LA SEMAINE 2 INSCRITE : GOLD 452, TAGGER 402/H50, MATRICE DU DÉFAUT, PANINI 26 SIGNATURES, RESTITUTION v3, PAGE /, TAGGER EN LOT
2929ccf7 SEMAINE 2 — X3 CORRIGÉ : LES 50 TEXTES LIBRES SONT LE BANC DE ROBUSTESSE (1 000 ITEMS, 677 TEXTES, 672 APPELS, 99 971 TOKENS, 0,02177 $ ; CACHE CHAUD 0 $, 1 000/1 000 HASHES)
e1a28307 SEMAINE 2 — X3 : LE TAGGER EN LOT (1 000 ITEMS, 662 APPELS RÉSEAU, 98 968 TOKENS, 0,0216 $ ; CACHE CHAUD 0 $, 1 000/1 000 HASHES) ; --JSONL 1 003 LIGNES
d2fd406a SEMAINE 2 — X1/X2 : LA PAGE / MESURÉE (369/0 CONTRE 359/99, LA RECETTE) ET L'OR DE RÔLES (LE PROTOCOLE POUR S, LE SCHÉMA, LA BASE v1)
2b5bd1cd JOURNAL — RÉGÉNÉRÉ APRÈS LA CLÔTURE DE LA SEMAINE 2 (W1-W6) ; LE TAG semaine-2-2026-11-20 REPOSÉ SUR LE COMMIT W5
049343d3 SEMAINE 2 — W6 : LA CLÔTURE (5 VAGUES, 3 POSITIVES, 1 BLOQUÉE, 1 MIXTE) ; 85 PORTES LUES (81/4), CIBLAGE 9/9 ; TAG ANNOTÉ semaine-2-2026-11-20 SUR 73edb3dd
9960b37f SEMAINE 2 — W5 : LA RESTITUTION v3 SÉPARE LES CINQ RÔLES (GOLD S 144/144, 18/18, PERMUTATION 0/18) ; LE G
… [1606 caractères tronqués]
  ```

### 🤖 Assistant

Je vois un historique fourni autour du tagger. Lisons les fichiers clés.

- **bash** `{"command": "find tools -iname '*tagger*' -o -iname '*analyse*' | head -40; echo '---'; grep -rln \"tagger\" tools --include='*.py' | head -30; echo '---TESTS---'; ls -la tools/tests/ | head", "description": "Trouver les fichiers liés au tagger et à analyser"}`

  ```
tools/analyse_flux.py
tools/analyse_empreinte.py
tools/analyse_experts_statique.py
tools/analyse_engram.py
tools/analyse_octets_par_jeton.py
tools/analyse_hc.py
tools/analyse_reutilisation_experts.py
tools/analyse_union_experts.py
tools/__pycache__/analyse_experts_statique.cpython-313.pyc
tools/analyse_litteraire.py
tools/analyse_alignement.py
tools/tests/linguistique/__pycache__/qualifier_tagger_612.cpython-313.pyc
tools/tests/linguistique/__pycache__/qualifier_tagger_h50.cpython-313.pyc
tools/tests/linguistique/__pycache__/qualifier_tagger_lot.cpython-313.pyc
tools/tests/linguistique/qualifier_tagger_612.py
tools/tests/linguistique/qualifier_tagger_h50.py
tools/tests/linguistique/qualifier_tagger_lot.py
tools/tests/__pycache__/test_tagger_api.cpython-313-pytest-9.1.1.pyc
tools/tests/__pycache__/test_tagger_api.cpython-313.pyc
tools/tests/test_tagger_api.py
tools/structures/donnees/gold-analyseur.json
tools/structures/donnees/mesure-analyseur.json
tools/structures/__pycache__/mesure_analyseur.cpython-313.pyc
tools/structures/mesure_analyseur.py
---
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/ncl.py
tools/docwatch/.venv/lib/python3.13/site-packages/more_iterto
… [1105 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"analyser\" tools --include='*.py' | head -30; echo '---LLM---'; ls tools/llm/; echo '---'; grep -rln \"tagger\" tools/llm/ 2>/dev/null", "description": "Trouver la commande analyser et le module LLM"}`

  ```
tools/analyse_flux.py
tools/trace_compacite.py
tools/analyse_empreinte.py
tools/aligneur_litteraire.py
tools/docwatch/src/docwatch/diagrams.py
tools/docwatch/src/docwatch/server.py
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/util.py
tools/docwatch/.venv/lib/python3.13/site-packages/pygments/util.py
tools/tests/linguistique/evaluer_gold.py
tools/tests/linguistique/juge.py
tools/tests/linguistique/qualifier_neuronal.py
tools/tests/linguistique/qualifier_syntagmes.py
tools/tests/linguistique/qualifier_cascade.py
tools/tests/linguistique/qualifier_pragmatique.py
tools/tests/linguistique/miroir.py
tools/tests/linguistique/qualifier_lien_appris.py
tools/tests/linguistique/qualifier_quatre_modes.py
tools/tests/linguistique/classement_cible.py
tools/tests/linguistique/replis_cible.py
tools/tests/linguistique/classer_gv.py
tools/tests/linguistique/qualifier_tagger_612.py
tools/tests/linguistique/test_bloc_linguistique.py
tools/tests/linguistique/gold_reel_50.py
tools/tests/linguistique/qualifier_tagger_h50.py
tools/tests/linguistique/qualifier_tagger_lot.py
tools/tests/test_produit_libre.py
tools/tests/test_schema_produit.py
tools/tests/test_restitution.py
tools/t
… [259 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"tagger\\|analyser\\|auto\" tools/drave.py | head -80; echo '---WC---'; wc -l tools/drave.py tools/bloc_linguistique.py tools/tests/test_tagger_api.py docs/produit/README.md", "description": "Chercher analyser et tagger dans drave.py"}`

  ```
6:    python3 tools/drave.py analyser "Le chat dort."
7:    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
8:    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
11:    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
18:Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
23:En **option** (`--tagger`, `analyser` et `evaluer`), le POS (et lui seul) vient du tagger de
26:**Sans `--tagger`, le défaut ne change pas** : heuristique, CPU, hors ligne, déterministe.
30:Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger indisponible
47:# externe n'est importé : le point d'entrée est autonome.
62:# Le tagger est une **option** : sans `--tagger`, rien de ce bloc n'est importé ni exécuté.
65:# La fusion de l'option : le POS vient du tagger, tout le reste de l'heuristique. On ne force
90:# --------------------------------------------------------------------------- le tagger (option)
94:    """Aucune clé : le tagger est une option, jamais un prérequis du produit."""
109:            f"Sans --tagger, le défaut 
… [4919 caractères tronqués]
  ```

- **bash** `{"command": "cat tools/tests/test_tagger_api.py", "description": "Lire le test tagger api"}`

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
   puis `DEEPSEEK_API_KEY`.

A
… [24851 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "limit": 480}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """drave.py — le point d'entrée produit du bloc linguistique.
3: 
4: Une seule commande, quatre gestes, hors ligne et déterministe :
5: 
6:     python3 tools/drave.py analyser "Le chat dort."
7:     python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
8:     python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
9:     python3 tools/drave.py evaluer
10:     python3 tools/drave.py evaluer --gold --json
11:     python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
12:     python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
13:     python3 tools/drave.py restituer "Le chat dort."
14:     python3 tools/drave.py restituer "Le chat dort." --roles
15:     python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
16:     python3 tools/drave.py --version
17: 
18: Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
19: avec rôle et cible d'attacheme
… [23034 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "offset": 680, "limit": 361}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
680:                 mt = evaluateur.evaluer_bloc("cascade", cascade, sous)
681:                 m["tagger"] = {
682:                     "pos": {k: mt["pos"][k] for k in ("exactitude", "exactitude_ferme",
683:                                                       "exactitude_ouvert", "tokens")},
684:                     "syntagme": {"f1": mt["syntagme"]["f1"],
685:                                  "tete": {"f1": mt["syntagme"]["tete"]["f1"]}},
686:                     "pragmatique": mt["pragmatique"],
687:                     "fraction_semantique": mt["fraction_semantique"],
688:                     "delta_pos": round(mt["pos"]["exactitude"] - m["pos"]["exactitude"], 4),
689:                 }
690:             par_langue[langue] = m
691:         rapport["par_langue"] = par_langue
692:     if args.json:
693:         sys.stdout.write(_dumps(rapport))
694:         if stats is not None:
695:             print(f"{NOM}: TAGGER API · {_ligne_tagger(stats)}", file=sys.stderr)
696:     else:
697:         print(_formater_evaluation(rapport))
698:     return 0
699: 
700: 
701: def cmd_rejo
… [19527 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"tagger auto\\|--tagger auto\\|mode auto\\|TAGGER API\" reports docs journal 2>/dev/null | head -40", "description": "Chercher les mentions du tagger auto"}`

  ```
reports/rapport-exemples-tagger.json
reports/rapport-exemples-tagger.md
reports/rapport-tagger-erreurs.md
reports/rapport-tagger-erreurs.json
reports/rapport-tagger-defaut.md
reports/rapport-tagger-defaut.json
reports/rapport-tagger-lot.json
docs/produit/exemples.md
docs/produit/README.md
journal/sessions/22bcae27-254b-47b2-acda-87467dab060c/digest.md
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md
journal/sessions/4d7a793b-74d1-4c46-bb53-21953fe91d87/rapport.md
journal/sessions/4d7a793b-74d1-4c46-bb53-21953fe91d87/digest.md
journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/rapport.md
journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/digest.md
journal/sessions/8156fdcb-5033-4ba4-a5f3-f8a078e6e57e/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
journal/sessions/24e34ad3-f423-4394-bb1c-74a6930a57e5/digest.md
journal/sessions/session-e73a3601-e2c6-417c-a009-88ffadca4e61/digest.md
journal/sessions/session-3ee08872-fd34-4732-af49-0639cb5d82a9/digest.md
journal/sessions/session-01599146-2479-4a06-8381-4ace3d13f
… [229 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"3.7\\|tagger\" docs/produit/README.md | head -40; echo '---TAIL---'; sed -n '1,80p' docs/produit/README.md", "description": "Chercher la section 3.7 et le tagger dans la doc produit"}`

  ```
11:> porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
12:> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le format
47:aucun accès réseau **par défaut** (le tagger en option, lui, appelle l'API DeepSeek, § 3.7). Les
64:| **POS** | DET, NOUN, VERB, ADJ, ADV, PREP, PRON, AUX, CONJ, NUM… | **0,8625** (fermé 0,9373, ouvert 0,7918) ; **0,8891** sur le réel 452 ; **0,9575** avec `--tagger` |
143:gold vivant (hand + reel + synthétique) · 612 phrases · 3179 tokens · 239 cibles d'attachement
145:POS         exactitude 86.25 %  (fermé 93.73 %, ouvert 79.18 %)
148:  vue linéaire (partition filtrer) F1 81.44 %  · attachement 93.72 % de couverture
356:contrôle négatif : mélange exacte 0.0000 (caractères 0.3077) · troncature exacte 0.0000
386:### 3.7 Le tagger en option — `--tagger`
389:python3 tools/drave.py analyser "Le chat dort." --tagger
390:python3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger
391:python3 tools/drave.py evaluer --tagger
394:drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
416:**Les cas d'erreur.** Mesurés par [`test_tagger_api.py`](../../tools/tests/test_tagger_api.py)
… [8484 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "offset": 380, "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
380: ```
381: 
382: `--reel` mesure les **452 phrases réelles** (main + corpus), sans les 160 synthétiques : POS
383: **88,91 %**, F1 **79,06 %**, attachement **99,46 %**. Sans lui, `evaluer` publie la ligne
384: `BASE RÉELLE` à côté du global (612 phrases) — le chiffre global seul peut tromper.
385: 
386: ### 3.7 Le tagger en option — `--tagger`
387: 
388: ```bash
389: python3 tools/drave.py analyser "Le chat dort." --tagger
390: python3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger
391: python3 tools/drave.py evaluer --tagger
392: ```
393: ```
394: drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)
395: langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
396: POS  Le/DET chat/NOUN dort/VERB ./PONCT
397: SYNTAGMES
398:   GN   [0:7]   Le chat  rôle=agent     → dort
399:   GV   [8:12]  dort     rôle=predicat  → chat
400: PRAGMATIQUE
401:   phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
402: COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=
… [7470 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/rapport-tagger-defaut.md; echo '===JSON==='; cat reports/rapport-tagger-defaut.json", "description": "Lire la fiche tagger défaut et son JSON"}`

  ```
# W3 — la matrice du tagger : le défaut reste hors ligne (code 0), `--tagger` est la seule porte qui peut sortir 4

> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **W3** (semaine 2, J2
> après-midi) · **Date** : 2026-11-15 · **HEAD mesuré** : `3439cb0c` + ce diff (champ de coût
> additif) · **Verdict** : ✅ **la matrice est mesurée** — le **défaut sans clé** rend
> l'heuristique, **code 0**, **0 socket** ; avec clé, **code 0**, **130 tokens** et **1,16 s**
> pour une phrase ; **clé invalide**, **code 4**, `stdout` vide ; **réseau coupé**, **code 0**
> après **3 essais**, repli heuristique explicite. **Coût pour 1 000 phrases** : **143 870
> tokens**, **989 requêtes**, **981,9 s** de réseau, **~0,031 $ hors pointe / ~0,062 $ en
> pointe**. **Recommandation** : garder le **défaut hors ligne** et `--tagger` **opt-in** ; ne
> pas livrer `auto` maintenant, et si `auto` vient, **seulement si la clé existe** et **sans
> changer le code de sortie**. **21/21 tests**.

**En trois lignes.** (1) Le **défaut** ne touche ni la clé, ni le réseau, ni l'API : `analyser`
et `evaluer` sans `--tagger` sortent **0** dans un `HOME` vide, le JSON dit `source=heuristique`,
et un `so
… [32586 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/llm/deepseek.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/llm/deepseek.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """deepseek.py — le professeur externe, sans poids locaux.
3: 
4: POURQUOI CE MODULE. Le dépôt garde ses GPU et ses CPU pour le **modèle natif**
5: Drave (`entrainer_moteur.py`, `drave-core`) et pour les mesures **boîte blanche**
6: (perplexité, activations, flux, sondes). Le **langage** — traduire, juger,
7: générer, évaluer — passe par une API : on ne charge plus un Qwen de 7/14/32 B
8: pour cela. DeepSeek est ce **professeur externe** ; ses sorties peuvent servir à
9: entraîner/distiller l'élève natif (autorisation explicite du propriétaire de la
10: licence).
11: 
12: CE QUE LE MODULE NE FAIT PAS. Il ne remplace pas les mesures d'états internes :
13: une API ne donne pas les poids ni les activations. Il ne met **jamais** la clé
14: dans le dépôt, dans un cache ou dans un message d'erreur. Il ne dépend d'aucun
15: paquet externe : `urllib` suffit.
16: 
17: CONTRAT.
18: - `DEEPSEEK_API_KEY` (ou `DSH_API_KEY`) : la clé, lue dans l'environnement ;
19: - `DEEPSEEK_BASE_URL` (ou `DSH_BASE_URL`) : `https://api.deepseek.com` par défaut ;
20: - `DEE
… [11956 caractères tronqués]
  ```

- **bash** `{"command": "for f in \"$HOME/.config/drave/deepseek.key\"; do if [ -s \"$f\" ]; then echo \"fichier présent: $f\"; else echo \"fichier absent/vide: $f\"; fi; done; for v in DEEPSEEK_API_KEY DSH_API_KEY DEEPSEEK_KEY_FILE DSH_KEY_FILE; do if [ -n \"${!v:-}\" ]; then echo \"$v défini (non affiché)\";  … [164 caractères tronqués]`

  ```
fichier présent: /home/stephane/.config/drave/deepseek.key
DEEPSEEK_API_KEY absent
DSH_API_KEY absent
DEEPSEEK_KEY_FILE absent
DSH_KEY_FILE absent
---cache---
3759
  ```

- **bash** `{"command": "python3 tools/tests/test_tagger_api.py 2>&1 | tail -20; echo '---PYTEST---'; python3 -m pytest tools/tests/test_tagger_api.py -q 2>&1 | tail -10", "description": "Lancer les tests existants du tagger"}`

  ```
test_evaluer_tagger (__main__.TestCliAvecTransportFactice.test_evaluer_tagger) ... ok
test_aide_expose_tagger (__main__.TestDefaultInchange.test_aide_expose_tagger) ... ok
test_analyser_json_sans_tagger (__main__.TestDefaultInchange.test_analyser_json_sans_tagger) ... ok
test_evaluer_sans_tagger (__main__.TestDefaultInchange.test_evaluer_sans_tagger) ... ok
test_cle_invalide_code_4 (__main__.TestErreursTagger.test_cle_invalide_code_4) ... ok
test_modele_json_incomplet_repli_heuristique (__main__.TestErreursTagger.test_modele_json_incomplet_repli_heuristique)
Un JSON qui n'a pas une classe par token est un refus de contrat, pas une exception. ... ok
test_refus_du_modele_repli_heuristique (__main__.TestErreursTagger.test_refus_du_modele_repli_heuristique) ... ok
test_reseau_coupe_repli_heuristique (__main__.TestErreursTagger.test_reseau_coupe_repli_heuristique) ... ok
test_cout_pour_1000_phrases (__main__.TestMatriceW3.test_cout_pour_1000_phrases)
`evaluer --tagger` publie le coût linéaire pour 1 000 phrases. ... ok
test_defaut_n_ouvre_aucune_socket (__main__.TestMatriceW3.test_defaut_n_ouvre_aucune_socket)
Le défaut ne charge pas le client réseau et ne construit aucune socket. ... o
… [379 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"Y1\\|tagger auto\\|mode auto\\|auto\" docs/pilotage/roadmap.md docs/pilotage/en-cours.md tools/chantier/plan.json 2>/dev/null | head -60", "description": "Chercher la tâche Y1 dans le pilotage"}`

  ```
docs/pilotage/roadmap.md:35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **fusion réparée par niveau : 0,9309/0,8226/0,8784/0,9954 (le max)** ([fiche](../../reports/rapport-pensee-fusion-reparee.md)) ; **corpus commun UDHR : 21 textes, 418/438 paires exactes (95,4 %), 20 écarts exclus** ([fiche](../../reports/rapport-corpus-commun.md)) ; **J3.1 retrieval à époque contrôlée : l'écriture domine (+0,609), l'époque ne pèse pas à écriture contrôlée (−0,034/siècle, p=0,19), le brut est un effet de composition (0,238 vs 0,427)** ([fiche](../../reports/rapport-retrieval-epoque.md)) ; **J3.2 généalogie à deux faces : Panini couvre 5/21 langues (200/210 paires « inconnues »), Glottolog 21/21 ; 154/154 paires hors script au hasard exact, le si
… [6868 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"tagger\" docs/pilotage/roadmap.md | head -30; echo '---PLAN---'; python3 -c \"import json;d=json.load(open('tools/chantier/plan.json'));print(json.dumps(d,ensure_ascii=False)[:3000])\" 2>/dev/null", "description": "Voir la roadmap et le plan chantier"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [8026 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nfor t in d['taches']:\n    if t['id']=='Y1':\n        print(json.dumps(t, ensure_ascii=False, indent=2))\nPY", "description": "Afficher la tâche Y1 du plan"}`

  ```
{
  "id": "Y1",
  "jour": 18,
  "titre": "J5 — le mode auto du tagger (prototype)",
  "mandat": "Tâche Y1 (J5, la décision du tagger) : le **prototype** du mode `auto` — `analyser --tagger auto` : si la clé existe (le fichier ou l'environnement), utiliser l'API ; sinon l'heuristique ; **sans changer le code de sortie** (0 dans les deux cas, 3 pour un refus) ; un message sur stderr qui dit lequel a servi (sans la clé, sans le secret) ; le coût affiché dans la ligne TAGGER API. Mesure : les quatre cas (clé présente/invalide/absente/clé + réseau coupé), les codes de sortie, le comportement identique au défaut sans clé ; fiche `reports/rapport-tagger-auto.md` + JSON, un test dans `tools/tests/test_tagger_api.py`, doc `docs/produit/README.md` § 3.7. **La décision reste à l'humain** : la fiche dit la recommandation, ne change pas le défaut.",
  "budget_min": 90,
  "acceptation": [
    {
      "commande": "test -f reports/rapport-tagger-auto.md && echo FICHE-OK",
      "attendu": "FICHE-OK"
    },
    {
      "commande": "python3 tools/tests/test_tagger_api.py 2>&1 | tail -1",
      "attendu": "OK"
    }
  ]
}
  ```

- **bash** `{"command": "cat reports/rapport-tagger-erreurs.md | head -80; echo '===EXEMPLES==='; grep -n \"TAGGER API\\|coût\\|cout\" docs/produit/exemples.md | head -30; echo '---'; sed -n '/## 6/,/## 7/p' docs/produit/exemples.md | head -120", "description": "Lire les conventions de coût du tagger"}`

  ```
# E2 — les cas d'erreur de `--tagger` : clé refusée = code 4, réseau et refus du modèle = repli heuristique

> **Ligne de roadmap** : **B13** (le produit) · **Tâche** : **E2** · **Date** : 2026-11-15 ·
> **Verdict** : ✅ **4/4 cas caractérisés**, **18/18 tests**, **0 socket**.
> **La clé invalide (HTTP 401/403) sort désormais 4** avec un message clair et **rien sur
> `stdout`** ; avant, elle était avalée par le tagger et le CLI rendait **0** avec un repli
> heuristique déguisé en cascade. Le **réseau coupé** (3 essais du client) et le **refus du
> modèle** restent des refus **par phrase** : repli heuristique, code **0**, cause dans `refus`.
> **Dispositif** : [`tools/drave.py`](../tools/drave.py) 0.1.0, client `DeepSeek` injecté,
> transport factice, cache temporaire vide, aucun socket. **Contrôle négatif** : un transport
> valide donne code 0 et des POS neuronaux ; la mutation qui retire le contrôle 401/403 fait
> échouer le test (`0 != 4`). **JSON** : [`rapport-tagger-erreurs.json`](rapport-tagger-erreurs.json).

## 1. Les quatre cas

Le tableau dit le comportement **du code courant**, pas l'intention. Chaque ligne a son test
dans [`test_tagger_api.py`](../tools/tests/test_tagger_
… [10976 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class Annotation\\|class Cascade\\|class NeuronalLLMPOS\\|def analyser\\|refus\" tools/bloc_linguistique.py | head -60", "description": "Repérer les classes et le champ refus"}`

  ```
102:class Annotation:
107:    refus: str = ""
134:            "source": self.source, "refus": self.refus,
145:    def analyser(self, texte: str, langue: str | None = None,
150:    """Le modèle n'a pas rendu une annotation exploitable — le contrat refuse, il n'invente pas."""
1471:    def analyser(self, texte: str, langue: str | None = None,
1475:            # une entrée non textuelle est **refusée** proprement (le produit ne plante pas)
1476:            return Annotation(texte=str(texte)[:200], refus="non_texte", source=self.nom,
1477:                              trace=[{"etape": "refus", "raison": "non_texte",
1483:            return Annotation(texte=texte, refus="vide", source=self.nom,
1484:                              trace=[{"etape": "refus", "raison": "vide"}],
1861:    def analyser(self, texte: str, langue: str | None = None,
1932:    def analyser(self, texte: str, langue: str | None = None,
1984:class NeuronalLLMPOS:
2042:    def analyser(self, texte: str, langue: str | None = None,
2048:            return Annotation(texte=texte, langue=lg, script=script, refus="vide", source=self.nom)
2054:            return Annotation(texte=texte, langue=lg, script=script, refus="vide",
… [1643 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class Annotation\" -A60 tools/bloc_linguistique.py | head -80; echo '---CASCADE---'; grep -n \"class Cascade\" -A90 tools/bloc_linguistique.py | head -110", "description": "Lire Annotation et Cascade"}`

  ```
102:class Annotation:
103-    texte: str
104-    langue: str = "und"
105-    script: str = SCRIPT_NEUTRE
106-    etiquettes: list[Etiquette] = field(default_factory=list)
107-    refus: str = ""
108-    trace: list[dict] = field(default_factory=list)
109-    cout: dict = field(default_factory=dict)
110-    unites_semantiques: list[Span] = field(default_factory=list)
111-    fraction_semantique: float = 0.0
112-    source: str = "heuristique"
113-    contexte: str = ""
114-
115-    def par_niveau(self) -> dict[str, list[Etiquette]]:
116-        sortie: dict[str, list[Etiquette]] = collections.defaultdict(list)
117-        for e in self.etiquettes:
118-            sortie[e.niveau].append(e)
119-        return dict(sortie)
120-
121-    def couverture(self) -> dict[str, float]:
122-        """La confiance maximale par niveau — la couverture *déclarée*, pas une précision."""
123-        return {n: round(max((e.confiance for e in es), default=0.0), 4)
124-                for n, es in self.par_niveau().items()}
125-
126-    def json(self, avec_duree: bool = False) -> dict:
127-        cout = dict(self.cout)
128-        if not avec_duree:
129-            cout.pop("duree_s", None)
130-     
… [6015 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"construire_parseur\\|tagger_mode\\|tagger_auto\\|\\.tagger\" tools tests src --include='*.py' 2>/dev/null | grep -v __pycache__ | head -40", "description": "Chercher les usages du parseur et de args.tagger"}`

  ```
tools/couche_distante.py:2061:def construire_parseur() -> argparse.ArgumentParser:
tools/couche_distante.py:2091:    args = construire_parseur().parse_args(argv)
tools/drave.py:872:def construire_parseur() -> argparse.ArgumentParser:
tools/drave.py:1022:    args = construire_parseur().parse_args(argv)
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "offset": 520, "limit": 180}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
520:         f"POS         exactitude {_pct(pos['exactitude'])}  "
521:         f"(fermé {_pct(pos['exactitude_ferme'])}, ouvert {_pct(pos['exactitude_ouvert'])})",
522:         f"SYNTAGMES   F1 {_pct(syn['f1'])}  "
523:         f"(P {_pct(syn['precision'])} / R {_pct(syn['rappel'])})",
524:         f"  tête      F1 {_pct(tete['f1'])}  "
525:         f"(P {_pct(tete['precision'])} / R {_pct(tete['rappel'])})",
526:         f"  vue linéaire (partition filtrer) F1 {_pct(rapport['syntagmes_lineaire']['f1'])}  "
527:         f"· attachement {_pct(rapport['attachement_lineaire']['couverture'])} de couverture",
528:         (f"BASE RÉELLE (hand + reel, {rapport['reel']['phrases']} phrases)  "
529:          f"POS {_pct(rapport['reel']['pos'])} · F1 {_pct(rapport['reel']['f1'])} "
530:          f"· attachement {_pct(rapport['reel']['couverture'])}"
531:          if rapport.get("reel") else f"BASE RÉELLE — (déjà la base, ou gold gelé)"),
532:         f"ATTACHEMENT exact {_pct(att['exact_taux'])} · couverture {_pct(att['couverture'])} "
533:         f"· exact sur span {_pct(att['exact_taux
… [9795 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"formater_annotation\" -n tools --include='*.py' | grep -v __pycache__", "description": "Chercher les appels à formater_annotation"}`

  ```
tools/drave.py:306:def formater_annotation(a: bl.Annotation, tagger: bool = False,
tools/drave.py:460:        print(_sur(formater_annotation(annotation, tagger=stats is not None, stats=stats)))
  ```

- **bash** `{"command": "date -Iseconds; git rev-parse --short HEAD; git branch --show-current", "description": "Voir la date et le HEAD"}`

  ```
2026-11-15T14:16:20-05:00
f63ad709
s/v7
  ```

- **todo_write** `{"todos": [{"content": "Implémenter `--tagger auto` dans drave.py (parsing, sélection API/heuristique, messages, coût)", "status": "in_progress"}, {"content": "Ajouter les tests des quatre cas dans tools/tests/test_tagger_api.py", "status": "pending"}, {"content": "Mesurer les quatre cas réels (clé  … [309 caractères tronqués]`

  ```
Updated todo list: 5 pending, 1 in progress, 0 completed.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "    python3 tools/drave.py analyser \"Le chat dort.\" --tagger          # API DeepSeek (clé, réseau)\n    python3 tools/drave.py evaluer", "new_string": "    python3 tools/drave.py analyser \"Le chat dort. … [192 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "En **option** (`--tagger`, `analyser` et `evaluer`), le POS (et lui seul) vient du tagger de\nl'API DeepSeek : la clé est lue dans `DEEPSEEK_KEY_FILE`, `~/.config/drave/deepseek.key` puis\n`DEEPSEEK_API_KE … [936 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "def _client_tagger():\n    \"\"\"Le client de l'API. L'import est **local** : le défaut ne charge pas le module réseau.\"\"\"\n    from tools.llm.deepseek import DeepSeek\n    return DeepSeek(cle=_cle_tagg … [4951 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "def formater_annotation(a: bl.Annotation, tagger: bool = False,\n                        stats: dict | None = None) -> str:\n    \"\"\"La sortie lisible : POS compact, syntagmes (rôle + cible), pragmatique … [1136 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "def _analyser_jsonl(texte: str, args: argparse.Namespace, h: bl.Heuristique, bloc,\n                    stats: dict | None = None) -> int:\n    \"\"\"Une **ligne JSON par phrase** (traitement de corpus : ` … [760 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "    if stats is not None:\n        print(f\"{NOM}: TAGGER API · {_ligne_tagger(stats)}\", file=sys.stderr)\n        if refus:\n            print(f\"{NOM}: tagger · {refus}/{n} phrase(s) refusée(s) (JSON pa … [445 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "offset": 505, "limit": 70}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
505: def _analyser_jsonl(texte: str, args: argparse.Namespace, h: bl.Heuristique, bloc,
506:                     stats: dict | None = None, auto: _TaggerAuto | None = None) -> int:
507:     """Une **ligne JSON par phrase** (traitement de corpus : `--jsonl`).
508: 
509:     `h` segmente (le tagger ne change pas les frontières de phrase) ; `bloc` analyse — la
510:     cascade du tagger quand `--tagger` est posé. Le coût va sur `stderr`, jamais dans le JSONL.
511:     En mode `auto`, le message qui dit la voie servie va aussi sur `stderr`.
512:     """
513:     n = 0
514:     refus = 0
515:     for debut, fin, _typ, _ in h._phrases(texte):
516:         phrase = texte[debut:fin]
517:         if not phrase.strip():
518:             continue
519:         a = bloc.analyser(phrase, args.langue, args.contexte)
520:         refus += int(bool(a.refus))
521:         sys.stdout.write(_sur(json.dumps(a.json(), ensure_ascii=False)) + "\n")
522:         n += 1
523:     if n == 0:
524:         print(f"{NOM}: refus d'analyse : vide", file=sys.stderr)
525:         return 3
526:     if stats is not 
… [2651 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "offset": 574, "limit": 15}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py</path>
<type>file</type>
<content>
574:             print(f"{NOM}: TAGGER API · {_ligne_tagger(stats)}", file=sys.stderr)
575:     else:
576:         print(_sur(formater_annotation(annotation, tagger=stats is not None, stats=stats)))
577:     return 0
578: 
579: 
580: def _module_evaluation():
581:     """Charge `evaluer_gold.py` (le gold et sa mesure) sans dépendre du répertoire courant."""
582:     chemin = RACINE / "tools" / "tests" / "linguistique" / "evaluer_gold.py"
583:     if not chemin.is_file():
584:         raise FileNotFoundError(f"mesure du gold introuvable : {chemin}")
585:     spec = importlib.util.spec_from_file_location("_drave_evaluer_gold", chemin)
586:     if spec is None or spec.loader is None:
587:         raise ImportError(f"impossible de charger {chemin}")
588:     module = importlib.util.module_from_spec(spec)

(Showing lines 574-588 of 1157. Use offset=589 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "    def __init__(self, heuristique: bl.Heuristique, cascade=None, stats: dict | None = None):\n        self.h = heuristique\n        self.cascade = cascade\n        self.stats = stats\n        self.api_ser … [634 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "        if self.cascade is None:\n            return \"heuristique (clé absente)\"\n        if self.cause:", "new_string": "        if self.cascade is None:\n            if self.cle_presente:\n             … [147 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "        if self.cascade is None:\n            return f\"{NOM} {VERSION} — analyse heuristique (CPU, hors ligne ; auto sans clé)\"\n        if self.cause:", "new_string": "        if self.cascade is None:\n … [105 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "def cmd_analyser(args: argparse.Namespace) -> int:\n    texte = _lire_entree(args)\n    h = bl.Heuristique(partition=args.partition)\n    bloc, stats = h, None\n    if getattr(args, \"tagger\", False):\n   … [6338 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "    if n == 0:\n        print(f\"{NOM}: refus d'analyse : vide\", file=sys.stderr)\n        return 3", "new_string": "    if n == 0:\n        print(f\"{NOM}: refus d'analyse : vide\", file=sys.stderr)\n    … [125 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "def construire_parseur() -> argparse.ArgumentParser:\n    epilogue = (\n        \"Commandes : analyser, evaluer, rejouer, restituer.\\n\"\n        \"Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse … [3571 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "        help=\"étiqueter un texte (POS, syntagmes, pragmatique)\",\n        description=\"Analyse un texte avec l'heuristique et rend la lecture compacte ou le JSON. \"\n                    \"Avec --tagger … [1272 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "    analyser.add_argument(\"--tagger\", action=\"store_true\",\n                          help=\"tagger POS par l'API DeepSeek (clé et réseau ; défaut : heuristique)\")\n    analyser.add_argument(\"--json\ … [801 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "    evaluer.add_argument(\"--tagger\", action=\"store_true\",\n                         help=\"mesurer en plus la cascade POS de l'API DeepSeek (clé et réseau)\")\n    evaluer.add_argument(\"--json\", acti … [589 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "def cmd_evaluer(args: argparse.Namespace) -> int:\n    evaluateur = _module_evaluation()", "new_string": "def cmd_evaluer(args: argparse.Namespace) -> int:\n    if getattr(args, \"tagger_auto\", False):\n  … [182 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "    args = construire_parseur().parse_args(argv)\n    try:\n        return args.fonction(args)", "new_string": "    brut = list(sys.argv[1:] if argv is None else argv)\n    args = construire_parseur().pars … [240 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **bash** `{"command": "python3 -m py_compile tools/drave.py && echo COMPILE-OK; python3 tools/drave.py analyser \"Le chat dort.\" --aide 2>&1 | tail -25", "description": "Compiler et afficher l'aide"}`

  ```
COMPILE-OK
usage: drave analyser [-h] [--partition {brut,alternative,filtrer_union,filtrer}] [--fichier CHEMIN]
                      [--jsonl] [--contexte CONTEXTE] [--langue {fr,en}] [--tagger] [--json]
                      [TEXTE]

Analyse un texte avec l'heuristique et rend la lecture compacte ou le JSON. Avec --tagger, le POS (et lui seul) vient du tagger de l'API DeepSeek : clé requise, réseau, cache du client ; sans l'option, rien ne change. Avec --tagger auto, l'API sert si une clé existe, sinon l'heuristique ; le code de sortie ne change pas (0 dans les deux cas, 3 pour un refus).

arguments:
  TEXTE                 texte à analyser (entre guillemets) ou --fichier

options:
  -h, --help, --aide    afficher cette aide et quitter
  --partition {brut,alternative,filtrer_union,filtrer}
                        la vue des syntagmes qui se chevauchent (défaut : alternative)
  --fichier CHEMIN      lire le texte dans un fichier UTF-8 (au lieu de l'argument)
  --jsonl               une ligne JSON par phrase (traitement de corpus)
  --contexte CONTEXTE   le texte qui précède (mémoire de discours : coréférence, connecteurs)
  --langue {fr,en}      indice de langue (fr/en) ; sans lui
… [511 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/tests/test_tagger_api.py 2>&1 | tail -12", "description": "Lancer les tests existants après modification"}`

  ```
test_reseau_coupe_repli_heuristique (__main__.TestErreursTagger.test_reseau_coupe_repli_heuristique) ... ok
test_cout_pour_1000_phrases (__main__.TestMatriceW3.test_cout_pour_1000_phrases)
`evaluer --tagger` publie le coût linéaire pour 1 000 phrases. ... ok
test_defaut_n_ouvre_aucune_socket (__main__.TestMatriceW3.test_defaut_n_ouvre_aucune_socket)
Le défaut ne charge pas le client réseau et ne construit aucune socket. ... ok
test_defaut_sans_cle_code_0 (__main__.TestMatriceW3.test_defaut_sans_cle_code_0)
Sans clé, le défaut rend l'heuristique, code 0, et n'appelle jamais le tagger. ... ok

----------------------------------------------------------------------
Ran 21 tests in 5.924s

OK
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "old_string": "def _tokens_de_invite(invite: str) -> list[str]:", "new_string": "def _env_sans_cle(home: pathlib.Path, **extra: str) -> dict[str, str]:\n    \"\"\"Un environnement sans aucune des sources  … [452 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "offset": 1, "limit": 80}`

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
… [2494 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "old_string": "6. l'ordre de résolution de la clé : `DEEPSEEK_KEY_FILE`, puis `~/.config/drave/deepseek.key`,\n   puis `DEEPSEEK_API_KEY`.\n\nAucun test n'ouvre de socket : les transports sont injectés, e … [796 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "old_string": "def _tokens_de_invite(invite: str) -> list[str]:", "new_string": "def _env_sans_cle(home: pathlib.Path, **extra: str) -> dict[str, str]:\n    \"\"\"Un environnement sans aucune des sources  … [452 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "offset": 490, "limit": 70}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py</path>
<type>file</type>
<content>
490:             "socket.socket = Interdit\n"
491:             "sys.path.insert(0, 'tools')\n"
492:             "import drave\n"
493:             "with contextlib.redirect_stdout(io.StringIO()):\n"
494:             "    c = drave.main(['analyser', 'Le chat dort.', '--json'])\n"
495:             "print('CODE', c)\n"
496:             "print('DEEPSEEK', 'tools.llm.deepseek' in sys.modules)\n"
497:         )
498:         with tempfile.TemporaryDirectory() as tmp:
499:             env = self._env_sans_cle(pathlib.Path(tmp))
500:             resultat = subprocess.run(
501:                 [sys.executable, "-c", code], cwd=str(RACINE), capture_output=True,
502:                 text=True, encoding="utf-8", timeout=60, env=env)
503:         self.assertEqual(resultat.returncode, 0, resultat.stderr)
504:         self.assertIn("CODE 0", resultat.stdout)
505:         self.assertIn("DEEPSEEK False", resultat.stdout)
506: 
507:     def test_cout_pour_1000_phrases(self) -> None:
508:         """`evaluer --tagger` publie le coût linéaire pour 1 000 phrases."""
509:         client 
… [2239 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "old_string": "def _pos_map(donnees: dict) -> dict[tuple[int, int], str]:", "new_string": "class TestTaggerAuto(unittest.TestCase):\n    \"\"\"Le prototype `--tagger auto` : API si clé, heuristique sinon, … [9234 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/tests/test_tagger_api.py 2>&1 | tail -40", "description": "Lancer les tests du tagger avec le mode auto"}`

  ```
test_cache_par_texte (__main__.TestCascadeTagger.test_cache_par_texte) ... ok
test_cascade_remplace_les_pos (__main__.TestCascadeTagger.test_cascade_remplace_les_pos) ... ok
test_json_valide_schema (__main__.TestCascadeTagger.test_json_valide_schema) ... ok
test_transport_invalide_ne_fait_pas_planter (__main__.TestCascadeTagger.test_transport_invalide_ne_fait_pas_planter)
Un tagger qui rend autre chose qu'un JSON est un refus, pas une exception. ... ok
test_absence_de_cle_ne_fuit_pas (__main__.TestCle.test_absence_de_cle_ne_fuit_pas) ... ok
test_la_cle_ne_sort_pas_du_client (__main__.TestCle.test_la_cle_ne_sort_pas_du_client) ... ok
test_ordre_de_resolution (__main__.TestCle.test_ordre_de_resolution) ... ok
test_sans_cle_code_4 (__main__.TestCle.test_sans_cle_code_4) ... ok
test_analyser_tagger_json (__main__.TestCliAvecTransportFactice.test_analyser_tagger_json) ... ok
test_analyser_tagger_lisible (__main__.TestCliAvecTransportFactice.test_analyser_tagger_lisible) ... ok
test_evaluer_tagger (__main__.TestCliAvecTransportFactice.test_evaluer_tagger) ... ok
test_aide_expose_tagger (__main__.TestDefaultInchange.test_aide_expose_tagger) ... ok
test_analyser_json_sans_tagger (__main__.
… [2142 caractères tronqués]
  ```

- **bash** `{"command": "tmp=$(mktemp -d); env -i HOME=\"$tmp\" PATH=\"$PATH\" python3 tools/drave.py analyser \"Le chat dort.\" --tagger auto > /tmp/auto-no-key.out 2> /tmp/auto-no-key.err; code=$?; echo \"code=$code\"; echo '---stdout---'; cat /tmp/auto-no-key.out; echo '---stderr---'; cat /tmp/auto-no-key.er … [477 caractères tronqués]`

  ```
code=0
---stdout---
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
---stderr---
drave: tagger auto · heuristique (clé absente)
---JSON---
code=0
source heuristique refus '' etiquettes 20
stderr: drave: tagger auto · heuristique (clé absente)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, os, pathlib, subprocess, sys, tempfile, time\nracine = pathlib.Path('.').resolve()\ncache = tempfile.mkdtemp(prefix='auto-cache-')\nenv = dict(os.environ, DEEPSEEK_CACHE=cache)\nt0 = time.perf_counter()\np = subprocess.run([sys.executable, 'tools/drave.py' … [530 caractères tronqués]`

  ```
code 0 duree_s 1.145 stdout_octets 6117
stderr: drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=0.9 s
drave: tagger auto · API (clé présente)
source cascade refus ''
pos [('Le', 'DET', 'neuronal'), ('chat', 'NOUN', 'neuronal'), ('dort', 'VERB', 'neuronal'), ('.', 'PONCT', 'heuristique')]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, os, pathlib, subprocess, sys, tempfile, time\nracine = pathlib.Path('.').resolve()\ntmp = pathlib.Path(tempfile.mkdtemp(prefix='auto-invalid-'))\ncle = tmp / 'bad.key'\ncle.write_text('cle-invalide-sentinelle-auto\\n', encoding='utf-8')\ncache = tmp / 'cac … [799 caractères tronqués]`

  ```
code 0 duree_s 0.727 stdout_octets 5904
stderr: drave: tagger : refus partiel : tagger auto : clé refusée (HTTP 401) ; heuristique
drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=0 · tokens=0 · latence=0.0 s
drave: tagger auto · heuristique (repli : clé refusée (HTTP 401))
source heuristique refus 'tagger auto : clé refusée (HTTP 401) ; heuristique'
pos_sources ['heuristique']
sentinelle_dans_sortie False
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, os, pathlib, subprocess, sys, tempfile, time\nracine = pathlib.Path('.').resolve()\ntmp = pathlib.Path(tempfile.mkdtemp(prefix='auto-network-'))\ncache = tmp / 'cache'\nenv = dict(os.environ, DEEPSEEK_BASE_URL='http://127.0.0.1:9', DEEPSEEK_CACHE=str(cache … [602 caractères tronqués]`

  ```
code 0 duree_s 3.285 stdout_octets 5950
stderr: drave: tagger : refus partiel : tagger auto : neuronal-pos: ErreurDeepSeek: réseau : [Errno 111] Connection refused ; heuristique
drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=0 · cache=0 · tokens=0 · latence=0.0 s
drave: tagger auto · heuristique (repli : neuronal-pos: ErreurDeepSeek: réseau : [Errno 111] Connection refused)
source heuristique refus 'tagger auto : neuronal-pos: ErreurDeepSeek: réseau : [Errno 111] Connection refused ; heuristique'
pos_sources ['heuristique']
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport os, pathlib, subprocess, sys, tempfile, time\nracine = pathlib.Path('.').resolve()\ncache = tempfile.mkdtemp(prefix='auto-cache-readable-')\nenv = dict(os.environ, DEEPSEEK_CACHE=cache)\nt0 = time.perf_counter()\np = subprocess.run([sys.executable, 'tools/drave. … [348 caractères tronqués]`

  ```
code 0 duree_s 1.016
---stdout---
drave 0.1.0 — analyse cascade POS (tagger auto : API DeepSeek, réseau)
langue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)
POS  Le/DET chat/NOUN dort/VERB ./PONCT
SYNTAGMES
  GN   [0:7]   Le chat  rôle=agent     → dort
  GV   [8:12]  dort     rôle=predicat  → chat
PRAGMATIQUE
  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non
COUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·
            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70
TAGGER API  modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=0.8 s

---stderr---
drave: tagger auto · API (clé présente)
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py", "old_string": "    def test_auto_refus_texte_code_3(self) -> None:", "new_string": "    def test_auto_refus_du_modele_repli(self) -> None:\n        \"\"\"Un modèle qui ne rend pas le contrat POS est un re … [929 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_tagger_api.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/tests/test_tagger_api.py 2>&1 | tail -8", "description": "Relancer les tests après ajout du refus modèle"}`

  ```
test_auto_sans_cle_n_importe_pas_le_reseau (__main__.TestTaggerAuto.test_auto_sans_cle_n_importe_pas_le_reseau) ... ok
test_auto_texte_apres_le_drapeau (__main__.TestTaggerAuto.test_auto_texte_apres_le_drapeau)
`--tagger auto TEXTE` ne doit pas avaler le texte comme une valeur de `--tagger`. ... ok

----------------------------------------------------------------------
Ran 30 tests in 7.386s

OK
  ```

- **bash** `{"command": "cat > /tmp/mesure_auto.py <<'PY'\nimport json, os, pathlib, re, subprocess, sys, tempfile, time\n\nRACINE = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\nCLI = RACINE / 'tools' / 'drave.py'\nTEXTE = 'Le chat dort.'\nTEXTE_VIDE = '... !!! ???'\n\ndef env_propre(home, * … [6894 caractères tronqués]`

  ```
code=0
defaut_sans_cle_json code 0 octets 5852 duree 0.192 source heuristique refus  stats {}
auto_sans_cle_json code 0 octets 5852 duree 0.228 source heuristique refus  stats {}
defaut_sans_cle_lisible code 0 octets 593 duree 0.197 source None refus  stats {}
auto_sans_cle_lisible code 0 octets 593 duree 0.192 source None refus  stats {}
auto_cle_presente_json code 0 octets 6117 duree 1.673 source cascade refus  stats {'appels': 1, 'reseau': 1, 'cache': 0, 'tokens': 130, 'latence_s': 1.4}
auto_cle_presente_lisible code 0 octets 710 duree 1.467 source None refus  stats {}
auto_cle_invalide_json code 0 octets 5904 duree 0.704 source heuristique refus tagger auto : clé refusée (HTTP 401) ; heuristique stats {'appels': 1, 'reseau': 0, 'cache': 0, 'tokens': 0, 'latence_s': 0.0}
api_cle_invalide_controle code 4 octets 0 duree 0.655 source None refus  stats {}
auto_reseau_coupe_json code 0 octets 5950 duree 3.303 source heuristique refus tagger auto : neuronal-pos: ErreurDeepSeek: réseau : [Errno 111] Conne stats {'appels': 1, 'reseau': 0, 'cache': 0, 'tokens': 0, 'latence_s': 0.0}
api_reseau_coupe_controle code 0 octets 6253 duree 3.318 source cascade refus neuronal-pos: ErreurDeepSeek:
… [435 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, os, pathlib, re, subprocess, sys, tempfile, time\nracine = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\ncache = tempfile.mkdtemp(prefix='auto-readable-final-')\nenv = dict(os.environ, DEEPSEEK_CACHE=cache)\nt0 = time.perf_counter()\np = … [855 caractères tronqués]`

  ```
{
 "code": 0,
 "duree_s": 1.534,
 "stdout": "drave 0.1.0 — analyse cascade POS (tagger auto : API DeepSeek, réseau)\nlangue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)\nPOS  Le/DET chat/NOUN dort/VERB ./PONCT\nSYNTAGMES\n  GN   [0:7]   Le chat  rôle=agent     → dort\n  GV   [8:12]  dort     rôle=predicat  → chat\nPRAGMATIQUE\n  phrase [0:13] déclarative · acte=assertion · négation=non · modalité=non · double sens=non\nCOUVERTURE  (confiance max par niveau)  graphème=0.99 · mot=0.98 · pos=0.95 · syntagme=0.55 ·\n            phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70\nTAGGER API  modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=1.3 s\n",
 "stderr": "drave: tagger auto · API (clé présente)\n",
 "stats": {
  "modele": "deepseek-chat",
  "appels": 1,
  "reseau": 1,
  "cache": 0,
  "tokens": 130,
  "latence_s": 1.3
 },
 "stdout_octets": 710
}
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/mesure_auto.json'))\nfor nom, r in d['resultats'].items():\n    print('===', nom)\n    print('code', r['code'], 'stdout_octets', r['stdout_octets'], 'duree_s', r['duree_s'])\n    print('source', r['source'], 'refus', repr(r['refus']) … [312 caractères tronqués]`

  ```
=== defaut_sans_cle_json
code 0 stdout_octets 5852 duree_s 0.192
source heuristique refus ''
pos_sources ['heuristique'] tagger_dans_json False
stats {}
stderr ''
=== auto_sans_cle_json
code 0 stdout_octets 5852 duree_s 0.228
source heuristique refus ''
pos_sources ['heuristique'] tagger_dans_json False
stats {}
stderr 'drave: tagger auto · heuristique (clé absente)'
=== defaut_sans_cle_lisible
code 0 stdout_octets 593 duree_s 0.197
source None refus None
pos_sources [] tagger_dans_json False
stats {}
stderr ''
=== auto_sans_cle_lisible
code 0 stdout_octets 593 duree_s 0.192
source None refus None
pos_sources [] tagger_dans_json False
stats {}
stderr 'drave: tagger auto · heuristique (clé absente)'
=== auto_cle_presente_json
code 0 stdout_octets 6117 duree_s 1.673
source cascade refus ''
pos_sources ['heuristique', 'neuronal'] tagger_dans_json False
stats {'appels': 1, 'reseau': 1, 'cache': 0, 'tokens': 130, 'latence_s': 1.4}
stderr 'drave: TAGGER API · modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=130 · latence=1.4 s\ndrave: tagger auto · API (clé présente)'
=== auto_cle_presente_lisible
code 0 stdout_octets 710 duree_s 1.467
source None refus None
pos_sources [] t
… [2601 caractères tronqués]
  ```

- **bash** `{"command": "ls -l reports/rapport-tagger-auto.* 2>/dev/null || echo absent; ls -l docs/produit/README.md tools/drave.py tools/tests/test_tagger_api.py", "description": "Vérifier les fichiers cibles"}`

  ```
absent
-rw-r--r--. 1 stephane stephane 53963 15 nov 12:34 docs/produit/README.md
-rw-------. 1 stephane stephane 61285 15 nov 14:17 tools/drave.py
-rw-------. 1 stephane stephane 36799 15 nov 14:19 tools/tests/test_tagger_api.py
  ```

- **write** `{"content": "{\n  \"tache\": \"Y1 — le prototype du mode auto du tagger\",\n  \"titre\": \"`analyser --tagger auto` : l'API si la clé existe, l'heuristique sinon, sans changer le code de sortie\",\n  \"date\": \"2026-11-15\",\n  \"ligne_roadmap\": \"R0.7 (le lecteur) / B13\",\n  \"head_mesure\": \"f … [13248 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-auto.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np='reports/rapport-tagger-auto.json'\nd=json.load(open(p, encoding='utf-8'))\nprint('JSON OK', len(d), 'clés')\nprint(d['matrice'][0]['cas'], d['matrice'][0]['code'])\nPY", "description": "Valider le JSON du rapport"}`

  ```
JSON OK 17 clés
cle_presente 0
  ```

- **write** `{"content": "# Y1 — le prototype du mode `auto` du tagger : l'API si la clé existe, l'heuristique sinon, sans changer le code de sortie\n\n> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **Y1** (J5, la décision\n> du tagger) · **Date** : 2026-11-15 · **HEAD mesuré** : `f63ad70 … [19636 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-auto.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "offset": 596, "limit": 25}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
596: **La porte produit, mesurée le 07/11** : `✅ porte produit verte` — `drave 0.1.0`, JSON valide et
597: étiqueté en `fr` et `en`, `sha256 f4b7822076a4203d` deux fois, **18 tests** de fumée, **8 tests**
598: de schéma (v2 + rétro-compatibilité v1), **4 tests** sur 50 textes libres, **11 tests** de
599: restitution, **183/183** portes d'autotest ; **12 contrôles**. Le smoke test est
600: `tools/tests/test_produit.py`.
601: 
602: **Codes de sortie — ce qui existe.** Le CLI implémente **0 / 1 / 2 / 3 / 4** :
603: 
604: | code | sens | aujourd'hui |
605: |---:|---|---|
606: | **0** | succès : annotation rendue, évaluation rendue, rejeu identique, restitution rendue | `analyser`, `evaluer`, `rejouer`, `restituer` |
607: | **1** | erreur ; tagger qui refuse une phrase sans POS | argument illisible, divergence de rejeu, exception |
608: | **2** | usage invalide : argument, sous-commande, langue hors `fr`/`en` | `argparse` |
609: | **3** | refus **distinct** de l'erreur, avec l'annotation de refus sur `stdout` | `analyser ""`, `restituer "..."` |
610: | **4** | dépendance absen
… [813 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "offset": 1, "limit": 18}`

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
8: > **Vérifié le 2026-11-14** sur la branche `s/v7`. Le point d'entrée `tools/drave.py` est
9: > **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
10: > existent, et la
11: > porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
12: > § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le format
13: > est **version 2** (`schema: "drave.annotation"`,
14: > `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
15: > reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du
16: > § 3.5 ont été relancées le 07/11 pour le format
… [310 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "> porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,\n> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le format", "new_stri … [390 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "```bash\npython3 tools/drave.py analyser \"Le chat dort.\" --tagger\npython3 tools/drave.py analyser --fichier corpus.txt --jsonl --tagger\npython3 tools/drave.py evaluer --tagger\n```", "new_strin … [256 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "offset": 426, "limit": 22}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
426: | **clé invalide** (HTTP 401/403) | refuse de démarrer, **sans repli** | **4** | vide | `drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.` |
427: | **réseau coupé** (après 3 essais) | **replie** sur l'heuristique | **0** | annotation heuristique | `drave: tagger : refus partiel : neuronal-pos: ErreurDeepSeek: réseau : …` ; JSON `refus` non vide, POS `source=heuristique` |
428: | **refus du modèle** (non JSON, JSON incomplet) | **replie** sur l'heuristique | **0** | annotation heuristique | `drave: tagger : refus partiel : neuronal-pos: ValueError: …` ; JSON `refus` non vide, POS `source=heuristique` |
429: 
430: **Deux familles.** Une **clé absente** ou **refusée** est une dépendance manquante : le run ne
431: peut pas commencer, il sort **4**, rien sur `stdout`, et il ne publie pas un repli déguisé en
432: cascade. Un **réseau coupé** ou un **refus du modèle** est un refus **par phrase** : la cascade
433: garde le POS de
… [1212 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "lisible.\n\n**En `--jsonl`**, une clé refusée peut laisser sur `stdout` les lignes déjà écrites avant le", "new_string": "lisible.\n\n**Le mode `auto` — prototype.** `--tagger auto` choisit la voie … [2364 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "offset": 510, "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md</path>
<type>file</type>
<content>
510: (le test [`test_tagger_api.py`](../../tools/tests/test_tagger_api.py) le compare octet pour
511: octet ; le test W3 piège `socket.socket` et vérifie que `tools.llm.deepseek` n'est pas importé).
512: Le `--tagger` est une **option**, pas un changement de produit : c'est la seule porte qui peut
513: sortir **4** (clé absente ou refusée).
514: 
515: ## 4. Ce que le produit ne fait pas encore
516: 
517: **1. Il ne génère pas de texte.** `restituer` reconstruit la **surface** depuis l'annotation
518: (codec), mais il n'y a **pas de génération** : pas de traduction, pas de réponse libre, pas de
519: paraphrase. Le produit rend des **étiquettes** et, avec `restituer`, la surface qu'elles
520: portent. Les résultats de traduction de la vitrine ([`README.md`](../../README.md)) sont une
521: recherche sur un modèle externe ; ils ne sont pas dans ce produit.
522: 
523: **1 bis. La restitution v2 lit les rôles, pas leur justesse.** `restituer --roles` rend un
524: cadre `agent / prédicat / lieu` lisible, mais la fidélité mesurée sur les 46 textes de la v0
525: est **19/46** cadr
… [1226 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "Le `--tagger` est une **option**, pas un changement de produit : c'est la seule porte qui peut\nsortir **4** (clé absente ou refusée).", "new_string": "Le `--tagger` **explicite** est une **option* … [275 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"dépendance absente : la clé du tagger\" docs/produit/README.md", "description": "Trouver la ligne du code 4"}`

  ```
640:| **4** | dépendance absente : la clé du tagger (absente **ou refusée**) | `--tagger` sans clé, ou clé refusée HTTP 401/403 : message clair, rien sur `stdout`, pas de repli |
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "| **4** | dépendance absente : la clé du tagger (absente **ou refusée**) | `--tagger` sans clé, ou clé refusée HTTP 401/403 : message clair, rien sur `stdout`, pas de repli |", "new_string": "| **4 … [251 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "tmp=$(mktemp -d); env -i HOME=\"$tmp\" PATH=\"$PATH\" python3 tools/drave.py analyser \"Le chat dort.\" --tagger=auto --json >/tmp/eq.json 2>/tmp/eq.err; echo \"code=$?\"; head -c 80 /tmp/eq.json; echo; cat /tmp/eq.err; echo '---help epilogue---'; python3 tools/drave.py --aide 2>&1 | ta … [66 caractères tronqués]`

  ```
code=0
{
 "schema": "drave.annotation",
 "version": 2,
 "texte": "Le chat dort.",
 "lan
drave: tagger auto · heuristique (clé absente)
---help epilogue---
--contexte, --banc, --tagger [auto].
Limites : heuristique CPU, hors ligne, déterministe par défaut ; --tagger appelle l'API
DeepSeek (clé, réseau) pour le POS ; --tagger auto l'appelle seulement si une clé existe,
sinon il rend l'heuristique, sans changer le code de sortie ; la restitution est un codec
de surface (graphème), pas un décodeur neuronal ; ni traduction ni génération.
Exemples :
  python3 tools/drave.py analyser "Le chat dort."
  python3 tools/drave.py analyser "Le chat dort." --tagger
  python3 tools/drave.py analyser "Le chat dort." --tagger auto
  python3 tools/drave.py evaluer --gold --json
  python3 tools/drave.py restituer "Le chat dort."
  python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
  ```

- **todo_write** `{"todos": [{"content": "Implémenter `--tagger auto` dans drave.py (parsing, sélection API/heuristique, messages, coût)", "status": "completed"}, {"content": "Ajouter les tests des quatre cas dans tools/tests/test_tagger_api.py", "status": "completed"}, {"content": "Mesurer les quatre cas réels (clé  … [319 caractères tronqués]`

  ```
Updated todo list: 0 pending, 1 in progress, 5 completed.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -60; echo \"REVUE=$?\"", "description": "Lancer la revue de documentation"}`

  ```
revue de documentation · 759 fiche(s) · 853 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 758 fichiers, le disque en a 759
     · compteurs : en-cours.md dit 852 JSON, le disque en a 853
REVUE=0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -20; echo \"PORTE_TABLEAUX=$?\"", "description": "Lancer la porte des tableaux"}`

  ```
✅ 1835 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4602 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
PORTE_TABLEAUX=0
  ```

- **bash** `{"command": "grep -n \"758\\|852\" docs/pilotage/en-cours.md | head -20", "description": "Trouver les compteurs à mettre à jour"}`

  ```
105:| fichiers / JSON de résultats | **758** / **852** | `reports/*.md` / `reports/*.json` |
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **758** / **852** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **759** / **853** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 98, "limit": 12}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
98: 
99: > Vérifié par `tools/revue_documentation.py`.
100: 
101: | invariant | valeur | contrôle |
102: |---|---|---|
103: | portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
104: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
105: | fichiers / JSON de résultats | **758** / **852** | `reports/*.md` / `reports/*.json` |
106: | documents de `docs/` | **124** (hors archive et README) | `docs/**/*.md` |
107: | dernière passe | **15/11 09 h 53 → 12 h 15** (85, **81/4**) ; rouges `indice`, `melange` (structurelles), `sessions` (**réparée** à 12 h 20), `prechargement` (**environnementale**) ; ciblage W6 **9/9** | `work/portes-1115-09h53/registre.txt` ; `work/portes/w6-final/` |
108: 
109: ## Les chantiers et leurs bloquants

(Showing lines 98-109 of 145. Use offset=110 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **758** / **852** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **759** / **853** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py > /tmp/revue.out 2>&1; code=$?; tail -20 /tmp/revue.out; echo \"REVUE=$code\"", "description": "Relancer la revue et capturer le vrai code"}`

  ```
revue de documentation · 759 fiche(s) · 853 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE=0
  ```

- **bash** `{"command": "sed -n '1,80p' tools/porte-produit.sh", "description": "Voir ce que vérifie la porte produit"}`

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
… [2142 caractères tronqués]
  ```

- **bash** `{"command": "bash tools/porte-produit.sh 2>&1 | tail -20; echo \"PORTE_PRODUIT=${PIPESTATUS[0]}\"", "description": "Lancer la porte produit"}`

  ```
[still running after 60000ms; moved to background job bash-42]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "python3 tools/tests/test_tagger_api.py > /tmp/tests-tagger.log 2>&1; code=$?; tail -6 /tmp/tests-tagger.log; echo \"TESTS=$code\"", "description": "Relancer les tests du tagger"}`

  ```
`--tagger auto TEXTE` ne doit pas avaler le texte comme une valeur de `--tagger`. ... ok

----------------------------------------------------------------------
Ran 30 tests in 6.989s

OK
TESTS=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -10; echo \"EN_COURS=${PIPESTATUS[0]}\"", "description": "Vérifier l'état en-cours"}`

  ```
en-cours · 1627 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EN_COURS=0
  ```

- **bash** `{"command": "git status --short; echo '---DIFF STAT---'; git diff --stat; echo '---DIFF DRAVE (extraits)---'; git diff -- tools/drave.py | sed -n '1,220p'", "description": "Inspecter le diff"}`

  ```
M docs/pilotage/en-cours.md
 M docs/produit/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
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
 M tools/tests/test_tagger_api.py
?? journal/sessions/session-ed9b8942-25a3-48ee-9f86-f6821e56df9d/
?? reports/rapport-s-paragraphes.md
?? reports/rapport-tagger-auto.json
?? reports/rapport-tagger-auto.md
?? tools/protocole_or_roles.py
?? tools/tests/linguistique/gold_reel_50.py
---DIFF STAT---
 docs/pilotage/en-cours.md                          |   2 +-
 docs/produit/README.md                             |  59 +-
 journal/README.md                                  |   3 +-
 journal/sessions/MANIFEST.md                       |   5 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  22 +
 .../rapport.md    
… [11319 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-42", "wait": true, "timeout_ms": 120000}`

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
  ✅ restitution v2 : Ran 17 tests
  ✅ schéma v2 : Ran 8 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
PORTE_PRODUIT=0
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -20; echo \"TAILLE=${PIPESTATUS[0]}\"", "description": "Vérifier le budget de contexte"}`

  ```
3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2733    231   T1   2800  reports/README.md
    2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3997 mots (budget 4 000)

  avertissements :
     · 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-p
… [144 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -15; echo \"JOURNAL=${PIPESTATUS[0]}\"", "description": "Vérifier le journal"}`

  ```
journal · 47 jour(s) · 216 session(s) · 2650 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
JOURNAL=0
  ```

- **bash** `{"command": "python3 tools/verifier_schemas.py 2>&1 | tail -10; echo \"SCHEMAS=${PIPESTATUS[0]}\"", "description": "Vérifier les schémas SVG"}`

  ```
schémas · 464 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
SCHEMAS=0
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-auto.md", "old_string": "**Décision.** **Humaine, non appliquée ici.** Le code livré ne change pas le défaut : sans\n`--tagger`, la commande reste l'heuristique, CPU, hors ligne, déterministe, **0 socket**.", "new_ … [571 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-auto.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-auto.json", "old_string": "  \"decision\": \"humaine, non appliquée dans ce diff : le défaut reste l'heuristique hors ligne\",", "new_string": "  \"decision\": \"humaine, non appliquée dans ce diff : le défaut rest … [285 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-auto.json has been updated successfully.
  ```

- **bash** `{"command": "python3 -c \"import json;json.load(open('reports/rapport-tagger-auto.json'));print('JSON OK')\"", "description": "Valider le JSON après ajout de la note"}`

  ```
JSON OK
  ```

- **bash** `{"command": "git diff -- tools/drave.py | sed -n '220,520p'", "description": "Voir la suite du diff drave.py"}`

  ```
+                # la clé a disparu entre la vérification et la construction : heuristique
+                auto.cle_presente = False
+            else:
+                auto.cascade, auto.stats = cascade, stats_tagger
+                stats = stats_tagger
+        bloc = auto
+        # un texte sans mot ni nombre est un refus d'analyse : on ne paie pas un appel API
+    elif mode == "api":
         # la clé est vérifiée avant toute analyse : sans elle, code 4 (jamais de trace de la clé)
         try:
             cascade, stats_tagger = _construire_tagger(partition=args.partition)
         except CleTaggerAbsente as exc:
             print(f"{NOM}: dépendance absente : {exc}", file=sys.stderr)
             return 4
-        # un texte sans mot ni nombre est un refus d'analyse : on ne paie pas un appel API
-        if any(typ in ("mot", "nombre") for _, _, _, typ in h._mots(texte)):
+        if a_des_mots:
             bloc, stats = cascade, stats_tagger
         # sinon, le refus (code 3) reste celui de l'heuristique
     if args.jsonl:
-        return _analyser_jsonl(texte, args, h, bloc, stats)
+        return _analyser_jsonl(texte, args, h, bloc, stats, auto)
     annotation =
… [8426 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py", "old_string": "                auto.cascade, auto.stats = cascade, stats_tagger\n                stats = stats_tagger\n        bloc = auto\n        # un texte sans mot ni nombre est un refus d'analyse : on ne paie pas un … [303 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/drave.py has been updated successfully.
  ```

- **bash** `{"command": "tmp=$(mktemp -d); env -i HOME=\"$tmp\" PATH=\"$PATH\" python3 tools/drave.py analyser \"Le chat dort. Le chien court.\" --jsonl --tagger auto > /tmp/auto-jsonl.out 2> /tmp/auto-jsonl.err; echo \"code=$?\"; echo '---stdout---'; cat /tmp/auto-jsonl.out | head -2 | cut -c1-100; echo '---st … [87 caractères tronqués]`

  ```
code=0
---stdout---
{"schema": "drave.annotation", "version": 2, "texte": "Le chat dort.", "langue": "fr", "script": "La
{"schema": "drave.annotation", "version": 2, "texte": "Le chien court.", "langue": "fr", "script": "
---stderr---
drave: tagger auto · heuristique (clé absente)
  ```

- **bash** `{"command": "python3 tools/tests/test_tagger_api.py > /tmp/tests-tagger-final.log 2>&1; code=$?; tail -4 /tmp/tests-tagger-final.log; echo \"TESTS=$code\"", "description": "Tests finaux du tagger"}`

  ```
----------------------------------------------------------------------
Ran 30 tests in 7.307s

OK
TESTS=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py > /tmp/revue-final.out 2>&1; code=$?; tail -6 /tmp/revue-final.out; echo \"REVUE=$code\"", "description": "Revue de documentation finale"}`

  ```
revue de documentation · 759 fiche(s) · 853 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE=0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh > /tmp/tableaux-final.out 2>&1; code=$?; tail -6 /tmp/tableaux-final.out; echo \"TABLEAUX=$code\"", "description": "Porte des tableaux finale"}`

  ```
✅ 1835 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4602 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
TABLEAUX=0
  ```

- **bash** `{"command": "git diff --check -- tools/drave.py tools/tests/test_tagger_api.py docs/produit/README.md docs/pilotage/en-cours.md; echo \"DIFF_CHECK=$?\"; python3 -c \"import json;json.load(open('reports/rapport-tagger-auto.json'));print('JSON OK')\"; wc -l reports/rapport-tagger-auto.md reports/rappo … [84 caractères tronqués]`

  ```
DIFF_CHECK=0
JSON OK
  296 reports/rapport-tagger-auto.md
  220 reports/rapport-tagger-auto.json
  516 total
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 110, "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
110: 
111: **Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
112: externes** et la **prochaine action**.
113: 
114: | chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
115: |---|---|---|---|
116: | **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
117: | **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit (J11)** | **`g017` tranché** ; T132/T133, **[gold 452](../../reports/rapport-gold-452.md)** ; **B10.3 bloquée** |
118: | **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)** ; porte propre 2,7856 (manque **0,2856** val / **0,3566** test) ; **[v2](../../reports/rapport-coordination-n2-v2.md)** ; **N3 couvert** (17 portes, inventaire ; deux conditions) ; N4 0/4 ; N5 gelé | **les runs N2** ; puis la **porte propre** ; **N4** |
119: | **R — l
… [2452 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "W6 : [rapport semaine 2](../../reports/rapport-semaine-2.md), tag `semaine-2-2026-11-20` sur `73edb3dd`** ; R2/R3 attendent N5/N4 | **J4 — l'or de rôles** (seconds cadres) ; **Panini** si les 26 … [915 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**R0.7** — `auto` non livré, coût 1 000 extrapolé, fermé 402 ouvert", "new_string": "**R0.7** — `auto` prototype livré (opt-in, défaut inchangé ; décision humaine), coût 1 000 extrapolé, fermé 4 … [11 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -6; echo \"EN_COURS=${PIPESTATUS[0]}\"", "description": "Vérifier en-cours après mise à jour"}`

  ```
en-cours · 1666 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
EN_COURS=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py > /tmp/revue-encours.out 2>&1; code=$?; tail -5 /tmp/revue-encours.out; echo \"REVUE=$code\"", "description": "Revue après mise à jour de en-cours"}`

  ```
revue de documentation · 759 fiche(s) · 853 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE=0
  ```

- **bash** `{"command": "git diff -- docs/produit/README.md | sed -n '1,240p'", "description": "Inspecter le diff complet de la doc produit"}`

  ```
diff --git a/docs/produit/README.md b/docs/produit/README.md
index b077d93a..184a7c11 100644
--- a/docs/produit/README.md
+++ b/docs/produit/README.md
@@ -9,7 +9,10 @@
 > **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
 > existent, et la
 > porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
-> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le format
+> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le
+> **prototype `--tagger auto`** (complété le **2026-11-15**, § 3.7) choisit l'API si une clé
+> existe, l'heuristique sinon, **sans changer le code de sortie** ; il ne change pas le défaut.
+> Le format
 > est **version 2** (`schema: "drave.annotation"`,
 > `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
 > reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du
@@ -387,6 +390,7 @@ python3 tools/drave.py evaluer --reel
 
 ```bash
 python3 tools/drave.py analyser "Le chat dort." --tagger
+python3 tools/drave.py analyser "Le chat dort." --tagger auto
 p
… [6878 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib, subprocess\nbase = subprocess.run(['git', 'show', 'HEAD:docs/produit/README.md'], cwd='.', capture_output=True, text=True, check=True).stdout\nt = base\n# 1. intro\nold = (\"> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défa … [5345 caractères tronqués]`

  ```
écrit 54799 caractères
---DIFF entre la version Y1 seule et le fichier courant---
--- /tmp/readme-y1.md	2026-11-15 14:26:32.550858668 -0500
+++ docs/produit/README.md	2026-11-15 14:21:32.677101408 -0500
@@ -480,10 +480,19 @@
 [`rapport-tagger-option.md`](../../reports/rapport-tagger-option.md).
 
 **Le coût.** **Un appel par phrase** (le tagger de syntagmes, qui était appelé sans contribuer,
-a été retiré), **22 299 tokens** et **155 s** pour les **612 phrases**, soit **~0,02 $**. Le
-**cache** (mémoire par texte + disque du client) rend la seconde analyse gratuite :
-`appels=20 · réseau=0 · cache=20 · tokens=0` sur les 20 phrases rejouées. Les **trois exemples**
-de [`exemples.md`](exemples.md) § 6 totalisent **3 appels**, **441 tokens** et **3,7 s**.
+a été retiré). La référence mesurée est la passe API de W2 sur **452 phrases** : **65 029
+tokens** (55 572 d'entrée + 9 457 de sortie), **447 requêtes** et **443,8 s**. Le **cache**
+(mémoire par texte + disque du client) rend la seconde analyse gratuite : `appels=20 ·
+réseau=0 · cache=20 · tokens=0` sur les 20 phrases rejouées. Les **trois exemples** de
+[`exemples.md`](exemples.md) § 6 totalisent **3 appels**, **441 tokens** et 
… [1787 caractères tronqués]
  ```

- **bash** `{"command": "blob=$(git hash-object -w /tmp/readme-y1.md); git update-index --cacheinfo 100644,\"$blob\",docs/produit/README.md; git add docs/pilotage/en-cours.md reports/rapport-tagger-auto.md reports/rapport-tagger-auto.json tools/drave.py tools/tests/test_tagger_api.py; echo '---STATUS---'; git s … [205 caractères tronqués]`

  ```
---STATUS---
M  docs/pilotage/en-cours.md
MM docs/produit/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
A  reports/rapport-tagger-auto.json
A  reports/rapport-tagger-auto.md
 M tools/chantier/plan.json
M  tools/drave.py
M  tools/tests/test_tagger_api.py
?? journal/sessions/session-ed9b8942-25a3-48ee-9f86-f6821e56df9d/
?? reports/rapport-s-paragraphes.md
?? tools/protocole_or_roles.py
?? tools/tests/linguistique/gold_reel_50.py
---STAGED STAT---
 docs/pilotage/en-cours.md        |   6 +-
 docs/produit/README.md           |  37 ++++-
 reports/rapport-tagger-auto.json | 220 +++++++++++++++++++++++++++++
 reports/rapport-tagger-auto.md   | 296 +++++++++++++++++++++++++++++++++++++++
 tools/drave.py                   | 253 ++++++++++++++++++++++++++++
… [3069 caractères tronqués]
  ```

- **bash** `{"command": "git diff --cached -- docs/produit/README.md | sed -n '1,140p'", "description": "Vérifier la version indexée de la doc"}`

  ```
diff --git a/docs/produit/README.md b/docs/produit/README.md
index b077d93a..4ddf9337 100644
--- a/docs/produit/README.md
+++ b/docs/produit/README.md
@@ -9,7 +9,10 @@
 > **livré** (version **0.1.0**) : `analyser`, `evaluer`, `rejouer`, `restituer` et `--version`
 > existent, et la
 > porte produit est verte. Le **tagger POS par API** est livré **en option** (`--tagger`,
-> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le format
+> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le
+> **prototype `--tagger auto`** (complété le **2026-11-15**, § 3.7) choisit l'API si une clé
+> existe, l'heuristique sinon, **sans changer le code de sortie** ; il ne change pas le défaut.
+> Le format
 > est **version 2** (`schema: "drave.annotation"`,
 > `version: 2`) : le schéma v2 ajoute `meta.partition` et `meta.alternative`, et la **version 1
 > reste lue** ([`tools/schemas/`](../../tools/schemas/)). Les sorties du § 3.1, du § 3.4 et du
@@ -387,6 +390,7 @@ python3 tools/drave.py evaluer --reel
 
 ```bash
 python3 tools/drave.py analyser "Le chat dort." --tagger
+python3 tools/drave.py analyser "Le chat dort." --tagger auto
 p
… [4725 caractères tronqués]
  ```

- **bash** `{"command": "git diff --cached -- docs/pilotage/en-cours.md; echo '---TESTS STAT---'; git diff --cached --stat -- tools/tests/test_tagger_api.py tools/drave.py", "description": "Vérifier le diff en-cours et les stats"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index b84e308e..47dd0756 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -102,7 +102,7 @@
 |---|---|---|
 | portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
 | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
-| fichiers / JSON de résultats | **758** / **852** | `reports/*.md` / `reports/*.json` |
+| fichiers / JSON de résultats | **759** / **853** | `reports/*.md` / `reports/*.json` |
 | documents de `docs/` | **124** (hors archive et README) | `docs/**/*.md` |
 | dernière passe | **15/11 09 h 53 → 12 h 15** (85, **81/4**) ; rouges `indice`, `melange` (structurelles), `sessions` (**réparée** à 12 h 20), `prechargement` (**environnementale**) ; ciblage W6 **9/9** | `work/portes-1115-09h53/registre.txt` ; `work/portes/w6-final/` |
 
@@ -116,7 +116,7 @@ externes** et la **prochaine action**.
 | **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
 | **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183
… [3739 caractères tronqués]
  ```

- **bash** `{"command": "git commit -m \"J5 — Y1 : LE MODE AUTO DU TAGGER (CLÉ 0/130 TOKENS, INVALIDE 0, SANS CLÉ 0 IDENTIQUE AU DÉFAUT, RÉSEAU 0 APRÈS 3 ESSAIS) ; 30/30 TESTS\" 2>&1 | tail -20", "description": "Committer les changements Y1"}`

  ```
[still running after 60000ms; moved to background job bash-63]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **job_output** `{"job_id": "bash-63", "wait": true, "timeout_ms": 120000}`

  ```
✅ index : aucun fait stagé sans état
[s/v7 519b729f] J5 — Y1 : LE MODE AUTO DU TAGGER (CLÉ 0/130 TOKENS, INVALIDE 0, SANS CLÉ 0 IDENTIQUE AU DÉFAUT, RÉSEAU 0 APRÈS 3 ESSAIS) ; 30/30 TESTS
 20 files changed, 3072 insertions(+), 48 deletions(-)
 create mode 100644 journal/sessions/session-ed9b8942-25a3-48ee-9f86-f6821e56df9d/digest.md
 create mode 100644 journal/sessions/session-ed9b8942-25a3-48ee-9f86-f6821e56df9d/rapport.md
 create mode 100644 reports/rapport-tagger-auto.json
 create mode 100644 reports/rapport-tagger-auto.md
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "git show --stat --oneline HEAD; echo '---STATUS---'; git status --short | head -40", "description": "Inspecter le commit et l'état"}`

  ```
519b729f J5 — Y1 : LE MODE AUTO DU TAGGER (CLÉ 0/130 TOKENS, INVALIDE 0, SANS CLÉ 0 IDENTIQUE AU DÉFAUT, RÉSEAU 0 APRÈS 3 ESSAIS) ; 30/30 TESTS
 docs/pilotage/en-cours.md                          |    6 +-
 docs/produit/README.md                             |   37 +-
 journal/2026-11-15/README.md                       |    7 +-
 journal/2026-11-15/distribue.md                    |    2 +-
 journal/2026-11-15/docs.md                         |    2 +-
 journal/2026-11-15/memoire.md                      |    2 +-
 journal/2026-11-15/mesures.md                      |    6 +-
 journal/2026-11-15/modele.md                       |    2 +-
 journal/2026-11-15/outils.md                       |    2 +-
 journal/2026-11-15/portes.md                       |    2 +-
 journal/README.md                                  |    3 +-
 journal/sessions/MANIFEST.md                       |    5 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   29 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 1887 ++++++++++++++++++++
 .../rapport.md                                     |  139 ++
 reports/rapport-tagger-auto.json              
… [729 caractères tronqués]
  ```

- **bash** `{"command": "echo 'HEAD README 65029:'; git show HEAD:docs/produit/README.md | grep -c \"65 029\" || true; echo 'WORKTREE README 65029:'; grep -c \"65 029\" docs/produit/README.md || true; echo '---HEAD Y1---'; git show HEAD:reports/rapport-tagger-auto.md | head -6; echo '---STATUS---'; git status - … [67 caractères tronqués]`

  ```
HEAD README 65029:
0
WORKTREE README 65029:
1
---HEAD Y1---
# Y1 — le prototype du mode `auto` du tagger : l'API si la clé existe, l'heuristique sinon, sans changer le code de sortie

> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **Y1** (J5, la décision
> du tagger) · **Date** : 2026-11-15 · **HEAD mesuré** : `f63ad709` + ce diff · **Verdict** :
> ✅ **le prototype est mesuré** — clé présente → API, **code 0**, **130 tokens** ; clé
> invalide → heuristique, **code 0** (pas 4), `refus` explicite ; clé absente → heuristique,
---STATUS---
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
?? reports/rapport-s-paragraphes.md
?? tools/protocole_or_roles.py
?? tools/tests/linguistique/gold_reel_50.py
  ```

- **bash** `{"command": "test -f reports/rapport-tagger-auto.md && echo FICHE-OK; python3 tools/tests/test_tagger_api.py 2>&1 | tail -1", "description": "Vérifier l'acceptation de la tâche"}`

  ```
FICHE-OK
OK
  ```

- **bash** `{"command": "grep -RIn \"Bearer\\|Authorization\\|cle-secrete\\|sentinelle-auto\" journal/sessions/session-ed9b8942-25a3-48ee-9f86-f6821e56df9d journal/2026-11-15 2>/dev/null | head -20; echo \"GREP=$?\"", "description": "Vérifier l'absence de secret dans le journal commité"}`

  ```
journal/sessions/session-ed9b8942-25a3-48ee-9f86-f6821e56df9d/digest.md:1037:- **bash** `{"command": "python3 - <<'PY'\nimport json, os, pathlib, subprocess, sys, tempfile, time\nracine = pathlib.Path('.').resolve()\ntmp = pathlib.Path(tempfile.mkdtemp(prefix='auto-invalid-'))\ncle = tmp / 'bad.key'\ncle.write_text('cle-invalide-sentinelle-auto\\n', encoding='utf-8')\ncache = tmp / 'cac … [799 caractères tronqués]`
GREP=0
  ```

- **todo_write** `{"todos": [{"content": "Implémenter `--tagger auto` dans drave.py (parsing, sélection API/heuristique, messages, coût)", "status": "completed"}, {"content": "Ajouter les tests des quatre cas dans tools/tests/test_tagger_api.py", "status": "completed"}, {"content": "Mesurer les quatre cas réels (clé  … [317 caractères tronqués]`

  ```
Updated todo list: 0 pending, 0 in progress, 6 completed.
  ```

### 🤖 Assistant

## Y1 livré — le prototype `--tagger auto`

### Ce qui a été fait

- **`tools/drave.py`** : `analyser --tagger auto` choisit la voie.
  - clé trouvée (`DEEPSEEK_KEY_FILE`, `DSH_KEY_FILE`, `~/.config/drave/deepseek.key`, `DEEPSEEK_API_KEY`, `DSH_API_KEY`) → cascade API ;
  - pas de clé → heuristique, **sans importer le module réseau** ;
  - clé invalide ou réseau coupé → **repli heuristique, code 0**, avec `refus` explicite ;
  - refus de texte → **code 3**, aucun appel API ;
  - `--tagger` explicite reste la seule porte qui peut sortir **4** ;
  - message `stderr` disant la voie servie, sans jamais afficher la clé ;
  - coût dans la ligne `TAGGER API` quand l’API a été tentée.
- **`tools/tests/test_tagger_api.py`** : classe `TestTaggerAuto`, **9 tests** ajoutés (30 au total).
- **`reports/rapport-tagger-auto.md`** + **`reports/rapport-tagger-auto.json`**.
- **`docs/produit/README.md`** § 3.7 : tableau des cas `auto`, codes, coût, contrôle négatif.
- **`docs/pilotage/en-cours.md`** : compteurs et état R0.7 mis à jour.

### Les quatre cas mesurés

| cas | code | résultat |
|---|---:|---|
| **clé présente** | **0** | API, `source=cascade`, **130 tokens**, 1,673 s |
| **clé invalide** | **0** (pas 4) | heuristique, `refus="clé refusée (HTTP 401)"` |
| **clé absente** | **0** | heuristique, **stdout identique au défaut octet pour octet** (5 852 octets JSON), `tools.llm.deepseek` non importé |
| **clé + réseau coupé** | **0** | 3 essais, heuristique, `refus` réseau |
| **refus de texte** | **3** | `refus="vide"`, **0 appel API** |

**Contrôle négatif principal** : la même clé invalide sort **0** en `auto`, mais **4** avec `--tagger` explicite, `stdout` vide.

### Validation

- `python3 tools/tests/test_tagger_api.py` → **30 tests, OK**
- `bash tools/porte-produit.sh` → **verte**
- `python3 tools/revue_documentation.py` → **tout passe**
- `bash tools/porte-tableaux.sh` → **verte**
- `python3 tools/verifie_en_cours.py` → **état reprenable**

### Recommandation — décision humaine

La fiche recommande de **garder le défaut heuristique hors ligne** et de traiter `--tagger auto` comme un **prototype opt-in**, jamais comme défaut : le même texte peut changer de POS selon la machine, et le coût n’est pas nul. **Le code ne change pas le défaut** ; la décision reste à l’humain.

Commit : **`519b729f`** — *J5 — Y1 : LE MODE AUTO DU TAGGER (CLÉ 0/130 TOKENS, INVALIDE 0, SANS CLÉ 0 IDENTIQUE AU DÉFAUT, RÉSEAU 0 APRÈS 3 ESSAIS) ; 30/30 TESTS*.

